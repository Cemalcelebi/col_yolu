# -*- coding: utf-8 -*-
"""test_tahtaci_oyunu — yapay dünya: çöküş → klimaks → tepki → dağıtım → sessiz geri çekilme.
Çalıştır: python -I test_tahtaci_oyunu.py  (aynı klasörde tahtaci_oyunu.py)
Mutasyon: python -I test_tahtaci_oyunu.py --mutasyon  (her mutasyonun en az bir testi düşürmesi gerekir)"""
import os
import re
import sys
import tempfile
import traceback

import numpy as np
import pandas as pd

KLASOR = os.path.dirname(os.path.abspath(__file__))
KAYNAK = open(os.path.join(KLASOR, "tahtaci_oyunu.py"), encoding="utf-8").read()


def yukle(kod: str = KAYNAK, on: dict = None):
    """Gerçek modül sözlüğünde yükler (dataclass sys.modules ister; Colab'daki exec de __main__ üzerinden aynı şeyi yapar)."""
    import types
    m = types.ModuleType("tahtaci_test"); m.__file__ = "tahtaci_oyunu.py"; sys.modules["tahtaci_test"] = m
    if on:
        m.__dict__.update(on)
    exec(compile(kod, "tahtaci_oyunu.py", "exec"), m.__dict__)
    m.__dict__["_TEST_KOD"] = kod
    return m.__dict__


def dunya(seed=1, n_once=120, cokus_gun=15, tepki_gun=6, bos=10, sonra=40, sessiz_hacim=400_000, klimaks_hacim=20_000_000, sonra_hacim=900_000):
    """Tek hisse: 120 gün yatay 20 TL, 15 günde 10'a çöker (hacim artar), klimaks günü dev hacim + çekiç,
    6 gün tepki (hacim yüksek) 14'e, dağıtım günü: 2× hacim + uzun üst fitil, sonra 10 gün sessiz geri çekilme 12'ye, sonra yatay."""
    rng = np.random.default_rng(seed)
    O, H, L, C, V = [], [], [], [], []
    p = 20.0
    for i in range(n_once):
        o = p * (1 + rng.normal(0, 0.004)); c = o * (1 + rng.normal(0, 0.004))
        h = max(o, c) * 1.004; l = min(o, c) * 0.996
        O.append(o); H.append(h); L.append(l); C.append(c); V.append(1_000_000 * (1 + rng.normal(0, 0.1)))
        p = c
    for i in range(cokus_gun):                      # çöküş: her gün −%4.5, hacim yükselir
        o = p; c = p * 0.955; h = o * 1.005; l = c * 0.99
        O.append(o); H.append(h); L.append(l); C.append(c); V.append(1_400_000 + 150_000 * i); p = c
    # klimaks: dibe vurur, kapanış üst yarıda, hacim 20 kat
    o = p; l = p * 0.90; c = p * 1.02; h = c * 1.01
    O.append(o); H.append(h); L.append(l); C.append(c); V.append(klimaks_hacim); p = c
    k_idx = len(C) - 1
    for i in range(tepki_gun):                      # tepki: açılış boşluklu, +%5/gün, hacim 3× normal
        o = p * 1.01; c = p * 1.05; h = c * 1.01; l = o * 0.995
        O.append(o); H.append(h); L.append(l); C.append(c); V.append(3_000_000); p = c
    # dağıtım: yukarı açılır, uzun üst fitil, kapanış gün ortasının altında, hacim 6× normal
    o = p * 1.02; h = p * 1.12; l = p * 0.99; c = p * 1.01
    O.append(o); H.append(h); L.append(l); C.append(c); V.append(6_000_000); p = c
    d_idx = len(C) - 1
    for i in range(bos):                            # sessiz geri çekilme: −%1.5/gün, hacim 0.4× normal
        o = p; c = p * 0.985; h = o * 1.003; l = c * 0.997
        O.append(o); H.append(h); L.append(l); C.append(c); V.append(sessiz_hacim); p = c
    for i in range(sonra):                          # yatay
        o = p; c = p * (1 + rng.normal(0, 0.003)); h = max(o, c) * 1.003; l = min(o, c) * 0.997
        O.append(o); H.append(h); L.append(l); C.append(c); V.append(sonra_hacim); p = c
    ix = pd.bdate_range("2024-01-01", periods=len(C))
    df = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=ix)
    return df, k_idx, d_idx


