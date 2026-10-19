# -*- coding: utf-8 -*-
"""test_olcum_denetimi — denetim aletinin kendi testi. python -I test_olcum_denetimi.py [--mutasyon]"""
import os
import sys
import types
import traceback

import numpy as np
import pandas as pd

KLASOR = os.path.dirname(os.path.abspath(__file__))
KAYNAK_TO = open(os.path.join(KLASOR, "tahtaci_oyunu.py"), encoding="utf-8").read()
KAYNAK_OD = open(os.path.join(KLASOR, "olcum_denetimi.py"), encoding="utf-8").read()
sys.path.insert(0, KLASOR)
from test_tahtaci_oyunu import dunya  # noqa: E402


def yukle(kod_od: str = KAYNAK_OD):
    m = types.ModuleType("denetim_test"); m.__file__ = "olcum_denetimi.py"; sys.modules["denetim_test"] = m
    exec(compile(KAYNAK_TO, "tahtaci_oyunu.py", "exec"), m.__dict__)
    exec(compile(kod_od, "olcum_denetimi.py", "exec"), m.__dict__)
    m.__dict__["_TEST_KOD"] = kod_od
    return m.__dict__


def evren_ve_olaylar(ns, n=12):
    """n yapay hisse (farklı tohum) → evren + olay tablosu."""
    E = {}
    for i in range(n):
        df, k, d = dunya(seed=100 + i)
        E[f"S{i}"] = ns["to_ohlcv"](df)
    O = ns["to_olaylar"](E)
    return E, O


def T1_plasebo_yapay(ns):
    E, O = evren_ve_olaylar(ns)
    T = ns["TahtaciTanim"]()
    P = ns["od_plasebo"](E, O, T, n_rastgele=10)
    assert P["n"] == len(O) and not np.isnan(P["fark"])
    # yapay dünyada klimaks sonrası +%5/gün tepki var: klimaks plasebodan iyi olmalı
    assert P["band"][0] > 0 and "BİLGİ" in P["hukum"], P


def T2_plasebo_gercek_degil_rastgele(ns):
    """Plasebo günleri klimaks günleri olmamalı ve olaya 2 günden yakın olmamalı (kaynak koda bakılır)."""
    assert "abs(j - k) > 2" in ns["_TEST_KOD"] and "not kl[j]" in ns["_TEST_KOD"]


def T3_bolunme_tek_gun(ns):
    E, O = evren_ve_olaylar(ns, n=4)
    T = ns["TahtaciTanim"]()
    # bir hissede çöküşü tek güne sıkıştır: klimaks öncesi kapanış 20'ye çek
    s = "S0"; M = E[s]; k = M.index.get_indexer([pd.Timestamp(O.loc[O.sembol == s, "tarih"].iloc[0])])[0]
    M.iloc[k - 1, M.columns.get_loc("C")] = 20.0
    B = ns["od_bolunme"](E, O, T, yf_ornek=0)
    assert B["tek_gun_cokus"] == 1, B


def T4_bolunme_yf_karsilastirma(ns):
    E, O = evren_ve_olaylar(ns, n=4)
    T = ns["TahtaciTanim"]()

    def sahte_indir(s, bas):
        C = E[s]["C"]; a = C.copy(); h = C * 2.0   # önbellek düzeltilmişle aynı, hamın yarısı
        return a, h
    B = ns["od_bolunme"](E, O, T, yf_ornek=3, indir=sahte_indir)
    assert B["duzeltilmis"] == 3 and B["ham"] == 0 and "temettü-düzeltili" in B["hukum"], B

    def sahte_ham(s, bas):
        C = E[s]["C"]; return C * 2.0, C.copy()
    B2 = ns["od_bolunme"](E, O, T, yf_ornek=3, indir=sahte_ham)
    assert B2["ham"] == 3 and "düzeltisiz" in B2["hukum"], B2


def T5_hayatta_kalma(ns):
    E, O = evren_ve_olaylar(ns, n=5)
    E["S0"] = E["S0"].iloc[:-60]                       # 60 bar erken bitiyor
    H = ns["od_hayatta_kalma"](E, O, bayat_gun=30)
    assert H["son_bari_eski"] == 1 and H["olay_eski_hissede"] == 1, H


def T6_giris(ns):
    E, O = evren_ve_olaylar(ns, n=3)
    T = ns["TahtaciTanim"]()
    G = ns["od_giris"](E, O, T, tavan=0.09)
    assert G["n"] == len(O)
    # yapay dünyada ertesi açılış +%1 boşluk; tavan payı 0
    assert abs(G["bosluk_medyan_pct"] - 1.0) < 0.2 and G["tavan_acilis_pay"] == 0, G
    # elle: ilk olay r10 açılış = olaylar tablosundaki klimaks_r10
    s = O.sembol.iloc[0]; M = E[s]; k = M.index.get_indexer([pd.Timestamp(O.tarih.iloc[0])])[0]
    bek = (M["C"].iloc[k + 11] / M["O"].iloc[k + 1] - 1 - 2 * T.maliyet) * 100
    assert abs(O.klimaks_r10.iloc[0] - bek) < 1e-9
    bek_k = (M["C"].iloc[k + 11] / M["C"].iloc[k + 1] - 1 - 2 * T.maliyet) * 100
    assert abs(ns["_od_r"](M, k, 10, T.maliyet, "kapanis") - bek_k) < 1e-9


