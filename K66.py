"""K66 — ABD AÇIĞA SATIŞ TALEBİ (short interest) ÇÖL SİNYALİNE EK BİLGİ TAŞIYOR MU? Tek dosya
(12 Kasım 2026; ana oturum iş tanımı; ön kayıt arastirma_cikti/col_dis_bilgi/K66_ON_KAYIT.md).

Tasarım K64 + K65 ile AYNIDIR (K64_K65_ON_KAYIT.md): olay, S1 (çöl içi ÜST / ALT üçte bir; ÜST - ALT ay kümeli bootstrap), S2 (çöl dışı evren; bilgi), cetvel
(FON_IZI FI_OLCUT aynen), piyasa koşulu, maliyet, dönem ve karar kuralları, BH. K64.py MODÜL olarak içe alınır ve DEĞİŞMEZ; yalnız değişkenler yenidir:
  SI_PAY   son bilinen açık pozisyon / o gün bilinen toplam pay (K60.k60_pay; float yok -> toplam pay)
  DTC      son bilinen kapatma günü = açık pozisyon / ortalama günlük hacim (FINRA dosyasının iki alanı; ADV > 0)
  SI_DEG   son bilinen açık pozisyonun 6 rapor (~3 ay) önceki bilinen değere göre ln oranı (bölünme düzeltmeli)
  SI_DEG1  son raporun bir önceki rapora göre değişimi (dosyadaki changePercent / 100; bilgi amaçlı kısa vade)
Veri: FINRA iki haftalık açık pozisyon dosyaları (cdn.finra.org/equity/otcmarket/biweekly/shrtYYYYMMDD.csv; 2017-12-29 ->). Ücretsiz, anahtarsız.
BİLGİ TARİHİ: rapor ödeme (settlement) gününden sonraki 12. işlem günü (tutucu; FINRA yayını 7. iş günü); değer ancak bilgi tarihi < t ise kullanılır.

Komut:  python K66.py indir        yalnız VERİ: FINRA dosyaları -> /tmp/k66_finra (var olan yeniden inmez); getiri / ölçüm yok
        python -I K66.py kapsam    yalnız SAYIM (FINRA kapsamı, olay, değişken kapsamı, üçte bir grupları); getiri HESAPLANMAZ
        python K66.py onkayit      ön kaydı yazar (ölçümden ÖNCE; mühür + veri sha256 + kapsam; varsa üzerine yazmaz)
        python -I K66.py kos       mühür + veri sha256 + ön kayıt git'e işlenmiş ve değişmemiş -> ölçüm + rapor
        python K66.py rapor        K66_RAPOR.md'yi çıktılardan yeniden yazar
Colab:  exec(open('K66.py').read()); k66_kos()
Veri:   /tmp/veri/V_ABD.pkl (islenmis-veri dalı), /tmp/k60_* (K60 önbellekleri; pay sayısı ve bölünmeler), /tmp/k66_finra (FINRA). SEC'e istek atılmaz;
        kişisel e-posta / anahtar yok. Çıktılar arastirma_cikti/col_dis_bilgi/ (k66_*).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K66 = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import glob  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K66 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K66 not in sys.path:
    sys.path.insert(0, KOK_K66)

import K64  # noqa: E402

FI, K60 = K64.FI, K64.K60
K59 = K60.K59

k66log = logging.getLogger("col.k66")
if not k66log.handlers:
    _k66_h = logging.StreamHandler(sys.stderr)
    _k66_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k66: %(message)s", "%H:%M:%S"))
    k66log.addHandler(_k66_h)
    k66log.setLevel(logging.INFO)
    k66log.propagate = False

K66_SURUM = "K66 v1.0 (2026-11-12): ABD açığa satış talebi (FINRA açık pozisyon) çöl sinyaline ek bilgi; K64 tasarımı aynen, 4 değişken x 2 yön"
K66_YOL = {"cikti": os.path.join(KOK_K66, "arastirma_cikti", "col_dis_bilgi"), "veri": os.environ.get("K66_VERI", K64.K64_YOL["veri"]),
           "finra": os.environ.get("K66_FINRA", "/tmp/k66_finra"), "ara": os.environ.get("K66_ARA", "/tmp/k66_ara")}
K66_DOSYA = {"onkayit": "K66_ON_KAYIT.md", "kapsam": "k66_kapsam.csv", "kapsam_ozet": "k66_kapsam_ozet.json", "olay": "k66_olaylar.csv.gz", "s1": "k66_s1.csv",
             "fark": "k66_s1_fark.csv", "s2": "k66_s2.csv", "karar": "k66_karar.csv", "meta": "k66_meta.json", "rapor": "K66_RAPOR.md", "indir": "k66_indir.json"}
_K66_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")
_K66_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
K66_FINRA_SUTUN = ["accountingYearMonthNumber", "symbolCode", "issueName", "issuerServicesGroupExchangeCode", "marketClassCode", "currentShortPositionQuantity",
                   "previousShortPositionQuantity", "stockSplitFlag", "averageDailyVolumeQuantity", "daysToCoverQuantity", "revisionFlag", "changePercent",
                   "changePreviousNumber", "settlementDate"]

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256'sı ön kayıtta; sonradan değişmez)
_K66_DEGISKEN: List[Tuple[str, str, str, str]] = [
    ("SI_PAY", "K66", "SI(r0) x b(r0) / PAY(t): son bilinen rapor r0'ın açık pozisyonu (bugünkü pay birimine bölünme çarpanı b ile) / t günü bilinen toplam pay "
     "(K60.k60_pay, bugünkü birim). PAY > 0; oran > 2 ise veri hatası sayılır (yok)", "açığa satış oranı (yüksek = kötü haber beklentisi; Dechow vd. 2001, Asquith vd. 2005)"),
    ("DTC", "K66", "SI(r0) / ADV(r0): r0 raporunun açık pozisyonu / aynı raporun ortalama günlük hacmi (FINRA 'days to cover' formülü; dosyadaki 1,00 tabanı ve "
     "yuvarlama uygulanmaz); ADV > 0", "kapatma günü (Hong vd. 2016)"),
    ("SI_DEG", "K66", "ln(SI(r0) x b(r0) / (SI(r0-6) x b(r0-6))): son bilinen rapor ile 6 rapor (~3 ay) önceki rapor; ikisi de > 0. Aradaki 6 raporun birinde FINRA "
     "bölünme bayrağı varken K60 bölünme kaydında o aralıkta bölünme yoksa (düzeltilemiyor) yok", "açık pozisyon artışı (proje ölçüsü)"),
    ("SI_DEG1", "K66", "changePercent(r0) / 100: son raporun bir önceki rapora göre değişimi (dosyadaki alan); önceki pozisyon > 0; r0'da bölünme bayrağı ya da "
     "(r0-1, r0] aralığında bilinen bölünme varsa yok", "kısa vade değişim (bilgi)"),
]

K66_ESIK: Dict[str, Any] = {
    "kriz": K64.K64_ESIK["kriz"],
    "donem": [["2018-2021", "2018-01-01", "2021-12-31"], ["2022-2026", "2022-01-01", "2026-12-31"], ["2023-2026", "2023-01-01", "2026-12-31"]],
    "bagimsiz": ["2018-2021", "2022-2026"],
    "pazar": ["ABD"], "karar_pazari": "ABD",
    "olay": copy.deepcopy(K64.K64_ESIK["olay"]),
    "sira": {"ust": 2.0 / 3.0, "alt": 1.0 / 3.0, "min_evren": 30, "ic_gun": 365, "ic_min": 30, "karar": {"K66": "IC"}},
    "sira_secim": {"n_min": 30, "oran_min": 0.5},
    "s1": {"n_esik": 30, "bootstrap": 2000, "tohum": 66001, "guven": [2.5, 97.5], "gecerli_pay": 0.90},
    "s2": {"bootstrap": 2000, "tohum": 66002},
    "ek_ufuk": 20, "piyasa": {"sma": 200, "min_hisse": 30},
    "maliyet": {"ABD": 0.0020},
    "coklu": {"bh_q": 0.10},
    "finra": {"url": "https://cdn.finra.org/equity/otcmarket/biweekly/shrt{g}.csv", "ilk": "2017-12-29", "son": "2026-08-31", "ay_ortasi_gun": 15, "aday_gun": 7,
              "bilgi_gecikme_islem": 12, "deg_rapor": 6, "si_pay_aykiri": 2.0, "bekle": 0.4, "deneme": 3,
              "kimlik": {"bant": 3.0, "ilk_gun": 14, "min_bar": 3}},
    "degisken": [{"kod": k, "aile": a, "tanim": t, "kaynak": ky} for k, a, t, ky in _K66_DEGISKEN],
}


class K66Hata(RuntimeError):
    """K66'ya özgü durdurucu hata (ön kayıt yok / değişmiş / git'e işlenmemiş, veri eksik ya da farklı, FINRA dosyası bozuk, çıktı yok)."""


def _k66_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K66_YOL["cikti"], K66_DOSYA.get(ad, ad))


def _k66_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def k66_kodlar(E: Optional[Dict[str, Any]] = None) -> List[str]:
    return K64.k64_kodlar(E or K66_ESIK)


def k66_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: K66_ESIK (değişken tanımları, FINRA bilgi tarihi kuralı, karar sırası dahil) + K64 dış tanımları (FI_K24, FI_OLCUT, K60 bilgi kuralı ve
    mührü, COL_v1 D13) + K64 mührü (içe alınan tasarım). Biri değişirse koşu durur."""
    s = json.dumps({"K66_ESIK": E or K66_ESIK, "bagimli": K64._k64_bagimli(), "K64_muhur": K64.k64_esik_sha()}, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- 1) FINRA VERİSİ (ağ yalnız `indir` komutunda, yalnız cdn.finra.org)
def k66_finra_adaylar(E: Optional[Dict[str, Any]] = None) -> List[Tuple[str, List[str]]]:
    """Rapor yuvaları ve aday ödeme günleri: her ay (a) ay ortası: 15'i ve önceki aday_gun - 1 gün, (b) ay sonu: ayın son günü ve önceki aday_gun - 1 gün;
    yalnız hafta içi, [ilk, son] aralığında, yeni -> eski sırada (FINRA kuralı: 15'i ya da ondan önceki ödeme günü; ayın son ödeme günü). Döner [(yuva, [YYYYMMDD])]."""
    F = (E or K66_ESIK)["finra"]; ilk, son = pd.Timestamp(F["ilk"]), pd.Timestamp(F["son"]); out = []
    for ay in pd.period_range(ilk.to_period("M"), son.to_period("M"), freq="M"):
        orta = pd.Timestamp(year=ay.year, month=ay.month, day=int(F["ay_ortasi_gun"])); sonu = ay.end_time.normalize()
        for ad, bas in (("orta", orta), ("son", sonu)):
            g = [bas - pd.Timedelta(days=k) for k in range(int(F["aday_gun"]))]
            g = [x.strftime("%Y%m%d") for x in g if x.weekday() < 5 and ilk <= x <= son]
            if g:
                out.append((f"{ay}-{ad}", g))
    return out


def _k66_getir(gun: str, E: Optional[Dict[str, Any]] = None) -> Tuple[int, bytes]:
    """FINRA CDN'den bir dosya: (HTTP durum kodu, gövde). Kimlik / anahtar / kişisel bilgi gönderilmez; genel tarayıcı User-Agent."""
    import ssl
    import urllib.error
    import urllib.request
    url = (E or K66_ESIK)["finra"]["url"].format(g=gun); ca = os.environ.get("K66_CA", "/root/.ccr/ca-bundle.crt")
    ctx = ssl.create_default_context(cafile=ca if os.path.exists(ca) else None)
    r = urllib.request.Request(url, headers={"User-Agent": _K66_UA, "Accept": "text/csv,*/*"})
    try:
        with urllib.request.urlopen(r, timeout=60, context=ctx) as f:
            return int(f.status), f.read()
    except urllib.error.HTTPError as ex:
        return int(ex.code), b""


def _k66_dosya_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for p in iter(lambda: f.read(1 << 20), b""):
            h.update(p)
    return h.hexdigest()