def T1_klimaks_yeri(ns):
    df, k, d = dunya()
    M = ns["to_metrikler"](df)
    idx = list(np.flatnonzero(M["klimaks"].to_numpy()))
    assert idx == [k], f"klimaks yanlış yerde: {idx} beklenen [{k}]"


def T2_fazlar(ns):
    df, k, d = dunya()
    M = ns["to_metrikler"](df)
    oy = ns["to_oyun"](M, k)
    assert oy["faz"][0] == "KLIMAKS"
    assert oy["dagitim_i"] == d, f"dağıtım günü {oy['dagitim_i']} beklenen {d}"
    assert all(f == "TEPKI" for f in oy["faz"][1:d - k]), oy["faz"][1:d - k]
    assert oy["sessiz_i"] is not None and oy["sessiz_i"] > d, oy["sessiz_i"]
    assert oy["kirik_i"] is None
    assert oy["maliyet"][-1] > oy["dip"]
    assert oy["teyit_i"] == k + 1, oy["teyit_i"]                  # ilk tepki günü klimaks yükseğinin üstünde kapanır


def T3_kirilma(ns):
    df, k, d = dunya()
    df = df.copy()
    j = k + 3
    df.iloc[j, df.columns.get_loc("Close")] = df["Low"].iloc[k] * 0.95        # dip altı kapanış
    df.iloc[j, df.columns.get_loc("Low")] = df["Low"].iloc[k] * 0.94
    M = ns["to_metrikler"](df)
    oy = ns["to_oyun"](M, k)
    assert oy["kirik_i"] == j and oy["faz"][j - k] == "KIRILDI" and all(f == "KIRILDI" for f in oy["faz"][j - k:])
    assert oy["dagitim_i"] is None


def T4_nedensellik(ns):
    """Geleceği kesince geçmiş metrikler değişmemeli."""
    df, k, d = dunya()
    M1 = ns["to_metrikler"](df)
    M2 = ns["to_metrikler"](df.iloc[: d + 1])
    for c in ("klimaks", "dagitim_aday", "cokus", "hacim_kat", "clv"):
        a = M1[c].iloc[: d + 1]; b = M2[c]
        assert (a.fillna(-9).to_numpy() == b.fillna(-9).to_numpy()).all(), f"{c} geleceğe bakıyor"
    oy1 = ns["to_oyun"](M1, k); oy2 = ns["to_oyun"](M2, k)
    assert oy1["faz"][: d - k + 1] == oy2["faz"], "oyun fazları geleceğe bakıyor"


def T5_olaylar_ve_getiri(ns):
    df, k, d = dunya()
    E = {"XXX": df}
    temel = pd.DataFrame({"defter_hisse": [25.0], "net_nakit": [5e6], "hisse_sayisi": [1e6], "kaynak": ["csv"]}, index=["XXX"])
    O = ns["to_olaylar"](E, temel)
    assert len(O) == 1 and O["sembol"].iloc[0] == "XXX"
    r = O.iloc[0]
    assert abs(r["pd_dd"] - r["fiyat"] / 25.0) < 1e-9
    assert r["nakit_pd"] > 0 and r["dagitim_gun"] == d - k and r["tutuldu"]
    T = ns["TahtaciTanim"]()
    assert r["teyit_gun"] == 1 and not r["teyit_sonra_kirildi"]
    bek_t = (df["Close"].iloc[k + 12] / df["Open"].iloc[k + 2] - 1 - 2 * T.maliyet) * 100
    assert abs(r["teyit_r10"] - bek_t) < 1e-9
    beklenen = (df["Close"].iloc[k + 11] / df["Open"].iloc[k + 1] - 1 - 2 * T.maliyet) * 100
    assert abs(r["klimaks_r10"] - beklenen) < 1e-9, (r["klimaks_r10"], beklenen)


