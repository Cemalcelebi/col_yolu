# test_mum_sukun.py — MUM_SUKUN mekanik sinama (2026-10-22)
# Calistir: python3 test_mum_sukun.py   (repo kokunde; veri indirilmez, sentetik seri)
# 1) Sakin bitis: son 3 mum hissenin kendi gecmisinin en kucugu -> yuzdelik <= 5, oran < 0,5.
# 2) Oynak bitis: son 3 mum gecmisin en buyugu -> yuzdelik >= 95.
# 3) Hisseye ozel: ayni mutlak mum boyu, sakin hissede yuksek, oynak hissede dusuk yuzdelik verir.
# 4) Olay: dusus + sakin 3 mum -> p02 varyantinda o gun olay bulunur (p05 daha once tetiklenmis olabilir: 20 bar tekrar kurali), taban varyantinda o gun olay yok.
# 5) Sonuc: once +%20 mi -%10 mu dogru isaretlenir.
# 6) Cakisma kapisi: modul bellekteki baska bir adi ezerse durur.
# 7) v1.1 gecerli mum: islem gormeyen (hacim 0) ya da kilitli (O=H=L=C) son mumlar sakin sayilmaz, olcu verilmez.
# 9) v1.3 kisa ufuk: once +%3 / -%3 dogru isaretlenir; ayrilma: duz bolge 12 bar surer, sonra yukari kopar -> yon +1, bolge_bar
#    dogru, sertlik > 0; hacim bolgede iki kat -> hacim_kat ~2.
# 8) v1.2 zemin: sert dusus + dipleri hizali, bosluksuz 5 mum -> z_siki; ayni dusus + daginik sira -> taban; dipleri kayan sira zemin degil.
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
    kilit = seri(dusus=True); kilit["Volume"] = 1000.0
    for j in (1, 2, 3):
        pc = kilit.Close.iat[-j - 1]; kilit.iloc[-j, :4] = [pc, pc, pc, pc]
    r = M.ms_yuzdelik(kilit, 3, "govde", A)
    if np.isfinite(r["yuzdelik"]): hata.append(f"7) kilitli mumlar olculdu: {r}")
    sifir = seri(dusus=True, son=[0.0005, 0.0005, 0.0005]); sifir["Volume"] = 1000.0; sifir.iloc[-1, sifir.columns.get_loc("Volume")] = 0.0
    O7 = M.ms_k2_olaylar({"T7": sifir}, "ABD", A)
    if not O7[(O7.tarih == sifir.index[-1])].empty: hata.append("7) hacmi 0 olan gun sinyal verdi")
    def zemin_seri(son):
        z = seri(n=420, oynak=0.02, tohum=7)
        z.iloc[-25:] = z.iloc[-26].Close  # duz bekleme
        c0 = z.Close.iat[-26]
        for j, i in enumerate(range(len(z) - 13, len(z) - 5)):  # 8 gunde sert dusus, buyuk mumlar
            pc = z.Close.iat[i - 1]; cc = pc * 0.95
            z.iloc[i] = [pc, pc * 1.01, cc * 0.98, cc]
        for j, (o, h, l, c) in enumerate(son):
            i = len(z) - 5 + j; b = z.Close.iat[len(z) - 6]
            z.iloc[i] = [b * o, b * h, b * l, b * c]
        z.iloc[-25:-13] = [[c0 * 1.0, c0 * 1.01, c0 * 0.99, c0]] * 12
        return z
    duz = [(1.0, 1.006, 0.995, 1.002), (1.002, 1.007, 0.995, 1.0), (1.0, 1.005, 0.996, 1.003), (1.003, 1.006, 0.995, 1.001), (1.001, 1.006, 0.996, 1.002)]
    Zd = M.ms_zemin_olcu(zemin_seri(duz), 5, A).iloc[-1]
    if not (Zd.baglam and Zd.z_siki and not Zd.taban): hata.append(f"8) duz zemin z_siki degil: {Zd.to_dict()}")
    dag = [(1.0, 1.05, 0.97, 1.04), (1.04, 1.06, 0.98, 0.99), (0.95, 1.0, 0.94, 0.99), (1.0, 1.08, 0.99, 1.06), (1.02, 1.05, 0.96, 0.97)]
    Zg = M.ms_zemin_olcu(zemin_seri(dag), 5, A).iloc[-1]
    if not (Zg.baglam and Zg.taban and not Zg.z_gevsek): hata.append(f"8) daginik sira taban degil: {Zg.to_dict()}")
    kay = [(1.0, 1.004, 0.992, 0.994), (0.994, 0.998, 0.984, 0.986), (0.986, 0.99, 0.976, 0.978), (0.978, 0.982, 0.968, 0.97), (0.97, 0.974, 0.96, 0.962)]
    Zk = M.ms_zemin_olcu(zemin_seri(kay), 5, A).iloc[-1]
    if Zk.z_siki: hata.append(f"8) dipleri kayan sira zemin sayildi: {Zk.to_dict()}")
    idx9 = pd.bdate_range("2024-01-01", periods=12)
    y9 = pd.DataFrame({"Open": 100.0, "High": [100, 101, 104, 100] + [100] * 8, "Low": [100, 99, 99, 90] + [100] * 8, "Close": 100.0}, index=idx9)
    if M._sonuc_kisa(y9, 0, 0.02, A)["once_3_3"] != 1.0: hata.append("9) kisa: once +%3 isaretlenmedi")
    y9b = y9.copy(); y9b.loc[idx9[1], "Low"] = 96
    if M._sonuc_kisa(y9b, 0, 0.02, A)["once_3_3"] != 0.0: hata.append("9) kisa: once -%3 isaretlenmedi")
    n9 = 100; i9 = 60; idx = pd.bdate_range("2024-01-01", periods=n9)
    c9 = np.full(n9, 100.0); h9 = c9 * 1.02; l9 = c9 * 0.98; v9 = np.full(n9, 1000.0)
    h9[i9 - 4:i9 + 8] = 100.5; l9[i9 - 4:i9 + 8] = 99.5; v9[i9 - 4:i9 + 8] = 2000.0   # 5 mumluk sira + 7 bar daha bolgede
    h9[i9 + 8:] = 108.0; c9[i9 + 8:] = 107.0; l9[i9 + 8:] = 106.0                     # yukari kopus
    a9 = M._ayrilma(pd.DataFrame({"Open": c9, "High": h9, "Low": l9, "Close": c9, "Volume": v9}, index=idx), i9, 5, 0.01, A)
    if not (a9["yon"] == 1.0 and a9["bolge_bar"] == 12 and a9["sertlik"] > 0 and abs(a9["hacim_kat"] - 2.0) < 0.01):
        hata.append(f"9) ayrilma yanlis: {a9}")
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
    print("test_mum_sukun: 9/9 OK")
