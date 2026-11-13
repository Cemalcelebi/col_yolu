"""GENIS_KESIT testleri — YALNIZ SENTETİK veri (ağ yok; gerçek ölçüm yok). Çalıştırma: python test_genis_kesit.py

1) Spearman: tekdüze = +1 / -1, eşitlik ortalama sıra, eksik değer dışarıda; permütasyon p tohumla birebir, güçlü ilişkide küçük, bağımsızda büyük
2) Benjamini-Hochberg: elle örnek (anlamlılar ve q-değerleri)
3) sınanabilirlik: < 20 değer, tek değer, ikili küçük grup < 5 -> sınanmaz; yarı farkı elle
4) istatistik tablosu: güçlü ve Y2 ile aynı yönlü özellik ADAY, gürültü değil, ters yönlü Y2 aday değil
5) derinlik-2 ağaç: ayrılabilir veride doğru eşik, yaprak en az 5; LOO doğruluk yüksek; gürültüde %50 civarı
6) metin kuralları: yüzde okuma, şirket adı anahtarı, tasfiye / Ziraat fonu, ortak mı, leke cümlesi + olumsuzlama, alım yönü, %5 eşiğine ulaşma
   (mevzuat alıntısı sayılmaz), geri alım program özeti, finansal rapor özkaynağı, şirket sayfası endeks listesi
7) eşik tablosu ayrıştırma: kod sütunlu / sütunsuz satır, fon payı (Rehber 9.8) satırı atılır, yayın zamanı eşlenir
8) GELECEĞE BAKMA kapısı: kesim sonrası tarih durdurur; fiyat kesimde kesilir
9) sonuç değişkenleri: Y1, Y2 (tavan sayısı), Y3 elle
10) ön kayıt kapısı: yok -> RET; git'te değil -> RET; commit sonrası geçer; eşik değişince RET; X sha farkı RET; kod farkı sapmasız RET
11) çakışma kapısı; kodda e-posta yok; yasak defter dosyalarına yazan kod yok; e-posta içeren metin yazılmaz
"""
from __future__ import annotations

import copy
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import GENIS_KESIT as G  # noqa: E402

HATA: list = []


def kontrol(kosul: bool, mesaj: str) -> None:
    if not kosul:
        HATA.append(mesaj)


def durmali(f, mesaj: str, parca: str) -> None:
    try:
        f()
        HATA.append(mesaj)
    except (G.GkHata, RuntimeError) as ex:
        kontrol(parca in str(ex), f"{mesaj} (yanlış neden: {ex})")


def t1_spearman() -> None:
    x = np.arange(30.0)
    kontrol(abs(G.gk_spearman(x, x ** 3) - 1) < 1e-12 and abs(G.gk_spearman(x, -x) + 1) < 1e-12, "1: tekdüze ilişki +1 / -1 olmalı")
    kontrol(np.allclose(G.gk_sira(np.array([3.0, 1.0, 3.0, 2.0])), [3.5, 1.0, 3.5, 2.0]), "1: eşitlikte ortalama sıra")
    a = np.array([1.0, 2.0, np.nan, 4.0, 5.0]); b = np.array([2.0, 1.0, 9.0, 4.0, 3.0])
    m = np.isfinite(a)
    kontrol(abs(G.gk_spearman(a, b) - G.gk_spearman(a[m], b[m])) < 1e-12, "1: eksik değer dışarıda kalmalı")
    # elle: x = 1..5, y = 2,1,4,3,5 -> d^2 = 1+1+1+1+0 = 4; rho = 1 - 6*4/(5*24) = 0.8
    kontrol(abs(G.gk_spearman([1, 2, 3, 4, 5], [2, 1, 4, 3, 5]) - 0.8) < 1e-12, "1: elle rho 0,8 tutmuyor")
    rng = np.random.default_rng(1); u = rng.normal(size=64); v = u + rng.normal(scale=0.3, size=64); w = rng.normal(size=64)
    r1, p1 = G.gk_perm_p(u, v, 2000, 7); r1b, p1b = G.gk_perm_p(u, v, 2000, 7)
    kontrol(r1 > 0.8 and p1 < 0.002 and (r1, p1) == (r1b, p1b), f"1: güçlü ilişkide p küçük ve tohumla aynı olmalı ({r1}, {p1})")
    _, p2 = G.gk_perm_p(u, w, 2000, 7)
    kontrol(p2 > 0.05, f"1: bağımsız seride p büyük olmalı ({p2})")
    kontrol(np.isnan(G.gk_perm_p(np.ones(10), np.arange(10.0), 100, 1)[0]), "1: sabit X'te rho tanımsız")


