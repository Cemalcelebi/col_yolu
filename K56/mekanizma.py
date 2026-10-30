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


# ---------------------------------------------------------------- kanıt sınıfları (ONKAYIT_K56 3) ve mekanizma hipotez kaydı (ONKAYIT_K56 4)
KANIT_SINIFLARI: Tuple[str, ...] = ("DOĞRULANMIŞ MEKANİZMA", "GÜÇLÜ AÇIKLAMA", "ALTERNATİF AÇIKLAMA", "İLİŞKİ VAR, NEDEN BELİRSİZ", "VERİ YETERSİZ", "YANLIŞ BULGU")
ETKI_YOK = "ETKİ YOK (başarısız kalır; açıklanacak etki yok)"
YONTEM_DENETIMI = "YÖNTEM DENETİMİ (bulgu değil)"

# Her hipotez: kimlik, ad, açıklama, hangi bulguları açıklar (kimlik desenleri, düzenli ifade), doğruysa / yanlışsa bağımsız veride ne görülmeli,
# gerekli veri (veri modülü kaynak kimlikleri), karşıt gruplar (karsit_ornekler.GRUPLAR), ölçü, çürütme ölçütü (önceden; sonuçla değişmez),
# öncelik (1 = önce), yarışan hipotezler. Sürüm: v1.1 kilidiyle donar (Faz 1 öncesi).
HIPOTEZLER: List[Dict[str, Any]] = [
    {"kimlik": "M01", "ad": "Olay başlangıcı seçim etkisi (mekanik eser)", "tur": "yontem",
     "aciklama": "Olay günü t0 = ileri pencerenin eşiği İLK yakaladığı gün ve giriş t0+1 açılışı; etiket giriş fiyatına göre tanımlandığından t0 öncesi düşüş, zayıf kapanış, negatif göreli güç TANIM GEREĞİ seçilir. Bilgi yok.",
     "aciklar": [r"^K55-D\d\d-S\d\d$"], "dogruysa": "bilgisiz yapay veride aynı tanım + aynı kod gerçek d'nin >= %50'sini aynı işaretle üretir; etki t0−k gecikmesiyle hızla söner (k=5'te <= 1/3); seçimsiz ileri ölçüde (K55 B) etki yok",
     "yanlissa": "yapay veride |d| < 0,05; gerçek veride etki gecikmeyle sönmez; B ileri getiride iz verir", "veri": ["YEREL_K55_PANEL", "SENTETIK"], "karsit": ["G1", "G7"],
     "olcu": "d_sentetik / d_gerçek (Y60); gecikme 0/1/5/20 sönümü (gerçek ve sentetik)", "curutme": "ONKAYIT_K56 6 eşikleri; gerçek veride k=5'te |d| >= 0,7 × |d(k=0)| -> M01 tek başına açıklamaz",
     "oncelik": 1, "yarisan": ["M02", "M03"], "faz0": "SENTETİK SINAMA YAPILDI (K56_SECIM_SENTETIK_OZET.csv)"},
    {"kimlik": "M02", "ad": "Kısa dönem tersine dönüş / likidite sağlama (gerçek fiyat baskısı)", "tur": "piyasa",
     "aciklama": "Bilgisiz satış baskısı fiyatı geçici iter, likidite sağlayan alıcı primle karşılar; dönüş likiditesi düşük hisselerde büyük olur (Jegadeesh 1990, Nagel 2012).",
     "aciklar": [r"^K55-D0[1256]-", r"^K53-T", r"^K51-.*(CEK|ÇEK|H-A)"], "dogruysa": "M01 gecikme denetiminden sonra kalan ters etki yüksek spread / düşük derinlik (Corwin-Schultz, MIDAS gizli emir ve tek lot altı payı) grubunda büyük; 8-K haberi yok; seçimsiz ileri getiride (sinyal günü sabit) zayıf kapanışlı hisseler pozitif 5-20 gün getirisi verir",
     "yanlissa": "kalan etki likiditeyle değişmez ya da ileri getiri sıfır (K55 B 0/164 bunun 60 gün için ön kanıtı)", "veri": ["OHLC_SPREAD_VEKIL", "SEC_MIDAS", "FINRA_REGSHO", "SEC_SUBMISSIONS_OZET"],
     "karsit": ["G2", "G7"], "olcu": "ileri 5 / 20 gün eşli fark × spread üçlüsü; etkileşim katsayısı ve ay kümeli aralık", "curutme": "yüksek spread üçlüsünde 20 gün eşli fark aralığı 0'ı kapsıyor", "oncelik": 2,
     "yarisan": ["M01", "M04"], "faz0": "veri erişimi: spread vekili yerel, MIDAS 2012+, Reg SHO 2018-08+"},
    {"kimlik": "M03", "ad": "Oynaklık / risk seçimi (oynaklık ondalığı denetimi yetersiz)", "tur": "yontem",
     "aciklama": "Büyük yükseliş eşiği oynak hisselerde ve oynaklığın arttığı dönemlerde kolay aşılır; gün içi 60 gün oynaklık ondalığı koşullu (GARCH) oynaklığı ve ondalık içi farkı denetlemez.",
     "aciklar": [r"^K55-D03-", r"^K55-D0[1-6]-", r"^K51-.*OYNAK"], "dogruysa": "yalnız GARCH'lı yapay evrende mekanik iz (BELİRSİZ hücreler); ince oynaklık denetimi (yüzdelik, koşullu oynaklık, beta) gerçek d'yi >= %50 küçültür",
     "yanlissa": "ince denetim d'yi değiştirmez", "veri": ["YEREL_K55_PANEL"], "karsit": ["G2", "G7"], "olcu": "d (vd 10'luk) − d (oynaklık yüzdeliği 50'lik + GARCH koşullu oynaklık)",
     "curutme": "küçülme < %25", "oncelik": 1, "yarisan": ["M01"], "faz0": "sentetik: 4 KEŞİF hücresi yalnız GARCH spekinde mekanik (BELİRSİZ)"},
    {"kimlik": "M04", "ad": "Haber / bilanço / kurumsal olay kaynaklı sıçrama", "tur": "sirket",
     "aciklama": "Büyük yükselişler çoğunlukla ayrık bir habere (bilanço 8-K 2.02, sözleşme 1.01, FDA / ürün 7.01-8.01, birleşme) bağlı; olay öncesi zayıflık tesadüf ya da haber öncesi belirsizlik.",
     "aciklar": [r"^K55-", r"^K53-", r"^K52-"], "dogruysa": "G1 olaylarının G2'den belirgin büyük payında [t0−5, t0+10] içinde 8-K var (madde koduyla); haber türüne koşullu iken olay öncesi fark küçülür",
     "yanlissa": "8-K sıklığı G1 ve G2'de aynı", "veri": ["SEC_SUBMISSIONS_OZET"], "karsit": ["G2", "G7"], "olcu": "8-K (madde) payı farkı G1 − G2, ay kümeli aralık; haber türü dağılımı",
     "curutme": "fark aralığı 0'ı kapsıyor", "oncelik": 1, "yarisan": ["M02", "M15"], "faz0": "veri yerel (sec_ozet: 8-K madde kodu dolu pay 1,0); indirme yok"},
    {"kimlik": "M05", "ad": "Açığa satış sıkışması", "tur": "yatirimci",
     "aciklama": "Açığa satış pozisyonu yüksek, fiyatı düşmüş hisselerde kapatma alımları ani yükseliş üretir (tema / meme dönemleri).",
     "aciklar": [r"^K51-.*(KR|KAZANAN|EN20)", r"^K55-D0[156]-", r"^K52-KIR-EN20"], "dogruysa": "G1'de t0 öncesi açığa satış / dolaşım ve kapatma gün sayısı G2'den yüksek; t0 sonrası pozisyon düşer; FTD artar",
     "yanlissa": "açığa satış ölçüleri G1 ve G2'de aynı", "veri": ["FINRA_SI", "FINRA_REGSHO", "SEC_FTD"], "karsit": ["G2", "G4"], "olcu": "kapatma gün sayısı ve SI değişimi farkı; FTD payı",
     "curutme": "fark aralığı 0'ı kapsıyor", "oncelik": 2, "yarisan": ["M18", "M02"], "faz0": "KAPSAM: FINRA SI API ~2017-12+, Reg SHO CDN 2018-08+ -> KEŞİF'in yalnız 2018-21'i; FTD 2004+"},
    {"kimlik": "M06", "ad": "Sulandırma / finansman döngüsü (hisse ihracı)", "tur": "sermaye",
     "aciklama": "Nakit ihtiyacı olan şirketler zayıf fiyatta ya da yükselişe satarak (ATM, 424B5, S-3, 8-K 3.02) hisse çıkarır; sayı artışı dağıtımdır (şirket satıcı).",
     "aciklar": [r"^K51-.*(KAYNAK|TIINGO|BATAN)", r"^K55-D02-", r"^K54-"], "dogruysa": "G5 (12 ayda > %20 hisse artışı) ve ihraç başvurusu G4 / G3'te ve G1'in olay SONRASI penceresinde sık; G1 olay öncesinde değil",
     "yanlissa": "ihraç sıklığı gruplar arasında aynı", "veri": ["SEC_COMPANYFACTS", "SEC_SUBMISSIONS_OZET"], "karsit": ["G1", "G3", "G4", "G5"], "olcu": "olay öncesi / sonrası ihraç ve hisse artışı payı farkı",
     "curutme": "fark aralığı 0'ı kapsıyor", "oncelik": 2, "yarisan": ["M07"], "faz0": "XBRL hisse sayısı bölünmeye göre düzeltilmemiş (TRMB, TLGTQ sıçramaları): bölünme verisiyle düzeltme şart"},
    {"kimlik": "M07", "ad": "Temel iyileşme / bozulma", "tur": "sirket",
     "aciklama": "Satış, faaliyet nakit akışı ya da kârdaki değişim yükselişi açıklar; fiyat bilgiyi bildirim tarihinde (filed) alır.",
     "aciklar": [r"^K55-", r"^K51-.*(H-B|H-D)"], "dogruysa": "G1'de t0 sonrası ilk bildirimde (filed) satış / FNA iyileşmesi G2'den büyük; t0 öncesi bildirimlerde fark yok",
     "yanlissa": "temel değişim farkı yok", "veri": ["SEC_COMPANYFACTS", "SEC_FS_DS"], "karsit": ["G2", "G3"], "olcu": "bildirim tarihine göre çeyrek değişimi farkı (ay kümeli aralık)", "curutme": "aralık 0'ı kapsıyor",
     "oncelik": 2, "yarisan": ["M04"], "faz0": "companyfacts 12/12 indi; yabancı ihraççı (IFRS) ve CIK değişimi boşluk bırakıyor"},
    {"kimlik": "M08", "ad": "Kurumsal birikim (13F pozisyon artışı)", "tur": "yatirimci",
     "aciklama": "Büyük yöneticiler sıkışma / dip döneminde pozisyon büyütür; fiyat sonra yükselir (Çöl Yolu 'birikim' anlatısı).",
     "aciklar": [r"^K51-H(1|2|3)$", r"^K51-.*P1", r"^K55-D02-"], "dogruysa": "olay ya da P1 öncesi çeyrekte (bildirim tarihine göre) kurumsal sahiplik payı ve sahip sayısı artışı G1'de G2'den büyük",
     "yanlissa": "artış farkı yok ya da sonra geliyor", "veri": ["SEC_13F_DS", "OPENFIGI"], "karsit": ["G2", "G7"], "olcu": "Δ kurumsal pay (13F toplam hisse / dolaşım), Δ sahip sayısı", "curutme": "fark aralığı 0'ı kapsıyor",
     "oncelik": 2, "yarisan": ["M11"], "faz0": "13F 2013q2+, KEŞİF ~1,1 GB; CUSIP -> sembol OpenFIGI 9/10 (süzgeç gerekli); 45 gün gecikme"},
    {"kimlik": "M09", "ad": "Kurumsal / içeriden dağıtım (pozisyon azaltma)", "tur": "yatirimci",
     "aciklama": "Düşüş ve 'yüksek hacimli düşüş' içeriden / kurumsal satışın izidir; yükselmeyenlerde (G2, G4) daha sık beklenir.",
     "aciklar": [r"^K53-", r"^K55-D02-S02", r"^K55-D05-"], "dogruysa": "plansız (10b5-1 dışı) içeriden S ve 13F azaltımı G4'te ve G2'de G1'den sık",
     "yanlissa": "fark yok", "veri": ["SEC_INSIDER_DS", "SEC_13F_DS"], "karsit": ["G1", "G2", "G4"], "olcu": "plansız S sayısı / değeri, 13F azaltım payı", "curutme": "aralık 0'ı kapsıyor", "oncelik": 2,
     "yarisan": ["M11", "M02"], "faz0": "Form 4 2006q1+; KEŞİF 248 MB; 10b5-1 işareti yalnız 2023+ (öncesi dipnot %2,7)"},
    {"kimlik": "M10", "ad": "İçeriden bilgi (açık piyasa alımı)", "tur": "yatirimci",
     "aciklama": "Yöneticilerin kendi parasıyla açık piyasa alımı (P) bilgi taşır; yükseliş öncesi sıklaşır.",
     "aciklar": [r"^K55-", r"^K51-.*P1"], "dogruysa": "t0 öncesi 90 günde P alımı G1'de G2'den sık", "yanlissa": "fark yok", "veri": ["SEC_INSIDER_DS", "K30_ALIM"], "karsit": ["G2", "G7"],
     "olcu": "P alımı olan hisse payı farkı", "curutme": "aralık 0'ı kapsıyor", "oncelik": 3, "yarisan": ["M07"], "faz0": "K30 (Ç102) daha önce ölçtü: yeniden yapılmaz, yalnız K55 olaylarına eşlenir"},
    {"kimlik": "M11", "ad": "Emilim (büyük satışın başka alıcılarca karşılanması)", "tur": "yatirimci",
     "aciklama": "Yüksek hacimli satış günlerinde fiyat az düşer çünkü büyük alıcı (kurum, blok) karşılar; olumlu habere tepkisizlik (K53) de emilim olabilir.",
     "aciklar": [r"^K53-", r"^K55-D02-S0[2-8]", r"^K55-D05-S0[68]"], "dogruysa": "satış baskılı günlerde işlem başına hacim (MIDAS TradeVol / Trades) ve gizli / ATS payı artar; aynı çeyrekte 13F sahip sayısı ya da 13D / 13G başvurusu artar; fiyat etkisi (Amihud) düşer",
     "yanlissa": "işlem büyüklüğü ve kurumsal sahiplik değişmez (o zaman dağıtım ya da likidite)", "veri": ["SEC_MIDAS", "SEC_13F_DS", "SEC_SUBMISSIONS_OZET", "FINRA_ATS"], "karsit": ["G2", "G4"],
     "olcu": "MIDAS işlem büyüklüğü ve gizli pay farkı; 13F Δ sahip sayısı", "curutme": "fark aralığı 0'ı kapsıyor", "oncelik": 2, "yarisan": ["M09", "M12"],
     "faz0": "MIDAS günlük hisse × borsa 2012+ (çeyrek ~87 MB); FINRA ATS genel API yakın geçmiş (KEŞİF yok)"},
    {"kimlik": "M12", "ad": "Likidite / piyasa derinliği değişimi", "tur": "piyasa",
     "aciklama": "Spread ve derinlik değişimi fiyat tepkisini değiştirir; düşük derinlik hem sert düşüş hem sert yükseliş üretir.",
     "aciklar": [r"^K55-D02-S03", r"^K55-D05-", r"^K51-.*LIKIDITE"], "dogruysa": "olay öncesi spread / Amihud / iptal-işlem oranı G1'de G2'den farklı ve bu fark olay öncesi farkı açıklar",
     "yanlissa": "fark yok", "veri": ["OHLC_SPREAD_VEKIL", "SEC_MIDAS"], "karsit": ["G2", "G7"], "olcu": "spread / derinlik farkı ve aracılık payı", "curutme": "aracılık < %25 ve fark aralığı 0'ı kapsıyor",
     "oncelik": 3, "yarisan": ["M02", "M11"], "faz0": "spread vekili yerel (dolu pay 0,99); MIDAS erişilebilir"},
    {"kimlik": "M13", "ad": "Veri / fiyat düzeltmesi / evren kaynaklı yanlış görüntü", "tur": "veri",
     "aciklama": "Bölünme / ters bölünme düzeltme hatası, sembol yeniden kullanımı, sağlayıcı farkı ve hayatta kalanlardan oluşan evren yapay etki ya da yapay olay üretir.",
     "aciklar": [r"^K54-", r"^K55-F0-", r"^K51-.*(KAYNAK|V\d|DEN)"], "dogruysa": "etki sağlayıcıya göre işaret değiştirir (K51 P1: V_ABD +, Tiingo −); olay günleri bölünme / sembol değişimi tarihlerine yığılır; ikinci sağlayıcı (Tiingo) sıçramayı doğrulamaz",
     "yanlissa": "etki sağlayıcıdan bağımsız; olaylar bölünme tarihlerinden bağımsız", "veri": ["YAHOO_SPLITS", "SEC_SUBMISSIONS_OZET", "TIINGO_BATAN"], "karsit": ["G3", "G6"],
     "olcu": "kaynak × etki etkileşimi; bölünme ±3 gün çakışma payı", "curutme": "etkileşim aralığı 0'ı kapsıyor ve çakışma payı taban kadar", "oncelik": 1, "yarisan": ["M17"],
     "faz0": "V_ABD bölünme günlerinde düzeltilmiş (AAPL / TSLA / NVDA gece oranı ~1); XBRL hisse sayısı düzeltilmemiş"},
    {"kimlik": "M14", "ad": "Kasıtlı yanıltma (manipülasyon / pompala-boşalt)", "tur": "kasit",
     "aciklama": "Fiyat / hacim kasıtlı olarak yanıltıcı gösterilir. Varsayılan açıklama DEĞİL; yalnız resmî kayıtla (SEC askıya alma, dava, idari karar, mahkeme, FINRA disiplin) desteklenir.",
     "aciklar": [r"^K51-.*(KR|KAZANAN|EN20)", r"^K55-"], "dogruysa": "G1 olaylarının sembol + tarih eşleşmeli resmî kayıtla çakışma payı G2'den büyük", "yanlissa": "çakışma payı aynı ya da sıfır (kasıt kanıtı yok)",
     "veri": ["SEC_ASKIYA_ALMA", "SEC_DAVA"], "karsit": ["G2", "G7"], "olcu": "resmî kayıt çakışma payı; üç sütun: gözlenen davranış / olası mekanizma / kasıt kanıtı", "curutme": "kayıt yok -> KASIT KANITI YOK",
     "oncelik": 3, "yarisan": ["M05", "M18"], "faz0": "SEC askıya alma 1995-2026, 1.349 bülten; sembol yok, ad eşlemesiyle evrende 10 şirket; dava bültenleri sayfalı"},
    {"kimlik": "M15", "ad": "Birleşme / satın alma teklifi", "tur": "sirket",
     "aciklama": "Yükselişin bir kısmı satın alma primi; hedef şirketler çoğu zaman zayıf fiyatlı.",
     "aciklar": [r"^K55-", r"^K54-"], "dogruysa": "G1'in [t0, t0+60] içinde SC TO-T / DEFM14A / 425 / 8-K 1.01-2.01 başvurusu payı G2'den büyük; birleşmeli olaylar çıkarılınca olay öncesi fark küçülür",
     "yanlissa": "pay farkı yok", "veri": ["SEC_SUBMISSIONS_OZET"], "karsit": ["G2", "G6"], "olcu": "birleşme başvurusu payı farkı", "curutme": "aralık 0'ı kapsıyor", "oncelik": 2, "yarisan": ["M04"],
     "faz0": "veri yerel (sec_ozet)"},
    {"kimlik": "M16", "ad": "Toplu piyasa dibi / beta (2020 Mart gibi)", "tur": "piyasa",
     "aciklama": "Olaylar piyasa diplerinde kümelenir; yüksek betalı hisseler önce çok düşer sonra çok yükselir.",
     "aciklar": [r"^K55-D06-", r"^K55-D0[1-5]-"], "dogruysa": "olaylar ay bazında kümelenir; 2020-03..06 çıkarılınca ya da beta denetlenince d küçülür", "yanlissa": "değişmez",
     "veri": ["YEREL_K55_PANEL"], "karsit": ["G7"], "olcu": "dönem dışlama ve beta denetimi duyarlılığı", "curutme": "küçülme < %25", "oncelik": 2, "yarisan": ["M03"], "faz0": "veri yerel"},
    {"kimlik": "M17", "ad": "Hayatta kalma yanlılığı (evren)", "tur": "veri",
     "aciklama": "Evren çoğunlukla bugün işlem görenlerden; düşüp batanlar eksik olduğu için 'düşüş sonrası yükseliş' fazla görünür.",
     "aciklar": [r"^K51-.*(KAYNAK|H9|KR-)", r"^K54-", r"^K55-"], "dogruysa": "batan şirketler eklendikçe ters etki ve P1 artısı küçülür / işaret değiştirir", "yanlissa": "değişmez",
     "veri": ["TIINGO_BATAN", "SEC_SUBMISSIONS_OZET"], "karsit": ["G3"], "olcu": "evren genişletme duyarlılığı", "curutme": "değişim < ölçüm aralığı", "oncelik": 2, "yarisan": ["M13"],
     "faz0": "K54: 266 çıkış / 3.267; eksik batanlar Tiingo kotasıyla (ayda 500) eklenebilir (Cemal kararı)"},
    {"kimlik": "M18", "ad": "Tema / sektör rüzgârı (tema rallisi)", "tur": "piyasa",
     "aciklama": "Yükselişler sektör / tema dalgalarında kümelenir (kripto, yapay zekâ, meme); bireysel hisse belirtisi tema üyeliğinin vekilidir.",
     "aciklar": [r"^K51-.*(KR|SEKTOR|RUZGAR)", r"^K55-D06-", r"^K55-D10-S09"], "dogruysa": "olaylar sektör × hafta kümelenir; sektör × gün sabit etkisiyle olay öncesi fark küçülür",
     "yanlissa": "değişmez", "veri": ["YEREL_K55_PANEL", "SEC_SUBMISSIONS_OZET"], "karsit": ["G7"], "olcu": "sektör × gün sabit etkili d", "curutme": "küçülme < %25", "oncelik": 2, "yarisan": ["M05", "M16"],
     "faz0": "K35-K37 rüzgâr çalışmaları var (Ç108-Ç111)"},
    {"kimlik": "M19", "ad": "Bilgi gecikmesi: analist fiyatı izler", "tur": "bilgi",
     "aciklama": "Olumlu revizyonlar fiyat yükseldikten sonra gelir (izleme); bilgi taşımaz.",
     "aciklar": [r"^K52-", r"^K53-"], "dogruysa": "revizyonların çoğu pencere dibinden >= %10 yükseliş SONRASI (K52 H4 zamanlama payı); revizyon sonrası eşli fark sıfır",
     "yanlissa": "revizyon yükselişten önce gelir ve sonrası pozitif", "veri": ["YEREL_ANALIST"], "karsit": ["G2"], "olcu": "zamanlama payı ve sonrası eşli fark", "curutme": "zamanlama payı < 0,3",
     "oncelik": 3, "yarisan": ["M04"], "faz0": "K52 H4-P2 zamanlama payı 0,504 (ön kanıt)"},
]


def hipotez_tablosu() -> pd.DataFrame:
    T = pd.DataFrame(HIPOTEZLER)
    for c in ("aciklar", "veri", "karsit", "yarisan"):
        T[c] = T[c].map(lambda x: "; ".join(x))
    if T.kimlik.duplicated().any():
        raise RuntimeError("yinelenen hipotez kimliği")
    return T


def bulgu_hipotezleri(kimlik: str) -> List[str]:
    """Bir envanter bulgusunu açıklayabilecek hipotezler (kimlik desenlerinden)."""
    import re
    return [h["kimlik"] for h in HIPOTEZLER if any(re.search(p, kimlik) for p in h["aciklar"])]
