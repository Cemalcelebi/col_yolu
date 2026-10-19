# -*- coding: utf-8 -*-
"""test_col_ogren — python -I test_col_ogren.py [--mutasyon]   (col_tanim2.py aynı klasörde)"""
import os
import sys
import tempfile
import traceback
import types

import numpy as np
import pandas as pd

KLASOR = os.path.dirname(os.path.abspath(__file__))
KAYNAK = open(os.path.join(KLASOR, "col_ogren.py"), encoding="utf-8").read()
TANIM = open(os.path.join(KLASOR, "col_tanim2.py"), encoding="utf-8").read()


def yukle(kod=KAYNAK):
    m = types.ModuleType("co_test"); m.__file__ = "col_ogren.py"; sys.modules["co_test"] = m
    exec(compile(TANIM, "col_tanim2.py", "exec"), m.__dict__)
    exec(compile(kod, "col_ogren.py", "exec"), m.__dict__)
    return m.__dict__


def barlar(c, gurultu=0.004, seed=1, start="2022-01-03"):
    rng = np.random.default_rng(seed); c = np.asarray(c, float); n = len(c)
    o = c * (1 + rng.normal(0, gurultu, n)); h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, gurultu * 1.5, n))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, gurultu * 1.5, n)))
    return pd.DataFrame({"Open": o, "High": h, "Low": l, "Close": c, "Volume": 2e5}, index=pd.bdate_range(start, periods=n))


def hisse(sonuc="EVET", seed=1, gurultu_on=0.012):
    """300 bar gürültülü geçmiş (sıkışma yok) + sol bacak 20→10 (40) + çöl: dipten sürünme (50) + sonuç: EVET fırlar, HAYIR dibin altına."""
    rng = np.random.default_rng(seed)
    gecmis = 20 * np.cumprod(1 + rng.normal(0, gurultu_on, 300)); gecmis = gecmis / gecmis[-1] * 20
    sol = 10 + 10 * np.linspace(1, 0, 40) ** 2
    kol = 10 * (1 + 0.10 * np.linspace(0, 1, 50) ** 1.3) + rng.normal(0, 0.02, 50); kol[0] = 9.99
    if sonuc == "EVET":
        son = np.linspace(kol[-1], kol[-1] * 1.4, 40)
    elif sonuc == "HAYIR":
        son = np.linspace(kol[-1], 9.0, 40)
    else:
        son = np.full(40, kol[-1])
    df = barlar(np.concatenate([gecmis, sol, kol, son]), seed=seed)
    return df, 340, 50                   # çöl başlangıcı, uzunluğu


def T1_aday_ve_etiket(ns):
    A = ns["OgrenAyar"](); K = ns["ColKural"]()
    df, bas, nc = hisse("EVET"); T = df.index[bas + nc - 1]
    o = ns["co_aday"](df, T, ns["ct_olc"], K, A); assert o is not None, "aday bulunamadı"
    i = df.index.get_loc(pd.Timestamp(o["bas"])); assert abs(i - bas) <= 6, (i, bas)
    assert o["tavan"] >= float(df["Close"].iloc[bas: bas + nc].max()) - 1e-9 and o["taban"] <= float(df["Low"].iloc[bas: bas + nc].min()) + 1e-9
    assert ns["co_etiket"](df, T, o["taban"], o["tavan"], A)[0] == "EVET"
    df2, _, _ = hisse("HAYIR"); assert ns["co_etiket"](df2, T, o["taban"], o["tavan"], A)[0] == "HAYIR"
    df3, _, _ = hisse("YOK"); assert ns["co_etiket"](df3, T, o["taban"], o["tavan"], A)[0] == "YOK"
    assert ns["co_etiket"](df, df.index[-5], o["taban"], o["tavan"], A)[0] == "KISA"
    assert ns["co_aday"](df, df.index[200], ns["ct_olc"], K, A) is None                       # gürültülü geçmişte aday yok (mumlar büyük)
    assert ns["co_aday"](df, df.index[bas + 5], ns["ct_olc"], K, A) is None                   # çölün 5. barı: pencere 15'ten kısa / sol bacak içeride
    # genç çöl: 10 bar düz + dip + 9 bar sürünme → dip pencerenin ortasında ama dipten sonra 15 bar yok → aday değil
    genc = np.concatenate([20 * np.cumprod(1 + np.random.default_rng(3).normal(0, 0.012, 300)), np.full(10, 10.1), [9.99], 10 * (1 + 0.05 * np.linspace(0, 1, 9))])
    dfg = barlar(genc, seed=3); assert ns["co_aday"](dfg, dfg.index[-1], ns["ct_olc"], K, A) is None


