"""test_canli_tarama — CANLI_TARAMA.py sentetik testleri (gerçek veri ve ağ gerekmez).

1) birleştirme: yeni bar ekleme, ortak gün aynı -> ölçek yok; tek tip oran (temettü) -> eski kısım yeni kipe; oran > %40 -> şüpheli;
   yeni barda |getiri| > %40 -> şüpheli; yarım bar sınırı; AVR Kur ileri taşınır
2) yarım bar sınırı (pazar kapanış saatinden önce / sonra)
3) sinyal seçimi: havuz dışı düşer, 60 gün tekil, yalnız son 5 gün
4) havuz kademeleri: Ş1 VE Ş7 -> (i) Ş1 VE F22 > 0 -> (ii) Ş1 -> boş; kademe atlanmaz
5) sıralama: puan7 azalan, eşitlikte Ş9 önce, sonra F18 küçük; en iyi 10; pazar başına en çok 5
6) aday alanları + json alanları (dürüstlük, ileri test, ölçüm tarihi = sinyal + 15 iş günü)
7) puan7 matrisi = YH._yh_matris7 (aynı eğitim medyanı, NaN bayrakları)
8) olc hesabı = YAPI_HEDEF cetveli: yh_olay_olc satırı elle yh_sim ile (giriş t+1 açılış, stop0 = hat x 0,98); uçtan uca ct_olc ->
   CANLI_SONUC.md eklenir (ikinci ölçüm eskisini silmez), OLCULDU işareti
9) geleceğe bakma: özellikler (F1-F29, Ş10, mahkeme) seri t'de kesilince ve t sonrası değişince aynı
10) kriz kesiği bağlamı geri yüklenir; e-posta / anahtar taraması; çakışma kapısı; ön kayıt sha kapısı
Çalıştır: python test_canli_tarama.py
"""
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

import CANLI_TARAMA as CT  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import SIKISMA_YENIDEN as SY  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

GECTI, KALDI = [], []


def kontrol(ad, kosul, ek=""):
    (GECTI if kosul else KALDI).append(ad)
    print(("  OK   " if kosul else "  HATA ") + ad + (f"  ({ek})" if ek else ""))


def rastgele_hisse(n, tohum, bas="2016-01-01", oyn=0.02, kur=False):
    rng = np.random.default_rng(tohum)
    C = 50 * np.exp(np.cumsum(rng.normal(0.0, oyn, n)))
    O = C * (1 + rng.normal(0, 0.006, n))
    a = rng.uniform(0, 0.02, n); b = rng.uniform(0, 0.02, n)
    H = np.maximum(O, C) * (1 + b); L = np.minimum(O, C) * (1 - a)
    V = rng.integers(5000, 80000, n).astype(float)
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=pd.bdate_range(bas, periods=n))
    if kur:
        d["Kur"] = 1.1
    return d


# ---------------------------------------------------------------- 1) birleştirme
print("1) birleştirme")
e = rastgele_hisse(300, 1)
y = e.iloc[-50:].copy()
ek = rastgele_hisse(10, 2, bas=str((e.index[-1] + pd.offsets.BDay(1)).date()))
ek = ek * (e.Close.iloc[-1] / ek.Close.iloc[0])
y = pd.concat([y, ek])
B, b = CT.ct_birlestir(e, y, pd.Timestamp("2100-01-01"))
kontrol("10 yeni bar eklendi, ortak gün aynı -> ölçek yok", b["yeni_bar"] == 10 and not b["olcek"] and b["fark_gun"] == 0 and len(B) == 310)
kontrol("eski tarihler korundu (ortak öncesi aynı)", np.allclose(B.Close.iloc[:250].to_numpy(), e.Close.iloc[:250].to_numpy()))
y2 = y.copy(); y2[["Open", "High", "Low", "Close"]] *= 0.97
B2, b2 = CT.ct_birlestir(e, y2, pd.Timestamp("2100-01-01"))
kontrol("tek tip oran 0,97 -> eski kısım yeni kipe ölçeklendi", b2["olcek"] and abs(b2["oran"] - 0.97) < 1e-9 and b2["fark_gun"] == 50
        and np.allclose(B2.Close.iloc[:250].to_numpy(), e.Close.iloc[:250].to_numpy() * 0.97) and not b2["supheli"])
