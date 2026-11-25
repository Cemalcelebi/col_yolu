"""MACD_UYUM_KASA — K47 'derin toplam uyumsuzluk' (T) KASA KÖR SINAMASI, 2023-24 (25 Kasım 2026; iş tanımı: ana model mesajı).

Ön kayıt (ana bölüm DEĞİŞMEZ): arastirma_cikti/macd_uyum/KASA_T_ON_KAYIT.md (git 2aedf2e). Cemal (25 Kas 08:47): "Aç".
T = U1 olayı VE PFc <= -0,10 VE MRc >= 0,30.
  U1     : MACD_UYUM.mu_pazar / mu_hisse aynen (Ç217).
  Zincir : UYUM_Z_ON_KAYIT (f5edc17): aynı hissede U1 olayları sırayla; önceki U1 olayı en çok 60 geçerli bar önce (i farkı) VE Low(L2) daha
           düşükse sıra + 1, değilse 1. Yalnız geçmiş olaylar.
  PFc/MRc: UYUM_T_ON_KAYIT (c4cc7d7): PFc = Low(L2, olay) / Low(L1, zincirin ilk olayı) - 1;
           MRc = (MACD(L2, olay) - MACD(L1, ilk olay)) / |MACD(L1, ilk olay)|; MACD(L2) = F66m x close_L2 (olayın kendi penceresi),
           MACD(L1, ilk) = (F66m - F66) x close_L2 (ilk olayın penceresi). Sıra 1'de PFc = F65, MRc = MR.
  Eş     : CETVEL2 v2.2 konum eşi + K20 temiz eş (MACD_UYUM_ES.es_panel_bayrak / es_kirli_cift / es_es aynen).
  h5/st5 : MACD_UYUM.mu_olc_h5 (1. tur 15 bar cetveli) aynen.
ÖLÇÜ  Ö1 ÜST10 / ALT10 (temiz eş sırası >= 0,90 / <= 0,10), ay kümeli boot (MU.mu_sira_boot, B 2000); Ö2 R15 temiz eş FARK
      (C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum, plasebo hariç); Ö3 bilgi (piyasa yukarı / aşağı, +%5 / stop, Tz, yıl, BIST).
KARAR ön kayıttaki kural harfiyen (mk_karar).

Komut:  python MACD_UYUM_KASA.py dogrula --veri /tmp/kasa/acik       açık veride (<= 2022-12-31) Ç217 / Ç222 / Ç223 değerlerini yeniden üretir
        python MACD_UYUM_KASA.py olc --veri <kasa açık kısmı>         kasa verisinde (<= 2024-12-31) ölçer -> kasa_t_satir / sonuc / rapor
        python MACD_UYUM_KASA.py sha                                  kod / eşik sha'ları
Colab:  exec(open('MACD_UYUM_KASA.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
MACD_UYUM / MACD_UYUM_ES / CETVEL2 / KASA / IZ_KARNE DEĞİŞTİRİLMEZ; içe alınır. Evren bugün işlem gören hisseler (sonuç yukarı yanlı).
Alım-satım önerisi değildir; tarayıcı yalnız aday bulur.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_MK = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_MK = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_MK not in sys.path:
    sys.path.insert(0, KOK_MK)

import CETVEL2 as C2  # noqa: E402
import KASA as KS  # noqa: E402
import MACD_UYUM as MU  # noqa: E402
import MACD_UYUM_ES as ES  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

mklog = logging.getLogger("col.macd_uyum_kasa")
if not mklog.handlers:
    _mk_h = logging.StreamHandler(sys.stderr)
    _mk_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s macd_uyum_kasa: %(message)s", "%H:%M:%S"))
    mklog.addHandler(_mk_h)
    mklog.setLevel(logging.INFO)
    mklog.propagate = False

MK_SURUM = "MACD_UYUM_KASA v1.0 (2026-11-25): K47 T (derin toplam uyumsuzluk) KASA 2023-24 kör sınaması"
MK_YOL = {"cikti": os.path.join(KOK_MK, "arastirma_cikti", "macd_uyum"), "kod": os.path.abspath(__file__) if "__file__" in globals() else ""}
MK_DOSYA = {"onkayit": "KASA_T_ON_KAYIT.md", "satir": "kasa_t_satir.csv.gz", "sonuc": "kasa_t_sonuc.json", "rapor": "KASA_T_RAPOR.md",
            "dogrulama": "kasa_t_dogrulama.json",
            "olay": "uyum_olay.csv.gz", "zincir": "uyum_zincir.csv.gz", "toplam": "uyum_toplam.csv.gz", "es": "es_satir.csv.gz",
            "c217_satir": "uyum_satir.csv.gz", "t_sonuc": "uyum_t_sonuc.json", "ust10": "uyum_ust10_bilgi.json"}
MK_PAZAR = ["ABD", "AVR", "BIST"]

# ---------------------------------------------------------------- EŞİKLER (sha ön kayıt ekinde; sonuçtan sonra DEĞİŞMEZ)
MK_ESIK: Dict[str, Any] = {
    "hipotez": "MACD_UYUM_T",
    "T": {"PFc_ust": -0.10, "MRc_alt": 0.30},                 # T = U1 ∧ PFc <= -0,10 ∧ MRc >= 0,30
    "zincir": {"ara_bar": 60},                                 # önceki U1 olayı en çok 60 geçerli bar önce ve Low(L2) daha düşük
    "ust10": 0.90, "alt10": 0.10, "ust20": 0.80,               # temiz eş sırası eşikleri (ÜST20 yalnız bilgi)
    "kasa": {"kesik": "2024-12-31", "giris_ilk": "2023-01-01", "giris_son": "2024-12-31",
             "donem": {"k2324": ["2023-01-01", "2024-12-31"]},
             "yil": {"y2023": ["2023-01-01", "2023-12-31"], "y2024": ["2024-01-01", "2024-12-31"]}},
    "acik": {"kesik": "2022-12-31"},
    "karar": {"pazar": ["ABD", "AVR"], "n_min": 100, "ust10_taban": 0.10},
    # tohumlar (kasa açılmadan önce sabit): hücre tohumu = taban + 10 x pazar sırası (+ 1 yıl / piyasa alt kırılımı)
    "tohum": {"T": 6100, "Tz": 6200, "ust10": 6300, "alt10": 6400, "birlesik": 6500, "yil": 6600, "piyasa": 6700},
    "prefix": {"n": 30, "tohum": 4747},
    # açık veri doğrulama tohumları: toplam_olc.py (Ç223) ile aynı: T 900 + 10 x pazar + dönem, Tz aynı
    "dogrulama": {"tohum_T": 900, "dt_rtol": 1e-9, "olay_rtol": 1e-10, "zincir_atol": 1e-9,
                  "beklenen_T": {"ABD|d2022": [357, 0.01359], "AVR|d1619": [64, 0.01601]},
                  "beklenen_ust10": {"n": 669, "ust10": 0.16591928251121077, "alt10": 0.14499252615844543}},
}


class MKHata(RuntimeError):
    """Durdurucu hata: doğrulama, kapı, kasa kesiği, yeniden üretim, prefix."""


# ================================================================ 0) ORTAK
def _mk_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def mk_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or MK_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _mk_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _mk_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or MK_YOL["cikti"], MK_DOSYA[ad])


def _mk_json(o: Any) -> Any:
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, _dt.date)):
        return str(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def _mk_nan(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _mk_nan(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_mk_nan(v) for v in o]
    if isinstance(o, (float, np.floating)):
        return None if not np.isfinite(o) else float(o)
    return o


def _mk_jyaz(yol: str, J: Any) -> None:
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(_mk_nan(J), f, ensure_ascii=False, indent=1, default=_mk_json)


def mk_sha_simdi() -> Dict[str, str]:
    out = {"MK_ESIK_SHA": mk_esik_sha(), "MU_ESIK_SHA": MU.mu_esik_sha(), "ES_ESIK_SHA": ES.es_esik_sha(), "C2_ESIK22_SHA": C2.c2_esik22_sha(),
           "YH_ESIK8_SHA": YH.yh_esik8_sha()}
    for f in ("MACD_UYUM_KASA.py", "MACD_UYUM.py", "MACD_UYUM_ES.py", "CETVEL2.py", "KASA.py", "YAPI_HEDEF.py", "ORTAK_CETVEL.py",
              "POZITIF_KONTROL.py", "DUSUS_SONRASI.py"):
        out[f"KOD:{f}"] = _mk_sha(os.path.join(KOK_MK, f))
    c2c = C2.C2_YOL["cikti"]
    for ad, y in (("C2_ESIK22_JSON_SHA", os.path.join(c2c, "cetvel2_esik_v2.2.json")), ("C2_GUC22_JSON_SHA", os.path.join(c2c, "cetvel2_guc_v2.2.json"))):
        out[ad] = _mk_sha(y)
    return out


def mk_kapi(veri: str, kesik: str) -> Dict[str, Any]:
    """KASA kapısı: V_*.pkl en geç tarihi <= kesik (KS.kasa_kapisi); değilse DURUR (fail-closed)."""
    yollar = [os.path.join(veri, f"V_{p}.pkl") for p in MK_PAZAR]
    try:
        K = KS.kasa_kapisi(yollar, kesik)
    except KS.KasaHata as ex:
        raise MKHata(f"KASA kapısı KAPALI: {ex}") from ex
    durum = None
    yd = os.path.join(veri, KS.KS_DURUM_AD)
    if os.path.exists(yd):
        durum = json.load(open(yd, encoding="utf-8"))
    return {"kesik": K["kesik"], "dosya": K["dosya"], "durum": durum}


# ================================================================ 1) ZİNCİR, PFc, MRc, T
def mk_zincir(U: pd.DataFrame, ara: Optional[int] = None) -> pd.DataFrame:
    """U1 olayları (pazar, sembol, i, tarih, low_L1, low_L2, F66, F66m, close_L2) -> zincir, PFc, MRc, T. Yalnız geçmiş olaylar."""
    ara = int(ara if ara is not None else MK_ESIK["zincir"]["ara_bar"])
    gerek = ["pazar", "sembol", "i", "tarih", "low_L1", "low_L2", "F66", "F66m", "close_L2"]
    eks = [k for k in gerek if k not in U.columns]
    if eks:
        raise MKHata(f"zincir girdisinde sütun yok: {eks}")
    X = U.sort_values(["pazar", "sembol", "i"], kind="mergesort").reset_index(drop=True)
    n = len(X)
    z = np.ones(n, np.int64); ilk = np.arange(n)
    pz = X.pazar.to_numpy(); sb = X.sembol.to_numpy(); ii = X.i.to_numpy(np.int64); lo2 = X.low_L2.to_numpy(float)
    for k in range(1, n):
        if pz[k] == pz[k - 1] and sb[k] == sb[k - 1] and ii[k] - ii[k - 1] <= ara and lo2[k] < lo2[k - 1]:
            z[k] = z[k - 1] + 1; ilk[k] = ilk[k - 1]
    lo1f = X.low_L1.to_numpy(float)[ilk]
    m1 = (X.F66m.to_numpy(float)[ilk] - X.F66.to_numpy(float)[ilk]) * X.close_L2.to_numpy(float)[ilk]
    m2 = X.F66m.to_numpy(float) * X.close_L2.to_numpy(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        X["zincir"] = z
        X["PFc"] = lo2 / lo1f - 1.0
        X["MRc"] = (m2 - m1) / np.abs(m1)
    T = MK_ESIK["T"]
    X["T"] = (X.PFc.to_numpy(float) <= float(T["PFc_ust"])) & (X.MRc.to_numpy(float) >= float(T["MRc_alt"]))
    return X


# ================================================================ 2) PAZAR: olay -> zincir -> eş -> h5
def mk_pazar(p: str, veri: str, donem: Dict[str, List[str]]) -> Dict[str, Any]:
    """Bir pazar: MU.mu_pazar (U1) -> mk_zincir -> CETVEL2 v2.2 eş + K20 temiz eş (MACD_UYUM_ES) -> MU.mu_olc_h5. Hepsi mevcut modüllerden."""
    t0 = time.time()
    Pb = C2.c2_panel22_al(p, veri, None)
    O, _ = MU.mu_pazar(p, veri, Pb["Vd"])
    U = O[O.hipotez == "U1"].copy()
    Zc = mk_zincir(U)
    Pn = C2.c2_panel22_al(p, veri, int(ES.ES_ESIK["ufuk"]))
    B = ES.es_panel_bayrak(Pn)
    X, _ = C2.c2_olay(U[["sembol", "tarih"]].copy(), Pn, int(ES.ES_ESIK["tekil_gun"]))
    X["donem"] = C2._c2_donem22(X.giris, donem)
    d = X.d.to_numpy(np.int64)
    e0 = ES.es_es(Pn, X)
    kd, kj = ES.es_kirli_cift(Pn, B["K20"], d)
    ET = ES.es_es(Pn, X, kd, kj)
    X["es_r15"] = e0["es_r15"]; X["n_es"] = e0["n_es"]; X["sira"] = e0["sira"]
    X["es_r15_temiz"] = ET["es_r15"]; X["n_es_temiz"] = ET["n_es"]; X["fark_temiz"] = ET["fark"]; X["sira_temiz"] = ET["sira"]
    X["pazar"] = p
    Z5 = MU.mu_olc_h5(O, "U1", p, veri)
    if len(Z5):
        Z5 = Z5[["sembol", "tarih", "h5", "st5", "es_h5", "es_st5", "cikis_tur"]].copy()
        Z5["tarih"] = pd.to_datetime(Z5.tarih)
        X = X.merge(Z5, on=["sembol", "tarih"], how="left", validate="one_to_one")
    else:
        for k in ("h5", "st5", "es_h5", "es_st5", "cikis_tur"):
            X[k] = np.nan
    Zk = Zc[["sembol", "tarih", "i", "zincir", "PFc", "MRc", "T", "F65"]].copy(); Zk["tarih"] = pd.to_datetime(Zk.tarih)
    X = X.merge(Zk, on=["sembol", "tarih"], how="left", validate="one_to_one")
    if X.zincir.isna().any():
        raise MKHata(f"{p}: eşli olayların {int(X.zincir.isna().sum())} tanesinde zincir yok (iç tutarlılık)")
    mklog.info("%s tamam (%.0f sn): U1 %d, c2_olay %d, temiz eşli %d", p, time.time() - t0, len(U), len(X),
               int(np.isfinite(X.fark_temiz.to_numpy(float)).sum()))
    return {"pazar": p, "O": O, "U": Zc, "X": X, "Vd": Pb["Vd"]}


# ================================================================ 3) HÜCRE ve ÜST10
def mk_hucre(x: pd.DataFrame, p: Optional[str], hucre: Optional[str], tek: int) -> Dict[str, Any]:
    """Ö2 hücresi: C2.c2_hucre (+ güç eğrisi; KASA hücre adı eğride yoksa 'acik' eğrisi) + MU.mu_sira_boot + MU.mu_hukum (plasebo hariç).
    p None (birleşik): eğri yok -> güç NaN -> hüküm ÖLÇÜLEMEDİ (yalnız FARK / boot / SIRA bilgi)."""
    x = x.dropna(subset=["r15", "es_r15_temiz"])
    if len(x) < 2:
        return {"n": int(len(x)), "fark": np.nan, "hukum": "ÖLÇÜLEMEDİ", "hukum_neden": "n < 2"}
    eg = C2._c2_egri22_al(p, hucre, 15, None) if p else None
    c = C2.c2_hucre(x.r15.to_numpy(float), x.es_r15_temiz.to_numpy(float), x.sira_temiz.to_numpy(float), x.giris.to_numpy(), "+",
                    tohum_ek=int(tek), egri=eg)
    ay = pd.to_datetime(x.giris).dt.strftime("%Y-%m").to_numpy()
    c["sira_alt"], c["sira_ust"] = MU.mu_sira_boot(x.sira_temiz.to_numpy(float), ay, int(tek)); c["plasebo_gecti"] = True
    h, hn = MU.mu_hukum(c)
    f = lambda k: float(np.nanmean(x[k].to_numpy(float))) if k in x and np.isfinite(x[k].to_numpy(float)).any() else np.nan  # noqa: E731
    return {"n": int(c["n"]), "fark": c["fark"], "boot_alt": c["boot_alt"], "boot_ust": c["boot_ust"], "med": c["med"], "sira": c["sira"],
            "sira_alt": c["sira_alt"], "l3o": c["l3o"], "p": c["p"], "guc": c["guc"], "hukum": h, "hukum_neden": hn,
            "egri_hucre": (hucre if hucre in C2.C2_HUCRE22 else "acik") if p else None,
            "r15": f("r15"), "es": f("es_r15_temiz"), "h5": f("h5"), "es_h5": f("es_h5"), "st5": f("st5"), "es_st5": f("es_st5"),
            "n_h5": int(np.isfinite(x.h5.to_numpy(float)).sum()) if "h5" in x else 0}


def mk_ust10(x: pd.DataFrame, tek: int) -> Dict[str, Any]:
    """Ö1: ÜST10 = temiz eş sırası >= 0,90 payı; ALT10 <= 0,10; ay kümeli boot %95 (MU.mu_sira_boot: B 2000, giriş ayı)."""
    x = x.dropna(subset=["r15", "es_r15_temiz"])
    n = int(len(x))
    if n == 0:
        return {"n": 0, "ust10": np.nan, "lo": np.nan, "hi": np.nan, "alt10": np.nan, "alt_lo": np.nan, "alt_hi": np.nan, "ust20": np.nan}
    s = x.sira_temiz.to_numpy(float); ay = pd.to_datetime(x.giris).dt.strftime("%Y-%m").to_numpy()
    u = (s >= float(MK_ESIK["ust10"])).astype(float); a = (s <= float(MK_ESIK["alt10"])).astype(float)
    lo, hi = MU.mu_sira_boot(u, ay, int(tek)); alo, ahi = MU.mu_sira_boot(a, ay, int(tek) + 1)
    return {"n": n, "ust10": float(u.mean()), "lo": lo, "hi": hi, "alt10": float(a.mean()), "alt_lo": alo, "alt_hi": ahi,
            "ust20": float((s >= float(MK_ESIK["ust20"])).mean()), "r15": float(x.r15.mean()), "es": float(x.es_r15_temiz.mean()),
            "ay": int(len(np.unique(ay)))}


def mk_karar(u_bir: Dict[str, Any], u_abd: Dict[str, Any], u_avr: Dict[str, Any], fark_bir: float) -> Dict[str, Any]:
    """Ön kayıt karar kuralı HARFİYEN. (a) birleşik ÜST10 boot alt > 0,10; (b) birleşik ÜST10 > ALT10; (c) ABD ve AVR ÜST10 nokta > 0,10;
    (d) birleşik R15 FARK > 0. TUTTU = a∧b∧c∧d; KISMEN = b∧c∧d∧¬a; TUTMADI aksi; birleşik n < 100 -> ÖLÇÜLEMEDİ (yön yine yazılır)."""
    t = float(MK_ESIK["karar"]["ust10_taban"])
    ok = lambda v: v is not None and np.isfinite(v)  # noqa: E731
    a = bool(ok(u_bir.get("lo")) and u_bir["lo"] > t)
    b = bool(ok(u_bir.get("ust10")) and ok(u_bir.get("alt10")) and u_bir["ust10"] > u_bir["alt10"])
    c = bool(ok(u_abd.get("ust10")) and u_abd["ust10"] > t and ok(u_avr.get("ust10")) and u_avr["ust10"] > t)
    d = bool(ok(fark_bir) and fark_bir > 0)
    madde = {"a": a, "b": b, "c": c, "d": d}
    if int(u_bir.get("n", 0)) < int(MK_ESIK["karar"]["n_min"]):
        k = "ÖLÇÜLEMEDİ"
    elif a and b and c and d:
        k = "TUTTU"
    elif b and c and d and not a:
        k = "KISMEN"
    else:
        k = "TUTMADI"
    return {"karar": k, "madde": madde, "n_birlesik": int(u_bir.get("n", 0))}


# ================================================================ 4) PREFIX (K2) ve YENİDEN ÜRETİM (K11)
def mk_prefix(R: Dict[str, Any], Xk: pd.DataFrame, p: str, pi: int) -> Dict[str, Any]:
    """K2: pazar başına 30 rastgele KASA olayı; hissenin verisi t'de kesilir; U1 (mu_hisse), zincir, PFc, MRc, T yeniden; aynı olmalı."""
    Pr = MK_ESIK["prefix"]; rng = np.random.default_rng([int(Pr["tohum"]), int(pi)])
    if not len(Xk):
        return {"pazar": p, "n": 0, "tuttu": 0, "olay": []}
    sat, bozuk = [], []
    for x in rng.choice(len(Xk), min(int(Pr["n"]), len(Xk)), replace=False):
        r = Xk.iloc[int(x)]; t = pd.Timestamp(r.tarih)
        ham = R["Vd"]["V"][r.sembol]; kes = YH._yh_hazir(ham[ham.index <= t])
        Ok, _ = MU.mu_hisse(kes)
        Uk = Ok[Ok.hipotez == "U1"].copy(); Uk.insert(0, "sembol", r.sembol); Uk.insert(0, "pazar", p)
        Zk = mk_zincir(Uk) if len(Uk) else Uk
        e = Zk[pd.to_datetime(Zk.tarih) == t] if len(Zk) else Zk
        tut = len(e) == 1
        if tut:
            e = e.iloc[0]
            a = np.array([float(r.zincir), float(r.PFc), float(r.MRc), float(bool(r["T"]))])
            b = np.array([float(e.zincir), float(e.PFc), float(e.MRc), float(bool(e["T"]))])
            tut = bool(np.array_equal(a, b, equal_nan=True))
        sat.append({"sembol": r.sembol, "tarih": str(t.date()), "T": bool(r["T"]), "tuttu": tut})
        if not tut:
            bozuk.append(sat[-1])
    if bozuk:
        raise MKHata(f"{p}: prefix (K2) TUTMADI {len(bozuk)} / {len(sat)}: {bozuk[:3]} -> DURDU")
    return {"pazar": p, "n": len(sat), "tuttu": int(sum(s["tuttu"] for s in sat)), "T_say": int(sum(s["T"] for s in sat)), "olay": sat}


