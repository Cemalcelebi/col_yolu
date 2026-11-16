"""test_cokus_oynak.py — COKUS_OYNAK.py denetimi (16 Kasım 2026).

Sentetik: geçerli bar süzgeci, çöküş günü kuralı (ilk gün + 250 gün ara), dilimler, giriş = karar sonrası açılış, ham sıçrama düzeltmesi.
Gerçek çıktı (varsa): kontrol kapısı, mühür, K11 bağımsız yeniden üretim (>= 2 hücre: 2023 OYNAK ve 2018B OYNAK P100 / M50 ve TABAN),
satır düzeyinde ham veriden bağımsız yeniden hesap (rastgele 5 hisse), geleceğe bakma (karar < giriş), e-posta / anahtar taraması, çakışma kapısı.
Çalıştır: python test_cokus_oynak.py
"""
from __future__ import annotations

import json
import os
import re
import sys

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import COKUS_OYNAK as C  # noqa: E402

CIK = os.path.join(KOK, "arastirma_cikti", "cokus_oynak")
HATA = []


def ok(kosul: bool, ad: str) -> None:
    print(("GEÇTİ  " if kosul else "KALDI  ") + ad)
    if not kosul:
        HATA.append(ad)


def _sentetik(n: int = 900, tohum: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(tohum)
    ix = pd.bdate_range("2016-01-01", periods=n)
    c = 10 * np.exp(np.cumsum(rng.normal(0, 0.02, n)))
    o = c * (1 + rng.normal(0, 0.005, n))
    return pd.DataFrame({"Open": o, "High": np.maximum(o, c) * 1.01, "Low": np.minimum(o, c) * 0.99, "Close": c,
                         "Volume": rng.integers(1000, 5000, n).astype(float)}, index=ix)


def t_sentetik() -> None:
    d = _sentetik()
    d.iloc[10, d.columns.get_loc("High")] = d.iloc[10]["Low"]          # H = L
    d.iloc[11, d.columns.get_loc("Volume")] = 0                         # V = 0
    g = C.co_gecerli(d)
    ok(len(g) == len(d) - 2, "geçerli bar: H=L ve V=0 atılır")
    # çöküş kuralı
    ix = pd.bdate_range("2018-01-01", periods=800)
    med = pd.Series(0.0, index=ix); med.iloc[100:105] = -0.35; med.iloc[200] = -0.40; med.iloc[400] = -0.31
    M = pd.DataFrame({"medyan": med, "n": 100})
    gun = C.co_cokus_gunleri(M)
    ok(gun == [ix[100], ix[400]], f"çöküş: ilk gün + 250 gün ara ({[str(x.date()) for x in gun]})")
    # dilimler
    D = pd.DataFrame({"sembol": [f"S{i}" for i in range(100)], "sigma250": np.arange(100) / 100.0,
                      "dusus250": -np.arange(100) / 100.0, "likidite": np.arange(100) + 1.0})
    X = C.co_dilimle(D)
    ok(int(X.liq_alt.sum()) == 20, "likidite alt %20 hariç")
    ok(int(X.OYNAK.sum()) == 16 and int(X.TABAN.sum()) == 48, f"σ beşlik: OYNAK {int(X.OYNAK.sum())}, TABAN {int(X.TABAN.sum())}")
    ok(bool(X.loc[X.DUSMUS, "dusus250"].max() < X.loc[X.TABAN_D, "dusus250"].min()), "DUSMUS en negatif düşüş")
    # olay: giriş açılışı, geleceğe bakma
    d = _sentetik(900, 3)
    T = d.index
    r = C.co_hisse_olay("X", d, T, 400, pd.DatetimeIndex([]), None)
    ok(r is not None and r["giris"] == d.Open.iloc[400] and r["karar"] == T[399], "giriş = karar sonrası ilk günün AÇILIŞI")
    c_ = d.Close.to_numpy(); lr = np.diff(np.log(c_[399 - 250:400]))
    ok(abs(r["sigma250"] - np.std(lr, ddof=1)) < 1e-12, "σ250 yalnız karar günü ve öncesi 251 kapanış")
    w = d.Close.iloc[400:651]
    ok(r["p100"] == bool((w >= 2 * r["giris"]).any()) and abs(r["r250"] - (w.iloc[-1] / r["giris"] - 1)) < 1e-12, "P100 / r250 ufuk 250 gün")
    # ham sıçrama düzeltmesi
    d2 = _sentetik(300, 5)
    d2.iloc[150:, 0:4] = d2.iloc[150:, 0:4] / 5.0                       # düzeltilmemiş 1:5 bedelsiz
    x, k = C.co_ham_duzelt(d2)
    ok(k == 1 and abs(x.Close.iloc[149] - x.Close.iloc[150]) < 1e-9
       and abs(x.Close.iloc[100] / x.Close.iloc[149] - d2.Close.iloc[100] / d2.Close.iloc[149]) < 1e-9
       and abs((x.Close * x.Volume).iloc[100] - (d2.Close * d2.Volume).iloc[100]) < 1e-6,
       "ham sıçrama: sıçrama günü getirisi 0 sayılır, önceki fiyatlar oranla düzeltilir, işlem değeri korunur")


def t_cikti() -> None:
    onk = os.path.join(CIK, "ON_KAYIT.md")
    if not os.path.exists(os.path.join(CIK, "sonuc.json")):
        print("ATLANDI  çıktı yok (önce python COKUS_OYNAK.py kos)"); return
    import IZ_KARNE as IK
    ok(IK.ik_kontrol_kapisi(onk, dur=False)["gecti"], "kontrol kapısı açık (14 satır)")
    J0 = json.load(open(os.path.join(CIK, "on_kayit.json"), encoding="utf-8"))
    S = json.load(open(os.path.join(CIK, "sonuc.json"), encoding="utf-8"))
    ok(J0["muhur"] == C.co_muhur() == S["muhur"], "CO_ESIK mühürü ön kayıt = kod = sonuç")
    ok(J0["zaman"] < S["zaman"], "ön kayıt zamanı < koşu zamanı")
    D = pd.read_csv(os.path.join(CIK, "cokus_oynak_olay.csv.gz"), parse_dates=["karar", "giris_gunu", "giris_bar"])
    ok(bool((D.karar < D.giris_gunu).all()), "geleceğe bakma: her satırda karar < giriş günü")
    ok(bool((D.giris_bar.dropna() >= D.loc[D.giris_bar.notna(), "giris_gunu"]).all()), "giriş barı giriş gününden önce değil")
    # K11: bağımsız yeniden üretim (pandas ile ayrı yol)
    for tur, o in (("cokus", "2023"), ("bilgi", "2018B"), ("normal", "N2017")):
        x = D[(D.tur == tur) & (D.olay.astype(str) == o) & D.p100.notna() & (D.bolunme != True)]  # noqa: E712
        h = S["tablo"][f"{tur}|OYNAK"][o]
        for g, kol in (("A", "OYNAK"), ("B", "TABAN")):
            y = x[x[kol] == True]  # noqa: E712
            ok(len(y) == h[g]["n"] and abs(y.p100.astype(bool).mean() - h[g]["P100"]) < 1e-9 and abs(y.m50.astype(bool).mean() - h[g]["M50"]) < 1e-9
               and abs(y.r250.median() - h[g]["med_r250"]) < 1e-4,
               f"K11 {o} {kol}: n {len(y)}, P100 {y.p100.astype(bool).mean():.4f}, M50 {y.m50.astype(bool).mean():.4f}")
    # satır düzeyi: ham veriden bağımsız yeniden hesap (5 rastgele hisse, 2023 çöküşü)
    V = pd.read_pickle(os.path.join(C.CO_YOL["veri"], "V_BIST.pkl"))
    x = D[(D.tur == "cokus") & (D.olay.astype(str) == "2023") & D.p100.notna()].sample(5, random_state=7)
    tm = True
    for _, r in x.iterrows():
        d = V[r.sembol]
        d = d[(d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0)]
        e = d.loc[d.index >= r.giris_gunu, "Open"].iloc[0]
        tm &= abs(e - r.giris) < 1e-6 * max(1, e)
        once = d.loc[d.index <= r.karar, "Close"].iloc[-251:]
        tm &= abs(np.log(once).diff().dropna().std() - r.sigma250) < 1e-5
    ok(bool(tm), "satır düzeyi: giriş açılışı ve σ250 ham V_BIST'ten bağımsız aynı (5 hisse)")
    # sızıntı
    eposta = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    anahtar = re.compile(r"(api[_-]?key|token|secret|password)\s*[:=]\s*['\"][^'\"]{8,}", re.I)
    sz = []
    for f in ["COKUS_OYNAK.py", "test_cokus_oynak.py"] + [os.path.join("arastirma_cikti", "cokus_oynak", g) for g in ("ON_KAYIT.md", "RAPOR.md", "sonuc.json")]:
        m = open(os.path.join(KOK, f), encoding="utf-8").read()
        if eposta.search(m) or anahtar.search(m):
            sz.append(f)
    ok(not sz, f"e-posta / anahtar sızıntısı yok {sz}")
    # alım dili
    rap = open(os.path.join(CIK, "RAPOR.md"), encoding="utf-8").read()
    yasak = [w for w in (" al ", "öneri:", "kaçırma", "garanti", "kesin al") if w in rap.lower()]
    ok(not yasak, f"raporda alım dili yok {yasak}")


def t_cakisma() -> None:
    g = {"co_kos": "baska"}
    try:
        exec(compile(open(os.path.join(KOK, "COKUS_OYNAK.py"), encoding="utf-8").read().replace('if __name__ == "__main__"', "if False"),
                     "COKUS_OYNAK.py", "exec"), g)
        ok(False, "çakışma kapısı ad ezmeyi durdurur")
    except RuntimeError as ex:
        ok("EZDİ" in str(ex), "çakışma kapısı ad ezmeyi durdurur")


if __name__ == "__main__":
    t_sentetik()
    t_cakisma()
    t_cikti()
    print(f"\n{'HEPSİ GEÇTİ' if not HATA else 'KALAN: ' + str(HATA)}")
    sys.exit(1 if HATA else 0)
