"""K56 Faz 0 raporu: (1) etki envanteri, (2) açıklanmamış bulgular, (3) mekanizma hipotezleri, (4) hipotez × veri kaynağı, (5) veri kaynaklarının
kapsamı / gecikmesi / maliyeti (+ erişim testi ölçümleri), (6) doğrulama ve çürütme yöntemleri (+ M01 sentetik sınama), (7) veri eksiklikleri ve
teknik riskler, (8) önerilen uygulama sırası. Tablolar CSV'de tam, raporda özet."""
from __future__ import annotations

import os
from typing import Any, Dict, List

import numpy as np
import pandas as pd

# ---------------------------------------------------------------- (5) veri kaynakları: erişim testinde ölçülen + belgeden (kaynak sütunu)
KAYNAKLAR: List[Dict[str, str]] = [
    {"kimlik": "SEC_13F_DS", "sinif": "A_kurumsal_sahiplik", "ad": "SEC Form 13F veri setleri (INFOTABLE, SUBMISSION, COVERPAGE)", "erisim": "www.sec.gov/data-research/sec-markets-data/form-13f-data-sets (çeyreklik zip; 2024 sonrası 3 aylık dosya adları)",
     "kapsam": "2013q2 -> 2026; KEŞİF tam", "gecikme": "çeyrek sonundan 45 güne kadar; point-in-time için başvuru tarihi", "maliyet": "ücretsiz (kamu verisi)", "boyut": "KEŞİF 24 çeyrek ~1,1 GB zip (INFOTABLE çeyrek başına ~160 MB açık)",
     "eslesme": "CUSIP (9) -> sembol OpenFIGI; FIGI sütunu 2016'da çoğu boş", "olcer": "yönetici uzun pozisyonları, sahip sayısı, pay değişimi", "olcemez": "açığa satış, gün içi akış, 100 mn $ altı yöneticiler", "projede": "yok (Ç103'te CUSIP eşlemesinde tıkandı)"},
    {"kimlik": "OPENFIGI", "sinif": "A_kurumsal_sahiplik", "ad": "OpenFIGI eşleme API'si", "erisim": "POST api.openfigi.com/v3/mapping (anahtarsız 25 istek / dk, istek başına 10 kimlik; ücretsiz anahtarla daha fazla)",
     "kapsam": "güncel + tarihsel CUSIP'lerin çoğu", "gecikme": "-", "maliyet": "ücretsiz", "boyut": "-", "eslesme": "ID_CUSIP -> ticker, securityType, exchCode", "olcer": "13F CUSIP -> sembol", "olcemez": "değişmiş / kaldırılmış CUSIP'lerin bir kısmı", "projede": "yok"},
    {"kimlik": "SEC_NPORT_DS", "sinif": "A_kurumsal_sahiplik", "ad": "SEC Form N-PORT veri setleri (fon portföyleri)", "erisim": "www.sec.gov/data-research/sec-markets-data/form-n-port-data-sets", "kapsam": "2019q4 -> 2026; KEŞİF yalnız 2019q4-2021q4",
     "gecikme": "çeyrek sonu + 60 gün (yayın)", "maliyet": "ücretsiz", "boyut": "çeyrek ~440 MB zip", "eslesme": "CUSIP / ISIN / sembol", "olcer": "fon (yatırım şirketi) pozisyonları", "olcemez": "13F dışı kurumlar, 2019 öncesi", "projede": "yok"},
    {"kimlik": "SEC_INSIDER_DS", "sinif": "B_iceriden", "ad": "SEC Insider Transactions Data Sets (Form 3 / 4 / 5)", "erisim": "www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets",
     "kapsam": "2006q1 -> 2026q3; KEŞİF tam", "gecikme": "işlemden bildirime medyan 2 gün (2016q1), %90'ı <= 10 gün", "maliyet": "ücretsiz", "boyut": "KEŞİF 24 çeyrek ~248 MB zip (2016q1 13 MB)",
     "eslesme": "ISSUERCIK (+ sembol); yabancı özel ihraççı Form 4 vermez; ortak dosyalamada çift sayım riski", "olcer": "P / S / M / F / A / G kodlu işlemler, sahiplik sonrası pay",
     "olcemez": "10b5-1 planı 2023 öncesi yalnız dipnot metni (işaret sütunu 2023q1+); %10 altı fonlar", "projede": "K30 P özeti (k30_alim); K31 S satışları; ham zipler 2016q1-2026q1 bu oturumun karalama klasöründe (kalıcı değil)"},
    {"kimlik": "SEC_COMPANYFACTS", "sinif": "C_finansal", "ad": "SEC XBRL companyfacts API", "erisim": "data.sec.gov/api/xbrl/companyfacts/CIK##########.json (şirket başına 0,1-5 MB; saniyede < 10 istek)",
     "kapsam": "XBRL 2009-11+; KEŞİF çoğu şirket tam", "gecikme": "her değer 'filed' (bildirim) tarihinden sonra; 10-Q ~40-45 gün", "maliyet": "ücretsiz", "boyut": "3.260 şirket ~5 GB JSON (indirme sırasında özetlenir)",
     "eslesme": "CIK (yeniden yapılanmada CIK değişir: APO); IFRS'li yabancılar ayrı ad alanı", "olcer": "satış, FNA, net kâr, nakit, borç, hisse ihracı geliri, hisse sayısı", "olcemez": "bölünmeye göre düzeltilmiş hisse sayısı (düzeltme gerekir)", "projede": "secfs 2021q1+ özütü"},
    {"kimlik": "SEC_FS_DS", "sinif": "C_finansal", "ad": "SEC Financial Statement Data Sets", "erisim": "www.sec.gov/files/dera/data/financial-statement-data-sets/YYYYqN.zip", "kapsam": "2009q1 -> 2026; projede 2021q1+",
     "gecikme": "başvuru tarihi", "maliyet": "ücretsiz", "boyut": "eksik 2016-20: 20 çeyrek ~1,6 GB zip", "eslesme": "CIK, adsh", "olcer": "bütün XBRL kalemleri", "olcemez": "-", "projede": "islenmis-veri secfs 2021q1-2026q3"},
    {"kimlik": "SEC_SUBMISSIONS_OZET", "sinif": "D_kurumsal_olay", "ad": "SEC başvuru geçmişi özeti (form, tarih, 8-K madde kodu)", "erisim": "yerel: islenmis-veri k55/sec_ozet.json (K54'te data.sec.gov/submissions'tan)",
     "kapsam": "3.262 CIK, bütün başvurular 1990'lar -> 2026-10-30; KEŞİF tam", "gecikme": "başvuru tarihi (kabul günü)", "maliyet": "ücretsiz, indirme yok", "boyut": "105 MB (xz 6,6 MB)",
     "eslesme": "CIK = K55 evreninin %100'ü", "olcer": "8-K maddeleri (2.02 bilanço, 1.01, 1.03, 2.01, 3.01, 3.02, 5.03), S-1 / S-3 / 424B, SC 13D / 13G, SC TO, DEFM14A, 25-NSE, 15-12B, NT 10-K / Q",
     "olcemez": "ihracın hisse mi borç mu olduğu (424B2 banka notu), bölünme oranı", "projede": "VAR (K54)"},
    {"kimlik": "YAHOO_SPLITS", "sinif": "G_veri_hatasi", "ad": "Yahoo bölünme listesi (yfinance)", "erisim": "query1.finance.yahoo.com (yfinance; crumb / hız sınırı: bu ortamda 401 / 429 görüldü, ikinci denemede geçti)",
     "kapsam": "uzun geçmiş; batan sembollerde boş", "gecikme": "-", "maliyet": "ücretsiz (resmî olmayan API; kullanım koşulu belirsiz)", "boyut": "küçük", "eslesme": "sembol", "olcer": "bölünme tarihi / oranı -> XBRL hisse sayısı düzeltmesi, V_ABD denetimi",
     "olcemez": "batan / kodu değişen şirketler", "projede": "V_ABD (Yahoo, düzeltilmiş)"},
    {"kimlik": "TIINGO_BATAN", "sinif": "G_veri_hatasi", "ad": "Tiingo günlük fiyat (batanlar, splitFactor, divCash)", "erisim": "api.tiingo.com (anahtar .env TIINGO_TOKEN; ücretsiz hesap ayda 500 sembol)",
     "kapsam": "uzun geçmiş, batanlar dahil", "gecikme": "-", "maliyet": "ücretsiz hesap kota; ücretli plan sınırsız", "boyut": "sembol başına küçük", "eslesme": "sembol + Tiingo listesi (başlangıç / bitiş)",
     "olcer": "batan şirket fiyatları, bölünme katsayısı (ikinci sağlayıcı denetimi)", "olcemez": "-", "projede": "450 batan (repoya konmaz, lisans)"},
    {"kimlik": "SEC_MIDAS", "sinif": "E_islem", "ad": "SEC MIDAS 'Metrics by Individual Security and Exchange'", "erisim": "www.sec.gov/data-research/sec-markets-data/market-structure-data-security-exchange (çeyreklik zip, aylık CSV)",
     "kapsam": "2012q1 -> 2026q2; KEŞİF tam; günlük × hisse (ayrıca hisse × borsa); evren CRSP SHRCD 10/11 + ETP: REIT ve yabancı hisse YOK (IRM, EXR, BNS örneklemde yok)",
     "gecikme": "çeyrek sonrası yayın", "maliyet": "ücretsiz", "boyut": "hisse dosyası çeyrek ~15-22 MB -> KEŞİF ~0,4 GB (borsa kırılımlı ~2 GB)",
     "eslesme": "Ticker + Date (CIK yok; batanlarda o günkü sembol gerekir: TLGT değil TLGTQ değil)", "olcer": "işlem sayısı, tek lot altı, gizli emir, iptal, emir / işlem hacmi -> işlem büyüklüğü, gizli pay", "olcemez": "alıcı / satıcı tarafı, kurum kimliği, gün içi sıra (yalnız günlük toplam)", "projede": "yok"},
    {"kimlik": "FINRA_REGSHO", "sinif": "E_islem", "ad": "FINRA Reg SHO günlük açığa satış hacmi (borsa dışı)", "erisim": "cdn.finra.org/equity/regsho/daily/{CNMS|FNYX|FNSQ|FORF}shvolYYYYMMDD.txt",
     "kapsam": "tesis dosyaları (FNYX, FNSQ) 2009-08 -> bugün: KEŞİF tam; konsolide CNMS 2018-08 ->",
     "gecikme": "ertesi gün", "maliyet": "ücretsiz", "boyut": "gün ~0,3 MB", "eslesme": "sembol", "olcer": "günlük borsa dışı açığa satış hacmi payı (TRF / ADF / ORF)", "olcemez": "pozisyon; borsa içi açığa satış; piyasa yapıcı açığa satışını yönlü baskıdan ayırmaz", "projede": "yok (FINRA koşulu: ham veri dağıtılmaz)"},
    {"kimlik": "FINRA_SI", "sinif": "E_islem", "ad": "FINRA konsolide açığa satış pozisyonu (API)", "erisim": "POST api.finra.org/data/group/otcMarket/name/consolidatedShortInterest", "kapsam": "API'de ~2017-12 -> bugün (2017 boş): KEŞİF'in 2016-01..2017-11'i EKSİK",
     "gecikme": "ödeme gününden ~1 hafta sonra yayın (ayda iki kez)", "maliyet": "ücretsiz", "boyut": "küçük", "eslesme": "sembol", "olcer": "açığa satış pozisyonu, kapatma gün sayısı", "olcemez": "2017 öncesi (borsa dosyaları ücretli)", "projede": "K31: 2022-11 -> 2026-08 (Ç103)"},
    {"kimlik": "FINRA_ATS", "sinif": "E_islem", "ad": "FINRA OTC Transparency ATS / OTC haftalık hacim", "erisim": "POST api.finra.org/data/group/otcMarket/name/weeklySummary (genel API yalnız yakın geçmiş); tarihsel: otctransparency.finra.org",
     "kapsam": "genel API'de KEŞİF boş; tarihsel dosyalar 2014 (ATS) / 2016 (OTC) sonrası, elle", "gecikme": "2-4 hafta", "maliyet": "ücretsiz (kullanım koşulu)", "boyut": "orta", "eslesme": "sembol",
     "olcer": "karanlık havuz (ATS) payı", "olcemez": "taraf, fiyat", "projede": "yok"},
    {"kimlik": "SEC_FTD", "sinif": "E_islem", "ad": "SEC başarısız teslim (Fails-to-Deliver)", "erisim": "www.sec.gov/data-research/sec-markets-data/fails-deliver-data (yarım aylık zip)", "kapsam": "2004 -> 2026; KEŞİF tam",
     "gecikme": "yayın ~1 ay", "maliyet": "ücretsiz", "boyut": "yarım ay ~1 MB -> KEŞİF ~150 MB", "eslesme": "sembol + CUSIP", "olcer": "eşik üstü teslim edilemeyen bakiye (çıplak açığa satış / sıkışma izi)", "olcemez": "sıfır günler (yalnız eşik üstü)", "projede": "yok"},
    {"kimlik": "OHLC_SPREAD_VEKIL", "sinif": "E_islem", "ad": "Günlük OHLC'den spread tahmini (Corwin-Schultz 2012, Abdi-Ranaldo 2017)", "erisim": "yerel (V_ABD); K56/islem_davranisi", "kapsam": "fiyat serisi kadar",
     "gecikme": "-", "maliyet": "ücretsiz", "boyut": "-", "eslesme": "sembol", "olcer": "efektif spread VEKİLİ (likidite)", "olcemez": "gerçek kote / derinlik", "projede": "fiyat verisi var"},
    {"kimlik": "TAQ_ITCH_UCRETLI", "sinif": "E_islem", "ad": "Gün içi işlem / kote / emir defteri (NYSE TAQ, Nasdaq ITCH, Polygon, Databento)", "erisim": "ücretli (WRDS kurumsal abonelik; Polygon / Databento kullanım başına)",
     "kapsam": "uzun geçmiş", "gecikme": "-", "maliyet": "ücretli: Faz 0'da istek yok; fiyat kaynak araştırmasında", "boyut": "çok büyük (TB)", "eslesme": "sembol",
     "olcer": "işlem sırası, alıcı / satıcı başlatmalı akış (Lee-Ready), blok işlemler, derinlik", "olcemez": "kurum kimliği", "projede": "yok"},
    {"kimlik": "SEC_ASKIYA_ALMA", "sinif": "F_kasit_kaniti", "ad": "SEC işlem askıya alma bültenleri", "erisim": "www.sec.gov/enforcement-litigation/trading-suspensions (sayfalı tablo, 100 satır / sayfa)",
     "kapsam": "1995-10 -> 2026-10; 1.349 bülten (şirket satırı)", "gecikme": "askıya alma günü", "maliyet": "ücretsiz", "boyut": "~3 MB HTML", "eslesme": "SEMBOL YOK: şirket adı eşlemesi (normalize ad + eski adlar) -> evrende 10 şirket",
     "olcer": "resmî kasıt / yanıltma şüphesi kaydı", "olcemez": "yakalanmayan manipülasyon", "projede": "yok"},
    {"kimlik": "SEC_DAVA", "sinif": "F_kasit_kaniti", "ad": "SEC dava bültenleri (litigation releases) ve idari kararlar", "erisim": "www.sec.gov/enforcement-litigation/litigation-releases (sayfalı)", "kapsam": "uzun geçmiş",
     "gecikme": "olaydan yıllar sonra", "maliyet": "ücretsiz", "boyut": "küçük-orta (metin)", "eslesme": "kişi / şirket adı; sembol metinde", "olcer": "manipülasyon / pompala-boşalt davaları", "olcemez": "yakalanmayan", "projede": "yok"},
    {"kimlik": "SEC_13F_LISTE", "sinif": "A_kurumsal_sahiplik", "ad": "SEC 'Official List of Section 13(f) Securities' (CUSIP + ihraççı adı)", "erisim": "sec.gov 13(f) listeleri (çeyreklik; 2016-19 yalnız PDF)", "kapsam": "1996q1 -> 2026",
     "gecikme": "çeyrek başı", "maliyet": "ücretsiz (CUSIP lisans tartışması: repoya konmaz)", "boyut": "küçük", "eslesme": "CUSIP -> ihraççı adı (tarihli)", "olcer": "OpenFIGI'nin güncel sembol döndürmesi sorununa karşı tarihli ad", "olcemez": "sembol", "projede": "yok"},
    {"kimlik": "SEC_FORM144", "sinif": "B_iceriden", "ad": "Form 144 (satış niyeti bildirimi)", "erisim": "EDGAR", "kapsam": "elektronik zorunluluk 2023-04-13; öncesi çoğu kâğıt (2021'de ~30.000'in ~234'ü elektronik)", "gecikme": "satışla aynı gün",
     "maliyet": "ücretsiz", "boyut": "küçük", "eslesme": "CIK", "olcer": "planlanan içeriden satış", "olcemez": "KEŞİF dönemi (kâğıt)", "projede": "yok"},
    {"kimlik": "NASDAQ_HALT", "sinif": "F_kasit_kaniti", "ad": "Nasdaq işlem durdurma geçmişi", "erisim": "nasdaqtrader.com işlem durdurma arşivi (gün parametreli)", "kapsam": "2016 ve 2025 günleri denendi, veri var", "gecikme": "aynı gün",
     "maliyet": "ücretsiz (yeniden dağıtım koşulu doğrulanmadı)", "boyut": "küçük", "eslesme": "sembol", "olcer": "haber bekleniyor / düzenleyici durdurma (T1, T12, H10)", "olcemez": "kasıt (yalnız durdurma)", "projede": "yok"},
    {"kimlik": "DOJ_FINRA_AAER", "sinif": "F_kasit_kaniti", "ad": "DOJ basın bültenleri, FINRA disiplin kararları, SEC AAER", "erisim": "justice.gov / finra.org / sec.gov", "kapsam": "DOJ 2009+, FINRA 2005+, AAER 1982+",
     "gecikme": "olaydan yıllar sonra", "maliyet": "ücretsiz", "boyut": "metin", "eslesme": "ad (sembol metinde)", "olcer": "dava / yaptırım (kasıt kanıtı)", "olcemez": "yakalanmayan", "projede": "yok"},
    {"kimlik": "NYSE_SI_UCRETLI", "sinif": "E_islem", "ad": "NYSE / Compustat tarihsel açığa satış pozisyonu", "erisim": "NYSE veri ürünleri / WRDS Compustat", "kapsam": "NYSE 1988+, Compustat yarım aylık 2007+", "gecikme": "yarım ay",
     "maliyet": "ücretli (kurumsal lisans; fiyat yayımlanmıyor)", "boyut": "orta", "eslesme": "sembol / GVKEY", "olcer": "2016-17 açığa satış pozisyonu (FINRA API'de yok)", "olcemez": "-", "projede": "yok"},
    {"kimlik": "POLYGON_DATABENTO", "sinif": "E_islem", "ad": "Massive (Polygon) / Databento gün içi işlem verisi", "erisim": "ücretli API", "kapsam": "Polygon Advanced 20+ yıl; Databento Nasdaq ITCH 2018-05+",
     "gecikme": "-", "maliyet": "Polygon Starter 29 $/ay (5 yıl), Advanced 199 $/ay (bireysel kullanım); Databento kullanım bazlı (yeni hesaba kredi)", "boyut": "çok büyük", "eslesme": "sembol",
     "olcer": "işlem sırası, alış / satış başlatmalı akış, blok işlem", "olcemez": "kurum kimliği", "projede": "yok"},
    {"kimlik": "YEREL_K55_PANEL", "sinif": "yerel", "ad": "K55 ortak paneli + olay tablosu", "erisim": "K55 Faz 0 çıktısı (panel 725 MB; Drive OUTPUT/K55)", "kapsam": "2016-2026, 3.260 hisse",
     "gecikme": "-", "maliyet": "-", "boyut": "-", "eslesme": "-", "olcer": "M01 gecikme sınaması, M03 / M16 / M18 denetimleri", "olcemez": "-", "projede": "VAR"},
    {"kimlik": "YEREL_ANALIST", "sinif": "yerel", "ad": "Yahoo analist not günlüğü (K52)", "erisim": "K52 verisi", "kapsam": "K52 veri kapsamı raporu", "gecikme": "-", "maliyet": "-", "boyut": "-", "eslesme": "sembol",
     "olcer": "revizyon zamanlaması (M19)", "olcemez": "-", "projede": "VAR"},
    {"kimlik": "SENTETIK", "sinif": "yerel", "ad": "Bilgisiz yapay evren (K56/mekanizma)", "erisim": "kod", "kapsam": "-", "gecikme": "-", "maliyet": "-", "boyut": "-", "eslesme": "-", "olcer": "mekanik eser (M01, M03)", "olcemez": "-", "projede": "VAR"},
    {"kimlik": "K30_ALIM", "sinif": "B_iceriden", "ad": "K30 açık piyasa alımları özeti", "erisim": "islenmis-veri veri2/k30_alim", "kapsam": "K30 kapsamı", "gecikme": "-", "maliyet": "-", "boyut": "-", "eslesme": "sembol",
     "olcer": "P alımları", "olcemez": "satış / plan", "projede": "VAR"},
]


