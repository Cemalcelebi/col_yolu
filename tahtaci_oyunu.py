# -*- coding: utf-8 -*-
"""
TAHTACI OYUNU v1.3 — defter değeri altına düşmüş hissede hâkim ortağın (tahtacı) oyunu
=====================================================================================
Soru: Zorla satışla defter değerinin altına inen hissede tahtacı ne yapar?
  1. KLİMAKS  : satan tükenirken (en yüksek hacim + en düşük fiyat + kapanış üst yarıda) toplar.
  2. TEPKİ    : alıcı gelince fiyat yükselir; tahtacı sessiz kalır.
  3. DAĞITIM  : kalabalık hacimle girince (yüksek hacim + üst fitil / zayıf kapanış) satar.
  4. SESSİZ GERİ ÇEKİLME : hacim kuruyup fiyat maliyetine yaklaşınca yeniden alır.
  5. KIRILDI  : klimaks dibinin altında kapanış → oyun bitti, tez yanlış.
  TEYİT kolu : klimaksta alma; ilk teyit_gun içinde kapanış klimaks yükseğinin üstüne çıkınca (dip kırılmadan) al, stop dip.
Bu dosya bu fazları ÖLÇER ve geçmişte (veri_1d_turkey.pkl) test eder. Alım-satım kararı vermez.

Veri:  {K}/veri_1d_turkey.pkl  ({"kayit","veri":{sembol: OHLCV}})
Temel: ÖNCE {K}/temel_duz.csv (temel.py, İş Yatırım 2022-2026; açıklama tarihli özkaynak ve net borç → DÖNEM BAZLI,
       olay gününde bilinen son bilanço) + hisse sayısı tahtaci_temel.pkl'den (yfinance, bugünkü; fiyat bölünme-düzeltili olduğu
       için tutarlı, bedelli artırım payı kalır). temel_duz yoksa: tahtaci_temel.csv ya da yfinance bugünkü defter (uyarılı).

Kullanım (Colab):
    exec(open(K + "/tahtaci_oyunu.py", encoding="utf-8").read())
    R = tahtaci_olc(K)          # geçmiş ölçüm (tüm BIST, 2023-06'dan)
    tahtaci_bugun(K)            # bugün hangi hisse hangi fazda
Tüm isimler `to_` / `TO_` ön ekiyle başlar; çakışma kapısı yüklenirken mevcut isimleri ezmez.
"""
from __future__ import annotations

import logging
import math
import os
import pickle
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

TO_SURUM = "1.3"
_to_log = logging.getLogger("tahtaci_oyunu")
if not _to_log.handlers:
    _h = logging.StreamHandler(sys.stdout)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s tahtaci: %(message)s", "%H:%M:%S"))
    _to_log.addHandler(_h)
_to_log.setLevel(logging.INFO)
_to_log.propagate = False

# ---------------------------------------------------------------- çakışma kapısı (tanımlardan ÖNCE)
_TO_ISIMLER = ("TahtaciTanim", "to_veri_ac", "to_ohlcv", "to_evren", "to_temel_oku", "to_metrikler", "to_oyun", "to_olaylar",
               "to_karne", "to_hukum", "to_rapor", "tahtaci_olc", "tahtaci_bugun")
_to_g = globals()
_to_catisan = [k for k in _TO_ISIMLER if k in _to_g and _to_g.get("_TO_IMZA") != "tahtaci_oyunu"]
if _to_catisan:
    raise RuntimeError(f"çakışma kapısı: bellekte başka bir '{_to_catisan[0]}' var ({len(_to_catisan)} isim) — yeni oturumda çalıştır")
if _to_g.get("_TO_IMZA") == "tahtaci_oyunu" and _to_g.get("TO_SURUM") not in (None, TO_SURUM):
    _to_log.warning("tahtaci_oyunu v%s bellekteki v%s'in üstüne yükleniyor", TO_SURUM, _to_g.get("TO_SURUM"))
_TO_IMZA = "tahtaci_oyunu"