kontrol("ölçek sonrası birleşim sürekli (ortak ilk gün oranı 1)", abs(B2.Close.iloc[250] / B2.Close.iloc[249] - e.Close.iloc[250] / e.Close.iloc[249]) < 1e-9)
y3 = y.copy(); y3[["Open", "High", "Low", "Close"]] *= 0.5
_, b3 = CT.ct_birlestir(e, y3, pd.Timestamp("2100-01-01"))
kontrol("oran 0,5 (bölünme / birim) -> şüpheli", b3["supheli"] and "oran" in b3["neden"])
y3b = y.copy(); y3b.iloc[:20, [y3b.columns.get_loc(c) for c in ("Open", "High", "Low", "Close")]] *= 1.6
_, b3b = CT.ct_birlestir(e, y3b, pd.Timestamp("2100-01-01"))
kontrol("ortak günlerde oran tek tip değil (1,0 / 1,6) -> şüpheli (SAPMA 1)", b3b["supheli"] and "tek tip değil" in b3b["neden"])
y4 = y.copy(); y4.iloc[-3, y4.columns.get_loc("Close")] *= 1.6
_, b4 = CT.ct_birlestir(e, y4, pd.Timestamp("2100-01-01"))
kontrol("yeni barda +%60 -> şüpheli", b4["supheli"] and "getiri" in b4["neden"])
B5, b5 = CT.ct_birlestir(e, y, ek.index[-3])
kontrol("yarım bar sınırı: sınırdan sonraki barlar atıldı", b5["yeni_bar"] == 8 and B5.index.max() == ek.index[-3])
ek_k = rastgele_hisse(300, 1, kur=True); ek_k.iloc[-1, ek_k.columns.get_loc("Kur")] = 1.2
B6, _ = CT.ct_birlestir(ek_k, y, pd.Timestamp("2100-01-01"))
kontrol("AVR Kur yeni barlarda son bilinen Kur (1,2)", "Kur" in B6 and np.allclose(B6.Kur.iloc[-10:].to_numpy(), 1.2))

# ---------------------------------------------------------------- 2) yarım bar
print("2) yarım bar sınırı")
kontrol("ABD 18:00 UTC -> dün", CT.ct_yarim_bar_sinir("ABD", pd.Timestamp("2026-11-20 18:00")) == pd.Timestamp("2026-11-19"))
kontrol("ABD 22:00 UTC -> bugün", CT.ct_yarim_bar_sinir("ABD", pd.Timestamp("2026-11-20 22:00")) == pd.Timestamp("2026-11-20"))
kontrol("BIST 17:30 UTC -> bugün", CT.ct_yarim_bar_sinir("BIST", pd.Timestamp("2026-11-20 17:30")) == pd.Timestamp("2026-11-20"))

# ---------------------------------------------------------------- 3) sinyal seçimi
print("3) sinyal seçimi")
idx = pd.bdate_range("2026-01-01", periods=200)
S = ["A", "B", "C"]
ok = np.ones((200, 3), bool); ok[198, 2] = False
Hs = {"tarih": idx, "sembol": S, "kol": {s: i for i, s in enumerate(S)}, "ok": ok, "lik_alt": ~ok, "sup": np.zeros((200, 3), bool)}
A = pd.DataFrame({"sembol": ["A", "A", "B", "B", "C"], "tarih": [idx[150], idx[197], idx[100], idx[196], idx[198]], "hat": 1.0})
sg, say = CT.ct_sinyal_sec(A, Hs)
kontrol("A: 150. gün tutuldu -> 197 (47 gün) tekil düşer", "A" not in set(sg.sembol) and say["tekil"] == 1)
kontrol("B: 100 -> 196 (96 gün) tutulur, son 5 günde", list(sg.sembol) == ["B"] and sg.tarih.iloc[0] == idx[196])
kontrol("C: havuz dışı (t günü) düşer", say["havuz_disi"] == 1 and say["likidite_alt20"] == 1 and say["al_son5"] == 3)

