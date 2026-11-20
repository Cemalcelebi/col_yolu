# -*- coding: utf-8 -*-
"""KAZANANLAR — Ekim eş kümesinde (ESLER_<etiket>) en iyi gidenler ile en kötü gidenler arasındaki fark (SONRADAN BAKMA, keşif).

SONRADAN BAKMA; BULGU DEĞİL; HİPOTEZ; ÖN KAYITLA SINANIR.

Küme: esler_pdf.es_kume (284 eş + 4 aday; kapı es_kapi = CANLI_SONUC). Tekilleştirme (K4, sonuçtan bağımsız kural): aynı sembol birden çok
grupta varsa EN ERKEN giriş günlü satır kalır (eşitlikte aday satırı, sonra aday adı sırası).
Sonuç: k15 = 15 geçerli barda en yüksek kapanış / giriş açılışı - 1 (esler_pdf max15 ile birebir; kapı), h5 = grubun stop geometrisiyle +%5.
KAZANAN = k15 sırasında ilk 20, KAYBEDEN = son 20, ORTA = gerisi.
Teknik ölçüler sinyal günü t'ye kadar: veri t'de KESİLİR (d[d.index <= t]) ve özellik kesik veride hesaplanır (geleceğe bakma mekanik kapalı).
Sektör: ABD sektor_ABD.csv (Yahoo etiketi, bugünkü hali), AVR Yahoo info (bugünkü hali); sektör ETF getirisi aynı 15 bar penceresinde (Yahoo).
Haber tablosu: KZ_HABER (elle WebFetch ile doğrulanmış; kaynak URL + tarih).

Kullanım: python arastirma_cikti/canli/kazananlar.py [etiket=2026-10-22] [veri=/tmp/veri_canli]
Yazı yeri: arastirma_cikti/canli/KAZANANLAR_<etiket>.md. Defter dosyalarına dokunmaz. Kod değişirse Colab'da çalışma zamanını yeniden başlat.
"""
from __future__ import annotations

import logging
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for _y in (KOK, os.path.dirname(os.path.abspath(__file__))):
    if _y not in sys.path:
        sys.path.insert(0, _y)

import CANLI_TARAMA as CT  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402
import esler_pdf as EP  # noqa: E402

kzlog = logging.getLogger("col.kazananlar")
if not kzlog.handlers:
    _h = logging.StreamHandler(sys.stderr); _h.setFormatter(logging.Formatter("%(asctime)s KZ %(levelname)s %(message)s"))
    kzlog.addHandler(_h); kzlog.setLevel(logging.INFO); kzlog.propagate = False

CIKTI = os.path.join(KOK, "arastirma_cikti", "canli")
KZ_BASLIK = "SONRADAN BAKMA; BULGU DEĞİL; HİPOTEZ; ÖN KAYITLA SINANIR."
KZ_ESIK = {"uc": 20, "ufuk": 15, "bh_q": 0.10, "atr_gun": 20, "hacim_gun": 20, "tepe_gun": 252, "sma": (20, 50, 200),
           "getiri": (5, 60), "dusus_gun": 60, "konum_gun": 120, "buyuk_gun": 250, "buyuk_parca": 25}
# Yahoo sektörü -> sektör ETF'i (ABD: SPDR Select Sector; AVR: iShares STOXX Europe 600 sektör ETF'leri, Xetra; yaklaşık eşleme)
KZ_ETF = {"ABD": {"Technology": "XLK", "Financial Services": "XLF", "Healthcare": "XLV", "Industrials": "XLI", "Energy": "XLE",
                  "Basic Materials": "XLB", "Utilities": "XLU", "Consumer Defensive": "XLP", "Consumer Cyclical": "XLY",
                  "Real Estate": "XLRE", "Communication Services": "XLC"},
          "AVR": {"Technology": "EXV3.DE", "Financial Services": "EXV1.DE", "Healthcare": "EXV4.DE", "Industrials": "EXH4.DE",
                  "Energy": "EXH1.DE", "Basic Materials": "EXV6.DE", "Utilities": "EXH9.DE", "Consumer Defensive": "EXH3.DE",
                  "Consumer Cyclical": "EXV5.DE", "Real Estate": "EXI5.DE", "Communication Services": "EXV2.DE"}}
KZ_PIYASA = {"ABD": "SPY", "AVR": "EXSA.DE"}
KZ_OLCU = [("F15", "120 gün konumu (0 dip, 1 tepe)"), ("F17b", "60 gün düşüş: C_t / max(C, t-60..t-1) - 1"),
           ("F14", "büyük resim: 250 bar dip eğimi (yh_buyuk_egim)"), ("atr", "ATR20 / fiyat (oynaklık)"),
           ("rhac", "göreli hacim: V_t / ort(V, t-20..t-1)"), ("rhac5", "5 gün hacim / önceki 20 gün hacim"),
           ("S9", "Ş9 U dip (yh_s9_sartlar)"), ("S10", "Ş10 MACD uyumsuzluğu (yh_s10)"), ("F68", "MACD > sinyal (t)"),
           ("tepe52", "52 hafta tepeye uzaklık: C_t / max(H, 252) - 1"), ("sma20", "C_t / SMA20 - 1"), ("sma50", "C_t / SMA50 - 1"),
           ("sma200", "C_t / SMA200 - 1"), ("r5", "son 5 gün getiri"), ("r60", "son 60 gün getiri")]

