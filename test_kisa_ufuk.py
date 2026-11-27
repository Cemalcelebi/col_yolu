"""test_kisa_ufuk — KISA_UFUK sentetik testleri (gerçek veride getiri hesaplanmaz; ağ yok).

Kapsam: R_H tanımı (giriş barı dahil H'inci geçerli bar kapanışı) ve pencere kesiği (H bar yoksa / tarih > kesik ise ölçülmez); yönlü kümede işaret;
T1_H'nin hisse-dönem BÜTÜN uygun günlerinden hesaplanması (elle döngüyle) ve k % 5 alt kümesinin YO.yo_ornek_maske ile birebir olması; 'önce hangisi'
(+1 ATR / -1 ATR; aynı barda ikisi: kötümser, desen yönünün tersi önce); ilk mum getirisi; P_H (H = 15'te YO.yo_P15 ile birebir); dönem kodu
(HV.hv_hucre_ad ile aynı); bootstrap; hüküm / maliyet kuralları; aşama kapısı (kısa ufuk yalnız ölçüm kapısından sonra); kesik assert; olay
dosyalarının okunurken değişmediği (sha; AVR K1 / K2 gerçek dosyaları, getirisiz); çakışma kapısı.
Çalıştır: python test_kisa_ufuk.py"""
import os
import sys

import numpy as np
import pandas as pd

import KISA_UFUK as KU
import MUM_IZI as MI
import MUM_IZI_HAVUZ as HV
import YUKSELIS_ONCESI as YO

ISIM = []


def t(f):
    ISIM.append(f)
    return f


def _depo(n_hisse=3, n=400, tohum=1, bas="2016-01-04", P2=True):
    """Sentetik bar deposu (YO ham biçimi): her hisse her gün işlem görür; rastgele yürüyüş."""
    r = np.random.default_rng(tohum); tarih = pd.bdate_range(bas, periods=n)
    O, H, L, C, POS, off = [], [], [], [], [], [0]
    Op = np.full((n, n_hisse), np.nan); Cl = np.full((n, n_hisse), np.nan)
    for j in range(n_hisse):
        c = 50 * np.exp(np.cumsum(r.normal(0, 0.02, n))); o = c * np.exp(r.normal(0, 0.005, n))
        h = np.maximum(o, c) * (1 + r.uniform(0.001, 0.02, n)); lo = np.minimum(o, c) * (1 - r.uniform(0.001, 0.02, n))
        O.append(o); H.append(h); L.append(lo); C.append(c); POS.append(np.arange(n)); off.append(off[-1] + n); Op[:, j] = o; Cl[:, j] = c
    D = {"O": np.concatenate(O), "H": np.concatenate(H), "L": np.concatenate(L), "C": np.concatenate(C), "POS": np.concatenate(POS),
         "off": np.array(off, np.int64), "Op": Op, "Cl": Cl, "P2": np.full((n, n_hisse), bool(P2)), "tarih": tarih.values,
         "sembol": np.array([f"S{j}" for j in range(n_hisse)]), "_sentetik": True}
    D["tarih_ix"] = pd.DatetimeIndex(D["tarih"]); D["sembol_ix"] = {f"S{j}": j for j in range(n_hisse)}
    return D


@t
def test_R_H_tanim_ve_kesik():
    D = _depo(n=200)
    j = np.array([0, 1, 2]); e = np.array([10, 50, 199]); g = D["O"][D["off"][j] + e]
    R3 = KU.ku_R_olay(D, j, e, g, 3, "test")
    assert abs(R3[0] - (D["C"][D["off"][0] + 12] / g[0] - 1)) < 1e-15            # giriş barı dahil 3. bar = e + 2
    assert abs(R3[1] - (D["C"][D["off"][1] + 52] / g[1] - 1)) < 1e-15
    assert np.isnan(R3[2])                                                        # e + 2 veride yok -> ölçülmez
    R1 = KU.ku_R_olay(D, j[:1], e[:1], g[:1], 1, "test")
    assert abs(R1[0] - (D["C"][D["off"][0] + 10] / g[0] - 1)) < 1e-15            # ilk mum = giriş barının kendi getirisi
    D2 = _depo(n=60, bas="2022-11-01")
    jj = np.array([0]); ee = np.array([38]); rr = KU.ku_R_olay(D2, jj, ee, D2["O"][ee], 5, "test")
    tar = D2["tarih_ix"][D2["POS"][ee[0] + 4]]
    assert (np.isnan(rr[0]) if tar > KU.KU_KESIK else np.isfinite(rr[0]))         # tarih > kesik -> ölçülmez


