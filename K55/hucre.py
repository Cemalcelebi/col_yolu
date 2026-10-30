"""K55 hücre motoru: bir değişkeni (sembol-gün paneli sütunu) üç yöntemle sınar (ONKAYIT_K55 4-7, v1.2: purge / embargo etiketleri, blok bootstrap).
A olay öncesi: olay günlerinde değişken (gün × oynaklık ondalığı içinde z) vs aynı gün olay olmayanlar: Cohen d (ay kümeli + blok aralık), AUC.
B eşleşmiş ileri: gün içi üst (yon = +1) / alt (−1) beşte bir, sembol başına 60 gün örtüşmeyen sinyal; eşleşmiş kontrole göre r60 farkı (ay, blok60,
  hisse × çeyrek aralıkları), net fark, slot portföyü rastgele sağlaması; karar ölçütleri sabit.
C değişim noktası: hisse başına CUSUM; değişimden sonraki h günde olay oranı / taban oranı (lift), yanlış pozitif payı.
Dönem seçimi ufuk bazlıdır: A ve C için olay / satır ufkunun donem{h} etiketi (PURGE / EMBARGO / TANIMSIZ dışarıda), B için donem60.
Faz 0'da bu motor yalnız iskele olarak (D01-S01, olumlu / olumsuz kontrol) koşar; sonuç optimize edilmez.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from .eslestirme import eslestir
from .istatistik import auc, boot_kume, boot_p, cusum, d_boot_ay, slot_portfoy
from .ortak import A_AUC_ESIK, A_D_ESIK, B_FARK_ESIK, BOOT, C_LIFT_ESIK, CUSUM_H, N_MIN, OLAY, log


def degisken_ekle(P: pd.DataFrame, V: Dict[str, pd.DataFrame], fonk: Callable[[pd.DataFrame], pd.Series], ad: str) -> pd.Series:
    """Değişkeni sembol başına seriden hesaplar (fonk: OHLCV -> Series, yalnız geçmişe bakar) ve panele hizalar (sembol, i)."""
    out = np.full(len(P), np.nan, dtype=np.float32); sem = P.sembol.to_numpy(); ii = P.i.to_numpy(); bas = 0; n = len(P)
    while bas < n:
        son = bas
        while son < n and sem[son] == sem[bas]:
            son += 1
        d = V.get(sem[bas])
        if d is not None:
            x = np.asarray(fonk(d), float)
            if len(x) == len(d):
                out[bas:son] = x[ii[bas:son]]
        bas = son
    return pd.Series(out, index=P.index, name=ad)


def _donem_sec(D: pd.DataFrame, donem: Any, kol: str) -> pd.DataFrame:
    """donem: None (hepsi: PURGE / EMBARGO / TANIMSIZ / DISI hariç), tek ad ya da demet; kol = ufuk bazlı dönem sütunu."""
    if donem is None:
        return D[~D[kol].isin(["PURGE", "EMBARGO", "TANIMSIZ", "DISI"])]
    adlar = (donem,) if isinstance(donem, str) else tuple(donem)
    return D[D[kol].isin(adlar)]


def _donem_ad(donem: Any) -> str:
    return "hepsi" if donem is None else (donem if isinstance(donem, str) else "+".join(donem))


def _z_gun_vd(D: pd.DataFrame, x: str, en_az: int = 5) -> np.ndarray:
    """Gün × oynaklık ondalığı içinde z-skor; hücrede en_az satır yoksa yalnız gün içinde z (v1.1); gün içinde de yoksa NaN."""
    g = D.groupby(["tarih", "vd"])[x]; mu = g.transform("mean"); sd = g.transform("std"); n = g.transform("size")
    z = (D[x] - mu) / sd.replace(0, np.nan); z[n < en_az] = np.nan
    g2 = D.groupby("tarih")[x]; mu2 = g2.transform("mean"); sd2 = g2.transform("std"); n2 = g2.transform("size")
    z2 = (D[x] - mu2) / sd2.replace(0, np.nan); z2[n2 < en_az] = np.nan
    return z.fillna(z2).to_numpy(float)


def yontem_A(P: pd.DataFrame, O: pd.DataFrame, x: str, ufuk: str, rng: np.random.Generator, donem: Any = None) -> Dict[str, Any]:
    """Olay öncesi: likit, pencere tanımlı ve purge / embargo dışı satırlar; olay = (sembol, tarih) olay tablosunda (aynı dönem etiketiyle)."""
    h = OLAY[ufuk][0]; kol = f"donem{h}"; D = _donem_sec(P[P.likit & P[x].notna()], donem, kol)
    if not len(D):
        return {"yontem": "A", "ufuk": ufuk, "donem": _donem_ad(donem), "n_olay": 0, "karar": "VERİ YETERSİZ"}
    Ou = _donem_sec(O[O.ufuk == ufuk], donem, "donem"); anahtar = set(zip(Ou.sembol, Ou.tarih))
    olay = np.fromiter(((s, t) in anahtar for s, t in zip(D.sembol, D.tarih)), bool, len(D))
    z = _z_gun_vd(D, x); d, a, b = d_boot_ay(z, olay, D.ay.to_numpy(), BOOT, rng); _, ab, bb = d_boot_ay(z, olay, D.blok60.to_numpy(), BOOT, rng); au = auc(z[olay], z[~olay])
    n1 = int(olay.sum()); xv = D[x].to_numpy(float)
    out = {"yontem": "A", "ufuk": ufuk, "donem": _donem_ad(donem), "n_olay": n1, "n_olmayan": int((~olay).sum()), "d": d, "d_alt": a, "d_ust": b, "d_alt_blok": ab, "d_ust_blok": bb, "auc": au,
           "x_olay_ort": float(np.nanmean(xv[olay])) if n1 else np.nan, "x_olmayan_ort": float(np.nanmean(xv[~olay])) if (~olay).any() else np.nan}
    yil = D.tarih.dt.year.to_numpy(); isaret = {}; zok = np.isfinite(z)
    for y in np.unique(yil):
        m = (yil == y) & zok
        if (m & olay).sum() >= 10 and (m & ~olay).sum() >= 10:
            isaret[int(y)] = float(np.sign(z[m & olay].mean() - z[m & ~olay].mean()))
    out["yil_isaret"] = isaret; out["yil_tekrar"] = int(sum(1 for v in isaret.values() if v == np.sign(d))) if np.isfinite(d) else 0
    out["p"] = float(min(1.0, 2 * min(np.mean(np.r_[a, b] > 0), 1 - np.mean(np.r_[a, b] > 0)) + 1e-9)) if np.isfinite(a) else np.nan   # kaba; FDR için bootstrap p ayrıca
    out["karar"] = "VERİ YETERSİZ" if n1 < N_MIN else ("ETKİ" if (abs(d) >= A_D_ESIK and np.isfinite(a) and (a > 0 or b < 0) and abs(au - 0.5) >= A_AUC_ESIK) else "ETKİ YOK")
    return out


def _ortusmez(S: pd.DataFrame, h: int) -> pd.DataFrame:
    """Sembol başına örtüşmeyen sinyaller (v1.1): i sıralı; önceki alınan sinyalden en az h işlem günü sonra."""
    S = S.sort_values(["sembol", "i"]); sem = S.sembol.to_numpy(); ii = S.i.to_numpy(); al = np.zeros(len(S), dtype=bool); son = -10 ** 9; onceki = None
    for k in range(len(S)):
        if sem[k] != onceki:
            onceki = sem[k]; son = -10 ** 9
        if ii[k] >= son + h:
            al[k] = True; son = ii[k]
    return S[al]


def yontem_B(P: pd.DataFrame, x: str, yon: int, rng: np.random.Generator, donem: Any = None, k: int = 5) -> Dict[str, Any]:
    """Eşleşmiş ileri: sinyal = gün içi beşte bir (yon), örtüşmez; r60_ileri − kontrol; ay / blok60 / hisse × çeyrek aralıkları; net; slot portföyü."""
    D = _donem_sec(P[P.likit & P.r60_tanimli & P[x].notna() & (P.vd >= 0)], donem, "donem60")
    if not len(D):
        return {"yontem": "B", "donem": _donem_ad(donem), "n": 0, "karar": "VERİ YETERSİZ"}
    q = D.groupby("tarih")[x].rank(pct=True); sin = _ortusmez((D[q >= 0.8] if yon > 0 else D[q <= 0.2]).copy(), OLAY["Y60"][0])
    if not len(sin):
        return {"yontem": "B", "donem": _donem_ad(donem), "n": 0, "karar": "VERİ YETERSİZ"}
    M = eslestir(D, sin, D, k=k, rng=rng); X = pd.concat([sin, M], axis=1); X = X[X.kontrol_n > 0]
    if not len(X):
        return {"yontem": "B", "donem": _donem_ad(donem), "n": 0, "eslesmeyen_pay": 1.0, "karar": "VERİ YETERSİZ"}
    f = (X.r60_ileri - X.kontrol_r60_ileri).to_numpy(float); fn = ((X.r60_ileri - X.mal) - (X.kontrol_r60_ileri - X.kontrol_mal)).to_numpy(float)
    ort, a, b = boot_kume(f, X.ay.to_numpy(), BOOT, rng); _, a2, b2 = boot_kume(f, (X.sembol + "|" + X.ceyrek).to_numpy(), BOOT, rng); _, a3, b3 = boot_kume(f, X.blok60.to_numpy(), BOOT, rng)
    ortn, an, bn = boot_kume(fn, X.ay.to_numpy(), BOOT, rng)
    sp = slot_portfoy(X.assign(net=X.r60_ileri - X.mal)[["tarih", "sembol", "vd", "net"]], D.assign(net=D.r60_ileri - D.mal)[["tarih", "sembol", "vd", "net"]], rng)
    out = {"yontem": "B", "donem": _donem_ad(donem), "yon": yon, "n": int(len(X)), "hisse": int(X.sembol.nunique()), "eslesmeyen_pay": float(1 - len(X) / len(sin)),
           "fark": ort, "fark_alt": a, "fark_ust": b, "fark_alt_hisse_ceyrek": a2, "fark_alt_blok": a3, "fark_ust_blok": b3, "net_fark": ortn, "net_fark_alt": an,
           "p": boot_p(f, X.ay.to_numpy(), BOOT, rng), **{f"slot_{k_}": v for k_, v in sp.items()}}
    out["karar"] = "VERİ YETERSİZ" if out["n"] < N_MIN else ("TUTAR" if (ort >= B_FARK_ESIK and a > 0 and a2 > 0 and ortn > 0 and sp["rastgele_yuzdelik"] >= 0.90) else "TUTMAZ")
    return out


def yontem_C(P: pd.DataFrame, V: Dict[str, pd.DataFrame], O: pd.DataFrame, x_fonk: Callable[[pd.DataFrame], pd.Series], ufuk: str = "Y60", donem: Any = None) -> Dict[str, Any]:
    """Değişim noktası: hisse başına CUSUM; değişimden sonraki h günde olay var mı; taban = likit günlerin olay-öncesi-h-gün payı (purge dışı satırlar)."""
    h = OLAY[ufuk][0]; Ou = _donem_sec(O[O.ufuk == ufuk], donem, "donem"); olay_i = {s: g.i.to_numpy() for s, g in Ou.groupby("sembol")}
    L = _donem_sec(P[P.likit], donem, f"donem{h}"); likit_i = {s: g.i.to_numpy() for s, g in L.groupby("sembol")}
    deg_n = 0; deg_olay = 0; taban_n = 0; taban_olay = 0; yon_say = {1: 0, -1: 0}
    for s, li in likit_i.items():
        d = V.get(s)
        if d is None or not len(li):
            continue
        oi = olay_i.get(s, np.array([], dtype=int)); x = np.asarray(x_fonk(d), float)
        if len(x) != len(d):
            continue
        onde = np.array([((oi > i) & (oi <= i + h)).any() for i in li]) if len(oi) else np.zeros(len(li), dtype=bool)
        taban_n += len(li); taban_olay += int(onde.sum()); cp = cusum(x, CUSUM_H); lset = set(li.tolist())
        for i, yon in cp:
            if i not in lset:
                continue
            deg_n += 1; yon_say[int(yon)] += 1; deg_olay += int(((oi > i) & (oi <= i + h)).any()) if len(oi) else 0
    taban = taban_olay / taban_n if taban_n else np.nan; oran = deg_olay / deg_n if deg_n else np.nan; lift = oran / taban if (taban and np.isfinite(oran)) else np.nan
    out = {"yontem": "C", "ufuk": ufuk, "donem": _donem_ad(donem), "n_degisim": deg_n, "degisim_sonrasi_olay_orani": oran, "taban_orani": taban, "lift": lift,
           "yanlis_pozitif_pay": (1 - oran) if np.isfinite(oran) else np.nan, "yon_yukari": yon_say[1], "yon_asagi": yon_say[-1]}
    out["karar"] = "VERİ YETERSİZ" if deg_n < N_MIN else ("ETKİ" if lift >= C_LIFT_ESIK else "ETKİ YOK")
    return out


def hucre_kos(kimlik: str, tanim: Dict[str, Any], P: pd.DataFrame, V: Dict[str, pd.DataFrame], O: pd.DataFrame, rng: np.random.Generator,
              donemler: Tuple[str, ...] = ("KESIF",), ufuklar: Tuple[str, ...] = ("Y60",), yontemler: Tuple[str, ...] = ("A", "B", "C")) -> List[Dict[str, Any]]:
    """Bir hücreyi (tanım: soru, yon, fonk) verilen dönem ve ufuklarda üç yöntemle koşar; satır listesi döner (hepsi kaydedilir)."""
    x = kimlik; rows = []
    if x not in P:
        P[x] = degisken_ekle(P, V, tanim["fonk"], x)
    eksik = float(P.loc[P.likit, x].isna().mean()) if P.likit.any() else 1.0
    for dn in donemler:
        for uf in ufuklar:
            if "A" in yontemler:
                rows.append({"hucre": kimlik, **yontem_A(P, O, x, uf, rng, dn), "eksik_pay": eksik})
            if "C" in yontemler:
                rows.append({"hucre": kimlik, **yontem_C(P, V, O, tanim["fonk"], uf, dn), "eksik_pay": eksik})
        if "B" in yontemler:
            rows.append({"hucre": kimlik, **yontem_B(P, x, int(tanim.get("yon", 1)), rng, dn), "eksik_pay": eksik})
    for r in rows:
        r["soru"] = tanim.get("soru", ""); r["dal"] = kimlik.split("-")[0]; r["varyant"] = f"{r.get('ufuk', 'Y60')}|{r.get('donem')}|{tanim.get('yon', 1)}"
    return rows
