"""FITIL_OBEK — Cemal'in fitil öbeği hipotezi (16 Kasım 2026), ORTAK_CETVEL v1.0 ile tek dosya ölçüm.

Cemal: "PAPIL'de alt fitil yok, üst fitil biraz uzun mumlar öbek olunca has yukarı çıkma mumları; DGXX'te tersi (üst fitil yok, aşağı sert
dişler)." Hipotez H: son k geçerli barda fitil asimetrisi yönü öngörür. S+ (YUKARI öbek: üst fitiller baskın, alt fitilsiz barlar çoğunlukta)
-> sonraki 60 günde eşlerden iyi; S- (AŞAĞI öbek: alt fitiller baskın, üst fitilsiz barlar çoğunlukta) -> eşlerden kötü (kaçınma, ayna şart).
İş tanımı: arastirma_cikti/fitil_obek/FITIL_OBEK_IS_TANIMI.md (koşudan önce git'e işlendi). Ölçüm cetveli ORTAK_CETVEL değişmez.

Komut:  python FITIL_OBEK.py onkayit [--veri K] [--uzerine-yaz]   ON_KAYIT.md (mühür, kod sha, veri sha, olay sayımı GETİRİSİZ, kontrol listesi)
        python FITIL_OBEK.py kos [--veri K] [--gitsiz]            ölçüm (IZ_KARNE.ik_kontrol_kapisi + ORTAK_CETVEL.oc_kapi + kendi mühür kapısı)
        python FITIL_OBEK.py rapor [--ek DOSYA]                   sonuc.json -> RAPOR.md (ek: HATA / denetim / defter metni bölümleri)
        python FITIL_OBEK.py ornek [--veri K]                     örnek doğrulama (PAPIL, DGXX, FENER, DESA, YKSLN); getirisiz
Colab:  exec(open('FITIL_OBEK.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   ORTAK_CETVEL.oc_veri (V_BIST / V_ABD / V_AVR; k34_yahoo varsa ABD'ye eklenir). DGXX Eki-Kas 2026 (kriz kesiği sonrası) yalnız örnek
        doğrulama için yfinance'tan indirilir; ölçüme girmez.
Komisyon / kayma yok. Evren bugün işlem gören hisseler: hayatta kalma yanlılığı (getiriler yukarı, -%50 olasılığı aşağı yanlı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_FO = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_FO = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_FO not in sys.path:
    sys.path.insert(0, KOK_FO)

import ORTAK_CETVEL as OC  # noqa: E402

folog = logging.getLogger("col.fitil_obek")
if not folog.handlers:
    _fo_h = logging.StreamHandler(sys.stderr)
    _fo_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s fitil_obek: %(message)s", "%H:%M:%S"))
    folog.addHandler(_fo_h)
    folog.setLevel(logging.INFO)
    folog.propagate = False

FO_SURUM = "FITIL_OBEK v1.0 (2026-11-16): fitil öbeği (S+ alt fitilsiz / S- üst fitilsiz), ORTAK CETVEL v1.0 ile"
FO_YOL = {"cikti": os.path.join(KOK_FO, "arastirma_cikti", "fitil_obek"), "kod": os.path.join(KOK_FO, "FITIL_OBEK.py"),
          "is_tanimi": os.path.join(KOK_FO, "arastirma_cikti", "fitil_obek", "FITIL_OBEK_IS_TANIMI.md"),
          "veri": os.environ.get("OC_VERI", "/tmp/veri"), "veri2": os.environ.get("OC_VERI2", "/tmp/veri2"),
          "satir": os.environ.get("FO_SATIR", "/tmp/fitil_obek")}
FO_DOSYA = {"onkayit": "ON_KAYIT.md", "sonuc": "sonuc.json", "rapor": "RAPOR.md", "olay": "olay_ana.csv.gz", "ornek": "ornek.json"}

# ================================================================ MÜHÜRLÜ TANIM (sonuç görüldükten sonra DEĞİŞMEZ)
FO_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "bar": "geçerli bar (OC.oc_veri temiz: H > L, V > 0, fiyat > 0); R = H - L; alt = (min(O,C) - L) / R; üst = (H - max(O,C)) / R; "
           "gövde = |C - O| / R",
    "fitil_yok": 0.10,
    "k_ana": 10, "k_bilgi": [5, 15],
    "pencere": "son k geçerli bar (t dahil, rolling; yalnız t'ye kadar bilgi). A = ortalama alt, U = ortalama üst, ASIM = U - A; "
               "ALTYOK = alt < 0,10 bar payı; USTYOK = üst < 0,10 bar payı",
    "s_arti": {"asim_min": 0.20, "altyok_min": 0.50},
    "s_eksi": {"asim_max": -0.20, "ustyok_min": 0.50},
    "kucuk": {"carpan": 0.75, "atr_gun": 250, "atr_min": 120,
              "tanim": "KUCUK = pencere medyanı (R / C) <= 0,75 x ATR%250; ATR%250 = t'de biten 250 geçerli barın (en az 120) ortalama TR / C; "
                       "TR = max(H, önceki geçerli kapanış) - min(L, önceki geçerli kapanış)"},
    "onda": {"ust": 0.90, "alt": 0.10, "min_hisse": 30,
             "tanim": "aynı gün (t), aynı pazarda k=10 ASIM'i tanımlı hisseler arasında yüzdelik sıra (rank pct, ortalama bağ); > 0,90 -> "
                      "S+ onda; <= 0,10 -> S- onda (50 hissede 5 / 5); o gün en az 30 hisse (yalnız t günü bilinen)"},
    "satirlar": {
        "SP_k10": "S+ (YUKARI öbek) k=10: ASIM >= 0,20 VE ALTYOK >= 0,50 [ANA]",
        "SM_k10": "S- (AŞAĞI öbek) k=10: ASIM <= -0,20 VE USTYOK >= 0,50 [ANA]",
        "SP_k5": "S+ k=5 [bilgi]", "SM_k5": "S- k=5 [bilgi]", "SP_k15": "S+ k=15 [bilgi]", "SM_k15": "S- k=15 [bilgi]",
        "SP_kucuk": "S+ k=10 VE KUCUK [bilgi]", "SM_kucuk": "S- k=10 VE KUCUK [bilgi]",
        "SP_onda": "S+ yalnız ASIM üst %10 (k=10, günlük kesit) [bilgi]", "SM_onda": "S- yalnız ASIM alt %10 (k=10, günlük kesit) [bilgi]"},
    "ana": ["SP_k10", "SM_k10"],
    "yon": {"SP": "+", "SM": "-"},
    "olay": "DURUM GÜNLERİ: şartın t (pencerenin son günü) kapanışında doğru olduğu her geçerli bar OC.oc_olc'a verilir; giriş t'den sonraki "
            "ilk geçerli açılış, tekilleştirme 60 gün (cetvel: ilk durum günü tutulur)",
    "karar": {
        "arti": "S+ beklenen yön yukarı: hücre durumu ORTAK_CETVEL oc_hucre 'tutar' (dört şart + iki yarı > 0) ve oc_hucre_durum",
        "eksi": "S- beklenen yön aşağı (kaçınma, AYNA; fark = eşli - olay): n >= 30; ortalama eşli fark < 0 VE ay kümeli %95 ÜST uç < 0; "
                "ortalama hücre içi sıra < 0,50; slot portföyü < 200 plasebo portföyün %10 yüzdeliği (p10); iki yarının ortalama eşli farkı "
                "da < 0. Durum: n < 30 ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 ya da güç(n, δ 5) >= %80) -> TUTMADI; aksi ÖLÇÜLEMEDİ "
                "(OC.oc_hucre_durum, tutar yerine ayna şart)",
        "etiket": "S+ ve S- AYRI: OC.oc_etiket (karar hücreleri ABD 2023 / 2024-26, AVR 2023 / 2024-26; BIST bilgi) ile; cetvelin 'İZ DEĞİL' "
                  "etiketi bu işte 'DESTEKLENMEDİ' olarak yazılır (güç yeterli, tutmadı). EMARE = en az bir karar hücresi TUTAR ama dördü değil.",
        "ters": "bilgi: her ana satır için TERS yön de aynı kuralla yazılır (S+ için ayna, S- için cetvel); karar değildir",
        "olasilik_eksi": "bilgi: S- için -%50 eş katının alt ucu > 1 VE +%100 eş katının üst ucu < 1 -> 'AŞAĞI SEÇİCİ' (karar dışı); "
                         "cetvelin olasılık etiketi (SEÇİCİ / PİYANGO / YOK) iki satırda da aynen yazılır"},
    "coklu": {"ana": "ana karar yalnız SP_k10 ve SM_k10 (çoklu düzeltme yok; iki ayrı ön kayıtlı soru)",
              "bilgi": "8 bilgi satırı x 4 karar hücresi = 32 test; p = beklenen yönde ay kümeli bootstrap (2000, tohum 27, oc_hucre ile aynı "
                       "örnekleme): S+ için (1 + #ortalama <= 0) / 2001, S- için (1 + #ortalama >= 0) / 2001; Benjamini-Hochberg q 0,10; "
                       "n < 30 hücre teste girmez"},
    "gelecek_denetimi": {"n": 40, "n_onda": 4, "tohum": 1611,
                         "tanim": "kos: her pazarda rastgele olaylarda hisse serisi t'de kesilip pencere ölçüleri yeniden hesaplanır; sinyal aynı "
                                  "olmalı (onda satırı: bütün pazar t'de kesilir); tutmazsa koşu DURUR"},
    "ornek": {
        "PAPIL": {"pazar": "BIST", "bas": "2025-11-13", "son": "2025-12-09", "beklenen": "SP_k10"},
        "DGXX": {"pazar": "ABD", "bas": "2026-10-27", "son": "2026-11-13", "beklenen": "SM_k10",
                 "kaynak": "V_ABD 2026-10-22'de bitiyor ve oc_veri 31.08.2026'da keser: yalnız örnek için yfinance (auto_adjust=False, "
                           "2026-06-01 .. 2026-11-13; 16 Kas yarım bar alınmaz); ölçüme girmez"},
        "FENER": {"pazar": "BIST", "bas": "2025-10-14", "son": "2025-11-07", "beklenen": "bilgi"},
        "DESA": {"pazar": "BIST", "bas": "2021-10-27", "son": "2021-12-23", "beklenen": "bilgi"},
        "YKSLN": {"pazar": "BIST", "bas": "2026-03-19", "son": "2026-05-15", "beklenen": "bilgi"}},
    "veri": "OC.oc_veri (cetvel): V_BIST / V_ABD / V_AVR; ABD k34_yahoo varsa eklenir, yoksa yalnız V_ABD (raporda yazılır)",
}

FO_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc: aynı giriş günü, aynı pazar, 60 gün momentum beşliği x 20 gün likidite üçlüsü, "
                   "aynı giriş (ertesi açılış) / çıkış (60. gün) geometrisi; 200 plasebo portföy aynı gün aynı hücreden. Mekanik üstünlük: sinyal "
                   "yalnız t'ye kadar mum şekli; giriş t+1 açılışı olduğu için t kapanış konumu getiriyi mekanik üretmez; kısa vadeli dönüş "
                   "(üst fitilli = kapanış dipte) eşlenmez, raporda sınır olarak yazılır"),
    "K2": ("EVET", "pencere ölçüleri rolling (geriye), ATR%250 t'de biter, onda sırası yalnız t günü; kos fo_gelecek_denetimi her pazarda "
                   "40 (+4 onda) rastgele olayda seriyi t'de kesip sinyali yeniden hesaplar, tutmazsa DURUR; test 'geleceğe bakma'"),
    "K3": ("EVET", "sinyal OC.oc_veri temiz barlarıyla (H>L, V>0, fiyat > 0; geçersiz bar veriden atılır, pencereye girmez); DGXX örneğinde "
                   "16 Kas (seans içi yarım bar) alınmaz"),
    "K4": ("EVET", "durum günleri cetvele verilir; OC.oc_olay_hazirla aynı hissede 60 gün tekilleştirir; n bağımsız olay; hücrede medyan da yazılır"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla); sinyal t kapanışında biter"),
    "K6": ("EVET", "tek kip fi_k1_veri düzeltilmiş fiyat (V_*.pkl); fitil payları oran, birimden bağımsız; bölünme şüphesi cetvelde (geçmiş "
                   "pencere); DGXX örneği ham (auto_adjust=False) ama yalnız fitil payı, birim etkisiz"),
    "K7": ("EVET", "evren bugün işlem görenler (V_*; k34_yahoo yoksa ABD yalnız V_ABD 1.411 hisse); batanlar yok; raporda 'getiriler yukarı, "
                   "-%50 olasılığı aşağı yanlı' notu"),
    "K8": ("EVET", "3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki yarı şartı; DESTEKLENMEDİ yalnız güç yeterliyken; bilgi satırları BH q 0,10; "
                   "olay sayımı bu ön kayıtta getiri hesaplanmadan"),
    "K9": ("EVET", "FO_ESIK sha + FITIL_OBEK.py sha + cetvel üç sha + veri sha bu dosyada; iş tanımı koşudan önce git'e işlendi (99bdc76); "
                   "kos ik_kontrol_kapisi + OC.oc_kapi + fo_onkayit_dogrula geçmezse durur; eşik sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "metin / KAP ayrıştırma yok; yalnız OHLCV; örnek bölgelerde fitil payları ham bardan elle yeniden hesaplanır (rapor)"),
    "K11": ("EVET", "ana olay satırları arastirma_cikti/fitil_obek/olay_ana.csv.gz; >= 2 hücre bağımsız kodla yeniden üretilir (rapor DENETİM)"),
    "K12": ("EVET", "etiketler yalnız oc_etiket / ayna kuralı; 'iz / emare' sözü yalnız kural geçerse; fiyat değişimi ile işlem kârı ayrı "
                    "(komisyon yok); sayı ve yorum ayrı cümle; 'al' / 'öneri' dili yok"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_fo; defter dosyaları ve mevcut .py modülleri yalnız okunur (git status); e-posta / anahtar "
                    "taraması testte ve raporda; ücretli veri yok; commit / push ana modelin"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; yön ölçümü (kapalı konu 'tek göstergeye göre alım' açılmaz)"),
}


class FOHata(RuntimeError):
    """Durdurucu hata: ön kayıt yok / sha tutmuyor / git kapısı / geleceğe bakma denetimi tutmadı / veri yok."""


# ================================================================ 0) ORTAK
_FO_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_FO_ANAHTAR = re.compile(r"(api[_-]?key|token|secret|password|şifre)\s*[=:]\s*['\"][^'\"]{8,}", re.I)


def _fo_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _fo_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fo_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    s = json.dumps(FO_ESIK if E is None else E, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _fo_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or FO_YOL["cikti"], FO_DOSYA[ad])


def _fo_sizinti(metin: str, ad: str) -> None:
    if _FO_EPOSTA.search(metin) or _FO_ANAHTAR.search(metin):
        raise FOHata(f"{ad}: e-posta / anahtar biçimli parça var")


# ================================================================ 1) MUM ve PENCERE ÖLÇÜLERİ (yalnız t'ye kadar)
def fo_bar(df: pd.DataFrame) -> pd.DataFrame:
    """Geçerli barlar (temiz veri beklenir) -> R, alt, üst, gövde, R/C, TR/C. Geçersiz bar varsa atılır (K3)."""
    d = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)
    ok = np.isfinite(d).all(axis=1) & (d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0) & (d.Low > 0)
    d = d[ok]
    O, H, L, C = (d[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    R = H - L
    alt = (np.minimum(O, C) - L) / R
    ust = (H - np.maximum(O, C)) / R
    gov = np.abs(C - O) / R
    Cp = np.r_[np.nan, C[:-1]]
    TR = np.where(np.isfinite(Cp), np.maximum(H, Cp) - np.minimum(L, Cp), R)
    return pd.DataFrame({"R": R, "alt": np.clip(alt, 0, 1), "ust": np.clip(ust, 0, 1), "govde": gov, "RC": R / C, "TRC": TR / C,
                         "Close": C}, index=d.index)


def fo_pencere(B: pd.DataFrame, k: int, E: Dict[str, Any] = FO_ESIK) -> pd.DataFrame:
    """fo_bar çıktısı -> k barlık pencere ölçüleri (t dahil): A, U, ASIM, ALTYOK, USTYOK, medRC, ATR250, KUCUK."""
    fy = E["fitil_yok"]; K = E["kucuk"]
    A = B.alt.rolling(k, min_periods=k).mean(); U = B.ust.rolling(k, min_periods=k).mean()
    altyok = (B.alt < fy).astype(float).rolling(k, min_periods=k).mean()
    ustyok = (B.ust < fy).astype(float).rolling(k, min_periods=k).mean()
    med = B.RC.rolling(k, min_periods=k).median()
    atr = B.TRC.rolling(K["atr_gun"], min_periods=K["atr_min"]).mean()
    P = pd.DataFrame({"A": A, "U": U, "ASIM": U - A, "ALTYOK": altyok, "USTYOK": ustyok, "medRC": med, "ATR250": atr}, index=B.index)
    P["KUCUK"] = (P.medRC <= K["carpan"] * P.ATR250) & P.ATR250.notna() & P.medRC.notna()
    return P


def fo_kural(P: pd.DataFrame, yon: str, E: Dict[str, Any] = FO_ESIK) -> pd.Series:
    """S+ / S- şartı (pencere ölçülerinden)."""
    if yon == "SP":
        return (P.ASIM >= E["s_arti"]["asim_min"]) & (P.ALTYOK >= E["s_arti"]["altyok_min"])
    if yon == "SM":
        return (P.ASIM <= E["s_eksi"]["asim_max"]) & (P.USTYOK >= E["s_eksi"]["ustyok_min"])
    raise FOHata(f"yön {yon}?")


def fo_hisse_sinyal(df: pd.DataFrame, E: Dict[str, Any] = FO_ESIK) -> Tuple[Dict[str, pd.Series], pd.Series]:
    """Bir hisse -> ({satır: bool seri} onda hariç, k=10 ASIM serisi)."""
    B = fo_bar(df)
    out: Dict[str, pd.Series] = {}
    if not len(B):   # kısa seri: rolling min_periods pencere dolmadan NaN verir (k=5 satırı 5. bardan itibaren tanımlı)
        bos = pd.Series(False, index=B.index)
        return {s: bos for s in E["satirlar"] if not s.endswith("_onda")}, pd.Series(np.nan, index=B.index)
    P10 = fo_pencere(B, E["k_ana"], E)
    for yon in ("SP", "SM"):
        k10 = fo_kural(P10, yon, E)
        out[f"{yon}_k10"] = k10
        out[f"{yon}_kucuk"] = k10 & P10.KUCUK
        for k in E["k_bilgi"]:
            out[f"{yon}_k{k}"] = fo_kural(fo_pencere(B, k, E), yon, E)
    return out, P10.ASIM


def fo_onda(asim: pd.DataFrame, E: Dict[str, Any] = FO_ESIK) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """asim: tarih x sembol (k=10 ASIM, NaN = o gün tanımsız / bar yok). Günlük kesit yüzdelik sırası -> (S+ onda, S- onda)."""
    O = E["onda"]
    say = asim.notna().sum(axis=1)
    rk = asim.rank(axis=1, pct=True, method="average")
    yeter = (say >= O["min_hisse"]).to_numpy()[:, None]
    return (rk > O["ust"]) & yeter, (rk <= O["alt"]) & yeter


def fo_sinyaller(Vd: Dict[str, Any], pazar: str, E: Dict[str, Any] = FO_ESIK) -> pd.DataFrame:
    """oc_veri çıktısı -> durum günleri: DataFrame[sembol, tarih, pazar, satir]. ABD k34 evren_bas öncesi günler atılır (cetvel de atar)."""
    V = Vd["V"]; evb = Vd.get("evren_bas", {}); sat, AS = [], {}
    for s in sorted(V):
        sig, asim = fo_hisse_sinyal(V[s], E)
        AS[s] = asim
        for ad, ser in sig.items():
            g = ser.index[ser.fillna(False).to_numpy(bool)]
            if s in evb:
                g = g[g >= pd.Timestamp(evb[s])]
            if len(g):
                sat.append(pd.DataFrame({"sembol": s, "tarih": g, "pazar": pazar, "satir": ad}))
    if AS:
        A = pd.DataFrame(AS)
        for s in list(A.columns):
            if s in evb:
                A.loc[A.index < pd.Timestamp(evb[s]), s] = np.nan
        up, dn = fo_onda(A, E)
        for ad, M in (("SP_onda", up), ("SM_onda", dn)):
            st = M.stack()
            st = st[st.to_numpy(bool)]
            if len(st):
                sat.append(pd.DataFrame({"sembol": st.index.get_level_values(1).astype(str), "tarih": st.index.get_level_values(0),
                                         "pazar": pazar, "satir": ad}))
    if not sat:
        return pd.DataFrame(columns=["sembol", "tarih", "pazar", "satir"])
    X = pd.concat(sat, ignore_index=True)
    X["tarih"] = pd.to_datetime(X.tarih)
    return X.sort_values(["satir", "sembol", "tarih"]).reset_index(drop=True)


# ================================================================ 2) GELECEĞE BAKMA DENETİMİ (koşu içinde, mekanik)
def fo_gelecek_denetimi(Vd: Dict[str, Any], X: pd.DataFrame, pazar: str, E: Dict[str, Any] = FO_ESIK) -> Dict[str, int]:
    """Rastgele olaylarda seri t'de kesilir; sinyal yeniden hesaplanır ve doğru olmalı. Tutmazsa FOHata."""
    G = E["gelecek_denetimi"]; rng = np.random.default_rng(G["tohum"]); V = Vd["V"]; out = {"hisse": 0, "onda": 0}
    Xh = X[~X.satir.str.endswith("_onda")]
    if len(Xh):
        for r in Xh.iloc[rng.choice(len(Xh), min(G["n"], len(Xh)), replace=False)].itertuples():
            t = pd.Timestamp(r.tarih)
            sig, _ = fo_hisse_sinyal(V[r.sembol][V[r.sembol].index <= t], E)
            v = sig[r.satir]
            if not len(v) or v.index[-1] != t or not bool(v.iloc[-1]):
                raise FOHata(f"geleceğe bakma denetimi tutmadı: {pazar} {r.sembol} {t.date()} {r.satir}")
            out["hisse"] += 1
    Xo = X[X.satir.str.endswith("_onda")]
    if len(Xo):
        evb = Vd.get("evren_bas", {})
        for r in Xo.iloc[rng.choice(len(Xo), min(G["n_onda"], len(Xo)), replace=False)].itertuples():
            t = pd.Timestamp(r.tarih); A = {}
            for s, d in V.items():
                if s in evb and t < pd.Timestamp(evb[s]):
                    continue
                kes = d[d.index <= t]
                if len(kes) < E["k_ana"]:
                    continue
                _, a = fo_hisse_sinyal(kes, E)
                if len(a) and a.index[-1] == t:
                    A[s] = a.iloc[-1:]
            up, dn = fo_onda(pd.DataFrame(A), E)
            M = up if r.satir == "SP_onda" else dn
            if r.sembol not in M.columns or t not in M.index or not bool(M.loc[t, r.sembol]):
                raise FOHata(f"geleceğe bakma denetimi (onda) tutmadı: {pazar} {r.sembol} {t.date()} {r.satir}")
            out["onda"] += 1
    return out


