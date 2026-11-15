"""K59 testleri (ağ gerekmez; yalnız SENTETİK veri, gerçek veride getiri ölçmez). Çalıştırma: python test_k59.py

1) çakışma kapısı  2) ön kayıt mührü (zaman, üzerine yazmama, bozuk / farklı mühür reddi, eşik değişince mühür değişir; gerçek
K59_ON_KAYIT.md bugünkü eşiklerle aynı, koşu meta'sı varsa ön kayıt koşudan önce)  3) ön kayıtsız / git'e işlenmemiş / verisi farklı koşu
durur  4) GELECEĞE BAKMA YOK: ay sonu t'den sonraki fiyat, hacim, ham fiyat, olay, temel veri ve pay başvurusu bozulunca t ve öncesi
evren + dokuz sinyal + iki bileşik aynı; temel veri 'filed' <= t, bir gün geç başvuru kullanılmaz  5) sinyal tanımları elle hesapla aynı
(S1-S9), ihraç / bölünme kuralı, o günkü fiyat ve piyasa değeri bölünmeden etkilenmez, S3 kapsam kuralı  6) uygunluk (fiyat, likidite,
geçmiş)  7) COMP sıra mantığı ve '4'ün en az 3'ü' kuralı  8) portföy muhasebesi, maliyet, kıyas, ölçüm dönemi  9) NW t ve alfa regresyonu
(bilinen sentetik alfa; beta tuzağı: yüksek beta alfasız portföy v2'den geçmez)  10) plasebo tohumla birebir; kâhin sinyal tutar
11) karar kuralları (PORTFÖY-ADAY, TUTAR AMA KÜÇÜK, TUTMAZ, GÜÇLÜ, plasebo > %5 -> hüküm yok)  12) French birleştirme ve Yahoo ham okuyucu
13) uçtan uca sentetik koşu + rapor  14) e-posta / anahtar yok (kod, test, ön kayıt, çıktılar).
Ek (v1.1): X1 / X2 / X3 bileşenleri ve DOSYA_Y / DOSYA_D / DOSYA_YD bileşikleri 4, 5, 7, 11, 13'te (geleceğe bakma, elle hesap, sıra mantığı
ve 'en az k' kuralı, DOSYA 'GÜÇLÜ' eşiği, karara girmeme); UCUZLUK koşullu testi 8'de (üst %20'nin S9'a göre ikiye bölünmesi, fark serisi).

K59-B (K59 §6'daki üç deneme; yine yalnız SENTETİK veri): B1) K59 mührü ve K59 ön kaydı değişmedi; K59-B eşikleri iş tanımındaki gibi
B2) K59-B ön kaydı (iki mühür, UTC zaman, BOŞLUK listesi, üzerine yazmama; K59 ön kaydı yokken / mühürlerden biri bozukken / verisi farklıyken
/ git'e işlenmemişken durur; eşik değişince mühür değişir)  B3) (a) alt evren: boyut medyanının KESİN altı, boyutu olmayan dışarıda, sıralar
ve kıyas alt evren içinde, geleceğe bakma yok  B4) (b) örtüşen kohortlar: tut = 1 iken K58 portföyüyle birebir, bağımsız elle benzetimle aynı,
al-tut, maliyet yalnız yenilenen kohortta, uygunluğu yitiren hisse tutulur, ilk iki ay dışarıda, kesintide durur, geleceğe bakma yok
B5) (c) French: yalıtılmış çok bölümlü ayrıştırıcı, harman, kıyaslar, sabit maliyet, dönemler, okuma cümlesi  B6) karar kuralları
(PORTFÖY-ADAY yalnız COMP4, iki evren + >= 4 puan, GÜÇLÜ 2,75, tasarıma özel plasebo, hüküm yok)  B7) plasebo tohumları, kâhin sinyal
B8) uçtan uca sentetik `b_kos` + `b_rapor`, çıktılardan yeniden üretim, sayım modunda getiri yok, e-posta yok.
"""
from __future__ import annotations

import copy
import json
import os
import re
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K59 as K  # noqa: E402

FI, K58 = K.FI, K.K58
BOL_GERI = pd.Timestamp("2019-06-03")     # S005: 1:10 ters bölünme
BOL_ILERI = pd.Timestamp("2018-09-04")    # S006: 4:1 bölünme
PAY0 = 1.0e7


def sentetik_ham(n: int = 120, bas: str = "2015-06-01", bit: str = "2020-12-31", tohum: int = 1) -> dict:
    """Sentetik ABD benzeri veri: OHLCV, çeyrek açıklama günleri, K57 biçimli temel tablo, bilgi tarihleri, pay başvuruları, bölünmeler."""
    rng = np.random.default_rng(tohum); idx = pd.bdate_range(bas, bit); V = {}; x = np.linspace(0, 20, len(idx))
    for i in range(n):
        r = rng.normal(rng.normal(0.0003, 0.0006), 0.02, len(idx)); c = rng.uniform(20, 80) * np.exp(np.cumsum(r))
        if i == 3:
            c = 1.2 + 0.3 * np.sin(x)                       # hep 2 $ altı
        if i == 5:
            c = 12.0 + 3.0 * np.sin(x)                      # düzeltilmiş 9-15; ters bölünmeden önce o günkü fiyat 0,9-1,5
        o = c * np.exp(rng.normal(0, 0.005, len(idx)))
        vol = rng.integers(200_000, 1_000_000, len(idx)).astype(float)
        if i == 4:
            vol[:] = 100.0                                  # likit değil
        d = pd.DataFrame({"Open": o, "High": np.maximum(o, c) * 1.01, "Low": np.minimum(o, c) * 0.99, "Close": c, "Volume": vol}, index=idx)
        V[f"S{i:03d}"] = d.iloc[int(rng.integers(300, 500)) if (i % 9 == 0 and i) else 0:]
    T = {"Q": {}, "I": {}}; bilgi = {}; s2c = {}; pay = []; duyuru = []
    for i, s in enumerate(sorted(V)):
        cik = str(1000 + i)
        if i != 10:
            s2c[s] = cik
        gelir = "SalesRevenueNet" if i % 3 == 0 else "Revenues"; g0 = rng.uniform(50, 500); oz = rng.uniform(200, 900)
        for y in range(2015, 2021):
            for q in range(1, 5):
                sira = y * 4 + q - 1; son = pd.Period(f"{y}Q{q}", "Q").end_time.normalize()
                g0 *= float(np.exp(rng.normal(0.02, 0.10)))
                T["Q"].setdefault((cik, gelir), {})[sira] = (son, g0)
                if not (i == 8 and sira % 5 == 0):
                    T["Q"].setdefault((cik, "NetIncomeLoss"), {})[sira] = (son, float(rng.normal(0.08, 0.10) * g0))
                T["I"].setdefault((cik, "StockholdersEquity"), {})[sira] = (son, -50.0 if i == 7 else oz)
                yk = oz * float(rng.uniform(0.2, 3.0))
                if i % 4 == 2:
                    T["I"].setdefault((cik, "LiabilitiesAndStockholdersEquity"), {})[sira] = (son, yk + oz)   # yalnız toplam pasif
                elif i != 12:
                    T["I"].setdefault((cik, "Liabilities"), {})[sira] = (son, yk)
                bil = son + pd.Timedelta(days=40 + i % 5); bilgi[(cik, sira)] = bil
                p = PAY0 * (4.0 if (i == 6 and son >= BOL_ILERI) else 1.0) * (1.0 if i == 6 else 1.01 ** (sira - 2015 * 4) * (1 + 0.3 * (i % 4 == 1)))
                pay.append({"sembol": s, "filed": bil, "pay": p, "pay_t": son, "sira": sira})
                duyuru.append({"sembol": s, "D": son + pd.offsets.BDay(25)})
    F = pd.DataFrame(pay).sort_values(["sembol", "sira"])
    F["pay_yil"] = F.groupby("sembol").pay.transform(lambda z: z / z.shift(4) - 1)
    F.loc[(F.sembol == "S011") & (F.sira % 4 == 0), "pay_yil"] = 6.0          # 7 kat: veri yok sayılmalı
    bol = {"S005": (np.array([BOL_GERI.to_datetime64()], "datetime64[ns]"), np.array([0.1])),
           "S006": (np.array([BOL_ILERI.to_datetime64()], "datetime64[ns]"), np.array([4.0]))}
    return {"V": V, "T": T, "bilgi": bilgi, "s2c": s2c, "pay": F.drop(columns="sira"), "duyuru": pd.DataFrame(duyuru), "bolunme": bol}


def olaylar(H: dict, V: dict) -> pd.DataFrame:
    return FI.fi_k28_olaylar(H["duyuru"], V, "ABD", FI.FI_K28)[["sembol", "D", "tepki_son", "ear"]]


def demet(H: dict, tur: str = "U2", V: dict | None = None, **ek) -> dict:
    """Sentetik veriden K59 demeti (U2: ham kapanış + bölünme + piyasa değeri; U1: düzeltilmiş fiyat + işlem değeri; BIST: yalnız fiyat)."""
    V = V or H["V"]
    ev = {**K.K59_ESIK["evren"][tur], "bas": "2016-01-01", "kes": "2020-12-31", "min_evren": 30, "min_sinyal": 20}
    D = {"ad": tur, "evren": ev, "V": V, "ham": None, "bolunme": None, "olay": None, "T": None, "bilgi": None, "s2c": None, "pay": None}
    if tur != "BIST":
        D.update({"olay": olaylar(H, V), "T": H["T"], "bilgi": H["bilgi"], "s2c": H["s2c"], "pay": H["pay"]})
    if tur == "U2":
        D.update({"ham": pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index(), "bolunme": H["bolunme"]})
    D.update(ek)
    return D


def boz(H: dict, t0: pd.Timestamp, tohum: int = 9) -> dict:
    """t0'dan SONRAKİ her şeyi bozar: fiyat, hacim, bilgi tarihi > t0 olan çeyrek değerleri, 'filed' > t0 olan pay başvuruları."""
    rng = np.random.default_rng(tohum); Vb = {}
    for s, d in H["V"].items():
        k = np.where(d.index > t0, rng.uniform(0.3, 3.0, len(d)), 1.0)
        Vb[s] = d.assign(Open=d.Open * k, High=d.High * k * np.where(d.index > t0, 1.2, 1.0), Low=d.Low * k, Close=d.Close * k,
                         Volume=d.Volume * np.where(d.index > t0, rng.uniform(0.01, 5.0, len(d)), 1.0))
    Tb = {"Q": {}, "I": {}}
    for tab in ("Q", "I"):
        for (cik, e), q in H["T"][tab].items():
            Tb[tab][(cik, e)] = {s: (b, v * float(rng.uniform(-2, 3)) if H["bilgi"][(cik, s)] > t0 else v) for s, (b, v) in q.items()}
    Fb = H["pay"].copy(); m = (Fb.filed > t0).to_numpy()
    Fb.loc[m, "pay"] = Fb.loc[m, "pay"].to_numpy() * rng.uniform(0.2, 5.0, int(m.sum()))
    Fb.loc[m, "pay_yil"] = rng.uniform(-0.5, 3.0, int(m.sum()))
    return {**H, "V": Vb, "T": Tb, "pay": Fb}


def mini_panel(R: np.ndarray, U: np.ndarray, maliyet: float = 0.001, min_sinyal: int = 5) -> dict:
    n = len(R); me = pd.DatetimeIndex(pd.date_range("2020-01-31", periods=n + 1, freq="ME"))
    z = np.zeros((1, R.shape[1]))
    return {"ad": "T", "evren": {"maliyet": maliyet, "min_sinyal": min_sinyal, "french": False}, "ay_sonu": me, "U": np.vstack([U, z.astype(bool)]),
            "R": np.vstack([R, z * np.nan]), "olusum": np.r_[np.ones(n, bool), False]}


