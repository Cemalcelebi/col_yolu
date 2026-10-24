# =====================================================================
#  MUM_SUKUN — dusus sonrasi 3-4 mumluk sukunet, her hissenin KENDI normaline gore   (2026-10-22, v1.3)
#
#  CEMAL (22 Eki, ANGX grafigi): "Son 3-4 mum: dizilim ve mum boyu kuculmesi cok derin bir isaret. Standart sayi cevirmeyeceksin;
#    her hissenin normal donem hareketliligi ile boyle donemlere orani tek tek hisseye ozel hesaplanmali."
#  OLCU (gercek zamanli, ileriye bakis yok):
#    b_t      = mum boyu / onceki kapanis (%). Iki tanim: 'govde' |C-O|, 'aralik' H-L (Cemal'in kucuk mum tanimi, CLAUDE.md).
#    B_t      = son k mumun b ortalamasi (k = 3, 4).
#    normal   = AYNI hissenin B degerleri, onceki 250 bar (k bar geriden, ust uste binmez; en az 120 bar).
#    yuzdelik = B_t, hissenin kendi normal dagiliminin yuzde kacinda (0 = gecmisindeki en sakin an). Esik bu yuzdeliktir: her hisse
#               kendi oynakligina gore olculur, sabit bir mum boyu yoktur. oran = B_t / normal medyan (bilgi icin).
#    dizilim  = 'sira' varyanti: k mumun boyu ardisik kuculuyor (b_{t-k+1} >= ... >= b_t).
#    v1.1 (22 Eki): GECERLI MUM sarti (COL_v1 D1 ile ayni): H > L ve hacim > 0. Islem gormeyen ya da tavan/tabanda kilitli
#               (O=H=L=C) gun "sakin" sayilmaz; k mumdan biri gecersizse o gunun olcusu yok, normal dagilima da girmez.
#               v1.0'da ABD sinyallerinin %5'i, BIST sinyallerinin %24'u bu tur barlardan geliyordu (ornek cizimde goruldu).
#  v1.2 (22 Eki) ZEMIN modu. CEMAL: "akiskan bir madde asagi duserken sert ve duz zemine carpip zemine yapisik kalarak n duzleminde
#    bir sira gecmesi; 3 az, 4-5 mumluk bolge." Kopuk kucuk mumlar degil: dipleri hizali, aralarinda acilis boslugu yok, kaymayan sira.
#    Olculer hissenin KENDI normal tek mum araligi (nr = onceki 250 barin H-L/C medyani, k bar geriden) cinsinden:
#      bant = k mumun (maks H - min L)/C / nr      dip_hiza = (k mumun en yuksek dibi - en dusuk dibi)/C / nr
#      bosluk = sira icindeki en buyuk |O_t - C_{t-1}| / nr     kayma = |C_t - O_{t-k+1}|/C / nr
#    Baglam (sert dusus, zemine carpma): siradan once 20 barda kapanis tepeden >= %15 asagi, siradan onceki 10 barda >= %12 asagi,
#      siradan onceki 5 mum normalin >= 1,3 kati (hizla gelen dusus), sira 60 barin dibinde (en dusuk dip <= 60 bar dibi x 1,03),
#      k mumun hepsi gecerli. Varyant z_siki: bant <= 2, dip_hiza <= 0,5, bosluk <= 0,4, kayma <= 0,7; z_gevsek: 2,5 / 0,7 / 0,6 / 1,0.
#      TABAN: ayni baglam, zemin yok (bant >= 3: sira daginik). k = 4, 5, 6. Sonuc ve iz standardi asagidaki ile ayni.
#  v1.3 (22 Eki) KISA UFUK + AYRILMA. CEMAL: "60 gun cok uzun; 2-3 gunluk sikisma %3-5'lik hareket verir. Bolge uzun sikisip
#    oraya para girerse ayrilma sert olur." Zemin olaylarina iki sonuc eklendi (60 gunluk sonuc aynen duruyor):
#    KISA: sinyal kapanisindan 3/5/10 bar icindeki en yuksek ve en dusuk (%, ve hissenin normal mumu cinsinden); 10 bar icinde
#      once +%3 mu -%3 mu, once +%5 mi -%3 mu, once +%5 mi -%5 mi (ayni gun ikisi = olumsuz). Taban yine dagnik sira.
#    AYRILMA: bolge = sira bandi (min L .. maks H) +- 0,5 normal mum; sinyalden sonra barlar bandin icinde kaldikca bolge uzar.
#      Bandi ilk asan bar = ayrilma. bolge_bar = toplam uzunluk, hacim_kat = bolgedeki ortalama hacim / bolge oncesi 50 bar
#      medyani, yon = yukari/asagi, sertlik = ayrilma bari dahil 5 barda banttan uzaklasma, normal mum cinsinden.
#      Sabit kovalar: bolge 4-7 / 8-15 / >=16 bar; hacim <0,8 / 0,8-1,5 / >=1,5. Iz: uzun + hacimli kova kisa kovaya gore
#      dort dilimde de >= 1,3 kat (sert ayrilma = sertlik >= 3 normal mum).
#  BAGLAM: dusus sonrasi = kapanis, son 60 barin en yuksek kapanisinin %80'i veya alti VE son 20 barin en dusugunun %15 yakininda.
#  SINYAL: baglam + yuzdelik <= esik {2, 5, 10}. TABAN: ayni baglam, yuzdelik 30-70 (normal oynaklikta mumlar). Ayni hisse 20 bar
#    icinde bir kez sayilir.
#  SONUC: 20/60 bar ileri kapanis getirisi; 120 bar icinde once +%20 mi -%10 mu (High/Low ile, ayni gun ikisi = olumsuz sayilir).
#  STANDART (CLAUDE.md): BIST 2016-21 ve 2022-26 + ABD 2016-21 ve 2022-26, esikler sabit; iz = dort dilimde de taban oraninin
#    >= 1,3 kati ve getiri ayni yonde. Bu bir YON testidir; gecerse trail + slot simulasyonu ayrica yapilir.
#  KURAL_MOTORU: K1 veri  K2 olcu + olaylar  K3 ozet  K4 tek hisse (bugunku deger)  K5 rapor
#  Calistirma: python MUM_SUKUN.py [--zemin] [hisse ...]   (veri: MS_VERI_BIST / MS_VERI_ABD ortam degiskenleri ya da Drive yolu)
#  Cikti: arastirma_cikti/mum_sukun/ (MUM_SUKUN_rapor.md, mum_sukun_ozet.csv, mum_sukun_olaylar.csv.gz)
# =====================================================================
from __future__ import annotations

