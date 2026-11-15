"""test_ters_parmak — TERS_PARMAK.py sentetik testleri (veri gerekmez).

1) büyük mum tanımı (3 x ATR250 VE 2 x σ250, önceki bardan; boşluk > 7 takvim günü sayılmaz; yön)
2) önceki pencere ölçüleri yalnız s ve öncesi: s'den sonraki barlar değişince / seri s'de kesilince ölçüler aynı (büyük mum günü ölçüye girmez)
3) elle hesap: mum_10, egim_10, bant_20, kucuk_son, alt_test_20, konum_250
4) kes: 'kes' gününden sonra büyük mum etiketi ve sonuç penceresi NaN
5) kontrol eşleme: aynı ay, aynı σ250 ondalığı x likidite üçlüsü, uygun, ertesi gün büyük mum yok, en çok 5 kat
6) kural uygulaması ve arama yordamı (en çok 3 kural, en çok 1 ortak ölçü)
7) tekilleştirme ve 'önceki 20 bar' kapsaması (kaba kuvvetle)
8) KAT bootstrap: tp_kat_p aralığı OC.oc_kat ile birebir; tp_kural_olc çalışır
9) cetvel çağrısı: OC.oc_olc sentetik profil günleriyle
10) kapı: ön kayıt yok / sha bozuk -> durur; e-posta / anahtar taraması
Çalıştır: python test_ters_parmak.py
"""
import os
import re
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
warnings.filterwarnings("ignore")

import ORTAK_CETVEL as OC  # noqa: E402
import TERS_PARMAK as TP  # noqa: E402

GECTI, KALDI = [], []


def kontrol(ad, kosul, ek=""):
    (GECTI if kosul else KALDI).append(ad)
    print(("  OK   " if kosul else "  HATA ") + ad + (f"  ({ek})" if ek else ""))


def hisse(n, tohum, sok=(), bas="2016-01-01", sigma=0.015):
    """Rastgele yürüyüş; sok: [(bar, getiri)] büyük mum enjeksiyonu (aralık da büyür)."""
    rng = np.random.default_rng(tohum)
    r = rng.normal(0.0002, sigma, n)
    for b, g in sok:
        r[b] = g
    C = 50 * np.exp(np.cumsum(r)); Cp = np.r_[C[0], C[:-1]]
    O = Cp * (1 + rng.normal(0, 0.002, n))
    ek = np.abs(rng.normal(0, 0.006, n)) + 0.001
    H = np.maximum(O, C) * (1 + ek); L = np.minimum(O, C) * (1 - ek)
    V = rng.integers(10000, 90000, n).astype(float)
    ix = pd.bdate_range(bas, periods=n)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V, "Kur": 1.0}, index=ix)


