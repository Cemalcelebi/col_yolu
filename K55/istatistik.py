"""K55 istatistik: kümeli bootstrap (ay; hisse × çeyrek), Cohen d, AUC, Holm, BH-FDR, CUSUM değişim noktası, slot portföyü rastgele sağlaması.
Bağımsız, saf numpy / pandas; sentetik testlerle doğrulanır (test_k55.py).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


def boot_kume(x: np.ndarray, kume: np.ndarray, B: int, rng: np.random.Generator, w: Optional[np.ndarray] = None) -> Tuple[float, float, float]:
    """Kümeli bootstrap: kümeler (ör. ay) yerine koyarak örneklenir; ağırlıklı ortalama. Dönüş: ortalama, %2,5, %97,5."""
    x = np.asarray(x, float); ok = np.isfinite(x); x = x[ok]; kume = np.asarray(kume)[ok]; w = (np.ones(len(x)) if w is None else np.asarray(w, float)[ok])
    if not len(x):
        return np.nan, np.nan, np.nan
    k, inv = np.unique(kume, return_inverse=True); K = len(k)
    sx = np.bincount(inv, weights=x * w, minlength=K); sw = np.bincount(inv, weights=w, minlength=K)
    ort = float(sx.sum() / sw.sum())
    if K < 2:
        return ort, np.nan, np.nan
    sec = rng.integers(0, K, size=(B, K)); num = sx[sec].sum(axis=1); den = sw[sec].sum(axis=1)
    bs = num / np.where(den > 0, den, np.nan)
    return ort, float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))


def cohen_d(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, float); b = np.asarray(b, float); a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    s = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return float((a.mean() - b.mean()) / s) if s > 0 else np.nan


def auc(pozitif: np.ndarray, negatif: np.ndarray) -> float:
    """Mann-Whitney AUC: P(pozitif > negatif) + 0,5 P(eşit)."""
    p = np.asarray(pozitif, float); n = np.asarray(negatif, float); p = p[np.isfinite(p)]; n = n[np.isfinite(n)]
    if not len(p) or not len(n):
        return np.nan
    hepsi = np.concatenate([p, n]); r = pd.Series(hepsi).rank().to_numpy()
    return float((r[: len(p)].sum() - len(p) * (len(p) + 1) / 2) / (len(p) * len(n)))


def d_boot_ay(z: np.ndarray, olay: np.ndarray, ay: np.ndarray, B: int, rng: np.random.Generator) -> Tuple[float, float, float]:
    """Cohen d'nin ay kümeli bootstrap aralığı: ay başına (n, toplam, kare toplam) olay / olay dışı; aylar yerine koyarak örneklenir."""
    z = np.asarray(z, float); ok = np.isfinite(z); z = z[ok]; olay = np.asarray(olay, bool)[ok]; ay = np.asarray(ay)[ok]
    if olay.sum() < 2 or (~olay).sum() < 2:
        return np.nan, np.nan, np.nan
    k, inv = np.unique(ay, return_inverse=True); K = len(k)
    def agg(m):
        return (np.bincount(inv[m], minlength=K), np.bincount(inv[m], weights=z[m], minlength=K), np.bincount(inv[m], weights=z[m] ** 2, minlength=K))
    n1, s1, q1 = agg(olay); n0, s0, q0 = agg(~olay)
    def d_hesap(N1, S1, Q1, N0, S0, Q0):
        m1 = S1 / N1; m0 = S0 / N0; v1 = (Q1 - N1 * m1 ** 2) / np.maximum(N1 - 1, 1); v0 = (Q0 - N0 * m0 ** 2) / np.maximum(N0 - 1, 1)
        s = np.sqrt(((N1 - 1) * v1 + (N0 - 1) * v0) / np.maximum(N1 + N0 - 2, 1)); return (m1 - m0) / np.where(s > 0, s, np.nan)
    d = float(d_hesap(n1.sum(), s1.sum(), q1.sum(), n0.sum(), s0.sum(), q0.sum()))
    if K < 2:
        return d, np.nan, np.nan
    sec = rng.integers(0, K, size=(B, K))
    bs = d_hesap(n1[sec].sum(1), s1[sec].sum(1), q1[sec].sum(1), n0[sec].sum(1), s0[sec].sum(1), q0[sec].sum(1))
    return d, float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))


def boot_p(x: np.ndarray, kume: np.ndarray, B: int, rng: np.random.Generator) -> float:
    """Tek yönlü bootstrap p: ortalama > 0 hipotezi için P(bootstrap ortalaması <= 0) (kümeli)."""
    x = np.asarray(x, float); ok = np.isfinite(x); x = x[ok]; kume = np.asarray(kume)[ok]
    if len(x) < 2:
        return np.nan
    k, inv = np.unique(kume, return_inverse=True); K = len(k); sx = np.bincount(inv, weights=x, minlength=K); n = np.bincount(inv, minlength=K)
    if K < 2:
        return np.nan
    sec = rng.integers(0, K, size=(B, K)); bs = sx[sec].sum(1) / n[sec].sum(1)
    return float(max((bs <= 0).mean(), 1.0 / B))