def T2_fitil_degil_govde(ns):
    A = ns["OgrenAyar"](); df, bas, nc = hisse("YOK"); T = df.index[bas + nc - 1]
    tavan = float(df["Close"].iloc[bas + nc - 1]); taban = 9.8
    j = df.index.get_loc(T) + 3; df.iloc[j, df.columns.get_loc("High")] = tavan * 1.15           # yalnız fitil tavanı deliyor
    assert ns["co_etiket"](df, T, taban, tavan, A)[0] == "YOK"
    df.iloc[j, df.columns.get_loc("Close")] = tavan * 1.03                                       # kapanış az üstünde → kırılım anı var ama onay yok
    et, kac, g, kir = ns["co_etiket"](df, T, taban, tavan, A); assert et == "YOK" and kir == 3, (et, kir)
    df.iloc[j, df.columns.get_loc("Close")] = tavan * 1.11                                       # kapanış %10+ üstünde → EVET
    assert ns["co_etiket"](df, T, taban, tavan, A)[0] == "EVET"
    df3, _, _ = hisse("YOK"); m = df3.index.get_loc(T) + 70
    df3 = pd.concat([df3, barlar(np.concatenate([np.full(40, tavan), np.full(40, tavan * 1.2)]), seed=9, start=df3.index[-1] + pd.Timedelta(days=1))])   # kırılım 81. bar: ufuk dışı
    assert ns["co_etiket"](df3, T, taban, tavan, A)[0] == "YOK"
    df2, _, _ = hisse("YOK"); k = df2.index.get_loc(T) + 2; df2.iloc[k, df2.columns.get_loc("Low")] = taban * 0.9
    assert ns["co_etiket"](df2, T, taban, tavan, A)[0] == "YOK"                                   # fitil dibi deliyor, kapanış değil
    df2.iloc[k, df2.columns.get_loc("Close")] = taban * 0.99; assert ns["co_etiket"](df2, T, taban, tavan, A)[0] == "HAYIR"


def T3_tara_ogren_rapor(ns):
    A = ns["OgrenAyar"](adim=10, bas="2023-03-01"); K = ns["ColKural"]()
    V = {}
    for i in range(4):
        V[f"E{i}"] = hisse("EVET", seed=10 + i)[0]
    for i in range(4):
        V[f"H{i}"] = hisse("HAYIR", seed=20 + i)[0]
    with tempfile.TemporaryDirectory() as Kd:
        S = ns["col_ogren"](Kd, {"kayit": {}, "veri": V}, ns["ct_olc"], ns["ColKural"], A=A)
        assert os.path.exists(os.path.join(Kd, "col_ogren_adaylar.csv")) and os.path.exists(os.path.join(Kd, "col_ogren_rapor.txt"))
        col_bas = V["E0"].index[340 - 6]                                                              # çöl bölgesi (öncesi rastgele yürüyüş, oradaki adaylar sayılmaz)
        Sc = S[pd.to_datetime(S.bas) >= col_bas]; e = Sc[Sc.sembol.str.startswith("E")]; h = Sc[Sc.sembol.str.startswith("H")]
        assert len(e) and len(h), S[["sembol", "etiket"]]
        assert (e.etiket.isin(["EVET", "YOK", "KISA"])).all() and (h.etiket.isin(["HAYIR", "YOK", "KISA"])).all(), S[["sembol", "tarih", "etiket"]]
        assert "EVET" in set(e.etiket) and "HAYIR" in set(h.etiket)
        assert not S.duplicated(subset=["sembol", "bas"]).any()
        r = open(os.path.join(Kd, "col_ogren_rapor.txt"), encoding="utf-8").read()
        assert "ayırma gücü" in r and "NEDENSEL" in r and "SİMETRİK" in r and "GERÇEK İZ" in r, r[-300:]
        assert "etiket_sim" in S.columns and "kapanis" in S.columns and S.kapanis.notna().all() and "doji_taban_15" in S.columns and S.doji_taban_15.notna().all()
        assert "DOJİ ÇEKİRDEĞİ" in r
        ok = S[S.etiket.isin(["EVET", "HAYIR"])]; assert (ok[ok.etiket == "EVET"].etiket_sim != "HAYIR_S").all()   # fırlayan EVET'ler simetrikte de aşağı değil
        # kaldığı yerden: durum var, ikinci çağrı tarama yapmaz, aynı sonuç
        S2 = ns["co_tara"](Kd, ns["_co_veri"](V), ns["ct_olc"], K, A); assert len(S2) == len(S)


