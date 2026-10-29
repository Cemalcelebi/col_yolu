# test_col_yolu_abd.py — COL_YOLU_ABD.py mekanik denetimleri (sentetik veri; gerçek veri gerekmez)
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import COL_YOLU_ABD as C  # noqa: E402


def _seri(c, o=None, h=None, l=None, v=None, bas="2018-01-01"):
    c = np.asarray(c, float); n = len(c)
    o = c.copy() if o is None else np.asarray(o, float); h = np.maximum(o, c) * 1.002 if h is None else np.asarray(h, float)
    l = np.minimum(o, c) * 0.998 if l is None else np.asarray(l, float); v = np.full(n, 1e6) if v is None else np.asarray(v, float)
    return pd.DataFrame({"Open": o, "High": h, "Low": l, "Close": c, "Volume": v}, index=pd.bdate_range(bas, periods=n))


def sina():
    hata = []
    # 1) üçlü bariyer: +%20 önce -> 1 / 0,20; -%10 önce -> 0 / -0,10; aynı gün ikisi -> 0; boşlukla açılış -> açılış fiyatı; vade -> kapanış
    n = 120; c = np.full(n, 100.0); d = _seri(c, h=np.full(n, 101.0), l=np.full(n, 99.0))
    d1 = d.copy(); d1.iloc[13, d1.columns.get_loc("High")] = 121.0
    d2 = d.copy(); d2.iloc[12, d2.columns.get_loc("Low")] = 89.0
    d3 = d.copy(); d3.iloc[12, d3.columns.get_loc("Low")] = 89.0; d3.iloc[12, d3.columns.get_loc("High")] = 121.0
    d4 = d.copy(); d4.iloc[14, d4.columns.get_loc("Open")] = 125.0; d4.iloc[14, d4.columns.get_loc("High")] = 126.0
    d5 = d.copy(); d5.iloc[70, d5.columns.get_loc("Close")] = 104.0
    t1, t2, t3, t4, t5 = (C.cy_uclu_bariyer(x, 0.20, -0.10, 60, False) for x in (d1, d2, d3, d4, d5))
    ok = (t1.y.iloc[10] == 1 and abs(t1.brut.iloc[10] - 0.20) < 1e-12 and t1.cikis.iloc[10] == 13 and t2.y.iloc[10] == 0
          and abs(t2.brut.iloc[10] + 0.10) < 1e-12 and t3.y.iloc[10] == 0 and abs(t4.brut.iloc[10] - 0.25) < 1e-12 and t4.y.iloc[10] == 1
          and abs(t5.brut.iloc[10] - 0.04) < 1e-12 and t5.cikis.iloc[10] == 70 and np.isnan(t5.y.iloc[n - 5]))
    if not ok:
        hata.append("1) üçlü bariyer temel durumlar yanlış")
    # 2) borsadan çıkış: seri vadeden önce biter, son 60 gün eksi -> son kapanış x 0,7; çıkmayan seride aynı satır NaN
    c6 = np.r_[np.full(100, 100.0), np.linspace(100, 50, 30)]; d6 = _seri(c6, h=c6 * 1.001, l=c6 * 0.999)
    t6 = C.cy_uclu_bariyer(d6, 0.20, -0.60, 60, True); t6b = C.cy_uclu_bariyer(d6, 0.20, -0.60, 60, False)
    i = 100; o = d6.Open.iloc[i + 1]; bek = (50.0 / o) * 0.7 - 1
    if not (abs(t6.brut.iloc[i] - bek) < 1e-9 and t6.y.iloc[i] == 0 and np.isnan(t6b.y.iloc[i])):
        hata.append(f"2) borsadan çıkış getirisi yanlış: {t6.brut.iloc[i]} {bek}")
    # 3) sızıntı yok: son 60 bar kesilince önceki ölçüler aynı
    r = np.random.default_rng(3); c7 = 50 * np.exp(np.cumsum(r.normal(0, 0.02, 700))); o7 = c7 * (1 + r.normal(0, 0.004, 700))
    d7 = _seri(c7, o=o7, h=np.maximum(o7, c7) * (1 + r.uniform(0, 0.02, 700)), l=np.minimum(o7, c7) * (1 - r.uniform(0, 0.02, 700)), v=r.uniform(5e5, 2e6, 700))
    M = C.cy_olculer(d7); Mk = C.cy_olculer(d7.iloc[:-60])
    a = M["F"].iloc[:-60].to_numpy(float); b = Mk["F"].to_numpy(float); m = ~(np.isnan(a) & np.isnan(b))
    a2 = M["col"][60].iloc[:-60].to_numpy(float); b2 = Mk["col"][60].to_numpy(float); m2 = ~(np.isnan(a2) & np.isnan(b2))
    if not (np.allclose(np.nan_to_num(a[m]), np.nan_to_num(b[m]), rtol=1e-6, atol=1e-9) and np.allclose(np.nan_to_num(a2[m2]), np.nan_to_num(b2[m2]), rtol=1e-6, atol=1e-9)):
        hata.append("3) ölçüler geleceğe bakıyor")
    im = C.cy_resim(d7, 500); imk = C.cy_resim(d7.iloc[:501], 500)
    if not (im.shape == (64, 180) and set(np.unique(im)) <= {0, 255} and np.array_equal(im, imk)):
        hata.append("3b) resim biçimi / sızıntı yanlış")
    # 4) sentetik çöl: 300 bar dalgalı yükseliş, 60 barda %55 düşüş, 120 bar küçük mumlu, düşük hacimli, dar bant -> P1 var; düşüşsüz seride P1 yok
    r = np.random.default_rng(4)
    up = 100 * np.exp(np.cumsum(r.normal(0.001, 0.025, 300))); dn = np.linspace(up[-1], up[-1] * 0.45, 60) * np.exp(r.normal(0, 0.01, 60))
    tab = up[-1] * 0.45 * (1 + r.normal(0, 0.004, 160)); c8 = np.r_[up, dn, tab]; o8 = np.r_[c8[0], c8[:-1]] * (1 + r.normal(0, 0.002, len(c8)))
    gen = np.r_[np.full(360, 0.03), np.full(160, 0.006)]
    h8 = np.maximum(o8, c8) * (1 + gen * r.uniform(0.3, 1, len(c8))); l8 = np.minimum(o8, c8) * (1 - gen * r.uniform(0.3, 1, len(c8)))
    o8[360:] = c8[360:] * (1 + r.normal(0, 0.0003, 160))             # gövdesiz (doji) mumlar
    v8 = np.r_[np.full(360, 2e6), np.full(160, 5e5)]
    d8 = _seri(c8, o=o8, h=h8, l=l8, v=v8); M8 = C.cy_olculer(d8); S8 = C.cy_sinyaller(d8, M8, np.ones(len(d8), bool))
    c9 = 100 * np.exp(np.cumsum(r.normal(0.0008, 0.01, 520))); d9 = _seri(c9, v=np.full(520, 1e6)); S9 = C.cy_sinyaller(d9, C.cy_olculer(d9), np.ones(520, bool))
    if not (len(S8["P1"]) >= 1 and all(i >= 360 for i in S8["P1"]) and len(S9["P1"]) == 0):
        hata.append(f"4) sentetik çöl tespiti yanlış: {S8['P1'][:5]} / {S9['P1'][:5]}")
    # 5) PBO: tek baskın yapı -> ~0; saf gürültü -> 0,2-0,8
    r = np.random.default_rng(5); Mn = r.normal(0, 1, (96, 12)); Md = Mn.copy(); Md[:, 3] += 2.0
    p0 = C.cy_pbo(Md, 8)["pbo"]; p1 = C.cy_pbo(Mn, 8)["pbo"]
    if not (p0 < 0.05 and 0.2 < p1 < 0.8):
        hata.append(f"5) PBO yanlış: baskın {p0}, gürültü {p1}")
    # 6) DSR: yüksek Sharpe -> daha yüksek DSR
    sr = r.normal(0, 0.1, 36); lo = C.cy_dsr(r.normal(0.001, 0.05, 80), sr)["dsr"]; hi = C.cy_dsr(r.normal(0.03, 0.05, 80), sr)["dsr"]
    if not (hi > lo and 0 <= lo <= 1):
        hata.append(f"6) DSR yanlış: {lo} {hi}")
    # 7) portföy: tek işlem, +%20 hedef -> toplam ~ 0,1 x 0,2 eksi maliyet
    T1 = C.cy_uclu_bariyer(d1, 0.20, -0.10, 60, False)
    H = {"X": {"tarih": d1.index.to_numpy(), "kapanis": d1.Close.to_numpy(np.float32), "acilis": d1.Open.to_numpy(np.float32),
               "kayma": np.full(len(d1), 0.0, np.float32), "T": T1[["brut", "cikis"]].to_numpy(np.float64)}}
    po = C.cy_portfoy(H, [(d1.index[10], "X", 10)], str(d1.index[0].date()), str(d1.index[-1].date()), "ABD", C.CY, None, d1.index)
    bek = 0.1 * ((1 + 0.20) * (1 - 0.0005) / (1 + 0.0005) - 1)
    if not (po["islem_n"] == 1 and abs(po["toplam"] - bek) < 2e-4):
        hata.append(f"7) portföy hesabı yanlış: {po['toplam']} {bek}")
    # 8) çakışma kapısı: başka dosyanın tanımladığı adı ezerse durur
    kod = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "COL_YOLU_ABD.py"), encoding="utf-8").read()
    g = {"__name__": "__main__", "get_ipython": None, "CY": {"baska": 1}, "_CK_KAYIT": {"CY": "BASKA.py"}}
    try:
        exec(compile(kod, "COL_YOLU_ABD.py", "exec"), g); hata.append("8) çakışma kapısı çalışmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"8) çakışma kapısı yanlış hata: {ex}")
    g2 = {"__name__": "__main__", "get_ipython": None}
    try:
        exec(compile(kod, "COL_YOLU_ABD.py", "exec"), g2); exec(compile(kod, "COL_YOLU_ABD.py", "exec"), g2)
    except RuntimeError as ex:
        hata.append(f"8b) aynı dosyanın yeniden yüklenmesi durdu: {ex}")
    return hata


if __name__ == "__main__":
    h = sina()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_col_yolu_abd: 8/8 OK")
