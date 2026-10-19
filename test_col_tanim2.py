# -*- coding: utf-8 -*-
"""test_col_tanim2 — python -I test_col_tanim2.py [--mutasyon]"""
import os
import sys
import tempfile
import traceback
import types

import numpy as np
import pandas as pd

KLASOR = os.path.dirname(os.path.abspath(__file__))
KAYNAK = open(os.path.join(KLASOR, "col_tanim2.py"), encoding="utf-8").read()


def yukle(kod=KAYNAK):
    m = types.ModuleType("ct_test"); m.__file__ = "col_tanim2.py"; sys.modules["ct_test"] = m
    exec(compile(kod, "col_tanim2.py", "exec"), m.__dict__)
    return m.__dict__


def barlar(c, gurultu=0.004, seed=1, start="2024-01-01"):
    rng = np.random.default_rng(seed); c = np.asarray(c, float); n = len(c)
    o = c * (1 + rng.normal(0, gurultu, n)); h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, gurultu * 1.5, n))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, gurultu * 1.5, n)))
    return pd.DataFrame({"Open": o, "High": h, "Low": l, "Close": c, "Volume": 1e6}, index=pd.bdate_range(start, periods=n))


def sag_kol(n=50, yukselis=0.12, seed=1):
    """Cemal'in çölü: dipten başlayıp yavaş sürünen sağ kol (+%12 / 50 bar ≈ %0,24/gün), küçük mumlar."""
    return 10 * (1 + yukselis * np.linspace(0, 1, n) ** 1.3) + np.random.default_rng(seed).normal(0, 0.02, n)


def ders_kitabi(seed=1):
    """sol bacak 20→10 yavaşlayarak (40 bar) + çöl: dipten sürünen sağ kol (50 bar) + fırlama."""
    sol = 10 + 10 * np.linspace(1, 0, 40) ** 2; kol = sag_kol(50, 0.12, seed); kol = kol - kol[0] + 10.0; kol[0] = 9.99
    return barlar(np.concatenate([sol, kol, np.linspace(kol[-1], 15, 20)]), seed=seed), 40, 50


def T1_cemal_colu_gecer(ns):
    df, ns_, nc = ders_kitabi(); seg = df.iloc[ns_: ns_ + nc]; onc = df.iloc[:ns_]
    o = ns["ct_olc"](seg, onc); ok, kalan = ns["ct_karar"](o)
    assert ok, (kalan, o)
    assert o["dip_konum"] <= 0.15 and o["sag_kol_pct"] > 8 and 0.1 < o["egim_pct_gun"] < 0.5 and o["sol_bacak_pct"] > 50, o


def T2_dip_basta_K2(ns):
    kol = sag_kol(50, 0.12); dus = np.concatenate([np.linspace(11.5, 10, 30), kol[:20]])          # dip %60'ta (EGSER gibi: hâlâ iniyor)
    o = ns["ct_olc"](barlar(dus, gurultu=0.002, seed=2)); ok, kalan = ns["ct_karar"](o)
    assert "K2" in kalan and o["dip_konum"] > 0.5, (kalan, o["dip_konum"])
    duz = 10 + np.random.default_rng(3).normal(0, 0.03, 30)                                        # düz: sağ kol yok (AGHOL gibi)
    o2 = ns["ct_olc"](barlar(duz, gurultu=0.002, seed=3)); assert "K2" in ns["ct_karar"](o2)[1] and o2["sag_kol_pct"] < 5
    tam_u = np.concatenate([np.linspace(10.8, 10, 20), kol[:30]])                                   # tam çanak: dip %40'ta → çöl dipten başlamalı
    o3 = ns["ct_olc"](barlar(tam_u, gurultu=0.002, seed=4)); assert "K2" in ns["ct_karar"](o3)[1]


