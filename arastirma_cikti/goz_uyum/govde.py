"""GOVDE — GÖVDE TEPKİSİ TANIMI: Cemal'in 'dipte fitil değil GÖVDE ile tepki' gözünü ölçülebilir tanıma çevirme  (23 Kasım 2026)

GETİRİ ÖLÇMEZ. Sinyal sonrası fiyat hiçbir adımda okunmaz: G1-G4 yalnız kör sayfa penceresinden (tanim2.tz_pencere = goz_uyum._gu_pencere;
veri sinyal günü t'de KESİLİR, son 121 geçerli bar), bunun da yalnız son 40 mumundan [t-39..t] (ATR14 için [t-14..t]) hesaplanır.
Cemal'in sözü (23.11.2026): "dip delinmiş mi tamam, bu kolay, ancak bu yeterli değil; çünkü mumların fitili değil GÖVDE ile tepki alması
gerekir bu diplerde." Eski kural: "dip oluşumu + alt fitili az mumlar + dip savunması = yön yukarı".
Komutlar (repo kökünden):
  python arastirma_cikti/goz_uyum/govde.py anahtar            ADIM 2 + 3: ilk 40 sayfa + cemal_isaret.json -> eşik / GOVDE_1 / GOVDE_2 seçimi;
                                                              ikinci setin 40 sayfası (tanim2_anahtar.json) için G1-G4 + yanıtlar -> govde_anahtar.json
  python arastirma_cikti/goz_uyum/govde.py muhur              sha'lar + seçim kuralı + hüküm + kontrol tablosu -> GOVDE_ON_KAYIT.md (kontrol kapısı)
  python arastirma_cikti/goz_uyum/govde.py olc --cemal J.json mühür denetimi (govde + tanim2) -> GOVDE_SONUC.md (J.json: {"1": "VAR", "2": "YOK", ...})
  python arastirma_cikti/goz_uyum/govde.py test               çakışma kapısı + prefix değişmezliği + sabit yönlü eşik seçimi sağlaması
Veri: /tmp/kasa2/acik (V_ABD.pkl, V_AVR.pkl), /tmp/kasa/acik/V_BIST.pkl (goz_uyum.GU_VERI).  Kod değiştiyse çalışma zamanını yeniden başlat.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
from typing import Any, Dict, List, Tuple

_CK_ONCE_GV = {k: id(v) for k, v in globals().items()}

import numpy as np
import pandas as pd

GV_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(os.getcwd(), "arastirma_cikti", "goz_uyum")
if GV_DIR not in sys.path:
    sys.path.insert(0, GV_DIR)
import goz_uyum as GU  # noqa: E402
import tanim2 as TZ  # noqa: E402  (yalnız okunur: tz_pencere, _tz_muhur_oku, TZ_YOL)

gvlog = logging.getLogger("govde")
if not gvlog.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

KOK = GU.KOK
GV_YOL = {"is_tanimi": os.path.join(GV_DIR, "GOVDE_IS_TANIMI.md"), "anahtar": os.path.join(GV_DIR, "govde_anahtar.json"),
          "onkayit": os.path.join(GV_DIR, "GOVDE_ON_KAYIT.md"), "sonuc": os.path.join(GV_DIR, "GOVDE_SONUC.md"),
          "sonuc_json": os.path.join(GV_DIR, "govde_sonuc.json"),
          "ilk_anahtar": GU.GU_YOL["anahtar"], "ilk_cemal": os.path.join(GV_DIR, "cemal_isaret.json"), "iki_anahtar": TZ.TZ_YOL["anahtar"],
          "kod": os.path.abspath(__file__) if "__file__" in globals() else os.path.join(GV_DIR, "govde.py")}

# ---------------------------------------------------------------- TANIMLAR (etiketler okunmadan yazıldı; ADIM 1 commit'i)
# Pencere: W = kör sayfa penceresi (121 geçerli bar, t = son bar). P = son 40 bar [t-39..t] (dizin 0..39, t = 39).
# gövde altı b = min(O, C); gövde üstü u = max(O, C); alt fitil = b - L; aralık = H - L (> 0, ge_hazir geçerli bar).
# TR_j = max(H_j - L_j, |H_j - C_{j-1}|, |L_j - C_{j-1}|); ATR14 = ort TR [t-13..t]; ATRP14 = ATR14 / C_t.
# S_g = min b (P) (GÖVDE DİBİ); lo = min L (P) (FİTİL DİBİ); hi = max H (P).
# gövde dokunuşu: P içinde b_j <= S_g x (1 + 0,5 x ATRP14) olan bar j.
GV_OZ: Dict[str, Dict[str, str]] = {
    "G1_govde_dokunus_n": {
        "tanim": "GÖVDE DESTEĞİ: son 40 mumda gövde altı (min(O,C)) gövde dibi S_g'nin S_g x (1 + 0,5 x ATRP14) bandında kalan mum sayısı "
                 "(dip gövdeyle kaç kez savunuldu)",
        "yon": ">=", "nan": "NaN olmaz (S_g barının kendisi her zaman bantta; en az 1)"},
    "G2_dip_alt_fitil": {
        "tanim": "GÖVDE / FİTİL DİBİ: son 40 mumda dip bölgesi (L <= lo + 0,20 x (hi - lo)) barlarında ortalama alt fitil payı "
                 "(min(O,C) - L) / (H - L) (küçük = dipte gövde tepkisi, uzun alt fitil yok)",
        "yon": "<=", "nan": "NaN olmaz (lo barı her zaman dip bölgesinde)"},
    "G3_govdeli_tepki_payi": {
        "tanim": "GÖVDELİ TEPKİ: her gövde dokunuşundan (G1 bandı, bar j) sonraki 3 mum [j+1..min(j+3, t)] içinde C > O ve (C - O) >= 0,5 x (H - L) "
                 "olan (güçlü gövdeli yükselen) mum bulunan dokunuşların payı; payda = j < t olan dokunuşlar",
        "yon": ">=", "nan": "j < t olan dokunuş yoksa NaN (kuralda YOK)"},
    "G4_fitil_govde_arasi": {
        "tanim": "FİTİL DİBİ ile GÖVDE DİBİ ARASI: (S_g - lo) / ATR14 (küçük = dip gövdeyle kurulmuş, fitille aşağı sarkmamış)",
        "yon": "<=", "nan": "ATR14 <= 0 ise NaN (ge_hazir geçerli barda olmaz)"},
}
GV_KOL = list(GV_OZ)

GV_SECIM_KURALI = ("Her özellik için YÖN ÖNCEDEN SABİT (GV_OZ['yon']); tek eşik = ilk 40 sayfada (goz_uyum_anahtar.json + cemal_isaret.json; "
                   "hedef = Cemal VAR) dengeli doğruluğu en yüksek yapan (eşik adayları: ardışık benzersiz sonlu değerlerin orta noktaları; eşitlikte "
                   "ham doğruluk büyük > eşit eşik listesinin alt-orta elemanı; NaN = YOK). LOOCV kappa: her dışarıda bırakılan sayfa için eşik kalan "
                   "39 sayfadan aynı kuralla yeniden seçilir. GOVDE_1 = LOOCV kappa'sı en yüksek tek özellik (eşitlikte 40 sayfa kappa büyük > G sırası); "
                   "GOVDE_2 = GOVDE_1 VE eski Ş3 (dip delinmemiş: F2 >= -0,01). Eşik 40 sayfanın TAMAMIYLA seçilir ve SAYI olarak mühürlenir.")

GV_ESIK: Dict[str, Any] = {
    "pencere_bar": 40, "atr_n": 14, "bant_atr_k": 0.5, "dip_bolge": 0.20, "tepki_bar": 3, "tepki_govde_oran": 0.5,
    "s3": {"ozellik": "F2", "yon": ">=", "esik": -0.01, "tanim": "eski Ş3: F2 (hat eğimi) >= -0,01 (dip delinmemiş)"},
    "kural": {"amac": "dengeli doğruluk = (VAR duyarlılığı + YOK duyarlılığı) / 2", "nan": "NaN = YOK",
              "esitlik": "dengeli doğruluk büyük > ham doğruluk büyük > alt-orta eşik", "secim": GV_SECIM_KURALI},
    "kappa": {"B": 5000, "tohum": 20261124, "gecerli": 0.60, "gecerli_alt": 0.40, "kismen": 0.40, "karar_min": 30},
    "hukum": "ikinci sette GOVDE_1 (ve GOVDE_2) kappa >= 0,60 ve bootstrap %95 alt ucu >= 0,40 -> TANIM GEÇERLİ; kappa 0,40-0,60 (ya da kappa >= 0,60 "
             "ama alt uç < 0,40) KISMEN; < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. ADAY_1 / ADAY_2 / KONTROL (tanim2 mührü) karşılaştırma için yazılır",
    "not": "ikinci set GOVDE'ye göre tabakalanmadı; GOVDE ikinci sette ikincil adaydır; tanım Cemal'in 23 Kas sözünden, ikinci setin işaretleri "
           "gelmeden mühürlendi",
    "tanim_sha": hashlib.sha256(json.dumps(GV_OZ, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest(),
}


class GVHata(RuntimeError):
    """Durdurucu hata: veri / seçim / mühür tutmadı."""


def _sha_esik() -> str:
    return hashlib.sha256(json.dumps(GV_ESIK, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _f(x: Any, d: int = 3) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"{float(x):.{d}f}"
    except (TypeError, ValueError):
        return str(x)


# ================================================================ 1) ÖZELLİKLER (yalnız pencerenin son 40 barı)
def gv_ozellik_dizi(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray) -> Dict[str, float]:
    """Diziler kör sayfa penceresi (son eleman = t). Yalnız son 40 bar (+ ATR için önceki kapanış) kullanılır."""
    n = int(GV_ESIK["pencere_bar"]); an = int(GV_ESIK["atr_n"])
    if len(C) < max(n, an + 1):
        raise GVHata(f"pencere kısa: {len(C)} bar")
    O, H, L, C = (np.asarray(a, float) for a in (O, H, L, C))
    if not (np.all(H > L) and np.all(np.isfinite(np.c_[O, H, L, C]))):
        raise GVHata("geçersiz bar (H <= L ya da NaN) pencerede")
    tr = np.maximum(H[1:] - L[1:], np.maximum(np.abs(H[1:] - C[:-1]), np.abs(L[1:] - C[:-1])))
    atr = float(np.mean(tr[-an:])); atrp = atr / float(C[-1])
    o, h, l, c = O[-n:], H[-n:], L[-n:], C[-n:]
    b = np.minimum(o, c); rng_ = h - l
    Sg = float(b.min()); lo = float(l.min()); hi = float(h.max())
    out = {k: np.nan for k in GV_KOL}
    bant = Sg * (1.0 + float(GV_ESIK["bant_atr_k"]) * atrp)
    dok = np.flatnonzero(b <= bant + 1e-12)
    out["G1_govde_dokunus_n"] = float(len(dok))
    dip = l <= lo + float(GV_ESIK["dip_bolge"]) * (hi - lo) + 1e-12
    out["G2_dip_alt_fitil"] = float(np.mean(((b - l) / rng_)[dip]))
    guclu = (c > o) & ((c - o) >= float(GV_ESIK["tepki_govde_oran"]) * rng_)
    k = int(GV_ESIK["tepki_bar"]); uy = [j for j in dok if j < n - 1]
    if uy:
        out["G3_govdeli_tepki_payi"] = float(np.mean([bool(guclu[j + 1:min(j + k, n - 1) + 1].any()) for j in uy]))
    out["G4_fitil_govde_arasi"] = (Sg - lo) / atr if atr > 0 else np.nan
    return out


def gv_ozellik(W: pd.DataFrame) -> Dict[str, float]:
    O, H, L, C = (W[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    return gv_ozellik_dizi(O, H, L, C)


# ================================================================ 2) SABİT YÖNLÜ EŞİK SEÇİMİ + LOOCV
def gv_kural(x: np.ndarray, yon: str, e: float) -> np.ndarray:
    return TZ.tz_kural(x, yon, e)


def gv_esik_sec(x: np.ndarray, y: np.ndarray, yon: str) -> Dict[str, Any]:
    ea = TZ._esik_aday(np.asarray(x, float))
    if not len(ea):
        return {"yon": yon, "esik": float("nan"), "bal": 0.5}
    P = np.stack([gv_kural(x, yon, e) for e in ea])
    bal, acc = TZ._metrik(P, y)
    idx = TZ._en_iyi(bal, acc)
    k = int(idx[(len(idx) - 1) // 2])
    return {"yon": yon, "esik": float(ea[k]), "bal": float(bal[k])}


def gv_loocv(x: np.ndarray, y: np.ndarray, yon: str) -> np.ndarray:
    n = len(y); pr = np.zeros(n, bool)
    for k in range(n):
        m = np.arange(n) != k
        r = gv_esik_sec(x[m], y[m], yon)
        pr[k] = bool(gv_kural(x[k:k + 1], yon, r["esik"])[0]) if np.isfinite(r["esik"]) else False
    return pr


def gv_s3(F2: np.ndarray) -> np.ndarray:
    s = GV_ESIK["s3"]; return gv_kural(np.asarray(F2, float), s["yon"], float(s["esik"]))


# ================================================================ 3) SETLER
def _set_ozellik(S: pd.DataFrame) -> pd.DataFrame:
    Vc: Dict[str, Dict[str, pd.DataFrame]] = {}
    rows = []
    for r in S.itertuples(index=False):
        if r.pazar not in Vc:
            Vc[r.pazar] = GU.gu_veri(r.pazar)
        t = pd.Timestamp(r.sinyal_gunu)
        W = TZ.tz_pencere(r.pazar, r.sembol, t, Vc[r.pazar])        # K2: veri t'de kesik + mekanik denetim
        if W.index.max() > t:
            raise GVHata(f"{r.sembol} {t.date()}: pencere t sonrasını içeriyor")
        rows.append(gv_ozellik(W))
    return pd.concat([S.reset_index(drop=True), pd.DataFrame(rows)], axis=1)


def gv_ilk() -> Tuple[pd.DataFrame, np.ndarray]:
    J = json.load(open(GV_YOL["ilk_anahtar"], encoding="utf-8"))
    S = pd.DataFrame(J["sayfalar"]).sort_values("sayfa").reset_index(drop=True)
    C = json.load(open(GV_YOL["ilk_cemal"], encoding="utf-8")); cem = {int(k): GU.gu_norm(v) for k, v in C.items()}
    if sorted(cem) != list(S.sayfa):
        raise GVHata("cemal_isaret.json sayfaları ilk anahtarla uyuşmuyor")
    S["cemal"] = S.sayfa.map(cem)
    if (S.cemal == "?").any():
        raise GVHata("ilk sette '?' var")
    S = _set_ozellik(S[["sayfa", "pazar", "sembol", "sinyal_gunu", "F2", "S3", "cemal"]])
    if (gv_s3(S.F2.to_numpy(float)) != S.S3.to_numpy(bool)).any():
        raise GVHata("ilk sette F2 >= -0,01 ile anahtardaki S3 uyuşmuyor")
    return S, (S.cemal == "VAR").to_numpy(bool)


def gv_anahtar() -> Dict[str, Any]:
    t0 = time.time()
    S, y = gv_ilk()
    s3 = S.S3.to_numpy(bool)
    tab = []
    for c in GV_KOL:
        x = S[c].to_numpy(float); yon = GV_OZ[c]["yon"]
        r = gv_esik_sec(x, y, yon)
        tam = gv_kural(x, yon, r["esik"]) if np.isfinite(r["esik"]) else np.zeros(len(y), bool)
        lo = gv_loocv(x, y, yon)
        g = {}
        for ad, m in (("VAR", y), ("YOK", ~y)):
            v = x[m]; f = v[np.isfinite(v)]
            g[ad] = {"n": int(len(v)), "nan": int((~np.isfinite(v)).sum()),
                     "medyan": float(np.median(f)) if len(f) else np.nan,
                     "q25": float(np.percentile(f, 25)) if len(f) else np.nan, "q75": float(np.percentile(f, 75)) if len(f) else np.nan}
        tab.append({"ozellik": c, "yon": yon, "esik": r["esik"], "bal": r["bal"], "kappa": GU.gu_kappa(y, tam),
                    "loocv_kappa": GU.gu_kappa(y, lo), "loocv_uyum": float(np.mean(lo == y)), "tam_VAR": int(tam.sum()),
                    "s3_ile_kappa": GU.gu_kappa(y, tam & s3), "dagilim": g})
    T = pd.DataFrame(tab); T["_s"] = range(len(T))
    T["_k"] = T.loocv_kappa.fillna(-9); T["_t"] = T.kappa.fillna(-9)
    Ts = T.sort_values(["_k", "_t", "_s"], ascending=[False, False, True], kind="mergesort").reset_index(drop=True)
    a = Ts.iloc[0]
    G1 = {"ozellik": a.ozellik, "yon": a.yon, "esik": float(a.esik), "kappa_40": float(a.kappa), "loocv_kappa_40": float(a.loocv_kappa),
          "tanim": GV_OZ[a.ozellik]["tanim"]}
    x1 = S[a.ozellik].to_numpy(float)
    g1_ilk = gv_kural(x1, a.yon, float(a.esik))
    G2 = {"tanim": f"GOVDE_1 VE Ş3 ({a.ozellik} {a.yon} {float(a.esik)!r} VE F2 >= -0,01)", "kappa_40": GU.gu_kappa(y, g1_ilk & s3),
          "loocv_kappa_40": GU.gu_kappa(y, gv_loocv(x1, y, a.yon) & s3)}
    KESIF = {"etiket": "KEŞİF (ilk 40 sayfa; küçük örneklem; 4 özellik; seçilen kural ikinci sette sınanır)", "n": int(len(y)),
             "cemal_VAR": int(y.sum()), "cemal_YOK": int((~y).sum()), "S3_kappa_40": GU.gu_kappa(y, s3),
             "tablo": Ts.drop(columns=["_k", "_t", "_s"]).to_dict("records"),
             "ilk_degerler": S[["sayfa", "pazar", "cemal", "S3"] + GV_KOL].to_dict("records")}
    # ikinci set (Cemal'in işareti YOK; yalnız pazar / sembol / sinyal günü / F2 / S3 / tanim2 yanıtları okunur)
    J2 = json.load(open(GV_YOL["iki_anahtar"], encoding="utf-8"))
    S2 = pd.DataFrame(J2["sayfalar"]).sort_values("sayfa").reset_index(drop=True)
    S2 = _set_ozellik(S2[["sayfa", "pazar", "sembol", "sinyal_gunu", "F2", "S3", "yanit"]])
    s3b = gv_s3(S2.F2.to_numpy(float))
    if (s3b != S2.S3.to_numpy(bool)).any():
        raise GVHata("ikinci sette F2 >= -0,01 ile anahtardaki S3 uyuşmuyor")
    g1b = gv_kural(S2[a.ozellik].to_numpy(float), a.yon, float(a.esik)); g2b = g1b & s3b
    a1 = (S2.yanit.map(lambda z: z["ADAY_1"]) == "VAR").to_numpy(bool)
    sayfalar = []
    for i, r in S2.iterrows():
        sayfalar.append({"sayfa": int(r.sayfa), "pazar": r.pazar, "sembol": r.sembol, "sinyal_gunu": r.sinyal_gunu, "F2": float(r.F2),
                         "S3": bool(r.S3), **{c: (None if not np.isfinite(r[c]) else float(r[c])) for c in GV_KOL},
                         "yanit": {"GOVDE_1": "VAR" if g1b[i] else "YOK", "GOVDE_2": "VAR" if g2b[i] else "YOK"},
                         "tanim2_yanit": dict(r.yanit)})
    ozet = {"GOVDE_1_VAR": int(g1b.sum()), "GOVDE_2_VAR": int(g2b.sum()), "ADAY_1_VAR": int(a1.sum()),
            "GOVDE_1_ADAY_1_ayrisan": int((g1b != a1).sum()), "ayrisan_sayfalar": [int(s) for s in S2.sayfa[g1b != a1]],
            "GOVDE_2_ADAY_1_ayrisan": int((g2b != a1).sum())}
    J = {"surum": "govde v1", "uretim_utc": GU._simdi(),
         "uyari": "GETİRİ YOK; ikinci setin Cemal işaretleri bu dosya yazılırken YOK (Cemal işaretliyor)",
         "esik": GV_ESIK, "esik_sha": _sha_esik(), "tanim_sha": GV_ESIK["tanim_sha"], "tanimlar": GV_OZ, "secim_kurali": GV_SECIM_KURALI,
         "tanim2_anahtar_sha": GU._sha(GV_YOL["iki_anahtar"]),
         "kurallar": {"GOVDE_1": G1, "GOVDE_2": G2}, "kesif": KESIF, "ikinci_ozet": ozet, "sayfalar": sayfalar,
         "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(GV_YOL["anahtar"], J)
    gvlog.info("GOVDE_1 %s %s %.4g (kappa %.3f, LOOCV %.3f); ikinci set VAR %d, ADAY_1 ile ayrışan %d", G1["ozellik"], G1["yon"], G1["esik"],
               G1["kappa_40"], G1["loocv_kappa_40"], ozet["GOVDE_1_VAR"], ozet["GOVDE_1_ADAY_1_ayrisan"])
    return J


# ================================================================ 4) MÜHÜR
GV_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralların uyumu, kappa)"),
    "K2": ("EVET", "G1-G4 yalnız kör sayfa penceresinin son 40 barından: tanim2.tz_pencere = goz_uyum._gu_pencere (veri t'de KESİK, 121 bar) + "
                   "mekanik denetim (W.index.max() <= t, W.index[-1] == t); govde.py test prefix değişmezliği (t sonrası değişince G1-G4 aynı); "
                   "getiri / sinyal sonrası fiyat okunmaz; ikinci setin Cemal işareti mühür anında yok"),
    "K3": ("EVET", "GE.ge_hazir (H>L, V>0, O/H/L/C>0) geçerli bar (goz_uyum ile aynı); gv_ozellik_dizi H <= L / NaN görürse durur"),
    "K4": ("EVET", "sayfalar ilk set (goz_uyum_anahtar) ve ikinci set (tanim2_anahtar) ile aynı: aynı hissede en çok 1 sayfa, 60 bar tekil; n = 40 + 40"),
    "K5": ("UYGULANMAZ", "giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik"),
    "K6": ("EVET", "tek kip V_*.pkl (goz_uyum ile aynı); G1 bar sayısı, G2 / G3 pay, G4 ATR birimi: birimsiz"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok"),
    "K8": ("EVET", "keşif 40 sayfa küçük örneklem: 'KEŞİF' etiketli; 4 özellik (çoklu karşılaştırma küçük), yön önceden sabit; seçilen kural yalnız "
                   "ikinci bağımsız 40 sayfada sınanır; karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); ikinci set GOVDE'ye göre tabakalanmadı"),
    "K9": ("EVET", "tanımlar (GV_OZ) + sabit yönler + seçim kuralı etiket hesabından önce commit (ADIM 1); eşikler SAYI olarak bu dosyada; "
                   "govde_anahtar + govde.py + GV_ESIK sha'ları burada; bu dosya ikinci setin Cemal işaretleri gelmeden commit; hüküm eşikleri sabit"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırma yok; yalnız OHLCV"),
    "K11": ("EVET", "govde.py anahtar aynı komutla deterministik yeniden üretilir (rastgelelik yok); olc tabloyu anahtardan ve tanim2_anahtar'dan yeniden kurar"),
    "K12": ("EVET", "iddia yok; yalnız 'uyum' ve 'kappa' sayısı; keşif sayıları 'bulgu' denmez; hüküm sözü yalnız ön kayıttaki eşikle"),
    "K13": ("EVET", "çakışma kapısı _CK_ONCE_GV + test; yasak dosyalar (defter, mevcut .py, tanim2 / goz_uyum dosyaları ve mühürleri) değişmedi "
                    "(git diff boş); e-posta / anahtar yok; git add -A yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


def gv_muhur() -> str:
    for y in (GV_YOL["anahtar"], GV_YOL["is_tanimi"]):
        if not os.path.exists(y):
            raise GVHata(f"mühür için dosya yok: {y}")
    J = json.load(open(GV_YOL["anahtar"], encoding="utf-8"))
    if J["esik_sha"] != _sha_esik():
        raise GVHata("GV_ESIK anahtardan sonra değişmiş")
    if J["tanim2_anahtar_sha"] != GU._sha(GV_YOL["iki_anahtar"]):
        raise GVHata("tanim2_anahtar.json anahtardan sonra değişmiş")
    ad = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
          "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
          "K13": "süreç", "K14": "boyut (gerçek para)"}
    tab = "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |\n|---|---|---|---|\n"
    for k, (yy, kn) in GV_KONTROL.items():
        tab += f"| {k} | {ad[k]} | {yy} | {kn} |\n"
    G1, G2 = J["kurallar"]["GOVDE_1"], J["kurallar"]["GOVDE_2"]; K = J["kesif"]; oz = J["ikinci_ozet"]
    tanim = "\n".join(f"- **{c}** (VAR yönü `{v['yon']}`): {v['tanim']}. NaN: {v['nan']}." for c, v in GV_OZ.items())
    kt = ["| özellik | yön | eşik (40 sayfa) | kappa 40 | LOOCV kappa | VAR medyan [q25, q75] | YOK medyan [q25, q75] | 40'ta VAR | Ş3 ile kappa |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in K["tablo"]:
        d = r["dagilim"]
        kt.append(f"| {r['ozellik']} | {r['yon']} | {r['esik']!r} | {_f(r['kappa'])} | {_f(r['loocv_kappa'])} | {_f(d['VAR']['medyan'])} "
                  f"[{_f(d['VAR']['q25'])}, {_f(d['VAR']['q75'])}] | {_f(d['YOK']['medyan'])} [{_f(d['YOK']['q25'])}, {_f(d['YOK']['q75'])}] | "
                  f"{r['tam_VAR']} | {_f(r['s3_ile_kappa'])} |")
    m = f"""# GÖVDE TEPKİSİ — ÖN KAYIT (ikinci setin Cemal işaretleri gelmeden ÖNCE mühürlenir)