def mk_yeniden(satir: str, J: Dict[str, Any]) -> Dict[str, Any]:
    """K11: satır dosyasından bağımsız düz pandas: birleşik (ABD + AVR) T ÜST10 / ALT10 / n ve ABD T FARK / n. Göreli 1e-9 değilse DURUR."""
    Y = pd.read_csv(satir)
    Y = Y[(Y["T"].astype(str).str.lower().isin(["true", "1"])) & Y.r15.notna() & Y.es_r15_temiz.notna()]
    b = Y[Y.pazar.isin(["ABD", "AVR"])]; a = Y[Y.pazar == "ABD"]
    yen = {"birlesik_ust10": float((b.sira_temiz >= 0.90).mean()), "birlesik_alt10": float((b.sira_temiz <= 0.10).mean()), "birlesik_n": int(len(b)),
           "abd_fark": float((a.r15 - a.es_r15_temiz).mean()), "abd_n": int(len(a))}
    ref = J["O1"]["T|birlesik"], J["O2"]["T|ABD"]
    ok = (yen["birlesik_n"] == ref[0]["n"] and np.isclose(yen["birlesik_ust10"], ref[0]["ust10"], rtol=1e-9)
          and np.isclose(yen["birlesik_alt10"], ref[0]["alt10"], rtol=1e-9) and yen["abd_n"] == ref[1]["n"]
          and np.isclose(yen["abd_fark"], ref[1]["fark"], rtol=1e-9))
    yen["tuttu"] = bool(ok)
    if not ok:
        raise MKHata(f"K11 yeniden üretim tutmadı: {yen} -> DURDU")
    return yen


