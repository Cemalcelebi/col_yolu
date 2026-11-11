"""K64 + K65 — ÇÖL SİNYALİNE EK BİLGİ: 52 HAFTALIK ZİRVE ailesi (K64) ve ŞİRKET KALİTESİ ailesi (K65); tek dosya
(11 Kasım 2026; ana oturum iş tanımı; ön kayıt arastirma_cikti/col_dis_bilgi/K64_K65_ON_KAYIT.md).

Soru (Cemal): çöl tanımı ve cetvel DEĞİŞMEDEN, yeni değişkenler mevcut çöl sinyaline ek bilgi taşıyor mu?
  Olay      ANA = K24 çöl sinyali (FON_IZI.fi_k24_tara 'kural'; iki pazarda aynı kod). İKİNCİL (sağlamlık) = üretim D13 segmenti + AL kırılımı
            (COL_v1.col_olc + kapanış > tavan x AL_PAY). Aynı hissede 60 işlem gününde tek olay (ilk sinyal).
  K64       Z52 (52 hafta zirvesine uzaklık), D52 (dipten uzaklık), HIZ (zirveye yaklaşma hızı), DUSUS (çöl öncesi düşüş).
  K65       GP, OP, FCF, BORC, SATIS_B, KAR_B, PAY_D; yalnız bilgi tarihi < sinyal günü olan finansal veriyle (ABD: K60 SEC frames + EDGAR
            başvuru günleri; BIST: İş Yatırım mali tablo kalemleri + KAP 'Finansal Rapor' yayın günleri).
  S1        çöl olayları İÇİNDE değişkenin ÜST / ALT üçte biri (aynı gün evren içi yüzdelik sıra) x FI_OLCUT; ÜST - ALT (ay kümeli bootstrap).
  S2        çöl DIŞI evrende aynı günlerde ÜST / ALT üçte birinin 60 günlük eşli farkı (bilgi).
  Cetvel    FON_IZI FI_OLCUT aynen (fi_olcut_panel / olay / hucre); ek: r20, piyasa koşulu, maliyet, Benjamini-Hochberg.
FON_IZI.py, K60.py, COL_v1.py MODÜL olarak içe alınır; DEĞİŞMEZ. SEC'e istek atılmaz. Üretim koduna ekleme yok.

Komut:  python K64.py indir       yalnız VERİ: İş Yatırım mali tablo önbelleği (BIST kalemleri); getiri / ölçüm yok
        python -I K64.py kapsam   yalnız SAYIM (olay, değişken kapsamı, üçte bir grupları); getiri HESAPLANMAZ
        python K64.py onkayit     ön kaydı yazar (ölçümden ÖNCE; mühür + veri sha256 + kapsam; varsa üzerine yazmaz)
        python -I K64.py kos      mühür + veri sha256 + ön kayıt git'e işlenmiş ve değişmemiş -> ölçüm + rapor
        python K64.py rapor       K64_K65_RAPOR.md'yi çıktılardan yeniden yazar
Colab:  exec(open('K64.py').read()); k64_kos()
Veri:   /tmp/veri/V_BIST.pkl, V_ABD.pkl (islenmis-veri dalı), /tmp/k60_* (K60 önbellekleri), /tmp/pead (KAP finansal rapor listeleri),
        /tmp/k64_bist_temel (İş Yatırım). Kişisel e-posta / anahtar yok. Çıktılar arastirma_cikti/col_dis_bilgi/.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K64 = {k: id(v) for k, v in globals().items()}

import contextlib  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K64 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K64 not in sys.path:
    sys.path.insert(0, KOK_K64)

import FON_IZI as FI  # noqa: E402
import K60  # noqa: E402

K57 = K60.K57

k64log = logging.getLogger("col.k64")
if not k64log.handlers:
    _k64_h = logging.StreamHandler(sys.stderr)
    _k64_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k64: %(message)s", "%H:%M:%S"))
    k64log.addHandler(_k64_h)
    k64log.setLevel(logging.INFO)
    k64log.propagate = False

K64_SURUM = "K64 v1.0 (2026-11-11): çöl sinyaline ek bilgi; K64 52 hafta zirvesi ailesi + K65 şirket kalitesi ailesi; S1 çöl içi üçte bir, S2 çöl dışı evren"
K64_YOL = {"cikti": os.path.join(KOK_K64, "arastirma_cikti", "col_dis_bilgi"), "veri": os.environ.get("K64_VERI", "/tmp/veri"),
           "isy": os.environ.get("K64_ISY", "/tmp/k64_bist_temel"), "kap": os.environ.get("K64_KAP", "/tmp/pead"), "ara": os.environ.get("K64_ARA", "/tmp/k64_ara")}
K64_DOSYA = {"onkayit": "K64_K65_ON_KAYIT.md", "kapsam": "kapsam.csv", "kapsam_ozet": "kapsam_ozet.json", "olay": "k64_olaylar.csv.gz", "s1": "k64_s1.csv",
             "fark": "k64_s1_fark.csv", "s2": "k64_s2.csv", "karar": "k64_karar.csv", "meta": "k64_meta.json", "rapor": "K64_K65_RAPOR.md"}
_K64_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")
_K64_ISY_URL = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
_K64_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256'sı ön kayıtta; sonradan değişmez)
# (kod, aile, tanım, kaynak / beklenti). Hepsi yalnız sinyal günü t ve öncesi bilgiyle. C = kapanış (hissenin kendi işlem günleri).
_K64_DEGISKEN: List[Tuple[str, str, str, str]] = [
    ("Z52", "K64", "C(t) / max(C[t-251 .. t]) (son 252 işlem gününün en yüksek KAPANIŞI, t dahil; en az 200 gözlem). 1 = zirvede", "George-Hwang 2004 (zirveye yakın = iyi)"),
    ("D52", "K64", "C(t) / min(C[t-251 .. t]) (son 252 işlem gününün en düşük kapanışı; en az 200 gözlem). 1 = dipte", "proje ölçüsü"),
    ("HIZ", "K64", "Z52(t) - Z52(t-20) (20 işlem gününde zirveye yaklaşma; ikisi de olmalı)", "proje ölçüsü"),
    ("DUSUS", "K64", "çöl başlangıcı b gününde DD252(b) = C(b) / max(C[b-252 .. b-1]) - 1 (önceki 252 günün en yüksek kapanışından çöl başlangıç kapanışına; "
     "en az 200 gözlem). ANA tanımda b = t - 14 işlem günü (K24 1. evresinin ilk barı); İKİNCİL tanımda b = kutu başı (dip günü). Daha eksi = daha derin düşüş",
     "Cemal'in tanımı: çöl düşüş sonrası dipte olur"),
    ("GP", "K65", "brüt kâr son 4 çeyrek / toplam varlık(ç0) (K60 GP_A)", "Novy-Marx 2013"),
    ("OP", "K65", "faaliyet kârı son 4 çeyrek / özkaynak(ç0); özkaynak > 0 (K60 OP_BE)", "Fama-French 2006"),
    ("FCF", "K65", "(işletme nakit akışı - maddi duran varlık yatırımı) / toplam varlık. ABD: son mali yıl y0 / varlık(y0 sonu) (çeyreklik nakit akışı önbellekte yok); "
     "BIST: son 4 çeyrek / varlık(ç0). İki kalem de olmalı", "serbest nakit akışı verimi (varlığa göre)"),
    ("BORC", "K65", "toplam yükümlülük(ç0) / toplam varlık(ç0); yükümlülük = Liabilities, yoksa varlık - özkaynak", "defter kaldıracı (düşük = sağlam)"),
    ("SATIS_B", "K65", "satış(ç0) / satış(ç0-4) - 1; ikisi de > 0 (K60 REV_YOY)", "proje ölçüsü (K59 X1)"),
    ("KAR_B", "K65", "(net kâr son 4 çeyrek(ç0) - net kâr son 4 çeyrek(ç0-4)) / toplam varlık(ç0-4)", "kâr büyümesi (varlığa göre)"),
    ("PAY_D", "K65", "ln(pay(t) / pay(t - 365 gün)); pay bölünme düzeltmeli, iki uç aynı kaynaktan; oran > 5 ya da < 1/5 ise veri yok (K60 NSI_1Y kuralı, günlük)",
     "Pontiff-Woodgate 2008 (ihraç = kötü)"),
]

K64_ESIK: Dict[str, Any] = {
    "kriz": "2026-08-31",
    "donem": [["2017-2021", "2017-01-01", "2021-12-31"], ["2022-2026", "2022-01-01", "2026-12-31"], ["2023-2026", "2023-01-01", "2026-12-31"]],
    "bagimsiz": ["2017-2021", "2022-2026"],
    "pazar": ["BIST", "ABD"], "karar_pazari": "ABD",
    "olay": {"ana": "K24", "ikincil": ["D13"], "tekil_gun": 60, "k24_bas_geri": 14,
             "d13": {"etkin": True, "tespit": "hafta_sonu", "min_bar": 300, "kirilim_gun": 60, "gecer": True, "isci": 4}},
    "k64": {"pencere": 252, "min_gozlem": 200, "hiz_gun": 20},
    "k65": {"parca_gun": 250, "pay_gun": 365, "pay_aykiri": 5.0, "fcf": {"ABD": "yillik", "BIST": "ttm"}, "pay": {"ABD": True, "BIST": False}},
    "bist": {"yil_bas": 2014, "yil_son": 2026, "grup": "XI_29", "yedek_ara_gun": 75, "yedek_yil_gun": 100, "kap_min_gun": 5, "isci": 10, "bekle": 0.15,
             "kalem": {"Assets": "1BL", "StockholdersEquity": "2N", "Revenues": "3C", "GrossProfit": "3D", "OperatingIncomeLoss": "3DF", "NetIncomeLoss": "3L",
                       "NetCashProvidedByUsedInOperatingActivities": "4C", "PaymentsToAcquirePropertyPlantAndEquipment": "4CAI"},
             "anlik": ["Assets", "StockholdersEquity"], "eksi": ["PaymentsToAcquirePropertyPlantAndEquipment"]},
    "sira": {"ust": 2.0 / 3.0, "alt": 1.0 / 3.0, "min_evren": 30, "ic_gun": 365, "ic_min": 30, "karar": {"K64": "IC", "K65": "EVREN"}},
    "s1": {"n_esik": 30, "bootstrap": 2000, "tohum": 64001, "guven": [2.5, 97.5], "gecerli_pay": 0.90},
    "s2": {"bootstrap": 2000, "tohum": 64002},
    "ek_ufuk": 20, "piyasa": {"sma": 200, "min_hisse": 30},
    "maliyet": {"BIST": 0.0060, "ABD": 0.0020},
    "coklu": {"bh_q": 0.10},
    "degisken": [{"kod": k, "aile": a, "tanim": t, "kaynak": ky} for k, a, t, ky in _K64_DEGISKEN],
}


class K64Hata(RuntimeError):
    """K64'e özgü durdurucu hata (ön kayıt yok / değişmiş / git'e işlenmemiş, veri eksik ya da farklı, çıktı yok)."""


def _k64_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K64_YOL["cikti"], K64_DOSYA.get(ad, ad))


def _k64_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _k64_colv1() -> Any:
    """COL_v1 modülü (üretim; DEĞİŞMEZ). İçe alınırken bastığı satır yutulur."""
    if "COL_v1" in sys.modules:
        return sys.modules["COL_v1"]
    with contextlib.redirect_stdout(io.StringIO()):
        import COL_v1
    return COL_v1


def k64_kodlar(E: Optional[Dict[str, Any]] = None, aile: Optional[str] = None) -> List[str]:
    return [d["kod"] for d in (E or K64_ESIK)["degisken"] if aile is None or d["aile"] == aile]


def k64_karar_sirasi(kod: str, E: Optional[Dict[str, Any]] = None) -> str:
    """Değişkenin KARAR sırası türü (aile bazında; ön kayıt §4): K64 ailesi 'IC' (çöl içi sıra), K65 ailesi 'EVREN' (aynı gün evren içi sıra). Öteki sıra türü
    o değişken için 'sağlamlık, karar dışı'dır. Tanımsız kod ya da aile durdurur."""
    E = E or K64_ESIK
    for d in E["degisken"]:
        if d["kod"] == kod:
            st = E["sira"]["karar"].get(d["aile"])
            if st not in ("EVREN", "IC"):
                raise K64Hata(f"{kod}: '{d['aile']}' ailesinin karar sırası tanımlı değil")
            return st
    raise K64Hata(f"karar sırası sorulan değişken tanımlı değil: {kod}")


def _k64_bagimli() -> Dict[str, Any]:
    """Mühre giren dış tanımlar: K24 çöl kuralı, FI_OLCUT, K60 bilgi tarihi kuralı + K60 mührü, üretim D13 / AL sabitleri."""
    CV = _k64_colv1()
    d13 = {k: getattr(CV, k) for k in ("SEGMENT_MOD", "D13_N", "D13_KENAR", "D13_BAR", "D13_INIS", "D13_KONUM", "D13_RETEST", "D13_YUV", "D13_KUCUK", "D13_OBEK",
                                        "D13_OBEK_YUK", "MIN_UZ", "MAX_YUK", "AL_PAY", "E_CLV", "E_BS", "E_OU", "BIST_MODU")}
    return {"FI_K24": FI.FI_K24, "FI_OLCUT": FI.FI_OLCUT, "K60_bilgi": K60.K60_ESIK["bilgi"], "K60_muhur": K60.k60_esik_sha(), "K57_ABD_GELIR": list(K57.K57_ABD_GELIR),
            "COL_v1": d13}


def k64_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: K64_ESIK (değişken tanımları dahil) + dış tanımlar; biri değişirse koşu durur."""
    s = json.dumps({"K64_ESIK": E or K64_ESIK, "bagimli": _k64_bagimli()}, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- 1) VERİ (yalnız önbellek; ağ yalnız `indir` komutunda, yalnız İş Yatırım)
def k64_fiyat_yukle(pazar: str, klasor: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, pd.DataFrame]:
    """V_<pazar>.pkl (fi_k1_veri çıktısı) -> {sembol: OHLCV}; fon krizi kesiği (kriz sonrası barlar atılır); en az 150 bar."""
    E = E or K64_ESIK; yol = os.path.join(klasor or K64_YOL["veri"], f"V_{pazar}.pkl")
    if not os.path.exists(yol):
        raise K64Hata(f"fiyat verisi yok: {yol} (islenmis-veri dalı: python FON_IZI.py vpac /tmp/iv/veri /tmp/veri)")
    with open(yol, "rb") as f:
        V = pickle.load(f)
    if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
        V = V["veri"]
    kriz = pd.Timestamp(E["kriz"]); out: Dict[str, pd.DataFrame] = {}
    for s, d in V.items():
        try:
            d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float)
            d = d[d.index <= kriz]
            d = d[~d.index.duplicated(keep="last")].sort_index()
            if len(d) >= 150:
                out[str(s)] = d
        except Exception as ex:   # tek hisse bozuksa ötekiler sürer
            k64log.warning("%s %s atlandı: %s", pazar, s, ex)
    if not out:
        raise K64Hata(f"{yol}: yüklenebilen hisse yok")
    return out


def _k64_isy_getir(sembol: str, yil: int, grup: str) -> bytes:
    """İş Yatırım mali tablo servisi: bir hissenin bir yılının 12 / 9 / 6 / 3 aylık dönemleri (ham JSON). Kimlik / anahtar gerekmez."""
    import ssl
    import urllib.parse
    import urllib.request
    q: Dict[str, Any] = {"companyCode": sembol, "exchange": "TRY", "financialGroup": grup}
    for i, p in enumerate((12, 9, 6, 3), 1):
        q[f"year{i}"] = yil; q[f"period{i}"] = p
    ca = os.environ.get("K64_CA", "/root/.ccr/ca-bundle.crt")
    ctx = ssl.create_default_context(cafile=ca if os.path.exists(ca) else None)
    r = urllib.request.Request(_K64_ISY_URL + "?" + urllib.parse.urlencode(q), headers={"User-Agent": _K64_UA, "Accept": "application/json"})
    with urllib.request.urlopen(r, timeout=40, context=ctx) as f:
        return f.read()


