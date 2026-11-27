"""test_doji_obek — DOJI_OBEK sentetik testleri (gerçek veri / sonuç görülmez; ağ yok).

Kapsam: yapay POZİTİF (aynı seviyede 1-2 mum arayla 2 / 3 / 4 doji) ve NEGATİF seriler (farklı seviye, 3'ten çok mum ara, ölü / fiyat adımına yapışmış
barlar, gövde / boy > 0,10 küçük gövdeler, rastgele seri): yakalama >= %95, yanlış kabul <= %5; öbeğin k'inci dojinin barında yalnız o bara kadarki
veriyle tanınması (sonrası bozulunca aynı); seviye bandı 0,5 ATR sınırı (dahil / hariç); doji arası en çok 2 mum sınırı; takvim boşluğu; ölü bar dışlama;
uygunluk maskesinin YO.yo_ornek_maske ile 5. barlarda birebir olması; hücre adı; çıkış yönü ve çıkış sonrası getiri mantığı; ATR eşikli dokunma; bootstrap;
hüküm / doz kuralları; kesik assert; ölçüm kapısı sırası; çakışma kapısı.
Çalıştır: python test_doji_obek.py"""
import os
import sys
import tempfile

import numpy as np
import pandas as pd

import DOJI_OBEK as DJ
import MUM_IZI_HAVUZ as HV
import YUKSELIS_ONCESI as YO

ISIM = []
SONUC = {}


def t(f):
    ISIM.append(f)
    return f


# ---------------------------------------------------------------- yapay seri üreticisi
def _taban(n, r, s=0.02, govde=(0.3, 0.9)):
    """Doji olmayan rastgele seri: her bar gövde / boy oranı govde aralığında (doji değil)."""
    C = np.empty(n); O = np.empty(n); H = np.empty(n); L = np.empty(n); p = 50.0
    for i in range(n):
        boy = p * s * r.uniform(0.8, 1.2); g = boy * r.uniform(*govde); yon = 1 if r.random() < 0.5 else -1
        alt = p - r.uniform(0, boy - g) if yon > 0 else p - r.uniform(g, boy)
        lo = alt; hi = lo + boy
        if yon > 0:
            o = r.uniform(lo, hi - g); c = o + g
        else:
            o = r.uniform(lo + g, hi); c = o - g
        O[i], H[i], L[i], C[i] = o, hi, lo, c; p = c
    return O, H, L, C


def _doji_koy(O, H, L, C, i, seviye, boy, govde_oran=0.02):
    g = boy * govde_oran; O[i] = seviye - g / 2; C[i] = seviye + g / 2; H[i] = seviye + boy / 2; L[i] = seviye - boy / 2


def _atr(O, H, L, C):
    return DJ._dj_ozellik(O, H, L, C)["ATRP20"] * C


def _gom(r, k, n=80, bas=50, ara=(0, 2), yay_atr=0.15):
    """POZİTİF: bas'tan itibaren k doji; arada 0-2 mum; seviyeler taban seviyesinden en çok +-yay_atr/2 ATR (ATR doji öncesi 20 bardan kestirilir)."""
    O, H, L, C = _taban(n, r)
    atr0 = float(np.mean((H - L)[bas - 20:bas])); lv0 = C[bas - 1]; ix = []; i = bas
    for q in range(k):
        ix.append(i); lv = lv0 + r.uniform(-yay_atr / 2, yay_atr / 2) * atr0
        _doji_koy(O, H, L, C, i, lv, atr0 * r.uniform(0.9, 1.1))
        # aradaki mumlar seviyeye yakın kalsın (doji değil)
        i += 1 + int(r.integers(ara[0], ara[1] + 1))
    return (O, H, L, C), ix


def _olaylar(O, H, L, C, govde=None):
    m = len(C); F = DJ._dj_ozellik(O, H, L, C)
    Dj = DJ.dj_doji(O, H, L, C, govde)
    return DJ.dj_obek(Dj["doji"], O, H, L, C, F["ATRP20"] * C, np.arange(m)), Dj


