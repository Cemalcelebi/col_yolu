"""K55 eşleşmiş kontrol (ONKAYIT_K55 bölüm 5): aynı gün (± gun_tol işlem günü), aynı oynaklık ondalığı (vd), aynı likidite üçlüsü (lt), aynı rejim,
aynı trend işareti, |dd250 farkı| <= DD_TOL, sektör biliniyorsa aynı sektör, hisse farklı; en yakın k (standartlaştırılmış dd250, vol60, log_dv20, r60, ar20).
Yalnız sinyal gününe kadar bilinen özellikler kullanılır (hepsi geriye bakar). K51 v1.2 mantığının yeniden yazımı; sentetik testle doğrulanır.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

from .ortak import DD_TOL, GUN_TOL, K_ES

UZAK = ("dd250", "vol60", "log_dv20", "r60", "ar20")


def eslestir(P: pd.DataFrame, olay: pd.DataFrame, havuz: pd.DataFrame, k: int = K_ES, gun_tol: int = GUN_TOL, deger: str = "r60_ileri",
             rng: np.random.Generator = None) -> pd.DataFrame:
    """olay satırlarına (index korunur) kontrol_n, kontrol_<deger>, kontrol_mal, kontrol_kimlik ekler. P: standartlaştırma için (likit satırlar).
    havuz: aday kontrol satırları (likit, deger tanımlı)."""
    sd = P[list(UZAK)].astype(float).std().fillna(1.0).replace(0, 1.0).to_numpy(float)
    gunler = np.array(sorted(pd.unique(pd.concat([havuz.tarih, olay.tarih])))); gix = {g: i for i, g in enumerate(gunler)}
    hv = havuz.sort_values("tarih"); hg = hv.tarih.map(gix).to_numpy(); hx = hv[list(UZAK)].to_numpy(float); hvd = hv["vd"].to_numpy(); hlt = hv["lt"].to_numpy()
    htr = hv.trend.to_numpy(); hsk = hv.sektor.to_numpy(); hsm = hv.sembol.to_numpy(); hrj = hv.rejim.to_numpy()
    hy = hv[deger].to_numpy(float); hm = hv.mal.to_numpy(float) if "mal" in hv else np.zeros(len(hv)); hid = hv.index.to_numpy(); out = []
    for r in olay.itertuples():
        g = gix.get(r.tarih)
        if g is None:
            out.append((0, np.nan, np.nan, "")); continue
        a, b = np.searchsorted(hg, g - gun_tol), np.searchsorted(hg, g + gun_tol, side="right")
        m = (hvd[a:b] == r.vd) & (hlt[a:b] == r.lt) & (htr[a:b] == r.trend) & (hrj[a:b] == r.rejim) & (np.abs(hx[a:b, 0] - r.dd250) <= DD_TOL) & (hsm[a:b] != r.sembol)
        if isinstance(r.sektor, str) and r.sektor != "bilinmiyor":
            m &= hsk[a:b] == r.sektor
        cand = np.flatnonzero(m)
        if not len(cand):
            out.append((0, np.nan, np.nan, "")); continue
        x = hx[a:b][cand]; e = np.array([getattr(r, u) for u in UZAK], float)
        dist = np.sqrt(np.nansum(((x - e) / sd) ** 2, axis=1)); sec = cand[np.argsort(dist, kind="stable")[:k]]
        out.append((len(sec), float(np.nanmean(hy[a:b][sec])), float(np.nanmean(hm[a:b][sec])), ";".join(f"{hsm[a:b][j]}@{int(hid[a:b][j])}" for j in sec)))
    return pd.DataFrame(out, columns=["kontrol_n", f"kontrol_{deger}", "kontrol_mal", "kontrol_kimlik"], index=olay.index)