# ================================================================ 3) ÖLÇÜM (cetvel) ve KARAR
def fo_kacinma(h: Dict[str, Any], E: Dict[str, Any] = FO_ESIK) -> bool:
    """S- ayna şartı (oc_hucre çıktısından): n >= 30, ort < 0 ve üst uç < 0, sıra < 0,50, portföy < p10, iki yarı < 0."""
    K = OC.OC_ESIK["hucre_karar"]
    try:
        n = int(h.get("n", 0) or 0)
        if n < K["n_esik"]:
            return False
        y1, y2 = float(h.get("yari1_fark", np.nan)), float(h.get("yari2_fark", np.nan))
        return bool(float(h["ort_fark"]) < 0 and float(h["ust95"]) < 0 and float(h["sira"]) < K["sira_esik"]
                    and float(h["portfoy"]) < float(h["portfoy_esli_p10"]) and np.isfinite(y1) and y1 < 0 and y2 < 0)
    except (KeyError, TypeError, ValueError):
        return False


def fo_durum(h: Dict[str, Any], yon: str) -> Tuple[str, float]:
    """Beklenen yönde hücre durumu: '+' cetvel tutar, '-' ayna (kaçınma)."""
    if yon == "+":
        return OC.oc_hucre_durum(h)
    return OC.oc_hucre_durum({"n": h.get("n", 0), "tutar": fo_kacinma(h)})