# ---------------------------------------------------------------- POZİTİF / NEGATİF yapay sınama
@t
def test_pozitif_yakalama():
    r = np.random.default_rng(11); out = {}
    for k in (2, 3, 4):
        tut = 0; N = 300
        for _ in range(N):
            (O, H, L, C), ix = _gom(r, k)
            B, _ = _olaylar(O, H, L, C)
            hit = B[(B.t == ix[-1]) & (B.k == k) & (B.ilk == ix[0])]
            tut += int(len(hit) == 1)
        out[k] = tut / N
        assert out[k] >= 0.95, f"k={k} yakalama {out[k]:.3f} < 0,95"
    SONUC["yakalama"] = out


@t
def test_negatif_yanlis_kabul():
    r = np.random.default_rng(12); out = {}; N = 300

    def k2_var(B, a, b):
        return bool(((B.t == b) & (B.k >= 2) & (B.ilk == a)).any())
    # (a) farklı seviye: ara 1 mum, seviye farkı 0,8-2 ATR
    say = 0
    for _ in range(N):
        O, H, L, C = _taban(80, r); atr0 = float(np.mean((H - L)[30:50])); lv = C[49]
        _doji_koy(O, H, L, C, 50, lv, atr0); _doji_koy(O, H, L, C, 52, lv + r.choice([-1, 1]) * r.uniform(0.8, 2.0) * atr0, atr0)
        B, _ = _olaylar(O, H, L, C); say += k2_var(B, 50, 52)
    out["farkli_seviye"] = say / N
    # (b) arada 3-6 mum, aynı seviye
    say = 0
    for _ in range(N):
        O, H, L, C = _taban(80, r); atr0 = float(np.mean((H - L)[30:50])); lv = C[49]; g = int(r.integers(4, 8))
        _doji_koy(O, H, L, C, 50, lv, atr0); _doji_koy(O, H, L, C, 50 + g, lv, atr0)
        B, _ = _olaylar(O, H, L, C); say += k2_var(B, 50, 50 + g)
    out["ara_uzak"] = say / N
    # (c) ölü barlar: gövdesiz ama boyu çok küçük (normalin %10-40'ı)
    say = 0
    for _ in range(N):
        O, H, L, C = _taban(80, r); atr0 = float(np.mean((H - L)[30:50])); lv = C[49]
        _doji_koy(O, H, L, C, 50, lv, atr0 * r.uniform(0.1, 0.4), 0.0); _doji_koy(O, H, L, C, 51, lv, atr0 * r.uniform(0.1, 0.4), 0.0)
        B, Dj = _olaylar(O, H, L, C); say += int(Dj["doji"][50] or Dj["doji"][51])
    out["olu"] = say / N
    # (d) küçük gövde ama gövde / boy 0,11-0,30
    say = 0
    for _ in range(N):
        O, H, L, C = _taban(80, r); atr0 = float(np.mean((H - L)[30:50])); lv = C[49]
        _doji_koy(O, H, L, C, 50, lv, atr0, r.uniform(0.11, 0.30)); _doji_koy(O, H, L, C, 51, lv, atr0, r.uniform(0.11, 0.30))
        B, Dj = _olaylar(O, H, L, C); say += int(Dj["doji"][50] or Dj["doji"][51])
    out["govde_buyuk"] = say / N
    # (e) rastgele seri (gövde / boy >= 0,2): hiç öbek olmamalı
    say = 0
    for _ in range(N):
        O, H, L, C = _taban(120, r, govde=(0.2, 1.0))
        B, _ = _olaylar(O, H, L, C); say += int((B.k >= 2).any() if len(B) else 0)
    out["rastgele"] = say / N
    for a, v in out.items():
        assert v <= 0.05, f"yanlış kabul {a} {v:.3f} > 0,05"
    SONUC["yanlis_kabul"] = out


