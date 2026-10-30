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
    # 9) v1.1: aynı gün hem hedef hem stop -> belirsiz = 1 (etiket 0); gün başına dizi bariyer: 10. gün için üst +%5 -> 13. gün 121 değil 106 yeter
    if not (t3.belirsiz.iloc[10] == 1 and t1.belirsiz.iloc[10] == 0):
        hata.append("9) belirsiz işareti yanlış")
    d9b = d.copy(); d9b.iloc[13, d9b.columns.get_loc("High")] = 106.0; ust = np.full(n, 0.20); ust[10] = 0.05
    t9 = C.cy_uclu_bariyer(d9b, ust, -0.10, 60, False)
    if not (t9.y.iloc[10] == 1 and abs(t9.brut.iloc[10] - 0.05) < 1e-12 and t9.y.iloc[11] == 0):
        hata.append(f"9b) dizi bariyer yanlış: {t9.y.iloc[10]} {t9.brut.iloc[10]}")
    # 10) v1.1 özellikleri geleceğe bakmıyor
    yeni = ["kapanis_yer", "kir_hacim", "tepe_bar250", "dus_sure", "dus_atr", "cmf20", "obv_egim20", "ad_egim20", "mfi14", "macd_hist"]
    a3 = M["F"][yeni].iloc[:-60].to_numpy(float); b3 = Mk["F"][yeni].to_numpy(float); m3 = ~(np.isnan(a3) & np.isnan(b3))
    if not np.allclose(np.nan_to_num(a3[m3]), np.nan_to_num(b3[m3]), rtol=1e-6, atol=1e-9):
        hata.append("10) v1.1 özellikleri geleceğe bakıyor")
    # 11) olay CSV'si dört kümeyi (P1, P2, ES, HT) eksiksiz yazar ve geri okuyup doğrular
    import tempfile
    E11 = pd.DataFrame({"tip": ["P1", "P2", "ES", "HT", "HT", "P1|-0.35|60|0.8|3"], "i": range(6), "sembol": "X", "vd": 1,
                        "tarih": pd.bdate_range("2024-01-01", periods=6)})
    with tempfile.TemporaryDirectory() as td:
        say = C.cy_olay_yaz(E11, td, "ABD")
        geri = pd.read_csv(os.path.join(td, "cy_olay_ABD.csv.gz"))
    if not (say == {"P1": 1, "P2": 1, "ES": 1, "HT": 2} and (geri.tip == "HT").sum() == 2 and "vd" not in geri):
        hata.append(f"11) olay CSV'sinde HT / küme eksik: {say}")
    # 12) v1.2 eşleştirme: yalnız aynı gün (gun_tol 0), aynı vd / lt / trend, |dd250| <= 0,10, hisse farklı; gelecek günün etiketi eşleşmeyi değiştirmez; aynı tohumla aynı sonuç
    K12 = {**C.CY, "_v12": C.CY_V12}; g12 = pd.bdate_range("2024-01-01", periods=3)
    def satir(sem, t, dd, y, vd=3, lt=1, tr=1, sk="Tech"):
        return {"sembol": sem, "tarih": t, "dd250": dd, "vol60": 0.02, "log_dv20": 7.0, "r60": 0.0, "ar20": 1.0, "vd": vd, "lt": lt, "trend": tr, "sektor": sk, "y": y, "net": y - 0.01, "imza_h": 1}
    P12 = pd.DataFrame([satir("E", g12[0], -0.40, 1.0), satir("A", g12[0], -0.38, 0.0), satir("B", g12[0], -0.42, 1.0), satir("C", g12[0], -0.60, 1.0), satir("D", g12[0], -0.40, 1.0, vd=5),
                        satir("F", g12[0], -0.40, 1.0, tr=0), satir("G", g12[1], -0.40, 1.0), satir("H", g12[0], -0.40, 1.0, sk="Energy")])
    ol = P12.iloc[[0]]; hv = P12.iloc[1:]; rng12 = np.random.default_rng(5)
    M12 = C.cy_v12_eslestir(P12, ol, hv, K12, 5, 0, rng12); kim = set(M12.kontrol_kimlik.iloc[0].split("@")[0].split(";"))
    P12b = P12.copy(); P12b.loc[P12b.sembol == "G", "y"] = 0.0; M12b = C.cy_v12_eslestir(P12b, ol, P12b.iloc[1:], K12, 5, 0, rng12)
    semler = [x.split("@")[0] for x in M12.kontrol_kimlik.iloc[0].split(";")]
    if not (sorted(semler) == ["A", "B"] and abs(M12.kontrol_y.iloc[0] - 0.5) < 1e-9 and M12.kontrol_kimlik.iloc[0] == M12b.kontrol_kimlik.iloc[0] and M12.kontrol_n.iloc[0] == 2):
        hata.append(f"12) v1.2 eşleştirme yanlış: {semler} {M12.kontrol_y.iloc[0]}")
    # 13) sembol tekilliği
    try:
        C.cy_v12_tekil(pd.DataFrame({"pazar": ["ABD", "ABD"], "sembol": ["X", "X"]})); hata.append("13) yinelenen sembol yakalanmadı")
    except RuntimeError:
        pass
    # 14) delist senaryoları: seri 100 -> 50'de biter (vade dolmadan), son 60 gün eksi: ek kayıp -30 / 0 / -100 beklenen brüt getiriyi verir
    c14 = np.r_[np.full(100, 100.0), np.linspace(100, 50, 30)]; d14 = _seri(c14, h=c14 * 1.001, l=c14 * 0.999); o14 = d14.Open.iloc[101]
    bek = {-0.30: (50 / o14) * 0.7 - 1, 0.0: 50 / o14 - 1, -1.0: -1.0}; ok14 = True
    for sn, b_ in bek.items():
        t14 = C.cy_uclu_bariyer(d14, 0.20, -0.60, 60, True, {**C.CY, "delist_kayip": sn}); ok14 &= abs(t14.brut.iloc[100] - b_) < 1e-9 and t14.y.iloc[100] == 0
    if not ok14:
        hata.append("14) delist senaryoları yanlış")
    # 15) ham / düzeltilmiş: orantılı ölçekli seri aynı etiketleri verir (bariyerler göreli)
    t15a = C.cy_uclu_bariyer(d7, 0.20, -0.10, 60, False); t15b = C.cy_uclu_bariyer(d7.assign(**{k: d7[k] * 3.0 for k in ("Open", "High", "Low", "Close")}), 0.20, -0.10, 60, False)
    if not (np.array_equal(np.nan_to_num(t15a.y, nan=-1), np.nan_to_num(t15b.y, nan=-1)) and np.allclose(np.nan_to_num(t15a.brut), np.nan_to_num(t15b.brut))):
        hata.append("15) ölçekli seride etiket değişti")
    # 16) hücre hesabı: fark = ağırlıklı ortalama (y - kontrol_y); net fark aynı; maliyet = brüt - net
    D16 = pd.DataFrame({"tarih": pd.bdate_range("2023-01-02", periods=40, freq="3B"), "sembol": [f"S{i % 7}" for i in range(40)], "y": [1.0, 0.0] * 20, "kontrol_y": 0.25,
                        "net": 0.02, "kontrol_net": 0.01, "brut": 0.03, "agirlik": 1.0})
    h16 = C.cy_v12_hucre(D16, K12, np.random.default_rng(1))
    if not (abs(h16["fark"] - 0.25) < 1e-9 and abs(h16["net_fark"] - 0.01) < 1e-9 and h16["n"] == 40 and C.cy_v12_karar(h16, K12) == "TUTAR"):
        hata.append(f"16) v1.2 hücre hesabı yanlış: {h16.get('fark')} {h16.get('net_fark')}")
    # 17) eski kod yüklenebilir (git show b3835d8) ve aynı imzalı işleyici var
    import subprocess
    r17 = subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(__file__)), "show", f"{C.CY_V12['eski_commit']}:COL_YOLU_ABD.py"], capture_output=True, text=True)
    if r17.returncode == 0:
        import types
        m17 = types.ModuleType("cy_eski_test"); sys.modules["cy_eski_test"] = m17; m17.__dict__.update({"get_ipython": None, "__file__": __file__})
        try:
            exec(compile(r17.stdout, "eski.py", "exec"), m17.__dict__)
            if not (callable(m17.__dict__.get("cy_hisse_isle")) and callable(m17.__dict__.get("cy_birlestir"))):
                hata.append("17) eski kodda cy_hisse_isle / cy_birlestir yok")
        except Exception as ex:
            hata.append(f"17) eski kod yüklenemedi: {ex}")
    # ---------------- v1.3 (K52 analist revizyonları)
    # 18) günlük yükleme: aynı kurum aynı tarih tek kayıt, kurum adı normalize, olumlu / olumsuz bayrakları
    import pickle, tempfile
    g18 = pd.DataFrame({"Firm": ["JP Morgan & Co", "JPMorgan", "Barclays", "Citi", "UBS"], "ToGrade": ["Overweight", "Overweight", "Hold", "Buy", "Sell"],
                        "FromGrade": ["Neutral", "Neutral", "Buy", "", "Hold"], "Action": ["up", "up", "down", "init", "main"],
                        "priceTargetAction": ["Raises", "Raises", "Lowers", "Announces", "Maintains"], "currentPriceTarget": [10.0, 10.0, 5.0, 12.0, 0.0], "priorPriceTarget": [8.0, 8.0, 7.0, 0.0, 0.0]},
                       index=pd.DatetimeIndex(["2024-03-01 09:30", "2024-03-01 11:00", "2024-03-05", "2024-03-06", "2024-03-07"], name="GradeDate"))
    y18 = os.path.join(tempfile.gettempdir(), "cy_test_grades.pkl"); pickle.dump({"AAA": g18, "BBB": None}, open(y18, "wb"))
    G18 = C.cy_v13_gunluk_yukle(y18)
    if not (len(G18) == 4 and G18.olumlu.tolist() == [True, False, True, False] and G18.olumsuz.tolist() == [False, True, False, False]
            and G18.kurum_n.iloc[0] == "JPMORGAN" and G18.hedef.isna().iloc[3] and abs(G18.hedef_degisim.iloc[0] - 0.25) < 1e-9):
        hata.append(f"18) v1.3 günlük yükleme yanlış: n={len(G18)} olumlu={G18.olumlu.tolist()} kurum={G18.kurum_n.tolist()}")
    # 19) sızıntı: olay günü d için yalnız tarih <= d-1 kayıtları; aynı gün ve sonrası sayılmaz; kaydı olmayan sembolde kayit_var False
    t19 = pd.bdate_range("2024-01-01", periods=60); h19 = {"tarih": t19.to_numpy().astype("datetime64[ns]"), "kapanis": np.linspace(10, 12, 60),
                                                          "ptarih": t19.to_numpy().astype("datetime64[ns]"), "py": np.ones(60)}
    G19 = C.cy_v13_gunluk_yukle(y18); G19 = pd.concat([G19.assign(sembol="AAA", tarih=t19[29], zaman=t19[29]), G19.assign(sembol="AAA", tarih=t19[30], zaman=t19[30]),
                                                       G19.assign(sembol="AAA", tarih=t19[31], zaman=t19[31])], ignore_index=True)
    G19 = G19[G19.kurum_n.isin(["JPMORGAN", "BARCLAYS"])].drop_duplicates(["sembol", "kurum_n", "tarih"])   # her tarihte 1 olumlu (JPM) + 1 olumsuz (Barclays)
    E19 = pd.DataFrame({"sembol": ["AAA", "AAA", "ZZZ"], "tarih": [t19[30], t19[31], t19[30]], "i": [30, 31, 30]})
    F19 = C.cy_v13_ozellik(E19, G19, {"AAA": h19, "ZZZ": h19})
    if not (F19.n_kayit.tolist() == [2, 4, 0] and F19.kayit_var.tolist() == [True, True, False] and (not F19.teyit.any()) and F19.olumlu.tolist() == [1, 2, 0]):
        hata.append(f"19) v1.3 sızıntı kuralı yanlış: n_kayit={F19.n_kayit.tolist()} kayit_var={F19.kayit_var.tolist()} olumlu={F19.olumlu.tolist()}")
    # 20) teyit kuralı ve grup ayrımı: olumlu >= 1 ve olumlu > olumsuz -> teyit; veri var teyit yok -> G2a; veri yok -> G2b
    G20 = G19[G19.kurum_n == "JPMORGAN"]; F20 = C.cy_v13_ozellik(E19, G20, {"AAA": h19, "ZZZ": h19})
    grp20 = np.where(F20.teyit, "G1", np.where(F20.kayit_var, "G2a", "G2b")).tolist(); grp19 = np.where(F19.teyit, "G1", np.where(F19.kayit_var, "G2a", "G2b")).tolist()
    if not (grp20 == ["G1", "G1", "G2b"] and grp19 == ["G2a", "G2a", "G2b"] and F20.teyit_turu.tolist()[0] == "ikisi" and F20.tazelik_gun.tolist()[0] == 1):
        hata.append(f"20) v1.3 teyit / grup yanlış: {grp20} {grp19} {F20.teyit_turu.tolist()} {F20.tazelik_gun.tolist()}")
    # 21) hücre hesabı: Δ = ort(y - e_y | A) - ort(y - e_y | B) ve karar
    K13 = C.CY_V13; tt = pd.bdate_range("2023-01-02", periods=40, freq="3B")
    A21 = pd.DataFrame({"tarih": tt, "sembol": [f"S{i % 7}" for i in range(40)], "y": [1.0, 0.0] * 20, "e_y": 0.25, "net": 0.03, "e_net": 0.01, "agirlik": 1.0})
    B21 = pd.DataFrame({"tarih": tt, "sembol": [f"T{i % 7}" for i in range(40)], "y": 0.25, "e_y": 0.25, "net": 0.01, "e_net": 0.01, "agirlik": 1.0})
    h21 = C.cy_v13_fark(A21, B21, K13, np.random.default_rng(1))
    if not (abs(h21["delta"] - 0.25) < 1e-9 and abs(h21["net_fark"] - 0.02) < 1e-9 and h21["n_a"] == 40 and C.cy_v13_karar(h21, K13) == "TUTAR"
            and C.cy_v13_karar({"n_a": 10, "n_b": 40, "delta": 0.3, "delta_alt": 0.1, "net_fark": 0.1}, K13) == "YETERSİZ ÖRNEKLEM"):
        hata.append(f"21) v1.3 hücre hesabı yanlış: {h21.get('delta')} {h21.get('net_fark')}")
    # ---------------- v1.4 (K53 bilgi direnci)
    # 22) BDS: sentetik seri; pencerede fiyat SPY'ye göre zayıf, satış baskısı azalıyor (A10 B10'dan iyi), ATR düşüyor -> BDS 3; tersi -> BDS 0
    n22 = 60; C22 = np.full(n22, 100.0); H22 = C22 + 2.0; L22 = C22 - 2.0; V22 = np.full(n22, 1000.0)
    # B10 = [40, 49]: her gün -%2, geniş aralık, kapanış dipte, hacim yüksek; A10 = [50, 59] (pencere [55, 59]): hafif düşüş, dar aralık, kapanış tepede
    for t in range(40, 50):
        C22[t] = C22[t - 1] * 0.98; H22[t] = C22[t] + 3.0; L22[t] = C22[t] - 0.2; V22[t] = 3000.0
    for t in range(50, 60):
        C22[t] = C22[t - 1] * (0.999 if t % 2 else 1.0005); H22[t] = C22[t] + 0.2; L22[t] = C22[t] - 0.5; V22[t] = 800.0
    R22 = np.r_[np.nan, C22[1:] / C22[:-1] - 1]; rs22 = np.full(n22, 0.001); rk22 = np.full(n22, np.nan)
    f22 = C.cy_v14_sekil(C22, H22, L22, V22, R22, rs22, rk22, 59)
    if not (f22 and f22["bds"] == 3 and f22["fiyat_zayif"] and f22["satis_azaliyor"] and f22["oyn_dusuyor"] and f22["iyilesme"] >= 3 and np.isnan(f22["rel_sek5"])):
        hata.append(f"22) v1.4 BDS hesabı yanlış: {f22}")
    C22b = np.linspace(100, 130, n22); H22b = C22b + 1.0 + np.arange(n22) * 0.1; L22b = C22b - 1.0 - np.arange(n22) * 0.1; R22b = np.r_[np.nan, C22b[1:] / C22b[:-1] - 1]
    f22b = C.cy_v14_sekil(C22b, H22b, L22b, V22, R22b, np.zeros(n22), rk22, 59)
    if not (f22b and f22b["bds"] == 0 and not f22b["fiyat_zayif"] and not f22b["oyn_dusuyor"]):
        hata.append(f"22b) v1.4 BDS 0 bekleniyordu: {f22b}")
    if C.cy_v14_sekil(C22, H22, L22, V22, R22, rs22, rk22, 20)["gecerli"]:
        hata.append("22c) v1.4 yetersiz geçmişte geçersiz dönmeli")
    # 26) EK 1: eksik veri sıfır sayılmaz: pencerede SPY eksik -> ölçülemez (neden SPY); hacim sıfır -> hacim; ATR 0 -> ATR
    rs26 = rs22.copy(); rs26[57] = np.nan; f26 = C.cy_v14_sekil(C22, H22, L22, V22, R22, rs26, rk22, 59)
    V26 = V22.copy(); V26[35:55] = 0.0; f26b = C.cy_v14_sekil(C22, H22, L22, V26, R22, rs22, rk22, 59)
    f26c = C.cy_v14_sekil(np.full(60, 100.0), np.full(60, 100.0), np.full(60, 100.0), V22, np.zeros(60), rs22, rk22, 59)
    if not (not f26["gecerli"] and "SPY" in f26["neden"] and not f26b["gecerli"] and "hacim" in f26b["neden"] and not f26c["gecerli"] and "ATR" in f26c["neden"]):
        hata.append(f"26) v1.4 eksik veri işleme yanlış: {f26.get('neden')} {f26b.get('neden')} {f26c.get('neden')}")
    # 23) KGS: d0 = 10; 8. günde SPY göreli +%6 -> 8 (geç); hiç olmazsa 21 (yok); 3. günde -> hızlı
    C23 = np.full(50, 100.0); S23 = np.full(50, 100.0); C23[17:] = 106.0
    if not (C.cy_v14_kgs(C23, S23, 10) == 8 and C.cy_v14_kgs(np.full(50, 100.0), S23, 10) == 21):
        hata.append(f"23) v1.4 KGS yanlış: {C.cy_v14_kgs(C23, S23, 10)} {C.cy_v14_kgs(np.full(50, 100.0), S23, 10)}")
    C23c = np.full(50, 100.0); C23c[12:] = 110.0; S23c = np.full(50, 100.0); S23c[12:] = 104.0        # göreli +%5,8 -> 3. gün
    if C.cy_v14_kgs(C23c, S23c, 10) != 3:
        hata.append(f"23b) v1.4 KGS hızlı yanlış: {C.cy_v14_kgs(C23c, S23c, 10)}")
    # 27) EK 3: KGS-sonra başlangıç d0 kapanışı: sıçrama d0 günündeyse KGS-önce 1, KGS-sonra ulaşmadı (21); sıçrama 17. günde ise önce 8, sonra 7 (bir gün geç başlar)
    C27 = np.full(50, 100.0); C27[10:] = 106.0
    if not (C.cy_v14_kgs(C27, S23, 10) == 1 and C.cy_v14_kgs(C27, S23, 10, baslangic="sonra") == 21 and C.cy_v14_kgs(C23, S23, 10, baslangic="sonra") == 7):
        hata.append(f"27) v1.4 KGS-sonra yanlış: {C.cy_v14_kgs(C27, S23, 10)} {C.cy_v14_kgs(C27, S23, 10, baslangic='sonra')} {C.cy_v14_kgs(C23, S23, 10, baslangic='sonra')}")
    # 24) olay günleri: hafta sonu kaydı pazartesiye eşlenir; 5 gün arayla iki kayıt tek 'ilk' olay; 30 gün sonraki kayıt yeni olay; 10 gün boşluk kaydı düşer
    idx24 = pd.bdate_range("2024-01-01", periods=80).to_numpy().astype("datetime64[ns]")
    t24 = np.array(["2024-01-13", "2024-01-22", "2024-02-26", "2024-03-15"], dtype="datetime64[ns]")      # 13 Oca cumartesi -> 15 Oca (i=10); 22 Oca i=15; 26 Şub i=40; 15 Mar i=54
    idx24b = np.delete(idx24, np.arange(54, 64))                                                          # 15 Mar..28 Mar işlem günleri yok -> 15 Mar kaydı 10+ gün sonraya eşlenir, düşer
    hepsi24, ilk24 = C.cy_v14_olay_gunleri(idx24b, t24)
    if not (hepsi24.tolist() == [10, 15, 40] and ilk24.tolist() == [10, 40]):
        hata.append(f"24) v1.4 olay günleri yanlış: {hepsi24.tolist()} {ilk24.tolist()}")
    # 25) ADE: 90 gün içinde 3 kurumun son hedefleri (JPM 10 -> 12, Barclays 9, Citi 15) -> std/ort; 2 kurum -> boş
    g25 = pd.DataFrame({"tarih": pd.to_datetime(["2024-01-05", "2024-02-01", "2024-02-10", "2024-02-20", "2023-10-01"]), "kurum_n": ["JPM", "JPM", "BARCLAYS", "CITI", "UBS"], "hedef": [10.0, 12.0, 9.0, 15.0, 30.0]})
    a25, n25 = C.cy_v14_ade(g25, np.datetime64("2024-03-01"))
    bek = np.std([12.0, 9.0, 15.0]) / 12.0
    if not (n25 == 3 and abs(a25 - bek) < 1e-9 and np.isnan(C.cy_v14_ade(g25[g25.kurum_n != "CITI"], np.datetime64("2024-03-01"))[0])):
        hata.append(f"25) v1.4 ADE yanlış: {a25} {n25} (beklenen {bek})")
    # ---------------- v1.5 (K54 evren sınıflandırması)
    # 28) sınıflandırma kuralları (sentetik SEC özeti): 1 aktif, 2 iflas (8-K 1.03), 3 satın alma (2.01 + DEFM14A), 4a devam eden şirket, 4b kod yeniden kullanımı, 5 belirsiz, 6 doğrulanamayan
    def sec28(forms, dates, items=None):
        return {"name": "X", "tickers": ["XX"], "formerNames": [], "form": forms, "date": dates, "items": items or [""] * len(forms)}
    ti = {"endDate": "2026-10-29", "exchange": "NASDAQ"}
    r1 = C.cy_v15_sinifla("XX", "2026-08-28", 1, sec28(["10-Q"], ["2026-06-01"]), ti, 1)
    r2 = C.cy_v15_sinifla("XX", "2021-03-10", 1, sec28(["8-K", "10-Q"], ["2021-02-15", "2020-11-10"], ["1.03,9.01", ""]), {"endDate": "2021-03-10", "exchange": "NASDAQ"}, None)
    r3 = C.cy_v15_sinifla("XX", "2021-03-10", 1, sec28(["8-K", "DEFM14A", "10-Q"], ["2021-03-20", "2020-12-01", "2020-11-10"], ["2.01,9.01", "", ""]), None, None)
    r4a = C.cy_v15_sinifla("XX", "2021-03-10", 1, sec28(["10-Q", "10-K", "10-Q"], ["2023-05-10", "2022-03-01", "2020-11-10"]), None, 1)
    r4b = C.cy_v15_sinifla("XX", "2026-08-28", 1, sec28(["10-Q", "10-Q"], ["2020-06-30", "2020-03-31"]), ti, 999)       # seri bugüne sürüyor ama şirket 2020'de susmuş, sembol başka CIK'te
    r5 = C.cy_v15_sinifla("XX", "2021-03-10", 1, sec28(["15-12G", "10-Q"], ["2021-04-01", "2020-11-10"]), None, None)
    r6 = C.cy_v15_sinifla("XX", "2021-03-10", None, None, None, None)
    bek = [(r1, 1, "y"), (r2, 2, "y_d100"), (r3, 3, "y_d0"), (r4a, 4, "y_d0"), (r4b, 4, "y_kes"), (r5, 5, "y"), (r6, 6, "y")]
    if not all(r["sinif"] == sn and r["cikis_islemi"] == isl for r, sn, isl in bek) or r4b["kesim_tarihi"] != "2020-10-28" or r2["b103_tarih"] != "2021-02-15":
        hata.append("28) v1.5 sınıflandırma yanlış: " + "; ".join(f"{r['sinif']}/{r['cikis_islemi']} (bek {sn}/{isl})" for r, sn, isl in bek) + f" kes={r4b['kesim_tarihi']} b103={r2['b103_tarih']}")
    # 29) değerlendirme sınıfları
    e29 = {"n": 100, "fark": 0.03, "fark_alt": 0.01, "fark_ust": 0.05, "karar": "TUTMAZ"}; y29 = {"n": 95, "fark": 0.04, "fark_alt": 0.02, "fark_ust": 0.06, "karar": "TUTMAZ"}
    y29b = {"n": 95, "fark": 0.08, "fark_alt": 0.06, "fark_ust": 0.10, "karar": "TUTAR"}
    if not (C.cy_v15_degerlendir(e29, y29, 0.1, C.CY_V15) == "SAĞLAM" and C.cy_v15_degerlendir(e29, y29b, 0.1, C.CY_V15) == "ETKİLENMİŞ" and C.cy_v15_degerlendir(e29, y29, 0.5, C.CY_V15).startswith("GEÇERSİZ")):
        hata.append(f"29) v1.5 değerlendirme yanlış: {C.cy_v15_degerlendir(e29, y29, 0.1, C.CY_V15)} {C.cy_v15_degerlendir(e29, y29b, 0.1, C.CY_V15)}")
    return hata


if __name__ == "__main__":
    h = sina()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_col_yolu_abd: 29/29 OK")
