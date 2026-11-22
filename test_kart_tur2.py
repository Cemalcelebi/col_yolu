"""KART_TUR2 testleri (yalnız SENTETİK veri; gerçek fiyat verisi okunmaz). Çalıştırma: python test_kart_tur2.py

1) çakışma kapısı  2) KASA durumu (KASA 2 mühürü, 2024Q1'den kesintisiz bloklar, bakış 4 / 8 / 12) ve tutarsız durumlar durur
3) KASA kapısı: V_*.pkl -> V_*2.pkl bağlantısı yoksa durur; veri en geç tarihi > açık kesik ise durur  4) çeyrek / hücre adları
5) k2_rh = OLCU_SINAMA.os_olcu_hesap 'R' (sentetik panel); açık dondurması yalnız giriş <= kesik ve çıkış > kesik hisse-günlerini siler
6) DS durum kopyası = DUSUS_SONRASI.ds_ozellik_hisse 's_ds'  7) D9 durum kopyası = KART_TUR1.kt_d9_durum (aynı pencerede); pencere 2000'e açılınca
   2015 öncesi satır gelir  8) hücre istatistiği (boot, SIRA boot, L3O, permütasyon) ve TUTAR yön simetrisi; bakış düzeyi daha geniş
9) plasebo çekimi: aynı gün, gün içinde tekrar yok  10) güç ara değeri  11) karar kuralı: İZ ADAYI, KATKI−, ABD-ADAY (AVR güçsüz), KT10
   ABD-ADAY, ETKİ YOK, ÖLÇÜLEMEDİ, SORGULA, BH düşer, plasebo düşer, alt dönem şartı, bakış dışı BİLGİ, kontrol kartı GÖRDÜ / GÖRMEDİ
12) sabitler (Bonferroni %98,33, q / 3, m 24, KART_TUR1 tanımları aynen)  13) Y1 bayrakları = YAPI_HEDEF Ş şartları; 6 anlamlı basamak
14) tablo sha'sı sıradan bağımsız, değere duyarlı  15) sızıntı taraması + kontrol tablosu IZ_KARNE kapısından geçer
16) önbellek yaz / oku: bozulursa ya da ön kayıt sha'sı tutmazsa durur  17) gerçek ön kayıt (varsa, işlenmişse) KASA 'ac' kapısından geçer
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
warnings.filterwarnings("ignore", category=RuntimeWarning)
import KART_TUR2 as K2  # noqa: E402
import KASA as KS  # noqa: E402
import OLCU_SINAMA as OS  # noqa: E402

MUHUR = json.load(open(K2.K2_YOL["manifest"], encoding="utf-8"))["muhur_id"]


def _durum(kl: str, kesik: str, acilan, muhur: str = MUHUR) -> None:
    os.makedirs(kl, exist_ok=True)
    json.dump({"acik_kesik": kesik, "acilan": list(acilan), "muhur_id": muhur}, open(os.path.join(kl, KS.KS_DURUM_AD), "w"))


def _seri(rng, idx, mu=0.0003, sd=0.02, fiyat=20.0):
    C = fiyat * np.exp(np.cumsum(rng.normal(mu, sd, len(idx))))
    O = C * (1 + rng.normal(0, 0.003, len(idx))); H = np.maximum(O, C) * 1.01; L = np.minimum(O, C) * 0.99
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(2 * 10 ** 5, 10 ** 6, len(idx)).astype(float),
                         "Kur": 1.0}, index=pd.DatetimeIndex(idx))


def _panel(n_hisse=45, bas="2015-06-01", son="2017-12-29", tohum=5):
    rng = np.random.default_rng(tohum); idx = pd.bdate_range(bas, son); V = {}
    for i in range(n_hisse):
        x = _seri(rng, idx, sd=0.01 + 0.002 * (i % 7))
        if i % 9 == 0:   # boşluklu hisse (2H kuralı)
            x = x.drop(x.index[300:330])
        V[f"S{i:03d}"] = x
    Vd = {"pazar": "ABD", "V": V, "gecersiz": {s: pd.DatetimeIndex([]) for s in V}, "not": []}
    Pn = OS.os_panel(Vd)
    return Vd, Pn


# ------------------------------------------------------------------ 1
def test_cakisma_kapisi():
    kaynak = open(os.path.join(KOK, "KART_TUR2.py"), encoding="utf-8").read()
    ns = {"__name__": "k2_test"}
    exec(compile(kaynak, "KART_TUR2.py", "exec"), ns)
    exec(compile(kaynak, "KART_TUR2.py", "exec"), ns)            # aynı dosya yeniden: geçer
    ns2 = {"__name__": "k2_test", "k2_olc": 1}
    exec(compile(kaynak, "KART_TUR2.py", "exec"), ns2)           # k2_ önekli ad: geçer
    ns3 = {"__name__": "k2_test", "KOK": "başka modülün adı", "_CK_KAYIT": {}}
    try:
        exec(compile(kaynak.replace("KOK_K2 = os.path", "KOK = 'ezen'\nKOK_K2 = os.path", 1), "KART_TUR2.py", "exec"), ns3)
    except RuntimeError as ex:
        assert "EZDİ" in str(ex)
    else:
        raise AssertionError("çakışma kapısı önek dışı adı ezmeye izin verdi")


# ------------------------------------------------------------------ 2
def test_durum_bloklar():
    with tempfile.TemporaryDirectory() as td:
        kl = os.path.join(td, "acik")
        _durum(kl, "2023-12-31", []); D = K2.k2_durum(kl); assert D["blok_sayi"] == 0 and D["bakis_no"] == 0
        _durum(kl, "2024-12-31", K2.k2_bloklar_beklenen(4)); assert K2.k2_durum(kl)["bakis_no"] == 1
        _durum(kl, "2025-12-31", K2.k2_bloklar_beklenen(8)); assert K2.k2_durum(kl)["bakis_no"] == 2
        _durum(kl, "2026-11-20", K2.k2_bloklar_beklenen(12)); assert K2.k2_durum(kl)["bakis_no"] == 3
        _durum(kl, "2024-06-30", K2.k2_bloklar_beklenen(2)); D = K2.k2_durum(kl); assert D["bakis_no"] == 0 and D["blok_sayi"] == 2
        for kes, ac, mh in (("2024-06-30", ["2024Q2"], MUHUR), ("2024-09-30", ["2024Q1", "2024Q2"], MUHUR), ("2024-03-31", [], MUHUR),
                            ("2023-12-31", ["2024Q1"], MUHUR), ("2023-12-31", [], "baska_muhur"), ("2022-12-31", [], MUHUR)):
            _durum(kl, kes, ac, mh)
            try:
                K2.k2_durum(kl)
            except K2.K2Hata:
                pass
            else:
                raise AssertionError(f"tutarsız durum geçti: {kes} {ac} {mh}")
        try:
            K2.k2_durum(td)
        except K2.K2Hata:
            pass
        else:
            raise AssertionError("durum dosyasız klasör geçti")


# ------------------------------------------------------------------ 3
def test_kasa_kapisi():
    rng = np.random.default_rng(3)
    with tempfile.TemporaryDirectory() as td:
        kl = os.path.join(td, "acik"); _durum(kl, "2023-12-31", [])
        for p in ("ABD", "AVR"):
            pd.to_pickle({"A": _seri(rng, pd.bdate_range("2023-01-03", "2023-12-29"))}, os.path.join(kl, f"V_{p}2.pkl"))
            os.symlink(os.path.join(kl, f"V_{p}2.pkl"), os.path.join(kl, f"V_{p}.pkl"))
        D = K2.k2_durum(kl); assert K2.k2_kasa(kl, D)["kesik"] == "2023-12-31"
        pd.to_pickle({"A": _seri(rng, pd.bdate_range("2023-01-03", "2024-01-05"))}, os.path.join(kl, "V_AVR2.pkl"))
        try:
            K2.k2_kasa(kl, D)
        except K2.K2Hata as ex:
            assert "KESİK AŞIMI" in str(ex)
        else:
            raise AssertionError("kesik aşımı geçti")
        os.remove(os.path.join(kl, "V_ABD.pkl")); pd.to_pickle({"A": _seri(rng, pd.bdate_range("2023-01-03", "2023-12-29"))},
                                                               os.path.join(kl, "V_ABD.pkl"))
        try:
            K2.k2_kasa(kl, D)
        except K2.K2Hata as ex:
            assert "bağlantı" in str(ex)
        else:
            raise AssertionError("bağlantısız V_ABD.pkl geçti")


# ------------------------------------------------------------------ 4
def test_ceyrek_hucre():
    assert [K2.k2_ceyrek(x) for x in ("2024-01-02", "2024-03-31", "2024-04-01", "2026-12-31")] == ["2024Q1", "2024Q1", "2024Q2", "2026Q4"]
    assert K2.k2_bloklar_beklenen(6) == ["2024Q1", "2024Q2", "2024Q3", "2024Q4", "2025Q1", "2025Q2"]
    h = K2.k2_hucre_adi(["2000-12-29", "2001-01-02", "2007-12-31", "2008-01-02", "2015-12-31", "2016-01-04", "2023-12-29", "2024-01-02"])
    assert list(h) == ["dis", "acik_d1", "acik_d1", "acik_d2", "acik_d2", "acik_d3", "acik_d3", "blok"]


# ------------------------------------------------------------------ 5
def test_rh_ve_dondurma():
    _, Pn = _panel()
    for H in (15, 30):
        R, X = K2.k2_rh(Pn, H, None)
        o = OS.os_olcu_matris(Pn, H)["R"]
        assert np.array_equal(np.isnan(R), np.isnan(o)) and np.nanmax(np.abs(R - o)) == 0.0
        kes = pd.Timestamp("2016-12-30"); Rd, _ = K2.k2_rh(Pn, H, kes)
        nd = int(Pn["tarih"].searchsorted(kes, side="right"))
        sil = np.isfinite(R) & ~np.isfinite(Rd)
        assert sil.any() and not sil[nd:].any()                         # giriş > kesik silinmez
        dd, jj = np.nonzero(sil); assert (X[dd, jj] >= nd).all()       # silinenlerin çıkışı kesikten sonra
        kal = np.isfinite(Rd[:nd]); dd, jj = np.nonzero(kal); assert (X[:nd][dd, jj] < nd).all()


# ------------------------------------------------------------------ 6
def test_ds_kopya():
    import DUSUS_SONRASI as DS
    rng = np.random.default_rng(6); idx = pd.bdate_range("2018-01-02", "2020-12-31"); V = {}
    for i in range(6):
        x = _seri(rng, idx, mu=-0.002 if i % 2 else 0.0005, sd=0.025, fiyat=8 + i)
        x["Volume"] = x.Volume * 5
        V[f"D{i}"] = x
    V["KISA"] = _seri(rng, idx[:90])
    for p in ("ABD", "AVR"):
        bag = DS.ds_baglam({"V": V, "pazar": p})
        n_ds = 0
        for s, x in V.items():
            _, _, sds = DS.ds_ozellik_hisse(x, p, bag, s, None, None)
            a = K2.k2_ds_durum_hisse(x, p); assert np.array_equal(a, sds.to_numpy(bool)); n_ds += int(a.sum())
        assert n_ds > 0
        assert K2.k2_ds_ornek_denetim(V, p, 4)["esit"] == 4


# ------------------------------------------------------------------ 7
def test_d9_kopya_pencere():
    import KART_TUR1 as KT
    sk = pd.read_csv(os.path.join(KOK, "sektor_ABD.csv")).dropna(subset=["endustri"])
    g = sk.groupby("endustri").sembol.apply(list); grp = [x for x in g if len(x) >= 8][:2]
    rng = np.random.default_rng(13); V = {}
    idx = pd.bdate_range("2013-01-02", "2017-12-29")
    for i, uy in enumerate(grp):
        for s in uy[:7]:
            d = _seri(rng, idx); d["Close"] *= np.exp(np.linspace(0, 0.8 * (i == 0), len(idx))); d["High"] = np.maximum(d.High, d.Close)
            d["Low"] = np.minimum(d.Low, d.Close); V[str(s).upper().replace(".AM", "")] = d
    Vd = {"V": V, "evren_bas": {}}
    import D9_YENIDEN as D9
    A = KT.kt_d9_durum(Vd, "ABD"); B = K2.k2_d9_durum(Vd, "ABD", D9.D9_ESIK["olay_bas"])
    pd.testing.assert_frame_equal(A.reset_index(drop=True), B.reset_index(drop=True))
    C = K2.k2_d9_durum(Vd, "ABD", K2.K2_ESIK["d9_olay_bas"])
    assert (pd.to_datetime(C.tarih) < pd.Timestamp("2015-06-01")).any() and len(C) > len(B)
    m = pd.to_datetime(C.tarih) >= pd.Timestamp(D9.D9_ESIK["olay_bas"])
    pd.testing.assert_frame_equal(C[m].reset_index(drop=True), B.reset_index(drop=True))


# ------------------------------------------------------------------ 8
def test_hucre_istatistik():
    rng = np.random.default_rng(8); n = 600; ay = rng.integers(0, 36, n)
    f = rng.normal(0.02, 0.05, n); s = np.clip(0.5 + f * 3 + rng.normal(0, 0.05, n), 0, 1)
    c = K2.k2_stat(f, s, ay, 1, perm=True)
    assert c["n"] == n and c["boot_alt98"] < c["boot_alt95"] < c["fark"] < c["boot_ust95"] < c["boot_ust98"]
    assert c["p_p"] < 0.01 and c["p_n"] > 0.99 and K2.k2_tutar(c, "+", False) and K2.k2_tutar(c, "+", True) and not K2.k2_tutar(c, "-", False)
    c2 = K2.k2_stat(-f, 1 - s, ay, 1, perm=True)
    assert K2.k2_tutar(c2, "-", False) and not K2.k2_tutar(c2, "+", False) and abs(c2["fark"] + c["fark"]) < 1e-15
    assert abs(c2["l3o_n"] + c["l3o_p"]) < 1e-12
    k = K2.k2_stat(f[:20], s[:20], ay[:20], 1); assert not K2.k2_tutar(k, "+", False)             # n < 30
    z = K2.k2_stat(np.where(np.arange(n) % 2, 0.03, -0.0299), np.full(n, 0.5), ay, 2); assert not K2.k2_tutar(z, "+", False)   # SIRA = 0,5
    q = np.quantile(f, [0.01, 0.99]); assert abs(c["kirp"] - f[(f >= q[0]) & (f <= q[1])].mean()) < 1e-15


# ------------------------------------------------------------------ 9
def test_plasebo_cekim():
    Vd, Pn = _panel()
    P2 = Pn["ok"] & (Pn["H"] >= 0)
    R, _ = K2.k2_rh(Pn, 15, None); hv = K2.K2Havuz(Pn, P2, R)
    rng = np.random.default_rng(9); d = np.repeat(np.arange(300, 340), 3)
    dd, jj = hv.cek_gun(d, rng)
    assert len(dd) == len(d) and np.array_equal(np.sort(dd), np.sort(d))
    assert len(set(zip(dd.tolist(), jj.tolist()))) == len(dd)
    assert (hv.KV[dd, jj] >= 0).all() and np.isfinite(R[dd, jj]).all()
    pl = K2.k2_plasebo(hv, d, False, "test"); assert set(pl) == {"plasebo_fark", "plasebo_pay_p", "plasebo_pay_n", "plasebo_gecti"}


# ------------------------------------------------------------------ 10
def test_guc_ara_deger():
    eg = [{"pazar": "ABD", "H": 15, "pencere": "1y", "n": n, "guc_0.01": g} for n, g in ((30, 0.1), (100, 0.4), (1000, 0.9))]
    assert K2.k2_guc(eg, "ABD", 15, "1y", 20) == 0.0 and K2.k2_guc(eg, "ABD", 15, "1y", 30) == 0.1
    assert abs(K2.k2_guc(eg, "ABD", 15, "1y", np.sqrt(100 * 1000)) - 0.65) < 1e-12 and K2.k2_guc(eg, "ABD", 15, "1y", 5000) == 0.9
    assert K2.k2_guc(eg, "AVR", 15, "1y", 500) == 0.0


# ------------------------------------------------------------------ 11
def _hc(over=None, acik_isaret=1.0):
    """Sentetik hücre tablosu: bütün kartlar x H x pazar x (acik_d1-3, birikimli); varsayılan nötr, güçlü."""
    sat = []
    for k, v in K2.K2_KART.items():
        for H in (15, 30):
            for P in v["pazar"]:
                for h in ("acik_d1", "acik_d2", "acik_d3", "birikimli"):
                    r = {"kod": k, "yon": v["yon"], "pazar": P, "ufuk": H, "hucre": h, "n": 500, "fark": 0.0, "sira": 0.5,
                         "boot_alt95": -0.004, "boot_ust95": 0.004, "boot_alt98": -0.005, "boot_ust98": 0.005, "p_p": 0.5, "p_n": 0.5,
                         "tutar_p": False, "tutar_n": False, "plasebo_gecti": True, "guc": 0.95}
                    if h.startswith("acik"):
                        r["fark"] = 0.001 * acik_isaret * (1 if v["yon"] == "+" else -1)
                    sat.append(r)
    H = pd.DataFrame(sat)
    for (k, h, P, U), d in (over or {}).items():
        m = (H.kod == k) & (H.hucre == h) & (H.pazar == P) & (H.ufuk == U)
        for c, x in d.items():
            H.loc[m, c] = x
    return H


def _iz(kod="KT03", yon="+"):
    s = 1 if yon == "+" else -1
    t = {"fark": 0.02 * s, "tutar_p": yon == "+", "tutar_n": yon == "-", "p_p": 0.0001 if yon == "+" else 0.9999,
         "p_n": 0.9999 if yon == "+" else 0.0001, "boot_alt98": 0.01 if yon == "+" else -0.03, "boot_ust98": 0.03 if yon == "+" else -0.01}
    o = {(kod, "birikimli", P, 15): t for P in ("ABD", "AVR")}
    o.update({(kod, "birikimli", P, 30): {"fark": 0.005 * s} for P in ("ABD", "AVR")})
    return o


def test_karar_kurali():
    D = {"blok_sayi": 4, "acilan": K2.k2_bloklar_beklenen(4), "bakis_no": 1}
    K = K2.k2_karar(_hc(_iz()), D).set_index("kod")
    assert K.loc["KT03", "etiket"] == "İZ ADAYI" and K.loc["KT01", "etiket"] == "ETKİ YOK"
    assert K.loc["KT00", "etiket"].startswith("KONTROL GÖRMEDİ")
    # ters yön
    K = K2.k2_karar(_hc(_iz("KT04", "-"), acik_isaret=-1.0), D).set_index("kod"); assert K.loc["KT04", "etiket"] == "KATKI−"
    # '-' kart (KT08): beklenen yönde İZ ADAYI
    K = K2.k2_karar(_hc(_iz("KT08", "-")), D).set_index("kod"); assert K.loc["KT08", "etiket"] == "İZ ADAYI"
    # plasebo düşerse TUT yok
    o = _iz(); o[("KT03", "birikimli", "AVR", 15)]["plasebo_gecti"] = False
    K = K2.k2_karar(_hc(o), D).set_index("kod"); assert K.loc["KT03", "etiket"] == "SORGULA"
    # alt dönem şartı: açık işaretler ters -> İZ ADAYI değil
    K = K2.k2_karar(_hc(_iz(), acik_isaret=-1.0), D).set_index("kod"); assert K.loc["KT03", "etiket"] != "İZ ADAYI"
    # öteki ufuk işareti ters -> değil
    o = _iz(); o[("KT03", "birikimli", "ABD", 30)] = {"fark": -0.001}
    K = K2.k2_karar(_hc(o), D).set_index("kod"); assert K.loc["KT03", "etiket"] != "İZ ADAYI"
    # BH düşer (p büyük)
    o = _iz(); o[("KT03", "birikimli", "ABD", 15)]["p_p"] = 0.2
    K = K2.k2_karar(_hc(o), D).set_index("kod"); assert K.loc["KT03", "etiket"] != "İZ ADAYI"
    # ABD-ADAY: yalnız ABD tutuyor, AVR güçsüz
    o = {k: v for k, v in _iz().items() if k[2] == "ABD"}
    o.update({("KT03", "birikimli", "AVR", U): {"n": 20, "guc": 0.1} for U in (15, 30)})
    K = K2.k2_karar(_hc(o), D).set_index("kod"); assert K.loc["KT03", "etiket"] == "ABD-ADAY"
    # yalnız ABD tutuyor ama AVR güçlü -> SORGULA
    o = {k: v for k, v in _iz().items() if k[2] == "ABD"}
    K = K2.k2_karar(_hc(o), D).set_index("kod"); assert K.loc["KT03", "etiket"] == "SORGULA"
    # KT10 (yalnız ABD) -> ABD-ADAY
    o = {k: v for k, v in _iz("KT10").items() if k[2] == "ABD"}
    K = K2.k2_karar(_hc(o), D).set_index("kod"); assert K.loc["KT10", "etiket"] == "ABD-ADAY"
    # ÖLÇÜLEMEDİ: güç yetersiz
    K = K2.k2_karar(_hc({("KT02", "birikimli", "AVR", 30): {"guc": 0.5}}), D).set_index("kod"); assert K.loc["KT02", "etiket"] == "ÖLÇÜLEMEDİ"
    # ETKİ YOK değil: aralık geniş -> SORGULA
    K = K2.k2_karar(_hc({("KT05", "birikimli", "ABD", 15): {"boot_alt98": -0.02}}), D).set_index("kod"); assert K.loc["KT05", "etiket"] == "SORGULA"
    # kontrol kartı GÖRDÜ
    K = K2.k2_karar(_hc(_iz("KT00")), D).set_index("kod"); assert K.loc["KT00", "etiket"] == "KONTROL GÖRDÜ"
    # bakış dışı -> BİLGİ (95 düzeyi)
    D2 = {"blok_sayi": 5, "acilan": K2.k2_bloklar_beklenen(5), "bakis_no": 0}
    o = _iz(); [v.update({"boot_alt95": 0.01, "boot_ust95": 0.03}) for k, v in o.items() if k[3] == 15]
    K = K2.k2_karar(_hc(o), D2).set_index("kod"); assert K.loc["KT03", "etiket"] == "BİLGİ (İZ ADAYI)"
    # blok yok
    K = K2.k2_karar(_hc(), {"blok_sayi": 0, "acilan": [], "bakis_no": 0}); assert K.etiket.str.startswith("BİLGİ (blok yok").all()


# ------------------------------------------------------------------ 12
def test_sabitler():
    import KART_TUR1 as KT
    B = K2.K2_ESIK["boot"]; assert abs(B["alt_bakis"] - 0.025 / 3) < 1e-15 and abs(B["ust_bakis"] - (1 - 0.025 / 3)) < 1e-15
    assert abs(K2.K2_ESIK["bh"]["q_bakis"] - 0.10 / 3) < 1e-15 and K2.K2_ESIK["ufuk"]["karar"] == [15, 30]
    karar = [k for k, v in K2.K2_KART.items() if v["karar"]]; assert len(karar) * 2 == 24 and "KT00" not in karar and "KT13" not in karar
    assert list(K2.K2_KART) == [f"KT{i:02d}" for i in range(14)]
    for k in [f"KT{i:02d}" for i in range(11)]:
        for c in ("yon", "cumle", "tanim", "esik", "kaynak"):
            assert K2.K2_KART[k][c] == KT.KT_KART[k][c], (k, c)
    assert K2.K2_KART["KT08"]["yon"] == "-" and K2.K2_KART["KT10"]["pazar"] == ["ABD"]
    assert K2.K2_ESIK["plasebo"]["tohum_sayi"] == 200 and K2.K2_ESIK["plasebo"]["fark_esik"] == 0.005 and K2.K2_ESIK["plasebo"]["tutar_pay"] == 0.07
    assert K2.K2_ESIK["boot"]["B"] == 2000 and K2.K2_ESIK["es"]["min"] == 5 and K2.K2_ESIK["bakis"]["12"] == 3
    assert "P2 36 hükmün 35'inde" in K2.K2_ESIK["kararlar"] and "SAPMA notudur" in K2.K2_ESIK["kararlar"]


# ------------------------------------------------------------------ 13
def test_y1_bayrak_yuvarlama():
    import YAPI_HEDEF as YH
    rng = np.random.default_rng(13); n = 400
    F = pd.DataFrame({c: rng.normal(0, 1, n) for c in K2._Y1_OZ})
    F["F15"] = rng.uniform(0, 1, n); F["F17"] = rng.uniform(-0.6, 0.2, n); F["F2"] = rng.normal(0, 0.03, n); F["F4"] = rng.uniform(0, 0.6, n)
    F["F3"] = rng.uniform(0.3, 1.5, n); F["F24"] = rng.normal(0.01, 0.02, n); F["F25"] = rng.uniform(0, 1, n); F["F26"] = rng.uniform(0, 1, n)
    F["F27"] = rng.uniform(0, 3, n); F["F28"] = rng.uniform(0, 2, n); F["F29"] = rng.normal(0, 5, n); F["S10"] = rng.integers(0, 2, n).astype(float)
    F.loc[::17, "F2"] = np.nan
    B = K2.k2_y1_bayrak(F)
    X = F.copy()
    for c in K2._Y1_OZ:
        X[c] = K2._r6(X[c].to_numpy(float))
    S = YH.yh_s9_sartlar(X)
    for k, m in (("F_KT02", S["S1"]), ("F_KT03", S["S3"]), ("F_KT04", S["S5"]), ("F_KT05", S["S4"]), ("F_KT06", S["S7"]),
                 ("F_KT07", S["S1"] & S["S3"] & S["S5"]), ("F_KT11", S["S9"]), ("F_KT12", F.S10.to_numpy() == 1)):
        assert np.array_equal(B[k].to_numpy() == 1.0, np.asarray(m, bool)), k
    assert B.F_KT01.eq(1.0).all() and 0 < B.F_KT11.sum() < n and not B.loc[::17, "F_KT03"].any()
    assert list(K2._r6(np.array([0.123456789, -0.0100000049]))) == [0.123457, -0.01]


# ------------------------------------------------------------------ 14
def test_tablo_sha():
    X = pd.DataFrame({"sembol": ["B", "A", "A"], "tarih": pd.to_datetime(["2020-01-02", "2020-01-03", "2020-01-02"]), "v": [1.0, 2.0, 3.0]})
    a = K2.k2_tablo_sha(X); b = K2.k2_tablo_sha(X.iloc[::-1].reset_index(drop=True)); assert a == b
    Y = X.copy(); Y.loc[0, "v"] = 1.0 + 1e-15; assert K2.k2_tablo_sha(Y) != a


# ------------------------------------------------------------------ 15
def test_sizinti_kontrol():
    with tempfile.TemporaryDirectory() as td:
        for m in ("iletisim ali@ornek.com", "api_key = ABCDEFGHIJKLMNOPQRST"):
            try:
                K2._k2_yaz(os.path.join(td, "x.md"), m)
            except K2.K2Hata:
                pass
            else:
                raise AssertionError("sızıntı taraması geçti")
        y = os.path.join(td, "k.md"); open(y, "w", encoding="utf-8").write("## KONTROL\n\n" + K2.k2_kontrol_tablosu() + "\n")
        import IZ_KARNE as IK
        assert IK.ik_kontrol_kapisi(y)["gecti"]
    src = open(os.path.join(KOK, "KART_TUR2.py"), encoding="utf-8").read()
    assert not [m for m in K2._K2_EPOSTA.findall(src) if m != "noreply@anthropic.com"]


# ------------------------------------------------------------------ 16
def test_onbellek():
    rng = np.random.default_rng(16)
    G = {g: pd.DataFrame({"sembol": ["A", "A", "B"], "tarih": pd.to_datetime(["2023-12-28", "2024-01-03", "2023-06-01"]),
                          "v": rng.normal(size=3)}) for g in ("Y1", "DS", "BOFA", "D9")}
    with tempfile.TemporaryDirectory() as td:
        m = K2.k2_onbellek_yaz(G, "ABD", pd.Timestamp("2023-12-31"), td)
        assert m["satir"]["Y1"] == 2
        O = K2.k2_onbellek_oku("ABD", None, td); assert len(O["tablo"]["DS"]) == 2
        O = K2.k2_onbellek_oku("ABD", {f"ABD|{g}": s for g, s in m["tablo_sha"].items()}, td)
        try:
            K2.k2_onbellek_oku("ABD", {"ABD|Y1": "0" * 64}, td)
        except K2.K2Hata:
            pass
        else:
            raise AssertionError("ön kayıt sha'sı tutmayan önbellek geçti")
        P = pd.read_pickle(K2._k2_ob_yol("ABD", td)); P["tablo"]["DS"].loc[0, "v"] += 1; pd.to_pickle(P, K2._k2_ob_yol("ABD", td))
        try:
            K2.k2_onbellek_oku("ABD", None, td)
        except K2.K2Hata:
            pass
        else:
            raise AssertionError("bozuk önbellek geçti")
        assert K2.k2_onbellek_oku("AVR", None, td) is None


# ------------------------------------------------------------------ 17
def test_gercek_onkayit_kapisi():
    y = K2.K2_YOL["onkayit"]
    if not os.path.exists(y):
        print("  (gerçek ön kayıt yok: atlandı)"); return
    r = subprocess.run(["git", "status", "--porcelain", "--", y], cwd=KOK, capture_output=True, text=True)
    if r.stdout.strip():
        print("  (gerçek ön kayıt git'e işlenmemiş: atlandı)"); return
    G = KS.ks_onkayit_kapi(y, K2.K2_HIPOTEZ, kontrol=True)
    assert {k["yol"] for k in G["kod"]} >= {"KART_TUR2.py", "KART_TUR1.py", "TEZGAH2_DOGRULAMA.py"}
    assert K2.k2_onkayit_kapisi(y)["bagimli"] == len(K2.K2_BAGIMLI)


if __name__ == "__main__":
    testler = [(k, v) for k, v in list(globals().items()) if k.startswith("test_") and callable(v)]
    hata = 0
    for ad, f in testler:
        try:
            f(); print(f"GEÇTİ  {ad}")
        except Exception as ex:   # her test ayrı raporlanır
            hata += 1; print(f"KALDI  {ad}: {type(ex).__name__}: {ex}")
    print(f"{len(testler) - hata}/{len(testler)} test geçti")
    sys.exit(1 if hata else 0)
