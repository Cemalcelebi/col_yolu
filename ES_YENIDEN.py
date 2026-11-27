"""ES_YENIDEN — eski 'iz değil' kayıtlarının AYNI HİSSENİN RASTGELE / BÜTÜN GÜNLERİNE göre yeniden okunması, birinci parti (27 Kasım 2026).

İş tanımı: arastirma_cikti/goz_tespit/ES_YENIDEN_IS_TANIMI.md (ana model). Envanter: arastirma_cikti/goz_tespit/ES_OLCUT_ENVANTER.md (Liste 1).
Bu bir AYNI VERİDE YENİDEN OKUMADIR (kör değil): hiçbir sonuç 'iz' diye yazılmaz; en fazla 'ZAMANLAMA ADAYI / TOPLAM ADAYI (aynı veride yeniden okuma;
ileri test gerekir)'. Yeni veri indirilmez; her kayıt KENDİ verisini, KENDİ giriş kuralını, KENDİ ufkunu ve KENDİ veri kesiğini kullanır (KASA kavramı
değişmez: geniş evrende (V_*2) kesik 2024-12-31 = KASA_DEFTERI'nde açılmış son blok).

ÖLÇÜ (iş tanımı 2. bölüm, AYNEN):
  R            = olayın H ufuklu getirisi (dosyadaki; yoksa aynı kuralla fiyattan)
  T1(s, hücre) = aynı hissenin hücre dönemindeki BÜTÜN günlerinde (olay günleri DAHİL) aynı giriş kuralıyla H ufuklu getirinin ortalaması
  PİYASA(t)    = giriş günü t'de aynı pazarın evrenindeki bütün hisselerin H ufuklu getirisinin eşit ağırlıklı ortalaması (en az 30 hisse)
  T2(hücre)    = PİYASA'nın hücre dönemindeki bütün günler üzerinden ortalaması
  TOPLAM = R - T1;  ZAMANLAMA = PİYASA(t) - T2;  SEÇİM = TOPLAM - ZAMANLAMA
  Hücre ortalaması + ay kümeli bootstrap %95 (2.000 tekrar, tohum 11; KISA_UFUK.ku_boot), ayrı ay sayısı; BH (MUM_IZI_HAVUZ._hv_bh) q 0,10.
GİRİŞ KURALLARI (kayıtların kendi tanımı; ES_KAYIT['kural']):
  'gecerli'  CETVEL2 v2.2 R_H: giriş = t+1 açılışı (dosyanın 'giris' günü), çıkış = giriş barı dahil H'inci GEÇERLİ bar (High > Low ve Volume > 0) kapanışı.
  'fi_olcut' FON_IZI.FI_OLCUT r60: giriş günü açılışı, birleşik pazar takviminde 60. günün kapanışı (5 güne kadar ffill), kriz kesiği (FON_IZI.fi_olcut_panel).

Komut:  python ES_YENIDEN.py secim     seçim listesi + atlananlar (getirisiz)
        python ES_YENIDEN.py sayim     GETİRİSİZ SAYIM (kayıt x kol x hücre: n, ayrı ay; kaynak sha) -> /root/.kasa/ham/es_yeniden/es_sayim.json
        python ES_YENIDEN.py dogrula   giriş kuralı sağlaması (dosya R'si = fiyattan R? yalnız eşleşme oranı; fark / taban hesaplanmaz)
        python ES_YENIDEN.py onkayit   ES_YENIDEN_ON_KAYIT.md (seçim + sayım + sağlama + karar kuralı + kontrol tablosu + kod sha)
        python ES_YENIDEN.py olcum     kapı (ön kayıt commit + push + temiz ağaç + kontrol kapısı + kod sha) -> ölçüm (BİR KEZ) -> es_yeniden_ozet.json
        python ES_YENIDEN.py rapor     ES_YENIDEN_RAPOR.md (özet json'undan; ek bölümler ham/es_rapor_ek.json'dan)
        python ES_YENIDEN.py sha       kod sha
Colab:  exec(open('ES_YENIDEN.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7: sonuç yukarı yanlı); geniş evren (V_*2) batanları kısmen içerir.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_ES = {k: id(v) for k, v in globals().items()}

import gzip  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_ES = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_ES not in sys.path:
    sys.path.insert(0, KOK_ES)

eslog = logging.getLogger("col.es_yeniden")
if not eslog.handlers:
    _es_h = logging.StreamHandler(sys.stderr)
    _es_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s es_yeniden: %(message)s", "%H:%M:%S"))
    eslog.addHandler(_es_h)
    eslog.setLevel(logging.INFO)
    eslog.propagate = False


class ESHata(RuntimeError):
    """Durdurucu hata: kapı / şema / kesik / sıra / sağlama uyuşmazlığı."""


ES_SURUM = "ES_YENIDEN v1.0 (2026-11-27): eski E tabanlı 'iz değil' kayıtları, aynı hisse bütün günleri tabanı (TOPLAM / ZAMANLAMA / SEÇİM)"
ES_YOL = {"cikti": os.path.join(KOK_ES, "arastirma_cikti", "goz_tespit"), "ham": os.environ.get("ES_HAM", "/root/.kasa/ham/es_yeniden"),
          "kod": os.path.join(KOK_ES, "ES_YENIDEN.py"), "envanter": os.path.join(KOK_ES, "arastirma_cikti", "goz_tespit", "ES_OLCUT_ENVANTER.md"),
          "is_tanimi": os.path.join(KOK_ES, "arastirma_cikti", "goz_tespit", "ES_YENIDEN_IS_TANIMI.md")}
ES_DOSYA = {"onkayit": "ES_YENIDEN_ON_KAYIT.md", "rapor": "ES_YENIDEN_RAPOR.md", "ozet": "es_yeniden_ozet.json"}
ES_VERI = {"V": "/tmp/veri/V_{p}.pkl", "V2": "/root/.kasa/ham/veri3/V_{p}2.pkl"}

# eşikler (iş tanımı 1-2. bölüm; sonuçtan sonra DEĞİŞMEZ)
ES_ESIK: Dict[str, Any] = {
    "secim": {"en_az_olay": 300, "en_cok_kayit": 20, "son_tarih_haric": "2026-11-26"},
    "boot": {"B": 2000, "tohum": 11},
    "karar": {"hucre_n": 100, "en_az_hucre": 2, "ay": 12, "bh_q": 0.10,
              "tanim": "ZAMANLAMA ADAYI <=> kol x kaydın n >= 100 olan hücrelerinin HEPSİNDE (en az 2 hücre) ZAMANLAMA GA alt ucu > 0 VE her n >= 100 "
                       "hücrede ayrı ay >= 12; TOPLAM ADAYI aynı kuralla TOPLAM için. Birleşik p = n >= 100 hücrelerin tek yönlü bootstrap p'lerinin "
                       "EN BÜYÜĞÜ (kesişim-birleşim sınaması). BH ailesi = ölçülebilir (>= 2 hücre n >= 100, ay >= 12) BÜTÜN kollar (ZAMANLAMA ve "
                       "TOPLAM ayrı aile); q <= 0,10 geçen aday = ADAY, geçemeyen = EMARE. n >= 100 hücresi 2'den az ya da bir n >= 100 hücrede ay < 12 "
                       "= ÖLÇÜLEMEDİ; aksi = YOK. Bilgi: bütün n >= 100 hücrelerde üst uç < 0 = EKSİ (ters)."},
    "piyasa": {"en_az_hisse": 30},
}

# ---------------------------------------------------------------- KAYIT KAYDI (giriş kuralı, ufuk, hücreler, kaynak: kayıtların kendi tanımı)
# Her satır: kod, ad, dosya(lar), kaynak veri, kural, H, kesik, hücre etiketi -> [baş, son] (giriş günü), kol tanımı (okuyucu), R sütunu, eski eşli fark sütunu.
ES_KAYIT: Dict[str, Dict[str, Any]] = {
    "Ç209": {"ad": "KART TUR 2 (geniş tezgâh, KASA 2): 14 kart", "kaynak": "V2", "kural": "gecerli", "H": 15, "kesik": "2024-12-31",
             "pazar": ["ABD", "AVR"], "dosya": ["arastirma_cikti/kart2/2024Q4/k2_satir.csv.gz"],
             "hucre": {"acik_d1": ["2001-01-01", "2007-12-31"], "acik_d2": ["2008-01-01", "2015-12-31"], "acik_d3": ["2016-01-01", "2023-12-31"],
                       "blok": ["2024-01-01", "2024-12-31"]},
             "kaynak_not": "KART_TUR2.K2_ESIK['hucre'] (acik_d1/d2/d3) + KASA_DEFTERI 2024Q1-Q4; ufuk 15 = ilk karar ufku (15 / 30); R = dosya 'R'; "
                           "durum 'olculdu' + 'essiz' (eşsiz olay da olaydır; eş yalnız E tabanının şartı)",
             "eski": "ÖLÇÜLEMEDİ (KART TUR 2; 12 kart) / açık veride kartların FARK'ı ~0"},
    "Ç205": {"ad": "KART TUR 1 (KASA yürüyen ileri test): 11 kart", "kaynak": "V", "kural": "gecerli", "H": 15, "kesik": "2023-12-31",
             "pazar": ["ABD", "AVR"], "dosya": ["arastirma_cikti/kart/2023Q4/kt_satir.csv.gz"],
             "hucre": {"acik": ["2016-01-01", "2022-12-31"], "birikimli": ["2023-01-01", "2023-12-31"]},
             "kaynak_not": "KART_TUR1.KT_ESIK['hucre'] (acik 2016-22, blok_bas 2023-01-01; KASA 2023Q1-Q4 açık); ufuk 15; kart bayrakları F_U (KT00) "
                           "ve F_KT01-F_KT10; R = dosya 'r15'",
             "eski": "ÖLÇÜLEMEDİ (KART TUR 1; hiçbir kart tutmadı)"},
    "Ç206": {"ad": "ÖLÇÜ SINAMASI: bilinen etki bacakları (MOM, STREV, HIGH52)", "kaynak": "V", "kural": "gecerli", "H": 15, "kesik": "2023-12-31",
             "pazar": ["ABD", "AVR"], "dosya": ["arastirma_cikti/olcu_sinama/os_kart_olay_ABD_H15.csv.gz", "arastirma_cikti/olcu_sinama/os_kart_olay_AVR_H15.csv.gz"],
             "hucre": {"d1": ["2016-01-01", "2019-12-31"], "d2": ["2020-01-01", "2023-12-31"]},
             "kaynak_not": "OLCU_SINAMA.OS_ESIK['donem'] (d1 2016-19, d2 2020-23; açık veri <= 2023-12-31); H 15 = ilk ufuk (15 / 30 / 60); "
                           "kol = 'bacak'; R = dosya 'R'",
             "eski": "HİÇBİR ÖLÇÜ GEÇMEDİ 0 / 36 (hat testi)"},
    "Ç226": {"ad": "ÜÇ İZ BİRLİKTE BİLANÇO OLAYINDA (UC_IZ2)", "kaynak": "V2", "kural": "gecerli", "H": 60, "kesik": "2022-12-31",
             "pazar": ["ABD"], "dosya": ["/root/.kasa/ham/sec2016/uc_iz2_satir.csv.gz"],
             "hucre": {"d1619": ["2016-01-01", "2019-12-31"], "d2022": ["2020-01-01", "2022-12-31"]},
             "kaynak_not": "UC_IZ2.UC2_ESIK['donem'] + UC2_KESIK 2022-12-31; ufuk R60 = ilk karar ufku (R60, R15); kol = R / B / İ izi var (== 1) ve "
                           "N >= 2 (birlikte); R = dosya 'R60'",
             "eski": "İZ DEĞİL (güç yeterli)"},
    "Ç204": {"ad": "CETVEL2 R15 yeniden koşusu (Y1 tabanı + Ç194-Ç202 hipotezleri + hakem turu kolları)", "kaynak": "V", "kural": "gecerli", "H": 15,
             "kesik": "2026-08-31", "pazar": ["ABD", "AVR", "BIST"],
             "dosya": ["arastirma_cikti/cetvel2/yk_TABAN.csv.gz", "arastirma_cikti/cetvel2/yk_TABAN_DS.csv.gz"]
                      + [f"arastirma_cikti/cetvel2/yk_C{c}.csv.gz" for c in range(194, 203)] + ["arastirma_cikti/cetvel2/yk_TUR.csv.gz"],
             "hucre": {"egitim": ["2016-01-01", "2022-12-31"], "sinama": ["2023-01-01", "2026-08-31"]},
             "kaynak_not": "CETVEL2.C2_ESIK['donem'] (egitim 2016-22, sinama 2023-01-01..2026-08-31); R15 (STOP YOK); kol = yk_TABAN 'Y1' (bütün satırlar), "
                           "yk_TABAN_DS 'DS_ANA', öteki dosyalarda F_* == 1; R = dosya 'r15'",
             "eski": "İZ DEĞİL / ÖLÇÜLEMEDİ (124 hipotez; KATKI+ 0, KATKI− 0)"},
    "Ç191": {"ad": "YAPI_HEDEF 2. tur: Y6 / Y8 / Y8B (Y7 n = 0)", "kaynak": "V", "kural": "gecerli", "H": 15, "kesik": "2026-08-31",
             "pazar": ["ABD", "AVR", "BIST"], "dosya": ["arastirma_cikti/yapi_hedef/olay_Y6.csv.gz", "arastirma_cikti/yapi_hedef/olay_Y8.csv.gz",
                                                    "arastirma_cikti/yapi_hedef/olay_Y8B.csv.gz"],
             "hucre": {"2016-22": ["2016-01-01", "2022-12-31"], "2023": ["2023-01-01", "2023-12-31"], "2024-26": ["2024-01-01", "2026-08-31"]},
             "kaynak_not": "YAPI_HEDEF: giriş = kırılım mumundan sonraki ilk geçerli bar açılışı ('giris'), 15 bar ufuk; dosyada R15 yok -> CETVEL2 R15 "
                           "tanımıyla fiyattan (Ç204 yeniden koşu tanımı); kol = 'deneme' (Y6, Y8, Y8B)",
             "eski": "ÖLÇÜLEMEDİ (YAPI_HEDEF 2. tur Y6-Y8; yön aleyhte)"},
    "Ç189": {"ad": "S+ v2 TAM GİRİLİR (TAM_DIP)", "kaynak": "V", "kural": "fi_olcut", "H": 60, "kesik": "2026-08-31", "pazar": ["ABD", "AVR", "BIST"],
             "dosya": ["arastirma_cikti/fitil_v2/olay_TAM_DIP.csv.gz"],
             "hucre": {"2016-22": ["2016-01-01", "2022-12-31"], "2023": ["2023-01-01", "2023-12-31"], "2024-26": ["2024-01-01", "2026-08-31"]},
             "kaynak_not": "FITIL_V2 FI_OLCUT r60 (giriş ertesi gün açılış, 60. gün kapanışı, kriz 2026-08-31); hücre = pazar x 'donem'; R = dosya 'r60'",
             "eski": "ÖLÇÜLEMEDİ (TAM_DIP; hiçbir hücrede alt uç > 0)"},
    "Ç99": {"ad": "KAP içeriden alım (K27): net alım, büyük alım, çölde alım", "kaynak": "V", "kural": "fi_olcut", "H": 60, "kesik": "2026-08-31",
            "pazar": ["BIST"], "dosya": ["arastirma_cikti/fon_izi/k27_olay.csv"],
            "hucre": {"2023": ["2023-01-01", "2023-12-31"], "2024-26": ["2024-01-01", "2026-08-31"]},
            "kaynak_not": "FON_IZI K27 FI_OLCUT (donem 2023 / 2024-26; giriş = 'giris' açılışı, r60); kol = 'olay' alim / buyuk / col_alim "
                          "('satim' beklenen yönü eksi olduğu için alınmadı); R = dosya 'r60'",
            "eski": "İçeriden alım bildirimi olumlu bilgi taşımıyor (eşlerin gerisinde)"},
}

# Liste 1'den seçilmeyenler (nedenleri ön kayıtta; getirisiz karar)
ES_ATLA: Dict[str, str] = {
    "Ç72": "olay kümesi kapalı Ç47 (D13 / Öbek, COL_OZET kapanan) ile aynı; giriş kuralı (alim_a / alim_b) dosyada sabit ufuklu değil",
    "Ç227": "TESPİT GEÇERSİZ (CLAUDE.md 25 Kas yasağı: tespit doğrulanmadan sonrası getirisi kalıbın sonucu diye sunulamaz)",
    "Ç229": "TESPİT GEÇERSİZ (haftalık kalıp v1; CLAUDE.md 25 Kas yasağı)",
    "Ç228": "Ç227 ile aynı tespit ailesi (görüntüden kurulan mum kalıbı; görsel onay yok; CLAUDE.md 25 Kas yasağı)",
    "Ç136": "çıktı bariyer isabeti / değişken çıkışlı net getiri (y, net); sabit H ufuklu getiri yok, T1 aynı kuralla kurulamaz",
    "Ç146": "olay kümesi kapalı Ç138 (K55, 90+ şekil ölçüsü) ile aynı (K55_OLAYLAR)",
    "Ç134": "çıktı bariyer isabeti / değişken çıkışlı net getiri (K51 eşleşmiş kontrol); sabit H ufuklu getiri yok",
    "Ç132": "çıktı bariyer isabeti / değişken çıkışlı net getiri (K51 cy_olay); sabit H ufuklu getiri yok",
    "Ç133": "Ç132 ile aynı olay dosyası (cy_olay) ve aynı bariyer çıkışı; sabit H ufuklu getiri yok",
    "Ç41": "işlemler değişken çıkışlı (hedef / 120 bar; 'getiri' işlem getirisi); sabit H ufuklu getiri yok",
    "Ç38": "çıktı kutu sonrası en büyük yukarı / aşağı sapma (up / dn), getiri değil; 'ref' tanımı dosyada belirsiz; ABD olay dosyası yok",
    "Ç39": "Ç38 ile aynı dosya ve aynı belirsiz çıktı (up / dn)",
    "Ç97": "olay sayısı 19-24 (< 300)",
    "Ç98": "giriş kutu tavanında bekleyen alış emri (alis_tarih, fiyat düzeyli giriş); t+1 açılış kuralı değil, T1 aynı kuralla kurulamaz",
}
# aynı olay kümesini paylaşan kayıtlar (tek satır sayılır): kod -> satırı taşıyan kayıt
ES_PAYLASAN: Dict[str, str] = {
    "Ç190": "Ç204", "Ç192": "Ç204", "Ç193": "Ç204", "Ç194": "Ç204", "Ç195": "Ç204", "Ç196": "Ç204", "Ç197": "Ç204", "Ç198": "Ç204",
    "Ç199": "Ç204", "Ç201": "Ç204", "Ç202": "Ç204",
}
ES_PAYLASAN_NOT = {
    "Ç204": "Ç204 yeniden koşusu Ç194-Ç202'nin olaylarını CETVEL2 R15 ile yeniden ölçtü (yk_C194..C202); Ç190 Y1 = yk_TABAN; Ç192 (OLUR etiketi) ve "
            "Ç197-Ç199 (puan / devir) Y1 kümesinin alt kümeleri (yk_C197-C199); Ç193 Y9 = Ç196 G2 (yk_C196 F_S1 ailesi)",
}


# ================================================================ 0) yardımcılar
def es_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:16]


def es_kod_sha() -> str:
    return es_sha_dosya(ES_YOL["kod"])


def es_esik_sha() -> str:
    return hashlib.sha256(json.dumps({"E": ES_ESIK, "K": {k: {a: v[a] for a in ("kaynak", "kural", "H", "kesik", "hucre", "dosya", "pazar")}
                                                         for k, v in ES_KAYIT.items()}}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def _es_yol(ad: str, kok: Optional[str] = None) -> str:
    return os.path.join(kok or ES_YOL["cikti"], ad)


def _es_tam(p: str) -> str:
    return p if os.path.isabs(p) else os.path.join(KOK_ES, p)


def es_ay(giris: Any) -> np.ndarray:
    """Ay kümesi anahtarı: giriş gününün YYYY-MM'i."""
    return pd.DatetimeIndex(pd.to_datetime(pd.Series(giris)).to_numpy()).strftime("%Y-%m").to_numpy()


