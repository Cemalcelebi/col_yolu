"""K55 birim ve sentetik testler (Faz 0 madde 6). Gerçek veri gerekmez. Çalıştırma: python test_k55.py"""
from __future__ import annotations

import os
import sys
import tempfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from K55 import eslestirme, hucre, hucreler, istatistik, olay_tanimlari, ortak, sizinti, veri_kalitesi, veri_paket  # noqa: E402
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
    # 3) veri kalitesi: temiz seri eksiksiz; 10 iş günü boşluk; bölünme sıçraması
    q = veri_kalitesi.sembol_kalite("T", _seri(400))
    if not (q["eksiksiz"] and q["bosluk_sayi"] == 0 and q["sert_hareket_sayi"] == 0):
        hata.append(f"3a) temiz seri eksiksiz değil: {q}")
    db = _seri(400); db = db.drop(db.index[200:210]); qb = veri_kalitesi.sembol_kalite("B", db)
    ds = _seri(400); ds.iloc[250:, 3] = ds.Close.iloc[250:] / 2; ds.iloc[250:, 4] = ds.Volume.iloc[250:] * 3; qs = veri_kalitesi.sembol_kalite("S", ds)
    if not (qb["bosluk_sayi"] == 1 and qb["bosluk_max_gun"] == 10 and not qb["eksiksiz"] and qs["sert_hareket_sayi"] >= 1):
        hata.append(f"3b) boşluk / sıçrama tespiti yanlış: {qb['bosluk_sayi']} {qb['bosluk_max_gun']} {qs['sicrama_sayi']}")
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
    return hata


if __name__ == "__main__":
    h = testler()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_k55: 26/26 OK")