# ================================================================ 5) DOĞRULAMA (açık veri, kasa açılmadan önce)
def mk_dogrula(veri: str, cikti: Optional[str] = None) -> Dict[str, Any]:
    """Aynı kod açık kesitte (<= 2022-12-31): U1 = uyum_olay; zincir / PFc / MRc = uyum_zincir / uyum_toplam; eş = es_satir; h5 = uyum_satir;
    T hücreleri = uyum_t_sonuc (n, FARK, boot, hüküm; Ç223 tohumları); ÜST10 / ALT10 = uyum_ust10_bilgi. Biri tutmazsa MKHata."""
    t0 = time.time(); c = cikti or MK_YOL["cikti"]; Dg = MK_ESIK["dogrulama"]
    G = mk_kapi(veri, MK_ESIK["acik"]["kesik"])
    Oref = pd.read_csv(_mk_yol("olay", c)); Oref = Oref[Oref.hipotez == "U1"]
    Zref = pd.read_csv(_mk_yol("zincir", c)).merge(pd.read_csv(_mk_yol("toplam", c)), on=["pazar", "sembol", "tarih"], validate="one_to_one")
    Eref = pd.read_csv(_mk_yol("es", c)); Sref = pd.read_csv(_mk_yol("c217_satir", c)); Sref = Sref[Sref.hipotez == "U1"]
    out: Dict[str, Any] = {"zaman": _mk_simdi(), "kapi": G, "pazar": {}}
    Xs, Us = [], []
    for p in MK_PAZAR:
        R = mk_pazar(p, veri, dict(ES.ES_DONEM))
        U = R["U"].copy(); U["tarih"] = pd.to_datetime(U.tarih).dt.strftime("%Y-%m-%d")
        X = R["X"].copy(); X["tarih"] = pd.to_datetime(X.tarih).dt.strftime("%Y-%m-%d")
        # (1) U1 olayları
        o = Oref[Oref.pazar == p].sort_values(["sembol", "i"]).reset_index(drop=True)
        u = U.sort_values(["sembol", "i"]).reset_index(drop=True)
        kol_t = ["sembol", "tarih", "i", "L1", "L2", "L1_tarih", "L2_tarih"]
        kol_s = ["tL2", "F65", "F66", "F66m", "F66h", "F67", "F68", "low_L1", "low_L2", "close_L2", "close_t", "rsi_L1", "rsi_L2", "stop0"]
        u_kt = u[kol_t].copy()
        for k in ("L1_tarih", "L2_tarih"):
            u_kt[k] = pd.to_datetime(u_kt[k]).dt.strftime("%Y-%m-%d")
        ok1 = len(o) == len(u) and (o[kol_t].astype(str).to_numpy() == u_kt.astype(str).to_numpy()).all() and \
            all(np.allclose(o[k].to_numpy(float), u[k].to_numpy(float), rtol=Dg["olay_rtol"], atol=0, equal_nan=True) for k in kol_s)
        # (2) zincir / PFc / MRc
        z = Zref[Zref.pazar == p].merge(U[["sembol", "tarih", "zincir", "PFc", "MRc"]], on=["sembol", "tarih"], how="outer",
                                        suffixes=("_ref", ""), indicator=True)
        ok2 = bool((z._merge == "both").all() and (z.zincir_ref == z.zincir).all()
                   and np.allclose(z.PFc_ref, z.PFc, rtol=0, atol=Dg["zincir_atol"]) and np.allclose(z.MRc_ref, z.MRc, rtol=0, atol=Dg["zincir_atol"]))
        # (3) eş satırları
        e = Eref[Eref.pazar == p].merge(X[["sembol", "tarih", "giris", "donem", "r15", "es_r15_temiz", "n_es_temiz", "sira_temiz", "fark_temiz",
                                           "n_es"]], on=["sembol", "tarih"], how="outer", suffixes=("_ref", ""), indicator=True)
        ok3 = bool((e._merge == "both").all() and (e.donem_ref == e.donem).all() and (e.n_es_temiz_ref == e.n_es_temiz).all()
                   and (e.n_es_ref == e.n_es).all()
                   and all(np.allclose(e[f"{k}_ref"].to_numpy(float), e[k].to_numpy(float), rtol=Dg["dt_rtol"], atol=1e-12, equal_nan=True)
                           for k in ("r15", "es_r15_temiz", "sira_temiz", "fark_temiz")))
        # (4) h5 / st5
        s = Sref[Sref.pazar == p][["sembol", "tarih", "h5", "st5", "es_h5", "es_st5"]].merge(
            X[["sembol", "tarih", "h5", "st5", "es_h5", "es_st5"]], on=["sembol", "tarih"], how="left", suffixes=("_ref", ""))
        ok4 = bool(len(s) == int((Sref.pazar == p).sum()) and all(
            np.allclose(s[f"{k}_ref"].to_numpy(float), s[k].to_numpy(float), rtol=1e-9, atol=1e-12, equal_nan=True) for k in ("h5", "st5", "es_h5", "es_st5")))
        out["pazar"][p] = {"U1": {"n_ref": int(len(o)), "n": int(len(u)), "tuttu": bool(ok1)}, "zincir": {"n": int(len(z)), "tuttu": ok2},
                           "es": {"n_ref": int((Eref.pazar == p).sum()), "n": int(len(X)), "tuttu": ok3}, "h5": {"n": int(len(s)), "tuttu": ok4}}
        mklog.info("%s doğrulama: U1 %s, zincir %s, eş %s, h5 %s", p, ok1, ok2, ok3, ok4)
        Xs.append(R["X"]); Us.append(R["U"])
    E = pd.concat(Xs, ignore_index=True)
    E["giris"] = pd.to_datetime(E.giris)
    # (5) T hücreleri (toplam_olc.py tohumları)
    J = json.load(open(_mk_yol("t_sonuc", c), encoding="utf-8"))["hucre"]
    hc = {}; ok5 = True
    for g, M in (("T (derin toplam)", E["T"].astype(bool)), ("Tz (kalan)", ~E["T"].astype(bool))):
        for i, p in enumerate(MK_PAZAR):
            for j, h in enumerate(("d1619", "d2022")):
                x = E[M & (E.pazar == p) & (E.donem == h)]
                v = mk_hucre(x, p, h, int(Dg["tohum_T"]) + 10 * i + j)
                ref = J[f"{g}|{p}|{h}"]
                ok = (v["n"] == ref["n"] and np.isclose(v["fark"], ref["fark"], rtol=1e-9) and np.isclose(v["boot_alt"], ref["a"], rtol=1e-9)
                      and np.isclose(v["sira"], ref["sira"], rtol=1e-9) and v["hukum"] == ref["hukum"])
                hc[f"{g}|{p}|{h}"] = {"n": v["n"], "fark": v["fark"], "boot_alt": v["boot_alt"], "hukum": v["hukum"], "ref_n": ref["n"],
                                      "ref_fark": ref["fark"], "tuttu": bool(ok)}
                ok5 = ok5 and bool(ok)
    for k, (n_, f_) in Dg["beklenen_T"].items():
        v = hc[f"T (derin toplam)|{k}"]
        ok5 = ok5 and v["n"] == n_ and abs(v["fark"] - f_) < 5e-5
    # (6) ÜST10 / ALT10 (ABD + AVR, d1619 + d2022)
    b = E[E["T"].astype(bool) & E.pazar.isin(["ABD", "AVR"]) & E.donem.isin(["d1619", "d2022"])]
    u10 = mk_ust10(b, int(MK_ESIK["tohum"]["ust10"]))
    Bk = Dg["beklenen_ust10"]; Ju = json.load(open(_mk_yol("ust10", c), encoding="utf-8"))["derin toplam (zincir)|hepsi"]
    ok6 = bool(u10["n"] == Bk["n"] == Ju["n"] and np.isclose(u10["ust10"], Ju["ust10"], rtol=1e-12) and np.isclose(u10["alt10"], Ju["alt10"], rtol=1e-12))
    out.update({"T_hucre": hc, "T_tuttu": bool(ok5), "ust10": {**u10, "ref": Ju, "tuttu": ok6}})
    hepsi = all(v[k]["tuttu"] for v in out["pazar"].values() for k in ("U1", "zincir", "es", "h5")) and ok5 and ok6
    out["tuttu"] = bool(hepsi); out["sure_sn"] = round(time.time() - t0, 1); out["sha"] = mk_sha_simdi()
    _mk_jyaz(_mk_yol("dogrulama", c), out)
    if not hepsi:
        raise MKHata(f"DOĞRULAMA TUTMADI (ayrıntı {MK_DOSYA['dogrulama']}) -> DURDU")
    mklog.info("doğrulama TUTTU (%.0f sn)", time.time() - t0)
    return out