import logging
import os
import pickle
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_CK_ONCE_MS = {k: id(v) for k, v in globals().items()}

MS_SURUM = "MUM_SUKUN v1.3 (2026-10-22, hisseye ozel mum kuculmesi; gecerli mum sarti; zemin modu; kisa ufuk + ayrilma)"
mslog = logging.getLogger("col.mum_sukun")
if not mslog.handlers:
    _ms_h = logging.StreamHandler(sys.stderr)
    _ms_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sukun: %(message)s", "%H:%M:%S"))
    mslog.addHandler(_ms_h)
    mslog.setLevel(logging.INFO)
    mslog.propagate = False


@dataclass
class MSAyar:
    k_list: Tuple[int, ...] = (3, 4)
    olculer: Tuple[str, ...] = ("govde", "aralik")
    esikler: Tuple[float, ...] = (2.0, 5.0, 10.0)
    taban_band: Tuple[float, float] = (30.0, 70.0)
    normal: int = 250
    normal_min: int = 120
    dusus: float = 0.20          # son 60 bar en yuksek kapanisa gore en az %20 asagi
    dip_yakin: float = 0.15      # son 20 barin en dusugunun en fazla %15 ustunde
    tekrar: int = 20             # ayni hissede ayni varyant 20 bar icinde bir kez
    ufuk: int = 120
    hedef_yukari: float = 0.20
    hedef_asagi: float = 0.10
    sicrama: float = 0.25        # BIST: bu kadar gunluk hareket veri hatasi (sinir %10); pencerede varsa olay atlanir
    donem_siniri: str = "2022-01-01"
    # v1.2 zemin modu
    zemin_k: Tuple[int, ...] = (4, 5, 6)
    zemin_esik: Dict[str, Tuple[float, float, float, float]] = field(default_factory=lambda: {
        "z_siki": (2.0, 0.5, 0.4, 0.7), "z_gevsek": (2.5, 0.7, 0.6, 1.0)})   # bant, dip_hiza, bosluk, kayma (nr cinsinden)
    zemin_taban_bant: float = 3.0   # taban: ayni baglam, sira daginik
    zemin_dusus20: float = 0.15
    zemin_hiz10: float = 0.12
    zemin_carp: float = 1.3
    zemin_dip: float = 0.03
    # v1.3 kisa ufuk + ayrilma
    kisa_ufuk: Tuple[int, ...] = (3, 5, 10)
    kisa_hedef: Tuple[Tuple[float, float], ...] = ((3.0, 3.0), (5.0, 3.0), (5.0, 5.0))   # (+% , -%) once hangisi, 10 bar
    kisa_sure: int = 10
    ayrilma_tol: float = 0.5     # bant payi, normal mum cinsinden
    ayrilma_max: int = 120       # bolge en fazla bu kadar uzar
    ayrilma_bar: int = 5         # sertlik penceresi
    sert_esik: float = 3.0       # sertlik >= 3 normal mum = sert ayrilma
    veri: Dict[str, str] = field(default_factory=lambda: {
        "BIST": os.environ.get("MS_VERI_BIST", "/content/drive/MyDrive/col_tarayici/veri_1d_turkey.pkl"),
        "ABD": os.environ.get("MS_VERI_ABD", "/content/drive/MyDrive/col_tarayici/veri_1d_america.pkl"),
    })
    cikti: str = "arastirma_cikti/mum_sukun"


