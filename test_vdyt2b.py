"""VDYT2-B testleri — YALNIZ SENTETİK veri (ağ yok; Tiingo'ya istek yok; sahte istemci). Çalıştırma: python test_vdyt2b.py

1) MA1 / MA2 / MA3 elle hesap; vektörel = döngülü; kopukluk / veri sonu NaN  2) GELECEĞE BAKMAZ: σ ve ATR250 yalnız t ve öncesinden (t sonrası bozulunca eşik
aynı; t+20 sonrası bozulunca etiket aynı)  3) hizalama denetimi (yanlış seri -> dur)  4) ağırlıklı oran: ağırlık 1 iken V2.v2_oran_karsilastir ile birebir;
elle ağırlıklı ortalama  5) karar hücresi kuralları  6) evren kuralları (kod, yinelenen, k60, BORSA, OTCQ, ayrık OTC, SPAC birimi)  7) dağıtım ve örneklem
tohumla birebir (aynı tohum aynı liste; başka tohum başka)  8) hız sınırı sayacı (saatte 45, günde 900, ayda 500 farklı sembol; kalıcı; sahte saat ve sahte
istemci) ve önbellek (ikinci çağrıda istek yok)  9) anahtar loga / dosyaya / hata metnine yazılmaz; URL'de yok  10) Tiingo bölünme düzeltmesi elle; SPAC
kalıbı (D2); kod değişikliği (D4)  11) pilot ölçütleri ve pilot kararı  12) yedek planı  13) ret kapısı (ön kayıt yok / işlenmemiş / mühür / kod / tablo /
liste / VDYT2 kodu; git'e işlenince geçer; sonra değişince ret) ve ön kaydın git'teyken üzerine yazılmaması  14) uçtan uca sentetik: A (VDYT2 tabloları ->
MA etiketleri -> kapsam yalnız sayar -> analiz -> karar) ve B (batan satırları VDYT2 koduyla; birleşik ağırlıklı karar)  15) çakışma kapısı  16) VDYT2.py /
VDYT.py değişmedi (sha256 VDYT2 ön kaydıyla aynı); kodda anahtar / e-posta yok.
"""
from __future__ import annotations

import copy
import io
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import VDYT as V1  # noqa: E402
import VDYT2 as V2  # noqa: E402
import VDYT2B as V  # noqa: E402
import test_vdyt2 as T2  # noqa: E402  (sentetik pazar üretici; yalnız okunur)

E0 = V.VDYT2B_ESIK
GIZLI = "GIZLI_ANAHTAR_7f3a9c"


def kucuk_E() -> dict:
    E = copy.deepcopy(E0); E["basari"]["bootstrap"] = 200
    return E


def durmali(fn, mesaj: str, hata: list, icerik: str = "") -> None:
    try:
        fn()
    except (V.Vdyt2bHata, V2.Vdyt2Hata, V1.VdytHata, RuntimeError) as ex:
        if icerik and icerik not in str(ex):
            hata.append(f"{mesaj} (yanlış neden: {ex})")
        return
    hata.append(mesaj)


class Yanit:
    def __init__(self, kod: int, veri) -> None:
        self.status_code = kod; self._v = veri

    def json(self):
        return self._v


class SahteOturum:
    """Tiingo yerine: çağrıları kaydeder; kod -> (HTTP, satırlar). Hata kodu 'PATLA' ise anahtar içeren istisna fırlatır."""

    def __init__(self, veri: dict) -> None:
        self.veri = veri; self.cagri = []

    def get(self, url, params=None, headers=None, timeout=None):
        self.cagri.append({"url": url, "params": dict(params or {}), "headers": dict(headers or {})})
        kod = url.rstrip("/").split("/")[-2]
        if kod == "PATLA":
            raise ConnectionError(f"bağlantı koptu; başlık {headers}")
        if kod not in self.veri:
            return Yanit(404, {"detail": "not found"})
        return Yanit(200, self.veri[kod])


class Saat:
    def __init__(self, t0: float = 1_790_000_000.0) -> None:
        self.t = t0

    def __call__(self) -> float:
        return self.t

    def uyu(self, s: float) -> None:
        self.t += float(s)


def tiingo_satir(gunler, c, sf=None, v=1e6):
    sf = sf if sf is not None else np.ones(len(gunler))
    return [{"date": f"{g.date()}T00:00:00.000Z", "open": float(x), "high": float(x) * 1.01, "low": float(x) * 0.99, "close": float(x), "volume": float(v),
             "adjClose": float(x), "divCash": 0.0, "splitFactor": float(s)} for g, x, s in zip(gunler, c, sf)]


def git(kl: str, *a: str) -> str:
    return subprocess.run(["git", "-C", kl, "-c", "user.name=vdyt2b", "-c", "user.email=vdyt2b@test.invalid"] + list(a), capture_output=True, text=True,
                          check=True).stdout