@t
def test_fiyat_adimi_yapisik():
    """Kuruşa yapışmış bar: fiyatlar 0,01 adımlı, doji boyu 2 adım (ORT_BOY şartını geçer) -> ADIM kuralı düşürür; boyu 10 adım olan doji kalır."""
    r = np.random.default_rng(3); n = 60
    C = np.round(1.0 + np.cumsum(r.choice([-0.01, 0.0, 0.01], n)), 2); O = np.round(C + r.choice([-0.01, 0.01], n), 2)
    H = np.maximum(O, C) + 0.01; L = np.minimum(O, C) - 0.01
    i = 40; O[i] = C[i] = C[i - 1]; H[i] = C[i] + 0.01; L[i] = C[i] - 0.01          # boy 2 adım
    Dj = DJ.dj_doji(O, H, L, C)
    assert abs(Dj["adim"][i] - 0.01) < 1e-9 and Dj["yapis"][i] and not Dj["doji"][i]
    O2, H2, L2, C2 = _taban(60, r); atr0 = float(np.mean((H2 - L2)[20:40])); _doji_koy(O2, H2, L2, C2, 45, C2[44], atr0)
    D2 = DJ.dj_doji(O2, H2, L2, C2); assert D2["doji"][45] and not D2["yapis"][45]


@t
def test_doji_tanimi_sinir():
    O = np.array([10.0] * 11 + [10.0]); H = np.array([10.5] * 11 + [10.5]); L = np.array([9.5] * 11 + [9.5]); C = np.array([10.4] * 11 + [10.1])
    Dj = DJ.dj_doji(O, H, L, C)
    assert Dj["doji"][11] and not Dj["doji"][:10].any()                   # gövde 0,1 = 0,10 x boy 1,0 (dahil); ilk 10 bar ORT_BOY yok
    C2 = C.copy(); C2[11] = 10.1001; assert not DJ.dj_doji(O, H, L, C2)["doji"][11]
    H3 = H.copy(); L3 = L.copy(); H3[11] = 10.24; L3[11] = 9.76; C3 = C.copy(); C3[11] = 10.0      # boy 0,48 < 0,5 x 1,0
    assert not DJ.dj_doji(O, H3, L3, C3)["doji"][11]
    assert DJ.dj_doji(O, H, L, np.r_[C[:11], 10.14], govde=0.15)["doji"][11] and not DJ.dj_doji(O, H, L, np.r_[C[:11], 10.14])["doji"][11]


@t
def test_bant_sinir_ve_ara():
    n = 30; O = np.full(n, 10.0); C = np.full(n, 10.0); H = np.full(n, 10.5); L = np.full(n, 9.5); atr = np.full(n, 1.0)
    d = np.zeros(n, bool); d[[10, 12]] = True
    O[12] = C[12] = 10.5 - 1e-9                                            # fark 0,5 - eps <= 0,5 x 1 -> bağlanır
    B = DJ.dj_obek(d, O, H, L, C, atr); assert list(B.k) == [1, 2]
    O[12] = C[12] = 10.5 + 1e-6                                            # hariç
    B = DJ.dj_obek(d, O, H, L, C, atr); assert list(B.k) == [1, 1] and B.red.iloc[1] == "SEVIYE_FARKLI"
    O[12] = C[12] = 10.0
    for g, bek in ((1, [1, 2]), (2, [1, 2]), (3, [1, 2]), (4, [1, 1]), (5, [1, 1])):
        d = np.zeros(n, bool); d[[10, 10 + g]] = True; B = DJ.dj_obek(d, O, H, L, C, atr); assert list(B.k) == bek, (g, list(B.k))
    d = np.zeros(n, bool); d[[10, 13]] = True; pos = np.arange(n); pos[13:] += 4             # takvim satırı farkı 7 > 6
    B = DJ.dj_obek(d, O, H, L, C, atr, pos); assert list(B.k) == [1, 1] and B.red.iloc[1] == "TAKVIM"
    # üç doji: üçüncü, ilk ikisinin yayılımıyla birlikte 0,5'i aşınca yeni öbek
    d = np.zeros(n, bool); d[[10, 11, 12]] = True; O2 = O.copy(); C2 = C.copy(); O2[11] = C2[11] = 10.3; O2[12] = C2[12] = 9.75
    B = DJ.dj_obek(d, O2, H, L, C2, atr); assert list(B.k) == [1, 2, 1] and B.obek.tolist() == [0, 0, 1]
    # bant = dojilerin maks H / min L
    d = np.zeros(n, bool); d[[10, 12]] = True; H2 = H.copy(); H2[12] = 10.9; L2 = L.copy(); L2[10] = 9.2
    B = DJ.dj_obek(d, O, H2, L2, C, atr); assert B.bant_H.iloc[1] == 10.9 and B.bant_L.iloc[1] == 9.2 and B.bant_H.iloc[0] == 10.5