def veri_kaynaklari(Er: pd.DataFrame) -> pd.DataFrame:
    """Kaynak tablosu + erişim testinin özet durumu (kaynak başına: GECTI / KISMI / BASARISIZ sayısı ve ölçümler)."""
    T = pd.DataFrame(KAYNAKLAR)
    if len(Er) and "kaynak" in Er:
        g = Er.groupby("kaynak").apply(lambda x: "; ".join(f"{r.test}: {r.durum} ({r.olcu} = {r.deger})" for r in x.itertuples()), include_groups=False).rename("erisim_testi")
        d = Er.groupby("kaynak").durum.agg(lambda s: "BASARISIZ" if (s == "BASARISIZ").all() else ("GECTI" if (s == "GECTI").all() else "KISMI")).rename("erisim_durumu")
        T = T.merge(g, left_on="kimlik", right_index=True, how="left").merge(d, left_on="kimlik", right_index=True, how="left")
    else:
        T["erisim_testi"] = ""; T["erisim_durumu"] = "TEST EDİLMEDİ"
    T["erisim_durumu"] = T.erisim_durumu.fillna(np.where(T.sinif == "yerel", "YEREL", "TEST EDİLMEDİ"))
    return T


def hipotez_veri(H: pd.DataFrame, VK: pd.DataFrame) -> pd.DataFrame:
    """(4) Her hipotez için gerekli kaynak: kapsam, maliyet, erişim durumu; KEŞİF kapsamı eksikse işaret."""
    rows = []; vk = VK.set_index("kimlik")
    for h in H.itertuples():
        for k in [x.strip() for x in str(h.veri).split(";") if x.strip()]:
            v = vk.loc[k] if k in vk.index else None
            rows.append({"hipotez": h.kimlik, "hipotez_ad": h.ad, "kaynak": k, "kaynak_ad": v["ad"] if v is not None else "TANIMSIZ", "kapsam": v["kapsam"] if v is not None else "",
                         "maliyet": v["maliyet"] if v is not None else "", "boyut": v["boyut"] if v is not None else "", "erisim_durumu": v["erisim_durumu"] if v is not None else "TANIMSIZ",
                         "kesif_eksik": bool(v is not None and "EKSİK" in str(v["kapsam"]).upper()) or bool(v is not None and "boş" in str(v["kapsam"]))})
    return pd.DataFrame(rows)