def holm(p: Sequence[float]) -> np.ndarray:
    """Holm düzeltmesi (NaN korunur)."""
    p = np.asarray(p, float); out = np.full(len(p), np.nan); ok = np.isfinite(p); q = p[ok]; m = len(q)
    if not m:
        return out
    sira = np.argsort(q); duz = np.empty(m); cum = 0.0
    for r, j in enumerate(sira):
        cum = max(cum, (m - r) * q[j]); duz[j] = min(1.0, cum)
    out[ok] = duz; return out


def bh_fdr(p: Sequence[float], q: float = 0.10) -> Tuple[np.ndarray, np.ndarray]:
    """Benjamini-Hochberg: düzeltilmiş p (q-değeri) ve q eşiğinde ret bayrağı (NaN korunur)."""
    p = np.asarray(p, float); out = np.full(len(p), np.nan); ret = np.zeros(len(p), dtype=bool); ok = np.isfinite(p); x = p[ok]; m = len(x)
    if not m:
        return out, ret
    sira = np.argsort(x); sx = x[sira]; qv = sx * m / (np.arange(m) + 1); qv = np.minimum.accumulate(qv[::-1])[::-1]; qv = np.minimum(qv, 1.0)
    duz = np.empty(m); duz[sira] = qv; out[ok] = duz; ret[ok] = duz <= q
    return out, ret


def cusum(x: np.ndarray, h: float = 4.0, pencere: int = 250, k: float = 0.5) -> np.ndarray:
    """Değişim noktaları: x'in kayan (pencere) ortalama / sapmasına göre z (bir gün gecikmeli), iki yönlü CUSUM; |S| > h -> değişim, sıfırlanır.
    Dönüş: değişim günlerinin indeksleri (işaret: +i yukarı, −i aşağı değilse ayrı dizi yerine çift dizi: idx, yon)."""
    x = np.asarray(x, float); n = len(x); s = pd.Series(x); mu = s.rolling(pencere, min_periods=pencere // 2).mean().shift(1); sd = s.rolling(pencere, min_periods=pencere // 2).std(ddof=0).shift(1)
    z = ((s - mu) / sd.replace(0, np.nan)).to_numpy(); sp = 0.0; sn = 0.0; out = []
    for i in range(n):
        if not np.isfinite(z[i]):
            sp = sn = 0.0; continue
        sp = max(0.0, sp + z[i] - k); sn = max(0.0, sn - z[i] - k)
        if sp > h:
            out.append((i, 1)); sp = sn = 0.0
        elif sn > h:
            out.append((i, -1)); sp = sn = 0.0
    return np.array(out, dtype=int).reshape(-1, 2)


def slot_portfoy(sinyal: pd.DataFrame, havuz: pd.DataFrame, rng: np.random.Generator, slot: int = 10, gun_tut: int = 60, gunde: int = 2, R: int = 200) -> Dict[str, float]:
    """Slot portföyü: sinyaller tarih sırasıyla; boş slot varsa (günde en çok 2) alınır, gun_tut gün tutulur (net r60 ile). Rastgele sağlama: alınan her
    sinyal yerine aynı gün aynı (vd) hücresinden rastgele hisse (R kez). Dönüş: portföy ortalama net getiri, rastgele dağılım yüzdeliği.
    sinyal / havuz sütunları: tarih, sembol, vd, net (r60_ileri − mal)."""
    if not len(sinyal):
        return {"n_islem": 0, "ort_net": np.nan, "rastgele_yuzdelik": np.nan, "rastgele_ort": np.nan}
    S = sinyal.sort_values(["tarih", "sembol"]); gunler = np.array(sorted(S.tarih.unique())); gix = {g: i for i, g in enumerate(gunler)}
    dolu: List[int] = []; alinan = []
    for g, grp in S.groupby("tarih", sort=True):
        gi = gix[g]; dolu = [c for c in dolu if c > gi]; bos = slot - len(dolu); k = 0
        for r in grp.itertuples():
            if bos <= 0 or k >= gunde:
                break
            alinan.append((r.tarih, r.sembol, int(r.vd), float(r.net))); dolu.append(gi + gun_tut); bos -= 1; k += 1
    if not alinan:
        return {"n_islem": 0, "ort_net": np.nan, "rastgele_yuzdelik": np.nan, "rastgele_ort": np.nan}
    A = pd.DataFrame(alinan, columns=["tarih", "sembol", "vd", "net"]); ort = float(A.net.mean())
    H = havuz[["tarih", "vd", "net", "sembol"]].dropna(subset=["net"]); grp = {k_: v.net.to_numpy(float) for k_, v in H.groupby(["tarih", "vd"])}
    rast = np.empty(R)
    for r_ in range(R):
        top = 0.0; say = 0
        for t in A.itertuples():
            arr = grp.get((t.tarih, t.vd))
            if arr is None or not len(arr):
                continue
            top += arr[rng.integers(0, len(arr))]; say += 1
        rast[r_] = top / say if say else np.nan
    return {"n_islem": int(len(A)), "ort_net": ort, "rastgele_yuzdelik": float(np.nanmean(rast < ort)), "rastgele_ort": float(np.nanmean(rast))}
