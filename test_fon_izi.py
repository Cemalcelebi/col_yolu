# test_fon_izi.py — FON_IZI mekanik sinama (2026-10-22)
# Calistir: python3 test_fon_izi.py   (repo kokunde; veri indirilmez, sentetik seri)
# 1) Bolunme duzeltme: %50 bedelsiz sicramasi (2020 sonrasi, sinir %10) duzeltilir, gercek %9 tavan gunu dokunulmaz; hacim ters carpan.
# 2) Pencere olculeri: tabansiz istikrarli yukseliste taban=0, verim yuksek; bir -%10 gun eklenince taban=1.
# 3) Sonuc: once 2 kat / once -%30 dogru isaretlenir.
# 4) Kosu: dip, ilk 2 kat ve tepe dogru bulunur; kriz tarihinden sonraki tepe sayilmaz.
# 6) v1.1 hacim esligi: kucuk mumlu, kuru hacimli, yukselis gunlerinde hacimli sessiz yukselis Z0 sayilir; hk < 1, udvr > 1, dh < 1.
# 5) Cakisma kapisi: modul bellekteki baska bir adi ezerse durur.
# 7) v1.2 gelecege bakmama: 500 bara kesilen seride butun gostergeler ve sinyaller tam serinin ilk 500 bariyla ayni.
# 8) v1.2 vektorlu sonuc (_fi_ilk) = dongu (_fi_once).
# 9) v1.2 uyumsuzluk: fiyat daha dusuk dip + gosterge daha yuksek dip -> duz boga, sinyal pivotun dogrulandigi gun (p+k).
# 10) v1.2 KAP esleme: 18:00 sonrasi bildirim ertesi islem gunu, hafta sonu bildirimi pazartesi.
# 11) v1.2 blok hacim: kilitli tavan serisi icinde 50x hacimli tavan gunu blok_tavan ve blok_seri_ici.
# 12) v1.4 bolunme duzeltmesi: 10 Mart 2020 -%15 (marj %20) gercek; Haziran 2020 -%12 KAP kaydi yoksa gercek, bedelsiz kaydi varsa
#     bolunme; Haziran 2020 -%50 her zaman bolunme; 2024 -%12 (marj %10) bolunme.
# 13) v1.4 _fi_ilk: ayni barda hem +esik hem -esik -> asagi=1, yukari=0; hicbiri -> 0/0.
# 14) v1.4 esli taban: kat_dus_esli = sinyal orani / esli taban orani; _es_ satirlari iz tablosuna girmez.
import sys, numpy as np, pandas as pd

import FON_IZI as F


