"""K60_veri testleri (ağ gerekmez; yalnız SENTETİK veri ve sahte indirici; gerçek önbelleklere dokunmaz). Çalıştırma: python test_k60_veri.py

1) çakışma kapısı  2) istek listesi (dönem aralıkları, birimler, yalnız yıllık nakit akış kalemleri, eski önbellekte olan indirilmez, sayılar)
3) kimlik kuralı: K60_SEC_UA yoksa indir_sec ÇALIŞMAZ (işlev ve komut satırı; tek istek atılmaz)  4) SEC indirme: kaldığı yerden sürme
(hata, 404 işareti, yarım dosya, kayıp manifest, bozuk dosya), 403'te durma, geçersiz yanıt  5) hız sınırı: saniyede en çok 8 istek (sahte saatle
tam liste; gerçek saatle 4 iş parçacığı), üst sınır aşılamaz  6) manifest sha256 (dosya özeti, klasör özeti, kurcalanan / eksik / fazla dosya)
7) e-posta / kimlik satırı sızıntısı yok (istek başlığına gider; günlük, durum, manifest, raporlarda yok; hata iletisi maskelenir)
8) Yahoo indirme: uç ve kimlik K57-B ile aynı, 2010 başlangıcı, olaylar saklanır, kaldığı yerden, 404 işareti, engelde durma, K59 klasörüne yazmaz
9) okuyucu + uygun evren: K59 okuyucusuyla aynı ham kapanış / bölünme çarpanı; fiyat, likidite, geçmiş, tür, bayat seri, ters bölünme;
bağımsız panel hesabıyla aynı ay sayıları; GELECEĞE BAKMA YOK  10) SEC denetimi: şirket sayıları, 'filed' alanı, dizin sayımı
11) plan / denetim / özet raporları (sentetik klasörlerde; yedek kural metni)  12) kodda ve çıktılarda e-posta / anahtar yok.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import threading
import time

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K60_veri as K  # noqa: E402

K57 = K.K57
# Sahte kimlik satırı çalışma anında kurulur (kaynak kodda e-posta biçimli dize olmasın diye)
SAHTE_UA = "K60 Test Arastirma " + "ornek.kisi" + "@" + "example" + ".org"
SAHTE_PARCA = ("ornek.kisi", "example" + ".org")


class SahteSaat:
    """Sahte saat: uyu() gerçek beklemez, saati ilerletir."""

    def __init__(self):
        self.t = 0.0; self._k = threading.Lock()

    def zaman(self) -> float:
        return self.t

    def uyu(self, s: float) -> None:
        with self._k:
            self.t += max(0.0, float(s))


class SahteSec:
    """Sahte SEC: her çağrıyı kaydeder; davranis(url) -> (kod, gövde) ya da istisna. Varsayılan: 3 şirketli geçerli çerçeve."""

    def __init__(self, davranis=None):
        self.cagri, self.an, self.baslik, self._k, self.davranis = [], [], [], threading.Lock(), davranis

    def __call__(self, url, basliklar, zaman_asimi):
        with self._k:
            self.cagri.append(url); self.an.append(time.monotonic()); self.baslik.append(dict(basliklar))
        if self.davranis is not None:
            r = self.davranis(url)
            if r is not None:
                return r
        return 200, cerceve(url)


def cerceve(url: str, n: int = 3, filed: bool = False) -> bytes:
    """Sentetik frames yanıtı (gerçek şema: accn, cik, entityName, loc, [start], end, val)."""
    m = re.search(r"/frames/([\w-]+)/(\w+)/(\w+)/(CY\w+)\.json$", url)
    tax, etiket, birim, donem = m.groups()
    veri = []
    for i in range(n):
        d = {"accn": f"0000000{i}-20-000001", "cik": 1000 + i, "entityName": f"SIRKET {i}", "loc": "US-NY", "end": "2015-03-31", "val": 100 + i}
        if not donem.endswith("I"):
            d["start"] = "2015-01-01"
        if filed:
            d["filed"] = "2015-05-01"
        veri.append(d)
    veri.append(dict(veri[0], val=7))   # aynı CIK ikinci satır: ayrı şirket sayısı değişmemeli
    return json.dumps({"taxonomy": tax, "tag": etiket, "ccp": donem, "uom": birim, "pts": len(veri), "data": veri}).encode()


def yahoo_json(idx, kapanis, hacim, tur="EQUITY", bolunme=None, temettu=None, duz=None) -> bytes:
    """Sentetik Yahoo chart yanıtı. bolunme: [(tarih, pay, payda)], temettu: [(tarih, tutar)]."""
    def ts(d):
        return int((pd.Timestamp(d) + pd.Timedelta(hours=14, minutes=30)).tz_localize("UTC").timestamp())
    c = [float(x) for x in kapanis]; olay = {}
    if bolunme:
        olay["splits"] = {str(ts(d)): {"date": ts(d), "numerator": p, "denominator": q, "splitRatio": f"{p}:{q}"} for d, p, q in bolunme}
    if temettu:
        olay["dividends"] = {str(ts(d)): {"amount": a, "date": ts(d)} for d, a in temettu}
    res = {"meta": {"currency": "USD", "symbol": "X", "instrumentType": tur, "exchangeTimezoneName": "America/New_York", "firstTradeDate": ts(idx[0])},
           "timestamp": [ts(d) for d in idx],
           "indicators": {"quote": [{"open": c, "high": [x * 1.01 for x in c], "low": [x * 0.99 for x in c], "close": c, "volume": [float(v) for v in hacim]}],
                          "adjclose": [{"adjclose": [float(x) for x in (duz if duz is not None else c)]}]}}
    if olay:
        res["events"] = olay
    return json.dumps({"chart": {"result": [res], "error": None}}).encode()


def sentetik_evren():
    """Yedi hisse: IYI (uygun), UCUZ (fiyat < 2), SIG (likit değil), YENI (geçmişi kısa), TERS (ters bölünmeden önce o günkü fiyat < 2),
    FON (ETF), ESKI (2011 ortasında biten seri)."""
    idx = pd.bdate_range("2010-01-04", "2012-12-31"); n = len(idx); x = np.linspace(0, 12, n)
    S = {"IYI": (idx, 50 + 5 * np.sin(x), np.full(n, 1.0e6), "EQUITY", None),
         "UCUZ": (idx, 1.5 + 0.2 * np.sin(x), np.full(n, 5.0e6), "EQUITY", None),
         "SIG": (idx, 30 + 2 * np.sin(x), np.full(n, 100.0), "EQUITY", None),
         "YENI": (idx[idx >= "2012-03-01"], (20 + np.sin(x))[idx >= "2012-03-01"], np.full(int((idx >= "2012-03-01").sum()), 1.0e6), "EQUITY", None),
         "TERS": (idx, 15 + np.sin(x), np.full(n, 1.0e6), "EQUITY", [("2012-06-01", 1, 10)]),
         "FON": (idx, 100 + np.sin(x), np.full(n, 1.0e7), "ETF", None),
         "ESKI": (idx[idx <= "2011-06-30"], (40 + np.sin(x))[idx <= "2011-06-30"], np.full(int((idx <= "2011-06-30").sum()), 1.0e6), "EQUITY", None)}
    return idx, S


def evren_yaz(klasor: str, S: dict, boz_sonra=None) -> None:
    """Sentetik fiyat önbelleği. boz_sonra verilirse o günden SONRAKİ fiyat ve hacim bozulur (geleceğe bakma testi)."""
    os.makedirs(klasor, exist_ok=True)
    for s, (idx, c, v, tur, bol) in S.items():
        c = np.array(c, float); v = np.array(v, float)
        if boz_sonra is not None:
            m = idx > pd.Timestamp(boz_sonra); c[m] *= 0.01; v[m] = 3.0
        with open(os.path.join(klasor, s + ".json"), "wb") as f:
            f.write(yahoo_json(idx, c, v, tur, bol, [(idx[5], 0.1)] if s == "IYI" else None))
    pd.DataFrame({"sembol": list(S), "kaynak": "test"}).to_csv(os.path.join(klasor, "_evren.csv"), index=False)


def referans_ay(idx, S: dict) -> pd.DataFrame:
    """Uygun evren ay sayıları, bağımsız panel hesabı (K59 k59_panel mantığı: geçmiş, o günkü fiyat, medyan işlem değeri, 5 gün taşıma)."""
    U = K.K60V_ESIK["uygunluk"]; me = pd.Series(idx, index=idx).groupby(idx.to_period("M")).last().to_numpy()
    say = pd.Series(0, index=pd.DatetimeIndex(me))
    for s, (ix, c, v, tur, bol) in S.items():
        if tur not in U["tur"]:
            continue
        c = pd.Series(np.array(c, float), index=ix); v = pd.Series(np.array(v, float), index=ix)
        carp = pd.Series(1.0, index=ix)
        for d, p, q in bol or []:
            carp[ix < pd.Timestamp(d)] *= p / q
        ok = ((pd.Series(np.arange(1, len(ix) + 1), index=ix) >= U["gecmis_gun"]) & (c * carp >= U["fiyat_min"])
              & ((c * v).rolling(U["likit_gun"], min_periods=U["likit_min_gun"]).median() >= U["likit_min"]))
        ok = ok.astype(float).reindex(idx).ffill(limit=U["ileri_tasima"]).fillna(0.0)
        say += ok.reindex(pd.DatetimeIndex(me)).to_numpy().astype(int)
    return say


class Yakala(logging.Handler):
    def __init__(self):
        super().__init__(logging.DEBUG); self.satir = []

    def emit(self, record):
        self.satir.append(record.getMessage())


def testler() -> list:
    hata = []
    bos_uyu = lambda s: None  # noqa: E731

    def sahte() -> dict:
        """Sahte saat çifti (uyu saati ilerletir): hız sınırı ve geri çekilme beklemeleri gerçek zaman harcamaz."""
        ss = SahteSaat()
        return {"uyu": ss.uyu, "zaman": ss.zaman}
    eski_ua = os.environ.pop(K.K60V_UA_DEGISKEN, None)
    yedek_yol = dict(K.K60V_YOL); yedek_yahoo = dict(K.K60V_ESIK["yahoo"])
    try:
        # 1) çakışma kapısı
        src = open(os.path.join(KOK, "K60_veri.py"), encoding="utf-8").read().replace("from __future__ import annotations\n", "")
        g = {"__name__": "kapi_test", "k60v_plan": object(), "_CK_KAYIT": {"k60v_plan": "BASKA.py"}}
        try:
            exec(compile(src, "K60_veri.py", "exec"), g)
            hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
        except RuntimeError as ex:
            if "EZDİ" not in str(ex):
                hata.append(f"1) beklenmeyen hata: {ex}")
        g2 = {"__name__": "kapi_test2"}
        try:
            exec(compile(src, "K60_veri.py", "exec"), g2); exec(compile(src, "K60_veri.py", "exec"), g2)
        except Exception as ex:
            hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
        if "_CK_ONCE_K60V" not in src or "_cakisma_kontrol_k60v()" not in src:
            hata.append("1) çakışma kapısı adı _CK_ONCE_K60V değil")

        with tempfile.TemporaryDirectory() as td:
            bos = os.path.join(td, "bos_eski"); os.makedirs(bos)
            eski = os.path.join(td, "eski"); os.makedirs(eski)
            for t, d in K57.k57_sec_listesi():                      # K57 / K59 önbelleğinin sahtesi (206 dosya)
                with open(os.path.join(eski, f"us-gaap_{t}_{d}.json"), "w") as f:
                    f.write('{"data": []}')
            eski_ozet = {f: K.k60v_dosya_sha(os.path.join(eski, f)) for f in sorted(os.listdir(eski))}

            # 2) istek listesi
            L = pd.DataFrame(K.k60v_sec_listesi(True, bos)); Le = pd.DataFrame(K.k60v_sec_listesi(True, eski)); Ls = pd.DataFrame(K.k60v_sec_listesi(False, bos))
            if len(L) != 1916 or L.dosya.duplicated().any() or L.url.duplicated().any():
                hata.append(f"2) tam liste 1916 ayrı çerçeve değil: {len(L)}")
            if len(Ls) != 1916 - 191 or (Ls.grup == "EK").any():
                hata.append(f"2) EK'siz liste 1725 değil: {len(Ls)}")
            if int(Le.mevcut.notna().sum()) != 206 or int(Le.mevcut.isna().sum()) != 1710 or len(eski_ozet) != 206:
                hata.append(f"2) eski önbellekte olan 206 çerçeve atlanmadı: {int(Le.mevcut.notna().sum())}")
            gi = Le[Le.mevcut.isna()].groupby("grup").size().to_dict()
            if gi != {"A": 422, "B": 1029, "C": 68, "EK": 191}:
                hata.append(f"2) grup istek sayıları yanlış: {gi}")
            for t in list(K57.K57_ABD_GELIR) + ["NetIncomeLoss"]:
                d = set(Le[(Le.etiket == t) & Le.mevcut.isna()].donem)
                bek = {f"CY{y}Q{q}" for y in range(2009, 2020) for q in range(1, 5)} | {f"CY{y}" for y in range(2009, 2020)}
                if d != bek:
                    hata.append(f"2) {t}: inecek dönemler CY2009Q1..CY2019Q4 + CY2009..CY2019 değil")
            for t in K57.K57_ABD_ANLIK:
                d = set(Le[(Le.etiket == t) & Le.mevcut.isna()].donem)
                if d != {f"CY{y}Q{q}I" for y in range(2009, 2020) for q in range(1, 5)}:
                    hata.append(f"2) {t}: inecek dönemler CY2009Q1I..CY2019Q4I değil")
            dei = L[L.etiket == "EntityCommonStockSharesOutstanding"]
            if len(dei) != 70 or set(dei.tax) != {"dei"} or not dei.url.str.contains("/frames/dei/EntityCommonStockSharesOutstanding/shares/CY").all() \
                    or dei.donem.iloc[0] != "CY2009Q1I" or dei.donem.iloc[-1] != "CY2026Q2I":
                hata.append("2) dei pay sayısı çerçeveleri (shares, 2009Q1I..2026Q2I) yanlış")
            for t in ("NetCashProvidedByUsedInOperatingActivities", "PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsForRepurchaseOfCommonStock",
                      "ProceedsFromIssuanceOfCommonStock"):
                d = list(L[L.etiket == t].donem)
                if d != [f"CY{y}" for y in range(2009, 2026)]:
                    hata.append(f"2) {t}: yalnız yıllık CY2009..CY2025 değil")
            for t in ("Assets", "GrossProfit", "CostOfRevenue", "CostOfGoodsAndServicesSold", "OperatingIncomeLoss", "CashAndCashEquivalentsAtCarryingValue",
                      "LongTermDebt", "LongTermDebtNoncurrent", "AssetsCurrent", "LiabilitiesCurrent", "ResearchAndDevelopmentExpense",
                      "IncomeTaxExpenseBenefit", "DepreciationDepletionAndAmortization"):
                g_ = L[L.etiket == t]
                if not len(g_) or g_.donem.iloc[0] not in ("CY2009Q1", "CY2009Q1I") or not (set(g_.donem) & {"CY2026Q2", "CY2026Q2I"}):
                    hata.append(f"2) {t}: 2009Q1..2026Q2 aralığı yok")
                if not g_.url.str.contains(f"/frames/us-gaap/{t}/USD/CY").all():
                    hata.append(f"2) {t}: adres biçimi yanlış")
            if not L[L.birim == "shares"].url.str.contains("/shares/").all() or L.url.str.contains(" ").any() or not L.url.str.startswith("https://data.sec.gov/api/xbrl/frames/").all():
                hata.append("2) adreslerde birim / kök yanlış")
            Dz = K.k60v_dizin_listesi()
            if len(Dz) != 71 or Dz[0]["url"] != "https://www.sec.gov/Archives/edgar/full-index/2009/QTR1/master.gz" or Dz[-1]["donem"] != "2026Q3":
                hata.append("2) EDGAR dizin listesi yanlış")
            Pt = K.k60v_plan_tablo(True, False, eski, os.path.join(td, "yok"))
            if Pt["istek"] != 1710 or Pt["eski_onbellekte"] != 206 or Pt["kalan"] != 1710 or not (3.5 < Pt["sure_alt_dk"] < 3.9) or not (0.2 < Pt["mb"] / 1000 < 3):
                hata.append(f"2) plan sayıları yanlış: {Pt['istek']}, {Pt['sure_alt_dk']:.2f} dk, {Pt['mb']:.0f} MB")

            # 3) kimlik kuralı
            sf = os.path.join(td, "sec"); sahte_sec = SahteSec()
            for deger in (None, "", "   "):
                if deger is None:
                    os.environ.pop(K.K60V_UA_DEGISKEN, None)
                else:
                    os.environ[K.K60V_UA_DEGISKEN] = deger
                try:
                    K.k60v_sec_indir(getir=sahte_sec, klasor=sf, eski_klasor=bos, **sahte())
                    hata.append(f"3) K60_SEC_UA {deger!r} iken indir_sec çalıştı")
                except K.K60VKimlikYok:
                    pass
            if sahte_sec.cagri or os.path.exists(sf):
                hata.append("3) kimlik yokken istek atıldı / klasör açıldı")
            os.environ.pop(K.K60V_UA_DEGISKEN, None)
            ortam = {k: v for k, v in os.environ.items() if k != K.K60V_UA_DEGISKEN}
            ortam.update({"K60_SECFRAMES": os.path.join(td, "sec_cli"), "HTTPS_PROXY": "http://127.0.0.1:9", "https_proxy": "http://127.0.0.1:9"})
            r = subprocess.run([sys.executable, os.path.join(KOK, "K60_veri.py"), "indir_sec"], capture_output=True, text=True, env=ortam, timeout=120)
            if r.returncode != 2 or K.K60V_UA_DEGISKEN not in r.stderr or os.path.exists(os.path.join(td, "sec_cli")):
                hata.append(f"3) komut satırı kimliksiz indir_sec'i reddetmedi (çıkış {r.returncode})")

            # 4) SEC indirme: kaldığı yerden sürme
            os.environ[K.K60V_UA_DEGISKEN] = SAHTE_UA
            isler = [x for x in K.k60v_sec_listesi(True, eski) if not x["mevcut"]][:40]
            bozuk = {x["url"] for x in isler[3:8]}; yok = {x["url"] for x in isler[10:13]}

            def ilk(url):
                if url in bozuk:
                    raise OSError("bağlantı koptu")
                if url in yok:
                    return 404, b""
                return None
            with open(os.path.join(td, "yarim_ornek"), "w") as f:
                f.write("x")
            os.makedirs(sf, exist_ok=True)
            with open(os.path.join(sf, isler[0]["dosya"] + ".yarim"), "w") as f:
                f.write('{"data": [')
            s1 = SahteSec(ilk); d1 = K.k60v_sec_indir(adet=40, getir=s1, klasor=sf, eski_klasor=eski, **sahte())
            if (d1["indirilen"], d1["yok_404"], d1["hata"], d1["onbellek"]) != (32, 3, 5, 0) or not d1["durum"].startswith("eksik") or len(s1.cagri) != 32 + 3 + 5 * 3:
                hata.append(f"4) ilk koşu sayıları yanlış: {d1['indirilen']}, {d1['yok_404']}, {d1['hata']}, çağrı {len(s1.cagri)}")
            if sorted(d1["inemeyen"]) != sorted(x["ad"] for x in isler[3:8]) or any(f.endswith(".yarim") for f in os.listdir(sf)):
                hata.append("4) inemeyen listesi yanlış / yarım dosya silinmedi")
            if any(os.path.exists(os.path.join(sf, x["dosya"])) for x in isler[3:8]) or open(os.path.join(sf, isler[10]["dosya"])).read() != "{}":
                hata.append("4) hatalı iş dosya bıraktı / 404 işareti '{}' değil")
            s2 = SahteSec(); d2 = K.k60v_sec_indir(adet=40, getir=s2, klasor=sf, eski_klasor=eski, **sahte())
            if sorted(s2.cagri) != sorted(bozuk) or (d2["indirilen"], d2["onbellek"], d2["durum"]) != (5, 35, "tamam"):
                hata.append(f"4) ikinci koşu yalnız eksik 5 çerçeveyi istemedi: çağrı {len(s2.cagri)}, {d2['durum']}")
            s3 = SahteSec(); d3 = K.k60v_sec_indir(adet=40, getir=s3, klasor=sf, eski_klasor=eski, **sahte())
            if s3.cagri or d3["onbellek"] != 40 or d3["manifest_sha256"] != d2["manifest_sha256"] or d3["ilk_indirme_utc"] != d1["ilk_indirme_utc"]:
                hata.append("4) üçüncü koşu istek attı / manifest özeti değişti")
            os.remove(os.path.join(sf, "_manifest.json"))                                   # yarıda kesilen koşu: manifest kayıp
            s4 = SahteSec(); d4 = K.k60v_sec_indir(adet=40, getir=s4, klasor=sf, eski_klasor=eski, **sahte())
            if s4.cagri or d4["manifest_sha256"] != d2["manifest_sha256"] or d4["manifest_dosya"] != 40:
                hata.append("4) kayıp manifest diskteki dosyalardan yeniden kurulmadı")
            open(os.path.join(sf, isler[20]["dosya"]), "w").close()                         # sıfır baytlık (bozuk) dosya yeniden iner
            s5 = SahteSec(); K.k60v_sec_indir(adet=40, getir=s5, klasor=sf, eski_klasor=eski, **sahte())
            if s5.cagri != [isler[20]["url"]]:
                hata.append("4) sıfır baytlık dosya yeniden indirilmedi")
            if {f: K.k60v_dosya_sha(os.path.join(eski, f)) for f in sorted(os.listdir(eski))} != eski_ozet:
                hata.append("4) eski önbellek (K59 girdisi) değişti")
            try:
                K.k60v_sec_indir(getir=SahteSec(), klasor=eski, eski_klasor=eski, **sahte())
                hata.append("4) eski önbellek klasörüne yazmayı reddetmedi")
            except K.K60VHata:
                pass
            sr = os.path.join(td, "sec_ret"); s6 = SahteSec(lambda url: (403, b""))
            d6 = K.k60v_sec_indir(adet=200, getir=s6, klasor=sr, eski_klasor=eski, **sahte())
            if not d6["durum"].startswith("reddedildi") or len(s6.cagri) > 12 or d6["indirilen"] or [f for f in os.listdir(sr) if f.endswith(".json") and not f.startswith("_")]:
                hata.append(f"4) 403'te indirme durmadı: çağrı {len(s6.cagri)}, {d6['durum']}")
            sg = os.path.join(td, "sec_gecersiz"); s7 = SahteSec(lambda url: (200, b"<html>bakim</html>"))
            d7 = K.k60v_sec_indir(adet=3, getir=s7, klasor=sg, eski_klasor=eski, **sahte())
            if d7["hata"] != 3 or len(s7.cagri) != 9 or [f for f in os.listdir(sg) if not f.startswith("_")]:
                hata.append("4) geçersiz yanıt dosya olarak yazıldı / yeniden denenmedi")

            # 5) hız sınırı
            saat = SahteSaat(); izin = []; orj = K.K60VHizSiniri.bekle

            def kayitli(self):
                t = orj(self); izin.append(t); return t
            K.K60VHizSiniri.bekle = kayitli
            try:
                st = os.path.join(td, "sec_tam"); s8 = SahteSec()
                d8 = K.k60v_sec_indir(hiz=500.0, getir=s8, klasor=st, eski_klasor=eski, uyu=saat.uyu, zaman=saat.zaman)   # 500 / sn istenir: 8'e iner
            finally:
                K.K60VHizSiniri.bekle = orj
            a = np.sort(np.array(izin))
            if len(s8.cagri) != 1710 or len(izin) != 1710 or d8["indirilen"] != 1710 or d8["durum"] != "tamam" or len(set(s8.cagri)) != 1710:
                hata.append(f"5) tam liste 1710 istek değil: {len(s8.cagri)}")
            if len(a) > 1 and (np.diff(a).min() < 0.125 - 1e-9 or max(int(np.searchsorted(a, t + 1.0, side="left") - i) for i, t in enumerate(a)) > 8):
                hata.append(f"5) sahte saatte hız sınırı aşıldı: en küçük aralık {np.diff(a).min():.4f} sn")
            if set(Le[Le.mevcut.notna()].url) & set(s8.cagri) or {f: K.k60v_dosya_sha(os.path.join(eski, f)) for f in sorted(os.listdir(eski))} != eski_ozet:
                hata.append("5) eski önbellekte olan çerçeve istendi / eski önbellek değişti")
            if any(b.get("User-Agent") != SAHTE_UA for b in s8.baslik):
                hata.append("5) kimlik satırı istek başlığına K60_SEC_UA'dan gitmedi")
            hs = K.K60VHizSiniri(1000.0)
            if hs.hiz != 8.0 or hs.aralik < 0.125:
                hata.append("5) hız üst sınırı (8 / sn) aşılabiliyor")
            for kotu in (0, -1, None):
                try:
                    K.K60VHizSiniri(kotu); hata.append(f"5) hız {kotu} kabul edildi")
                except K.K60VHata:
                    pass
            sgz = os.path.join(td, "sec_gercek"); s9 = SahteSec(); t0 = time.monotonic()
            K.k60v_sec_indir(hiz=8.0, adet=17, getir=s9, klasor=sgz, eski_klasor=eski)        # gerçek saat, 4 iş parçacığı
            b = np.sort(np.array(s9.an))
            if len(b) != 17 or np.diff(b).min() < 0.115 or max(int(np.searchsorted(b, t + 1.0, side="left") - i) for i, t in enumerate(b)) > 8 \
                    or time.monotonic() - t0 < 16 * 0.125:
                hata.append(f"5) gerçek saatte hız sınırı aşıldı: en küçük aralık {np.diff(b).min():.3f} sn, süre {time.monotonic() - t0:.2f} sn")

            # 6) manifest sha256
            Mj = json.load(open(os.path.join(st, "_manifest.json"), encoding="utf-8")); ad0 = sorted(Mj["dosyalar"])[0]
            if Mj["dosya_sayisi"] != 1710 or Mj["dosyalar"][ad0]["sha256"] != hashlib.sha256(open(os.path.join(st, ad0), "rb").read()).hexdigest():
                hata.append("6) manifestteki sha256 dosyanın sha256'sı değil")
            h = hashlib.sha256()
            for ad in sorted(Mj["dosyalar"]):
                h.update(f"{ad}:{Mj['dosyalar'][ad]['sha256']}\n".encode("utf-8"))
            if h.hexdigest() != Mj["klasor_ozet_sha256"] or d8["manifest_sha256"] != Mj["klasor_ozet_sha256"]:
                hata.append("6) klasör özeti 'ad:sha256' kuralıyla yeniden üretilemedi")
            if any(a_.startswith("_") for a_ in Mj["dosyalar"]):
                hata.append("6) manifest kendi durum dosyalarını içeriyor")
            v0 = K.k60v_manifest_dogrula(st)
            if not v0["saglam"] or v0["dosya"] != 1710:
                hata.append("6) sağlam klasör doğrulanamadı")
            adlar = sorted(Mj["dosyalar"])
            with open(os.path.join(st, adlar[1]), "ab") as f:
                f.write(b" ")
            os.remove(os.path.join(st, adlar[2]))
            with open(os.path.join(st, "yabanci.json"), "w") as f:
                f.write("{}")
            v1 = K.k60v_manifest_dogrula(st)
            if v1["saglam"] or v1["farkli"] != [adlar[1]] or v1["eksik"] != [adlar[2]] or v1["fazla"] != ["yabanci.json"]:
                hata.append(f"6) kurcalanan / eksik / fazla dosya yakalanmadı: {v1['farkli']}, {v1['eksik']}, {v1['fazla']}")

            # 7) e-posta / kimlik satırı sızıntısı
            yk = Yakala(); K.k60vlog.addHandler(yk); eski_duzey = K.k60vlog.level; K.k60vlog.setLevel(logging.DEBUG)
            try:
                sz = os.path.join(td, "sec_sizinti")
                isz = [x for x in K.k60v_sec_listesi(True, eski) if not x["mevcut"]][:6]

                def sizdir(url):
                    if url == isz[1]["url"]:
                        raise OSError(f"proxy hatası, başlık: {SAHTE_UA}")
                    if url == isz[2]["url"]:
                        raise RuntimeError(f"beklenmedik: {SAHTE_UA}")
                    return None
                s10 = SahteSec(sizdir); K.k60v_sec_indir(adet=6, getir=s10, klasor=sz, eski_klasor=eski, **sahte())
                K.k60vlog.info("elle sızıntı denemesi %s ve %s", SAHTE_UA, "baska.kisi" + "@" + "example" + ".org")
            finally:
                K.k60vlog.removeHandler(yk); K.k60vlog.setLevel(eski_duzey)
            if not s10.baslik or any(b_.get("User-Agent") != SAHTE_UA for b_ in s10.baslik):
                hata.append("7) kimlik satırı isteğe gitmedi")
            gunluk = "\n".join(yk.satir)
            if "<K60_SEC_UA>" not in gunluk or "<e-posta>" not in gunluk:
                hata.append("7) günlükte maske izi yok (sızıntı denemesi günlüğe hiç düşmedi)")
            metinler = {"günlük (bellek)": gunluk}
            for kl in (sf, st, sz, sr):
                for f in os.listdir(kl):
                    if f.startswith("_"):
                        metinler[os.path.join(os.path.basename(kl), f)] = open(os.path.join(kl, f), encoding="utf-8").read()
            if not any(k_.endswith("_gunluk.log") for k_ in metinler) or not any(k_.endswith("_durum.json") for k_ in metinler):
                hata.append("7) günlük / durum dosyası yazılmadı")
            for ad, m in metinler.items():
                if any(p in m for p in SAHTE_PARCA) or SAHTE_UA in m or "User-Agent" in m:
                    hata.append(f"7) kimlik satırı / e-posta sızdı: {ad}")
            if K.k60v_maskele(f"x {SAHTE_UA} y") != "x <K60_SEC_UA> y":
                hata.append("7) k60v_maskele kimlik satırını silmiyor")

            # 8) Yahoo indirme
            idx, S = sentetik_evren(); fy = os.path.join(td, "fiyat"); govde = {}
            for s_, (ix, c, v, tur, bol) in S.items():
                govde[s_] = yahoo_json(ix, c, v, tur, bol, [(ix[5], 0.1)] if s_ == "IYI" else None)

            def yahoo(url):
                s_ = re.search(r"/chart/([^?]+)\?", url).group(1)
                if s_ == "YOKTUR":
                    return 404, b""
                if s_.startswith("ENGEL"):
                    return 429, b""
                return 200, govde[s_]
            y1 = SahteSec(yahoo); e1 = K.k60v_fiyat_indir(semboller=list(S) + ["YOKTUR", "iyi"], getir=y1, klasor=fy, uyu=bos_uyu)
            if (e1["indirilen"], e1["yok_404"], e1["istenen"], e1["durum"]) != (7, 1, 8, "tamam") or len(y1.cagri) != 8:
                hata.append(f"8) Yahoo ilk koşu sayıları yanlış: {e1['indirilen']}, {e1['yok_404']}, {e1['istenen']}")
            u0 = y1.cagri[0]; p1 = int(pd.Timestamp("2010-01-01", tz="UTC").timestamp())
            if not u0.startswith(K57.K57B_ESIK["yahoo"]["url"].split("{")[0]) or f"period1={p1}&" not in u0 or "events=div%2Csplits" not in u0 \
                    or "interval=1d" not in u0 or any(b_.get("User-Agent") != K57.K57B_YAHOO_UA for b_ in y1.baslik):
                hata.append("8) Yahoo ucu / kimliği K57-B ile aynı değil ya da başlangıç 2010-01-01 değil")
            if open(os.path.join(fy, "TERS.json"), "rb").read() != govde["TERS"] or json.load(open(os.path.join(fy, "YOKTUR.json"))) != {"yok": 404}:
                hata.append("8) ham yanıt bayt bayt saklanmadı / 404 işareti yanlış")
            if "splits" not in json.load(open(os.path.join(fy, "TERS.json")))["chart"]["result"][0]["events"] \
                    or "dividends" not in json.load(open(os.path.join(fy, "IYI.json")))["chart"]["result"][0]["events"]:
                hata.append("8) bölünme / temettü olayları saklanmadı")
            y2 = SahteSec(yahoo); e2 = K.k60v_fiyat_indir(semboller=list(S) + ["YOKTUR"], getir=y2, klasor=fy, uyu=bos_uyu)
            if y2.cagri or e2["onbellek"] != 8 or e2["manifest_sha256"] != e1["manifest_sha256"] or not K.k60v_manifest_dogrula(fy)["saglam"]:
                hata.append("8) Yahoo ikinci koşu istek attı / manifest değişti")
            K.K60V_ESIK["yahoo"]["engel_ardisik"] = 4
            fe = os.path.join(td, "fiyat_engel"); y3 = SahteSec(yahoo)
            e3 = K.k60v_fiyat_indir(semboller=[f"ENGEL{i}" for i in range(60)], getir=y3, klasor=fe, uyu=bos_uyu)
            K.K60V_ESIK["yahoo"].update(yedek_yahoo)
            if not e3["durum"].startswith("engellendi") or len(y3.cagri) >= 60 * K.K60V_ESIK["yahoo"]["deneme"] or e3["indirilen"] or e3["durdu"] == 0:
                hata.append(f"8) art arda engelde indirme durmadı: {e3['durum']}, çağrı {len(y3.cagri)}")
            try:
                K.k60v_fiyat_indir(semboller=["IYI"], getir=SahteSec(yahoo), klasor=K.K60V_YOL["eski_fiyat"], uyu=bos_uyu)
                hata.append("8) K59 fiyat klasörüne yazmayı reddetmedi")
            except K.K60VHata:
                pass
            if os.path.abspath(K.K60V_YOL["fiyat"]) == os.path.abspath(K57.K57B_YOL["fiyat"]) or os.path.abspath(K.K60V_YOL["frames"]) == os.path.abspath(K57.K57_YOL["frames"]):
                hata.append("8) yeni önbellek klasörleri K59 girdileriyle aynı")
            try:
                Ue = K.k60v_evren()
                if Ue.sembol.duplicated().any() or (os.path.exists(K.K60V_YOL["evren_b1"]) and len(Ue) < 4000):
                    hata.append("8) evren listesi yinelemeli / eksik")
            except K.K60VHata:
                pass

            # 9) okuyucu + uygun evren
            import K59
            o, dr = K.k60v_yahoo_oku(os.path.join(fy, "TERS.json"), "2012-12-31"); c59, b59 = K59.k59_yahoo_ham(os.path.join(fy, "TERS.json"), "2012-12-31")
            if dr != "fiyat" or not np.allclose(o["kapanis"], c59.to_numpy()) or not o["gun"].equals(c59.index) or not np.allclose(o["bolunme"][1], b59[1]) \
                    or not (o["bolunme"][0] == b59[0]).all():
                hata.append("9) okuyucu K59 k59_yahoo_ham ile aynı ham kapanışı / bölünmeyi vermiyor")
            tt = o["gun"].to_numpy("datetime64[ns]")
            if not np.allclose(K.k60v_bolunme_carpan(o["bolunme"], tt), K59.k59_bolunme_carpan(b59, tt)) or K.k60v_bolunme_carpan(None, tt).min() != 1.0:
                hata.append("9) bölünme çarpanı K59 ile aynı değil")
            if K.k60v_yahoo_oku(os.path.join(fy, "YOKTUR.json"))[1] != "yok" or K.k60v_yahoo_oku(os.path.join(td, "yarim_ornek"))[0] is not None:
                hata.append("9) 404 işareti / bozuk dosya okuyucuda ayrışmadı")
            ok_ = K.k60v_yahoo_oku(os.path.join(fy, "IYI.json"), "2011-03-31")[0]
            if ok_["gun"][-1] != pd.Timestamp("2011-03-31") or ok_["temettu"] != 1 or ok_["tur"] != "EQUITY":
                hata.append("9) kesme günü / temettü sayısı / tür yanlış")
            bay = K.k60v_gunluk_bayrak(o)
            g_once = o["gun"] < pd.Timestamp("2012-06-01")
            if (bay[g_once] & 2).any() or not (bay[~g_once] & 2).all() or (bay[:251] & 1).any() or not (bay[251:] & 1).all() or (bay[:14] & 4).any() or not (bay[14:] & 4).all():
                hata.append("9) günlük bayraklar yanlış (ters bölünme öncesi o günkü fiyat 1,5 $; 252. gün; 15. gün)")
            T = K.k60v_fiyat_tara(fy); Kp, Ay, Yl = T["kapsam"].set_index("sembol"), T["ay"].set_index("ay_sonu"), T["yil"].set_index("yil")
            ref = referans_ay(idx, S)
            if len(Ay) != len(ref) or not (Ay.index == ref.index).all() or not (Ay.uygun.to_numpy() == ref.to_numpy()).all():
                hata.append(f"9) uygun evren ay sayıları bağımsız panel hesabıyla aynı değil (fark {int((Ay.uygun.to_numpy() != ref.to_numpy()).sum()) if len(Ay) == len(ref) else 'boy'})")
            bek = {"2010-11-30": 0, "2010-12-31": 2, "2011-06-30": 2, "2011-07-29": 1, "2012-05-31": 1, "2012-06-29": 2, "2012-12-31": 2}
            for a_, n_ in bek.items():
                if int(Ay.uygun.get(pd.Timestamp(a_), -1)) != n_:
                    hata.append(f"9) {a_} uygun evren {n_} olmalı: {Ay.uygun.get(pd.Timestamp(a_), None)}")
            if int(Ay.islem.loc["2012-12-31"]) != 5 or int(Ay.fiyat.loc["2012-12-31"]) != 4 or int(Ay.likit.loc["2012-12-31"]) != 4 or int(Ay.gecmis.loc["2012-12-31"]) != 4:
                hata.append("9) yıl sonu bileşen sayıları (işlem gören 5, fiyat 4, likit 4, geçmiş 4) yanlış")
            if Kp.loc["FON", "tur"] != "ETF" or Kp.loc["YOKTUR", "durum"] != "yok" or int(Kp.loc["TERS", "bolunme"]) != 1 or int(Kp.loc["IYI", "temettu"]) != 1 \
                    or str(Kp.loc["YENI", "ilk"]) != "2012-03-01" or str(Kp.loc["ESKI", "son"]) != "2011-06-30" or int(Kp.loc["IYI", "gun"]) != len(idx):
                hata.append("9) kapsam tablosu yanlış")
            if int(Yl.loc[2010, "seri"]) != 6 or int(Yl.loc[2012, "seri"]) != 6 or int(Yl.loc[2011, "tam_yil_seri"]) != 5 or int(Yl.loc[2012, "hisse_gun"]) != 5 * int((idx.year == 2012).sum()) + int((idx >= "2012-03-01").sum()) \
                    or int(Yl.loc[2012, "uygun_yil_sonu"]) != 2 or int(Yl.loc[2011, "uygun_min"]) != 1 or int(Yl.loc[2011, "uygun_maks"]) != 2:
                hata.append("9) yıl tablosu yanlış")
            fb_ = os.path.join(td, "fiyat_bozuk"); evren_yaz(fb_, S, boz_sonra="2011-12-30")   # geleceğe bakma: 2011 sonrasını boz
            Ab = K.k60v_fiyat_tara(fb_)["ay"].set_index("ay_sonu"); m_ = Ay.index <= pd.Timestamp("2011-12-30")
            if not Ab.loc[Ab.index <= pd.Timestamp("2011-12-30")].equals(Ay.loc[m_]) or Ab.equals(Ay):
                hata.append("9) GELECEĞE BAKMA: 2011 sonrası bozulunca 2011 ve öncesi ay sayıları değişti (ya da bozma etkisiz)")

            # 10) SEC denetimi
            sd_ = os.path.join(td, "sec_denet"); id_ = [x for x in K.k60v_sec_listesi(True, eski) if not x["mevcut"]][:12]

            def karisik(url):
                if url == id_[0]["url"]:
                    return 404, b""
                if url == id_[1]["url"]:
                    return 200, cerceve(url, 5, filed=True)
                if "full-index" in url:
                    govde_ = ("Description: Master Index\n\nCIK|Company Name|Form Type|Date Filed|Filename\n----\n"
                              "1000|A CORP|10-K|2015-03-01|edgar/data/1000/0001.txt\n1000|A CORP|8-K|2015-03-02|edgar/data/1000/0002.txt\n"
                              "1001|B CORP|10-Q|2015-03-03|edgar/data/1001/0003.txt\n1001|B CORP|10-Q|2015-02-03|edgar/data/1001/0004.txt\n")
                    return 200, gzip.compress(govde_.encode("latin-1"))
                return None
            K.k60v_sec_indir(adet=12, getir=SahteSec(karisik), klasor=sd_, eski_klasor=eski, **sahte())
            dz = K.k60v_dizin_listesi()[0]; kd, hm = karisik(dz["url"])
            Md = K.K60VManifest(sd_); Md.dosya_yaz(dz["dosya"], hm, "tamam"); Md.kaydet()
            R = K.k60v_sec_denetle(sd_, eski); Sy = R["sayim"]; q = Sy.set_index(["etiket", "donem"])
            if len(Sy[Sy.grup != "DIZIN"]) != 1916 or (Sy.kaynak == "k60").sum() != 13 or (Sy.kaynak == "eski").sum() != 206 or (Sy.kaynak == "inmedi").sum() != 1916 - 12 - 206:
                hata.append(f"10) denetim kaynak sayıları yanlış: {Sy.kaynak.value_counts().to_dict()}")
            r0, r1, r2 = q.loc[(id_[0]["etiket"], id_[0]["donem"])], q.loc[(id_[1]["etiket"], id_[1]["donem"])], q.loc[(id_[2]["etiket"], id_[2]["donem"])]
            if r0.durum != "yok_404" or (int(r1.sirket), int(r1.satir), bool(r1.filed_var)) != (5, 6, True) or (int(r2.sirket), int(r2.satir), bool(r2.filed_var)) != (3, 4, False):
                hata.append("10) çerçeve sayımı (ayrı CIK, satır, 'filed' alanı) yanlış")
            rd = Sy[Sy.grup == "DIZIN"].iloc[0]
            if len(Sy[Sy.grup == "DIZIN"]) != 1 or (int(rd.satir), int(rd.sirket)) != (3, 2):
                hata.append("10) EDGAR dizin sayımı (10-K / 10-Q başvurusu 3, şirket 2) yanlış")
            fbl = K.k60v_filed_bulgusu(Sy)
            if fbl["eski_dosya"] != 11 or fbl["eski_filed"] != 1 or fbl["dizin_dosya"] != 1 or "accn" not in fbl["alanlar"] or "filed" not in fbl["alanlar"]:
                hata.append(f"10) 'filed' bulgusu yanlış: {fbl}")
            if K.k60v_frame_say(os.path.join(td, "yarim_ornek"))["durum"] != "bozuk":
                hata.append("10) bozuk çerçeve 'bozuk' sayılmadı")

            # 11) raporlar (sentetik klasörlerde)
            ck = os.path.join(td, "cikti"); K.K60V_YOL.update({"frames": sd_, "fiyat": fy, "eski_frames": eski})
            try:
                yp = K.k60v_plan(ck); pm = open(yp, encoding="utf-8").read(); Lc = pd.read_csv(os.path.join(ck, "K60_SEC_ISTEK_LISTESI.csv"))
                if len(Lc) != 1916 or (Lc.durum == "indirilecek").sum() != 1710 or not Lc.url.str.startswith("https://data.sec.gov/").all():
                    hata.append("11) istek listesi CSV'si yanlış")
                for parca in ("1.710 istek", "saniyede en çok 8 istek", "YALNIZ YILLIK", "K60_SEC_UA=", "indir_sec", "EntityCommonStockSharesOutstanding",
                              "NetCashProvidedByUsedInOperatingActivities", "CY2009Q1 .. CY2026Q2", "CY2009 .. CY2025", "4. çeyrek", "çeyrek sonu + 90 gün"):
                    if parca not in pm:
                        hata.append(f"11) planda '{parca}' yok")
                Rd = K.k60v_denetle(ck); dm = open(Rd["yol"], encoding="utf-8").read()
                if Rd["sec_manifest"] is None or not Rd["sec_manifest"]["saglam"] or Rd["fiyat_manifest"] is None or Rd["sec_manifest"]["klasor_ozet_sha256"] not in dm \
                        or Rd["fiyat_manifest"]["klasor_ozet_sha256"] not in dm or not os.path.exists(os.path.join(ck, "sec_sayim.csv")) or not os.path.exists(os.path.join(ck, "fiyat_kapsam.csv")):
                    hata.append("11) denetim raporu manifest sha256'larını / sayım dosyalarını yazmadı")
                if "| Revenues | çeyreklik |" not in dm or "'filed' alanı" not in dm:
                    hata.append("11) denetim raporunda etiket x yıl tablosu / 'filed' satırı yok")
                yo = K.k60v_ozet(ck); om = open(yo, encoding="utf-8").read()
                for parca in ("Yalnız yaşayanlar", "son bildirilen değeri", "çeyrek sonu + 90 gün", "XBRL'e geçiş", "| 2012 |", "KEŞİF", "İlk fiyat gününe göre",
                              "fiyat ≥ 2 $", "yalnız yıllık"):
                    if parca not in om:
                        hata.append(f"11) özette '{parca}' yok")
                if not os.path.exists(os.path.join(ck, "evren_ay.csv")):
                    hata.append("11) evren_ay.csv yazılmadı")
                K.K60V_YOL.update({"frames": os.path.join(td, "hic_yok"), "fiyat": os.path.join(td, "hic_yok2")})
                om2 = open(K.k60v_ozet(os.path.join(td, "cikti2")), encoding="utf-8").read()
                if "HENÜZ YAPILMADI" not in om2 or "Fiyat önbelleği yok" not in om2 or "`filed` alanı YOK" not in om2:
                    hata.append("11) indirme yokken özet durumu açık yazmadı")
                for kl in (ck, os.path.join(td, "cikti2")):
                    for f in os.listdir(kl):
                        m = open(os.path.join(kl, f), encoding="utf-8").read()
                        if any(p in m for p in SAHTE_PARCA) or SAHTE_UA in m:
                            hata.append(f"11) raporda kimlik satırı / e-posta: {f}")
            finally:
                K.K60V_YOL.clear(); K.K60V_YOL.update(yedek_yol)
            r = subprocess.run([sys.executable, os.path.join(KOK, "K60_veri.py"), "plan", "--cikti", os.path.join(td, "cli_plan"), "--ek", "hayir", "--dizin", "evet"],
                               capture_output=True, text=True, timeout=120, env={k: v for k, v in os.environ.items() if k != K.K60V_UA_DEGISKEN})
            if r.returncode != 0 or "K60 veri planı" not in r.stdout or not os.path.exists(os.path.join(td, "cli_plan", "K60_VERI_PLANI.md")) or "EDGAR dizini 71 istek" not in r.stdout:
                hata.append(f"11) komut satırı plan çalışmadı (çıkış {r.returncode}): {r.stderr[-300:]}")
    except Exception as ex:
        import traceback
        hata.append(f"testler çöktü: {type(ex).__name__} {ex}\n{traceback.format_exc()[-1500:]}")
    finally:
        K.K60V_YOL.clear(); K.K60V_YOL.update(yedek_yol); K.K60V_ESIK["yahoo"].update(yedek_yahoo)
        if eski_ua is None:
            os.environ.pop(K.K60V_UA_DEGISKEN, None)
        else:
            os.environ[K.K60V_UA_DEGISKEN] = eski_ua

    # 12) kodda ve çıktılarda e-posta / anahtar yok
    cik = yedek_yol["cikti"]
    dosyalar = [os.path.join(KOK, "K60_veri.py"), os.path.join(KOK, "test_k60_veri.py")] + \
               ([os.path.join(cik, f) for f in os.listdir(cik) if f.endswith((".md", ".csv", ".json"))] if os.path.isdir(cik) else [])
    for kl in (yedek_yol["frames"], yedek_yol["fiyat"]):                 # gerçek önbelleklerin durum / günlük / manifest dosyaları (varsa)
        if os.path.isdir(kl):
            dosyalar += [os.path.join(kl, f) for f in os.listdir(kl) if f.startswith("_")]
    for y in dosyalar:
        t = open(y, encoding="utf-8", errors="replace").read()
        if re.search(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b", t):
            hata.append(f"12) e-posta var: {y}")
        if re.search(r"(api[_-]?key|token|secret|password)\s*[=:]\s*['\"][A-Za-z0-9_\-]{12,}", t, re.I):
            hata.append(f"12) anahtar benzeri dize var: {y}")
    kod = open(os.path.join(KOK, "K60_veri.py"), encoding="utf-8").read()
    if kod.count('os.environ.get(K60V_UA_DEGISKEN') != 2 or '"User-Agent": ua' not in kod or re.search(r"User-Agent\W+[\"'](?!K57)[A-Za-z]", kod):
        hata.append("12) SEC kimlik satırı ortam değişkeni dışında bir yerden geliyor olabilir")
    return hata


if __name__ == "__main__":
    Hh = testler()
    if Hh:
        print("K60_veri TEST: HATA", len(Hh)); print("\n".join(Hh)); sys.exit(1)
    print("K60_veri TEST: 12/12 bölüm GEÇTİ")