@t
def test_gelecege_bakma_yok():
    r = np.random.default_rng(5)
    for _ in range(40):
        (O, H, L, C), ix = _gom(r, 4, n=120, bas=60)
        B, _ = _olaylar(O, H, L, C); cut = ix[-1]
        O2, H2, L2, C2 = (x.copy() for x in (O, H, L, C)); Ob, Hb, Lb, Cb = _taban(120 - cut - 1, r)
        O2[cut + 1:], H2[cut + 1:], L2[cut + 1:], C2[cut + 1:] = Ob * 3, Hb * 3, Lb * 3, Cb * 3      # sonrası bozuldu
        B2, _ = _olaylar(O2, H2, L2, C2)
        a = B[B.t <= cut].drop(columns="obek_boy").reset_index(drop=True); b = B2[B2.t <= cut].drop(columns="obek_boy").reset_index(drop=True)
        pd.testing.assert_frame_equal(a, b)
        # tara_hisse (özellikler dahil) aynı
        pos = np.arange(120); p2 = np.ones(120, bool); tr = pd.bdate_range("2017-01-02", periods=120)
        X1, _ = DJ.dj_tara_hisse(O, H, L, C, pos, p2, tr); X2, _ = DJ.dj_tara_hisse(O2, H2, L2, C2, pos, p2, tr)
        c = ["t", "k", "ilk", "bant_H", "bant_L", "ATRP20", "KONUM120", "ONCEKI10"]
        pd.testing.assert_frame_equal(X1[X1.t <= cut][c].reset_index(drop=True), X2[X2.t <= cut][c].reset_index(drop=True))


@t
def test_uygunluk_yo_ile_ayni():
    r = np.random.default_rng(7)
    for _ in range(20):
        m = int(r.integers(40, 400)); pos = np.cumsum(r.choice([1, 1, 1, 2, 12], m)); n = int(pos[-1] + 5)
        tarih = pd.bdate_range("2015-06-01", periods=n); p2 = r.random(n) < 0.9
        k5 = YO.yo_ornek_maske(m, pos, p2, tarih)
        kk = np.arange(0, m, 5); ok = DJ.dj_uygun(m, pos, p2, tarih, kk)
        assert np.array_equal(kk[ok], k5)


@t
def test_hucre_ayni():
    g = pd.DatetimeIndex(["2015-12-31", "2016-01-01", "2019-12-31", "2020-01-02", "2022-12-30"])
    assert list(DJ.dj_hucre(g, "ABD")) == [HV.hv_hucre_ad(x, "ABD") for x in g]


def _dep(O, H, L, C):
    m = len(C)
    return {"O": np.asarray(O, float), "H": np.asarray(H, float), "L": np.asarray(L, float), "C": np.asarray(C, float),
            "POS": np.arange(m, dtype=np.int64), "off": np.array([0, m], np.int64)}


