"""VDYT2-B — VDYT2 SAĞLAMASI (v2b_20261112): A) MUTLAK HAREKET etiketiyle başarı (1); B) BATANLAR DAHİL (Tiingo; ABD) başarı (1). Tek dosya.

Cemal'in kararı (12 Kasım 2026, aynen): 'İkisini de yap. Önce bir saatlik ön kayıt ve ölçütleri sabitleme; sonra veri çekme ve test. Özellikle başarısız
örnekleri dışarıda bırakmayalım. Aksi hâlde yalnızca başarılı hisseleri inceleyerek sistemi olduğundan iyi sanabiliriz.'

Bu iş bir SAĞLAMADIR: VDYT2 sonuçları ve IZ_KARNE Ç163 kararı DEĞİŞMEZ. VDYT2.py ve VDYT.py İÇE AKTARILIR, DEĞİŞTİRİLMEZ (ön kayıttaki sha256'ları `kos` denetler).
KASA bu işte yeniden 'açılmaz': VDYT2'de açılmış KASA dönemi aynı veriyle sağlama için kullanılır (yeni karar değil).
A) Büyük hareket etiketi bölgeden BAĞIMSIZ ve mutlak: MA1 (ANA) = t'den sonraki 20 işlem gününde |ln(C[t+k] / C[t])| en büyüğü >= max(ln 1,15; 3 σ √20);
   σ = t'ye kadar (t dahil) son 250 günlük log getirinin std'si. MA2 (uç nokta), MA3 (gerçek aralık >= 3 x ATR250) BİLGİ. Satırlar VDYT2 (1) satırlarının AYNISI.
B) Tiingo ücretsiz katmanıyla borsadan çıkmış / batmış ABD hisseleri: önce 12 sembollük DOĞRULAMA PİLOTU (önceden yazılı ölçütler), sonra tabakalı rastgele
   örneklem (en çok 450 + yedek; tohum sabit; liste çekimden ÖNCE dosyada), ters olasılık ağırlığıyla 'BATANLAR DAHİL' başarı (1).

Komut:  python VDYT2B.py liste                  supported_tickers (anahtarsız açık dosya) -> evren sayımı + tabakalı örneklem dosyası (Tiingo FİYAT isteği YOK)
        python -I VDYT2B.py kapsam             A için YALNIZ SAYIM (MA etiketi ölçülebilir satır sayısı; oran YOK)
        python VDYT2B.py onkayit               ön kaydı yazar (eşik mührü, kod / VDYT2 / VDYT sha256, tablo ve liste sha256, kapsam); git'e işlenmişse üzerine yazmaz
        python VDYT2B.py pilot                 yalnız pilot sembolleri (Tiingo; en çok 12 istek) + pilot kararı (GÜVENİLİR / KISMEN / GÜVENİLMEZ)
        python VDYT2B.py cek                   örneklem (kaldığı yerden sürer; saatte 45, günde 900, ayda 500 farklı sembol sert sınırı; önbellek /tmp/vdyt2b/tiingo)
        python -I VDYT2B.py kos --test A       mutlak sağlama (Tiingo gerekmez); ön kayıt git'e işlenmemiş / değişmişse REDDEDER
        python -I VDYT2B.py kos --test B       batanlar dahil (pilot GÜVENİLİR / KISMEN ve çekim tamam değilse REDDEDER)
        python VDYT2B.py rapor --test A|B      raporu sonuç JSON'undan yeniden yazar
Anahtar: YALNIZ ortamdan (TIINGO_API_KEY); yoksa 'Token proxy' (oturumun ağ vekili başlığı enjekte edebilir). Anahtar loglanmaz, dosyaya yazılmaz.
Veri: Tiingo fiyatları lisans gereği repoya KONMAZ (/tmp/vdyt2b/tiingo). Repoya yalnız ön kayıt, örneklem listesi (kodlar), sayım ve sonuç dosyaları.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_VDYT2B = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import zipfile  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_VDYT2B = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_VDYT2B not in sys.path:
    sys.path.insert(0, KOK_VDYT2B)
import VDYT as V1  # noqa: E402  (VDYT sürüm 1; DEĞİŞTİRİLMEZ)
import VDYT2 as V2  # noqa: E402  (VDYT sürüm 2; DEĞİŞTİRİLMEZ)

v2blog = logging.getLogger("col.vdyt2b")
if not v2blog.handlers:
    _v2b_h = logging.StreamHandler(sys.stderr)
    _v2b_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s vdyt2b: %(message)s", "%H:%M:%S"))
    v2blog.addHandler(_v2b_h)
    v2blog.setLevel(logging.INFO)
    v2blog.propagate = False

VDYT2B_ETIKET = "v2b_20261112"
VDYT2B_SURUM = "VDYT2-B v1.0 (v2b_20261112): Faz 1 (ön kayıt, kod + sentetik test, yalnız sayım; Tiingo fiyat isteği yok); ölçüm Faz 2'de"

VDYT2B_YOL: Dict[str, str] = {
    "cikti": os.environ.get("VDYT2B_CIKTI", os.path.join(KOK_VDYT2B, "arastirma_cikti", "vdyt", "v2_20261112")),
    "ara": os.environ.get("VDYT2B_ARA", "/tmp/vdyt2b"),
    "tablo": os.environ.get("VDYT2B_TABLO", "/tmp/vdyt2/kasa"),       # VDYT2 `kos --asama kasa` ara tabloları (satır / kontrol; wf ile içerik aynı)
}
VDYT2B_DOSYA: Dict[str, str] = {
    "onkayit": "VDYT2B_ON_KAYIT.md", "liste": "vdyt2b_orneklem.tsv", "evren": "vdyt2b_evren_sayim.json", "kapsam": "vdyt2b_kapsam_A.json",
    "pilot": "vdyt2b_pilot.json", "sonuc_A": "vdyt2b_sonuc_A.json", "sonuc_B": "vdyt2b_sonuc_B.json", "rapor_A": "VDYT2B_RAPOR_A.md",
    "rapor_B": "VDYT2B_RAPOR_B.md", "cek": "vdyt2b_cek_durum.json",
}
_V2B_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")
_V2B_ABD_TATIL = None   # (önbellek) ABD federal tatil takvimi iş günü nesnesi

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256 mührü ön kayıtta; sonuç görüldükten sonra değişmez)
VDYT2B_ESIK: Dict[str, Any] = {
    "surum_etiket": VDYT2B_ETIKET,
    "kesik": "2026-08-31",
    # VDYT2 ön kaydındaki değerler (VDYT2_ON_KAYIT.md): `kos` VDYT2.py / VDYT.py sha256'larını ve VDYT2 eşik mührünü bunlarla karşılaştırır (değişmişse ret)
    "vdyt2": {"esik_sha": "3051e5b8ddd99c7c42e36f106bdaede734e8dac5ed6588029c5d50bc2274f5a8",
              "kod_sha": "e33b2fd1c611e32930e8e8af29b9a4a9e86607a1df303e0fae8d9e94d0a30741",
              "vdyt_kod_sha": "10ead8062c2c8ec25984a23b68b299cec4d8a7cfd144ad22e542e867d40c932d",
              "onkayit_commit": "f13b96e", "karar": "Ç163: (1) BAŞARILI, (2) ve (3) BAŞARISIZ (DEĞİŞMEZ)"},
    "donem": {"wf": ["2019-01-01", "2023-12-31"], "kasa": ["2024-01-01", "2026-08-31"]},
    "basari": copy.deepcopy(V2.VDYT2_ESIK["basari"]),     # hisse kümeli bootstrap B = 2000, tohum 20261112, %95
    "A": {
        "ufuk": 20, "sigma_n": 250, "sigma_min": 200, "atr_n": 250, "atr_min": 200,
        "MA1": {"taban_yuzde": 0.15, "k_sigma": 3.0, "olcu": "max_k |ln(C[t+k]/C[t])|, k = 1..20 >= max(ln(1+taban), k_sigma x sigma x sqrt(20))"},
        "MA2": {"k_sigma": 2.0, "olcu": "|ln(C[t+20]/C[t])| >= k_sigma x sigma x sqrt(20)"},
        "MA3": {"k_atr": 3.0, "olcu": "max_k TR[t+k], k = 1..20 >= k_atr x ATR250[t]"},
        "yon": "ilk eşiği aşan taraf (MA1: ilk aşan günün ln işareti; MA2: uç nokta işareti; MA3: ilk büyük TR gününün C - C[-1] işareti)",
        "ana_etiket": "MA1", "bilgi_etiket": ["MA2", "MA3"], "pazarlar": ["BIST", "ABD"], "ana_tanim": "G5", "ana_onkosul": "P1",
        "ma23_tanim": ["G5"], "bh1_ayni_satir_tanim": ["G5"],
        "kontrol": {"DISARI": ["sembol", "yil", "natr_d"], "RASTGELE": ["yil", "yas"]},
        "satir": "VDYT2 (1) satırları aynen (tarih dönemde, son20 <= dönem sonu, y20 ölçülebilir) VE MA etiketi ölçülebilir (t+20 veri içinde, (t, t+20] "
                 "kopukluk yok, sigma / ATR250 tanımlı)",
        "tablolar": ["satir", "kontrol"],
    },
    "B": {
        "tiingo": {"liste_url": "https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip",
                   "fiyat_url": "https://api.tiingo.com/tiingo/daily/{kod}/prices", "baslangic": "2010-01-01", "bitis": "2026-08-31",
                   "saat_istek": 45, "gun_istek": 900, "ay_sembol": 500, "zaman_asimi": 60, "bekle_429": 900, "art_arda_429_dur": 3,
                   "anahtar_ortam": "TIINGO_API_KEY", "anahtar_yok": "proxy"},
        "pilot": {
            # Bilinen (EDGAR, yerel dizin; SEC'e istek yok) Form 25-NSE tarihi: borsanın kotasyondan çıkarma bildirimi. Tür: Q = bütün geçmiş bugünkü OTC 'Q'
            # kodunda (Tiingo listesinde başlangıç borsa döneminden); BORSA = borsa dönemi ayrı kayıt (OTC dönemi ayrı Q kodu); YENIDEN = kod yeniden kullanımı.
            "semboller": [
                {"kod": "SIVBQ", "sirket": "SVB Financial Group", "cik": 719739, "f25": "2023-05-02", "tur": "Q", "liste": "PINK 1990-03-26 .. 2026-11-11"},
                {"kod": "BBBYQ", "sirket": "Bed Bath & Beyond", "cik": 886158, "f25": "2023-07-10", "tur": "Q", "liste": "PINK 1992-06-05 .. 2023-09-29"},
                {"kod": "RADCQ", "sirket": "Rite Aid", "cik": 84129, "f25": "2023-10-31", "tur": "Q", "liste": "PINK 1984-12-17 .. 2026-11-11"},
                {"kod": "WEWKQ", "sirket": "WeWork", "cik": 1813756, "f25": "2023-11-22", "tur": "Q", "liste": "EXPM 2020-10-21 .. 2024-06-11"},
                {"kod": "SHLDQ", "sirket": "Sears Holdings", "cik": 1310067, "f25": "2018-11-15", "tur": "Q", "liste": "EXPM 2003-05-01 .. 2022-10-31 (SHLD bugün ETF)"},
                {"kod": "HTZGQ", "sirket": "Hertz Global (eski hisse)", "cik": 1657853, "f25": "2020-10-30", "tur": "Q", "liste": "PINK 2006-11-16 .. 2021-06-30"},
                {"kod": "REVRQ", "sirket": "Revlon", "cik": 887921, "f25": "2022-10-21", "tur": "Q", "liste": "PINK 1996-02-29 .. 2023-05-24"},
                {"kod": "YELLQ", "sirket": "Yellow Corp", "cik": 716006, "f25": "2023-09-08", "tur": "Q", "liste": "OTCMKTS 1986-07-09 .. 2026-07-01"},
                {"kod": "DNR", "sirket": "Denbury Resources", "cik": 945764, "f25": "2020-08-17", "tur": "BORSA", "liste": "NYSE 1995-09-06 .. 2020-07-30 (DNRCQ ayrı)"},
                {"kod": "GNC", "sirket": "GNC Holdings", "cik": 1502034, "f25": "2020-07-01", "tur": "BORSA", "liste": "NYSE 2011-04-01 .. 2020-06-30 (GNCIQ ayrı)"},
                {"kod": "SUNE", "sirket": "SunEdison (kod bugün SUNation)", "cik": 945436, "f25": "2016-05-06", "tur": "YENIDEN",
                 "liste": "iki kayıt: NYSE 1995-07-13 .. 2016-04-21 ve NASDAQ 1990-03-26 .. 2026-11-11", "yeni_bas": "2016-04-22",
                 "yahoo_karsilastir": "k34_yahoo SUNE (bugünkü şirket)"},
                {"kod": "CHK", "sirket": "Chesapeake Energy (2020 iflas; eski hisse 2021-02-09 iptal, yeni hisse 2021-02-10, aynı kod)", "cik": 895126,
                 "f25": "2020-07-20", "tur": "YENIDEN", "liste": "NASDAQ 1993-02-16 .. 2024-10-04; CHKAQ NYSE 2021-03-17 .. 2021-05-17; EXE 2021-02-10 ..",
                 "yeni_bas": "2021-02-10", "yahoo_karsilastir": "k60_fiyat EXE (yeni hisse; 2021-02-10 .. 2024-10-01 örtüşme)"},
            ],
            "basin_kapanis": {"SIVBQ": [["2023-03-09", 106.04, "basın: SVB hissesi 9 Mart 2023'te %60 düşüşle 106,04 $ kapandı"]]},
            "olcut": {
                "K1_seri": "HTTP 200 ve kapanışı > 0 en az 252 bar",
                "K2_son_gun": "BORSA: son bar ∈ [F25 - 60 iş günü, F25 + 10 iş günü] (borsa önce işlemi durdurur, Form 25 sonra; Kural 12d2-2); Q: son bar >= F25 - 60 "
                              "iş günü ve seride [F25 - 60, F25 + 10] iş günü penceresinde en az 1 bar (borsa dönemi kotasyondan çıkışa kadar seride); YENIDEN: "
                              "seride F25 - 60 iş gününden önceki 60 iş gününde bar var (eski şirketin dönemi seride)",
                "K3_bosluk": "A = (BORSA: son bar; Q / YENIDEN: F25 - 60 iş günü); [A - 60 iş günü, A] penceresinde eksik iş günü <= 5 ve en uzun boşluk <= 5 iş günü "
                             "(iş günü: ABD federal tatil takvimi)",
                "K4_tutarlilik": "kaynak varsa: basın kapanışı ±%10 içinde (bölünmesiz ham kapanış); Yahoo örtüşmesi: ortak günlerde günlük log getiri korelasyonu "
                                 ">= 0,90 ve |kapanış oranı - 1| medyanı <= %2 (bölünme düzeltmeli); kaynak yoksa DEĞERLENDİRİLMEDİ (karara girmez)",
                "K5_ohlcv": "barların >= %95'inde açılış / yüksek / düşük / kapanış / hacim dolu ve yüksek >= düşük ve kapanış > 0",
                "K6_karisma": "YENIDEN: seri hem eski (yeni_bas'tan önceki 250 iş günü) hem yeni dönemi (yeni_bas'tan sonraki 250 iş günü) içeriyorsa aralarında "
                              ">= 30 iş günü boşluk olmalı (ayırt edilebilir); yoksa KARIŞIK. Diğerleri: bölünme günü olmayan |günlük ln getiri| > ln 10 sıçrama yok",
            },
            "karar": {"gecti": "K1 VE K2 VE K3 VE K5 VE K6 VE (K4 değerlendirildiyse K4)", "guvenilir_min": 10, "kismen_min": 7,
                      "yeniden_karisik": "iki YENIDEN sembolünün ikisi de KARIŞIK ise karar en çok KISMEN",
                      "q_hepsi_kaldi": "Q türünün HİÇBİRİ geçmezse OTCQ tabakası B'den çıkarılır (beyan; örneklemden düşer, ağırlıkta yer almaz)"},
            "kos_izin": ["GÜVENİLİR", "KISMEN"],
        },
        "evren": {
            "borsa": ["NYSE", "NASDAQ", "NYSE MKT", "AMEX"],
            "otc": ["PINK", "OTCMKTS", "EXPM", "OTCGREY", "OTCQB", "OTCQX", "OTCBB", "OTCCE", "OTCD"],
            "asset": "Stock", "para": "USD", "kod_regex": "^[A-Z]{1,5}$", "bes_harf_at": "FGHIMNOPRSTUVWXYZ",
            "son_bas": "2019-02-01", "son_bit": "2026-06-30", "min_omur_gun": 400, "otcq_regex": "^[A-Z]{3,4}Q$", "otcq_bas_ust": "2025-06-30",
            "ayrik_otc_gun": 10, "spac_unite_ek": ["U", "-U"], "spac_unite_gun": 30, "k60_klasor": "/tmp/k60_fiyat",
            "kural": [
                "1 tür: assetType Stock, priceCurrency USD",
                "2 kod: ^[A-Z]{1,5}$ (nokta / tire / rakam yok: imtiyazlı, sınıf, birim); 5 harfli kodlarda son harf F G H I M N O P R S T U V W X Y Z ise atılır "
                "(yabancı, tahvil, imtiyazlı, hak, fayda payı, varant, birim, when-issued, fon, ADR); Q (iflas) ve A-E, J-L kalır",
                "3 yinelenen kod: aynı kod listede birden çok Stock kaydıyla geçiyorsa (kod yeniden kullanımı; API hangi seriyi verir belirsiz) atılır",
                "4 k60'ta olan kod atılır (yaşayan evren zaten VDYT2'de)",
                "5 BORSA kaynağı: exchange ∈ borsa, endDate ∈ [son_bas, son_bit], startDate <= endDate - 400 gün",
                "6 OTCQ kaynağı: exchange ∈ otc, kod ^[A-Z]{3,4}Q$ (iflas eki), endDate >= son_bas, startDate <= min(endDate - 400 gün, otcq_bas_ust); "
                "AYRIK OTC dönemi (ilk 3 harfi aynı bir borsa kaydının endDate'i Q kaydının startDate'inden en çok 10 gün önce / sonra) atılır (borsa dönemi "
                "BORSA kaynağında)",
                "7 SPAC kabuğu (çekim öncesi): kod + U ya da kod + -U birim kaydı varsa VE birimin endDate'i >= kodun endDate'i - 30 gün (birleşmeden önce "
                "tasfiye / birleşme yok) atılır; birleşip yaşayan / sonra batan şirket (birimi erken biten) KALIR",
            ],
        },
        "orneklem": {"n": 450, "yedek": 38, "tohum": 20261117, "tabaka": ["kaynak", "son_yil"], "dagitim": "orantılı, en büyük kalan; N_h > 0 ise en az 1",
                     "otcq_hala": "OTCQ'da endDate > son_bit ise son_yil = 'OTC_HALA' (hâlâ OTC'de işlem görüyor)",
                     "sira": "tabaka içinde numpy default_rng(tohum + tabaka sırası) permütasyonu; ilk n_h ANA, sonraki y_h YEDEK",
                     "yedek_kural": "YEDEK yalnız aynı tabakada VERİ YOK (HTTP 404 / boş / temiz bar < 252) olan ANA sembolün yerine, sırayla; başka hiçbir "
                                    "nedenle (sonuç, getiri, etiket) yedek kullanılmaz ve sembol çıkarılmaz"},
        "cekim_sonrasi": {
            "D1_veri_yok": "HTTP 404 / boş / temiz bar < 252 -> VERİ YOK (yedekle değiştirilir; raporda listelenir)",
            "D2_spac_kalibi": {"aralik": [9.0, 11.0], "pay": 0.80, "kural": "ham kapanışların >= %80'i [9, 11] $ aralığında -> SPAC kabuğu (evren dışı; "
                                                                             "değiştirilmez; raporda listelenir)"},
            "D4_yeniden_ad": {"son_bar": 60, "min_ortak": 55, "korelasyon": 0.98, "oran_std": 0.01,
                              "kural": "son 60 barın günlük ln getirisi bir k60 serisiyle (ortak gün >= 55) korelasyon >= 0,98 VE ln(kapanış oranı) std <= 0,01 "
                                       "-> KOD DEĞİŞİKLİĞİ (aynı şirket yaşayan evrende; ör. CHK -> EXE) -> evren dışı (değiştirilmez; raporda listelenir)"},
            "D3_uygun_gun_yok": "VDYT uygunluğu (>= 252 bar, ekrandaki fiyat >= 2 $, 20 gün medyan işlem değeri >= 1 mn $) hiç sağlanmayan sembol ÇIKARILMAZ "
                                "(evrenin üyesidir; satırı olmaz, ağırlık paydasında kalır)",
            "fiyat": "Tiingo ham açılış / yüksek / düşük / kapanış / hacim + splitFactor: bölünme düzeltmeli seri = ham / (gelecekteki bölünme oranlarının çarpımı) "
                     "(Yahoo / k60 ile aynı tür: bölünme düzeltmeli, temettü düzeltmesiz); hacim x aynı çarpım; ekrandaki fiyat = ham kapanış "
                     "(meta 'bolunme' ile V1.vdyt_bolunme_carpan aynı sonucu verir); V1.vdyt_bar_temizle + 2010-01-01 .. 2026-08-31 kesiti",
        },
        "agirlik": "tabaka h: w_h = N_h / m_h (m_h = h'de verisi gelen örneklem sayısı; SPAC kalıbı ve kod değişikliği dahil: evren dışı payı N_h'yi aynı "
                   "oranda küçültür); yaşayan (k60) satırlar w = 1",
        "kolon": ["sembol", "kaynak", "t", "tarih", "yil", "yas", "natr_d", "P1", "P2", "y20", "son20", "yon", "r20", "mae", "ma1", "ma1_yon", "w"],
        "tanim": "G5", "onkosul": ["P0", "P1", "P2"], "etiket": ["y20", "MA1"],
        "panel": "ABD paneli k60 + batan örneklemi BİRLİKTE (V1.vdyt_panel; uygunluk, NATR ondalığı, tertiller); batan satırları bu panelle V2._v2_hisse_is "
                 "(tanım yalnız G5); yaşayan satırlar VDYT2 tablolarından AYNEN (yeniden hesaplanmaz)",
        "bilgi": ["yalnız batanlar: gerçek / DIŞARI / RASTGELE oranları (ağırlıklı)", "batanlarda (2) / (3) bilgi: y20 = 1 satırlarda yukarı payı, r20 ortalaması, MAE"],
    },
    "karar": {
        "A": "(1)-MUTLAK BAŞARILI <=> ANA (G5, P1), etiket MA1: gerçek - DIŞARI (tabakalı) fark > 0 ve %95 alt > 0 VE gerçek - RASTGELE fark > 0 ve alt > 0; "
             "WF'de VE KASA'da; BIST ve ABD AYRI. n < 30 ya da tek sınıf -> VERİ YOK",
        "B": "(1)-BATANLAR DAHİL BAŞARILI <=> ABD, ANA (G5, P1), birleşik ağırlıklı evren: aynı kural (iki kontrol, WF VE KASA); etiket y20 (BH1; VDYT2 ile aynı) "
             "ve MA1 ayrı sütun",
    },
}


class Vdyt2bHata(RuntimeError):
    """VDYT2-B durdurucu hata (ön kayıt yok / değişmiş / git'e işlenmemiş, VDYT2 kodu değişmiş, tablo / liste sha256 farklı, hız sınırı, pilot / çekim eksik)."""


# ---------------------------------------------------------------- 0) YARDIMCILAR
def _v2b_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _v2b_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or VDYT2B_YOL["cikti"], VDYT2B_DOSYA.get(ad, ad))


