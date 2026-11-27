"""test_sekil_devam — SEKIL_DEVAM sentetik testleri (gerçek veri / sonuç görülmez; ağ yok).

Kapsam: (i) Cemal'in kalıbı gömülü yapay panelde (sonrası +0,5 Z) yöntem IC > 0 bulur, kalıbı tek kümede toplar, en iyi kümeler kalıbın kendisi / erken
evresidir, N1 / N2 negatiflerini kalıbın kümesine sokmaz; (ii) ilişkisiz rastgele yürüyüşte IC aralığı sıfırı içerir; (iii) komşular yalnız geçmişten
(>= 20 satır önce biten, devamı bilinen) ve başka hisseden, tam arama saf çözümle aynı; (iv) tanımlayıcı pencere sonrası barlardan etkilenmez; elle örnek;
(v) HEDEF / AYNA 'önce hangisi' (aynı bar = stop); (vi) kesik assert, tohumlar, sonuç kapısı, çakışma kapısı.
Çalıştır: python test_sekil_devam.py"""
import sys

import numpy as np
import pandas as pd

import SEKIL_DEVAM as SD
import MUM_IZI as MI

ISIM = []


def t(f):
    ISIM.append(f)
    return f


def _seri(n, tohum=1, s=0.02):
    r = np.random.default_rng(tohum)
    C = 20 * np.exp(np.cumsum(r.normal(0, s, n))); O = C * np.exp(r.normal(0, s / 2, n))
    H = np.maximum(O, C) * (1 + np.abs(r.normal(0, s, n))); L = np.minimum(O, C) * (1 - np.abs(r.normal(0, s, n)))
    V = 1000 * np.exp(r.normal(0, 0.3, n))
    return O, H, L, C, V


# ---------------------------------------------------------------- (v) HEDEF / AYNA
@t
def test_hedef_ayna():
    U = 15

    def dep_kur(Hs, Ls, Cs):
        n = 3 + U
        O = np.full(n, 100.0); H = np.full(n, 100.5); L = np.full(n, 99.5); C = np.full(n, 100.0)
        H[2:2 + U] = Hs; L[2:2 + U] = Ls; C[2:2 + U] = Cs
        return {"O": O, "H": H, "L": L, "C": C, "off": np.array([0, n])}
    a = np.array([0.01])                                       # ATRP 1 %: hedef 102, stop 99 (yukarı); ayna hedef 98, stop 101
    Hs = np.full(U, 100.5); Ls = np.full(U, 99.5); Cs = np.full(U, 100.0)
    H1 = Hs.copy(); H1[3] = 102.0                              # hedef 4. barda, stop yok
    R = SD.sd_sonuc_dizi(dep_kur(H1, Ls, Cs), np.array([0]), np.array([1]), a)
    assert R["HEDEF"][0] == 1 and R["AYNA"][0] == 0
    L2 = Ls.copy(); L2[1] = 99.0                               # stop 2. barda, hedef 4. barda -> 0
    assert SD.sd_sonuc_dizi(dep_kur(H1, L2, Cs), np.array([0]), np.array([1]), a)["HEDEF"][0] == 0
    H3 = Hs.copy(); H3[2] = 102.5; L3 = Ls.copy(); L3[2] = 98.9   # aynı barda ikisi -> stop önce
    R3 = SD.sd_sonuc_dizi(dep_kur(H3, L3, Cs), np.array([0]), np.array([1]), a)
    assert R3["HEDEF"][0] == 0 and R3["AYNA"][0] == 0
    L4 = Ls.copy(); L4[5] = 98.0                               # ayna: -2 ATRP önce, +1 yok -> 1
    assert SD.sd_sonuc_dizi(dep_kur(Hs, L4, Cs), np.array([0]), np.array([1]), a)["AYNA"][0] == 1
    H5 = Hs.copy(); H5[4] = 101.0                              # +1 ATRP önce (stop), sonra -2 -> 0
    assert SD.sd_sonuc_dizi(dep_kur(H5, L4, Cs), np.array([0]), np.array([1]), a)["AYNA"][0] == 0
    C6 = Cs.copy(); C6[-1] = 103.0                             # Z15 = (103 / 100 - 1) / (0,01 kök 15)
    R6 = SD.sd_sonuc_dizi(dep_kur(Hs, Ls, C6), np.array([0]), np.array([1]), a)
    assert abs(R6["Z15"][0] - 0.03 / (0.01 * np.sqrt(15))) < 1e-12 and abs(R6["R15"][0] - 0.03) < 1e-12
    assert abs(R6["YOL"][0, -1] - R6["Z15"][0]) < 1e-12