Üretim: {GU._simdi()} (UTC). Soru: Cemal'in 23.11.2026 sözü ("dip delinmiş mi tamam, bu kolay, ancak bu yeterli değil; çünkü mumların fitili değil GÖVDE ile tepki alması gerekir bu diplerde") ölçülebilir bir 'gövde tepkisi' kuralına çevrilince, ikinci bağımsız kör sette (TANIM2_KOR.pdf) Cemal'in VAR / YOK işaretleriyle örtüşüyor mu? GETİRİ ÖLÇÜLMEZ.

**NOT:** ikinci set GOVDE'ye göre tabakalanmadı (ADAY_1 x Ş3 tabakalı); GOVDE ikinci sette ikincil adaydır; tanım Cemal'in 23 Kas sözünden, ikinci setin işaretleri gelmeden mühürlendi.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/govde_anahtar.json` sha256: `{GU._sha(GV_YOL['anahtar'])}`
- kod: `arastirma_cikti/goz_uyum/govde.py` sha256: `{GU._sha(GV_YOL['kod'])}`
- eşik sözlüğü (GV_ESIK) sha256: `{_sha_esik()}`
- tanım sözlüğü (GV_OZ) sha256: `{GV_ESIK['tanim_sha']}`
- iş tanımı: `arastirma_cikti/goz_uyum/GOVDE_IS_TANIMI.md` sha256: `{GU._sha(GV_YOL['is_tanimi'])}`
- ikinci set anahtarı (değişmedi; tanim2 mührü): `tanim2_anahtar.json` sha256: `{GU._sha(GV_YOL['iki_anahtar'])}`
- bağımlı kod: tanim2.py `{GU._sha(TZ.TZ_YOL['kod'])[:16]}`, goz_uyum.py `{GU._sha(GU.GU_YOL['kod'])[:16]}`, GOZ_ETIKET.py `{GU._sha(os.path.join(KOK, 'GOZ_ETIKET.py'))[:16]}`

## 2. Tanımlar (ADIM 1'de etiket hesabından önce commit)
Pencere: kör sayfa penceresi (goz_uyum._gu_pencere, veri sinyal günü t'de kesik) içindeki son 40 mum [t-39..t]. Gövde altı = min(Open, Close). S_g = son 40 mumda gövde altlarının en düşüğü (GÖVDE DİBİ); lo = son 40 mumda en düşük Low (FİTİL DİBİ); hi = en yüksek High. ATR14 = son 14 barın gerçek aralık ortalaması; ATRP14 = ATR14 / C_t. Gövde dokunuşu = gövde altı <= S_g x (1 + 0,5 x ATRP14).
{tanim}

## 3. Seçim kuralı (iş tanımından; etiketlerden önce yazıldı)
{GV_SECIM_KURALI}

## 4. İlk set (KEŞİF, 40 sayfa; Cemal VAR {K['cemal_VAR']} / YOK {K['cemal_YOK']}; Ş3 kappa {_f(K['S3_kappa_40'])})
{chr(10).join(kt)}

## 5. Mühürlü kurallar (SAYI; 40 sayfanın tamamıyla seçildi; NaN = YOK)
- **GOVDE_1**: VAR ⇔ {G1['ozellik']} {G1['yon']} {G1['esik']!r}. Tanım: {G1['tanim']}. 40 sayfada kappa {_f(G1['kappa_40'])}, LOOCV kappa {_f(G1['loocv_kappa_40'])} (keşif).
- **GOVDE_2**: VAR ⇔ {G2['tanim']}. 40 sayfada kappa {_f(G2['kappa_40'])}, LOOCV kappa {_f(G2['loocv_kappa_40'])} (keşif).
- Karşılaştırma (tanim2 mührü, değişmez): ADAY_1, ADAY_2, KONTROL (Ş3) — tanim2_anahtar.json yanıtları.

## 6. İkinci set yanıtları (govde_anahtar.json 'sayfalar'; Cemal'in işareti YOK iken yazıldı)
GOVDE_1 VAR {oz['GOVDE_1_VAR']} / 40; GOVDE_2 VAR {oz['GOVDE_2_VAR']} / 40; ADAY_1 VAR {oz['ADAY_1_VAR']} / 40; GOVDE_1 ile ADAY_1 {oz['GOVDE_1_ADAY_1_ayrisan']} sayfada ayrışıyor (sayfalar {oz['ayrisan_sayfalar']}); GOVDE_2 ile ADAY_1 {oz['GOVDE_2_ADAY_1_ayrisan']} sayfada ayrışıyor.

## 7. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in ikinci setteki VAR / YOK işaretleri ile GOVDE_1, GOVDE_2 (ve karşılaştırma: ADAY_1, ADAY_2, KONTROL) arasında uyum ve Cohen kappa; '?' karar dışı, sayısı ayrıca yazılır; kappa bootstrap %95 aralığı (B {GV_ESIK['kappa']['B']}, tohum {GV_ESIK['kappa']['tohum']}, sayfa yeniden örneklemesi).
- HÜKÜM: {GV_ESIK['hukum']}.
- Eşik ve kural sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 8. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
{tab}
## 9. Git kaydı (bu dosyanın yazıldığı an)
- govde.py: {GU._gu_git('arastirma_cikti/goz_uyum/govde.py')}
"""
    GU._yaz(GV_YOL["onkayit"], m)
    import IZ_KARNE as IK
    r = IK.ik_kontrol_kapisi(GV_YOL["onkayit"])
    gvlog.info("kontrol kapısı: %s", "GEÇTİ" if r["gecti"] else r)
    return GV_YOL["onkayit"]


# ================================================================ 5) ÖLÇÜM (olc)
def _gv_muhur_oku() -> Dict[str, str]:
    if not os.path.exists(GV_YOL["onkayit"]):
        raise GVHata("ön kayıt yok")
    t = open(GV_YOL["onkayit"], encoding="utf-8").read(); out = {}
    for ad, anahtar in (("anahtar", "govde_anahtar.json"), ("kod", "govde.py")):
        m = re.search(re.escape(anahtar) + r"` sha256: `([0-9a-f]{64})`", t)
        if not m:
            raise GVHata(f"ön kayıtta {ad} sha'sı yok")
        out[ad] = m.group(1)
    m = re.search(r"eşik sözlüğü \(GV_ESIK\) sha256: `([0-9a-f]{64})`", t)
    if not m:
        raise GVHata("ön kayıtta GV_ESIK sha'sı yok")
    out["esik"] = m.group(1)
    return out


