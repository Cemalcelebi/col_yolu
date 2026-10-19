# -*- coding: utf-8 -*-
"""
YENİDEN TARA v1.0 — Çöl sinyal listesini BUGÜNKÜ kodla (col_olc) ve onarılmış veriyle baştan üretir; kaldığı yerden sürer
=======================================================================================================================
Neden: zincir denetimi 6. halka, d (v1_final_BIST.csv) listesindeki segment ölçülerinin (uzunluk, clv) bugünkü col_olc ile
%25 oranında uyuşmadığını gösterdi → liste eski bir Çöl tanımıyla üretilmiş. Canlıda gun() bugünkü kodu çalıştırıyor;
ölçülen sayı canlı kuralın sayısı olsun diye liste aynı tarihlerde yeniden üretilir.

Çatlak olmaması için:
  • Tarama mantığı COL_v1.tara() ile BİREBİR aynı (aynı sıra, aynı eşikler, aynı atlama kuralları); tek fark kaldığı yerden
    sürmesi ve yon='YOK' satırlarını da saklaması (v2 listesi tara() gibi yalnız YUKARI/ASAGI satırlarını içerir).
    Test T1 bunu tara()'nın kopyasıyla, Colab hücresi ise gerçek tara() ile canlı doğrular.
  • Tarih listesi tahmin edilmez: d ve d23'teki tarihlerin kendisi kullanılır (yt_tarihler).
  • ileri (ufuk) tahmin edilmez: d'deki 'getiri' sütunu hangi ufukla üretilmişse o bulunur (yt_ileri_bul); bulunamazsa durur.
  • Veri imzası: tarama birden çok oturuma yayılırsa, aradaki oturumda tarihsel barlar değişmişse (onarım vb.) uyarır ve
    o hisseleri baştan tarar (yeni bar eklenmesi imzayı değiştirmez: imza yalnız son tarama tarihine kadar olan barlardan alınır).
  • Her tarih bitince durum dosyasına yazılır ({K}/yeniden_tara_{ad}.pkl); çökme/kesilme sonrası aynı çağrı kaldığı yerden sürer.
  • Bitince v2_{ad}.csv yazılır ve eski liste ile karşılaştırma raporu üretilir (yt_karsilastir).

    exec(open(K + "/yeniden_tara.py", encoding="utf-8").read())
    d2 = yeniden_tara(K, VERI, d, "2024_26", col_olc, AL_PAY)       # kaldığı yerden sürer; bitince v2_2024_26.csv
    d2_23 = yeniden_tara(K, VERI, d23, "2023", col_olc, AL_PAY)
"""
from __future__ import annotations

import logging
import os
import pickle
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

YT_SURUM = "1.0"
YT_SUTUNLAR = ["sembol", "tarih", "yon", "clv", "bant_son", "ortaust", "uzunluk", "doji", "alt_fitil", "dar", "gecerli_oran",
               "onceki_250", "GECER", "getiri", "taban", "tavan"]          # tara() sütunları + taban/tavan (nedensellik için)
YT_UFUKLAR = (20, 30, 40, 60, 80, 100, 120)

_yt_log = logging.getLogger("yeniden_tara")
if not _yt_log.handlers:
    _h = logging.StreamHandler(sys.stdout); _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s yt: %(message)s", "%H:%M:%S"))
    _yt_log.addHandler(_h); _yt_log.setLevel(logging.INFO)


# ---------------------------------------------------------------- yardımcılar
def _yt_veri(V: Any) -> Dict[str, pd.DataFrame]:
    V = V["veri"] if isinstance(V, dict) and isinstance(V.get("veri"), dict) else V
    return {str(s): df for s, df in V.items() if isinstance(df, pd.DataFrame) and "Close" in df.columns}


def yt_tarihler(d: pd.DataFrame) -> List[pd.Timestamp]:
    """Eski listedeki tarama tarihlerinin kendisi (tahmin yok)."""
    t = pd.to_datetime(d["tarih"]).dt.normalize().drop_duplicates().sort_values()
    return [pd.Timestamp(x) for x in t]


