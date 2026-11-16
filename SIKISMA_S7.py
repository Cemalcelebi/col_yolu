"""SIKISMA_S7 — S7: bölge İÇİNDEN ölçülen sıkışma kutusu (göz aracı; getiri / kazanç YOK), Pine ikizi COL_S7_BOLGE.pine (16 Kasım 2026).

SIKISMA_OBEK.py'den TAŞINDI (denetim, 16 Kas): S5 ön kaydının KOD sha kapısı bütün SIKISMA_OBEK.py dosyasına bakar; Mart 2027 S5_DİP ileri testi
aynı komutla koşacağı için SIKISMA_OBEK.py HEAD ile bayt bayt aynı tutulur. Mantık, eşik, ızgara ve kural taşımadan önceki koda göre AYNI
(so_s7_muhur değişmedi). SIKISMA_OBEK yalnız kütüphane olarak içe alınır (so_s5, so_bolge_sonu, SO_ESIK, SO_YOL, SO_PAZAR, SOHata).

Cemal (16 Kas): "kod rastgele bölgelere sıkışma diyor". S5 / S6 her günü SON 15 BARLIK kayan pencereyle yargılar; S7'de bütün şekil şartları YALNIZ aday
bölgenin [s, e] barlarıyla ölçülür; R (normal gün) bölgeden ÖNCEKİ 250 bardan gelir. Kural tablosu SO7_KURAL / SO7_SINIF (KURAL MOTORU).
Komut:  python SIKISMA_S7.py s7onyazim (ölçümden önce; zaten yazıldı) | s7tasarim (8 örnek x 72 nokta) | s7sayim (S5 / S6 / S7) | s7pine | s7md
Colab:  exec(open('SIKISMA_S7.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_*.pkl (islenmis-veri dalı). Çıktı: arastirma_cikti/sikisma_obek/ S7_TASARIM.md, s7_tasarim.json, COL_S7_BOLGE.pine (beklenen kutular).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_S7 = {k: id(v) for k, v in globals().items()}

import hashlib  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import datetime as _dt  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_S7 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_S7 not in sys.path:
    sys.path.insert(0, KOK_S7)

import SIKISMA_OBEK as SO  # noqa: E402  (kütüphane; S5 fonksiyonları değişmez)
import SIKISMA_YENIDEN as SY  # noqa: E402
import SIKISMA_CEMAL as SC  # noqa: E402

s7log = logging.getLogger("col.sikisma_s7")
if not s7log.handlers:
    _s7_h = logging.StreamHandler(sys.stderr)
    _s7_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sikisma_s7: %(message)s", "%H:%M:%S"))
    s7log.addHandler(_s7_h)
    s7log.setLevel(logging.INFO)
    s7log.propagate = False


class S7Hata(SO.SOHata):
    """S7 durdurucu hata (ön yazım yok / mühür tutmuyor / veri yok / geçersiz aralık)."""


_S7_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _s7_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


# ---------------------------------------------------------------- S7) BÖLGE İÇİNDEN ÖLÇÜLEN SIKIŞMA KUTUSU (16 Kasım 2026; Pine ikizi COL_S7_BOLGE.pine)
# Cemal (16 Kas): "kod rastgele bölgelere sıkışma diyor". S5 / S6 her günü SON 15 BARLIK kayan pencereyle yargılar; pencere bölgeden önceki düşüşü
# içerir. S7'de bütün şekil şartları YALNIZ aday bölgenin [s, e] barlarıyla ölçülür; hissenin 'normal günü' R bölgeden ÖNCEKİ 250 bardan gelir.
# Bu bir GÖZ ARACIDIR: getiri / kazanç ölçülmez, iddia yoktur. S5 fonksiyonları (so_s5 ...) değişmedi; S7 adları so_s7_ / _so7_ / SO7_ önekli.
SO7_SURUM = "S7 v1.0 (2026-11-16): bölge içinden ölçülen sıkışma kutusu (Z1-Z6 + DİP / YOL ÜSTÜ; nedensel açılış, geriye uzatma, kırılım / sönme)"
SO7_DOSYA = {"tasarim": "S7_TASARIM.md", "tasarim_json": "s7_tasarim.json", "pine": "COL_S7_BOLGE.pine", "nasil": "PINE_S7_NASIL.md"}
SO7_ON_YAZIM_SONU = "<!-- S7_ON_YAZIM_SONU -->"
SO7_SAPMA_NOTU = ("**SAPMA NOTU (yalnız dosya taşıma, mantık aynı; 16 Kas 2026, ana model denetimi):** ön yazımda 'Python ikizi: SIKISMA_OBEK.py "
                  "so_s7_bolgeler' yazar; S7 kodu S5 ön kaydının KOD sha kapısını bozmamak için SIKISMA_S7.py dosyasına taşındı (SIKISMA_OBEK.py HEAD ile "
                  "bayt bayt aynı). Komutlar `python SIKISMA_S7.py s7tasarim | s7sayim | s7pine | s7md`. Eşik, ızgara, kural ve örnekler aynı: ön yazım "
                  "mührü (so_s7_muhur) yeniden hesaplandı ve tuttu; tasarım ve sayım yeni modülle yeniden koşuldu, sayılar taşımadan önceki koşuyla birebir aynı.")
SO7_PINE_BAS = "// ==== BEKLENEN KUTULAR (so_s7_pine_blok üretir; elle düzenleme) ===="
SO7_PINE_SON = "// ==== BEKLENEN KUTULAR SONU ===="

SO7_ESIK: Dict[str, Any] = {
    # varsayılan = iş tanımı (16 Kas); 'secilen' = tasarım sınamasının seçtiği nokta (sonuçtan sonra OYNANMAZ).
    "varsayilan": {"k_m": 0.75, "bb": 0.20, "Lmin": 8, "bant": {"BIST": 0.08, "ABD": 0.06, "AVR": 0.06}, "egim": [-0.03, 0.08]},
    "secilen": {"k_m": 0.75, "bb": 0.15, "Lmin": 8, "bant": {"BIST": 0.08, "ABD": 0.06, "AVR": 0.06}, "egim": [-0.03, 0.08]},   # s7tasarim 16.11.2026: 7 / 8 (CCOLA-E kaçtı), 8/8 nokta yok
    "Lmax": 80, "R_gun": 250, "zipla": 1, "z2_zipla_haric": 2.0, "z2_hepsi": 3.0, "z5_R": 0.5, "z5_son": "n_son = floor(2L / 5), n_ilk = L - n_son",
    "bb_gun": 20, "bb_k": 2.0, "bb_dagilim": 250, "sinif_gun": 120, "dip_konum": 0.30, "dip_tepe": 0.10, "yol_konum": 0.60,
    "sma_gun": 50, "sma_egim_gun": 20, "kirilim": 0.01, "gecmis_min": 290,
    "kilit": "bölge bitince (kırılım mumu ya da sönmeyi tetikleyen bar = kilit barı) yeni bölgenin başlangıcı s > kilit (onay e >= kilit + Lmin)",
    "gecerli_bar": "H > L, V > 0, O > 0, C > 0, sonlu (SY.sy_veri_hazirla; Python'da 31.08.2026 kriz kesiği)",
}

# KURAL MOTORU: her şart ad + eşik + yön + açıklama; 'acik' = bölge AÇIKKEN her yeni barda yeniden sınanır. d / s = ölçü ve sınır (m: ölçüler, p: eşikler).
SO7_KURAL: List[Dict[str, Any]] = [
    {"ad": "Z1", "esik": "k_m", "yon": "<=", "acik": True, "aciklama": "küçük mum: bölgedeki en büyük 1 mum (zıplama) hariç (H-L)/C medyanı <= k_m x R",
     "d": lambda m, p, E: m["z1"], "s": lambda m, p, E: p["k_m"] * m["R"]},
    {"ad": "Z2a", "esik": "z2_zipla_haric", "yon": "<", "acik": True, "aciklama": "dev mum yok: zıplama hariç en büyük mum (2. büyük) < 2 x R",
     "d": lambda m, p, E: m["z2_ikinci"], "s": lambda m, p, E: E["z2_zipla_haric"] * m["R"]},
    {"ad": "Z2b", "esik": "z2_hepsi", "yon": "<", "acik": True, "aciklama": "dev mum yok: zıplama dahil en büyük mum < 3 x R",
     "d": lambda m, p, E: m["z2_max"], "s": lambda m, p, E: E["z2_hepsi"] * m["R"]},
    {"ad": "Z3", "esik": "bant", "yon": "<=", "acik": False, "aciklama": "bant: bölge kapanışlarından bandı en çok daraltan 1 uç gün çıkarılır; max/min - 1 <= bant",
     "d": lambda m, p, E: m["band"], "s": lambda m, p, E: p["bant"]},
    {"ad": "Z4a", "esik": "egim[0]", "yon": ">=", "acik": False, "aciklama": "yataylık: ln(C) ~ gün EKK eğimi x L >= eğim alt",
     "d": lambda m, p, E: m["egim"], "s": lambda m, p, E: p["egim"][0]},
    {"ad": "Z4b", "esik": "egim[1]", "yon": "<=", "acik": False, "aciklama": "yataylık: ln(C) ~ gün EKK eğimi x L <= eğim üst",
     "d": lambda m, p, E: m["egim"], "s": lambda m, p, E: p["egim"][1]},
    {"ad": "Z5", "esik": "z5_R", "yon": ">=", "acik": False, "aciklama": "dip savunması: son floor(2L/5) barın en düşük Low'u >= ilk barların en düşük Low'u x (1 - 0,5 x R)",
     "d": lambda m, p, E: m["z5_son"], "s": lambda m, p, E: m["z5_ilk"] * (1.0 - E["z5_R"] * m["R"])},
    {"ad": "Z6", "esik": "bb", "yon": "<=", "acik": True, "aciklama": "Bollinger: bölgedeki EN DAR BBW (20, 2σ, nüfus std, 4σ/SMA20); s'den önceki 250 BBW içinde payı (<=) <= bb",
     "d": lambda m, p, E: m["z6p"], "s": lambda m, p, E: p["bb"]},
]
SO7_SINIF: Dict[str, List[Dict[str, Any]]] = {
    "DIP": [{"ad": "D1", "esik": "dip_konum", "yon": "<=", "aciklama": "konum = (bölge medyan C - min C[s-120..e]) / (max - min) <= 0,30",
             "d": lambda m, p, E: m["konum"], "s": lambda m, p, E: E["dip_konum"]},
            {"ad": "D2", "esik": "dip_tepe", "yon": ">=", "aciklama": "max C[s-120..s-1] / bölge medyan C - 1 >= %10",
             "d": lambda m, p, E: m["tepe"], "s": lambda m, p, E: E["dip_tepe"]}],
    "YOL": [{"ad": "Y1", "esik": "-", "yon": ">", "aciklama": "bölge medyan C > SMA50(e)", "d": lambda m, p, E: m["med"], "s": lambda m, p, E: m["sma"]},
            {"ad": "Y2", "esik": "sma_egim_gun", "yon": ">", "aciklama": "SMA50(e) > SMA50(e-20)", "d": lambda m, p, E: m["sma"], "s": lambda m, p, E: m["sma_once"]},
            {"ad": "Y3", "esik": "yol_konum", "yon": ">=", "aciklama": "konum >= 0,60 (Z5 ayrıca bütün bölgelerde şart)",
             "d": lambda m, p, E: m["konum"], "s": lambda m, p, E: E["yol_konum"]}],
}

SO7_IZGARA: Dict[str, Any] = {
    "k_m": [0.65, 0.75, 0.85], "bb": [0.15, 0.20, 0.25], "Lmin": [8, 10],
    "bant": [{"BIST": 0.08, "ABD": 0.06, "AVR": 0.06}, {"BIST": 0.10, "ABD": 0.08, "AVR": 0.08}],
    "egim": [[-0.03, 0.08], [-0.02, 0.06]],
    "secim_kurali": "(1) 8 sınamanın (3 seçmeli + 5 seçmemeli, V_BIST) hepsini tutan noktalar. (2) Aralarından varsayılana (k_m 0,75, bb 0,20, Lmin 8, "
                    "bant BIST %8, eğim [-%3, +%8]) en az farklı parametre sayısı. (3) Eşitlikte SIKI olan: sıra anahtarı (k_m küçük, bb küçük, Lmin büyük, "
                    "bant dar, eğim aralığı dar). (4) Hiçbir nokta 8/8 değilse en çok tutanlar arasında (2)-(3); kaçanlar açıkça yazılır. Eşik bu sonuçtan "
                    "sonra OYNANMAZ.",
    "ornek_kurali": "SEÇMELİ tutar: örnek aralığıyla (geçerli bar) kesişimi en büyük S7 bölgesi [s, bitiş] (eşitlikte erken olan) için kesişim / örnek "
                    "uzunluğu >= 0,5 VE sınıfı beklenen. Başlangıç farkı = s - örnek ilk barı, bitiş farkı = bitiş - örnek son barı (geçerli bar). SEÇMEMELİ "
                    "tutar: [örnek ilk - 5 geçerli bar, örnek son + 5 geçerli bar] ile kesişen hiçbir S7 bölgesi [s, bitiş] yok. Fiyat V_BIST (düzeltilmiş).",
    "bant_eslesme": "bant ızgarası BIST değeriyle seçilir; ABD / AVR eşi S5 ızgarasındaki gibi (BIST %8 -> %6, BIST %10 -> %8)",
}
SO7_ORNEK: List[Dict[str, Any]] = [
    {"ad": "FENER-E", "sembol": "FENER", "ilk": "2025-10-14", "son": "2025-11-07", "beklenen": "DIP", "secmeli": True},
    {"ad": "CCOLA-E", "sembol": "CCOLA", "ilk": "2025-10-02", "son": "2025-10-20", "beklenen": "DIP", "secmeli": True},
    {"ad": "ENJSA-T", "sembol": "ENJSA", "ilk": "2025-07-28", "son": "2025-08-15", "beklenen": "YOL", "secmeli": True},
    {"ad": "FENER-A", "sembol": "FENER", "ilk": "2025-12-03", "son": "2025-12-16", "beklenen": "-", "secmeli": False},
    {"ad": "CCOLA-T", "sembol": "CCOLA", "ilk": "2025-07-29", "son": "2025-08-29", "beklenen": "-", "secmeli": False},
    {"ad": "ENJSA-O", "sembol": "ENJSA", "ilk": "2025-01-20", "son": "2025-02-14", "beklenen": "-", "secmeli": False},
    {"ad": "ENJSA-A", "sembol": "ENJSA", "ilk": "2025-12-30", "son": "2026-01-27", "beklenen": "-", "secmeli": False},
    {"ad": "ENJSA-V", "sembol": "ENJSA", "ilk": "2026-07-06", "son": "2026-07-17", "beklenen": "-", "secmeli": False},
]
SO7_TAMPON = 5
SO7_ORTUSME = 0.5
SO7_S6 = {"egim": [-0.01, 0.10], "bb": 0.10, "net_alt": -0.01, "N": 5,
          "aciklama": "COL_S6_TASLAK.pine varsayılanı: S5 yapısı (so_s5) + eğim x15 [-%1, +%10] + BB yüzdelik <= 0,10 + net >= -%1 + N = 5 ardışık gün; "
                      "kutu: onay = N. gün, başlangıç = onay - (N-1), kırılım %1 / sönme; S5 kutusu = aynı makine, S5 ön kayıt eşikleri, N = 1"}

SO7_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "getiri / sonuç ölçülmüyor; yalnız bölge sayımı ve 8 örnekte göz sınaması; kıyas S5 / S6 kutularıyla aynı evren ve aynı geçerli bar"),
    "K2": ("EVET", "so_s7_bolgeler nedensel: e'de yalnız [s, e] ve s öncesi 250 bar (R, BBW payı), sınıf [s-120, e], SMA50(e), SMA50(e-20); geriye uzatma "
                   "yalnız e'ye kadarki barlarla; test_sikisma_obek.py önek değişmezliği (3 hisse x 5 kesim: s, e, sınıf, R aynı) mekanik"),
    "K3": ("EVET", "SY.sy_veri_hazirla: H>L, V>0, O>0, C>0, sonlu olmayan bar atılır; bütün pencereler geçerli bar sayar; Pine'da aynı 'gecerli' süzgeci"),
    "K4": ("UYGULANMAZ", "getiri yok; bölge tekilleştirmesi tanımda (kilit: yeni bölge s > önceki bölgenin bitiş / kırılım barı)"),
    "K5": ("UYGULANMAZ", "getiri / giriş fiyatı yok; kutuda kazanç etiketi YOK"),
    "K6": ("EVET", "tek fiyat kipi V_BIST / V_ABD / V_AVR düzeltilmiş (fi_k1_veri); mum ve R yüzde (oran); BIST bölünme sıçraması bir kapanışla "
                   "bandı kırar ya da Z2 (3 x R) ile bölge açılmaz; Pine'da TradingView fiyatı (kuruş farkı yazılı)"),
    "K7": ("EVET", "evren bugünün listesi (V_*.pkl): batan / kottan çıkan hisse yok; sayım tablosunda ve raporda yazılı"),
    "K8": ("EVET", "tasarım 3 seçmeli + 5 seçmemeli örnekle (aşırı uyum riski yazılı; 'bulgu' denmez); sayım üç pazar, bütün dönem, betimsel"),
    "K9": ("EVET", "bu ön yazım (ızgara + seçim kuralı + örnek kuralı + eşikler, mühür sha256 + UTC zaman) s7tasarim koşmadan ÖNCE yazıldı; "
                   "s7tasarim mührü yeniden hesaplar, tutmazsa durur; commit ana modelde"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırma yok; yalnız OHLCV"),
    "K11": ("EVET", "en az 2 sayı bağımsız kodla (rapor dışı betik, ayrı hesap) yeniden üretilir: bir örnek bölgesinin Z ölçüleri ve BIST bölge sayısı"),
    "K12": ("EVET", "göz aracı; 'iz / emare' sözü yok, getiri / kazanç iddiası yok; Pine'da getiri etiketi yok"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_so korunur (S7 adları önekli, öteki modüllerle ad kesişimi testte); yasak dosyalara dokunulmaz; "
                    "e-posta / anahtar taraması testte; ağdan veri yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; gösterge aday gösterir"),
}


def _so7_swv(x: np.ndarray, w: int) -> np.ndarray:
    """Satır j = x[j .. j+w-1] (n < w ise 0 satır)."""
    x = np.asarray(x, float)
    if len(x) < w:
        return np.empty((0, w))
    return np.lib.stride_tricks.sliding_window_view(x, w)


def _so7_prm(prm: Dict[str, Any], pazar: str) -> Dict[str, Any]:
    """Pazar bandını çöz: {'k_m', 'bb', 'Lmin', 'bant' (sayı), 'egim'}."""
    b = prm["bant"]
    return {"k_m": float(prm["k_m"]), "bb": float(prm["bb"]), "Lmin": int(prm["Lmin"]), "egim": [float(prm["egim"][0]), float(prm["egim"][1])],
            "bant": float(b[pazar] if isinstance(b, dict) else b)}


def _so7_smin(E: Dict[str, Any]) -> int:
    """En erken bölge başlangıcı: R için 250 önceki rp (rp[0] yok), BBW payı için 250 önceki tanımlı BBW, sınıf için 120 önceki bar."""
    return int(max(E["R_gun"] + 1, E["bb_gun"] - 1 + E["bb_dagilim"], E["sinif_gun"]))


def _so7_diziler(d: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Hisse dizileri (yalnız geçerli barlar; d = SY.sy_veri_hazirla çıktısı). Her bar kendi geçmişiyle: BBW_j, SMA50_j; R[s] = medyan rp[s-250..s-1]."""
    E = E or SO7_ESIK
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    n = len(C)
    if n and not ((H > L).all() and (C > 0).all() and (O > 0).all()):
        raise S7Hata("S7: geçersiz bar var (önce SY.sy_veri_hazirla)")
    Cp = np.r_[np.nan, C[:-1]]
    rp = (H - L) / Cp
    R = np.full(n + 1, np.nan)
    RW = _so7_swv(rp, E["R_gun"])
    if len(RW):
        R[E["R_gun"]:E["R_gun"] + len(RW)] = np.median(RW, axis=1)        # R[s] = medyan rp[s-250 .. s-1]
    bbw = np.full(n, np.nan)
    W = _so7_swv(C, E["bb_gun"])
    if len(W):
        m = W.mean(axis=1)
        sd = np.sqrt(((W - m[:, None]) ** 2).mean(axis=1))
        bbw[E["bb_gun"] - 1:] = 2.0 * E["bb_k"] * sd / m
    sma = np.full(n, np.nan)
    Ws = _so7_swv(C, E["sma_gun"])
    if len(Ws):
        sma[E["sma_gun"] - 1:] = Ws.mean(axis=1)
    return {"n": n, "O": O, "H": H, "L": L, "C": C, "mum": (H - L) / C, "rp": rp, "R": R[:n], "bbw": bbw, "sma": sma,
            "lnC": np.log(C), "tarih": d.index}


