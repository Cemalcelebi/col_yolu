"""FITIL_KOR — fitil öbeği: hata nerede? Üç halka (Cemal, 16 Kasım 2026: 'kesin bir tanı; kod ya tam şeklimi almadı, ya algılamadı, ya
yanlış doğruladı; nerede hata yaptığını ölçmeliyiz'). Tek dosya; Ç187 (FITIL_OBEK.py) tanımını, S6_TABAN v1.1 tabanını ve ORTAK_CETVEL'i
yalnız İMPORT eder (değiştirmez).

  HALKA 1 (tanım bağlamı): S+ / S- günleri S6 TABAN İÇİ (açık bölge, sınıf DİP) / TABAN DIŞI ayrılır; taban içi S+ (a) eşlere (cetvel r60) ve
          (b) taban içi S+ OLMAYAN günlere (aynı bölge ailesi; kontrol K1) karşı ölçülür. Varyantlar (gevşek / sıkı / küçük mum) bilgi.
  HALKA 3 (doğrulama ölçüsü): r20 eşli fark (cetvel mekaniği, ufuk 20) ve 'önce ne oldu' (60 geçerli bar içinde önce S6 tavanının kapanışla
          üstü = YUKARI / önce dip x 0,98 kapanış altı = AŞAĞI / hiçbiri); S+ vs taban içi S+ olmayan; fark ve ay kümeli bootstrap %95.
  HALKA 2 (algılama): kör set PDF (30 S+ [15 taban içi, 15 dışı] + 10 S-; BIST + ABD; adsız, tarihsiz, sonrası yok), anahtar ayrı json;
          PAPIL / DGXX adlı kalibrasyon sayfaları (kodun fitil payları ve bayrakları); Cemal'in yanıtı gelince `olc --cevap`.

İş tanımı: arastirma_cikti/fitil_obek/HALKA_IS_TANIMI.md (koşudan önce git'e işlendi).
Komut:  python FITIL_KOR.py onkayit [--veri K] [--uzerine-yaz]   KOR_SET_ON_KAYIT.md (mühür, sayım GETİRİSİZ, kontrol listesi)
        python FITIL_KOR.py kos [--veri K] [--gitsiz]            HALKA 1 + HALKA 3 -> halka_sonuc.json (kapılar: ik_kontrol_kapisi, oc_kapi, mühür)
        python FITIL_KOR.py kor [--veri K] [--gitsiz]            HALKA 2: FITIL_KOR_SET.pdf + kor_anahtar.json (+ PAPIL / DGXX kalibrasyon)
        python FITIL_KOR.py rapor [--ek DOSYA]                   halka_sonuc.json -> HALKA_RAPOR.md
        python FITIL_KOR.py olc --cevap "1:E,2:H,3:B,..."        Cemal'in kör set yanıtı -> uyum (E payı S+ vs S-, taban içi / dışı)
Colab:  exec(open('FITIL_KOR.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Komisyon / kayma yok. Evren bugün işlem gören hisseler: hayatta kalma yanlılığı (getiriler yukarı yanlı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_FK = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
import zlib  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_FK = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_FK not in sys.path:
    sys.path.insert(0, KOK_FK)

import ORTAK_CETVEL as OC  # noqa: E402
import FITIL_OBEK as FO  # noqa: E402
import S6_TABAN as S6  # noqa: E402

fklog = logging.getLogger("col.fitil_kor")
if not fklog.handlers:
    _fk_h = logging.StreamHandler(sys.stderr)
    _fk_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s fitil_kor: %(message)s", "%H:%M:%S"))
    fklog.addHandler(_fk_h)
    fklog.setLevel(logging.INFO)
    fklog.propagate = False

FK_SURUM = "FITIL_KOR v1.0 (2026-11-16): fitil öbeği üç halka (tanım bağlamı / doğrulama ölçüsü / algılama kör seti)"
FK_YOL = {"cikti": os.path.join(KOK_FK, "arastirma_cikti", "fitil_obek"), "kod": os.path.join(KOK_FK, "FITIL_KOR.py"),
          "is_tanimi": os.path.join(KOK_FK, "arastirma_cikti", "fitil_obek", "HALKA_IS_TANIMI.md"),
          "veri": os.environ.get("OC_VERI", "/tmp/veri"), "satir": os.environ.get("FK_SATIR", "/tmp/fitil_kor")}
FK_DOSYA = {"onkayit": "KOR_SET_ON_KAYIT.md", "sonuc": "halka_sonuc.json", "rapor": "HALKA_RAPOR.md", "pdf": "FITIL_KOR_SET.pdf",
            "anahtar": "kor_anahtar.json"}

# ================================================================ MÜHÜRLÜ TANIM (sonuç görüldükten sonra DEĞİŞMEZ)
FK_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "fitil": "Ç187 FITIL_OBEK.FO_ESIK aynen (fo_bar / fo_pencere / fo_kural; k = 10): S+ = ASIM >= 0,20 VE ALTYOK >= 0,50; S- = ASIM <= -0,20 "
             "VE USTYOK >= 0,50; KUCUK = pencere medyanı R/C <= 0,75 x ATR%250",
    "s6": "S6_TABAN.s6_taban, v1.1 varsayılanları (S6_PRM; parametre verilmez); girdi oc_veri temiz barları (geçerli bar, kriz kesiği)",
    "ic": "TABAN İÇİ (t, as-of t): S6 ölçülür bar (i >= 250) VE bolge_id >= 0 VE durum YENI / SURER / YENIDEN (bölge t'de açık; AL / KIRILDI "
          "günü bölge biter, sayılmaz) VE bölgenin sınıfı (bölgenin ilk barı = onay günündeki 'sinif') DIP",
    "dis": "TABAN DIŞI (t): S6 ölçülür bar VE TABAN İÇİ değil (bölge yok, bölge YOL / ORTA sınıfı, AL / KIRILDI günü)",
    "olculur": "bütün satırlar S6 ölçülür barlarda (ilk 250 geçerli bar dışarıda); ABD evren_bas öncesi atılır",
    "varyant": {"SPg": {"asim_min": 0.10, "altyok_min": 0.40}, "SPs": {"asim_min": 0.30, "altyok_min": 0.60}, "SPk": "S+ k=10 VE KUCUK",
                "duz": {"esik": 1.0, "esik_bilgi": [0.7, 1.5], "konum_gun": 120, "konum_max": 0.25,
                        "tanim": "EK TANIM (Cemal 16 Kas sözlü, ön kayıttan önce): DÜZ DİP = son 10 geçerli bar (t dahil) Low yayılımı "
                                 "(max L - min L) / medyan(H - L) <= 1,0 (0,7 ve 1,5 bilgi); DİP BAĞLAMI = TABAN İÇİ YA DA konum120 = "
                                 "(C - min C) / (max C - min C) son 120 geçerli kapanış <= 0,25; S+DÜZ = S+ (k=10) VE DÜZ DİP VE DİP BAĞLAMI; "
                                 "K_DUZ = DÜZ DİP VE DİP BAĞLAMI VE S+ değil (düz dip tek başına mı iş yapıyor)"}},
    "satirlar": {
        "SP_ic": "S+ TABAN İÇİ [HALKA 1 ANA]", "SM_ic": "S- TABAN İÇİ [HALKA 1 ANA, ayna]",
        "SP_dis": "S+ TABAN DIŞI [bilgi]", "SM_dis": "S- TABAN DIŞI [bilgi]",
        "SP_tum": "S+ bütün ölçülür günler (Ç187 SP_k10, S6 ölçülür süzgeciyle) [bilgi / HALKA 3 genel]",
        "SM_tum": "S- bütün ölçülür günler [bilgi / HALKA 3 genel]",
        "K_SP": "TABAN İÇİ ve S+ OLMAYAN günler [HALKA 1 (b) kontrol; HALKA 3 kontrol]",
        "K_SM": "TABAN İÇİ ve S- OLMAYAN günler [S- kontrol]",
        "K_SP_r": "K_SP'den her bölgede tek RASTGELE gün (tohum 187; bölge içi konum dengesi) [bilgi kontrol]",
        "K_SM_r": "K_SM'den her bölgede tek RASTGELE gün (tohum 187) [bilgi kontrol]",
        "SPg_ic": "S+ gevşek (ASIM >= 0,10, ALTYOK >= 0,40) TABAN İÇİ [bilgi]",
        "SPs_ic": "S+ sıkı (ASIM >= 0,30, ALTYOK >= 0,60) TABAN İÇİ [bilgi]",
        "SPk_ic": "S+ VE küçük mum (KUCUK) TABAN İÇİ [bilgi]",
        "SPD": "S+DÜZ (S+ VE düz dip <= 1,0 VE dip bağlamı) [EK; bilgi + ayrı satır]",
        "SPD07": "S+DÜZ eşik 0,7 [bilgi]", "SPD15": "S+DÜZ eşik 1,5 [bilgi]",
        "K_DUZ": "düz dip (<= 1,0) VE dip bağlamı VE S+ değil [S+DÜZ kontrolü]",
        "SPDb": "S+ VE düz dip (<= 1,0), dip bağlamı ŞARTSIZ [bilgi; kalibrasyonda TEHOL May 2025 / BINBN dip bağlamını geçmedi (konum120 > 0,25, "
                "taban yok), getiri görülmeden eklendi]",
        "K_DUZb": "düz dip (<= 1,0) VE S+ değil, bağlam şartsız [SPDb kontrolü]"},
    "r60_satir": ["SP_ic", "SM_ic", "SP_dis", "SM_dis", "SP_tum", "SM_tum", "K_SP", "K_SM", "K_SP_r", "K_SM_r", "SPg_ic", "SPs_ic", "SPk_ic",
                  "SPD", "SPD07", "SPD15", "K_DUZ", "SPDb", "K_DUZb"],
    "r20_satir": ["SP_ic", "SP_tum", "K_SP", "SM_ic", "SM_tum", "K_SM", "SPD", "K_DUZ"],
    "kontrol_tohum": 187,
    "olay": "durum günleri ORTAK_CETVEL.oc_olc'a verilir (giriş t'den sonraki ilk geçerli açılış; aynı hissede 60 gün tekilleştirme: ilk gün)",
    "fark_bootstrap": {"n": 2000, "tohum": 27, "kume": "giriş ayı",
                       "tanim": "iki grup (A olay, B kontrol) AYRI ay kümeli yeniden örnekleme (her grupta kendi ayları, yerine koyarak); "
                                "fark = ort(A) - ort(B); %95 = 2,5 / 97,5 yüzdelik"},
    "h1_karar": {
        "a": "taban içi S+ vs eşler: FITIL_OBEK.fo_etiket (Ç187 kuralı aynen; karar hücreleri ABD / AVR x 2023 / 2024-26, BIST bilgi); S- ayna",
        "b": "taban içi S+ vs K_SP (eşli farkların farkı): hücre AYRIŞIR = iki grup n >= 30, fark > 0 VE %95 alt uç > 0; AYRIŞMAZ = n >= 30 "
             "ve şart tutmadı; n < 30 ÖLÇÜLEMEDİ. S- ayna: fark < 0 VE üst uç < 0. Genel: dört karar hücresi AYRIŞIR -> 'KONTROLDEN AYRIŞIR'; "
             "en az biri -> 'KISMİ (hücreler)'; hiçbiri -> 'AYRIŞMAZ'",
        "varyant": "SPg_ic / SPs_ic / SPk_ic: (a) ile aynı etiket, BİLGİ (çoklu: 3 varyant; karar değildir)"},
    "h3": {
        "r20": "OC_ESIK kopyası, yalnız olcu.ufuk = 20: r20 = giriş + 19 birleşik takvim günü kapanışı / giriş açılışı - 1; eşler, havuz, "
               "tekilleştirme aynı; slot tutma 29 gün. Hücre: ortalama eşli fark, %95, sıra, oc_hucre 'tutar' (5 şart) BİLGİ (güç tablosu "
               "r60 için yazıldı; r20'de 'TUTMADI' etiketi kullanılmaz). r20 fark (b): SP_ic - K_SP, SM_ic - K_SM, aynı bootstrap",
        "kirilim": {"ufuk": 60, "asagi_carpan": 0.98,
                    "tanim": "TABAN İÇİ olay (cetvel tekil olayları, r60 koşusunun olay satırları): t'deki bölge kutusu (kutu_ust = tavan, "
                             "kutu_alt = dip; as-of t). t'den sonraki 60 geçerli bar (hissenin kendi barları; t+1 .. t+60) kapanışları: ilk "
                             "C > tavan barı -> YUKARI; ilk C < dip x 0,98 barı -> AŞAĞI; hangisi önce; ikisi de yoksa YOK. 60 bar kriz "
                             "kesiğinden (31.08.2026) ya da hissenin son barından önce dolmuyorsa olay ÖLÇÜLMEZ. Dönem = cetvel dönemi (giriş)"},
        "kirilim_karar": "S+: YUKARI oranı(SP_ic) - YUKARI oranı(K_SP); hücre AYRIŞIR = iki grup n >= 30, fark > 0 VE %95 alt uç > 0. "
                         "S- ayna: AŞAĞI oranı(SM_ic) - AŞAĞI oranı(K_SM) > 0 VE alt uç > 0. Genel etiket h1_karar.b ile aynı biçim",
        "kirilim10": "EK (S+DÜZ): aynı kural, kutu = t'de biten 10 geçerli barın max High / min Low (taban dışında da tanımlı); S+DÜZ vs K_SP "
                     "ve vs K_DUZ (düz dip tek başına), SP_ic vs K_SP bilgi; karar biçimi kirilim_karar ile aynı, BİLGİ",
        "genel": "TABAN DIŞI / genel S+ için tavan / dip yok -> kırılım UYGULANMAZ; genel için cetvelin 'once20' (60 gün +%20 önce -%10) olay "
                 "oranı vs eş oranı BİLGİ"},
    "tani": "HALKA tanısı (önceden yazılı okuma): (1) taban içi S+ (a) ya da (b) karar hücrelerinde TUTAR / AYRIŞIR ise ve Ç187 genel S+ "
            "tutmadıysa -> hata HALKA 1'de (bağlam); (2) r20 ya da kırılım AYRIŞIR, r60 ayrışmazsa -> hata HALKA 3'te (ölçü); (3) ikisi de "
            "hayırsa -> tanım bağlamı ve ölçü değişikliği sonucu değiştirmiyor; kalan HALKA 2 (algılama), kör setle Cemal'in gözüyle sınanır. "
            "Beklenti (Cemal): taban içi S+ eşlerden ve kontrolden iyi; YUKARI oranı S+'ta yüksek; S- ayna. EK: S+DÜZ (düz dip + dip "
            "bağlamı) için beklenti: 10 mum kutusunda YUKARI oranı K_SP ve K_DUZ'dan yüksek, r60 eşli fark > 0 (bilgi)",
    "kor": {"tohum": 1116, "pazar": ["BIST", "ABD"], "bas": "2016-01-01", "son": "2026-08-31", "pencere": 10, "once": 40,
            "grup": {"SP_ic": {"ABD": 8, "BIST": 7}, "SP_dis": {"ABD": 7, "BIST": 8}, "SM": {"ABD": 5, "BIST": 5}, "SPD": {"ABD": 5, "BIST": 5}},
            "ek": "EK (Cemal 16 Kas, ön kayıttan önce): S+DÜZ havuzundan 10 ek sayfa (ABD 5, BIST 5), toplam 50; SPD grubu seçimde en sonda; "
                  "olc kararı ilk 30 S+ vs 10 S- ile; SPD E payı bilgi",
            "secim": "havuz = o grubun durum günleri (SP_ic: S+ ve TABAN İÇİ; SP_dis: S+ ve TABAN DIŞI; SM: S- bütün ölçülür günler), t en az 50 "
                     "geçerli barın sonu; gün düzeyinde eşit olasılıklı rastgele (tohum 1116, grup ve pazar sırası: SP_ic ABD, SP_ic BIST, "
                     "SP_dis ABD, SP_dis BIST, SM ABD, SM BIST); aynı hisse sette bir kez; 50 sayfa (EK S+DÜZ 10 dahil) karıştırılır (aynı tohum)",
            "sayfa": "bir sayfa = pencere (son 10 mum, gri zemin) + öncesi 40 mum; SONRASI YOK; hisse adı / tarih / pazar / fiyat rakamı yok; "
                     "fiyat ekseni oransal (pencereden önceki son kapanış = 0 %); hacim altta; numara 'No k'",
            "cevap": "E = benim mumum, H = değil, B = belirsiz",
            "karar": "olc: E payı (B hariç payda ve B dahil ikisi de yazılır). 'ALGILAMA SAĞLAM' = S+ E payı >= 0,60 VE S+ E payı - S- E payı "
                     ">= 0,30; 'ALGILAMA KIRIK' = S+ E payı < 0,40; arası 'KISMİ'. Taban içi / dışı E payı ve Fisher kesin p bilgi; n küçük "
                     "(30 / 10): 'bulgu' değil, tanı"},
    "kalibrasyon": {"PAPIL": {"pazar": "BIST", "bas": "2025-11-13", "son": "2025-12-09", "kaynak": "oc_veri V_BIST"},
                    "TEHOL_2505": {"pazar": "BIST", "sembol": "TEHOL", "bas": "2025-05-02", "son": "2025-05-28",
                                   "kaynak": "oc_veri V_BIST; Cemal düzeltmesi (16 Kas): bölge 2024-12-01 .. 2025-05-28, parmak izi Mayıs 2025"},
                    "TEHOL_bolge": {"pazar": "BIST", "sembol": "TEHOL", "bas": "2025-03-03", "son": "2025-05-28",
                                    "kaynak": "oc_veri V_BIST; bağlam (Mart-Nisan yatay + Mayıs): S6 tabanı açık mı"},
                    "BINBN": {"pazar": "BIST", "bas": "2024-12-17", "son": "2025-01-21", "kaynak": "oc_veri V_BIST; Cemal 'en net olan'"},
                    "DGXX": {"pazar": "ABD", "bas": "2026-10-20", "son": "2026-11-16",
                             "kaynak": "yfinance (auto_adjust=False, 2025-01-01 ..; V_ABD 31.08.2026'da kesik); 16 Kas seans içi yarım bar "
                                       "ATILIR (K3); ölçüme girmez"}},
    "cemal_ornek": {"ornekler": ["PAPIL", "TEHOL_2505", "BINBN", "TEHOL_bolge"],
                    "tanim": "EK ÖRNEKLER (Cemal 16 Kas; sonuç görülmeden eklendi; TEHOL Şubat 2026 etiketi Cemal düzeltmesiyle KALDIRILDI, TEHOL bölgesi 2024-12-01 .. 2025-05-28, parmak izi Mayıs 2025; S+ beklenen: PAPIL, TEHOL Mayıs 2025, BINBN; S- beklenen: DGXX): her BIST kalibrasyon penceresi için olay t = (i) pencerenin "
                             "İLK S+ (k10) günü (yoksa yazılmaz) ve (ii) pencerenin SON günü; her olay için cetvel r60 ve r20 eşli fark (tek olay, "
                             "oc_olc; tekilleştirme olay başına ayrı), taban içi mi, taban içiyse kırılım (h3 tanımı); pencerede S+ / gevşek / sıkı / "
                             "küçük S+ günleri ve S6 taban içi günleri. n küçük: BİLGİ, karar değildir"},
    "gelecek_denetimi": {"n": 40, "tohum": 1612,
                         "tanim": "kos: her pazarda rastgele 40 (sembol, t) durum gününde seri t'de kesilir; fk_hisse yeniden: TABAN İÇİ, kutu "
                                  "üst / alt, S+ / S- aynı olmalı; tutmazsa koşu DURUR"},
}

FK_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "(a) eşler YALNIZ ORTAK_CETVEL.oc_olc (aynı giriş günü, 60 gün momentum beşlisi x 20 gün likidite üçlüsü, 200 plasebo); "
                   "(b) kontrol = TABAN İÇİ ama S+ olmayan günler (aynı S6 bölge ailesi, aynı cetvel mekaniği) + bölge başına tek rastgele gün "
                   "(K_SP_r, konum dengesi); kırılım kontrolü aynı bölge kutusu. Mekanik üstünlük: S+ kapanış dipte -> giriş t+1 açılış; "
                   "kırılım tavanı t günü dahil kutu, t kapanışı tavanın altında (S6 AL tanımı)"),
    "K2": ("EVET", "fitil pencereleri rolling (geriye); S6 durum makinesi sıralı (as-of t: bölge, sınıf = onay günü sınıfı, kutu t'ye kadar); "
                   "kos fk_gelecek_denetimi her pazarda 40 olayda seriyi t'de kesip yeniden hesaplar, tutmazsa DURUR; kör sayfada t'den sonra "
                   "bar çizilmez (test)"),
    "K3": ("EVET", "OC.oc_veri temiz barları (H>L, V>0, fiyat > 0); geçersiz bar sinyal / ölçü üretmez; DGXX kalibrasyonunda 16 Kas seans içi "
                   "yarım bar atılır"),
    "K4": ("EVET", "cetvel oc_olay_hazirla aynı hissede 60 gün tekilleştirir (n bağımsız olay); kırılım cetvelin tekil olaylarında; kör sette "
                   "aynı hisse bir kez; hücrede medyan da yazılır"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (cetvel); kırılım t+1 kapanışından itibaren; kör anahtarı sonucu da t+1 açılış"),
    "K6": ("EVET", "tek kip V_*.pkl düzeltilmiş fiyat (fi_k1_veri); fitil payları ve oransal eksen birimden bağımsız; DGXX ham (auto_adjust=False) "
                   "yalnız kalibrasyon, fitil payı birim etkisiz"),
    "K7": ("EVET", "evren bugün işlem görenler (V_*; k34_yahoo yoksa ABD yalnız V_ABD); batanlar yok; raporda 'getiriler yukarı yanlı' notu; "
                   "kırılımda AŞAĞI oranı aşağı yanlı okunur"),
    "K8": ("EVET", "3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki yarı şartı (cetvel); varyantlar bilgi; kör set 30 + 10 küçük n: 'tanı', bulgu "
                   "değil; olay sayımı bu ön kayıtta getirisiz"),
    "K9": ("EVET", "FK_ESIK sha + FITIL_KOR.py sha + FO_ESIK sha + S6_PRM sha + cetvel üç sha + veri sha bu dosyada; iş tanımı koşudan önce "
                   "git'e işlendi; kos / kor ik_kontrol_kapisi + oc_kapi + fk_onkayit_dogrula geçmezse durur; eşik sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "metin / KAP ayrıştırma yok; yalnız OHLCV; kalibrasyon sayfalarında fitil payları ham bardan yazılır"),
    "K11": ("EVET", "olay satırları FK_SATIR klasöründe (olay_<satır>_<r>.csv.gz); >= 2 hücre bağımsız kodla yeniden üretilir (rapor DENETİM)"),
    "K12": ("EVET", "etiketler yalnız önceden yazılı kurallarla; 'iz / emare' sözü yalnız kural geçerse; sayı ve yorum ayrı cümle; 'al' / "
                    "'öneri' dili yok; kör PDF'te hisse / tarih / sonuç yok"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_fk; defter dosyaları ve mevcut .py modülleri yalnız import (git status); e-posta / anahtar "
                    "taraması (ön kayıt, sonuç, rapor, anahtar); commit / push ana modelin"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; tanı ölçümü (kapalı konu 'tek göstergeye göre alım' açılmaz)"),
}

FK_CIZIM = {"yesil": "#26a69a", "kirmizi": "#ef5350", "zemin": "#9e9e9e", "baslik": "#1f2a44", "vurgu": "#c0392b"}


class FKHata(RuntimeError):
    """Durdurucu hata: ön kayıt yok / sha tutmuyor / kapı / geleceğe bakma denetimi / veri yok."""


# ================================================================ 0) ORTAK
_FK_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_FK_ANAHTAR = re.compile(r"(api[_-]?key|token|secret|password|şifre)\s*[=:]\s*['\"][^'\"]{8,}", re.I)


def _fk_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _fk_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _fk_sha_obj(o: Any) -> str:
    return hashlib.sha256(json.dumps(o, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")).hexdigest()


def fk_esik_sha() -> str:
    return _fk_sha_obj(FK_ESIK)


def _fk_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or FK_YOL["cikti"], FK_DOSYA[ad])


def _fk_sizinti(metin: str, ad: str) -> None:
    if _FK_EPOSTA.search(metin) or _FK_ANAHTAR.search(metin):
        raise FKHata(f"{ad}: e-posta / anahtar biçimli parça var")


def fk_e20() -> Dict[str, Any]:
    """r20 için cetvel kopyası: yalnız olcu.ufuk = 20."""
    E = copy.deepcopy(OC.OC_ESIK)
    E["olcu"]["ufuk"] = 20
    return E


# ================================================================ 1) HİSSE: fitil bayrakları + S6 taban içi (yalnız t'ye kadar)
def fk_hisse(df: pd.DataFrame) -> pd.DataFrame:
    """Temiz barlar (oc_veri) -> her bar: olculur, ic, dis, SP, SM, SPg, SPs, SPk, bolge, ust, alt. Hepsi as-of t."""
    d = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)
    kol = ["olculur", "ic", "dis", "SP", "SM", "SPg", "SPs", "SPk", "dipb", "duz", "duz07", "duz15"]
    if len(d) < FO.FO_ESIK["k_ana"] + 1:
        Z = pd.DataFrame(False, index=d.index, columns=kol)
        Z["bolge"] = -1; Z["ust"] = np.nan; Z["alt"] = np.nan; Z["duz_oran"] = np.nan; Z["wH"] = np.nan; Z["wL"] = np.nan
        return Z
    B = FO.fo_bar(d)
    P = FO.fo_pencere(B, FO.FO_ESIK["k_ana"]).reindex(d.index)
    V = FK_ESIK["varyant"]
    with np.errstate(invalid="ignore"):
        SP = FO.fo_kural(P, "SP").fillna(False).astype(bool)
        SM = FO.fo_kural(P, "SM").fillna(False).astype(bool)
        SPg = ((P.ASIM >= V["SPg"]["asim_min"]) & (P.ALTYOK >= V["SPg"]["altyok_min"])).fillna(False).astype(bool)
        SPs = ((P.ASIM >= V["SPs"]["asim_min"]) & (P.ALTYOK >= V["SPs"]["altyok_min"])).fillna(False).astype(bool)
    SPk = SP & P.KUCUK.fillna(False).astype(bool)
    Dz = V["duz"]; k = FO.FO_ESIK["k_ana"]
    wH = d.High.rolling(k, min_periods=k).max(); wL = d.Low.rolling(k, min_periods=k).min()
    with np.errstate(invalid="ignore", divide="ignore"):
        duz_oran = (d.Low.rolling(k, min_periods=k).max() - wL) / (d.High - d.Low).rolling(k, min_periods=k).median()
        cmx = d.Close.rolling(Dz["konum_gun"], min_periods=Dz["konum_gun"]).max(); cmn = d.Close.rolling(Dz["konum_gun"], min_periods=Dz["konum_gun"]).min()
        konum = ((d.Close - cmn) / (cmx - cmn)).where(cmx > cmn)
    T = S6.s6_taban(d)
    bid = T["bolge_id"].to_numpy(int)
    sinif = T["sinif"].astype(str).to_numpy()
    ilk_sinif: Dict[int, str] = {}
    for b, s in zip(bid, sinif):
        if b >= 0 and b not in ilk_sinif:
            ilk_sinif[b] = s                                  # bölgenin ilk barı = onay günü (as-of: t >= onay)
    bs = np.array([ilk_sinif.get(b, "") for b in bid], dtype=object)
    olc = T["olculur"].to_numpy(bool)
    acik = np.isin(T["durum"].astype(str).to_numpy(), ["YENI", "SURER", "YENIDEN"])
    ic = olc & (bid >= 0) & acik & (bs == "DIP")
    Z = pd.DataFrame({"olculur": olc, "ic": ic, "dis": olc & ~ic, "SP": SP.to_numpy(bool), "SM": SM.to_numpy(bool),
                      "SPg": SPg.to_numpy(bool), "SPs": SPs.to_numpy(bool), "SPk": SPk.to_numpy(bool),
                      "dipb": ic | (konum.to_numpy(float) <= Dz["konum_max"]),
                      "duz": (duz_oran <= Dz["esik"]).to_numpy(bool), "duz07": (duz_oran <= Dz["esik_bilgi"][0]).to_numpy(bool),
                      "duz15": (duz_oran <= Dz["esik_bilgi"][1]).to_numpy(bool), "duz_oran": duz_oran.to_numpy(float),
                      "wH": wH.to_numpy(float), "wL": wL.to_numpy(float),
                      "bolge": np.where(ic, bid, -1), "ust": np.where(ic, T["kutu_ust"].to_numpy(float), np.nan),
                      "alt": np.where(ic, T["kutu_alt"].to_numpy(float), np.nan)}, index=d.index)
    return Z


def fk_satir_maske(Z: pd.DataFrame, sembol: str) -> Dict[str, np.ndarray]:
    """fk_hisse çıktısı -> satır başına durum günü maskesi (FK_ESIK satirlar)."""
    o, ic, dis = Z.olculur.to_numpy(bool), Z.ic.to_numpy(bool), Z.dis.to_numpy(bool)
    SP, SM = Z.SP.to_numpy(bool), Z.SM.to_numpy(bool)
    M = {"SP_ic": SP & ic, "SM_ic": SM & ic, "SP_dis": SP & dis, "SM_dis": SM & dis, "SP_tum": SP & o, "SM_tum": SM & o,
         "K_SP": ic & ~SP, "K_SM": ic & ~SM, "SPg_ic": Z.SPg.to_numpy(bool) & ic, "SPs_ic": Z.SPs.to_numpy(bool) & ic,
         "SPk_ic": Z.SPk.to_numpy(bool) & ic}
    dipb = Z.dipb.to_numpy(bool) & o
    M["SPD"] = SP & Z.duz.to_numpy(bool) & dipb; M["SPD07"] = SP & Z.duz07.to_numpy(bool) & dipb
    M["SPD15"] = SP & Z.duz15.to_numpy(bool) & dipb; M["K_DUZ"] = ~SP & Z.duz.to_numpy(bool) & dipb
    M["SPDb"] = SP & Z.duz.to_numpy(bool) & o; M["K_DUZb"] = ~SP & Z.duz.to_numpy(bool) & o
    bol = Z.bolge.to_numpy(int)
    rng = np.random.default_rng([FK_ESIK["kontrol_tohum"], zlib.crc32(sembol.encode("utf-8"))])
    for ad, kay in (("K_SP_r", M["K_SP"]), ("K_SM_r", M["K_SM"])):
        r = np.zeros(len(Z), bool)
        for b in np.unique(bol[kay]):
            ix = np.flatnonzero(kay & (bol == b))
            r[ix[int(rng.integers(len(ix)))]] = True
        M[ad] = r
    return M


def fk_sinyaller(Vd: Dict[str, Any], pazar: str) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """oc_veri çıktısı -> (durum günleri DataFrame[sembol, tarih, pazar, satir], {sembol: fk_hisse tablosu (yalnız ic günleri + bayraklar)})."""
    V = Vd["V"]; evb = Vd.get("evren_bas", {}); sat, ZZ = [], {}
    for s in sorted(V):
        try:
            Z = fk_hisse(V[s])
        except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer (S6 / FO hatası); sayım loglanır
            fklog.warning("%s %s atlandı: %s", pazar, s, ex); continue
        if s in evb:
            Z.loc[Z.index < pd.Timestamp(evb[s]), ["olculur", "ic", "dis"]] = False
        M = fk_satir_maske(Z, s)
        for ad, m in M.items():
            if m.any():
                sat.append(pd.DataFrame({"sembol": s, "tarih": Z.index[m], "pazar": pazar, "satir": ad}))
        ZZ[s] = Z[Z.ic | Z.SP | Z.SM | Z.duz]
    X = pd.concat(sat, ignore_index=True) if sat else pd.DataFrame(columns=["sembol", "tarih", "pazar", "satir"])
    X["tarih"] = pd.to_datetime(X.tarih)
    return X, ZZ


# ================================================================ 2) GELECEĞE BAKMA DENETİMİ
def fk_gelecek_denetimi(Vd: Dict[str, Any], X: pd.DataFrame, ZZ: Dict[str, pd.DataFrame], pazar: str) -> int:
    G = FK_ESIK["gelecek_denetimi"]; rng = np.random.default_rng(G["tohum"]); V = Vd["V"]; say = 0
    Xh = X[X.satir.isin(["SP_ic", "SM_ic", "SP_dis", "K_SP", "SPD", "K_DUZ"])]
    if not len(Xh):
        return 0
    for r in Xh.iloc[rng.choice(len(Xh), min(G["n"], len(Xh)), replace=False)].itertuples():
        t = pd.Timestamp(r.tarih); kes = V[r.sembol][V[r.sembol].index <= t]
        Zk = fk_hisse(kes).iloc[-1]; Zt = ZZ[r.sembol].loc[t]
        ayni = (Zk.name == t and bool(Zk.duz) == bool(Zt.duz) and bool(Zk.dipb) == bool(Zt.dipb) and bool(Zk.ic) == bool(Zt.ic) and bool(Zk.SP) == bool(Zt.SP) and bool(Zk.SM) == bool(Zt.SM)
                and (not Zt.ic or (np.isclose(Zk.ust, Zt.ust) and np.isclose(Zk.alt, Zt.alt))))
        if not ayni:
            raise FKHata(f"geleceğe bakma denetimi tutmadı: {pazar} {r.sembol} {t.date()} {r.satir}")
        say += 1
    return say


# ================================================================ 3) KIRILIM ve BOOTSTRAP
def fk_kirilim(C: np.ndarray, i: int, tavan: float, dip: float, ufuk: int = 60, carpan: float = 0.98) -> str:
    """t = i. bar; t+1 .. t+ufuk kapanışlarında ilk C > tavan (YUKARI) / C < dip x carpan (AŞAĞI); bar yetmezse 'OLCULMEZ'."""
    if not (np.isfinite(tavan) and np.isfinite(dip)) or i + ufuk >= len(C):
        return "OLCULMEZ"
    w = C[i + 1:i + 1 + ufuk]
    u = np.flatnonzero(w > tavan); a = np.flatnonzero(w < dip * carpan)
    u0 = u[0] if len(u) else 10 ** 9; a0 = a[0] if len(a) else 10 ** 9
    if u0 < a0:
        return "YUKARI"
    if a0 < u0:
        return "ASAGI"
    return "YOK"


def fk_kirilim_ekle(Ol: pd.DataFrame, V: Dict[str, pd.DataFrame], ZZ: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    K = FK_ESIK["h3"]["kirilim"]; out = []
    for r in Ol.itertuples():
        d = V[r.sembol]; t = pd.Timestamp(r.tarih); i = int(d.index.get_loc(t)); z = ZZ[r.sembol].loc[t]
        C = d.Close.to_numpy(float)
        out.append((fk_kirilim(C, i, float(z.ust), float(z.alt), K["ufuk"], K["asagi_carpan"]) if bool(z.ic) else "UYGULANMAZ",
                    fk_kirilim(C, i, float(z.wH), float(z.wL), K["ufuk"], K["asagi_carpan"])))
    Ol = Ol.copy(); Ol["kirilim"] = [a for a, _ in out]; Ol["kirilim10"] = [b for _, b in out]
    return Ol


def fk_fark_boot(a: np.ndarray, ga: np.ndarray, b: np.ndarray, gb: np.ndarray) -> Dict[str, float]:
    """İki grup ayrı ay kümeli bootstrap: fark = ort(a) - ort(b); %95."""
    F = FK_ESIK["fark_bootstrap"]
    ia, ib = np.isfinite(a), np.isfinite(b)
    a, ga, b, gb = a[ia], ga[ia], b[ib], gb[ib]
    out = {"n_a": int(len(a)), "n_b": int(len(b)), "ort_a": float(a.mean()) if len(a) else np.nan,
           "ort_b": float(b.mean()) if len(b) else np.nan, "fark": np.nan, "alt95": np.nan, "ust95": np.nan}
    if not len(a) or not len(b):
        return out
    out["fark"] = out["ort_a"] - out["ort_b"]
    rng = np.random.default_rng(F["tohum"])

    def hazir(x, g):
        u, inv = np.unique(g, return_inverse=True)
        return np.bincount(inv, weights=x), np.bincount(inv).astype(float)
    sa, na = hazir(a, ga); sb, nb = hazir(b, gb); v = np.empty(F["n"])
    for k in range(F["n"]):
        xa = rng.integers(0, len(sa), len(sa)); xb = rng.integers(0, len(sb), len(sb))
        v[k] = sa[xa].sum() / na[xa].sum() - sb[xb].sum() / nb[xb].sum()
    out["alt95"] = float(np.quantile(v, 0.025)); out["ust95"] = float(np.quantile(v, 0.975))
    return out


def fk_ayrisma(r: Dict[str, Any], yon: str) -> str:
    n = OC.OC_ESIK["hucre_karar"]["n_esik"]
    if r.get("n_a", 0) < n or r.get("n_b", 0) < n:
        return "ÖLÇÜLEMEDİ"
    if yon == "+":
        return "AYRIŞIR" if r["fark"] > 0 and r["alt95"] > 0 else "AYRIŞMAZ"
    return "AYRIŞIR" if r["fark"] < 0 and r["ust95"] < 0 else "AYRIŞMAZ"


def fk_ayrisma_genel(dur: Dict[str, str]) -> str:
    kh = [f"{p} {d}" for p in OC.OC_ESIK["karar_pazar"] for d in OC.OC_ESIK["karar_donem"]]
    v = [dur.get(k) for k in kh]
    if all(x == "AYRIŞIR" for x in v):
        return "KONTROLDEN AYRIŞIR"
    tut = [k for k, x in zip(kh, v) if x == "AYRIŞIR"]
    if tut:
        return "KISMİ (" + ", ".join(tut) + ")"
    if all(x == "ÖLÇÜLEMEDİ" for x in v):
        return "ÖLÇÜLEMEDİ"
    return "AYRIŞMAZ"


def _fk_ay(g: pd.Series) -> np.ndarray:
    return pd.to_datetime(g).dt.to_period("M").astype(str).to_numpy()


# ================================================================ 4) ÖN KAYIT
def _fk_is_tanimi_git() -> Dict[str, str]:
    try:
        return OC._oc_git_islenmis(FK_YOL["is_tanimi"])
    except OC.OCHata as ex:
        raise FKHata(f"iş tanımı git kapısı: {ex}")


def fk_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = FK_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', '')} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def fk_muhur() -> Dict[str, str]:
    return {"FK_ESIK_SHA": fk_esik_sha(), "FK_KOD_SHA": _fk_sha_dosya(FK_YOL["kod"]), "FO_ESIK_SHA": FO.fo_esik_sha(),
            "S6_PRM_SHA": _fk_sha_obj(S6.S6_PRM), "IS_TANIMI_SHA": _fk_sha_dosya(FK_YOL["is_tanimi"])}


def fk_onkayit_metni(say: Dict[str, Any], vsha: Dict[str, str], notlar: Dict[str, List[str]], git_it: Dict[str, str]) -> str:
    E = FK_ESIK; M = fk_muhur()
    s = ["# FITIL_KOR — ÖN KAYIT (fitil öbeği: hata nerede? üç halka)", "", FK_SURUM, ""] + \
        [f"- {k}: `{v}`" for k, v in M.items()] + \
        [f"- İş tanımı git: {git_it.get('commit', '-')[:10]} ({git_it.get('commit_zamani', '-')})", f"- ZAMAN (UTC): `{_fk_simdi()}`", "",
         "Bu dosya ölçümden ÖNCE yazıldı; hiçbir getiri / eş farkı / kırılım hesaplanmadı (yalnız durum günü ve cetvel tekil olay sayımı, "
         "getirisiz). `kos` / `kor` kontrol listesi, cetvel üç sha'sı, yukarıdaki beş sha ve iş tanımının git kaydı tutmazsa durur. Eşikler "
         "sonuç görülünce değişmez.", "",
         "## Cetvel mühür satırları (ORTAK_CETVEL; aynen)", "", OC.oc_kapi_satirlari(), "",
         "## Tanım (sabit)", "", f"- Fitil: {E['fitil']}.", f"- S6: {E['s6']}.", f"- TABAN İÇİ: {E['ic']}.", f"- TABAN DIŞI: {E['dis']}.",
         f"- Ölçülür: {E['olculur']}.", f"- Varyantlar: gevşek {E['varyant']['SPg']}, sıkı {E['varyant']['SPs']}, küçük: {E['varyant']['SPk']}.",
         f"- S+DÜZ: {E['varyant']['duz']['tanim']}.", f"- Kırılım 10 mum kutusu: {E['h3']['kirilim10']}.", f"- Kör set ek: {E['kor']['ek']}.",
         f"- Olay: {E['olay']}.", "", "Satırlar:", ""] + [f"- {k}: {v}" for k, v in E["satirlar"].items()] + \
        ["", f"r60 (cetvel) satırları: {', '.join(E['r60_satir'])}. r20 satırları: {', '.join(E['r20_satir'])}.", "",
         "## HALKA 1 karar kuralı (önceden yazılı)", "", f"- (a) {E['h1_karar']['a']}.", f"- (b) {E['h1_karar']['b']}.",
         f"- Varyant: {E['h1_karar']['varyant']}.", f"- Fark bootstrap: {E['fark_bootstrap']['tanim']} (n {E['fark_bootstrap']['n']}, tohum "
         f"{E['fark_bootstrap']['tohum']}, küme {E['fark_bootstrap']['kume']}).", "",
         "## HALKA 3 kuralı (önceden yazılı)", "", f"- r20: {E['h3']['r20']}.", f"- Kırılım: {E['h3']['kirilim']['tanim']}.",
         f"- Kırılım kararı: {E['h3']['kirilim_karar']}.", f"- Genel S+: {E['h3']['genel']}.", "",
         "## HALKA 2 kör set (önceden yazılı)", "", f"- Seçim: {E['kor']['secim']}.", f"- Grup / pazar: {E['kor']['grup']}.",
         f"- Sayfa: {E['kor']['sayfa']}.", f"- Yanıt: {E['kor']['cevap']}.", f"- Okuma: {E['kor']['karar']}.",
         "- Kalibrasyon (kör sete girmez; adlı, tarihli): " + "; ".join(f"{k} {v['pazar']} {v['bas']} .. {v['son']} ({v['kaynak']})"
                                                                       for k, v in E["kalibrasyon"].items()) + ".", "",
         "## EK ÖRNEKLER (Cemal 16 Kas; ön kayıttan önce geldi, sonuç görülmeden eklendi)", "", f"- {E['cemal_ornek']['tanim']}.",
         "- Pencereler: " + "; ".join(f"{k} {E['kalibrasyon'][k]['bas']} .. {E['kalibrasyon'][k]['son']}" for k in E['cemal_ornek']['ornekler']) +
         ". Hepsi adlı kalibrasyon sayfası olarak da basılır (fitil payları altta).", "",
         "## Tanı okuması ve beklenti (önceden yazılı)", "", f"- {E['tani']}.", "",
         "## Veri", ""] + [f"- V_{p}.pkl sha256: `{v}`" for p, v in vsha.items()] + \
        [f"- {p} oc_veri notu: {'; '.join(n)}" for p, n in notlar.items()] + ["",
         "## SAYIM (getirisiz; durum günü sinyal tarihine, cetvel tekil olay giriş tarihine göre dönem)", "",
         "| Satır | Pazar | durum günü | OLAY (tekil, havuzda) 2016-22 / 2023 / 2024-26 |", "|---|---|---|---|"]
    for sat in E["r60_satir"]:
        for p, c in say.items():
            v = c.get(sat, {})
            o = v.get("olay", {})
            s.append(f"| {sat} | {p} | {v.get('durum', 0)} | {o.get('2016-22', 0)} / {o.get('2023', 0)} / {o.get('2024-26', 0)} |")
    s += ["", "Kural: hücre n < 30 ise ÖLÇÜLEMEDİ.", "",
          "## SAPMA / sınır (sonuç görülmeden yazıldı)", "",
          "- Ön kaydı alt ajan git'e işleyemez (commit yasak): iş tanımı koşudan önce işlendi; bu dosyanın sha'sı ve yazım zamanı "
          "halka_sonuc.json'a yazılır, kos zamanı ondan sonradır (--gitsiz). Ana model işlerken sha'yı karşılaştırır.",
          "- k34_yahoo (veri2) yoksa ABD evreni yalnız V_ABD (oc_veri notu).",
          "- Kontrol K_SP cetvel tekilleştirmesiyle bölgenin ilk günlerine yığılır (S+ günü bölgede daha geç olabilir): bu yüzden bölge başına "
          "tek rastgele gün K_SP_r bilgi kontrolü olarak yazılır.",
          "- r20 hücrelerinde güç tablosu (r60) uygulanmaz; 'TUTAR' bilgi.", "",
          fk_kontrol_tablosu(), "",
          "## Test", "", "`python test_fitil_kor.py` (sentetik: taban içi tanımı, geleceğe bakma kesme, kırılım, fark bootstrap, kör sayfada "
          "ad / tarih / sonrası yok, yanıt ayrıştırma ve Fisher, kapı, e-posta / anahtar taraması).", ""]
    return "\n".join(s)


def fk_sayim(X: pd.DataFrame, P: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for sat in FK_ESIK["r60_satir"]:
        x = X[X.satir == sat][["sembol", "tarih", "pazar"]]
        Y, _ = OC.oc_olay_hazirla(x, P)
        out[sat] = {"durum": int(len(x)), "olay": {k: int(v) for k, v in (Y.donem.value_counts().to_dict() if len(Y) else {}).items() if k}}
    return out


def fk_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False) -> str:
    yol = _fk_yol("onkayit", cikti)
    if os.path.exists(yol):
        try:
            OC._oc_git_islenmis(yol)
            raise FKHata(f"ön kayıt git'e işlenmiş ({yol}); üzerine yazılmaz")
        except OC.OCHata:
            if not uzerine:
                raise FKHata(f"ön kayıt var ({yol}); git'e işlenmemişse --uzerine-yaz")
    for ad in ("sonuc", "anahtar"):
        if os.path.exists(_fk_yol(ad, cikti)):
            raise FKHata(f"{FK_DOSYA[ad]} var: ölçüm / kör set üretilmiş, ön kayıt yeniden yazılamaz (SAPMA)")
    git_it = _fk_is_tanimi_git(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    say, vsha, notlar = {}, {}, {}
    for p in OC.OC_ESIK["pazar"]:
        vsha[p] = _fk_sha_dosya(os.path.join(veri or FK_YOL["veri"], f"V_{p}.pkl"))
        Vd = OC.oc_veri(p, klasor=veri or FK_YOL["veri"]); notlar[p] = list(Vd.get("not", []))
        X, _ = fk_sinyaller(Vd, p); P = OC.oc_panel(Vd)
        say[p] = fk_sayim(X, P); fklog.info("%s: durum günü %d", p, len(X))
        del Vd, P, X
    metin = fk_onkayit_metni(say, vsha, notlar, git_it)
    _fk_sizinti(metin, "ön kayıt")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    fklog.info("ön kayıt yazıldı: %s", yol)
    return yol


def fk_onkayit_dogrula(yol: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    yol = yol or _fk_yol("onkayit")
    if not os.path.exists(yol):
        raise FKHata(f"ön kayıt yok ({yol}): önce `python FITIL_KOR.py onkayit`")
    metin = open(yol, encoding="utf-8").read(); simdi = fk_muhur(); out: Dict[str, Any] = {"yol": yol}
    for ad, v in simdi.items():
        m = re.search(ad + r":\s*`([0-9a-f]{64})`", metin)
        if not m:
            raise FKHata(f"ön kayıt bozuk: '{ad}' satırı yok")
        if m.group(1) != v:
            raise FKHata(f"{ad} tutmuyor (ön kayıt {m.group(1)[:12]}…, şimdi {v[:12]}…): koşu DURDU (SAPMA)")
        out[ad] = v
    out["onkayit_sha"] = _fk_sha_dosya(yol)
    z = re.search(r"ZAMAN \(UTC\):\s*`([^`]+)`", metin)
    if not z:
        raise FKHata("ön kayıt bozuk: ZAMAN satırı yok")
    out["onkayit_yazim_utc"] = z.group(1)
    out["git_is_tanimi"] = _fk_is_tanimi_git()
    try:
        out["git_onkayit"] = OC._oc_git_islenmis(yol)
    except OC.OCHata as ex:
        if git:
            raise FKHata(f"{ex} (alt ajan commit yapamaz: --gitsiz ile koş, SAPMA olarak yazılır)")
        out["git_onkayit"] = f"İŞLENMEDİ (gitsiz koşu; ön kayıt sha {out['onkayit_sha'][:12]}…, yazım {out['onkayit_yazim_utc']})"
    return out


def fk_kapi(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    yol = _fk_yol("onkayit", cikti)
    if kontrol:
        import IZ_KARNE as IK
        try:
            IK.ik_kontrol_kapisi(yol)
        except RuntimeError as ex:
            raise FKHata(str(ex))
    try:
        kapi = OC.oc_kapi(yol, git=False, kontrol=False)
    except OC.OCHata as ex:
        raise FKHata(str(ex))
    ok = fk_onkayit_dogrula(yol, git=git)
    ok["oc_kapi"] = {k: v for k, v in kapi.items() if k != "kontrol"}
    ok["kos_zaman_utc"] = _fk_simdi()
    if ok["onkayit_yazim_utc"] > ok["kos_zaman_utc"]:
        raise FKHata("ön kayıt zamanı koşu zamanından sonra")
    return ok


def fk_cemal_ornek(Vd: Dict[str, Any], P: Dict[str, Any], P20: Optional[Dict[str, Any]], E20: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Cemal örnekleri (BİLGİ): her BIST kalibrasyon penceresi için ilk S+ günü ve son gün olayları; r60 / r20 eşli fark, taban içi, kırılım."""
    out = []; Kr = FK_ESIK["h3"]["kirilim"]
    for ad in FK_ESIK["cemal_ornek"]["ornekler"]:
        K = FK_ESIK["kalibrasyon"][ad]; sem = K.get("sembol", ad); d = Vd["V"].get(sem)
        if d is None:
            out.append({"ornek": ad, "not": "veri yok"}); continue
        Z = fk_hisse(d); m = (Z.index >= pd.Timestamp(K["bas"])) & (Z.index <= pd.Timestamp(K["son"])); Zw = Z[m]
        gunler = {k: [str(t.date()) for t in Zw.index[Zw[k].to_numpy(bool)]] for k in ("SP", "SPg", "SPs", "SPk", "SM", "ic")}
        olay = []
        if len(gunler["SP"]):
            olay.append(("ilk_SP", pd.Timestamp(gunler["SP"][0])))
        if len(Zw):
            olay.append(("son_gun", Zw.index[-1]))
        for tur, t in olay:
            r: Dict[str, Any] = {"ornek": ad, "sembol": sem, "olay": tur, "tarih": str(t.date()), "taban_ici": bool(Z.loc[t, "ic"])}
            for etk, PP, EE in (("r60", P, OC.OC_ESIK), ("r20", P20, E20)):
                if PP is None:
                    continue
                S = OC.oc_olc(pd.DataFrame({"sembol": [sem], "tarih": [t], "pazar": [K["pazar"]]}), {K["pazar"]: PP}, EE)
                o = S["olay"]
                r[f"{etk}_fark"] = float(o.fark.iloc[0]) if len(o) and np.isfinite(o.fark.iloc[0]) else None
                r[f"{etk}"] = float(o.r60.iloc[0]) if len(o) and np.isfinite(o.r60.iloc[0]) else None
                if etk == "r60":
                    r["giris"] = str(pd.Timestamp(o.giris.iloc[0]).date()) if len(o) else None
            i = int(d.index.get_loc(t))
            r["kirilim"] = (fk_kirilim(d.Close.to_numpy(float), i, float(Z.loc[t, "ust"]), float(Z.loc[t, "alt"]), Kr["ufuk"], Kr["asagi_carpan"])
                            if r["taban_ici"] else "UYGULANMAZ")
            out.append(r)
        out.append({"ornek": ad, "sembol": sem, "olay": "pencere", "bas": K["bas"], "son": K["son"], **{f"{k}_gun": v for k, v in gunler.items()}})
    return out


