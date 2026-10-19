# -*- coding: utf-8 -*-
"""
ÖLÇÜM DENETİMİ v1.0 — ölçü aletinin kendisini tartar (tahtaci_oyunu olayları üstünde)
==================================================================================
Soru: "GEÇMEDİ" hükmü aletin hatası olabilir mi? Beş kontrol:
  1. PLASEBO      : aynı hisselerde, olaya ±250 gün yakın RASTGELE günlerin r10'u. Klimaks < plasebo → sinyal zararlı;
                    klimaks ≈ plasebo → sinyal boş; klimaks > plasebo → sinyal bilgi taşıyor (hüküm yanlıştı).
  2. BÖLÜNME      : çöküş tek günde mi oluşmuş (BIST'te tek günde ≥%30 ancak işlem durdurma sonrası açılış ya da düzeltilmemiş
                    bölünme olabilir; liste raporda, grafikte kontrol edilir). Veri temettü-düzeltili mi (yfinance ile 20 hisse)?
                    Not: Yahoo ham fiyatı bölünme/bedelsiz için zaten düzeltilmiştir; auto_adjust yalnız temettüyü ekler.
  3. HAYATTA KALMA: veride son barı eski olan (borsadan çıkmış / durmuş) hisse sayısı; yön: çıkanlar yoksa dip alımı OLDUĞUNDAN İYİ görünür.
  4. GİRİŞ        : ertesi açılış boşluğu; ≥%9 açılanlar (tavan, alınamaz) hariç ve "ertesi kapanıştan giriş" ile r10.
  5. REJİM        : XU100'ün olay günündeki 60 günlük getirisine göre r10 (düşüş rejimi / yükseliş rejimi).
Her kontrol kendi hükmünü yazar; rapor {K}/olcum_denetimi_rapor.txt.

Kullanım (Colab, tahtaci_oyunu.py yüklü ve tahtaci_olaylar.csv üretilmiş olmalı):
    exec(open(K + "/olcum_denetimi.py", encoding="utf-8").read())
    D = olcum_denetimi(K)
"""
from __future__ import annotations

import logging
import os
import pickle
import sys
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

OD_SURUM = "1.1"
_od_log = logging.getLogger("olcum_denetimi")
if not _od_log.handlers:
    _h = logging.StreamHandler(sys.stdout)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s denetim: %(message)s", "%H:%M:%S"))
    _od_log.addHandler(_h)
_od_log.setLevel(logging.INFO)
_od_log.propagate = False

_OD_ISIMLER = ("od_plasebo", "od_bolunme", "od_hayatta_kalma", "od_giris", "od_rejim", "od_rapor", "olcum_denetimi")
_od_g = globals()
if any(k in _od_g for k in _OD_ISIMLER) and _od_g.get("_OD_IMZA") != "olcum_denetimi":
    raise RuntimeError("çakışma kapısı: bellekte başka bir od_* ismi var — yeni oturumda çalıştır")
_OD_IMZA = "olcum_denetimi"
for _ad in ("to_evren", "to_metrikler", "TahtaciTanim"):
    if _ad not in _od_g:
        raise RuntimeError(f"önce tahtaci_oyunu.py yüklenmeli ({_ad} yok)")


def _od_band(x: np.ndarray, y: Optional[np.ndarray] = None, n: int = 2000, seed: int = 11) -> Tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    x = x[~np.isnan(x)]
    if y is None:
        if len(x) < 5:
            return (np.nan, np.nan, np.nan)
        b = np.array([x[rng.integers(0, len(x), len(x))].mean() for _ in range(n)])
        return (float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5)))
    y = y[~np.isnan(y)]
    if len(x) < 5 or len(y) < 5:
        return (np.nan, np.nan, np.nan)
    b = np.array([x[rng.integers(0, len(x), len(x))].mean() - y[rng.integers(0, len(y), len(y))].mean() for _ in range(n)])
    return (float(x.mean() - y.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5)))


