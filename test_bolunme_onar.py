# -*- coding: utf-8 -*-
"""test_bolunme_onar — python -I test_bolunme_onar.py [--mutasyon]"""
import os
import pickle
import sys
import tempfile
import traceback
import types

import numpy as np
import pandas as pd

KLASOR = os.path.dirname(os.path.abspath(__file__))
KAYNAK = open(os.path.join(KLASOR, "bolunme_onar.py"), encoding="utf-8").read()


def yukle(kod=KAYNAK, on=None):
    m = types.ModuleType("bolunme_test"); m.__file__ = "bolunme_onar.py"; sys.modules["bolunme_test"] = m
    if on:
        m.__dict__.update(on)
    exec(compile(kod, "bolunme_onar.py", "exec"), m.__dict__)
    return m.__dict__


def seri(n=200, bas=100.0, seed=1):
    """Yatay gürültülü seri; bedelsiz yok."""
    rng = np.random.default_rng(seed)
    c = bas * np.cumprod(1 + rng.normal(0, 0.01, n))
    ix = pd.bdate_range("2024-01-01", periods=n)
    return pd.DataFrame({"Open": c * (1 + rng.normal(0, 0.003, n)), "High": c * 1.012, "Low": c * 0.988, "Close": c, "Volume": 1e6 + rng.integers(0, 1e5, n)}, index=ix)


def bedelsiz_uygula(df, k, oran):
    """k gününden itibaren fiyatlar oran ile çarpılır (ham Yahoo'nun yaptığı gibi: geçmiş düzeltilmez), hacim bölünür."""
    d = df.copy()
    for c in ("Open", "High", "Low", "Close"):
        d.iloc[k:, d.columns.get_loc(c)] = d[c].iloc[k:] * oran
    d.iloc[k:, d.columns.get_loc("Volume")] = d["Volume"].iloc[k:] / oran
    return d


def T1_bul(ns):
    df = seri(); ham = bedelsiz_uygula(df, 120, 0.5)           # %100 bedelsiz
    ol = ns["bo_bul"](ham)
    assert len(ol) == 1 and ol[0][0] == 120 and abs(ol[0][1] - 0.5) < 0.03, ol
    assert ns["bo_bul"](df) == [], "bedelsizsiz seride olay bulundu"
    # bedelsiz günü içinde +%8 hareket: oran açılıştan (referans) okunmalı, kapanıştan değil
    h8 = ham.copy(); h8.iloc[120, h8.columns.get_loc("Open")] = df["Close"].iloc[119] * 0.5
    h8.iloc[120, h8.columns.get_loc("Close")] = df["Close"].iloc[119] * 0.5 * 1.08; h8.iloc[120, h8.columns.get_loc("High")] = h8["Close"].iloc[120] * 1.005
    ol8 = ns["bo_bul"](h8); assert len(ol8) == 1 and abs(ol8[0][1] - 0.5) < 0.005, ol8
    ters = bedelsiz_uygula(df, 80, 4.0)                        # birleştirme
    ol2 = ns["bo_bul"](ters); assert len(ol2) == 1 and ol2[0][0] == 80 and abs(ol2[0][1] - 4.0) < 0.2, ol2


def T2_onar_geri_getirir(ns):
    df = seri(); ham = bedelsiz_uygula(df, 120, 0.5)
    yeni, kayit = ns["bo_onar"](ham, ns["bo_bul"](ham))
    assert kayit[0]["onarildi"]
    # onarılmış seri, orijinalin 0.5 ile çarpılmış haline eşit olmalı (bedelsiz sonrası düzeyde süreklilik)
    hedef = df.copy()
    for c in ("Open", "High", "Low", "Close"):
        hedef[c] = hedef[c] * (yeni["Close"].iloc[150] / df["Close"].iloc[150])
    oran = yeni["Close"].iloc[150] / df["Close"].iloc[150]
    assert abs(oran - 0.5) < 1e-9
    assert np.allclose(yeni["Close"].to_numpy(), hedef["Close"].to_numpy(), rtol=0.02), "geçmiş çarpılmadı"
    assert np.allclose(yeni["Volume"].to_numpy(), (df["Volume"] / 0.5).to_numpy(), rtol=0.02), "hacim bölünmedi"
    assert ns["bo_bul"](yeni) == [], "onarımdan sonra olay kalmamalı"