def fo_etiket(T: pd.DataFrame, yon: str) -> Dict[str, Any]:
    """T: oc_olc hücre tablosu. Beklenen yön durumları ile OC.oc_etiket; 'İZ DEĞİL' -> 'DESTEKLENMEDİ'."""
    Y = T.copy()
    Y["durum"] = [fo_durum(r, yon)[0] for r in T.to_dict("records")]
    e = OC.oc_etiket(Y)
    e["genel_cetvel"] = e["genel"]
    e["genel"] = e["genel"].replace("İZ DEĞİL", "DESTEKLENMEDİ")
    e["durumlar"] = {f"{r.pazar} {r.donem}": r.durum for r in Y.itertuples()}
    return e


def fo_p(fark: np.ndarray, giris: pd.Series, yon: str, E: Dict[str, Any] = FO_ESIK) -> float:
    """Beklenen yönde tek yanlı ay kümeli bootstrap p (oc_hucre ile aynı örnekleme: tohum 27, 2000)."""
    O = OC.OC_ESIK["olcu"]
    g = np.isfinite(fark)
    f = fark[g]
    if len(f) < OC.OC_ESIK["hucre_karar"]["n_esik"]:
        return np.nan
    gi = pd.to_datetime(pd.Series(giris).reset_index(drop=True)[g])
    srt = np.argsort(gi.to_numpy(), kind="mergesort"); f = f[srt]; gi = gi.iloc[srt]
    ay = gi.dt.to_period("M").astype(str).to_numpy(); aylar = np.unique(ay)
    grup = {a: f[ay == a] for a in aylar}; rng = np.random.default_rng(O["tohum"]); m = []
    for _ in range(O["bootstrap"]):
        sec = rng.choice(aylar, len(aylar), replace=True)
        m.append(np.concatenate([grup[a] for a in sec]).mean())
    m = np.array(m)
    say = (m <= 0).sum() if yon == "+" else (m >= 0).sum()
    return float((1 + say) / (len(m) + 1))


