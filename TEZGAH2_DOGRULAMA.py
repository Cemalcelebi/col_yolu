"""TEZGAH2_DOGRULAMA — TEZGÂH 2 DOĞRULAMA: büyütülmüş tezgâh (ABD bugün yaşayan bütün adi hisseler + AVR 574 hisse, 2000-01 .. 2023-12)
yayımlanmış serileri (Kenneth French) ay ay izliyor mu, ve hangi HAVUZ SÜZGECİYLE (P1 / P2 / P3)? İz ARANMAZ; yalnız doğrulama ve havuz
seçimi (22 Kasım 2026).

İş tanımı: arastirma_cikti/tezgah2/TEZGAH2_DOGRULAMA_IS_TANIMI.md.
Veri: hisse fiyatı YALNIZ /tmp/kasa2/acik (V_ABD.pkl -> V_ABD2.pkl, V_AVR.pkl -> V_AVR2.pkl; KASA 2 açık kesik 2023-12-31); her adımdan önce
  KASA.kasa_kapisi (hisse pkl + kesilmiş referans pkl'leri). ORTAK_CETVEL.oc_veri, OS.os_veri üzerinden veri2 = var olmayan klasörle çağrılır:
  k34_yahoo KULLANILMAZ.
Referans: Kenneth French (TEZGAH_DOGRULAMA'nın indirip kestiği /tmp/claude-0/tezgah_ref/ref_kesik.pkl; yoksa TD.td_ref_indir ile aynı kod)
  + AVR USD çevirimi için EURUSD: FRED DEXUSEU (günlük, 1999+, kimliksiz curl; /tmp/claude-0/tezgah2_ref/), 2023-12-31'de kesilir.
Panel / seriler: OLCU_SINAMA (os_veri, os_panel, os_prefix, os_kart_sinyal, os_olcu_matris) ve TEZGAH_DOGRULAMA (td_kesit, td_piyasa,
  td_portfoy, td_karsilastir, td_hukum, td_french_elle) İÇE ALINIR, kopyalanmaz.

Komut:  python TEZGAH2_DOGRULAMA.py ref        EURUSD (FRED) indir + kes; French kesik dosyası yoksa TD koduyla indir
        python TEZGAH2_DOGRULAMA.py hazirlik   KASA kapısı -> panel (getirisiz) -> kova sınırları + EVREN PREFIX TESTİ + havuz sayımları
                                               -> arastirma_cikti/tezgah2/tezgah2_hazirlik.json (prefix tutmazsa DURUR)
        python TEZGAH2_DOGRULAMA.py onkayit    TEZGAH2_DOGRULAMA_ON_KAYIT.md
        python TEZGAH2_DOGRULAMA.py kos        kapılar (KASA, ön kayıt git + sha + kontrol) -> seriler -> karşılaştırma -> seçim -> json + rapor
        python TEZGAH2_DOGRULAMA.py rapor      TEZGAH2_DOGRULAMA_RAPOR.md (json'dan)
Sonraki ajan için arayüz: t2_secili_panel(pazar) -> {'Vd', 'Pn', 'havuz' (seçilen havuz maskesi, gün x hisse), 'ad'}.
Colab:  exec(open('TEZGAH2_DOGRULAMA.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_T2 = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_T2 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_T2 not in sys.path:
    sys.path.insert(0, KOK_T2)

import OLCU_SINAMA as OS  # noqa: E402  (nedensel panel; DEĞİŞTİRİLMEZ, yalnız çağrılır)
import TEZGAH_DOGRULAMA as TD  # noqa: E402  (kesit / portföy / karşılaştırma; DEĞİŞTİRİLMEZ, yalnız çağrılır)

t2log = logging.getLogger("col.tezgah2_dogrulama")
if not t2log.handlers:
    _t2_h = logging.StreamHandler(sys.stderr)
    _t2_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s tezgah2_dogrulama: %(message)s", "%H:%M:%S"))
    t2log.addHandler(_t2_h)
    t2log.setLevel(logging.INFO)
    t2log.propagate = False

T2_SURUM = "TEZGAH2_DOGRULAMA v1.0 (2026-11-22)"
T2_YOL = {"cikti": os.path.join(KOK_T2, "arastirma_cikti", "tezgah2"), "veri": os.environ.get("T2_VERI", "/tmp/kasa2/acik"),
          "kasa_dizin": os.environ.get("T2_KASA_DIZIN", "/tmp/kasa2"), "ref_td": os.environ.get("TD_REF", "/tmp/claude-0/tezgah_ref"),
          "ref2": os.environ.get("T2_REF", "/tmp/claude-0/tezgah2_ref"), "kod": os.path.join(KOK_T2, "TEZGAH2_DOGRULAMA.py"),
          "is_tanimi": os.path.join(KOK_T2, "arastirma_cikti", "tezgah2", "TEZGAH2_DOGRULAMA_IS_TANIMI.md"),
          "eski_json": os.path.join(KOK_T2, "arastirma_cikti", "tezgah_dogrulama", "tezgah_dogrulama.json")}
T2_DOSYA = {"onkayit": "TEZGAH2_DOGRULAMA_ON_KAYIT.md", "rapor": "TEZGAH2_DOGRULAMA_RAPOR.md", "json": "tezgah2_dogrulama.json",
            "hazirlik": "tezgah2_hazirlik.json", "eurusd_csv": "DEXUSEU.csv", "eurusd_kesik": "eurusd_kesik.pkl", "ref2_durum": "ref2_durum.json"}
T2_HAVUZ = ["P1", "P2", "P3"]

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
T2_ESIK: Dict[str, Any] = {
    "surum": "T2-1.0",
    "kesik": "2023-12-31",
    "veri": {"klasor": "/tmp/kasa2/acik (V_ABD.pkl -> V_ABD2.pkl, V_AVR.pkl -> V_AVR2.pkl); başka fiyat kaynağı YOK",
             "yukle": "OS.os_veri(pazar, klasor) = OC.oc_veri(min_bar 1, abd_ek_aktif False, veri2 = '/nonexistent_os_k34_yok'): k34_yahoo "
                      "KULLANILMAZ; geçerli bar süzgeci + ABD evren dışı (fon / ETF) listesi + açılış kırpması",
             "kapi": "KASA.kasa_kapisi(V_ABD2.pkl, V_AVR2.pkl; cikti /tmp/kasa2) + /tmp/kasa2/acik/KASA_DURUM.json açık kesik = 2023-12-31; "
                     "referans pkl'leri (ref_kesik, yahoo_kesik, eurusd_kesik) aynı kesikle"},
    "havuz": {
        "metin": "P1 = OLCU_SINAMA havuzu olduğu gibi (alt %20 likidite dışı, bölünme şüphesi dışı). P2 = P1 + ABD'de kapanış >= 2 $ (AVR'de "
                 ">= 1 EUR karşılığı) + son 20 gün medyan işlem değeri >= 1 mn $ (AVR 1 mn EUR). P3 = P2 + son 250 barda |günlük getiri| > %50 "
                 "olan ve 3 bar içinde en az yarısını geri veren (sıçra-geri dön) bir bar varsa o hisse-gün dışı (nedensel: yalnız d-1'e "
                 "kadarki barlar).",
        "P1": "OS paneli: ok (d günü geçerli bar, kendi 80. geçerli barından sonra, momentum60 ve likidite sonlu, alt %20 likidite dışı, "
              "nedensel bölünme şüphesi dışı) VE H >= 0 (5 x 3 kova; günde >= 30 hisse)",
        "P2": "P1 VE d'den önceki son geçerli kapanış x Kur >= fiyat_min (ABD 2 USD; AVR 1 EUR; Kur = yerel -> EUR) VE Lq (C x V x Kur, d'den "
              "önceki 20 birleşik takvim gününün medyanı, en az 10 gün; OS paneli) >= likidite_min (ABD 1e6 USD; AVR 1e6 EUR)",
        "P3": "P2 VE değil SG: hissenin kendi geçerli barlarında (değer = Close x Kur) bar i sıçrama = |C_i / C_{i-1} - 1| > 0,50; geri dönüş = "
              "i+1..i+3 barlarının ilkinde (C_i - C_{i+k}) / (C_i - C_{i-1}) >= 0,50 (fiyat farkının en az yarısı geri), c = o ilk bar; "
              "hisse-gün d dışı <=> nb(d) (d'den önceki geçerli bar sayısı) [c+1, i+250] aralığında (onay barı c <= d-1 VE sıçrama barı "
              "son 250 bar içinde); birleşik takvimde satır (pos[c], pos[i+250]] (i+250 veri sonunu aşıyorsa sona kadar)",
        "fiyat_min": {"ABD": 2.0, "AVR": 1.0}, "likidite_min": {"ABD": 1e6, "AVR": 1e6},
        "sg": {"sicrama": 0.50, "geri_bar": 3, "geri_pay": 0.50, "pencere": 250},
        "sayim_yil": [2000, 2005, 2010, 2015, 2020, 2023],
        "kova_sinir": "KV1 / KV2 sınırları OS kuralıyla (os_kova_sinir: P1 havuzu, giriş 2016-22, getirisiz) BU veride hazırlıkta hesaplanır, "
                      "tezgah2_hazirlik.json'a ve ön kayda yazılır, koşuda aynı sayılar verilir"},
    "prefix": {"kisa": "2015-06-30", "uzun": "2023-12-29", "son": "2015-05-29",
               "tanim": "iki kesikte panel: OS.os_prefix (ok, H, KV1, KV2, sup, lik_alt, evren, ATRP, F15, Lq, M, kart olay kümeleri) + P1 / P2 / "
                        "P3 maskeleri; sinyal / havuz günü <= 2015-05-29 olan bütün hisse-günlerde fark 0 beklenir, değilse DURUR"},
    "donem": {"tum": ["2000-07", "2023-12"], "d1": ["2001-01", "2007-12"], "d2": ["2008-01", "2015-12"], "d3": ["2016-01", "2023-12"],
              "tarih": "TUTMA ayı (getirinin ölçüldüğü ay); ilk aylar 12-1 momentum için ısınma (MOM serileri ~2001-02'den)"},
    "seri": "TD_CIFT (A1-A8 ABD, E1-E4 AVR) aynen; 'havuz' maskesi yerine P1 / P2 / P3; getiri r = ay kapanışından ay kapanışına (AVR USD: "
            "Close x Kur x EURUSD ay son kuru); onluk / 2x3 / ağırlık tanımları TD_ESIK['bizim'] aynen",
    "eurusd": {"kaynak": "FRED DEXUSEU (https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU), günlük USD / EUR, kimliksiz curl",
               "ay": "ayın son geçerli gözlemi", "kesik": "<= 2023-12-31", "denetim": "Yahoo EURUSD=X (TD yahoo_kesik, 2015-23) ay sonu ile "
               "aylık değişim korelasyonu ve en büyük seviye farkı raporlanır (bilgi)"},
    "hukum": {"metin": "HÜKÜM: DOĞRU = korelasyon >= 0,70 ve işaret uyumu >= %70 (piyasa >= 0,90); KISMEN 0,40-0,70; UYUŞMUYOR < 0,40.",
              "kod": "TD.td_hukum aynen (Pearson; DOĞRU eşiği geçilip işaret uyumu < %70 ise KISMEN; piyasa 0,40-0,90 KISMEN; n < 36 ay ÖLÇÜLEMEDİ)"},
    "secim": {"metin": "HAVUZ SEÇİM KURALI (sonuç görülmeden): seçilen havuz = bütün ana serilerde (piyasa, momentum 2x3, dönüş 2x3; ABD üç dönem "
                       "+ AVR) DOĞRU olanlar arasında EN GENİŞ olan (P1 > P2 > P3 sırası: önce P1); hiçbiri tam geçmezse en çok seri geçen ve "
                       "neden / hangi dönem düştüğü raporlanır.",
              "kume": {"ABD": ["A1", "A2", "A5", "A8"], "AVR": ["E1", "E2", "E3"], "donem": ["d1", "d2", "d3"]},
              "yorum": "ana seriler = ABD piyasa EW (A1) ve işlem değeri ağırlıklı (A2), MOM 2x3 (A5), STREV 2x3 (A8) x üç alt dönem (d1 2001-07, "
                       "d2 2008-15, d3 2016-23) + AVR piyasa LQ (E1) ve EW (E2), WML 2x3 (E3) x aynı üç alt dönem = havuz başına 21 hüküm. "
                       "'AVR' de üç dönemde sınanır (üç alt dönem ayrı ayrı şartı bütün serilere uygulanır). Yedek: en çok DOĞRU; eşitlikte "
                       "geniş olan (P1 > P2 > P3). Onluk farkları (A3, A4, A6, A7, E4) ve 'tum' dönemi bilgi; seçime girmez."},
    "sonuc": {"kural": "tek cümle (seçilen havuz): 12 ana çift x üç alt dönem hepsi DOĞRU ise 'geniş tezgâh yayımlanmış serileri izliyor'; biri "
                       "UYUŞMUYOR ise 'geniş tezgâhta / evrende fark var' (hangi seri / dönem); aksi 'kısmen izliyor' (DOĞRU olmayanlar)"},
    "eski": {"tanim": "seçilen havuzun (ve bilgi olarak P1'in) A1-A8, E1-E4 serileri ile eski tezgâhın (Ç207, 1.380 ABD + 576 AVR hisse; "
                      "tezgah_dogrulama.json 'seriler' ABD|havuz|r|...) aynı seriler arasında Pearson korelasyonu ve ortalama farkı, tutma ayı "
                      "2016-01..2023-12; eski hisse listesi açık kasa dışında olmadığı için yeni veride 1.401 ortak sembole kısıtlama yapılmaz"},
    "ek": {"sayim": "seçilen havuzda yıl başına hisse-gün sayısı; likidite üst / alt yarı payı = o gün taban (geçerli bar, evrende, Lq sonlu) "
                    "hisselerinin Lq medyanının üstünde / altında kalan havuz hisse-günleri payı",
           "es_sd": "seçilen havuz, H = 15 ve 30: R_H (OS.os_olcu_matris: giriş barı açılışı E0, H. geçerli barın kapanışı / E0 - 1, 2H satır "
                    "kuralı) her hisse-gün için; eş-farkı = R_H - aynı giriş günü d ve aynı KV1 kovasındaki (seçilen havuz içinde, KV1 >= 0, "
                    "R_H sonlu) öteki hisselerin R_H ortalaması (kendisi hariç; en az 5 eş); dağılım: n, ortalama, standart sapma, IQR / 1,349, "
                    "p01 / p05 / p50 / p95 / p99; pazar x alt dönem (giriş günü yılı: d1 2001-07, d2 2008-15, d3 2016-23); hipotez yok"},
    "yeniden": {"seri": ["ABD|tum|r|MOM|D10-D1|EW", "ABD|tum|r|PIYASA|-|EW"], "ay": ["2003-05", "2011-09", "2020-04"],
                "tanim": "ham V_ABD2.pkl'den düz pandas (OC / OS / TD kodu kullanmadan; TD.td_yeniden mantığı, ay listesi farklı): geçerli bar "
                         "süzgeci, K55 + evren_disi fon listesi dışı, birleşik takvim ay sonu, MOM kendi bar indeksiyle, rank(first, pct), ceil "
                         "onluk, ay kapanışı getirisi; fark < 1e-9 TUTAR; French ham satırı TD.td_french_elle"},
}

T2_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "iz / sinyal sınaması yok; doğrulama: bizim aylık portföy serileri = yayımlanmış French serileriyle ay ay; dış referans "
                         "kontrol yerine geçer; eş-farkı SD yalnız dağılım genişliği (OS eş kuralı: aynı gün, aynı KV1, kendisi hariç, >= 5 eş)"),
    "K2": ("EVET", "sıralama t kapanışında bilinenle (MOM C_{k-21}/C_{k-252}, STREV C_k/C_{k-21}); havuz giriş günü d'de yalnız d-1'e kadarki "
                   "barlarla (P2 fiyatı shift(1), Lq shift(1), P3 onay barı <= d-1); EVREN PREFIX TESTİ (2015-06-30 / 2023-12-29, <= 2015-05-29 "
                   "fark 0) P1 / P2 / P3 dahil; KASA 2 kapısı hisse + referans pkl (2023-12-31)"),
    "K3": ("EVET", "OS.os_veri -> OC.oc_veri_hazirla geçerli bar (O/H/L/C > 0, H > L, V > 0); ay sonu t'de geçerli bar (os_kart_sinyal); P3 "
                   "yalnız geçerli barların Close x Kur'u"),
    "K4": ("UYGULANMAZ", "olay yok; ay başına bir portföy getirisi; eş-farkı SD hisse-gün dağılımı (karar dışı, n bağımsız olay iddiası yok)"),
    "K5": ("EVET", "birincil getiri French ile aynı kip (ay kapanışından ay kapanışına); eş-farkı R_H giriş barı açılışı E0'dan (OS)"),
    "K6": ("EVET", "V_*2.pkl tek kip (auto_adjust; TEZGAH2_VERI raporu); AVR Close x Kur (EUR) x EURUSD (FRED, ay son) = USD; P2 fiyat eşiği "
                   "EUR karşılığı; P3 Close x Kur ile (Londra peni / sterlin birim sıçraması sayılmaz); French yüzde -> ondalık"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batan yok; ABD 2000 aktif = 2025'in %31'i): seviye getirileri ve alt onluklar yukarı "
                   "yanlı, 2000-15 daha çok; raporda yazılı; korelasyon / ortalama ayrı okunur"),
    "K8": ("EVET", "üç alt dönem (2001-07, 2008-15, 2016-23) ayrı hüküm; n < 36 ay ÖLÇÜLEMEDİ; havuz seçimi 21 hükmün hepsi"),
    "K9": ("EVET", "T2_ESIK sha + kod sha + git commit, hazırlık json sha (kova sınırı, prefix), referans sha'ları ön kayıtta; sıra kod commit -> "
                   "hazırlık (getirisiz) -> ön kayıt commit -> koşu; t2_kapi ön kaydın işlenmiş + değişmemiş + sha eşit + ik_kontrol_kapisi; "
                   "havuz tanımı, hüküm ve seçim kuralı iş tanımından aynen"),
    "K10": ("EVET", "French ayrıştırma TD.td_french_ayristir (Ç207'de sınandı) + TD.td_french_elle ham satır 4 hücre; FRED CSV: başlık + "
                    "tarih,değer; '.' / boş eksik; 3 satır ham metinden elle (rapor)"),
    "K11": ("EVET", "t2_yeniden: 2 seri x 3 ay ham V_ABD2.pkl'den düz pandas (OC / OS / TD kodu yok) + French 4 satır; tutmazsa rapor TUTMADI"),
    "K12": ("EVET", "iz iddiası yok; hüküm ve seçim yalnız önceden yazılı eşik / kuralla; sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_t2; test); OS / TD / OC / KASA / TEZGAH2_VERI / defter / kart / kasa dosyalarına dokunulmadı; "
                    "dış istek yalnız FRED (+ gerekirse French; kimlik yok, Tiingo yok); e-posta / anahtar taraması (_t2_yaz)"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; tezgâh doğrulaması"),
}


class T2Hata(RuntimeError):
    """Durdurucu hata: veri / referans yok, kasa / ön kayıt kapısı kapalı, prefix tutmuyor, ayrıştırma bozuk."""


# ================================================================ 0) ORTAK
_T2_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_T2_ANAHTAR = re.compile(r"(?i)(api[_-]?key|token|secret|password|sifre)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")


def _t2_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def t2_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    s = json.dumps(T2_ESIK if E is None else E, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _t2_yol(ad: str, kl: Optional[str] = None) -> str:
    if ad in ("eurusd_csv", "eurusd_kesik", "ref2_durum"):
        return os.path.join(kl or T2_YOL["ref2"], T2_DOSYA[ad])
    return os.path.join(kl or T2_YOL["cikti"], T2_DOSYA.get(ad, ad))


def _t2_yaz(yol: str, metin: str, ad: str = "dosya") -> str:
    """Metin dosyası yazar; e-posta / anahtar deseni varsa DURUR (K13)."""
    if _T2_EPOSTA.search(metin) or _T2_ANAHTAR.search(metin):
        raise T2Hata(f"{ad}: e-posta / anahtar deseni bulundu, yazılmadı ({yol})")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    t2log.info("%s yazıldı: %s", ad, yol)
    return yol


def _t2_json_yaz(yol: str, J: Any, ad: str) -> str:
    return _t2_yaz(yol, json.dumps(OS._os_temizle(J), ensure_ascii=False, indent=1, default=OS._os_json), ad)


def _per(a: str, b: str) -> Tuple[pd.Period, pd.Period]:
    return pd.Period(a, "M"), pd.Period(b, "M")


# ================================================================ 1) REFERANS (EURUSD; French TD'den)
def t2_fred_ayristir(metin: str) -> pd.Series:
    """FRED fredgraph CSV ('observation_date,DEXUSEU' ya da 'DATE,DEXUSEU') -> günlük Series (DatetimeIndex); '.' / boş eksik atılır."""
    sat = [s.strip() for s in metin.splitlines() if s.strip()]
    if not sat or "," not in sat[0] or "DEXUSEU" not in sat[0].upper():
        raise T2Hata(f"FRED: beklenmeyen başlık {sat[:1]}")
    ix, val = [], []
    for s in sat[1:]:
        p = [x.strip() for x in s.split(",")]
        if len(p) != 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", p[0]):
            raise T2Hata(f"FRED: bozuk satır {s[:60]}")
        if p[1] in ("", "."):
            continue
        ix.append(pd.Timestamp(p[0])); val.append(float(p[1]))
    x = pd.Series(val, index=pd.DatetimeIndex(ix), name="EURUSD").sort_index()
    if x.index.duplicated().any() or (x <= 0).any():
        raise T2Hata("FRED: yinelenen tarih ya da pozitif olmayan kur")
    return x


def t2_ref_indir(kl: Optional[str] = None) -> Dict[str, Any]:
    """EURUSD (FRED DEXUSEU) indir + kes (<= 2023-12-31) -> eurusd_kesik.pkl + ref2_durum.json. French kesik dosyası yoksa TD koduyla indirilir."""
    kl = kl or T2_YOL["ref2"]; os.makedirs(kl, exist_ok=True)
    if not os.path.exists(TD._td_yol("ref_kesik", T2_YOL["ref_td"])):
        t2log.info("French kesik dosyası yok: TD.td_ref_indir ile indiriliyor")
        TD.td_ref_indir(T2_YOL["ref_td"])
    csv = _t2_yol("eurusd_csv", kl)
    ok, msg = TD._td_curl("https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU", csv)
    if not ok:
        raise T2Hata(f"FRED DEXUSEU erişilemedi: {msg}")
    x = t2_fred_ayristir(open(csv, encoding="utf-8").read())
    x = x[x.index <= pd.Timestamp(T2_ESIK["kesik"])]
    pd.to_pickle({"eurusd": x.to_frame()}, _t2_yol("eurusd_kesik", kl))
    ay = x.groupby(x.index.to_period("M")).last()
    durum: Dict[str, Any] = {"zaman": _t2_simdi(), "kaynak": T2_ESIK["eurusd"]["kaynak"], "n_gun": int(len(x)), "ilk": str(x.index.min().date()),
                             "son": str(x.index.max().date()), "csv_sha": OS._os_sha_dosya(csv), "kesik_sha": OS._os_sha_dosya(_t2_yol("eurusd_kesik", kl)),
                             "ham_ornek": [s for s in open(csv, encoding="utf-8").read().splitlines() if s.startswith(("2003-05-30", "2011-09-30", "2020-04-30"))]}
    try:   # Yahoo EURUSD=X (TD) ile karşılaştırma (bilgi)
        _, Y = TD.td_ref_yukle(T2_YOL["ref_td"])
        yf = TD.td_eurusd_ay(Y)
        if yf is not None:
            D = pd.concat({"fred": ay, "yahoo": yf}, axis=1).dropna()
            durum["yahoo_karsilastirma"] = {"n_ay": int(len(D)), "ilk": str(D.index.min()), "son": str(D.index.max()),
                                            "degisim_korelasyon": float(D.pct_change().dropna().corr().iloc[0, 1]),
                                            "maks_seviye_fark_pct": float(((D.fred / D.yahoo - 1).abs().max()) * 100)}
    except Exception as ex:   # karşılaştırma bilgi amaçlı; ölçümü durdurmaz
        durum["yahoo_karsilastirma"] = {"durum": f"yapılamadı ({type(ex).__name__}: {ex})"}
    _t2_json_yaz(_t2_yol("ref2_durum", kl), durum, "EURUSD durumu")
    return durum


def t2_eurusd_ay(kl: Optional[str] = None) -> pd.Series:
    x = pd.read_pickle(_t2_yol("eurusd_kesik", kl))["eurusd"]["EURUSD"]
    return x.groupby(x.index.to_period("M")).last()


def t2_kasa_kapi(veri: Optional[str] = None) -> Dict[str, Any]:
    """KASA 2: açık kesik = 2023-12-31; hisse pkl'leri ve kesilmiş referans pkl'leri kesiği aşmıyor."""
    import KASA as _KS
    v = veri or T2_YOL["veri"]
    try:
        dur = _KS._durum_oku(T2_YOL["kasa_dizin"])
    except Exception as ex:   # kasa durumu okunamazsa ölçüm başlamaz (fail-closed)
        raise T2Hata(f"KASA 2 durumu okunamadı: {type(ex).__name__}: {ex}") from ex
    if pd.Timestamp(dur["acik_kesik"]) != pd.Timestamp(T2_ESIK["kesik"]):
        raise T2Hata(f"KASA 2 açık kesik {dur['acik_kesik']} != {T2_ESIK['kesik']} -> DURDU")
    hisse = [os.path.join(v, f) for f in ("V_ABD2.pkl", "V_AVR2.pkl")]
    for p in ("ABD", "AVR"):   # OS / OC V_<pazar>.pkl okur: V_<pazar>2.pkl'ye bağlantı olmalı
        y = os.path.join(v, f"V_{p}.pkl")
        if not os.path.exists(y) or os.path.realpath(y) != os.path.realpath(os.path.join(v, f"V_{p}2.pkl")):
            raise T2Hata(f"{y} -> V_{p}2.pkl bağlantısı yok (başka veri okunabilir) -> DURDU")
    ref = [TD._td_yol("ref_kesik", T2_YOL["ref_td"]), TD._td_yol("yahoo_kesik", T2_YOL["ref_td"]), _t2_yol("eurusd_kesik")]
    eksik = [y for y in hisse + ref if not os.path.exists(y)]
    if eksik:
        raise T2Hata(f"dosya yok: {eksik} (önce 'ref')")
    try:
        r1 = _KS.kasa_kapisi(hisse, cikti=T2_YOL["kasa_dizin"])
        r2 = _KS.kasa_kapisi(ref, kesik=T2_ESIK["kesik"], cikti=T2_YOL["kasa_dizin"])
    except Exception as ex:
        raise T2Hata(f"KASA 2 kapısı KAPALI: {ex}") from ex
    return {"durum": dur, "hisse": r1, "referans": r2}


# ================================================================ 2) HAVUZLAR (P1 / P2 / P3; nedensel)
def t2_sg_disi(pos: np.ndarray, CK: np.ndarray, n: int, E: Dict[str, Any] = T2_ESIK) -> np.ndarray:
    """Hissenin kendi geçerli barları (birleşik takvim konumu pos, değer CK = Close x Kur) -> P3 dışı birleşik takvim satırları (bool, nedensel)."""
    G = E["havuz"]["sg"]; out = np.zeros(n, bool); m = len(CK)
    if m < 3:
        return out
    with np.errstate(all="ignore"):
        r = CK[1:] / CK[:-1] - 1
    for i in np.flatnonzero(np.abs(r) > G["sicrama"]) + 1:
        d0 = CK[i] - CK[i - 1]
        c = None
        for k in range(1, int(G["geri_bar"]) + 1):
            if i + k >= m:
                break
            if (CK[i] - CK[i + k]) / d0 >= G["geri_pay"]:
                c = i + k
                break
        if c is None:
            continue
        son = int(pos[i + G["pencere"]]) if i + G["pencere"] < m else n - 1
        out[int(pos[c]) + 1:son + 1] = True
    return out


def t2_havuz(Pn: Dict[str, Any], Vd: Dict[str, Any], E: Dict[str, Any] = T2_ESIK) -> Dict[str, np.ndarray]:
    """P1 / P2 / P3 maskeleri (gün x hisse, bool) + SG (sıçra-geri dışı) — yalnız d-1'e kadarki bilgi."""
    pz = Pn["pazar"]; idx = Pn["tarih"]; S = Pn["sembol"]; n, u = len(idx), len(S); V = Vd["V"]; dep = Pn["dep"]
    P1 = Pn["ok"] & (Pn["H"] >= 0)
    CK = pd.DataFrame({s: V[s].Close * V[s].Kur for s in S}).reindex(idx).ffill().shift(1).to_numpy(float)
    with np.errstate(invalid="ignore"):
        P2 = P1 & (CK >= E["havuz"]["fiyat_min"][pz]) & (Pn["Lq"] >= E["havuz"]["likidite_min"][pz])
    del CK
    SG = np.zeros((n, u), bool)
    for j, s in enumerate(S):
        a, b = dep["off"][j], dep["off"][j + 1]
        ck = (V[s].Close * V[s].Kur).to_numpy(float)
        if len(ck) != b - a:
            raise T2Hata(f"{s}: bar deposu ile veri uzunluğu farklı")
        SG[:, j] = t2_sg_disi(dep["POS"][a:b], ck, n, E)
    return {"P1": P1, "P2": P2, "P3": P2 & ~SG, "SG": SG}


