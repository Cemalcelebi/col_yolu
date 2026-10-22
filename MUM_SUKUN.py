# =====================================================================
#  MUM_SUKUN — dusus sonrasi 3-4 mumluk sukunet, her hissenin KENDI normaline gore   (2026-10-22, v1.1)
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
#  BAGLAM: dusus sonrasi = kapanis, son 60 barin en yuksek kapanisinin %80'i veya alti VE son 20 barin en dusugunun %15 yakininda.
#  SINYAL: baglam + yuzdelik <= esik {2, 5, 10}. TABAN: ayni baglam, yuzdelik 30-70 (normal oynaklikta mumlar). Ayni hisse 20 bar
#    icinde bir kez sayilir.
#  SONUC: 20/60 bar ileri kapanis getirisi; 120 bar icinde once +%20 mi -%10 mu (High/Low ile, ayni gun ikisi = olumsuz sayilir).
#  STANDART (CLAUDE.md): BIST 2016-21 ve 2022-26 + ABD 2016-21 ve 2022-26, esikler sabit; iz = dort dilimde de taban oraninin
#    >= 1,3 kati ve getiri ayni yonde. Bu bir YON testidir; gecerse trail + slot simulasyonu ayrica yapilir.
#  KURAL_MOTORU: K1 veri  K2 olcu + olaylar  K3 ozet  K4 tek hisse (bugunku deger)  K5 rapor
#  Calistirma: python MUM_SUKUN.py [hisse ...]   (veri: MS_VERI_BIST / MS_VERI_ABD ortam degiskenleri ya da Drive yolu)
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

MS_SURUM = "MUM_SUKUN v1.1 (2026-10-22, hisseye ozel mum kuculmesi; gecerli mum sarti)"
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


def ms_k2_olaylar(V: Dict[str, pd.DataFrame], pazar: str, A: MSAyar) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    t0 = time.time()
    for no, (s, d) in enumerate(V.items(), 1):
        c = d.Close
        hi60 = c.rolling(60, min_periods=40).max().shift(1)
        lo20 = d.Low.rolling(20, min_periods=15).min()
        baglam = ((c <= hi60 * (1 - A.dusus)) & (c <= lo20 * (1 + A.dip_yakin))).to_numpy().copy()
        if pazar == "BIST":
            # veri sicramasi (bolunme/bedelsiz izi) olcu penceresinde ya da ileri pencerede varsa olay sayilmaz
            bozuk = (c.pct_change().abs() > A.sicrama).to_numpy().astype(int)
            cs = np.concatenate([[0], np.cumsum(bozuk)]); n = len(c); ii = np.arange(n)
            bas = np.maximum(0, ii - A.normal - 10); bit = np.minimum(n, ii + A.ufuk + 1)
            baglam &= (cs[bit] - cs[bas]) == 0
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
def ms_k5_rapor(oz: pd.DataFrame, iz: pd.DataFrame, hisseler: Dict[str, pd.DataFrame]) -> str:
    sat = [f"# MUM_SUKUN — {MS_SURUM}", "",
           "Soru (Cemal, 22 Eki): dusus sonrasi son 3-4 mumun kuculmesi, hissenin KENDI normal oynakligina gore olculunce bir isaret mi?",
           "Olcu: son k mumun ortalama boyu, ayni hissenin onceki 250 bardaki dagiliminin yuzde kacinda. Sinyal: yuzdelik <= esik.",
           "Taban: ayni dusus baglaminda normal boyda mumlar (yuzdelik 30-70). Iz: 4 dilimde (BIST/ABD x 2016-21/2022-26) kat >= 1,3 ve 60g getiri tabandan iyi.", ""]
    sat += ["## Varyant ozeti (4 dilim)", "", iz.sort_values(["gecti", "ayni_yon", "kat_ort"], ascending=False).round(2).to_markdown(index=False), ""]
    sat += ["## Dilim ayrintisi", "", oz.round(2).to_markdown(index=False), ""]
    for s, t in hisseler.items():
        sat += [f"## {s} bugun", "", t.to_markdown(index=False), ""]
    return "\n".join(sat)


def mum_sukun(hisse_listesi: Optional[List[str]] = None, A: Optional[MSAyar] = None) -> Dict[str, Any]:
    A = A or MSAyar()
    os.makedirs(A.cikti, exist_ok=True)
    tum = []; veri = {}
    for pazar, yol in A.veri.items():
        try:
            V = ms_k1_veri(yol)
        except Exception as ex:
            mslog.error("%s verisi okunamadi (%s); bu pazar atlandi", pazar, ex)
            continue
        veri[pazar] = V
        tum.append(ms_k2_olaylar(V, pazar, A))
    if not tum:
        raise RuntimeError("hic veri okunamadi")
    O = pd.concat(tum, ignore_index=True)
    O.to_csv(os.path.join(A.cikti, "mum_sukun_olaylar.csv.gz"), index=False)
    oz = ms_k3_ozet(O); iz = ms_iz(oz)
    oz.to_csv(os.path.join(A.cikti, "mum_sukun_ozet.csv"), index=False)
    hs = {}
    for s in hisse_listesi or []:
        for V in veri.values():
            if s in V:
                hs[s] = ms_k4_hisse(V[s], A); break
    rapor = ms_k5_rapor(oz, iz, hs)
    with open(os.path.join(A.cikti, "MUM_SUKUN_rapor.md"), "w", encoding="utf-8") as f:
        f.write(rapor)
    return {"olaylar": O, "ozet": oz, "iz": iz, "hisse": hs, "rapor": rapor}


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
    R = mum_sukun(sys.argv[1:])
    print(R["iz"].sort_values(["gecti", "ayni_yon", "kat_ort"], ascending=False).round(2).to_string(index=False))
    for s, t in R["hisse"].items():
        print(f"\n{s} bugun:\n{t.to_string(index=False)}")
