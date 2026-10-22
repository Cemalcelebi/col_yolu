# test_mum_sukun.py — MUM_SUKUN mekanik sinama (2026-10-22)
# Calistir: python3 test_mum_sukun.py   (repo kokunde; veri indirilmez, sentetik seri)
# 1) Sakin bitis: son 3 mum hissenin kendi gecmisinin en kucugu -> yuzdelik <= 5, oran < 0,5.
# 2) Oynak bitis: son 3 mum gecmisin en buyugu -> yuzdelik >= 95.
# 3) Hisseye ozel: ayni mutlak mum boyu, sakin hissede yuksek, oynak hissede dusuk yuzdelik verir.
# 4) Olay: dusus + sakin 3 mum -> p02 varyantinda o gun olay bulunur (p05 daha once tetiklenmis olabilir: 20 bar tekrar kurali), taban varyantinda o gun olay yok.
# 5) Sonuc: once +%20 mi -%10 mu dogru isaretlenir.
# 6) Cakisma kapisi: modul bellekteki baska bir adi ezerse durur.
import sys, numpy as np, pandas as pd

import MUM_SUKUN as M


def seri(n=420, oynak=0.03, son=None, dusus=False, tohum=3):
    rng = np.random.default_rng(tohum)
    idx = pd.bdate_range("2023-01-02", periods=n)
    c = np.empty(n); c[0] = 100.0
    for i in range(1, n):
        c[i] = c[i - 1] * (1 + rng.normal(0, oynak))
    if dusus:
        for i in range(n - 40, n - 3):
            c[i] = c[i - 1] * 0.985
    o = np.r_[c[0], c[:-1]] * (1 + rng.normal(0, oynak / 3, n))
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, oynak / 2, n)))
    l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, oynak / 2, n)))
    d = pd.DataFrame({"Open": o, "High": h, "Low": l, "Close": c}, index=idx)
    if son is not None:
        for j, g in enumerate(son):
            i = n - len(son) + j
            pc = d.Close.iat[i - 1]
            d.iloc[i] = [pc, pc * (1 + g), pc * (1 - g / 2), pc * (1 + g / 2)]
    return d


def sina():
    hata = []
    A = M.MSAyar()
    sakin = seri(son=[0.001, 0.001, 0.001])
    r = M.ms_yuzdelik(sakin, 3, "govde", A)
    if not (r["yuzdelik"] <= 5 and r["oran"] < 0.5): hata.append(f"1) sakin bitis yuzdelik {r}")
    oyn = seri(son=[0.15, 0.15, 0.15])
    r = M.ms_yuzdelik(oyn, 3, "govde", A)
    if not r["yuzdelik"] >= 95: hata.append(f"2) oynak bitis yuzdelik {r}")
    ayni = [0.008, 0.008, 0.008]
    r_sakin = M.ms_yuzdelik(seri(oynak=0.005, son=ayni), 3, "govde", A)["yuzdelik"]
    r_oynak = M.ms_yuzdelik(seri(oynak=0.04, son=ayni), 3, "govde", A)["yuzdelik"]
    if not r_sakin > r_oynak: hata.append(f"3) hisseye ozel degil: sakin hisse {r_sakin}, oynak hisse {r_oynak}")
    d = seri(dusus=True, son=[0.0005, 0.0005, 0.0005])
    O = M.ms_k2_olaylar({"TEST": d}, "ABD", A)
    son_gun = d.index[-1]
    sig = O[(O.tarih == son_gun) & (O.k == 3) & (O.olcu == "govde")]
    if "p02" not in set(sig.varyant): hata.append(f"4) sakin dusus sonu p02 olayi yok: {sorted(sig.varyant)}")
    if "taban" in set(sig.varyant): hata.append("4) taban varyanti sakin gunu da sayiyor")
    idx = pd.bdate_range("2024-01-01", periods=10)
    yol = pd.DataFrame({"Open": 100.0, "High": [100, 101, 125, 100, 100, 100, 100, 100, 100, 100],
                        "Low": [100, 99, 99, 85, 100, 100, 100, 100, 100, 100], "Close": 100.0}, index=idx)
    if M._sonuc(yol, 0, A)["once_yukari"] != 1.0: hata.append("5) once +%20 isaretlenmedi")
    yol2 = yol.copy(); yol2.loc[idx[1], "Low"] = 85
    if M._sonuc(yol2, 0, A)["once_yukari"] != 0.0: hata.append("5) once -%10 isaretlenmedi")
    g = {"MSAyar": object(), "__name__": "kapi_test"}
    try:
        src = open("MUM_SUKUN.py", encoding="utf-8").read()
        g["_CK_KAYIT"] = {"MSAyar": "BASKA.py"}
        exec(compile(src.replace("from __future__ import annotations\n", ""), "MUM_SUKUN.py", "exec"), g)
        hata.append("6) cakisma kapisi baska dosyanin adini ezince durmadi")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex): hata.append(f"6) beklenmeyen hata: {ex}")
    except Exception as ex:
        hata.append(f"6) kapi sinamasi calismadi: {type(ex).__name__} {ex}")
    return hata


if __name__ == "__main__":
    h = sina()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_mum_sukun: 6/6 OK")