def es_ay_sayisi(giris: Any) -> int:
    return int(len(np.unique(es_ay(giris)))) if len(giris) else 0


def es_hucre_ata(giris: Any, hucre: Dict[str, List[str]]) -> np.ndarray:
    """Giriş günü -> hücre etiketi (sözlük sırasıyla ilk eşleşen; yoksa 'dis')."""
    g = pd.to_datetime(pd.Series(giris)).to_numpy()
    out = np.full(len(g), "dis", dtype=object)
    for ad, (a, b) in hucre.items():
        m = (g >= np.datetime64(pd.Timestamp(a))) & (g <= np.datetime64(pd.Timestamp(b))) & (out == "dis")
        out[m] = ad
    return out


def es_ayristir(R: Any, T1: Any, PIY: Any, T2: Any) -> Dict[str, np.ndarray]:
    """TOPLAM = R - T1; ZAMANLAMA = PİYASA(t) - T2; SEÇİM = TOPLAM - ZAMANLAMA (özdeşlik: SEÇİM = (R - PİYASA) - (T1 - T2))."""
    R = np.asarray(R, float); T1 = np.asarray(T1, float); PIY = np.asarray(PIY, float); T2 = np.asarray(T2, float)
    TOP = R - T1; ZAM = PIY - T2
    return {"TOPLAM": TOP, "ZAMANLAMA": ZAM, "SECIM": TOP - ZAM}