def _od_r(M: pd.DataFrame, i: int, ufuk: int, maliyet: float, giris: str = "acilis") -> float:
    """i sinyal günü → giriş i+1 açılış (ya da i+1 kapanış), çıkış i+1+ufuk kapanış, iki yön maliyet."""
    if i + 1 + ufuk >= len(M):
        return np.nan
    g = float(M["O"].iloc[i + 1]) if giris == "acilis" else float(M["C"].iloc[i + 1])
    c = float(M["C"].iloc[i + 1 + ufuk])
    return (c / g - 1 - 2 * maliyet) * 100 if g > 0 and c > 0 else np.nan


# ---------------------------------------------------------------- 1. plasebo
def od_plasebo(E: Dict[str, pd.DataFrame], O: pd.DataFrame, T: Any, n_rastgele: int = 20, pencere: int = 250, seed: int = 3) -> Dict[str, Any]:
    """Her olay için aynı hissede ±pencere gün içinden, klimaks olmayan n_rastgele gün → r10 ortalaması (eşleşmiş plasebo)."""
    rng = np.random.default_rng(seed)
    gercek: List[float] = []; plasebo: List[float] = []; plasebo_tut: List[float] = []
    for s, grup in O.groupby("sembol"):
        if s not in E:
            continue
        M = to_metrikler(E[s], T)
        kl = M["klimaks"].to_numpy()
        for _, r in grup.iterrows():
            k = M.index.get_indexer([pd.Timestamp(r["tarih"])])[0]
            if k < 0:
                continue
            lo, hi = max(T.hacim_taban_gun, k - pencere), min(len(M) - 12, k + pencere)
            aday = [j for j in range(lo, hi) if not kl[j] and abs(j - k) > 2]
            if len(aday) < 5:
                continue
            sec = rng.choice(aday, size=min(n_rastgele, len(aday)), replace=False)
            pr = [_od_r(M, int(j), 10, T.maliyet) for j in sec]
            pr = [x for x in pr if not np.isnan(x)]
            if not pr:
                continue
            gercek.append(float(r["klimaks_r10"])); plasebo.append(float(np.mean(pr)))
            # plasebo "dip tuttu": rastgele günün dibi 40 gün kırılmadı mı
            dips = [float((M["C"].iloc[int(j) + 1: int(j) + 1 + T.oyun_omru] >= M["L"].iloc[int(j)]).all()) for j in sec if int(j) + T.oyun_omru < len(M)]
            if dips:
                plasebo_tut.append(float(np.mean(dips)))
    g = np.array(gercek); p = np.array(plasebo)
    d, lo, hi = _od_band(g, p)
    m_g, _, _ = _od_band(g); m_p, _, _ = _od_band(p)
    hukum = ("sinyal ZARARLI (plasebodan kötü)" if hi < 0 else "sinyal BİLGİ TAŞIYOR (plasebodan iyi) — hüküm yeniden bakılmalı" if lo > 0 else "sinyal BOŞ (plasebodan farksız)")
    return {"n": int(len(g)), "klimaks_r10": m_g, "plasebo_r10": m_p, "fark": d, "band": (lo, hi),
            "plasebo_tutuldu": float(np.mean(plasebo_tut)) if plasebo_tut else np.nan, "hukum": hukum}