def T6_cokus_esigi(ns):
    """%30'dan az düşen hisse klimaks vermemeli."""
    df, k, d = dunya()
    df = df.copy()
    sig = df.iloc[: k - 15].copy()                     # çöküşü sil: sadece yatay + küçük düşüş
    sig = pd.concat([sig, df.iloc[k:].assign(**{c: df[c].iloc[k:] * 1.9 for c in ("Open", "High", "Low", "Close")})])
    M = ns["to_metrikler"](sig)
    assert not M["klimaks"].any(), "düşüşsüz klimaks üretildi"


def T7_temel_csv(ns):
    with tempfile.TemporaryDirectory() as K:
        pd.DataFrame({"sembol": ["abc.is", "DEF"], "defter_hisse": [10, 20], "net_nakit": [1, -2], "hisse_sayisi": [100, 200]}).to_csv(os.path.join(K, "tahtaci_temel.csv"), index=False)
        T = ns["to_temel_oku"](K, ["ABC", "DEF", "GHI"])
        assert list(T.index) == ["ABC", "DEF"] and T.loc["ABC", "defter_hisse"] == 10 and (T["kaynak"] == "csv").all()


def T8_temel_indir_kaldigi_yerden(ns):
    sayac = {"n": 0}

    def indir(s):
        sayac["n"] += 1
        if sayac["n"] == 2:
            raise RuntimeError("kesildi")
        return {"defter_hisse": 1.0, "net_nakit": 0.0, "hisse_sayisi": 1.0, "kaynak": "sahte"}
    with tempfile.TemporaryDirectory() as K:
        T = ns["to_temel_oku"](K, ["A", "B", "C"], indir=indir, parti=1)
        assert len(T) == 3 and str(T.loc["B", "kaynak"]).startswith("hata")
        T2 = ns["to_temel_oku"](K, ["A", "B", "C", "D"], indir=indir, parti=1)
        assert sayac["n"] == 4 and len(T2) == 4, "önbellek kaldığı yerden sürmedi"


def T9_karne_ve_hukum(ns):
    rng = np.random.default_rng(3)
    n = 80
    O = pd.DataFrame({"sembol": [f"S{i}" for i in range(n)], "tarih": pd.bdate_range("2024-01-01", periods=n),
                      "klimaks_r10": rng.normal(4, 3, n), "sessiz_r10": rng.normal(-1, 3, n), "dagitim_r10": rng.normal(0, 1, n),
                      "tutuldu": [True] * 60 + [False] * 20, "dagitim_gun": [5] * 50 + [np.nan] * 30, "sessiz_gun": [9] * 40 + [np.nan] * 40,
                      "pd_dd": np.r_[np.full(40, 0.7), np.full(40, 1.4)], "nakit_pd": np.r_[np.full(40, 0.2), np.full(40, -0.1)]})
    R = ns["to_karne"](O)
    h = ns["to_hukum"](R)
    assert "klimaks: İZ" in h and "sessiz: GEÇMEDİ" in h, h
    assert R["tutuldu_pay"] == 0.75 and abs(R["dagitim_pay"] - 50 / 80) < 1e-9
    assert "pd_dd_klimaks" in R and R["pd_dd_klimaks"]["n_alt"] == 40
    rapor = ns["to_rapor"](O, R, "yfinance_bugun")
    assert "UYARI" in rapor and "HÜKÜM" in rapor


def T10_evren_ve_norm(ns):
    df, k, d = dunya()
    V = {"kayit": {}, "veri": {"ersu.is": df, "BOS": pd.DataFrame(), "KOTU": df[["Close"]]}}
    E = ns["to_evren"](V)
    assert list(E) == ["ERSU"] and list(E["ERSU"].columns) == ["O", "H", "L", "C", "V"]


def T11_cakisma_kapisi(ns):
    kod = ns["_TEST_KOD"]
    try:
        yukle(kod, on={"to_oyun": 1})
    except RuntimeError as e:
        assert "çakışma kapısı" in str(e)
    else:
        raise AssertionError("çakışma kapısı çalışmadı")
    yukle(kod, on={"to_oyun": 1, "_TO_IMZA": "tahtaci_oyunu"})  # kendi üstüne yüklenir


def T12_hacimsiz_dip_klimaks_degil(ns):
    """Dip günü hacim düşükse (satan tükenmemiş) klimaks sayılmaz."""
    df, k, d = dunya(klimaks_hacim=1_000_000)
    M = ns["to_metrikler"](df)
    assert not M["klimaks"].iloc[k], "hacimsiz dip klimaks sayıldı"


