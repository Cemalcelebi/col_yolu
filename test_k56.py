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
        if f.endswith(".py") and "@gmail" in open(os.path.join(O.KOK, "K56", f), encoding="utf-8").read():
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
    if EE.on_sinif(r)[0] != "YANLIŞ BULGU":
        hata.append("9) M01 mekanik -> YANLIŞ BULGU kuralı")
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
    # 10) olay sayıları ve ad normalizasyonu
    T = pd.DataFrame({"form": ["8-K", "8-K", "S-3", "424B2", "SC 13D/A", "25-NSE"], "tarih": pd.to_datetime(["2017-01-01"] * 6), "madde": ["2.02,9.01", "1.03", "", "", "", ""]})
    s = KOL.olay_sayilari(T)
    if not (s["8K_iflas"] == 1 and s["ihrac_izahname"] == 1 and s["borc_notu_424B2"] == 1 and s["sahiplik_13D"] == 1 and s["kot_cikis"] == 1):
        hata.append(f"10) olay sayıları: {s}")
    if KOL._ad_norm("Moleculin Biotech, Inc.") != KOL._ad_norm("MOLECULIN BIOTECH INC") or KOL._ad_norm("Inc.") != "":
        hata.append("10) ad normalizasyonu")
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
    if not (len(MR.riskler()) >= 10 and len(MR.uygulama_sirasi()) >= 8 and MR.uygulama_sirasi().sira.is_monotonic_increasing):
        hata.append("14) risk / sıra tabloları")
    if MR.KAYNAKLAR and len({k["kimlik"] for k in MR.KAYNAKLAR}) != len(MR.KAYNAKLAR):
        hata.append("14) yinelenen kaynak kimliği")
    # 15) K51-K55 dosyaları değişmedi
    git1 = subprocess.run(["git", "status", "--porcelain", "--", *KORUNAN], capture_output=True, text=True).stdout
    if git1 != git0 or git1.strip():
        hata.append(f"15) korunan dosyalarda değişiklik: {git1[:300]}")
    return hata


if __name__ == "__main__":
    h = testler()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_k56: 15/15 OK")