def T3b_simetrik_ve_iz(ns):
    A = ns["OgrenAyar"](); df, bas, nc = hisse("EVET"); T = df.index[bas + nc - 1]
    assert ns["co_etiket_sim"](df, T, A) == "EVET_S"
    df2, _, _ = hisse("HAYIR"); assert ns["co_etiket_sim"](df2, T, A) == "HAYIR_S"
    df3, _, _ = hisse("YOK"); assert ns["co_etiket_sim"](df3, T, A) == "YOK_S"
    S = pd.DataFrame([{"sembol": "E0", "tarih": T, "taban": 9.8, "tavan": float(df["Close"].iloc[bas + nc - 1])}])
    S2 = ns["co_yeniden_etiketle"](S, {"E0": df}, A); assert S2.etiket.iloc[0] == "EVET" and S2.etiket_sim.iloc[0] == "EVET_S" and abs(S2.kapanis.iloc[0] - float(df.loc[T, "Close"])) < 1e-9
    T1 = pd.DataFrame({"olcu": ["a", "b", "c"], "auc": [0.7, 0.7, 0.5], "auc_d1": [0.7, 0.7, 0.5], "auc_d2": [0.7, 0.7, 0.5], "ayni_yon": [True, True, False], "guc": [0.2, 0.2, 0.0]})
    T2 = pd.DataFrame({"olcu": ["a", "b", "c"], "auc": [0.65, 0.5, 0.5], "auc_d1": [0.65, 0.5, 0.5], "auc_d2": [0.65, 0.5, 0.5], "ayni_yon": [True, False, False], "guc": [0.15, 0.0, 0.0]})
    M = ns["co_iz"](T1, T2); assert M[M.olcu == "a"].iz.iloc[0] and not M[M.olcu == "b"].iz.iloc[0] and M[M.olcu == "b"].kusku.iloc[0] and not M[M.olcu == "c"].kusku.iloc[0]


def T3c_doji_taban(ns):
    n = 30; ix = pd.bdate_range("2024-01-01", periods=n); c = np.full(n, 10.0); c[0] = 9.9; c[10:] = np.linspace(10.0, 10.6, 20)
    dojili = pd.DataFrame({"Open": c * 1.0002, "High": c * 1.01, "Low": c * 0.99, "Close": c, "Volume": 1e6}, index=ix)      # gövde aralığın %1'i → hepsi doji
    r = ns["co_doji_taban"](dojili, ix[0], ix[-1]); assert r["taban_bar"] >= 8 and r["doji_taban_15"] == r["taban_bar"] and r["doji_taban_oran"] == 1.0, r
    govdeli = dojili.copy(); govdeli["Open"] = c * 0.993                                                                      # gövde aralığın %50'si → doji yok
    r2 = ns["co_doji_taban"](govdeli, ix[0], ix[-1]); assert r2["doji_taban_15"] == 0 and r2["doji_taban_25"] == 0 and r2["taban_bar"] == r["taban_bar"], r2
    orta = dojili.copy(); orta["Open"] = c * 0.996                                                                             # gövde aralığın %20'si → 0,15'e göre değil, 0,25'e göre doji
    r3 = ns["co_doji_taban"](orta, ix[0], ix[-1]); assert r3["doji_taban_15"] == 0 and r3["doji_taban_25"] == r3["taban_bar"], r3
    dik = dojili.copy(); cd = np.concatenate([[9.9], np.linspace(10.5, 11.0, n - 1)]); dik["Close"] = cd; dik["Open"] = cd * 1.0002; dik["High"] = cd * 1.01; dik["Low"] = cd * 0.99
    r4 = ns["co_doji_taban"](dik, ix[0], ix[-1]); assert r4["taban_bar"] == 8, r4                                              # dip tek bar, %3 içinde başka yok → dipten 8 bar garantisi
    S = pd.DataFrame([{"sembol": "A", "bas": ix[0], "tarih": ix[-1], "etiket": "EVET", "etiket_sim": "EVET_S"}, {"sembol": "B", "bas": ix[0], "tarih": ix[-1], "etiket": "HAYIR", "etiket_sim": "HAYIR_S"}])
    S2 = ns["co_ek_olculer"](S, {"A": dojili, "B": govdeli}); assert S2.doji_taban_15.tolist() == [r["taban_bar"], 0]
    rp = ns["co_doji_rapor"](S2); assert "9+: n=1 EVET %100" in rp and "0–2: n=1 EVET %0" in rp, rp