# ---------------------------------------------------------------- 4) havuz kademeleri
print("4) havuz kademeleri")


def F_(n, f15=0.1, f17=-0.3, f22=0.01, f22a=-0.01, f23=0.6, pazar="ABD"):
    d = {c: np.full(n, 1.0) for c in YH.YH_ESIK7["ozellik"]}
    d.update({"F15": np.full(n, f15), "F17": np.full(n, f17), "F22": np.full(n, f22), "F22a": np.full(n, f22a), "F23": np.full(n, f23)})
    X = pd.DataFrame(d); X.insert(0, "pazar", pazar); X.insert(1, "sembol", [f"S{i}" for i in range(n)])
    return X


F0 = pd.concat([F_(2), F_(3, f23=0.2), F_(2, f15=0.9)], ignore_index=True)
H0, hb0 = CT.ct_havuz_sec(F0)
kontrol("kademe 0 (Ş1 VE Ş7): 2 aday", hb0["kademe"] == "S1_S7" and len(H0) == 2 and hb0["sayi"] == {"S1_S7": 2, "S1_F22": 5, "S1": 5})
H1, hb1 = CT.ct_havuz_sec(pd.concat([F_(3, f23=0.2), F_(2, f22=-0.01), F_(2, f15=0.9)], ignore_index=True))
kontrol("kademe (i) Ş1 VE F22 > 0 (gövde şartı yok): 3 aday", hb1["kademe"] == "S1_F22" and len(H1) == 3)
H2, hb2 = CT.ct_havuz_sec(pd.concat([F_(2, f22=-0.01), F_(2, f15=0.9)], ignore_index=True))
kontrol("kademe (ii) Ş1: 2 aday", hb2["kademe"] == "S1" and len(H2) == 2)
H3, hb3 = CT.ct_havuz_sec(F_(2, f17=-0.1))
kontrol("Ş1 yok -> havuz boş (kademe yok)", hb3["kademe"] is None and len(H3) == 0)
Fn = F_(1); Fn.loc[0, "F23"] = np.nan
kontrol("NaN şart tutmaz (Ş7 NaN F23 -> kademe i)", CT.ct_havuz_sec(Fn)[1]["kademe"] == "S1_F22")

# ---------------------------------------------------------------- 5) sıralama
print("5) sıralama")
R = pd.DataFrame({"pazar": ["ABD"] * 7 + ["AVR"] * 3 + ["BIST"] * 3, "sembol": [f"X{i}" for i in range(13)],
                  "puan7": [0.9, 0.8, 0.8, 0.8, 0.7, 0.65, 0.6, 0.5, 0.5, 0.4, 0.3, 0.2, 0.1],
                  "S9": [False, False, True, False, False, False, False, False, False, False, False, False, False],
                  "F18": [0.05, 0.02, 0.09, 0.01, 0.03, 0.03, 0.03, 0.1, 0.05, 0.03, 0.03, 0.03, 0.03]})
Ls = CT.ct_sirala(R)
kontrol("en iyi 10", len(Ls) == 10 and list(Ls.sira) == list(range(1, 11)))
kontrol("eşitlikte Ş9 önce, sonra F18 küçük", list(Ls.sembol[:4]) == ["X0", "X2", "X3", "X1"])
kontrol("pazar başına en çok 5 (ABD X5, X6 atlandı; 11 uygun -> en düşük X12 dışarıda)", (Ls.pazar == "ABD").sum() == 5
        and "X5" not in set(Ls.sembol) and "X6" not in set(Ls.sembol) and "X11" in set(Ls.sembol) and "X12" not in set(Ls.sembol))