def yt_ileri_bul(d: pd.DataFrame, veri: Dict[str, pd.DataFrame], ornek: int = 40, seed: int = 3) -> Tuple[Optional[int], Dict[int, float]]:
    """d['getiri'] = (ileri. barın kapanışı / sinyal günü kapanışı − 1)×100 hangi ileri ile tutuyor? Tolerans %0,05 puan.
    Veri onarılmış olabilir (bedelsiz): tutmayan örnekler sayılmaz, en çok tutan ufuk seçilir; hiçbiri %60'ı geçmezse None."""
    if "getiri" not in d.columns:
        return None, {}
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(d), size=min(ornek, len(d)), replace=False)
    skor: Dict[int, float] = {u: 0.0 for u in YT_UFUKLAR}; n = 0
    for j in idx:
        r = d.iloc[j]; df = veri.get(str(r["sembol"]))
        if df is None:
            continue
        T = pd.Timestamp(r["tarih"]).normalize(); x = df[df.index <= T]; il = df[df.index > T]
        if len(x) == 0 or len(il) < max(YT_UFUKLAR):
            continue
        p0 = float(x["Close"].iloc[-1]); n += 1
        for u in YT_UFUKLAR:
            g = (float(il["Close"].iloc[u - 1]) / p0 - 1) * 100
            if abs(g - float(r["getiri"])) < 0.05:
                skor[u] += 1
    if n == 0:
        return None, {}
    oran = {u: v / n for u, v in skor.items()}
    en = max(oran, key=oran.get)
    return (en if oran[en] >= 0.6 else None), oran


def yt_imza(veri: Dict[str, pd.DataFrame], son_tarih: pd.Timestamp) -> Dict[str, Tuple[int, float]]:
    """Hisse başına (bar sayısı, kapanış toplamı) — yalnız son tarama tarihine kadar: sonradan eklenen bar imzayı değiştirmez, onarım değiştirir."""
    im = {}
    for s, df in veri.items():
        x = df[df.index <= son_tarih]
        im[s] = (int(len(x)), round(float(x["Close"].sum()), 4) if len(x) else 0.0)
    return im


# ---------------------------------------------------------------- bir tarih (tara() ile birebir)
def yt_bir_tarih(T: pd.Timestamp, veri: Dict[str, pd.DataFrame], col_olc: Callable, al_pay: float, ileri: int = 60,
                 semboller: Optional[Sequence[str]] = None) -> List[Dict[str, Any]]:
    """COL_v1.tara() iç döngüsünün kopyası. Fark: yon='YOK' satırları da döner (tara atar) ve taban/tavan saklanır."""
    Ts = pd.Timestamp(T); R: List[Dict[str, Any]] = []
    for s in (semboller if semboller is not None else list(veri)):
        df = veri[s]
        x = df[df.index <= Ts]
        if len(x) < 250:
            continue
        try:
            o = col_olc(df, Ts)
        except Exception as e:
            _yt_log.debug("%s@%s col_olc: %s", s, Ts.date(), e); o = None
        if not o:
            continue
        il = df[df.index > Ts].head(ileri)
        if len(il) < 20:
            continue
        p0 = float(x["Close"].iloc[-1]); yon = "YOK"
        for c in il["Close"].to_numpy(float):
            if c > o["tavan"] * al_pay:
                yon = "YUKARI"; break
            if c < o["taban"]:
                yon = "ASAGI"; break
        R.append({"sembol": s, "tarih": Ts, "yon": yon, "clv": o["clv"], "bant_son": o["bant_son"], "ortaust": o["ortaust"],
                  "uzunluk": o["uzunluk"], "doji": o["doji"], "alt_fitil": o["alt_fitil"], "dar": o["dar"], "gecerli_oran": o["gecerli_oran"],
                  "onceki_250": o.get("onceki_250"), "GECER": o["GECER"], "getiri": (float(il["Close"].iloc[-1]) / p0 - 1) * 100,
                  "taban": o["taban"], "tavan": o["tavan"]})
    return R


# ---------------------------------------------------------------- kaldığı yerden süren tarama
def _yt_bos() -> Dict[str, Any]:
    return {"surum": YT_SURUM, "bitti": [], "satirlar": [], "imza": None, "ileri": None, "al_pay": None, "tarihler": None}


def yt_durum_oku(yol: str) -> Dict[str, Any]:
    if os.path.exists(yol):
        try:
            with open(yol, "rb") as f:
                D = pickle.load(f)
            if isinstance(D, dict) and "bitti" in D and "satirlar" in D:
                return D
            _yt_log.warning("durum dosyası beklenmeyen biçimde, sıfırdan: %s", yol)
        except Exception as e:
            _yt_log.warning("durum dosyası okunamadı (%s), sıfırdan: %s", e, yol)
    return _yt_bos()


def yt_durum_yaz(yol: str, D: Dict[str, Any]) -> None:
    gecici = yol + ".tmp"
    with open(gecici, "wb") as f:
        pickle.dump(D, f, protocol=4)
    os.replace(gecici, yol)                     # yarım yazılmış durum dosyası kalmasın