# ================================================================ 5) KOŞU: HALKA 1 + HALKA 3
def _fk_hucre_json(T: pd.DataFrame) -> List[Dict[str, Any]]:
    return json.loads(T.to_json(orient="records", force_ascii=False)) if len(T) else []


def fk_kos(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or FK_YOL["cikti"]; ok = fk_kapi(cikti, git, kontrol)
    os.makedirs(FK_YOL["satir"], exist_ok=True); E20 = fk_e20()
    sonuc: Dict[str, Any] = {"surum": FK_SURUM, "onkayit": ok, "fk_esik_sha": fk_esik_sha(), "cetvel20_sha": OC.oc_esik_sha(E20),
                             "gelecek_denetimi": {}, "veri_not": {}, "r60": {}, "r20": {}, "h1b": {}, "h3_r20b": {}, "h3_kir": {}, "once20": {}}
    OL60: Dict[str, List[pd.DataFrame]] = {s: [] for s in FK_ESIK["r60_satir"]}
    OL20: Dict[str, List[pd.DataFrame]] = {s: [] for s in FK_ESIK["r20_satir"]}
    H60: Dict[str, List[pd.DataFrame]] = {s: [] for s in FK_ESIK["r60_satir"]}
    H20: Dict[str, List[pd.DataFrame]] = {s: [] for s in FK_ESIK["r20_satir"]}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or FK_YOL["veri"]); sonuc["veri_not"][p] = list(Vd.get("not", [])) + [f"hisse {len(Vd['V'])}"]
        X, ZZ = fk_sinyaller(Vd, p)
        sonuc["gelecek_denetimi"][p] = fk_gelecek_denetimi(Vd, X, ZZ, p)
        fklog.info("%s: durum %d; geleceğe bakma denetimi TUTTU (%d) %.0f sn", p, len(X), sonuc["gelecek_denetimi"][p], time.time() - t0)
        P = OC.oc_panel(Vd)
        for sat in FK_ESIK["r60_satir"]:
            x = X[X.satir == sat][["sembol", "tarih", "pazar"]].reset_index(drop=True)
            S = OC.oc_olc(x, {p: P})
            Ol = S["olay"].copy()
            if len(Ol) and sat in ("SP_ic", "SM_ic", "K_SP", "K_SM", "K_SP_r", "K_SM_r", "SPg_ic", "SPs_ic", "SPk_ic", "SPD", "SPD07",
                                 "SPD15", "K_DUZ", "SPDb", "K_DUZb"):
                Ol = fk_kirilim_ekle(Ol, Vd["V"], ZZ)
            if len(S["hucre"]):
                H60[sat].append(S["hucre"].drop(columns=[c for c in S["hucre"].columns if c.startswith("_")], errors="ignore"))
            OL60[sat].append(Ol)
            fklog.info("%s r60 %s: olay %d (%.0f sn)", p, sat, len(Ol), time.time() - t0)
        P20 = OC.oc_panel(Vd, E20)
        if p == "BIST":
            sonuc["cemal_ornek"] = fk_cemal_ornek(Vd, P, P20, E20)
        del P
        for sat in FK_ESIK["r20_satir"]:
            x = X[X.satir == sat][["sembol", "tarih", "pazar"]].reset_index(drop=True)
            S = OC.oc_olc(x, {p: P20}, E20)
            if len(S["hucre"]):
                H20[sat].append(S["hucre"])
            OL20[sat].append(S["olay"])
            fklog.info("%s r20 %s: olay %d (%.0f sn)", p, sat, len(S["olay"]), time.time() - t0)
        del P20, Vd, X, ZZ
    # birleştir, satır dosyaları
    for sat in FK_ESIK["r60_satir"]:
        Ol = pd.concat([o for o in OL60[sat] if len(o)], ignore_index=True) if any(len(o) for o in OL60[sat]) else pd.DataFrame()
        OL60[sat] = Ol
        if len(Ol):
            Ol.to_csv(os.path.join(FK_YOL["satir"], f"olay_{sat}_r60.csv.gz"), index=False)
        T = pd.concat(H60[sat], ignore_index=True) if H60[sat] else pd.DataFrame()
        rec = {"hucre": _fk_hucre_json(T)}
        if len(T):
            yon = "-" if sat.startswith("SM") or sat.startswith("K_SM") else "+"
            e = FO.fo_etiket(T, yon)
            rec["etiket"] = {k: v for k, v in e.items()}
        sonuc["r60"][sat] = rec
    for sat in FK_ESIK["r20_satir"]:
        Ol = pd.concat([o for o in OL20[sat] if len(o)], ignore_index=True) if any(len(o) for o in OL20[sat]) else pd.DataFrame()
        OL20[sat] = Ol
        if len(Ol):
            Ol.to_csv(os.path.join(FK_YOL["satir"], f"olay_{sat}_r20.csv.gz"), index=False)
        T = pd.concat(H20[sat], ignore_index=True) if H20[sat] else pd.DataFrame()
        sonuc["r20"][sat] = {"hucre": _fk_hucre_json(T.drop(columns=[c for c in T.columns if c.startswith("_")], errors="ignore") if len(T) else T)}
    # karşılaştırmalar (hücre: pazar x dönem) + havuz 'TÜM 2023-26' bilgi
    hucreler = [(p, d) for p in OC.OC_ESIK["pazar"] for d, _a, _b in OC.OC_ESIK["donem"]]

    def karsilastir(A: pd.DataFrame, B: pd.DataFrame, kol: str, yon: str, donus=None) -> Dict[str, Any]:
        out = {}
        for p, d in hucreler + [("TÜM", "2023-26")]:
            if p == "TÜM":
                a = A[A.donem.isin(["2023", "2024-26"])] if len(A) else A; b = B[B.donem.isin(["2023", "2024-26"])] if len(B) else B
            else:
                a = A[(A.pazar == p) & (A.donem == d)] if len(A) else A; b = B[(B.pazar == p) & (B.donem == d)] if len(B) else B
            if donus is not None:
                a = donus(a); b = donus(b)
            va = a[kol].to_numpy(float) if len(a) else np.array([]); vb = b[kol].to_numpy(float) if len(b) else np.array([])
            r = fk_fark_boot(va, _fk_ay(a.giris) if len(a) else np.array([]), vb, _fk_ay(b.giris) if len(b) else np.array([]))
            r["durum"] = fk_ayrisma(r, yon)
            out[f"{p} {d}"] = r
        return out
    for sat, kon in (("SP_ic", "K_SP"), ("SP_ic", "K_SP_r"), ("SM_ic", "K_SM"), ("SM_ic", "K_SM_r"), ("SPg_ic", "K_SP"), ("SPs_ic", "K_SP"),
                     ("SPk_ic", "K_SP"), ("SPD", "K_SP"), ("SPD", "K_DUZ"), ("SPD07", "K_DUZ"), ("SPD15", "K_DUZ"), ("SPDb", "K_DUZb")):
        yon = "-" if sat.startswith("SM") else "+"
        c = karsilastir(OL60[sat], OL60[kon], "fark", yon)
        sonuc["h1b"][f"{sat}-{kon}"] = {"hucre": c, "genel": fk_ayrisma_genel({k: v["durum"] for k, v in c.items()})}
    for sat, kon in (("SP_ic", "K_SP"), ("SM_ic", "K_SM"), ("SPD", "K_DUZ")):
        yon = "-" if sat.startswith("SM") else "+"
        c = karsilastir(OL20[sat], OL20[kon], "fark", yon)
        sonuc["h3_r20b"][f"{sat}-{kon}"] = {"hucre": c, "genel": fk_ayrisma_genel({k: v["durum"] for k, v in c.items()})}

    def kir_gost(hedef: str, kol: str = "kirilim"):
        def f(x):
            if not len(x):
                return x
            x = x[~x[kol].isin(["OLCULMEZ", "UYGULANMAZ"])].copy(); x["_g"] = (x[kol] == hedef).astype(float)
            return x
        return f
    for sat, kon, hedef in (("SP_ic", "K_SP", "YUKARI"), ("SP_ic", "K_SP_r", "YUKARI"), ("SM_ic", "K_SM", "ASAGI"), ("SM_ic", "K_SM_r", "ASAGI"),
                            ("SP_ic", "K_SP", "ASAGI"), ("SM_ic", "K_SM", "YUKARI")):
        c = karsilastir(OL60[sat], OL60[kon], "_g", "+", kir_gost(hedef))
        ana = (sat, hedef) in (("SP_ic", "YUKARI"), ("SM_ic", "ASAGI"))
        sonuc["h3_kir"][f"{sat}-{kon} {hedef}"] = {"hucre": c, "genel": fk_ayrisma_genel({k: v["durum"] for k, v in c.items()}),
                                                   "ana": ana and kon in ("K_SP", "K_SM")}
    # EK: S+DÜZ kırılımı 10 mumluk pencere kutusuyla (S6 kutusu taban dışında yok): 'dip kırılmadan önce yukarı' (YUKARI) oranı
    for sat, kon in (("SPD", "K_SP"), ("SPD", "K_DUZ"), ("SPD07", "K_DUZ"), ("SPD15", "K_DUZ"), ("SPDb", "K_DUZb"), ("SP_ic", "K_SP")):
        c = karsilastir(OL60[sat], OL60[kon], "_g", "+", kir_gost("YUKARI", "kirilim10"))
        sonuc["h3_kir"][f"{sat}-{kon} YUKARI (10 mum kutu)"] = {"hucre": c, "genel": fk_ayrisma_genel({k: v["durum"] for k, v in c.items()}),
                                                                "ana": False, "ek": True}
    # kırılım dağılımı (bilgi)
    sonuc["h3_kir_dagilim"] = {}
    for sat, kol in [(x, "kirilim") for x in ("SP_ic", "K_SP", "K_SP_r", "SM_ic", "K_SM", "K_SM_r", "SPg_ic", "SPs_ic", "SPk_ic")] + \
                    [(x, "kirilim10") for x in ("SPD", "SPD07", "SPD15", "K_DUZ", "SPDb", "K_DUZb", "SP_ic", "K_SP")]:
        Ol = OL60[sat]
        if not len(Ol) or kol not in Ol:
            continue
        d_ = {}
        for p, d in hucreler:
            x = Ol[(Ol.pazar == p) & (Ol.donem == d) & ~Ol[kol].isin(["OLCULMEZ", "UYGULANMAZ"])]
            d_[f"{p} {d}"] = {"n": int(len(x)), **{k: float((x[kol] == k).mean()) if len(x) else None for k in ("YUKARI", "ASAGI", "YOK")}}
        sonuc["h3_kir_dagilim"][sat + ("" if kol == "kirilim" else " (10 mum kutu)")] = d_
    # once20 (cetvel, 60 gün +%20 önce -%10) olay vs eş (bilgi; genel S+ dahil)
    for sat in ("SP_ic", "SP_dis", "SP_tum", "K_SP", "SM_ic", "SM_tum", "K_SM"):
        Ol = OL60[sat]; d_ = {}
        if len(Ol) and "once20" in Ol:
            for p, d in hucreler:
                x = Ol[(Ol.pazar == p) & (Ol.donem == d)]
                g = x[["once20", "es_once20"]].dropna()
                d_[f"{p} {d}"] = {"n": int(len(g)), "olay": float(g.once20.mean()) if len(g) else None,
                                  "es": float(g.es_once20.mean()) if len(g) else None}
        sonuc["once20"][sat] = d_
    sonuc["sure_sn"] = round(time.time() - t0, 1)
    metin = json.dumps(sonuc, ensure_ascii=False, indent=1, default=str)
    _fk_sizinti(metin, "sonuç")
    with open(_fk_yol("sonuc", cikti), "w", encoding="utf-8") as f:
        f.write(metin)
    fklog.info("halka_sonuc.json yazıldı (%.0f sn)", time.time() - t0)
    return sonuc


