"""SIKISMA_OBEK testleri (sentetik veri + 7 tasarım örneği mekanik; gerçek veride sonuç ÖLÇMEZ). Çalıştırma: python test_sikisma_obek.py

1) çakışma kapısı  2) DİP: düşüş + öbek bölge -> S5 DİP, olay ilk gün  3) YOL ÜSTÜ: yükseliş + dinlenme -> S5 YOL  4) orta konumda öbek -> sınıf dışı,
S5 yok  5) aşağı kayan küçük mumlu bölge -> (c) eğim yanlış, S5 yok  6) zıplama mumu (a)'yı bozmaz  7) koşullar elle (mum medyanı, öbek, eğim, BB
yüzdeliği, konum, taban)  8) olay / bölge sonu kuralı (20 bar)  9) GELECEĞE BAKMA: seri t'de kesilince ve t sonrası bozulunca aynı; denetim
fonksiyonu  10) sonuçlar: SC.sc_sonuc ile aynı, M2 / M3 elle  11) panel + KAT + bölge sonu eşi elle  12) (C) işlem ve OC.oc_olc çalışır
13) uçtan uca so_kos (sentetik veri, git kapısız) + rapor  14) mühür / ön kayıt doğrulama  15) kontrol kapısı  16) 7 tasarım örneği (veri varsa):
seçilen nokta 14/14 ve SO_ESIK ile aynı  17) e-posta / anahtar yok.
"""
from __future__ import annotations

import os
import re
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import SIKISMA_OBEK as S  # noqa: E402
import SIKISMA_CEMAL as SC  # noqa: E402
import SIKISMA_YENIDEN as SY  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402

E = S.SO_ESIK
SONUC = []


def kontrol(ad, kosul, ek=""):
    SONUC.append((ad, bool(kosul)))
    print(("TAMAM " if kosul else "HATA  ") + ad + (f"  [{ek}]" if ek != "" else ""))


def _seri(segler, tohum=1, bas="2016-01-04", zipla=None):
    """segler: [(gün, günlük kayma, getiri oynaklığı, mum yarı genişliği)]. Sıkı (mum < %0,5) parçada açılış = önceki kapanış."""
    rng = np.random.default_rng(tohum)
    r, w, sik = [], [], []
    for g, k, s, m in segler:
        r += list(k + rng.normal(0, s, g)); w += list(np.abs(rng.normal(m, m * 0.2, g))); sik += [m < 0.005] * g
    r = np.array(r); w = np.array(w); sik = np.array(sik); n = len(r)
    idx = pd.bdate_range(bas, periods=n)
    C = 100 * np.exp(np.cumsum(r))
    O = np.r_[C[0], C[:-1]] * np.where(sik, 1.0, 1 + rng.normal(0, 0.003, n))
    H = np.fmax(C, O) * (1 + w); L = np.fmin(C, O) * (1 - w)
    if zipla is not None:
        H[zipla] = max(C[zipla], O[zipla]) * 1.05; L[zipla] = min(C[zipla], O[zipla]) * 0.97
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(1e5, 2e5, n).astype(float) * 100 / C}, index=idx)


ARKA = (400, 0.0, 0.01, 0.012)


def _dip(tohum=1, **k):
    return _seri([ARKA, (60, -0.008, 0.004, 0.012), (45, 0.0, 0.0008, 0.002), (60, 0.0, 0.01, 0.012)], tohum, **k)


def _yol(tohum=2):
    return _seri([ARKA, (60, 0.006, 0.004, 0.012), (45, 0.0004, 0.0008, 0.002), (60, 0.0, 0.01, 0.012)], tohum)


def _orta(tohum=3):
    return _seri([ARKA, (40, 0.008, 0.003, 0.012), (20, -0.008, 0.003, 0.012), (45, 0.0, 0.0008, 0.002), (60, 0.0, 0.01, 0.012)], tohum)


def _kayan(tohum=4):
    return _seri([ARKA, (60, -0.008, 0.004, 0.012), (45, -0.004, 0.0008, 0.002), (60, 0.0, 0.01, 0.012)], tohum)


def _hz(d):
    return SY.sy_veri_hazirla(d, SY.SY_ESIK)