def t2_bh() -> None:
    p = [0.01, 0.04, 0.03, 0.20, 0.50]
    B = G.gk_bh(p, 0.10)
    # sıralı: 0.01 (1), 0.03 (2), 0.04 (3), 0.20 (4), 0.50 (5); eşik q*i/n = 0.02, 0.04, 0.06, 0.08, 0.10 -> ilk üçü anlamlı
    kontrol(B[0].tolist() == [1.0, 1.0, 1.0, 0.0, 0.0], f"2: BH anlamlılar yanlış {B[0]}")
    # q (sıralı): 0.05, min(0.075, 0.0667) = 0.0667, 0.0667, 0.25, 0.5 -> özgün sıraya: 0.01 -> 0.05, 0.04 -> 0.0667, 0.03 -> 0.0667
    kontrol(np.allclose(B[1], [0.05, 1 / 15, 1 / 15, 0.25, 0.5]), f"2: BH q-değerleri yanlış {B[1]}")
    kontrol(G.gk_bh([0.5, 0.6], 0.10)[0].sum() == 0, "2: hiçbir şey anlamlı olmamalı")


def t3_sinanir() -> None:
    kontrol(not G.gk_sinanir_mi(pd.Series([1.0] * 10 + [np.nan] * 54))[0], "3: < 20 değer sınanmamalı")
    kontrol(not G.gk_sinanir_mi(pd.Series([1.0] * 64))[0], "3: tek değerli sınanmamalı")
    kontrol(not G.gk_sinanir_mi(pd.Series([1] * 4 + [0] * 60))[0], "3: ikili küçük grup 4 sınanmamalı")
    kontrol(G.gk_sinanir_mi(pd.Series([1] * 5 + [0] * 59))[0], "3: ikili küçük grup 5 sınanmalı")
    x = pd.Series([0, 0, 1, 1]); y = pd.Series([1.0, 3.0, 5.0, 9.0])
    kontrol(abs(G.gk_yari_fark(x, y) - (7.0 - 2.0)) < 1e-12, "3: ikili yarı farkı elle")
    x2 = pd.Series([1.0, 2.0, 3.0, 4.0]); kontrol(abs(G.gk_yari_fark(x2, y) - (7.0 - 2.0)) < 1e-12, "3: sürekli yarı farkı (X >= medyan)")
    x3 = pd.Series([0.0, 0.0, 0.0, 2.0, 5.0]); y3 = pd.Series([1.0, 2.0, 3.0, 10.0, 20.0])
    kontrol(abs(G.gk_yari_fark(x3, y3) - (15.0 - 2.0)) < 1e-12, "3: sıfır yığılmalı X'te üst = X > 0")


def _sentetik_xy(n: int = 64, tohum: int = 3):
    rng = np.random.default_rng(tohum); s = [f"H{i:02d}" for i in range(n)]
    guc = rng.normal(size=n); Y1 = np.exp(0.6 * guc + rng.normal(scale=0.3, size=n))
    Y2 = np.clip(np.round(3 + 2 * guc + rng.normal(scale=0.5, size=n)), 0, None)
    X = pd.DataFrame({"sembol": s, "x01_guc": guc, "x02_gurultu": rng.normal(size=n), "x03_sabit": np.ones(n),
                      "x04_ikili_az": np.r_[np.ones(3), np.zeros(n - 3)], "x05_ters": -guc + rng.normal(scale=0.2, size=n)})
    Y = pd.DataFrame({"sembol": s, "Y1": Y1, "Y2": Y2, "Y3": Y1 * 1.5})
    return X, Y