kontrol("AVR eşit puanda F18 küçük önce", list(Ls[Ls.pazar == "AVR"].sembol[:2]) == ["X8", "X7"])

# ---------------------------------------------------------------- 6) aday ve json alanları
print("6) aday ve json alanları")
La = pd.DataFrame({"sira": [1], "pazar": ["AVR"], "sembol": ["Q"], "tarih": [pd.Timestamp("2026-10-22")], "hat": [100.0], "kapanis": [104.0]})
La = CT.ct_aday_alanlari(La)
kontrol("stop0 = hat x 0,98; uzaklık; hedefler kapanışa göre", abs(La.stop0[0] - 98.0) < 1e-12 and abs(La.stop_uzak[0] - (98 / 104 - 1)) < 1e-12
        and abs(La.hedef5[0] - 109.2) < 1e-9 and abs(La.hedef10[0] - 114.4) < 1e-9 and La.para[0] == "EUR")
kontrol("ölçüm tarihi = sinyal + 15 iş günü", La.olcum_tarihi[0] == pd.Timestamp("2026-11-12"))
Mm = {"n": 1, "pozitif": 0.4, "esik7_sha": "x", "sklearn": "1", "egitim_sinir": "2026-08-31", "giris_max": "2026-08-01", "n_iter": 1, "zaman_utc": "z"}
J = CT.ct_json("2026-10-22", La, La.assign(puan7=0.5, kademe="S1_S7", F15=0.1, F17=-0.3, F18=0.04, S9=False), pd.DataFrame(),
               {"kademe": "S1_S7", "sayi": {}}, {}, {}, [], None, Mm, {"esik_sha": "e", "kontrol": True})
kontrol("json: dürüstlük, adaylar, ileri test alanları", J["durustluk"].startswith("DÜRÜSTLÜK") and "ÖNERİ DEĞİLDİR" in J["durustluk"]
        and J["ileri_test"]["olcum_tarihi"]["AVR:Q"] == "2026-11-12" and J["ileri_test"]["komut"].endswith("--tarih 2026-10-22")
        and J["adaylar"][0]["stop0"] == 98.0 and abs(J["havuz_tumu"][0]["stop0"] - 98.0) < 1e-12)
js = json.dumps(CT._ct_temiz(J), ensure_ascii=False, default=CT._ct_json)
kontrol("json yazılabilir (NaN -> null)", "NaN" not in js)

# ---------------------------------------------------------------- 7) puan7 matrisi
print("7) puan7 matrisi")
rng = np.random.default_rng(5)
D = pd.DataFrame(rng.normal(size=(40, len(YH.YH_ESIK7["ozellik"]))), columns=YH.YH_ESIK7["ozellik"])
for c in YH.YH_ESIK7["nan_bayrak"]:
    D.loc[rng.choice(40, 6, replace=False), c] = np.nan
Xa, Xb, _ = YH._yh_matris7(D.iloc[:30], D.iloc[30:])
med = D.iloc[:30][YH.YH_ESIK7["ozellik"]].median().fillna(0.0)
kontrol("_ct_matris = YH._yh_matris7 (eğitim ve sınama)", np.allclose(CT._ct_matris(D.iloc[:30], med), Xa) and np.allclose(CT._ct_matris(D.iloc[30:], med), Xb))