def T13_zirve_ve_normal_bugunu_disarda_tutar(ns):
    df, k, d = dunya()
    M = ns["to_metrikler"](df)
    T = ns["TahtaciTanim"]()
    j = d                                             # dağıtım günü: bugünkü H ve V uç değer
    assert abs(M["zirve"].iloc[j] - M["H"].iloc[j - T.zirve_pencere: j].max()) < 1e-9, "zirve bugünü içeriyor"
    assert abs(M["hacim_normal"].iloc[j] - M["V"].iloc[j - T.hacim_taban_gun: j].median()) < 1e-6, "hacim normali bugünü içeriyor"


def T14_gurultulu_geri_cekilme_sessiz_degil(ns):
    df, k, d = dunya(sessiz_hacim=5_000_000, sonra_hacim=5_000_000)
    M = ns["to_metrikler"](df)
    oy = ns["to_oyun"](M, k)
    assert oy["dagitim_i"] == d and oy["sessiz_i"] is None, oy["sessiz_i"]


def T15_hukum_yarilar_ters(ns):
    rng = np.random.default_rng(5)
    n = 80
    O = pd.DataFrame({"sembol": [f"S{i}" for i in range(n)], "tarih": pd.bdate_range("2024-01-01", periods=n),
                      "klimaks_r10": np.r_[rng.normal(8, 1, 40), rng.normal(-1, 1, 40)], "sessiz_r10": rng.normal(2, 1, n),
                      "tutuldu": [True] * n, "dagitim_gun": [np.nan] * n, "sessiz_gun": [np.nan] * n})
    R = ns["to_karne"](O)
    assert R["klimaks"]["band"][0] > 0
    assert "klimaks: GEÇMEDİ" in ns["to_hukum"](R), ns["to_hukum"](R)


def T16_sahte_klimaks_sonrasi_gercek_klimaks(ns):
    """İlk klimaks kırılırsa (ERSU 23 Eyl), kırılmadan sonraki yeni klimaks (30 Eyl) ayrı olay olarak alınmalı."""
    df, k, d = dunya()
    df2 = df.copy()
    # klimakstan 3 gün sonra dibi kır, 2 gün daha düş, sonra yeni (daha büyük) klimaks
    j = k + 3
    f = df2.columns.get_loc
    for n, m in enumerate((0.93, 0.90, 0.88)):
        df2.iloc[j + n, f("Open")] = df["Low"].iloc[k] * (m + 0.02); df2.iloc[j + n, f("High")] = df["Low"].iloc[k] * (m + 0.03)
        df2.iloc[j + n, f("Low")] = df["Low"].iloc[k] * m; df2.iloc[j + n, f("Close")] = df["Low"].iloc[k] * (m + 0.01)
        df2.iloc[j + n, f("Volume")] = 2_500_000
    g = j + 3                                      # gerçek klimaks
    df2.iloc[g, f("Open")] = df["Low"].iloc[k] * 0.87; df2.iloc[g, f("Low")] = df["Low"].iloc[k] * 0.80
    df2.iloc[g, f("Close")] = df["Low"].iloc[k] * 0.89; df2.iloc[g, f("High")] = df["Low"].iloc[k] * 0.90
    df2.iloc[g, f("Volume")] = 30_000_000
    for n in range(g + 1, min(g + 15, len(df2))):      # sonrası: dip üstünde tepki, hacim normal
        df2.iloc[n, f("Low")] = df["Low"].iloc[k] * 0.85; df2.iloc[n, f("Open")] = df["Low"].iloc[k] * 0.9
        df2.iloc[n, f("Close")] = df["Low"].iloc[k] * (0.9 + 0.01 * (n - g)); df2.iloc[n, f("High")] = df2.iloc[n, f("Close")] * 1.01
        df2.iloc[n, f("Volume")] = 1_000_000
    O = ns["to_olaylar"]({"X": df2})
    assert len(O) == 2, f"kırılma sonrası ikinci klimaks alınmadı: {len(O)} olay"
    assert O["kirik_gun"].iloc[0] == 3 and np.isnan(O["kirik_gun"].iloc[1]), O[["tarih", "kirik_gun"]]
    assert list(O["onceki_sahte"]) == [0, 1], list(O["onceki_sahte"])
    # oyun sürerken (kırılma yok) 40 gün içinde ikinci klimaks alınmaz
    O1 = ns["to_olaylar"]({"X": df})
    assert len(O1) == 1