# ---------------------------------------------------------------- 2. bölünme
def od_bolunme(E: Dict[str, pd.DataFrame], O: pd.DataFrame, T: Any, yf_ornek: int = 20, indir: Any = None, seed: int = 5) -> Dict[str, Any]:
    """(a) Çöküşün tek günde oluştuğu olaylar (önceki kapanış → klimaks dibi ≥ %30 tek barda): bedelsiz/bölünme şüphesi.
    (b) Önbellek düzeltilmiş mi: yfinance düzeltilmiş ve ham kapanışla 20 hissede karşılaştırma."""
    tek_gun = 0; tek_gun_r10: List[float] = []; diger_r10: List[float] = []; tek_gun_liste: List[str] = []
    for s, grup in O.groupby("sembol"):
        if s not in E:
            continue
        M = E[s]
        for _, r in grup.iterrows():
            k = M.index.get_indexer([pd.Timestamp(r["tarih"])])[0]
            if k <= 0:
                continue
            onceki = float(M["C"].iloc[k - 1]); dip = float(M["L"].iloc[k])
            if onceki > 0 and 1 - dip / onceki >= T.cokus_min:
                tek_gun += 1; tek_gun_r10.append(float(r["klimaks_r10"])); tek_gun_liste.append(f"{s} {pd.Timestamp(r['tarih']).date()} ({onceki:.2f}→{dip:.2f})")
            else:
                diger_r10.append(float(r["klimaks_r10"]))
    sonuc: Dict[str, Any] = {"tek_gun_cokus": tek_gun, "n": int(len(O)), "tek_gun_liste": tek_gun_liste,
                             "tek_gun_r10": float(np.nanmean(tek_gun_r10)) if tek_gun_r10 else np.nan,
                             "diger_r10": float(np.nanmean(diger_r10)) if diger_r10 else np.nan}
    # (b) düzeltme kontrolü
    rng = np.random.default_rng(seed)
    semboller = [s for s in E if len(E[s]) > 100]
    sec = list(rng.choice(semboller, size=min(yf_ornek, len(semboller)), replace=False)) if semboller else []
    indir = indir or _od_yf_ciftt
    duz = 0; ham = 0; belirsiz = 0; hata = 0
    for s in sec:
        try:
            C = E[s]["C"]; bas = C.index[-min(250, len(C) - 50)]
            a, h = indir(s, bas.strftime("%Y-%m-%d"))
            ortak = C.index.intersection(a.index).intersection(h.index)
            if len(ortak) < 50:
                belirsiz += 1; continue
            fa = float(np.nanmedian(np.abs(C.loc[ortak] / a.loc[ortak] - 1))); fh = float(np.nanmedian(np.abs(C.loc[ortak] / h.loc[ortak] - 1)))
            if fa < fh * 0.5:
                duz += 1
            elif fh < fa * 0.5:
                ham += 1
            else:
                belirsiz += 1
        except Exception as e:
            hata += 1; _od_log.debug("%s yf karşılaştırma: %s", s, e)
    sonuc.update({"yf_ornek": len(sec), "duzeltilmis": duz, "ham": ham, "belirsiz": belirsiz, "yf_hata": hata})
    sonuc["hukum"] = (f"tek günlük çöküş {tek_gun}/{len(O)} olay (%{100 * tek_gun / max(1, len(O)):.0f}); "
                      + ("önbellek temettü-düzeltili" if duz > ham else "önbellek temettü-düzeltisiz (BASLAT B1 ile uyumlu; bölünme düzeltmesi Yahoo'da zaten var) — elde tutma getirileri temettü kadar düşük ölçülür" if ham > duz else "düzeltme durumu belirsiz"))
    return sonuc


def _od_yf_ciftt(s: str, bas: str) -> Tuple[pd.Series, pd.Series]:
    import yfinance as yf
    a = yf.download(s + ".IS", start=bas, interval="1d", auto_adjust=True, progress=False)["Close"]
    h = yf.download(s + ".IS", start=bas, interval="1d", auto_adjust=False, progress=False)["Close"]
    if isinstance(a, pd.DataFrame):
        a = a.iloc[:, 0]
    if isinstance(h, pd.DataFrame):
        h = h.iloc[:, 0]
    for x in (a, h):
        x.index = pd.to_datetime(x.index).tz_localize(None).normalize()
    return a, h


# ---------------------------------------------------------------- 3. hayatta kalma
def od_hayatta_kalma(E: Dict[str, pd.DataFrame], O: pd.DataFrame, bayat_gun: int = 30) -> Dict[str, Any]:
    son = max(df.index[-1] for df in E.values())
    eski = {s: df.index[-1] for s, df in E.items() if (son - df.index[-1]).days > bayat_gun}
    olay_eski = int(O["sembol"].isin(eski).sum())
    return {"evren": len(E), "son_bari_eski": len(eski), "olay_eski_hissede": olay_eski,
            "hukum": (f"{len(eski)}/{len(E)} hissenin son barı {bayat_gun}+ gün eski (borsadan çıkmış/durmuş); olayların {olay_eski} tanesi bunlarda. "
                      + ("Çıkan hisse veride YOK gibi: dip alımı gerçekte burada görünenden DAHA KÖTÜ olur (hayatta kalan yanlılığı sinyal lehine)."
                         if len(eski) < 0.03 * len(E) else "Çıkan hisseler kısmen veride; yanlılık sınırlı."))}