def _so7_olcu(A: Dict[str, Any], s: int, e: int, E: Optional[Dict[str, Any]] = None, acik: bool = False) -> Dict[str, float]:
    """[s, e] bölgesinin ölçüleri (yalnız s..e barları + s öncesi R / BBW referansı + sınıf için [s-120, e] ve SMA50(e), SMA50(e-20)).
    acik=True: yalnız açık bölgede yeniden sınanan Z1, Z2, Z6 ve kutu üst / alt (Z3 bandı)."""
    E = E or SO7_ESIK
    L = e - s + 1
    if s < 1 or L < 3 or e >= A["n"]:
        raise S7Hata(f"S7 ölçü: geçersiz aralık s={s} e={e} n={A['n']}")
    mm = np.sort(A["mum"][s:e + 1])
    R = float(A["R"][s])
    w = np.sort(A["C"][s:e + 1])
    if w[-2] / w[0] <= w[-1] / w[1]:
        ust, alt = float(w[-2]), float(w[0])
    else:
        ust, alt = float(w[-1]), float(w[1])
    z6 = float(np.min(A["bbw"][s:e + 1]))
    pre = A["bbw"][s - E["bb_dagilim"]:s] if s >= E["bb_dagilim"] else np.full(E["bb_dagilim"], np.nan)
    m: Dict[str, float] = {"L": L, "R": R, "z1": float(np.median(mm[:-1])), "z2_max": float(mm[-1]), "z2_ikinci": float(mm[-2]),
                           "ust": ust, "alt": alt, "band": ust / alt - 1.0, "z6": z6,
                           "z6p": float(np.mean(pre <= z6)) if np.isfinite(z6) and np.isfinite(pre).all() else float("nan")}
    if acik:
        return m
    xm = np.arange(L, dtype=float) - (L - 1) / 2.0
    y = A["lnC"][s:e + 1]
    m["egim"] = float(((y - y.mean()) @ xm) / (xm @ xm) * L)
    ns = (2 * L) // 5
    m["z5_son"] = float(np.min(A["L"][e - ns + 1:e + 1])); m["z5_ilk"] = float(np.min(A["L"][s:e - ns + 1]))
    med = float(np.median(w))
    g = E["sinif_gun"]
    if s >= g:
        Cw = A["C"][s - g:e + 1]; lo, hi = float(Cw.min()), float(Cw.max())
        tp = float(A["C"][s - g:s].max())
    else:
        lo = hi = tp = float("nan")
    m["med"] = med
    m["konum"] = (med - lo) / (hi - lo) if hi > lo else float("nan")
    m["tepe"] = tp / med - 1.0
    m["sma"] = float(A["sma"][e]); m["sma_once"] = float(A["sma"][e - E["sma_egim_gun"]]) if e >= E["sma_egim_gun"] else float("nan")
    return m


