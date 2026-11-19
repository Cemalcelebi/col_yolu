"""test_yapi_hedef — YAPI_HEDEF.py sentetik testleri (gerçek veri gerekmez).

1) yh_sim: hedef / stop / takip / kilit / 15 bar sınırı / bar 0 / High sütunu / yön - aynası / ölçülemezlik
2) yh_getiri: stop (ertesi açılış), ters oluşum, zaman tavanı, kesik
3) sinyaller elle: Y3 kazan + dönüş, Y5 düz tavan SAT, Y1 = S6 al günleri ve hat kuralı, Y4 hafıza (yalnız geçmiş)
4) geleceğe bakma: seri her kesimde kesilince sinyaller tam serinin o güne kadarki sinyalleriyle aynı (Y1 / Y3 / Y4 / Y5)
5) KAT = ORTAK_CETVEL.oc_kat (aynı aralık); BH; etiket kuralı; hücre şartları
6) eş / taban / plasebo AYNI kural (yh_olay_olc elle yeniden üretim; giriş ertesi açılış)
7) güç tekrarı: KAT_ref 1,0 enjeksiyonsuz, 1,5 enjeksiyonlu; güç bakışı muhafazakâr
8) kapı: ön kayıt yok / sha tutmuyor -> durur; kontrol listesi 14 satır kapıdan geçer
9) uçtan uca: sentetik 3 pazar ile onkayit + kos (git'siz) -> sonuc.json, olay csv, RAPOR.md; ikinci koşu durur
10) e-posta / anahtar taraması; çakışma kapısı (bellekteki adı ezince durur)
11) 2. TUR (Y6 / Y7 / Y8 / Y8B): hat dokunuş sayımı, kırılım payı, iki kenar, büyük desen eğimi, Y8 hafızası (elle = kod), prefix (geleceğe
    bakma) değişmezliği bayraklarla, ESIK_TUR1_SHA = 1. tur mührü, E5a stop_uzak düşmesi, E5b bilgi = elle yh_sim; uçtan uca (9'da) 2. tur
    onkayit2 + kos + kapı, Y1-Y5 sonuçları ve RAPOR.md değişmez
12) 3. TUR (Y9 / Y9b / Y9c / Y9d): F1 / F11 / F15 / F17 = GOZ_ETIKET.ge_ozellik_bar, seçim sınırları, çeyrek, özellik birleştirme sembol +
    tarih (karışık sıralı dosya; eksik satır durur), prefix (geleceğe bakma), F15 paneli elle, konum eşli KAT elle = kod, TERS ve 3. tur
    etiketi, ESIK_TUR2_SHA = 2. tur mührü; uçtan uca (9'da) onkayit3 + kos + kapı + Y1 regresyonu, önceki turlar değişmez
Çalıştır: python test_yapi_hedef.py
"""
import copy
import json
import os
import shutil
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
warnings.filterwarnings("ignore")

import ORTAK_CETVEL as OC  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

GECTI, KALDI = [], []


def kontrol(ad, kosul, ek=""):
    (GECTI if kosul else KALDI).append(ad)
    print(("  OK   " if kosul else "  HATA ") + ad + (f"  ({ek})" if ek else ""))


def rastgele_hisse(n, tohum, bas="2016-01-01", oyn=0.02):
    rng = np.random.default_rng(tohum)
    C = 50 * np.exp(np.cumsum(rng.normal(0.0, oyn, n)))
    O = C * (1 + rng.normal(0, 0.006, n))
    a = rng.uniform(0, 0.02, n); b = rng.uniform(0, 0.02, n)
    H = np.maximum(O, C) * (1 + b); L = np.minimum(O, C) * (1 - a)
    V = rng.integers(5000, 80000, n).astype(float)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=pd.bdate_range(bas, periods=n))


def sim1(C, E=100.0, stop0=95.0, yon=1, H=None, L=None):
    C = np.asarray(C, float)[:, None]
    H = C if H is None else np.asarray(H, float)[:, None]
    L = C if L is None else np.asarray(L, float)[:, None]
    S = YH.yh_sim(C, H, L, np.array([E]), np.array([stop0]), yon)
    return {k: (v[0] if hasattr(v, "__len__") else v) for k, v in S.items()}


print("1) yh_sim")
duz = [100.0] * 20
r = sim1([101, 103, 105.5] + duz)
kontrol("+%5 stop'tan önce (bar 2)", r["h5"] == 1 and r["st5"] == 0 and r["k5"] == 2)
r = sim1([99, 96, 94.9] + duz)
kontrol("stop önce (kapanış < 95, bar 2)", r["st5"] == 1 and r["h5"] == 0 and r["kst"] == 2)
r = sim1([104, 96.5] + duz)
kontrol("takip stopu: 104 x 0,93 = 96,72 > 96,5 -> stop", r["st5"] == 1 and r["kst"] == 1)
r = sim1([104, 96.8] + duz)
kontrol("takip stopu sınırın üstünde sürer", r["st5"] == 0 and r["kst"] == -1)
r = sim1([105, 101.9] + duz)
kontrol("+%5 sonra kilit giriş x 1,02 -> 101,9 stop; h5 = 1, h10 = 0", r["h5"] == 1 and r["h10"] == 0 and r["kst"] == 1 and r["st5"] == 0)
r = sim1([105, 110.5, 106.9] + duz)
kontrol("+%10 sonra kilit giriş x 1,07 -> 106,9 stop", r["h10"] == 1 and r["kst"] == 2)
r = sim1([105.2] + duz)
kontrol("giriş barı (bar 0) kapanışı sayılır", r["h5"] == 1 and r["k5"] == 0)
r = sim1([100.0] * 15 + [106.0] + duz)
kontrol("16. bar (bar 15) sayılmaz", r["h5"] == 0 and r["st5"] == 0)
r = sim1([100.0] * 14 + [106.0] + duz)
kontrol("15. bar (bar 14) sayılır", r["h5"] == 1)
r = sim1([100.0] * 10)
kontrol("15 geçerli bar yoksa ölçülmez", (not r["olc"]) and np.isnan(r["h5"]))
Cn = np.array([100.0] * 10 + [np.nan] * 25 + [100.0] * 10)
r = sim1(YH._yh_pencere(Cn[:, None], 0, 30)[:, 0])
kontrol("15 bar 30 takvim satırına sığmazsa ölçülmez", not r["olc"])
r = sim1([102, 103] + duz, H=[106, 103] + duz)
kontrol("High sütunu: H >= 105 -> h5H = 1, kapanış h5 = 0", r["h5H"] == 1 and r["h5"] == 0)
r = sim1([94, 103] + duz, H=[106, 103] + duz)
kontrol("aynı barda kapanış stop'u -> High hedefi sayılmaz", r["h5H"] == 0 and r["st5"] == 1)
r = sim1([99, 97, 94.8] + duz, E=100, stop0=105, yon=-1)
kontrol("yön -: -%5 önce", r["h5"] == 1 and r["st5"] == 0)
r = sim1([101, 104, 105.1] + duz, E=100, stop0=105, yon=-1)
kontrol("yön -: stop (kapanış > 105) önce", r["st5"] == 1)
r = sim1([96, 103.0] + duz, E=100, stop0=105, yon=-1)
kontrol("yön -: takip 96 x 1,07 = 102,72 < 103 -> stop", r["st5"] == 1 and r["kst"] == 1)
r = sim1([95, 98.1] + duz, E=100, stop0=105, yon=-1)
kontrol("yön -: -%5 sonra kilit giriş x 0,98 -> 98,1 stop", r["h5"] == 1 and r["kst"] == 1)
r = sim1([100] + duz, E=100, stop0=101)
kontrol("giriş stop'un ötesinde (stop0 >= giriş) ölçülmez", not r["olc"])

print("2) yh_getiri")
n = 80; O = np.full(n, 100.0); C = np.full(n, 100.0); H = C * 1.04; L = C * 0.96
C2 = C.copy(); C2[3] = 94.0; O2 = O.copy(); O2[4] = 93.0
g, b, t = YH.yh_getiri(O2, H, L, C2, 0, 100.0, 95.0, 1)
kontrol("stop -> ertesi açılış", t == "stop" and b == 4 and abs(g - (-0.07)) < 1e-12, (g, b, t))
Hh = np.full(n, 100.5); Ll = np.full(n, 99.5); C3 = C.copy(); C3[12] = 97.0; O3 = O.copy(); O3[13] = 97.5
g, b, t = YH.yh_getiri(O3, Hh, Ll, C3, 0, 100.0, 90.0, 1)
kontrol("ters oluşum (10 bar bant %1, kapanış < dip x 0,98)", t == "ters" and b == 13 and abs(g + 0.025) < 1e-12, (g, b, t))
g, b, t = YH.yh_getiri(O, H, L, C, 0, 100.0, 90.0, 1)
kontrol("zaman tavanı 60 bar", t == "zaman" and b == 59)
g, b, t = YH.yh_getiri(O[:20], H[:20], L[:20], C[:20], 0, 100.0, 90.0, 1)
kontrol("veri biterse kesik", t == "kesik" and b == 19)
C4 = C.copy(); C4[2] = 106.0; O4 = O.copy(); O4[3] = 104.0
g, b, t = YH.yh_getiri(O4, H, L, C4, 0, 100.0, 105.0, -1)
kontrol("yön -: stop (106 > 105) -> getiri = 1 - çıkış / giriş", t == "stop" and b == 3 and abs(g - (-0.04)) < 1e-12, (g, t))
kontrol("stop yanlış tarafta -> ölçülmez", YH.yh_getiri(O4, H, L, C4, 0, 100.0, 95.0, -1)[2] == "olculmez")

print("3) sinyaller elle")


def kazan_seri():
    rows = []
    for i in range(150):
        rows.append((100.0, 100.8, 99.2, 100.0))
    for i in range(40):                       # düşüş 100 -> 70
        c = 100 - 30 * (i + 1) / 40; rows.append((c + 0.2, c + 0.6, c - 0.6, c))
    n = 40
    for i in range(n):                        # kazan: 70 -> 60 -> 70 (U), sağ kenar yükselir
        x = (i - (n - 1) / 2) / ((n - 1) / 2); c = 60 + 10 * x * x
        if i >= n - 8:
            c = 66 + 0.5 * (i - (n - 8))
        rows.append((c, c + 0.5, c - 0.5, c))
    rows.append((70.0, 76.5, 69.8, 76.0))     # kırılım: kapanış pencere tavanının üstünde
    d = pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"], index=pd.bdate_range("2020-01-01", periods=len(rows)))
    d["Volume"] = 1000.0
    return d


d3 = kazan_seri(); X3 = YH.yh_y3_hisse(d3)
t_son = d3.index[-1]
kontrol("Y3: son gün kazan + dönüş kırılımı", len(X3) and pd.Timestamp(X3.tarih.iloc[-1]) == t_son, X3.tail(1).to_dict("records") if len(X3) else "yok")
if len(X3) and pd.Timestamp(X3.tarih.iloc[-1]) == t_son:
    n3 = int(X3.n.iloc[-1]); W = d3.iloc[-1 - n3:-1]
    kontrol("Y3: hat = pencere [t-n, t-1] dibi, stop0 = hat x 0,98", abs(X3.hat.iloc[-1] - W.Low.min()) < 1e-12 and abs(X3.stop0.iloc[-1] - W.Low.min() * 0.98) < 1e-12)
    kontrol("Y3: tavan = pencere max High (t hariç)", abs(X3.tavan.iloc[-1] - W.High.max()) < 1e-12)
    xs = np.arange(n3) - (n3 - 1) / 2; a = np.polyfit(xs, W.Low.to_numpy(), 2)[0]
    kontrol("Y3: a = np.polyfit x^2 katsayısı > 0", a > 0 and abs(a - float(W.Low.to_numpy() @ YH._yh_kare_agirlik(n3))) < 1e-9)
d3b = d3.copy(); d3b.iloc[:190, :4] = d3b.iloc[:190, :4].to_numpy() * 0 + np.array([60.5, 61, 60, 60.5])   # önceki düşüş yok: 120 bar tepesi = kırılım
kontrol("Y3: tepeye yakınsa (120 bar tepesinden < %15 aşağı) sinyal yok", not len(YH.yh_y3_hisse(d3b)) or pd.Timestamp(YH.yh_y3_hisse(d3b).tarih.iloc[-1]) != t_son)


def tavan_seri(kir=True):
    rows = []
    for i in range(100):
        rows.append((80.0, 80.8, 79.2, 80.0))
    for i in range(40):                       # yükseliş 80 -> 110
        c = 80 + 30 * (i + 1) / 40; rows.append((c - 0.2, c + 0.5, c - 0.5, c))
    for i in range(20):                       # düz tavan 110 (bant ~%3)
        c = 110 + (0.4 if i % 2 else -0.4); rows.append((c, 111.5, 108.5, c))
    rows.append((109.0, 109.2, 104.0, 104.5 if kir else 108.8))
    d = pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"], index=pd.bdate_range("2020-01-01", periods=len(rows)))
    d["Volume"] = 1000.0
    return d


d5 = tavan_seri(); X5 = YH.yh_y5_hisse(d5)
ok5 = len(X5) and pd.Timestamp(X5.tarih.iloc[-1]) == d5.index[-1]
kontrol("Y5: düz tavan SAT son gün", ok5, X5.tail(1).to_dict("records") if len(X5) else "yok")
if ok5:
    n5 = int(X5.n.iloc[-1]); W = d5.iloc[-1 - n5:-1]
    kontrol("Y5: stop0 = pencere max H x 1,02, yön -", abs(X5.stop0.iloc[-1] - W.High.max() * 1.02) < 1e-12 and int(X5.yon.iloc[-1]) == -1)
    kontrol("Y5: kırılım kapanış < pencere min L x 0,98", d5.Close.iloc[-1] < W.Low.min() * 0.98)
X5b = YH.yh_y5_hisse(tavan_seri(kir=False))
kontrol("Y5: kırılım yoksa sinyal yok", not len(X5b) or pd.Timestamp(X5b.tarih.iloc[-1]) != d5.index[-1])

import S6_TABAN as S6  # noqa: E402
import SIKISMA_YENIDEN as SY  # noqa: E402
dr = rastgele_hisse(900, 11, oyn=0.012)
X1, X4 = YH.yh_s6_hisse(dr)
T = S6.s6_taban(SY.sy_veri_hazirla(dr, SY.SY_ESIK))
gun = set(T.index[T.al.to_numpy(bool)])
kontrol("Y1 = S6 al günleri", set(pd.to_datetime(X1.tarih)) <= gun and len(X1) > 0 and len(gun - set(pd.to_datetime(X1.tarih))) == int((~np.isfinite(
    np.where(T.durum.to_numpy(object) == "AL", T.kutu_alt.to_numpy(float), np.r_[np.nan, T.dip.to_numpy(float)[:-1]])[T.al.to_numpy(bool)])).sum()), f"{len(X1)} / {len(gun)}")
okh = True
for rr in X1.itertuples():
    i = T.index.get_loc(pd.Timestamp(rr.tarih))
    bek = T.kutu_alt.iloc[i] if T.durum.iloc[i] == "AL" else T.dip.iloc[i - 1]
    okh &= abs(rr.hat - bek) < 1e-12
kontrol("Y1 hat = kutu_alt (AL) / DİP(t-1) (AL_BOLGESIZ)", okh)
kontrol("Y4 ⊆ Y1 ve hafıza >= 0", set(pd.to_datetime(X4.tarih)) <= set(pd.to_datetime(X1.tarih)) and (X4.hafiza >= 0).all())
# Y4 hafızası elle (bir olay)
okm = True
du = T.durum.to_numpy(object); Cc = dr.Close.to_numpy(); Oo = dr.Open.to_numpy()
for rr in X1.itertuples():
    i = T.index.get_loc(pd.Timestamp(rr.tarih)); hit = kir = 0
    for a in range(max(0, i - 250), i):
        if du[a] == "AL" and a + 15 <= i and Cc[a + 1:a + 16].max() >= Oo[a + 1] * 1.05:
            hit += 1
        if du[a] == "KIRILDI":
            kir += 1
    okm &= (hit - kir) == rr.hafiza