def sina():
    hata = []; A = F.FIAyar()
    idx = pd.bdate_range("2024-01-01", periods=10)
    c = np.array([100, 109, 110, 55, 56, 57, 58, 59, 60, 61], float)    # 3. gun %50 bedelsiz
    d = pd.DataFrame({"Open": c, "High": c, "Low": c, "Close": c, "Volume": 1000.0}, index=idx)
    z, k = F.fi_duzelt(d, A)
    if k != 1 or abs(z.Close.iat[3] / z.Close.iat[2] - 1.0) > 1e-9 or abs(z.Close.iat[1] / z.Close.iat[0] - 1.09) > 1e-9:
        hata.append(f"1) duzeltme yanlis: k={k} {z.Close.round(2).tolist()}")
    if abs(z.Volume.iat[0] - 2000.0) > 1e-6:
        hata.append(f"1) hacim ters carpan yok: {z.Volume.iat[0]}")
    n = 400; idx = pd.bdate_range("2023-01-02", periods=n)
    rng = np.random.default_rng(1); c = 100 * np.cumprod(1 + rng.normal(0, 0.02, n)); c[-60:] = c[-61] * np.cumprod(np.full(60, 1.006))
    d = pd.DataFrame({"Open": c, "High": c * 1.01, "Low": c * 0.99, "Close": c, "Volume": 1e5}, index=idx)
    Z = F.fi_pencere(d, A).iloc[-1]
    if not (Z.taban == 0 and Z.verim > 0.9 and Z.g > 0.3): hata.append(f"2) istikrarli yukselis olculeri yanlis: {Z.to_dict()}")
    d2 = d.copy(); d2.iloc[-10, d2.columns.get_loc("Close")] = d2.Close.iat[-11] * 0.89
    if F.fi_pencere(d2, A).iloc[-1].taban != 1: hata.append("2) taban gunu sayilmadi")
    idx = pd.bdate_range("2024-01-01", periods=300)
    y = pd.DataFrame({"Open": 100.0, "High": 100.0, "Low": 100.0, "Close": 100.0, "Volume": 1.0}, index=idx)
    y.iloc[5, y.columns.get_loc("High")] = 201.0
    if F._fi_sonuc(y, 0, A)["x2_once"] != 1.0: hata.append("3) once 2 kat isaretlenmedi")
    y.iloc[3, y.columns.get_loc("Low")] = 69.0
    if F._fi_sonuc(y, 0, A)["x2_once"] != 0.0: hata.append("3) once -%30 isaretlenmedi")
    idx = pd.bdate_range("2025-01-01", periods=200)
    c = np.r_[np.linspace(50, 10, 50), np.linspace(10, 100, 100), np.full(50, 500.0)]
    d = pd.DataFrame({"Open": c, "High": c, "Low": c, "Close": c, "Volume": 1.0}, index=idx)
    k = F.fi_kosu(d, F.FIAyar(kriz_tarih=str(idx[150].date())))
    if not (k["dip"] == idx[49] and k["tepe"] == idx[149] and abs(k["kat"] - 10) < 1e-6 and k["x2"] is not None and d.Close[k["x2"]] >= 20):
        hata.append(f"4) kosu yanlis: {k}")
    n = 400; idx = pd.bdate_range("2023-01-02", periods=n); rng6 = np.random.default_rng(2)
    r6 = rng6.normal(0, 0.02, n); r6[-20:] = np.where(np.arange(20) % 3 == 2, -0.003, 0.01)
    c = 100 * np.cumprod(1 + r6); hl = np.where(np.arange(n) >= n - 20, 0.006, 0.03)
    v = np.where(np.arange(n) >= n - 20, np.where(r6 > 0, 600.0, 200.0), 1000.0)
    d6 = pd.DataFrame({"Open": c, "High": c * (1 + hl / 2), "Low": c * (1 - hl / 2), "Close": c, "Volume": v}, index=idx)
    o6 = F.fi_hacim_olc(d6, A).iloc[-1]
    if not (o6.Z0 and o6.hk < 1 and o6.udvr > 1 and o6.dh < 1):
        hata.append(f"6) sessiz yuvarlanma / hacim olculeri yanlis: {o6.to_dict()}")
    g = {"FIAyar": object(), "__name__": "kapi_test"}
    try:
        src = open("FON_IZI.py", encoding="utf-8").read()
        g["_CK_KAYIT"] = {"FIAyar": "BASKA.py"}
        exec(compile(src.replace("from __future__ import annotations\n", ""), "FON_IZI.py", "exec"), g)
        hata.append("5) cakisma kapisi baska dosyanin adini ezince durmadi")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex): hata.append(f"5) beklenmeyen hata: {ex}")
    except Exception as ex:
        hata.append(f"5) kapi sinamasi calismadi: {type(ex).__name__} {ex}")
    rng7 = np.random.default_rng(7); n7 = 700; idx7 = pd.bdate_range("2020-01-01", periods=n7)
    c7 = 50 * np.cumprod(1 + rng7.normal(0, 0.025, n7)); o7 = c7 * (1 + rng7.normal(0, 0.005, n7))
    d7 = pd.DataFrame({"Open": o7, "High": np.maximum(o7, c7) * (1 + rng7.uniform(0, 0.02, n7)),
                       "Low": np.minimum(o7, c7) * (1 - rng7.uniform(0, 0.02, n7)), "Close": c7,
                       "Volume": rng7.uniform(1e5, 1e6, n7)}, index=idx7)
    try:
        Gt = F.fi_gostergeler(d7, A); Gk = F.fi_gostergeler(d7.iloc[:500], A)
        St = pd.DataFrame(F.fi_gosterge_sinyal(Gt, A)).iloc[:500]; Sk = pd.DataFrame(F.fi_gosterge_sinyal(Gk, A))
        fark = [c for c in Gk.columns if not np.allclose(Gt[c].iloc[:500].to_numpy(float), Gk[c].to_numpy(float), equal_nan=True, rtol=1e-9, atol=1e-12)]
        fark += [c for c in Sk.columns if not (St[c].to_numpy() == Sk[c].to_numpy()).all()]
        if fark:
            hata.append(f"7) gelecek degisince gecmis degisti: {fark}")
        if sum(int(St[c].sum()) for c in St.columns if c.startswith("uy_")) == 0:
            hata.append("7) rastgele seride hic uyumsuzluk yok (sinama bos)")
    except Exception as ex:
        hata.append(f"7) gosterge hesaplanamadi: {type(ex).__name__} {ex}")
    cc, hh, ll = d7.Close.to_numpy(), d7.High.to_numpy(), d7.Low.to_numpy()
    u8, _ = F._fi_ilk(cc, hh, ll, 60, 0.20, 0.10)
    dongu = np.array([F._fi_once(d7, i, 60, 0.20, 0.10) for i in range(n7 - 60)])
    if not np.array_equal(u8[:n7 - 60], dongu) or not np.isnan(u8[n7 - 60:]).all():
        hata.append("8) vektorlu sonuc dongu ile ayni degil")
    f9 = np.r_[np.linspace(10, 5, 21), np.linspace(5.1, 9, 20), np.linspace(8.8, 4, 20), np.linspace(4.2, 10, 20)]
    g9 = np.full(len(f9), 50.0); g9[20] = 20.0; g9[60] = 30.0
    duz9, gizli9 = F._fi_uyumsuzluk(f9, g9, 5, 60, True)
    if not (duz9[65] and duz9.sum() == 1 and not gizli9.any()):
        hata.append(f"9) uyumsuzluk yanlis: duz {np.flatnonzero(duz9)} gizli {np.flatnonzero(gizli9)}")
    idx10 = pd.bdate_range("2026-05-04", periods=15)
    olay = {"kap_vbts_tedbir": pd.DataFrame({"tarih": pd.to_datetime(["2026-05-05", "2026-05-06", "2026-05-09"]),
                                              "saat": ["10:00", "18:30", "12:00"]})}
    k10 = F.fi_kap_sinyal(idx10, olay)["kap_vbts_tedbir"]
    if list(k10[k10].index.strftime("%m-%d")) != ["05-05", "05-07", "05-11"]:
        hata.append(f"10) KAP esleme yanlis: {list(k10[k10].index.strftime('%m-%d'))}")
    c11 = np.r_[np.full(30, 100.0), 100 * 1.1 ** np.arange(1, 5)]; v11 = np.r_[np.full(30, 1000.0), 100.0, 100.0, 100.0, 50000.0]
    d11 = pd.DataFrame({"Open": c11, "High": c11, "Low": c11, "Close": c11, "Volume": v11}, index=pd.bdate_range("2026-01-01", periods=len(c11)))
    d11.iloc[:30, d11.columns.get_loc("High")] = 101.0; d11.iloc[:30, d11.columns.get_loc("Low")] = 99.0
    S11 = F.fi_gosterge_sinyal(F.fi_gostergeler(d11, A), A)
    if not (S11["blok_tavan"].iat[-1] and S11["blok_seri_ici"].iat[-1] and S11["blok_hacim"].sum() == 1):
        hata.append("11) blok hacim / seri ici yakalanmadi")
    def _seri(tarihler_r):
        idx = pd.bdate_range("2019-12-02", "2024-12-31"); c = np.full(len(idx), 100.0)
        for t, r in tarihler_r:
            j = idx.get_loc(pd.Timestamp(t)); c[j:] = c[j:] * (1 + r)
        return pd.DataFrame({"Open": c, "High": c, "Low": c, "Close": c, "Volume": 1000.0}, index=idx)
    olay = [("2020-03-10", -0.15), ("2020-06-15", -0.12), ("2020-09-15", -0.50), ("2024-04-15", -0.12)]
    d12 = _seri(olay)
    z0, k0 = F.fi_duzelt(d12, A)
    z1, k1 = F.fi_duzelt(d12, A, pd.DatetimeIndex(["2020-05-01"]))
    def _r(z, t):
        return z.Close.loc[pd.Timestamp(t)] / z.Close.shift().loc[pd.Timestamp(t)] - 1
    if not (k0 == 2 and abs(_r(z0, "2020-03-10") + 0.15) < 1e-9 and abs(_r(z0, "2020-06-15") + 0.12) < 1e-9
            and abs(_r(z0, "2020-09-15")) < 1e-9 and abs(_r(z0, "2024-04-15")) < 1e-9):
        hata.append(f"12) KAP kaydi yokken duzeltme yanlis: k={k0}")
    if not (k1 == 3 and abs(_r(z1, "2020-06-15")) < 1e-9 and abs(_r(z1, "2020-03-10") + 0.15) < 1e-9):
        hata.append(f"12) KAP bedelsiz kaydiyla duzeltme yanlis: k={k1}")
    c13 = np.full(6, 100.0); h13 = c13.copy(); l13 = c13.copy(); h13[2] = 125; l13[2] = 75
    u13, a13 = F._fi_ilk(c13, h13, l13, 3, 0.20, 0.20)
    if not (u13[0] == 0 and a13[0] == 1 and u13[2] == 0 and a13[2] == 0):
        hata.append(f"13) ayni bar kurali yanlis: u={u13[:3]} a={a13[:3]}")
    E14 = pd.DataFrame([{"pazar": "BIST", "sinyal": s_, "donem": "2016-21", "n": 100, "n_k20": 100, "k20": 40, "n_x2": 100, "x2": 30,
                         "n_dus": 100, "dus": d_} for s_, d_ in (("_TABAN", 20), ("blok_taban", 40), ("_es_taban_bloksuz", 38))])
    S14, iz14 = F.fi_k6_ozet(E14)
    r14 = S14[S14.sinyal == "blok_taban"]
    if not (len(r14) == 1 and abs(r14.kat_dus.iat[0] - 2.0) < 1e-9 and abs(r14.kat_dus_esli.iat[0] - 40 / 38) < 1e-9
            and not S14.sinyal.str.startswith("_es_").any()):
        hata.append("14) esli taban kati yanlis")
    return hata


if __name__ == "__main__":
    h = sina()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_fon_izi: 14/14 OK")