# ---------------------------------------------------------------- tanım
@dataclass
class TahtaciTanim:
    """Tüm eşikler burada; test ve ölçüm aynı tanımı kullanır."""
    zirve_pencere: int = 20          # çöküş derinliği: son N günün en yükseğinden düşüş
    cokus_min: float = 0.30          # klimaks için en az düşüş (%30)
    klimaks_pencere: int = 20        # klimaks: son N günün en yüksek hacmi ve en düşük dibi aynı gün
    klimaks_clv_min: float = 0.0     # kapanış gün ortasının üstünde (CLV ≥ 0)
    hacim_taban_gun: int = 60        # "normal hacim" = klimaks öncesi N günün medyanı
    maliyet_hacim_kat: float = 1.5   # tahtacı maliyeti: normalin ≥1.5 katı hacimli günlerin VWAP'ı
    dagitim_hacim_kat: float = 2.0   # dağıtım günü: normalin ≥2 katı hacim
    dagitim_fitil_min: float = 0.40  # ve üst fitil ≥ aralığın %40'ı (ya da kapanış gün ortasının altında)
    sessiz_hacim_kat: float = 0.60   # sessiz geri çekilme: son 3 gün hacmi, dağıtım günü hacminin <%60'ı
    sessiz_gun: int = 3
    geri_cekilme_payi: float = 0.50  # geri alım bölgesi: maliyet .. maliyet + %50×(dağıtım tepesi − maliyet)
    oyun_omru: int = 40              # klimakstan sonra en çok N gün izlenir
    teyit_gun: int = 5               # teyit: klimakstan sonraki N gün içinde kapanış > klimaks yükseği (dip kırılmadan)
    ufuklar: Tuple[int, ...] = (5, 10, 20)
    min_fiyat: float = 1.0
    min_hacim_tl: float = 2_000_000  # klimaks öncesi 60 gün medyan ciro (TL) alt sınırı
    maliyet: float = 0.005           # tek yön işlem maliyeti (ölçümde iki yön düşülür)


# ---------------------------------------------------------------- veri
def to_veri_ac(VERI: Any) -> Any:
    if isinstance(VERI, dict) and isinstance(VERI.get("veri"), dict):
        return VERI["veri"]
    return VERI


def _to_norm(s: str) -> str:
    s = str(s).upper().strip()
    for ek in (".IS", ".AM"):
        if s.endswith(ek):
            s = s[: -len(ek)]
    return s


