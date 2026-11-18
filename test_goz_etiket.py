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
9) hakem turları (tur ac / model / olc): örneklem 30 (katmanlar), AŞAMA A ve önceki turların olay / hisseleri hariç, sonuç sütunu okunmaz
   (silinince / bozulunca aynı), t sonrası bozulunca PNG aynı, PDF'te cevap satırı var / tarih / hisse adı yok, mühür (üzerine yazılmaz),
   mühür sırası (geçici git deposu), BAŞARI elle, olc uçtan uca + birikimli; gerçek tur 1 dosyaları yeniden üretim
Çalıştır: python test_goz_etiket.py
"""
import json
import os
import re
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
        # ---------------------------------------------------------------- 9) HAKEM TURLARI (tur ac / model / olc)
        print("9) hakem turları: örneklem dışlama, sonuç sütunu yok, PDF'te sonrası / hisse adı yok, mühür sırası, BAŞARI elle")
        tk = os.path.join(tmp, "tur_cikti"); os.makedirs(tk)
        Xt = sahte_olay(n_sembol=90, tohum=21)
        yt = os.path.join(tmp, "olay_tur.csv"); Xt.to_csv(yt, index=False)
        Pt = Xt[["pazar", "sembol", "tarih"]].copy(); Pt["F19"] = (np.random.default_rng(31).random(len(Pt)) < 0.5).astype(float)
        Pt.loc[Pt.index[::17], "F19"] = np.nan
        Pt.assign(tarih=pd.to_datetime(Pt.tarih).dt.strftime("%Y-%m-%d")).to_csv(os.path.join(tk, "parmak_Y1.csv.gz"), index=False)
        Pt11 = Pt.copy(); Pt11["F19"] = (np.random.default_rng(32).random(len(Pt11)) < 0.5).astype(float)   # P1.1 dosyası (tur >= 2) ayrı
        Pt11.loc[Pt11.index[::19], "F19"] = np.nan
        Pt11.assign(tarih=pd.to_datetime(Pt11.tarih).dt.strftime("%Y-%m-%d")).to_csv(os.path.join(tk, "parmak_Y1_p11.csv.gz"), index=False)
        try:
            GE.ge_tur_orneklem(1, yt, tk); ok = False
        except GE.GEHata:
            ok = True
        kontrol("tur: AŞAMA A anahtarı yoksa dışlama yapılamaz -> DURUR", ok)
        uyg = Xt[Xt.donem.isin(["2023", "2024-26"]) & (pd.to_datetime(Xt.giris) <= pd.Timestamp("2026-08-01"))]
        A0 = uyg.sample(25, random_state=4)
        json.dump({"olay": {str(i + 1): {"sembol": r.sembol, "pazar": r.pazar, "tarih": str(pd.Timestamp(r.tarih).date()),
                                         "giris": str(pd.Timestamp(r.giris).date()), "donem": r.donem} for i, r in enumerate(A0.itertuples())}},
                  open(os.path.join(tk, "anahtar.json"), "w"))
        hisse0 = {(r.pazar, r.sembol) for r in A0.itertuples()}
        S1 = GE.ge_tur_orneklem(1, yt, tk); S1b = GE.ge_tur_orneklem(1, yt, tk)
        dag = S1.groupby(["pazar", "parmak"]).size().to_dict()
        bek = {(p, d): k for p, d, k in GE.GE_TUR_ESIK["katman"]}
        pk = S1.merge(Pt.assign(tarih=pd.to_datetime(Pt.tarih)), on=["pazar", "sembol", "tarih"])
        kontrol("tur örneklem: parmak katmanı F19 dosyasıyla aynı; F19 NaN olay girmez", len(pk) == 30 and (pk.F19 == pk.parmak).all())
        kontrol("tur örneklem: 30 sayfa, parmak ABD 10+10 / AVR 3+2 / BIST 2+3, sayfa 1..30, aynı tohum aynı örneklem",
                len(S1) == 30 and dag == bek and list(S1.sayfa) == list(range(1, 31)) and S1.equals(S1b), str(dag))
        kontrol("tur örneklem: AŞAMA A hisseleri ve olayları hariç; turda bir hisse bir kez",
                not any((r.pazar, r.sembol) in hisse0 for r in S1.itertuples()) and not S1.duplicated(["pazar", "sembol"]).any())
        kontrol("tur örneklem: uygunluk (dönem 2023 / 2024-26, giriş <= kriz - 30 gün)",
                S1.donem.isin(["2023", "2024-26"]).all() and (S1.giris <= pd.Timestamp("2026-08-01")).all())
        Xd = Xt.drop(columns=["h5", "h10", "st5", "es_h5", "es_st5", "getiri", "olc"]); yd_ = os.path.join(tmp, "olay_tur_sonucsuz.csv"); Xd.to_csv(yd_, index=False)
        Xk = Xt.copy()
        for c_ in ["h5", "es_h5", "getiri", "olc"]:
            Xk[c_] = "BOZUK"
        yk_ = os.path.join(tmp, "olay_tur_bozuk.csv"); Xk.to_csv(yk_, index=False)
        kontrol("tur örneklem SONUÇ SÜTUNUNA BAKMAZ: sonuç sütunları silinince / bozulunca aynı örneklem",
                GE.ge_tur_orneklem(1, yd_, tk).equals(S1) and GE.ge_tur_orneklem(1, yk_, tk).equals(S1))
        kontrol("tur örneklem: tur no tohumu değiştirir (tur 1 != tur 2 sayfaları)",
                not GE.ge_tur_orneklem(2, yt, tk, gosterilen=GE.ge_tur_gosterilen(1, tk)).equals(S1))

        def tur_anahtar(no, S):
            kl = GE.ge_tur_klasor(no, tk); os.makedirs(kl, exist_ok=True)
            json.dump({"sayfa": {str(int(r.sayfa)): {"sembol": r.sembol, "pazar": r.pazar, "tarih": str(pd.Timestamp(r.tarih).date()),
                                                    "giris": str(pd.Timestamp(r.giris).date()), "donem": r.donem} for r in S.itertuples()}},
                      open(GE.ge_tur_yol("anahtar", no, tk), "w"))
        try:
            GE.ge_tur_gosterilen(2, tk); ok = False
        except GE.GEHata:
            ok = True
        kontrol("tur: önceki turun anahtarı yoksa DURUR (turlar sırayla)", ok)
        tur_anahtar(1, S1)
        S2 = GE.ge_tur_orneklem(2, yt, tk)
        pk2 = S2.merge(Pt11.assign(tarih=pd.to_datetime(Pt11.tarih)), on=["pazar", "sembol", "tarih"])
        kontrol("tur 2 örneklem (T1.2): parmak katmanı P1.1 dosyasından (parmak_Y1_p11), kotalar aynı",
                len(pk2) == 30 and (pk2.F19 == pk2.parmak).all() and S2.groupby(["pazar", "parmak"]).size().to_dict() == bek)
        kontrol("tur 2 örneklem: tur 1 ve AŞAMA A hisseleri hariç",
                not ({(r.pazar, r.sembol) for r in S2.itertuples()} & ({(r.pazar, r.sembol) for r in S1.itertuples()} | hisse0)))
        try:
            GE.ge_tur_ac(2, tk, png=os.path.join(tmp, "png2"), olay=yt); ok = False
        except GE.GEHata as ex:
            ok = "ölçülmedi" in str(ex)
        kontrol("tur ac: önceki tur ölçülmeden (Cemal yanıtlamadan) sonraki tur açılmaz", ok)
        try:
            GE.ge_tur_ac(1, tk, png=os.path.join(tmp, "pngx"), olay=yt); ok = False
        except GE.GEHata as ex:
            ok = "zaten" in str(ex)
        kontrol("tur ac: açılmış tur üzerine yazılmaz", ok)
        try:
            GE.ge_tur_ac(3, tk, png=os.path.join(KOK, "tur_png_yasak"), olay=yt); ok = False
        except GE.GEHata as ex:
            ok = "repo içinde" in str(ex)
        kontrol("tur ac: PNG klasörü repo içinde olamaz", ok)
        # görsel: t sonrası yok
        dh = GE.ge_hazir(rastgele_hisse(1500, 44)); ia, _T = al_gunleri(dh)
        it = [i for i in ia if i >= 200][0]; t_ = dh.index[it]
        G0 = GE.ge_gorsel_veri(dh, t_, hazir=True)
        pt = os.path.join(tmp, "tpng"); os.makedirs(pt)
        GE.ge_tur_sayfa_png(dh, t_, 1, os.path.join(pt, "No_1.png"), G0["hat"], G0["tavan"])
        db = dh.copy(); db.iloc[it + 1:, :4] = db.iloc[it + 1:, :4].to_numpy() * 3.0
        p2 = os.path.join(tmp, "No_1b.png"); GE.ge_tur_sayfa_png(db, t_, 1, p2, G0["hat"], G0["tavan"])
        kontrol("tur görsel: t sonrası barlar bozulunca PNG baytları aynı (sonrası yok)",
                open(os.path.join(pt, "No_1.png"), "rb").read() == open(p2, "rb").read())
        try:
            GE.ge_tur_sayfa_png(dh, t_, 1, os.path.join(tmp, "x.png"), G0["hat"] * 1.01, G0["tavan"]); ok = False
        except GE.GEHata:
            ok = True
        kontrol("tur görsel: hat olay dosyasıyla tutmazsa DURUR", ok)
        shutil.copyfile(os.path.join(pt, "No_1.png"), os.path.join(pt, "No_2.png"))
        yp = GE.ge_tur_pdf(9, [1, 2], pt, os.path.join(tmp, "TUR_9_KOR.pdf"))
        import pypdf
        rd = pypdf.PdfReader(yp); met = [pg.extract_text() for pg in rd.pages]
        kontrol("tur PDF: sayfa sayısı, her sayfada 'Cemal: ✓ OLUR / X OLMAZ / ? BELİRSİZ' satırı",
                len(rd.pages) == 2 and all(("✓ OLUR" in m and "X OLMAZ" in m and "? BELİRSİZ" in m) for m in met), met[0][-80:].replace("\n", " "))
        yp2 = GE.ge_tur_pdf(9, [1, 2], pt, os.path.join(tmp, "TUR_9_KOR_iki.pdf"), iki_soru=True)
        met2 = [pg.extract_text() for pg in pypdf.PdfReader(yp2).pages]
        kontrol("tur PDF iki soru (T1.2, CD8): her sayfada A) bölge / tavan doğru mu ✓ / X ve B) bu mumdan girilir mi ✓ OLUR / X OLMAZ / ? BELİRSİZ",
                len(met2) == 2 and all(("A) Kodun bölgesi / tavanı doğru mu" in m and "B) Bu mumdan girilir mi" in m and "✓ OLUR" in m
                                        and "X OLMAZ" in m and "? BELİRSİZ" in m) for m in met2)
                and not any("A) Kodun bölgesi" in m for m in met), met2[0][-160:].replace("\n", " "))
        kontrol("tur PDF: metinde tarih / hisse adı yok; üst veri boş",
                not any(re.search(r"\d{4}-\d{2}-\d{2}|S\d{3}", m) for m in met) and not (rd.metadata or {}).get("/Author"))
        # parmak izi F19 elle + prefix
        n_ = 300; O_ = np.full(n_, 10.0); C_ = O_.copy(); H_ = np.full(n_, 10.5); L_ = np.full(n_, 9.5)   # TR = 1 -> ATR 1
        i_ = 299; hat_ = 9.5
        for j_, (o, h, l, c) in enumerate([(9.6, 9.9, 9.55, 9.8), (9.7, 9.95, 9.6, 9.65), (9.62, 9.9, 9.58, 9.85), (9.8, 10.1, 9.7, 10.0)]):
            O_[i_ - 4 + j_], H_[i_ - 4 + j_], L_[i_ - 4 + j_], C_[i_ - 4 + j_] = o, h, l, c
        P1 = GE.ge_parmak_bar(O_, H_, L_, C_, hat_, i_)
        # elle: hiza (9.7-9.55)/1 = 0.15 <= 0.5; hat: 9.55 >= 9.405 ve 9.7 <= 9.88; alt fitil medyan {0.0714,0.1429,0.0938,0.25} = 0.1183; boy medyan 0.35 <= 0.9
        kontrol("parmak F19 elle: dört koşul tutar -> 1 (ATR 1)", P1["F19"] == 1.0 and abs(P1["atr"] - 1.0) < 1e-12, str(P1))
        L2_ = L_.copy(); L2_[i_ - 1] = 9.3; P2 = GE.ge_parmak_bar(O_, H_, L2_, C_, hat_, i_)
        kontrol("parmak F19 elle: bir dip hattın %1 altına inince (b) tutmaz -> 0", P2["F19"] == 0.0 and P2["pb"] == 0.0)
        H3_ = H_.copy(); H3_[i_] = 99.0; L3_ = L_.copy(); L3_[i_] = 0.1
        kontrol("parmak F19: t barı ve sonrası okunmaz", GE.ge_parmak_bar(O_, H3_, L3_, C_, hat_, i_) == P1)
        kontrol("parmak F19: ATR için 120 bar yoksa NaN", np.isnan(GE.ge_parmak_bar(O_, H_, L_, C_, hat_, 100)["F19"]))
        # P1.1 (hiza <= 0,7; max Low <= hat x 1,06) elle; P1.0 sha / sürüm korunur
        E11 = GE.ge_parmak_surum("P1.1")["esik"]
        kontrol("parmak sürümleri: P1.0 sha c41e3e50 aynen (tur 1), P1.1 yalnız hiza 0,7 + hat üstü 1,06 farklı, sha sabit",
                GE.ge_parmak_surum("P1.0")["sha"].startswith("c41e3e509b5d") and GE.ge_esik_sha(GE.GE_PARMAK_ESIK).startswith("c41e3e509b5d")
                and GE.GE_PARMAK_ESIK["hiza_atr"] == 0.5 and GE.GE_PARMAK_ESIK["hat_ust"] == 1.04
                and {k for k in E11 if E11[k] != GE.GE_PARMAK_ESIK.get(k)} == {"surum", "tanim", "hiza_atr", "hat_ust"}
                and E11["hiza_atr"] == 0.7 and E11["hat_ust"] == 1.06 and GE.ge_parmak_surum("P1.1")["sha"].startswith("1063e67354ea"))
        L4_ = L_.copy(); L4_[i_ - 1] = 9.55 + 0.6     # hiza (10.15 - 9.55) / 1 = 0,60: P1.0 (0,5) tutmaz, P1.1 (0,7) tutar
        O4_, C4_, H4_ = O_.copy(), C_.copy(), H_.copy(); O4_[i_ - 1], C4_[i_ - 1], H4_[i_ - 1] = 10.2, 10.4, 10.5
        # max Low 10.15 / hat 9.5 = 1,068 > 1,06 -> hat'ı 9.6'ya al: min 9.55 >= 9.504, max 10.15 <= 10.176 (P1.1), > 9.984 (P1.0)
        Pa0 = GE.ge_parmak_bar(O4_, H4_, L4_, C4_, 9.6, i_); Pa1 = GE.ge_parmak_bar(O4_, H4_, L4_, C4_, 9.6, i_, E11)
        kontrol("parmak P1.1 elle: hiza 0,60 ve max Low / hat 1,057 -> P1.0 = 0 (pa, pb tutmaz), P1.1 = 1",
                Pa0["F19"] == 0.0 and Pa0["pa"] == 0.0 and Pa0["pb"] == 0.0 and Pa1["F19"] == 1.0, f"{Pa0} {Pa1}")
        kontrol("tur eşik: tur 1 -> T1.1 (sha 47284ac6 aynen, P1.0, tek soru); tur >= 2 -> T1.2 (P1.1, iki soru, katman ve tohum tabanı aynı)",
                GE.ge_tur_esik(1) is GE.GE_TUR_ESIK and GE.ge_esik_sha(GE.GE_TUR_ESIK).startswith("47284ac6dc6c")
                and GE.ge_tur_esik(2)["parmak_surum"] == "P1.1" and GE.ge_tur_esik(2)["iki_soru"] is True
                and GE.ge_tur_esik(2)["katman"] == GE.GE_TUR_ESIK["katman"] and GE.ge_tur_esik(3)["tohum_taban"] == 100)
        yc2 = os.path.join(tmp, "cemal_iki.json")
        json.dump({"1": {"A": "✓", "B": "X"}, "2": {"A": "X", "B": "?"}, "3": "✓", "4": {"A": "z", "cevap": "OLUR"}}, open(yc2, "w", encoding="utf-8"),
                  ensure_ascii=False)
        Ci = GE.ge_tur_cemal_oku(yc2, [1, 2, 3, 4, 5])
        kontrol("Cemal yanıtı iki soru: B -> karar (OLMAZ / BELİRSİZ / OLUR), A -> DOĞRU / YANLIŞ, eski biçim ve eksik sayfa geçerli",
                Ci.cemal.tolist() == ["OLMAZ", "BELİRSİZ", "OLUR", "OLUR", None]
                and [x if isinstance(x, str) else None for x in Ci.cemal_bolge] == ["DOĞRU", "YANLIŞ", None, None, None], str(Ci[["cemal", "cemal_bolge"]].values.tolist()))
        okp = True; nd = 0
        for ia_ in ia[:40]:
            if ia_ < 130:
                continue
            tt = dh.index[ia_]
            r_full = GE.ge_parmak_hisse(dh, [tt], hazir=True)[0]
            r_kes = GE.ge_parmak_hisse(dh[dh.index <= tt], [tt], hazir=True)[0]
            esit = (lambda a, b: all((np.isnan(a[k]) and np.isnan(b[k])) or a[k] == b[k] for k in a))
            okp &= esit(r_full, r_kes)
            if ia_ <= it:      # db: it'den sonraki barlar bozuk -> t <= it için aynı olmalı
                okp &= esit(r_full, GE.ge_parmak_hisse(db, [tt], hazir=True)[0])
            nd += 1
        kontrol("parmak F19 prefix: veri t'de kesilince / t sonrası bozulunca aynı (al günleri)", okp and nd > 0, f"{nd} gün")
        # model etiketi + mühür
        def etiket_yaz(yol, sayfalar, karar_f):
            json.dump({"etiket": {str(s): {"karar": karar_f(s), "nedenler": ["C5+", "CD2-"], "guven": 3, "not": "x"} for s in sayfalar}},
                      open(yol, "w", encoding="utf-8"), ensure_ascii=False)
        ye1 = os.path.join(tmp, "model1.json")
        etiket_yaz(ye1, range(1, 31), lambda s: GE.GE_KARARLAR[s % 3])
        M1 = GE.ge_tur_model(1, ye1, tk)
        kontrol("tur model: kopya + sha mühürü (tur_1_muhur.json)",
                M1["model_sha"] == GE._ge_sha_dosya(GE.ge_tur_yol("model", 1, tk)) == GE._ge_sha_dosya(ye1) and M1["n"] == 30)
        try:
            GE.ge_tur_model(1, ye1, tk); ok = False
        except GE.GEHata:
            ok = True
        kontrol("tur model: mühür üzerine yazılmaz", ok)
        bad = os.path.join(tmp, "bad.json")
        hatalar = 0
        for fn in (lambda: etiket_yaz(bad, range(1, 30), lambda s: "OLUR"),
                   lambda: etiket_yaz(bad, range(1, 31), lambda s: "EVET"),
                   lambda: json.dump({"etiket": {str(s): {"karar": "OLUR", "nedenler": ["Z9+"]} for s in range(1, 31)}}, open(bad, "w"))):
            fn()
            try:
                GE.ge_tur_etiket_oku(bad, list(range(1, 31)))
            except GE.GEHata:
                hatalar += 1
        kontrol("tur model etiketi: eksik sayfa / geçersiz karar / geçersiz neden kodu DURUR", hatalar == 3)
        kontrol("tur cevap: ✓ / x / ? / belirsiz / OLMAZ / {'cevap': '✔'} normalleşir, 'evet' geçersiz",
                [GE.ge_tur_cevap_norm(v) for v in ("✓", "x", "?", "belirsiz", "OLMAZ", {"cevap": "✔"}, "evet")] ==
                ["OLUR", "OLMAZ", "BELİRSİZ", "BELİRSİZ", "OLMAZ", "OLUR", None])
        # BAŞARI elle
        Dm = pd.DataFrame({"sayfa": range(1, 11),
                           "model": ["OLUR", "OLUR", "OLUR", "OLMAZ", "OLMAZ", "OLMAZ", "OLMAZ", "BELİRSİZ", "OLUR", None],
                           "h5": [1, 0, 1, 0, 0, 1, 0, 1, np.nan, 1], "es_h5": [.4, .3, .5, .2, .4, .6, .3, .5, .4, .2]})
        g_ = GE.ge_tur_taraf(Dm, "model")
        from scipy.stats import fisher_exact
        pf = fisher_exact([[2, 1], [1, 3]])[1]
        kontrol("tur BAŞARI elle: (2 doğru OLUR + 3 doğru OLMAZ) / 7 karar; BELİRSİZ 1, yanıtsız 1, ölçülemedi 1; Fisher; taban; yanılınan [2, 6]",
                abs(g_["basari"] - 5 / 7) < 1e-12 and g_["karar"] == 7 and g_["BELİRSİZ"] == 1 and g_["yanitsiz"] == 1 and g_["olculemedi"] == 1
                and abs(g_["isabet_OLUR"] - 2 / 3) < 1e-12 and abs(g_["isabet_OLMAZ"] - 3 / 4) < 1e-12 and abs(g_["fisher_p"] - pf) < 1e-12
                and abs(g_["taban_es"] - np.mean([.4, .3, .5, .2, .4, .6, .3, .5, .2])) < 1e-12 and g_["yanilinan"] == [2, 6]
                and abs(g_["hep_OLMAZ_basari"] - (1 - 5 / 9)) < 1e-12, str({k: g_[k] for k in ("basari", "karar", "yanilinan")}))
        # olc uçtan uca (git=False) + birikimli
        Xr = Xt.copy(); rng_t = np.random.default_rng(77)
        Xr["h5"] = (rng_t.random(len(Xr)) < 0.4).astype(float); Xr["es_h5"] = rng_t.random(len(Xr)) * 0.5
        yr = os.path.join(tmp, "olay_tur_sonuc.csv"); Xr.to_csv(yr, index=False)
        isaret = {0: "✓", 1: "X", 2: "?"}
        yc1 = os.path.join(tmp, "cemal1.json"); json.dump({str(s): isaret[s % 3] for s in range(1, 31)}, open(yc1, "w", encoding="utf-8"), ensure_ascii=False)
        R1t = GE.ge_tur_olc(1, yc1, tk, olay=yr, git=False)
        L1 = pd.read_csv(GE.ge_tur_yol("satir", 1, tk), dtype={"sembol": str})
        Lk = L1[L1.cemal.isin(["OLUR", "OLMAZ"])]
        el = (((Lk.cemal == "OLUR") & (Lk.h5 == 1)) | ((Lk.cemal == "OLMAZ") & (Lk.h5 == 0))).sum() / len(Lk)
        kh = L1.merge(Xr[["pazar", "sembol", "tarih", "h5"]].assign(tarih=lambda x: pd.to_datetime(x.tarih).dt.strftime("%Y-%m-%d")),
                      on=["pazar", "sembol", "tarih"], suffixes=("", "_x"))
        kontrol("tur olc: satır dosyası 30 sayfa, h5 olay dosyasıyla aynı; Cemal BAŞARI satır dosyasından elle aynı",
                len(L1) == 30 and len(kh) == 30 and (kh.h5 == kh.h5_x).all() and abs(R1t["cemal"]["basari"] - el) < 1e-12)
        kontrol("tur olc: model kararları mühürlü etiketten (kappa / uyum hesaplandı)",
                list(L1.model) == [GE.GE_KARARLAR[s % 3] for s in range(1, 31)] and R1t["uyum"]["n"] == 30)
        try:
            GE.ge_tur_olc(1, yc1, tk, olay=yr, git=False); ok = False
        except GE.GEHata:
            ok = True
        kontrol("tur olc: ölçülmüş tur yeniden ölçülmez (üzerine yazılmaz)", ok)
        tur_anahtar(2, S2)
        try:
            GE.ge_tur_olc(2, yc1, tk, olay=yr, git=False); ok = False
        except GE.GEHata as ex:
            ok = "mühürlü değil" in str(ex)
        kontrol("tur olc: model mühürü yoksa sonuç AÇILMAZ", ok)
        ye2 = os.path.join(tmp, "model2.json"); etiket_yaz(ye2, range(1, 31), lambda s: "OLMAZ")
        GE.ge_tur_model(2, ye2, tk)
        yc9 = os.path.join(tmp, "cemal9.json"); json.dump({"99": "✓"}, open(yc9, "w"))
        try:
            GE.ge_tur_olc(2, yc9, tk, olay=yr, git=False); ok = False
        except GE.GEHata:
            ok = True
        kontrol("tur olc: anahtarda olmayan sayfa yanıtı DURUR", ok)
        R2t = GE.ge_tur_olc(2, yc1, tk, olay=yr, git=False)
        L2 = pd.read_csv(GE.ge_tur_yol("satir", 2, tk))
        LL = pd.concat([L1, L2]); LLk = LL[LL.cemal.isin(["OLUR", "OLMAZ"])]
        elb = (((LLk.cemal == "OLUR") & (LLk.h5 == 1)) | ((LLk.cemal == "OLMAZ") & (LLk.h5 == 0))).sum() / len(LLk)
        dft = open(GE.ge_tur_yol("defter", 2, tk), encoding="utf-8").read()
        kontrol("tur birikimli: tur 1 + 2 satırlarından; TUR_DEFTERI iki bölüm; rapor hedef / taban uyarısı",
                R2t["birikimli"]["turlar"] == [1, 2] and abs(R2t["birikimli"]["cemal"]["basari"] - elb) < 1e-12
                and dft.count("## TUR 1 ") == 1 and dft.count("## TUR 2 ") == 1
                and "%80-90" in open(GE.ge_tur_yol("rapor", 2, tk), encoding="utf-8").read())
        # mühür sırası (geçici git deposu)
        import subprocess

        def git(kl, *a):
            return subprocess.run(["git", "-C", kl, "-c", "user.name=t", "-c", "user.email=t@t", *a], capture_output=True, text=True, check=True)

        def depo(ad, sira):
            kl = os.path.join(tmp, ad); os.makedirs(kl); git(kl, "init", "-q")
            json.dump({"x": 1}, open(os.path.join(kl, "model.json"), "w"))
            json.dump({"model_sha": GE._ge_sha_dosya(os.path.join(kl, "model.json"))}, open(os.path.join(kl, "muhur.json"), "w"))
            json.dump({"1": "✓"}, open(os.path.join(kl, "cemal.json"), "w"))
            for grup in sira:
                git(kl, "add", *grup); git(kl, "commit", "-q", "-m", "c")
            return kl
        sonuc_ = []
        for ad, sira in (("g_ok", [["model.json", "muhur.json"], ["cemal.json"]]), ("g_ters", [["cemal.json"], ["model.json", "muhur.json"]]),
                         ("g_ayni", [["model.json", "muhur.json", "cemal.json"]])):
            kl = depo(ad, sira)
            try:
                GE.ge_tur_sira(os.path.join(kl, "muhur.json"), os.path.join(kl, "model.json"), os.path.join(kl, "cemal.json")); sonuc_.append("TUTTU")
            except GE.GEHata:
                sonuc_.append("DURDU")
        kl = depo("g_degis", [["model.json", "muhur.json"], ["cemal.json"]])
        json.dump({"x": 2}, open(os.path.join(kl, "model.json"), "w"))
        try:
            GE.ge_tur_sira(os.path.join(kl, "muhur.json"), os.path.join(kl, "model.json"), os.path.join(kl, "cemal.json")); sonuc_.append("TUTTU")
        except GE.GEHata:
            sonuc_.append("DURDU")
        kontrol("tur mühür sırası: mühür önce = TUTTU; Cemal önce / aynı commit / model sonradan değişmiş = DURDU",
                sonuc_ == ["TUTTU", "DURDU", "DURDU", "DURDU"], str(sonuc_))
        # gerçek parmak dosyası (F19)
        ypm = os.path.join(GE.GE_YOL["cikti"], "parmak_Y1.csv.gz")
        if os.path.exists(ypm):
            Pm = pd.read_csv(ypm, dtype={"sembol": str})
            Xo = pd.read_csv(GE.GE_YOL["olay"], usecols=["deneme", "pazar", "sembol", "tarih"], dtype={"sembol": str})
            Xo = Xo[Xo.deneme == "Y1"]
            Dn = json.load(open(os.path.join(GE.GE_YOL["cikti"], "parmak_denetim.json"), encoding="utf-8"))
            kontrol("gerçek parmak_Y1: Y1 olaylarıyla aynı sıra / sayı; yaygınlık denetim dosyasıyla aynı; sha",
                    len(Pm) == len(Xo) and (Pm[["pazar", "sembol", "tarih"]].to_numpy() == Xo[["pazar", "sembol", "tarih"]].to_numpy()).all()
                    and all(int((Pm[Pm.pazar == p].F19 == 1).sum()) == v["parmak"] for p, v in Dn["pazar"].items())
                    and Dn["satir_sha"] == GE._ge_sha_dosya(ypm))
            A231 = json.load(open(os.path.join(GE.GE_YOL["cikti"], "anahtar.json"), encoding="utf-8"))["olay"]["231"]
            f231 = Pm[(Pm.pazar == A231["pazar"]) & (Pm.sembol == A231["sembol"]) & (Pm.tarih == A231["tarih"])].F19.tolist()
            print(f"  BİLGİ hakem sayfa 25 (No 231, Cemal'in parmak izi örneği): F19 = {f231} (beklenen 1; eşik değiştirilmez)")
        ypm11 = os.path.join(GE.GE_YOL["cikti"], "parmak_Y1_p11.csv.gz")
        if os.path.exists(ypm11) and os.path.exists(ypm):
            Pm11 = pd.read_csv(ypm11, dtype={"sembol": str})
            Dn11 = json.load(open(os.path.join(GE.GE_YOL["cikti"], "parmak_denetim_p11.json"), encoding="utf-8"))
            kontrol("gerçek parmak_Y1_p11 (P1.1): Y1 sırası / sayısı; yaygınlık denetimle aynı; sha; eşik sha P1.1; prefix 10 / pazar",
                    len(Pm11) == len(Xo) and (Pm11[["pazar", "sembol", "tarih"]].to_numpy() == Xo[["pazar", "sembol", "tarih"]].to_numpy()).all()
                    and all(int((Pm11[Pm11.pazar == p].F19 == 1).sum()) == v["parmak"] and v["prefix_denetimi"] == 10 for p, v in Dn11["pazar"].items())
                    and Dn11["satir_sha"] == GE._ge_sha_dosya(ypm11) and Dn11["esik_sha"] == GE.ge_parmak_surum("P1.1")["sha"]
                    and os.path.getsize(ypm11) < 2 ** 20)
            g231 = Pm11[(Pm11.pazar == A231["pazar"]) & (Pm11.sembol == A231["sembol"]) & (Pm11.tarih == A231["tarih"])].F19.tolist()
            kontrol("gerçek P1.1: hakem s25 (No 231) F19 = 1 (iş tanımı ön koşulu); P1.0'da 1 olan her olay P1.1'de de 1 (gevşetme)",
                    g231 == [1.0] and not ((Pm.F19 == 1) & (Pm11.F19 == 0)).any(), str(g231))
        # gerçek tur 1 dosyaları
        yg = GE.ge_tur_yol("anahtar", 1)
        if os.path.exists(yg):
            Sg = GE.ge_tur_anahtar_oku(1)
            Sr = GE.ge_tur_orneklem(1)
            Ag = json.load(open(os.path.join(GE.GE_YOL["cikti"], "anahtar.json"), encoding="utf-8"))["olay"]
            hg = {(v["pazar"], v["sembol"]) for v in Ag.values()}
            kontrol("gerçek tur 1: 30 sayfa, parmak katmanları, anahtar = ge_tur_orneklem(1) yeniden üretim (parmak dahil)",
                    len(Sg) == 30 and Sg.groupby(["pazar", "parmak"]).size().to_dict() == bek and (Sg.parmak == Sr.parmak).all()
                    and all(Sg[c].astype(str).tolist() == Sr[c].astype(str).tolist() for c in ("sayfa", "pazar", "sembol", "tarih")))
            kontrol("gerçek tur 1: AŞAMA A 300 örneklemin hisseleri yok; turda hisse tekil",
                    not any((r.pazar, r.sembol) in hg for r in Sg.itertuples()) and not Sg.duplicated(["pazar", "sembol"]).any())
            ypg = GE.ge_tur_yol("pdf", 1)
            rg = pypdf.PdfReader(ypg); mg = [pg.extract_text() for pg in rg.pages]
            kontrol("gerçek TUR_1_KOR.pdf: 30 sayfa, cevap satırı her sayfada, hisse adı / tarih yok, sha anahtarla aynı",
                    len(rg.pages) == 30 and all("✓ OLUR" in m and "X OLMAZ" in m and "? BELİRSİZ" in m for m in mg)
                    and not any(re.search(r"\d{4}-\d{2}-\d{2}", m) for m in mg)
                    and not any(re.search(rf"(?<![A-Za-z0-9]){re.escape(s)}(?![A-Za-z0-9])", m) for s in Sg.sembol for m in mg)
                    and json.load(open(yg, encoding="utf-8"))["pdf_sha"] == GE._ge_sha_dosya(ypg))
        # gerçek tur 2 dosyaları (T1.2: P1.1, iki soru, tohum 102)
        yg2 = GE.ge_tur_yol("anahtar", 2)
        if os.path.exists(yg2):
            J2 = json.load(open(yg2, encoding="utf-8"))
            S2g = GE.ge_tur_anahtar_oku(2); S2r = GE.ge_tur_orneklem(2)
            h1 = {(r.pazar, r.sembol) for r in GE.ge_tur_anahtar_oku(1).itertuples()}
            hg = {(v["pazar"], v["sembol"]) for v in json.load(open(os.path.join(GE.GE_YOL["cikti"], "anahtar.json"), encoding="utf-8"))["olay"].values()}
            kontrol("gerçek tur 2: 30 sayfa, P1.1 katmanları, tohum 102, anahtar = ge_tur_orneklem(2) yeniden üretim; sürüm / sha kayıtları",
                    len(S2g) == 30 and S2g.groupby(["pazar", "parmak"]).size().to_dict() == bek and (S2g.parmak == S2r.parmak).all()
                    and all(S2g[c].astype(str).tolist() == S2r[c].astype(str).tolist() for c in ("sayfa", "pazar", "sembol", "tarih"))
                    and J2["tohum"] == 102 and J2["parmak_surum"] == "P1.1" and J2["tur_esik_surum"] == "T1.2" and J2["iki_soru"] is True
                    and J2["parmak_esik_sha"] == GE.ge_parmak_surum("P1.1")["sha"]
                    and J2["parmak_sha"] == GE._ge_sha_dosya(os.path.join(GE.GE_YOL["cikti"], "parmak_Y1_p11.csv.gz")))
            kontrol("gerçek tur 2: AŞAMA A 300 ve tur 1 hisseleri / olayları yok; turda hisse tekil",
                    not any((r.pazar, r.sembol) in (hg | h1) for r in S2g.itertuples()) and not S2g.duplicated(["pazar", "sembol"]).any())
            yp2g = GE.ge_tur_yol("pdf", 2)
            r2 = pypdf.PdfReader(yp2g); m2 = [pg.extract_text() for pg in r2.pages]
            kontrol("gerçek TUR_2_KOR.pdf: 30 sayfa, her sayfada A ve B soru satırları, hisse adı / tarih yok, sha anahtarla aynı",
                    len(r2.pages) == 30 and all("A) Kodun bölgesi / tavanı doğru mu" in m and "B) Bu mumdan girilir mi" in m and "✓ OLUR" in m
                                                and "X OLMAZ" in m and "? BELİRSİZ" in m for m in m2)
                    and not any(re.search(r"\d{4}-\d{2}-\d{2}", m) for m in m2)
                    and not any(re.search(rf"(?<![A-Za-z0-9]){re.escape(s)}(?![A-Za-z0-9])", m) for s in S2g.sembol for m in m2)
                    and J2["pdf_sha"] == GE._ge_sha_dosya(yp2g))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\nGEÇTİ {len(GECTI)}  KALDI {len(KALDI)}")
    if KALDI:
        print("KALAN: " + "; ".join(KALDI))
        sys.exit(1)


if __name__ == "__main__":
    main()