def gv_hukum(k: float, alt: float, n: int) -> str:
    E = GV_ESIK["kappa"]
    if n < int(E["karar_min"]) or not np.isfinite(k):
        return "ÖLÇÜLEMEDİ (karar sayısı < 30 ya da kappa tanımsız)"
    if k >= E["gecerli"] and np.isfinite(alt) and alt >= E["gecerli_alt"]:
        return "TANIM GEÇERLİ"
    return "KISMEN" if k >= E["kismen"] else "GEÇERSİZ"


def gv_olc(cemal_yol: str) -> Dict[str, Any]:
    M = _gv_muhur_oku()
    if GU._sha(GV_YOL["anahtar"]) != M["anahtar"]:
        raise GVHata("MÜHÜR BOZUK: govde_anahtar.json sha'sı ön kayıttakiyle aynı değil -> DURDU")
    if GU._sha(GV_YOL["kod"]) != M["kod"]:
        raise GVHata("MÜHÜR BOZUK: govde.py sha'sı ön kayıttakiyle aynı değil -> DURDU")
    if _sha_esik() != M["esik"]:
        raise GVHata("MÜHÜR BOZUK: GV_ESIK sha'sı ön kayıttakiyle aynı değil -> DURDU")
    M2 = TZ._tz_muhur_oku()                                                        # tanim2 mührü de bozulmamalı
    if GU._sha(TZ.TZ_YOL["anahtar"]) != M2["anahtar"]:
        raise GVHata("MÜHÜR BOZUK: tanim2_anahtar.json sha'sı TANIM2_ON_KAYIT ile aynı değil -> DURDU")
    J = json.load(open(GV_YOL["anahtar"], encoding="utf-8")); S = pd.DataFrame(J["sayfalar"])
    if J["tanim2_anahtar_sha"] != GU._sha(TZ.TZ_YOL["anahtar"]):
        raise GVHata("MÜHÜR BOZUK: tanim2_anahtar.json govde anahtarından sonra değişmiş -> DURDU")
    C = json.load(open(cemal_yol, encoding="utf-8")); cem = {int(k): GU.gu_norm(v) for k, v in C.items()}
    eksik = sorted(set(S.sayfa) - set(cem)); fazla = sorted(set(cem) - set(S.sayfa))
    if eksik or fazla:
        raise GVHata(f"yanıt sayfaları anahtarla uyuşmuyor: eksik {eksik}, fazla {fazla}")
    S["cemal"] = S.sayfa.map(cem)
    soru = int((S.cemal == "?").sum()); K = S[S.cemal != "?"].copy(); n = len(K)
    E = GV_ESIK["kappa"]; cb = (K.cemal == "VAR").to_numpy(bool)
    sonuc: Dict[str, Any] = {"n_sayfa": int(len(S)), "soru_isareti": soru, "karar_n": n, "cemal_VAR": int(cb.sum()), "modeller": {}}
    t2k = json.load(open(TZ.TZ_YOL["anahtar"], encoding="utf-8"))["kurallar"]
    modeller: List[Tuple[str, np.ndarray, bool]] = [
        ("GOVDE_1", (K.yanit.map(lambda z: z["GOVDE_1"]) == "VAR").to_numpy(bool), True),
        ("GOVDE_2", (K.yanit.map(lambda z: z["GOVDE_2"]) == "VAR").to_numpy(bool), True),
        ("ADAY_1", (K.tanim2_yanit.map(lambda z: z["ADAY_1"]) == "VAR").to_numpy(bool), False)]
    if t2k.get("ADAY_2"):
        modeller.append(("ADAY_2", (K.tanim2_yanit.map(lambda z: z["ADAY_2"]) == "VAR").to_numpy(bool), False))
    modeller.append(("KONTROL", (K.tanim2_yanit.map(lambda z: z["KONTROL"]) == "VAR").to_numpy(bool), False))
    for ad, mod, huk in modeller:
        k = GU.gu_kappa(cb, mod)
        ar = GU.gu_boot(cb, mod, int(E["B"]), int(E["tohum"])) if n else {"alt": np.nan, "ust": np.nan, "gecersiz": 0}
        tp, tn = int((cb & mod).sum()), int((~cb & ~mod).sum()); fp, fn = int((~cb & mod).sum()), int((cb & ~mod).sum())
        sonuc["modeller"][ad] = {"uyum": float(np.mean(cb == mod)) if n else np.nan, "kappa": k, "aralik": ar, "kod_VAR": int(mod.sum()),
                                 "hukum": gv_hukum(k, ar["alt"], n) if huk else "karşılaştırma (tanim2 mührü; hüküm TANIM2_SONUC'ta)",
                                 "tablo": {"Cemal VAR + kod VAR": tp, "Cemal YOK + kod YOK": tn, "Cemal YOK + kod VAR": fp, "Cemal VAR + kod YOK": fn},
                                 "uyusmayan": [int(s) for s in K.sayfa[cb != mod]]}
    Kr = J["kurallar"]
    L = ["# GÖVDE TEPKİSİ — İKİNCİ KÖR SET — SONUÇ", "",
         f"Üretim: {GU._simdi()} (UTC). Mühür denetimi: govde_anahtar, govde.py, GV_ESIK ve tanim2_anahtar sha'ları ön kayıtlarla aynı.", "",
         f"Sayfa {len(S)}; karar (VAR / YOK) {n} (Cemal VAR {int(cb.sum())}); '?' (karar dışı) {soru}.", "",
         f"- GOVDE_1: VAR ⇔ {Kr['GOVDE_1']['ozellik']} {Kr['GOVDE_1']['yon']} {Kr['GOVDE_1']['esik']!r}",
         f"- GOVDE_2: VAR ⇔ {Kr['GOVDE_2']['tanim']}", "- Karşılaştırma: ADAY_1 / ADAY_2 / KONTROL (tanim2 mührü)", "",
         "NOT: ikinci set GOVDE'ye göre tabakalanmadı; GOVDE ikinci sette ikincil adaydır.", "",
         "| model | kod VAR | uyum | kappa | %95 aralık (B 5000) | hüküm |", "|---|---|---|---|---|---|"]
    for ad, r in sonuc["modeller"].items():
        L.append(f"| {ad} | {r['kod_VAR']} | {_f(r['uyum'])} | {_f(r['kappa'])} | [{_f(r['aralik']['alt'])}, {_f(r['aralik']['ust'])}] | {r['hukum']} |")
    L += ["", f"HÜKÜM kuralı (ön kayıt): {GV_ESIK['hukum']}.", ""]
    for ad, r in sonuc["modeller"].items():
        L += [f"### {ad}: 2x2", "", "| | sayı |", "|---|---|"] + [f"| {k} | {v} |" for k, v in r["tablo"].items()]
        L += ["", f"Uyuşmayan sayfalar ({len(r['uyusmayan'])}): {r['uyusmayan']}", ""]
    GU._yaz(GV_YOL["sonuc"], "\n".join(L) + "\n")
    GU._jyaz(GV_YOL["sonuc_json"], sonuc)
    return sonuc