@t
def test_cikis_ve_devam():
    m = 60; O = np.full(m, 10.0); H = np.full(m, 10.2); L = np.full(m, 9.8); C = np.full(m, 10.0)
    # t = 20; bant 9,8 .. 10,2; t + 3 kapanışı 10,3 -> YUKARI, e = 23; O[24] = 10,4, C[33] = 11,44 -> R10 = +%10
    C[23] = 10.3; H[23] = 10.35; O[24] = 10.4; C[33] = 11.44
    R = DJ.dj_getiri_dizi(_dep(O, H, L, C), [0], [20], [0.02], [10.2], [9.8])
    assert R["CIKIS"][0] == 1 and R["CIKIS_BAR"][0] == 3 and abs(R["DEVAM"][0] - 0.10) < 1e-12
    # aşağı: t + 2 kapanışı 9,7; O[23] = 9,6; C[32] = 8,64 -> R10 = -%10 -> çıkış yönünde +%10
    C2 = np.full(m, 10.0); O2 = np.full(m, 10.0); L2 = L.copy(); C2[22] = 9.7; L2[22] = 9.65; O2[23] = 9.6; C2[32] = 8.64
    R = DJ.dj_getiri_dizi(_dep(O2, H, L2, C2), [0], [20], [0.02], [10.2], [9.8])
    assert R["CIKIS"][0] == -1 and R["CIKIS_BAR"][0] == 2 and abs(R["DEVAM"][0] - 0.10) < 1e-12
    # kapanış bandın üstüne eşit (10,2) çıkış değil; hiç çıkış yok
    C3 = np.full(m, 10.0); C3[25] = 10.2
    R = DJ.dj_getiri_dizi(_dep(O, H, L, C3), [0], [20], [0.02], [10.2], [9.8])
    assert R["CIKIS"][0] == 0 and np.isnan(R["DEVAM"][0])
    # çıkış barı veri sonuna çok yakın -> DEVAM yok
    m2 = 37; R = DJ.dj_getiri_dizi(_dep(O[:m2], H[:m2], L[:m2], np.r_[np.full(35, 10.0), 10.5, 10.5]), [0], [20], [0.02], [10.2], [9.8])
    assert R["CIKIS"][0] == 1 and np.isnan(R["DEVAM"][0])
    # R15 = C[t+15] / O[t+1] - 1; giriş t + 1 açılışı
    R = DJ.dj_getiri_dizi(_dep(O, H, L, C), [0], [20], [0.02])
    assert abs(R["R15"][0] - (C[35] / O[21] - 1)) < 1e-12 and np.isnan(R["CIKIS"][0])
    try:
        DJ.dj_getiri_dizi(_dep(O[:30], H[:30], L[:30], C[:30]), [0], [20], [0.02]); raise AssertionError("pencere aşımı yakalanmadı")
    except DJ.DJHata:
        pass


@t
def test_atr_dokunma():
    m = 40; O = np.full(m, 100.0); H = np.full(m, 100.5); L = np.full(m, 99.5); C = np.full(m, 100.0)
    H[24] = 104.0                                                          # +2 ATR (ATRP 0,02 -> +%4) t + 4'te; stop -%2 yok
    R = DJ.dj_getiri_dizi(_dep(O, H, L, C), [0], [20], [0.02]); assert R["U2"][0] == 1 and R["D2"][0] == 0
    L2 = L.copy(); L2[23] = 98.0                                           # stop -%2 önce
    R = DJ.dj_getiri_dizi(_dep(O, H, L2, C), [0], [20], [0.02]); assert R["U2"][0] == 0
    L3 = L.copy(); L3[24] = 98.0                                           # aynı bar -> stop önce
    R = DJ.dj_getiri_dizi(_dep(O, H, L3, C), [0], [20], [0.02]); assert R["U2"][0] == 0
    L4 = L.copy(); L4[22] = 96.0                                           # ayna: -%4, +%2'den önce
    R = DJ.dj_getiri_dizi(_dep(O, np.full(m, 100.5), L4, C), [0], [20], [0.02]); assert R["D2"][0] == 1
    assert abs(R["BUYUKLUK"][0] - abs(R["R15"][0]) / (0.02 * np.sqrt(15))) < 1e-12