def testler() -> list:
    hata = []
    # 1) çakışma kapısı
    src = open(os.path.join(KOK, "K59.py"), encoding="utf-8").read().replace("from __future__ import annotations\n", "")
    g = {"__name__": "kapi_test", "k59_kos": object(), "_CK_KAYIT": {"k59_kos": "BASKA.py"}}
    try:
        exec(compile(src, "K59.py", "exec"), g)
        hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "kapi_test2"}
    try:
        exec(compile(src, "K59.py", "exec"), g2); exec(compile(src, "K59.py", "exec"), g2)
    except Exception as ex:
        hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
    if "_CK_ONCE_K59" not in src or "_cakisma_kontrol_k59()" not in src:
        hata.append("1) çakışma kapısı adı _CK_ONCE_K59 değil")
    # 2) ön kayıt mührü
    with tempfile.TemporaryDirectory() as td:
        y = K.k59_onkayit(td, veri_sha={"V_ABD.pkl": ("a" * 64, 1), "secframes": ("b" * 64, 7)}); ilk = open(y, encoding="utf-8").read()
        if K.k59_esik_sha() not in ilk or not re.search(r"^Yazım zamanı: \d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC", ilk, re.M):
            hata.append("2) ön kayıtta mühür / UTC zaman yok")
        for parca in ("## Veri", "## 1. Evrenler", "## 2. Sinyaller", "## 3. Portföy ve cetvel v2", "## 4. Karar kuralları", "## 5. Plasebo",
                      "## 6. COMP4 tutmazsa", "## 5b. Koşullu test 'UCUZLUK'", "DOSYA_Y (", "DOSYA_D (", "DOSYA_YD (", "VEKİLİDİR", "SÜRÜM NOTU", "- X1 "[2:],
                      "6. DOSYA AİLESİ", K.K59_ONCEKI["muhur"], "HAYATTA KALMA", "PORTFÖY-ADAY", "TUTAR AMA KÜÇÜK", "GÜÇLÜ", "TUTAR (yineleme)", "İZ ilan EDİLEMEZ",
                      "COMP4 (KARAR", "COMP9 (BİLGİ)", "BAĞIMSIZ DEĞİL", "python -I K59.py kos") + tuple(f"- S{i} " for i in range(1, 10)):
            if parca not in ilk:
                hata.append(f"2) ön kayıtta '{parca}' yok")
        oc = K._k59_onkayit_oku(y)
        if oc["veri"] != {"V_ABD.pkl": ("a" * 64, 1), "secframes": ("b" * 64, 7)}:
            hata.append(f"2) ön kayıttan veri sha256'ları okunamadı: {oc['veri']}")
        K.k59_onkayit(td)
        if open(y, encoding="utf-8").read() != ilk:
            hata.append("2) ön kayıt üzerine yazıldı")
        if K.k59_onkayit_dogrula(td)["sha"] != K.k59_esik_sha():
            hata.append("2) doğrulama mührü yanlış")
        try:
            K.k59_onkayit_dogrula(td, veri=True); hata.append("3) verisi ön kayıttan farklı koşu durmadı")
        except K.K59Hata:
            pass
        try:
            K.k59_onkayit_dogrula(td, git=True); hata.append("3) git'e işlenmemiş ön kayıt kabul edildi")
        except K.K59Hata:
            pass
        open(y, "w", encoding="utf-8").write(ilk.replace(K.k59_esik_sha(), "0" * 64))
        for f_, ad in ((K.k59_onkayit_dogrula, "bozuk mühür kabul edildi"), (K.k59_onkayit, "mührü farklı ön kayıt sessizce kabul edildi")):
            try:
                f_(td); hata.append(f"2) {ad}")
            except K.K59Hata:
                pass
    E2 = copy.deepcopy(K.K59_ESIK); E2["cetvel"]["t_esik"] = 1.9
    E3 = copy.deepcopy(K.K59_ESIK); E3["bilesik"]["COMP4"]["min"] = 2
    if len({K.k59_esik_sha(), K.k59_esik_sha(E2), K.k59_esik_sha(E3)}) != 3 or K.k59_esik_sha() != K.k59_esik_sha(copy.deepcopy(K.K59_ESIK)):
        hata.append("2) eşik değişince mühür değişmiyor / aynı eşikte mühür farklı")
    gercek = K._k59_yol("onkayit")
    if not os.path.exists(gercek):
        hata.append("2) arastirma_cikti/k59_basit_sinyaller/K59_ON_KAYIT.md yok")
    else:
        try:
            oc = K.k59_onkayit_dogrula()
            if not oc["zaman_utc"] or len(oc["veri"]) < 5:
                hata.append(f"2) gerçek ön kayıtta UTC zaman / veri sha256 eksik ({len(oc['veri'])} kaynak)")
            my = K._k59_yol("meta")
            if os.path.exists(my):
                meta = json.load(open(my, encoding="utf-8"))
                if pd.Timestamp(oc["zaman_utc"]) > pd.Timestamp(meta["kos_baslangic"].replace(" UTC", "")) or meta["onkayit"]["sha"] != oc["sha"]:
                    hata.append("2) ön kayıt koşudan sonra yazılmış / koşu başka mühürle yapılmış")
        except K.K59Hata as ex:
            hata.append(f"2) gerçek ön kayıt bugünkü eşiklerle aynı değil: {ex}")
    # 3) ön kayıtsız koşu durur (sentetik demetle bile)
    H = sentetik_ham(); D2 = demet(H, "U2"); D1 = demet(H, "U1")
    with tempfile.TemporaryDirectory() as td:
        try:
            K.k59_kos(td, git_sart=False, demetler={"U2": D2}); hata.append("3) ön kayıtsız koşu durmadı")
        except K.K59Hata:
            pass
        K.k59_onkayit(td, veri_sha={})
        try:
            K.k59_kos(td, git_sart=True, demetler={"U2": D2}); hata.append("3) git'e işlenmemiş ön kayıtla koşu durmadı")
        except K.K59Hata:
            pass
    # 4) geleceğe bakma yok
    def hepsi(S_: dict, ek_: dict, U_: np.ndarray) -> dict:
        """Sinyaller + ek bileşenler (X1-X3) + bütün bileşikler (K59 k59_evren_olc ile aynı havuz)."""
        havuz = {**S_, **ek_["bilesen"]}
        return {**havuz, **{b: K.k59_bilesik(havuz, U_, tn["uye"], tn["min"]) for b, tn in K.K59_ESIK["bilesik"].items()}}
    P2 = K.k59_panel(D2); S2, ek2 = K.k59_sinyaller(D2, P2); S2 = hepsi(S2, ek2, P2["U"])
    eksik = [a for a in K.K59_SIRA + ["X1", "X2", "X3"] + list(K.K59_ESIK["bilesik"]) if a not in S2 or np.isfinite(S2[a]).sum() < 500]
    if eksik:
        hata.append(f"4) sentetik demette sinyal üretilemedi: {eksik}")
    me = P2["ay_sonu"]; k0 = int(np.flatnonzero(P2["olusum"])[26]); t0 = me[k0]
    Hb = boz(H, t0); Db = demet(Hb, "U2"); Pb = K.k59_panel(Db); Sb, ekb = K.k59_sinyaller(Db, Pb); Sb = hepsi(Sb, ekb, Pb["U"])
    if not np.array_equal(P2["U"][:k0 + 1], Pb["U"][:k0 + 1]) or not np.allclose(P2["fiyat_o"][:k0 + 1], Pb["fiyat_o"][:k0 + 1], equal_nan=True) \
            or not np.allclose(P2["tl_me"][:k0 + 1], Pb["tl_me"][:k0 + 1], equal_nan=True):
        hata.append("4) uygunluk (evren / o günkü fiyat / işlem değeri) ay sonu t'den sonrasını görüyor")
    if not np.allclose(P2["R"][:k0], Pb["R"][:k0], equal_nan=True) or np.allclose(P2["R"][k0:k0 + 3], Pb["R"][k0:k0 + 3], equal_nan=True):
        hata.append("4) t'den önceki ay getirileri değişti / bozma etkisiz")
    for a in S2:
        if not np.allclose(S2[a][:k0 + 1], Sb[a][:k0 + 1], equal_nan=True):
            hata.append(f"4) {a} ay sonu t'den sonraki veriyi görüyor (geleceğe bakma)")
        if np.allclose(S2[a][k0 + 6:], Sb[a][k0 + 6:], equal_nan=True):
            hata.append(f"4) {a}: bozma testi etkisiz (sonraki sinyaller de değişmedi)")
    mt = me.to_numpy("datetime64[ns]")[:, None]
    for a, alan in (("S5", "bilgi_son"), ("S7", "bilgi_son"), ("X1", "bilgi_son"), ("X2", "bilgi_son"), ("S6", "pay_filed")):
        m = np.isfinite(S2[a]); b = ek2[alan]
        if np.isnat(b[m]).any() or (b > mt)[m].any():
            hata.append(f"4) {a}: kullanılan temel verinin 'filed' / bilgi tarihi ay sonundan sonra ya da yok")
    X = D2["olay"]; pos = P2["gun"].get_indexer(pd.DatetimeIndex(X.tepki_son))
    j7 = int(np.flatnonzero(np.isfinite(S2["S7"][k0]))[0]); s7 = P2["sembol"][j7]; c7 = H["s2c"][s7]
    q0 = max(q for (c, q), b in H["bilgi"].items() if c == c7 and b <= t0)
    for gun_, kullan in ((1, False), (0, True)):
        bg = dict(H["bilgi"]); bg[(c7, q0)] = t0 + pd.Timedelta(days=gun_)
        Tg = K.k59_temel_sinyal(H["T"], bg, H["s2c"], P2["sembol"], me, P2["U"])
        ayni = np.isclose(Tg["S7"][k0, j7], S2["S7"][k0, j7], equal_nan=True)
        if ayni != kullan or (np.isfinite(Tg["S7"][k0, j7]) and Tg["bilgi_son"][k0, j7] > t0.to_datetime64()):
            hata.append(f"4) bilgi tarihi t + {gun_} gün olan çeyrek için kural yanlış (kullanıldı mı: {bool(ayni)}, beklenen {kullan})")
    # 5) sinyal tanımları elle hesapla
    Cm = P2["Cm"]; jj = [j for j in np.flatnonzero(P2["U"][k0]) if j not in (5, 6)][:6]
    for j in jj:
        s = P2["sembol"][j]; d = H["V"][s]; d = d[d.index <= t0]; c = d.Close
        bek = {"S1": Cm.iloc[k0 - 1, j] / Cm.iloc[k0 - 12, j] - 1, "S2": -(Cm.iloc[k0, j] / Cm.iloc[k0 - 1, j] - 1),
               "S8": -c.pct_change().iloc[-60:].std(), "S9": c.iloc[-1] / d.High.iloc[-252:].max()}
        e = X[(X.sembol == s).to_numpy() & (pos >= 0) & (pos <= P2["me_pos"][k0]) & (pos > P2["me_pos"][k0] - 63)]
        bek["S4"] = float(e.sort_values("tepki_son").ear.iloc[-1]) if len(e) else np.nan
        f = H["pay"][(H["pay"].sembol == s) & (H["pay"].filed <= t0)].sort_values("filed").iloc[-1]
        bek["S6"] = -float(K.k59_ihrac(np.array([f.pay_yil]), 0.03, 5.0)[0])
        bek["S3"] = -float(c.iloc[-1] * f.pay)
        cik = H["s2c"].get(s)
        if cik:
            qb = sorted(q for (cc, q), b in H["bilgi"].items() if cc == cik and b <= t0)
            q0_ = qb[-1]; kar = H["T"]["Q"].get((cik, "NetIncomeLoss"), {}); gel = [v for (cc, e_), v in H["T"]["Q"].items() if cc == cik and e_ != "NetIncomeLoss"][0]
            oz = H["T"]["I"][(cik, "StockholdersEquity")][q0_][1]
            bek["S5"] = sum(kar[q][1] for q in range(q0_ - 3, q0_ + 1)) / oz if all(q in kar for q in range(q0_ - 3, q0_ + 1)) and oz > 0 else np.nan
            bek["S7"] = gel[q0_][1] / ((gel[q0_ - 1][1] + gel[q0_ - 2][1]) / 2)
            bek["X1"] = gel[q0_][1] / gel[q0_ - 4][1] - 1
            Ti = H["T"]["I"]; yk = Ti[(cik, "Liabilities")][q0_][1] if (cik, "Liabilities") in Ti else (
                Ti[(cik, "LiabilitiesAndStockholdersEquity")][q0_][1] - oz if (cik, "LiabilitiesAndStockholdersEquity") in Ti else np.nan)
            bek["X2"] = -yk / oz if oz > 0 else np.nan
        bek["X3"] = -bek["S9"]
        for a, v in bek.items():
            if not np.isclose(S2[a][k0, j], v, equal_nan=True, rtol=1e-9):
                hata.append(f"5) {a} {s}: {S2[a][k0, j]} != elle {v}")
    gun_ = P2["gun"]; mpk = np.array([int(P2["me_pos"][k0])])
    Xs = pd.DataFrame({"sembol": ["A", "B", "C", "C", "D"], "tepki_son": gun_[[mpk[0] - 62, mpk[0] - 63, mpk[0] - 40, mpk[0] - 5, mpk[0] + 1]],
                       "ear": [0.11, 0.22, 0.33, 0.44, 0.55]})
    p4 = K.k59_pead_sinyal(Xs, ["A", "B", "C", "D", "E"], gun_, mpk, 63)
    if not np.allclose(p4, [[0.11, np.nan, 0.44, np.nan, np.nan]], equal_nan=True):
        hata.append(f"5) S4 penceresi (son 63 işlem günü, en son olay, t'den sonraki olay yok) yanlış: {p4}")
    j2_, j12_ = P2["sembol"].index("S002"), P2["sembol"].index("S012")
    if not np.isfinite(S2["X2"][:, j2_]).any() or np.isfinite(S2["X2"][:, j12_]).any() or not np.isfinite(S2["X1"][:, j12_]).any():
        hata.append("5) X2: yalnız toplam pasifi olan hissede yedek kural çalışmadı / yükümlülüğü olmayan hissede değer üretildi")
    if np.isfinite(S2["X2"][:, P2["sembol"].index("S007")]).any() or np.nanmax(S2["X2"]) > 0:
        hata.append("5) X2: özkaynak <= 0 iken hesaplandı / işaret yanlış (düşük kaldıraç yüksek olmalı)")
    j7_, j8_, j10_, j11_ = (P2["sembol"].index(x) for x in ("S007", "S008", "S010", "S011"))
    if np.isfinite(S2["S5"][:, j7_]).any() or not np.isfinite(S2["S7"][:, j7_]).any():
        hata.append("5) özkaynak <= 0 iken S5 hesaplandı / S7 de düştü")
    if np.isfinite(S2["S5"][:, j10_]).any() or np.isfinite(S2["S7"][:, j10_]).any() or not np.isfinite(S2["S1"][:, j10_]).any():
        hata.append("5) CIK'i olmayan hissede temel sinyal var / fiyat sinyali yok")
    n8 = np.isfinite(S2["S5"][P2["U"][:, j8_], j8_])
    if n8.all() or not n8.any():
        hata.append("5) eksik çeyrekli hissede S5 kuralı (4 çeyreğin hepsi şart) çalışmıyor")
    if np.isfinite(S2["S6"][P2["U"][:, j11_], j11_]).all():
        hata.append("5) 7 kat pay sıçraması veri yok sayılmadı")
    ih = K.k59_ihrac(np.array([0.08, 1.0, 1.02, 6.0, -0.75, -0.5, -0.9, 0.5, np.nan, 4.0, 4.2, -1.0]), 0.03, 5.0)
    bek = [0.08, 0.0, 0.01, np.nan, 0.0, 0.0, np.nan, 0.5, np.nan, 0.0, np.nan, np.nan]
    if not np.allclose(ih, bek, equal_nan=True, atol=1e-12):
        hata.append(f"5) ihraç / bölünme kuralı yanlış: {ih}")
    cr = K.k59_bolunme_carpan(H["bolunme"]["S006"], np.array(["2018-08-31", "2018-09-04", "2018-09-28", "NaT"], "datetime64[ns]"))
    if list(cr) != [4.0, 1.0, 1.0, 1.0] or list(K.k59_bolunme_carpan(None, np.array(["2018-08-31"], "datetime64[ns]"))) != [1.0]:
        hata.append(f"5) bölünme çarpanı yanlış: {cr}")
    j6 = P2["sembol"].index("S006"); u6 = P2["U"][:, j6]
    if not np.allclose(S2["S3"][u6, j6], -(P2["ham_me"][u6, j6] * 4 * PAY0)) or not (me[u6] < BOL_ILERI).any() or not (me[u6] > BOL_ILERI).any():
        hata.append("5) piyasa değeri bölünmeden etkileniyor (bölünme öncesi ve sonrası aynı ölçekte değil)")
    if set(x for x in ek2["S3_olcu"] if x) != {"piyasa_degeri"}:
        hata.append(f"5) U2'de S3 ölçüsü piyasa değeri değil: {set(ek2['S3_olcu'])}")
    P1 = K.k59_panel(D1); S1_, ek1 = K.k59_sinyaller(D1, P1)
    if set(x for x in ek1["S3_olcu"] if x) != {"islem_degeri"} or not np.allclose(S1_["S3"][P1["U"]], -P1["tl_me"][P1["U"]]):
        hata.append("5) U1'de S3 işlem değeri değil")
    s0 = sorted(H["V"])[20]; d0 = H["V"][s0]; d0 = d0[d0.index <= t0]
    if not np.isclose(P1["tl_me"][k0, P1["sembol"].index(s0)], (d0.Close * d0.Volume).iloc[-20:].median()):
        hata.append("5) 20 günlük medyan işlem değeri elle hesapla aynı değil")
    az = H["pay"][H["pay"].sembol.isin(sorted(H["V"])[:30])]
    Sa, eka = K.k59_sinyaller(demet(H, "U2", pay=az), P2)
    if set(x for x in eka["S3_olcu"] if x) != {"islem_degeri"} or not np.allclose(Sa["S3"][P2["U"]], -P2["tl_me"][P2["U"]]):
        hata.append("5) pay kapsamı < %50 iken S3 işlem değerine dönmedi")
    # 6) uygunluk
    j3, j4, j5, j9 = (P2["sembol"].index(x) for x in ("S003", "S004", "S005", "S009"))
    if P2["U"][:, j3].any() or P2["U"][:, j4].any():
        hata.append("6) 2 $ altı / likit olmayan hisse evrene girdi")
    u5 = P2["U"][:, j5]
    if u5[me < BOL_GERI].any() or not u5[me > BOL_GERI].any() or not P1["U"][:, P1["sembol"].index("S005")][me < BOL_GERI].any():
        hata.append("6) o günkü fiyat kuralı: ters bölünmeden önce kuruşluk hisse U2'ye girdi / sonra girmedi / U1 (düzeltilmiş) farklı değil")
    ilk9 = H["V"]["S009"].index[251]
    if P2["U"][me < ilk9, j9].any() or not P2["U"][me >= ilk9, j9].any():
        hata.append("6) 252 gün geçmiş kuralı yanlış")
    if (me[P2["olusum"]] < pd.Timestamp("2016-01-01")).any() or P2["olusum"][-1] or (P2["U"].sum(axis=1)[P2["olusum"]] < 30).any():
        hata.append("6) oluşum ayı aralık dışında / son ay oluşumda / evren tabanın altında")
    # 7) COMP sıra mantığı
    U_ = np.ones((1, 5), bool)
    r1 = K.k59_yuzde_sira(np.array([[1.0, 2.0, 3.0, 4.0, np.nan]]), U_); r2 = K.k59_yuzde_sira(np.array([[1.0, 1.0, 2.0, np.nan, np.nan]]), U_)
    if not np.allclose(r1, [[0.125, 0.375, 0.625, 0.875, np.nan]], equal_nan=True) or not np.allclose(r2, [[1 / 3, 1 / 3, 2.5 / 3, np.nan, np.nan]], equal_nan=True):
        hata.append(f"7) yüzdelik sıra yanlış: {r1} {r2}")
    nan = np.nan
    Sd = {"S1": np.array([[1.0, 2.0, 3.0, 4.0, 5.0]]), "S4": np.array([[5.0, nan, 3.0, nan, 1.0]]), "S5": np.array([[1.0, nan, nan, 4.0, 5.0]]),
          "S6": np.array([[nan, nan, 3.0, 4.0, 5.0]])}
    c4 = K.k59_bilesik(Sd, U_, ["S1", "S4", "S5", "S6"], 3)
    bek = [np.mean([0.1, 2.5 / 3, 0.5 / 3]), nan, np.mean([0.5, 1.5 / 3, 0.5 / 3]), np.mean([0.7, 1.5 / 3, 1.5 / 3]), np.mean([0.9, 0.5 / 3, 2.5 / 3, 2.5 / 3])]
    if not np.allclose(c4, [bek], equal_nan=True):
        hata.append(f"7) COMP4 / '4'ün en az 3'ü' kuralı yanlış: {c4} != {bek}")
    if np.isfinite(K.k59_bilesik(Sd, np.array([[True, True, False, True, True]]), ["S1", "S4", "S5", "S6"], 3)[0, 2]):
        hata.append("7) uygun olmayan hisse bileşiğe girdi")
    c4s = S2["COMP4"]; say4 = sum(np.isfinite(S2[a]).astype(int) for a in ("S1", "S4", "S5", "S6"))
    if not np.array_equal(np.isfinite(c4s), say4 >= 3) or np.nanmin(c4s) <= 0 or np.nanmax(c4s) >= 1:
        hata.append("7) sentetik panelde COMP4 '>= 3 üye' kuralına uymuyor / aralık dışı")
    Bk = K.K59_ESIK["bilesik"]
    if [(Bk[b]["uye"], Bk[b]["min"], Bk[b]["rol"]) for b in ("DOSYA_Y", "DOSYA_D", "DOSYA_YD")] != [
            (["S7", "X1", "S5", "S6", "S4"], 4, "DOSYA"), (["X2", "X1", "X3"], 3, "DOSYA"), (["S7", "X1", "S5", "S6", "S4", "X2"], 5, "DOSYA")] \
            or K.K59_ESIK["karar"]["dosya"] != ["DOSYA_Y", "DOSYA_D", "DOSYA_YD"] or Bk["COMP4"]["uye"] != ["S1", "S4", "S5", "S6"] or Bk["COMP4"]["min"] != 3:
        hata.append("7) DOSYA / COMP4 bileşik tanımları iş tanımındaki gibi değil")
    U6 = np.ones((1, 6), bool)                                   # 6 hisse: A tam, B 4 üye, C 3 üye, D yalnız X'ler, E tam (kötü), F uygun değil
    Sx = {"S7": np.array([[6.0, 5.0, 4.0, nan, 1.0, 9.0]]), "X1": np.array([[6.0, 5.0, 4.0, 3.0, 1.0, 9.0]]), "S5": np.array([[6.0, 5.0, 4.0, nan, 1.0, 9.0]]),
          "S6": np.array([[6.0, 5.0, nan, nan, 1.0, 9.0]]), "S4": np.array([[6.0, nan, nan, nan, 1.0, 9.0]]), "X2": np.array([[-0.5, nan, -1.0, -2.0, -3.0, -0.1]]),
          "X3": np.array([[-0.9, -0.8, -0.7, -0.5, -0.99, -0.1]])}
    U6[0, 5] = False
    dy = K.k59_bilesik(Sx, U6, Bk["DOSYA_Y"]["uye"], Bk["DOSYA_Y"]["min"]); dd = K.k59_bilesik(Sx, U6, Bk["DOSYA_D"]["uye"], Bk["DOSYA_D"]["min"])
    dyd = K.k59_bilesik(Sx, U6, Bk["DOSYA_YD"]["uye"], Bk["DOSYA_YD"]["min"])
    bek_y = [np.mean([3.5 / 4, 4.5 / 5, 3.5 / 4, 2.5 / 3, 1.5 / 2]), np.mean([2.5 / 4, 3.5 / 5, 2.5 / 4, 1.5 / 3]), nan, nan, np.mean([0.5 / 4, 0.5 / 5, 0.5 / 4, 0.5 / 3, 0.5 / 2]), nan]
    bek_d = [np.mean([3.5 / 4, 4.5 / 5, 1.5 / 5]), nan, np.mean([2.5 / 4, 2.5 / 5, 3.5 / 5]), np.mean([1.5 / 4, 1.5 / 5, 4.5 / 5]), np.mean([0.5 / 4, 0.5 / 5, 0.5 / 5]), nan]
    bek_yd = [np.mean([3.5 / 4, 4.5 / 5, 3.5 / 4, 2.5 / 3, 1.5 / 2, 3.5 / 4]), nan, nan, nan, np.mean([0.5 / 4, 0.5 / 5, 0.5 / 4, 0.5 / 3, 0.5 / 2, 0.5 / 4]), nan]
    for ad, v, b in (("DOSYA_Y (5'in en az 4'ü)", dy, bek_y), ("DOSYA_D (3'ün 3'ü)", dd, bek_d), ("DOSYA_YD (6'nın en az 5'i)", dyd, bek_yd)):
        if not np.allclose(v, [b], equal_nan=True):
            hata.append(f"7) {ad} sıra ortalaması / 'en az k' kuralı yanlış: {v} != {b}")
    for b in ("DOSYA_Y", "DOSYA_D", "DOSYA_YD"):
        say = sum(np.isfinite(S2[a]).astype(int) for a in Bk[b]["uye"])
        if not np.array_equal(np.isfinite(S2[b]), say >= Bk[b]["min"]) or not np.isfinite(S2[b]).any() or np.nanmin(S2[b]) <= 0 or np.nanmax(S2[b]) >= 1:
            hata.append(f"7) sentetik panelde {b} '>= {Bk[b]['min']} üye' kuralına uymuyor / aralık dışı")
    k1 = int(np.flatnonzero(P2["olusum"])[30]); g_ = np.isfinite(S2["DOSYA_D"][k1])
    if np.corrcoef(S2["DOSYA_D"][k1, g_], S2["S9"][k1, g_])[0, 1] >= 0:
        hata.append("7) DOSYA_D zirveden DÜŞMÜŞ hisseyi öne almıyor (X3 yönü ters)")
    # 8) portföy muhasebesi
    rng = np.random.default_rng(4); R = rng.normal(0.01, 0.05, (3, 20)); U = np.ones((3, 20), bool); U[:, 19] = False
    S = np.tile(np.arange(20.0), (3, 1)); S[:, 10:] = np.nan; S[0, 3:] = np.nan            # ilk ay yalnız 3 hissede sinyal (< 5): ölçüm 2. aydan
    ek_satir = lambda X_: np.vstack([X_, np.full((1, X_.shape[1]), np.nan)])  # noqa: E731
    Pm = mini_panel(R, U); row, A = K.k59_sinyal_olc(Pm, ek_satir(S), None, {**K.K59_ESIK, "cetvel": {**K.K59_ESIK["cetvel"], "min_ay": 1}})
    kiyas = R[1:, :19].mean(axis=1)
    if len(A) != 2 or list(A.n_hisse) != [1, 1] or list(A.n_sinyal) != [10, 10] or list(A.n_evren) != [19, 19]:
        hata.append(f"8) ölçüm dönemi / üst %10 sayısı / evren sayısı yanlış: {A}")
    elif not (np.allclose(A.brut, R[1:, 9]) and np.allclose(A.kiyas, kiyas) and np.isclose(A.devir.iloc[0], 1.0) and np.isclose(A.devir.iloc[1], 0.0)
              and np.isclose(A.net.iloc[0], (1 - 0.001) * (1 + R[1, 9]) - 1) and np.isclose(A.net.iloc[1], R[2, 9]) and list(A.getiri_ayi) == ["2020-03", "2020-04"]):
        hata.append(f"8) portföy muhasebesi (en yüksek sinyal, maliyet, devir, kıyas = bütün uygun evren, getiri ayı) yanlış: {A}")
    Sx = np.tile(np.arange(20.0), (3, 1)); Sx[1] = Sx[1][::-1]; Sx[:, 19] = np.nan
    _, Ax = K.k59_sinyal_olc(Pm, ek_satir(Sx), None, K.K59_ESIK)
    if not np.allclose(Ax.devir, [1.0, 2.0, 2.0]) or not np.allclose(Ax.net, (1 - 0.001 * Ax.devir) * (1 + Ax.brut) - 1) or list(Ax.n_hisse) != [2, 2, 2]:
        hata.append(f"8) devir / maliyet (tek yön 10 bp x devir) yanlış: {Ax}")
    Ru = rng.normal(0.01, 0.05, (14, 45)); Uu = np.ones((14, 45), bool); Pu = mini_panel(Ru, Uu)
    Scu = ek_satir(np.tile(np.arange(45.0), (14, 1))); Sbu = ek_satir(np.tile(np.r_[np.zeros(36), [5.0, 1.0, 7.0, 3.0, 9.0, 2.0, 8.0, 4.0, 6.0]], (14, 1)))
    sat_u, ayl_u = K.k59_ucuzluk(Pu, Scu, Sbu, None, {**K.K59_ESIK, "cetvel": {**K.K59_ESIK["cetvel"], "min_ay": 1}})
    Au = {str(a.sinyal.iloc[0]): a for a in ayl_u}; dus_j, yak_j = [37, 41, 39, 43], [44, 42, 38, 40]      # üst %20 = 36..44 (9 hisse); ortadaki (36) dışarıda
    if [r["portfoy"] for r in sat_u] != ["dusmus", "yakin", "fark (dusmus - yakin)"] or set(Au) != {"UCUZLUK_dusmus", "UCUZLUK_yakin"}:
        hata.append(f"8) UCUZLUK satırları / aylık serileri eksik: {[r['portfoy'] for r in sat_u]}")
    else:
        d_ = Au["UCUZLUK_dusmus"].net.to_numpy() - Au["UCUZLUK_yakin"].net.to_numpy()
        if not (np.allclose(Au["UCUZLUK_dusmus"].brut, Ru[:, dus_j].mean(axis=1)) and np.allclose(Au["UCUZLUK_yakin"].brut, Ru[:, yak_j].mean(axis=1))
                and list(Au["UCUZLUK_dusmus"].n_hisse) == [4] * 14 and np.isclose(sat_u[2]["yillik_fazla"], 12 * d_.mean())
                and np.isclose(sat_u[2]["nw_t"], K58.k58_nw_t(d_, 6)) and np.isclose(sat_u[0]["yillik_fazla"], 12 * (Au["UCUZLUK_dusmus"].net - Au["UCUZLUK_dusmus"].kiyas).mean())
                and not {"tutar_v2", "etiket"} & set(sat_u[0])):
            hata.append(f"8) UCUZLUK: üst %20'nin S9'a göre ikiye bölünmesi / fark serisi / 'karar yok' yanlış: {sat_u}")
    if K.k59_ucuzluk(Pu, np.full((15, 45), np.nan), Sbu, None, K.K59_ESIK) != ([], []):
        hata.append("8) UCUZLUK bileşik yokken satır üretti")
    if K.k59_sinyal_olc(Pm, np.full((4, 20), np.nan), None, K.K59_ESIK)[0].get("olculdu") is not False:
        hata.append("8) sinyali olmayan evren ölçüldü sayıldı")
    # 9) NW t ve alfa regresyonu
    rs = np.random.default_rng(11); x = rs.normal(0.01, 0.05, 240); e = rs.normal(0, 0.004, 240)
    y = 0.004 + 1.2 * x + e; reg = K.k59_ols_nw(y, x, 6)
    A_ = np.column_stack([np.ones(240), x]); b_ = np.linalg.lstsq(A_, y, rcond=None)[0]; u_ = y - A_ @ b_; Gi = np.linalg.inv(A_.T @ A_)
    Sx_ = np.zeros((2, 2))
    for i in range(240):
        for j in range(240):
            if abs(i - j) <= 6:
                Sx_ += (1 - abs(i - j) / 7) * u_[i] * u_[j] * np.outer(A_[i], A_[j])
    t_el = b_ / np.sqrt(np.diag(Gi @ Sx_ @ Gi))
    if not (np.allclose(reg["katsayi"], b_) and np.allclose(reg["t"], t_el) and abs(reg["katsayi"][0] - 0.004) < 0.001 and abs(reg["katsayi"][1] - 1.2) < 0.03
            and reg["t"][0] > 5):
        hata.append(f"9) alfa regresyonu bilinen sentetik alfayı / elle NW t'yi vermiyor: {reg} {t_el}")
    if not np.isclose(K.k59_ols_nw(x, None, 6)["t"][0], K58.k58_nw_t(x, 6)) or not np.isclose(K.k59_ols_nw(x, None, 0)["t"][0], x.mean() / (x.std(ddof=0) / np.sqrt(240))):
        hata.append("9) yalnız sabitli NW t, K58 k58_nw_t / sıradan t ile aynı değil")
    C = K.K59_ESIK["cetvel"]; kb = 0.02 + rs.normal(0, 0.03, 120)
    v_alfa = K.k59_cetvel_v2(0.01 + kb + rs.normal(0, 0.01, 120), kb, C)
    v_beta = K.k59_cetvel_v2(1.6 * kb + rs.normal(0, 0.004, 120), kb, C)
    v_sifir = K.k59_cetvel_v2(kb + rs.normal(0, 0.01, 120), kb, C)
    if not (v_alfa["tutar_v2"] and v_alfa["s_alfa"] and abs(v_alfa["alfa_aylik"] - 0.01) < 0.004 and abs(v_alfa["beta"] - 1) < 0.1 and K.k59_etiket(v_alfa) == "GÜÇLÜ"):
        hata.append(f"9) gerçek alfalı portföy cetvel v2'den geçmedi: {v_alfa}")
    if not (v_beta["k58c_tutar"] and not v_beta["s_alfa"] and not v_beta["tutar_v2"] and abs(v_beta["beta"] - 1.6) < 0.05 and K.k59_etiket(v_beta) == "TUTMAZ"):
        hata.append(f"9) beta tuzağı: yüksek betalı alfasız portföy K58 C'den geçip v2'de elenmeliydi: {v_beta}")
    if v_sifir["tutar_v2"]:
        hata.append("9) alfasız, beta 1 portföy tuttu")
    v_kisa = K.k59_cetvel_v2(0.01 + kb[:30], kb[:30], C)
    if v_kisa["olculdu"] or v_kisa["tutar_v2"] or K.k59_etiket(v_kisa) != "ÖLÇÜLEMEDİ":
        hata.append("9) 36 aydan kısa seri ölçüldü sayıldı")
    Pf = {"net": 0.01 + kb + rs.normal(0, 0.01, 120), "brut": 0.012 + kb, "kiyas": kb, "devir": np.r_[1.0, np.full(119, 0.5)]}
    ay = pd.period_range("2011-01", periods=120, freq="M")
    FFs = pd.DataFrame(rs.normal(0.003, 0.03, (150, 6)), columns=K.K59_ESIK["french"]["faktor"], index=pd.period_range("2010-01", periods=150, freq="M")).assign(RF=0.001)
    Pf["net"] = 0.001 + 0.006 + 0.9 * FFs["MKT_RF"].reindex(ay).to_numpy() + 0.3 * FFs["UMD"].reindex(ay).to_numpy() + rs.normal(0, 0.003, 120)
    o = K.k59_olc(Pf, ay, FFs)
    eq = np.cumprod(1 + Pf["net"])
    if not (abs(o["ff_alfa_yillik"] - 0.072) < 0.015 and o["ff_ay"] == 120 and o["ff_t_alfa"] > 5 and np.isclose(o["ort_devir"], 0.5)
            and np.isclose(o["mdd"], (eq / np.maximum.accumulate(np.r_[1.0, eq])[1:] - 1).min())
            and np.isclose(o["sharpe"], (Pf["net"] - 0.001).mean() / (Pf["net"] - 0.001).std(ddof=1) * np.sqrt(12)) and "brut_tutar_v2" in o and "brut_sharpe" in o):
        hata.append(f"9) bilgi istatistikleri (FF5+UMD alfası, Sharpe, en büyük düşüş, devir, brüt) yanlış: {o}")
    # 10) plasebo ve kâhin sinyal
    Et = copy.deepcopy(K.K59_ESIK); Et["plasebo"]["n"] = 3; Et["cetvel"]["min_ay"] = 24
    p1 = K.k59_plasebo(P2, Et); p2 = K.k59_plasebo(P2, Et)
    if p1.to_json() != p2.to_json() or p1.brut_nw_t.nunique() < 3 or len(p1) != 3 or not {"tutar_v2", "brut_tutar_v2", "t_alfa", "brut_t_alfa"} <= set(p1.columns):
        hata.append("10) plasebo tohumla birebir tekrar etmiyor / plasebolar aynı / sütun eksik")
    if not (p1.brut_yillik_fazla >= p1.yillik_fazla - 1e-12).all():
        hata.append("10) maliyet net fazlayı düşürmüyor")
    Et2 = copy.deepcopy(Et); Et2["plasebo"]["tohum"] += 1
    if not np.isclose(K.k59_plasebo(P2, Et2).brut_nw_t.iloc[0], p1.brut_nw_t.iloc[1]):
        hata.append("10) plasebo tohumu 'tohum + i' değil")
    kah, _ = K.k59_sinyal_olc(P2, np.where(P2["U"], P2["R"], np.nan), None, Et)
    if not kah["tutar_v2"] or not kah["brut_tutar_v2"] or kah["ort_hisse"] < 5:
        hata.append(f"10) kâhin sinyal (gelecek ay getirisi) cetvel v2'den geçmedi: {kah}")
    # 11) karar kuralları
    Pl = pd.DataFrame({"plasebo": range(200), "tutar_v2": False, "brut_tutar_v2": False})

    def Zk(**deg) -> pd.DataFrame:
        taban = {"olculdu": True, "tutar_v2": True, "nw_t": 2.5, "t_alfa": 2.3, "yillik_fazla": 0.06}
        sat = [{"evren": e, "sinyal": s, **taban} for e in ("U1", "U2") for s in ("COMP4", "S1")]
        for (e, s), d in deg.get("d", {}).items():
            next(r for r in sat if r["evren"] == e and r["sinyal"] == s).update(d)
        return pd.DataFrame(sat)
    for ad, Z_, Pl_, bek in (
            ("aday", Zk(), Pl, "PORTFÖY-ADAY"),
            ("küçük", Zk(d={("U2", "COMP4"): {"yillik_fazla": 0.039}}), Pl, "TUTAR AMA KÜÇÜK"),
            ("tam %4", Zk(d={("U2", "COMP4"): {"yillik_fazla": 0.04}}), Pl, "PORTFÖY-ADAY"),
            ("U2 tutmaz", Zk(d={("U2", "COMP4"): {"tutar_v2": False}}), Pl, "TUTMAZ (U1 TUTAR (yineleme), U2 TUTMAZ)"),
            ("U1 ölçülemedi", Zk(d={("U1", "COMP4"): {"olculdu": False}}), Pl, "TUTMAZ (U1 ÖLÇÜLEMEDİ, U2 TUTAR (yineleme))"),
            ("tekil sinyal karara girmez", Zk(d={("U1", "S1"): {"tutar_v2": False}, ("U2", "S1"): {"tutar_v2": False}}), Pl, "PORTFÖY-ADAY")):
        kr = K.k59_karar(Z_, Pl_)
        if kr["bilesik"] != bek or kr["cetvel"] != "GÜVENİLİR":
            hata.append(f"11) karar '{ad}': {kr['bilesik']} (beklenen {bek})")
    kr = K.k59_karar(Zk(d={("U1", "COMP4"): {"nw_t": 2.9, "t_alfa": 2.81}, ("U2", "COMP4"): {"nw_t": 3.5, "t_alfa": 2.8}, ("U1", "S1"): {"yillik_fazla": 0.02}}), Pl)
    if kr["etiket"][("U1", "COMP4")] != "GÜÇLÜ" or kr["etiket"][("U2", "COMP4")] != "TUTAR (yineleme)" or not kr["kucuk"][("U1", "S1")] or kr["kucuk"][("U2", "S1")]:
        hata.append(f"11) GÜÇLÜ (iki t de > 2,8) / küçük işareti yanlış: {kr}")
    ds = [{"evren": e, "sinyal": d, "olculdu": True, "tutar_v2": d != "DOSYA_D", "nw_t": t_, "t_alfa": t_, "yillik_fazla": 0.03 if e == "U2" else 0.08}
          for e in ("U1", "U2") for d, t_ in (("DOSYA_Y", 2.85), ("DOSYA_D", 3.5), ("DOSYA_YD", 2.95))]
    Zd = pd.concat([Zk(d={("U2", "COMP4"): {"tutar_v2": False}}), pd.DataFrame(ds)], ignore_index=True); kr = K.k59_karar(Zd, Pl)
    if kr["dosya"] != {"U1 DOSYA_Y": "TUTAR (yineleme)", "U2 DOSYA_Y": "TUTAR (yineleme), küçük", "U1 DOSYA_D": "TUTMAZ", "U2 DOSYA_D": "TUTMAZ",
                       "U1 DOSYA_YD": "GÜÇLÜ", "U2 DOSYA_YD": "GÜÇLÜ, küçük"} or not kr["bilesik"].startswith("TUTMAZ"):
        hata.append(f"11) DOSYA ailesi: kendi başına etiket / 'GÜÇLÜ' eşiği 2,9 / PORTFÖY-ADAY kararına girmeme yanlış: {kr.get('dosya')} {kr['bilesik']}")
    if K.k59_karar(pd.concat([Zk(), pd.DataFrame(ds).assign(tutar_v2=False)], ignore_index=True), Pl)["bilesik"] != "PORTFÖY-ADAY" \
            or K.k59_etiket({"sinyal": "S1", "olculdu": True, "tutar_v2": True, "nw_t": 2.85, "t_alfa": 2.85}) != "GÜÇLÜ":
        hata.append("11) DOSYA tutmayınca COMP4 kararı değişti / tekil sinyal 'GÜÇLÜ' eşiği (2,8) değişti")
    for ad, kol, pay in (("brüt", "brut_tutar_v2", 11), ("net", "tutar_v2", 11)):
        Pk = Pl.copy(); Pk.loc[:pay - 1, kol] = True; kr = K.k59_karar(Zk(), Pk)
        if kr["cetvel"] != "GÜVENİLMEZ" or not kr["bilesik"].startswith("HÜKÜM YOK") or kr["etiket"]:
            hata.append(f"11) plasebo {ad} yanlış pozitif %5,5 iken hüküm verildi: {kr}")
    Pk = Pl.copy(); Pk.loc[:9, "brut_tutar_v2"] = True
    if K.k59_karar(Zk(), Pk)["cetvel"] != "GÜVENİLİR" or not np.isclose(K.k59_karar(Zk(), Pk)["yp_brut"], 0.05):
        hata.append("11) plasebo yanlış pozitif tam %5 iken cetvel güvenilmez sayıldı")
    if not K.k59_karar(Zk(), None)["bilesik"].startswith("HÜKÜM YOK") or not K.k59_karar(Zk(), Pl.iloc[:150])["bilesik"].startswith("HÜKÜM YOK"):
        hata.append("11) plasebo yok / eksik iken hüküm verildi")
    # 12) French birleştirme ve Yahoo ham okuyucu
    with tempfile.TemporaryDirectory() as td:
        ff = ("test\n\n,Mkt-RF,SMB,HML,RMW,CMA,RF\n196307,  -0.39,  -0.41,  -0.97,   0.68,  -1.18,   0.27\n196308,   5.07,  -0.80,   1.80,   0.36,  -0.35,   0.25\n\n"
              " Annual Factors: January-December \n,Mkt-RF,SMB,HML,RMW,CMA,RF\n  1964,  12.0, 1.0, 2.0, 3.0, 4.0, 3.5\n")
        mo = "Momentum test\n\n          ,Mom   \n196307,   0.90\n196308,   1.00\n\n Annual Factors: \n,Mom\n  1964, 10.0\n"
        z1, z2 = os.path.join(td, "ff.zip"), os.path.join(td, "mo.zip")
        with zipfile.ZipFile(z1, "w") as z:
            z.writestr("F-F_Research_Data_5_Factors_2x3.csv", ff)
        with zipfile.ZipFile(z2, "w") as z:
            z.writestr("F-F_Momentum_Factor.csv", mo)
        Fr = K.k59_french({"ff5": z1, "mom": z2})
        if list(Fr.columns) != ["MKT_RF", "SMB", "HML", "RMW", "CMA", "UMD", "RF"] or not np.isclose(Fr.loc[pd.Period("1963-08", "M"), "MKT_RF"], 0.0507) \
                or not np.isclose(Fr.RF.iloc[0], 0.0027) or not np.isclose(Fr.UMD.iloc[1], 0.01):
            hata.append(f"12) French birleştirme (ondalık, RF, UMD) yanlış: {Fr}")
        gun = pd.bdate_range("2020-01-02", periods=300).tz_localize("America/New_York") + pd.Timedelta(hours=9, minutes=30)
        ts = [int(v) for v in (gun - pd.Timestamp("1970-01-01", tz="UTC")) // pd.Timedelta("1s")]
        cl = np.linspace(10, 20, 300).tolist(); cl[5] = None
        J = {"chart": {"result": [{"meta": {"exchangeTimezoneName": "America/New_York", "instrumentType": "EQUITY"}, "timestamp": ts,
                                   "events": {"splits": {str(ts[100]): {"date": ts[100], "numerator": 1.0, "denominator": 10.0, "splitRatio": "1:10"},
                                                         str(ts[200]): {"date": ts[200], "numerator": 3.0, "denominator": 1.0, "splitRatio": "3:1"},
                                                         "x": {"date": ts[50], "numerator": 1.0, "denominator": 1.0}}},
                                   "indicators": {"quote": [{"close": cl}], "adjclose": [{"adjclose": [v and v * 0.9 for v in cl]}]}}]}}
        yy = os.path.join(td, "x.json"); json.dump(J, open(yy, "w"))
        c, b = K.k59_yahoo_ham(yy, "2020-12-31")
        g0 = gun.tz_localize(None).normalize()
        if c is None or b is None or len(c) != int((g0 <= pd.Timestamp("2020-12-31")).sum()) - 1 or not np.isclose(c.iloc[0], 10.0) \
                or not np.allclose(b[1], [0.1, 3.0]) or pd.Timestamp(b[0][0]) != g0[100] or pd.Timestamp(b[0][1]) != g0[200]:
            hata.append(f"12) Yahoo ham okuyucu (temettüsüz kapanış, bölünme oranı, kesik) yanlış: {c is None} {b}")
        open(yy, "w").write('{"yok": 404}')
        if K.k59_yahoo_ham(yy, "2020-12-31") != (None, None) or K.k59_yahoo_ham(os.path.join(td, "yok.json"), "2020-12-31") != (None, None):
            hata.append("12) olmayan / boş Yahoo dosyası hata verdi")
    # 13) uçtan uca sentetik koşu + rapor
    with tempfile.TemporaryDirectory() as td:
        K.k59_onkayit(td, veri_sha={})
        try:
            Ro = K.k59_kos(td, git_sart=False, demetler={"U1": D1, "U2": D2, "BIST": demet(H, "BIST")}, FF=FFs.set_axis(pd.period_range("2015-01", periods=150, freq="M")), E=Et)
            Z = pd.read_csv(K._k59_yol("sonuc", td)); Am = pd.read_csv(K._k59_yol("aylik", td)); Kp = pd.read_csv(K._k59_yol("kapsam", td))
            rt = open(Ro["rapor"], encoding="utf-8").read(); meta = json.load(open(K._k59_yol("meta", td), encoding="utf-8"))
            bek = {(e, s) for e in ("U1", "U2") for s in K.K59_SIRA + list(K.K59_ESIK["bilesik"])} | {("BIST", s) for s in ("S1", "S2", "S3", "S8", "S9", "COMP9")}
            if set(zip(Z.evren, Z.sinyal)) != bek:
                hata.append(f"13) sonuç satırları eksik / fazla: {set(zip(Z.evren, Z.sinyal)) ^ bek}")
            Plc = pd.read_csv(K._k59_yol("plasebo", td)); krc = K.k59_karar(Z, Plc, Et)
            if len(Plc) != 3 or Ro["karar"]["cetvel"] not in ("GÜVENİLİR", "GÜVENİLMEZ") or krc["bilesik"] != Ro["karar"]["bilesik"] or not meta["sentetik"] \
                    or meta["karar"]["bilesik"] != Ro["karar"]["bilesik"] or list(Z.etiket) != [krc["etiket"].get((e, s_), "HÜKÜM YOK") for e, s_ in zip(Z.evren, Z.sinyal)]:
                hata.append("13) plasebo çıktısı / karar çıktılardan yeniden üretilemiyor / sentetik işareti yanlış")
            if "HÜKÜM YOK" not in open(K.k59_rapor(td), encoding="utf-8").read():
                hata.append("13) plasebo eksikken (3 < 200) rapor hüküm verdi")
            g = Am[(Am.evren == "U2") & (Am.sinyal == "COMP4")]; r = Z[(Z.evren == "U2") & (Z.sinyal == "COMP4")].iloc[0]
            c = K.k59_cetvel_v2(g.net.to_numpy(), g.kiyas.to_numpy(), Et["cetvel"])
            if not (np.isclose(r.yillik_fazla, 12 * (g.net - g.kiyas).mean()) and np.isclose(r.nw_t, c["nw_t"]) and np.isclose(r.t_alfa, c["t_alfa"]) and r.ay == len(g)
                    and bool(r.tutar_v2) == c["tutar_v2"] and np.isclose(r.ort_hisse, g.n_hisse.mean())):
                hata.append("13) sonuç satırı aylık getiri dosyasından yeniden üretilemiyor")
            Uz = pd.read_csv(K._k59_yol("ucuzluk", td)); gd_ = Am[(Am.evren == "U1") & (Am.sinyal == "UCUZLUK_dusmus")]; gy_ = Am[(Am.evren == "U1") & (Am.sinyal == "UCUZLUK_yakin")]
            fr = Uz[(Uz.evren == "U1") & Uz.portfoy.str.startswith("fark")]
            if len(Uz) != 6 or set(Uz.evren) != {"U1", "U2"} or not len(gd_) or len(gd_) != len(gy_) or not np.isclose(fr.yillik_fazla.iloc[0], 12 * (gd_.net.to_numpy() - gy_.net.to_numpy()).mean()) \
                    or len(gd_) != int(Z[(Z.evren == "U1") & (Z.sinyal == "COMP4")].ay.iloc[0]) or set(Z.sinyal) & {"UCUZLUK_dusmus", "X1", "X2", "X3"}:
                hata.append("13) UCUZLUK çıktısı eksik / fark aylık dosyadan yeniden üretilemiyor / dönemi COMP4 ile aynı değil / ek bileşen tek başına ölçüldü")
            if Z[Z.sinyal.str.startswith("DOSYA")].rol.ne("DOSYA").any() or set(Ro["karar"].get("dosya", {})) != {f"{e} {d}" for e in ("U1", "U2") for d in K.K59_ESIK["karar"]["dosya"]}:
                hata.append("13) DOSYA ailesi rolü / karar özeti yanlış")
            if Z[(Z.evren == "BIST")].rol.ne("BİLGİ").any() or Z[(Z.evren == "U1") & (Z.sinyal == "COMP4")].rol.iloc[0] != "KARAR" or Z[Z.sinyal == "COMP9"].rol.ne("BİLGİ").any():
                hata.append("13) karar / bilgi rolleri yanlış")
            if Z[(Z.evren == "BIST")].ff_alfa_yillik.notna().any() if "ff_alfa_yillik" in Z else True:
                hata.append("13) BIST'te French alfası hesaplandı / ABD'de hiç hesaplanmadı")
            if not Z[(Z.evren == "U2") & (Z.sinyal == "S1")].ff_alfa_yillik.notna().all():
                hata.append("13) ABD'de FF5 + UMD alfası yok")
            if not {"hisse_ay", "maks_hisse_ay_getiri", "getiri_ust_300_hisse_ay"} <= set(meta["evren"]["U2"]) or "Veri denetimi" not in rt:
                hata.append("13) veri denetimi (en büyük tek hisse getirisi) meta / raporda yok")
            if not {"n_evren", "n_S4", "n_COMP4", "n_X1", "n_X2", "n_X3", "n_DOSYA_Y", "n_DOSYA_D", "n_DOSYA_YD", "S3_olcu"} <= set(Kp.columns) or set(Kp.evren) != {"U1", "U2", "BIST"}:
                hata.append("13) kapsam tablosu eksik")
            for parca in ("## Düz dille", "## Karar", "## U1", "## U2", "## BIST", "## Plasebo", "## Kapsam", "## Sınırlar", "sıradaki üç deneme", "IZ_KARNE önerisi",
                          "## DOSYA ailesi", "## Koşullu test UCUZLUK", "DOSYA_YD", "fark (dusmus - yakin)"):
                if parca not in rt:
                    hata.append(f"13) raporda '{parca}' yok")
            Ok = K.k59_evren_olc(D2, None, Et, yalniz_kapsam=True)
            if Ok["sonuc"] or Ok["aylik"] or Ok["plasebo"] is not None or not len(Ok["kapsam"]):
                hata.append("13) kapsam modu getiri / plasebo hesapladı")
            for f in os.listdir(td):
                if K._K59_EPOSTA.search(open(os.path.join(td, f), encoding="utf-8").read()):
                    hata.append(f"14) sentetik çıktıda e-posta var: {f}")
        except Exception as ex:
            hata.append(f"13) uçtan uca sentetik koşu çöktü: {type(ex).__name__} {ex}")
    # 14) e-posta / anahtar yok
    cik = K.K59_YOL["cikti"]
    dosyalar = [os.path.join(KOK, "K59.py"), os.path.join(KOK, "test_k59.py")] + \
               ([os.path.join(cik, f) for f in os.listdir(cik) if f.endswith((".md", ".csv", ".json"))] if os.path.isdir(cik) else [])
    for y in dosyalar:
        t = open(y, encoding="utf-8").read()
        if re.search(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b", t):
            hata.append(f"14) e-posta var: {os.path.basename(y)}")
        if re.search(r"(api[_-]?key|token|secret|password)\s*[=:]\s*['\"][A-Za-z0-9_\-]{12,}", t, re.I):
            hata.append(f"14) anahtar benzeri dize var: {os.path.basename(y)}")
    return hata


# ================================================================ K59-B testleri (yalnız SENTETİK veri)
K59_MUHUR_SABIT = "6fe8bb38566701f175883f803332524dbbab493561eef3e4c968bfa332c51eb0"      # K59 ön kaydının mührü: K59-B bunu DEĞİŞTİRMEZ
K59_ONKAYIT_SHA = "11560c74c315c676daffea4763861cdbb16001092abd863d2714a9130b4659e9"      # K59_ON_KAYIT.md (git 9e04f3e) dosya sha256'sı
MOM_KOL = ["Lo PRIOR", "PRIOR 2", "PRIOR 3", "PRIOR 4", "PRIOR 5", "PRIOR 6", "PRIOR 7", "PRIOR 8", "PRIOR 9", "Hi PRIOR"]
OP_KOL = ["Lo 30", "Med 40", "Hi 30", "Lo 20", "Qnt 2", "Qnt 3", "Qnt 4", "Hi 20", "Lo 10", "2-Dec", "3-Dec", "4-Dec", "5-Dec", "6-Dec", "7-Dec",
          "8-Dec", "9-Dec", "Hi 10"]


def french_sentetik(td: str, bas: str = "1963-07", n: int = 759, tohum: int = 3, prim: float = 0.45) -> dict:
    """Sentetik French dosyaları (gerçek dosyaların biçimi: açıklama satırları, VW / EW aylık bölümleri, yıllık bölümler, hisse sayısı
    bölümü, eksik kodu) + ondalık faktör tablosu. Döner: zip yolları, FF, yüzde tabloları (elle hesap için)."""
    rng = np.random.default_rng(tohum); ay = pd.period_range(bas, periods=n, freq="M"); mkt = rng.normal(0.9, 4.5, n); rf = np.full(n, 0.3)
    FF = pd.DataFrame({"MKT_RF": mkt - rf, "SMB": rng.normal(0, 2, n), "HML": rng.normal(0, 2, n), "RMW": rng.normal(0, 2, n),
                       "CMA": rng.normal(0, 2, n), "UMD": rng.normal(0, 3, n), "RF": rf}, index=ay) / 100.0
    tab = {}
    for d, kol, ust in (("mom", MOM_KOL, "Hi PRIOR"), ("op", OP_KOL, "Hi 20")):
        for ag in ("vw", "ew"):
            X = pd.DataFrame(mkt[:, None] + rng.normal(0, 1.5, (n, len(kol))), index=ay, columns=kol).round(2)
            X[ust] = (X[ust] + prim).round(2)
            tab[(d, ag)] = X

    def bolum(X: pd.DataFrame, yil: bool = False) -> str:
        sat = ["," + ",".join(X.columns)]
        for p, r in X.iterrows():
            sat.append((f"  {p.year}" if yil else f"{p.year}{p.month:02d}") + "," + ",".join(f"{v:8.2f}" for v in r.to_numpy()))
        return "\n".join(sat)
    yol = {}
    for d, ad, b_vw in (("mom", "10_Portfolios_Prior_12_2", "  Value Weight Returns -- Monthly"), ("op", "Portfolios_Formed_on_OP", "  Average Value Weight Returns -- Monthly")):
        yillik = tab[(d, "vw")].iloc[::12].head(5); say = (tab[(d, "vw")] * 0 + 250).head(24)
        metin = "\n".join(["This file was created using the 202609 CRSP database.", "It contains value- and equal-weighted returns.", "",
                           "Missing data are indicated by -99.99 or -999.", "", "", b_vw, bolum(tab[(d, "vw")]), "", "",
                           "  Average Equal Weighted Returns -- Monthly", bolum(tab[(d, "ew")]), "", "",
                           "  Average Value Weighted Returns -- Annual", bolum(yillik, True), "", "",
                           "  Equal Weight Returns -- Annual from January to December", bolum(yillik, True), "", "",
                           "  Number of Firms in Portfolios", bolum(say), "", "Copyright 2026 Eugene F. Fama and Kenneth R. French", ""])
        yol[d] = os.path.join(td, ad + "_CSV.zip")
        with zipfile.ZipFile(yol[d], "w") as z:
            z.writestr(ad + ".csv", metin)
    return {"yol": yol, "FF": FF, "tab": tab}


def elle_ortusen(Rh: np.ndarray, R: np.ndarray, sec: np.ndarray, U: np.ndarray, maliyet: float, tut: int) -> dict:
    """K59-B (b) muhasebesinin BAĞIMSIZ, sözlük tabanlı benzetimi (K59 kodu kullanılmaz): kohort başına hisse -> ağırlık."""
    n = len(R); koh = [dict() for _ in range(tut)]; out = {"brut": [], "net": [], "devir": [], "kiyas": []}
    sifir = lambda v: 0.0 if not np.isfinite(v) else float(v)  # noqa: E731
    for i in range(n):
        c = i % tut; j_ = np.flatnonzero(sec[i] & U[i]); yeni = {int(j): 1.0 / len(j_) for j in j_}
        d = sum(abs(yeni.get(j, 0.0) - koh[c].get(j, 0.0)) for j in set(yeni) | set(koh[c])); koh[c] = yeni; rb, rn = [], []
        for cc in range(min(tut, i + 1)):
            r = sum(w * sifir(Rh[i, j]) for j, w in koh[cc].items())
            rb.append(r); rn.append((1 - maliyet * (d if cc == c else 0.0)) * (1 + r) - 1)
            koh[cc] = {j: w * (1 + sifir(Rh[i, j])) / (1 + r) for j, w in koh[cc].items()}
        if i >= tut - 1:
            out["brut"].append(np.mean(rb)); out["net"].append(np.mean(rn)); out["devir"].append(d / tut); out["kiyas"].append(np.nanmean(R[i][U[i]]))
    return {k: np.array(v) for k, v in out.items()}


def testler_b() -> list:
    hata = []; B0 = K.K59B_ESIK; nan = np.nan
    # B1) K59 değişmedi; K59-B eşikleri iş tanımındaki gibi
    if K.k59_esik_sha() != K59_MUHUR_SABIT:
        hata.append(f"B1) K59 mührü değişmiş: {K.k59_esik_sha()} (K59-B, K59 eşiklerine dokunamaz)")
    gk = K._k59_yol("onkayit")
    if not os.path.exists(gk) or K58._k58_dosya_sha(gk) != K59_ONKAYIT_SHA:
        hata.append("B1) K59_ON_KAYIT.md değişmiş / yok (dosya sha256 farklı)")
    C0 = B0["c"]
    if not (B0["evren"] == ["U1", "U2"] and B0["sinyal"] == ["COMP4", "DOSYA_Y", "S5", "S1"] and B0["birincil"] == "COMP4" and B0["b"]["tut"] == 3
            and B0["karar"]["t_guclu"] == 2.75 and B0["karar"]["buyukluk_yillik"] == 0.04 and B0["karar"]["deneme"] == 8
            and B0["karar"]["aday"] == "K59-B PORTFÖY-ADAY" and B0["karar"]["degil"] == "TUTMAZ" and B0["plasebo"] == {"evren": "U2", "n": 200, "yp_esik": 0.05, "tohum": {"a": 59100, "b": 59200}}
            and C0["zip"] == {"mom": "10_Portfolios_Prior_12_2_CSV.zip", "op": "Portfolios_Formed_on_OP_CSV.zip"} and C0["kolon"]["mom"] == "Hi PRIOR"
            and C0["kolon"]["op"] == "Hi 20" and C0["kolon"]["mom_hepsi"] == MOM_KOL and C0["agirlik"] == {"mom": 0.5, "op": 0.5} and C0["maliyet_aylik"] == 0.0010
            and [d[:2] for d in C0["donem"]] == [["1963-son", "1963-07"], ["2000-son", "2000-01"], ["2000-09", "2000-01"], ["2010-19", "2010-01"], ["2020-son", "2020-01"]]
            and C0["kok"].startswith("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/") and "K60" in B0["sonraki"]):
        hata.append("B1) K59B_ESIK iş tanımındaki sabitlerle aynı değil")
    for ad_, d_ in (("Value Weight Returns -- Monthly", "vw"), ("Average Value Weight Returns -- Monthly", "vw"), ("Average Equal Weighted Returns -- Monthly", "ew")):
        if not re.match(C0["bolum"][d_], ad_, re.I) or re.match(C0["bolum"]["ew" if d_ == "vw" else "vw"], ad_, re.I):
            hata.append(f"B1) bölüm deseni '{ad_}' başlığını doğru seçmiyor")
    if any(re.match(C0["bolum"][d_], x, re.I) for d_ in ("vw", "ew") for x in ("Average Value Weighted Returns -- Annual", "Equal Weight Returns -- Annual from January to December", "Number of Firms in Portfolios")):
        hata.append("B1) bölüm deseni yıllık / hisse sayısı bölümünü de seçiyor")
    for yasak in ("import K5", "pandas", "numpy", "import os", "subprocess", "open("):
        if yasak in K._K59B_FRENCH_KOD:
            hata.append(f"B1) yalıtılmış French ayrıştırıcısı standart dışı / gereksiz şey içeriyor: {yasak}")
    # B2) ön kayıt: iki mühür
    with tempfile.TemporaryDirectory() as td:
        try:
            K.k59b_onkayit(td, veri_sha={}); hata.append("B2) K59 ön kaydı yokken K59-B ön kaydı yazıldı")
        except K.K59Hata:
            pass
        vs = {"V_ABD.pkl": ("a" * 64, 1), "secframes": ("b" * 64, 7)}
        yk = K.k59_onkayit(td, veri_sha=vs)
        y = K.k59b_onkayit(td, veri_sha={**vs, "10_Portfolios_Prior_12_2_CSV.zip": ("c" * 64, 1)}); ilk = open(y, encoding="utf-8").read()
        if os.path.basename(y) != "K59B_ON_KAYIT.md" or open(yk, encoding="utf-8").read().count("K59B") or K58._k58_dosya_sha(yk) not in ilk:
            hata.append("B2) K59-B ön kaydı ayrı dosya değil / K59 ön kaydına dokundu / K59 ön kaydının dosya sha256'sını yazmadı")
        if f"K59B_ESIK_SHA256: {K.k59b_esik_sha()}" not in ilk or f"K59_ESIK_SHA256: {K.k59_esik_sha()}" not in ilk \
                or not re.search(r"^Yazım zamanı: \d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC", ilk, re.M) or K.k59b_esik_sha() == K.k59_esik_sha():
            hata.append("B2) K59-B ön kaydında iki mühür / UTC zaman yok")
        for parca in ("## Veri", "## 0. Neden", "## 1. K59'dan aynen", "## 2. Tasarım (a)", "## 3. Tasarım (b)", "## 4. Tasarım (c)", "## 5. Plasebo",
                      "## 6. Karar kuralları", "## 7. BOŞLUK listesi", "## 8. Kapsam", "## 9. K59-B'den sonra", "## 10. Değişmezlik", "K59-B PORTFÖY-ADAY", "TUTMAZ", "HÜKÜM YOK",
                      "İZ ilan EDİLEMEZ", "K60", "kör DEĞİLDİR", "ÇOKLU DENEME", "2.75", "Hi PRIOR", "Hi 20", "EW10", "MKT = Mkt-RF + RF", "%0.10 / ay", "al-tut",
                      "KESİN", "bileşik uzun dönemde tutuyor ama 2020 sonrası zayıf", "bileşik uzun dönemde tutuyor ve 2020 sonrası güçlü", "python -I K59.py b_kos",
                      "59100", "59200", "COMP4 (BİRİNCİL)", "1963-07", "2000-01", "2009-12", "2010-01", "2019-12", "2020-01") + tuple(f"BOŞLUK {i}" for i in range(1, 11)):
            if parca not in ilk:
                hata.append(f"B2) K59-B ön kaydında '{parca}' yok")
        oc = K._k59b_onkayit_oku(y)
        if oc["sha"] != K.k59b_esik_sha() or oc["k59_sha"] != K.k59_esik_sha() or len(oc["veri"]) != 3:
            hata.append(f"B2) K59-B ön kaydından mühürler / veri sha256'ları okunamadı: {oc}")
        K.k59b_onkayit(td)
        if open(y, encoding="utf-8").read() != ilk:
            hata.append("B2) K59-B ön kaydı üzerine yazıldı")
        d = K.k59b_onkayit_dogrula(td)
        if d["sha"] != K.k59b_esik_sha() or d["k59_sha"] != K59_MUHUR_SABIT or d["k59"]["dosya_sha256"] != K58._k58_dosya_sha(yk):
            hata.append("B2) K59-B doğrulaması iki mührü / K59 ön kaydını döndürmüyor")
        for ad, kw in (("verisi ön kayıttan farklı", {"veri": True}), ("git'e işlenmemiş", {"git": True})):
            try:
                K.k59b_onkayit_dogrula(td, **kw); hata.append(f"B2) {ad} K59-B ön kaydı kabul edildi")
            except K.K59Hata:
                pass
        for ad, eski, yeni in (("K59-B mührü bozuk", f"K59B_ESIK_SHA256: {K.k59b_esik_sha()}", "K59B_ESIK_SHA256: " + "0" * 64),
                               ("içindeki K59 mührü farklı", f"K59_ESIK_SHA256: {K.k59_esik_sha()}", "K59_ESIK_SHA256: " + "0" * 64),
                               ("K59 kaynağının veri özeti K59 ön kaydından farklı", "- V_ABD.pkl: sha256 " + "a" * 64, "- V_ABD.pkl: sha256 " + "d" * 64)):
            open(y, "w", encoding="utf-8").write(ilk.replace(eski, yeni))
            try:
                K.k59b_onkayit_dogrula(td); hata.append(f"B2) {ad} iken doğrulama geçti")
            except K.K59Hata:
                pass
        open(y, "w", encoding="utf-8").write(ilk.replace(f"K59B_ESIK_SHA256: {K.k59b_esik_sha()}", "K59B_ESIK_SHA256: " + "0" * 64))
        try:
            K.k59b_onkayit(td); hata.append("B2) mührü farklı K59-B ön kaydı sessizce kabul edildi")
        except K.K59Hata:
            pass
        open(y, "w", encoding="utf-8").write(ilk); kt = open(yk, encoding="utf-8").read()
        open(yk, "w", encoding="utf-8").write(kt.replace(K.k59_esik_sha(), "0" * 64))
        try:
            K.k59b_onkayit_dogrula(td); hata.append("B2) K59 ön kaydının mührü bozukken K59-B doğrulaması geçti")
        except K.K59Hata:
            pass
        os.remove(yk)
        try:
            K.k59b_onkayit_dogrula(td); hata.append("B2) K59 ön kaydı yokken K59-B doğrulaması geçti")
        except K.K59Hata:
            pass
    Bx = copy.deepcopy(B0); Bx["karar"]["t_guclu"] = 2.7
    By = copy.deepcopy(B0); By["b"]["tut"] = 6
    Ex = copy.deepcopy(K.K59_ESIK); Ex["cetvel"]["t_esik"] = 1.9
    if len({K.k59b_esik_sha(), K.k59b_esik_sha(Bx), K.k59b_esik_sha(By), K.k59b_esik_sha(None, Ex)}) != 4 or K.k59b_esik_sha() != K.k59b_esik_sha(copy.deepcopy(B0)):
        hata.append("B2) K59B_ESIK ya da K59_ESIK değişince K59-B mührü değişmiyor / aynı eşikte mühür farklı")
    gb = K._k59b_yol("onkayit")
    if not os.path.exists(gb):
        hata.append("B2) arastirma_cikti/k59_basit_sinyaller/K59B_ON_KAYIT.md yok")
    else:
        try:
            oc = K.k59b_onkayit_dogrula(); gt = open(gb, encoding="utf-8").read()
            if not oc["zaman_utc"] or len(oc["veri"]) < 10 or not set(C0["zip"].values()) <= set(oc["veri"]) or K59_ONKAYIT_SHA not in gt \
                    or "HENÜZ YAPILMADI" in gt or pd.Timestamp(oc["zaman_utc"]) <= pd.Timestamp(oc["k59"]["zaman_utc"]):
                hata.append(f"B2) gerçek K59-B ön kaydında UTC zaman / veri sha256 (iki French zip dahil) / K59 dosya sha256 / kapsam notu eksik ({len(oc['veri'])} kaynak)")
            my = K._k59b_yol("meta")
            if os.path.exists(my):
                meta = json.load(open(my, encoding="utf-8"))
                if pd.Timestamp(oc["zaman_utc"]) > pd.Timestamp(meta["kos_baslangic"].replace(" UTC", "")) or meta["onkayit"]["sha"] != oc["sha"]:
                    hata.append("B2) K59-B ön kaydı koşudan sonra yazılmış / koşu başka mühürle yapılmış")
        except K.K59Hata as ex:
            hata.append(f"B2) gerçek K59-B ön kaydı bugünkü eşiklerle aynı değil: {ex}")
    # ortak sentetik panel
    H = sentetik_ham(); D2 = demet(H, "U2"); D1 = demet(H, "U1")
    Et = copy.deepcopy(K.K59_ESIK); Et["cetvel"]["min_ay"] = 24
    Bt = copy.deepcopy(B0); Bt["plasebo"]["n"] = 3
    with tempfile.TemporaryDirectory() as td:
        K.k59_onkayit(td, veri_sha={})
        try:
            K.k59b_kos(td, git_sart=False, demetler={"U2": D2}, E=Et, B=Bt); hata.append("B2) K59-B ön kaydı yokken b_kos durmadı")
        except K.K59Hata:
            pass
        K.k59b_onkayit(td, veri_sha={})
        try:
            K.k59b_kos(td, git_sart=True, demetler={"U2": D2}, E=Et, B=Bt); hata.append("B2) git'e işlenmemiş K59-B ön kaydıyla b_kos durmadı")
        except K.K59Hata:
            pass
    # B3) (a) alt evren
    Pk = {"evren": {"min_evren": 2}, "U": np.array([[1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0]], bool), "olusum": np.array([True, True, True]),
          "R": np.arange(21.0).reshape(3, 7) / 100}
    Pk["R"] = np.where(Pk["U"], Pk["R"], nan)
    S3k = -np.array([[5.0, 1.0, 3.0, nan, 2.0, 3.0, 9.0], [5.0, 1.0, 3.0, 4.0, 2.0, 3.5, 9.0], [5.0, 1.0, nan, nan, nan, nan, nan]])
    Ak = K.k59b_alt_evren(Pk, S3k)
    if not (np.array_equal(Ak["U"], np.array([[0, 1, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0]], bool)) and list(Ak["olusum"]) == [True, True, False]
            and np.allclose(Ak["boyut_medyan"], [3.0, 3.5, 3.0]) and np.isnan(Ak["R"][~Ak["U"]]).all() and np.allclose(Ak["R"][Ak["U"]], Pk["R"][Ak["U"]])
            and np.array_equal(Pk["U"][0], [1, 1, 1, 1, 1, 1, 0]) and Ak["U_tam"] is Pk["U"]):
        hata.append(f"B3) alt evren kuralı (medyanın KESİN altı, boyutu olmayan / uygun olmayan dışarıda, küçük ay atlanır, özgün panel bozulmaz) yanlış: {Ak['U']}")
    P2 = K.k59_panel(D2); S2, ek2 = K.k59_sinyaller(D2, P2); Pa = K.k59b_alt_evren(P2, S2["S3"])
    Sa = K.k59b_sinyal_seti(S2, ek2, Pa["U"]); Sb = K.k59b_sinyal_seti(S2, ek2, P2["U"]); me = P2["ay_sonu"]
    k0 = int(np.flatnonzero(Pa["olusum"])[26]); t0 = me[k0]
    havuz = {**S2, **ek2["bilesen"]}; Bk = K.K59_ESIK["bilesik"]
    if set(Sa) != set(B0["sinyal"]) or set(Sb) != set(B0["sinyal"]):
        hata.append(f"B3) dört sinyal üretilemedi: {set(Sa)} {set(Sb)}")
    else:
        boy = -S2["S3"]; ua, u = Pa["U"][k0], P2["U"][k0]; var = u & np.isfinite(boy[k0])
        if not ((ua & ~u).sum() == 0 and ua.sum() == var.sum() // 2 and boy[k0][ua].max() < np.median(boy[k0][var]) <= boy[k0][var & ~ua].min()
                and (Pa["U"].sum(axis=1)[Pa["olusum"]] >= 30).all() and not Pa["U"][~Pa["olusum"]].any()):
            hata.append("B3) sentetik panelde alt evren uygun evrenin boyutça alt yarısı değil")
        if not np.allclose(Sb["COMP4"], K.k59_bilesik(havuz, P2["U"], Bk["COMP4"]["uye"], 3), equal_nan=True) \
                or not np.allclose(Sb["DOSYA_Y"], K.k59_bilesik(havuz, P2["U"], Bk["DOSYA_Y"]["uye"], 4), equal_nan=True) \
                or not np.allclose(Sb["S1"], S2["S1"], equal_nan=True) or not np.allclose(Sb["S5"], S2["S5"], equal_nan=True):
            hata.append("B3) tam evrende K59-B sinyalleri K59'un sinyalleri / bileşikleriyle birebir aynı değil")
        j = np.flatnonzero(ua)
        Y4 = np.stack([np.where(np.isfinite(S2[a][k0, j]), (pd.Series(S2[a][k0, j]).rank().to_numpy() - 0.5) / max(1, np.isfinite(S2[a][k0, j]).sum()), nan)
                       for a in Bk["COMP4"]["uye"]])
        say4 = np.isfinite(Y4).sum(axis=0); elle = np.where(say4 >= 3, np.nansum(Y4, axis=0) / np.maximum(say4, 1), nan)
        if not np.allclose(Sa["COMP4"][k0, j], elle, equal_nan=True) or np.isfinite(Sa["COMP4"][k0, ~ua]).any() or np.isfinite(Sa["S1"][~Pa["U"]]).any() \
                or np.allclose(Sa["COMP4"][k0, j], Sb["COMP4"][k0, j], equal_nan=True):
            hata.append("B3) (a) bileşik sıraları alt evren İÇİNDE yeniden hesaplanmıyor / alt evren dışına sinyal sızıyor")
        row_a, A_a = K.k59_sinyal_olc(Pa, Sa["COMP4"], None, Et)
        g = A_a[A_a.ay_sonu == str(t0.date())]; jj = j[np.isfinite(Sa["COMP4"][k0, j])]; m_ = max(1, int(round(0.10 * len(jj))))
        ust = jj[np.argsort(-Sa["COMP4"][k0, jj], kind="stable")][:m_]
        if len(g) != 1 or not (np.isclose(g.brut.iloc[0], P2["R"][k0, ust].mean()) and np.isclose(g.kiyas.iloc[0], P2["R"][k0, ua].mean())
                               and g.n_evren.iloc[0] == ua.sum() and g.n_hisse.iloc[0] == m_ and g.n_sinyal.iloc[0] == len(jj)):
            hata.append("B3) (a) portföyü (alt evrende üst %10) / kıyası (alt evrenin eşit ağırlıklısı) elle hesapla aynı değil")
        Hb = boz(H, t0); Db = demet(Hb, "U2"); Pb = K.k59_panel(Db); Sbz, ekb = K.k59_sinyaller(Db, Pb); Pab = K.k59b_alt_evren(Pb, Sbz["S3"])
        Sab = K.k59b_sinyal_seti(Sbz, ekb, Pab["U"])
        if not np.array_equal(Pa["U"][:k0 + 1], Pab["U"][:k0 + 1]) or np.array_equal(Pa["U"][k0 + 6:], Pab["U"][k0 + 6:]):
            hata.append("B3) (a) alt evren ay sonu t'den sonrasını görüyor (geleceğe bakma) / bozma testi etkisiz")
        for a in B0["sinyal"]:
            if not np.allclose(Sa[a][:k0 + 1], Sab[a][:k0 + 1], equal_nan=True):
                hata.append(f"B3) (a) {a} ay sonu t'den sonraki veriyi görüyor (geleceğe bakma)")
        _, A_ab = K.k59_sinyal_olc(Pab, Sab["COMP4"], None, Et)
        o1, o2 = A_a[A_a.getiri_ayi <= str(t0.to_period("M"))], A_ab[A_ab.getiri_ayi <= str(t0.to_period("M"))]
        if len(o1) < 10 or len(o1) != len(o2) or not np.allclose(o1[["brut", "net", "kiyas", "devir"]].to_numpy(), o2[["brut", "net", "kiyas", "devir"]].to_numpy()):
            hata.append("B3) (a) t'ye kadar gerçekleşen aylık getiriler t'den sonraki veriyle değişti")
    # B4) (b) örtüşen kohortlar
    rng = np.random.default_rng(7); n_, N_ = 9, 12
    R = rng.normal(0.01, 0.06, (n_, N_)); U = np.ones((n_, N_), bool); U[3:, 2] = False; U[:, 11] = False       # 2 numaralı hisse 4. aydan sonra uygun değil
    Rh = R.copy(); R = np.where(U, R, nan)
    sec = np.zeros((n_, N_), bool)
    for i in range(n_):
        sec[i, rng.choice(11, 3, replace=False)] = True
    sec[0, [1, 2, 3]] = True; sec[0, [0] + list(range(4, 11))] = False; sec[3] = False; sec[3, [1, 2, 5]] = True        # 3. ayda 2 seçili ama uygun değil
    ol = np.ones(n_, bool)
    Pf = K.k59b_ortusen_portfoy(Rh, R, sec, U, ol, 0.001, 3); El = elle_ortusen(Rh, R, sec, U, 0.001, 3)
    for kol in ("brut", "net", "devir", "kiyas"):
        if len(Pf[kol]) != n_ - 2 or not np.allclose(Pf[kol], El[kol]):
            hata.append(f"B4) örtüşen kohort muhasebesi bağımsız elle benzetimle aynı değil ({kol}): {Pf[kol]} != {El[kol]}")
    w0 = np.zeros(N_); w0[[1, 2, 3]] = 1 / 3; r0 = [float(w0 @ Rh[0])]; w1 = w0 * (1 + Rh[0]) / (1 + r0[0]); r0.append(float(w1 @ Rh[1]))
    w2 = w1 * (1 + Rh[1]) / (1 + r0[1]); r0.append(float(w2 @ Rh[2]))
    if not (np.isclose(Pf["kohort_brut"][0, 0], r0[2]) and np.isclose(Pf["kohort_net"][0, 0], r0[2]) and Pf["kohort_devir"][0, 0] == 0
            and np.isclose(Pf["kohort_devir"][0, 2], 1.0) and np.isclose(Pf["kohort_net"][0, 2], (1 - 0.001) * (1 + Pf["kohort_brut"][0, 2]) - 1)
            and np.isclose(Pf["devir"][0], 1 / 3) and np.isclose(Pf["brut"][0], Pf["kohort_brut"][0].mean()) and list(Pf["ay_idx"]) == list(range(2, n_))):
        hata.append("B4) al-tut (3. ayda kaymış ağırlıkla getiri, ara ayda işlem / maliyet yok), ilk kuruluş devri 1, ilk iki ayın dışarıda kalması yanlış")
    w3 = w2 * (1 + Rh[2]) / (1 + r0[2]); y3 = np.zeros(N_); y3[[1, 5]] = 0.5
    if not np.isclose(Pf["kohort_devir"][1, 0], np.abs(y3 - w3).sum()) or not np.isclose(Pf["kohort_brut"][1, 0], (Rh[3, 1] + Rh[3, 5]) / 2):
        hata.append("B4) yenilemede devir Σ|w_yeni - w_kaymış| değil / uygun olmayan hisse yeni kohorta girdi")
    U_t = U.copy(); U_t[1:3, 2] = False; R_t = np.where(U_t, Rh, nan)                     # 2 numaralı hisse tutulurken uygunluğu yitiriyor
    Pf_t = K.k59b_ortusen_portfoy(Rh, R_t, sec, U_t, ol, 0.001, 3)
    if not np.isclose(Pf_t["kohort_brut"][0, 0], r0[2]) or np.isclose(Pf_t["kiyas"][0], Pf["kiyas"][0]):
        hata.append("B4) tutulan hisse uygunluğu yitirince satıldı / kıyas uygun evrenden hesaplanmıyor")
    for tut in (1, 2, 3):
        a_ = K.k59b_ortusen_portfoy(Rh, R, sec, U, ol, 0.001, tut)
        if len(a_["net"]) != n_ - tut + 1 or not np.allclose(a_["net"], elle_ortusen(Rh, R, sec, U, 0.001, tut)["net"]):
            hata.append(f"B4) tut = {tut}: ay sayısı / net getiri bağımsız benzetimle aynı değil")
    b_ = K58.k58_portfoy(R, sec, U, ol, 0.001); a_ = K.k59b_ortusen_portfoy(Rh, R, sec, U, ol, 0.001, 1)
    if not all(np.allclose(a_[kol], b_[kol]) for kol in ("brut", "net", "devir", "kiyas")):
        hata.append("B4) tut = 1 iken örtüşen kohort K58 k58_portfoy ile birebir aynı değil")
    try:
        K.k59b_ortusen_portfoy(Rh, R, sec, U, np.array([1, 1, 1, 0, 1, 1, 1, 1, 1], bool), 0.001, 3); hata.append("B4) kesintili oluşum aylarında durmadı")
    except K.K59Hata:
        pass
    Rh2 = K.k59b_tutma_getiri(P2); j5 = P2["sembol"].index("S005")
    if not np.allclose(Rh2[P2["U"]], P2["R"][P2["U"]]) or Rh2.shape != P2["R"].shape or not np.isfinite(Rh2[:-1][~P2["U"][:-1] & np.isfinite(P2["Cm"].to_numpy(float)[:-1])]).all() \
            or P2["U"][:, j5].all() or not np.isfinite(Rh2[:-1, j5]).all():
        hata.append("B4) tutma getirisi uygun hissede K59 ay getirisiyle aynı değil / uygun olmayan (ama fiyatı olan) hissede yok")
    row_k, A_k = K.k59_sinyal_olc(P2, Sb["COMP4"], None, Et); row_b, A_b = K.k59b_ortusen_olc(P2, Rh2, Sb["COMP4"], None, Et, B0)
    if not (row_b["ay"] == row_k["ay"] - 2 and len(A_b) == len(A_k) - 2 and list(A_b.ay_sonu) == list(A_k.ay_sonu)[2:] and np.allclose(A_b.kiyas, A_k.kiyas.to_numpy()[2:])
            and list(A_b.n_sinyal) == list(A_k.n_sinyal)[2:] and row_b["ort_devir"] < row_k["ort_devir"] and row_b["ort_hisse"] > row_k["ort_hisse"] and row_b["olculdu"]):
        hata.append(f"B4) (b) ölçüm dönemi (K59 - 2 ay), kıyas (K59 ile aynı), devir (daha düşük) / hisse sayısı (daha çok) beklenen gibi değil: {row_b['ay']} {row_k['ay']}")
    idx = np.flatnonzero(P2["olusum"] & ((P2["U"] & np.isfinite(Sb["COMP4"])).sum(axis=1) >= 20)); i0 = int(idx[0])
    secK = K58.k58_ust_dilim(np.where(P2["U"], Sb["COMP4"], nan), P2["U"] & np.isfinite(Sb["COMP4"]), 0.10); olK = P2["olusum"].copy(); olK[:i0] = False
    ElK = elle_ortusen(Rh2[olK], P2["R"][olK], secK[olK], P2["U"][olK], 0.001, 3)
    if len(A_b) != len(ElK["net"]) or not np.allclose(A_b.net, ElK["net"]) or not np.allclose(A_b.brut, ElK["brut"]) or not np.allclose(A_b.devir, ElK["devir"]):
        hata.append("B4) (b) sentetik panelde COMP4 aylık serisi bağımsız benzetimle aynı değil")
    Pbz = K.k59_panel(Db); Sbz2, ekbz = K.k59_sinyaller(Db, Pbz); _, A_bz = K.k59b_ortusen_olc(Pbz, K.k59b_tutma_getiri(Pbz), K.k59b_sinyal_seti(Sbz2, ekbz, Pbz["U"])["COMP4"], None, Et, B0)
    o1, o2 = A_b[A_b.getiri_ayi <= str(t0.to_period("M"))], A_bz[A_bz.getiri_ayi <= str(t0.to_period("M"))]
    if len(o1) < 10 or len(o1) != len(o2) or not np.allclose(o1[["brut", "net", "kiyas", "devir"]].to_numpy(), o2[["brut", "net", "kiyas", "devir"]].to_numpy()) \
            or (len(A_b) == len(A_bz) and np.allclose(A_b.net.to_numpy()[len(o1) + 3:], A_bz.net.to_numpy()[len(o1) + 3:])):
        hata.append("B4) (b) t'ye kadar gerçekleşen aylık getiriler t'den sonraki veriyle değişti (geleceğe bakma) / bozma testi etkisiz")
    if K.k59b_ortusen_olc(P2, Rh2, np.full(P2["U"].shape, nan), None, Et, B0)[0].get("olculdu") is not False:
        hata.append("B4) sinyali olmayan evren (b)'de ölçüldü sayıldı")
    # B5) (c) French
    with tempfile.TemporaryDirectory() as td:
        Fs = french_sentetik(td); tab = Fs["tab"]; FF = Fs["FF"]
        Dm = K.k59b_french_bolum(Fs["yol"]["mom"], C0["bolum"]["vw"]); De = K.k59b_french_bolum(Fs["yol"]["op"], C0["bolum"]["ew"])
        if list(Dm.columns) != MOM_KOL or list(De.columns) != OP_KOL or len(Dm) != 759 or str(Dm.index[0]) != "1963-07" or str(Dm.index[-1]) != "2026-09" \
                or not np.allclose(Dm.to_numpy(), tab[("mom", "vw")].to_numpy() / 100) or not np.allclose(De.to_numpy(), tab[("op", "ew")].to_numpy() / 100):
            hata.append("B5) French bölüm ayrıştırıcısı doğru aylık bölümü (VW / EW; yıllık ve hisse sayısı bölümleri hariç) ondalık olarak vermiyor")
        A = K.k59b_french_seri(Fs["yol"], FF); Zc = K.k59b_french_olc(A)
        bek_vw = 0.5 * tab[("mom", "vw")]["Hi PRIOR"] / 100 + 0.5 * tab[("op", "vw")]["Hi 20"] / 100
        bek_ew = 0.5 * tab[("mom", "ew")]["Hi PRIOR"] / 100 + 0.5 * tab[("op", "ew")]["Hi 20"] / 100
        if not (len(A) == 759 and np.allclose(A.harman_vw, bek_vw) and np.allclose(A.harman_ew, bek_ew) and np.allclose(A.MKT, FF.MKT_RF + FF.RF)
                and np.allclose(A.EW10, tab[("mom", "ew")][MOM_KOL].mean(axis=1) / 100)):
            hata.append("B5) French harmanı (0,5 x momentum üst onluğu + 0,5 x kârlılık üst beşliği), MKT = Mkt-RF + RF ya da EW10 yanlış")
        if list(Zc.varyant.unique()) != ["VW_MKT", "EW_EW10", "EW_MKT"] or len(Zc) != 15 or list(Zc[Zc.varyant == "VW_MKT"].donem) != [d[0] for d in C0["donem"]] \
                or list(Zc[Zc.varyant == "VW_MKT"].ay) != [759, 321, 120, 120, 81] or set(Zc[Zc.varyant == "EW_MKT"].rol) != {"BİLGİ"}:
            hata.append(f"B5) French ölçüm tablosu (3 varyant x 5 dönem, ay sayıları) yanlış: {list(Zc.ay)}")
        else:
            for v, hk, kk, dn, a, b in (("VW_MKT", "harman_vw", "MKT", "2010-19", "2010-01", "2019-12"), ("EW_EW10", "harman_ew", "EW10", "2000-son", "2000-01", "2026-09")):
                g = A[(A.index >= pd.Period(a, "M")) & (A.index <= pd.Period(b, "M"))]; r = Zc[(Zc.varyant == v) & (Zc.donem == dn)].iloc[0]
                cn = K.k59_cetvel_v2(g[hk].to_numpy() - 0.001, g[kk].to_numpy(), K.K59_ESIK["cetvel"]); cb = K.k59_cetvel_v2(g[hk].to_numpy(), g[kk].to_numpy(), K.K59_ESIK["cetvel"])
                if not (np.isclose(r.yillik_fazla, 12 * (g[hk] - 0.001 - g[kk]).mean()) and np.isclose(r.brut_yillik_fazla - r.yillik_fazla, 0.012) and np.isclose(r.nw_t, cn["nw_t"])
                        and np.isclose(r.t_alfa, cn["t_alfa"]) and bool(r.tutar_v2) == cn["tutar_v2"] and bool(r.brut_tutar_v2) == cb["tutar_v2"] and r.ilk == a and r.son == b):
                    hata.append(f"B5) French {v} {dn}: cetvel v2 / sabit maliyet (%0,10 / ay) / dönem sınırı elle hesapla aynı değil")
        ok = K.k59b_french_okuma(Zc)
        if set(ok) != {"VW_MKT", "EW_EW10"} or not all(x.startswith("bileşik uzun dönemde") for x in ok.values()):
            hata.append(f"B5) French okuması yalnız iki ANA varyant için üretilmiyor: {ok}")
        tab2 = french_sentetik(os.path.join(td), tohum=5)["tab"]
        Xe = tab2[("mom", "ew")].copy(); Xe.iloc[5, 3] = -99.99; Xe.iloc[7, 9] = -999.0
        with zipfile.ZipFile(os.path.join(td, "eksik.zip"), "w") as z:
            z.writestr("x.csv", "aciklama\n\n  Average Equal Weighted Returns -- Monthly\n," + ",".join(MOM_KOL) + "\n" + "\n".join(
                f"{p.year}{p.month:02d}," + ",".join(f"{v:.2f}" for v in r.to_numpy()) for p, r in Xe.iterrows()) + "\n\n  Average Equal Weighted Returns -- Annual\n,a\n 1964, 1.0\n")
        Dx = K.k59b_french_bolum(os.path.join(td, "eksik.zip"), C0["bolum"]["ew"])
        if not (np.isnan(Dx.iloc[5, 3]) and np.isnan(Dx.iloc[7, 9]) and int(Dx.isna().sum().sum()) == 2):
            hata.append("B5) French eksik değer kodları (-99.99 / -999) NaN yapılmıyor")
        for ad, icerik, desen in (("bölüm yok", "x\n\n  Value Weight Returns -- Annual\n,a\n 1964, 1.0\n", C0["bolum"]["vw"]),
                                  ("iki eşleşme", "  Value Weight Returns -- Monthly\n,a\n196307, 1.0\n\n  Average Value Weighted Returns -- Monthly\n,a\n196307, 1.0\n", C0["bolum"]["vw"]),
                                  ("aylık satır yok", "  Value Weight Returns -- Monthly\n,a\n 1964, 1.0\n", C0["bolum"]["vw"])):
            yz = os.path.join(td, "bozuk.zip")
            with zipfile.ZipFile(yz, "w") as z:
                z.writestr("x.csv", icerik)
            try:
                K.k59b_french_bolum(yz, desen); hata.append(f"B5) bozuk French dosyası ({ad}) kabul edildi")
            except K.K59Hata:
                pass
        open(os.path.join(td, "duz.zip"), "w").write("zip degil")
        try:
            K.k59b_french_bolum(os.path.join(td, "duz.zip"), C0["bolum"]["vw"]); hata.append("B5) zip olmayan dosya kabul edildi")
        except K.K59Hata:
            pass
        try:
            K.k59b_french_seri(Fs["yol"], FF.drop(FF.index[100])); hata.append("B5) ardışık olmayan French aylarında durmadı")
        except K.K59Hata:
            pass

    def Zf(u1: bool, u2: bool, son: float, olc: bool = True) -> pd.DataFrame:
        return pd.DataFrame([{"varyant": v, "donem": d, "olculdu": olc, "tutar_v2": t_, "ort_aylik": o_} for v in ("VW_MKT", "EW_EW10", "EW_MKT")
                             for d, t_, o_ in (("1963-son", u1, 0.002), ("2000-son", u2, 0.001), ("2000-09", False, 0.0), ("2010-19", False, 0.0), ("2020-son", False, son))])
    for ad, Z_, bek in (("tutuyor + güçlü", Zf(True, True, 0.001), "bileşik uzun dönemde tutuyor ve 2020 sonrası güçlü"),
                        ("tutuyor + zayıf", Zf(True, True, -0.001), "bileşik uzun dönemde tutuyor ama 2020 sonrası zayıf"),
                        ("sıfır = zayıf", Zf(True, True, 0.0), "bileşik uzun dönemde tutuyor ama 2020 sonrası zayıf"),
                        ("2000 sonrası tutmuyor", Zf(True, False, 0.001), "bileşik uzun dönemde tutmuyor (1963-son: TUTAR, 2000-son: TUTMAZ); 2020 sonrası güçlü"),
                        ("ikisi de tutmuyor", Zf(False, False, -0.001), "bileşik uzun dönemde tutmuyor (1963-son: TUTMAZ, 2000-son: TUTMAZ); 2020 sonrası zayıf")):
        ok = K.k59b_french_okuma(Z_)
        if ok != {"VW_MKT": bek, "EW_EW10": bek}:
            hata.append(f"B5) önceden yazılı okuma '{ad}': {ok}")
    if not K.k59b_french_okuma(Zf(True, True, 0.001, olc=False))["VW_MKT"].startswith("ÖLÇÜLEMEDİ") or K.k59b_french_okuma(None) != {}:
        hata.append("B5) ölçülemeyen / olmayan French tablosunda okuma üretildi")
    # B6) karar kuralları
    Pl = pd.DataFrame([{"tasarim": t, "plasebo": i, "tutar_v2": False, "brut_tutar_v2": False} for t in ("a", "b") for i in range(200)])

    def Zk(**deg) -> pd.DataFrame:
        sat = [{"tasarim": t, "evren": e, "sinyal": s, "olculdu": True, "tutar_v2": False, "nw_t": 2.5, "t_alfa": 2.3, "yillik_fazla": 0.06}
               for t in ("a", "b") for e in ("U1", "U2") for s in B0["sinyal"]]
        for (t, e, s), d in deg.get("d", {}).items():
            for r in sat:
                if r["tasarim"] in t and r["evren"] in e and r["sinyal"] == s:
                    r.update(d)
        return pd.DataFrame(sat)
    tut_ = {"tutar_v2": True}; iki = ("U1", "U2")
    for ad, Z_, Pl_, bek_k, bek_s in (
            ("hiçbiri", Zk(), Pl, "TUTMAZ", {("a", "COMP4"): "TUTMAZ (U1 TUTMAZ, U2 TUTMAZ)"}),
            ("(a) aday", Zk(d={("a", iki, "COMP4"): tut_}), Pl, "K59-B PORTFÖY-ADAY (COMP4 tasarım (a) iki evrende tutar)", {("a", "COMP4"): "TUTAR", ("b", "COMP4"): "TUTMAZ (U1 TUTMAZ, U2 TUTMAZ)"}),
            ("(b) aday", Zk(d={("b", iki, "COMP4"): tut_}), Pl, "K59-B PORTFÖY-ADAY (COMP4 tasarım (b) iki evrende tutar)", {("b", "COMP4"): "TUTAR"}),
            ("ikisi de", Zk(d={("ab", iki, "COMP4"): tut_}), Pl, "K59-B PORTFÖY-ADAY (COMP4 tasarım (a), (b) iki evrende tutar)", {}),
            ("tek evren", Zk(d={("a", ("U2",), "COMP4"): tut_}), Pl, "TUTMAZ", {("a", "COMP4"): "TUTMAZ (U1 TUTMAZ, U2 TUTAR (yineleme))"}),
            ("farklı tasarımlarda birer evren", Zk(d={("a", ("U1",), "COMP4"): tut_, ("b", ("U2",), "COMP4"): tut_}), Pl, "TUTMAZ", {}),
            ("küçük", Zk(d={("a", iki, "COMP4"): tut_, ("a", ("U2",), "COMP4"): {"tutar_v2": True, "yillik_fazla": 0.039}}), Pl, "TUTMAZ",
             {("a", "COMP4"): "TUTMAZ (küçük: iki evrende cetvel v2 tutar ama net yıllık fazla < +4 puan)"}),
            ("tam %4", Zk(d={("a", iki, "COMP4"): {"tutar_v2": True, "yillik_fazla": 0.04}}), Pl, "K59-B PORTFÖY-ADAY (COMP4 tasarım (a) iki evrende tutar)", {}),
            ("ölçülemedi", Zk(d={("a", iki, "COMP4"): tut_, ("a", ("U1",), "COMP4"): {"olculdu": False}}), Pl, "TUTMAZ", {("a", "COMP4"): "TUTMAZ (U1 ÖLÇÜLEMEDİ, U2 TUTAR (yineleme))"}),
            ("öteki sinyaller karara girmez", Zk(d={("ab", iki, "S1"): tut_, ("ab", iki, "S5"): tut_, ("ab", iki, "DOSYA_Y"): tut_}), Pl, "TUTMAZ",
             {("a", "S1"): "TUTAR", ("b", "DOSYA_Y"): "TUTAR"}),
            ("güçlü", Zk(d={("b", iki, "COMP4"): {"tutar_v2": True, "nw_t": 2.76, "t_alfa": 2.8}}), Pl, "K59-B PORTFÖY-ADAY (COMP4 tasarım (b) iki evrende tutar)", {("b", "COMP4"): "GÜÇLÜ"}),
            ("tam 2,75 güçlü değil", Zk(d={("b", iki, "COMP4"): {"tutar_v2": True, "nw_t": 2.75, "t_alfa": 3.5}}), Pl, "K59-B PORTFÖY-ADAY (COMP4 tasarım (b) iki evrende tutar)", {("b", "COMP4"): "TUTAR"}),
            ("tek evrende güçlü", Zk(d={("b", iki, "COMP4"): tut_, ("b", ("U1",), "COMP4"): {"tutar_v2": True, "nw_t": 3.0, "t_alfa": 3.0}}), Pl,
             "K59-B PORTFÖY-ADAY (COMP4 tasarım (b) iki evrende tutar)", {("b", "COMP4"): "TUTAR"})):
        kr = K.k59b_karar(Z_, Pl_)
        if kr["karar"] != bek_k or any(kr["sinyal"][k_] != v_ for k_, v_ in bek_s.items()) or kr["cetvel"] != {"a": "GÜVENİLİR", "b": "GÜVENİLİR"}:
            hata.append(f"B6) karar '{ad}': {kr['karar']} / {[kr['sinyal'][k_] for k_ in bek_s]} (beklenen {bek_k} / {list(bek_s.values())})")
    kr = K.k59b_karar(Zk(d={("b", iki, "COMP4"): {"tutar_v2": True, "nw_t": 2.9, "t_alfa": 2.9}, ("a", ("U1",), "S1"): {"tutar_v2": True, "yillik_fazla": 0.02}}), Pl)
    if kr["etiket"][("b", "U1", "COMP4")] != "GÜÇLÜ" or kr["etiket"][("a", "U1", "S1")] != "TUTAR (yineleme)" or not kr["kucuk"][("a", "U1", "S1")] or kr["kucuk"][("b", "U1", "COMP4")]:
        hata.append("B6) evren düzeyi etiket (GÜÇLÜ > 2,75; küçük işareti) yanlış")
    Za = Zk(d={("ab", iki, "COMP4"): tut_})
    Pa_ = Pl.copy(); Pa_.loc[(Pa_.tasarim == "a") & (Pa_.plasebo < 11), "brut_tutar_v2"] = True; kr = K.k59b_karar(Za, Pa_)
    if kr["cetvel"] != {"a": "GÜVENİLMEZ", "b": "GÜVENİLİR"} or not kr["sinyal"][("a", "COMP4")].startswith("HÜKÜM YOK") or kr["sinyal"][("b", "COMP4")] != "TUTAR" \
            or kr["karar"] != "K59-B PORTFÖY-ADAY (COMP4 tasarım (b) iki evrende tutar)" or ("a", "U1", "COMP4") in kr["etiket"]:
        hata.append(f"B6) (a) plasebosu %5,5 iken (a)'da hüküm verildi / (b) etkilendi: {kr['cetvel']} {kr['karar']}")
    Pb_ = Pa_.copy(); Pb_.loc[(Pb_.tasarim == "b") & (Pb_.plasebo < 11), "tutar_v2"] = True; kr = K.k59b_karar(Za, Pb_)
    if not kr["karar"].startswith("HÜKÜM YOK") or kr["etiket"]:
        hata.append(f"B6) iki tasarımda da plasebo > %5 iken karar verildi: {kr['karar']}")
    Pc_ = Pl.copy(); Pc_.loc[(Pc_.tasarim == "a") & (Pc_.plasebo < 10), "brut_tutar_v2"] = True; kr = K.k59b_karar(Za, Pc_)
    if kr["cetvel"]["a"] != "GÜVENİLİR" or not np.isclose(kr["yp_brut"]["a"], 0.05) or kr["yp_net"]["a"] != 0:
        hata.append("B6) plasebo yanlış pozitif tam %5 iken cetvel güvenilmez sayıldı")
    if not K.k59b_karar(Za, None)["karar"].startswith("HÜKÜM YOK") or K.k59b_karar(Za, Pl[Pl.tasarim == "b"])["cetvel"] != {"a": "PLASEBO ÖLÇÜLMEDİ", "b": "GÜVENİLİR"} \
            or K.k59b_karar(Za, Pl[(Pl.tasarim == "a") | (Pl.plasebo < 150)])["sinyal"][("b", "COMP4")] != "HÜKÜM YOK (plasebo ölçülmedi)":
        hata.append("B6) plasebo yok / eksik iken hüküm verildi")
    if K.k59b_karar(pd.DataFrame(), Pl)["karar"] != "TUTMAZ":
        hata.append("B6) sonuç satırı yokken karar TUTMAZ değil")
    # B7) plasebo tohumları ve kâhin sinyal
    pb1 = K.k59b_plasebo_b(P2, Rh2, Et, Bt); pb2 = K.k59b_plasebo_b(P2, Rh2, Et, Bt)
    Bt2 = copy.deepcopy(Bt); Bt2["plasebo"]["tohum"]["b"] += 1
    if pb1.to_json() != pb2.to_json() or len(pb1) != 3 or pb1.brut_nw_t.nunique() < 3 or not np.isclose(K.k59b_plasebo_b(P2, Rh2, Et, Bt2).brut_nw_t.iloc[0], pb1.brut_nw_t.iloc[1]) \
            or not (pb1.brut_yillik_fazla >= pb1.yillik_fazla - 1e-12).all() or not {"tutar_v2", "brut_tutar_v2", "t_alfa", "brut_t_alfa"} <= set(pb1.columns):
        hata.append("B7) (b) plasebosu tohumla ('tohum_b + i') birebir tekrar etmiyor / sütun eksik / maliyet net fazlayı düşürmüyor")
    rs = np.random.default_rng(59200); Sr = rs.random(P2["U"].shape); Sr[~P2["U"]] = nan
    Pr = K.k59b_ortusen_portfoy(Rh2, P2["R"], K58.k58_ust_dilim(Sr, P2["U"], 0.10), P2["U"], P2["olusum"], 0.001, 3)
    if not np.isclose(pb1.nw_t.iloc[0], K.k59_cetvel_v2(Pr["net"], Pr["kiyas"], Et["cetvel"])["nw_t"]):
        hata.append("B7) (b) plasebosu elle kurulan rastgele sinyalle (default_rng(59200)) aynı değil")
    kah_b, _ = K.k59b_ortusen_olc(P2, Rh2, np.where(P2["U"], P2["R"], nan), None, Et, B0)
    kah_a, _ = K.k59_sinyal_olc(Pa, np.where(Pa["U"], Pa["R"], nan), None, Et)
    if not kah_b["tutar_v2"] or not kah_a["tutar_v2"] or kah_a["ort_hisse"] < 3:
        hata.append(f"B7) kâhin sinyal (gelecek ay getirisi) (a) / (b) tasarımında cetvel v2'den geçmedi: {kah_a.get('nw_t')} {kah_b.get('nw_t')}")
    # B8) uçtan uca sentetik koşu + rapor
    with tempfile.TemporaryDirectory() as td:
        K.k59_onkayit(td, veri_sha={}); K.k59b_onkayit(td, veri_sha={}); k59_once = open(K._k59_yol("onkayit", td), encoding="utf-8").read()
        try:
            Fs = french_sentetik(td)
            FFu = Fs["FF"]
            Ro = K.k59b_kos(td, git_sart=False, demetler={"U1": D1, "U2": D2}, FF=FFu, E=Et, B=Bt, french=Fs["yol"])
            Z = pd.read_csv(K._k59b_yol("sonuc", td)); Am = pd.read_csv(K._k59b_yol("aylik", td)); Kp = pd.read_csv(K._k59b_yol("kapsam", td))
            Plc = pd.read_csv(K._k59b_yol("plasebo", td)); Zc = pd.read_csv(K._k59b_yol("french", td)); Ac = pd.read_csv(K._k59b_yol("french_aylik", td))
            rt = open(Ro["rapor"], encoding="utf-8").read(); meta = json.load(open(K._k59b_yol("meta", td), encoding="utf-8"))
            bek = {(t, e, s) for t in ("a", "b") for e in ("U1", "U2") for s in B0["sinyal"]}
            if set(zip(Z.tasarim, Z.evren, Z.sinyal)) != bek or set(Z[Z.sinyal == "COMP4"].rol) != {"BİRİNCİL"} or set(Z[Z.sinyal != "COMP4"].rol) != {"BİLGİ"}:
                hata.append(f"B8) sonuç satırları eksik / fazla ya da roller yanlış: {set(zip(Z.tasarim, Z.evren, Z.sinyal)) ^ bek}")
            krc = K.k59b_karar(Z, Plc, Bt)
            if krc["karar"] != Ro["karar"]["karar"] or meta["karar"]["karar"] != Ro["karar"]["karar"] or not meta["sentetik"] or len(Plc) != 6 or set(Plc.tasarim) != {"a", "b"} \
                    or list(Z.etiket) != [krc["etiket"].get((t, e, s), "HÜKÜM YOK") for t, e, s in zip(Z.tasarim, Z.evren, Z.sinyal)] \
                    or meta["onkayit"]["sha"] != K.k59b_esik_sha() or meta["onkayit"]["k59_sha"] != K59_MUHUR_SABIT:
                hata.append("B8) karar çıktılardan yeniden üretilemiyor / plasebo çıktısı / meta'daki iki mühür yanlış")
            if "HÜKÜM YOK" not in open(K.k59b_rapor(td), encoding="utf-8").read():
                hata.append("B8) plasebo eksikken (3 < 200) rapor hüküm verdi")
            for t in ("a", "b"):
                g = Am[(Am.tasarim == t) & (Am.evren == "U2") & (Am.sinyal == "COMP4")]; r = Z[(Z.tasarim == t) & (Z.evren == "U2") & (Z.sinyal == "COMP4")].iloc[0]
                c = K.k59_cetvel_v2(g.net.to_numpy(), g.kiyas.to_numpy(), Et["cetvel"])
                if not (np.isclose(r.yillik_fazla, 12 * (g.net - g.kiyas).mean()) and np.isclose(r.nw_t, c["nw_t"]) and np.isclose(r.t_alfa, c["t_alfa"]) and r.ay == len(g)
                        and bool(r.tutar_v2) == c["tutar_v2"] and np.isclose(r.ort_hisse, g.n_hisse.mean()) and np.isfinite(r.ff_alfa_yillik)):
                    hata.append(f"B8) ({t}) sonuç satırı aylık getiri dosyasından yeniden üretilemiyor / FF alfası yok")
            ga, gb_ = (Am[(Am.tasarim == t) & (Am.evren == "U2") & (Am.sinyal == "COMP4")] for t in ("a", "b"))
            if len(ga) != len(A_a) or len(gb_) != len(A_b) or not np.allclose(ga.net, A_a.net) or not np.allclose(ga.kiyas, A_a.kiyas) or not np.allclose(gb_.net, A_b.net) \
                    or not np.allclose(gb_.kiyas, A_b.kiyas) or list(ga.n_sinyal) != list(A_a.n_sinyal):
                hata.append("B8) koşudaki (a) / (b) COMP4 serisi, ayrı kurulan alt evren içi sıralı (a) ve tam evren (b) serisiyle aynı değil (boru hattı yanlış bağlanmış)")
            if not (ga.n_evren < 0.6 * gb_.n_evren.mean()).all() or len(gb_) != len(Am[(Am.tasarim == "a") & (Am.evren == "U2") & (Am.sinyal == "S5")]) - 2:
                hata.append("B8) (a) alt evren tam evrenin yarısı dolayında değil / (b) ay sayısı aylık tutmadan 2 eksik değil")
            g = Ac[(Ac.ay >= "2000-01") & (Ac.ay <= "2009-12")]; r = Zc[(Zc.varyant == "VW_MKT") & (Zc.donem == "2000-09")].iloc[0]
            if len(Zc) != 15 or len(Ac) != 759 or not np.isclose(r.yillik_fazla, 12 * (g.harman_vw - 0.001 - g.MKT).mean()) or meta["c"]["ay"] != 759 \
                    or set(meta["c"]["okuma"]) != {"VW_MKT", "EW_EW10"} or meta["c"]["son_ay"] != "2026-09":
                hata.append("B8) (c) French çıktısı aylık dosyadan yeniden üretilemiyor / meta eksik")
            if not {"n_evren", "n_boyutlu", "n_alt", "alt_olusum", "a_n_COMP4", "b_n_COMP4", "a_n_S1", "b_n_DOSYA_Y", "S3_olcu"} <= set(Kp.columns) or set(Kp.evren) != {"U1", "U2"} \
                    or not (Kp.n_alt <= Kp.n_boyutlu / 2 + 0.5).all() or not (Kp.a_n_COMP4 <= Kp.n_alt).all():
                hata.append("B8) K59-B kapsam tablosu eksik / tutarsız")
            for parca in ("## Düz dille", "## Karar", "## Tasarım (a)", "## Tasarım (b)", "### (a) U1", "### (b) U2", "## Tasarım (c)", "VW_MKT (ANA)", "EW_MKT (BİLGİ)",
                          "Önceden yazılı okuma", "## Plasebo", "## Kapsam", "## Sınırlar", "IZ_KARNE önerisi", "K60", "BİRİNCİL", "K59 mührü 6fe8bb385667 değişmedi", "kör değildir"):
                if parca not in rt:
                    hata.append(f"B8) K59-B raporunda '{parca}' yok")
            if open(K._k59_yol("onkayit", td), encoding="utf-8").read() != k59_once or os.path.exists(K._k59_yol("sonuc", td)) or os.path.exists(K._k59_yol("rapor", td)):
                hata.append("B8) b_kos K59'un ön kaydına / çıktılarına dokundu")
            Ok = K.k59b_evren_olc(D2, None, Et, Bt, yalniz_kapsam=True)
            if Ok["sonuc"] or Ok["aylik"] or Ok["plasebo"] or not len(Ok["kapsam"]) or not Ok["ozet"]["olusum_ardisik"]:
                hata.append("B8) sayım modu getiri / plasebo hesapladı ya da kapsam üretmedi")
            Ko = K.k59b_kapsam_ozet(Ok["kapsam"], {"evren": {"U2": {"min_sinyal": 20}}}, Bt)
            ra, rb = (Z[(Z.tasarim == t) & (Z.evren == "U2") & (Z.sinyal == "COMP4")].iloc[0] for t in ("a", "b"))
            if list(Ko[(Ko.sinyal == "COMP4")].ay) != [int(ra.ay), int(rb.ay)] or len(Ko) != 8:
                hata.append(f"B8) sayımdan beklenen ölçüm ayı koşudaki ay sayısıyla aynı değil: {list(Ko[Ko.sinyal == 'COMP4'].ay)} != {[int(ra.ay), int(rb.ay)]}")
            R2 = K.k59b_kos(td, git_sart=False, demetler={"U1": D1, "U2": D2}, E=Et, B=Bt)
            if R2["french"] is not None or "(c) French harmanı ölçülmedi" not in " ".join(R2["meta"]["not"]):
                hata.append("B8) French verisi yokken (c) ölçüldü / not düşülmedi")
            for f in os.listdir(td):
                if f.endswith((".md", ".csv", ".json")) and K._K59_EPOSTA.search(open(os.path.join(td, f), encoding="utf-8").read()):
                    hata.append(f"B8) sentetik çıktıda e-posta var: {f}")
        except Exception as ex:
            hata.append(f"B8) uçtan uca sentetik K59-B koşusu çöktü: {type(ex).__name__} {ex}")
    return hata


if __name__ == "__main__":
    Hh = testler()
    if Hh:
        print("K59 TEST: HATA", len(Hh)); print("\n".join(Hh)); sys.exit(1)
    print("K59 TEST: 14/14 bölüm GEÇTİ")
    Hb_ = testler_b()
    if Hb_:
        print("K59-B TEST: HATA", len(Hb_)); print("\n".join(Hb_)); sys.exit(1)
    print("K59-B TEST: 8/8 bölüm GEÇTİ")