# ================================================================ 1) SEÇİM (getirisiz; envanterden)
def es_envanter_liste1(yol: Optional[str] = None) -> List[Dict[str, Any]]:
    """Envanter Liste 1 tablosu (sıra, Ç, ad, dosya satırı)."""
    metin = open(yol or ES_YOL["envanter"], encoding="utf-8").read()
    bas = metin.index("## Liste 1:"); son = metin.index("## Liste 2a:")
    out = []
    for sat in metin[bas:son].splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*(Ç\d+)\s*\|\s*(.*?)\s*\|\s*([^|]*?)\s*\|", sat)
        if not m:
            continue
        ds = m.group(4).replace(".", "").strip()
        out.append({"sira": int(m.group(1)), "kod": m.group(2), "ad": m.group(3), "dosya_satiri": int(ds) if ds.isdigit() else None})
    if not out:
        raise ESHata("K10: envanter Liste 1 okunamadı")
    return out


def es_envanter_kapali(yol: Optional[str] = None) -> Dict[str, str]:
    """Envanterin 'Kapalı konuya giren kayıtlar' listesi + ana tablonun 'Kapalı konu' sütunu ('—' değilse)."""
    metin = open(yol or ES_YOL["envanter"], encoding="utf-8").read()
    out: Dict[str, str] = {}
    bas = metin.index("## Kapalı konuya giren kayıtlar"); son = metin.index("## Kayıtta olumsuz kararı olmayan")
    for m in re.finditer(r"(Ç\d+) \(([^)]*)", metin[bas:son]):
        out[m.group(1)] = m.group(2)
    tb = metin[metin.index("## Tablo:"):metin.index("## Liste 1:")]
    for sat in tb.splitlines():
        p = [x.strip() for x in sat.split("|")]
        if len(p) > 10 and re.match(r"^Ç\d+$", p[1]) and p[9] not in ("—", "-", ""):
            out.setdefault(p[1], p[9])
    return out


def es_kayit_tarih() -> Dict[str, str]:
    import IZ_KARNE as IK   # yalnız okunur
    return {r["kod"]: str(r["tarih"]) for r in IK.IK_KAYIT}


