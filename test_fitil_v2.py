"""test_fitil_v2 — FITIL_V2.py sentetik testleri (veri gerekmez; etiket seti testi repodaki kor_anahtar / kor_cevap json'larını okur).

1) ölçüler elle (HAT, düz, önceki 30 dip, düşüş, yol, tepe)   2) TAM sentetik seride tutar; her şart tek tek bozulunca düşer ve düşüren doğru
3) geleceğe bakma: seri t'de kesilince ölçüler / bayraklar tam seriyle aynı (bütün günler); fv_gelecek_denetimi bozuk olayda DURUR
4) ızgara 72 nokta, tekil, sadelik sırası, seçim eşitlik bozma   5) etiket seti sayıları (E 19 = 7 + 12, NEG 10) ve r alanları okunmaz
6) puan / tasarım uçtan uca (sentetik getir)   7) kırılım / stop   8) kör cevap ayrıştırma ve karar kuralı   9) kör sayfa ad / tarih sızıntısı yok
10) V2_SECIM ızgarada ve TASARIM.md ile aynı; mühür seçimi kapsar   11) kapı: ön kayıt yok / bozuk / sha tutmuyor -> durur; kontrol listesi 14 satır
12) e-posta / anahtar taraması; çakışma kapısı
Çalıştır: python test_fitil_v2.py
"""
import copy
import json
import os
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
warnings.filterwarnings("ignore")

import FITIL_V2 as FV  # noqa: E402

GECTI, KALDI = [], []


def kontrol(ad, kosul, ek=""):
    (GECTI if kosul else KALDI).append(ad)
    print(("  OK   " if kosul else "  HATA ") + ad + (f"  ({ek})" if ek else ""))


def rastgele_hisse(n, tohum, bas="2016-01-01"):
    rng = np.random.default_rng(tohum)
    C = 50 * np.exp(np.cumsum(rng.normal(0.0, 0.02, n)))
    O = C * (1 + rng.normal(0, 0.006, n))
    a = rng.uniform(0, 0.02, n); b = rng.uniform(0, 0.02, n)
    H = np.maximum(O, C) * (1 + b); L = np.minimum(O, C) * (1 - a)
    V = rng.integers(5000, 80000, n).astype(float)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=pd.bdate_range(bas, periods=n))


DUZ_BAR = 180


def tam_seri():
    """TAM'ı (ve bağlam DİP'i) son günde tutan sentetik seri: 180 bar 100'de yatay, 60 bar 100 -> 70 düşüş, 10 bar 70 tabanında S+ mumları
    (alt fitil yok, üst fitil uzun), kapanış HAT'ın %3 üstünde."""
    rows = []
    for i in range(DUZ_BAR):
        rows.append((100.0, 101.0, 99.0, 100.0))
    for i in range(60):
        c = 100.0 - 30.0 * (i + 1) / 60
        rows.append((c + 0.3, c + 0.8, c - 0.8, c))
    for i in range(10):
        L = 70.0 + (0.3 if i % 2 else 0.0)
        O = L; C = L + 0.6; H = L + 2.0   # alt fitil 0, üst fitil (2,0 - 0,6) / 2,0 = 0,70
        rows.append((O, H, L, C))
    d = pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"], index=pd.bdate_range("2020-01-01", periods=len(rows)))
    d["Volume"] = 1000.0
    return d


S = FV.V2_SECIM