def fo_bh(p: List[float], q: float = 0.10) -> List[bool]:
    """Benjamini-Hochberg: NaN olmayanlar üzerinde; NaN -> False."""
    p = np.asarray(p, float); ok = np.isfinite(p); m = int(ok.sum()); out = np.zeros(len(p), bool)
    if not m:
        return out.tolist()
    ix = np.where(ok)[0]; srt = ix[np.argsort(p[ix], kind="mergesort")]
    esik = q * np.arange(1, m + 1) / m
    gec = np.where(p[srt] <= esik)[0]
    if len(gec):
        out[srt[:gec.max() + 1]] = True
    return out.tolist()


def _fo_json_S(S: Dict[str, Any]) -> Dict[str, Any]:
    return {"hucre": json.loads(S["hucre"].to_json(orient="records", force_ascii=False)) if len(S["hucre"]) else [],
            "olasilik": json.loads(S["olasilik"].to_json(orient="records", force_ascii=False)) if len(S["olasilik"]) else [],
            "sayim": json.loads(json.dumps(S["sayim"], default=int)), "cetvel_sha": S["cetvel_sha"], "kod_sha": S["kod_sha"]}


def fo_olc_satir(X: pd.DataFrame, PN: Dict[str, Any]) -> Dict[str, Any]:
    """Bir satırın olaylarını pazar pazar OC.oc_olc ile ölçer; hücre / olasılık / olay / sayım birleşik."""
    parca = []
    for p in [q for q in OC.OC_ESIK["pazar"] if q in set(X.pazar) and q in PN]:
        x = X[X.pazar == p][["sembol", "tarih", "pazar"]].reset_index(drop=True)
        parca.append(OC.oc_olc(x, {p: PN[p]}))
    if not parca:
        return {"hucre": pd.DataFrame(), "olasilik": pd.DataFrame(), "olay": pd.DataFrame(), "sayim": {}, "cetvel_sha": OC.oc_esik_sha(), "kod_sha": ""}
    return {"hucre": pd.concat([q["hucre"] for q in parca], ignore_index=True),
            "olasilik": pd.concat([q["olasilik"] for q in parca], ignore_index=True),
            "olay": pd.concat([q["olay"] for q in parca], ignore_index=True),
            "sayim": {k: v for q in parca for k, v in q["sayim"].items()}, "cetvel_sha": parca[0]["cetvel_sha"], "kod_sha": parca[0]["kod_sha"]}


def fo_satir_sonuc(S: Dict[str, Any], satir: str) -> Dict[str, Any]:
    """Satır sonucu: hücreler (beklenen + ters yön durumu), etiket (beklenen / ters), olasılık, S- 'AŞAĞI SEÇİCİ' bilgisi, p (karar hücreleri)."""
    yon = FO_ESIK["yon"][satir[:2]]; ters = "-" if yon == "+" else "+"
    J = _fo_json_S(S); T = S["hucre"]
    J["yon"] = yon
    if not len(T):
        J["etiket"] = {"genel": "VERİ YOK"}; J["etiket_ters"] = {"genel": "VERİ YOK"}; J["p"] = {}
        return J
    J["etiket"] = fo_etiket(T, yon); J["etiket_ters"] = fo_etiket(T, ters)
    for h in J["hucre"]:
        h["durum_yon"], h["guc_yon"] = fo_durum(h, yon); h["durum_ters"], _ = fo_durum(h, ters)
    for r in J["olasilik"]:
        a, u = r.get("dn50_es_alt"), r.get("up100_es_ust")
        r["asagi_secici"] = bool(r.get("n250", 0) >= 30 and a is not None and u is not None and np.isfinite(a) and np.isfinite(u)
                                 and a > 1 and u < 1)
    Ol = S["olay"]; J["p"] = {}
    for p in OC.OC_ESIK["karar_pazar"]:
        for d in OC.OC_ESIK["karar_donem"]:
            x = Ol[(Ol.pazar == p) & (Ol.donem == d)] if len(Ol) else Ol
            J["p"][f"{p} {d}"] = fo_p(x.fark.to_numpy(float), x.giris, yon) if len(x) else np.nan
    return J


# ================================================================ 4) VERİ, SAYIM, ÖN KAYIT
def fo_veri(pazar: str, veri: Optional[str] = None, veri2: Optional[str] = None) -> Dict[str, Any]:
    return OC.oc_veri(pazar, klasor=veri or FO_YOL["veri"], veri2=veri2 or FO_YOL["veri2"])