@t
def test_bootstrap_ve_fark():
    r = np.random.default_rng(1); ay = np.repeat([f"2017-{i:02d}" for i in range(1, 13)], 50); x = r.normal(0.01, 0.05, len(ay))
    o = DJ.dj_boot(x, ay, "a", B=2000); assert o["alt"] < o["ort"] < o["ust"] and o["n"] == 600
    o2 = DJ.dj_boot(x, ay, "a", B=2000); assert o == o2                    # tohum tekrarlanır
    f = DJ.dj_boot_fark(x + 0.05, ay, x, ay, "f", B=2000); assert abs(f["fark"] - 0.05) < 1e-12 and f["alt"] > 0.049 and f["p"] < 0.01
    k = DJ.dj_boot(np.full(600, 2.0), ay, "k", B=500, pay=np.ones(600)); assert abs(k["ort"] - 2.0) < 1e-12


@t
def test_hukum_ve_doz():
    a = {"n": 2000, "ort": 0.01, "alt": 0.002, "ust": 0.02}; z = {"n": 2000, "ort": 0.0, "alt": -0.01, "ust": 0.01}
    e = {"n": 2000, "ort": -0.01, "alt": -0.02, "ust": -0.002}; av = {"n": 300, "ort": 0.004}
    o = {"ABD|d1619": a, "ABD|d2022": a, "AVR|d1619": av, "AVR|d2022": av}
    assert DJ.dj_etiket(o, bh_gecti=True) == "ARTI" and DJ.dj_etiket(o, bh_gecti=False) == "BH GEÇMEDİ"
    assert DJ.dj_etiket({**o, "AVR|d2022": {"ort": -0.001}}, bh_gecti=True) == "ABD İKİ DÖNEM, AVR UYMADI"
    assert DJ.dj_etiket({**o, "ABD|d2022": z}) == "TEK DÖNEM" and DJ.dj_etiket({**o, "ABD|d2022": e}) == "ÇELİŞKİLİ"
    assert DJ.dj_etiket({**o, "ABD|d1619": z, "ABD|d2022": z}) == "AYRIŞMIYOR"
    assert DJ.dj_etiket({**o, "ABD|d1619": z, "ABD|d2022": {**z, "n": 999}}) == "ÖLÇÜLEMEDİ"
    eo = {"ABD|d1619": e, "ABD|d2022": e, "AVR|d1619": {"ort": -0.1}, "AVR|d2022": {"ort": -0.2}}
    assert DJ.dj_etiket(eo, bh_gecti=True) == "EKSİ"
    s = {h: {1: 0.0, 2: 0.01, 3: 0.02, 4: 0.03} for h in DJ.DJ_ABD}; fk = {h: {3: {"alt": 0.001}, 4: {"alt": 0.002}} for h in DJ.DJ_ABD}
    assert DJ.dj_doz(s, fk)["etkili"]
    assert not DJ.dj_doz({**s, "ABD|d2022": {1: 0.0, 2: 0.02, 3: 0.01, 4: 0.03}}, fk)["etkili"]
    assert not DJ.dj_doz(s, {h: {3: {"alt": -0.001}, 4: {"alt": -0.002}} for h in DJ.DJ_ABD})["etkili"]


@t
def test_kesik_assert():
    DJ.dj_kesik_kapi(pd.DatetimeIndex(["2022-12-30"]))
    try:
        DJ.dj_kesik_kapi(pd.DatetimeIndex(["2023-01-02"])); raise AssertionError("kesik yakalanmadı")
    except DJ.DJHata:
        pass


@t
def test_olcum_kapisi_sira():
    with tempfile.TemporaryDirectory() as d:
        try:
            DJ.dj_kapi(cikti=d, ham=d, git=False); raise AssertionError("ön kayıtsız kapı açıldı")
        except DJ.DJHata as ex:
            assert "ön kayıt yok" in str(ex)
        open(os.path.join(d, "DJ_ON_KAYIT.md"), "w").write("| K1 | kontrol | EVET | kısa |\n")
        try:
            DJ.dj_kapi(cikti=d, ham=d, git=False); raise AssertionError("eksik kontrol tablosuyla kapı açıldı")
        except DJ.DJHata as ex:
            assert "kontrol kapısı" in str(ex)


