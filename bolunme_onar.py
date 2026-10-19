# -*- coding: utf-8 -*-
"""
BÖLÜNME ONAR v1.0 — önbellekteki düzeltilmemiş bedelsiz/bölünme günlerini bulur ve geçmişi düzeltir
===================================================================================================
BIST'te günlük fiyat limiti ±%10: tek günde önceki kapanışa göre ≤ 0,62 (ya da ≥ 1,6) oranlı bir açılış işlemle oluşamaz;
bedelsiz sermaye artırımı / bölünme / birleştirme (ya da uzun süreli işlem durdurma sonrası açılış) demektir.
Yahoo BIST bedelsizlerini geriye dönük düzeltmez; BASLAT B2 örtüşme kontrolü de bunu göremez (son 15 gün kendi içinde tutarlı).
Sonuç: önbellekte sahte −%50 çöküşler, çöl kırılımı içinde hayalet zararlar, sahte sol bacaklar.

Yöntem (nedensel değil, tarihsel onarım): olay günü k'da oran f = Open_k / Close_{k-1} (açılış = bedelsiz sonrası referans fiyat).
  f ≤ ESIK_ALT ya da f ≥ ESIK_UST ise k'dan ÖNCEKİ tüm O/H/L/C f ile çarpılır, Volume f'e bölünür.
  Güvenlik: onarım sonrası o günün açılış/önceki kapanış farkı ≤ %15 olmalı (değilse onarılmaz, "şüpheli" listesine yazılır).
  KAPANIŞ DOĞRULAMASI (v1.2): Yahoo'nun açılış fiyatı BIST'te zaman zaman bozuk (ör. 2020-02-28 onlarca hissede ~0,80). Gerçek
  bedelsizde o günün KAPANIŞI da aynı oranda düşer; bozuk açılışta kapanış normal kalır. Close_k/Close_{k-1}, açılış oranından
  %15'ten fazla sapıyorsa olay "açılış hatası" sayılır, onarılmaz. bolunme_dogrula(K): yedekten eski onarımları bu kuralla yeniden tartar.
  Hassasiyet: oran açılıştan tahmin edildiği için ~%0,5 gürültü taşır (BIST referans fiyatı veride yok); %50'lik sahte çöküşün yanında ihmal edilir.
Çıktı: {K}/bolunme_olaylar.csv (sembol, tarih, oran, onarildi), pkl yedeklenir ve yerinde yazılır.
Not: bedelli (rüçhan) artırımlarda referans fiyat da değişir; o gün de yakalanır ve aynı yöntemle düzeltilir — fiyat sürekliliği
için doğru olan budur. Onarım sonrası onbellek_*.pkl (sinyal önbellekleri) ESKİ fiyatları taşır; yeniden kurulmalı.

    exec(open(K + "/bolunme_onar.py", encoding="utf-8").read())
    BO = bolunme_onar(K)            # yalnız rapor: bolunme_onar(K, uygula=False)
"""
from __future__ import annotations

import logging
import os
import pickle
import shutil
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

BO_SURUM = "1.2"
BO_ESIK_ALT = 0.62      # oran bunun altındaysa bölünme/bedelsiz
BO_ESIK_UST = 1.60      # oran bunun üstündeyse birleştirme (ters bölünme)
BO_SUPHE_ALT = 0.85     # 0,62 < oran ≤ 0,85: BIST açılış marjı (±%10) dışında ama bedelsiz mi temettü mü işlem durdurma mı belirsiz → onarılmaz, listelenir
BO_GUVEN = 0.15         # onarım sonrası günlük açılış farkı bu kadar kalmalı
BO_KAPANIS_TOL = 0.15   # KAPANIŞ DOĞRULAMASI: Close_k/Close_{k-1} oranı, açılış oranından en çok bu kadar sapabilir (Yahoo açılış hatasına karşı)
_bo_log = logging.getLogger("bolunme_onar")
if not _bo_log.handlers:
    _h = logging.StreamHandler(sys.stdout)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s bolunme: %(message)s", "%H:%M:%S"))
    _bo_log.addHandler(_h)