def fo_sayim(X: pd.DataFrame, P: Dict[str, Any]) -> Dict[str, Any]:
    """GETİRİSİZ olay sayımı: durum günü ve cetvel sonrası (tekil, havuzda) olay, girişe göre dönem; satır başına."""
    out = {}
    for sat in FO_ESIK["satirlar"]:
        x = X[X.satir == sat][["sembol", "tarih", "pazar"]]
        Y, say = OC.oc_olay_hazirla(x, P)
        dg = pd.Series(OC._oc_donem(x.tarih, OC.OC_ESIK)).value_counts().to_dict() if len(x) else {}
        ol = Y.donem.value_counts().to_dict() if len(Y) else {}
        out[sat] = {"durum_gunu": {k: int(v) for k, v in dg.items() if k}, "olay": {k: int(v) for k, v in ol.items() if k},
                    "dusme": {k: int(v) for k, v in say.items()}}
    return out


def fo_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = FO_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def _fo_is_tanimi_git() -> Dict[str, str]:
    try:
        return OC._oc_git_islenmis(FO_YOL["is_tanimi"])
    except OC.OCHata as ex:
        raise FOHata(f"iş tanımı git kapısı: {ex}")


def _fo_say_tablo(say: Dict[str, Dict[str, Any]]) -> List[str]:
    s = ["| Satır | Pazar | durum günü 2016-22 / 2023 / 2024-26 | OLAY (cetvel sonrası, giriş dönemi) 2016-22 / 2023 / 2024-26 | tekil düşen | havuz dışı |",
         "|---|---|---|---|---|---|"]
    for sat in FO_ESIK["satirlar"]:
        for p, c in say.items():
            if sat not in c:
                continue
            v = c[sat]; dg = v["durum_gunu"]; ol = v["olay"]
            s.append(f"| {sat} | {p} | {dg.get('2016-22', 0)} / {dg.get('2023', 0)} / {dg.get('2024-26', 0)} | {ol.get('2016-22', 0)} / "
                     f"{ol.get('2023', 0)} / {ol.get('2024-26', 0)} | {v['dusme'].get('tekil', 0)} | {v['dusme'].get('havuz_disi', 0)} |")
    return s


def fo_onkayit_metni(say: Dict[str, Any], vsha: Dict[str, str], notlar: Dict[str, List[str]], git_it: Dict[str, str]) -> str:
    E = FO_ESIK
    s = ["# FITIL_OBEK — ÖN KAYIT", "", FO_SURUM, "",
         f"- FO_ESIK_SHA: `{fo_esik_sha()}`", f"- FO_KOD_SHA: `{_fo_sha_dosya(FO_YOL['kod'])}`",
         f"- IS_TANIMI_SHA: `{_fo_sha_dosya(FO_YOL['is_tanimi'])}` (git {git_it.get('commit', '-')[:10]}, {git_it.get('commit_zamani', '-')})",
         f"- ZAMAN (UTC): `{_fo_simdi()}`", "",
         "Bu dosya ölçümden ÖNCE yazıldı; hiçbir getiri / eş farkı / olasılık hesaplanmadı (yalnız olay sayımı, getirisiz). `kos` kontrol listesi, "
         "cetvel üç sha'sı, FO_ESIK / kod sha'sı ve iş tanımının git kaydı tutmazsa durur. Eşikler sonuç görülünce değişmez.", "",
         "## Cetvel mühür satırları (ORTAK_CETVEL; aynen)", "", OC.oc_kapi_satirlari(), "",
         "## Tanım (iş tanımı §2; sabit)", "",
         f"- Bar: {E['bar']}. Fitil yok eşiği {E['fitil_yok']}.", f"- Pencere: {E['pencere']}.",
         f"- S+ (YUKARI öbek) k={E['k_ana']}: ASIM >= {E['s_arti']['asim_min']} VE ALTYOK >= {E['s_arti']['altyok_min']}.",
         f"- S- (AŞAĞI öbek) k={E['k_ana']}: ASIM <= {E['s_eksi']['asim_max']} VE USTYOK >= {E['s_eksi']['ustyok_min']}.",
         f"- KUCUK: {E['kucuk']['tanim']}.", f"- Onda birlik: {E['onda']['tanim']}.", f"- Olay: {E['olay']}.", "",
         "Satırlar:", ""] + [f"- {k}: {v}" for k, v in E["satirlar"].items()] + ["",
         "## Karar kuralı (önceden yazılı)", "", f"- S+: {E['karar']['arti']}.", f"- S-: {E['karar']['eksi']}.", f"- Etiket: {E['karar']['etiket']}",
         f"- Ters yön: {E['karar']['ters']}.", f"- Olasılık: {E['karar']['olasilik_eksi']}.",
         f"- Çoklu karşılaştırma: {E['coklu']['ana']}; {E['coklu']['bilgi']}.", "",
         "## Örnek doğrulama (tanım değiştirilmez; tutmazsa hangi şart olduğu raporda)", ""] + \
        [f"- {k}: {v['pazar']} {v['bas']} .. {v['son']}, beklenen {v['beklenen']}" + (f" ({v['kaynak']})" if "kaynak" in v else "")
         for k, v in E["ornek"].items()] + ["",
         "## Veri", ""] + [f"- V_{p}.pkl sha256: `{v}`" for p, v in vsha.items()] + \
        [f"- {p} oc_veri notu: {'; '.join(n)}" for p, n in notlar.items()] + ["",
         "## OLAY SAYIMI (getirisiz; durum günü sinyal tarihine, olay giriş tarihine göre dönem)", ""] + _fo_say_tablo(say) + ["",
         "Kural: hücre n < 30 ise ÖLÇÜLEMEDİ; güç yetersizse DESTEKLENMEDİ denmez.", "",
         "## SAPMA / sınır (sonuç görülmeden yazıldı)", "",
         "- k34_yahoo (veri2) yoksa ABD evreni yalnız V_ABD'dir (oc_veri notunda); güç tablosu ABD + k34 ile üretilmişti (cetvel), aynen kullanılır.",
         "- ON_KAYIT.md'yi alt ajan git'e işleyemez (commit yasak): iş tanımı koşudan önce işlendi (yukarıdaki commit); bu dosyanın sha'sı ve yazım "
         "zamanı sonuc.json'a yazılır, kos zamanı ondan sonradır. oc_kapi git=False ile, ORTAK_CETVEL.py / güç tablosu / iş tanımı git kaydı ayrıca "
         "denetlenir. Ana model ON_KAYIT.md'yi işlerken sha'yı karşılaştırır.",
         "- Kısa vadeli dönüş / oynaklık eşlenmez (cetvel yalnız 60 gün momentum x likidite eşler): S+ (kapanış dipte) / S- (kapanış tepede) ile "
         "son günlerin getirisi ilişkili olabilir; yorumda sınır.", "",
         fo_kontrol_tablosu(), "",
         "## Test", "", "`python test_fitil_obek.py` (sentetik: fitil payları elle, pencere / kural, onda kesiti, geleceğe bakma kesme testi, ayna "
         "kuralı, BH, cetvel çağrısı, kapı, e-posta / anahtar taraması).", ""]
    return "\n".join(s)


def fo_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False) -> str:
    yol = _fo_yol("onkayit", cikti)
    if os.path.exists(yol):
        try:
            OC._oc_git_islenmis(yol)
            raise FOHata(f"ön kayıt git'e işlenmiş ({yol}); üzerine yazılmaz")
        except OC.OCHata:
            if not uzerine:
                raise FOHata(f"ön kayıt var ({yol}); git'e işlenmemişse --uzerine-yaz")
    if os.path.exists(_fo_yol("sonuc", cikti)):
        raise FOHata("sonuc.json var: ölçüm koşulmuş, ön kayıt yeniden yazılamaz (SAPMA)")
    git_it = _fo_is_tanimi_git()
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    say, vsha, notlar = {}, {}, {}
    for p in OC.OC_ESIK["pazar"]:
        vsha[p] = _fo_sha_dosya(os.path.join(veri or FO_YOL["veri"], f"V_{p}.pkl"))
        Vd = fo_veri(p, veri); notlar[p] = list(Vd.get("not", []))
        X = fo_sinyaller(Vd, p); P = OC.oc_panel(Vd)
        say[p] = fo_sayim(X, P)
        folog.info("%s: durum günü %d", p, len(X))
        del Vd, P, X
    metin = fo_onkayit_metni(say, vsha, notlar, git_it)
    _fo_sizinti(metin, "ön kayıt")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    folog.info("ön kayıt yazıldı: %s", yol)
    return yol