def T3_iki_olay(ns):
    df = seri(); ham = bedelsiz_uygula(bedelsiz_uygula(df, 60, 0.5), 150, 0.25)
    yeni, kayit = ns["bo_onar"](ham, ns["bo_bul"](ham))
    assert len(kayit) == 2 and all(r["onarildi"] for r in kayit)
    g = yeni["Close"] / df["Close"]
    # oran açılıştan tahmin edilir: ~%0,5 hassasiyet (açılış gürültüsü); eski seviyelerde %1 içinde
    assert abs(g.iloc[10] / 0.125 - 1) < 0.01 and abs(g.iloc[100] / 0.125 - 1) < 0.01 and abs(g.iloc[190] - 0.125) < 1e-9, g.iloc[[10, 100, 190]].tolist()


def T4_supheli_onarilmaz(ns):
    """Oran açılışa göre ama kapanış çok farklı: onarım sonrası fark > %15 → onarılmaz."""
    df = seri(); ham = df.copy(); k = 120
    ham.iloc[k, ham.columns.get_loc("Open")] = df["Close"].iloc[k - 1] * 0.5     # açılış yarı
    for c in ("High", "Low", "Close"):
        ham.iloc[k:, ham.columns.get_loc(c)] = df[c].iloc[k:] * 0.5
    ham.iloc[k + 1:, ham.columns.get_loc("Open")] = df["Open"].iloc[k + 1:] * 0.5
    # güven eşiğini sıkı yapıp yapay fark üret: açılışı 0.3'e çek
    ham.iloc[k, ham.columns.get_loc("Open")] = df["Close"].iloc[k - 1] * 0.3
    yeni, kayit = ns["bo_onar"](ham, [(k, 0.5)])
    assert not kayit[0]["onarildi"], kayit
    assert np.allclose(yeni["Close"].to_numpy(), ham["Close"].to_numpy()), "şüpheli olay yine de onarıldı"


def T5_dosya_ve_yedek(ns):
    with tempfile.TemporaryDirectory() as K:
        df = seri(); ham = bedelsiz_uygula(df, 120, 0.5)
        pickle.dump({"kayit": {"a": 1}, "veri": {"XXX": ham, "YYY": df}}, open(os.path.join(K, "veri_1d_turkey.pkl"), "wb"))
        R = ns["bolunme_onar"](K, uygula=False)
        assert len(R["olaylar"]) == 1 and R["degisen_hisse"] == 0
        assert not any(f.startswith("veri_1d_turkey.pkl.yedek") for f in os.listdir(K))
        R2 = ns["bolunme_onar"](K)
        assert R2["degisen_hisse"] == 1
        P = pickle.load(open(os.path.join(K, "veri_1d_turkey.pkl"), "rb"))
        assert ns["bo_bul"](P["veri"]["XXX"]) == [] and P["kayit"]["a"] == 1 and P["kayit"]["bolunme_onar"]["olay"] == 1
        assert np.allclose(P["veri"]["YYY"]["Close"].to_numpy(), df["Close"].to_numpy())
        assert any(f.startswith("veri_1d_turkey.pkl.yedek_bolunme") for f in os.listdir(K))
        assert os.path.exists(os.path.join(K, "bolunme_olaylar.csv"))


def T6_kucuk_sutun_adlari(ns):
    df = seri(); ham = bedelsiz_uygula(df, 120, 0.5); ham.columns = [c.lower() for c in ham.columns]
    ol = ns["bo_bul"](ham); assert len(ol) == 1
    yeni, kayit = ns["bo_onar"](ham, ol); assert kayit[0]["onarildi"] and ns["bo_bul"](yeni) == []


def T8_ara_bolge(ns):
    df = seri(); ham = bedelsiz_uygula(df, 120, 0.72)          # %40 bedelsiz: ara bölge
    assert ns["bo_bul"](ham) == [] and len(ns["bo_supheli"](ham)) == 1 and ns["bo_supheli"](ham)[0][0] == 120
    ham2 = bedelsiz_uygula(df, 120, 0.5)
    assert ns["bo_supheli"](ham2) == [] and len(ns["bo_bul"](ham2)) == 1
    with tempfile.TemporaryDirectory() as K:
        pickle.dump({"veri": {"XXX": ham}}, open(os.path.join(K, "veri_1d_turkey.pkl"), "wb"))
        R = ns["bolunme_onar"](K)
        assert R["degisen_hisse"] == 0 and len(R["ara_bolge"]) == 1 and os.path.exists(os.path.join(K, "bolunme_ara_bolge.csv"))


def T9_int_hacim(ns):
    df = seri(); ham = bedelsiz_uygula(df, 120, 0.5); ham["Volume"] = ham["Volume"].round().astype("int64")
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        yeni, kayit = ns["bo_onar"](ham, ns["bo_bul"](ham))
    assert kayit[0]["onarildi"] and yeni["Volume"].dtype == float


