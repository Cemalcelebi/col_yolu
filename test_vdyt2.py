"""VDYT2 testleri — YALNIZ SENTETİK veri (gerçek veriye dokunmaz; ağ yok). Çalıştırma: python test_vdyt2.py

1) sessiz bölge tanımları elle (G1 küçük mum, G2 dar bant, G3 yaklaşan tepe-dip, G4 savunulan destek = V1.vdyt_savunma'nın kayan penceresi, G5 bileşik)
2) ön koşul P1 / P2 elle  3) büyük mum, onay, etiket YALNIZ t'den sonra (g > t), NaN kuralı, geçerli karar günü (D1a)  4) bölge motoru elle (açılış, devam,
SÖNME, BÜYÜK MUM, SANSÜR, kopukluk, yeniden açılış aralığı)  5) GELECEĞE BAKMAZ (t sonrası barlar bozulunca durumlar, geçerlilik, özellikler, ön koşul aynı)
6) BHU elle  7) walk-forward sızıntısı (eğitim etiketi test yılına taşmaz; eşikler / standartlaştırma yalnız eğitimden; test etiketi değişince tahmin aynı)
8) kontrol satırları (DIŞARI sıkışma dışı ve aynı yıl / NATR ondalığı; RASTGELE aynı süre dağılımı; aynı etiket ve geçerlilik)  9) oran karşılaştırması ve
D1b skill farkı elle  10) sınıflandırma kuralları + eşiklerin yalnız eğitimden gelmesi  11) TESPİT GÜNÜ grafiğinde gelecek öğe yok; ciz üstüne yazmaz
12) mühür / ön kayıt üzerine yazmaz / ret kapısı (git, kod, VDYT.py, mühür) / KASA tek açılış / canlı KASA'sız ret  13) uçtan uca sentetik (kapsam yalnız
sayar; kos wf + kasa; karar tablosu üç başarı ayrı; paket + ciz)  14) Yahoo takvim ayrıştırıcı  15) çakışma kapısı  16) bağımsızlık (Çöl Yolu / K modülü
yok), e-posta / anahtar yok, VDYT.py / v1 dosyaları değişmedi.
"""
from __future__ import annotations

import copy
import gzip
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import VDYT as V1  # noqa: E402
import VDYT2 as V  # noqa: E402

E0 = V.VDYT2_ESIK


def kucuk_E() -> dict:
    E = copy.deepcopy(E0); E["basari"]["bootstrap"] = 200; E["model"]["min_egitim"] = 50; E["coklu"]["plasebo_olay_tekrar"] = 1
    return E


def durmali(fn, mesaj: str, hata: list, icerik: str = "") -> None:
    try:
        fn()
    except (V.Vdyt2Hata, V1.VdytHata, RuntimeError) as ex:
        if icerik and icerik not in str(ex):
            hata.append(f"{mesaj} (yanlış neden: {ex})")
        return
    hata.append(mesaj)


def rastgele_bar(n: int, tohum: int = 1, bas: str = "2015-01-01", sig: float = 0.015) -> pd.DataFrame:
    rng = np.random.default_rng(tohum); c = 100 * np.exp(np.cumsum(rng.normal(0, sig, n))); o = c * np.exp(rng.normal(0, sig / 3, n))
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, sig / 2, n))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, sig / 2, n)))
    return pd.DataFrame({"o": o, "h": h, "l": l, "c": c, "v": rng.lognormal(10, 0.4, n)}, index=pd.bdate_range(bas, periods=n))


def sentetik_pazar(nh: int = 12, bas: str = "2013-01-01", bit: str = "2025-12-31", tohum: int = 7, pazar: str = "BIST"):
    """Sert hareket -> küçük mumlu sessiz bölge -> büyük mumlar döngüleri içeren sentetik OHLCV + olaylar (bilanço, B olayı, FOMC benzeri)."""
    rng = np.random.default_rng(tohum); gun = pd.bdate_range(bas, bit); n = len(gun); S = {}; ol = []
    for j in range(nh):
        sig = np.full(n, 0.02); mu = np.zeros(n); i = 300
        while i < n - 200:
            D = int(rng.integers(20, 40)); mu[i: i + D] = -0.45 / D * (1 if rng.random() < 0.7 else -0.8)
            Lq = int(rng.integers(25, 90)); q0 = i + D; sig[q0: q0 + Lq] = 0.004
            mu[q0 + Lq: q0 + Lq + 5] = rng.choice([-1, 1]) * 0.03; sig[q0 + Lq: q0 + Lq + 5] = 0.05
            i = q0 + Lq + int(rng.integers(80, 220))
        r = mu + rng.normal(0, 1, n) * sig
        c = 50 * np.exp(np.cumsum(r)); o = np.r_[c[0], c[:-1]] * np.exp(rng.normal(0, 0.3, n) * sig)
        h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.4, n)) * sig); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.4, n)) * sig)
        s = f"S{j:02d}"; S[s] = pd.DataFrame({"o": o, "h": h, "l": l, "c": c, "v": rng.lognormal(12, 0.5, n) * (1 + j)}, index=gun)
        for k in range(150, n, 63):
            ol.append((pazar, s, f"{pazar}_BILANCO", "A", True, gun[k], gun[k], "sentetik", ""))
        for k in rng.choice(n - 10, 15, replace=False):
            ol.append((pazar, s, "BIST_ICERIDEN_ALIM" if pazar == "BIST" else "ABD_8K", "B", False, gun[k], gun[k], "sentetik", ""))
    for k in range(200, n, 30):
        ol.append((pazar, "*", "MAKRO_FOMC", "C", True, gun[k], gun[k], "sentetik", ""))
    if nh >= 3:   # uç durumlar: kısa geçmişli hisse, işlem durması (kopukluk) + sabit fiyatlı günler
        S["K1"] = S["S00"].iloc[-300:].copy() * 1.1
        k2 = S["S01"].copy(); k2 = k2.drop(k2.index[1500:1530]); k2.iloc[800:806, :4] = k2.iloc[800, 3]; S["K2"] = k2
    Ev = pd.DataFrame(ol, columns=V1.OLAY_SUTUN); Ev["g0_tarih"] = pd.to_datetime(Ev.g0_tarih); Ev["bilgi_tarih"] = pd.to_datetime(Ev.bilgi_tarih)
    return {"S": S, "meta": {s: {"tur": "EQUITY", "son": S[s].index[-1]} for s in S}, "kaynak": "sentetik"}, Ev


def git(kl: str, *a: str) -> str:
    return subprocess.run(["git", "-C", kl, "-c", "user.name=vdyt2", "-c", "user.email=vdyt2@test.invalid"] + list(a), capture_output=True, text=True,
                          check=True).stdout


def bolge_sabit(n=80, sessiz=(20, 60), buyuk=None):
    """Elle denetlenebilir dizi: TR, gövde, kapanış; sessiz aralıkta küçük, isteğe bağlı büyük mum günü."""
    tr = np.full(n, 1.0); gv = np.full(n, 0.5); c = np.full(n, 100.0) + np.sin(np.arange(n)) * 0.2
    tr[sessiz[0]: sessiz[1]] = 0.3; gv[sessiz[0]: sessiz[1]] = 0.1
    if buyuk is not None:
        tr[buyuk] = 2.0; gv[buyuk] = 1.0
    return tr, gv, c


