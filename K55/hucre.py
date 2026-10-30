"""K55 hücre motoru (Faz 1 sürümü): bir hücrenin bütün varyantlarını (pencereler) üç yöntemle sınar (ONKAYIT_K55 4-7, v1.2 purge / embargo, blok bootstrap).
A olay öncesi: olay günlerinde değişken (gün × oynaklık ondalığı içinde z) vs aynı gün olay olmayanlar: Cohen d (ay kümeli + blok aralık, bootstrap p), AUC,
  yıl yıl işaret tekrarı, rejim (BOĞA / AYI) işaret tutarlılığı.
B eşleşmiş ileri: gün içi üst (yon = +1) / alt (−1) beşte bir, sembol başına 60 gün örtüşmeyen sinyal; eşleşmiş kontrole göre r60 farkı (ay, blok60,
  hisse × çeyrek aralıkları, bootstrap p), net fark, slot portföyü rastgele sağlaması.
C değişim noktası: hisse başına CUSUM bir kez; her ufuk için değişimden sonraki h günde olay oranı / taban oranı (lift), yanlış pozitif payı.
Dönem seçimi ufuk bazlıdır (donem{h}; PURGE / EMBARGO / TANIMSIZ dışarıda); B için donem60. Varyant sütunu: '<kimlik>|<pencere>'.
"""
from __future__ import annotations

import zlib
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from .eslestirme import eslestir
from .istatistik import auc, boot_kume, boot_p, cusum, d_boot_ay, slot_portfoy
from .ortak import A_AUC_ESIK, A_D_ESIK, B_FARK_ESIK, BOOT, C_LIFT_ESIK, CUSUM_H, N_MIN, OLAY, log


def hucre_rng(kimlik: str, tohum: int) -> np.random.Generator:
    return np.random.default_rng(tohum + zlib.crc32(kimlik.encode()) % 1_000_000)


def degisken_ekle(P: pd.DataFrame, V: Dict[str, pd.DataFrame], fonk: Callable[[pd.DataFrame], pd.Series], ad: str) -> pd.Series:
    """Değişkeni sembol başına seriden hesaplar (fonk: OHLCV -> Series, yalnız geçmişe bakar) ve panele hizalar (sembol, i)."""
    out = np.full(len(P), np.nan, dtype=np.float32); sem = P.sembol.to_numpy(); ii = P.i.to_numpy(); bas = 0; n = len(P)
    while bas < n:
        son = bas
        while son < n and sem[son] == sem[bas]:
            son += 1
        d = V.get(sem[bas])
        if d is not None:
            try:
                x = np.asarray(fonk(d), float)
                if len(x) == len(d):
                    out[bas:son] = x[ii[bas:son]]
            except Exception as ex:
                log.warning("değişken %s %s hesaplanamadı: %s", ad, sem[bas], ex)
        bas = son
    return pd.Series(out, index=P.index, name=ad)


def varyantlar(tanim: Dict[str, Any]) -> List[Optional[int]]:
    return list(tanim.get("pencereler") or (None,))


def degisken_hesapla(P: pd.DataFrame, V: Dict[str, pd.DataFrame], tanim: Dict[str, Any], p: Optional[int], ad: str) -> Tuple[pd.Series, Optional[Callable]]:
    """Varyant p için değişken: panel fonksiyonu (kesitsel) ya da sembol fonksiyonu (fabrika(p) / fonk). Dönüş: seri, sembol fonksiyonu (C için; kesitselde None)."""
    if tanim.get("panel_fonk") is not None:
        pf = tanim["fabrika"](p) if (tanim.get("fabrika") is not None and p is not None) else tanim["panel_fonk"]
        x = pf(P); return pd.Series(np.asarray(x, np.float32), index=P.index, name=ad), None
    fonk = tanim["fabrika"](p) if (tanim.get("fabrika") is not None and p is not None) else tanim["fonk"]
    return degisken_ekle(P, V, fonk, ad), fonk


def _donem_sec(D: pd.DataFrame, donem: Any, kol: str) -> pd.DataFrame:
    if donem is None:
        return D[~D[kol].isin(["PURGE", "EMBARGO", "TANIMSIZ", "DISI"])]
    adlar = (donem,) if isinstance(donem, str) else tuple(donem)
    return D[D[kol].isin(adlar)]