# ================================================================ 6) HALKA 2: KÖR SET
def fk_kor_sec(X: pd.DataFrame, Vlen: Dict[Tuple[str, str], pd.DataFrame]) -> List[Dict[str, Any]]:
    """X: durum günleri (pazar BIST / ABD; satir SP_ic / SP_dis / SM_tum). Vlen: (pazar, sembol) -> veri. Önceden yazılı seçim (tohum)."""
    K = FK_ESIK["kor"]; rng = np.random.default_rng(K["tohum"]); kul: set = set(); sec = []
    X = X[(X.tarih >= pd.Timestamp(K["bas"])) & (X.tarih <= pd.Timestamp(K["son"]))]
    for grup, satir in (("SP_ic", "SP_ic"), ("SP_dis", "SP_dis"), ("SM", "SM_tum"), ("SPD", "SPD")):
        for pz in ("ABD", "BIST"):
            n = K["grup"][grup][pz]
            h = X[(X.satir == satir) & (X.pazar == pz)].reset_index(drop=True)
            if len(h):
                gec = np.array([int(Vlen[(pz, s)].index.get_loc(t)) + 1 >= K["once"] + K["pencere"] for s, t in zip(h.sembol, h.tarih)])
                h = h[gec].reset_index(drop=True)
            sira = rng.permutation(len(h)); k = 0
            for i in sira:
                if k >= n:
                    break
                r = h.iloc[int(i)]
                if (pz, r.sembol) in kul:
                    continue
                kul.add((pz, r.sembol)); k += 1
                sec.append({"grup": grup, "pazar": pz, "sembol": str(r.sembol), "tarih": str(pd.Timestamp(r.tarih).date())})
            if k < n:
                raise FKHata(f"kör set: {grup} {pz} için yeterli aday yok ({k} < {n})")
    sira = rng.permutation(len(sec))
    return [dict(sec[int(i)], no=j + 1) for j, i in enumerate(sira)]