def T10_acilis_hatasi_onarilmaz(ns):
    """Açılış 0.5× ama kapanış normal: Yahoo açılış hatası → onarılmaz, neden=acilis_hatasi; kapanış da 0.5× ise onarılır."""
    df = seri(); k = 120
    hata = df.copy(); hata.iloc[k, hata.columns.get_loc("Open")] = df["Close"].iloc[k - 1] * 0.5
    hata.iloc[k, hata.columns.get_loc("Low")] = min(hata["Low"].iloc[k], hata["Open"].iloc[k])
    ol = ns["bo_bul"](hata); assert len(ol) == 1
    yeni, kayit = ns["bo_onar"](hata, ol)
    assert not kayit[0]["onarildi"] and kayit[0]["neden"] == "acilis_hatasi", kayit
    assert np.allclose(yeni["Close"].to_numpy(), hata["Close"].to_numpy())
    gercek = bedelsiz_uygula(df, k, 0.5)
    yeni2, kayit2 = ns["bo_onar"](gercek, ns["bo_bul"](gercek)); assert kayit2[0]["onarildi"] and kayit2[0]["neden"] == ""


def T11_dogrula_yedekten(ns):
    with tempfile.TemporaryDirectory() as K:
        df = seri(); k = 120
        gercek = bedelsiz_uygula(df, k, 0.5)
        hata = df.copy(); hata.iloc[k, hata.columns.get_loc("Open")] = df["Close"].iloc[k - 1] * 0.5; hata.iloc[k, hata.columns.get_loc("Low")] = hata["Open"].iloc[k]
        yol = os.path.join(K, "veri_1d_turkey.pkl")
        # "eski onarım": her ikisi de açılış oranıyla onarılmış gibi (hatalı olan da çarpılmış)
        bozuk_onarim = hata.copy()
        for c in ("Open", "High", "Low", "Close"):
            bozuk_onarim.iloc[:k, bozuk_onarim.columns.get_loc(c)] = hata[c].iloc[:k] * 0.5
        pickle.dump({"veri": {"GERCEK": gercek, "HATA": hata}}, open(yol + ".yedek_bolunme_20260101_0000", "wb"))
        pickle.dump({"veri": {"GERCEK": gercek, "HATA": bozuk_onarim}}, open(yol, "wb"))
        R = ns["bolunme_dogrula"](K)
        assert R["geri_alinan_hisse"] == 1 and len(R["olaylar"]) == 2 and R["olaylar"]["onarildi"].sum() == 1
        P = pickle.load(open(yol, "rb"))
        assert np.allclose(P["veri"]["HATA"]["Close"].to_numpy(), hata["Close"].to_numpy()), "açılış hatası geri alınmadı"
        assert ns["bo_bul"](P["veri"]["GERCEK"]) == [], "gerçek bedelsiz onarılmadı"


def T7_cakisma(ns):
    try:
        yukle(on={"bo_bul": 1})
    except RuntimeError as e:
        assert "çakışma" in str(e)
    else:
        raise AssertionError("kapı çalışmadı")


TESTLER = [T1_bul, T2_onar_geri_getirir, T3_iki_olay, T4_supheli_onarilmaz, T5_dosya_ve_yedek, T6_kucuk_sutun_adlari, T7_cakisma, T8_ara_bolge, T9_int_hacim, T10_acilis_hatasi_onarilmaz, T11_dogrula_yedekten]
MUTASYONLAR = [
    ("kapanış doğrulaması kalkar", "ok = np.isfinite(fark) and fark <= guven and kap_ok", "ok = np.isfinite(fark) and fark <= guven"),
    ("ara bölge alt sınırı kalkar", "if f > alt]", "]"),
    ("alt eşik kalkar", "(oran <= esik_alt) | (oran >= esik_ust)", "(oran >= esik_ust)"),
    ("hacim bölünmez", 'out.iloc[:i, out.columns.get_loc(k["volume"])] = pd.to_numeric(out[k["volume"]], errors="coerce").iloc[:i] / f', "pass"),
    ("güven kontrolü kalkar", "ok = np.isfinite(fark) and fark <= guven", "ok = True"),
    ("yedek alınmaz", 'shutil.copy(yol, yol + time.strftime(".yedek_bolunme_%Y%m%d_%H%M"))', "pass"),
    ("uygula=False yine değiştirir", "if uygula and any(r[\"onarildi\"] for r in kayit):", "if any(r[\"onarildi\"] for r in kayit):"),
    ("sadece Close kullanılır (açılış yok)", 'ref = np.where(np.isfinite(O) & (O > 0), O, C)', "ref = C"),
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