def k64_isy_indir(semboller: List[str], klasor: Optional[str] = None, getir: Optional[Callable[[str, int, str], bytes]] = None,
                  E: Optional[Dict[str, Any]] = None) -> Dict[str, int]:
    """İş Yatırım önbelleği: <klasor>/<SEMBOL>_<YIL>.json (ham yanıt). Var olan dosya yeniden indirilmez. Yalnız veri; ölçüm yok."""
    from concurrent.futures import ThreadPoolExecutor
    E = E or K64_ESIK; B = E["bist"]; kl = klasor or K64_YOL["isy"]; os.makedirs(kl, exist_ok=True); getir = getir or _k64_isy_getir

    def tek(a: Tuple[str, int]) -> int:
        s, y = a; yol = os.path.join(kl, f"{s}_{y}.json")
        if os.path.exists(yol):
            return 0
        son: Optional[Exception] = None
        for k in range(4):
            try:
                ham = getir(s, y, B["grup"]); J = json.loads(ham)
                if not isinstance(J, dict) or "value" not in J:
                    raise ValueError("beklenmeyen yanıt biçimi")
                with open(yol + ".yarim", "wb") as f:
                    f.write(ham)
                os.replace(yol + ".yarim", yol); time.sleep(B["bekle"])
                return 1
            except Exception as ex:   # ağ / biçim hatası: yeniden dene, sonra kaydet ve sür
                son = ex; time.sleep(2 * (k + 1))
        k64log.warning("İş Yatırım %s %s indirilemedi: %s", s, y, son)
        return -1
    isler = [(s, y) for s in semboller for y in range(B["yil_bas"], B["yil_son"] + 1)]
    with ThreadPoolExecutor(int(B["isci"])) as ex:
        sonuc = list(ex.map(tek, isler))
    out = {"is": len(isler), "yeni": sum(x == 1 for x in sonuc), "vardi": sum(x == 0 for x in sonuc), "hata": sum(x == -1 for x in sonuc)}
    k64log.info("İş Yatırım önbelleği: %s", out)
    return out


def _k64_sayi(x: Any) -> float:
    try:
        return float(x) if x is not None else np.nan
    except (TypeError, ValueError):
        return np.nan


def k64_isy_oku(semboller: List[str], klasor: Optional[str] = None, E: Optional[Dict[str, Any]] = None, eksik_dur: bool = True) -> Tuple[Dict[str, Dict[Tuple[int, int], Dict[str, float]]], Dict[str, Any]]:
    """Önbellekten {sembol: {(yıl, ay): {kalem: KÜMÜLATİF / anlık değer}}}; yalnız toplam varlığı > 0 olan dönemler. Döner (tablo, özet: dosya,
    eksik dosya, boş hisse (mali sektör şablonu farklı / veri yok), içerik sha256)."""
    E = E or K64_ESIK; B = E["bist"]; kl = klasor or K64_YOL["isy"]; out: Dict[str, Dict[Tuple[int, int], Dict[str, float]]] = {}
    h = hashlib.sha256(); eksik: List[str] = []; dosya = 0
    for s in semboller:
        out[s] = {}
        for y in range(B["yil_bas"], B["yil_son"] + 1):
            yol = os.path.join(kl, f"{s}_{y}.json")
            if not os.path.exists(yol):
                eksik.append(f"{s}_{y}"); continue
            try:
                with open(yol, encoding="utf-8") as f:
                    J = json.load(f)
            except (OSError, ValueError) as ex:
                raise K64Hata(f"İş Yatırım önbellek dosyası okunamadı: {yol} ({type(ex).__name__})")
            dosya += 1; d = {str(r.get("itemCode")): r for r in (J.get("value") or []) if isinstance(r, dict)}
            oz = {t: [d[k].get(f"value{i}") if k in d else None for i in range(1, 5)] for t, k in B["kalem"].items()}
            h.update(f"{s}_{y}:".encode()); h.update(json.dumps(oz, sort_keys=True).encode())
            for i, p in enumerate((12, 9, 6, 3)):
                v = {t: _k64_sayi(oz[t][i]) for t in B["kalem"]}
                if np.isfinite(v["Assets"]) and v["Assets"] > 0:
                    for t in B["eksi"]:
                        v[t] = -v[t]
                    if not (np.isfinite(v["Revenues"]) and v["Revenues"] != 0):       # satış geliri 0 / yok: satış ve brüt kâr kalemi YOK sayılır
                        v["Revenues"] = np.nan; v["GrossProfit"] = np.nan
                    out[s][(y, p)] = v
    if eksik and eksik_dur:
        raise K64Hata(f"İş Yatırım önbelleği eksik: {len(eksik)} dosya (ör. {eksik[:3]}); önce `python K64.py indir`")
    return out, {"dosya": dosya, "eksik": len(eksik), "bos_hisse": sorted(s for s in semboller if not out[s]), "icerik_sha256": h.hexdigest()}


def k64_kap_bilgi(yollar: Optional[List[str]] = None) -> Dict[Tuple[str, int, int], np.datetime64]:
    """KAP 'Finansal Rapor' listeleri (fi_k28_liste_bist çıktıları) -> {(kod, yıl, dönem 1-4): İLK yayın günü}. Birden çok kodlu satır her koda yazılır."""
    yollar = yollar or [os.path.join(K64_YOL["kap"], a) for a in ("liste_bist_2016_22.csv.gz", "liste_bist.csv.gz")]
    par = []
    for y in yollar:
        if not os.path.exists(y):
            raise K64Hata(f"KAP finansal rapor listesi yok: {y} (FON_IZI fi_k28_liste_bist çıktısı)")
        par.append(pd.read_csv(y, dtype=str))
    L = pd.concat(par, ignore_index=True)
    L["g"] = pd.to_datetime(L.yayin, format="%d.%m.%Y %H:%M:%S", errors="coerce").dt.normalize()
    L["y"] = pd.to_numeric(L.yil, errors="coerce"); L["p"] = pd.to_numeric(L.donem, errors="coerce")
    L = L.dropna(subset=["g", "y", "p", "kod"])
    out: Dict[Tuple[str, int, int], np.datetime64] = {}
    for kodlar, y, p, g in zip(L.kod, L.y.astype(int), L.p.astype(int), L.g.to_numpy("datetime64[D]")):
        for k in str(kodlar).split(","):
            a = (k.strip(), int(y), int(p))
            if a[0] and (a not in out or g < out[a]):
                out[a] = g
    return out