def yt_calistir(K: str, veri: Dict[str, pd.DataFrame], tarihler: Sequence[pd.Timestamp], ad: str, col_olc: Callable, al_pay: float,
                ileri: int = 60, kaydet_her: int = 1) -> pd.DataFrame:
    """Tarihleri sırayla tarar; her `kaydet_her` tarihte durumu yazar. Aynı çağrı kesilmeden sonra kaldığı yerden sürer.
    Parametre (ileri, al_pay, tarih listesi) değişmişse eski durum geçersizdir → sıfırdan başlar ve söyler."""
    yol = os.path.join(K, f"yeniden_tara_{ad}.pkl")
    tarihler = [pd.Timestamp(t).normalize() for t in tarihler]
    D = yt_durum_oku(yol)
    anahtar = {"ileri": int(ileri), "al_pay": float(al_pay), "tarihler": [str(t.date()) for t in tarihler]}
    if D["bitti"] and any(D.get(k) != v for k, v in anahtar.items()):
        _yt_log.warning("%s: parametre/tarih listesi değişmiş (eski ileri=%s al_pay=%s, %s tarih) → sıfırdan", ad, D.get("ileri"), D.get("al_pay"), len(D.get("tarihler") or []))
        D = _yt_bos()
    D.update(anahtar)
    imza = yt_imza(veri, max(tarihler))
    if D["bitti"]:
        degisen = sorted(s for s in imza if D["imza"] is not None and D["imza"].get(s) != imza[s])
        if degisen:
            _yt_log.warning("%s: %d hissenin tarihsel barları değişmiş (ör. %s) → o hisseler bitmiş tarihlerde yeniden taranıyor",
                            ad, len(degisen), ", ".join(degisen[:6]))
            D["satirlar"] = [r for r in D["satirlar"] if r["sembol"] not in degisen]
            t0 = time.monotonic()
            for i, T in enumerate([t for t in tarihler if str(t.date()) in D["bitti"]], 1):
                D["satirlar"].extend(yt_bir_tarih(T, veri, col_olc, al_pay, ileri, semboller=[s for s in degisen if s in veri]))
            _yt_log.info("%s: değişen hisseler yeniden tarandı (%.0fs)", ad, time.monotonic() - t0)
    D["imza"] = imza
    kalan = [t for t in tarihler if str(t.date()) not in D["bitti"]]
    _yt_log.info("%s: %d tarih, %d bitmiş, %d kalan | hisse %d | ileri=%d al_pay=%s", ad, len(tarihler), len(D["bitti"]), len(kalan), len(veri), ileri, al_pay)
    t0 = time.monotonic(); yapilan = 0
    for T in kalan:
        t1 = time.monotonic()
        R = yt_bir_tarih(T, veri, col_olc, al_pay, ileri)
        D["satirlar"].extend(R); D["bitti"].append(str(T.date())); yapilan += 1
        if yapilan % kaydet_her == 0:
            yt_durum_yaz(yol, D)
        n_sin = sum(1 for r in R if r["yon"] != "YOK"); n_gec = sum(1 for r in R if r["yon"] != "YOK" and r["GECER"])
        gec = time.monotonic() - t0; kalan_sn = gec / yapilan * (len(kalan) - yapilan)
        print(f"  {len(D['bitti'])}/{len(tarihler)} {T.date()} -> {n_sin} sinyal ({n_gec} GECER) | {time.monotonic() - t1:.0f}s | kalan ~{kalan_sn / 60:.0f} dk", flush=True)
    yt_durum_yaz(yol, D)
    S = pd.DataFrame(D["satirlar"], columns=YT_SUTUNLAR)
    if len(S):
        S = S.drop_duplicates(subset=["sembol", "tarih"], keep="last").sort_values(["tarih", "sembol"]).reset_index(drop=True)
    return S