# ---------------------------------------------------------------- 8) olc = YAPI_HEDEF cetveli
print("8) olc hesabı")
tmp = tempfile.mkdtemp(prefix="ct_test_")
try:
    V = {f"H{i:02d}": rastgele_hisse(400, 100 + i, bas="2025-06-02") for i in range(120)}
    pd.to_pickle(V, os.path.join(tmp, "V_ABD.pkl"))
    t = V["H00"].index[300]
    Ad = pd.DataFrame({"pazar": ["ABD", "ABD"], "sembol": ["H00", "H01"], "tarih": [t, t],
                       "hat": [float(V["H00"].Low.iloc[290:300].min()), float(V["H01"].Low.iloc[290:300].min())], "kapsam": ["liste", "havuz"], "sira": [1, np.nan]})
    Z = CT.ct_olc_olaylar(Ad, veri=tmp)
    r = Z[Z.sembol == "H00"].iloc[0]; d = V["H00"]
    E0 = float(d.Open.iloc[301]); st0 = Ad.hat[0] * 0.98
    S_ = YH.yh_sim(d.Close.to_numpy(float)[301:331, None], d.High.to_numpy(float)[301:331, None], d.Low.to_numpy(float)[301:331, None],
                   np.array([E0]), np.array([st0]), 1)
    kontrol("giriş = t+1 açılışı", abs(r.E0 - E0) < 1e-12 and pd.Timestamp(r.giris) == d.index[301])
    kontrol("h5 / h10 / st5 / k5 / kst = elle yh_sim", r.olc and r.h5 == S_["h5"][0] and r.h10 == S_["h10"][0] and r.st5 == S_["st5"][0]
            and int(r.k5) == int(S_["k5"][0]) and int(r.kst) == int(S_["kst"][0]), f"h5 {r.h5} st5 {r.st5}")
    kontrol("eş ölçüldü (aynı gün aynı kova, en az 3)", np.isfinite(r.es_h5) and r.n_es >= 3, f"n_es {r.n_es}")
    cik = os.path.join(tmp, "canli"); os.makedirs(cik)
    Jt = {"durustluk": CT.CT_DURUSTLUK, "havuz": {"kademe": "S1_S7"}, "adaylar": [Ad.iloc[0][["pazar", "sembol", "hat", "sira"]].to_dict() | {"tarih": str(t.date())}],
          "havuz_tumu": [Ad.iloc[1][["pazar", "sembol", "hat"]].to_dict() | {"tarih": str(t.date())}],
          "ileri_test": {"cetvel": "test", "olcum_tarihi_en_gec": str((t + pd.offsets.BDay(15)).date())}}
    with open(os.path.join(cik, "CANLI_TARAMA_2026-01-01.json"), "w", encoding="utf-8") as f:
        json.dump(Jt, f)
    son = os.path.join(cik, "CANLI_SONUC.md")
    O1 = CT.ct_olc("2026-01-01", tmp, cik, son)
    m1 = open(son, encoding="utf-8").read()
    kontrol("CANLI_SONUC.md yazıldı: dürüstlük + tablo + OLCULDU", m1.count("ÖNERİ DEĞİLDİR") == 1 and "<!-- OLCULDU 2026-01-01 -->" in m1
            and "| liste | 1 | ABD | H00 |" in m1 and O1["tamam"])
    CT.ct_olc("2026-01-01", tmp, cik, son)
    m2 = open(son, encoding="utf-8").read()
    kontrol("ikinci ölçüm eklenir, ilk satırlar silinmez", m2.startswith(m1.rstrip("\n")) and m2.count("## Ölçüm: liste 2026-01-01") == 2)
    kontrol("vadesi: OLCULDU işaretli liste yeniden ölçülmez", CT.ct_olc_vadesi(tmp, cik, son) == [])

    # ------------------------------------------------------------ 9) geleceğe bakma
    print("9) geleceğe bakma (özellik prefix)")
    with CT.ct_kriz_ac():
        bul = None
        for s in sorted(V):
            X1, _ = YH.yh_s6_hisse(V[s])
            X1 = X1[X1.tarih <= V[s].index[-20]]
            if len(X1):
                bul = (s, pd.Timestamp(X1.tarih.iloc[-1])); break
        if bul is None:
            kontrol("sentetik veride S6 AL günü bulundu", False)
        else:
            s, t = bul
            Fa = CT.ct_ozellik_hisse(V[s], [t])
            dk = V[s][V[s].index <= t]
            Fb = CT.ct_ozellik_hisse(dk, [t])
            dz = V[s].copy(); dz.loc[dz.index > t, ["Open", "High", "Low", "Close"]] *= 1.5
            Fc = CT.ct_ozellik_hisse(dz, [t])
            kol = YH.YH_ESIK7["ozellik"] + ["F65", "F66", "F67", "F68", "S10", "hat", "kural12"]
            a_, b_, c_ = (x[kol].to_numpy(float)[0] for x in (Fa, Fb, Fc))
            kontrol("F1-F29 / Ş10 / hat / 12 kural: kesik veri = tam veri", np.allclose(a_, b_, equal_nan=True))
            kontrol("t sonrası fiyat değişince aynı", np.allclose(a_, c_, equal_nan=True) and Fa.mahkeme[0] == Fc.mahkeme[0])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------- 10) kriz / sızıntı / çakışma / kapı
