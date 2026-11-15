"""K62 — BIST PEAD BİREBİR TEKRAR, tek dosya (11 Kasım 2026; ana oturum iş tanımı; ön kayıt arastirma_cikti/col_dis_bilgi/K62_ON_KAYIT.md).

Kaynak makale: Ahlatcıoğlu & Okay (2021), "Post-earnings announcement drift: Evidence from Turkey", Borsa Istanbul Review 21(1) 92-103,
doi 10.1016/j.bir.2020.09.001 (yöntem ayrıntısı: Ahlatcıoğlu 2020 Boğaziçi doktora tezi, 3. bölüm; özet ve sayılar makaleyle aynı).
  Ölçüler   SUETF = (E_q - E_{q-4}) / MV_q;  SUEAF = (E_q - analist ortalaması) / MV_q (VERİ YOK: ücretsiz tarihsel tahmin yok, vekil üretilmez);
            EAR = [t-1, t+1] al-tut getirisi - eşleşen 2x3 büyüklük-DD/PD portföyünün (eşit ağırlık) al-tut getirisi.
  Sonuç     CAR[2,61] (ve [2,21], [2,41]) = [t+2, t+N] al-tut getirisi - eşleşen portföyünki; PEAD = ort. CAR(Q3) - ort. CAR(Q1); mali çeyrek içi tertil.
  Bölümler  A birebir tekrar (makale örneklemi, veri izin verdiği kadar)  B aynı ölçüler 2017-2021 / 2022-2026 / 2023-2026
            C proje cetveli (FON_IZI FI_OLCUT; geleceğe bakmayan tertil, giriş t+2 açılışı)  D protokol (maliyet, çoklu test, tekilleştirme).
FON_IZI fonksiyonları MODÜL olarak içe alınır (kopya yok; FON_IZI.py DEĞİŞMEZ). Bütün eşikler K62_ESIK'tedir ve sha256 ile mühürlüdür.

Komut:  python K62.py indir      KAP 'Finansal Rapor' listesi + İş Yatırım fiyat / piyasa değeri + İş Yatırım mali tablo (yalnız indirme; getiri yok)
        python K62.py kapsam     veri demeti + sayım (hisse, açıklama, dönem dönem, ölçüsü hesaplanabilen olay); GETİRİ / SÜRPRİZ DEĞERİ HESAPLAMAZ
        python K62.py onkayit    K62_ON_KAYIT.md'yi yazar (mühür + veri sha256 + kapsam); var olanın üzerine yazmaz
        python -I K62.py kos     ön kayıt mührü + git + veri sha256 doğrulanır; A, B, C tek koşuda ölçülür; çıktılar + rapor
        python K62.py rapor      K62_RAPOR.md'yi çıktılardan yeniden yazar
Colab:  exec(open('K62.py').read()); k62_kos()
Veri:   önbellek /tmp/k62_veri (K62_VERI ile değişir; repoya veri konmaz). Kişisel e-posta / anahtar yok; SEC'e istek yok.
Çıktı:  arastirma_cikti/col_dis_bilgi/ K62_ON_KAYIT.md, k62_kapsam.json, k62_tablo.csv, k62_olay.csv, k62_meta.json, K62_RAPOR.md.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K62 = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import ssl  # noqa: E402
import subprocess  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402
import urllib.error  # noqa: E402
import urllib.parse  # noqa: E402
import urllib.request  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K62 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K62 not in sys.path:
    sys.path.insert(0, KOK_K62)

k62log = logging.getLogger("col.k62")
if not k62log.handlers:
    _k62_h = logging.StreamHandler(sys.stderr)
    _k62_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k62: %(message)s", "%H:%M:%S"))
    k62log.addHandler(_k62_h)
    k62log.setLevel(logging.INFO)
    k62log.propagate = False

K62_SURUM = "K62 v1.0 (2026-11-11): BIST PEAD birebir tekrar (Ahlatcıoğlu & Okay 2021): SUETF, SUEAF (veri yok), EAR; CAR[2,61]; dönemler; FI_OLCUT"
K62_YOL = {"cikti": os.path.join(KOK_K62, "arastirma_cikti", "col_dis_bilgi"), "veri": os.environ.get("K62_VERI", "/tmp/k62_veri"),
           "v_bist": os.environ.get("K62_VBIST", "/tmp/veri/V_BIST.pkl"), "sektor": os.path.join(KOK_K62, "sektor_BIST.csv"),
           "ca": os.environ.get("K62_CA", "/root/.ccr/ca-bundle.crt")}
K62_DOSYA = {"onkayit": "K62_ON_KAYIT.md", "kapsam": "k62_kapsam.json", "tablo": "k62_tablo.csv", "olay": "k62_olay.csv", "meta": "k62_meta.json",
             "rapor": "K62_RAPOR.md", "regresyon": "k62_regresyon.csv", "olcut": "k62_olcut.csv"}

# Ağ ayarları (eşik değildir; mühre girmez). Genel tarayıcı User-Agent; kişisel bilgi gönderilmez.
K62_AG = {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
          "zaman_asimi": 90, "deneme": 5, "bekle": 0.25, "is_parcacigi": 3, "kap_bekle": 0.5, "engel_ardisik": 12,
          "isy_fiyat": "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse={kod}&startdate={a}&enddate={b}",
          "isy_mali": ("https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo?companyCode={kod}&exchange=TRY"
                       "&financialGroup={grup}&year1={y}&period1=3&year2={y}&period2=6&year3={y}&period3=9&year4={y}&period4=12"),
          "isy_ref": "https://www.isyatirim.com.tr/"}

# ÖN KAYITTAKİ BÜTÜN SABİTLER (K62_ON_KAYIT.md). Sonuç görüldükten sonra buraya eşik EKLENMEZ / DEĞİŞTİRİLMEZ: mühür (k62_esik_sha) bozulur, koşu durur.
K62_ESIK: Dict[str, Any] = {
    "makale": {"doi": "10.1016/j.bir.2020.09.001", "donem": ["2007-01-01", "2018-12-31"], "n_tam": 6471, "n_analist": 2398,
               "pead": {"SUETF": {"21": 0.0118, "41": 0.0219, "61": 0.0294}, "SUEAF": {"21": 0.0131, "41": 0.0261, "61": 0.0290},
                        "EAR": {"21": 0.00763, "41": 0.0121, "61": 0.0218}},
               "t": {"SUETF": {"21": 3.75, "41": 4.44, "61": 4.26}, "SUEAF": {"21": 3.09, "41": 4.39, "61": 3.63}, "EAR": {"21": 2.17, "41": 2.61, "61": 3.88}},
               "regresyon_61": {"SUETF": 0.0278, "EAR": 0.0226}},
    "veri": {"kap": {"bas": "2009-06-01", "bit": "2026-08-31", "sinif": "FR", "konu": "Finansal Rapor", "pencere_gun": 14, "sinir": 2000},
             "fiyat": {"bas": "2008-01-01", "bit": "2026-08-31", "parca_yil": 4},
             "mali": {"bas_yil": 2008, "bit_yil": 2026, "grup": ["XI_29", "UFRS", "UFRS_K", "XI_29K"], "kar": "3Z", "ozkaynak": "2O",
                      "kar_desen": "ANA ORTAKLIK PAYLARI|NET D[ÖO]NEM KARI|D[ÖO]NEM NET KARI", "ozkaynak_desen": "[ÖO]ZKAYNAK|[ÖO]ZSERMAYE"},
             "takvim_min_hisse": 10, "kod_desen": "^[A-Z][A-Z0-9]{3,5}$"},
    "olay": {"saat_kaydir": False,          # A / B: t = KAP yayın günü (işlem günü değilse sonraki işlem günü); makalede Bloomberg günü, saat ayrımı yok
             "ear": [-1, 1], "car": {"bas": 2, "ufuk": [21, 41, 61], "ana": 61}, "on_pencere": [-61, -2], "getiri_pay": 2.0 / 3.0,
             "tertil": 3, "min_ceyrek_olay": 30, "winsor": [0.01, 0.99]},
    "ornek": {"pd_usd_min": 100.0e6, "defter_min": 0.0, "mali_yil_sonu_ay": 12, "lag_min": 1, "lag_max": 150},
    "portfoy": {"boyut_kova": 2, "dd_kova": 3, "olusum_ay": 6, "min_hisse": 5},
    "bolum_a": {"mali_bas": [2009, 2], "mali_bit": [2018, 4], "basari_puan": 0.015, "olculen": ["SUETF", "EAR"], "veri_yok": ["SUEAF"]},
    "bolum_b": {"donem": [["2017-2021", "2017-01-01", "2021-12-31"], ["2022-2026", "2022-01-01", "2026-12-31"], ["2023-2026", "2023-01-01", "2026-12-31"]],
                "kriz": "2026-08-31", "tms29_bas_yil": 2022, "tms29_haric": [[2022, 4], [2023, 4], [2024, 1], [2024, 2], [2024, 3], [2024, 4], [2025, 4]]},
    "bolum_c": {"giris_gun": 2, "tertil_onceki_min": 30, "havuz_geri": 4, "donem_ek": [["2017-2021", "2017-01-01", "2021-12-31"], ["2022-2026", "2022-01-01", "2026-12-31"],
                                                                     ["2023-2026", "2023-01-01", "2026-12-31"]]},
    "protokol": {"tekil_gun": 60, "maliyet_tek_yon": 0.0030, "bootstrap": 2000, "tohum": 62, "guven": [2.5, 97.5], "bh_q": 0.10, "bonferroni_alfa": 0.05,
                 "kume": "mali_ceyrek"},
    "regresyon": {"kontrol": ["CONCEARNINGS", "FRIDUM", "IVOL", "ILLIQUIDITY", "SIZE", "REPORTLAG", "BM", "BETA", "PRERET"], "eksik": ["IO"],
                  "sabit_etki": ["sektor", "mali_ceyrek"], "kume": "mali_ceyrek"},
}


class K62Hata(RuntimeError):
    """K62'ye özgü durdurucu hata (ön kayıt yok / mühür tutmuyor / git'e işlenmemiş, veri ön kayıttakinden farklı, veri ya da çıktı yok)."""


# ---------------------------------------------------------------- 0) ORTAK YARDIMCILAR, MÜHÜR
def _k62_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K62_YOL["cikti"], K62_DOSYA.get(ad, ad))


def _k62_veri_yol(*p: str, veri: Optional[str] = None) -> str:
    return os.path.join(veri or K62_YOL["veri"], *p)


def _k62_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _k62_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _k62_metin_sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _k62_bagimli() -> Dict[str, Any]:
    """Mühre giren dış tanım: FON_IZI FI_OLCUT (proje cetveli). FON_IZI içe alınamazsa mühür hesaplanamaz (koşu durur)."""
    import FON_IZI as FI
    return {"FI_OLCUT": FI.FI_OLCUT}


def k62_esik_sha(E: Optional[Dict[str, Any]] = None, bagimli: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: K62_ESIK + FI_OLCUT'un kararlı JSON'unun sha256'sı; biri değişirse koşu durur."""
    s = json.dumps({"K62_ESIK": E or K62_ESIK, "bagimli": bagimli if bagimli is not None else _k62_bagimli()}, sort_keys=True, default=str, ensure_ascii=False)
    return _k62_metin_sha(s)