print("1) ölçüler elle")
d = tam_seri(); M = FV.fv_olcu(d); t = d.index[-1]; m = M.loc[t]
W = d.iloc[-10:]
kontrol("HMAXW9 = t hariç önceki 9 bar max High", abs(m.HMAXW9 - d.iloc[-10:-1].High.max()) < 1e-12)
kontrol("HAT = min(Low, W)", abs(m.HAT - W.Low.min()) < 1e-12, m.HAT)
kontrol("düz = (max L - HAT) / medyan R", abs(m.DUZ - (W.Low.max() - W.Low.min()) / (W.High - W.Low).median()) < 1e-12, round(m.DUZ, 3))
kontrol("önceki 30 dip = W öncesi 30 bar min Low", abs(m.ONC30 - d.iloc[-40:-10].Low.min()) < 1e-12)
kontrol("düşüş = 1 - C / W öncesi 60 bar max Close", abs(m.DUSUS - (1 - d.Close.iloc[-1] / d.iloc[-70:-10].Close.max())) < 1e-12, round(m.DUSUS, 3))
kontrol("yol = C / HAT - 1", abs(m.YOL - (d.Close.iloc[-1] / W.Low.min() - 1)) < 1e-12)
kontrol("tepe = 1 - C / 120 bar max Close (t dahil)", abs(m.TEPE - (1 - d.Close.iloc[-1] / d.iloc[-120:].Close.max())) < 1e-12)
kontrol("ASIM / ALTYOK (S+ mumları)", m.ASIM > 0.5 and m.ALTYOK == 1.0, f"{m.ASIM:.2f} {m.ALTYOK:.2f}")
kontrol("geçmiş yetersizken ölçü tanımsız (NaN)", np.isnan(FV.fv_olcu(d.iloc[:100]).MAXC120.iloc[-1]) and np.isnan(FV.fv_olcu(d.iloc[:60]).MAXC60.iloc[-1]))

print("2) TAM ve tek tek şart bozma")
Z = FV.fv_kural(M, S)
kontrol("TAM son günde tutar", bool(Z.TAM.iloc[-1]), FV.fv_dusuren(Z.iloc[-1]))
kontrol("bilgi satırları TAM'ı kapsar", bool(Z.S1.iloc[-1] and Z.S12.iloc[-1] and Z.S123.iloc[-1]))


def bozuk(f):
    x = tam_seri(); f(x); Mx = FV.fv_olcu(x); Zx = FV.fv_kural(Mx, S); return Zx.iloc[-1]


def alt_fitil(x):
    x.iloc[-10:, x.columns.get_loc("Low")] = x.iloc[-10:].Open.to_numpy() - 0.6
z = bozuk(alt_fitil)
kontrol("(1) alt fitil eklenince şekil düşer", not z.s1 and not z.TAM and "(1)" in FV.fv_dusuren(z))


def yeni_dip(x):
    x.iloc[-5, x.columns.get_loc("Low")] = 60.0
z = bozuk(yeni_dip)
kontrol("(2) önceki 30 dibin %2 altına inen HAT -> hat kırık", not z.s2 and not z.TAM and any("yeni dip" in a for a in FV.fv_dusuren(z)))


def az_dusus(x):
    x.iloc[:DUZ_BAR + 60, :4] = x.iloc[:DUZ_BAR + 60, :4] * 0 + np.array([72.0, 72.5, 71.5, 72.0])
z = bozuk(az_dusus)
kontrol("(3) düşüş < %20 -> dönüm düşer", not z.s3 and not z.TAM)


def yol_almis(x):
    x.iloc[-1, :4] = [76.0, 79.0, 75.5, 78.0]
z = bozuk(yol_almis)
kontrol("(4) C > HAT x 1,10 -> yol almış", not z.s4 and not z.TAM and any("hattan uzak" in a for a in FV.fv_dusuren(z)))


def tepe_kir(x):
    x.iloc[-1, :4] = [70.0, 73.0, 70.0, 72.4]   # önceki 9 barın en yüksek High'ı 72,3: kapanış 72,4 > 72,3 (fitilli mumda da)
z = bozuk(tepe_kir)
kontrol("(4) kapanış t hariç pencere tepesini kırınca (SAPMA-1) -> düşer", not z.s4_tepe and not z.TAM and any("pencere tepesini" in a for a in FV.fv_dusuren(z)))


def tepe_esit(x):
    x.iloc[-1, :4] = [70.0, 73.0, 70.0, 72.3]
z = bozuk(tepe_esit)
kontrol("(4) kapanış = önceki 9 bar tepesi -> tutar (<=)", bool(z.s4_tepe))
kontrol("(4) kapanış pencere tepesinin altında -> tutar", bool(FV.fv_kural(FV.fv_olcu(tam_seri()), S).s4_tepe.iloc[-1]))