def testler() -> list:
    hata: list = []
    E = E0; H = int(E["A"]["ufuk"])
    td0 = tempfile.mkdtemp(prefix="vdyt2b_test_")
    V.VDYT2B_YOL["ara"] = os.path.join(td0, "ara")          # gerçek sayaç / önbellek hiç kullanılmaz
    # ---------------------------------------------------------------- 1) MA etiketleri elle
    n = 320; r = np.where(np.arange(n) % 2 == 0, 0.01, -0.01); r[0] = 0.0; t = 280
    r[t + 1:] = 0.008
    c = 100 * np.exp(np.cumsum(r)); tr = np.full(n, 1.0); tr[t + 5] = 3.5; kop = np.zeros(n, bool)
    M = V.v2b_ma_etiket(np.array([t]), c, tr, kop, E)
    lr = np.diff(np.log(c))[t - 250: t]; s_el = float(np.std(lr, ddof=1)); e1 = max(np.log(1.15), 3 * s_el * np.sqrt(H))
    k_el = int(np.ceil(e1 / 0.008 - 1e-12))
    if abs(M["sigma"][0] - s_el) > 1e-12:
        hata.append(f"1) σ elle tutmadı ({M['sigma'][0]} != {s_el})")
    if not (M["ma1"][0] == 1 and M["ma1_yon"][0] == 1 and M["ma1_k"][0] == k_el):
        hata.append(f"1) MA1 elle tutmadı (ma1 {M['ma1'][0]}, k {M['ma1_k'][0]} != {k_el})")
    if not (M["ma2"][0] == 1 and M["ma2_yon"][0] == 1):
        hata.append("1) MA2 elle tutmadı (uç nokta 0,16 >= 2σ√20)")
    if not (M["ma3"][0] == 1 and M["ma3_yon"][0] == 1):
        hata.append("1) MA3 elle tutmadı (t+5 TR 3,5 >= 3 x ATR250 = 3,0)")
    c2 = c.copy(); c2[t + 1:] = c[t] * np.exp(-0.005 * np.arange(1, n - t))   # yavaş düşüş: MA1 yok (0,10 < 0,14), MA2 var (0,10 >= 0,09)
    M2 = V.v2b_ma_etiket(np.array([t]), c2, np.full(n, 1.0), kop, E)
    if not (M2["ma1"][0] == 0 and M2["ma1_yon"][0] == 0 and M2["ma2"][0] == 1 and M2["ma2_yon"][0] == -1 and M2["ma3"][0] == 0):
        hata.append(f"1) aşağı / eşik altı durum tutmadı ({ {k: M2[k][0] for k in ('ma1', 'ma2', 'ma2_yon', 'ma3')} })")
    kop2 = kop.copy(); kop2[t + 7] = True
    if not np.isnan(V.v2b_ma_etiket(np.array([t]), c, tr, kop2, E)["ma1"][0]):
        hata.append("1) (t, t+20] kopukluğunda MA1 NaN değil")
    if not np.isnan(V.v2b_ma_etiket(np.array([n - 10]), c, tr, kop, E)["ma1"][0]) or not np.isnan(V.v2b_ma_etiket(np.array([150]), c, tr, kop, E)["ma1"][0]):
        hata.append("1) veri sonu / σ geçmişi yetersizken MA1 NaN değil")
    rng = np.random.default_rng(3); rr_ = rng.normal(0, 0.02, 900); m_ = rng.random(900) < 0.03; rr_[m_] += rng.choice([-0.25, 0.25], int(m_.sum()))
    cr = 50 * np.exp(np.cumsum(rr_)); trr = np.abs(rng.normal(1, 0.6, 900)); trr[rng.random(900) < 0.02] = 4.0; kr = rng.random(900) < 0.003
    ts = np.arange(200, 900); Mv = V.v2b_ma_etiket(ts, cr, trr, kr, E); fark = 0
    for i, tt in enumerate(ts.tolist()):
        m1 = V.v2b_ma_etiket_tek(tt, cr, trr, kr, E)
        for k in ("ma1", "ma1_yon", "ma2", "ma2_yon", "ma3", "ma3_yon"):
            a, b = Mv[k][i], m1[k]
            if not ((np.isnan(a) and np.isnan(b)) or a == b):
                fark += 1
    if fark:
        hata.append(f"1) vektörel MA = döngülü MA tutmadı ({fark} fark)")
    if np.nanmean(Mv["ma1"]) <= 0 or np.nanmean(Mv["ma1"]) >= 1:
        hata.append("1) rastgele seride MA1 tek sınıf (test zayıf)")
    # ---------------------------------------------------------------- 2) geleceğe bakmaz
    cb = cr.copy(); cb[701:] *= np.exp(rng.normal(0, 0.2, 199)); tb = trr.copy(); tb[701:] *= 5
    a = V.v2b_ma_etiket(np.array([700]), cr, trr, kr, E); b = V.v2b_ma_etiket(np.array([700]), cb, tb, kr, E)
    if a["sigma"][0] != b["sigma"][0] or a["atr250"][0] != b["atr250"][0] or a["ma1_esik"][0] != b["ma1_esik"][0]:
        hata.append("2) t sonrası barlar bozulunca σ / ATR250 / eşik değişti (geleceğe bakıyor)")
    cc = cr.copy(); cc[600 + H + 1:] *= 3; tc = trr.copy(); tc[600 + H + 1:] *= 9
    a = V.v2b_ma_etiket(np.array([600]), cr, trr, kr, E); b = V.v2b_ma_etiket(np.array([600]), cc, tc, kr, E)
    if any(not ((np.isnan(a[k][0]) and np.isnan(b[k][0])) or a[k][0] == b[k][0]) for k in ("ma1", "ma2", "ma3", "ma1_yon", "ma3_yon")):
        hata.append("2) t+20 sonrası bozulunca etiket değişti")
    sg = V.v2b_sigma(cr, E); sgb = V.v2b_sigma(np.r_[cr[:500], cr[500:] * 7], E)
    if not np.allclose(sg[:500], sgb[:500], equal_nan=True):
        hata.append("2) σ dizisi geleceğe bakıyor")
    # ---------------------------------------------------------------- 3) hizalama denetimi
    gun = pd.bdate_range("2015-01-01", periods=900)
    d = pd.DataFrame({"o": cr, "h": cr * 1.01, "l": cr * 0.99, "c": cr, "v": 1e6}, index=gun)
    D = pd.DataFrame({"sembol": ["X", "X"], "t": [500, 600], "tarih": [gun[500], gun[600]]})
    Dl = V.v2b_etiketle(D, {"S": {"X": d}}, E)
    if "ma1" not in Dl or len(Dl) != 2:
        hata.append("3) etiketleme sütun / satır eksik")
    durmali(lambda: V.v2b_etiketle(D.assign(tarih=[gun[501], gun[600]]), {"S": {"X": d}}, E), "3) tarih != gün[t] iken durmadı", hata, "hizalama")
    durmali(lambda: V.v2b_etiketle(D.assign(sembol="Y"), {"S": {"X": d}}, E), "3) fiyatı olmayan hissede durmadı", hata, "hizalama")
    # ---------------------------------------------------------------- 4) ağırlıklı oran
    rng = np.random.default_rng(11); m = 3000
    Dg = pd.DataFrame({"sembol": rng.choice(list("ABCDEFGHIJ"), m), "yil": rng.choice([2019, 2020], m), "yas": rng.choice([10, 20], m), "natr_d": rng.integers(0, 3, m)})
    Dg["y"] = (rng.random(m) < 0.3).astype(float); Dk = Dg.sample(frac=1.0, random_state=1).reset_index(drop=True).assign(y=(rng.random(m) < 0.2).astype(float))
    Es = kucuk_E(); Es2 = copy.deepcopy(V2.VDYT2_ESIK); Es2["basari"]["bootstrap"] = 200
    for tab in (["yil", "yas"], ["sembol", "yil", "natr_d"]):
        r1 = V.v2b_oran_karsilastir(Dg, Dk, "y", tab, Es); r2 = V2.v2_oran_karsilastir(Dg, Dk, "y", tab, Es2)
        if any(abs(r1[k] - r2[k]) > 1e-12 for k in ("fark", "alt", "ust", "ort1", "ort0")):
            hata.append(f"4) ağırlık 1 iken V2.v2_oran_karsilastir ile aynı değil ({tab})")
    G = pd.DataFrame({"sembol": ["a", "b", "c", "d"], "yil": [1, 1, 1, 1], "y": [1.0, 0.0, 1.0, 1.0], "w": [1.0, 1.0, 4.0, 4.0]})
    K = pd.DataFrame({"sembol": ["a", "b", "c", "d"], "yil": [1, 1, 1, 1], "y": [0.0, 0.0, 1.0, 0.0], "w": [1.0, 1.0, 4.0, 4.0]})
    r = V.v2b_oran_karsilastir(G, K, "y", ["yil"], Es, agirlik="w")
    if abs(r["ort1"] - 9 / 10) > 1e-12 or abs(r["ort0"] - 4 / 10) > 1e-12:
        hata.append(f"4) ağırlıklı oran elle tutmadı ({r['ort1']}, {r['ort0']})")
    # ---------------------------------------------------------------- 5) karar hücresi
    iyi = {"n1": 100, "n0": 100, "fark": 0.1, "alt": 0.02}; kotu = {"n1": 100, "n0": 100, "fark": 0.1, "alt": -0.01}
    if V.v2b_karar_hucre(iyi, iyi) != "TUTTU" or V.v2b_karar_hucre(iyi, kotu) != "TUTMADI" or V.v2b_karar_hucre({**iyi, "n1": 20}, iyi) != "VERİ YOK":
        hata.append("5) karar hücresi kuralı tutmadı")
    if V.v2b_karar("TUTTU", "TUTTU") != "BAŞARILI" or V.v2b_karar("TUTTU", "TUTMADI") != "BAŞARISIZ" or V.v2b_karar("VERİ YOK", "TUTTU") != "VERİ YOK":
        hata.append("5) birleşik karar kuralı tutmadı")
    # ---------------------------------------------------------------- 6) evren kuralları
    satir = [("AAA", "NYSE", "2015-01-01", "2021-05-01"), ("BBB", "NASDAQ", "2020-12-01", "2021-05-01"),    # BBB ömür < 400 gün
             ("CCCCW", "NASDAQ", "2015-01-01", "2021-05-01"), ("DD-P", "NYSE", "2015-01-01", "2021-05-01"), ("EEE", "NYSE", "2015-01-01", "2021-05-01"),
             ("EEE", "NASDAQ", "2022-01-01", "2026-11-11"), ("FFF", "NYSE", "2015-01-01", "2021-05-01"), ("GGG", "NYSE", "2010-01-01", "2017-05-01"),
             ("HHHQ", "PINK", "1995-01-01", "2026-11-11"), ("IIIQ", "PINK", "2020-07-31", "2022-03-01"), ("III", "NYSE", "2005-01-01", "2020-07-30"),
             ("SPC", "NYSE", "2020-01-01", "2022-06-01"), ("SPC-U", "NYSE", "2019-11-01", "2022-06-01"), ("DSP", "NYSE", "2019-01-01", "2023-06-01"),
             ("DSPU", "NASDAQ", "2018-11-01", "2019-08-01"), ("JJJJQ", "PINK", "2025-08-01", "2026-11-11"), ("KKKY", "PINK", "2010-01-01", "2026-11-11"),
             ("LLLLD", "NASDAQ", "2015-01-01", "2023-01-01"), ("MMMQ", "PINK", "2010-01-01", "2018-06-01")]
    Tl = pd.DataFrame(satir, columns=["ticker", "exchange", "startDate", "endDate"]).assign(assetType="Stock", priceCurrency="USD")
    Tl = pd.concat([Tl, pd.DataFrame([("ZZZ", "NYSE", "2015-01-01", "2021-01-01", "ETF", "USD")], columns=list(Tl.columns))], ignore_index=True)
    Tl["startDate"] = pd.to_datetime(Tl.startDate); Tl["endDate"] = pd.to_datetime(Tl.endDate)
    U, say = V.v2b_evren(Tl, {"FFF"}, E)
    bek = {"AAA", "HHHQ", "DSP", "LLLLD", "III"}
    if set(U.ticker) != bek:
        hata.append(f"6) evren kuralları tutmadı: {sorted(U.ticker)} != {sorted(bek)}")
    if say["4_k60_atilan"] != 1 or say["6_otcq_ayrik_atilan"] != 1 or say["3_yinelenen_kod_atilan_kayit"] != 2 or say["7_spac_kabugu_atilan"]["BORSA"] != 1:
        hata.append(f"6) evren sayımları tutmadı: {say}")
    if set(U[U.kaynak == "OTCQ"].son_yil) != {"OTC_HALA"}:
        hata.append("6) OTC_HALA tabakası tutmadı")
    # ---------------------------------------------------------------- 7) dağıtım ve örneklem tohumu
    dg = V.v2b_dagit({"a": 100, "b": 50, "c": 1, "d": 0}, 30)
    if sum(dg.values()) != 30 or dg["d"] != 0 or dg["c"] != 1 or dg["a"] < dg["b"]:
        hata.append(f"7) dağıtım tutmadı: {dg}")
    if V.v2b_dagit({"a": 3, "b": 2}, 10) != {"a": 3, "b": 2}:
        hata.append("7) n >= evren iken hepsi alınmadı")
    rng = np.random.default_rng(5); Ub = pd.DataFrame({"ticker": [f"T{i:04d}" for i in range(800)], "exchange": "NYSE",
                                                       "startDate": pd.Timestamp("2010-01-01"), "endDate": pd.Timestamp("2021-01-01"),
                                                       "kaynak": rng.choice(["BORSA", "OTCQ"], 800), "son_yil": rng.choice(["2019", "2020", "2021"], 800)})
    Ub["tabaka"] = Ub.kaynak + "|" + Ub.son_yil
    L1 = V.v2b_orneklem(Ub, E); L2 = V.v2b_orneklem(Ub.sample(frac=1.0, random_state=9), E)
    E3 = copy.deepcopy(E); E3["B"]["orneklem"]["tohum"] = 999; L3 = V.v2b_orneklem(Ub, E3)
    if not L1.equals(L2):
        hata.append("7) aynı tohumla örneklem birebir aynı değil (girdi sırasından etkileniyor)")
    if L1.equals(L3) or set(L1[L1.rol == "ANA"].ticker) == set(L3[L3.rol == "ANA"].ticker):
        hata.append("7) başka tohum aynı örneklemi verdi")
    if (L1.rol == "ANA").sum() != 450 or (L1.rol == "YEDEK").sum() != 38 or L1.ticker.duplicated().any():
        hata.append("7) örneklem boyu / tekillik tutmadı")
    w = L1[L1.rol == "ANA"].groupby("tabaka").size(); Nh = Ub.tabaka.value_counts()
    if (abs(w / w.sum() - Nh.reindex(w.index) / Nh.sum()) > 0.01).any():
        hata.append("7) dağıtım orantılı değil")
    # ---------------------------------------------------------------- 8) hız sınırı ve önbellek (sahte saat + sahte istemci)
    os.environ[E["B"]["tiingo"]["anahtar_ortam"]] = GIZLI
    kayit_akisi = io.StringIO(); lh = logging.StreamHandler(kayit_akisi); V.v2blog.addHandler(lh); V.v2blog.setLevel(logging.DEBUG)
    try:
        gunler = pd.bdate_range("2018-01-01", periods=300); veri = {f"K{i:03d}": tiingo_satir(gunler, np.full(300, 10.0 + i)) for i in range(120)}
        saat = Saat(); sy = os.path.join(td0, "sayac.json"); kl = os.path.join(td0, "tiingo")
        ot = SahteOturum(veri); ist = V.TiingoIstemci(E, ot, V.TiingoSayac(sy, E, saat), kl, uyu=saat.uyu)
        zaman = []
        for i in range(120):
            ist.fiyat(f"K{i:03d}"); zaman.append(saat.t)
        zaman = np.array(zaman)
        en_cok_saat = max(int(((zaman > x - 3600) & (zaman <= x)).sum()) for x in zaman)
        if en_cok_saat > 45:
            hata.append(f"8) bir saatte {en_cok_saat} > 45 istek")
        if len(ot.cagri) != 120:
            hata.append("8) istek sayısı tutmadı")
        ist.fiyat("K000")
        if len(ot.cagri) != 120:
            hata.append("8) önbellekteki sembol yeniden istendi")
        say2 = V.TiingoSayac(sy, E, saat)
        if say2.durum()["ay_sembol"] != 120:
            hata.append("8) sayaç kalıcı değil (yeniden açılınca ay sembolü kayboldu)")
        Eg = copy.deepcopy(E); Eg["B"]["tiingo"]["saat_istek"] = 10 ** 6; Eg["B"]["tiingo"]["gun_istek"] = 5
        saat2 = Saat(); ist2 = V.TiingoIstemci(Eg, SahteOturum(veri), V.TiingoSayac(os.path.join(td0, "s2.json"), Eg, saat2), os.path.join(td0, "t2"),
                                               uyu=saat2.uyu)
        z2 = []
        for i in range(12):
            ist2.fiyat(f"K{i:03d}"); z2.append(saat2.t)
        z2 = np.array(z2)
        if max(int(((z2 > x - 86400) & (z2 <= x)).sum()) for x in z2) > 5:
            hata.append("8) günlük sınır aşıldı")
        Ea = copy.deepcopy(E); Ea["B"]["tiingo"]["ay_sembol"] = 3; saat3 = Saat()
        ist3 = V.TiingoIstemci(Ea, SahteOturum(veri), V.TiingoSayac(os.path.join(td0, "s3.json"), Ea, saat3), os.path.join(td0, "t3"), uyu=saat3.uyu)
        for i in range(3):
            ist3.fiyat(f"K{i:03d}")
        durmali(lambda: ist3.fiyat("K050"), "8) ay sembol sınırında durmadı", hata, "ay içinde")
        ist4 = V.TiingoIstemci(E, SahteOturum(veri), V.TiingoSayac(os.path.join(td0, "s4.json"), E, Saat()), os.path.join(td0, "t4"), en_cok_bekle=10.0)
        for i in range(45):
            ist4.fiyat(f"K{i:03d}")
        durmali(lambda: ist4.fiyat("K046"), "8) en_cok_bekle aşılınca durmadı", hata, "hız sınırı")
        if ot.cagri and "startDate" not in ot.cagri[0]["params"]:
            hata.append("8) istek parametreleri eksik")
        # ---------------------------------------------------------------- 9) anahtar sızıntısı
        if not all(c_["headers"].get("Authorization") == f"Token {GIZLI}" for c_ in ot.cagri):
            hata.append("9) başlıkta anahtar yok")
        if any(GIZLI in c_["url"] or GIZLI in json.dumps(c_["params"]) for c_ in ot.cagri):
            hata.append("9) anahtar URL / parametrede")
        x = ist.fiyat("PATLA")
        if x.get("durum") != "hata":
            hata.append("9) istek hatası 'hata' dönmedi")
        if GIZLI in kayit_akisi.getvalue():
            hata.append("9) anahtar loga yazıldı")
        for kok_, _d, dosyalar in os.walk(td0):
            for f in dosyalar:
                try:
                    if GIZLI in open(os.path.join(kok_, f), encoding="utf-8", errors="ignore").read():
                        hata.append(f"9) anahtar dosyaya yazıldı: {f}")
                except OSError:
                    pass
        durmali(lambda: V._v2b_yaz(os.path.join(td0, "x.txt"), f"anahtar {GIZLI}"), "9) anahtarlı metin dosyaya yazıldı", hata, "anahtar")
        del os.environ[E["B"]["tiingo"]["anahtar_ortam"]]
        if V._v2b_anahtar() != "proxy":
            hata.append("9) anahtar yokken 'proxy' kullanılmadı")
        ot5 = SahteOturum(veri); V.TiingoIstemci(E, ot5, V.TiingoSayac(os.path.join(td0, "s5.json"), E, Saat()), os.path.join(td0, "t5")).fiyat("K001")
        if ot5.cagri[0]["headers"].get("Authorization") != "Token proxy":
            hata.append("9) anahtarsız başlık 'Token proxy' değil")
    finally:
        V.v2blog.removeHandler(lh); V.v2blog.setLevel(logging.INFO); os.environ.pop(E["B"]["tiingo"]["anahtar_ortam"], None)
    # ---------------------------------------------------------------- 10) bölünme düzeltmesi, SPAC kalıbı, kod değişikliği
    g = pd.bdate_range("2020-01-01", periods=6); sf = np.array([1, 1, 2, 1, 1, 1.0])
    X = V.v2b_tiingo_df({"durum": "ok", "veri": tiingo_satir(g, [100, 100, 50, 50, 50, 50], sf, v=10)})
    if not (np.allclose(X.Close.to_numpy(), 50.0) and np.allclose(X.Volume.to_numpy(), [20, 20, 10, 10, 10, 10]) and np.allclose(X.rc.to_numpy()[:2], 100)):
        hata.append("10) bölünme düzeltmesi elle tutmadı")
    if V1.vdyt_bolunme_carpan([(g[2], 2.0)], g)[0] * X.Close.iloc[0] != 100.0:
        hata.append("10) ekrandaki fiyat (V1 bölünme çarpanı) ham kapanışa dönmedi")
    gl = pd.bdate_range("2019-01-01", periods=400)
    Lb = pd.DataFrame({"ticker": ["SPX", "OKA", "YOK", "ADD"], "tabaka": ["BORSA|2021"] * 4, "N_h": [40] * 4, "rol": "ANA"})
    kl = os.path.join(td0, "tb"); os.makedirs(kl, exist_ok=True)
    rngb = np.random.default_rng(2)
    k60c = 30 * np.exp(np.cumsum(rngb.normal(0, 0.02, 400)))
    for k, cc_ in (("SPX", 10.0 + rngb.normal(0, 0.05, 400)), ("OKA", 20 * np.exp(np.cumsum(rngb.normal(0, 0.02, 400)))), ("ADD", k60c * 2.0)):
        V._v2b_json(os.path.join(kl, f"{k}.json"), {"durum": "ok", "veri": tiingo_satir(gl, cc_, v=5e5)})
    V._v2b_json(os.path.join(kl, "YOK.json"), {"durum": "yok", "veri": []})
    Fk = {"S": {"LIVE": pd.DataFrame({"o": k60c, "h": k60c * 1.01, "l": k60c * 0.99, "c": k60c, "v": 1e6}, index=gl),
                "OTHER": pd.DataFrame({"o": 5.0, "h": 5.1, "l": 4.9, "c": 5 * np.exp(np.cumsum(rngb.normal(0, 0.02, 400))), "v": 1e6}, index=gl)}}
    Fb, Tb = V.v2b_batan_fiyat(Lb, {"SPX": "ok", "OKA": "ok", "YOK": "yok", "ADD": "ok"}, E, kl, F_k60=Fk)
    Tb = Tb.set_index("ticker")
    if not (Tb.loc["SPX", "spac"] and not Tb.loc["OKA", "spac"] and Tb.loc["YOK", "veri"] == "YOK" and Tb.loc["ADD", "yeniden_ad"] == "LIVE"
            and pd.isna(Tb.loc["OKA", "yeniden_ad"])):
        hata.append(f"10) D1 / D2 / D4 kuralları tutmadı: {Tb[['veri', 'spac', 'yeniden_ad']].to_dict()}")
    if set(Fb["S"]) != {"OKA"} or abs(Tb.loc["OKA", "w"] - 40 / 3) > 1e-12 or not np.isnan(Tb.loc["YOK", "w"]):
        hata.append(f"10) batan F / ağırlık (N_h / m_h = 40 / 3) tutmadı: {Tb.w.to_dict()}")
    # ---------------------------------------------------------------- 11) pilot ölçütleri ve kararı
    S0 = {"kod": "ABCQ", "tur": "Q", "f25": "2023-05-02"}
    g11 = pd.bdate_range("2021-01-01", "2023-09-01", freq=V._v2b_is_gunu())
    r11 = V.v2b_pilot_olc(S0, {"durum": "ok", "http": 200, "veri": tiingo_satir(g11, np.linspace(50, 1, len(g11)))}, E)
    if not (r11["K1_seri"] and r11["K2_son_gun"] and r11["K3_bosluk"] and r11["K5_ohlcv"] and r11["K6_karisma"] and r11["GECTI"] and r11["K4_tutarlilik"] is None):
        hata.append(f"11) Q türü iyi seri geçmedi: {r11}")
    g11b = g11[(g11 < pd.Timestamp("2022-12-01"))]
    if V.v2b_pilot_olc(S0, {"durum": "ok", "http": 200, "veri": tiingo_satir(g11b, np.linspace(50, 1, len(g11b)))}, E)["K2_son_gun"]:
        hata.append("11) borsa dönemi delistingden aylar önce biten Q seri K2'den geçti")
    g11c = g11.delete(slice(len(g11[g11 < pd.Timestamp("2023-01-15")]), len(g11[g11 < pd.Timestamp("2023-01-30")])))
    if V.v2b_pilot_olc(S0, {"durum": "ok", "http": 200, "veri": tiingo_satir(g11c, np.linspace(50, 1, len(g11c)))}, E)["K3_bosluk"]:
        hata.append("11) 10 iş günlük boşluk K3'ten geçti")
    Sb = {"kod": "BRS", "tur": "BORSA", "f25": "2020-08-17"}; gb = pd.bdate_range("2018-01-01", "2020-07-30", freq=V._v2b_is_gunu())
    if not V.v2b_pilot_olc(Sb, {"durum": "ok", "http": 200, "veri": tiingo_satir(gb, np.full(len(gb), 5.0))}, E)["GECTI"]:
        hata.append("11) BORSA türü iyi seri geçmedi")
    gb2 = gb[gb < pd.Timestamp("2020-02-01")]
    if V.v2b_pilot_olc(Sb, {"durum": "ok", "http": 200, "veri": tiingo_satir(gb2, np.full(len(gb2), 5.0))}, E)["K2_son_gun"]:
        hata.append("11) BORSA türünde çok erken biten seri K2'den geçti")
    Sy = {"kod": "REU", "tur": "YENIDEN", "f25": "2020-07-20", "yeni_bas": "2021-02-10"}
    gy = pd.bdate_range("2018-01-01", "2022-06-01", freq=V._v2b_is_gunu())
    ry = V.v2b_pilot_olc(Sy, {"durum": "ok", "http": 200, "veri": tiingo_satir(gy, np.full(len(gy), 5.0))}, E)
    gy2 = gy[(gy < pd.Timestamp("2020-07-01")) | (gy >= pd.Timestamp("2021-02-10"))]
    ry2 = V.v2b_pilot_olc(Sy, {"durum": "ok", "http": 200, "veri": tiingo_satir(gy2, np.full(len(gy2), 5.0))}, E)
    if not ry.get("K6_KARISIK") or ry2.get("K6_KARISIK") or not ry2["GECTI"]:
        hata.append(f"11) kod yeniden kullanımı (karışma) ölçütü tutmadı ({ry.get('K6_ara_is_gunu')}, {ry2.get('K6_ara_is_gunu')})")
    if V.v2b_pilot_olc(S0, {"durum": "yok", "http": 404, "veri": []}, E)["GECTI"]:
        hata.append("11) 404 sembol geçti")
    Sk = {"kod": "SIVBQ", "tur": "Q", "f25": "2023-05-02"}; gk = pd.bdate_range("2021-01-01", "2023-09-01", freq=V._v2b_is_gunu())
    ck_ = np.full(len(gk), 200.0); ck_[gk.get_loc(pd.Timestamp("2023-03-09"))] = 106.0
    if not V.v2b_pilot_olc(Sk, {"durum": "ok", "veri": tiingo_satir(gk, ck_)}, E)["K4_tutarlilik"]:
        hata.append("11) basın kapanışı ±%10 içinde iken K4 tutmadı")
    ck_[gk.get_loc(pd.Timestamp("2023-03-09"))] = 150.0
    if V.v2b_pilot_olc(Sk, {"durum": "ok", "veri": tiingo_satir(gk, ck_)}, E)["GECTI"]:
        hata.append("11) basın kapanışıyla tutarsız seri geçti")

    def pk(gecen, yen_karisik=0, q_hic=False):
        L_ = ([{"kod": f"Y{i}", "tur": "YENIDEN", "K6_KARISIK": i < yen_karisik} for i in range(2)] + [{"kod": f"B{i}", "tur": "BORSA"} for i in range(2)]
              + [{"kod": f"Q{i}", "tur": "Q"} for i in range(8)])
        for i, x_ in enumerate(L_):
            x_["GECTI"] = bool(i < gecen and not (q_hic and x_["tur"] == "Q"))
        return V.v2b_pilot_karar(L_, E)
    if pk(10)["karar"] != "GÜVENİLİR" or pk(9)["karar"] != "KISMEN" or pk(7)["karar"] != "KISMEN" or pk(6)["karar"] != "GÜVENİLMEZ":
        hata.append("11) pilot karar eşikleri tutmadı")
    if pk(12, yen_karisik=2)["karar"] != "KISMEN" or pk(12, yen_karisik=1)["karar"] != "GÜVENİLİR":
        hata.append("11) iki YENIDEN karışıkken karar KISMEN'e inmedi")
    if pk(4, q_hic=True)["otcq_dahil"] or not pk(5)["otcq_dahil"]:
        hata.append("11) Q türünün hiçbiri geçmediğinde OTCQ dahil kaldı")
    # ---------------------------------------------------------------- 12) yedek planı
    Lp = pd.DataFrame({"ticker": ["A1", "A2", "Y1", "Y2", "B1", "YB"], "tabaka": ["a", "a", "a", "a", "b", "b"], "rol": ["ANA", "ANA", "YEDEK", "YEDEK", "ANA", "YEDEK"],
                       "tabaka_sira": [1, 2, 3, 4, 1, 2]})
    if V.v2b_cek_plan(Lp, {}) != ["A1", "A2", "B1"]:
        hata.append("12) ilk plan yalnız ANA değil")
    if V.v2b_cek_plan(Lp, {"A1": "yok", "A2": "ok", "B1": "ok"}) != ["A1", "A2", "B1", "Y1"]:
        hata.append("12) VERİ YOK yerine aynı tabakadan ilk yedek alınmadı")
    if V.v2b_cek_plan(Lp, {"A1": "yok", "A2": "ok", "B1": "ok", "Y1": "yok"}) != ["A1", "A2", "B1", "Y1", "Y2"]:
        hata.append("12) yedek de VERİ YOK iken sıradaki yedek alınmadı")
    if V.v2b_cek_plan(Lp, {"A1": "ok", "A2": "ok", "B1": "ok"}) != ["A1", "A2", "B1"]:
        hata.append("12) veri varken yedek kullanıldı")
    Lq = pd.DataFrame({"ticker": ["A1"] + [f"Y{i}" for i in range(2, 12)], "tabaka": "a", "rol": ["ANA"] + ["YEDEK"] * 10,
                       "tabaka_sira": [str(i) for i in range(1, 12)]})
    if V.v2b_cek_plan(Lq, {"A1": "yok"}) != ["A1", "Y2"]:
        hata.append("12) metin tabaka_sira ile yedek sırası yanlış (sözlük sırası)")
    # ---------------------------------------------------------------- 13) ret kapısı
    td = tempfile.mkdtemp(prefix="vdyt2b_git_"); cik = os.path.join(td, "cikti"); os.makedirs(cik)
    kod_kopya = os.path.join(td, "VDYT2B.py"); shutil.copy(os.path.join(KOK, "VDYT2B.py"), kod_kopya)
    tk = os.path.join(td, "tablo"); os.makedirs(tk)
    eski_kok, eski_tablo = V.KOK_VDYT2B, V.VDYT2B_YOL["tablo"]
    try:
        V.KOK_VDYT2B = td; V.VDYT2B_YOL["tablo"] = tk
        for tur, pz, ad in V.v2b_tablo_listesi(["BIST"])[:2]:
            pd.DataFrame({"a": [1, 2]}).to_csv(os.path.join(tk, f"{tur}_{pz}_{ad}.csv.gz"), index=False)
        git(td, "init", "-q")
        durmali(lambda: V.v2b_onkayit_dogrula(cik, "A", git=False), "13) ön kayıtsız geçti", hata, "ön kayıt yok")
        V._v2b_liste_yaz(V._v2b_yol("liste", cik), pd.DataFrame({"ticker": ["A"]}))
        V.v2b_onkayit(cik)
        V.v2b_onkayit_dogrula(cik, "A", git=False)
        durmali(lambda: V.v2b_onkayit_dogrula(cik, "A", git=True), "13) git'e işlenmemiş ön kayıtla geçti", hata, "işlenmemiş")
        git(td, "add", "-A"); git(td, "commit", "-q", "-m", "on kayit")
        V.v2b_onkayit_dogrula(cik, "A", git=True); V.v2b_onkayit_dogrula(cik, "B", git=True)
        if V.v2b_onkayit(cik) != V._v2b_yol("onkayit", cik):
            hata.append("13) aynı mühürle onkayit yolu döndürmedi")
        Eb = copy.deepcopy(V.VDYT2B_ESIK)
        V.VDYT2B_ESIK["A"]["ufuk"] = 21
        durmali(lambda: V.v2b_onkayit_dogrula(cik, "A", git=False), "13) mühür değişince geçti", hata, "eşik mührü")
        durmali(lambda: V.v2b_onkayit(cik), "13) git'teki ön kaydın üstüne farklı mühürle yazdı", hata, "üzerine yazılmadı")
        V.VDYT2B_ESIK.clear(); V.VDYT2B_ESIK.update(Eb)
        with open(kod_kopya, "a", encoding="utf-8") as f:
            f.write("\n# değişiklik\n")
        durmali(lambda: V.v2b_onkayit_dogrula(cik, "A", git=False), "13) kod değişince geçti", hata, "VDYT2B.py")
        git(td, "checkout", "-q", "--", "VDYT2B.py")
        pd.DataFrame({"a": [1, 3]}).to_csv(os.path.join(tk, os.listdir(tk)[0]), index=False)
        durmali(lambda: V.v2b_onkayit_dogrula(cik, "A", git=False), "13) tablo değişince geçti", hata, "tablo")
        V.v2b_onkayit_dogrula(cik, "B", git=False)
        V._v2b_liste_yaz(V._v2b_yol("liste", cik), pd.DataFrame({"ticker": ["B"]}))
        durmali(lambda: V.v2b_onkayit_dogrula(cik, "B", git=False), "13) liste değişince B geçti", hata, "liste")
        git(td, "checkout", "-q", "--", ".")
        with open(V._v2b_yol("onkayit", cik), "a", encoding="utf-8") as f:
            f.write("\nek satır\n")
        durmali(lambda: V.v2b_onkayit_dogrula(cik, "B", git=True), "13) işlendikten sonra değişen ön kayıtla geçti", hata, "değişmiş")
        git(td, "checkout", "-q", "--", ".")
        oc = V.VDYT2B_ESIK["vdyt2"]["kod_sha"]; V.VDYT2B_ESIK["vdyt2"]["kod_sha"] = "0" * 64
        durmali(lambda: V.v2b_onkayit_dogrula(cik, "A", git=False), "13) VDYT2.py sha256 tutmazken geçti", hata)
        V.VDYT2B_ESIK["vdyt2"]["kod_sha"] = oc
        durmali(lambda: V.v2b_kos("B", cik, 1, git_sart=False), "13) pilot sonucu yokken kos B geçti", hata, "pilot")
        durmali(lambda: V.v2b_cek(cik, istemci=None, git_sart=False), "13) pilot sonucu yokken cek geçti", hata, "pilot")
        V._v2b_json(V._v2b_yol("pilot", cik), {"karar": {"karar": "GÜVENİLMEZ", "otcq_dahil": True}})
        durmali(lambda: V.v2b_kos("B", cik, 1, git_sart=False), "13) pilot GÜVENİLMEZ iken kos B geçti", hata, "KOŞULMAZ")
        durmali(lambda: V.v2b_cek(cik, istemci=None, git_sart=False), "13) pilot GÜVENİLMEZ iken cek geçti", hata, "KOŞULMAZ")
        V._v2b_json(V._v2b_yol("pilot", cik), {"karar": {"karar": "KISMEN", "otcq_dahil": True}})
        durmali(lambda: V.v2b_kos("B", cik, 1, git_sart=False), "13) çekim tamamlanmadan kos B geçti", hata, "çekim")
        gc = pd.bdate_range("2018-01-01", periods=300); cik2 = os.path.join(td, "cikti2"); os.makedirs(cik2)
        Lc = pd.DataFrame({"ticker": ["AA", "BB", "CC", "YY"], "tabaka": ["t1", "t1", "t2", "t1"], "rol": ["ANA", "ANA", "ANA", "YEDEK"],
                           "tabaka_sira": [1, 2, 1, 3], "kaynak": "BORSA", "N_h": 9})
        V._v2b_liste_yaz(V._v2b_yol("liste", cik2), Lc); V.v2b_onkayit(cik2)
        V._v2b_json(V._v2b_yol("pilot", cik2), {"karar": {"karar": "GÜVENİLİR", "otcq_dahil": True}})
        ot_c = SahteOturum({"AA": tiingo_satir(gc, np.full(300, 5.0)), "CC": tiingo_satir(gc, np.full(300, 6.0)), "YY": tiingo_satir(gc, np.full(300, 7.0))})
        sc = Saat(); ist_c = V.TiingoIstemci(E, ot_c, V.TiingoSayac(os.path.join(td, "sc.json"), E, sc), os.path.join(td, "tc"), uyu=sc.uyu)
        cd = V.v2b_cek(cik2, istemci=ist_c, git_sart=False)
        if not cd["tamam"] or cd["durum"] != {"AA": "ok", "BB": "yok", "CC": "ok", "YY": "ok"} or len(ot_c.cagri) != 4:
            hata.append(f"13) çekim + yedek uçtan uca tutmadı: {cd['durum']}, istek {len(ot_c.cagri)}")
        V.v2b_cek(cik2, istemci=ist_c, git_sart=False)
        if len(ot_c.cagri) != 4:
            hata.append("13) ikinci çekim önbelleği kullanmadı (yeniden istek)")
        V._v2b_liste_yaz(V._v2b_yol("liste", cik2), Lc.assign(N_h=10))
        durmali(lambda: V.v2b_cek(cik2, istemci=ist_c, git_sart=False), "13) liste ön kayıttan sonra değişince cek geçti", hata, "liste")
    finally:
        V.KOK_VDYT2B = eski_kok; V.VDYT2B_YOL["tablo"] = eski_tablo
        shutil.rmtree(td, ignore_errors=True)
    # ---------------------------------------------------------------- 14) uçtan uca sentetik (A ve B)
    with tempfile.TemporaryDirectory() as tdx:
        Fs, Evs = T2.sentetik_pazar(nh=8, pazar="BIST"); Es2 = T2.kucuk_E()
        Z = V2.v2_pazar_isle("BIST", "kos", 1, Fs, Evs, Es2); ara = os.path.join(tdx, "ara"); V2.v2_analiz(Z, "kasa", Es2, ara=ara, p1_tekrar=0)
        ZA = V.v2b_A_hazirla(["BIST"], {"BIST": Fs}, ara, ["G5", "G1"], kucuk_E())
        K = V.v2b_A_kapsam(ZA, kucuk_E()); Ks = pd.DataFrame(K["sayim"])
        if not len(Ks) or set(Ks.columns) & {"ma1", "oran", "fark", "yukari_payi"} or (Ks.ma1_olculebilir > Ks.vdyt2_satir).any():
            hata.append("14) A kapsamı yalnız sayı değil ya da ölçülebilir > satır")
        g5 = ZA["BIST"]["G5"]["G"]; d5 = Fs["S"][g5.sembol.iloc[0]]; t5 = int(g5.t.iloc[0])
        tek = V.v2b_ma_etiket_tek(t5, d5.c.to_numpy(float), V._v2b_tr(d5), V1.vdyt_kopuk(d5.index, V2._v2_e1()), E)
        if not ((np.isnan(tek["ma1"]) and np.isnan(g5.ma1.iloc[0])) or tek["ma1"] == g5.ma1.iloc[0]):
            hata.append("14) uçtan uca MA1 elle (tek satır) tutmadı")
        R = V.v2b_A_analiz({"BIST": {"G5": ZA["BIST"]["G5"], "G1": ZA["BIST"]["G1"]}}, kucuk_E())
        if not R["karar"] or any(k["sonuc"] not in ("BAŞARILI", "BAŞARISIZ", "VERİ YOK") for k in R["karar"]) or "MA1" not in {k["etiket"] for k in R["karar"]}:
            hata.append("14) A karar tablosu eksik")
        S_ = R["satir"]
        if not ((S_.ana) & (S_.etiket == "MA1") & (S_.tanim == "G5") & (S_.onkosul == "P1")).sum() == 4:
            hata.append("14) A ANA hücre satırı (2 aşama x 2 kontrol) eksik")
        rp = V.v2b_rapor_metin({"test": "A", "zaman": "x", "sure_sn": 0, "onkayit": {}, **R, "kapsam": K["sayim"]})
        if "## 1. Karar" not in rp:
            hata.append("14) A raporu eksik")
        # B: yaşayan = sentetik ABD (6 hisse), batan = 3 hisse; batan satırları VDYT2 koduyla
        Fa, Eva = T2.sentetik_pazar(nh=6, pazar="ABD", tohum=21); Fbb, _e = T2.sentetik_pazar(nh=3, pazar="ABD", tohum=33)
        Fb2 = {"S": {f"B{s}": d_.assign(v=d_.v * 50) for s, d_ in Fbb["S"].items() if s.startswith("S")},
               "meta": {f"B{s}": {"tur": "EQUITY", "bolunme": []} for s in Fbb["S"] if s.startswith("S")}}
        Fy = {"S": {s: Fa["S"][s] for s in list(Fa["S"])[:6]}, "meta": {s: Fa["meta"][s] for s in list(Fa["S"])[:6]}}
        Bs = V.v2b_batan_satirlar(Fb2, 1, Fa, Eva); Ys = V.v2b_batan_satirlar(Fy, 1, Fa, Eva)
        if not len(Bs["G"]) or not len(Bs["K"]) or set(Bs["G"].sembol) - set(Fb2["S"]) or Bs["hata"]:
            hata.append(f"14) batan satırları üretilmedi ({len(Bs['G'])}, hata {list(Bs['hata'].items())[:1]})")
        else:
            Eb = kucuk_E(); kol = Eb["B"]["kolon"]
            Gb = V.v2b_etiketle(Bs["G"], Fb2, Eb).assign(w=5.0); Kb = V.v2b_etiketle(Bs["K"], Fb2, Eb).assign(w=5.0)
            Gy = V.v2b_etiketle(Ys["G"], Fa, Eb).assign(w=1.0); Ky = V.v2b_etiketle(Ys["K"], Fa, Eb).assign(w=1.0)
            Gb, Kb, Gy, Ky = (x_[[k for k in kol if k in x_]] for x_ in (Gb, Kb, Gy, Ky))
            RB = V.v2b_B_analiz(Gy, Ky, Gb, Kb, Eb); SB = RB["satir"]
            if len(RB["karar"]) != 2 or {k["etiket"] for k in RB["karar"]} != {"Y20", "MA1"}:
                hata.append("14) B karar tablosu eksik")
            x1 = SB[(SB.kume == "BIRLESIK") & (SB.etiket == "Y20") & (SB.asama == "kasa") & (SB.onkosul == "P0") & (SB.kontrol == "RASTGELE")]
            x2 = SB[(SB.kume == "BATAN") & (SB.etiket == "Y20") & (SB.asama == "kasa") & (SB.onkosul == "P0") & (SB.kontrol == "RASTGELE")]
            x3 = SB[(SB.kume == "YASAYAN") & (SB.etiket == "Y20") & (SB.asama == "kasa") & (SB.onkosul == "P0") & (SB.kontrol == "RASTGELE")]
            if len(x1) and len(x2) and len(x3) and int(x1.n1_ham.iloc[0]) != int(x2.n1_ham.iloc[0]) + int(x3.n1_ham.iloc[0]):
                hata.append("14) birleşik gerçek satır sayısı batan + yaşayan değil")
            if len(x1) and len(x2) and len(x3) and np.isfinite(x1.ort1.iloc[0]) and int(x1.n1_dusen.iloc[0]) == 0:
                gb_ = V.v2b_donemde(Gb, "kasa", "ma1", Eb); gy_ = V.v2b_donemde(Gy, "kasa", "ma1", Eb)
                bek = (5.0 * gb_.y20.sum() + gy_.y20.sum()) / (5.0 * len(gb_) + len(gy_))
                if abs(float(x1.ort1.iloc[0]) - bek) > 1e-9:
                    hata.append("14) birleşik ağırlıklı gerçek oran elle tutmadı")
            rb = V.v2b_rapor_metin({"test": "B", "zaman": "x", "sure_sn": 0, "onkayit": {}, **RB, "semboller": pd.DataFrame({"ticker": ["BS00"], "w": [5.0]})})
            if "BATANLAR DAHİL" not in rb:
                hata.append("14) B raporu eksik")
    # ---------------------------------------------------------------- 15) çakışma kapısı
    g15 = {"__name__": "x", "_CK_KAYIT": {"v2b_sigma": "BASKA.py"}, "v2b_sigma": 1}
    try:
        cwd = os.getcwd(); os.chdir(KOK)
        exec(compile(open(os.path.join(KOK, "VDYT2B.py"), encoding="utf-8").read(), "VDYT2B.py", "exec"), g15)
        hata.append("15) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"15) çakışma kapısı yanlış neden: {ex}")
    finally:
        os.chdir(cwd)
    g15b: dict = {"__name__": "x"}
    try:
        cwd = os.getcwd(); os.chdir(KOK)
        exec(compile(open(os.path.join(KOK, "VDYT2B.py"), encoding="utf-8").read(), "VDYT2B.py", "exec"), g15b)
        exec(compile(open(os.path.join(KOK, "VDYT2B.py"), encoding="utf-8").read(), "VDYT2B.py", "exec"), g15b)
    except RuntimeError as ex:
        hata.append(f"15) aynı dosyanın ikinci yüklemesi durdu: {ex}")
    finally:
        os.chdir(cwd)
    # ---------------------------------------------------------------- 16) VDYT2 / VDYT değişmedi; anahtar / e-posta yok
    if V2.v2_kod_sha() != E["vdyt2"]["kod_sha"] or V2.v2_v1_kod_sha() != E["vdyt2"]["vdyt_kod_sha"] or V2.v2_esik_sha() != E["vdyt2"]["esik_sha"]:
        hata.append("16) VDYT2.py / VDYT.py / VDYT2 mührü VDYT2 ön kaydındakiyle aynı değil (DEĞİŞMİŞ)")
    kaynak = open(os.path.join(KOK, "VDYT2B.py"), encoding="utf-8").read()
    if V._V2B_EPOSTA.search(kaynak) or re.search(r"Token [0-9a-f]{20,}", kaynak):
        hata.append("16) kodda e-posta / anahtar biçimli metin var")
    for f in ("FON_IZI", "COL_v1", "takip", "IZ_KARNE"):
        if re.search(rf"^\s*(import|from)\s+{f}\b", kaynak, re.M):
            hata.append(f"16) VDYT2B {f} içe aktarıyor (bağımsız olmalı)")
    shutil.rmtree(td0, ignore_errors=True)
    return hata


if __name__ == "__main__":
    h = testler()
    if h:
        print("BAŞARISIZ:", len(h)); print("\n".join(" - " + x for x in h)); sys.exit(1)
    print("test_vdyt2b: hepsi geçti")