def testler():
    # 1) çakışma kapısı
    g = {"so_kos": lambda: None, "__name__": "x"}
    try:
        exec(compile(open(os.path.join(KOK, "SIKISMA_OBEK.py"), encoding="utf-8").read(), "SIKISMA_OBEK.py", "exec"), g)
        kontrol("çakışma kapısı bellekteki adı ezince durur", False)
    except RuntimeError as ex:
        kontrol("çakışma kapısı bellekteki adı ezince durur", "EZDİ" in str(ex))

    # 2) DİP
    d = _hz(_dip())
    X = S.so_s5(d, "ABD")
    s5 = np.where(X.s5c.to_numpy())[0]
    kontrol("DİP: öbek bölgede S5 günü var, hepsi bölgede (pencere gecikmesi < p/2)", len(s5) > 0 and s5.min() >= 460 + 10 and s5.max() <= 505 + 7, f"{s5.min() if len(s5) else '-'}..{s5.max() if len(s5) else '-'}")
    kontrol("DİP: sınıf DİP (YOL değil)", len(s5) > 0 and X.s5c_dip.to_numpy()[s5].all() and not X.s5c_yol.any())
    ev = np.where(X.ev5.to_numpy())[0]
    kontrol("DİP: tek olay, ilk S5 günü", len(ev) == 1 and ev[0] == s5[0] and bool(X.ev5_dip.iat[ev[0]]), str(ev))
    # 3) YOL
    dy = _hz(_yol()); Xy = S.so_s5(dy, "ABD")
    sy_ = np.where(Xy.s5c.to_numpy())[0]
    kontrol("YOL ÜSTÜ: dinlenme bölgesinde S5, sınıf YOL", len(sy_) > 0 and Xy.s5c_yol.to_numpy()[sy_].all() and sy_.min() >= 460, f"{len(sy_)} gün")
    # 4) orta konum
    do = _hz(_orta()); Xo = S.so_s5(do, "ABD")
    kontrol("orta konumda öbek: (a)-(f) doğru günler var ama S5 yok (sınıf dışı)", Xo.cek.iloc[460:505].any() and not Xo.s5c.any(),
            f"cek {int(Xo.cek.sum())} konum {Xo.konum.iloc[470:505].mean():.2f}")
    # 5) aşağı kayan
    dk = _hz(_kayan()); Xk = S.so_s5(dk, "ABD")
    kontrol("aşağı kayan küçük mumlu bölge: (a) doğru, (c) eğim yanlış, bölgede S5 yok", Xk.ca.iloc[475:505].all() and not Xk.cc.iloc[475:505].any() and not Xk.s5c.iloc[460:506].any())
    # 6) zıplama
    dz = _hz(_dip(zipla=490)); Xz = S.so_s5(dz, "ABD")
    kontrol("zıplama mumu (a)'yı bozmaz", Xz.ca.iloc[490:500].all() and Xz.s5c.iloc[490:500].any())
    Ez = {**E, "S5": {**E["S5"], "zipla_cikar": 0}}
    mm0 = S.so_s5(dz, "ABD", None, Ez).mmed.iat[495]
    kontrol("zıplama çıkarılınca medyan ölçüsü değişir (çıkarma kodu çalışıyor)", Xz.mmed.iat[495] <= mm0)

    # 7) koşullar elle
    i = int(s5[0])
    C = d.Close.to_numpy(); O = d.Open.to_numpy(); H = d.High.to_numpy(); L = d.Low.to_numpy()
    mum = (H - L) / C
    kontrol("(a) elle: en büyük mum çıkarılmış medyan", abs(X.mmed.iat[i] - np.median(np.sort(mum[i - 14:i + 1])[:14])) < 1e-12)
    w = np.sort(C[i - 14:i + 1])
    kontrol("(b) elle: bir uç gün hariç bant", abs(X.obek.iat[i] - (min(w[-2] / w[0], w[-1] / w[1]) - 1)) < 1e-12)
    kontrol("(c) elle: EKK eğim x p", abs(X.egim.iat[i] - np.polyfit(np.arange(15), np.log(C[i - 14:i + 1]), 1)[0] * 15) < 1e-10)
    Cp = np.r_[np.nan, C[:-1]]
    kontrol("(d) elle: aşağı açılış payı", abs(X.asagi.iat[i] - np.mean(O[i - 14:i + 1] < Cp[i - 14:i + 1])) < 1e-12)
    bb = (pd.Series(C).rolling(20).std(ddof=0) * 4 / pd.Series(C).rolling(20).mean()).to_numpy()
    kontrol("(e) elle: BBW yüzdeliği önceki 250 gün", abs(X.bbp.iat[i] - np.mean(bb[i - 250:i] <= bb[i])) < 1e-12 and abs(X.bbw.iat[i] - bb[i]) < 1e-12)
    tr = np.fmax(H, Cp) - np.fmin(L, Cp)
    kontrol("ATR250 elle (t-249..t TR/C_önceki)", abs(X.atr5.iat[i] - np.mean(tr[i - 249:i + 1] / Cp[i - 249:i + 1])) < 1e-12)
    c120 = C[i - 119:i + 1]
    kontrol("konum120 ve tepeden düşüş elle", abs(X.konum.iat[i] - (C[i] - c120.min()) / (c120.max() - c120.min())) < 1e-12 and abs(X.dd120.iat[i] - (C[i] / c120.max() - 1)) < 1e-12)
    j = int(sy_[0]); Cy = dy.Close.to_numpy()
    kontrol("taban elle (pencere min >= ilk 5 gün min x 0,99)", bool(Xy.taban.iat[j]) == bool(Cy[j - 14:j + 1].min() >= Cy[j - 14:j - 9].min() * 0.99))

    # 8) olay / bölge sonu
    k = np.zeros(120, bool); k[[10, 11, 12, 25, 26, 60, 61, 100]] = True
    ev_ = S._so_olay(k, 20, 0); bs = S.so_bolge_sonu(ev_, k, 20)
    kontrol("olay kuralı: 10 (bölge 10..26), 60 (34 bar sonra), 100", list(np.where(ev_)[0]) == [10, 60, 100], str(np.where(ev_)[0]))
    kontrol("bölge sonu: 26, 61, 100", list(bs[ev_]) == [26, 61, 100], str(bs[ev_]))

    # 9) geleceğe bakma
    G = S.so_gecmis(d, "ABD")
    t = d.index[i + 2]
    kol = S._SO_DENETIM_KOL
    a = pd.to_numeric(G.loc[t, kol], errors="coerce").astype(float).to_numpy()
    b = pd.to_numeric(S.so_gecmis(d[d.index <= t], "ABD").iloc[-1][kol], errors="coerce").astype(float).to_numpy()
    kontrol("geleceğe bakma: seri t'de kesilince aynı", np.allclose(a, b, equal_nan=True, rtol=1e-9, atol=1e-12))
    db = d.copy(); db.iloc[i + 3:, :4] = db.iloc[i + 3:, :4] * 3.0
    c3 = pd.to_numeric(S.so_gecmis(db, "ABD").loc[t, kol], errors="coerce").astype(float).to_numpy()
    kontrol("geleceğe bakma: t'den sonrası bozulunca aynı", np.allclose(a, c3, equal_nan=True))
    kontrol("so_gelecek_denetimi geçer", S.so_gelecek_denetimi({"A": d}, pd.DataFrame({"sembol": ["A"], "tarih": [t]}), "ABD") == 1)

    # 10) sonuçlar
    R = S.so_sonuc(d, G)
    Rs = SC.sc_sonuc(d, G, S._so_sc_E(15))
    kontrol("B1 / BH2 / B1k2 = SC.sc_sonuc", all((R[c].to_numpy() == Rs[c].to_numpy()).all() for c in ("B1", "BH2", "B1k2", "BH2k2", "k1")))
    q = i + 1; mf = (H[q + 1:q + 21] - L[q + 1:q + 21]) / C[q:q + 20]
    kontrol("M2 / M3 elle", bool(R.M2.iat[q]) == bool((mf >= 2 * G.mmed.iat[q]).any()) and bool(R.M3.iat[q]) == bool((mf >= 3 * G.mmed.iat[q]).any()))
    dl = d.copy(); dl["ekran"] = dl.Close
    rl = S._so_bolge_satir("A", dl, X, i, int(R.bs_i.iat[i]), 15, 0.11)
    e_ = int(R.bs_i.iat[i])
    kontrol("liste satırı (sentetik): bölge sonu, g20 bölge sonundan, sınıf", rl["sinif"] == "DİP" and rl["bolge_son"] == str(d.index[e_].date())
            and abs(rl["g20"] - (C[e_ + 20] / C[e_] - 1)) < 1e-12 and len(S._so_bolge_md([rl])) == 3)
    kontrol("bölge sonu indeksi olay barında, son S5 günü", int(R.bs_i.iat[i]) == int(s5.max()), f"{R.bs_i.iat[i]} vs {s5.max()}")

    # 11) panel + KAT + bölge sonu
    V = {f"D{k}": _hz(_dip(tohum=10 + k)) for k in range(4)}
    V.update({f"Y{k}": _hz(_yol(tohum=20 + k)) for k in range(4)})
    V.update({f"Z{k}": _hz(_seri([(565, 0.0, 0.012, 0.012)], tohum=40 + k)) for k in range(110)})
    P = S.so_panel(V, "ABD")
    kontrol("panelde DİP ve YOL olayı var", int((P.uygun & P.ev5_dip).sum()) >= 2 and int((P.uygun & P.ev5_yol).sum()) >= 2,
            f"{int((P.uygun & P.ev5_dip).sum())} / {int((P.uygun & P.ev5_yol).sum())}")
    TA, sat = S.so_olc_A(P)
    X1 = sat["S5_es1"]
    if len(X1):
        r0 = X1.iloc[0]
        es = P[(P.tarih == r0.tarih) & (P.hucA == r0.hucA) & P.uygun & ~P.s5c]
        kontrol("eş 1 ortalaması elle (aynı gün, aynı hücre, S5 dışı)", abs(es.B1.mean() - r0.es_B1) < 1e-12 and len(es) == r0.es_n)
        Y = X1[X1.donem == "2016-22"]
        k_ = TA[(TA.sikisma == "S5") & (TA.es == "es1") & (TA.olcu == "BH2") & (TA.donem == "2016-22")]
        if Y.es_BH2.sum() > 0:
            kontrol("KAT elle = Σ olay / Σ eş", abs(k_.kat.iat[0] - Y.BH2.sum() / Y.es_BH2.sum()) < 1e-12)
    else:
        kontrol("eş 1 satırı var", False)
    kontrol("KAT tablosu üç tanım x iki eş", set(TA.sikisma) >= {"S5", "S5_DIP", "S5_YOL"} and set(TA.es) >= {"es1", "es2"})
    TBS, XBS = S.so_olc_bolge_sonu(P)
    if len(XBS):
        r0 = XBS.iloc[0]
        es = P[(P.tarih == r0.bs_tarih) & (P.hucA == r0.e_hucA) & P.uygun & ~P.s5c]
        olay_e = P[(P.sembol == r0.sembol) & (P.tarih == r0.bs_tarih)].iloc[0]
        kontrol("bölge sonu: olay değeri e günündeki B1, eş e günü aynı hücre", abs(es.B1.mean() - r0.es_A3) < 1e-12 and bool(olay_e.B1) == bool(r0.A3)
                and abs(es.M2.mean() - r0.es_M2) < 1e-12)
    else:
        kontrol("bölge sonu satırı var", False)
    kontrol("so_karar etiket üretir", "etiket" in S.so_karar(TA)["S5_DIP"]["B1"])
    # 12) (C) ve OC
    tC, XC = S.so_olc_C(P, "ev5_yol")
    kontrol("(C) SY.sy_olc_C S5_YOL olaylarıyla çalışır", len(tC) == 4 and int(XC.shape[0]) == int((P.uygun_c & P.ev5_yol).sum()))
    ol = P.loc[P.ev5, ["sembol", "tarih"]].copy(); ol["pazar"] = "ABD"
    Vd = OC._oc_veri_sar({k: v[["Open", "High", "Low", "Close", "Volume"]] for k, v in V.items()}, "ABD")
    So = OC.oc_olc(ol.reset_index(drop=True), {"ABD": Vd})
    kontrol("OC.oc_olc S5 olaylarıyla çalışır", "hucre" in So and len(So["hucre"]) == 3, So["etiket"]["genel"])

    with tempfile.TemporaryDirectory() as td:
        # 13) uçtan uca (sentetik veri; git kapısız)
        vk = os.path.join(td, "veri"); os.makedirs(vk)
        pd.to_pickle({k: v[["Open", "High", "Low", "Close", "Volume"]] for k, v in V.items()}, os.path.join(vk, "V_ABD.pkl"))
        ck = os.path.join(td, "cikti"); os.makedirs(ck)
        y = os.path.join(ck, S.SO_DOSYA["onkayit"])
        open(y, "w", encoding="utf-8").write(
            f"- MÜHÜR (SO_ESIK sha256): `{S.so_esik_sha()}`\n- KOD (SIKISMA_OBEK.py sha256): `{SY._sy_sha_dosya(S.SO_YOL['kod'])}`\n"
            f"- SC_KOD (SIKISMA_CEMAL.py sha256): `{SY._sy_sha_dosya(S.SO_YOL['sc_kod'])}`\n- SY_KOD (SIKISMA_YENIDEN.py sha256): `{SY._sy_sha_dosya(S.SO_YOL['sy_kod'])}`\n"
            f"- ZAMAN (UTC): `x`\n\n{OC.oc_kapi_satirlari()}\n\n{S.so_kontrol_tablosu()}\n")
        try:
            Rk = S.so_kos(cikti=ck, veri=vk, git=False, kontrol=True, pazarlar=("ABD",), satir=os.path.join(td, "satir"), oc_veri=False)
            kontrol("uçtan uca so_kos + rapor (sentetik, git kapısız)", "S5" in Rk["sonuc"]["karar"] and "DÜZ DİL ÖZET" in Rk["rapor"]
                    and os.path.exists(os.path.join(td, "satir", "bolge_sonu_ABD.csv.gz")))
        except Exception as ex:   # noqa: BLE001
            kontrol("uçtan uca so_kos + rapor (sentetik, git kapısız)", False, repr(ex))
        # 14) mühür / ön kayıt
        try:
            S.so_onkayit_dogrula(os.path.join(td, "yok.md"), git=False); kontrol("ön kayıt yoksa durur", False)
        except S.SOHata:
            kontrol("ön kayıt yoksa durur", True)
        y2 = os.path.join(td, "ok.md")
        sat_ = f"- KOD (SIKISMA_OBEK.py sha256): `{'0' * 64}`\n- SC_KOD (SIKISMA_CEMAL.py sha256): `{'0' * 64}`\n- SY_KOD (SIKISMA_YENIDEN.py sha256): `{'0' * 64}`\n- ZAMAN (UTC): `x`\n"
        open(y2, "w", encoding="utf-8").write(f"- MÜHÜR (SO_ESIK sha256): `{'0' * 64}`\n" + sat_)
        try:
            S.so_onkayit_dogrula(y2, git=False); kontrol("mühür farkı durdurur", False)
        except S.SOHata as ex:
            kontrol("mühür farkı durdurur", "mühr" in str(ex))
        open(y2, "w", encoding="utf-8").write(f"- MÜHÜR (SO_ESIK sha256): `{S.so_esik_sha()}`\n" + sat_)
        try:
            S.so_onkayit_dogrula(y2, git=False); kontrol("kod sha farkı durdurur", False)
        except S.SOHata as ex:
            kontrol("kod sha farkı durdurur", "sha256" in str(ex))
        # 15) kontrol kapısı
        import IZ_KARNE as IK
        k2 = os.path.join(td, "k.md"); open(k2, "w", encoding="utf-8").write(S.so_kontrol_tablosu())
        kontrol("kontrol kapısı ön kayıt tablosunu geçer", IK.ik_kontrol_kapisi(k2)["gecti"])
        open(k2, "w", encoding="utf-8").write("boş")
        try:
            IK.ik_kontrol_kapisi(k2); kontrol("boş kontrol tablosu durur", False)
        except RuntimeError:
            kontrol("boş kontrol tablosu durur", True)
    # 16) 7 tasarım örneği
    if os.path.isdir(S.SO_YOL["yahoo"]) or os.path.exists(os.path.join(S.SO_YOL["veri"], "V_BIST.pkl")):
        J = S.so_tasarim(yaz=False)
        kontrol("7 örnek: seçilen nokta SO_ESIK secilen ile aynı", J["secilen"] == E["S5"]["secilen"], J["secilen"])
        kontrol("7 örnek: seçilen noktada bütün sınamalar tuttu (3 seçmeli doğru sınıf, 4 seçmemeli dışarıda)",
                all(v["tutar"] for v in J["secilen_sonuc"].values()) and len(J["secilen_sonuc"]) == 14,
                [k for k, v in J["secilen_sonuc"].items() if not v["tutar"]])
    else:
        print("ATLANDI 7 örnek (veri yok)")
    # 17) e-posta / anahtar
    desen = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    dosyalar = [os.path.join(KOK, "SIKISMA_OBEK.py"), os.path.join(KOK, "test_sikisma_obek.py")]
    kl = S.SO_YOL["cikti"]
    if os.path.isdir(kl):
        dosyalar += [os.path.join(kl, f) for f in os.listdir(kl) if f.endswith((".md", ".json"))]
    bulunan = [f for f in dosyalar if desen.search(open(f, encoding="utf-8").read().replace("noreply@anthropic.com", ""))]
    kontrol("e-posta biçimli parça yok", not bulunan, bulunan)
    kontrol("anahtar / token yok", not any(re.search(r"(api[_-]?key|token|secret)\s*[:=]\s*['\"][A-Za-z0-9]{12,}", open(f, encoding="utf-8").read(), re.I) for f in dosyalar))


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    testler()
    n_h = sum(1 for _, k in SONUC if not k)
    print(f"\n{len(SONUC) - n_h}/{len(SONUC)} test geçti")
    sys.exit(1 if n_h else 0)
