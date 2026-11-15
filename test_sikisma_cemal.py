"""SIKISMA_CEMAL testleri (sentetik veri + FENER mekanik doğrulama; gerçek veride sonuç ÖLÇMEZ). Çalıştırma: python test_sikisma_cemal.py

1) çakışma kapısı  2) S4 tespiti: oynak geçmiş + 35 gün yatay dar bölge -> S4 doğru, olay 20 bar arayla  3) küçük mum ama aşağı kayan bölge
-> (iii) yanlış, S4 yok  4) kısa (12 gün) dar bölge: (i)-(iii) doğru, run < 10 günlerde S4 yok  5) GELECEĞE BAKMA: seri t'de kesilince S4 / tanı sütunları aynı;
t'den sonraki barlar bozulunca da aynı  6) sonuçlar: BH2 = SY B2, B1 = SY B1, k=2 varyantı >= k=3, zaman / yön elle  7) panel + KAT: satır
tablosundan elle KAT ve eş ortalaması (aynı gün, aynı hücre, S4 dışı)  8) (C) işlem SY.sy_olc_C ile çalışır  9) cetvel çağrısı OC.oc_olc
10) mühür / ön kayıt doğrulama (eksik / mühür farkı -> SCHata)  11) kontrol kapısı ön kayıt tablosunu geçer  12) FENER mekanik doğrulama (veri varsa):
yanlış bölgede S4 yok; asıl bölge sonucu ön kayıttaki tanıyla aynı  13) e-posta / anahtar yok.
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
import SIKISMA_CEMAL as S  # noqa: E402
import SIKISMA_YENIDEN as SY  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402

E = S.SC_ESIK
SONUC = []


def kontrol(ad, kosul, ek=""):
    SONUC.append((ad, bool(kosul)))
    print(("TAMAM " if kosul else "HATA  ") + ad + (f"  [{ek}]" if ek != "" else ""))


def _seri(n=520, tohum=1, bolge=None, kayma=0.0, bas="2016-01-04"):
    """Oynak seri (günlük ~%2, mum ~%2,4); bolge=(a, b): bu barlarda mum %0,4, kapanış sabit (+ kayma/gün), sonra oynak devam."""
    rng = np.random.default_rng(tohum)
    idx = pd.bdate_range(bas, periods=n)
    r = rng.normal(0, 0.02, n)
    if bolge:
        a, b = bolge
        r[a:b] = kayma + rng.normal(0, 0.0005, b - a)
    C = 100 * np.exp(np.cumsum(r))
    w = np.abs(rng.normal(0.012, 0.004, n))
    if bolge:
        w[a:b] = 0.002
    O = np.r_[C[0], C[:-1]] * (1 + (rng.normal(0, 0.0002, n) if bolge else 0))
    H = np.fmax(C * (1 + w), np.fmax(O, C)); L = np.fmin(C * (1 - w), np.fmin(O, C))
    if bolge:   # bölgede açılış = önceki kapanış (aşağı açılış payı ~0) ve mum dar
        O[a:b] = np.r_[C[a - 1:b - 1]]; H[a:b] = np.fmax(C[a:b], O[a:b]) * 1.002; L[a:b] = np.fmin(C[a:b], O[a:b]) * 0.998
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(1e5, 2e5, n).astype(float)}, index=idx)


def _hz(d):
    return SY.sy_veri_hazirla(d, SY.SY_ESIK)


def testler():
    # 1) çakışma kapısı
    g = {"sc_kos": lambda: None, "__name__": "x"}
    try:
        exec(compile(open(os.path.join(KOK, "SIKISMA_CEMAL.py"), encoding="utf-8").read(), "SIKISMA_CEMAL.py", "exec"), g)
        kontrol("çakışma kapısı bellekteki adı ezince durur", False)
    except RuntimeError as ex:
        kontrol("çakışma kapısı bellekteki adı ezince durur", "EZDİ" in str(ex))

    # 2) S4 tespiti
    d = _hz(_seri(bolge=(400, 435)))
    X = S.sc_s4(d, "ABD", 15)
    s4 = np.where(X.s4c.to_numpy())[0]
    kontrol("yatay dar bölgede S4 doğru", len(s4) > 0 and s4.min() >= 400 + 9 and s4.max() <= 435 + 3, f"{s4.min() if len(s4) else '-'}..{s4.max() if len(s4) else '-'}")
    ev = np.where(X.ev4.to_numpy())[0]
    kontrol("olay ilk S4 günü ve 20 bar ara", len(ev) >= 1 and ev[0] == s4[0] and (len(ev) < 2 or np.diff(ev).min() >= 20), str(ev))
    kontrol("bölge dışında S4 yok", not X.s4c.to_numpy()[:400].any() and not X.s4c.to_numpy()[440:].any())
    i = int(s4[0])
    C = d.Close.to_numpy(); mum = (d.High - d.Low).to_numpy() / C
    m15 = mum[i - 14:i + 1].mean()
    dag = np.array([mum[s - 14:s + 1].mean() for s in range(i - 15 - 249, i - 15 + 1)])
    kontrol("(i) elle: pencere ort mum <= önceki 250 günün 15 gün ortalaması %20 yüzdeliği",
            abs(X.m.iat[i] - m15) < 1e-12 and abs(X.qm.iat[i] - np.quantile(dag, 0.2)) < 1e-12)
    bb = pd.Series(C).rolling(20).std(ddof=0) * 4 / pd.Series(C).rolling(20).mean()
    kontrol("(ii) elle: BBW(t) ve önceki 250 gün %20 yüzdeliği", abs(X.bbw.iat[i] - bb.iat[i]) < 1e-12 and abs(X.qb.iat[i] - np.quantile(bb.iloc[i - 250:i], 0.2)) < 1e-12)
    kontrol("(iii) elle: net ve bant", abs(X.net.iat[i] - (C[i] / C[i - 14] - 1)) < 1e-12 and abs(X.bant4.iat[i] - (C[i - 14:i + 1].max() / C[i - 14:i + 1].min() - 1)) < 1e-12)

    # 3) küçük mum ama aşağı kayıyor -> (iii) yanlış
    d2 = _hz(_seri(bolge=(400, 435), kayma=-0.005))
    X2 = S.sc_s4(d2, "ABD", 15)
    kontrol("aşağı kayan küçük mumlu bölgede S4 yok (net kayma)", not X2.s4c.any() and X2.ci.iloc[410:435].any(), f"(i) gün {int(X2.ci.iloc[400:440].sum())}")
    # 4) kısa bölge: (i)-(iii) doğru ama (iv) run < 10 olan günler S4 değil
    d3 = _hz(_seri(bolge=(400, 412)))
    X3 = S.sc_s4(d3, "ABD", 15)
    kisa = (X3.ci & X3.cii & X3.ciii & (X3.run4 < E["S4"]["uzunluk"])).to_numpy()
    kontrol("12 günlük dar bölge: (i)-(iii) doğru ama run < 10 olan günlerde S4 yok; S4 günlerinde run >= 10",
            kisa.any() and not X3.s4c.to_numpy()[kisa].any() and (X3.run4[X3.s4c] >= 10).all(),
            f"run<10 aday gün {int(kisa.sum())}")

    # 5) geleceğe bakma
    G = S.sc_gecmis(d, "ABD")
    t = d.index[i + 2]
    kol = ["m", "qm", "bbw", "qb", "bbr", "net", "bant4", "asagi", "trp", "run4", "s4c", "ev4", "s4c_20", "ev4_20", "oran", "oran_20", "atr", "liq", "s1c"]
    G2 = S.sc_gecmis(d[d.index <= t], "ABD").iloc[-1][kol]
    a = pd.to_numeric(G.loc[t, kol], errors="coerce").astype(float).to_numpy(); b = pd.to_numeric(G2, errors="coerce").astype(float).to_numpy()
    kontrol("geleceğe bakma: seri t'de kesilince aynı", np.allclose(a, b, equal_nan=True, rtol=1e-9, atol=1e-12))
    db = d.copy(); db.iloc[i + 3:, :4] = db.iloc[i + 3:, :4] * 3.0
    G3 = S.sc_gecmis(db, "ABD").loc[t, kol]
    kontrol("geleceğe bakma: t'den sonrası bozulunca aynı", np.allclose(a, pd.to_numeric(G3, errors="coerce").astype(float).to_numpy(), equal_nan=True))
    V_ = {"A": d}
    Xp = pd.DataFrame({"sembol": ["A"], "tarih": [t]})
    kontrol("sc_gelecek_denetimi geçer", S.sc_gelecek_denetimi(V_, Xp, "ABD") == 1)

    # 6) sonuçlar
    dB = d.copy(); j = i + 5
    cp = dB.Close.iat[j - 1]
    dB.iloc[j, dB.columns.get_loc("High")] = cp * 1.12; dB.iloc[j, dB.columns.get_loc("Low")] = cp * 0.99
    dB.iloc[j, dB.columns.get_loc("Close")] = cp * 1.10; dB.iloc[j:, dB.columns.get_loc("Close")] = dB.Close.iloc[j:] * 1.0
    dB = _hz(dB)
    GB = S.sc_gecmis(dB, "ABD"); RB = S.sc_sonuc(dB, GB); SB = SY.sy_sonuc(dB, SY.sy_gecmis(dB, "ABD", SY.SY_ESIK), SY.SY_ESIK)
    kontrol("BH2 = SY B2, B1 = SY B1 (bütün barlar)", (RB.BH2.to_numpy() == SB.B2.to_numpy()).all() and (RB.B1.to_numpy() == SB.B1.to_numpy()).all())
    kontrol("k=2 varyantları k=3'ü kapsar", (RB.B1k2 | ~RB.B1).all() and (RB.BH2k2 | ~RB.BH2).all())
    kontrol("B1 zaman ve yön elle (t = büyük günden 3 önce)", bool(RB.B1.iat[j - 3]) and int(RB.k1.iat[j - 3]) == 3 and bool(RB.B1_up.iat[j - 3]) and bool(RB.f1.iat[j - 3]),
            f"k1 {RB.k1.iat[j - 3]}")

    # 7) panel + KAT elle
    V = {f"H{k}": _hz(_seri(tohum=10 + k, bolge=(400 + 7 * k, 440 + 7 * k))) for k in range(6)}
    V.update({f"Z{k}": _hz(_seri(tohum=40 + k)) for k in range(14)})
    P = S.sc_panel(V, "ABD")
    P["donem"] = np.where(P.tarih.dt.year <= 2022, "2016-22", "")
    P.loc[P.tarih.dt.year == 2017, "donem"] = "2023"     # sentetik: dönem etiketleri tarihten bağımsız sınanır
    TA, sat = S.sc_olc_A(P)
    X1 = sat["S4_es1"]
    kontrol("panelde S4 olayı var", int((P.uygun & P.ev4).sum()) >= 3, int((P.uygun & P.ev4).sum()))
    if len(X1):
        r0 = X1.iloc[0]
        es = P[(P.tarih == r0.tarih) & (P.hucA == r0.hucA) & P.uygun & ~P.s4c]
        kontrol("eş 1 ortalaması elle (aynı gün, aynı hücre, S4 dışı)", abs(es.B1.mean() - r0.es_B1) < 1e-12 and len(es) == r0.es_n)
        Y = X1[X1.donem == "2016-22"]
        k_ = TA[(TA.sikisma == "S4") & (TA.es == "es1") & (TA.olcu == "BH2") & (TA.donem == "2016-22")]
        if len(Y) and Y.es_BH2.sum() > 0:
            kontrol("KAT elle = Σ olay / Σ eş oranı", abs(k_.kat.iat[0] - Y.BH2.sum() / Y.es_BH2.sum()) < 1e-12)
    kontrol("KAT tablosu iki eş x dört tanım", set(TA.es) >= {"es1", "es2"} and set(TA.sikisma) >= {"S4", "S4_p20", "S4_supSY", "S1"})
    kontrol("sc_karar etiket üretir", "etiket" in S.sc_karar(TA)["B1"])
    # 8) (C) işlem
    tC, XC = S.sc_olc_C(P)
    kontrol("(C) SY.sy_olc_C S4 olaylarıyla çalışır", len(tC) == 4 and int(XC.shape[0]) == int((P.uygun_c & P.ev4).sum()))
    # 9) cetvel
    ol = P.loc[P.ev4, ["sembol", "tarih"]].copy(); ol["pazar"] = "ABD"
    Vd = OC._oc_veri_sar({k: v[["Open", "High", "Low", "Close", "Volume"]] for k, v in V.items()}, "ABD")
    So = OC.oc_olc(ol.reset_index(drop=True), {"ABD": Vd})
    kontrol("OC.oc_olc S4 olaylarıyla çalışır", "hucre" in So and len(So["hucre"]) == 3, So["etiket"]["genel"])
    # 10) mühür / ön kayıt
    with tempfile.TemporaryDirectory() as td:
        try:
            S.sc_onkayit_dogrula(os.path.join(td, "yok.md"), git=False); kontrol("ön kayıt yoksa durur", False)
        except S.SCHata:
            kontrol("ön kayıt yoksa durur", True)
        y = os.path.join(td, "ok.md")
        open(y, "w", encoding="utf-8").write(f"- MÜHÜR (SC_ESIK sha256): `{'0' * 64}`\n- KOD (SIKISMA_CEMAL.py sha256): `{'0' * 64}`\n"
                                            f"- SY_KOD (SIKISMA_YENIDEN.py sha256): `{'0' * 64}`\n- ZAMAN (UTC): `x`\n")
        try:
            S.sc_onkayit_dogrula(y, git=False); kontrol("mühür farkı durdurur", False)
        except S.SCHata as ex:
            kontrol("mühür farkı durdurur", "mühr" in str(ex))
        open(y, "w", encoding="utf-8").write(f"- MÜHÜR (SC_ESIK sha256): `{S.sc_esik_sha()}`\n- KOD (SIKISMA_CEMAL.py sha256): `{'0' * 64}`\n"
                                            f"- SY_KOD (SIKISMA_YENIDEN.py sha256): `{'0' * 64}`\n- ZAMAN (UTC): `x`\n")
        try:
            S.sc_onkayit_dogrula(y, git=False); kontrol("kod sha farkı durdurur", False)
        except S.SCHata as ex:
            kontrol("kod sha farkı durdurur", "sha256" in str(ex))
        # 11) kontrol kapısı
        import IZ_KARNE as IK
        k = os.path.join(td, "k.md"); open(k, "w", encoding="utf-8").write(S.sc_kontrol_tablosu())
        kontrol("kontrol kapısı ön kayıt tablosunu geçer", IK.ik_kontrol_kapisi(k)["gecti"])
        open(k, "w", encoding="utf-8").write("boş")
        try:
            IK.ik_kontrol_kapisi(k); kontrol("boş kontrol tablosu durur", False)
        except RuntimeError:
            kontrol("boş kontrol tablosu durur", True)
    # 12) FENER
    if os.path.isdir(S.SC_YOL["yahoo"]) or os.path.exists(os.path.join(S.SC_YOL["veri"], "V_BIST.pkl")):
        F = S.sc_fener()
        kay = [k for k, v in F.items() if isinstance(v, dict) and "asil" in v]
        kontrol("FENER: en az bir fiyat kaynağı okundu", len(kay) >= 1, kay)
        kontrol("FENER: 03-16.12.2025 (kayan, geniş BB) bölgesinde S4 YOK", all(F[k]["yanlis_tutar"] for k in kay))
        kontrol("FENER: S1 03-16.12.2025'te seçiyor (Cemal'in itirazı yeniden üretildi)", all(len(F[k]["yanlis"]["s1_gun"]) > 0 for k in kay))
        asil = {k: F[k]["asil_tutar"] for k in kay}
        # ön kayıttaki tanı: asıl bölgede S4 YOK, düşen koşul (iv) uzunluk ((i)&(ii) en uzun 3-4 gün); test bu tanının değişmediğini denetler
        run_max = {k: max(g["run"] for g in F[k]["asil"]["gunluk"]) for k in kay}
        iii_son = {k: all(g["iii"] for g in F[k]["asil"]["gunluk"][-3:]) for k in kay}
        kontrol("FENER: 14.10-07.11.2025 tanısı ön kayıtla aynı (S4 yok; (iv) uzunluk düşüyor, (iii) yatay son günlerde doğru)",
                all((not asil[k]) and run_max[k] < E["S4"]["uzunluk"] and iii_son[k] for k in kay), f"run_max {run_max}")
    else:
        print("ATLANDI FENER (veri yok)")
    # 13) e-posta / anahtar
    desen = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    dosyalar = [os.path.join(KOK, "SIKISMA_CEMAL.py"), os.path.join(KOK, "test_sikisma_cemal.py")]
    kl = S.SC_YOL["cikti"]
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