print("10) kriz bağlamı, sızıntı, çakışma kapısı, ön kayıt kapısı")
k0 = (SY.SY_ESIK["kriz"], OC.OC_ESIK["kriz"], YH.YH_ESIK["kriz"])
try:
    with CT.ct_kriz_ac():
        ic = (SY.SY_ESIK["kriz"], OC.OC_ESIK["kriz"])
        raise ValueError("deneme")
except ValueError:
    pass
kontrol("kriz kesiği bağlam içinde açık, çıkışta (hata olsa da) geri", ic == ("2100-01-01", "2100-01-01")
        and (SY.SY_ESIK["kriz"], OC.OC_ESIK["kriz"], YH.YH_ESIK["kriz"]) == k0 == ("2026-08-31",) * 3)
tmp2 = tempfile.mkdtemp(prefix="ct_test2_")
try:
    yakalandi = False
    try:
        CT._ct_yaz(os.path.join(tmp2, "x.md"), "iletişim: ornek" + "@" + "ornek.com", "deneme")
    except CT.CTHata:
        yakalandi = True
    kontrol("e-posta içeren metin yazılmaz", yakalandi and not os.path.exists(os.path.join(tmp2, "x.md")))
    ok_ = os.path.join(tmp2, "ok.md")
    open(ok_, "w", encoding="utf-8").write(CT.ct_onkayit_metni())
    kontrol("ön kayıt kapısı geçer (sha + 14 madde)", CT.ct_kapi(ok_)["kontrol"])
    open(ok_, "w", encoding="utf-8").write(CT.ct_onkayit_metni().replace(CT.ct_esik_sha(), "0" * 64))
    try:
        CT.ct_kapi(ok_); dur = False
    except CT.CTHata:
        dur = True
    kontrol("CT_ESIK sha tutmazsa DURUR", dur)
finally:
    shutil.rmtree(tmp2, ignore_errors=True)
kontrol("depodaki ön kayıt kapıdan geçer", CT.ct_kapi()["kontrol"])
ns = {"__name__": "ct_cakisma", "__file__": os.path.join(KOK, "CANLI_TARAMA.py"), "ct_tara": "baska", "_CK_KAYIT": {"ct_tara": "BASKA.py"}}
try:
    exec(compile(open(os.path.join(KOK, "CANLI_TARAMA.py"), encoding="utf-8").read(), "CANLI_TARAMA.py", "exec"), ns)
    ezdi = False
except RuntimeError as ex:
    ezdi = "EZDİ" in str(ex)
kontrol("çakışma kapısı: başka dosyanın adını ezince durur", ezdi)

print(f"\nSONUÇ: {len(GECTI)} geçti, {len(KALDI)} kaldı")
if KALDI:
    print("KALAN:", KALDI)
    sys.exit(1)