def t4_istatistik() -> None:
    X, Y = _sentetik_xy(); E = copy.deepcopy(G.GK_ESIK); E["test"]["perm"] = 2000
    R = G.gk_istatistik(X, Y, E).set_index("degisken")
    kontrol(bool(R.loc["x01_guc", "aday"]) and R.loc["x01_guc", "rho_Y1"] > 0.6, "4: güçlü özellik ADAY olmalı")
    kontrol(not bool(R.loc["x02_gurultu", "aday"]), "4: gürültü aday olmamalı")
    kontrol(not bool(R.loc["x03_sabit", "sinanir"]) and not bool(R.loc["x04_ikili_az", "sinanir"]), "4: sabit / küçük ikili sınanmamalı")
    kontrol(bool(R.loc["x05_ters", "aday"]) and R.loc["x05_ters", "rho_Y1"] < 0, "4: ters yönlü güçlü özellik de (Y2 aynı yön) aday olmalı")
    Y2 = Y.copy(); Y2["Y2"] = -Y2["Y2"]
    R2 = G.gk_istatistik(X, Y2, E).set_index("degisken")
    kontrol(not bool(R2.loc["x01_guc", "aday"]) and bool(R2.loc["x01_guc", "bh"]), "4: Y2 ters yönlüyse BH anlamlı olsa da aday olmamalı")
    kontrol(np.isnan(R.loc["x03_sabit", "q_Y1"]), "4: sınanmayan değişken BH ailesine girmemeli")


def t5_agac() -> None:
    rng = np.random.default_rng(5); n = 64
    a = rng.uniform(0, 10, n); b = rng.uniform(0, 10, n)
    y = ((a > 6) | (b > 8)).astype(int)
    T = G.gk_agac(np.c_[a, b], y, 2, 5)
    kontrol(T.get("j") in (0, 1) and "sol" in T and "sag" in T, "5: kök bölmesi olmalı")
    kontrol(all(G.gk_agac_tahmin(T, r) == v for r, v in zip(np.c_[a, b], y)) or
            np.mean([G.gk_agac_tahmin(T, r) == v for r, v in zip(np.c_[a, b], y)]) > 0.9, "5: ayrılabilir veride iç doğruluk > %90")

    def yapraklar(d):
        return [d["n"]] if "j" not in d else yapraklar(d["sol"]) + yapraklar(d["sag"])
    kontrol(min(yapraklar(T)) >= 5, "5: yaprak en az 5 hisse")
    X, Y = _sentetik_xy()
    A = G.gk_agac_loo(X, Y, ["x01_guc", "x02_gurultu", "x05_ters"])
    kontrol(A["loo_dogruluk"] >= 0.75 and "x01_guc" in A["degiskenler"], f"5: sinyalli veride LOO yüksek olmalı {A['loo_dogruluk']}")
    rng = np.random.default_rng(9); Xg = X.copy(); Xg["x01_guc"] = rng.normal(size=64); Xg["x05_ters"] = rng.normal(size=64)
    Ag = G.gk_agac_loo(Xg, Y, ["x01_guc", "x02_gurultu", "x05_ters"])
    kontrol(Ag["loo_dogruluk"] < 0.72, f"5: gürültüde LOO taban civarında olmalı {Ag['loo_dogruluk']}")
    kontrol(len(A["metin"]) >= 3 and any("GÜÇLÜ" in s or "ZAYIF" in s for s in A["metin"]), "5: ağaç metni")