def k66_finra_indir(klasor: Optional[str] = None, getir: Optional[Callable[[str], Tuple[int, bytes]]] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """FINRA önbelleği: <klasor>/shrtYYYYMMDD.csv (ham dosya). Her yuva için adaylar sırayla denenir; 200 + doğru başlık gelen ilk aday yazılır, 403 / 404 sonraki
    adaya geçer, öteki hatalar yeniden denenir. Yuvanın dosyası zaten varsa istek atılmaz. Bulunamayan yuva kaydedilir. Yalnız veri; ölçüm yok."""
    E = E or K66_ESIK; F = E["finra"]; kl = klasor or K66_YOL["finra"]; os.makedirs(kl, exist_ok=True); getir = getir or (lambda g: _k66_getir(g, E))
    say = {"yuva": 0, "vardi": 0, "yeni": 0, "istek": 0, "bulunamadi": [], "hata": []}
    for yuva, adaylar in k66_finra_adaylar(E):
        say["yuva"] += 1
        if any(os.path.exists(os.path.join(kl, f"shrt{g}.csv")) for g in adaylar):
            say["vardi"] += 1; continue
        bulundu = False
        for g in adaylar:
            son_hata: Optional[str] = None
            for k in range(int(F["deneme"])):
                try:
                    say["istek"] += 1; kod, ham = getir(g); time.sleep(float(F["bekle"]))
                except Exception as ex:   # ağ hatası: yeniden dene
                    son_hata = f"{type(ex).__name__}: {ex}"; time.sleep(2.0 * (k + 1)); continue
                if kod in (403, 404):
                    son_hata = None; break
                if kod != 200:
                    son_hata = f"HTTP {kod}"; time.sleep(2.0 * (k + 1)); continue
                try:
                    k66_finra_ayristir(ham, g)
                except K66Hata as ex:
                    son_hata = str(ex); break
                yol = os.path.join(kl, f"shrt{g}.csv")
                with open(yol + ".yarim", "wb") as f:
                    f.write(ham)
                os.replace(yol + ".yarim", yol); bulundu = True; say["yeni"] += 1
                break
            if son_hata:
                say["hata"].append(f"{g}: {son_hata}"); k66log.warning("FINRA %s: %s", g, son_hata)
            if bulundu:
                break
        if not bulundu:
            say["bulunamadi"].append(yuva)
    dosyalar = sorted(glob.glob(os.path.join(kl, "shrt????????.csv")))
    say["dosya"] = len(dosyalar); say["ilk"] = os.path.basename(dosyalar[0])[4:12] if dosyalar else None; say["son"] = os.path.basename(dosyalar[-1])[4:12] if dosyalar else None
    say["bayt"] = int(sum(os.path.getsize(y) for y in dosyalar)); say["zaman"] = _k66_simdi()
    say["sha256"] = {os.path.basename(y): _k66_dosya_sha(y) for y in dosyalar}
    K60._k60_json_yaz(os.path.join(kl, K66_DOSYA["indir"]), say)
    k66log.info("FINRA önbelleği: %d yuva, %d dosya (%s .. %s), yeni %d, istek %d, bulunamayan yuva %d", say["yuva"], say["dosya"], say["ilk"], say["son"], say["yeni"],
                say["istek"], len(say["bulunamadi"]))
    return say


def k66_finra_ayristir(ham: bytes, beklenen: Optional[str] = None) -> pd.DataFrame:
    """Bir FINRA dosyası (boru ayraçlı; tırnaklı ya da tırnaksız) -> kod, ad, sinif, si, si_once, adv, dtc_dosya, deg_yuzde, bolunme (bayrak), revizyon (bayrak).
    Başlık 14 sütun olmalı (403 / XML yanıtı reddedilir); bütün satırlarda tek ödeme günü olmalı ve dosya adındaki günle aynı olmalı. Aynı kod iki kez geçerse
    o kodun satırları atılır (attrs['yinelenen'])."""
    import csv
    metin = ham.decode("utf-8", errors="replace").lstrip("﻿")
    bas0 = metin.split("\n", 1)[0].strip(); bas = bas0.replace('"', "")
    if bas.split("|") != K66_FINRA_SUTUN:
        raise K66Hata(f"FINRA dosyası beklenen 14 sütunlu başlıkla başlamıyor ({bas[:60]!r}); 403 / XML yanıtı olabilir")
    tirnakli = bas0.startswith('"')       # yeni dosyalar tırnaklı; eski dosyalarda tırnak yok ve ad alanında tek '"' geçebilir
    try:
        D = pd.read_csv(io.StringIO(metin), sep="|", dtype=str, keep_default_na=False, quotechar='"', quoting=csv.QUOTE_MINIMAL if tirnakli else csv.QUOTE_NONE)
    except (pd.errors.ParserError, ValueError) as ex:
        raise K66Hata(f"FINRA dosyası ayrıştırılamadı: {str(ex)[:120]}")
    if not tirnakli:
        D = D.apply(lambda s: s.str.strip())
    if list(D.columns) != K66_FINRA_SUTUN:
        raise K66Hata("FINRA dosyası sütunları beklenen gibi değil")
    od = pd.to_datetime(D.settlementDate.str.strip(), format="%Y-%m-%d", errors="coerce")
    if not len(D) or od.isna().any() or od.nunique() != 1:
        raise K66Hata("FINRA dosyasında ödeme günü boş / bozuk ya da birden fazla")
    if beklenen is not None and od.iloc[0] != pd.Timestamp(beklenen):
        raise K66Hata(f"FINRA dosyasının ödeme günü ({od.iloc[0].date()}) dosya adındakiyle ({beklenen}) aynı değil")

    def say(c: str) -> np.ndarray:
        return pd.to_numeric(D[c].str.replace(",", "", regex=False).str.strip(), errors="coerce").to_numpy(float)
    X = pd.DataFrame({"kod": D.symbolCode.str.strip().str.upper(), "ad": D.issueName.str.strip(), "sinif": D.marketClassCode.str.strip(), "si": say("currentShortPositionQuantity"),
                      "si_once": say("previousShortPositionQuantity"), "adv": say("averageDailyVolumeQuantity"), "dtc_dosya": say("daysToCoverQuantity"),
                      "deg_yuzde": say("changePercent"), "bolunme": D.stockSplitFlag.str.strip().ne("").to_numpy(), "revizyon": D.revisionFlag.str.strip().ne("").to_numpy()})
    X = X[X.kod != ""]; yin = X.kod.duplicated(keep=False)
    X = X[~yin].reset_index(drop=True)
    X.attrs["odeme"] = od.iloc[0]; X.attrs["yinelenen"] = int(yin.sum())
    return X


def k66_isim_anahtari(ad: Any) -> str:
    """Şirket adının ilk anlamlı kelimesi (küçük harf, yalnız harf / rakam; baştaki 'the' atılır). Örn. 'Agilent Technologies Inc.' -> 'agilent'."""
    t = re.sub(r"[^a-z0-9 ]", "", str(ad).lower()).split()
    if t and t[0] == "the":
        t = t[1:]
    return t[0] if t else ""


def k66_finra_kodu(sembol: str) -> str:
    """V_ABD sembolü -> FINRA kodu: büyük harf, harf / rakam dışı karakterler atılır (BRK-B -> BRKB; FINRA sınıf kodlarını ayraçsız yazar)."""
    return re.sub(r"[^A-Z0-9]", "", str(sembol).upper())


def k66_finra_panel(semboller: List[str], klasor: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """FINRA dosyaları -> rapor x hisse matrisleri (rapor = ödeme gününe göre sıralı dosyalar): si, si_once, adv, dtc_dosya, deg_yuzde, bolunme, revizyon, otc, var
    (satır var), isim_ok (BİLGİ: satırdaki ad anahtarı sembolün kesik öncesi son dosyadaki ad anahtarıyla aynı; karara girmez, kimlik denetimi k66_kimlik'tir).
    Aynı FINRA koduna eşlenen iki sembol (çakışma) dışarıda bırakılır. Döner: matrisler + odeme + özet."""
    E = E or K66_ESIK; F = E["finra"]; kl = klasor or K66_YOL["finra"]; S = list(semboller); N = len(S)
    dosyalar = sorted(glob.glob(os.path.join(kl, "shrt????????.csv")))
    if not dosyalar:
        raise K66Hata(f"FINRA önbelleği boş: {kl} (önce `python K66.py indir`)")
    kod: Dict[str, List[int]] = {}
    for j, s in enumerate(S):
        kod.setdefault(k66_finra_kodu(s), []).append(j)
    cak = sorted(k for k, v in kod.items() if len(v) > 1); ix = {k: v[0] for k, v in kod.items() if len(v) == 1}
    R = len(dosyalar); M = {k: np.full((R, N), np.nan) for k in ("si", "si_once", "adv", "dtc_dosya", "deg_yuzde")}
    B = {k: np.zeros((R, N), bool) for k in ("bolunme", "revizyon", "otc", "var")}; anahtar = np.full((R, N), "", object); odeme = []; h = hashlib.sha256()
    oz: Dict[str, Any] = {"dosya": R, "satir": 0, "yinelenen": 0, "cakisan_kod": cak}
    for r, y in enumerate(dosyalar):
        ad = os.path.basename(y)
        with open(y, "rb") as f:
            ham = f.read()
        h.update(ad.encode()); h.update(hashlib.sha256(ham).hexdigest().encode())
        try:
            X = k66_finra_ayristir(ham, ad[4:12])
        except K66Hata as ex:
            raise K66Hata(f"{ad}: {ex}")
        odeme.append(np.datetime64(X.attrs["odeme"].date(), "D")); oz["satir"] += len(X); oz["yinelenen"] += X.attrs["yinelenen"]
        X = X[X.kod.isin(ix)]
        j = X.kod.map(ix).to_numpy(int)
        for k in M:
            M[k][r, j] = X[k].to_numpy(float)
        B["bolunme"][r, j] = X.bolunme.to_numpy(bool); B["revizyon"][r, j] = X.revizyon.to_numpy(bool); B["otc"][r, j] = (X.sinif == "OTC").to_numpy(bool)
        B["var"][r, j] = True; anahtar[r, j] = [k66_isim_anahtari(a) for a in X.ad]
    od = np.array(odeme, "datetime64[D]")
    if (np.diff(od) <= np.timedelta64(0, "D")).any():
        raise K66Hata("FINRA ödeme günleri artan sırada değil (aynı günün iki dosyası olabilir)")
    kriz = np.datetime64(E["kriz"], "D"); ref = np.full(N, "", object); son_r = np.full(N, -1)
    for r in range(R):
        if od[r] <= kriz:
            m = B["var"][r]; ref[m] = anahtar[r, m]; son_r[m] = r
    isim_ok = B["var"] & (anahtar == ref[None, :]) & (ref[None, :] != "")
    out = {**M, **B, "isim_ok": np.asarray(isim_ok, bool), "odeme": od, "sembol": S, "icerik_sha256": h.hexdigest()}
    oz.update({"ilk": str(od[0]), "son": str(od[-1]), "eslesen_sembol": int(B["var"].any(axis=0).sum()), "isim_ok_sembol": int(isim_ok.any(axis=0).sum()),
               "eslesen_satir": int(B["var"].sum()), "isim_uyusmaz_satir": int((B["var"] & ~isim_ok).sum()), "otc_satir": int((B["var"] & B["otc"]).sum()),
               "revizyon_satir": int((B["var"] & B["revizyon"]).sum()), "bolunme_bayrak_satir": int((B["var"] & B["bolunme"]).sum()),
               "dtc_taban_pay": float(((M["dtc_dosya"] <= 1.0) & B["var"]).sum() / max(int(B["var"].sum()), 1)),
               "adv_sifir_pay": float(((M["adv"] <= 0) & B["var"]).sum() / max(int(B["var"].sum()), 1))})
    out["ozet"] = oz
    return out


# ---------------------------------------------------------------- 2) BİLGİ TARİHİ ve DEĞİŞKENLER (yalnız t ve öncesi bilinen)
def k66_hacim_matris(V: Dict[str, pd.DataFrame], takvim: pd.DatetimeIndex, semboller: List[str]) -> np.ndarray:
    """Takvim x hisse günlük hacim (V_ABD; işlem görmediği gün NaN)."""
    tv = takvim.to_numpy("datetime64[ns]"); out = np.full((len(takvim), len(semboller)), np.nan)
    for j, s in enumerate(semboller):
        d = V[s]; p = np.searchsorted(tv, d.index.to_numpy("datetime64[ns]")); ok = (p < len(tv))
        ok[ok] &= tv[p[ok]] == d.index.to_numpy("datetime64[ns]")[ok]
        out[p[ok], j] = d.Volume.to_numpy(float)[ok]
    return out


def k66_kimlik(Fp: Dict[str, Any], hacim: np.ndarray, takvim: pd.DatetimeIndex, bol: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Tuple[np.ndarray, np.ndarray]:
    """KİMLİK DENETİMİ (rapor x hisse): FINRA satırının şirketi V_ABD fiyat serisinin şirketiyle aynı mı? Oran = ADV(r) x b(r) / V_ABD ortalama günlük hacmi
    (önceki dosyanın ödeme gününden SONRAKİ ilk işlem gününden bu ödeme gününe kadar, dahil; ilk dosyada ödeme - ilk_gun takvim günü; en az min_bar bar);
    b = ödeme gününden sonraki bölünmelerin çarpımı (V_ABD hacmi bugünkü pay biriminde). 1 / bant <= oran <= bant ise satır kabul. Yalnız ödeme günü ve öncesi
    hacim kullanılır (geleceğe bakmaz). ADV = 0 ya da hacim yoksa denetlenemez -> red. Döner (kabul, log10 oran)."""
    E = E or K66_ESIK; Kc = E["finra"]["kimlik"]; od = Fp["odeme"]; S = Fp["sembol"]; R, N = Fp["si"].shape; tv = takvim.to_numpy("datetime64[D]")
    bas = np.r_[od[:1] - np.timedelta64(int(Kc["ilk_gun"]), "D"), od[:-1]] if R else od
    a = np.searchsorted(tv, bas, side="right"); b = np.searchsorted(tv, od, side="right")
    cs = np.vstack([np.zeros((1, N)), np.nancumsum(hacim, axis=0)]); cn = np.vstack([np.zeros((1, N)), np.cumsum(np.isfinite(hacim), axis=0)])
    top = cs[b] - cs[a]; say = cn[b] - cn[a]
    carp = np.ones((R, N))
    for j, s in enumerate(S):
        if bol.get(s) is not None:
            carp[:, j] = K59.k59_bolunme_carpan(bol[s], od.astype("datetime64[ns]"))
    with np.errstate(invalid="ignore", divide="ignore"):
        ort = np.where(say >= int(Kc["min_bar"]), top / np.maximum(say, 1), np.nan)
        lo = np.log10(Fp["adv"] * carp / ort)
    ok = Fp["var"] & np.isfinite(lo) & (np.abs(lo) <= np.log10(float(Kc["bant"])))
    return ok, np.where(Fp["var"], lo, np.nan)


def k66_bilgi_indeksi(odeme: np.ndarray, takvim: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Her raporun BİLGİ GÜNÜ (takvim indeksi) = ödeme gününün takvimdeki yeri (ödeme günü işlem günü değilse sonraki ilk işlem günü) + bilgi_gecikme_islem.
    Takvimin dışına düşen rapor hiç kullanılmaz (indeks >= len(takvim))."""
    g = int((E or K66_ESIK)["finra"]["bilgi_gecikme_islem"])
    p = np.searchsorted(takvim.to_numpy("datetime64[D]"), np.asarray(odeme, "datetime64[D]"), side="left")
    return p.astype(int) + g


def k66_son_rapor(bilgi_idx: np.ndarray, G: int) -> np.ndarray:
    """Her takvim günü i için kullanılabilen SON rapor r0(i) = bilgi_idx[r] < i olan en büyük r (yoksa -1). bilgi_idx artan olmalı."""
    b = np.asarray(bilgi_idx, int)
    if len(b) > 1 and (np.diff(b) < 0).any():
        raise K66Hata("bilgi günleri artan sırada değil")
    return np.searchsorted(b, np.arange(G), side="left").astype(int) - 1


def k66_bolunme_say(bol: Optional[Tuple[np.ndarray, np.ndarray]], gunler: np.ndarray) -> np.ndarray:
    """Her gün için o güne kadar (dahil) olan bilinen bölünme sayısı (aralıktaki bölünme = iki ucun farkı)."""
    if bol is None or not len(bol[0]):
        return np.zeros(len(gunler), int)
    return np.searchsorted(np.asarray(bol[0], "datetime64[ns]"), np.asarray(gunler, "datetime64[ns]"), side="right").astype(int)


def k66_rapor_olculeri(Fp: Dict[str, Any], bol: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """Rapor x hisse düzeyinde ölçüler (henüz bilgi tarihi uygulanmamış): SIb (bugünkü pay birimine bölünme düzeltmeli açık pozisyon), DTC, SI_DEG, SI_DEG1.
    Yalnız kimlik denetiminden (k66_kimlik; Fp['kimlik_ok']) geçen satırlar."""
    E = E or K66_ESIK; F = E["finra"]; od = Fp["odeme"]; S = Fp["sembol"]; R, N = Fp["si"].shape; k = int(F["deg_rapor"])
    carp = np.ones((R, N)); nb = np.zeros((R, N), int)
    for j, s in enumerate(S):
        if bol.get(s) is not None:
            carp[:, j] = K59.k59_bolunme_carpan(bol[s], od.astype("datetime64[ns]")); nb[:, j] = k66_bolunme_say(bol[s], od)
    if "kimlik_ok" not in Fp:
        raise K66Hata("FINRA panelinde kimlik denetimi yok (k66_kimlik çağrılmadı)")
    ok = Fp["var"] & Fp["kimlik_ok"]; si, adv = Fp["si"], Fp["adv"]
    with np.errstate(invalid="ignore", divide="ignore"):
        SIb = np.where(ok & np.isfinite(si) & (si >= 0), si * carp, np.nan)
        DTC = np.where(ok & np.isfinite(adv) & (adv > 0) & np.isfinite(si) & (si >= 0), si / adv, np.nan)
        DEG = np.full((R, N), np.nan); DEG1 = np.full((R, N), np.nan)
        if R > k:
            a, b = SIb[k:], SIb[:-k]; bay = np.zeros((R - k, N), bool)
            for d in range(k):
                bay |= Fp["bolunme"][k - d:R - d] & Fp["var"][k - d:R - d]
            duzelmez = bay & ((nb[k:] - nb[:-k]) == 0)
            DEG[k:] = np.where(np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0) & ~duzelmez, np.log(np.where((a > 0) & (b > 0), a / np.where(b > 0, b, 1.0), 1.0)), np.nan)
        if R > 1:
            so, dy = Fp["si_once"][1:], Fp["deg_yuzde"][1:]
            g1 = ok[1:] & np.isfinite(so) & (so > 0) & np.isfinite(dy) & ~Fp["bolunme"][1:] & ((nb[1:] - nb[:-1]) == 0)
            DEG1[1:] = np.where(g1, dy / 100.0, np.nan)
    return {"SIb": SIb, "DTC": DTC, "SI_DEG": DEG, "SI_DEG1": DEG1}


def k66_pay_matris(T: Optional[Dict[str, Any]], gunD: np.ndarray, S: List[str], bol: Dict[str, Any], parca: int = 250) -> np.ndarray:
    """Gün x hisse: o gün bilinen toplam pay (K60.k60_pay; bugünkü pay birimi; K64.k64_kalite PAY_D ile aynı çağrı). T yoksa NaN."""
    G, N = len(gunD), len(S); out = np.full((G, N), np.nan)
    if T is None:
        return out
    Bg = K60.K60_ESIK["bilgi"]; Dl = {"temel": T, "bolunme": bol or {}}
    for a in range(0, G, parca):
        g = np.asarray(gunD[a:a + parca], "datetime64[D]"); AO = K60._K60Temel(T, g, N, Bg)
        s1, _k = K60.k60_pay(Dl, {"U": np.zeros((len(g), N), bool), "mtD": g, "sembol": S}, AO, K60.K60_ESIK)
        out[a:a + len(g)] = s1
    return out


def k66_degiskenler(Fp: Dict[str, Any], takvim: pd.DatetimeIndex, pay: np.ndarray, bol: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
    """Gün x hisse değişken matrisleri: gün i'de yalnız bilgi_idx < i olan SON rapor r0(i) kullanılır (sembolün r0'da satırı yoksa değer yok; daha eski rapora
    düşülmez). SI_PAY paydası o gün bilinen pay. Döner (matrisler, bilgi: r0, bilgi_idx)."""
    E = E or K66_ESIK; F = E["finra"]; G = len(takvim)
    if list(Fp["sembol"]) and pay.shape != (G, len(Fp["sembol"])):
        raise K66Hata("pay matrisi takvim x sembol boyutunda değil")
    bi = k66_bilgi_indeksi(Fp["odeme"], takvim, E); r0 = k66_son_rapor(bi, G); Ro = k66_rapor_olculeri(Fp, bol, E); m = (r0 >= 0)[:, None]; rr = np.maximum(r0, 0)
    X: Dict[str, np.ndarray] = {}
    for k in ("DTC", "SI_DEG", "SI_DEG1"):
        X[k] = np.where(m, Ro[k][rr], np.nan).astype(np.float32)
    with np.errstate(invalid="ignore", divide="ignore"):
        sp = np.where(m, Ro["SIb"][rr], np.nan) / np.where(np.isfinite(pay) & (pay > 0), pay, np.nan)
    X["SI_PAY"] = np.where(np.isfinite(sp) & (sp >= 0) & (sp <= float(F["si_pay_aykiri"])), sp, np.nan).astype(np.float32)
    return {k: X[k] for k in k66_kodlar(E)}, {"r0": r0, "bilgi_idx": bi}


def k66_pazar_hazirla(g: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """K64.k64_olay_degerleri / k64_s1 / k64_s2'nin beklediği H demeti: takvim, sembol, kol, X (4 değişken), sira (evren içi), var, rejim. Getiri HESAPLANMAZ."""
    E = E or K66_ESIK; V = g["V"]; M = K64.k64_fiyat_matrisleri(V, K64.K64_ESIK); tak = M["takvim"]; S = M["sembol"]
    if list(g["F"]["sembol"]) != list(S):
        raise K66Hata("FINRA paneli ile fiyat matrisleri aynı sembol sırasında değil")
    bol = (g.get("pay") or {}).get("bolunme") or {}
    kim, lo = k66_kimlik(g["F"], k66_hacim_matris(V, tak, S), tak, bol, E); Fp = {**g["F"], "kimlik_ok": kim}
    kozet = {"kimlik_ok_satir": int(kim.sum()), "kimlik_red_satir": int((g["F"]["var"] & ~kim).sum()), "kimlik_ok_sembol": int(kim.any(axis=0).sum()),
             "isim_uyusmaz_kimlik_ok": int((g["F"]["var"] & ~g["F"]["isim_ok"] & kim).sum()), "isim_ok_kimlik_red": int((g["F"]["isim_ok"] & ~kim).sum()),
             "log10_oran_yuzdelik": [float(x) for x in np.percentile(lo[np.isfinite(lo)], [1, 5, 50, 95, 99])] if np.isfinite(lo).any() else []}
    pay = k66_pay_matris(g.get("T"), tak.to_numpy("datetime64[D]"), S, bol)
    X, bilgi = k66_degiskenler(Fp, tak, pay, bol, E)
    sira = {k: K64.k64_sira(v, M["var"], E["sira"]["min_evren"]) for k, v in X.items()}
    return {"takvim": tak, "sembol": S, "kol": {s: j for j, s in enumerate(S)}, "X": X, "sira": sira, "var": M["var"], "rejim": K64.k64_rejim(M["C"], E),
            "bilgi": bilgi, "pay": pay, "kimlik": kozet}


# ---------------------------------------------------------------- 3) GİRDİ, OLAYLAR, KAPSAM
def k66_girdi(E: Optional[Dict[str, Any]] = None, k60_veri: Optional[Dict[str, Tuple[str, int]]] = None) -> Dict[str, Dict[str, Any]]:
    """GERÇEK girdi (yalnız önbellek; ağ yok): ABD -> {V, T, pay, F (FINRA paneli), ozet}."""
    E = E or K66_ESIK
    Va = K64.k64_fiyat_yukle("ABD", K66_YOL["veri"], E); Sa = sorted(Va); D = K60.k60_demet_yukle(k60_veri); Ta, bol, var = K64.k64_abd_temel(Sa, D)
    Fp = k66_finra_panel(Sa, None, E)
    return {"ABD": {"V": Va, "T": Ta, "pay": {"bolunme": bol, "sembol": Sa}, "F": Fp, "ozet": {"hisse": len(Sa), "demette": int(var.sum()), "finra": Fp["ozet"]}}}


def _k66_olaylar(V: Dict[str, pd.DataFrame], E: Dict[str, Any], sentetik: bool) -> Dict[str, pd.DataFrame]:
    """ANA (K24) ve İKİNCİL (D13) olaylar K64 fonksiyonlarıyla (tanımlar aynen). Gerçek veride D13 ara önbelleği: olay ayarları K64 ile aynıysa K64'ün dosyası
    (aynı fiyat + aynı COL_v1 + aynı ayar -> aynı olaylar), değilse K66'nın kendi ara klasörü."""
    out = {"K24": K64.k64_olay_k24(V, E)}
    if E["olay"]["d13"]["etkin"]:
        ara = None
        if not sentetik:
            if E["olay"] == K64.K64_ESIK["olay"] and E["kriz"] == K64.K64_ESIK["kriz"] and K66_YOL["veri"] == K64.K64_YOL["veri"]:
                ara = K64._k64_d13_ara("ABD")
            else:
                a = hashlib.sha256(json.dumps([K60._k60_sha(os.path.join(K66_YOL["veri"], "V_ABD.pkl")), K60._k60_sha(os.path.join(KOK_K66, "COL_v1.py")), E["olay"], E["kriz"]],
                                              sort_keys=True).encode()).hexdigest()[:16]
                ara = os.path.join(K66_YOL["ara"], f"d13_ABD_{a}.pkl")
        out["D13"] = K64.k64_olay_d13(V, E, None, ara)
    return out


def k66_sira_sec(K: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Tuple[str, List[Dict[str, Any]]]:
    """KARAR SIRASI SEÇİM KURALI (ölçümden önce, yalnız kapsam sayısıyla; eşikler kapsam koşulmadan yazıldı): ANA tanım, bağımsız dönemler, her değişken için
    EVREN sırasıyla ÜST ve ALT pencereli olay sayıları alınır. Bir hücrede küçük grup < n_min YA DA küçük / büyük < oran_min ise çöl olayları evren sırasında bir
    uçta TOPLANIYOR sayılır. Herhangi bir hücrede toplanma varsa aile karar sırası 'IC' (çöl içi), yoksa 'EVREN'. Döner (seçim, hücre satırları)."""
    E = E or K66_ESIK; R = E["sira_secim"]; sat = []
    A = K[(K.tanim == E["olay"]["ana"]) & (K.degisken.isin(k66_kodlar(E))) & K.donem.isin(E["bagimsiz"])]
    for r in A.itertuples():
        u, a = int(r.n_ust), int(r.n_alt); kucuk, buyuk = min(u, a), max(u, a)
        top = bool(kucuk < R["n_min"] or (buyuk > 0 and kucuk / buyuk < R["oran_min"]) or buyuk == 0)
        sat.append({"degisken": r.degisken, "donem": r.donem, "n_ust": u, "n_alt": a, "oran": (kucuk / buyuk) if buyuk else np.nan, "toplanma": top})
    if not sat:
        raise K66Hata("karar sırası seçimi için kapsam satırı yok")
    return ("IC" if any(s["toplanma"] for s in sat) else "EVREN"), sat


def k66_kapsam(cikti: Optional[str] = None, girdi: Optional[Dict[str, Dict[str, Any]]] = None, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """KAPSAM: yalnız SAYIM. Tanım x dönem: olay sayısı (ham / tekil / pencereli), her değişkenin hesaplanabildiği olay ve ÜST / ORTA / ALT sayıları (evren içi ve
    çöl içi sıra); FINRA özeti (dosya, tarih, eşleşen sembol, kimlik denetimi, isim bilgisi, revizyon / OTC satırları), evren doluluğu. Getiri, eşli fark, FI_OLCUT paneli
    HESAPLANMAZ."""
    E = E or K66_ESIK; sentetik = girdi is not None; t0 = time.time()
    girdi = girdi if sentetik else k66_girdi(E, K60.k60_veri_sha(dogrula=False))
    sat = []; ozet: Dict[str, Any] = {"zaman": _k66_simdi(), "surum": K66_SURUM, "muhur": k66_esik_sha(E), "pazar": {}}
    for pazar in E["pazar"]:
        if pazar not in girdi:
            continue
        g = girdi[pazar]; V = g["V"]; H = k66_pazar_hazirla(g, E); tak = H["takvim"]; son = len(tak) - 1; O = _k66_olaylar(V, E, sentetik)
        bi = H["bilgi"]["bilgi_idx"]; od = g["F"]["odeme"]; ok = bi < len(tak)
        gecikme = (tak[bi[ok]].to_numpy("datetime64[D]") - od[ok]).astype(int) if ok.any() else np.array([], int)
        bas2018 = tak >= pd.Timestamp(E["donem"][0][1])
        ozet["pazar"][pazar] = {**g.get("ozet", {}), "takvim_gun": len(tak), "ilk_gun": str(tak[0].date()), "son_gun": str(tak[-1].date()),
                                "k24_sapma": int(O["K24"].attrs.get("sapma", 0)), "kullanilan_rapor": int(ok.sum()), "kimlik": H["kimlik"],
                                "bilgi_gecikme_takvim_gun": {"min": int(gecikme.min()) if len(gecikme) else None, "medyan": float(np.median(gecikme)) if len(gecikme) else None,
                                                             "max": int(gecikme.max()) if len(gecikme) else None},
                                "evren_kapsam_2018": {k: float(np.isfinite(np.where(H["var"][bas2018], H["X"][k][bas2018], np.nan)).sum() / max(int(H["var"][bas2018].sum()), 1))
                                                      for k in k66_kodlar(E)}}
        for tanim, X0 in O.items():
            X = K64.k64_olay_degerleri(X0, H, tanim, E); gi = tak.get_indexer(pd.DatetimeIndex(X.giris)) if len(X) else np.array([], int)
            X["pencere"] = (gi >= 0) & (gi + FI.FI_OLCUT["ufuk"] - 1 <= son) if len(X) else []
            if tanim == "D13" and E["olay"]["d13"]["gecer"] and len(X):
                X = X[X.gecer].reset_index(drop=True)
            for dn, a, b in E["donem"]:
                md = ((X.giris >= a) & (X.giris <= b)).to_numpy() if len(X) else np.zeros(0, bool); tk = md & X.tekil.to_numpy(bool) if len(X) else md
                pn = tk & X.pencere.to_numpy(bool) if len(X) else md
                kim = {"tanim": tanim, "pazar": pazar, "donem": dn, "n_ham": int(md.sum()), "n_tekil": int(tk.sum()), "n_pencere": int(pn.sum())}
                sat.append({**kim, "degisken": "(olay)"})
                for k in k66_kodlar(E):
                    ge = K64.k64_grup(X[k + "_sira"].to_numpy(float), E) if len(X) else np.array([], str); gc = K64.k64_grup(X[k + "_ic"].to_numpy(float), E) if len(X) else ge
                    sat.append({**kim, "degisken": k, "n_deger": int((pn & np.isfinite(X[k].to_numpy(float))).sum()) if len(X) else 0,
                                "n_ust": int((pn & (ge == "UST")).sum()), "n_orta": int((pn & (ge == "ORTA")).sum()), "n_alt": int((pn & (ge == "ALT")).sum()),
                                "n_ust_ic": int((pn & (gc == "UST")).sum()), "n_orta_ic": int((pn & (gc == "ORTA")).sum()), "n_alt_ic": int((pn & (gc == "ALT")).sum())})
        k66log.info("kapsam %s: %d hisse, %d gün (%.0f sn)", pazar, len(H["sembol"]), len(tak), time.time() - t0)
    K = pd.DataFrame(sat); cik = cikti or K66_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    try:
        sec, hucre = k66_sira_sec(K, E); ozet["sira_secim"] = {"secim": sec, "hucre": hucre, "kural": E["sira_secim"]}
    except K66Hata as ex:
        ozet["sira_secim"] = {"secim": None, "neden": str(ex)}
    K.to_csv(_k66_yol("kapsam", cikti), index=False); K60._k60_json_yaz(_k66_yol("kapsam_ozet", cikti), K60._k60_yuvarla(ozet, 10))
    return K


def k66_kapsam_notu(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """Kapsam sayımının ön kayıt metnine giren özeti (yalnız SAYI). Mühre girmez."""
    E = E or K66_ESIK; yk, yo = _k66_yol("kapsam", cikti), _k66_yol("kapsam_ozet", cikti)
    if not (os.path.exists(yk) and os.path.exists(yo)):
        return "Kapsam sayımı henüz koşulmadı (`python -I K66.py kapsam`)."
    K = pd.read_csv(yk); O = K60._k60_json_oku(yo)
    par = [f"Kapsam sayımı ({O.get('zaman', '?')}; `python -I K66.py kapsam`; yalnız SAYI: getiri, eşli fark, FI_OLCUT paneli hesaplanmadı).\n"]
    for p, v in O.get("pazar", {}).items():
        f = v.get("finra") or {}; bg = v.get("bilgi_gecikme_takvim_gun") or {}; ki = v.get("kimlik") or {}
        ek = ", ".join(f"{k} %{100 * float(x):.0f}" for k, x in (v.get("evren_kapsam_2018") or {}).items())
        par.append(f"- {p}: {v.get('hisse')} hisse (K60 demetinde {v.get('demette')}), takvim {v.get('takvim_gun')} gün ({v.get('ilk_gun')} .. {v.get('son_gun')}).")
        par.append(f"- FINRA: {f.get('dosya')} dosya, ödeme günleri {f.get('ilk')} .. {f.get('son')}, toplam {f.get('satir')} satır (yinelenen kod satırı {f.get('yinelenen')}); "
                   f"V_ABD sembolü eşleşen {f.get('eslesen_sembol')} / {v.get('hisse')}; eşleşen satır {f.get('eslesen_satir')}; KİMLİK denetiminden geçen satır "
                   f"{ki.get('kimlik_ok_satir')} (en az bir satırı geçen sembol {ki.get('kimlik_ok_sembol')}), reddedilen {ki.get('kimlik_red_satir')}; log10(ADV x b / V_ABD hacmi) "
                   f"yüzdelikleri 1 / 5 / 50 / 95 / 99: {', '.join(f'{float(x):.3f}' for x in (ki.get('log10_oran_yuzdelik') or []) if x is not None)}. İsim (bilgi): adı bugünküyle uyuşmayan satır "
                   f"{f.get('isim_uyusmaz_satir')} (bunların kimliği doğrulanan {ki.get('isim_uyusmaz_kimlik_ok')}), adı uyuşup kimliği reddedilen {ki.get('isim_ok_kimlik_red')}. "
                   f"OTC sınıfı satır {f.get('otc_satir')}, revizyon bayraklı {f.get('revizyon_satir')}, "
                   f"bölünme bayraklı {f.get('bolunme_bayrak_satir')}; çakışan kod {len(f.get('cakisan_kod') or [])}. Dosyadaki DTC'nin 1,00 tabanında olduğu satır payı "
                   f"%{100 * float(f.get('dtc_taban_pay') or 0):.1f}; ADV = 0 payı %{100 * float(f.get('adv_sifir_pay') or 0):.1f}.")
        par.append(f"- Bilgi tarihi: takvim içinde kullanılan rapor {v.get('kullanilan_rapor')}; ödeme günü -> bilgi günü takvim günü farkı en az {bg.get('min')}, medyan "
                   f"{bg.get('medyan')}, en çok {bg.get('max')}. Evren hisse-günlerinde (2018-01-01 ->) değişken doluluk: {ek}.")
    for tanim in K.tanim.unique():
        par.append(f"\n**{tanim} olayları** (ham = tekilleştirme öncesi; tekil = 60 işlem günü kuralı sonrası; pencere = 60 günlük penceresi 31.08.2026 kesiğinden önce biten tekil olay"
                   + ("; D13'te yalnız GECER" if tanim == "D13" else "") + ")\n\n| pazar | dönem | ham | tekil | pencere |\n|---|---|---|---|---|")
        for r in K[(K.tanim == tanim) & (K.degisken == "(olay)")].itertuples():
            par.append(f"| {r.pazar} | {r.donem} | {int(r.n_ham)} | {int(r.n_tekil)} | {int(r.n_pencere)} |")
        par.append(f"\n**{tanim}: değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; EVREN = aynı gün evren içi sıra, İÇ = çöl içi sıra; hücre = değer / ÜST / ALT)\n\n"
                   "| değişken | sıra | " + " | ".join(f"{p} {d[0]}" for p in E["pazar"] for d in E["donem"]) + " |\n|---|---|" + "---|" * (len(E["pazar"]) * len(E["donem"])))
        for k in k66_kodlar(E):
            for st, u, al in (("EVREN", "n_ust", "n_alt"), ("İÇ", "n_ust_ic", "n_alt_ic")):
                h = []
                for p in E["pazar"]:
                    for d in E["donem"]:
                        x = K[(K.tanim == tanim) & (K.pazar == p) & (K.donem == d[0]) & (K.degisken == k)]
                        h.append("—" if not len(x) else f"{int(x.n_deger.iloc[0])} / {int(x[u].iloc[0])} / {int(x[al].iloc[0])}")
                par.append(f"| {k} | {st} | " + " | ".join(h) + " |")
    sec = (O.get("sira_secim") or {})
    if sec.get("hucre"):
        par.append("\n**Karar sırası seçim kuralı uygulaması** (ANA tanım, bağımsız dönemler, EVREN sırası; toplanma = küçük grup < "
                   f"{E['sira_secim']['n_min']} ya da küçük / büyük < {E['sira_secim']['oran_min']}): "
                   + "; ".join(f"{h['degisken']} {h['donem']} ÜST {h['n_ust']} / ALT {h['n_alt']} (oran {float(h['oran']):.2f}{', TOPLANMA' if h['toplanma'] else ''})" for h in sec["hucre"])
                   + f". Kuralın sonucu: **{'İÇ' if sec.get('secim') == 'IC' else 'EVREN'}**.")
    st = list(E["sira"]["karar"].values())[0]
    A = K[(K.tanim == E["olay"]["ana"]) & (K.degisken != "(olay)") & K.donem.isin(E["bagimsiz"])]
    az = [f"{r.degisken} {r.donem} (ÜST {int(r.n_ust_ic if st == 'IC' else r.n_ust)}, ALT {int(r.n_alt_ic if st == 'IC' else r.n_alt)})" for r in A.itertuples()
          if min(int(r.n_ust_ic if st == "IC" else r.n_ust), int(r.n_alt_ic if st == "IC" else r.n_alt)) < E["s1"]["n_esik"]]
    par.append(f"\nANA tanım, KARAR sırası ({'İÇ' if st == 'IC' else 'EVREN'}), bağımsız dönemlerde grubu n < {E['s1']['n_esik']} olan (karar kuralında 'ÖLÇÜLEMEZ' kalacak) hücreler "
               "(pencereli olay sayısıyla; ölçülebilen olay daha az olabilir): " + ("; ".join(az) if az else "yok") + ".")
    return "\n".join(par)


# ---------------------------------------------------------------- 4) ÖN KAYIT
def k66_veri_sha(finra: Optional[str] = None) -> Dict[str, Tuple[str, int]]:
    """Koşunun okuyacağı verinin ve içe alınan kodun / tasarımın sha256'ları: ad -> (sha256, dosya sayısı). Eksik dosyada durur. K60 önbellekleri K60 ön kaydıyla
    doğrulanır (`kos` başında K60.k60_onkayit_dogrula veri=True)."""
    sha = K60._k60_sha; out: Dict[str, Tuple[str, int]] = {}
    y = os.path.join(K66_YOL["veri"], "V_ABD.pkl")
    if not os.path.exists(y):
        raise K66Hata(f"fiyat verisi yok: {y}")
    out["V_ABD.pkl"] = (sha(y), 1)
    kl = finra or K66_YOL["finra"]; dos = sorted(glob.glob(os.path.join(kl, "shrt????????.csv")))
    if not dos:
        raise K66Hata(f"FINRA önbelleği boş: {kl}")
    h = hashlib.sha256()
    for d in dos:
        h.update(os.path.basename(d).encode()); h.update(sha(d).encode())
    out["k66_finra"] = (h.hexdigest(), len(dos))
    for ad, yol in (("K60_ON_KAYIT.md", K60._k60_yol("onkayit")), ("K64_K65_ON_KAYIT.md", K64._k64_yol("onkayit"))):
        if not os.path.exists(yol):
            raise K66Hata(f"içe alınan ön kayıt yok: {yol}")
        out[ad] = (sha(yol), 1)
    for a in ("FON_IZI.py", "K60.py", "K59.py", "COL_v1.py", "K64.py"):
        y = os.path.join(KOK_K66, a)
        if not os.path.exists(y):
            raise K66Hata(f"içe alınan kod dosyası yok: {y}")
        out[a] = (sha(y), 1)
    return out


def k66_onkayit_metin(zaman: str, veri_sha: Dict[str, Tuple[str, int]], kapsam: str, E: Optional[Dict[str, Any]] = None, secim: str = "") -> str:
    E = E or K66_ESIK; O = E["olay"]; S = E["sira"]; S1 = E["s1"]; F = E["finra"]; FO = FI.FI_OLCUT; K24 = FI.FI_K24; RS = E["sira_secim"]
    st = S["karar"]["K66"]; stad = "İÇ (çöl içi sıra)" if st == "IC" else "EVREN (aynı gün evren içi sıra)"; oteki = "EVREN" if st == "IC" else "İÇ"
    vs = "\n".join(f"- {k}: sha256 {v[0]} ({v[1]} dosya)" for k, v in veri_sha.items()) or "- (veri dosyası bulunamadı)"
    dg = "\n".join(f"| {d['kod']} | {d['tanim']} | {d['kaynak']} |" for d in E["degisken"])
    dn = ", ".join(f"{a} ({b} .. {c})" for a, b, c in E["donem"]); m = len(E["degisken"]) * 2 * len(E["pazar"]) * len(E["bagimsiz"])
    return f"""# K66 — ABD AÇIĞA SATIŞ TALEBİ ÇÖL SİNYALİNE EK BİLGİ TAŞIYOR MU: ÖN KAYIT (ölçümden ÖNCE)

{K66_SURUM}
Yazım zamanı: {zaman}
ESIK_SHA256: {k66_esik_sha(E)}

Bu dosya gerçek veride değişkene bağlı HİÇBİR getiri / eşli fark hesaplanmadan yazıldı (yalnız `indir` ve `kapsam` sayımı koşuldu: §12). `python -I K66.py kos`
bu dosya git'e işlenmeden, mühür ya da veri sha256'ları tutmadan çalışmaz. Sonuç görüldükten sonra yeni kural eklenmez. Tasarım K64_K65_ON_KAYIT.md ile aynıdır
(K64.py fonksiyonları içe alınır, kopyalanmaz; K64.py değişmez); burada yalnız farklar ve yeni değişkenler tam yazılır.

## Veri (sha256; `kos` başında yeniden hesaplanır, farklıysa koşu durur)
{vs}
K60 önbellekleri (/tmp/k60_fiyat, /tmp/k60_secframes ...; pay sayısı ve bölünmeler) K60 ön kaydındaki sha256'larla doğrulanır (K60.k60_onkayit_dogrula, veri = True).
K60 mührü ve K64 mührü bu işin mührüne girer.

## 0. Soru (Cemal'in isteği; ana oturum iş tanımı K66)
Çöl tanımı ve mevcut cetvel DEĞİŞMEZ. ABD açığa satış talebi (FINRA açık pozisyon: oran, kapatma günü, değişim) mevcut ÇÖL sinyaline EK BİLGİ taşıyor mu? Her
değişken tek tek ve İKİ YÖNDE sınanır; katkı değişkensiz temel modele (yalnız çöl) karşı ölçülür. Üretim koduna ekleme yapılmaz.
EVREN: yalnız ABD. **BIST VERİSİ YOK**: BIST'te açığa satış 2020'den beri yalnız BIST-30 / 50 hisselerinde (yasak dönemlerinde hiç) var, açık pozisyon yayını yok (K63);
çöl evreni (küçük hisseler) için ölçülemez. ABD bulgusu BIST'e genellenmez.
**ÖDÜNÇ ÜCRETİ / KULLANILABİLİR ADET / KULLANIM ORANI: VERİ YOK** (ücretsiz tarihsel kaynak yok, K63; ücretli: IBorrowDesk API 29 $/ay; karar Cemal'de). Vekil uydurulmadı.

## 1. Olay (K64_K65_ON_KAYIT.md §1 AYNEN; K64.k64_olay_k24 / k64_olay_d13 çağrılır)
- ANA: K24 'iki evre' çöl sinyali — FON_IZI.fi_k24_tara, FI_K24 = {json.dumps(K24, ensure_ascii=False)}. Sinyal günü t; giriş = hissenin t'den sonraki ilk işlem
  günü açılışı. TEKİLLEŞTİRME: son TUTULAN sinyalden en az {O['tekil_gun']} işlem günü sonra gelen ilk sinyal (FI_K24 'tekrar' = 60 ile birebir; kodda denetlenir).
- İKİNCİL (sağlamlık; BH ailesine ve karara GİRMEZ): üretim D13 + AL kırılımı (COL_v1.col_olc, haftalık tespit ızgarası, GECER şartı; K64 §1 (ii) aynen).
  Gerçek veride D13 olayları K64'ün ara önbelleğinden okunur (aynı fiyat dosyası + aynı COL_v1.py + aynı olay ayarı -> aynı olaylar; dosya adı bunların sha256'sıdır).

## 2. Evren, veri ve BİLGİ TARİHİ
- Fiyat: V_ABD.pkl (islenmis-veri dalı; 1.411 hisse; K24 cetvelinin evreni). Fon krizi: {E['kriz']} sonrası barlar atılır; 60 günlük penceresi bu tarihi aşan olay ölçülmez.
- AÇIK POZİSYON: FINRA iki haftalık açık pozisyon dosyaları (Rule 4560; borsa kotlu + OTC): `{F['url'].format(g='YYYYMMDD')}`, ücretsiz, anahtarsız;
  en eski erişilebilen {F['ilk']} (daha eskisi 403; K63), son indirilen ödeme günü <= {F['son']}. 14 sütun: {', '.join(K66_FINRA_SUTUN)}.
  Ödeme (settlement) günleri: ayın 15'i (ödeme günü değilse önceki ödeme günü) ve ayın son ödeme günü. `indir` her yuva için hafta içi adayları (15'inden ve ayın son
  gününden geriye {F['aday_gun']} gün) sırayla dener; 403 / 404 sonraki adaya geçer; dosya 14 sütunlu başlık ve tek, dosya adıyla aynı ödeme günü taşımalıdır.
- **BİLGİ TARİHİ (geleceğe bakma kuralı):** bir raporun bilgi günü = ödeme gününün ABD işlem takvimindeki yeri (ödeme günü işlem günü değilse sonraki ilk işlem günü)
  + **{F['bilgi_gecikme_islem']} işlem günü**; t günü yalnız **bilgi günü < t** olan raporlar kullanılır ve bunların EN SONUNCUSU (r0) alınır. Sembolün r0'da satırı yoksa
  değer YOK sayılır (daha eski rapora düşülmez). İşlem takvimi = V_ABD birleşik işlem günleri (FI_OLCUT panelinin takvimi).
  KAYNAK: FINRA 'About Equity Short Interest' ve 'Equity Short Interest Data Glossary' (finra.org/finra-data/browse-catalog/equity-short-interest): veriler 'ödeme
  gününden sonraki 7. iş gününde yayına verilir'; aracı kurumlar ödeme gününden sonraki 2. iş günü 18:00 ET'ye kadar bildirir (Rule 4560); FINRA 2026 takvimi
  (finra.org/filing-reporting/regulatory-filing-systems/short-interest; ör. 15.01.2026 -> 27.01.2026, 15.05.2026 -> 27.05.2026: 7. iş günü); SR-FINRA-2026-012
  ('yayın ödemeden 7 iş günü sonra'). Eski yıllarda yayının 8. iş günü olduğuna dair ikincil (doğrulanamayan) kaynak var. Dosya bazında gerçek yayın günü
  BULUNAMADI (CDN 'Last-Modified' alanı yeniden yükleme günüdür: shrt20180112.csv için 2023-07-27). Bu yüzden iş tanımındaki TUTUCU kural uygulandı: 12 işlem
  günü (7-8 iş gününe en az 4 işlem günü pay; yayın akşam olsa bile t günü kapanışında bilinir).
- REVİZYON: CDN dosyaları revizyonları içerir ('revisionFlag' = R; ilk yayımlanan değer elde yok). Revizyonlu satırlar kullanılır (sayısı §12'de); revizyon günü
  bilinmediği için küçük bir geleceğe bakma riski beyan edilir (§10).
- SEMBOL EŞLEMESİ: FINRA kodu = V_ABD sembolü (büyük harf, harf / rakam dışı karakterler atılır; V_ABD'de böyle karakter yok). İki V_ABD sembolü aynı koda düşerse ikisi de
  dışarıda kalır. **KİMLİK DENETİMİ** (k66_kimlik): FINRA satırının şirketi V_ABD fiyat serisinin şirketiyle aynı olmalı (V_ABD serisinin kimliği BUGÜNKÜ şirkettir; kod
  daha önce başka şirkete aitse eski satırlar başka şirketindir). Ölçü: oran = ADV(r) x b(r) / V_ABD ortalama günlük hacmi (önceki dosyanın ödeme gününden sonraki ilk
  işlem gününden bu ödeme gününe kadar, dahil = FINRA ADV'nin kendi penceresi; ilk dosyada ödeme - {F['kimlik']['ilk_gun']} takvim günü; en az {F['kimlik']['min_bar']} bar;
  b = ödeme gününden sonraki bölünme çarpanı, V_ABD hacmi bugünkü birimdedir). **1 / {F['kimlik']['bant']:g} <= oran <= {F['kimlik']['bant']:g}** ise satır kabul; değilse ya da
  denetlenemiyorsa (ADV = 0, hacim yok) satır YOK. Yalnız ödeme günü ve öncesi hacim kullanılır: geleceğe bakmaz. Şirket adı yalnız BİLGİ olarak sayılır (§12).
  Pazar sınıfı süzgeci yok (OTC'den borsaya geçen şirketin OTC dönemi satırları da, kimliği doğrulanırsa, kullanılır; sayısı §12'de).
- PAY SAYISI: K60 demetindeki 'o gün bilinen' pay okuyucusu K60.k60_pay (K64 PAY_D ile aynı çağrı; kapak sayısı, yoksa bölünmesiz hissede bilanço / ağırlıklı
  ortalama pay; bilgi tarihi < t; BUGÜNKÜ pay biriminde). Halka açık pay (float) verisi YOK: oran toplam paya göredir (beyan; float'a göre oranlardan küçüktür).
- BÖLÜNME: K60 demetinin bölünme kayıtları (tarih, oran). Açık pozisyon bugünkü pay birimine çevrilir: SI x b(ödeme günü), b = ödeme gününden SONRAKİ bölünme
  oranlarının çarpımı (K59.k59_bolunme_carpan). SI_PAY'de pay da bugünkü birimde olduğundan t'den sonraki bölünmeler oranda sadeleşir (geleceğe bakmaz).

## 3. Değişkenler (hepsi yalnız t ve öncesi bilinen raporlarla; r0 = bilgi günü < t olan son rapor, r0 - k = ondan k önceki rapor (bütün dosyalar sırasında))
| kod | tanım | beklenti (bilgi) |
|---|---|---|
{dg}

Beklenti sütunu bilgidir: her değişken İKİ YÖNDE sınanır. DTC dosyadaki 'daysToCoverQuantity' alanının formülüdür (SI / ADV); dosya alanı <= 1 değerleri 1,00'a
basar ve ADV = 0'da 999,99 yazar, bu yüzden aynı iki alandan yeniden hesaplanır (SAPMA 1). SI_DEG1 dosyadaki 'changePercent' alanıdır.

## 4. S1 — 'etkileşim / ek katkı' (asıl soru; K64 §4 aynen, K64.k64_s1)
- Örneklem: yalnız ÇÖL OLAYLARI (tekil; FI_OLCUT ile ölçülebilen). 'EVREN' sırası = aynı gün evren içi yüzdelik sıra (n >= {S['min_evren']}); 'İÇ' sırası = sinyal günü
  [t - {S['ic_gun']} gün, t] aralığındaki tekil çöl olayları (kendisi dahil, n >= {S['ic_min']}) içindeki sıra. ÜST = sıra >= 2/3, ALT = sıra <= 1/3.
- **KARAR SIRASI: {stad}** (bütün K66 ailesi için). {oteki} sırası 'sağlamlık, karar dışı' (karara ve BH ailesine GİRMEZ).
  SEÇİM KURALI (eşikler kapsam sayımı KOŞULMADAN koda yazıldı; k66_sira_sec): ANA tanım, bağımsız dönemler, her değişken için EVREN sırasıyla pencereli ÜST ve ALT olay
  sayısı; bir hücrede küçük grup < {RS['n_min']} ya da küçük / büyük < {RS['oran_min']} ise çöl olayları evren sırasında bir uçta TOPLANIYOR; herhangi bir hücrede toplanma
  varsa İÇ, yoksa EVREN. Uygulama: {secim or 'kapsam sayımı yok'}. Ayrıntı §12'de. **Kapsam sayımı görüldü, getiri görülmedi** (hiçbir getiri / eşli fark hesaplanmadı). `onkayit` kapsam
  dosyasındaki kural sonucu ile mühürdeki karar sırası aynı değilse yazmaz.
- Temel model = hücredeki BÜTÜN çöl olayları (değişkensiz). ÜST - ALT = ortalama eşli farkların farkı; ay kümeli bootstrap ({S1['bootstrap']} çekiliş, tohum {S1['tohum']};
  iki grubu dolu çekiliş payı < %{100 * S1['gecerli_pay']:.0f} ise aralık yok); %95 aralık = {S1['guven'][0]} / {S1['guven'][1]} yüzdelikleri.
- **'EK KATKI VAR (yön ÜST)'** <=> n_ÜST >= {S1['n_esik']} ve n_ALT >= {S1['n_esik']} VE ÜST grubunun ortalama eşli farkı > temel modelin VE (ÜST - ALT) %95 alt sınırı > 0.
  **'EK KATKI VAR (yön ALT)'** ayna: ALT grubunun ortalama eşli farkı > temel VE (ÜST - ALT) %95 üst sınırı < 0.

## 5. S2 — 'tek başına' (bilgi; K64 §5 aynen, K64.k64_s2)
Çöl DIŞI evrende, ANA çöl sinyali olan günlerde, değişkenin evren içi ÜST / ALT üçte birindeki hisselerin (giriş = ertesi takvim günü açılışı) 60 günlük eşli farkı ve
ÜST - ALT (ay kümeli bootstrap; {E['s2']['bootstrap']} çekiliş, tohum {E['s2']['tohum']}). 'Çöl dışı' = o gün ve önceki {O['tekil_gun'] - 1} işlem gününde tekil ANA çöl sinyali vermemiş hisse.

## 6. Cetvel (FON_IZI FI_OLCUT aynen; K64 §6 aynen)
FI_OLCUT = {json.dumps({k: v for k, v in FO.items() if k not in ('donem', 'karar')}, ensure_ascii=False)}.
- fi_olcut_panel / fi_olcut_olay / fi_olcut_hucre (K64.k64_olc, k64_hucre): giriş = sinyalden sonraki ilk işlem günü açılışı; r60; EŞLİ FARK = r60 - aynı giriş günü aynı
  momentum beşliği x likidite üçlüsü hücresindeki öteki hisselerin ortalama r60'ı; HÜCRE TUTAR <=> n >= {FO['n_esik']}, aralığın alt ucu > 0, ortalama sıra > 0,50, portföy >
  rastgele %90. Piyasa koşulu katmanı (eşit ağırlıklı evren endeksi {E['piyasa']['sma']} günlük ortalamasının üstü / altı; bilgi). Ek ufuk r20 (bilgi).
- MALİYET: ABD gidiş-dönüş {1e4 * E['maliyet']['ABD']:.0f} bp her olayın getirisinden ve eşli farkından düşülür; rastgele eş portföyler maliyetsiz (tutucu).

## 7. Hücreler ve KARAR (K64 §7 kuralı aynen; K64.k64_karar)
- Hücre = ABD x dönem (giriş gününe göre): {dn}. Bağımsız dönemler {E['bagimsiz'][0]} ve {E['bagimsiz'][1]}; {E['donem'][2][0]} örtüşür (tutarlılık; BH ailesine girmez).
- Karar birimi: (değişken, yön); ANA tanım (K24) ve KARAR sırası ({stad}).
- **'ADAY'** <=> iki bağımsız dönemin İKİSİNDE de aynı yönde 'EK KATKI VAR' ve ikisi de BH'den geçiyor. İki bağımsız dönemden birinde n_ÜST ya da n_ALT < {S1['n_esik']}
  ise **'ÖLÇÜLEMEZ'** ('İZ DEĞİL' ile karıştırılmaz). Aksi **'İZ DEĞİL'**.
- İŞARET: ölçülebilen bütün hücrelerde (üç dönem) ÜST - ALT nokta farkının işareti yönle aynı olmalı; dönerse aday düşer.
- Genel karar en fazla **'ABD-ADAY'**: İZ = ABD + Avrupa; Avrupa açığa satış verisi bu işte yok (AVRUPA VERİSİ YOK). Grubun dört şartı (brüt / net) ayrıca yazılır.

## 8. Çoklu test
Aile = ANA tanım, KARAR sırası, ölçülebilen bütün (değişken x yön x bağımsız dönem) hipotezleri: en çok {len(E['degisken'])} x 2 x {len(E['bagimsiz'])} = {m} (yalnız ABD).
p = 1 - Φ(±(ÜST - ALT) / bootstrap standart sapması) (tek yönlü). Benjamini-Hochberg q = %{100 * E['coklu']['bh_q']:.0f} (K60.k60_bh); Bonferroni bilgi olarak yazılır.
K64 / K65'in 84 hipotezlik ailesiyle birleştirilmez (ayrı soru, ayrı veri); ana oturum isterse birleşik BH'yi raporda ayrıca hesaplar.

## 9. GÜÇ BEYANI
K58 (arastirma_cikti/k58_cetvel_sagla/K58_RAPOR.md): FI_OLCUT, 60 günde +%2'lik gerçek etkiyi n = 300 olayda yalnız %11, +%4'ü %45 olasılıkla yakalıyor. Çöl olayları
içindeki üçte bir grupları birkaç yüz olaydır (§12). Her hücrede n ve 'saptanabilir en küçük etki' (aralık yarı genişliği) raporlanır. n < {S1['n_esik']} hücre 'ÖLÇÜLEMEZ'dir;
'ek katkı yok' 'etki yok' demek değildir, 'bu veriyle gösterilemedi' demektir.

## 10. Yanlılık beyanı
- YAŞAYAN YANLILIĞI: V_ABD yalnız BUGÜN işlem gören hisselerdir. Yüksek açığa satışlı çöl hisseleri batmaya en açık gruptur; batanlar örneklemde yok, bu grubun
  getirisi YUKARI yanlıdır (yüksek açık pozisyonun kötü haberi örneklemde eksik görünür). Eşli kontrol aynı evrenden seçildiği için yanlılığın bir kısmı farkta götürülür.
- SEMBOL: eşleme bugünkü kodla yapılır; kod değiştiren şirketlerin eski koddaki satırları eşleşmez (veri yok); eski kodu başka şirkete ait satırlar kimlik (hacim)
  denetimiyle düşer. Hacimleri tesadüfen 3 kat içinde olan farklı iki şirketin satırı tam dışlanamaz; kimliği doğru bir satır olağan dışı hacim farkıyla düşebilir.
- OTC satırları: FINRA dosyası OTC menkul kıymetlerini de kapsar; V_ABD sembolüyle eşleşen OTC satırları (OTC'den borsaya geçiş) kullanılır.
- TOPLAM PAY, FLOAT DEĞİL: SI_PAY halka açık paya göre değil toplam paya göredir; kurucu / içeriden payı yüksek şirketlerde oran olduğundan küçüktür.
- REVİZYON: CDN dosyaları sonradan düzeltilmiş değerleri taşıyabilir (revisionFlag); düzeltme günü bilinmiyor.
- FINRA açık pozisyonu aracı kurum bildirimidir (Reg SHO Rule 200 'short' hesapları); piyasa yapıcı ve bazı kurumsal pozisyonlar eksik / gecikmeli olabilir.
- K24 sinyali yalnız fiyatla tanımlıdır (sektör rüzgârı / katalizör şartı yok; K64 §10).

## 11. SAPMA / BOŞLUK listesi (iş tanımına göre; en dar yorum)
SAPMA 1. DTC dosyadaki alan yerine aynı iki alandan (currentShortPositionQuantity / averageDailyVolumeQuantity) yeniden hesaplanır: dosya alanı 1'in altını 1,00'a basar
  (bağ; §12'de pay) ve ADV = 0'da 999,99 yazar; 1'in üstünde iki değer 0,01 içinde birebir aynıdır (K66 örnek dosya denetimi).
SAPMA 2. Dönemler 2018-2021 / 2022-2026 / 2023-2026 (K64'te 2017-2021): FINRA verisi 2017-12-29'dan başlar; 2018-2021, 2017-2021'in veri olan kısmıdır. İlk bilgi günü
  Ocak 2018 ortasıdır; SI_DEG için 6 rapor geçmiş gerektiğinden ~Nisan 2018'den önce yok.
SAPMA 3. Evren yalnız ABD (BIST VERİSİ YOK); karar pazarı ABD; BH ailesi en çok {m} hipotez.
SAPMA 4. Bootstrap tohumları {S1['tohum']} / {E['s2']['tohum']} (K64: 64001 / 64002); yöntem aynı.
SAPMA 5. Kimlik denetimi ilk taslakta İSİM eşleşmesiydi (satırdaki adın ilk kelimesi = bugünkü adın ilk kelimesi). Kapsam incelemesinde (yalnız satır sayıları ve
  adlar; getiri görülmedi) adını değiştiren şirketlerin (ör. XOM, NEE, SLB, MSTR, CPB) bütün geçmişini düşürdüğü, kod yeniden kullanımını (ör. BNY: eski satırlar bir
  belediye tahvili fonu) ise hacimle de yakalanabildiği görüldü; ayrıca bugünkü ad sonraki bilgidir. Ön kayıttan ÖNCE hacim uyumuna çevrildi; isim yalnız bilgi.
BOŞLUK 1. Bilgi tarihi tutucu kuralı (ödeme + {F['bilgi_gecikme_islem']} işlem günü; dosya bazında yayın günü bulunamadı; kaynak §2).
BOŞLUK 2. r0 kuralı: yalnız en son kullanılabilir rapor; sembolün o raporda satırı yoksa değer yok (eski rapora düşülmez).
BOŞLUK 3. SI_DEG adımı bütün dosyalar sırasında 6 rapordur (iki rapor arası ~yarım ay; 6 rapor ~3 ay). Bölünme: K60 bölünme kayıtlarıyla bugünkü birime çevrilir;
  FINRA bölünme bayrağı aradaki raporlarda varken K60 kaydında o aralıkta bölünme yoksa değer yok.
BOŞLUK 4. SI_DEG1 = dosyadaki changePercent / 100; önceki pozisyon 0 (dosya %100 yazar) ya da r0'da bölünme bayrağı / bilinen bölünme varsa yok.
BOŞLUK 5. SI_PAY > {F['si_pay_aykiri']} (toplam payın iki katı) veri hatası sayılır; pay <= 0 / yoksa değer yok.
BOŞLUK 6. Sıfır açık pozisyon geçerli değerdir (SI_PAY = 0, DTC = 0); SI_DEG'de ln için iki uç da > 0 olmalı.
BOŞLUK 7. Kimlik denetiminin bandı {F['kimlik']['bant']:g} kat, penceresi FINRA ADV penceresidir (§2); bant FINRA ADV ile V_ABD hacminin birebire yakın olmasına göre seçildi
  (kapsam incelemesi: medyan log10 oran 0; §12) — getiri görülmedi.
BOŞLUK 8. Aynı dosyada iki kez geçen kod o dosyada atılır (§12'de sayısı).
BOŞLUK 9. K64 BOŞLUK 2, 7, 8, 9, 11-14 aynen geçerlidir (giriş gününe göre dönem; evren sırası için 'uygun hisse'; piyasa koşulu endeksi; D13 haftalık ızgara; maliyet;
  S2 girişi; fi_k24_tara ileriye bakan sütunları kullanılmaz; işaret şartında 0 tutmaz).

## 12. Kapsam (yalnız SAYI; mühre girmez)
{kapsam}

## 13. Çıktılar ve komutlar
Çıktılar arastirma_cikti/col_dis_bilgi/: k66_olaylar.csv.gz, k66_s1.csv, k66_s1_fark.csv, k66_s2.csv, k66_karar.csv, k66_meta.json, K66_RAPOR.md
(k66_kapsam.csv, k66_kapsam_ozet.json: kapsam). Raporda her değişken için: veri kaynağı ve kapsamı, tanım, örneklem, ortalama ve medyan getiri (20 ve 60 gün),
eşli fark, güven aralığı, dönemler arası tutarlılık, maliyet sonrası sonuç, veri eksikleri, karar.
1. (ana oturum) bu dosyayı denetler ve git'e işler.
2. `python -I K66.py kos`  -> ölçüm + rapor (mühür, veri sha256, K60 verisi, git doğrulanır)
3. `python K66.py rapor`   -> raporu çıktılardan yeniden yazar

## 14. Değişmezlik
K66_ESIK ya da içe alınan tanımlar (FI_K24, FI_OLCUT, K60 bilgi kuralı ve mührü, COL_v1 D13 sabitleri, K64 mührü) değişirse ESIK_SHA256 değişir ve koşu durur. Veri
(V_ABD, FINRA dosyaları), içe alınan ön kayıtlar (K60, K64 + K65) ya da kod dosyaları (FON_IZI.py, K60.py, K59.py, COL_v1.py, K64.py) değişirse sha256 tutmaz ve koşu durur.
"""


def k66_onkayit(cikti: Optional[str] = None, veri_sha: Optional[Dict[str, Tuple[str, int]]] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kaydı yazar. Dosya varsa ÜZERİNE YAZMAZ: mühür aynıysa yolu döndürür, değilse durur. Kapsam dosyası varsa karar sırası seçim kuralının sonucu mühürdeki
    karar sırasıyla aynı olmalı (değilse durur)."""
    E = E or K66_ESIK; yol = _k66_yol("onkayit", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True)
    if os.path.exists(yol):
        mevcut = K64._k64_onkayit_oku(yol)["sha"]
        if mevcut != k66_esik_sha(E):
            raise K66Hata(f"ön kayıt zaten var ve mühür farklı ({mevcut} != {k66_esik_sha(E)}): eşikler ön kayıttan sonra değişmiş")
        k66log.info("ön kayıt zaten var (mühür aynı): %s", yol)
        return yol
    yk = _k66_yol("kapsam", cikti); secim = ""
    if os.path.exists(yk):
        sec, hc = k66_sira_sec(pd.read_csv(yk), E)
        if sec != E["sira"]["karar"]["K66"]:
            raise K66Hata(f"karar sırası seçim kuralı kapsam sayımında '{sec}' veriyor, mühürdeki karar sırası '{E['sira']['karar']['K66']}': ön kayıt yazılmadı")
        top = [f"{h['degisken']} {h['donem']} (ÜST {h['n_ust']} / ALT {h['n_alt']}, oran {float(h['oran']):.2f})".replace(".", ",") for h in hc if h["toplanma"]]
        secim = (("toplanma olan hücre: " + "; ".join(top)) if top else "hiçbir hücrede toplanma yok") + f" -> {'İÇ' if sec == 'IC' else 'EVREN'}"
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    metin = k66_onkayit_metin(zaman, k66_veri_sha() if veri_sha is None else veri_sha, k66_kapsam_notu(cikti, E), E, secim)
    if _K66_EPOSTA.search(metin):
        raise K66Hata("ön kayıt metninde e-posta biçimli parça var; yazılmadı")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k66log.info("ön kayıt yazıldı: %s (mühür %s)", yol, k66_esik_sha(E)[:12])
    return yol


def k66_onkayit_dogrula(cikti: Optional[str] = None, veri: bool = False, git: bool = False, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Mühür (her zaman), veri sha256'ları (veri=True) ve git'e işlenmişlik (git=True) doğrulanır; biri tutmazsa K66Hata."""
    E = E or K66_ESIK; yol = _k66_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise K66Hata(f"ön kayıt yok ({yol}): önce `python K66.py onkayit`")
    oc = K64._k64_onkayit_oku(yol)
    if oc["sha"] != k66_esik_sha(E):
        raise K66Hata(f"ön kayıt mührü tutmuyor ({oc['sha']} != {k66_esik_sha(E)}): eşikler ön kayıttan sonra değişmiş, koşu durdu")
    out = {"yol": yol, "sha": oc["sha"], "zaman_utc": oc["zaman_utc"], "dosya_sha256": K60._k60_sha(yol), "veri": oc["veri"]}
    if veri:
        simdi = k66_veri_sha()
        fark = sorted(k for k in set(simdi) | set(oc["veri"]) if simdi.get(k) != oc["veri"].get(k))
        if fark:
            raise K66Hata(f"veri / içe alınan kod ön kayıttakiyle aynı değil (sha256 ya da dosya sayısı farklı): {fark}; koşu durdu")
    if git:
        try:
            out["git"] = K60._k60_git_islenmis(yol, "K66 ön kaydı")
        except K60.K60Hata as ex:
            raise K66Hata(str(ex))
    return out


# ---------------------------------------------------------------- 5) KOŞU (K64 cetvel / S1 / S2 / karar fonksiyonları aynen)
def k66_kos(cikti: Optional[str] = None, git_sart: bool = True, girdi: Optional[Dict[str, Dict[str, Any]]] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Tek koşu: ön kayıt (mühür + git) -> [gerçek veride veri sha256 + K60 ön kaydı / verisi] -> olaylar -> değişkenler -> FI_OLCUT -> S1, S2 -> karar -> çıktılar +
    rapor. girdi / E yalnız testler içindir (sentetik girdi: veri sha256 doğrulaması atlanır; ön kayıt doğrulaması yine şarttır)."""
    Ek = E or K66_ESIK; sentetik = girdi is not None; t0 = time.time()
    oc = k66_onkayit_dogrula(cikti, veri=not sentetik, git=git_sart, E=Ek)
    meta: Dict[str, Any] = {"surum": K66_SURUM, "onkayit": oc, "sentetik": sentetik, "kos_baslangic": _k66_simdi(), "isolated": bool(sys.flags.isolated),
                            "k66_kod_sha256": K60._k60_sha(os.path.join(KOK_K66, "K66.py")) if os.path.exists(os.path.join(KOK_K66, "K66.py")) else None,
                            "surumler": {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}, "pazar": {}}
    if not sentetik:
        try:
            k60 = K60.k60_onkayit_dogrula(None, veri=True, git=False)
        except K60.K60Hata as ex:
            raise K66Hata(f"K60 ön kaydı / verisi doğrulanamadı: {ex}")
        meta["k60_muhur"] = k60["sha"]; girdi = k66_girdi(Ek, k60["veri"])
    olaylar, s1, frk, s2 = [], [], [], []
    for pazar in Ek["pazar"]:
        if pazar not in girdi:
            continue
        g = girdi[pazar]; V = g["V"]; H = k66_pazar_hazirla(g, Ek)
        P = FI.fi_olcut_panel(V); P20 = FI.fi_olcut_panel(V, {**FI.FI_OLCUT, "ufuk": int(Ek["ek_ufuk"])}); F = K64.k64_fark_matris(P)
        if list(P["sembol"]) != list(H["sembol"]) or not P["tarih"].equals(H["takvim"]):
            raise K66Hata(f"{pazar}: FI_OLCUT paneli ile değişken matrisleri aynı takvim / sembol sırasında değil")
        O = _k66_olaylar(V, Ek, sentetik); meta["pazar"][pazar] = {**g.get("ozet", {}), "hisse": len(V), "gun": len(H["takvim"])}
        for tanim, X0 in O.items():
            X = K64.k64_olay_degerleri(X0, H, tanim, Ek); n_ham = len(X); X = X[X.tekil & X.giris.notna()].reset_index(drop=True)
            if tanim == "D13" and Ek["olay"]["d13"]["gecer"] and len(X):
                X = X[X.gecer].reset_index(drop=True)
            X = K64.k64_olc(P, P20, X) if len(X) else X.assign(r60=np.nan, esli_r60=np.nan, sira=np.nan, fark=np.nan, r20=np.nan, fark20=np.nan)
            X["pazar"] = pazar; X["tanim"] = tanim
            meta["pazar"][pazar][tanim] = {"ham": int(n_ham), "tekil": int(len(X)), "olculen": int(X.fark.notna().sum()) if len(X) else 0}
            a, b = K64.k64_s1(X, pazar, tanim, Ek); s1.append(a); frk.append(b); olaylar.append(X.drop(columns=[c for c in ("_esler",) if c in X]))
            if tanim == Ek["olay"]["ana"]:
                s2.append(K64.k64_s2(P, F, H, X0, pazar, Ek))
        k66log.info("%s ölçüldü (%.0f sn)", pazar, time.time() - t0)
    if not s1:
        raise K66Hata("ölçülecek pazar yok")
    S1 = pd.concat(s1, ignore_index=True); Fk = pd.concat(frk, ignore_index=True); S2 = pd.concat(s2, ignore_index=True) if s2 else pd.DataFrame(); Kr = K64.k64_karar(Fk, Ek)
    cik = cikti or K66_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    pd.concat(olaylar, ignore_index=True).to_csv(_k66_yol("olay", cikti), index=False); S1.to_csv(_k66_yol("s1", cikti), index=False)
    Fk.to_csv(_k66_yol("fark", cikti), index=False); S2.to_csv(_k66_yol("s2", cikti), index=False); Kr.to_csv(_k66_yol("karar", cikti), index=False)
    meta["kos_bitis"] = _k66_simdi(); meta["sure_sn"] = round(time.time() - t0)
    with open(_k66_yol("meta", cikti), "w", encoding="utf-8") as f:
        json.dump(K60._k60_yuvarla(meta, 12), f, ensure_ascii=False, indent=1, default=str)
    return {"s1": S1, "fark": Fk, "s2": S2, "karar": Kr, "meta": meta, "rapor": k66_rapor(cikti, Ek)}


# ---------------------------------------------------------------- 6) RAPOR
def k66_rapor(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """K66_RAPOR.md'yi çıktı dosyalarından yazar (her değişken: tanım, örneklem, 20 / 60 gün ortalama ve medyan, eşli fark, aralık, dönemler, maliyet sonrası, karar)."""
    E = E or K66_ESIK; yol = {k: _k66_yol(k, cikti) for k in ("s1", "fark", "s2", "karar", "meta")}
    if not all(os.path.exists(y) for y in yol.values()):
        raise K66Hata(f"K66 çıktıları yok ({yol['s1']}): önce `python -I K66.py kos`")
    S1 = pd.read_csv(yol["s1"]) if os.path.getsize(yol["s1"]) > 2 else pd.DataFrame(columns=["tanim", "pazar", "donem", "degisken", "sira_turu", "grup", "rejim"])
    S1[["degisken", "sira_turu"]] = S1[["degisken", "sira_turu"]].fillna(""); Fk = pd.read_csv(yol["fark"]) if os.path.getsize(yol["fark"]) > 2 else pd.DataFrame(columns=["degisken"])
    S2 = pd.read_csv(yol["s2"]) if os.path.getsize(yol["s2"]) > 2 else pd.DataFrame(); Kr = pd.read_csv(yol["karar"]) if os.path.getsize(yol["karar"]) > 2 else pd.DataFrame()
    with open(yol["meta"], encoding="utf-8") as f:
        m = json.load(f)
    f_, yz, tm, ev = K64._k64_f, K64._k64_yuz, K64._k64_tam, K64._k64_evet
    ana = E["olay"]["ana"]; tn = {d["kod"]: d for d in E["degisken"]}; st = E["sira"]["karar"]["K66"]
    par = [f"# K66 — ABD açığa satış talebi çöl sinyaline ek bilgi: RAPOR\n\n{K66_SURUM}. Ön kayıt K66_ON_KAYIT.md (mühür {str(m['onkayit']['sha'])[:12]}, dosya sha256 "
           f"{str(m['onkayit']['dosya_sha256'])[:12]}, git {str(m['onkayit'].get('git', {}).get('commit', ''))[:7]}); koşu {m['kos_baslangic']} -> {m['kos_bitis']} ({m.get('sure_sn')} sn).\n"]
    if len(Kr):
        par.append(f"## Karar tablosu (ANA tanım K24; karar sırası {'çöl içi' if st == 'IC' else 'evren içi'}; yön = hangi üçte bir daha iyi)\n| değişken | yön | karar | ABD | ek katkı (3 dönem) | "
                   "BH (bağımsız) | işaret tutarlı | grubun dört şartı (brüt / net) |\n|---|---|---|---|---|---|---|---|")
        for r in Kr.to_dict("records"):
            par.append(f"| {r['degisken']} | {'ÜST' if r['yon'] == 'UST' else 'ALT'} | {r['karar']} | {r.get('ABD_karar', '—')} | {r.get('ABD_ek', '—')} | {r.get('ABD_bh', '—')} | "
                       f"{'evet' if ev(r['isaret_tutarli']) else 'hayır'} | {'evet' if ev(r.get('ABD_dort_sart')) else 'hayır'} / {'evet' if ev(r.get('ABD_dort_sart_net')) else 'hayır'} |")
        par.append(f"\nBH ailesi m = {int(Kr.aile_m.iloc[0])} ölçülebilen hipotez; q = %{100 * E['coklu']['bh_q']:.0f}. 'İZ' bu işte verilemez (Avrupa açığa satış verisi yok).\n")
    T = S1[(S1.tanim == ana) & (S1.grup == "TEMEL") & (S1.rejim == "HEPSI")]
    par.append("## Temel model (yalnız çöl; değişkensiz)\n| pazar | dönem | n | ort. r60 | medyan r60 | ort. r20 | ort. eşli fark [%95] | medyan eşli fark | sıra | dört şart |\n|---|---|---|---|---|---|---|---|---|---|")
    for r in T.to_dict("records"):
        par.append(f"| {r['pazar']} | {r['donem']} | {tm(f_(r, 'n'))} | {yz(f_(r, 'ort_r60'))} | {yz(f_(r, 'medyan_r60'))} | {yz(f_(r, 'ort_r20'))} | "
                   f"{yz(f_(r, 'ort_fark'))} [{yz(f_(r, 'alt95'))}; {yz(f_(r, 'ust95'))}] | {yz(f_(r, 'medyan_fark'))} | {f_(r, 'sira'):.2f} | {'tutar' if ev(r.get('tutar')) else 'tutmaz'} |")
    for k in k66_kodlar(E):
        d = tn[k]
        par.append(f"\n## {k}\nTanım: {d['tanim']}. Beklenti: {d['kaynak']}. Karar sırası: {'çöl içi (İÇ)' if st == 'IC' else 'evren içi (EVREN)'}; öteki sıra sağlamlık.\n")
        par.append("| dönem | grup | n | ort. r60 | medyan r60 | ort. r20 | medyan r20 | ort. eşli fark [%95] | medyan eşli fark | yarı genişlik | net eşli fark | dört şart (brüt / net) |\n"
                   "|---|---|---|---|---|---|---|---|---|---|---|---|")
        for r in S1[(S1.tanim == ana) & (S1.degisken == k) & (S1.sira_turu == st) & (S1.rejim == "HEPSI") & S1.grup.isin(["UST", "ALT"])].to_dict("records"):
            par.append(f"| {r['donem']} | {'ÜST' if r['grup'] == 'UST' else 'ALT'} | {tm(f_(r, 'n'))} | {yz(f_(r, 'ort_r60'))} | {yz(f_(r, 'medyan_r60'))} | {yz(f_(r, 'ort_r20'))} | "
                       f"{yz(f_(r, 'medyan_r20'))} | {yz(f_(r, 'ort_fark'))} [{yz(f_(r, 'alt95'))}; {yz(f_(r, 'ust95'))}] | {yz(f_(r, 'medyan_fark'))} | {yz(f_(r, 'yari_genislik'))} | "
                       f"{yz(f_(r, 'ort_fark_net'))} | {'tutar' if ev(r.get('tutar')) else 'tutmaz'} / {'tutar' if ev(r.get('tutar_net')) else 'tutmaz'} |")
        par.append("\n| tanım | sıra | dönem | n ÜST / ALT | ÜST - ALT [%95] | temel eşli fark | ek katkı | 20 gün ÜST - ALT |\n|---|---|---|---|---|---|---|---|")
        for r in Fk[Fk.degisken == k].to_dict("records"):
            ek = "ÖLÇÜLEMEZ" if not ev(r["olculebilir"]) else ("VAR (ÜST)" if ev(r["ek_UST"]) else ("VAR (ALT)" if ev(r["ek_ALT"]) else "yok"))
            par.append(f"| {r['tanim']} | {r['sira_turu']} | {r['donem']} | {int(r['n_ust'])} / {int(r['n_alt'])} | {yz(f_(r, 'nokta'))} [{yz(f_(r, 'alt'))}; {yz(f_(r, 'ust'))}] | "
                       f"{yz(f_(r, 'ort_temel'))} | {ek} | {yz(f_(r, 'nokta20'))} |")
        if len(S2):
            par.append("\nS2 (çöl dışı evren; bilgi): " + "; ".join(f"{r['donem']} ÜST - ALT {yz(f_(r, 'nokta'))} [{yz(f_(r, 'alt'))}; {yz(f_(r, 'ust'))}] "
                                                                     f"(n {tm(f_(r, 'n_ust'))} / {tm(f_(r, 'n_alt'))})" for r in S2[S2.degisken == k].to_dict("records")))
        Rj = S1[(S1.tanim == ana) & (S1.degisken == k) & (S1.rejim != "HEPSI")]
        if len(Rj):
            par.append("\nPiyasa koşulu (bilgi): " + "; ".join(f"{r['donem']} {'endeks ort. üstü' if r['rejim'] == 'UST200' else 'endeks ort. altı'} {'ÜST' if r['grup'] == 'UST' else 'ALT'} "
                                                               f"n {tm(f_(r, 'n'))} eşli fark {yz(f_(r, 'ort_fark'))}" for r in Rj.to_dict("records")))
    par.append("\n## Veri eksikleri ve sınırlar\nBIST VERİSİ YOK (açığa satış yalnız BIST-30 / 50, açık pozisyon yayını yok). ÖDÜNÇ ÜCRETİ / KULLANILABİLİR ADET: VERİ YOK (ücretli). "
               "Pay toplam paydır (float değil). Bilgi tarihi tutucu: ödeme + 12 işlem günü. Evren yalnız yaşayanlar (ön kayıt §10). 'ÖLÇÜLEMEZ' = hücrede n < 30 (az veri), "
               "'İZ DEĞİL' değildir. Ayrıntı: K66_ON_KAYIT.md §9-§11; koşu sayıları k66_meta.json.\n")
    metin = "\n".join(par); y = _k66_yol("rapor", cikti)
    if _K66_EPOSTA.search(metin):
        raise K66Hata("rapor metninde e-posta biçimli parça var; yazılmadı")
    with open(y, "w", encoding="utf-8") as f:
        f.write(metin)
    k66log.info("rapor: %s", y)
    return y


def _cakisma_kontrol_k66(_once=_CK_ONCE_K66, _dosya="K66.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K66", "_CK_KAYIT", "_cakisma_kontrol_k66", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "io", "glob", "copy", "hashlib", "_dt", "annotations", "Any", "Callable", "Dict", "List",
           "Optional", "Tuple", "FI", "K60", "K59", "K64")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k66()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=K66_SURUM)
    ap.add_argument("komut", choices=["onkayit", "indir", "kapsam", "kos", "rapor"])
    ap.add_argument("--cikti", default=None)
    a_ = ap.parse_args()
    try:
        if a_.komut == "onkayit":
            y_ = k66_onkayit(a_.cikti); print(y_, "mühür", k66_esik_sha(), "dosya sha256", K60._k60_sha(y_))
        elif a_.komut == "indir":
            r_ = k66_finra_indir(); print(json.dumps({k: v for k, v in r_.items() if k != "sha256"}, ensure_ascii=False))
        elif a_.komut == "kapsam":
            K_ = k66_kapsam(a_.cikti); print(K_[K_.degisken == "(olay)"].to_string(index=False)); print(_k66_yol("kapsam", a_.cikti))
        elif a_.komut == "kos":
            R_ = k66_kos(a_.cikti); print("K66 bitti:", json.dumps({"sure_sn": R_["meta"]["sure_sn"], "pazar": R_["meta"]["pazar"]}, ensure_ascii=False, default=str))
            print(R_["karar"].to_string(index=False) if len(R_["karar"]) else "(karar tablosu boş)"); print(R_["rapor"])
        else:
            print(k66_rapor(a_.cikti))
    except (K66Hata, K64.K64Hata, K60.K60Hata, FileNotFoundError) as ex:
        k66log.error("%s", ex); sys.exit(1)