def T4_auc(ns):
    assert abs(ns["_auc"](np.array([3, 4, 5.0]), np.array([0, 1, 2.0])) - 1.0) < 1e-9
    assert abs(ns["_auc"](np.array([0, 1, 2.0]), np.array([3, 4, 5.0])) - 0.0) < 1e-9
    assert abs(ns["_auc"](np.array([1, 2, 3.0]), np.array([1, 2, 3.0])) - 0.5) < 1e-9
    assert np.isnan(ns["_auc"](np.array([np.nan]), np.array([1.0])))


def T5_sizinti(ns):
    A = ns["OgrenAyar"](); K = ns["ColKural"]()
    df, bas, nc = hisse("EVET"); T = df.index[bas + nc - 1]
    S = pd.DataFrame([{"sembol": "E0", "tarih": T}])
    r = ns["co_sizinti"]({"E0": df}, S, ns["ct_olc"], K, A, ornek=1); assert r["fark"] == 0 and "NEDENSEL" in r["hukum"], r
    asil = ns["co_aday"]
    def aday_sizan(df_, T_, olc, K_, A_):                                   # geleceğe bakan aday: verilen serinin uzunluğunu ölçüye yazar
        o = asil(df_, T_, olc, K_, A_)
        if o: o["clv"] = float(len(df_))
        return o
    ns["co_aday"] = aday_sizan
    try:
        r2 = ns["co_sizinti"]({"E0": df}, S, ns["ct_olc"], K, A, ornek=1); assert r2["fark"] == 1 and "FARK" in r2["hukum"], r2
    finally:
        ns["co_aday"] = asil


def T6_veri_imza(ns):
    """v1.3: veri değişmezse tarama yok; bir hissenin geçmişi değişirse YALNIZ o yeniden taranır ve sonuç sıfırdan taramayla aynı;
    kesimden sonra eklenen bar imzayı bozmaz; imzasız (v1.2) durum sıfırdan taranır."""
    import pickle
    from collections import Counter
    A = ns["OgrenAyar"](adim=10, bas="2023-03-01"); K = ns["ColKural"]()
    V = {"E0": hisse("EVET", seed=10)[0], "E1": hisse("EVET", seed=11)[0], "H0": hisse("HAYIR", seed=20)[0], "H1": hisse("HAYIR", seed=21)[0]}
    asil = ns["co_aday"]; sayac = Counter(); kimlik = {}
    def say(df_, T_, *a):
        sayac[kimlik.get(id(df_), "?")] += 1
        return asil(df_, T_, *a)
    def kimlik_kur(v):
        kimlik.clear(); kimlik.update({id(d): s for s, d in v.items()})
    anahtar = ["sembol", "tarih", "bas", "etiket", "taban", "tavan"]
    def tablo(S):
        return S[anahtar].sort_values(["sembol", "bas", "tarih"]).reset_index(drop=True)
    ns["co_aday"] = say
    try:
        with tempfile.TemporaryDirectory() as Kd, tempfile.TemporaryDirectory() as Kd2:
            kimlik_kur(V); S1 = ns["co_tara"](Kd, V, ns["ct_olc"], K, A); assert len(S1) and sum(sayac.values()) > 0
            sayac.clear(); S2 = ns["co_tara"](Kd, V, ns["ct_olc"], K, A)
            assert sum(sayac.values()) == 0, sayac; pd.testing.assert_frame_equal(tablo(S1), tablo(S2))
            V2 = dict(V); V2["H0"] = hisse("EVET", seed=20)[0]                     # yalnız çöl SONRASI barlar değişir (390+)
            assert (V2["H0"].iloc[:390].values == V["H0"].iloc[:390].values).all() and not (V2["H0"].iloc[390:].values == V["H0"].iloc[390:].values).all()
            kimlik_kur(V2); sayac.clear(); S3 = ns["co_tara"](Kd, V2, ns["ct_olc"], K, A)
            assert set(sayac) == {"H0"}, sayac
            sayac.clear(); S3f = ns["co_tara"](Kd2, V2, ns["ct_olc"], K, A); n_tam = sum(sayac.values())
            pd.testing.assert_frame_equal(tablo(S3), tablo(S3f))
            assert not tablo(S3[S3.sembol == "H0"]).equals(tablo(S1[S1.sembol == "H0"])), "değişen hissenin adayları yenilenmedi"
            D = pickle.load(open(os.path.join(Kd, "col_ogren_durum.pkl"), "rb")); k = D["kesim"]
            ek = barlar(np.full(5, 12.0), seed=4, start=V2["E0"].index[-1] + pd.Timedelta(days=1))
            V3 = dict(V2); V3["E0"] = pd.concat([V2["E0"], ek])
            assert ns["_co_imza_esit"](ns["co_veri_imza"](V2, k)["E0"], ns["co_veri_imza"](V3, k)["E0"])          # yeni bar imzayı bozmaz
            D.pop("veri_imza"); D.pop("kesim"); pickle.dump(D, open(os.path.join(Kd, "col_ogren_durum.pkl"), "wb"))
            kimlik_kur(V2); sayac.clear(); S4 = ns["co_tara"](Kd, V2, ns["ct_olc"], K, A)
            assert set(sayac) == set(V2) and sum(sayac.values()) == n_tam, (sayac, n_tam)                       # imzasız durum → sıfırdan
            pd.testing.assert_frame_equal(tablo(S4), tablo(S3f))
    finally:
        ns["co_aday"] = asil


