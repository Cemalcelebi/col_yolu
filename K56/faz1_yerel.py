"""K56 Faz 1 yerel analizler (ONKAYIT_K56 v1.2-A) ve İÇ doğrulamanın ortak motoru (v1.2-B). Yeni veri indirmez.

A1 seçimsiz kontrol: K55'te KEŞİF ölçütünü geçen 125 (hücre, varyant, ufuk) satırında üç etiketle aynı A ölçüsü: (i) K55 ilk geçiş olayları, (ii) bütün
nitelikli günler, (iii) olay başına kesintisiz nitelikli dizide rastgele gün. Karar tablosu v1.2-A.
A2 kalan etki denetimi (M03 / M16 / M18): yalnız A1'de etkisi kalan satırlarda, (ii) etiketiyle, farklı z tabakalarıyla.
A3 haber ve birleşme bileşimi (M04 / M15): K55 olayları (G1) ve eşleşmiş eşler (G7); ÖNCESİ (sızıntısız, t0−1'e kadar) ve SONRASI (AÇIKLAYICI, öngörü
değil) pencereleri; SEC başvuru özeti (yerel).
Bütün ölçümler K55 kodunu (degisken_hesapla, _z_gun_vd, d_boot_ay, auc, ileri_getiri, yontem_B) aynen kullanır; dönem kapısı (ortak.donem_kapisi)
her ölçümde çağrılır.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from .ortak import K56Ayar, KaynakKaydi, donem_kapisi, log

ESIKLER: Dict[str, Any] = {"mekanik_r": 0.20, "kismi_r": 0.50, "a2_aciklar": 0.50, "a2_kismi": 0.25, "boot": 2000, "g7_es": 5, "vd_tol": 1, "tohum": 56,
                           "oncesi": (-20, -1), "sonrasi_haber": (1, 10), "ic_d": 0.20, "ic_auc": 0.06, "ic_q": 0.10, "ic_yil_n": 10, "m16_dis": ("2020-02-15", "2020-06-30")}
HABER_MADDE = ("1.01", "7.01", "8.01")
BIRLESME_FORM = ("SC TO-T", "SC TO-T/A", "SC TO-I", "SC TO-I/A", "SC 14D9", "SC 14D9/A", "DEFM14A", "425", "S-4", "S-4/A")
IHRAC_FORM = ("S-1", "S-1/A", "S-3", "S-3ASR", "424B1", "424B4", "424B5")
SAHIPLIK_FORM = ("SC 13D", "SC 13D/A", "SC 13G", "SC 13G/A")


# ---------------------------------------------------------------- veri hazırlığı (K55 Faz 1 ile aynı yol)
def k55_veri(A: K56Ayar, kk: KaynakKaydi, panel_yol: str, olay_yol: str) -> Dict[str, Any]:
    """K55 evreni (network=False), panel, olay tablosu, ek veriler (SPY, sektör sepetleri) ve D10 bileşen sütunları."""
    from K55.evren import evren_kur
    from K55.faz1 import D10_BILESEN, DALLAR, ek_kur, hucreleri_kur
    from K55.hucre import degisken_hesapla
    from K55.hucreler import HUCRELER
    from K55.ortak import K55Ayar, cy, veri_sha
    A55 = K55Ayar(veri=A.veri, cikti=os.path.dirname(os.path.dirname(panel_yol)), k54=A.abd, isci=1)
    E = evren_kur(A55, veri_sha(A55), network=False); V, EV = E["V"], E["EV"]
    P = pd.read_pickle(kk.oku(panel_yol, "veri", "K55 Faz 0 tam evren paneli")); O = pd.read_csv(kk.oku(olay_yol, "veri", "K55 olay tablosu")); O["tarih"] = pd.to_datetime(O.tarih)
    C = cy(); endeks = C.cy_endeks(C.CYAyar(veri=A.veri, cikti=A55.cikti, pazarlar=("ABD",)), C.CY); ek_kur(V, EV, endeks); hucreleri_kur(DALLAR)
    for kb, p in D10_BILESEN:
        if kb in HUCRELER and kb not in P:
            P[kb], _ = degisken_hesapla(P, V, HUCRELER[kb], p, kb)
    return {"P": P, "V": V, "EV": EV, "O": O, "endeks": endeks, "evren_surum": E["surum"]}


def _bloklar(sem: np.ndarray):
    bas = 0; n = len(sem)
    while bas < n:
        son = bas
        while son < n and sem[son] == sem[bas]:
            son += 1
        yield bas, son
        bas = son


def nitelikli_gunler(P: pd.DataFrame, V: Dict[str, pd.DataFrame]) -> Dict[str, np.ndarray]:
    """Ufuk başına: likit ve pencere tam ve C[t+h] / O[t+1] − 1 >= eşik (K55/olay_tanimlari.ileri_getiri, seri_erken False)."""
    from K55.olay_tanimlari import ileri_getiri
    from K55.ortak import OLAY
    out = {u: np.zeros(len(P), bool) for u in OLAY}; sem = P.sembol.to_numpy(); ii = P.i.to_numpy(); lk = P.likit.to_numpy()
    for a, b in _bloklar(sem):
        d = V.get(sem[a])
        if d is None:
            continue
        Oa = d.Open.to_numpy(float); Ca = d.Close.to_numpy(float); ix = ii[a:b]
        for u, (h, e) in OLAY.items():
            r, tam = ileri_getiri(Oa, Ca, h, False, "k51"); out[u][a:b] = tam[ix] & (r[ix] >= e) & lk[a:b]
    return out


def olay_maskesi(P: pd.DataFrame, O: pd.DataFrame, ufuk: str, donem: str) -> np.ndarray:
    Ou = O[(O.ufuk == ufuk) & (O.donem == donem)]; anahtar = set(zip(Ou.sembol, Ou.tarih))
    return np.fromiter(((s, t) in anahtar for s, t in zip(P.sembol.to_numpy(), P.tarih.to_numpy())), bool, len(P))


def rastgele_gun_maskesi(P: pd.DataFrame, olay: np.ndarray, nit: np.ndarray, tohum_metni: str) -> np.ndarray:
    """(iii): her olay satırından başlayan kesintisiz nitelikli satır dizisinde (aynı sembol, ardışık i) tek tip rastgele bir satır."""
    rng = np.random.default_rng(int(hashlib.sha256(tohum_metni.encode()).hexdigest()[:12], 16))
    out = np.zeros(len(P), bool); sem = P.sembol.to_numpy(); ii = P.i.to_numpy()
    for k in np.flatnonzero(olay):
        L = 1
        while k + L < len(P) and sem[k + L] == sem[k] and ii[k + L] == ii[k] + L and nit[k + L]:
            L += 1
        out[k + int(rng.integers(L))] = True
    return out


# ---------------------------------------------------------------- A ölçüsü (K55 ile aynı tahminci) ve karar tablosu
def z_tabaka(D: pd.DataFrame, x: str, gruplar: List[str], en_az: int = 5) -> np.ndarray:
    """K55/_z_gun_vd'nin genellemesi: z (tarih + gruplar) içinde; grup < en_az ise yalnız gün içi z (K55 v1.1 yedeği)."""
    g = D.groupby(["tarih"] + gruplar)[x]; mu = g.transform("mean"); sd = g.transform("std"); n = g.transform("size")
    z = (D[x] - mu) / sd.replace(0, np.nan); z[n < en_az] = np.nan
    g2 = D.groupby("tarih")[x]; z2 = (D[x] - g2.transform("mean")) / g2.transform("std").replace(0, np.nan); z2[g2.transform("size") < en_az] = np.nan
    return z.fillna(z2).to_numpy(float)