# ---------------------------------------------------------------- K1 veri
def ms_k1_veri(yol: str) -> Dict[str, pd.DataFrame]:
    """pkl: {sembol: OHLC DataFrame} ya da {'veri': {...}} (veri_1d_turkey.pkl yapisi)."""
    if not os.path.exists(yol):
        raise FileNotFoundError(f"veri yok: {yol}")
    with open(yol, "rb") as f:
        V = pickle.load(f)
    if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
        V = V["veri"]
    temiz = {}
    for s, d in V.items():
        try:
            kol = ["Open", "High", "Low", "Close"] + (["Volume"] if "Volume" in d.columns else [])
            d = d[kol].astype(float).dropna(subset=["Open", "High", "Low", "Close"])
            d = d[(d.High >= d.Low) & (d.Close > 0)]
            if len(d) >= 150:  # normal_min 120 + k; olay icin ayrica normal_min aranir
                temiz[str(s)] = d.sort_index()
        except Exception as ex:  # tek hisse bozuksa digerleri devam eder
            mslog.warning("%s atlandi: %s", s, ex)
    mslog.info("%s: %d hisse", yol, len(temiz))
    return temiz


# ---------------------------------------------------------------- K2 olcu
def _mum_boyu(d: pd.DataFrame, k: int, olcu: str) -> Tuple[pd.Series, pd.Series]:
    """b: gunluk mum boyu (%); B: son k mum ortalamasi. Gecersiz mum (H <= L ya da hacim 0) iceren pencere NaN."""
    pc = d.Close.shift(1)
    b = ((d.Close - d.Open).abs() if olcu == "govde" else (d.High - d.Low)) / pc * 100
    gecerli = d.High > d.Low
    if "Volume" in d.columns and d.Volume.notna().any():
        gecerli &= d.Volume.fillna(0) > 0
    b = b.where(gecerli)
    tam = gecerli.astype(int).rolling(k, min_periods=k).sum() == k
    B = b.rolling(k, min_periods=k).mean().where(tam)
    return b, B


def ms_olcu(d: pd.DataFrame, k: int, olcu: str, A: MSAyar) -> pd.DataFrame:
    """Her gun: B (son k mum ortalama boyu, %), hissenin kendi normal yuzdelik esikleri, yuzdelik ve dizilim."""
    b, B = _mum_boyu(d, k, olcu)
    gecmis = B.shift(k)
    roll = gecmis.rolling(A.normal, min_periods=A.normal_min)
    out = pd.DataFrame({"B": B, "med": roll.median()})
    for q in sorted(set(A.esikler) | set(A.taban_band)):
        out[f"q{int(q):02d}"] = roll.quantile(q / 100.0)
    out["oran"] = out.B / out.med
    sira = pd.Series(True, index=d.index)
    for j in range(1, k):
        sira &= b.shift(j - 1) <= b.shift(j)
    out["sira"] = sira
    return out


def ms_yuzdelik(d: pd.DataFrame, k: int, olcu: str, A: MSAyar) -> Dict[str, float]:
    """Son gun icin tam yuzdelik (tek hisse raporu)."""
    b, B = _mum_boyu(d, k, olcu)
    if len(B) < k + 30 or not np.isfinite(B.iloc[-1]):
        return {"B": np.nan, "yuzdelik": np.nan, "oran": np.nan, "normal_bar": int(B.notna().sum()), "not": "son mumlar gecersiz ya da veri kisa"}
    son = B.iloc[-1]
    gecmis = B.iloc[:-k].iloc[-A.normal:].dropna()
    return {"B": round(float(son), 2), "yuzdelik": round(float((gecmis <= son).mean() * 100), 1),
            "oran": round(float(son / gecmis.median()), 2), "normal_bar": int(len(gecmis)),
            "son_mumlar": [round(float(x), 2) for x in b.iloc[-k:]], "normal_medyan": round(float(gecmis.median()), 2)}


def _sonuc(d: pd.DataFrame, i: int, A: MSAyar) -> Dict[str, float]:
    c = d.Close.to_numpy(); h = d.High.to_numpy(); l = d.Low.to_numpy(); n = len(c)
    r = {"r20": (c[i + 20] / c[i] - 1) * 100 if i + 20 < n else np.nan,
         "r60": (c[i + 60] / c[i] - 1) * 100 if i + 60 < n else np.nan}
    if i + 1 >= n:
        r["once_yukari"] = np.nan; return r
    up = c[i] * (1 + A.hedef_yukari); dn = c[i] * (1 - A.hedef_asagi)
    son = min(n, i + 1 + A.ufuk); sonuc = np.nan
    for j in range(i + 1, son):
        u = h[j] >= up; a = l[j] <= dn
        if a:
            sonuc = 0.0; break
        if u:
            sonuc = 1.0; break
    if np.isnan(sonuc) and son - (i + 1) >= A.ufuk:
        sonuc = 0.0
    r["once_yukari"] = sonuc
    return r


