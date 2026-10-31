"""K56-PBO: K55 ön kaydı §7 "DOĞRULAMA BEKLİYOR adayları için PBO ve Deflated Sharpe (K51 yöntemi)" (ONKAYIT_K56 v1.3-F). Yalnız KEŞİF + İÇ (donem60),
BAĞIMSIZ açılmadan önce, bir kez. Yapı = 64 KEŞİF varyantı; seri = K55 B seçiminin (gün içi sıra >= 0,80 ya da <= 0,20, örtüşmez 60 gün) eşleşmiş net farkının
(r60 − maliyet − eş ortalaması; K55 eslestir, k = 5) t0 ayı ortalaması. Yön: asıl = KEŞİF A işareti (adayın keşfedilen yönü); bilgi = kayıt yönü (K55 B).
PBO = COL_YOLU_ABD.cy_pbo (CSCV, 16 blok), DSR = cy_dsr (IS'te en iyi yapı, N = yapı sayısı). K51 H8 aynen: PBO < 0,5 ve DSR >= 0,95 -> aşırı uyum riski düşük.
"""
from __future__ import annotations

import hashlib
import time
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

from .ortak import donem_kapisi, log

PBO: Dict[str, Any] = {"donemler": ("KESIF", "IC_DOGRULAMA"), "blok": 16, "k_es": 5, "pbo_esik": 0.5, "dsr_esik": 0.95, "ust": 0.8, "alt": 0.2}
_PC: Dict[str, Any] = {}


def _isci(arg) -> Dict[str, Any]:
    from K55.eslestirme import eslestir
    from K55.hucre import _ortusmez, degisken_hesapla
    from K55.hucreler import HUCRELER
    from K55.ortak import OLAY
    hucre, varyant, yon_a, yon_k = arg; P = _PC["P"]; t0 = time.time(); out = {"hucre": hucre, "varyant": varyant, "yon_a": yon_a, "yon_kayit": yon_k}
    p_ = varyant.split("|")[1]; p_ = None if p_ == "tek" else int(p_)
    try:
        x, _ = degisken_hesapla(P, _PC["V"], HUCRELER[hucre], p_, varyant); x = np.asarray(x, float)
    except Exception as ex:
        return {**out, "hata": f"{type(ex).__name__}: {ex}"}
    m = P.likit.to_numpy() & P.r60_tanimli.to_numpy() & np.isfinite(x) & (P.vd.to_numpy() >= 0) & P.donem60.isin(PBO["donemler"]).to_numpy()
    for d in PBO["donemler"]:
        donem_kapisi(d, P.loc[m & (P.donem60.to_numpy() == d), ["tarih", "bitis60"]], 60)
    D = P.loc[m].copy(); D["_x"] = x[m]; q = D.groupby("tarih")._x.rank(pct=True); seriler = {}
    for ad, yon in (("a", yon_a), ("kayit", yon_k)):
        rng = np.random.default_rng(int(hashlib.sha256(f"{hucre}|{varyant}|{ad}|pbo".encode()).hexdigest()[:12], 16))
        sin = _ortusmez((D[q >= PBO["ust"]] if yon > 0 else D[q <= PBO["alt"]]).copy(), OLAY["Y60"][0])
        if not len(sin):
            seriler[ad] = pd.Series(dtype=float); continue
        M = eslestir(D, sin, D, k=PBO["k_es"], rng=rng); X = pd.concat([sin, M], axis=1); X = X[X.kontrol_n > 0]
        fn = (X.r60_ileri - X.mal) - (X.kontrol_r60_ileri - X.kontrol_mal)
        seriler[ad] = fn.groupby(X.tarih.dt.to_period("M").astype(str)).mean()
        out[f"n_{ad}"] = int(len(X)); out[f"ort_{ad}"] = float(fn.mean()) if len(fn) else np.nan
    out["seriler"] = seriler; out["sure_sn"] = round(time.time() - t0, 1)
    return out