@t
def test_taban_maske_yo_ile_ayni():
    r = np.random.default_rng(3)
    for _ in range(20):
        m = int(r.integers(30, 300)); bos = r.integers(1, 4, m); pos = np.cumsum(bos) - 1; nrow = int(pos[-1]) + 1
        tarih = pd.bdate_range("2015-10-01", periods=nrow); p2 = r.random(nrow) > 0.2
        k = KU.ku_taban_k(m, pos, p2, tarih); k5 = YO.yo_ornek_maske(m, pos, p2, tarih)
        assert np.array_equal(k[k % 5 == 0], k5)
        assert len(k) >= len(k5)


@t
def test_T1_butun_gunler_ve_isaret():
    D = _depo(n_hisse=2, n=500, tohum=5)
    X = KU._ku_cerceve("K1", np.array(["W1", "W1T"]), np.array([1, -1]), "ABD", D, np.array([0, 1]), np.array([100, 300]),
                       np.array([D["O"][100], D["O"][D["off"][1] + 300]]))
    X["kol_id"] = "K1|" + X.kol.astype(str)
    Y = KU.ku_pazar_hesap("ABD", D, X, "test")
    for i, (j, H) in enumerate([(0, 3), (1, 5)]):
        a, b = int(D["off"][j]), int(D["off"][j + 1]); pos = D["POS"][a:b]
        kk = KU.ku_taban_k(b - a, pos, D["P2"][:, j], D["tarih_ix"])
        dk = KU.ku_hucre_kod(D["tarih_ix"][pos[kk + 1]]); hk = int(Y.dk.iloc[i]); kk = kk[dk == hk]
        elle = np.mean([D["C"][a + k + H] / D["O"][a + k + 1] - 1 for k in kk])          # bütün günler, elle
        assert abs(Y[f"T1_{H}"].iloc[i] - elle) < 1e-12
        R = D["C"][a + int(Y.e.iloc[i]) + H - 1] / Y.giris.iloc[i] - 1
        assert abs(Y[f"TF{H}"].iloc[i] - Y.yon.iloc[i] * (R - elle)) < 1e-12           # yönlü: aşağı desende işaret çevrilir
    assert Y.yon.iloc[1] == -1 and abs(Y.TF5.iloc[1] + (Y.R5.iloc[1] - Y.T1_5.iloc[1])) < 1e-15
    assert abs(Y.ILK.iloc[0] - (Y.R1.iloc[0] - Y.T1_1.iloc[0])) < 1e-15


@t
def test_once_hangisi():
    g = np.array([100.0, 100.0, 100.0, 100.0, 100.0, 100.0]); A = np.array([2.0, 2.0, 2.0, 2.0, np.nan, 2.0])
    #            satır 0: yukarı önce (bar 1); 1: aşağı önce (bar 0); 2: aynı barda ikisi; 3: hiçbiri; 4: ATR yok; 5: aynı barda ikisi (aşağı desen)
    Hs = np.array([[101, 103, 99, 99, 99], [101, 101, 103, 99, 99], [103, 100, 100, 100, 100], [101, 101, 101, 101, 101],
                   [103, 100, 100, 100, 100], [103, 100, 100, 100, 100]], float)
    Ls = np.array([[99, 99, 97, 99, 99], [97, 99, 99, 99, 99], [97, 99, 99, 99, 99], [99, 99, 99, 99, 99], [97, 99, 99, 99, 99],
                   [97, 99, 99, 99, 99]], float)
    o = KU.ku_once_dizi(Hs, Ls, g, A, np.array([1, 1, 1, 1, 1, -1]))
    assert list(o[:4]) == [1.0, -1.0, -1.0, 0.0] and np.isnan(o[4]) and o[5] == -1.0     # bağ: desen yönünün tersi önce (iki yönde de -1)
    o2 = KU.ku_once_dizi(Hs[:2], Ls[:2], g[:2], A[:2], np.array([-1, -1]))
    assert list(o2) == [-1.0, 1.0]                                                       # aşağı desen: aşağı önce = +1