def _temiz_pencere(c: pd.Series, A: MSAyar) -> np.ndarray:
    """BIST: veri sicramasi (bolunme/bedelsiz izi) olcu penceresinde varsa o gun olay sayilmaz. Denetim 24 Eki: eskiden ileri
    pencereye (gelecek 120 bar) de bakiyordu -> olay secimi gelecege bagliydi; simdi yalniz gecmis (sonuc etkilenmedi: 1,06 -> 1,07)."""
    bozuk = (c.pct_change().abs() > A.sicrama).to_numpy().astype(int)
    cs = np.concatenate([[0], np.cumsum(bozuk)]); n = len(c); ii = np.arange(n)
    bas = np.maximum(0, ii - A.normal - 10); bit = np.minimum(n, ii + 1)
    return (cs[bit] - cs[bas]) == 0


def ms_k2_olaylar(V: Dict[str, pd.DataFrame], pazar: str, A: MSAyar) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    t0 = time.time()
    for no, (s, d) in enumerate(V.items(), 1):
        c = d.Close
        hi60 = c.rolling(60, min_periods=40).max().shift(1)
        lo20 = d.Low.rolling(20, min_periods=15).min()
        baglam = ((c <= hi60 * (1 - A.dusus)) & (c <= lo20 * (1 + A.dip_yakin))).to_numpy().copy()
        if pazar == "BIST":
            baglam &= _temiz_pencere(c, A)
        if not baglam.any():
            continue
        idx = np.flatnonzero(baglam)
        for k in A.k_list:
            for olcu in A.olculer:
                M = ms_olcu(d, k, olcu, A)
                Bv = M.B.to_numpy(); siv = M.sira.to_numpy()
                varyant = {f"p{int(e):02d}": M[f"q{int(e):02d}"].to_numpy() for e in A.esikler}
                lo_q = M[f"q{int(A.taban_band[0]):02d}"].to_numpy(); hi_q = M[f"q{int(A.taban_band[1]):02d}"].to_numpy()
                secim: Dict[str, np.ndarray] = {}
                for ad, q in varyant.items():
                    m = np.isfinite(q) & (Bv <= q)
                    secim[ad] = m
                    secim[ad + "_sira"] = m & siv
                secim["taban"] = np.isfinite(lo_q) & (Bv >= lo_q) & (Bv <= hi_q)
                for ad, m in secim.items():
                    son = -10 ** 9
                    for i in idx:
                        if not m[i] or i - son < A.tekrar:
                            continue
                        son = i
                        rr = _sonuc(d, i, A)
                        rows.append({"pazar": pazar, "sembol": s, "tarih": d.index[i], "k": k, "olcu": olcu, "varyant": ad,
                                     "oran": float(M.oran.iat[i]) if np.isfinite(M.oran.iat[i]) else np.nan, **rr})
        if no % 200 == 0:
            mslog.info("%s %d/%d hisse, %d olay, %.0f sn", pazar, no, len(V), len(rows), time.time() - t0)
    O = pd.DataFrame(rows)
    if not O.empty:
        O["donem"] = np.where(pd.to_datetime(O.tarih) < pd.Timestamp(A.donem_siniri), "2016-21", "2022-26")
        O = O[pd.to_datetime(O.tarih) >= pd.Timestamp("2016-01-01")]
    return O


# ---------------------------------------------------------------- K2z zemin (v1.2)
def ms_zemin_olcu(d: pd.DataFrame, k: int, A: MSAyar) -> pd.DataFrame:
    """Her gun, o gun biten k mumluk sira icin zemin olculeri (hissenin kendi normal mum araligi cinsinden) ve baglam."""
    O, H, L, C = d.Open, d.High, d.Low, d.Close
    gec = H > L
    if "Volume" in d.columns and d.Volume.notna().any():
        gec &= d.Volume.fillna(0) > 0
    r = ((H - L) / C).where(gec)
    nr = r.shift(k).rolling(A.normal, min_periods=A.normal_min).median()
    Lm = L.rolling(k).min()
    out = pd.DataFrame(index=d.index)
    out["bant"] = (H.rolling(k).max() - Lm) / C / nr
    out["dip_hiza"] = (L.rolling(k).max() - Lm) / C / nr
    out["bosluk"] = ((O - C.shift()).abs() / C.shift() / nr).rolling(k - 1).max()
    out["kayma"] = (C - O.shift(k - 1)).abs() / C / nr
    out["tam"] = gec.astype(int).rolling(k).sum() == k
    once = C.shift(k)
    out["dusus20"] = once / once.rolling(20, min_periods=15).max() - 1
    out["hiz10"] = once / once.rolling(10, min_periods=8).max() - 1
    out["carp"] = r.shift(k).rolling(5, min_periods=4).mean() / nr
    out["dipte"] = Lm <= L.rolling(60, min_periods=40).min() * (1 + A.zemin_dip)
    out["baglam"] = (out.tam & out.dipte & (out.dusus20 <= -A.zemin_dusus20) & (out.hiz10 <= -A.zemin_hiz10)
                     & (out.carp >= A.zemin_carp) & nr.notna())
    for ad, (b, dh, bo, ka) in A.zemin_esik.items():
        out[ad] = out.baglam & (out.bant <= b) & (out.dip_hiza <= dh) & (out.bosluk <= bo) & (out.kayma <= ka)
    out["taban"] = out.baglam & (out.bant >= A.zemin_taban_bant)
    out["nr"] = nr
    return out


