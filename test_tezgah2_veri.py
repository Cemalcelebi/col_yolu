"""TEZGAH2_VERI testleri (ag gerekmez; sentetik veri). Calistirma: python test_tezgah2_veri.py"""
from __future__ import annotations

import os
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import TEZGAH2_VERI as T  # noqa: E402

SAY = {"ok": 0}


def kontrol(ad: str, kosul: bool) -> None:
    if not kosul:
        raise AssertionError(ad)
    SAY["ok"] += 1
    print("TAMAM", ad)


def sentetik(n: int = 400, tohum: int = 1, bas: str = "2020-01-02") -> pd.DataFrame:
    r = np.random.default_rng(tohum)
    c = 50 * np.exp(np.cumsum(r.normal(0, 0.01, n)))
    idx = pd.bdate_range(bas, periods=n)
    d = pd.DataFrame({"Open": c * 0.998, "High": c * 1.01, "Low": c * 0.99, "Close": c, "Volume": r.integers(1000, 5000, n).astype(float)}, index=idx)
    return d


# 1) cakisma kapisi: ayni adi baska dosya tanimlamissa ezme algilanir
g = {"tz_yol": 1}
kontrol("cakisma kapisi var", callable(T._cakisma_kontrol_tz))

# 2) evren ayristirma
NAS = ("Symbol|Security Name|Market Category|Test Issue|Financial Status|Round Lot Size|ETF|NextShares\n"
       "AAAA|Alfa Inc. - Common Stock|Q|N|N|100|N|N\n"
       "AAAE|Alfa ETF Trust|G|N|N|100|Y|N\n"
       "AAAW|Alfa Inc. - Warrant|S|N|N|100|N|N\n"
       "AAAU|Alfa Acquisition Corp - Unit|S|N|N|100|N|N\n"
       "AAAT|Test Corp - Common Stock|Q|Y|N|100|N|N\n"
       "ADRX|Beta Ltd American Depositary Shares|Q|N|N|100|N|N\n"
       "SPCE|Blue Acquisition Corp. - Class A Common Stock|G|N|N|100|N|N\n"
       "File Creation Time: 1120202621:31||||||\n")
OTH = ("ACT Symbol|Security Name|Exchange|CQS Symbol|ETF|Round Lot Size|Test Issue|NASDAQ Symbol\n"
       "BRK.B|Berkshire Hathaway Inc. Class B|N|BRK.B|N|100|N|BRK.B\n"
       "MPLX|MPLX LP Common Units Representing Limited Partner Interests|N|MPLX|N|100|N|MPLX\n"
       "XYZ$A|Xyz Preferred Series A|N|XYZ-A|N|100|N|XYZ$A\n"
       "SPY|SPDR S&P 500 ETF|P|SPY|Y|100|N|SPY\n"
       "BXSL|Blackstone Secured Lending Fund Common Shares of Beneficial Interest|N|BXSL|N|100|N|BXSL\n"
       "EQF|Adams Diversified Equity Fund Inc. - Closed End Fund|N|EQF|N|100|N|EQF\n"
       "File Creation Time: 1120202621:31||||||\n")
E = T.tz_evren_ayristir(NAS, OTH, ["ESKI", "AAAA"])
k = set(E.yahoo)
kontrol("evren: adi hisse kalir", {"AAAA", "ADRX", "SPCE", "BRK-B", "MPLX", "BXSL"} <= k)
kontrol("evren: ETF / warrant / unit / test / preferred / Arca / fon elenir", not ({"AAAE", "AAAW", "AAAU", "AAAT", "SPY", "EQF"} & k) and not any("$" in x for x in k))
kontrol("evren: BRK.B -> BRK-B Yahoo kodu", "BRK-B" in k)
kontrol("evren: eski listede olup listede olmayan eklenir", "ESKI" in k and E[E.yahoo == "ESKI"].borsa.iloc[0] == "eski_liste")
kontrol("evren: ADR / SPAC bayragi", E[E.yahoo == "ADRX"].adr.iloc[0] == 1 and E[E.yahoo == "SPCE"].spac.iloc[0] == 1)