def t2_sayim(Pn: Dict[str, Any], M: Dict[str, np.ndarray], E: Dict[str, Any] = T2_ESIK) -> Dict[str, Any]:
    """Havuz başına yıl yıl: hisse sayısı (yılda en az bir gün havuzda), günlük ortalama, hisse-gün; likidite üst / alt yarı payı."""
    idx = Pn["tarih"]; yil = idx.year.to_numpy(); Lq = Pn["Lq"]
    taban = Pn["gec"] & Pn["evren"] & np.isfinite(Lq)
    with np.errstate(all="ignore"):
        med = np.array([np.median(Lq[d, taban[d]]) if taban[d].any() else np.nan for d in range(len(idx))])
        ust = Lq >= med[:, None]
    out: Dict[str, Any] = {"pazar": Pn["pazar"], "hisse_toplam": len(Pn["sembol"]), "havuz": {}}
    for hv in T2_HAVUZ:
        m = M[hv]; sat = {}
        for y in sorted(set(yil.tolist())):
            r = yil == y; my = m[r]
            hg = int(my.sum())
            sat[str(y)] = {"hisse": int(my.any(axis=0).sum()), "gunluk_ort": float(my.sum(axis=1).mean()), "hisse_gun": hg,
                           "lik_ust_pay": float((my & ust[r]).sum() / hg) if hg else float("nan")}
        out["havuz"][hv] = {"yil": sat, "hisse_gun_toplam": int(m.sum()), "hisse_toplam": int(m.any(axis=0).sum())}
    out["sg_hisse_gun"] = int((M["P2"] & M["SG"]).sum())
    return out