# ---------------------------------------------------------------- 4. giriş gerçekçiliği
def od_giris(E: Dict[str, pd.DataFrame], O: pd.DataFrame, T: Any, tavan: float = 0.09) -> Dict[str, Any]:
    bosluk: List[float] = []; r_acilis: List[float] = []; r_kapanis: List[float] = []; r_alinabilir: List[float] = []
    for s, grup in O.groupby("sembol"):
        if s not in E:
            continue
        M = E[s]
        for _, r in grup.iterrows():
            k = M.index.get_indexer([pd.Timestamp(r["tarih"])])[0]
            if k < 0 or k + 1 >= len(M):
                continue
            b = float(M["O"].iloc[k + 1] / M["C"].iloc[k] - 1)
            bosluk.append(b)
            ra = _od_r(M, k, 10, T.maliyet, "acilis"); rk = _od_r(M, k, 10, T.maliyet, "kapanis")
            r_acilis.append(ra); r_kapanis.append(rk)
            if b < tavan:
                r_alinabilir.append(ra)
    b = np.array(bosluk)
    ma, la, ha = _od_band(np.array(r_acilis)); mk, lk, hk = _od_band(np.array(r_kapanis)); mal, lal, hal = _od_band(np.array(r_alinabilir))
    return {"n": int(len(b)), "bosluk_medyan_pct": float(np.median(b) * 100) if len(b) else np.nan,
            "tavan_acilis_pay": float((b >= tavan).mean()) if len(b) else np.nan,
            "r10_acilis": (ma, la, ha), "r10_kapanis": (mk, lk, hk), "r10_alinabilir": (mal, lal, hal),
            "hukum": ("ertesi açılış medyan boşluğu %" + f"{np.median(b) * 100:+.1f}" + f", tavan açılış payı %{100 * (b >= tavan).mean():.0f}; "
                      + ("alınabilir olaylarda da r10 ≤ 0: giriş yöntemi sonucu değiştirmiyor" if hal <= 0 or np.isnan(hal) else "alınabilir olaylarda r10 pozitif: tavan açılışlar sonucu bozuyor — hüküm yeniden bakılmalı")) if len(b) else "veri yok"}


# ---------------------------------------------------------------- 5. rejim
def od_rejim(O: pd.DataFrame, xu100: Optional[pd.Series], T: Any) -> Dict[str, Any]:
    if xu100 is None or not len(xu100):
        return {"hukum": "XU100 indirilemedi — rejim kontrolü yapılamadı"}
    x = xu100.sort_index()
    g60 = x / x.shift(60) - 1
    r = O.copy(); r["tarih"] = pd.to_datetime(r["tarih"])
    r["xu60"] = g60.reindex(r["tarih"], method="ffill").to_numpy()
    dus = r[r["xu60"] < 0]; yuk = r[r["xu60"] >= 0]
    md, ld, hd = _od_band(dus["klimaks_r10"].to_numpy(float)); my, ly, hy = _od_band(yuk["klimaks_r10"].to_numpy(float))
    return {"n_dusus": int(len(dus)), "n_yukselis": int(len(yuk)), "r10_dusus": (md, ld, hd), "r10_yukselis": (my, ly, hy),
            "tutuldu_dusus": float(dus["tutuldu"].mean()) if len(dus) else np.nan, "tutuldu_yukselis": float(yuk["tutuldu"].mean()) if len(yuk) else np.nan,
            "hukum": ("yükseliş rejiminde klimaks r10 pozitif ve band sıfırı dışlıyor: sinyal REJİME BAĞLI, toptan 'geçmedi' eksik hüküm" if ly > 0
                      else "iki rejimde de pozitif değil: rejim ayrımı hükmü değiştirmiyor")}