@t
def test_PH_yo_P15_ile_ayni():
    D = _depo(n_hisse=8, n=120, tohum=7); D["P2"] = np.random.default_rng(1).random(D["P2"].shape) > 0.3
    D["Cl"][5:9, 2] = np.nan
    a, _ = YO.yo_P15(D["Op"], D["Cl"], D["P2"]); b = KU.ku_PH(D["Op"], D["Cl"], D["P2"], 15)
    assert np.allclose(a, b, equal_nan=True, rtol=0, atol=0)
    c = KU.ku_PH(D["Op"], D["Cl"], D["P2"], 3)
    d = 10; jj = np.flatnonzero(D["P2"][d] & np.isfinite(D["Op"][d]))
    R = [D["Cl"][d + 2, j] / D["Op"][d, j] - 1 for j in jj if np.isfinite(D["Cl"][d + 2, j])]
    if len(R) >= 5 and all(np.isfinite(D["Cl"][d + 2, jj])):
        assert abs(c[d] - np.mean(R)) < 1e-12


@t
def test_donem_kodu():
    g = pd.to_datetime(["2015-12-31", "2016-01-01", "2019-12-31", "2020-01-01", "2022-12-30", "2023-01-02"])
    k = KU.ku_hucre_kod(g)
    bek = [{"ABD|d1619": 0, "ABD|d2022": 1}.get(HV.hv_hucre_ad(x, "ABD"), -1) for x in g]
    assert list(k) == bek


@t
def test_boot_ve_hukum():
    x = np.full(50, 0.01); ay = np.array([f"2017-{m:02d}" for m in np.arange(50) % 12 + 1]); k, W = KU.ku_ay_W(ay, "a", 500)
    b = KU.ku_boot(x, k, W); assert abs(b["alt"] - 0.01) < 1e-12 and abs(b["ust"] - 0.01) < 1e-12 and b["p"] < 0.01

    def c(n, ort, alt, ust, ay_=20):
        return {"n": n, "ay": ay_, "TF3": {"ort": ort, "alt": alt, "ust": ust}}
    o = {"ABD|d1619": c(500, 0.01, 0.001, 0.02), "ABD|d2022": c(500, 0.005, 0.0001, 0.01), "AVR|d1619": c(200, 0.002, -1, 1), "AVR|d2022": c(50, -0.01, -1, 1)}
    assert KU.ku_hukum(o, 3, True, True)[0] == "TUTAR"
    assert KU.ku_hukum(o, 3, False, True)[0] == "TUTMADI"
    o2 = {**o, "AVR|d1619": c(200, -0.002, -1, 1)}; assert KU.ku_hukum(o2, 3, True, True)[0] == "TUTMADI"
    o3 = {**o, "ABD|d2022": c(500, -0.005, -0.01, 0.001)}; assert KU.ku_hukum(o3, 3, True, True)[0] == "TEK DÖNEM"
    o4 = {**o, "ABD|d1619": c(500, -0.01, -0.02, -0.001), "ABD|d2022": c(500, -0.01, -0.02, -0.002)}
    assert KU.ku_hukum(o4, 3, True, True)[0] == "TERS" and KU.ku_hukum(o4, 3, True, False)[0] == "EKSİ"
    o5 = {**o, "ABD|d1619": c(299, 0.01, 0.001, 0.02)}; assert KU.ku_hukum(o5, 3, True, True)[0] == "ÖLÇÜLEMEDİ"
    o6 = {**o, "ABD|d1619": c(500, 0.01, 0.001, 0.02, 11)}; assert KU.ku_hukum(o6, 3, True, True)[0] == "ÖLÇÜLEMEDİ"
    assert KU.ku_maliyet(o, 3, "TUTAR")["etiket"] == "İŞLENEBİLİR"                     # (1,0 + 0,5) / 2 = %0,75 > %0,20
    o7 = {**o, "ABD|d1619": c(500, 0.0015, 0.001, 0.02), "ABD|d2022": c(500, 0.0015, 0.0001, 0.01)}
    assert KU.ku_maliyet(o7, 3, "TUTAR")["etiket"].startswith("işlenemez")