def _donem_ad(donem: Any) -> str:
    return "hepsi" if donem is None else (donem if isinstance(donem, str) else "+".join(donem))


def _z_gun_vd(D: pd.DataFrame, x: str, en_az: int = 5) -> np.ndarray:
    g = D.groupby(["tarih", "vd"])[x]; mu = g.transform("mean"); sd = g.transform("std"); n = g.transform("size")
    z = (D[x] - mu) / sd.replace(0, np.nan); z[n < en_az] = np.nan
    g2 = D.groupby("tarih")[x]; mu2 = g2.transform("mean"); sd2 = g2.transform("std"); n2 = g2.transform("size")
    z2 = (D[x] - mu2) / sd2.replace(0, np.nan); z2[n2 < en_az] = np.nan
    return z.fillna(z2).to_numpy(float)


def yontem_A(P: pd.DataFrame, O: pd.DataFrame, x: str, ufuk: str, rng: np.random.Generator, donem: Any = None) -> Dict[str, Any]:
    h = OLAY[ufuk][0]; kol = f"donem{h}"; D = _donem_sec(P[P.likit & P[x].notna()], donem, kol)
    bos = {"yontem": "A", "ufuk": ufuk, "donem": _donem_ad(donem), "n_olay": 0, "p": np.nan, "karar": "VERİ YETERSİZ"}
    if not len(D):
        return bos
    Ou = _donem_sec(O[O.ufuk == ufuk], donem, "donem"); anahtar = set(zip(Ou.sembol, Ou.tarih))
    olay = np.fromiter(((s, t) in anahtar for s, t in zip(D.sembol, D.tarih)), bool, len(D))
    if olay.sum() < 2:
        return {**bos, "n_olay": int(olay.sum())}
    z = _z_gun_vd(D, x); d, a, b, p = d_boot_ay(z, olay, D.ay.to_numpy(), BOOT, rng); _, ab, bb, pb = d_boot_ay(z, olay, D.blok60.to_numpy(), BOOT, rng); au = auc(z[olay], z[~olay])
    n1 = int(olay.sum()); xv = D[x].to_numpy(float); zok = np.isfinite(z)
    out = {"yontem": "A", "ufuk": ufuk, "donem": _donem_ad(donem), "n_olay": n1, "n_olmayan": int((~olay).sum()), "d": d, "d_alt": a, "d_ust": b, "d_alt_blok": ab, "d_ust_blok": bb, "p": p, "p_blok": pb, "auc": au,
           "x_olay_ort": float(np.nanmean(xv[olay])), "x_olmayan_ort": float(np.nanmean(xv[~olay])) if (~olay).any() else np.nan}
    yil = D.tarih.dt.year.to_numpy(); isaret = {}
    for y in np.unique(yil):
        m = (yil == y) & zok
        if (m & olay).sum() >= 10 and (m & ~olay).sum() >= 10:
            isaret[int(y)] = float(np.sign(z[m & olay].mean() - z[m & ~olay].mean()))
    out["yil_isaret"] = isaret; out["yil_n"] = len(isaret); out["yil_tekrar"] = int(sum(1 for v in isaret.values() if v == np.sign(d))) if np.isfinite(d) else 0
    rj = D.rejim.to_numpy(); rej = {}
    for r_ in ("BOGA", "AYI"):
        m = (rj == r_) & zok
        if (m & olay).sum() >= N_MIN and (m & ~olay).sum() >= N_MIN:
            rej[r_] = float(np.sign(z[m & olay].mean() - z[m & ~olay].mean()))
    out["rejim_isaret"] = rej; out["rejim_tutarli"] = bool(len(rej) < 2 or len(set(rej.values())) == 1)
    out["karar"] = "VERİ YETERSİZ" if n1 < N_MIN else ("ETKİ" if (abs(d) >= A_D_ESIK and np.isfinite(a) and (a > 0 or b < 0) and abs(au - 0.5) >= A_AUC_ESIK) else "ETKİ YOK")
    return out


def _ortusmez(S: pd.DataFrame, h: int) -> pd.DataFrame:
    S = S.sort_values(["sembol", "i"]); sem = S.sembol.to_numpy(); ii = S.i.to_numpy(); al = np.zeros(len(S), dtype=bool); son = -10 ** 9; onceki = None
    for k in range(len(S)):
        if sem[k] != onceki:
            onceki = sem[k]; son = -10 ** 9
        if ii[k] >= son + h:
            al[k] = True; son = ii[k]
    return S[al]