def _sonuc_kisa(d: pd.DataFrame, i: int, nr: float, A: MSAyar) -> Dict[str, float]:
    """v1.3: sinyal kapanisindan kisa ufukta en yuksek/en dusuk ve once hangi hedef."""
    c = d.Close.to_numpy(); h = d.High.to_numpy(); l = d.Low.to_numpy(); n = len(c); r: Dict[str, float] = {}
    for u in A.kisa_ufuk:
        if i + u < n:
            up = (h[i + 1:i + u + 1].max() / c[i] - 1) * 100; dn = (1 - l[i + 1:i + u + 1].min() / c[i]) * 100
        else:
            up = dn = np.nan
        r[f"yuk{u}"] = up; r[f"dus{u}"] = dn
        r[f"yuk{u}_nr"] = up / (nr * 100) if np.isfinite(nr) and nr > 0 else np.nan
    for (hu, hd) in A.kisa_hedef:
        ad = f"once_{int(hu)}_{int(hd)}"
        if i + A.kisa_sure >= n:
            r[ad] = np.nan; continue
        up_s = c[i] * (1 + hu / 100); dn_s = c[i] * (1 - hd / 100); snc = 0.0   # sure dolarsa olumsuz
        for j in range(i + 1, i + A.kisa_sure + 1):
            if l[j] <= dn_s:
                snc = 0.0; break
            if h[j] >= up_s:
                snc = 1.0; break
        r[ad] = snc
    return r


def _ayrilma(d: pd.DataFrame, i: int, k: int, nr: float, A: MSAyar) -> Dict[str, float]:
    """v1.3: sira bandinin uzadigi bolge ve ondan ayrilma (bolge uzunlugu, hacim, yon, sertlik)."""
    bos = {"bolge_bar": np.nan, "hacim_kat": np.nan, "yon": np.nan, "sertlik": np.nan, "sertlik_pct": np.nan, "ayrilma_gun": pd.NaT}
    if not (np.isfinite(nr) and nr > 0):
        return bos
    h = d.High.to_numpy(); l = d.Low.to_numpy(); c = d.Close.to_numpy(); n = len(c); s0 = i - k + 1
    pay = A.ayrilma_tol * nr * c[i]
    ust = h[s0:i + 1].max() + pay; alt = l[s0:i + 1].min() - pay
    e = i + 1
    while e < n and e - i <= A.ayrilma_max and h[e] <= ust and l[e] >= alt:
        e += 1
    if e >= n or e - i > A.ayrilma_max or e + A.ayrilma_bar > n:
        return bos
    yukari = h[e] > ust and not (l[e] < alt and c[e] < (ust + alt) / 2)
    son = e + A.ayrilma_bar
    if yukari:
        sert = (h[e:son].max() - ust) / c[i]
    else:
        sert = (alt - l[e:son].min()) / c[i]
    hk = np.nan
    if "Volume" in d.columns:
        v = d.Volume.to_numpy(dtype=float)
        once = v[max(0, s0 - 50):s0]; once = once[once > 0]
        if len(once) >= 20:
            hk = float(np.mean(v[s0:e]) / np.median(once))
    return {"bolge_bar": float(e - s0), "hacim_kat": hk, "yon": 1.0 if yukari else -1.0,
            "sertlik": float(sert / nr), "sertlik_pct": float(sert * 100), "ayrilma_gun": d.index[e]}


