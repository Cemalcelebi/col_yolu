"""K55 birim ve sentetik testler (Faz 0 madde 6). Gerçek veri gerekmez. Çalıştırma: python test_k55.py"""
from __future__ import annotations

import os
import sys
import tempfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from K55 import eslestirme, hucre, hucreler, istatistik, olay_tanimlari, ortak, sizinti, vekil as vkm, veri_kalitesi, veri_paket  # noqa: E402
from K55 import evren as evm  # noqa: E402
from K55.evren import evren_daralt, ornek_sec  # noqa: E402


def _seri(n=600, tohum=1, bas="2018-01-01"):
    rng = np.random.default_rng(tohum); r = rng.normal(0, 0.01, n); C = 100 * np.exp(np.cumsum(r)); O = C * (1 + rng.normal(0, 0.002, n))
    H = np.maximum(O, C) * (1 + abs(rng.normal(0, 0.004, n))); L = np.minimum(O, C) * (1 - abs(rng.normal(0, 0.004, n))); V = rng.integers(100000, 500000, n).astype(float)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=pd.bdate_range(bas, periods=n))


def testler():
    hata = []
    # 1) olay tanımı: i=300'de Y60 olayı (C[360] = 1,4 × O[301]); 310'daki ikinci aday örtüştüğü için alınmaz; tekillik geçer
    d = _seri(); d.iloc[301, 0] = 100.0; d.iloc[360, 3] = 141.0; d.iloc[311, 0] = 100.0; d.iloc[370, 3] = 145.0
    lk = np.ones(len(d), dtype=bool); rows, tan = olay_tanimlari.sembol_olaylari("X", d, lk)
    y60 = [r for r in rows if r["ufuk"] == "Y60"]
    if not (len(y60) >= 1 and y60[0]["i"] == 300 and abs(y60[0]["getiri"] - 0.41) < 1e-9 and all(r["i"] != 310 for r in y60)):
        hata.append(f"1) olay tanımı yanlış: {[(r['i'], round(r['getiri'], 3)) for r in y60]}")
    O = pd.DataFrame(rows); O["tarih"] = pd.to_datetime(O.tarih)
    if not olay_tanimlari.olay_tekillik_denetimi(O)["gecti"]:
        hata.append("1b) tekillik denetimi yanlış")
    # 1c) likit olmayan gün olay olamaz; pencere seri sonunu aşan gün tanımsız (sayım)
    lk2 = lk.copy(); lk2[300] = False; rows2, tan2 = olay_tanimlari.sembol_olaylari("X", d, lk2)
    if any(r["i"] == 300 for r in rows2) or tan2["Y60"] != len(d) - 61:
        hata.append(f"1c) likit / tanımlı sayımı yanlış: {tan2}")
    # 2) ileri getiri seri sonu işlemi
    O_ = np.full(100, 10.0); C_ = np.full(100, 10.0); C_[-61:] = 9.0; C_[-1] = 8.0
    r100, _ = olay_tanimlari.ileri_getiri(O_, C_, 60, True, "d100"); r0, _ = olay_tanimlari.ileri_getiri(O_, C_, 60, True, "d0"); rk, tam = olay_tanimlari.ileri_getiri(O_, C_, 60, True, "k51")
    rn, tamn = olay_tanimlari.ileri_getiri(O_, C_, 60, False, "k51")
    if not (r100[50] == -1.0 and abs(r0[50] - (-0.2)) < 1e-9 and abs(rk[50] - (8 * 0.7 / 10 - 1)) < 1e-9 and np.isnan(rn[50]) and tam[10] and not tam[50] and abs(rk[10] - (C_[70] / 10 - 1)) < 1e-9):
        hata.append(f"2) ileri getiri seri sonu işlemi yanlış: {r100[50]} {r0[50]} {rk[50]} {rn[50]}")
    # 3) veri kalitesi (yeni modül, Cemal'in 11 vakası): temiz seri kullanılabilir; sırasız; yinelenen işlem günü; eksik OHLC; sıfır hacim; eksik hacim;
    # negatif fiyat; bölünme benzeri sıçrama; borsa tatili eksik gün değil; altı işlem günü boşluk ciddi; EV'de olup V'de olmayan; yanlış CIK
    tak = veri_kalitesi.abd_islem_gunleri("2023-01-01", "2023-12-31")
    if not (len(tak) == 250 and pd.Timestamp("2023-07-04") not in tak and pd.Timestamp("2023-04-07") not in tak and pd.Timestamp("2023-06-19") not in tak and pd.Timestamp("2023-01-02") not in tak and pd.Timestamp("2022-12-30") in veri_kalitesi.abd_islem_gunleri("2022-12-26", "2022-12-31")):
        hata.append(f"3a) ABD işlem takvimi yanlış: {len(tak)} gün")
    tz = veri_kalitesi.abd_islem_gunleri("2018-01-01", "2018-12-31"); t22 = veri_kalitesi.abd_islem_gunleri("2021-12-27", "2022-01-07")
    if pd.Timestamp("2018-12-05") in tz or len(tz) != 251 or pd.Timestamp("2022-01-03") not in t22 or pd.Timestamp("2021-12-31") not in t22 or pd.Timestamp("2023-01-02") in veri_kalitesi.abd_islem_gunleri("2023-01-01", "2023-01-05"):
        hata.append(f"3a2) özel kapanış / yılbaşı cumartesi kuralı yanlış: {len(tz)} {list(t22.date)}")
    def seri_tak(n=400, bas="2022-01-03"):
        g = veri_kalitesi.abd_islem_gunleri(bas, pd.Timestamp(bas) + pd.Timedelta(days=int(n * 1.6)))[:n]; d = _seri(n); d.index = g; return d
    temiz = seri_tak(); q0 = veri_kalitesi.sembol_kalite("T", temiz)
    if not (q0["kullanilabilir"] and q0["eksik_islem_gunu"] == 0 and q0["takvim_disi_satir"] == 0 and q0["veri_hatasi"] == "" and q0["veri_yetersiz"] == ""):
        hata.append(f"3b) temiz seri (tatiller dahil aralık) kullanılabilir değil: {q0['veri_hatasi']} {q0['veri_yetersiz']} eksik {q0['eksik_islem_gunu']}")
    ds = temiz.iloc[::-1]; qs = veri_kalitesi.sembol_kalite("S", ds)                                   # sırasız
    dy = pd.concat([temiz, temiz.iloc[[100]]]); qy = veri_kalitesi.sembol_kalite("Y", dy)              # yinelenen işlem günü
    dtz = temiz.copy(); dtz.index = dtz.index.tz_localize("UTC") + pd.Timedelta(hours=21); qtz = veri_kalitesi.sembol_kalite("Z", dtz)   # saat dilimi (21:00 UTC = 17:00 NY aynı gün)
    do = temiz.drop(columns=["High"]); qo = veri_kalitesi.sembol_kalite("O", do)                        # eksik OHLC sütunu
    dn = temiz.copy(); dn.iloc[50, dn.columns.get_loc("Close")] = np.nan; qn = veri_kalitesi.sembol_kalite("N", dn)
    dz = temiz.copy(); dz.iloc[10:110, dz.columns.get_loc("Volume")] = 0; qz = veri_kalitesi.sembol_kalite("ZV", dz)   # sıfır hacim %25
    de = temiz.copy(); de.iloc[10:110, de.columns.get_loc("Volume")] = np.nan; qe = veri_kalitesi.sembol_kalite("EV_", de)  # eksik hacim
    dneg = temiz.copy(); dneg.iloc[20, dneg.columns.get_loc("Low")] = -1.0; dneg.iloc[21, dneg.columns.get_loc("High")] = dneg.Close.iloc[21] * 0.5; qneg = veri_kalitesi.sembol_kalite("NEG", dneg)
    dsp = temiz.copy(); dsp.iloc[200:, dsp.columns.get_loc("Close")] /= 4; dsp.iloc[200:, dsp.columns.get_loc("Open")] /= 4; dsp.iloc[200:, dsp.columns.get_loc("High")] /= 4; dsp.iloc[200:, dsp.columns.get_loc("Low")] /= 4
    dsp.iloc[200:, dsp.columns.get_loc("Volume")] *= 4; qsp = veri_kalitesi.sembol_kalite("SP", dsp)                                      # 4:1 bölünme benzeri
    qsp_k = veri_kalitesi.sembol_kalite("SPK", dsp, kurumsal=pd.DataFrame({"tarih": [dsp.index[200]], "oran": [4]}))                     # kurumsal veriyle kesin
    dh = temiz.copy(); dh.iloc[300, dh.columns.get_loc("Close")] *= 2.2; dh.iloc[300, dh.columns.get_loc("High")] = dh.Close.iloc[300] * 1.01; dh.iloc[300, dh.columns.get_loc("Volume")] *= 8
    qh = veri_kalitesi.sembol_kalite("H", dh)                                                           # sert haber (High tutarlı; ertesi gün dönüş açıklanamayan)
    dg = temiz.drop(temiz.index[150:156]); qg = veri_kalitesi.sembol_kalite("G", dg)                   # altı işlem günü boşluk
    kontrol = {"sirasiz": qs["sirasiz"] == 1 and qs["eksik_islem_gunu"] == 0, "yinelenen": qy["yinelenen_islem_gunu"] == 1 and "yinelenen_islem_gunu" in qy["veri_hatasi"],
               "saat_dilimi": qtz["saat_dilimli"] and qtz["yinelenen_islem_gunu"] == 0 and qtz["eksik_islem_gunu"] == 0 and qtz["takvim_disi_satir"] == 0,
               "sutun": qo["sutun_eksik"] == 1 and "High" in qo["sutun_eksik_liste"] and not qo["kullanilabilir"], "nan": qn["nan_fiyat"] == 1 and "nan_fiyat" in qn["veri_hatasi"],
               "sifir_hacim": qz["sifir_hacim_sayi"] == 100 and qz["sifir_hacim_pay_yuksek"] == 1 and qz["eksik_hacim_sayi"] == 0, "eksik_hacim": qe["eksik_hacim_sayi"] == 100 and qe["sifir_hacim_sayi"] == 0 and qe["eksik_hacim_pay_yuksek"] == 1,
               "negatif": qneg["sifir_negatif_fiyat"] == 1 and qneg["ohlc_high_dusuk"] == 1, "bolunme": qsp["muhtemel_bolunme"] == 1 and qsp["kesin_bolunme"] == 0 and qsp_k["kesin_bolunme"] == 1,
               "haber": qh["sert_haber_hareketi"] == 1 and qh["getiri_100_ustu_sayi"] == 1 and qh["veri_hatasi"] == "" and "sert_haber_hareketi" in qh["piyasa_davranisi"],
               "bosluk": qg["bosluk_sayi"] == 1 and qg["en_uzun_bosluk"] == 6 and qg["ciddi_bosluk_sayi"] == 1 and "ciddi_bosluk_sayi" in qg["veri_yetersiz"]}
    kalan = [k for k, v in kontrol.items() if not v]
    if kalan:
        hata.append(f"3c) veri kalitesi vakaları yanlış: {kalan}")
    # orijinal değişmedi
    if not (ds.index[0] > ds.index[-1] and dtz.index.tz is not None):
        hata.append("3d) orijinal seri değiştirildi")
    # evren düzeyi: EV'de olup V'de olmayan sembol, yanlış CIK, bir CIK iki sembol, NaN sektör, 'False' metni, V'de fazla
    EV3 = pd.DataFrame({"sembol": ["AAA", "BBB", "CCC", "DDD"], "kaynak": "V_ABD", "sinif": [1, 1, 1, 4], "alt": ["", "", "", "4b kod"], "seri_sonu": ["k51", "k51", "k51", "kes"], "cik": [100, 100, -5, np.nan],
                        "sec_ad": ["A", "B", np.nan, "D"], "sektor": ["Tek", np.nan, "nan", "Fin"], "seri_erken": ["False", "True", "belki", False]})
    V3 = {"AAA": temiz, "BBB": temiz, "DDD": temiz, "FAZLA": temiz}
    Q3, oz3 = veri_kalitesi.evren_kalite(V3, EV3)
    if not (len(Q3) == 4 and oz3["fiyat_yok"] == 1 and oz3["v_fazla"] == 1 and oz3["v_fazla_liste"] == ["FAZLA"] and oz3["cik_coklu_sembol"] == 2 and oz3["cik_gecersiz"] == 1 and oz3["cik_bos"] == 1
            and oz3["sektor_bilinen"] == 2 and oz3["sektor_bos"] == 2 and oz3["seri_erken"] == 1 and oz3["seri_erken_gecersiz"] == 1 and oz3["sinif_4b"] == 1 and oz3["kesilmis_k54"] == 1 and oz3["sec_ad_bos"] == 1
            and Q3.set_index("sembol").loc["CCC", "fiyat_yok"] == 1):
        hata.append(f"3e) evren düzeyi kalite yanlış: {{k: oz3[k] for k in ('fiyat_yok', 'v_fazla', 'cik_coklu_sembol', 'cik_gecersiz', 'cik_bos', 'sektor_bilinen', 'sektor_bos', 'seri_erken', 'seri_erken_gecersiz', 'sinif_4b', 'kesilmis_k54', 'sec_ad_bos')}}")
    # 4) kesme testi: D01-S01 geçer, geleceğe bakan değişken kalır
    k1 = sizinti.kesme_testi(hucreler.d01_s01_dip_band_gun, d, [300, 400, 599]); k2 = sizinti.kesme_testi(sizinti.gelecek_degisken, d, [300, 400])
    if not (k1["gecti"] and not k2["gecti"]):
        hata.append(f"4) kesme testi yanlış: {k1} {k2}")
    # 4b) olay etiketi testi: pencere dışı değişiklik etiketi değiştirmez, pencere içi değiştirir
    et = sizinti.olay_etiketi_testi(d, lk, 300)
    if not et["gecti"]:
        hata.append(f"4b) olay etiketi testi yanlış: {et}")
    # 5) istatistik
    rng = np.random.default_rng(5); a = rng.normal(0.5, 1, 4000); b = rng.normal(0, 1, 4000)
    dd = istatistik.cohen_d(a, b); au = istatistik.auc(a, b)
    hp = istatistik.holm([0.01, 0.04, 0.03]); q_, ret = istatistik.bh_fdr([0.001, 0.01, 0.5, 0.2], 0.10)
    x = np.concatenate([rng.normal(0, 1, 400), rng.normal(2.5, 1, 100)]); cp = istatistik.cusum(x, 4.0, 250)
    m, lo, hi = istatistik.boot_kume(a, np.arange(4000) // 100, 500, rng)
    if not (0.4 < dd < 0.6 and 0.6 < au < 0.7 and abs(hp[0] - 0.03) < 1e-12 and abs(hp[1] - 0.06) < 1e-12 and abs(hp[2] - 0.06) < 1e-12 and ret.tolist() == [True, True, False, False]
            and len(cp) and any(400 <= i <= 415 and y == 1 for i, y in cp) and not any(i < 400 and y == 1 for i, y in cp) and lo < m < hi and abs(m - a.mean()) < 1e-9):
        hata.append(f"5) istatistik yanlış: d {dd:.3f} auc {au:.3f} holm {hp} fdr {ret} cusum {cp[:2].tolist() if len(cp) else cp} boot {m:.3f} [{lo:.3f},{hi:.3f}]")
    # 6) eşleştirme: aynı gün, aynı vd / lt / trend / rejim / sektör, |dd250| <= 0,10, hisse farklı; en yakın k = 2
    gun = pd.Timestamp("2020-03-02"); kol = ["tarih", "sembol", "vd", "lt", "trend", "rejim", "sektor", "dd250", "vol60", "log_dv20", "r60", "ar20", "r60_ileri", "mal"]
    H = pd.DataFrame([[gun, "A", 3, 1, 1, "BOGA", "tek", -0.30, 0.30, 14.0, 0.0, 1.0, 0.10, 0.01], [gun, "B", 3, 1, 1, "BOGA", "tek", -0.31, 0.31, 14.1, 0.0, 1.0, 0.20, 0.01],
                      [gun, "C", 3, 1, 1, "BOGA", "tek", -0.32, 0.32, 14.2, 0.0, 1.0, 0.30, 0.01], [gun, "D", 3, 1, 1, "BOGA", "tek", -0.90, 0.30, 14.0, 0.0, 1.0, 9.0, 0.01],
                      [gun, "E", 4, 1, 1, "BOGA", "tek", -0.30, 0.30, 14.0, 0.0, 1.0, 9.0, 0.01], [gun, "F", 3, 1, 1, "BOGA", "baska", -0.30, 0.30, 14.0, 0.0, 1.0, 9.0, 0.01]], columns=kol)
    H = pd.concat([H, H.assign(tarih=gun + pd.Timedelta(days=90), sembol=H.sembol + "2")], ignore_index=True)
    M = eslestirme.eslestir(H, H.iloc[[0]], H, k=2, gun_tol=0)       # tolerans 0: havuzda yalnız iki tarih var (90 gün ara = 1 indeks)
    if not (M.kontrol_n.iloc[0] == 2 and set(x.split("@")[0] for x in M.kontrol_kimlik.iloc[0].split(";")) == {"B", "C"} and abs(M.kontrol_r60_ileri.iloc[0] - 0.25) < 1e-9):
        hata.append(f"6) eşleştirme yanlış: {M.to_dict('records')}")
    if not sizinti.eslesme_testi(pd.concat([H.iloc[[0]], M], axis=1), H, gun_tol=0)["gecti"]:
        hata.append("6b) eşleşme sızıntı testi yanlış")
    # 7) örneklem seçimi ve daraltma: tabakalı, tohumlu, tekrar üretilebilir
    EV = pd.DataFrame({"sembol": [f"S{i}" for i in range(400)], "kaynak": ["V_ABD"] * 200 + ["K34_yahoo"] * 100 + ["K34_tiingo"] * 100,
                       "sinif": [1] * 300 + [2] * 30 + [3] * 40 + [5] * 20 + [4] * 10})
    EV["lik_uclu"] = (np.arange(len(EV)) % 3)
    o1, d1 = ornek_sec(EV, 50, 7); o2, _ = ornek_sec(EV, 50, 7); V7 = {s: 1 for s in EV.sembol}; V7d, EVd = evren_daralt(V7, EV, o1)
    if not (len(o1) == 50 and o1.sembol.is_unique and o1.sembol.tolist() == o2.sembol.tolist() and (o1.sinif == 2).sum() == 4 and (o1.kaynak == "V_ABD").sum() == 30 and len(V7d) == 50 and len(EVd) == 50 and d1.eksik.sum() == 0):
        hata.append(f"7) örneklem seçimi yanlış: {len(o1)} {o1.sinif.value_counts().to_dict()} {o1.kaynak.value_counts().to_dict()}")
    # 8) veri paketi: paketle -> aç -> sha256 aynı; bozuk parça -> durur; beklenen sha farklı -> durur
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "a.json"); open(src, "w").write('{"x": ' + "1" * 200000 + "}")
        man = veri_paket.paketle({"a.json": {"yol": src, "kaynak": "test", "indirme_tarihi": "2026-10-30", "donem": "-", "surum": "1", "isleme_kodu": "t", "tur": "islenmis"}}, os.path.join(tmp, "p"))
        ac = veri_paket.ac(os.path.join(tmp, "p"), os.path.join(tmp, "o")); ok8 = ortak.sha256_dosya(ac["a.json"]["yol"]) == man["veri"]["a.json"]["sha256"] and ac["a.json"]["meta"]["kaynak"] == "test"
        try:
            veri_paket.ac(os.path.join(tmp, "p"), os.path.join(tmp, "o2"), {"a.json": "0" * 64}); ok8 = False
        except RuntimeError:
            pass
        parca = os.path.join(tmp, "p", "a.json.xz.000"); b_ = bytearray(open(parca, "rb").read()); b_[10] ^= 0xFF; open(parca, "wb").write(bytes(b_))
        try:
            veri_paket.ac(os.path.join(tmp, "p"), os.path.join(tmp, "o3")); ok8 = False
        except RuntimeError:
            pass
        if not ok8:
            hata.append("8) veri paketi doğrulaması yanlış")
    # 9) hücre motoru A: sentetik panelde olumlu kontrol (x = gürültü + 2·olay) büyük d, olumsuz (gürültü) küçük d
    rng = np.random.default_rng(9); gunler = pd.bdate_range("2018-01-01", periods=40); rows = []
    for g in gunler:
        for j in range(120):
            rows.append({"tarih": g, "sembol": f"S{j}", "vd": j % 10, "lt": j % 3, "trend": 1, "rejim": "BOGA", "sektor": "tek", "likit": True, "r60_tanimli": True, "olay": (j % 7 == 0)})
    P9 = pd.DataFrame(rows); P9["ay"] = P9.tarih.dt.to_period("M").astype(str); P9["ceyrek"] = P9.tarih.dt.to_period("Q").astype(str); P9["donem"] = "KESIF"; P9["donem60"] = "KESIF"; P9["blok60"] = 0
    P9["x_pos"] = rng.normal(0, 1, len(P9)) + 2.0 * P9.olay; P9["x_neg"] = rng.normal(0, 1, len(P9))
    O9 = P9[P9.olay][["sembol", "tarih"]].assign(ufuk="Y60", i=0, donem="KESIF")
    ra = hucre.yontem_A(P9, O9, "x_pos", "Y60", rng, "KESIF"); rb = hucre.yontem_A(P9, O9, "x_neg", "Y60", rng, "KESIF")
    if not (ra["d"] > 1.5 and ra["auc"] > 0.85 and ra["karar"] == "ETKİ" and abs(rb["d"]) < 0.15 and rb["karar"] == "ETKİ YOK" and ra["n_olay"] == 40 * 18):
        hata.append(f"9) hücre A kontrolleri yanlış: {ra['d']:.2f} {ra['auc']:.2f} {ra['karar']} | {rb['d']:.2f} {rb['karar']}")
    # 10) dönem etiketi ve slot portföyü
    de = ortak.donem_etiketi(pd.Series(pd.to_datetime(["2015-06-01", "2016-01-01", "2021-12-31", "2022-06-01", "2024-01-01", "2026-06-05", "2026-06-06", "2026-09-01"])))
    if de.tolist() != ["DISI", "KESIF", "KESIF", "IC_DOGRULAMA", "BAGIMSIZ", "BAGIMSIZ", "DISI", "ILERI"]:
        hata.append(f"10) dönem etiketi yanlış: {de.tolist()}")
    sinyal = pd.DataFrame({"tarih": gunler[:5].repeat(3), "sembol": [f"S{i}" for i in range(15)], "vd": [0] * 15, "net": [0.10] * 15})
    havuz = pd.DataFrame({"tarih": gunler[:5].repeat(20), "sembol": [f"H{i}" for i in range(100)], "vd": [0] * 100, "net": [0.0] * 100})
    sp = istatistik.slot_portfoy(sinyal, havuz, rng, slot=10, gun_tut=60, gunde=2, R=50)
    if not (sp["n_islem"] == 10 and abs(sp["ort_net"] - 0.10) < 1e-9 and sp["rastgele_yuzdelik"] == 1.0):
        hata.append(f"10b) slot portföyü yanlış: {sp}")
    # 11) dönem etiketi kenarları: gün sonu damgası bitiş gününe dahil, saat dilimli damga yerel güne indirgenir, NaT -> DISI
    t11 = pd.Series([pd.Timestamp("2021-12-31 23:59:59"), pd.Timestamp("2021-12-31 23:00", tz="UTC"), pd.NaT, pd.Timestamp("2026-06-05 16:00"), pd.Timestamp("2022-01-01 00:00:01")])
    e11a = ortak.donem_etiketi(t11.iloc[[0, 2, 3, 4]]).tolist(); e11b = ortak.donem_etiketi(t11.iloc[[1]]).tolist()
    if not (e11a == ["KESIF", "DISI", "BAGIMSIZ", "IC_DOGRULAMA"] and e11b == ["KESIF"]):
        hata.append(f"11) dönem etiketi kenarları yanlış: {e11a} {e11b}")
    # 12) purge / embargo: pencere dönem sınırını aşan -> PURGE; dönem başındaki 14 takvim günü -> EMBARGO; bitis NaT -> TANIMSIZ; PURGE_GUN = 250
    t12 = pd.Series(pd.to_datetime(["2021-10-01", "2021-10-01", "2021-06-01", "2022-01-05", "2022-02-01", "2016-01-10"]))
    b12 = pd.Series(pd.to_datetime(["2022-02-15", "2021-12-30", None, "2022-04-10", "2022-05-01", "2016-04-15"]))
    e12 = ortak.donem_etiketi_ufuk(t12, b12).tolist()
    if not (e12 == ["PURGE", "KESIF", "TANIMSIZ", "EMBARGO", "IC_DOGRULAMA", "EMBARGO"] and ortak.PURGE_GUN == 250 and ortak.EMBARGO_GUN == 10):
        hata.append(f"12) purge / embargo etiketi yanlış: {e12} {ortak.PURGE_GUN}")
    # 13) koşu kimliği: kilit sha boşsa durur; eksik veri dosyası durur; çıkış yolu denetimi (yasak / izinsiz / izinli)
    A13 = ortak.K55Ayar(veri="/nonexistent_13", cikti=os.path.join(ortak.KOK, "arastirma_cikti", "k55_dallanma", "deneme"))
    ok13 = True
    try:
        ortak.veri_sha(A13); ok13 = False
    except FileNotFoundError:
        pass
    eski = ortak.onkayit_sha
    try:
        ortak.onkayit_sha = lambda: ""
        try:
            ortak.kosu_kimligi(A13, "x", None, {}); ok13 = False
        except RuntimeError:
            pass
    finally:
        ortak.onkayit_sha = eski
    for yasak in (os.path.join(ortak.KOK, "arastirma_cikti", "col_yolu_abd"), "/tmp/k55_baska", os.path.join(ortak.KOK, "arastirma_cikti", "k55_dallanma", "..", "col_yolu_abd")):
        try:
            ortak.cikti_dogrula(yasak); ok13 = False
        except PermissionError:
            pass
    if not (ok13 and ortak.cikti_dogrula(A13.cikti).endswith("k55_dallanma/deneme") and ortak.ayar_sha() and len(ortak.kod_dosyalari()) >= 15):
        hata.append("13) koşu kimliği / çıkış yolu denetimi yanlış")
    # 14) COL_YOLU_ABD içe aktarma yan etkisiz: ağ kapalı, K51-K54 çıktı dosyalarının sha256'sı aynı, yeni dosya yok
    import socket
    kl = os.path.join(ortak.KOK, "arastirma_cikti", "col_yolu_abd"); dosyalar = sorted(f for f in os.listdir(kl) if f.endswith((".md", ".csv", ".json"))) if os.path.isdir(kl) else []
    once = {f: ortak.sha256_dosya(os.path.join(kl, f)) for f in dosyalar[:40]}; eski_sock = socket.socket.connect
    def _yasak(*a, **k):
        raise RuntimeError("test: ağ kapalı")
    socket.socket.connect = _yasak
    try:
        sys.modules.pop("COL_YOLU_ABD", None); C = ortak.cy(); _ = C.CY_SURUM
    finally:
        socket.socket.connect = eski_sock
    sonra = {f: ortak.sha256_dosya(os.path.join(kl, f)) for f in dosyalar[:40]}; yeni = sorted(f for f in os.listdir(kl) if f.endswith((".md", ".csv", ".json"))) if os.path.isdir(kl) else []
    if not (once == sonra and yeni == dosyalar):
        hata.append("14) COL_YOLU_ABD içe aktarması yan etkili (dosya değişti ya da yeni dosya)")
    # 15) çoklu test özeti: hücre içi Holm, aile içi BH; test yükü sayımı
    R15 = pd.DataFrame({"hucre": ["H1", "H1", "H2", "H3"], "dal": "D01", "yontem": "A", "donem": "KESIF", "p": [0.001, 0.02, 0.5, 0.04]})
    Rc, yuk = istatistik.coklu_test_ozeti(R15, 0.10)
    if not (yuk.test.iloc[0] == 4 and yuk.hucre.iloc[0] == 3 and bool(Rc[Rc.hucre == "H1"].ret.iloc[0]) and not bool(Rc[Rc.hucre == "H2"].ret.iloc[0]) and abs(Rc[Rc.hucre == "H1"].p_holm.iloc[0] - 0.002) < 1e-12):
        hata.append(f"15) çoklu test özeti yanlış: {yuk.to_dict('records')} {Rc[['hucre', 'p_holm', 'q_bh', 'ret']].to_dict('records')}")
    # ---------------- 16-26) evren inşası (saf) sentetik vakalar (Cemal, 30 Eki): K54 sınıfı yok, yinelenen sembol, 'False' metni, boş çıkış işlemi,
    # kesim tarihi olmayan 4b, kesim günü işlem günü olmayan 4b, fiyat serisi olmayan sembol, kısa seri, iki tabakada aynı sembol, eksik tabaka, ağ çağrısı
    def seri(n, bas="2018-01-01"):
        return _seri(n, tohum=n, bas=bas)
    idx = pd.bdate_range("2018-01-01", periods=600); kes_gun = idx[400]; kes_tatil = kes_gun + pd.Timedelta(days=(5 - kes_gun.weekday()) % 7 or 6)   # bir hafta sonu
    V16 = {"AAA": seri(600), "BBB": seri(600), "CCC": seri(600), "DDD": seri(600), "EEE": seri(600), "FFF": seri(600), "GGG": seri(600), "HHH": seri(600), "KSA": seri(600), "ZZZ": seri(600)}
    EV16 = pd.DataFrame({"pazar": "ABD", "sembol": list(V16), "kaynak": "V_ABD", "evren_bas": pd.Timestamp("2018-01-01"), "batan": False, "agirlik": 1.0})
    EV16 = pd.concat([EV16, pd.DataFrame([{"pazar": "ABD", "sembol": "YOK", "kaynak": "V_ABD", "evren_bas": pd.Timestamp("2018-01-01"), "batan": False, "agirlik": 1.0}])], ignore_index=True)   # serisi yok
    SD16 = pd.DataFrame([
        {"sembol": "AAA", "sinif": 1, "alt": "", "cikis_islemi": "y", "kesim_tarihi": "", "erken_bitti": "False"},
        {"sembol": "BBB", "sinif": 2, "alt": "", "cikis_islemi": "y_d100", "kesim_tarihi": "", "erken_bitti": "True"},
        {"sembol": "CCC", "sinif": 3, "alt": "", "cikis_islemi": "", "kesim_tarihi": "", "erken_bitti": "True"},                       # boş çıkış işlemi -> belirsiz
        {"sembol": "DDD", "sinif": 4, "alt": "4b kod yeniden kullanımı", "cikis_islemi": "y_kes", "kesim_tarihi": "", "erken_bitti": "False"},   # kesim yok -> tutarsız
        {"sembol": "EEE", "sinif": 4, "alt": "4b kod yeniden kullanımı", "cikis_islemi": "y_kes", "kesim_tarihi": str(kes_tatil.date()), "erken_bitti": "False"},   # kesim hafta sonu
        {"sembol": "FFF", "sinif": 4, "alt": "4b kod yeniden kullanımı", "cikis_islemi": "y_kes", "kesim_tarihi": str(kes_gun.date()), "erken_bitti": "False"},
        {"sembol": "GGG", "sinif": 6, "alt": "", "cikis_islemi": "y", "kesim_tarihi": "", "erken_bitti": "False"},
        {"sembol": "HHH", "sinif": 5, "alt": "", "cikis_islemi": "y", "kesim_tarihi": "", "erken_bitti": "belki"},                  # geçersiz boolean -> tutarsız
        {"sembol": "KSA", "sinif": 1, "alt": "", "cikis_islemi": "y", "kesim_tarihi": "", "erken_bitti": "False"},
        {"sembol": "KSA", "sinif": 1, "alt": "", "cikis_islemi": "y", "kesim_tarihi": "", "erken_bitti": "False"},                  # yinelenen sembol
        {"sembol": "YOK", "sinif": 1, "alt": "", "cikis_islemi": "y", "kesim_tarihi": "", "erken_bitti": "False"},
    ])                                                                                                                                # ZZZ: K54'te yok
    ES16 = pd.DataFrame({"sembol": list(V16) + ["YOK"], "cik": [1, 2, 3, 4, 5, 6, 7, 8, 9, np.nan, 11], "sec_ad": "x"})
    # 22) fiyat serisi bulunmayan sembol (EV'de var, V'de yok) -> durur
    try:
        evm.evren_insa(V16, EV16, SD16, ES16, {"UUP"}); hata.append("22) serisi olmayan EV sembolü durdurmadı")
    except RuntimeError:
        pass
    EV16b = EV16[EV16.sembol != "YOK"]; kisa16 = pd.DataFrame([{"sembol": "KIS", "kaynak": "V_ABD", "n_gun": 100}]); eksik16 = pd.DataFrame([{"sembol": "TNG", "ayrinti": "Tiingo dosyası yok"}])
    R16 = evm.evren_insa(V16, EV16b, SD16, ES16, {"UUP"}, kisa16, eksik16); EVr = R16["EV"].set_index("sembol"); D16 = R16["disi"]; kat = dict(zip(D16.sembol, D16.kategori))
    # 16) K54 sınıfı olmayan (ZZZ) -> k54_yok; 17) yinelenen (KSA) -> k54_tutarsiz; 18) 'False' metni False; 19) boş çıkış işlemi (CCC) -> cikis_belirsiz
    # 20) kesim tarihi olmayan 4b (DDD) -> k54_tutarsiz; 21) hafta sonu kesim (EEE) etkin kesim son işlem günü; FFF kesim satır sayıları; GGG sınıf 6; HHH geçersiz boolean
    bek = {"ZZZ": "k54_yok", "KSA": "k54_tutarsiz", "CCC": "cikis_belirsiz", "DDD": "k54_tutarsiz", "GGG": "sinif6", "HHH": "k54_tutarsiz", "KIS": "kisa_seri_yukleyici", "TNG": "veri_saglayici_eksik", "UUP": "fon_evren_disi", "ZZZ": "k54_yok"}
    yanlis = {k: kat.get(k) for k, v in bek.items() if kat.get(k) != v}
    if yanlis:
        hata.append(f"16-20) dışlama kategorileri yanlış: {yanlis}")
    if not (set(EVr.index) == {"AAA", "BBB", "EEE", "FFF"} and EVr.loc["AAA", "erken_bitti_k54"] is False or EVr.loc["AAA", "erken_bitti_k54"] == False):
        hata.append(f"18) evren üyeleri / boolean yanlış: {sorted(EVr.index)} {EVr.loc['AAA', 'erken_bitti_k54']!r}")
    KS = R16["kesim"].set_index("sembol")
    if not (len(R16["V"]["FFF"]) == 401 and KS.loc["FFF", "once"] == 600 and KS.loc["FFF", "sonra"] == 401 and KS.loc["FFF", "atilan"] == 199 and bool(KS.loc["FFF", "kesim_islem_gunu"])
            and not bool(KS.loc["EEE", "kesim_islem_gunu"]) and R16["V"]["EEE"].index[-1] <= kes_tatil and (R16["V"]["EEE"].index > kes_tatil).sum() == 0 and EVr.loc["FFF", "seri_sonu_getiri"] == "k51"
            and EVr.loc["BBB", "seri_sonu"] == "d100" and R16["tutarlilik"]["gecti"]):
        hata.append(f"20-21) 4b kesimi yanlış: {KS.to_dict('index')}")
    if not (evm.bool_cevir("False") is False and evm.bool_cevir("true") is True and evm.bool_cevir("belki") is None and evm.bool_cevir(np.nan) is None and evm.bool_cevir(1) is True):
        hata.append("18b) bool_cevir yanlış")
    # 23) kısa seri eşiği: yükleyici 320 doğrulanır; 24) evren sürümü girdilere duyarlı
    try:
        evm.yukleyici_esigi_dogrula()
    except Exception as ex:
        hata.append(f"23) yükleyici eşiği doğrulanamadı: {ex}")
    s1 = evm.evren_surum(R16["EV"], {"a": "1"}, {"v": "1"}); s2 = evm.evren_surum(R16["EV"], {"a": "1"}, {"v": "2"}); s3 = evm.evren_surum(R16["EV"], {"a": "2"}, {"v": "1"})
    EV24 = R16["EV"].copy(); EV24.loc[0, "sinif"] = 5; s4 = evm.evren_surum(EV24, {"a": "1"}, {"v": "1"})
    if len({s1, s2, s3, s4}) != 4:
        hata.append("24) evren sürümü veri / dosya / sınıf değişimine duyarlı değil")
    # 25) örneklem: aynı sembol iki tabakaya uyabilir (lik_uclu eksik) -> tekrarsız; eksik tabaka raporlanır ve tamamlanır; boş aday hata vermez
    EV25 = pd.DataFrame({"sembol": [f"S{i}" for i in range(60)], "kaynak": ["V_ABD"] * 40 + ["K34_yahoo"] * 20, "sinif": [1] * 60})      # sınıf 2 / 3 / 4 / 5 yok
    o25, d25 = ornek_sec(EV25, 50, 3)
    if not (len(o25) == 50 and o25.sembol.is_unique and (d25.eksik > 0).sum() >= 4 and d25[d25.tabaka.str.startswith("tamamlama")].secilen.iloc[0] > 0 and d25.toplam_secilen.iloc[0] == 50):
        hata.append(f"25) örneklem eksik tabaka / tekrarsızlık yanlış: {d25.to_dict('records')}")
    o25b, d25b = ornek_sec(EV25.head(30), 50, 3)
    if not (len(o25b) == 30 and o25b.sembol.is_unique):
        hata.append("25b) evren n'den küçükken hepsi alınmadı")
    # 26) ağ erişimi gerektiren çağrı kapı içinde durur
    ok26 = False
    try:
        with evm.ag_kapali():
            import socket as _sk
            _sk.create_connection(("example.com", 80), timeout=1)
    except RuntimeError as ex:
        ok26 = "ağ erişimi yasak" in str(ex)
    except Exception:
        ok26 = False
    if not ok26:
        hata.append("26) ağ kapalı kapısı bağlantıyı durdurmadı")
    # 27) Faz 1 hücre tanımları: bütün kayıtlı hücreler (D01-D06, D10 sembol fonksiyonları) sentetik seride kesme testini geçer; NaN payı < %60
    from K55 import dal_ortak, faz1 as f1m
    f1m.hucreleri_kur(); n27 = 700; idx27 = pd.bdate_range("2017-01-02", periods=n27); d27 = _seri(n27, tohum=27); d27.index = idx27; d27.attrs["sektor"] = "Tek"
    spy = pd.Series(100 * np.exp(np.cumsum(np.random.default_rng(1).normal(0, 0.008, n27))), index=idx27)
    dal_ortak.EK.clear(); dal_ortak.EK.update({"SPY": spy, "IWM": spy * 1.1, "sektor_getiri": {"Tek": spy.pct_change()}, "lider_getiri": {"Tek": spy.pct_change()}, "sektor_of": {"X": "Tek"}})
    kalan27 = []; nan27 = []
    for kimlik, t in hucreler.HUCRELER.items():
        if t.get("panel_fonk") is not None:
            continue
        for pz in t["pencereler"]:
            f = t["fabrika"](pz) if (t.get("fabrika") is not None and pz is not None) else t["fonk"]
            r = sizinti.kesme_testi(f, d27, [400, 550, 699])
            if not r["gecti"]:
                kalan27.append(f"{kimlik}|{pz}")
            x = np.asarray(f(d27), float)
            if len(x) != n27 or np.isnan(x[400:]).mean() > 0.6:
                nan27.append(f"{kimlik}|{pz}")
    if kalan27 or nan27:
        hata.append(f"27) hücre tanımları: kesme testi kalan {kalan27}; NaN yüksek / uzunluk {nan27}")
    say27 = sum(1 for v in hucreler.HUCRELER.values())
    if say27 < 60:
        hata.append(f"27b) kayıtlı hücre sayısı az: {say27}")
    # 28) kesitsel bileşik (D10) ve panel fonksiyonları sentetik panelde çalışır; 29) hucre_kos bütün yöntem satırlarını üretir
    rng = np.random.default_rng(28); gunler = pd.bdate_range("2018-01-01", periods=30); semboller = [f"S{j}" for j in range(40)]; rows = []
    V28 = {}
    for j, sm in enumerate(semboller):
        dd = _seri(400, tohum=100 + j); dd.index = pd.bdate_range("2016-06-01", periods=400); dd.attrs["sektor"] = "Tek" if j % 2 else "Fin"; V28[sm] = dd
    for g in gunler:
        for j, sm in enumerate(semboller):
            i = int(V28[sm].index.get_indexer([g])[0]) if g in V28[sm].index else 300
            rows.append({"tarih": g, "sembol": sm, "i": i, "vd": j % 10, "lt": j % 3, "trend": 1, "rejim": "BOGA", "sektor": V28[sm].attrs["sektor"], "likit": True, "r60_tanimli": True, "r60_ileri": rng.normal(0, 0.1), "mal": 0.002,
                         "dv20": 1e6 * (j + 1), "r60": rng.normal(0, 0.1), "vol60": 0.3, "log_dv20": 14.0, "dd250": -0.2, "ar20": 1.0, "close": float(V28[sm].Close.get(g, 100.0))})
    P28 = pd.DataFrame(rows); P28["ay"] = P28.tarih.dt.to_period("M").astype(str); P28["ceyrek"] = P28.tarih.dt.to_period("Q").astype(str); P28["blok60"] = 0
    for h_ in (60, 120, 250):
        P28[f"donem{h_}"] = "KESIF"
    P28["donem"] = "KESIF"; P28 = P28.sort_values(["sembol", "tarih"]).reset_index(drop=True)
    O28 = P28.sample(60, random_state=1)[["sembol", "tarih", "i"]].assign(ufuk="Y60", donem="KESIF")
    for kb, pz in f1m.D10_BILESEN:
        P28[kb], _ = hucre.degisken_hesapla(P28, V28, hucreler.HUCRELER[kb], pz, kb)
    x28 = hucreler.HUCRELER["D10-S01"]["panel_fonk"](P28); x28b = hucreler.HUCRELER["D02-S10"]["fabrika"](20)(P28)
    if not (len(x28) == len(P28) and np.isfinite(x28).mean() > 0.5 and len(x28b) == len(P28)):
        hata.append(f"28) D10 / kesitsel panel fonksiyonu yanlış: {np.isfinite(x28).mean():.2f}")
    r29 = hucre.hucre_kos("D01-S02", hucreler.HUCRELER["D01-S02"], P28, V28, O28, np.random.default_rng(29), donemler=("KESIF",), ufuklar=("Y60",))
    y29 = pd.Series([r["yontem"] for r in r29]).value_counts().to_dict(); v29 = {r["varyant"] for r in r29}
    if not (y29.get("A") == 5 and y29.get("B") == 5 and y29.get("C") == 5 and len(v29) == 5 and all("karar" in r for r in r29) and "D01-S02|5" not in P28):
        hata.append(f"29) hucre_kos varyant / yöntem satırları yanlış: {y29} {sorted(v29)}")
    # 30) vekil kıyası (2.7): r60'ın kendisi olan değişken VEKİL (en yakın r60, |ρ| > 0,8); rastgele değişken vekil değil; seçim KEŞİF + not
    rng30 = np.random.default_rng(30); P30 = P28.copy()
    P30["r60"] = [float(V28[sm].Close.iloc[i] / V28[sm].Close.iloc[i - 60] - 1) for sm, i in zip(P30.sembol, P30.i)]
    P30["dd250"] = rng30.uniform(-0.6, 0, len(P30)); P30["likit"] = True
    hucreler.temizle()
    hucreler.kaydet("T-VEK", "T", "r60 kopyası", +1, lambda d: d.Close / d.Close.shift(60) - 1, not_="")
    hucreler.kaydet("T-RAST", "T", "rastgele", +1, lambda d: pd.Series(np.random.default_rng(int(d.Close.iloc[0] * 1000) % 2**31).normal(size=len(d)), index=d.index), not_="OBV vekil denetimi")
    hucreler.kaydet("T-DIS", "T", "seçilmez", +1, lambda d: d.Close * 0, not_="")
    D30 = pd.DataFrame([{"hucre": "T-VEK", "durum": "KEŞİF", "A_en_iyi": "T-VEK|tek", "B_en_iyi": "", "A_d": 0.3}, {"hucre": "T-RAST", "durum": "REDDEDİLDİ", "A_en_iyi": "", "B_en_iyi": "T-RAST|tek", "A_d": 0.0},
                        {"hucre": "T-DIS", "durum": "REDDEDİLDİ", "A_en_iyi": "T-DIS|tek", "B_en_iyi": "", "A_d": 0.0}])
    sec30 = vkm.hucre_sec(D30); T30 = vkm.vekil_kiyas(D30, P30, V28, O28, rng30)
    r_vek = T30[T30.hucre == "T-VEK"].iloc[0] if (T30.hucre == "T-VEK").any() else None; r_rast = T30[T30.hucre == "T-RAST"].iloc[0] if (T30.hucre == "T-RAST").any() else None
    if not (sec30 == ["T-VEK", "T-RAST"] and r_vek is not None and r_rast is not None and bool(r_vek.vekil) and r_vek.en_yakin_bilinen == "r60" and r_vek.rho_r60 > 0.95
            and not bool(r_rast.vekil) and abs(r_rast.en_yakin_rho) < 0.5 and "T-VEK|tek" not in P30 and all(f"rho_{b}" in T30 for b in vkm.BILINEN)):
        hata.append(f"30) vekil kıyası yanlış: seçim {sec30}; " + (f"VEK ρ_r60={r_vek.rho_r60:.2f} vekil={r_vek.vekil} en={r_vek.en_yakin_bilinen}; " if r_vek is not None else "VEK yok; ") + (f"RAST en ρ={r_rast.en_yakin_rho:.2f} vekil={r_rast.vekil}" if r_rast is not None else "RAST yok"))
    with tempfile.TemporaryDirectory() as td30:
        vkm.vekil_yaz(T30, {"kimlik": "test"}, td30)
        if "VEKİL işaretli hücre: 1" not in open(os.path.join(td30, "K55_VEKIL.md"), encoding="utf-8").read():
            hata.append("30b) K55_VEKIL.md vekil sayısı yanlış")
    hucreler.temizle(); dal_ortak.EK.clear(); hucreler.kaydet("D01-S01", "D01", "iskele", +1, hucreler.d01_s01_dip_band_gun)
    return hata


if __name__ == "__main__":
    h = testler()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_k55: 30/30 OK")