def t6_metin() -> None:
    kontrol(G._gk_yuzde("7,05%") == 7.05 and G._gk_yuzde("49,814%") == 49.814 and np.isnan(G._gk_yuzde("abc")), "6: yüzde okuma")
    kontrol(G._gk_ad("ANEL ELEKTRİK PROJE TAAHHÜT VE TİCARET A.Ş.") == G._gk_ad("Anel Elektrik Proje Taahhüt ve Ticaret AŞ"), "6: şirket adı anahtarı")
    kontrol(G.gk_tasfiye_fonu("TERA PORTFÖY BİRİNCİ SERBEST FON") and G.gk_tasfiye_fonu("PUSULA PORTFÖY PARA PİYASASI (TL) FONU"), "6: tasfiye fonu")
    kontrol(not G.gk_tasfiye_fonu("TERA YATIRIM MENKUL DEĞERLER A.Ş.") and not G.gk_tasfiye_fonu("İŞ PORTFÖY ÜÇÜNCÜ SERBEST (TL) FON")
            and not G.gk_tasfiye_fonu("TERA PORTFÖY YÖNETİMİ A.Ş."), "6: aracı kurum / başka portföy / portföy şirketi tasfiye fonu değil")
    kontrol(G.gk_ziraat_fonu("ATLAS PORTFÖY BİRİNCİ HİSSE SENEDİ SERBEST FON") and not G.gk_ziraat_fonu("TERA PORTFÖY BİRİNCİ SERBEST FON"), "6: Ziraat fonu")
    kontrol(G.gk_ortak_mi("FIRAT KIRHAN", "PRİZMA PRES MATBAACILIK A.Ş.") and not G.gk_ortak_mi("MERRILL LYNCH INTERNATIONAL", "X A.Ş.")
            and not G.gk_ortak_mi("OYLUM SINAİ YATIRIMLAR ANONİM ŞİRKETİ", "OYLUM SINAİ YATIRIMLAR A.Ş.")
            and not G.gk_ortak_mi("PARDUS PORTFÖY ONBİRİNCİ HİSSE SENEDİ SERBEST (TL) FON", "X A.Ş."), "6: ortak mı")
    kontrol(len(G.gk_leke_kap_metin("Şirketimize kayyım atanmıştır. Diğer konular.")) == 1, "6: kayyım cümlesi leke")
    kontrol(not G.gk_leke_kap_metin("Şirketimiz hakkında kayyım atanmasına ilişkin bir karar bulunmamaktadır."), "6: olumsuzlanan cümle leke değil")
    kontrol(G.gk_alim_yonu("net 52.207 adet pay satın alınmıştır") == "alis" and G.gk_alim_yonu("net 92.640 adet pay satılmıştır") == "satis", "6: net kalıbı")
    kontrol(G.gk_alim_yonu("Pay Alım Satım Bildirimi | İşlem Türü | Alış | 10.000") == "alis", "6: tablo alış")
    kontrol(G.gk_alim_yonu("Pay Alım Satım Bildirimi | İşlem Türü | Satış | 10.000") == "satis", "6: tablo satış")
    kontrol(G.gk_alim_yonu("Pay Alım Satım Bildirimi") == "belirsiz", "6: yalnız başlık belirsiz")
    form = ("tarihinde X A.Ş. payları ile ilgili olarak 13,66 - 13,66 TL fiyat aralığından 14.630.577,00 TL toplam\n nominal tutarlı alış işlemi "
            "ve/veya 0 TL toplam nominal tutarlı satış işlemi tarafımca gerçekleştirilmiştir. | Alım Satım |")
    kontrol(G.gk_alim_yonu(form) == "alis", "6: MKK formu alış")
    kontrol(G.gk_alim_yonu(form.replace("14.630.577,00 TL toplam\n nominal tutarlı alış", "0 TL toplam nominal tutarlı alış")
                            .replace("0 TL toplam nominal tutarlı satış", "5.000 TL toplam nominal tutarlı satış")) == "satis", "6: MKK formu satış")
    kontrol(G.gk_alim_yonu("SKBNK rüçhan tahtasından 7.000.000 adet alış işlemi tarafımızdan gerçekleştirilmiş") == "alis", "6: adet alış işlemi")
    boiler = ('hükmü uyarınca "Bir kurucuya ait yatırım fonlarının ... %5, %10, %15, %20, %25, %33, %50, %67 veya %95\'ine ulaşması ve söz konusu '
              'oranların altına düşmesi halinde kurucu tarafından, yerine getirilir." açıklama: fonlar 1.000 pay sattı ve pay %4,2 oldu.')
    kontrol(not G.gk_esik5(boiler), "6: mevzuat alıntısı %5 ulaşma sayılmamalı")
    kontrol(G.gk_esik5("fonlarımızın X A.Ş. sermayesindeki payı %5'ine ulaşmıştır."), "6: %5'e ulaşma")
    kontrol(G.gk_esik5("hisselerinin toplamı, 12.11.2024 tarihinde 8.076.500 TL nominal hisse alımı sonucunda %5 sınırını aşarak %6.11'e ulaşmıştır."),
            "6: '%5 sınırını aşarak' yukarı geçiş")
    kontrol(not G.gk_esik5("27.05.2024 tarihinde hisse satımı sonucunda %5 sınırından %0,53'e düşmüştür."), "6: %5'ten aşağı düşüş ulaşma değil")
    kontrol(not G.gk_esik5("payı %50'sine ulaşmıştır") and not G.gk_esik5("payı %5,4'ten %4,1'e inmiştir"), "6: %50 / azalış %5 ulaşma değil")
    kontrol(G.gk_geri_alim_program("Pay Geri Alım Programının Başlatılması Hk.") and not G.gk_geri_alim_program("Pay Geri Alım Programı Kapsamında "
            "Gerçekleştirilen İşlemler Hk.") and not G.gk_geri_alim_program("Pay Geri Alım İşlemleri"), "6: geri alım program özeti")
    h = "<td>Ana Ortaklığa Ait Özkaynaklar</td><td>12</td><td>1.234.567.890</td><td>1.000.000.000</td>"
    kontrol(G.gk_fr_ozkaynak(h) == 1234567890.0, f"6: FR özkaynak okuma {G.gk_fr_ozkaynak(h)}")
    kontrol(G.gk_fr_ozkaynak("<td>Toplam Özkaynaklar</td><td>-5.000.000</td>") == -5000000.0, "6: negatif toplam özkaynak")
    h2 = "<td>Sunum Para Birimi</td><td>1.000 TL</td><td>ÖZKAYNAKLAR</td><td>EQUITY</td><td>14.817.002</td><td>14.817.002</td>"
    kontrol(G.gk_fr_ozkaynak(h2) == 14817002000.0, f"6: finans biçimi + bin TL çarpanı {G.gk_fr_ozkaynak(h2)}")
    p = 'xx Şirketin Dahil Olduğu Endeksler\\",\\"children\\":\\"BIST 100\\"}],[\\"children\\":\\"BIST TÜM\\"}'
    kontrol(G.gk_endeksler(p) == ["BIST 100", "BIST TÜM"] and G.gk_endeksler(None) is None, f"6: endeks listesi {G.gk_endeksler(p)}")