def _v2b_ara(*parca: str) -> str:
    y = os.path.join(VDYT2B_YOL["ara"], *parca)
    os.makedirs(os.path.dirname(y) if os.path.splitext(y)[1] else y, exist_ok=True)
    return y


def _v2b_anahtar() -> str:
    """Tiingo anahtarı YALNIZ ortamdan; yoksa 'proxy' (ağ vekili başlığı enjekte edebilir). Değer hiçbir yere yazılmaz."""
    return os.environ.get(VDYT2B_ESIK["B"]["tiingo"]["anahtar_ortam"], "").strip() or VDYT2B_ESIK["B"]["tiingo"]["anahtar_yok"]


def _v2b_temiz(metin: str) -> str:
    """Log / dosya metninden anahtarı ve e-posta biçimli parçaları siler."""
    a = os.environ.get(VDYT2B_ESIK["B"]["tiingo"]["anahtar_ortam"], "").strip()
    m = str(metin)
    if a and len(a) >= 4:
        m = m.replace(a, "***")
    return _V2B_EPOSTA.sub("***", m)


def _v2b_yaz(yol: str, metin: str) -> str:
    a = os.environ.get(VDYT2B_ESIK["B"]["tiingo"]["anahtar_ortam"], "").strip()
    if a and len(a) >= 4 and a in metin:
        raise Vdyt2bHata(f"{os.path.basename(yol)}: metinde Tiingo anahtarı var; yazılmadı")
    if _V2B_EPOSTA.search(metin):
        raise Vdyt2bHata(f"{os.path.basename(yol)}: metinde e-posta biçimli parça var; yazılmadı")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    gec = yol + ".yaz"
    with open(gec, "w", encoding="utf-8") as f:
        f.write(metin)
    os.replace(gec, yol)
    return yol


def _v2b_json(yol: str, obj: Any) -> str:
    return _v2b_yaz(yol, json.dumps(V2._v2_kayit(obj), ensure_ascii=False, indent=1, default=str, sort_keys=True))


def _v2b_json_oku(yol: str) -> Any:
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def v2b_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: VDYT2B_ESIK (sıralı JSON)."""
    return hashlib.sha256(json.dumps(E or VDYT2B_ESIK, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")).hexdigest()


def v2b_kod_sha(yol: Optional[str] = None) -> str:
    return V1.vdyt_sha_dosya(yol or os.path.join(KOK_VDYT2B, "VDYT2B.py"))


def _v2b_is_gunu() -> Any:
    global _V2B_ABD_TATIL
    if _V2B_ABD_TATIL is None:
        from pandas.tseries.holiday import USFederalHolidayCalendar
        from pandas.tseries.offsets import CustomBusinessDay
        _V2B_ABD_TATIL = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    return _V2B_ABD_TATIL


def _v2b_is_kaydir(gun: Any, k: int) -> pd.Timestamp:
    return pd.Timestamp(gun) + int(k) * _v2b_is_gunu()


def _v2b_is_gunleri(a: Any, b: Any) -> pd.DatetimeIndex:
    return pd.date_range(pd.Timestamp(a), pd.Timestamp(b), freq=_v2b_is_gunu())


# ---------------------------------------------------------------- 1) A: MUTLAK HAREKET ETİKETLERİ (yalnız t ve öncesiyle eşik; t sonrası yalnız etikette)
def v2b_sigma(c: np.ndarray, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """σ[t] = std(ln C[j] / C[j-1], j = t-249 .. t) (ddof 1; en az sigma_min geçerli getiri). Yalnız t ve öncesi."""
    A = (E or VDYT2B_ESIK)["A"]; c = np.asarray(c, float)
    with np.errstate(invalid="ignore", divide="ignore"):
        lr = np.log(c / np.r_[np.nan, c[:-1]])
    return pd.Series(lr).rolling(int(A["sigma_n"]), min_periods=int(A["sigma_min"])).std(ddof=1).to_numpy()


def v2b_atr250(tr: np.ndarray, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """ATR250[t] = ortalama TR[t-249 .. t] (en az atr_min). Yalnız t ve öncesi (bölgeden bağımsız)."""
    A = (E or VDYT2B_ESIK)["A"]
    return pd.Series(np.asarray(tr, float)).rolling(int(A["atr_n"]), min_periods=int(A["atr_min"])).mean().to_numpy()


def v2b_ma_etiket(ts: np.ndarray, c: np.ndarray, tr: np.ndarray, kop: np.ndarray, E: Optional[Dict[str, Any]] = None,
                  sig: Optional[np.ndarray] = None, atr: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """Karar günleri ts için MA1 / MA2 / MA3 (1 / 0 / NaN) ve yönleri (+1 / -1 / 0 / NaN). Eşikler yalnız t ve öncesinden (σ, ATR250); etiket (t, t+20].
    NaN <=> t + 20 > son bar ya da (t, t+20] içinde kopukluk ya da σ (MA1 / MA2) / ATR250 (MA3) tanımsız."""
    E = E or VDYT2B_ESIK; A = E["A"]; H = int(A["ufuk"]); c = np.asarray(c, float); tr = np.asarray(tr, float); n = len(c)
    ts = np.asarray(ts, np.int64); m = len(ts)
    sig = v2b_sigma(c, E) if sig is None else sig; atr = v2b_atr250(tr, E) if atr is None else atr
    out = {k: np.full(m, np.nan) for k in ("ma1", "ma1_yon", "ma2", "ma2_yon", "ma3", "ma3_yon", "sigma", "atr250", "ma1_esik", "ma1_k")}
    if not m:
        return out
    kc = np.r_[0, np.cumsum(np.asarray(kop, bool).astype(np.int64))]
    ok = (ts >= 1) & (ts + H <= n - 1)
    tt = np.where(ok, ts, 0)
    ok &= (kc[np.minimum(tt + H + 1, n)] - kc[np.minimum(tt + 1, n)]) == 0
    K = tt[:, None] + np.arange(1, H + 1)[None, :]; K = np.minimum(K, n - 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        P = np.log(c[K] / c[tt][:, None]); s = sig[tt]; at = atr[tt]
        e1 = np.maximum(np.log1p(float(A["MA1"]["taban_yuzde"])), float(A["MA1"]["k_sigma"]) * s * np.sqrt(H))
        h1 = np.abs(P) >= e1[:, None]; v1 = h1.any(1); k1 = np.where(v1, h1.argmax(1), -1)
        y1 = np.where(v1, np.sign(P[np.arange(m), np.maximum(k1, 0)]), 0.0)
        e2 = float(A["MA2"]["k_sigma"]) * s * np.sqrt(H); son = P[:, -1]; v2 = np.abs(son) >= e2; y2 = np.where(v2, np.sign(son), 0.0)
        TRk = tr[K]; h3 = TRk >= float(A["MA3"]["k_atr"]) * at[:, None]; v3 = h3.any(1); k3 = np.where(v3, h3.argmax(1), -1)
        g3 = tt + 1 + np.maximum(k3, 0); y3 = np.where(v3, np.sign(c[np.minimum(g3, n - 1)] - c[np.maximum(g3 - 1, 0)]), 0.0)
    ok1 = ok & np.isfinite(s) & np.all(np.isfinite(P), 1); ok3 = ok & np.isfinite(at) & np.all(np.isfinite(TRk), 1)
    out["ma1"] = np.where(ok1, v1.astype(float), np.nan); out["ma1_yon"] = np.where(ok1, y1, np.nan)
    out["ma2"] = np.where(ok1, v2.astype(float), np.nan); out["ma2_yon"] = np.where(ok1, y2, np.nan)
    out["ma3"] = np.where(ok3, v3.astype(float), np.nan); out["ma3_yon"] = np.where(ok3, y3, np.nan)
    out["sigma"] = np.where(ts >= 0, sig[tt], np.nan); out["atr250"] = at; out["ma1_esik"] = e1; out["ma1_k"] = np.where(ok1 & v1, k1 + 1, np.nan)
    return out


def v2b_ma_etiket_tek(t: int, c: np.ndarray, tr: np.ndarray, kop: np.ndarray, E: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    """v2b_ma_etiket'in tek satırlık, döngülü (elle doğrulanabilir) sürümü; testte vektörel sürümle karşılaştırılır."""
    E = E or VDYT2B_ESIK; A = E["A"]; H = int(A["ufuk"]); n = len(c)
    r = {k: np.nan for k in ("ma1", "ma1_yon", "ma2", "ma2_yon", "ma3", "ma3_yon")}
    if t < 1 or t + H > n - 1 or any(bool(kop[j]) for j in range(t + 1, t + H + 1)):
        return r
    lr = [np.log(c[j] / c[j - 1]) for j in range(max(1, t - int(A["sigma_n"]) + 1), t + 1)]
    lr = [x for x in lr if np.isfinite(x)]
    if len(lr) >= int(A["sigma_min"]):
        s = float(np.std(lr, ddof=1)); e1 = max(np.log(1.0 + float(A["MA1"]["taban_yuzde"])), float(A["MA1"]["k_sigma"]) * s * np.sqrt(H))
        r["ma1"], r["ma1_yon"] = 0.0, 0.0
        for k in range(1, H + 1):
            x = np.log(c[t + k] / c[t])
            if abs(x) >= e1:
                r["ma1"], r["ma1_yon"] = 1.0, float(np.sign(x)); break
        x = np.log(c[t + H] / c[t]); e2 = float(A["MA2"]["k_sigma"]) * s * np.sqrt(H)
        r["ma2"], r["ma2_yon"] = (1.0, float(np.sign(x))) if abs(x) >= e2 else (0.0, 0.0)
    w = [tr[j] for j in range(max(0, t - int(A["atr_n"]) + 1), t + 1) if np.isfinite(tr[j])]
    if len(w) >= int(A["atr_min"]):
        at = float(np.mean(w)); r["ma3"], r["ma3_yon"] = 0.0, 0.0
        for k in range(1, H + 1):
            if tr[t + k] >= float(A["MA3"]["k_atr"]) * at:
                r["ma3"], r["ma3_yon"] = 1.0, float(np.sign(c[t + k] - c[t + k - 1])); break
    return r


# ---------------------------------------------------------------- 2) A: VDYT2 SATIR TABLOLARI (yeniden hesaplanmaz; içerik sha256 ön kayıtta)
def _v2b_tablo_yol(tur: str, pazar: str, ad: str, kl: Optional[str] = None) -> str:
    return os.path.join(kl or VDYT2B_YOL["tablo"], f"{tur}_{pazar}_{ad}.csv.gz")


def v2b_tablo_listesi(pazarlar: Optional[List[str]] = None) -> List[Tuple[str, str, str]]:
    pazarlar = pazarlar or list(VDYT2B_ESIK["A"]["pazarlar"])
    return [(tur, pz, ad) for pz in pazarlar for ad in V2.VDYT2_ESIK["tanim"] for tur in VDYT2B_ESIK["A"]["tablolar"]]


def v2b_tablo_sha(pazarlar: Optional[List[str]] = None, kl: Optional[str] = None) -> Dict[str, str]:
    """Kullanılan VDYT2 ara tablolarının İÇERİK sha256'sı (gzip açılmış bayt; gzip başlığındaki zaman damgası sha'ya girmez). Yoksa 'YOK'."""
    out = {}
    for tur, pz, ad in v2b_tablo_listesi(pazarlar):
        y = _v2b_tablo_yol(tur, pz, ad, kl); h = hashlib.sha256()
        if not os.path.exists(y):
            out[os.path.basename(y)] = "YOK"; continue
        with gzip.open(y, "rb") as f:
            for blok in iter(lambda: f.read(1 << 20), b""):
                h.update(blok)
        out[os.path.basename(y)] = h.hexdigest()
    return out


def v2b_tablo_oku(tur: str, pazar: str, ad: str, kl: Optional[str] = None) -> pd.DataFrame:
    y = _v2b_tablo_yol(tur, pazar, ad, kl)
    if not os.path.exists(y):
        raise Vdyt2bHata(f"VDYT2 ara tablosu yok: {y} (VDYT2 `kos --asama kasa` ara çıktısı; yoksa aynı kodla yeniden üretilir, sha256 ön kayıtla tutmalı)")
    D = pd.read_csv(y, dtype={"sembol": str}, keep_default_na=True, na_values=[""])
    D["sembol"] = D.sembol.astype(str); D["tarih"] = pd.to_datetime(D.tarih); D["yil"] = D.tarih.dt.year
    for k in ("son5", "son10", "son20"):
        if k in D:
            D[k] = pd.to_datetime(D[k])
    return D