def tepede(x):
    x.iloc[:DUZ_BAR, :4] = x.iloc[:DUZ_BAR, :4] * 0 + np.array([80.0, 80.5, 79.5, 80.0])
    for i in range(60):
        c = 80.0 - 0.5 * (i + 1) / 60
        x.iloc[DUZ_BAR + i, :4] = [c + 0.1, c + 0.3, c - 0.3, c]
    x.iloc[-10:, :4] = x.iloc[-10:, :4] - 70.0 + 78.0
z = bozuk(tepede)
kontrol("(5) 120 bar tepesinin %15'ten yakını -> tepede", not z.s5 and not z.TAM)

print("2b) bağlam (EK) ve ayna")
kontrol("tam seri: bağlam DİP, TAM_DIP tutar", FV.fv_baglam(Z.iloc[-1]) == "DİP" and bool(Z.TAM_DIP.iloc[-1]), round(float(M.KONUM.iloc[-1]), 3))
kontrol("KONUM = (C - min L 250) / (max H 250 - min L 250)", abs(M.KONUM.iloc[-1] - (d.Close.iloc[-1] - d.iloc[-250:].Low.min()) /
                                                                  (d.iloc[-250:].High.max() - d.iloc[-250:].Low.min())) < 1e-12)
kontrol("250 bar yoksa TANIMSIZ, TAM_DIP yok", FV.fv_baglam(FV.fv_kural(FV.fv_olcu(d.iloc[-249:]), S).iloc[-1]) == "TANIMSIZ"
        and not FV.fv_kural(FV.fv_olcu(d.iloc[-249:]), S).TAM_DIP.iloc[-1])
yuk = pd.DataFrame({"Open": np.linspace(10, 100, 300), "Close": np.linspace(10, 100, 300) - 0.05}, index=pd.bdate_range("2020-01-01", periods=300))
yuk["High"] = yuk.Open + 0.02; yuk["Low"] = yuk.Close - 0.6; yuk["Volume"] = 1000.0   # üst fitilsiz, uzun alt fitil = S- mumu, tepede
Zy = FV.fv_kural(FV.fv_olcu(yuk), S)
kontrol("yükselen seride bağlam TEPE ve S- -> SM_TEPE", FV.fv_baglam(Zy.iloc[-1]) == "TEPE" and bool(Zy.SM_TEPE.iloc[-1]))
orta = yuk.copy(); orta.iloc[-20:, :4] = orta.iloc[-20:, :4].to_numpy() * 0.6
Zo = FV.fv_kural(FV.fv_olcu(orta), S)
kontrol("ortaya inen seride bağlam ORTA", FV.fv_baglam(Zo.iloc[-1]) == "ORTA", round(float(FV.fv_olcu(orta).KONUM.iloc[-1]), 2))
kontrol("satır listesi: ana TAM_DIP, ayna SM_TEPE yön -", FV.V2_ESIK["ana"] == ["TAM_DIP"] and FV.V2_ESIK["yon"]["SM_TEPE"] == "-"
        and set(FV.V2_ESIK["yon"]) == set(FV.V2_ESIK["satirlar"]))

print("3) geleceğe bakma")
h = rastgele_hisse(600, 3)
M1 = FV.fv_olcu(h); Z1 = FV.fv_kural(M1, S); fark = 0
for k in range(150, 600, 7):
    Mk = FV.fv_olcu(h.iloc[:k + 1]); Zk = FV.fv_kural(Mk, S)
    a = M1.iloc[k].to_numpy(float); b = Mk.iloc[-1].to_numpy(float)
    if not np.allclose(a, b, equal_nan=True) or not (Z1.iloc[k] == Zk.iloc[-1]).all():
        fark += 1
kontrol("seri t'de kesilince ölçü ve bayraklar aynı (65 gün)", fark == 0, fark)
Vd = {"V": {"AAA": d}, "evren_bas": {}}
X = pd.DataFrame({"sembol": ["AAA"], "tarih": [d.index[-1]], "pazar": ["BIST"], "satir": ["TAM_DIP"], "baglam": ["DİP"]})
kontrol("gelecek denetimi doğru olayda TUTAR", FV.fv_gelecek_denetimi(Vd, X, "BIST") == 1)
try:
    FV.fv_gelecek_denetimi(Vd, X.assign(tarih=[d.index[-30]]), "BIST"); kontrol("gelecek denetimi bozuk olayda DURUR", False)