@t
def test_asama_kapisi():
    D = _depo(n=100)
    for H in (1, 3, 5):
        try:
            KU.ku_R_olay(D, [0], [10], [1.0], H, "dogrulama"); raise AssertionError("dogrulama aşamasında kısa ufuk")
        except KU.KUHata:
            pass
    KU._KU_DURUM["kapi_gecti"] = False
    try:
        KU.ku_R_olay(D, [0], [10], [1.0], 3, "olcum"); raise AssertionError("kapısız ölçüm")
    except KU.KUHata:
        pass
    D2 = dict(D); D2.pop("_sentetik")
    try:
        KU.ku_R_olay(D2, [0], [10], [1.0], 3, "test"); raise AssertionError("gerçek depoda test aşaması")
    except KU.KUHata:
        pass
    assert np.isfinite(KU.ku_R_olay(D2, [0], [10], [D["O"][10]], 15, "dogrulama")[0])   # H = 15 sağlaması izinli


@t
def test_kesik_assert():
    D = _depo(n=60, bas="2022-11-15")
    try:
        KU.ku_kesik_olay(D, np.array([0]), np.array([40])); raise AssertionError("kesik aşımı geçti")
    except KU.KUHata:
        pass
    import tempfile
    d = tempfile.mkdtemp(); z = {k: v for k, v in D.items() if k in ("O", "H", "L", "C", "POS", "off", "Op", "Cl", "P2", "tarih", "sembol")}
    np.savez(os.path.join(d, "ham_ABD.npz"), **z)
    try:
        KU.ku_depo("ABD", d); raise AssertionError("2023 verili depo açıldı")
    except KU.KUHata:
        pass


@t
def test_olay_dosyalari_degismez():
    if not (os.path.exists(KU.KU_KAYNAK["K1_olay_AVR"]) and os.path.exists(KU.KU_KAYNAK["DEPO_AVR"])):
        print("  (gerçek dosya yok; atlandı)"); return
    a = KU.ku_kaynak_sha(["K1_olay_AVR", "K2_olay_AVR", "DEPO_AVR"])
    D = KU.ku_depo("AVR"); X1 = KU.ku_olay_K1("AVR", D); X2 = KU.ku_olay_K2("AVR", D)
    assert len(X1) and len(X2) and set(X2.kol.unique()) <= {"2", "3", "4"}
    assert not any(c.startswith("R") and c[1:].isdigit() for c in X1.columns)             # getirisiz
    b = KU.ku_kaynak_sha(["K1_olay_AVR", "K2_olay_AVR", "DEPO_AVR"])
    assert a == b


@t
def test_kollar_ve_aile():
    assert len(KU.KU_KOLLAR) == 41 and len(set(KU.KU_KOL_ID)) == 41
    assert sum(k["kume"] == "K1" for k in KU.KU_KOLLAR) == 17 and sum(k["kume"] == "K3" for k in KU.KU_KOLLAR) == 16
    assert all(not k["yonlu"] and k["yon"] == 1 for k in KU.KU_KOLLAR if k["kume"] != "K1")


@t
def test_cakisma_kapisi():
    try:
        KU._cakisma_kontrol_ku(_once={**KU._CK_ONCE_KU, "ku_boot": -1}); raise AssertionError("ezilen ad yakalanmadı")
    except RuntimeError:
        pass
    KU._cakisma_kontrol_ku()


if __name__ == "__main__":
    bas = 0
    for f in ISIM:
        try:
            f(); print("GEÇTİ", f.__name__)
        except Exception as ex:  # noqa: BLE001
            bas += 1; print("KALDI", f.__name__, type(ex).__name__, ex)
    print(f"{len(ISIM) - bas} / {len(ISIM)} geçti")
    sys.exit(1 if bas else 0)