def testler() -> list:
    hata: list = []
    E = E0; L = int(E["sessiz"]["L"])
    # ---------------------------------------------------------------- 1) sessiz bölge tanımları elle
    d = rastgele_bar(700); Ol = V.v2_olculer(d); o, h, l, c = (d[k].to_numpy() for k in "ohlc"); t = 650
    tr = Ol["tr"]; atr_ref = np.mean(tr[t - L - 249: t - L + 1]); rng_ = h - l; gv = np.abs(c - o); w = slice(t - L + 1, t + 1)
    if not np.isclose(Ol["atr_ref"][t], atr_ref):
        hata.append("1) ATRref elle tutmadı")
    if not (np.isclose(Ol["m_aralik_atr"][t], np.median(rng_[w]) / atr_ref) and np.isclose(Ol["m_govde_atr"][t], np.median(gv[w]) / atr_ref)
            and np.isclose(Ol["m_maks_aralik"][t], np.max(rng_[w]) / atr_ref)):
        hata.append("1) G1 ölçüleri elle tutmadı")
    if not np.isclose(Ol["m_doji_pay"][t], np.mean(gv[w] <= 0.10 * rng_[w])):
        hata.append("1) doji payı elle tutmadı")
    kb = lambda i: (c[i - L + 1: i + 1].max() - c[i - L + 1: i + 1].min()) / c[i - L + 1: i + 1].mean()   # noqa: E731
    kb_ref = np.median([kb(i) for i in range(t - L - 249, t - L + 1)])
    gb = lambda i: (np.maximum(o, c)[i - L + 1: i + 1].max() - np.minimum(o, c)[i - L + 1: i + 1].min()) / c[i - L + 1: i + 1].mean()   # noqa: E731
    gb_ref = np.median([gb(i) for i in range(t - L - 249, t - L + 1)])
    if not (np.isclose(Ol["b_kapanis_bant"][t], kb(t) / kb_ref) and np.isclose(Ol["b_govde_bant"][t], gb(t) / gb_ref)):
        hata.append("1) G2 bant oranları elle tutmadı")
    x = np.arange(L)
    if not (np.isclose(Ol["b_egim_tepe"][t], np.polyfit(x, h[w], 1)[0] / atr_ref) and np.isclose(Ol["b_egim_dip"][t], np.polyfit(x, l[w], 1)[0] / atr_ref)):
        hata.append("1) G3 eğimleri elle tutmadı")
    G1e = E["sessiz"]["G1"]
    g1 = (Ol["m_aralik_atr"] <= G1e["aralik_atr"][0]) & (Ol["m_govde_atr"] <= G1e["govde_atr"]) & (Ol["m_maks_aralik"] <= G1e["maks_aralik_atr"])
    if not np.array_equal(Ol["durum"]["G1"], np.nan_to_num(g1, nan=False).astype(bool)):
        hata.append("1) G1 durum eşiği")
    g2 = (Ol["b_kapanis_bant"] <= 0.5) & (Ol["b_govde_bant"] <= 0.5); g3 = (Ol["b_egim_tepe"] <= 0) & (Ol["b_egim_dip"] >= 0)
    if not np.array_equal(Ol["durum"]["G2"], g2) or not np.array_equal(Ol["durum"]["G3"], g3):
        hata.append("1) G2 / G3 durum eşiği")
    if not np.array_equal(Ol["durum"]["G5"], Ol["durum"]["G1"] & Ol["durum"]["G2"] & (Ol["durum"]["G3"] | Ol["durum"]["G4"])):
        hata.append("1) G5 = G1 ve G2 ve (G3 ya da G4) tutmadı")
    if not np.array_equal(Ol["durum"]["G12"], Ol["durum"]["G1"] & Ol["durum"]["G2"]):
        hata.append("1) G5 devam durumu (G1 ve G2) tutmadı")
    # G4 = V1.vdyt_savunma'nın kayan penceresi (her taban), hat VAR ve kırılma YOK
    W4 = int(E["sessiz"]["G4"]["pencere"]); v = d.v.to_numpy(); fark = 0
    for tb in ("govde", "fitil", "kapanis"):
        hv, kr, sv = V.v2_hat_pencere(o, h, l, c, tr, W4, tb)
        for t_ in range(300, 700, 7):
            s1 = V1.vdyt_savunma(o, h, l, c, v, tr, Ol["atr"], t_ - W4 + 1, t_, tb, V1.VDYT_ESIK)
            if bool(s1["hat_var"]) != bool(hv[t_]) or (s1["hat_var"] and bool(s1["kirilma"]) != bool(kr[t_])) or \
                    (np.isfinite(s1["seviye"]) and not np.isclose(s1["seviye"], sv[t_])):
                fark += 1
    if fark:
        hata.append(f"1) G4 kayan pencere V1.vdyt_savunma ile {fark} günde farklı")
    hv, kr, _sv = V.v2_hat_pencere(o, h, l, c, tr, W4, "govde")
    if not np.array_equal(Ol["durum"]["G4"], hv & ~kr):
        hata.append("1) G4 'savunulan' (hat var ve kırılma yok) tutmadı")
    # elle küçük örnek: üç eşit gövde dibi, aralık >= 5 bar -> hat VAR; sonra kapanış kırılırsa savunulmuyor
    n = 20; o2 = np.full(n, 10.5); c2 = np.full(n, 10.6); h2 = np.full(n, 10.9); l2 = np.full(n, 10.4); tr2 = np.full(n, 0.5)
    for i in (2, 9, 16):
        o2[i], c2[i], l2[i] = 10.0, 10.2, 9.95
    hv2, kr2, sv2 = V.v2_hat_pencere(o2, h2, l2, c2, tr2, 20, "govde")
    if not (hv2[-1] and not kr2[-1] and np.isclose(sv2[-1], 10.0)):
        hata.append(f"1) elle hat örneği: {hv2[-1]}, {kr2[-1]}, {sv2[-1]}")
    c3 = c2.copy(); c3[18] = 9.7; o3 = o2.copy(); l3 = l2.copy(); l3[18] = 9.65
    hv3, kr3, _ = V.v2_hat_pencere(o3, h2, l3, c3, tr2, 20, "govde")
    if not kr3[-1]:
        hata.append("1) kapanışla kırılan hat 'savunulan' sayıldı")
    if not np.array_equal(Ol["durum"]["V1:T1"], V1.vdyt_durum(Ol, "T1", 0, V1.VDYT_ESIK)):
        hata.append("1) v1 T1 durumu içe aktarılandan farklı")

    # ---------------------------------------------------------------- 2) ön koşul elle
    cc = np.r_[np.full(100, 100.0), np.linspace(100, 60, 30), np.full(30, 60.0)]
    dd, uu, p1, p2 = V.v2_onkosul(cc, 140)
    if not (np.isclose(dd, 60 / 100 - 1) and p1 == 1 and p2 == 1):
        hata.append(f"2) P1 elle: {dd}, {p1}, {p2}")
    cc2 = np.r_[np.full(100, 100.0), np.linspace(100, 140, 30), np.full(30, 140.0)]
    dd2, uu2, p1b, p2b = V.v2_onkosul(cc2, 140)
    if not (p1b == 0 and p2b == 1 and np.isclose(uu2, 0.4)):
        hata.append(f"2) P2 (yukarı hareket) elle: {p1b}, {p2b}, {uu2}")
    if not np.isnan(V.v2_onkosul(cc, 100)[2]):
        hata.append("2) 120 bardan kısa geçmişte ön koşul tanımsız olmalı")
    if not np.isnan(V.v2_onkosul(cc, 119)[0]):
        hata.append("2) geçmiş 120 bar değilken ölçüldü")

    # ---------------------------------------------------------------- 3) büyük mum, onay, etiket (yalnız t'den sonra), geçerlilik
    trb, gvb, cb = bolge_sabit(120, (10, 100), buyuk=50); kop = np.zeros(120, bool)
    if not V.v2_buyuk_mum(50, 10, trb, gvb, cb) or V.v2_buyuk_mum(49, 10, trb, gvb, cb):
        hata.append("3) büyük mum elle")
    trc = trb.copy(); trc[50] = 0.3 * 2.5 - 1e-6
    if V.v2_buyuk_mum(50, 10, trc, gvb, cb):
        hata.append("3) k_b eşiğin altında büyük mum sayıldı")
    gvc = gvb.copy(); gvc[50] = 0.1 * 3 - 1e-6
    if V.v2_buyuk_mum(50, 10, trb, gvc, cb):
        hata.append("3) gövde şartı (m) uygulanmadı")
    if not V.v2_buyuk_mum(50, 10, trb, gvc, cb, kapanis=True):
        hata.append("3) kapanış kipinde gövde şartı uygulanmamalı")
    if V.v2_buyuk_mum(14, 10, trb, gvb, cb):
        hata.append("3) ref_min'den kısa referansla büyük mum sayıldı")
    cu = cb.copy(); cu[50:] = 105.0
    if V.v2_onay(50, 10, cu, kop) != (1, 50):
        hata.append(f"3) onay yukarı: {V.v2_onay(50, 10, cu, kop)}")
    cd_ = cb.copy(); cd_[53:] = 90.0
    if V.v2_onay(50, 10, cd_, kop) != (-1, 53):
        hata.append(f"3) onay aşağı: {V.v2_onay(50, 10, cd_, kop)}")
    if V.v2_onay(50, 10, cb, kop)[0] != 0:
        hata.append("3) bant içinde kalan büyük mum onaylı sayıldı")
    if V.v2_onay(115, 10, cb, kop)[0] != -9:
        hata.append("3) veri sonu taşan onay belirsiz olmalı")
    Y = V.v2_etiket(40, 10, cu, trb, gvb, kop)
    if not (Y["g"] == 50 and Y["y5"] == 0 and Y["y10"] == 1 and Y["y20"] == 1 and Y["yon"] == 1):
        hata.append(f"3) etiket elle: {Y}")
    Y2 = V.v2_etiket(50, 10, cu, trb, gvb, kop)
    if Y2["g"] == 50 or Y2["y20"] == 1:
        hata.append(f"3) etiket t gününde başlayan hareketi saydı (g > t olmalı): {Y2}")
    Y3 = V.v2_etiket(95, 10, cu, trb, gvb, kop)
    if not (np.isnan(Y3["y20"]) and Y3["y10"] == 0 and np.isnan(V.v2_etiket(101, 10, cu, trb, gvb, kop)["y10"])):
        hata.append(f"3) veri sonunu aşan ufuk ölçüldü: {Y3}")
    kp = kop.copy(); kp[60] = True
    if not np.isnan(V.v2_etiket(45, 10, cb, trb, gvb, kp)["y20"]):
        hata.append("3) kopukluk içeren ufuk ölçüldü")
    # ilk onaysız büyük mum atlanır, sonraki onaylı mum etiket olur
    tr4, gv4, c4 = bolge_sabit(120, (10, 100)); tr4[45] = 2.0; gv4[45] = 1.0; tr4[55] = 2.0; gv4[55] = 1.0; c4[55:] = 104.0
    Y4 = V.v2_etiket(40, 10, c4, tr4, gv4, kop)
    if Y4["g"] != 55 or Y4["y10"] != 0 or Y4["y20"] != 1:
        hata.append(f"3) onaysız mum atlanmadı: {Y4}")
    # vektörel referans bloğu (v2_ref_blok) skaler v2_buyuk_mum / v2_onay ile birebir aynı
    rng = np.random.default_rng(11); nn = 400; trr = rng.lognormal(0, 0.6, nn); gvr = trr * rng.uniform(0, 1, nn); crr = 100 + np.cumsum(rng.normal(0, 1, nn))
    kz = np.zeros(nn, bool); fark = 0
    for bs in (0, 37, 150, 300):
        bl = V.v2_ref_blok(bs, bs + 1, bs + 120, trr, gvr, crr)
        for g in range(bl["g0"], bl["g1"] + 1):
            k = g - bl["g0"]; a_ = max(bs, g - 60)
            if bool(bl["buyuk"][k]) != V.v2_buyuk_mum(g, bs, trr, gvr, crr):
                fark += 1
            if g - a_ >= 1 and not (np.isclose(bl["lo"][k], crr[a_:g].min()) and np.isclose(bl["hi"][k], crr[a_:g].max())):
                fark += 1
            if bool(V.v2_ref_blok(bs, g, g, trr, gvr, crr, kapanis=True)["buyuk"][0]) != V.v2_buyuk_mum(g, bs, trr, gvr, crr, kapanis=True):
                fark += 1
    if fark:
        hata.append(f"3) vektörel referans bloğu skaler tanımdan {fark} yerde farklı")
    # çok satırlı vektörel etiket (v2_etiket_toplu) tek satırlı v2_etiket ile aynı (kopukluk ve veri sonu dahil)
    rng = np.random.default_rng(12); nn = 700; trr = rng.lognormal(0, 0.7, nn); gvr = trr * rng.uniform(0, 1, nn); crr = 100 * np.exp(np.cumsum(rng.normal(0, 0.02, nn)))
    kz = np.zeros(nn, bool); kz[[333, 640]] = True; tsx = rng.integers(20, nn - 1, 400); bsx = tsx - rng.integers(9, 90, 400)
    Yt = V.v2_etiket_toplu(tsx, bsx, crr, trr, gvr, kz); fark = 0
    for i in range(400):
        y1 = V.v2_etiket(int(tsx[i]), int(bsx[i]), crr, trr, gvr, kz)
        for k in ("y5", "y10", "y20", "g", "e", "yon"):
            a_, b_ = y1[k], Yt[k][i]
            if not ((isinstance(a_, float) and np.isnan(a_) and np.isnan(b_)) or a_ == b_):
                fark += 1
    if fark or np.nansum(Yt["y20"]) == 0:
        hata.append(f"3) toplu etiket tekli etiketten {fark} yerde farklı (ya da hiç olay yok)")
    Ytk = V.v2_etiket_toplu(tsx[:50], bsx[:50], crr, trr, gvr, kz, kapanis=True)
    if any(V.v2_etiket(int(tsx[i]), int(bsx[i]), crr, trr, gvr, kz, kapanis=True)["g"] != Ytk["g"][i] for i in range(50)):
        hata.append("3) toplu etiket kapanış kipinde farklı")
    if not all(np.allclose(np.asarray(V.v2_onkosul_dizi(crr)[j][150:400], float), [V.v2_onkosul(crr, b)[j] for b in range(150, 400)], equal_nan=True) for j in range(4)):
        hata.append("3) vektörel ön koşul skaler ön koşuldan farklı")
    # geçerli karar günü (D1a): son 3 günün her biri <= 2 x medyan
    trg = np.full(60, 1.0)
    if not V.v2_gecerli(40, 10, trg, np.full(60, 100.0)):
        hata.append("3) sakin günde geçerlilik")
    trg2 = trg.copy(); trg2[39] = 2.01
    if V.v2_gecerli(40, 10, trg2, np.full(60, 100.0)) or not V.v2_gecerli(42, 10, trg2, np.full(60, 100.0)):
        hata.append("3) D1a: son 3 günde büyük aralık kuralı")
    if V.v2_gecerli(11, 10, trg, np.full(60, 100.0)):
        hata.append("3) bas'tan önceki barlar geçerlilikte kullanıldı")

    # ---------------------------------------------------------------- 4) bölge motoru elle
    n = 80; kop = np.zeros(n, bool); dur = np.zeros(n, bool); dur[20:41] = True; tr5, gv5, c5 = bolge_sabit(n, (0, n))
    B = V.v2_bolgeler(dur, kop, tr5, gv5, c5, 1)
    if B.tolist() != [[20 - L + 1, 20, 45, V.BIT_SONME]]:
        hata.append(f"4) SÖNME elle: {B.tolist()}")
    tr6 = tr5.copy(); gv6 = gv5.copy(); tr6[30] = 2.0; gv6[30] = 1.0
    B6 = V.v2_bolgeler(dur, kop, tr6, gv6, c5, 1)
    if B6[0].tolist() != [11, 20, 30, V.BIT_BUYUK]:
        hata.append(f"4) BÜYÜK MUM bitişi elle: {B6.tolist()}")
    if len(B6) > 1 and B6[1, 1] < 30 + L:
        hata.append(f"4) yeni bölge önceki bitişten L gün içinde açıldı: {B6.tolist()}")
    dv = np.zeros(n, bool); dv[20:61] = True
    B7 = V.v2_bolgeler(dur, kop, tr5, gv5, c5, 1, devam=dv)
    if B7[0].tolist() != [11, 20, 65, V.BIT_SONME]:
        hata.append(f"4) devam durumu ile SÖNME: {B7.tolist()}")
    k8 = kop.copy(); k8[35] = True
    B8 = V.v2_bolgeler(dur, k8, tr5, gv5, c5, 1)
    if B8[0].tolist() != [11, 20, 34, V.BIT_SANSUR]:
        hata.append(f"4) kopukluk SANSÜR: {B8.tolist()}")
    dur9 = np.zeros(n, bool); dur9[70:] = True
    if V.v2_bolgeler(dur9, kop, tr5, gv5, c5, 1).tolist() != [[61, 70, 79, V.BIT_SANSUR]]:
        hata.append("4) veri sonu SANSÜR")
    B10 = V.v2_bolgeler(dur, kop, tr5, gv5, c5, 10)
    if B10.tolist() != [[20, 29, 45, V.BIT_SONME]]:
        hata.append(f"4) v1 T kuralı (10 gün kesintisiz): {B10.tolist()}")

    # ---------------------------------------------------------------- 5) geleceğe bakmama
    d5 = rastgele_bar(900, 3); t5 = 700; Oa = V.v2_olculer(d5); bozuk = d5.copy()
    rng = np.random.default_rng(9); bozuk.iloc[t5 + 1:, :4] = bozuk.iloc[t5 + 1:, :4].to_numpy() * rng.uniform(0.3, 3.0, (len(bozuk) - t5 - 1, 1))
    bozuk.iloc[t5 + 1:, 4] = 1.0; bozuk["h"] = bozuk[["o", "h", "c"]].max(axis=1); bozuk["l"] = bozuk[["o", "l", "c"]].min(axis=1)
    Ob = V.v2_olculer(bozuk)
    for k in ("m_aralik_atr", "b_kapanis_bant", "b_egim_tepe", "ema200", "atr_ref", "natr_oran", "rv_yuzde", "hacim_oran"):
        if not np.allclose(Oa[k][: t5 + 1], Ob[k][: t5 + 1], equal_nan=True):
            hata.append(f"5) {k} t sonrası barlardan etkilendi")
    for k in Oa["durum"]:
        if not np.array_equal(Oa["durum"][k][: t5 + 1], Ob["durum"][k][: t5 + 1]):
            hata.append(f"5) durum {k} t sonrası barlardan etkilendi")
    ctx = {"rj_pazar": np.zeros(900), "rj_sektor": np.zeros(900), "p_pazar_ret60": np.zeros(900), "p_pazar_ret20": np.zeros(900),
           "p_sektor_ret20": np.zeros(900), "natr_d": np.zeros(900), "mom_t": np.zeros(900), "liq_t": np.zeros(900), "p_lr": np.zeros(900),
           "bilanco_tarih": d5.index[[300, 500, 690, 780]].to_numpy("datetime64[D]"), "bilanco_bilgi_i": np.array([300, 500, 690, 780]),
           "B_bilgi_i": np.array([400, 697, 760]), "B_g0_i": np.array([400, 697, 760]), "makro_g0_i": np.array([705, 820]), "gun": d5.index.to_numpy("datetime64[D]")}

    def A_(dx, Ox):
        return {"Ol": Ox, "o": dx.o.to_numpy(), "h": dx.h.to_numpy(), "l": dx.l.to_numpy(), "c": dx.c.to_numpy(), "v": dx.v.to_numpy(), "gun": dx.index,
                "n": len(dx), "pazar": "BIST", "E1": V._v2_e1()}
    once = np.array([[100, 109, 140, V.BIT_BUYUK, 1], [200, 209, 230, V.BIT_SONME, -1], [400, 409, 450, V.BIT_BUYUK, 0]], np.int64)
    fa = V.v2_ozellik(t5, t5 - 29, A_(d5, Oa), ctx, once); fb = V.v2_ozellik(t5, t5 - 29, A_(bozuk, Ob), ctx, once)
    fark = [k for k in fa if not (fa[k] == fb[k] or (isinstance(fa[k], float) and np.isnan(fa[k]) and np.isnan(fb[k])))]
    if fark:
        hata.append(f"5) özellikler t sonrası barlardan etkilendi: {fark}")
    if V.v2_gecerli(t5, t5 - 29, Oa["tr"], d5.c.to_numpy()) != V.v2_gecerli(t5, t5 - 29, Ob["tr"], bozuk.c.to_numpy()):
        hata.append("5) geçerlilik t sonrası barlardan etkilendi")
    if fa["o_makro_10"] != 1.0 or fa["o_olay_son5"] != 1.0 or fa["o_bilanco_bolgede"] != 1.0:
        hata.append(f"5) olay özellikleri bilgi kuralı: {fa['o_makro_10']}, {fa['o_olay_son5']}, {fa['o_bilanco_bolgede']}")
    if not (fa["hs_yetersiz"] == 0 and np.isclose(fa["hs_bh_pay"], 1 / 3) and np.isclose(fa["hs_oran"], 30 / np.median([41, 31, 51]))):
        hata.append(f"5) hisse geçmişi özelliği elle: {fa['hs_oran']}, {fa['hs_bh_pay']}")
    # bölge açılışları t'ye kadar aynı (bitişi t'den sonra olan bölgenin açılışı da)
    Ba = V.v2_bolgeler(Oa["durum"]["G5"], Oa["kopuk"], Oa["tr"], Oa["govde"], d5.c.to_numpy(), 1, devam=Oa["durum"]["G12"])
    Bb = V.v2_bolgeler(Ob["durum"]["G5"], Ob["kopuk"], Ob["tr"], Ob["govde"], bozuk.c.to_numpy(), 1, devam=Ob["durum"]["G12"])
    ia, ib = Ba[Ba[:, 2] <= t5], Bb[Bb[:, 2] <= t5]
    if not np.array_equal(ia, ib) or not np.array_equal(Ba[Ba[:, 1] <= t5][:, :2], Bb[Bb[:, 1] <= t5][:, :2]):
        hata.append("5) t'ye kadar biten / açılan bölgeler t sonrası barlardan etkilendi")

    # ---------------------------------------------------------------- 6) BHU elle
    trh, gvh, ch = bolge_sabit(200, (0, 200)); trh[:] = 1.0; gvh[:] = 0.5; trh[120] = 3.0; gvh[120] = 2.0; ch[121:] = 110.0; trh[130] = 3.0; gvh[130] = 2.0
    BH = V.v2_bhu(ch, trh, gvh, np.zeros(200, bool))
    if BH.g.tolist() != [120] or BH.yon.tolist() != [1] or BH.e.tolist() != [121]:
        hata.append(f"6) BHU elle (ve 20 bar tekilleştirme): {BH.to_dict('records')}")

    # ---------------------------------------------------------------- 7) walk-forward sızıntısı
    rng = np.random.default_rng(5); N = 3000; tar = pd.to_datetime("2016-01-01") + pd.to_timedelta(rng.integers(0, 365 * 8, N), unit="D")
    Dw = pd.DataFrame({"tarih": tar, "x1": rng.normal(size=N), "x2": rng.normal(size=N), "yas_kova": rng.integers(0, 3, N), "ay": tar.month,
                       "sembol": rng.choice(list("ABCDEFGH"), N)}).rename_axis("satir")
    Dw["y10"] = (rng.random(N) < V1.vdyt_sigmoid(Dw.x1.to_numpy())).astype(float); Dw["son10"] = Dw.tarih + pd.Timedelta(days=30)
    Pw, kay, _k = V.v2_wf(Dw, "y10", "son10", {"M": ["x1", "x2"]}, {"T1": ["yas_kova", "ay"]}, [2021, 2022], "2023-12-31", kucuk_E())
    for k_ in kay:
        if k_["egitim_son_max"] and pd.Timestamp(k_["egitim_son_max"]) >= pd.Timestamp(f"{k_['yil']}-01-01"):
            hata.append(f"7) {k_['yil']} eğitiminde etiketi test yılına taşan satır var")
    Dw2 = Dw.copy(); m22 = Dw2.tarih.dt.year == 2022; Dw2.loc[m22, "y10"] = 1.0 - Dw2.loc[m22, "y10"]; Dw2.loc[m22, "x2"] = 99.0 * Dw2.loc[m22, "x2"]
    Pw2, _k2, _ = V.v2_wf(Dw2, "y10", "son10", {"M": ["x1", "x2"]}, {"T1": ["yas_kova", "ay"]}, [2021], "2023-12-31", kucuk_E())
    a1 = Pw[Pw.yil == 2021].sort_values("satir"); a2 = Pw2.sort_values("satir")
    if not (np.allclose(a1.p_M, a2.p_M) and np.allclose(a1.q80_M, a2.q80_M) and np.allclose(a1.p_T1, a2.p_T1)):
        hata.append("7) gelecek yılın etiket / özellik değişimi geçmiş yılın tahminini / eşiğini değiştirdi")
    Dw3 = Dw.copy(); m21 = Dw3.tarih.dt.year == 2021; Dw3.loc[m21, "y10"] = 1.0 - Dw3.loc[m21, "y10"]
    Pw3, _k3, _ = V.v2_wf(Dw3, "y10", "son10", {"M": ["x1", "x2"]}, {}, [2021], "2023-12-31", kucuk_E())
    if not np.allclose(Pw3.sort_values("satir").p_M, a1.p_M) or not np.allclose(Pw3.q80_M.iloc[0], a1.q80_M.iloc[0]):
        hata.append("7) test yılının kendi etiketi tahmini / eşiği değiştirdi (eşik test verisine bağlı)")
    tr21 = Dw[(Dw.son10 < pd.Timestamp("2021-01-01")) & Dw.y10.notna()]
    Xa, _xb = V1.vdyt_standart(tr21[["x1", "x2"]].to_numpy(float), tr21[["x1", "x2"]].to_numpy(float)[:1], (0.01, 0.99))
    bb = V1.vdyt_lojistik(Xa, tr21.y10.to_numpy(float), 1.0, 25, 1e-8)
    if not np.isclose(a1.q80_M.iloc[0], np.quantile(V1.vdyt_sigmoid(np.column_stack([np.ones(len(Xa)), Xa]) @ bb), 0.8)):
        hata.append("7) q80 eğitim tahminlerinin %80'i değil")

    # ---------------------------------------------------------------- 8-13) uçtan uca sentetik (kontroller, karşılaştırmalar, sınıf, grafik, kapılar)
    yedek = dict(V1.VDYT_YOL); yedek2 = dict(V.VDYT2_YOL)
    with tempfile.TemporaryDirectory() as td:
        try:
            for k_ in V1.VDYT_YOL:
                if k_ not in ("cikti",):
                    V1.VDYT_YOL[k_] = os.path.join(td, "yok_" + k_)
            V1.VDYT_YOL["ara"] = os.path.join(td, "ara1"); V.VDYT2_YOL["ara"] = os.path.join(td, "ara2"); V.VDYT2_YOL["k67_takvim"] = os.path.join(td, "yok_k67")
            V1.VDYT_YOL["sektor_bist"] = os.path.join(td, "sektor.csv")
            pd.DataFrame({"sembol": [f"S{j:02d}" for j in range(12)], "sektor": ["A"] * 6 + ["B"] * 6}).to_csv(V1.VDYT_YOL["sektor_bist"], index=False)
            Fs, Evs = sentetik_pazar(); Es = kucuk_E(); cik = os.path.join(td, "cikti")
            # 8) kontrol satırları (kos kipi tek hisse)
            Z = V.v2_pazar_isle("BIST", "kos", 1, Fs, Evs, Es)
            if Z["hata"]:
                hata.append(f"8) hisse işleminde hata: {list(Z['hata'].items())[:3]}")
            h0 = next(x for x in Z["R"] if x["sembol"] == "S02"); T = h0["bolge"]["G5"]; K = h0["kontrol"]["G5"]; S_ = h0["satir"]["G5"]
            d0 = Fs["S"]["S02"]; icinde = np.zeros(len(d0), bool)
            for r in T.itertuples():
                icinde[r.bas: r.bit + 1] = True
            Kd = K[K.kaynak == "DISARI"]; Kr = K[K.kaynak == "RASTGELE"]
            if not len(S_) or not len(Kd) or not len(Kr):
                hata.append(f"8) gerçek / kontrol satırı yok: {len(S_)}, {len(Kd)}, {len(Kr)}")
            else:
                if icinde[Kd.t.to_numpy()].any():
                    hata.append("8) DIŞARI kontrol günü bir sessiz bölgenin içinde")
                gh = set(zip(S_.tarih.dt.year, S_.natr_d)); kh = set(zip(Kd.tarih.dt.year, Kd.natr_d))
                if not kh <= gh:
                    hata.append("8) DIŞARI kontrol günü gerçek satırlarla aynı (yıl, NATR ondalığı) hücresinde değil")
                if not set(Kd.yas) <= set(S_.yas):
                    hata.append("8) DIŞARI sözde yaşları gerçek yaşlardan çekilmedi")
                Ol0 = V.v2_olculer(d0)
                for r in pd.concat([S_, Kd, Kr]).head(60).itertuples():
                    if not V.v2_gecerli(int(r.t), int(r.bas), Ol0["tr"], d0.c.to_numpy()):
                        hata.append("8) geçersiz (D1a) satır üretildi"); break
                    Ye = V.v2_etiket(int(r.t), int(r.bas), d0.c.to_numpy(), Ol0["tr"], Ol0["govde"], Ol0["kopuk"])
                    if not all((np.isnan(Ye[f"y{hh}"]) and np.isnan(getattr(r, f"y{hh}"))) or Ye[f"y{hh}"] == getattr(r, f"y{hh}") for hh in (5, 10, 20)):
                        hata.append("8) kontrol / gerçek satır etiketi aynı fonksiyonla değil"); break
                    if r.g >= 0 and r.g <= r.t:
                        hata.append("8) etiket t gününde ya da önce başlayan hareketi saydı"); break
                if not set(Kr.yas) <= set(Es["karar_yas"]):
                    hata.append("8) RASTGELE satırları karar yaşlarında değil")
                rs = (Kr.t - Kr.bas + 1); su = set(T[T.uygun_tespit].sure)
                if (rs > max(su)).any():
                    hata.append("8) RASTGELE bölge süresi gerçek süre dağılımının dışında")
                if not set(T.tespit - T.bas) == {L - 1}:
                    hata.append("8) bas = tespit - L + 1 tutmadı")
                if not (S_.tarih.values == d0.index[S_.t.to_numpy()].values).all():
                    hata.append("8) satır tarihi")
            # 9) oran karşılaştırması ve D1b elle
            Dg = pd.DataFrame({"sembol": ["a", "a", "b", "b"], "y": [1.0, 0.0, 1.0, 1.0], "s": [1, 1, 2, 2]})
            Dk = pd.DataFrame({"sembol": ["a", "a", "a", "b"], "y": [0.0, 0.0, 1.0, 0.0], "s": [1, 1, 1, 2]})
            r9 = V.v2_oran_karsilastir(Dg, Dk, "y", ["s"], Es)
            if not (np.isclose(r9["ort1"], 0.75) and np.isclose(r9["ort0"], (1 / 3 * 2 + 0 * 2) / 4)):
                hata.append(f"9) tabakalı oran karşılaştırması elle: {r9}")
            Pa = pd.DataFrame({"satir": np.arange(40), "p_M": np.r_[np.full(20, 0.8), np.full(20, 0.2)], "p_T": 0.5})
            Da = pd.DataFrame({"y": np.r_[np.ones(20), np.zeros(20)], "sembol": np.tile(list("abcd"), 10)})
            Pb = pd.DataFrame({"satir": np.arange(40), "p_M": 0.5, "p_T": 0.5}); f9 = V.v2_skill_fark(Pa, Da, Pb, Da, "y", "M", "T", Es)
            if not (np.isclose(f9["skill_a"], 1 - 0.04 / 0.25) and np.isclose(f9["skill_b"], 0.0) and np.isclose(f9["fark"], 0.84)):
                hata.append(f"9) D1b skill farkı elle: {f9}")
            # 10) sınıf kuralları
            s_ = V.v2_sinif
            beklenen = [((False, True, 0, True, .9, .5, .9, True, True), "Genişleme başladı"), ((False, False, 2, True, .9, .5, .9, True, True), "Sıkışma oluşuyor"),
                        ((False, False, 1, True, .9, .5, .9, True, True), "Sıkışma yok"), ((True, False, 3, True, .4, .5, .9, True, True), "Sıkışma devam ediyor"),
                        ((True, False, 3, False, .9, .5, .9, True, True), "Sıkışma devam ediyor"), ((True, False, 3, True, .9, .5, .9, False, True), "Sıkışma devam ediyor"),
                        ((True, False, 3, True, .9, .5, .9, True, False), "Yön belirsiz"), ((True, False, 3, True, .9, .5, .6, True, True), "Yukarı kırılma adayı"),
                        ((True, False, 3, True, .9, .5, .4, True, True), "Aşağı kırılma adayı"), ((True, False, 3, True, .9, .5, .5, True, True), "Genişlemeye yaklaşan sıkışma")]
            for a, b in beklenen:
                if s_(*a) != b:
                    hata.append(f"10) sınıf kuralı {a} -> {s_(*a)} (beklenen {b})")
            if V.v2_guven(True, 0.02, 0.06, 0.03, 0.05) != "YÜKSEK" or V.v2_guven(True, 0.05, 0.06, 0.03, 0.05) != "ORTA" or V.v2_guven(False, 0.0, 1, 0.03, 0.05) != "DÜŞÜK":
                hata.append("10) güvenilirlik düzeyleri")
            if set(E["sinif"]["siniflar"]) != {"Sıkışma yok", "Sıkışma oluşuyor", "Sıkışma devam ediyor", "Genişlemeye yaklaşan sıkışma", "Yukarı kırılma adayı",
                                                "Aşağı kırılma adayı", "Yön belirsiz", "Genişleme başladı"}:
                hata.append("10) sınıf listesi")
            # 13) uçtan uca: kapsam yalnız sayar
            Kp = V.v2_kapsam(["BIST"], cik, 1, girdi={"BIST": (Fs, Evs)}, E=Es); js = json.dumps(Kp, ensure_ascii=False, default=str)
            o_ = Kp["pazar"]["BIST"]
            if o_["bolge"]["G5"]["bolge_uygun"] <= 0 or o_["karar"]["G5"]["toplam"] <= 0 or o_["kontrol"]["G5"]["DISARI"]["toplam"] <= 0:
                hata.append("13) kapsam bölge / karar / kontrol saymadı")
            if any(x in js for x in ("\"y10\"", "\"y20\"", "\"r20\"", "yukari", "brier", "oran\"", "\"yon\"", "sure_ort", "SONME", "BUYUK_MUM", "onay")):
                hata.append("13) kapsam etiket / getiri / oran / bitiş bilgisi içeriyor")
            V.v2_onkayit(cik, veri_sha={})
            S1 = V.v2_kos("wf", cik, 1, git_sart=False, veri_sart=False, pazarlar=["BIST"], girdi={"BIST": (Fs, Evs)}, p1_tekrar=1, E=Es)
            P = S1["pazar"]["BIST"]; ara = os.path.join(cik, "_ara")
            if "durum" in P or not P.get("basari1") or not P.get("basari2") or not P.get("basari3") or not P.get("hipotez") or not P.get("d1b"):
                hata.append(f"13) kos wf çıktısı eksik: {P.get('durum')} {[k for k in ('basari1', 'basari2', 'basari3', 'd1b') if not P.get(k)]}")
            if any(r["b1"] != "KASA AÇILMADI" for r in S1["karar"]):
                hata.append("13) wf aşamasında karar 'KASA AÇILMADI' olmalı")
            if not any(r.get("tanim") == "G5" and r.get("onkosul") == "P1" and r.get("kontrol") == "DISARI" and r.get("ana") for r in P.get("basari1", [])):
                hata.append("13) başarı (1) ana hücresi yok")
            Pm = pd.read_csv(os.path.join(ara, "wf", "tahmin_m1_BIST_G5_y10.csv.gz"), parse_dates=["tarih"])
            if (Pm.tarih >= pd.Timestamp("2024-01-01")).any():
                hata.append("13) wf aşamasında KASA dönemi test satırı var")
            Sd = pd.read_csv(os.path.join(ara, "wf", "satir_BIST_G5.csv.gz"), parse_dates=["tarih", "son10"]).set_index("satir")
            if (Sd.loc[Pm.satir].son10 > pd.Timestamp("2023-12-31")).any():
                hata.append("13) wf test satırının etiketi 2023 sonunu aşıyor")
            if (Pm.q80_M_TAM.groupby(Pm.yil).nunique() > 1).any():
                hata.append("13) q80 eşiği test yılı içinde satıra göre değişiyor (eğitimden tek değer olmalı)")
            for f in ("VDYT2_RAPOR_wf.md", "VDYT2_HATA_wf.md", "vdyt2_parametre_kaydi.json", "vdyt2_meta.json", "vdyt2_sonuc_wf.json"):
                if not os.path.exists(os.path.join(cik, f)):
                    hata.append(f"13) {f} yazılmadı")
            durmali(lambda: V.v2_canli(cik, 1, git_sart=False, veri_sart=False, girdi={"BIST": (Fs, Evs)}, pazarlar=["BIST"], E=Es),
                    "12) KASA'sız canlı çıktı üretildi", hata, "KASA")
            S2 = V.v2_kos("kasa", cik, 1, git_sart=False, veri_sart=False, pazarlar=["BIST"], girdi={"BIST": (Fs, Evs)}, p1_tekrar=1, E=Es)
            kb_ = S2["karar"][0]
            if kb_["b1"] == "KASA AÇILMADI" or not os.path.exists(os.path.join(cik, "vdyt2_kasa_acildi.json")) or \
                    not all(k in kb_ for k in ("b1", "b2a", "b2b", "b2", "b3")):
                hata.append(f"13) KASA karar tablosu: {kb_}")
            for r in S2["karar"]:
                if r["b2"] == "BAŞARILI" and not (r["b2a"] == "BAŞARILI" and r["b2b"] == "BAŞARILI"):
                    hata.append("13) (2) yalnız (2a) VE (2b) ile BAŞARILI olmalı")
            Pk = pd.read_csv(os.path.join(ara, "kasa", "tahmin_m1_BIST_G5_y10.csv.gz"), parse_dates=["tarih"])
            if (Pk.tarih < pd.Timestamp("2024-01-01")).any():
                hata.append("13) KASA aşamasında 2024 öncesi test satırı var")
            durmali(lambda: V.v2_kos("kasa", cik, 1, git_sart=False, veri_sart=False, pazarlar=["BIST"], girdi={"BIST": (Fs, Evs)}, E=Es),
                    "12) KASA ikinci kez açıldı", hata, "zaten")
            yc = V.v2_canli(cik, 1, git_sart=False, veri_sart=False, girdi={"BIST": (Fs, Evs)}, pazarlar=["BIST"], E=Es)
            C = pd.read_csv(yc)
            if not len(C) or not set(C.sinif) <= set(E["sinif"]["siniflar"]) or not (C.etiket == "CANLI, test dışı").all():
                hata.append(f"13) canlı tablo: {C.sinif.value_counts().to_dict() if len(C) else 'boş'}")
            for k_ in ("bolge_var", "baslangic", "sure_gun", "sikisma_gucu", "savunma_hatti", "p5", "p10", "p20", "zaman_araligi", "p_yukari_kosullu",
                       "p_asagi_kosullu", "guvenilirlik", "dayanaklar", "sinif", "kod_sha256"):
                if k_ not in C:
                    hata.append(f"13) canlı tabloda {k_} yok")
            yon_ok = {r["onkosul"]: r["b3"] == "BAŞARILI" for r in S2["karar"] if r["pazar"] == "BIST"}
            if not all(yon_ok.get(r.onkosul if isinstance(r.onkosul, str) else "P0", False) for r in C[C.sinif.isin(["Yukarı kırılma adayı", "Aşağı kırılma adayı"])].itertuples()):
                hata.append("13) yön motoru geçmeden yön adayı sınıfı verildi")
            durmali(lambda: V.v2_canli(cik, 1, git_sart=False, veri_sart=False, girdi={"BIST": (Fs, Evs)}, pazarlar=["BIST"], E=Es),
                    "13) canlı tablo üzerine yazıldı", hata, "üzerine yazılmaz")
            # 11) grafik paketi + TESPİT GÜNÜ öğeleri + ciz
            yp = V.v2_paket("kasa", cik, ["BIST"], F_ver={"BIST": Fs}, ara=os.path.join(ara, "kasa"), E=Es)
            if not yp or any(os.path.getsize(x) > 3e6 for x in yp):
                hata.append("11) paket yazılmadı ya da 3 MB'ı aşıyor")
            else:
                J = json.load(open([x for x in yp if x.endswith(".json")][0], encoding="utf-8")); Bp = pd.read_csv([x for x in yp if x.endswith(".csv.gz")][0], parse_dates=["tarih"])
                if not {m["grup"] for m in J["ornek"]} >= {"BASARILI", "YON_DOGRU"}:
                    hata.append(f"11) paket grupları: {sorted({m['grup'] for m in J['ornek']})}")
                for m in J["ornek"]:
                    og = V.v2_grafik_ogeler(m, Bp[Bp.ornek == m["ornek"]], True)
                    xs = [og["bar"].i.max(), og["bolge"][1]] + [x for _a, x in og["vcizgi"]] + ([og["hat"][1]] if og["hat"] else [])
                    if max(xs) > m["t"] or og["metin"] or any(a == "büyük hareket başlangıcı" for a, _x in og["vcizgi"]) or m["grup"] in og["baslik"] or "sonuç" in og["baslik"]:
                        hata.append(f"11) TESPİT GÜNÜ grafiğinde gelecek öğe / sonuç: {m['ornek']}"); break
                    if m["g"] >= 0 and not any(a == "büyük hareket başlangıcı" for a, _x in V.v2_grafik_ogeler(m, Bp[Bp.ornek == m["ornek"]], False)["vcizgi"]):
                        hata.append("11) tam grafikte büyük hareket başlangıcı yok"); break
                try:
                    import matplotlib  # noqa: F401
                    gk = os.path.join(td, "png"); y1 = V.v2_ciz(os.path.dirname(yp[0]), gk)
                    if not y1 or not any(x.endswith("_tespit.png") for x in y1):
                        hata.append("11) ciz PNG yazmadı")
                    t0 = {x: os.path.getmtime(x) for x in y1}; y2 = V.v2_ciz(os.path.dirname(yp[0]), gk)
                    if y2 or any(os.path.getmtime(x) != t0[x] for x in y1):
                        hata.append("11) ciz var olan PNG'nin üstüne yazdı")
                except ImportError:
                    print("not: matplotlib yok, çizim testi atlandı")
            # K62 yolu (yalnız kapanış) uçtan uca
            Fk = {"S": {k_: d_.assign(o=d_.c, h=d_.c, l=d_.c) for k_, d_ in Fs["S"].items()}, "meta": Fs["meta"], "kaynak": "sentetik K62"}
            cik2 = os.path.join(td, "cikti_k62"); V.v2_onkayit(cik2, kapsam={}, veri_sha={})
            S3 = V.v2_kos("wf", cik2, 1, git_sart=False, veri_sart=False, pazarlar=["BIST_K62"], girdi={"BIST_K62": (Fk, Evs.iloc[:0])}, p1_tekrar=0, E=Es)
            P3 = S3["pazar"]["BIST_K62"]
            if "durum" in P3 or not any(r.get("tanim") == "G2K" for r in P3.get("basari1", [])):
                hata.append(f"13) BIST_K62 uçtan uca: {P3.get('durum')}")
            # beklenmeyen hata pazarı 'HATA' diye kaydeder; bütün hisseler hatalıysa analiz durur
            cik3 = os.path.join(td, "cikti_hata"); V.v2_onkayit(cik3, kapsam={}, veri_sha={})
            S4 = V.v2_kos("wf", cik3, 1, git_sart=False, veri_sart=False, pazarlar=["BIST_K62"], girdi={"BIST_K62": ({"S": None, "meta": {}}, Evs)}, E=Es)
            if not str(S4["pazar"]["BIST_K62"].get("durum", "")).startswith("HATA"):
                hata.append(f"13) beklenmeyen hata pazar kaydı: {S4['pazar']['BIST_K62']}")
            durmali(lambda: V.v2_analiz({"pazar": "X", "R": [], "hata": {"A": "x"}}, "wf", Es), "13) bütün hisseler hatalıyken analiz durmadı", hata, "bütün hisseler")
        finally:
            V1.VDYT_YOL.clear(); V1.VDYT_YOL.update(yedek); V.VDYT2_YOL.clear(); V.VDYT2_YOL.update(yedek2)

    # ---------------------------------------------------------------- 12) mühür, ön kayıt, ret kapısı, KASA kapısı
    E2 = copy.deepcopy(E0); E2["buyuk"]["k_b"] = 2.6
    if V.v2_esik_sha(E2) == V.v2_esik_sha():
        hata.append("12) eşik değişince mühür değişmedi")
    with tempfile.TemporaryDirectory() as td:
        y = V.v2_onkayit(td, kapsam={}, veri_sha={"x": ("a" * 64, 1)}); m_ = open(y, encoding="utf-8").read()
        for zorunlu in ("ESIK_SHA256: " + V.v2_esik_sha(), "KOD_SHA256: " + V.v2_kod_sha(), "VDYT_KOD_SHA256: " + V.v2_v1_kod_sha(), "SAPMA / BOŞLUK",
                        "ÜÇ BAŞARI", "Yanlılık beyanı", "Kapsam", "walk-forward".upper()[:4], "D1", "D2", "D3", "D4", "D5", "TESPİT GÜNÜ", "q_yüksek"):
            if zorunlu not in m_:
                hata.append(f"12) ön kayıtta '{zorunlu}' yok")
        if V.v2_onkayit(td, kapsam={}) != y:
            hata.append("12) aynı mühürle ikinci yazım yolu döndürmedi")
        oc = V.v2_onkayit_dogrula(td, veri=False, git=False)
        if oc["esik"] != V.v2_esik_sha():
            hata.append("12) doğrulama mühür")
        durmali(lambda: V.v2_onkayit_dogrula(td, veri=True, git=False), "12) farklı veri sha256'sı kabul edildi", hata, "veri")
        open(y, "w", encoding="utf-8").write(m_.replace("KOD_SHA256: " + V.v2_kod_sha(), "KOD_SHA256: " + "0" * 64, 1))
        durmali(lambda: V.v2_onkayit_dogrula(td, veri=False, git=False), "12) farklı VDYT2.py sha256 ile doğrulama geçti", hata, "VDYT2.py")
        open(y, "w", encoding="utf-8").write(m_.replace("VDYT_KOD_SHA256: " + V.v2_v1_kod_sha(), "VDYT_KOD_SHA256: " + "0" * 64))
        durmali(lambda: V.v2_onkayit_dogrula(td, veri=False, git=False), "12) farklı VDYT.py sha256 ile doğrulama geçti", hata, "VDYT.py")
        open(y, "w", encoding="utf-8").write(m_.replace(V.v2_esik_sha(), "1" * 64))
        durmali(lambda: V.v2_onkayit_dogrula(td, veri=False, git=False), "12) bozuk mühürle doğrulama geçti", hata, "mühr")
        durmali(lambda: V.v2_onkayit(td), "12) farklı mühürlü ön kaydın üzerine yazıldı", hata, "üzerine yazılmadı")
    with tempfile.TemporaryDirectory() as td:
        durmali(lambda: V.v2_onkayit_dogrula(td, veri=False, git=False), "12) ön kayıt yokken doğrulama geçti", hata, "ön kayıt yok")
        durmali(lambda: V.v2_kos("wf", td, 1, git_sart=False, veri_sart=False, pazarlar=[]), "12) ön kayıtsız kos çalıştı", hata, "REDDEDİLDİ")
        git(td, "init", "-q"); y = V.v2_onkayit(td, kapsam={}, veri_sha={})
        durmali(lambda: V.v2_onkayit_dogrula(td, veri=False, git=True), "12) git'e işlenmemiş ön kayıt kabul edildi", hata, "ön kaydı")
        durmali(lambda: V.v2_kos("wf", td, 1, git_sart=True, veri_sart=False, pazarlar=[]), "12) işlenmemiş ön kayıtla kos çalıştı", hata, "REDDEDİLDİ")
        git(td, "add", V.VDYT2_DOSYA["onkayit"]); git(td, "commit", "-q", "-m", "on kayit")
        if V.v2_git_islenmis(y, "ön kayıt")["commit"] != git(td, "rev-parse", "HEAD").strip():
            hata.append("12) git commit kimliği")
        temiz = lambda f: subprocess.run(["git", "-C", KOK, "status", "--porcelain", "--", f], capture_output=True, text=True).stdout.strip() == "" and \
            subprocess.run(["git", "-C", KOK, "log", "-1", "--", f], capture_output=True, text=True).stdout.strip() != ""   # noqa: E731
        if not temiz("VDYT2.py"):
            durmali(lambda: V.v2_onkayit_dogrula(td, veri=False, git=True), "12) git'e işlenmemiş VDYT2.py ile doğrulama geçti", hata, "VDYT2.py")
        open(y, "a", encoding="utf-8").write("\nsonradan eklenen satır\n")
        durmali(lambda: V.v2_git_islenmis(y, "ön kayıt"), "12) işlendikten sonra değişen ön kayıt kabul edildi", hata, "değişmiş")
    with tempfile.TemporaryDirectory() as td:
        V.v2_onkayit(td, kapsam={}, veri_sha={})
        durmali(lambda: V.v2_kos("kasa", td, 1, git_sart=False, veri_sart=False, pazarlar=[]), "12) wf olmadan KASA açıldı", hata, "KASA")
        V._v2_json(V._v2_yol("vdyt2_sonuc_wf.json", td), {"pazar": {}}); V._v2_json(V._v2_yol("kasa", td), {"acilis": "önce"})
        durmali(lambda: V.v2_kos("kasa", td, 1, git_sart=False, veri_sart=False, pazarlar=[]), "12) KASA ikinci kez açıldı", hata, "zaten")

    # ---------------------------------------------------------------- 14) Yahoo takvim ayrıştırıcı
    html = (b"<table><thead><tr><th>Symbol</th><th>Company</th><th>Earnings Date</th><th>EPS Estimate</th></tr></thead><tbody>"
            b"<tr><td>AAA</td><td>x</td><td>Feb 3, 2022 at 4 PM EST</td><td>1</td></tr><tr><td>AAA</td><td>x</td><td>May 5, 2022 at 7 AM EDT</td><td>-</td></tr>"
            b"<tr><td>AAA</td><td>x</td><td>Aug 4, 2022 at 12 AM EDT</td><td>-</td></tr></tbody></table>")
    Ty = V.v2_yahoo_takvim_ayristir(html, "AAA")
    if Ty.saat.tolist() != [16, 7, 0] or Ty.tarih.dt.strftime("%Y-%m-%d").tolist() != ["2022-02-03", "2022-05-05", "2022-08-04"]:
        hata.append(f"14) Yahoo takvim ayrıştırma: {Ty.to_dict('records')}")
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "tk")); gzip.open(os.path.join(td, "tk", "AAA.html.gz"), "wb").write(html)
        yy = V.VDYT2_YOL["ara"]; V.VDYT2_YOL["ara"] = os.path.join(td, "ara")
        try:
            Yt, yn = V.v2_yahoo_takvim(os.path.join(td, "tk"))
            Fy = {"S": {"AAA": rastgele_bar(2000, 4, "2015-01-01"), "BBB": rastgele_bar(2000, 5, "2015-01-01")}, "meta": {}}
            Ev0 = pd.DataFrame([("ABD", "AAA", "ABD_BILANCO", "A", True, pd.Timestamp("2022-02-10"), pd.Timestamp("2022-02-10"), "EDGAR", ""),
                                ("ABD", "BBB", "ABD_BILANCO", "A", True, pd.Timestamp("2022-02-10"), pd.Timestamp("2022-02-10"), "EDGAR", "")], columns=V1.OLAY_SUTUN)
            ab = V1.vdyt_olaylar
            V1.vdyt_olaylar = lambda pz, F, E: (Ev0.copy(), {})
            try:
                Ev2, _n = V.v2_olaylar("ABD", Fy, False, yahoo=Yt)
            finally:
                V1.vdyt_olaylar = ab
            ba = Ev2[(Ev2.tur == "ABD_BILANCO") & (Ev2.sembol == "AAA")].g0_tarih.dt.strftime("%Y-%m-%d").tolist()
            if ba != ["2022-02-04", "2022-05-05", "2022-08-04"] or (Ev2[(Ev2.tur == "ABD_BILANCO") & (Ev2.sembol == "BBB")].kaynak != "EDGAR").any():
                hata.append(f"14) Yahoo birincil bilanço değişimi: {ba}")
        finally:
            V.VDYT2_YOL["ara"] = yy

    # ---------------------------------------------------------------- 15) çakışma kapısı
    kaynak = open(os.path.join(KOK, "VDYT2.py"), encoding="utf-8").read()
    ns = {"__name__": "vdyt2_test", "__file__": os.path.join(KOK, "VDYT2.py"), "v2_esik_sha": "başka dosyanın adı", "_CK_KAYIT": {"v2_esik_sha": "BASKA.py"}}
    try:
        exec(compile(kaynak, "VDYT2.py", "exec"), ns); hata.append("15) başka dosyanın adını ezen yükleme durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"15) çakışma kapısı yanlış nedenle durdu: {ex}")
    ns2 = {"__name__": "vdyt2_test", "__file__": os.path.join(KOK, "VDYT2.py")}
    exec(compile(kaynak, "VDYT2.py", "exec"), ns2); exec(compile(kaynak, "VDYT2.py", "exec"), ns2)

    # ---------------------------------------------------------------- 16) bağımsızlık, e-posta / anahtar, v1 dosyaları değişmedi
    if re.search(r"^\s*(import|from)\s+(FON_IZI|K5\d|K6\d|COL_\w+|IZ_KARNE|BASLAT|takip|VDYT_GRAFIK)\b", kaynak, re.M):
        hata.append("16) VDYT2 Çöl Yolu / K / VDYT_GRAFIK modüllerinden içe alıyor")
    for ad in ("VDYT2.py", "test_vdyt2.py"):
        mt = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if V._V2_EPOSTA.search(mt.replace("vdyt2@test.invalid", "")) or re.search(r"(api[_-]?key|token|password|sifre)\s*=\s*['\"][A-Za-z0-9]{8,}", mt, re.I):
            hata.append(f"16) {ad} içinde e-posta / anahtar biçimli parça var")
    for f in ("VDYT.py", "test_vdyt.py", "arastirma_cikti/vdyt/VDYT_ON_KAYIT.md", "arastirma_cikti/vdyt/VDYT_RAPOR.md"):
        r = subprocess.run(["git", "-C", KOK, "status", "--porcelain", "--", f], capture_output=True, text=True).stdout.strip()
        if r:
            hata.append(f"16) v1 dosyası değişmiş: {r}")
    if "vdyt/paket" in kaynak.replace("vdyt/paket'e", "") or "VDYT_GRAFIK" in re.sub(r"VDYT_GRAFIK\.py ve", "", kaynak).split("D5:")[0][:0]:
        hata.append("16) v1 grafik paketi / VDYT_GRAFIK yoluna yazma")
    return hata


if __name__ == "__main__":
    h = testler()
    for x in h:
        print("HATA:", x)
    print("test_vdyt2:", "TAMAM (16/16)" if not h else f"{len(h)} HATA")
    sys.exit(1 if h else 0)
