"""K56 birim ve sentetik testler (ağ gerekmez). Çalıştırma: python test_k56.py"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from K56 import etki_envanteri as EE, finansal_mekanizma as FM, islem_davranisi as ID, karsit_ornekler as KO, kurumsal_olaylar as KOL, mekanizma as M  # noqa: E402
from K56 import mekanizma_raporu as MR, ortak as O  # noqa: E402

KORUNAN = ("K55", "COL_YOLU_ABD.py", "K51.py", "arastirma_cikti/col_yolu_abd", "arastirma_cikti/k55_dallanma", "evren_disi_ABD.csv")


class SahteIstemci(O.Istemci):
    """Ağsız: verilen bayt dizisini HTTP Range ile dilimler (zip yardımcılarını sınamak için)."""

    def __init__(self, veri: bytes):
        self.veri = veri; self.gunluk = []; self.sinir = 10 ** 9

    def bas(self, url, ek_baslik=None):
        return 200, {"Content-Length": str(len(self.veri))}

    def al(self, url, ad=None, aralik=None, sinir=None, ek_baslik=None, yontem="GET", govde=None, deneme=3):
        return (206, self.veri[aralik[0]:aralik[1] + 1], {}) if aralik else (200, self.veri, {})


def testler():
    hata = []
    git0 = subprocess.run(["git", "status", "--porcelain", "--", *KORUNAN], capture_output=True, text=True).stdout
    # 1) çıktı yolu
    for yasak in ("arastirma_cikti/col_yolu_abd", "arastirma_cikti/k55_dallanma/tam_evren", "/content/drive/MyDrive/COLAB_VERILER/OUTPUT/K55", "/tmp/k56_baska"):
        try:
            O.cikti_dogrula(yasak); hata.append(f"1) yasak yol kabul edildi: {yasak}")
        except PermissionError:
            pass
    try:
        O.cikti_dogrula(O.REPO_CIKTI)
    except PermissionError as ex:
        hata.append(f"1) K56 yolu reddedildi: {ex}")
    # 2) kaynak kaydı
    kk = O.KaynakKaydi(); A = O.K56Ayar()
    kk.oku(os.path.join(A.k55, "K55_HUCRE_SONUC.csv"), "envanter")
    try:
        kk.oku(os.path.join(A.k55, "K55_HUCRE_SONUC.csv"), "yaz"); hata.append("2) bilinmeyen amaç kabul edildi")
    except ValueError:
        pass
    if len(kk.tablo()) != 1 or len(kk.tablo().sha256.iloc[0]) != 64:
        hata.append("2) kaynak kaydı sha yok")
    # 3) ağ kapısı ve SEC e-postası
    ist = O.Istemci(O.K56Ayar(onbellek=tempfile.mkdtemp()))
    try:
        ist.al("https://www.sec.gov/"); hata.append("3) ağ kapalıyken istek gitti")
    except O.AgKapali:
        pass
    eski = os.environ.pop("SEC_EPOSTA", None)
    try:
        O.Istemci.sec_ua(); hata.append("3) SEC_EPOSTA yokken UA üretildi")
    except RuntimeError:
        pass
    if eski:
        os.environ["SEC_EPOSTA"] = eski
    G = pd.DataFrame({"url": ["https://x.sec.gov/a?u=ad.soyad@ornek.com", "https://y"]})
    G["url"] = G.url.str.replace(r"[\w.+-]+@[\w-]+\.[\w.]+", "<e-posta>", regex=True)
    if G.url.str.contains("@").any():
        hata.append("3) istek günlüğü e-posta temizlemiyor")
    for f in os.listdir(os.path.join(O.KOK, "K56")):
        if f.endswith(".py") and __import__("re").search(r"[\w.+-]+@(gmail|hotmail|yahoo|outlook)\.", open(os.path.join(O.KOK, "K56", f), encoding="utf-8").read()):
            hata.append(f"3) kodda e-posta: {f}")
    # 4) zip merkez dizini ve üye başı (Range ile kısmi okuma)
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("A/README.txt", "x" * 100); z.writestr("A/INFOTABLE.tsv", "CUSIP\tVALUE\n" + "".join(f"{i:09d}\t{i}\n" for i in range(20000)))
    si = SahteIstemci(b.getvalue()); L = O.zip_icerik_listesi(si, "u", "t")
    if set(L.dosya) != {"A/README.txt", "A/INFOTABLE.tsv"}:
        hata.append(f"4) zip listesi yanlış: {L.to_dict()}")
    bas = O.zip_uye_bas(si, "u", L, "INFOTABLE.tsv", 3000, "t"); T = pd.read_csv(io.BytesIO(bas[: bas.rfind(b"\n")]), sep="\t", dtype=str)
    if list(T.columns) != ["CUSIP", "VALUE"] or T.CUSIP.iloc[0] != "000000000" or len(T) < 100:
        hata.append(f"4) zip üye başı yanlış: {len(T)} {list(T.columns)}")
    # 5) sentetik veri: sıfır beklenen getiri, tohum kararlılığı
    V, EV, E = M.sentetik_veri(30, 600, 7, "garch_t"); V2, _, _ = M.sentetik_veri(30, 600, 7, "garch_t")
    r = np.concatenate([np.diff(np.log(d.Close.to_numpy())) for d in V.values()])
    if abs(r.mean()) > 3 * r.std() / np.sqrt(len(r)) + 2e-4 or not V["S0000"].equals(V2["S0000"]):
        hata.append(f"5) sentetik veri ortalama / tohum: {r.mean():.2e}")
    if not all(((d.High >= d[["Open", "Close"]].max(axis=1)) & (d.Low <= d[["Open", "Close"]].min(axis=1))).all() for d in V.values()):
        hata.append("5) sentetik OHLC tutarsız")
    # 6) sentetik sınıf eşikleri
    beklenen = [((-0.30, -0.4, -0.2, -0.25), "MEKANIK_ACIKLAR"), ((-0.08, -0.15, -0.01, -0.25), "KISMEN_MEKANIK"), ((-0.03, -0.1, 0.04, -0.25), "MEKANIK_IZ_YOK"),
                ((0.2, 0.1, 0.3, -0.25), "TERS_ISARET"), ((-0.3, -0.5, 0.1, -0.25), "MEKANIK_IZ_YOK"), ((np.nan, 0, 0, -0.2), "TANIMSIZ")]
    for (ds, a, u, dg), k in beklenen:
        if M.sentetik_sinif(ds, a, u, dg) != k:
            hata.append(f"6) sentetik_sinif({ds},{a},{u},{dg}) = {M.sentetik_sinif(ds, a, u, dg)} != {k}")
    # 7) M01 yöntemi iki yönlü: rastgele değişken d ~ 0 (olumsuz kontrol), 5 gün getirisi güçlü negatif (mekanik olumlu kontrol)
    V, EV, E = M.sentetik_veri(120, 900, 11, "gauss"); P, Ol = M.sentetik_panel(V, EV, E); rng = np.random.default_rng(1)
    P["rast"] = np.random.default_rng(5).normal(size=len(P)); P["r5"] = P.groupby("sembol").close.pct_change(5)
    a0 = M.a_d(P, Ol, "rast", "Y60", 200, rng); a1 = M.a_d(P, Ol, "r5", "Y60", 200, rng); a5 = M.a_d(P, Ol, "r5", "Y60", 200, rng, gecikme=20)
    if not (abs(a0["d"]) < 0.1 and a1["d"] < -0.15 and a1["d_ust"] < 0 and abs(a5["d"]) < abs(a1["d"]) / 2):
        hata.append(f"7) M01 kontrol: rastgele d {a0['d']:.3f}, r5 d {a1['d']:.3f} [{a1['d_alt']:.3f}, {a1['d_ust']:.3f}], r5 gecikme20 {a5['d']:.3f}")
    # 8) hipotez kaydı: tekil, zorunlu alanlar, veri kaynakları tanımlı
    H = M.hipotez_tablosu(); kay = {k["kimlik"] for k in MR.KAYNAKLAR}
    for h in M.HIPOTEZLER:
        if not all(h.get(a) for a in ("dogruysa", "yanlissa", "curutme", "veri", "karsit", "yarisan")):
            hata.append(f"8) {h['kimlik']} alanı eksik")
        if [v for v in h["veri"] if v not in kay]:
            hata.append(f"8) {h['kimlik']} tanımsız kaynak: {[v for v in h['veri'] if v not in kay]}")
        if [g for g in h["karsit"] if g not in {x['grup'] for x in KO.GRUPLAR}]:
            hata.append(f"8) {h['kimlik']} tanımsız karşıt grup")
    if len(H) < 15 or "M14" not in set(H.kimlik):
        hata.append("8) hipotez sayısı / kasıt hipotezi")
    if not any(h["kimlik"] == "M14" and "resmî kayıt" in h["aciklama"] for h in M.HIPOTEZLER):
        hata.append("8) kasıt hipotezi resmî kayıt şartını yazmıyor")
    # 9) envanter: ön sınıf kuralları ve denetim
    r = pd.Series({"kimlik": "K55-D01-S02", "kaynak_calisma": "K55", "sinif": "TERS_YONLU", "m01_sentetik": "MEKANIK_ACIKLAR", "m01_oran_Y60": 1.1})
    if not EE.on_sinif(r)[0].startswith(M.YANLIS_ADAY):
        hata.append("9) M01 mekanik -> YANLIŞ BULGU ADAYI kuralı (sentetik tek başına kesin sınıf vermez)")
    for kar, sin, bek in (("DESTEKLENMİYOR (2016-22: TUTMAZ | 2023: TUTAR)", "DONEM_CELISKILI", M.ETKI_SAGLAM_DEGIL), ("TUTMAZ / TUTMAZ / TUTMAZ", "KUCUK_ETKI", M.ETKI_SAGLAM_DEGIL),
                          ("H4 DESTEKLENİYOR", "KUCUK_ETKI", "İLİŞKİ VAR, NEDEN BELİRSİZ"), ("kaynakta karar yok (bilgi)", "TERS_YONLU", M.BETIMLEYICI), ("ÖLÇÜLEMEDİ", "VERI_YETERSIZ", "VERİ YETERSİZ")):
        o_ = EE.on_sinif(pd.Series({"kimlik": "K51-X", "kaynak_calisma": "K51", "sinif": sin, "eski_karar": kar}))[0]
        if o_ != bek:
            hata.append(f"9) ön sınıf kuralı: '{kar}' / {sin} -> {o_} (beklenen {bek})")
    if EE.on_sinif(pd.Series({"kimlik": "K51-H3", "kaynak_calisma": "K51", "sinif": "BASARISIZ"}))[0] != M.ETKI_YOK:
        hata.append("9) başarısız bulgu sonradan sınıf aldı")
    E = pd.DataFrame([{"kimlik": "K51-H1", "eski_karar": "DESTEKLENMİYOR (küçük)", "kaynak_calisma": "K51", "olasi_aciklamalar": ["a"], "dogrulayici_veri": ["b"]},
                      {"kimlik": "K51-H2", "eski_karar": "DESTEKLENİYOR", "kaynak_calisma": "K51", "olasi_aciklamalar": [], "dogrulayici_veri": ["b"]}])
    kod = {EE._norm("K51-H1"): {"kod": "H1", "karar": "DESTEKLENMİYOR", "dosya": "cy_hipotez.csv"}, EE._norm("K51-H2"): {"kod": "H2", "karar": "DESTEKLENMİYOR", "dosya": "cy_hipotez.csv"},
           EE._norm("K51-H9"): {"kod": "H9", "karar": "ÖLÇÜLEMEDİ", "dosya": "cy_hipotez.csv"}}
    D = EE.denetle(E, kod); t = set(D.tur)
    if not {"envanterde_yok", "karar_uyusmuyor", "bos_olasi_aciklamalar"} <= t:
        hata.append(f"9) denetim eksik: {t}")
    with tempfile.TemporaryDirectory() as td:
        y = os.path.join(td, "k.json"); json.dump({"bulgular": [{a: "x" for a in EE.ALANLAR}, {a: "x" for a in EE.ALANLAR}]}, open(y, "w"))
        try:
            EE.kurasyon_yukle(y); hata.append("9) yinelenen kimlik kabul edildi")
        except ValueError:
            pass
    # 9b) tam kimlik önce: H10 kodu H10-BIST-META'ya eşlenmez
    E2 = pd.DataFrame([{"kimlik": k, "eski_karar": "DESTEKLENMİYOR", "kaynak_calisma": "K51", "olasi_aciklamalar": ["a"], "dogrulayici_veri": ["b"]} for k in ("K51-H10-P1", "K51-H10-BIST-META", "K51-H10")]) 
    D2 = EE.denetle(E2, {EE._norm("K51-H10"): {"kod": "H10", "karar": "DESTEKLENMİYOR", "dosya": "cy_hipotez.csv"}}); D2 = D2[D2.tur != "k55_hucre_sayisi"]
    if len(D2):
        hata.append(f"9b) tam kimlik eşleşmesi: {D2.to_dict('records')}")
    # 9c) hatalı / boş sentetik satır TANIMSIZ (HATA) olur
    Zt = M.sentetik_ozet(pd.DataFrame([{"hucre": "X", "ufuk": "Y60", "gecikme": 0, "d": np.nan, "d_alt": np.nan, "d_ust": np.nan, "spek": "gauss", "tohum": 1}]),
                         pd.DataFrame([{"hucre": "X", "durum": "KEŞİF", "varyant": "X|5", "yon": 1, "d_gercek_Y60": -0.2, "d_gercek_Y120": np.nan, "d_gercek_Y250": np.nan}]))
    if Zt.karar.iloc[0] != "TANIMSIZ (HATA)":
        hata.append(f"9c) hatalı sentetik satır: {Zt.karar.iloc[0]}")
    # 10) olay sayıları ve ad normalizasyonu
    T = pd.DataFrame({"form": ["8-K", "8-K", "S-3", "424B2", "SC 13D/A", "25-NSE"], "tarih": pd.to_datetime(["2017-01-01"] * 6), "madde": ["2.02,9.01", "1.03", "", "", "", ""]})
    s = KOL.olay_sayilari(T)
    if not (s["8K_iflas"] == 1 and s["ihrac_izahname"] == 1 and s["borc_notu_424B2"] == 1 and s["sahiplik_13D"] == 1 and s["kot_cikis"] == 1):
        hata.append(f"10) olay sayıları: {s}")
    if KOL._ad_norm("Moleculin Biotech, Inc.") != KOL._ad_norm("MOLECULIN BIOTECH INC") or KOL._ad_norm("Inc.") != "":
        hata.append("10) ad normalizasyonu")
    # 10b) askıya alma eşlemesi: tarih şartı (ilk başvurudan önce eşleşmez), belirsiz ad, panel penceresi
    Jt = {"1": {"name": "Meridian Corp", "date": ["2018-08-24", "2020-01-01"], "form": [], "formerNames": []},
          "2": {"name": "Acme Inc", "date": ["2010-01-01"], "form": [], "formerNames": []}, "3": {"name": "ACME CORP", "date": ["2011-01-01"], "form": [], "formerNames": []},
          "4": {"name": "Yeni Ad Inc", "date": ["2012-01-01"], "form": [], "formerNames": [{"name": "Eski Ad Inc", "from": "2012-01-01T00:00:00Z", "to": "2015-06-01T00:00:00Z"}]}}
    St = pd.DataFrame([{"tarih": pd.Timestamp("2017-09-18"), "ad": "Meridian Co., Ltd.", "no": "34-1"}, {"tarih": pd.Timestamp("2016-01-05"), "ad": "Acme, Inc.", "no": "34-2"},
                       {"tarih": pd.Timestamp("2014-03-01"), "ad": "Eski Ad Inc.", "no": "34-3"}, {"tarih": pd.Timestamp("2016-03-01"), "ad": "Eski Ad Inc.", "no": "34-4"}])
    EVt = pd.DataFrame({"cik": [4], "ilk_islem": ["2013-01-01"], "son_islem": ["2020-01-01"]})
    Et = KOL.askiya_eslestir(St, Jt, EVt).set_index("no")
    if not (Et.loc["34-1", "durum"] == "yok" and Et.loc["34-2", "durum"] == "belirsiz" and Et.loc["34-3", "durum"] == "eslesti" and bool(Et.loc["34-3", "panel_penceresinde"])
            and Et.loc["34-4", "durum"] == "yok"):
        hata.append(f"10b) askıya alma eşlemesi: {Et.durum.to_dict()}")
    # 10c) SEC e-postalı başlık yalnız sec.gov sunucularına
    if not (O.Istemci.sec_mi("https://data.sec.gov/x") and O.Istemci.sec_mi("https://www.sec.gov/") and not O.Istemci.sec_mi("https://evil.example/?u=sec.gov")
            and not O.Istemci.sec_mi("https://sec.gov.evil.example/")):
        hata.append("10c) SEC sunucu denetimi")
    # 11) sulandırma ölçüsü
    T = pd.DataFrame({"filed": pd.to_datetime(["2017-01-10", "2017-04-10", "2017-07-10", "2018-01-10", "2018-04-10"]), "val": [100, 100, 110, 130, 140]})
    if not abs(FM.sulandirma(T) - 0.40) < 1e-9:
        hata.append(f"11) sulandırma {FM.sulandirma(T)}")
    J = {"facts": {"dei": {"EntityCommonStockSharesOutstanding": {"units": {"shares": [{"end": "2017-01-01", "filed": "2017-02-01", "val": 5}]}}}}}
    if len(FM.kavram_serisi(J, ["dei:EntityCommonStockSharesOutstanding"])) != 1 or len(FM.kavram_serisi(J, ["us-gaap:Yok"])):
        hata.append("11) kavram serisi")
    # 12) spread tahminleri geleceğe bakmaz ve negatif değil
    d = M.sentetik_veri(1, 400, 3, "gauss")[0]["S0000"]
    for f in (ID.corwin_schultz, ID.abdi_ranaldo):
        x = f(d).to_numpy(); xk = f(d.iloc[:300]).to_numpy()
        if not np.allclose(x[:300], xk, equal_nan=True) or (np.nan_to_num(x) < 0).any():
            hata.append(f"12) {f.__name__} geleceğe bakıyor ya da negatif")
    # 13) erişim örneklemi: tekrarsız, gruplar, işlemde olma
    kk = O.KaynakKaydi(); Orn = KO.ornek_sec(O.K56Ayar(), kk)
    if len(Orn) != 12 or Orn.sembol.duplicated().any() or Orn.grup.value_counts().to_dict() != {"G1": 4, "G2": 4, "G3": 2, "G6": 2}:
        hata.append(f"13) örneklem: {Orn.grup.value_counts().to_dict()}")
    EVk = pd.read_csv(os.path.join(O.K56Ayar().k55, "K55_EVREN.csv")).set_index("sembol")
    for r in Orn[Orn.grup == "G2"].itertuples():
        if pd.to_datetime(EVk.loc[r.sembol, "ilk_islem"]) > r.tarih or pd.to_datetime(EVk.loc[r.sembol, "son_islem"]) < r.tarih:
            hata.append(f"13) G2 {r.sembol} o tarihte işlemde değil")
    # 14) rapor tabloları
    if not (len(MR.riskler()) >= 10 and len(MR.uygulama_sirasi()) >= 8 and MR.uygulama_sirasi().sira.is_monotonic_increasing and "donem" in MR.uygulama_sirasi()):
        hata.append("14) risk / sıra tabloları")
    if MR._durum_birlestir(pd.Series(["ATLANDI"])) != "ATLANDI" or MR._durum_birlestir(pd.Series(["GECTI", "ATLANDI"])) != "GECTI" or MR._durum_birlestir(pd.Series(["GECTI", "KISMI"])) != "KISMI":
        hata.append("14) erişim durumu birleştirme")
    if [k["kimlik"] for k in MR.KAYNAKLAR if k["kimlik"] not in MR.KESIF_KAPSAM]:
        hata.append(f"14) KEŞİF kapsamı tanımsız kaynak: {[k['kimlik'] for k in MR.KAYNAKLAR if k['kimlik'] not in MR.KESIF_KAPSAM]}")
    if MR.KAYNAKLAR and len({k["kimlik"] for k in MR.KAYNAKLAR}) != len(MR.KAYNAKLAR):
        hata.append("14) yinelenen kaynak kimliği")
    # 14b) Drive kopyası: sha doğrulamalı, yasak köke yazmaz
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "k", "alt"), exist_ok=True); open(os.path.join(td, "k", "a.csv"), "w").write("x,y\n1,2\n"); open(os.path.join(td, "k", "alt", "b.csv"), "w").write("z\n3\n")
        os.environ["K56_CIKTI_EK"] = td
        from K56 import surucu as SU
        Mf = SU.drive_kopyala(os.path.join(td, "k"), os.path.join(td, "h"))
        if len(Mf) != 2 or not os.path.exists(os.path.join(td, "h", "alt", "b.csv")) or not os.path.exists(os.path.join(td, "h", "K56_DRIVE_MANIFEST.csv")):
            hata.append("14b) drive_kopyala")
        try:
            SU.drive_kopyala(os.path.join(td, "k"), os.path.join(O.KOK, "arastirma_cikti", "k55_dallanma", "x")); hata.append("14b) yasak köke kopyaladı")
        except PermissionError:
            pass
        os.environ.pop("K56_CIKTI_EK", None)
    # 16) K56-F1A karar tablosu ve hücre çoğunluğu (ONKAYIT v1.2-A)
    from K56 import batan_evren as BE, faz1_yerel as F1
    vaka = [((-0.5, -0.02, -0.1, 0.06, 0.8), "MEKANİK (gerçek + sentetik)"), ((-0.5, -0.05, -0.08, -0.02, 0.1), "MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor)"),
            ((-0.5, -0.2, -0.25, -0.15, 0.8), "KISMEN MEKANİK"), ((-0.5, -0.4, -0.45, -0.35, 0.8), "GERÇEK ETKİ KALIYOR"), ((-0.5, 0.2, 0.1, 0.3, 0.8), "TERS KALINTI"),
            ((np.nan, -0.2, -0.3, -0.1, 0.8), "TANIMSIZ")]
    for g, bek in vaka:
        if F1.karar_a1(*g) != bek:
            hata.append(f"16) karar_a1{g} = {F1.karar_a1(*g)} (beklenen {bek})")
    if F1.hucre_karari(["MEKANİK (gerçek + sentetik)", "MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor)", "GERÇEK ETKİ KALIYOR"]) != "MEKANİK" or \
            F1.hucre_karari(["KISMEN MEKANİK", "GERÇEK ETKİ KALIYOR"]) != "BELİRSİZ":
        hata.append("16) hücre çoğunluğu")
    # 17) seçimsiz etiketler: sentetik veride (ii) bütün nitelikli günler seçim etkisini taşımaz, (i) ilk geçiş taşır; (iii) dizi içinde
    rng = np.random.default_rng(5); n = 4000; sem = np.repeat(["A", "B"], n // 2); i = np.tile(np.arange(n // 2), 2)
    nit = np.zeros(n, bool)
    for k in range(0, n, 97):
        nit[k:k + 25] = True                                                                 # 25 günlük kesintisiz nitelikli diziler
    ilk = nit & ~np.r_[False, nit[:-1]] ; ilk[n // 2] = nit[n // 2]
    Pz = pd.DataFrame({"sembol": sem, "i": i}); iii = F1.rastgele_gun_maskesi(Pz, ilk, nit, "test|56")
    if iii.sum() != ilk.sum() or (iii & ~nit).any():
        hata.append("17) rastgele gün nitelikli dizi dışında / sayısı yanlış")
    dz = F1.olay_dizisi_maskesi(Pz, ilk, nit)
    if (dz & ~nit).any() or not (dz[ilk]).all() or dz.sum() > nit.sum():
        hata.append("17) olay dizisi maskesi")
    x = rng.normal(size=n); x[ilk] -= 1.0                                                    # yalnız ilk günde yapay (seçim) farkı
    ay = np.repeat(np.arange(40), n // 40); yil = np.repeat([2020, 2021], n // 2)
    di = F1.a_olc(x, ilk, ay, yil, 300, rng)["d"]; dii = F1.a_olc(x, nit, ay, yil, 300, rng)["d"]
    if not (di < -0.8 and abs(dii) < abs(di) * 0.2):
        hata.append(f"17) seçimsiz etiket ayırmıyor: d(i) {di:.2f}, d(ii) {dii:.2f}")
    # 18) sızıntı kapısı: t0 günü ya da sonrası başvuru ÖNCESİ penceresine girerse durur; SONRASI t0'ı içermez
    gunler = pd.bdate_range("2020-01-01", periods=60); i0 = 30
    t_ok = np.array([gunler[i0 - 5], gunler[i0 + 3]], dtype="datetime64[D]"); f_ = np.array(["8-K", "8-K"], dtype=object); it_ = np.array(["2.02", "8.01"], dtype=object)
    ob = F1.oncesi_bayraklar(t_ok, f_, it_, gunler, i0); sb = F1.sonrasi_bayraklar(t_ok, f_, it_, gunler, i0, 20)
    if ob["once_8k_202"] != 1 or sb["sonra_haber"] != 1 or sb["sonra_202"] != 0:
        hata.append(f"18) bayraklar {ob} {sb}")
    t0b = np.array([gunler[i0]], dtype="datetime64[D]")
    if F1.oncesi_bayraklar(t0b, f_[:1], it_[:1], gunler, i0)["once_8k"] != 0 or F1.sonrasi_bayraklar(t0b, f_[:1], it_[:1], gunler, i0, 20)["sonra_202"] != 0:
        hata.append("18) t0 günü başvurusu ÖNCESİ ya da SONRASI sayıldı")
    _eski = F1.ESIKLER["oncesi"]; F1.ESIKLER["oncesi"] = (-20, 0)                               # kural bozulursa kapı durdurmalı
    try:
        F1.oncesi_bayraklar(t0b, f_[:1], it_[:1], gunler, i0); hata.append("18) sızıntı kapısı t0 başvurusunu geçirdi")
    except RuntimeError:
        pass
    finally:
        F1.ESIKLER["oncesi"] = _eski
    # 18b) G7 eşleri: aynı gün, aynı likidite üçlüsü, |vd farkı| <= 1, sektör, ±h içinde olayı olan eş yok
    Pg = pd.DataFrame({"tarih": pd.to_datetime(["2018-05-01"] * 6), "sembol": list("ABCDEF"), "i": [100] * 6, "sektor": ["s1", "s1", "s1", "s2", "s1", "s1"],
                       "lt": np.array([1, 1, 1, 1, 2, 1], np.int8), "vd": np.array([5, 6, 4, 5, 5, 8], np.int8), "likit": True, "donem60": "KESIF"})
    Og = pd.DataFrame({"sembol": ["A", "C", "B"], "tarih": pd.to_datetime(["2018-05-01", "2018-03-01", "2018-03-01"]), "i": [100, 60, 60], "ufuk": "Y60", "donem": ["KESIF", "KESIF", "IC_DOGRULAMA"],
                       "bitis": pd.to_datetime(["2018-07-30", "2018-05-25", "2022-05-25"])})    # B'nin olayı dönem sonrasında biter: eşlemeyi engellemez
    Gg = F1.g7_esleri(Pg, Og, "Y60", "KESIF", np.random.default_rng(1))
    if sorted(Gg.sembol) != ["B"]:
        hata.append(f"18b) G7 eşleri {sorted(Gg.sembol)} (beklenen ['B'])")
    # 18c) A3 bileşim: aynı günde çok olay olsa da olay başına tek satır (eş tablosu olay anahtarıyla birleşir)
    gun3 = pd.bdate_range("2017-01-02", periods=300); n3 = 35; sem3 = [f"E{k:02d}" for k in range(n3)] + [f"Q{k:02d}" for k in range(10)]
    P3 = pd.DataFrame({"tarih": gun3[100], "sembol": sem3, "i": 100, "sektor": "s1", "lt": np.int8(1), "vd": np.int8(5), "likit": True,
                       "donem60": "KESIF", "donem120": "KESIF", "donem250": "KESIF"})
    O3 = pd.DataFrame({"sembol": sem3[:n3], "tarih": gun3[100], "i": 100, "ufuk": "Y60", "donem": "KESIF", "bitis": gun3[160]})
    V3 = {s_: pd.DataFrame({"Close": 1.0}, index=gun3) for s_ in sem3}; cm3 = {s_: k + 1 for k, s_ in enumerate(sem3)}
    J3 = {str(k + 1): {"date": [str(gun3[95].date()), str(gun3[103].date())], "form": ["8-K", "8-K"], "items": ["2.02", "8.01"]} for k in range(len(sem3))}
    B3_ = F1.bilesim(P3, V3, O3, J3, cm3, "KESIF")
    if not len(B3_) or (B3_.n_olay != n3).any() or not np.allclose(B3_[B3_.olcu == "once_8k_202"].pay_g1, 1.0):
        hata.append(f"18c) bileşim olay sayısı {B3_.n_olay.unique().tolist() if len(B3_) else 'boş'} (beklenen {n3})")
    # 19) dönem kapısı: BAĞIMSIZ kapalı; dönem dışı satır ve dönem sonunu aşan etiket penceresi durdurur
    os.environ.pop("K56_BAGIMSIZ_AC", None)
    for g, bek in ((("BAGIMSIZ",), True), (("KESIF", pd.DataFrame({"tarih": ["2022-01-03"]})), True),
                   (("IC_DOGRULAMA", pd.DataFrame({"tarih": ["2023-06-01"], "bitis120": ["2024-01-10"]}), 120), True),
                   (("IC_DOGRULAMA", pd.DataFrame({"tarih": ["2023-01-03"], "bitis60": ["2023-04-01"]}), 60), False), (("KESIF",), False)):
        try:
            O.donem_kapisi(*g); dur = False
        except O.DonemKapali:
            dur = True
        if dur != bek:
            hata.append(f"19) donem_kapisi{tuple(type(x).__name__ if not isinstance(x, str) else x for x in g)} durdu={dur}")
    os.environ["K56_BAGIMSIZ_AC"] = "1"
    try:
        O.donem_kapisi("BAGIMSIZ", kilit_klasoru=tempfile.mkdtemp()); hata.append("19) kilit dosyası olmadan BAĞIMSIZ açıldı")
    except O.DonemKapali:
        pass
    finally:
        os.environ.pop("K56_BAGIMSIZ_AC", None)
    # 20) Ö2 (v1.2-a): havuz kuralları, sonradan yeniden kullanılan sembol seçilmez; CIK bağlama ad / sembol + tarih; seri denetimi
    T = pd.DataFrame({"ticker": ["ABC", "ABC", "XYZ", "QQQ", "PR-A", "OLD"], "exchange": ["NYSE", "NASDAQ", "NASDAQ", "NASDAQ", "NYSE", "PINK"], "assetType": ["Stock"] * 6,
                      "startDate": pd.to_datetime(["2012-01-03", "2019-05-01", "2014-01-02", "2010-01-04", "2010-01-04", "2010-01-04"]),
                      "endDate": pd.to_datetime(["2018-03-01", "2026-10-29", "2019-07-10", "2017-02-01", "2018-01-02", "2018-01-02"])})
    Hv = BE.o2_havuz(T, {"QQQ"}).set_index("sembol")
    if sorted(Hv.index) != ["ABC", "QQQ", "XYZ"] or not Hv.sonraki_kullanim["ABC"] or Hv.sonraki_kullanim["XYZ"] or not Hv.haric["QQQ"]:
        hata.append(f"20) Ö2 havuz: {Hv.to_dict('index')}")
    N25 = pd.DataFrame({"cik": [11, 22, 33], "ad": ["Xyz Holdings, Inc.", "Other Corp", "Zeta Co"], "sembol": [None, None, "ZZZ"], "nse_tarih": pd.to_datetime(["2019-06-28", "2019-06-28", "2017-01-20"])})
    if BE.cik_bagla("XYZ", "XYZ HOLDINGS INC", pd.Timestamp("2019-07-10"), N25) != (11, "ad + tarih") or BE.cik_bagla("ZZZ", "Başka Ad", pd.Timestamp("2017-02-01"), N25) != (33, "sembol + tarih") \
            or BE.cik_bagla("XYZ", "XYZ HOLDINGS INC", pd.Timestamp("2020-07-10"), N25)[0] is not None or BE.ad_norm("The Xyz Co., Inc.") != "XYZ":
        hata.append("20) CIK bağlama / ad normalizasyonu")
    with tempfile.TemporaryDirectory() as td:
        y = os.path.join(td, "x.csv"); pd.DataFrame({"date": pd.bdate_range("2017-01-02", "2019-07-03").strftime("%Y-%m-%dT00:00:00.000Z")}).to_csv(y, index=False)
        if BE.seri_denetimi(y, pd.Timestamp("2019-07-10"))[0] != "TAMAM" or BE.seri_denetimi(y, pd.Timestamp("2021-07-10"))[0] != "TIINGO SERİSİ UYUŞMADI" or BE.seri_denetimi(y + "z", pd.Timestamp("2019-07-10"))[0] != "İNMEDİ":
            hata.append("20) seri denetimi")
    # 21) evren v2 yardımcıları: SIC bölümü (K34 tablosu), Tiingo okuma (düzeltilmiş OHLCV), K54 satırının K55 tutarlılık denetiminden geçmesi, olay karşılaştırması
    from K56 import evren_v2 as E2
    from K55.evren import k54_tutarlilik
    if E2.sic_bolum(2834) != "İmalat" or E2.sic_bolum(6021) != "Finans" or E2.sic_bolum(None) != "bilinmiyor" or E2.sic_bolum("x") != "bilinmiyor":
        hata.append("21) SIC bölümü")
    with tempfile.TemporaryDirectory() as td:
        g = pd.bdate_range("2017-01-02", periods=400); y = os.path.join(td, "ABC.csv")
        pd.DataFrame({"date": g.strftime("%Y-%m-%dT00:00:00.000Z"), "open": 10, "high": 11, "low": 9, "close": 10, "volume": 1000, "adjOpen": 5.0, "adjHigh": 5.5, "adjLow": 4.5,
                      "adjClose": 5.0, "adjVolume": 2000}).to_csv(y, index=False)
        d = E2.yeni_seri_oku(y, pd.Timestamp("2026-08-31"))
        if d is None or list(d.columns) != ["Open", "High", "Low", "Close", "Volume"] or float(d.Close.iloc[0]) != 5.0 or len(d) != 400:
            hata.append("21) Tiingo okuma")
    SDt = pd.DataFrame([{"sembol": "AAA", "sinif": 2, "alt": "", "cikis_islemi": "y_d100", "kesim_tarihi": "", "erken_bitti": True},
                        {"sembol": "BBB", "sinif": 3, "alt": "", "cikis_islemi": "y_d0", "kesim_tarihi": "", "erken_bitti": True},
                        {"sembol": "CCC", "sinif": 5, "alt": "", "cikis_islemi": "y", "kesim_tarihi": "", "erken_bitti": True}])
    if not k54_tutarlilik(SDt)[0].tutarli.all():
        hata.append(f"21) K54 satırları K55 tutarlılık denetiminden geçmedi: {k54_tutarlilik(SDt)[1].to_dict('records')}")
    Oa = pd.DataFrame({"sembol": ["X", "Y"], "donem": "KESIF", "ufuk": "Y60"}); Ob = pd.DataFrame({"sembol": ["X", "Y", "N1"], "donem": "KESIF", "ufuk": "Y60"})
    OKt = E2.olay_karsilastir(Oa, Ob, pd.DataFrame({"sembol": ["X", "Y", "N1"], "kaynak": ["V_ABD", "V_ABD", "K56_O2"]}))
    if OKt[["k55", "v2", "v2_yeni_sirket", "fark"]].iloc[0].tolist() != [2, 3, 1, 1]:
        hata.append(f"21) olay karşılaştırması {OKt.to_dict('records')}")
    # 22) indirme_sonrasi: inen ve inmeyen sembol karışıkken çökmez (NaT); inmeyen İNMEDİ, Ö1 CIK'i korunur; adi hisse süzgeci
    if not (BE.adi_hisse_degil("RBAC-U") and BE.adi_hisse_degil("ZEV-WS") and BE.adi_hisse_degil("GRNAW") and not BE.adi_hisse_degil("GOOGL") and not BE.adi_hisse_degil("AAPL")):
        hata.append("22) adi hisse süzgeci")
    with tempfile.TemporaryDirectory() as td:
        g = pd.bdate_range("2017-01-02", periods=400)
        pd.DataFrame({"date": g.strftime("%Y-%m-%dT00:00:00.000Z"), "adjOpen": 5.0, "adjHigh": 5.5, "adjLow": 4.5, "adjClose": 5.0, "adjVolume": 2000}).to_csv(os.path.join(td, "AAA.csv"), index=False)
        AD = pd.DataFrame({"cik": [1339469, np.nan], "sembol": ["AAA", "BBB"], "kaynak": ["Ö1 (K34 kalan)", "Ö2 (Tiingo KEŞİF bitişi)"], "baslangic": ["2017-01-02", "2015-01-02"],
                           "bitis": [str(g[-1].date()), "2019-06-28"], "borsa": "NASDAQ"})
        Tt = pd.DataFrame({"ticker": ["AAA", "BBB"], "exchange": "NASDAQ", "assetType": "Stock", "priceCurrency": "USD", "startDate": pd.to_datetime(["2017-01-02", "2015-01-02"]),
                           "endDate": pd.to_datetime([g[-1], "2019-06-28"])})
        try:
            Yt = E2.indirme_sonrasi(O.K56Ayar(), None, AD, td, pd.DataFrame(columns=["cik", "ad", "sembol", "nse_tarih"]), Tt, os.path.join(td, "yok.json"))
            if Yt.set_index("sembol").seri_durum.to_dict() != {"AAA": "TAMAM", "BBB": "İNMEDİ"} or Yt.set_index("sembol").cik["AAA"] != 1339469:
                hata.append(f"22) indirme_sonrasi {Yt[['sembol', 'seri_durum', 'cik']].to_dict('records')}")
        except Exception as ex:
            hata.append(f"22) indirme_sonrasi çöktü: {type(ex).__name__}: {ex}")
    # 23) v1.3 ayrışma: ortak bootstrap = boot_kume; kimlik E1 − E2 = −Cov(L, f) / ort L; satır kararı; spek çoğunluğu
    from K56 import ayrisma as AY
    from K55.istatistik import boot_kume
    rr = np.random.default_rng(3); xs = rr.normal(size=300); ks = rr.integers(0, 40, 300)
    nk, lo, hi = boot_kume(xs, ks, 500, np.random.default_rng(9)); inv, sec = AY.kume_cekilis(ks, 500, np.random.default_rng(9)); nn, bs = AY.oran_boot(xs, np.ones(300), inv, sec)
    if not (abs(nk - nn) < 1e-12 and abs(np.percentile(bs, 2.5) - lo) < 1e-12 and abs(np.percentile(bs, 97.5) - hi) < 1e-12):
        hata.append("23) ortak bootstrap boot_kume ile aynı değil")
    nz = 400; zz = rr.normal(size=nz); gun = np.repeat(np.arange(40), 10); vd = np.tile(np.arange(2), 200)
    gl = [np.arange(k, k + L) for k, L in zip(range(0, 380, 20), rr.integers(1, 15, 19))]; pl = [np.arange(1, len(g) + 1) for g in gl]; Ls = np.array([len(g) for g in gl])
    out23 = AY.satir_olc(zz, gun, vd, gl, pl, Ls, -1.0, {"ay": np.arange(19) % 7, "sembol_yil": np.arange(19) % 5}, np.arange(19), "test", B=200)
    if out23.get("karar_veri") != "VERİ YETERSİZ":
        hata.append("23) 19 olayda VERİ YETERSİZ beklenirdi")
    nz = 2000; zz = rr.normal(size=nz); gun = np.repeat(np.arange(100), 20); vd = np.tile(np.arange(2), 1000)
    gl = [np.arange(k, k + L) for k, L in zip(range(0, 1980, 30), rr.integers(1, 11, 66))]; pl = [np.arange(1, len(g) + 1) for g in gl]; Ls = np.array([len(g) for g in gl])
    out23 = AY.satir_olc(zz, gun, vd, gl, pl, Ls, -1.0, {"ay": np.arange(66) % 9, "sembol_yil": np.arange(66) % 11}, np.arange(66), "test", B=200)
    if not (abs(out23.get("kimlik_fark", 1)) < 1e-9 and abs(out23["iii_cekilis_ort"] - out23["E1"]) < 0.05):
        hata.append(f"23) kimlik / çekiliş: {out23.get('kimlik_fark')}, {out23.get('iii_cekilis_ort')} vs {out23.get('E1')}")
    r_ = {"G": 0.3, "G_ay_alt": 0.2, "G_ay_ust": 0.4, "G_sembol_yil_alt": 0.1, "G_sembol_yil_ust": 0.5, "G_blok60_alt": 0.15, "G_blok60_ust": 0.45, "E1": -0.3, "E2": 0.0,
          "E2_ay_alt": -0.05, "E2_ay_ust": 0.05}
    if AY.satir_karari(r_, "MEKANIK_ACIKLAR") != "AĞIRLIK ETKİSİ + MEKANİK (yapay veri üretiyor)" or AY.satir_karari({**r_, "G_ay_alt": -0.1}, "MEKANIK_ACIKLAR") != "AYRIŞMA YOK" \
            or AY.satir_karari(r_, "MEKANIK_IZ_YOK") != "AĞIRLIK ETKİSİ (gerçek veriye özgü, öngörü değil)" or AY.satir_karari({**r_, "E2": -0.2, "E2_ay_alt": -0.25, "E2_ay_ust": -0.15}, "MEKANIK_IZ_YOK") != "AÇIKLANMADI" \
            or AY.satir_karari({**r_, "G_blok60_alt": -0.01}, "MEKANIK_ACIKLAR") != "AYRIŞMA YOK" \
            or AY.spek_cogunluk(["MEKANIK_ACIKLAR"] * 3 + ["MEKANIK_IZ_YOK"]) != "MEKANIK_ACIKLAR" or AY.spek_cogunluk(["MEKANIK_ACIKLAR"] * 2 + ["MEKANIK_IZ_YOK"] * 2) != "BELİRSİZ (yapay)":
        hata.append("23) ayrışma satır kararı / spek çoğunluğu")
    # 24) v1.3 bir kez kuralı ve açık kayıt kapısı; BAĞIMSIZ'da sinir reddi; BAGIMSIZ_B sınırları; kilitte git etiketi zorunlu
    with tempfile.TemporaryDirectory() as td:
        kim = {"kimlik": "K56-BAG-test", "commit": "abc"}; O.acilis_baslat("K55_125_B", kim, td)
        for f_, bek in ((lambda: O.acilis_baslat("K55_125_B", kim, td), "BAŞLADI"),):
            try:
                f_(); hata.append("24) bitmemiş kayıt varken ikinci açılış")
            except O.DonemKapali:
                pass
        os.environ["K56_BAGIMSIZ_KIMLIK"] = "K56-BAG-test"; O.acik_kayit_dogrula(td); os.environ["K56_BAGIMSIZ_KIMLIK"] = "baska"
        try:
            O.acik_kayit_dogrula(td); hata.append("24) yanlış kimlikle açık kayıt geçti")
        except O.DonemKapali:
            pass
        os.environ.pop("K56_BAGIMSIZ_KIMLIK", None); O.acilis_bitir("K55_125_B", kim, "ÇÖKTÜ", td, notu="test")
        try:
            O.acilis_baslat("K55_125_B", {"kimlik": "K56-BAG-2", "commit": "abc"}, td); hata.append("24) çöküş sonrası gerekçesiz yeniden deneme")
        except O.DonemKapali:
            pass
        os.environ["K56_BAGIMSIZ_YENIDEN"] = "test gerekçesi"; O.acilis_baslat("K55_125_B", {"kimlik": "K56-BAG-2", "commit": "abc"}, td); os.environ.pop("K56_BAGIMSIZ_YENIDEN", None)
        O.acilis_bitir("K55_125_B", {"kimlik": "K56-BAG-2", "commit": "abc"}, "TAMAMLANDI", td)
        try:
            os.environ["K56_BAGIMSIZ_YENIDEN"] = "x"; O.acilis_baslat("K55_125_B", {"kimlik": "K56-BAG-3", "commit": "abc"}, td); hata.append("24) TAMAMLANDI sonrası yeniden koşu")
        except O.DonemKapali:
            pass
        finally:
            os.environ.pop("K56_BAGIMSIZ_YENIDEN", None)
    try:
        F1.calistir(O.K56Ayar(), O.KaynakKaydi(), "BAGIMSIZ", None, None, sinir=1); hata.append("24) BAĞIMSIZ'da sinir kabul edildi")
    except ValueError:
        pass
    try:
        O.git_kilit_dogrula({"etiket": "", "commit_tam": ""}); hata.append("24) etiketsiz kilit geçti")
    except O.DonemKapali:
        pass
    from K56 import surucu as SU2
    Pb = pd.DataFrame({"tarih": pd.to_datetime(["2024-01-05", "2024-03-01", "2026-05-01", "2026-06-10"]), "donem60": ["EMBARGO", "BAGIMSIZ", "PURGE", "DISI"],
                       "donem120": "X", "donem250": "X", "bitis60": pd.to_datetime(["2024-04-01", "2024-05-24", "2026-07-28", "2026-09-04"]), "bitis120": pd.NaT, "bitis250": pd.NaT})
    Ob = pd.DataFrame({"tarih": pd.to_datetime(["2026-05-01"]), "bitis": pd.to_datetime(["2026-07-28"]), "donem": ["PURGE"]})
    SU2.bagimsiz_b_etiketle({"P": Pb, "O": Ob})
    if Pb.donem60.tolist() != ["EMBARGO", "BAGIMSIZ_B", "BAGIMSIZ_B", "DISI"] or Ob.donem.tolist() != ["BAGIMSIZ_B"]:
        hata.append(f"24) BAGIMSIZ_B etiketi {Pb.donem60.tolist()} {Ob.donem.tolist()}")
    # 25) sızıntı karşılaştırması: aynı tablo birebir, tek hücre farkı yakalanır
    from K56 import sizinti_denetimi as SZ
    Sx = pd.DataFrame({"hucre": ["a", "b"], "varyant": ["a|1", "b|1"], "ufuk": "Y60", "i_d": [0.1, np.nan], "sinif_a1": ["MEKANİK", "X"], "sure_sn": [1.0, 2.0]})
    _, z1 = SZ.karsilastir({"S": Sx}, {"S": Sx.assign(sure_sn=[5.0, 6.0])}); Sy = Sx.copy(); Sy.loc[0, "i_d"] = 0.1000001
    F25, z2 = SZ.karsilastir({"S": Sx}, {"S": Sy})
    if not z1["birebir"]["S"] or z2["birebir"]["S"] or len(F25) != 1:
        hata.append(f"25) sızıntı karşılaştırması {z1} {z2}")
    # 26) EVREN2 v1.3: ad normalizasyonu, sonek, paylaşılan sembol, adi hisse adı, kimlik
    if BE.ad_norm("Co-Diagnostics, Inc.") != "CO DIAGNOSTICS" or BE.ad_norm("JACKSONVILLE BANCORP INC /FL/") != "JACKSONVILLE BANCORP" or BE.ad_norm("The Xyz Co., Inc.") != "XYZ":
        hata.append("26) ad normalizasyonu")
    if BE.sonek_sinifi("CBSHP", "NASDAQ")[0] != "DIŞI" or BE.sonek_sinifi("DXBCL", "NYSE")[0] != "DIŞI" or BE.sonek_sinifi("ABCDF", "NASDAQ")[0] != "İŞARET" or BE.sonek_sinifi("CHMA", "NASDAQ")[0] != "":
        hata.append("26) sonek kuralı")
    Tp = pd.DataFrame({"ticker": ["DNB", "DNB"], "startDate": pd.to_datetime(["2010-01-04", "2020-07-01"]), "endDate": pd.to_datetime(["2019-02-08", "2026-10-29"])})
    Tq = pd.DataFrame({"ticker": ["GWGHQ", "GWGHQ"], "exchange": ["NASDAQ", "EXPM"], "startDate": pd.to_datetime(["2015-01-02", "2022-05-03"]), "endDate": pd.to_datetime(["2022-04-25", "2023-08-25"])})
    if BE.cakisan_satir(Tq, "GWGHQ", "2015-01-02", "2022-04-25") != 0 or BE.devam_satiri(Tq, "GWGHQ", "2015-01-02", "2022-04-25") is None \
            or "OTC devamı" not in BE.indirme_oncesi_suzgec(Tq, "GWGHQ", "NASDAQ", "2015-01-02", "2022-04-25")[1]:
        hata.append("26) OTC devamı istisnası")
    if BE.cakisan_satir(Tp, "YOKSEMBOL", "2010-01-04", "2019-02-08") != 0 or BE.devam_satiri(Tp, "YOKSEMBOL", "2010-01-04", "2019-02-08") is not None:
        hata.append("26) boş Tiingo satırında paylaşılan sembol")
    if BE.cakisan_satir(Tp, "DNB", "2010-01-04", "2019-02-08") != 1 or BE.beklenen_gun("2010-01-01", "2016-01-29") >= 320:
        hata.append("26) paylaşılan sembol / beklenen gün")
    if E2.adi_hisse_ad("XYZ Corp 6.5% Senior Notes", None)[0] != "DIŞI" or E2.adi_hisse_ad("Kinder Morgan Energy Partners LP Common Units", None)[0] != "İŞARET" \
            or E2.adi_hisse_ad("Foo American Depositary Shares", None)[0] != "İŞARET" or E2.adi_hisse_ad("Chiasma Inc", None)[0] != "":
        hata.append("26) adi hisse adı kuralı")
    if E2.kimlik_ad("Chiasma Inc", {"name": "CHIASMA, INC", "formerNames": []})[0] != "UYUMLU" or E2.kimlik_ad("Totally Different LLC", {"name": "CHIASMA, INC", "formerNames": []})[0] != "UYUMSUZ":
        hata.append("26) kimlik kuralı")
    # 15) K51-K55 dosyaları değişmedi
    git1 = subprocess.run(["git", "status", "--porcelain", "--", *KORUNAN], capture_output=True, text=True).stdout
    if git1 != git0 or git1.strip():
        hata.append(f"15) korunan dosyalarda değişiklik: {git1[:300]}")
    return hata


if __name__ == "__main__":
    h = testler()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_k56: 28/28 OK")
