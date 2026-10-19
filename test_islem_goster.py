# -*- coding: utf-8 -*-
"""test_islem_goster — python -I test_islem_goster.py [--mutasyon]   (DENETIM.py aynı klasörde olmalı: islemler() gerçek kodla alınır)"""
import os
import sys
import tempfile
import traceback
import types

import numpy as np
import pandas as pd

KLASOR = os.path.dirname(os.path.abspath(__file__))
KAYNAK = open(os.path.join(KLASOR, "islem_goster.py"), encoding="utf-8").read()
DEN = open(os.path.join(KLASOR, "DENETIM.py"), encoding="utf-8").read()
DEN = DEN[:DEN.index("def _agirlik")] if "def _agirlik" in DEN else DEN        # yalnız islemler ve yardımcıları (print/K yok)


def yukle(kod=KAYNAK):
    m = types.ModuleType("ig_test"); m.__file__ = "islem_goster.py"; sys.modules["ig_test"] = m
    exec(compile(kod, "islem_goster.py", "exec"), m.__dict__)
    return m.__dict__


def denetim_ns():
    m = types.ModuleType("den_test"); sys.modules["den_test"] = m; m.K = "/tmp"
    exec(compile(DEN, "DENETIM.py", "exec"), m.__dict__)
    return m.__dict__


def kayit(sembol="S1", seed=1, kirilim_bar=3, hedef_bar=15, dusus_bar=30, n_il=200, seg_n=30):
    """Önbellek kaydı (onbellek._kayit biçimi): segment 10±0.3, ileri: kirilim_bar'da tavan üstü kapanış, hedef_bar'da +%22, dusus_bar'dan sonra düşüş."""
    rng = np.random.default_rng(seed)
    ix = pd.bdate_range("2024-01-01", periods=seg_n + n_il)
    sc = 10 + rng.normal(0, 0.1, seg_n); so = sc + rng.normal(0, 0.05, seg_n); sh = np.maximum(so, sc) + 0.1; sl = np.minimum(so, sc) - 0.1
    ic = np.full(n_il, 10.1); ic[kirilim_bar:] = 10.6; ic[hedef_bar:] = 12.9; ic[dusus_bar:] = 11.0
    ic = ic + rng.normal(0, 0.02, n_il); io = ic - 0.05; ih = ic + 0.15; il_ = ic - 0.15
    s20 = pd.Series(np.concatenate([sc, ic])).rolling(20).mean().to_numpy()[-n_il:]
    return {"sembol": sembol, "tarih": ix[seg_n - 1], "GECER": True, "seg": {"bas_tarih": str(ix[0].date()), "son_tarih": str(ix[seg_n - 1].date()), "atr_ref": 0.3, "uzunluk": seg_n},
            "sT": ix[:seg_n].to_numpy(), "sO": so, "sH": sh, "sL": sl, "sC": sc, "sV": np.full(seg_n, 2e5),
            "iT": ix[seg_n:].to_numpy(), "iO": io, "iH": ih, "iL": il_, "iC": ic, "iV": np.full(n_il, 2e5), "s20": s20}


def veri_from(OB):
    V = {}
    for o in OB:
        ix = pd.DatetimeIndex(np.concatenate([o["sT"], o["iT"]]))
        onc = pd.bdate_range(end=ix[0], periods=51)[:-1]
        df = pd.DataFrame({"Open": np.concatenate([np.full(50, 9.5), o["sO"], o["iO"]]), "High": np.concatenate([np.full(50, 9.7), o["sH"], o["iH"]]),
                           "Low": np.concatenate([np.full(50, 9.3), o["sL"], o["iL"]]), "Close": np.concatenate([np.full(50, 9.5), o["sC"], o["iC"]]), "Volume": 2e5}, index=onc.append(ix))
        V[o["sembol"]] = df
    return V