def yontem_B(P: pd.DataFrame, x: str, yon: int, rng: np.random.Generator, donem: Any = None, k: int = 5) -> Dict[str, Any]:
    D = _donem_sec(P[P.likit & P.r60_tanimli & P[x].notna() & (P.vd >= 0)], donem, "donem60")
    bos = {"yontem": "B", "donem": _donem_ad(donem), "yon": yon, "n": 0, "p": np.nan, "karar": "VERİ YETERSİZ"}
    if not len(D):
        return bos
    q = D.groupby("tarih")[x].rank(pct=True); sin = _ortusmez((D[q >= 0.8] if yon > 0 else D[q <= 0.2]).copy(), OLAY["Y60"][0])
    if not len(sin):
        return bos
    M = eslestir(D, sin, D, k=k, rng=rng); X = pd.concat([sin, M], axis=1); X = X[X.kontrol_n > 0]
    if not len(X):
        return {**bos, "eslesmeyen_pay": 1.0}
    f = (X.r60_ileri - X.kontrol_r60_ileri).to_numpy(float); fn = ((X.r60_ileri - X.mal) - (X.kontrol_r60_ileri - X.kontrol_mal)).to_numpy(float)
    ort, a, b = boot_kume(f, X.ay.to_numpy(), BOOT, rng); _, a2, b2 = boot_kume(f, (X.sembol + "|" + X.ceyrek).to_numpy(), BOOT, rng); _, a3, b3 = boot_kume(f, X.blok60.to_numpy(), BOOT, rng)
    ortn, an, bn = boot_kume(fn, X.ay.to_numpy(), BOOT, rng)
    sp = slot_portfoy(X.assign(net=X.r60_ileri - X.mal)[["tarih", "sembol", "vd", "net"]], D.assign(net=D.r60_ileri - D.mal)[["tarih", "sembol", "vd", "net"]], rng)
    yil = X.tarih.dt.year.to_numpy(); isaret = {int(y): float(np.sign(f[yil == y].mean())) for y in np.unique(yil) if (yil == y).sum() >= 10}
    out = {"yontem": "B", "donem": _donem_ad(donem), "yon": yon, "n": int(len(X)), "hisse": int(X.sembol.nunique()), "eslesmeyen_pay": float(1 - len(X) / len(sin)),
           "fark": ort, "fark_alt": a, "fark_ust": b, "fark_alt_hisse_ceyrek": a2, "fark_alt_blok": a3, "fark_ust_blok": b3, "net_fark": ortn, "net_fark_alt": an,
           "p": boot_p(f, X.ay.to_numpy(), BOOT, rng), "yil_isaret": isaret, "yil_n": len(isaret), "yil_tekrar": int(sum(1 for v in isaret.values() if v == np.sign(ort))),
           **{f"slot_{k_}": v for k_, v in sp.items()}}
    out["karar"] = "VERİ YETERSİZ" if out["n"] < N_MIN else ("TUTAR" if (ort >= B_FARK_ESIK and a > 0 and a2 > 0 and ortn > 0 and sp["rastgele_yuzdelik"] >= 0.90) else "TUTMAZ")
    return out


