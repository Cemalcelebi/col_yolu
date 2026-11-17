"""test_goz_etiket — GOZ_ETIKET.py testleri (sentetik veri; gerçek veri varsa ek denetim).

1) örneklem SONUÇ SÜTUNLARINA BAKMAZ: yasak sütun istenirse durur; olay dosyasının sonuç sütunları silinince / karıştırılınca örneklem aynı;
   aynı tohum aynı örneklem; katman kotaları, sembol başına en çok 2, uygunluk (dönem, giriş <= kriz - 30 gün), numara karıştırılmış
2) görselde t sonrası bar YOK: son bar = t, t sonrası barlar bozulunca görsel verisi ve PNG baytları aynı; PNG 1200x800, metin parçası yok
3) özelliklerin prefix değişmezliği: veri t'de kesilince F1-F18 tam seriyle aynı (bütün al günleri); t sonrası bozulunca aynı
4) özellikler elle: F1, F2, F4-F13, F15, F18 elle hesapla eşit; bölge / hat YAPI_HEDEF yh_y6_bayrak ile aynı (dokunuş = F1)
5) anahtar gizliliği: PNG'de sembol / tarih / pazar yok (metin parçası yok; başlık 'No k'), anahtar yalnız no -> kimlik; e-posta / anahtar taraması
6) çakışma kapısı (bellekteki adı ezince durur); kontrol tablosu 14 satır kapıdan geçer
7) (gerçek dosyalar varsa) anahtar.json 300 olay, kotalar; ozellik_Y1.csv.gz 26.663 satır, olay dosyasıyla aynı sıra; PNG klasörü 300 dosya
8) AŞAMA C: birleştirme bire bir (eksik / fazla DURUR), KAT5 = Σ h5 / Σ es_h5 = oc_kat, CV sızıntısı yok (katta doldurma / ölçek yalnız eğitim katından),
   hakem seçimi (40 sayfa, 3/7/10, tohum 13), kappa, cevap değerlendirme; gerçek dosyalarda yeniden üretim
Çalıştır: python test_goz_etiket.py
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

import GOZ_ETIKET as GE  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

GECTI, KALDI = [], []


def kontrol(ad, kosul, ek=""):
    (GECTI if kosul else KALDI).append(ad)
    print(("  OK   " if kosul else "  HATA ") + ad + (f"  ({ek})" if ek else ""))


def rastgele_hisse(n, tohum, bas="2016-01-01", oyn=0.02):
    """Sıkışma dönemleri olan sentetik hisse (S6 al günleri üretsin)."""
    rng = np.random.default_rng(tohum)
    r = rng.normal(0.0, oyn, n)
    for k in range(300, n - 80, 160):          # dönem dönem sakin pencereler
        r[k:k + 50] = rng.normal(0.0, oyn * 0.25, 50)
        r[k + 50] = 0.06
    C = 50 * np.exp(np.cumsum(r))
    O = C * (1 + rng.normal(0, 0.004, n))
    a = rng.uniform(0, 0.012, n); b = rng.uniform(0, 0.012, n)
    H = np.maximum(O, C) * (1 + b); L = np.minimum(O, C) * (1 - a)
    V = rng.integers(5000, 80000, n).astype(float)
    ix = pd.bdate_range(bas, periods=n)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=ix)


def al_gunleri(d):
    T = GE.ge_s6(d)
    return [int(i) for i in np.flatnonzero(T["al"]) if i >= 1], T


def sahte_olay(n_sembol=40, tohum=3):
    """olay_Y1 biçiminde sahte dosya: kimlik + sinyal + sonuç sütunları."""
    rng = np.random.default_rng(tohum); sat = []
    for pz in ("ABD", "AVR", "BIST"):
        for s in range(n_sembol):
            for k in range(rng.integers(2, 6)):
                gun = pd.Timestamp("2022-12-01") + pd.Timedelta(days=int(rng.integers(0, 1350)))
                sat.append({"deneme": "Y1", "pazar": pz, "sembol": f"S{s:03d}", "tarih": gun, "giris": gun + pd.Timedelta(days=1),
                            "hat": 10.0, "tavan": 11.0, "n": 20, "ek": "AL;haf=0"})
    X = pd.DataFrame(sat).drop_duplicates(["pazar", "sembol", "tarih"]).reset_index(drop=True)
    X["donem"] = np.where(X.giris < "2023-01-01", "2016-22", np.where(X.giris <= "2023-12-31", "2023", "2024-26"))
    for c in ["h5", "h10", "st5", "es_h5", "es_st5", "getiri", "olc"]:
        X[c] = rng.random(len(X))
    return X


def main():
    tmp = tempfile.mkdtemp(prefix="test_ge_")
    try:
        print("1) örneklem sonuç sütunlarına bakmaz")
        X = sahte_olay()
        y1 = os.path.join(tmp, "olay1.csv.gz"); X.to_csv(y1, index=False)
        E = json.loads(json.dumps(GE.GE_ESIK))
        E["orneklem"]["katman"] = [["ABD", "2023", 12], ["ABD", "2024-26", 16], ["AVR", "2023", 8], ["AVR", "2024-26", 12],
                                   ["BIST", "2023", 4], ["BIST", "2024-26", 8]]
        S1 = GE.ge_orneklem(y1, E)
        try:
            GE.ge_olay_oku(["sembol", "h5"], y1); kontrol("yasak sütun (h5) istenince durur", False)
        except GE.GEHata:
            kontrol("yasak sütun (h5) istenince durur", True)
        X2 = X.copy(); rng = np.random.default_rng(9)
        for c in ["h5", "h10", "st5", "es_h5", "es_st5", "getiri", "olc"]:
            X2[c] = rng.permutation(X2[c].to_numpy())
        y2 = os.path.join(tmp, "olay2.csv.gz"); X2.to_csv(y2, index=False)
        y3 = os.path.join(tmp, "olay3.csv.gz"); X.drop(columns=["h5", "h10", "st5", "es_h5", "es_st5", "getiri", "olc", "hat", "tavan", "n", "ek"]).to_csv(y3, index=False)
        S2 = GE.ge_orneklem(y2, E); S3 = GE.ge_orneklem(y3, E)
        kontrol("sonuç sütunları karıştırılınca örneklem aynı", S1.equals(S2))
        kontrol("sonuç (ve sinyal) sütunları silinince örneklem aynı", S1.equals(S3))
        kontrol("aynı tohum aynı örneklem", S1.equals(GE.ge_orneklem(y1, E)))
        E2 = json.loads(json.dumps(E)); E2["orneklem"]["tohum"] = 12
        kontrol("farklı tohum farklı örneklem", not S1.equals(GE.ge_orneklem(y1, E2)))
        dag = S1.groupby(["pazar", "donem"]).size()
        kontrol("katman kotaları", all(int(dag.get((p, d), 0)) == k for p, d, k in E["orneklem"]["katman"]))
        kontrol("sembol başına en çok 2", int(S1.groupby(["pazar", "sembol"]).size().max()) <= 2)
        sinir = pd.Timestamp(E["kriz"]) - pd.Timedelta(days=30)
        kontrol("uygunluk: dönem 2023 / 2024-26 ve giriş <= kriz - 30 gün", bool(S1.donem.isin(["2023", "2024-26"]).all() and (S1.giris <= sinir).all()))
        kontrol("numara 1..N ve pazar sırası taşımıyor", list(S1.no) == list(range(1, len(S1) + 1)) and not S1.pazar.is_monotonic_increasing)
        E3 = json.loads(json.dumps(E)); E3["orneklem"]["katman"] = [["BIST", "2023", 10 ** 6]]
        try:
            GE.ge_orneklem(y1, E3); kontrol("kota dolmazsa durur", False)
        except GE.GEHata:
            kontrol("kota dolmazsa durur", True)
        GE.ge_anahtar_yaz(S1, tmp, E)
        J = json.load(open(os.path.join(tmp, "anahtar.json"), encoding="utf-8"))
        kontrol("anahtar: yalnız no -> kimlik (sonuç alanı yok)",
                all(set(v) == {"sembol", "pazar", "tarih", "giris", "donem"} for v in J["olay"].values()) and len(J["olay"]) == len(S1))
        kontrol("anahtar geri okunur", GE.ge_anahtar_oku(tmp)[["no", "sembol"]].equals(S1[["no", "sembol"]]))

        print("2) görselde t sonrası bar yok")
        d = YH._yh_hazir(rastgele_hisse(1500, 1))
        al, T = al_gunleri(d)
        kontrol("sentetik veride al günü var", len(al) >= 5, f"{len(al)}")
        i = al[len(al) // 2]; t = d.index[i]
        G1 = GE.ge_gorsel_veri(d, t, hazir=True)
        kontrol("görselin son barı = t", G1["W"].index[-1] == t and len(G1["W"]) == GE.GE_ESIK["gorsel"]["bar"])
        db = d.copy(); db.iloc[i + 1:, :4] = db.iloc[i + 1:, :4].to_numpy() * 3.0   # t sonrası bozulur
        G2 = GE.ge_gorsel_veri(db, t, hazir=True)
        kontrol("t sonrası bozulunca görsel verisi aynı", G1["W"].equals(G2["W"]) and G1["hat"] == G2["hat"] and G1["sol"] == G2["sol"])
        p1 = GE.ge_ciz(G1, 7, os.path.join(tmp, "a", "No_7.png")); p2 = GE.ge_ciz(G2, 7, os.path.join(tmp, "b", "No_7.png"))
        kontrol("t sonrası bozulunca PNG baytları aynı", open(p1, "rb").read() == open(p2, "rb").read())
        B = GE.ge_bolge(T, i)
        kontrol("görsel hat / tavan = tam seri hat / tavan", abs(G1["hat"] - B["hat"]) < 1e-12 and abs(G1["tavan"] - B["tavan"]) < 1e-12)
        ham = open(p1, "rb").read()
        from PIL import Image
        im = Image.open(p1)
        kontrol("PNG 1200x800", im.size == (1200, 800), f"{im.size}")
        parca, k = [], 8
        while k < len(ham):
            ln = int.from_bytes(ham[k:k + 4], "big"); parca.append(ham[k + 4:k + 8].decode("latin1")); k += 12 + ln
        kontrol("PNG metin parçası yok (tEXt / iTXt / zTXt)", not any(c in parca for c in ("tEXt", "iTXt", "zTXt")), ",".join(parca[:6]))
        try:
            GE.ge_gorsel_veri(d, d.index[al[0] + 1] if al[0] + 1 not in al else d.index[0], hazir=True)
            kontrol("al günü olmayan günde durur", False)
        except GE.GEHata:
            kontrol("al günü olmayan günde durur", True)

        print("3) özelliklerin prefix değişmezliği")
        O, H, L, C, V = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
        Fk = [f"F{k}" for k in range(1, 19)]
        Fs, _ = GE.ge_ozellik_hisse(d, [d.index[j] for j in al], hazir=True)
        es = True; es_boz = True
        for j, f in zip(al, Fs):
            dk = d.iloc[:j + 1]
            fk, _ = GE.ge_ozellik_hisse(dk, [d.index[j]], hazir=True)
            a = np.array([f[k] for k in Fk]); b = np.array([fk[0][k] for k in Fk])
            es &= bool(np.allclose(a, b, rtol=1e-12, equal_nan=True))
        db2 = d.copy(); jj = al[len(al) // 2]
        db2.iloc[jj + 1:, :4] = db2.iloc[jj + 1:, :4].to_numpy() * 0.5
        fb, _ = GE.ge_ozellik_hisse(db2, [d.index[jj]], hazir=True)
        es_boz = bool(np.allclose([Fs[al.index(jj)][k] for k in Fk], [fb[0][k] for k in Fk], rtol=1e-12, equal_nan=True))
        kontrol("bütün al günlerinde kesik seri = tam seri (F1-F18)", es, f"{len(al)} gün")
        kontrol("t sonrası bozulunca F1-F18 aynı", es_boz)
        # ikinci sentetik hisse (farklı tohum) aynı denetim
        d2 = YH._yh_hazir(rastgele_hisse(1300, 5)); al2, _ = al_gunleri(d2)
        F2s, _ = GE.ge_ozellik_hisse(d2, [d2.index[j] for j in al2], hazir=True)
        es2 = all(np.allclose([f[k] for k in Fk], [GE.ge_ozellik_hisse(d2.iloc[:j + 1], [d2.index[j]], hazir=True)[0][0][k] for k in Fk],
                              rtol=1e-12, equal_nan=True) for j, f in zip(al2, F2s))
        kontrol("ikinci hisse: kesik seri = tam seri", es2, f"{len(al2)} gün")

        print("4) özellikler elle")
        f = Fs[al.index(i)]; s = B["sol"]; z = slice(s, i); hat = B["hat"]; tav = B["tavan"]
        dok = np.flatnonzero(L[z] <= hat * 1.015)
        kontrol("F1 dokunuş", f["F1"] == len(dok))
        kontrol("F2 eğim", (len(dok) == 0 and np.isnan(f["F2"])) or abs(f["F2"] - (L[z][dok[-1]] / L[z][dok[0]] - 1)) < 1e-12)
        rz = H[z] - L[z]
        kontrol("F4 alt fitil", abs(f["F4"] - np.median((np.minimum(O[z], C[z]) - L[z]) / rz)) < 1e-12)
        kontrol("F5 açılış-dip", abs(f["F5"] - np.median((O[z] - L[z]) / rz)) < 1e-12)
        kontrol("F6 üst fitil", abs(f["F6"] - np.median((H[z] - np.maximum(O[z], C[z])) / rz)) < 1e-12)
        kontrol("F7 yeşil pay", abs(f["F7"] - np.mean(C[z] > O[z])) < 1e-12)
        kontrol("F8 boy", f["F8"] == i - s)
        kontrol("F9 bant", abs(f["F9"] - (tav / hat - 1)) < 1e-12)
        kontrol("F10 net", abs(f["F10"] - (C[i - 1] / C[s] - 1)) < 1e-12)
        kontrol("F11 kırılım payı > 0 (C_t > tavan)", abs(f["F11"] - (C[i] / tav - 1)) < 1e-12 and f["F11"] > 0)
        kontrol("F12 gövde / medyan mum", abs(f["F12"] - abs(C[i] - O[i]) / np.median(rz)) < 1e-12)
        kontrol("F13 hacim", abs(f["F13"] - V[i] / np.median(V[z])) < 1e-12)
        c120 = C[i - 119:i + 1]
        kontrol("F15 konum", abs(f["F15"] - (C[i] - c120.min()) / (c120.max() - c120.min())) < 1e-12)
        kontrol("F18 stop uzaklığı", abs(f["F18"] - (C[i] / hat - 1)) < 1e-12)
        Z6 = YH.yh_y6_bayrak(d)
        z6 = Z6.set_index(pd.to_datetime(Z6.tarih))
        uy = all(int(z6.loc[d.index[j], "dokunus"]) == int(ff["F1"]) and abs(float(z6.loc[d.index[j], "hat"]) - GE.ge_bolge(T, j)["hat"]) < 1e-9
                 for j, ff in zip(al, Fs))
        kontrol("bölge / hat / dokunuş = YAPI_HEDEF yh_y6_bayrak (F1 = dokunus)", uy)
        uy16 = all(int(z6.loc[d.index[j], "kir250"]) == int(ff["F16"]) for j, ff in zip(al, Fs))
        kontrol("F16 = YAPI_HEDEF kir250", uy16)

        print("5) anahtar gizliliği ve sızıntı")
        kontrol("PNG baytlarında sembol / tarih metni yok", b"2016-" not in ham and b"2017-" not in ham and b"S00" not in ham)
        try:
            GE._ge_sizinti("iletisim: ornek@ornek.com", "t"); kontrol("e-posta taraması durdurur", False)
        except GE.GEHata:
            kontrol("e-posta taraması durdurur", True)
        try:
            GE._ge_sizinti("api_key = ABCDEFGHIJKLMNOP1234", "t"); kontrol("anahtar taraması durdurur", False)
        except GE.GEHata:
            kontrol("anahtar taraması durdurur", True)
        try:
            GE.ge_gorsel(cikti=tmp, png=os.path.join(KOK, "png_test_yasak")); kontrol("PNG klasörü repo içinde olamaz", False)
        except GE.GEHata:
            kontrol("PNG klasörü repo içinde olamaz", True)
        kod = open(os.path.join(KOK, "GOZ_ETIKET.py"), encoding="utf-8").read()
        kontrol("kodda e-posta / anahtar yok", not GE._GE_EPOSTA.search(kod) and not GE._GE_ANAHTAR.search(kod))

        print("6) çakışma kapısı ve kontrol tablosu")
        g = {}
        exec("def ge_orneklem():\n    return 1\n", g)
        g["_CK_KAYIT"] = {"ge_orneklem": "BASKA.py"}
        try:
            exec(compile(open(os.path.join(KOK, "GOZ_ETIKET.py"), encoding="utf-8").read(), "GOZ_ETIKET.py", "exec"), g)
            kontrol("çakışma kapısı: bellekteki adı ezince durur", False)
        except RuntimeError as ex:
            kontrol("çakışma kapısı: bellekteki adı ezince durur", "EZDİ" in str(ex))
        yk = os.path.join(tmp, "ON_KAYIT_test.md")
        open(yk, "w", encoding="utf-8").write(GE.ge_kontrol_tablosu() + "\n")
        import IZ_KARNE as IK
        r = IK.ik_kontrol_kapisi(yk, dur=False)
        kontrol("kontrol tablosu 14 satır kapıdan geçer", r["gecti"] and r["n"] == 14, str(r.get("eksik")))
        kontrol("§5 iş tanımından aynen alınır", GE.ge_is_tanimi_bolum("5") in open(GE.GE_YOL["is_tanimi"], encoding="utf-8").read()
                and "ÖLÇÜ 1" in GE.ge_is_tanimi_bolum("5"))

        print("7) gerçek çıktılar (varsa)")
        ya = os.path.join(GE.GE_YOL["cikti"], "anahtar.json")
        if os.path.exists(ya):
            S = GE.ge_anahtar_oku()
            dg = S.groupby(["pazar", "donem"]).size()
            kontrol("anahtar.json 300 olay, kotalar", len(S) == 300 and all(int(dg.get((p, dd), 0)) == k for p, dd, k in GE.GE_ESIK["orneklem"]["katman"]))
            kontrol("anahtar.json = ge_orneklem() yeniden üretim", S[["no", "pazar", "sembol", "tarih"]].reset_index(drop=True).equals(
                GE.ge_orneklem()[["no", "pazar", "sembol", "tarih"]].reset_index(drop=True)))
            kontrol("gerçek örneklem: sembol başına en çok 2", int(S.groupby(["pazar", "sembol"]).size().max()) <= 2)
        yo = os.path.join(GE.GE_YOL["cikti"], "ozellik_Y1.csv.gz")
        if os.path.exists(yo):
            Ft = pd.read_csv(yo); Xo = GE.ge_olay_oku(["pazar", "sembol", "tarih"])
            kontrol("ozellik_Y1: 26.663 satır, olay dosyasıyla aynı sıra", len(Ft) == len(Xo) == 26663 and
                    (Ft.sembol.astype(str).to_numpy() == Xo.sembol.astype(str).to_numpy()).all() and
                    (pd.to_datetime(Ft.tarih).to_numpy() == Xo.tarih.to_numpy()).all())
            kontrol("ozellik_Y1: F1-F18 sütunları", all(f"F{k}" in Ft for k in range(1, 19)))
            kontrol("ozellik_Y1: sonuç sütunu yok", not any(c in Ft for c in GE.GE_SONUC_KOL_ORNEK))
        if os.path.isdir(GE.GE_YOL["png"]):
            pl = [x for x in os.listdir(GE.GE_YOL["png"]) if x.endswith(".png")]
            kontrol("PNG klasörü 300 dosya (No_k.png)", len(pl) == 300 and all(x.startswith("No_") for x in pl), f"{len(pl)}")
            metin_yok = True
            for x in pl:
                hb = open(os.path.join(GE.GE_YOL["png"], x), "rb").read(); k = 8
                while k < len(hb):
                    ln = int.from_bytes(hb[k:k + 4], "big")
                    if hb[k + 4:k + 8] in (b"tEXt", b"iTXt", b"zTXt"):
                        metin_yok = False
                    k += 12 + ln
            kontrol("gerçek PNG'lerin hiçbirinde metin parçası yok (sembol / tarih / pazar gömülemez)", metin_yok)
        print("8) AŞAMA C: birleştirme, KAT, CV sızıntısı, hakem seçimi, kappa, hakem değerlendirme")
        rng = np.random.default_rng(5)
        Xs = sahte_olay(n_sembol=30, tohum=8)
        Xs["giris"] = pd.to_datetime(Xs["giris"]); Xs["tarih"] = pd.to_datetime(Xs["tarih"])
        for c in ("h5", "h10", "st5"):
            Xs[c] = (rng.random(len(Xs)) < 0.3).astype(float)
        Xs["es_h10"] = rng.random(len(Xs)) * 0.2
        Ss = Xs.sample(60, random_state=1)[["pazar", "sembol", "tarih", "giris", "donem"]].reset_index(drop=True)
        Ss.insert(0, "no", np.arange(1, 61))
        kar = np.array(["OLUR"] * 6 + ["BELİRSİZ"] * 14 + ["OLMAZ"] * 40)
        Ts = pd.DataFrame({"no": np.arange(1, 61), "karar": kar, "nedenler": [["C5+", "C3-"] if i % 2 else ["C11-"] for i in range(60)],
                           "guven": 3, "not": "x"})
        Ms = GE.ge_birlestir(Ss, Ts, Xs)
        kontrol("C birleştirme: 60 satır, bire bir, sonuç sütunu doğru eşleşti",
                len(Ms) == 60 and all(float(Xs[(Xs.pazar == r.pazar) & (Xs.sembol == r.sembol) & (Xs.tarih == r.tarih)].h5.iloc[0]) == r.h5
                                      for r in Ms.itertuples()))
        S_bad = Ss.copy(); S_bad.loc[0, "sembol"] = "YOK999"
        try:
            GE.ge_birlestir(S_bad, Ts, Xs); ok = False
        except GE.GEHata:
            ok = True
        kontrol("C birleştirme: olay dosyasında olmayan etiketli olay DURUR", ok)
        try:
            GE.ge_birlestir(Ss, Ts[Ts.no != 5], Xs); ok = False
        except GE.GEHata:
            ok = True
        kontrol("C birleştirme: anahtar / etiket numara farkı DURUR", ok)
        g = GE.ge_grup(Ms[Ms.karar == "OLMAZ"])
        gg = Ms[Ms.karar == "OLMAZ"]
        kontrol("C KAT5 = Σ h5 / Σ es_h5 (elle)", abs(g["h5_kat"] - gg.h5.sum() / gg.es_h5.sum()) < 1e-12 and g["h5_alt"] <= g["h5_kat"] <= g["h5_ust"])
        import ORTAK_CETVEL as OC_
        ay = pd.to_datetime(gg.sort_values("giris").giris).dt.to_period("M").astype(str).to_numpy()
        r_oc = OC_.oc_kat(gg.sort_values("giris").h5.to_numpy(float), gg.sort_values("giris").es_h5.to_numpy(float), ay)
        kontrol("C KAT5 bootstrap = ORTAK_CETVEL.oc_kat (alt / üst)", abs(r_oc["alt"] - g["h5_alt"]) < 1e-12 and abs(r_oc["ust"] - g["h5_ust"]) < 1e-12)
        R1 = GE.ge_iki_grup(Ms[Ms.karar == "OLUR"], Ms[Ms.karar == "OLMAZ"], "OLUR", "OLMAZ", GE.GE_C_ESIK["olcu1"])
        kontrol("C ölçü 1: OLUR n < 30 -> ÖLÇÜLEMEDİ", R1["durum"] == "ÖLÇÜLEMEDİ")
        # CV sızıntısı: her katın doldurma medyanı / ölçek ortalaması yalnız eğitim katından
        A = rng.normal(size=(120, 18)); A[rng.random(A.shape) < 0.1] = np.nan; A[:, 0] += np.arange(120) / 10
        y = (rng.random(120) < 0.3).astype(int)
        cv = GE.ge_cv(A, y, perm=False)
        sz = True
        for k in cv["katlar"]:
            med_tr = np.nanmedian(A[k["tr"]], axis=0); med_tum = np.nanmedian(A, axis=0)
            sz &= bool(np.allclose(k["doldur"], med_tr)) and not np.allclose(k["doldur"], med_tum) and len(set(k["tr"]) & set(k["te"])) == 0
        kontrol("C CV sızıntısı yok: doldurma / ölçek her katta yalnız eğitim katından; katlar ayrık", sz and len(cv["katlar"]) == 5)
        kontrol("C CV: OOF olasılık her satırda tek kez (NaN yok)", np.isfinite(cv["oof"]).all())
        # hakem seçimi
        Th = pd.DataFrame({"no": np.arange(1, 301), "karar": ["OLUR"] * 6 + ["BELİRSİZ"] * 51 + ["OLMAZ"] * 243})
        D1 = GE.ge_hakem_sec(Th); D2 = GE.ge_hakem_sec(Th)
        kk = D1[D1.yari == "KÖR"].karar.value_counts().to_dict(); ka = D1[D1.yari == "AÇIK"].karar.value_counts().to_dict()
        kontrol("C hakem: 40 sayfa, her yarı OLUR 3 / BELİRSİZ 7 / OLMAZ 10; 6 OLUR'un hepsi; no tekil; tohum 13 deterministik",
                len(D1) == 40 and kk == {"OLMAZ": 10, "BELİRSİZ": 7, "OLUR": 3} and ka == kk and set(D1[D1.karar == "OLUR"].no) == set(range(1, 7))
                and not D1.no.duplicated().any() and D1.equals(D2) and list(D1.sayfa) == list(range(1, 41))
                and (D1.yari.iloc[:20] == "KÖR").all() and (D1.yari.iloc[20:] == "AÇIK").all())
        kontrol("C kappa: tam uyum 1, bilinen örnek", abs(GE.ge_kappa(list("aabb"), list("aabb")) - 1) < 1e-12 and
                abs(GE.ge_kappa(list("aabbab"), list("ababab")) - (4 / 6 - 0.5) / 0.5) < 1e-12)
        kontrol("C cevap normalleştirme (Türkçe / ASCII)", GE.ge_cevap_norm("doğru") == "DOĞRU" and GE.ge_cevap_norm("Belirsiz") == "BELİRSİZ"
                and GE.ge_cevap_norm("YANLIS") == "YANLIŞ" and GE.ge_cevap_norm("") is None)
        # hakem değerlendirme (sahte anahtar + cevap)
        hk = os.path.join(tmp, "hk"); os.makedirs(hk)
        Ah = {"sayfa": {str(r.sayfa): {"yari": r.yari, "no": int(r.no), "karar": r.karar, "nedenler": ["C5+", "C11-"]} for r in D1.itertuples()}}
        json.dump(Ah, open(os.path.join(hk, "hakem_anahtar.json"), "w"))
        cv_yol = os.path.join(hk, "cevap.csv")
        sat = ["sayfa,cevap,neden"] + [f"{r.sayfa},{r.karar if r.yari == 'KÖR' else ('YANLIŞ' if r.sayfa % 2 else 'DOĞRU')},C5 yanlış" for r in D1.itertuples()]
        open(cv_yol, "w").write("\n".join(sat))
        Hs = GE.ge_hakem_degerlendir(cv_yol, hk)
        kontrol("C hakem değerlendirme: kör kappa 1 (aynı cevap), açık 10 yanlış, C5 sayımı 10",
                abs(Hs["kappa"] - 1) < 1e-12 and Hs["yanlis"] == 10 and Hs["dogru"] == 10 and Hs["kural_andigi"].get("C5") == 10
                and os.path.exists(os.path.join(hk, "HAKEM_SONUC.md")))
        kontrol("C neden açılımı", GE.ge_neden_acilim("C5-").startswith("C5- kırılım") and "UYMUYOR" in GE.ge_neden_acilim("C5-"))
        ye = os.path.join(GE.GE_YOL["cikti"], "etiket.json")
        if os.path.exists(ye):
            Tg = GE.ge_etiket_oku()
            kontrol("gerçek etiket.json: 300 etiket, anahtarla aynı numaralar", len(Tg) == 300 and set(Tg.no) == set(range(1, 301)))
            Dg = GE.ge_hakem_sec(Tg)
            kontrol("gerçek hakem seçimi: 6 OLUR'un hepsi, yarılar 3/7/10", set(Dg[Dg.karar == "OLUR"].no) == set(Tg[Tg.karar == "OLUR"].no)
                    and Dg[Dg.yari == "KÖR"].karar.value_counts().to_dict() == {"OLMAZ": 10, "BELİRSİZ": 7, "OLUR": 3})
            yh = os.path.join(GE.GE_YOL["cikti"], "hakem_anahtar.json")
            if os.path.exists(yh):
                Jh = json.load(open(yh, encoding="utf-8"))["sayfa"]
                kontrol("hakem_anahtar.json = ge_hakem_sec yeniden üretim", all(Jh[str(r.sayfa)]["no"] == r.no and Jh[str(r.sayfa)]["karar"] == r.karar
                                                                                for r in Dg.itertuples()))
        ys = os.path.join(GE.GE_YOL["cikti"], "etiket_olcu.csv.gz")
        if os.path.exists(ys):
            Ls = pd.read_csv(ys)
            Lg = Ls[np.isfinite(Ls.h5) & np.isfinite(Ls.es_h5)]
            Js = json.load(open(os.path.join(GE.GE_YOL["cikti"], "sonuc_C.json"), encoding="utf-8"))
            od = Lg[Lg.karar != "OLMAZ"]
            kontrol("yeniden üretim: ölçü 1b OLMAZ-DEĞİL n ve KAT5 satır dosyasından", Js["olcu1b"]["OLMAZ-DEĞİL"]["n"] == len(od) and
                    abs(Js["olcu1b"]["OLMAZ-DEĞİL"]["h5_kat"] - od.h5.sum() / od.es_h5.sum()) < 1e-9)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\nGEÇTİ {len(GECTI)}  KALDI {len(KALDI)}")
    if KALDI:
        print("KALAN: " + "; ".join(KALDI))
        sys.exit(1)


if __name__ == "__main__":
    main()