except FV.FVHata:
    kontrol("gelecek denetimi bozuk olayda DURUR", True)
Xs = FV.fv_sinyaller(Vd, "BIST", kirilim=True)
kontrol("fv_sinyaller TAM_DIP günü bağlamla verir", ((Xs.satir == "TAM_DIP") & (Xs.tarih == d.index[-1]) & (Xs.baglam == "DİP")).any())

print("4) ızgara ve sadelik")
G = FV.fv_izgara()
kontrol("ızgara 72 nokta, tekil", len(G) == 72 and len({json.dumps({k: g[k] for k in g if k != 'no'}, sort_keys=True) for g in G}) == 72)
kontrol("ızgara 3 x 2 x 2 x 3 x 2 değerleri", sorted({str(g["duz"]) for g in G}) == ["1.0", "1.5", "None"] and {g["sekil"] for g in G} == {"S+", "gevsek"}
        and {g["dusus"] for g in G} == {0.10, 0.15, 0.20} and {g["hatTol"] for g in G} == {0.02, 0.03} and {g["yol"] for g in G} == {0.05, 0.10})
en_sade = min(G, key=FV.fv_sadelik)
kontrol("en sade = düz kapalı, S+, 0,02, 0,10, 0,10", (en_sade["duz"], en_sade["sekil"], en_sade["hatTol"], en_sade["dusus"], en_sade["yol"]) ==
        (None, "S+", 0.02, 0.10, 0.10))
sonuc = [{"nokta": g, "puan": {"puan": 5 if g["no"] in ("N05", "N66") else 3}} for g in G]
kontrol("seçim: eşitlikte sade (N66 düz kapalı > N05 düz 1,0)", FV.fv_secim_yap(sonuc)["nokta"]["no"] == "N66")

print("5) etiket seti")
et = FV.fv_etiket_seti()
say = pd.Series([e["sinif"] for e in et]).value_counts().to_dict()
kontrol("E-GİRİŞ 7, E-ŞEKİL 12, NEG 10, ÖRNEK+ 3, NEG-ARALIK 2", say == {"E-SEKIL": 12, "NEG": 10, "E-GIRIS": 7, "ORNEK+": 3, "NEG-ARALIK": 2}, say)
kontrol("etiketlerde r20 / r60 alanı yok", all("r20" not in e and "r60" not in e for e in et))
kontrol("NEG = H + (SM ve E değil)", sorted(e["no"] for e in et if e["sinif"] == "NEG") == [1, 2, 4, 7, 13, 15, 33, 46, 48, 50])

print("6) puan / tasarım uçtan uca (sentetik)")
with tempfile.TemporaryDirectory() as td:
    A = {"sayfalar": [{"no": 1, "pazar": "BIST", "sembol": "AAA", "tarih": str(d.index[-1].date()), "grup": "SP_ic", "r20": 9.9, "r60": 9.9},
                      {"no": 2, "pazar": "BIST", "sembol": "AAA", "tarih": str(d.index[-60].date()), "grup": "SP_ic"},
                      {"no": 3, "pazar": "BIST", "sembol": "AAA", "tarih": str(d.index[-1].date()), "grup": "SP_ic"}]}
    Cv = {"cevap": {"1": "E", "2": "H", "3": "E"}, "not": {}}
    ya, yc = os.path.join(td, "a.json"), os.path.join(td, "c.json")
    json.dump(A, open(ya, "w")); json.dump(Cv, open(yc, "w"))
    E0 = copy.deepcopy(FV.V2_ESIK["etiket"])
    FV.V2_ESIK["etiket"]["E_GIRIS"] = [1]
    FV.V2_ESIK["etiket"]["ornek_poz"] = [{"ad": "AAA", "pazar": "BIST", "bas": str(d.index[-3].date()), "son": str(d.index[-1].date())}]
    FV.V2_ESIK["etiket"]["neg_aralik"] = [{"ad": "AAA", "pazar": "BIST", "bas": str(d.index[-150].date()), "son": str(d.index[-100].date())}]
    try:
        T = FV.fv_tasarim(getir=lambda p, s: d, anahtar_yol=ya, cevap_yol=yc)
    finally:
        FV.V2_ESIK["etiket"] = E0
    R = next(x for x in T["sonuc"] if x["nokta"]["no"] == S["no"])
    kontrol("seçilen noktada E-GİRİŞ / örnek / NEG / NEG aralık doğru, E-ŞEKİL (TAM tuttu) yanlış",
            R["puan"]["yakalanan_E_GIRIS"] == 1 and R["puan"]["yakalanan_ORNEK"] == 1 and R["puan"]["elenen_NEG"] == 1
            and R["puan"]["elenen_NEG_ARALIK"] == 1 and R["puan"]["sekil_E_SEKIL"] == 0, R["puan"])
    kontrol("tasarım metni SECIM_JSON satırı taşır", "SECIM_JSON: `" in FV.fv_tasarim_metni(T))