# 3) parcalama + devam (parca dosyasi varsa atlanir)
P = T.tz_parcala([f"S{i:03d}" for i in range(250)], 60)
kontrol("parcalama: 5 parca, tekrar yok", len(P) == 5 and len({x for p in P for x in p}) == 250)
with tempfile.TemporaryDirectory() as td:
    T.TZ_AYAR["kok"] = td
    import pickle
    cagri = {"n": 0}
    asil_parca, asil_tek = T.tz_indir_parca, T.tz_tek
    def sahte_parca(kodlar):
        cagri["n"] += 1
        return {c: sentetik(300, hash(c) % 100) for c in kodlar if c != "YOK"}, [c for c in kodlar if c == "YOK"]
    T.tz_indir_parca = sahte_parca; T.tz_tek = lambda c: None
    T.TZ_AYAR["bekle"] = 0
    kodlar = [f"S{i:03d}" for i in range(130)] + ["YOK"]
    T.tz_indir("ABD", kodlar); ilk = cagri["n"]
    T.tz_indir("ABD", kodlar)
    kontrol("devam: ikinci kosuda parca yeniden indirilmez", cagri["n"] == ilk and ilk == 3)
    veri, yok = T.tz_ham_topla("ABD")
    kontrol("ham toplama: 130 veri, 1 indirilemeyen", len(veri) == 130 and yok == ["YOK"])
    T.tz_indir_parca, T.tz_tek = asil_parca, asil_tek

# 4) bicim: gecersiz bar, bugunku bar, tip
d = sentetik(300); bugun = str(d.index[-1].date())
d.iloc[10, d.columns.get_loc("High")] = d.iloc[10].Low * 0.9   # H < L
d.iloc[20, d.columns.get_loc("Close")] = np.nan
t = T.tz_temizle(d, bugun)
kontrol("bicim: H<L ve bos bar atilir", len(t) == 300 - 2 - 1)   # -1: bugunku bar
kontrol("bicim: sutun / indeks yapisi V_ABD ile ayni", list(t.columns) == ["Open", "High", "Low", "Close", "Volume"] and t.index.name == "Date"
        and str(t.index.dtype) == "datetime64[s]" and t.columns.name == "Price" and all(str(x) == "float64" for x in t.dtypes))
kontrol("bicim: bugunku (yarim olabilir) bar yok", t.index.max() < pd.Timestamp(bugun))

# 5) AVR: peni / sterlin 100x temizligi + Kur
a = sentetik(300, 3); a.iloc[150:, :4] = a.iloc[150:, :4] * 100.0   # pens -> 100x sicrama
fx = {"GBp": pd.Series(1.15, index=a.index)}
b, neden = T.tz_avr_duzelt(T.tz_temizle(a, "2100-01-01"), "GBp", fx)
kontrol("AVR: 100x sicrama duzeltilir, seri surekli (son parca birimi)", b is not None and abs(b.Close.pct_change()).max() < 0.2 and b.Close.iloc[-1] > 1000)
kontrol("AVR: GBp -> Kur = fx/100", b is not None and abs(b.Kur.iloc[-1] - 0.0115) < 1e-9)
gec = sentetik(300, 14); gec.iloc[100:200, :4] = gec.iloc[100:200, :4] * 100.0    # gecici 100x parca (PNL.L tipi)
g2, _ = T.tz_avr_duzelt(T.tz_temizle(gec, "2100-01-01"), "EUR", {})
kontrol("AVR: gecici 100x parca (yukari + geri) duzelir", g2 is not None and abs(g2.Close.pct_change()).max() < 0.2)
kal = T.tz_birim_kalibre(g2.assign(Kur=1.0), g2.assign(Kur=1.0, Close=g2.Close * 100))
kontrol("birim kalibre: yeni 100x kucukse Kur x100", kal == 100.0 and T.tz_birim_kalibre(g2.assign(Kur=1.0), g2.assign(Kur=1.0)) == 1.0)
ng = sentetik(300, 15); ng.iloc[100:110, :4] = -5.0
cg, nk = T.tz_negatif_kes(ng)
kontrol("negatif kesme: son bozuk bara kadar kesilir", nk == 110 and len(cg) == 190)
ng2 = sentetik(300, 16); ng2.iloc[-1, :4] = -5.0
cg2, nk2 = T.tz_negatif_kes(ng2)
kontrol("negatif kesme: son barlardaki bozuk bar yalniz atilir", nk2 == 0 and len(cg2) == 299)
c = sentetik(300, 4); c.iloc[100] = c.iloc[100] * 30   # aciklanamayan 30x sicrama
kontrol("AVR: aciklanamayan sicrama dislanir", T.tz_avr_duzelt(T.tz_temizle(c, "2100-01-01"), "EUR", {})[0] is None)
e, _ = T.tz_avr_duzelt(T.tz_temizle(sentetik(300, 5), "2100-01-01"), "EUR", {})
kontrol("AVR: EUR icin Kur=1", e is not None and (e.Kur == 1.0).all())
f, _ = T.tz_avr_duzelt(T.tz_temizle(sentetik(300, 6), "2100-01-01"), "CHF", {"CHF": pd.Series(0.9, index=pd.bdate_range("2019-01-01", periods=1000))})
kontrol("AVR: CHF Kur uygulanir", f is not None and (f.Kur - 0.9).abs().max() < 1e-12)