# ================================================================ 6) TEST
def gv_cakisma_kontrol() -> None:
    ez = [k for k, v in _CK_ONCE_GV.items() if k in globals() and id(globals()[k]) != v and not k.startswith("_")]
    if ez:
        raise GVHata(f"çakışma kapısı: bellekteki mevcut ad(lar) ezildi: {ez[:5]}")


def gv_test() -> Dict[str, Any]:
    gv_cakisma_kontrol()
    rng = np.random.default_rng(5); n = 200
    C = 100 + np.cumsum(rng.normal(0, 1, n)); O = C + rng.normal(0, .3, n)
    H = np.maximum(O, C) + abs(rng.normal(0, .5, n)) + .1; L = np.minimum(O, C) - abs(rng.normal(0, .5, n)) - .1
    i = 150; s = slice(i - 120, i + 1)
    x1 = gv_ozellik_dizi(O[s], H[s], L[s], C[s])
    O2, H2, L2, C2 = O.copy(), H.copy(), L.copy(), C.copy()
    O2[i + 1:] = 1; H2[i + 1:] = 2; L2[i + 1:] = 0.5; C2[i + 1:] = 1.5
    x2 = gv_ozellik_dizi(O2[s], H2[s], L2[s], C2[s])
    assert all((np.isnan(x1[k]) and np.isnan(x2[k])) or x1[k] == x2[k] for k in GV_KOL), "G özelliği t sonrasına bağlı"
    # tam dizi üzerinden pencere: t sonrası veri değişse de _gu_pencere mantığı (veri t'de kesik) aynı değeri verir
    idx = pd.bdate_range("2020-01-01", periods=n)
    D1 = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C}, index=idx); D2 = pd.DataFrame({"Open": O2, "High": H2, "Low": L2, "Close": C2}, index=idx)
    t = idx[i]
    y1 = gv_ozellik(D1[D1.index <= t].iloc[-121:]); y2 = gv_ozellik(D2[D2.index <= t].iloc[-121:])
    assert all((np.isnan(y1[k]) and np.isnan(y2[k])) or y1[k] == y2[k] for k in GV_KOL), "prefix (DataFrame) değişmezliği bozuk"
    assert x1["G1_govde_dokunus_n"] >= 1 and 0 <= x1["G2_dip_alt_fitil"] <= 1 and x1["G4_fitil_govde_arasi"] >= 0
    # elle: gövdeyle savunulan dip (alt fitil yok) -> G2 = 0, G4 = 0
    m = 130; Oa = np.full(m, 10.0); Ca = np.full(m, 10.2); Ha = np.full(m, 10.3); La = np.full(m, 10.0)
    z = gv_ozellik_dizi(Oa, Ha, La, Ca)
    assert z["G2_dip_alt_fitil"] == 0 and z["G4_fitil_govde_arasi"] == 0 and z["G1_govde_dokunus_n"] == 40, z
    assert z["G3_govdeli_tepki_payi"] == 1.0, z          # her mum C > O ve gövde 0,2 / aralık 0,3 >= %50
    # sabit yönlü eşik seçimi
    y = np.array([0, 0, 0, 1, 1, 1], bool); x = np.array([1., 2, 3, 4, 5, 6])
    r = gv_esik_sec(x, y, ">="); assert r["esik"] == 3.5 and abs(r["bal"] - 1) < 1e-12, r
    r = gv_esik_sec(-x, y, "<="); assert r["esik"] == -3.5 and abs(r["bal"] - 1) < 1e-12, r
    r = gv_esik_sec(x, y, "<="); assert r["bal"] <= 0.5 + 1e-12, r   # yön ters çevrilmez
    assert (gv_loocv(np.array([1., 2, 3, 10, 11, 12]), y, ">=") == y).all()
    assert gv_s3(np.array([-0.02, -0.01, 0.0])).tolist() == [False, True, True]
    return {"tamam": True}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", choices=["anahtar", "muhur", "olc", "test"])
    ap.add_argument("--cemal", default=None)
    a = ap.parse_args()
    if a.komut == "anahtar":
        J = gv_anahtar(); print(json.dumps({"kurallar": J["kurallar"], "ikinci_ozet": J["ikinci_ozet"]}, ensure_ascii=False, default=str))
    elif a.komut == "muhur":
        print(gv_muhur())
    elif a.komut == "olc":
        if not a.cemal:
            raise SystemExit("olc için --cemal J.json gerekli")
        r = gv_olc(a.cemal); print(json.dumps({k: r[k] for k in ("n_sayfa", "soru_isareti", "karar_n")}, ensure_ascii=False))
    else:
        print(gv_test())