def _k62_git_islenmis(yol: str, ne: str) -> Dict[str, str]:
    """Dosya git'e işlenmiş ve işlendikten sonra değişmemiş olmalı (denetim sırası: git zamanı + içerik)."""
    kl, ad = os.path.dirname(os.path.abspath(yol)), os.path.basename(yol)
    try:
        r = subprocess.run(["git", "-C", kl, "log", "-1", "--format=%H %cI", "--", ad], capture_output=True, text=True, timeout=60)
        d = subprocess.run(["git", "-C", kl, "status", "--porcelain", "--", ad], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as ex:
        raise K62Hata(f"git çalıştırılamadı ({ex}): {ne} dosyasının işlendiği doğrulanamadı, koşu durdu")
    if r.returncode != 0 or not r.stdout.strip():
        raise K62Hata(f"{ne} git'e işlenmemiş ({yol}): önce ana oturum denetleyip commit eder")
    if d.returncode != 0 or d.stdout.strip():
        raise K62Hata(f"{ne} git'e işlendikten sonra değişmiş ({d.stdout.strip() or d.stderr.strip()}): koşu durdu")
    h, z = r.stdout.strip().split(" ", 1)
    return {"commit": h, "commit_zamani": z}


def _k62_json_yaz(yol: str, govde: Any) -> str:
    """Kararlı JSON (anahtar sıralı). Döner: sha256."""
    metin = json.dumps(govde, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n"
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol + ".yarim", "w", encoding="utf-8") as f:
        f.write(metin)
    os.replace(yol + ".yarim", yol)
    return _k62_metin_sha(metin)


def _k62_json_oku(yol: str) -> Any:
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


_K62_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


# ---------------------------------------------------------------- 1) İNDİRME (yalnız veri; getiri hesaplanmaz)
def _k62_ctx() -> ssl.SSLContext:
    return ssl.create_default_context(cafile=K62_YOL["ca"]) if os.path.exists(K62_YOL["ca"]) else ssl.create_default_context()


def _k62_getir(url: str, ctx: Optional[ssl.SSLContext] = None, dur: Optional[threading.Event] = None) -> Tuple[str, Optional[bytes]]:
    """Tek GET (gzip): ('tamam', gövde) / ('yok', None) (404) / ('engel', None) (401/403/429 bütün denemelerde) / ('hata', None) / ('durdu', None)."""
    A = K62_AG; son = "hata"; ctx = ctx or _k62_ctx()
    for deneme in range(A["deneme"]):
        if dur is not None and dur.is_set():
            return "durdu", None
        try:
            req = urllib.request.Request(url, headers={"User-Agent": A["ua"], "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip",
                                                       "Referer": A["isy_ref"], "X-Requested-With": "XMLHttpRequest"})
            with urllib.request.urlopen(req, context=ctx, timeout=A["zaman_asimi"]) as r:
                ham = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    ham = gzip.decompress(ham)
            return "tamam", ham
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "yok", None
            son = "engel" if e.code in (401, 403, 429) else "hata"
            time.sleep(8.0 * 2 ** deneme if son == "engel" else 2.0 * (deneme + 1))
        except (urllib.error.URLError, TimeoutError, ValueError, OSError, EOFError) as e:      # IncompleteRead OSError alt sınıfı değildir: aşağıda
            son = "hata"; k62log.debug("GET %s: %s", url[-70:], str(e)[:100]); time.sleep(2.0 * (deneme + 1))
        except Exception as e:      # http.client.IncompleteRead vb. aktarım kopmaları: yeniden dene
            son = "hata"; k62log.debug("GET %s: %s", url[-70:], str(e)[:100]); time.sleep(2.0 * (deneme + 1))
    return son, None


def _k62_gz_yaz(yol: str, ham: bytes) -> None:
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with gzip.open(yol + ".yarim", "wb") as f:
        f.write(ham)
    os.replace(yol + ".yarim", yol)


def _k62_gz_oku(yol: str) -> bytes:
    with gzip.open(yol, "rb") as f:
        return f.read()


def k62_kap_indir(veri: Optional[str] = None, E: Optional[Dict[str, Any]] = None, istek: Optional[Callable[[str, str], Optional[List[Dict[str, Any]]]]] = None) -> Dict[str, Any]:
    """KAP 'Finansal Rapor' (bildirim sınıfı FR) listesi, pencere pencere; pencere 'sinir' kayda çarparsa ikiye bölünür (tek günde çarparsa 'kesik
    gün' olarak işaretlenir). Yaprak pencereler kap/AAAA-AA-GG_AAAA-AA-GG.json.gz; kaldığı yerden sürer. `istek(a, b)` testler içindir."""
    K = (E or K62_ESIK)["veri"]["kap"]; kl = _k62_veri_yol("kap", veri=veri); os.makedirs(kl, exist_ok=True)
    durum = {"pencere": 0, "onbellek": 0, "indirilen": 0, "hata": 0, "kesik_gun": [], "kayit": 0}
    if istek is None:
        import FON_IZI as FI
        s = FI._fi_kap_oturum()

        def istek(a: str, b: str) -> Optional[List[Dict[str, Any]]]:
            r = FI._fi_kap_istek(s, "POST", FI._FI_KAP + "/tr/api/disclosure/members/byCriteria", deneme=5,
                                 data=json.dumps({"fromDate": a, "toDate": b, "mkkMemberOidList": [], "subjectList": [], "disclosureClass": K["sinif"]}))
            time.sleep(K62_AG["kap_bekle"])
            if r is None:
                return None
            try:
                J = r.json()
            except ValueError:
                return None
            return J if isinstance(J, list) else None

    def al(a: pd.Timestamp, b: pd.Timestamp) -> None:
        ad = os.path.join(kl, f"{a.date()}_{b.date()}.json.gz"); durum["pencere"] += 1
        if os.path.exists(ad):
            durum["onbellek"] += 1; return
        def bol() -> None:
            durum["pencere"] -= 1; m = a + pd.Timedelta(days=int((b - a).days // 2)); al(a, m); al(m + pd.Timedelta(days=1), b)
        if os.path.exists(ad + ".bol"):       # daha önce sınıra çarpmış pencere: doğrudan böl
            bol(); return
        J = istek(str(a.date()), str(b.date()))
        if J is None:
            durum["hata"] += 1; k62log.error("KAP %s..%s alınamadı", a.date(), b.date()); return
        if len(J) >= K["sinir"]:
            if a == b:
                durum["kesik_gun"].append(str(a.date())); k62log.warning("KAP %s: tek günde %d kayıt (sınır); kesik gün", a.date(), len(J))
            else:
                open(ad + ".bol", "w").close(); bol(); return
        sat = [{k: j.get(k) for k in ("publishDate", "stockCodes", "year", "period", "ruleType", "subject", "summary", "disclosureIndex", "isLate",
                                      "modifyStatus", "kapTitle", "disclosureClass")} for j in J]
        _k62_gz_yaz(ad, json.dumps(sat, ensure_ascii=False).encode("utf-8")); durum["indirilen"] += 1

    a = pd.Timestamp(K["bas"]); son = pd.Timestamp(K["bit"])
    while a <= son:
        b = min(a + pd.Timedelta(days=K["pencere_gun"] - 1), son)
        try:
            al(a, b)
        except Exception as ex:       # tek pencere bozulursa ötekiler sürer; eksik pencere 'hata' sayılır
            durum["hata"] += 1; k62log.error("KAP %s..%s: %s", a.date(), b.date(), ex)
        a = b + pd.Timedelta(days=1)
        if durum["pencere"] % 40 == 0:
            k62log.info("KAP: %d pencere (indirilen %d, önbellek %d, hata %d)", durum["pencere"], durum["indirilen"], durum["onbellek"], durum["hata"])
    L = k62_kap_oku(veri); durum["kayit"] = int(len(L))
    _k62_json_yaz(os.path.join(kl, "_durum.json"), {**durum, "zaman_utc": _k62_simdi()})
    k62log.info("KAP bitti: %s", {k: (v if k != "kesik_gun" else len(v)) for k, v in durum.items()})
    return durum


def k62_kap_oku(veri: Optional[str] = None) -> pd.DataFrame:
    """Önbellekteki KAP pencerelerini tek tabloya çevirir (disclosureIndex'e göre tekil; yalnız konu 'Finansal Rapor')."""
    kl = _k62_veri_yol("kap", veri=veri); sat: List[Dict[str, Any]] = []
    for ad in sorted(os.listdir(kl)) if os.path.isdir(kl) else []:
        if ad.endswith(".json.gz"):
            try:
                sat += json.loads(_k62_gz_oku(os.path.join(kl, ad)).decode("utf-8"))
            except (OSError, ValueError, EOFError) as ex:
                k62log.error("KAP önbellek dosyası okunamadı (%s): %s", ad, ex)
    kol = ["publishDate", "stockCodes", "year", "period", "ruleType", "subject", "summary", "disclosureIndex", "isLate", "modifyStatus", "kapTitle", "disclosureClass"]
    if not sat:
        return pd.DataFrame(columns=kol)
    L = pd.DataFrame(sat).reindex(columns=kol).drop_duplicates("disclosureIndex")
    return L[L.subject.astype(str).str.strip() == K62_ESIK["veri"]["kap"]["konu"]].reset_index(drop=True)


def k62_kod_adaylari(L: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """KAP listesindeki bütün borsa kodları (virgülle ayrılmış 'stockCodes' parçaları, desen uyanlar): kod, ilk ve son mali yıl, kayıt sayısı."""
    ds = re.compile((E or K62_ESIK)["veri"]["kod_desen"]); sat: Dict[str, List[int]] = {}
    for kodlar, yil in zip(L.stockCodes, L.year):
        if not isinstance(kodlar, str) or not pd.notna(yil):
            continue
        for k in (x.strip() for x in kodlar.split(",")):
            if ds.match(k):
                v = sat.setdefault(k, [int(yil), int(yil), 0]); v[0] = min(v[0], int(yil)); v[1] = max(v[1], int(yil)); v[2] += 1
    return pd.DataFrame([{"kod": k, "ilk_yil": v[0], "son_yil": v[1], "kayit": v[2]} for k, v in sorted(sat.items())], columns=["kod", "ilk_yil", "son_yil", "kayit"])


def _k62_parcalar(ilk_yil: int, son_yil: int, E: Optional[Dict[str, Any]] = None) -> List[Tuple[str, str]]:
    """Sabit sınırlı fiyat parçaları (parca_yil yıllık), hissenin [ilk mali yıl - 1, son mali yıl + 1] aralığını kesenler; 'gg-aa-yyyy' çiftleri."""
    F = (E or K62_ESIK)["veri"]["fiyat"]; bas, bit = pd.Timestamp(F["bas"]), pd.Timestamp(F["bit"]); out = []
    y = bas.year
    while y <= bit.year:
        a = max(bas, pd.Timestamp(year=y, month=1, day=1)); b = min(bit, pd.Timestamp(year=y + F["parca_yil"] - 1, month=12, day=31))
        if b.year >= ilk_yil - 1 and a.year <= son_yil + 1:
            out.append((a.strftime("%d-%m-%Y"), b.strftime("%d-%m-%Y")))
        y += F["parca_yil"]
    return out


_K62_FIYAT_KOL = ["tarih", "kapanis", "ham", "pd", "pd_usd", "hacim_tl", "hacim_usd", "endeks", "sermaye"]


def k62_fiyat_ayristir(ham: bytes) -> pd.DataFrame:
    """İş Yatırım HisseTekil yanıtı -> tarih sıralı tablo: düzeltilmiş kapanış (bölünme + temettü), ham kapanış, piyasa değeri (TL, USD), hacim (TL, USD),
    BIST-100 değeri, sermaye. Boş yanıt -> boş tablo."""
    v = (json.loads(ham.decode("utf-8")) or {}).get("value") or []
    if not v:
        return pd.DataFrame(columns=_K62_FIYAT_KOL)
    D = pd.DataFrame(v)
    X = pd.DataFrame({"tarih": pd.to_datetime(D["HGDG_TARIH"], format="%d-%m-%Y", errors="coerce")})
    for hedef, kaynak in (("kapanis", "HGDG_KAPANIS"), ("ham", "HG_KAPANIS"), ("pd", "PD"), ("pd_usd", "PD_USD"), ("hacim_tl", "HGDG_HACIM"),
                          ("hacim_usd", "DOLAR_HACIM"), ("endeks", "END_DEGER"), ("sermaye", "SERMAYE")):
        X[hedef] = pd.to_numeric(D[kaynak], errors="coerce") if kaynak in D else np.nan
    return X.dropna(subset=["tarih"]).drop_duplicates("tarih").sort_values("tarih").reset_index(drop=True)


def k62_fiyat_indir(kodlar: pd.DataFrame, veri: Optional[str] = None, E: Optional[Dict[str, Any]] = None,
                    getir: Optional[Callable[[str], Tuple[str, Optional[bytes]]]] = None) -> Dict[str, Any]:
    """Her aday kod için İş Yatırım günlük fiyat + piyasa değeri (kotasyondan çıkanlar dahil). fiyat/KOD.csv.gz (boş kod: sıfır satır); kaldığı
    yerden sürer. Ardışık engel / hata K62_AG['engel_ardisik']'e ulaşırsa durur."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    kl = _k62_veri_yol("fiyat", veri=veri); os.makedirs(kl, exist_ok=True); ctx = _k62_ctx(); dur = threading.Event()
    getir = getir or (lambda u: _k62_getir(u, ctx, dur))
    isler = [r for r in kodlar.itertuples() if not os.path.exists(os.path.join(kl, f"{r.kod}.csv.gz"))]
    durum = {"istenen": int(len(kodlar)), "onbellek": int(len(kodlar) - len(isler)), "dolu": 0, "bos": 0, "hata": 0, "durum": "tamam"}
    kilit = threading.Lock(); ardisik = [0]

    def is_(r: Any) -> Tuple[str, str]:
        par = []
        for a, b in _k62_parcalar(int(r.ilk_yil), int(r.son_yil), E):
            d, ham = getir(K62_AG["isy_fiyat"].format(kod=urllib.parse.quote(r.kod), a=a, b=b))
            if d != "tamam" or ham is None:
                return r.kod, d if d != "tamam" else "hata"
            try:
                par.append(k62_fiyat_ayristir(ham))
            except (ValueError, KeyError) as ex:
                k62log.debug("fiyat %s ayrıştırılamadı: %s", r.kod, ex); return r.kod, "hata"
            time.sleep(K62_AG["bekle"])
        X = pd.concat(par, ignore_index=True).drop_duplicates("tarih").sort_values("tarih") if par else pd.DataFrame(columns=_K62_FIYAT_KOL)
        tmp = os.path.join(kl, f"{r.kod}.csv.gz.yarim"); X.to_csv(tmp, index=False, compression="gzip"); os.replace(tmp, os.path.join(kl, f"{r.kod}.csv.gz"))
        return r.kod, "dolu" if len(X) else "bos"

    with ThreadPoolExecutor(K62_AG["is_parcacigi"]) as ex:
        for i, f in enumerate(as_completed([ex.submit(is_, r) for r in isler])):
            try:
                kod, d = f.result()
            except Exception as e:       # tek kod bozulursa ötekiler sürer
                kod, d = "?", "hata"; k62log.warning("fiyat işi: %s", e)
            with kilit:
                if d in ("dolu", "bos"):
                    durum[d] += 1; ardisik[0] = 0
                elif d != "durdu":
                    durum["hata"] += 1; ardisik[0] += 1
                    if ardisik[0] >= K62_AG["engel_ardisik"] and not dur.is_set():
                        dur.set(); durum["durum"] = "durdu (ardışık engel / hata)"; k62log.error("fiyat: ardışık %d engel / hata; indirme durdu", ardisik[0])
            if (i + 1) % 50 == 0:
                k62log.info("fiyat: %d / %d (dolu %d, boş %d, hata %d)", i + 1, len(isler), durum["dolu"], durum["bos"], durum["hata"])
    _k62_json_yaz(os.path.join(kl, "_durum.json"), {**durum, "zaman_utc": _k62_simdi()})
    k62log.info("fiyat bitti: %s", durum)
    return durum


def k62_mali_ayristir(ham: bytes, E: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """İş Yatırım MaliTablo yanıtı (bir yıl, 3/6/9/12 ay) -> {'kar': [4 birikimli değer], 'ozkaynak': [4 değer]} (kalem kodu + açıklama deseni tutmalı;
    tutmayan kalem None listesi). Boş yanıt -> None."""
    M = (E or K62_ESIK)["veri"]["mali"]; v = (json.loads(ham.decode("utf-8")) or {}).get("value") or []
    if not v:
        return None

    def say(x: Any) -> Optional[float]:
        try:
            f = float(str(x).replace(",", "."))
        except (TypeError, ValueError):
            return None
        return f if math.isfinite(f) else None
    out: Dict[str, Any] = {"kar": [None] * 4, "ozkaynak": [None] * 4, "kalem": len(v)}
    for r in v:
        acik = str(r.get("itemDescTr") or "").upper().replace("Â", "A")
        for ad, kod, desen in (("kar", M["kar"], M["kar_desen"]), ("ozkaynak", M["ozkaynak"], M["ozkaynak_desen"])):
            if r.get("itemCode") == kod and re.search(desen, acik):
                out[ad] = [say(r.get(f"value{i}")) for i in (1, 2, 3, 4)]; out[ad + "_ad"] = acik.strip()[:60]
    return out


def k62_mali_indir(kodlar: pd.DataFrame, veri: Optional[str] = None, E: Optional[Dict[str, Any]] = None,
                   getir: Optional[Callable[[str], Tuple[str, Optional[bytes]]]] = None) -> Dict[str, Any]:
    """Her kod için İş Yatırım çeyreklik mali tablo kalemleri (net dönem kârı ana ortaklık payı, özkaynak), yıl yıl. Grup sırası K62_ESIK['veri']
    ['mali']['grup']: bir yıl için ilk dolu grup; kodun bulunan grubu sonraki yıllarda önce denenir. mali/KOD.json; kaldığı yerden sürer."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    M = (E or K62_ESIK)["veri"]["mali"]; kl = _k62_veri_yol("mali", veri=veri); os.makedirs(kl, exist_ok=True); ctx = _k62_ctx(); dur = threading.Event()
    getir = getir or (lambda u: _k62_getir(u, ctx, dur))
    isler = [r for r in kodlar.itertuples() if not os.path.exists(os.path.join(kl, f"{r.kod}.json"))]
    durum = {"istenen": int(len(kodlar)), "onbellek": int(len(kodlar) - len(isler)), "dolu": 0, "bos": 0, "hata": 0, "durum": "tamam"}
    kilit = threading.Lock(); ardisik = [0]

    def is_(r: Any) -> Tuple[str, str]:
        yillar: Dict[str, Any] = {}; son_grup: Optional[str] = None
        for y in range(max(M["bas_yil"], int(r.ilk_yil) - 1), min(M["bit_yil"], int(r.son_yil)) + 1):
            for g in ([son_grup] if son_grup else []) + [g for g in M["grup"] if g != son_grup]:
                d, ham = getir(K62_AG["isy_mali"].format(kod=urllib.parse.quote(r.kod), grup=g, y=y))
                if d != "tamam" or ham is None:
                    return r.kod, d if d != "tamam" else "hata"
                try:
                    x = k62_mali_ayristir(ham, E)
                except (ValueError, KeyError) as ex:
                    k62log.debug("mali %s %d ayrıştırılamadı: %s", r.kod, y, ex); return r.kod, "hata"
                time.sleep(K62_AG["bekle"])
                if x is not None:
                    yillar[str(y)] = {**x, "grup": g}; son_grup = g; break
        _k62_json_yaz(os.path.join(kl, f"{r.kod}.json"), {"kod": r.kod, "yil": yillar})
        return r.kod, "dolu" if yillar else "bos"

    with ThreadPoolExecutor(K62_AG["is_parcacigi"]) as ex:
        for i, f in enumerate(as_completed([ex.submit(is_, r) for r in isler])):
            try:
                kod, d = f.result()
            except Exception as e:       # tek kod bozulursa ötekiler sürer
                kod, d = "?", "hata"; k62log.warning("mali işi: %s", e)
            with kilit:
                if d in ("dolu", "bos"):
                    durum[d] += 1; ardisik[0] = 0
                elif d != "durdu":
                    durum["hata"] += 1; ardisik[0] += 1
                    if ardisik[0] >= K62_AG["engel_ardisik"] and not dur.is_set():
                        dur.set(); durum["durum"] = "durdu (ardışık engel / hata)"; k62log.error("mali: ardışık %d engel / hata; indirme durdu", ardisik[0])
            if (i + 1) % 50 == 0:
                k62log.info("mali: %d / %d (dolu %d, boş %d, hata %d)", i + 1, len(isler), durum["dolu"], durum["bos"], durum["hata"])
    _k62_json_yaz(os.path.join(kl, "_durum.json"), {**durum, "zaman_utc": _k62_simdi()})
    k62log.info("mali bitti: %s", durum)
    return durum


def k62_indir(veri: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Üç kaynak sırayla: KAP listesi -> aday kodlar -> İş Yatırım fiyat -> (fiyatı dolu kodlar için) İş Yatırım mali tablo. Getiri hesaplanmaz."""
    out: Dict[str, Any] = {"bas_utc": _k62_simdi()}
    out["kap"] = k62_kap_indir(veri, E)
    kodlar = k62_kod_adaylari(k62_kap_oku(veri), E); out["aday_kod"] = int(len(kodlar))
    out["fiyat"] = k62_fiyat_indir(kodlar, veri, E)
    kl = _k62_veri_yol("fiyat", veri=veri)
    dolu = kodlar[[os.path.exists(os.path.join(kl, f"{k}.csv.gz")) and os.path.getsize(os.path.join(kl, f"{k}.csv.gz")) > 200 for k in kodlar.kod]]
    out["fiyati_dolu_kod"] = int(len(dolu))
    out["mali"] = k62_mali_indir(dolu, veri, E)
    out["bit_utc"] = _k62_simdi()
    _k62_json_yaz(_k62_veri_yol("_indir.json", veri=veri), out)
    return out


# ---------------------------------------------------------------- 2) VERİ DEMETİ (önbellekten; getiri hesaplanmaz)
def k62_veri_sha(veri: Optional[str] = None) -> Dict[str, Any]:
    """Önbelleğin içerik özeti: kap / fiyat / mali altındaki her veri dosyasının sha256'sından tek sha256 + dosya sayıları; V_BIST.pkl sha256."""
    out: Dict[str, Any] = {}; h = hashlib.sha256()
    for alt, uz in (("kap", ".json.gz"), ("fiyat", ".csv.gz"), ("mali", ".json")):
        kl = _k62_veri_yol(alt, veri=veri); adlar = sorted(a for a in os.listdir(kl) if a.endswith(uz) and not a.startswith("_")) if os.path.isdir(kl) else []
        for a in adlar:
            h.update(f"{alt}/{a}:{_k62_sha(os.path.join(kl, a))}\n".encode("utf-8"))
        out[alt + "_dosya"] = len(adlar)
    out["sha256"] = h.hexdigest()
    out["v_bist_sha256"] = _k62_sha(K62_YOL["v_bist"]) if os.path.exists(K62_YOL["v_bist"]) else None
    return out


def _k62_son_gun(tak: pd.DatetimeIndex, tarih: Any) -> int:
    """tarih'e eşit ya da ondan önceki son işlem gününün konumu (yoksa -1)."""
    return int(tak.searchsorted(pd.Timestamp(tarih), side="right")) - 1


def k62_duyurular(L: pd.DataFrame, kodlar: List[str], agirlik: Optional[Dict[str, float]] = None) -> pd.DataFrame:
    """KAP listesi -> açıklama tablosu: (kod, mali yıl, çeyrek) başına İLK 'Finansal Rapor' yayın anı. Bir kaydın birden çok borsa kodu varsa fiyat
    verisi olanlardan toplam USD hacmi en büyük olan (en likit pay grubu) seçilir. Çeyrek = KAP 'period' (1-4)."""
    var = set(kodlar); agirlik = agirlik or {}; sec: Dict[str, Optional[str]] = {}

    def kod_sec(s: Any) -> Optional[str]:
        if not isinstance(s, str):
            return None
        if s not in sec:
            ad = [x.strip() for x in s.split(",") if x.strip() in var]
            sec[s] = max(ad, key=lambda k: (agirlik.get(k, 0.0), k)) if ad else None
        return sec[s]
    if not len(L):
        return pd.DataFrame(columns=["kod", "yil", "ceyrek", "yayin", "bildirim"])
    X = pd.DataFrame({"kod": [kod_sec(s) for s in L.stockCodes], "yil": pd.to_numeric(L.year, errors="coerce"), "ceyrek": pd.to_numeric(L.period, errors="coerce"),
                      "yayin": pd.to_datetime(L.publishDate, format="%d.%m.%Y %H:%M:%S", errors="coerce")})
    X = X.dropna(subset=["kod", "yil", "ceyrek", "yayin"]); X = X[X.ceyrek.isin([1, 2, 3, 4])]
    X["yil"] = X.yil.astype(int); X["ceyrek"] = X.ceyrek.astype(int)
    G = X.groupby(["kod", "yil", "ceyrek"]).yayin.agg(["min", "size"]).reset_index().rename(columns={"min": "yayin", "size": "bildirim"})
    return G.sort_values(["yayin", "kod"]).reset_index(drop=True)


def k62_mali_tablo(veri: Optional[str] = None) -> pd.DataFrame:
    """mali/KOD.json dosyaları -> uzun tablo: kod, yil, ceyrek (1-4), kar_bir (yıl başından birikimli net kâr), ozkaynak, grup."""
    kl = _k62_veri_yol("mali", veri=veri); sat = []
    for ad in sorted(os.listdir(kl)) if os.path.isdir(kl) else []:
        if not ad.endswith(".json") or ad.startswith("_"):
            continue
        try:
            J = _k62_json_oku(os.path.join(kl, ad))
        except (OSError, ValueError) as ex:
            k62log.error("mali dosyası okunamadı (%s): %s", ad, ex); continue
        for y, x in (J.get("yil") or {}).items():
            for c in range(4):
                k, o = x.get("kar", [None] * 4)[c], x.get("ozkaynak", [None] * 4)[c]
                if k is not None or o is not None:
                    sat.append({"kod": J["kod"], "yil": int(y), "ceyrek": c + 1, "kar_bir": k, "ozkaynak": o, "grup": x.get("grup")})
    M = pd.DataFrame(sat, columns=["kod", "yil", "ceyrek", "kar_bir", "ozkaynak", "grup"])
    M["kar_bir"] = pd.to_numeric(M.kar_bir, errors="coerce"); M["ozkaynak"] = pd.to_numeric(M.ozkaynak, errors="coerce")
    return M


def k62_demet_kur(veri: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Önbellekten veri demeti: takvim (işlem günleri), kod listesi, C (düzeltilmiş kapanış), PD, PDU (USD), HU (USD hacim) [gün x hisse], X
    (BIST-100), mali (uzun tablo), duyuru (ilk Finansal Rapor), sektor. Yalnız veri düzeni; getiri hesaplanmaz."""
    E = E or K62_ESIK; kl = _k62_veri_yol("fiyat", veri=veri)
    if not os.path.isdir(kl):
        raise K62Hata(f"fiyat önbelleği yok ({kl}): önce `python K62.py indir`")
    F: Dict[str, pd.DataFrame] = {}
    for ad in sorted(os.listdir(kl)):
        if ad.endswith(".csv.gz"):
            try:
                X = pd.read_csv(os.path.join(kl, ad), parse_dates=["tarih"])
            except (OSError, ValueError, pd.errors.EmptyDataError) as ex:
                k62log.error("fiyat dosyası okunamadı (%s): %s", ad, ex); continue
            if len(X):
                F[ad[:-7]] = X.set_index("tarih")
    if not F:
        raise K62Hata(f"fiyat önbelleğinde dolu dosya yok ({kl})")
    kod = sorted(F); say = pd.concat([F[k].kapanis.notna() for k in kod], axis=1, sort=True).sum(axis=1)
    tak = pd.DatetimeIndex(sorted(say.index[say >= E["veri"]["takvim_min_hisse"]]))
    tak = tak[(tak >= pd.Timestamp(E["veri"]["fiyat"]["bas"])) & (tak <= pd.Timestamp(E["veri"]["fiyat"]["bit"]))]

    def pan(kolon: str) -> np.ndarray:
        return pd.DataFrame({k: F[k][kolon] for k in kod}).reindex(tak).to_numpy(float)
    Xs = pd.concat([F[k].endeks for k in kod], axis=1, sort=True).reindex(tak).median(axis=1)       # BIST-100: bütün hisselerin satırlarındaki aynı değer
    L = k62_kap_oku(veri); ag = {k: float(np.nansum(F[k].hacim_usd.to_numpy(float))) for k in kod}
    D = {"takvim": tak, "kod": kod, "C": pan("kapanis"), "PD": pan("pd"), "PDU": pan("pd_usd"), "HU": pan("hacim_usd"), "X": Xs.to_numpy(float),
         "mali": k62_mali_tablo(veri), "duyuru": k62_duyurular(L, kod, ag), "sektor": k62_sektor_oku(), "kap_kayit": int(len(L))}
    k62log.info("demet: %d işlem günü (%s .. %s), %d hisse, %d açıklama, %d mali satır", len(tak), tak[0].date(), tak[-1].date(), len(kod), len(D["duyuru"]), len(D["mali"]))
    return D


def k62_sektor_oku(yol: Optional[str] = None) -> Dict[str, str]:
    """sektor_BIST.csv -> {kod: sektör}; dosya yoksa boş (sabit etkide 'BILINMIYOR')."""
    yol = yol or K62_YOL["sektor"]
    try:
        S = pd.read_csv(yol)
        return {str(a): str(b) for a, b in zip(S.sembol, S.sektor)}
    except (OSError, ValueError, AttributeError) as ex:
        k62log.warning("sektör dosyası okunamadı (%s): %s", yol, ex); return {}


# ---------------------------------------------------------------- 3) ÖLÇÜLER (saf işlevler; sentetik veriyle sınanır)
def k62_ceyreklik(M: pd.DataFrame) -> Dict[Tuple[str, int, int], Tuple[float, float]]:
    """Birikimli net kâr -> çeyreklik net kâr: Ç1 = birikimli(3 ay); Ç2..Ç4 = birikimli(q) - birikimli(q-1) (ikisi de varsa).
    Döner: {(kod, yil, ceyrek): (ceyreklik_kar, ozkaynak)}; eksik -> NaN."""
    bir = {(r.kod, int(r.yil), int(r.ceyrek)): (r.kar_bir, r.ozkaynak) for r in M.itertuples()}; out = {}
    for (k, y, c), (kb, oz) in bir.items():
        if c == 1:
            e = kb
        else:
            on = bir.get((k, y, c - 1), (np.nan, np.nan))[0]
            e = kb - on if (kb is not None and on is not None and np.isfinite(kb) and np.isfinite(on)) else np.nan
        out[(k, y, c)] = (float(e) if e is not None and np.isfinite(e) else np.nan, float(oz) if oz is not None and np.isfinite(oz) else np.nan)
    return out


def _k62_kova(deger: np.ndarray, k: int) -> np.ndarray:
    """Değerleri k eşit kovaya böler (0 en küçük .. k-1 en büyük); sıra (değer, konum) ile kesin; kova = floor(k x sıra / n)."""
    n = len(deger); sira = np.empty(n, int); sira[np.lexsort((np.arange(n), deger))] = np.arange(n)
    return (k * sira // n).astype(int)


def k62_portfoy_ata(D: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """2 x 3 büyüklük - DD/PD portföy kimliği [gün x hisse] (-1: yok). Her Y yılı Haziran sonunda: büyüklük = Haziran son işlem günü piyasa
    değeri (2 kova); DD/PD = (Y-1) yıl sonu özkaynağı / (Y-1) Aralık son işlem günü piyasa değeri (3 kova); bağımsız sıralama; özkaynağı <= 0
    olan dışarıda. Atama Temmuz Y ilk işlem gününden Haziran Y+1 son işlem gününe kadar geçerlidir (yalnız oluşum gününe kadarki bilgi)."""
    E = E or K62_ESIK; K = E["portfoy"]; tak = D["takvim"]; T, N = D["C"].shape; Pid = np.full((T, N), -1, np.int8)
    PDf = pd.DataFrame(D["PD"]).ffill(limit=5).to_numpy(); kol = {k: j for j, k in enumerate(D["kod"])}
    oz: Dict[int, np.ndarray] = {}
    for r in D["mali"][D["mali"].ceyrek == 4].itertuples():
        j = kol.get(r.kod)
        if j is not None and r.ozkaynak is not None and np.isfinite(r.ozkaynak):
            oz.setdefault(int(r.yil), np.full(N, np.nan))[j] = float(r.ozkaynak)
    for Y in range(tak[0].year, tak[-1].year + 1):
        iJ = _k62_son_gun(tak, f"{Y}-{K['olusum_ay']:02d}-30"); iD = _k62_son_gun(tak, f"{Y - 1}-12-31")
        if iJ < 0 or iD < 0 or (Y - 1) not in oz or tak[iJ].year != Y or tak[iD].year != Y - 1:
            continue
        boyut, pdd, bv = PDf[iJ], PDf[iD], oz[Y - 1]
        with np.errstate(invalid="ignore"):
            ok = np.isfinite(boyut) & (boyut > 0) & np.isfinite(pdd) & (pdd > 0) & np.isfinite(bv) & (bv > 0)
        ix = np.flatnonzero(ok)
        if len(ix) < K["boyut_kova"] * K["dd_kova"] * K["min_hisse"]:
            continue
        pid = _k62_kova(boyut[ix], K["boyut_kova"]) * K["dd_kova"] + _k62_kova(bv[ix] / pdd[ix], K["dd_kova"])
        i0 = iJ + 1; i1 = _k62_son_gun(tak, f"{Y + 1}-{K['olusum_ay']:02d}-30")
        if i0 <= i1:
            Pid[i0:i1 + 1, ix] = pid.astype(np.int8)[None, :]
    return Pid


def k62_hazirla(D: Dict[str, Any], E: Optional[Dict[str, Any]] = None, deger: bool = True) -> Dict[str, Any]:
    """Panelden türetilenler. A = günlük getirisi VAR mı (o gün kapanış + önceki 5 işlem günü içinde kapanış); Pid = portföy kimliği; RpA = portföy
    getirisi VAR mı (o gün getirisi olan üye >= min_hisse). deger=True ise ayrıca R (günlük getiri), Rp (portföy eşit ağırlıklı getirisi), Rm
    (BIST-100 getirisi). deger=False (sayım modu) HİÇBİR getiri hesaplamaz."""
    E = E or K62_ESIK; K = E["portfoy"]; C = D["C"]; T, N = C.shape; nP = K["boyut_kova"] * K["dd_kova"]
    onc = np.vstack([np.full((1, N), np.nan), pd.DataFrame(C).ffill(limit=5).to_numpy()[:-1]])
    with np.errstate(invalid="ignore"):
        A = np.isfinite(C) & np.isfinite(onc) & (onc > 0) & (C > 0)
    Pid = k62_portfoy_ata(D, E); say = np.stack([((Pid == p) & A).sum(axis=1) for p in range(nP)], axis=1)
    out: Dict[str, Any] = {"A": A, "Pid": Pid, "RpA": say >= K["min_hisse"]}
    if deger:
        with np.errstate(invalid="ignore", divide="ignore"):
            R = np.where(A, C / onc - 1.0, np.nan); Rp = np.full((T, nP), np.nan)
            for p in range(nP):
                m = (Pid == p) & A; Rp[:, p] = np.where(say[:, p] >= K["min_hisse"], np.where(m, R, 0.0).sum(axis=1) / np.maximum(say[:, p], 1), np.nan)
            X = np.asarray(D["X"], float); Rm = np.full(T, np.nan); Rm[1:] = X[1:] / X[:-1] - 1.0
        out.update({"R": R, "Rp": Rp, "Rm": Rm})
    return out


def _k62_altut(ri: np.ndarray, rp: np.ndarray, var: np.ndarray) -> Tuple[float, int]:
    """Al-tut anormal getiri: prod(1 + r_i) - prod(1 + r_p). Hissenin getirisi olmayan günde hisse eşleşen portföyün getirisini alır (makale dipnot
    5: kotasyondan çıkan hisse kalan günlerde portföy getirisini kazanır); portföy getirisi de yoksa o gün ikisi de 0. Döner: (değer, var gün)."""
    ok = var & np.isfinite(ri) & np.isfinite(rp); p = np.where(np.isfinite(rp), rp, 0.0); i = np.where(ok, ri, p)
    return float(np.prod(1.0 + i) - np.prod(1.0 + p)), int(ok.sum())


def k62_olay_tablosu(D: Dict[str, Any], E: Optional[Dict[str, Any]] = None, deger: bool = True, H: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Her açıklama için olay satırı. t = yayın gününe eşit ya da sonraki ilk işlem günü; karar günü = t+1 (EAR o günün kapanışında bilinir); giriş
    günü = t+2. Bayraklar (yalnız VAR / YOK): f_mali (E_q, E_{q-4}, MV_q), f_boyut (önceki yıl sonu PD > 100 mn $), f_defter (önceki yıl sonu
    özkaynak >= 0), f_portfoy, f_ear, f_on ([t-61, t-2] getirilerinin >= 2/3'ü), f_lag (0 < yayın - çeyrek sonu <= lag_max gün), f_giris, f_car
    ([t+2, t+61] takvimde ve getirilerinin >= 2/3'ü). onsel = karar gününde bilinen şartların hepsi; tam = onsel + f_car (makale örneklemi).
    deger=True ise SUETF, EAR, CAR21 / CAR41 / CAR61 ve kontrol değişkenleri de hesaplanır; deger=False (sayım) hiçbir getiri / sürpriz DEĞERİ üretmez."""
    E = E or K62_ESIK; O, Or = E["olay"], E["ornek"]; H = H or k62_hazirla(D, E, deger); tak = D["takvim"]; T = len(tak)
    kol = {k: j for j, k in enumerate(D["kod"])}; Q = k62_ceyreklik(D["mali"]); A, Pid, RpA = H["A"], H["Pid"], H["RpA"]
    PDf = pd.DataFrame(D["PD"]).ffill(limit=5).to_numpy(); PUf = pd.DataFrame(D["PDU"]).ffill(limit=5).to_numpy()
    U = D["duyuru"].reset_index(drop=True); e0, e1 = O["ear"]; c0 = O["car"]["bas"]; cN = O["car"]["ana"]; p0, p1 = O["on_pencere"]; pay = O["getiri_pay"]
    gun = pd.to_datetime(U.yayin).dt.normalize(); ti = tak.searchsorted(gun.to_numpy(), side="left")
    ayni = pd.Series(ti).value_counts().to_dict(); sat = []
    for r, t in zip(U.itertuples(), ti):
        j = kol.get(r.kod); t = int(t)
        if j is None:
            continue
        y, c = int(r.yil), int(r.ceyrek); qs = pd.Timestamp(year=y, month=3 * c, day=1) + pd.offsets.MonthEnd(0)
        lag = int((gun.iloc[r.Index] - qs).days); iq = _k62_son_gun(tak, qs); iy = _k62_son_gun(tak, f"{y - 1}-12-31")
        eq, e4 = Q.get((r.kod, y, c), (np.nan, np.nan))[0], Q.get((r.kod, y - 1, c), (np.nan, np.nan))[0]
        bv = Q.get((r.kod, y - 1, 4), (np.nan, np.nan))[1]
        mv = PDf[iq, j] if iq >= 0 and tak[iq] > qs - pd.Timedelta(days=10) else np.nan
        pu = PUf[iy, j] if iy >= 0 and tak[iy].year == y - 1 else np.nan; pt = PDf[iy, j] if iy >= 0 and tak[iy].year == y - 1 else np.nan
        row: Dict[str, Any] = {"kod": r.kod, "yil": y, "ceyrek": c, "mali_ceyrek": f"{y}Q{c}", "yayin": r.yayin, "t_i": t, "t": tak[t] if t < T else pd.NaT,
                               "karar_i": t + 1, "giris": tak[t + O["car"]["bas"]] if t + O["car"]["bas"] < T else pd.NaT, "lag": lag}
        row["f_mali"] = bool(np.isfinite(eq) and np.isfinite(e4) and np.isfinite(mv) and mv > 0)
        row["f_boyut"] = bool(np.isfinite(pu) and pu > Or["pd_usd_min"]); row["f_defter"] = bool(np.isfinite(bv) and bv >= Or["defter_min"])
        row["f_lag"] = bool(Or["lag_min"] <= lag <= Or["lag_max"]); row["f_giris"] = bool(t + c0 < T)
        ic = t + e0 >= 1 and t + e1 < T; pid = int(Pid[t, j]) if t < T else -1
        row["f_portfoy"] = bool(pid >= 0)
        row["f_ear"] = bool(ic and pid >= 0 and A[t + e0:t + e1 + 1, j].sum() >= math.ceil(pay * (e1 - e0 + 1) - 1e-9) and RpA[t + e0:t + e1 + 1, pid].all())
        row["f_on"] = bool(t + p0 >= 1 and t + p1 < T and A[t + p0:t + p1 + 1, j].sum() >= math.ceil(pay * (p1 - p0 + 1) - 1e-9))
        row["f_car"] = bool(t + cN < T and A[t + c0:t + cN + 1, j].sum() >= math.ceil(pay * (cN - c0 + 1) - 1e-9))
        row["onsel"] = bool(row["f_mali"] and row["f_boyut"] and row["f_defter"] and row["f_lag"] and row["f_giris"] and row["f_portfoy"] and row["f_ear"] and row["f_on"])
        row["tam"] = bool(row["onsel"] and row["f_car"])
        if deger:
            R, Rp, Rm = H["R"], H["Rp"], H["Rm"]
            row["SUETF"] = float((eq - e4) / mv) if row["f_mali"] else np.nan
            row["EAR"] = _k62_altut(R[t + e0:t + e1 + 1, j], Rp[t + e0:t + e1 + 1, pid], A[t + e0:t + e1 + 1, j])[0] if row["f_ear"] else np.nan
            for n in O["car"]["ufuk"]:
                row[f"CAR{n}"] = _k62_altut(R[t + c0:t + n + 1, j], Rp[t + c0:t + n + 1, pid], A[t + c0:t + n + 1, j])[0] if (row["f_car"] and pid >= 0) else np.nan
            row.update(_k62_kontroller(R[t + p0:t + p1 + 1, j], Rm[t + p0:t + p1 + 1], D["HU"][t + p0:t + p1 + 1, j], A[t + p0:t + p1 + 1, j]) if row["f_on"]
                       else {"IVOL": np.nan, "BETA": np.nan, "PRERET": np.nan, "ILLIQUIDITY": np.nan})
            row.update({"SIZE": float(pu / 1e6) if np.isfinite(pu) else np.nan, "BM": float(bv / pt) if (np.isfinite(bv) and np.isfinite(pt) and pt > 0) else np.nan,
                        "REPORTLAG": float(lag), "CONCEARNINGS": float(ayni.get(t, 1)), "FRIDUM": float(tak[t].dayofweek == 4) if t < T else np.nan})
        sat.append(row)
    Ev = pd.DataFrame(sat)
    if len(Ev):
        Ev["sektor"] = [D.get("sektor", {}).get(k, "BILINMIYOR") for k in Ev.kod]
    return Ev


def _k62_kontroller(ri: np.ndarray, rm: np.ndarray, hu: np.ndarray, var: np.ndarray) -> Dict[str, float]:
    """[t-61, t-2] penceresi: BETA ve IVOL (R_i = a + b R_m; kalıntı standart sapması), PRERET (al-tut - BIST-100 al-tut), ILLIQUIDITY
    (ort. ln(1 + |R| / hacim); hacim milyon USD: makaledeki enflasyon düzeltmeli TL hacmin yerine, SAPMA)."""
    ok = var & np.isfinite(ri) & np.isfinite(rm); out = {"IVOL": np.nan, "BETA": np.nan, "PRERET": np.nan, "ILLIQUIDITY": np.nan}
    if ok.sum() >= 10:
        x, y = rm[ok], ri[ok]; vx = float(((x - x.mean()) ** 2).sum())
        if vx > 0:
            b = float(((x - x.mean()) * (y - y.mean())).sum() / vx); a = float(y.mean() - b * x.mean()); k = y - a - b * x
            out["BETA"] = b; out["IVOL"] = float(np.sqrt((k ** 2).sum() / max(len(k) - 2, 1)))
        out["PRERET"] = float(np.prod(1.0 + y) - np.prod(1.0 + x))
    with np.errstate(invalid="ignore", divide="ignore"):
        h = ok & np.isfinite(hu) & (hu > 0)
        if h.sum() >= 10:
            out["ILLIQUIDITY"] = float(np.mean(np.log1p(np.abs(ri[h]) / (hu[h] / 1e6))))
    return out


def k62_tertil(deger: np.ndarray, ceyrek: np.ndarray, kod: np.ndarray, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """MAKALE tertili (A / B): mali çeyrek İÇİNDE sıra -> 0 (Q1, en olumsuz) / 1 / 2 (Q3, en olumlu); eşitlik hisse koduyla bozulur. Değeri olmayan
    ya da çeyreğinde min_ceyrek_olay'dan az olay bulunan satır -1. (Çeyreğin sonradan açıklayanlarını da kullanır: makaledeki gibi; ileriye bakar.)"""
    O = (E or K62_ESIK)["olay"]; out = np.full(len(deger), -1, int); deger = np.asarray(deger, float); ceyrek = np.asarray(ceyrek); kod = np.asarray(kod)
    for q in pd.unique(ceyrek):
        ix = np.flatnonzero((ceyrek == q) & np.isfinite(deger))
        if len(ix) < O["min_ceyrek_olay"]:
            continue
        ix = ix[np.lexsort((kod[ix], deger[ix]))]; out[ix] = O["tertil"] * np.arange(len(ix)) // len(ix)
    return out


def k62_tertil_onsel(Ev: pd.DataFrame, kolon: str, E: Optional[Dict[str, Any]] = None, haric: Optional[List[List[int]]] = None) -> np.ndarray:
    """GELECEĞE BAKMAYAN tertil (C): olayın sınıfı, ÖNCEKİ mali çeyreğin karar günü bu olayın karar gününden geç olmayan olaylarının aynı ölçüdeki
    1/3 ve 2/3 dilim değerleriyle belirlenir: değer >= üst kesim -> 2 (Q3); <= alt kesim -> 0 (Q1); arası 1. Havuz < tertil_onceki_min ise -1.
    haric (mali çeyrek listesi; TMS 29 kirli çeyrekleri): bu çeyreklerin olayları sınıfsızdır ve havuz olamazlar; havuz en yakın önceki temiz
    çeyrektir (en çok havuz_geri çeyrek geride; yoksa sınıfsız)."""
    C = (E or K62_ESIK)["bolum_c"]; out = np.full(len(Ev), -1, int); v = Ev[kolon].to_numpy(float); ki = Ev.karar_i.to_numpy(int)
    grup: Dict[Tuple[int, int], np.ndarray] = {k: np.asarray(ix) for k, ix in Ev.groupby(["yil", "ceyrek"]).indices.items()}
    kirli = {(int(a), int(b)) for a, b in (haric or [])}
    for (y, c), ix in grup.items():
        if (y, c) in kirli:
            continue
        on = None; yy, cc = y, c
        for _ in range(C["havuz_geri"] if kirli else 1):
            yy, cc = (yy, cc - 1) if cc > 1 else (yy - 1, 4)
            if (yy, cc) not in kirli:
                on = grup.get((yy, cc)); break
        if on is None:
            continue
        on = on[np.isfinite(v[on])]; sira = np.argsort(ki[on], kind="stable"); ok, ov = ki[on][sira], v[on][sira]
        for i in ix:
            if not np.isfinite(v[i]):
                continue
            n = int(np.searchsorted(ok, ki[i], side="right"))
            if n < C["tertil_onceki_min"]:
                continue
            alt, ust = np.quantile(ov[:n], [1.0 / 3.0, 2.0 / 3.0])
            out[i] = 2 if v[i] >= ust else (0 if v[i] <= alt else 1)
    return out


def k62_tekil(Ev: pd.DataFrame, gun: Optional[int] = None, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Aynı hissede 'gun' işlem günü içinde tekrarlanan olaylardan yalnız ilki (t_i sırasıyla; tutulan olaydan sonra < gun uzaklıktakiler düşer)."""
    gun = int(gun if gun is not None else (E or K62_ESIK)["protokol"]["tekil_gun"]); sec = []; son: Dict[str, int] = {}
    for r in Ev.sort_values(["t_i", "kod"]).itertuples():
        if r.kod in son and r.t_i - son[r.kod] < gun:
            continue
        son[r.kod] = int(r.t_i); sec.append(r.Index)
    return Ev.loc[sec]


def k62_winsor(x: np.ndarray, grup: np.ndarray, sinir: Tuple[float, float]) -> np.ndarray:
    """Grup (mali çeyrek) içi %alt / %üst dilim değerlerine kırpma (makale: sürekli değişkenler çeyreklik dağılımın %1 ve %99'unda kırpılır)."""
    x = np.asarray(x, float).copy(); grup = np.asarray(grup)
    for g in pd.unique(grup):
        m = (grup == g) & np.isfinite(x)
        if m.sum() >= 2:
            a, b = np.quantile(x[m], sinir); x[m] = np.clip(x[m], a, b)
    return x


# ---------------------------------------------------------------- 4) İSTATİSTİK
def _k62_betai(a: float, b: float, x: float) -> float:
    """Düzenlenmiş eksik beta işlevi I_x(a, b) (sürekli kesir; Student t olasılığı için)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x)

    def kesir(a: float, b: float, x: float) -> float:
        kucuk = 1e-300; qab, qap, qam = a + b, a + 1.0, a - 1.0; c = 1.0; d = 1.0 - qab * x / qap
        d = 1.0 / (d if abs(d) > kucuk else kucuk); h = d
        for m in range(1, 400):
            m2 = 2 * m; aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > kucuk else kucuk); c = 1.0 + aa / c; c = c if abs(c) > kucuk else kucuk; h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > kucuk else kucuk); c = 1.0 + aa / c; c = c if abs(c) > kucuk else kucuk; de = d * c; h *= de
            if abs(de - 1.0) < 3e-14:
                break
        return h
    if x < (a + 1.0) / (a + b + 2.0):
        return math.exp(lb) * kesir(a, b, x) / a
    return 1.0 - math.exp(lb) * kesir(b, a, 1.0 - x) / b


def k62_t_p(t: float, sd: float) -> float:
    """Student t iki yanlı p değeri (sd serbestlik derecesi)."""
    if not (np.isfinite(t) and sd > 0):
        return float("nan")
    return float(_k62_betai(sd / 2.0, 0.5, sd / (sd + t * t)))


def k62_ols_kume(y: np.ndarray, X: np.ndarray, kume: np.ndarray) -> Dict[str, Any]:
    """EKK + kümeye göre sağlam standart hata (CR1: G/(G-1) x (N-1)/(N-K)); p değeri t(G-1). Döner: katsayi, se, t, p, n, G."""
    y = np.asarray(y, float); X = np.asarray(X, float); n, k = X.shape; kume = np.asarray(kume)
    XtXi = np.linalg.pinv(X.T @ X); b = XtXi @ X.T @ y; u = y - X @ b; et = np.zeros((k, k)); G = 0
    for g in pd.unique(kume):
        m = kume == g; s = X[m].T @ u[m]; et += np.outer(s, s); G += 1
    if G < 2 or n <= k:
        nan = np.full(k, np.nan); return {"katsayi": b, "se": nan, "t": nan, "p": nan, "n": n, "G": G}
    V = XtXi @ et @ XtXi * (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    with np.errstate(invalid="ignore", divide="ignore"):
        t = np.where(se > 0, b / se, np.nan)
    return {"katsayi": b, "se": se, "t": t, "p": np.array([k62_t_p(x, G - 1) for x in t]), "n": n, "G": G}


def k62_bh(p: np.ndarray, q: float) -> np.ndarray:
    """Benjamini-Hochberg: yanlış keşif oranı q'da reddedilenler (NaN p reddedilmez)."""
    p = np.asarray(p, float); out = np.zeros(len(p), bool); ix = np.flatnonzero(np.isfinite(p)); m = len(ix)
    if not m:
        return out
    s = ix[np.argsort(p[ix], kind="stable")]; gec = np.flatnonzero(p[s] <= q * (np.arange(1, m + 1) / m))
    if len(gec):
        out[s[:gec[-1] + 1]] = True
    return out


def k62_pead(car: np.ndarray, sinif: np.ndarray, kume: np.ndarray, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """PEAD = ort. CAR(Q3) - ort. CAR(Q1). t ve p: Q1 ve Q3 olaylarında CAR'ın Q3 kuklasına EKK'si, kümeye (mali çeyrek) göre sağlam hata.
    Uçların ortalaması için ayrı sabitli EKK (kümeli). Güven aralığı: küme (mali çeyrek) yeniden örneklemeli bootstrap. Medyanlar ve medyan farkı."""
    P = (E or K62_ESIK)["protokol"]; car = np.asarray(car, float); sinif = np.asarray(sinif); kume = np.asarray(kume)
    ok = np.isfinite(car) & (sinif >= 0); car, sinif, kume = car[ok], sinif[ok], kume[ok]; ust = int(sinif.max()) if len(sinif) else 2
    q1, q3 = sinif == 0, sinif == ust; out: Dict[str, Any] = {"n": int(len(car)), "n_q1": int(q1.sum()), "n_q3": int(q3.sum()), "kume": int(len(pd.unique(kume)))}
    for ad in ("ort_q1", "ort_q2", "ort_q3", "med_q1", "med_q3", "pead", "pead_medyan", "t", "p", "alt", "ust", "t_q1", "p_q1", "t_q3", "p_q3", "alt_q1", "ust_q1", "alt_q3", "ust_q3"):
        out[ad] = np.nan
    if not (q1.sum() >= 2 and q3.sum() >= 2):
        return out
    out.update({"ort_q1": float(car[q1].mean()), "ort_q3": float(car[q3].mean()), "med_q1": float(np.median(car[q1])), "med_q3": float(np.median(car[q3]))})
    orta = (sinif > 0) & (sinif < ust)
    out["ort_q2"] = float(car[orta].mean()) if orta.any() else np.nan
    out["pead"] = out["ort_q3"] - out["ort_q1"]; out["pead_medyan"] = out["med_q3"] - out["med_q1"]
    m = q1 | q3; r = k62_ols_kume(car[m], np.column_stack([np.ones(int(m.sum())), q3[m].astype(float)]), kume[m]); out["t"], out["p"] = float(r["t"][1]), float(r["p"][1])
    for ad, mm in (("q1", q1), ("q3", q3)):
        r = k62_ols_kume(car[mm], np.ones((int(mm.sum()), 1)), kume[mm]); out[f"t_{ad}"], out[f"p_{ad}"] = float(r["t"][0]), float(r["p"][0])
    kl = pd.unique(kume); G = len(kl); kod = pd.Series(np.arange(G), index=kl).reindex(kume).to_numpy()
    s1 = np.bincount(kod[q1], car[q1], G); n1 = np.bincount(kod[q1], minlength=G).astype(float); s3 = np.bincount(kod[q3], car[q3], G); n3 = np.bincount(kod[q3], minlength=G).astype(float)
    cek = np.random.default_rng(P["tohum"]).integers(0, G, size=(P["bootstrap"], G))
    with np.errstate(invalid="ignore", divide="ignore"):
        b1 = s1[cek].sum(axis=1) / n1[cek].sum(axis=1); b3 = s3[cek].sum(axis=1) / n3[cek].sum(axis=1)
    for ad, dizi in (("", b3 - b1), ("_q1", b1), ("_q3", b3)):
        d = dizi[np.isfinite(dizi)]
        if len(d) >= 0.5 * P["bootstrap"]:
            out["alt" + ad], out["ust" + ad] = (float(x) for x in np.percentile(d, P["guven"]))
    return out


def k62_regresyon(Ev: pd.DataFrame, olcu_sinif: np.ndarray, car_kol: str, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Makale denklem 4: CAR = a0 + a1 PUAN + toplam(b X) + toplam(c PUAN x X) + sektör ve mali çeyrek sabit etkileri; küme = mali çeyrek.
    PUAN = tertil / 2 (0, 0,5, 1); X standartlaştırılmış kontroller (SIZE logaritmik); IO yok (SAPMA). Döner: a1, t, p, n, G, kontrol katsayıları."""
    E = E or K62_ESIK; Rg = E["regresyon"]; W = E["olay"]["winsor"]; kon = list(Rg["kontrol"])
    ok = (olcu_sinif >= 0) & np.isfinite(Ev[car_kol].to_numpy(float)) & np.all(np.isfinite(Ev[kon].to_numpy(float)), axis=1) & (Ev.SIZE.to_numpy(float) > 0)
    if ok.sum() < 50:
        return {"n": int(ok.sum()), "a1": np.nan, "t": np.nan, "p": np.nan, "G": 0}
    X_ = Ev.loc[ok]; q = X_.mali_ceyrek.to_numpy(); puan = olcu_sinif[ok] / float(E["olay"]["tertil"] - 1); y = k62_winsor(X_[car_kol].to_numpy(float), q, W)
    kol = [np.ones(len(X_)), puan]; ad = ["sabit", "PUAN"]
    for k in kon:
        x = X_[k].to_numpy(float); x = np.log(x) if k == "SIZE" else x
        x = k62_winsor(x, q, W) if k != "FRIDUM" else x; sd = x.std(ddof=1); z = (x - x.mean()) / sd if sd > 0 else np.zeros(len(x))
        kol += [z, puan * z]; ad += [k, "PUANx" + k]
    for etki in Rg["sabit_etki"]:
        duz = pd.unique(X_[etki].to_numpy())
        for d in duz[1:]:
            kol.append((X_[etki].to_numpy() == d).astype(float)); ad.append(f"{etki}={d}")
    r = k62_ols_kume(y, np.column_stack(kol), q)
    return {"n": int(r["n"]), "G": int(r["G"]), "a1": float(r["katsayi"][1]), "t": float(r["t"][1]), "p": float(r["p"][1]),
            "katsayi": {a: float(b) for a, b in zip(ad, r["katsayi"]) if "=" not in a}, "t_hepsi": {a: float(b) for a, b in zip(ad, r["t"]) if "=" not in a}}


# ---------------------------------------------------------------- 5) KAPSAM (yalnız sayım; getiri / sürpriz değeri hesaplanmaz)
def _k62_vbist_yukle(yol: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    """V_BIST.pkl (FON_IZI fi_k1_veri çıktısı; islenmis-veri dalı): {sembol: OHLCV}. Proje cetveli (FI_OLCUT) bu panelde ölçülür."""
    import pickle
    yol = yol or K62_YOL["v_bist"]
    if not os.path.exists(yol):
        raise K62Hata(f"{yol} yok: `git worktree add /tmp/iv origin/islenmis-veri` + `python FON_IZI.py vpac /tmp/iv/veri /tmp/veri`")
    with open(yol, "rb") as f:
        V = pickle.load(f)
    return V["veri"] if isinstance(V, dict) and isinstance(V.get("veri"), dict) else V


def _k62_a_maske(Ev: pd.DataFrame, E: Dict[str, Any]) -> np.ndarray:
    a, b = E["bolum_a"]["mali_bas"], E["bolum_a"]["mali_bit"]; k = Ev.yil.to_numpy(int) * 10 + Ev.ceyrek.to_numpy(int)
    return (k >= a[0] * 10 + a[1]) & (k <= b[0] * 10 + b[1])


def _k62_haric_maske(Ev: pd.DataFrame, haric: List[List[int]]) -> np.ndarray:
    """Mali çeyreği 'haric' listesinde olan olaylar (TMS 29 kirli çeyrekleri)."""
    k = Ev.yil.to_numpy(int) * 10 + Ev.ceyrek.to_numpy(int)
    return np.isin(k, [int(a) * 10 + int(b) for a, b in haric])


def _k62_t_maske(Ev: pd.DataFrame, a: str, b: str) -> np.ndarray:
    t = pd.to_datetime(Ev.t)
    return ((t >= pd.Timestamp(a)) & (t <= pd.Timestamp(b))).to_numpy()


def k62_kapsam(veri: Optional[str] = None, cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None, demet: Optional[Dict[str, Any]] = None,
               v_semboller: Optional[List[str]] = None) -> Dict[str, Any]:
    """Kapsam sayımı: kaç hisse, kaç açıklama, bölüm / dönem başına kaç olay, ölçüsü HESAPLANABİLEN olay sayısı. Olay tablosu deger=False ile
    kurulur: getiri, CAR, EAR, SUETF DEĞERİ üretilmez (yalnız veri var / yok bayrakları). k62_kapsam.json yazılır."""
    E = E or K62_ESIK; sentetik = demet is not None; D = demet if sentetik else k62_demet_kur(veri, E)
    Ev = k62_olay_tablosu(D, E, deger=False); yasak = [k for k in Ev.columns if k in ("SUETF", "EAR", "SUEAF") or k.startswith("CAR")]
    if yasak:
        raise K62Hata(f"sayım modunda değer sütunu üretildi: {yasak}")
    if v_semboller is None:
        try:
            v_semboller = sorted(_k62_vbist_yukle())
        except (K62Hata, OSError, ValueError) as ex:
            k62log.warning("V_BIST okunamadı (%s): C bölümü sayımı boş", ex); v_semboller = []
    vs = set(v_semboller); tak = D["takvim"]; son = np.array([np.flatnonzero(np.isfinite(D["C"][:, j]))[-1] if np.isfinite(D["C"][:, j]).any() else -1 for j in range(len(D["kod"]))])
    cikan = {k for k, s in zip(D["kod"], son) if s < len(tak) - 21}
    bay = ["f_mali", "f_boyut", "f_defter", "f_lag", "f_portfoy", "f_ear", "f_on", "f_giris", "f_car", "onsel", "tam"]

    def say(m: np.ndarray) -> Dict[str, Any]:
        X = Ev[m]
        return {"aciklama": int(len(X)), "hisse": int(X.kod.nunique()), **{b: int(X[b].sum()) for b in bay}, "tam_hisse": int(X[X.tam].kod.nunique()),
                "tam_mali_ceyrek": int(X[X.tam].mali_ceyrek.nunique()), "tam_cikan_hisse_olayi": int(X[X.tam].kod.isin(cikan).sum()),
                "SUETF_hesaplanabilir": int((X.tam & X.f_mali).sum()), "EAR_hesaplanabilir": int((X.tam & X.f_ear).sum()), "SUEAF_hesaplanabilir": 0,
                "onsel_vbist": int((X.onsel & X.kod.isin(vs)).sum()), "tam_vbist": int((X.tam & X.kod.isin(vs)).sum()),
                "tam_tms29_temiz": int((X.tam.to_numpy() & ~_k62_haric_maske(X, E["bolum_b"]["tms29_haric"])).sum()) if len(X) else 0}
    hepsi = np.ones(len(Ev), bool); am = _k62_a_maske(Ev, E) if len(Ev) else hepsi
    M = D["mali"]; U = D["duyuru"]
    out: Dict[str, Any] = {"surum": K62_SURUM, "zaman_utc": _k62_simdi(), "sentetik": sentetik, "muhur": k62_esik_sha(E),
                           "veri": None if sentetik else k62_veri_sha(veri),
                           "kap": {"finansal_rapor_kaydi": int(D.get("kap_kayit", 0)), "aciklama_hisse_ceyrek": int(len(U)),
                                   "ilk_yayin": str(pd.to_datetime(U.yayin).min()) if len(U) else None, "son_yayin": str(pd.to_datetime(U.yayin).max()) if len(U) else None,
                                   "yila_gore": {str(k): int(v) for k, v in pd.to_datetime(U.yayin).dt.year.value_counts().sort_index().items()} if len(U) else {}},
                           "fiyat": {"hisse": int(len(D["kod"])), "islem_gunu": int(len(tak)), "ilk_gun": str(tak[0].date()), "son_gun": str(tak[-1].date()),
                                     "kotasyondan_cikan_hisse": int(len(cikan)), "v_bist_hisse": int(len(vs)), "v_bist_te_olan": int(len(vs & set(D["kod"])))},
                           "mali": {"hisse": int(M.kod.nunique()) if len(M) else 0, "satir": int(len(M)), "ilk_yil": int(M.yil.min()) if len(M) else None,
                                    "son_yil": int(M.yil.max()) if len(M) else None, "grup": {str(k): int(v) for k, v in M.drop_duplicates("kod").grup.value_counts().items()} if len(M) else {}},
                           "olay": {"hepsi": say(hepsi) if len(Ev) else {}}, "makale_n": {"tam": E["makale"]["n_tam"], "analist": E["makale"]["n_analist"]}}
    if len(Ev):
        out["olay"]["A"] = say(am); X = Ev[am & Ev.tam.to_numpy()]
        out["olay"]["A_ceyrek_basina_tam"] = {str(k): int(v) for k, v in X.mali_ceyrek.value_counts().sort_index().items()}
        out["olay"]["A_mali_ceyrek_olay_alt_sinir_alti"] = int((X.mali_ceyrek.value_counts() < E["olay"]["min_ceyrek_olay"]).sum())
        for ad, a, b in E["bolum_b"]["donem"]:
            out["olay"]["B " + ad] = say(_k62_t_maske(Ev, a, b))
    if not sentetik or cikti:
        _k62_json_yaz(_k62_yol("kapsam", cikti), out)
    return out


# ---------------------------------------------------------------- 6) ÖN KAYIT
_K62_OC_DESEN = {"sha": r"MÜHÜR \(K62_ESIK \+ FI_OLCUT sha256\): `([0-9a-f]{64})`", "veri_sha256": r"VERİ \(önbellek sha256\): `([0-9a-f]{64}|yok)`",
                 "v_bist_sha256": r"V_BIST\.pkl \(sha256\): `([0-9a-f]{64}|yok)`", "zaman_utc": r"ZAMAN \(UTC\): `([^`]+)`"}


def _k62_yz(x: float, n: int = 1) -> str:
    return ("%" + f"{100 * x:.{n}f}").replace(".", ",")


def k62_onkayit_metni(E: Optional[Dict[str, Any]] = None, kapsam: Optional[Dict[str, Any]] = None, veri_sha: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt metni (K62_ESIK'ten üretilir; sayılar koddaki sabitlerle aynıdır)."""
    import FON_IZI as FI
    E = E or K62_ESIK; Mk, O, Or, Pf, A, B, C, Pr, Rg, Vr = (E[k] for k in ("makale", "olay", "ornek", "portfoy", "bolum_a", "bolum_b", "bolum_c", "protokol", "regresyon", "veri"))
    FO = FI.FI_OLCUT; vs = veri_sha or {}; ks = kapsam or {}; ol = ks.get("olay", {}); kA = ol.get("A", {})
    pe, tt = Mk["pead"], Mk["t"]

    def ksat(ad: str, x: Dict[str, Any]) -> str:
        return (f"| {ad} | {x.get('aciklama', '—')} | {x.get('hisse', '—')} | {x.get('f_mali', '—')} | {x.get('f_boyut', '—')} | {x.get('f_ear', '—')} | {x.get('onsel', '—')} | "
                f"{x.get('tam', '—')} | {x.get('tam_hisse', '—')} | {x.get('tam_mali_ceyrek', '—')} | {x.get('tam_cikan_hisse_olayi', '—')} | {x.get('onsel_vbist', '—')} |")
    kapsam_tablo = "\n".join([ksat("A (mali çeyrek %dÇ%d-%dÇ%d)" % (A["mali_bas"][0], A["mali_bas"][1], A["mali_bit"][0], A["mali_bit"][1]), kA)]
                             + [ksat("B " + d[0], ol.get("B " + d[0], {})) for d in B["donem"]] + [ksat("hepsi", ol.get("hepsi", {}))])
    kp, fy, ml = ks.get("kap", {}), ks.get("fiyat", {}), ks.get("mali", {})
    return f"""# K62 ÖN KAYIT — BIST PEAD birebir tekrar (Ahlatcıoğlu & Okay 2021)

{K62_SURUM}

- MÜHÜR (K62_ESIK + FI_OLCUT sha256): `{k62_esik_sha(E)}`
- VERİ (önbellek sha256): `{vs.get('sha256') or 'yok'}`
- V_BIST.pkl (sha256): `{vs.get('v_bist_sha256') or 'yok'}`
- ZAMAN (UTC): `{_k62_simdi()}`

Bu dosya ölçümden ÖNCE yazıldı. Yazıldığı anda gerçek veride sürprize bağlı hiçbir getiri / CAR / fark hesaplanmadı (yalnız indirme ve sayım:
`python K62.py indir`, `python K62.py kapsam`). `python -I K62.py kos` bu dosyanın mührünü, git'e işlenmiş ve değişmemiş olmasını ve veri
sha256'sını doğrulamadan ölçüm yapmaz. Sonuç görüldükten sonra bu dosyaya ve K62_ESIK'e kural / eşik eklenmez.

## 0. Kaynak makale ve yöntemi

- Künye: Aykut Ahlatcıoğlu, Nesrin Okay (2021). "Post-earnings announcement drift: Evidence from Turkey". Borsa Istanbul Review 21(1), 92-103.
  doi {Mk['doi']} (açık erişim, CC BY-NC-ND; çevrim içi Eylül 2020).
- Erişim: ScienceDirect tam metni bu ortamdan alınamadı (HTTP 403), EconStor kopyası bot engelinde. Yöntem ve tablolar aynı yazarın doktora tezinden
  okundu: A. Ahlatcıoğlu (2020), "Determinants of post-announcement drift and market reaction to earnings announcements", Boğaziçi Üniversitesi,
  3. bölüm "PEAD: Evidence from Turkey" (bölümün giriş paragrafı makale özetiyle kelimesi kelimesine aynı; %2,9 / %2,9 / %2,2 aynı).
  BİLİNMEYEN: makalenin teze göre olası küçük farkları (tablo numaraları, yuvarlama, hakem düzeltmeleri) doğrulanamadı.
- Örneklem: 2007-2018, çeyreklik kazanç açıklamaları; başlangıç 16.061 şirket-çeyrek, süzgeçlerden sonra TAM ÖRNEKLEM {Mk['n_tam']} gözlem; ANALİST ÖRNEKLEMİ {Mk['n_analist']} gözlem.
  Süzgeçler: (i) mali yılı Aralık'ta biten şirketler; (ii) bütün ölçü ve açıklayıcı değişkenlerin verisi var; (iii) önceki yıl sonu piyasa değeri
  > 100 milyon USD ve özkaynak negatif değil; CAR ve EAR pencerelerindeki günlük getirilerin en az 2/3'ü var. Sürekli değişkenler çeyreklik dağılımın
  %1 ve %99'unda kırpılır (winsorize). Kotasyondan çıkan hisse kalan günlerde eşleşen portföyün getirisini kazanır (dipnot 5).
- Veri kaynakları (makale): muhasebe verisi Rasyonet; piyasa verisi ve açıklama günü Bloomberg; kurumsal sahiplik MKK; sektör GICS (Compustat Global);
  analist tahmini 2014'e kadar CNBC-E anketleri, sonra Bloomberg anketleri (en az 1 tahmin).
- Ölçü 1, SUETF_(i,q) = (E_(i,q) - E_(i,q-4)) / MV_(i,q): mevsimsel rassal yürüyüş; E çeyreklik kazanç (TL), MV çeyrek sonu piyasa değeri.
- Ölçü 2, SUEAF_(i,q) = (E_(i,q) - F_(i,q)) / MV_(i,q): F analist tahminlerinin ortalaması.
- Ölçü 3, EAR_(i,q) = prod_(k=t-1..t+1)(1 + R_(i,k)) - prod_(k=t-1..t+1)(1 + R_(p,k)): açıklama günü t çevresinde üç işlem günü; p hissenin eşleştiği
  büyüklük-DD/PD portföyü. Portföyler: her yıl Haziran sonunda 2 büyüklük x 3 DD/PD grubu kesişimi (6 portföy); büyüklük = Haziran sonu piyasa
  değeri; DD/PD = önceki mali yıl sonu defter değeri / önceki Aralık sonu piyasa değeri; günlük EŞİT AĞIRLIKLI getiri, Temmuz t - Haziran t+1.
- Gruplama: üç ölçü de her takvim çeyreğinde sıraya göre TERTİL puanına çevrilir (0, 0,5, 1); Q1 en olumsuz, Q3 en olumlu.
- Sonuç ölçüsü: CAR[2,61]_(i,q) = prod_(k=t+2..t+61)(1 + R_(i,k)) - prod_(k=t+2..t+61)(1 + R_(p,k)) (60 işlem günü; ayrıca [2,21], [2,41]).
  PEAD[2,61] = ortalama CAR(Q3) - ortalama CAR(Q1) (üst üçte bir uzun, alt üçte bir kısa korunma portföyü; olay zamanı). p değerleri değişen varyansa
  dayanıklı, kazanç çeyreğine göre kümelenmiş standart hatayla.
- Kontrol değişkenleri (Tablo 5-6; CAR = a0 + a1 PUAN + b X + c PUAN x X; sektör ve çeyrek sabit etkisi; çeyreğe göre küme; X standartlaştırılmış):
  CONCEARNINGS (aynı gün açıklayan şirket sayısı), FRIDUM (Cuma), IVOL ([t-61, t-2] piyasa modeli kalıntı standart sapması, BIST-100), ILLIQUIDITY
  (ort. ln(1 + |R| / enflasyon düzeltmeli hacim, milyon TL), [t-61, t-2]), SIZE (önceki yıl sonu piyasa değeri, milyon USD; logaritması), REPORTLAG
  (çeyrek sonundan açıklamaya gün), IO (kurumsal sahiplik / halka açık pay), B/M, BETA ([t-61, t-2]), PRERET ([t-61, t-2] al-tut - BIST-100).
- BİLDİRİLEN SAYILAR (Tablo 3 Panel B "PEAD at Different Horizons"; t değerleri parantezde):

| ölçü | PEAD[2,21] | PEAD[2,41] | PEAD[2,61] |
|---|---|---|---|
| SUETF | {pe['SUETF']['21']:.4f} ({tt['SUETF']['21']}) | {pe['SUETF']['41']:.4f} ({tt['SUETF']['41']}) | {pe['SUETF']['61']:.4f} ({tt['SUETF']['61']}) |
| SUEAF | {pe['SUEAF']['21']:.4f} ({tt['SUEAF']['21']}) | {pe['SUEAF']['41']:.4f} ({tt['SUEAF']['41']}) | {pe['SUEAF']['61']:.4f} ({tt['SUEAF']['61']}) |
| EAR | {pe['EAR']['21']:.5f} ({tt['EAR']['21']}) | {pe['EAR']['41']:.4f} ({tt['EAR']['41']}) | {pe['EAR']['61']:.4f} ({tt['EAR']['61']}) |

  Özetteki %2,9 / %2,9 / %2,2 = PEAD[2,61] sütunu (SUETF / SUEAF / EAR). Kontrollü regresyonda ortalama şirket için PEAD[2,61]: SUETF
  {_k62_yz(Mk['regresyon_61']['SUETF'], 2)}, EAR {_k62_yz(Mk['regresyon_61']['EAR'], 2)} (Tablo 5-6). SUETF ile 12 yılın 11'inde, EAR ile 10'unda, SUEAF ile 9'unda artı.
  Aylık takvim portföyü alfaları (Tablo 7; Fama-French 3 faktör): SUETF %1,12, SUEAF %0,77, EAR %0,47.

## A. BİREBİR TEKRAR (makale tanımları; veri izin verdiği kadar)

A1. Veri: açıklama anı = KAP'ta o hisse - mali yıl - çeyrek için yayımlanan İLK 'Finansal Rapor' bildirimi (bildirim sınıfı {Vr['kap']['sinif']};
    liste {Vr['kap']['bas']} - {Vr['kap']['bit']}). Fiyat (bölünme ve temettü düzeltilmiş kapanış), piyasa değeri (TL ve USD), USD hacim, BIST-100: İş Yatırım
    günlük hisse verisi ({Vr['fiyat']['bas']} - {Vr['fiyat']['bit']}; kotasyondan çıkanlar dahil). Mali tablo: İş Yatırım çeyreklik tablolar ({Vr['mali']['bas_yil']}'den;
    grup sırası {', '.join(Vr['mali']['grup'])}; ilk dolu grup).
A2. t = yayın gününe eşit ya da ondan sonraki ilk işlem günü (saat ayrımı yok; makalede Bloomberg günü). EAR penceresi [t{O['ear'][0]}, t+{O['ear'][1]}]; CAR penceresi
    [t+{O['car']['bas']}, t+N], N = {', '.join(str(x) for x in O['car']['ufuk'])}; ana ufuk {O['car']['ana']}.
A3. E = net dönem kârının ana ortaklık payı (kalem {Vr['mali']['kar']}); çeyreklik = birikimli(q) - birikimli(q-1) (Ç1 = 3 aylık). MV_q = çeyreğin son işlem
    günü piyasa değeri (TL). SUETF = (E_q - E_(q-4)) / MV_q.
A4. Portföyler: {Pf['boyut_kova']} büyüklük x {Pf['dd_kova']} DD/PD kovası (eşit sayıda; bağımsız sıralama), Haziran sonu; özkaynağı <= 0 olan portföy dışı; bir portföyde o gün
    getirisi olan en az {Pf['min_hisse']} hisse yoksa portföy getirisi yok. Olayın portföyü t günündeki atamadır (pencere boyunca sabit).
A5. Örneklem: mali çeyrek {A['mali_bas'][0]}Ç{A['mali_bas'][1]} - {A['mali_bit'][0]}Ç{A['mali_bit'][1]}; E_q, E_(q-4), MV_q var; önceki mali yıl sonu piyasa değeri > {Or['pd_usd_min'] / 1e6:.0f} milyon USD; önceki
    yıl sonu özkaynak >= 0; t günü portföy ataması var; EAR, [t-61, t-2] ve CAR[2,61] pencerelerinde günlük getirilerin en az 2/3'ü var;
    {Or['lag_min']} <= açıklama - çeyrek sonu <= {Or['lag_max']} gün. Getirisi olmayan günde hisse portföy getirisini alır.
A6. Tertil: mali çeyrek içinde sıra (eşitlik hisse koduyla); çeyrekte en az {O['min_ceyrek_olay']} olay yoksa çeyrek ölçülmez. CAR çeyrek içi %{100 * O['winsor'][0]:.0f} / %{100 * O['winsor'][1]:.0f} kırpılır.
A7. Ölçülenler: {', '.join(A['olculen'])}. VERİ YOK: {', '.join(A['veri_yok'])} (ücretsiz tarihsel analist tahmini yok; tahmin uydurulmaz, vekil üretilmez).
A8. BAŞARI ÖLÇÜTÜ (önceden): bir ölçü 'YENİDEN ÜRETİLDİ' ⇔ PEAD[2,61] işareti makaledekiyle aynı VE nokta değeri makaledekinin ±{_k62_yz(A['basari_puan']).replace('%', '')} puanı içinde
    (SUETF: {_k62_yz(pe['SUETF']['61'] - A['basari_puan'], 2)} .. {_k62_yz(pe['SUETF']['61'] + A['basari_puan'], 2)}; EAR: {_k62_yz(pe['EAR']['61'] - A['basari_puan'], 2)} .. {_k62_yz(pe['EAR']['61'] + A['basari_puan'], 2)}). Ölçü bazında ayrı ayrı. SUEAF: 'VERİ YOK,
    yeniden üretilemedi'. İşaret aynı ama aralık dışı: 'YÖN AYNI, BÜYÜKLÜK FARKLI'; işaret ters: 'YENİDEN ÜRETİLEMEDİ'. [2,21] ve [2,41] bilgi.
    Kontrollü regresyon (PUAN katsayısı; makale {_k62_yz(Mk['regresyon_61']['SUETF'], 2)} / {_k62_yz(Mk['regresyon_61']['EAR'], 2)}) aynı ±{_k62_yz(A['basari_puan']).replace('%', '')} puan kuralıyla ayrıca yazılır (bilgi).

SAPMA listesi (veri yüzünden zorunlu; her biri sonucu etkileyebilir):
- SAPMA 1 (dönem): makale 2007Ç1-2018Ç4 (48 çeyrek). KAP 'Finansal Rapor' kayıtları Haziran 2009'da, İş Yatırım mali tabloları 2008/3'te başlıyor;
  tekrar örneklemi {A['mali_bas'][0]}Ç{A['mali_bas'][1]}-{A['mali_bit'][0]}Ç{A['mali_bit'][1]} (39 çeyrek). 2007Ç1-2009Ç1 (9 çeyrek; 2008 krizi dahil) YOK.
- SAPMA 2 (kaynak): Rasyonet / Bloomberg yerine İş Yatırım + KAP. Açıklama günü Bloomberg günü değil, KAP'taki ilk Finansal Rapor günü
  (bankalarda solo ve konsolide rapordan ilk gelen).
- SAPMA 3 (SUEAF): analist tahmini verisi yok; ölçü 2 ölçülmez.
- SAPMA 4 (IO): MKK kurumsal sahiplik verisi yok; örneklem şartında ve regresyonda yok.
- SAPMA 5 (ILLIQUIDITY): enflasyon düzeltmeli TL hacim yerine USD hacim (milyon USD).
- SAPMA 6 (sektör sabit etkisi): GICS yerine sektor_BIST.csv; listede olmayan (çoğu kotasyondan çıkmış) hisse 'BILINMIYOR' sınıfında.
- SAPMA 7 (Aralık mali yılı): özel hesap dönemli şirketlerin listesi yok; şart dolaylı: İş Yatırım'da 3/6/9/12. ay tablosu olması + açıklama
  gecikmesi {Or['lag_min']}-{Or['lag_max']} gün süzgeci (makalede bu süzgeç yok; REPORTLAG en büyük 785).
- SAPMA 8 (kazanç tanımı): makale 'reported earnings' der; burada net dönem kârı ana ortaklık payı; bankalarda solo tablo öncelikli (grup sırası).
- SAPMA 9 (yeniden sunum; KANITLI): İş Yatırım YILLIK (12 aylık) değerleri sonraki yılın raporundaki yeniden sunulmuş karşılaştırmalı değerle
  değiştirilmiş görünüyor. Kanıt (11 Kasım 2026, getiri hesabından önce): BIMAS 2022 birikimli net kâr 3 / 6 / 9 / 12 ay = 1,34 / 3,02 / 4,79 / 16,60
  milyar TL (12 aylık değer TMS 29 ile Aralık 2023 alım gücüne taşınmış; ilk açıklanan yaklaşık 8,2 milyar TL); 2024 / 12 değeri binliğe yuvarlı
  değil (24.328.622.067). Ara dönem (3 / 6 / 9 ay) değerleri ilk açıklandığı gibi duruyor. Sonuç: (a) mali 2022'den itibaren 4. çeyrek kazancı
  (birikimli 12 - birikimli 9) hem birim karışıklığı hem GELECEK BİLGİSİ içerir; (b) 2024 1.-3. çeyreklerde E_q enflasyon düzeltmeli, E_(q-4)
  nominaldir. Bu yüzden SUETF için mali çeyrek {', '.join(f"{a}Ç{b}" for a, b in B['tms29_haric'])} 'KİRLİ' sayılır (B3, C1). (c) Haziran 2023 ve sonrasındaki portföy
  oluşumlarında DD/PD yeniden sunulmuş özkaynağı kullanır (sınıflamada küçük ileriye bakma; düzeltilemedi). (d) 2022 öncesinde de yıllık değerler
  sonradan düzeltilmiş olabilir (doğrulanamadı; A'da olası küçük sızıntı). Mali yılı Ocak'ta biten MAVI gibi 1-2 şirket gecikme süzgecinden geçer.
- SAPMA 10 (çok faktörlü modeller, Tablo 7-8): kapsam dışı; ölçülmez.
- SAPMA 11 (takvim çeyreği): makale 'takvim çeyreği içinde sıra' der; burada mali çeyrek (kümeleme de mali çeyrek).

## B. DÖNEM (aynı ölçüler, aynı yöntem)

B1. A'daki yöntem (makale tertili, CAR[2,N], aynı örneklem süzgeçleri) açıklama günü t şu aralıklarda olan olaylara ayrı ayrı uygulanır:
    {'; '.join(f"{d[0]} ({d[1]} .. {d[2]})" for d in B['donem'])}. Tertil ve kırpma mali çeyrek içinde, bütün tam örneklem üzerinden bir kez yapılır.
B2. Fon krizi kesiği: fiyatlar {B['kriz']}'de kesilir (sonrası indirilmez); [t+2, t+61] penceresi bu tarihi aşan olay ölçülmez.
B3. TMS 29 (SAPMA 9): başlangıcı {B['tms29_bas_yil']} ve sonrası olan dönemlerde (2022-2026, 2023-2026) SUETF'in ANA satırı yalnız TEMİZ mali çeyreklerdir (kirli çeyrekler
    {', '.join(f"{a}Ç{b}" for a, b in B['tms29_haric'])} hariç); bütün çeyrekleri içeren satır 'kirli, bilgi' diye ayrıca yazılır. EAR'da çeyrek ayıklanmaz. 2017-2021 etkilenmez.
B4. Okuma (önceden): bir dönem-ölçü 'TUTAR' ⇔ PEAD[2,61] > 0, kümeli p < 0,05 ve BH düzeltmesinden sonra da reddedilir (D3). Aksi 'TUTMAZ'.

## C. PROJE CETVELİ (FON_IZI FI_OLCUT; karar günü bilgisiyle)

C1. Olaylar: 'onsel' örneklem (A5'in karar gününde bilinen şartları; CAR penceresi şartı YOK). Sürpriz sınıfı GELECEĞE BAKMADAN: olayın değeri, önceki
    mali çeyreğin (karar günü bu olayın karar gününden geç olmayan) olaylarının 1/3 ve 2/3 dilim değerleriyle kıyaslanır (>= üst: Q3; <= alt: Q1);
    havuz < {C['tertil_onceki_min']} ise olay sınıfsız. Karar günü = t+1 (EAR o günün kapanışında bilinir); GİRİŞ = t+{C['giris_gun']} işlem günü AÇILIŞI. SUETF'te TMS 29 kirli
    çeyreklerinin (B3) olayları sınıfsızdır ve havuz olamazlar; havuz en yakın önceki temiz çeyrektir (en çok {C['havuz_geri']} çeyrek geride; yoksa sınıfsız).
C2. Ölçüm: fi_olcut_panel / fi_olcut_olay / fi_olcut_hucre, V_BIST.pkl üzerinde (yalnız bugün işlem gören hisseler): r60 = 60. gün kapanışı / giriş açılışı - 1
    (kriz {FO['kriz']}'de kesik); EŞLİ FARK = r60 - aynı giriş günü aynı {FO['mom']} gün momentum beşliği x likidite üçlüsündeki öteki hisselerin ortalama r60'ı.
C3. Hücre TUTAR (Q3, iyi sürpriz): n >= {FO['n_esik']}; ortalama eşli fark > 0 ve ay kümeli bootstrap %95 aralığının alt ucu > 0; ortalama hücre içi sıra > 0,50;
    {FO['slot']} yuvalı slot portföyü, {FO['port_n']} eşli rastgele portföyün %{100 * FO['port_yuzde']:.0f}'ından büyük. Q1 (kötü sürpriz) için AYNA (kaçınma): üst uç < 0, sıra < 0,50, portföy
    rastgele portföylerin %{100 * (1 - FO['port_yuzde']):.0f}'undan küçük. Hücreler: BIST {', BIST '.join(d[0] for d in FO['donem'])} (FI_OLCUT dönemleri) + bilgi: {', '.join(d[0] for d in C['donem_ek'])}.
C4. Aynı hissede {Pr['tekil_gun']} işlem günü içinde tekrarlanan olay tek olay (ilki), her ölçü x uç için ayrı.
C5. KARAR (CLAUDE.md 'Test ve bulgu standardı'): İZ için karar hücreleri ABD ve Avrupa'dır; K62 yalnız BIST'tir. Bu yüzden karar en fazla
    'BIST-BİLGİ: TUTAR' (BIST 2023 ve BIST 2024-26 hücrelerinin ikisi de tutarsa), aksi 'İZ DEĞİL'. İZ ya da ADAY denmez. Eşik oynatılmaz.

## D. PROTOKOL

D1. Tekilleştirme: makale örtüşen pencerelere izin verir (yıllık rapor ile 1. çeyrek arası ~45 işlem günü). A ve B'nin ana satırları makaledeki gibi
    tekilleştirmesizdir; aynı satırlar {Pr['tekil_gun']} işlem günü tekilleştirmesiyle de yazılır (bilgi). C'de tekilleştirme ana kuraldır.
D2. Her satırda birlikte: ortalama, medyan, eşli fark (CAR'ın kendisi eşleşen portföye göre farktır; C'de FI_OLCUT eşli farkı), %95 güven aralığı
    (mali çeyrek kümeli bootstrap, {Pr['bootstrap']} çekiliş, tohum {Pr['tohum']}), kümeli t ve p.
D3. Çoklu test: B ailesi = {len(A['olculen'])} ölçülen ölçü x {len(B['donem'])} dönem x 3 sınama (Q3 ortalaması ≠ 0, Q1 ortalaması ≠ 0, PEAD ≠ 0; ufuk 61) = {len(A['olculen']) * len(B['donem']) * 3} sınama
    (SUEAF verisi olsaydı 27). Benjamini-Hochberg %{100 * Pr['bh_q']:.0f}; Bonferroni bilgi (alfa {Pr['bonferroni_alfa']} / sınama sayısı). A birebir tekrar olduğundan aileye girmez.
D4. İşlem maliyeti: BIST tek yön {10000 * Pr['maliyet_tek_yon']:.0f} bp. Net korunma getirisi = PEAD - 4 x maliyet; net uzun bacak = CAR(Q3) - 2 x maliyet; açığa satış
    maliyeti / kısıtı ayrıca hesaplanmaz (kısa bacak BIST'te pratikte kısıtlı; bilgi).
D5. Geleceğe bakma: C'de her bilgi tarihi <= karar günü (t+1 kapanışı); açıklama saati kullanılmaz, giriş her durumda t+2 açılışıdır (saat bilinmese de
    güvenli). A ve B makaledeki gibi çeyrek içi tertil ve kırpma kullanır (çeyreğin sonradan açıklayanlarına bakar); bu yüzden A / B tekrar ölçüsüdür,
    alınabilirlik ölçüsü C'dir.
D6. Yaşayan yanlılığı: A ve B'de İş Yatırım verisi kotasyondan çıkan hisseleri içerir (KAP listesindeki kodlardan fiyatı bulunanlar); kodu değişen ya
    da İş Yatırım'da bulunmayan eski hisseler eksik kalabilir (kapsamda sayılır). C yalnız bugün işlem gören V_BIST hisseleridir (yanlılık var; beyan).
D7. Sayım modu (`kapsam`) hiçbir getiri / sürpriz değeri üretmez; testte denetlenir.

## E. K28 KARŞILAŞTIRMA TABLOSU (şablon; Faz 2'de doldurulur)

| özellik | K28 (Ç100; FON_IZI fi_k28_*) | Makale | K62 A / B | K62 C |
|---|---|---|---|---|
| olay günü | KAP ilk Finansal Rapor; 18:00 sonrası ertesi gün | Bloomberg açıklama günü | KAP ilk Finansal Rapor günü (saat ayrımı yok) | aynı; karar t+1 |
| sürpriz ölçüsü | tepki: kapanış(D-1) -> kapanış(D+1) - bütün hisselerin medyanı | SUETF, SUEAF, EAR (2x3 portföye göre, [t-1, t+1]) | SUETF, EAR (SUEAF veri yok) | SUETF, EAR |
| gruplama | takvim çeyreği içinde üst / alt %20 | çeyrek içi tertil | mali çeyrek içi tertil | önceki çeyreğin tertil kesimleri |
| giriş | tepki bitişinden sonraki işlem günü açılışı | t+2 (kapanıştan kapanışa) | t+2 (kapanış t+1'den) | t+2 açılışı |
| getiri | r60: açılıştan 60. gün kapanışına | CAR[2,61] al-tut farkı | CAR[2,61] al-tut farkı | r60 |
| kıyas | aynı gün momentum beşliği x likidite üçlüsü ortalaması | 2x3 büyüklük-DD/PD portföyü | 2x3 büyüklük-DD/PD portföyü | momentum x likidite hücresi |
| örneklem | V_BIST'te olan bütün hisseler (boyut şartı yok) | > 100 mn USD, özkaynak >= 0, Aralık mali yılı | makaledeki süzgeçler (SAPMA'larla) | aynı süzgeçler, V_BIST'te olanlar |
| dönem | 2022-07 -> 2026 (ek: 2016-22 örneklem dışı) | 2007-2018 | 2009Ç2-2018Ç4; 2017-21; 2022-26; 2023-26 | 2023; 2024-26; + bilgi dönemleri |
| yaşayan yanlılığı | var (yalnız yaşayanlar) | dipnot 5 kuralı | kotasyondan çıkanlar dahil (bulunabilenler) | var |
| tekilleştirme | yok (hisse-dönem başına ilk rapor) | yok | ana: yok; bilgi: {Pr['tekil_gun']} gün | {Pr['tekil_gun']} gün |
| olay sayısı | (k28_ozet.csv) | {Mk['n_tam']} / {Mk['n_analist']} | (Faz 2) | (Faz 2) |
| sonuç | üst %20 eşli fark BIST 2023 +%5,0, 2024-26 +%1,0; alt %20 -%5,1 / -%3,0 | PEAD %2,9 / %2,9 / %2,2 | (Faz 2) | (Faz 2) |

## F. MÜHÜR

Eşik / parametre sözlüğü K62_ESIK ve FON_IZI FI_OLCUT birlikte kararlı JSON'a (anahtar sıralı) çevrilir; sha256'sı dosyanın başındaki MÜHÜR satırıdır
(`K62.k62_esik_sha()`). `kos` bu değeri yeniden hesaplar; tutmazsa durur. VERİ satırı önbellek dosyalarının (KAP pencereleri, hisse fiyat dosyaları,
mali tablo dosyaları) sha256 özetidir; koşudaki veri farklıysa `kos` durur (`--veri-yeniden` ile ve raporda açıkça yazılarak sürdürülebilir).

## G. VERİ VE KAPSAM (sayım; getiri yok)

- KAP: {kp.get('finansal_rapor_kaydi', '—')} Finansal Rapor kaydı -> {kp.get('aciklama_hisse_ceyrek', '—')} hisse-çeyrek açıklaması (ilk {kp.get('ilk_yayin', '—')}, son {kp.get('son_yayin', '—')}).
- Fiyat (İş Yatırım): {fy.get('hisse', '—')} hisse, {fy.get('islem_gunu', '—')} işlem günü ({fy.get('ilk_gun', '—')} .. {fy.get('son_gun', '—')}); son 21 işlem gününde fiyatı olmayan
  (kotasyondan çıkmış sayılan) {fy.get('kotasyondan_cikan_hisse', '—')} hisse; V_BIST'te de olan {fy.get('v_bist_te_olan', '—')} / {fy.get('v_bist_hisse', '—')}.
- Mali tablo (İş Yatırım): {ml.get('hisse', '—')} hisse, {ml.get('satir', '—')} hisse-çeyrek satırı ({ml.get('ilk_yil', '—')}-{ml.get('son_yil', '—')}); grup dağılımı {ml.get('grup', '—')}.

| bölüm / dönem | açıklama | hisse | SUETF girdisi var | > 100 mn USD | EAR penceresi var | onsel (C) | TAM örneklem | tam: hisse | tam: çeyrek | tam: kotasyondan çıkan hisse olayı | onsel ve V_BIST'te |
|---|---|---|---|---|---|---|---|---|---|---|---|
{kapsam_tablo}

Makale tam örneklemi {Mk['n_tam']} gözlem / 48 çeyrek (çeyrek başına ~135); analist örneklemi {Mk['n_analist']}.

Veri fizibilitesi (11 Kasım 2026; gerçek istekle denendi; kişisel bilgi gönderilmedi):

| kaynak | sonuç | kapsam / alanlar | kısıt |
|---|---|---|---|
| Yahoo chart API (.IS) | çalışıyor (tarayıcı User-Agent ile) | 2005-01'den günlük; düzeltilmiş kapanış, temettü / bölünme; XU100.IS ve XU030.IS var | XUTUM.IS boş; denenen 15 kotasyondan çıkmış kodun 15'i 404 (ASYAB, KIPA, DENIZ, FINBN, BOYNR, ADANA, UNYEC, SODA, TRKCM, ANACM, ABANA, ALNTF, TEKST, BOLUC, BSHEV): yaşayan yanlılığı; K62'de kullanılmadı |
| İş Yatırım günlük hisse verisi | çalışıyor | 2000'lerden (KIPA 2000-01 .. 2018-08; ASYAB 2006-07 .. 2016-05); düzeltilmiş kapanış (temettü dahil; TUPRS Nisan 2018'de katsayı sıçraması Yahoo ile aynı), ham kapanış, piyasa değeri TL / USD, halka açık PD, hacim TL / USD, BIST-100, sermaye | açılış fiyatı yok (FI_OLCUT bu yüzden V_BIST'te); büyük yanıt kopuyor (4 yıllık parça + gzip) |
| V_BIST.pkl (islenmis-veri dalı) | var | 581 yaşayan hisse, OHLCV; 358'i 2015-06'dan | yalnız yaşayanlar; piyasa değeri yok. K28'in 2016-22 örneklem dışı koşusu fiyatı buradan aldı |
| KAP bildirim sorgusu (sınıf FR) | çalışıyor (403 yok; ara sıra 429) | 2009-06-01'den (öncesi 0 kayıt); yayın anı (saniye), mali yıl, dönem, kodlar; kotasyondan çıkanlar dahil | K28'in konu kodu süzgeci 2016 öncesi kayıt döndürmüyor (sınıf süzgeci kullanıldı); Haziran 2009 öncesi açıklama günü YOK |
| İş Yatırım mali tablo servisi | çalışıyor | 2008 / 3'ten (2007 boş); çeyreklik birikimli gelir tablosu ve bilanço; gruplar XI_29, UFRS, UFRS_K, XI_29K | yıllık değerlerde yeniden sunum sızıntısı (SAPMA 9); analist tahmini yok |
| Analist tahmini: Yahoo kazanç geçmişi | çalışıyor ama yetersiz | yalnız son 4 çeyrek; GARAN'da var, THYAO ve ALARK'ta boş | tarihsel değil |
| Analist tahmini: Investing takvimi, Fintables (site ve API) | 403 | — | bot engeli / üyelik |
| Analist tahmini: İş Yatırım, BigPara, Mynet beklenti sayfaları | 404 | — | sayfa yok |
| Analist tahmini: Ekofin konsensüs | yalnız güncel çeyrek | ~38 hisse | arşiv yok |
| Analist tahmini: Foreks / ForInvest, CNBC-E, Bloomberg HT anketleri | toplu veri yok | haber arşivinde çeyrek çeyrek tablolar (makale 2014'e kadar CNBC-E anketini kullandı) | elle derleme gerekir; tarihsel bütünlük doğrulanamaz |
| Analist tahmini: Rasyonet, Finnet, Matriks, Bloomberg, I/B/E/S (LSEG), FactSet | ücretli / kurumsal | tarihsel konsensüs var (makalenin kaynağı 2014'e kadar CNBC-E anketi, sonra Bloomberg anketi; muhasebe verisi Rasyonet) | fiyat yayımlanmıyor; bireysel erişim yok; denenmedi (K63 ile aynı sonuç) |
| Analist tahmini: EODHD, Alpha Vantage (EARNINGS_ESTIMATES) | ücretli (59,99 / 49,99 $ ay) | ABD'de donmuş çeyreklik konsensüs 2017-06'dan (K63) | BIST'te alanın dolu olduğu DOĞRULANAMADI; 2007-2018 makale dönemini zaten kapsamaz |

SUEAF için sonuç: VERİ YOK.

## H. BOŞLUK (makalede açık yazılmayan yerler; burada en dar / en mekanik yorum)

- BOŞLUK 1: 'kazanç' kalemi (bkz. SAPMA 8). BOŞLUK 2: 'önceki yıl' = mali çeyreğin yılından bir önceki takvim yılı sonu (piyasa değeri ve özkaynak).
- BOŞLUK 3: portföy kovaları eşit sayıda (medyan; üçte birler); hisse kendi portföyünün üyesidir; portföy t günü atamasıyla pencere boyunca sabit.
- BOŞLUK 4: günlük getiri = kapanış / önceki 5 işlem günü içindeki son kapanış - 1; o gün kapanışı yoksa getirisi yok sayılır ve hisse portföy
  getirisini alır; portföy getirisi de yoksa ikisi de 0.
- BOŞLUK 5: MV_q çeyrek sonuna eşit ya da önceki son işlem günü (en çok 10 takvim günü geride; 5 işlem günü ileri taşıma).
- BOŞLUK 6: tertil sınırı = kat(3 x sıra / n); çeyrekte en az {O['min_ceyrek_olay']} olay. Kırpma yalnız CAR ve regresyon değişkenlerine (tertil sırasını etkilemez).
- BOŞLUK 7: kümeli standart hata CR1 (G/(G-1) x (N-1)/(N-K)), p değeri t(G-1). Uç ortalamalarının t'si sabitli EKK'den.
- BOŞLUK 8: çok kodlu şirkette (pay grupları) fiyat verisi olan kodlardan toplam USD hacmi en büyük olan (bütün dönem hacmi; sınıf seçimi için
  küçük bir ileriye bakma içerir).
- BOŞLUK 9: CONCEARNINGS = aynı t gününe düşen bütün açıklamalar (örneklem dışı şirketler dahil; kendisi dahil). FRIDUM = t Cuma.
- BOŞLUK 10: regresyonda kontroller çeyrek içi kırpılıp bölüm örnekleminde standartlaştırılır; FRIDUM kırpılmaz; sabit etkiler kukla.
- BOŞLUK 11: C'de dönem = GİRİŞ günü (FI_OLCUT kuralı); B'de dönem = açıklama günü t.

## I. FAZ 2 KOMUTLARI

1. Ana oturum bu dosyayı ve K62.py / test_k62.py'yi denetler, git'e işler (ön kayıt commit'i ölçümden önce).
2. `python test_k62.py` (sentetik; geçmeli).  3. `python -I K62.py kos` (A + B + C + rapor; veri /tmp/k62_veri ve /tmp/veri/V_BIST.pkl).
4. `python K62.py rapor` (K62_RAPOR.md'yi çıktılardan yeniden yazar).
"""


def k62_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, E: Optional[Dict[str, Any]] = None, yol: Optional[str] = None,
                    kapsam: Optional[Dict[str, Any]] = None, veri_sha: Optional[Dict[str, Any]] = None, uzerine: bool = False) -> str:
    """K62_ON_KAYIT.md'yi yazar. Var olan dosyanın üzerine yazmaz (uzerine=True yalnız dosya git'e İŞLENMEMİŞSE kabul edilir)."""
    yol = yol or _k62_yol("onkayit", cikti)
    if os.path.exists(yol):
        if not uzerine:
            raise K62Hata(f"ön kayıt zaten var ({yol}); üzerine yazılmaz")
        try:
            _k62_git_islenmis(yol, "ön kayıt"); islenmis = True
        except K62Hata as ex:
            islenmis = "işlendikten sonra değişmiş" in str(ex)
        if islenmis:
            raise K62Hata(f"ön kayıt git'e işlenmiş ({yol}); üzerine yazılmaz")
    if kapsam is None and os.path.exists(_k62_yol("kapsam", cikti)):
        kapsam = _k62_json_oku(_k62_yol("kapsam", cikti))
    if veri_sha is None:
        veri_sha = (kapsam or {}).get("veri") or k62_veri_sha(veri)
    metin = k62_onkayit_metni(E, kapsam, veri_sha)
    if _K62_EPOSTA.search(metin):
        raise K62Hata("ön kayıt metninde e-posta biçimli parça var; yazılmadı")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k62log.info("ön kayıt yazıldı: %s (mühür %s)", yol, k62_esik_sha(E)[:12])
    return yol


def _k62_onkayit_oku(yol: str) -> Dict[str, Any]:
    with open(yol, encoding="utf-8") as f:
        metin = f.read()
    out: Dict[str, Any] = {}
    for ad, desen in _K62_OC_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise K62Hata(f"ön kayıt bozuk: '{ad}' satırı yok ({yol})")
        out[ad] = m.group(1)
    return out


def k62_onkayit_dogrula(yol: Optional[str] = None, E: Optional[Dict[str, Any]] = None, git: bool = True, cikti: Optional[str] = None) -> Dict[str, Any]:
    """Ön kayıt var, mührü bugünkü K62_ESIK + FI_OLCUT ile aynı ve (git=True) git'e işlenmiş, sonradan değişmemiş olmalı; biri tutmazsa K62Hata."""
    yol = yol or _k62_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise K62Hata(f"ön kayıt yok ({yol}): önce `python K62.py onkayit`")
    oc = _k62_onkayit_oku(yol)
    if oc["sha"] != k62_esik_sha(E):
        raise K62Hata(f"ön kayıt mührü tutmuyor ({oc['sha'][:12]} != {k62_esik_sha(E)[:12]}): eşikler ön kayıttan sonra değişmiş, koşu durdu")
    out = {"yol": yol, **oc, "dosya_sha256": _k62_sha(yol)}
    if git:
        out["git"] = _k62_git_islenmis(yol, "ön kayıt")
    return out


# ---------------------------------------------------------------- 7) KOŞU (A, B, C)
def _k62_satir(bolum: str, donem: str, olcu: str, ufuk: int, r: Dict[str, Any], E: Dict[str, Any], tekil: bool = False, ek: str = "") -> Dict[str, Any]:
    c = E["protokol"]["maliyet_tek_yon"]; mk = E["makale"]["pead"].get(olcu, {}).get(str(ufuk))
    out = {"bolum": bolum, "donem": donem, "olcu": olcu, "ufuk": int(ufuk), "tekil": bool(tekil), "notu": ek, **r,
           "pead_net": r["pead"] - 4 * c if np.isfinite(r["pead"]) else np.nan, "q3_net": r["ort_q3"] - 2 * c if np.isfinite(r["ort_q3"]) else np.nan,
           "makale": mk if bolum == "A" else np.nan}
    return out


def k62_olc_ab(Ev: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """A ve B bölümleri. Ev: k62_olay_tablosu(deger=True). TAM örneklemde makale tertili ve çeyrek içi kırpma bir kez; sonra bölüm / dönem maskeleri.
    Döner: (tablo, regresyon tablosu, tertil sütunları eklenmiş tam örneklem olay tablosu)."""
    E = E or K62_ESIK; O, A, B, Pr = E["olay"], E["bolum_a"], E["bolum_b"], E["protokol"]; X = Ev[Ev.tam.to_numpy()].reset_index(drop=True)
    q = X.mali_ceyrek.to_numpy(); kod = X.kod.to_numpy(); sinif = {o: k62_tertil(X[o].to_numpy(float), q, kod, E) for o in A["olculen"]}
    car = {n: k62_winsor(X[f"CAR{n}"].to_numpy(float), q, O["winsor"]) for n in O["car"]["ufuk"]}
    temiz = ~_k62_haric_maske(X, B["tms29_haric"]); bolumler: List[Tuple[str, str, str, np.ndarray, str, str]] = []
    for o in A["olculen"]:
        bolumler.append(("A", "%dÇ%d-%dÇ%d" % (A["mali_bas"][0], A["mali_bas"][1], A["mali_bit"][0], A["mali_bit"][1]), o, _k62_a_maske(X, E), "", ""))
    for ad, a, b in B["donem"]:
        for o in A["olculen"]:
            if o == "SUETF" and pd.Timestamp(a).year >= B["tms29_bas_yil"]:      # B3: SUETF'te ana satır TMS 29 temiz çeyrekler; bütün çeyrekler bilgi
                bolumler.append(("B", ad, o, _k62_t_maske(X, a, b) & temiz, "", "TMS29 temiz çeyrekler"))
                bolumler.append(("B", ad, o, _k62_t_maske(X, a, b), "TMS29 kirli çeyrekler dahil (bilgi)", "bütün çeyrekler"))
            else:
                bolumler.append(("B", ad, o, _k62_t_maske(X, a, b), "", ""))
    sat, reg = [], []
    for bolum, donem, o, m, ek, kapsam in bolumler:
        for n in O["car"]["ufuk"]:
            sat.append({**_k62_satir(bolum, donem, o, n, k62_pead(car[n][m], sinif[o][m], q[m], E), E, False, ek), "kapsam": kapsam})
            if not ek:
                tk = np.zeros(len(X), bool); tk[k62_tekil(X[m], Pr["tekil_gun"]).index.to_numpy()] = True
                sat.append({**_k62_satir(bolum, donem, o, n, k62_pead(car[n][tk], sinif[o][tk], q[tk], E), E, True, f"{Pr['tekil_gun']} işlem günü tekilleştirme (bilgi)"), "kapsam": kapsam})
        if not ek:
            try:
                r = k62_regresyon(X[m].reset_index(drop=True), sinif[o][m], f"CAR{O['car']['ana']}", E)
            except (np.linalg.LinAlgError, ValueError, KeyError) as ex:
                k62log.warning("regresyon %s %s %s: %s", bolum, donem, o, ex); r = {"n": 0, "a1": np.nan, "t": np.nan, "p": np.nan, "G": 0}
            reg.append({"bolum": bolum, "donem": donem, "olcu": o, "kapsam": kapsam, "ufuk": O["car"]["ana"], "n": r["n"], "kume": r["G"], "a1": r["a1"], "t": r["t"], "p": r["p"],
                        "makale": E["makale"]["regresyon_61"].get(o) if bolum == "A" else np.nan,
                        "katsayi": json.dumps(r.get("katsayi", {}), ensure_ascii=False), "t_hepsi": json.dumps(r.get("t_hepsi", {}), ensure_ascii=False)})
    T = pd.DataFrame(sat); T["fark_puan"] = T.pead - T.makale
    T["basari"] = [("YENİDEN ÜRETİLDİ" if (np.sign(r.pead) == np.sign(r.makale) and abs(r.fark_puan) <= A["basari_puan"]) else
                    ("YÖN AYNI, BÜYÜKLÜK FARKLI" if np.sign(r.pead) == np.sign(r.makale) else "YENİDEN ÜRETİLEMEDİ"))
                   if (r.bolum == "A" and not r.tekil and r.ufuk == O["car"]["ana"] and np.isfinite(r.pead)) else "" for r in T.itertuples()]
    # D3: B ailesi (tekilleştirmesiz, bilgi satırı olmayan, ana ufuk): ölçü x dönem x (Q3, Q1, PEAD)
    aile = ((T.bolum == "B") & ~T.tekil & (T.notu == "") & (T.ufuk == O["car"]["ana"])).to_numpy(); ix = np.flatnonzero(aile)
    p = np.concatenate([T.p_q3.to_numpy(float)[ix], T.p_q1.to_numpy(float)[ix], T.p.to_numpy(float)[ix]]); m_ = len(p)
    bh = k62_bh(p, Pr["bh_q"]); bon = p <= (Pr["bonferroni_alfa"] / m_ if m_ else 0.0)
    for j, ad in enumerate(("q3", "q1", "pead")):
        T[f"bh_{ad}"] = False; T[f"bonf_{ad}"] = False
        T.loc[T.index[ix], f"bh_{ad}"] = bh[j * len(ix):(j + 1) * len(ix)]; T.loc[T.index[ix], f"bonf_{ad}"] = bon[j * len(ix):(j + 1) * len(ix)]
    T["aile_sinama"] = m_
    T["okuma"] = [("TUTAR" if (r.pead > 0 and r.p < 0.05 and r.bh_pead) else "TUTMAZ") if (r.bolum == "B" and not r.tekil and r.notu == "" and r.ufuk == O["car"]["ana"]
                                                                                           and np.isfinite(r.pead)) else "" for r in T.itertuples()]
    Xs = X.copy()
    for o in A["olculen"]:
        Xs[o + "_tertil"] = sinif[o]
    return T, pd.DataFrame(reg), Xs


def k62_olc_c(Ev: pd.DataFrame, V: Dict[str, pd.DataFrame], E: Optional[Dict[str, Any]] = None, P: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """C bölümü (proje cetveli): onsel olaylar, geleceğe bakmayan tertil, giriş t+2 açılışı, tekilleştirme; FON_IZI fi_olcut_* ile hücreler ve karar."""
    import FON_IZI as FI
    E = E or K62_ESIK; C, Pr, A = E["bolum_c"], E["protokol"], E["bolum_a"]; O = FI.FI_OLCUT; P = P or FI.fi_olcut_panel(V, O)
    X = Ev[Ev.onsel.to_numpy()].reset_index(drop=True); sat = []; karar: Dict[str, str] = {}
    donemler = [(d[0], d[1], d[2], "karar") for d in O["donem"]] + [(d[0], d[1], d[2], "bilgi") for d in C["donem_ek"]]
    for o in A["olculen"]:
        s = k62_tertil_onsel(X, o, E, E["bolum_b"]["tms29_haric"] if o == "SUETF" else None)      # SUETF: TMS 29 kirli çeyrekleri sınıfsız
        for uc, deger in (("Q3", 2), ("Q1", 0)):
            G = X[(s == deger) & X.kod.isin(set(V)).to_numpy() & X.giris.notna().to_numpy()]; G = k62_tekil(G, Pr["tekil_gun"])
            Tt = FI.fi_olcut_olay(P, pd.DataFrame({"sembol": G.kod.to_numpy(), "giris": pd.to_datetime(G.giris).to_numpy()})); tut = {}
            for ad, a, b, tur in donemler:
                h = FI.fi_olcut_hucre(Tt[(Tt.giris >= pd.Timestamp(a)) & (Tt.giris <= pd.Timestamp(b))], O)
                if h.get("n", 0) >= 1:
                    t_ = bool(h["n"] >= O["n_esik"] and ((h["alt95"] > 0 and h["sira"] > 0.5 and h["portfoy"] > h["portfoy_esli_p90"]) if uc == "Q3" else
                                                         (h["ust95"] < 0 and h["sira"] < 0.5 and h["portfoy"] < h["portfoy_esli_p10"])))
                else:
                    t_ = False
                if tur == "karar":
                    tut[ad] = t_
                sat.append({"olcu": o, "uc": uc, "pazar": "BIST", "donem": ad, "tur": tur, "olay_tekil": int(len(G)), **h, "tutar": t_})
            karar[f"{o} {uc}"] = ("BIST-BİLGİ: TUTAR" + (" (kaçınma)" if uc == "Q1" else "")) if (tut and all(tut.values())) else "İZ DEĞİL"
    return pd.DataFrame(sat), karar


def k62_kos(cikti: Optional[str] = None, veri: Optional[str] = None, demet: Optional[Dict[str, Any]] = None, V: Optional[Dict[str, pd.DataFrame]] = None,
            E: Optional[Dict[str, Any]] = None, onkayit_yol: Optional[str] = None, git_sart: bool = True, veri_yeniden: bool = False) -> Dict[str, Any]:
    """Tek koşu: ön kayıt (mühür + git) -> [gerçek veride veri sha256] -> olay tablosu (değerlerle) -> A, B, regresyon, C -> çıktılar + rapor.
    demet / V / E yalnız testler içindir (sentetik demet: veri sha256 doğrulaması atlanır; ön kayıt doğrulaması yine şarttır)."""
    Ek = E or K62_ESIK; sentetik = demet is not None; t0 = time.time()
    oc = k62_onkayit_dogrula(onkayit_yol, Ek, git_sart, cikti)
    meta: Dict[str, Any] = {"surum": K62_SURUM, "onkayit": oc, "sentetik": sentetik, "kos_baslangic": _k62_simdi(), "isolated": bool(sys.flags.isolated),
                            "kod_sha256": _k62_sha(os.path.join(KOK_K62, "K62.py")) if os.path.exists(os.path.join(KOK_K62, "K62.py")) else None,
                            "surumler": {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}, "not": []}
    if not sentetik:
        vs = k62_veri_sha(veri); meta["veri"] = vs
        if vs["sha256"] != oc["veri_sha256"] or (vs["v_bist_sha256"] or "yok") != oc["v_bist_sha256"]:
            if not veri_yeniden:
                raise K62Hata(f"veri ön kayıttakiyle aynı değil (önbellek {vs['sha256'][:12]} / ön kayıt {oc['veri_sha256'][:12]}; V_BIST {str(vs['v_bist_sha256'])[:12]} / "
                              f"{oc['v_bist_sha256'][:12]}): koşu durdu (`--veri-yeniden` ile, raporda yazılarak sürdürülebilir)")
            meta["not"].append(f"VERİ ÖN KAYITTAKİNDEN FARKLI (--veri-yeniden): önbellek {vs['sha256'][:12]} (ön kayıt {oc['veri_sha256'][:12]}); V_BIST "
                               f"{str(vs['v_bist_sha256'])[:12]} (ön kayıt {oc['v_bist_sha256'][:12]})")
        D = k62_demet_kur(veri, Ek); V = _k62_vbist_yukle()
    else:
        D = demet
    Ev = k62_olay_tablosu(D, Ek, deger=True)
    if not len(Ev) or not Ev.tam.any():
        raise K62Hata("tam örneklemde olay yok: ölçülecek bir şey yok")
    T, Rg, Xs = k62_olc_ab(Ev, Ek)
    if V:
        Cz, karar = k62_olc_c(Ev, V, Ek)
    else:
        Cz, karar = pd.DataFrame(), {}; meta["not"].append("V (OHLCV paneli) verilmedi: C bölümü ölçülmedi")
    meta.update({"olay": {"hepsi": int(len(Ev)), "onsel": int(Ev.onsel.sum()), "tam": int(Ev.tam.sum())}, "karar_c": karar})
    cik = cikti or K62_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    T.to_csv(_k62_yol("tablo", cikti), index=False); Rg.to_csv(_k62_yol("regresyon", cikti), index=False); Cz.to_csv(_k62_yol("olcut", cikti), index=False)
    Xs.to_csv(_k62_yol("olay", cikti), index=False)
    meta["kos_bitis"] = _k62_simdi(); meta["sure_sn"] = round(time.time() - t0)
    _k62_json_yaz(_k62_yol("meta", cikti), meta)
    return {"tablo": T, "regresyon": Rg, "olcut": Cz, "olay": Xs, "meta": meta, "rapor": k62_rapor(cikti, Ek)}


# ---------------------------------------------------------------- 8) RAPOR
def _k62_s(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return f"{v:.{n}f}".replace(".", ",") if np.isfinite(v) else "—"


def _k62_y(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return ("%" + f"{100 * v:.{n}f}".replace(".", ",")) if np.isfinite(v) else "—"


def k62_rapor(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """K62_RAPOR.md'yi k62_tablo.csv, k62_regresyon.csv, k62_olcut.csv ve k62_meta.json'dan yazar."""
    E = E or K62_ESIK; yt, ym = _k62_yol("tablo", cikti), _k62_yol("meta", cikti)
    if not (os.path.exists(yt) and os.path.exists(ym)):
        raise K62Hata(f"K62 çıktıları yok ({yt}): önce `python -I K62.py kos`")
    T = pd.read_csv(yt, keep_default_na=True); m = _k62_json_oku(ym); ana = E["olay"]["car"]["ana"]
    for k in ("notu", "basari", "okuma", "kapsam"):
        T[k] = T[k].fillna("").astype(str)
    Rg = pd.read_csv(_k62_yol("regresyon", cikti)) if os.path.exists(_k62_yol("regresyon", cikti)) else pd.DataFrame()
    try:
        Cz = pd.read_csv(_k62_yol("olcut", cikti))
    except (OSError, pd.errors.EmptyDataError):
        Cz = pd.DataFrame()
    bas = ("| bölüm | dönem | ölçü | ufuk | n Q1 / Q3 | çeyrek | ort. CAR Q1 | ort. CAR Q3 | medyan Q1 / Q3 | PEAD [%95] | t (p) | net (4 x 30 bp) | makale | fark (puan) | sonuç | not |\n"
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")

    def sat(X: pd.DataFrame) -> str:
        return bas + "\n".join(
            f"| {r.bolum} | {r.donem} | {r.olcu} | [2,{r.ufuk}] | {int(r.n_q1)} / {int(r.n_q3)} | {int(r.kume)} | {_k62_y(r.ort_q1)} | {_k62_y(r.ort_q3)} | {_k62_y(r.med_q1)} / {_k62_y(r.med_q3)} | "
            f"{_k62_y(r.pead)} [{_k62_y(r.alt)}; {_k62_y(r.ust)}] | {_k62_s(r.t)} ({_k62_s(r.p, 3)}) | {_k62_y(r.pead_net)} | {_k62_y(r.makale)} | {_k62_s(100 * r.fark_puan) if pd.notna(r.fark_puan) else '—'} | "
            f"{r.basari or r.okuma} | {'; '.join(x for x in (r.kapsam, 'tekil' if r.tekil else '', r.notu) if x)} |" for r in X.itertuples())
    Aa = T[(T.bolum == "A")]; Bb = T[(T.bolum == "B")]; par = [
        f"# K62 — BIST PEAD birebir tekrar: RAPOR\n\n{K62_SURUM}. Ön kayıt K62_ON_KAYIT.md (mühür {m['onkayit']['sha'][:12]}, git {str(m['onkayit'].get('git', {}).get('commit', ''))[:7]}); "
        f"koşu {m['kos_baslangic']} → {m['kos_bitis']} ({m.get('sure_sn')} sn). Olay: {m['olay']['hepsi']} açıklama, onsel {m['olay']['onsel']}, tam örneklem {m['olay']['tam']}.\n",
        "## A. Birebir tekrar (makale: PEAD[2,61] SUETF %2,94, SUEAF %2,90, EAR %2,18)\n" + sat(Aa[~Aa.tekil]) + "\n\nSUEAF: VERİ YOK (ücretsiz tarihsel analist tahmini yok); yeniden üretilemedi.\n",
        "### A, 60 işlem günü tekilleştirmeyle (bilgi)\n" + sat(Aa[Aa.tekil & (Aa.ufuk == ana)]) + "\n",
        "## B. Dönemler (makale yöntemi; dönem = açıklama günü)\n" + sat(Bb[~Bb.tekil & (Bb.ufuk == ana)]) + "\n",
        "### B, kısa ufuklar ve tekilleştirme (bilgi)\n" + sat(Bb[(Bb.ufuk != ana) & ~Bb.tekil]) + "\n\n" + sat(Bb[Bb.tekil & (Bb.ufuk == ana)]) + "\n"]
    f61 = Bb[~Bb.tekil & (Bb.ufuk == ana) & (Bb.notu == "")]
    if len(f61):
        par.append(f"### B çoklu test (aile {int(f61.aile_sinama.iloc[0])} sınama; BH %{100 * E['protokol']['bh_q']:.0f}, Bonferroni bilgi)\n| dönem | ölçü | Q3 ort. (p; BH; Bonf.) | Q1 ort. (p; BH; Bonf.) | PEAD (p; BH; Bonf.) |\n|---|---|---|---|---|\n"
                   + "\n".join(f"| {r.donem} | {r.olcu} | {_k62_y(r.ort_q3)} ({_k62_s(r.p_q3, 3)}; {'ret' if r.bh_q3 else '—'}; {'ret' if r.bonf_q3 else '—'}) | {_k62_y(r.ort_q1)} ({_k62_s(r.p_q1, 3)}; "
                               f"{'ret' if r.bh_q1 else '—'}; {'ret' if r.bonf_q1 else '—'}) | {_k62_y(r.pead)} ({_k62_s(r.p, 3)}; {'ret' if r.bh_pead else '—'}; {'ret' if r.bonf_pead else '—'}) |" for r in f61.itertuples()) + "\n")
    if len(Rg):
        par.append("## Kontrollü regresyon (PUAN katsayısı; CAR[2,61]; IO yok)\n| bölüm | dönem | ölçü | n | küme | a1 | t (p) | makale |\n|---|---|---|---|---|---|---|---|\n"
                   + "\n".join(f"| {r.bolum} | {r.donem} | {r.olcu} | {int(r.n)} | {int(r.kume)} | {_k62_y(r.a1)} | {_k62_s(r.t)} ({_k62_s(r.p, 3)}) | {_k62_y(r.makale)} |" for r in Rg.itertuples()) + "\n")
    if len(Cz):
        par.append("## C. Proje cetveli (FI_OLCUT; giriş t+2 açılışı; geleceğe bakmayan tertil; yalnız V_BIST hisseleri)\n"
                   "| ölçü | uç | dönem | tür | n | ort. eşli fark [%95] | medyan fark | ort. r60 / eşli | sıra | portföy / rastgele p10-p90 | tutar |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
                   + "\n".join(f"| {r.olcu} | {r.uc} | {r.donem} | {r.tur} | {int(r.n)} | {_k62_y(getattr(r, 'ort_fark', np.nan))} [{_k62_y(getattr(r, 'alt95', np.nan))}; {_k62_y(getattr(r, 'ust95', np.nan))}] | "
                               f"{_k62_y(getattr(r, 'medyan_fark', np.nan))} | {_k62_y(getattr(r, 'ort_r60', np.nan))} / {_k62_y(getattr(r, 'ort_esli', np.nan))} | {_k62_s(getattr(r, 'sira', np.nan), 3)} | "
                               f"{_k62_y(getattr(r, 'portfoy', np.nan), 0)} / {_k62_y(getattr(r, 'portfoy_esli_p10', np.nan), 0)}-{_k62_y(getattr(r, 'portfoy_esli_p90', np.nan), 0)} | {'EVET' if r.tutar else 'hayır'} |"
                               for r in Cz.itertuples()) + "\n\nKarar: " + "; ".join(f"{k}: {v}" for k, v in m.get("karar_c", {}).items())
                   + ". (İZ / ADAY denmez: karar hücreleri ABD ve Avrupa; K62 yalnız BIST.)\n")
    k28 = os.path.join(KOK_K62, "arastirma_cikti", "fon_izi", "k28_ozet.csv")
    if os.path.exists(k28):
        try:
            K = pd.read_csv(k28); K = K[(K.pazar == "BIST") & K.olay.isin(["ust", "alt"])]
            par.append("## K28 ile karşılaştırma (K28: tepki üst / alt %20, eşli fark r60; ön kayıt E tablosu)\n| K28 olay | dönem | n | ort. eşli fark [%95] | sıra |\n|---|---|---|---|---|\n"
                       + "\n".join(f"| {r.olay} | {r.donem} | {int(r.n)} | {_k62_y(r.ort_fark)} [{_k62_y(r.alt95)}; {_k62_y(r.ust95)}] | {_k62_s(r.sira, 3)} |" for r in K.itertuples())
                       + "\n\nK62 C satırlarıyla aynı cetvel (FI_OLCUT); fark: K62'de boyut süzgeci (> 100 mn USD), tertil (üçte bir), EAR 2x3 portföye göre ve [t-1, t+1], giriş t+2.\n")
        except (OSError, ValueError, AttributeError) as ex:
            k62log.warning("K28 özeti okunamadı: %s", ex)
    if m.get("not"):
        par.append("## Koşu notları\n" + "\n".join(f"- {x}" for x in m["not"]) + "\n")
    par.append("## Sınırlar\nSAPMA ve BOŞLUK listesi ön kayıttadır (K62_ON_KAYIT.md A ve H). A / B makaledeki gibi çeyrek içi tertil kullanır (ileriye bakar); alınabilirlik ölçüsü C'dir. "
               "Kısa bacak BIST'te pratikte kısıtlıdır; net sütunu yalnız alım-satım komisyonunu düşer.\n")
    metin = "\n".join(par); yol = _k62_yol("rapor", cikti)
    if _K62_EPOSTA.search(metin):
        raise K62Hata("rapor metninde e-posta biçimli parça var; yazılmadı")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k62log.info("rapor: %s", yol)
    return yol


def _cakisma_kontrol_k62(_once=_CK_ONCE_K62, _dosya="K62.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K62", "_CK_KAYIT", "_cakisma_kontrol_k62", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "gzip", "ssl", "hashlib", "subprocess", "threading", "urllib", "_dt",
           "annotations", "Any", "Callable", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k62()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=K62_SURUM)
    ap.add_argument("komut", choices=["indir", "kapsam", "onkayit", "kos", "rapor"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--veri-yeniden", action="store_true", help="kos: veri ön kayıttakinden farklıysa durma; farkı rapora yaz")
    ap.add_argument("--uzerine-yaz", action="store_true", help="onkayit: git'e İŞLENMEMİŞ ön kaydı yeniden yaz")
    a = ap.parse_args()
    try:
        if a.komut == "indir":
            print(json.dumps(k62_indir(a.veri), ensure_ascii=False, default=str))
        elif a.komut == "kapsam":
            K_ = k62_kapsam(a.veri, a.cikti)
            print(json.dumps({k: K_[k] for k in ("muhur", "veri", "kap", "fiyat", "mali", "olay")}, ensure_ascii=False, default=str, indent=1))
        elif a.komut == "onkayit":
            print(k62_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            R_ = k62_kos(a.cikti, a.veri, veri_yeniden=a.veri_yeniden)
            print("K62 bitti:", json.dumps({"olay": R_["meta"]["olay"], "karar_c": R_["meta"]["karar_c"], "sure_sn": R_["meta"]["sure_sn"]}, ensure_ascii=False, default=str))
            print(R_["rapor"])
        else:
            print(k62_rapor(a.cikti))
    except (K62Hata, FileNotFoundError) as ex:
        k62log.error("%s", ex); sys.exit(1)
