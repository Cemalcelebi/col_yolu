"""CETVEL2 YENİDEN KOŞU (ADIM H; iş tanımı arastirma_cikti/cetvel2/CETVEL2_IS_TANIMI.md bölüm 4).

18-20 Kasım testlerinin (Ç194-Ç202 + hakem turları 4 / 6) AYNI olay kümeleri ve AYNI eşikleriyle (bayraklar dosyadan okunur ya da ilgili
modülün maske fonksiyonu AYNEN çağrılır; sha ön kayıtta) CETVEL2 v2.1 (C2.c2_olc: R15 konum eşli fark, plasebo kapısı, güç, BH) ile yeniden
ölçülmesi. ESKİ (h5 cetveli: rapordaki etiket ve FARK) ve YENİ (R15 FARK [boot], SIRA, plasebo kapısı, etiket) yan yana; 'DEĞİŞTİ Mİ'.

Komut:  python arastirma_cikti/cetvel2/c2_yeniden_kosu.py huni            getirisiz bayrak sayımı + regresyon (ön kayıt girdisi)
        python arastirma_cikti/cetvel2/c2_yeniden_kosu.py onkayit         YENIDEN_KOSU_ON_KAYIT.md (getirisiz; kontrol tablosu ana metinde)
        python arastirma_cikti/cetvel2/c2_yeniden_kosu.py kos --c C194    kapı -> bir Ç'nin ölçümü -> parça (json + satır dosyası)
        python arastirma_cikti/cetvel2/c2_yeniden_kosu.py birlestir       bütün parçalar -> YENIDEN_KOSU.md + yeniden_kosu.json + yeniden üretim
CETVEL2.py, YAPI_HEDEF.py, DUSUS_SONRASI.py, ORTAK_CETVEL.py, POZITIF_KONTROL.py DEĞİŞTİRİLMEZ; içe alınır. Veri /tmp/veri (islenmis-veri).
Colab: exec(open(...).read()) (kod değiştiyse çalışma zamanını yeniden başlat). Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_YK = {k: id(v) for k, v in globals().items()}

import argparse  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)   # c2_olc satır çerçevesi çok sütunlu (yalnız uyarı)

KOK_YK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if KOK_YK not in sys.path:
    sys.path.insert(0, KOK_YK)

import CETVEL2 as C2  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

yklog = logging.getLogger("col.cetvel2.yeniden")
if not yklog.handlers:
    _h = logging.StreamHandler(); _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s yeniden_kosu: %(message)s", "%H:%M:%S"))
    yklog.addHandler(_h); yklog.setLevel(logging.INFO); yklog.propagate = False


class YKHata(RuntimeError):
    """Yeniden koşu kapısı / girdi hatası (koşu DURUR)."""


YK_SURUM = "CETVEL2 YENİDEN KOŞU v1.0 (2026-11-21): Ç194-Ç202 + hakem turları 4 / 6, CETVEL2 v2.1 (C2.c2_olc) ile; eşikler / olay kümeleri aynı"
YK_YOL = {"cikti": os.path.join(KOK_YK, "arastirma_cikti", "cetvel2"), "yh": os.path.join(KOK_YK, "arastirma_cikti", "yapi_hedef"),
          "ds": os.path.join(KOK_YK, "arastirma_cikti", "dusus_sonrasi"), "tur": os.path.join(KOK_YK, "arastirma_cikti", "goz_etiket", "tur"),
          "kod": os.path.abspath(__file__), "parca": os.environ.get("YK_PARCA", os.path.join(KOK_YK, "arastirma_cikti", "cetvel2", "yk_parca"))}
YK_DOSYA = {"onkayit": "YENIDEN_KOSU_ON_KAYIT.md", "rapor": "YENIDEN_KOSU.md", "json": "yeniden_kosu.json", "satir": "yk_{c}.csv.gz",
            "huni": "yk_huni.json"}
YK_UST20 = ("ust20", "ust10", "ust5")          # puan_Y1 dilim etiketleri: üst %20 = ust20 ∪ ust10 ∪ ust5 (yh_rapor7 / yh_yeniden_uret7 ile aynı)
YK_TUR = (4, 6)                                 # Cemal'in ve modelin etiketi açık turlar; 5 ve 7 Cemal etiketi yok -> AÇILMAZ (kör kural)

# ---------------------------------------------------------------- KAPSAM (ön kayıtta aynen; sonuç görülmeden)
# hip: (kod, bayrak, yön, eski kaynak). Eski kaynak: ('deneme', ad) | ('y1', ad) | ('karne', filtre, kol) | ('grup', ad) | ('puan', ad)
#      | ('devir', no, aday, kol) | ('ds', kod) | ('tur', ad) | ('taban', ad)
_D1 = [k for k in YH.YH_ESIK_D1["aday"]]
_D2 = [k for k, v in YH.YH_ESIK_D2["aday"].items() if v.get("tur") == "ana"]
_D3 = [k for k, v in YH.YH_ESIK_D3["aday"].items() if v.get("tur") == "ana"]
_KARNE_A = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "F14"]
_KARNE_B = ["S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "F14"]


def _yk_d1_yon(a: str) -> str:
    return "+" if YH.YH_ESIK_D1["aday"][a]["yon"] == "ana" else "-"


YK_C: List[Dict[str, Any]] = [
    {"c": "C194", "ad": "Ç194 S7 (Cemal'in 8 kuralı; YAPI_HEDEF 4. tur)", "kume": "Y1", "m": 3, "tohum0": 194,
     "hip": [("Y10", "F_Y10", "+", ("deneme", "Y10")), ("Y10b", "F_Y10b", "+", ("deneme", "Y10b")), ("Y10c", "F_Y10c", "+", ("deneme", "Y10c"))]},
    {"c": "C195", "ad": "Ç195 Ş9 U dip (YAPI_HEDEF 5. tur)", "kume": "Y1", "m": 3, "tohum0": 195,
     "hip": [("Y11", "F_Y11", "+", ("deneme", "Y11")), ("Y11b", "F_Y11b", "+", ("deneme", "Y11b")), ("Y11c", "F_Y11c", "+", ("deneme", "Y11c"))]},
    {"c": "C196", "ad": "Ç196 filtre karnesi (Ş1-Ş9, F14 tek süzgeç; kol A Y1, kol B Y9 dipte) + gruplar G1 / G2 / G2u", "kume": "Y1",
     "m": len(_KARNE_A) + len(_KARNE_B) + 3, "tohum0": 196,
     "hip": [(f"A_{f}", f"F_{f}", "+", ("karne", f, "A")) for f in _KARNE_A]
            + [(f"B_{f}", f"F_B_{f}", "+", ("karne", f, "B")) for f in _KARNE_B]
            + [("G1", "F_G1", "+", ("grup", "G1")), ("G2", "F_G2", "+", ("grup", "G2")), ("G2u", "F_G2u", "+", ("grup", "G2u"))]},
    {"c": "C197", "ad": "Ç197 PUAN (M2 birleşik; sızıntısız dilim: eğitim B, sınama A; yürüyen C)", "kume": "Y1", "m": 4, "tohum0": 197,
     "hip": [("P_AB_ust20", "F_P_AB_ust20", "+", ("puan", "AB_ust20")), ("P_C_ust20", "F_P_C_ust20", "+", ("puan", "C_ust20")),
             ("P_AB_alt20", "F_P_AB_alt20", "-", ("puan", "AB_alt20")), ("P_C_alt20", "F_P_C_alt20", "-", ("puan", "C_alt20"))]},
    {"c": "C198", "ad": "Ç198 DEVİR 1 (18 aday x kol A / B; ana +, ters -)", "kume": "Y1", "m": 2 * len(_D1), "tohum0": 198,
     "hip": [(f"D1_{a}_{k}", f"F_D1_{a}_{k}", _yk_d1_yon(a), ("devir", 1, a, k)) for a in _D1 for k in ("A", "B")]},
    {"c": "C199", "ad": "Ç199 DEVİR 2 (10 ana aday x kol A / B)", "kume": "Y1", "m": 2 * len(_D2), "tohum0": 199,
     "hip": [(f"D2_{a}_{k}", f"F_D2_{a}_{k}", "+", ("devir", 2, a, k)) for a in _D2 for k in ("A", "B")]},
    {"c": "C200", "ad": "Ç200 DEVİR 3 (4 ana aday x kol A / B)", "kume": "Y1", "m": 2 * len(_D3), "tohum0": 200,
     "hip": [(f"D3_{a}_{k}", f"F_D3_{a}_{k}", "+", ("devir", 3, a, k)) for a in _D3 for k in ("A", "B")]},
    {"c": "C201", "ad": "Ç201 Ş10 MACD pozitif uyumsuzluk (YAPI_HEDEF 8. tur)", "kume": "Y1", "m": 3, "tohum0": 201,
     "hip": [("Y13", "F_Y13", "+", ("deneme", "Y13")), ("Y13b", "F_Y13b", "+", ("deneme", "Y13b")), ("Y13c", "F_Y13c", "+", ("deneme", "Y13c"))]},
    {"c": "C202", "ad": "Ç202 DÜŞÜŞ SONRASI 25 hipotez (DS ANA olayları; F_DS* bayrakları)", "kume": "DS", "m": 25, "tohum0": 202,
     "hip": "DS"},
    {"c": "TABAN", "ad": "TABAN (bilgi): bütün Y1 (S6 AL) olayları", "kume": "Y1", "m": 1, "tohum0": 190,
     "hip": [("Y1", None, "+", ("taban", "Y1"))]},
    {"c": "TABAN_DS", "ad": "TABAN (bilgi): bütün DS ANA olayları (DS içi eş bilgisinin tabanı)", "kume": "DS", "m": 1, "tohum0": 191,
     "hip": [("DS_ANA", None, "+", ("taban", "DS_ANA"))]},
    {"c": "TUR", "ad": "HAKEM TURLARI 4 ve 6 (bilgi): model / Cemal OLUR ve OLMAZ sayfaları", "kume": "TUR", "m": 4, "tohum0": 189,
     "hip": [("T_MODEL_OLUR", "F_T_MODEL_OLUR", "+", ("tur", "model OLUR")), ("T_MODEL_OLMAZ", "F_T_MODEL_OLMAZ", "-", ("tur", "model OLMAZ")),
             ("T_CEMAL_OLUR", "F_T_CEMAL_OLUR", "+", ("tur", "Cemal OLUR")), ("T_CEMAL_OLMAZ", "F_T_CEMAL_OLMAZ", "-", ("tur", "Cemal OLMAZ"))]},
]
YK_KARAR_C = ["C194", "C195", "C196", "C197", "C198", "C199", "C200", "C201", "C202"]


def _yk_ds_hip() -> List[Tuple[str, str, str, Tuple[str, str]]]:
    import DUSUS_SONRASI as DS
    return [(k, f"F_{k}", DS.DS_HIP[k]["yon"], ("ds", k)) for k in DS.DS_HIP_SIRA]


def yk_c(c: str) -> Dict[str, Any]:
    for x in YK_C:
        if x["c"] == c:
            y = dict(x)
            if y["hip"] == "DS":
                y["hip"] = _yk_ds_hip()
            return y
    raise YKHata(f"bilinmeyen Ç: {c}")


# ---------------------------------------------------------------- yardımcılar
def _yk_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _yk_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _yk_yaz(yol: str, metin: str) -> None:
    """Yaz + e-posta / anahtar sızıntı taraması (K13)."""
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", metin) and "noreply@anthropic.com" not in metin:
        raise YKHata(f"{yol}: metinde e-posta biçimli dizi var -> yazılmadı")
    if re.search(r"(api[_-]?key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9]{16,}", metin, flags=re.I):
        raise YKHata(f"{yol}: metinde anahtar biçimli dizi var -> yazılmadı")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    tmp = yol + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(metin)
    os.replace(tmp, yol)


def _yk_json(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _yk_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_yk_json(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        v = float(o)
        return v if np.isfinite(v) else None
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, _dt.date)):
        return str(o)
    return o


def _yk_anahtar(df: pd.DataFrame) -> pd.MultiIndex:
    return pd.MultiIndex.from_arrays([df.pazar.astype(str), df.sembol.astype(str), pd.to_datetime(df.tarih).dt.normalize()])


def _yk_oku(yol: str, **kw) -> pd.DataFrame:
    if not os.path.exists(yol):
        raise YKHata(f"dosya yok: {yol}")
    try:
        return pd.read_csv(yol, dtype={"sembol": str}, **kw)
    except Exception as ex:
        raise YKHata(f"okunamadı: {yol}: {ex}") from ex


def _yk_hucre_adi(donem: Any) -> str:
    d = str(donem)
    return "egitim" if d in ("2016-22", "egitim") else ("sinama" if d in ("2023", "2024-26", "sinama") else "?")


# ---------------------------------------------------------------- 1) BAYRAKLAR (getirisiz; eşikler ilgili modülün maske fonksiyonlarıyla AYNEN)
def yk_girdi_dosyalari() -> Dict[str, str]:
    yh, ds, tur = YK_YOL["yh"], YK_YOL["ds"], YK_YOL["tur"]
    d = {"olay_Y1": os.path.join(yh, "olay_Y1.csv.gz"), "ozellik_Y1": YH.YH_YOL["ozellik"], "ozellik_Y1_s7": YH.YH_YOL["ozellik_s7"],
         "ozellik_Y1_s9": YH.YH_YOL["ozellik_s9"], "ozellik_Y1_s10": YH.YH_YOL["ozellik_s10"],
         "ozellik_Y1_d1": os.path.join(yh, "ozellik_Y1_d1.csv.gz"), "ozellik_Y1_d2": os.path.join(yh, "ozellik_Y1_d2.csv.gz"),
         "devir1_esik": os.path.join(yh, "devir1_esik.json"), "devir2_esik": os.path.join(yh, "devir2_esik.json"),
         "devir3_esik": os.path.join(yh, "devir3_esik.json"), "puan_Y1": os.path.join(yh, "puan_Y1.csv.gz"),
         "sonuc_json": os.path.join(yh, "sonuc.json"), "grup6_json": os.path.join(yh, "grup6.json"), "puan7_json": os.path.join(yh, "puan7.json"),
         "filtre_karne_json": os.path.join(yh, "filtre_karne.json"), "devir1_sonuc": os.path.join(yh, "devir1_sonuc.json"),
         "devir2_sonuc": os.path.join(yh, "devir2_sonuc.json"), "devir3_sonuc": os.path.join(yh, "devir3_sonuc.json"),
         "ds_olay": os.path.join(ds, "ds_olay.csv.gz"), "ds_sonuc": os.path.join(ds, "ds_sonuc.json"), "ds_esik": os.path.join(ds, "ds_esik.json")}
    for dn in ("Y9", "Y10", "Y10b", "Y10c", "Y11", "Y11b", "Y11c", "Y13", "Y13b", "Y13c"):
        d[f"olay_{dn}"] = os.path.join(yh, f"olay_{dn}.csv.gz")
    for t in YK_TUR:
        d[f"tur_{t}_satir"] = os.path.join(tur, str(t), f"tur_{t}_satir.csv")
    return d


def yk_y1_bayrak() -> pd.DataFrame:
    """olay_Y1 kimliği (pazar, sembol, tarih, donem) + bütün Y1 tabanlı bayraklar (F_*; 1 / 0). Getirisiz."""
    M = YH.yh_g6_taban()                                       # olay_Y1 ∩ F1-F29 + G0 / G1 / G2 / G2u (yh_grup6_maske)
    S = YH.yh_s9_sartlar(M)                                    # Ş1-Ş9, F14 (YH_ESIK eşikleri)
    out = M[["pazar", "sembol", "tarih", "donem"]].copy()
    kolB = S["S1"].copy()
    if not np.array_equal(kolB, M["G2"].to_numpy(bool)):
        raise YKHata("Ş1 ile G2 (kol B) aynı değil -> DURDU")
    for f in _KARNE_A:
        out[f"F_{f}"] = S[f].astype(int)
    for f in _KARNE_B:
        out[f"F_B_{f}"] = (kolB & S[f]).astype(int)
    for g in ("G1", "G2", "G2u"):
        out[f"F_{g}"] = M[g].to_numpy(bool).astype(int)
    for d in ("Y10", "Y10b", "Y10c"):
        out[f"F_{d}"] = YH.yh_y10_maske(M, d).astype(int)
    for d in ("Y11", "Y11b", "Y11c"):
        out[f"F_{d}"] = YH.yh_y11_maske(M, d).astype(int)
    # Ş10 (yh_s10_maske; kol B = Ş1)
    S10 = YH.yh_s10_oku()
    T = out[["pazar", "sembol", "tarih"]].merge(S10, on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one", indicator=True)
    if (T._merge != "both").any():
        raise YKHata(f"Ş10 özellik dosyası Y1 anahtarlarını kapsamıyor ({int((T._merge != 'both').sum())}) -> DURDU")
    T["kolB"] = kolB
    for d in ("Y13", "Y13b", "Y13c"):
        out[f"F_{d}"] = YH.yh_s10_maske(T, d).astype(int)
    # DEVİR 1-3 (yh_d*_maske; YÖN 1 eşikleri = eğitim 2016-22 çeyrekleri, mühürlü json'lardan AYNEN; sha denetimi modülün fonksiyonuyla)
    e1 = YH.yh_d2_eski_esik_oku(YK_YOL["yh"])                  # devir1_esik.json (esik_d1_sha == YH_ESIK_D1 değilse DURUR)
    e1_, e2 = YH._yh_d3_kaynak_esik(YK_YOL["yh"])               # + devir2_esik.json (esik_d2_sha denetimi)
    y3 = os.path.join(YK_YOL["yh"], "devir3_esik.json"); e3 = json.load(open(y3, encoding="utf-8"))
    if e3.get("esik_d3_sha") != YH.yh_esik_d3_sha():
        raise YKHata("devir3_esik.json esik_d3_sha YH_ESIK_D3 ile aynı değil -> DURDU")
    M1 = YH.yh_d1_taban(YK_YOL["yh"]); M3 = YH.yh_d3_taban(YK_YOL["yh"])
    k_out = _yk_anahtar(out)
    for no, Mx, adaylar, fn in ((1, M1, _D1, lambda M_, a: YH.yh_d1_maske(M_, a, e1, "yon1")),
                                (2, M3, _D2, lambda M_, a: YH.yh_d2_maske(M_, a, e2, e1, "yon1")),
                                (3, M3, _D3, lambda M_, a: YH.yh_d3_maske(M_, a, e3, "yon1"))):
        kx = _yk_anahtar(Mx); pos = kx.get_indexer(k_out)
        if (pos < 0).any() or len(kx) != len(k_out):
            raise YKHata(f"DEVİR {no} tabanı Y1 anahtarlarıyla eşleşmiyor -> DURDU")
        kB = Mx["kolB"].to_numpy(bool)[pos]
        if not np.array_equal(kB, kolB):
            raise YKHata(f"DEVİR {no} kol B, Ş1 ile aynı değil -> DURDU")
        for a in adaylar:
            m = fn(Mx, a)[pos]
            out[f"F_D{no}_{a}_A"] = m.astype(int); out[f"F_D{no}_{a}_B"] = (m & kolB).astype(int)
    # PUAN (puan_Y1.csv.gz; M2 birleşik dilimi; sızıntısız: 2016-22 -> B (2023-26'da öğrenilmiş), 2023-26 -> A (2016-22'de öğrenilmiş))
    P = _yk_oku(yk_girdi_dosyalari()["puan_Y1"], parse_dates=["tarih"])
    T = out[["pazar", "sembol", "tarih", "donem"]].merge(P[["pazar", "sembol", "tarih", "dilim_A", "dilim_B", "dilim_C"]],
                                                          on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one", indicator=True)
    if (T._merge != "both").any():
        raise YKHata("puan_Y1 Y1 anahtarlarını kapsamıyor -> DURDU")
    eg = (T.donem.astype(str) == "2016-22").to_numpy()
    dAB = np.where(eg, T.dilim_B.astype(object), T.dilim_A.astype(object))
    out["F_P_AB_ust20"] = pd.Series(dAB).isin(YK_UST20).astype(int).to_numpy()
    out["F_P_AB_alt20"] = (pd.Series(dAB) == "alt20").astype(int).to_numpy()
    out["F_P_C_ust20"] = T.dilim_C.isin(YK_UST20).astype(int).to_numpy()
    out["F_P_C_alt20"] = (T.dilim_C == "alt20").astype(int).to_numpy()
    return out.reset_index(drop=True)


def yk_ds_olay() -> pd.DataFrame:
    """DS ANA olayları + F_DS* bayrakları (ds_olay.csv.gz AYNEN; DUSUS_SONRASI koşusunun mühürlü eşikleriyle hesaplanmış)."""
    import DUSUS_SONRASI as DS
    kol = ["pazar", "sembol", "tarih", "donem"] + [f"F_{k}" for k in DS.DS_HIP_SIRA]
    X = _yk_oku(yk_girdi_dosyalari()["ds_olay"], usecols=kol, parse_dates=["tarih"])
    for k in DS.DS_HIP_SIRA:
        v = pd.to_numeric(X[f"F_{k}"], errors="coerce")
        if not set(np.unique(v[np.isfinite(v)])) <= {0.0, 1.0}:
            raise YKHata(f"ds_olay F_{k} 0 / 1 / NaN değil -> DURDU")
    return X


def yk_tur_olay() -> pd.DataFrame:
    """Hakem turları 4 ve 6 sayfaları (tur_<t>_satir.csv; iki etiket de açık). Tur 5 / 7 Cemal etiketi yok -> okunmaz."""
    par = []
    for t in YK_TUR:
        S = _yk_oku(yk_girdi_dosyalari()[f"tur_{t}_satir"], parse_dates=["tarih"])
        S["tur"] = t; par.append(S)
    S = pd.concat(par, ignore_index=True)
    out = S[["pazar", "sembol", "tarih", "donem", "tur", "sayfa"]].copy()
    out["F_T_MODEL_OLUR"] = (S.model.astype(str).str.upper() == "OLUR").astype(int)
    out["F_T_MODEL_OLMAZ"] = (S.model.astype(str).str.upper() == "OLMAZ").astype(int)
    out["F_T_CEMAL_OLUR"] = (S.cemal.astype(str).str.upper() == "OLUR").astype(int)
    out["F_T_CEMAL_OLMAZ"] = (S.cemal.astype(str).str.upper() == "OLMAZ").astype(int)
    d = out.duplicated(["pazar", "sembol", "tarih"]).sum()
    if d:
        yklog.warning("tur sayfalarında %d tekrar (pazar, sembol, tarih); ilki tutulur", d)
        out = out.drop_duplicates(["pazar", "sembol", "tarih"], keep="first")
    return out.reset_index(drop=True)


_YK_ONB: Dict[str, pd.DataFrame] = {}


def yk_olay(kume: str) -> pd.DataFrame:
    if kume not in _YK_ONB:
        _YK_ONB[kume] = {"Y1": yk_y1_bayrak, "DS": yk_ds_olay, "TUR": yk_tur_olay}[kume]()
    return _YK_ONB[kume]


def yk_regresyon(F: pd.DataFrame) -> Dict[str, Any]:
    """Bayrak kümeleri eski deneme satır dosyalarıyla (olay_Y9 / Y10* / Y11* / Y13*) birebir mi (anahtar kümesi eşitliği)."""
    G = yk_girdi_dosyalari(); out: Dict[str, Any] = {}
    kF = _yk_anahtar(F)
    for dn, col in (("Y9", "F_S1"), ("Y10", "F_Y10"), ("Y10b", "F_Y10b"), ("Y10c", "F_Y10c"), ("Y11", "F_Y11"), ("Y11b", "F_Y11b"),
                    ("Y11c", "F_Y11c"), ("Y13", "F_Y13"), ("Y13b", "F_Y13b"), ("Y13c", "F_Y13c")):
        O = _yk_oku(G[f"olay_{dn}"], usecols=["pazar", "sembol", "tarih"], parse_dates=["tarih"])
        a = set(kF[F[col].to_numpy() == 1]); b = set(_yk_anahtar(O))
        out[dn] = {"bayrak": len(a), "dosya": len(b), "esit": a == b, "yalniz_bayrak": len(a - b), "yalniz_dosya": len(b - a)}
    return out


def yk_huni(F: pd.DataFrame, bayraklar: List[str]) -> Dict[str, Dict[str, int]]:
    """Getirisiz sayım: bayrak x pazar x hücre (sinyal günü dönemi; ölçülen n c2_olc'de giriş günü + tekil + 15 bar + eş ile küçülür)."""
    h = F.donem.map(_yk_hucre_adi) if "donem" in F.columns else pd.Series("?", index=F.index)
    out: Dict[str, Dict[str, int]] = {}
    for b in bayraklar:
        m = np.ones(len(F), bool) if b is None else (pd.to_numeric(F[b], errors="coerce").to_numpy() == 1)
        out[b or "hepsi"] = {f"{p}|{c}": int((m & (F.pazar == p).to_numpy() & (h == c).to_numpy()).sum())
                             for p in C2.C2_PAZAR for c in C2.C2_HUCRE}
    return out


# ---------------------------------------------------------------- 2) ESKİ SONUÇLAR (h5 cetveli; rapor / satır dosyalarından)
def _yk_eski_fark_satir(X: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Eski satır dosyası (h5, es_h5, olc, donem) -> pazar x hücre: n, FARK = ort(h5 - es_h5) (eski h5 cetveli aynen)."""
    X = X.copy()
    if "olc" in X.columns:
        X = X[X.olc.astype(str).str.lower().isin(["true", "1", "1.0"])]
    X = X[np.isfinite(pd.to_numeric(X.h5, errors="coerce")) & np.isfinite(pd.to_numeric(X.es_h5, errors="coerce"))]
    X["hc"] = X.donem.map(_yk_hucre_adi); out: Dict[str, Dict[str, Any]] = {}
    for p in C2.C2_PAZAR:
        for c in C2.C2_HUCRE:
            g = X[(X.pazar == p) & (X.hc == c)]
            out[f"{p}|{c}"] = {"n": int(len(g)), "fark": float((g.h5 - g.es_h5).mean()) if len(g) else None}
    return out


def yk_eski(cd: Dict[str, Any], F: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Her hipotez: {'etiket': eski etiket, 'kaynak': ..., 'hucre': {pazar|hücre: {n, fark}}}."""
    G = yk_girdi_dosyalari(); out: Dict[str, Dict[str, Any]] = {}
    son = json.load(open(G["sonuc_json"], encoding="utf-8"))["deneme"]
    Y1 = None
    for kod, bayrak, yon, kay in cd["hip"]:
        t = kay[0]; r: Dict[str, Any] = {"kaynak": "", "etiket": "-", "hucre": {}}
        if t == "deneme":
            r["etiket"] = son[kay[1]]["etiket"]; r["kaynak"] = f"sonuc.json deneme {kay[1]}; FARK olay_{kay[1]}.csv.gz (h5 - es_h5)"
            r["hucre"] = _yk_eski_fark_satir(_yk_oku(G[f"olay_{kay[1]}"], usecols=["pazar", "donem", "olc", "h5", "es_h5"]))
        elif t in ("y1", "karne", "grup", "puan", "taban") and cd["kume"] == "Y1":
            if Y1 is None:
                Y1 = _yk_oku(G["olay_Y1"], usecols=["pazar", "sembol", "tarih", "donem", "olc", "h5", "es_h5"], parse_dates=["tarih"])
                pos = _yk_anahtar(F).get_indexer(_yk_anahtar(Y1))
                if (pos < 0).any():
                    raise YKHata("olay_Y1 satırı bayrak çerçevesinde yok -> DURDU")
            m = np.ones(len(Y1), bool) if bayrak is None else (F[bayrak].to_numpy()[pos] == 1)
            r["hucre"] = _yk_eski_fark_satir(Y1[m])
            r["kaynak"] = "FARK olay_Y1.csv.gz (h5 - es_h5; bayraklı satırlar)"
            if t == "karne":
                K = json.load(open(G["filtre_karne_json"], encoding="utf-8"))["tablo"]
                if kay[2] == "A":
                    x = [q for q in K if q["kol"] == "S7" and q["filtre"] == kay[1] and q["pazar"] == "ABD+AVR"]
                    if not x:
                        x = [q for q in K if q["kol"] == "U" and q["filtre"] == kay[1] and q["pazar"] == "ABD+AVR"]
                    r["etiket"] = (f"{x[0]['etiket']} (karne huni adımı {x[0]['adim']}, kol {x[0]['kol']})" if x else "-")
                else:
                    r["etiket"] = "- (eski testte kol B tek süzgeç yok)"
            elif t == "grup":
                r["etiket"] = json.load(open(G["grup6_json"], encoding="utf-8"))["grup"][kay[1]]["etiket"]
            elif t == "puan":
                r["etiket"] = (json.load(open(G["puan7_json"], encoding="utf-8"))["etiket"]["birlesik|M2"]["etiket"] if kay[1].endswith("ust20")
                               else "- (alt %20 eski raporda bilgi)")
            elif t == "taban":
                r["etiket"] = son["Y1"]["etiket"]
        elif t == "devir":
            no, aday, kol = kay[1], kay[2], kay[3]
            K = json.load(open(G[f"devir{no}_sonuc"], encoding="utf-8"))["karne"]
            x = {q["pazar"]: q for q in K if q["aday"] == aday and q["kol"] == kol}
            if "ABD+AVR" in x:
                e = x["ABD+AVR"].get("etiket", "-"); kr = x["ABD+AVR"].get("karar")
                r["etiket"] = e + (f" / {kr}" if kr and kr != "-" else "")
            for p in C2.C2_PAZAR:
                for c in C2.C2_HUCRE:
                    q = x.get(p, {}).get(c, {})
                    r["hucre"][f"{p}|{c}"] = {"n": q.get("n"), "fark": q.get("fark")}
            r["kaynak"] = f"devir{no}_sonuc.json karne (pazar satırı egitim / sinama fark; DEVİR 2-3 sınaması 60 bar ambargolu)"
        elif t == "ds":
            K = {q["kod"]: q for q in json.load(open(G["ds_sonuc"], encoding="utf-8"))["karne"]}
            q = K[kay[1]]; r["etiket"] = q["etiket"]
            for p in C2.C2_PAZAR:
                for c in C2.C2_HUCRE:
                    h = q["hucre"].get(p, {}).get(c, {})
                    r["hucre"][f"{p}|{c}"] = {"n": h.get("n"), "fark": h.get("fark")}
            r["kaynak"] = "ds_sonuc.json karne (DS içi eş; h5 FARK)"
        elif t == "taban" and cd["kume"] == "DS":
            r["kaynak"] = "ds_sonuc.json (DS kümesi vs dış eş: kume bölümü)"; r["etiket"] = "- (bilgi)"
        elif t == "tur":
            S = pd.concat([_yk_oku(G[f"tur_{x}_satir"], usecols=["pazar", "donem", "olc", "h5", "es_h5", "model", "cemal"]) for x in YK_TUR])
            k1, k2 = kay[1].split(" ")
            m = (S["model" if k1 == "model" else "cemal"].astype(str).str.upper() == k2).to_numpy()
            r["hucre"] = _yk_eski_fark_satir(S[m]); r["kaynak"] = "tur_4 / tur_6 satir.csv (h5 - es_h5)"; r["etiket"] = "- (hakem turu bilgi)"
        out[kod] = r
    return out


# ---------------------------------------------------------------- 3) KAPI (ön kayıt, sha, git, kontrol listesi)
def yk_sha_simdi() -> Dict[str, str]:
    """Ön kayda yazılan / koşuda denetlenen sha'lar: CETVEL2 (kod, eşik, v2.1 json / ön kayıt), modüller, girdiler, bu kod."""
    out = dict(C2.c2_sha_simdi())
    c2c = C2.C2_YOL["cikti"]
    out["C2_ONKAYIT_V21_SHA"] = _yk_sha(os.path.join(c2c, "CETVEL2_ON_KAYIT_v2.1.md"))
    out["YK_KOD_SHA"] = _yk_sha(YK_YOL["kod"])
    for k, y in sorted(yk_girdi_dosyalari().items()):
        out[f"G_{k.upper()}_SHA"] = _yk_sha(y) if os.path.exists(y) else "-"
    out["YH_ESIK_D1_SHA"] = YH.yh_esik_d1_sha(); out["YH_ESIK_D2_SHA"] = YH.yh_esik_d2_sha(); out["YH_ESIK_D3_SHA"] = YH.yh_esik_d3_sha()
    out["YH_ESIK6_SHA"] = YH.yh_esik6_sha(); out["YH_ESIK8_SHA"] = YH.yh_esik8_sha()
    return out


def yk_kapi(git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    """(1) CETVEL2 v2.1 kapısı (C2.c2_kapi: ön kayıt v2.1 sha'ları + git + kontrol); (2) YENIDEN_KOSU_ON_KAYIT.md'deki her sha şimdiki ile aynı;
    (3) ön kayıt + bu kod git'te işlenmiş ve değişmemiş; (4) IZ_KARNE.ik_kontrol_kapisi. Biri tutmazsa DURUR."""
    c2k = C2.c2_kapi(git=git, kontrol=kontrol)
    yol = os.path.join(YK_YOL["cikti"], YK_DOSYA["onkayit"])
    if not os.path.exists(yol):
        raise YKHata(f"ön kayıt yok: {yol} (python c2_yeniden_kosu.py onkayit)")
    metin = open(yol, encoding="utf-8").read(); simdi = yk_sha_simdi()
    for k, v in simdi.items():
        m = re.search(rf"(?<![A-Z0-9_]){re.escape(k)}:\s*`([0-9a-f]{{64}}|-)`", metin)
        if not m or m.group(1) != v:
            raise YKHata(f"{k} ön kayıttakiyle aynı değil (ön kayıt {m.group(1) if m else 'yok'}, şimdi {v}) -> koşu DURDU")
    out: Dict[str, Any] = {"sha": simdi, "c2_kapi": {"git_onkayit": c2k.get("git_onkayit")}}
    if git:
        try:
            st = subprocess.run(["git", "status", "--porcelain", yol, YK_YOL["kod"]], cwd=KOK_YK, capture_output=True, text=True, check=True).stdout.strip()
            lg = subprocess.run(["git", "log", "-1", "--format=%H %cI", "--", yol], cwd=KOK_YK, capture_output=True, text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as ex:
            raise YKHata(f"git denetimi yapılamadı: {ex}") from ex
        if st or not lg:
            raise YKHata(f"ön kayıt / kod git'e işlenmemiş ya da değişmiş ({st or 'kayıt yok'}) -> koşu DURDU")
        out["git_onkayit"] = lg
    if kontrol:
        import IZ_KARNE as IK
        out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
    yklog.info("yk_kapi AÇIK")
    return out


# ---------------------------------------------------------------- 4) ÖLÇÜM (bir Ç)
_YK_SATIR_SUTUN = ["pazar", "sembol", "tarih", "giris", "donem", "kova", "atrp", "f15", "lq3", "E0", "r15", "h5", "st5", "h5_atr", "st5_atr",
                   "r60", "esli_r60"]


def yk_kos_c(c: str, git: bool = True, kontrol: bool = True, parca: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time(); kp = yk_kapi(git=git, kontrol=kontrol); cd = yk_c(c)
    F = yk_olay(cd["kume"])
    hip = {k: {"bayrak": b, "yon": y} for k, b, y, _ in cd["hip"]}
    bay = [b for _, b, _, _ in cd["hip"] if b is not None]
    O = F[["pazar", "sembol", "tarih"] + bay].copy()
    yklog.info("%s: %d olay, %d hipotez, m %d -> c2_olc", c, len(O), len(hip), cd["m"])
    R = C2.c2_olc(O, hip, m_bh=int(cd["m"]), tohum0=int(cd["tohum0"]))
    S = R["satir"]
    ek = [x for x in S.columns if x.startswith(("es_r15_", "n_es_", "sira_", "fark_"))]
    sat = S[[x for x in _YK_SATIR_SUTUN if x in S.columns] + bay + ek].copy()
    pdir = parca or YK_YOL["parca"]; os.makedirs(pdir, exist_ok=True)
    sy = os.path.join(YK_YOL["cikti"], YK_DOSYA["satir"].format(c=c))
    sat.to_csv(sy, index=False, compression="gzip")
    eski = yk_eski(cd, F)
    J = {"c": c, "ad": cd["ad"], "m": cd["m"], "tohum0": cd["tohum0"], "zaman_utc": _yk_simdi(), "sure_sn": round(time.time() - t0, 1),
         "kapi": {"git_onkayit": kp.get("git_onkayit"), "c2_git_onkayit": kp["c2_kapi"].get("git_onkayit"), "kontrol": kp.get("kontrol")},
         "hip": [{"kod": k, "bayrak": b, "yon": y, "eski_kaynak": list(e)} for k, b, y, e in cd["hip"]],
         "say": R["say"], "hucre": R["hucre"].to_dict("records"), "etiket": R["etiket"].to_dict("records"), "eski": eski,
         "satir_dosya": os.path.relpath(sy, KOK_YK), "satir_sha": _yk_sha(sy)}
    _yk_yaz(os.path.join(pdir, f"{c}.json"), json.dumps(_yk_json(J), ensure_ascii=False, indent=1))
    yklog.info("%s bitti (%.0f sn)", c, time.time() - t0)
    return J


# ---------------------------------------------------------------- 5) BİRLEŞTİRME, EK BİLGİLER, YENİDEN ÜRETİM, RAPOR
def _yk_norm(e: Any) -> str:
    s = str(e or "-").strip()
    s = re.sub(r"^BİLGİ \((.*)\)$", r"\1", s)
    s = re.sub(r"\s*\(.*$", "", s).strip()           # 'SORGULA (BH)', '... (karne huni adımı ...)', 'ÖLÇÜLEMEDİ (tek hücre ...)'
    s = s.split(" / ")[0].strip()
    return s or "-"


def _yk_boot_fark(a: pd.DataFrame, b: pd.DataFrame, B: int = 2000, tohum: int = 2161) -> Tuple[float, float, float]:
    """İki grup ort FARK farkı (a - b) + ay kümeli bootstrap %95 (giriş ayı; aylar birlikte yeniden örneklenir). Bilgi."""
    if not len(a) or not len(b):
        return float("nan"), float("nan"), float("nan")
    a = a.assign(ay=pd.to_datetime(a.giris).dt.strftime("%Y-%m")); b = b.assign(ay=pd.to_datetime(b.giris).dt.strftime("%Y-%m"))
    aylar = np.array(sorted(set(a.ay) | set(b.ay)))
    sa = a.groupby("ay").f.agg(["sum", "count"]).reindex(aylar).fillna(0).to_numpy()
    sb = b.groupby("ay").f.agg(["sum", "count"]).reindex(aylar).fillna(0).to_numpy()
    rng = np.random.default_rng(tohum); d = []
    for _ in range(B):
        ix = rng.integers(0, len(aylar), len(aylar)); xa = sa[ix].sum(0); xb = sb[ix].sum(0)
        if xa[1] > 0 and xb[1] > 0:
            d.append(xa[0] / xa[1] - xb[0] / xb[1])
    est = float(a.f.mean() - b.f.mean())
    return est, float(np.quantile(d, 0.025)) if d else float("nan"), float(np.quantile(d, 0.975)) if d else float("nan")


def yk_ek_bilgi(P: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """(a) Ç196 G2 - G1 ve G2 - G1 R15 FARK farkı (ay kümeli boot; bilgi); (b) Ç202 DS içi: TABAN_DS satırlarının FARK'ı ile bayrak 1 - bayrak 0."""
    out: Dict[str, Any] = {"g2_g1": [], "ds_ici": []}
    if "C196" in P:
        S = pd.read_csv(os.path.join(KOK_YK, P["C196"]["satir_dosya"]), parse_dates=["giris"])
        for p in C2.C2_PAZAR:
            for c in C2.C2_HUCRE:
                g = S[(S.pazar == p) & (S.donem == c)]
                a = g[g.F_G2 == 1].assign(f=g.fark_G2).dropna(subset=["f"]); b = g[g.F_G1 == 1].assign(f=g.fark_G1).dropna(subset=["f"])
                e, lo, hi = _yk_boot_fark(a, b)
                out["g2_g1"].append({"pazar": p, "hucre": c, "n_G2": int(len(a)), "n_G1": int(len(b)), "fark": e, "boot_alt": lo, "boot_ust": hi})
    if "TABAN_DS" in P and "C202" in P:
        S = pd.read_csv(os.path.join(KOK_YK, P["TABAN_DS"]["satir_dosya"]), parse_dates=["giris", "tarih"], dtype={"sembol": str})
        Fds = yk_olay("DS")
        T = S.merge(Fds.drop(columns=["donem"]), on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one", suffixes=("", "_ds"))
        for k, b, y, _ in yk_c("C202")["hip"]:
            for p in C2.C2_PAZAR:
                for c in C2.C2_HUCRE:
                    g = T[(T.pazar == p) & (T.donem == c)].assign(f=lambda z: z.fark_DS_ANA).dropna(subset=["f"])
                    v = pd.to_numeric(g[b], errors="coerce")
                    e, lo, hi = _yk_boot_fark(g[v == 1], g[v == 0])
                    out["ds_ici"].append({"kod": k, "yon": y, "pazar": p, "hucre": c, "n1": int((v == 1).sum()), "n0": int((v == 0).sum()),
                                          "fark": e, "boot_alt": lo, "boot_ust": hi})
    return out


def yk_yeniden_uretim(P: Dict[str, Dict[str, Any]], veri: Optional[str] = None, tohum: int = 2171) -> Dict[str, Any]:
    """BAĞIMSIZ YENİDEN ÜRETİM (düz pandas / düz döngü): (1) >= 3 hücre: satır dosyasından n / ort FARK / ort SIRA / medyan FARK;
    (2) 30 olayın R15'i ham V_*.pkl'den düz döngüyle; (3) 2 olayın eş ortalaması bütün evrende düz döngüyle (kova elle)."""
    import pickle
    v = veri or C2.C2_YOL["veri"]; out: Dict[str, Any] = {"hucre": [], "r15": [], "es": []}
    sec = [("C194", "Y10c", "ABD", "sinama"), ("C196", "A_S1", "AVR", "egitim"), ("C202", "DS06", "ABD", "sinama"), ("C199", "D2_NR7_A", "ABD", "egitim")]
    for c, kod, p, hc in sec:
        if c not in P:
            continue
        S = pd.read_csv(os.path.join(KOK_YK, P[c]["satir_dosya"]))
        g = S[(S.pazar == p) & (S.donem == hc)]
        f = pd.to_numeric(g[f"fark_{kod}"], errors="coerce").dropna(); sr = pd.to_numeric(g.loc[f.index, f"sira_{kod}"], errors="coerce")
        q = [h for h in P[c]["hucre"] if h["kod"] == kod and h["pazar"] == p and h["hucre"] == hc][0]
        out["hucre"].append({"c": c, "kod": kod, "pazar": p, "hucre": hc, "n_duz": int(len(f)), "fark_duz": float(f.mean()), "sira_duz": float(sr.mean()),
                             "med_duz": float(f.median()), "n": q["n"], "fark": q["fark"], "sira": q["sira"], "med": q["med"],
                             "esit": bool(len(f) == int(q["n"]) and abs(f.mean() - q["fark"]) < 1e-9 and abs(sr.mean() - q["sira"]) < 1e-9
                                          and abs(f.median() - q["med"]) < 1e-9)})
    # (2) R15 ham veriden: C194 satırlarından 30 olay (pazar karışık)
    S = pd.read_csv(os.path.join(KOK_YK, P["C194"]["satir_dosya"]), parse_dates=["giris"]) if "C194" in P else None
    rng = np.random.default_rng(tohum)
    if S is not None:
        g = S[np.isfinite(S.r15)].reset_index(drop=True)
        Vc: Dict[str, Any] = {}
        for i in rng.choice(len(g), size=min(30, len(g)), replace=False):
            r = g.iloc[int(i)]
            if r.pazar not in Vc:
                Vc[r.pazar] = pickle.load(open(os.path.join(v, f"V_{r.pazar}.pkl"), "rb"))
            df = Vc[r.pazar][r.sembol]
            df = df[(df.High > df.Low) & (df.Volume > 0) & (df.Open > 0) & (df.Close > 0) & (df.Low > 0)].copy()
            df["Open"] = df.Open.clip(lower=df.Low, upper=df.High)          # DS açılış kırpması (O, [L, H] dışındaysa)
            ix = list(df.index); k = ix.index(pd.Timestamp(r.giris)) if pd.Timestamp(r.giris) in ix else -1
            duz = float(df.Close.iloc[k + 14] / df.Open.iloc[k] - 1) if k >= 0 and k + 14 < len(ix) else float("nan")
            out["r15"].append({"pazar": r.pazar, "sembol": r.sembol, "giris": str(r.giris.date()), "kod": float(r.r15), "duz": duz,
                               "esit": bool(np.isclose(duz, r.r15, rtol=1e-6, atol=1e-9))})
    # (3) eş ortalaması düz döngü: C194 Y10c ABD satırlarından 2 olay; kova panelden (Pn['KV']) okunur, R15 panelden; eş kümesi elle
    if S is not None:
        Pn = C2.c2_panel_al("ABD", v); P_ = Pn["P"]; idx = P_["tarih"]
        g = S[(S.pazar == "ABD") & np.isfinite(S["fark_Y10c"])].reset_index(drop=True)
        ayni = S[(S.pazar == "ABD") & (S.F_Y10c == 1)]
        for i in rng.choice(len(g), size=min(2, len(g)), replace=False):
            r = g.iloc[int(i)]; d = idx.get_loc(pd.Timestamp(r.giris)); j0 = P_["kol"][r.sembol]
            dis = set(ayni[pd.to_datetime(ayni.giris) == r.giris].sembol) | {r.sembol}
            vals = []
            for s, j in P_["kol"].items():
                if s in dis:
                    continue
                if not (P_["ok"][d, j] and P_["H"][d, j] >= 0):
                    continue
                if Pn["KV"][d, j] != Pn["KV"][d, j0] or not np.isfinite(Pn["R15"][d, j]):
                    continue
                vals.append(float(Pn["R15"][d, j]))
            es = float(np.mean(vals)) if len(vals) >= int(C2.C2_ESIK["es_min"]) else float("nan")
            out["es"].append({"sembol": r.sembol, "giris": str(r.giris.date()), "n_duz": len(vals), "n_kod": int(r["n_es_Y10c"]), "es_duz": es,
                              "es_kod": float(r["es_r15_Y10c"]), "esit": bool(len(vals) == int(r["n_es_Y10c"]) and np.isclose(es, r["es_r15_Y10c"], rtol=1e-9))})
    out["tuttu"] = bool(len(out["hucre"]) >= 3 and all(h["esit"] for h in out["hucre"]) and all(x["esit"] for x in out["r15"])
                        and all(x["esit"] for x in out["es"]))
    return out


def _yy(x: Any, n: int = 1, isaret: bool = True) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    return (f"{100 * v:+.{n}f}" if isaret else f"{100 * v:.{n}f}").replace(".", ",")


def _ys(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(v) else f"{v:.{n}f}".replace(".", ",")


def yk_birlestir(parca: Optional[str] = None, veri: Optional[str] = None) -> Dict[str, Any]:
    pdir = parca or YK_YOL["parca"]; P: Dict[str, Dict[str, Any]] = {}
    eksik = []
    for x in YK_C:
        y = os.path.join(pdir, f"{x['c']}.json")
        if not os.path.exists(y):
            eksik.append(x["c"]); continue
        P[x["c"]] = json.load(open(y, encoding="utf-8"))
    if eksik:
        raise YKHata(f"parça eksik: {eksik} -> yarım sonuç YAZILMAZ")
    satir, et_ozet = [], []
    for c, J in P.items():
        et = {e["kod"]: e for e in J["etiket"]}
        for h in J["hip"]:
            k = h["kod"]; e = et[k]; es = J["eski"][k]
            eski_n = _yk_norm(es["etiket"]); yeni_n = _yk_norm(e["etiket"])
            degisti = (eski_n != yeni_n) if eski_n not in ("-",) else None
            et_ozet.append({"c": c, "kod": k, "yon": h["yon"], "eski": es["etiket"], "yeni": e["etiket"], "yeni_ham": e["etiket_ham"],
                            "neden": e["neden"], "p_bh": e["p_bh"], "bh": e["bh_gecti"], "eski_n": eski_n, "yeni_n": yeni_n, "degisti": degisti})
            for r in [q for q in J["hucre"] if q["kod"] == k]:
                o = es["hucre"].get(f"{r['pazar']}|{r['hucre']}", {})
                of, nf = o.get("fark"), r.get("fark")
                isa = (None if of is None or nf is None or not np.isfinite(float(of)) or not np.isfinite(float(nf))
                       else bool(np.sign(float(of)) != np.sign(float(nf))))
                satir.append({"c": c, "kod": k, "yon": h["yon"], "pazar": r["pazar"], "hucre": r["hucre"], "n": r["n"], "n_bayrak": r["n_bayrak"],
                              "n_essiz": r["n_essiz"], "eski_n": o.get("n"), "eski_fark": of, "eski_etiket": es["etiket"], "fark": nf, "med": r["med"],
                              "boot_alt": r["boot_alt"], "boot_ust": r["boot_ust"], "sira": r["sira"], "l3o": r["l3o"], "l3o_neg": r.get("l3o_neg"),
                              "p": r["p"], "guc": r["guc"], "plasebo_fark": r.get("plasebo_fark"), "plasebo_tutar_pay": r.get("plasebo_tutar_pay"),
                              "plasebo_gecti": r.get("plasebo_gecti"), "tutar": r["tutar"], "ters": r["ters"], "durum": r["durum"],
                              "h5": r.get("h5"), "h5_atr": r.get("h5_atr"), "r60_fark": r.get("r60_fark"), "r15_med": r.get("r15_med"),
                              "yeni_etiket": e["etiket"], "isaret_degisti": isa, "etiket_degisti": degisti})
    Sa = pd.DataFrame(satir); Eo = pd.DataFrame(et_ozet)
    gecis = Eo[Eo.c.isin(YK_KARAR_C)].groupby(["eski_n", "yeni_n"]).size().reset_index(name="sayi").to_dict("records")
    secili = Eo[Eo.yeni_n.isin(["KATKI+", "KATKI−", "ÇELİŞKİLİ"]) | Eo.yeni_ham.astype(str).str.startswith(("KATKI", "ÇELİŞKİLİ"))]
    k30 = Sa[(Sa.n >= 30)].copy()
    buyuk = k30.reindex(k30.fark.astype(float).sort_values(ascending=False).index).head(10)
    ek = yk_ek_bilgi(P); yu = yk_yeniden_uretim(P, veri)
    J = {"surum": YK_SURUM, "c2_surum": C2.C2_SURUM, "zaman_utc": _yk_simdi(), "parca": {c: {k: P[c][k] for k in ("zaman_utc", "sure_sn", "kapi",
         "satir_dosya", "satir_sha", "m", "tohum0", "say")} for c in P}, "satir": Sa.to_dict("records"), "etiket": Eo.to_dict("records"),
         "gecis": gecis, "secili": secili.to_dict("records"), "en_buyuk10": buyuk.to_dict("records"), "ek": ek, "yeniden_uretim": yu}
    _yk_yaz(os.path.join(YK_YOL["cikti"], YK_DOSYA["json"]), json.dumps(_yk_json(J), ensure_ascii=False, indent=1))
    md = yk_rapor_md(J, P)
    _yk_yaz(os.path.join(YK_YOL["cikti"], YK_DOSYA["rapor"]), md)
    return J


def yk_rapor_md(J: Dict[str, Any], P: Dict[str, Dict[str, Any]]) -> str:
    Sa = pd.DataFrame(J["satir"]); Eo = pd.DataFrame(J["etiket"])
    s = [f"# CETVEL2 YENİDEN KOŞU (ADIM H) — {J['zaman_utc']}", "",
         f"{J['surum']}. Cetvel: {J['c2_surum']} (C2.c2_olc; ön kayıt CETVEL2_ON_KAYIT_v2.1.md). Ön kayıt YENIDEN_KOSU_ON_KAYIT.md "
         f"(git {next(iter(J['parca'].values()))['kapi'].get('git_onkayit')}). Koşu parçaları: "
         + ", ".join(f"{c} {v['zaman_utc'][11:19]} ({v['sure_sn']:.0f} sn)" for c, v in J["parca"].items()) + ".",
         "",
         "Okuma: ESKİ = h5 cetveli (15 barda +%5 stop = dip x 0,98'den önce; eş = aynı gün aynı kova; rapordaki etiket ve h5 FARK, puan). YENİ = "
         "CETVEL2: R15 = 15. geçerli bar kapanışı / giriş açılışı − 1 (stop yok); FARK = R15 − konum eşli eş ortalaması (aynı gün, aynı ATRP x "
         "likidite x F15 kovası, bütün evren, en az 5 eş); SIRA = eş dağılımındaki yüzdelik; boot = ay kümeli %95; plasebo kapısı 200 tohum. "
         "Değerler yüzde puan. Hücreler: eğitim 2016-22, sınama 2023-01..2026-08 (giriş günü). Karar hücreleri ABD ve AVR; BIST bilgi. "
         "Evren bugün işlem gören hisseler (hayatta kalma: olay ve eş ikisi de yukarı yanlı). Komisyon yok. 'İz' iddiası yok.", ""]
    # özet
    K = Eo[Eo.c.isin(YK_KARAR_C)]
    s += ["## 1. ÖZET", "", f"- Hipotez sayısı (Ç194-Ç202): {len(K)}; eski etiketi olan {int((K.eski_n != '-').sum())}; "
          f"etiketi DEĞİŞEN {int((K.degisti == True).sum())}, aynı kalan {int((K.degisti == False).sum())}, eski etiket yok {int(K.degisti.isna().sum())}.",  # noqa: E712
          "- Etiket geçişleri (eski -> yeni; normalleştirilmiş: 'BİLGİ (X)' = X, 'SORGULA (BH)' = SORGULA):", "",
          "| eski | yeni | sayı |", "|---|---|---|"]
    for g in J["gecis"]:
        s.append(f"| {g['eski_n']} | {g['yeni_n']} | {g['sayi']} |")
    s += ["", "- Yeni etiket dağılımı (Ç başına):", "", "| Ç | hipotez | eski etiket dağılımı | yeni etiket dağılımı | değişen |", "|---|---|---|---|---|"]
    for c in J["parca"]:
        e = Eo[Eo.c == c]
        s.append(f"| {c} | {len(e)} | " + ", ".join(f"{k} {v}" for k, v in e.eski_n.value_counts().items()) + " | "
                 + ", ".join(f"{k} {v}" for k, v in e.yeni.value_counts().items()) + f" | {int((e.degisti == True).sum())} |")  # noqa: E712
    s += ["", "### CETVEL2 ile KATKI+ / KATKI− / ÇELİŞKİLİ çıkanlar (BH öncesi ham etiket dahil)", ""]
    if not len(J["secili"]):
        s.append("- YOK: hiçbir hipotez CETVEL2'de KATKI+ / KATKI− / ÇELİŞKİLİ çıkmadı.")
    else:
        s += ["| Ç | kod | yön | ham etiket | BH | etiket | gerekçe | hücreler (pazar hücre: n, FARK [boot], SIRA, kapı) |", "|---|---|---|---|---|---|---|---|"]
        for e in J["secili"]:
            hs = Sa[(Sa.c == e["c"]) & (Sa.kod == e["kod"])]
            hm = "; ".join(f"{r.pazar} {r.hucre}: n {r.n}, {_yy(r.fark, 2)} [{_yy(r.boot_alt, 2)}, {_yy(r.boot_ust, 2)}], {_ys(r.sira, 3)}, "
                           f"{'geçti' if r.plasebo_gecti else 'DÜŞTÜ'}" for r in hs.itertuples())
            s.append(f"| {e['c']} | {e['kod']} | {e['yon']} | {e['yeni_ham']} | {'geçti' if e['bh'] else '-'} (p {_ys(e['p_bh'], 4)}) | {e['yeni']} | "
                     f"{e['neden']} | {hm} |")
    s += ["", "### En büyük 10 R15 FARK (n >= 30 hücreler; bütün pazarlar)", "",
          "| Ç | kod | pazar | hücre | n | R15 FARK [boot] | SIRA | p | güç | plasebo | durum | eski h5 FARK | yeni etiket |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in J["en_buyuk10"]:
        s.append(f"| {r['c']} | {r['kod']} | {r['pazar']} | {r['hucre']} | {r['n']} | {_yy(r['fark'], 2)} [{_yy(r['boot_alt'], 2)}, {_yy(r['boot_ust'], 2)}] | "
                 f"{_ys(r['sira'], 3)} | {_ys(r['p'], 4)} | {_ys(r['guc'], 2)} | {'geçti' if r['plasebo_gecti'] else 'DÜŞTÜ'} | {r['durum']} | "
                 f"{_yy(r['eski_fark'], 1)} | {r['yeni_etiket']} |")
    # ek bilgiler
    s += ["", "## 2. EK BİLGİ", "", "### Ç196 dip grubu (G2) − trend içi raf (G1): R15 FARK farkı (ay kümeli boot %95; bilgi)", "",
          "| pazar | hücre | n G2 | n G1 | G2 − G1 [boot] |", "|---|---|---|---|---|"]
    for r in J["ek"]["g2_g1"]:
        s.append(f"| {r['pazar']} | {r['hucre']} | {r['n_G2']} | {r['n_G1']} | {_yy(r['fark'], 2)} [{_yy(r['boot_alt'], 2)}, {_yy(r['boot_ust'], 2)}] |")
    s += ["", "### Ç202 DS içi eş (bilgi): TABAN_DS konum eşli FARK'ı ile bayrak 1 − bayrak 0 (aynı DS ANA kümesi içinde; ay kümeli boot)", "",
          "| kod | yön | pazar | hücre | n1 / n0 | fark [boot] |", "|---|---|---|---|---|---|"]
    for r in J["ek"]["ds_ici"]:
        if r["pazar"] == "BIST":
            continue
        s.append(f"| {r['kod']} | {r['yon']} | {r['pazar']} | {r['hucre']} | {r['n1']} / {r['n0']} | {_yy(r['fark'], 2)} [{_yy(r['boot_alt'], 2)}, {_yy(r['boot_ust'], 2)}] |")
    # tam tablo
    s += ["", "## 3. SATIR TABLOSU (her hipotez x pazar x hücre)", "",
          "| Ç | deneme | pazar | hücre | n (bayrak / eşsiz) | ESKİ h5 FARK (n) / etiket | YENİ R15 FARK [boot] | SIRA | p | güç | plasebo FARK / kapı | durum | YENİ etiket | DEĞİŞTİ Mİ (etiket; işaret) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in J["satir"]:
        dg = ("-" if r["etiket_degisti"] is None else ("EVET" if r["etiket_degisti"] else "hayır")) + "; " + \
             ("-" if r["isaret_degisti"] is None else ("EVET" if r["isaret_degisti"] else "hayır"))
        s.append(f"| {r['c']} | {r['kod']} ({r['yon']}) | {r['pazar']} | {r['hucre']} | {r['n']} ({r['n_bayrak']} / {r['n_essiz']}) | "
                 f"{_yy(r['eski_fark'], 1)} ({r['eski_n'] if r['eski_n'] is not None else '-'}) / {r['eski_etiket']} | "
                 f"{_yy(r['fark'], 2)} [{_yy(r['boot_alt'], 2)}, {_yy(r['boot_ust'], 2)}] | {_ys(r['sira'], 3)} | {_ys(r['p'], 4)} | {_ys(r['guc'], 2)} | "
                 f"{_yy(r['plasebo_fark'], 2)} / {'geçti' if r['plasebo_gecti'] else 'DÜŞTÜ'} | {r['durum']} | {r['yeni_etiket']} | {dg} |")
    s += ["", "## 4. ETİKET TABLOSU (hipotez başına; BH: Ç'nin m'i, sınama p = max(p ABD, p AVR))", "",
          "| Ç | kod | yön | eski etiket | yeni ham | gerekçe | p (BH) | BH | YENİ etiket | değişti |", "|---|---|---|---|---|---|---|---|---|---|"]
    for e in J["etiket"]:
        s.append(f"| {e['c']} | {e['kod']} | {e['yon']} | {e['eski']} | {e['yeni_ham']} | {e['neden']} | {_ys(e['p_bh'], 4)} | {'geçti' if e['bh'] else '-'} | "
                 f"{e['yeni']} | {'-' if e['degisti'] is None else ('EVET' if e['degisti'] else 'hayır')} |")
    yu = J["yeniden_uretim"]
    s += ["", "## 5. YENİDEN ÜRETİM (bağımsız düz pandas / düz döngü)", "", f"- SONUÇ: {'TUTTU' if yu['tuttu'] else 'TUTMADI'}", "",
          "| Ç | kod | pazar | hücre | n düz / kod | FARK düz / kod | SIRA düz / kod | medyan düz / kod | eşit |", "|---|---|---|---|---|---|---|---|---|"]
    for h in yu["hucre"]:
        s.append(f"| {h['c']} | {h['kod']} | {h['pazar']} | {h['hucre']} | {h['n_duz']} / {h['n']} | {_yy(h['fark_duz'], 4)} / {_yy(h['fark'], 4)} | "
                 f"{_ys(h['sira_duz'], 6)} / {_ys(h['sira'], 6)} | {_yy(h['med_duz'], 4)} / {_yy(h['med'], 4)} | {'EVET' if h['esit'] else 'HAYIR'} |")
    s += ["", f"- R15 ham veriden düz döngü (30 olay, C194 satırları): eşit {sum(x['esit'] for x in yu['r15'])} / {len(yu['r15'])}"
          + ("" if all(x["esit"] for x in yu["r15"]) else "; bozuk: " + "; ".join(f"{x['pazar']} {x['sembol']} {x['giris']} kod {x['kod']} düz {x['duz']}"
                                                                                 for x in yu["r15"] if not x["esit"])),
          "- Eş ortalaması bütün evrende düz döngü (2 olay, C194 Y10c ABD): " + "; ".join(
              f"{x['sembol']} {x['giris']}: n {x['n_duz']} / {x['n_kod']}, eş {_yy(x['es_duz'], 4)} / {_yy(x['es_kod'], 4)} {'EVET' if x['esit'] else 'HAYIR'}"
              for x in yu["es"])]
    return "\n".join(s) + "\n"


# ---------------------------------------------------------------- 6) ÖN KAYIT (getirisiz)
def yk_onkayit_metni(kontrol_md: str, uzerine: bool = False) -> str:
    F1 = yk_olay("Y1"); Fd = yk_olay("DS"); Ft = yk_olay("TUR")
    reg = yk_regresyon(F1); sha = yk_sha_simdi()
    huni = {}
    for x in YK_C:
        cd = yk_c(x["c"]); F = {"Y1": F1, "DS": Fd, "TUR": Ft}[cd["kume"]]
        huni[cd["c"]] = yk_huni(F, [b for _, b, _, _ in cd["hip"]])
    _yk_yaz(os.path.join(YK_YOL["cikti"], YK_DOSYA["huni"]), json.dumps(_yk_json({"zaman_utc": _yk_simdi(), "huni": huni, "regresyon": reg}),
                                                                         ensure_ascii=False, indent=1))
    s = [f"# CETVEL2 YENİDEN KOŞU — ÖN KAYIT ({_yk_simdi()})", "",
         f"{YK_SURUM}. Bu dosya ölçümden ÖNCE yazıldı ve git'e işlendi; yk_kapi (c2_yeniden_kosu.py) burada yazılı her sha'yı, git kaydını, "
         "CETVEL2 v2.1 kapısını (C2.c2_kapi) ve IZ_KARNE.ik_kontrol_kapisi'ni denetler; biri tutmazsa koşu DURUR. Bayrak sayımları getirisizdir "
         "(sinyal günü dönemi; ölçülen n giriş günü / tekil / 15 bar / eş ile küçülür).", "",
         "## 0. SHA'LAR", ""]
    s += [f"- {k}: `{v}`" for k, v in sha.items()]
    s += ["", "## 1. CETVEL (değişmez)", "",
          "CETVEL2 v2.1 AYNEN (CETVEL2_ON_KAYIT_v2.1.md; C2_ESIK_SHA ve C2_KOD_SHA yukarıda): giriş t'den sonraki ilk geçerli bar açılışı; R15 = 15. geçerli "
          "bar kapanışı / E0 − 1 (stop yok); eş = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x likidite üçlüsü x F15 çeyreği; sınırlar "
          "cetvel2_esik_v2.1.json), aynı denemenin o günkü olayları dışarıda, en az 5 eş; hücre TUTAR / plasebo kapısı (200 tohum) / güç (cetvel2_guc_v2.1.json) "
          "/ ETİKET (ABD + AVR dört hücre) / BH q 0,10 (sınama p = max(p ABD, p AVR), m = Ç'nin m'i) C2_ESIK'ten. Arayüz: C2.c2_olc(olaylar, hipotez, "
          "m_bh = m, tohum0 = Ç tohumu). Dönem: eğitim 2016-22, sınama 2023-01-01..2026-08-31 (giriş günü). tekil 15 işlem günü (c2_olay).", "",
          "## 2. KAPSAM (Ç, olay kümesi, hipotezler, yön, m, tohum)", "",
          "Yön: '+' = bayraklı olay konum eşli eşlerden İYİ beklenir (R15 FARK > 0); '-' = KÖTÜ beklenir; '?' = iki yönlü (DS hipotezlerinde DS_HIP'teki "
          "gibi). Kol A = bütün Y1 (S6 AL) olayları; kol B = Y9 (Y1 VE Ş1: F15 <= 0,25 VE F17 <= -0,20). Eşikler: YAPI_HEDEF YH_ESIK (Ş1-Ş9, F14, "
          "Y10-Y11), YH_ESIK6 (G1 / G2 / G2u), YH_ESIK8 (Ş10, Y13), devir1/2/3_esik.json YÖN 1 (eğitim 2016-22 Y1 çeyrekleri; mühürlü), puan_Y1 "
          "dilimleri (M2 birleşik), ds_olay.csv.gz F_DS* (ds_esik.json). Bayraklar dosyadan okunur ya da modülün maske fonksiyonu AYNEN çağrılır "
          "(yh_s9_sartlar, yh_y10_maske, yh_y11_maske, yh_grup6_maske, yh_s10_maske, yh_d1_maske, yh_d2_maske, yh_d3_maske); yeniden hesap yok.", "",
          "| Ç | ad | olay kümesi | m (BH) | tohum0 | hipotezler (kod: bayrak, yön; eski kaynak) |", "|---|---|---|---|---|---|"]
    for x in YK_C:
        cd = yk_c(x["c"])
        hs = "; ".join(f"{k}: {b or 'hepsi'} {y} ({'/'.join(str(z) for z in e)})" for k, b, y, e in cd["hip"])
        s.append(f"| {cd['c']} | {cd['ad']} | {cd['kume']} | {cd['m']} | {cd['tohum0']} | {hs} |")
    s += ["", "Notlar (ölçümden önce): (a) Ç196 karne eski testte BİRİKİMLİ huni idi; burada iş tanımı gereği TEK süzgeç (Y1 üstünde ve Y9 üstünde); eski etiket "
          "'huni adımı' olarak yazılır (yalnız Ş1 adımı tek süzgeçle aynı). (b) Ç197 PUAN: A modeli 2016-22'de öğrenip 2023-26'yı, B tersini puanlar; "
          "sızıntısız tek bayrak = eğitim hücresinde B dilimi, sınama hücresinde A dilimi (P_AB); C yürüyen. Üst %20 = ust20 ∪ ust10 ∪ ust5. (c) DEVİR: "
          "D1 18 aday (ana '+', ters '-'), D2 10 ana, D3 4 ana = 32 aday x 2 kol; D2 / D3 W1 / W2 / W2D / AYK / NR7 aynı maske (tekrar; her Ç kendi m'iyle). "
          "PP ve RV (Ç199) eski ön kayıtta 'kapalı konu (hacim)' işaretliydi; yeniden ölçüm yalnız eski testin cetvel düzeltmesi, konu yeniden açılmaz. "
          "(d) TABAN ve TABAN_DS bilgi (m 1; karar yok); TUR bilgi (sayfa n 40 + 40; ÖLÇÜLEMEDİ beklenir). (e) Hakem tur 5 ve 7: Cemal etiketi yok -> "
          "anahtar dosyaları AÇILMAZ (kör kural); tur havuz listeleri (T1.6 / T1.7 / T1.8) diskte saklı değil (yalnız sayılar) ve tur 5 / 7 sayfalarını "
          "içerir -> havuz ölçülmez. (f) Ç202 sınıf II (DS47-DS53) kapsam dışı (iş tanımı: 25 hipotez). (g) DS içi eş (Ç202) ve G2 − G1 (Ç196) "
          "ay kümeli boot ile BİLGİ.", "",
          "ESKİ değerler: etiket = rapordaki / sonuç json'daki etiket (sonuc.json deneme, filtre_karne.json, grup6.json, puan7.json birlesik|M2, devir*_sonuc.json "
          "ABD+AVR satırı, ds_sonuc.json karne); h5 FARK = eski satır dosyasından ort(h5 − es_h5) (olc satırları; eğitim 2016-22, sınama 2023 + 2024-26) ya da "
          "eski json'daki fark (devir, DS). DEĞİŞTİ Mİ: normalleştirilmiş etiket (BİLGİ (X) = X; parantez notu atılır) farklı mı; ayrıca hücre FARK işareti.", "",
          "YENİDEN ÜRETİM (koşudan sonra, bağımsız): >= 3 hücre (C194 Y10c ABD sınama, C196 A_S1 AVR eğitim, C202 DS06 ABD sınama, C199 D2_NR7_A ABD eğitim) "
          "satır dosyasından düz pandas (n, ort FARK, ort SIRA, medyan); 30 olayın R15'i ham V_*.pkl'den düz döngü; 2 olayın eş ortalaması bütün evrende düz döngü.", "",
          "## 3. GETİRİSİZ BAYRAK SAYIMI (sinyal günü dönemi; pazar|hücre)", ""]
    for c, H in huni.items():
        s.append(f"### {c}"); s.append("")
        s.append("| bayrak | " + " | ".join(f"{p} {h}" for p in C2.C2_PAZAR for h in C2.C2_HUCRE) + " |")
        s.append("|---|" + "---|" * 6)
        for b, v in H.items():
            s.append(f"| {b} | " + " | ".join(str(v[f'{p}|{h}']) for p in C2.C2_PAZAR for h in C2.C2_HUCRE) + " |")
        s.append("")
    s += ["## 4. REGRESYON (bayrak kümesi = eski deneme satır dosyası; anahtar kümesi)", "", "| deneme | bayrak | dosya | eşit | yalnız bayrak | yalnız dosya |",
          "|---|---|---|---|---|---|"]
    for d, v in reg.items():
        s.append(f"| {d} | {v['bayrak']} | {v['dosya']} | {'EVET' if v['esit'] else 'HAYIR'} | {v['yalniz_bayrak']} | {v['yalniz_dosya']} |")
    s += ["", kontrol_md.strip(), ""]
    return "\n".join(s)


def yk_onkayit_yaz(kontrol_md_yol: str, uzerine: bool = False) -> str:
    yol = os.path.join(YK_YOL["cikti"], YK_DOSYA["onkayit"])
    if os.path.exists(yol) and not uzerine:
        raise YKHata(f"ön kayıt zaten var: {yol} (üzerine yazılmaz; --uzerine-yaz yalnız koşu öncesi)")
    if not os.path.exists(kontrol_md_yol):
        raise YKHata(f"kontrol tablosu dosyası yok: {kontrol_md_yol}")
    m = yk_onkayit_metni(open(kontrol_md_yol, encoding="utf-8").read(), uzerine)
    reg = json.load(open(os.path.join(YK_YOL["cikti"], YK_DOSYA["huni"]), encoding="utf-8"))["regresyon"]
    bozuk = [d for d, v in reg.items() if not v["esit"]]
    if bozuk:
        raise YKHata(f"regresyon TUTMADI: {bozuk} -> ön kayıt yazılmadı")
    _yk_yaz(yol, m)
    return yol


# ---------------------------------------------------------------- çakışma kapısı
def _cakisma_kontrol_yk(_once=_CK_ONCE_YK, _dosya="c2_yeniden_kosu.py"):
    """Çakışma kapısı: bu dosya bellekteki yk_ / YK_ / _yk öneki DIŞINDAKİ mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_YK", "_CK_KAYIT", "_cakisma_kontrol_yk", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "subprocess", "_dt", "annotations", "argparse", "warnings",
           "Any", "Dict", "List", "Optional", "Tuple", "C2", "YH", "_h", "_D1", "_D2", "_D3", "_KARNE_A", "_KARNE_B")
    onek = ("yk_", "YK_", "_yk", "YKHata", "yklog", "KOK_YK", "_YK")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std and not k.startswith(onek))
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_yk()

if __name__ == "__main__" and "get_ipython" not in globals():
    ap = argparse.ArgumentParser(description=YK_SURUM)
    ap.add_argument("komut", choices=["huni", "onkayit", "kos", "birlestir", "sha"])
    ap.add_argument("--c", default=None, help="Ç kodu (kos): " + ", ".join(x["c"] for x in YK_C))
    ap.add_argument("--kontrol-md", default=None)
    ap.add_argument("--parca", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--gitsiz", action="store_true")
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "huni":
            F_ = yk_olay("Y1")
            print(json.dumps(_yk_json(yk_regresyon(F_)), ensure_ascii=False, indent=1))
        elif a.komut == "onkayit":
            print(yk_onkayit_yaz(a.kontrol_md, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            if not a.c:
                raise YKHata("--c gerekli")
            for c_ in a.c.split(","):
                yk_kos_c(c_.strip(), git=not a.gitsiz, parca=a.parca)
        elif a.komut == "birlestir":
            J_ = yk_birlestir(a.parca, a.veri)
            print(json.dumps(_yk_json({"gecis": J_["gecis"], "secili": len(J_["secili"]), "yeniden_uretim": J_["yeniden_uretim"]["tuttu"]}),
                             ensure_ascii=False, indent=1))
        else:
            print(json.dumps(yk_sha_simdi(), indent=1))
    except (YKHata, C2.C2Hata, YH.YHHata) as ex:
        yklog.error("%s", ex); sys.exit(1)