def t7_esik_tablo() -> None:
    tmp = tempfile.mkdtemp(prefix="gk_esik_")
    try:
        y = os.path.join(tmp, "esik.csv")
        sat = ["0,1,2,3,4,5,6,7,8,9,10,11",
               '101,01/09/2026,TERA PORTFÖY BİRİNCİ SERBEST FON,ANEL ELEKTRİK PROJE TAAHHÜT VE TİCARET A.Ş.,"42.955.201,00","62.939.511,00","16,21%","23,75%",1,1,,',
               '102,02/10/2026,A1 PORTFÖY YÖNETİMİ A.Ş.,CVL,A1 CAPİTAL PORTFÖY ÇOKLU VARLIK KATILIM FONU,29,18,"46,44%","32,03%",63,57,',
               '103,03/11/2026,FIRAT KIRHAN,PRİZMA PRES MATBAACILIK YAYINCILIK SANAYİ VE TİCARET A.Ş.,PRZMA,"1,00","2,00","1,52%","4,70%",7,7,']
        with open(y, "w", encoding="utf-8") as f:
            f.write("\n".join(sat) + "\n")
        L = pd.DataFrame({"disclosureIndex": [101, 102, 103, 9], "t": pd.to_datetime(["2026-09-01 09:00", "2026-10-02 09:00", "2026-11-03 09:00",
                                                                                       "2026-09-05 10:00"]),
                          "kapTitle": ["", "", "", "ANEL ELEKTRİK PROJE TAAHHÜT VE TİCARET A.Ş."], "own": [[], [], [], ["ANELE"]]})
        T = G.gk_esik_tablo(L, y)
        kontrol(len(T) == 2 and sorted(T.kod) == ["ANELE", "PRZMA"], f"7: fon payı satırı atılmalı, kodlar eşlenmeli {T.kod.tolist()}")
        a = T[T.kod == "ANELE"].iloc[0]; b = T[T.kod == "PRZMA"].iloc[0]
        kontrol(a.p0 == 16.21 and a.p1 == 23.75 and b.p0 == 1.52 and b.p1 == 4.70, "7: yüzdeler (kod sütunlu satırda kaydırma)")
        kontrol(a.yay == pd.Timestamp("2026-09-01 09:00") and b.yay == pd.Timestamp("2026-11-03 09:00"), "7: yayın zamanı eşlemesi")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def t8_ileri() -> None:
    durmali(lambda: G.gk_ileri_denetim("deneme", [pd.Timestamp("2026-11-01 00:00:01")]), "8: kesim sonrası bilgi durdurmalı", "GELECEĞE BAKMA")
    G.gk_ileri_denetim("deneme", [pd.Timestamp("2026-10-31 23:59:00"), pd.NaT])
    idx = pd.bdate_range("2026-10-20", "2026-11-13")
    d = pd.DataFrame({"o": 1.0, "h": 1.0, "l": 1.0, "c": 1.0, "v": 1.0, "carpan": 1.0}, index=idx)
    x = G.gk_fiyat_kes(d, G.gk_kesim_ts())
    kontrol(x.index[-1] == pd.Timestamp("2026-10-30"), f"8: fiyat 30.10'da kesilmeli {x.index[-1]}")