def a_olc(z: np.ndarray, olay: np.ndarray, ay: np.ndarray, yil: np.ndarray, B: int, rng: np.random.Generator) -> Dict[str, Any]:
    from K55.istatistik import auc, d_boot_ay
    ok = np.isfinite(z)
    if (olay & ok).sum() < 30:
        return {"n_olay": int((olay & ok).sum()), "d": np.nan, "d_alt": np.nan, "d_ust": np.nan, "p": np.nan, "auc": np.nan, "yil_isaret": {}}
    d, a, b, p = d_boot_ay(z, olay, ay, B, rng); isaret = {}
    for y in np.unique(yil):
        m = (yil == y) & ok
        if (m & olay).sum() >= ESIKLER["ic_yil_n"] and (m & ~olay).sum() >= ESIKLER["ic_yil_n"]:
            isaret[int(y)] = float(np.sign(z[m & olay].mean() - z[m & ~olay].mean()))
    return {"n_olay": int((olay & ok).sum()), "d": d, "d_alt": a, "d_ust": b, "p": p, "auc": auc(z[olay & ok], z[~olay & ok]), "yil_isaret": isaret}


def karar_a1(di: float, dii: float, alt: float, ust: float, sent_oran: float) -> str:
    """v1.2-A karar tablosu (satır)."""
    if not (np.isfinite(di) and np.isfinite(dii)) or di == 0:
        return "TANIMSIZ"
    kapsar = not (alt > 0 or ust < 0); r = dii / di
    if r < 0 and not kapsar:
        return "TERS KALINTI"
    if kapsar or 0 <= r <= ESIKLER["mekanik_r"]:
        return "MEKANİK (gerçek + sentetik)" if (np.isfinite(sent_oran) and sent_oran >= 0.5) else "MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor)"
    if r < ESIKLER["kismi_r"]:
        return "KISMEN MEKANİK"
    return "GERÇEK ETKİ KALIYOR"