# ================================================================ 6) KASA ÖLÇÜMÜ
def _mk_giris_filtre(X: pd.DataFrame) -> pd.DataFrame:
    K = MK_ESIK["kasa"]
    g = pd.to_datetime(X.giris)
    return X[(g >= pd.Timestamp(K["giris_ilk"])) & (g <= pd.Timestamp(K["giris_son"]))].copy()


def mk_olc(veri: str, cikti: Optional[str] = None, uzerine: bool = False) -> Dict[str, Any]:
    """KASA verisinde (<= 2024-12-31): olaylar (zincir geçmişi 2022 ve öncesinden), giriş 2023-01-01 .. 2024-12-31, R15 penceresi veri sonunu
    aşmayan (R15 sonlu) olaylar. Ö1 / Ö2 / Ö3, prefix, K11, karar -> satır / sonuç / rapor."""
    t0 = time.time(); c = cikti or MK_YOL["cikti"]; K = MK_ESIK["kasa"]; Tt = MK_ESIK["tohum"]
    for ad in ("satir", "sonuc", "rapor"):
        if os.path.exists(_mk_yol(ad, c)) and not uzerine:
            raise MKHata(f"{MK_DOSYA[ad]} zaten var: kasa bu hipotez için bir kez ölçülür (ikinci koşu DURDU)")
    import IZ_KARNE as IK
    try:
        IK.ik_kontrol_kapisi(_mk_yol("onkayit", c))
    except RuntimeError as ex:
        raise MKHata(str(ex)) from ex
    G = mk_kapi(veri, K["kesik"])
    zaman = _mk_simdi()
    Xs, pre = [], {}
    for pi, p in enumerate(MK_PAZAR):
        R = mk_pazar(p, veri, dict(K["donem"]))
        Xk = _mk_giris_filtre(R["X"])
        pre[p] = mk_prefix(R, Xk.reset_index(drop=True), p, pi)
        Xs.append(Xk)
        del R
    E = pd.concat(Xs, ignore_index=True)
    E["giris"] = pd.to_datetime(E.giris); E["T"] = E["T"].astype(bool); E["yil"] = E.giris.dt.year
    son_g = pd.Timestamp(K["kesik"])
    if (E.giris > son_g).any() or (E.giris < pd.Timestamp(K["giris_ilk"])).any():
        raise MKHata("giriş günü kasa dönemi dışında (iç tutarlılık)")
    Eo = E.dropna(subset=["r15", "es_r15_temiz"])
    O1: Dict[str, Any] = {}; O2: Dict[str, Any] = {}; O3: Dict[str, Any] = {}
    for g, M in (("T", Eo["T"]), ("Tz", ~Eo["T"])):
        X = Eo[M]
        for i, p in enumerate(MK_PAZAR):
            xp = X[X.pazar == p]
            O1[f"{g}|{p}"] = mk_ust10(xp, int(Tt["ust10"]) + 10 * i + (0 if g == "T" else 5))
            O2[f"{g}|{p}"] = mk_hucre(xp, p, "k2324", int(Tt[g]) + 10 * i)
            for y in (2023, 2024):
                xy = xp[xp.yil == y]
                O3[f"{g}|{p}|{y}|ust10"] = mk_ust10(xy, int(Tt["yil"]) + 10 * i + (y - 2023) + (0 if g == "T" else 5))
                O3[f"{g}|{p}|{y}|hucre"] = mk_hucre(xy, p, f"y{y}", int(Tt["yil"]) + 100 + 10 * i + (y - 2023) + (0 if g == "T" else 5))
            for ad, mm in (("yukari", xp.es_r15_temiz > 0), ("asagi", xp.es_r15_temiz <= 0)):
                O3[f"{g}|{p}|{ad}"] = mk_ust10(xp[mm], int(Tt["piyasa"]) + 10 * i + (0 if ad == "yukari" else 1) + (0 if g == "T" else 5))
        xb = X[X.pazar.isin(MK_ESIK["karar"]["pazar"])]
        O1[f"{g}|birlesik"] = mk_ust10(xb, int(Tt["birlesik"]) + (0 if g == "T" else 5))
        O2[f"{g}|birlesik"] = mk_hucre(xb, None, None, int(Tt["birlesik"]) + 100 + (0 if g == "T" else 5))
        for y in (2023, 2024):
            O3[f"{g}|birlesik|{y}|ust10"] = mk_ust10(xb[xb.yil == y], int(Tt["yil"]) + 200 + (y - 2023) + (0 if g == "T" else 5))
            O3[f"{g}|birlesik|{y}|hucre"] = mk_hucre(xb[xb.yil == y], None, None, int(Tt["yil"]) + 300 + (y - 2023) + (0 if g == "T" else 5))
        for ad, mm in (("yukari", xb.es_r15_temiz > 0), ("asagi", xb.es_r15_temiz <= 0)):
            O3[f"{g}|birlesik|{ad}"] = mk_ust10(xb[mm], int(Tt["piyasa"]) + 100 + (0 if ad == "yukari" else 1) + (0 if g == "T" else 5))
    karar = mk_karar(O1["T|birlesik"], O1["T|ABD"], O1["T|AVR"], O2["T|birlesik"]["fark"])
    # huni (getirisiz sayımlar)
    huni = {}
    for p in MK_PAZAR:
        x = E[E.pazar == p]
        huni[p] = {"U1_c2_olay": int(len(x)), "T": int(x["T"].sum()), "r15_sonlu": int(np.isfinite(x.r15.to_numpy(float)).sum()),
                   "temiz_esli": int(len(Eo[Eo.pazar == p])), "T_temiz_esli": int(Eo[(Eo.pazar == p)]["T"].sum()),
                   "r15_yok_donem_sonu": int((~np.isfinite(x.r15.to_numpy(float))).sum())}
    # satır dosyası
    kol = ["pazar", "sembol", "tarih", "giris", "zincir", "PFc", "MRc", "T", "F65", "r15", "es_r15_temiz", "n_es_temiz", "sira_temiz", "fark_temiz",
           "h5", "st5", "es_h5", "es_st5", "es_r15", "n_es", "sira", "kova", "donem"]
    S = E[[k for k in kol if k in E.columns]].copy()
    S["tarih"] = pd.to_datetime(S.tarih).dt.strftime("%Y-%m-%d"); S["giris"] = pd.to_datetime(S.giris).dt.strftime("%Y-%m-%d")
    S = S.sort_values(["pazar", "sembol", "tarih"], kind="mergesort")
    sy = _mk_yol("satir", c)
    S.to_csv(sy, index=False, float_format="%.15g", compression={"method": "gzip", "mtime": 0})
    en_gec = KS.ks_en_gec_tarih(sy)
    if en_gec is not None and en_gec > son_g:
        raise MKHata(f"satır dosyasında kesik aşımı: {en_gec}")
    J: Dict[str, Any] = {"surum": MK_SURUM, "zaman": zaman, "kapi": G, "esik_sha": mk_esik_sha(), "sha": mk_sha_simdi(), "huni": huni,
                         "O1": O1, "O2": O2, "O3": O3, "karar": karar, "prefix": pre,
                         "satir_dosya": os.path.relpath(sy, KOK_MK), "satir_sha": _mk_sha(sy),
                         "satir_en_gec_tarih": str(en_gec.date()) if en_gec is not None else None}
    J["yeniden"] = mk_yeniden(sy, J)
    J["sure_sn"] = round(time.time() - t0, 1)
    _mk_jyaz(_mk_yol("sonuc", c), J)
    mk_rapor(J, c)
    mklog.info("kasa ölçümü bitti: KARAR %s %s (%.0f sn)", karar["karar"], karar["madde"], time.time() - t0)
    return J


