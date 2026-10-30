"""K56 mekanizma: kanıt sınıfları (karar kuralları), mekanizma hipotez kaydı (önceden yazılı tahmin + çürütme ölçütü) ve M01 'olay başlangıcı
seçim etkisi' için sentetik sıfır sınaması (yöntem kalibrasyonu; gerçek evren değil).

Sentetik sıfır sınaması: getirisi tanım gereği öngörülemeyen (sıfır beklenen getirili, ortak piyasa + sektör + özel bileşenli) yapay hisselerde
K55'in KİLİTLİ olay tanımı (K55/olay_tanimlari.sembol_olaylari) ve K55 hücre değişkenleri (K55/dal*.py, aynı fonksiyonlar) aynen uygulanır;
A yöntemi (gün × oynaklık ondalığı içinde z; Cohen d; ay kümeli bootstrap) aynı kodla (K55/hucre._z_gun_vd, K55/istatistik.d_boot_ay) ölçülür.
Yapay veride değişkenlerin geleceğe dair hiçbir bilgisi yoktur; bu yüzden çıkan her d, olay tanımının (t0 = ileri pencerenin eşiği ilk yakaladığı
gün, giriş t0+1 açılışı) ve oynaklık seçiminin mekanik izidir. Gerçek K55 d'siyle oran ONKAYIT_K56 bölüm 6'daki önceden yazılı eşiklerle
sınıflanır. Gecikme sınaması: değişken t0−k'da (k = 1, 5, 20) ölçülürse mekanik iz hızla sönmeli.
"""
from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from .ortak import K56Ayar, KaynakKaydi, log

# ---------------------------------------------------------------- M01 sentetik sınama: ön kayıtlı eşikler (ONKAYIT_K56 6)
SENTETIK_SPEK: Tuple[Tuple[str, int], ...] = (("gauss", 561), ("gauss", 562), ("garch_t", 563), ("garch_t", 564))
SENTETIK_HISSE = 400
SENTETIK_GUN = 1600
SENTETIK_BOOT = 400
GECIKME: Tuple[int, ...] = (0, 1, 5, 20)
MEKANIK_ORAN = 0.50          # d_sentetik / d_gerçek >= 0,50 (aynı işaret, sentetik aralık 0'ı dışlar) -> MEKANİK AÇIKLAR
KISMI_ORAN = 0.20            # 0,20 <= oran < 0,50 -> KISMEN MEKANİK
ANLAMSIZ_D = 0.05            # |d_sentetik| < 0,05 -> mekanik iz yok
SPEK_UYUM = 3                # dört yapay evrenden en az üçü aynı sınıfı vermeli; yoksa BELİRSİZ