# ---------------------------------------------------------------- (iv) tanımlayıcı
@t
def test_tanim_gelecege_bakmaz():
    O, H, L, C, V = _seri(400, 3); ks = np.array([150, 200, 250, 300]); a = np.full(4, 0.02)
    for Lw in (20, 10):
        T1 = SD.sd_tanim_seri(O, H, L, C, V, ks, Lw, a)
        for k in ks:
            O2, H2, L2, C2, V2 = (x.copy() for x in (O, H, L, C, V))
            r = np.random.default_rng(k)
            for x in (O2, H2, L2, C2):
                x[k + 1:] *= np.exp(r.normal(0, 0.3, len(x) - k - 1))
            V2[k + 1:] *= 50
            T2 = SD.sd_tanim_seri(O2, H2, L2, C2, V2, ks, Lw, a)
            i = int(np.flatnonzero(ks == k)[0])
            for c in ("A", "VOL", "Z0"):
                assert np.array_equal(T1[c][i], T2[c][i]), (Lw, k, c)


@t
def test_tanim_elle():
    O, H, L, C, V = _seri(300, 5); k = 200; Lw = 20; a = 0.021
    T = SD.sd_tanim_seri(O, H, L, C, V, np.array([k]), Lw, np.array([a])); A = T["A"][0]
    assert A.shape == (4 * Lw + 4,) and T["VOL"].shape == (1, Lw) and T["ok"][0]
    i = k - 3                                                   # pencerenin 18. barı
    w = C[i - 19:i + 1]; mu = w.mean(); sd = w.std()            # ddof 0
    p = (i - (k - Lw + 1))
    for q, x in enumerate((O, H, L, C)):
        assert abs(A[4 * p + q] - np.clip((x[i] - mu) / (2 * sd), -3, 3)) < 1e-9
    s = k - Lw + 1
    bw = lambda j: (4 * C[j - 19:j + 1].std()) / C[j - 19:j + 1].mean()  # noqa: E731
    assert abs(A[4 * Lw] - (bw(k) / bw(s) - 1)) < 1e-9
    assert abs(A[4 * Lw + 1] - (L[s:k + 1].min() - H[s - 60:s].max()) / (a * C[k])) < 1e-9
    kon = lambda j: (C[j] - C[j - 119:j + 1].min()) / (C[j - 119:j + 1].max() - C[j - 119:j + 1].min())  # noqa: E731
    assert abs(A[4 * Lw + 2] - kon(s)) < 1e-9 and abs(A[4 * Lw + 3] - kon(k)) < 1e-9
    assert abs(T["VOL"][0, -1] - np.clip(np.log(V[k] / np.median(V[k - 60:k])), -3, 3)) < 1e-9
    assert abs(T["Z0"][0, 1] - (C[k] / C[k - 15] - 1) / a) < 1e-12
    # önceki 60 bar yoksa geçersiz
    assert not SD.sd_tanim_seri(O, H, L, C, V, np.array([70]), Lw, np.array([a]))["ok"][0]


# ---------------------------------------------------------------- (iii) komşu
def _mini_panel(n_h=12, n_ay=30, tohum=7):
    r = np.random.default_rng(tohum); rows = []
    for j in range(n_h):
        for tr in range(0, n_ay * 21, 5):
            rows.append((j, tr))
    j = np.array([x[0] for x in rows]); tr = np.array([x[1] for x in rows]); s15 = tr + 16 + r.integers(0, 3, len(tr))
    tarih = pd.bdate_range("2016-01-04", periods=n_ay * 21 + 40)
    ay = np.asarray(tarih[tr + 1].strftime("%Y-%m")); M = r.normal(size=(len(j), 6)).astype(np.float32)
    return M, j, tr, s15, ay


@t
def test_komsu_yalniz_gecmis_baska_hisse_tam():
    M, j, tr, s15, ay = _mini_panel()
    sorgu = np.flatnonzero(tr >= 400); havuz = np.arange(len(j))
    I, b = SD.sd_komsu(M, sorgu, havuz, j, tr, s15, ay, K=10, is_parcasi=7, isci=2)
    d = SD.sd_komsu_denetim(I, sorgu, j, tr, s15, ay)
    assert not any(d.values()), d
    # saf çözüm (float64) ile karşılaştırma: komşuların en büyük uzaklığı saf K. uzaklığı aşmaz
    for qi in range(0, len(sorgu), 37):
        q = sorgu[qi]; a_ = ay[q]; r0 = tr[sorgu][ay[sorgu] == a_].min()
        uy = np.flatnonzero((tr <= r0 - 20) & (s15 < r0) & (j != j[q]))
        dd = ((M[uy].astype(float) - M[q].astype(float)) ** 2).sum(1); kth = np.sort(dd)[9]
        dk = ((M[I[qi]].astype(float) - M[q].astype(float)) ** 2).sum(1)
        assert dk.max() <= kth + 1e-4 and set(I[qi]) <= set(uy)
    # rastgele komşu da aynı kurala uyar ve tohumla tekrarlanır
    R1, _ = SD.sd_komsu(M, sorgu, havuz, j, tr, s15, ay, K=10, rastgele=True, anahtar="t")
    R2, _ = SD.sd_komsu(M, sorgu, havuz, j, tr, s15, ay, K=10, rastgele=True, anahtar="t")
    assert np.array_equal(R1, R2) and not any(SD.sd_komsu_denetim(R1, sorgu, j, tr, s15, ay).values())
    # bozuk komşu denetimde yakalanır
    I2 = I.copy(); I2[0, 0] = sorgu[0]
    assert sum(SD.sd_komsu_denetim(I2, sorgu, j, tr, s15, ay).values()) > 0