def fk_kor_sonuc(d: pd.DataFrame, t: pd.Timestamp, Z: Optional[pd.DataFrame]) -> Dict[str, Any]:
    """Anahtar için sonuç (PDF'te YOK): r20 / r60 (t+1 açılış girişi, 19 / 59 geçerli bar sonra kapanış), taban içiyse kırılım."""
    i = int(d.index.get_loc(t)); O, C = d.Open.to_numpy(float), d.Close.to_numpy(float); out: Dict[str, Any] = {}
    for ad, h in (("r20", 20), ("r60", 60)):
        out[ad] = float(C[i + h] / O[i + 1] - 1) if i + h < len(C) else None
    ic = Z is not None and t in Z.index and bool(Z.loc[t, "ic"])
    out["taban_ici"] = bool(ic)
    K = FK_ESIK["h3"]["kirilim"]
    out["kirilim"] = fk_kirilim(C, i, float(Z.loc[t, "ust"]), float(Z.loc[t, "alt"]), K["ufuk"], K["asagi_carpan"]) if ic else "UYGULANMAZ"
    return out


def fk_kor_ciz(ax, axh, w: pd.DataFrame, pencere: int, ref: float, etiket: bool = False) -> None:
    """Mum grafiği: w = çizilecek barlar (sonrası yok); son 'pencere' mum gri zemin; y oransal (ref = pencereden önceki son kapanış)."""
    K = FK_CIZIM
    x = np.arange(len(w)); O, H, L, C = (w[c].to_numpy(float) / ref - 1 for c in ("Open", "High", "Low", "Close"))
    yuk = C >= O; r = np.where(yuk, K["yesil"], K["kirmizi"])
    ax.vlines(x, L * 100, H * 100, color=r, lw=1.1, zorder=2)
    gov = np.abs(C - O) * 100; asg = max(0.0015 * 100, 0.004 * float(np.nanmax(H - L) * 100))
    ax.bar(x, np.maximum(gov, asg), bottom=np.minimum(O, C) * 100 - np.where(gov < asg, asg / 2, 0), color=r, width=0.62, zorder=3, linewidth=0)
    ax.axvspan(len(w) - pencere - 0.5, len(w) - 0.5, color=K["zemin"], alpha=0.15, zorder=0)
    alt, ust = float(np.nanmin(L) * 100), float(np.nanmax(H) * 100); pay = (ust - alt) * 0.06 or 1.0
    ax.set_ylim(alt - pay, ust + pay); ax.set_xlim(-0.8, len(w) - 0.2)
    ax.yaxis.set_major_formatter(_fk_yuzde_bicim()); ax.tick_params(axis="y", labelsize=8)
    ax.grid(axis="y", color="#dddddd", lw=0.5)
    axh.bar(x, w.Volume.to_numpy(float), color=r, alpha=0.45, width=0.62, linewidth=0)
    axh.axvspan(len(w) - pencere - 0.5, len(w) - 0.5, color=K["zemin"], alpha=0.15, zorder=0)
    axh.set_xlim(-0.8, len(w) - 0.2); axh.set_yticks([])
    for a in (ax, axh):
        for s_ in ("top", "right"):
            a.spines[s_].set_visible(False)
    if etiket:
        ix = list(range(0, len(w), 5))
        axh.set_xticks(ix); axh.set_xticklabels([w.index[i].strftime("%d.%m") for i in ix], fontsize=7)
        ax.set_xticks([])
    else:
        ax.set_xticks([]); axh.set_xticks([])