print("7) kırılım / stop")
C = np.array([10, 10, 10.5, 11.2, 9, 9], float)
kontrol("önce kırılım", FV.fv_kirilim(C, 0, 11.0, 9.5, ufuk=4) == "KIRILIM")
C2 = np.array([10, 10, 9.2, 11.2, 9, 9], float)
kontrol("önce stop (HAT x 0,98 altı)", FV.fv_kirilim(C2, 0, 11.0, 9.5, ufuk=4) == "STOP")
kontrol("hiçbiri -> YOK; bar yetmez -> ÖLÇÜLMEZ", FV.fv_kirilim(np.full(6, 10.0), 0, 11, 9.5, ufuk=4) == "YOK" and
        FV.fv_kirilim(C, 3, 11, 9.5, ufuk=4) == "OLCULMEZ")

print("8) kör cevap ve karar")
c = FV.fv_cevap_ayristir("1:E, 2:h 3:B", 3)
kontrol("ayrıştırma", c == {1: "E", 2: "H", 3: "B"})
for bozuk_metin in ("1:E,2:E", "1:E,1:H,2:B,3:B", "1:X,2:E,3:E"):
    try:
        FV.fv_cevap_ayristir(bozuk_metin, 3); kontrol(f"bozuk yanıt durur ({bozuk_metin})", False)
    except FV.FVHata:
        kontrol(f"bozuk yanıt durur ({bozuk_metin})", True)
kontrol("karar kuralı", FV.fv_kor_karar(0.7, 0.3) == "GÖZLE UYUMLU" and FV.fv_kor_karar(0.7, 0.5) == "KISMİ" and FV.fv_kor_karar(0.3, 0.0) == "GÖZLE UYUMSUZ")

print("8b) kısmi yanıt ('-', eksik_izin, dosya, yanıtsız dışlama)")
c = FV.fv_cevap_ayristir("1:E, 2:-, 3:b", 3)
kontrol("'-' yanıtsız ayrışır", c == {1: "E", 2: "-", 3: "B"})
try:
    FV.fv_cevap_ayristir("1:E,3:H", 3); kontrol("eksik numara eksik_izin olmadan durur", False)
except FV.FVHata:
    kontrol("eksik numara eksik_izin olmadan durur", True)