def sentetik_veri(n: int, gun: int, tohum: int, tur: str) -> Tuple[Dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    """Sıfır beklenen getirili yapay evren. tur: 'gauss' (sabit oynaklık, normal) | 'garch_t' (GARCH(1,1), t(4) yenilik).
    Getiri = beta × piyasa + sektör + özel; gece / gün içi ayrımı, fitil ve hacim (|getiri| ile ilişkili ama geleceğe bilgisiz).
    Dönüş: V (sembol -> OHLCV), EV (sembol, sektor), endeks (SPY, IWM)."""
    if tur not in ("gauss", "garch_t"):
        raise ValueError(tur)
    rng = np.random.default_rng(tohum); idx = pd.bdate_range("2012-01-02", periods=gun); sm = 0.0095
    m = rng.standard_t(4, gun) / np.sqrt(2) * sm if tur == "garch_t" else rng.normal(0, sm, gun)
    spy = pd.Series(100 * np.exp(np.cumsum(m)), index=idx); iwm = pd.Series(100 * np.exp(np.cumsum(1.15 * m + rng.normal(0, 0.004, gun))), index=idx)
    n_sek = 11; sf = rng.normal(0, 0.006, (n_sek, gun)); V: Dict[str, pd.DataFrame] = {}; ev = []
    for i in range(n):
        yillik = float(np.clip(np.exp(rng.normal(np.log(0.45), 0.5)), 0.15, 1.6)); sd = yillik / np.sqrt(252); beta = rng.uniform(0.5, 1.6); s = i % n_sek
        ozel_var = max(sd ** 2 - (beta * sm) ** 2 - 0.006 ** 2, (0.3 * sd) ** 2)
        if tur == "garch_t":
            a, b = 0.08, 0.90; w = ozel_var * (1 - a - b); h = ozel_var; e = np.empty(gun); zz = rng.standard_t(4, gun) / np.sqrt(2)
            for t in range(gun):
                e[t] = np.sqrt(h) * zz[t]; h = w + a * e[t] ** 2 + b * h
            sig = np.sqrt(np.maximum(pd.Series(e ** 2).ewm(alpha=0.06).mean().to_numpy(), 1e-8))
        else:
            e = rng.normal(0, np.sqrt(ozel_var), gun); sig = np.full(gun, np.sqrt(ozel_var))
        r = beta * m + sf[s] + e; sig_t = np.sqrt(sig ** 2 + (beta * sm) ** 2)
        r_o = rng.normal(0, 0.45, gun) * sig_t; r_o = np.clip(r_o, -np.abs(r) - 3 * sig_t, np.abs(r) + 3 * sig_t)
        C = 50 * np.exp(np.cumsum(r)); onceki = np.r_[50.0, C[:-1]]; O = onceki * np.exp(r_o)
        H = np.maximum(O, C) * np.exp(np.abs(rng.normal(0, 0.6, gun)) * sig_t); L = np.minimum(O, C) * np.exp(-np.abs(rng.normal(0, 0.6, gun)) * sig_t)
        Vol = np.exp(13 + rng.normal(0, 0.8) + 0.6 * np.abs(r) / sig_t + rng.normal(0, 0.35, gun))
        ad = f"S{i:04d}"; V[ad] = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": Vol}, index=idx); ev.append({"sembol": ad, "sektor": f"SEK{s:02d}"})
    return V, pd.DataFrame(ev), pd.DataFrame({"SPY": spy, "IWM": iwm})


def sentetik_panel(V: Dict[str, pd.DataFrame], EV: pd.DataFrame, endeks: pd.DataFrame, min_gun: int = 260) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """K55 paneliyle aynı sütun anlamları (tarih, i, sembol, likit, close, dv20, r60, vol60, log_dv20, dd250, vd, lt, rejim, ay, blok60, donem{h}) ve
    K55 olay tablosu (K55/olay_tanimlari.sembol_olaylari; likit = ilk min_gun sonrası)."""
    from K55.olay_tanimlari import sembol_olaylari
    from K55.ortak import OLAY
    parcalar = []; olay = []; sek = EV.set_index("sembol").sektor.to_dict()
    for s, d in V.items():
        n = len(d); C = d.Close.to_numpy(float); lr = np.r_[np.nan, np.diff(np.log(C))]; likit = np.arange(n) >= min_gun
        rows, _ = sembol_olaylari(s, d, likit); olay += rows
        dv = pd.Series(C * d.Volume.to_numpy(float)).rolling(20, min_periods=10).median().to_numpy()
        P = pd.DataFrame({"tarih": d.index, "i": np.arange(n, dtype=np.int32), "sembol": s, "likit": likit, "close": C, "open": d.Open.to_numpy(float), "dv20": dv,
                          "vol60": pd.Series(lr).rolling(60, min_periods=40).std().to_numpy(), "log_dv20": np.log(np.maximum(dv, 1.0)),
                          "dd250": C / pd.Series(C).rolling(250, min_periods=60).max().to_numpy() - 1, "r60": C / np.r_[np.full(60, np.nan), C[:-60]] - 1,
                          "ar20": (pd.Series(d.High.to_numpy() - d.Low.to_numpy()) / pd.Series(C)).rolling(20).mean().to_numpy(), "sektor": sek.get(s, "bilinmiyor")})
        for ad, (h, _) in OLAY.items():
            P[f"donem{h}"] = np.where(np.arange(n) + h < n, "KESIF", "TANIMSIZ")
        parcalar.append(P[np.arange(n) >= min_gun])
    P = pd.concat(parcalar, ignore_index=True); L = P[P.likit]
    P["vd"] = np.minimum((L.groupby("tarih").vol60.rank(pct=True) * 10).fillna(5).astype(int), 9).astype(np.int8)
    P["lt"] = np.minimum((L.groupby("tarih").log_dv20.rank(pct=True) * 3).fillna(1).astype(int), 2).astype(np.int8)
    sp = endeks["SPY"]; boga = (sp > sp.rolling(200).mean()).reindex(P.tarih.values).fillna(False).to_numpy(); P["rejim"] = np.where(boga, "BOGA", "AYI")
    P["ay"] = P.tarih.dt.to_period("M").astype(str); gunler = np.array(sorted(P.tarih.unique())); P["blok60"] = P.tarih.map(pd.Series(np.arange(len(gunler)) // 60, index=gunler)).astype(np.int32)
    P["donem"] = "KESIF"; P["r60_ileri"] = np.nan; P["r60_tanimli"] = False
    P = P.sort_values(["sembol", "tarih"], kind="stable").reset_index(drop=True)
    O = pd.DataFrame(olay); O["tarih"] = pd.to_datetime(O.tarih); O["donem"] = "KESIF"
    return P, O


def a_d(P: pd.DataFrame, O: pd.DataFrame, x: str, ufuk: str, B: int, rng: np.random.Generator, gecikme: int = 0) -> Dict[str, Any]:
    """K55 A yöntemiyle aynı d: yalnız likit ve ufuk penceresi tanımlı satırlar; z gün × oynaklık ondalığı içinde (K55/hucre._z_gun_vd); ay kümeli
    bootstrap (K55/istatistik.d_boot_ay); AUC. gecikme k > 0: değişken t0−k'daki değeriyle (sembol içinde kaydırma)."""
    from K55.hucre import _z_gun_vd
    from K55.istatistik import auc, d_boot_ay
    from K55.ortak import OLAY
    h = OLAY[ufuk][0]; xs = P[x] if gecikme == 0 else P.groupby("sembol", sort=False)[x].shift(gecikme)
    m = P.likit.to_numpy() & np.isfinite(xs.to_numpy(float)) & (P[f"donem{h}"].to_numpy() == "KESIF")
    D = P.loc[m, ["tarih", "sembol", "vd", "ay"]].copy(); D["_x"] = xs.to_numpy(float)[m]
    Ou = O[O.ufuk == ufuk]; anahtar = set(zip(Ou.sembol, Ou.tarih)); olay = np.fromiter(((s, t) in anahtar for s, t in zip(D.sembol, D.tarih)), bool, len(D))
    if olay.sum() < 30:
        return {"n_olay": int(olay.sum()), "d": np.nan, "d_alt": np.nan, "d_ust": np.nan, "auc": np.nan}
    z = _z_gun_vd(D, "_x"); d, a, b, _ = d_boot_ay(z, olay, D.ay.to_numpy(), B, rng)
    return {"n_olay": int(olay.sum()), "d": d, "d_alt": a, "d_ust": b, "auc": auc(z[olay], z[~olay])}


def k55_hucre_varyantlari(A: K56Ayar, kk: KaynakKaydi) -> pd.DataFrame:
    """K55 hücreleri ve en iyi varyantı (A_en_iyi; yoksa B_en_iyi; yoksa ilk pencere) + gerçek A d'leri (ufuk başına), yön (kayıttan)."""
    from K55.hucreler import HUCRELER
    D = pd.read_csv(kk.oku(os.path.join(A.k55, "K55_HUCRE_SONUC.csv"), "kiyas", "K55 hücre durumları ve en iyi varyant"))
    H = pd.read_csv(kk.oku(os.path.join(A.k55, "K55_VARYANTLAR.csv"), "kiyas", "K55 A yöntemi gerçek d (ufuk başına)"))
    rows = []
    for r in D.itertuples():
        t = HUCRELER.get(r.hucre)
        if t is None:
            continue
        var = next((v for v in (getattr(r, "A_en_iyi", None), getattr(r, "B_en_iyi", None)) if isinstance(v, str) and v), None)
        if var is None:
            p0 = t["pencereler"][0]; var = f"{r.hucre}|{p0 if p0 is not None else 'tek'}"
        g = H[(H.hucre == r.hucre) & (H.varyant == var) & (H.yontem == "A")]
        gercek = {f"d_gercek_{u}": float(g[g.ufuk == u].d.iloc[0]) if (g.ufuk == u).any() else np.nan for u in ("Y60", "Y120", "Y250")}
        rows.append({"hucre": r.hucre, "durum": r.durum, "varyant": var, "yon": t["yon"], **gercek})
    return pd.DataFrame(rows)


def secim_sentetik(A: K56Ayar, kk: KaynakKaydi, hucre_listesi: Optional[List[str]] = None, spekler: Tuple[Tuple[str, int], ...] = SENTETIK_SPEK,
                   n: int = SENTETIK_HISSE, gun: int = SENTETIK_GUN, B: int = SENTETIK_BOOT) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """M01 sentetik sıfır sınaması. Dönüş: (satırlar: hücre × spek × ufuk × gecikme, hücre özeti + sınıf)."""
    from K55 import dal_ortak
    from K55.faz1 import D10_BILESEN, ek_kur, hucreleri_kur
    from K55.hucre import degisken_hesapla
    from K55.hucreler import HUCRELER
    hucreleri_kur(); T = k55_hucre_varyantlari(A, kk)
    if hucre_listesi:
        T = T[T.hucre.isin(hucre_listesi)].reset_index(drop=True)
    satir: List[Dict[str, Any]] = []
    for tur, tohum in spekler:
        t0 = time.time(); V, EV, endeks = sentetik_veri(n, gun, tohum, tur); P, O = sentetik_panel(V, EV, endeks); ek_kur(V, EV, endeks)
        for kb, p in D10_BILESEN:
            if kb in HUCRELER:
                P[kb], _ = degisken_hesapla(P, V, HUCRELER[kb], p, kb)
        rng = np.random.default_rng(tohum + 1000)
        log.info("sentetik %s/%d: %d hisse, panel %d satır, olay %s (%.0f sn)", tur, tohum, len(V), len(P), O.ufuk.value_counts().to_dict(), time.time() - t0)
        for r in T.itertuples():
            p = r.varyant.split("|")[1]; p = None if p == "tek" else int(p)
            try:
                x, _ = degisken_hesapla(P, V, HUCRELER[r.hucre], p, r.varyant)
            except Exception as ex:
                satir.append({"hucre": r.hucre, "varyant": r.varyant, "spek": tur, "tohum": tohum, "hata": str(ex)[:200]}); continue
            P["_x"] = np.asarray(x, np.float64)
            for uf in ("Y60", "Y120", "Y250"):
                for k in GECIKME:
                    if uf != "Y60" and k:
                        continue
                    satir.append({"hucre": r.hucre, "varyant": r.varyant, "spek": tur, "tohum": tohum, "ufuk": uf, "gecikme": k, "eksik_pay": float(P["_x"].isna().mean()),
                                  **a_d(P, O, "_x", uf, B, rng, k)})
        P.drop(columns=["_x"], inplace=True, errors="ignore"); dal_ortak.EK.clear()
    S = pd.DataFrame(satir)
    return S, sentetik_ozet(S, T)


def sentetik_sinif(d_s: float, alt: float, ust: float, d_g: float) -> str:
    """Tek spek için önceden yazılı sınıf (ONKAYIT_K56 6)."""
    if not np.isfinite(d_s) or not np.isfinite(d_g) or d_g == 0:
        return "TANIMSIZ"
    if abs(d_s) < ANLAMSIZ_D or not (alt > 0 or ust < 0):
        return "MEKANIK_IZ_YOK"
    oran = d_s / d_g
    if oran >= MEKANIK_ORAN:
        return "MEKANIK_ACIKLAR"
    if oran >= KISMI_ORAN:
        return "KISMEN_MEKANIK"
    return "MEKANIK_IZ_YOK" if oran >= 0 else "TERS_ISARET"


def sentetik_ozet(S: pd.DataFrame, T: pd.DataFrame) -> pd.DataFrame:
    """Hücre başına (birincil ufuk Y60, gecikme 0): dört spekin sınıfları, uyum (>= SPEK_UYUM aynı sınıf) ve gecikme sönümü."""
    rows = []
    if not len(S) or "ufuk" not in S:
        return pd.DataFrame()
    for r in T.itertuples():
        g = S[(S.hucre == r.hucre) & (S.ufuk == "Y60")]
        g0 = g[g.gecikme == 0]; sinif = [sentetik_sinif(x.d, x.d_alt, x.d_ust, r.d_gercek_Y60) for x in g0.itertuples()]
        say = pd.Series(sinif).value_counts() if sinif else pd.Series(dtype=int); ust = say.index[0] if len(say) else "TANIMSIZ"
        karar = ust if (len(say) and say.iloc[0] >= SPEK_UYUM) else "BELIRSIZ"
        gec = {f"d_sent_gecikme{k}": float(g[g.gecikme == k].d.mean()) if (g.gecikme == k).any() else np.nan for k in GECIKME}
        uz = {f"d_sent_{u}": float(S[(S.hucre == r.hucre) & (S.ufuk == u) & (S.gecikme == 0)].d.mean()) for u in ("Y120", "Y250")}
        d_s = float(g0.d.mean()) if len(g0) else np.nan
        rows.append({"hucre": r.hucre, "durum_k55": r.durum, "varyant": r.varyant, "yon": r.yon, "d_gercek_Y60": r.d_gercek_Y60, "d_sent_Y60": d_s,
                     "oran_Y60": d_s / r.d_gercek_Y60 if (np.isfinite(d_s) and np.isfinite(r.d_gercek_Y60) and r.d_gercek_Y60) else np.nan,
                     "d_sent_alt_min": float(g0.d_alt.min()) if len(g0) else np.nan, "d_sent_ust_max": float(g0.d_ust.max()) if len(g0) else np.nan,
                     "spek_siniflari": ";".join(sinif), "karar": karar, **gec, "d_gercek_Y120": r.d_gercek_Y120, "d_gercek_Y250": r.d_gercek_Y250, **uz})
    return pd.DataFrame(rows)