def _fk_yuzde_bicim():
    from matplotlib.ticker import FuncFormatter
    return FuncFormatter(lambda v, _p: f"{v:+.0f}%".replace("+0%", "0%"))


def fk_kor_sayfa(d: pd.DataFrame, t: pd.Timestamp, no: int):
    """Kör sayfa figürü: t'de biten pencere + öncesi; adsız, tarihsiz, sonrası yok. Döner: matplotlib Figure."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    K = FK_ESIK["kor"]; i = int(d.index.get_loc(pd.Timestamp(t)))
    w = d.iloc[i - K["once"] - K["pencere"] + 1:i + 1]
    if len(w) != K["once"] + K["pencere"] or w.index[-1] != pd.Timestamp(t):
        raise FKHata(f"kör sayfa {no}: pencere eksik")
    ref = float(w.Close.iloc[K["once"] - 1])
    fig = plt.figure(figsize=(11.69, 8.27))
    ax = fig.add_axes([0.07, 0.30, 0.90, 0.58]); axh = fig.add_axes([0.07, 0.10, 0.90, 0.17])
    fk_kor_ciz(ax, axh, w, K["pencere"], ref)
    fig.text(0.07, 0.94, f"No {no}", fontsize=22, weight="bold", color=FK_CIZIM["baslik"])
    fig.text(0.30, 0.945, "gri zemin = değerlendirilecek 10 mum (sağ kenar = son gün; sonrası gösterilmez)", fontsize=10, color="#555555")
    fig.text(0.07, 0.04, "Yanıt: E = benim mumum (alt fitil küçük / yok, üst fitil kısa-uzun, has yukarı çıkma öbeği) · H = değil · B = belirsiz",
             fontsize=10, color="#333333")
    return fig


def _fk_metinler(fig) -> List[str]:
    """Figürdeki bütün metinler (test: ad / tarih sızıntısı)."""
    out = [t.get_text() for t in fig.texts]
    for a in fig.axes:
        out += [a.get_title()] + [t.get_text() for t in a.texts] + [t.get_text() for t in a.get_xticklabels()] + \
               [t.get_text() for t in a.get_yticklabels()]
    return out


def _fk_dgxx(K: Dict[str, Any]) -> Optional[pd.DataFrame]:
    try:
        import yfinance as yf
        d = yf.download("DGXX", start="2025-01-01", end="2026-11-17", progress=False, auto_adjust=False)
    except Exception as ex:   # ağ / paket yoksa kalibrasyon sayfası 'veri yok' yazar
        fklog.warning("DGXX indirilemedi: %s", ex); return None
    if d is None or not len(d):
        return None
    if isinstance(d.columns, pd.MultiIndex):
        d.columns = d.columns.get_level_values(0)
    d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float)
    d.index = pd.DatetimeIndex(d.index).tz_localize(None).normalize()
    d = d[d.index < pd.Timestamp("2026-11-16")]                   # K3: 16 Kas seans içi yarım bar atılır
    ok = np.isfinite(d).all(axis=1) & (d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0) & (d.Low > 0)
    return d[ok]


def fk_kalibrasyon(ad: str, d: Optional[pd.DataFrame]) -> Dict[str, Any]:
    """Adlı kalibrasyon: pencere [bas, son] barları için fitil payları, k=10 S+ / S-, taban içi; pencere özeti."""
    K = FK_ESIK["kalibrasyon"][ad]; fy = FO.FO_ESIK["fitil_yok"]
    if d is None or not len(d):
        return {"ad": ad, "not": "veri yok"}
    B = FO.fo_bar(d); P = FO.fo_pencere(B, FO.FO_ESIK["k_ana"])
    try:
        Z = fk_hisse(d)
    except Exception as ex:   # S6 kısa seri
        fklog.warning("%s S6 hesaplanamadı: %s", ad, ex); Z = None
    m = (B.index >= pd.Timestamp(K["bas"])) & (B.index <= pd.Timestamp(K["son"]))
    Bw = B[m]; Pw = P[m]
    gun = []
    for t in Bw.index:
        o = d.loc[t]; R = float(o.High - o.Low)
        gun.append({"tarih": str(t.date()), "alt": round(float(B.loc[t, "alt"]), 2), "ust": round(float(B.loc[t, "ust"]), 2),
                    "konum": round(float((o.Close - o.Low) / R), 2), "yesil": bool(o.Close > o.Open),
                    "ASIM": round(float(P.loc[t, "ASIM"]), 3), "ALTYOK": round(float(P.loc[t, "ALTYOK"]), 2),
                    "USTYOK": round(float(P.loc[t, "USTYOK"]), 2), "SP": bool(FO.fo_kural(P.loc[[t]], "SP").iloc[0]),
                    "SM": bool(FO.fo_kural(P.loc[[t]], "SM").iloc[0]),
                    "ic": bool(Z.loc[t, "ic"]) if Z is not None else None, "olculur": bool(Z.loc[t, "olculur"]) if Z is not None else None,
                    "SPg": bool(Z.loc[t, "SPg"]) if Z is not None else None, "SPs": bool(Z.loc[t, "SPs"]) if Z is not None else None,
                    "SPk": bool(Z.loc[t, "SPk"]) if Z is not None else None,
                    "duz": round(float(Z.loc[t, "duz_oran"]), 2) if Z is not None and np.isfinite(Z.loc[t, "duz_oran"]) else None,
                    "dipb": bool(Z.loc[t, "dipb"]) if Z is not None else None,
                    "SPD": bool(Z.loc[t, "SP"] and Z.loc[t, "duz"] and Z.loc[t, "dipb"] and Z.loc[t, "olculur"]) if Z is not None else None})
    ozet = {"bar": int(len(Bw)), "alt_yok_payi": float((Bw.alt < fy).mean()), "ust_yok_payi": float((Bw.ust < fy).mean()),
            "alt_medyan": float(Bw.alt.median()), "ust_medyan": float(Bw.ust.median()),
            "konum_medyan": float(np.median([g["konum"] for g in gun])), "yesil_payi": float(np.mean([g["yesil"] for g in gun])),
            "SP_gun": [g["tarih"] for g in gun if g["SP"]], "SM_gun": [g["tarih"] for g in gun if g["SM"]],
            "ic_gun": [g["tarih"] for g in gun if g["ic"]], "asim_min": float(Pw.ASIM.min()), "asim_maks": float(Pw.ASIM.max()),
            "asim_ort": float(Pw.ASIM.mean()), "SPg_gun": [g["tarih"] for g in gun if g["SPg"]],
            "SPs_gun": [g["tarih"] for g in gun if g["SPs"]], "SPk_gun": [g["tarih"] for g in gun if g["SPk"]],
            "SPD_gun": [g["tarih"] for g in gun if g["SPD"]], "dipb_gun": int(sum(1 for g in gun if g["dipb"])),
            "duz_medyan": float(np.median([g["duz"] for g in gun if g["duz"] is not None])) if any(g["duz"] is not None for g in gun) else None,
            "duz_min": float(min(g["duz"] for g in gun if g["duz"] is not None)) if any(g["duz"] is not None for g in gun) else None}
    if K.get("son_alt") and Z is not None:
        ma = (Z.index > pd.Timestamp(K["son"])) & (Z.index <= pd.Timestamp(K["son_alt"]))
        ozet["son_alt"] = K["son_alt"]; ozet["SP_gun_alt_ek"] = [str(t.date()) for t in Z.index[ma & Z.SP.to_numpy(bool)]]
        ozet["ic_gun_alt_ek"] = [str(t.date()) for t in Z.index[ma & Z.ic.to_numpy(bool)]]
    return {"ad": ad, "sembol": K.get("sembol", ad), "pazar": K["pazar"], "bas": K["bas"], "son": K["son"], "kaynak": K["kaynak"], "gun": gun,
            "ozet": ozet}


def fk_kalibrasyon_sayfa(d: pd.DataFrame, kal: Dict[str, Any]):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    Kk = FK_ESIK["kor"]; g = kal["gun"]; n = len(g)
    i = int(d.index.get_loc(pd.Timestamp(g[-1]["tarih"])))
    w = d.iloc[max(0, i - Kk["once"] - n + 1):i + 1]
    ref = float(w.Close.iloc[len(w) - n - 1])
    fig = plt.figure(figsize=(11.69, 8.27))
    ax = fig.add_axes([0.07, 0.42, 0.90, 0.46]); axh = fig.add_axes([0.07, 0.30, 0.90, 0.10])
    fk_kor_ciz(ax, axh, w, n, ref, etiket=True)
    o = kal["ozet"]
    fig.text(0.07, 0.94, f"KALİBRASYON — {kal['sembol']} ({kal['pazar']}) {kal['bas']} .. {kal['son']}", fontsize=16, weight="bold",
             color=FK_CIZIM["vurgu"])
    fig.text(0.07, 0.905, "Kör sete girmez. Gri zemin = senin pencerenin mumları; altta kodun her mum için hesapladığı fitil payları ve bayraklar "
             "(g = gevşek S+, s = sıkı S+, k = küçük mumlu S+, D = S+DÜZ; düz dip = 10 mum Low yayılımı / medyan mum boyu, <= 1,0 düz; İÇ = S6 taban içi).",
             fontsize=9, color="#555555")
    ax2 = fig.add_axes([0.07, 0.06, 0.90, 0.22]); ax2.set_xlim(-0.8, len(w) - 0.2); ax2.set_ylim(-1.4, 6.6); ax2.axis("off")
    x0 = len(w) - n
    satirlar = [("alt fitil", "alt"), ("üst fitil", "ust"), ("kapanış konumu", "konum"), ("ASIM (k10)", "ASIM"), ("düz dip (k10)", "duz"),
                ("S+ / S-", None), ("varyant g/s/k/D", "var"), ("taban içi", "ic")]
    for k, (ad, kol) in enumerate(satirlar):
        y = 6 - k
        ax2.text(x0 - 1.0, y, ad, fontsize=7, ha="right", va="center", color="#333333")
        for j, gg in enumerate(g):
            if kol is None:
                v = "S+" if gg["SP"] else ("S-" if gg["SM"] else "·")
                renk = FK_CIZIM["yesil"] if gg["SP"] else (FK_CIZIM["kirmizi"] if gg["SM"] else "#999999")
            elif kol == "var":
                v = "".join(c for c, f in (("g", gg.get("SPg")), ("s", gg.get("SPs")), ("k", gg.get("SPk")), ("D", gg.get("SPD"))) if f) or "·"
                renk = "#1f2a44"
            elif kol == "ic":
                v = "-" if gg["ic"] is None else ("İÇ" if gg["ic"] else "·"); renk = "#1f2a44"
            elif gg.get(kol) is None:
                v = "-"; renk = "#999999"
            else:
                v = f"{gg[kol]:.2f}"; renk = "#333333"
                if kol == "alt" and gg[kol] < FO.FO_ESIK["fitil_yok"]:
                    renk = FK_CIZIM["yesil"]
            ax2.text(x0 + j, y, v, fontsize=6, ha="center", va="center", color=renk, rotation=90 if kol not in (None, "ic", "var") else 0)
    ozet = (f"Pencere {o['bar']} mum: alt fitilsiz (< 0,10) mum payı {o['alt_yok_payi']:.2f} · üst fitilsiz payı {o['ust_yok_payi']:.2f} · "
            f"alt fitil medyan {o['alt_medyan']:.2f} · üst fitil medyan {o['ust_medyan']:.2f} · kapanış konumu medyan {o['konum_medyan']:.2f} · "
            f"yeşil payı {o['yesil_payi']:.2f} · ASIM {o['asim_min']:+.2f} .. {o['asim_maks']:+.2f} · S+ gün {len(o['SP_gun'])} · S- gün "
            f"{len(o['SM_gun'])} · taban içi gün {len(o['ic_gun'])} · düz dip medyan {(o['duz_medyan'] or float('nan')):.2f} · S+DÜZ gün "
            f"{len(o['SPD_gun'])}").replace(".", ",")
    fig.text(0.07, 0.02, ozet, fontsize=8, color="#1f2a44")
    return fig


def fk_kor(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or FK_YOL["cikti"]; ok = fk_kapi(cikti, git, kontrol)
    if os.path.exists(_fk_yol("anahtar", cikti)):
        raise FKHata("kor_anahtar.json var: kör set bir kez üretilir (tohum sabit); yeniden üretmek için dosyayı bilerek sil")
    Xs, VV, ZZs = [], {}, {}
    for p in FK_ESIK["kor"]["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or FK_YOL["veri"])
        X, ZZ = fk_sinyaller(Vd, p)
        Xs.append(X[X.satir.isin(["SP_ic", "SP_dis", "SM_tum", "SPD"])])
        for s, d in Vd["V"].items():
            VV[(p, s)] = d
        for s, z in ZZ.items():
            ZZs[(p, s)] = z
        if p == "BIST":
            VB = Vd["V"]
        del Vd
    X = pd.concat(Xs, ignore_index=True)
    sec = fk_kor_sec(X, VV)
    for e in sec:
        e.update(fk_kor_sonuc(VV[(e["pazar"], e["sembol"])], pd.Timestamp(e["tarih"]), ZZs.get((e["pazar"], e["sembol"]))))
    kal = {k: ((_fk_dgxx(v) if k == "DGXX" else VB.get(v.get("sembol", k))), None) for k, v in FK_ESIK["kalibrasyon"].items()}
    kal_sonuc = {k: fk_kalibrasyon(k, d) for k, (d, _) in kal.items()}
    yol = _fk_yol("pdf", cikti); sayfa = 0
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=(11.69, 8.27))
        nk = len(FK_ESIK["kalibrasyon"])
        fig.text(0.07, 0.92, f"FİTİL ÖBEĞİ — KÖR SET ({len(sec)} grafik) + {nk} kalibrasyon sayfası", fontsize=18, weight="bold", color=FK_CIZIM["baslik"])
        for k_, s_ in enumerate([
                f"Sayfa 2-{1 + nk}: KALİBRASYON (adlı, tarihli; kör sete girmez): PAPIL, TEHOL (Mayıs 2025), TEHOL (Mart-Mayıs 2025 bağlam), BINBN, DGXX; "
                "altta kodun mum mum fitil payları.",
                f"Sonraki {len(sec)} sayfa: No 1 .. No {len(sec)}. Her grafik: gri zemin = 10 mum (sağ kenar = son gün) + öncesi 40 mum. SONRASI YOK.",
                "Hisse adı, tarih, pazar ve fiyat rakamı yok; fiyat ekseni oransal (gri zeminden önceki son kapanış = %0); hacim altta.",
                "Her numaraya bir harf yaz: E = benim mumum (alt fitil küçük / yok, üst fitil kısa, has yukarı çıkma öbeği), H = değil, B = belirsiz.",
                f"Yanıt biçimi: 1:E, 2:H, 3:B, ... ({len(sec)} numaranın hepsi). Anahtar ayrı dosyada; sen işaretlemeden açılmaz.",
                "Bu set yalnız şunu ölçer: kodun 'S+' dediği mum öbeği senin gözündeki öbek mi (algılama). Sonuç / getiri bu sette yok."]):
            fig.text(0.07, 0.84 - k_ * 0.05, s_, fontsize=11, va="top")
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        for k, (d, _) in kal.items():
            if d is None or "gun" not in kal_sonuc[k]:
                fig = plt.figure(figsize=(11.69, 8.27)); fig.text(0.07, 0.9, f"KALİBRASYON — {k}: veri yok", fontsize=16)
            else:
                fig = fk_kalibrasyon_sayfa(d, kal_sonuc[k])
            pdf.savefig(fig); plt.close(fig); sayfa += 1
        for e in sorted(sec, key=lambda z: z["no"]):
            fig = fk_kor_sayfa(VV[(e["pazar"], e["sembol"])], pd.Timestamp(e["tarih"]), e["no"])
            m = " ".join(_fk_metinler(fig))
            if e["sembol"] in m or e["tarih"][:4] in m:
                raise FKHata(f"kör sayfa {e['no']}: ad / tarih sızıntısı")
            pdf.savefig(fig); plt.close(fig); sayfa += 1
    anahtar = {"surum": FK_SURUM, "uyari": "GİZLİ: Cemal işaretlemeden açılmaz; PDF'te bu bilgiler yok", "onkayit": ok,
               "fk_esik_sha": fk_esik_sha(), "pdf_sha": _fk_sha_dosya(yol), "pdf_sayfa": sayfa, "kor_sayfa_ofset": 1 + len(FK_ESIK["kalibrasyon"]),
               "sayfalar": sorted(sec, key=lambda z: z["no"]), "kalibrasyon": kal_sonuc}
    metin = json.dumps(anahtar, ensure_ascii=False, indent=1, default=str)
    _fk_sizinti(metin, "anahtar")
    with open(_fk_yol("anahtar", cikti), "w", encoding="utf-8") as f:
        f.write(metin)
    fklog.info("kör set: %s (%d sayfa), anahtar yazıldı", yol, sayfa)
    return {"pdf": yol, "sayfa": sayfa, "kalibrasyon": kal_sonuc}


# ================================================================ 7) DEĞERLENDİRME (Cemal'in yanıtı)
def fk_cevap_ayristir(metin: str, n: int = 50) -> Dict[int, str]:
    out: Dict[int, str] = {}
    for parca in re.split(r"[,;\s]+", metin.strip()):
        if not parca:
            continue
        m = re.fullmatch(r"(\d{1,3})\s*[:=]\s*([EeHhBb])", parca)
        if not m:
            raise FKHata(f"yanıt parçası okunamadı: '{parca}' (biçim 1:E,2:H,3:B)")
        k = int(m.group(1))
        if not 1 <= k <= n:
            raise FKHata(f"numara {k} 1..{n} dışında")
        if k in out:
            raise FKHata(f"numara {k} iki kez")
        out[k] = m.group(2).upper()
    eksik = [k for k in range(1, n + 1) if k not in out]
    if eksik:
        raise FKHata(f"yanıtı olmayan numara: {eksik}")
    return out


def fk_fisher(a: int, b: int, c: int, d: int) -> float:
    """2x2 [[a, b], [c, d]] iki yanlı Fisher kesin p (olasılığı gözlenenden küçük-eşit tablolar)."""
    n1, n2, k, N = a + b, c + d, a + c, a + b + c + d

    def pr(x):
        return math.comb(n1, x) * math.comb(n2, k - x) / math.comb(N, k)
    p0 = pr(a); lo, hi = max(0, k - n2), min(k, n1)
    return float(min(1.0, sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p0 * (1 + 1e-9))))


def fk_olc(cevap: str, cikti: Optional[str] = None) -> Dict[str, Any]:
    A = json.load(open(_fk_yol("anahtar", cikti), encoding="utf-8"))
    S = A["sayfalar"]; c = fk_cevap_ayristir(cevap, len(S)); K = FK_ESIK["kor"]

    def pay(grp):
        x = [c[e["no"]] for e in S if grp(e)]
        e_, h_, b_ = x.count("E"), x.count("H"), x.count("B")
        return {"n": len(x), "E": e_, "H": h_, "B": b_, "E_payi": e_ / len(x) if x else None,
                "E_payi_B_haric": e_ / (e_ + h_) if (e_ + h_) else None}
    spg = ("SP_ic", "SP_dis")
    out = {"SP": pay(lambda e: e["grup"] in spg), "SM": pay(lambda e: e["grup"] == "SM"), "SP_ic": pay(lambda e: e["grup"] == "SP_ic"),
           "SPD": pay(lambda e: e["grup"] == "SPD"),
           "SP_dis": pay(lambda e: e["grup"] == "SP_dis"), "BIST": pay(lambda e: e["pazar"] == "BIST" and e["grup"] in spg),
           "ABD": pay(lambda e: e["pazar"] == "ABD" and e["grup"] in spg)}
    sp, sm = out["SP"], out["SM"]
    out["fisher_SP_SM"] = fk_fisher(sp["E"], sp["n"] - sp["E"], sm["E"], sm["n"] - sm["E"])
    out["fisher_ic_dis"] = fk_fisher(out["SP_ic"]["E"], out["SP_ic"]["n"] - out["SP_ic"]["E"], out["SP_dis"]["E"],
                                     out["SP_dis"]["n"] - out["SP_dis"]["E"])
    fpay = sp["E_payi"] - sm["E_payi"]
    out["karar"] = ("ALGILAMA SAĞLAM" if sp["E_payi"] >= 0.60 and fpay >= 0.30 else "ALGILAMA KIRIK" if sp["E_payi"] < 0.40 else "KISMİ")
    # bilgi: Cemal'in E dediği vs demediği S+ sayfalarında sonuç (n küçük; bulgu değil)
    bil = {}
    for etk in ("E", "H", "B"):
        x = [e for e in S if e["grup"] != "SM" and c[e["no"]] == etk]   # S+ ve S+DÜZ sayfaları
        r20 = [e["r20"] for e in x if e.get("r20") is not None]; r60 = [e["r60"] for e in x if e.get("r60") is not None]
        kir = [e["kirilim"] for e in x if e.get("kirilim") in ("YUKARI", "ASAGI", "YOK")]
        bil[etk] = {"n": len(x), "r20_medyan": float(np.median(r20)) if r20 else None, "r60_medyan": float(np.median(r60)) if r60 else None,
                    "yukari_payi": (kir.count("YUKARI") / len(kir)) if kir else None, "kir_n": len(kir)}
    out["sonuc_bilgi"] = bil; out["kural"] = K["karar"]
    return out


# ================================================================ 8) RAPOR
def _yz(x: Any, n: int = 1) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{100 * x:+.{n}f}%".replace(".", ",")


def _sy(x: Any, n: int = 2) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


_FK_HUC = ["ABD 2023", "ABD 2024-26", "AVR 2023", "AVR 2024-26", "BIST 2023", "BIST 2024-26"]


def _fk_hucre_kisa(h: Dict[str, Any], durum_kol: str = "durum") -> str:
    n = int(h.get("n") or 0)
    if not n:
        return "n 0"
    return f"n {n}, {_yz(h.get('ort_fark'))} [{_yz(h.get('alt95'))}, {_yz(h.get('ust95'))}], sıra {_sy(h.get('sira'))}, {h.get(durum_kol, '')}"


def fk_rapor(cikti: Optional[str] = None, ek: Optional[str] = None) -> str:
    J = json.load(open(_fk_yol("sonuc", cikti), encoding="utf-8")); E = FK_ESIK
    an_yol = _fk_yol("anahtar", cikti); A = json.load(open(an_yol, encoding="utf-8")) if os.path.exists(an_yol) else None
    on = J["onkayit"]
    s = ["# FITIL_KOR — HALKA RAPORU (fitil öbeği: hata nerede?)", "",
         f"Ön kayıt yazım {on.get('onkayit_yazim_utc')} (sha `{on.get('onkayit_sha', '')}`; git: {on.get('git_onkayit') if isinstance(on.get('git_onkayit'), str) else on.get('git_onkayit', {}).get('commit', '-')}); "
         f"iş tanımı git {on['git_is_tanimi']['commit'][:10]} ({on['git_is_tanimi']['commit_zamani']}); koşu {on.get('kos_zaman_utc')}; süre {J.get('sure_sn')} sn. "
         "Geleceğe bakma denetimi: " + ", ".join(f"{p} {v} olay TUTTU" for p, v in J["gelecek_denetimi"].items()) + ".", ""]
    if ek and os.path.exists(ek):
        e_ = open(ek, encoding="utf-8").read()
        i = e_.find("## ÖZET")
        if i >= 0:
            j = e_.find("\n## ", i + 5)
            s += [e_[i:j if j > 0 else None].rstrip(), ""]
    # HALKA 1
    s += ["## HALKA 1 — TANIM BAĞLAMI (S+ yalnız S6 TABAN İÇİNDE)", "",
          "(a) r60 eşli fark (ORTAK_CETVEL; hücre: n, ortalama eşli fark [%95], sıra, durum beklenen yönde). Etiket Ç187 kuralı.", "",
          "| Satır | etiket | " + " | ".join(_FK_HUC) + " |", "|---|---|" + "---|" * len(_FK_HUC)]
    for sat in E["r60_satir"]:
        r = J["r60"].get(sat, {}); hc = {f"{h['pazar']} {h['donem']}": h for h in r.get("hucre", [])}
        yon = "-" if sat.startswith("SM") or sat.startswith("K_SM") else "+"
        par = []
        for k in _FK_HUC:
            h = hc.get(k)
            if not h:
                par.append("-"); continue
            d = FO.fo_durum(h, yon)[0] if int(h.get("n") or 0) else "ÖLÇÜLEMEDİ"
            par.append(_fk_hucre_kisa(dict(h, durum=d)))
        s.append(f"| {sat} | {r.get('etiket', {}).get('genel', '-')} | " + " | ".join(par) + " |")
    s += ["", "(b) taban içi S+ vs taban içi S+ OLMAYAN günler (eşli farkların farkı; iki grup ayrı ay kümeli bootstrap %95). S- ayna.", "",
          "| Karşılaştırma | genel | " + " | ".join(_FK_HUC + ["TÜM 2023-26"]) + " |", "|---|---|" + "---|" * (len(_FK_HUC) + 1)]
    for k, v in J["h1b"].items():
        par = [f"{_yz(h['fark'])} [{_yz(h['alt95'])}, {_yz(h['ust95'])}] ({h['n_a']}/{h['n_b']}) {h['durum']}" for h in
               (v["hucre"].get(x, {}) for x in _FK_HUC + ["TÜM 2023-26"])]
        s.append(f"| {k} | {v['genel']} | " + " | ".join(par) + " |")
    # HALKA 3
    s += ["", "## HALKA 3 — DOĞRULAMA ÖLÇÜSÜ (r20 ve 'önce tavan mı, dip mi')", "",
          "r20 eşli fark (cetvel mekaniği, ufuk 20; 'tutar' bilgi):", "",
          "| Satır | " + " | ".join(_FK_HUC) + " |", "|---|" + "---|" * len(_FK_HUC)]
    for sat in E["r20_satir"]:
        hc = {f"{h['pazar']} {h['donem']}": h for h in J["r20"].get(sat, {}).get("hucre", [])}
        par = []
        for k in _FK_HUC:
            h = hc.get(k)
            par.append(_fk_hucre_kisa(dict(h, durum="TUTAR" if h.get("tutar") else "-")) if h else "-")
        s.append(f"| {sat} | " + " | ".join(par) + " |")
    s += ["", "r20 fark (b):", "", "| Karşılaştırma | genel | " + " | ".join(_FK_HUC + ["TÜM 2023-26"]) + " |", "|---|---|" + "---|" * (len(_FK_HUC) + 1)]
    for k, v in J["h3_r20b"].items():
        par = [f"{_yz(h['fark'])} [{_yz(h['alt95'])}, {_yz(h['ust95'])}] ({h['n_a']}/{h['n_b']}) {h['durum']}" for h in
               (v["hucre"].get(x, {}) for x in _FK_HUC + ["TÜM 2023-26"])]
        s.append(f"| {k} | {v['genel']} | " + " | ".join(par) + " |")
    s += ["", "Kırılım: 60 geçerli bar içinde önce S6 tavanı (kapanış) = YUKARI / önce dip x 0,98 altı (kapanış) = AŞAĞI. Oranlar (n ölçülen olay):", "",
          "| Satır | " + " | ".join(_FK_HUC) + " |", "|---|" + "---|" * len(_FK_HUC)]
    for sat, d_ in J.get("h3_kir_dagilim", {}).items():
        par = [f"n {d_[k]['n']}: Y {_yz(d_[k]['YUKARI'], 0)} / A {_yz(d_[k]['ASAGI'], 0)} / yok {_yz(d_[k]['YOK'], 0)}" if k in d_ and d_[k]["n"] else "-"
               for k in _FK_HUC]
        s.append(f"| {sat} | " + " | ".join(par) + " |")
    s += ["", "Kırılım oran farkı (S+ YUKARI vs kontrol; S- AŞAĞI vs kontrol = ANA; ters yön bilgi):", "",
          "| Karşılaştırma | genel | " + " | ".join(_FK_HUC + ["TÜM 2023-26"]) + " |", "|---|---|" + "---|" * (len(_FK_HUC) + 1)]
    for k, v in J["h3_kir"].items():
        par = [f"{_yz(h['fark'])} [{_yz(h['alt95'])}, {_yz(h['ust95'])}] ({h['n_a']}/{h['n_b']}) {h['durum']}" for h in
               (v["hucre"].get(x, {}) for x in _FK_HUC + ["TÜM 2023-26"])]
        s.append(f"| {k}{' [ANA]' if v.get('ana') else ''} | {v['genel']} | " + " | ".join(par) + " |")
    s += ["", "Genel S+ (tavan / dip yok; bilgi): cetvel once20 (60 günde önce +%20, -%10'dan önce) olay oranı / eş oranı:", "",
          "| Satır | " + " | ".join(_FK_HUC) + " |", "|---|" + "---|" * len(_FK_HUC)]
    for sat, d_ in J.get("once20", {}).items():
        s.append(f"| {sat} | " + " | ".join(f"n {d_[k]['n']}: {_yz(d_[k]['olay'], 0)} / {_yz(d_[k]['es'], 0)}" if k in d_ and d_[k]["n"] else "-"
                                         for k in _FK_HUC) + " |")
    # Cemal örnekleri (bilgi)
    s += ["", "## CEMAL ÖRNEKLERİ (HALKA 1 ve 3; n küçük, BİLGİ)", "",
          "| Örnek | pencere | S+ günleri | gevşek / sıkı / küçük S+ | S- günleri | S6 taban içi günleri |", "|---|---|---|---|---|---|"]
    for r in J.get("cemal_ornek", []):
        if r.get("olay") == "pencere":
            s.append(f"| {r['ornek']} | {r['bas']} .. {r['son']} | {', '.join(r['SP_gun']) or 'yok'} | {len(r['SPg_gun'])} / {len(r['SPs_gun'])} / "
                     f"{len(r['SPk_gun'])} gün | {', '.join(r['SM_gun']) or 'yok'} | {', '.join(r['ic_gun']) or 'YOK (taban açık değil)'} |")
    s += ["", "| Örnek | olay | t | giriş | taban içi | r60 / eşli fark | r20 / eşli fark | kırılım |", "|---|---|---|---|---|---|---|---|"]
    for r in J.get("cemal_ornek", []):
        if r.get("olay") in ("ilk_SP", "son_gun"):
            s.append(f"| {r['ornek']} | {r['olay']} | {r['tarih']} | {r.get('giris') or '-'} | {'EVET' if r['taban_ici'] else 'hayır'} | "
                     f"{_yz(r.get('r60'))} / {_yz(r.get('r60_fark'))} | {_yz(r.get('r20'))} / {_yz(r.get('r20_fark'))} | {r['kirilim']} |")
    # HALKA 2
    s += ["", "## HALKA 2 — ALGILAMA (kör set hazır)", ""]
    if A:
        say = {}
        for e in A["sayfalar"]:
            say[(e["grup"], e["pazar"])] = say.get((e["grup"], e["pazar"]), 0) + 1
        s += [f"- FITIL_KOR_SET.pdf: {A['pdf_sayfa']} sayfa (1 açıklama + {len(A['kalibrasyon'])} kalibrasyon + {len(A['sayfalar'])} kör grafik); PDF sha `{A['pdf_sha']}`.",
              "- Kör grafik dağılımı (anahtar gizli; yalnız sayım): " + ", ".join(f"{g} {p} {n}" for (g, p), n in sorted(say.items())) + ".",
              f"- Değerlendirme komutu: `python FITIL_KOR.py olc --cevap \"1:E,2:H,3:B,...\"` ({len(A['sayfalar'])} numaranın hepsi; E / H / B).",
              f"- Okuma kuralı (önceden yazılı): {E['kor']['karar']}.", "", "Kalibrasyon sayfaları (kodun ölçtüğü):", "",
              "| Hisse | pencere | mum | alt fitilsiz payı | üst fitilsiz payı | alt medyan | üst medyan | kapanış konumu medyan | yeşil payı | ASIM min / maks | S+ gün | S- gün | taban içi gün |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for k, v in A["kalibrasyon"].items():
            if "ozet" not in v:
                s.append(f"| {k} | - | {v.get('not')} |" + " - |" * 10); continue
            o = v["ozet"]
            s.append(f"| {k} | {v['bas']} .. {v['son']} | {o['bar']} | {_sy(o['alt_yok_payi'])} | {_sy(o['ust_yok_payi'])} | {_sy(o['alt_medyan'])} | "
                     f"{_sy(o['ust_medyan'])} | {_sy(o['konum_medyan'])} | {_sy(o['yesil_payi'])} | {_sy(o['asim_min'])} / {_sy(o['asim_maks'])} | "
                     f"{', '.join(o['SP_gun']) or 'yok'} (g/s/k {len(o.get('SPg_gun', []))}/{len(o.get('SPs_gun', []))}/{len(o.get('SPk_gun', []))}) | "
                     f"{', '.join(o['SM_gun']) or 'yok'} | {', '.join(o['ic_gun']) or 'yok'} |")
    else:
        s.append("- Kör set henüz üretilmedi (`python FITIL_KOR.py kor`).")
    s += ["", "## VERİ ve SINIRLAR", ""] + [f"- {p}: {'; '.join(n)}" for p, n in J["veri_not"].items()] + [
          "- Hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, AŞAĞI kırılım oranı aşağı yanlı okunmalı. Komisyon yok; 31.08.2026 sonrası yok.",
          "- r20 hücrelerinde güç tablosu uygulanmaz ('tutar' bilgi). Kırılım yalnız taban içi (tavan / dip tanımlı) olaylarda.", ""]
    onm = open(_fk_yol("onkayit", cikti), encoding="utf-8").read()
    i = onm.find("## KONTROL LİSTESİ")
    if i >= 0:
        s += [onm[i:].split("\n## Test")[0].rstrip(), ""]
    if ek and os.path.exists(ek):
        e_ = open(ek, encoding="utf-8").read(); i = e_.find("## ÖZET"); j = e_.find("\n## ", i + 5) if i >= 0 else -1
        kalan = (e_[:i] + (e_[j:] if j > 0 else "")) if i >= 0 else e_
        s += [kalan.strip(), ""]
    metin = "\n".join(s)
    _fk_sizinti(metin, "rapor")
    with open(_fk_yol("rapor", cikti), "w", encoding="utf-8") as f:
        f.write(metin)
    return metin


# ================================================================ 9) ÇAKIŞMA KAPISI
def _cakisma_kontrol_fk(_once=_CK_ONCE_FK, _dosya="FITIL_KOR.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_FK", "_CK_KAYIT", "_cakisma_kontrol_fk", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "warnings", "_dt", "OC", "FO", "S6", "copy", "math", "zlib",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple", "_yz", "_sy")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_fk()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=FK_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "kor", "rapor", "olc"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--ek", default=None)
    ap.add_argument("--cevap", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true")
    ap.add_argument("--gitsiz", action="store_true", help="ön kayıt git'e işlenmemişse (alt ajan) SAPMA olarak yazıp koş")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(fk_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            fk_kos(a.cikti, a.veri, git=not a.gitsiz)
            print(fk_rapor(a.cikti, a.ek)[:6000])
        elif a.komut == "kor":
            R_ = fk_kor(a.cikti, a.veri, git=not a.gitsiz)
            print(json.dumps({"pdf": R_["pdf"], "sayfa": R_["sayfa"]}, ensure_ascii=False))
        elif a.komut == "rapor":
            print(fk_rapor(a.cikti, a.ek))
        else:
            if not a.cevap:
                raise FKHata("--cevap gerekli: \"1:E,2:H,...\"")
            print(json.dumps(fk_olc(a.cevap, a.cikti), ensure_ascii=False, indent=1, default=str))
    except (FKHata, OC.OCHata, S6.S6Hata) as ex:
        fklog.error("%s", ex); sys.exit(1)