_FO_DESEN = {"esik": r"FO_ESIK_SHA:\s*`([0-9a-f]{64})`", "kod": r"FO_KOD_SHA:\s*`([0-9a-f]{64})`", "is_tanimi": r"IS_TANIMI_SHA:\s*`([0-9a-f]{64})`"}


def fo_onkayit_dogrula(yol: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    yol = yol or _fo_yol("onkayit")
    if not os.path.exists(yol):
        raise FOHata(f"ön kayıt yok ({yol}): önce `python FITIL_OBEK.py onkayit`")
    metin = open(yol, encoding="utf-8").read(); b = {}
    for ad, desen in _FO_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise FOHata(f"ön kayıt bozuk: '{ad}' satırı yok")
        b[ad] = m.group(1)
    simdi = {"esik": fo_esik_sha(), "kod": _fo_sha_dosya(FO_YOL["kod"]), "is_tanimi": _fo_sha_dosya(FO_YOL["is_tanimi"])}
    for ad in simdi:
        if b[ad] != simdi[ad]:
            raise FOHata(f"{ad} sha tutmuyor (ön kayıt {b[ad][:12]}…, şimdi {simdi[ad][:12]}…): koşu DURDU (SAPMA)")
    out: Dict[str, Any] = {"yol": yol, **b, "onkayit_sha": _fo_sha_dosya(yol),
                           "onkayit_yazim_utc": re.search(r"ZAMAN \(UTC\):\s*`([^`]+)`", metin).group(1)}
    out["git_is_tanimi"] = _fo_is_tanimi_git()
    try:
        out["git_cetvel_kod"] = OC._oc_git_islenmis(OC.OC_YOL["kod"])
        out["git_guc"] = OC._oc_git_islenmis(os.path.join(OC.OC_YOL["cikti"], OC.OC_DOSYA["guc_json"]))
    except OC.OCHata as ex:
        raise FOHata(str(ex))
    try:
        out["git_onkayit"] = OC._oc_git_islenmis(yol)
    except OC.OCHata as ex:
        if git:
            raise FOHata(f"{ex} (alt ajan commit yapamaz: --gitsiz ile koş, SAPMA olarak yazılır)")
        out["git_onkayit"] = f"İŞLENMEDİ (gitsiz koşu; ön kayıt sha {out['onkayit_sha'][:12]}…, yazım {out['onkayit_yazim_utc']})"
    return out


# ================================================================ 5) ÖRNEK DOĞRULAMA (getirisiz)
def _fo_dgxx_indir(E: Dict[str, Any] = FO_ESIK) -> Optional[pd.DataFrame]:
    try:
        import yfinance as yf
        d = yf.download("DGXX", start="2026-06-01", end="2026-11-14", progress=False, auto_adjust=False)
    except Exception as ex:   # ağ / paket yoksa örnek 'veri yok' yazılır
        folog.warning("DGXX indirilemedi: %s", ex); return None
    if d is None or not len(d):
        return None
    if isinstance(d.columns, pd.MultiIndex):
        d.columns = d.columns.get_level_values(0)
    d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float)
    d.index = pd.DatetimeIndex(d.index).tz_localize(None).normalize()
    return d[d.index <= pd.Timestamp(E["ornek"]["DGXX"]["son"])]


def fo_ornek(veri: Optional[str] = None, VV: Optional[Dict[str, Any]] = None, E: Dict[str, Any] = FO_ESIK) -> Dict[str, Any]:
    """Örnek bölgelerde her gün (pencere sonu) ASIM / ALTYOK / USTYOK / S+ / S- (k=10). DGXX yfinance (yalnız örnek)."""
    out: Dict[str, Any] = {}
    ham = {}
    for p in sorted({v["pazar"] for k, v in E["ornek"].items() if k != "DGXX"}):
        ham[p] = (VV or {}).get(p) or fo_veri(p, veri)
    for s, o in E["ornek"].items():
        if s == "DGXX":
            df = _fo_dgxx_indir(E); kaynak = "yfinance (yalnız örnek)"
        else:
            df = ham[o["pazar"]]["V"].get(s); kaynak = f"oc_veri {o['pazar']}"
        if df is None or not len(df):
            out[s] = {"kaynak": kaynak, "not": "veri yok"}; continue
        B = fo_bar(df); P = fo_pencere(B, E["k_ana"], E)
        P["SP"] = fo_kural(P, "SP", E); P["SM"] = fo_kural(P, "SM", E)
        P = P[(P.index >= pd.Timestamp(o["bas"])) & (P.index <= pd.Timestamp(o["son"]))]
        gun = [{"tarih": str(t.date()), "ASIM": round(float(r.ASIM), 3), "ALTYOK": round(float(r.ALTYOK), 2), "USTYOK": round(float(r.USTYOK), 2),
                "A": round(float(r.A), 3), "U": round(float(r.U), 3), "KUCUK": bool(r.KUCUK), "SP": bool(r.SP), "SM": bool(r.SM)}
               for t, r in P.iterrows()]
        sp = [g["tarih"] for g in gun if g["SP"]]; sm = [g["tarih"] for g in gun if g["SM"]]
        Bw = B[(B.index >= pd.Timestamp(o["bas"])) & (B.index <= pd.Timestamp(o["son"]))]
        out[s] = {"kaynak": kaynak, "pazar": o["pazar"], "bas": o["bas"], "son": o["son"], "beklenen": o["beklenen"], "gun": gun,
                  "SP_gunleri": sp, "SM_gunleri": sm, "bolge_bar": int(len(Bw)),
                  "bolge_alt_medyan": float(Bw.alt.median()) if len(Bw) else None, "bolge_ust_medyan": float(Bw.ust.median()) if len(Bw) else None,
                  "bolge_altyok": float((Bw.alt < E["fitil_yok"]).mean()) if len(Bw) else None,
                  "bolge_ustyok": float((Bw.ust < E["fitil_yok"]).mean()) if len(Bw) else None,
                  "asim_maks": float(P.ASIM.max()) if len(P) else None, "asim_min": float(P.ASIM.min()) if len(P) else None,
                  "altyok_maks": float(P.ALTYOK.max()) if len(P) else None, "ustyok_maks": float(P.USTYOK.max()) if len(P) else None}
    return out


