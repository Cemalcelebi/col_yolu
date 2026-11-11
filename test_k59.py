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
        Vb[s] = d.assign(Open=d.Open * k, High=d.High * k * 1.2, Low=d.Low * k, Close=d.Close * k,
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
                      "## 6. COMP4 tutmazsa", "HAYATTA KALMA", "PORTFÖY-ADAY", "TUTAR AMA KÜÇÜK", "GÜÇLÜ", "TUTAR (yineleme)", "İZ ilan EDİLEMEZ",
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
    P2 = K.k59_panel(D2); S2, ek2 = K.k59_sinyaller(D2, P2)
    for b, tn in K.K59_ESIK["bilesik"].items():
        S2[b] = K.k59_bilesik(S2, P2["U"], tn["uye"], tn["min"])
    eksik = [a for a in K.K59_SIRA + ["COMP4", "COMP9"] if a not in S2 or np.isfinite(S2[a]).sum() < 500]
    if eksik:
        hata.append(f"4) sentetik demette sinyal üretilemedi: {eksik}")
    me = P2["ay_sonu"]; k0 = int(np.flatnonzero(P2["olusum"])[26]); t0 = me[k0]
    Hb = boz(H, t0); Db = demet(Hb, "U2"); Pb = K.k59_panel(Db); Sb, ekb = K.k59_sinyaller(Db, Pb)
    for b, tn in K.K59_ESIK["bilesik"].items():
        Sb[b] = K.k59_bilesik(Sb, Pb["U"], tn["uye"], tn["min"])
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
    for a, alan in (("S5", "bilgi_son"), ("S7", "bilgi_son"), ("S6", "pay_filed")):
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
        for a, v in bek.items():
            if not np.isclose(S2[a][k0, j], v, equal_nan=True, rtol=1e-9):
                hata.append(f"5) {a} {s}: {S2[a][k0, j]} != elle {v}")
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
    # 8) portföy muhasebesi
    rng = np.random.default_rng(4); R = rng.normal(0.01, 0.05, (3, 20)); U = np.ones((3, 20), bool); U[:, 19] = False
    S = np.tile(np.arange(20.0), (3, 1)); S[:, 10:] = np.nan; S[0, 3:] = np.nan            # ilk ay yalnız 3 hissede sinyal (< 5): ölçüm 2. aydan
    Pm = mini_panel(R, U); row, A = K.k59_sinyal_olc(Pm, S, None, {**K.K59_ESIK, "cetvel": {**K.K59_ESIK["cetvel"], "min_ay": 1}})
    kiyas = R[1:, :19].mean(axis=1)
    if len(A) != 2 or list(A.n_hisse) != [1, 1] or list(A.n_sinyal) != [10, 10] or list(A.n_evren) != [19, 19]:
        hata.append(f"8) ölçüm dönemi / üst %10 sayısı / evren sayısı yanlış: {A}")
    elif not (np.allclose(A.brut, R[1:, 9]) and np.allclose(A.kiyas, kiyas) and np.isclose(A.devir.iloc[0], 1.0) and np.isclose(A.devir.iloc[1], 0.0)
              and np.isclose(A.net.iloc[0], (1 - 0.001) * (1 + R[1, 9]) - 1) and np.isclose(A.net.iloc[1], R[2, 9]) and list(A.getiri_ayi) == ["2020-03", "2020-04"]):
        hata.append(f"8) portföy muhasebesi (en yüksek sinyal, maliyet, devir, kıyas = bütün uygun evren, getiri ayı) yanlış: {A}")
    Sx = np.tile(np.arange(20.0), (3, 1)); Sx[1] = Sx[1][::-1]; Sx[:, 19] = np.nan
    _, Ax = K.k59_sinyal_olc(Pm, Sx, None, K.K59_ESIK)
    if not np.allclose(Ax.devir, [1.0, 2.0, 2.0]) or not np.allclose(Ax.net, (1 - 0.001 * Ax.devir) * (1 + Ax.brut) - 1) or list(Ax.n_hisse) != [2, 2, 2]:
        hata.append(f"8) devir / maliyet (tek yön 10 bp x devir) yanlış: {Ax}")
    if K.k59_sinyal_olc(Pm, np.full((4, 20), np.nan)[:3], None, K.K59_ESIK)[0].get("olculdu") is not False:
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
            bek = {(e, s) for e in ("U1", "U2") for s in K.K59_SIRA + ["COMP4", "COMP9"]} | {("BIST", s) for s in ("S1", "S2", "S3", "S8", "S9", "COMP9")}
            if set(zip(Z.evren, Z.sinyal)) != bek:
                hata.append(f"13) sonuç satırları eksik / fazla: {set(zip(Z.evren, Z.sinyal)) ^ bek}")
            if not len(pd.read_csv(K._k59_yol("plasebo", td))) == 3 or not Ro["karar"]["bilesik"].startswith("HÜKÜM YOK") or not meta["sentetik"]:
                hata.append("13) plasebo çıktısı / eksik plaseboda hüküm yok kuralı / sentetik işareti yanlış")
            g = Am[(Am.evren == "U2") & (Am.sinyal == "COMP4")]; r = Z[(Z.evren == "U2") & (Z.sinyal == "COMP4")].iloc[0]
            c = K.k59_cetvel_v2(g.net.to_numpy(), g.kiyas.to_numpy(), Et["cetvel"])
            if not (np.isclose(r.yillik_fazla, 12 * (g.net - g.kiyas).mean()) and np.isclose(r.nw_t, c["nw_t"]) and np.isclose(r.t_alfa, c["t_alfa"]) and r.ay == len(g)
                    and bool(r.tutar_v2) == c["tutar_v2"] and np.isclose(r.ort_hisse, g.n_hisse.mean())):
                hata.append("13) sonuç satırı aylık getiri dosyasından yeniden üretilemiyor")
            if Z[(Z.evren == "BIST")].rol.ne("BİLGİ").any() or Z[(Z.evren == "U1") & (Z.sinyal == "COMP4")].rol.iloc[0] != "KARAR" or Z[Z.sinyal == "COMP9"].rol.ne("BİLGİ").any():
                hata.append("13) karar / bilgi rolleri yanlış")
            if Z[(Z.evren == "BIST")].ff_alfa_yillik.notna().any() if "ff_alfa_yillik" in Z else True:
                hata.append("13) BIST'te French alfası hesaplandı / ABD'de hiç hesaplanmadı")
            if not Z[(Z.evren == "U2") & (Z.sinyal == "S1")].ff_alfa_yillik.notna().all():
                hata.append("13) ABD'de FF5 + UMD alfası yok")
            if not {"n_evren", "n_S4", "n_COMP4", "S3_olcu"} <= set(Kp.columns) or set(Kp.evren) != {"U1", "U2", "BIST"}:
                hata.append("13) kapsam tablosu eksik")
            for parca in ("## Düz dille", "## Karar", "## U1", "## U2", "## BIST", "## Plasebo", "## Kapsam", "## Sınırlar", "sıradaki üç deneme", "IZ_KARNE önerisi", "HÜKÜM YOK"):
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


if __name__ == "__main__":
    Hh = testler()
    if Hh:
        print("K59 TEST: HATA", len(Hh)); print("\n".join(Hh)); sys.exit(1)
    print("K59 TEST: 14/14 bölüm GEÇTİ")