def riskler() -> pd.DataFrame:
    R = [
        ("Olay tanımı seçim etkisi (M01)", "K55'in olay-öncesi (A) karşılaştırmaları bilgisiz veride de aynı farkı üretiyor; olay tanımlı her mekanizma testi aynı esere açık",
         "yüksek", "mekanizma testlerinde olay günü değil sinyal günü sabit tasarım (ileri ölçü) ya da t0−k gecikmeli ölçüm; her testte sentetik sıfır koşusu"),
        ("Keşif verisinin yeniden kullanımı", "K56 hipotezleri K55 KEŞİF 2016-21 sonuçlarından üretildi; aynı dönemde doğrulama döngüseldir", "yüksek",
         "DOĞRULANMIŞ sınıfı için İÇ / BAĞIMSIZ dönem gerekir (Cemal kararı); yeniden kullanım kaydı (K56_KAYNAK_KAYDI)"),
        ("Açığa satış verisi KEŞİF'i kapsamıyor", "FINRA SI API ~2017-12+, Reg SHO CDN 2018-08+", "orta", "M05 yalnız 2018-21 alt döneminde; ya da ücretli borsa dosyaları"),
        ("13F eşleme ve gecikme", "CUSIP -> sembol (OpenFIGI hız sınırı, fon / tahvil CUSIP'leri), 45 gün gecikme, yalnız 100 mn $ üstü yöneticiler, çeyrek sonu anlık görüntü", "orta",
         "OpenFIGI ücretsiz anahtar + yerel önbellek; Common Stock / US süzgeci; başvuru tarihi point-in-time"),
        ("CIK değişimi", "yeniden yapılanmada yeni CIK (APO 2022): companyfacts / Form 4 eski dönemi kaçırır", "orta", "SEC eski ad / CIK zinciri (formerNames, 8-K 2.01 / 425) ile CIK geçmişi kurulmalı"),
        ("Yabancı özel ihraççılar", "20-F / 40-F (BNS): Form 4 yok, IFRS kalemleri", "düşük-orta", "ayrı alt grup; ifrs-full eşlemesi ya da dışlama (önceden yazılı)"),
        ("XBRL hisse sayısı bölünmeye göre düzeltilmemiş", "TRMB +%104, TLGTQ +16 kat görünen 'sulandırma' bölünme / ters bölünme", "yüksek (M06 için)", "bölünme verisiyle düzeltme (Yahoo / Tiingo splitFactor) ve 8-K 5.03 denetimi"),
        ("İhraç formu hisse / borç ayırmıyor", "424B2 çoğunlukla banka notu (BNS 10.925 başvuru)", "orta", "424B2 / 424B3 ayrı; hisse sayısı artışıyla doğrulama"),
        ("10b5-1 planı 2023 öncesi görünmez", "plansız satış ayrımı yalnız dipnot metninden (%2,7)", "orta", "dipnot metin araması + 2023 sonrası işaretle duyarlılık"),
        ("Hayatta kalma yanlılığı", "evren 266 çıkış / 3.267; batanlar eksik (K54)", "orta", "Tiingo kotasıyla batan evren genişletme (Cemal kararı)"),
        ("Kasıt kanıtı kapsamı", "askıya alma listesi sembolsüz (ad eşlemesi hatalı olabilir), yalnız yakalananlar, yıllar sonra", "yüksek (M14)", "yalnız sembol + tarih doğrulanmış kayıt kanıt; kayıt yoksa 'KASIT KANITI YOK'"),
        ("Gün içi veri yok", "dağıtım / emilim işlem sırası düzeyinde ayrılamaz; MIDAS yalnız günlük toplam", "yüksek (M09 / M11)", "MIDAS + 13F + FINRA ATS üçlemesi; ücretli TAQ yalnız Cemal kararıyla"),
        ("İndirme hacmi ve süre", "13F ~1,1 GB, MIDAS ~2 GB, FS 2016-20 ~1,6 GB, Form 4 ~0,25 GB, companyfacts ~5 GB", "orta", "Drive önbelleği, sürümlü özet (islenmis-veri), bir kez indir"),
        ("Yahoo erişim kararsızlığı", "yfinance crumb 401 / 429 (bu ortamda bir kez)", "düşük", "Tiingo splitFactor ile çapraz"),
        ("Çoklu test", "19 hipotez × gruplar × dönemler", "orta", "aile = hipotez × dönem; BH q 0,10; önceden yazılı birincil ölçü"),
        ("Lisans", "Tiingo fiyatları repoya konmaz; SEC / FINRA ham verileri büyük", "düşük", "yalnız türetilmiş özet + manifest sha"),
    ]
    return pd.DataFrame(R, columns=["risk", "ayrinti", "etki", "onlem"])