kontrol("eksik_izin: yazılmayan numara yanıtsız", FV.fv_cevap_ayristir("1:E,3:H", 3, eksik_izin=True) == {1: "E", 2: "-", 3: "H"})
with tempfile.TemporaryDirectory() as td:
    yc = os.path.join(td, "cv.json")
    Y = {"1": ("E", "açık"), "2": ("H", "çıkarım"), "3": ("-", "yanıtsız"), "4": ("B", "açık"), "5": ("E", "açık"), "6": ("-", "yanıtsız")}
    json.dump({"yanit": {k: {"etiket": e, "tur": t} for k, (e, t) in Y.items()}}, open(yc, "w", encoding="utf-8"), ensure_ascii=False)
    cd, td_, sha = FV.fv_cevap_dosya_oku(yc, 6)
    kontrol("dosyadan okuma (etiket + tur + sha)", cd == {1: "E", 2: "H", 3: "-", 4: "B", 5: "E", 6: "-"} and td_[2] == "çıkarım" and len(sha) == 64)
    json.dump({"yanit": {"1": {"etiket": "E", "tur": "yanıtsız"}}}, open(os.path.join(td, "b.json"), "w", encoding="utf-8"), ensure_ascii=False)
    try:
        FV.fv_cevap_dosya_oku(os.path.join(td, "b.json"), 1); kontrol("etiket / tur çelişkisi durur", False)
    except FV.FVHata:
        kontrol("etiket / tur çelişkisi durur", True)
    # yanıtsız dışlama: sentetik anahtar (TAM 1-4, DEĞİL 5-6) üzerinde fv_olc
    os.makedirs(os.path.join(td, "c"))
    A = {"sayfalar": [{"no": i, "grup": "TAM" if i <= 4 else "DEGIL", "pazar": "BIST" if i % 2 else "ABD", "r20": 0.01 * i, "r60": 0.02 * i,
                       "once": "STOP" if i % 2 else "KIRILIM"} for i in range(1, 7)]}
    json.dump(A, open(os.path.join(td, "c", FV.FV_DOSYA["anahtar"]), "w", encoding="utf-8"))
    o = FV.fv_olc(cikti=os.path.join(td, "c"), cevap_dosya=yc)
    kontrol("yanıtsız paylardan çıkar (TAM n 3, E payı 1/3; DEĞİL n 1)", o["TAM"]["n"] == 3 and abs(o["TAM"]["E_payi"] - 1 / 3) < 1e-12
            and o["TAM"]["yanitsiz"] == 1 and o["DEGIL"]["n"] == 1 and o["DEGIL"]["E_payi"] == 1.0, o["TAM"])
    kontrol("n_yanitli / yanıtsız listesi", o["n_yanitli"] == 4 and o["yanitsiz"] == [3, 6] and o["n_yanitsiz"] == 2)
    kontrol("çapraz tablo ve tur kırılımı", o["capraz"]["-"] == {"TAM": 1, "DEGIL": 1} and o["capraz"]["E"] == {"TAM": 1, "DEGIL": 1}
            and o["tur"]["çıkarım"]["TAM"]["H"] == 1 and o["tur"]["açık"]["TAM"]["n"] == 2)
    kontrol("karar kuralı yanıtlı n ile", o["karar"] == FV.fv_kor_karar(1 / 3, 1.0) == "GÖZLE UYUMSUZ")
    kontrol("sonuç bilgisi yanıtsızı dışlar (TAM H: no 2 r60)", o["sonuc_bilgi"]["H"]["n"] == 1 and abs(o["sonuc_bilgi"]["H"]["r60_medyan"] - 0.04) < 1e-12
            and o["sonuc_bilgi"]["H"]["kirilim_payi"] == 1.0)
    try:
        FV.fv_olc("1:E", cikti=os.path.join(td, "c"), cevap_dosya=yc); kontrol("--cevap ve --cevap-dosya birlikte durur", False)
    except FV.FVHata:
        kontrol("--cevap ve --cevap-dosya birlikte durur", True)
    o2 = FV.fv_olc("1:E,2:H,3:E,4:B,5:H,6:B", cikti=os.path.join(td, "c"))
    kontrol("tam metin yanıt eski davranış (n 4, yanıtsız 0)", o2["TAM"]["n"] == 4 and o2["n_yanitsiz"] == 0 and o2["tur"] is None)

print("9) kör sayfa sızıntı")
h2 = rastgele_hisse(300, 5, bas="2019-03-01")
fig = FV.fv_kor_sayfa(h2, h2.index[250], 7)
kontrol("kör sayfa önce 120 mum (EK)", FV.V2_ESIK["kor2"]["once"] == 120)
import FITIL_KOR as FK  # noqa: E402
metin = " ".join(FK._fk_metinler(fig))
kontrol("sayfada tarih / yıl yok", "2019" not in metin and "AAA" not in metin)
import matplotlib.pyplot as plt  # noqa: E402
plt.close(fig)
try:
    FV.fv_kor_sayfa(h2, h2.index[100], 1); kontrol("kısa pencere durur", False)