def t9_y() -> None:
    idx = pd.bdate_range("2026-08-03", "2026-11-13")
    c = np.full(len(idx), 10.0)
    i30 = idx.get_loc(pd.Timestamp("2026-10-30")); c[idx.get_loc(pd.Timestamp("2026-10-15"))] = 4.0
    c[i30] = 5.0; c[i30 + 1:] = 5.0 * 1.1 ** np.arange(1, len(idx) - i30)   # 2.11'den itibaren her gün tavan
    c[-1] = c[-2]                                                             # son gün tavan değil
    d = pd.DataFrame({"o": c, "h": c, "l": c, "c": c, "v": 1e6, "carpan": 1.0}, index=idx)
    C = pd.DataFrame({"sembol": ["A"]})
    Y = G.gk_y_tablo(C, {"A": d}).iloc[0]
    n_tavan = len(idx) - i30 - 2
    kontrol(abs(Y.Y1 - c[-1] / 5.0) < 1e-9 and int(Y.Y2) == n_tavan and abs(Y.Y3 - c[-1] / 4.0) < 1e-9,
            f"9: Y1 / Y2 / Y3 elle tutmuyor ({Y.Y1}, {Y.Y2} vs {n_tavan}, {Y.Y3})")


def t10_kapi() -> None:
    tmp = tempfile.mkdtemp(prefix="gk_kapi_"); eski = dict(G.GK_YOL)
    try:
        G.GK_YOL["is"] = tmp
        Xy = os.path.join(tmp, G.GK_DOSYA["X"])
        pd.DataFrame({"sembol": ["A"], "x01": [1.0]}).to_csv(Xy, index=False)
        durmali(lambda: G.gk_kapi(tmp, git=False), "10: ön kayıt yokken kapı açılmamalı", "ön kayıt yok")
        y = os.path.join(tmp, G.GK_DOSYA["onkayit"]); xs = G.TS.ts_sha_dosya(Xy)
        with open(y, "w", encoding="utf-8") as f:
            f.write(f"x\nESIK_SHA256: {G.gk_esik_sha()}\nKOD_SHA256: {G.gk_kod_sha()}\nX_SHA256: {xs}\n")
        durmali(lambda: G.gk_kapi(tmp, git=True), "10: git'e işlenmemiş ön kayıtla kapı açılmamalı", "git")
        subprocess.run(["git", "-C", tmp, "init", "-q"], check=True)
        subprocess.run(["git", "-C", tmp, "add", G.GK_DOSYA["onkayit"]], check=True)
        subprocess.run(["git", "-C", tmp, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "on kayit"], check=True)
        K = G.gk_kapi(tmp, git=True)
        kontrol(K["kod_ayni"] and len(K["onkayit_git"]["commit"]) == 40, "10: commit sonrası kapı geçmeli")
        E2 = copy.deepcopy(G.GK_ESIK); E2["test"]["bh_q"] = 0.2
        durmali(lambda: G.gk_kapi(tmp, git=True, E=E2), "10: eşik değişince kapı açılmamalı", "eşik")
        pd.DataFrame({"sembol": ["A"], "x01": [2.0]}).to_csv(Xy, index=False)
        durmali(lambda: G.gk_kapi(tmp, git=True), "10: X değişince kapı açılmamalı", "X.csv")
        pd.DataFrame({"sembol": ["A"], "x01": [1.0]}).to_csv(Xy, index=False)
        with open(y, "a", encoding="utf-8") as f:
            f.write("sonradan\n")
        durmali(lambda: G.gk_kapi(tmp, git=True), "10: ön kayıt commit sonrası değişince kapı açılmamalı", "farklı")
        with open(y, "w", encoding="utf-8") as f:
            f.write(f"x\nESIK_SHA256: {G.gk_esik_sha()}\nKOD_SHA256: {'0' * 64}\nX_SHA256: {xs}\n")
        durmali(lambda: G.gk_kapi(tmp, git=False), "10: kod farkında sapmasız kapı açılmamalı", "sapma")
        kontrol(G.gk_kapi(tmp, git=False, sapma="test")["sapma"] == "test", "10: sapma gerekçesiyle geçmeli")
    finally:
        G.GK_YOL.update(eski); shutil.rmtree(tmp, ignore_errors=True)