def calistir(P: pd.DataFrame, V: Dict[str, pd.DataFrame], K: pd.DataFrame, yon_kayit: Dict[str, int], isci: int = 3) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """K: 125 KEŞİF satırı (hucre, varyant, ufuk, d); varyant başına A yönü = KEŞİF d işareti (varyantın satırlarında çoğunluk). Dönüş: (yapı özeti,
    PBO / DSR tablosu, aylık matrisler)."""
    import multiprocessing as mp
    from K55.ortak import cy
    for d in PBO["donemler"]:
        donem_kapisi(d)
    C = cy(); _PC.clear(); _PC.update({"P": P, "V": V})
    isler = []
    for (h, v), g in K.groupby(["hucre", "varyant"], sort=True):
        ya = int(np.sign(np.sign(g.d).sum()) or np.sign(g.d.iloc[0])); isler.append((h, v, ya, int(yon_kayit.get(h, 1))))
    log.info("PBO: %d yapı, işçi %d", len(isler), isci)
    if isci > 1:
        with mp.get_context("fork").Pool(isci) as hv:
            son = hv.map(_isci, isler, chunksize=1)
    else:
        son = [_isci(a) for a in isler]
    Y = pd.DataFrame([{k: v for k, v in r.items() if k != "seriler"} for r in son]); sonuc, mats = [], {}
    for ad in ("a", "kayit"):
        S = {f"{r['hucre']}|{r['varyant']}": r["seriler"].get(ad) for r in son if r.get("seriler") is not None and r["seriler"].get(ad) is not None and len(r["seriler"][ad])}
        Mx = pd.DataFrame(S).sort_index(); mats[ad] = Mx; Mf = Mx.fillna(0.0).to_numpy(float)     # ay sinyalsiz -> 0 getiri (nakit)
        pb = C.cy_pbo(Mf, PBO["blok"]) if Mf.shape[1] >= 2 else {"pbo": np.nan}
        sr = Mx.mean() / Mx.std(ddof=1); en = sr.idxmax() if len(sr.dropna()) else None
        ds = C.cy_dsr(Mx[en].to_numpy(float), sr.to_numpy(float)) if en is not None else {"dsr": np.nan}
        if en is not None:                                                # bilgi: aylık seri örtüşen 60 günlük getirilerden; otokorelasyon ve etkin T (T / 3) ile DSR
            ser = Mx[en].dropna(); ds["ac1"] = float(ser.autocorr(1)) if len(ser) > 3 else np.nan; ds["ac2"] = float(ser.autocorr(2)) if len(ser) > 4 else np.nan
            ds["dsr_etkinT_bilgi"] = dsr_etkin_T(ser.to_numpy(float), ds.get("sr0", np.nan), oran=3)    # aynı SR ve SR0, T yerine T / 3 (örtüşen 60 günlük getiriler)
        karar = ("aşırı uyum riski düşük" if (pb.get("pbo", np.nan) < PBO["pbo_esik"] and ds.get("dsr", np.nan) >= PBO["dsr_esik"]) else "aşırı uyum riski yüksek") \
            if np.isfinite(pb.get("pbo", np.nan)) and np.isfinite(ds.get("dsr", np.nan)) else "VERİ YETERSİZ"
        sonuc.append({"yon": "A (keşfedilen)" if ad == "a" else "kayıt (K55 B)", "yapi": int(Mf.shape[1]), "ay": int(Mf.shape[0]), **{f"pbo_{k}": v for k, v in pb.items()},
                      "en_iyi_yapi": en, "en_iyi_sr_aylik": float(sr.max()) if len(sr.dropna()) else np.nan, **{f"dsr_{k}": v for k, v in ds.items()}, "karar": karar})
    return Y, pd.DataFrame(sonuc), mats


def dsr_etkin_T(r: np.ndarray, sr0: float, oran: int = 3) -> float:
    """cy_dsr ile aynı formül (Bailey-López de Prado), yalnız gözlem sayısı T yerine etkin T = T / oran (bilgi; karar vermez)."""
    import math
    from scipy.stats import kurtosis, norm, skew
    r = r[np.isfinite(r)]; T = len(r) / oran
    if T < 3 or not np.isfinite(sr0):
        return np.nan
    sr = r.mean() / (r.std(ddof=1) + 1e-12); sk = float(skew(r)); ku = float(kurtosis(r, fisher=False))
    z = (sr - sr0) * math.sqrt(T - 1) / math.sqrt(max(1 - sk * sr + (ku - 1) / 4 * sr ** 2, 1e-12))
    return float(norm.cdf(z))