def T3_surunme_K3(ns):
    firlama = 10 * (1 + 0.5 * np.linspace(0, 1, 30))                                                # +%50 / 30 bar = %1,7/gün: çölün sonu, çöl değil
    o = ns["ct_olc"](barlar(firlama, gurultu=0.002, seed=5)); ok, kalan = ns["ct_karar"](o)
    assert "K3" in kalan and o["egim_pct_gun"] > 1.0, (kalan, o["egim_pct_gun"])
    kol = sag_kol(50, 0.12, seed=6); o2 = ns["ct_olc"](barlar(kol, gurultu=0.002, seed=6)); assert "K3" not in ns["ct_karar"](o2)[1]
    asagi = np.concatenate([[9.9], np.linspace(10.6, 10.0, 39)])                                     # dip başta ama sonra aşağı sürünme: eğim negatif
    o3 = ns["ct_olc"](barlar(asagi, gurultu=0.002, seed=7)); assert "K3" in ns["ct_karar"](o3)[1] and o3["egim_pct_gun"] < 0


def T4_mum_ve_bant_K1_K4(ns):
    rng = np.random.default_rng(6); c = 10 * np.cumprod(1 + rng.normal(0, 0.03, 40))
    o = ns["ct_olc"](barlar(c, gurultu=0.02, seed=6)); assert "K1" in ns["ct_karar"](o)[1]
    c4 = np.full(40, 10.0); o4 = c4 * (1 + 0.03 * np.where(np.arange(40) % 2 == 0, 1, -1))
    df4 = pd.DataFrame({"Open": o4, "High": np.maximum(o4, c4), "Low": np.minimum(o4, c4), "Close": c4, "Volume": 1e6}, index=pd.bdate_range("2024-01-01", periods=40))
    o5 = ns["ct_olc"](df4); assert "K1" in ns["ct_karar"](o5)[1] and o5["aralik_pct"] < 4.5
    buyuk = sag_kol(60, 0.9); o6 = ns["ct_olc"](barlar(buyuk, gurultu=0.002, seed=7)); assert "K4" in ns["ct_karar"](o6)[1] and o6["bant_pct"] > 65
    o7 = ns["ct_olc"](barlar(np.full(6, 10.0), seed=8)); assert "K4" in ns["ct_karar"](o7)[1]


def T5_bul_dipten_baslar(ns):
    df, ns_, nc = ders_kitabi(); T = df.index[ns_ + nc - 1]
    b = ns["ct_bul"](df, T); assert b is not None and b["gecti"], b
    i = df.index.get_loc(pd.Timestamp(b["bas"])); assert abs(i - ns_) <= 6, (i, ns_)                 # çöl sol bacağın dibinden başlar
    assert ns["ct_bul"](df, df.index[ns_ + 5]) is None                                                # dipte henüz sağ kol yok
    assert ns["ct_bul"](df, T, ns["ColKural"](sol_bacak_min=1.50)) is None and ns["ct_bul"](df, T, ns["ColKural"](sol_bacak_min=0.50)) is not None


def T6_ogret(ns):
    V = {}
    df, ns_, nc = ders_kitabi(); V["COL1"] = df; V["COL2"] = ders_kitabi(seed=2)[0]
    V["DUZ"] = barlar(10 + np.random.default_rng(9).normal(0, 0.03, 60), gurultu=0.002, seed=9)
    bas = str(df.index[ns_].date()); son = str(df.index[ns_ + nc - 1].date())
    evet = [("COL1", bas, son, "örnek"), ("COL2", bas, son, ""), ("YOK", bas, son, "")]
    hayir = [("DUZ", str(V["DUZ"].index[5].date()), str(V["DUZ"].index[55].date()), "düz kutu")]
    with tempfile.TemporaryDirectory() as K:
        T = ns["ct_ogret"](K, {"kayit": {}, "veri": V}, evet, hayir)
        assert os.path.exists(os.path.join(K, "col_tanim2_ogret.csv")) and (T[T.sembol == "YOK"].durum == "VERİDE YOK").all()
        e = T[(T.etiket == "EVET") & (T.durum == "ok")]; assert e.kural_gecti.all() and (e.bas_fark.abs() <= 6).all(), e[["sembol", "kalan", "bas_fark"]]
        h = T[T.etiket == "HAYIR"]; assert not h.kural_gecti.any() and "K3" in h.kalan.iloc[0], h[["kalan"]]
        r = open(os.path.join(K, "col_tanim2_ogret.txt"), encoding="utf-8").read(); assert "EVET: 2/2" in r and "HAYIR: 0/1" in r and "K2 dip başta" in r