# ================================================================ 7) RAPOR
def _y(x: Any, n: int = 1, isaret: bool = False) -> str:
    if x is None or not np.isfinite(x):
        return "-"
    return (f"{x * 100:+.{n}f}" if isaret else f"{x * 100:.{n}f}").replace(".", ",")


def _s(x: Any, n: int = 3) -> str:
    return "-" if x is None or not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


def mk_rapor(J: Dict[str, Any], cikti: Optional[str] = None) -> str:
    c = cikti or MK_YOL["cikti"]; K = J["karar"]; L: List[str] = []
    L += [f"# MACD_UYUM — KASA KÖR SINAMASI SONUCU (T: derin toplam uyumsuzluk; 2023-24)", "",
          f"KARAR: **{K['karar']}** — madde (a) birleşik ÜST10 boot alt > 0,10: {K['madde']['a']}; (b) ÜST10 > ALT10: {K['madde']['b']}; "
          f"(c) ABD ve AVR ÜST10 > 0,10: {K['madde']['c']}; (d) birleşik FARK > 0: {K['madde']['d']}; birleşik n {K['n_birlesik']}.",
          "", f"Ön kayıt: arastirma_cikti/macd_uyum/KASA_T_ON_KAYIT.md (ana bölüm 2aedf2e). Koşu UTC {J['zaman']}. Kod {MK_SURUM}.",
          f"Veri kesiği {J['kapi']['kesik']} (en geç tarih: {', '.join(f'{os.path.basename(k)} {v}' for k, v in J['kapi']['dosya'].items())}).", "",
          "## Ö1 ÜST10 / ALT10 (temiz eş sırası; ay kümeli boot %95)", "",
          "| Grup | Hücre | n | ÜST10 [%95] | ALT10 [%95] | ÜST20 | r15 ort | eş ort |", "|---|---|---|---|---|---|---|---|"]
    for g in ("T", "Tz"):
        for h in ("ABD", "AVR", "birlesik", "BIST"):
            u = J["O1"][f"{g}|{h}"]
            L.append(f"| {g} | {h} | {u['n']} | %{_y(u['ust10'])} [{_y(u['lo'])}; {_y(u['hi'])}] | %{_y(u['alt10'])} [{_y(u.get('alt_lo'))}; "
                     f"{_y(u.get('alt_hi'))}] | %{_y(u.get('ust20'))} | {_y(u.get('r15'), 2, True)} | {_y(u.get('es'), 2, True)} |")
    L += ["", "Piyasa yukarı (eş ort > 0) / aşağı (<= 0):", "", "| Grup | Hücre | Piyasa | n | ÜST10 [%95] | ALT10 |", "|---|---|---|---|---|---|"]
    for g in ("T", "Tz"):
        for h in ("ABD", "AVR", "birlesik", "BIST"):
            for ad in ("yukari", "asagi"):
                u = J["O3"][f"{g}|{h}|{ad}"]
                L.append(f"| {g} | {h} | {ad} | {u['n']} | %{_y(u['ust10'])} [{_y(u['lo'])}; {_y(u['hi'])}] | %{_y(u['alt10'])} |")
    L += ["", "## Ö2 R15 temiz eş FARK (C2.c2_hucre + MU.mu_hukum, plasebo hariç; güç eğrisi 'acik')", "",
          "| Grup | Hücre | n | FARK [%95] | medyan | SIRA [alt] | L3O | güç | hüküm | +%5 olay / eş | stop olay / eş |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for g in ("T", "Tz"):
        for h in ("ABD", "AVR", "birlesik", "BIST"):
            v = J["O2"][f"{g}|{h}"]
            L.append(f"| {g} | {h} | {v['n']} | {_y(v.get('fark'), 2, True)} [{_y(v.get('boot_alt'), 2, True)}; {_y(v.get('boot_ust'), 2, True)}] | "
                     f"{_y(v.get('med'), 2, True)} | {_s(v.get('sira'))} [{_s(v.get('sira_alt'))}] | {_y(v.get('l3o'), 2, True)} | {_s(v.get('guc'), 2)} | "
                     f"{v.get('hukum')} | %{_y(v.get('h5'))} / %{_y(v.get('es_h5'))} | %{_y(v.get('st5'))} / %{_y(v.get('es_st5'))} |")
    L += ["", "## Yıl ayrımı (bilgi)", "", "| Grup | Hücre | Yıl | n | ÜST10 | ALT10 | FARK [%95] |", "|---|---|---|---|---|---|---|"]
    for g in ("T", "Tz"):
        for h in ("ABD", "AVR", "birlesik", "BIST"):
            for y in (2023, 2024):
                u = J["O3"][f"{g}|{h}|{y}|ust10"]; v = J["O3"][f"{g}|{h}|{y}|hucre"]
                L.append(f"| {g} | {h} | {y} | {u['n']} | %{_y(u['ust10'])} | %{_y(u['alt10'])} | {_y(v.get('fark'), 2, True)} "
                         f"[{_y(v.get('boot_alt'), 2, True)}; {_y(v.get('boot_ust'), 2, True)}] |")
    L += ["", "## Huni, prefix, yeniden üretim", "", "```", json.dumps(J["huni"], ensure_ascii=False),
          json.dumps({p: {k: v[k] for k in ("n", "tuttu", "T_say") if k in v} for p, v in J["prefix"].items()}, ensure_ascii=False),
          json.dumps(J["yeniden"], ensure_ascii=False), "```", "",
          f"Satır dosyası: {J['satir_dosya']} (sha {J['satir_sha'][:16]}…; en geç tarih {J['satir_en_gec_tarih']}).", "",
          "Sınırlar: evren bugün işlem gören hisseler (batanlar yok; sonuç yukarı yanlı). Komisyon / kayma yok. Tek başına alım-satım kuralı değildir.", ""]
    yol = _mk_yol("rapor", c)
    with open(yol, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return yol


# ================================================================ 8) ÇAKIŞMA KAPISI ve CLI
def _cakisma_kontrol_mk(_once=_CK_ONCE_MK, _dosya="MACD_UYUM_KASA.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_MK", "_CK_KAYIT", "_cakisma_kontrol_mk", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "hashlib", "time", "_dt", "annotations", "Any", "Dict", "List", "Optional", "Tuple",
           "C2", "KS", "MU", "ES", "YH", "_y", "_s")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_mk()


def _mk_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=MK_SURUM)
    alt = ap.add_subparsers(dest="komut", required=True)
    for k in ("dogrula", "olc", "sha"):
        p = alt.add_parser(k); p.add_argument("--veri", default=None); p.add_argument("--cikti", default=None)
    a = ap.parse_args(argv)
    try:
        if a.komut == "sha":
            print(json.dumps(mk_sha_simdi(), ensure_ascii=False, indent=1))
            return 0
        if not a.veri:
            raise MKHata("--veri zorunlu (varsayılan veri yolu yok)")
        if a.komut == "dogrula":
            J = mk_dogrula(a.veri, a.cikti)
            print("DOĞRULAMA:", "TUTTU" if J["tuttu"] else "TUTMADI")
        else:
            J = mk_olc(a.veri, a.cikti)
            print("KARAR:", J["karar"]["karar"], J["karar"]["madde"])
    except MKHata as ex:
        mklog.error("%s", ex)
        print(f"DURDU: {ex}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__" and "get_ipython" not in globals():
    sys.exit(_mk_ana())