def ms_k2z_olaylar(V: Dict[str, pd.DataFrame], pazar: str, A: MSAyar) -> pd.DataFrame:
    """Zemin olaylari; ciktinin bicimi ms_k2_olaylar ile ayni (olcu='zemin'), boylece K3 ozet ve iz ayni kalir."""
    rows: List[Dict[str, Any]] = []
    t0 = time.time()
    varyantlar = list(A.zemin_esik) + ["taban"]
    for no, (s, d) in enumerate(V.items(), 1):
        try:
            temiz = _temiz_pencere(d.Close, A) if pazar == "BIST" else np.ones(len(d), bool)
            for k in A.zemin_k:
                Z = ms_zemin_olcu(d, k, A)
                for ad in varyantlar:
                    m = Z[ad].to_numpy(dtype=bool) & temiz
                    son = -10 ** 9
                    for i in np.flatnonzero(m):
                        if i - son < A.tekrar:
                            continue
                        son = i
                        nri = float(Z.nr.iat[i])
                        rows.append({"pazar": pazar, "sembol": s, "tarih": d.index[i], "k": k, "olcu": "zemin", "varyant": ad,
                                     "oran": float(Z.bant.iat[i]), **_sonuc(d, i, A), **_sonuc_kisa(d, i, nri, A),
                                     **_ayrilma(d, i, k, nri, A)})
        except Exception as ex:  # tek hisse bozuksa digerleri devam eder
            mslog.warning("zemin %s atlandi: %s", s, ex)
        if no % 200 == 0:
            mslog.info("zemin %s %d/%d hisse, %d olay, %.0f sn", pazar, no, len(V), len(rows), time.time() - t0)
    O = pd.DataFrame(rows)
    if not O.empty:
        O["donem"] = np.where(pd.to_datetime(O.tarih) < pd.Timestamp(A.donem_siniri), "2016-21", "2022-26")
        O = O[pd.to_datetime(O.tarih) >= pd.Timestamp("2016-01-01")]
    return O


def ms_zemin_bugun(d: pd.DataFrame, A: Optional[MSAyar] = None) -> pd.DataFrame:
    """Tek hisse: son gun biten 4/5/6 mumluk sira zemin mi (olculer ve hangi kosul tutmadi)."""
    A = A or MSAyar()
    rows = []
    for k in A.zemin_k:
        Z = ms_zemin_olcu(d, k, A).iloc[-1]
        rows.append({"k": k, **{c: (round(float(Z[c]), 2) if not isinstance(Z[c], (bool, np.bool_)) else bool(Z[c]))
                                for c in ["bant", "dip_hiza", "bosluk", "kayma", "dusus20", "hiz10", "carp", "dipte", "baglam",
                                          *A.zemin_esik, "taban"]}})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- K3z zemin kisa ufuk + ayrilma ozeti (v1.3)
def ms_k3z_kisa(O: pd.DataFrame, A: MSAyar) -> pd.DataFrame:
    """Kisa ufuk: varyant x dilim; once-hedef oranlari ve tabana gore kat."""
    hed = [f"once_{int(u)}_{int(dd)}" for u, dd in A.kisa_hedef]
    agg = {"n": ("sembol", "size"), **{h: (h, "mean") for h in hed}}
    for u in A.kisa_ufuk:
        agg[f"yuk{u}_med"] = (f"yuk{u}", "median"); agg[f"dus{u}_med"] = (f"dus{u}", "median")
        agg[f"yuk{u}_nr_med"] = (f"yuk{u}_nr", "median")
    g = O.groupby(["k", "varyant", "pazar", "donem"]).agg(**agg).reset_index()
    for h in hed:
        g[h] *= 100
    t = g[g.varyant == "taban"][["k", "pazar", "donem"] + hed].rename(columns={h: "t_" + h for h in hed})
    g = g.merge(t, on=["k", "pazar", "donem"], how="left")
    for h in hed:
        g["kat_" + h[5:]] = g[h] / g["t_" + h]
    return g


def ms_iz_kisa(g: pd.DataFrame, A: MSAyar, min_n: int = 30) -> pd.DataFrame:
    rows = []
    for (k, v), s in g[g.varyant != "taban"].groupby(["k", "varyant"]):
        for u, dd in A.kisa_hedef:
            kc = f"kat_{int(u)}_{int(dd)}"
            rows.append({"k": k, "varyant": v, "hedef": f"+{int(u)}/-{int(dd)}", "dilim": len(s),
                         "gecti": int(((s[kc] >= 1.3) & (s.n >= min_n)).sum()), "ayni_yon": int((s[kc] > 1.0).sum()),
                         "kat_min": s[kc].min(), "kat_ort": s[kc].mean(), "n_min": int(s.n.min())})
    return pd.DataFrame(rows)


