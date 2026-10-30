"""K55 olay tanımları (ONKAYIT_K55 bölüm 3; KİLİTLİ): Y60 +%30 / Y120 +%50 / Y250 +%100, giriş = ertesi gün açılışı, getiri = ufuk günü kapanışı.
Olay günü = pencerenin ilk günü (yalnız likit günler); örtüşmez (ilk olay alınır); pencere seri sonunu aşarsa tanımsız.
Ayrıca ileri getiri (seri sonu işlemiyle) ve olay tekillik denetimi.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

from .ortak import OLAY, ALIVE_SINIR


def ileri_getiri(O: np.ndarray, C: np.ndarray, h: int, seri_erken: bool, seri_sonu: str) -> Tuple[np.ndarray, np.ndarray]:
    """Her i için C[i+h] / O[i+1] − 1. Pencere seri sonunu aşıyorsa: seri erken bitmişse seri sonu işlemi (d100 → −1; d0 → son kapanış;
    k51 → son kapanış, son 60 gün getirisi negatifse ek −%30), değilse tanımsız (NaN). Dönüş: (getiri, tanimli: pencere tam)."""
    n = len(C); r = np.full(n, np.nan); tam = np.zeros(n, dtype=bool)
    if n < 2:
        return r, tam
    i = np.arange(n); giris = np.full(n, np.nan); giris[:-1] = O[1:]
    ok = (i + h < n); r[ok] = C[i[ok] + h] / giris[ok] - 1.0; tam[ok] = True
    if seri_erken:
        kalan = (~ok) & (i + 1 < n); son = C[-1]
        if seri_sonu == "d100":
            r[kalan] = -1.0
        else:
            cikis = son
            if seri_sonu == "k51" and (C[-1] / C[max(0, n - 61)] - 1.0) < 0:
                cikis = son * 0.70
            r[kalan] = cikis / giris[kalan] - 1.0
    return r, tam


def _pencere_en_yuksek(C: np.ndarray, O: np.ndarray, h: int) -> np.ndarray:
    """Pencere içindeki en yüksek kapanışla ulaşılan en büyük getiri (bilgi sütunu)."""
    n = len(C); out = np.full(n, np.nan)
    if n < 2:
        return out
    from numpy.lib.stride_tricks import sliding_window_view
    if n - 1 >= h:
        sw = sliding_window_view(C[1:], h)                       # satır i: C[i+1 .. i+h]
        mx = sw.max(axis=1); out[: len(mx)] = mx / O[1 : len(mx) + 1] - 1.0
    return out


def sembol_olaylari(s: str, d: pd.DataFrame, likit: np.ndarray) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """Bir sembolün Y60 / Y120 / Y250 olayları (örtüşmez, yalnız likit günler, tam pencere) ve ufuk başına tanımlı likit gün sayısı."""
    O = d.Open.to_numpy(float); C = d.Close.to_numpy(float); idx = d.index; n = len(d); rows = []; tanimli = {}
    for ad, (h, esik) in OLAY.items():
        r, tam = ileri_getiri(O, C, h, False, "k51"); aday = likit & tam; tanimli[ad] = int(aday.sum())
        enyuk = _pencere_en_yuksek(C, O, h); son = -10 ** 9
        for i in np.flatnonzero(aday & (r >= esik)):
            if i < son + h:                                       # örtüşme: önceki olayın penceresi bitmeden yeni olay yok
                continue
            rows.append({"sembol": s, "tarih": idx[i], "i": int(i), "ufuk": ad, "giris": float(O[i + 1]), "getiri": float(r[i]), "en_yuksek_getiri": float(enyuk[i])}); son = i
    return rows, tanimli


def olaylar(V: Dict[str, pd.DataFrame], likit_map: Dict[str, np.ndarray]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Evren olay tablosu + sembol × ufuk tanımlı likit gün sayısı (taban oranı için)."""
    rows: List[Dict[str, Any]] = []; say = []
    for s, d in V.items():
        lk = likit_map.get(s)
        if lk is None or len(lk) != len(d):
            continue
        r, t = sembol_olaylari(s, d, lk); rows += r; say.append({"sembol": s, **{f"tanimli_{k}": v for k, v in t.items()}})
    kol = ["sembol", "tarih", "i", "ufuk", "giris", "getiri", "en_yuksek_getiri"]
    O = pd.DataFrame(rows, columns=kol) if rows else pd.DataFrame(columns=kol)
    if len(O):
        O["tarih"] = pd.to_datetime(O.tarih); O = O.sort_values(["ufuk", "sembol", "tarih"]).reset_index(drop=True)
    return O, pd.DataFrame(say)


def olay_tekillik_denetimi(O: pd.DataFrame) -> Dict[str, Any]:
    """Aynı olayın birden fazla sayılması: (sembol, ufuk, tarih) yinelemesi ve aynı sembolde örtüşen pencere sayısı (ikisi de 0 olmalı)."""
    out = {"yineleme": 0, "ortusme": 0, "olay": int(len(O))}
    if not len(O):
        return out
    out["yineleme"] = int(O.duplicated(["sembol", "ufuk", "tarih"]).sum())
    ort = 0
    for (s, uf), g in O.groupby(["sembol", "ufuk"]):
        h = OLAY[uf][0]; ii = np.sort(g.i.to_numpy()); ort += int((np.diff(ii) < h).sum()) if len(ii) > 1 else 0
    out["ortusme"] = ort; out["gecti"] = bool(out["yineleme"] == 0 and ort == 0)
    return out