def v2b_etiketle(D: pd.DataFrame, F: Dict[str, Any], E: Optional[Dict[str, Any]] = None, E1: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Satır tablosuna MA etiketlerini ekler (hisse başına: temizlenmiş fiyat F['S'][s]; t = o serideki bar sırası). HİZALAMA DENETİMİ: her satırda
    tarih == gün[t] olmalı; tutmayan satır varsa Vdyt2bHata (yanlış seri / yanlış evren)."""
    E = E or VDYT2B_ESIK; E1 = E1 or V2._v2_e1()
    if not len(D):
        return D.assign(**{k: np.nan for k in ("ma1", "ma1_yon", "ma2", "ma2_yon", "ma3", "ma3_yon", "sigma", "atr250")})
    parca, eksik, uyumsuz = [], [], 0
    for s, g in D.groupby("sembol", sort=False):
        d = F["S"].get(s)
        if d is None:
            eksik.append(s); continue
        t = g.t.to_numpy(np.int64); n = len(d)
        if (t < 0).any() or (t >= n).any():
            uyumsuz += int(((t < 0) | (t >= n)).sum()); continue
        if not np.array_equal(d.index.to_numpy("datetime64[D]")[t], g.tarih.to_numpy("datetime64[D]")):
            uyumsuz += int((d.index.to_numpy("datetime64[D]")[t] != g.tarih.to_numpy("datetime64[D]")).sum()); continue
        c = d.c.to_numpy(float); Ol_tr = _v2b_tr(d); kop = V1.vdyt_kopuk(d.index, E1)
        M = v2b_ma_etiket(t, c, Ol_tr, kop, E)
        parca.append(g.assign(**{k: M[k] for k in ("ma1", "ma1_yon", "ma2", "ma2_yon", "ma3", "ma3_yon", "sigma", "atr250")}))
    if eksik or uyumsuz:
        raise Vdyt2bHata(f"hizalama tutmadı: fiyatı olmayan hisse {len(eksik)} (ilk: {eksik[:5]}), tarih != gün[t] satır {uyumsuz}; koşu durdu")
    return pd.concat(parca).sort_index() if parca else D.iloc[:0].assign(**{k: np.nan for k in ("ma1", "ma1_yon", "ma2", "ma2_yon", "ma3", "ma3_yon", "sigma", "atr250")})


def _v2b_tr(d: pd.DataFrame) -> np.ndarray:
    """Gerçek aralık (V1.vdyt_olculer ile aynı tanım)."""
    h, l, c = d.h.to_numpy(float), d.l.to_numpy(float), d.c.to_numpy(float); cp = np.r_[np.nan, c[:-1]]
    with np.errstate(invalid="ignore"):
        tr = np.nanmax(np.vstack([h - l, np.abs(h - cp), np.abs(l - cp)]), axis=0)
    tr[0] = h[0] - l[0]
    return tr


def v2b_donemde(D: pd.DataFrame, asama: str, etiket: str, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """VDYT2 (1) satır kümesi (tarih dönemde, son20 <= dönem sonu, y20 ölçülebilir) VE etiket ölçülebilir."""
    E = E or VDYT2B_ESIK; a, b = (pd.Timestamp(x) for x in E["donem"][asama])
    if not len(D):
        return D
    m = (D.tarih >= a) & (D.tarih <= b) & (D.son20 <= b) & D.y20.notna() & D[etiket].notna()
    return D[m]


# ---------------------------------------------------------------- 3) ORAN KARŞILAŞTIRMASI (ağırlıklı; ağırlık 1 iken V2.v2_oran_karsilastir ile aynı)
def v2b_oran_karsilastir(Dg: pd.DataFrame, Dk: pd.DataFrame, y: str, tabaka: List[str], E: Optional[Dict[str, Any]] = None,
                         agirlik: Optional[str] = None) -> Dict[str, Any]:
    """Gerçek oran - kontrol oranı (kontrol, tabaka içinde gerçeğin AĞIRLIKLI dağılımına yeniden ağırlıklı); hisse kümeli bootstrap (V1.vdyt_bootstrap_fark).
    agirlik: satır ağırlığı sütunu (ters olasılık; yoksa 1). Tabaka içinde: gerçek satır ağırlığı = w; kontrol = w x (Σw_gerçek / Σw_kontrol)."""
    E = E or VDYT2B_ESIK; B = E["basari"]
    kol = ["sembol", y] + [c for c in tabaka if c not in ("sembol", y)]
    if agirlik:
        kol = kol + [agirlik]
    U = pd.concat([Dg[kol].assign(g=1.0), Dk[kol].assign(g=0.0)], ignore_index=True)
    U = U[U[y].notna()]
    if not len(U) or U.g.nunique() < 2:
        return {"n1": int((U.g == 1).sum()) if len(U) else 0, "n0": int((U.g == 0).sum()) if len(U) else 0, "fark": np.nan, "alt": np.nan, "ust": np.nan,
                "p": np.nan}
    w0 = U[agirlik].to_numpy(float) if agirlik else np.ones(len(U)); g = U.g.to_numpy(float)
    k = U[tabaka].fillna(-1).reset_index(drop=True).groupby(list(tabaka), sort=False, dropna=False).ngroup().to_numpy(); m = int(k.max()) + 1
    s1 = np.bincount(k, weights=w0 * (g == 1), minlength=m); s0 = np.bincount(k, weights=w0 * (g == 0), minlength=m); iki = (s1 > 0) & (s0 > 0)
    with np.errstate(invalid="ignore", divide="ignore"):
        w = np.where(iki[k], np.where(g == 1, w0, w0 * s1[k] / s0[k]), 0.0)
    r = V1.vdyt_bootstrap_fark(U.sembol.to_numpy(), U[y].to_numpy(float), np.where(w > 0, g, np.nan), int(B["bootstrap"]), int(B["tohum"]),
                               tuple(B["guven"]), agirlik=w)
    r["n1_ham"] = int((g == 1).sum()); r["n0_ham"] = int((g == 0).sum()); r["n1_dusen"] = int(((g == 1) & (w <= 0)).sum())
    r["oran"] = float(r["ort1"] / r["ort0"]) if r.get("ort0") and np.isfinite(r.get("ort0", np.nan)) and r["ort0"] > 0 else np.nan
    return r


def v2b_karar_hucre(rd: Optional[Dict[str, Any]], rr: Optional[Dict[str, Any]], n_min: int = 30) -> str:
    """İki kontrol (DIŞARI, RASTGELE) için fark > 0 ve alt > 0 -> True; n < 30 ya da tanımsız -> VERİ YOK."""
    for r in (rd, rr):
        if not r or int(r.get("n1", 0) or 0) < n_min or int(r.get("n0", 0) or 0) < n_min or not np.isfinite(r.get("alt", np.nan) if r.get("alt") is not None else np.nan):
            return "VERİ YOK"
    return "TUTTU" if all((r.get("fark") or -1) > 0 and (r.get("alt") or -1) > 0 for r in (rd, rr)) else "TUTMADI"


def v2b_karar(wf: str, kasa: str) -> str:
    if "VERİ YOK" in (wf, kasa):
        return "VERİ YOK"
    return "BAŞARILI" if (wf == "TUTTU" and kasa == "TUTTU") else "BAŞARISIZ"


# ---------------------------------------------------------------- 4) A: KAPSAM (yalnız sayım) ve KOŞU
def _v2b_fiyat(pazar: str) -> Dict[str, Any]:
    return V2.v2_fiyat(pazar, canli=False)


@V2._v2_sessiz
def v2b_A_hazirla(pazarlar: Optional[List[str]] = None, F_ver: Optional[Dict[str, Dict[str, Any]]] = None, kl: Optional[str] = None,
                  tanimlar: Optional[List[str]] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Dict[str, pd.DataFrame]]]:
    """Pazar x tanım için VDYT2 gerçek + kontrol satırları + MA etiketleri (hizalama denetimli)."""
    E = E or VDYT2B_ESIK; pazarlar = pazarlar or list(E["A"]["pazarlar"]); out: Dict[str, Dict[str, Dict[str, pd.DataFrame]]] = {}
    for pz in pazarlar:
        F = (F_ver or {}).get(pz) or _v2b_fiyat(pz); out[pz] = {}
        for ad in (tanimlar or list(V2.VDYT2_ESIK["tanim"])):
            G = v2b_etiketle(v2b_tablo_oku("satir", pz, ad, kl), F, E); K = v2b_etiketle(v2b_tablo_oku("kontrol", pz, ad, kl), F, E)
            out[pz][ad] = {"G": G, "K": K}
            v2blog.info("A %s %s: gerçek %d, kontrol %d satır etiketlendi", pz, ad, len(G), len(K))
        del F
    return out


def v2b_A_kapsam(Z: Dict[str, Dict[str, Dict[str, pd.DataFrame]]], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """YALNIZ SAYIM: VDYT2 (1) satır kümesi ve bunun içinde MA1 / MA2 / MA3 ölçülebilir satır SAYISI (pazar x dönem x tanım x ön koşul x kaynak).
    Etiket DEĞERİ, oran, yön HESAPLANMAZ."""
    E = E or VDYT2B_ESIK; out: Dict[str, Any] = {"zaman": _v2b_simdi(), "surum": VDYT2B_SURUM, "kod_sha256": v2b_kod_sha(), "sayim": []}
    for pz, T in Z.items():
        for ad, GK in T.items():
            for asama in ("wf", "kasa"):
                a, b = (pd.Timestamp(x) for x in E["donem"][asama])
                for kaynak, D in (("GERCEK", GK["G"]), ("DISARI", GK["K"][GK["K"].kaynak == "DISARI"] if len(GK["K"]) else GK["K"]),
                                  ("RASTGELE", GK["K"][GK["K"].kaynak == "RASTGELE"] if len(GK["K"]) else GK["K"])):
                    if not len(D):
                        continue
                    D0 = D[(D.tarih >= a) & (D.tarih <= b) & (D.son20 <= b) & D.y20.notna()]
                    for p in ("P0", "P1", "P2"):
                        Dp = D0 if p == "P0" else D0[D0[p] == 1]
                        out["sayim"].append({"pazar": pz, "tanim": ad, "asama": asama, "kaynak": kaynak, "onkosul": p, "vdyt2_satir": int(len(Dp)),
                                             "ma1_olculebilir": int(Dp.ma1.notna().sum()), "ma2_olculebilir": int(Dp.ma2.notna().sum()),
                                             "ma3_olculebilir": int(Dp.ma3.notna().sum()), "hisse": int(Dp.sembol.nunique())})
    return out


def v2b_A_analiz(Z: Dict[str, Dict[str, Dict[str, pd.DataFrame]]], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """A koşusu: MA1 (bütün tanımlar x ön koşul x kontrol; WF ve KASA), MA2 / MA3 ve aynı satırlarda BH1 (G5; bilgi), yön payı (bilgi); karar tablosu."""
    E = E or VDYT2B_ESIK; A = E["A"]; sat, yon = [], []
    for pz, T in Z.items():
        for ad, GK in T.items():
            etiketler = ["ma1"] + (["ma2", "ma3"] if ad in A["ma23_tanim"] else []) + (["y20"] if ad in A["bh1_ayni_satir_tanim"] else [])
            for asama in ("wf", "kasa"):
                for et in etiketler:
                    ref = "ma1" if et == "y20" else et
                    Dg = v2b_donemde(GK["G"], asama, ref, E); Dk = v2b_donemde(GK["K"], asama, ref, E)
                    for p in ("P0", "P1", "P2"):
                        g_ = Dg if p == "P0" else Dg[Dg[p] == 1]; k_ = Dk if p == "P0" else Dk[Dk[p] == 1]
                        for kn, tab in A["kontrol"].items():
                            kk = k_[k_.kaynak == kn] if len(k_) else k_
                            r = v2b_oran_karsilastir(g_, kk, et, tab, E) if len(g_) and len(kk) else {"fark": np.nan, "n1": len(g_), "n0": len(kk)}
                            r.update({"pazar": pz, "tanim": ad, "asama": asama, "etiket": et.upper(), "onkosul": p, "kontrol": kn,
                                      "ana": bool(ad == A["ana_tanim"] and p == A["ana_onkosul"] and et == "ma1")})
                            sat.append(r)
                        if ad == A["ana_tanim"] and et in ("ma1", "ma2", "ma3"):
                            for kaynak, D in (("GERCEK", g_), ("DISARI", k_[k_.kaynak == "DISARI"] if len(k_) else k_),
                                              ("RASTGELE", k_[k_.kaynak == "RASTGELE"] if len(k_) else k_)):
                                h = D[D[et] == 1] if len(D) else D
                                yon.append({"pazar": pz, "asama": asama, "etiket": et.upper(), "onkosul": p, "kaynak": kaynak, "n_hareket": int(len(h)),
                                            "yukari_payi": float((h[et + "_yon"] == 1).mean()) if len(h) else np.nan})
    S = pd.DataFrame(sat); karar = []
    for pz in Z:
        for et in ("MA1", "MA2", "MA3", "Y20"):
            x = S[(S.pazar == pz) & (S.tanim == A["ana_tanim"]) & (S.onkosul == A["ana_onkosul"]) & (S.etiket == et)] if len(S) else S
            if not len(x):
                continue
            h = {}
            for asama in ("wf", "kasa"):
                rd = x[(x.asama == asama) & (x.kontrol == "DISARI")].to_dict("records"); rr = x[(x.asama == asama) & (x.kontrol == "RASTGELE")].to_dict("records")
                h[asama] = v2b_karar_hucre(rd[0] if rd else None, rr[0] if rr else None)
            karar.append({"pazar": pz, "etiket": et, "rol": "KARAR" if et == "MA1" else "BİLGİ", "wf": h["wf"], "kasa": h["kasa"],
                          "sonuc": v2b_karar(h["wf"], h["kasa"])})
    return {"karar": karar, "satir": S, "yon": pd.DataFrame(yon)}


# ---------------------------------------------------------------- 5) B: TIINGO LİSTESİ, EVREN, ÖRNEKLEM (fiyat isteği YOK)
def v2b_st_indir(hedef: Optional[str] = None, E: Optional[Dict[str, Any]] = None, oturum: Any = None) -> str:
    """supported_tickers.zip (anahtarsız açık dosya) -> /tmp/vdyt2b/st/supported_tickers.zip. Varsa yeniden indirmez (liste günlük değişir; sha ön kayıtta)."""
    E = E or VDYT2B_ESIK; hedef = hedef or _v2b_ara("st", "supported_tickers.zip")
    if os.path.exists(hedef):
        return hedef
    if oturum is None:
        import requests
        oturum = requests.Session()
    r = oturum.get(E["B"]["tiingo"]["liste_url"], timeout=120)
    if r.status_code != 200 or not r.content[:2] == b"PK":
        raise Vdyt2bHata(f"supported_tickers indirilemedi (HTTP {r.status_code}); liste anahtarla sonra")
    with open(hedef + ".yaz", "wb") as f:
        f.write(r.content)
    os.replace(hedef + ".yaz", hedef)
    return hedef


def v2b_st_oku(yol: str) -> pd.DataFrame:
    with zipfile.ZipFile(yol) as z:
        ad = [x for x in z.namelist() if x.endswith(".csv")]
        if not ad:
            raise Vdyt2bHata(f"{yol}: zip içinde csv yok")
        T = pd.read_csv(z.open(ad[0]), keep_default_na=False, na_values=[""], dtype=str)
    for k in ("startDate", "endDate"):
        T[k] = pd.to_datetime(T[k], errors="coerce")
    T["ticker"] = T.ticker.astype(str).str.strip()
    return T


def v2b_k60_semboller(kl: Optional[str] = None) -> set:
    kl = kl or VDYT2B_ESIK["B"]["evren"]["k60_klasor"]
    if not os.path.isdir(kl):
        raise Vdyt2bHata(f"k60 fiyat klasörü yok: {kl}")
    return {os.path.basename(f)[:-5] for f in os.listdir(kl) if f.endswith(".json") and not f.startswith("_")}


def v2b_evren(T: pd.DataFrame, k60: set, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Ön kayıtlı evren kuralları (VDYT2B_ESIK['B']['evren']['kural'] sırasıyla). Döner (evren tablosu, adım adım sayım)."""
    E = E or VDYT2B_ESIK; V = E["B"]["evren"]; say: Dict[str, Any] = {"liste_satir": int(len(T))}
    S = T[(T.assetType == V["asset"]) & (T.priceCurrency == V["para"])].copy(); say["1_stock_usd"] = int(len(S))
    kod = S.ticker.str.match(V["kod_regex"]) & ~((S.ticker.str.len() == 5) & S.ticker.str[-1].isin(list(V["bes_harf_at"])))
    say["2_kod_atilan"] = int((~kod).sum()); S = S[kod]
    tekrar = S.ticker.duplicated(keep=False); say["3_yinelenen_kod_atilan_kayit"] = int(tekrar.sum()); S = S[~tekrar]
    k6 = S.ticker.isin(k60); say["4_k60_atilan"] = int(k6.sum()); S = S[~k6]
    son_bas, son_bit = pd.Timestamp(V["son_bas"]), pd.Timestamp(V["son_bit"]); omur = pd.Timedelta(days=int(V["min_omur_gun"]))
    B = S[S.exchange.isin(V["borsa"]) & (S.endDate >= son_bas) & (S.endDate <= son_bit) & (S.startDate <= S.endDate - omur)].assign(kaynak="BORSA")
    say["5_borsa"] = int(len(B))
    say["5_borsa_bilgi_2016_2019_bitis"] = int((S.exchange.isin(V["borsa"]) & (S.endDate >= pd.Timestamp("2016-01-01")) & (S.endDate < son_bas)).sum())
    Q = S[S.exchange.isin(V["otc"]) & S.ticker.str.match(V["otcq_regex"]) & (S.endDate >= son_bas) & (S.startDate <= S.endDate - omur)
          & (S.startDate <= pd.Timestamp(V["otcq_bas_ust"]))].assign(kaynak="OTCQ")
    say["6_otcq_aday"] = int(len(Q))
    Tb = T[(T.assetType == V["asset"]) & T.exchange.isin(V["borsa"])]
    ilk3 = {}
    for r in Tb[["ticker", "endDate"]].itertuples(index=False):
        if pd.notna(r.endDate):
            ilk3.setdefault(str(r.ticker)[:3], []).append(r.endDate)
    gun = pd.Timedelta(days=int(V["ayrik_otc_gun"]))
    ayrik = np.array([any(abs(e - q.startDate) <= gun for e in ilk3.get(str(q.ticker)[:3], [])) if pd.notna(q.startDate) else False
                      for q in Q[["ticker", "startDate"]].itertuples(index=False)], bool)
    say["6_otcq_ayrik_atilan"] = int(ayrik.sum()); Q = Q[~ayrik] if len(Q) else Q; say["6_otcq"] = int(len(Q))
    U = pd.concat([B, Q], ignore_index=True)
    birim = T[T.assetType == V["asset"]].drop_duplicates("ticker").set_index("ticker").endDate
    sp = np.array([any(((x + ek) in birim.index) and pd.notna(birim.get(x + ek)) and birim.get(x + ek) >= e - pd.Timedelta(days=int(V["spac_unite_gun"]))
                       for ek in V["spac_unite_ek"]) for x, e in zip(U.ticker, U.endDate)], bool) if len(U) else np.zeros(0, bool)
    say["7_spac_kabugu_atilan"] = {"BORSA": int((sp & (U.kaynak == "BORSA")).sum()), "OTCQ": int((sp & (U.kaynak == "OTCQ")).sum())}
    U = U[~sp].copy()
    U["son_yil"] = np.where((U.kaynak == "OTCQ") & (U.endDate > son_bit), "OTC_HALA", U.endDate.dt.year.astype(str))
    U["tabaka"] = U.kaynak + "|" + U.son_yil
    say["evren"] = int(len(U)); say["evren_kaynak"] = {k: int(v) for k, v in U.kaynak.value_counts().items()}
    say["tabaka_N"] = {k: int(v) for k, v in U.tabaka.value_counts().sort_index().items()}
    return U.sort_values(["tabaka", "ticker"]).reset_index(drop=True), say


def v2b_dagit(N: Dict[str, int], n: int) -> Dict[str, int]:
    """Orantılı dağıtım, en büyük kalan; N_h > 0 ise en az 1 (toplam n; tabaka sayısı n'den büyükse en büyük tabakalar)."""
    ks = sorted(k for k in N if N[k] > 0); tot = float(sum(N[k] for k in ks))
    if not ks or n <= 0:
        return {k: 0 for k in N}
    if n >= tot:
        return {k: int(N.get(k, 0)) for k in N}
    q = {k: n * N[k] / tot for k in ks}; a = {k: max(1, int(np.floor(q[k]))) for k in ks}
    a = {k: min(a[k], N[k]) for k in ks}
    while sum(a.values()) > n:
        k = max((k for k in ks if a[k] > 1), key=lambda k: (a[k] - q[k], k)); a[k] -= 1
    while sum(a.values()) < n:
        k = max((k for k in ks if a[k] < N[k]), key=lambda k: (q[k] - a[k], k)); a[k] += 1
    return {k: int(a.get(k, 0)) for k in N}


def v2b_orneklem(U: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Tabakalı rastgele örneklem (tohum sabit): ANA n (orantılı) + YEDEK (orantılı). Döner sıralı liste (rol, tabaka içi sıra, N_h, n_h)."""
    E = E or VDYT2B_ESIK; O = E["B"]["orneklem"]
    N = {k: int(v) for k, v in U.tabaka.value_counts().items()}; tabakalar = sorted(N)
    na = v2b_dagit(N, int(O["n"])); kalan = {k: N[k] - na[k] for k in tabakalar}; ny = v2b_dagit(kalan, int(O["yedek"]))
    sat = []
    for i, tb in enumerate(tabakalar):
        X = U[U.tabaka == tb].sort_values("ticker").reset_index(drop=True)
        p = np.random.default_rng(int(O["tohum"]) + i).permutation(len(X))
        for j, ix in enumerate(p[: na[tb] + ny[tb]].tolist()):
            r = X.iloc[ix]
            sat.append({"ticker": r.ticker, "exchange": r.exchange, "startDate": str(r.startDate.date()), "endDate": str(r.endDate.date()), "kaynak": r.kaynak,
                        "son_yil": r.son_yil, "tabaka": tb, "rol": "ANA" if j < na[tb] else "YEDEK", "tabaka_sira": j + 1, "N_h": N[tb], "n_h": na[tb],
                        "yedek_h": ny[tb]})
    L = pd.DataFrame(sat)
    return L.sort_values(["rol", "tabaka", "tabaka_sira"]).reset_index(drop=True)


def _v2b_liste_yaz(yol: str, L: pd.DataFrame) -> str:
    """Örneklem listesi: sekme ayrılmış metin (.tsv; depo .gitignore '*.csv' kuralına takılmaz, git'e işlenebilir)."""
    return _v2b_yaz(yol, L.to_csv(index=False, sep="\t", lineterminator="\n"))


def _v2b_liste_oku(yol: str) -> pd.DataFrame:
    return pd.read_csv(yol, sep="\t", dtype=str, keep_default_na=False, na_values=[""])


def v2b_liste(cikti: Optional[str] = None, st_yol: Optional[str] = None, k60: Optional[set] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """`liste`: supported_tickers -> evren sayımı (json) + örneklem (csv). Tiingo FİYAT isteği YOK. Liste dosyası git'e işlenmişse üzerine yazmaz."""
    E = E or VDYT2B_ESIK; yl = _v2b_yol("liste", cikti)
    if os.path.exists(yl) and _v2b_git_izli(yl):
        raise Vdyt2bHata(f"örneklem listesi git'e işlenmiş ({yl}); üzerine yazılmadı")
    st = st_yol or v2b_st_indir(E=E); T = v2b_st_oku(st)
    U, say = v2b_evren(T, v2b_k60_semboller() if k60 is None else k60, E); L = v2b_orneklem(U, E)
    say.update({"zaman": _v2b_simdi(), "st_sha256": V1.vdyt_sha_dosya(st), "st_en_son_endDate": str(T.endDate.max().date()), "orneklem_ana": int((L.rol == "ANA").sum()),
                "orneklem_yedek": int((L.rol == "YEDEK").sum()), "tabaka_n": {k: int(v) for k, v in L[L.rol == "ANA"].tabaka.value_counts().sort_index().items()},
                "tabaka_yedek": {k: int(v) for k, v in L[L.rol == "YEDEK"].tabaka.value_counts().sort_index().items()}})
    _v2b_liste_yaz(yl, L); say["liste_sha256"] = V1.vdyt_sha_dosya(yl)
    _v2b_json(_v2b_yol("evren", cikti), say)
    v2blog.info("liste: evren %d, örneklem %d + yedek %d -> %s", say["evren"], say["orneklem_ana"], say["orneklem_yedek"], yl)
    return say


# ---------------------------------------------------------------- 6) B: TIINGO İSTEMCİSİ, HIZ SINIRI SAYACI, ÖNBELLEK
class TiingoSayac:
    """Kalıcı hız sınırı sayacı (/tmp/vdyt2b/tiingo_sayac.json): istek zamanları (son 24 saat) ve ay başına farklı semboller. Sert sınırlar: saatte
    saat_istek, günde gun_istek, ayda ay_sembol farklı sembol. Önbellekten gelen sembol sayılmaz. saat: zaman kaynağı (test için sahte saat)."""

    def __init__(self, yol: Optional[str] = None, E: Optional[Dict[str, Any]] = None, saat: Callable[[], float] = time.time) -> None:
        self.E = (E or VDYT2B_ESIK)["B"]["tiingo"]; self.yol = yol or _v2b_ara("tiingo_sayac.json"); self.saat = saat
        self.d: Dict[str, Any] = {"istek": [], "ay": {}}
        if os.path.exists(self.yol):
            try:
                self.d = _v2b_json_oku(self.yol); self.d.setdefault("istek", []); self.d.setdefault("ay", {})
            except (OSError, ValueError) as ex:
                raise Vdyt2bHata(f"hız sayacı okunamadı ({self.yol}: {type(ex).__name__}); sayaç bozuk, istek gönderilmedi") from None

    def _ay(self) -> str:
        return _dt.datetime.fromtimestamp(self.saat(), _dt.timezone.utc).strftime("%Y-%m")

    def durum(self) -> Dict[str, int]:
        s = self.saat(); I = [x for x in self.d["istek"] if s - x < 86400]
        return {"saat": sum(1 for x in I if s - x < 3600), "gun": len(I), "ay_sembol": len(self.d["ay"].get(self._ay(), []))}

    def bekle(self, sembol: str) -> float:
        """0 -> şimdi istek gönderilebilir; > 0 -> o kadar saniye beklenmeli. Ay sınırı dolmuşsa Vdyt2bHata (dur)."""
        s = self.saat(); I = sorted(x for x in self.d["istek"] if s - x < 86400); ay = self.d["ay"].get(self._ay(), [])
        if sembol not in ay and len(ay) >= int(self.E["ay_sembol"]):
            raise Vdyt2bHata(f"ay içinde {len(ay)} farklı sembol: ücretsiz katman sınırı ({self.E['ay_sembol']}); çekim DURDU (sonraki ay sürer)")
        b = 0.0
        sa = [x for x in I if s - x < 3600]
        if len(sa) >= int(self.E["saat_istek"]):
            b = max(b, sa[-int(self.E["saat_istek"])] + 3600 - s + 1)
        if len(I) >= int(self.E["gun_istek"]):
            b = max(b, I[-int(self.E["gun_istek"])] + 86400 - s + 1)
        return float(b)

    def kaydet(self, sembol: str) -> None:
        s = self.saat(); self.d["istek"] = [x for x in self.d["istek"] if s - x < 86400] + [s]
        ay = self.d["ay"].setdefault(self._ay(), [])
        if sembol not in ay:
            ay.append(sembol)
        _v2b_json(self.yol, self.d)


class TiingoIstemci:
    """Tiingo günlük fiyat istemcisi: başlık 'Authorization: Token <anahtar>' (anahtar YALNIZ ortamdan; yoksa 'proxy'); URL'de anahtar yok; anahtar loglanmaz
    ve dosyaya yazılmaz. Önbellek /tmp/vdyt2b/tiingo/<KOD>.json (varsa istek yok). oturum: requests benzeri (get) — test için sahte; uyu: bekleme işlevi."""

    def __init__(self, E: Optional[Dict[str, Any]] = None, oturum: Any = None, sayac: Optional[TiingoSayac] = None, klasor: Optional[str] = None,
                 uyu: Callable[[float], None] = time.sleep, en_cok_bekle: Optional[float] = None) -> None:
        self.EB = (E or VDYT2B_ESIK)["B"]; self.T = self.EB["tiingo"]; self.sayac = sayac or TiingoSayac(E=E); self.uyu = uyu
        self.klasor = klasor or _v2b_ara("tiingo"); os.makedirs(self.klasor, exist_ok=True); self.en_cok_bekle = en_cok_bekle; self.art_429 = 0
        if oturum is None:
            import requests
            oturum = requests.Session()
        self.oturum = oturum

    def _baslik(self) -> Dict[str, str]:
        return {"Content-Type": "application/json", "Authorization": "Token " + _v2b_anahtar()}

    def onbellek_yol(self, kod: str) -> str:
        if not re.match(r"^[A-Z0-9.\-]{1,10}$", kod):
            raise Vdyt2bHata(f"geçersiz kod: {kod!r}")
        return os.path.join(self.klasor, f"{kod}.json")

    def onbellekte(self, kod: str) -> Optional[Dict[str, Any]]:
        y = self.onbellek_yol(kod)
        if os.path.exists(y):
            try:
                return _v2b_json_oku(y)
            except (OSError, ValueError):
                v2blog.warning("önbellek bozuk, yeniden istenecek: %s", kod)
        return None

    def fiyat(self, kod: str) -> Dict[str, Any]:
        """Önbellekte varsa döner (istek yok). Yoksa hız sınırına uyarak bir istek; sonuç (durum ok / yok / hata, http, veri) önbelleğe yazılır (yalnız ok
        ve 404). 429: bekle_429 saniye bekle; art arda art_arda_429_dur kez -> dur."""
        x = self.onbellekte(kod)
        if x is not None and x.get("durum") in ("ok", "yok"):
            return x
        while True:
            b = self.sayac.bekle(kod)
            if b <= 0:
                break
            if self.en_cok_bekle is not None and b > self.en_cok_bekle:
                raise Vdyt2bHata(f"hız sınırı: {b:.0f} sn beklemek gerekiyor (en çok {self.en_cok_bekle:.0f}); çekim durdu (kaldığı yerden sürer)")
            v2blog.info("hız sınırı (%s): %.0f sn bekleniyor", self.sayac.durum(), b); self.uyu(b)
        url = self.T["fiyat_url"].format(kod=kod); prm = {"startDate": self.T["baslangic"], "endDate": self.T["bitis"], "format": "json"}
        self.sayac.kaydet(kod)
        try:
            r = self.oturum.get(url, params=prm, headers=self._baslik(), timeout=int(self.T["zaman_asimi"]))
            kodu = int(getattr(r, "status_code", 0))
        except Exception as ex:   # ağ hatası: önbelleğe yazılmaz, sonraki koşuda yeniden denenir
            v2blog.warning("Tiingo %s: istek hatası %s", kod, _v2b_temiz(f"{type(ex).__name__}: {str(ex)[:160]}"))
            return {"durum": "hata", "http": None, "neden": _v2b_temiz(type(ex).__name__), "veri": None}
        if kodu == 429:
            self.art_429 += 1
            if self.art_429 >= int(self.T["art_arda_429_dur"]):
                raise Vdyt2bHata(f"Tiingo art arda {self.art_429} kez 429 (hız sınırı): çekim durdu")
            v2blog.warning("Tiingo %s: 429; %d sn bekleniyor", kod, int(self.T["bekle_429"])); self.uyu(float(self.T["bekle_429"]))
            return {"durum": "hata", "http": 429, "neden": "429", "veri": None}
        self.art_429 = 0
        if kodu == 200:
            try:
                veri = r.json()
            except ValueError:
                return {"durum": "hata", "http": 200, "neden": "json değil", "veri": None}
            if not isinstance(veri, list):
                return {"durum": "hata", "http": 200, "neden": "liste değil", "veri": None}
            kayit = {"durum": "ok" if len(veri) else "yok", "http": 200, "kod": kod, "zaman": _v2b_simdi(), "satir": len(veri), "veri": veri}
        elif kodu == 404:
            kayit = {"durum": "yok", "http": 404, "kod": kod, "zaman": _v2b_simdi(), "satir": 0, "veri": []}
        else:
            v2blog.warning("Tiingo %s: HTTP %s", kod, kodu)
            return {"durum": "hata", "http": kodu, "neden": f"HTTP {kodu}", "veri": None}
        _v2b_json(self.onbellek_yol(kod), kayit)
        v2blog.info("Tiingo %s: %s (%d satır; sayaç %s)", kod, kayit["durum"], kayit["satir"], self.sayac.durum())
        return kayit


def v2b_tiingo_df(kayit: Optional[Dict[str, Any]]) -> Optional[pd.DataFrame]:
    """Önbellek kaydı -> günlük DataFrame: ham açılış..hacim (ro, rh, rl, rc, rv), splitFactor, divCash ve bölünme düzeltmeli Open..Volume
    (ham / gelecekteki bölünme oranlarının çarpımı; hacim x çarpım). Boşsa None."""
    if not kayit or kayit.get("durum") != "ok" or not kayit.get("veri"):
        return None
    D = pd.DataFrame(kayit["veri"])
    if "date" not in D or "close" not in D:
        return None
    D.index = pd.to_datetime(D.date.astype(str).str[:10]); D = D[~D.index.duplicated(keep="last")].sort_index()
    for k in ("open", "high", "low", "close", "volume", "splitFactor", "divCash"):
        D[k] = pd.to_numeric(D[k], errors="coerce") if k in D else (1.0 if k == "splitFactor" else np.nan)
    sf = D.splitFactor.fillna(1.0).where(lambda x: x > 0, 1.0).to_numpy(float)
    gelecek = np.r_[np.cumprod(sf[::-1])[::-1][1:], 1.0]   # gün i: j > i bölünmelerinin çarpımı
    X = pd.DataFrame({"ro": D.open, "rh": D.high, "rl": D.low, "rc": D.close, "rv": D.volume, "splitFactor": sf, "divCash": D.divCash}, index=D.index)
    X["Open"] = X.ro / gelecek; X["High"] = X.rh / gelecek; X["Low"] = X.rl / gelecek; X["Close"] = X.rc / gelecek; X["Volume"] = X.rv * gelecek
    return X


# ---------------------------------------------------------------- 7) B: PİLOT ÖLÇÜTLERİ (önceden yazılı)
def v2b_pilot_olc(s: Dict[str, Any], kayit: Optional[Dict[str, Any]], E: Optional[Dict[str, Any]] = None, yahoo: Optional[pd.DataFrame] = None
                  ) -> Dict[str, Any]:
    """Tek pilot sembolü için K1-K6 (bölüm 'olcut'). yahoo: karşılaştırma serisi (Close; bölünme düzeltmeli) ya da None. Döner ölçütler + GEÇTİ."""
    E = E or VDYT2B_ESIK; P = E["B"]["pilot"]; r: Dict[str, Any] = {"kod": s["kod"], "tur": s["tur"], "http": (kayit or {}).get("http")}
    X = v2b_tiingo_df(kayit); f25 = pd.Timestamp(s["f25"])
    ok_c = X is not None and int((X.rc > 0).sum()) >= 252
    r["K1_seri"] = bool(ok_c); r["bar"] = 0 if X is None else int(len(X))
    if not ok_c:
        r.update({"K2_son_gun": False, "K3_bosluk": False, "K4_tutarlilik": None, "K5_ohlcv": False, "K6_karisma": False, "GECTI": False}); return r
    X = X[X.rc > 0]; ilk, son = X.index[0], X.index[-1]; r.update({"ilk": str(ilk.date()), "son": str(son.date())})
    a60, b10 = _v2b_is_kaydir(f25, -60), _v2b_is_kaydir(f25, 10)
    if s["tur"] == "BORSA":
        r["K2_son_gun"] = bool(a60 <= son <= b10); A = son
    elif s["tur"] == "Q":
        r["K2_son_gun"] = bool(son >= a60 and ((X.index >= a60) & (X.index <= b10)).any()); A = a60
    else:
        r["K2_son_gun"] = bool(((X.index < a60) & (X.index >= _v2b_is_kaydir(a60, -60))).any()); A = a60
    pen = _v2b_is_gunleri(_v2b_is_kaydir(A, -60), A); var = X.index[(X.index >= pen[0]) & (X.index <= pen[-1])]
    eksik = pen.difference(var); r["K3_eksik_gun"] = int(len(eksik))
    idx = np.searchsorted(pen.to_numpy(), var.to_numpy()); bos = np.diff(np.r_[-1, idx, len(pen)]) - 1 if len(pen) else np.array([999])
    r["K3_en_uzun"] = int(bos.max()) if len(bos) else 999; r["K3_bosluk"] = bool(r["K3_eksik_gun"] <= 5 and r["K3_en_uzun"] <= 5)
    dolu = X[["ro", "rh", "rl", "rc", "rv"]].notna().all(1) & (X.rh >= X.rl) & (X.rc > 0); r["K5_dolu_pay"] = float(dolu.mean()); r["K5_ohlcv"] = bool(r["K5_dolu_pay"] >= 0.95)
    with np.errstate(invalid="ignore", divide="ignore"):
        lr = np.log(X.Close / X.Close.shift(1))
    if s["tur"] == "YENIDEN":
        yb = pd.Timestamp(s["yeni_bas"]); eski = X.index[(X.index < yb) & (X.index >= _v2b_is_kaydir(yb, -250))]
        yeni = X.index[(X.index >= yb) & (X.index <= _v2b_is_kaydir(yb, 250))]
        if len(eski) and len(yeni):
            ara = len(_v2b_is_gunleri(eski[-1], yeni[0])) - 2; r["K6_ara_is_gunu"] = int(ara); r["K6_karisma"] = bool(ara >= 30)
        else:
            r["K6_ara_is_gunu"] = None; r["K6_karisma"] = True
        r["K6_KARISIK"] = not r["K6_karisma"]
    else:
        sic = (np.abs(lr) > np.log(10.0)) & (X.splitFactor == 1.0); r["K6_sicrama"] = int(sic.sum()); r["K6_karisma"] = bool(r["K6_sicrama"] == 0)
    k4 = []
    for g, fiyat, _kaynak in P["basin_kapanis"].get(s["kod"], []):
        g = pd.Timestamp(g)
        if g in X.index:
            k4.append(bool(abs(float(X.rc.loc[g]) / float(fiyat) - 1.0) <= 0.10)); r["K4_basin"] = [str(g.date()), float(X.rc.loc[g]), float(fiyat)]
        else:
            k4.append(False); r["K4_basin"] = [str(g.date()), None, float(fiyat)]
    if yahoo is not None and len(yahoo):
        ort = X.index.intersection(yahoo.index)
        if len(ort) >= 60:
            a = X.Close.reindex(ort); b = yahoo.reindex(ort).astype(float)
            ra, rb = np.log(a / a.shift(1)).to_numpy()[1:], np.log(b / b.shift(1)).to_numpy()[1:]; ok = np.isfinite(ra) & np.isfinite(rb)
            kor = float(np.corrcoef(ra[ok], rb[ok])[0, 1]) if ok.sum() > 30 else np.nan; med = float(np.nanmedian(np.abs(a.to_numpy() / b.to_numpy() - 1.0)))
            r["K4_yahoo"] = {"ortak": int(len(ort)), "korelasyon": kor, "medyan_oran_fark": med}; k4.append(bool(np.isfinite(kor) and kor >= 0.90 and med <= 0.02))
        else:
            r["K4_yahoo"] = {"ortak": int(len(ort))}
    r["K4_tutarlilik"] = (all(k4) if k4 else None)
    r["GECTI"] = bool(r["K1_seri"] and r["K2_son_gun"] and r["K3_bosluk"] and r["K5_ohlcv"] and r["K6_karisma"] and (r["K4_tutarlilik"] is not False))
    return r


def v2b_pilot_karar(sonuclar: List[Dict[str, Any]], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or VDYT2B_ESIK; K = E["B"]["pilot"]["karar"]; gec = sum(bool(r.get("GECTI")) for r in sonuclar)
    karar = "GÜVENİLİR" if gec >= int(K["guvenilir_min"]) else ("KISMEN" if gec >= int(K["kismen_min"]) else "GÜVENİLMEZ")
    yen = [r for r in sonuclar if r.get("tur") == "YENIDEN"]
    if yen and all(r.get("K6_KARISIK") for r in yen) and karar == "GÜVENİLİR":
        karar = "KISMEN"
    q = [r for r in sonuclar if r.get("tur") == "Q"]
    return {"gecen": int(gec), "toplam": len(sonuclar), "karar": karar, "otcq_dahil": bool(any(r.get("GECTI") for r in q)) if q else False,
            "yeniden_karisik": [r["kod"] for r in yen if r.get("K6_KARISIK")]}


def _v2b_yahoo_seri(kaynak: str) -> Optional[pd.Series]:
    """Pilot K4 Yahoo karşılaştırması: 'k34_yahoo SUNE' -> /tmp/veri2/k34_yahoo.pkl; 'k60_fiyat EXE' -> k60 JSON (bölünme düzeltmeli kapanış)."""
    try:
        if kaynak.startswith("k34_yahoo"):
            import pickle
            kod = kaynak.split()[1]
            with open("/tmp/veri2/k34_yahoo.pkl", "rb") as f:
                X = pickle.load(f)
            d = X.get(kod)
            if d is None:
                return None
            c = d["Close"] if "Close" in d else d.iloc[:, 3]
            c.index = pd.to_datetime(c.index).tz_localize(None) if getattr(c.index, "tz", None) is not None else pd.to_datetime(c.index)
            return c.astype(float)
        if kaynak.startswith("k60_fiyat"):
            kod = kaynak.split()[1]; d, _m = V1.vdyt_yahoo_oku(os.path.join(V1.VDYT_YOL["k60_fiyat"], f"{kod}.json"))
            return None if d is None else d.Close.astype(float)
    except (OSError, KeyError, ValueError, IndexError, AttributeError) as ex:
        v2blog.warning("pilot Yahoo serisi okunamadı (%s): %s", kaynak, type(ex).__name__)
    return None


def v2b_pilot(cikti: Optional[str] = None, istemci: Optional[TiingoIstemci] = None, E: Optional[Dict[str, Any]] = None, git_sart: bool = True) -> Dict[str, Any]:
    """`pilot`: ön kayıt kapısı (git) -> pilot sembolleri (en çok 12 istek) -> ölçütler -> karar (vdyt2b_pilot.json)."""
    E = E or VDYT2B_ESIK
    oc = v2b_onkayit_dogrula(cikti, test="pilot", git=git_sart)
    ist = istemci or TiingoIstemci(E)
    S = E["B"]["pilot"]["semboller"]; son = []
    for s in S:
        k = ist.fiyat(s["kod"])
        if k.get("durum") == "hata":
            raise Vdyt2bHata(f"pilot {s['kod']}: istek hatası ({k.get('neden')}); pilot tamamlanmadı, sonra yeniden (önbellek sürer)")
        yah = _v2b_yahoo_seri(s["yahoo_karsilastir"]) if s.get("yahoo_karsilastir") else None
        son.append(v2b_pilot_olc(s, k, E, yah))
    out = {"zaman": _v2b_simdi(), "onkayit": oc, "sonuc": son, "karar": v2b_pilot_karar(son, E)}
    _v2b_json(_v2b_yol("pilot", cikti), out)
    v2blog.info("pilot: %s (%d / %d geçti)", out["karar"]["karar"], out["karar"]["gecen"], out["karar"]["toplam"])
    return out


# ---------------------------------------------------------------- 8) B: ÇEKİM (kaldığı yerden sürer)
def v2b_cek_plan(L: pd.DataFrame, durum: Dict[str, str]) -> List[str]:
    """Çekilecek kodlar: bütün ANA; her tabakada VERİ YOK olan ANA sayısı kadar YEDEK (tabaka sırasıyla; yedeğin kendisi de VERİ YOK ise bir sonraki)."""
    plan = list(L[L.rol == "ANA"].ticker)
    for tb, g in L.groupby("tabaka"):
        yok = sum(1 for k in g[g.rol == "ANA"].ticker if durum.get(k) == "yok")
        for k in g[g.rol == "YEDEK"].assign(_s=lambda x: x.tabaka_sira.astype(int)).sort_values("_s").ticker:
            if yok <= 0:
                break
            plan.append(k)
            if durum.get(k) == "yok":
                continue
            if durum.get(k) is None:
                break
            yok -= 1
    return plan


def v2b_cek(cikti: Optional[str] = None, istemci: Optional[TiingoIstemci] = None, E: Optional[Dict[str, Any]] = None, git_sart: bool = True,
            en_cok: Optional[int] = None) -> Dict[str, Any]:
    """`cek`: ön kayıt + pilot (GÜVENİLİR / KISMEN) kapısı -> örneklem kodları (önbellekte olan atlanır). VERİ YOK -> aynı tabakadan yedek. Durum dosyası yazılır."""
    E = E or VDYT2B_ESIK; oc = v2b_onkayit_dogrula(cikti, test="cek", git=git_sart); pk = _v2b_pilot_oku(cikti, E)
    L = _v2b_liste_oku(_v2b_yol("liste", cikti))
    if not pk["otcq_dahil"]:
        L = L[L.kaynak != "OTCQ"]
    ist = istemci or TiingoIstemci(E); durum: Dict[str, str] = {}; sayi = 0; durdu = None
    try:
        while True:
            plan = v2b_cek_plan(L, durum); yeni = [k for k in plan if k not in durum]
            if not yeni:
                break
            for k in yeni:
                if en_cok is not None and sayi >= en_cok:
                    break
                x = ist.fiyat(k)
                if x.get("durum") == "hata":
                    raise Vdyt2bHata(f"çekim {k}: {x.get('neden')}; durdu (kaldığı yerden sürer)")
                X = v2b_tiingo_df(x); durum[k] = "ok" if (X is not None and int((X.rc > 0).sum()) >= 252) else "yok"; sayi += 1
            if en_cok is not None and sayi >= en_cok:
                break
    except Vdyt2bHata as ex:
        durdu = str(ex)
    plan = v2b_cek_plan(L, durum); tamam = durdu is None and all(k in durum for k in plan)
    out = {"zaman": _v2b_simdi(), "tamam": bool(tamam), "plan": len(plan), "durum": durum, "veri_yok": sorted(k for k, v in durum.items() if v == "yok"),
           "sayac": ist.sayac.durum(), "onkayit_commit": oc.get("git_onkayit", {}).get("commit"), "durdu": durdu}
    _v2b_json(_v2b_yol("cek", cikti), out)
    if durdu:
        raise Vdyt2bHata(durdu)
    return out


# ---------------------------------------------------------------- 9) B: KOŞU (batan satırları VDYT2 kodu ile; yaşayanlar VDYT2 tablolarından)
def v2b_k60_getiri(F_k60: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """D4 için k60 kapanış ve günlük ln getiri matrisleri (gün x sembol; float32)."""
    C = pd.DataFrame({s: d.c.astype(np.float32) for s, d in F_k60["S"].items()})
    with np.errstate(invalid="ignore", divide="ignore"):
        R = np.log(C / C.shift(1))
    return C, R


def v2b_yeniden_ad(close: pd.Series, C: pd.DataFrame, R: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """D4 kod değişikliği: son 60 barı bir k60 serisiyle (ortak gün >= 55) getiri korelasyonu >= 0,98 VE ln(kapanış oranı) std <= 0,01 ise o k60 kodu; yoksa None."""
    D = (E or VDYT2B_ESIK)["B"]["cekim_sonrasi"]["D4_yeniden_ad"]; c = close.dropna(); c = c[c > 0].iloc[-(int(D["son_bar"]) + 1):]
    if len(c) < int(D["min_ortak"]) + 1:
        return None
    r = np.log(c / c.shift(1)).iloc[1:]; Rk = R.reindex(r.index); say = Rk.notna().sum(); Rk = Rk.loc[:, say >= int(D["min_ortak"])]
    if not Rk.shape[1]:
        return None
    kor = Rk.astype(float).corrwith(r.astype(float)); aday = kor[kor >= float(D["korelasyon"])].sort_values(ascending=False)
    for s in aday.index:
        with np.errstate(invalid="ignore", divide="ignore"):
            o = np.log(c / C[s].reindex(c.index).astype(float))
        if o.notna().sum() >= int(D["min_ortak"]) and float(o.std()) <= float(D["oran_std"]):
            return str(s)
    return None


def v2b_batan_fiyat(L: pd.DataFrame, durum: Dict[str, str], E: Optional[Dict[str, Any]] = None, klasor: Optional[str] = None,
                    F_k60: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Çekilen batan serileri -> F (V1 biçimi: S temiz o,h,l,c,v; meta tur EQUITY + bölünmeler) ve sembol tablosu (veri / SPAC kalıbı / kod değişikliği /
    ağırlık). F_k60 verilirse D4 (kod değişikliği) uygulanır; verilmezse D4 'uygulanmadı' yazılır."""
    E = E or VDYT2B_ESIK; E1 = V2._v2_e1(); C = E["B"]["cekim_sonrasi"]; kl = klasor or _v2b_ara("tiingo"); S, M, sat = {}, {}, []
    Ck, Rk = v2b_k60_getiri(F_k60) if F_k60 is not None else (None, None)
    for k in [k for k in L.ticker if k in durum]:
        r = L[L.ticker == k].iloc[0].to_dict(); y = os.path.join(kl, f"{k}.json"); X = v2b_tiingo_df(_v2b_json_oku(y)) if os.path.exists(y) else None
        if X is None or int((X.rc > 0).sum()) < 252:
            sat.append({**r, "veri": "YOK", "spac": False}); continue
        rc = X.rc[X.rc > 0]; lo, hi = C["D2_spac_kalibi"]["aralik"]; spac = bool(((rc >= lo) & (rc <= hi)).mean() >= float(C["D2_spac_kalibi"]["pay"]))
        yad = None if (spac or Ck is None) else v2b_yeniden_ad(X.Close, Ck, Rk, E)
        sat.append({**r, "veri": "VAR", "spac": spac, "yeniden_ad": yad if Ck is not None else "UYGULANMADI", "bar": int(len(X)), "ilk": str(X.index[0].date()),
                    "son": str(X.index[-1].date())})
        if spac or yad:
            continue
        d = V1._vdyt_kes(V1.vdyt_bar_temizle(X[["Open", "High", "Low", "Close", "Volume"]], E1), V1.VDYT_ESIK["pazar"]["ABD"]["bas"], E1)
        if len(d):
            S[k] = d; M[k] = {"tur": "EQUITY", "bolunme": [(g, float(f)) for g, f in X.splitFactor[X.splitFactor != 1.0].items()], "kaynak": "tiingo"}
    T = pd.DataFrame(sat)
    if len(T):
        m = T.groupby("tabaka").veri.apply(lambda x: int((x == "VAR").sum())); T["m_h"] = T.tabaka.map(m)
        T["w"] = np.where(T.veri == "VAR", T.N_h.astype(float) / T.m_h.replace(0, np.nan), np.nan)
    return {"S": S, "meta": M, "kaynak": "tiingo"}, T


@V2._v2_sessiz
def v2b_batan_satirlar(F_b: Dict[str, Any], isci: int = 3, F_k60: Optional[Dict[str, Any]] = None, Ev: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Batan sembolleri VDYT2 kodu ile (V2._v2_hisse_is; tanım yalnız G5; kip 'kos'): panel k60 + batan BİRLİKTE (V1.vdyt_panel). VDYT2.py değişmez."""
    E = V2.VDYT2_ESIK; E1 = V2._v2_e1(); F_k60 = F_k60 or V2.v2_fiyat("ABD", canli=False)
    F = {"S": {**F_k60["S"], **F_b["S"]}, "meta": {**F_k60.get("meta", {}), **F_b["meta"]}}
    if Ev is None:
        Ev, _n = V2.v2_olaylar("ABD", F)
    Pn = V1.vdyt_panel("ABD", F, E1, isci); Pn["p_pazar_ret20"] = Pn["p_pazar_lr"].rolling(20, min_periods=20).sum()
    Ev_m = Ev[Ev.sembol == "*"]; Ev_s = {s: g for s, g in Ev[Ev.sembol.isin(list(F_b["S"]))].groupby("sembol")}
    V2._V2_IS.clear()
    V2._V2_IS.update({"E": E, "F": F, "pazar": "ABD", "kip": "kos", "Pn": Pn, "Ev_s": Ev_s, "Ev_m": Ev_m, "bos_olay": Ev.iloc[:0],
                      "tanimlar": {VDYT2B_ESIK["B"]["tanim"]: E["tanim"][VDYT2B_ESIK["B"]["tanim"]]}, "canli": False})
    R = V1._vdyt_harita(V2._v2_hisse_is, sorted(F_b["S"]), isci); hata = {r["sembol"]: r["hata"] for r in R if r.get("hata")}
    R = [r for r in R if not r.get("hata")]; ad = VDYT2B_ESIK["B"]["tanim"]
    G = V2._v2_hazirla(V2._v2_birlestir(R, "satir", ad), E); K = V2._v2_hazirla(V2._v2_birlestir(R, "kontrol", ad), E)
    return {"G": G, "K": K, "hata": hata, "F": F_b}


def _v2b_ort(h: pd.DataFrame, x: Optional[pd.Series]) -> float:
    """Ağırlıklı ortalama (w sütunu); NaN değerler ve ağırlıklar atılır."""
    if x is None or not len(h):
        return np.nan
    v = x.to_numpy(float); w = h.w.to_numpy(float); ok = np.isfinite(v) & np.isfinite(w) & (w > 0)
    return float(np.average(v[ok], weights=w[ok])) if ok.any() else np.nan


def v2b_B_analiz(Gy: pd.DataFrame, Ky: pd.DataFrame, Gb: pd.DataFrame, Kb: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """B koşusu: (a) yalnız batanlar (ağırlıklı; bilgi), (b) birleşik (yaşayan w = 1 + batan w_h): y20 ve MA1; WF ve KASA; P0 / P1 / P2; iki kontrol. Karar ANA."""
    E = E or VDYT2B_ESIK; A = E["A"]; sat, bilgi = [], []
    Gy = Gy.assign(evren="YASAYAN"); Ky = Ky.assign(evren="YASAYAN"); Gb = Gb.assign(evren="BATAN"); Kb = Kb.assign(evren="BATAN")
    for et in ("y20", "ma1"):
        for asama in ("wf", "kasa"):
            for kume, Dg, Dk in (("BATAN", Gb, Kb), ("BIRLESIK", pd.concat([Gy, Gb], ignore_index=True), pd.concat([Ky, Kb], ignore_index=True)),
                                 ("YASAYAN", Gy, Ky)):
                g0 = v2b_donemde(Dg, asama, "ma1", E); k0 = v2b_donemde(Dk, asama, "ma1", E)
                for p in ("P0", "P1", "P2"):
                    g_ = g0 if p == "P0" else g0[g0[p] == 1]; k_ = k0 if p == "P0" else k0[k0[p] == 1]
                    for kn, tab in A["kontrol"].items():
                        kk = k_[k_.kaynak == kn] if len(k_) else k_
                        r = v2b_oran_karsilastir(g_, kk, et, tab, E, agirlik="w") if len(g_) and len(kk) else {"fark": np.nan, "n1": len(g_), "n0": len(kk)}
                        r.update({"kume": kume, "etiket": et.upper(), "asama": asama, "onkosul": p, "kontrol": kn,
                                  "ana": bool(kume == "BIRLESIK" and p == A["ana_onkosul"])})
                        sat.append(r)
    for asama in ("wf", "kasa"):
        for p in ("P0", "P1"):
            for evren, D in (("BATAN", Gb), ("YASAYAN", Gy)):
                d = v2b_donemde(D, asama, "ma1", E); d = d if p == "P0" else d[d[p] == 1]; h = d[d.y20 == 1] if len(d) else d
                bilgi.append({"evren": evren, "asama": asama, "onkosul": p, "n": int(len(d)), "n_y20": int(len(h)),
                              "yukari_payi_w": _v2b_ort(h, (h.yon == 1).astype(float) if len(h) else None),
                              "r20_ort_w": _v2b_ort(h, h.r20 if "r20" in h else None), "mae_ort_w": _v2b_ort(h, h.mae if "mae" in h else None)})
    S = pd.DataFrame(sat); karar = []
    for et in ("Y20", "MA1"):
        x = S[(S.kume == "BIRLESIK") & (S.onkosul == A["ana_onkosul"]) & (S.etiket == et)]; h = {}
        for asama in ("wf", "kasa"):
            rd = x[(x.asama == asama) & (x.kontrol == "DISARI")].to_dict("records"); rr = x[(x.asama == asama) & (x.kontrol == "RASTGELE")].to_dict("records")
            h[asama] = v2b_karar_hucre(rd[0] if rd else None, rr[0] if rr else None)
        karar.append({"pazar": "ABD", "etiket": et, "sutun": "BATANLAR DAHİL", "wf": h["wf"], "kasa": h["kasa"], "sonuc": v2b_karar(h["wf"], h["kasa"])})
    return {"karar": karar, "satir": S, "bilgi": pd.DataFrame(bilgi)}


# ---------------------------------------------------------------- 10) ÖN KAYIT, RET KAPISI, KOŞU, RAPOR
def _v2b_git_izli(yol: str) -> bool:
    k, o, _e = V1._vdyt_git(["log", "-1", "--format=%H", "--", os.path.basename(yol)], os.path.dirname(os.path.abspath(yol)))
    return k == 0 and bool(o)


def _v2b_onkayit_oku(yol: str) -> Dict[str, Any]:
    with open(yol, encoding="utf-8") as f:
        m = f.read()
    g = lambda d: (re.search(d, m, re.M).group(1) if re.search(d, m, re.M) else None)   # noqa: E731
    tablo = dict(re.findall(r"^- (\w+_\w+_[\w.]+\.csv\.gz): sha256 ([0-9a-f]{64}|YOK)$", m, re.M))
    return {"esik": g(r"^ESIK_SHA256: ([0-9a-f]{64})$"), "kod": g(r"^KOD_SHA256: ([0-9a-f]{64})$"), "vdyt2_kod": g(r"^VDYT2_KOD_SHA256: ([0-9a-f]{64})$"),
            "vdyt_kod": g(r"^VDYT_KOD_SHA256: ([0-9a-f]{64})$"), "liste": g(r"^LISTE_SHA256: ([0-9a-f]{64}|YOK)$"), "zaman": g(r"^Yazım zamanı: (.+)$"),
            "tablo": tablo}


def v2b_onkayit_dogrula(cikti: Optional[str] = None, test: str = "A", git: bool = True, tablo: bool = True) -> Dict[str, Any]:
    """Ret kapısı (`kos`, `pilot`, `cek`): ön kayıt var; mühür, VDYT2B.py sha256 ön kayıtla aynı; VDYT2.py / VDYT.py sha256'ları VDYT2 ön kaydıyla (ve bu ön
    kayıtla) aynı; (A) VDYT2 tablo sha256'ları aynı; (B / pilot / cek) örneklem listesi sha256 aynı; (git) ön kayıt, VDYT2B.py, liste git'e işlenmiş ve
    değişmemiş. Biri tutmazsa Vdyt2bHata (REDDEDİLİR)."""
    yol = _v2b_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise Vdyt2bHata(f"ön kayıt yok ({yol}): önce `python VDYT2B.py onkayit`; REDDEDİLDİ")
    oc = _v2b_onkayit_oku(yol); V = VDYT2B_ESIK["vdyt2"]
    if oc["esik"] != v2b_esik_sha():
        raise Vdyt2bHata(f"eşik mührü tutmuyor ({oc['esik']} != {v2b_esik_sha()}): eşikler ön kayıttan sonra değişmiş; REDDEDİLDİ")
    if oc["kod"] != v2b_kod_sha():
        raise Vdyt2bHata(f"VDYT2B.py sha256 ön kayıttakiyle aynı değil ({oc['kod']} != {v2b_kod_sha()}): kod değişmiş; REDDEDİLDİ")
    if V2.v2_kod_sha() != V["kod_sha"] or oc["vdyt2_kod"] != V["kod_sha"]:
        raise Vdyt2bHata(f"VDYT2.py değişmiş (sha256 {V2.v2_kod_sha()[:12]} != VDYT2 ön kaydı {V['kod_sha'][:12]}); REDDEDİLDİ")
    if V2.v2_v1_kod_sha() != V["vdyt_kod_sha"] or oc["vdyt_kod"] != V["vdyt_kod_sha"]:
        raise Vdyt2bHata(f"VDYT.py değişmiş (sha256 {V2.v2_v1_kod_sha()[:12]} != {V['vdyt_kod_sha'][:12]}); REDDEDİLDİ")
    if V2.v2_esik_sha() != V["esik_sha"]:
        raise Vdyt2bHata(f"VDYT2 eşik mührü değişmiş ({V2.v2_esik_sha()[:12]} != {V['esik_sha'][:12]}); REDDEDİLDİ")
    out = {"yol": yol, "esik": oc["esik"], "kod": oc["kod"], "zaman": oc["zaman"], "dosya_sha256": V1.vdyt_sha_dosya(yol)}
    if test == "A" and tablo:
        simdi = v2b_tablo_sha(); fark = sorted(k for k in set(simdi) | set(oc["tablo"]) if simdi.get(k) != oc["tablo"].get(k))
        if fark:
            raise Vdyt2bHata(f"VDYT2 ara tabloları ön kayıttakiyle aynı değil: {fark[:6]} ({len(fark)}); REDDEDİLDİ")
    if test in ("B", "pilot", "cek"):
        yl = _v2b_yol("liste", cikti)
        if not os.path.exists(yl) or oc["liste"] in (None, "YOK") or V1.vdyt_sha_dosya(yl) != oc["liste"]:
            raise Vdyt2bHata(f"örneklem listesi yok ya da sha256 ön kayıttakiyle aynı değil ({yl}); REDDEDİLDİ")
        if git:
            out["git_liste"] = _v2b_git(yl, "örneklem listesi")
    if git:
        out["git_onkayit"] = _v2b_git(yol, "VDYT2B ön kaydı"); out["git_kod"] = _v2b_git(os.path.join(KOK_VDYT2B, "VDYT2B.py"), "VDYT2B.py")
    return out


def _v2b_git(yol: str, ne: str) -> Dict[str, str]:
    try:
        return V1.vdyt_git_islenmis(yol, ne)
    except V1.VdytHata as ex:
        raise Vdyt2bHata(str(ex)) from None


def _v2b_pilot_oku(cikti: Optional[str], E: Dict[str, Any]) -> Dict[str, Any]:
    y = _v2b_yol("pilot", cikti)
    if not os.path.exists(y):
        raise Vdyt2bHata("pilot sonucu yok: önce `python VDYT2B.py pilot`; REDDEDİLDİ")
    k = _v2b_json_oku(y)["karar"]
    if k["karar"] not in E["B"]["pilot"]["kos_izin"]:
        raise Vdyt2bHata(f"pilot kararı {k['karar']}: B testinin geri kalanı KOŞULMAZ (ön kayıt kuralı); REDDEDİLDİ")
    return k


def v2b_kos(test: str = "A", cikti: Optional[str] = None, isci: int = 3, git_sart: bool = True, F_ver: Optional[Dict[str, Dict[str, Any]]] = None,
            kl: Optional[str] = None, E: Optional[Dict[str, Any]] = None, B_hazir: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """`kos --test A|B`: ret kapısı -> ölçüm -> sonuç JSON + rapor. A: VDYT2 tabloları + fiyat; B: pilot + çekim tamam + batan satırları."""
    E = E or VDYT2B_ESIK; t0 = time.time()
    oc = v2b_onkayit_dogrula(cikti, test=test, git=git_sart, tablo=(kl is None))
    if test == "A":
        Z = v2b_A_hazirla(None, F_ver, kl, None, E); R = v2b_A_analiz(Z, E); kap = v2b_A_kapsam(Z, E)
        out = {"test": "A", "zaman": _v2b_simdi(), "sure_sn": round(time.time() - t0, 1), "onkayit": oc, "karar": R["karar"], "satir": R["satir"], "yon": R["yon"],
               "kapsam": kap["sayim"]}
        _v2b_json(_v2b_yol("sonuc_A", cikti), out); _v2b_yaz(_v2b_yol("rapor_A", cikti), v2b_rapor_metin(out)); return out
    if test != "B":
        raise Vdyt2bHata(f"bilinmeyen test: {test}")
    pk = _v2b_pilot_oku(cikti, E); cd = _v2b_json_oku(_v2b_yol("cek", cikti)) if os.path.exists(_v2b_yol("cek", cikti)) else None
    if not cd or not cd.get("tamam"):
        raise Vdyt2bHata("çekim tamamlanmamış (vdyt2b_cek_durum.json 'tamam' değil): önce `python VDYT2B.py cek`; REDDEDİLDİ")
    L = _v2b_liste_oku(_v2b_yol("liste", cikti))
    if not pk["otcq_dahil"]:
        L = L[L.kaynak != "OTCQ"]
    L["N_h"] = L.N_h.astype(int)
    if B_hazir is None:
        F_k60 = (F_ver or {}).get("ABD") or _v2b_fiyat("ABD"); F_b, Tb = v2b_batan_fiyat(L, cd["durum"], E, F_k60=F_k60)
        Bs = v2b_batan_satirlar(F_b, isci, F_k60)
        Gy = v2b_etiketle(v2b_tablo_oku("satir", "ABD", "G5", kl), F_k60, E); Ky = v2b_etiketle(v2b_tablo_oku("kontrol", "ABD", "G5", kl), F_k60, E)
    else:
        F_b, Tb, Bs, Gy, Ky = B_hazir["F_b"], B_hazir["Tb"], B_hazir["Bs"], B_hazir["Gy"], B_hazir["Ky"]
    w = Tb.set_index("ticker").w; kol = E["B"]["kolon"]
    Gb = v2b_etiketle(Bs["G"], F_b, E).assign(w=lambda x: x.sembol.map(w).astype(float)) if len(Bs["G"]) else Bs["G"].assign(w=np.nan)
    Kb = v2b_etiketle(Bs["K"], F_b, E).assign(w=lambda x: x.sembol.map(w).astype(float)) if len(Bs["K"]) else Bs["K"].assign(w=np.nan)
    Gy, Ky = (X.assign(w=1.0) for X in (Gy, Ky))
    Gy, Ky, Gb, Kb = (X[[k for k in kol if k in X]] for X in (Gy, Ky, Gb, Kb))
    R = v2b_B_analiz(Gy, Ky, Gb, Kb, E)
    out = {"test": "B", "zaman": _v2b_simdi(), "sure_sn": round(time.time() - t0, 1), "onkayit": oc, "pilot": pk, "karar": R["karar"], "satir": R["satir"],
           "bilgi": R["bilgi"], "semboller": Tb, "hisse_hata": Bs.get("hata", {})}
    _v2b_json(_v2b_yol("sonuc_B", cikti), out); _v2b_yaz(_v2b_yol("rapor_B", cikti), v2b_rapor_metin(out))
    return out


def _v2b_md(rows: List[Dict[str, Any]], kol: List[str], n: int = 4) -> str:
    L = ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
    for r in rows:
        h = []
        for k in kol:
            v = r.get(k)
            h.append(V1._t(v, n) if isinstance(v, (float, np.floating)) and np.isfinite(v) else ("—" if v is None or (isinstance(v, float) and not np.isfinite(v)) else str(v).replace("|", " / ")))
        L.append("| " + " | ".join(h) + " |")
    return "\n".join(L) + "\n"


def v2b_rapor_metin(R: Dict[str, Any]) -> str:
    """Rapor: karar tablosu önce; sonra ANA ve bilgi satırları; kapsam; yanlılık notu. Sonuç doğrulanmış sinyal değildir."""
    S = R["satir"] if isinstance(R["satir"], pd.DataFrame) else pd.DataFrame(R["satir"])
    kol = ["pazar", "tanim", "asama", "etiket", "onkosul", "kontrol", "n1", "n0", "ort1", "ort0", "fark", "alt", "ust", "oran"]
    L = [f"# VDYT2-B raporu — test {R['test']} — {VDYT2B_ETIKET}\n\nKoşu {R['zaman']} ({R['sure_sn']} sn). Kod {str(R['onkayit'].get('kod', ''))[:12]}, mühür "
         f"{str(R['onkayit'].get('esik', ''))[:12]}, ön kayıt commit {R['onkayit'].get('git_onkayit', {}).get('commit', '—')}. Bu bir SAĞLAMADIR: VDYT2 sonuçları ve "
         "Ç163 DEĞİŞMEZ; KASA dönemi VDYT2'de açılmıştı, aynı veriyle sağlama için kullanıldı. Sonuç doğrulanmış sinyal değildir.\n\n## 1. Karar\n\n"]
    L.append(_v2b_md(R["karar"], [k for k in ("pazar", "etiket", "sutun", "rol", "wf", "kasa", "sonuc") if any(k in r for r in R["karar"])]))
    if R["test"] == "A":
        a = S[S.ana] if len(S) else S
        L.append("\n## 2. ANA hücre (G5, P1, MA1)\n\n" + _v2b_md(a.to_dict("records"), kol))
        b = S[(S.tanim == "G5") & (S.onkosul == "P1") & (~S.ana)] if len(S) else S
        L.append("\n## 3. G5 P1 bilgi (MA2, MA3, aynı satırlarda BH1 = Y20)\n\n" + _v2b_md(b.to_dict("records"), kol))
        Y = R["yon"] if isinstance(R["yon"], pd.DataFrame) else pd.DataFrame(R["yon"])
        L.append("\n## 4. Yön payı (bilgi; MA1 / MA2 / MA3 hareketinde yukarı payı)\n\n" + _v2b_md(Y.to_dict("records"), list(Y.columns) if len(Y) else []))
        c = S[(S.etiket == "MA1") & (~S.ana)] if len(S) else S
        L.append("\n## 5. MA1 bütün tanımlar x ön koşul x kontrol (bilgi)\n\n" + _v2b_md(c.to_dict("records"), kol))
        K = pd.DataFrame(R.get("kapsam", []))
        L.append("\n## 6. Kapsam (satır sayısı)\n\n" + _v2b_md(K[K.tanim == "G5"].to_dict("records") if len(K) else [], list(K.columns) if len(K) else []))
    else:
        kolb = ["kume", "etiket", "asama", "onkosul", "kontrol", "n1", "n0", "ort1", "ort0", "fark", "alt", "ust", "oran"]
        L.append("\n## 2. Birleşik / batan / yaşayan oranları\n\n" + _v2b_md(S.to_dict("records"), kolb))
        Bi = R["bilgi"] if isinstance(R["bilgi"], pd.DataFrame) else pd.DataFrame(R["bilgi"])
        L.append("\n## 3. Batanlarda (2) / (3) bilgi\n\n" + _v2b_md(Bi.to_dict("records"), list(Bi.columns) if len(Bi) else []))
        T = R["semboller"] if isinstance(R["semboller"], pd.DataFrame) else pd.DataFrame(R["semboller"])
        L.append("\n## 4. Bütün örneklem sembolleri (başarısızlar dahil; hiçbiri sonuç görülerek çıkarılmadı)\n\n"
                 + _v2b_md(T.to_dict("records"), [k for k in ("ticker", "tabaka", "rol", "veri", "spac", "bar", "ilk", "son", "w") if k in T]))
    L.append("\nYanlılık: Tiingo kapsamı (2010-2014 çıkışları eksik; OTC'ye düşüp Q eki almayanlar kapsanmaz), kod yeniden kullanımı (pilot K6), OTC dönemi (uygunluk "
             "eşiği çoğunu dışarıda bırakır), temettü düzeltmesi yok (k60 ile aynı), batanlarda olay özellikleri boş (yalnız (1) karar).\n")
    return "".join(L)


def v2b_rapor(test: str = "A", cikti: Optional[str] = None) -> str:
    y = _v2b_yol(f"sonuc_{test}", cikti)
    if not os.path.exists(y):
        raise Vdyt2bHata(f"sonuç yok: {y}")
    R = _v2b_json_oku(y); R["satir"] = pd.DataFrame(R["satir"])
    return _v2b_yaz(_v2b_yol(f"rapor_{test}", cikti), v2b_rapor_metin(R))


def v2b_kapsam(cikti: Optional[str] = None, F_ver: Optional[Dict[str, Dict[str, Any]]] = None, kl: Optional[str] = None) -> Dict[str, Any]:
    """`kapsam`: A için YALNIZ SAYIM (ölçülebilir satır sayısı). Etiket değeri / oran / yön YOK."""
    Z = v2b_A_hazirla(None, F_ver, kl); K = v2b_A_kapsam(Z); K["tablo_sha256"] = v2b_tablo_sha(kl=kl)
    _v2b_json(_v2b_yol("kapsam", cikti), K)
    return K


def v2b_onkayit(cikti: Optional[str] = None, metin_fn: Optional[Callable[[str], str]] = None) -> str:
    """Ön kaydı yazar. Git'e işlenmiş ön kayıt varsa ÜZERİNE YAZMAZ (mühür / kod aynıysa yolu döndürür, değilse durur)."""
    yol = _v2b_yol("onkayit", cikti)
    if os.path.exists(yol) and _v2b_git_izli(yol):
        oc = _v2b_onkayit_oku(yol)
        if oc["esik"] != v2b_esik_sha() or oc["kod"] != v2b_kod_sha():
            raise Vdyt2bHata("ön kayıt git'e işlenmiş ve mühür / kod farklı; üzerine yazılmadı (SAPMA yazılıp yeniden işlenmeli)")
        return yol
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    _v2b_yaz(yol, (metin_fn or v2b_onkayit_metin)(zaman, cikti))
    v2blog.info("ön kayıt yazıldı: %s (mühür %s, kod %s)", yol, v2b_esik_sha()[:12], v2b_kod_sha()[:12])
    return yol


_V2B_GOVDE = """Bu dosya, VDYT2B.py ve örneklem listesi (vdyt2b_orneklem.tsv) git'e işlenmeden; eşik mührü, VDYT2B.py sha256'sı, VDYT2.py / VDYT.py sha256'ları (VDYT2 ön
kaydındakiyle aynı), VDYT2 ara tablo sha256'ları (A) ve liste sha256'sı (B) tutmadan `kos`, `pilot` ve `cek` ÇALIŞMAZ (Vdyt2bHata, çıkış 1). Sonuç görüldükten
sonra tanım, eşik, evren, örneklem, kontrol ya da karar kuralı değişmez; değişirse bu dosyada tarihli SAPMA yazılır ve ön kayıt yeniden işlenir.

## 0. Amaç ve sınır
- Cemal (12 Kasım 2026, aynen): 'İkisini de yap. Önce bir saatlik ön kayıt ve ölçütleri sabitleme; sonra veri çekme ve test. Özellikle başarısız örnekleri
  dışarıda bırakmayalım. Aksi hâlde yalnızca başarılı hisseleri inceleyerek sistemi olduğundan iyi sanabiliriz.'
- Bu iş bir SAĞLAMADIR. VDYT2 sonuçları (WF ve KASA raporları) ve IZ_KARNE Ç163 kararı ((1) bölgeyi bulmak BAŞARILI; (2) genişleme zamanı ve (3) yön
  BAŞARISIZ) DEĞİŞMEZ. VDYT2.py ve VDYT.py içe aktarılır, değiştirilmez. KASA bu işte yeniden 'açılmaz': VDYT2'de açılmış KASA dönemi (2024-01-01 -> 2026-08-31)
  aynı veriyle sağlama için kullanılır (yeni karar değil).
- Yalnız başarı (1) sağlanır. (2) ve (3) mutlak etiketle YENİDEN ÖLÇÜLMEZ (yalnız yön payı BİLGİ). Sonuç doğrulanmış sinyal değildir.

## 1. A — MUTLAK HAREKET SAĞLAMASI (başarı (1) için)
Gerekçe: VDYT2'de büyük hareket (BH1) bölgenin kendi küçük mumlarına göre tanımlıydı (büyük mum = TR >= 2,5 x bölge medyan TR); sessiz bölgede referans küçük
olduğu için 'bölge sonrası büyük mum' kısmen mekanik olabilir. A'da etiket bölgeden BAĞIMSIZ ve mutlaktır.
- σ[t] = t'ye kadar (t dahil) son 250 barın günlük ln getirisinin std'si (ddof 1, en az 200 geçerli getiri). ATR250[t] = son 250 barın ortalama gerçek
  aralığı (TR = max(H-L, |H-C[-1]|, |L-C[-1]|); en az 200). İkisi de YALNIZ t ve öncesinden (bölge kullanılmaz).
- MA1 (ANA): max_k=1..20 |ln(C[t+k] / C[t])| >= max(ln 1,15; 3 x σ[t] x √20). Yön = eşiği İLK aşan günün işareti. ('%15' ln ölçeğinde simetrik:
  yukarı +%15, aşağı -%13,1 basit getiri.)
- MA2 (BİLGİ): |ln(C[t+20] / C[t])| >= 2 x σ[t] x √20 (yalnız uç nokta). Yön = uç nokta işareti.
- MA3 (BİLGİ): max_k=1..20 TR[t+k] >= 3 x ATR250[t]. Yön = ilk büyük TR gününün C - C[-1] işareti.
- Ölçülemez (NaN): t + 20 > son bar, (t, t+20] içinde kopukluk (> 15 takvim günü; V1.vdyt_kopuk), σ / ATR250 tanımsız.
- Satırlar: VDYT2 (1)'in satırlarının AYNISI (yeniden hesaplanmaz): /tmp/vdyt2/kasa/satir_<pazar>_<tanım>.csv.gz ve kontrol_<pazar>_<tanım>.csv.gz (VDYT2
  `kos --asama kasa` ara çıktısı; wf klasöründekilerle içerik sha256'sı aynı, ön kayıt anında denetlendi; içerik sha256'ları EK-1). Satır kümesi: VDYT2 (1)
  kuralı (karar günü dönemde, son20 <= dönem sonu, y20 ölçülebilir) VE MA etiketi ölçülebilir. Hizalama denetimi: her satırda tarih == temiz fiyat serisinin
  t. barı (V2.v2_fiyat; VDYT2 ile aynı kesikli seri); tek satır tutmazsa koşu durur.
- Kontroller VDYT2 ile aynı: DIŞARI (tabaka sembol x yıl x NATR ondalığı) ve RASTGELE (tabaka yıl x yaş); kontrol, tabaka içinde gerçeğin dağılımına
  yeniden ağırlıklanır; hisse kümeli bootstrap B = 2000, tohum 20261112, %95.
- KARAR (1)-MUTLAK: ANA hücre = tanım G5, ön koşul P1, etiket MA1. BAŞARILI <=> gerçek oran - DIŞARI oranı > 0 ve %95 alt > 0 VE gerçek - RASTGELE > 0 ve
  alt > 0; WF (2019-2023) VE KASA'da; BIST ve ABD AYRI. n < 30 ya da tanımsız -> VERİ YOK. P0 / P2, öteki 15 tanım (AILE / ALT), MA2, MA3 ve aynı
  satırlarda BH1 (Y20) BİLGİ. Yön payı (MA hareketlerinde yukarı payı; gerçek / DIŞARI / RASTGELE) BİLGİ.

## 2. B — BATANLAR DAHİL SAĞLAMA (Tiingo ücretsiz katman; yalnız ABD)
### 2.1 Doğrulama pilotu (12 sembol; çekimden önce)
Tiingo'nun borsadan silinmiş şirketlerin fiyat geçmişini eksiksiz verdiği VARSAYILMAZ. supported_tickers listesinde (aşağıdaki 'liste' sütunu) görülen:
Tiingo iflas eden şirketin bütün geçmişini çoğunlukla bugünkü OTC 'Q' kodu altında tutuyor (SIVBQ PINK 1990-03-26 -> ; BBBYQ; RADCQ), bazen borsa dönemini ayrı
kayıtta bırakıyor (DNR NYSE -> 2020-07-30 ve DNRCQ PINK 2020-07-31 ->), kod yeniden kullanımında iki kayıt açıyor (SUNE NYSE 1995-2016 ve SUNE NASDAQ) ya da tek
kayıtta iki hisseyi birleştirmiş olabiliyor (CHK 1993-2024: 2020 iflasında eski hisse iptal, 2021-02-10 yeni hisse aynı kodla). Pilot bunları sınar.
Bilinen tarih = EDGAR Form 25-NSE (borsanın kotasyondan çıkarma bildirimi) tarihi, YEREL EDGAR dizininden (SEC'e istek yok).

| kod | şirket | CIK | Form 25-NSE | tür | Tiingo listesi |
|---|---|---|---|---|---|
{pilot_tablo}
Tür: Q = bütün geçmiş bugünkü OTC Q kodunda; BORSA = borsa dönemi ayrı kayıt; YENIDEN = kod yeniden kullanımı (karışma sınaması).
Pilot ölçütleri (sembol başına; önceden):
- K1 seri: HTTP 200 ve kapanışı > 0 en az 252 bar.
- K2 son gün: BORSA: son bar ∈ [F25 - 60 iş günü, F25 + 10 iş günü] (borsa önce işlemi askıya alır, Form 25 sonra gelir; arada haftalar olabilir); Q: son bar >=
  F25 - 60 iş günü VE [F25 - 60, F25 + 10] iş günü penceresinde en az 1 bar (borsa dönemi kotasyondan çıkışa kadar seride); YENIDEN: F25 - 60 iş gününden
  önceki 60 iş gününde bar var (eski şirketin dönemi seride).
- K3 boşluk: A = (BORSA: son bar; Q / YENIDEN: F25 - 60 iş günü); [A - 60 iş günü, A] penceresinde eksik iş günü <= 5 ve en uzun boşluk <= 5 iş günü (ABD
  federal tatil takvimi).
- K4 kaba tutarlılık (kaynak varsa; yoksa DEĞERLENDİRİLMEDİ, karara girmez): SIVBQ 2023-03-09 ham kapanışı basında bildirilen 106,04 $'ın ±%10'u içinde;
  SUNE Tiingo serisi ↔ k34_yahoo SUNE (bugünkü şirket) ve CHK ↔ k60_fiyat EXE (yeni hisse, 2021-02-10 -> 2024-10): ortak günlerde günlük ln getiri
  korelasyonu >= 0,90 ve |kapanış oranı - 1| medyanı <= %2 (bölünme düzeltmeli). (SUNE / CHK'de K4'ün tutması 'yeni şirketin serisi Tiingo kodunda' demektir;
  karışma K6 ile ölçülür.)
- K5 OHLCV: barların >= %95'inde açılış / yüksek / düşük / kapanış / hacim dolu, yüksek >= düşük, kapanış > 0.
- K6 karışma: YENIDEN: seri hem eski (yeni_bas'tan önceki 250 iş günü) hem yeni (sonraki 250 iş günü) dönemi içeriyorsa arada >= 30 iş günü boşluk olmalı
  (ayırt edilebilir); değilse KARIŞIK. Diğerleri: bölünme günü olmayan |günlük ln getiri| > ln 10 sıçrama yok.
- Sembol GEÇTİ <=> K1 VE K2 VE K3 VE K5 VE K6 VE (K4 değerlendirildiyse K4).
- PİLOT KARARI: GÜVENİLİR <=> >= 10 / 12 geçti; KISMEN <=> 7-9; GÜVENİLMEZ <=> <= 6. İki YENIDEN sembolünün ikisi de KARIŞIK ise karar en çok KISMEN.
  Q türünün HİÇBİRİ geçmezse OTCQ kaynağı B'den çıkarılır (beyan). GÜVENİLMEZ ise B testinin geri kalanı (çekim ve koşu) KOŞULMAZ; raporda yazılır.
### 2.2 Evren (supported_tickers; fiyat isteği YOK; kurallar sırasıyla, sayımlar EK-2)
1. assetType Stock, priceCurrency USD.
2. Kod ^[A-Z]{1,5}$ (nokta / tire / rakam yok: imtiyazlı, sınıf, birim); 5 harfli kodlarda son harf F G H I M N O P R S T U V W X Y Z ise atılır (yabancı,
   tahvil, imtiyazlı, hak, fayda payı, varant, birim, when-issued, fon, ADR); Q (iflas) ve A-E, J-L kalır.
3. Aynı kod listede birden çok Stock kaydıyla geçiyorsa (kod yeniden kullanımı; API'nin hangi seriyi vereceği belirsiz) bütün kayıtları atılır.
4. k60 evreninde (bugün yaşayan, VDYT2'de zaten olan) kod atılır.
5. BORSA kaynağı: exchange ∈ {NYSE, NASDAQ, NYSE MKT, AMEX}, endDate ∈ [2019-02-01, 2026-06-30], startDate <= endDate - 400 gün.
6. OTCQ kaynağı: exchange ∈ {PINK, OTCMKTS, EXPM, OTCGREY, OTCQB, OTCQX, OTCBB, OTCCE, OTCD}, kod ^[A-Z]{3,4}Q$ (iflas eki), endDate >= 2019-02-01,
   startDate <= min(endDate - 400 gün, 2025-06-30). AYRIK OTC dönemi (ilk 3 harfi aynı bir borsa kaydının endDate'i Q kaydının startDate'inden en çok 10 gün
   uzakta: borsa dönemi BORSA kaynağında) atılır.
7. SPAC kabuğu (çekim öncesi): kod + 'U' ya da kod + '-U' birim kaydı var VE birimin endDate'i >= kodun endDate'i - 30 gün (kabuk birleşmeden tasfiye /
   kapanış) -> atılır. Birleşip sonra yaşayan ya da batan şirket (birimi erken biten) KALIR.
### 2.3 Tabakalama ve örneklem (çekimden ÖNCE; liste dosyası vdyt2b_orneklem.tsv, sha256 başlıkta)
- Tabaka = kaynak (BORSA / OTCQ) x endDate yılı (OTCQ'da endDate > 2026-06-30 ise 'OTC_HALA': bugün de OTC'de kotalı). Son piyasa değeri / son fiyat listede
  yok (fiyat isteği gerekir) -> tabakaya girmez.
- ANA 450 (orantılı dağıtım, en büyük kalan; her dolu tabakada en az 1) + YEDEK 38 (kalan evrenden orantılı). Tabaka içinde sıra: numpy default_rng(20261117 +
  tabaka sırası) permütasyonu (tabakalar adla sıralı; tabaka içinde kodlar adla sıralı). İlk n_h ANA, sonraki y_h YEDEK.
- YEDEK yalnız aynı tabakada VERİ YOK (HTTP 404 / boş / temiz bar < 252) olan ANA sembolün yerine, sırayla kullanılır. Başka hiçbir nedenle (sonuç, getiri,
  etiket) yedek kullanılmaz; hiçbir sembol sonuç görülerek çıkarılmaz.
### 2.4 Çekim sonrası kurallar (önceden; etiket / sonuç görülmeden uygulanır; hepsi raporda sembol sembol listelenir)
- D1 VERİ YOK: HTTP 404 / boş / temiz bar < 252 -> yedekle değiştirilir.
- D2 SPAC KALIBI: ham kapanışların >= %80'i [9, 11] $ aralığında -> SPAC kabuğu: evren dışı, değiştirilmez.
- D4 KOD DEĞİŞİKLİĞİ: son 60 barın günlük ln getirisi bir k60 serisiyle (ortak gün >= 55) korelasyon >= 0,98 VE ln(kapanış oranı) std <= 0,01 -> aynı şirket
  yaşayan evrende (ör. CHK -> EXE): evren dışı, değiştirilmez (çift sayımı önler).
- D3: VDYT uygunluğunu (>= 252 bar, ekrandaki fiyat >= 2 $, 20 gün medyan işlem değeri >= 1 mn $) hiç sağlamayan sembol ÇIKARILMAZ (evrenin üyesidir; satırı
  olmaz, ağırlık paydasında kalır).
- Fiyat: Tiingo ham OHLCV + splitFactor -> bölünme düzeltmeli seri = ham / (gelecekteki bölünme oranlarının çarpımı), hacim x aynı çarpım (Yahoo / k60 ile aynı
  tür: bölünme düzeltmeli, temettü düzeltmesiz); ekrandaki fiyat = ham kapanış (meta 'bolunme' ile V1.vdyt_bolunme_carpan aynı sonucu verir). V1.vdyt_bar_temizle
  + 2010-01-01 .. 2026-08-31 kesiti (VDYT2 ABD ile aynı).
- Ağırlık (ters olasılık): tabaka h için w_h = N_h / m_h; m_h = h'de verisi gelen örneklem sayısı (D2 ve D4 dahil: evren dışı payı N_h'yi aynı oranda küçültür).
  Yaşayan (k60) satırlar w = 1.
### 2.5 B işlemi ve karar
- Batan satırları VDYT2 kodu ile üretilir (V2._v2_hisse_is; tanım YALNIZ G5; kip 'kos'; DIŞARI ve RASTGELE kontrolleri dahil, aynı tohum kuralı). ABD paneli
  (uygunluk, NATR ondalığı, tertiller) k60 + batan örneklemi BİRLİKTE kurulur (V1.vdyt_panel). Yaşayan satırlar VDYT2 tablolarından AYNEN alınır (yeniden
  hesaplanmaz). Olay özellikleri batanlarda boş (VDYT2 olay kaynakları yaşayanlar için; makro olaylar var): yalnız (2) / (3) modellerini etkiler, burada model yok.
- Etiketler: y20 (BH1; VDYT2 ile aynı) ve MA1 (A ile aynı). Satır kümesi A ile aynı kural (VDYT2 (1) satırı VE MA1 ölçülebilir; iki etiket aynı satırlarda).
- (a) yalnız batanlar (ağırlıklı): gerçek / DIŞARI / RASTGELE oranları ve farkları (BİLGİ; n küçük olabilir).
- (b) BİRLEŞİK evren (yaşayan w = 1 + batan w_h): (1)-BATANLAR DAHİL BAŞARILI <=> G5, P1: gerçek - DIŞARI > 0 ve alt > 0 VE gerçek - RASTGELE > 0 ve alt > 0;
  WF VE KASA. y20 ve MA1 ayrı sütun. Ağırlıklı karşılaştırma: tabaka içinde kontrol ağırlığı = w x (Σw_gerçek / Σw_kontrol); ağırlıklar 1 iken VDYT2'nin
  v2_oran_karsilastir'ı ile birebir aynı (test).
- Batanlarda (2) / (3) BİLGİ: y20 = 1 satırlarında yukarı payı, r20 ve MAE ortalaması (ağırlıklı), yaşayanlarla yan yana.

## 3. İstek bütçesi ve takvim (Tiingo ücretsiz katman: ayda 500 farklı sembol, saatte 50, günde 1.000 istek)
- Kodda sert sınırlar: saatte en çok 45 istek, günde en çok 900, takvim ayı (UTC) içinde en çok 500 farklı sembol. Kalıcı sayaç /tmp/vdyt2b/tiingo_sayac.json
  (istek gönderilmeden ÖNCE kaydedilir); sınıra gelince bekler, ay sınırında durur. 429 -> 15 dk bekle, art arda 3 kez -> dur. Önbellek /tmp/vdyt2b/tiingo/
  (repoya veri YOK; Tiingo lisansı). Önbellekte olan sembol yeniden istenmez.
- Pilot: 12 istek (12 farklı sembol; birkaç dakika). Örneklem: 450 ANA (SHLDQ ve YELLQ hem pilotta hem örneklemde: önbellekten, ek istek yok) -> 448 istek +
  en çok 38 yedek. Ay toplamı en çok 12 + 448 + 38 = 498 farklı sembol (< 500). Saatte 45 ile ~10-11 saat (günlük 900 sınırı bağlamaz). Çekim kaldığı yerden
  sürer.
- Anahtar YALNIZ ortamdan (TIINGO_API_KEY); yoksa istek 'Authorization: Token proxy' başlığıyla gider (oturumun ağ vekili gerçek anahtarı enjekte edebilir).
  Anahtar URL'ye, loga, önbelleğe, sayaca ya da çıktıya yazılmaz (test).

## 4. Yanlılık beyanı
- Tiingo kapsamı: 2010-2014 çıkışları listede az (envanter); bu iş 2019+ çıkışları kullanır. Borsadan düşüp OTC'de Q eki almadan işlem gören (iflassız
  kotasyondan çıkma: fiyat < 1 $, rapor gecikmesi) şirketler OTC listesinde ayırt edilemez -> KAPSANMAZ (yalnız borsa kaydı ölü olanlar BORSA kaynağında).
- Kod yeniden kullanımı: listede yinelenen kodlar atılır; tek kayıtta iki hisseyi birleştiren seri (CHK türü) ayırt edilemeyebilir -> pilot K6 ve D4 ile kısmen;
  kalan risk beyan. Kopukluk (> 15 takvim günü boşluk) VDYT2 kuralıyla zaten etiketi bölmez (NaN).
- OTC dönemi: uygunluk (fiyat >= 2 $, işlem değeri >= 1 mn $) OTC barlarının çoğunu dışarıda bırakır; batan satırlarının çoğu borsa dönemindendir.
- Temettü düzeltmesi yok (k60 ile aynı tür); bölünme düzeltmesi Tiingo splitFactor'dan.
- Kapalı uçlu fon / NYSE ADR'leri listede ad olmadığı için ayıklanamaz (5 harfli F / Y elenir; 4 harfli ADR kalır).
- Yaşayan evren k60'tır (Tiingo aktif evreninin 2024'te ~%70'i; envanter): birleşik evren 'bütün ABD' değil 'k60 + batan örneklemi'dir.
- Örneklem: evrenin ~%20'si (450 / 2.219); batan sonuçlarının belirsizliği hisse kümeli bootstrap'ta (ağırlıklı) görünür.
- A'da satırlar ve kontroller VDYT2'den aynen: VDYT2'nin yaşayan evren yanlılığı A'da da vardır (A'nın sorusu etiketin mekanikliğidir).

## 5. SAPMA / BOŞLUK (iş tanımına göre; ölçümden önce)
1. B evreninde endDate alt sınırı 2016-01-01 değil 2019-02-01: 2016-2018 çıkışlarının karar satırları 2019 öncesindedir; başarı (1) yalnız WF test yılları
   (2019-2023) ve KASA'da ölçüldüğü için katkıları SIFIR olurdu (ayda 500 sembollük bütçe boşa gider). Sayıları (2016-01 .. 2019-01 arası biten borsa kaydı)
   EK-2'de bilgi olarak yazıldı.
2. B evrenine OTCQ kaynağı eklendi ('exchange NYSE / NASDAQ / NYSE MKT' süzgeci tek başına iflas edenlerin çoğunu dışarıda bırakırdı: Tiingo bunların
   geçmişini bugünkü OTC Q kodunda tutuyor). 'Bugün işlem görmeyen' = 'bugün borsada işlem görmeyen'; OTC_HALA tabakası bugün OTC'de kotalı.
3. Tabakalama endDate yılı x kaynak (son piyasa değeri / son fiyat listede yok; fiyat isteği gerekir).
4. SPAC / fon / ADR / imtiyazlı / varant elemesi ad ile yapılamadı (listede şirket adı yok): kod kuralları + SPAC birim kuralı (çekim öncesi) + SPAC fiyat
   kalıbı (çekim sonrası) + kod değişikliği kuralı D4 (çekim sonrası).
5. Pilot listesi iş tanımındaki öneriden değişti: LK (yabancı ADR; örneklemde ADR elenir) ve FRC (banka: Form 25-NSE EDGAR'da yok, bilinen tarih yerelden
   doğrulanamaz) yerine HTZGQ, REVRQ, YELLQ, DNR, GNC. SIVB / BBBY / RAD / WE / SHLD Tiingo'da Q kodlarıyla (SIVBQ, BBBYQ, RADCQ, WEWKQ, SHLDQ). Son gün
   ölçütü '±10 iş günü' yerine [F25 - 60, F25 + 10] iş günü (bilinen tarih Form 25-NSE; askı ondan önce).
6. Pilot K4 kaynağı yalnız 3 sembolde var (SIVBQ basın kapanışı, SUNE k34 Yahoo, CHK ↔ k60 EXE); diğerlerinde DEĞERLENDİRİLMEDİ.
7. B yalnız ANA tanım G5 (AILE / ALT yok) ve etiketler y20 + MA1 (MA2 / MA3 yok).
8. B'de batan satırlarının kesit ondalıkları birleşik panelde (k60 + batan örneklemi); yaşayan satırlar VDYT2 tablolarından aynen (birleşik panelde batan payı
   küçük; yaşayan satırların ondalığı değişmez).
9. A satırları VDYT2 ara tablolarından (yeniden hesaplanmaz; içerik sha256 EK-1). Tablolar kaybolursa VDYT2 kodu aynı veriyle (tohumlu) aynı tabloyu üretir;
   sha256 tutmalı (tutmazsa SAPMA).
10. A ve B satır kümesi: VDYT2 (1) satırları ∩ MA1 ölçülebilir (aynı satırlarda BH1 bilgi olarak yeniden hesaplanır; VDYT2 raporundaki BH1 sayılarından biraz az).
11. MA1 eşiği ln ölçeğinde simetrik (ln 1,15); σ penceresi t'yi içerir (C_t kapanışında bilinir).
12. SHLDQ ve YELLQ hem pilotta hem örneklemde (tohumlu seçim; önbellek; ek istek yok; örneklemde diğer semboller gibi işlenir).
13. Kapsam sayımı (EK-3) ön kayıttan hemen önce AYNI kodla yapıldı (vdyt2b_kapsam_A.json 'kod_sha256' = KOD_SHA256; değilse ret sebebi, ana oturum denetler).
14. `kos --test B` için pilot ve çekim dosyaları (vdyt2b_pilot.json, vdyt2b_cek_durum.json) çıktı klasörüne yazılır; Tiingo fiyatı içermez (yalnız durum,
    tarih, ölçüt sonucu; pilotta birkaç kapanış değeri).
15. BOŞLUK: batanlarda olay verisi yok; ABD dışı batan yok (BIST batanları VDYT2'de BIST_K62 ile bilgi olarak var); Tiingo listesi günlük değişir (sha256
    başlıkta; Faz 2 aynı liste dosyasıyla).

## 6. Faz 2 komutları
1. (ana oturum) bu dosyayı, VDYT2B.py'yi, test_vdyt2b.py'yi, vdyt2b_orneklem.tsv / vdyt2b_evren_sayim.json / vdyt2b_kapsam_A.json'u denetler, git'e işler.
2. `python -I VDYT2B.py kos --test A` -> vdyt2b_sonuc_A.json + VDYT2B_RAPOR_A.md (Tiingo gerekmez; ret kapısı: mühür, kodlar, tablo sha256, git).
3. TIINGO_API_KEY ortamda (ya da ağ vekili başlığı) -> `python VDYT2B.py pilot` (12 istek) -> vdyt2b_pilot.json (GÜVENİLİR / KISMEN / GÜVENİLMEZ).
4. Pilot GÜVENİLİR / KISMEN ise `python VDYT2B.py cek` (arka planda, ~10-11 saat; kaldığı yerden sürer; `--en-cok N` ile parçalı) -> vdyt2b_cek_durum.json.
5. `python -I VDYT2B.py kos --test B` -> vdyt2b_sonuc_B.json + VDYT2B_RAPOR_B.md. 6. `python VDYT2B.py rapor --test A|B` raporu JSON'dan yeniden yazar.

## 7. Değişmezlik
VDYT2B_ESIK değişirse ESIK_SHA256; VDYT2B.py değişirse KOD_SHA256; VDYT2.py / VDYT.py / VDYT2 eşikleri değişirse VDYT2_* satırları; VDYT2 tabloları değişirse
EK-1; liste değişirse LISTE_SHA256 tutmaz -> `kos` / `pilot` / `cek` durur.
"""


def v2b_onkayit_metin(zaman: str, cikti: Optional[str] = None) -> str:
    """Ön kayıt metni: başlık satırları (mühür, kodlar, liste, tablolar) + tanımlar + kapsam / evren sayımı. Uzun açıklamalar ön kayıt şablonundan."""
    E = VDYT2B_ESIK; yl = _v2b_yol("liste", cikti); ls = V1.vdyt_sha_dosya(yl) if os.path.exists(yl) else "YOK"
    ts = v2b_tablo_sha(); ev = _v2b_json_oku(_v2b_yol("evren", cikti)) if os.path.exists(_v2b_yol("evren", cikti)) else None
    kp = _v2b_json_oku(_v2b_yol("kapsam", cikti)) if os.path.exists(_v2b_yol("kapsam", cikti)) else None
    govde = _V2B_GOVDE.replace("{pilot_tablo}", "".join(f"| {x['kod']} | {x['sirket']} | {x['cik']} | {x['f25']} | {x['tur']} | {x['liste']} |\n"
                                                         for x in E["B"]["pilot"]["semboller"]))
    L = [f"# VDYT2-B ÖN KAYIT — VDYT2 sağlaması: A) mutlak hareket, B) batanlar dahil ({VDYT2B_ETIKET}) — ölçümden ÖNCE\n\n",
         f"Yazım zamanı: {zaman}\n", f"ESIK_SHA256: {v2b_esik_sha()}\n", f"KOD_SHA256: {v2b_kod_sha()}\n", f"VDYT2_KOD_SHA256: {V2.v2_kod_sha()}\n",
         f"VDYT_KOD_SHA256: {V2.v2_v1_kod_sha()}\n", f"VDYT2_ESIK_SHA256: {V2.v2_esik_sha()}\n", f"LISTE_SHA256: {ls}\n", f"Sürüm: {VDYT2B_SURUM}\n\n", govde]
    L.append("\n## EK-1. VDYT2 ara tablo içerik sha256'ları (A; `kos --test A` yeniden hesaplar, farklıysa ret)\n\n")
    L += [f"- {k}: sha256 {v}\n" for k, v in sorted(ts.items())]
    if ev:
        L.append(f"\n## EK-2. B evren sayımı (`liste`, {ev.get('zaman')}; supported_tickers sha256 {ev.get('st_sha256')}, listedeki en son endDate "
                 f"{ev.get('st_en_son_endDate')})\n\n")
        for k in sorted(k for k in ev if k[0].isdigit() or k in ("liste_satir", "evren", "evren_kaynak")):
            L.append(f"- {k}: {json.dumps(ev[k], ensure_ascii=False)}\n")
        L.append("\n| tabaka | evren N_h | örneklem n_h | yedek | ağırlık N_h / n_h |\n|---|---|---|---|---|\n")
        for tb, N in sorted(ev["tabaka_N"].items()):
            nh = ev["tabaka_n"].get(tb, 0)
            L.append(f"| {tb.replace('|', ' / ')} | {V1._t(N)} | {nh} | {ev['tabaka_yedek'].get(tb, 0)} | {V1._t(N / nh, 2) if nh else '—'} |\n")
        L.append(f"\nToplam: evren {V1._t(ev['evren'])}, örneklem {ev['orneklem_ana']} + yedek {ev['orneklem_yedek']}; liste dosyası {VDYT2B_DOSYA['liste']} "
                 f"(sha256 {ls}).\n")
    if kp:
        L.append(f"\n## EK-3. A kapsamı (YALNIZ SAYI; `python -I VDYT2B.py kapsam`, {kp.get('zaman')}; kod {str(kp.get('kod_sha256'))[:12]})\n\n"
                 "| pazar | dönem | kaynak | VDYT2 (1) satırı G5 P1 | MA1 ölçülebilir | MA3 ölçülebilir | hisse | VDYT2 satırı G5 P0 | MA1 ölçülebilir P0 |\n"
                 "|---|---|---|---|---|---|---|---|---|\n")
        K = pd.DataFrame(kp["sayim"])
        for (pz, asama, kaynak), g in K[K.tanim == "G5"].groupby(["pazar", "asama", "kaynak"], sort=False):
            p1 = g[g.onkosul == "P1"].iloc[0]; p0 = g[g.onkosul == "P0"].iloc[0]
            L.append(f"| {pz} | {asama.upper()} | {kaynak} | {V1._t(p1.vdyt2_satir)} | {V1._t(p1.ma1_olculebilir)} | {V1._t(p1.ma3_olculebilir)} | {V1._t(p1.hisse)} | "
                     f"{V1._t(p0.vdyt2_satir)} | {V1._t(p0.ma1_olculebilir)} |\n")
    L.append("\n## EK-4. Eşik sözlüğü (mühür = sha256 of sıralı JSON)\n\n```json\n" + json.dumps(E, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n```\n")
    return "".join(L)


def _cakisma_kontrol_vdyt2b(_once=_CK_ONCE_VDYT2B, _dosya="VDYT2B.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_VDYT2B", "_CK_KAYIT", "_cakisma_kontrol_vdyt2b", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "gzip", "copy", "zipfile", "_dt", "annotations",
           "Any", "Callable", "Dict", "List", "Optional", "Tuple", "V1", "V2")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_vdyt2b()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=VDYT2B_SURUM)
    ap.add_argument("komut", choices=["liste", "kapsam", "onkayit", "pilot", "cek", "kos", "rapor"])
    ap.add_argument("--test", default="A", choices=["A", "B"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--isci", type=int, default=3)
    ap.add_argument("--en-cok", type=int, default=None, help="cek: bu koşuda en çok bu kadar istek")
    a_ = ap.parse_args()
    try:
        if a_.komut == "liste":
            s_ = v2b_liste(a_.cikti); print(json.dumps({k: s_[k] for k in ("evren", "orneklem_ana", "orneklem_yedek", "liste_sha256")}, ensure_ascii=False))
        elif a_.komut == "kapsam":
            k_ = v2b_kapsam(a_.cikti); print(_v2b_yol("kapsam", a_.cikti), len(k_["sayim"]), "sayım satırı")
        elif a_.komut == "onkayit":
            y_ = v2b_onkayit(a_.cikti); print(y_, "mühür", v2b_esik_sha(), "kod", v2b_kod_sha(), "dosya sha256", V1.vdyt_sha_dosya(y_))
        elif a_.komut == "pilot":
            print(json.dumps(v2b_pilot(a_.cikti)["karar"], ensure_ascii=False))
        elif a_.komut == "cek":
            c_ = v2b_cek(a_.cikti, en_cok=a_.en_cok); print(json.dumps({k: c_[k] for k in ("tamam", "plan", "sayac")}, ensure_ascii=False), len(c_["veri_yok"]), "veri yok")
        elif a_.komut == "kos":
            R_ = v2b_kos(a_.test, a_.cikti, a_.isci); print(json.dumps(V2._v2_kayit(R_["karar"]), ensure_ascii=False, indent=1))
        else:
            print(v2b_rapor(a_.test, a_.cikti))
    except (Vdyt2bHata, V2.Vdyt2Hata, V1.VdytHata, FileNotFoundError) as ex:
        v2blog.error("%s", _v2b_temiz(str(ex))); sys.exit(1)