_bo_log.setLevel(logging.INFO)
_bo_log.propagate = False

if any(k in globals() for k in ("bo_bul", "bo_onar", "bolunme_onar")) and globals().get("_BO_IMZA") != "bolunme_onar":
    raise RuntimeError("çakışma kapısı: bellekte başka bir bo_* ismi var — yeni oturumda çalıştır")
_BO_IMZA = "bolunme_onar"


def _bo_kol(df: pd.DataFrame) -> Dict[str, Any]:
    kol = {str(c).lower(): c for c in df.columns}
    return {k: kol.get(k) for k in ("open", "high", "low", "close", "volume")}


def bo_supheli(df: pd.DataFrame, alt: float = BO_ESIK_ALT, ust: float = BO_SUPHE_ALT) -> List[Tuple[int, float]]:
    """Onarılmayan ara bölge: alt < oran ≤ ust (açılış marjı dışında ama oran küçük). Yalnız raporlanır."""
    return [(i, f) for i, f in bo_bul(df, esik_alt=ust, esik_ust=99.0) if f > alt]


def bo_bul(df: pd.DataFrame, esik_alt: float = BO_ESIK_ALT, esik_ust: float = BO_ESIK_UST) -> List[Tuple[int, float]]:
    """Tek hissede bölünme günleri: [(indeks, oran)] — oran = Open_k / Close_{k-1}; Open yoksa Close_k / Close_{k-1}."""
    k = _bo_kol(df)
    if k["close"] is None or len(df) < 2:
        return []
    C = pd.to_numeric(df[k["close"]], errors="coerce").to_numpy(float)
    O = pd.to_numeric(df[k["open"]], errors="coerce").to_numpy(float) if k["open"] is not None else C
    onc = np.roll(C, 1); onc[0] = np.nan
    ref = np.where(np.isfinite(O) & (O > 0), O, C)
    with np.errstate(divide="ignore", invalid="ignore"):
        oran = ref / onc
    idx = np.flatnonzero(np.isfinite(oran) & ((oran <= esik_alt) | (oran >= esik_ust)) & (onc > 0))
    return [(int(i), float(oran[i])) for i in idx]


def bo_onar(df: pd.DataFrame, olaylar: List[Tuple[int, float]], guven: float = BO_GUVEN, kapanis_tol: float = BO_KAPANIS_TOL) -> Tuple[pd.DataFrame, List[Dict[str, Any]]]:
    """Olayları SONDAN başa uygular (her olay kendinden önceki tüm barları çarpar). Döner: (onarılmış df, kayıtlar)."""
    k = _bo_kol(df)
    out = df.copy(); kayit: List[Dict[str, Any]] = []
    fiyat_kol = [k[c] for c in ("open", "high", "low", "close") if k[c] is not None]
    for c in fiyat_kol + ([k["volume"]] if k["volume"] is not None else []):
        out[c] = pd.to_numeric(out[c], errors="coerce").astype(float)         # int64 hacim → float (uyarı/ hata önlenir)
    for i, f in sorted(olaylar, key=lambda x: -x[0]):
        onceki = float(pd.to_numeric(out[k["close"]], errors="coerce").iloc[i - 1])
        acilis = float(pd.to_numeric(out[k["open"]], errors="coerce").iloc[i]) if k["open"] is not None else float(out[k["close"]].iloc[i])
        kapanis = float(pd.to_numeric(out[k["close"]], errors="coerce").iloc[i])
        f_kap = kapanis / onceki if onceki > 0 else np.nan
        kap_ok = np.isfinite(f_kap) and abs(f_kap / f - 1) <= kapanis_tol
        yeni_onceki = onceki * f
        fark = abs(acilis / yeni_onceki - 1) if yeni_onceki > 0 else np.inf
        ok = np.isfinite(fark) and fark <= guven and kap_ok
        kayit.append({"tarih": out.index[i], "oran": f, "oran_kapanis": float(f_kap) if np.isfinite(f_kap) else np.nan, "onceki_kapanis": onceki, "acilis": acilis,
                      "kapanis": kapanis, "onarildi": bool(ok), "neden": "" if ok else ("acilis_hatasi" if not kap_ok else "fark_buyuk"),
                      "kalan_fark": float(fark) if np.isfinite(fark) else np.nan})
        if not ok:
            continue
        for c in fiyat_kol:
            out.iloc[:i, out.columns.get_loc(c)] = pd.to_numeric(out[c], errors="coerce").iloc[:i] * f
        if k["volume"] is not None:
            out.iloc[:i, out.columns.get_loc(k["volume"])] = pd.to_numeric(out[k["volume"]], errors="coerce").iloc[:i] / f
    return out, kayit