def ms_k3z_ayrilma(O: pd.DataFrame, A: MSAyar) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Ayrilma: z_gevsek olaylari (z_siki onun alt kumesi). Ayni bolgeden (ayni ayrilma gunu) gelen k=4/5/6 olaylari tek
    sayilir, en kucuk k tutulur. Sabit kovalar."""
    Z = O[(O.varyant == "z_gevsek") & O.sertlik.notna()].sort_values(["k", "tarih"])
    Z = Z.drop_duplicates(["pazar", "sembol", "ayrilma_gun"]).copy()
    Z["boy"] = pd.cut(Z.bolge_bar, [0, 7, 15, 10 ** 6], labels=["4-7", "8-15", ">=16"])
    Z["hac"] = pd.cut(Z.hacim_kat, [0, 0.8, 1.5, 10 ** 6], right=False, labels=["<0,8", "0,8-1,5", ">=1,5"])
    Z["sert"] = (Z.sertlik >= A.sert_esik).astype(float) * 100
    Z["yuk"] = (Z.yon > 0).astype(float) * 100
    f = dict(n=("sembol", "size"), sert_oran=("sert", "mean"), sertlik_med=("sertlik", "median"),
             sertlik_pct_med=("sertlik_pct", "median"), yukari=("yuk", "mean"))
    t1 = Z.groupby(["pazar", "donem", "boy"], observed=True).agg(**f).reset_index()
    t2 = Z.groupby(["pazar", "donem", "boy", "hac"], observed=True).agg(**f).reset_index()
    return t1, t2


# ---------------------------------------------------------------- K3 ozet
def ms_k3_ozet(O: pd.DataFrame) -> pd.DataFrame:
    g = O.groupby(["k", "olcu", "varyant", "pazar", "donem"]).agg(
        n=("sembol", "size"), once_yukari=("once_yukari", "mean"), r20=("r20", "median"), r60=("r60", "median")).reset_index()
    g["once_yukari"] *= 100
    t = g[g.varyant == "taban"][["k", "olcu", "pazar", "donem", "once_yukari", "r20", "r60"]].rename(
        columns={"once_yukari": "t_once", "r20": "t_r20", "r60": "t_r60"})
    g = g.merge(t, on=["k", "olcu", "pazar", "donem"], how="left")
    g["kat"] = g.once_yukari / g.t_once
    g["r60_fark"] = g.r60 - g.t_r60
    return g


def ms_iz(oz: pd.DataFrame, min_n: int = 30) -> pd.DataFrame:
    """Varyant basina: dort dilimin (2 pazar x 2 donem) kacinda kat >= 1,3 ve r60 tabandan iyi."""
    s = oz[oz.varyant != "taban"].copy()
    s["gecti"] = (s.kat >= 1.3) & (s.r60_fark > 0) & (s.n >= min_n)
    s["yon"] = (s.kat > 1.0) & (s.r60_fark > 0)
    return s.groupby(["k", "olcu", "varyant"]).agg(dilim=("n", "size"), gecti=("gecti", "sum"), ayni_yon=("yon", "sum"),
                                                     kat_min=("kat", "min"), kat_ort=("kat", "mean"), n_min=("n", "min")).reset_index()


# ---------------------------------------------------------------- K4 tek hisse
def ms_k4_hisse(d: pd.DataFrame, A: Optional[MSAyar] = None) -> pd.DataFrame:
    A = A or MSAyar()
    rows = []
    for k in A.k_list:
        for olcu in A.olculer:
            rows.append({"k": k, "olcu": olcu, **ms_yuzdelik(d, k, olcu, A)})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- K5 rapor
def ms_k5_rapor(oz: pd.DataFrame, iz: pd.DataFrame, hisseler: Dict[str, pd.DataFrame], mod: str = "sukun",
                ekler: Optional[Dict[str, pd.DataFrame]] = None) -> str:
    if mod == "zemin":
        sat = [f"# MUM_SUKUN zemin — {MS_SURUM}", "",
               "Soru (Cemal, 22 Eki): sert dusus duz bir zemine carpip 4-6 mum dipleri hizali, bosluksuz, kaymadan yan yana dizilince isaret mi?",
               "Olculer hissenin kendi normal mum araligi cinsinden (dosya basindaki v1.2 notu). Taban: ayni sert dusus baglami, sira daginik (bant >= 3).",
               "Iz: 4 dilimde (BIST/ABD x 2016-21/2022-26) kat >= 1,3 ve 60g getiri tabandan iyi, her dilimde n >= 30.", ""]
        sat += ["## Varyant ozeti (4 dilim)", "", iz.sort_values(["gecti", "ayni_yon", "kat_ort"], ascending=False).round(2).to_markdown(index=False), ""]
        sat += ["## Dilim ayrintisi", "", oz.round(2).to_markdown(index=False), ""]
        for baslik, t in (ekler or {}).items():
            sat += [f"## {baslik}", "", t.round(2).to_markdown(index=False), ""]
        for s, t in hisseler.items():
            sat += [f"## {s} bugun", "", t.to_markdown(index=False), ""]
        return "\n".join(sat)
    sat = [f"# MUM_SUKUN — {MS_SURUM}", "",
           "Soru (Cemal, 22 Eki): dusus sonrasi son 3-4 mumun kuculmesi, hissenin KENDI normal oynakligina gore olculunce bir isaret mi?",
           "Olcu: son k mumun ortalama boyu, ayni hissenin onceki 250 bardaki dagiliminin yuzde kacinda. Sinyal: yuzdelik <= esik.",
           "Taban: ayni dusus baglaminda normal boyda mumlar (yuzdelik 30-70). Iz: 4 dilimde (BIST/ABD x 2016-21/2022-26) kat >= 1,3 ve 60g getiri tabandan iyi.", ""]
    sat += ["## Varyant ozeti (4 dilim)", "", iz.sort_values(["gecti", "ayni_yon", "kat_ort"], ascending=False).round(2).to_markdown(index=False), ""]
    sat += ["## Dilim ayrintisi", "", oz.round(2).to_markdown(index=False), ""]
    for s, t in hisseler.items():
        sat += [f"## {s} bugun", "", t.to_markdown(index=False), ""]
    return "\n".join(sat)


def mum_sukun(hisse_listesi: Optional[List[str]] = None, A: Optional[MSAyar] = None, mod: str = "sukun") -> Dict[str, Any]:
    """mod='sukun': v1.1 mum kuculmesi testi. mod='zemin': v1.2 duz zemin testi (ayri cikti dosyalari)."""
    if mod not in ("sukun", "zemin"):
        raise ValueError(f"mod sukun ya da zemin olmali: {mod}")
    A = A or MSAyar()
    on = "zemin_" if mod == "zemin" else "mum_sukun_"
    k2 = ms_k2z_olaylar if mod == "zemin" else ms_k2_olaylar
    k4 = ms_zemin_bugun if mod == "zemin" else ms_k4_hisse
    os.makedirs(A.cikti, exist_ok=True)
    tum = []; veri = {}
    for pazar, yol in A.veri.items():
        try:
            V = ms_k1_veri(yol)
        except Exception as ex:
            mslog.error("%s verisi okunamadi (%s); bu pazar atlandi", pazar, ex)
            continue
        veri[pazar] = V
        tum.append(k2(V, pazar, A))
    if not tum:
        raise RuntimeError("hic veri okunamadi")
    O = pd.concat(tum, ignore_index=True)
    O.to_csv(os.path.join(A.cikti, on + "olaylar.csv.gz"), index=False)
    oz = ms_k3_ozet(O); iz = ms_iz(oz)
    oz.to_csv(os.path.join(A.cikti, on + "ozet.csv"), index=False)
    ekler: Dict[str, pd.DataFrame] = {}
    if mod == "zemin":
        try:
            gk = ms_k3z_kisa(O, A); izk = ms_iz_kisa(gk, A); a1, a2 = ms_k3z_ayrilma(O, A)
            gk.to_csv(os.path.join(A.cikti, "zemin_kisa_ozet.csv"), index=False)
            a1.to_csv(os.path.join(A.cikti, "zemin_ayrilma_boy.csv"), index=False)
            a2.to_csv(os.path.join(A.cikti, "zemin_ayrilma_boy_hacim.csv"), index=False)
            ekler = {"v1.3 KISA UFUK iz ozeti (10 bar icinde once hedef, tabana gore kat)": izk,
                     "v1.3 KISA UFUK dilim ayrintisi": gk,
                     "v1.3 AYRILMA bolge uzunluguna gore (z_gevsek)": a1,
                     "v1.3 AYRILMA bolge uzunlugu x hacim": a2}
        except Exception as ex:  # ek ozet bozulursa ana sonuc yine yazilir
            mslog.error("v1.3 kisa/ayrilma ozeti yazilamadi: %s", ex)
    hs = {}
    for s in hisse_listesi or []:
        for V in veri.values():
            if s in V:
                hs[s] = k4(V[s], A); break
    rapor = ms_k5_rapor(oz, iz, hs, mod, ekler)
    with open(os.path.join(A.cikti, "MUM_SUKUN_zemin_rapor.md" if mod == "zemin" else "MUM_SUKUN_rapor.md"), "w", encoding="utf-8") as f:
        f.write(rapor)
    return {"olaylar": O, "ozet": oz, "iz": iz, "hisse": hs, "rapor": rapor, "ekler": ekler}


def _cakisma_kontrol_ms(_once=_CK_ONCE_MS, _dosya='MUM_SUKUN.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_MS', '_CK_KAYIT', '_cakisma_kontrol_ms', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'time', 'pickle', 'logging', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass', 'field')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ms()

if __name__ == "__main__":
    _arg = sys.argv[1:]
    _mod = "zemin" if "--zemin" in _arg else "sukun"
    R = mum_sukun([a for a in _arg if not a.startswith("--")], mod=_mod)
    print(R["iz"].sort_values(["gecti", "ayni_yon", "kat_ort"], ascending=False).round(2).to_string(index=False))
    for s, t in R["hisse"].items():
        print(f"\n{s} bugun:\n{t.to_string(index=False)}")