def T7_en_dip_K6_ve_bilgi(ns):
    df, ns_, nc = ders_kitabi(); seg = df.iloc[ns_: ns_ + nc]; onc = df.iloc[:ns_]
    o = ns["ct_olc"](seg, onc); assert "K6" not in ns["ct_karar"](o)[1] and abs(o["dip_gercek_pct"]) < 2.5, o["dip_gercek_pct"]
    assert np.isfinite(o["bb_rank_son"]) and 0 <= o["bb_rank_son"] <= 1 and np.isfinite(o["hafta_egim_pct"]) and o["hafta_egim_pct"] > 0 and o["hafta_govde_pct"] < 5, o
    # tepe sıkışması: önce 8'den 20'ye yükseliş, sonra 20 civarında küçük mumlarla sürünme → dip burada değil, dağıtım
    yuk = np.concatenate([np.linspace(8, 20, 80), np.full(40, 20.0)]); tepe = sag_kol(40, 0.12, seed=11); tepe = tepe - tepe[0] + 20.0   # yükseliş + 40 bar düzlük + tepe sürünmesi (+%12, çöl gibi ama tepede)
    df2 = barlar(np.concatenate([yuk, tepe]), seed=11); seg2 = df2.iloc[120:]; onc2 = df2.iloc[:120]
    o2 = ns["ct_olc"](seg2, onc2); ok2, kalan2 = ns["ct_karar"](o2)
    assert "K6" in kalan2 and o2["dip_gercek_pct"] > 50, (kalan2, o2["dip_gercek_pct"])
    assert ns["ct_bul"](df2, df2.index[-1]) is None                                                   # bulucu da tepeyi çöl saymaz
    o3 = ns["ct_olc"](seg2); assert "K6" not in ns["ct_karar"](o3)[1]                                 # önceki veri yoksa K6 bakılamaz, kalmaz


TESTLER = [T1_cemal_colu_gecer, T2_dip_basta_K2, T3_surunme_K3, T4_mum_ve_bant_K1_K4, T5_bul_dipten_baslar, T6_ogret, T7_en_dip_K6_ve_bilgi]
MUTASYONLAR = [
    ("K1 gövde eşiği gevşer", 'o["govde_pct"] <= K.govde_pct * 100 and', "True and"),
    ("K2 dip konumu bakılmaz", 'o["dip_konum"] <= K.dip_max and', "True and"),
    ("K2 sağ kol bakılmaz (düz kutu geçer)", 'and o["sag_kol_pct"] >= K.kol_min * 100):', "):"),
    ("K3 üst sınır kalkar (fırlama çöl olur)", 'K.egim_min <= o["egim_pct_gun"] <= K.egim_max', 'K.egim_min <= o["egim_pct_gun"]'),
    ("K3 alt sınır kalkar (düşen de çöl olur)", 'K.egim_min <= o["egim_pct_gun"] <= K.egim_max', 'o["egim_pct_gun"] <= K.egim_max'),
    ("K4 bant sınırı kalkar", 'o["bant_pct"] <= K.bant_max * 100', "True"),
    ("K5 sol bacak kapısı kalkar", "if K.sol_bacak_min > 0 and not", "if False and not"),
    ("eğim fiyata bölünmez", "np.polyfit(np.arange(n), C, 1)[0] / C.mean() * 100", "np.polyfit(np.arange(n), C, 1)[0] * 100"),
    ("bul geleceğe bakar", 'x = df[df.index <= pd.Timestamp(T)] if T is not None else df', "x = df"),
    ("finder dibe kırpmaz", "            if i_min > 0:", "            if False:"),
    ("K6 en dip kapısı kalkar", 'if np.isfinite(dg) and dg > K.dip_gercek_tol * 100:', "if False:"),
    ("finder K6 için geriye yeterince bakmaz", "geri = max(K.sol_bacak_bar, K.dip_bakis, 120)", "geri = 30"),
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
    import logging; logging.disable(logging.WARNING)
    if "--mutasyon" in sys.argv:
        kacan = []
        for ad, eski, yeni in MUTASYONLAR:
            assert eski in KAYNAK, f"mutasyon hedefi yok: {ad}"
            try:
                ns = yukle(KAYNAK.replace(eski, yeni, 1))
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
