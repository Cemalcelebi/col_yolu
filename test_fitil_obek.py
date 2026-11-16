"""test_fitil_obek — FITIL_OBEK.py sentetik testleri (veri gerekmez).

1) fitil payları elle   2) pencere / S+ / S- kuralı (k barı dolunca, eşik sınırı)   3) KUCUK   4) onda kesiti
5) geleceğe bakma: seri t'de kesilince bütün satırlar aynı; fo_gelecek_denetimi sentetik pazarda TUTAR, bozuk olayda DURUR
6) ayna (kaçınma) kuralı ve durum   7) BH   8) bootstrap p yönü   9) cetvel çağrısı: fo_olc_satir + fo_satir_sonuc + etiket eşlemesi
10) kapı: ön kayıt yok / bozuk / sha tutmuyor -> durur; kontrol listesi 14 satır kapıdan geçer   11) e-posta / anahtar taraması
Çalıştır: python test_fitil_obek.py
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

import FITIL_OBEK as FO  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402

GECTI, KALDI = [], []


def kontrol(ad, kosul, ek=""):
    (GECTI if kosul else KALDI).append(ad)
    print(("  OK   " if kosul else "  HATA ") + ad + (f"  ({ek})" if ek else ""))


def mum(alt, ust, govde=0.4, yesil=True, L=100.0, R=2.0):
    """alt / üst / gövde paylarından bir bar (O, H, L, C)."""
    gb = L + alt * R; gt = gb + govde * R
    H = L + R
    assert abs((H - gt) / R - ust) < 1e-9 or abs(alt + ust + govde - 1) < 1e-9
    O, C = (gb, gt) if yesil else (gt, gb)
    return O, H, L, C


def seri(paylar, bas="2020-01-01", V=1000.0):
    rows = [mum(a, u, 1 - a - u) for a, u in paylar]
    ix = pd.bdate_range(bas, periods=len(rows))
    return pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"], index=ix).assign(Volume=V)


def rastgele_hisse(n, tohum, bas="2016-01-01"):
    rng = np.random.default_rng(tohum)
    C = 50 * np.exp(np.cumsum(rng.normal(0.0003, 0.02, n)))
    O = C * (1 + rng.normal(0, 0.006, n))
    a = rng.uniform(0, 0.012, n); b = rng.uniform(0, 0.012, n)
    H = np.maximum(O, C) * (1 + b); L = np.minimum(O, C) * (1 - a)
    V = rng.integers(5000, 80000, n).astype(float)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=pd.bdate_range(bas, periods=n))


print("1) fitil payları")
d = pd.DataFrame({"Open": [10.0, 12.0], "High": [13.0, 12.5], "Low": [9.0, 10.0], "Close": [12.0, 10.5], "Volume": [1, 1]},
                 index=pd.bdate_range("2021-01-04", periods=2))
B = FO.fo_bar(d)
kontrol("alt (yeşil) = (O-L)/R", abs(B.alt.iloc[0] - 0.25) < 1e-12, B.alt.iloc[0])
kontrol("üst (yeşil) = (H-C)/R", abs(B.ust.iloc[0] - 0.25) < 1e-12)
kontrol("alt (kırmızı) = (C-L)/R", abs(B.alt.iloc[1] - 0.2) < 1e-12)
kontrol("üst (kırmızı) = (H-O)/R", abs(B.ust.iloc[1] - 0.2) < 1e-12)
kontrol("TR ilk bar = R, sonra önceki kapanışla", abs(B.TRC.iloc[0] - 4 / 12) < 1e-12 and abs(B.TRC.iloc[1] - (12.5 - 10) / 10.5) < 1e-12)
dg = d.copy(); dg.loc[dg.index[1], "Volume"] = 0
kontrol("geçersiz bar (V=0) atılır", len(FO.fo_bar(dg)) == 1)

print("2) pencere ve kural")
nötr = [(0.3, 0.3)] * 30
sp = [(0.0, 0.5)] * 6 + [(0.2, 0.4)] * 4      # ALTYOK 0,6, ASIM = 0,46 - 0,08 = 0,38
x = seri(nötr + sp)
sig, asim = FO.fo_hisse_sinyal(x)
kontrol("S+ k10 son barda doğru", bool(sig["SP_k10"].iloc[-1]))
kontrol("S+ k10: 4 alt fitilsiz barda yanlış, 5.'de doğru", not bool(sig["SP_k10"].iloc[33]) and bool(sig["SP_k10"].iloc[34])
        and not sig["SP_k10"].iloc[:33].any())
kontrol("S- k10 yanlış", not sig["SM_k10"].any())
sm = [(0.5, 0.0)] * 6 + [(0.4, 0.2)] * 4
sig2, _ = FO.fo_hisse_sinyal(seri(nötr + sm))
kontrol("S- k10 ayna doğru", bool(sig2["SM_k10"].iloc[-1]) and not sig2["SP_k10"].any())
sinir = [(0.05, 0.25)] * 5 + [(0.15, 0.25)] * 5   # ALTYOK 0,5 (sınır dahil), ASIM 0,25 - 0,10 = 0,15 < 0,20
sig3, _ = FO.fo_hisse_sinyal(seri(nötr + sinir))
kontrol("ASIM eşiğin altında -> S+ yok", not bool(sig3["SP_k10"].iloc[-1]))
sinir2 = [(0.0, 0.3)] * 5 + [(0.12, 0.3)] * 5   # ALTYOK 0,5 tam, ASIM 0,30 - 0,06 = 0,24
sig4, _ = FO.fo_hisse_sinyal(seri(nötr + sinir2))
kontrol("ALTYOK = 0,50 sınırı dahil", bool(sig4["SP_k10"].iloc[-1]))
kontrol("k5 / k15 satırları üretiliyor", {"SP_k5", "SP_k15", "SM_k5", "SM_k15", "SP_kucuk", "SM_kucuk"} <= set(sig))
P = FO.fo_pencere(FO.fo_bar(seri(nötr + sp)), 10)
kontrol("ASIM = U - A", abs(P.ASIM.iloc[-1] - (P.U.iloc[-1] - P.A.iloc[-1])) < 1e-12 and abs(P.ASIM.iloc[-1] - 0.38) < 1e-9, P.ASIM.iloc[-1])

print("3) KUCUK")
h = rastgele_hisse(400, 3)
Bh = FO.fo_bar(h); Ph = FO.fo_pencere(Bh, 10)
i = 300
beklenen = np.median(Bh.RC.iloc[i - 9:i + 1]) <= 0.75 * Bh.TRC.iloc[i - 249:i + 1].mean()
kontrol("KUCUK elle", bool(Ph.KUCUK.iloc[i]) == bool(beklenen))
kontrol("ATR250 en az 120 bar", Ph.ATR250.iloc[:119].isna().all() and np.isfinite(Ph.ATR250.iloc[119]))

print("4) onda")
rng = np.random.default_rng(5)
A = pd.DataFrame(rng.normal(0, 1, (3, 50)), index=pd.bdate_range("2022-01-03", periods=3), columns=[f"S{i}" for i in range(50)])
A.iloc[2, 25:] = np.nan
up, dn = FO.fo_onda(A)
kontrol("onda üst %10 = 5 hisse (50 hissede)", int(up.iloc[0].sum()) == 5 and int(dn.iloc[0].sum()) == 5)
kontrol("onda < 30 hisse -> yok", not up.iloc[2].any() and not dn.iloc[2].any())
kontrol("onda en büyük ASIM üstte", bool(up.iloc[0][A.iloc[0].idxmax()]) and bool(dn.iloc[0][A.iloc[0].idxmin()]))

print("5) geleceğe bakma")
Vs = {f"H{i:02d}": rastgele_hisse(700, 100 + i) for i in range(45)}
Vd = OC._oc_veri_sar(Vs, "ABD")
X = FO.fo_sinyaller(Vd, "ABD")
kontrol("sentetik pazarda olay var (ana + onda + k5 + kucuk)", {"SP_k10", "SM_k10", "SP_onda", "SM_onda", "SP_k5", "SM_k5", "SP_kucuk"} <= set(X.satir),
        X.satir.value_counts().to_dict())
tam, _ = FO.fo_hisse_sinyal(Vd["V"]["H03"])
hep = True
for t in Vd["V"]["H03"].index[[50, 200, 333, 512, 699]]:
    kes, _ = FO.fo_hisse_sinyal(Vd["V"]["H03"][Vd["V"]["H03"].index <= t])
    for k in tam:
        if bool(tam[k].loc[t]) != bool(kes[k].iloc[-1]):
            hep = False
kontrol("seri t'de kesilince bütün satırlar aynı", hep)
kisa, _ = FO.fo_hisse_sinyal(seri(sp[:6] + [(0.0, 0.5)] * 6))
kontrol("kısa seri (12 bar): k5 tanımlı, k15 yanlış", bool(kisa["SP_k5"].iloc[-1]) and not kisa["SP_k15"].any())
for t in Vd["V"]["H07"].index[[4, 6, 9, 12, 14]]:
    kes, _ = FO.fo_hisse_sinyal(Vd["V"]["H07"][Vd["V"]["H07"].index <= t])
    tam7, _ = FO.fo_hisse_sinyal(Vd["V"]["H07"])
    if any(bool(tam7[k].loc[t]) != bool(kes[k].iloc[-1]) for k in tam7):
        hep = False
kontrol("seri başında (< 15 bar) kesme testi aynı", hep)
try:
    g = FO.fo_gelecek_denetimi(Vd, X, "ABD")
    kontrol("fo_gelecek_denetimi sentetikte TUTAR", g["hisse"] > 0 and g["onda"] > 0, g)
except FO.FOHata as ex:
    kontrol("fo_gelecek_denetimi sentetikte TUTAR", False, str(ex))
bozuk = pd.DataFrame({"sembol": ["H01"], "tarih": [Vd["V"]["H01"].index[5]], "pazar": ["ABD"], "satir": ["SP_k10"]})
try:
    FO.fo_gelecek_denetimi(Vd, bozuk, "ABD"); kontrol("bozuk olayda denetim durur", False)
except FO.FOHata:
    kontrol("bozuk olayda denetim durur", True)

print("6) ayna kuralı")
h0 = {"n": 100, "ort_fark": -0.03, "ust95": -0.01, "alt95": -0.05, "sira": 0.45, "portfoy": 0.1, "portfoy_esli_p10": 0.2,
      "portfoy_esli_p90": 0.5, "yari1_fark": -0.02, "yari2_fark": -0.04, "tutar": False}
kontrol("ayna TUTAR", FO.fo_kacinma(h0))
for k, v in (("ust95", 0.001), ("sira", 0.5), ("portfoy", 0.25), ("yari2_fark", 0.01), ("n", 29)):
    kontrol(f"ayna {k} bozulunca TUTMAZ", not FO.fo_kacinma({**h0, k: v}))
kontrol("ayna NaN / None güvenli", not FO.fo_kacinma({**h0, "yari1_fark": None}))
kontrol("durum '-' n 100 tutar -> TUTAR", FO.fo_durum(h0, "-")[0] == "TUTAR")
kontrol("durum '-' n 1500 tutmaz -> TUTMADI", FO.fo_durum({**h0, "n": 1500, "sira": 0.6}, "-")[0] == "TUTMADI")
kontrol("durum n < 30 -> ÖLÇÜLEMEDİ", FO.fo_durum({**h0, "n": 10}, "-")[0] == "ÖLÇÜLEMEDİ" and FO.fo_durum({"n": 10, "tutar": True}, "+")[0] == "ÖLÇÜLEMEDİ")

print("7) BH")
kontrol("BH örnek", FO.fo_bh([0.01, 0.04, 0.03, 0.5, np.nan], 0.10) == [True, True, True, False, False])
kontrol("BH hiç geçmez", not any(FO.fo_bh([0.5, 0.9], 0.10)))

print("8) bootstrap p")
gun = pd.Series(pd.date_range("2023-01-01", periods=120, freq="5D"))
f = np.random.default_rng(1).normal(0.05, 0.1, 120)
kontrol("pozitif fark: p(+) küçük, p(-) büyük", FO.fo_p(f, gun, "+") < 0.01 and FO.fo_p(f, gun, "-") > 0.99)
kontrol("n < 30 -> NaN", np.isnan(FO.fo_p(f[:20], gun[:20], "+")))

print("9) cetvel çağrısı")
P_ = OC.oc_panel(Vd)
Xa = X[X.satir == "SP_k10"]
S = FO.fo_olc_satir(Xa, {"ABD": P_})
J = FO.fo_satir_sonuc(S, "SP_k10")
kontrol("fo_olc_satir hücre tablosu 3 dönem", len(S["hucre"]) == 3, S["hucre"][["donem", "n"]].to_dict("records"))
kontrol("etiket beklenen / ters var", "genel" in J["etiket"] and "genel" in J["etiket_ters"])
kontrol("hücrelerde durum_yon / durum_ters", all("durum_yon" in h and "durum_ters" in h for h in J["hucre"]))
kontrol("AVR yok -> etiket AVR verisi yok ya da ÖLÇÜLEMEDİ", J["etiket"]["genel"] in ("ÖLÇÜLEMEDİ", "VERİ YOK") or "AVR" in J["etiket"]["genel"]
        or J["etiket"]["genel"].startswith(("EMARE", "DESTEKLENMEDİ")), J["etiket"]["genel"])
T = pd.DataFrame([{"pazar": p, "donem": dn_, "n": 2000, "tutar": False, "ort_fark": 0.01, "ust95": 0.02, "sira": 0.5, "portfoy": 0.3,
                   "portfoy_esli_p10": 0.1, "yari1_fark": 0.01, "yari2_fark": 0.0, "olas": "YOK"}
                  for p in ("ABD", "AVR") for dn_ in ("2023", "2024-26")])
e = FO.fo_etiket(T, "+")
kontrol("güç yeterli + tutmadı -> DESTEKLENMEDİ", e["genel"] == "DESTEKLENMEDİ" and e["genel_cetvel"] == "İZ DEĞİL", e["genel"])
T2 = T.assign(ort_fark=-0.03, ust95=-0.01, sira=0.4, portfoy=0.05, yari1_fark=-0.02, yari2_fark=-0.02)
kontrol("ayna dört hücre -> İZ (S- yönü)", FO.fo_etiket(T2, "-")["genel"] == "İZ")
say = FO.fo_sayim(X, P_)
kontrol("sayım getirisiz (r60 / fark anahtarı yok)", all("r60" not in json_k for v in say.values() for json_k in v["dusme"]))

print("10) kapı")
with tempfile.TemporaryDirectory() as td:
    try:
        FO.fo_onkayit_dogrula(os.path.join(td, "yok.md")); kontrol("ön kayıt yok -> durur", False)
    except FO.FOHata:
        kontrol("ön kayıt yok -> durur", True)
    yb = os.path.join(td, "ON_KAYIT.md")
    open(yb, "w", encoding="utf-8").write("# bozuk\n")
    try:
        FO.fo_onkayit_dogrula(yb); kontrol("ön kayıt bozuk -> durur", False)
    except FO.FOHata:
        kontrol("ön kayıt bozuk -> durur", True)
    open(yb, "w", encoding="utf-8").write(f"FO_ESIK_SHA: `{'0' * 64}`\nFO_KOD_SHA: `{'0' * 64}`\nIS_TANIMI_SHA: `{'0' * 64}`\nZAMAN (UTC): `x`\n")
    try:
        FO.fo_onkayit_dogrula(yb, git=False); kontrol("sha tutmuyor -> durur", False)
    except FO.FOHata as ex:
        kontrol("sha tutmuyor -> durur", "sha tutmuyor" in str(ex))
    yk = os.path.join(td, "K.md")
    open(yk, "w", encoding="utf-8").write(FO.fo_kontrol_tablosu())
    import IZ_KARNE as IK
    kontrol("kontrol listesi 14 satır kapıdan geçer", IK.ik_kontrol_kapisi(yk)["gecti"] and len(FO.FO_KONTROL) == 14)

print("11) e-posta / anahtar")
temiz = True
for ad in ("FITIL_OBEK.py", "test_fitil_obek.py"):
    m = open(os.path.join(KOK, ad), encoding="utf-8").read()
    m = m.replace("noreply@anthropic.com", "")
    if FO._FO_EPOSTA.search(m) or FO._FO_ANAHTAR.search(m):
        temiz = False
kl = FO.FO_YOL["cikti"]
for ad in ("ON_KAYIT.md", "RAPOR.md", "sonuc.json"):
    y = os.path.join(kl, ad)
    if os.path.exists(y):
        m = open(y, encoding="utf-8").read()
        if FO._FO_EPOSTA.search(m) or FO._FO_ANAHTAR.search(m):
            temiz = False
kontrol("kod ve çıktılarda e-posta / anahtar yok", temiz)
kontrol("çakışma kapısı fonksiyonu var", callable(getattr(FO, "_cakisma_kontrol_fo", None)))

print(f"\nSONUÇ: {len(GECTI)} geçti, {len(KALDI)} kaldı" + (f" -> {KALDI}" if KALDI else ""))
sys.exit(1 if KALDI else 0)