kontrol("Y4 hafıza elle = kod (a + 15 <= t)", okm)

print("4) geleceğe bakma (kesik seri = tam seri)")
for ad, f in (("Y3", lambda x: YH.yh_y3_hisse(x)), ("Y5", lambda x: YH.yh_y5_hisse(x)),
              ("Y1", lambda x: YH.yh_s6_hisse(x)[0]), ("Y4", lambda x: YH.yh_s6_hisse(x)[1])):
    tamam = True; say = 0
    for toh in (3, 5, 8):
        dx = rastgele_hisse(700, toh, oyn=0.015)
        Full = f(dx); Full["tarih"] = pd.to_datetime(Full.tarih)
        kes = sorted(set(list(Full.tarih[::3])[:12]) | set(dx.index[[300, 420, 555, 699]]))
        for t in kes:
            Z = f(dx[dx.index <= t]); Z["tarih"] = pd.to_datetime(Z.tarih)
            A = Full[Full.tarih <= t].reset_index(drop=True); B = Z.reset_index(drop=True)
            if len(A) != len(B) or not (np.allclose(A.stop0.to_numpy(float), B.stop0.to_numpy(float), rtol=0, atol=1e-9) and (A.tarih == B.tarih).all()):
                tamam = False
            say += 1
    kontrol(f"{ad}: {say} kesimde kesik = tam (tarih + stop0)", tamam)
kontrol("Y3 kazan serisi kesik = tam", len(YH.yh_y3_hisse(d3.iloc[:-1])) == len(X3) - 1 or len(YH.yh_y3_hisse(d3.iloc[:-1])) == len(X3[pd.to_datetime(X3.tarih) < t_son]))

print("5) KAT, BH, etiket, hücre")
rng = np.random.default_rng(5)
a = (rng.random(400) < 0.4).astype(float); b = rng.uniform(0.2, 0.4, 400)
ay = np.array([f"2023-{1 + i % 12:02d}" for i in range(400)])
k1 = YH.yh_kat(a, b, ay); k2 = OC.oc_kat(a, b, ay)
kontrol("yh_kat = OC.oc_kat (kat, alt, üst)", all(abs(k1[x] - k2[x]) < 1e-12 for x in ("kat", "alt", "ust")), (k1["kat"], k1["alt"], k1["ust"]))
kontrol("BH", YH._yh_bh([0.001, 0.2, 0.03, np.nan, 0.5], 0.10) == [True, False, True, False, False])
D = {("ABD", "2023"): "TUTAR", ("ABD", "2024-26"): "TUTAR", ("AVR", "2023"): "TUTAR", ("AVR", "2024-26"): "TUTAR"}
kontrol("etiket İZ", YH.yh_etiket(D) == "İZ")
D2 = dict(D); D2[("BIST", "2023")] = "TUTAR"; D2[("BIST", "2024-26")] = "TUTAR"
kontrol("etiket İZ + BIST", YH.yh_etiket(D2) == "İZ + BIST")
D3 = dict(D); D3[("AVR", "2023")] = "DESTEKLENMEDİ"; D3[("AVR", "2024-26")] = "ÖLÇÜLEMEDİ"
kontrol("etiket EMARE (tek pazar iki dönem)", YH.yh_etiket(D3).startswith("EMARE (ABD 2023, ABD 2024-26"))
D4 = {k: "DESTEKLENMEDİ" for k in D}; D4[("ABD", "2023")] = "TUTAR"
kontrol("etiket tek hücre -> DESTEKLENMEDİ (tek hücre tuttu)", YH.yh_etiket(D4).startswith("DESTEKLENMEDİ (tek hücre tuttu: ABD 2023"))
D5 = dict(D4); D5[("AVR", "2023")] = "ÖLÇÜLEMEDİ"
kontrol("etiket tek hücre + güçsüz -> ÖLÇÜLEMEDİ", YH.yh_etiket(D5).startswith("ÖLÇÜLEMEDİ (tek hücre"))
kontrol("etiket hepsi DESTEKLENMEDİ", YH.yh_etiket({k: "DESTEKLENMEDİ" for k in D}) == "DESTEKLENMEDİ")
kontrol("etiket karışık -> ÖLÇÜLEMEDİ; 'iz değil' yok", YH.yh_etiket({**{k: "DESTEKLENMEDİ" for k in D}, ("AVR", "2023"): "ÖLÇÜLEMEDİ"}) == "ÖLÇÜLEMEDİ")
nh = 400
Xh = pd.DataFrame({"giris": pd.to_datetime(ay.astype(object) + "-15"), "h5": a, "es_h5": b * 0.8, "h10": a * 0, "es_h10": b * 0, "st5": 1 - a,
                   "es_st5": np.full(nh, 0.9), "h5H": a, "es_h5H": b, "h10H": a * 0, "es_h10H": b * 0, "tb_h5": b, "tb_h10": b, "tb_st5": b,
                   "pl_h5": b * 0.8, "pl_h10": b, "pl_st5": b, "getiri": rng.normal(0, 0.05, nh), "cikis_bar": rng.integers(0, 60, nh),
                   "cikis_tur": "stop", "dd": 0.05})
h = YH.yh_hucre(Xh)
kontrol("hücre: dört şart -> TUTAR", h["tutar"] and h["s_kat"] and h["s_stop"] and h["s_plasebo"], (h["h5_kat"], h["h5_alt"], h["pl_h5_alt"]))
Xh2 = Xh.copy(); Xh2["es_st5"] = 0.3
kontrol("hücre: stop payı eşten büyükse TUTMAZ", not YH.yh_hucre(Xh2)["tutar"])
Xh3 = Xh.copy(); Xh3["pl_h5"] = a
kontrol("hücre: plasebo KAT alt <= 1 ise TUTMAZ", not YH.yh_hucre(Xh3)["tutar"])
kontrol("hücre: n < 30 -> ÖLÇÜLEMEDİ", YH.yh_durum(YH.yh_hucre(Xh.iloc[:20]), 1, None)[0] == "ÖLÇÜLEMEDİ")
tablo = {"guc": {"1": {"300": {"1.25": {"0.03": 0.9, "0.06": 0.7, "0.10": 0.95}}, "1000": {"1.25": {"0.03": 0.99, "0.06": 0.99, "0.10": 0.99}}}}}
kontrol("güç bakışı: n'e küçük-eşit satır, d'lerin en küçüğü", YH.yh_guc_bak(999, 1, tablo) == 0.7 and YH.yh_guc_bak(1000, 1, tablo) == 0.99 and YH.yh_guc_bak(200, 1, tablo) == 0.0)
kontrol("durum: n 400 tutmaz güç %70 -> ÖLÇÜLEMEDİ", YH.yh_durum({"n": 400, "tutar": False}, 1, tablo)[0] == "ÖLÇÜLEMEDİ")
kontrol("durum: n 1.000 tutmaz -> DESTEKLENMEDİ", YH.yh_durum({"n": 1000, "tutar": False}, 1, tablo)[0] == "DESTEKLENMEDİ")

print("6) eş / taban / plasebo aynı kural")
Vs = {f"S{i:02d}": rastgele_hisse(400, 100 + i) for i in range(40)}
Vd = OC._oc_veri_sar(Vs, "ABD"); P = OC.oc_panel(Vd); Cl = YH.yh_kapanis(P, Vd)
sig = pd.DataFrame({"sembol": ["S03", "S07"], "tarih": [Vs["S03"].index[200], Vs["S07"].index[250]], "pazar": "ABD"})
sig["hat"] = [Vs["S03"].Low.iloc[190:201].min(), Vs["S07"].Low.iloc[240:251].min()]; sig["stop0"] = sig.hat * 0.98; sig["yon"] = 1
Z, say = YH.yh_olc_pazar(Vd, P, Cl, sig, "Y1", "ABD")
kontrol("olaylar ölçüldü", len(Z) == 2 and Z.olc.all(), say)
r0 = Z.iloc[0]; d, j = int(r0.d), int(r0.j)
kontrol("giriş = sinyalden sonraki ilk bar açılışı", r0.giris == Vs["S03"].index[201] and abs(r0.E0 - Vs["S03"].Open.iloc[201]) < 1e-12)
es = [k for k in range(len(P["sembol"])) if k != j and P["ok"][d, k] and P["H"][d, k] == P["H"][d, j]]
vals = []
for k in es:
    S_ = YH.yh_sim(YH._yh_pencere(Cl, d, 30, np.array([k])), YH._yh_pencere(P["Hi"], d, 30, np.array([k])), YH._yh_pencere(P["Lo"], d, 30, np.array([k])),
                   np.array([P["Op"][d, k]]), np.array([P["Op"][d, k] * (1 - r0.dd)]), 1)
    if S_["olc"][0]:
        vals.append(S_["h5"][0])
kontrol("eş h5 = elle (aynı kova, aynı d, tek tek yh_sim)", len(vals) == int(r0.n_es) and abs(np.mean(vals) - r0.es_h5) < 1e-12, (len(vals), r0.n_es))
dp = int(r0.pl_d)
S_ = YH.yh_sim(YH._yh_pencere(Cl, dp, 30, np.array([j])), YH._yh_pencere(P["Hi"], dp, 30, np.array([j])), YH._yh_pencere(P["Lo"], dp, 30, np.array([j])),
               np.array([P["Op"][dp, j]]), np.array([P["Op"][dp, j] * (1 - r0.dd)]), 1)
kontrol("plasebo: aynı hisse, farklı gün, aynı dönem, aynı d", dp != d and P["ok"][dp, j] and S_["h5"][0] == r0.pl_h5
        and OC._oc_donem(pd.Series([P["tarih"][dp]]), OC.OC_ESIK)[0] == r0.donem)
Z2, _ = YH.yh_olc_pazar(Vd, P, Cl, sig, "Y1", "ABD")
kontrol("plasebo deterministik (tohum)", (Z2.pl_d.to_numpy() == Z.pl_d.to_numpy()).all())
sig2 = sig.copy(); sig2.loc[0, "stop0"] = Vs["S03"].Open.iloc[201] * 1.01
Z3, say3 = YH.yh_olc_pazar(Vd, P, Cl, sig2, "Y1", "ABD")
kontrol("giriş stop'un ötesinde -> ölçülmez, sayımda", say3["giris_stop_otesi"] == 1 and not bool(Z3.olc.iloc[0]))

print("7) güç")
Hv = pd.DataFrame({"ay": np.repeat([f"2024-{m:02d}" for m in range(1, 13)], 50), "h5": (np.random.default_rng(1).random(600) < 0.3).astype(float),
                   "st5": (np.random.default_rng(2).random(600) < 0.3).astype(float), "es_h5": 0.3, "es_st5": 0.3, "pl_h5": 0.3, "yon": 1, "dd": 0.05})
g0 = np.mean([YH.yh_guc_tekrar(Hv, 300, 1.0, np.random.default_rng(i)) for i in range(40)])
g2 = np.mean([YH.yh_guc_tekrar(Hv, 300, 1.6, np.random.default_rng(i)) for i in range(40)])
kontrol("güç: KAT 1,0 düşük, KAT 1,6 yüksek", g0 < 0.2 and g2 > 0.8, (g0, g2))

print("8) kapı")
tmp = tempfile.mkdtemp(prefix="yh_test_")
try:
    try:
        YH.yh_kapi(tmp, git=False); kontrol("ön kayıt yok -> durur", False)
    except YH.YHHata:
        kontrol("ön kayıt yok -> durur", True)
    import IZ_KARNE as IK
    yk = os.path.join(tmp, "k.md"); open(yk, "w", encoding="utf-8").write(YH.yh_kontrol_tablosu())
    kontrol("kontrol listesi 14 satır, kapıdan geçer", IK.ik_kontrol_kapisi(yk)["gecti"] and len(__import__("re").findall(r"(?m)^\| K\d{1,2} \|", YH.yh_kontrol_tablosu())) == 14)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("9) uçtan uca (sentetik 3 pazar, git'siz)")