@t
def test_hafta_bar():
    tr = pd.bdate_range("2017-01-02", periods=15); O = np.arange(15.0) + 10; H = O + 1; L = O - 1; C = O + 0.5
    W = DJ.dj_hafta_bar(O, H, L, C, tr, np.arange(15))
    assert len(W) == 3 and W.O.iloc[0] == 10 and W.C.iloc[0] == 14.5 and W.H.iloc[0] == 15 and W.L.iloc[0] == 9 and W.ilk_row.iloc[1] == 5


@t
def test_esik_sabit():
    E = DJ.DJ_ESIK
    assert E["doji"]["govde"] == 0.10 and E["doji"]["boy_oran"] == 0.5 and E["obek"]["ara_en_cok"] == 3 and E["obek"]["bant_atr"] == 0.5
    assert E["tohum"] == 2712 and E["boot"]["B"] == 10000 and E["bh"]["q"] == 0.10 and E["sonuc"]["ufuk"] == 15 and E["hukum"]["n_min"] == 1000
    assert set(DJ.DJ_KONTROL) == {f"K{i}" for i in range(1, 15)}


@t
def test_cakisma_kapisi():
    kod = open(os.path.join(os.path.dirname(os.path.abspath(DJ.__file__)), "DOJI_OBEK.py"), encoding="utf-8").read()
    ns = {"__name__": "dj_test", "__file__": DJ.__file__}
    exec(compile(kod, "DOJI_OBEK.py", "exec"), ns)
    ns2 = {"__name__": "dj_test2", "__file__": DJ.__file__, "dj_kapi": 1}
    try:
        exec(compile(kod, "DOJI_OBEK.py", "exec"), ns2)
    except RuntimeError as ex:
        assert "çakışma" in str(ex)
    else:
        raise AssertionError("çakışma kapısı çalışmadı")


def _sentetik_pazar(u=30, tohum=3):
    tr = pd.bdate_range("2015-01-02", "2022-12-30"); n = len(tr); r = np.random.default_rng(tohum)
    Os, Hs, Ls, Cs = [], [], [], []
    for j in range(u):
        C = 20 * np.exp(np.cumsum(r.normal(0, 0.02, n))); O = C * np.exp(r.normal(0, 0.01, n))
        H = np.maximum(O, C) * (1 + np.abs(r.normal(0, 0.01, n))) + 1e-6; L = np.minimum(O, C) * (1 - np.abs(r.normal(0, 0.01, n)))
        Os.append(O); Hs.append(H); Ls.append(L); Cs.append(C)
    O = np.concatenate(Os); H = np.concatenate(Hs); L = np.concatenate(Ls); C = np.concatenate(Cs)
    return {"O": O, "H": H, "L": L, "C": C, "POS": np.tile(np.arange(n), u), "off": np.arange(u + 1) * n, "Op": np.stack(Os, 1), "Cl": np.stack(Cs, 1),
            "P2": np.ones((n, u), bool), "tarih": tr.values.astype("datetime64[ns]"), "sembol": np.array([f"S{j}" for j in range(u)])}