# ---------------------------------------------------------------- (vi) kapılar / tohum
@t
def test_kesik_ve_kapi():
    try:
        SD._sd_tarih_kapi(pd.DatetimeIndex(["2022-12-30", "2023-01-02"]), "deneme"); assert False
    except SD.SDHata:
        pass
    V = {"X": pd.DataFrame({"Close": [1.0]}, index=pd.DatetimeIndex(["2023-01-03"]))}
    try:
        SD.sd_kesik_kapi(V, "deneme"); assert False
    except SD.SDHata:
        pass
    P = {"N": 2, "hucre": np.array(["ABD|d1619", "ABD|d2022"]), "j": np.zeros(2, int), "k": np.zeros(2, int), "atrp": np.ones(2)}
    try:
        SD.sd_sonuc(P, {}, "kesif"); assert False                 # keşifte doğrulama hücresi sonucu istenemez
    except SD.SDHata:
        pass


@t
def test_tohum_tekrar():
    r = np.random.default_rng(3); X = r.normal(size=(600, 5))
    a = SD.sd_kmeans(X, k=8); b = SD.sd_kmeans(X, k=8)
    assert np.array_equal(a["merkez"], b["merkez"]) and np.array_equal(a["etiket"], b["etiket"])
    assert np.array_equal(SD.sd_W(12, "x", 50), SD.sd_W(12, "x", 50)) and not np.array_equal(SD.sd_W(12, "x", 50), SD.sd_W(12, "y", 50))


@t
def test_ic_ve_boot():
    r = np.random.default_rng(4); n = 3000; ay = np.repeat([f"2020-{m:02d}" for m in range(1, 13)], n // 12)
    Z = r.normal(size=n)
    ic = SD.sd_ic_ay(Z, Z, ay); assert np.allclose(ic.to_numpy(), 1.0)
    ic0 = SD.sd_boot_ic(SD.sd_ic_ay(r.normal(size=n), Z, ay), "t", 2000)
    assert ic0["alt"] < 0 < ic0["ust"]
    us, al = SD.sd_uc_maske(Z, ay); assert abs(us.mean() - 0.10) < 0.01 and abs(al.mean() - 0.10) < 0.01


@t
def test_cakisma_kapisi():
    """Colab exec: bellekte aynı adlı bir nesne varken modül yüklenirse durur; temiz ad alanında durmaz."""
    import os
    kod = open(os.path.join(SD.KOK_SD, "SEKIL_DEVAM.py"), encoding="utf-8").read()
    ns = {"__name__": "colab", "__file__": os.path.join(SD.KOK_SD, "SEKIL_DEVAM.py"), "sd_kmeans": object()}
    try:
        exec(compile(kod, "SEKIL_DEVAM.py", "exec"), ns); assert False, "çakışma kapısı durmadı"
    except RuntimeError as ex:
        assert "çakışma kapısı" in str(ex)
    ns2 = {"__name__": "colab", "__file__": os.path.join(SD.KOK_SD, "SEKIL_DEVAM.py")}
    exec(compile(kod, "SEKIL_DEVAM.py", "exec"), ns2)
    assert "sd_kmeans" in ns2


# ---------------------------------------------------------------- (i) / (ii) gömülü kalıp + negatifler; ilişkisiz panel
@t
def test_sentetik_gomulu_ve_ilgisiz():
    J = SD.sd_sentetik_olc(1)
    g = J["gomulu"]; n = J["ilgisiz"]
    assert g["ic"]["A"]["ic"] > 0 and g["ic"]["A"]["alt"] > 0, g["ic"]["A"]           # gömülü ilişki bulundu
    assert g["ust_alt_Z15"]["alt"] > 0
    assert n["ic"]["A"]["alt"] <= 0 <= n["ic"]["A"]["ust"], n["ic"]["A"]               # ilişkisizde aralık sıfırı içerir
    assert g["ic"]["R"]["alt"] <= 0 <= g["ic"]["R"]["ust"]                             # rastgele komşu şans tabanı
    assert g["yakalama_hepsi"] >= 0.90 and min(g["yakalama"].values()) >= 0.80          # kalıp tek kümede toplanıyor
    assert max(g["yanlis_kabul"][x] for x in ("N1", "N2", "N3")) <= 0.30                # negatifler kalıbın kümesine girmiyor
    assert g["iyi5_erken_pay"] >= 0.80                                                  # en iyi 5 küme = kalıbın kendisi / erken evresi
    assert g["kalip_sira"] <= 10 and g["kalip_kume_poz_pay"] >= 0.9


def main() -> int:
    bas = 0
    for f in ISIM:
        try:
            f(); print("GEÇTİ", f.__name__)
        except Exception as ex:   # noqa: BLE001
            bas += 1; print("KALDI", f.__name__, repr(ex))
    print(f"{len(ISIM) - bas} / {len(ISIM)} test geçti")
    return 1 if bas else 0


if __name__ == "__main__":
    sys.exit(main())