def uygulama_sirasi() -> pd.DataFrame:
    S = [
        (1, "M01 gerçek veri gecikme sınaması", "K55 paneli: 25 KEŞİF hücresi t0−1 / 5 / 20'de; olay tanımı seçimsiz biçimde (sinyal günü sabit, ileri getiri üst %5) yeniden", "yerel, indirme yok, ~15 dk",
         "hayır (KEŞİF yeniden kullanımı kayıtlı)", "MEKANİK AÇIKLAR kesinleşirse K55'in 25 KEŞİF'i YANLIŞ BULGU; K55 tabanlı mekanizma araştırması gereksizleşir"),
        (2, "M03 / M16 / M18 yerel denetimler", "ince oynaklık + GARCH, 2020 dışlama + beta, sektör × gün: 1. adımda kalan hücreler için", "yerel, ~15 dk", "hayır", "kalan etkinin oynaklık / piyasa / tema bileşeni"),
        (3, "M04 / M15 haber ve birleşme bileşimi", "yerel SEC başvuru özetiyle G1 / G2 / G7'de [t0−5, t0+60] 8-K maddeleri, SC TO, DEFM14A", "yerel, ~10 dk", "hayır",
         "büyük yükselişlerin ne kadarının ayrık habere bağlı olduğu (mekanizmanın kendisi)"),
        (4, "M13 / M17 evren ve sağlayıcı (K51 P1)", "K51 P1 artısının yalnız V_ABD'de olması: sağlayıcı × etki; batan evren genişletme", "yerel + Tiingo kotası (Kasım)", "EVET (Tiingo kotası)", "K51 küçük artısının hayatta kalma eseri olup olmadığı"),
        (5, "M09 / M10 Form 4 (yalnız 1-3'ten sonra kalan açıklanmamış etki varsa)", "Insider DS KEŞİF ~250 MB; plansız S, P", "indirme ~250 MB, ~30 dk", "hayır (SEC izni var)", "dağıtım / içeriden bilgi"),
        (6, "M08 / M11 13F + OpenFIGI (yalnız kalan etki varsa)", "13F KEŞİF ~1,1 GB, CUSIP eşleme", "indirme ~1,1 GB + eşleme ~1-2 saat", "EVET (Drive alanı / süre)", "kurumsal birikim / emilim"),
        (7, "M02 / M11 / M12 MIDAS (yalnız kalan etki varsa)", "MIDAS KEŞİF ~2 GB; işlem büyüklüğü, gizli / tek lot altı pay", "indirme ~2 GB", "EVET", "likidite / emilim"),
        (8, "M05 açığa satış (2018-21 alt dönemi)", "FINRA SI + Reg SHO + FTD", "küçük-orta indirme", "hayır", "sıkışma; KEŞİF'in yalnız bir kısmı"),
        (9, "M14 resmî kayıt eşlemesi", "askıya alma (1.349) + dava bültenleri, ad + CIK eşleme, sembol / tarih doğrulama", "küçük", "hayır", "kasıt yalnız resmî kayıtla"),
        (10, "Doğrulama dönemi", "kalan her GÜÇLÜ AÇIKLAMA için İÇ 2022-23 (ve BAĞIMSIZ 2024-26)", "-", "EVET (dönem açma)", "DOĞRULANMIŞ MEKANİZMA sınıfı için zorunlu"),
    ]
    return pd.DataFrame(S, columns=["sira", "adim", "icerik", "maliyet_sure", "karar_gerekir", "ne_kazanilir"])