def yontem_C_coklu(P: pd.DataFrame, V: Dict[str, pd.DataFrame], O: pd.DataFrame, x_fonk: Callable[[pd.DataFrame], pd.Series], ufuklar: Tuple[str, ...], donem: Any = None) -> List[Dict[str, Any]]:
    """CUSUM değişim noktaları sembol başına BİR kez; her ufuk için lift. Taban = likit günlerin olay-öncesi-h-gün payı (purge dışı satırlar)."""
    cp_map: Dict[str, np.ndarray] = {}; x_map: Dict[str, int] = {}
    for s in P.loc[P.likit, "sembol"].unique():
        d = V.get(s)
        if d is None:
            continue
        try:
            x = np.asarray(x_fonk(d), float)
        except Exception:
            continue
        if len(x) == len(d):
            cp_map[s] = cusum(x, CUSUM_H); x_map[s] = len(d)
    rows = []
    for ufuk in ufuklar:
        h = OLAY[ufuk][0]; Ou = _donem_sec(O[O.ufuk == ufuk], donem, "donem"); olay_i = {s: g.i.to_numpy() for s, g in Ou.groupby("sembol")}
        L = _donem_sec(P[P.likit], donem, f"donem{h}"); likit_i = {s: g.i.to_numpy() for s, g in L.groupby("sembol")}
        deg_n = 0; deg_olay = 0; taban_n = 0; taban_olay = 0; yon_say = {1: 0, -1: 0}
        for s, li in likit_i.items():
            cp = cp_map.get(s)
            if cp is None or not len(li):
                continue
            oi = olay_i.get(s, np.array([], dtype=int))
            if len(oi):
                onde = np.array([((oi > i) & (oi <= i + h)).any() for i in li]); taban_olay += int(onde.sum())
            taban_n += len(li); lset = set(li.tolist())
            for i, yon in cp:
                if i not in lset:
                    continue
                deg_n += 1; yon_say[int(yon)] += 1; deg_olay += int(((oi > i) & (oi <= i + h)).any()) if len(oi) else 0
        taban = taban_olay / taban_n if taban_n else np.nan; oran = deg_olay / deg_n if deg_n else np.nan; lift = oran / taban if (taban and np.isfinite(oran)) else np.nan
        rows.append({"yontem": "C", "ufuk": ufuk, "donem": _donem_ad(donem), "n_degisim": deg_n, "degisim_sonrasi_olay_orani": oran, "taban_orani": taban, "lift": lift,
                     "yanlis_pozitif_pay": (1 - oran) if np.isfinite(oran) else np.nan, "yon_yukari": yon_say[1], "yon_asagi": yon_say[-1], "p": np.nan,
                     "karar": "VERİ YETERSİZ" if deg_n < N_MIN else ("ETKİ" if lift >= C_LIFT_ESIK else "ETKİ YOK")})
    return rows


def yontem_C(P, V, O, x_fonk, ufuk="Y60", donem=None):
    return yontem_C_coklu(P, V, O, x_fonk, (ufuk,), donem)[0]


def hucre_kos(kimlik: str, tanim: Dict[str, Any], P: pd.DataFrame, V: Dict[str, pd.DataFrame], O: pd.DataFrame, rng: np.random.Generator,
              donemler: Tuple[str, ...] = ("KESIF",), ufuklar: Tuple[str, ...] = tuple(OLAY), yontemler: Optional[Tuple[str, ...]] = None) -> List[Dict[str, Any]]:
    """Bir hücreyi bütün varyantlarında (pencereler) verilen dönem ve ufuklarda koşar; satır listesi döner (hepsi kaydedilir, hiçbiri silinmez)."""
    yont = tuple(yontemler or tanim.get("yontemler", ("A", "B", "C"))); rows = []
    for p in varyantlar(tanim):
        ad = f"{kimlik}|{p if p is not None else 'tek'}"
        try:
            x, fonk = degisken_hesapla(P, V, tanim, p, ad)
        except Exception as ex:
            rows.append({"hucre": kimlik, "varyant": ad, "pencere": p, "yontem": "-", "donem": "", "karar": f"HATA: {ex}"}); log.warning("%s hesaplanamadı: %s", ad, ex); continue
        P[ad] = x; eksik = float(P.loc[P.likit, ad].isna().mean()) if P.likit.any() else 1.0
        for dn in donemler:
            if "A" in yont:
                for uf in ufuklar:
                    rows.append({"hucre": kimlik, "varyant": ad, "pencere": p, **yontem_A(P, O, ad, uf, rng, dn), "eksik_pay": eksik})
            if "C" in yont and fonk is not None:
                rows += [{"hucre": kimlik, "varyant": ad, "pencere": p, **r, "eksik_pay": eksik} for r in yontem_C_coklu(P, V, O, fonk, ufuklar, dn)]
            if "B" in yont:
                rows.append({"hucre": kimlik, "varyant": ad, "pencere": p, **yontem_B(P, ad, int(tanim.get("yon", 1)), rng, dn), "eksik_pay": eksik})
        P.drop(columns=[ad], inplace=True)
    for r in rows:
        r["soru"] = tanim.get("soru", ""); r["dal"] = kimlik.split("-")[0]; r["yon"] = int(tanim.get("yon", 1)); r["not"] = tanim.get("not", "")
    return rows
