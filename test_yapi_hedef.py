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
        V_ = {f"{p}{i:02d}": rastgele_hisse(1900, 1000 * pi + i, bas="2019-01-01", oyn=0.015) for i in range(36)}
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
    kontrol("2. tur: Y6 / Y7 / Y8 + Y8B (bilgi) eklendi", set(J3["deneme"]) == set(YH.YH_DENEMELER_HEPSI) and J3["deneme"]["Y8B"].get("bilgi") is True)
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
finally:
    YH.YH_YOL.clear(); YH.YH_YOL.update(yol_eski)
    shutil.rmtree(tmp, ignore_errors=True)

print("10) e-posta / anahtar, çakışma kapısı")
temiz = True
for ad in ("YAPI_HEDEF.py", "test_yapi_hedef.py"):
    m = open(os.path.join(KOK, ad), encoding="utf-8").read()
    if YH._YH_EPOSTA.search(m) or YH._YH_ANAHTAR.search(m):
        temiz = False
for ad in ("onkayit", "sonuc", "rapor", "guc_json", "guc_md"):
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

print(f"\nSONUÇ: {len(GECTI)} geçti, {len(KALDI)} kaldı" + (f" -> {KALDI}" if KALDI else ""))
sys.exit(1 if KALDI else 0)