def T17_teyit_gelmeyince_bos(ns):
    """Teyit penceresinde kapanış klimaks yükseğini aşmazsa teyit yok; teyitten sonra kırılma ayrıca sayılır."""
    df, k, d = dunya()
    df2 = df.copy(); f = df2.columns.get_loc
    hi = df["High"].iloc[k]
    for n in range(k + 1, k + 6):                     # 5 gün yüksek altında yatay
        df2.iloc[n, f("Open")] = hi * 0.97; df2.iloc[n, f("Close")] = hi * 0.98; df2.iloc[n, f("High")] = hi * 0.995; df2.iloc[n, f("Low")] = hi * 0.96
    M = ns["to_metrikler"](df2); oy = ns["to_oyun"](M, k)
    assert oy["teyit_i"] is None
    # dibi delip yüksek üstünde kapanan tek gün: dip test edilmiş, teyit sayılmaz
    df4 = df.copy(); dip = df["Low"].iloc[k]
    df4.iloc[k + 1, f("Low")] = dip * 0.97; df4.iloc[k + 1, f("Open")] = dip * 0.99
    df4.iloc[k + 1, f("Close")] = hi * 1.02; df4.iloc[k + 1, f("High")] = hi * 1.03
    oy4 = ns["to_oyun"](ns["to_metrikler"](df4), k)
    assert oy4["teyit_i"] != k + 1, "dip altına sarkan gün teyit sayıldı"
    # teyit sonra kırılma
    df3 = df.copy(); j = k + 3
    df3.iloc[j, f("Close")] = df["Low"].iloc[k] * 0.95; df3.iloc[j, f("Low")] = df["Low"].iloc[k] * 0.94
    O = ns["to_olaylar"]({"X": df3})
    assert O["teyit_gun"].iloc[0] == 1 and bool(O["teyit_sonra_kirildi"].iloc[0])


def T18_donem_bazli_temel(ns):
    """Olay gününde bilinen son bilanço kullanılır; sonraki bilanço görülmez (sızıntı yok)."""
    df, k, d = dunya()
    tarih = df.index[k]
    temel = pd.DataFrame({"defter_hisse": [25.0], "net_nakit": [5e6], "hisse_sayisi": [1e6], "kaynak": ["yfinance_bugun"]}, index=["XXX"])
    td = pd.DataFrame({"sembol": ["XXX", "XXX", "XXX"], "aciklama": [tarih - pd.Timedelta(days=100), tarih - pd.Timedelta(days=10), tarih + pd.Timedelta(days=5)],
                       "ozkaynak": [10e6, 12e6, 50e6], "net_borc": [-1e6, 2e6, -9e6]})
    O = ns["to_olaylar"]({"XXX": df}, temel, temel_donem=td)
    r = O.iloc[0]
    assert r["temel_kaynak"] == "donem"
    assert abs(r["pd_dd"] - r["fiyat"] / 12.0) < 1e-9, r["pd_dd"]          # 12e6 / 1e6 hisse = 12 TL defter
    assert abs(r["nakit_pd"] - (-2e6) / (1e6 * r["fiyat"])) < 1e-12
    with tempfile.TemporaryDirectory() as K:
        assert ns["to_temel_donem"](K) is None
        td.to_csv(os.path.join(K, "temel_duz.csv"), index=False)
        t2 = ns["to_temel_donem"](K); assert len(t2) == 3 and list(t2.columns) == ["sembol", "aciklama", "ozkaynak", "net_borc"]
        oz, nb = ns["to_temel_o_gun"](t2, "XXX", tarih); assert oz == 12e6 and nb == 2e6
        assert np.isnan(ns["to_temel_o_gun"](t2, "YYY", tarih)[0])