# 6) kalite fonksiyonlari
v = sentetik(300, 7)
v.iloc[5, v.columns.get_loc("Volume")] = 0
g = T.tz_gecerlilik(v)
kontrol("kalite: hacim 0 sayimi", int(g.hacim0.sum()) == 1 and int(g.bar.sum()) == 300)
x = sentetik(300, 8); x.iloc[100:, :4] = x.iloc[100:, :4] * 0.1   # ters bolunme benzeri sicrama, bolunme kaydi yok
s1 = T.tz_sicrama(x, None)
kontrol("kalite: >%50 gun bolunmesiz sayilir", s1["buyuk50"] == 1 and s1["buyuk50_bolunme_esli"] == 0)
bol = pd.Series([0.1], index=[x.index[100]])
s2 = T.tz_sicrama(x, bol)
kontrol("kalite: bolunme gunuyle eslesme", s2["buyuk50_bolunme_esli"] == 1 and s2["ters_bolunme"] == 1)
y = sentetik(300, 9); y.iloc[50, :4] = y.iloc[50, :4] * 1.6   # tek gunluk sicra, ertesi gun geri
kontrol("kalite: sicra-geri don yakalanir", T.tz_sicrama(y, None)["sicra_geri"] == 1)
eski = sentetik(300, 10); yeni = eski.copy(); yeni.iloc[:, :4] = yeni.iloc[:, :4] * 1.05
o = T.tz_oran_tutarlilik(yeni, eski)
kontrol("kalite: sabit carpan -> CV ~ 0, oran 1.05", o["cv_Close"] < 1e-9 and abs(o["oran_ort"] - 1.05) < 1e-9)
yeni2 = eski.copy(); yeni2.iloc[150:, :4] = yeni2.iloc[150:, :4] * 1.2
kontrol("kalite: tutarsiz ayar CV > %1", T.tz_oran_tutarlilik(yeni2, eski)["cv_Close"] > 0.01)
Vd = {"A": sentetik(300, 11), "B": sentetik(300, 11), "C": sentetik(300, 12)}
yg = T.tz_yinelenen(Vd, {"A": "Alfa Inc Class A Common Stock", "B": "Alfa Inc. Class B Common Stock", "C": "Gama"})
kontrol("kalite: ayni seri + sinif cifti", yg["ayni_seri"] == [["A", "B"]] and yg["ad_esit"] == [["A", "B"]])
ay = T.tz_aktif_yil({"A": sentetik(300, 13, "2020-01-02")}, (2019, 2022))
kontrol("kalite: aktif yil sayimi", ay[2019] == 0 and ay[2020] == 1 and ay[2021] == 1)

# 7) kodda e-posta / anahtar yok, Tiingo istegi yok
kod = open(os.path.join(KOK, "TEZGAH2_VERI.py"), encoding="utf-8").read()
import re
kontrol("e-posta biçimli dize yok", not re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", kod))
kontrol("Tiingo istegi yok", "api.tiingo" not in kod.lower() and "token" not in kod.lower())

print(f"\n{SAY['ok']} kontrol gecti")
