"""KOR_TEST — VDYT2 G5 sessiz bölge dedektörü için İNSAN GÖZÜ KÖR TESTİ + Tiingo batan OHLC doğrulaması (12 Kasım 2026). Tek dosya.

Cemal (12 Kasım 2026, aynen): 'Tiingo'nun borsadan silinmiş şirketler için geçmiş OHLC verisi sağlayabildiği örneklerle doğrulanmalı. İlk örneklerde algoritmanın
insan gözünün gördüğü sıkışma bölgelerini yakaladığına dair ölçülebilir işaret bulunmalı. Veri dalını kalıcılaştırmak için acele etmeyelim; önce sinyalin
varlığını doğrulayalım; sonra Aralık kotasını yalnızca bu test için kullanalım.'

İŞ 1 (`ohlc`): Tiingo pilot önbelleğindeki 12 seri (/tmp/vdyt2b/tiingo; YENİ İSTEK YOK) için OHLC doluluğu, iç tutarlılık, düzeltme katsayısı, donuk bar,
kotasyondan çıkış öncesi aralık gerçekçiliği, OTC sıçramaları, kod yeniden kullanımı ve elde bağımsız kaynak olan sembollerde (SUNE: k60 / k34 Yahoo; SIVB:
basın kapanışı; CHK: k60 EXE) OHLC karşılaştırması. Örnek grafikler /tmp/vdyt2b/ohlc_ornek/ (Tiingo lisansı: repoya girmez). Rapor yalnız sayı.
İŞ 2 (`set` -> `onkayit` -> Cemal işaretler -> `olc`): 40 grafiklik kör set (16 G5 tespit günü + 16 bölge dışı kontrol + 8 batan), seçim kuralı ve tohum
KOR_ESIK'te (ön kayıt mührü), grafikte karar gününden sonra bar YOK, hiçbir etiket / işaret / sembol / tarih YOK. Cevap anahtarı /tmp/kor_test_vdyt2/anahtar.json
(sha256 ön kayıtta; repoya ancak `olc`ta, Cemal işaretledikten SONRA kopyalanır).

SINIR: VDYT.py, VDYT2.py, VDYT2B.py ve onların ön kayıt / sonuçları DEĞİŞMEZ (yalnız içe aktarılır; VDYT2 / VDYT kod sha256'ları VDYT2 ön kaydıyla aynı
olmalı, değilse durur). Tiingo'ya, SEC'e istek YOK; ağ yok; e-posta / anahtar yok. Tiingo fiyatı ve kör set grafikleri repoya girmez.

Komut:  python KOR_TEST.py ohlc                 İŞ 1 raporu (VDYT2B_OHLC_DOGRULAMA.md + json) ve örnek grafikler
        python KOR_TEST.py set                  kör set: seçim + 40 grafik + anahtar + manifest + cevap şablonu (ön kayıt varsa üzerine yazmaz)
        python KOR_TEST.py onkayit              KOR_TEST_ON_KAYIT.md (eşik mührü, kod / tablo / aday / anahtar / manifest sha256; varsa üzerine yazmaz)
        python KOR_TEST.py olc --cevap DOSYA    Cemal'in cevapları -> ölçüm (ön kayıt + KOR_TEST.py git'e işlenmemişse, mühür / anahtar sha256 tutmazsa REDDEDER)
        python KOR_TEST.py rapor                KOR_TEST_RAPOR.md'yi sonuç JSON'undan yeniden yazar
Colab:  exec(open('KOR_TEST.py').read()) (VDYT.py, VDYT2.py, VDYT2B.py aynı klasörde)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_KOR = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_KOR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_KOR not in sys.path:
    sys.path.insert(0, KOK_KOR)
import VDYT as V1  # noqa: E402  (DEĞİŞTİRİLMEZ)
import VDYT2 as V2  # noqa: E402  (G5 dedektörü; DEĞİŞTİRİLMEZ)
import VDYT2B as V2B  # noqa: E402  (Tiingo önbellek okuyucusu ve pilot tanımları; DEĞİŞTİRİLMEZ)

korlog = logging.getLogger("col.kor")
if not korlog.handlers:
    _kor_h = logging.StreamHandler(sys.stderr)
    _kor_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s kor: %(message)s", "%H:%M:%S"))
    korlog.addHandler(_kor_h)
    korlog.setLevel(logging.INFO)
    korlog.propagate = False

KOR_ETIKET = "kor_vdyt2_20261112"
KOR_SURUM = "KOR_TEST v1.0 (kor_vdyt2_20261112): İş 1 Tiingo OHLC doğrulaması + İş 2 insan gözü kör testi (ön kayıt; ölçüm Cemal'in işaretlerinden sonra)"

KOR_YOL: Dict[str, str] = {
    "cikti": os.environ.get("KOR_CIKTI", os.path.join(KOK_KOR, "arastirma_cikti", "vdyt", "v2_20261112")),
    "set": os.environ.get("KOR_SET", "/tmp/kor_test_vdyt2"),
    "tiingo": os.environ.get("KOR_TIINGO", "/tmp/vdyt2b/tiingo"),
    "ohlc_png": os.environ.get("KOR_OHLC_PNG", "/tmp/vdyt2b/ohlc_ornek"),
    "vdyt2_tablo": os.environ.get("KOR_VDYT2_TABLO", "/tmp/vdyt2/kasa"),
    "vdyt2_tablo_wf": os.environ.get("KOR_VDYT2_TABLO_WF", "/tmp/vdyt2/wf"),
    "k34": "/tmp/veri2/k34_yahoo.pkl",
}
KOR_DOSYA: Dict[str, str] = {
    "onkayit": "KOR_TEST_ON_KAYIT.md", "sonuc": "kor_test_sonuc.json", "rapor": "KOR_TEST_RAPOR.md", "anahtar_repo": "kor_test_anahtar.json",
    "ohlc_md": "VDYT2B_OHLC_DOGRULAMA.md", "ohlc_json": "vdyt2b_ohlc_dogrulama.json",
    "anahtar": "anahtar.json", "manifest": "manifest.json", "aday": "aday_listesi.json", "sablon": "cevap_sablon.json", "grafik": "grafik",
}
_KOR_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256 mührü ön kayıtta; sonuç görüldükten sonra değişmez)
KOR_ESIK: Dict[str, Any] = {
    "surum_etiket": KOR_ETIKET,
    "vdyt2": {"kod_sha256": "e33b2fd1c611e32930e8e8af29b9a4a9e86607a1df303e0fae8d9e94d0a30741",    # VDYT2 ön kaydındaki KOD_SHA256 (dedektör değişmedi)
              "vdyt_kod_sha256": "10ead8062c2c8ec25984a23b68b299cec4d8a7cfd144ad22e542e867d40c932d", "tanim": "G5"},
    "tohum": 20261118,
    "set": {
        "G5": {"BIST": 8, "ABD": 8}, "KONTROL": {"BIST": 8, "ABD": 8}, "BATAN_G5": 4, "BATAN_KONTROL": 4,
        "yas": [10, 30],                     # G5 karar yaşı aralığı (VDYT2 karar yaşları 10, 15, 20, 30); bölge son 10-30 mumda
        "g5_kaynak": "GERCEK", "kontrol_kaynak": "DISARI",   # VDYT2 satir_<pazar>_G5 (P1 olsun olmasın) / kontrol_<pazar>_G5 DIŞARI satırları
        "sag_bosluk": 30,                    # KONTROL / BATAN_KONTROL: [t-29, t] hiçbir G5 bölgesinin [bas, bit] aralığıyla kesişmez (sağ uçta bölge yok)
        "farkli_hisse": True,                # her grupta farklı hisse; KONTROL'de G5 grubunun hisseleri ilk geçişte dışarıda (tercih)
        "pencere_kopuk_yok": True,           # 120 barlık pencerede > 15 takvim günü boşluk (V1.vdyt_kopuk) olmaz
        "batan": {"semboller": ["BBBYQ", "WEWKQ", "SHLDQ", "HTZGQ", "REVRQ", "DNR", "GNC"],   # vdyt2b_pilot.json GEÇTİ = True olanlar (çalışırken denetlenir)
                  "karar_once_f25": True,    # karar günü < Form 25-NSE günü (borsa dönemi)
                  "uygunluk": "ABD VDYT kuralı yeniden: bar no >= 252, ekrandaki (ham) kapanış >= 2 $, 20 gün medyan işlem değeri (min 10 gün) >= 1 mn $; "
                              "t >= 260; panel (kesit) kurulmaz",
                  "kontrol_yas": 10,         # BATAN_KONTROL geçerlilik (V2.v2_gecerli) sözde yaşı
                  "tekrar_izni": True},      # 7 seri: farklı hisse yetmezse aynı hisseden >= 120 bar uzak ikinci gün (önce farklı hisse)
    },
    "grafik": {"bar": 120, "piksel": [1200, 800], "dpi": 110, "hedef_kb": 150, "normal": "fiyat / karar günü kapanışı x 100",
               "x_tik": [-120, -100, -80, -60, -40, -20, 0], "hacim_pay": 0.25, "yukari": "#26a69a", "asagi": "#ef5350", "govde_en": 0.7,
               "font": 12, "metin": "yalnız eksen sayıları (x: gün sırası, y: normalize fiyat); hacim ekseni sayısız; başlık / etiket / çizgi / ızgara YOK"},
    "soru": {
        "bolge": "Grafiğin sağ ucunda (son 10-30 mumda) küçük mumlu, dar bantlı sessiz bir bölge görüyor musun?",
        "bolge_cevap": ["EVET", "HAYIR", "EMİN DEĞİLİM"],
        "destek": "Bölgenin altında savunulan bir destek (tekrar tekrar test edilen dip) görüyor musun? (isteğe bağlı)",
        "destek_cevap": ["EVET", "HAYIR"],
    },
    "olcum": {
        "ana_gruplar": ["G5", "KONTROL"], "bilgi_gruplar": ["BATAN_G5", "BATAN_KONTROL"],
        "emin": "EMİN DEĞİLİM oranlarda paydadan çıkar (ANA); sağlama: HAYIR'a eklenmiş hali (BİLGİ)",
        "basari": {"g5_evet_min": 0.70, "kontrol_evet_max": 0.35, "kappa_min": 0.40, "fisher_p_max": 0.05, "fisher": "iki_yonlu"},
        "zayif": {"g5_evet_min": 0.60, "fark_min": 0.0},
        "min_payda": 8,                       # bir ANA grupta EVET + HAYIR < 8 -> 'VERİ YETERSİZ' (İŞARET YOK sayılır)
        "guven": 0.95, "z": 1.959963984540054, "bootstrap": {"B": 2000, "tohum": 20261119, "kume": "hisse"},
        "fark_araligi": "Newcombe hibrit Wilson (yöntem 10) ANA; hisse kümeli bootstrap BİLGİ",
        "destek": "insan destek EVET / HAYIR ile G4 (gövde tabanı) durumu: uyum ve kappa (BİLGİ)",
    },
    "karar_kullanimi": "BAŞARILI ya da ZAYIF İŞARET -> Aralık Tiingo kotası YALNIZ VDYT2-B testi B için kullanılır; İŞARET YOK (VERİ YETERSİZ dahil) -> B'ye "
                       "kota harcanmaz, dedektör önce düzeltilir (yeni ön kayıtla).",
}
KOR_GRUPLAR = ["G5", "KONTROL", "BATAN_G5", "BATAN_KONTROL"]


class KorHata(RuntimeError):
    """KOR_TEST'e özgü durdurucu hata (ön kayıt yok / işlenmemiş / mühür ya da anahtar sha256 tutmuyor, veri eksik, cevap dosyası geçersiz)."""


# ---------------------------------------------------------------- 0) YARDIMCILAR
def _kor_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _kor_yol(ad: str, kl: Optional[str] = None) -> str:
    return os.path.join(kl or KOR_YOL["cikti"], KOR_DOSYA.get(ad, ad))


def _kor_set_yol(ad: str, kl: Optional[str] = None) -> str:
    return os.path.join(kl or KOR_YOL["set"], KOR_DOSYA.get(ad, ad))