def main():
    print("== test_ters_parmak ==")
    # 1) büyük mum
    d = hisse(600, 1, sok=[(400, 0.12), (500, -0.10)])
    B = TP.tp_buyuk(d)
    kontrol("enjekte yukarı büyük mum bulunur (+1)", B.big.iat[400] == 1, str(B.big.iat[400]))
    kontrol("enjekte aşağı büyük mum bulunur (-1)", B.big.iat[500] == -1, str(B.big.iat[500]))
    Hh, Ll, Cc = d.High.to_numpy(), d.Low.to_numpy(), d.Close.to_numpy()
    TR = np.maximum(Hh[1:], Cc[:-1]) - np.minimum(Ll[1:], Cc[:-1]); TR = np.r_[Hh[0] - Ll[0], TR]
    A399 = TR[150:400].mean(); lr = np.log(Cc[1:] / Cc[:-1]); S399 = lr[149:399].std(ddof=1)
    elle = (TR[400] >= 3 * A399) and (abs(Cc[400] / Cc[399] - 1) >= 2 * S399)
    kontrol("ATR250 / σ250 önceki 250 bardan (elle)", abs(B.A.iat[399] - A399) < 1e-10 and abs(B.S.iat[399] - S399) < 1e-12 and elle)
    kontrol("250 bar öncesi tanımsız (NaN)", np.isnan(B.big.iat[200]))
    say = int((np.abs(B.big.to_numpy()[260:]) == 1).sum())
    kontrol("rastgele yürüyüşte büyük mum nadir", say <= 6, f"{say}")
    d2 = d.copy(); yeni = d2.index.to_list(); yeni[400:] = [x + pd.Timedelta(days=10) for x in yeni[400:]]; d2.index = pd.DatetimeIndex(yeni)
    kontrol("t-1 / t arası > 7 takvim günü: büyük mum sayılmaz", TP.tp_buyuk(d2).big.iat[400] == 0)

    # 2) geleceğe bakma: s'den sonrası değişince ve seri s'de kesilince aynı ölçüler
    X = TP.tp_olculer(d)
    s = 399
    dd = d.copy(); dd.iloc[s + 1:, :4] *= 3.0; dd.iloc[s + 1:, 4] *= 7
    X2 = TP.tp_olculer(dd)
    kontrol("s'den sonraki barlar değişince s ölçüleri aynı", np.allclose(X.iloc[s].to_numpy(float), X2.iloc[s].to_numpy(float), equal_nan=True))
    Xk = TP.tp_olculer(d.iloc[:s + 1])
    kontrol("seri s'de kesilince s ölçüleri aynı (büyük mum günü t = s+1 hariç)", np.allclose(X.iloc[s].to_numpy(float), Xk.iloc[-1].to_numpy(float), equal_nan=True))
    fark = [s_ for s_ in range(300, 590, 7) if not np.allclose(X.iloc[s_].to_numpy(float), TP.tp_olculer(d.iloc[:s_ + 1]).iloc[-1].to_numpy(float), equal_nan=True)]
    kontrol("kesme testi 42 günde", not fark, str(fark[:5]))
    Hk = TP.tp_hisse(d.iloc[:s + 1])
    kontrol("tp_hisse geçmiş sütunları kesilince aynı (A, S, Lq)", np.allclose(TP.tp_hisse(d).loc[d.index[s], ["A", "S", "Lq"]].to_numpy(float),
                                                                           Hk.iloc[-1][["A", "S", "Lq"]].to_numpy(float)))
    kontrol("30 ölçü", len(TP.TP_OLCULER) == 30, str(len(TP.TP_OLCULER)))

    # 3) elle hesap
    O_, H_, L_, C_ = (d[k].to_numpy() for k in ("Open", "High", "Low", "Close")); A = B.A.iat[s]; S = B.S.iat[s]
    rg = H_ - L_
    kontrol("mum_10 elle", abs(X.mum_10.iat[s] - rg[s - 9:s + 1].mean() / A) < 1e-10)
    y = np.log(C_[s - 9:s + 1]); sl = np.polyfit(np.arange(10), y, 1)[0]
    kontrol("egim_10 elle (polyfit)", abs(X.egim_10.iat[s] - sl / S) < 1e-8)
    kontrol("bant_20 elle", abs(X.bant_20.iat[s] - np.log(C_[s - 19:s + 1].max() / C_[s - 19:s + 1].min()) / (S * np.sqrt(20))) < 1e-10)
    ks = 0
    for j in range(40):
        if rg[s - j] < 0.5 * A:
            ks += 1
        else:
            break
    kontrol("kucuk_son elle", X.kucuk_son.iat[s] == ks, f"{X.kucuk_son.iat[s]} vs {ks}")
    lw = L_[s - 19:s + 1]
    kontrol("alt_test_20 elle", X.alt_test_20.iat[s] == (lw <= lw.min() + 0.25 * A).sum() - 1)
    kontrol("konum_250 elle", abs(X.konum_250.iat[s] - (C_[s] - L_[s - 249:s + 1].min()) / (H_[s - 249:s + 1].max() - L_[s - 249:s + 1].min())) < 1e-10)
    # O H-L dışındaysa aralık genişler
    d3 = d.copy(); d3.iloc[350, 0] = d3.High.iat[350] * 1.05
    kontrol("açılış H dışında: gövde / fitil oranları [0, 1]", (TP.tp_olculer(d3)[["govde_20", "ust_fitil_20", "alt_fitil_20"]].iloc[350:370].to_numpy() >= -1e-12).all()
            and (TP.tp_olculer(d3)[["govde_20", "ust_fitil_20", "alt_fitil_20"]].iloc[350:370].to_numpy() <= 1 + 1e-12).all())

    # 4) kes
    Hc = TP.tp_hisse(d, kes=str(d.index[450].date()))
    kontrol("kes: kes günü ve sonrası büyük mum NaN", np.isnan(Hc.big0.iat[450]) and np.isnan(Hc.big0.iat[500]) and Hc.big0.iat[400] == 1)
    kontrol("kes: sonuç penceresi kesi aşan f20 NaN", np.isnan(Hc.f20.iat[440]) and Hc.f20.iat[420] in (0.0, 1.0) and Hc.f20.iat[385] == 1.0)
    kontrol("nb1 = ertesi bar büyük mum", Hc.nb1.iat[399] == 1)
    Hn = TP.tp_hisse(d)
    kontrol("kes yokken f20 / y20 ölçülür", Hn.f20.iat[490] == 1.0 and Hn.y20.iat[490] == -1 and Hn.y20.iat[390] == 1)
    kontrol("son 20 barda f20 NaN (gelecek yok)", np.isnan(Hn.f20.iat[-5]))

    # 5) panel + kontrol eşleme (45 hisse)
    rng = np.random.default_rng(5)
    V = {}
    for k in range(45):
        soklar = [(int(b), float(rng.choice([-1, 1]) * rng.uniform(0.09, 0.15))) for b in rng.choice(np.arange(300, 880), 6, replace=False)]
        V[f"H{k:02d}"] = hisse(900, 100 + k, sok=soklar, bas="2015-06-01", sigma=float(rng.uniform(0.01, 0.03)))
    Vd = OC._oc_veri_sar(V, "ABD")
    T = TP.tp_panel(Vd, kes="2018-06-01", bas="2015-01-01")
    kontrol("panel: uygun satır var, kovalar 0-9 / 0-2", T.uygun.any() and T.loc[T.uygun, "sig_ay"].between(0, 9).all() and T.loc[T.uygun, "lik_gun"].between(0, 2).all())
    lq = T[np.isfinite(T.Lq)]
    alt_pay = lq.groupby("tarih").lik_alt.mean().mean()
    kontrol("likidite alt %20 dışarı (gün kesiti)", 0.15 < alt_pay < 0.25, f"{alt_pay:.3f}")
    Xo = TP.tp_kesif_orneklem(T, bas="2016-01-01", son="2018-05-01")
    b_, k_ = Xo[Xo.grup == "BUYUK"], Xo[Xo.grup == "KONTROL"]
    kontrol("keşif örneklemi: büyük ve kontrol var", len(b_) > 20 and len(k_) > 0, f"{len(b_)} / {len(k_)}")
    kontrol("kontroller: ertesi gün büyük mum yok ve uygun", (k_.nb1 == 0).all() and k_.uygun.all() and b_.uygun.all())
    eb = b_.groupby(["ay", "kat_ay"]).size(); ek = k_.groupby(["ay", "kat_ay"]).size()
    kontrol("kontroller aynı ay x katmanda, en çok 5 kat", set(ek.index) <= set(eb.index) and all(ek[i] <= 5 * eb[i] for i in ek.index))
    kontrol("büyük mumlar 20 barda bir (aynı hisse)", all((np.diff(g.i.to_numpy()) >= 20).all() for _, g in b_.groupby("sid")))

    # 6) kural uygulama ve arama
    kr = {"kod": "PX", "kosul": [{"olcu": "mum_10", "yon": "<=", "esik": 0.9, "yuzdelik": 0.3}, {"olcu": "hacim_10_50", "yon": ">=", "esik": 1.0, "yuzdelik": 0.7}]}
    m = TP.tp_kural_uygula(T, kr)
    kontrol("kural VE uygulaması", (m == ((T.mum_10.to_numpy() <= 0.9) & (T.hacim_10_50.to_numpy() >= 1.0))).all())
    Xo2 = Xo.copy(); Xo3 = Xo.copy(); Xo3["pazar"] = "AVR"; Xa = pd.concat([Xo2, Xo3], ignore_index=True)
    tek = TP.tp_tek_olcu(Xa)
    kontrol("tek ölçü tablosu: 30 ölçü x 3 (ABD, AVR, HAVUZ)", len(tek) == 90 and tek.q.notna().any())
    ara = TP.tp_kural_ara(Xa, tek)
    ks_ = ara["kurallar"]
    kontrol("arama: en çok 3 kural, en çok 1 ortak ölçü", len(ks_) <= 3 and all(len(set(a["olcu_set"]) & set(b["olcu_set"])) <= 1 for a in ks_ for b in ks_ if a is not b),
            f"{[k['ad'] for k in ks_]}")
    kontrol("arama: her kural 1-3 koşul, iki pazarda duyarlılık >= %10", all(1 <= len(k["kosul"]) <= 3 and min(k["cc"][p]["duyarlilik_cc"] for p in ("ABD", "AVR")) >= 0.10
                                                                         for k in ks_))
    a_, p_ = TP.tp_auc(np.array([3.0, 4, 5]), np.array([1.0, 2, 3]))
    kontrol("AUC elle (8,5/9)", abs(a_ - 8.5 / 9) < 1e-12)
    kontrol("BH q", np.allclose(TP.tp_bh(np.array([0.01, 0.04, 0.03])), [0.03, 0.04, 0.04]))

    # 7) tekil ve kapsama
    sid = np.array([0, 0, 0, 0, 1, 1]); ii = np.array([1, 5, 21, 40, 3, 10])
    kontrol("tp_tekil 20 bar", TP.tp_tekil(sid, ii, 20).tolist() == [True, False, True, False, True, False])
    fl = (np.random.default_rng(3).random(len(T)) < 0.02)
    kp = TP._tp_kapsar(T, fl, 20)
    sids, iis = T.sid.to_numpy(), T.i.to_numpy(); hata = 0
    for r in np.random.default_rng(4).choice(len(T), 400, replace=False):
        g = (sids == sids[r]) & (iis <= iis[r]) & (iis > iis[r] - 20)
        hata += int(kp[r] != fl[g].any())
    kontrol("önceki 20 bar kapsaması (kaba kuvvet 400 satır)", hata == 0, str(hata))

    # 8) KAT
    rng = np.random.default_rng(9); n = 400
    ol = (rng.random(n) < 0.2).astype(float); orn = np.full(n, 0.12); ay = np.array([f"2020-{1 + k % 12:02d}" for k in range(n)])
    r1 = OC.oc_kat(ol, orn, ay); r2 = TP.tp_kat_p(ol, orn, ay)
    kontrol("tp_kat_p aralığı OC.oc_kat ile birebir", abs(r1["alt"] - r2["alt_kontrol"]) < 1e-12 and r1["kat"] == r2["kat"] and r2["p"] < 0.05, f"{r2}")
    Tn = TP.tp_panel(Vd, kes=None, bas="2015-01-01")
    R = TP.tp_kural_olc(Tn, kr, [["x", "2016-06-01", "2018-06-30"]], satir_don=True)
    h = R["hucre"]["x"]
    kontrol("tp_kural_olc: profil günü, KAT, duyarlılık", h["profil_gunu"] > 0 and h["n"] >= 0 and "duyarlilik" in h and isinstance(h["gecer"], bool), f"n {h['n']} kat {h['kat']}")
    Hx = {"ABD 2023": {"gecer": True, "n": 50}, "ABD 2024-26": {"gecer": True, "n": 50}, "AVR 2023": {"gecer": True, "n": 50}, "AVR 2024-26": {"gecer": True, "n": 50}}
    kontrol("etiket: dört hücre + BH -> PARMAK İZİ VAR", TP.tp_kural_etiket(Hx, 0.01) == "PARMAK İZİ VAR")
    Hx["AVR 2023"]["gecer"] = False
    kontrol("etiket: üç hücre -> EMARE", TP.tp_kural_etiket(Hx, 0.01) == "EMARE")
    Hy = {k: {"gecer": False, "n": 2000} for k in Hx}
    kontrol("etiket: hiçbiri + güç -> İZ DEĞİL", TP.tp_kural_etiket(Hy, 0.9) == "İZ DEĞİL")
    Hy["AVR 2023"]["n"] = 500
    kontrol("etiket: hiçbiri, güç yok -> ÖLÇÜLEMEDİ", TP.tp_kural_etiket(Hy, 0.9) == "ÖLÇÜLEMEDİ")

    # 9) cetvel çağrısı
    ev = R["satir"][["sembol", "tarih"]].head(80).copy(); ev["pazar"] = "ABD"
    S_ = OC.oc_olc(ev.reset_index(drop=True), {"ABD": Vd})
    kontrol("OC.oc_olc profil günleriyle çalışır", "hucre" in S_ and len(S_["hucre"]) == 3, S_["etiket"]["genel"])
    OC._OC_PANEL_ONBELLEK.clear()

    # 10) kapı ve tarama
    with tempfile.TemporaryDirectory() as kl:
        try:
            TP.tp_onkayit_dogrula(os.path.join(kl, "yok.md"), git=False); kontrol("ön kayıt yok -> durur", False)
        except TP.TPHata:
            kontrol("ön kayıt yok -> durur", True)
        y = os.path.join(kl, TP.TP_DOSYA["onkayit"])
        open(os.path.join(kl, TP.TP_DOSYA["kural"]), "w").write("{}")
        open(y, "w").write(f"TP_ESIK_SHA: `{'0' * 64}`\nTP_KOD_SHA: `{'0' * 64}`\nTP_KURAL_SHA: `{'0' * 64}`\n")
        try:
            TP.tp_onkayit_dogrula(y, git=False); kontrol("sha bozuk -> durur", False)
        except TP.TPHata:
            kontrol("sha bozuk -> durur", True)
        open(y, "w").write(f"TP_ESIK_SHA: `{TP.tp_sha(TP.TP_ESIK)}`\nTP_KOD_SHA: `{TP._tp_sha_dosya(TP.TP_YOL['kod'])}`\n"
                           f"TP_KURAL_SHA: `{TP._tp_sha_dosya(os.path.join(kl, TP.TP_DOSYA['kural']))}`\n")
        kontrol("sha doğru -> kapı açık (git'siz)", TP.tp_onkayit_dogrula(y, git=False)["esik"] == TP.tp_sha(TP.TP_ESIK))
        try:
            TP._tp_yaz(os.path.join(kl, "x.md"), "iletisim: ornek" + "@" + "alan.com"); kontrol("e-posta yazımı durur", False)
        except TP.TPHata:
            kontrol("e-posta yazımı durur", True)
    tablo = TP.tp_kontrol_tablosu()
    import IZ_KARNE as IK
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(tablo); yk = f.name
    kontrol("KONTROL LİSTESİ ik_kontrol_kapisi'ni geçer", IK.ik_kontrol_kapisi(yk)["gecti"]); os.unlink(yk)
    dosyalar = [TP.TP_YOL["kod"], os.path.abspath(__file__)]
    kl = TP.TP_YOL["cikti"]
    if os.path.isdir(kl):
        dosyalar += [os.path.join(kl, x) for x in os.listdir(kl) if x.endswith((".md", ".json"))]
    desen = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|(?i:api[_-]?key|token|secret)\s*[:=]\s*['\"][A-Za-z0-9]{12,}")
    bulgu = [x for x in dosyalar if desen.search(open(x, encoding="utf-8").read())]
    kontrol("e-posta / anahtar yok (kod, test, çıktılar)", not bulgu, str(bulgu))
    print(f"\n{len(GECTI)} geçti, {len(KALDI)} kaldı")
    return len(KALDI) == 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