def bolunme_onar(K: str, veri_ad: str = "veri_1d_turkey.pkl", uygula: bool = True) -> Dict[str, Any]:
    yol = os.path.join(K, veri_ad)
    P = pickle.load(open(yol, "rb"))
    sarmal = isinstance(P, dict) and isinstance(P.get("veri"), dict)
    V: Dict[str, pd.DataFrame] = P["veri"] if sarmal else P
    satir: List[Dict[str, Any]] = []; degisen = 0; t0 = time.monotonic(); ara: List[str] = []
    for s, df in V.items():
        try:
            for i, f in bo_supheli(df):
                C = pd.to_numeric(df[_bo_kol(df)["close"]], errors="coerce")
                fk = float(C.iloc[i] / C.iloc[i - 1]) if i > 0 and C.iloc[i - 1] > 0 else np.nan
                etiket = "KAPANIŞ DOĞRULUYOR (gerçek düşüş/bedelsiz)" if np.isfinite(fk) and abs(fk / f - 1) <= BO_KAPANIS_TOL else "açılış hatası"
                ara.append(f"{s} {pd.Timestamp(df.index[i]).date()} açılış {f:.3f} kapanış {fk:.3f} → {etiket}")
            ol = bo_bul(df)
            if not ol:
                continue
            yeni, kayit = bo_onar(df, ol)
            for r in kayit:
                r["sembol"] = s; satir.append(r)
            if uygula and any(r["onarildi"] for r in kayit):
                V[s] = yeni; degisen += 1
        except Exception as e:
            _bo_log.warning("%s: %s", s, e)
    O = pd.DataFrame(satir)
    if len(O):
        O = O[["sembol", "tarih", "oran", "oran_kapanis", "onceki_kapanis", "acilis", "kapanis", "onarildi", "neden", "kalan_fark"]].sort_values(["tarih", "sembol"]).reset_index(drop=True)
        O.to_csv(os.path.join(K, "bolunme_olaylar.csv"), index=False)
    if uygula and degisen:
        shutil.copy(yol, yol + time.strftime(".yedek_bolunme_%Y%m%d_%H%M"))
        if sarmal:
            P["veri"] = V
            if isinstance(P.get("kayit"), dict):
                P["kayit"]["bolunme_onar"] = {"surum": BO_SURUM, "tarih": str(pd.Timestamp.now()), "hisse": degisen, "olay": int(O["onarildi"].sum())}
        tmp = yol + ".tmp"; pickle.dump(P, open(tmp, "wb")); os.replace(tmp, yol)
    n_ol = int(len(O)); n_on = int(O["onarildi"].sum()) if n_ol else 0
    print(f"BÖLÜNME ONAR v{BO_SURUM}: {len(V)} hissede {n_ol} bölünme/bedelsiz günü bulundu, {n_on} onarıldı ({degisen} hisse), "
          f"{n_ol - n_on} şüpheli (onarılmadı) | {'pkl yazıldı, yedek alındı' if uygula and degisen else 'pkl DEĞİŞMEDİ'} | {time.monotonic() - t0:.0f}s")
    if n_ol:
        yil = O[O["onarildi"]].assign(yil=lambda d: pd.to_datetime(d["tarih"]).dt.year).groupby("yil").size()
        print("  yıla göre onarılan:", ", ".join(f"{y}:{n}" for y, n in yil.items()))
        sup = O[~O["onarildi"]]
        if len(sup):
            print("  onarılmayan:", "; ".join(f"{r.sembol} {pd.Timestamp(r.tarih).date()} açılış {r.oran:.3f} kapanış {r.oran_kapanis:.3f} [{r.neden}]" for r in sup.head(25).itertuples()))
    if ara:
        gercek = [a for a in ara if "DOĞRULUYOR" in a]
        print(f"  ara bölge (0,62–0,85; onarılmadı): {len(ara)} gün, kapanışın doğruladığı {len(gercek)} (bunlar bedelsiz/temettü/durdurma — elle bak), kalanı açılış hatası")
        if gercek:
            print("  kapanışın doğruladıkları: " + "; ".join(gercek[:40]) + (" ..." if len(gercek) > 40 else ""))
        pd.DataFrame({"kayit": ara}).to_csv(os.path.join(K, "bolunme_ara_bolge.csv"), index=False)
    return {"olaylar": O, "degisen_hisse": degisen, "ara_bolge": ara}