def t2_prefix(Pk: Dict[str, Any], Pu: Dict[str, Any], Mk: Dict[str, np.ndarray], Mu: Dict[str, np.ndarray], son: Optional[str] = None) -> Dict[str, Any]:
    """OS.os_prefix + P1 / P2 / P3 maskeleri: <= son satırlarda ortak hisselerde eşit, uzunda olup kısada olmayan hisselerde False."""
    son = son or T2_ESIK["prefix"]["son"]
    r = OS.os_prefix(Pk, Pu, son)
    nk = int(Pk["tarih"].searchsorted(pd.Timestamp(son), side="right"))
    cu = np.array([Pu["kol"].get(s, -1) for s in Pk["sembol"]])
    yeni = [Pu["kol"][s] for s in Pu["sembol"] if s not in Pk["kol"]]
    hf: Dict[str, int] = {}
    if (cu < 0).any() or not Pk["tarih"][:nk].equals(Pu["tarih"][:nk]):
        hf["yapi"] = 1
    else:
        for hv in T2_HAVUZ + ["SG"]:
            hf[hv] = int((Mk[hv][:nk] != Mu[hv][:nk][:, cu]).sum())
            if yeni and hv != "SG":
                hf[hv + "_yeni"] = int(Mu[hv][:nk][:, yeni].sum())
    r["havuz_fark"] = hf
    r["havuz_kisa"] = {hv: int(Mk[hv][:nk].sum()) for hv in T2_HAVUZ}
    r["toplam_fark"] = int(r["toplam_fark"] + sum(hf.values()))
    r["tutar"] = bool(r["toplam_fark"] == 0)
    return r