def _od_xu100(bas: str = "2016-01-01") -> Optional[pd.Series]:
    try:
        import yfinance as yf
        x = yf.download("XU100.IS", start=bas, interval="1d", auto_adjust=True, progress=False)["Close"]
        if isinstance(x, pd.DataFrame):
            x = x.iloc[:, 0]
        x.index = pd.to_datetime(x.index).tz_localize(None).normalize()
        return x.dropna()
    except Exception as e:
        _od_log.warning("XU100 indirilemedi: %s", e)
        return None


# ---------------------------------------------------------------- rapor
def od_rapor(D: Dict[str, Any]) -> str:
    s = [f"ÖLÇÜM DENETİMİ v{OD_SURUM} — tahtaci_oyunu olayları üstünde"]
    p = D["plasebo"]
    s.append(f"1 PLASEBO  n={p['n']} klimaks r10 {p['klimaks_r10']:+.2f} | plasebo r10 {p['plasebo_r10']:+.2f} | fark {p['fark']:+.2f} [{p['band'][0]:+.2f},{p['band'][1]:+.2f}] | plasebo dip tuttu %{100 * p['plasebo_tutuldu']:.0f} → {p['hukum']}")
    b = D["bolunme"]
    s.append(f"2 BÖLÜNME  tek günlük çöküş {b['tek_gun_cokus']}/{b['n']} (r10 {b['tek_gun_r10']:+.2f} / diğer {b['diger_r10']:+.2f}) | yf örnek {b['yf_ornek']}: düzeltilmiş {b['duzeltilmis']}, ham {b['ham']}, belirsiz {b['belirsiz']}, hata {b['yf_hata']} → {b['hukum']}")
    if b.get("tek_gun_liste"):
        s.append("   tek günlük çöküş listesi (grafikte kontrol): " + "; ".join(b["tek_gun_liste"]))
    h = D["hayatta"]
    s.append(f"3 HAYATTA KALMA  → {h['hukum']}")
    g = D["giris"]
    if g["n"]:
        s.append(f"4 GİRİŞ  n={g['n']} r10 açılış {g['r10_acilis'][0]:+.2f} [{g['r10_acilis'][1]:+.2f},{g['r10_acilis'][2]:+.2f}] | ertesi kapanıştan {g['r10_kapanis'][0]:+.2f} | tavan hariç {g['r10_alinabilir'][0]:+.2f} [{g['r10_alinabilir'][1]:+.2f},{g['r10_alinabilir'][2]:+.2f}] → {g['hukum']}")
    r = D["rejim"]
    if "n_dusus" in r:
        s.append(f"5 REJİM  düşüş n={r['n_dusus']} r10 {r['r10_dusus'][0]:+.2f} [{r['r10_dusus'][1]:+.2f},{r['r10_dusus'][2]:+.2f}] tuttu %{100 * r['tutuldu_dusus']:.0f} | yükseliş n={r['n_yukselis']} r10 {r['r10_yukselis'][0]:+.2f} [{r['r10_yukselis'][1]:+.2f},{r['r10_yukselis'][2]:+.2f}] tuttu %{100 * r['tutuldu_yukselis']:.0f} → {r['hukum']}")
    else:
        s.append("5 REJİM  → " + r["hukum"])
    return "\n".join(s)


def olcum_denetimi(K: str, veri_ad: str = "veri_1d_turkey.pkl", olay_ad: str = "tahtaci_olaylar.csv", T: Any = None, xu100: Any = "indir") -> Dict[str, Any]:
    T = T or TahtaciTanim()
    E = to_evren(pickle.load(open(os.path.join(K, veri_ad), "rb")))
    O = pd.read_csv(os.path.join(K, olay_ad), parse_dates=["tarih"])
    _od_log.info("evren %d hisse, olay %d", len(E), len(O))
    D = {"plasebo": od_plasebo(E, O, T), "bolunme": od_bolunme(E, O, T), "hayatta": od_hayatta_kalma(E, O),
         "giris": od_giris(E, O, T), "rejim": od_rejim(O, _od_xu100() if isinstance(xu100, str) else xu100, T)}
    rapor = od_rapor(D)
    open(os.path.join(K, "olcum_denetimi_rapor.txt"), "w", encoding="utf-8").write(rapor)
    print(rapor)
    D["rapor"] = rapor
    return D
