"""K55 birim ve sentetik testler (Faz 0 madde 6). Gerçek veri gerekmez. Çalıştırma: python test_k55.py"""
from __future__ import annotations

import os
import sys
import tempfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from K55 import eslestirme, hucre, hucreler, istatistik, olay_tanimlari, ortak, sizinti, veri_kalitesi, veri_paket  # noqa: E402
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
    o1 = ornek_sec(EV, 50, 7); o2 = ornek_sec(EV, 50, 7); V7 = {s: 1 for s in EV.sembol}; V7d, EVd = evren_daralt(V7, EV, o1)
    if not (len(o1) == 50 and o1.sembol.tolist() == o2.sembol.tolist() and (o1.sinif == 2).sum() == 4 and (o1.kaynak == "V_ABD").sum() == 30 and len(V7d) == 50 and len(EVd) == 50):
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
    return hata


if __name__ == "__main__":
    h = testler()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_k55: 15/15 OK")