# ================================================================ 3) HAZIRLIK (getirisiz): kova sınırı, prefix, sayım
def t2_hazirlik(veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time()
    kasa = t2_kasa_kapi(veri)
    v = veri or T2_YOL["veri"]
    out: Dict[str, Any] = {"surum": T2_SURUM, "esik_sha": t2_esik_sha(), "zaman": _t2_simdi(), "kasa": kasa, "sinir": {}, "prefix": {},
                           "sayim": {}, "veri_not": {}}
    for p in ("ABD", "AVR"):
        Vu = OS.os_veri(p, v)
        out["veri_not"][p] = {"hisse": len(Vu["V"]), "en_gec": str(max(d.index.max() for d in Vu["V"].values()).date()),
                              "ilk": str(min(d.index.min() for d in Vu["V"].values()).date()), "not": Vu.get("not", [])}
        Pu = OS.os_panel(Vu); out["sinir"][p] = Pu["sinir"]
        Mu = t2_havuz(Pu, Vu)
        out["sayim"][p] = t2_sayim(Pu, Mu)
        del Vu; gc.collect()
        Vk = OS.os_veri(p, v, kesik=T2_ESIK["prefix"]["kisa"])
        Pk = OS.os_panel(Vk, out["sinir"][p]); Mk = t2_havuz(Pk, Vk)
        pr = t2_prefix(Pk, Pu, Mk, Mu); out["prefix"][p] = pr
        t2log.info("%s prefix: %s (toplam fark %s; %.0f sn)", p, "TUTTU" if pr["tutar"] else "TUTMADI", pr["toplam_fark"], time.time() - t0)
        del Vk, Pk, Mk, Pu, Mu; gc.collect()
    out["sure_sn"] = round(time.time() - t0)
    _t2_json_yaz(_t2_yol("hazirlik", cikti), out, "hazırlık")
    bozuk = [p for p, r in out["prefix"].items() if not r["tutar"]]
    if bozuk:
        raise T2Hata(f"EVREN PREFIX TESTİ TUTMADI: {bozuk} -> DURDU")
    return out


# ================================================================ 4) SERİLER, KARŞILAŞTIRMA, SEÇİM
def t2_seriler(Z: pd.DataFrame, pazar: str, havuzlar: Optional[List[str]] = None) -> Dict[str, pd.Series]:
    """Ad biçimi TD ile aynı: 'PAZAR|havuz|r|kart|portföy|ağırlık'; havuz P1 / P2 / P3 / tum (STREV farkları alt - üst)."""
    S: Dict[str, pd.Series] = {}
    for hv in (havuzlar or T2_HAVUZ + ["tum"]):
        m = np.ones(len(Z), bool) if hv == "tum" else Z[hv].to_numpy(bool)
        for k, v in TD.td_piyasa(Z, m, "r").items():
            S[f"{pazar}|{hv}|r|PIYASA|-|{k}"] = v
        for kart in ("MOM", "STREV"):
            for k, v in TD.td_portfoy(Z, m, kart, "r").items():
                port, w = (k.split("|") + ["-"])[:2]
                if kart == "STREV" and port in ("D10-D1", "2X3", "U30A30"):
                    v = -v
                    port = {"D10-D1": "D1-D10", "2X3": "2X3", "U30A30": "A30U30"}[port]
                S[f"{pazar}|{hv}|r|{kart}|{port}|{w}"] = v
    return S


def t2_ciftler() -> List[Dict[str, Any]]:
    L = []
    for hv in T2_HAVUZ:
        for k, b, r, p, a in TD.TD_CIFT:
            L.append({"havuz": hv, "kod": k, "biz": b.replace("|havuz|", f"|{hv}|"), "ref": r, "piyasa": p, "aciklama": a})
    return L


def t2_karsilastir(S: Dict[str, pd.Series], R: Dict[str, pd.Series]) -> List[Dict[str, Any]]:
    K = t2_ciftler()
    for c in K:
        c["donem"] = {}
        for dn, pen in T2_ESIK["donem"].items():
            if dn == "tarih":
                continue
            if c["biz"] not in S or c["ref"] not in R:
                c["donem"][dn] = {"n": 0, "hukum": "ÖLÇÜLEMEDİ", "neden": "seri yok"}
                continue
            x = TD.td_karsilastir(S[c["biz"]], R[c["ref"]], c["piyasa"], pen)
            x.pop("alt", None)
            c["donem"][dn] = x
    return K


def t2_secim(K: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Önceden yazılı seçim kuralı: 21 ana hüküm (ABD A1/A2/A5/A8, AVR E1/E2/E3 x d1/d2/d3) hepsi DOĞRU olan en geniş havuz; yoksa en çok DOĞRU."""
    km = T2_ESIK["secim"]["kume"]; kodlar = km["ABD"] + km["AVR"]
    tablo = {}
    for hv in T2_HAVUZ:
        sat = []
        for c in K:
            if c["havuz"] != hv or c["kod"] not in kodlar:
                continue
            for dn in km["donem"]:
                sat.append({"kod": c["kod"], "donem": dn, "hukum": c["donem"][dn]["hukum"], "pearson": c["donem"][dn].get("pearson"),
                            "isaret": c["donem"][dn].get("isaret")})
        tablo[hv] = {"dogru": sum(x["hukum"] == "DOĞRU" for x in sat), "n": len(sat), "dusen": [x for x in sat if x["hukum"] != "DOĞRU"]}
    tam = [hv for hv in T2_HAVUZ if tablo[hv]["n"] == len(kodlar) * len(km["donem"]) and tablo[hv]["dogru"] == tablo[hv]["n"]]
    if tam:
        sec, yol = tam[0], "tam: bütün ana hükümler DOĞRU olanlar arasında en geniş"
    else:
        en = max(tablo[hv]["dogru"] for hv in T2_HAVUZ)
        sec = [hv for hv in T2_HAVUZ if tablo[hv]["dogru"] == en][0]
        yol = f"yedek: hiçbir havuz 21 / 21 DOĞRU değil; en çok DOĞRU ({en}), eşitlikte en geniş"
    return {"secilen": sec, "yol": yol, "tam_gecen": tam, "tablo": tablo}


def t2_sonuc(K: List[Dict[str, Any]], sec: str) -> str:
    ana = [c for c in K if c["havuz"] == sec]
    don = ["d1", "d2", "d3"]
    hk = [(c["kod"], d, c["donem"][d]["hukum"]) for c in ana for d in don]
    if all(h == "DOĞRU" for _, _, h in hk):
        return f"geniş tezgâh ({sec}) yayımlanmış serileri üç alt dönemde de izliyor (12 ana çift x 3 dönem DOĞRU)"
    uy = [f"{k} {d}" for k, d, h in hk if h == "UYUŞMUYOR"]
    if uy:
        return f"geniş tezgâhta ({sec}) ya da evrende fark var (UYUŞMUYOR: {', '.join(uy)})"
    return f"geniş tezgâh ({sec}) yayımlanmış serileri kısmen izliyor (DOĞRU olmayan: " + ", ".join(
        f"{k} {d} {h}" for k, d, h in hk if h != "DOĞRU") + ")"


def _t2_ort_t(s: Optional[pd.Series], a: str, b: str) -> Dict[str, Any]:
    if s is None:
        return {"n": 0, "ort": float("nan"), "t": float("nan")}
    x = s[(s.index >= pd.Period(a, "M")) & (s.index <= pd.Period(b, "M"))].to_numpy(float)
    x = x[np.isfinite(x)]
    return {"n": int(len(x)), "ort": float(x.mean()) if len(x) else float("nan"), "t": TD._td_t(x)}


def t2_donem_ort(S: Dict[str, pd.Series], R: Dict[str, pd.Series], sec: str) -> List[Dict[str, Any]]:
    """Yayımlanmış ve bizim (seçilen havuz) dönem ortalamaları yan yana (ana çiftler)."""
    out = []
    for k, b, r, p, a in TD.TD_CIFT:
        sat = {"kod": k, "ref": r, "biz": b.replace("|havuz|", f"|{sec}|"), "aciklama": a, "donem": {}}
        for dn, (x, y) in ((d, T2_ESIK["donem"][d]) for d in ("tum", "d1", "d2", "d3")):
            sat["donem"][dn] = {"ref": _t2_ort_t(R.get(r), x, y), "biz": _t2_ort_t(S.get(sat["biz"]), x, y)}
        out.append(sat)
    return out


def t2_eski(S: Dict[str, pd.Series], yol: Optional[str] = None, havuzlar: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Eski tezgâh (Ç207 json 'seriler') ile aynı seriler, tutma ayı 2016-01..2023-12: Pearson ve ortalama farkı."""
    y = yol or T2_YOL["eski_json"]
    if not os.path.exists(y):
        return [{"durum": f"eski json yok: {y}"}]
    E = json.load(open(y, encoding="utf-8"))["seriler"]
    a, b = _per("2016-01", "2023-12"); out = []
    for hv in (havuzlar or T2_HAVUZ):
        for k, bz, r, p, ac in TD.TD_CIFT:
            es = E.get(bz)
            yn = S.get(bz.replace("|havuz|", f"|{hv}|"))
            if es is None or yn is None:
                out.append({"havuz": hv, "kod": k, "durum": "seri yok"}); continue
            es = pd.Series({pd.Period(kk, "M"): (np.nan if vv is None else vv) for kk, vv in es.items()}, dtype=float)
            D = pd.concat({"yeni": yn, "eski": es}, axis=1)
            D = D[(D.index >= a) & (D.index <= b)].dropna()
            out.append({"havuz": hv, "kod": k, "n": int(len(D)), "pearson": float(D.yeni.corr(D.eski)) if len(D) > 2 else float("nan"),
                        "yeni_ort": float(D.yeni.mean()) if len(D) else float("nan"), "eski_ort": float(D.eski.mean()) if len(D) else float("nan")})
    return out


# ================================================================ 5) EK BİLGİ: eş-farkı dağılımı
def t2_es_sd(Pn: Dict[str, Any], havuz: np.ndarray, H: int, E: Dict[str, Any] = T2_ESIK) -> List[Dict[str, Any]]:
    """Seçilen havuzda R_H eş-farkı (aynı d, aynı KV1, kendisi hariç, >= 5 eş) dağılımı; pazar x alt dönem (giriş günü yılı)."""
    X = OS.os_olcu_matris(Pn, H)["R"]
    KV = np.where(havuz, Pn["KV1"], -1)
    pm = (KV >= 0) & np.isfinite(X)
    dd, jj = np.nonzero(pm); r = X[dd, jj]
    del X; gc.collect()
    key = dd.astype(np.int64) * OS.OS_KOVA_K + KV[dd, jj].astype(np.int64)
    _, inv = np.unique(key, return_inverse=True)
    s = np.bincount(inv, weights=r); c = np.bincount(inv)
    ne = c[inv] - 1
    ok = ne >= int(OS.OS_ESIK["es"]["min"])
    with np.errstate(invalid="ignore", divide="ignore"):
        f = r - (s[inv] - r) / ne
    yil = Pn["tarih"][dd].year.to_numpy()
    out = []
    for dn in ("d1", "d2", "d3"):
        a, b = int(E["donem"][dn][0][:4]), int(E["donem"][dn][1][:4])
        m = ok & (yil >= a) & (yil <= b)
        x = f[m]; rr = r[m]
        if not len(x):
            out.append({"pazar": Pn["pazar"], "H": H, "donem": dn, "n": 0}); continue
        q = np.quantile(x, [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
        out.append({"pazar": Pn["pazar"], "H": H, "donem": dn, "n": int(len(x)), "gun": int(len(np.unique(dd[m]))), "ort": float(x.mean()),
                    "sd": float(x.std(ddof=1)), "iqr_sd": float((q[4] - q[2]) / 1.349), "p01": float(q[0]), "p05": float(q[1]),
                    "p50": float(q[3]), "p95": float(q[5]), "p99": float(q[6]), "sd_ham_R": float(rr.std(ddof=1)),
                    "es_ort_n": float(ne[m].mean())})
    return out


# ================================================================ 6) YENİDEN ÜRETİM (düz pandas; OC / OS / TD kodu yok)
def t2_yeniden(J: Dict[str, Any], veri: Optional[str] = None, aylar: Optional[List[str]] = None) -> Dict[str, Any]:
    v = veri or T2_YOL["veri"]
    ham = pd.read_pickle(os.path.join(v, "V_ABD.pkl"))
    if isinstance(ham, dict) and "veri" in ham and isinstance(ham["veri"], dict):
        ham = ham["veri"]
    fon = set()
    y = os.path.join(KOK_T2, "arastirma_cikti", "k55_dallanma", "K55_EVREN_DISI.csv")
    if os.path.exists(y):
        t = pd.read_csv(y); t = t[t.kategori.astype(str) == "fon_evren_disi"] if "kategori" in t.columns else t
        fon = set(t.sembol.astype(str).str.upper())
    y2 = os.path.join(KOK_T2, "evren_disi_ABD.csv")
    if os.path.exists(y2):
        fon |= set(pd.read_csv(y2).sembol.astype(str).str.upper())
    temiz = {}
    for s in list(ham):
        d = ham.pop(s)
        if str(s).upper() in fon:
            continue
        if isinstance(d.columns, pd.MultiIndex):
            d.columns = d.columns.get_level_values(0)
        ix = pd.DatetimeIndex(d.index)
        d.index = (ix.tz_localize(None) if ix.tz is not None else ix).normalize()
        d = d[~d.index.duplicated(keep="last")].sort_index()
        d = d[d.index <= pd.Timestamp("2026-08-31")]
        d = d[(d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0) & (d.Low > 0)].dropna(subset=["Open", "High", "Low", "Close", "Volume"])
        if len(d):
            temiz[str(s)] = d[["Close"]]
    del ham; gc.collect()
    tak = pd.DatetimeIndex(sorted(set().union(*[d.index for d in temiz.values()])))
    ay_sonu = pd.Series(tak, index=tak).groupby(tak.to_period("M")).max()
    sonuc = []
    seri = J["seriler"]
    for ay in (aylar or T2_ESIK["yeniden"]["ay"]):
        p_tut = pd.Period(ay, "M"); t = ay_sonu[p_tut - 1]
        rows = []
        for s in sorted(temiz):
            d = temiz[s]
            if t not in d.index:
                continue
            k = d.index.get_loc(t)
            if k + 1 >= len(d) or tak.get_loc(d.index[k + 1]) - tak.get_loc(t) > 10:
                continue
            nxt = d[(d.index.to_period("M") == p_tut)]
            r = nxt.Close.iloc[-1] / d.Close.iloc[k] - 1 if len(nxt) else np.nan
            mom = d.Close.iloc[k - 21] / d.Close.iloc[k - 252] - 1 if k >= 252 else np.nan
            rows.append((s, mom, r))
        T = pd.DataFrame(rows, columns=["sembol", "MOM", "r"])
        piy = float(T.r.mean())
        Tm = T[np.isfinite(T.MOM)].copy()
        Tm["pct"] = Tm.MOM.rank(method="first", pct=True); Tm["onluk"] = np.clip(np.ceil(Tm.pct * 10).astype(int), 1, 10)
        fark = float(Tm[Tm.onluk == 10].r.mean() - Tm[Tm.onluk == 1].r.mean())
        for ad, deger in (("ABD|tum|r|MOM|D10-D1|EW", fark), ("ABD|tum|r|PIYASA|-|EW", piy)):
            kod = seri.get(ad, {}).get(str(p_tut))
            sonuc.append({"seri": ad, "ay": str(p_tut), "elle": deger, "kod": kod, "n_hisse": int(len(T)),
                          "tutar": bool(kod is not None and np.isfinite(deger) and abs(deger - kod) < 1e-9)})
    fr = TD.td_french_elle(J, kl=T2_YOL["ref_td"])
    return {"satir": sonuc, "french": fr, "tutar": all(x["tutar"] for x in sonuc) and all(x["tutar"] for x in fr)}


# ================================================================ 7) SHA, ÖN KAYIT, KAPI
_T2_SHA_KAPI = ("T2_ESIK_SHA", "T2_KOD_SHA", "TD_KOD_SHA", "OS_KOD_SHA", "OC_KOD_SHA", "V_ABD2_SHA", "V_AVR2_SHA", "REF_KESIK_SHA",
                "YAHOO_KESIK_SHA", "EURUSD_KESIK_SHA", "HAZIRLIK_SHA")


def t2_sha_simdi(veri: Optional[str] = None) -> Dict[str, str]:
    v = veri or T2_YOL["veri"]
    out = {"T2_ESIK_SHA": t2_esik_sha(), "T2_KOD_SHA": OS._os_sha_dosya(T2_YOL["kod"]),
           "TD_KOD_SHA": OS._os_sha_dosya(os.path.join(KOK_T2, "TEZGAH_DOGRULAMA.py")),
           "OS_KOD_SHA": OS._os_sha_dosya(os.path.join(KOK_T2, "OLCU_SINAMA.py")), "OC_KOD_SHA": OS._os_sha_dosya(os.path.join(KOK_T2, "ORTAK_CETVEL.py")),
           "KASA_KOD_SHA": OS._os_sha_dosya(os.path.join(KOK_T2, "KASA.py")), "IS_TANIMI_SHA": OS._os_sha_dosya(T2_YOL["is_tanimi"]),
           "V_ABD2_SHA": OS._os_sha_dosya(os.path.join(v, "V_ABD2.pkl")), "V_AVR2_SHA": OS._os_sha_dosya(os.path.join(v, "V_AVR2.pkl")),
           "REF_KESIK_SHA": OS._os_sha_dosya(TD._td_yol("ref_kesik", T2_YOL["ref_td"])),
           "YAHOO_KESIK_SHA": OS._os_sha_dosya(TD._td_yol("yahoo_kesik", T2_YOL["ref_td"])),
           "EURUSD_KESIK_SHA": OS._os_sha_dosya(_t2_yol("eurusd_kesik"))}
    if os.path.exists(_t2_yol("hazirlik")):
        out["HAZIRLIK_SHA"] = OS._os_sha_dosya(_t2_yol("hazirlik"))
    return out


def _sayi(x: Any, n: int = 0) -> str:
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return "-"
    return f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def t2_onkayit_metni(veri: Optional[str] = None) -> str:
    kasa = t2_kasa_kapi(veri)
    if not os.path.exists(_t2_yol("hazirlik")):
        raise T2Hata("hazırlık json yok (önce 'hazirlik')")
    HZ = json.load(open(_t2_yol("hazirlik"), encoding="utf-8"))
    if HZ.get("esik_sha") != t2_esik_sha():
        raise T2Hata("hazırlık json başka T2_ESIK ile üretilmiş -> hazırlığı yeniden koş")
    sh = t2_sha_simdi(veri); kod_git = OS._os_git_islenmis(T2_YOL["kod"])
    tdd = json.load(open(TD._td_yol("ref_durum", T2_YOL["ref_td"]), encoding="utf-8"))
    r2 = json.load(open(_t2_yol("ref2_durum"), encoding="utf-8"))
    L = [f"# TEZGÂH 2 DOĞRULAMA — ÖN KAYIT ({_t2_simdi()})", "",
         f"Sürüm: {T2_SURUM}. İş tanımı: arastirma_cikti/tezgah2/TEZGAH2_DOGRULAMA_IS_TANIMI.md (sha {sh['IS_TANIMI_SHA']}).",
         f"Kod: TEZGAH2_DOGRULAMA.py git {kod_git['commit']} {kod_git['commit_zamani']}. Bu dosya koşudan ÖNCE commit edilir; t2_kapi git kaydını, "
         "değişmemişliği, sha'ları ve kontrol tablosunu denetler. İz aranmaz; yalnız doğrulama ve havuz seçimi. Bizim aylık getiri serileri "
         "henüz HESAPLANMADI (hazırlık getirisiz: kova sınırları, evren prefix testi, havuz sayımları).", "",
         f"Açık kesik: KASA 2 (/tmp/kasa2/acik/KASA_DURUM.json) {kasa['durum']['acik_kesik']} (mühür {kasa['durum'].get('muhur_id')}); "
         f"kasa_kapisi: " + "; ".join(f"{os.path.basename(k)} en geç {t}" for k, t in kasa["hisse"]["dosya"].items()) + "; referans: "
         + "; ".join(f"{os.path.basename(k)} en geç {t}" for k, t in kasa["referans"]["dosya"].items()) + ".", "",
         "Veri yolu: OS.os_veri(pazar, '/tmp/kasa2/acik') -> OC.oc_veri(..., veri2='/nonexistent_os_k34_yok'): k34_yahoo KULLANILMAZ; "
         "V_ABD.pkl / V_AVR.pkl bu klasörde V_ABD2.pkl / V_AVR2.pkl'ye bağlantı (t2_kasa_kapi denetler).", "",
         "## 1. HAVUZ ADAYLARI (iş tanımından AYNEN)", "", T2_ESIK["havuz"]["metin"], "",
         f"İşlemsel tanım (kodda): P1: {T2_ESIK['havuz']['P1']}.", f"P2: {T2_ESIK['havuz']['P2']}.", f"P3: {T2_ESIK['havuz']['P3']}.", "",
         "## 2. HÜKÜM KURALI (iş tanımından AYNEN)", "", T2_ESIK["hukum"]["metin"], "", f"Kod: {T2_ESIK['hukum']['kod']}.", "",
         "## 3. HAVUZ SEÇİM KURALI (iş tanımından AYNEN)", "", T2_ESIK["secim"]["metin"], "", f"İşlemsel: {T2_ESIK['secim']['yorum']}", "",
         f"Sonuç cümlesi: {T2_ESIK['sonuc']['kural']}.", "",
         "## 4. SERİLER VE DÖNEMLER", "", f"Dönemler (tutma ayı): tüm {T2_ESIK['donem']['tum']}, d1 {T2_ESIK['donem']['d1']}, d2 "
         f"{T2_ESIK['donem']['d2']}, d3 {T2_ESIK['donem']['d3']}. {T2_ESIK['seri']}.", "",
         "| kod | bizim seri (havuz = P1 / P2 / P3) | referans | piyasa | açıklama |", "|---|---|---|---|---|"]
    for k, b, r, p, a in TD.TD_CIFT:
        L.append(f"| {k} | `{TD._ad(b)}` | `{r}` | {'E' if p else 'H'} | {a} |")
    L += ["", f"Eski tezgâhla karşılaştırma: {T2_ESIK['eski']['tanim']}.", "", f"Ek bilgi (karar dışı): {T2_ESIK['ek']['sayim']}. {T2_ESIK['ek']['es_sd']}.", "",
          f"Yeniden üretim: {T2_ESIK['yeniden']['tanim']}; seriler {T2_ESIK['yeniden']['seri']}, aylar {T2_ESIK['yeniden']['ay']}.", "",
          "## 5. HAZIRLIK SONUCU (getirisiz; tezgah2_hazirlik.json)", "", "### 5a. EVREN PREFIX TESTİ (kısa kesik 2015-06-30, uzun 2023-12-29; <= 2015-05-29)", "",
          "| pazar | sonuç | toplam fark | gün | hisse kısa / uzun | P1 / P2 / P3 hisse-gün (önek) | maske farkları |", "|---|---|---|---|---|---|---|"]
    for p, r in HZ["prefix"].items():
        L.append(f"| {p} | {'TUTTU' if r['tutar'] else 'TUTMADI'} | {r['toplam_fark']} | {r.get('n_gun')} | {r.get('n_hisse_kisa')} / {r.get('n_hisse_uzun')} | "
                 + " / ".join(_sayi(r["havuz_kisa"].get(h)) for h in T2_HAVUZ) + " | "
                 + ", ".join(f"{k} {v}" for k, v in {**r["fark"], **r["havuz_fark"]}.items()) + " |")
    L += ["", "### 5b. KOVA SINIRLARI (OS kuralı, bu veride; koşuda aynı sayılar)", "", "```json", json.dumps(HZ["sinir"], ensure_ascii=False), "```", "",
          "### 5c. HAVUZ BAŞINA HİSSE SAYISI (yılda en az bir gün havuzda; günlük ortalama)", "",
          "| pazar | havuz | " + " | ".join(str(y) for y in T2_ESIK["havuz"]["sayim_yil"]) + " | toplam hisse |", "|---|---|" + "---|" * (len(T2_ESIK["havuz"]["sayim_yil"]) + 1)]
    for p, sy in HZ["sayim"].items():
        for hv in T2_HAVUZ:
            yy = sy["havuz"][hv]["yil"]
            L.append(f"| {p} | {hv} | " + " | ".join(f"{_sayi(yy.get(str(y), {}).get('hisse'))} ({_sayi(yy.get(str(y), {}).get('gunluk_ort'))})"
                                                     for y in T2_ESIK["havuz"]["sayim_yil"]) + f" | {_sayi(sy['havuz'][hv]['hisse_toplam'])} |")
    L += ["", "## 6. REFERANS KAYNAK VE ERİŞİM", "", f"French (TEZGAH_DOGRULAMA ile aynı kesik dosya; indirme {tdd.get('zaman')}; yedek: "
          f"{tdd.get('yedek') or 'kullanılmadı'}):", "", "| dosya | durum | sha256 |", "|---|---|---|"]
    for ad, d in tdd["french"].items():
        L.append(f"| {ad} | {d.get('durum')} | `{d.get('sha', '-')}` |")
    L += ["", f"EURUSD: {r2['kaynak']}; indirme {r2['zaman']}; {r2['n_gun']} gün {r2['ilk']}..{r2['son']} (kesik); csv sha `{r2['csv_sha']}`; "
          f"Yahoo karşılaştırma: {r2.get('yahoo_karsilastirma')}.", "", "## 7. SHA", "", "| ad | sha256 |", "|---|---|"]
    for k, v in sh.items():
        L.append(f"| {k} | `{v}` |")
    L += ["", "## 8. TANIMLAR (T2_ESIK)", "", "```json", json.dumps(T2_ESIK, ensure_ascii=False, indent=1), "```", "",
          "## 9. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
          "|---|---|---|---|"]
    try:
        import IZ_KARNE as _IK
        adlar = {k["kod"]: k.get("madde", k.get("ad", "")) for k in _IK.IK_KONTROL}
    except Exception:   # IZ_KARNE okunamazsa ad boş kalır; kapı yine denetler
        adlar = {}
    for k, (y, kn) in T2_KONTROL.items():
        L.append(f"| {k} | {adlar.get(k, '')} | {y} | {kn} |")
    return "\n".join(L) + "\n"


def t2_onkayit_yaz(veri: Optional[str] = None, uzerine: bool = False) -> str:
    y = _t2_yol("onkayit")
    if os.path.exists(y) and not uzerine:
        raise T2Hata(f"ön kayıt zaten var: {y} (--uzerine-yaz)")
    return _t2_yaz(y, t2_onkayit_metni(veri), "ön kayıt")


def t2_kapi(onkayit: Optional[str] = None, git: bool = True, kontrol: bool = True, veri: Optional[str] = None) -> Dict[str, Any]:
    yol = onkayit or _t2_yol("onkayit")
    if not os.path.exists(yol):
        raise T2Hata(f"ön kayıt yok: {yol}")
    kasa = t2_kasa_kapi(veri)
    metin = open(yol, encoding="utf-8").read(); sh = t2_sha_simdi(veri); bozuk = []
    for k in _T2_SHA_KAPI:
        m = re.search(rf"\|\s*{k}\s*\|\s*`([0-9a-f]{{64}})`", metin)
        if not m or m.group(1) != sh.get(k):
            bozuk.append(k)
    if bozuk:
        raise T2Hata(f"ön kayıt sha tutmuyor: {bozuk} -> DURDU")
    g = OS._os_git_islenmis(yol) if git else {"commit": "-", "commit_zamani": "-"}
    gh = OS._os_git_islenmis(_t2_yol("hazirlik")) if git else None
    kk = None
    if kontrol:
        import IZ_KARNE as _IK
        kk = _IK.ik_kontrol_kapisi(yol)
    return {"onkayit": yol, "git": g, "hazirlik_git": gh, "kasa": kasa, "sha": sh, "kontrol": bool(kk["gecti"]) if kk else None}


# ================================================================ 8) KOŞU
def _t2_seri_json(S: Dict[str, pd.Series]) -> Dict[str, Dict[str, Optional[float]]]:
    return {k: {str(p): (float(x) if np.isfinite(x) else None) for p, x in v.items()} for k, v in S.items()}


def t2_kos(veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    t0 = time.time(); bas = _t2_simdi()
    kp = t2_kapi(git=git, kontrol=kontrol, veri=veri)
    v = veri or T2_YOL["veri"]
    HZ = json.load(open(_t2_yol("hazirlik"), encoding="utf-8"))
    R, _ = TD.td_ref_yukle(T2_YOL["ref_td"])
    fx = t2_eurusd_ay()
    S: Dict[str, pd.Series] = {}; nt: Dict[str, Any] = {}; ZK: Dict[str, Any] = {}
    for p in ("ABD", "AVR"):
        Vd = OS.os_veri(p, v)
        Pn = OS.os_panel(Vd, HZ["sinir"][p])
        M = t2_havuz(Pn, Vd)
        Z = TD.td_kesit(Pn, Vd, fx if p == "AVR" else None)
        dd = Z.d.to_numpy(np.int64); jj = Z.j.to_numpy(np.int64)
        for hv in T2_HAVUZ:
            Z[hv] = M[hv][dd, jj]
        if not (Z.havuz.to_numpy(bool) == Z.P1.to_numpy(bool)).all():
            raise T2Hata(f"{p}: os_kart_sinyal havuzu P1 ile aynı değil")
        nt[p] = {"hisse": len(Vd["V"]), "en_gec": str(max(d.index.max() for d in Vd["V"].values()).date()), "kesit_satir": int(len(Z)),
                 **{f"kesit_{hv}": int(Z[hv].sum()) for hv in T2_HAVUZ}, "fx": "FRED DEXUSEU ay son kuru" if p == "AVR" else "-"}
        S.update(t2_seriler(Z, p))
        ZK[p] = {"Pn": Pn, "M": M}
        del Z, Vd; gc.collect()
        t2log.info("%s seriler hazır (%.0f sn)", p, time.time() - t0)
    K = t2_karsilastir(S, R)
    SEC = t2_secim(K)
    sec = SEC["secilen"]
    DO = t2_donem_ort(S, R, sec)
    ES = []
    for p in ("ABD", "AVR"):
        Pn = ZK[p]["Pn"]; m = ZK[p]["M"][sec]
        for H in (15, 30):
            ES += t2_es_sd(Pn, m, H)
            gc.collect()
        t2log.info("%s eş-farkı SD hazır (%.0f sn)", p, time.time() - t0)
        ZK[p] = None; del Pn, m; gc.collect()
    kullan = {c["biz"] for c in K} | set(T2_ESIK["yeniden"]["seri"])
    J: Dict[str, Any] = {"surum": T2_SURUM, "esik_sha": t2_esik_sha(), "kapi": OS._os_temizle({"git": kp["git"], "hazirlik_git": kp["hazirlik_git"],
                         "kontrol": kp["kontrol"], "sha": kp["sha"], "kasa": kp["kasa"]}), "bas": bas, "bit": None, "veri_not": nt,
                         "ciftler": K, "secim": SEC, "sonuc": t2_sonuc(K, sec), "donem_ort": DO, "eski": t2_eski(S, havuzlar=sorted({"P1", sec})),
                         "es_sd": ES, "hazirlik": {"prefix": HZ["prefix"], "sayim": HZ["sayim"], "sinir": HZ["sinir"], "veri_not": HZ["veri_not"]},
                         "seriler": _t2_seri_json({k: v for k, v in S.items() if k in kullan}),
                         "seri_n": _t2_seri_json({k: v for k, v in S.items() if k.endswith("|N") and "|r|PIYASA|" in k}),
                         "ref_seriler": _t2_seri_json({k: v[v.index >= pd.Period("2000-01", "M")] for k, v in R.items()
                                                       if k in {c["ref"] for c in K} | {"US_MKT", "US_MOM", "US_P12_VW_FARK", "EU_WML"}}),
                         "seriler_tum_sayi": len(S)}
    J["ref_en_gec"] = max(str(v.index.max()) for v in R.values())
    del S, ZK; gc.collect()
    J["yeniden"] = t2_yeniden(J, v)
    J["ref2_durum"] = json.load(open(_t2_yol("ref2_durum"), encoding="utf-8"))
    J["hata"] = list(T2_HATA)
    J["bit"] = _t2_simdi(); J["sure_sn"] = round(time.time() - t0)
    _t2_yaz(_t2_yol("json"), json.dumps(OS._os_temizle(J), ensure_ascii=False, default=OS._os_json), "json")
    if not J["yeniden"]["tutar"]:
        t2log.error("YENİDEN ÜRETİM TUTMADI: %s", J["yeniden"])
    return J


T2_HATA: List[str] = []


# ================================================================ 9) ARAYÜZ (sonraki ajan)
def t2_secili_panel(pazar: str, veri: Optional[str] = None, havuz: Optional[str] = None) -> Dict[str, Any]:
    """Seçilen havuzlu nedensel panel: {'Vd', 'Pn' (OS paneli; kova sınırları hazırlıktaki sayılar), 'havuz' (gün x hisse bool), 'ad',
    'maskeler' (P1 / P2 / P3 / SG)}. havuz verilmezse tezgah2_dogrulama.json 'secim.secilen'. KASA 2 kapısı önce geçer."""
    t2_kasa_kapi(veri)
    if havuz is None:
        havuz = json.load(open(_t2_yol("json"), encoding="utf-8"))["secim"]["secilen"]
    if havuz not in T2_HAVUZ:
        raise T2Hata(f"bilinmeyen havuz {havuz}")
    HZ = json.load(open(_t2_yol("hazirlik"), encoding="utf-8"))
    Vd = OS.os_veri(pazar, veri or T2_YOL["veri"])
    Pn = OS.os_panel(Vd, HZ["sinir"][pazar])
    M = t2_havuz(Pn, Vd)
    return {"Vd": Vd, "Pn": Pn, "havuz": M[havuz], "ad": havuz, "maskeler": M}


# ================================================================ 10) RAPOR
_p = TD._p
_y = TD._y
_DON_AD = {"tum": "2000-07..2023-12", "d1": "2001-07", "d2": "2008-15", "d3": "2016-23"}


def _isr(x: Any) -> str:
    return "-" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f"%{x * 100:.0f}"


def t2_rapor(J: Optional[Dict[str, Any]] = None) -> str:
    J = J or json.load(open(_t2_yol("json"), encoding="utf-8"))
    K = J["ciftler"]; SEC = J["secim"]; sec = SEC["secilen"]; HZ = J["hazirlik"]
    Ks = {(c["havuz"], c["kod"]): c for c in K}
    L = [f"# TEZGÂH 2 DOĞRULAMA — RAPOR ({J['bit']})", "",
         f"{J['surum']}. Ön kayıt TEZGAH2_DOGRULAMA_ON_KAYIT.md (git {J['kapi']['git']['commit']} {J['kapi']['git']['commit_zamani']}); koşu "
         f"{J['bas']} .. {J['bit']} ({J['sure_sn']} sn). Hisse verisi yalnız KASA 2 açık kısmı (/tmp/kasa2/acik, kesik 2023-12-31; k34 yok); "
         "referans French veri kütüphanesi (2023-12'de kesik) + FRED EURUSD.", "",
         "## 1. TEK SAYFA ÖZET", "",
         f"**Seçilen havuz: {sec}** ({SEC['yol']}). Havuz başına 21 ana hükümden DOĞRU: " + ", ".join(
             f"{hv} {SEC['tablo'][hv]['dogru']} / {SEC['tablo'][hv]['n']}" for hv in T2_HAVUZ) + ".", ""]
    for hv in T2_HAVUZ:
        d = SEC["tablo"][hv]["dusen"]
        if d:
            L.append(f"- {hv}'de DOĞRU olmayan: " + "; ".join(f"{x['kod']} {_DON_AD[x['donem']]} {x['hukum']} (r {_p(x['pearson'])}, işaret {_isr(x['isaret'])})" for x in d))
    L += ["", f"**Geniş tezgâh yayımlanmış serileri izliyor mu: {J['sonuc']}.**", "",
          f"Seri başına hüküm, seçilen havuz {sec} (Pearson / işaret uyumu; kural: korelasyon >= 0,70 ve işaret >= %70 DOĞRU, piyasa >= 0,90; "
          "0,40-0,70 KISMEN; < 0,40 UYUŞMUYOR):", "", "| kod | seri | 2001-07 | 2008-15 | 2016-23 | 2000-07..2023-12 |", "|---|---|---|---|---|---|"]
    for k, b, r, p, a in TD.TD_CIFT:
        c = Ks[(sec, k)]
        L.append(f"| {k} | {a} | " + " | ".join(f"{c['donem'][d]['hukum']} ({_p(c['donem'][d].get('pearson'))} / {_isr(c['donem'][d].get('isaret'))})"
                                                for d in ("d1", "d2", "d3", "tum")) + " |")
    L += ["", "Yayımlanmış ve bizim dönem ortalamaları (aylık %, parantezde t; bizim = seçilen havuz):", "",
          "| kod | referans | 2001-07 ref / biz | 2008-15 ref / biz | 2016-23 ref / biz |", "|---|---|---|---|---|"]
    for r in J["donem_ort"]:
        L.append(f"| {r['kod']} | `{r['ref']}` | " + " | ".join(
            f"{_y(r['donem'][d]['ref']['ort'])} ({_p(r['donem'][d]['ref']['t'])}) / {_y(r['donem'][d]['biz']['ort'])} ({_p(r['donem'][d]['biz']['t'])})"
            for d in ("d1", "d2", "d3")) + " |")
    L += ["", "Okuma: evren bugün işlem gören hisselerdir (batan yok; ABD'de 2000'de aktif hisse sayısı 2025'in ~%31'i). Bu, seviye getirilerini "
          "ve alt onlukları (MOM alt, STREV alt) yukarı çeker; 2000-15'te daha çok. Korelasyon (ay ay zamanlama) bu yanlılıktan az etkilenir, "
          "ortalama (seviye) çok etkilenir.", "",
          "Havuz başına hisse sayısı (yılda en az bir gün havuzda; parantezde günlük ortalama):", "",
          "| pazar | havuz | " + " | ".join(str(y) for y in T2_ESIK["havuz"]["sayim_yil"]) + " |", "|---|---|" + "---|" * len(T2_ESIK["havuz"]["sayim_yil"])]
    for p, sy in HZ["sayim"].items():
        for hv in T2_HAVUZ:
            yy = sy["havuz"][hv]["yil"]
            L.append(f"| {p} | {hv} | " + " | ".join(f"{_sayi(yy.get(str(y), {}).get('hisse'))} ({_sayi(yy.get(str(y), {}).get('gunluk_ort'))})"
                                                     for y in T2_ESIK["havuz"]["sayim_yil"]) + " |")
    L += ["", "## 2. BÜTÜN HÜKÜMLER (havuz x seri x dönem)", "",
          "| havuz | kod | dönem | ay | Pearson | Spearman | işaret | eğim | biz ort (t) | ref ort (t) | hüküm |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in K:
        for d in ("d1", "d2", "d3", "tum"):
            s = c["donem"][d]
            L.append(f"| {c['havuz']} | {c['kod']} | {_DON_AD[d]} | {s.get('n', 0)} | {_p(s.get('pearson'))} | {_p(s.get('spearman'))} | {_isr(s.get('isaret'))} | "
                     f"{_p(s.get('egim'))} | {_y(s.get('biz_ort'))} ({_p(s.get('biz_t'))}) | {_y(s.get('ref_ort'))} ({_p(s.get('ref_t'))}) | {s['hukum']} |")
    L += ["", "### En çok ayrışan 5 ay (seçilen havuz, ana çiftler, dönem 2000-07..2023-12; % puan)", ""]
    for k, *_ in TD.TD_CIFT:
        s = Ks[(sec, k)]["donem"]["tum"]
        if s.get("ayrisan"):
            L.append(f"- **{k}**: " + "; ".join(f"{a['ay']} biz {_y(a['biz'])} / ref {_y(a['ref'])}" for a in s["ayrisan"][:5]))
    L += ["", "## 3. ESKİ TEZGÂHLA (Ç207) AYNI SERİLER, 2016-01..2023-12", "", "| havuz | kod | ay | Pearson (yeni, eski) | yeni ort | eski ort |", "|---|---|---|---|---|---|"]
    for r in J["eski"]:
        if "pearson" in r:
            L.append(f"| {r['havuz']} | {r['kod']} | {r['n']} | {_p(r['pearson'])} | {_y(r['yeni_ort'])} | {_y(r['eski_ort'])} |")
        else:
            L.append(f"| {r.get('havuz', '-')} | {r.get('kod', '-')} | - | {r.get('durum')} | | |")
    L += ["", "## 4. EK BİLGİ (karar dışı; sayım)", "", f"### 4a. Seçilen havuz {sec}: yıl başına hisse-gün ve likidite üst yarı payı", "",
          "| yıl | ABD hisse-gün | ABD lik. üst yarı | AVR hisse-gün | AVR lik. üst yarı |", "|---|---|---|---|---|"]
    ya, ye = HZ["sayim"]["ABD"]["havuz"][sec]["yil"], HZ["sayim"]["AVR"]["havuz"][sec]["yil"]
    for y in sorted(set(ya) | set(ye)):
        a, e = ya.get(y, {}), ye.get(y, {})
        L.append(f"| {y} | {_sayi(a.get('hisse_gun'))} | {_isr(a.get('lik_ust_pay'))} | {_sayi(e.get('hisse_gun'))} | {_isr(e.get('lik_ust_pay'))} |")
    L += ["", f"### 4b. Eş-farkı R_H dağılımı (seçilen havuz {sec}; aynı gün, aynı KV1, kendisi hariç, >= 5 eş; giriş günü yılı)", "",
          "| pazar | H | dönem | n | gün | ort | SD | IQR/1,349 | p05 | p50 | p95 | SD ham R | ort eş |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in J["es_sd"]:
        if not r.get("n"):
            L.append(f"| {r['pazar']} | {r['H']} | {_DON_AD[r['donem']]} | 0 | | | | | | | | | |"); continue
        L.append(f"| {r['pazar']} | {r['H']} | {_DON_AD[r['donem']]} | {_sayi(r['n'])} | {_sayi(r['gun'])} | {_y(r['ort'])} | {_y(r['sd'])} | {_y(r['iqr_sd'])} | "
                 f"{_y(r['p05'])} | {_y(r['p50'])} | {_y(r['p95'])} | {_y(r['sd_ham_R'])} | {_sayi(r['es_ort_n'], 1)} |")
    L += ["", "## 5. EVREN PREFIX TESTİ (kısa kesik 2015-06-30, uzun 2023-12-29; havuz / sinyal günü <= 2015-05-29)", "",
          "| pazar | sonuç | toplam fark | gün | hisse kısa / uzun | P1 / P2 / P3 hisse-gün (önek) | farklar |", "|---|---|---|---|---|---|---|"]
    for p, r in HZ["prefix"].items():
        L.append(f"| {p} | {'TUTTU' if r['tutar'] else 'TUTMADI'} | {r['toplam_fark']} | {r.get('n_gun')} | {r.get('n_hisse_kisa')} / {r.get('n_hisse_uzun')} | "
                 + " / ".join(_sayi(r["havuz_kisa"].get(h)) for h in T2_HAVUZ) + " | " + ", ".join(f"{k} {v}" for k, v in {**r["fark"], **r["havuz_fark"]}.items()) + " |")
    L += ["", "Olay kümeleri (OS bacak x H, <= 2015-05-29): " + "; ".join(f"{p}: " + ", ".join(f"{k} {v['n_kisa']}/{v['n_uzun']} fark {v['fark']}"
                                                                                            for k, v in list(r["olay"].items())[:5]) + " ..." for p, r in HZ["prefix"].items()), "",
          "## 6. YENİDEN ÜRETİM: " + ("TUTTU" if J["yeniden"]["tutar"] else "TUTMADI"), "",
          "Ham V_ABD2.pkl'den düz pandas (OC / OS / TD kodu kullanılmadan):", "", "| seri | tutma ayı | hisse | elle | kod | tutar |", "|---|---|---|---|---|---|"]
    for r in J["yeniden"]["satir"]:
        L.append(f"| `{TD._ad(r['seri'])}` | {r['ay']} | {r['n_hisse']} | {r['elle']:.10f} | {('-' if r['kod'] is None else f'{r['kod']:.10f}')} | {'E' if r['tutar'] else 'H'} |")
    L += ["", "French ham satırından elle (ayrıştırıcı kullanılmadan):", "", "| dosya | ay | ham satır | elle | kod | tutar |", "|---|---|---|---|---|---|"]
    for r in J["yeniden"].get("french", []):
        L.append(f"| {r['dosya']} | {r['ay']} | `{r.get('satir', r.get('hata', ''))}` | {('-' if r.get('elle') is None else f'{r['elle']:.6f}')} | "
                 f"{('-' if r.get('kod') is None else f'{r['kod']:.6f}')} | {'E' if r['tutar'] else 'H'} |")
    r2 = J["ref2_durum"]
    L += ["", f"FRED EURUSD ham satırları (elle okunur): {r2.get('ham_ornek')}; Yahoo EURUSD=X ile: {r2.get('yahoo_karsilastirma')}.", "",
          "## 7. EN GEÇ TARİH", "", f"- KASA 2 açık kesik: {J['kapi']['kasa']['durum']['acik_kesik']} (mühür {J['kapi']['kasa']['durum'].get('muhur_id')})",
          "- kasa_kapisi (hisse): " + "; ".join(f"{os.path.basename(k)} {t}" for k, t in J["kapi"]["kasa"]["hisse"]["dosya"].items()),
          "- kasa_kapisi (referans): " + "; ".join(f"{os.path.basename(k)} {t}" for k, t in J["kapi"]["kasa"]["referans"]["dosya"].items()),
          "- panel en geç bar: " + "; ".join(f"{p} {v['en_gec']}" for p, v in J["veri_not"].items()), f"- French en geç ay: {J['ref_en_gec']}",
          f"- EURUSD: {r2.get('ilk')}..{r2.get('son')}", "", "## 8. VERİ NOTU", ""]
    for p, v in J["veri_not"].items():
        L.append(f"- {p}: {v['hisse']} hisse, ay sonu kesit satırı {v['kesit_satir']} (P1 {v['kesit_P1']}, P2 {v['kesit_P2']}, P3 {v['kesit_P3']}); kur: {v['fx']}")
    for p, v in HZ["veri_not"].items():
        L.append(f"- {p} (hazırlık): ilk bar {v['ilk']}, en geç {v['en_gec']}; " + "; ".join(v["not"]))
    L += ["", "## 9. HATA (koşu sırasında ve sonrasında bulunan; IK_HATA'ya ana model yazar)", ""]
    L += [f"- {h}" for h in (J.get("hata") or ["yok"])]
    L += ["", "## 10. KONTROL LİSTESİ (ön kayıttaki tablo aynen)", "", "| Kod | Yanıt | Kanıt |", "|---|---|---|"]
    L += [f"| {k} | {y} | {kn} |" for k, (y, kn) in T2_KONTROL.items()]
    L += ["", "## 11. ARAYÜZ (sonraki ajan)", "", "`import TEZGAH2_DOGRULAMA as T2; X = T2.t2_secili_panel('ABD')` -> X['Pn'] (OS nedensel paneli, kova sınırları "
          "hazırlıktaki sayılar), X['havuz'] (seçilen havuz maskesi, gün x hisse), X['Vd'], X['maskeler'] (P1 / P2 / P3 / SG). Veri /tmp/kasa2/acik; "
          "KASA 2 kapısı fonksiyonun içinde."]
    return "\n".join(L) + "\n"


# ================================================================ ÇAKIŞMA KAPISI
def _cakisma_kontrol_t2(_once=_CK_ONCE_T2, _dosya="TEZGAH2_DOGRULAMA.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_T2", "_CK_KAYIT", "_cakisma_kontrol_t2", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "warnings", "copy", "_dt", "gc",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple", "OS", "TD", "_p", "_y")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_t2()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=T2_SURUM)
    ap.add_argument("komut", choices=["ref", "hazirlik", "onkayit", "kos", "rapor", "sha", "kapi"])
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    try:
        if a.komut == "ref":
            print(json.dumps(OS._os_temizle(t2_ref_indir()), ensure_ascii=False, indent=1, default=OS._os_json))
        elif a.komut == "hazirlik":
            H_ = t2_hazirlik(a.veri)
            print(json.dumps(OS._os_temizle({p: {"tutar": r["tutar"], "toplam_fark": r["toplam_fark"]} for p, r in H_["prefix"].items()}), ensure_ascii=False))
        elif a.komut == "onkayit":
            print(t2_onkayit_yaz(a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kapi":
            print(json.dumps(OS._os_temizle(t2_kapi(veri=a.veri)), ensure_ascii=False, indent=1, default=OS._os_json))
        elif a.komut == "kos":
            J_ = t2_kos(a.veri)
            print(_t2_yaz(_t2_yol("rapor"), t2_rapor(J_), "rapor"))
            print("seçilen:", J_["secim"]["secilen"], "|", J_["sonuc"]); print("yeniden üretim:", J_["yeniden"]["tutar"])
        elif a.komut == "rapor":
            print(_t2_yaz(_t2_yol("rapor"), t2_rapor(), "rapor"))
        else:
            print(json.dumps(t2_sha_simdi(a.veri), indent=1))
    except T2Hata as ex:
        t2log.error("%s", ex); sys.exit(1)