def bolunme_dogrula(K: str, veri_ad: str = "veri_1d_turkey.pkl") -> Dict[str, Any]:
    """Önceki (v1.0/1.1) onarımı yedekten yeniden tartar: kapanışın doğrulamadığı olaylar varsa o hisseler yedekteki haline döner,
    kapanışın doğruladıkları yeniden onarılır. En eski 'yedek_bolunme' yedeği esas alınır (ham veri)."""
    yol = os.path.join(K, veri_ad)
    yedekler = sorted(f for f in os.listdir(K) if f.startswith(veri_ad + ".yedek_bolunme_"))
    if not yedekler:
        print("yedek_bolunme yok — doğrulanacak eski onarım yok"); return {}
    Py = pickle.load(open(os.path.join(K, yedekler[0]), "rb"))
    Vy: Dict[str, pd.DataFrame] = Py["veri"] if isinstance(Py, dict) and isinstance(Py.get("veri"), dict) else Py
    P = pickle.load(open(yol, "rb"))
    sarmal = isinstance(P, dict) and isinstance(P.get("veri"), dict)
    V: Dict[str, pd.DataFrame] = P["veri"] if sarmal else P
    geri = 0; satir: List[Dict[str, Any]] = []
    for s, df in Vy.items():
        ol = bo_bul(df)
        if not ol:
            continue
        yeni, kayit = bo_onar(df, ol)
        for r in kayit:
            r["sembol"] = s; satir.append(r)
        V[s] = yeni                                   # kapanışın doğruladıkları onarılmış, doğrulamadıkları ham kalır
        if any(not r["onarildi"] for r in kayit):
            geri += 1
    O = pd.DataFrame(satir)
    if len(O):
        O = O[["sembol", "tarih", "oran", "oran_kapanis", "onceki_kapanis", "acilis", "kapanis", "onarildi", "neden", "kalan_fark"]].sort_values(["tarih", "sembol"]).reset_index(drop=True)
        O.to_csv(os.path.join(K, "bolunme_olaylar.csv"), index=False)
    if sarmal:
        P["veri"] = V
    tmp = yol + ".tmp"; pickle.dump(P, open(tmp, "wb")); os.replace(tmp, yol)
    n_on = int(O["onarildi"].sum()) if len(O) else 0
    print(f"BÖLÜNME DOĞRULA: yedek {yedekler[0]} → {len(O)} olay yeniden tartıldı: {n_on} kapanışla doğrulandı ve onarıldı, {len(O) - n_on} açılış hatası (ham bırakıldı, {geri} hisse)")
    if len(O) and (~O["onarildi"]).any():
        print("  açılış hatası sayılanlar: " + "; ".join(f"{r.sembol} {pd.Timestamp(r.tarih).date()} açılış {r.oran:.3f} kapanış {r.oran_kapanis:.3f}" for r in O[~O["onarildi"]].itertuples()))
    return {"olaylar": O, "geri_alinan_hisse": geri}