@t
def test_uctan_uca_sentetik():
    """hazırla -> sayım -> (kapı atlanarak) ölçüm -> hüküm -> özet + rapor: şema ve akış (sonuç değerleri sınanmaz)."""
    Dm = {"ABD": _sentetik_pazar(30, 3), "AVR": _sentetik_pazar(12, 4)}
    with tempfile.TemporaryDirectory() as d:
        for p in DJ.DJ_PAZAR:
            DJ.dj_hazirla_pazar(p, ham=d, D=Dm[p])
        S = DJ.dj_sayim(d); assert S["ANA"]["ABD|d1619"]["2"]["n"] > 0
        eski_k, eski_d = DJ.dj_kapi, DJ.dj_depo
        try:
            DJ.dj_kapi = lambda *a, **k: {"kontrol": True}
            DJ.dj_depo = lambda p, kaynak=None: Dm[p]
            J = DJ.dj_olcum(cikti=d, ham=d, git=False, B=200)
        finally:
            DJ.dj_kapi, DJ.dj_depo = eski_k, eski_d
        assert J["hukum"]["genel"] and len(J["hukum"]["bh"]) == 32 and os.path.exists(os.path.join(d, "dj_ozet.csv"))
        r = J["ANA"]["hucre"]["ABD|d1619"]["2"]; assert r["n"] > 0 and r["TOPLAM_FARK"]["alt"] is not None and r["CIKIS_PAY"]["YUKARI"] is not None
        eski_h = DJ.DJ_YOL["ham"]
        try:
            DJ.DJ_YOL["ham"] = d; DJ.dj_rapor_yaz(cikti=d, ham=d)
        finally:
            DJ.DJ_YOL["ham"] = eski_h
        assert "## HATA" in open(os.path.join(d, "DJ_RAPOR.md"), encoding="utf-8").read()


@t
def test_d40_kati_ve_basamak():
    O = np.full(12, 8.0); H = np.full(12, 9.0); L = np.full(12, 7.75); C = np.array([8.75] * 11 + [8.5])      # ikili kesin sayılar: gövde 0,5 = 0,40 x 1,25
    assert not DJ.dj_doji(O, H, L, C, 0.40, kati=True)["doji"][11]           # KATI küçüktür -> doji değil
    assert DJ.dj_doji(O, H, L, C, 0.40, kati=False)["doji"][11]
    C2 = C.copy(); C2[11] = 8.49; assert DJ.dj_doji(O, H, L, C2, 0.40, kati=True)["doji"][11]
    # basamaklar: 8 dojilik öbek -> 1, 2, 3, 4, 5, 7 olayları (6. ve 8. olay değil)
    n = 260; O = np.full(n, 10.0); C = np.full(n, 10.6); H = np.full(n, 10.8); L = np.full(n, 9.8); ix = list(range(200, 208))   # gövde 0,6 boy: doji değil
    C[ix] = 10.0
    tr = pd.bdate_range("2017-01-02", periods=n)
    B, _ = DJ.dj_tara_hisse(O, H, L, C, np.arange(n), np.ones(n, bool), tr, 0.40, None, True, DJ.DJ_D40_KSIN)
    g = B[B.t.isin(ix)]
    assert sorted(g.k.tolist()) == [1, 2, 3, 4, 5, 7], g.k.tolist()
    B0, _ = DJ.dj_tara_hisse(O, H, L, C, np.arange(n), np.ones(n, bool), tr, 0.10)
    assert sorted(B0[B0.t.isin(ix)].k.tolist()) == [1, 2, 3, 4]               # ANA varsayılanı değişmedi


@t
def test_d40_rastgele_ve_hukum():
    r = np.random.default_rng(9); O, H, L, C = DJ.dj_rastgele_seri(300, r); assert (H >= np.maximum(O, C)).all() and (L <= np.minimum(O, C)).all()
    s = {h: {1: 0.0, 2: 0.01, 3: 0.02, 4: 0.03, 5: 0.04, 7: 0.05} for h in DJ.DJ_ABD}; fk = {h: {3: {"alt": 0.001}, 4: {"alt": 0.002}} for h in DJ.DJ_ABD}
    assert DJ.dj_doz(s, fk, DJ.DJ_D40_KSIN)["etkili"]
    s2 = {h: {**s[h], 7: 0.0} for h in DJ.DJ_ABD}; assert not DJ.dj_doz(s2, fk, DJ.DJ_D40_KSIN)["etkili"]


if __name__ == "__main__":
    bas = 0
    for f in ISIM:
        try:
            f(); print("GEÇTİ", f.__name__)
        except Exception as ex:  # noqa: BLE001
            bas += 1; print("KALDI", f.__name__, type(ex).__name__, ex)
    print("yapay:", SONUC)
    print(f"{len(ISIM) - bas} / {len(ISIM)} geçti")
    sys.exit(1 if bas else 0)