def to_ohlcv(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Herhangi bir OHLCV tablosunu O,H,L,C,V sütunlu, tz'siz, artan tarihli tabloya çevirir."""
    if df is None or not len(df):
        return None
    kol = {str(c).lower(): c for c in df.columns}
    ad = {k: kol.get(uzun, kol.get(k)) for k, uzun in (("o", "open"), ("h", "high"), ("l", "low"), ("c", "close"), ("v", "volume"))}
    if any(v is None for v in ad.values()):
        return None
    out = pd.DataFrame({k.upper(): pd.to_numeric(df[v], errors="coerce") for k, v in ad.items()})
    ix = pd.to_datetime(out.index)
    ix = ix.tz_localize(None) if getattr(ix, "tz", None) is not None else ix
    out.index = ix.normalize()
    out = out[~out.index.duplicated(keep="last")].sort_index()
    out = out[(out["C"] > 0) & (out["H"] >= out["L"])]
    return out if len(out) else None


def to_evren(VERI: Any) -> Dict[str, pd.DataFrame]:
    V = to_veri_ac(VERI)
    if not isinstance(V, dict):
        raise RuntimeError("veri sözlük değil: {sembol: OHLCV} bekleniyor")
    E: Dict[str, pd.DataFrame] = {}
    for k, df in V.items():
        try:
            o = to_ohlcv(df)
            if o is not None:
                E[_to_norm(k)] = o
        except Exception as e:
            _to_log.debug("%s atlandı: %s", k, e)
    if not E:
        raise RuntimeError("okunabilir OHLCV yok (Open/High/Low/Close/Volume sütunları gerekli)")
    return E


# ---------------------------------------------------------------- temel (defter, nakit)
def to_temel_oku(K: str, semboller: List[str], indir: Any = None, parti: int = 50) -> pd.DataFrame:
    """Önce {K}/tahtaci_temel.csv; yoksa yfinance .info'dan çeker, {K}/tahtaci_temel.pkl'e kaldığı yerden yazar.
    Sütunlar: defter_hisse (TL), net_nakit (TL), hisse_sayisi, kaynak. Bulunamayan NaN kalır — uydurulmaz."""
    csv = os.path.join(K, "tahtaci_temel.csv")
    if os.path.exists(csv):
        T = pd.read_csv(csv)
        T["sembol"] = T["sembol"].map(_to_norm)
        T = T.set_index("sembol")
        for c in ("defter_hisse", "net_nakit", "hisse_sayisi"):
            if c not in T:
                T[c] = np.nan
        T["kaynak"] = "csv"
        _to_log.info("temel: csv'den %d sembol", len(T))
        return T[["defter_hisse", "net_nakit", "hisse_sayisi", "kaynak"]]
    yol = os.path.join(K, "tahtaci_temel.pkl")
    D: Dict[str, Any] = {}
    if os.path.exists(yol):
        try:
            D = pickle.load(open(yol, "rb"))
        except Exception as e:
            _to_log.warning("temel önbelleği okunamadı (%s) — baştan", e)
    satir: Dict[str, Dict[str, Any]] = D.get("satir", {})
    kalan = [s for s in dict.fromkeys(semboller) if s not in satir]
    indir = indir or _to_yf_temel
    if kalan:
        _to_log.info("temel indiriliyor: %d kaldı (%d hazır)", len(kalan), len(satir))
    for i in range(0, len(kalan), parti):
        for s in kalan[i:i + parti]:
            try:
                satir[s] = indir(s)
            except Exception as e:
                satir[s] = {"defter_hisse": np.nan, "net_nakit": np.nan, "hisse_sayisi": np.nan, "kaynak": f"hata:{str(e)[:40]}"}
        D = {"surum": TO_SURUM, "oturum": str(pd.Timestamp.now()), "satir": satir}
        pickle.dump(D, open(yol, "wb"))
    T = pd.DataFrame.from_dict(satir, orient="index")
    for c in ("defter_hisse", "net_nakit", "hisse_sayisi", "kaynak"):
        if c not in T:
            T[c] = np.nan
    return T[["defter_hisse", "net_nakit", "hisse_sayisi", "kaynak"]]


def to_temel_donem(K: str) -> Optional[pd.DataFrame]:
    """{K}/temel_duz.csv → sembol, aciklama, ozkaynak, net_borc (uzun tablo, açıklama tarihine göre sıralı). Yoksa None."""
    yol = os.path.join(K, "temel_duz.csv")
    if not os.path.exists(yol):
        return None
    t = pd.read_csv(yol, parse_dates=["aciklama"])
    gerek = {"sembol", "aciklama", "ozkaynak"}
    if not gerek.issubset(t.columns):
        _to_log.warning("temel_duz.csv beklenen sütunlar yok (%s) — dönem bazlı temel kullanılmadı", gerek - set(t.columns)); return None
    t["sembol"] = t["sembol"].map(_to_norm)
    if "net_borc" not in t:
        t["net_borc"] = pd.to_numeric(t.get("fin_borc"), errors="coerce") - pd.to_numeric(t.get("nakit"), errors="coerce")
    t = t[["sembol", "aciklama", "ozkaynak", "net_borc"]].dropna(subset=["aciklama"]).sort_values(["sembol", "aciklama"])
    _to_log.info("temel: dönem bazlı %d satır, %d hisse (temel_duz.csv)", len(t), t["sembol"].nunique())
    return t.reset_index(drop=True)


def to_temel_o_gun(td: pd.DataFrame, s: str, tarih: pd.Timestamp) -> Tuple[float, float]:
    """Olay gününde bilinen son bilanço (aciklama ≤ tarih): (ozkaynak, net_borc); yoksa (nan, nan)."""
    g = td[(td["sembol"] == s) & (td["aciklama"] <= tarih)]
    if not len(g):
        return (np.nan, np.nan)
    r = g.iloc[-1]
    return (float(r["ozkaynak"]), float(r["net_borc"]))


def _to_yf_temel(sembol: str) -> Dict[str, Any]:
    import yfinance as yf
    inf = yf.Ticker(sembol + ".IS").info or {}
    nakit = inf.get("totalCash"); borc = inf.get("totalDebt")
    net = (float(nakit) - float(borc or 0)) if nakit is not None else np.nan
    return {"defter_hisse": float(inf["bookValue"]) if inf.get("bookValue") else np.nan,
            "net_nakit": net,
            "hisse_sayisi": float(inf["sharesOutstanding"]) if inf.get("sharesOutstanding") else np.nan,
            "kaynak": "yfinance_bugun"}


# ---------------------------------------------------------------- günlük metrikler (nedensel)
def to_metrikler(df: pd.DataFrame, T: TahtaciTanim = TahtaciTanim()) -> pd.DataFrame:
    """Her gün için yalnız o güne kadar bilinen veriyle hesaplanan sütunlar. Ham OHLCV ya da O,H,L,C,V kabul eder."""
    M = to_ohlcv(df)
    if M is None:
        raise ValueError("OHLCV okunamadı")
    arl = (M["H"] - M["L"]).replace(0, np.nan)
    M["clv"] = ((M["C"] - M["L"]) - (M["H"] - M["C"])) / arl               # −1..+1
    M["ust_fitil"] = (M["H"] - M[["O", "C"]].max(axis=1)) / arl
    M["zirve"] = M["H"].rolling(T.zirve_pencere, min_periods=5).max().shift(1)
    M["cokus"] = 1 - M["L"] / M["zirve"]                                    # zirveden dibe düşüş
    M["hacim_normal"] = M["V"].rolling(T.hacim_taban_gun, min_periods=20).median().shift(1)
    M["ciro_normal"] = (M["V"] * M["C"]).rolling(T.hacim_taban_gun, min_periods=20).median().shift(1)
    M["hacim_kat"] = M["V"] / M["hacim_normal"]
    hacim_max = M["V"].rolling(T.klimaks_pencere, min_periods=5).max()
    dip_min = M["L"].rolling(T.klimaks_pencere, min_periods=5).min()
    M["klimaks"] = ((M["V"] >= hacim_max) & (M["L"] <= dip_min) & (M["clv"] >= T.klimaks_clv_min)
                    & (M["cokus"] >= T.cokus_min) & (M["C"] >= T.min_fiyat) & (M["ciro_normal"] >= T.min_hacim_tl))
    M["dagitim_aday"] = ((M["C"] > M["C"].shift(1)) & (M["hacim_kat"] >= T.dagitim_hacim_kat)
                         & ((M["ust_fitil"] >= T.dagitim_fitil_min) | (M["clv"] < 0)))
    return M


def to_oyun(M: pd.DataFrame, k: int, T: TahtaciTanim = TahtaciTanim()) -> Dict[str, Any]:
    """k indeksindeki klimakstan başlayarak oyunu gün gün oynar; fazları ve seviyeleri döner (nedensel)."""
    n = min(len(M), k + 1 + T.oyun_omru)
    dip = float(M["L"].iloc[k]); normal = float(M["hacim_normal"].iloc[k])
    pay = 0.0; tutar = 0.0
    faz: List[str] = []; maliyet: List[float] = []
    dagitim_i: Optional[int] = None; dagitim_h = np.nan; sessiz_i: Optional[int] = None; kirik_i: Optional[int] = None
    teyit_i: Optional[int] = None; k_yuksek = float(M["H"].iloc[k])
    for i in range(k, n):
        r = M.iloc[i]
        if teyit_i is None and kirik_i is None and k < i <= k + T.teyit_gun and r["C"] > k_yuksek and r["L"] > dip:
            teyit_i = i
        if i == k or (r["V"] >= T.maliyet_hacim_kat * normal and dagitim_i is None):
            vw = (r["H"] + r["L"] + r["C"]) / 3.0
            pay += float(r["V"]); tutar += float(r["V"]) * float(vw)
        mal = tutar / pay if pay else np.nan
        maliyet.append(mal)
        if kirik_i is not None:
            faz.append("KIRILDI"); continue
        if r["C"] < dip:
            kirik_i = i; faz.append("KIRILDI"); continue
        if i == k:
            faz.append("KLIMAKS"); continue
        if dagitim_i is None:
            if bool(r["dagitim_aday"]) and r["C"] > mal:
                dagitim_i = i; dagitim_h = float(r["H"]); faz.append("DAGITIM"); continue
            faz.append("TEPKI"); continue
        # dağıtım sonrası
        son = M["V"].iloc[max(dagitim_i + 1, i - T.sessiz_gun + 1): i + 1]
        bolge_ust = mal + T.geri_cekilme_payi * (dagitim_h - mal)
        sessiz = (len(son) >= T.sessiz_gun and son.mean() < T.sessiz_hacim_kat * float(M["V"].iloc[dagitim_i])
                  and mal <= r["C"] <= bolge_ust and r["L"] > dip)
        if sessiz:
            if sessiz_i is None:
                sessiz_i = i
            faz.append("SESSIZ_GERI_CEKILME")
        else:
            faz.append("DAGITIM_SONRASI")
    return {"k": k, "dip": dip, "faz": faz, "maliyet": maliyet, "dagitim_i": dagitim_i, "dagitim_h": dagitim_h,
            "sessiz_i": sessiz_i, "kirik_i": kirik_i, "teyit_i": teyit_i, "son_i": n - 1}


# ---------------------------------------------------------------- olaylar
def _to_getiri(M: pd.DataFrame, i: int, ufuk: int, T: TahtaciTanim) -> float:
    """i günü sinyal → i+1 açılışta giriş, i+1+ufuk kapanışta çıkış; iki yön maliyet düşülür. Veri yoksa NaN."""
    if i + 1 + ufuk >= len(M):
        return np.nan
    giris = float(M["O"].iloc[i + 1]); cikis = float(M["C"].iloc[i + 1 + ufuk])
    if not (giris > 0 and cikis > 0):
        return np.nan
    return (cikis / giris - 1 - 2 * T.maliyet) * 100


def to_olaylar(E: Dict[str, pd.DataFrame], temel: Optional[pd.DataFrame] = None, T: TahtaciTanim = TahtaciTanim(),
               temel_donem: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Tüm evrende klimaks olayları + oyun fazları + ileri getiriler. Oyun sürerken (40 gün) ikinci klimaks alınmaz;
    dip KIRILDI ise oyun bitmiştir, kırılmadan sonraki yeni klimaks yeni olay sayılır (ERSU: 23 Eyl sahte, 30 Eyl gerçek)."""
    satir: List[Dict[str, Any]] = []
    for s, df in E.items():
        M = to_metrikler(df, T)
        idx = np.flatnonzero(M["klimaks"].to_numpy())
        serbest = -1                                   # bu indeksten önceki klimakslar alınmaz
        kirilanlar: List[int] = []                     # kırılmış klimaks indeksleri (sahte klimaks sayımı için)
        for k in idx:
            if k <= serbest:
                continue
            oy = to_oyun(M, int(k), T)
            serbest = oy["kirik_i"] if oy["kirik_i"] is not None else int(k) + T.oyun_omru
            onceki_sahte = sum(1 for j in kirilanlar if k - j <= T.oyun_omru)
            if oy["kirik_i"] is not None:
                kirilanlar.append(int(k))
            r = M.iloc[k]
            kayit: Dict[str, Any] = {"sembol": s, "tarih": M.index[k], "fiyat": float(r["C"]), "dip": oy["dip"], "onceki_sahte": onceki_sahte,
                                     "cokus": float(r["cokus"]), "hacim_kat": float(r["hacim_kat"]), "clv": float(r["clv"]),
                                     "maliyet_son": oy["maliyet"][-1] if oy["maliyet"] else np.nan,
                                     "dagitim_gun": (oy["dagitim_i"] - k) if oy["dagitim_i"] is not None else np.nan,
                                     "dagitim_tepe_pct": (oy["dagitim_h"] / oy["dip"] - 1) * 100 if oy["dagitim_i"] is not None else np.nan,
                                     "sessiz_gun": (oy["sessiz_i"] - k) if oy["sessiz_i"] is not None else np.nan,
                                     "teyit_gun": (oy["teyit_i"] - k) if oy["teyit_i"] is not None else np.nan,
                                     "teyit_sonra_kirildi": (oy["kirik_i"] is not None and oy["teyit_i"] is not None and oy["kirik_i"] > oy["teyit_i"]),
                                     "kirik_gun": (oy["kirik_i"] - k) if oy["kirik_i"] is not None else np.nan,
                                     "tutuldu": oy["kirik_i"] is None and oy["son_i"] - k >= T.oyun_omru}
            for u in T.ufuklar:
                kayit[f"klimaks_r{u}"] = _to_getiri(M, int(k), u, T)
                kayit[f"sessiz_r{u}"] = _to_getiri(M, oy["sessiz_i"], u, T) if oy["sessiz_i"] is not None else np.nan
                kayit[f"teyit_r{u}"] = _to_getiri(M, oy["teyit_i"], u, T) if oy["teyit_i"] is not None else np.nan
            if oy["dagitim_i"] is not None:
                kayit["dagitim_r10"] = _to_getiri(M, oy["dagitim_i"], 10, T)
            if temel is not None and s in temel.index:
                t = temel.loc[s]
                dh = float(t.get("defter_hisse", np.nan)); nn = float(t.get("net_nakit", np.nan)); hs = float(t.get("hisse_sayisi", np.nan))
                kayit["temel_kaynak"] = str(t.get("kaynak", ""))
                if temel_donem is not None and hs and hs > 0:
                    oz, nb = to_temel_o_gun(temel_donem, s, M.index[k])
                    if not math.isnan(oz):
                        dh = oz / hs; nn = -nb if not math.isnan(nb) else np.nan; kayit["temel_kaynak"] = "donem"
                kayit["pd_dd"] = float(r["C"]) / dh if dh and dh > 0 else np.nan
                kayit["dd_mesafe_pct"] = (dh / float(r["C"]) - 1) * 100 if dh and dh > 0 else np.nan
                kayit["nakit_pd"] = nn / (hs * float(r["C"])) if hs and hs > 0 and not math.isnan(nn) else np.nan
            satir.append(kayit)
    O = pd.DataFrame(satir)
    if len(O):
        O = O.sort_values(["tarih", "sembol"]).reset_index(drop=True)
    return O


# ---------------------------------------------------------------- ölçüm
def _to_band(x: pd.Series, y: Optional[pd.Series] = None, n: int = 2000, seed: int = 7) -> Tuple[float, float, float]:
    """Ortalama (ya da iki grubun farkı) ve %95 bootstrap bandı."""
    rng = np.random.default_rng(seed)
    a = x.dropna().to_numpy(float)
    if y is None:
        if len(a) < 5:
            return (np.nan, np.nan, np.nan)
        b = np.array([a[rng.integers(0, len(a), len(a))].mean() for _ in range(n)])
        return (float(a.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5)))
    c = y.dropna().to_numpy(float)
    if len(a) < 5 or len(c) < 5:
        return (np.nan, np.nan, np.nan)
    b = np.array([a[rng.integers(0, len(a), len(a))].mean() - c[rng.integers(0, len(c), len(c))].mean() for _ in range(n)])
    return (float(a.mean() - c.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5)))


def to_karne(O: pd.DataFrame, T: TahtaciTanim = TahtaciTanim()) -> Dict[str, Any]:
    """Oyunun her adımı için: n, ortalama getiri, band, iki yarı tutarlılığı; P/D<1 ile ≥1 farkı."""
    R: Dict[str, Any] = {"n_klimaks": int(len(O))}
    if not len(O):
        return R
    orta = O["tarih"].median()
    for ad, kol in (("klimaks", "klimaks_r10"), ("teyit", "teyit_r10"), ("sessiz", "sessiz_r10"), ("dagitim", "dagitim_r10")):
        if kol not in O:
            continue
        x = O[kol]
        m, lo, hi = _to_band(x)
        y1 = x[O["tarih"] <= orta]; y2 = x[O["tarih"] > orta]
        R[ad] = {"n": int(x.notna().sum()), "ort": m, "band": (lo, hi), "pozitif_pay": float((x.dropna() > 0).mean()) if x.notna().any() else np.nan,
                 "yari": (float(y1.mean()) if y1.notna().any() else np.nan, float(y2.mean()) if y2.notna().any() else np.nan)}
    R["tutuldu_pay"] = float(O["tutuldu"].mean())
    if "teyit_gun" in O:
        t = O[O["teyit_gun"].notna()]
        R["teyit_pay"] = float(O["teyit_gun"].notna().mean())
        R["teyit_sonra_kirildi_pay"] = float(t["teyit_sonra_kirildi"].mean()) if len(t) else np.nan
        if "klimaks_r10" in O and len(t) >= 10:
            d, lo, hi = _to_band(t["teyit_r10"], O["klimaks_r10"])
            R["teyit_vs_klimaks"] = {"fark": d, "band": (lo, hi)}
    R["dagitim_pay"] = float(O["dagitim_gun"].notna().mean())
    R["sessiz_pay"] = float(O["sessiz_gun"].notna().mean())
    if "pd_dd" in O and O["pd_dd"].notna().sum() >= 10:
        alt = O[O["pd_dd"] < 1]; ust = O[O["pd_dd"] >= 1]
        for ad, kol in (("klimaks", "klimaks_r10"), ("sessiz", "sessiz_r10")):
            d, lo, hi = _to_band(alt[kol], ust[kol])
            R[f"pd_dd_{ad}"] = {"n_alt": int(alt[kol].notna().sum()), "n_ust": int(ust[kol].notna().sum()), "fark": d, "band": (lo, hi),
                                "tutuldu": (float(alt["tutuldu"].mean()) if len(alt) else np.nan, float(ust["tutuldu"].mean()) if len(ust) else np.nan)}
    if "onceki_sahte" in O and (O["onceki_sahte"] >= 1).sum() >= 10:
        a = O[O["onceki_sahte"] >= 1]; b = O[O["onceki_sahte"] == 0]
        d, lo, hi = _to_band(a["klimaks_r10"], b["klimaks_r10"])
        R["ikinci_klimaks"] = {"n_ikinci": int(a["klimaks_r10"].notna().sum()), "n_ilk": int(b["klimaks_r10"].notna().sum()), "fark": d, "band": (lo, hi),
                               "tutuldu": (float(a["tutuldu"].mean()), float(b["tutuldu"].mean()))}
    if "nakit_pd" in O and O["nakit_pd"].notna().sum() >= 10:
        a = O[O["nakit_pd"] > 0]; b = O[O["nakit_pd"] <= 0]
        d, lo, hi = _to_band(a["klimaks_r10"], b["klimaks_r10"])
        R["nakit_klimaks"] = {"n_nakit": int(a["klimaks_r10"].notna().sum()), "n_borc": int(b["klimaks_r10"].notna().sum()), "fark": d, "band": (lo, hi)}
    return R


def to_hukum(R: Dict[str, Any]) -> str:
    """Tek cümle: iz var mı. Şart: band sıfırı dışlar VE iki yarı aynı yönde."""
    if not R.get("n_klimaks"):
        return "VERİ YOK"
    par = []
    for ad in ("klimaks", "teyit", "sessiz"):
        r = R.get(ad)
        if not r or r["n"] < 30:
            par.append(f"{ad}: az örnek (n={r['n'] if r else 0})"); continue
        lo, hi = r["band"]; y1, y2 = r["yari"]
        iz = lo > 0 and y1 > 0 and y2 > 0
        par.append(f"{ad}: {'İZ' if iz else 'GEÇMEDİ'} (n={r['n']}, ort {r['ort']:+.1f} [{lo:+.1f},{hi:+.1f}], yarılar {y1:+.1f}/{y2:+.1f})")
    p = R.get("pd_dd_klimaks")
    if p:
        lo, hi = p["band"]
        par.append(f"defter altı − üstü (klimaks r10): {p['fark']:+.1f} [{lo:+.1f},{hi:+.1f}] → {'İZ' if lo > 0 else 'GEÇMEDİ' if hi < 0 else 'BELİRSİZ'}")
    return " | ".join(par)


def to_rapor(O: pd.DataFrame, R: Dict[str, Any], temel_kaynak: str = "") -> str:
    s = [f"TAHTACI OYUNU v{TO_SURUM} — klimaks olayı: {R.get('n_klimaks', 0)}"]
    if R.get("n_klimaks"):
        s.append(f"dönem {O['tarih'].min().date()} → {O['tarih'].max().date()}, hisse {O['sembol'].nunique()}")
        s.append(f"oyun 40 gün tutuldu (dip kırılmadı): %{100 * R['tutuldu_pay']:.0f} | dağıtım günü görüldü: %{100 * R['dagitim_pay']:.0f} | sessiz geri çekilme görüldü: %{100 * R['sessiz_pay']:.0f}")
        if "teyit_pay" in R:
            tv = R.get("teyit_vs_klimaks")
            s.append(f"teyit geldi: %{100 * R['teyit_pay']:.0f} | teyitten sonra dip kırıldı: %{100 * R['teyit_sonra_kirildi_pay']:.0f}"
                     + (f" | teyit − klimaks r10: {tv['fark']:+.2f} [{tv['band'][0]:+.2f},{tv['band'][1]:+.2f}]" if tv else ""))
        for ad in ("klimaks", "teyit", "sessiz", "dagitim"):
            r = R.get(ad)
            if r:
                s.append(f"{ad:>8} r10: n={r['n']} ort {r['ort']:+.2f} band [{r['band'][0]:+.2f},{r['band'][1]:+.2f}] pozitif %{100 * r['pozitif_pay']:.0f} yarılar {r['yari'][0]:+.2f}/{r['yari'][1]:+.2f}")
        for ad in ("pd_dd_klimaks", "pd_dd_sessiz"):
            p = R.get(ad)
            if p:
                s.append(f"{ad}: defter altı n={p['n_alt']} / üstü n={p['n_ust']} fark {p['fark']:+.2f} [{p['band'][0]:+.2f},{p['band'][1]:+.2f}] tutuldu {100 * p['tutuldu'][0]:.0f}%/{100 * p['tutuldu'][1]:.0f}%")
        ik = R.get("ikinci_klimaks")
        if ik:
            s.append(f"kırılma sonrası ikinci klimaks − ilk klimaks (r10): fark {ik['fark']:+.2f} [{ik['band'][0]:+.2f},{ik['band'][1]:+.2f}] n={ik['n_ikinci']}/{ik['n_ilk']} tutuldu {100 * ik['tutuldu'][0]:.0f}%/{100 * ik['tutuldu'][1]:.0f}%")
        nk = R.get("nakit_klimaks")
        if nk:
            s.append(f"net nakit>0 − borçlu (klimaks r10): fark {nk['fark']:+.2f} [{nk['band'][0]:+.2f},{nk['band'][1]:+.2f}] n={nk['n_nakit']}/{nk['n_borc']}")
        s.append("HÜKÜM: " + to_hukum(R))
        if temel_kaynak == "donem":
            n_d = int((O["temel_kaynak"] == "donem").sum()) if "temel_kaynak" in O else 0
            s.append(f"temel: dönem bazlı (olay gününde bilinen son bilanço) {n_d}/{len(O)} olayda; kalanı bugünkü yfinance değeri (2022 öncesi)")
        elif "yfinance" in temel_kaynak:
            s.append("UYARI: defter/nakit BUGÜNKÜ değerle geçmişe uygulandı (geleceği bilme payı var); temel_duz.csv varsa dönem bazlı kullanılır.")
    return "\n".join(s)


# ---------------------------------------------------------------- giriş noktaları
def tahtaci_olc(K: str, T: TahtaciTanim = TahtaciTanim(), veri_ad: str = "veri_1d_turkey.pkl", temel: bool = True) -> Dict[str, Any]:
    t0 = time.monotonic()
    yol = os.path.join(K, veri_ad)
    if not os.path.exists(yol):
        raise FileNotFoundError(f"veri yok: {yol}")
    E = to_evren(pickle.load(open(yol, "rb")))
    _to_log.info("evren: %d hisse", len(E))
    Tm = to_temel_oku(K, sorted(E)) if temel else None
    Td = to_temel_donem(K) if temel else None
    O = to_olaylar(E, Tm, T, Td)
    kaynak = "donem" if (len(O) and "temel_kaynak" in O and (O["temel_kaynak"] == "donem").mean() > 0.5) else (str(Tm["kaynak"].iloc[0]) if Tm is not None and len(Tm) else "")
    R = to_karne(O, T)
    O.to_csv(os.path.join(K, "tahtaci_olaylar.csv"), index=False)
    rapor = to_rapor(O, R, kaynak)
    open(os.path.join(K, "tahtaci_rapor.txt"), "w", encoding="utf-8").write(rapor)
    print(rapor)
    _to_log.info("bitti %.0fs → tahtaci_olaylar.csv, tahtaci_rapor.txt", time.monotonic() - t0)
    return {"olaylar": O, "karne": R, "rapor": rapor}


def tahtaci_bugun(K: str, T: TahtaciTanim = TahtaciTanim(), veri_ad: str = "veri_1d_turkey.pkl", gun: int = 40) -> pd.DataFrame:
    """Son `gun` içinde klimaks vermiş hisseler: bugünkü faz, tahtacı maliyeti, dağıtım tepesi, geri alım bölgesi, kırılma seviyesi."""
    E = to_evren(pickle.load(open(os.path.join(K, veri_ad), "rb")))
    son_tarih = max(df.index[-1] for df in E.values())
    yas = (pd.Timestamp.now().normalize() - son_tarih).days
    if yas > 3:
        _to_log.warning("VERİ BAYAT: son bar %s (%d gün önce) — önce önbelleği güncelle, sonra tekrar çalıştır", son_tarih.date(), yas)
    Tm = to_temel_oku(K, sorted(E))
    satir = []
    for s, df in E.items():
        M = to_metrikler(df, T)
        idx = np.flatnonzero(M["klimaks"].to_numpy())
        idx = [int(k) for k in idx if len(M) - 1 - k <= gun]
        if not idx:
            continue
        k = idx[-1]; oy = to_oyun(M, k, T)
        mal = oy["maliyet"][-1]; r = M.iloc[-1]
        sahte = len(idx) - 1                            # aynı pencerede daha önce kırılmış klimaks sayısı
        dh = float(Tm.loc[s, "defter_hisse"]) if s in Tm.index else np.nan
        bolge_ust = mal + T.geri_cekilme_payi * (oy["dagitim_h"] - mal) if oy["dagitim_i"] is not None else np.nan
        satir.append({"sembol": s, "klimaks": M.index[k].date(), "gun": len(M) - 1 - k, "faz": oy["faz"][-1], "onceki_sahte": sahte,
                      "teyit": M.index[oy["teyit_i"]].date() if oy["teyit_i"] is not None else "", "fiyat": float(r["C"]),
                      "dip_kirilma": oy["dip"], "tahtaci_maliyet": mal, "dagitim_tepe": oy["dagitim_h"],
                      "geri_alim_bolgesi": f"{mal:.2f}–{bolge_ust:.2f}" if not math.isnan(bolge_ust) else "",
                      "hacim_kat": float(r["hacim_kat"]), "pd_dd": float(r["C"]) / dh if dh and dh > 0 else np.nan,
                      "defter_fiyat": dh})
    B = pd.DataFrame(satir)
    if len(B):
        B = B.sort_values(["faz", "gun"]).reset_index(drop=True)
        B.to_csv(os.path.join(K, "tahtaci_bugun.csv"), index=False)
        with pd.option_context("display.width", 200, "display.max_columns", 20):
            print(B.to_string(index=False))
    else:
        print(f"son {gun} günde klimaks veren hisse yok")
    return B