# Haber / temel tablosu: WebFetch ile doğrulanan satırlar (kaynak URL + tarih). Doldurulmayan satır 'doğrulanamadı' yazılır.
KZ_HABER: Dict[str, Dict[str, str]] = {
    'CAPR': {'bilanco': '10 Kas 2026 Q3 (pencerede): zarar büyüdü ($0,73 / hisse), gelir yok', 'beklenti': 'öngörü yok; Yahoo sürpriz -%74', 'olay': 'FDA: deramiocel BLA karar tarihi 22 Kas 2026 (24 Ağu uzatıldı); fiyat karar öncesi koştu (2-4 Kas, 11 Kas +%26)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/CAPR/ (okundu 2026-11-20)'},
    'ARRY': {'bilanco': '4 Kas 2026 Q3 (pencerede): gelir $330M (yıllık düşüş), zarar', 'beklenti': 'yıl öngörüsü DÜŞÜRÜLDÜ ($1,34-1,40B)', 'olay': '4 Kas: Shoals (SHLS) ile hisse takaslı birleşme (SHLS da KAZANAN #17)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/ARRY/ (okundu 2026-11-20)'},
    'AXGN': {'bilanco': '28 Eki 2026 Q3 (pencerede): gelir +%26', 'beklenti': 'yıl gelir öngörüsü YÜKSELTİLDİ (>= $290M); Yahoo sürpriz +%60; o gün +%31', 'olay': 'doğrulanamadı (basın bülteni sayfasında yok)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/AXGN/ (okundu 2026-11-20)'},
    'TDOC': {'bilanco': '28 Eki 2026 Q3 (pencerede): gelir -%3, zarar daraldı, Adj. EBITDA +%14', 'beklenti': 'öngörü alt uçları yükseltildi (karışık); Yahoo sürpriz +%36; ertesi gün +%27', 'olay': 'doğrulanamadı (basın bülteni sayfasında yok)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/TDOC/ (okundu 2026-11-20)'},
    'JBLU': {'bilanco': '26 Eki 2026 Q3 (pencerede): gelir +%21, zarar büyüdü', 'beklenti': 'Q4 birim gelir +%18-22 öngörüsü (önceki öngörü kaynakta yok); Yahoo sürpriz -%9; ertesi gün +%19', 'olay': 'doğrulanamadı (basın bülteni sayfasında yok)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/JBLU/ (okundu 2026-11-20)'},
    'LQDA': {'bilanco': '10 Kas 2026 Q3 (pencerede): YUTREPIA satışı $222,7M (çeyreklik +%31)', 'beklenti': 'Yahoo sürpriz +%25; öngörü kaynakta yok', 'olay': '13 Eki (girişten ÖNCE): United Therapeutics ile küresel dava uzlaşması (14 Eki +%27)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/LQDA/ (okundu 2026-11-20)'},
    'REAL': {'bilanco': '29 Eki 2026 Q3 (pencerede): gelir +%19, net kâr $16M (geçen yıl zarar); Yahoo tarihi ilk koşuda gelmedi, ikinci koşuda geldi (Yahoo kararsızlığı)', 'beklenti': 'yıl öngörüsü YÜKSELTİLDİ', 'olay': '15 Eki (girişten ÖNCE): Fortress ile refinansman (+%16)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/REAL/ (okundu 2026-11-20)'},
    'FUN': {'bilanco': '5 Kas 2026 Q3 (pencerede): gelir -%11, Adj. EBITDA -%11 (devam eden parklarda +%1)', 'beklenti': 'Q4 öngörüsü geçen yılın altında; Yahoo sürpriz +%19; o gün +%17', 'olay': 'doğrulanamadı (basın bülteni sayfasında yok)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/FUN/ (okundu 2026-11-20)'},
    'NXT': {'bilanco': '28 Eki 2026 Q2 FY27 (pencerede): rekor gelir $1.109M', 'beklenti': 'yıl öngörüsü YÜKSELTİLDİ; Yahoo sürpriz +%19', 'olay': '29 Eki: SVP / NewEdge batarya ortaklığı', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/NXT/ (okundu 2026-11-20)'},
    'BHVN': {'bilanco': '29 Eki 2026 Q3 (pencerede)', 'beklenti': 'Yahoo sürpriz -%562 (zarar)', 'olay': '22 Eki (girişten 1 gün sonra): FDA Vyglxia yeniden başvurusunu kabul etti (karar 2027 Q1), gün içi +%25; 8 Eki (ÖNCE): Ono lisansı $80M peşin', 'analist': '22 Eki Baird hedef fiyat 42 -> 48 (Outperform)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/BHVN/ (okundu 2026-11-20); https://www.insidermonkey.com/news/biohaven-bhvn-soars-25-on-fda-drug-review-price-target-upgrade-1858483/ (22 Eki 2026)'},
    'SOUN': {'bilanco': '5 Kas 2026 Q3 (pencerede): gelir +%48 rekor, brüt marj %42,6 -> %34,1', 'beklenti': '2026 gelir $250-260M (önceki öngörü kaynakta yok); Yahoo sürpriz -%15', 'olay': '3-4 Kas: LG ve Ultraviolette ortaklıkları', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/SOUN/ (okundu 2026-11-20)'},
    'BRUN': {'bilanco': '12 Kas 2026 Q3 (pencere DIŞI; 15. bar 10 Kas): gelir +%496, o gün -%20', 'beklenti': 'kaynakta yok', 'olay': '26 Eki: backlog / $600M finansman güncellemesi (+%8)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/BRUN/ (okundu 2026-11-20)'},
    'SNEX': {'bilanco': 'pencerede YOK (18 Kas)', 'beklenti': '-', 'olay': 'doğrulanamadı (basın bülteni sayfasında yok)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/SNEX/ (okundu 2026-11-20)'},
    'NNE': {'bilanco': 'pencerede YOK', 'beklenti': '-', 'olay': '21 Eki IMPSA mühendislik anlaşması, 27 Eki Hyundai MOU (bağlayıcı değil)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/NNE/ (okundu 2026-11-20)'},
    'CSTM': {'bilanco': '28 Eki 2026 Q3 (pencerede): gelir +%22, net kâr +%35', 'beklenti': 'yıl öngörüsü YÜKSELTİLDİ; Yahoo sürpriz -%4; o gün -%0,5', 'olay': 'doğrulanamadı (basın bülteni sayfasında yok)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/CSTM/ (okundu 2026-11-20)'},
    'AESI': {'bilanco': '2 Kas 2026 Q3 (pencerede): net zarar $45M, Adj. EBITDA 50,8 -> 30,3M', 'beklenti': 'Yahoo sürpriz -%48; Q4 EBITDA $40-50M', 'olay': '22 Eki: $424M teminatlı köprü kredi (veri merkezi ekipmanı)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/AESI/ (okundu 2026-11-20)'},
    'MLYS': {'bilanco': '4 Kas 2026 Q3 (pencerede)', 'beklenti': 'Yahoo sürpriz -%19', 'olay': '22 Eki / 8 Kas lorundrostat verileri; FDA karar tarihi 22 Ara 2026 (pencere dışı)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/MLYS/ (okundu 2026-11-20)'},
    'BHF': {'bilanco': '5 Kas 2026 Q3 (pencerede)', 'beklenti': 'Yahoo sürpriz -%29', 'olay': 'bekleyen satın alma: Aquarian $70 / hisse nakit (fiyat teklif bandına kilitli; kapanış gecikiyor)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/BHF/ (okundu 2026-11-20)'},
    'SLM': {'bilanco': '22 Eki 2026 Q3 (giriş günü, pencerede)', 'beklenti': 'Yahoo sürpriz -%196; o gün -%10,8', 'olay': '20 Eki: temettü ilanı', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/SLM/ (okundu 2026-11-20)'},
    'RSI': {'bilanco': '28 Eki 2026 Q3 (pencerede): gelir +%39, net kâr +%93', 'beklenti': 'öngörü yalnız TEYİT edildi (yükseltilmedi); Yahoo sürpriz +%12; o gün -%10', 'olay': 'doğrulanamadı (basın bülteni sayfasında yok)', 'analist': 'doğrulanamadı (basın bülteni sayfasında yok)', 'iceriden': 'doğrulanamadı (basın bülteni sayfasında yok)', 'kaynak': 'https://www.stocktitan.net/news/RSI/ (okundu 2026-11-20)'},
}


# Yorum metni (sayılar üretildikten SONRA yazıldı; sayıları değiştirmez): sektör özeti, haber özeti, iz adayları.
KZ_EK: Dict[str, Any] = {
    "sektor_ozet": (
        "Okuma (sonradan bakma): KAZANAN'ların en çok 3 sektörü (Healthcare 5, Technology 5, Industrials 4) = 14 / 20 (%70); aynı üç sektör "
        "bütün kümede %45. Sektör YOĞUNLAŞMASI zayıf-orta; ama sektör ETF'i farkı YOK: KAZANAN'ların sektör ETF'i 15 barda medyan %+3,3, "
        "ORTA %+4,0, KAYBEDEN %+3,9; hisse - sektör ETF farkı KAZANAN'da medyan %+25,9. Yani kazananları 'sektör yükselişi' taşımadı; hareket "
        "hisseye özgü. Tek tema alt sektörde: güneş (Solar) 5 hissenin 3'ü KAZANAN (ARRY, NXT, SHLS; ARRY-SHLS birleşmesi 4 Kas) - XLK aynı "
        "dönemde düştü, yani tema sektör ETF'inde görünmez. KAYBEDEN'de Financial Services 5 / 20 (%25; kümede %12), KAZANAN'da 0."),
    "haber_ozet": (
        "Okuma (20 isim, stocktitan basın bülteni sayfaları + 1 haber; Yahoo EPS sürprizi): KAZANAN 10'un 10'unda pencerede bilanço var; "
        "KAYBEDEN 10'un 7'sinde (BRUN 12 Kas pencere dışı, SNEX 18 Kas, NNE yok). Bilanço 'iyi' (öngörü yükseltme) KAZANAN'da 3 (AXGN, NXT, REAL) "
        "+ 1 karışık (TDOC); KAYBEDEN'de 1 (CSTM, yine düştü) + 1 teyit (RSI, -%10). Öngörü DÜŞÜREN / zayıf bilanço KAZANAN'da da var "
        "(ARRY, FUN, JBLU, CAPR) ama bunlarda ayrı bir olay ya da beklentiden iyi tepki vardı. Bilanço DIŞI katalizör: KAZANAN'da 4 / 10 "
        "(CAPR FDA karar tarihi 22 Kas, ARRY birleşme, BHVN FDA kabulü + Baird hedef artışı, LQDA dava uzlaşması [girişten önce]); KAYBEDEN'de "
        "olumlu katalizör 0 / 10, bir yapısal fren (BHF: $70 nakit satın alma teklifine kilitli fiyat). Analist notu yalnız 1 isimde (BHVN) "
        "bulundu; içeriden alım hiçbir sayfada görülmedi (Form 4 taranmadı: 'doğrulanamadı'). Sonuç: kazananları ayıran 'iyi bilanço' değil, "
        "pencerede bir OLAY (bilanço ya da ikili katalizör) olması ve tepkinin yönü; yön t'de bilinmiyor."),
    "iz": [
        "Hepsi bu tablolardan türetildi (sonradan bakma); hiçbiri ölçülmüş iz değildir. Önerilen sınama: ORTAK CETVEL ufuk 15, S6 / Y1 olay "
        "kümesinde ve eşli (aynı gün, aynı kova) h5 / st5 ile; dönemler 2023 ve 2024-26 (kriz kesiği 31.08.2026), pazarlar ABD + AVR; eşik "
        "sonuç görülmeden yazılır, sonuca göre oynanmaz; çoklu karşılaştırma BH q 0,10 (3 hipotez).",
        "",
        "**H1 — Bilanço takvimi bir 'kuyruk büyüteci' (yön değil).** Tanım: giriş ile 15. bar arasında şirketin duyurulmuş bilanço günü var "
        "(BIL15 = 1). Bilgi tarihi: bilanço tarihinin DUYURU tarihi <= t olmalı (Yahoo geçmiş tarihleri gerçekleşen tarihtir; K2 için duyuru "
        "bülteni ya da >= 14 gün önceden bilinen takvim kullanılır). Bu kümede: KAZANAN 20 / 20, ötekiler %74 (Fisher p 0,005); ama bütün "
        "kümede bilançolu h5 %67 / st5 %27, bilançosuz h5 %73 / st5 %16. Ön kayıt önerisi: BIL15 = 1 olaylarda eşli st5 farkı >= +5 puan VE "
        "|eşli h5 farkı| < 5 puan ise 'kuyruk büyüteci' DOĞRU; karar kuralı önerisi: S6 adayında BIL15 = 1 ise giriş bilanço SONRASINA "
        "ertelenir (ayrı kol olarak ölçülür: ertelenmiş giriş h5 >= bilanço öncesi giriş h5 + 5 puan, iki dönemde aynı yön).",
        "",
        "**H2 — Düşen bıçak: 120 günün tam dibine son 5 günde düşerek gelen hisse kaybeder.** Tanım: F15 <= 0,05 VE r5 <= -%3 (t'de). "
        "Bu kümede grup-göreli sırada KAYBEDEN F15 medyanı 0,023 (KAZANAN 0,088; MW p 0,037, BH sonrası KALMADI; ham sırada 0,043 / 0,067, p 0,27), r5 medyanı KAYBEDEN -%4,7 (KAZANAN %0,0; p 0,16); tanıma uyan "
        "77 hissede h5 %64 / st5 %32, ötekilerde h5 %71 / st5 %21. Ön kayıt önerisi: tanıma uyan olaylarda eşli h5 farkı <= -5 puan VE st5 farkı "
        ">= +5 puan, dört hücreden (ABD / AVR x 2023 / 2024-26) en az üçünde aynı yön; tutarsa S6 seçicisinde dışlama kuralı adayı.",
        "",
        "**H3 — Önceden bilinen ikili katalizör (FDA karar tarihi / bekleyen birleşme oylaması) öncesi koşu.** Tanım: biyotek / ilaç hissesinde "
        "FDA PDUFA ya da danışma kurulu tarihi t + 5 ile t + 40 takvim günü arasında (tarih t'de kamuya açık). Bu kümede: CAPR (PDUFA 22 Kas; "
        "15 barda %+92) ve BHVN (FDA kabulü 22 Eki) KAZANAN; MLYS'te PDUFA 22 Ara (t + 60, pencere dışı) KAYBEDEN. n çok küçük (2-3): bu yalnız "
        "literatürdeki 'PDUFA öncesi koşu' iddiasının bizim cetvelle sınanması önerisidir. Ön kayıt önerisi: PDUFA penceresindeki olaylarda "
        "eşli h5 farkı >= +10 puan, n >= 30 hücre başına (yetmezse ÖLÇÜLEMEDİ); veri: FDA takvim kaynakları (WebFetch ile doğrulanan tarih + "
        "duyuru günü). Avrupa'da karşılığı yok: en fazla ABD-ADAY.",
        "",
        "Elenenler (bu tablolarda ayrım yok): göreli hacim, 52 hafta tepeye uzaklık, SMA 20 / 50 / 200 konumu, 60 gün getiri, Ş9, Ş10, MACD, "
        "önceki çeyrek EPS sürprizi (KAZANAN vs KAYBEDEN p 0,47). Sektör ETF yükselişi kazananları açıklamıyor (ETF medyanları eşit).",
        "",
        "K1 uyarısı (mekanik üstünlük): k15 'en yüksek kapanış' ölçüsü oynak hisseyi kendiliğinden öne çıkarır (ATR / fiyat KAZANAN 0,050, "
        "ORTA 0,036; k15 ile rho 0,12). Aynı stop uzaklığında oynaklık üst üçte birinde h5 %61 / st5 %39, ötekilerde h5 %73 / st5 %16: oynaklık "
        "k15'i büyütür ama +%5-stop cetvelinde ZARAR yazar. Bu yüzden oynaklık iz adayı yapılmadı.",
    ],
}


class KZHata(RuntimeError):
    pass


def kz_ozellik(df: pd.DataFrame, t: pd.Timestamp) -> Dict[str, float]:
    """Sinyal günü t'ye kadar teknik ölçüler. Veri t'de KESİLİR; t geçerli bar değilse KZHata."""
    E = KZ_ESIK
    with CT.ct_kriz_ac():
        d = YH._yh_hazir(df)
    d = d[d.index <= t]
    if not len(d) or d.index[-1] != t:
        raise KZHata(f"t {t.date()} geçerli bar değil")
    O, H, L, C, V = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    i = len(C) - 1; F: Dict[str, float] = {}
    k = E["konum_gun"]; c = C[max(0, i - k + 1):]
    F["F15"] = float((C[i] - c.min()) / (c.max() - c.min())) if len(c) == k and c.max() > c.min() else np.nan
    q = E["dusus_gun"]
    F["F17b"] = float(C[i] / np.max(C[i - q:i]) - 1) if i >= q else np.nan
    G = E["buyuk_gun"]
    e = YH.yh_buyuk_egim(L[i - G:i], E["buyuk_parca"]) if i >= G else np.nan
    F["F14"] = float(e) if np.isfinite(e) else np.nan
    tr = YH._yh_trp(H, L, C); a = E["atr_gun"]
    F["atr"] = float(np.mean(tr[i - a + 1:i + 1])) if i >= a else np.nan
    g = E["hacim_gun"]; mv = float(np.mean(V[i - g:i])) if i >= g else np.nan
    F["rhac"] = float(V[i] / mv) if np.isfinite(mv) and mv > 0 else np.nan
    mv2 = float(np.mean(V[i - 25:i - 5])) if i >= 25 else np.nan
    F["rhac5"] = float(np.mean(V[i - 4:i + 1]) / mv2) if np.isfinite(mv2) and mv2 > 0 else np.nan
    try:
        F["S9"] = float(bool(YH.yh_s9_sartlar(YH.yh_s9_ozellik(d, [t], hazir=True))["S9"][0]))
    except Exception as ex:  # tanımsızsa NaN, neden loglanır
        kzlog.warning("Ş9 %s: %s", t.date(), ex); F["S9"] = np.nan
    try:
        S10 = YH.yh_s10_ozellik(d, [t], hazir=True).iloc[0]
        F["S10"] = float(S10["S10"]); F["F68"] = float(S10["F68"])
    except Exception as ex:  # tanımsızsa NaN
        kzlog.warning("Ş10 %s: %s", t.date(), ex); F["S10"] = F["F68"] = np.nan
    T = E["tepe_gun"]
    F["tepe52"] = float(C[i] / np.max(H[max(0, i - T + 1):i + 1]) - 1)
    for n in E["sma"]:
        F[f"sma{n}"] = float(C[i] / np.mean(C[i - n + 1:i + 1]) - 1) if i >= n - 1 else np.nan
    for n in E["getiri"]:
        F[f"r{n}"] = float(C[i] / C[i - n] - 1) if i >= n else np.nan
    return F


def kz_k15(df: pd.DataFrame, giris: pd.Timestamp, u: int = KZ_ESIK["ufuk"]) -> Tuple[float, float, pd.Timestamp]:
    """Bağımsız k15: giriş günü açılışı ve 15 geçerli barın en yüksek kapanışı. Döner (E0, k15, 15. barın tarihi)."""
    with CT.ct_kriz_ac():
        d = YH._yh_hazir(df)
    w = d[d.index >= giris].iloc[:u]
    if len(w) < u or w.index[0] != giris:
        raise KZHata(f"giriş {giris.date()}: 15 geçerli bar yok")
    E0 = float(w.Open.iloc[0])
    return E0, float(w.Close.max() / E0 - 1), w.index[-1]


def kz_kume(etiket: str, veri: Optional[str]) -> Tuple[pd.DataFrame, Dict[str, Dict[str, pd.DataFrame]], List[str]]:
    """288 satır (284 eş + 4 aday) -> tekil küme. k15 kapısı: bağımsız k15 = esler max15 (eşlerde), E0 = yh E0 (adaylarda)."""
    K = EP.es_kume(etiket, veri); kapi = EP.es_kapi(K["Z"], K["E"])
    Es = K["E"].assign(rol="eş"); Z = K["Z"]
    Ad = pd.DataFrame({"pazar": Z.pazar, "aday": Z.sembol, "sinyal": pd.to_datetime(Z.tarih), "giris": pd.to_datetime(Z.giris),
                       "kova": Z.hucre.astype(int), "sembol": Z.sembol, "E0": Z.E0.astype(float), "h5": Z.h5.astype(float),
                       "h10": Z.h10.astype(float), "st5": Z.st5.astype(float), "max15": np.nan, "rol": "aday"})
    A = pd.concat([Es[Ad.columns], Ad], ignore_index=True)
    if len(Es) != 284 or len(Ad) != 4:
        raise KZHata(f"küme boyu beklenen değil: eş {len(Es)}, aday {len(Ad)}")
    k15, son = [], []
    for r in A.itertuples(index=False):
        E0, k, s = kz_k15(K["V"][r.pazar][r.sembol], pd.Timestamp(r.giris))
        if abs(E0 / r.E0 - 1) > 1e-9:
            raise KZHata(f"{r.sembol}: giriş açılışı tutmuyor ({E0} / {r.E0})")
        if np.isfinite(r.max15) and abs(k - r.max15) > 1e-9:
            raise KZHata(f"{r.sembol}: k15 esler max15 ile tutmuyor ({k} / {r.max15})")
        k15.append(k); son.append(s)
    A["k15"] = k15; A["son15"] = son
    kapi.append(f"k15 bağımsız hesap = esler max15: {int(A.max15.notna().sum())} eş satırında birebir (1e-9); 4 adayda giriş açılışı yh E0 ile birebir")
    n0 = len(A)
    A = A.sort_values(["sembol", "giris", "rol", "aday"], ascending=[True, True, True, True]).drop_duplicates("sembol", keep="first")
    kapi.append(f"tekilleştirme: {n0} satır -> {len(A)} tekil sembol (en erken giriş; {n0 - len(A)} tekrar satırı atıldı)")
    return A.reset_index(drop=True), K["V"], kapi


def kz_grup(A: pd.DataFrame) -> pd.DataFrame:
    n = KZ_ESIK["uc"]
    A = A.sort_values(["k15", "sembol"], ascending=[False, True]).reset_index(drop=True)
    A["sira"] = np.arange(1, len(A) + 1)
    A["grup"] = np.where(A.sira <= n, "KAZANAN", np.where(A.sira > len(A) - n, "KAYBEDEN", "ORTA"))
    return A


def kz_teknik(A: pd.DataFrame, Vt: Dict[str, Dict[str, pd.DataFrame]]) -> pd.DataFrame:
    sat = []
    for r in A.itertuples(index=False):
        try:
            F = kz_ozellik(Vt[r.pazar][r.sembol], pd.Timestamp(r.sinyal))
        except KZHata as ex:
            kzlog.warning("%s: %s", r.sembol, ex); F = {}
        sat.append(F)
    F = pd.DataFrame(sat, index=A.index)
    return pd.concat([A, F.reindex(columns=[k for k, _ in KZ_OLCU])], axis=1)


def kz_bh(p: np.ndarray, q: float) -> np.ndarray:
    """Benjamini-Hochberg: q düzeyinde reddedilenler (NaN p reddedilmez)."""
    p = np.asarray(p, float); m = int(np.isfinite(p).sum()); out = np.zeros(len(p), bool)
    if not m:
        return out
    idx = np.flatnonzero(np.isfinite(p)); o = idx[np.argsort(p[idx])]
    ok = p[o] <= q * np.arange(1, m + 1) / m
    if ok.any():
        out[o[:np.flatnonzero(ok).max() + 1]] = True
    return out


def kz_test(A: pd.DataFrame) -> pd.DataFrame:
    from scipy.stats import mannwhitneyu
    sat = []
    for k, ad in KZ_OLCU:
        g = {x: A.loc[A.grup == x, k].astype(float).dropna() for x in ("KAZANAN", "ORTA", "KAYBEDEN")}
        p = float(mannwhitneyu(g["KAZANAN"], g["KAYBEDEN"], alternative="two-sided").pvalue) if min(len(g["KAZANAN"]), len(g["KAYBEDEN"])) >= 5 else np.nan
        # bilgi: k15 ile Spearman (bütün küme; uç seçiminden bağımsız)
        x = A[[k, "k15"]].astype(float).dropna()
        rho = float(x[k].rank().corr(x.k15.rank())) if len(x) > 10 else np.nan
        sat.append({"olcu": k, "tanim": ad, **{f"med_{x}": float(v.median()) if len(v) else np.nan for x, v in g.items()},
                    **{f"n_{x}": int(len(v)) for x, v in g.items()}, "p": p, "rho": rho})
    T = pd.DataFrame(sat)
    T["bh"] = kz_bh(T.p.to_numpy(), KZ_ESIK["bh_q"])
    from scipy.stats import spearmanr
    pr = []
    for k, _ in KZ_OLCU:
        x = A[[k, "k15"]].astype(float).dropna()
        pr.append(float(spearmanr(x[k], x.k15).pvalue) if len(x) > 10 else np.nan)
    T["p_rho"] = pr; T["bh_rho"] = kz_bh(T.p_rho.to_numpy(), KZ_ESIK["bh_q"])
    return T


def kz_sektor(A: pd.DataFrame) -> pd.DataFrame:
    """ABD: sektor_ABD.csv (sembol.AM; BILINMIYOR ise Yahoo info); AVR: Yahoo info (bugünkü etiket); yoksa 'yok'."""
    S = pd.read_csv(os.path.join(KOK, "sektor_ABD.csv"))
    S["s"] = S.sembol.str.replace(r"\.AM$", "", regex=True); m = dict(zip(S.s, S.sektor)); me = dict(zip(S.s, S.endustri))
    sek, end = [], []
    for r in A.itertuples(index=False):
        if r.pazar == "ABD" and m.get(r.sembol, "BILINMIYOR") not in ("BILINMIYOR", "yok") and isinstance(m.get(r.sembol), str):
            sek.append(m[r.sembol]); end.append(me.get(r.sembol, "yok"))
        else:                                  # AVR ve sektor_ABD.csv'de BILINMIYOR olan ABD: Yahoo info (bugünkü etiket)
            try:
                import yfinance as yf
                inf = yf.Ticker(r.sembol).info
                sek.append(inf.get("sector") or "yok"); end.append(inf.get("industry") or "yok")
            except Exception as ex:  # ağ yoksa 'yok'
                kzlog.warning("Yahoo sektör %s: %s", r.sembol, ex); sek.append("yok"); end.append("yok")
    return A.assign(sektor=sek, endustri=end)


def kz_etf(A: pd.DataFrame) -> pd.DataFrame:
    """Sektör ETF'i ve piyasa ETF'i: giriş açılışından 15. barın kapanışına getiri (aynı takvim penceresi). Veri yoksa NaN."""
    import yfinance as yf
    sem = sorted({v for p in KZ_ETF for v in KZ_ETF[p].values()} | set(KZ_PIYASA.values()))
    bas = pd.Timestamp(A.giris.min()) - pd.Timedelta(days=5); son = pd.Timestamp(A.son15.max()) + pd.Timedelta(days=3)
    D = yf.download(sem, start=str(bas.date()), end=str(son.date()), progress=False, auto_adjust=False, group_by="ticker")

    def ret(s: str, a: pd.Timestamp, b: pd.Timestamp) -> float:
        try:
            x = D[s].dropna(subset=["Open", "Close"])
            if a not in x.index or b not in x.index:
                return np.nan
            return float(x.loc[b, "Close"] / x.loc[a, "Open"] - 1)
        except Exception:  # sembol inmediyse NaN
            return np.nan
    etf, re, rp = [], [], []
    for r in A.itertuples(index=False):
        e = KZ_ETF[r.pazar].get(r.sektor); etf.append(e or "yok")
        re.append(ret(e, pd.Timestamp(r.giris), pd.Timestamp(r.son15)) if e else np.nan)
        rp.append(ret(KZ_PIYASA[r.pazar], pd.Timestamp(r.giris), pd.Timestamp(r.son15)))
    return A.assign(etf=etf, r_etf=re, r_piyasa=rp)


def kz_bilanco(A: pd.DataFrame) -> pd.DataFrame:
    """Yahoo earnings tarihleri (get_earnings_dates): ÖNCE = [giriş - 14 takvim günü, giriş) (karar günü bilinen), SONRA = [giriş, 15. bar]
    (sonuç penceresi; t'de bilinmez, açıklayıcı). Sürpriz % Yahoo'nun EPS sürprizi. Inmezse 'yok' (NaN)."""
    import yfinance as yf
    sat = []
    for r in A.itertuples(index=False):
        g0, s15 = pd.Timestamp(r.giris), pd.Timestamp(r.son15); x = {"bil_once": np.nan, "bil_sonra": np.nan, "bil_tarih": "", "surpriz": np.nan,
                                                                   "onceki_surpriz": np.nan}
        try:
            e = yf.Ticker(r.sembol).get_earnings_dates(limit=12)
            if e is not None and len(e):
                tz = pd.DatetimeIndex(e.index).tz_localize(None).normalize()
                once = (tz >= g0 - pd.Timedelta(days=14)) & (tz < g0); sonra = (tz >= g0) & (tz <= s15)
                x["bil_once"] = float(once.any()); x["bil_sonra"] = float(sonra.any())
                k = np.flatnonzero(once | sonra)
                if len(k):
                    x["bil_tarih"] = str(tz[k[0]].date())
                    sp = e["Surprise(%)"].iloc[k[0]] if "Surprise(%)" in e else np.nan
                    x["surpriz"] = float(sp) if pd.notna(sp) else np.nan
                # t'de BİLİNEN: ÖNCE penceresinden de önceki son açıklanmış çeyreğin EPS sürprizi
                ok_ = np.flatnonzero((tz < g0 - pd.Timedelta(days=14)) & e["Reported EPS"].notna().to_numpy()) if "Reported EPS" in e else []
                if len(ok_):
                    j_ = ok_[np.argmax(tz[ok_])]; sp0 = e["Surprise(%)"].iloc[j_]
                    x["onceki_surpriz"] = float(sp0) if pd.notna(sp0) else np.nan
        except Exception as ex:  # Yahoo inmezse NaN; neden loglanır
            kzlog.warning("bilanço %s: %s", r.sembol, str(ex)[:100])
        sat.append(x)
    return pd.concat([A, pd.DataFrame(sat, index=A.index)], axis=1)


def kz_goreli(A: pd.DataFrame) -> pd.DataFrame:
    """Dayanıklılık: k15 - aynı aday grubunun k15 medyanı (gün / kova farkını çıkarır); bu sırayla ilk / son 20."""
    A = A.copy(); A["k15g"] = A.k15 - A.groupby("aday").k15.transform("median")
    o = A.k15g.rank(ascending=False, method="first"); n = KZ_ESIK["uc"]
    A["grup_g"] = np.where(o <= n, "KAZANAN", np.where(o > len(A) - n, "KAYBEDEN", "ORTA"))
    return A


def kz_bilanco_md(A: pd.DataFrame) -> List[str]:
    """Bütün kümede Yahoo bilanço tarihi / sürpriz özeti (hesaplanan; elle yazılmaz)."""
    from scipy.stats import fisher_exact, mannwhitneyu
    x = A.dropna(subset=["bil_sonra"]); kz = x.grup == "KAZANAN"
    t = pd.crosstab(kz, x.bil_sonra.astype(int)).reindex(index=[False, True], columns=[0, 1], fill_value=0)
    p = float(fisher_exact(t.to_numpy())[1])
    L = ["### Bilanço takvimi bütün kümede (Yahoo earnings tarihleri; bilgi)", "",
         "SONRA = bilanço [giriş, 15. bar] içinde (t'de sonucu bilinmez; tarihi çoğunlukla önceden duyurulur). ÖNCE = [giriş - 14 gün, giriş). "
         "Sürpriz = Yahoo EPS sürprizi %. Önceki sürpriz = ÖNCE penceresinden önceki son açıklanmış çeyrek (t'de bilinen).", "",
         "| grup | n (Yahoo tarihi var) | ÖNCE payı | SONRA payı | SONRA sürpriz > 0 payı | sürpriz medyan | önceki sürpriz > 0 payı | önceki sürpriz medyan |",
         "|---|---|---|---|---|---|---|---|"]
    for g in ("KAZANAN", "ORTA", "KAYBEDEN"):
        y = A[A.grup == g]; yb = y.dropna(subset=["bil_sonra"]); s_ = y.surpriz.dropna(); o_ = y.onceki_surpriz.dropna()
        L.append(f"| {g} | {len(yb)} / {len(y)} | %{yb.bil_once.mean() * 100:.0f} | %{yb.bil_sonra.mean() * 100:.0f} | "
                 f"%{(s_ > 0).mean() * 100:.0f} (n {len(s_)}) | {_s(s_.median(), 1)} | %{(o_ > 0).mean() * 100:.0f} (n {len(o_)}) | {_s(o_.median(), 1)} |")
    b = x.groupby(x.bil_sonra.astype(int))
    L += ["", f"KAZANAN içinde SONRA bilanço {int(t.loc[True, 1])} / {int(t.loc[True].sum())}, ötekilerde {int(t.loc[False, 1])} / "
          f"{int(t.loc[False].sum())} (Fisher p {_s(p, 4)}; sonradan bakma, tek test). Bütün kümede SONRA bilançolu / bilançosuz: "
          + "; ".join(f"{'bilançolu' if k else 'bilançosuz'} n {len(v)}, h5 %{v.h5.mean() * 100:.0f}, stop önce (st5) %{v.st5.mean() * 100:.0f}, "
                      f"k15 medyan {_y(v.k15.median())}, 15. bar getiri medyan {_y(v.r15.median())}" for k, v in b) + ".", ""]
    o = A.dropna(subset=["onceki_surpriz"])
    if len(o) > 10:
        L.append("Önceki çeyrek sürprizi (t'de bilinen) ile: " + "; ".join(
            f"{'önceki sürpriz > 0' if k else 'önceki sürpriz <= 0'} n {len(v)}, h5 %{v.h5.mean() * 100:.0f}, k15 medyan {_y(v.k15.median())}"
            for k, v in o.groupby(o.onceki_surpriz > 0)) + ". Mann-Whitney önceki sürpriz KAZANAN vs KAYBEDEN p " +
            _s(float(mannwhitneyu(A[A.grup == "KAZANAN"].onceki_surpriz.dropna(), A[A.grup == "KAYBEDEN"].onceki_surpriz.dropna()).pvalue), 4) + ".")
        L.append("")
    return L


# ---------------------------------------------------------------- yazım
def _y(x: float, n: int = 1) -> str:
    return "-" if x is None or not np.isfinite(x) else f"%{x * 100:+.{n}f}".replace(".", ",")


def _s(x: float, n: int = 3) -> str:
    return "-" if x is None or not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


def kz_md(etiket: str, A: pd.DataFrame, T: pd.DataFrame, kapi: List[str], ek: Dict[str, Any]) -> str:
    L = [f"# Kazananlar vs kaybedenler — Ekim eşleri (liste {etiket})", "", f"**{KZ_BASLIK}**", "",
         "**Bu dosya keşiftir. Sonuç (k15) görüldükten sonra bakılmıştır; buradaki hiçbir fark bir kural ya da iz değildir. Her hipotez yalnız "
         "ön kayıtla, başka dönem / başka küme üzerinde sınanır. Alım-satım kararı Cemal'indir.**", "",
         "Küme: ESLER_2026-10-22.md (284 eş + 4 aday; giriş 21-23 Ekim 2026; 3 ABD + 1 AVR grubu). k15 = 15 geçerli barda en yüksek kapanış / "
         "giriş açılışı - 1; h5 = 15 barda +%5 stop'tan önce (grubun stop geometrisi). KAZANAN = k15 ilk 20, KAYBEDEN = son 20, ORTA = gerisi. "
         "Teknik ölçüler sinyal günü t'de, veri t'de kesilerek. Hayatta kalma: evren bugün işlem gören hisseler (yukarı yanlı). "
         "Giriş günleri farklı (21 / 22 / 23 Ekim) ve gruplar farklı kovalardan: k15 sırası kısmen gün ve kova farkını da taşır.", "",
         "Kapılar:", ""] + [f"- {k}" for k in kapi] + [""]
    # (a)
    L += ["## (a) Kazanan / kaybeden listeleri", ""]
    for g in ("KAZANAN", "KAYBEDEN"):
        X = A[A.grup == g]
        L += [f"### {g} ({len(X)})", "", "| sıra | sembol | pazar | rol / grup | giriş | k15 | h5 | sektör | endüstri |", "|" + "---|" * 9]
        for r in X.itertuples(index=False):
            L.append(f"| {r.sira} | {r.sembol} | {r.pazar} | {r.rol} / {r.aday} | {pd.Timestamp(r.giris).date()} | {_y(r.k15)} | {int(r.h5)} | "
                     f"{r.sektor} | {r.endustri} |")
        L.append("")
    gs = A.groupby("grup")
    L += ["Grup özeti: " + "; ".join(f"{g} n {len(x)}, k15 medyan {_y(x.k15.median())}, h5 payı %{x.h5.mean() * 100:.0f}"
                                     for g, x in ((g, gs.get_group(g)) for g in ("KAZANAN", "ORTA", "KAYBEDEN"))), "",
          "Kazanan / kaybedenlerin geldiği grup (aday adı): " +
          "; ".join(f"{g}: " + ", ".join(f"{k} {v}" for k, v in A[A.grup == g].aday.value_counts().items()) for g in ("KAZANAN", "KAYBEDEN")) +
          "; tüm küme: " + ", ".join(f"{k} {v}" for k, v in A.aday.value_counts().items()), ""]
    # (b)
    L += ["## (b) Teknik karşılaştırma (sinyal günü t; medyanlar)", "",
          f"Mann-Whitney iki yanlı (KAZANAN vs KAYBEDEN, n 20 / 20); {len(T)} test, Benjamini-Hochberg q 0,10. "
          "Spearman rho = ölçü ile k15 sıra ilişkisi bütün kümede (uç seçiminden bağımsız; kendi BH'si). YALNIZ BİLGİ.", "",
          "| ölçü | tanım | KAZANAN | ORTA | KAYBEDEN | MW p | BH q0,10 | rho (k15) | rho p | BH (rho) |", "|" + "---|" * 10]
    for r in T.itertuples(index=False):
        L.append(f"| {r.olcu} | {r.tanim} | {_s(r.med_KAZANAN)} | {_s(r.med_ORTA)} | {_s(r.med_KAYBEDEN)} | {_s(r.p, 4)} | "
                 f"{'KALDI' if r.bh else '·'} | {_s(r.rho, 2)} | {_s(r.p_rho, 4)} | {'KALDI' if r.bh_rho else '·'} |")
    Tg = ek.get("Tg")
    if Tg is not None:
        L += ["", "Dayanıklılık (gün / kova farkı çıkarılmış): sıra = k15 - aynı aday grubunun k15 medyanı; ilk / son 20 (KAZANAN-g / KAYBEDEN-g). "
              f"Mann-Whitney + BH q {KZ_ESIK['bh_q']:.2f}".replace(".", ",") + ":", "",
              "| ölçü | KAZANAN-g | ORTA-g | KAYBEDEN-g | MW p | BH |", "|---|---|---|---|---|---|"]
        for r in Tg.itertuples(index=False):
            L.append(f"| {r.olcu} | {_s(r.med_KAZANAN)} | {_s(r.med_ORTA)} | {_s(r.med_KAYBEDEN)} | {_s(r.p, 4)} | {'KALDI' if r.bh else '·'} |")
        L.append("")
    L += ["", "İkili ölçülerde (Ş9, Ş10, F68) medyan 0/1'dir; paylar: " +
          "; ".join(f"{k}: " + ", ".join(f"{g} %{A.loc[A.grup == g, k].mean() * 100:.0f}" for g in ("KAZANAN", "ORTA", "KAYBEDEN"))
                    for k in ("S9", "S10", "F68")), ""]
    # (c)
    L += ["## (c) Sektör", "", "| sektör | tüm küme n | pay | KAZANAN n | pay | KAYBEDEN n | pay | ETF | ETF 15 bar (medyan, kümede) |", "|" + "---|" * 9]
    sk = sorted(A.sektor.unique(), key=lambda s: (-int((A.sektor == s).sum()), s))
    for s in sk:
        a = A[A.sektor == s]; kz = A[(A.grup == "KAZANAN") & (A.sektor == s)]; kb = A[(A.grup == "KAYBEDEN") & (A.sektor == s)]
        L.append(f"| {s} | {len(a)} | %{len(a) / len(A) * 100:.0f} | {len(kz)} | %{len(kz) / 20 * 100:.0f} | {len(kb)} | %{len(kb) / 20 * 100:.0f} | "
                 f"{', '.join(sorted(set(a.etf)))} | {_y(a.r_etf.median())} |")
    L += ["", ek["sektor_ozet"], ""]
    L += ["Sektör ETF'i ve piyasa ETF'i aynı 15 bar penceresinde (giriş açılışı -> 15. barın kapanışı), grup medyanı:", "",
          "| grup | k15 medyan | hissenin 15. bar getirisi medyan | sektör ETF medyan | piyasa (SPY / EXSA) medyan | hisse - sektör ETF medyan |",
          "|---|---|---|---|---|---|"]
    for g in ("KAZANAN", "ORTA", "KAYBEDEN"):
        x = A[A.grup == g]
        L.append(f"| {g} | {_y(x.k15.median())} | {_y(x.r15.median())} | {_y(x.r_etf.median())} | {_y(x.r_piyasa.median())} | "
                 f"{_y((x.r15 - x.r_etf).median())} |")
    L += ["", "AVR sektör ETF eşlemesi yaklaşıktır (STOXX 600 sektör ETF'leri: Financial Services -> banka ETF'i, Consumer Cyclical -> otomotiv ETF'i); "
          "ETF verisi inmeyen satır '-'.", ""]
    # (d)
    L += ["## (d) Temel / haber (KAZANAN ilk 10 ve KAYBEDEN son 10)", "",
          "Pencere: giriş gününden önceki 10 gün ve sonraki 15 gün. Kaynaklar WebFetch ile okundu; okunamayan madde 'doğrulanamadı'.", "",
          "| grup | sembol | k15 | bilanço (tarih) | beklenti / öngörü | olay haberi (satın alma, anlaşma, FDA, sözleşme) | analist | içeriden alım | kaynak |",
          "|" + "---|" * 9]
    for g, X in (("KAZANAN", A[A.grup == "KAZANAN"].head(10)), ("KAYBEDEN", A[A.grup == "KAYBEDEN"].tail(10))):
        for r in X.itertuples(index=False):
            h = KZ_HABER.get(r.sembol, {})
            L.append(f"| {g} | {r.sembol} | {_y(r.k15)} | {h.get('bilanco', 'doğrulanamadı')} | {h.get('beklenti', 'doğrulanamadı')} | "
                     f"{h.get('olay', 'doğrulanamadı')} | {h.get('analist', 'doğrulanamadı')} | {h.get('iceriden', 'doğrulanamadı')} | "
                     f"{h.get('kaynak', '-')} |")
    L += ["", ek["haber_ozet"], ""]
    L += kz_bilanco_md(A)
    # (e)
    L += ["## (e) İZ ADAYLARI (hipotez; iddia değil; ön kayıtla sınanır)", ""] + ek["iz"] + [""]
    L += ["## Tam liste (276 tekil; sıra = k15)", "", "| sıra | sembol | pazar | grup | aday | k15 | h5 | " +
          " | ".join(k for k, _ in KZ_OLCU) + " | sektör |", "|" + "---|" * (8 + len(KZ_OLCU))]
    for r in A.itertuples(index=False):
        L.append(f"| {r.sira} | {r.sembol} | {r.pazar} | {r.grup} | {r.aday} | {_y(r.k15)} | {int(r.h5)} | " +
                 " | ".join(_s(getattr(r, k), 3) for k, _ in KZ_OLCU) + f" | {r.sektor} |")
    return "\n".join(L) + "\n"


def kz_hazirla(etiket: str = "2026-10-22", veri: Optional[str] = None) -> Dict[str, Any]:
    A, Vt, kapi = kz_kume(etiket, veri)
    A = kz_grup(A)
    r15 = []
    for r in A.itertuples(index=False):        # bilgi: 15. barın kapanışı / giriş - 1 (ETF ile aynı pencere)
        with CT.ct_kriz_ac():
            d = YH._yh_hazir(Vt[r.pazar][r.sembol])
        r15.append(float(d.loc[pd.Timestamp(r.son15), "Close"] / r.E0 - 1))
    A["r15"] = r15
    A = kz_teknik(A, Vt)
    A = kz_sektor(A)
    A = kz_etf(A)
    A = kz_bilanco(A)
    A = kz_goreli(A)
    T = kz_test(A)
    Tg = kz_test(A.assign(grup=A.grup_g))
    return {"A": A, "T": T, "Tg": Tg, "kapi": kapi}


if __name__ == "__main__":
    et = sys.argv[1] if len(sys.argv) > 1 else "2026-10-22"; vr = sys.argv[2] if len(sys.argv) > 2 else None
    try:
        # KZ_OKU: hesaplanmış ara çıktıdan yalnız md yaz (Yahoo / veri yeniden çekilmez; yorum metni değişince)
        R_ = pd.read_pickle(os.environ["KZ_OKU"]) if os.environ.get("KZ_OKU") else kz_hazirla(et, vr)
    except (KZHata, EP.ESHata) as ex_:
        kzlog.error("DURDU: %s", ex_); sys.exit(2)
    if os.environ.get("KZ_ARA"):              # ara çıktı (karalama klasörüne; repoya girmez)
        pd.to_pickle(R_, os.environ["KZ_ARA"])
    md_ = kz_md(et, R_["A"], R_["T"], R_["kapi"], {**KZ_EK, "Tg": R_["Tg"]})
    CT._ct_yaz(os.path.join(CIKTI, f"KAZANANLAR_{et}.md"), md_, "kazananlar md")
    kzlog.info("yazıldı KAZANANLAR_%s.md (%d tekil)", et, len(R_["A"]))