def T1_barlar_denetimle_ayni(ns):
    dn = denetim_ns(); OB = [kayit("S1"), kayit("S2", seed=2, kirilim_bar=5, hedef_bar=40, dusus_bar=70), kayit("S3", seed=3, hedef_bar=500)]   # S3: hedef yok → ufuk
    q, _ = dn["islemler"](OB, "acilis"); assert len(q) == 3
    for i in range(3):
        B, b = ns["ig_barlar"](q.iloc[i], veri_from(OB))
        assert abs(b["getiri_net"] - float(q.iloc[i]["g"])) < 1e-9, (b["getiri_net"], q.iloc[i]["g"])
        assert b["giris_fiyat"] == float(q.iloc[i]["gp"]) and b["cikis_fiyat"] == float(q.iloc[i]["cp"])
        assert b["giris_gunu"] == q.iloc[i]["giris_t"].date() and b["cikis_gunu"] == q.iloc[i]["cikis_t"].date()
        assert (B["rol"] == "baglam").sum() == 40 and (B["rol"].isin(["segment", "sinyal"])).sum() == 30 and (B["rol"] == "sinyal").sum() == 1
        assert B["rol"].str.contains("kirilim").sum() == 1 and B["rol"].str.contains("giris").sum() == 1 and B["rol"].str.contains("cikis").sum() == 1
        kb = B.index[B["rol"].str.contains("kirilim")][0]; gi = B.index[B["rol"].str.contains("giris")][0]
        assert gi == kb + 1 and float(B.loc[kb, "C"]) > b["kirilim_esigi"] and float(B.loc[kb - 1, "C"]) <= b["kirilim_esigi"] if B.loc[kb - 1, "rol"] == "ileri" else True
    _, b1 = ns["ig_barlar"](q.iloc[0], None); assert b1["hedef_vuruldu"] and "SMA20" in b1["cikis_neden"] and b1["tutus_bar"] == int(q.iloc[0]["jt"] - q.iloc[0]["e"])
    _, b3 = ns["ig_barlar"](q.iloc[2], None); assert not b3["hedef_vuruldu"] and "ufuk" in b3["cikis_neden"] and b3["tutus_bar"] == 120
    # giriş=kapanış: kırılım ve giriş aynı bar
    qk, _ = dn["islemler"](OB, "kapanis"); Bk, bk = ns["ig_barlar"](qk.iloc[0], None)
    assert (Bk["rol"] == "kirilim+giris").sum() == 1 and bk["giris_fiyat"] == bk["kirilim_kapanis"]


def T2_sec(ns):
    q = pd.DataFrame({"sembol": ["A", "B", "C", "D"], "giris_t": pd.to_datetime(["2024-01-02", "2024-02-02", "2024-03-02", "2024-04-02"]), "cikis_t": pd.to_datetime(["2024-01-20", "2024-02-20", "2024-03-20", "2024-04-20"])})
    assert ns["ig_sec"](q, [0, 3, 99]) == [0, 3]
    assert ns["ig_sec"](q, [("B", "2024-02-02"), ("C", "2024-03-20"), ("D", "2024-03-25"), ("Z", "2024-01-01")]) == [1, 2, 3]
    r = ns["ig_sec"](q, "rastgele:2"); assert len(r) == 2 and len(set(r)) == 2 and all(0 <= i < 4 for i in r)


def T3_uctan_uca(ns):
    dn = denetim_ns(); OB = [kayit("S1"), kayit("S2", seed=2, kirilim_bar=5, hedef_bar=40, dusus_bar=70)]
    with tempfile.TemporaryDirectory() as K:
        T = ns["islem_goster"](K, OB, [0, 1], "t", dn["islemler"], {"kayit": {}, "veri": veri_from(OB)})
        assert len(T) == 2 and os.path.exists(os.path.join(K, "teshis", "t_ozet.csv"))
        d = sorted(os.listdir(os.path.join(K, "teshis")))
        assert any(f.endswith(".png") and "S1" in f for f in d) and any(f.endswith("_barlar.csv") and "S2" in f for f in d), d
        assert os.path.getsize(os.path.join(K, "teshis", [f for f in d if f.endswith(".png")][0])) > 20000
        assert np.allclose(T["getiri_net"], T["denetim_getiri"])


TESTLER = [T1_barlar_denetimle_ayni, T2_sec, T3_uctan_uca]
MUTASYONLAR = [
    ("kırılım tanımı DENETIM'den sapar (×1.002 yok)", 'tavan = float(np.maximum(o["sO"], o["sC"]).max()); kir = tavan * 1.002', 'tavan = float(np.maximum(o["sO"], o["sC"]).max()); kir = tavan * 1.05'),
    ("maliyet düşülmez", '"getiri_net": (cp / gp - 1) * 100 - IG_MALIYET', '"getiri_net": (cp / gp - 1) * 100'),
    ("hedef vuruş barı yanlış pencere", 'm = o["iH"][e + 1: jt + 1] >= hedef', 'm = o["iH"][e + 1: jt + 1] >= hedef * 2'),
    ("çıkış nedeni: ufuk tanımı bozuk", 'if jt == e + 120 else', 'if jt == e + 60 else'),
    ("seçim: aralık dışı satır alınır", "if 0 <= int(s) < len(q):", "if True:"),
    ("tutuş süresi yanlış", '"tutus_bar": jt - e,', '"tutus_bar": jt,'),
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