def t11_kapilar() -> None:
    kod = open(os.path.join(KOK, "GENIS_KESIT.py"), encoding="utf-8").read()
    kontrol(not re.search(r"[\w.+-]+@[\w-]+\.(com|net|org|io|tr)\b", kod), "11: kodda e-posta biçimli metin var")
    for yasak in ("IZ_DEFTERI.md", "IZ_KARNE.py", "CLAUDE.md", "COL_OZET.md", "ONERI_DEFTERI.md"):
        kontrol(yasak not in kod.split('"""', 2)[2], f"11: kod {yasak} dosyasına atıf yapıyor (yalnız belge başında olabilir)")
    kontrol("open(os.path.join(KOK_GK, \"TAVAN_SERISI.py\"), \"w\"" not in kod and "TAVAN_SERISI.py\", \"w\"" not in kod, "11: TAVAN_SERISI.py yazılmamalı")
    g = {"__name__": "gk_cakisma", "gk_kos": lambda: None}
    try:
        exec(compile(kod, "GENIS_KESIT.py", "exec"), g)
        HATA.append("11: çakışma kapısı bellekteki gk_kos'u ezen yüklemeyi durdurmalı")
    except RuntimeError as ex:
        kontrol("EZDİ" in str(ex), f"11: çakışma kapısı yanlış neden {ex}")
    tmp = tempfile.mkdtemp(prefix="gk_yaz_")
    try:
        durmali(lambda: G._gk_yaz(os.path.join(tmp, "a.md"), "iletişim: ornek@alan.com"), "11: e-posta içeren metin yazılmamalı", "e-posta")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    for t in (t1_spearman, t2_bh, t3_sinanir, t4_istatistik, t5_agac, t6_metin, t7_esik_tablo, t8_ileri, t9_y, t10_kapi, t11_kapilar):
        try:
            t()
        except Exception as ex:  # noqa: BLE001  (test çerçevesi: beklenmeyen hata da hata sayılır)
            HATA.append(f"{t.__name__}: beklenmeyen {type(ex).__name__}: {ex}")
    if HATA:
        print("TEST HATALI:\n- " + "\n- ".join(HATA)); sys.exit(1)
    print("test_genis_kesit: bütün testler geçti")
