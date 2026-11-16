"""COKUS_OYNAK — BIST geniş çöküşü sonrası oynak / çok düşmüş hisse hipotezi (Cemal, 16 Kasım 2026). Tek dosya.

İş tanımı: arastirma_cikti/cokus_oynak/COKUS_OYNAK_IS_TANIMI.md (ön kayıt; eşikler CO_ESIK'te, sonuç görülmeden yazıldı).
HİPOTEZ H: geniş çöküşten (evren medyan 120 gün getirisi <= -%30, ilk gün) sonra σ250 en üst beşlik (OYNAK) hisseler 250 günde
  (a) +%100'e orta üç beşlikten (TABAN) daha sık ulaşır, (b) -%50'ye anlamlı olarak daha sık ulaşMAZ.
Komut:  python COKUS_OYNAK.py onkayit [--veri D] [--canli D]   ON_KAYIT.md (eşik mühürü, veri / kod sha, kontrol listesi, olay SAYIMI; getiri yok)
        python COKUS_OYNAK.py kos     [--veri D] [--canli D]   kontrol kapısı (IZ_KARNE.ik_kontrol_kapisi) + mühür -> ölçüm + bugünün listesi -> sonuc.json, csv.gz, RAPOR.md
        python COKUS_OYNAK.py rapor                            RAPOR.md'yi sonuc.json'dan yeniden yazar
Colab:  exec(open('COKUS_OYNAK.py').read()); co_kos()   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   V_BIST.pkl (düzeltilmiş fiyat, 2015-06 .. 2026-10; ölçüm 31.08.2026'da kesik), G.pkl / dol.pkl (K25 fon tabloları),
        canlı bist_3y.pkl (yfinance, 16 Kas; yalnız bugünün listesi). Repoya veri girmez.
Hayatta kalma: evren bugün işlem görenler; 2018 / 2020'de batanlar yok -> sonuçlar YUKARI YANLI (özellikle P(-%50) düşük görünür).
Hiçbir isim için alım / öneri dili kullanılmaz: liste ADAY listesidir.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_CO = {k: id(v) for k, v in globals().items()}

import argparse  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import traceback  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_CO = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_CO not in sys.path:
    sys.path.insert(0, KOK_CO)

colog = logging.getLogger("col.cokus_oynak")
if not colog.handlers:
    _co_h = logging.StreamHandler(sys.stderr)
    _co_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s cokus_oynak: %(message)s", "%H:%M:%S"))
    colog.addHandler(_co_h)
    colog.setLevel(logging.INFO)
    colog.propagate = False

CO_SURUM = "COKUS_OYNAK v1.0 (16 Kas 2026)"
_CO_SCR = "/tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad"
CO_YOL: Dict[str, str] = {
    "veri": os.environ.get("CO_VERI", os.path.join(_CO_SCR, "veri")),
    "canli": os.environ.get("CO_CANLI", os.path.join(_CO_SCR, "canli")),
    "cikti": os.path.join(KOK_CO, "arastirma_cikti", "cokus_oynak"),
}

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (iş tanımı; sonuç görüldükten sonra DEĞİŞMEZ)
CO_ESIK: Dict[str, Any] = {
    "kriz": "2026-08-31",                 # ölçüm fiyat kesiği (fon krizi); 250 gün penceresi bunu aşan olay ölçülmez
    "gecerli_bar": "H>L ve V>0 ve O,C>0 ve sonlu",
    "cokus": {"gun": 120, "esik": -0.30, "ara": 250, "min_hisse": 50,
              "tanim": "evren medyan 120 işlem günü getirisi (ortak takvim, kapanış en çok 10 gün ileri taşınır, t'de geçerli barı olan hisse) "
                       "<= -%30 olan İLK gün; sonraki çöküş için en az 250 işlem günü ara. Tespit kesiksiz veriyle (yalnız geçmiş fiyat); "
                       "sonuç kesik veriyle."},
    "giris_gecikme": 5,                   # çöküş gününden sonraki 5. işlem günü açılışı (ana)
    "giris_gecikme_ek": 20,               # bilgi
    "giris_tolerans": 5,                  # giriş günü bar yoksa en çok 5 takvim işlem günü içindeki ilk geçerli bar açılışı
    "bayat_gun": 5,                       # karar gününden 5 işlem gününden eski son bar -> işlem görmüyor, dışarıda
    "sigma_gun": 250, "zirve_gun": 250, "likidite_gun": 60, "likidite_alt": 0.20, "r_kisa": 60,
    "ufuk": 250, "ufuk_kisa": 120, "mdd_gun": 60, "yukari": 1.0, "asagi": -0.5,
    "dilim": {"OYNAK": "σ250 sıra yüzdeliği > 0,80 (likidite süzgecinden sonra, giriş günü evreni)",
              "TABAN": "σ250 sıra yüzdeliği (0,20, 0,80]",
              "DUSMUS": "250 gün zirveden düşüş sıra yüzdeliği <= 0,20 (en çok düşmüş beşlik)",
              "TABAN_D": "düşüş sıra yüzdeliği (0,20, 0,80]",
              "CAPRAZ": "OYNAK ve DUSMUS (taban: TABAN)",
              "PROFIL": "OYNAK ve zirveden düşüş <= -%60 (bugünün piyango profili; bilgi, taban: TABAN)"},
    "bolunme": "SIKISMA_YENIDEN.sy_bolunme_supheli ANA kuralı; şüpheli günü [giriş-260 bar, giriş+250 takvim günü] içinde olan hisse olaydan çıkar (sayılır, yazılır)",
    "bootstrap": {"n": 1000, "tohum": 20261116, "duzey": "hisse; birleşikte olay içinde katmanlı", "yuzde": [2.5, 97.5]},
    "permutasyon": {"n": 1000, "tohum": 20261117, "tanim": "olay içinde OYNAK / TABAN etiketleri karıştırılır (bilgi)"},
    "bilgi_olay": {"2018B": "2018-08-20", "2020B": "2020-03-19",
                   "tanim": "BİLGİ, karar dışı (olay sayımından sonra, getiri görülmeden eklendi): ana tanım 2018 ve 2020'yi çöküş saymadı "
                            "(2018 yıl en düşük medyan r120 -%28,5; 2020 -%1,7). Bu günler yılın en düşük medyan r120 günüdür, yani GERİYE BAKARAK "
                            "seçildi (dip o gün bilinmezdi); aynı +5 gün girişiyle aynı tablo, etiket yalnız bilgi"},
    "normal": {"yillar": [2017, 2023], "giris": "yılın ilk ortak takvim işlem günü açılışı (karar = önceki işlem günü)"},
    "karar_kurali": {
        "birincil": "OYNAK vs TABAN, birleşik (iki tamamlanmış çöküş), ana giriş (+5 gün)",
        "Ha": "birleşik P(+%100) farkı > 0 VE bootstrap %95 alt uç > 0 VE her çöküş olayında nokta fark > 0",
        "Hb": "birleşik P(-%50) farkının bootstrap %95 alt ucu <= 0 (anlamlı yüksek değil)",
        "etiket": "Ha ve Hb -> EMARE; Ha ve Hb değil -> PİYANGO; Ha değil -> DESTEKLENMEDİ; "
                  "tamamlanmış çöküş < 2 ya da herhangi olayda OYNAK veya TABAN n < 30 -> ÖLÇÜLEMEDİ",
        "ikincil": "DUSMUS ve CAPRAZ aynı kuralla ayrı etiket (bilgi); üç (a) testinin tek yönlü bootstrap p'leri BH ile (bilgi)",
        "not": "iki çöküş = iki olay: tutsa bile İZ denmez, en fazla EMARE",
    },
    "bugun": {"tarih": "2026-11-16", "karar": "2026-11-13", "dusus_esik": -0.60,
              "uzak": ["TEHOL", "PEKGY", "ODINE", "ANELE", "MANAS", "IEYHO", "GUNDG", "DSTKF", "OZATD", "TRHOL", "SKYLP"],
              "ilk": 15, "son_gun": 20,
              "profil": "σ250 en üst beşlik (likidite süzgecinden sonra) VE 250 gün zirveden >= %60 düşmüş VE likidite alt %20 dışı VE fon lekesi "
                        "(son fon raporunda tasfiye fonu pozisyonu) yok VE Uzak listede yok; sıra σ250 büyükten"},
}


# SAPMA (ilk koşudan SONRA eklendi; CO_ESIK mühürü değişmez, karar kuralı değişmez): K6 veri birimi
CO_SAPMA: Dict[str, Any] = {
    "ham_sicrama": 0.25,
    "tanim": "ham (süzülmemiş) ardışık iki işlem günü kapanışı arasında |değişim| > %25 = düzeltilmemiş sermaye işlemi şüphesi "
             "(BIST fiyat marjı ±%10, 12.03.2020 öncesi ±%20; kilitli taban / tavan serileri ardışık ham günlerde %10'u aşmaz, bu yüzden yakalanmaz). "
             "Bugünün listesi: şüpheli günden önceki fiyatlar oranla geriye düzeltilir (hacim ters oranla). Geçmiş tablo: şüpheli günü "
             "[giriş-260 bar, ufuk sonu] içinde olan hisseler çıkarılarak DUYARLILIK tablosu (bilgi; karar değişmez).",
}


CO_HATA: List[str] = [
    "Beklenti tutmadı (yanlış yorum riski): iş tanımı 2018 ve 2020'yi çöküş bekliyordu; sabit tanımla (medyan r120 <= -%30) 2018'in en düşüğü -%28,5, 2020'nin -%1,7 "
    "(Mart 2020 öncesi 120 günde küçük hisseler yükselmişti). Çöküşler 2023-05-22 ve 2026-10-13; ölçülebilir tek olay 2023 -> birincil karar ÖLÇÜLEMEDİ. Tanım değiştirilmedi.",
    "Kod (süreç): ilk koşu 2026 olayında boş tabloda düştü (AttributeError); giriş kriz kesiğinden sonraysa olay atlanır. Sonuç görülmeden önceki hata; eşik değişmedi.",
    "Veri (K6): canlı Yahoo verisinde düzeltilmemiş bedelsiz var (ör. MERKO 30.04 -> 04.05.2026 ardışık iki günde -%86, hacim 15 kat); ilk liste MERKO'yu σ250 ile 1. sıraya "
    "koymuştu. Ham ardışık gün |değişim| > %25 geriye düzeltildi (evrende 62 hisse). Geçmiş V_BIST'te pencerelerde bu tür sıçrama 0 (duyarlılık tablosu ana tabloyla aynı).",
    "Ölçü yorumu: σ250 geçerli bar (H > L) getirisiyle hesaplanır; kilitli taban serisi (H = L günleri atılır) tek bir büyük getiri gibi görünür (UFUK 07.10 -%72, LYDYE 04.11 -%74). "
    "Bugünün listesinin üstü bu yüzden fon krizi taban serisi yaşayan hisselerdir; 'oynak' burada 'kilitli çöküş' demektir.",
    "Kapsam: fon lekesi yalnız fon portföyünde tasfiye fonu pozisyonuna bakar; HEDEF (Hedef Holding) tasfiyedeki portföy şirketiyle aynı adı taşır ama leke 'temiz' çıkar. "
    "Listedeki isimler DOSYA kapısından geçmedi.",
    "Kıyas: 'normal dönem' N2023 girişi (2023-01-02) balon sonrasıdır (medyan r120 +%120) ve 250 gün penceresi 2023 çöküşünü içerir; 2017 ve 2023 nötr dönem değildir.",
    "Süreç (K9): ON_KAYIT.md commit'i alt ajana yasak; ön kayıt zamanı dosyada (UTC), CO_ESIK mühürü kos'ta denetlenir; commit ana modelde.",
    "Geriye bakma (bilgi hücreleri): 2018B / 2020B günleri yılın en düşük medyan günü olarak seçildi (dip o gün bilinmezdi); getiri görülmeden eklendi, karar dışı.",
]


class COHata(RuntimeError):
    """Durdurucu hata."""


def _co_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def co_muhur() -> str:
    return hashlib.sha256(json.dumps(CO_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _co_kod_sha() -> str:
    return _co_sha(os.path.join(KOK_CO, "COKUS_OYNAK.py"))


# ---------------------------------------------------------------- 1) VERİ
def co_gecerli(d: pd.DataFrame, kes: Optional[str] = None) -> pd.DataFrame:
    """Geçerli bar süzgeci (H > L, V > 0, O / C > 0, sonlu); kes verilirse o tarihten sonrası atılır."""
    d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float).copy()
    d.index = pd.DatetimeIndex(d.index).tz_localize(None) if getattr(d.index, "tz", None) is not None else pd.DatetimeIndex(d.index)
    if kes is not None:
        d = d[d.index <= pd.Timestamp(kes)]
    ok = (d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0) & np.isfinite(d[["Open", "High", "Low", "Close"]]).all(axis=1)
    d = d[ok].sort_index()
    return d[~d.index.duplicated(keep="last")]


def co_ham_sicrama(d: pd.DataFrame) -> pd.DatetimeIndex:
    """Ham ardışık işlem günleri (C > 0) arasında |kapanış değişimi| > CO_SAPMA eşiği olan günler."""
    x = d[["Close"]].astype(float)
    x = x[(x.Close > 0) & np.isfinite(x.Close)].sort_index()
    x = x[~x.index.duplicated(keep="last")]
    r = x.Close / x.Close.shift(1) - 1
    return pd.DatetimeIndex(x.index[r.abs() > CO_SAPMA["ham_sicrama"]])


def co_ham_duzelt(d: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """Ham şüpheli sıçramaları geriye doğru oranla düzeltir (sermaye işlemi varsayımı). Döner: (düzeltilmiş, düzeltme sayısı)."""
    x = d[["Open", "High", "Low", "Close", "Volume"]].astype(float).copy()
    x = x[(x.Close > 0) & np.isfinite(x.Close)].sort_index()
    x = x[~x.index.duplicated(keep="last")]
    gun = co_ham_sicrama(x)
    for t in gun:
        i = x.index.get_loc(t)
        f = x.Close.iloc[i] / x.Close.iloc[i - 1]
        x.iloc[:i, 0:4] = x.iloc[:i, 0:4] * f
        x.iloc[:i, 4] = x.iloc[:i, 4] / f
    return x, len(gun)


def co_veri(veri: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    yol = os.path.join(veri or CO_YOL["veri"], "V_BIST.pkl")
    if not os.path.exists(yol):
        raise COHata(f"veri yok: {yol} (git worktree add /tmp/iv origin/islenmis-veri; python FON_IZI.py vpac /tmp/iv/veri /tmp/veri)")
    V = pd.read_pickle(yol)
    if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
        V = V["veri"]
    out: Dict[str, pd.DataFrame] = {}
    for s, d in V.items():
        try:
            x = co_gecerli(d)
            if len(x):
                out[str(s)] = x
        except Exception as ex:  # tek hisse bozuksa diğerleri sürer
            colog.warning("BIST %s atlandı: %s", s, ex)
    if "XU100" in out:
        colog.info("XU100 V_BIST'te var ama evren medyanı kullanılır (iş tanımı tek tanım)")
        out.pop("XU100")
    colog.info("V_BIST: %d hisse (%s)", len(out), yol)
    return out


def co_takvim(V: Dict[str, pd.DataFrame]) -> Tuple[pd.DatetimeIndex, pd.DataFrame]:
    """Ortak takvim (en az min_hisse geçerli barı olan günler) ve kapanış matrisi (yalnız geçerli bar; NaN = bar yok)."""
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index()
    say = C.notna().sum(axis=1)
    T = C.index[say >= CO_ESIK["cokus"]["min_hisse"]]
    return pd.DatetimeIndex(T), C.loc[T]


def co_medyan120(C: pd.DataFrame) -> pd.DataFrame:
    """Her takvim günü t: medyan_s (C_s(t) / C_s(t-120) - 1); C_s(t) geçerli bar olmalı, t-120 kapanışı en çok 10 gün ileri taşınır."""
    g = CO_ESIK["cokus"]["gun"]
    Cf = C.ffill(limit=10)
    r = C / Cf.shift(g) - 1.0
    return pd.DataFrame({"medyan": r.median(axis=1, skipna=True), "n": r.notna().sum(axis=1)})


def co_cokus_gunleri(M: pd.DataFrame) -> List[pd.Timestamp]:
    E = CO_ESIK["cokus"]
    out: List[pd.Timestamp] = []
    son_i = -10 ** 9
    T = M.index
    for i, (t, row) in enumerate(M.iterrows()):
        if row.n >= E["min_hisse"] and row.medyan <= E["esik"] and i - son_i >= E["ara"]:
            out.append(t); son_i = i
    return out


# ---------------------------------------------------------------- 2) OLAY ÖLÇÜLERİ
def _co_bolunme(d: pd.DataFrame) -> pd.DatetimeIndex:
    import SIKISMA_YENIDEN as SY
    s = SY.sy_bolunme_supheli(d.Close.to_numpy(), SY.SY_ESIK)
    return d.index[s]


def co_hisse_olay(s: str, d: pd.DataFrame, T: pd.DatetimeIndex, gi: int, bol: pd.DatetimeIndex,
                  kes: Optional[str], ham: Optional[pd.DatetimeIndex] = None) -> Optional[Dict[str, Any]]:
    """Giriş takvim sırası gi; karar = T[gi-1]. Ölçüler yalnız <= karar barlarından; sonuç giriş açılışından 250 takvim günü."""
    E = CO_ESIK
    karar, giris = T[gi - 1], T[gi]
    x = d[d.index <= karar]
    if len(x) < E["sigma_gun"] + 1:
        return None
    if x.index[-1] < T[max(0, gi - 1 - E["bayat_gun"])]:
        return None                                              # K3: işlem görmüyor
    if x.index.max() > karar:
        raise COHata("geleceğe bakma: karar sonrası bar ölçüye girdi")
    C, V = x.Close.to_numpy(), x.Volume.to_numpy()
    lr = np.diff(np.log(C[-(E["sigma_gun"] + 1):]))
    r: Dict[str, Any] = {"sembol": s, "karar": karar, "giris_gunu": giris}
    r["sigma250"] = float(np.std(lr, ddof=1))
    r["dusus250"] = float(C[-1] / C[-E["zirve_gun"]:].max() - 1)
    r["likidite"] = float(np.mean(C[-E["likidite_gun"]:] * V[-E["likidite_gun"]:]))
    r["r60_once"] = float(C[-1] / C[-E["r_kisa"] - 1] - 1) if len(C) > E["r_kisa"] else np.nan
    # giriş
    son_tol = T[min(len(T) - 1, gi + E["giris_tolerans"])]
    y = d[(d.index >= giris) & (d.index <= son_tol)]
    if not len(y):
        r["sonuc_yok"] = "giriş penceresinde bar yok"; return r
    e = float(y.Open.iloc[0]); r["giris_bar"] = y.index[0]; r["giris"] = e
    if gi + E["ufuk"] >= len(T):
        r["sonuc_yok"] = "ufuk takvimi aşıyor"; return r
    t_son = T[gi + E["ufuk"]]
    if kes is not None and t_son > pd.Timestamp(kes):
        r["sonuc_yok"] = "250 gün penceresi kriz kesiğini aşıyor"; return r
    w = d[(d.index >= y.index[0]) & (d.index <= t_son)]
    Cw = w.Close.to_numpy()
    r["n_bar_ufuk"] = len(w)
    up = np.where(Cw >= e * (1 + E["yukari"]))[0]; dn = np.where(Cw <= e * (1 + E["asagi"]))[0]
    r["p100"] = bool(len(up)); r["m50"] = bool(len(dn))
    r["ilk"] = ("+100" if (len(up) and (not len(dn) or up[0] < dn[0])) else ("-50" if len(dn) else ""))
    r["r250"] = float(Cw[-1] / e - 1)
    w120 = w[w.index <= T[gi + E["ufuk_kisa"]]]
    r["r120"] = float(w120.Close.iloc[-1] / e - 1)
    w60 = w[w.index <= T[gi + E["mdd_gun"]]]
    r["mdd60"] = float(min(w60.Close.min() / e - 1, 0.0))
    r["son_bar_ufuk"] = w.index[-1]
    r["yarim"] = bool(w.index[-1] < T[gi + E["ufuk"] - E["bayat_gun"]])   # pencere sonunda işlem yok (bilgi)
    b0 = x.index[-min(len(x), 260)]
    r["bolunme"] = bool(((bol >= b0) & (bol <= t_son)).any())
    if ham is not None:
        r["ham_sicrama"] = bool(((ham >= b0) & (ham <= t_son)).any())          # SAPMA (K6), yalnız duyarlılık tablosu
    return r


def co_olay(V: Dict[str, pd.DataFrame], T: pd.DatetimeIndex, gi: int, ad: str, tur: str,
            bolm: Dict[str, pd.DatetimeIndex], kes: Optional[str], hamm: Optional[Dict[str, pd.DatetimeIndex]] = None) -> pd.DataFrame:
    rows = []
    for s, d in V.items():
        try:
            r = co_hisse_olay(s, d, T, gi, bolm.get(s, pd.DatetimeIndex([])), kes,
                              None if hamm is None else hamm.get(s, pd.DatetimeIndex([])))
        except COHata:
            raise
        except Exception as ex:
            colog.warning("%s %s: %s", ad, s, traceback.format_exc(limit=1)); r = None
        if r is not None:
            rows.append(r)
    D = pd.DataFrame(rows)
    D["olay"] = ad; D["tur"] = tur
    if not len(D):          # ör. 2026 çöküşü: karar günü kriz kesiğinden sonra, kesik veride ölçülecek hisse yok
        return D
    return co_dilimle(D)


def co_dilimle(D: pd.DataFrame) -> pd.DataFrame:
    """Likidite alt %20 hariç; kalan evrende σ250 ve düşüş sıra yüzdelikleri ve dilimler."""
    E = CO_ESIK
    D = D.copy()
    D["liq_alt"] = D.likidite < D.likidite.quantile(E["likidite_alt"])
    k = ~D.liq_alt
    D["sig_pct"] = np.nan; D["dd_pct"] = np.nan
    D.loc[k, "sig_pct"] = D.loc[k, "sigma250"].rank(pct=True)
    D.loc[k, "dd_pct"] = D.loc[k, "dusus250"].rank(pct=True)          # küçük (en negatif) = en çok düşmüş
    D["OYNAK"] = k & (D.sig_pct > 0.8)
    D["TABAN"] = k & (D.sig_pct > 0.2) & (D.sig_pct <= 0.8)
    D["DUSMUS"] = k & (D.dd_pct <= 0.2)
    D["TABAN_D"] = k & (D.dd_pct > 0.2) & (D.dd_pct <= 0.8)
    D["CAPRAZ"] = D.OYNAK & D.DUSMUS
    D["PROFIL"] = D.OYNAK & (D.dusus250 <= E["bugun"]["dusus_esik"])
    return D


# ---------------------------------------------------------------- 3) İSTATİSTİK
KARS: List[Tuple[str, str, str]] = [("OYNAK", "OYNAK", "TABAN"), ("DUSMUS", "DUSMUS", "TABAN_D"),
                                    ("CAPRAZ", "CAPRAZ", "TABAN"), ("PROFIL", "PROFIL", "TABAN")]


def _co_olcum(D: pd.DataFrame) -> pd.DataFrame:
    """Sonucu olan, bölünme şüphesi olmayan satırlar."""
    if "p100" not in D.columns:
        return D.iloc[0:0]
    return D[D.p100.notna() & (D.bolunme != True)]  # noqa: E712


def co_ozet(x: pd.DataFrame) -> Dict[str, Any]:
    n = len(x)
    if n == 0:
        return {"n": 0}
    return {"n": int(n), "P100": float(x.p100.mean()), "M50": float(x.m50.mean()),
            "med_r250": float(x.r250.median()), "ort_r250": float(x.r250.mean()),
            "med_r120": float(x.r120.median()), "med_mdd60": float(x.mdd60.median()),
            "ilk_p100": float((x.ilk == "+100").mean()), "ilk_m50": float((x.ilk == "-50").mean())}


def co_karsilas(Ds: List[pd.DataFrame], a: str, b: str, rng_tohum: int) -> Dict[str, Any]:
    """Ds: olay başına ölçüm tabloları (katmanlı). A vs B: P100, M50 farkı ve kat; hisse düzeyinde katmanlı bootstrap."""
    E = CO_ESIK["bootstrap"]
    A = [x[x[a]] for x in Ds]; B = [x[x[b]] for x in Ds]
    oA = co_ozet(pd.concat(A) if A else pd.DataFrame()); oB = co_ozet(pd.concat(B) if B else pd.DataFrame())
    out: Dict[str, Any] = {"A": oA, "B": oB}
    if oA["n"] == 0 or oB["n"] == 0:
        return out
    rng = np.random.default_rng(rng_tohum)
    fark = {"P100": [], "M50": [], "kat100": [], "kat50": [], "med": []}
    for _ in range(E["n"]):
        ra, rb = [], []
        for xa, xb in zip(A, B):
            if len(xa):
                ra.append(xa.iloc[rng.integers(0, len(xa), len(xa))])
            if len(xb):
                rb.append(xb.iloc[rng.integers(0, len(xb), len(xb))])
        ca, cb = pd.concat(ra), pd.concat(rb)
        pa, pb = ca.p100.mean(), cb.p100.mean(); ma, mb = ca.m50.mean(), cb.m50.mean()
        fark["P100"].append(pa - pb); fark["M50"].append(ma - mb)
        fark["kat100"].append(pa / pb if pb > 0 else np.nan); fark["kat50"].append(ma / mb if mb > 0 else np.nan)
        fark["med"].append(ca.r250.median() - cb.r250.median())
    q = E["yuzde"]
    for k, v in fark.items():
        v = np.array(v, float); v = v[np.isfinite(v)]
        out[f"bs_{k}"] = [float(np.percentile(v, q[0])), float(np.percentile(v, q[1]))] if len(v) else [np.nan, np.nan]
    out["fark_P100"] = oA["P100"] - oB["P100"]; out["fark_M50"] = oA["M50"] - oB["M50"]
    out["kat_P100"] = oA["P100"] / oB["P100"] if oB["P100"] > 0 else None
    out["kat_M50"] = oA["M50"] / oB["M50"] if oB["M50"] > 0 else None
    out["fark_med_r250"] = oA["med_r250"] - oB["med_r250"]
    v = np.array(fark["P100"]); out["p_tek_P100"] = float((v <= 0).mean())
    # permütasyon (bilgi): olay içinde etiket karıştırma
    P = CO_ESIK["permutasyon"]; rp = np.random.default_rng(P["tohum"])
    havuz = [pd.concat([xa.assign(_g=1), xb.assign(_g=0)]) for xa, xb in zip(A, B) if len(xa) and len(xb)]
    gozlenen = out["fark_P100"]; say = 0
    for _ in range(P["n"]):
        aa, bb = [], []
        for h in havuz:
            g = rp.permutation(h._g.to_numpy())
            aa.append(h.p100.to_numpy()[g == 1]); bb.append(h.p100.to_numpy()[g == 0])
        if np.concatenate(aa).mean() - np.concatenate(bb).mean() >= gozlenen:
            say += 1
    out["perm_p_P100"] = (say + 1) / (P["n"] + 1)
    return out


def _bh(p: List[float]) -> List[float]:
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); q = np.empty(n)
    m = 1.0
    for k in range(n - 1, -1, -1):
        m = min(m, p[o[k]] * n / (k + 1)); q[o[k]] = m
    return q.tolist()


def co_etiket(K_olay: Dict[str, Dict[str, Any]], K_bir: Dict[str, Any], n_olay: int) -> Dict[str, Any]:
    if n_olay < 2:
        return {"etiket": "ÖLÇÜLEMEDİ", "neden": f"tamamlanmış çöküş {n_olay} < 2"}
    for o, k in K_olay.items():
        if k["A"]["n"] < 30 or k["B"]["n"] < 30:
            return {"etiket": "ÖLÇÜLEMEDİ", "neden": f"{o}: n {k['A']['n']} / {k['B']['n']} < 30"}
    Ha = (K_bir["fark_P100"] > 0 and K_bir["bs_P100"][0] > 0 and all(k["fark_P100"] > 0 for k in K_olay.values()))
    Hb = K_bir["bs_M50"][0] <= 0
    et = "EMARE" if (Ha and Hb) else ("PİYANGO" if Ha else "DESTEKLENMEDİ")
    return {"etiket": et, "Ha": bool(Ha), "Hb": bool(Hb),
            "neden": f"P100 farkı {K_bir['fark_P100']:+.3f} [{K_bir['bs_P100'][0]:+.3f}, {K_bir['bs_P100'][1]:+.3f}], olay farkları "
                     + ", ".join(f"{o} {k['fark_P100']:+.3f}" for o, k in K_olay.items())
                     + f"; M50 farkı {K_bir['fark_M50']:+.3f} [{K_bir['bs_M50'][0]:+.3f}, {K_bir['bs_M50'][1]:+.3f}]"}


# ---------------------------------------------------------------- 4) BUGÜNÜN LİSTESİ
def co_fon_leke(veri: str, karar: pd.Timestamp) -> pd.DataFrame:
    import FON_IZI as F
    G = pd.read_pickle(os.path.join(veri, "G.pkl"))
    if pd.Timestamp(G.bilinme.max()) > karar + pd.Timedelta(days=1):
        raise COHata("fon tablosunda karar gününden sonra bilinen satır var (geleceğe bakma)")
    G = G.copy()
    G["tasf"] = G.sirket.astype(str).str.upper().str.match(F.FI_TASFIYE_RE)
    G["tasf_lot"] = np.where(G.tasf, G.nominal, 0.0)
    G = G.join(G.groupby("kod").ay.max().rename("son_ay"), on="kod")
    S = G[G.ay == G.son_ay].groupby("kod").agg(son_ay=("ay", "max"), tasf_lot=("tasf_lot", "sum"))
    S["son_ay"] = [f"{a // 12}-{a % 12 + 1:02d}" for a in S.son_ay]
    S["leke"] = S.tasf_lot > 0
    return S


def _co_s6(x: pd.DataFrame) -> str:
    try:
        import S6_TABAN as S6
        T6 = S6.s6_taban(x)
        son = T6.iloc[-1]; Tk = T6.iloc[-10:]
        if not bool(son.olculur):
            return "HESAPLANAMADI"
        if bool(Tk.kirildi.any()):
            return "KIRILDI (son 10)"
        if bool(Tk.al.any()):
            return "AL (son 10)"
        if son.bolge_id >= 0 and son.durum in ("YENI", "SURER", "YENIDEN"):
            g = int(son.kutu_sag_i - son.kutu_sol_i + 1)
            return f"AÇIK {son.sinif} ({g} gün)"
        return f"yok ({son.sinif})"
    except Exception as ex:
        return f"HESAPLANAMADI: {type(ex).__name__}"


def co_bugun(canli: str, veri: str) -> Dict[str, Any]:
    E = CO_ESIK; B = E["bugun"]
    P = pd.read_pickle(os.path.join(canli, "bist_3y.pkl"))
    Vh: Dict[str, pd.DataFrame] = P["veri"]
    karar = pd.Timestamp(B["karar"])
    V = {}
    duz: Dict[str, int] = {}
    for s, d in Vh.items():
        if s == "XU100":
            continue
        try:
            dd_, k_ = co_ham_duzelt(d[d.index <= karar])          # SAPMA (K6): düzeltilmemiş sermaye işlemi
            duz[s] = k_
            x = co_gecerli(dd_, kes=B["karar"])
            if len(x):
                V[s] = x
        except Exception as ex:
            colog.warning("canlı %s atlandı: %s", s, ex)
    T, C = co_takvim(V)
    T = T[T <= karar]
    if T[-1] != karar:
        raise COHata(f"canlı veride karar günü {karar.date()} yok (son {T[-1].date()})")
    M = co_medyan120(C.loc[T])
    med = float(M.medyan.iloc[-1])
    rows = []
    gi_sanal = len(T)                          # karar = T[-1]; giriş henüz yok
    Tx = T.append(pd.DatetimeIndex([karar + pd.offsets.BDay(1)]))
    for s, d in V.items():
        x = d[d.index <= karar]
        if len(x) < E["sigma_gun"] + 1 or x.index[-1] < T[max(0, len(T) - 1 - E["bayat_gun"])]:
            continue
        Cc, Vv = x.Close.to_numpy(), x.Volume.to_numpy()
        lr = np.diff(np.log(Cc[-(E["sigma_gun"] + 1):]))
        rg = Cc[1:] / Cc[:-1] - 1
        sg = rg[-B["son_gun"]:]; j = int(np.argmax(np.abs(sg)))
        rows.append({"sembol": s, "sigma250": float(np.std(lr, ddof=1)), "dusus250": float(Cc[-1] / Cc[-E["zirve_gun"]:].max() - 1),
                     "likidite": float(np.mean(Cc[-E["likidite_gun"]:] * Vv[-E["likidite_gun"]:])),
                     "r60_once": float(Cc[-1] / Cc[-E["r_kisa"] - 1] - 1), "kapanis": float(Cc[-1]),
                     "son20_en_buyuk_gun": float(sg[j]), "son20_en_buyuk_tarih": str(x.index[-B["son_gun"]:][j].date()),
                     "son20_en_yuksek": float(sg.max())})
    del gi_sanal, Tx
    D = co_dilimle(pd.DataFrame(rows))
    D["ham_duzeltme"] = D.sembol.map(duz).fillna(0).astype(int)
    L = co_fon_leke(veri, karar)
    D["fon_leke"] = D.sembol.map(L.leke).fillna(False).astype(bool)
    D["fon_son_ay"] = D.sembol.map(L.son_ay)
    D["uzak"] = D.sembol.isin(B["uzak"])
    D["profil"] = D.OYNAK & (D.dusus250 <= B["dusus_esik"]) & (~D.liq_alt) & (~D.fon_leke) & (~D.uzak)
    D = D.sort_values("sigma250", ascending=False)
    Lp = D[D.profil].copy()
    Lp["s6"] = [_co_s6(co_gecerli(co_ham_duzelt(Vh[s][Vh[s].index <= karar])[0], kes=B["karar"])) for s in Lp.sembol]
    return {"karar": str(karar.date()), "evren_medyan_r120": med, "esik_gecti": bool(med <= E["cokus"]["esik"]),
            "n_evren": int(len(D)), "n_likit": int((~D.liq_alt).sum()), "n_oynak": int(D.OYNAK.sum()),
            "n_oynak_dusus60": int((D.OYNAK & (D.dusus250 <= B["dusus_esik"])).sum()),
            "n_leke_ele": int((D.OYNAK & (D.dusus250 <= B["dusus_esik"]) & D.fon_leke).sum()),
            "n_uzak_ele": int((D.OYNAK & (D.dusus250 <= B["dusus_esik"]) & D.uzak & ~D.fon_leke).sum()),
            "n_profil": int(len(Lp)), "n_ham_duzeltilen": int(sum(1 for v in duz.values() if v)),
            "n_profil_duzeltilen": int((Lp.ham_duzeltme > 0).sum()), "medyan_seri_son": {str(t.date()): float(v) for t, v in M.medyan.iloc[-130::10].items()},
            "liste": Lp.to_dict("records")}


# ---------------------------------------------------------------- 5) KONTROL LİSTESİ (ön kayda girer)
CO_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban = aynı giriş günü, aynı evren (likidite süzgeci sonrası) σ250 orta üç beşlik; aynı giriş açılışı ve 250 gün geometrisi; mekanik üstünlük: yüksek σ iki kuyruğu birden büyütür, bu yüzden normal dönem (2017, 2023) aynı tabloyla kıyaslanır; olasılık ölçüsünde portföy yerine olay içi permütasyon (1000)"),
    "K2": ("EVET", "ölçüler yalnız karar günü (giriş-1) ve öncesi barlardan (co_hisse_olay içinde x.index.max() <= karar mekanik denetim, COHata); çöküş günü yalnız geçmiş 120 gün; fon tablosu bilinme <= karar denetimi (co_fon_leke); evren bugünün listesi (K7)"),
    "K3": ("EVET", "geçerli bar H>L, V>0, O,C>0 (co_gecerli); karar gününden 5 işlem gününden eski son bar -> hisse dışarıda; bugünün listesi 13 Kas tam bar (16 Kas yarım bar atılır)"),
    "K4": ("EVET", "çöküşler arası en az 250 işlem günü; her hisse olay başına bir kez; n = hisse sayısı; ortalama yanında medyan r250"),
    "K5": ("EVET", "giriş = çöküş + 5. işlem günü AÇILIŞI (karar günü kapanışı değil); bar yoksa 5 gün içindeki ilk geçerli açılış"),
    "K6": ("EVET", "V_BIST tek kip düzeltilmiş fiyat; bölünme şüphesi SY.sy_bolunme_supheli ANA ile [giriş-260 bar, ufuk sonu] içinde olan hisse çıkar ve sayısı yazılır; likidite TL (dilim içi sıralama, birim farkı etkilemez)"),
    "K7": ("EVET", "evren bugün işlem görenler (V_BIST 581); 2018 / 2020 batanları yok -> P(-%50) aşağı, P(+%100) yukarı yanlı; RAPOR'da HAYATTA KALMA UYARISI bölümü"),
    "K8": ("EVET", "hücre n < 30 -> ÖLÇÜLEMEDİ; iki çöküş ayrı hücre + birleşik, Ha her olayda aynı yön şartı; üç (a) testi BH (bilgi); iki olay = en fazla EMARE"),
    "K9": ("EVET", "iş tanımı commit 69fbed0 koşudan önce; CO_ESIK sha256 mühürü + kod sha + veri sha ON_KAYIT.md'de, kos mühür farklıysa durur; git commit alt ajana yasak -> ON_KAYIT commit'i ana modelde (zaman damgası dosyada)"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırması yok; yalnız fiyat-hacim; fon tablosu FON_IZI.FI_TASFIYE_RE ile mevcut ayrıştırılmış G.pkl'den"),
    "K11": ("EVET", "olay satırları csv.gz'ye yazılır; test_cokus_oynak.py en az iki hücreyi (2018 ve 2020 OYNAK P100 / M50) satır dosyasından bağımsız yeniden üretir"),
    "K12": ("EVET", "fiyat değişimi (kapanış / giriş) ile gerçekleşen kâr ayrı; 'emare / piyango' yalnız önceden yazılı kuralla; sayı ve yorum ayrı cümle; hiçbir isme alım dili yok"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_co); defter dosyaları ve mevcut .py değişmez; e-posta / anahtar taraması testte; commit / push yok; kod değişirse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri işi değil, aday listesi; boyut / çıkış kuralı yok, alım dili yok; taban oran (3 yılda 10x ~%1-1,85) RAPOR'da yazılı"),
}


# ---------------------------------------------------------------- 6) ÖN KAYIT
def co_onkayit(veri: Optional[str] = None, canli: Optional[str] = None) -> Dict[str, Any]:
    veri = veri or CO_YOL["veri"]; canli = canli or CO_YOL["canli"]
    os.makedirs(CO_YOL["cikti"], exist_ok=True)
    V = co_veri(veri)
    T, C = co_takvim(V)
    M = co_medyan120(C)
    gun = co_cokus_gunleri(M)
    say = []
    for t in gun:
        i = T.get_loc(t)
        gi = i + CO_ESIK["giris_gecikme"]
        tam = gi + CO_ESIK["ufuk"] < len(T) and T[min(gi + CO_ESIK["ufuk"], len(T) - 1)] <= pd.Timestamp(CO_ESIK["kriz"])
        say.append({"cokus": str(t.date()), "medyan_r120": round(float(M.medyan.loc[t]), 4), "n_hisse": int(M.n.loc[t]),
                    "giris": str(T[gi].date()) if gi < len(T) else "-", "sonuc_olculur": bool(tam)})
    min_t = M.medyan.idxmin()
    J = {"surum": CO_SURUM, "zaman": _dt.datetime.now(_dt.timezone.utc).isoformat(), "muhur": co_muhur(), "kod_sha": _co_kod_sha(),
         "veri_sha": {f: _co_sha(os.path.join(veri, f)) for f in ("V_BIST.pkl", "G.pkl", "dol.pkl")},
         "canli_sha": _co_sha(os.path.join(canli, "bist_3y.pkl")), "takvim": [str(T[0].date()), str(T[-1].date()), len(T)],
         "cokus": say, "medyan_en_dusuk": [str(min_t.date()), float(M.medyan.min())]}
    L = [f"# ÇÖKÜŞ SONRASI OYNAK HİSSE — ÖN KAYIT ({CO_SURUM})", "",
         f"Zaman (UTC): {J['zaman']}. İş tanımı: COKUS_OYNAK_IS_TANIMI.md (commit 69fbed0). Bu dosya getiri hesaplanmadan yazıldı: yalnız çöküş günü SAYIMI.",
         "Git commit alt ajana yasak: bu dosyanın commit'i ana modelde; kos mühür / kod sha denetler.", "",
         "## MÜHÜR", "", f"- CO_ESIK sha256: `{J['muhur']}`", f"- COKUS_OYNAK.py sha256: `{J['kod_sha']}`",
         *[f"- {k} sha256: `{v}`" for k, v in J["veri_sha"].items()], f"- canlı bist_3y.pkl sha256: `{J['canli_sha']}`", "",
         "## EŞİKLER (CO_ESIK; sonuç görüldükten sonra değişmez)", "", "```json", json.dumps(CO_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## OLAY SAYIMI (getirisiz)", "", f"Ortak takvim {J['takvim'][0]} .. {J['takvim'][1]} ({J['takvim'][2]} gün, en az 50 hisseli gün). "
         f"Evren medyan 120 gün getirisinin en düşük değeri: {J['medyan_en_dusuk'][1]:+.3f} ({J['medyan_en_dusuk'][0]}).", "",
         "| Çöküş günü | Medyan r120 | Hisse | Giriş (+5) | Sonuç ölçülür |", "|---|---|---|---|---|"]
    L += [f"| {x['cokus']} | {x['medyan_r120']:+.3f} | {x['n_hisse']} | {x['giris']} | {'EVET' if x['sonuc_olculur'] else 'HAYIR (kriz kesiği / ufuk)'} |" for x in say]
    if not say:
        L += ["| (yok) | | | | |"]
    ntam = sum(1 for x in say if x["sonuc_olculur"])
    L += ["", f"Sonucu ölçülebilir çöküş sayısı: {ntam}. Karar kuralı gereği < 2 ise birincil etiket ÖLÇÜLEMEDİ olur (tanım değiştirilmez; "
          "iş tanımının beklediği 2018 / 2020 ana tanımda çöküş değildir).",
          "Getiri görülmeden eklenen BİLGİ hücreleri (karar dışı): CO_ESIK['bilgi_olay'] — 2018-08-20 ve 2020-03-19 (yılın en düşük medyan r120 günü; "
          "geriye bakarak seçildi). Normal dönem 2023 girişi (2023-01-02) 250 gün penceresi 2023 çöküşünü içerir; kıyas buna göre okunur."]
    L += ["", "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    import IZ_KARNE as IK
    for k in IK.IK_KONTROL:
        y, kn = CO_KONTROL.get(k["kod"], ("", ""))
        L.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    open(os.path.join(CO_YOL["cikti"], "ON_KAYIT.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    with open(os.path.join(CO_YOL["cikti"], "on_kayit.json"), "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1)
    colog.info("ön kayıt yazıldı: %d çöküş günü", len(say))
    return J


# ---------------------------------------------------------------- 7) KOŞU
def co_kos(veri: Optional[str] = None, canli: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    veri = veri or CO_YOL["veri"]; canli = canli or CO_YOL["canli"]
    onk = os.path.join(CO_YOL["cikti"], "ON_KAYIT.md")
    kapi = IK.ik_kontrol_kapisi(onk)
    colog.info("kontrol kapısı açık (%d madde)", kapi["n"])
    J0 = json.load(open(os.path.join(CO_YOL["cikti"], "on_kayit.json"), encoding="utf-8"))
    if J0["muhur"] != co_muhur():
        raise COHata("CO_ESIK mühürü ön kayıttan farklı: eşik sonuçtan sonra değişemez")
    sapma = []
    if J0["kod_sha"] != _co_kod_sha():
        sapma.append("kod sha ön kayıttan farklı (eşik mühürü aynı; değişiklik yalnız kod / gösterim olmalı, RAPOR SAPMA bölümüne bakın)")
    for f in ("V_BIST.pkl", "G.pkl", "dol.pkl"):
        if J0["veri_sha"][f] != _co_sha(os.path.join(veri, f)):
            raise COHata(f"veri sha ön kayıttan farklı: {f}")
    if J0["canli_sha"] != _co_sha(os.path.join(canli, "bist_3y.pkl")):
        raise COHata("canlı veri sha ön kayıttan farklı")
    sapma.append("İLK KOŞU HATASI: 2026 çöküşünde kesik veride hisse kalmayınca co_dilimle boş tabloda düştü; giriş kriz kesiğinden sonraysa olay "
                 "'sonuç yok' yazılıp atlanır (kod düzeltmesi, eşik değişmedi).")
    sapma.append("K6 (ilk koşudan sonra): bugünün listesindeki ilk 15 hissenin hepsinde ham veride > %25 tek gün sıçrama vardı; bir kısmı kilitli taban "
                 "serisi (gerçek), bir kısmı Yahoo'da düzeltilmemiş bedelsiz (ör. ardışık iki ham günde -%86). " + CO_SAPMA["tanim"])
    E = CO_ESIK
    V = co_veri(veri)
    T, C = co_takvim(V)
    M = co_medyan120(C)
    gun = co_cokus_gunleri(M)
    Vk = {s: d[d.index <= pd.Timestamp(E["kriz"])] for s, d in V.items()}
    Vk = {s: d for s, d in Vk.items() if len(d)}
    bolm = {s: _co_bolunme(d) for s, d in Vk.items()}
    Vham = pd.read_pickle(os.path.join(veri, "V_BIST.pkl"))
    if isinstance(Vham, dict) and "veri" in Vham and isinstance(Vham["veri"], dict):
        Vham = Vham["veri"]
    hamm = {str(s): co_ham_sicrama(d[d.index <= pd.Timestamp(E["kriz"])]) for s, d in Vham.items() if str(s) in Vk}
    del Vham
    olaylar: List[pd.DataFrame] = []
    tanim = []
    for t in gun:
        i = T.get_loc(t)
        for gec, tur in ((E["giris_gecikme"], "cokus"), (E["giris_gecikme_ek"], "cokus_ek20")):
            gi = i + gec
            if gi >= len(T):
                continue
            if T[gi] > pd.Timestamp(E["kriz"]):
                tanim.append({"olay": f"{t.year}", "tur": tur, "cokus": str(t.date()), "karar": str(T[gi - 1].date()), "giris": str(T[gi].date()),
                              "medyan_r120": float(M.medyan.loc[t]), "n_evren": 0, "n_sonuc": 0, "n_bolunme": 0,
                              "sonuc_yok": {"giriş kriz kesiğinden (31.08.2026) sonra": 1}})
                continue
            ad = f"{t.year}"
            D = co_olay(Vk, T, gi, ad, tur, bolm, E["kriz"], hamm)
            olaylar.append(D)
            tanim.append({"olay": ad, "tur": tur, "cokus": str(t.date()), "karar": str(T[gi - 1].date()), "giris": str(T[gi].date()),
                          "medyan_r120": float(M.medyan.loc[t]), "n_evren": int(len(D)),
                          "n_sonuc": int(_co_olcum(D).shape[0]), "n_bolunme": int(D.get("bolunme", pd.Series(dtype=bool)).fillna(False).sum()),
                          "sonuc_yok": D["sonuc_yok"].dropna().value_counts().to_dict() if "sonuc_yok" in D else {}})
            colog.info("olay %s %s: giriş %s, evren %d", ad, tur, T[gi].date(), len(D))
    for ad, tb in [(k, v) for k, v in E["bilgi_olay"].items() if k != "tanim"]:
        gi = int(T.searchsorted(pd.Timestamp(tb))) + E["giris_gecikme"]
        D = co_olay(Vk, T, gi, ad, "bilgi", bolm, E["kriz"], hamm)
        olaylar.append(D)
        tanim.append({"olay": ad, "tur": "bilgi", "cokus": tb, "karar": str(T[gi - 1].date()), "giris": str(T[gi].date()),
                      "medyan_r120": float(M.medyan.loc[pd.Timestamp(tb)]), "n_evren": int(len(D)), "n_sonuc": int(_co_olcum(D).shape[0]),
                      "n_bolunme": int(D.get("bolunme", pd.Series(dtype=bool)).fillna(False).sum()), "sonuc_yok": {}})
    for y in E["normal"]["yillar"]:
        gi = int(T.searchsorted(pd.Timestamp(f"{y}-01-01")))
        D = co_olay(Vk, T, gi, f"N{y}", "normal", bolm, E["kriz"], hamm)
        olaylar.append(D)
        tanim.append({"olay": f"N{y}", "tur": "normal", "cokus": "-", "karar": str(T[gi - 1].date()), "giris": str(T[gi].date()),
                      "medyan_r120": float(M.medyan.iloc[gi - 1]), "n_evren": int(len(D)), "n_sonuc": int(_co_olcum(D).shape[0]),
                      "n_bolunme": int(D.get("bolunme", pd.Series(dtype=bool)).fillna(False).sum()), "sonuc_yok": {}})
    TUM = pd.concat(olaylar, ignore_index=True)
    # tablolar
    tablo: Dict[str, Any] = {}
    gruplar: Dict[str, List[str]] = {}
    tam_cokus = [x["olay"] for x in tanim if x["tur"] == "cokus" and x["n_sonuc"] > 0]
    for tur in ("cokus", "cokus_ek20", "bilgi", "normal"):
        ol = [x["olay"] for x in tanim if x["tur"] == tur and x["n_sonuc"] > 0]
        gruplar[tur] = ol
        for ad, a, b in KARS:
            hucre = {}
            for o in ol:
                Do = _co_olcum(TUM[(TUM.olay == o) & (TUM.tur == tur)])
                hucre[o] = co_karsilas([Do], a, b, CO_ESIK["bootstrap"]["tohum"])
            if len(ol) >= 2:
                hucre["BIRLESIK"] = co_karsilas([_co_olcum(TUM[(TUM.olay == o) & (TUM.tur == tur)]) for o in ol], a, b, CO_ESIK["bootstrap"]["tohum"])
            tablo[f"{tur}|{ad}"] = hucre
    duy: Dict[str, Any] = {}          # SAPMA (K6): ham sıçramalı hisseler çıkarılmış duyarlılık (bilgi)
    for tur in ("cokus", "bilgi", "normal"):
        ol = gruplar.get(tur, [])
        for ad, a, b in KARS:
            hucre = {}
            parca = []
            for o in ol:
                Do = _co_olcum(TUM[(TUM.olay == o) & (TUM.tur == tur)])
                Do = Do[Do.get("ham_sicrama", False) != True]  # noqa: E712
                parca.append(Do)
                hucre[o] = co_karsilas([Do], a, b, CO_ESIK["bootstrap"]["tohum"])
            if len(ol) >= 2:
                hucre["BIRLESIK"] = co_karsilas(parca, a, b, CO_ESIK["bootstrap"]["tohum"])
            duy[f"{tur}|{ad}"] = hucre
    karar: Dict[str, Any] = {}
    for ad, _, _ in KARS[:3]:
        h = tablo.get(f"cokus|{ad}", {})
        olay_h = {o: h[o] for o in tam_cokus if o in h}
        karar[ad] = co_etiket(olay_h, h.get("BIRLESIK", {}), len(tam_cokus)) if "BIRLESIK" in h else co_etiket(olay_h, {}, len(tam_cokus))
    bilgi_ol = gruplar.get("bilgi", [])
    karar_bilgi = {ad: co_etiket({o: tablo[f"bilgi|{ad}"][o] for o in bilgi_ol}, tablo[f"bilgi|{ad}"].get("BIRLESIK", {}), len(bilgi_ol))
                   for ad, _, _ in KARS[:3] if f"bilgi|{ad}" in tablo}
    p = [tablo.get(f"cokus|{ad}", {}).get("BIRLESIK", {}).get("p_tek_P100", np.nan) for ad, _, _ in KARS[:3]]
    bh = _bh([x if x == x else 1.0 for x in p])
    bugun = co_bugun(canli, veri)
    S = {"surum": CO_SURUM, "zaman": _dt.datetime.now(_dt.timezone.utc).isoformat(), "muhur": co_muhur(), "kod_sha": _co_kod_sha(),
         "on_kayit_zaman": J0["zaman"], "sapma": sapma, "olaylar": tanim, "gruplar": gruplar, "tablo": tablo, "duyarlilik": duy, "karar": karar, "karar_bilgi": karar_bilgi,
         "bh": {ad: {"p": p[k], "q": bh[k]} for k, (ad, _, _) in enumerate(KARS[:3])}, "bugun": bugun,
         "cokus_gunleri": [str(t.date()) for t in gun]}
    kol = ["olay", "tur", "sembol", "karar", "giris_gunu", "giris_bar", "giris", "sigma250", "dusus250", "likidite", "r60_once", "liq_alt",
           "sig_pct", "dd_pct", "OYNAK", "TABAN", "DUSMUS", "TABAN_D", "CAPRAZ", "PROFIL", "bolunme", "sonuc_yok", "p100", "m50", "ilk",
           "r120", "r250", "mdd60", "n_bar_ufuk", "yarim", "ham_sicrama"]
    TUM[[c for c in kol if c in TUM.columns]].to_csv(os.path.join(CO_YOL["cikti"], "cokus_oynak_olay.csv.gz"), index=False,
                                                       compression="gzip", float_format="%.6g")
    with open(os.path.join(CO_YOL["cikti"], "sonuc.json"), "w", encoding="utf-8") as f:
        json.dump(S, f, ensure_ascii=False, indent=1, default=_co_json)
    co_rapor(S)
    return S


def _co_json(o: Any) -> Any:
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, _dt.date)):
        return str(o.date()) if isinstance(o, pd.Timestamp) else str(o)
    return str(o)


# ---------------------------------------------------------------- 8) RAPOR
def _y(x: Any, n: int = 1) -> str:
    try:
        if x is None or x != x:
            return "-"
        return f"%{100 * x:.{n}f}".replace(".", ",")
    except Exception:
        return "-"


def _k(x: Any) -> str:
    try:
        return "-" if x is None or x != x else f"{x:.2f}".replace(".", ",")
    except Exception:
        return "-"


def _co_tablo_md(S: Dict[str, Any], tur: str) -> List[str]:
    L = ["| Olay | Dilim | n | P(+%100) | P(-%50) | Medyan r250 | Ort. r250 | Medyan MDD60 | Kat +100 | Fark +100 [%95] | Kat -50 | Fark -50 [%95] | Perm. p |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for ad, a, b in KARS:
        h = S["tablo"].get(f"{tur}|{ad}", {})
        for o, k in h.items():
            if not k.get("A") or k["A"].get("n", 0) == 0:
                L.append(f"| {o} | {a} | 0 | - | - | - | - | - | - | - | - | - | - |"); continue
            A, B = k["A"], k["B"]
            L.append(f"| {o} | {a} | {A['n']} | {_y(A['P100'])} | {_y(A['M50'])} | {_y(A['med_r250'])} | {_y(A['ort_r250'])} | {_y(A['med_mdd60'])} | "
                     f"{_k(k.get('kat_P100'))} | {_y(k.get('fark_P100'))} [{_y(k.get('bs_P100', [None])[0])}, {_y(k.get('bs_P100', [None, None])[1])}] | "
                     f"{_k(k.get('kat_M50'))} | {_y(k.get('fark_M50'))} [{_y(k.get('bs_M50', [None])[0])}, {_y(k.get('bs_M50', [None, None])[1])}] | {_k(k.get('perm_p_P100'))} |")
            if ad == "OYNAK" or ad == "DUSMUS":
                bn = "TABAN" if ad == "OYNAK" else "TABAN_D"
                L.append(f"| {o} | {bn} | {B['n']} | {_y(B['P100'])} | {_y(B['M50'])} | {_y(B['med_r250'])} | {_y(B['ort_r250'])} | {_y(B['med_mdd60'])} | 1 | | 1 | | |")
    return L


def co_rapor(S: Optional[Dict[str, Any]] = None) -> str:
    if S is None:
        S = json.load(open(os.path.join(CO_YOL["cikti"], "sonuc.json"), encoding="utf-8"))
    K = S["karar"]; Bg = S["bugun"]
    def _o(tur, ad, o="BIRLESIK"):
        h = S["tablo"].get(f"{tur}|{ad}", {})
        if o == "BIRLESIK" and o not in h and len(h) == 1:
            return next(iter(h.values()))
        return h.get(o, {})
    ob = _o("cokus", "OYNAK"); pr = _o("cokus", "PROFIL")
    nb = {o: _o("normal", "OYNAK", o) for o in S["gruplar"].get("normal", [])}
    L = [f"# ÇÖKÜŞ SONRASI OYNAK HİSSE — RAPOR ({S['surum']})", "",
         f"Üreten: `python COKUS_OYNAK.py kos`. Ön kayıt: ON_KAYIT.md ({S['on_kayit_zaman']}); mühür `{S['muhur'][:16]}`. Koşu: {S['zaman']}.", "",
         "## ÖZET (bulgu)", ""]
    if ob.get("A"):
        L += [f"- Çöküşten (+5 gün) sonra en oynak beşlik, 250 günde: P(+%100) {_y(ob['A']['P100'])} (orta üç beşlik {_y(ob['B']['P100'])}; kat {_k(ob.get('kat_P100'))}), "
              f"P(-%50) {_y(ob['A']['M50'])} (orta {_y(ob['B']['M50'])}; kat {_k(ob.get('kat_M50'))}); medyan r250 {_y(ob['A']['med_r250'])} / {_y(ob['B']['med_r250'])}; n {ob['A']['n']} / {ob['B']['n']}."]
    for o, k in nb.items():
        if k.get("A"):
            L.append(f"- Normal dönem {o[1:]} başı: oynak P(+%100) {_y(k['A']['P100'])} / orta {_y(k['B']['P100'])} (kat {_k(k.get('kat_P100'))}); "
                     f"P(-%50) {_y(k['A']['M50'])} / {_y(k['B']['M50'])} (kat {_k(k.get('kat_M50'))}).")
    L += [f"- KARAR (önceden yazılı kural, OYNAK): **{K['OYNAK']['etiket']}**. En çok düşmüş beşlik: {K['DUSMUS']['etiket']}; çapraz: {K['CAPRAZ']['etiket']}.",
          f"- Bugün (karar {Bg['karar']}): evren medyan 120 gün getirisi {_y(Bg['evren_medyan_r120'])} -> çöküş eşiği (-%30) {'GEÇİLDİ' if Bg['esik_gecti'] else 'geçilmedi'}; piyango profilinde {Bg['n_profil']} hisse.",
          "- Hayatta kalma: yalnız bugün işlem gören hisseler; batanlar yok -> P(-%50) gerçekte daha yüksek, P(+%100) daha düşük olabilir.", "",
          "## ÇÖKÜŞ GÜNLERİ", "", "| Olay | Tür | Çöküş günü | Medyan r120 | Karar | Giriş | Evren | Sonuçlu (bölünmesiz) | Bölünme şüphesiyle çıkan | Sonuç yok |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for x in S["olaylar"]:
        L.append(f"| {x['olay']} | {x['tur']} | {x['cokus']} | {_y(x['medyan_r120'])} | {x['karar']} | {x['giris']} | {x['n_evren']} | {x['n_sonuc']} | {x['n_bolunme']} | "
                 f"{'; '.join(f'{k}: {v}' for k, v in x['sonuc_yok'].items()) or '-'} |")
    L += ["", f"Tespit edilen bütün çöküş günleri: {', '.join(S['cokus_gunleri']) or 'yok'}. 2026 çöküşünün sonucu kriz kesiği (31.08.2026) yüzünden ölçülemez.", "",
          "## OLASILIK TABLOSU (ana giriş: çöküş + 5 işlem günü açılışı; ufuk 250 işlem günü)", "",
          "P(+%100) = 250 gün içinde bir kapanış >= 2 x giriş; P(-%50) = bir kapanış <= 0,5 x giriş. Kat = dilim / taban. Fark aralığı: hisse düzeyinde bootstrap %95 (1.000; birleşikte olay içi katmanlı). Perm. p: olay içi etiket karıştırma, tek yönlü (P+100). "
          "TABAN = σ250 orta üç beşlik (DUSMUS için düşüş orta üç beşliği TABAN_D). PROFIL = OYNAK ve zirveden >= %60 düşmüş.", ""]
    L += _co_tablo_md(S, "cokus")
    L += ["", "## KARAR (önceden yazılı kural)", ""]
    for ad in ("OYNAK", "DUSMUS", "CAPRAZ"):
        k = K[ad]
        L.append(f"- {ad}: **{k['etiket']}** — {k.get('neden', '')}. BH q (P+100, tek yönlü): {_k(S['bh'][ad]['q'])}.")
    for ad, k in S.get("karar_bilgi", {}).items():
        L.append(f"- BİLGİ (2018B + 2020B, geriye bakarak seçilmiş dip günleri; karar değil) {ad}: {k['etiket']} — {k.get('neden', '')}.")
    L += ["- Birincil karar OYNAK satırıdır; iki çöküş = iki olay olduğu için kural tutsa bile en fazla EMARE (İZ değil).", "",
          "## EK GİRİŞ (bilgi): çöküş + 20 işlem günü", ""]
    L += _co_tablo_md(S, "cokus_ek20")
    L += ["", "## BİLGİ: 2018 ve 2020 dip günleri (ana tanımda çöküş değil; geriye bakarak seçildi, karar dışı)", "",
          CO_ESIK["bilgi_olay"]["tanim"] + ".", ""]
    L += _co_tablo_md(S, "bilgi")
    L += ["", "## DUYARLILIK (SAPMA, bilgi): ham veride > %25 tek gün sıçraması olan hisseler çıkarılınca", "",
          CO_SAPMA["tanim"], ""]
    Sd = dict(S); Sd["tablo"] = S.get("duyarlilik", {})
    for tur in ("cokus", "bilgi", "normal"):
        L += [f"**{tur}**", ""] + _co_tablo_md(Sd, tur) + [""]
    L += ["", "## NORMAL DÖNEM KIYASI (yılın ilk işlem günü girişi; aynı tablo)", ""]
    L += _co_tablo_md(S, "normal")
    L += ["", "Not: 2017 ve 2023 BIST'te güçlü yükseliş yıllarıdır (2023 yüksek TL enflasyonu); 'normal' dönem nötr değildir, kıyas kat ve fark üzerinden okunmalıdır.", "",
          "## BUGÜNÜN LİSTESİ (aday listesi, ölçüm değil; hiçbir isim için alım dili yok)", ""]
    if pr.get("A"):
        L.append(f"Geçmişte bu profil (OYNAK ve zirveden >= %60 düşmüş; çöküş + 5 gün, birleşik): P(+%100) = {_y(pr['A']['P100'])}, P(-%50) = {_y(pr['A']['M50'])}, "
                 f"medyan r250 {_y(pr['A']['med_r250'])}, n = {pr['A']['n']}" + (" (n < 30: örneklem yetersiz)" if pr['A']['n'] < 30 else "") + ".")
        for o in S["gruplar"].get("cokus", []):
            po = _o("cokus", "PROFIL", o)
            if po.get("A"):
                L.append(f"- {o}: n {po['A']['n']}, P(+%100) {_y(po['A']['P100'])}, P(-%50) {_y(po['A']['M50'])}.")
    else:
        L.append("Geçmişte bu profil: ölçülemedi (n = 0).")
    L += ["", f"Karar günü {Bg['karar']}: evren {Bg['n_evren']} hisse, likidite süzgecinden sonra {Bg['n_likit']}; σ250 üst beşlik {Bg['n_oynak']}; bunlardan zirveden >= %60 düşmüş {Bg['n_oynak_dusus60']}; "
          f"fon lekesiyle çıkan {Bg['n_leke_ele']}, Uzak listesiyle çıkan {Bg['n_uzak_ele']}; profil {Bg['n_profil']}. "
          f"Ölçüler düzeltilmemiş sermaye işlemine karşı geriye düzeltilmiş fiyatla (SAPMA K6): evrende {Bg.get('n_ham_duzeltilen', '-')} hisse, profilde {Bg.get('n_profil_duzeltilen', '-')} hisse düzeltildi. "
          "σ250 kilitli taban / tavan günlerini (H = L) atlayan geçerli bar getirileriyle hesaplanır: fon krizinde taban serisi yaşayan hissenin σ'sı bu yüzden çok yüksektir.", "",
          "| # | Sembol | σ250 (günlük) | Zirveden düşüş | r60 | Likidite 60g (mn TL) | Fon | S6 durumu | Son 20 günde en büyük gün | Ham düzeltme |", "|---|---|---|---|---|---|---|---|---|---|"]
    for j, r in enumerate(Bg["liste"][:CO_ESIK["bugun"]["ilk"]], 1):
        L.append(f"| {j} | {r['sembol']} | {_y(r['sigma250'], 2)} | {_y(r['dusus250'])} | {_y(r['r60_once'])} | {r['likidite'] / 1e6:.1f} | "
                 f"{'temiz' + (' (' + str(r.get('fon_son_ay')) + ')' if isinstance(r.get('fon_son_ay'), str) else ' (fon yok)')} | {r.get('s6', '-')} | "
                 f"{_y(r['son20_en_buyuk_gun'])} ({r['son20_en_buyuk_tarih']}) | {r.get('ham_duzeltme', 0)} |")
    L += ["", "## HAYATTA KALMA UYARISI", "",
          "Evren V_BIST'teki bugün işlem gören 581 hissedir. 2018 ve 2020 çöküşlerinden sonra kottan çıkan / batan hisseler veride yoktur. Bu yüzden ölçülen P(-%50) "
          "gerçek değerden DÜŞÜK, P(+%100) ve medyan r250 YÜKSEK olabilir; en çok etkilenen dilim en oynak ve en çok düşmüş hisselerdir (batanlar çoğunlukla orada). "
          "Hb'nin (risk büyük değil) tutması bu yanlılıkla kısmen açıklanabilir. 3 yılda 10x taban oranı (BIST USD ~%1,85) değişmez.", "",
          "## KONTROL LİSTESİ", "", "| Kod | Yanıt | Kanıt |", "|---|---|---|"]
    L += [f"| {k} | {v[0]} | {v[1]} |" for k, v in CO_KONTROL.items()]
    L += ["", "## SAPMA", ""] + ([f"- {x}" for x in S["sapma"]] or ["- yok"])
    L += ["", "## HATA", ""] + [f"- {h}" for h in CO_HATA] + ["",
          "## ÖNERİLEN DEFTER METNİ (ana model işler)", "",
          f"- IK_KAYIT Ç satırı: 'ÇÖKÜŞ SONRASI OYNAK (Cemal hipotezi, 16 Kas): BIST çöküş günleri {', '.join(S['cokus_gunleri'])}; OYNAK (σ250 üst beşlik) vs orta üç beşlik, 250 gün: "
          + (f"P(+%100) {_y(ob['A']['P100'])} / {_y(ob['B']['P100'])}, P(-%50) {_y(ob['A']['M50'])} / {_y(ob['B']['M50'])}; " if ob.get('A') else "")
          + f"karar {K['OYNAK']['etiket']} (iki olay; İZ değil); hayatta kalma yanlılığı yukarı.'",
          "- IK_ILERI satırı: '2026 çöküşü (V_BIST kesiksiz tespit) sonucu: Mart 2027 (r120) ve Kasım 2027 (r250) aynı komut (`python COKUS_OYNAK.py kos`, aynı CO_ESIK, kriz kesiği kaldırılmış ayrı ön kayıtla), aynı eşik.'"]
    m = "\n".join(L) + "\n"
    open(os.path.join(CO_YOL["cikti"], "RAPOR.md"), "w", encoding="utf-8").write(m)
    return m


# ---------------------------------------------------------------- 9) ÇAKIŞMA KAPISI
def _cakisma_kontrol_co(_once=_CK_ONCE_CO, _dosya="COKUS_OYNAK.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_CO", "_CK_KAYIT", "_cakisma_kontrol_co", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "re", "argparse", "hashlib", "traceback", "_dt", "annotations",
           "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_co()

if __name__ == "__main__" and "get_ipython" not in globals():
    ap = argparse.ArgumentParser(description=CO_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor"])
    ap.add_argument("--veri", default=None)
    ap.add_argument("--canli", default=None)
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            J_ = co_onkayit(a.veri, a.canli)
            print(json.dumps({"cokus": J_["cokus"], "muhur": J_["muhur"]}, ensure_ascii=False))
        elif a.komut == "kos":
            S_ = co_kos(a.veri, a.canli)
            print(json.dumps({k: v["etiket"] for k, v in S_["karar"].items()}, ensure_ascii=False))
        else:
            co_rapor()
    except COHata as ex:
        colog.error("%s", ex); sys.exit(1)