TESTLER = [T1_klimaks_yeri, T2_fazlar, T3_kirilma, T4_nedensellik, T5_olaylar_ve_getiri, T6_cokus_esigi, T7_temel_csv,
           T8_temel_indir_kaldigi_yerden, T9_karne_ve_hukum, T10_evren_ve_norm, T11_cakisma_kapisi,
           T12_hacimsiz_dip_klimaks_degil, T13_zirve_ve_normal_bugunu_disarda_tutar, T14_gurultulu_geri_cekilme_sessiz_degil, T15_hukum_yarilar_ters, T16_sahte_klimaks_sonrasi_gercek_klimaks, T17_teyit_gelmeyince_bos, T18_donem_bazli_temel]

MUTASYONLAR = [
    ("klimaks hacim şartı kalkar", "(M[\"V\"] >= hacim_max) & ", ""),
    ("klimaks CLV şartı kalkar", "& (M[\"clv\"] >= T.klimaks_clv_min)", ""),
    ("çöküş şartı kalkar", "& (M[\"cokus\"] >= T.cokus_min)", ""),
    ("zirve geleceğe bakar (shift kalkar)", ".max().shift(1)", ".max()"),
    ("hacim normali geleceğe bakar", ".median().shift(1)\n    M[\"ciro_normal\"]", ".median()\n    M[\"ciro_normal\"]"),
    ("kırılma kontrolü kalkar", "if r[\"C\"] < dip:", "if False:"),
    ("dağıtım üst fitil/clv şartı kalkar", "& ((M[\"ust_fitil\"] >= T.dagitim_fitil_min) | (M[\"clv\"] < 0))", ""),
    ("sessiz: hacim şartı kalkar", "and son.mean() < T.sessiz_hacim_kat * float(M[\"V\"].iloc[dagitim_i])", ""),
    ("getiri giriş aynı gün kapanış", "giris = float(M[\"O\"].iloc[i + 1])", "giris = float(M[\"C\"].iloc[i])"),
    ("maliyet düşülmez", "- 2 * T.maliyet)", ")"),
    ("hüküm: yarı şartı kalkar", "iz = lo > 0 and y1 > 0 and y2 > 0", "iz = lo > 0"),
    ("temel csv sembol normalize edilmez", "T[\"sembol\"] = T[\"sembol\"].map(_to_norm)", "pass"),
    ("önbellek yazılmaz", "pickle.dump(D, open(yol, \"wb\"))", "pass"),
    ("çakışma kapısı kapanır", "if _to_catisan:", "if False:"),
    ("teyit: yüksek şartı kalkar", 'and r["C"] > k_yuksek and r["L"] > dip:', 'and r["L"] > dip:'),
    ("teyit: dip şartı kalkar", 'and r["C"] > k_yuksek and r["L"] > dip:', 'and r["C"] > k_yuksek:'),
    ("dönem temeli geleceğe bakar", '(td["aciklama"] <= tarih)', '(td["aciklama"] <= tarih + pd.Timedelta(days=30))'),
    ("sahte klimaks sayılmaz", "onceki_sahte = sum(1 for j in kirilanlar if k - j <= T.oyun_omru)", "onceki_sahte = 0"),
    ("kırılma sonrası klimaks serbest bırakılmaz", 'serbest = oy["kirik_i"] if oy["kirik_i"] is not None else int(k) + T.oyun_omru', "serbest = int(k) + T.oyun_omru"),
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
            assert eski in KAYNAK, f"mutasyon hedefi kaynakta yok: {ad}"
            kod = KAYNAK.replace(eski, yeni, 1)
            try:
                ns = yukle(kod)
            except Exception as e:
                print(f"  ✓ yakalandı (yükleme): {ad}"); continue
            h = kos(ns, sessiz=True)
            print(f"  {'✓ yakalandı' if h else '✗ KAÇTI'}: {ad}" + (f" ← {h[0][0]}" if h else ""))
            if not h:
                kacan.append(ad)
        print(f"\n{len(MUTASYONLAR) - len(kacan)}/{len(MUTASYONLAR)} mutasyon yakalandı"); sys.exit(1 if kacan else 0)
    ns = yukle()
    h = kos(ns)
    print(f"\n{len(TESTLER) - len(h)}/{len(TESTLER)} test geçti"); sys.exit(1 if h else 0)