tmp = tempfile.mkdtemp(prefix="yh_uc_"); veri = os.path.join(tmp, "veri"); cikti = os.path.join(tmp, "cikti"); os.makedirs(veri); os.makedirs(cikti)
yol_eski = dict(YH.YH_YOL)
try:
    for pi, p in enumerate(["ABD", "AVR", "BIST"]):
        V_ = {f"{p}{i:02d}": rastgele_hisse(1900, 1000 * pi + i, bas="2019-01-01", oyn=0.015) for i in range(45)}
        pd.to_pickle(V_, os.path.join(veri, f"V_{p}.pkl"))
    y2 = pd.DataFrame({"satir": "TAM_DIP", "pazar": "ABD", "sembol": ["ABD01", "ABD02"], "tarih": pd.to_datetime(["2023-03-01", "2024-05-01"])})
    y2["giris"] = y2.tarih + pd.offsets.BDay(1)
    y2p = os.path.join(tmp, "olay_TAM_DIP.csv.gz"); y2.to_csv(y2p, index=False)
    YH.YH_YOL["y2_olay"] = y2p; YH.YH_YOL["is_tanimi"] = os.path.join(tmp, "yok.md"); YH.YH_YOL["satir_buyuk"] = os.path.join(tmp, "buyuk")
    J = {"yh_esik_sha": YH.yh_esik_sha(), "surum": "test", "guc": {str(y): {str(n): {f"{k:.2f}": {f"{dd:.2f}": 0.5 for dd in YH.YH_ESIK["guc"]["d"]}
                                                                         for k in YH.YH_ESIK["guc"]["kat_ref"]} for n in YH.YH_ESIK["guc"]["n"]} for y in (1, -1)},
         "havuz_ozet": {}, "zaman_utc": "x"}
    open(os.path.join(cikti, "guc_tablosu.json"), "w").write(json.dumps(J))
    yo = YH.yh_onkayit_yaz(cikti, veri, islem=1)
    kontrol("onkayit yazıldı, kontrol kapısı geçer", os.path.exists(yo) and YH.yh_kapi(cikti, git=False)["kontrol"])
    R = YH.yh_kos(None, cikti, veri, islem=2, git=False)
    J2 = json.load(open(os.path.join(cikti, "sonuc.json"), encoding="utf-8"))
    kontrol("sonuc.json beş deneme + etiket", set(J2["deneme"]) == set(YH.YH_DENEMELER) and all("etiket" in v for v in J2["deneme"].values()),
            {k: v["etiket"] for k, v in J2["deneme"].items()})
    kontrol("geleceğe bakma denetimi koşuda TUTTU", all(v >= 0 for d_ in J2["gelecek_denetimi"].values() for v in d_.values()))
    kontrol("RAPOR.md başlıkları", all(x in R["rapor"] for x in ("ÖZET", "HÜCRE TABLOSU", "OLASILIK TABLOSU", "YENİDEN ÜRETİM", "KONTROL LİSTESİ")))
    f1 = os.path.join(cikti, "olay_Y1.csv.gz")
    if os.path.exists(f1):
        x = pd.read_csv(f1); hh = [h for h in J2["deneme"]["Y1"]["hucre"] if h["pazar"] == "ABD" and h["donem"] == "2023"][0]
        x = x[(x.pazar == "ABD") & (x.donem == "2023") & x.h5.notna() & x.es_h5.notna()]
        kontrol("yeniden üretim: satır dosyasından KAT5 = sonuc.json", len(x) == hh["n"] and (len(x) == 0 or abs(x.h5.sum() / x.es_h5.sum() - hh["h5_kat"]) < 1e-4),
                (len(x), hh.get("h5_kat")))
    try:
        YH.yh_kos(["Y1"], cikti, veri, git=False); kontrol("ikinci koşu durur", False)
    except YH.YHHata:
        kontrol("ikinci koşu durur", True)
    m = open(yo, encoding="utf-8").read().replace(YH.yh_esik_sha(), "0" * 64)
    open(yo, "w", encoding="utf-8").write(m)
    try:
        YH.yh_kapi(cikti, git=False); kontrol("sha tutmuyor -> durur", False)
    except YH.YHHata:
        kontrol("sha tutmuyor -> durur", True)
    # ---- 2. tur uçtan uca (1. tur mührü = yh_esik_sha_tur1; gerçekteki gibi ON_KAYIT.md ve güç tablosu 1. tur sha'sını taşır)
    t1 = YH.yh_esik_sha_tur1()
    open(yo, "w", encoding="utf-8").write(m.replace("0" * 64, t1))
    J["yh_esik_sha"] = t1; open(os.path.join(cikti, "guc_tablosu.json"), "w").write(json.dumps(J))
    J_once = json.load(open(os.path.join(cikti, "sonuc.json"), encoding="utf-8"))
    rapor1 = open(os.path.join(cikti, "RAPOR.md"), "rb").read()
    try:
        YH.yh_kos(["Y6"], cikti, veri, git=False); kontrol("2. tur: ön kayıt 2 yokken koşu durur", False)
    except YH.YHHata:
        kontrol("2. tur: ön kayıt 2 yokken koşu durur", True)
    yo2 = YH.yh_onkayit2_yaz(cikti, veri, islem=1, git=False)
    m2 = open(yo2, encoding="utf-8").read()
    kontrol("2. tur: ON_KAYIT_2 yazıldı, ESIK_TUR1_SHA ve kontrol kapısı", f"ESIK_TUR1_SHA: `{t1}`" in m2 and YH.yh_kapi(cikti, git=False, tur=2)["kontrol"]
            and "Y6 hunisi" in m2 and "Y7 hunisi" in m2)
    try:
        YH.yh_kos(["Y6", "Y1"], cikti, veri, git=False); kontrol("2. tur: 1. ve 2. tur aynı koşuda olmaz", False)
    except YH.YHHata:
        kontrol("2. tur: 1. ve 2. tur aynı koşuda olmaz", True)
    R2 = YH.yh_kos(["Y6", "Y7", "Y8"], cikti, veri, islem=2, git=False)
    J3 = json.load(open(os.path.join(cikti, "sonuc.json"), encoding="utf-8"))
    kontrol("2. tur: Y6 / Y7 / Y8 + Y8B (bilgi) eklendi", set(J3["deneme"]) == set(YH.YH_DENEMELER + YH.YH_DENEMELER_2) and J3["deneme"]["Y8B"].get("bilgi") is True)
    kontrol("2. tur: Y1-Y5 sonuçları, sayımı ve BH'si AYNEN", all(J3["deneme"][k] == J_once["deneme"][k] for k in YH.YH_DENEMELER)
            and J3["bh"] == J_once["bh"] and all(J3["sayim"][k] == J_once["sayim"][k] for k in YH.YH_DENEMELER) and "bh_tur2" in J3)
    kontrol("2. tur: RAPOR.md değişmedi, RAPOR_2.md başlıkları", open(os.path.join(cikti, "RAPOR.md"), "rb").read() == rapor1
            and all(x in R2["rapor"] for x in ("SONUÇ", "HUNİ", "HÜCRE TABLOSU", "OLASILIK TABLOSU", "E5b", "YENİDEN ÜRETİM", "KONTROL LİSTESİ")))
    kontrol("2. tur: huni taban aşaması = 1. tur Y1 / Y3 girdisi", all(J3["huni"][p]["Y6"]["asama"][0]["sinyal"] == J3["sayim"]["Y1"][p]["girdi"]
                                                                        and J3["huni"][p]["Y7"]["asama"][0]["sinyal"] == J3["sayim"]["Y3"][p]["girdi"] for p in J3["huni"]))
    pz6 = {h["pazar"] for h in J3["deneme"]["Y6"]["hucre"] if h.get("n_ham", 0) > 0}
    kontrol("2. tur: stop_uzak sayımı olay olan her pazarda", all("stop_uzak" in J3["sayim"]["Y6"][p] for p in pz6), (pz6, J3["sayim"]["Y6"]))
    try:
        YH.yh_kos(["Y7"], cikti, veri, git=False); kontrol("2. tur: ikinci koşu durur", False)
    except YH.YHHata:
        kontrol("2. tur: ikinci koşu durur", True)
    open(yo2, "w", encoding="utf-8").write(m2.replace(f"ESIK_TUR1_SHA: `{t1}`", "ESIK_TUR1_SHA: `" + "1" * 64 + "`"))
    try:
        YH.yh_kapi(cikti, git=False, tur=2); kontrol("2. tur: Y1-Y5 mührü tutmazsa kapı durur", False)
    except YH.YHHata:
        kontrol("2. tur: Y1-Y5 mührü tutmazsa kapı durur", True)
    # ---- 3. tur uçtan uca (gerçekteki gibi ON_KAYIT_2.md 2. tur sha'sını taşır: yh_esik_sha_tur2; özellik dosyası = Y1 olay satırları)
    t2 = YH.yh_esik_sha_tur2()
    open(yo2, "w", encoding="utf-8").write(m2.replace(YH.yh_esik_sha(), t2))
    J_once3 = json.load(open(os.path.join(cikti, "sonuc.json"), encoding="utf-8"))
    rapor2 = open(os.path.join(cikti, "RAPOR_2.md"), "rb").read()
    O1t = pd.read_csv(os.path.join(cikti, "olay_Y1.csv.gz"), parse_dates=["tarih"])
    oz = []
    for (pz, sb), g in O1t.groupby(["pazar", "sembol"]):
        Vt = pd.read_pickle(os.path.join(veri, f"V_{pz}.pkl"))[sb]
        Ft = YH.yh_y9_ozellik(Vt, list(g.tarih)); Ft.insert(0, "tarih", g.tarih.to_numpy()); Ft.insert(0, "sembol", sb); Ft.insert(0, "pazar", pz)
        oz.append(Ft)
    ozt = pd.concat(oz, ignore_index=True).sample(frac=1.0, random_state=3)          # satır sırası karışık: eşleme sembol + tarih ile
    ozt.insert(3, "durum", "AL"); yoz = os.path.join(tmp, "ozellik_Y1.csv.gz"); ozt.to_csv(yoz, index=False, float_format="%.6g", compression="gzip")
    YH.YH_YOL["ozellik"] = yoz
    try:
        YH.yh_kos(["Y9"], cikti, veri, git=False); kontrol("3. tur: ön kayıt 3 yokken koşu durur", False)
    except YH.YHHata:
        kontrol("3. tur: ön kayıt 3 yokken koşu durur", True)
    yo3 = YH.yh_onkayit3_yaz(cikti, veri, islem=1, git=False)
    m3 = open(yo3, encoding="utf-8").read()
    kontrol("3. tur: ON_KAYIT_3 yazıldı (§2 notu aynen, bakılmış işareti, ESIK_TUR2_SHA, OZELLIK_SHA, kapı)",
            f"ESIK_TUR2_SHA: `{t2}`" in m3 and YH._yh_is_tanimi3_s2() in m3 and "BAKILMIŞ HÜCRE İŞARETİ" in m3 and "OZELLIK_SHA" in m3
            and "Y9 hunisi" in m3 and YH.yh_kapi3(cikti, git=False)["kontrol"])
    try:
        YH.yh_kos(["Y9", "Y6"], cikti, veri, git=False); kontrol("3. tur: başka turla aynı koşuda olmaz", False)
    except YH.YHHata:
        kontrol("3. tur: başka turla aynı koşuda olmaz", True)
    R3 = YH.yh_kos(["Y9", "Y9b", "Y9c", "Y9d"], cikti, veri, islem=2, git=False)
    J4 = json.load(open(os.path.join(cikti, "sonuc.json"), encoding="utf-8"))
    kontrol("3. tur: Y9 / Y9b / Y9c / Y9d eklendi, Y9d bilgi", set(J4["deneme"]) == set(YH.YH_DENEMELER + YH.YH_DENEMELER_2 + YH.YH_DENEMELER_3)
            and J4["deneme"]["Y9d"].get("bilgi") is True)
    kontrol("3. tur: önceki turların sonuçları, sayımı, BH'si, hunisi AYNEN", all(J4["deneme"][k] == J_once3["deneme"][k] for k in YH.YH_DENEMELER + YH.YH_DENEMELER_2)
            and J4["bh"] == J_once3["bh"] and J4["bh_tur2"] == J_once3["bh_tur2"] and J4["huni"] == J_once3["huni"]
            and all(J4["sayim"][k] == J_once3["sayim"][k] for k in YH.YH_DENEMELER + YH.YH_DENEMELER_2) and "bh_tur3" in J4)
    kontrol("3. tur: RAPOR.md / RAPOR_2.md değişmedi, RAPOR_3.md başlıkları", open(os.path.join(cikti, "RAPOR.md"), "rb").read() == rapor1
            and open(os.path.join(cikti, "RAPOR_2.md"), "rb").read() == rapor2
            and all(x in R3["rapor"] for x in ("SONUÇ", "HUNİ", "HÜCRE TABLOSU", "KONUM EŞLİ KAT", "OLASILIK TABLOSU", "DIŞ SINAMA", "BIST (bilgi",
                                                "İKİ YÖNLÜ", "BAKILMIŞ", "YENİDEN ÜRETİM", "KONTROL LİSTESİ")))
    kontrol("3. tur: etiket en fazla EMARE (İZ yazılmaz), ters etiket ve kural etiketi var",
            all(not J4["deneme"][k]["etiket"].startswith("İZ") and "ters_etiket" in J4["deneme"][k] and "etiket_kural" in J4["deneme"][k] for k in YH.YH_DENEMELER_3))
    rg = J4.get("regresyon_y1", {})
    kontrol("3. tur: Y1 regresyonu (ölçülen satır = olay_Y1 satırı) her ölçülen deneme x pazarda", all(v["esit"] for d_ in rg.values() for v in d_.values())
            and sum(v["n"] for d_ in rg.values() for v in d_.values()) > 0, {k: {p: v["n"] for p, v in d_.items()} for k, d_ in rg.items()})
    n9 = {k: sum(h.get("n_ham", 0) for h in J4["deneme"][k]["hucre"]) for k in YH.YH_DENEMELER_3}
    kontrol("3. tur: Y9 + Y9c + Y9d <= Y1 olay; Y9b <= Y9", n9["Y9"] + n9["Y9c"] + n9["Y9d"] <= len(O1t) and n9["Y9b"] <= n9["Y9"], n9)
    f9 = os.path.join(cikti, "olay_Y9c.csv.gz")
    if os.path.exists(f9):
        x9 = pd.read_csv(f9)
        kontrol("3. tur: satır dosyasında konum eş sütunları, olay F15 >= 0,75", {"k_es_h5", "k_n_es", "q_olay", "q_panel", "es_f15_ort"} <= set(x9.columns)
                and (x9.F15 >= 0.75).all() and (x9.q_olay == 3).all())
        for hh in J4["deneme"]["Y9c"]["hucre"]:
            if hh.get("k_n", 0) > 0:
                xx = x9[(x9.pazar == hh["pazar"]) & (x9.donem == hh["donem"]) & x9.h5.notna() & x9.k_es_h5.notna()]
                kontrol("3. tur: yeniden üretim konum eşli KAT5 = sonuc.json", len(xx) == hh["k_n"] and abs(xx.h5.sum() / xx.k_es_h5.sum() - hh["k_h5_kat"]) < 1e-4,
                        (hh["pazar"], hh["donem"], len(xx), hh["k_h5_kat"]))
                break
    try:
        YH.yh_kos(["Y9b"], cikti, veri, git=False); kontrol("3. tur: ikinci koşu durur", False)
    except YH.YHHata:
        kontrol("3. tur: ikinci koşu durur", True)
    open(yo3, "w", encoding="utf-8").write(m3.replace(f"ESIK_TUR2_SHA: `{t2}`", "ESIK_TUR2_SHA: `" + "2" * 64 + "`"))
    try:
        YH.yh_kapi3(cikti, git=False); kontrol("3. tur: Y1-Y8B mührü tutmazsa kapı durur", False)
    except YH.YHHata:
        kontrol("3. tur: Y1-Y8B mührü tutmazsa kapı durur", True)
    open(yo3, "w", encoding="utf-8").write(m3)
    # ---- 4. tur uçtan uca (gerçekteki gibi ON_KAYIT_3.md 3. tur sha'sını taşır: yh_esik_sha_tur3; F1-F18 + S7 dosyaları = Y1 olay satırları)
    import GOZ_ETIKET as GE
    t3 = YH.yh_esik_sha_tur3()
    open(yo3, "w", encoding="utf-8").write(m3.replace(YH.yh_esik_sha(), t3))
    J_once4 = json.load(open(os.path.join(cikti, "sonuc.json"), encoding="utf-8"))
    rapor3 = open(os.path.join(cikti, "RAPOR_3.md"), "rb").read()
    oz4 = []
    for (pz, sb), g in O1t.groupby(["pazar", "sembol"]):
        Vt = pd.read_pickle(os.path.join(veri, f"V_{pz}.pkl"))[sb]
        Fs_, _ = GE.ge_ozellik_hisse(Vt, list(pd.to_datetime(g.tarih)))
        F_ = pd.DataFrame(Fs_); F_.insert(0, "tarih", pd.to_datetime(g.tarih).to_numpy()); F_.insert(0, "sembol", sb); F_.insert(0, "pazar", pz)
        oz4.append(F_)
    oz4 = pd.concat(oz4, ignore_index=True).sample(frac=1.0, random_state=5); oz4.insert(3, "durum", "AL")
    yoz4 = os.path.join(tmp, "ozellik_Y1_tam.csv.gz"); oz4.to_csv(yoz4, index=False, float_format="%.6g", compression="gzip")
    YH.YH_YOL["ozellik"] = yoz4; YH.YH_YOL["ozellik_s7"] = os.path.join(tmp, "ozellik_Y1_s7.csv.gz")
    try:
        YH.yh_kos(["Y10"], cikti, veri, git=False); kontrol("4. tur: ön kayıt 4 yokken koşu durur", False)
    except YH.YHHata:
        kontrol("4. tur: ön kayıt 4 yokken koşu durur", True)
    try:
        YH.yh_onkayit4_yaz(cikti, veri, git=False); kontrol("4. tur: S7 özellik dosyası yokken ön kayıt yazılmaz", False)
    except YH.YHHata:
        kontrol("4. tur: S7 özellik dosyası yokken ön kayıt yazılmaz", True)
    Rs7 = YH.yh_s7_ozellik_yaz(veri, cikti, ozellik=yoz4)
    kontrol("4. tur: S7 dosyası = Y1 olay satırları, prefix denetimi tuttu", Rs7["satir"] == len(oz4) == len(O1t)
            and all(v["prefix_tuttu"] > 0 for v in Rs7["pazar"].values()), Rs7["pazar"])
    yo4 = YH.yh_onkayit4_yaz(cikti, veri, islem=1, git=False)
    m4 = open(yo4, encoding="utf-8").read()
    kontrol("4. tur: ON_KAYIT_4 yazıldı (S7 tanımı aynen, ESIK_TUR3_SHA, S7_OZELLIK_SHA, GE_KOD_SHA, huni Ş1..Ş8, kapı)",
            f"ESIK_TUR3_SHA: `{t3}`" in m4 and YH._yh_is_tanimi4_s2() in m4 and "S7_OZELLIK_SHA" in m4 and "GE_KOD_SHA" in m4 and "Y10 hunisi" in m4
            and "+ Ş8" in m4 and "= Y10b" in m4 and YH.yh_kapi4(cikti, git=False)["kontrol"])
    try:
        YH.yh_kos(["Y10", "Y9"], cikti, veri, git=False); kontrol("4. tur: başka turla aynı koşuda olmaz", False)
    except YH.YHHata:
        kontrol("4. tur: başka turla aynı koşuda olmaz", True)
    # MEKANİK test (yalnız test): sentetik veride gerçek S7 şartlarıyla olay çıkmıyor (0); ölçüm yolunu sınamak için koşu Y'si gevşek şartlı
    # bir kopya (Y10 = Ş1, Y10c = Ş2; Y10b = Ş1 + F14). Kapı ve mühür zinciri GLOBAL YH_ESIK ile denetlenir (gerçek eşikler değişmez).
    Yg = copy.deepcopy(YH.YH_ESIK); Yg["denemeler"]["Y10"]["sartlar"] = ["S1"]; Yg["denemeler"]["Y10c"]["sartlar"] = ["S2"]
    R4 = YH.yh_kos(["Y10", "Y10b", "Y10c"], cikti, veri, islem=2, git=False, Y=Yg)
    J5 = json.load(open(os.path.join(cikti, "sonuc.json"), encoding="utf-8"))
    kontrol("4. tur: Y10 / Y10b / Y10c eklendi, Y10c bilgi", set(J5["deneme"]) == set(YH.YH_DENEMELER + YH.YH_DENEMELER_2 + YH.YH_DENEMELER_3 + YH.YH_DENEMELER_4) and J5["deneme"]["Y10c"].get("bilgi") is True)
    kontrol("4. tur: önceki turların sonuçları, sayımı, BH'si, hunisi AYNEN", all(J5["deneme"][k] == J_once4["deneme"][k] for k in YH.YH_DENEMELER + YH.YH_DENEMELER_2 + YH.YH_DENEMELER_3)
            and all(J5[a] == J_once4[a] for a in ("bh", "bh_tur2", "bh_tur3", "huni", "huni3")) and "bh_tur4" in J5
            and all(J5["sayim"][k] == J_once4["sayim"][k] for k in YH.YH_DENEMELER + YH.YH_DENEMELER_2 + YH.YH_DENEMELER_3))
    kontrol("4. tur: RAPOR.md / RAPOR_2.md / RAPOR_3.md değişmedi, RAPOR_4.md başlıkları", open(os.path.join(cikti, "RAPOR.md"), "rb").read() == rapor1
            and open(os.path.join(cikti, "RAPOR_2.md"), "rb").read() == rapor2 and open(os.path.join(cikti, "RAPOR_3.md"), "rb").read() == rapor3
            and all(x in R4["rapor"] for x in ("SONUÇ", "HUNİ", "HÜCRE TABLOSU", "KONUM EŞLİ KAT", "OLASILIK TABLOSU", "DIŞ SINAMA", "BIST (bilgi",
                                                "İKİ YÖNLÜ", "BAKILMIŞ", "CEMAL'İN GÖZÜYLE UYUM", "TUR 4 ÖRNEKLEMİ", "YENİDEN ÜRETİM", "KONTROL LİSTESİ", "## HATA")))
    kontrol("4. tur: etiket en fazla EMARE, ters ve kural etiketi var",
            all(not J5["deneme"][k]["etiket"].startswith("İZ") and "ters_etiket" in J5["deneme"][k] and "etiket_kural" in J5["deneme"][k] for k in YH.YH_DENEMELER_4))
    rg4 = {k: v for k, v in J5.get("regresyon_y1", {}).items() if k in YH.YH_DENEMELER_4}
    kontrol("4. tur: Y1 regresyonu (ölçülen satır = olay_Y1 satırı) her ölçülen deneme x pazarda", all(v["esit"] for d_ in rg4.values() for v in d_.values())
            and sum(v["n"] for d_ in rg4.values() for v in d_.values()) > 0, {k: {p: v["n"] for p, v in d_.items()} for k, d_ in rg4.items()})
    n10 = {k: sum(h.get("n_ham", 0) for h in J5["deneme"][k]["hucre"]) for k in YH.YH_DENEMELER_4}
    kontrol("4. tur (gevşek test şartı): Y10b <= Y10 = Y9 (Ş1 = Y9 şartı), Y10c > 0", n10["Y10b"] <= n10["Y10"] == n9["Y9"] and n10["Y10c"] > 0, n10)
    f10 = os.path.join(cikti, "olay_Y10c.csv.gz")
    if os.path.exists(f10):
        x10 = pd.read_csv(f10)
        kontrol("4. tur: Y10c satırları şartları sağlar (dosya değerleriyle), konum eş sütunları var", bool(YH.yh_y10_maske(x10, "Y10c", Yg).all())
                and {"k_es_h5", "q_olay", "F20", "F22a", "F23"} <= set(x10.columns), len(x10))
    try:
        YH.yh_kos(["Y10b"], cikti, veri, git=False); kontrol("4. tur: ikinci koşu durur", False)
    except YH.YHHata:
        kontrol("4. tur: ikinci koşu durur", True)
    open(yo4, "w", encoding="utf-8").write(m4.replace(f"ESIK_TUR3_SHA: `{t3}`", "ESIK_TUR3_SHA: `" + "3" * 64 + "`"))
    try:
        YH.yh_kapi4(cikti, git=False); kontrol("4. tur: Y1-Y9d mührü tutmazsa kapı durur", False)
    except YH.YHHata:
        kontrol("4. tur: Y1-Y9d mührü tutmazsa kapı durur", True)
    open(yo4, "w", encoding="utf-8").write(m4)
    s7p = YH.YH_YOL["ozellik_s7"]; s7b = open(s7p, "rb").read(); pd.read_csv(s7p).iloc[:-1].to_csv(s7p, index=False, compression="gzip")
    try:
        YH.yh_kapi4(cikti, git=False); kontrol("4. tur: S7 dosyası değişince kapı durur", False)
    except YH.YHHata:
        kontrol("4. tur: S7 dosyası değişince kapı durur", True)
    open(s7p, "wb").write(s7b)
    # ---- 5. tur uçtan uca (gerçekteki gibi ON_KAYIT_4.md 4. tur sha'sını taşır: yh_esik_sha_tur4; S9 dosyası = Y1 olay satırları)
    t4 = YH.yh_esik_sha_tur4()
    open(yo4, "w", encoding="utf-8").write(m4.replace(YH.yh_esik_sha(), t4))
    J_once5 = json.load(open(os.path.join(cikti, "sonuc.json"), encoding="utf-8"))
    rapor4 = open(os.path.join(cikti, "RAPOR_4.md"), "rb").read()
    YH.YH_YOL["ozellik_s9"] = os.path.join(tmp, "ozellik_Y1_s9.csv.gz")
    try:
        YH.yh_kos(["Y11"], cikti, veri, git=False); kontrol("5. tur: ön kayıt 5 yokken koşu durur", False)
    except YH.YHHata:
        kontrol("5. tur: ön kayıt 5 yokken koşu durur", True)
    try:
        YH.yh_onkayit5_yaz(cikti, veri, git=False); kontrol("5. tur: S9 dosyası / tasarım kaydı yokken ön kayıt yazılmaz", False)
    except YH.YHHata:
        kontrol("5. tur: S9 dosyası / tasarım kaydı yokken ön kayıt yazılmaz", True)
    Rs9 = YH.yh_s9_ozellik_yaz(veri, cikti, ozellik=yoz4)
    kontrol("5. tur: S9 dosyası = Y1 olay satırları, prefix denetimi tuttu", Rs9["satir"] == len(oz4) == len(O1t)
            and all(v["prefix_tuttu"] > 0 for v in Rs9["pazar"].values()), Rs9["pazar"])
    try:
        YH.yh_onkayit5_yaz(cikti, veri, git=False); kontrol("5. tur: tasarım kaydı yokken ön kayıt yazılmaz", False)
    except YH.YHHata as ex:
        kontrol("5. tur: tasarım kaydı yokken ön kayıt yazılmaz", "tasarım" in str(ex))
    # tasarım kaydı (sentetik veride No 38 / TUR 2 sayfaları yok): mekanik kapı için elle; TUTMAYAN kayıt ayar kararı olmadan ön kaydı durdurur
    yt5 = os.path.join(cikti, "tasarim5.json"); E11 = dict(YH.YH_ESIK["denemeler"]["Y11"]["esik"])
    kay = {"zaman": "test", "esik": E11, "satir": [], "a_no38_gecmedi": True, "b_tur2_gecen": 2, "tuttu": False, "ozellik_s9_sha": Rs9["sha"]}
    json.dump({"kayit": [kay]}, open(yt5, "w", encoding="utf-8"))
    try:
        YH.yh_onkayit5_yaz(cikti, veri, git=False); kontrol("5. tur: tasarım TUTMADI + ayar kararı yok -> ön kayıt yazılmaz", False)
    except YH.YHHata as ex:
        kontrol("5. tur: tasarım TUTMADI + ayar kararı yok -> ön kayıt yazılmaz", "ayar kararı" in str(ex))
    json.dump({"kayit": [kay, kay]}, open(yt5, "w", encoding="utf-8"))
    try:
        YH.yh_tasarim5(cikti, veri); kontrol("5. tur: tasarım üçüncü kez koşmaz (ilk + tek ayar)", False)
    except YH.YHHata as ex:
        kontrol("5. tur: tasarım üçüncü kez koşmaz (ilk + tek ayar)", "iki kez" in str(ex))
    json.dump({"kayit": [kay]}, open(yt5, "w", encoding="utf-8"))
    Yk = copy.deepcopy(YH.YH_ESIK); Yk["denemeler"]["Y11"]["esik"]["F27_min"] = 0.8
    try:
        YH.yh_tasarim5(cikti, veri, E=Yk); kontrol("5. tur: ayar F26_min / F25_alt dışında yapılamaz", False)
    except YH.YHHata as ex:
        kontrol("5. tur: ayar F26_min / F25_alt dışında yapılamaz", "yalnız F26_min" in str(ex))
    YH.yh_tasarim5_karar("test: izinli ayar sonucu değiştiremiyor", cikti)
    yo5 = YH.yh_onkayit5_yaz(cikti, veri, islem=1, git=False)
    m5 = open(yo5, encoding="utf-8").read()
    kontrol("5. tur: ON_KAYIT_5 yazıldı (Ş9 tanımı aynen, ESIK_TUR4_SHA, S9 / TASARIM5 sha, huni, SAPMA-1, kapı)",
            f"ESIK_TUR4_SHA: `{t4}`" in m5 and YH._yh_is_tanimi5_s2() in m5 and "S9_OZELLIK_SHA" in m5 and "TASARIM5_SHA" in m5 and "Y11 hunisi" in m5
            and "= Y11b" in m5 and "SAPMA-1" in m5 and "AYAR KULLANILMADI" in m5 and YH.yh_kapi5(cikti, git=False)["kontrol"])
    try:
        YH.yh_tasarim5(cikti, veri); kontrol("5. tur: ön kayıttan sonra tasarım koşmaz", False)
    except YH.YHHata as ex:
        kontrol("5. tur: ön kayıttan sonra tasarım koşmaz", "ON_KAYIT_5" in str(ex))
    try:
        YH.yh_kos(["Y11", "Y10"], cikti, veri, git=False); kontrol("5. tur: başka turla aynı koşuda olmaz", False)
    except YH.YHHata:
        kontrol("5. tur: başka turla aynı koşuda olmaz", True)
    # MEKANİK test: gevşek şartlı kopya (Y11 = Ş1, Y11b = Ş1 + Ş2, Y11c = Ş2); kapı / mühür GLOBAL YH_ESIK ile
    Yg5 = copy.deepcopy(YH.YH_ESIK); Yg5["denemeler"]["Y11"]["sartlar"] = ["S1"]; Yg5["denemeler"]["Y11b"]["sartlar"] = ["S1", "S2"]
    Yg5["denemeler"]["Y11c"]["sartlar"] = ["S2"]
    R5 = YH.yh_kos(["Y11", "Y11b", "Y11c"], cikti, veri, islem=2, git=False, Y=Yg5)
    J6 = json.load(open(os.path.join(cikti, "sonuc.json"), encoding="utf-8"))
    kontrol("5. tur: Y11 / Y11b / Y11c eklendi, Y11c bilgi", set(J6["deneme"]) == set(YH.YH_DENEMELER_HEPSI) and J6["deneme"]["Y11c"].get("bilgi") is True)
    kontrol("5. tur: önceki turların sonuçları, sayımı, BH'si, hunisi AYNEN", all(J6["deneme"][k] == J_once5["deneme"][k] for k in YH.YH_DENEMELER + YH.YH_DENEMELER_2 + YH.YH_DENEMELER_3 + YH.YH_DENEMELER_4)
            and all(J6[a] == J_once5[a] for a in ("bh", "bh_tur2", "bh_tur3", "bh_tur4", "huni", "huni3", "huni4")) and "bh_tur5" in J6
            and all(J6["sayim"][k] == J_once5["sayim"][k] for k in YH.YH_DENEMELER + YH.YH_DENEMELER_2 + YH.YH_DENEMELER_3 + YH.YH_DENEMELER_4))
    kontrol("5. tur: RAPOR .. RAPOR_4 değişmedi, RAPOR_5.md başlıkları", open(os.path.join(cikti, "RAPOR.md"), "rb").read() == rapor1
            and open(os.path.join(cikti, "RAPOR_2.md"), "rb").read() == rapor2 and open(os.path.join(cikti, "RAPOR_3.md"), "rb").read() == rapor3
            and open(os.path.join(cikti, "RAPOR_4.md"), "rb").read() == rapor4
            and all(x in R5["rapor"] for x in ("SONUÇ", "TASARIM KONTROLÜ", "HUNİ", "HÜCRE TABLOSU", "KONUM EŞLİ KAT", "OLASILIK TABLOSU", "DIŞ SINAMA",
                                                "kısmen bakılmış (Y9 alt kümesi)", "İKİ YÖNLÜ", "CEMAL'İN GÖZÜYLE UYUM", "TUR 4 KURU SAYIM", "İLERLEME",
                                                "YENİDEN ÜRETİM", "KONTROL LİSTESİ", "## HATA")))
    kontrol("5. tur: BH yalnız n >= 30 hücreler (n < 30 'BH dışı')", all(("p" in b) == (b.get("n", 30) >= 30) for b in J6["bh_tur5"])
            and all(not (b.get("not")) or b["n"] < 30 for b in J6["bh_tur5"]), J6["bh_tur5"])
    kontrol("5. tur: İLERLEME satır dosyalarından = sonuc.json hücreleri", J6["ilerleme5"]["uyum"] and {"Y1", "Y9", "Y10", "Y11"} <= set(J6["ilerleme5"]["deneme"]),
            J6["ilerleme5"].get("uyumsuz"))
    rg5 = {k: v for k, v in J6.get("regresyon_y1", {}).items() if k in YH.YH_DENEMELER_5}
    kontrol("5. tur: Y1 regresyonu her ölçülen deneme x pazarda", all(v["esit"] for d_ in rg5.values() for v in d_.values())
            and sum(v["n"] for d_ in rg5.values() for v in d_.values()) > 0)
    n11 = {k: sum(h.get("n_ham", 0) for h in J6["deneme"][k]["hucre"]) for k in YH.YH_DENEMELER_5}
    kontrol("5. tur (gevşek test şartı): Y11 = Y9 (Ş1), Y11b <= Y11, Y11c > 0", n11["Y11"] == n9["Y9"] and n11["Y11b"] <= n11["Y11"] and n11["Y11c"] > 0, n11)
    f11 = os.path.join(cikti, "olay_Y11.csv.gz")
    if os.path.exists(f11):
        x11 = pd.read_csv(f11)
        kontrol("5. tur: satır dosyasında F24-F29 ve konum eş sütunları", {"F24", "F25", "F26", "F27", "F28", "F29", "k_es_h5", "q_olay"} <= set(x11.columns), len(x11))
    try:
        YH.yh_kos(["Y11b"], cikti, veri, git=False); kontrol("5. tur: ikinci koşu durur", False)
    except YH.YHHata:
        kontrol("5. tur: ikinci koşu durur", True)
    open(yo5, "w", encoding="utf-8").write(m5.replace(f"ESIK_TUR4_SHA: `{t4}`", "ESIK_TUR4_SHA: `" + "4" * 64 + "`"))
    try:
        YH.yh_kapi5(cikti, git=False); kontrol("5. tur: Y1-Y10c mührü tutmazsa kapı durur", False)
    except YH.YHHata:
        kontrol("5. tur: Y1-Y10c mührü tutmazsa kapı durur", True)
    open(yo5, "w", encoding="utf-8").write(m5)
    s9p = YH.YH_YOL["ozellik_s9"]; s9b = open(s9p, "rb").read(); pd.read_csv(s9p).iloc[:-1].to_csv(s9p, index=False, compression="gzip")
    try:
        YH.yh_kapi5(cikti, git=False); kontrol("5. tur: S9 dosyası değişince kapı durur", False)
    except YH.YHHata:
        kontrol("5. tur: S9 dosyası değişince kapı durur", True)
    open(s9p, "wb").write(s9b)
    # ---- 6. tur uçtan uca (gruplar + karne + mahkeme; ON_KAYIT_5 YH_ESIK_SHA = yh_esik_sha(): Y1-Y11c aynen)
    try:
        YH.yh_kos6(cikti, veri, git=False); kontrol("6. tur: ön kayıt 6 yokken koşu durur", False)
    except YH.YHHata:
        kontrol("6. tur: ön kayıt 6 yokken koşu durur", True)
    yo6 = YH.yh_onkayit6_yaz(cikti, git=False)
    m6 = open(yo6, encoding="utf-8").read()
    g3t = pd.read_csv(os.path.join(cikti, "grup6_G3.csv"))
    kontrol("6. tur: ON_KAYIT_6 yazıldı (§A/§B/§C aynen, YH_ESIK6 / G3 sha, grup sayıları, karne hunisi, kapı)",
            YH._yh_is_tanimi6_bolum("A") in m6 and YH._yh_is_tanimi6_bolum("C") in m6 and f"YH_ESIK6_SHA: `{YH.yh_esik6_sha()}`" in m6
            and "G3_SHA" in m6 and "GRUP OLAY SAYILARI" in m6 and "KARNE HUNİSİ" in m6 and YH.yh_kapi6(cikti, git=False)["kontrol"], len(g3t))
    R6 = YH.yh_kos6(cikti, veri, islem=2, git=False)
    kontrol("6. tur: tutarlılık kapısı G2 = olay_Y9, F15 >= 0,75 = olay_Y9c", all(v["esit"] for v in R6["tutarlilik"].values()), R6["tutarlilik"])
    kontrol("6. tur: Y1 regresyonu plasebo dahil her pazarda", all(v["esit"] and v.get("plasebo_esit") for v in R6["regresyon_y1"].values()))
    ng = {g: sum(h.get("n_ham", 0) for h in R6["grup"][g]["hucre"]) for g in YH._YH_GRUP6}
    kontrol("6. tur: G0 = Y1 olayı; G2 = Y9; G2u <= G2; G3 = G2 (olay satırı)", ng["G0"] == len(O1t) and ng["G2"] == n9["Y9"] and ng["G2u"] <= ng["G2"]
            and ng["G3"] == ng["G2"] == len(g3t), ng)
    x6 = pd.read_csv(os.path.join(cikti, "olay_G6.csv.gz"))
    hh = [h for h in R6["grup"]["G0"]["hucre"] if h.get("n", 0) > 0][0]
    xx = x6[x6.G0 & (x6.pazar == hh["pazar"]) & (x6.donem == hh["donem"]) & x6.h5.notna() & x6.es_h5.notna()]
    kontrol("6. tur: yeniden üretim (satır dosyası) KAT5 = grup6.json", len(xx) == hh["n"] and abs(xx.h5.sum() / xx.es_h5.sum() - hh["h5_kat"]) < 1e-4,
            (len(xx), hh["h5_kat"]))
    kontrol("6. tur: grup farkı aralığı noktayı içerir", all((not np.isfinite(v["fark"])) or (v["alt"] <= v["fark"] + 1e-9 and v["fark"] <= v["ust"] + 1e-9)
                                                        for v in R6["fark"].values()))
    try:
        YH.yh_kos6(cikti, veri, git=False); kontrol("6. tur: ikinci koşu durur", False)
    except YH.YHHata:
        kontrol("6. tur: ikinci koşu durur", True)
    try:
        YH.yh_onkayit6_yaz(cikti, uzerine=True, git=False); kontrol("6. tur: ölçümden sonra ön kayıt yazılmaz", False)
    except YH.YHHata:
        kontrol("6. tur: ölçümden sonra ön kayıt yazılmaz", True)
    Kr = YH.yh_filtre_karne(cikti)
    kontrol("6. tur: filtre karnesi (2 kol x 10 adım x 4 pazar, tek-çıkarma 18 x 4, SORGULANACAK satırı)",
            len(Kr["tablo"]) == (10 + 10) * 4 and len(Kr["tek_cikarma"]) == 18 * 4
            and "SORGULANACAK FİLTRELER" in open(os.path.join(cikti, "FILTRE_KARNE.md"), encoding="utf-8").read())
    r_ = [r for r in Kr["tablo"] if r["pazar"] == "ABD" and r["kol"] == "S7" and r["adim"] == 1][0]
    xk = O1t.merge(YH.yh_ozellik5_oku(), on=["pazar", "sembol", "tarih"])
    xk = xk[(xk.pazar == "ABD") & (xk.donem == "2016-22") & (xk.F15 <= 0.25) & (xk.F17 <= -0.20) & xk.h5.notna() & xk.es_h5.notna()]
    kontrol("6. tur: karne Ş1 adımı ABD eğitim n / FARK elle = kod", r_["egitim"]["n"] == len(xk)
            and (len(xk) == 0 or abs(r_["egitim"]["fark"] - (xk.h5.mean() - xk.es_h5.mean())) < 1e-9), (r_["egitim"]["n"], len(xk)))
    Lm = O1t[["pazar", "sembol", "tarih"]].drop_duplicates().sort_values(["pazar", "sembol", "tarih"]).iloc[::max(1, len(O1t) // 12)].head(12).copy()
    Lm.insert(0, "no", np.arange(1, len(Lm) + 1))
    Rm = YH.yh_mahkeme_toplu(Lm, os.path.join(cikti, "M.md"), "test mahkeme", os.path.join(cikti, "M.json"), veri)
    mt = open(os.path.join(cikti, "M.md"), encoding="utf-8").read()
    kontrol("6. tur: toplu mahkeme (prefix kapısı geçti, seçilen = özellik dosyası, sembol / tarih sızıntısı yok)",
            Rm["ozet"]["mahkeme"] == len(Lm) and Rm["ozet"]["regresyon_esit"] == len(Lm) and not any(str(s_) in mt for s_ in Lm.sembol)
            and not any(pd.Timestamp(t_).strftime("%Y-%m-%d") in mt for t_ in Lm.tarih), Rm["ozet"])
    try:
        YH.yh_mahkeme_toplu(Lm, os.path.join(cikti, "M2.md"), "test", None, veri, ek_not=str(Lm.sembol.iloc[0]))
        kontrol("6. tur: toplu md'de sembol sızıntısı -> yazılmaz", False)
    except YH.YHHata as ex:
        kontrol("6. tur: toplu md'de sembol sızıntısı -> yazılmaz", "sızıntı" in str(ex) and not os.path.exists(os.path.join(cikti, "M2.md")))
    Jm = json.load(open(os.path.join(cikti, "M.json"), encoding="utf-8"))
    kontrol("6. tur: mahkeme kararı puan kuralıyla tutarlı", all(o["onceki_daha_uygun"] == (bool(o["adaylar"]) and max(a["puan"] for a in o["adaylar"]) > o["secilen"]["puan"])
                                                               for o in Jm["olay"]))
    R6r = YH.yh_rapor6(cikti)
    kontrol("6. tur: RAPOR_6.md başlıkları", all(x in R6r for x in ("A. GRUPLAR", "OLASILIK TABLOSU", "GRUP FARKLARI", "B. FİLTRE KARNESİ",
                                                                    "SORGULANACAK FİLTRELER", "C. MAHKEME", "YENİDEN ÜRETİM", "KONTROL LİSTESİ", "## HATA")))
    kontrol("6. tur: önceki turların sonuc.json'u değişmedi", json.load(open(os.path.join(cikti, "sonuc.json"), encoding="utf-8")) == J6)
    open(yo6, "w", encoding="utf-8").write(m6.replace(YH.yh_esik6_sha(), "6" * 64))
    try:
        YH.yh_kapi6(cikti, git=False); kontrol("6. tur: YH_ESIK6 mührü tutmazsa kapı durur", False)
    except YH.YHHata:
        kontrol("6. tur: YH_ESIK6 mührü tutmazsa kapı durur", True)
    open(yo6, "w", encoding="utf-8").write(m6)
    open(yo4, "w", encoding="utf-8").write(m4)
    YH.YH_YOL["ozellik"] = yoz; open(yo3, "w", encoding="utf-8").write(m3)
    ozt.iloc[:-1].to_csv(yoz, index=False, float_format="%.6g", compression="gzip")
    try:
        YH.yh_kapi3(cikti, git=False); kontrol("3. tur: özellik dosyası değişince kapı durur", False)
    except YH.YHHata:
        kontrol("3. tur: özellik dosyası değişince kapı durur", True)
finally:
    YH.YH_YOL.clear(); YH.YH_YOL.update(yol_eski)
    shutil.rmtree(tmp, ignore_errors=True)

print("10) e-posta / anahtar, çakışma kapısı")
temiz = True
for ad in ("YAPI_HEDEF.py", "test_yapi_hedef.py"):
    m = open(os.path.join(KOK, ad), encoding="utf-8").read()
    if YH._YH_EPOSTA.search(m) or YH._YH_ANAHTAR.search(m):
        temiz = False
for ad in ("onkayit", "onkayit2", "onkayit3", "onkayit4", "onkayit5", "sonuc", "rapor", "rapor2", "rapor3", "rapor4", "rapor5", "tasarim5", "guc_json", "guc_md"):
    y = YH._yh_yol(ad)
    if os.path.exists(y):
        m = open(y, encoding="utf-8").read()
        if YH._YH_EPOSTA.search(m) or YH._YH_ANAHTAR.search(m):
            temiz = False
kontrol("kod ve çıktılarda e-posta / anahtar yok", temiz)
ns = {"__name__": "yh_cakisma", "__file__": os.path.join(KOK, "YAPI_HEDEF.py"), "yh_sim": "baska dosyanin adi"}
try:
    exec(compile(open(os.path.join(KOK, "YAPI_HEDEF.py"), encoding="utf-8").read(), "YAPI_HEDEF.py", "exec"), ns)
    kontrol("çakışma kapısı: bellekteki adı ezince durur", False)
except RuntimeError as ex:
    kontrol("çakışma kapısı: bellekteki adı ezince durur", "yh_sim" in str(ex))
ns2 = {"__name__": "yh_cakisma2", "__file__": os.path.join(KOK, "YAPI_HEDEF.py")}
exec(compile(open(os.path.join(KOK, "YAPI_HEDEF.py"), encoding="utf-8").read(), "YAPI_HEDEF.py", "exec"), ns2)
try:
    exec(compile(open(os.path.join(KOK, "YAPI_HEDEF.py"), encoding="utf-8").read(), "YAPI_HEDEF.py", "exec"), ns2)
    kontrol("çakışma kapısı: aynı dosya yeniden yüklenince durmaz", True)
except RuntimeError:
    kontrol("çakışma kapısı: aynı dosya yeniden yüklenince durmaz", False)

print("11) 2. tur şartları")
n_, ok_ = YH.yh_dokunus(np.array([10.0, 10.1, 12.0, 10.05, 11.0]), 10.0, 0.015, 0.99)
kontrol("dokunuş: Low <= hat x 1,015 sayımı (3), eğim tuttu", n_ == 3 and ok_)
n_, ok_ = YH.yh_dokunus(np.array([10.14, 10.1, 10.0]), 10.0, 0.015, 0.99)
kontrol("dokunuş: alçalan dokunuş (son < ilk x 0,99) -> eğim tutmaz", n_ == 3 and not ok_)
kontrol("dokunuş: 2 dokunuş", YH.yh_dokunus(np.array([10.0, 11, 12, 10.1]), 10.0, 0.015, 0.99)[0] == 2)
yuk = np.repeat(np.linspace(80, 100, 10), 25); dus = np.repeat(np.linspace(100, 80, 10), 25)
kontrol("büyük desen: yükselen dipler eğim > 0, alçalan -%20", YH.yh_buyuk_egim(yuk, 25) > 0.2 and abs(YH.yh_buyuk_egim(dus, 25) + 0.2) < 1e-9)
kontrol("büyük desen: eksik / bölünmeyen uzunluk -> -inf", YH.yh_buyuk_egim(yuk[:-1], 25) == -np.inf)
kontrol("büyük desen: eşik -0,05 sınırı", YH.yh_buyuk_egim(np.repeat(np.linspace(100, 95, 10), 25), 25) >= -0.05 - 1e-12
        and YH.yh_buyuk_egim(np.repeat(np.linspace(100, 94.9, 10), 25), 25) < -0.05)
U = np.r_[np.full(10, 70.0), np.full(10, 60.0), np.full(10, 66.0)]
kontrol("iki kenar: U (70 / 60 / 66) tutar", YH.yh_iki_kenar(U, 1.05)[0])
kontrol("iki kenar: sağ kenar dipte (62) tutmaz", not YH.yh_iki_kenar(np.r_[np.full(10, 70.0), np.full(10, 60.0), np.full(10, 62.0)], 1.05)[0])
kontrol("iki kenar: orta = W[n//3 : 2n//3]", YH.yh_iki_kenar(np.r_[np.full(10, 70.0), np.full(10, 60.0), np.full(11, 66.0)], 1.05)[2] == 60.0)

# Y6 bayrakları elle (rastgele seriler; Y1 sinyallerinin hepsi)
okb = True; n6 = 0; nf = {c: 0 for c in ("f_hat", "f_kir", "f_stop", "f_buyuk")}; nk = 0
for toh in (11, 21, 31, 41, 51, 61, 71, 81):
    dx = rastgele_hisse(1200, toh, oyn=0.012)
    F = YH.yh_y6_bayrak(dx); X1_, _ = YH.yh_s6_hisse(dx)
    okb &= len(F) == len(X1_) and (pd.to_datetime(F.tarih).values == pd.to_datetime(X1_.tarih).values).all()
    dd_ = SY.sy_veri_hazirla(dx, SY.SY_ESIK); T_ = S6.s6_taban(dd_); Lx, Hx, Cx = dd_.Low.to_numpy(), dd_.High.to_numpy(), dd_.Close.to_numpy()
    du_ = T_.durum.to_numpy(object)
    for rr in F.itertuples():
        i = dd_.index.get_loc(pd.Timestamp(rr.tarih)); n6 += 1
        sol = int(T_.kutu_sol_i.iloc[i]) if du_[i] == "AL" else int(T_.bas_i.iloc[i - 1])
        Lz = Lx[sol:i]; tch = np.flatnonzero(Lz <= rr.hat * 1.015)
        a_ = len(tch) >= 3 and Lz[tch[-1]] >= Lz[tch[0]] * 0.99
        b_ = Cx[i] > rr.tavan * 1.01 and (Hx[i] - Lx[i]) >= np.median(Hx[sol:i] - Lx[sol:i])
        c_ = Cx[i] / rr.hat - 1 <= 0.10
        if i >= 250:
            mm = Lx[i - 250:i].reshape(10, 25).min(1); bb, aa = np.polyfit(np.arange(10.0), mm, 1); d_ = (aa + 9 * bb) / aa - 1 >= -0.05
        else:
            d_ = True
        k_ = sum(1 for a in range(i - 250, i) if a >= 0 and du_[a] == "KIRILDI")
        okb &= (bool(a_), bool(b_), bool(c_), bool(d_), k_) == (bool(rr.f_hat), bool(rr.f_kir), bool(rr.f_stop), bool(rr.f_buyuk), int(rr.kir250))
        for c, v in (("f_hat", a_), ("f_kir", b_), ("f_stop", c_), ("f_buyuk", d_)):
            nf[c] += int(bool(v))
        nk += int(k_ > 0)
    Y6_ = YH.yh_hisse_sinyal(dx, "Y6"); Y8_ = YH.yh_hisse_sinyal(dx, "Y8"); Y8B_ = YH.yh_hisse_sinyal(dx, "Y8B")
    okb &= len(Y8_) + len(Y8B_) == len(Y6_) and set(pd.to_datetime(Y6_.tarih)) <= set(pd.to_datetime(X1_.tarih))
kontrol("Y6 bayrakları elle = kod (bölge, dokunuş, kırılım payı + mum, stop, büyük desen, kir250); Y8 + Y8B = Y6", okb and n6 > 20, (n6, nf, nk))
kontrol("Y6 şartları sentetikte iki yönlü (her bayrak hem tutuyor hem tutmuyor)", all(0 < v < n6 for v in nf.values()), nf)

# Y7 bayrakları elle (kazan serisi + rastgele)
okk = True; n7 = 0
for dx in [d3] + [rastgele_hisse(900, t, oyn=0.02) for t in (41, 51)]:
    F = YH.yh_y7_bayrak(dx); X3_ = YH.yh_y3_hisse(dx)
    okk &= len(F) == len(X3_)
    dd_ = SY.sy_veri_hazirla(dx, SY.SY_ESIK); Lx, Hx, Cx = dd_.Low.to_numpy(), dd_.High.to_numpy(), dd_.Close.to_numpy()
    Cp = np.r_[np.nan, Cx[:-1]]; trp = (np.fmax(Hx, Cp) - np.fmin(Lx, Cp)) / Cp
    for rr in F.itertuples():
        i = dd_.index.get_loc(pd.Timestamp(rr.tarih)); n = int(rr.n); W = slice(i - n, i); n7 += 1
        Lw = Lx[W]; a3, b3 = n // 3, 2 * n // 3
        ke = Lw[:a3].min() >= Lw[a3:b3].min() * 1.05 and Lw[b3:].min() >= Lw[a3:b3].min() * 1.05
        cnt = min(250, i - n - 1); atr = trp[i - n - cnt:i - n].mean() if cnt >= 120 else np.nan
        mu = np.isfinite(atr) and np.median(((Hx - Lx) / Cx)[i - n + a3:i - n + b3]) <= 0.9 * atr
        dk = (Lw <= rr.hat * 1.015).sum() >= 3
        st = Cx[i] / rr.hat - 1 <= 0.10
        okk &= (bool(ke), bool(mu), bool(dk), bool(st)) == (bool(rr.f_kenar), bool(rr.f_mum), bool(rr.f_dok), bool(rr.f_stop))
kontrol("Y7 bayrakları elle = kod (iki kenar, orta üçte bir mum / ATR, dip savunması, stop)", okk and n7 > 0, n7)
F3o = YH.yh_y7_bayrak(d3)
if len(F3o):
    n3_ = int(F3o.n.iloc[-1]); Lw3 = d3.Low.to_numpy()[-1 - n3_:-1]; k3 = YH.yh_iki_kenar(Lw3, 1.05)
kontrol("Y7: kazan serisinde (sağ kenar orta dibin yalnız %0,9 üstü) iki kenar TUTMAZ, ek sütunu yardımcıyla aynı",
        len(F3o) and not bool(F3o.f_kenar.iloc[-1]) and f"kenar={k3[1] / k3[2] - 1:.3f}/{k3[3] / k3[2] - 1:.3f}" in F3o.ek.iloc[-1], F3o.tail(1).ek.tolist() if len(F3o) else "yok")

# Y8 hafızası: elle kurulmuş KIRILDI
okh8 = True
for toh in (11, 21, 31):
    dx = rastgele_hisse(900, toh, oyn=0.012); F = YH.yh_y6_bayrak(dx)
    Y6_ = YH.yh_tur2_sec(F, "Y6"); Y8_ = YH.yh_tur2_sec(F, "Y8"); Y8B_ = YH.yh_tur2_sec(F, "Y8B")
    okh8 &= (Y8_.kir250 == 0).all() and (Y8B_.kir250 > 0).all() and len(Y8_) + len(Y8B_) == len(Y6_)
kontrol("Y8 = Y6 ve kir250 = 0; Y8B = Y6 ve kir250 > 0", okh8)

# geleceğe bakma: bayraklı çerçeve (bütün Y1 / Y3 sinyalleri + bayraklar) kesik seri = tam seri
for ad, f, kol in (("Y6 bayrak", YH.yh_y6_bayrak, ["f_hat", "f_kir", "f_stop", "f_buyuk", "kir250", "dokunus"]),
                   ("Y7 bayrak", YH.yh_y7_bayrak, ["f_kenar", "f_mum", "f_dok", "f_stop", "dokunus"])):
    tamam = True; say_ = 0
    for toh in (3, 5, 8):
        dx = rastgele_hisse(700, toh, oyn=0.015)
        Full = f(dx); Full["tarih"] = pd.to_datetime(Full.tarih)
        kes = sorted(set(list(Full.tarih[::2])[:10]) | set(dx.index[[300, 555, 699]]))
        for t in kes:
            Z_ = f(dx[dx.index <= t]); Z_["tarih"] = pd.to_datetime(Z_.tarih)
            A = Full[Full.tarih <= t].reset_index(drop=True); B = Z_.reset_index(drop=True)
            if len(A) != len(B) or not ((A.tarih == B.tarih).all() and all((A[c].astype(float).to_numpy() == B[c].astype(float).to_numpy()).all() for c in kol)
                                         and np.allclose(A.stop0.to_numpy(float), B.stop0.to_numpy(float), rtol=0, atol=1e-9)):
                tamam = False
            say_ += 1
    kontrol(f"{ad}: {say_} kesimde kesik = tam (tarih, stop0, bayraklar)", tamam)
for ad in ("Y6", "Y7", "Y8", "Y8B"):
    tamam = True
    for toh in (3, 5):
        dx = rastgele_hisse(700, toh, oyn=0.015); Full = YH.yh_hisse_sinyal(dx, ad); Full["tarih"] = pd.to_datetime(Full.tarih)
        for t in sorted(set(Full.tarih) | set(dx.index[[400, 699]])):
            Z_ = YH.yh_hisse_sinyal(dx[dx.index <= t], ad)
            tamam &= len(Z_) == int((Full.tarih <= t).sum())
    kontrol(f"{ad}: yh_hisse_sinyal kesik = tam", tamam)

# 1. tur mührü
y1 = YH._yh_yol("onkayit")
if os.path.exists(y1):
    import re as _re
    m_ = _re.search(r"YH_ESIK_SHA:\s*`([0-9a-f]{64})`", open(y1, encoding="utf-8").read())
    gj = json.load(open(YH._yh_yol("guc_json"), encoding="utf-8"))
    kontrol("ESIK_TUR1_SHA = ON_KAYIT.md YH_ESIK_SHA = güç tablosu (Y1-Y5 eşikleri aynen)", m_ and m_.group(1) == YH.yh_esik_sha_tur1() == gj["yh_esik_sha"])
kontrol("2. tur denemeleri YH_ESIK'te, Y1-Y5 dizini aynı", all(k in YH.YH_ESIK["denemeler"] for k in YH.YH_DENEMELER_2)
        and [YH.YH_DENEMELER_HEPSI.index(k) for k in YH.YH_DENEMELER] == [0, 1, 2, 3, 4])

# E5a stop_uzak ve E5b bilgi (bölüm 6'nın sentetik paneli)
sig3 = sig.copy(); sig3["hat"] = [Vs["S03"].Open.iloc[201] / 1.2, Vs["S07"].Open.iloc[251] / 1.05]; sig3["stop0"] = sig3.hat * 0.98
Z6, say6 = YH.yh_olc_pazar(Vd, P, Cl, sig3, "Y6", "ABD")
kontrol("E5a: giriş / hat - 1 > %10 olay ölçülmez, stop_uzak sayımında", say6.get("stop_uzak") == 1 and len(Z6) == 1 and Z6.sembol.iloc[0] == "S07", say6)
Zb = YH.yh_e5b_olc(P, Cl, Z6)
r6 = Zb.iloc[0]; d6, j6 = int(r6.d), int(r6.j); st_b = max(r6.hat * 0.98, r6.E0 * 0.95)
Sb = YH.yh_sim(YH._yh_pencere(Cl, d6, 30, np.array([j6])), YH._yh_pencere(P["Hi"], d6, 30, np.array([j6])), YH._yh_pencere(P["Lo"], d6, 30, np.array([j6])),
               np.array([r6.E0]), np.array([st_b]), 1)
esb = [k for k in range(len(P["sembol"])) if k != j6 and P["ok"][d6, k] and P["H"][d6, k] == P["H"][d6, j6]]
vb = []
for k in esb:
    S_ = YH.yh_sim(YH._yh_pencere(Cl, d6, 30, np.array([k])), YH._yh_pencere(P["Hi"], d6, 30, np.array([k])), YH._yh_pencere(P["Lo"], d6, 30, np.array([k])),
                   np.array([P["Op"][d6, k]]), np.array([P["Op"][d6, k] * (1 - r6.b_dd)]), 1)
    if S_["olc"][0]:
        vb.append(S_["st5"][0])
kontrol("E5b: stop0b = max(hat x 0,98, giriş x 0,95); olay ve eş elle = kod", abs(r6.b_dd - (1 - st_b / r6.E0)) < 1e-12 and Sb["h5"][0] == r6.b_h5
        and len(vb) == int(r6.b_n_es) and (abs(np.mean(vb) - r6.b_es_st5) < 1e-12 if len(vb) >= 3 else np.isnan(r6.b_es_st5)), (r6.b_dd, len(vb)))
kontrol("E5b: 1. tur ölçümü (yh_olay_olc) b_ sütunu üretmez", "b_h5" not in Z.columns)

print("12) 3. tur (Y9 / Y9b / Y9c / Y9d)")
import GOZ_ETIKET as GE  # noqa: E402
Pz = YH.YH_ESIK["denemeler"]["Y9"]["ozellik_prm"]; GP = GE.GE_ESIK["ozellik"]
kontrol("Y9 özellik parametreleri = GOZ_ETIKET (hat bandı, 120 konum, 60 düşüş)", Pz["hat_bant"] == GP["hat_bant"] and Pz["konum_gun"] == GP["konum_gun"]
        and Pz["dusus_gun"] == GP["dusus_gun"])
okf, nf9 = True, 0
for toh in (11, 21, 31, 41, 51, 61):
    dx = rastgele_hisse(1500, toh, oyn=0.015); X1_, _ = YH.yh_s6_hisse(dx)
    Fy = YH.yh_y9_ozellik(dx, list(X1_.tarih))
    dg = GE.ge_hazir(dx); Tg = GE.ge_s6(dg); A_ = [dg[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume")]
    for q, t in enumerate(pd.to_datetime(X1_.tarih)):
        Fg = GE.ge_ozellik_bar(*A_, Tg, int(dg.index.get_loc(t)))
        okf &= bool(np.allclose(Fy.iloc[q][YH._Y9_OZ].to_numpy(float), np.array([Fg[c] for c in YH._Y9_OZ], float), rtol=0, atol=1e-12, equal_nan=True))
        nf9 += 1
kontrol("F1 / F11 / F15 / F17 = GOZ_ETIKET.ge_ozellik_bar (bütün Y1 günleri)", okf and nf9 > 20, nf9)
Fm = pd.DataFrame({"F15": [0.25, 0.2500001, 0.1, 0.1, 0.1, np.nan, 0.75, 0.7499, 0.5, 0.25, 0.75],
                   "F17": [-0.20, -0.5, -0.1999, np.nan, -0.3, -0.5, 0.0, 0.0, 0.0, -0.3, 0.0],
                   "F1": [3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3], "F11": [0.01, 0.01, 0.01, 0.01, 0.02, 0.01, 0, 0, 0, 0.009, 0]})
kontrol("Y9: F15 <= 0,25 VE F17 <= -0,20 (kapalı sınır, NaN tutmaz)", list(YH.yh_y9_maske(Fm, "Y9")) == [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0])
kontrol("Y9b: Y9 + F1 >= 3 + F11 >= 0,01", list(YH.yh_y9_maske(Fm, "Y9b")) == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
kontrol("Y9c: F15 >= 0,75; Y9d: 0,25 < F15 < 0,75", list(YH.yh_y9_maske(Fm, "Y9c")) == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        and list(YH.yh_y9_maske(Fm, "Y9d")) == [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0])
kontrol("Y9 / Y9c / Y9d ayrık", not (YH.yh_y9_maske(Fm, "Y9") & YH.yh_y9_maske(Fm, "Y9c")).any()
        and not (YH.yh_y9_maske(Fm, "Y9d") & (YH.yh_y9_maske(Fm, "Y9") | YH.yh_y9_maske(Fm, "Y9c"))).any())
kontrol("çeyrek sınırları (0,25 / 0,5 / 0,75 / NaN / 0,7499999999 gürültüsü)",
        list(YH.yh_ceyrek(np.array([0, 0.25, 0.2500001, 0.5, 0.50001, 0.7499, 0.75, 1.0, np.nan, 0.7499999999999]))) == [0, 0, 1, 1, 2, 2, 3, 3, -1, 3])
# özellik birleştirme (sembol + tarih; satır sırası karışık; başka pazar satırları; eksik satır durur)
Vs9 = {f"Q{i:02d}": rastgele_hisse(1100, 300 + i, oyn=0.015) for i in range(45)}
Vd9 = OC._oc_veri_sar(Vs9, "ABD"); P9 = OC.oc_panel(Vd9)
S1_ = YH.yh_sinyaller(Vd9, "ABD", ["Y1"])["Y1"]; S1_["tarih"] = pd.to_datetime(S1_.tarih)
Z1_, _ = OC.oc_olay_hazirla(S1_[["sembol", "tarih", "pazar"]], P9)
oz9 = []
for sb, g in Z1_.groupby("sembol"):
    F_ = YH.yh_y9_ozellik(Vs9[sb], list(g.tarih)); F_.insert(0, "tarih", pd.to_datetime(g.tarih).to_numpy()); F_.insert(0, "sembol", sb); oz9.append(F_)
oz9 = pd.concat(oz9, ignore_index=True); oz9.insert(0, "pazar", "ABD")
yabanci = oz9.head(5).assign(pazar="AVR", F15=9.9)
tmp9 = tempfile.mkdtemp(prefix="yh_oz_")
try:
    y9 = os.path.join(tmp9, "oz.csv.gz"); pd.concat([oz9, yabanci]).sample(frac=1.0, random_state=7).to_csv(y9, index=False, float_format="%.6g", compression="gzip")
    S9 = YH.yh_sinyaller3(Vd9, "ABD", YH.YH_DENEMELER_3, P=P9, ozellik=y9)
    M_ = S9["_Y9F"].merge(oz9, on=["sembol", "tarih"], suffixes=("", "_e"))
    kontrol("birleştirme: her Y1 olayı kendi (sembol, tarih) özelliğini aldı (karışık sıra, yabancı pazar satırı)", len(M_) == len(oz9) == len(S9["_Y9F"])
            and all(np.allclose(M_[c], M_[c + "_e"], rtol=1e-5, equal_nan=True) for c in YH._Y9_OZ) and S9["_Y9R"]["y1_olay"] == len(oz9), S9["_Y9R"])
    kontrol("birleştirme: hat / stop0 Y1 sinyalinden", np.allclose(S9["_Y9F"].stop0, S9["_Y9F"].hat * 0.98))
    kontrol("birleştirme: Y9 + Y9c + Y9d + NaN = Y1 olayı", len(S9["Y9"]) <= int((S9["_Y9F"].F15 <= 0.25).sum())
            and int((S9["_Y9F"].F15 <= 0.25).sum()) + len(S9["Y9c"]) + len(S9["Y9d"]) + int(S9["_Y9F"].F15.isna().sum()) == len(S9["_Y9F"]),
            {k: len(S9[k]) for k in YH.YH_DENEMELER_3})
    oz9.iloc[1:].to_csv(y9, index=False, float_format="%.6g", compression="gzip")
    try:
        YH.yh_sinyaller3(Vd9, "ABD", ["Y9"], P=P9, ozellik=y9); kontrol("birleştirme: özellik kümesi != Y1 olay kümesi -> durur", False)
    except YH.YHHata:
        kontrol("birleştirme: özellik kümesi != Y1 olay kümesi -> durur", True)
    try:
        YH.yh_sinyaller3(Vd9, "ABD", ["Y9"], P=P9, ozellik=os.path.join(tmp9, "yok.csv.gz")); kontrol("özellik dosyası yoksa durur", False)
    except YH.YHHata:
        kontrol("özellik dosyası yoksa durur", True)
finally:
    shutil.rmtree(tmp9, ignore_errors=True)
# F15 paneli elle
F15p = YH.yh_f15_panel(P9, Vd9); okp = True; nk = 0
rng9 = np.random.default_rng(5)
for _ in range(60):
    d_, j_ = int(rng9.integers(130, len(P9["tarih"]))), int(rng9.integers(len(P9["sembol"])))
    c_ = Vs9[P9["sembol"][j_]].Close; c_ = c_[c_.index < P9["tarih"][d_]].to_numpy()[-120:]
    bek = (c_[-1] - c_.min()) / (c_.max() - c_.min()) if len(c_) == 120 and c_.max() > c_.min() else np.nan
    okp &= bool(np.isclose(F15p[d_, j_], bek, rtol=0, atol=1e-12, equal_nan=True)); nk += 1
kontrol("F15 paneli = elle (giriş gününden önceki son geçerli bar, 120 kapanış)", okp and nk == 60)
Zo = Z1_.merge(oz9, on=["sembol", "tarih"])
kontrol("F15 paneli olayda dosya F15'ine eşit (aynı bilgi anı)", np.allclose(F15p[Zo.d.to_numpy(int), Zo.j.to_numpy(int)], Zo.F15, rtol=1e-5, atol=1e-7, equal_nan=True))
# konum eşli KAT elle = kod
Cl9 = YH.yh_kapanis(P9, Vd9)
X9 = S9["_Y9F"]
Zk, _ = YH.yh_olc_pazar(Vd9, P9, Cl9, X9, "Y9", "ABD")
Zk = Zk.merge(X9[["sembol", "tarih"] + YH._Y9_OZ], on=["sembol", "tarih"], how="left")
Zk = YH.yh_konum_es_olc(P9, Cl9, Zk, F15p)
okk, nkk = True, 0
for r9 in Zk[Zk.olc.astype(bool)].head(25).itertuples():
    d_, j_ = int(r9.d), int(r9.j); qo = int(YH.yh_ceyrek(np.array([r9.F15]))[0]); v_ = []; tum = []
    for k in range(len(P9["sembol"])):
        if k == j_ or not P9["ok"][d_, k] or P9["H"][d_, k] != P9["H"][d_, j_]:
            continue
        S_ = YH.yh_sim(YH._yh_pencere(Cl9, d_, 30, np.array([k])), YH._yh_pencere(P9["Hi"], d_, 30, np.array([k])), YH._yh_pencere(P9["Lo"], d_, 30, np.array([k])),
                       np.array([P9["Op"][d_, k]]), np.array([P9["Op"][d_, k] * (1 - r9.dd)]), 1)
        if S_["olc"][0]:
            tum.append(S_["h5"][0])
            if YH.yh_ceyrek(np.array([F15p[d_, k]]))[0] == qo and qo >= 0:
                v_.append(S_["h5"][0])
    okk &= len(v_) == int(r9.k_n_es) and len(tum) == int(r9.n_es) and (abs(np.mean(v_) - r9.k_es_h5) < 1e-12 if len(v_) >= 3 else np.isnan(r9.k_es_h5))
    nkk += 1
kontrol("konum eşli: eş = aynı gün, aynı kova, ölçülebilir VE F15 aynı çeyrek; k_es_h5 elle = kod; 1. tur eşi aynı", okk and nkk > 0, nkk)
Zk2 = YH.yh_konum_es_olc(P9, Cl9, Zk.drop(columns=[c for c in Zk.columns if c.startswith("k_") or c.startswith("es_f15") or c in ("q_olay", "q_panel", "f15_panel", "es_ayni_ceyrek")]),
                         F15p, islem=2)
kontrol("konum eşli: yeniden çağrı aynı sonuç (deterministik)", np.allclose(Zk2.k_es_h5.to_numpy(float), Zk.k_es_h5.to_numpy(float), equal_nan=True))
# TERS ve etiket
hT = {"n": 100, "h5_ust": 0.95, "yari1_kat5": 0.8, "yari2_kat5": 0.9}
kontrol("TERS: üst < 1 ve iki yarı < 1", YH.yh_ters(hT) and not YH.yh_ters({**hT, "yari2_kat5": 1.01}) and not YH.yh_ters({**hT, "h5_ust": 1.0})
        and not YH.yh_ters({**hT, "n": 29}) and not YH.yh_ters({**hT, "h5_ust": np.nan}))
HH = [{"pazar": p, "donem": q, "tutar": False, "ters": False} for p in ("ABD", "AVR", "BIST") for q in ("2016-22", "2023", "2024-26")]
def _set(H, p, q, **kw):
    H = [dict(h) for h in H]
    for h in H:
        if h["pazar"] == p and h["donem"] == q:
            h.update(kw)
    return H
H1 = _set(_set(HH, "ABD", "2023", tutar=True), "ABD", "2024-26", tutar=True)
e1 = YH.yh_etiket3(H1, "EMARE (ABD 2023, ABD 2024-26)")
kontrol("3. tur etiket: EMARE -> 'EMARE (bakılmış hücreler...)'", e1["etiket"].startswith("EMARE (bakılmış hücreler: ABD 2023, ABD 2024-26") and e1["ters_etiket"].startswith("TERS YOK"))
H2 = _set(_set(H1, "ABD", "2016-22", tutar=True), "AVR", "2016-22", tutar=True)
kontrol("3. tur etiket: İZ -> en fazla EMARE; dış sınama iki hücre TUTAR -> 'EMARE (dış sınama tuttu)'", YH.yh_etiket3(H2, "İZ")["etiket"] == "EMARE (dış sınama tuttu)"
        and YH.yh_etiket3(_set(H2, "AVR", "2016-22", tutar=False), "İZ")["etiket"].startswith("EMARE (bakılmış"))
kontrol("3. tur etiket: kural EMARE / İZ değilse aynen", YH.yh_etiket3(HH, "DESTEKLENMEDİ")["etiket"] == "DESTEKLENMEDİ" and YH.yh_etiket3(H2, "ÖLÇÜLEMEDİ")["etiket"] == "ÖLÇÜLEMEDİ")
H3 = _set(_set(HH, "ABD", "2023", ters=True), "AVR", "2024-26", ters=True)
H4 = _set(_set(H3, "ABD", "2016-22", ters=True), "AVR", "2016-22", ters=True)
kontrol("3. tur etiket: >= 2 karar hücresi TERS -> TERS EMARE; dış sınama TERS -> '(dış sınama tuttu)'; tek -> TERS YOK",
        YH.yh_etiket3(H3, "DESTEKLENMEDİ")["ters_etiket"].startswith("TERS EMARE (bakılmış") and YH.yh_etiket3(H4, "x")["ters_etiket"] == "TERS EMARE (dış sınama tuttu)"
        and YH.yh_etiket3(_set(HH, "ABD", "2023", ters=True), "x")["ters_etiket"].startswith("TERS YOK (TERS karar hücresi 1"))
# prefix (geleceğe bakma): yh_hisse_sinyal Y9* kesik = tam
for ad in YH.YH_DENEMELER_3:
    tamam = True; nn = 0
    for toh in (3, 41):
        dx = rastgele_hisse(800, toh, oyn=0.015); Full = YH.yh_hisse_sinyal(dx, ad); Full["tarih"] = pd.to_datetime(Full.tarih)
        for t in sorted(set(Full.tarih) | set(dx.index[[500, 799]])):
            Z_ = YH.yh_hisse_sinyal(dx[dx.index <= t], ad); Z_["tarih"] = pd.to_datetime(Z_.tarih)
            A = Full[Full.tarih <= t].reset_index(drop=True); B = Z_.reset_index(drop=True)
            tamam &= len(A) == len(B) and (len(A) == 0 or (bool((A.tarih == B.tarih).all()) and all(np.allclose(A[c].astype(float), B[c].astype(float), rtol=0, atol=1e-12,
                                                                                                             equal_nan=True) for c in YH._Y9_OZ + ["stop0"])))
            nn += 1
    kontrol(f"{ad}: {nn} kesimde kesik = tam (tarih, stop0, F1 / F11 / F15 / F17)", tamam)
# ---------------------------------------------------------------- 13) 4. TUR (S7 / Y10 / Y10b / Y10c)
print("13) 4. tur (S7: F20-F23, şartlar, Y10 / Y10b / Y10c, prefix, mühür)")
n_ = 20; Lx = np.full(n_, 11.0); Hx = np.full(n_, 11.5); Ox = np.full(n_, 11.2); Cx = np.full(n_, 11.3)
Lx[4:14] = [10.4, 10.2, 10.0, 10.3, 10.6, 10.1, 10.5, 10.8, 10.2, 10.9]; Lx[14:19] = [10.6, 10.5, 10.7, 10.9, 10.8]
Hx[4:19] = 11.5; Hx[9] = 12.0; Lx[19] = 11.5; Hx[19] = 13.0; Ox[19] = 11.8; Cx[19] = 12.6
b19 = YH.yh_s7_bar(Ox, Hx, Lx, Cx, 19)
kontrol("F20 = min L[t-5..t-1] / min L[t-15..t-6] - 1 (yapay)", abs(b19["F20"] - (10.5 / 10.0 - 1)) < 1e-12, b19)
kontrol("F21 = max H[t-15..t-1]; F22 = C_t / F21 - 1; F22a = O_t / F21 - 1; F23 = |C - O| / (H - L) (yapay)",
        b19["F21"] == 12.0 and abs(b19["F22"] - 0.05) < 1e-12 and abs(b19["F22a"] - (11.8 / 12 - 1)) < 1e-12 and abs(b19["F23"] - 0.8 / 1.5) < 1e-12)
Lq = Lx.copy(); Lq[3] = 1.0; Hq = Hx.copy(); Hq[3] = 99.0
kontrol("F20 / F21 yalnız [t-15, t-1] (t-16 barı etkisiz)", YH.yh_s7_bar(Ox, Hq, Lq, Cx, 19) == b19)
b14 = YH.yh_s7_bar(Ox, Hx, Lx, Cx, 14); b15 = YH.yh_s7_bar(Ox, Hx, Lx, Cx, 15)
kontrol("t'den önce 15 bar yoksa F20 / F21 / F22 / F22a NaN; 15 bar varsa tanımlı", all(np.isnan(b14[k]) for k in ("F20", "F21", "F22", "F22a"))
        and all(np.isfinite(b15[k]) for k in ("F20", "F21", "F22", "F22a")))
Hz_ = Hx.copy(); Hz_[19] = Lx[19]
kontrol("H_t = L_t -> F23 NaN", np.isnan(YH.yh_s7_bar(Ox, Hz_, Lx, Cx, 19)["F23"]))
taban = {"F1": 3, "F2": -0.01, "F3": 0.90, "F4": 0.25, "F11": 0.02, "F14": 0.0, "F15": 0.25, "F17": -0.20, "F18": 0.20, "F20": 0.0, "F21": 12.0,
         "F22": 0.001, "F22a": -0.001, "F23": 0.50}
deg = [{}, {"F15": 0.2500001}, {"F17": -0.1999}, {"F1": 2}, {"F2": -0.0101}, {"F2": np.nan}, {"F3": 0.9001}, {"F4": 0.2501}, {"F20": -1e-6},
       {"F20": np.nan}, {"F22": 0.0}, {"F22a": 0.0}, {"F22a": 0.01}, {"F23": 0.4999}, {"F23": np.nan}, {"F18": 0.2001}, {"F14": -1e-6}, {"F14": np.nan},
       {"F15": 0.9, "F17": 0.1}]
Fq = pd.DataFrame([{**taban, **d} for d in deg])
kontrol("Y10: Ş1-Ş8 sınırları kapalı / açık, NaN tutmaz; Ş7 boşluklu açılış (O_t >= F21) elenir",
        list(YH.yh_y10_maske(Fq, "Y10")) == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0])
kontrol("Y10b = Y10 + F14 >= 0 (NaN tutmaz)", list(YH.yh_y10_maske(Fq, "Y10b")) == [1] + [0] * 18)
kontrol("Y10c = Ş2-Ş8 (Ş1 yok)", list(YH.yh_y10_maske(Fq, "Y10c")) == [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1])
rng13 = np.random.default_rng(13); Fr = pd.DataFrame({c: rng13.uniform(a, b, 4000) for c, a, b in
                                                      [("F1", 0, 8), ("F2", -0.05, 0.05), ("F3", 0.3, 1.5), ("F4", 0, 0.5), ("F14", -0.3, 0.3), ("F15", 0, 1),
                                                       ("F17", -0.6, 0.2), ("F18", 0, 0.4), ("F20", -0.1, 0.1), ("F22", -0.02, 0.05), ("F22a", -0.05, 0.02),
                                                       ("F23", 0, 1), ("F11", 0, 0.05)]})
m10, m10b, m10c, m9 = (YH.yh_y10_maske(Fr, "Y10"), YH.yh_y10_maske(Fr, "Y10b"), YH.yh_y10_maske(Fr, "Y10c"), YH.yh_y9_maske(Fr, "Y9"))
kontrol("Y10b ⊆ Y10 ⊆ Y10c; Y10 ⊆ Y9; Y10 = Y9 ∩ Y10c", not (m10b & ~m10).any() and not (m10 & ~m10c).any() and not (m10 & ~m9).any()
        and (m10 == (m9 & m10c)).all() and m10.sum() > 0, (int(m10.sum()), int(m10c.sum())))
okp7, n7 = True, 0
for toh in (5, 17):
    dx = rastgele_hisse(900, toh, oyn=0.015); X1_, _ = YH.yh_s6_hisse(dx); tl = list(pd.to_datetime(X1_.tarih))
    Ft7 = YH.yh_s7_ozellik(dx, tl); dz = YH._yh_hazir(dx)
    for q, t in enumerate(tl):
        i = int(dz.index.get_loc(t))
        a = YH.yh_s7_ozellik(dx[dx.index <= t], [t]).iloc[0].to_numpy(float)
        b = YH.yh_s7_ozellik(dz.iloc[max(0, i - 250):i + 1], [t], hazir=True).iloc[0].to_numpy(float)
        okp7 &= bool(np.allclose(a, Ft7.iloc[q].to_numpy(float), rtol=0, atol=0, equal_nan=True) and np.allclose(b, a, rtol=0, atol=0, equal_nan=True)); n7 += 1
kontrol("S7 prefix: t'de kesik ve [t-250, t] kesiti = tam seri (bütün Y1 günleri)", okp7 and n7 > 10, n7)
kontrol("4. tur denemeleri YH_ESIK'te; Y1-Y9d dizini aynı (plasebo / denetim tohumu)", all(k in YH.YH_ESIK["denemeler"] for k in YH.YH_DENEMELER_4)
        and YH.YH_DENEMELER_HEPSI[:13] == YH.YH_DENEMELER + YH.YH_DENEMELER_2 + YH.YH_DENEMELER_3)
y3_ = YH._yh_yol("onkayit3")
if os.path.exists(y3_):
    import re as _re
    m_ = _re.search(r"YH_ESIK_SHA:\s*`([0-9a-f]{64})`", open(y3_, encoding="utf-8").read())
    kontrol("ESIK_TUR3_SHA = ON_KAYIT_3.md YH_ESIK_SHA (Y1-Y9d eşikleri aynen)", m_ and m_.group(1) == YH.yh_esik_sha_tur3())
if os.path.exists(YH.YH_YOL["ozellik_s7"]) and os.path.exists(YH.YH_YOL["ozellik"]):
    F4r = YH.yh_ozellik4_oku()
    kontrol("gerçek: S7 dosyası anahtarları = ozellik_Y1 anahtarları (26.663)", len(F4r) == 26663, len(F4r))
    U4 = YH.yh_cemal_uyum4(F4r)
    kontrol("gerçek: Cemal uyumu (hakem KÖR + TUR 1 + TUR 2) sayfalar özellikle eşleşti, h5 okunmadı", U4["n"] >= 70 and set(U4["set"]) == {"hakem (KÖR)", "TUR 1", "TUR 2"},
            (U4["n"], U4["set"]))

# ---------------------------------------------------------------- 14) 5. TUR (Ş9 / Y11 / Y11b / Y11c)
print("14) 5. tur (Ş9: F24-F29 yapay vakalar, şartlar, Y11 / Y11b / Y11c, prefix, mühür)")


def s9_yap(w, n0=260):
    L = np.r_[np.full(n0, 99.0), w, [w[-1]]]; H = L + 2.0; C = L + 1.0; H[:n0] = 101.0; C[:n0] = 100.0
    return H, L, C, len(L) - 1


x40 = np.arange(40.0)
vaka = {"parabol": 90 + 0.01 * (x40 - 18) ** 2, "alcalan": 95 - 0.5 * x40 + 0.004 * x40 ** 2 + 1.2 * np.abs(np.sin(np.pi * x40 / 6)),
        "duz": 90 + 0.05 * np.sin(x40), "semsiye": 95 - 0.01 * (x40 - 20) ** 2}
R9 = {}
for ad_, w_ in vaka.items():
    H_, L_, C_, i_ = s9_yap(w_); R9[ad_] = YH.yh_s9_bar(H_, L_, C_, i_)
F9 = pd.DataFrame([R9[k] for k in vaka]); S9v = YH.yh_s9_sartlar(F9)["S9"]; A9 = YH.yh_s9_alt(F9)
atr_ = 0.02 * float(np.mean(vaka["parabol"] + 1.0))
kontrol("Ş9 tam parabol geçer (F24 = a / ATR, F25 = 18 / 39, R² = 1, F27 = 3,24 / ATR, F28 = 4,41 / ATR, F29 = 0)", bool(S9v[0])
        and abs(R9["parabol"]["F24"] - 0.01 / atr_) < 1e-9 and abs(R9["parabol"]["F25"] - 18 / 39) < 1e-9 and abs(R9["parabol"]["F26"] - 1) < 1e-9
        and abs(R9["parabol"]["F27"] - 3.24 / atr_) < 1e-6 and abs(R9["parabol"]["F28"] - 4.41 / atr_) < 1e-6 and abs(R9["parabol"]["F29"]) < 1e-6, R9["parabol"])
kontrol("Ş9 alçalan dipler zinciri geçmez (dip pencere sonunda: F25 > 0,75, F28 < 0,5)", not S9v[1] and not A9["b"][1] and not A9["e"][1], R9["alcalan"])
kontrol("Ş9 düz taban geçmez (F27 < 1)", not S9v[2] and not A9["d"][2], R9["duz"])
kontrol("Ş9 şemsiye (a < 0) geçmez; F25 / F27 / F28 / F29 NaN", not S9v[3] and R9["semsiye"]["F24"] < 0 and all(np.isnan(R9["semsiye"][k]) for k in ("F25", "F27", "F28", "F29")))
H_, L_, C_, i_ = s9_yap(vaka["parabol"]); L2_ = L_.copy(); L2_[i_] = 1.0; H2_ = H_.copy(); H2_[i_] = 500.0
kontrol("Ş9 t barını okumaz (L_t / H_t değişince aynı)", YH.yh_s9_bar(H2_, L2_, C_, i_) == R9["parabol"])
H3_, L3_, C3_ = H_.copy(), L_.copy(), C_.copy(); H3_[: i_ - 291] = 999.0; L3_[: i_ - 291] = 0.5
kontrol("Ş9 yalnız [t-291, t-1] okur (öncesi etkisiz)", YH.yh_s9_bar(H3_, L3_, C3_, i_) == R9["parabol"])
kontrol("Ş9: t'den önce 40 bar ya da 120 bar ATR yoksa NaN", all(np.isnan(v) for v in YH.yh_s9_bar(H_, L_, C_, 39).values())
        and all(np.isnan(v) for v in YH.yh_s9_bar(H_[150:], L_[150:], C_[150:], i_ - 150).values()))
t9 = {"F24": 0.001, "F25": 0.20, "F26": 0.40, "F27": 1.0, "F28": 0.5, "F29": 5.0}
d9 = [{}, {"F25": 0.75}, {"F29": -5.0}, {"F24": 0.0}, {"F25": 0.1999}, {"F25": 0.7501}, {"F26": 0.3999}, {"F27": 0.9999}, {"F28": 0.4999},
      {"F29": 5.0001}, {"F25": np.nan}]
kontrol("Ş9 sınırları: F24 > 0 açık, F25 [0,20, 0,75] kapalı, F26 / F27 / F28 >= kapalı, |F29| <= 5 kapalı, NaN tutmaz",
        list(YH.yh_s9_sartlar(pd.DataFrame([{**t9, **d} for d in d9]))["S9"]) == [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
Fr9 = Fr.copy(); rng14 = np.random.default_rng(14)
for c_, a_, b_ in [("F24", -0.01, 0.02), ("F25", 0, 1), ("F26", 0, 1), ("F27", 0, 4), ("F28", 0, 3), ("F29", -12, 12)]:
    Fr9[c_] = rng14.uniform(a_, b_, len(Fr9))
m11, m11b, m11c = (YH.yh_y11_maske(Fr9, k) for k in YH.YH_DENEMELER_5)
S_all = YH.yh_s9_sartlar(Fr9)
kontrol("Y11 = Ş1 + Ş2 + Ş9; Y11b = Y10 şartları Ş6 yerine Ş9; Y11c = Ş9; Y11 ⊆ Y9; Y11b ⊆ Y11 ⊆ Y11c",
        (m11 == (S_all["S1"] & S_all["S2"] & S_all["S9"])).all() and (m11c == S_all["S9"]).all()
        and (m11b == (S_all["S1"] & S_all["S2"] & S_all["S3"] & S_all["S4"] & S_all["S5"] & S_all["S9"] & S_all["S7"] & S_all["S8"])).all()
        and not (m11 & ~m9).any() and not (m11b & ~m11).any() and not (m11 & ~m11c).any() and m11.sum() > 0, (int(m11.sum()), int(m11b.sum()), int(m11c.sum())))
okp9, n9_ = True, 0
for toh in (5, 17):
    dx = rastgele_hisse(900, toh, oyn=0.015); X1_, _ = YH.yh_s6_hisse(dx); tl = list(pd.to_datetime(X1_.tarih))
    Ft9 = YH.yh_s9_ozellik(dx, tl); dz = YH._yh_hazir(dx)
    for q, t in enumerate(tl):
        i = int(dz.index.get_loc(t))
        a = YH.yh_s9_ozellik(dx[dx.index <= t], [t]).iloc[0].to_numpy(float)
        b = YH.yh_s9_ozellik(dz.iloc[max(0, i - 291):i + 1], [t], hazir=True).iloc[0].to_numpy(float)
        okp9 &= bool(np.allclose(a, Ft9.iloc[q].to_numpy(float), rtol=1e-12, atol=0, equal_nan=True) and np.allclose(b, a, rtol=1e-12, atol=0, equal_nan=True)); n9_ += 1
kontrol("S9 prefix: t'de kesik ve [t-291, t] kesiti = tam seri (bütün Y1 günleri)", okp9 and n9_ > 10, n9_)
kontrol("5. tur denemeleri YH_ESIK'te; Y1-Y10c dizini aynı (plasebo / denetim tohumu)", all(k in YH.YH_ESIK["denemeler"] for k in YH.YH_DENEMELER_5)
        and YH.YH_DENEMELER_HEPSI[:16] == YH.YH_DENEMELER + YH.YH_DENEMELER_2 + YH.YH_DENEMELER_3 + YH.YH_DENEMELER_4)
y4_ = YH._yh_yol("onkayit4")
if os.path.exists(y4_):
    import re as _re
    m_ = _re.search(r"YH_ESIK_SHA:\s*`([0-9a-f]{64})`", open(y4_, encoding="utf-8").read())
    kontrol("ESIK_TUR4_SHA = ON_KAYIT_4.md YH_ESIK_SHA (Y1-Y10c eşikleri aynen)", m_ and m_.group(1) == YH.yh_esik_sha_tur4())
if os.path.exists(YH.YH_YOL["ozellik_s9"]) and os.path.exists(YH.YH_YOL["ozellik_s7"]) and os.path.exists(YH.YH_YOL["ozellik"]):
    F5r = YH.yh_ozellik5_oku()
    kontrol("gerçek: S9 dosyası anahtarları = ozellik_Y1 anahtarları (26.663)", len(F5r) == 26663, len(F5r))

# mühürler
y2_ = YH._yh_yol("onkayit2")
if os.path.exists(y2_):
    import re as _re
    m_ = _re.search(r"YH_ESIK_SHA:\s*`([0-9a-f]{64})`", open(y2_, encoding="utf-8").read())
    kontrol("ESIK_TUR2_SHA = ON_KAYIT_2.md YH_ESIK_SHA (Y1-Y8B eşikleri aynen)", m_ and m_.group(1) == YH.yh_esik_sha_tur2())
kontrol("3. tur denemeleri YH_ESIK'te; Y1-Y8B dizini aynı", all(k in YH.YH_ESIK["denemeler"] for k in YH.YH_DENEMELER_3)
        and YH.YH_DENEMELER_HEPSI[:9] == YH.YH_DENEMELER + YH.YH_DENEMELER_2)
sj = YH._yh_yol("sonuc")
if os.path.exists(sj):
    Jr = json.load(open(sj, encoding="utf-8"))
    hr = [h for h in Jr["deneme"]["Y1"]["hucre"] if h["pazar"] == "ABD" and h["donem"] == "2023"][0]
    kontrol("regresyon: Y1 ABD 2023 n 2040, KAT5 0,9752 (sonuc.json)", hr["n"] == 2040 and abs(hr["h5_kat"] - 0.9752) < 5e-5, (hr["n"], hr["h5_kat"]))

print("13) 6. TUR: grup bayrakları, G3, karne etiketi, mahkeme kararı, C13, aday prefix")
Fg = pd.DataFrame({"F14": [0.0, -0.01, 0.1, np.nan, 0.2], "F15": [0.5, 0.9, 0.25, 0.1, 0.49], "F17": [-0.3, -0.3, -0.2, -0.5, -0.1],
                   **{c: [np.nan] * 5 for c in YH._Y11_OZ_S9}})
Mg = YH.yh_grup6_maske(Fg)
kontrol("G1 = F14 >= 0 VE F15 >= 0,50 (NaN tutmaz)", list(Mg["G1"]) == [True, False, False, False, False])
kontrol("G2 = F15 <= 0,25 VE F17 <= -0,20 (sınır dahil); G2u Ş9 NaN -> yok", list(Mg["G2"]) == [False, False, True, True, False] and not Mg["G2u"].any())
Mt = pd.DataFrame({"pazar": ["ABD"] * 40, "sembol": [f"S{i:02d}" for i in range(40)], "tarih": pd.Timestamp("2023-05-01"), "donem": "2023",
                   "G2": [True] * 7 + [False] * 33})
g3a = YH.yh_grup6_g3(Mt); g3b = YH.yh_grup6_g3(Mt.sample(frac=1.0, random_state=9))
kontrol("G3: n = G2 n, satır sırasından bağımsız (tohumlu)", len(g3a) == 7 and g3a.equals(g3b))
kontrol("G3: G2 0 olan hücrede 0", len(YH.yh_grup6_g3(Mt.assign(G2=False))) == 0)
kontrol("karne etiketi: KATKI+ / KATKI− / SORGULA (çelişki, n < 30, NaN)",
        YH._yh_karne_etiket(0.01, 0.02, 30, 31, 30) == "KATKI+" and YH._yh_karne_etiket(-0.01, -0.02, 40, 40, 30) == "KATKI−"
        and YH._yh_karne_etiket(0.01, -0.02, 40, 40, 30) == "SORGULA" and YH._yh_karne_etiket(0.01, 0.02, 29, 40, 30) == "SORGULA"
        and YH._yh_karne_etiket(np.nan, 0.02, 40, 40, 30) == "SORGULA")
kr = lambda tut: {k: (k in tut) for k in YH._YH_KURAL6}  # noqa: E731
sec_ = {"bar": 0, "tur": "AL", "kural": kr(["S1", "S2", "S3"]), "puan": 3}
ad_ = [{"bar": -40, "tur": "AL", "kural": kr(["S1", "S2", "S3", "S4", "S5"]), "puan": 5}, {"bar": -10, "tur": "Ş9 ÇANAK", "kural": kr(["S9"]), "puan": 1}]
Kk = YH.yh_m_karar(sec_, ad_)
kontrol("mahkeme: önceki aday daha yüksek puanlı -> ÖNCEKİ BÖLGE DAHA UYGUN (bar, puan, eksikler)", Kk["onceki_daha_uygun"]
        and Kk["karar"].startswith("ÖNCEKİ BÖLGE DAHA UYGUN: bar -40") and "5/12 vs seçilen 3/12" in Kk["karar"] and "Ş4 küçük mum" in Kk["karar"]
        and not Kk["tam_puan"], Kk["karar"])
Kk2 = YH.yh_m_karar({**sec_, "kural": kr(YH._YH_KURAL6), "puan": 12}, ad_)
kontrol("mahkeme: seçilen tam puan -> SEÇİM TUTARLI, eksik yok", not Kk2["onceki_daha_uygun"] and Kk2["karar"].startswith("SEÇİM TUTARLI") and Kk2["tam_puan"])
Kk3 = YH.yh_m_karar(sec_, [{**ad_[0], "puan": 3}, {**ad_[0], "bar": -5, "puan": 3}])
kontrol("mahkeme: eşit puan -> SEÇİM TUTARLI; en iyi aday eşitlikte en yakın", not Kk3["onceki_daha_uygun"] and Kk3["en_iyi"]["bar"] == -5)
kontrol("mahkeme: önceki aday yok -> SEÇİM TUTARLI (önceki aday yok)", YH.yh_m_karar(sec_, [])["karar"] == "SEÇİM TUTARLI (önceki aday yok)")
Cc = np.r_[np.full(260, 100.0)] * np.cumprod(np.r_[1.0, np.full(259, 1.001)]); Hc = Cc * 1.01; Lc = Cc * 0.99
c13a = YH._yh_c13(Hc, Lc, Cc, 259, 250); Cc2 = Cc.copy(); Cc2[200:] *= 1.15; c13b = YH._yh_c13(Cc2 * 1.01, Cc2 * 0.99, Cc2, 259, 250)
kontrol("C13: dev mum yok -> <= 4, %15 sıçrama -> > 4; 250 bar yoksa NaN", c13a <= 4 and c13b > 4 and np.isnan(YH._yh_c13(Hc, Lc, Cc, 200, 250)), (c13a, c13b))
dfm = rastgele_hisse(1300, 77, bas="2019-01-01", oyn=0.015)
X1m, _ = YH.yh_s6_hisse(dfm)
nm, npre, nonc = 0, 0, 0
for tm in list(pd.to_datetime(X1m.tarih))[-8:]:
    Mm = YH.yh_mahkeme_hisse(dfm, tm)             # prefix kapısı içeride (aday değerleri t_k'da kesik veriyle aynı, değilse DURUR)
    Mk = YH.yh_mahkeme_hisse(dfm[dfm.index <= tm + pd.Timedelta(days=400)], tm, prefix=False)
    nm += 1; npre += len(Mm["adaylar"]); nonc += int(Mm["onceki_daha_uygun"])
    assert Mm["karar"] == Mk["karar"] and [a["bar"] for a in Mm["adaylar"]] == [a["bar"] for a in Mk["adaylar"]]
    assert all(-250 <= a["bar"] <= -1 for a in Mm["adaylar"])
kontrol("mahkeme: t sonrası veri kararı değiştirmez; adaylar [t-250, t-1]; aday prefix kapısı geçti", nm == min(8, len(X1m)) and nm >= 5 and npre > 0, (nm, npre, nonc))

print(f"\nSONUÇ: {len(GECTI)} geçti, {len(KALDI)} kaldı" + (f" -> {KALDI}" if KALDI else ""))
sys.exit(1 if KALDI else 0)