except FV.FVHata:
    kontrol("kısa pencere durur", True)

print("10) seçim ve mühür")
kontrol("V2_SECIM ızgarada", any(g["no"] == S["no"] and all(g[k] == S[k] for k in ("sekil", "duz", "hatTol", "dusus", "yol")) for g in G))
ty = os.path.join(FV.FV_YOL["cikti"], FV.FV_DOSYA["tasarim"])
if os.path.exists(ty):
    kontrol("V2_SECIM == TASARIM.md SECIM_JSON", FV.fv_secim_denetle(ty)["no"] == S["no"])
s0 = FV.fv_esik_sha(); FV.V2_SECIM = dict(S, dusus=0.10); s1 = FV.fv_esik_sha(); FV.V2_SECIM = S
kontrol("mühür seçimi kapsar", s0 != s1 and FV.fv_esik_sha() == s0)

print("11) kapı")
with tempfile.TemporaryDirectory() as td:
    try:
        FV.fv_onkayit_dogrula(os.path.join(td, "yok.md"), git=False); kontrol("ön kayıt yok -> durur", False)
    except FV.FVHata:
        kontrol("ön kayıt yok -> durur", True)
    yb = os.path.join(td, "ON_KAYIT.md")
    open(yb, "w", encoding="utf-8").write("bozuk")
    try:
        FV.fv_onkayit_dogrula(yb, git=False); kontrol("ön kayıt bozuk -> durur", False)
    except FV.FVHata:
        kontrol("ön kayıt bozuk -> durur", True)
    open(yb, "w", encoding="utf-8").write("".join(f"{k}: `{'0' * 64}`\n" for k in ("V2_ESIK_SHA", "V2_KOD_SHA", "IS_TANIMI_SHA", "TASARIM_SHA",
                                                                                 "KOR_ANAHTAR_SHA", "KOR_CEVAP_SHA")) + "ZAMAN (UTC): `x`\n")
    import shutil
    if os.path.exists(ty):
        shutil.copy(ty, os.path.join(td, "TASARIM.md"))
        try:
            FV.fv_onkayit_dogrula(yb, git=False, cikti=td); kontrol("sha tutmuyor -> durur", False)
        except FV.FVHata as ex:
            kontrol("sha tutmuyor -> durur", "sha tutmuyor" in str(ex))
    yk = os.path.join(td, "K.md")
    open(yk, "w", encoding="utf-8").write(FV.fv_kontrol_tablosu())
    import IZ_KARNE as IK
    kontrol("kontrol listesi 14 satır kapıdan geçer", IK.ik_kontrol_kapisi(yk)["gecti"] and len(FV.FV_KONTROL) == 14)

print("12) e-posta / anahtar, çakışma kapısı")
temiz = True
for ad in ("FITIL_V2.py", "test_fitil_v2.py"):
    m = open(os.path.join(KOK, ad), encoding="utf-8").read().replace("noreply@anthropic.com", "")
    if FV._FV_EPOSTA.search(m) or FV._FV_ANAHTAR.search(m):
        temiz = False
for ad in FV.FV_DOSYA.values():
    y = os.path.join(FV.FV_YOL["cikti"], ad)
    if os.path.exists(y) and not y.endswith(".pdf"):
        m = open(y, encoding="utf-8").read()
        if FV._FV_EPOSTA.search(m) or FV._FV_ANAHTAR.search(m):
            temiz = False
kontrol("kod ve çıktılarda e-posta / anahtar yok", temiz)
kontrol("çakışma kapısı fonksiyonu var", callable(getattr(FV, "_cakisma_kontrol_fv", None)))

print(f"\nSONUÇ: {len(GECTI)} geçti, {len(KALDI)} kaldı" + (f" -> {KALDI}" if KALDI else ""))
sys.exit(1 if KALDI else 0)