def k64_bist_temel(semboller: List[str], ham: Dict[str, Dict[Tuple[int, int], Dict[str, float]]], kap: Dict[Tuple[str, int, int], np.datetime64],
                   E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """BIST temel tablosu, K60 temel tablo BİÇİMİNDE (K60._K60Temel ile okunur): Q (çeyreklik akış = kümülatif farkı), I (çeyrek sonu anlık), Y (yıllık =
    12 aylık kümülatif), bit / bilgi (çeyrek sonu / BİLGİ TARİHİ = KAP ilk yayın günü; yoksa ya da dönem sonuna kap_min_gun'den yakınsa YEDEK: ara dönem +
    yedek_ara_gun, yıl sonu + yedek_yil_gun), Ybit / Ybilgi / Yq. bilgi_kaynak: 1 KAP, 2 yedek."""
    E = E or K64_ESIK; B = E["bist"]; yb, ys = int(B["yil_bas"]), int(B["yil_son"]); ny = ys - yb + 1; nq = ny * 4; N = len(semboller); nat = np.datetime64("NaT", "D")
    akis = [t for t in B["kalem"] if t not in B["anlik"]]
    T: Dict[str, Any] = {"q_bas": yb * 4, "y_bas": yb, "Q": {t: np.full((nq, N), np.nan) for t in akis}, "I": {t: np.full((nq, N), np.nan) for t in B["anlik"]},
                         "Y": {t: np.full((ny, N), np.nan) for t in akis}, "bit": np.full((nq, N), nat), "bilgi": np.full((nq, N), nat), "Ybit": np.full((ny, N), nat),
                         "Ybas": np.full((ny, N), nat), "Ybilgi": np.full((ny, N), nat), "Yq": np.full((ny, N), -1), "bilgi_kaynak": np.zeros((nq, N), np.int8), "pay": [None] * N}
    gD = lambda n: np.timedelta64(int(n), "D")  # noqa: E731
    for j, s in enumerate(semboller):
        for (y, p), v in (ham.get(s) or {}).items():
            if not (yb <= y <= ys) or p not in (3, 6, 9, 12):
                continue
            q = (y - yb) * 4 + p // 3 - 1
            b = (pd.Timestamp(year=y, month=p, day=1) + pd.offsets.MonthEnd(0)).to_datetime64().astype("datetime64[D]")
            T["bit"][q, j] = b
            for t in B["anlik"]:
                T["I"][t][q, j] = v.get(t, np.nan)
            once = ham[s].get((y, p - 3)) if p > 3 else {}
            for t in akis:
                x = v.get(t, np.nan); o = 0.0 if p == 3 else (once.get(t, np.nan) if once is not None else np.nan)
                if np.isfinite(x) and np.isfinite(o):
                    T["Q"][t][q, j] = x - o
                if p == 12:
                    T["Y"][t][y - yb, j] = x
            k = kap.get((s, y, p // 3)); yedek = b + gD(B["yedek_yil_gun"] if p == 12 else B["yedek_ara_gun"])
            if k is not None and k >= b + gD(B["kap_min_gun"]):
                T["bilgi"][q, j] = k; T["bilgi_kaynak"][q, j] = 1
            else:
                T["bilgi"][q, j] = yedek; T["bilgi_kaynak"][q, j] = 2
            if p == 12:
                T["Ybit"][y - yb, j] = b; T["Ybas"][y - yb, j] = np.datetime64(f"{y}-01-01"); T["Ybilgi"][y - yb, j] = T["bilgi"][q, j]; T["Yq"][y - yb, j] = q
    return T


def k64_abd_temel(semboller: List[str], D: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any], np.ndarray]:
    """K60 demetinin temel tablosundan verilen sembollerin sütunları (aynı biçim). Döner (T, bölünmeler, eşleşen maske). Demette olmayan sembol: NaN / NaT."""
    ix = {s: j for j, s in enumerate(D["sembol"])}; col = np.array([ix.get(s, -1) for s in semboller], int); var = col >= 0; c = np.maximum(col, 0); T0 = D["temel"]

    def al(X: np.ndarray, bos: Any) -> np.ndarray:
        Y = np.array(X[:, c], copy=True); Y[:, ~var] = bos
        return Y
    nat = np.datetime64("NaT", "D")
    T: Dict[str, Any] = {"q_bas": T0["q_bas"], "y_bas": T0["y_bas"], "Q": {k: al(v, np.nan) for k, v in T0["Q"].items()}, "I": {k: al(v, np.nan) for k, v in T0["I"].items()},
                         "Y": {k: al(v, np.nan) for k, v in T0["Y"].items()}, "bit": al(T0["bit"], nat), "bilgi": al(T0["bilgi"], nat), "Ybit": al(T0["Ybit"], nat),
                         "Ybas": al(T0["Ybas"], nat), "Ybilgi": al(T0["Ybilgi"], nat), "Yq": al(T0["Yq"], -1),
                         "bilgi_kaynak": al(T0["bilgi_kaynak"], 0) if "bilgi_kaynak" in T0 else np.zeros((T0["bilgi"].shape[0], len(semboller)), np.int8),
                         "pay": [T0["pay"][c[i]] if var[i] and T0.get("pay") is not None else None for i in range(len(semboller))]}
    bol = {s: D["bolunme"][s] for s in semboller if s in (D.get("bolunme") or {})}
    return T, bol, var


def k64_veri_sha(isy_ozet: Optional[Dict[str, Any]] = None) -> Dict[str, Tuple[str, int]]:
    """Koşunun okuyacağı verinin ve içe alınan kodun sha256'ları: ad -> (sha256, dosya sayısı). Eksik dosyada durur. K60 önbellekleri K60 ön kaydıyla
    doğrulanır (K60.k60_onkayit_dogrula veri=True; `kos` başında)."""
    sha = K60._k60_sha; out: Dict[str, Tuple[str, int]] = {}
    for p in K64_ESIK["pazar"]:
        y = os.path.join(K64_YOL["veri"], f"V_{p}.pkl")
        if not os.path.exists(y):
            raise K64Hata(f"fiyat verisi yok: {y}")
        out[f"V_{p}.pkl"] = (sha(y), 1)
    for a in ("liste_bist_2016_22.csv.gz", "liste_bist.csv.gz"):
        y = os.path.join(K64_YOL["kap"], a)
        if not os.path.exists(y):
            raise K64Hata(f"KAP finansal rapor listesi yok: {y}")
        out[a] = (sha(y), 1)
    if isy_ozet is None:
        _h, isy_ozet = k64_isy_oku(sorted(k64_fiyat_yukle("BIST")))
    out["k64_bist_temel"] = (isy_ozet["icerik_sha256"], int(isy_ozet["dosya"]))
    k60 = K60._k60_yol("onkayit")
    if not os.path.exists(k60):
        raise K64Hata(f"K60 ön kaydı yok: {k60}")
    out["K60_ON_KAYIT.md"] = (sha(k60), 1)
    for a in ("FON_IZI.py", "K60.py", "COL_v1.py"):
        y = os.path.join(KOK_K64, a)
        if not os.path.exists(y):
            raise K64Hata(f"içe alınan kod dosyası yok: {y}")
        out[a] = (sha(y), 1)
    return out


# ---------------------------------------------------------------- 2) OLAYLAR (çöl tanımları DEĞİŞMEDEN; yalnız t ve öncesi bilgi)
def k64_tekil(pos: np.ndarray, ayri: int) -> np.ndarray:
    """Sıralı bar konumları -> tutulanlar (bool): son TUTULAN sinyalden en az `ayri` işlem günü sonra gelen ilk sinyal tutulur."""
    out = np.zeros(len(pos), bool); son = -10 ** 9
    for i, p in enumerate(pos):
        if p - son >= ayri:
            out[i] = True; son = int(p)
    return out


def k64_olay_k24(V: Dict[str, pd.DataFrame], E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """ANA olay: K24 çöl sinyali (FON_IZI.fi_k24_tara 'kural' günleri; FI_K24 eşikleri aynen). Sütunlar: sembol, sinyal, bas (t - k24_bas_geri bar), giris
    (hissenin sinyalden sonraki ilk işlem günü; yoksa NaT), tekil (60 işlem günü kuralı; ilk sinyal). fi_k24_tara'nın ileriye bakan sonuç sütunları
    (yon60, yon20, r120) ALINMAZ. Tekil olaylar FI_K24 'tekrar' = 60 çıktısıyla birebir olmalıdır (denetim; sapma loglanır)."""
    E = E or K64_ESIK; O = E["olay"]; sat = []; sapma = 0
    for s in sorted(V):
        d = V[s]
        try:
            X = FI.fi_k24_tara(d, {**FI.FI_K24, "tekrar": 0})
            if not len(X) or "kural" not in X:
                continue
            gun = pd.DatetimeIndex(X.loc[X.kural, "tarih"])
            if not len(gun):
                continue
            pos = np.sort(d.index.get_indexer(gun)); tut = k64_tekil(pos, O["tekil_gun"])
            Y = FI.fi_k24_tara(d)
            asil = set(pd.DatetimeIndex(Y.loc[Y.kural, "tarih"])) if len(Y) and "kural" in Y else set()
            if asil != set(d.index[pos[tut]]):
                sapma += 1
            for p, t in zip(pos, tut):
                sat.append({"sembol": s, "sinyal": d.index[p], "bas": d.index[p - O["k24_bas_geri"]] if p >= O["k24_bas_geri"] else pd.NaT,
                            "giris": d.index[p + 1] if p + 1 < len(d) else pd.NaT, "tekil": bool(t)})
        except Exception as ex:   # tek hisse bozuksa ötekiler sürer
            k64log.warning("K24 %s atlandı: %s", s, ex)
    if sapma:
        k64log.warning("K24: %d hissede tekil olaylar FI_K24 tekrar = 60 çıktısından farklı", sapma)
    X = pd.DataFrame(sat, columns=["sembol", "sinyal", "bas", "giris", "tekil"])
    X.attrs["sapma"] = sapma
    return X


def _k64_d13_hisse(arg: Tuple[str, pd.DataFrame, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Bir hissede üretim D13 çölü + AL kırılımı. Tespit günleri = her haftanın son işlem günü e (yalnız <= e barları, COL_v1.col_olc); kırılım = e'den
    sonraki kirilim_gun bar içinde, kapanış tabanın altına inmeden önce, ilk kapanış > tavan x AL_PAY (COL_v1.tara kuralı). Olay günü = kırılım günü."""
    s, d, O = arg
    CV = _k64_colv1(); n = len(d); C = d.Close.to_numpy(float); hf = d.index.to_period("W"); son = np.flatnonzero(np.r_[np.asarray(hf[1:] != hf[:-1]), True])
    out: Dict[int, Dict[str, Any]] = {}
    for e in son:
        if e + 1 < O["min_bar"] or e + 1 >= n:
            continue
        try:
            o = CV.col_olc(d.iloc[:e + 1])
        except Exception:   # üretim kodu bu barda ölçemedi: tespit yok
            o = None
        if not o or not np.isfinite(o.get("tavan", np.nan)) or not np.isfinite(o.get("taban", np.nan)):
            continue
        for j in range(e + 1, min(e + O["kirilim_gun"], n - 1) + 1):
            if C[j] > o["tavan"] * CV.AL_PAY:
                r = out.setdefault(j, {"tespit": int(e), "bas": pd.Timestamp(o["bas_tarih"]), "gecer": False, "bas_gecer": pd.NaT})
                if bool(o["GECER"]) and not r["gecer"]:
                    r["gecer"] = True; r["bas_gecer"] = pd.Timestamp(o["bas_tarih"])
                break
            if C[j] < o["taban"]:
                break
    return [{"sembol": s, "sinyal": d.index[j], "pos": int(j), "bas": r["bas_gecer"] if r["gecer"] else r["bas"], "giris": d.index[j + 1] if j + 1 < n else pd.NaT,
             "gecer": r["gecer"]} for j, r in sorted(out.items())]


def k64_olay_d13(V: Dict[str, pd.DataFrame], E: Optional[Dict[str, Any]] = None, isci: Optional[int] = None, onbellek: Optional[str] = None) -> pd.DataFrame:
    """İKİNCİL olay: üretim D13 + AL kırılımı (bütün hisseler). 'gecer' = kırılımdan önce üretim kuralını (clv / bant / orta-üst) geçen tespit var.
    'tekil' = tanımdaki olaylar (gecer şartı açıksa yalnız gecer) içinde 60 işlem günü kuralı. onbellek: ara sonuç dosyası (aynı girdi -> yeniden taranmaz)."""
    E = E or K64_ESIK; O = E["olay"]["d13"]; isci = int(O["isci"] if isci is None else isci)
    if onbellek and os.path.exists(onbellek):
        try:
            return pd.read_pickle(onbellek)
        except Exception as ex:   # bozuk ara önbellek: yeniden taranır
            k64log.warning("D13 ara önbelleği okunamadı (%s): yeniden taranıyor", ex)
    isler = [(s, V[s], O) for s in sorted(V)]
    if isci > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(isci) as havuz:
            par = havuz.map(_k64_d13_hisse, isler, chunksize=8)
    else:
        par = [_k64_d13_hisse(a) for a in isler]
    X = pd.DataFrame([r for p in par for r in p], columns=["sembol", "sinyal", "pos", "bas", "giris", "gecer"])
    X["tekil"] = False
    for s, g in X.groupby("sembol", sort=False):
        g = g[g.gecer] if O["gecer"] else g
        if len(g):
            X.loc[g.index[k64_tekil(g.pos.to_numpy(), E["olay"]["tekil_gun"])], "tekil"] = True
    X = X.drop(columns=["pos"])
    if onbellek:
        os.makedirs(os.path.dirname(onbellek), exist_ok=True); X.to_pickle(onbellek)
    return X


# ---------------------------------------------------------------- 3) DEĞİŞKENLER (gün x hisse matrisleri; yalnız o gün ve öncesi bilgi)
def k64_fiyat_olculeri(c: np.ndarray, E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """Bir hissenin kendi işlem günlerinde K64 ölçüleri: Z52, D52, HIZ, DD252 (çöl başlangıcında okunur) ve DUSUS (= DD252'nin k24_bas_geri bar önceki değeri)."""
    E = E or K64_ESIK; K = E["k64"]; cs = pd.Series(np.asarray(c, float)); W, mn = int(K["pencere"]), int(K["min_gozlem"])
    tepe = cs.rolling(W, min_periods=mn).max(); dip = cs.rolling(W, min_periods=mn).min()
    z = cs / tepe; dd = cs / cs.shift(1).rolling(W, min_periods=mn).max() - 1
    return {"Z52": z.to_numpy(), "D52": (cs / dip).to_numpy(), "HIZ": (z - z.shift(int(K["hiz_gun"]))).to_numpy(), "DD252": dd.to_numpy(),
            "DUSUS": dd.shift(int(E["olay"]["k24_bas_geri"])).to_numpy()}


def k64_takvim(V: Dict[str, pd.DataFrame]) -> Tuple[pd.DatetimeIndex, List[str]]:
    """FI_OLCUT paneliyle aynı takvim ve sembol sırası (birleşik işlem günleri; sıralı semboller)."""
    S = sorted(V)
    return pd.DatetimeIndex(sorted(set().union(*[V[s].index for s in S]))), S


def k64_fiyat_matrisleri(V: Dict[str, pd.DataFrame], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """K64 ölçü matrisleri (takvim x hisse; hissenin işlem görmediği gün NaN), 'var' (o gün kapanışı var), kapanış matrisi."""
    tak, S = k64_takvim(V); G, N = len(tak), len(S); ad = ("Z52", "D52", "HIZ", "DD252", "DUSUS")
    M: Dict[str, Any] = {k: np.full((G, N), np.nan, np.float32) for k in ad}; C = np.full((G, N), np.nan); tv = tak.to_numpy("datetime64[ns]")
    for j, s in enumerate(S):
        d = V[s]; p = np.searchsorted(tv, d.index.to_numpy("datetime64[ns]")); c = d.Close.to_numpy(float); X = k64_fiyat_olculeri(c, E)
        C[p, j] = c
        for k in ad:
            M[k][p, j] = X[k]
    M.update({"takvim": tak, "sembol": S, "C": C, "var": np.isfinite(C)})
    return M


def k64_kalite(T: Optional[Dict[str, Any]], gunD: np.ndarray, N: int, pazar: str, pay: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """K65 ölçü matrisleri (gün x hisse): her gün t için yalnız BİLGİ TARİHİ < t olan dönemler (K60._K60Temel; ç0 = bilgi tarihi < t olan en son çeyrek,
    çeyrek sonu en çok 200 gün önce; y0 = en son mali yıl). pay = {'bolunme': ..., 'sembol': ...} verilirse PAY_D (K60.k60_pay, t ve t - pay_gun)."""
    E = E or K64_ESIK; K = E["k65"]; Bg = K60.K60_ESIK["bilgi"]; G = len(gunD); kod = k64_kodlar(E, "K65"); out = {k: np.full((G, N), np.nan, np.float32) for k in kod}
    if T is None:
        return out
    bol, ilk = K60._k60_bol, K60._k60_ilk; GEL = list(K57.K57_ABD_GELIR); OCF, CAP = "NetCashProvidedByUsedInOperatingActivities", "PaymentsToAcquirePropertyPlantAndEquipment"
    for a in range(0, G, int(K["parca_gun"])):
        g = np.asarray(gunD[a:a + int(K["parca_gun"])], "datetime64[D]"); M = len(g); AO = K60._K60Temel(T, g, N, Bg); sl = slice(a, a + M)

        def gel(f: Callable[[str], np.ndarray]) -> np.ndarray:
            return ilk(*[f(t) for t in GEL])

        def AT(q: int = 0) -> np.ndarray:
            return ilk(AO.i("Assets", q), AO.i("LiabilitiesAndStockholdersEquity", q))
        with np.errstate(invalid="ignore", divide="ignore"):
            EQ = AO.i("StockholdersEquity", 0); LT = ilk(AO.i("Liabilities", 0), AT(0) - EQ)
            gp4 = ilk(AO.ttm("GrossProfit"), gel(lambda t: AO.ttm(t)) - ilk(AO.ttm("CostOfRevenue"), AO.ttm("CostOfGoodsAndServicesSold")))
            out["GP"][sl] = bol(gp4, AT(0), True); out["OP"][sl] = bol(AO.ttm("OperatingIncomeLoss"), EQ, True)
            if K["fcf"][pazar] == "yillik":
                ATy = ilk(AO.ya("Assets", 0), AO.ya("LiabilitiesAndStockholdersEquity", 0)); out["FCF"][sl] = bol(AO.y(OCF, 0) - AO.y(CAP, 0), ATy, True)
            else:
                out["FCF"][sl] = bol(AO.ttm(OCF) - AO.ttm(CAP), AT(0), True)
            out["BORC"][sl] = bol(LT, AT(0), True)
            out["SATIS_B"][sl] = gel(lambda t: np.where(AO.q(t, 0) > 0, bol(AO.q(t, 0), AO.q(t, 4), True) - 1.0, np.nan))
            out["KAR_B"][sl] = bol(AO.ttm("NetIncomeLoss", 0) - AO.ttm("NetIncomeLoss", 4), AT(4), True)
            if pay is not None and K["pay"][pazar]:
                Dl = {"temel": T, "bolunme": pay.get("bolunme") or {}}; U0 = np.zeros((M, N), bool); g0 = g - np.timedelta64(int(K["pay_gun"]), "D")
                s1, k1 = K60.k60_pay(Dl, {"U": U0, "mtD": g, "sembol": pay["sembol"]}, AO, K60.K60_ESIK)
                s0, k0 = K60.k60_pay(Dl, {"U": U0, "mtD": g0, "sembol": pay["sembol"]}, K60._K60Temel(T, g0, N, Bg), K60.K60_ESIK)
                o = bol(s1, s0, True); ok = np.isfinite(o) & (o > 0) & (o <= K["pay_aykiri"]) & (o >= 1.0 / K["pay_aykiri"]) & (k1 == k0) & (k1 > 0)
                out["PAY_D"][sl] = np.where(ok, np.log(np.where(ok, o, 1.0)), np.nan)
    return out


def k64_sira(X: np.ndarray, var: np.ndarray, min_evren: int) -> np.ndarray:
    """Evren içi yüzdelik sıra (gün x hisse): o gün işlem gören ve ölçüsü olan hisseler içinde (küçük olan sayısı + 0,5 x eşit olan sayısı, kendisi dahil) / n.
    n < min_evren olan gün NaN."""
    Y = np.where(var & np.isfinite(X), X, np.nan).astype(float); n = np.isfinite(Y).sum(axis=1)
    R = pd.DataFrame(Y).rank(axis=1, method="average").to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        S = (R - 0.5) / np.maximum(n, 1)[:, None]
    S[n < int(min_evren)] = np.nan
    return S


def k64_ic_sira(gun: np.ndarray, x: np.ndarray, pencere_gun: int, min_n: int) -> np.ndarray:
    """ÇÖL İÇİ sıra (geleceğe bakmaz): olayın değeri, sinyal günü [t - pencere_gun, t] aralığındaki (kendisi ve aynı günküler dahil) çöl olaylarının
    değerleri içinde (küçük + 0,5 x eşit) / n; n < min_n ise NaN. gun: datetime64[D], x: değerler (aynı sırada)."""
    gun = np.asarray(gun, "datetime64[D]"); x = np.asarray(x, float); out = np.full(len(x), np.nan); s = np.argsort(gun, kind="stable"); gs, xs = gun[s], x[s]
    for i in range(len(xs)):
        if not np.isfinite(xs[i]):
            continue
        a = np.searchsorted(gs, gs[i] - np.timedelta64(int(pencere_gun), "D"), side="left"); b = np.searchsorted(gs, gs[i], side="right")
        w = xs[a:b]; w = w[np.isfinite(w)]
        if len(w) >= int(min_n):
            out[s[i]] = ((w < xs[i]).sum() + 0.5 * (w == xs[i]).sum()) / len(w)
    return out


def k64_grup(sira: Any, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Sıra -> 'UST' (>= 2/3), 'ALT' (<= 1/3), 'ORTA', '' (sıra yok)."""
    S = (E or K64_ESIK)["sira"]; s = np.asarray(sira, float)
    with np.errstate(invalid="ignore"):
        return np.where(~np.isfinite(s), "", np.where(s >= S["ust"], "UST", np.where(s <= S["alt"], "ALT", "ORTA")))


def k64_pazar_hazirla(pazar: str, V: Dict[str, pd.DataFrame], T: Optional[Dict[str, Any]], pay: Optional[Dict[str, Any]] = None,
                      E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Bir pazarın değişken matrisleri (K64 + K65), evren içi sıraları ve piyasa koşulu serisi. Getiri HESAPLANMAZ."""
    E = E or K64_ESIK; M = k64_fiyat_matrisleri(V, E); tak = M["takvim"]; N = len(M["sembol"])
    Kl = k64_kalite(T, tak.to_numpy("datetime64[D]"), N, pazar, pay, E)
    X = {k: M[k] for k in ("Z52", "D52", "HIZ", "DUSUS")}; X.update(Kl)
    sira = {k: k64_sira(v, M["var"], E["sira"]["min_evren"]) for k, v in X.items()}
    sira["DD252"] = k64_sira(M["DD252"], M["var"], E["sira"]["min_evren"])
    return {"takvim": tak, "sembol": M["sembol"], "kol": {s: j for j, s in enumerate(M["sembol"])}, "X": {**X, "DD252": M["DD252"]}, "sira": sira, "var": M["var"],
            "rejim": k64_rejim(M["C"], E)}


def k64_rejim(C: np.ndarray, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Piyasa koşulu (gün): eşit ağırlıklı evren endeksi (günlük kapanış getirilerinin ortalaması; en az min_hisse) sma günlük ortalamasının üstünde 1, değilse
    0; ortalama yoksa NaN. Yalnız o gün ve öncesi."""
    P = (E or K64_ESIK)["piyasa"]
    with np.errstate(invalid="ignore", divide="ignore"):
        r = C[1:] / C[:-1] - 1
    n = np.isfinite(r).sum(axis=1); ort = np.where(n >= P["min_hisse"], np.nansum(np.where(np.isfinite(r), r, 0.0), axis=1) / np.maximum(n, 1), 0.0)
    endeks = pd.Series(np.r_[1.0, np.cumprod(1 + ort)]); sma = endeks.rolling(int(P["sma"]), min_periods=int(P["sma"])).mean()
    return np.where(sma.notna(), (endeks > sma).astype(float), np.nan)


def k64_olay_degerleri(olay: pd.DataFrame, H: Dict[str, Any], tanim: str, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Olay tablosuna her değişkenin değeri (<kod>), evren içi sırası (<kod>_sira), çöl içi sırası (<kod>_ic) ve piyasa koşulu (rejim) eklenir. Değer ve sıra
    sinyal günü t'de okunur; DUSUS ANA tanımda t'deki 'DUSUS' matrisinden (= DD252(t - 14)), İKİNCİL tanımda DD252(bas) ve bas günündeki evren sırasından."""
    E = E or K64_ESIK; X = olay.copy().reset_index(drop=True); tak = H["takvim"]; n = len(X)
    it = tak.get_indexer(pd.DatetimeIndex(X.sinyal)) if n else np.array([], int); jj = np.array([H["kol"].get(s, -1) for s in X.sembol], int)
    ok = (it >= 0) & (jj >= 0); a, b = np.maximum(it, 0), np.maximum(jj, 0)
    X["rejim"] = np.where(ok, H["rejim"][a], np.nan) if n else []
    for k in k64_kodlar(E):
        if k == "DUSUS" and tanim != "K24":
            ib = tak.get_indexer(pd.DatetimeIndex(X.bas)) if n else np.array([], int); okb = ok & (ib >= 0); c = np.maximum(ib, 0)
            X[k] = np.where(okb, H["X"]["DD252"][c, b], np.nan) if n else []; X[k + "_sira"] = np.where(okb, H["sira"]["DD252"][c, b], np.nan) if n else []
        else:
            X[k] = np.where(ok, H["X"][k][a, b], np.nan) if n else []; X[k + "_sira"] = np.where(ok, H["sira"][k][a, b], np.nan) if n else []
        X[k + "_ic"] = np.nan
        m = X.tekil.to_numpy(bool) if n else np.zeros(0, bool)
        if m.any():
            X.loc[m, k + "_ic"] = k64_ic_sira(X.sinyal.to_numpy("datetime64[D]")[m], X[k].to_numpy(float)[m], E["sira"]["ic_gun"], E["sira"]["ic_min"])
    return X


# ---------------------------------------------------------------- 4) CETVEL (FI_OLCUT aynen) + S1 / S2 ÖLÇÜLERİ
def k64_fark_matris(P: Dict[str, Any]) -> np.ndarray:
    """FI_OLCUT eşli farkının bütün (giriş günü x hisse) hücreleri için vektörel hali: R - aynı gün aynı hücredeki ÖTEKİ hisselerin ortalaması (en az 3 eş).
    fi_olcut_olay ile birebir aynı sayıyı verir (test edilir); S2 için."""
    R, H, ok = P["R"], P["H"], P["ok"]; n, u = R.shape; F = np.full((n, u), np.nan); nh = int(H.max()) + 2
    for d in range(n):
        g = ok[d]
        if g.sum() < 4:
            continue
        h = H[d, g] + 1; r = R[d, g]; s = np.bincount(h, r, minlength=nh); c = np.bincount(h, minlength=nh)
        with np.errstate(invalid="ignore", divide="ignore"):
            F[d, g] = np.where(c[h] - 1 >= 3, r - (s[h] - r) / np.maximum(c[h] - 1, 1), np.nan)
    return F


def k64_grup_farki(fu: np.ndarray, ayu: np.ndarray, fa: np.ndarray, aya: np.ndarray, B: int, tohum: int, guven: List[float], gecerli_pay: float = 0.9) -> Dict[str, float]:
    """ÜST - ALT ortalama farkı ve ay kümeli bootstrap: aylar (iki grubun ortak ay kümesi) yerine koyarak çekilir, iki grup AYNI çekilişle yeniden kurulur.
    Döner: nokta, alt, ust (yüzdelikler), sd, p_ust = 1 - Φ(nokta / sd), p_alt = 1 - Φ(-nokta / sd), gecerli (iki grubu da dolu çekiliş sayısı). Geçerli çekiliş
    payı < gecerli_pay ise aralık ve p yok (NaN)."""
    fu, fa = np.asarray(fu, float), np.asarray(fa, float); out = {k: np.nan for k in ("nokta", "alt", "ust", "sd", "p_ust", "p_alt")}; out["gecerli"] = 0
    if not len(fu) or not len(fa):
        return out
    out["nokta"] = float(fu.mean() - fa.mean()); aylar, ters = np.unique(np.r_[np.asarray(ayu), np.asarray(aya)], return_inverse=True); m = len(aylar)
    iu, ia = ters[:len(fu)], ters[len(fu):]
    su = np.bincount(iu, fu, minlength=m); cu = np.bincount(iu, minlength=m).astype(float)
    sa = np.bincount(ia, fa, minlength=m); ca = np.bincount(ia, minlength=m).astype(float)
    sec = np.random.default_rng(int(tohum)).integers(0, m, (int(B), m))
    nu, na = cu[sec].sum(axis=1), ca[sec].sum(axis=1); gec = (nu > 0) & (na > 0)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = np.where(gec, su[sec].sum(axis=1) / np.maximum(nu, 1) - sa[sec].sum(axis=1) / np.maximum(na, 1), np.nan)
    out["gecerli"] = int(gec.sum())
    if gec.sum() >= gecerli_pay * int(B) and gec.sum() > 1:
        v = d[gec]; out["alt"], out["ust"] = (float(x) for x in np.percentile(v, guven)); sd = float(v.std(ddof=1)); out["sd"] = sd
        if sd > 0:
            out["p_ust"] = float(K60._k60_norm_p(out["nokta"] / sd)); out["p_alt"] = float(K60._k60_norm_p(-out["nokta"] / sd))
    return out


def k64_ek_katki(n_ust: float, n_alt: float, ort_ust: float, ort_alt: float, ort_temel: float, alt: float, ust: float, n_esik: int) -> Dict[str, bool]:
    """'Ek katkı VAR' kuralı. olculebilir: iki grubun n'i >= n_esik ve aralık var. UST: ÜST grubunun ortalama eşli farkı > temel modelin (bütün çöl olayları)
    ortalama eşli farkı VE (ÜST - ALT) %95 alt sınırı > 0. ALT: ayna (ALT > temel VE üst sınır < 0)."""
    olc = bool(n_ust >= n_esik and n_alt >= n_esik and np.isfinite(alt) and np.isfinite(ust) and np.isfinite(ort_temel))
    return {"olculebilir": olc, "UST": bool(olc and ort_ust > ort_temel and alt > 0), "ALT": bool(olc and ort_alt > ort_temel and ust < 0)}


def k64_tutar(h: Dict[str, Any], O: Optional[Dict[str, Any]] = None) -> bool:
    """FI_OLCUT hücre şartı (fi_olcut_karar 'tut' ile aynı dört şart)."""
    O = O or FI.FI_OLCUT
    try:
        return bool(h.get("n", 0) >= O["n_esik"] and h["alt95"] > 0 and h["sira"] > 0.5 and h["portfoy"] > h["portfoy_esli_p90"])
    except (KeyError, TypeError):
        return False


def k64_hucre(X: pd.DataFrame, maliyet: float, net: bool = True) -> Dict[str, Any]:
    """Bir olay grubunun ölçüleri: FI.fi_olcut_hucre (60 gün; aynen) + medyan r60, r20 ölçüleri (ortalama / medyan getiri ve eşli fark), dört şart, aralık yarı
    genişliği ('saptanabilir en küçük etki'), maliyet sonrası (gidiş-dönüş maliyeti her olayın getirisinden ve eşli farkından düşülür; rastgele eş portföyler
    maliyetsiz kalır: tutucu)."""
    X = X.dropna(subset=["fark"]); h: Dict[str, Any] = dict(FI.fi_olcut_hucre(X))
    if not h.get("n"):
        return {"n": 0}
    h["medyan_r60"] = float(X.r60.median()); h["tutar"] = k64_tutar(h); h["yari_genislik"] = float((h["ust95"] - h["alt95"]) / 2.0)
    for k in ("r20", "fark20"):
        v = X[k].dropna() if k in X else pd.Series(dtype=float)
        h[f"ort_{k}"] = float(v.mean()) if len(v) else np.nan; h[f"medyan_{k}"] = float(v.median()) if len(v) else np.nan
    h["n20"] = int(X["fark20"].notna().sum()) if "fark20" in X else 0
    if net:
        Y = X.copy(); Y["r60"] = Y.r60 - maliyet; Y["fark"] = Y.fark - maliyet; g = FI.fi_olcut_hucre(Y)
        h.update({"ort_fark_net": g["ort_fark"], "alt95_net": g["alt95"], "ort_r60_net": g["ort_r60"], "portfoy_net": g["portfoy"],
                  "tutar_net": bool(g["n"] >= FI.FI_OLCUT["n_esik"] and g["alt95"] > 0 and g["sira"] > 0.5 and g["portfoy"] > g["portfoy_esli_p90"])})
    return h


def k64_hafif(X: pd.DataFrame) -> Dict[str, Any]:
    """Bilgi grupları (KAPSAM, ORTA) için hafif ölçü: n, ortalama / medyan eşli fark ve getiri (bootstrap ve portföy yok)."""
    X = X.dropna(subset=["fark"])
    if not len(X):
        return {"n": 0}
    return {"n": int(len(X)), "ort_fark": float(X.fark.mean()), "medyan_fark": float(X.fark.median()), "ort_r60": float(X.r60.mean()), "medyan_r60": float(X.r60.median()),
            "ort_r20": float(X.r20.mean()), "medyan_r20": float(X.r20.median()), "ort_fark20": float(X.fark20.mean()), "medyan_fark20": float(X.fark20.median())}


def k64_olc(P: Dict[str, Any], P20: Dict[str, Any], olay: pd.DataFrame) -> pd.DataFrame:
    """Olaylara FI_OLCUT ölçüleri: r60, esli_r60, sira (hücre içi), fark, _esler (fi_olcut_olay; aynen) + r20, fark20 (aynı yöntem, ufuk 20)."""
    X = FI.fi_olcut_olay(P, olay); Y = FI.fi_olcut_olay(P20, olay[["sembol", "giris"]])
    X["r20"] = Y.r60.to_numpy(); X["fark20"] = Y.fark.to_numpy()
    return X


def k64_s1(X: pd.DataFrame, pazar: str, tanim: str, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """S1: bir pazar ve tanımın ölçülmüş (tekil) olayları -> (hücre tablosu, ÜST - ALT tablosu). Hücreler: dönem x değişken x sıra türü (EVREN / IC) x grup
    (TEMEL = bütün çöl olayları, KAPSAM = sırası olanlar, UST, ORTA, ALT; KAPSAM ve ORTA hafif ölçüyle); karar sıra türünde ve ANA tanımda ayrıca piyasa koşulu katmanları."""
    E = E or K64_ESIK; S1 = E["s1"]; c = float(E["maliyet"][pazar]); sat: List[Dict[str, Any]] = []; frk: List[Dict[str, Any]] = []
    if not len(X):
        return pd.DataFrame(), pd.DataFrame()
    ay = pd.to_datetime(X.giris).dt.to_period("M").astype(str).to_numpy() if len(X) else np.array([], str)
    for dn, a, b in E["donem"]:
        md = ((X.giris >= a) & (X.giris <= b) & X.fark.notna()).to_numpy() if len(X) else np.zeros(0, bool)
        temel = k64_hucre(X[md], c) if md.any() else {"n": 0}
        kim0 = {"tanim": tanim, "pazar": pazar, "donem": dn}
        sat.append({**kim0, "degisken": "", "sira_turu": "", "grup": "TEMEL", "rejim": "HEPSI", **temel})
        for k in k64_kodlar(E):
            for st, ek in (("EVREN", "_sira"), ("IC", "_ic")):
                g = k64_grup(X[k + ek].to_numpy(float), E) if len(X) else np.array([], str); kim = {**kim0, "degisken": k, "sira_turu": st}
                H: Dict[str, Dict[str, Any]] = {}
                for ad, m in (("KAPSAM", md & (g != "")), ("UST", md & (g == "UST")), ("ORTA", md & (g == "ORTA")), ("ALT", md & (g == "ALT"))):
                    H[ad] = (k64_hucre(X[m], c) if ad in ("UST", "ALT") else k64_hafif(X[m])) if m.any() else {"n": 0}
                    sat.append({**kim, "grup": ad, "rejim": "HEPSI", **H[ad]})
                mu, ma = md & (g == "UST"), md & (g == "ALT")
                f = k64_grup_farki(X.fark.to_numpy(float)[mu], ay[mu], X.fark.to_numpy(float)[ma], ay[ma], S1["bootstrap"], S1["tohum"], S1["guven"], S1["gecerli_pay"])
                f20 = k64_grup_farki(X.fark20.to_numpy(float)[mu & X.fark20.notna().to_numpy()], ay[mu & X.fark20.notna().to_numpy()],
                                     X.fark20.to_numpy(float)[ma & X.fark20.notna().to_numpy()], ay[ma & X.fark20.notna().to_numpy()],
                                     S1["bootstrap"], S1["tohum"], S1["guven"], S1["gecerli_pay"])
                ekk = k64_ek_katki(H["UST"].get("n", 0), H["ALT"].get("n", 0), H["UST"].get("ort_fark", np.nan), H["ALT"].get("ort_fark", np.nan),
                                   temel.get("ort_fark", np.nan), f["alt"], f["ust"], S1["n_esik"])
                frk.append({**kim, "n_ust": H["UST"].get("n", 0), "n_alt": H["ALT"].get("n", 0), "n_temel": temel.get("n", 0), "ort_ust": H["UST"].get("ort_fark", np.nan),
                            "ort_alt": H["ALT"].get("ort_fark", np.nan), "ort_temel": temel.get("ort_fark", np.nan), "ort_kapsam": H["KAPSAM"].get("ort_fark", np.nan), **f,
                            "nokta20": f20["nokta"], "alt20": f20["alt"], "ust20": f20["ust"], "olculebilir": ekk["olculebilir"], "ek_UST": ekk["UST"], "ek_ALT": ekk["ALT"],
                            "tutar_UST": bool(H["UST"].get("tutar", False)), "tutar_ALT": bool(H["ALT"].get("tutar", False)),
                            "tutar_net_UST": bool(H["UST"].get("tutar_net", False)), "tutar_net_ALT": bool(H["ALT"].get("tutar_net", False))})
                if st == k64_karar_sirasi(k, E) and tanim == E["olay"]["ana"]:
                    rj = X.rejim.to_numpy(float)
                    for rad, rm in (("UST200", rj == 1), ("ALT200", rj == 0)):
                        for ad, m in (("UST", mu & rm), ("ALT", ma & rm)):
                            sat.append({**kim, "grup": ad, "rejim": rad, **(k64_hucre(X[m], c, net=False) if m.any() else {"n": 0})})
        if tanim == E["olay"]["ana"] and md.any():
            rj = X.rejim.to_numpy(float)
            for rad, rm in (("UST200", rj == 1), ("ALT200", rj == 0)):
                sat.append({**kim0, "degisken": "", "sira_turu": "", "grup": "TEMEL", "rejim": rad, **(k64_hucre(X[md & rm], c, net=False) if (md & rm).any() else {"n": 0})})
    return pd.DataFrame(sat), pd.DataFrame(frk)


def k64_s2(P: Dict[str, Any], F: np.ndarray, H: Dict[str, Any], olay: pd.DataFrame, pazar: str, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """S2 (bilgi): çöl DIŞI evrende, ANA çöl sinyali olan günlerde, değişkenin evren içi ÜST / ALT üçte birindeki hisselerin (giriş = ertesi takvim günü) 60
    günlük eşli farkı ve ÜST - ALT (ay kümeli bootstrap). 'Çöl dışı' = o gün ve önceki tekil_gun - 1 işlem gününde tekil ANA çöl sinyali vermemiş hisse."""
    E = E or K64_ESIK; S2 = E["s2"]; S1 = E["s1"]; G, N = F.shape; tak = P["tarih"]; ayri = int(E["olay"]["tekil_gun"]); sat = []
    if list(P["sembol"]) != list(H["sembol"]) or len(tak) != len(H["takvim"]):
        raise K64Hata("S2: panel ve değişken matrisleri aynı takvim / sembol sırasında değil")
    T = olay[olay.tekil] if len(olay) else olay
    it = tak.get_indexer(pd.DatetimeIndex(T.sinyal)) if len(T) else np.array([], int); jj = np.array([H["kol"].get(s, -1) for s in T.sembol], int)
    col = np.zeros((G, N), bool); gun = np.zeros(G, bool)
    for i, j in zip(it, jj):
        if i >= 0 and j >= 0:
            col[i:i + ayri, j] = True; gun[i] = True
    sat_i = np.flatnonzero(gun[:-1]); ay_g = tak[sat_i + 1].to_period("M").astype(str).to_numpy() if len(sat_i) else np.array([], str); gt = tak[sat_i + 1] if len(sat_i) else tak[:0]
    for dn, a, b in E["donem"]:
        md = np.asarray((gt >= a) & (gt <= b)) if len(sat_i) else np.zeros(0, bool)
        for k in k64_kodlar(E):
            row = {"pazar": pazar, "donem": dn, "degisken": k, "gun": int(md.sum())}
            if md.any():
                r = sat_i[md]; Fg = F[r + 1]; Sr = H["sira"][k][r]; dis = ~col[r] & np.isfinite(Fg) & np.isfinite(Sr); ayM = np.repeat(ay_g[md][:, None], N, axis=1)
                with np.errstate(invalid="ignore"):
                    mu = dis & (Sr >= E["sira"]["ust"]); ma = dis & (Sr <= E["sira"]["alt"])
                f = k64_grup_farki(Fg[mu], ayM[mu], Fg[ma], ayM[ma], S2["bootstrap"], S2["tohum"], S1["guven"], S1["gecerli_pay"])
                row.update({"n_ust": int(mu.sum()), "n_alt": int(ma.sum()), "ort_ust": float(Fg[mu].mean()) if mu.any() else np.nan,
                            "ort_alt": float(Fg[ma].mean()) if ma.any() else np.nan, "medyan_ust": float(np.median(Fg[mu])) if mu.any() else np.nan,
                            "medyan_alt": float(np.median(Fg[ma])) if ma.any() else np.nan, **f})
            sat.append(row)
    return pd.DataFrame(sat)


def k64_karar(Fk: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Karar tablosu (değişken x yön): ANA tanım, değişkenin KARAR sırası (k64_karar_sirasi: K64 ailesi çöl içi, K65 ailesi evren içi). BH %10 ailesi = ölçülebilen bütün (değişken x yön x pazar x bağımsız dönem) hipotezleri
    (p = p_ust / p_alt). Pazar kararı: 'ADAY' <=> iki bağımsız dönemde de o yönde 'ek katkı VAR' ve BH'den geçiyor; iki bağımsız dönemden biri ölçülemiyorsa
    'ÖLÇÜLEMEZ'; aksi 'İZ DEĞİL'. İŞARET: ölçülebilen bütün hücrelerde (iki pazar x üç dönem) ÜST - ALT nokta farkının işareti yönle aynı olmalı; değilse aday
    düşer. Genel karar: ABD ADAY ve işaret tutarlı -> 'ABD-ADAY' (İZ için Avrupa verisi yok); yalnız BIST -> 'BIST-ADAY (bilgi)'; ABD ölçülemiyorsa
    'ÖLÇÜLEMEZ'; aksi 'İZ DEĞİL'."""
    E = E or K64_ESIK; q = E["coklu"]["bh_q"]; bag = list(E["bagimsiz"])
    if not len(Fk):
        return pd.DataFrame()
    A = Fk[(Fk.tanim == E["olay"]["ana"]) & (Fk.sira_turu == Fk.degisken.map(lambda k: k64_karar_sirasi(k, E)))].copy()
    hip = []
    for r in A.to_dict("records"):
        for yon in ("UST", "ALT"):
            hip.append({"degisken": r["degisken"], "yon": yon, "pazar": r["pazar"], "donem": r["donem"], "olculebilir": bool(r["olculebilir"]), "ek": bool(r[f"ek_{yon}"]),
                        "p": float(r["p_ust" if yon == "UST" else "p_alt"]) if r["olculebilir"] else np.nan, "nokta": float(r["nokta"]) if pd.notna(r["nokta"]) else np.nan,
                        "tutar": bool(r[f"tutar_{yon}"]), "tutar_net": bool(r[f"tutar_net_{yon}"])})
    Hp = pd.DataFrame(hip)
    if not len(Hp):
        return pd.DataFrame()
    aile = (Hp.donem.isin(bag) & Hp.olculebilir).to_numpy(); Hp["bh"] = False; Hp["bonferroni"] = False; m = int(aile.sum())
    if m:
        Hp.loc[aile, "bh"] = K60.k60_bh(Hp.p.to_numpy(float)[aile], q)
        Hp.loc[aile, "bonferroni"] = Hp.p.to_numpy(float)[aile] * m <= q
    out = []
    for (k, yon), g in Hp.groupby(["degisken", "yon"], sort=False):
        isa = 1.0 if yon == "UST" else -1.0; olc = g[g.olculebilir]
        tutarli = bool(len(olc) and (np.sign(olc.nokta.to_numpy(float)) == isa).all())
        row: Dict[str, Any] = {"degisken": k, "yon": yon, "aile_m": m, "isaret_tutarli": tutarli}
        for p in E["pazar"]:
            gp = g[g.pazar == p].set_index("donem"); b = [gp.loc[d] for d in bag if d in gp.index]
            if len(b) < len(bag) or not all(bool(x.olculebilir) for x in b):
                pk = "ÖLÇÜLEMEZ"
            elif all(bool(x.ek) and bool(x.bh) for x in b):
                pk = "ADAY"
            else:
                pk = "İZ DEĞİL"
            row[f"{p}_karar"] = pk; row[f"{p}_ek"] = "/".join("E" if (d in gp.index and bool(gp.loc[d].ek)) else "h" for d, _a, _b in E["donem"])
            row[f"{p}_bh"] = "/".join("E" if (d in gp.index and bool(gp.loc[d].bh)) else "h" for d in bag)
            row[f"{p}_dort_sart"] = bool(len(gp) == len(E["donem"]) and gp.tutar.astype(bool).all()); row[f"{p}_dort_sart_net"] = bool(len(gp) == len(E["donem"]) and gp.tutar_net.astype(bool).all())
        kp = E["karar_pazari"]
        if row[f"{kp}_karar"] == "ADAY" and tutarli:
            row["karar"] = f"{kp}-ADAY (İZ için Avrupa verisi yok)"
        elif row[f"{kp}_karar"] == "ÖLÇÜLEMEZ":
            row["karar"] = "ÖLÇÜLEMEZ (" + kp + " hücrelerinde n < 30)"
        elif any(row[f"{p}_karar"] == "ADAY" for p in E["pazar"] if p != kp) and tutarli:
            row["karar"] = "BIST-ADAY (bilgi; karar pazarı değil)"
        else:
            row["karar"] = "İZ DEĞİL"
        out.append(row)
    return pd.DataFrame(out)


# ---------------------------------------------------------------- 5) GİRDİ DEMETİ, KAPSAM
def k64_girdi(E: Optional[Dict[str, Any]] = None, k60_veri: Optional[Dict[str, Tuple[str, int]]] = None) -> Dict[str, Dict[str, Any]]:
    """GERÇEK girdi (yalnız önbellek; ağ yok): pazar -> {V, T (temel tablo), pay (PAY_D için), ozet}."""
    E = E or K64_ESIK; out: Dict[str, Dict[str, Any]] = {}
    Vb = k64_fiyat_yukle("BIST", None, E); Sb = sorted(Vb); ham, oz = k64_isy_oku(Sb, None, E); kap = k64_kap_bilgi(); Tb = k64_bist_temel(Sb, ham, kap, E)
    var_q = ~np.isnat(Tb["bit"])
    out["BIST"] = {"V": Vb, "T": Tb, "pay": None, "ozet": {"hisse": len(Sb), "isy": {k: v for k, v in oz.items() if k != "bos_hisse"}, "temel_hisse": int(var_q.any(axis=0).sum()),
                                                             "bos_hisse": len(oz["bos_hisse"]), "ceyrek": int(var_q.sum()),
                                                             "bilgi_kap_pay": float((Tb["bilgi_kaynak"][var_q] == 1).mean()) if var_q.any() else None, "kap_kayit": len(kap)}}
    Va = k64_fiyat_yukle("ABD", None, E); Sa = sorted(Va); D = K60.k60_demet_yukle(k60_veri); Ta, bol, var = k64_abd_temel(Sa, D)
    vq = ~np.isnat(Ta["bit"])
    out["ABD"] = {"V": Va, "T": Ta, "pay": {"bolunme": bol, "sembol": Sa}, "ozet": {"hisse": len(Sa), "demette": int(var.sum()), "temel_hisse": int(vq.any(axis=0).sum()),
                                                                                       "ceyrek": int(vq.sum()),
                                                                                       "bilgi_dizin_pay": float((Ta["bilgi_kaynak"][vq] == 1).mean()) if vq.any() else None}}
    return out


def _k64_olaylar(pazar: str, V: Dict[str, pd.DataFrame], E: Dict[str, Any], isci: Optional[int] = None, ara: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    out = {"K24": k64_olay_k24(V, E)}
    if E["olay"]["d13"]["etkin"]:
        out["D13"] = k64_olay_d13(V, E, isci, ara)
    return out


def _k64_d13_ara(pazar: str) -> Optional[str]:
    """Gerçek veride D13 ara önbelleğinin yolu (fiyat dosyası + COL_v1.py + D13 ayarları değişince ad değişir)."""
    try:
        a = hashlib.sha256(json.dumps([K60._k60_sha(os.path.join(K64_YOL["veri"], f"V_{pazar}.pkl")), K60._k60_sha(os.path.join(KOK_K64, "COL_v1.py")), K64_ESIK["olay"],
                                       K64_ESIK["kriz"]], sort_keys=True).encode()).hexdigest()[:16]
    except OSError:
        return None
    return os.path.join(K64_YOL["ara"], f"d13_{pazar}_{a}.pkl")


def k64_kapsam(cikti: Optional[str] = None, girdi: Optional[Dict[str, Dict[str, Any]]] = None, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """KAPSAM: yalnız SAYIM. Pazar x tanım x dönem: olay sayısı (tekilleştirme öncesi / sonrası), 60 günlük penceresi kesikten önce biten olay, her değişkenin
    hesaplanabildiği olay ve ÜST / ORTA / ALT sayıları (evren içi ve çöl içi sıra). Getiri, eşli fark, FI_OLCUT paneli HESAPLANMAZ."""
    E = E or K64_ESIK; sentetik = girdi is not None; t0 = time.time(); girdi = girdi if sentetik else k64_girdi(E, K60.k60_veri_sha(dogrula=False))
    sat = []; ozet: Dict[str, Any] = {"zaman": _k64_simdi(), "surum": K64_SURUM, "muhur": k64_esik_sha(E), "pazar": {}}
    for pazar in E["pazar"]:
        if pazar not in girdi:
            continue
        g = girdi[pazar]; V = g["V"]; H = k64_pazar_hazirla(pazar, V, g.get("T"), g.get("pay"), E); tak = H["takvim"]; son = len(tak) - 1
        O = _k64_olaylar(pazar, V, E, None, None if sentetik else _k64_d13_ara(pazar))
        ozet["pazar"][pazar] = {**g.get("ozet", {}), "takvim_gun": len(tak), "ilk_gun": str(tak[0].date()), "son_gun": str(tak[-1].date()),
                                "k24_sapma": int(O["K24"].attrs.get("sapma", 0)),
                                "evren_kapsam": {k: float(np.isfinite(np.where(H["var"], H["X"][k], np.nan)).sum() / max(int(H["var"].sum()), 1)) for k in k64_kodlar(E)}}
        for tanim, X0 in O.items():
            X = k64_olay_degerleri(X0, H, tanim, E); gi = tak.get_indexer(pd.DatetimeIndex(X.giris)) if len(X) else np.array([], int)
            X["pencere"] = (gi >= 0) & (gi + FI.FI_OLCUT["ufuk"] - 1 <= son) if len(X) else []
            for dn, a, b in E["donem"]:
                md = ((X.giris >= a) & (X.giris <= b)).to_numpy() if len(X) else np.zeros(0, bool); tk = md & X.tekil.to_numpy(bool) if len(X) else md
                pn = tk & X.pencere.to_numpy(bool) if len(X) else md
                kim = {"tanim": tanim, "pazar": pazar, "donem": dn, "n_ham": int(md.sum()), "n_tekil": int(tk.sum()), "n_pencere": int(pn.sum()),
                       "n_gecer_ham": int((md & X.gecer.to_numpy(bool)).sum()) if "gecer" in X and len(X) else None}
                sat.append({**kim, "degisken": "(olay)"})
                for k in k64_kodlar(E):
                    ge = k64_grup(X[k + "_sira"].to_numpy(float), E) if len(X) else np.array([], str); gc = k64_grup(X[k + "_ic"].to_numpy(float), E) if len(X) else ge
                    sat.append({**kim, "degisken": k, "n_deger": int((pn & np.isfinite(X[k].to_numpy(float))).sum()) if len(X) else 0,
                                "n_ust": int((pn & (ge == "UST")).sum()), "n_orta": int((pn & (ge == "ORTA")).sum()), "n_alt": int((pn & (ge == "ALT")).sum()),
                                "n_ust_ic": int((pn & (gc == "UST")).sum()), "n_orta_ic": int((pn & (gc == "ORTA")).sum()), "n_alt_ic": int((pn & (gc == "ALT")).sum())})
        k64log.info("kapsam %s: %d hisse, %d gün (%.0f sn)", pazar, len(H["sembol"]), len(tak), time.time() - t0)
    K = pd.DataFrame(sat); cik = cikti or K64_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    K.to_csv(_k64_yol("kapsam", cikti), index=False); K60._k60_json_yaz(_k64_yol("kapsam_ozet", cikti), ozet)
    return K


def k64_kapsam_notu(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """Kapsam sayımının ön kayıt metnine giren özeti (yalnız SAYI). Mühre girmez (eşik değil)."""
    E = E or K64_ESIK; yk, yo = _k64_yol("kapsam", cikti), _k64_yol("kapsam_ozet", cikti)
    if not (os.path.exists(yk) and os.path.exists(yo)):
        return "Kapsam sayımı henüz koşulmadı (`python -I K64.py kapsam`)."
    K = pd.read_csv(yk); O = K60._k60_json_oku(yo); par = [f"Kapsam sayımı ({O.get('zaman', '?')}; `python -I K64.py kapsam`; yalnız SAYI: getiri, eşli fark, FI_OLCUT paneli hesaplanmadı).\n"]
    for p, v in O.get("pazar", {}).items():
        ek = ", ".join(f"{k} %{100 * float(x):.0f}" for k, x in (v.get("evren_kapsam") or {}).items())
        par.append(f"- {p}: {v.get('hisse')} hisse, takvim {v.get('takvim_gun')} gün ({v.get('ilk_gun')} .. {v.get('son_gun')}); temel verisi olan hisse {v.get('temel_hisse')}, "
                   f"çeyrek kaydı {v.get('ceyrek')}; bilgi tarihi gerçek kaynaktan (BIST: KAP yayın günü; ABD: EDGAR dizini) "
                   f"%{100 * float(v.get('bilgi_kap_pay') if v.get('bilgi_kap_pay') is not None else (v.get('bilgi_dizin_pay') or 0)):.1f}, kalanı yedek kural"
                   + (f"; kalem şablonu dışında kalan (banka / sigorta / finansman; BIST VERİSİ YOK) {v.get('bos_hisse')} hisse" if v.get("bos_hisse") is not None else "")
                   + (f"; K60 demetinde bulunan {v.get('demette')} hisse" if v.get("demette") is not None else "")
                   + f". Evren hisse-günlerinde değişken doluluk: {ek}.")
    for tanim in K.tanim.unique():
        par.append(f"\n**{tanim} olayları** (ham = tekilleştirme öncesi; tekil = 60 işlem günü kuralı sonrası; pencere = 60 günlük penceresi 31.08.2026 kesiğinden önce biten tekil olay)\n\n"
                   "| pazar | dönem | ham | tekil | pencere |\n|---|---|---|---|---|")
        for r in K[(K.tanim == tanim) & (K.degisken == "(olay)")].itertuples():
            par.append(f"| {r.pazar} | {r.donem} | {int(r.n_ham)} | {int(r.n_tekil)} | {int(r.n_pencere)} |")
        par.append(f"\n**{tanim}: değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; EVREN = aynı gün evren içi sıra, İÇ = çöl içi sıra; hücre = değer / ÜST / ALT)\n\n"
                   "| değişken | sıra | " + " | ".join(f"{p} {d[0]}" for p in E["pazar"] for d in E["donem"]) + " |\n|---|---|" + "---|" * (len(E["pazar"]) * len(E["donem"])))
        for k in k64_kodlar(E):
            for st, u, al in (("EVREN", "n_ust", "n_alt"), ("İÇ", "n_ust_ic", "n_alt_ic")):
                h = []
                for p in E["pazar"]:
                    for d in E["donem"]:
                        x = K[(K.tanim == tanim) & (K.pazar == p) & (K.donem == d[0]) & (K.degisken == k)]
                        h.append("—" if not len(x) else f"{int(x.n_deger.iloc[0])} / {int(x[u].iloc[0])} / {int(x[al].iloc[0])}")
                par.append(f"| {k} | {st} | " + " | ".join(h) + " |")
    A = K[(K.tanim == E["olay"]["ana"]) & (K.degisken != "(olay)") & K.donem.isin(E["bagimsiz"])]
    A = A.assign(ic=[k64_karar_sirasi(k, E) == "IC" for k in A.degisken]); A = A.assign(ku=np.where(A.ic, A.n_ust_ic, A.n_ust), ka=np.where(A.ic, A.n_alt_ic, A.n_alt))
    az = [f"{r.degisken} {r.pazar} {r.donem} ({'İÇ' if r.ic else 'EVREN'}: ÜST {int(r.ku)}, ALT {int(r.ka)})" for r in A.itertuples()
          if (r.ku < E["s1"]["n_esik"] or r.ka < E["s1"]["n_esik"]) and not (r.degisken == "PAY_D" and r.pazar == "BIST")]
    ev = [f"{r.degisken} {r.pazar} {r.donem} (ÜST {int(r.n_ust)}, ALT {int(r.n_alt)})" for r in A.itertuples() if r.ic and (r.n_ust < E["s1"]["n_esik"] or r.n_alt < E["s1"]["n_esik"])]
    par.append("\nK64 ailesinde EVREN sırasıyla (bu ailede sağlamlık, karar dışı) grubu n < " + str(E["s1"]["n_esik"]) + " olan bağımsız dönem hücreleri: " + ("; ".join(ev) if ev else "yok") + ".")
    par.append(f"\nANA tanım, KARAR sırası (K64 ailesi İÇ, K65 ailesi EVREN), bağımsız dönemlerde grubu n < {E['s1']['n_esik']} olan (karar kuralında 'ÖLÇÜLEMEZ' kalacak) hücreler (pencereli olay sayısıyla; ölçülebilen olay daha az "
               "olabilir): " + ("; ".join(az) if az else "yok") + ". BIST PAY_D: BIST VERİSİ YOK.")
    return "\n".join(par)


# ---------------------------------------------------------------- 6) ÖN KAYIT
def k64_onkayit_metin(zaman: str, veri_sha: Dict[str, Tuple[str, int]], kapsam: str, E: Optional[Dict[str, Any]] = None) -> str:
    E = E or K64_ESIK; O = E["olay"]; S = E["sira"]; S1 = E["s1"]; B = E["bist"]; FO = FI.FI_OLCUT; K24 = FI.FI_K24; CV = _k64_colv1()
    vs = "\n".join(f"- {k}: sha256 {v[0]} ({v[1]} dosya)" for k, v in veri_sha.items()) or "- (veri dosyası bulunamadı)"
    dg = "\n".join(f"| {d['kod']} | {d['aile']} | {d['tanim']} | {d['kaynak']} |" for d in E["degisken"])
    dn = ", ".join(f"{a} ({b} .. {c})" for a, b, c in E["donem"])
    return f"""# K64 + K65 — ÇÖL SİNYALİNE EK BİLGİ: ÖN KAYIT (ölçümden ÖNCE)

{K64_SURUM}
Yazım zamanı: {zaman}
ESIK_SHA256: {k64_esik_sha(E)}

Bu dosya gerçek veride değişkene bağlı HİÇBİR getiri / eşli fark hesaplanmadan yazıldı (yalnız `kapsam` sayımı koşuldu: §12). `python -I K64.py kos`
bu dosya git'e işlenmeden, mühür ya da veri sha256'ları tutmadan çalışmaz. Sonuç görüldükten sonra yeni kural eklenmez.

## Veri (sha256; `kos` başında yeniden hesaplanır, farklıysa koşu durur)
{vs}
K60 önbellekleri (/tmp/k60_fiyat, /tmp/k60_secframes ...) K60 ön kaydındaki sha256'larla doğrulanır (K60.k60_onkayit_dogrula, veri = True). K60 mührü mühre girer.

## 0. Soru (Cemal'in isteği)
Çöl tanımı ve mevcut cetvel DEĞİŞMEZ. İki değişken ailesi (K64: 52 haftalık zirve; K65: şirket kalitesi) mevcut ÇÖL sinyaline EK BİLGİ taşıyor mu?
Her değişken tek tek ve çöl sinyaliyle etkileşimli sınanır; katkı değişkensiz temel modele (yalnız çöl) karşı ölçülür. Üretim koduna ekleme yapılmaz.

## 1. Olay (çöl sinyali; tanımlar DEĞİŞTİRİLMEDEN içe alınır)
ÇÖL TANIMI ENVANTERİ (depoda çöl olayı üreten tanımlar):
- (i) K24 'iki evre' çöl sinyali — FON_IZI.fi_k24_tara, eşikler FI_K24 = {json.dumps(K24, ensure_ascii=False)}. Sinyal günü t: SMA20 üstündeki kapanış serisinin
  tam {K24['seri']}. günü; serinin önündeki {K24['once']} barın >= %{100 * K24['once_alt']:.0f}'i SMA20 altında; serideki mumların en çok {K24['delen_en_cok']}'sinin dibi SMA20'yi deler;
  Bollinger genişliği son {K24['bbw_pencere']} barın en yükseğinin <= %{100 * K24['bbw_oran']:.0f}'i; son {K24['bbw_pencere']} barın dibi önceki 120 bar tepesinin en az %{-100 * K24['dusus']:.0f} altında.
  K28 / K29 / K32 / K38-B (F1) / K41 / Ç118'de 'çöl' olarak, iki pazarda aynı kodla ve FI_OLCUT cetveliyle kullanıldı. **ANA olay tanımı budur.**
  Çöl başlangıcı b = t - {O['k24_bas_geri']} işlem günü (1. evrenin ve {K24['bbw_pencere']} barlık sıkışma penceresinin ilk barı). Giriş = hissenin t'den sonraki ilk işlem günü açılışı.
- (ii) Üretim tanımı — COL_v1.col_olc (SEGMENT_MOD = '{CV.SEGMENT_MOD}': D13 dip kutusu; uzunluk >= {CV.MIN_UZ} bar, yükseklik <= {CV.MAX_YUK} ATR) + üretim kuralı GECER (clv >= {CV.E_CLV},
  bant_son >= {CV.E_BS}, ortaust >= {CV.E_OU}) + AL: kapanış > tavan x {CV.AL_PAY}. **İKİNCİL (sağlamlık) tanım:** tespit günleri her haftanın son işlem günü e (yalnız <= e barları;
  en az {O['d13']['min_bar']} bar); olay günü = e'den sonraki {O['d13']['kirilim_gun']} bar içinde, kapanış tabanın altına inmeden önce, ilk AL kırılımı günü (COL_v1.tara kuralı); kırılımdan önce
  GECER tespiti olmalı. Çöl başlangıcı b = kutu başı (dip günü, 'bas_tarih'). Giriş = kırılımdan sonraki ilk işlem günü açılışı. Haftalık tespit ızgarası hesap
  süresi içindir (günlük ızgara ~5 kat süre); üretim de günde bir kez tarar, bu yüzden haftalık ızgara üretimin bulacağı kırılımların bir ALT KÜMESİNİ verir (beyan).
  İkincil tanım BH ailesine ve karara GİRMEZ; yalnız 'aynı yön mü' diye raporlanır.
- (iii) K51 COL_YOLU_ABD P1 ('çöl oluşurken': cy_olculer / cy_cekirdek / cy_imza / cy_sinyaller; L = 60, düşüş <= -%35, imza >= 3). Bu işte KULLANILMAZ: 'çöl bitiş / sinyal günü'
  değil oluşum günüdür, kendi evreni (batanlar örneklemi + likidite maskesi) ve kendi cetveli (üçlü bariyer) vardır.
TEKİLLEŞTİRME: aynı hissede {O['tekil_gun']} işlem günü içinde tekrarlanan sinyal tek olaydır; son TUTULAN sinyalden en az {O['tekil_gun']} işlem günü sonra gelen ilk sinyal tutulur
(ANA tanımda FI_K24 'tekrar' = 60 ile birebir aynı sonuç; kodda denetlenir).

## 2. Evren, veri ve bilgi tarihi
- Fiyat: BIST = V_BIST.pkl, ABD = V_ABD.pkl (islenmis-veri dalı; FON_IZI.fi_k1_veri çıktıları; K24 çöl cetvelinin ölçüldüğü evrenler). Fon krizi: {E['kriz']}
  sonrası barlar atılır; 60 günlük penceresi bu tarihi aşan olay ölçülmez (FI_OLCUT 'kriz').
- ABD temel veri: K60 demeti (SEC XBRL frames 2009Q1-2026Q2 + EDGAR başvuru dizini), K60.py DEĞİŞTİRİLMEDEN içe alınır. BİLGİ TARİHİ kuralı K60_ON_KAYIT.md §3
  ile aynıdır: bir çeyreğin bilgi tarihi = çeyrek sonundan en az 15 gün sonraki ilk 10-Q / 10-K ailesi başvurusunun günü (yoksa yedek: çeyrek sonu + 90, mali yıl
  sonu + 120 gün); bir değer ancak bilgi tarihi < t ise kullanılır; ç0 = bilgi tarihi < t olan en son çeyrek (çeyrek sonu t'den en çok 200 gün önce), y0 = en son
  mali yıl (en çok 550 gün). V_ABD sembolü K60 demetinde yoksa temel veri YOK sayılır.
- BIST temel veri: KALEMLER İş Yatırım mali tablo servisi (MaliTablo, financialGroup {B['grup']}, {B['yil_bas']}-{B['yil_son']}; `python K64.py indir`): {json.dumps(B['kalem'], ensure_ascii=False)}.
  Gelir tablosu ve nakit akışı kümülatiftir; çeyrek = kümülatif farkı (aynı takvim yılı içinde). Satış geliri 0 / yok olan dönemde satış ve brüt kâr YOK sayılır.
  BİLGİ TARİHİ = KAP 'Finansal Rapor' listesinde (FON_IZI.fi_k28_liste_bist çıktıları; 2016-07 ->) aynı hisse-yıl-dönemin İLK yayın günü; KAP kaydı yoksa ya da dönem
  sonuna {B['kap_min_gun']} günden yakınsa YEDEK: ara dönem sonu + {B['yedek_ara_gun']} gün, yıl sonu + {B['yedek_yil_gun']} gün. 'Bilgi tarihi < t' kuralı aynen (akşam yayınları için de güvenli).
  Banka / sigorta / faktoring gibi {B['grup']} şablonu dışındaki şirketlerde kalem YOK ('BIST VERİSİ YOK'; vekil uydurulmaz).
- BIST'te PAY_D (hisse sayısı değişimi) için 'BIST VERİSİ YOK': ödenmiş sermaye değişimi bedelsiz (seyrelme değil) ile bedelli / tahsisli artışı ayırmıyor; güvenilir
  bölünme düzeltmeli pay serisi yok. Vekil uydurulmadı.

## 3. Değişkenler (hepsi yalnız sinyal günü t ve öncesi bilgiyle; C = hissenin kendi işlem günlerindeki kapanış)
| kod | aile | tanım | kaynak / beklenti (bilgi) |
|---|---|---|---|
{dg}

K65 değişkenleri K60'ın 'o gün bilinen' okuyucusuyla (K60._K60Temel, K60.k60_pay, K60._k60_bol / _k60_ilk; gelir etiketleri K57_ABD_GELIR) hesaplanır; GP = K60 GP_A,
OP = K60 OP_BE, SATIS_B = K60 REV_YOY formülleridir (ay sonunda K60 ile birebir aynı; testte denetlenir). Beklenti sütunu bilgidir: her değişken İKİ YÖNDE sınanır.

## 4. S1 — 'etkileşim / ek katkı' (asıl soru)
- Örneklem: yalnız ÇÖL OLAYLARI (tekil; FI_OLCUT ile ölçülebilen).
- İki sıra türü her değişken için hesaplanır; hangisinin KARAR sırası olduğu AİLE BAZINDA sabittir (aşağıda). Öteki sıra o değişkende 'sağlamlık, karar dışı'dır.
- 'EVREN' sırası: olayın değişken değerinin, AYNI GÜN o pazarda işlem gören ve o değişkeni hesaplanabilen bütün hisseler içindeki
  yüzdelik sırası = (küçük olan sayısı + 0,5 x eşit olan sayısı, kendisi dahil) / n (n >= {S['min_evren']}). ÜST = sıra >= 2/3, ALT = sıra <= 1/3, ORTA = arası.
  (DUSUS ikincil tanımda çöl başlangıcı gününde okunur ve o günün evren sırasıyla sınıflanır.)
- 'İÇ' (çöl içi) sırası: olayın değerinin, sinyal günü [t - {S['ic_gun']} gün, t] aralığındaki aynı pazar ve tanımın tekil çöl olayları (kendisi dahil) içindeki sırası
  (n >= {S['ic_min']}; geleceğe bakmaz). ÜST / ALT eşikleri aynı (>= 2/3, <= 1/3).
- **KARAR SIRASI (aile bazında; ana oturum kararı, 11 Kasım 2026):** K64 ailesi ({', '.join(k64_kodlar(E, 'K64'))}) = **İÇ**; K65 ailesi ({', '.join(k64_kodlar(E, 'K65'))}) = **EVREN**.
  K64 ailesinde EVREN, K65 ailesinde İÇ sırası 'sağlamlık, karar dışı' olarak raporlanır (karara ve BH ailesine GİRMEZ).
  GEREKÇE: çöl tanımı gereği düşmüş hissedir; evren sırası K64 ölçülerinde olayları ALT üçte birde topluyor (kapsam sayımı §12: DUSUS ABD 2022-2026 ÜST n = 27; Z52 ABD ÜST
  160 / 90 / 38) ve 'çöl İÇİNDE ayırıyor mu' sorusu evren sırasıyla ölçülemez kalıyor. Bu karar ölçümden ÖNCE, yalnız KAPSAM SAYIMI (olay sayıları) görülerek verildi:
  **kapsam sayımı görüldü, getiri görülmedi** (hiçbir getiri / eşli fark hesaplanmadı). Başka hiçbir eşik ya da kural değişmedi.
- Temel model = hücredeki BÜTÜN çöl olayları (değişkensiz). Her grup için FI_OLCUT ölçüleri (§6).
- ÜST - ALT = iki grubun ortalama eşli farklarının farkı; ay kümeli bootstrap (giriş ayları yerine koyarak çekilir, iki grup aynı çekilişle kurulur; {S1['bootstrap']} çekiliş,
  tohum {S1['tohum']}; iki grubu da dolu çekiliş payı < %{100 * S1['gecerli_pay']:.0f} ise aralık yok); %95 aralık = {S1['guven'][0]} / {S1['guven'][1]} yüzdelikleri.
- **'EK KATKI VAR (yön ÜST)'** <=> n_ÜST >= {S1['n_esik']} ve n_ALT >= {S1['n_esik']} VE ÜST grubunun ortalama eşli farkı > temel modelin ortalama eşli farkı VE (ÜST - ALT) %95 alt sınırı > 0.
  **'EK KATKI VAR (yön ALT)'** ayna: ALT grubunun ortalama eşli farkı > temel VE (ÜST - ALT) %95 üst sınırı < 0.

## 5. S2 — 'tek başına' (bilgi)
Aynı değişkenin çöl DIŞI evrende, ANA çöl sinyali olan günlerde, evren içi ÜST / ALT üçte birindeki hisselerin (giriş = ertesi takvim günü açılışı) 60 günlük eşli
farkı ve ÜST - ALT (ay kümeli bootstrap; {E['s2']['bootstrap']} çekiliş, tohum {E['s2']['tohum']}). 'Çöl dışı' = o gün ve önceki {O['tekil_gun'] - 1} işlem gününde tekil ANA çöl sinyali vermemiş hisse.
S2 karara girmez; 'değişken çölden bağımsız da çalışıyor mu' sorusunun cevabıdır.

## 6. Cetvel (FON_IZI FI_OLCUT aynen; fonksiyonlar çağrılır, kopyalanmaz)
FI_OLCUT = {json.dumps({k: v for k, v in FO.items() if k not in ('donem', 'karar')}, ensure_ascii=False)}.
- fi_olcut_panel / fi_olcut_olay / fi_olcut_hucre: giriş = sinyalden sonraki ilk işlem günü açılışı; r60 = 60. gün kapanışı / giriş - 1; EŞLİ FARK = r60 - aynı giriş günü
  aynı 60 gün momentum beşliği x likidite üçlüsü hücresindeki öteki hisselerin ortalama r60'ı; ay kümeli bootstrap %95; hücre içi sıra; 10 yuvalı slot portföyü 200
  rastgele eş portföyün %90'ından büyük. HÜCRE TUTAR <=> n >= {FO['n_esik']}, aralığın alt ucu > 0, ortalama sıra > 0,50, portföy > rastgele %90.
- Eşli kontrol boyutları: aynı gün (dolayısıyla aynı ay), momentum, likidite (FI_OLCUT) + PİYASA KOŞULU katmanı: sinyal günü eşit ağırlıklı evren endeksi (günlük
  kapanış getirilerinin ortalaması) {E['piyasa']['sma']} günlük ortalamasının üstünde / altında; ÜST, ALT ve TEMEL grupları iki katmanda ayrı raporlanır (bilgi).
- Ek ufuk: r20 ve 20 günlük eşli fark aynı yöntemle (fi_olcut_panel ufuk = {E['ek_ufuk']}; bilgi).
- Raporlanan: n, ortalama ve medyan getiri (20 ve 60 gün), ortalama ve medyan eşli fark, %95 aralık, sıra, portföy, dört şart.
- MALİYET: gidiş-dönüş BIST {1e4 * E['maliyet']['BIST']:.0f} bp, ABD {1e4 * E['maliyet']['ABD']:.0f} bp (tek yön 30 / 10 bp) her olayın getirisinden ve eşli farkından düşülür; rastgele eş portföyler
  maliyetsiz bırakılır (tutucu). Uygulanabilirlik: giriş ertesi açılış; olay başına tek giriş; slot portföyü 10 yuva.

## 7. Hücreler ve KARAR
- Hücre = pazar ({', '.join(E['pazar'])}) x dönem (giriş gününe göre): {dn}. Son iki dönem ÖRTÜŞÜR (2023-2026, 2022-2026'nın alt kümesi); bağımsız dönemler
  {E['bagimsiz'][0]} ve {E['bagimsiz'][1]}. 2023-2026 tutarlılık için ayrıca raporlanır, BH ailesine girmez.
- Karar birimi: (değişken, yön). ANA tanım (K24) ve değişkenin KARAR sırası ile (§4: K64 ailesi İÇ, K65 ailesi EVREN; kapsam sayımı görüldü, getiri görülmedi).
- Pazar kararı: **'ADAY'** <=> o pazarın iki bağımsız döneminin İKİSİNDE de aynı yönde 'EK KATKI VAR' ve ikisi de çoklu test düzeltmesinden geçiyor (§8).
  İki bağımsız dönemden birinde n_ÜST ya da n_ALT < {S1['n_esik']} ise **'ÖLÇÜLEMEZ'** (az veri; 'İZ DEĞİL' ile karıştırılmaz). Aksi **'İZ DEĞİL'**.
- İŞARET: ölçülebilen bütün hücrelerde (iki pazar x üç dönem) ÜST - ALT nokta farkının işareti yönle aynı olmalı; bir hücrede işaret dönerse aday düşer ('İZ DEĞİL').
- Genel karar: karar pazarı ABD'dir (CLAUDE.md: BIST bilgi). ABD 'ADAY' ve işaret tutarlı -> **'ABD-ADAY'**. 'İZ' bu işte VERİLEMEZ: İZ = ABD'nin üç döneminde de
  'ek katkı VAR' + grubun FI_OLCUT dört şartı + aynısının Avrupa'da tutması; Avrupa temel verisi ve Avrupa çöl koşusu bu işte yok. Yalnız BIST 'ADAY' ->
  'BIST-ADAY (bilgi)'. Grubun dört şartı (maliyetsiz ve maliyetli) üç dönemde tutuyorsa ayrıca yazılır.

## 8. Çoklu test
Aile = ANA tanım, değişkenin KARAR sırası (§4: K64 ailesi İÇ, K65 ailesi EVREN; karar kapsam sayımı görülerek, getiri görülmeden verildi), ölçülebilen bütün (değişken x yön x pazar x bağımsız dönem) hipotezleri (en çok {len(E['degisken'])} x 2 x 2 x 2 - 4 = {len(E['degisken']) * 8 - 4}; BIST PAY_D yok).
p = 1 - Φ(±(ÜST - ALT) / bootstrap standart sapması) (tek yönlü). Benjamini-Hochberg q = %{100 * E['coklu']['bh_q']:.0f} (K60.k60_bh); Bonferroni (p x m <= %{100 * E['coklu']['bh_q']:.0f}) bilgi olarak yazılır.

## 9. GÜÇ BEYANI
K58 (arastirma_cikti/k58_cetvel_sagla/K58_RAPOR.md): FI_OLCUT, 60 günde +%2'lik gerçek etkiyi n = 300 olayda yalnız %11, +%4'ü %45 olasılıkla yakalıyor. Çöl olayları
içinde üçte bir grupları daha da küçüktür (§12). Her hücrede n ve 'saptanabilir en küçük etki' (grup aralığının yarı genişliği; ÜST - ALT için aralık yarı genişliği)
raporlanır. 'İZ DEĞİL' yalnız ölçülebilen hücreler için söylenir; n < {S1['n_esik']} olan hücre 'ÖLÇÜLEMEZ'dir. 'Ek katkı yok' sonucu 'etki yok' demek değildir; 'bu veriyle
gösterilemedi' demektir.

## 10. Yanlılık beyanı
- YAŞAYAN YANLILIĞI (kaçınılamıyor): iki evren de yalnız BUGÜN işlem gören hisselerdir (V_BIST 2026-10, V_ABD 2026-10 listeleri). Batan / kottan çıkan şirketler yok;
  çöl (düşmüş hisse) ve düşük kalite grupları batmaya en açık gruplardır, bu grupların getirisi YUKARI yanlıdır. Kaliteli - kalitesiz farkı bu yüzden olduğundan
  KÜÇÜK görünebilir (kalitesizlerin batanları örneklemde yok). Eşli kontrol aynı evrenden seçildiği için yanlılığın bir kısmı farkta götürülür, tamamı değil.
- Yeniden sunum: SEC frames ve İş Yatırım değerleri ilk açıklanan değil, sonradan düzeltilmiş değer olabilir (tarih doğru, değer yeniden sunulmuş olabilir).
- BIST: TMS 29 (enflasyon muhasebesi; 2023 yıl sonu ve sonrası) kümülatif farklarını ve yıllık büyümeleri bozar (farklı satın alma gücü); bütün şirketleri birlikte
  etkilediği için sıra tabanlı gruplar kısmen korunur. Özel hesap dönemli şirketlerde (ör. spor kulüpleri) kümülatif farkı yanlış çeyrek verir. KAP listesi 2016-07
  öncesini kapsamaz (yedek kural). Fiyatlar fi_duzelt ile bölünme / bedelsiz düzeltmelidir; temettü düzeltmesi yok.
- ABD: yedek bilgi tarihi geç başvuranlarda geleceğe bakabilir (K60 beyanı). FCF yıllıktır (y0): çeyreklik nakit akışı önbellekte yok. V_ABD fiyatları temettü
  düzeltmelidir (Yahoo); 52 hafta ölçüleri düzeltilmiş kapanışla hesaplanır.
- K24 sinyali yalnız fiyatla tanımlıdır; sektör rüzgârı / katalizör şartı içermez (Cemal'in çöl tanımının tamamı değildir; cetvelde kullanılan ölçülebilir hâlidir).

## 11. SAPMA / BOŞLUK listesi (iş tanımına göre; en dar yorum)
BOŞLUK 1. DUSUS ANA tanımda 'çöl başlangıcı' = t - {O['k24_bas_geri']} işlem günü: K24 çöl başlangıcını ayrı bir gün olarak vermez; kuralın baktığı pencerenin ilk barı alındı.
BOŞLUK 2. Dönem = GİRİŞ gününe göre (FI_OLCUT alışkanlığı). 2017-2021 çöllerinin 252 günlük geçmişi için fiyat 2015-06'dan başlar (yeterli).
BOŞLUK 3. BORC = toplam yükümlülük / toplam varlık (iki pazarda aynı). 'Toplam finansal borç' ABD önbelleğinde yalnız uzun vadeli borç etiketiyle var (eksik); bu yüzden
  defter kaldıracı alındı. K60 LEV_MKT (yükümlülük / piyasa değeri) fiyat içerdiği için alınmadı.
BOŞLUK 4. FCF ABD'de yıllık (y0), BIST'te son 4 çeyrek. OP paydası özkaynak (K60 OP_BE); özkaynağı <= 0 olan şirkette OP yok.
BOŞLUK 5. KAR_B = TTM net kâr değişimi / dört çeyrek önceki toplam varlık. SATIS_B = son çeyrek satışının yıllık büyümesi (iki çeyrek de > 0).
BOŞLUK 6. PAY_D günlük sürüm: t ve t - {E['k65']['pay_gun']} takvim günü (K60 NSI_1Y ay sonlarıyla 12 ay). BIST'te yok.
BOŞLUK 7. Evren sırası için 'uygun hisse' = o gün kapanışı olan ve değişkeni hesaplanabilen hisse (gelecekteki getirinin varlığına bakılmaz). Ek fiyat / likidite süzgeci yok
  (K24 çöl cetvelinde de yoktu); likidite eşli kontrolün boyutudur.
BOŞLUK 8. Piyasa koşulu endeksi eşit ağırlıklı evren getirisidir (XU100 / SPY değil); sinyal günü kapanışıyla bilinir.
BOŞLUK 9. İKİNCİL tanım haftalık tespit ızgarasıyla taranır (§1); ABD'de de üretim (BIST) sabitleriyle. Karara girmez.
BOŞLUK 10. ABD evreni V_ABD'dir (1.411 hisse; K24 cetvelinin evreni). K60'ın geniş evreni (4.666 hisse) bu işte kullanılmadı (penny / likit olmayan hisseler K24
  cetvelinde yoktu); istenirse ayrı ön kayıtla eklenir.
BOŞLUK 11. Maliyet sonrası şartta rastgele eş portföyler maliyetsizdir (tutucu). 20 günlük ölçüler bilgidir; karar 60 günlük eşli farkla verilir.
BOŞLUK 12. S2'de giriş birleşik takvimin ertesi günüdür (S1'de hissenin kendi ertesi işlem günü); S2 bilgi düzeyindedir.
BOŞLUK 13. fi_k24_tara içinde ileriye bakan SONUÇ sütunları (yon60, yon20, r120) hesaplanır; K64 bunları ALMAZ ve kullanmaz (fonksiyon değiştirilmediği için hesap sürer).
BOŞLUK 14. İşaret şartı: ölçülebilen hücrelerde nokta farkı tam sıfırsa işaret tutmaz sayılır.
SAPMA 15. KARAR SIRASI aile bazındadır (iş tanımındaki tek kural 'aynı gün evren içi sıra' idi): K64 ailesinde İÇ (çöl içi), K65 ailesinde EVREN. Gerekçe §4'te; karar
  ölçümden önce verildi: kapsam sayımı görüldü, getiri görülmedi. İşaret şartı ve dört şart sütunları da değişkenin karar sırasındaki hücrelerle hesaplanır.

## 12. Kapsam (yalnız SAYI; mühre girmez)
{kapsam}

## 13. Çıktılar ve komutlar
Çıktılar arastirma_cikti/col_dis_bilgi/: k64_olaylar.csv.gz (olay düzeyi), k64_s1.csv (hücre ölçüleri), k64_s1_fark.csv (ÜST - ALT, ek katkı), k64_s2.csv, k64_karar.csv,
k64_meta.json, K64_K65_RAPOR.md. Her değişken için raporda: veri kaynağı ve kapsamı, matematiksel tanım, örneklem, ortalama ve medyan getiri (20 ve 60 gün), eşli kontrol
farkı, güven aralığı, dönemler arası tutarlılık, maliyet sonrası sonuç, veri eksikleri, karar.
1. (ana oturum) bu dosyayı denetler ve git'e işler.
2. `python -I K64.py kos`  -> ölçüm + rapor (mühür, veri sha256, git doğrulanır)
3. `python K64.py rapor`   -> raporu çıktılardan yeniden yazar

## 14. Değişmezlik
K64_ESIK ya da içe alınan tanımlar (FI_K24, FI_OLCUT, K60 bilgi kuralı ve mührü, COL_v1 D13 / AL sabitleri) değişirse ESIK_SHA256 değişir ve koşu durur. Veri ya da
içe alınan kod dosyaları (FON_IZI.py, K60.py, COL_v1.py) değişirse sha256 tutmaz ve koşu durur.
"""


def _k64_onkayit_oku(yol: str) -> Dict[str, Any]:
    with open(yol, encoding="utf-8") as f:
        metin = f.read()
    m = re.search(r"^ESIK_SHA256: ([0-9a-f]{64})$", metin, re.M); z = re.search(r"^Yazım zamanı: (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC", metin, re.M)
    veri = {a: (h, int(n)) for a, h, n in re.findall(r"^- ([\w.\-]+): sha256 ([0-9a-f]{64}) \((\d+) dosya\)$", metin, re.M)}
    return {"sha": m.group(1) if m else None, "zaman_utc": z.group(1) if z else "", "veri": veri}


def k64_onkayit(cikti: Optional[str] = None, veri_sha: Optional[Dict[str, Tuple[str, int]]] = None) -> str:
    """Ön kaydı yazar. Dosya varsa ÜZERİNE YAZMAZ: mühür aynıysa yolu döndürür, değilse durur. veri_sha None ise veri özetleri hesaplanır (eksikse durur)."""
    yol = _k64_yol("onkayit", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True)
    if os.path.exists(yol):
        mevcut = _k64_onkayit_oku(yol)["sha"]
        if mevcut != k64_esik_sha():
            raise K64Hata(f"ön kayıt zaten var ve mühür farklı ({mevcut} != {k64_esik_sha()}): eşikler ön kayıttan sonra değişmiş")
        k64log.info("ön kayıt zaten var (mühür aynı): %s", yol)
        return yol
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    metin = k64_onkayit_metin(zaman, k64_veri_sha() if veri_sha is None else veri_sha, k64_kapsam_notu(cikti))
    if _K64_EPOSTA.search(metin):
        raise K64Hata("ön kayıt metninde e-posta biçimli parça var; yazılmadı")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k64log.info("ön kayıt yazıldı: %s (mühür %s)", yol, k64_esik_sha()[:12])
    return yol


def k64_onkayit_dogrula(cikti: Optional[str] = None, veri: bool = False, git: bool = False) -> Dict[str, Any]:
    """Mühür (her zaman), veri sha256'ları (veri=True) ve git'e işlenmişlik (git=True) doğrulanır; biri tutmazsa K64Hata."""
    yol = _k64_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise K64Hata(f"ön kayıt yok ({yol}): önce `python K64.py onkayit`")
    oc = _k64_onkayit_oku(yol)
    if oc["sha"] != k64_esik_sha():
        raise K64Hata(f"ön kayıt mührü tutmuyor ({oc['sha']} != {k64_esik_sha()}): eşikler ön kayıttan sonra değişmiş, koşu durdu")
    out = {"yol": yol, "sha": oc["sha"], "zaman_utc": oc["zaman_utc"], "dosya_sha256": K60._k60_sha(yol), "veri": oc["veri"]}
    if veri:
        simdi = k64_veri_sha()
        fark = sorted(k for k in set(simdi) | set(oc["veri"]) if simdi.get(k) != oc["veri"].get(k))
        if fark:
            raise K64Hata(f"veri / içe alınan kod ön kayıttakiyle aynı değil (sha256 ya da dosya sayısı farklı): {fark}; koşu durdu")
    if git:
        try:
            out["git"] = K60._k60_git_islenmis(yol, "K64 ön kaydı")
        except K60.K60Hata as ex:
            raise K64Hata(str(ex))
    return out


# ---------------------------------------------------------------- 7) KOŞU
def k64_kos(cikti: Optional[str] = None, git_sart: bool = True, girdi: Optional[Dict[str, Dict[str, Any]]] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Tek koşu: ön kayıt (mühür + git) -> [gerçek veride veri sha256 + K60 ön kaydı / verisi] -> olaylar -> değişkenler -> FI_OLCUT -> S1, S2 -> karar -> çıktılar +
    rapor. girdi / E yalnız testler içindir (sentetik girdi: veri sha256 doğrulaması atlanır; ön kayıt doğrulaması yine şarttır)."""
    Ek = E or K64_ESIK; sentetik = girdi is not None; t0 = time.time()
    oc = k64_onkayit_dogrula(cikti, veri=not sentetik, git=git_sart)
    meta: Dict[str, Any] = {"surum": K64_SURUM, "onkayit": oc, "sentetik": sentetik, "kos_baslangic": _k64_simdi(), "isolated": bool(sys.flags.isolated),
                            "k64_kod_sha256": K60._k60_sha(os.path.join(KOK_K64, "K64.py")) if os.path.exists(os.path.join(KOK_K64, "K64.py")) else None,
                            "surumler": {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}, "pazar": {}}
    if not sentetik:
        try:
            k60 = K60.k60_onkayit_dogrula(None, veri=True, git=False)
        except K60.K60Hata as ex:
            raise K64Hata(f"K60 ön kaydı / verisi doğrulanamadı: {ex}")
        meta["k60_muhur"] = k60["sha"]; girdi = k64_girdi(Ek, k60["veri"])
    olaylar, s1, frk, s2 = [], [], [], []
    for pazar in Ek["pazar"]:
        if pazar not in girdi:
            continue
        g = girdi[pazar]; V = g["V"]; H = k64_pazar_hazirla(pazar, V, g.get("T"), g.get("pay"), Ek)
        P = FI.fi_olcut_panel(V); P20 = FI.fi_olcut_panel(V, {**FI.FI_OLCUT, "ufuk": int(Ek["ek_ufuk"])}); F = k64_fark_matris(P)
        if list(P["sembol"]) != list(H["sembol"]) or not P["tarih"].equals(H["takvim"]):
            raise K64Hata(f"{pazar}: FI_OLCUT paneli ile değişken matrisleri aynı takvim / sembol sırasında değil")
        O = _k64_olaylar(pazar, V, Ek, None, None if sentetik else _k64_d13_ara(pazar)); meta["pazar"][pazar] = {**g.get("ozet", {}), "hisse": len(V), "gun": len(H["takvim"])}
        for tanim, X0 in O.items():
            X = k64_olay_degerleri(X0, H, tanim, Ek); n_ham = len(X); X = X[X.tekil & X.giris.notna()].reset_index(drop=True)
            if tanim == "D13" and Ek["olay"]["d13"]["gecer"] and len(X):
                X = X[X.gecer].reset_index(drop=True)
            X = k64_olc(P, P20, X) if len(X) else X.assign(r60=np.nan, esli_r60=np.nan, sira=np.nan, fark=np.nan, r20=np.nan, fark20=np.nan)
            X["pazar"] = pazar; X["tanim"] = tanim
            meta["pazar"][pazar][tanim] = {"ham": int(n_ham), "tekil": int(len(X)), "olculen": int(X.fark.notna().sum()) if len(X) else 0}
            a, b = k64_s1(X, pazar, tanim, Ek); s1.append(a); frk.append(b); olaylar.append(X.drop(columns=[c for c in ("_esler",) if c in X]))
            if tanim == Ek["olay"]["ana"]:
                s2.append(k64_s2(P, F, H, X0, pazar, Ek))
        k64log.info("%s ölçüldü (%.0f sn)", pazar, time.time() - t0)
    if not s1:
        raise K64Hata("ölçülecek pazar yok")
    S1 = pd.concat(s1, ignore_index=True); Fk = pd.concat(frk, ignore_index=True); S2 = pd.concat(s2, ignore_index=True) if s2 else pd.DataFrame(); Kr = k64_karar(Fk, Ek)
    cik = cikti or K64_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    pd.concat(olaylar, ignore_index=True).to_csv(_k64_yol("olay", cikti), index=False); S1.to_csv(_k64_yol("s1", cikti), index=False)
    Fk.to_csv(_k64_yol("fark", cikti), index=False); S2.to_csv(_k64_yol("s2", cikti), index=False); Kr.to_csv(_k64_yol("karar", cikti), index=False)
    meta["kos_bitis"] = _k64_simdi(); meta["sure_sn"] = round(time.time() - t0)
    with open(_k64_yol("meta", cikti), "w", encoding="utf-8") as f:
        json.dump(K60._k60_yuvarla(meta, 12), f, ensure_ascii=False, indent=1, default=str)
    return {"s1": S1, "fark": Fk, "s2": S2, "karar": Kr, "meta": meta, "rapor": k64_rapor(cikti, Ek)}


# ---------------------------------------------------------------- 8) RAPOR
def _k64_f(r: Any, k: str) -> float:
    try:
        v = r[k] if isinstance(r, dict) else getattr(r, k)
        return float(v) if v is not None and pd.notna(v) else np.nan
    except (KeyError, AttributeError, TypeError, ValueError):
        return np.nan


def _k64_yuz(x: Any, n: int = 1) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return ("%" + f"{100 * v:+.{n}f}".replace(".", ",")) if np.isfinite(v) else "—"


def _k64_tam(x: Any) -> int:
    try:
        return int(x) if np.isfinite(float(x)) else 0
    except (TypeError, ValueError):
        return 0


def _k64_evet(x: Any) -> bool:
    return str(x).strip().lower() in ("true", "1", "1.0")


def k64_rapor(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """K64_K65_RAPOR.md'yi çıktı dosyalarından yazar (her değişken için: tanım, kapsam, örneklem, 20 / 60 gün ortalama ve medyan, eşli fark, aralık, dönemler,
    maliyet sonrası, karar)."""
    E = E or K64_ESIK; yol = {k: _k64_yol(k, cikti) for k in ("s1", "fark", "s2", "karar", "meta")}
    if not all(os.path.exists(y) for y in yol.values()):
        raise K64Hata(f"K64 çıktıları yok ({yol['s1']}): önce `python -I K64.py kos`")
    S1 = pd.read_csv(yol["s1"]) if os.path.getsize(yol["s1"]) > 2 else pd.DataFrame(columns=["tanim", "pazar", "donem", "degisken", "sira_turu", "grup", "rejim"])
    S1[["degisken", "sira_turu"]] = S1[["degisken", "sira_turu"]].fillna(""); Fk = pd.read_csv(yol["fark"]) if os.path.getsize(yol["fark"]) > 2 else pd.DataFrame(columns=["degisken"])
    S2 = pd.read_csv(yol["s2"]) if os.path.getsize(yol["s2"]) > 2 else pd.DataFrame(); Kr = pd.read_csv(yol["karar"]) if os.path.getsize(yol["karar"]) > 2 else pd.DataFrame()
    with open(yol["meta"], encoding="utf-8") as f:
        m = json.load(f)
    ana = E["olay"]["ana"]; tn = {d["kod"]: d for d in E["degisken"]}
    par = [f"# K64 + K65 — çöl sinyaline ek bilgi: RAPOR\n\n{K64_SURUM}. Ön kayıt K64_K65_ON_KAYIT.md (mühür {str(m['onkayit']['sha'])[:12]}, dosya sha256 "
           f"{str(m['onkayit']['dosya_sha256'])[:12]}, git {str(m['onkayit'].get('git', {}).get('commit', ''))[:7]}); koşu {m['kos_baslangic']} -> {m['kos_bitis']} ({m.get('sure_sn')} sn).\n"]
    if len(Kr):
        par.append("## Karar tablosu (ANA tanım K24; karar sırası K64 ailesinde çöl içi, K65 ailesinde evren içi; yön = hangi üçte bir daha iyi)\n| değişken | yön | karar | ABD | BIST | ABD ek katkı (3 dönem) | BIST ek katkı | "
                   "ABD BH | işaret tutarlı | ABD grubu dört şart (brüt / net) |\n|---|---|---|---|---|---|---|---|---|---|")
        for r in Kr.to_dict("records"):
            par.append(f"| {r['degisken']} | {'ÜST' if r['yon'] == 'UST' else 'ALT'} | {r['karar']} | {r.get('ABD_karar', '—')} | {r.get('BIST_karar', '—')} | {r.get('ABD_ek', '—')} | "
                       f"{r.get('BIST_ek', '—')} | {r.get('ABD_bh', '—')} | {'evet' if _k64_evet(r['isaret_tutarli']) else 'hayır'} | "
                       f"{'evet' if _k64_evet(r.get('ABD_dort_sart')) else 'hayır'} / {'evet' if _k64_evet(r.get('ABD_dort_sart_net')) else 'hayır'} |")
        par.append(f"\nBH ailesi m = {int(Kr.aile_m.iloc[0])} ölçülebilen hipotez; q = %{100 * E['coklu']['bh_q']:.0f}. 'İZ' bu işte verilemez (Avrupa verisi yok).\n")
    T = S1[(S1.tanim == ana) & (S1.grup == "TEMEL") & (S1.rejim == "HEPSI")]
    par.append("## Temel model (yalnız çöl; değişkensiz)\n| pazar | dönem | n | ort. r60 | medyan r60 | ort. r20 | ort. eşli fark [%95] | medyan eşli fark | sıra | dört şart |\n|---|---|---|---|---|---|---|---|---|---|")
    for r in T.to_dict("records"):
        par.append(f"| {r['pazar']} | {r['donem']} | {_k64_tam(_k64_f(r, 'n'))} | {_k64_yuz(_k64_f(r, 'ort_r60'))} | {_k64_yuz(_k64_f(r, 'medyan_r60'))} | {_k64_yuz(_k64_f(r, 'ort_r20'))} | "
                   f"{_k64_yuz(_k64_f(r, 'ort_fark'))} [{_k64_yuz(_k64_f(r, 'alt95'))}; {_k64_yuz(_k64_f(r, 'ust95'))}] | {_k64_yuz(_k64_f(r, 'medyan_fark'))} | "
                   f"{_k64_f(r, 'sira'):.2f} | {'tutar' if _k64_evet(r.get('tutar')) else 'tutmaz'} |")
    for k in k64_kodlar(E):
        d = tn[k]; st = k64_karar_sirasi(k, E)
        par.append(f"\n## {k} ({d['aile']})\nTanım: {d['tanim']}. Kaynak / beklenti: {d['kaynak']}. Karar sırası: {'çöl içi (İÇ)' if st == 'IC' else 'evren içi (EVREN)'}; öteki sıra sağlamlık.\n")
        par.append("| pazar | dönem | grup | n | ort. r60 | medyan r60 | ort. r20 | medyan r20 | ort. eşli fark [%95] | medyan eşli fark | yarı genişlik | net eşli fark | dört şart (brüt / net) |\n"
                   "|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for r in S1[(S1.tanim == ana) & (S1.degisken == k) & (S1.sira_turu == st) & (S1.rejim == "HEPSI") & S1.grup.isin(["UST", "ALT"])].to_dict("records"):
            n = _k64_tam(_k64_f(r, "n"))
            par.append(f"| {r['pazar']} | {r['donem']} | {'ÜST' if r['grup'] == 'UST' else 'ALT'} | {n} | {_k64_yuz(_k64_f(r, 'ort_r60'))} | {_k64_yuz(_k64_f(r, 'medyan_r60'))} | "
                       f"{_k64_yuz(_k64_f(r, 'ort_r20'))} | {_k64_yuz(_k64_f(r, 'medyan_r20'))} | {_k64_yuz(_k64_f(r, 'ort_fark'))} [{_k64_yuz(_k64_f(r, 'alt95'))}; {_k64_yuz(_k64_f(r, 'ust95'))}] | "
                       f"{_k64_yuz(_k64_f(r, 'medyan_fark'))} | {_k64_yuz(_k64_f(r, 'yari_genislik'))} | {_k64_yuz(_k64_f(r, 'ort_fark_net'))} | "
                       f"{'tutar' if _k64_evet(r.get('tutar')) else 'tutmaz'} / {'tutar' if _k64_evet(r.get('tutar_net')) else 'tutmaz'} |")
        par.append("\n| tanım | sıra | pazar | dönem | n ÜST / ALT | ÜST - ALT [%95] | temel eşli fark | ek katkı | 20 gün ÜST - ALT |\n|---|---|---|---|---|---|---|---|---|")
        for r in Fk[Fk.degisken == k].to_dict("records"):
            ek = "ÖLÇÜLEMEZ" if not _k64_evet(r["olculebilir"]) else ("VAR (ÜST)" if _k64_evet(r["ek_UST"]) else ("VAR (ALT)" if _k64_evet(r["ek_ALT"]) else "yok"))
            par.append(f"| {r['tanim']} | {r['sira_turu']} | {r['pazar']} | {r['donem']} | {int(r['n_ust'])} / {int(r['n_alt'])} | {_k64_yuz(_k64_f(r, 'nokta'))} [{_k64_yuz(_k64_f(r, 'alt'))}; "
                       f"{_k64_yuz(_k64_f(r, 'ust'))}] | {_k64_yuz(_k64_f(r, 'ort_temel'))} | {ek} | {_k64_yuz(_k64_f(r, 'nokta20'))} |")
        if len(S2):
            par.append("\nS2 (çöl dışı evren; bilgi): " + "; ".join(f"{r['pazar']} {r['donem']} ÜST - ALT {_k64_yuz(_k64_f(r, 'nokta'))} [{_k64_yuz(_k64_f(r, 'alt'))}; {_k64_yuz(_k64_f(r, 'ust'))}] "
                                                                     f"(n {_k64_tam(_k64_f(r, 'n_ust'))} / {_k64_tam(_k64_f(r, 'n_alt'))})" for r in S2[S2.degisken == k].to_dict("records")))
        Rj = S1[(S1.tanim == ana) & (S1.degisken == k) & (S1.rejim != "HEPSI")]
        if len(Rj):
            par.append("\nPiyasa koşulu (bilgi): " + "; ".join(f"{r['pazar']} {r['donem']} {'endeks ort. üstü' if r['rejim'] == 'UST200' else 'endeks ort. altı'} "
                                                               f"{'ÜST' if r['grup'] == 'UST' else 'ALT'} n {_k64_tam(_k64_f(r, 'n'))} eşli fark {_k64_yuz(_k64_f(r, 'ort_fark'))}" for r in Rj.to_dict("records")))
    par.append("\n## Veri eksikleri ve sınırlar\nBIST PAY_D: BIST VERİSİ YOK. Banka / sigorta şablonundaki şirketlerde BIST kalemleri yok. ABD FCF yıllık. İki evren de yalnız yaşayanlar "
               "(yaşayan yanlılığı; ön kayıt §10). 'ÖLÇÜLEMEZ' = hücrede n < 30 (az veri), 'İZ DEĞİL' değildir. Ayrıntı: K64_K65_ON_KAYIT.md §9-§11; koşu sayıları k64_meta.json.\n")
    metin = "\n".join(par); y = _k64_yol("rapor", cikti)
    if _K64_EPOSTA.search(metin):
        raise K64Hata("rapor metninde e-posta biçimli parça var; yazılmadı")
    with open(y, "w", encoding="utf-8") as f:
        f.write(metin)
    k64log.info("rapor: %s", y)
    return y


def _cakisma_kontrol_k64(_once=_CK_ONCE_K64, _dosya="K64.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K64", "_CK_KAYIT", "_cakisma_kontrol_k64", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "io", "pickle", "hashlib", "contextlib", "_dt", "annotations", "Any", "Callable", "Dict", "List",
           "Optional", "Tuple", "FI", "K60", "K57")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k64()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=K64_SURUM)
    ap.add_argument("komut", choices=["onkayit", "indir", "kapsam", "kos", "rapor"])
    ap.add_argument("--cikti", default=None)
    a_ = ap.parse_args()
    try:
        if a_.komut == "onkayit":
            y_ = k64_onkayit(a_.cikti); print(y_, "mühür", k64_esik_sha(), "dosya sha256", K60._k60_sha(y_))
        elif a_.komut == "indir":
            print(json.dumps(k64_isy_indir(sorted(k64_fiyat_yukle("BIST"))), ensure_ascii=False))
        elif a_.komut == "kapsam":
            K_ = k64_kapsam(a_.cikti); print(K_[K_.degisken == "(olay)"].to_string(index=False)); print(_k64_yol("kapsam", a_.cikti))
        elif a_.komut == "kos":
            R_ = k64_kos(a_.cikti); print("K64 bitti:", json.dumps({"sure_sn": R_["meta"]["sure_sn"], "pazar": R_["meta"]["pazar"]}, ensure_ascii=False, default=str))
            print(R_["karar"].to_string(index=False) if len(R_["karar"]) else "(karar tablosu boş)"); print(R_["rapor"])
        else:
            print(k64_rapor(a_.cikti))
    except (K64Hata, K60.K60Hata, FileNotFoundError) as ex:
        k64log.error("%s", ex); sys.exit(1)