def _so7_olcu_vek(A: Dict[str, Any], L: int, E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """_so7_olcu'nun her e için (uzunluk L, s = e-L+1) vektör hali; yalnız ÖN SÜZGEÇ (kesin karar _so7_olcu ile verilir). Dizi indeksi = e."""
    E = E or SO7_ESIK; n = A["n"]
    out = {k: np.full(n, np.nan) for k in ("R", "z1", "z2_max", "z2_ikinci", "band", "egim", "z5_son", "z5_ilk", "z6", "z6p", "med", "konum", "tepe",
                                           "sma", "sma_once")}
    if n < L + 1:
        return out
    e = np.arange(L - 1, n); s = e - L + 1
    Wm = np.sort(_so7_swv(A["mum"], L), axis=1)
    out["z1"][e] = np.median(Wm[:, :-1], axis=1); out["z2_max"][e] = Wm[:, -1]; out["z2_ikinci"][e] = Wm[:, -2]
    out["R"][e] = A["R"][s]
    Wc = np.sort(_so7_swv(A["C"], L), axis=1)
    k = Wc[:, -2] / Wc[:, 0] <= Wc[:, -1] / Wc[:, 1]
    out["band"][e] = np.where(k, Wc[:, -2], Wc[:, -1]) / np.where(k, Wc[:, 0], Wc[:, 1]) - 1.0
    out["med"][e] = np.median(Wc, axis=1)
    xm = np.arange(L, dtype=float) - (L - 1) / 2.0
    Wl = _so7_swv(A["lnC"], L)
    out["egim"][e] = ((Wl - Wl.mean(axis=1, keepdims=True)) @ xm) / (xm @ xm) * L
    ns = (2 * L) // 5
    Wlo = _so7_swv(A["L"], L)
    out["z5_son"][e] = Wlo[:, L - ns:].min(axis=1); out["z5_ilk"][e] = Wlo[:, :L - ns].min(axis=1)
    z6 = _so7_swv(A["bbw"], L).min(axis=1); out["z6"][e] = z6
    nb = E["bb_dagilim"]; ok = s >= nb
    if ok.any():
        P = _so7_swv(A["bbw"], nb)                                                     # satır j = bbw[j .. j+nb-1]
        ss = s[ok]; Pr = P[ss - nb]
        with np.errstate(invalid="ignore"):
            out["z6p"][e[ok]] = np.where(np.isfinite(Pr).all(axis=1) & np.isfinite(z6[ok]), (Pr <= z6[ok][:, None]).mean(axis=1), np.nan)
    g = E["sinif_gun"]; ok = s >= g
    if ok.any():
        G = _so7_swv(A["C"], g + L)                                                    # satır j = C[j .. j+g+L-1] = [s-g, e] (j = s-g)
        T = _so7_swv(A["C"], g)                                                        # satır j = C[j .. j+g-1] = [s-g, s-1]
        ss = s[ok]
        lo = G[ss - g].min(axis=1); hi = G[ss - g].max(axis=1); tp = T[ss - g].max(axis=1)
        md = out["med"][e[ok]]
        with np.errstate(invalid="ignore", divide="ignore"):
            out["konum"][e[ok]] = np.where(hi > lo, (md - lo) / (hi - lo), np.nan)
            out["tepe"][e[ok]] = tp / md - 1.0
    out["sma"][e] = A["sma"][e]
    eo = e[e >= E["sma_egim_gun"]]
    out["sma_once"][eo] = A["sma"][eo - E["sma_egim_gun"]]
    return out


def _so7_kiyas(d: Any, s: Any, yon: str, tol: float = 0.0) -> Any:
    """d (yon) s; tol > 0 ise sınır gevşetilir (yalnız ön süzgeç). NaN -> yanlış."""
    with np.errstate(invalid="ignore"):
        pay = tol * np.abs(s) + (1e-12 if tol else 0.0)
        if yon == "<=":
            return d <= s + pay
        if yon == "<":
            return d < s + pay
        if yon == ">=":
            return d >= s - pay
        if yon == ">":
            return d > s - pay
    raise S7Hata(f"S7 kural yönü bilinmiyor: {yon}")


def _so7_kural_sonuc(m: Dict[str, Any], p: Dict[str, Any], E: Dict[str, Any], acik: bool = False, tol: float = 0.0) -> Dict[str, Any]:
    """KURAL MOTORU: her şartın değeri, sınırı ve sonucu (skaler ya da dizi). acik=True: yalnız açıkken yeniden sınanan şartlar, sınıf yok."""
    out: Dict[str, Any] = {}
    for k in SO7_KURAL:
        if acik and not k["acik"]:
            continue
        out[k["ad"]] = _so7_kiyas(k["d"](m, p, E), k["s"](m, p, E), k["yon"], tol)
    if not acik:
        for sn, kl in SO7_SINIF.items():
            r = None
            for k in kl:
                v = _so7_kiyas(k["d"](m, p, E), k["s"](m, p, E), k["yon"], tol)
                out[k["ad"]] = v
                r = v if r is None else (r & v)
            out[sn] = r & out["Z5"] if sn == "YOL" else r
    return out


def _so7_tamam(m: Dict[str, Any], p: Dict[str, Any], E: Dict[str, Any], acik: bool = False, tol: float = 0.0) -> Any:
    """Bütün şartlar (açıkken yalnız Z1, Z2, Z6; açılışta Z1-Z6 + sınıf DİP ya da YOL ÜSTÜ)."""
    r = _so7_kural_sonuc(m, p, E, acik, tol)
    ok = None
    for k in SO7_KURAL:
        if k["ad"] in r:
            ok = r[k["ad"]] if ok is None else (ok & r[k["ad"]])
    if not acik:
        ok = ok & (r["DIP"] | r["YOL"])
    return ok


def _so7_sinif(m: Dict[str, Any], p: Dict[str, Any], E: Dict[str, Any]) -> str:
    r = _so7_kural_sonuc(m, p, E)
    return "DIP" if bool(r["DIP"]) else ("YOL" if bool(r["YOL"]) else "")


def so_s7_bolgeler(d: pd.DataFrame, pazar: str, prm: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None, sembol: str = "",
                   A: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """S7 bölge listesi (Pine COL_S7_BOLGE.pine birebir ikizi). d = SY.sy_veri_hazirla çıktısı (geçerli barlar).
    BOŞTA: e'de [e-Lmin+1, e] sınanır; geçerse başlangıç e-Lmax+1'e kadar geriye uzatılır (bütün şartları geçen EN ERKEN s), onay = e.
    AÇIK: her yeni barda önce kırılım (C > üst x 1,01 YUKARI / C < alt x 0,99 AŞAĞI; kırılım mumu bölgeye girmez), yoksa bar eklenir ve Z1, Z2, Z6
    yeniden sınanır; bozulursa 'sönme' (bölge son geçerli günde biter). Yeni bölge s > kilit (bitişi tetikleyen bar)."""
    E = E or SO7_ESIK
    p = _so7_prm(prm or E["secilen"], pazar)
    A = A if A is not None else _so7_diziler(d, E)
    n = A["n"]; Lmin = p["Lmin"]; Lmax = int(E["Lmax"]); smin = _so7_smin(E); kir = float(E["kirilim"])
    if Lmin < 3 or Lmax < Lmin:
        raise S7Hata(f"S7: Lmin {Lmin} / Lmax {Lmax} geçersiz")
    if n < max(E["gecmis_min"] + 1, smin + Lmin):
        return []
    V = _so7_olcu_vek(A, Lmin, E)
    idx = np.arange(n)
    aday = np.asarray(_so7_tamam(V, p, E, tol=1e-9), bool) & (idx >= E["gecmis_min"]) & (idx - Lmin + 1 >= smin)
    ad = np.flatnonzero(aday)
    C = A["C"]; T = A["tarih"]
    out: List[Dict[str, Any]] = []
    kilit = -1; j = 0
    while j < len(ad):
        e = int(ad[j]); s0 = e - Lmin + 1
        if s0 <= kilit:
            j = int(np.searchsorted(ad, kilit + Lmin)); continue
        m0 = _so7_olcu(A, s0, e, E)
        if not bool(_so7_tamam(m0, p, E)):
            j += 1; continue
        bas = s0
        s_alt = max(e - Lmax + 1, smin, kilit + 1)
        for s2 in range(s0 - 1, s_alt - 1, -1):                                         # tamamı taranır; geçen en erken s seçilir
            if bool(_so7_tamam(_so7_olcu(A, s2, e, E), p, E)):
                bas = s2
        m = m0 if bas == s0 else _so7_olcu(A, bas, e, E)
        sinif = _so7_sinif(m, p, E)
        ust, alt, son, tur, k = m["ust"], m["alt"], e, "AÇIK", e + 1
        while k < n:
            c = C[k]
            if c > ust * (1.0 + kir):
                tur = "YUKARI"; break
            if c < alt * (1.0 - kir):
                tur = "AŞAĞI"; break
            mk = _so7_olcu(A, bas, k, E, acik=True)
            if not bool(_so7_tamam(mk, p, E, acik=True)):
                tur = "sönme"; break
            ust, alt, son = mk["ust"], mk["alt"], k
            k += 1
        kilit = k
        out.append({"sembol": sembol, "pazar": pazar, "s_i": bas, "e_i": e, "son_i": son, "kilit_i": k,
                    "bas": str(pd.Timestamp(T[bas]).date()), "onay": str(pd.Timestamp(T[e]).date()), "bitis": str(pd.Timestamp(T[son]).date()),
                    "kilit_tarih": str(pd.Timestamp(T[k]).date()) if k < n else "-", "tur": tur, "sinif": sinif,
                    "L": son - bas + 1, "L_onay": e - bas + 1, "onay_sonrasi": son - e, "R": m["R"],
                    "z1_R": m["z1"] / m["R"], "z2_ikinci_R": m["z2_ikinci"] / m["R"], "z2_max_R": m["z2_max"] / m["R"], "z3": m["band"], "z4": m["egim"],
                    "z5_oran": m["z5_son"] / m["z5_ilk"] - 1.0, "z6p": m["z6p"], "konum": m["konum"], "tepe": m["tepe"],
                    "ust_onay": m["ust"], "alt_onay": m["alt"], "ust": ust, "alt": alt})
        j = int(np.searchsorted(ad, kilit + Lmin))
    return out


def so_s7_son_bar(d: pd.DataFrame, pazar: str, prm: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Pine bilgi tablosunun Python karşılığı: son barda açık bölge varsa [s, son], yoksa [son-Lmin+1, son] penceresinin Z1-Z6 değer / şartı."""
    E = E or SO7_ESIK; p = _so7_prm(prm or E["secilen"], pazar); A = _so7_diziler(d, E)
    B = so_s7_bolgeler(d, pazar, prm, E, A=A); n = A["n"]
    acik = B[-1] if B and B[-1]["tur"] == "AÇIK" else None
    s = acik["s_i"] if acik else n - p["Lmin"]
    m = _so7_olcu(A, s, n - 1, E)
    return {"pencere": [str(pd.Timestamp(A["tarih"][s]).date()), str(pd.Timestamp(A["tarih"][n - 1]).date())], "acik_gun": (n - acik["s_i"]) if acik else 0,
            "olcu": m, "sart": {k: bool(v) for k, v in _so7_kural_sonuc(m, p, E).items()}, "sinif": _so7_sinif(m, p, E)}


# ---- S5 / S6 kutuları (COL_S6_TASLAK.pine bölge makinesi; S5 ön ayarı N = 1) — sayım kıyası için
def so_s7_kutu_s56(d: pd.DataFrame, pazar: str, onayar: str = "S6", X: Optional[pd.DataFrame] = None, sembol: str = "") -> List[Dict[str, Any]]:
    """COL_S6_TASLAK.pine bölge kuralları (koşu N gün -> onay; kutu bant 1 uç gün hariç; kırılım %1 önce; koşul düşerse sönme). onayar 'S6' (varsayılan
    taslak) ya da 'S5' (so_s5 ön kayıt eşikleri, N = 1). Bölge uzunluğu = koşul günleri (başlangıç .. son koşul günü; kırılım mumu hariç)."""
    if onayar not in ("S5", "S6"):
        raise S7Hata(f"so_s7_kutu_s56: ön ayar {onayar}")
    X = X if X is not None else SO.so_s5(d, pazar)
    C = d.Close.to_numpy(float); n = len(C); T = d.index
    gm = SO.SO_ESIK["gecmis_min"]; ok_g = np.arange(n) >= gm
    sinif = (X.dip.to_numpy(bool) | X.yol.to_numpy(bool))
    if onayar == "S5":
        kos = X.cek.to_numpy(bool) & sinif; N = 1
    else:
        S6 = SO7_S6
        with np.errstate(invalid="ignore"):
            kos = (X.ca.to_numpy(bool) & X.cb.to_numpy(bool) & X.cd.to_numpy(bool) & ok_g & sinif
                   & (X.egim.to_numpy() >= S6["egim"][0]) & (X.egim.to_numpy() <= S6["egim"][1]) & (X.bbp.to_numpy() <= S6["bb"])
                   & (X.net.to_numpy() >= S6["net_alt"]))
        N = int(S6["N"])
    dip = X.dip.to_numpy(bool)
    kp = 0.01
    out: List[Dict[str, Any]] = []
    akt = False; kosu = 0; zC: List[float] = []; zU = zA = float("nan"); bas = son = 0; zs = ""

    def _bant(z: List[float]) -> Tuple[float, float]:
        w = sorted(z); m_ = len(w); u_, a_ = w[-1], w[0]
        if m_ >= 3:
            if w[-2] / w[0] <= w[-1] / w[1]:
                u_ = w[-2]
            else:
                a_ = w[1]
        return u_, a_

    for i in range(n):
        bitti = False
        if akt:
            if C[i] > zU * (1 + kp) or C[i] < zA * (1 - kp):
                out.append({"sembol": sembol, "bas": str(T[bas].date()), "onay": str(T[on].date()), "bitis": str(T[son].date()),
                            "tur": "YUKARI" if C[i] > zU * (1 + kp) else "AŞAĞI", "sinif": zs, "L": son - bas + 1, "ust": zU, "alt": zA})
                akt = False; kosu = 0; bitti = True
            elif kos[i]:
                zC.append(C[i]); zU, zA = _bant(zC); son = i
            else:
                out.append({"sembol": sembol, "bas": str(T[bas].date()), "onay": str(T[on].date()), "bitis": str(T[son].date()), "tur": "sönme",
                            "sinif": zs, "L": son - bas + 1, "ust": zU, "alt": zA})
                akt = False; kosu = 0
        if not akt and not bitti:
            kosu = kosu + 1 if kos[i] else 0
            if kosu >= N and i + 1 >= N:
                zC = list(C[i - N + 1:i + 1]); zU, zA = _bant(zC)
                bas = i - N + 1; on = i; son = i; zs = "DIP" if dip[i] else "YOL"; akt = True
    if akt:
        out.append({"sembol": sembol, "bas": str(T[bas].date()), "onay": str(T[on].date()), "bitis": str(T[son].date()), "tur": "AÇIK", "sinif": zs,
                    "L": son - bas + 1, "ust": zU, "alt": zA})
    return out


# ---- TASARIM SINAMASI (getirisiz; ön yazımdan SONRA)
def so_s7_tasarim_sozluk() -> Dict[str, Any]:
    """Ön yazım mührünün kapsamı: ızgara, seçim / örnek kuralı, örnekler, tampon, örtüşme, eşikler ('secilen' hariç), kural tablosu metni."""
    return {"izgara": SO7_IZGARA, "ornek": SO7_ORNEK, "tampon": SO7_TAMPON, "ortusme": SO7_ORTUSME,
            "esik": {k: v for k, v in SO7_ESIK.items() if k != "secilen"},
            "kural": [{k: v for k, v in r.items() if k not in ("d", "s")} for r in SO7_KURAL],
            "sinif": {sn: [{k: v for k, v in r.items() if k not in ("d", "s")} for r in kl] for sn, kl in SO7_SINIF.items()}}


def so_s7_muhur() -> str:
    return hashlib.sha256(json.dumps(so_s7_tasarim_sozluk(), sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")).hexdigest()


def _so7_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or SO.SO_YOL["cikti"], SO7_DOSYA.get(ad, ad))


def so_s7_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = SO7_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def _so7_kural_md() -> List[str]:
    s = ["| şart | eşik | yön | açıkken yeniden sınanır | açıklama |", "|---|---|---|---|---|"]
    for k in SO7_KURAL:
        s.append(f"| {k['ad']} | {k['esik']} | {k['yon']} | {'EVET' if k['acik'] else 'hayır'} | {k['aciklama']} |")
    for sn, kl in SO7_SINIF.items():
        for k in kl:
            s.append(f"| {sn}:{k['ad']} | {k['esik']} | {k['yon']} | hayır (onayda sabit) | {k['aciklama']} |")
    return s


def so_s7_on_yazim(cikti: Optional[str] = None, uzerine: bool = False) -> str:
    """S7_TASARIM.md ön yazım bloğu (ölçümden ÖNCE): eşikler, kural tablosu, ızgara, seçim / örnek kuralı, örnekler, kontrol listesi, mühür + UTC zaman."""
    yol = _so7_yol("tasarim", cikti)
    if os.path.exists(yol) and not uzerine:
        raise S7Hata(f"S7 ön yazım zaten var ({yol}); üzerine yazılmaz")
    E = SO7_ESIK; V = E["varsayilan"]
    s = ["# S7 — BÖLGE İÇİNDEN ÖLÇÜLEN SIKIŞMA KUTUSU: TASARIM SINAMASI VE SAYIM", "", SO7_SURUM, "",
         "Göz aracıdır: getiri / kazanç ölçülmez, iddia yoktur. Pine: COL_S7_BOLGE.pine; Python ikizi: SIKISMA_OBEK.py so_s7_bolgeler.", "",
         "## ÖN YAZIM (s7tasarim koşmadan ÖNCE yazıldı; bu blok sonradan değişmez)", "",
         f"- ZAMAN (UTC): `{_s7_simdi()}`", f"- ÖN YAZIM MÜHÜR (so_s7_muhur sha256): `{so_s7_muhur()}`",
         f"- Varsayılan: k_m {V['k_m']}, bb {V['bb']}, Lmin {V['Lmin']}, Lmax {E['Lmax']}, bant BIST %{V['bant']['BIST'] * 100:.0f} / ABD-AVR "
         f"%{V['bant']['ABD'] * 100:.0f}, eğim [{V['egim'][0] * 100:+.0f}%, {V['egim'][1] * 100:+.0f}%].",
         f"- R (normal gün) = bölge başlangıcı s'den ÖNCEKİ {E['R_gun']} geçerli barın (H-L) / önceki kapanış MEDYANI (bölge ve sonrası girmez).",
         f"- Geçerli bar: {E['gecerli_bar']}. İlk {E['gecmis_min']} geçerli barda (indeks < {E['gecmis_min']}) onay yok; en erken başlangıç s >= {_so7_smin(E)}.",
         f"- Kırılım payı %{E['kirilim'] * 100:.0f}; {E['kilit']}.", f"- Z5 bölünmesi: {E['z5_son']}.", "",
         "### Kural tablosu (KURAL MOTORU, SO7_KURAL / SO7_SINIF)", ""] + _so7_kural_md() + [
         "", "Bölge = Z1..Z6 VE (DİP ya da YOL ÜSTÜ). Sınıfsız bölge kutu olmaz.", "",
         "### Algoritma", "",
         "- BOŞTA: her geçerli bar e'de [e-Lmin+1, e] sınanır. Geçerse bölge AÇILIR; başlangıç s' = s-1 .. max(e-Lmax+1, en erken s, kilit+1) "
         "arasında bütün şartları geçen EN ERKEN s' (tamamı taranır). Onay günü = e. Sınıf, R, BBW referansı s'ye göre ve onayda sabit.",
         "- AÇIK: her yeni barda önce kırılım (kapanış > üst x 1,01 YUKARI; < alt x 0,99 AŞAĞI; kırılım mumu bölgeye girmez). Yoksa bar eklenir, "
         "Z1, Z2, Z6 yeniden sınanır; bozulursa bölge son geçerli günde 'sönme' ile biter. Üst / alt = Z3'teki 1 uç gün hariç bant (her eklemede "
         "yeniden). Lmax aşılırsa bölge sürer, başlangıç sabit.",
         "- Bölge bitince yeni bölge için bitiş barından (kırılım mumu / sönmeyi tetikleyen bar) SONRA en az Lmin yeni bar gerekir.", "",
         "### Izgara ve seçim (ölçümden önce)", "",
         f"- Izgara: k_m {SO7_IZGARA['k_m']} x bb {SO7_IZGARA['bb']} x Lmin {SO7_IZGARA['Lmin']} x bant BIST "
         f"{[b['BIST'] for b in SO7_IZGARA['bant']]} x eğim {SO7_IZGARA['egim']} = "
         f"{len(SO7_IZGARA['k_m']) * len(SO7_IZGARA['bb']) * len(SO7_IZGARA['Lmin']) * len(SO7_IZGARA['bant']) * len(SO7_IZGARA['egim'])} nokta. "
         f"{SO7_IZGARA['bant_eslesme']}.",
         f"- Seçim kuralı: {SO7_IZGARA['secim_kurali']}", f"- Örnek kuralı: {SO7_IZGARA['ornek_kurali']}", "",
         "| örnek | hisse | aralık | tür | beklenen sınıf |", "|---|---|---|---|---|"]
    s += [f"| {o['ad']} | {o['sembol']} | {o['ilk']} .. {o['son']} | {'SEÇMELİ' if o['secmeli'] else 'SEÇMEMELİ (±' + str(SO7_TAMPON) + ' bar)'} | {o['beklenen']} |"
          for o in SO7_ORNEK]
    s += ["", "- Örnek sayısı 3 + 5: aşırı uyum riski yüksek; sonuç 'bulgu' değildir, Cemal'in gözüyle sınanır.",
          "- Bilgi (karar yok): kalibre_etiketler.csv (çöl + olumsuz etiketler; uzun çöller, farklı ölçek) her etikette S7 örtüşmesi.",
          "- Sayım (seçilen noktayla, getiri YOK): BIST / ABD / AVR; 100 hisse-yılda bölge, uzunluk medyan / çeyrek, sınıf ve bitiş türü payı, 1-4 günlük "
          "bölge payı; S5 kutuları (N = 1) ve S6 varsayılanı aynı evrende yan yana.", "", so_s7_kontrol_tablosu(), "", SO7_ON_YAZIM_SONU, ""]
    metin = "\n".join(s)
    if _S7_EPOSTA.search(metin):
        raise S7Hata("S7 ön yazımında e-posta biçimli parça var")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    s7log.info("S7 ön yazım yazıldı: %s (mühür %s)", yol, so_s7_muhur()[:12])
    return yol


def _so7_on_yazim_oku(cikti: Optional[str] = None) -> Tuple[str, Dict[str, str]]:
    yol = _so7_yol("tasarim", cikti)
    if not os.path.exists(yol):
        raise S7Hata(f"S7 ön yazım yok ({yol}): önce `python SIKISMA_OBEK.py s7onyazim`")
    metin = open(yol, encoding="utf-8").read()
    if SO7_ON_YAZIM_SONU not in metin:
        raise S7Hata("S7 ön yazım bozuk: bitiş işareti yok")
    blok = metin.split(SO7_ON_YAZIM_SONU)[0] + SO7_ON_YAZIM_SONU + "\n"
    mh = re.search(r"ÖN YAZIM MÜHÜR \(so_s7_muhur sha256\): `([0-9a-f]{64})`", blok)
    zm = re.search(r"ZAMAN \(UTC\): `([^`]+)`", blok)
    if not mh or not zm:
        raise S7Hata("S7 ön yazım bozuk: mühür / zaman yok")
    if mh.group(1) != so_s7_muhur():
        raise S7Hata("S7 ön yazım mührü tutmuyor: ızgara / kural / eşik ön yazımdan sonra değişmiş (eşik oynanmaz), durdu")
    return blok, {"muhur": mh.group(1), "zaman": zm.group(1)}


def _so7_bistveri(semboller: List[str], veri: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    yol = os.path.join(veri or SO.SO_YOL["veri"], "V_BIST.pkl")
    if not os.path.exists(yol):
        raise S7Hata(f"V_BIST yok: {yol} (python FON_IZI.py vpac /tmp/iv/veri /tmp/veri)")
    Vb = pd.read_pickle(yol)
    Vb = Vb["veri"] if isinstance(Vb, dict) and "veri" in Vb and isinstance(Vb["veri"], dict) else Vb
    return {s: SY.sy_veri_hazirla(Vb[s], SY.SY_ESIK) for s in semboller if s in Vb}


def _so7_aralik(T: pd.Index, ilk: str, son: str) -> Tuple[int, int]:
    a = int(np.searchsorted(T.values, np.datetime64(pd.Timestamp(ilk)), side="left"))
    b = int(np.searchsorted(T.values, np.datetime64(pd.Timestamp(son)), side="right")) - 1
    return a, b


def so_s7_ornek_sina(B: List[Dict[str, Any]], T: pd.Index, o: Dict[str, Any]) -> Dict[str, Any]:
    """Bir örnekte S7 bölgelerinin sınaması (örnek kuralı SO7_IZGARA['ornek_kurali'])."""
    a, b = _so7_aralik(T, o["ilk"], o["son"])
    if b < a:
        return {"tutar": False, "neden": "örnek aralığında bar yok"}
    if o["secmeli"]:
        en, bi = 0, None
        for r in B:
            k = min(b, r["son_i"]) - max(a, r["s_i"]) + 1
            if k > en:
                en, bi = k, r
        if bi is None:
            return {"tutar": False, "bulundu": False, "ortusme": 0.0, "bolge": None, "uzunluk": b - a + 1}
        ort = en / (b - a + 1)
        return {"tutar": bool(ort >= SO7_ORTUSME and bi["sinif"] == o["beklenen"]), "bulundu": True, "ortusme": ort, "sinif": bi["sinif"],
                "bas_fark": bi["s_i"] - a, "bit_fark": bi["son_i"] - b, "bolge": {k: bi[k] for k in ("bas", "onay", "bitis", "tur", "sinif", "L")},
                "uzunluk": b - a + 1}
    ta, tb = a - SO7_TAMPON, b + SO7_TAMPON
    kes = [r for r in B if r["s_i"] <= tb and r["son_i"] >= ta]
    return {"tutar": not kes, "kesisen": [{k: r[k] for k in ("bas", "onay", "bitis", "tur", "sinif", "L")} for r in kes], "uzunluk": b - a + 1}


def so_s7_tasarim(veri: Optional[str] = None, cikti: Optional[str] = None, yaz: bool = True) -> Dict[str, Any]:
    """Izgaranın 72 noktasında 8 örneği V_BIST ile sınar (getirisiz); seçim kuralıyla noktayı seçer. Ön yazım mührü tutmazsa durur."""
    blok, oy = _so7_on_yazim_oku(cikti)
    Z = SO7_IZGARA; V0 = SO7_ESIK["varsayilan"]
    D = _so7_bistveri(sorted({o["sembol"] for o in SO7_ORNEK}), veri)
    eksik = sorted({o["sembol"] for o in SO7_ORNEK} - set(D))
    if eksik:
        raise S7Hata(f"S7 tasarım: V_BIST'te yok: {eksik}")
    AA = {s: _so7_diziler(d) for s, d in D.items()}
    noktalar = []
    for km, bb, lm, bi, gi in itertools.product(Z["k_m"], Z["bb"], Z["Lmin"], range(len(Z["bant"])), range(len(Z["egim"]))):
        prm = {"k_m": km, "bb": bb, "Lmin": lm, "bant": Z["bant"][bi], "egim": Z["egim"][gi]}
        B = {s: so_s7_bolgeler(D[s], "BIST", prm, sembol=s, A=AA[s]) for s in D}
        son = {o["ad"]: so_s7_ornek_sina(B[o["sembol"]], D[o["sembol"]].index, o) for o in SO7_ORNEK}
        fark = int(km != V0["k_m"]) + int(bb != V0["bb"]) + int(lm != V0["Lmin"]) + int(Z["bant"][bi] != V0["bant"]) + int(Z["egim"][gi] != V0["egim"])
        noktalar.append({"prm": prm, "tutan": sum(v["tutar"] for v in son.values()), "fark": fark,
                         "sira": (fark, km, bb, -lm, bi, -gi), "sonuc": son, "kacan": [k for k, v in son.items() if not v["tutar"]]})
    en_cok = max(n_["tutan"] for n_ in noktalar)
    aday = [n_ for n_ in noktalar if n_["tutan"] == en_cok]
    sec = sorted(aday, key=lambda n_: n_["sira"])[0]
    vars_ = next(n_ for n_ in noktalar if n_["fark"] == 0)
    J = {"zaman_utc": _s7_simdi(), "on_yazim": oy, "surum": SO7_SURUM, "kod_dosyasi": "SIKISMA_S7.py", "komut": "python SIKISMA_S7.py s7tasarim", "nokta_sayisi": len(noktalar), "en_cok_tutan": en_cok, "toplam": len(SO7_ORNEK),
         "tam_tutan_nokta": sum(n_["tutan"] == len(SO7_ORNEK) for n_ in noktalar), "aday_nokta": len(aday), "secilen": sec["prm"],
         "secilen_sonuc": sec["sonuc"], "secilen_kacan": sec["kacan"], "varsayilan_sonuc": vars_["sonuc"], "varsayilan_tutan": vars_["tutan"],
         "noktalar": [{"prm": n_["prm"], "tutan": n_["tutan"], "fark": n_["fark"], "kacan": n_["kacan"]} for n_ in noktalar]}
    # BİLGİ: kalibre_etiketler.csv (karar yok)
    J["kalibre"] = so_s7_kalibre(sec["prm"], veri)
    # Pine için beklenen kutular (seçilen nokta)
    Bsec = {s: so_s7_bolgeler(D[s], "BIST", sec["prm"], sembol=s, A=AA[s]) for s in D}
    J["beklenen"] = so_s7_beklenen(Bsec, D)
    if yaz:
        _so7_json_yaz(J, cikti)
        so_s7_md_yaz(cikti)
        s7log.info("S7 tasarım: en çok tutan %d / %d; 8/8 nokta %d; seçilen %s", en_cok, len(SO7_ORNEK), J["tam_tutan_nokta"], sec["prm"])
    return J


def so_s7_beklenen(B: Dict[str, List[Dict[str, Any]]], D: Dict[str, pd.DataFrame], pay: int = 20) -> List[Dict[str, Any]]:
    """Her örnek için [ilk - 20, son + 20] geçerli bar penceresiyle kesişen S7 kutuları (Pine'da karşılaştırma)."""
    out = []
    for o in SO7_ORNEK:
        T = D[o["sembol"]].index; a, b = _so7_aralik(T, o["ilk"], o["son"])
        kes = [r for r in B[o["sembol"]] if r["s_i"] <= b + pay and r["son_i"] >= a - pay]
        out.append({"ornek": o["ad"], "sembol": o["sembol"], "ilk": o["ilk"], "son": o["son"], "secmeli": o["secmeli"], "beklenen": o["beklenen"],
                    "kutular": [{k: r[k] for k in ("bas", "onay", "bitis", "kilit_tarih", "tur", "sinif", "L", "ust", "alt", "R")} for r in kes]})
    return out


def so_s7_kalibre(prm: Dict[str, Any], veri: Optional[str] = None, yol: Optional[str] = None) -> List[Dict[str, Any]]:
    """BİLGİ: kalibre_etiketler.csv her etiket için S7 bölgeleri (karar yok). Veri yoksa 'veri yok'."""
    yol = yol or os.path.join(KOK_S7, "kalibre_etiketler.csv")
    if not os.path.exists(yol):
        return [{"hata": f"etiket dosyası yok: {yol}"}]
    K = pd.read_csv(yol)
    D = _so7_bistveri(sorted(set(K.sembol.astype(str))), veri)
    BB = {s: so_s7_bolgeler(d, "BIST", prm, sembol=s) for s, d in D.items()}
    out = []
    for r in K.itertuples():
        s = str(r.sembol)
        if s not in D:
            out.append({"sembol": s, "bas": r.bas, "son": r.son, "etiket": r.sinif, "durum": "veri yok"}); continue
        T = D[s].index; a, b = _so7_aralik(T, r.bas, r.son)
        if b < a:
            out.append({"sembol": s, "bas": r.bas, "son": r.son, "etiket": r.sinif, "durum": "aralıkta bar yok"}); continue
        kes = [x for x in BB[s] if x["s_i"] <= b and x["son_i"] >= a]
        kap = np.zeros(b - a + 1, bool)
        for x in kes:
            kap[max(a, x["s_i"]) - a:min(b, x["son_i"]) - a + 1] = True
        en = max([min(b, x["son_i"]) - max(a, x["s_i"]) + 1 for x in kes], default=0)
        out.append({"sembol": s, "bas": r.bas, "son": r.son, "etiket": r.sinif, "durum": "ok", "uzunluk": b - a + 1, "bolge_sayisi": len(kes),
                    "kapsama": float(kap.mean()), "en_iyi_ortusme": en / (b - a + 1), "siniflar": "/".join(sorted({x["sinif"] for x in kes})) or "-",
                    "bolgeler": "; ".join(f"{x['bas']}..{x['bitis']} {x['sinif']} {x['tur']}" for x in kes)})
    return out


def _so7_json_yaz(J: Dict[str, Any], cikti: Optional[str] = None) -> None:
    y = _so7_yol("tasarim_json", cikti)
    eski = json.load(open(y, encoding="utf-8")) if os.path.exists(y) else {}
    eski.update(J)
    os.makedirs(os.path.dirname(y), exist_ok=True)
    SC._sc_json(y, SC._sc_temiz(eski))


# ---- SAYIM (getirisiz; seçilen noktayla)
def _so7_ozet(L: np.ndarray, siniflar: List[str], turler: List[str], hy: float) -> Dict[str, Any]:
    n = len(L)
    q = np.percentile(L, [25, 50, 75]) if n else [np.nan] * 3
    sin = pd.Series(siniflar).value_counts(normalize=True).to_dict() if n else {}
    tur = pd.Series(turler).value_counts(normalize=True).to_dict() if n else {}
    return {"n": n, "hisse_yil": hy, "yuz_hy": n / hy * 100 if hy else np.nan, "L_q25": float(q[0]), "L_med": float(q[1]), "L_q75": float(q[2]),
            "pay_1_4": float(np.mean(L <= 4)) if n else np.nan, "pay_1": float(np.mean(L == 1)) if n else np.nan,
            "sinif": {k: float(v) for k, v in sin.items()}, "tur": {k: float(v) for k, v in tur.items()}}


def _so7_hisse_say(arg: Tuple[str, pd.DataFrame, str, Dict[str, Any]]) -> Dict[str, Any]:
    s, d, pazar, prm = arg
    try:
        n = len(d); hy = max(0, n - SO.SO_ESIK["gecmis_min"]) / 252.0
        B7 = so_s7_bolgeler(d, pazar, prm, sembol=s)
        X = SO.so_s5(d, pazar)
        B5 = so_s7_kutu_s56(d, pazar, "S5", X, s); B6 = so_s7_kutu_s56(d, pazar, "S6", X, s)
        ev = X.ev5.to_numpy(bool); bs = SO.so_bolge_sonu(ev, X.s5c.to_numpy(bool), SO.SO_ESIK["S5"]["ara"])
        B5o = [{"L": int(bs[i] - i + 1), "sinif": "DIP" if X.s5c_dip.iat[i] else "YOL", "tur": "-"} for i in np.flatnonzero(ev)]
        return {"s": s, "hy": hy, "S7": [{k: r[k] for k in ("L", "sinif", "tur", "onay_sonrasi", "L_onay")} for r in B7],
                "S5": [{k: r[k] for k in ("L", "sinif", "tur")} for r in B5], "S6": [{k: r[k] for k in ("L", "sinif", "tur")} for r in B6], "S5o": B5o}
    except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer
        s7log.warning("S7 sayım %s %s atlandı: %s", pazar, s, ex)
        return {"s": s, "hy": 0.0, "S7": [], "S5": [], "S6": [], "S5o": [], "hata": str(ex)}


def so_s7_sayim(veri: Optional[str] = None, cikti: Optional[str] = None, pazarlar: Tuple[str, ...] = SO.SO_PAZAR, yaz: bool = True,
                isci: int = 2) -> Dict[str, Any]:
    """BIST / ABD / AVR: S7 (seçilen nokta), S5 kutusu (N = 1), S5 ölçüm bölgesi (ev5 .. bölge sonu, 20 bar birleştirme), S6 varsayılanı. Getiri YOK."""
    ty = _so7_yol("tasarim_json", cikti)
    if not os.path.exists(ty):
        raise S7Hata("S7 sayım: tasarım yok (önce s7tasarim)")
    TJ = json.load(open(ty, encoding="utf-8"))
    if json.dumps(TJ.get("secilen"), sort_keys=True) != json.dumps(SO7_ESIK["secilen"], sort_keys=True):
        raise S7Hata(f"S7 sayım: SO7_ESIK secilen {SO7_ESIK['secilen']} tasarımın seçtiğinden ({TJ.get('secilen')}) farklı")
    _so7_on_yazim_oku(cikti)
    prm = SO7_ESIK["secilen"]; out: Dict[str, Any] = {"zaman_utc": _s7_simdi(), "secilen": prm, "pazar": {}, "kod_dosyasi": "SIKISMA_S7.py",
                                                      "komut": "python SIKISMA_S7.py s7sayim"}
    t0 = time.time()
    for p in pazarlar:
        V = SY.sy_veri_yukle(p, SY.SY_ESIK, veri or SO.SO_YOL["veri"])
        args = [(s, d, p, prm) for s, d in V.items()]
        if isci > 1:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(isci) as pool:
                R = pool.map(_so7_hisse_say, args, chunksize=8)
        else:
            R = [_so7_hisse_say(a) for a in args]
        hy = float(sum(r["hy"] for r in R))
        o: Dict[str, Any] = {"hisse": len(R), "hata": sum(1 for r in R if "hata" in r)}
        for t in ("S5", "S5o", "S6", "S7"):
            Bt = [b for r in R for b in r[t]]
            o[t] = _so7_ozet(np.array([b["L"] for b in Bt], float), [b["sinif"] for b in Bt], [b["tur"] for b in Bt], hy)
        B7 = [b for r in R for b in r["S7"]]
        os_ = np.array([b["onay_sonrasi"] for b in B7], float)
        o["S7"]["onay_sonrasi_med"] = float(np.median(os_)) if len(os_) else np.nan
        o["S7"]["onay_sonrasi_0_3"] = float(np.mean(os_ <= 3)) if len(os_) else np.nan
        o["S7"]["L_onay_med"] = float(np.median([b["L_onay"] for b in B7])) if B7 else np.nan
        out["pazar"][p] = o
        s7log.info("S7 sayım %s: %d hisse, S7 %d, S5 %d, S6 %d (%.0f sn)", p, len(R), o["S7"]["n"], o["S5"]["n"], o["S6"]["n"], time.time() - t0)
        del V
    out["sure_sn"] = round(time.time() - t0, 1)
    if yaz:
        _so7_json_yaz({"sayim": out}, cikti)
        so_s7_md_yaz(cikti)
    return out


# ---- MD / PINE BLOĞU
def _so7_y(x: Any, k: int = 0) -> str:
    return "-" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f"%{x * 100:.{k}f}"


def so_s7_md_yaz(cikti: Optional[str] = None) -> str:
    """S7_TASARIM.md: ön yazım bloğu AYNEN + s7_tasarim.json'dan sonuç, bilgi ve sayım bölümleri."""
    blok, oy = _so7_on_yazim_oku(cikti)
    J = json.load(open(_so7_yol("tasarim_json", cikti), encoding="utf-8"))
    s = [blok.rstrip("\n"), "", SO7_SAPMA_NOTU, ""]
    if "secilen" in J:
        sp = J["secilen"]
        s += ["## TASARIM SONUCU (ön yazımdan sonra koşuldu; V_BIST)", "", f"- Koşu (UTC): `{J['zaman_utc']}`; ön yazım zamanı `{oy['zaman']}`.",
              f"- En çok tutan {J['en_cok_tutan']} / {J['toplam']}; 8/8 tutan nokta {J['tam_tutan_nokta']} / {J['nokta_sayisi']}; en çok tutan nokta {J['aday_nokta']}.",
              f"- **SEÇİLEN:** k_m {sp['k_m']}, bb {sp['bb']}, Lmin {sp['Lmin']}, bant BIST %{sp['bant']['BIST'] * 100:.0f} / ABD-AVR %{sp['bant']['ABD'] * 100:.0f}, "
              f"eğim [{sp['egim'][0] * 100:+.0f}%, {sp['egim'][1] * 100:+.0f}%]. Kaçan: {', '.join(J['secilen_kacan']) or 'YOK'}.",
              f"- Varsayılan noktada tutan {J['varsayilan_tutan']} / {J['toplam']}.", "",
              "| örnek | tür | sonuç | bulunan bölge (başlangıç .. bitiş, onay) | sınıf | örtüşme | başlangıç farkı (bar) | bitiş farkı (bar) |",
              "|---|---|---|---|---|---|---|---|"]
        for o in SO7_ORNEK:
            v = J["secilen_sonuc"][o["ad"]]
            if o["secmeli"]:
                bg = v.get("bolge") or {}
                s.append(f"| {o['ad']} {o['ilk']}..{o['son']} | SEÇ {o['beklenen']} | {'TUTTU' if v['tutar'] else 'KAÇTI'} | "
                         + (f"{bg.get('bas')} .. {bg.get('bitis')} (onay {bg.get('onay')}, {bg.get('tur')})" if bg else "bölge yok")
                         + f" | {v.get('sinif', '-')} | {_so7_y(v.get('ortusme'))} | {v.get('bas_fark', '-')} | {v.get('bit_fark', '-')} |")
            else:
                ks = "; ".join(f"{x['bas']}..{x['bitis']} {x['sinif']}" for x in v.get("kesisen", [])) or "yok"
                s.append(f"| {o['ad']} {o['ilk']}..{o['son']} | SEÇME (±{SO7_TAMPON}) | {'TUTTU' if v['tutar'] else 'KAÇTI'} | tampondaki bölge: {ks} | - | - | - | - |")
        s += ["", "### Bütün ızgara (tutan / 8, varsayılandan fark, kaçanlar)", "", "| k_m | bb | Lmin | bant BIST | eğim | tutan | fark | kaçan |", "|---|---|---|---|---|---|---|---|"]
        for n_ in J["noktalar"]:
            q = n_["prm"]
            s.append(f"| {q['k_m']} | {q['bb']} | {q['Lmin']} | {q['bant']['BIST']:.2f} | [{q['egim'][0]:+.2f}, {q['egim'][1]:+.2f}] | {n_['tutan']} | {n_['fark']} | "
                     f"{', '.join(n_['kacan']) or '-'} |")
        s += ["", "Not: 3 + 5 örnek; aşırı uyum riski yüksek. Seçilen nokta Cemal'in gözüyle (TradingView) ileri sınanır; eşik bu sonuçtan sonra oynanmaz.", ""]
    if J.get("kalibre"):
        s += ["## BİLGİ: kalibre_etiketler.csv (karar yok; uzun çöller, farklı ölçek)", "",
              "| hisse | aralık | etiket | durum | bar | S7 bölgesi | kapsama | en iyi örtüşme | sınıflar | bölgeler |", "|---|---|---|---|---|---|---|---|---|---|"]
        for r in J["kalibre"]:
            if r.get("durum") != "ok":
                s.append(f"| {r.get('sembol')} | {r.get('bas')}..{r.get('son')} | {r.get('etiket')} | {r.get('durum', r.get('hata'))} | - | - | - | - | - | - |"); continue
            s.append(f"| {r['sembol']} | {r['bas']}..{r['son']} | {r['etiket']} | ok | {r['uzunluk']} | {r['bolge_sayisi']} | {_so7_y(r['kapsama'])} | "
                     f"{_so7_y(r['en_iyi_ortusme'])} | {r['siniflar']} | {r['bolgeler'] or '-'} |")
        ok_ = [r for r in J["kalibre"] if r.get("durum") == "ok"]
        for et in sorted({r["etiket"] for r in ok_}):
            x = [r for r in ok_ if r["etiket"] == et]
            s.append(f"\n- {et}: {len(x)} etiket; en az bir S7 bölgesi olan {sum(r['bolge_sayisi'] > 0 for r in x)}; kapsama medyanı "
                     f"{_so7_y(float(np.median([r['kapsama'] for r in x])))}.")
        s.append("")
    if J.get("sayim"):
        S = J["sayim"]
        s += ["## SAYIM (seçilen nokta; getiri YOK; evren bugünün listesi, 31.08.2026 kesiği, likidite süzgeci yok)", "", f"- Koşu (UTC): `{S['zaman_utc']}`; süre {S.get('sure_sn')} sn.",
              "- S5 kutusu = COL_S6_TASLAK.pine 'S5 (ölçüm)' ön ayarı (N = 1; Cemal'in grafikte gördüğü S5 kutuları). S5 ölçüm bölgesi = so_s5 ev5 .. bölge sonu (20 bar "
              "birleştirme; ölçümde kullanılan). S6 = taslak varsayılanı (N = 5). Uzunluk = bölgenin geçerli bar sayısı (kırılım mumu hariç).", "",
              "| pazar | tanım | hisse | hisse-yıl | bölge | 100 hisse-yılda | uzunluk medyan [Ç1-Ç3] | 1-4 günlük payı | 1 günlük | DİP / YOL | YUKARI / AŞAĞI / sönme / AÇIK |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for p, o in S["pazar"].items():
            for t, ad in (("S5", "S5 kutusu (N=1)"), ("S5o", "S5 ölçüm bölgesi"), ("S6", "S6 varsayılan"), ("S7", "S7")):
                x = o[t]; sn = x["sinif"]; tr = x["tur"]
                s.append(f"| {p} | {ad} | {o['hisse']} | {x['hisse_yil']:.0f} | {x['n']} | {x['yuz_hy']:.1f} | {x['L_med']:.0f} [{x['L_q25']:.0f}-{x['L_q75']:.0f}] | "
                         f"{_so7_y(x['pay_1_4'])} | {_so7_y(x['pay_1'])} | {_so7_y(sn.get('DIP'))} / {_so7_y(sn.get('YOL'))} | "
                         + (" / ".join(_so7_y(tr.get(k)) for k in ("YUKARI", "AŞAĞI", "sönme", "AÇIK")) if t != "S5o" else "-") + " |")
        s += ["", "| pazar | S7 onay öncesi uzunluk medyanı (s..e) | onaydan sonra süre medyanı (bar) | onaydan sonra <= 3 barda biten payı |", "|---|---|---|---|"]
        for p, o in S["pazar"].items():
            x = o["S7"]
            s.append(f"| {p} | {x.get('L_onay_med', float('nan')):.0f} | {x.get('onay_sonrasi_med', float('nan')):.0f} | {_so7_y(x.get('onay_sonrasi_0_3'))} |")
        s += ["", "- S7'de 1-4 günlük bölge TANIM GEREĞİ yoktur (L >= Lmin); kısa ömür ölçüsü 'onaydan sonra <= 3 barda biten payı'dır.",
              "- Hayatta kalma: yalnız bugün işlem gören hisseler (V_*.pkl).", ""]
    metin = "\n".join(s) + "\n"
    if _S7_EPOSTA.search(metin):
        raise S7Hata("S7 tasarım metninde e-posta biçimli parça var")
    yol = _so7_yol("tasarim", cikti)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def so_s7_pine_blok(cikti: Optional[str] = None, yaz: bool = True) -> str:
    """COL_S7_BOLGE.pine sonundaki BEKLENEN KUTULAR bloğunu s7_tasarim.json'dan yeniden yazar (iki işaret arası)."""
    J = json.load(open(_so7_yol("tasarim_json", cikti), encoding="utf-8"))
    sp = J["secilen"]
    f2 = lambda x: f"{x:.2f}".replace(".", ",")   # noqa: E731
    t = lambda x: pd.Timestamp(x).strftime("%d.%m.%y") if x and x != "-" else "-"   # noqa: E731
    s = [SO7_PINE_BAS,
         f"// Python ikizi (SIKISMA_S7.so_s7_bolgeler), V_BIST fiyatı, BIST, input'lar varsayılan (k_m {sp['k_m']}, bb {sp['bb']}, Lmin {sp['Lmin']}, Lmax "
         f"{SO7_ESIK['Lmax']}, bant %{sp['bant']['BIST'] * 100:.0f}, eğim [{sp['egim'][0] * 100:+.0f}%, {sp['egim'][1] * 100:+.0f}%]).",
         "// Tarih gg.aa.yy. başlangıç = kutunun ilk mumu (geriye uzatılmış), onay = karar günü (elmas), bitiş = bölgenin son mumu (kırılım mumu hariç),",
         "// kırılım = bölgeyi bitiren mum (ok / sönme etiketi). üst / alt = son durumdaki kutu (1 uç gün hariç kapanış bandı). V_BIST temettü-düzeltmeli",
         "// olabilir; TradingView fiyatı düzeltmesizse üst / alt birkaç kuruş farklı çıkabilir (tarihler aynı olmalı). Her örnekte örnek aralığının",
         "// ±20 bar çevresindeki kutular yazılıdır (bağlam). SEÇMEMELİ örnekte ±5 bar tampona değen kutu OLMAMALI; ±20 içindeki komşu kutu kural",
         "// dışı değildir. Bayram / hacimsiz gün geçerli bar sayılmaz.", "//"]
    for b in J["beklenen"]:
        bas = f"// {b['ornek']} ({'SEÇMELİ ' + b['beklenen'] if b['secmeli'] else 'SEÇMEMELİ'}) {t(b['ilk'])}-{t(b['son'])}: "
        if not b["kutular"]:
            s.append(bas + "KUTU YOK"); continue
        s.append(bas + f"{len(b['kutular'])} kutu")
        for k in b["kutular"]:
            s.append(f"//     başlangıç {t(k['bas'])}  onay {t(k['onay'])}  bitiş {t(k['bitis'])}  kırılım {t(k['kilit_tarih'])}  {k['tur']:<6}  "
                     f"{'DİP' if k['sinif'] == 'DIP' else 'YOL ÜSTÜ'}  {k['L']} bar  üst {f2(k['ust'])} / alt {f2(k['alt'])}")
    s.append(SO7_PINE_SON)
    blok = "\n".join(s)
    yol = _so7_yol("pine", cikti)
    if yaz and os.path.exists(yol):
        m = open(yol, encoding="utf-8").read()
        if SO7_PINE_BAS in m and SO7_PINE_SON in m:
            m = m.split(SO7_PINE_BAS)[0] + blok + m.split(SO7_PINE_SON)[1]
            with open(yol, "w", encoding="utf-8") as f:
                f.write(m)
    return blok


# ---------------------------------------------------------------- ÇAKIŞMA KAPISI
def _cakisma_kontrol_s7(_once=_CK_ONCE_S7, _dosya="SIKISMA_S7.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_S7", "_CK_KAYIT", "_cakisma_kontrol_s7", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "itertools", "_dt", "SO", "SY", "SC",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_s7()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=SO7_SURUM)
    ap.add_argument("komut", choices=["s7onyazim", "s7tasarim", "s7sayim", "s7pine", "s7md"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true", help="s7onyazim: var olan ön yazımı yeniden yaz (YAPMA: mühür ve zaman değişir)")
    ap.add_argument("--isci", type=int, default=2, help="s7sayim: paralel süreç sayısı")
    a = ap.parse_args()
    try:
        if a.komut == "s7onyazim":
            print(so_s7_on_yazim(a.cikti, uzerine=a.uzerine_yaz))
        elif a.komut == "s7tasarim":
            J_ = so_s7_tasarim(a.veri, a.cikti)
            so_s7_pine_blok(a.cikti)
            print(json.dumps({k: J_[k] for k in ("en_cok_tutan", "toplam", "tam_tutan_nokta", "aday_nokta", "secilen", "secilen_kacan")}, ensure_ascii=False))
        elif a.komut == "s7sayim":
            R_ = so_s7_sayim(a.veri, a.cikti, isci=a.isci)
            print(json.dumps(SC._sc_temiz(R_), ensure_ascii=False, indent=1))
        elif a.komut == "s7pine":
            print(so_s7_pine_blok(a.cikti))
        else:
            print(so_s7_md_yaz(a.cikti))
    except S7Hata as ex:
        s7log.error("%s", ex); sys.exit(1)