TESTLER = [T1_aday_ve_etiket, T2_fitil_degil_govde, T3_tara_ogren_rapor, T3b_simetrik_ve_iz, T3c_doji_taban, T4_auc, T5_sizinti, T6_veri_imza]
MUTASYONLAR = [
    ("etiket: fitil onayı sayılır", "if c >= tavan * (1 + A.onay_pay):", "if float(il['High'].iloc[j]) >= tavan * (1 + A.onay_pay):"),
    ("etiket: onay payı sıfır (sürünme EVET olur)", "if c >= tavan * (1 + A.onay_pay):", "if c >= tavan * (1 + A.al_pay):"),
    ("aday: genç çöl elenmez", "if uz - i_min < A.min_bar:", "if False:"),
    ("etiket: dip fitille kırılır", "if c < taban:", "if float(il['Low'].iloc[j]) < taban:"),
    ("etiket: ufuk sınırsız", "il = df[df.index > pd.Timestamp(T)].head(A.ufuk)", "il = df[df.index > pd.Timestamp(T)]"),
    ("aday: geleceğe bakar", 'x = df[df.index <= pd.Timestamp(T)]', "x = df"),
    ("tekilleştirme kalkar", 'drop_duplicates(subset=["sembol", "bas"], keep="first")', "drop_duplicates()"),
    ("simetrik etiket: aşağı bakılmaz", "if c <= p0 * (1 - A.sim_pay):", "if False:"),
    ("iz: simetrik etiket şartı kalkar", "m[\"iz\"] = (m.ayni_yon & m.ayni_yon_sim & (m.guc >= esik) & (m.guc_sim >= esik) & ((m.auc - 0.5) * (m.auc_sim - 0.5) > 0))", "m[\"iz\"] = (m.ayni_yon & (m.guc >= esik))"),
    ("doji eşiği 0,15 yerine 0,5", "d15 = int((g[m] < 0.15).sum())", "d15 = int((g[m] < 0.5).sum())"),
    ("taban bölgesi dipten 8 bar garantisi kalkar", "m[i_min: i_min + en_az_bar] = True", "pass"),
    ("AUC ters", "return float((sira[: len(poz)].sum() - len(poz) * (len(poz) + 1) / 2) / (len(poz) * len(neg)))", "return 1 - float((sira[: len(poz)].sum() - len(poz) * (len(poz) + 1) / 2) / (len(poz) * len(neg)))"),
    ("imza: değişen hisse görülmez", "if not _co_imza_esit(eski_imza.get(s), yeni_imza.get(s)))", "if False)"),
    ("imza: değişen hissenin eski adayları silinmez", 'D["satirlar"] = [r for r in D["satirlar"] if r["sembol"] not in dset]', "pass"),
    ("imza: değişen hisse yeniden taranmaz", "                for s in degisen:", "                for s in degisen[:0]:"),
    ("imza: imzasız eski durum kabul edilir", 'if ayni and D0.get("bitti") and not', 'if False and not'),
    ("imza: kesim sonrası barlar da sayılır", 'c = pd.to_numeric(df["Close"][df.index <= k], errors="coerce")', 'c = pd.to_numeric(df["Close"], errors="coerce")'),
    ("imza: kesim ilk tarih", 'D["kesim"] = max(D["bitti"])', 'D["kesim"] = min(D["bitti"])'),
    ("imza: karşılaştırma bar sayısına bakmaz, toplam yanlış", "int(a[0]) == int(b[0]) and bool(np.isclose(float(a[1]), float(b[1])", "int(a[0]) == int(b[0]) and bool(np.isclose(float(a[0]), float(b[0])"),
    ("sızıntı testi kesik seriyi kullanmaz", "b = co_aday(kesik, T, ct_olc, K, A)", "b = co_aday(df, T, ct_olc, K, A)"),
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
