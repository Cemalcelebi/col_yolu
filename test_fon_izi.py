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
# 15) v1.5 SPK bicimi: Hisse Turk/Yabanci alt gruplari, ISIN'siz satir, 'Tem.Ver.' satiri, kodsuz ISIN satiri; GRUP TOPLAMI
#     mutabakati; islemde fiyat = deger olan 1 lotluk satir (sira: fiyat deger nominal) ve 'Toplami:' mutabakati.
# 16) v1.5 Atlas bicimi: %1.76 / 1.76% yuzde, kodu ust satirda kalan pozisyon, 'Hisse KOD .. g-Aaa-yy nominal tutar' islemleri ve
#     yalniz Hisse grubunun TOPLAM satiri (Takasbank grubu karismaz).
# 17) v1.5 tarih: 07/11/23, 30-Haz-25, 1-Şub-24, 05.01.2024.
# 18) v1.5 fon girisi: giris yalniz onceki ay raporu varsa; ikinci giren fon 'cok'; onceki ay hicbir fonda yoksa 'ilk'; cikis olayi;
#     fonlarin payi sermayenin %5 / %10'unu ilk astiginda yogun5/yogun10, bilinme = o ayin en gec fon raporu.
# 19) v1.5 giris mekanigi: yayin gunu ne saatte olursa olsun giris ertesi islem gunu acilisi; once +%20 (k20); +%8 sonrasi maliyete
#     donus -> trail getirisi 0 - %0,4; on60 giris oncesi veriyle (sonraki barlar degisince ayni).
# 21) K13 Ders 3 olcu/tarama (sentetik taban)
# 22) K14 esli kutu, yukselis, kirilim, ruzgar
# 23) K13b dip tabani (duzgun dip vs igne)
# 20) v1.5 artirimli ayristirma + paket: ikinci calistirmada eski rapor yeniden ayristirilmaz, yeni rapor eklenir; ayristirici
#     surumu farkli rapor yeniden ayristirilir; paket -> ac sonrasi tablolar ve metinler ayni; bozuk parca sha256 ile yakalanir.
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

    # 15) SPK bicimi
    m15 = "\n".join([
        "III-FON PORTFÖY DEĞERİ TABLOSU",
        "HİSSE SENETLERİ",
        "Hisse Türk",
        "AKBNK      TL   AKBANK   TRAAKBNK91N6     1.000,00   40,000000 23/07/25   80100511   50,000000   50.000,00   10,00",
        "                T.A.Ş.",
        "GEDZA      TL                 GEDZA           725,00   32,400000 27/12/22   80100514   36,880000   26.738,00   5,00",
        "Tem.Ver. ODAS   TL   ODAŞ   TREODAS00014      200,00   10,000000 30/12/22   80100511   10,000000    2.000,00   1,00",
        "                            TREDOTO00013      100,00   20,000000 20/08/24   80_100_5   20,000000    2.000,00   1,00",
        " GRUP TOPLAMI                                  2.025,00",
        "Hisse Yabancı",
        "AI US      USD  Application  US12468P1049      210,00   14,640000 17/11/22               14,000000    2.940,00",
        " GRUP TOPLAMI                                    210,00",
        "GRUP TOPLAMI                                   2.235,00",
        "IV-FON TOPLAM DEĞERİ TABLOSU",
        "    VII-PORTFÖYDEN SATIŞLAR",
        "     A) HİSSE SENETLERİ(SATIŞLAR)",
        "     TTRAK     TÜRK TRAKTÖR         06/12/22           539,300             539,30             1,00",
        "     TTRAK     TÜRK TRAKTÖR         06/12/22           539,200          36.665,60            68,00",
        "     HISSE TÜRK                          Toplamı:              37204,90            69,00",
        "     C) YATIRIM FONU (SATIŞLAR)",
        "     TKM TEB PORTFÖY   07/12/22  07/12/22   0,054     1.000.404,97   18.409.425,00",
        "IX-PORTFÖYE ALIŞLAR",
        "A) HİSSE SENETLERİ(ALIŞLAR)",
        "EKGYO                    07/11/23       6,770       67.700,00    10.000,00",
        "13X GF        13X GF     28/12/22       1,045       62.676,00    60.000,00",
        "                          Toplamı:         130376,00     70000,00",
        "H) MEVDUAT"])
    r15 = F.fi_k9_ayristir(m15); k15 = r15["kontrol"]
    kod15 = sorted(p["kod"] for p in r15["poz"]); t15 = [x for x in r15["islem"] if x["kod"] == "TTRAK"]
    if not (r15["bicim"] == "S" and kod15 == ["", "AKBNK", "GEDZA", "ODAS"] and k15["poz_rapor"] == 2025 and k15["poz_ayr"] == 2025
            and len(t15) == 2 and sorted(x["lot"] for x in t15) == [1.0, 68.0] and k15["satis_rapor"] == 69 and k15["satis_ayr"] == 69
            and k15["alis_rapor"] == 70000 and k15["alis_ayr"] == 70000 and abs(r15["poz"][0]["deger"] - 50000) < 1e-6):
        hata.append(f"15) SPK bicimi yanlis: {kod15} {k15} {t15}")
    # 16) Atlas bicimi
    m16 = "\n".join([
        "3- FON PORTFÖY DEĞERİ TABLOSU",
        " A) HİSSE SENETLERİ",
        "    ARASE                        Doğu Aras Enerji               38,000.00        8,724,800.00    %10.96",
        "   THYAO                 TÜRK HAVA YOLLARI A.O                25,433.00    7,210,255.50   9.33%",
        "   PGSUS",
        "                                    YOLLARI A.O            22,500.00    3,170,250.00   4.73%",
        "    TOPLAM:                                                85,933.00   19,105,305.50",
        " B) VARANTLAR",
        "4- FON TOPLAM DEĞERİ TABLOSU",
        "8-PORTFÖYDEN SATIŞLAR",
        "     Takasbank Para Piyasası   TRY      2-Haz-25        3-Haz-25               6,170,000.00   6,178,375.99",
        "TOPLAM:                                                     6,170,000.00   6,178,375.99",
        "Hisse     AKBNK   AKBANK T.A.S.                  2-Haz-25          343.00       17,493.00",
        "Hisse     AKBNK   AKBANK T.A.Ş.                  2-Haz-25          343.00       17,493.00",
        " TOPLAM:                                  686.00   34,986.00",
        "9- PORTFÖYE ALIŞLAR",
        "Hisse   GARAN   Garanti Bankası A.Ş.             30-Haz-25    142.00      17,679.00",
        "TOPLAM:                                                142.00      17,679.00"])
    r16 = F.fi_k9_ayristir(m16); k16 = r16["kontrol"]
    if not (r16["bicim"] == "A" and [p["kod"] for p in r16["poz"]] == ["ARASE", "THYAO", "PGSUS"] and k16["poz_ayr"] == k16["poz_rapor"] == 85933
            and k16["satis_ayr"] == k16["satis_rapor"] == 686 and k16["alis_ayr"] == k16["alis_rapor"] == 142
            and r16["islem"][0]["tarih"] == "2025-06-02" and abs(r16["islem"][0]["fiyat"] - 51.0) < 1e-9):
        hata.append(f"16) Atlas bicimi yanlis: {[p['kod'] for p in r16['poz']]} {k16}")
    # 17) tarih
    if [F._fi_tarih(x) for x in ("07/11/23", "30-Haz-25", "1-Şub-24", "05.01.2024", "31/02/24")] != \
            ["2023-11-07", "2025-06-30", "2024-02-01", "2024-01-05", None]:
        hata.append("17) tarih cevirisi yanlis")
    # 18) fon girisi / cikisi
    G18 = pd.DataFrame([
        {"fon": "F1", "sirket": "XX", "ay": 100, "kod": "AAA", "nominal": 10.0, "agirlik": 0.5},
        {"fon": "F1", "sirket": "XX", "ay": 101, "kod": "AAA", "nominal": 10.0, "agirlik": 0.5},
        {"fon": "F1", "sirket": "XX", "ay": 101, "kod": "BBB", "nominal": 5.0, "agirlik": 0.5},     # F1 BBB girisi (ilk)
        {"fon": "F2", "sirket": "TERA", "ay": 101, "kod": "BBB", "nominal": 5.0, "agirlik": 0.02},  # F2 BBB girisi (2. fon -> cok)
        {"fon": "F3", "sirket": "XX", "ay": 101, "kod": "CCC", "nominal": 5.0, "agirlik": 1.0},     # F3'un ay 100 raporu yok -> giris degil
        {"fon": "F1", "sirket": "XX", "ay": 102, "kod": "BBB", "nominal": 5.0, "agirlik": 1.0}])   # F1 AAA cikisi (ay 102)
    KP18 = pd.DataFrame([{"fon": f, "ay": a, "bilinme": pd.Timestamp("2024-01-01") + pd.Timedelta(days=30 * (a - 100) + i)}
                         for i, (f, a) in enumerate([("F1", 100), ("F1", 101), ("F2", 100), ("F2", 101), ("F3", 101), ("F1", 102)])])
    G18 = G18.merge(KP18, on=["fon", "ay"], how="left")
    O18 = pd.DataFrame([{"kod": k_, "ay": a_, "oran": 1.0} for k_ in ("AAA", "BBB", "CCC") for a_ in (99, 100, 101, 102)])
    D18 = pd.DataFrame([{"kod": "BBB", "sermaye_lot": 100.0}])
    E18 = F.fi_k10_olaylar(G18, KP18, O18, D18)
    y18 = E18[E18.tur.astype(str).str.startswith("yogun")]
    if not (sorted(y18.tur) == ["yogun10", "yogun5"] and (y18.kod == "BBB").all() and abs(y18.pay.iat[0] - 0.1) < 1e-12
            and y18.bilinme.iat[0] == G18[(G18.kod == "BBB") & (G18.ay == 101)].bilinme.max()):
        hata.append(f"18) yogun olayi yanlis: {y18.to_dict('records')}")
    gi = E18[E18.tur == "giris"]; ci = E18[E18.tur == "cikis"]
    if not (len(gi) == 2 and set(gi.fon) == {"F1", "F2"} and set(gi.kod) == {"BBB"}
            and gi[gi.fon == "F1"].ilk.iat[0] and not gi[gi.fon == "F2"].ilk.iat[0] and gi[gi.fon == "F2"].cok.iat[0]
            and gi[gi.fon == "F2"].tasfiye.iat[0] and gi[gi.fon == "F1"].buyuk.iat[0] and not gi[gi.fon == "F2"].buyuk.iat[0]
            and len(ci) == 1 and ci.kod.iat[0] == "AAA" and ci.ay.iat[0] == 102):
        hata.append(f"18) fon girisi/cikisi yanlis: {E18[['tur', 'fon', 'kod', 'ay', 'ilk', 'cok']].to_dict('records')}")
    # 19) giris mekanigi
    idx19 = pd.bdate_range("2024-01-01", periods=150)
    c19 = np.full(150, 101.0); o19 = c19.copy(); h19 = c19 + 1; l19 = c19 - 0.5
    o19[80] = 100.0; h19[82] = 109.0; l19[85] = 99.5                               # giris 100; +%9 gorulur, 85. barda maliyete doner
    d19 = pd.DataFrame({"Open": o19, "High": h19, "Low": l19, "Close": c19, "Volume": 1e6}, index=idx19)
    R19 = F.fi_k10_sonuc({"AAA": d19}, pd.Series(["AAA"]), pd.Series([idx19[79] + pd.Timedelta(hours=10)]))
    d19b = d19.copy(); d19b.iloc[100:, :4] = 500.0
    R19b = F.fi_k10_sonuc({"AAA": d19b}, pd.Series(["AAA"]), pd.Series([idx19[79]]))
    if not (len(R19) == 1 and R19.giris.iat[0] == idx19[80] and abs(R19.trail.iat[0] + 0.004) < 1e-12 and R19.k20.iat[0] == 0
            and R19.cikis_tarih.iat[0] == idx19[85] and R19.on60.iat[0] == R19b.on60.iat[0]):
        hata.append(f"19) giris mekanigi yanlis: {R19.to_dict('records')}")

    # 20) artirimli ayristirma + paket
    import tempfile, os, shutil
    kok = tempfile.mkdtemp(); A20 = F.FIAyar(kapfon=os.path.join(kok, "kf"))
    os.makedirs(os.path.join(A20.kapfon, "txt"))
    for i in (1, 2):
        with open(os.path.join(A20.kapfon, "txt", f"{i}__X_2024_{i}_0.txt"), "w", encoding="utf-8") as f:
            f.write(m15)
    L20 = pd.DataFrame([{"yayin": f"0{i}.0{i + 1}.2024 10:00:00", "fon": "XX", "unvan": "DENEME PORTFÖY HİSSE SENEDİ FONU",
                         "indeks": i, "yil": 2024, "donem": i, "ek": 1, "kural": f"{i}. Ay"} for i in (1, 2)])
    L20.to_csv(os.path.join(A20.kapfon, "liste.csv"), index=False)
    E20 = pd.DataFrame([{"indeks": 1, "dosya": "txt/1__X_2024_1_0.txt", "durum": "ok"}])
    P1, I1, K1 = F.fi_k9_tablolar_guncel(L20, E20, A20)
    E20 = pd.concat([E20, pd.DataFrame([{"indeks": 2, "dosya": os.path.join(A20.kapfon, "txt", "2__X_2024_2_0.txt"), "durum": "ok"}])])
    E20.to_csv(os.path.join(A20.kapfon, "ekler.csv"), index=False)
    E20 = F.fi_k9_ekler_oku(A20)                                   # mutlak yol -> goreli
    k0 = pd.read_csv(os.path.join(A20.kapfon, "k9_kontrol.csv.gz"))
    P2, I2, K2 = F.fi_k9_tablolar_guncel(L20, E20, A20)
    k2 = pd.read_csv(os.path.join(A20.kapfon, "k9_kontrol.csv.gz"))
    K2b = k2.copy(); K2b["ayristirici"] = K2b.ayristirici.astype(str); K2b.loc[K2b.indeks == 1, "ayristirici"] = "eski"; K2b.to_csv(os.path.join(A20.kapfon, "k9_kontrol.csv.gz"), index=False)
    P3, I3, K3 = F.fi_k9_tablolar_guncel(L20, E20, A20)
    paket = os.path.join(kok, "paket"); F.fi_k9_paketle(A20, paket, parca_mb=1)
    A20b = F.FIAyar(kapfon=os.path.join(kok, "kf2")); F.fi_k9_paket_ac(paket, A20b)
    acik_ok = (open(os.path.join(A20b.kapfon, "txt", "2__X_2024_2_0.txt"), encoding="utf-8").read() == m15 and
               len(pd.read_csv(os.path.join(A20b.kapfon, "k9_pozisyon.csv.gz"))) == len(P3))
    with open(os.path.join(paket, "metin.tar.xz.000"), "ab") as f:
        f.write(b"x")
    try:
        F.fi_k9_paket_ac(paket, F.FIAyar(kapfon=os.path.join(kok, "kf3"))); bozuk_yakalandi = False
    except RuntimeError:
        bozuk_yakalandi = True
    shutil.rmtree(kok)
    if not (len(K1) == 1 and len(K2) == 2 and len(P2) == 2 * len(P1) and list(E20.dosya) == ["txt/1__X_2024_1_0.txt", "txt/2__X_2024_2_0.txt"]
            and set(K3.ayristirici) == {F.FI_K9_SURUM} and len(P3) == len(P2) and acik_ok and bozuk_yakalandi
            and (k0.indeks == 1).all() and len(k2) == 2):
        hata.append(f"20) artirimli ayristirma / paket yanlis: {len(K1)} {len(K2)} {len(P1)} {len(P2)} {acik_ok} {bozuk_yakalandi}")
    # 21) K13 (Ders 3) olcu ve tarama: 400 bar sakin, 30 barda -%60, 60 bar kucuk mumlu hafif yukselen taban -> tek olay, dip
    # cokusun dibi, bilgi gunu tabanin icinde; ayni seri tabanda genis bantla (+-%20 salinim) -> olay yok.
    rng21 = np.random.default_rng(21)
    def seri21(salinim):
        c = np.r_[100 * np.exp(np.cumsum(rng21.normal(0, 0.01, 400))), np.linspace(100, 40, 31)[1:],
                  40 * (1 + np.linspace(0, 0.08, 60)) * (1 + salinim * np.sin(np.arange(60) / 3)), np.linspace(43.2, 50, 40)]
        c[:400] *= 100 / c[399]
        rg = np.r_[np.full(430, 0.04), np.full(60, 0.012), np.full(40, 0.03)]
        idx = pd.bdate_range("2020-01-01", periods=len(c))
        return pd.DataFrame({"Open": c, "High": c * (1 + rg / 2), "Low": c * (1 - rg / 2), "Close": c, "Volume": 1e6}, index=idx)
    d21 = seri21(0.0); O21 = F.fi_k13_tara({"AAA": d21}); O21b = F.fi_k13_tara({"BBB": seri21(0.20)})
    o21 = F.fi_k13_olc(d21, 430, 479)
    ok21 = (len(O21) == 1 and 425 <= d21.index.get_loc(O21.dip.iloc[0]) <= 431 and 455 <= d21.index.get_loc(O21.bilgi.iloc[0]) <= 489
            and len(O21b) == 0 and o21["bar"] == 50 and o21["dusus"] < -0.55 and o21["mum_norm"] < 0.5 and o21["u"] > 1.02)
    if not ok21:
        hata.append(f"21) K13 tarama/olcu yanlis: {len(O21)} {len(O21b)} {o21}")
    # 22) K14: esli kutu (genis bantli ayni cokus -> esli var; K13 olayinin dibinden olay gununden SONRA esli olmaz, oncesi
    # olabilir — v1.6 denetim: eskiden gelecekteki olay da eliyordu), yukselis (2 kat dip kirilmadan /
    # once dip kirilir), kirilim (tavan ustu kapanis -> yeni bilgi gunu), ruzgar (yukselen sektor ruzgarli, duz sektor degil).
    d22b = seri21(0.20)
    Es22 = F.fi_k14_esli({"AAA": d21, "BBB": d22b}, O21)
    def seri22(son):
        c = np.r_[np.full(300, 10.0), np.full(30, 10.0), son]
        idx = pd.bdate_range("2021-01-01", periods=len(c))
        return pd.DataFrame({"Open": c, "High": c * 1.01, "Low": c * 0.99, "Close": c, "Volume": 1e6}, index=idx)
    yuk = seri22(np.linspace(10, 25, 260)); dus_ = seri22(np.r_[np.linspace(10, 9, 20), np.linspace(9, 25, 240)])
    O22 = pd.DataFrame({"sembol": ["Y", "D"], "dip": [yuk.index[300]] * 2, "bilgi": [yuk.index[329]] * 2})
    Y22 = F.fi_k14_yukselis({"Y": yuk, "D": dus_}, O22)
    kir = seri22(np.r_[np.full(5, 10.0), np.full(20, 10.5), np.full(240, 10.5)])
    K22 = F.fi_k14_kirilim({"Y": kir}, O22.iloc[:1])
    idx22 = pd.bdate_range("2022-01-01", periods=200)
    V22 = {f"{g}{k}": pd.DataFrame({"Close": (np.linspace(10, 20, 200) if g == "A" else np.full(200, 10.0)) * (1 + 0.001 * k)}, index=idx22)
           for g in "AB" for k in range(5)}
    for k in range(10):
        V22[f"C{k}"] = pd.DataFrame({"Close": np.full(200, 10.0)}, index=idx22)
    W22 = F.fi_k14_ruzgar(V22, {s: s[0] for s in V22})
    ok22 = (len(Es22) >= 1 and "BBB" in set(Es22.sembol)
            and (Es22[Es22.sembol == "AAA"].bilgi < O21.bilgi.iloc[0]).all()      # v1.6: esli yalniz gecmisi bilir (olaydan sonra yok) and list(Y22.kat2) == [1.0, 0.0] and Y22.dip_kirildi.iloc[1] == 1.0
            and len(K22) == 1 and K22.bilgi.iloc[0] == kir.index[335] and bool(W22["A0"].iloc[-1]) and not bool(W22["B0"].iloc[-1])
            and not W22["A0"].iloc[:60].any())
    if not ok22:
        hata.append(f"22) K14 esli/yukselis/kirilim/ruzgar yanlis: {len(Es22)} {list(Y22.kat2) if len(Y22) else []} {len(K22)}")
    # 23) K13b dip tabanı: tek günlük iğne dip (V) düşük, haftalarca test edilen düz zemin yüksek.
    idx23 = pd.bdate_range("2022-01-03", periods=400)
    def kutu23(duz):
        c = np.full(400, 50.0); c[350:] = 51.0
        low = c * 0.99
        if duz:
            low[350:400:3] = 50.0 * 0.995           # her 3 günde bir dibe değiyor
        else:
            low[350] = 45.0                         # tek günlük iğne
        return pd.DataFrame({"Open": c, "High": c * 1.01, "Low": low, "Close": c, "Volume": 1e6}, index=idx23)
    a23 = F.fi_k13_olc(kutu23(True), 350, 399)["dip_taban"]; b23 = F.fi_k13_olc(kutu23(False), 350, 399)["dip_taban"]
    if not (a23 >= 0.30 and b23 <= 0.05):
        hata.append(f"23) dip tabanı yanlış: düz {a23:.2f} iğne {b23:.2f}")
    # 24) K17 iki yuvarlama: çöküş -> dip -> ∩ (aşağı yuvarlama) -> ∪ (yukarı yuvarlama) olay verir; yalnız ∪ (∩ yok) ve ∪'nun
    # dibi asıl dibi kırarsa olay yok; olay günü 2. bölge yukarı dönmeden önce değil.
    def seri24(kol):
        x1 = np.linspace(0, 1, 25); x2 = np.linspace(0, 1, 30)
        ark = 11 + 2.0 * np.sin(np.pi * x1) + x1                             # 11 -> 13,5 -> 12 (∩)
        kase = 12 + 1.6 * ((2 * x2 - 1) ** 2 - 1)                             # 12 -> 10,4 -> 12 (∪), dipten +%4
        if kol == "kase":
            ark = np.full(25, 11.0)
        if kol == "kirik":
            kase = kase - 1.6                                                 # ∪'nun dibi asıl dibin (10) altına iner
        c = np.r_[np.full(330, 20.0), np.linspace(20, 10, 20), [10.0], ark, kase, np.full(80, kase[-1])]
        idx = pd.bdate_range("2019-01-01", periods=len(c))
        return pd.DataFrame({"Open": c, "High": c * 1.01, "Low": c * 0.995, "Close": c, "Volume": 1e6}, index=idx)
    O24 = F.fi_k17_tara({"IKI": seri24("iki"), "KASE": seri24("kase"), "KIRIK": seri24("kirik")})
    ok24 = list(O24.sembol) == ["IKI"] and O24.bilgi.iloc[0] > seri24("iki").index[350 + 1 + 25 + 15] if len(O24) else False
    if not ok24:
        hata.append(f"24) K17 iki yuvarlama yanlış: {list(O24.sembol) if len(O24) else []}")
    # 25) v1.6 fi_duzelt (denetim): %15 yukarı tavan günü gerçek hareket (düzeltilmez); %50 bedelsiz düşüşü düzeltilir; piyasa
    # geneli aşağı sıçrama günü (hisselerin >= %2'si) bölünme sayılmaz.
    idx25 = pd.bdate_range("2023-01-02", periods=60)
    def seri25(adim, gun=30):
        c = np.full(60, 10.0); c[gun:] = 10.0 * adim
        return pd.DataFrame({"Open": c, "High": c * 1.01, "Low": c * 0.99, "Close": c, "Volume": 1e6}, index=idx25)
    A25 = F.FIAyar()
    u25, nu = F.fi_duzelt(seri25(1.15), A25)
    b25, nb = F.fi_duzelt(seri25(0.5), A25)
    piy25 = F.fi_piyasa_sicrama({f"H{k}": seri25(0.8) for k in range(10)}, A25)
    m25, nm = F.fi_duzelt(seri25(0.8), A25, piyasa=piy25)
    if not (nu == 0 and abs(u25.Close.iloc[0] - 10) < 1e-9 and nb == 1 and abs(b25.Close.iloc[0] - 5) < 1e-9
            and idx25[30] in piy25["asagi"] and nm == 0):
        hata.append(f"25) fi_duzelt v1.6 yanlış: yukarı {nu}, bedelsiz {nb}, piyasa günü {nm}")
    # 26) v1.6 K13 değişmezi (denetim): her olayda dipten bilgi gününe kadar dibin altına inen Low yok (eskiden t-29 barı
    # denetlenmiyordu; BIST 193 olayın 45'inde ihlal vardı). Gürültülü çöküş serilerinde gevşek eşikle sınanır.
    rng26 = np.random.default_rng(26); V26 = {}
    for k in range(12):
        c = np.r_[100 * np.exp(np.cumsum(rng26.normal(0, 0.01, 400))), np.linspace(100, 45, 30),
                  45 * np.exp(np.cumsum(rng26.normal(0.001, 0.025, 200)))]
        idx = pd.bdate_range("2019-01-01", periods=len(c))
        V26[f"R{k}"] = pd.DataFrame({"Open": c, "High": c * 1.02, "Low": c * (0.98 - 0.03 * rng26.random(len(c))), "Close": c,
                                     "Volume": 1e6}, index=idx)
    O26 = F.fi_k13_tara(V26, F.FI_K16_GEVSEK)
    ihlal26 = sum(V26[r.sembol].Low.loc[r.dip:r.bilgi].iloc[1:].min() < V26[r.sembol].Low.loc[r.dip] for r in O26.itertuples())
    if not len(O26) or ihlal26:
        hata.append(f"26) K13 dipten sonra yeni dip: {ihlal26}/{len(O26)} olay")
    # 27) K18 Cemal'in vaka profili: çöküş (iri mum, yüksek hacim) -> dar kutu (küçük mum, düşük hacim) -> kutu tavanı kırılımı
    # C1 olayı verir (bilgi = kırılım günü, kutu çöküş dibinden başlar); kutu mumları iri ise C1 yok, EŞLİ var; çöküş yoksa hiç olay
    # yok; kırılımdan sonraki veri değişse de olay aynı (geleceğe bakmaz).
    def seri27(kol, kes=None):
        c = np.r_[np.full(300, 20.0), np.linspace(20, 8, 30), np.linspace(8, 8.6, 50), [9.2], np.full(40, 9.4)]
        if kol == "dusussuz":
            c = np.r_[np.full(330, 8.0), np.linspace(8, 8.6, 50), [9.2], np.full(40, 9.4)]
        r = np.r_[np.full(300, 0.04), np.full(30, 0.08), np.full(50, 0.10 if kol == "iri" else 0.02), np.full(41, 0.05)]
        v = np.r_[np.full(300, 2e6), np.full(30, 3e6), np.full(50, 1e6), np.full(41, 2e6)]
        idx = pd.bdate_range("2019-01-01", periods=len(c))
        d = pd.DataFrame({"Open": c, "High": c * (1 + r / 2), "Low": c * (1 - r / 2), "Close": c, "Volume": v}, index=idx)
        return d.iloc[:kes] if kes else d
    V27 = {"COL": seri27("col"), "IRI": seri27("iri"), "DUZ": seri27("dusussuz")}
    C27 = F.fi_k18_tara(V27, F.FI_K18_ESIK, True); E27 = F.fi_k18_tara(V27, F.FI_K18_ESIK, False)
    K27 = F.fi_k18_tara({"COL": seri27("col", kes=381)}, F.FI_K18_ESIK, True)
    ok27 = (list(C27.sembol) == ["COL"] and list(E27.sembol) == ["IRI"] and C27.bilgi.iloc[0] == V27["COL"].index[380]
            and C27.dip.iloc[0] <= V27["COL"].index[331] and len(K27) == 1 and K27.bilgi.iloc[0] == C27.bilgi.iloc[0]
            and abs(K27.mum_kat.iloc[0] - C27.mum_kat.iloc[0]) < 1e-12) if len(C27) and len(E27) else False
    if not ok27:
        hata.append(f"27) K18 profil yanlış: C1 {list(C27.sembol) if len(C27) else []} eşli {list(E27.sembol) if len(E27) else []}")
    # 28) K19 sistem çıkışı: kapanış stop altına inerse o kapanıştan çık; +%20 görülünce ertesi bardan SMA20 trail (ufuk yok);
    # ikisi de yoksa 120. bar; 120 bar dolmadan veri biterse sayılmaz; aynı bar stop + hedef -> stop.
    def cik28(c, h=None, stop=9.0):
        c = np.asarray(c, float); h = c if h is None else np.asarray(h, float)
        return F.fi_k19_cikis(c, h, pd.Series(c).rolling(20).mean().to_numpy(), 0, 10.0, stop)
    s28 = cik28(np.r_[np.full(10, 10.0), [8.5], np.full(200, 10.0)])
    t28 = cik28(np.r_[np.linspace(10, 13, 30), np.full(30, 13.0), [11.0], np.full(100, 11.0)])
    u28 = cik28(np.full(150, 10.5)); n28 = cik28(np.full(50, 10.5))
    a28 = cik28(np.r_[[8.5], np.full(30, 10)], h=np.r_[[12.5], np.full(30, 10)])
    if not (abs(s28[0] - (0.85 - 1 - 0.004)) < 1e-9 and s28[1] == 11 and abs(t28[0] - (1.1 - 1 - 0.004)) < 1e-9
            and abs(u28[0] - (0.05 - 0.004)) < 1e-9 and u28[1] == 120 and n28[0] != n28[0] and abs(a28[0] - (-0.154)) < 1e-9):
        hata.append(f"28) K19 çıkış yanlış: stop {s28} trail {t28} ufuk {u28} kısa {n28} aynı bar {a28}")
    # 29) K21/K22 mum mum: yol girişin açılışından (k=0 giriş günü kapanışı), sıra sinyal hissesi hariç diğer hisselere göre; bekleyen emir
    # dolumu max(açılış, seviye) ve kapanış seviyenin altındaysa sahte; pencere 'dahil' t-1 kapanışından.
    ix29 = pd.bdate_range("2024-01-01", periods=200)
    def df29(c, o=None):
        c = np.asarray(c, float); o = c if o is None else np.asarray(o, float)
        return pd.DataFrame({"Open": o, "High": np.maximum(o, c), "Low": np.minimum(o, c), "Close": c, "Volume": 1.0}, index=ix29)
    V29 = {"S": df29(np.r_[np.full(100, 10.0), np.full(100, 12.0)], np.r_[np.full(100, 10.0), [11.0], np.full(99, 12.0)]),
           "A": df29(np.full(200, 10.0)), "B": df29(np.r_[np.full(100, 10.0), np.full(100, 13.0)], np.r_[np.full(101, 10.0), np.full(99, 13.0)])}
    W29 = F.fi_k21_yol(V29, pd.DataFrame({"sembol": ["S"], "giris": [ix29[100]]}), {**F.FI_K21, "ufuk": 5})
    P29 = F.fi_k22_pencere(V29, pd.DataFrame({"sembol": ["S"], "bilgi": [ix29[100]]}), g=5)
    ok29 = (len(W29["P"]) == 1 and abs(W29["P"][0, 0] - (12 / 11 - 1)) < 1e-12 and abs(W29["R"][0, 0] - 0.5) < 1e-12
            and abs(W29["M"][0, 0] - ((10 / 10 - 1) + (13 / 10 - 1)) / 2) < 1e-12 and len(P29) == 1
            and abs(P29.dahil_r.iloc[0] - 0.2) < 1e-12 and abs(P29.sonra_r.iloc[0]) < 1e-12 and abs(P29.sonra_sira.iloc[0] - 0.0) < 1e-12)
    S29 = F.fi_k22_sira(V29, pd.DataFrame({"sembol": ["S"], "bilgi": [ix29[100]], "dolum": [11.5], "sahte": [False]}), {**F.FI_K22, "gun": (0, 5)})
    ok29 = ok29 and len(S29) == 1 and abs(S29.r0.iloc[0] - (12 / 11.5 - 1)) < 1e-12 and abs(S29.s0.iloc[0] - 0.5) < 1e-12
    if not ok29:
        hata.append(f"29) K21/K22 mum mum yol/sıra yanlış: P {W29['P'][:1, :1] if len(W29['P']) else []} R {W29['R'][:1, :1] if len(W29['R']) else []} "
                    f"pencere {P29.to_dict('records') if len(P29) else []} emir {S29.to_dict('records') if len(S29) else []}")
    # 30) K23/K24 iki evre: 150 bar 20'de yatay, 60 barda 10'a düşüş, 12 bar dipte hafif iniş (SMA20 altında, bant daralıyor), sonra 5 bar
    # SMA20 üstünde dar dizilme (dipleri SMA'nın üstünde) -> K24 kuralı 5. günde tetikler; K23 seri = 5/L, delen = 0, once_alt = 1.
    ix30 = pd.bdate_range("2020-01-01", periods=300)
    c30 = np.r_[np.full(150, 20.0), np.linspace(20, 10, 60), np.linspace(9.95, 9.8, 12), [10.3, 10.35, 10.4, 10.45, 10.5], np.full(73, 10.5)]
    d30 = pd.DataFrame({"Open": c30 * 0.999, "High": c30 * 1.005, "Low": c30 * 0.995, "Close": c30, "Volume": 1e6}, index=ix30)
    K30 = F.fi_k24_tara(d30); t30 = ix30[226]
    P30 = F.fi_k23_parmak(d30, 15).loc[t30]
    ok30 = (len(K30) >= 1 and bool(K30.loc[K30.tarih == t30, "kural"].any()) and abs(P30.seri - 5 / 15) < 1e-12 and P30.delen == 0
            and abs(P30.once_alt - 1.0) < 1e-12 and P30.dusus < -0.4)
    if not ok30:
        hata.append(f"30) K23/K24 iki evre yanlış: K24 {K30.to_dict('records') if len(K30) else []} K23 seri {P30.seri} delen {P30.delen} "
                    f"once_alt {P30.once_alt} dusus {P30.dusus}")
    # 31) K25: payın ilk kez %5'i geçtiği rapor olay; sinyal anında bilinen pay (önceki rapor) ve sonraki 365 günde en yüksek pay.
    M31 = pd.DataFrame({"kod": ["X", "X", "Y"], "ay": [24288, 24290, 24288], "bil": pd.to_datetime(["2024-01-05", "2024-03-05", "2024-01-05"]),
                        "pay": [0.01, 0.06, 0.001]})
    G31 = F.fi_k25_girisler(M31); S31 = F.fi_k25_sonra(M31, pd.DataFrame({"sembol": ["X", "Y"], "tarih": pd.to_datetime(["2024-02-01"] * 2)}))
    ok31 = (list(G31.sembol) == ["X"] and G31.bil.iloc[0] == pd.Timestamp("2024-03-05") and abs(S31.pay0.iloc[0] - 0.01) < 1e-12
            and abs(S31.pay_max.iloc[0] - 0.06) < 1e-12 and bool(S31.giris5.iloc[0]) and not bool(S31.giris5.iloc[1]))
    if not ok31:
        hata.append(f"31) K25 fon girişi yanlış: olay {G31.to_dict('records')} sinyal {S31.to_dict('records')}")
    # 32) Kör set değerlendirme emri: bölge tepesi x 1,002'de bekleyen alış; dolum max(açılış, seviye); sonra +%15 önce -> yukarı.
    ix32 = pd.bdate_range("2021-01-01", periods=400)
    c32 = np.r_[np.full(300, 10.0), [10.5], np.linspace(10.6, 16.0, 99)]
    d32 = pd.DataFrame({"Open": c32, "High": c32 * 1.001, "Low": c32 * 0.999, "Close": c32, "Volume": 1.0}, index=ix32)
    R32 = F.fi_k23_emir_sonuc(d32, ix32[299], 10)
    ok32 = bool(R32["tepe_doldu"]) and R32["tepe_y60"] == 1.0 and bool(R32["govde_doldu"])
    if not ok32:
        hata.append(f"32) K23 kör set emir sonucu yanlış: {R32}")
    return hata


if __name__ == "__main__":
    h = sina()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_fon_izi: 32/32 OK")