# ================================================================ 6) KOŞU
def fo_kos(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    t_bas = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or FO_YOL["cikti"]; yol = _fo_yol("onkayit", cikti)
    if kontrol:
        import IZ_KARNE as IK
        try:
            IK.ik_kontrol_kapisi(yol)
        except RuntimeError as ex:
            raise FOHata(str(ex))
    kapi = OC.oc_kapi(yol, git=False, kontrol=kontrol)   # ön kaydı alt ajan işleyemez: git denetimleri fo_onkayit_dogrula'da
    ok = fo_onkayit_dogrula(yol, git=git)
    kos_zaman = _fo_simdi()
    if ok["onkayit_yazim_utc"] > kos_zaman:   # aynı saniye olabilir (onkayit && kos art arda)
        raise FOHata("ön kayıt zamanı koşu zamanından sonra")
    os.makedirs(FO_YOL["satir"], exist_ok=True)
    sonuc: Dict[str, Any] = {"surum": FO_SURUM, "onkayit": ok, "oc_kapi": {k: v for k, v in kapi.items() if k != "kontrol"}, "kos_zaman_utc": kos_zaman,
                             "fo_esik_sha": fo_esik_sha(), "gelecek_denetimi": {}, "veri_not": {}, "satir": {}, "ornek": {}}
    Xs, PN, VV = [], {}, {}
    for p in OC.OC_ESIK["pazar"]:
        Vd = fo_veri(p, veri); sonuc["veri_not"][p] = list(Vd.get("not", [])) + [f"hisse {len(Vd['V'])}"]
        X = fo_sinyaller(Vd, p)
        sonuc["gelecek_denetimi"][p] = fo_gelecek_denetimi(Vd, X, p)
        folog.info("%s: durum %d; geleceğe bakma denetimi TUTTU %s", p, len(X), sonuc["gelecek_denetimi"][p])
        PN[p] = OC.oc_panel(Vd); Xs.append(X)
        if p == "BIST":
            VV[p] = Vd
        del Vd
    X = pd.concat(Xs, ignore_index=True)
    sonuc["ornek"] = fo_ornek(veri, VV); del VV
    ana_olay = []
    for sat in FO_ESIK["satirlar"]:
        S = fo_olc_satir(X[X.satir == sat], PN)
        sonuc["satir"][sat] = fo_satir_sonuc(S, sat)
        if len(S["olay"]):
            Ol = S["olay"].copy(); Ol.insert(0, "satir", sat)
            (ana_olay if sat in FO_ESIK["ana"] else []).append(Ol)
            Ol.to_csv(os.path.join(FO_YOL["satir"], f"olay_{sat}.csv.gz"), index=False)
        folog.info("%s: %s (ters %s) %.0f sn", sat, sonuc["satir"][sat]["etiket"].get("genel"), sonuc["satir"][sat]["etiket_ters"].get("genel"),
                   time.time() - t_bas)
    # bilgi satırları BH (beklenen yön, karar hücreleri)
    anahtar, pler = [], []
    for sat in FO_ESIK["satirlar"]:
        if sat in FO_ESIK["ana"]:
            continue
        for h, pv in sonuc["satir"][sat].get("p", {}).items():
            anahtar.append((sat, h)); pler.append(pv)
    gec = fo_bh(pler, 0.10)
    sonuc["bh"] = [{"satir": a, "hucre": h, "p": p, "bh_q10": g} for (a, h), p, g in zip(anahtar, pler, gec)]
    if ana_olay:
        pd.concat(ana_olay, ignore_index=True).to_csv(_fo_yol("olay", cikti), index=False)
    sonuc["sure_sn"] = round(time.time() - t_bas, 1)
    metin = json.dumps(sonuc, ensure_ascii=False, indent=1, default=str)
    _fo_sizinti(metin, "sonuç")
    with open(_fo_yol("sonuc", cikti), "w", encoding="utf-8") as f:
        f.write(metin)
    return {"sonuc": sonuc, "rapor": fo_rapor(cikti)}


# ================================================================ 7) RAPOR
def _yz(x: Any, n: int = 1) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{100 * x:+.{n}f}%".replace(".", ",")


def _sy(x: Any, n: int = 2) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


def _fo_hucre_sat(sat: str, h: Dict[str, Any]) -> str:
    n = int(h.get("n") or 0)
    if not n:
        return f"| {sat} | {h['pazar']} | {h['donem']} | {'K' if h.get('karar_hucre') else 'b'} | 0 | - | - | - | - | - | - | - | {h.get('durum_yon')} | {h.get('durum_ters')} |"
    yon = FO_ESIK["yon"][sat[:2]]
    if yon == "+":
        dort = "".join("E" if h.get(k) else "h" for k in ("s_n", "s_fark", "s_sira", "s_port", "s_yari"))
    else:
        K = OC.OC_ESIK["hucre_karar"]
        sb = [n >= K["n_esik"], h["ort_fark"] < 0 and h["ust95"] < 0, h["sira"] < K["sira_esik"], h["portfoy"] < h["portfoy_esli_p10"],
              (h.get("yari1_fark") or 0) < 0 and (h.get("yari2_fark") or 0) < 0]
        dort = "".join("E" if b else "h" for b in sb)
    port = f"{_yz(h['portfoy'], 0)} / p90 {_yz(h['portfoy_esli_p90'], 0)} / p10 {_yz(h['portfoy_esli_p10'], 0)}"
    return (f"| {sat} | {h['pazar']} | {h['donem']} | {'K' if h.get('karar_hucre') else 'b'} | {n} | {_yz(h['ort_fark'])} [{_yz(h['alt95'])}, "
            f"{_yz(h['ust95'])}] | {_yz(h['medyan_fark'])} | {_sy(h['sira'])} | {port} | {_yz(h.get('yari1_fark'))} / {_yz(h.get('yari2_fark'))} | "
            f"{dort} | {_sy(100 * float(h.get('guc_yon') or 0), 0)}% | {h.get('durum_yon')} | {h.get('durum_ters')} |")


def fo_rapor(cikti: Optional[str] = None, ek: Optional[str] = None) -> str:
    J = json.load(open(_fo_yol("sonuc", cikti), encoding="utf-8"))
    E = FO_ESIK; SA = J["satir"]
    s = ["# FITIL_OBEK — RAPOR (Cemal'in fitil öbeği hipotezi, ORTAK CETVEL v1.0)", "",
         f"Ön kayıt yazım {J['onkayit'].get('onkayit_yazim_utc')} (sha {J['onkayit'].get('onkayit_sha', '')[:12]}…; git: "
         f"{J['onkayit'].get('git_onkayit') if isinstance(J['onkayit'].get('git_onkayit'), str) else J['onkayit'].get('git_onkayit', {}).get('commit', '-')[:10]}); "
         f"iş tanımı git {J['onkayit']['git_is_tanimi']['commit'][:10]} ({J['onkayit']['git_is_tanimi']['commit_zamani']}); koşu {J['kos_zaman_utc']}; "
         f"süre {J.get('sure_sn')} sn. Geleceğe bakma denetimi: " + ", ".join(f"{p} {v['hisse']} + {v['onda']} onda olay TUTTU"
                                                                            for p, v in J["gelecek_denetimi"].items()) + ".", "",
         "## ÖZET", ""]
    for sat in E["ana"]:
        e = SA[sat]["etiket"]; et = SA[sat]["etiket_ters"]
        s.append(f"- {E['satirlar'][sat]}: KARAR **{e['genel']}** (beklenen yön {SA[sat]['yon']}); ters yön (bilgi): {et['genel']}; "
                 f"olasılık etiketi {e.get('olasilik')}.")
        par = []
        for h in SA[sat]["hucre"]:
            if h.get("karar_hucre") or h["pazar"] == "BIST":
                if h["donem"] == "2016-22":
                    continue
                par.append(f"{h['pazar']} {h['donem']}: n {int(h.get('n') or 0)}, eş farkı {_yz(h.get('ort_fark'))} [{_yz(h.get('alt95'))}, "
                           f"{_yz(h.get('ust95'))}], sıra {_sy(h.get('sira'))} -> {h.get('durum_yon')}")
        s.append("  - " + "; ".join(par))
    s += ["- Okuma: 'eş farkı' = olay hissesinin 60 günlük getirisi eksi aynı gün, aynı 60 gün momentum ve likidite kovasındaki öteki hisselerin "
          "ortalaması. S+ için beklenen > 0, S- için < 0 (kaçınma, ayna şart). Hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, "
          "-%50 olasılığı aşağı yanlı. Komisyon yok.", "",
          "## TANIM", "", f"- Bar: {E['bar']}.", f"- Pencere: {E['pencere']}.",
          f"- S+ k=10: ASIM >= 0,20 VE ALTYOK >= 0,50. S- k=10: ASIM <= -0,20 VE USTYOK >= 0,50.", f"- KUCUK: {E['kucuk']['tanim']}.",
          f"- Onda: {E['onda']['tanim']}.", f"- Olay: {E['olay']}.", f"- S- ayna kuralı: {E['karar']['eksi']}.", "",
          "## OLAY SAYIMI (cetvel düşmeleri; ana satırlar)", "",
          "| Satır | Pazar | girdi (durum günü) | havuz dışı (lik alt %20 / geçmiş bölünme / geçmiş eksik / evren öncesi / havuz < 30) | tekil düşen | r60 ölçülemedi | eş < 3 |",
          "|---|---|---|---|---|---|---|"]
    for sat in E["ana"]:
        for p, c in SA[sat]["sayim"].items():
            s.append(f"| {sat} | {p} | {c.get('girdi')} | {c.get('havuz_disi')} ({c.get('likidite_alt20')} / {c.get('bolunme_gecmis')} / "
                     f"{c.get('gecmis_eksik')} / {c.get('evren_once')} / {c.get('havuz_az')}) | {c.get('tekil')} | {c.get('r60_olculemedi')} | {c.get('es_az')} |")
    s += ["", "## HÜCRE TABLOSU (r60 eşli fark; şartlar beklenen yönde: n / fark+aralık / sıra / portföy / iki yarı; E = tuttu, h = tutmadı)", "",
          "| Satır | Pazar | Dönem | karar | n | ort fark [%95] | medyan | sıra | portföy / plasebo | yarı1 / yarı2 | şart | güç (δ 5) | durum (beklenen) | durum (ters, bilgi) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for sat in E["ana"]:
        for h in SA[sat]["hucre"]:
            s.append(_fo_hucre_sat(sat, h))
    s += ["", "## OLASILIK TABLOSU (250 gün dokunma; eş katı karar, taban katı bilgi)", "",
          "| Satır | Pazar | Dönem | n250 | P(+%100) olay / eş | kat eş [%95] | kat taban | P(-%50) olay / eş | kat eş [%95] | kat taban | etiket | S- aşağı seçici |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for sat in E["ana"]:
        for r in SA[sat]["olasilik"]:
            s.append(f"| {sat} | {r['pazar']} | {r['donem']} | {r.get('n250', 0)} | {_yz(r.get('up100_es_p_olay'))} / {_yz(r.get('up100_es_p_ref'))} | "
                     f"{_sy(r.get('up100_es_kat'))} [{_sy(r.get('up100_es_alt'))}, {_sy(r.get('up100_es_ust'))}] | {_sy(r.get('up100_tb_kat'))} | "
                     f"{_yz(r.get('dn50_es_p_olay'))} / {_yz(r.get('dn50_es_p_ref'))} | {_sy(r.get('dn50_es_kat'))} [{_sy(r.get('dn50_es_alt'))}, "
                     f"{_sy(r.get('dn50_es_ust'))}] | {_sy(r.get('dn50_tb_kat'))} | {r.get('etiket')} | {'EVET' if r.get('asagi_secici') else '-'} |")
    s += ["", "## BİLGİ SATIRLARI (karar dışı; beklenen yönde p, BH q 0,10 karar hücrelerinde)", "",
          "| Satır | etiket (beklenen) | ters (bilgi) | ABD 2023 | ABD 2024-26 | AVR 2023 | AVR 2024-26 | BIST 2023 | BIST 2024-26 |", "|---|---|---|---|---|---|---|---|---|"]
    bh = {(r["satir"], r["hucre"]): r for r in J.get("bh", [])}
    for sat in E["satirlar"]:
        if sat in E["ana"]:
            continue
        J_ = SA[sat]; hc = {f"{h['pazar']} {h['donem']}": h for h in J_["hucre"]}; par = []
        for k in ("ABD 2023", "ABD 2024-26", "AVR 2023", "AVR 2024-26", "BIST 2023", "BIST 2024-26"):
            h = hc.get(k)
            if not h or not int(h.get("n") or 0):
                par.append("-"); continue
            b = bh.get((sat, k))
            bt = "" if b is None else f", p {_sy(b['p'], 3)}{' BH+' if b['bh_q10'] else ''}"
            par.append(f"n {int(h['n'])}, {_yz(h['ort_fark'])} [{_yz(h['alt95'])}, {_yz(h['ust95'])}], {h['durum_yon']}{bt}")
        s.append(f"| {sat} | {J_['etiket'].get('genel')} | {J_['etiket_ters'].get('genel')} | " + " | ".join(par) + " |")
    s += ["", f"BH q 0,10 geçen bilgi testi: {sum(1 for r in J.get('bh', []) if r['bh_q10'])} / {sum(1 for r in J.get('bh', []) if r['p'] == r['p'] and r['p'] is not None)}.", "",
          "## ÖRNEK DOĞRULAMA (k=10; tanım değiştirilmedi)", "",
          "| Hisse | bölge | kaynak | bar | alt medyan / üst medyan | alt yok / üst yok payı | ASIM min / maks | ALTYOK maks / USTYOK maks | S+ günleri | S- günleri |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for k, o in J["ornek"].items():
        if "gun" not in o:
            s.append(f"| {k} | - | {o.get('kaynak')} | - | - | - | - | - | {o.get('not')} | - |"); continue
        s.append(f"| {k} | {o['bas']} .. {o['son']} | {o['kaynak']} | {o['bolge_bar']} | {_sy(o['bolge_alt_medyan'])} / {_sy(o['bolge_ust_medyan'])} | "
                 f"{_sy(o['bolge_altyok'])} / {_sy(o['bolge_ustyok'])} | {_sy(o['asim_min'])} / {_sy(o['asim_maks'])} | {_sy(o['altyok_maks'])} / "
                 f"{_sy(o['ustyok_maks'])} | {', '.join(o['SP_gunleri']) or 'yok'} | {', '.join(o['SM_gunleri']) or 'yok'} |")
    s += ["", "## KARAR (önceden yazılı etiket kuralı)", ""]
    for sat in E["ana"]:
        e = SA[sat]["etiket"]
        s.append(f"- {sat}: **{e['genel']}** (cetvel genel: {e.get('genel_cetvel')}); karar hücreleri: " +
                 ", ".join(f"{k} {v}" for k, v in e.get("karar_hucre", {}).items()))
    s += ["", "## VERİ ve SINIRLAR", ""] + [f"- {p}: {'; '.join(n)}" for p, n in J["veri_not"].items()] + [
          "- Hayatta kalma: evren bugün işlem gören hisseler; batan / kottan çıkan yok. Getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı.",
          "- Komisyon / kayma yok; 31.08.2026 (fon krizi) sonrası fiyat yok; 250 gün dokunma en geç ~Ağustos 2025 girişlerini kapsar.",
          "- Kısa vadeli dönüş / oynaklık eşlenmez (cetvel yalnız 60 gün momentum x likidite eşler).", ""]
    on = _fo_yol("onkayit", cikti)
    if os.path.exists(on):
        m = open(on, encoding="utf-8").read()
        i = m.find("## KONTROL LİSTESİ")
        if i >= 0:
            s += [m[i:].split("\n## Test")[0].rstrip(), ""]
    if ek and os.path.exists(ek):
        s += [open(ek, encoding="utf-8").read().rstrip(), ""]
    metin = "\n".join(s)
    _fo_sizinti(metin, "rapor")
    with open(_fo_yol("rapor", cikti), "w", encoding="utf-8") as f:
        f.write(metin)
    return metin


# ================================================================ 8) ÇAKIŞMA KAPISI
def _cakisma_kontrol_fo(_once=_CK_ONCE_FO, _dosya="FITIL_OBEK.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_FO", "_CK_KAYIT", "_cakisma_kontrol_fo", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "warnings", "_dt", "OC",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple", "_yz", "_sy")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_fo()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=FO_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "ornek"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--ek", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true")
    ap.add_argument("--gitsiz", action="store_true", help="ön kayıt git'e işlenmemişse (alt ajan) SAPMA olarak yazıp koş")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(fo_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            R_ = fo_kos(a.cikti, a.veri, git=not a.gitsiz)
            print(R_["rapor"].split("## TANIM")[0])
        elif a.komut == "rapor":
            print(fo_rapor(a.cikti, a.ek))
        else:
            print(json.dumps(fo_ornek(a.veri), ensure_ascii=False, indent=1, default=str)[:20000])
    except (FOHata, OC.OCHata) as ex:
        folog.error("%s", ex); sys.exit(1)