# ---------------------------------------------------------------- karşılaştırma
def yt_karsilastir(d_eski: pd.DataFrame, d_yeni: pd.DataFrame) -> Dict[str, Any]:
    """Aynı (sembol, tarih) üzerinde eski ↔ yeni: GECER uyumu, yalnız eskide / yalnız yenide olan sinyaller, sütun farkları."""
    e = d_eski.copy(); y = d_yeni[d_yeni["yon"] != "YOK"].copy()
    sadece_gecer = bool(e["GECER"].astype(bool).all()) if len(e) else False       # eski liste yalnız GECER ise (d23 gibi) yeniyi de GECER'e indir
    if sadece_gecer:
        y = y[y["GECER"].astype(bool)]
    for t in (e, y):
        t["sembol"] = t["sembol"].astype(str).str.upper().str.replace(".IS", "", regex=False)
        t["tarih"] = pd.to_datetime(t["tarih"]).dt.normalize()
    e = e.drop_duplicates(subset=["sembol", "tarih"]); y = y.drop_duplicates(subset=["sembol", "tarih"])
    m = e.merge(y, on=["sembol", "tarih"], how="outer", suffixes=("_e", "_y"), indicator=True)
    ortak = m[m["_merge"] == "both"]; yalniz_e = m[m["_merge"] == "left_only"]; yalniz_y = m[m["_merge"] == "right_only"]
    R: Dict[str, Any] = {"eski": len(e), "yeni": len(y), "ortak": len(ortak), "yalniz_eski": len(yalniz_e), "yalniz_yeni": len(yalniz_y),
                         "eski_gecer": int(e["GECER"].astype(bool).sum()), "yeni_gecer": int(y["GECER"].astype(bool).sum())}
    if len(ortak):
        ge, gy = ortak["GECER_e"].astype(bool), ortak["GECER_y"].astype(bool)
        R["gecer_ayni"] = int((ge == gy).sum()); R["gecer_e1_y0"] = int((ge & ~gy).sum()); R["gecer_e0_y1"] = int((~ge & gy).sum())
        R["yon_ayni"] = int((ortak["yon_e"] == ortak["yon_y"]).sum())
        R["uzunluk_ayni"] = int((ortak["uzunluk_e"].astype(float).round() == ortak["uzunluk_y"].astype(float).round()).sum())
        R["clv_ayni"] = int(((ortak["clv_e"].astype(float) - ortak["clv_y"].astype(float)).abs() <= 0.0015).sum())
    R["yalniz_eski_gecer"] = int(yalniz_e["GECER_e"].astype(bool).sum()) if len(yalniz_e) else 0
    R["yalniz_yeni_gecer"] = int(yalniz_y["GECER_y"].astype(bool).sum()) if len(yalniz_y) else 0
    R["sadece_gecer"] = sadece_gecer
    s = [("(eski liste yalnız GECER → yeni de GECER'e indirildi) " if sadece_gecer else "") + f"eski {R['eski']} sinyal (GECER {R['eski_gecer']}) | yeni {R['yeni']} (GECER {R['yeni_gecer']})",
         f"ortak {R['ortak']} | yalnız eskide {R['yalniz_eski']} (GECER {R['yalniz_eski_gecer']}) | yalnız yenide {R['yalniz_yeni']} (GECER {R['yalniz_yeni_gecer']})"]
    if len(ortak):
        s.append(f"ortaklarda: GECER aynı {R['gecer_ayni']}/{R['ortak']} (eski1→yeni0 {R['gecer_e1_y0']}, eski0→yeni1 {R['gecer_e0_y1']}) | yön aynı {R['yon_ayni']} | uzunluk aynı {R['uzunluk_ayni']} | clv aynı {R['clv_ayni']}")
    R["rapor"] = "\n".join(s)
    return R


# ---------------------------------------------------------------- uçtan uca
def yeniden_tara(K: str, VERI: Any, d_eski: pd.DataFrame, ad: str, col_olc: Callable, al_pay: float, ileri: Optional[int] = None,
                 yaz: bool = True) -> pd.DataFrame:
    """Eski listenin tarihlerinde bugünkü kodla yeni liste. ileri verilmezse d_eski['getiri']'den bulunur; bulunamazsa durur (tahmin yok).
    Çıktı: {K}/v2_{ad}.csv (yalnız YUKARI/ASAGI, tara() ile aynı anlam) + {K}/v2_{ad}_tum.csv (YOK dahil) + karşılaştırma raporu."""
    veri = _yt_veri(VERI)
    tarihler = yt_tarihler(d_eski)
    if ileri is None:
        ileri, oran = yt_ileri_bul(d_eski, veri)
        _yt_log.info("%s: getiri ufku tahmini: %s", ad, {u: round(v, 2) for u, v in oran.items()})
        if ileri is None:
            raise ValueError(f"{ad}: eski listenin getiri ufku belirlenemedi; ileri= elle ver")
    S = yt_calistir(K, veri, tarihler, ad, col_olc, al_pay, ileri=ileri)
    S2 = S[S["yon"] != "YOK"].reset_index(drop=True)
    R = yt_karsilastir(d_eski, S)
    rapor = (f"YENİDEN TARA v{YT_SURUM} [{ad}] {len(tarihler)} tarih ({tarihler[0].date()} → {tarihler[-1].date()}), ileri={ileri}, AL_PAY={al_pay}, hisse {len(veri)}\n"
             + R["rapor"])
    if yaz:
        S2.to_csv(os.path.join(K, f"v2_{ad}.csv"), index=False)
        S.to_csv(os.path.join(K, f"v2_{ad}_tum.csv"), index=False)
        with open(os.path.join(K, f"v2_{ad}_rapor.txt"), "w", encoding="utf-8") as f:
            f.write(rapor + "\n")
        _yt_log.info("%s: v2_%s.csv (%d satır) yazıldı", ad, ad, len(S2))
    print(rapor)
    return S2