def _md(T: pd.DataFrame, kol: List[str], n: int = 0) -> List[str]:
    kol = [c for c in kol if c in T.columns]
    if not len(T) or not kol:
        return ["(boş)"]
    X = T[kol] if not n else T[kol].head(n)
    def h(v):
        if isinstance(v, float):
            return "" if np.isnan(v) else f"{v:.3f}"
        return str(v).replace("|", "/").replace("\n", " ")[:220]
    return ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)] + ["| " + " | ".join(h(v) for v in r) + " |" for r in X.itertuples(index=False)]


def faz0_yaz(cikti: str, kimlik: Dict[str, Any], E: pd.DataFrame, Den: pd.DataFrame, Ac: pd.DataFrame, H: pd.DataFrame, HV: pd.DataFrame, VK: pd.DataFrame,
             Er: pd.DataFrame, Z: Any, R: pd.DataFrame, Sira: pd.DataFrame) -> str:
    L = [f"# K56 — K51-K55 ETKİ VE MEKANİZMA ARAŞTIRMASI: FAZ 0 RAPORU ({kimlik['kimlik']})", "",
         f"- Kod {kimlik['surum']}; commit {kimlik['commit']}; kilit sha {kimlik['onkayit_sha'][:12]}. K51-K55 dosyaları yalnız okundu (K56_KAYNAK_KAYDI.csv: dosya, sha256, amaç).",
         "- Faz 0: envanter, hipotezler, veri kaynakları, küçük örneklem erişim testi ve M01 sentetik yöntem sınaması. Bütün evrene mekanizma testi YOK; büyük indirme YOK.",
         "- Sınıflar ön sınıftır (Faz 0); kesin sınıf Faz 1 testleriyle (ONKAYIT_K56 3). K51 İZ DEĞİL ve K55 İZ YOK kararları değişmedi.", ""]
    # özet
    L += ["## 0. Özet", ""]
    if Z is not None and len(Z):
        k = Z[Z.durum_k55 == "KEŞİF"]; mk = int((k.karar == "MEKANIK_ACIKLAR").sum())
        L += [f"- **M01 seçim etkisi**: bilgisiz yapay veride (4 evren × 400 hisse) K55'in olay tanımı ve aynı kod, 25 KEŞİF hücresinin {mk}'inde gerçek etkinin en az yarısını "
              f"aynı işaretle üretiyor (çoğunda tamamını: oran medyanı {k.oran_Y60.median():.2f}); {int((k.karar == 'BELIRSIZ').sum())} hücre BELİRSİZ (yalnız GARCH'lı evrende mekanik), "
              f"MEKANİK İZ YOK {int((k.karar == 'MEKANIK_IZ_YOK').sum())}. Yön uyumlu 5 hücre dahil. Etki t0−5'te üçte birine, t0−20'de sıfıra iniyor (mekanik imza).",
              "- Anlamı: K55'in 19 ters yönlü KEŞİF'i bir piyasa davranışı değil, olay tanımının (t0 = ileri pencerenin +%30'u ilk yakaladığı gün, giriş t0+1) eseri olmaya ADAY. "
              "Kesinleşmesi için gerçek veride gecikme sınaması gerekir (uygulama sırası 1; yerel, indirme yok)."]
    L += [f"- Envanter: {len(E)} bulgu ({', '.join(f'{k} {v}' for k, v in E.kaynak_calisma.value_counts().sort_index().items())}); ön sınıf: "
          + ", ".join(f"{k} {v}" for k, v in E.faz0_on_sinif.value_counts().items()) + ".",
          f"- Mekanik denetim: {len(Den)} uyuşmazlık / eksik (K56_ENVANTER_DENETIMI.csv; sessiz düzeltme yok).",
          f"- Erişim testi: {', '.join(f'{k} {v}' for k, v in Er.durum.value_counts().items()) if len(Er) else 'koşulmadı'}.", ""]
    # 1
    L += ["## 1. K51-K55 etki envanteri", "", "Tam tablo (18 alan + ön sınıf + hipotezler): K56_ETKI_ENVANTERI.csv. Çalışma × ön sınıf:", ""]
    L += _md(pd.crosstab(E.kaynak_calisma, E.faz0_on_sinif).reset_index(), list(pd.crosstab(E.kaynak_calisma, E.faz0_on_sinif).reset_index().columns))
    L += ["", "Bütün bulgular (kısa):", ""] + _md(E, ["kimlik", "ad", "sinif", "yon", "buyukluk", "faz0_on_sinif", "mekanizma_hipotezleri"])
    # 2
    L += ["", "## 2. Açıklanmamış bulgular", "", "Etkisi olan her bulgu; hiçbiri 'açıklandı' sayılmadı. ADAY AÇIKLAMA = Faz 1 doğrulaması bekleyen (M01 eseri / vekil).", ""]
    L += _md(Ac.groupby(["faz0_durum", "kaynak_calisma"]).size().rename("n").reset_index(), ["faz0_durum", "kaynak_calisma", "n"]) + [""]
    L += _md(Ac[Ac.faz0_durum == "AÇIKLANMADI"], ["kimlik", "ad", "sinif", "buyukluk", "faz0_gerekce", "mekanizma_hipotezleri"])
    # 3
    L += ["", "## 3. Mekanizma hipotezleri", "", "Önceden yazılı tahmin ve çürütme ölçütü; tam metin K56_HIPOTEZLER.csv. Her bulgu için en az üç yarışan açıklama envanterde (olasi_aciklamalar).", ""]
    L += _md(H, ["kimlik", "ad", "tur", "dogruysa", "yanlissa", "curutme", "oncelik", "faz0"])
    # 4
    L += ["", "## 4. Hipotez başına gerekli veri", ""] + _md(HV, ["hipotez", "kaynak", "kapsam", "maliyet", "erisim_durumu", "kesif_eksik"])
    # 5
    L += ["", "## 5. Veri kaynakları: kapsam, gecikme, maliyet (erişim testiyle)", ""] + _md(VK, ["kimlik", "ad", "kapsam", "gecikme", "maliyet", "boyut", "eslesme", "erisim_durumu", "projede"])
    if len(Er):
        L += ["", "Erişim testi ayrıntısı (K56_VERI_ERISIM_TESTI.csv; örneklem K56_ERISIM_ORNEKLEM.csv; istek günlüğü K56_ISTEK_GUNLUGU.csv):", ""]
        L += _md(Er, ["modul", "kaynak", "test", "durum", "olcu", "deger", "ayrinti"])
    # 6
    L += ["", "## 6. Doğrulama ve çürütme yöntemleri", "",
          "- Karşıt örnekler (her mekanizma): G1 olay, G2 aynı belirti yükseliş yok, G3 iflas, G4 büyük düşüş, G5 hisse sayısı > %20 artan, G6 birleşme, G7 sektör × likidite eşli rastgele; "
          "yanlış pozitif oranı = P(yükseliş yok | mekanizma var), kesinlik, etki ve ay kümeli %95 aralık.",
          "- Aracılık (mediation): mekanizma değişkeni denetlenince asıl etkinin küçülme payı (bootstrap aralığı); >= %50 DOĞRULANMIŞ / GÜÇLÜ için şart.",
          "- Sentetik sıfır sınaması: bilgisiz yapay evrende aynı tanım ve aynı kod (M01, M03); gerçek etkinin >= %50'sini üreten bulgu YANLIŞ BULGU adayı.",
          "- Gecikme sınaması: ölçü t0−k'da; mekanik eser k ile söner, gerçek birikim sönmez.",
          "- Sağlayıcı / evren duyarlılığı: V_ABD / K34 Yahoo / Tiingo ayrı; batan evren genişletme (M13, M17).",
          "- Point-in-time: bütün SEC / FINRA verisi bildirim / yayın tarihinden sonra kullanılır (13F 45 gün, Form 4 ~2 gün, 10-Q ~40 gün).",
          "- Kasıt: üç sütun (gözlenen davranış / olası mekanizma / kasıt kanıtı); kanıt yalnız sembol + tarih doğrulanmış resmî kayıt.", ""]
    if Z is not None and len(Z):
        L += ["M01 sentetik sınama (K56_SECIM_SENTETIK_OZET.csv; satırlar K56_SECIM_SENTETIK.csv):", ""]
        L += _md(Z.sort_values(["durum_k55", "hucre"]), ["hucre", "durum_k55", "varyant", "d_gercek_Y60", "d_sent_Y60", "oran_Y60", "karar", "d_sent_gecikme1", "d_sent_gecikme5", "d_sent_gecikme20"])
        L += ["", "Karar × K55 durumu:", ""] + _md(pd.crosstab(Z.durum_k55, Z.karar).reset_index(), list(pd.crosstab(Z.durum_k55, Z.karar).reset_index().columns))
    # 7
    L += ["", "## 7. Veri eksiklikleri ve teknik riskler", ""] + _md(R, ["risk", "ayrinti", "etki", "onlem"])
    # 8
    L += ["", "## 8. Önerilen uygulama sırası", "", "İlk üç adım yerel ve indirmesizdir; büyük indirmeler (5-7) yalnız 1-3'ten sonra AÇIKLANMAMIŞ etki kalırsa anlamlıdır.", ""]
    L += _md(Sira, ["sira", "adim", "icerik", "maliyet_sure", "karar_gerekir", "ne_kazanilir"])
    if len(Den):
        L += ["", "## Ek: envanter denetimi uyuşmazlıkları", ""] + _md(Den, ["tur", "kimlik", "kaynak", "ayrinti"])
    yol = os.path.join(cikti, "K56_FAZ0_RAPOR.md"); open(yol, "w", encoding="utf-8").write("\n".join(L) + "\n"); return yol