def hucre_karari(siniflar: List[str]) -> str:
    s = pd.Series([("MEKANİK" if c.startswith("MEKANİK") else c) for c in siniflar]).value_counts()
    if not len(s):
        return "TANIMSIZ"
    return s.index[0] if (len(s) == 1 or s.iloc[0] > s.iloc[1]) else "BELİRSİZ"


# ---------------------------------------------------------------- A2 kalan etki denetimi için ek sütunlar
def a2_sutunlari(P: pd.DataFrame, V: Dict[str, pd.DataFrame], endeks: pd.DataFrame) -> pd.DataFrame:
    """oynaklık yüzdeliği (50 kova, gün içi, likit), vol20 / vol60 üçlüsü, 250 gün beta üçlüsü (SPY); hepsi t gününe kadar bilinen veriyle."""
    sem = P.sembol.to_numpy(); ii = P.i.to_numpy(); v20 = np.full(len(P), np.nan); beta = np.full(len(P), np.nan)
    spy = endeks["SPY"].dropna(); rs = np.log(spy).diff()
    for a, b in _bloklar(sem):
        d = V.get(sem[a])
        if d is None:
            continue
        r = np.log(d.Close.astype(float)).diff(); v20[a:b] = r.rolling(20, min_periods=15).std().to_numpy()[ii[a:b]]
        m = rs.reindex(d.index); cov = r.rolling(250, min_periods=150).cov(m); var = m.rolling(250, min_periods=150).var()
        beta[a:b] = (cov / var.replace(0, np.nan)).to_numpy()[ii[a:b]]
    X = pd.DataFrame(index=P.index); L = P.likit.to_numpy()
    X["v_yuzde50"] = np.int16(-1); X["v_oran3"] = np.int8(-1); X["beta3"] = np.int8(-1)
    T = pd.DataFrame({"tarih": P.tarih, "vol60": P.vol60, "oran": v20 / P.vol60.to_numpy(float), "beta": beta})[L]
    X.loc[T.index, "v_yuzde50"] = np.minimum((T.groupby("tarih").vol60.rank(pct=True) * 50).fillna(25).astype(int), 49).astype(np.int16)
    X.loc[T.index, "v_oran3"] = np.minimum((T.groupby("tarih").oran.rank(pct=True) * 3).fillna(1).astype(int), 2).astype(np.int8)
    X.loc[T.index, "beta3"] = np.minimum((T.groupby("tarih").beta.rank(pct=True) * 3).fillna(1).astype(int), 2).astype(np.int8)
    return X


A2_DENETIMLER = (("M03a", ["v_yuzde50"], None), ("M03b", ["vd", "v_oran3"], None), ("M16a", ["vd"], "m16_dis"), ("M16b", ["vd", "beta3"], None), ("M18", ["sektor"], None))


# ---------------------------------------------------------------- A3 başvuru bayrakları (ÖNCESİ sızıntısız / SONRASI açıklayıcı)
_BASVURU_ONB: Dict[Tuple[int, int], Tuple[np.ndarray, np.ndarray, np.ndarray]] = {}


