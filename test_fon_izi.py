# test_fon_izi.py — FON_IZI mekanik sinama (2026-10-22)
# Calistir: python3 test_fon_izi.py   (repo kokunde; veri indirilmez, sentetik seri)
# 1) Bolunme duzeltme: %50 bedelsiz sicramasi (2020 sonrasi, sinir %10) duzeltilir, gercek %9 tavan gunu dokunulmaz; hacim ters carpan.
# 2) Pencere olculeri: tabansiz istikrarli yukseliste taban=0, verim yuksek; bir -%10 gun eklenince taban=1.
# 3) Sonuc: once 2 kat / once -%30 dogru isaretlenir.
# 4) Kosu: dip, ilk 2 kat ve tepe dogru bulunur; kriz tarihinden sonraki tepe sayilmaz.
# 5) Cakisma kapisi: modul bellekteki baska bir adi ezerse durur.
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
    return hata


if __name__ == "__main__":
    h = sina()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_fon_izi: 5/5 OK")