def T7_rejim(ns):
    E, O = evren_ve_olaylar(ns, n=6)
    T = ns["TahtaciTanim"]()
    ix = pd.bdate_range("2023-06-01", "2024-12-31")
    xu = pd.Series(np.linspace(100, 50, len(ix)), index=ix)      # sürekli düşüş → hepsi düşüş rejimi
    R = ns["od_rejim"](O, xu, T)
    assert R["n_dusus"] == len(O) and R["n_yukselis"] == 0, R
    xu2 = pd.Series(np.linspace(50, 100, len(ix)), index=ix)
    R2 = ns["od_rejim"](O, xu2, T)
    assert R2["n_yukselis"] == len(O), R2
    assert "XU100" in ns["od_rejim"](O, None, T)["hukum"]
    # 60 günlük pencere: son 30 gün yükselen ama 60 gün önce daha yüksek olan endeks → düşüş rejimi sayılmalı
    v = np.r_[np.linspace(100, 30, len(ix) - 30), np.linspace(30, 35, 30)]
    xu3 = pd.Series(v, index=ix); O3 = O.copy(); O3["tarih"] = ix[-5]
    R3 = ns["od_rejim"](O3, xu3, T)
    assert R3["n_dusus"] == len(O3), R3


def T8_rapor(ns):
    E, O = evren_ve_olaylar(ns, n=4)
    T = ns["TahtaciTanim"]()
    ix = pd.bdate_range("2023-06-01", "2024-12-31")
    D = {"plasebo": ns["od_plasebo"](E, O, T, n_rastgele=5), "bolunme": ns["od_bolunme"](E, O, T, yf_ornek=0),
         "hayatta": ns["od_hayatta_kalma"](E, O), "giris": ns["od_giris"](E, O, T),
         "rejim": ns["od_rejim"](O, pd.Series(np.linspace(50, 100, len(ix)), index=ix), T)}
    r = ns["od_rapor"](D)
    assert all(x in r for x in ("1 PLASEBO", "2 BÖLÜNME", "3 HAYATTA", "4 GİRİŞ", "5 REJİM")), r


TESTLER = [T1_plasebo_yapay, T2_plasebo_gercek_degil_rastgele, T3_bolunme_tek_gun, T4_bolunme_yf_karsilastirma, T5_hayatta_kalma, T6_giris, T7_rejim, T8_rapor]

MUTASYONLAR = [
    ("plasebo klimaks günlerini de seçer", "if not kl[j] and abs(j - k) > 2", "if abs(j - k) > 2"),
    ("plasebo hükmü ters", 'if hi < 0 else', 'if lo > 0 else'),
    ("tek günlük çöküş eşiği kalkar", ">= T.cokus_min:\n                tek_gun += 1", ">= 9:\n                tek_gun += 1"),
    ("düzeltme kıyası ters", "if fa < fh * 0.5:\n                duz += 1", "if fh < fa * 0.5:\n                duz += 1"),
    ("hayatta kalma eşiği kalkar", "(son - df.index[-1]).days > bayat_gun", "False"),
    ("giriş kapanıştan hesaplanmaz", 'if giris == "acilis" else float(M["C"].iloc[i + 1])', 'if giris == "acilis" else float(M["O"].iloc[i + 1])'),
    ("rejim 60 gün yerine 1 gün", "x / x.shift(60) - 1", "x / x.shift(1) - 1"),
]


def kos(ns, sessiz=False):
    hata = []
    for t in TESTLER:
        try:
            t(ns)
        except Exception as e:
            hata.append((t.__name__, e))
            if not sessiz:
                print(f"  ✗ {t.__name__}: {e}"); traceback.print_exc()
        else:
            if not sessiz:
                print(f"  ✓ {t.__name__}")
    return hata


if __name__ == "__main__":
    if "--mutasyon" in sys.argv:
        kacan = []
        for ad, eski, yeni in MUTASYONLAR:
            assert eski in KAYNAK_OD, f"mutasyon hedefi yok: {ad}"
            try:
                ns = yukle(KAYNAK_OD.replace(eski, yeni, 1))
            except Exception:
                print(f"  ✓ yakalandı (yükleme): {ad}"); continue
            h = kos(ns, sessiz=True)
            print(f"  {'✓ yakalandı' if h else '✗ KAÇTI'}: {ad}" + (f" ← {h[0][0]}" if h else ""))
            if not h:
                kacan.append(ad)
        print(f"\n{len(MUTASYONLAR) - len(kacan)}/{len(MUTASYONLAR)} mutasyon yakalandı"); sys.exit(1 if kacan else 0)
    ns = yukle()
    h = kos(ns)
    print(f"\n{len(TESTLER) - len(h)}/{len(TESTLER)} test geçti"); sys.exit(1 if h else 0)