def basvuru_tablosu(J: Dict[str, Any], cik: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """CIK başına (tarih, form, madde) dizileri, tarihe göre sıralı; (id(J), cik) ile önbellekli (olay başına yeniden ayrıştırma yok)."""
    from .kurumsal_olaylar import _liste
    if cik is None or not np.isfinite(cik):
        return np.array([], dtype="datetime64[D]"), np.array([], dtype=object), np.array([], dtype=object)
    k = (id(J), int(cik))
    if k in _BASVURU_ONB:
        return _BASVURU_ONB[k]
    v = J.get(str(int(cik)))
    if not v:
        r = (np.array([], dtype="datetime64[D]"), np.array([], dtype=object), np.array([], dtype=object))
    else:
        t = np.array(_liste(v["date"]), dtype="datetime64[D]"); f = np.array(_liste(v["form"]), dtype=object); it = np.array(_liste(v.get("items", "[]")) or [""] * len(f), dtype=object)
        s = np.argsort(t, kind="stable"); r = (t[s], f[s], it[s])
    _BASVURU_ONB[k] = r; return r


def oncesi_bayraklar(t: np.ndarray, f: np.ndarray, it: np.ndarray, gunler: pd.DatetimeIndex, i0: int) -> Dict[str, int]:
    """ÖNCESİ: başvuru tarihi ∈ [gün(i0−20), gün(i0−1)] (işlem günü takvimi; t0 günü HARİÇ — saat bilgisi yok). Sızıntı kapısı: kullanılan en geç tarih < t0."""
    a = gunler[max(0, i0 + ESIKLER["oncesi"][0])].to_datetime64().astype("datetime64[D]"); b = gunler[max(0, i0 + ESIKLER["oncesi"][1])].to_datetime64().astype("datetime64[D]")
    t0 = gunler[i0].to_datetime64().astype("datetime64[D]")
    m = (t >= a) & (t <= b)
    if m.any() and t[m].max() >= t0:
        raise RuntimeError("ÖNCESİ penceresine t0 ya da sonrası başvuru girdi (sızıntı)")
    ff, ii = f[m], it[m]
    return {"once_8k": int(any(str(x).startswith("8-K") for x in ff)), "once_8k_202": int(any(str(x).startswith("8-K") and "2.02" in str(y) for x, y in zip(ff, ii))),
            "once_ihrac": int(any(x in IHRAC_FORM or (str(x).startswith("8-K") and "3.02" in str(y)) for x, y in zip(ff, ii))), "once_13dg": int(any(x in SAHIPLIK_FORM for x in ff))}


def sonrasi_bayraklar(t: np.ndarray, f: np.ndarray, it: np.ndarray, gunler: pd.DatetimeIndex, i0: int, h: int) -> Dict[str, int]:
    """SONRASI (AÇIKLAYICI; öngörü değil): haber [i0+1, i0+10], birleşme / ihraç [i0+1, i0+h] işlem günü."""
    n = len(gunler)
    def ara(a, b):
        if i0 + a >= n:
            return np.zeros(len(t), bool)
        x, y = gunler[i0 + a].to_datetime64().astype("datetime64[D]"), gunler[min(n - 1, i0 + b)].to_datetime64().astype("datetime64[D]"); return (t >= x) & (t <= y)
    mh = ara(*ESIKLER["sonrasi_haber"]); mu = ara(1, h)
    return {"sonra_202": int(any(str(x).startswith("8-K") and "2.02" in str(y) for x, y in zip(f[mh], it[mh]))),
            "sonra_haber": int(any(str(x).startswith("8-K") and any(k in str(y) for k in HABER_MADDE) for x, y in zip(f[mh], it[mh]))),
            "sonra_birlesme": int(any(x in BIRLESME_FORM or (str(x).startswith("8-K") and "2.01" in str(y)) for x, y in zip(f[mu], it[mu]))),
            "sonra_ihrac": int(any(x in IHRAC_FORM or (str(x).startswith("8-K") and "3.02" in str(y)) for x, y in zip(f[mu], it[mu])))}


def g7_esleri(P: pd.DataFrame, O: pd.DataFrame, ufuk: str, donem: str, rng: np.random.Generator) -> pd.DataFrame:
    """Olay başına en çok 5 eş: aynı gün, sektör (bilinmiyorsa şartsız), likidite üçlüsü, |vd farkı| <= 1, likit, pencere tanımlı, ±h içinde aynı ufukta olayı yok."""
    from K55.ortak import OLAY
    h = OLAY[ufuk][0]; Ou = O[(O.ufuk == ufuk) & (O.donem == donem)]
    Pd = P[P.likit & (P[f"donem{h}"] == donem)][["tarih", "sembol", "i", "sektor", "lt", "vd"]]
    oi = O[O.ufuk == ufuk].groupby("sembol").i.apply(lambda s: np.sort(s.to_numpy())).to_dict()
    gun = {t: g for t, g in Pd.groupby("tarih")}; rows = []
    for r in Ou.itertuples():
        g = gun.get(r.tarih)
        if g is None:
            continue
        e = g[g.sembol == r.sembol]
        if not len(e):
            continue
        e = e.iloc[0]; m = (g.sembol != r.sembol) & (g["lt"] == e["lt"]) & ((g["vd"] - e["vd"]).abs() <= ESIKLER["vd_tol"])     # g.lt = DataFrame.lt metodu
        if isinstance(e.sektor, str) and e.sektor.lower() != "bilinmiyor":
            m &= g.sektor == e.sektor
        c = g[m]
        if len(c):
            iyi = [k for k, (s, i) in enumerate(zip(c.sembol, c.i)) if not (s in oi and np.any(np.abs(oi[s] - i) <= h))]
            c = c.iloc[iyi]
        sec = c.iloc[rng.permutation(len(c))[: ESIKLER["g7_es"]]] if len(c) else c
        for s_ in sec.itertuples():
            rows.append({"olay_sembol": r.sembol, "tarih": r.tarih, "sembol": s_.sembol, "i": int(s_.i)})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- koşu motoru (KEŞİF: K56-F1A; İÇ: K56-IC)
_CTX: Dict[str, Any] = {}


def basvuru_bayrak_dizileri(P: pd.DataFrame, V: Dict[str, pd.DataFrame], J: Dict[str, Any], cikmap: Dict[str, int]) -> Dict[str, np.ndarray]:
    """Ayrıştırma için satır başına SONRASI bayrakları (AÇIKLAYICI): haber10 = (gün(i), gün(i+10)] içinde 8-K 2.02 / 1.01 / 7.01 / 8.01; birlesme_h (h = 60 /
    120 / 250) = (gün(i), gün(i+h)] içinde birleşme belgesi ya da 8-K 2.01."""
    from K55.ortak import OLAY
    out = {"haber10": np.zeros(len(P), bool), **{f"birlesme{h}": np.zeros(len(P), bool) for h, _ in OLAY.values()}}
    sem = P.sembol.to_numpy(); ii = P.i.to_numpy()
    for a, b in _bloklar(sem):
        d = V.get(sem[a]); t, f, it = basvuru_tablosu(J, cikmap.get(sem[a], np.nan))
        if d is None or not len(t):
            continue
        g = d.index.to_numpy().astype("datetime64[D]"); n = len(g)
        hab = np.sort(t[[str(x).startswith("8-K") and any(k in str(y) for k in ("2.02",) + HABER_MADDE) for x, y in zip(f, it)]])
        bir = np.sort(t[[x in BIRLESME_FORM or (str(x).startswith("8-K") and "2.01" in str(y)) for x, y in zip(f, it)]])
        ix = ii[a:b]; bas = g[ix]
        def var(dizi, k):
            if not len(dizi):
                return np.zeros(len(ix), bool)
            son = g[np.minimum(ix + k, n - 1)]; return (np.searchsorted(dizi, son, side="right") - np.searchsorted(dizi, bas, side="right")) > 0
        out["haber10"][a:b] = var(hab, 10)
        for h, _ in OLAY.values():
            out[f"birlesme{h}"][a:b] = var(bir, h)
    return out


def _isci(arg) -> Dict[str, Any]:
    """Bir varyant: değişken bir kez hesaplanır; varyantın KEŞİF ufuklarında üç etiket, karar, ayrıştırma, (gerekirse) A2; İÇ'te ayrıca B3."""
    from K55.hucre import _z_gun_vd, degisken_hesapla, yontem_B
    from K55.hucreler import HUCRELER
    from K55.ortak import OLAY
    hucre, varyant, ufuklar = arg; C = _CTX; P = C["P"]; donem = C["donem"]; t0 = time.time(); rows = []; b3 = None
    p_ = varyant.split("|")[1]; p_ = None if p_ == "tek" else int(p_)
    try:
        x, _ = degisken_hesapla(P, C["V"], HUCRELER[hucre], p_, varyant); x = np.asarray(x, float)
    except Exception as ex:
        return {"satir": [{"hucre": hucre, "varyant": varyant, "ufuk": u, "hata": f"{type(ex).__name__}: {ex}"} for u in ufuklar], "b3": None}
    for u in ufuklar:
        h = OLAY[u][0]; m = P.likit.to_numpy() & np.isfinite(x) & (P[f"donem{h}"].to_numpy() == donem)
        Dm = P.loc[m, ["tarih", "vd", "ay", "sektor", "v_yuzde50", "v_oran3", "beta3", f"bitis{h}"]].copy(); Dm["_x"] = x[m]
        donem_kapisi(donem, Dm, h)
        yil = Dm.tarih.dt.year.to_numpy(); ay = Dm.ay.to_numpy(); rng = np.random.default_rng(int(hashlib.sha256(f"{hucre}|{varyant}|{u}|{donem}".encode()).hexdigest()[:12], 16))
        z = _z_gun_vd(Dm, "_x"); ev_i = C["olay"][u][m]; nit = C["nit"][u]; ev_ii = nit[m]
        ev_iii = rastgele_gun_maskesi(P, C["olay"][u], nit, f"{hucre}|{varyant}|{u}|56")[m]
        ri = a_olc(z, ev_i, ay, yil, ESIKLER["boot"], rng); rii = a_olc(z, ev_ii, ay, yil, ESIKLER["boot"], rng); riii = a_olc(z, ev_iii, ay, yil, ESIKLER["boot"], rng)
        so = C["sent"].get((hucre, varyant, u), np.nan)
        k1 = karar_a1(ri["d"], rii["d"], rii["d_alt"], rii["d_ust"], so); k3 = karar_a1(ri["d"], riii["d"], riii["d_alt"], riii["d_ust"], so)
        # ayrıştırma (AÇIKLAYICI): SONRASI haberi / birleşmesi olan nitelikli günler analizden çıkarılır
        if C.get("yalniz_a1"):
            ayr = np.ones(int(m.sum()), bool); ra = {"d": np.nan, "d_alt": np.nan, "d_ust": np.nan}
        else:
            ayr = ~(nit & (C["bayrak"]["haber10"] | C["bayrak"][f"birlesme{h}"]))[m]
            Da = Dm[ayr]; ra = a_olc(_z_gun_vd(Da, "_x"), ev_ii[ayr], Da.ay.to_numpy(), Da.tarih.dt.year.to_numpy(), ESIKLER["boot"], rng) if ayr.any() else {"d": np.nan, "d_alt": np.nan, "d_ust": np.nan}
        sat = {"hucre": hucre, "varyant": varyant, "ufuk": u, "donem": donem, "n_satir": int(m.sum()), "sent_oran_faz0": so,
               **{f"i_{k}": v for k, v in ri.items() if k != "yil_isaret"}, "i_yil": json.dumps(ri["yil_isaret"]),
               **{f"ii_{k}": v for k, v in rii.items() if k != "yil_isaret"}, **{f"iii_{k}": v for k, v in riii.items() if k != "yil_isaret"},
               "r_ii": rii["d"] / ri["d"] if (np.isfinite(ri["d"]) and ri["d"]) else np.nan, "sinif_a1": k1, "sinif_iii": k3, "iii_farkli": k1 != k3,
               "ayr_d": ra["d"], "ayr_d_alt": ra["d_alt"], "ayr_d_ust": ra["d_ust"], "ayr_cikan_nitelikli": int((ev_ii & ~ayr).sum())}
        if k1 in ("KISMEN MEKANİK", "GERÇEK ETKİ KALIYOR", "TERS KALINTI") and not C.get("yalniz_a1"):
            for ad, gruplar, dis in A2_DENETIMLER:
                if dis == "m16_dis":
                    a_, b_ = pd.Timestamp(ESIKLER["m16_dis"][0]), pd.Timestamp(ESIKLER["m16_dis"][1]); keep = ~((Dm.tarih >= a_) & (Dm.tarih <= b_)).to_numpy()
                    if keep.all():
                        sat[f"a2_{ad}_d"] = np.nan; sat[f"a2_{ad}_kuculme"] = np.nan; continue
                else:
                    keep = np.ones(len(Dm), bool)
                D2 = Dm[keep]; r2 = a_olc(z_tabaka(D2, "_x", gruplar), ev_ii[keep], D2.ay.to_numpy(), D2.tarih.dt.year.to_numpy(), ESIKLER["boot"], rng)
                sat[f"a2_{ad}_d"] = r2["d"]; sat[f"a2_{ad}_alt"] = r2["d_alt"]; sat[f"a2_{ad}_ust"] = r2["d_ust"]
                sat[f"a2_{ad}_kuculme"] = 1 - abs(r2["d"]) / abs(rii["d"]) if (np.isfinite(r2["d"]) and rii["d"]) else np.nan
        rows.append(sat)
    if C.get("b3"):
        try:
            P2 = P.copy(deep=False); P2[varyant] = x.astype(np.float32); yon = HUCRELER[hucre]["yon"]
            b3 = {"hucre": hucre, "varyant": varyant, **{k: v for k, v in yontem_B(P2, varyant, yon, np.random.default_rng(56), donem=donem).items() if not isinstance(v, dict)}}
        except Exception as ex:
            b3 = {"hucre": hucre, "varyant": varyant, "karar": f"HATA: {type(ex).__name__}: {ex}"}
    for r in rows:
        r["sure_sn"] = round(time.time() - t0, 1)
    return {"satir": rows, "b3": b3}


def bilesim(P: pd.DataFrame, V: Dict[str, pd.DataFrame], O: pd.DataFrame, J: Dict[str, Any], cikmap: Dict[str, int], donem: str) -> pd.DataFrame:
    """A3: G1 / G7 başvuru bileşimi (ÖNCESİ sızıntısız; SONRASI açıklayıcı), olay başına eşleşmiş fark ve ay kümeli %95 aralık."""
    from K55.istatistik import boot_kume
    from K55.ortak import OLAY
    rows = []
    for u, (h, _) in OLAY.items():
        rng = np.random.default_rng(ESIKLER["tohum"]); G = g7_esleri(P, O, u, donem, rng); Ou = O[(O.ufuk == u) & (O.donem == donem)]
        if not len(Ou):
            continue
        def bayrak(sym, i0):
            d = V.get(sym); t, f, it = basvuru_tablosu(J, cikmap.get(sym, np.nan))
            if d is None:
                return None
            return {**oncesi_bayraklar(t, f, it, d.index, i0), **sonrasi_bayraklar(t, f, it, d.index, i0, h), "sec_var": int(len(t) > 0)}
        b1 = {(r.sembol, r.tarih): bayrak(r.sembol, int(r.i)) for r in Ou.itertuples()}
        b7 = [(r.olay_sembol, r.tarih, bayrak(r.sembol, int(r.i))) for r in G.itertuples()] if len(G) else []
        es = pd.DataFrame([{"olay_sembol": a, "tarih": t, **b} for a, t, b in b7 if b]) if b7 else pd.DataFrame()
        g1 = pd.DataFrame([{"sembol": k[0], "tarih": k[1], **v} for k, v in b1.items() if v])
        g1 = g1[g1.sec_var == 1]
        for olc in ("once_8k", "once_8k_202", "once_ihrac", "once_13dg", "sonra_202", "sonra_haber", "sonra_birlesme", "sonra_ihrac"):
            if not len(es):
                continue
            em = es[es.sec_var == 1].groupby(["olay_sembol", "tarih"])[olc].mean().rename("es"); em.index.names = ["sembol", "tarih"]   # ad farklıysa join yalnız tarihte birleşir
            X = g1.set_index(["sembol", "tarih"])[[olc]].join(em, how="inner")
            if X.index.duplicated().any() or len(X) > len(g1):
                raise RuntimeError(f"A3 birleştirme olay başına tek satır değil ({len(X)} > {len(g1)})")
            if len(X) < 30:
                rows.append({"donem": donem, "ufuk": u, "olcu": olc, "n_olay": len(X), "karar": "VERİ YETERSİZ"}); continue
            f = (X[olc] - X.es).to_numpy(float); ayk = pd.to_datetime(X.index.get_level_values(1)).to_period("M").astype(str).to_numpy()
            ort, a, b = boot_kume(f, ayk, ESIKLER["boot"], np.random.default_rng(ESIKLER["tohum"]))
            rows.append({"donem": donem, "ufuk": u, "olcu": olc, "tur": "ÖNCESİ (sızıntısız)" if olc.startswith("once") else "SONRASI (açıklayıcı, öngörü değil)",
                         "n_olay": len(X), "pay_g1": float(X[olc].mean()), "pay_g7": float(X.es.mean()), "fark": ort, "fark_alt": a, "fark_ust": b,
                         "karar": "G1 > G7" if a > 0 else ("G1 < G7" if b < 0 else "fark yok")})
    return pd.DataFrame(rows)


def calistir(A: K56Ayar, kk: KaynakKaydi, donem: str, panel_yol: Optional[str], olay_yol: Optional[str], isci: int = 3, b3: bool = False, sinir: Optional[int] = None,
             veri: Optional[Dict[str, Any]] = None, yalniz_a1: bool = False) -> Dict[str, Any]:
    """Ortak motor: KEŞİF (A1-A3) ya da İÇ (B1-B4). Satırlar = K55 KEŞİF ölçütünü geçen 125 (hücre, varyant, ufuk). sinir: yalnız ilk n varyant (duman
    sınaması; rapora yazılmaz). veri: hazır P / V / O / EV / endeks / evren_surum (evren v2); yalniz_a1: A2, ayrıştırma ve A3 yok (evren v2 etkisi)."""
    import multiprocessing as mp
    from K55.istatistik import bh_fdr
    from . import mekanizma as M
    from .kurumsal_olaylar import sec_ozet_yukle
    donem_kapisi(donem); t0 = time.time()
    VERI = veri if veri is not None else k55_veri(A, kk, panel_yol, olay_yol); P, V, O, EV = VERI["P"], VERI["V"], VERI["O"], VERI["EV"]
    K = M.kesif_satirlari(A, kk)
    zk = os.path.join(A.cikti, "K56_SECIM_SENTETIK_KESIF.csv")
    sent = {(r.hucre, r.varyant, r.ufuk): r.oran for r in pd.read_csv(kk.oku(zk, "kiyas", "Faz 0 sentetik oran (KEŞİF satırları)")).itertuples()} if os.path.exists(zk) else {}
    X = a2_sutunlari(P, V, VERI["endeks"])
    for c in X.columns:
        P[c] = X[c].to_numpy()
    J = sec_ozet_yukle(A); kk.oku("/tmp/k55/sec_ozet.json", "veri", "SEC başvuru özeti (islenmis-veri k55)")
    k55ev = pd.read_csv(kk.oku(os.path.join(A.k55, "K55_EVREN.csv"), "veri", "sembol -> CIK")); cikmap = {r.sembol: int(r.cik) for r in k55ev.dropna(subset=["cik"]).itertuples()}
    nit = nitelikli_gunler(P, V); olay = {u: olay_maskesi(P, O, u, donem) for u in nit}
    bayrak = basvuru_bayrak_dizileri(P, V, J, cikmap) if not yalniz_a1 else None
    _CTX.clear(); _CTX.update({"P": P, "V": V, "donem": donem, "nit": nit, "olay": olay, "bayrak": bayrak, "sent": sent, "b3": b3, "yalniz_a1": yalniz_a1})
    isler = [(h, v, sorted(g.ufuk.unique())) for (h, v), g in K.groupby(["hucre", "varyant"], sort=True)][: sinir or None]
    log.info("%s motoru: %d varyant, %d satır, işçi %d (veri %.0f sn)", donem, len(isler), len(K), isci, time.time() - t0)
    if isci > 1:
        with mp.get_context("fork").Pool(isci) as hv:
            son = hv.map(_isci, isler, chunksize=1)
    else:
        son = [_isci(a) for a in isler]
    S = pd.DataFrame([r for s in son for r in s["satir"]]); B3 = pd.DataFrame([s["b3"] for s in son if s["b3"]]) if b3 else pd.DataFrame()
    # İÇ ölçütleri (B1): KEŞİF ile aynı işaret + |d| >= 0,20 + aralık 0'ı dışlar + AUC + iki yıl aynı işaret + BH q (125 satır)
    kd = K.set_index(["hucre", "varyant", "ufuk"]).d
    S["kesif_d"] = [kd.get((r.hucre, r.varyant, r.ufuk), np.nan) for r in S.itertuples()]
    if donem == "IC_DOGRULAMA" and "i_p" in S:
        S["q_bh"] = bh_fdr(S.i_p.fillna(1.0).to_numpy())[0]                     # aile = 125 satır; ölçülemeyen satır p = 1
        def gecti(r):
            yil = json.loads(r.i_yil) if isinstance(r.i_yil, str) else {}
            ayni = np.isfinite(r.i_d) and np.sign(r.i_d) == np.sign(r.kesif_d); etki = abs(r.i_d) >= ESIKLER["ic_d"] if np.isfinite(r.i_d) else False
            ci = (r.i_d_alt > 0 or r.i_d_ust < 0) if np.isfinite(r.i_d_alt) else False; au = abs(r.i_auc - 0.5) >= ESIKLER["ic_auc"] if np.isfinite(r.i_auc) else False
            yl = all(v == np.sign(r.kesif_d) for v in yil.values()) and len(yil) >= 1
            return bool(ayni and etki and ci and au and yl and r.q_bh <= ESIKLER["ic_q"])
        S["b1_gecti"] = S.apply(gecti, axis=1)
    agg = {"satir": ("ufuk", "size"), "a1": ("sinif_a1", lambda s: hucre_karari(list(s))), "a1_iii": ("sinif_iii", lambda s: hucre_karari(list(s))), "iii_farkli": ("iii_farkli", "sum")}
    if "b1_gecti" in S:
        agg["b1_gecen"] = ("b1_gecti", "sum")
    H = S.groupby("hucre").agg(**agg).reset_index()
    if "b1_gecti" in S:
        H["b1_durum"] = np.where(H.b1_gecen > H.satir / 2, "DOĞRULAMA BEKLİYOR (A, ilk geçiş)", "İÇ'TE TUTMADI (A, ilk geçiş)")
    Bl = bilesim(P, V, O, J, cikmap, donem) if not yalniz_a1 else pd.DataFrame()
    return {"S": S, "H": H, "B3": B3, "Bl": Bl, "evren_surum": VERI["evren_surum"], "olay_orani": {u: float(olay[u].sum() / max(1, (P.likit & (P[f"donem{h}"] == donem)).sum()))
                                                                                                    for u, h in (("Y60", 60), ("Y120", 120), ("Y250", 250))}, "sure_dk": round((time.time() - t0) / 60, 1)}