def es_secim(env: Optional[str] = None, tarih: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """İş tanımı 1. bölüm: Liste 1 sırasıyla (dosya satırı büyükten küçüğe), kapalı konu değil, tarih < 2026-11-26, olay >= 300, okunabilir; en çok 20."""
    L1 = es_envanter_liste1(env); kap = es_envanter_kapali(env); tar = tarih if tarih is not None else es_kayit_tarih()
    E = ES_ESIK["secim"]; secilen: List[str] = []; atlanan: List[Dict[str, str]] = []; paylasan: Dict[str, List[str]] = {}
    for r in L1:
        k = r["kod"]
        if k in kap:
            atlanan.append({"kod": k, "neden": f"kapalı konu ({kap[k]})"}); continue
        if str(tar.get(k, "9999")) >= E["son_tarih_haric"]:
            atlanan.append({"kod": k, "neden": f"tarih {tar.get(k)} >= 26 Kasım (zaten rastgele güne göre / iş tanımı dışı)"}); continue
        if r["dosya_satiri"] is None or r["dosya_satiri"] < int(E["en_az_olay"]):
            atlanan.append({"kod": k, "neden": f"olay sayısı < {E['en_az_olay']} ya da sayılmadı ({r['dosya_satiri']})"}); continue
        if k in ES_ATLA:
            atlanan.append({"kod": k, "neden": ES_ATLA[k]}); continue
        if k in ES_PAYLASAN:
            paylasan.setdefault(ES_PAYLASAN[k], []).append(k); continue
        if k not in ES_KAYIT:
            atlanan.append({"kod": k, "neden": "okuyucu yok (tanım belirsiz; uydurulmadı)"}); continue
        if len(secilen) < int(E["en_cok_kayit"]):
            secilen.append(k)
    for k, v in paylasan.items():
        if k not in secilen:
            raise ESHata(f"K4: paylaşılan küme sahibi {k} seçilmedi ({v})")
    return {"secilen": secilen, "atlanan": atlanan, "paylasan": paylasan}


# ================================================================ 2) OLAYLAR (getirisiz okuma; R yalnız sütun olarak taşınır)
_ES_OLAY_KOL = ["kayit", "kol", "pazar", "sembol", "giris", "hucre", "R_dosya", "eski_fark"]


def _es_cerceve(kayit: str, kol: Any, d: pd.DataFrame, pazar: Any, Rc: Optional[str], fark: Optional[pd.Series]) -> pd.DataFrame:
    return pd.DataFrame({"kayit": kayit, "kol": kol, "pazar": pazar, "sembol": d.sembol.astype(str).to_numpy(),
                         "giris": pd.to_datetime(d.giris).to_numpy(), "R_dosya": d[Rc].to_numpy(float) if Rc else np.nan,
                         "eski_fark": fark.to_numpy(float) if fark is not None else np.nan})


def es_oku_Ç209(K: Dict[str, Any]) -> pd.DataFrame:
    d = pd.read_csv(_es_tam(K["dosya"][0]), usecols=["kod", "pazar", "ufuk", "sembol", "giris", "durum", "R", "fark"])
    d = d[(d.ufuk == K["H"]) & d.durum.isin(["olculdu", "essiz"])]
    return _es_cerceve("Ç209", d.kod.to_numpy(), d, d.pazar.to_numpy(), "R", d.fark)


def es_oku_Ç205(K: Dict[str, Any]) -> pd.DataFrame:
    bas = pd.read_csv(_es_tam(K["dosya"][0]), nrows=2).columns
    F = ["F_U"] + [f"F_KT{i:02d}" for i in range(1, 11)]
    fk = {"F_U": "fark_KT00", **{f"F_KT{i:02d}": f"fark_KT{i:02d}" for i in range(1, 11)}}
    eksik = [c for c in F + list(fk.values()) if c not in bas]
    if eksik:
        raise ESHata(f"K10: Ç205 sütun eksik {eksik}")
    d = pd.read_csv(_es_tam(K["dosya"][0]), usecols=["pazar", "sembol", "giris", "ufuk", "r15"] + F + list(fk.values()))
    d = d[d.ufuk == K["H"]]; parca = []
    for f in F:
        g = d[d[f] == 1]
        parca.append(_es_cerceve("Ç205", "KT00" if f == "F_U" else f[2:], g, g.pazar.to_numpy(), "r15", g[fk[f]]))
    return pd.concat(parca, ignore_index=True)


def es_oku_Ç206(K: Dict[str, Any]) -> pd.DataFrame:
    parca = []
    for yol in K["dosya"]:
        d = pd.read_csv(_es_tam(yol), usecols=["pazar", "H", "bacak", "sembol", "giris", "R", "KV1_es_R"])
        if not (d.H == K["H"]).all():
            raise ESHata(f"K10: {yol} H != {K['H']}")
        parca.append(_es_cerceve("Ç206", d.bacak.to_numpy(), d, d.pazar.to_numpy(), "R", d.R - d.KV1_es_R))
    return pd.concat(parca, ignore_index=True)


def es_oku_Ç226(K: Dict[str, Any]) -> pd.DataFrame:
    d = pd.read_csv(_es_tam(K["dosya"][0]), usecols=["sembol", "giris", "R", "B", "I", "N", "R60", "fark_60"])
    parca = []
    for kol, m in (("R_var", d.R == 1), ("B_var", d.B == 1), ("I_var", d.I == 1), ("N_ge2", d.N >= 2)):
        g = d[m]
        parca.append(_es_cerceve("Ç226", kol, g, "ABD", "R60", g.fark_60))
    return pd.concat(parca, ignore_index=True)


def es_oku_Ç204(K: Dict[str, Any]) -> pd.DataFrame:
    parca = []
    for yol in K["dosya"]:
        kol = pd.read_csv(_es_tam(yol), nrows=2).columns
        ad = os.path.basename(yol).replace("yk_", "").replace(".csv.gz", "")
        if ad == "TABAN":
            d = pd.read_csv(_es_tam(yol), usecols=["pazar", "sembol", "giris", "r15", "fark_Y1"])
            parca.append(_es_cerceve("Ç204", "Y1", d, d.pazar.to_numpy(), "r15", d.fark_Y1)); continue
        if ad == "TABAN_DS":
            d = pd.read_csv(_es_tam(yol), usecols=["pazar", "sembol", "giris", "r15", "fark_DS_ANA"])
            parca.append(_es_cerceve("Ç204", "DS_ANA", d, d.pazar.to_numpy(), "r15", d.fark_DS_ANA)); continue
        F = [c for c in kol if c.startswith("F_")]
        fk = {f: (f"fark_{f[2:]}" if f"fark_{f[2:]}" in kol else None) for f in F}
        d = pd.read_csv(_es_tam(yol), usecols=["pazar", "sembol", "giris", "r15"] + F + [v for v in fk.values() if v])
        for f in F:
            g = d[d[f] == 1]
            parca.append(_es_cerceve("Ç204", f"{ad}:{f[2:]}", g, g.pazar.to_numpy(), "r15", g[fk[f]] if fk[f] else None))
    return pd.concat(parca, ignore_index=True)


def es_oku_Ç191(K: Dict[str, Any]) -> pd.DataFrame:
    parca = []
    for yol in K["dosya"]:
        d = pd.read_csv(_es_tam(yol), usecols=["deneme", "pazar", "sembol", "giris"])
        parca.append(_es_cerceve("Ç191", d.deneme.to_numpy(), d, d.pazar.to_numpy(), None, None))
    return pd.concat(parca, ignore_index=True)


def es_oku_Ç189(K: Dict[str, Any]) -> pd.DataFrame:
    d = pd.read_csv(_es_tam(K["dosya"][0]), usecols=["satir", "pazar", "sembol", "giris", "r60", "fark"])
    return _es_cerceve("Ç189", d.satir.to_numpy(), d, d.pazar.to_numpy(), "r60", d.fark)


def es_oku_Ç99(K: Dict[str, Any]) -> pd.DataFrame:
    d = pd.read_csv(_es_tam(K["dosya"][0]), usecols=["sembol", "giris", "r60", "fark", "olay"])
    d = d[d.olay.isin(["alim", "buyuk", "col_alim"])]
    return _es_cerceve("Ç99", d.olay.to_numpy(), d, "BIST", "r60", d.fark)


ES_OKU: Dict[str, Callable[[Dict[str, Any]], pd.DataFrame]] = {
    "Ç209": es_oku_Ç209, "Ç205": es_oku_Ç205, "Ç206": es_oku_Ç206, "Ç226": es_oku_Ç226, "Ç204": es_oku_Ç204, "Ç191": es_oku_Ç191,
    "Ç189": es_oku_Ç189, "Ç99": es_oku_Ç99}


def es_olaylar(kod: str) -> pd.DataFrame:
    K = ES_KAYIT[kod]; X = ES_OKU[kod](K)
    X = X[X.pazar.isin(K["pazar"])].copy()
    X["hucre"] = es_hucre_ata(X.giris, K["hucre"])
    X = X[X.hucre != "dis"].reset_index(drop=True)
    if (X.giris > pd.Timestamp(K["kesik"])).any():
        raise ESHata(f"K2: {kod} giriş kesikten sonra")
    return X[_ES_OLAY_KOL]


# ================================================================ 3) TABAN (aynı hisse bütün günleri; piyasa)
def es_veri(kaynak: str, pazar: str, kesik: str) -> Dict[str, pd.DataFrame]:
    """Kaydın kendi verisi, kesikte KESİLMİŞ (kesik sonrası bar hiçbir hesaba girmez; assert)."""
    yol = ES_VERI[kaynak].format(p=pazar)
    if not os.path.exists(yol):
        raise ESHata(f"K11: veri yok {yol} (python FON_IZI.py vpac /tmp/iv/veri /tmp/veri)")
    V = pickle.load(open(yol, "rb")); ks = pd.Timestamp(kesik); out = {}
    for s, d in V.items():
        d = d[d.index <= ks]
        if len(d):
            out[str(s)] = d
    if max(d.index.max() for d in out.values()) > ks:
        raise ESHata("K2: kesik sonrası bar kaldı")
    return out


def es_R_gecerli(d: pd.DataFrame, H: int) -> Tuple[np.ndarray, np.ndarray]:
    """CETVEL2 R_H: giriş barı i (geçerli: High > Low, Volume > 0, Open > 0), çıkış = i'den itibaren H'inci geçerli barın kapanışı. (tarih, R)."""
    o = d.Open.to_numpy(float); h = d.High.to_numpy(float); lo = d.Low.to_numpy(float); c = d.Close.to_numpy(float); v = d.Volume.to_numpy(float)
    with np.errstate(invalid="ignore"):
        m = np.isfinite(o) & np.isfinite(c) & (o > 0) & (h > lo) & (v > 0)
    t = d.index.to_numpy()[m]; o = o[m]; c = c[m]; n = len(o); H = int(H)
    if n < H:
        return np.array([], "datetime64[ns]"), np.array([])
    return t[:n - H + 1], c[H - 1:] / o[:n - H + 1] - 1


def es_taban_uzun(V: Dict[str, pd.DataFrame], kural: str, H: int, kesik: str) -> Dict[str, Any]:
    """Bütün hisse x bütün giriş günleri: uzun diziler (j, gün indeksi, R). Takvim = pazarın birleşik takvimi."""
    S = sorted(V)
    if kural == "gecerli":
        cal = pd.DatetimeIndex(np.unique(np.concatenate([V[s].index.values.astype("datetime64[ns]") for s in S])))
        J, D, R = [], [], []
        for j, s in enumerate(S):
            t, r = es_R_gecerli(V[s], H)
            if len(t):
                J.append(np.full(len(t), j, np.int32)); D.append(cal.get_indexer(pd.DatetimeIndex(t)).astype(np.int32)); R.append(r)
        J = np.concatenate(J); D = np.concatenate(D); R = np.concatenate(R)
    elif kural == "fi_olcut":
        import FON_IZI as F   # yalnız okunur (kütüphane); fi_olcut_panel kriz = kayıt kesiği
        if int(F.FI_OLCUT["ufuk"]) != int(H):
            raise ESHata(f"K5: FI_OLCUT ufku {F.FI_OLCUT['ufuk']} != {H}")
        O = dict(F.FI_OLCUT); O["kriz"] = kesik
        P = F.fi_olcut_panel(V, O); cal = P["tarih"]; S = P["sembol"]
        Op = pd.DataFrame({s: V[s].Open for s in S}).reindex(cal).to_numpy(float)
        with np.errstate(invalid="ignore"):
            ok = np.isfinite(P["R"]) & np.isfinite(Op) & (Op > 0)
        D, J = np.nonzero(ok); R = P["R"][D, J]; D = D.astype(np.int32); J = J.astype(np.int32)
    else:
        raise ESHata(f"K5: bilinmeyen kural {kural}")
    if (D < 0).any():
        raise ESHata("K10: takvim eşlemesi")
    ok = np.isfinite(R)
    return {"S": S, "kol": {s: j for j, s in enumerate(S)}, "cal": cal, "J": J[ok], "D": D[ok], "R": R[ok]}


def es_piyasa(T: Dict[str, Any], en_az: Optional[int] = None) -> np.ndarray:
    """PİYASA(gün) = o gün giriş yapılabilen bütün hisselerin R_H eşit ağırlıklı ortalaması (en az 30 hisse; olay günleri dahil)."""
    n = len(T["cal"]); s = np.bincount(T["D"], weights=T["R"], minlength=n); c = np.bincount(T["D"], minlength=n)
    with np.errstate(invalid="ignore", divide="ignore"):
        P = s / c
    P[c < int(en_az or ES_ESIK["piyasa"]["en_az_hisse"])] = np.nan
    return P


def es_T1_T2(T: Dict[str, Any], P: np.ndarray, bas: str, son: str) -> Tuple[np.ndarray, float, int]:
    """Hücre [bas, son]: T1[j] = hissenin dönemdeki BÜTÜN günlerinde R_H ortalaması; T2 = PİYASA'nın dönemdeki bütün günlerinin ortalaması."""
    cal = T["cal"]; a = cal.searchsorted(pd.Timestamp(bas), "left"); b = cal.searchsorted(pd.Timestamp(son), "right")
    m = (T["D"] >= a) & (T["D"] < b); u = len(T["S"])
    s = np.bincount(T["J"][m], weights=T["R"][m], minlength=u); c = np.bincount(T["J"][m], minlength=u)
    with np.errstate(invalid="ignore", divide="ignore"):
        T1 = np.where(c > 0, s / np.maximum(c, 1), np.nan)
    pp = P[a:b]; pp = pp[np.isfinite(pp)]
    return T1, (float(pp.mean()) if len(pp) else float("nan")), int(len(pp))


def es_olay_R_fiyat(T: Dict[str, Any], sembol: np.ndarray, giris: np.ndarray) -> np.ndarray:
    """Olayın fiyattan R'si (aynı kural; taban uzun dizisinden (j, gün) eşlemesiyle)."""
    u = len(T["S"]); key_t = T["J"].astype(np.int64) * (len(T["cal"]) + 1) + T["D"].astype(np.int64)
    o = np.argsort(key_t); kt = key_t[o]; Rt = T["R"][o]
    j = np.array([T["kol"].get(str(s), -1) for s in sembol], np.int64)
    d = T["cal"].get_indexer(pd.DatetimeIndex(giris)).astype(np.int64)
    out = np.full(len(j), np.nan); ok = (j >= 0) & (d >= 0)
    q = j[ok] * (len(T["cal"]) + 1) + d[ok]; p = np.searchsorted(kt, q); p = np.minimum(p, len(kt) - 1)
    hit = kt[p] == q; v = np.full(ok.sum(), np.nan); v[hit] = Rt[p[hit]]; out[ok] = v
    _ = u
    return out


# ================================================================ 4) İSTATİSTİK
def es_boot(x: np.ndarray, ay: np.ndarray) -> Dict[str, Any]:
    """Ay kümeli bootstrap (B 2.000, tohum 11; her hücre için taze üreteç): KISA_UFUK.ku_boot (ort, medyan, alt, üst, tek yönlü p)."""
    import KISA_UFUK as KU   # yalnız okunur (ku_boot)
    x = np.asarray(x, float); ay = np.asarray(ay, str)
    u, k = np.unique(ay, return_inverse=True); K = len(u)
    rng = np.random.default_rng(int(ES_ESIK["boot"]["tohum"]))
    W = rng.multinomial(K, np.full(K, 1.0 / K), size=int(ES_ESIK["boot"]["B"])).astype(float)
    return KU.ku_boot(x, k, W)


def es_bh(p: List[Optional[float]], q: float) -> List[Optional[float]]:
    import MUM_IZI_HAVUZ as HV   # yalnız okunur (_hv_bh: BH düzeltilmiş p)
    return HV._hv_bh(p, q)


def es_kol_karar(H: Dict[str, Dict[str, Any]], olcu: str) -> Dict[str, Any]:
    """Bir kol (bütün hücreleri) için önceden yazılı karar parçası (BH öncesi)."""
    E = ES_ESIK["karar"]; buyuk = {h: c for h, c in H.items() if c["n"] >= int(E["hucre_n"])}
    if len(buyuk) < int(E["en_az_hucre"]):
        return {"durum": "ÖLÇÜLEMEDİ", "neden": f"n >= {E['hucre_n']} hücre {len(buyuk)} < {E['en_az_hucre']}", "p": None, "hucre": sorted(buyuk)}
    az_ay = [h for h, c in buyuk.items() if c["ay"] < int(E["ay"])]
    if az_ay:
        return {"durum": "ÖLÇÜLEMEDİ", "neden": f"ayrı ay < {E['ay']}: {az_ay}", "p": None, "hucre": sorted(buyuk)}
    b = [buyuk[h][olcu] for h in sorted(buyuk)]
    hepsi_arti = all(x["alt"] is not None and x["alt"] > 0 for x in b)
    hepsi_eksi = all(x["ust"] is not None and x["ust"] < 0 for x in b)
    ps = [x["p"] for x in b]
    p = max(ps) if all(v is not None for v in ps) else None
    return {"durum": "ADAY_ONCESI" if hepsi_arti else ("EKSI" if hepsi_eksi else "YOK"), "p": p, "hucre": sorted(buyuk)}


# ================================================================ 5) SAYIM / SAĞLAMA (getirisiz)
def es_kaynak_sha(kod: str) -> Dict[str, str]:
    return {p: es_sha_dosya(_es_tam(p)) for p in ES_KAYIT[kod]["dosya"]}


def es_sayim(secim: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kayıt x kol x hücre: n (dosyada R'si olan ya da fiyattan ölçülecek), ayrı ay sayısı. Getiri DEĞERİ okunmaz (yalnız sonlu mu)."""
    sec = secim or es_secim(); out: Dict[str, Any] = {"secim": sec, "kayit": {}, "kod_sha": es_kod_sha(), "esik_sha": es_esik_sha()}
    for kod in sec["secilen"]:
        X = es_olaylar(kod); K = ES_KAYIT[kod]
        has = np.isfinite(X.R_dosya.to_numpy(float)) if X.R_dosya.notna().any() else np.ones(len(X), bool)
        kol: Dict[str, Any] = {}
        Xh = X[has].copy(); Xh["ph"] = Xh.pazar + "|" + Xh.hucre
        for (k, h), g in Xh.groupby(["kol", "ph"]):
            kol.setdefault(str(k), {})[h] = {"n": int(len(g)), "ay": es_ay_sayisi(g.giris)}
        out["kayit"][kod] = {"ad": K["ad"], "H": K["H"], "kural": K["kural"], "kaynak": K["kaynak"], "kesik": K["kesik"], "hucre_tanim": K["hucre"],
                             "olay_satiri": int(len(X)), "R_dosyada": bool(X.R_dosya.notna().any()), "kol": kol, "kaynak_sha": es_kaynak_sha(kod)}
        eslog.info("sayım %s: %d olay satırı, %d kol", kod, len(X), len(kol))
    return out


def es_dogrula(secim: Optional[Dict[str, Any]] = None, n: int = 500) -> Dict[str, Any]:
    """Giriş kuralı sağlaması: dosya R'si ile aynı kural ve veriden fiyattan R (rastgele n olay; yalnız |fark| < 1e-6 oranı). Fark / taban hesaplanmaz."""
    sec = secim or es_secim(); out: Dict[str, Any] = {}
    for kod in sec["secilen"]:
        K = ES_KAYIT[kod]; X = es_olaylar(kod); o = {}
        for p in K["pazar"]:
            g = X[X.pazar == p]
            if not len(g):
                continue
            V = es_veri(K["kaynak"], p, K["kesik"]); T = es_taban_uzun(V, K["kural"], K["H"], K["kesik"])
            if g.R_dosya.notna().any():
                s = g[np.isfinite(g.R_dosya.to_numpy(float))]
                s = s.drop_duplicates(["sembol", "giris"]).sample(min(n, len(s)), random_state=11)
                rf = es_olay_R_fiyat(T, s.sembol.to_numpy(), s.giris.to_numpy()); e = np.abs(rf - s.R_dosya.to_numpy(float))
                o[p] = {"orneklem": int(len(s)), "fiyatta_bulunan": int(np.isfinite(rf).sum()), "birebir": int((e < 1e-6).sum())}
            else:
                rf = es_olay_R_fiyat(T, g.sembol.to_numpy(), g.giris.to_numpy())
                o[p] = {"orneklem": int(len(g)), "fiyatta_bulunan": int(np.isfinite(rf).sum()), "birebir": None}
            del V, T
        out[kod] = o; eslog.info("sağlama %s: %s", kod, o)
    return out


# ================================================================ 6) ÖN KAYIT
ES_KONTROL_YANIT: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban aynı hissenin aynı hücre dönemindeki BÜTÜN günleri (T1) ve aynı gün evren ortalaması (PİYASA); aynı giriş / çıkış "
                   "geometrisi (kaydın kendi kuralı, stop / hedef yok: mekanik üstünlük yok); eşli taban zaten eski kayıtta (eski fark yan sütunda)"),
    "K2": ("EVET", "olay kümeleri kayıtların mühürlü dosyalarından aynen; veri kayıt kesiğinde kesilir (es_veri assert); giriş > kesik olay durur; "
                   "T1 / PİYASA yalnız giriş sonrası H bar (sonuç değişkeni, karar girdisi değil)"),
    "K3": ("EVET", "gecerli kuralında giriş ve sayılan barlar High > Low ve Volume > 0 (CETVEL2 R_H); fi_olcut FON_IZI.fi_olcut_panel aynen; "
                   "sağlama dosya R'si ile birebir oranı ön kayıtta"),
    "K4": ("EVET", "olay kümesi kaydın kendi tekilleştirmesiyle aynen (yeniden süzülmez); n = dosyadaki olay satırı; hücrede ortalama + medyan"),
    "K5": ("EVET", "giriş = dosyanın 'giris' günü açılışı (sinyalden sonraki ilk işlem günü), kapanış değil; T1 aynı kuralla"),
    "K6": ("EVET", "fiyat kaydın kendi veri dosyası (V_* ya da V_*2, tek kip); AVR yerel para; bölünme düzeltmesi kaynak paketlerde yapılmış"),
    "K7": ("EVET", "evren bugünün listesi (V_*); geniş evren V_*2 batanları kısmen içerir; raporda 'yukarı yanlı' uyarısı zorunlu"),
    "K8": ("EVET", "karar hücreleri n >= 100 ve ayrı ay >= 12; n < 100 hücre karara girmez (bilgi); BH q 0,10 bütün ölçülebilir kollarda"),
    "K9": ("EVET", "seçim, sayım, sağlama, karar kuralı ve kod sha bu dosyada; bu dosya commit + push edildikten sonra ölçüm (olcum kapısı commit "
                   "zamanını ve kod sha'yı denetler); eşik sonuçtan sonra değişmez, değişirse SAPMA"),
    "K10": ("EVET", "dosya sütunları okuyucularda zorunlu (eksikse durur); sağlama: rastgele 500 olayda dosya R'si = fiyattan R; haber ayrıştırma yok"),
    "K11": ("EVET", "ölçümden sonra iki kayıt-hücre satır dosyasından bağımsız kodla (düz pandas) yeniden üretilir ve raporda yazılır"),
    "K12": ("EVET", "'iz' sözü yok; en fazla ZAMANLAMA / TOPLAM ADAYI (aynı veride yeniden okuma; ileri test gerekir); sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı modül sonunda; yasak defter dosyalarına dokunulmaz (git diff denetimi); yalnız kendi yollar commit; e-posta / "
                    "anahtar taraması çıktılarda"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para kararı yok; yalnız eski kayıtların yeniden okunması"),
}


def es_kontrol_tablo() -> str:
    import IZ_KARNE as IK   # yalnız okunur
    s = ["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = ES_KONTROL_YANIT[k["kod"]]
        s.append(f"| {k['kod']} | {k['ad']} | {y} | {kn} |")
    return "\n".join(s)


def es_onkayit_yaz(S: Dict[str, Any], DG: Dict[str, Any], cikti: Optional[str] = None) -> str:
    sec = S["secim"]; L = ["# ES_YENIDEN ÖN KAYIT — eski 'iz değil'lerin rastgele güne göre yeniden okunması, birinci parti (27 Kasım 2026)", "",
                          f"Kod: ES_YENIDEN.py sha {S['kod_sha']} (eşik / kayıt tanımı sha {S['esik_sha']}). İş tanımı: ES_YENIDEN_IS_TANIMI.md. "
                          "Bu dosya ölçümden ÖNCE commit + push edilir; ölçüm (`python ES_YENIDEN.py olcum`) bu dosyanın commit'ini, push'unu, kontrol "
                          "kapısını ve kod sha'sını denetler, BİR KEZ koşar. Bu bir AYNI VERİDE YENİDEN OKUMADIR (kör değil).", "",
                          "## 1. Seçim (getirisiz)", "",
                          "Kural: envanter Liste 1 sırası (envanterin 'Dosya satırı' sütunu, büyükten küçüğe = olay sayısı sırası), kapalı konu değil, "
                          "kayıt tarihi < 2026-11-26, olay >= 300, dosya okunabilir ve giriş kuralı sabit ufuklu; en çok 20; aynı olay kümesini paylaşan "
                          "kayıtlar tek satır.", "",
                          "| # | Ç | Ad | Kaynak veri | Kural | H | Veri kesiği | Hücreler (giriş günü) | Olay satırı | Paylaşan |", "|---|---|---|---|---|---|---|---|---|---|"]
    for i, kod in enumerate(sec["secilen"], 1):
        K = ES_KAYIT[kod]; r = S["kayit"][kod]
        hc = "; ".join(f"{a} {b[0]}..{b[1]}" for a, b in K["hucre"].items())
        L.append(f"| {i} | {kod} | {K['ad']} | {K['kaynak']} ({', '.join(K['pazar'])}) | {K['kural']} | {K['H']} | {K['kesik']} | {hc} | "
                 f"{r['olay_satiri']} | {', '.join(sec['paylasan'].get(kod, [])) or '—'} |")
    L += ["", "Kaynak tanımları (giriş kuralı / ufuk / hücre kayıttan):", ""]
    for kod in sec["secilen"]:
        L.append(f"- {kod}: {ES_KAYIT[kod]['kaynak_not']}. Eski hüküm: {ES_KAYIT[kod]['eski']}.")
    for kod, nt in ES_PAYLASAN_NOT.items():
        L.append(f"- Paylaşılan küme ({kod}): {nt}.")
    L += ["", "Atlananlar (Liste 1 sırasıyla):", "", "| Ç | Neden |", "|---|---|"]
    for a in sec["atlanan"]:
        L.append(f"| {a['kod']} | {a['neden']} |")
    L += ["", "## 2. Getirisiz sayım (kayıt x kol x hücre: n / ayrı ay)", "",
          "n = dosyada R'si sonlu olan olay (R dosyada yoksa giriş günü kayıtlı olay); ölçümde ayrıca T1 ve PİYASA tanımlı olmalı (raporda son n).", ""]
    for kod in sec["secilen"]:
        r = S["kayit"][kod]; hs = sorted({h for v in r["kol"].values() for h in v})
        L += [f"### {kod} ({len(r['kol'])} kol; kaynak sha {', '.join(f'{os.path.basename(a)} {b}' for a, b in r['kaynak_sha'].items())})", "",
              "| Kol | " + " | ".join(hs) + " |", "|---|" + "---|" * len(hs)]
        for k in sorted(r["kol"]):
            L.append(f"| {k} | " + " | ".join(f"{r['kol'][k][h]['n']} / {r['kol'][k][h]['ay']}" if h in r["kol"][k] else "—" for h in hs) + " |")
        L.append("")
    L += ["## 3. Giriş kuralı sağlaması (dosya R'si = aynı kural ve veriden fiyattan R; rastgele <= 500 olay, |fark| < 1e-6)", "",
          "| Ç | Pazar | Örneklem | Fiyatta bulunan | Birebir |", "|---|---|---|---|---|"]
    for kod, o in DG.items():
        for p, v in o.items():
            L.append(f"| {kod} | {p} | {v['orneklem']} | {v['fiyatta_bulunan']} | {v['birebir'] if v['birebir'] is not None else 'R dosyada yok (fiyattan)'} |")
    L += ["", "## 4. Ölçü ve karar (iş tanımı 2. bölüm AYNEN; önceden)", "",
          "- R = dosyadaki H ufuklu getiri (yoksa aynı kuralla fiyattan). T1 = aynı hissenin hücre dönemindeki BÜTÜN günlerinde (olay günleri dahil) aynı "
          "kuralla R_H ortalaması. PİYASA(t) = giriş günü t'de pazarın evrenindeki (kaynak veri dosyasındaki bütün hisseler) giriş yapılabilen bütün "
          "hisselerin R_H eşit ağırlıklı ortalaması (en az 30 hisse). T2 = PİYASA'nın hücre dönemindeki bütün günlerinin ortalaması.",
          "- TOPLAM = R - T1; ZAMANLAMA = PİYASA(t) - T2; SEÇİM = TOPLAM - ZAMANLAMA. Hücre = kaydın kendi pazar x dönem hücresi. Ay kümeli bootstrap "
          "%95 (2.000, tohum 11), tek yönlü p = (1 + #(tekrar <= 0)) / (B + 1); ayrı ay sayısı; eski hüküm ve eski eşli fark (dosyanın fark sütunu, "
          "varsa) yan sütunda. Olay T1 ya da PİYASA tanımsızsa ölçülmez (sayısı raporda).",
          f"- KARAR: {ES_ESIK['karar']['tanim']}", "- Karar birimi = kayıt x kol (bir kaydın her kolu ayrı hipotezdir; kayıt satırı kollarının sayımıdır).",
          "- Uyarılar (raporda zorunlu): aynı veride yeniden okuma (kör değil); yaşayan evren (yukarı yanlı); zamanlama farkı olayların belirli piyasa "
          "dönemlerine yığılmasından gelebilir (ay kümesi ve ay sayısı şartı bu yüzden). Kayıtların bir kısmı (Ç204'teki Cemal kuralları) görsel "
          "onaydan geçmemiş dedektörlerdir: sonuçlar 'dedektörün bulduğu bölgeler' diye sınırlı okunur.",
          "- Bağımsız yeniden üretim: ölçümden sonra iki kayıt-hücre satır dosyasından düz pandas ile (TOPLAM / ZAMANLAMA / SEÇİM ortalaması ve n).", "",
          "## 5. KONTROL LİSTESİ", "", es_kontrol_tablo(), ""]
    yol = _es_yol(ES_DOSYA["onkayit"], cikti)
    with open(yol, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return yol


# ================================================================ 7) ÖLÇÜM
def _git(*a: str) -> str:
    return subprocess.run(["git", *a], cwd=KOK_ES, capture_output=True, text=True, check=True).stdout.strip()


def es_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    """Ölçüm kapısı: ön kayıt var + commit'li + push'lu + kendi dosyalarında değişiklik yok + kontrol kapısı + kod sha ön kayıtla aynı + daha önce koşulmamış."""
    import IZ_KARNE as IK
    ok_yol = _es_yol(ES_DOSYA["onkayit"], cikti); rel = os.path.relpath(ok_yol, KOK_ES)
    if not os.path.exists(ok_yol):
        raise ESHata("K9: ön kayıt yok")
    ck = _git("log", "-1", "--format=%H %cI", "--", rel)
    if not ck:
        raise ESHata("K9: ön kayıt commit'lenmemiş")
    if _git("status", "--porcelain", "--", rel, "ES_YENIDEN.py"):
        raise ESHata("K9: ön kayıt ya da kod commit sonrası değişmiş")
    _git("fetch", "-q", "origin")
    dal = _git("rev-parse", "--abbrev-ref", "HEAD")
    if _git("rev-parse", "HEAD") != _git("rev-parse", f"origin/{dal}"):
        raise ESHata("K9: push edilmemiş")
    metin = open(ok_yol, encoding="utf-8").read()
    if f"sha {es_kod_sha()}" not in metin:
        raise ESHata("K9: kod sha ön kayıttakiyle aynı değil")
    if f"sha {es_esik_sha()}" not in metin:
        raise ESHata("K9: eşik sha ön kayıttakiyle aynı değil")
    IK.ik_kontrol_kapisi(ok_yol)
    if os.path.exists(_es_yol(ES_DOSYA["ozet"], cikti)):
        raise ESHata("K9: ölçüm daha önce koşuldu (bir kez)")
    return {"onkayit_commit": ck, "kod_sha": es_kod_sha(), "esik_sha": es_esik_sha(), "zaman": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def es_kayit_hesap(kod: str) -> pd.DataFrame:
    """Bir kaydın olay satırları: R, T1, PİYASA, T2, TOPLAM, ZAMANLAMA, SEÇİM."""
    K = ES_KAYIT[kod]; X = es_olaylar(kod); parca = []
    for p in K["pazar"]:
        g = X[X.pazar == p].copy()
        if not len(g):
            continue
        V = es_veri(K["kaynak"], p, K["kesik"]); T = es_taban_uzun(V, K["kural"], K["H"], K["kesik"]); del V
        P = es_piyasa(T)
        g["R_fiyat"] = es_olay_R_fiyat(T, g.sembol.to_numpy(), g.giris.to_numpy())
        g["R"] = np.where(np.isfinite(g.R_dosya.to_numpy(float)), g.R_dosya.to_numpy(float), g.R_fiyat.to_numpy(float))
        if g.R_dosya.notna().any():   # dosyada R olan kayıtta R'si olmayan olay (pencere taşan) ölçülmez
            g.loc[~np.isfinite(g.R_dosya.to_numpy(float)), "R"] = np.nan
        d = T["cal"].get_indexer(pd.DatetimeIndex(g.giris)); g["PIY"] = np.where(d >= 0, P[np.maximum(d, 0)], np.nan)
        g["T1"] = np.nan; g["T2"] = np.nan; g["T2_gun"] = 0
        jj = np.array([T["kol"].get(s, -1) for s in g.sembol], np.int64)
        for h, (a, b) in K["hucre"].items():
            T1, T2, ng = es_T1_T2(T, P, a, b); m = (g.hucre == h).to_numpy()
            g.loc[m, "T1"] = np.where(jj[m] >= 0, T1[np.maximum(jj[m], 0)], np.nan); g.loc[m, "T2"] = T2; g.loc[m, "T2_gun"] = ng
        A = es_ayristir(g.R, g.T1, g.PIY, g.T2); g["TOPLAM"] = A["TOPLAM"]; g["ZAMANLAMA"] = A["ZAMANLAMA"]; g["SECIM"] = A["SECIM"]
        parca.append(g); del T
        eslog.info("hesap %s %s: %d olay, ölçülen %d", kod, p, len(g), int(np.isfinite(g.TOPLAM).sum()))
    return pd.concat(parca, ignore_index=True)


def es_hucre_ozet(g: pd.DataFrame) -> Dict[str, Any]:
    f = np.isfinite(g.TOPLAM.to_numpy(float)) & np.isfinite(g.ZAMANLAMA.to_numpy(float)); g = g[f]
    o: Dict[str, Any] = {"n": int(len(g)), "ay": es_ay_sayisi(g.giris) if len(g) else 0}
    if len(g) < 2:
        return o
    ay = es_ay(g.giris)
    for c in ("TOPLAM", "ZAMANLAMA", "SECIM"):
        o[c] = es_boot(g[c].to_numpy(float), ay)
    o["R_ort"] = float(g.R.mean()); o["T1_ort"] = float(g.T1.mean()); o["PIY_ort"] = float(g.PIY.mean()); o["T2"] = float(g.T2.iloc[0])
    ef = g.eski_fark.to_numpy(float); o["eski_fark"] = float(np.nanmean(ef)) if np.isfinite(ef).any() else None
    sy = pd.Series(ay).value_counts(); o["ust3_ay_pay"] = float(sy.iloc[:3].sum() / len(g))
    return o


def es_olcum_hesap(secilen: List[str], cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    ham = ham or ES_YOL["ham"]; os.makedirs(ham, exist_ok=True); J: Dict[str, Any] = {"kayit": {}}
    for kod in secilen:
        Xk = es_kayit_hesap(kod)
        Xk.to_csv(os.path.join(ham, f"es_satir_{kod}.csv.gz"), index=False, compression="gzip")
        kols: Dict[str, Any] = {}
        for k, gk in Xk.groupby("kol"):
            H = {f"{p}|{h}": es_hucre_ozet(gh) for (p, h), gh in gk.groupby(["pazar", "hucre"])}
            kols[str(k)] = {"hucre": H, "olay": int(len(gk)), "olculemeyen": int((~np.isfinite(gk.TOPLAM.to_numpy(float))).sum()),
                            "ZAMANLAMA": es_kol_karar(H, "ZAMANLAMA"), "TOPLAM": es_kol_karar(H, "TOPLAM")}
        J["kayit"][kod] = {"ad": ES_KAYIT[kod]["ad"], "H": ES_KAYIT[kod]["H"], "kural": ES_KAYIT[kod]["kural"], "eski": ES_KAYIT[kod]["eski"],
                           "kol": kols, "satir": os.path.join(ham, f"es_satir_{kod}.csv.gz")}
        del Xk
    # BH (ayrı aileler: ZAMANLAMA, TOPLAM) = ölçülebilir bütün kollar
    for olcu in ("ZAMANLAMA", "TOPLAM"):
        ad = [(kod, k) for kod, r in J["kayit"].items() for k, v in r["kol"].items() if v[olcu]["durum"] != "ÖLÇÜLEMEDİ"]
        q = es_bh([J["kayit"][a][ "kol"][b][olcu]["p"] for a, b in ad], float(ES_ESIK["karar"]["bh_q"]))
        for (a, b), qq in zip(ad, q):
            v = J["kayit"][a]["kol"][b][olcu]; v["bh_q"] = qq
            if v["durum"] == "ADAY_ONCESI":
                v["karar"] = f"{olcu} ADAYI" if (qq is not None and qq <= float(ES_ESIK["karar"]["bh_q"])) else "EMARE"
            else:
                v["karar"] = v["durum"]
        for kod, r in J["kayit"].items():
            for k, v in r["kol"].items():
                v[olcu].setdefault("karar", v[olcu]["durum"]); v[olcu].setdefault("bh_q", None)
        J[f"bh_aile_{olcu}"] = len(ad)
    return J


def es_olcum(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    kp = es_kapi(cikti); sec = es_secim()
    eslog.info("kapı geçti: %s", kp)
    J = es_olcum_hesap(sec["secilen"], cikti, ham); J["kapi"] = kp; J["surum"] = ES_SURUM; J["secim"] = sec; J["esik"] = ES_ESIK
    J["bitti"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    yol = _es_yol(ES_DOSYA["ozet"], cikti)
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1, default=lambda x: None if isinstance(x, float) and not np.isfinite(x) else str(x))
    return J


# ================================================================ 8) RAPOR
def _f(x: Any, n: int = 2) -> str:
    return "—" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{100 * x:+.{n}f}"


def _ga(b: Optional[Dict[str, Any]]) -> str:
    if not b or b.get("ort") is None:
        return "—"
    return f"{_f(b['ort'])} [{_f(b.get('alt'))}; {_f(b.get('ust'))}]"


def es_rapor_yaz(cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    J = json.load(open(_es_yol(ES_DOSYA["ozet"], cikti), encoding="utf-8"))
    ekyol = os.path.join(ham or ES_YOL["ham"], "es_rapor_ek.json"); EK = json.load(open(ekyol, encoding="utf-8")) if os.path.exists(ekyol) else {}
    L = ["# ES_YENIDEN RAPOR — eski 'iz değil'lerin aynı hissenin bütün günlerine göre yeniden okunması, birinci parti (27 Kasım 2026)", "",
         f"Ön kayıt: ES_YENIDEN_ON_KAYIT.md (commit {J['kapi']['onkayit_commit']}); ölçüm bir kez ({J['kapi']['zaman']} - {J['bitti']}); kod sha "
         f"{J['kapi']['kod_sha']}. Birim yüzde puan (H ufuklu getiri farkı). GA = ay kümeli bootstrap %95. Bu AYNI VERİDE YENİDEN OKUMADIR (kör değil): "
         "hiçbir satır 'iz' değildir; en fazla ADAY (ileri test gerekir).", ""]
    ad = {o: [] for o in ("ZAMANLAMA", "TOPLAM")}
    for kod, r in J["kayit"].items():
        for k, v in r["kol"].items():
            for o in ad:
                if v[o]["karar"] in (f"{o} ADAYI", "EMARE"):
                    ad[o].append((kod, k, v[o]["karar"], v[o]["bh_q"]))
    L += ["## SONUÇ", "", f"BH aileleri: ZAMANLAMA {J['bh_aile_ZAMANLAMA']} kol, TOPLAM {J['bh_aile_TOPLAM']} kol (ölçülebilir kollar).", ""]
    for o in ad:
        L.append(f"- {o}: " + ("; ".join(f"{a} {b} {c} (BH q {_q(d)})" for a, b, c, d in ad[o]) if ad[o] else "aday / emare yok"))
    L += ["", "Kayıt özeti (kol sayıları, ZAMANLAMA kararı / TOPLAM kararı):", "",
          "| Ç | Ad | H | Kol | ZAM ADAY | ZAM EMARE | ZAM EKSİ | ZAM YOK | ÖLÇÜLEMEDİ | TOP ADAY | TOP EMARE | TOP EKSİ | Eski hüküm |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for kod, r in J["kayit"].items():
        z = [v["ZAMANLAMA"]["karar"] for v in r["kol"].values()]; t = [v["TOPLAM"]["karar"] for v in r["kol"].values()]
        L.append(f"| {kod} | {r['ad']} | {r['H']} | {len(z)} | {z.count('ZAMANLAMA ADAYI')} | {z.count('EMARE')} | {z.count('EKSI')} | {z.count('YOK')} | "
                 f"{z.count('ÖLÇÜLEMEDİ')} | {t.count('TOPLAM ADAYI')} | {t.count('EMARE')} | {t.count('EKSI')} | {r['eski']} |")
    for b in ("KONTROL LİSTESİ", "HATA", "SAPMA", "YENİDEN ÜRETİM", "UYARILAR", "ÖNERİLEN DEFTER SATIRLARI"):
        L += ["", f"## {b}", ""] + (EK.get(b) or ["(yok)"])
    L += ["", "## TABLO: kayıt x kol x hücre", "",
          "n / ay = ölçülen olay / ayrı ay; değerler yüzde puan ort [GA]; eski fark = dosyanın eşli fark sütunu ortalaması (varsa).", ""]
    for kod, r in J["kayit"].items():
        L += [f"### {kod} — {r['ad']} (H {r['H']}, {r['kural']}; eski: {r['eski']})", "",
              "| Kol | Hücre | n / ay | TOPLAM | ZAMANLAMA | SEÇİM | Eski fark | ZAM karar | TOP karar |", "|---|---|---|---|---|---|---|---|---|"]
        for k, v in r["kol"].items():
            for h, c in v["hucre"].items():
                L.append(f"| {k} | {h} | {c['n']} / {c['ay']} | {_ga(c.get('TOPLAM'))} | {_ga(c.get('ZAMANLAMA'))} | {_ga(c.get('SECIM'))} | "
                         f"{_f(c.get('eski_fark'))} | {v['ZAMANLAMA']['karar']} | {v['TOPLAM']['karar']} |")
        L.append("")
    yol = _es_yol(ES_DOSYA["rapor"], cikti)
    with open(yol, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return yol


def _q(x: Any) -> str:
    return "—" if x is None else f"{x:.3f}"


def es_sizinti_tara(yollar: List[str]) -> List[str]:
    """E-posta / anahtar benzeri dizgi taraması (K13)."""
    bul = []
    for y in yollar:
        if not os.path.exists(y):
            continue
        ac = gzip.open if y.endswith(".gz") else open
        with ac(y, "rt", encoding="utf-8", errors="ignore") as f:
            m = f.read()
        if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", m) or re.search(r"(api[_-]?key|token|secret)\s*[:=]\s*\S{8,}", m, re.I):
            bul.append(y)
    return bul


# ================================================================ çakışma kapısı
def _cakisma_kontrol_es(_once=_CK_ONCE_ES, _dosya="ES_YENIDEN.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_ES",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_es()


def _es_ana(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(__doc__); return 0
    k = argv[0]; ham = ES_YOL["ham"]; os.makedirs(ham, exist_ok=True)
    try:
        if k == "secim":
            print(json.dumps(es_secim(), ensure_ascii=False, indent=1))
        elif k == "sayim":
            S = es_sayim(); json.dump(S, open(os.path.join(ham, "es_sayim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print({kod: (r["olay_satiri"], len(r["kol"])) for kod, r in S["kayit"].items()})
        elif k == "dogrula":
            D = es_dogrula(); json.dump(D, open(os.path.join(ham, "es_dogrula.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1); print(D)
        elif k == "onkayit":
            S = json.load(open(os.path.join(ham, "es_sayim.json"), encoding="utf-8")); D = json.load(open(os.path.join(ham, "es_dogrula.json"), encoding="utf-8"))
            if S["kod_sha"] != es_kod_sha() or S["esik_sha"] != es_esik_sha():
                raise ESHata("K9: sayım eski kodla alınmış; yeniden sayım")
            print(es_onkayit_yaz(S, D))
        elif k == "olcum":
            J = es_olcum(); print({kod: len(r["kol"]) for kod, r in J["kayit"].items()})
        elif k == "rapor":
            print(es_rapor_yaz())
        elif k == "sha":
            print(json.dumps({"kod": es_kod_sha(), "esik": es_esik_sha()}))
        else:
            print(__doc__); return 2
    except ESHata as ex:
        eslog.error("DURDU: %s", ex); return 1
    return 0


if __name__ == "__main__":
    sys.exit(_es_ana())