def _kor_yaz(yol: str, metin: str) -> str:
    if _KOR_EPOSTA.search(metin):
        raise KorHata(f"{os.path.basename(yol)}: metinde e-posta biçimli parça var; yazılmadı")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _kor_kayit(x: Any) -> Any:
    if isinstance(x, dict):
        return {str(k): _kor_kayit(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_kor_kayit(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        x = x.item()
    if isinstance(x, float) and not np.isfinite(x):
        return None
    if isinstance(x, (pd.Timestamp, _dt.date)):
        return str(x.date()) if isinstance(x, pd.Timestamp) else str(x)
    return x


def _kor_json(yol: str, obj: Any) -> str:
    return _kor_yaz(yol, json.dumps(_kor_kayit(obj), ensure_ascii=False, indent=1, sort_keys=True, default=str))


def _kor_json_oku(yol: str) -> Any:
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as ex:
        raise KorHata(f"{yol} okunamadı ({type(ex).__name__}: {ex})") from ex


def kor_sha_dosya(yol: str) -> str:
    return V1.vdyt_sha_dosya(yol)


def kor_sha_metin(metin: str) -> str:
    return hashlib.sha256(metin.encode("utf-8")).hexdigest()


def kor_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: KOR_ESIK (sıralı JSON) + VDYT2 G5 tanım eşikleri (V2.VDYT2_ESIK 'sessiz', 'bolge', 'buyuk', 'gecerli') sha256."""
    s = json.dumps({"KOR": E or KOR_ESIK, "VDYT2_SESSIZ": {k: V2.VDYT2_ESIK[k] for k in ("sessiz", "bolge", "buyuk", "gecerli", "atr_ref", "savunma")}},
                   sort_keys=True, default=str, ensure_ascii=False)
    return kor_sha_metin(s)


def kor_kod_sha(yol: Optional[str] = None) -> str:
    return kor_sha_dosya(yol or os.path.join(KOK_KOR, "KOR_TEST.py"))


def kor_bagimli_kod(E: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """VDYT2.py / VDYT.py sha256'sı VDYT2 ön kaydındakiyle aynı olmalı (dedektör değişmedi); değilse durur."""
    E = E or KOR_ESIK
    v2 = kor_sha_dosya(os.path.join(KOK_KOR, "VDYT2.py")); v1 = kor_sha_dosya(os.path.join(KOK_KOR, "VDYT.py"))
    if v2 != E["vdyt2"]["kod_sha256"] or v1 != E["vdyt2"]["vdyt_kod_sha256"]:
        raise KorHata(f"VDYT2.py / VDYT.py VDYT2 ön kaydındakinden farklı (VDYT2 {v2[:12]}, VDYT {v1[:12]}); dedektör değişmiş olabilir, durdu")
    return {"VDYT2.py": v2, "VDYT.py": v1, "VDYT2B.py": kor_sha_dosya(os.path.join(KOK_KOR, "VDYT2B.py"))}


def kor_git_durum(yol: str) -> Dict[str, str]:
    """Dosya git'e işlenmiş ve çalışma kopyası HEAD ile aynı mı? Değilse KorHata. Döner son commit ve zamanı."""
    kl = os.path.dirname(os.path.abspath(yol)); ad = os.path.basename(yol)
    try:
        r = subprocess.run(["git", "-C", kl, "ls-files", "--error-unmatch", ad], capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            raise KorHata(f"{ad} git'e işlenmemiş (ön kayıt / kod önce commit edilmeli)")
        r = subprocess.run(["git", "-C", kl, "diff", "--quiet", "HEAD", "--", ad], capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            raise KorHata(f"{ad} işlenmiş sürümden farklı (commit sonrası değişmiş)")
        r = subprocess.run(["git", "-C", kl, "log", "-1", "--format=%H|%cI", "--", ad], capture_output=True, text=True, timeout=30)
        h, z = (r.stdout.strip().split("|") + [""])[:2]
        if not h:
            raise KorHata(f"{ad}: git geçmişi yok")
        return {"commit": h, "commit_zamani": z}
    except (OSError, subprocess.SubprocessError) as ex:
        raise KorHata(f"git denetimi yapılamadı ({type(ex).__name__}: {ex})") from ex


# ---------------------------------------------------------------- 1) TIINGO ÖNBELLEĞİ (YALNIZ OKUMA; istek yok)
def kor_pilot_tanim() -> Dict[str, Dict[str, Any]]:
    return {s["kod"]: dict(s) for s in V2B.VDYT2B_ESIK["B"]["pilot"]["semboller"]}


def kor_tiingo_kayit(kod: str, kl: Optional[str] = None) -> Optional[Dict[str, Any]]:
    y = os.path.join(kl or KOR_YOL["tiingo"], f"{kod}.json")
    if not os.path.exists(y):
        return None
    return _kor_json_oku(y)


def kor_tiingo_ham(kayit: Optional[Dict[str, Any]]) -> Optional[pd.DataFrame]:
    """Önbellek kaydı -> bütün alanlar (ham + adj + splitFactor + divCash), tarih indeksli. Boşsa None."""
    if not kayit or kayit.get("durum") != "ok" or not kayit.get("veri"):
        return None
    R = pd.DataFrame(kayit["veri"])
    if "date" not in R:
        return None
    R.index = pd.to_datetime(R.date.astype(str).str[:10]); R = R[~R.index.duplicated(keep="last")].sort_index()
    for k in ("open", "high", "low", "close", "volume", "adjOpen", "adjHigh", "adjLow", "adjClose", "adjVolume", "splitFactor", "divCash"):
        R[k] = pd.to_numeric(R[k], errors="coerce") if k in R else np.nan
    return R.drop(columns=["date"])


def kor_tiingo_temiz(kayit: Optional[Dict[str, Any]]) -> Tuple[Optional[pd.DataFrame], Optional[pd.Series]]:
    """VDYT2-B ile aynı yol: V2B.v2b_tiingo_df (bölünme düzeltmeli) -> V1.vdyt_bar_temizle -> ABD başlangıcı + fon krizi kesiği. Döner (d: o,h,l,c,v; ham kapanış
    d'nin günlerine hizalı)."""
    X = V2B.v2b_tiingo_df(kayit)
    if X is None:
        return None, None
    E1 = V2._v2_e1()
    d = V1._vdyt_kes(V1.vdyt_bar_temizle(X[["Open", "High", "Low", "Close", "Volume"]], E1), V1.VDYT_ESIK["pazar"]["ABD"]["bas"], E1)
    return d, X.rc.reindex(d.index).astype(float)


# ---------------------------------------------------------------- 2) İŞ 1: OHLC DOĞRULAMASI
def _kor_donuk(R: pd.DataFrame) -> np.ndarray:
    """Donuk bar: O = H = L = C = önceki kapanış (işlem durması / dolgu barı)."""
    o, h, l, c = (R[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    onc = np.r_[np.nan, c[:-1]]
    return (o == h) & (h == l) & (l == c) & (c == onc)


def kor_adj_denetim(R: pd.DataFrame, tol: float = 1e-6, olay_tol: float = 0.005) -> Dict[str, Any]:
    """Düzeltilmiş alanlar: (a) aynı gün adjX / X oranlarının birbirine eşitliği (O, H, L, C); (b) f = adjClose / close katsayısının yalnız bölünme / temettü
    günlerinde değişmesi; (c) olay günü beklenen oran f[t-1] / f[t] = (1 - divCash / close[t-1]) / splitFactor ile uyum (CRSP türü geriye düzeltme)."""
    out: Dict[str, Any] = {"adj_alan_var": bool(all(k in R and R[k].notna().all() for k in ("adjOpen", "adjHigh", "adjLow", "adjClose")))}
    if not out["adj_alan_var"]:
        return out
    with np.errstate(invalid="ignore", divide="ignore"):
        f = (R.adjClose / R.close).to_numpy(float)
        sap = np.nanmax(np.abs(np.column_stack([(R.adjOpen / R.open).to_numpy(float), (R.adjHigh / R.high).to_numpy(float),
                                                (R.adjLow / R.low).to_numpy(float)]) / f[:, None] - 1.0), axis=1)
        deg = f[:-1] / f[1:]
        bek = (1.0 - R.divCash.fillna(0.0).to_numpy(float)[1:] / R.close.to_numpy(float)[:-1]) / R.splitFactor.fillna(1.0).to_numpy(float)[1:]
    olay = (R.splitFactor.fillna(1.0).to_numpy(float)[1:] != 1.0) | (R.divCash.fillna(0.0).to_numpy(float)[1:] > 0)
    degisim = np.abs(deg - 1.0) > tol
    out.update({"alanlar_arasi_sapma_gun": int(np.nansum(sap > tol)), "alanlar_arasi_maks_sapma": float(np.nanmax(sap)) if len(sap) else 0.0,
                "katsayi_degisim_gun": int(degisim.sum()), "olaysiz_degisim_gun": int((degisim & ~olay).sum()), "olay_gun": int(olay.sum()),
                "olay_uyumsuz_gun": int((olay & (np.abs(deg / bek - 1.0) > olay_tol)).sum()),
                "olay_uyumsuz": [[str(g.date()), round(float(x / y - 1.0), 4)] for g, x, y, u in zip(R.index[1:], deg, bek, olay & (np.abs(deg / bek - 1.0) > olay_tol))
                                 if u],
                "bolunme": int((R.splitFactor.fillna(1.0) != 1.0).sum()), "temettu": int((R.divCash.fillna(0.0) > 0).sum())})
    return out


def kor_ohlc_olc(kod: str, R: pd.DataFrame, f25: str, tur: str) -> Dict[str, Any]:
    """Tek sembolün OHLC denetimi (sayılar; fiyat tablosu yok)."""
    f = pd.Timestamp(f25); o, h, l, c, v = (R[k].astype(float) for k in ("open", "high", "low", "close", "volume"))
    ic = (h < np.maximum(o, c) - 1e-9) | (l > np.minimum(o, c) + 1e-9) | (h < l)
    donuk = _kor_donuk(R)
    with np.errstate(invalid="ignore", divide="ignore"):
        lr = np.log(c / c.shift(1))
    sic = (lr.abs() > np.log(10.0)) & (R.splitFactor.fillna(1.0) == 1.0)
    sic_g = list(R.index[sic.to_numpy(bool)])
    geri = 0   # geri dönen sıçrama: ertesi gün ters yönde neredeyse aynı büyüklükte (iki günlük toplam |ln| < ln 2) -> hatalı tik belirtisi
    for g in sic_g:
        j = int(R.index.get_loc(g))
        if j + 1 < len(lr) and abs(float(lr.iloc[j] + lr.iloc[j + 1])) < np.log(2.0):
            geri += 1
    once = R[R.index < f]; son60 = once.tail(60); yil_once = once.iloc[-310:-250] if len(once) >= 310 else once.iloc[:0]
    sonra = R[R.index >= f]
    with np.errstate(invalid="ignore", divide="ignore"):
        rng60 = ((son60.high - son60.low) / son60.close).median() if len(son60) else np.nan
        rng_y = ((yil_once.high - yil_once.low) / yil_once.close).median() if len(yil_once) else np.nan
    d_once = donuk[: len(once)]
    r: Dict[str, Any] = {
        "kod": kod, "tur": tur, "f25": f25, "bar": int(len(R)), "ilk": str(R.index[0].date()), "son": str(R.index[-1].date()),
        "ohlcv_dolu_pay": float(R[["open", "high", "low", "close", "volume"]].notna().all(axis=1).mean()),
        "ic_ihlal": int(ic.sum()), "sifir_negatif_fiyat": int((R[["open", "high", "low", "close"]] <= 0).any(axis=1).sum()),
        "hacim_sifir_pay": float((v.fillna(0) <= 0).mean()), "donuk_bar": int(donuk.sum()), "donuk_bar_f25_once": int(d_once.sum()),
        "donuk_hacimli": int((donuk & (v.fillna(0).to_numpy() > 0)).sum()),
        "f25_once_bar": int(len(once)), "f25_sonra_bar": int(len(sonra)),
        "son60_HL_esit_pay": float((son60.high == son60.low).mean()) if len(son60) else None,
        "son60_donuk_pay": float(donuk[max(0, len(once) - 60): len(once)].mean()) if len(once) else None,
        "son60_hacim_sifir_pay": float((son60.volume.fillna(0) <= 0).mean()) if len(son60) else None,
        "son60_medyan_aralik": float(rng60) if np.isfinite(rng60) else None,
        "aralik_orani_son60_bir_yil_once": float(rng60 / rng_y) if np.isfinite(rng60) and np.isfinite(rng_y) and rng_y > 0 else None,
        "otc_HL_esit_pay": float((sonra.high == sonra.low).mean()) if len(sonra) else None,
        "sicrama": int(sic.sum()), "sicrama_f25_once": int(sum(g < f for g in sic_g)), "sicrama_f25_sonra": int(sum(g >= f for g in sic_g)),
        "sicrama_geri_donen": int(geri), "sicrama_gun": [str(g.date()) for g in sic_g][:12],
        "bosluk_15g": int(V1.vdyt_kopuk(R.index).sum()),
    }
    r.update(kor_adj_denetim(R))
    return r


def kor_ohlc_karsilastir(T: pd.DataFrame, Y: pd.DataFrame) -> Dict[str, Any]:
    """Tiingo bölünme düzeltmeli OHLC (Open..Close) ile bağımsız seri (Yahoo; bölünme düzeltmeli) ortak günlerde: alan başına medyan |oran - 1|, %1 içinde
    payı; kapanış ln getiri korelasyonu."""
    ort = T.index.intersection(Y.index)
    out: Dict[str, Any] = {"ortak_gun": int(len(ort))}
    if len(ort) < 2:
        return out
    if len(ort):
        out["ilk"] = str(ort[0].date()); out["son"] = str(ort[-1].date())
    for a in ("Open", "High", "Low", "Close"):
        with np.errstate(invalid="ignore", divide="ignore"):
            q = np.abs(T[a].reindex(ort).to_numpy(float) / Y[a].reindex(ort).to_numpy(float) - 1.0)
        q = q[np.isfinite(q)]
        out[a] = {"medyan_sapma": float(np.median(q)) if len(q) else None, "yuzde1_ici_pay": float((q <= 0.01).mean()) if len(q) else None}
    if len(ort) >= 30:
        a = T.Close.reindex(ort).astype(float); b = Y.Close.reindex(ort).astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            ra, rb = np.log(a / a.shift(1)).to_numpy()[1:], np.log(b / b.shift(1)).to_numpy()[1:]
        ok = np.isfinite(ra) & np.isfinite(rb)
        out["kapanis_getiri_korelasyon"] = float(np.corrcoef(ra[ok], rb[ok])[0, 1]) if ok.sum() > 10 else None
    return out


def _kor_yahoo_k60(kod: str) -> Optional[pd.DataFrame]:
    d, _m = V1.vdyt_yahoo_oku(os.path.join(V1.VDYT_YOL["k60_fiyat"], f"{kod}.json"))
    return d


def _kor_yahoo_k34(kod: str) -> Optional[pd.DataFrame]:
    try:
        import pickle
        with open(KOR_YOL["k34"], "rb") as f:
            X = pickle.load(f)
        d = X.get(kod)
        if d is None:
            return None
        d = d.copy(); d.index = pd.to_datetime(d.index); d.index = d.index.tz_localize(None) if d.index.tz is not None else d.index
        return d.astype(float)
    except (OSError, KeyError, ValueError, AttributeError, EOFError) as ex:
        korlog.warning("k34 Yahoo okunamadı: %s", type(ex).__name__)
        return None


def kor_ohlc_grafik(kod: str, kayit: Dict[str, Any], f25: str, yol: str, E: Optional[Dict[str, Any]] = None) -> str:
    """İŞ 1 örnek grafiği (ana oturumun Cemal'e özel göstermesi için; repoya girmez): Form 25 öncesi son 120 bar, bölünme düzeltmeli Tiingo OHLC (temizlenmemiş;
    donuk barlar görünür), hacim paneli; başlıkta kod ve tarih aralığı; fiyat ekseni gerçek ($)."""
    E = E or KOR_ESIK; G = E["grafik"]
    import matplotlib.pyplot as plt
    X = V2B.v2b_tiingo_df(kayit)
    if X is None:
        raise KorHata(f"{kod}: seri yok")
    W = X[X.index < pd.Timestamp(f25)].tail(int(G["bar"]))
    if not len(W):
        W = X.tail(int(G["bar"]))
    win = pd.DataFrame({"o": W.Open, "h": W.High, "l": W.Low, "c": W.Close, "v": W.Volume.fillna(0)})
    fig = kor_ciz_fig(win, E)
    try:
        fig.subplots_adjust(top=0.95)
        fig.axes[0].set_title(f"{kod} | Tiingo | Form 25 ({f25}) öncesi son {len(W)} bar: {W.index[0].date()} .. {W.index[-1].date()} | yalnız iç inceleme",
                              fontsize=10)
        os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
        fig.savefig(yol, dpi=int(G["dpi"]), metadata={"Software": None})
    finally:
        plt.close(fig)
    return yol


def kor_ohlc(cikti: Optional[str] = None, kl: Optional[str] = None, png: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """İŞ 1: 12 pilot serisi (yalnız önbellek) -> ölçüler, bağımsız karşılaştırmalar, hüküm; rapor + json + örnek grafikler."""
    E = E or KOR_ESIK; P = kor_pilot_tanim(); pk = _kor_json_oku(os.path.join(cikti or KOR_YOL["cikti"], "vdyt2b_pilot.json"))
    gecti = {r["kod"]: bool(r.get("GECTI")) for r in pk["sonuc"]}
    out: Dict[str, Any] = {"zaman": _kor_simdi(), "sembol": [], "bagimsiz": {}, "grafik": []}
    for kod, s in P.items():
        R = kor_tiingo_ham(kor_tiingo_kayit(kod, kl))
        if R is None:
            out["sembol"].append({"kod": kod, "tur": s["tur"], "veri": "YOK"}); continue
        r = kor_ohlc_olc(kod, R, s["f25"], s["tur"]); r["pilot_gecti"] = gecti.get(kod)
        out["sembol"].append(r)
        try:
            out["grafik"].append(kor_ohlc_grafik(kod, kor_tiingo_kayit(kod, kl), s["f25"], os.path.join(png or KOR_YOL["ohlc_png"], f"{kod}_son120.png"), E))
        except (KorHata, ValueError, OSError, KeyError) as ex:
            korlog.warning("%s grafiği çizilemedi: %s", kod, ex)
    # bağımsız karşılaştırmalar
    B: Dict[str, Any] = {}
    Rs = kor_tiingo_ham(kor_tiingo_kayit("SUNE", kl))
    if Rs is not None:
        Ts = V2B.v2b_tiingo_df(kor_tiingo_kayit("SUNE", kl))
        y60 = _kor_yahoo_k60("SUNE"); y34 = _kor_yahoo_k34("SUNE")
        B["SUNE_k60_yahoo"] = kor_ohlc_karsilastir(Ts, y60) if y60 is not None else {"durum": "kaynak yok"}
        B["SUNE_k34_yahoo"] = kor_ohlc_karsilastir(Ts, y34) if y34 is not None else {"durum": "kaynak yok"}
        f = pd.Timestamp(P["SUNE"]["f25"]); eski = Rs[(Rs.index >= f - pd.Timedelta(days=550)) & (Rs.index < f)]
        B["SUNE_sunedison_donemi"] = {"bar": int(len(eski)), "medyan_gunluk_islem_degeri_usd": float((eski.close * eski.volume).median()) if len(eski) else None,
                                      "not": "Form 25 (2016-05-06) öncesi 18 ay; Tiingo SUNE kaydı k60 Yahoo SUNE (bugünkü SUNation, eski CSI) ile aynı seri"}
    Rc = kor_tiingo_ham(kor_tiingo_kayit("CHK", kl))
    if Rc is not None:
        yb = pd.Timestamp("2021-02-10"); sonra = Rc[Rc.index >= yb]; dk = _kor_donuk(Rc)[Rc.index >= yb]
        exe = _kor_yahoo_k60("EXE")
        b: Dict[str, Any] = {"yeni_bas_sonrasi_bar": int(len(sonra)), "yeni_bas_sonrasi_donuk": int(dk.sum()),
                             "yeni_bas_sonrasi_hacimli_bar": int((sonra.volume.fillna(0) > 0).sum()),
                             "en_uzun_bosluk_takvim_gun": int(np.diff(sonra.index.values).max() / np.timedelta64(1, "D")) if len(sonra) > 1 else None,
                             "eski_sirket_son_bar": str(Rc[Rc.index < yb].index[-1].date())}
        if exe is not None:
            g = pd.Timestamp("2024-10-04")
            if g in Rc.index and g in exe.index:
                b["tekil_2024_10_04"] = {"tiingo_CHK_kapanis": float(Rc.at[g, "close"]), "tiingo_CHK_hacim": float(Rc.at[g, "volume"]),
                                         "k60_EXE_acilis": float(exe.at[g, "Open"]), "k60_EXE_yuksek": float(exe.at[g, "High"]),
                                         "k60_EXE_dusuk": float(exe.at[g, "Low"]), "k60_EXE_kapanis": float(exe.at[g, "Close"]),
                                         "EXE_araliginda": bool(exe.at[g, "Low"] <= Rc.at[g, "close"] <= exe.at[g, "High"])}
            b["EXE_ortak_gun"] = kor_ohlc_karsilastir(V2B.v2b_tiingo_df(kor_tiingo_kayit("CHK", kl)), exe)
        B["CHK"] = b
    Rv = kor_tiingo_ham(kor_tiingo_kayit("SIVBQ", kl))
    if Rv is not None:
        g = pd.Timestamp("2023-03-09"); B["SIVB"] = {"basin_kapanis_2023_03_09": 106.04}
        if g in Rv.index:
            B["SIVB"].update({"tiingo_kapanis": float(Rv.at[g, "close"]), "tiingo_acilis": float(Rv.at[g, "open"]), "tiingo_yuksek": float(Rv.at[g, "high"]),
                              "tiingo_dusuk": float(Rv.at[g, "low"]), "onceki_kapanis": float(Rv.close[Rv.index < g].iloc[-1]),
                              "acilis_yuksek_dusuk_bagimsiz_kaynak": "YOK (yerelde yalnız basın kapanışı)"})
        d = _kor_donuk(Rv); w = (Rv.index > g) & (Rv.index < pd.Timestamp("2023-03-28"))
        B["SIVB"]["durma_donemi_bar"] = int(w.sum()); B["SIVB"]["durma_donemi_donuk"] = int((d & w).sum())
        B["SIVB"]["durma_donemi_donuk_hacimli"] = int((d & w & (Rv.volume.fillna(0).to_numpy() > 0)).sum())
    out["bagimsiz"] = B
    out["hukum"] = kor_ohlc_hukum(out["sembol"], B)
    _kor_json(_kor_yol("ohlc_json", cikti), out)
    _kor_yaz(_kor_yol("ohlc_md", cikti), kor_ohlc_md(out))
    korlog.info("İŞ 1: %s", out["hukum"]["karar"])
    return out


def kor_ohlc_hukum(S: List[Dict[str, Any]], B: Dict[str, Any]) -> Dict[str, Any]:
    """Sembol başına 'batan şirketin borsa dönemi OHLC'si': VAR = seri batan şirketi taşıyor, Form 25 öncesi >= 252 bar, OHLCV dolu >= %99, iç ihlal 0, sıfır /
    negatif 0, Form 25 öncesi açıklanamayan (geri dönen) sıçrama 0; KISMEN = taşıyor ama dolgu (donuk) / kayıt karışması temizlik gerektiriyor; YOK = batan
    şirketin fiyatı kayıtta yok. Genel: VAR >= 10 / 12 -> VAR; VAR + KISMEN >= 8 -> KISMEN; aksi YOK. (Betimleyici kural; bu iş için, veri keşfinden sonra
    yazıldı, ön kayıtlı değil; pilot kararını değiştirmez.)"""
    hk: Dict[str, str] = {}; neden: Dict[str, str] = {}
    for r in S:
        k = r["kod"]
        if r.get("veri") == "YOK":
            hk[k] = "YOK"; neden[k] = "önbellekte seri yok"; continue
        if k == "SUNE":
            hk[k] = "YOK"; neden[k] = "kayıt bugünkü SUNation (eski CSI) serisi; SunEdison fiyatı yok"; continue
        temel = (r["f25_once_bar"] >= 252 and r["ohlcv_dolu_pay"] >= 0.99 and r["ic_ihlal"] == 0 and r["sifir_negatif_fiyat"] == 0
                 and r.get("olaysiz_degisim_gun", 0) == 0)
        if not temel:
            hk[k] = "KISMEN"; neden[k] = "temel denetimlerden biri tutmadı"; continue
        if k == "CHK":
            hk[k] = "KISMEN"; neden[k] = "eski şirket 2021-02-09'a kadar tam; sonrasında donuk dolgu + 2024-10-04 tek yabancı bar (kesilmeli)"; continue
        if r["donuk_bar_f25_once"] > 3:
            hk[k] = "KISMEN"; neden[k] = (f"Form 25 öncesi {r['donuk_bar_f25_once']} donuk bar (O = H = L = C = önceki kapanış: işlem durması dolgusu ya da işlemsiz "
                                          "gün; bir kısmı hacimli, bar temizliği atmaz) ayıklanmalı"); continue
        hk[k] = "VAR"; neden[k] = "tam"
    nv = sum(v == "VAR" for v in hk.values()); nk = sum(v == "KISMEN" for v in hk.values())
    karar = "VAR" if nv >= 10 else ("KISMEN" if nv + nk >= 8 else "YOK")
    return {"sembol": hk, "neden": neden, "VAR": nv, "KISMEN": nk, "YOK": len(hk) - nv - nk, "karar": karar}


def _kor_f(x: Any, n: int = 3) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    if isinstance(x, bool):
        return "evet" if x else "hayır"
    if isinstance(x, (int, np.integer)):
        return f"{int(x):,}".replace(",", ".")
    return f"{float(x):.{n}f}".replace(".", ",")


def kor_ohlc_md(O: Dict[str, Any]) -> str:
    H = O["hukum"]; B = O["bagimsiz"]
    L = [f"# VDYT2-B — Tiingo batan şirket OHLC doğrulaması (İŞ 1; yalnız önbellek, yeni istek yok)\n\nÜretim: {O['zaman']} (`python KOR_TEST.py ohlc`). "
         "Tiingo fiyat değerleri lisans gereği bu dosyada TABLO olarak yok; yalnız sayımlar, oranlar ve birkaç tekil karşılaştırma değeri. Örnek grafikler "
         "(Form 25 öncesi son 120 bar, mum + hacim) /tmp/vdyt2b/ohlc_ornek/ (repoya girmez).\n\n",
         f"## SONUÇ: Tiingo batanlarda OHLC: **{H['karar']}**\n\n",
         f"- Batan şirketin borsa dönemi OHLC'si: VAR {H['VAR']} / KISMEN {H['KISMEN']} / YOK {H['YOK']} (12 sembol).\n"]
    for k, v in H["sembol"].items():
        L.append(f"  - {k}: {v} — {H['neden'][k]}\n")
    L.append("- Hüküm kuralı (betimleyici; bu iş için veri keşfinden sonra yazıldı, ön kayıtlı DEĞİL; pilot kararı KISMEN değişmez): VAR = Form 25 öncesi >= 252 bar, OHLCV dolu >= %99, iç tutarlılık ihlali 0, sıfır / "
             "negatif fiyat 0, düzeltme katsayısı olay dışında değişmiyor, donuk dolgu <= 3 bar ve kayıt batan şirketi taşıyor; KISMEN = taşıyor ama temizlik "
             "gerekiyor; YOK = batan şirketin fiyatı kayıtta yok. Genel: VAR >= 10 -> VAR; VAR + KISMEN >= 8 -> KISMEN; aksi YOK.\n\n")
    L.append("## 1. Sembol tablosu (sayılar)\n\n| kod | tür | pilot | bar | ilk | son | Form 25 öncesi bar | OHLCV dolu | iç ihlal | sıfır/neg | hacim 0 payı | "
             "donuk bar (F25 öncesi / hacimli) | son 60: H=L payı | son 60: medyan (H-L)/C | aralık oranı son60 / 1 yıl önce | OTC H=L payı | sıçrama "
             "(F25 önce / sonra / geri dönen) | > 15 gün boşluk |\n|" + "---|" * 18 + "\n")
    for r in O["sembol"]:
        if r.get("veri") == "YOK":
            L.append(f"| {r['kod']} | {r['tur']} | VERİ YOK |" + " |" * 15 + "\n"); continue
        L.append(f"| {r['kod']} | {r['tur']} | {'GEÇTİ' if r.get('pilot_gecti') else 'kaldı'} | {_kor_f(r['bar'])} | {r['ilk']} | {r['son']} | "
                 f"{_kor_f(r['f25_once_bar'])} | {_kor_f(r['ohlcv_dolu_pay'])} | {r['ic_ihlal']} | {r['sifir_negatif_fiyat']} | {_kor_f(r['hacim_sifir_pay'])} | "
                 f"{r['donuk_bar_f25_once']} ({r['donuk_bar']} toplam / {r['donuk_hacimli']} hacimli) | {_kor_f(r['son60_HL_esit_pay'])} | "
                 f"{_kor_f(r['son60_medyan_aralik'], 4)} | {_kor_f(r['aralik_orani_son60_bir_yil_once'], 2)} | {_kor_f(r['otc_HL_esit_pay'])} | "
                 f"{r['sicrama_f25_once']} / {r['sicrama_f25_sonra']} / {r['sicrama_geri_donen']} | {r['bosluk_15g']} |\n")
    L.append("\n## 2. Düzeltilmiş alanlar (adjOpen / adjHigh / adjLow / adjClose) ve bölünme / temettü katsayısı\n\n| kod | adj alanları dolu | O/H/L/C aynı gün "
             "katsayı farkı (gün; maks) | katsayı değişen gün | olay dışı değişim | olay günü (bölünme / temettü) | olayda beklenen orandan sapma > %0,5 |\n"
             "|---|---|---|---|---|---|---|\n")
    for r in O["sembol"]:
        if r.get("veri") == "YOK":
            continue
        L.append(f"| {r['kod']} | {_kor_f(r.get('adj_alan_var'))} | {r.get('alanlar_arasi_sapma_gun', '-')} ({_kor_f(r.get('alanlar_arasi_maks_sapma'), 8)}) | "
                 f"{r.get('katsayi_degisim_gun', '-')} | {r.get('olaysiz_degisim_gun', '-')} | {r.get('olay_gun', '-')} ({r.get('bolunme', '-')} / "
                 f"{r.get('temettu', '-')}) | {r.get('olay_uyumsuz_gun', '-')} |\n")
    uy = [f"{r['kod']} {g} (sapma {_kor_f(100 * x, 1)} %)" for r in O["sembol"] for g, x in r.get("olay_uyumsuz", [])]
    L.append("\nOlay günü sapmaları (bölünme / temettü dışında katsayı hiç değişmiyor; bölünmelerin hepsi beklenen oranla aynı): "
             + ("; ".join(uy) if uy else "yok") + " — bunlar özel dağıtım (spin-off / özel temettü) günleri; Tiingo farklı referans fiyat kullanıyor.\n")
    L.append("\nSıçrama günleri (|günlük ln getiri| > ln 10, bölünme günü değil):\n")
    for r in O["sembol"]:
        if r.get("sicrama_gun"):
            L.append(f"- {r['kod']}: {', '.join(r['sicrama_gun'])}\n")
    L.append("\n## 3. Bağımsız kaynakla karşılaştırma\n\n")
    for ad in ("SUNE_k60_yahoo", "SUNE_k34_yahoo"):
        b = B.get(ad)
        if b and b.get("ortak_gun"):
            L.append(f"- {ad.replace('_', ' ')}: ortak {_kor_f(b['ortak_gun'])} gün ({b.get('ilk')} .. {b.get('son')}); medyan |oran - 1| açılış "
                     f"{_kor_f(b['Open']['medyan_sapma'], 6)}, yüksek {_kor_f(b['High']['medyan_sapma'], 6)}, düşük {_kor_f(b['Low']['medyan_sapma'], 6)}, "
                     f"kapanış {_kor_f(b['Close']['medyan_sapma'], 6)}; %1 içinde pay A/Y/D/K {_kor_f(b['Open']['yuzde1_ici_pay'])} / "
                     f"{_kor_f(b['High']['yuzde1_ici_pay'])} / {_kor_f(b['Low']['yuzde1_ici_pay'])} / {_kor_f(b['Close']['yuzde1_ici_pay'])}; kapanış getiri "
                     f"korelasyonu {_kor_f(b.get('kapanis_getiri_korelasyon'), 4)}.\n")
    if "SUNE_sunedison_donemi" in B:
        s = B["SUNE_sunedison_donemi"]
        L.append(f"- SUNE SunEdison dönemi: Form 25 öncesi 18 ayda {s['bar']} bar, medyan günlük işlem değeri {_kor_f(s['medyan_gunluk_islem_degeri_usd'], 0)} $ "
                 "(SunEdison bu dönemde günde yüz milyonlarca dolar işlem gören bir NYSE hissesiydi; seri bugünkü SUNation / eski CSI'nin küçük hacimli serisi). "
                 "Tiingo SUNE kaydı yukarıdaki Yahoo SUNE ile 2010'dan beri aynı: SunEdison fiyatı bu kayıtta YOK (pilotta ayrı NYSE 1995-2016 kaydı listede "
                 "görünüyordu; API kodu yeni kayda çözüyor).\n")
    if "CHK" in B:
        c = B["CHK"]
        L.append(f"- CHK: eski şirketin son gerçek barı {c['eski_sirket_son_bar']}; 2021-02-10 ve sonrası {c['yeni_bas_sonrasi_bar']} bar, bunların "
                 f"{c['yeni_bas_sonrasi_donuk']}'i donuk dolgu, hacimli bar {c['yeni_bas_sonrasi_hacimli_bar']}; en uzun boşluk "
                 f"{_kor_f(c.get('en_uzun_bosluk_takvim_gun'))} takvim günü. Yeni şirket (bugün EXE) bu kayıtta YOK; kayıt KARIŞIK değil, eski şirketi taşıyor.\n")
        t = c.get("tekil_2024_10_04")
        if t:
            L.append(f"  - Tekil karşılaştırma 2024-10-04: Tiingo CHK kapanış {_kor_f(t['tiingo_CHK_kapanis'], 2)} $ (hacim {_kor_f(int(t['tiingo_CHK_hacim']))}); "
                     f"k60 EXE aynı gün açılış / yüksek / düşük / kapanış {_kor_f(t['k60_EXE_acilis'], 2)} / {_kor_f(t['k60_EXE_yuksek'], 2)} / "
                     f"{_kor_f(t['k60_EXE_dusuk'], 2)} / {_kor_f(t['k60_EXE_kapanis'], 2)} $ -> EXE gün aralığında: {_kor_f(t['EXE_araliginda'])} (yabancı bar).\n")
    if "SIVB" in B:
        s = B["SIVB"]
        L.append(f"- SIVB 2023-03-09: Tiingo kapanış {_kor_f(s.get('tiingo_kapanis'), 2)} $ = basın kapanışı 106,04 $; aynı gün açılış / yüksek / düşük "
                 f"{_kor_f(s.get('tiingo_acilis'), 2)} / {_kor_f(s.get('tiingo_yuksek'), 2)} / {_kor_f(s.get('tiingo_dusuk'), 2)} $ (önceki kapanış "
                 f"{_kor_f(s.get('onceki_kapanis'), 2)} $; açılış / yüksek / düşük için yerelde bağımsız kaynak YOK, iç tutarlılık geçti). İşlem durması "
                 f"(2023-03-10 .. 03-27) {s['durma_donemi_bar']} bar, {s['durma_donemi_donuk']}'i donuk dolgu ({s['durma_donemi_donuk_hacimli']}'i hacimli: "
                 "VDYT bar temizliği hacimsiz barı atar, hacimli donuk barı ATMAZ).\n")
    L.append("\n## 4. Ne demek (Cemal için)\n\n- Batan şirketlerin çoğunda borsa dönemi açılış / yüksek / düşük / kapanış / hacim tam ve kendi içinde tutarlı; mum "
             "grafiği çizilebilir, G5 hesaplanabilir.\n- İki tuzak var: (1) işlem durması günleri aynı fiyatla 'donuk' doldurulmuş (bazıları küçük hacimli); "
             "bunlar sessiz bölge gibi görünür, temizlenmeden kullanılmamalı. (2) Kod yeniden kullanımında Tiingo kodu BUGÜNKÜ kayda bağlıyor: SUNE'de SunEdison "
             "yok; CHK'de eski şirket var ama sonuna yabancı bir bar eklenmiş. B testinde yinelenen kodlar zaten atılıyor (VDYT2-B 2.2 kural 3).\n"
             "- Bağımsız sağlama sınırlı: kapanış (SIVB) ve tam OHLC (SUNE, yalnız bugünkü şirket) tuttu; batan şirketlerin açılış / yüksek / düşük değerleri "
             "için yerelde ikinci kaynak yok.\n")
    return "".join(L)


# ---------------------------------------------------------------- 3) İŞ 2: KÖR SET (aday listeleri, seçim, grafik, anahtar, manifest)
def _kor_tablo(tur: str, pazar: str, kl: Optional[str] = None) -> pd.DataFrame:
    y = os.path.join(kl or KOR_YOL["vdyt2_tablo"], f"{tur}_{pazar}_G5.csv.gz")
    if not os.path.exists(y):
        raise KorHata(f"VDYT2 tablosu yok: {y} (VDYT2 `kos --asama kasa` ara çıktısı)")
    return pd.read_csv(y)


def kor_icerik_sha(yol: str) -> str:
    """gzip dosyasının AÇILMIŞ içeriğinin sha256'sı (gzip başlığındaki zaman damgasından bağımsız)."""
    import gzip
    h = hashlib.sha256()
    with gzip.open(yol, "rb") as f:
        for p in iter(lambda: f.read(1 << 20), b""):
            h.update(p)
    return h.hexdigest()


def kor_tablo_sha(kl: Optional[str] = None) -> Dict[str, str]:
    kl = kl or KOR_YOL["vdyt2_tablo"]; out = {}
    for tur in ("satir", "kontrol", "bolge"):
        for p in ("BIST", "ABD"):
            out[f"{tur}_{p}_G5.csv.gz"] = kor_sha_dosya(os.path.join(kl, f"{tur}_{p}_G5.csv.gz"))
    return out


def _kor_sag_bos(T: pd.DataFrame, Z: pd.DataFrame, bosluk: int) -> np.ndarray:
    """T satırları (sembol, t) için: [t - bosluk + 1, t] hiçbir bölgenin [bas, bit] aralığıyla kesişmiyor mu (Z: sembol, bas, bit)."""
    ok = np.ones(len(T), bool)
    if not len(T):
        return ok
    zg = {s: g[["bas", "bit"]].to_numpy(np.int64) for s, g in Z.groupby("sembol")}
    for s, idx in T.groupby("sembol").indices.items():
        B = zg.get(s)
        if B is None or not len(B):
            continue
        t = T.t.to_numpy(np.int64)[idx]
        kes = (B[None, :, 0] <= t[:, None]) & (B[None, :, 1] >= (t - bosluk + 1)[:, None])
        ok[idx] = ~kes.any(1)
    return ok


def kor_aday_ana(pazar: str, grup: str, E: Optional[Dict[str, Any]] = None, kl: Optional[str] = None) -> pd.DataFrame:
    """ANA aday listesi (sonuç görülmeden, yalnız VDYT2 tablolarından): G5 = satir GERCEK, yaş [10, 30]; KONTROL = kontrol DISARI, [t-29, t]'de G5 bölgesi
    yok. Sütunlar: sembol, t, bas, yas, tarih, P1 (sembol, t sıralı)."""
    E = E or KOR_ESIK; S = E["set"]
    if grup == "G5":
        T = _kor_tablo("satir", pazar, kl); T = T[(T.kaynak == S["g5_kaynak"]) & T.yas.between(int(S["yas"][0]), int(S["yas"][1]))]
    elif grup == "KONTROL":
        T = _kor_tablo("kontrol", pazar, kl); T = T[T.kaynak == S["kontrol_kaynak"]]
        T = T[_kor_sag_bos(T.reset_index(drop=True), _kor_tablo("bolge", pazar, kl), int(S["sag_bosluk"]))]
    else:
        raise KorHata(f"bilinmeyen grup {grup}")
    T = T[["sembol", "t", "bas", "yas", "tarih", "P1"]].copy(); T["sembol"] = T.sembol.astype(str); T["tarih"] = T.tarih.astype(str).str[:10]
    return T.sort_values(["sembol", "t"]).reset_index(drop=True)


def kor_aday_sha(T: pd.DataFrame) -> str:
    return kor_sha_metin(T[["sembol", "tarih", "t", "yas"]].to_csv(index=False, lineterminator="\n"))


def kor_batan_uygun(d: pd.DataFrame, ham_c: pd.Series) -> np.ndarray:
    """Batan serisinde ABD uygunluk kuralı (VDYT panel kuralının tek hisse karşılığı): bar no >= 252, ham kapanış >= 2 $, 20 gün medyan işlem değeri (en az 10
    gün) >= 1 mn $."""
    U = V1.VDYT_ESIK["pazar"]["ABD"]["uygunluk"]
    deger = (d.c * d.v).rolling(int(U["likit_gun"]), min_periods=10).median().to_numpy()
    no = np.arange(1, len(d) + 1)
    with np.errstate(invalid="ignore"):
        return (no >= int(U["gecmis_gun"])) & (np.nan_to_num(deger) >= float(U["likit_min"])) & (np.nan_to_num(ham_c.to_numpy(float)) >= float(U["fiyat_min"]))


def kor_g5_bolgeler(d: pd.DataFrame, E2: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], np.ndarray]:
    """VDYT2 G5 bölgeleri (V2.v2_olculer + V2.v2_bolgeler; açılış G5, devam G12, min_kosu 1). Döner (Ol, B: bas, tespit, bit, bit_tur)."""
    E2 = E2 or V2.VDYT2_ESIK; Ol = V2.v2_olculer(d, E2); Tn = E2["tanim"]["G5"]
    c = d.c.to_numpy(float)
    B = V2.v2_bolgeler(Ol["durum"][Tn["durum"]], Ol["kopuk"], Ol["tr"], Ol["govde"], c, int(Tn["min_kosu"]), E2, False, Ol["durum"][Tn["devam"]])
    return Ol, B


def kor_aday_batan(E: Optional[Dict[str, Any]] = None, kl: Optional[str] = None, pilot: Optional[Dict[str, Any]] = None
                   ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """BATAN adayları (Tiingo önbelleği; VDYT2 fonksiyonlarıyla): G5 = açık G5 bölgesinde yaş [10, 30] karar günü (t >= tespit, t < bit, uygun, V2.v2_gecerli,
    t < Form 25); KONTROL = hiçbir G5 bölgesinin [bas, bit]'inde değil, [t-29, t]'de bölge yok, uygun, t >= 260, geçerli (sözde yaş 10), t < Form 25."""
    E = E or KOR_ESIK; S = E["set"]; Bt = S["batan"]; E2 = V2.VDYT2_ESIK; P = kor_pilot_tanim(); ilk = int(E2["kontrol"]["ilk_bar"])
    if pilot is not None:
        gecti = sorted(r["kod"] for r in pilot["sonuc"] if r.get("GECTI"))
        if gecti != sorted(Bt["semboller"]):
            raise KorHata(f"batan sembolleri pilot GEÇTİ listesiyle aynı değil: {gecti} != {sorted(Bt['semboller'])}")
    G, K, ozet = [], [], {}
    for kod in Bt["semboller"]:
        d, rc = kor_tiingo_temiz(kor_tiingo_kayit(kod, kl))
        if d is None or len(d) < 300:
            ozet[kod] = {"durum": "veri yok / kısa"}; continue
        f25 = pd.Timestamp(P[kod]["f25"]); uy = kor_batan_uygun(d, rc); Ol, B = kor_g5_bolgeler(d, E2)
        tr, c = Ol["tr"], d.c.to_numpy(float); n = len(d); once = (d.index < f25) if Bt["karar_once_f25"] else np.ones(n, bool)
        icinde = np.zeros(n, bool)
        for b0, _t0, b1, _tur in B.tolist():
            icinde[b0: b1 + 1] = True
        ng = 0
        for b0, t0, b1, _tur in B.tolist():
            for a in E2["karar_yas"]:
                a = int(a)
                if not (int(S["yas"][0]) <= a <= int(S["yas"][1])):
                    continue
                t = b0 + a - 1
                if t < t0 or t >= b1 or t < ilk or not uy[t] or not once[t] or not V2.v2_gecerli(t, b0, tr, c, E2):
                    continue
                G.append((kod, t, b0, a, str(d.index[t].date()), np.nan)); ng += 1
        sag = np.ones(n, bool); bos = int(S["sag_bosluk"])
        for b0, _t0, b1, _tur in B.tolist():
            sag[max(0, b0): min(n, b1 + bos)] = False   # t ∈ [bas, bit + bos - 1] -> [t-bos+1, t] bölgeyle kesişir
        nk = 0; a = int(Bt["kontrol_yas"])
        for t in np.flatnonzero(~icinde & sag & uy & once & (np.arange(n) >= ilk)).tolist():
            if V2.v2_gecerli(t, t - a + 1, tr, c, E2):
                K.append((kod, t, t - a + 1, a, str(d.index[t].date()), np.nan)); nk += 1
        ozet[kod] = {"bar": n, "f25": P[kod]["f25"], "bolge": int(len(B)), "g5_aday": ng, "kontrol_aday": nk, "uygun_gun": int((uy & once).sum())}
    kol = ["sembol", "t", "bas", "yas", "tarih", "P1"]
    Gd = pd.DataFrame(G, columns=kol).sort_values(["sembol", "t"]).reset_index(drop=True)
    Kd = pd.DataFrame(K, columns=kol).sort_values(["sembol", "t"]).reset_index(drop=True)
    return Gd, Kd, ozet


def kor_sec(T: pd.DataFrame, n: int, tohum: Any, haric: Optional[set] = None, uygun_mu: Optional[Callable[[Dict[str, Any]], bool]] = None,
            tekrar: bool = False, ara: int = 120) -> List[Dict[str, Any]]:
    """Tohumlu seçim: default_rng(tohum) permütasyonu sırasıyla aday gezilir. Geçiş 1: farklı hisse ve haric dışı; geçiş 2: farklı hisse (haric serbest);
    geçiş 3 (tekrar=True): aynı hisseden, seçilmiş günlerden >= ara bar uzak. uygun_mu(satır) False ise aday atlanır (pencere / doğrulama). n'den az bulunursa
    bulunanı döner (uydurma yok)."""
    if not len(T) or n <= 0:
        return []
    sira = np.random.default_rng(tohum).permutation(len(T)); kayit = T.to_dict("records"); secilen: List[Dict[str, Any]] = []
    red: set = set(); haric = haric or set()

    def gez(kosul: Callable[[Dict[str, Any]], bool]) -> None:
        for i in sira.tolist():
            if len(secilen) >= n:
                return
            r = kayit[i]
            if i in red or any(r is s for s in secilen) or not kosul(r):
                continue
            if uygun_mu is not None and not uygun_mu(r):
                red.add(i); continue
            secilen.append(r)
    gez(lambda r: r["sembol"] not in {s["sembol"] for s in secilen} and r["sembol"] not in haric)
    gez(lambda r: r["sembol"] not in {s["sembol"] for s in secilen})
    if tekrar:
        gez(lambda r: all(abs(int(r["t"]) - int(s["t"])) >= ara for s in secilen if s["sembol"] == r["sembol"]))
    return secilen


def kor_pencere(d: pd.DataFrame, t: int, bar: int = 120) -> pd.DataFrame:
    """Karar günü t'ye kadar (dahil) son `bar` bar; t'den SONRAKİ hiçbir bar dönmez. Fiyat t kapanışına göre x 100 normalize."""
    if t < bar - 1 or t > len(d) - 1:
        raise KorHata(f"pencere kurulamadı (t={t}, n={len(d)})")
    W = d.iloc[t - bar + 1: t + 1][["o", "h", "l", "c", "v"]].astype(float).copy()
    k = float(W.c.iloc[-1])
    if not np.isfinite(k) or k <= 0:
        raise KorHata("karar günü kapanışı geçersiz")
    W[["o", "h", "l", "c"]] = W[["o", "h", "l", "c"]] / k * 100.0
    return W


def kor_ciz_fig(W: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Any:
    """Mum (gövde + fitil) ve hacim paneli. x = gün sırası (-(n-1) .. 0; karar günü 0, sağ uçta). Başlık / eksen adı / lejant / çizgi / ızgara YOK; hacim
    ekseninde sayı YOK. Döner matplotlib Figure (kaydetmez)."""
    E = E or KOR_ESIK; G = E["grafik"]
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection, PolyCollection
    with matplotlib.rc_context({"axes.unicode_minus": False, "font.size": int(G["font"]), "axes.grid": False, "axes.titlesize": int(G["font"])}):
        px, py = G["piksel"]; dpi = int(G["dpi"])
        fig = plt.figure(figsize=(px / dpi, py / dpi), dpi=dpi)
        gs = fig.add_gridspec(2, 1, height_ratios=[1.0 - float(G["hacim_pay"]), float(G["hacim_pay"])], hspace=0.03, left=0.07, right=0.985, top=0.985,
                              bottom=0.06)
        ax = fig.add_subplot(gs[0]); axv = fig.add_subplot(gs[1], sharex=ax)
        n = len(W); x = np.arange(n) - (n - 1); o, h, l, c, v = (W[k].to_numpy(float) for k in ("o", "h", "l", "c", "v"))
        yuk = c >= o; renk = np.where(yuk, G["yukari"], G["asagi"]); w = float(G["govde_en"]) / 2.0
        aralik = float(np.nanmax(h) - np.nanmin(l)) if n else 1.0; en_az = max(aralik * 0.0015, 1e-12)
        alt = np.minimum(o, c); ust = np.maximum(np.maximum(o, c), alt + en_az)
        ax.add_collection(LineCollection([[(xi, li), (xi, hi)] for xi, li, hi in zip(x, l, h)], colors=list(renk), linewidths=1.0))
        ax.add_collection(PolyCollection([[(xi - w, a), (xi + w, a), (xi + w, b), (xi - w, b)] for xi, a, b in zip(x, alt, ust)],
                                         facecolors=list(renk), edgecolors=list(renk), linewidths=0.6))
        pay = aralik * 0.04 if aralik > 0 else 1.0
        ax.set_ylim(float(np.nanmin(l)) - pay, float(np.nanmax(h)) + pay)
        axv.bar(x, np.nan_to_num(v), width=float(G["govde_en"]), color=list(renk), alpha=0.7, linewidth=0)
        axv.set_ylim(0, float(np.nanmax(v)) * 1.05 if np.nanmax(np.nan_to_num(v)) > 0 else 1.0)
        ax.set_xlim(-n + 0.3, 0.9)
        xt = [int(t) for t in G["x_tik"] if t >= -n]
        axv.set_xticks(xt, labels=[str(t) for t in xt]); axv.set_yticks([])   # düz ASCII eksi (çizim anındaki rcParams'tan bağımsız)
        from matplotlib.ticker import FuncFormatter
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:g}".replace("\u2212", "-")))
        ax.tick_params(axis="x", labelbottom=False)
    return fig


def kor_metinler(fig: Any) -> List[str]:
    """Şekildeki bütün görünür, boş olmayan metinler (eksen sayıları dahil)."""
    import matplotlib.text as mtext
    fig.canvas.draw()
    return [t.get_text() for t in fig.findobj(mtext.Text) if t.get_visible() and t.get_text().strip()]


_KOR_SAYI = re.compile(r"^-?\d+(\.\d+)?$")


def kor_grafik_yaz(W: pd.DataFrame, yol: str, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kör grafik PNG'si (deterministik: yazılım üst verisi yok). Şekilde sayı dışı metin varsa durur. Döner (yol, sha256, bayt, piksel)."""
    E = E or KOR_ESIK
    import matplotlib.pyplot as plt
    fig = kor_ciz_fig(W, E)
    try:
        yabanci = [m for m in kor_metinler(fig) if not _KOR_SAYI.match(m.strip())]
        if yabanci:
            raise KorHata(f"grafikte sayı dışı metin var: {yabanci[:5]}")
        os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
        fig.savefig(yol, dpi=int(E["grafik"]["dpi"]), metadata={"Software": None})
    finally:
        plt.close(fig)
    from PIL import Image
    with Image.open(yol) as im:
        boy = list(im.size)
    return {"dosya": os.path.basename(yol), "sha256": kor_sha_dosya(yol), "bayt": int(os.path.getsize(yol)), "piksel": boy}


def kor_bilesen(Ol: Dict[str, Any], t: int) -> Dict[str, Any]:
    """Anahtar için G5 bileşen değerleri ve günlük durumlar (t günü; hepsi geriye bakar)."""
    D = Ol["durum"]
    out = {k: bool(D[k][t]) for k in ("G1", "G2", "G3", "G4", "G5", "G12")}
    for k in ("m_aralik_atr", "m_govde_atr", "m_maks_aralik", "b_kapanis_bant", "b_govde_bant", "b_egim_tepe", "b_egim_dip"):
        x = float(Ol[k][t]); out[k] = round(x, 6) if np.isfinite(x) else None
    out["g_bilesen"] = int(Ol["g_bilesen"][t])
    return out


def kor_set(cikti: Optional[str] = None, set_kl: Optional[str] = None, E: Optional[Dict[str, Any]] = None, tablo_kl: Optional[str] = None,
            tiingo_kl: Optional[str] = None, F_ver: Optional[Dict[str, Dict[str, Any]]] = None, kod_denetim: bool = True) -> Dict[str, Any]:
    """`set`: aday listeleri -> tohumlu seçim -> 40 grafik (rastgele sıra 1..40) -> anahtar + manifest + aday sha256 + cevap şablonu. Ön kayıt varsa reddeder
    (mühürlü set yeniden üretilmez)."""
    E = E or KOR_ESIK; S = E["set"]; set_kl = set_kl or KOR_YOL["set"]
    if os.path.exists(_kor_yol("onkayit", cikti)):
        raise KorHata("ön kayıt zaten var: kör set mühürlü, yeniden üretilmez")
    bag = kor_bagimli_kod(E) if kod_denetim else {}
    tohum = int(E["tohum"]); E2 = V2.VDYT2_ESIK; bar = int(E["grafik"]["bar"])
    pilot = _kor_json_oku(os.path.join(cikti or KOR_YOL["cikti"], "vdyt2b_pilot.json")) if F_ver is None else None
    F = F_ver or {}
    Z: Dict[str, pd.DataFrame] = {}
    aday: Dict[str, pd.DataFrame] = {}
    for p in ("BIST", "ABD"):
        aday[f"G5_{p}"] = kor_aday_ana(p, "G5", E, tablo_kl); aday[f"KONTROL_{p}"] = kor_aday_ana(p, "KONTROL", E, tablo_kl)
        Z[p] = _kor_tablo("bolge", p, tablo_kl)
    Gb, Kb, batan_ozet = kor_aday_batan(E, tiingo_kl, pilot)
    aday["BATAN_G5"] = Gb; aday["BATAN_KONTROL"] = Kb
    aday_sha = {k: kor_aday_sha(v) for k, v in aday.items()}
    korlog.info("aday sayıları: %s", {k: len(v) for k, v in aday.items()})
    # fiyat (yalnız seçilen hisselerin penceresi için)
    for p in ("BIST", "ABD"):
        if p not in F:
            korlog.info("%s fiyatları yükleniyor (V2.v2_fiyat)", p); F[p] = V2.v2_fiyat(p)
    tiingo_d: Dict[str, pd.DataFrame] = {}
    for kod in S["batan"]["semboller"]:
        d, _rc = kor_tiingo_temiz(kor_tiingo_kayit(kod, tiingo_kl))
        if d is not None:
            tiingo_d[kod] = d
    ol_cache: Dict[Tuple[str, str], Tuple[Dict[str, Any], np.ndarray]] = {}

    def seri(pazar: str, s: str) -> pd.DataFrame:
        return tiingo_d[s] if pazar == "BATAN" else F[pazar]["S"][s]

    def ol(pazar: str, s: str) -> Tuple[Dict[str, Any], np.ndarray]:
        if (pazar, s) not in ol_cache:
            ol_cache[(pazar, s)] = kor_g5_bolgeler(seri(pazar, s), E2)
        return ol_cache[(pazar, s)]

    def denetle(pazar: str, grup: str) -> Callable[[Dict[str, Any]], bool]:
        def f(r: Dict[str, Any]) -> bool:
            s, t = r["sembol"], int(r["t"])
            if pazar != "BATAN" and s not in F[pazar]["S"]:
                return False
            d = seri(pazar, s)
            if t < bar - 1 or t > len(d) - 1 or str(d.index[t].date()) != str(r["tarih"])[:10]:
                korlog.warning("hizalama tutmadı: %s %s t=%d", pazar, s, t); return False
            if S["pencere_kopuk_yok"] and V1.vdyt_kopuk(d.index[t - bar + 1: t + 1])[1:].any():
                return False
            _O, B = ol(pazar, s)
            if grup.endswith("G5"):
                return bool(((B[:, 0] == int(r["bas"])) & (B[:, 1] <= t) & (B[:, 2] > t)).any())
            ic = ((B[:, 0] <= t) & (B[:, 2] >= t - int(S["sag_bosluk"]) + 1)).any()
            return not bool(ic)
        return f
    secim: List[Tuple[str, str, Dict[str, Any]]] = []
    for i, (grup, p, n) in enumerate([("G5", "BIST", S["G5"]["BIST"]), ("G5", "ABD", S["G5"]["ABD"])]):
        for r in kor_sec(aday[f"G5_{p}"], int(n), [tohum, i], None, denetle(p, "G5")):
            secim.append(("G5", p, r))
    g5_hisse = {r["sembol"] for g, _p, r in secim if g == "G5"}
    for i, (p, n) in enumerate([("BIST", S["KONTROL"]["BIST"]), ("ABD", S["KONTROL"]["ABD"])]):
        for r in kor_sec(aday[f"KONTROL_{p}"], int(n), [tohum, 10 + i], g5_hisse, denetle(p, "KONTROL")):
            secim.append(("KONTROL", p, r))
    bg = kor_sec(Gb, int(S["BATAN_G5"]), [tohum, 20], None, denetle("BATAN", "BATAN_G5"), tekrar=bool(S["batan"]["tekrar_izni"]), ara=bar)
    secim += [("BATAN_G5", "BATAN", r) for r in bg]
    bk = kor_sec(Kb, int(S["BATAN_KONTROL"]), [tohum, 21], {r["sembol"] for r in bg}, denetle("BATAN", "BATAN_KONTROL"),
                 tekrar=bool(S["batan"]["tekrar_izni"]), ara=bar)
    secim += [("BATAN_KONTROL", "BATAN", r) for r in bk]
    hedef = {"G5": sum(S["G5"].values()), "KONTROL": sum(S["KONTROL"].values()), "BATAN_G5": int(S["BATAN_G5"]), "BATAN_KONTROL": int(S["BATAN_KONTROL"])}
    bulunan = {g: sum(1 for x in secim if x[0] == g) for g in hedef}
    eksik = {g: hedef[g] - bulunan[g] for g in hedef if bulunan[g] < hedef[g]}
    if eksik:
        korlog.warning("hedeften az bulunan gruplar (uydurulmaz): %s", eksik)
    sira = np.random.default_rng([tohum, 99]).permutation(len(secim))
    gkl = os.path.join(set_kl, KOR_DOSYA["grafik"])
    if os.path.isdir(gkl):
        shutil.rmtree(gkl)
    anahtar: Dict[str, Any] = {}; manifest: List[Dict[str, Any]] = []
    for no0, j in enumerate(sira.tolist()):
        no = no0 + 1; grup, pazar, r = secim[j]; s, t = r["sembol"], int(r["t"]); d = seri(pazar, s); Ol, B = ol(pazar, s)
        g = kor_grafik_yaz(kor_pencere(d, t, bar), os.path.join(gkl, f"grafik_{no:02d}.png"), E)
        bz = None
        if grup.endswith("G5"):
            k = np.flatnonzero((B[:, 0] == int(r["bas"])) & (B[:, 1] <= t) & (B[:, 2] > t))[0]
            bz = {"bas": str(d.index[B[k, 0]].date()), "tespit": str(d.index[B[k, 1]].date()), "bit": str(d.index[B[k, 2]].date()),
                  "bit_tur": V2.BIT_AD.get(int(B[k, 3]), str(int(B[k, 3])))}
        anahtar[str(no)] = {"grup": grup, "alg_g5": int(grup.endswith("G5")), "pazar": "ABD (Tiingo, batan)" if pazar == "BATAN" else pazar, "sembol": s,
                            "tarih": str(d.index[t].date()), "t": t, "yas": int(r["yas"]), "P1": None if pd.isna(r.get("P1")) else float(r["P1"]),
                            "kaynak": "tiingo önbelleği" if pazar == "BATAN" else f"{'satir' if grup == 'G5' else 'kontrol'}_{pazar}_G5.csv.gz",
                            "pencere": [str(d.index[t - bar + 1].date()), str(d.index[t].date())], "bolge": bz, "bilesen": kor_bilesen(Ol, t),
                            "grafik_sha256": g["sha256"]}
        manifest.append({"numara": no, **g})
    ak = _kor_json(_kor_set_yol("anahtar", set_kl), {"surum": KOR_SURUM, "esik_sha256": kor_esik_sha(E), "aday_sha256": aday_sha, "numara": anahtar})
    mk = _kor_json(_kor_set_yol("manifest", set_kl), {"surum": KOR_SURUM, "grafik_sayisi": len(manifest), "grafik": manifest,
                                                       "soru": E["soru"]})
    _kor_json(_kor_set_yol("sablon", set_kl), {str(m["numara"]): {"bolge": "", "destek": ""} for m in manifest})
    _kor_json(_kor_set_yol("aday", set_kl), {"aday_sayisi": {k: len(v) for k, v in aday.items()}, "aday_sha256": aday_sha, "batan_ozet": batan_ozet})
    out = {"zaman": _kor_simdi(), "hedef": hedef, "bulunan": bulunan, "eksik": eksik, "aday_sayisi": {k: len(v) for k, v in aday.items()},
           "aday_sha256": aday_sha, "anahtar": ak, "anahtar_sha256": kor_sha_dosya(ak), "manifest": mk, "manifest_sha256": kor_sha_dosya(mk),
           "grafik_bayt_maks": max((m["bayt"] for m in manifest), default=0), "grafik_bayt_ort": float(np.mean([m["bayt"] for m in manifest])) if manifest else 0,
           "piksel": sorted({tuple(m["piksel"]) for m in manifest}), "batan_ozet": batan_ozet, "bagimli_kod": bag,
           "tablo_sha256": kor_tablo_sha(tablo_kl) if F_ver is None else {}}
    _kor_json(_kor_set_yol("set_ozet.json", set_kl), out)
    korlog.info("kör set: %s grafik; anahtar sha256 %s", len(manifest), out["anahtar_sha256"])
    return out


# ---------------------------------------------------------------- 4) ÖN KAYIT
def kor_onkayit_metin(zaman: str, Z: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or KOR_ESIK; S = E["set"]; O = E["olcum"]; B = O["basari"]; Zy = O["zayif"]
    ic_kasa, wf_ayni = {}, {}
    for k, v in Z.get("tablo_sha256", {}).items():
        yk = os.path.join(KOR_YOL["vdyt2_tablo"], k); yw = os.path.join(KOR_YOL["vdyt2_tablo_wf"], k)
        if not os.path.exists(yk) or kor_sha_dosya(yk) != v:
            raise KorHata(f"{k}: VDYT2 tablosu set üretildikten sonra değişmiş")
        ic_kasa[k] = kor_icerik_sha(yk); wf_ayni[k] = (kor_icerik_sha(yw) == ic_kasa[k]) if os.path.exists(yw) else None
    L = [f"# KÖR TEST ÖN KAYIT — VDYT2 G5 sessiz bölge dedektörü ile insan gözü ({KOR_ETIKET}) — ölçümden (Cemal'in işaretlerinden) ÖNCE\n\n",
         f"Yazım zamanı: {zaman}\nESIK_SHA256: {kor_esik_sha(E)}\nKOD_SHA256: {kor_kod_sha()}\n",
         f"VDYT2_KOD_SHA256: {E['vdyt2']['kod_sha256']}\nVDYT_KOD_SHA256: {E['vdyt2']['vdyt_kod_sha256']}\n",
         f"ANAHTAR_SHA256: {Z['anahtar_sha256']}\nMANIFEST_SHA256: {Z['manifest_sha256']}\nSürüm: {KOR_SURUM}\n\n",
         "Bu dosya ve KOR_TEST.py git'e işlenmeden, eşik mührü / kod / anahtar / manifest sha256'sı tutmadan `olc` ÇALIŞMAZ (KorHata, çıkış 1). Cevap anahtarı "
         "(/tmp/kor_test_vdyt2/anahtar.json) Cemal işaretlemeden repoya KONMAZ; `olc` onu sha256 denetiminden sonra kor_test_anahtar.json olarak kopyalar. Sonuç "
         "görüldükten sonra tanım, eşik, set ya da karar kuralı değişmez; değişirse bu dosyada tarihli SAPMA yazılır.\n\n",
         "## 0. Amaç (Cemal, 12 Kasım 2026, aynen)\n'Tiingo'nun borsadan silinmiş şirketler için geçmiş OHLC verisi sağlayabildiği örneklerle doğrulanmalı. İlk "
         "örneklerde algoritmanın insan gözünün gördüğü sıkışma bölgelerini yakaladığına dair ölçülebilir işaret bulunmalı. Veri dalını kalıcılaştırmak için "
         "acele etmeyelim; önce sinyalin varlığını doğrulayalım; sonra Aralık kotasını yalnızca bu test için kullanalım.'\n"
         "- Soru: VDYT2 G5 dedektörünün 'küçük mumlu sessiz bölge' dediği günleri insan gözü de sessiz bölge olarak görüyor mu, bölge dışı günleri görmüyor mu?\n"
         "- Bu test yalnız BÖLGE TANIMININ insan gözüyle uyumunu ölçer; getiri, yön ya da genişleme tahmini ölçmez (VDYT2 kararları, Ç163 ve VDYT2-B değişmez).\n\n",
         "## 1. Set (40 grafik; kural ve tohum önceden, KOR_ESIK)\n",
         f"- G5 (ANA, {sum(S['G5'].values())}: BIST {S['G5']['BIST']} + ABD {S['G5']['ABD']}): VDYT2 satir_<pazar>_G5.csv.gz (/tmp/vdyt2/kasa; wf klasöründekiyle "
         f"içerik aynı), kaynak GERCEK, karar yaşı {S['yas'][0]}-{S['yas'][1]} (VDYT2 karar yaşları 10 / 15 / 20 / 30; P1 olsun olmasın). Karar günü açık bir G5 "
         "bölgesinin içinde (tespit <= t < bitiş; VDYT2.py fonksiyonlarıyla yeniden hesaplanıp doğrulanır).\n",
         f"- KONTROL ({sum(S['KONTROL'].values())}: BIST {S['KONTROL']['BIST']} + ABD {S['KONTROL']['ABD']}): aynı pazarın kontrol_<pazar>_G5.csv.gz DIŞARI satırları "
         f"(aynı hisse / yıl / NATR ondalığı, bölge dışı, geçerli) VE [t-{int(S['sag_bosluk']) - 1}, t] hiçbir G5 bölgesinin [bas, bit] aralığıyla kesişmez (sağ uçta "
         "son 30 mumda dedektörün bölgesi yok). İlk geçişte G5 grubunun hisseleri dışarıda (tercih).\n",
         f"- BATAN ({int(S['BATAN_G5']) + int(S['BATAN_KONTROL'])}: {S['BATAN_G5']} G5 + {S['BATAN_KONTROL']} kontrol): Tiingo pilot önbelleğinde pilotu GEÇEN 7 seri "
         f"({', '.join(S['batan']['semboller'])}); VDYT2-B ile aynı temizlik (V2B.v2b_tiingo_df -> V1.vdyt_bar_temizle -> 2010-01-01 .. 2026-08-31); G5 durumu ve "
         "bölgeler V2.v2_olculer + V2.v2_bolgeler ile (VDYT2.py DEĞİŞMEDİ); karar günü < Form 25-NSE günü; uygunluk: " + S["batan"]["uygunluk"] + ". BATAN_G5 = açık "
         "G5 bölgesinde yaş 10-30, geçerli; BATAN_KONTROL = bölge dışı, [t-29, t]'de bölge yok, geçerli (sözde yaş 10). Önce farklı hisse; yetmezse aynı hisseden "
         ">= 120 bar uzak ikinci gün. Yetmezse bulunan sayı yazılır (uydurma yok).\n",
         f"- Seçim: numpy default_rng([{E['tohum']}, grup no]) permütasyonu sırasıyla aday gezilir (aday listesi sembol, t sıralı); G5 BIST 0, G5 ABD 1, KONTROL BIST 10, "
         f"KONTROL ABD 11, BATAN_G5 20, BATAN_KONTROL 21; grafik numaraları default_rng([{E['tohum']}, 99]) permütasyonu. Her grupta farklı hisse. Aday atlanır "
         "<=> hizalama tutmaz / 120 barlık pencerede > 15 takvim günü boşluk / bölge doğrulaması tutmaz.\n",
         "- Aday listesi sha256 (sembol, tarih, t, yaş; CSV):\n"]
    for k, v in sorted(Z["aday_sha256"].items()):
        L.append(f"  - {k}: {v} ({_kor_f(Z['aday_sayisi'][k])} aday)\n")
    L.append(f"- Bulunan: {json.dumps(Z['bulunan'], ensure_ascii=False)}" + (f"; EKSİK (bulunamadı, uydurulmadı): {json.dumps(Z['eksik'], ensure_ascii=False)}"
                                                                              if Z["eksik"] else "") + "\n")
    L.append("- VDYT2 tablo sha256 (kasa klasörü; dosya / açılmış içerik; wf klasöründeki aynı adlı tablonun açılmış içeriği aynı mı):\n")
    for k, v in sorted(Z.get("tablo_sha256", {}).items()):
        L.append(f"  - {k}: dosya {v} / içerik {ic_kasa[k]} (wf içerik aynı: {_kor_f(wf_ayni.get(k))})\n")
    G = E["grafik"]
    L.append(f"\n## 2. Grafik\n- Karar gününe kadar son {G['bar']} işlem günü; karar günü SAĞ UÇTA (x = 0); karar gününden sonraki hiçbir bar yok. Mum gövdesi + fitil "
             f"(yukarı {G['yukari']}, aşağı {G['asagi']}), altta hacim paneli (payı {G['hacim_pay']}). Fiyat {G['normal']} (fiyat düzeyi hisseyi / pazarı ele vermez). "
             f"{G['metin']}. {G['piksel'][0]}x{G['piksel'][1]} piksel, {G['dpi']} dpi, PNG üst verisinde yazılım bilgisi yok.\n"
             f"- Grafik sayısı {Z['bulunan'] and sum(Z['bulunan'].values())}; en büyük dosya {_kor_f(Z['grafik_bayt_maks'])} bayt, ortalama "
             f"{_kor_f(Z['grafik_bayt_ort'], 0)} bayt. Klasör /tmp/kor_test_vdyt2/grafik/ (repoya girmez; batan grafikleri Tiingo verisi). Manifest (numara, dosya, "
             "sha256; GRUP BİLGİSİ YOK): /tmp/kor_test_vdyt2/manifest.json.\n")
    Q = E["soru"]
    L.append(f"\n## 3. Cemal'e soru (her grafik)\n- Soru 1 (ANA): '{Q['bolge']}' Cevap: {' / '.join(Q['bolge_cevap'])}.\n- Soru 2 (BİLGİ): '{Q['destek']}' "
             f"Cevap: {' / '.join(Q['destek_cevap'])}.\n- Cevap dosyası: numara -> cevap (JSON {{\"1\": {{\"bolge\": \"EVET\", \"destek\": \"HAYIR\"}}}} ya da "
             "satır başına '1 EVET HAYIR'); 40 numaranın hepsi gerekli; şablon /tmp/kor_test_vdyt2/cevap_sablon.json.\n")
    L.append(f"\n## 4. Ölçüler (önceden)\n- ANA karşılaştırma: G5 ({sum(S['G5'].values())}) ile KONTROL ({sum(S['KONTROL'].values())}). Algoritma etiketi: G5 = 1, KONTROL "
             "= 0. İnsan etiketi: EVET = 1, HAYIR = 0; EMİN DEĞİLİM ayrı sayılır ve oranlarda PAYDADAN ÇIKAR (ANA); sağlama olarak HAYIR'a eklenmiş hali de "
             "yazılır (BİLGİ).\n- p_G5 = EVET / (EVET + HAYIR) G5 grubunda; p_K aynısı KONTROL'de; Wilson %95 aralıkları; fark = p_G5 - p_K, %95 aralığı "
             "Newcombe hibrit Wilson (ANA) ve hisse kümeli bootstrap (B = 2000, tohum 20261119; BİLGİ).\n- Fisher kesin testi (2x2: grup x EVET / HAYIR) İKİ YÖNLÜ p "
             "(karar); tek yönlü (G5 > KONTROL) p BİLGİ.\n- Cohen kappa (algoritma G5 / değil ile insan EVET / HAYIR; EMİN DEĞİLİM hariç).\n- Duyarlılık ve kesinlik "
             "(insan etiketi doğru kabul edilerek): duyarlılık = insanın EVET dediklerinin G5 payı; kesinlik = G5 dediklerinin insan EVET payı; özgüllük de yazılır.\n"
             f"- BİLGİ: BATAN alt grubu ayrı (BATAN_G5 / BATAN_KONTROL; n küçük); 40 grafiğin tümünde kappa; pazar (BIST / ABD) kırılımı; Soru 2 (destek) ile G4 "
             "(gövde tabanı savunma hattı) durumunun uyumu ve kappası.\n")
    L.append(f"\n## 5. KARAR KURALI (önceden)\n- BAŞARILI <=> p_G5 >= {_kor_f(B['g5_evet_min'], 2)} VE p_K <= {_kor_f(B['kontrol_evet_max'], 2)} VE kappa >= "
             f"{_kor_f(B['kappa_min'], 2)} VE Fisher iki yönlü p < {_kor_f(B['fisher_p_max'], 2)}.\n- ZAYIF İŞARET <=> BAŞARILI değil VE p_G5 >= "
             f"{_kor_f(Zy['g5_evet_min'], 2)} VE fark > {_kor_f(Zy['fark_min'], 1)}.\n- İŞARET YOK <=> aksi. VERİ YETERSİZ (G5 ya da KONTROL grubunda EVET + HAYIR < "
             f"{O['min_payda']}) İŞARET YOK sayılır.\n- BATAN alt grubu ve destek sorusu karara girmez (BİLGİ).\n")
    L.append(f"\n## 6. KARAR KULLANIMI (Cemal'in sırası; önceden)\n- {E['karar_kullanimi']}\n- Tiingo'ya bu testte istek yok; Aralık kotası ancak bu karardan sonra "
             "ve yalnız VDYT2-B testi B için kullanılır. Veri dalı kalıcılaştırılmaz (Cemal: 'acele etmeyelim').\n")
    L.append("\n## 7. Yanlılık ve sınırlar (beyan)\n- 40 grafik küçük örneklemdir; sonuç 'bulgu' değil, dedektörün insan gözüyle uyumuna dair İLK işarettir.\n"
             "- Tek değerlendirici (Cemal): değerlendiriciler arası uyum ölçülmez. Cemal VDYT2'nin G5 tanımını biliyor; grafikte grup bilgisi olmadığı için kör.\n"
             "- KONTROL günleri 'sağ uçta son 30 mumda bölge yok' koşuluyla seçildi: soru da son 10-30 mumu sorduğu için bu, soruyla dedektörün aynı pencereye "
             "bakmasını sağlar; bölge dışı ama bölgeye yakın günler (dedektörün sınır davranışı) bu testte ölçülmez.\n"
             "- Fiyat normalize edildi (karar günü kapanışı = 100); hacim ekseni sayısız: düzey / pazar bilgisi gizli. Fiyat ekseni doğrusal.\n"
             "- BATAN uygunluğu tek hisse kuralıyla (kesit paneli kurulmadan); BATAN_KONTROL NATR ondalığıyla eşlenmedi.\n")
    L.append("\n## EK. Eşik sözlüğü (mühür = sha256 of sıralı JSON; VDYT2 sessiz / bölge / büyük mum / geçerlilik eşikleri dahil)\n\n```json\n" +
             json.dumps(E, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n```\n")
    return "".join(L)


def kor_onkayit(cikti: Optional[str] = None, set_kl: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """`onkayit`: set özeti okunur, anahtar / manifest sha256 yeniden hesaplanıp denetlenir, ön kayıt yazılır (varsa üzerine yazmaz)."""
    E = E or KOR_ESIK; y = _kor_yol("onkayit", cikti)
    if os.path.exists(y):
        raise KorHata(f"ön kayıt zaten var: {y} (üzerine yazılmaz)")
    oz = _kor_set_yol("set_ozet.json", set_kl)
    if not os.path.exists(oz):
        raise KorHata("kör set yok: önce `python KOR_TEST.py set`")
    Z = _kor_json_oku(oz)
    for ad, sha in (("anahtar", Z["anahtar_sha256"]), ("manifest", Z["manifest_sha256"])):
        if kor_sha_dosya(_kor_set_yol(ad, set_kl)) != sha:
            raise KorHata(f"{ad}.json set özetindeki sha256 ile tutmuyor")
    A = _kor_json_oku(_kor_set_yol("anahtar", set_kl))
    if A.get("esik_sha256") != kor_esik_sha(E):
        raise KorHata("anahtar farklı eşiklerle üretilmiş (mühür tutmuyor)")
    return _kor_yaz(y, kor_onkayit_metin(_kor_simdi(), Z, E))


def kor_onkayit_oku(yol: str) -> Dict[str, str]:
    if not os.path.exists(yol):
        raise KorHata(f"ön kayıt yok: {yol}")
    with open(yol, encoding="utf-8") as f:
        m = f.read()
    out = {}
    for k in ("ESIK_SHA256", "KOD_SHA256", "ANAHTAR_SHA256", "MANIFEST_SHA256", "Yazım zamanı"):
        r = re.search(rf"^{k}: (.+)$", m, re.M)
        if not r:
            raise KorHata(f"ön kayıtta '{k}' satırı yok")
        out[k] = r.group(1).strip()
    return out


def kor_kapi(cikti: Optional[str] = None, set_kl: Optional[str] = None, E: Optional[Dict[str, Any]] = None, git: bool = True, kod_git: bool = True,
             grafik: bool = True) -> Dict[str, Any]:
    """`olc` ret kapısı: ön kayıt (ve KOR_TEST.py) git'e işlenmiş ve değişmemiş; eşik mührü, kod, anahtar ve manifest sha256'sı ön kayıtla aynı; grafikler (klasör
    varsa) manifestle aynı. Tutmazsa KorHata."""
    E = E or KOR_ESIK; y = _kor_yol("onkayit", cikti); O = kor_onkayit_oku(y); out: Dict[str, Any] = {"onkayit": O}
    if git:
        out["git_onkayit"] = kor_git_durum(y)
        if kod_git:
            out["git_kod"] = kor_git_durum(os.path.join(KOK_KOR, "KOR_TEST.py"))
    if O["ESIK_SHA256"] != kor_esik_sha(E):
        raise KorHata("eşik mührü ön kayıtla tutmuyor (KOR_ESIK ya da VDYT2 eşikleri değişmiş)")
    if O["KOD_SHA256"] != kor_kod_sha():
        raise KorHata("KOR_TEST.py ön kayıttaki sürümden farklı")
    ak = _kor_set_yol("anahtar", set_kl); mk = _kor_set_yol("manifest", set_kl)
    if not os.path.exists(ak) or kor_sha_dosya(ak) != O["ANAHTAR_SHA256"]:
        raise KorHata("cevap anahtarı yok ya da sha256'sı ön kayıtla tutmuyor")
    if not os.path.exists(mk) or kor_sha_dosya(mk) != O["MANIFEST_SHA256"]:
        raise KorHata("manifest yok ya da sha256'sı ön kayıtla tutmuyor")
    M = _kor_json_oku(mk); gkl = _kor_set_yol("grafik", set_kl)
    if grafik and os.path.isdir(gkl):
        bozuk = [m["numara"] for m in M["grafik"] if not os.path.exists(os.path.join(gkl, m["dosya"]))
                 or kor_sha_dosya(os.path.join(gkl, m["dosya"])) != m["sha256"]]
        if bozuk:
            raise KorHata(f"grafikler manifestle tutmuyor: {bozuk[:10]}")
    out["anahtar"] = _kor_json_oku(ak); out["manifest"] = M
    return out


# ---------------------------------------------------------------- 5) ÖLÇÜM
def kor_cevap_norm(x: Any) -> Optional[str]:
    """Serbest yazım -> EVET / HAYIR / EMIN (boş -> None)."""
    if x is None:
        return None
    s = str(x).strip().upper()
    for a, b in (("İ", "I"), ("Ğ", "G"), ("Ü", "U"), ("Ş", "S"), ("Ö", "O"), ("Ç", "C")):
        s = s.replace(a, b)
    s = re.sub(r"\s+", " ", s)
    if not s:
        return None
    if s in ("EVET", "E", "YES", "Y"):
        return "EVET"
    if s in ("HAYIR", "H", "NO", "N"):
        return "HAYIR"
    if s.startswith("EMIN") or s in ("?", "BILMIYORUM", "EMIN DEGILIM", "ED"):
        return "EMIN"
    raise KorHata(f"tanınmayan cevap: {x!r} (EVET / HAYIR / EMİN DEĞİLİM)")


def kor_cevap_oku(yol: str, n: int = 40) -> Dict[int, Dict[str, Optional[str]]]:
    """Cevap dosyası: JSON {numara: 'EVET'} / {numara: {'bolge': .., 'destek': ..}} / {numara: [bolge, destek]} ya da metin satırları 'numara bolge [destek]'
    (ayraç boşluk / virgül / noktalı virgül / sekme / iki nokta). 1..n'nin HEPSİ ve geçerli bölge cevabı gerekir."""
    try:
        with open(yol, encoding="utf-8") as f:
            ham = f.read()
    except OSError as ex:
        raise KorHata(f"cevap dosyası okunamadı: {ex}") from ex
    C: Dict[int, Dict[str, Optional[str]]] = {}
    try:
        J = json.loads(ham)
    except ValueError:
        J = None
    if isinstance(J, dict):
        for k, v in J.items():
            if isinstance(v, dict):
                b, d = v.get("bolge"), v.get("destek")
            elif isinstance(v, (list, tuple)):
                b, d = (list(v) + [None, None])[:2]
            else:
                b, d = v, None
            C[int(k)] = {"bolge": kor_cevap_norm(b), "destek": kor_cevap_norm(d)}
    else:
        for sat in ham.splitlines():
            sat = sat.strip()
            if not sat or sat.startswith("#"):
                continue
            p = [x for x in re.split(r"[\s,;:\t]+", sat) if x]
            if not p[0].isdigit():
                continue
            # 'EMİN DEĞİLİM' iki kelime: birleştir
            kalan = " ".join(p[1:]); m = re.match(r"(?i)^(em[iİı]n( de[gğ][iİı]l[iİı]m)?|\S+)\s*(\S+)?$", kalan)
            b, d = (m.group(1), m.group(3)) if m else (None, None)
            C[int(p[0])] = {"bolge": kor_cevap_norm(b), "destek": kor_cevap_norm(d)}
    eksik = [i for i in range(1, n + 1) if i not in C or C[i]["bolge"] is None]
    fazla = [i for i in C if i < 1 or i > n]
    if eksik or fazla:
        raise KorHata(f"cevap dosyası eksik / fazla: eksik {eksik[:10]} fazla {fazla[:10]}")
    for i, c in C.items():
        if c["destek"] == "EMIN":
            c["destek"] = None
    return C


def kor_wilson(k: int, n: int, z: float = 1.959963984540054) -> Tuple[float, float, float]:
    if n <= 0:
        return np.nan, np.nan, np.nan
    p = k / n; m = z * z; a = (p + m / (2 * n)) / (1 + m / n); h = z * math.sqrt(p * (1 - p) / n + m / (4 * n * n)) / (1 + m / n)
    return p, max(0.0, a - h), min(1.0, a + h)


def kor_newcombe(k1: int, n1: int, k2: int, n2: int, z: float = 1.959963984540054) -> Tuple[float, float, float]:
    """p1 - p2 ve Newcombe hibrit Wilson (yöntem 10) %95 aralığı."""
    p1, l1, u1 = kor_wilson(k1, n1, z); p2, l2, u2 = kor_wilson(k2, n2, z)
    if not (np.isfinite(p1) and np.isfinite(p2)):
        return np.nan, np.nan, np.nan
    d = p1 - p2
    return d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


def kor_fisher(a: int, b: int, c: int, d: int) -> Dict[str, float]:
    """2x2 [[a, b], [c, d]] Fisher kesin testi (hipergeometrik). iki_yonlu: olasılığı gözlenenden büyük olmayan tabloların toplamı; tek_yonlu_buyuk: P(X >= a)
    (birinci satırın birinci sütunu büyük)."""
    r1, r2, c1 = a + b, c + d, a + c; N = r1 + r2
    if N == 0:
        return {"iki_yonlu": np.nan, "tek_yonlu_buyuk": np.nan}
    lo, hi = max(0, c1 - r2), min(r1, c1); tot = math.comb(N, c1)
    P = {x: math.comb(r1, x) * math.comb(r2, c1 - x) / tot for x in range(lo, hi + 1)}
    p0 = P[a]
    return {"iki_yonlu": float(min(1.0, sum(p for p in P.values() if p <= p0 * (1 + 1e-7)))), "tek_yonlu_buyuk": float(sum(p for x, p in P.items() if x >= a))}


def kor_kappa(x: List[int], y: List[int]) -> float:
    """Cohen kappa (iki ikili etiket dizisi)."""
    x = np.asarray(x, int); y = np.asarray(y, int)
    if not len(x):
        return np.nan
    po = float(np.mean(x == y)); pe = float(np.mean(x) * np.mean(y) + (1 - np.mean(x)) * (1 - np.mean(y)))
    return np.nan if pe >= 1.0 else (po - pe) / (1.0 - pe)


def _kor_say(R: List[Dict[str, Any]], grup: str, emin_hayir: bool = False) -> Dict[str, int]:
    g = [r for r in R if r["grup"] == grup]
    e = sum(r["bolge"] == "EVET" for r in g); h = sum(r["bolge"] == "HAYIR" for r in g); m = sum(r["bolge"] == "EMIN" for r in g)
    return {"n": len(g), "evet": e, "hayir": h + (m if emin_hayir else 0), "emin": 0 if emin_hayir else m}


def kor_karsilastir(R: List[Dict[str, Any]], ga: str, gb: str, E: Optional[Dict[str, Any]] = None, emin_hayir: bool = False,
                    bootstrap: bool = True) -> Dict[str, Any]:
    """İki grup (ga: algoritma evet, gb: algoritma hayır) için oranlar, Wilson, Newcombe fark aralığı, Fisher, kappa, duyarlılık / kesinlik / özgüllük,
    hisse kümeli bootstrap fark aralığı."""
    E = E or KOR_ESIK; O = E["olcum"]; z = float(O["z"])
    A = _kor_say(R, ga, emin_hayir); B = _kor_say(R, gb, emin_hayir); na, nb = A["evet"] + A["hayir"], B["evet"] + B["hayir"]
    pa, la, ua = kor_wilson(A["evet"], na, z); pb, lb, ub = kor_wilson(B["evet"], nb, z); d, dl, du = kor_newcombe(A["evet"], na, B["evet"], nb, z)
    fz = kor_fisher(A["evet"], A["hayir"], B["evet"], B["hayir"])
    sec = [r for r in R if r["grup"] in (ga, gb) and (r["bolge"] in ("EVET", "HAYIR") or (emin_hayir and r["bolge"] == "EMIN"))]
    alg = [int(r["grup"] == ga) for r in sec]; ins = [int(r["bolge"] == "EVET") for r in sec]
    tp, fn, fp, tn = A["evet"], B["evet"], A["hayir"], B["hayir"]
    out = {"gruplar": [ga, gb], "emin_hayira": bool(emin_hayir), ga: {**A, "oran": pa, "wilson": [la, ua]}, gb: {**B, "oran": pb, "wilson": [lb, ub]},
           "fark": d, "fark_newcombe": [dl, du], "fisher_iki_yonlu": fz["iki_yonlu"], "fisher_tek_yonlu": fz["tek_yonlu_buyuk"], "kappa": kor_kappa(alg, ins),
           "duyarlilik": tp / (tp + fn) if tp + fn else np.nan, "kesinlik": tp / (tp + fp) if tp + fp else np.nan,
           "ozgulluk": tn / (tn + fp) if tn + fp else np.nan, "payda": [na, nb]}
    if bootstrap and na and nb:
        Bt = O["bootstrap"]; rng = np.random.default_rng(int(Bt["tohum"])); fk = []
        kume = {g: {} for g in (ga, gb)}
        for r in sec:
            kume[r["grup"]].setdefault(r["sembol"], []).append(int(r["bolge"] == "EVET"))
        Ka, Kb = list(kume[ga].values()), list(kume[gb].values())
        for _ in range(int(Bt["B"])):
            xa = [v for i in rng.integers(0, len(Ka), len(Ka)) for v in Ka[i]]; xb = [v for i in rng.integers(0, len(Kb), len(Kb)) for v in Kb[i]]
            if xa and xb:
                fk.append(np.mean(xa) - np.mean(xb))
        out["fark_bootstrap"] = [float(np.percentile(fk, 2.5)), float(np.percentile(fk, 97.5))] if fk else [np.nan, np.nan]
    return out


def kor_karar(K: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or KOR_ESIK; O = E["olcum"]; B = O["basari"]; Z = O["zayif"]; ga, gb = K["gruplar"]
    if min(K["payda"]) < int(O["min_payda"]):
        return "VERİ YETERSİZ"
    pa, pb, kp, p = K[ga]["oran"], K[gb]["oran"], K["kappa"], K["fisher_iki_yonlu"]
    if pa >= B["g5_evet_min"] and pb <= B["kontrol_evet_max"] and np.isfinite(kp) and kp >= B["kappa_min"] and p < B["fisher_p_max"]:
        return "BAŞARILI"
    if pa >= Z["g5_evet_min"] and K["fark"] > Z["fark_min"]:
        return "ZAYIF İŞARET"
    return "İŞARET YOK"


def kor_kota(karar: str) -> str:
    return ("Aralık Tiingo kotası YALNIZ VDYT2-B testi B için kullanılabilir" if karar in ("BAŞARILI", "ZAYIF İŞARET")
            else "B'ye kota HARCANMAZ; dedektör önce düzeltilir (yeni ön kayıtla)")


def kor_olcu(A: Dict[str, Any], C: Dict[int, Dict[str, Optional[str]]], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Anahtar (numara -> grup, ...) + cevaplar -> bütün ölçüler ve karar (saf fonksiyon; dosya yok)."""
    E = E or KOR_ESIK; R = []
    for no, a in A.items():
        c = C[int(no)]; R.append({"no": int(no), "grup": a["grup"], "pazar": a["pazar"], "sembol": a["sembol"], "bolge": c["bolge"], "destek": c.get("destek"),
                                  "g4": (a.get("bilesen") or {}).get("G4")})
    ana = kor_karsilastir(R, "G5", "KONTROL", E)
    out: Dict[str, Any] = {"ana": ana, "karar": kor_karar(ana, E), "saglama_emin_hayir": kor_karsilastir(R, "G5", "KONTROL", E, emin_hayir=True)}
    out["kota"] = kor_kota(out["karar"])
    out["batan"] = kor_karsilastir(R, "BATAN_G5", "BATAN_KONTROL", E)
    R2 = [{**r, "grup": "ALG" if r["grup"].endswith("G5") else "DEG"} for r in R]
    out["tum_40"] = kor_karsilastir(R2, "ALG", "DEG", E)
    out["pazar"] = {}
    for p in ("BIST", "ABD"):
        Rp = [r for r in R if r["pazar"] == p]
        out["pazar"][p] = kor_karsilastir(Rp, "G5", "KONTROL", E, bootstrap=False)
    D = [r for r in R if r["destek"] in ("EVET", "HAYIR") and r["g4"] is not None]
    out["destek"] = {"n": len(D), "uyum": float(np.mean([int(r["destek"] == "EVET") == int(bool(r["g4"])) for r in D])) if D else None,
                     "kappa": kor_kappa([int(bool(r["g4"])) for r in D], [int(r["destek"] == "EVET") for r in D]) if D else None,
                     "insan_evet": sum(r["destek"] == "EVET" for r in D), "g4_dogru": sum(bool(r["g4"]) for r in D)}
    out["satir"] = sorted(R, key=lambda r: r["no"])
    return out


def kor_olc(cevap: str, cikti: Optional[str] = None, set_kl: Optional[str] = None, E: Optional[Dict[str, Any]] = None, git: bool = True,
            kod_git: bool = True) -> Dict[str, Any]:
    """`olc`: ret kapısı -> cevaplar -> ölçüler -> sonuç JSON + rapor; anahtar repoya (kor_test_anahtar.json) kopyalanır."""
    E = E or KOR_ESIK; K = kor_kapi(cikti, set_kl, E, git=git, kod_git=kod_git)
    A = K["anahtar"]["numara"]; C = kor_cevap_oku(cevap, n=len(A))
    S = kor_olcu(A, C, E)
    out = {"zaman": _kor_simdi(), "surum": KOR_SURUM, "kapi": {k: v for k, v in K.items() if k not in ("anahtar", "manifest")},
           "cevap_sha256": kor_sha_dosya(cevap), **S}
    _kor_json(_kor_yol("sonuc", cikti), out)
    shutil.copyfile(_kor_set_yol("anahtar", set_kl), _kor_yol("anahtar_repo", cikti))
    _kor_yaz(_kor_yol("rapor", cikti), kor_rapor_md(out, E))
    korlog.info("kör test: %s (%s)", out["karar"], out["kota"])
    return out


def _kor_oran(x: Dict[str, Any]) -> str:
    return f"{_kor_f(x['oran'], 2)} ({x['evet']} / {x['evet'] + x['hayir']}; Wilson {_kor_f(x['wilson'][0], 2)}-{_kor_f(x['wilson'][1], 2)}; EMİN DEĞİLİM {x['emin']})"


def kor_rapor_md(R: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or KOR_ESIK; A = R["ana"]; B = R["batan"]
    L = [f"# KÖR TEST RAPORU — VDYT2 G5 ile insan gözü ({KOR_ETIKET})\n\nÜretim: {R['zaman']}; ön kayıt commit {R['kapi'].get('git_onkayit', {}).get('commit', '-')}"
         f" ({R['kapi'].get('git_onkayit', {}).get('commit_zamani', '-')}); cevap dosyası sha256 {R['cevap_sha256']}.\n\n",
         f"## SONUÇ: **{R['karar']}** — {R['kota']}\n\n",
         f"- G5 grafiklerinde 'sessiz bölge var' (EVET) oranı: {_kor_oran(A['G5'])}\n- Kontrol grafiklerinde: {_kor_oran(A['KONTROL'])}\n",
         f"- Fark {_kor_f(A['fark'], 2)} (Newcombe %95 {_kor_f(A['fark_newcombe'][0], 2)} .. {_kor_f(A['fark_newcombe'][1], 2)}; hisse kümeli bootstrap "
         f"{_kor_f(A.get('fark_bootstrap', [None, None])[0], 2)} .. {_kor_f(A.get('fark_bootstrap', [None, None])[1], 2)}); Fisher iki yönlü p "
         f"{_kor_f(A['fisher_iki_yonlu'], 4)} (tek yönlü {_kor_f(A['fisher_tek_yonlu'], 4)}); kappa {_kor_f(A['kappa'], 2)}.\n",
         f"- Duyarlılık {_kor_f(A['duyarlilik'], 2)}, kesinlik {_kor_f(A['kesinlik'], 2)}, özgüllük {_kor_f(A['ozgulluk'], 2)} (insan etiketi doğru kabul).\n",
         f"- Karar kuralı (ön kayıt): BAŞARILI <=> G5 EVET >= 0,70 VE kontrol <= 0,35 VE kappa >= 0,40 VE Fisher p < 0,05; ZAYIF İŞARET <=> G5 EVET >= 0,60 ve "
         "fark > 0; aksi İŞARET YOK.\n\n## BİLGİ\n"]
    S = R["saglama_emin_hayir"]
    L.append(f"- Sağlama (EMİN DEĞİLİM = HAYIR): G5 {_kor_f(S['G5']['oran'], 2)}, kontrol {_kor_f(S['KONTROL']['oran'], 2)}, kappa {_kor_f(S['kappa'], 2)}, Fisher "
             f"{_kor_f(S['fisher_iki_yonlu'], 4)}.\n")
    L.append(f"- BATAN (Tiingo): G5 {_kor_oran(B['BATAN_G5'])}; kontrol {_kor_oran(B['BATAN_KONTROL'])}; Fisher {_kor_f(B['fisher_iki_yonlu'], 3)}.\n")
    T = R["tum_40"]; L.append(f"- 40 grafiğin tümü: algoritma evet {_kor_f(T['ALG']['oran'], 2)}, hayır {_kor_f(T['DEG']['oran'], 2)}, kappa {_kor_f(T['kappa'], 2)}.\n")
    for p, x in R["pazar"].items():
        L.append(f"- {p}: G5 {_kor_f(x['G5']['oran'], 2)} ({x['G5']['evet']} / {x['payda'][0]}), kontrol {_kor_f(x['KONTROL']['oran'], 2)} ({x['KONTROL']['evet']} / "
                 f"{x['payda'][1]}).\n")
    D = R["destek"]
    L.append(f"- Destek sorusu ile G4 (gövde tabanı): {D['n']} cevap, uyum {_kor_f(D['uyum'], 2)}, kappa {_kor_f(D['kappa'], 2)} (insan EVET {D['insan_evet']}, G4 "
             f"doğru {D['g4_dogru']}).\n")
    L.append("\n## Grafik grafik (anahtar artık açık: kor_test_anahtar.json)\n\n| no | grup | pazar | cevap | destek | G4 |\n|---|---|---|---|---|---|\n")
    for r in R["satir"]:
        L.append(f"| {r['no']} | {r['grup']} | {r['pazar']} | {r['bolge']} | {r['destek'] or '-'} | {_kor_f(r['g4'])} |\n")
    return "".join(L)


def kor_rapor(cikti: Optional[str] = None) -> str:
    R = _kor_json_oku(_kor_yol("sonuc", cikti))
    return _kor_yaz(_kor_yol("rapor", cikti), kor_rapor_md(R))


def _cakisma_kontrol_kor(_once=_CK_ONCE_KOR, _dosya="KOR_TEST.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_KOR", "_CK_KAYIT", "_cakisma_kontrol_kor", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "copy", "io", "math", "shutil", "subprocess", "_dt", "annotations",
           "Any", "Callable", "Dict", "List", "Optional", "Tuple", "V1", "V2", "V2B")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_kor()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=KOR_SURUM)
    ap.add_argument("komut", choices=["ohlc", "set", "onkayit", "olc", "rapor"])
    ap.add_argument("--cevap", default=None, help="olc: Cemal'in cevap dosyası")
    ap.add_argument("--cikti", default=None)
    a_ = ap.parse_args()
    try:
        if a_.komut == "ohlc":
            o_ = kor_ohlc(a_.cikti); print(json.dumps(o_["hukum"], ensure_ascii=False, indent=1)); print(_kor_yol("ohlc_md", a_.cikti))
        elif a_.komut == "set":
            z_ = kor_set(a_.cikti)
            print(json.dumps({k: z_[k] for k in ("hedef", "bulunan", "eksik", "aday_sayisi", "anahtar_sha256", "manifest_sha256", "grafik_bayt_maks")},
                             ensure_ascii=False, default=str, indent=1))
        elif a_.komut == "onkayit":
            y_ = kor_onkayit(a_.cikti); print(y_, "mühür", kor_esik_sha(), "kod", kor_kod_sha(), "dosya sha256", kor_sha_dosya(y_))
        elif a_.komut == "olc":
            if not a_.cevap:
                raise KorHata("olc: --cevap DOSYA gerekli")
            r_ = kor_olc(a_.cevap, a_.cikti); print(r_["karar"], "-", r_["kota"]); print(_kor_yol("rapor", a_.cikti))
        else:
            print(kor_rapor(a_.cikti))
    except (KorHata, V2.Vdyt2Hata, V1.VdytHata, FileNotFoundError) as ex:
        korlog.error("%s", ex); sys.exit(1)
