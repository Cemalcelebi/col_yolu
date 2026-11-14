"""SIKISMA_YENIDEN testleri (yalnız SENTETİK veri; gerçek veride sonuç ölçmez). Çalıştırma: python test_sikisma_yeniden.py

1) çakışma kapısı  2) sıkışma tespiti (S1: oynak geçmiş + 12 gün dar mum/bant -> koşul doğru; bant geniş -> yanlış; 20 bar ara)
3) B1 tanımı (3 x ATR250% eşiği; ilk büyük gün; 2,5 kat büyük gün B1 değil)  4) kontrol eşlemesi (aynı gün, aynı hücre, olay dışı; elle ortalama)
5) GELECEĞE BAKMA: seri t'de kesilince geçmiş özellikler ve tespit aynı; t'den sonrası bozulunca da aynı  6) (C) işlem: uzun kırılım + stop
elle hesap, kısa kırılım 20 gün çıkış elle hesap  7) bölünme şüphesi (2:1 bölünme yakalanır, geri dönen sıçrama yakalanmaz)
8) mühür + ön kayıt doğrulama (mühür farkı / kod farkı / git'e işlenmemiş -> SYHata)  9) kontrol kapısı ön kayıt tablosunu geçer, boş tablo durur
10) uçtan uca sentetik kos (git kapısı kapalı) + rapor  11) e-posta / anahtar yok.
12) DUYARLILIK: p=10 = Ç174 S1; ATR250 / ATR60 / ATR_sik / ilk 20-5 gün en büyük mum elle; k x REF sayımı; p=20 / 40 pencere tespiti; kesme testi;
    BH; uçtan uca sentetik (Ç174 tutarlılık, satır CSV'sinden KAT, ham panelden eş ortalaması, grafik anahtarı 40 / 20, aynı gün eş, PNG / PDF determinizm).
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import SIKISMA_YENIDEN as S  # noqa: E402

E = S.SY_ESIK


def _seri(n=420, tohum=1, sikis=None, buyuk=None, buyuk_kat=5.0):
    """Oynak (günlük ~%2) seri; sikis=(a,b) aralığında dar mum ve sabit kapanış; buyuk=gün: o gün aralık buyuk_kat x ATR."""
    rng = np.random.default_rng(tohum)
    idx = pd.bdate_range("2016-01-04", periods=n)
    C = 100 * np.exp(np.cumsum(rng.normal(0, 0.02, n)))
    H = C * (1 + np.abs(rng.normal(0.012, 0.004, n))); L = C * (1 - np.abs(rng.normal(0.012, 0.004, n)))
    if sikis:
        a, b = sikis
        C[a:b] = C[a - 1]
        H[a:b] = C[a:b] * 1.001; L[a:b] = C[a:b] * 0.999
        C[b:] = C[b:] / C[b] * C[a - 1]; H[b:] = H[b:] / C[b] * C[b] if False else C[b:] * (1 + np.abs(rng.normal(0.012, 0.004, n - b)))
        L[b:] = C[b:] * (1 - np.abs(rng.normal(0.012, 0.004, n - b)))
    O = np.r_[C[0], C[:-1]]
    H = np.fmax(H, np.fmax(O, C)); L = np.fmin(L, np.fmin(O, C))
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(1e5, 2e5, n).astype(float)}, index=idx)
    if buyuk is not None:
        G = S.sy_gecmis(S.sy_veri_hazirla(d, E), "ABD", E)
        atr = G.atr.iat[buyuk - 1]
        cp = d.Close.iat[buyuk - 1]
        d.iloc[buyuk, d.columns.get_loc("High")] = cp * (1 + buyuk_kat * atr * 0.6)
        d.iloc[buyuk, d.columns.get_loc("Low")] = cp * (1 - buyuk_kat * atr * 0.4)
        d.iloc[buyuk, d.columns.get_loc("Open")] = cp; d.iloc[buyuk, d.columns.get_loc("Close")] = cp
    return d


def testler():
    hata = []
    # 1) çakışma kapısı
    g = {"sy_kos": lambda: None, "__name__": "x"}
    try:
        exec(compile(open(os.path.join(KOK, "SIKISMA_YENIDEN.py"), encoding="utf-8").read(), "SIKISMA_YENIDEN.py", "exec"), g)
        hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "x"}
    src = compile(open(os.path.join(KOK, "SIKISMA_YENIDEN.py"), encoding="utf-8").read(), "SIKISMA_YENIDEN.py", "exec")
    try:
        exec(src, g2); exec(src, g2)
    except RuntimeError as ex:
        hata.append(f"1) aynı dosyanın yeniden yüklenmesi durdu: {ex}")

    # 2) sıkışma tespiti
    d = S.sy_veri_hazirla(_seri(sikis=(300, 330)), E)
    G = S.sy_gecmis(d, "ABD", E)
    if not G.s1c.iloc[309:330].all():
        hata.append(f"2) dar bölgede S1 koşulu doğru değil: {G.s1c.iloc[305:331].tolist()}")
    if G.s1c.iloc[270:299].any():
        hata.append("2) oynak bölgede S1 koşulu doğru")
    ev = np.where(G.ev1.to_numpy())[0]
    ilk = int(np.argmax(G.s1c.to_numpy()))
    if not (len(ev) >= 1 and ev[0] == ilk and 300 <= ilk <= 309 and all(np.diff(ev) >= 20) and (len(ev) < 2 or ev[1] == ilk + 20)):
        hata.append(f"2) olay günü / 20 bar ara yanlış: {ev[:5]}")
    if G.run.iat[320] != 320 - ilk + 1:
        hata.append(f"2) süre (run) yanlış: {G.run.iat[320]}")
    d2 = d.copy(); d2.iloc[300:330, d2.columns.get_loc("Close")] *= np.where(np.arange(30) % 2, 1.04, 0.96)
    d2["High"] = np.fmax(d2.High, d2.Close); d2["Low"] = np.fmin(d2.Low, d2.Close)
    G2 = S.sy_gecmis(d2, "ABD", E)
    if G2.s1c.iloc[300:330].any():
        hata.append("2) bant %8 iken (ABD eşiği %6) S1 doğru çıktı")

    # 3) B1 tanımı
    d = S.sy_veri_hazirla(_seri(sikis=(300, 330), buyuk=315, buyuk_kat=5.0), E)
    G = S.sy_gecmis(d, "ABD", E); R = S.sy_sonuc(d, G, E)
    i = 309
    tr = (d.High.iat[315] - d.Low.iat[315]) / d.Close.iat[314]
    if not (R.B1.iat[i] and R.k1.iat[i] == 6):
        hata.append(f"3) B1/k1 yanlış: B1 {R.B1.iat[i]} k1 {R.k1.iat[i]} (tr {tr:.4f}, 3xATR {3 * G.atr.iat[i]:.4f})")
    if not (R.B1_5.iat[312] and not R.B1_5.iat[i]):
        hata.append("3) B1_5 penceresi yanlış")
    d = S.sy_veri_hazirla(_seri(sikis=(300, 330), buyuk=315, buyuk_kat=2.5), E)
    G = S.sy_gecmis(d, "ABD", E); R = S.sy_sonuc(d, G, E)
    if R.B1.iat[309]:
        hata.append("3) 2,5 x ATR günü B1 sayıldı")
    if not R.B0.iat[309]:
        hata.append("3) B0 (göreli) dar bölgede doğru olmalı")

    # 4) kontrol eşlemesi
    P = pd.DataFrame({"tarih": pd.to_datetime(["2020-01-02"] * 6 + ["2020-01-03"] * 3), "hucA": [1, 1, 1, 2, 2, 1, 1, 1, 1],
                      "B1": [1, 0, 1, 1, 0, 1, 1, 0, 0], "olay": [1, 0, 0, 0, 0, 0, 1, 0, 0]})
    P["olay"] = P.olay.astype(bool)
    X = S.sy_es_ortalama(P, P.olay, ~P.olay, "hucA", ["B1"])
    if not (abs(X.es_B1.iat[0] - 2 / 3) < 1e-12 and X.es_n.iat[0] == 3 and X.es_B1.iat[1] == 0 and X.es_n.iat[1] == 2):
        hata.append(f"4) eş ortalaması yanlış: {X[['es_B1', 'es_n']].values.tolist()}")
    k, a, b = S.sy_oran_boot(np.array([1, 0, 1.0]), np.array([0.5, 0.5, 0.5]), np.array(["a", "a", "b"]), E)
    if abs(k - 2 / 1.5) > 1e-12 or not (a <= k <= b):
        hata.append("4) KAT / bootstrap yanlış")

    # 5) geleceğe bakma
    d = S.sy_veri_hazirla(_seri(n=500, tohum=3, sikis=(300, 330)), E)
    Gt = S.sy_gecmis(d, "ABD", E)
    kol = ["atr", "sig", "m10", "p20", "band", "s1c", "s2c", "s3c", "run", "dusus", "liq", "mom", "vk", "ev1", "ev2", "ev3"]
    for t in (280, 309, 315, 331, 400):
        a1 = Gt.iloc[t][kol].astype(float).to_numpy(); a2 = S.sy_gecmis(d.iloc[:t + 1], "ABD", E).iloc[-1][kol].astype(float).to_numpy()
        d3 = d.copy(); d3.iloc[t + 1:] = d3.iloc[t + 1:] * np.random.default_rng(t).uniform(0.5, 2, (len(d3) - t - 1, 1))
        a3 = S.sy_gecmis(d3, "ABD", E).iloc[t][kol].astype(float).to_numpy()
        if not (np.allclose(a1, a2, equal_nan=True) and np.allclose(a1, a3, equal_nan=True)):
            hata.append(f"5) geleceğe bakma: t={t} geçmiş özellik geleceğe bağlı")

    # 6) (C) işlem
    idx = pd.bdate_range("2020-01-01", periods=80)
    C = np.full(80, 100.0); C[30] = 101.5     # t=20: bant 100-100; j=10 -> C=101,5 > 101 -> uzun; giriş Open[31]
    O = C.copy(); O[31] = 102.0; H = C + 0.5; L = C - 0.5; H[31] = 103; L[31] = 101.6
    C[31:] = 102.5; O[32:] = 102.5; H[32:] = 103.0; L[32:] = 102.0
    L[36] = 99.0; O[36] = 102.5   # gün içi stop 100'de
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1e5, "Kur": 1.0}, index=idx)
    G = pd.DataFrame({"hi10": pd.Series(C).rolling(10).max().to_numpy(), "lo10": pd.Series(C).rolling(10).min().to_numpy()}, index=idx)
    T = S.sy_islem(d, G, E)
    t = 20
    if not (T.c_yon.iat[t] == 1 and abs(T.c_r.iat[t] - (100 / 102 - 1)) < 1e-12 and T.c_giris.iat[t] == idx[31] and T.c_cikis.iat[t] == idx[36]):
        hata.append(f"6) uzun işlem yanlış: yon {T.c_yon.iat[t]} r {T.c_r.iat[t]} giriş {T.c_giris.iat[t]} çıkış {T.c_cikis.iat[t]}")
    C = np.full(80, 100.0); C[25:] = 98.0      # t=20: j=5 -> 98 < 99 -> kısa; giriş Open[26]=98; 20 bar sonra C[45]=95
    C[40:] = 95.0
    O = C.copy(); H = C + 0.3; L = C - 0.3
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": 1e5, "Kur": 1.0}, index=idx)
    G = pd.DataFrame({"hi10": pd.Series(C).rolling(10).max().to_numpy(), "lo10": pd.Series(C).rolling(10).min().to_numpy()}, index=idx)
    T = S.sy_islem(d, G, E)
    if not (T.c_yon.iat[t] == -1 and abs(T.c_r.iat[t] - (1 - 95 / 98)) < 1e-12 and T.c_cikis.iat[t] == idx[26 + 19]):
        hata.append(f"6) kısa işlem yanlış: yon {T.c_yon.iat[t]} r {T.c_r.iat[t]} çıkış {T.c_cikis.iat[t]}")
    if not (T.c_ilk10.iat[t] == 0 and T.c_ilk20.iat[t] == 0):
        hata.append("6) P(+20/-10 önce) bayrakları yanlış")
    if T.c_ok.iat[60]:
        hata.append("6) 41 bar geleceği olmayan gün c_ok")

    # 7) bölünme şüphesi
    C = np.r_[np.full(50, 100.0), np.full(50, 50.0)]
    if not S.sy_bolunme_supheli(C, E)[50]:
        hata.append("7) 2:1 bölünme yakalanmadı")
    C = np.r_[np.full(50, 100.0), [140.0], np.full(49, 100.0)]
    if S.sy_bolunme_supheli(C, E).any() or S.sy_bolunme_supheli(C, E, kati=True).any():
        hata.append("7) geri dönen sıçrama şüpheli sayıldı")
    C = np.r_[np.full(50, 100.0), np.full(50, 137.0)]
    if S.sy_bolunme_supheli(C, E).any() or not S.sy_bolunme_supheli(C, E, kati=True)[50]:
        hata.append("7) kalıcı %37 sıçrama: ANA şüpheli saymamalı, KATI saymalı")

    # 8) mühür + ön kayıt doğrulama
    with tempfile.TemporaryDirectory() as tmp:
        try:
            S.sy_onkayit_dogrula(os.path.join(tmp, "yok.md"), git=False)
            hata.append("8) ön kayıt yokken durmadı")
        except S.SYHata:
            pass
        yol = os.path.join(tmp, "ok.md")
        kod = S._sy_sha_dosya(S.SY_YOL["kod"])
        open(yol, "w", encoding="utf-8").write(f"- MÜHÜR (SY_ESIK sha256): `{'0' * 64}`\n- KOD (SIKISMA_YENIDEN.py sha256): `{kod}`\n- ZAMAN (UTC): `x`\n")
        try:
            S.sy_onkayit_dogrula(yol, git=False); hata.append("8) mühür farkında durmadı")
        except S.SYHata:
            pass
        open(yol, "w", encoding="utf-8").write(f"- MÜHÜR (SY_ESIK sha256): `{S.sy_esik_sha()}`\n- KOD (SIKISMA_YENIDEN.py sha256): `{'1' * 64}`\n- ZAMAN (UTC): `x`\n")
        try:
            S.sy_onkayit_dogrula(yol, git=False); hata.append("8) kod sha farkında durmadı")
        except S.SYHata:
            pass
        open(yol, "w", encoding="utf-8").write(f"- MÜHÜR (SY_ESIK sha256): `{S.sy_esik_sha()}`\n- KOD (SIKISMA_YENIDEN.py sha256): `{kod}`\n- ZAMAN (UTC): `x`\n")
        try:
            S.sy_onkayit_dogrula(yol, git=False)
        except S.SYHata as ex:
            hata.append(f"8) doğru ön kayıt reddedildi: {ex}")
        try:
            S.sy_onkayit_dogrula(yol, git=True); hata.append("8) git'e işlenmemiş ön kayıtta durmadı")
        except S.SYHata:
            pass
        E2 = json.loads(json.dumps(E)); E2["B"]["b1_kat"] = 2.5
        if S.sy_esik_sha(E2) == S.sy_esik_sha():
            hata.append("8) eşik değişince mühür değişmedi")

        # 9) kontrol kapısı
        import IZ_KARNE as IK
        k = os.path.join(tmp, "k.md")
        open(k, "w", encoding="utf-8").write(S.sy_kontrol_tablosu())
        try:
            IK.ik_kontrol_kapisi(k)
        except RuntimeError as ex:
            hata.append(f"9) dolu kontrol tablosu kapıdan geçmedi: {ex}")
        open(k, "w", encoding="utf-8").write(IK.ik_kontrol_tablosu() if hasattr(IK, "ik_kontrol_tablosu") else "| K1 | x | | |")
        try:
            IK.ik_kontrol_kapisi(k); hata.append("9) boş kontrol tablosu kapıdan geçti")
        except RuntimeError:
            pass

        # 10) uçtan uca sentetik kos
        veri = os.path.join(tmp, "veri"); os.makedirs(veri)
        for p in S.SY_PAZAR:
            V = {}
            for j in range(120):
                n = 2900
                rng = np.random.default_rng(100 + j + 1000 * S.SY_PAZAR.index(p))
                idx = pd.bdate_range("2015-06-01", periods=n)
                dus = np.zeros(n, bool); i_ = 0
                while i_ < n:                       # düşük oynaklık rejimleri (~30 gün), çıkışta sıçrama
                    if rng.random() < 0.01:
                        L_ = int(rng.integers(15, 45)); dus[i_:i_ + L_] = True; i_ += L_
                    i_ += 1
                vol = np.where(dus, 0.003, 0.02)
                r = rng.normal(0, vol); r[rng.random(n) < 0.01] *= 8
                cik = np.where(dus[:-1] & ~dus[1:])[0] + 1
                r[cik] = rng.choice([-1, 1], len(cik)) * 0.12
                C = 50 * np.exp(np.cumsum(r)); O = np.r_[C[0], C[:-1]]
                H = np.fmax(O, C) * (1 + np.abs(rng.normal(0, vol / 2))) + 1e-6; L = np.fmin(O, C) * (1 - np.abs(rng.normal(0, vol / 2)))
                d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(1e4, 1e6, n).astype(float)}, index=idx)
                if p == "AVR":
                    d["Kur"] = 1.1
                V[f"S{j}"] = d
            pd.to_pickle(V, os.path.join(veri, f"V_{p}.pkl"))
        cikti = os.path.join(tmp, "cikti"); satir = os.path.join(tmp, "satir")
        try:
            yol = S.sy_onkayit_yaz(cikti, veri)
            m = open(yol, encoding="utf-8").read()
            for c in ("## Olay SAYIMI", "MÜHÜR", "## KONTROL LİSTESİ"):
                if c not in m:
                    hata.append(f"10) ön kayıtta '{c}' yok")
            if re.search(r"\| (B1|P\(B1)", m.split("## Olay SAYIMI")[1].split("## Sınırlar")[0]):
                hata.append("10) ön kayıt sayımında sonuç sütunu var")
            R = S.sy_kos(cikti, veri, git=False, satir=satir)
            if not os.path.exists(os.path.join(cikti, "SIKISMA_RAPOR.md")) or "DÜZ DİL ÖZET" not in R["rapor"]:
                hata.append("10) rapor yazılmadı")
            A = pd.DataFrame(R["sonuc"]["A"])
            # yeniden üretim: satır CSV'sinden bir hücre
            X = pd.read_csv(os.path.join(satir, "olay_A_ABD.csv.gz"), parse_dates=["tarih"])
            Y = X[X.donem == "2016-22"]
            kat = Y.B1.sum() / Y.es_B1.sum()
            a = A[(A.pazar == "ABD") & (A.donem == "2016-22") & (A.sikisma == "S1") & (A.olcu == "B1")]
            if not (len(a) and abs(a.kat.iat[0] - kat) < 1e-9):
                hata.append("10) satır CSV'sinden KAT yeniden üretilemedi")
            TC = pd.DataFrame(R["sonuc"]["C"])
            if len(TC) != 12 or not (TC.n > 0).all():
                hata.append("10) C tablosu 3 pazar x 4 dönem değil ya da boş hücre var")
            if not all(len(b["model"]) == 3 and "skill" in b["model"][0] for b in R["sonuc"]["B"]):
                hata.append("10) (B) model sonuçları eksik")
            k1 = A[(A.sikisma == "S1") & (A.olcu == "B1") & (A.donem == "2023+")]
            if not (k1.n > 0).all():
                hata.append("10) 2023+ hücresi boş")
            S.sy_rapor(cikti)
        except Exception as ex:
            import traceback
            hata.append(f"10) uçtan uca koşu hata: {ex}\n{traceback.format_exc()}")

        # 12d) DUYARLILIK uçtan uca (sentetik): ön kayıt, kontrol kapısı, Ç174 tutarlılık, satır CSV'sinden yeniden üretim, grafik anahtarı, determinizm
        try:
            dyol = S.sy_duy_onkayit_yaz(cikti, veri)
            m = open(dyol, encoding="utf-8").read()
            for c in ("MÜHÜR (SY_DUY sha256)", "## Olay SAYIMI", "## KONTROL LİSTESİ"):
                if c not in m:
                    hata.append(f"12d) duyarlılık ön kaydında '{c}' yok")
            if re.search(r"KAT|p_olay", m.split("## Olay SAYIMI")[1].split("## Sınırlar")[0]):
                hata.append("12d) duyarlılık ön kayıt sayımında sonuç sütunu var")
            IK.ik_kontrol_kapisi(dyol)
            png = os.path.join(tmp, "png"); dsat = os.path.join(tmp, "dsatir")
            R = S.sy_duy_kos(cikti, veri, git=False, satir=dsat, c174=os.path.join(cikti, "sikisma_sonuc.json"), png_kl=png)
            T = pd.DataFrame(R["sonuc"]["kat"])
            if len(T) != 5 * 3 * 2 * 4 * 2 * 3 * 4:
                hata.append(f"12d) KAT tablosu satır sayısı {len(T)} (2880 olmalı)")
            if len(R["sonuc"]["c174_tutarlilik"]) < 9 or max(x["fark"] for x in R["sonuc"]["c174_tutarlilik"]) > 1e-9:
                hata.append("12d) Ç174 tutarlılık denetimi eksik / tutmadı")
            X = pd.read_csv(os.path.join(dsat, "duy_olay_ABD_p20_es2.csv.gz"), parse_dates=["tarih"])
            Y = X[X.donem == "2016-22"]; c = "b_ATR60_2.5_20"
            kat = Y[c].sum() / Y["es_" + c].sum()
            a = T[(T.pazar == "ABD") & (T.p == 20) & (T.es == "es2") & (T.donem == "2016-22") & (T.ref == "ATR60") & (T.k == 2.5) & (T.ufuk == "20")]
            if not (len(a) == 1 and len(Y) == a.n.iat[0] and abs(a.kat.iat[0] - kat) < 1e-9):
                hata.append("12d) satır CSV'sinden duyarlılık KAT'ı yeniden üretilemedi")
            # eş ortalaması elle (ham panel): bir olay
            Pn = pd.read_pickle(os.path.join(dsat, "duy_panel_ABD_p10.pkl"))
            r0 = pd.read_csv(os.path.join(dsat, "duy_olay_ABD_p10_es1.csv.gz"), parse_dates=["tarih"]).iloc[0]
            es_ = Pn[(Pn.tarih == r0.tarih) & (Pn.hucA == r0.hucA) & ~Pn.s10]
            el = float((es_.mx20 >= 2.0 * es_.atr).mean())
            if not (len(es_) == r0.es_n and abs(el - r0["es_b_ATR250_2_20"]) < 1e-12):
                hata.append("12d) eş ortalaması ham panelden elle tutmadı")
            A_ = json.load(open(os.path.join(cikti, "ornek_anahtar.json"), encoding="utf-8"))
            g = A_["grafik"]
            if not (len(g) == 40 and sorted(x["numara"] for x in g) == list(range(1, 41)) and sum(x["tip"] == "olay" for x in g) == 20):
                hata.append("12d) grafik anahtarı 40 / 20 olay / 1-40 numara değil")
            ol = sorted((x["tarih"]) for x in g if x["tip"] == "olay"); es2 = sorted((x["tarih"]) for x in g if x["tip"] == "eş")
            if ol != es2 or any(x["tarih"] < "2023-01-01" for x in g):
                hata.append("12d) eşler olaylarla aynı günlerden değil ya da 2023 öncesi grafik var")
            for ad_, h_ in A_["dosya"]["png_sha256"].items():
                if S._sy_sha_dosya(os.path.join(png, ad_)) != h_:
                    hata.append(f"12d) {ad_} sha anahtarla tutmuyor")
            V_ = S.sy_veri_yukle("ABD", E, veri)
            g2 = S.sy_duy_grafikler(V_, g, os.path.join(tmp, "tekrar.pdf"), os.path.join(tmp, "png2"))
            if g2["png_sha256"] != A_["dosya"]["png_sha256"] or g2["pdf_sha256"] != A_["dosya"]["pdf_sha256"]:
                hata.append("12d) grafikler deterministik değil (ikinci çizim farklı)")
            if "DÜZ DİL ÖZET" not in R["rapor"] or "Göz ne görür" not in R["rapor"]:
                hata.append("12d) duyarlılık raporu eksik")
        except Exception as ex:
            import traceback
            hata.append(f"12d) duyarlılık uçtan uca hata: {ex}\n{traceback.format_exc()}")

    # 12) DUYARLILIK birim testleri
    D = S.SY_DUY
    d = S.sy_veri_hazirla(_seri(n=460, tohum=5, sikis=(300, 330), buyuk=335, buyuk_kat=2.2), E)
    G0 = S.sy_gecmis(d, "ABD", E); G = S.sy_duy_gecmis(d, "ABD"); R = S.sy_duy_sonuc(d)
    if not ((G.s10.to_numpy() == G0.s1c.to_numpy()).all() and (G.e10.to_numpy() == G0.ev1.to_numpy()).all()):
        hata.append("12a) p=10 sıkışma / olay Ç174 S1 ile aynı değil")
    t = 329
    H_, L_, C_ = (d[c].to_numpy(float) for c in ("High", "Low", "Close")); Cp = np.r_[np.nan, C_[:-1]]
    trc = (np.fmax(H_, Cp) - np.fmin(L_, Cp)) / Cp
    atr = trc[t - 249:t + 1].mean(); a60 = trc[t - 70:t - 10].mean(); msik = trc[t - 9:t + 1].mean(); mx = trc[t + 1:t + 21].max()
    if not (abs(G.atr.iat[t] - atr) < 1e-12 and abs(G.a60_10.iat[t] - a60) < 1e-12 and abs(G.m10.iat[t] - msik) < 1e-12 and abs(R.mx20.iat[t] - mx) < 1e-12
            and abs(R.mx5.iat[t] - trc[t + 1:t + 6].max()) < 1e-12):
        hata.append("12a) ATR250 / ATR60 (t-70..t-11) / ATR_sik / mx20 / mx5 elle hesapla tutmadı")
    if not (mx >= 2 * atr and mx < 2.5 * atr):
        hata.append(f"12a) sentetik büyük gün beklenen aralıkta değil ({mx / atr:.2f} x ATR250)")
    if not (R.mx5.iat[t] < 1.5 * atr):
        hata.append("12a) ilk 5 gün penceresi 6. günü saydı")
    # k x REF sayımı (sy_duy_olc'un kullandığı ifade): 2 x ATR250 doğru, 2,5 x yanlış
    if not ((R.mx20.iat[t] >= 2.0 * G.atr.iat[t]) and not (R.mx20.iat[t] >= 2.5 * G.atr.iat[t])):
        hata.append("12a) k x REF sayımı yanlış")
    # 12b) pencere 20 / 40 tespiti: 60 günlük dar bölge
    d = S.sy_veri_hazirla(_seri(n=520, tohum=7, sikis=(330, 390)), E)
    G = S.sy_duy_gecmis(d, "ABD")
    # sentetik: 330-389 dar bölge (60 gün). p gün ortalaması tek gün dağılımının %20'siyle kıyaslandığı için koşul dar bölgenin içinde, p dolmadan da doğru olabilir.
    for p_, tam in ((20, 349), (40, 369), (60, 389)):
        if not (G[f"s{p_}"].iloc[tam:390].all() and not G[f"s{p_}"].iloc[280:330].any()):
            hata.append(f"12b) p={p_} tespiti yanlış (dar bölge tam pencerede doğru, öncesinde yanlış olmalı)")
    e20 = np.where(G.e20.to_numpy())[0]
    if not (len(e20) and 330 <= e20[0] <= 349 and all(np.diff(e20) >= 20)):
        hata.append(f"12b) p=20 olay günü / 20 bar ara yanlış: {e20[:4]}")
    if G.s20.iloc[:270].any() or G.s60.iloc[:310].any():
        hata.append("12b) 250 + p bar geçmiş olmadan sıkışma doğru")
    # 12c) geleceğe bakma (duyarlılık geçmiş özellikleri)
    for t in (340, 371, 389, 450):
        a1 = G.iloc[t].astype(float).to_numpy(); a2 = S.sy_duy_gecmis(d.iloc[:t + 1], "ABD").iloc[-1].astype(float).to_numpy()
        d3 = d.copy(); d3.iloc[t + 1:] = d3.iloc[t + 1:] * np.random.default_rng(t).uniform(0.5, 2, (len(d3) - t - 1, 1))
        a3 = S.sy_duy_gecmis(d3, "ABD").iloc[t].astype(float).to_numpy()
        if not (np.allclose(a1, a2, equal_nan=True) and np.allclose(a1, a3, equal_nan=True)):
            hata.append(f"12c) geleceğe bakma: duyarlılık t={t}")
    # BH ve bootstrap
    Tb = pd.DataFrame({"ref": ["ATR250"] * 4 + ["ATR_sik"], "donem": ["2023"] * 5, "p_boot": [0.001, 0.02, 0.5, 0.9, 0.0005]})
    bh = S.sy_duy_bh(Tb)
    if not (bh.iloc[:4].tolist() == [True, True, False, False] and pd.isna(bh.iat[4])):
        hata.append(f"12) BH yanlış: {bh.tolist()}")
    bt = S._sy_duy_boot(np.array([[1, 0], [0, 0], [1, 1.0]]), np.array([[.5, .5], [.5, .5], [.5, .5]]), np.array(["a", "a", "b"]), D, 0)
    if not (abs(bt["kat"][0] - 2 / 1.5) < 1e-12 and abs(bt["kat"][1] - 1 / 1.5) < 1e-12 and (bt["alt"] <= bt["kat"]).all()):
        hata.append("12) duyarlılık bootstrap KAT yanlış")
    if S.sy_duy_sha() == S.sy_esik_sha():
        hata.append("12) duyarlılık mührü Ç174 mührüyle aynı")
    if D["c174_muhur"] != S.sy_esik_sha():
        hata.append("12) SY_DUY c174_muhur Ç174 SY_ESIK mührüyle aynı değil")

    # 11) e-posta / anahtar yok
    for ad in ("SIKISMA_YENIDEN.py", "test_sikisma_yeniden.py"):
        s_ = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if S._SY_EPOSTA.findall(s_) or re.search(r"(api[_-]?key|token|secret|password)\s*=\s*['\"][A-Za-z0-9]{12,}", s_, re.I):
            hata.append(f"11) {ad} içinde e-posta / anahtar var")
    return hata


if __name__ == "__main__":
    Hh = testler()
    if Hh:
        print("SIKISMA TEST: HATA", len(Hh)); print("\n".join(Hh)); sys.exit(1)
    print("SIKISMA TEST: 12/12 bölüm GEÇTİ (12: duyarlılık)")
