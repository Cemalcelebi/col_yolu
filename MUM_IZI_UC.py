"""MUM_IZI_UC — MUM_IZI EK 27: UÇLAR. En küçük mumlu ve fitil şartları en radikal bölgeler; 12 ölçü + 4 bileşik, her birinin ucu ve hepsi birden;
rastgele gün tabanı (T1), zamanlama / seçim (PİYASA(t)), hedef payı (+%5 / +%10 stop'tan önce) ve takvim (26 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI27_IS_TANIMI.md (ana model; commit 917e84e). Cemal (26 Kas): "en küçük mumlardan oluşan olanları bulup ölçmek; bütün
zorunlu fitillerin en radikal olan bölgeleri bulup test etmek; her şeyi dene". Bu modül eşikten geçenleri değil, şartların EN UÇ olduğu pencereleri ölçer.

PENCERELER (iki evren; günlük ve haftalık ayrı):
  E1 İSKELET = MUM_IZI8 taramasının R4 VAR, evren içi olayları (M ve mum boyu kapısı OLMADAN; ham dosya /tmp/mum_izi/v5/tarama_ham.json, sha
               mum_izi8_tarama.json ile denetlenir), aynı hissede 15 bar tekil (HV.hv_tekil); pencere = olayın kendi bölgesi (t - m + 1 .. t, m 16-24).
  E2 HER PENCERE = yapı şartı yok; her hissede 16 barlık pencere, pencere sonu t = 135 + 15 k (hissenin kendi bar sırası; önceki 120 bar var), sonuç pencereleri
               (t + 1 .. t + 15) örtüşmez; evren içi = P2 havuzu (MUM_IZI_ETIKET2.e6_p2_maske, MUM_IZI8 taramasıyla aynı; BIST işlem değeri kesit medyanı üstü).
ÖLÇÜLER (12, sürekli, uç yönü sabit) yalnız pencerenin son barına kadarki veriden; bileşikler B1-B4. Kesimler (UÇ10, UÇ2, beşlik) YALNIZ KEŞİF örneğinden
(ABD 2016-19, evren x zaman dilimi başına) hesaplanıp öteki hücrelere aynen uygulanır.
SONUÇ: MUM_IZI_HAVUZ (EK 25) ölçü dizileri AYNEN (hv25_dizi / hv25_uygun / hv25_olc_dizi = GZ.gz_olc_bir tanımı): giriş = pencereden sonraki ilk geçerli bar
açılışı, R15 = 15. mumun kapanışı / giriş - 1, stop = pencere dibi x 0,98, hedef +%5 / +%10 stop'tan önce. T1 = aynı hissenin aynı dönemdeki BÜTÜN uygun giriş
günlerinin R15 ortalaması (stop önceki 16 bar); taban hedef payı = hisse-dönem başına 200 rastgele gün (tohum 27). PİYASA(t) = pazarın bütün hisselerinin aynı
giriş günü açılışından 15 mumluk getirisi (HV.hv25_piyasa_R). Ay kümeli bootstrap (10.000; tohum 27). Hüküm önceden (UC_ESIK['hukum']).
Veri <= 2022-12-31 (assert + KASA kapısı). KASA AÇILMAZ. Mevcut modüller (MUM_IZI*, CETVEL2, ...) DEĞİŞTİRİLMEZ; içe alınır.

Komut:  python MUM_IZI_UC.py appn       APPN sağlaması (MUM_IZI26 SOL / SAĞ elle hesaplanmış değerler; getiri yok)
        python MUM_IZI_UC.py pencere    GETİRİSİZ pencere tabloları (/root/.kasa/ham/mum_izi27/pencere_*.pkl; getiri hesaplanmaz)
        python MUM_IZI_UC.py sayim      GETİRİSİZ SAYIM + keşif kesimleri (/tmp/mum_izi/uc/sayim27.json, kesim27.json)
        python MUM_IZI_UC.py onkayit    MUM_IZI27_ON_KAYIT.md (mühürler + sayım + kesimler + yorum noktaları + kontrol tablosu)
        python MUM_IZI_UC.py kos        kapı (kontrol + ön kayıt sha + commit + temiz ağaç + KASA) -> hesap -> olay satırları + mum_izi27_sonuc.json + özet csv
        python MUM_IZI_UC.py rapor      MUM_IZI27_RAPOR.md tabloları + MUM_IZI27_OZET.png (sonuç json'undan)
        python MUM_IZI_UC.py sha        kod / eşik sha
Colab:  exec(open('MUM_IZI_UC.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7: sonuç yukarı yanlı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_UC = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import time  # noqa: E402
import zlib  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_UC = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_UC not in sys.path:
    sys.path.insert(0, KOK_UC)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAFTALIK as MH  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAVUZ as HV  # noqa: E402  (DEĞİŞTİRİLMEZ; tekil, hücre, kesik, ölçü dizileri, piyasa, BH)
import MUM_IZI_GOZ as GZ  # noqa: E402  (DEĞİŞTİRİLMEZ; gz_olc_bir yeniden üretim denetimi)

uclog = logging.getLogger("col.mum_izi_uc")
if not uclog.handlers:
    _uc_h = logging.StreamHandler(sys.stderr)
    _uc_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_uc: %(message)s", "%H:%M:%S"))
    uclog.addHandler(_uc_h)
    uclog.setLevel(logging.INFO)
    uclog.propagate = False


class UCHata(RuntimeError):
    """Durdurucu hata: kapı / şema / veri / kesik / yeniden üretim uyuşmazlığı."""


UC_SURUM = "MUM_IZI_UC v1.0 (2026-11-26): EK 27 uçlar (12 ölçü + 4 bileşik; E1 iskelet / E2 her pencere; günlük / haftalık)"
_C = MI.MI_YOL["cikti"]
UC_YOL = {"cikti": _C, "kod": os.path.join(KOK_UC, "MUM_IZI_UC.py"), "ham": os.environ.get("UC_HAM", "/root/.kasa/ham/mum_izi27"),
          "gecici": "/tmp/mum_izi/uc", "is_tanimi": os.path.join(_C, "MUM_IZI27_IS_TANIMI.md"), "ham8": HV.HK.HK_YOL["ham8"],
          "tarama8": HV.HK.HK_YOL["tarama8"], "havuz_kod": os.path.join(KOK_UC, "MUM_IZI_HAVUZ.py")}
UC_DOSYA = {"onkayit": "MUM_IZI27_ON_KAYIT.md", "rapor": "MUM_IZI27_RAPOR.md", "sonuc": "mum_izi27_sonuc.json", "ozet": "mum_izi27_ozet.csv",
            "png": "MUM_IZI27_OZET.png"}
UC_KESIK = pd.Timestamp("2022-12-31")
UC_ZAMAN = ("gunluk", "haftalik")
UC_PAZAR = ("ABD", "AVR", "BIST")
UC_EVREN = ("E1", "E2")

# (ad, uç yönü): KUCUK -> uç skoru = -değer; BUYUK -> uç skoru = +değer (skor büyüdükçe uç)
UC_OLCU: List[Tuple[str, str]] = [
    ("BOY_YUZDE_ORAN", "KUCUK"), ("BOY_GRAFIK_ORAN", "KUCUK"), ("BOY_MUTLAK", "KUCUK"), ("GOVDE_ORAN", "KUCUK"), ("GOVDE_BOY", "KUCUK"),
    ("UST_FITIL", "BUYUK"), ("ALT_FITIL", "KUCUK"), ("UST_ALT_PAY", "BUYUK"), ("SON_UST_FITIL", "BUYUK"), ("DARALMA", "KUCUK"),
    ("BANT_SON", "BUYUK"), ("ONCEKI_DUSUS", "KUCUK")]
UC_OLCU_AD = [a for a, _ in UC_OLCU]
UC_BILESIK = {"B1_KUCUK_MUM": UC_OLCU_AD[0:5], "B2_FITIL": UC_OLCU_AD[5:9], "B3_HEPSI": UC_OLCU_AD[0:11],
              "B4_HEPSI_VE": ["BOY_YUZDE_ORAN", "GOVDE_BOY", "UST_FITIL", "ALT_FITIL", "DARALMA", "BANT_SON"]}
UC_SATIR = UC_OLCU_AD + list(UC_BILESIK)            # 16
UC_UC = ("UC10", "UC2")
UC_EK_KOL = ["BANT_SON_ham", "govdesiz_pay", "fiyat_med"]      # bilgi sütunları (hükme girmez)

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
UC_ESIK: Dict[str, Any] = {
    "surum": "UC27-1.0",
    "tohum": 27,
    "tohum_tanim": "np.random.default_rng([27, tür, crc32(anahtar)]); tür 1 = taban hedef payı çekimi (anahtar 'zaman|pazar|sembol|dönem'), 2 = satır "
                   "bootstrap'ı (anahtar satır adı), 3 = takvim bootstrap'ı (anahtar tablo adı); sıra bağımsız, tekrarlanabilir",
    "pencere": {
        "E1": "MUM_IZI8 tarama ham dosyası (HK.hk_olaylar ile aynı dosya, aynı sha denetimi) 'R4' listesi, evren == True (M ve mum boyu kapısı YOK); aynı zaman "
              "dilimi ve hissede bölge sonu bar sırasıyla 15 bar tekil (HV.hv_tekil; son tutulandan < 15 bar sonraki atılır); pencere = olayın bölgesi "
              "t - m + 1 .. t (m 16-24, taramanın kendi m'si); t taramanın bar indeksi (günlük MI.mi_veri açık kopya, haftalık MV.mv_haftalik_panel(MI.mi_veri "
              "tam)); takvimde tarih denetlenir (DUR)",
        "E2": {"uzunluk": 16, "adim": 15, "ilk_son": 135,
               "tanim": "her hissede pencere sonu t = 135 + 15 k (k = 0, 1, ...; hissenin kendi bar sırası, ilk barı 0), pencere t - 15 .. t (16 bar); önceki 120 "
                        "bar t - 135 .. t - 16 hep var; ardışık pencereler bir bar paylaşır, sonuç pencereleri (t + 1 .. t + 15) ÖRTÜŞMEZ; haftalıkta da 16 "
                        "hafta / önceki 120 hafta; pencere sonu tarihi tarama aralığında; evren içi = pencere sonu barında P2 (ABD / AVR: "
                        "MUM_IZI_ETIKET2.e6_p2_maske, e6_parcalar klasörleri; BIST: işlem değeri (Close x Volume) aynı gün / ISO haftası kesit medyanı "
                        "üstü, e6_bist_medyan) — MUM_IZI8 taramasının evren kuralı aynen"},
        "tarama": {"gunluk": ["2016-01-01", "2022-12-31"], "haftalik": ["2001-01-01", "2022-12-31"], "tanim": "pencere SONU tarihi aralıkta (iki evren)"},
        "onceki": 120, "onceki60": 60,
    },
    "atma": {
        "sira": ["ONCEKI_YOK", "BOSLUK", "KILITLI", "EVREN_DISI", "GIRIS_YOK", "UFUK_KESIK", "STOP_UST", "DONEM_DISI", "T1_YOK"],
        "ONCEKI_YOK": "pencere başı s = t - m + 1 için s - 120 < 0 (önceki 120 bar yok)",
        "BOSLUK": "haftalıkta pencerenin 2..m. barında 'bosluk' (önceki haftayla arada boş ISO haftası) var (MUM_IZI8 kuralı)",
        "KILITLI": {"pay": 0.20, "tanim": "pencerenin takvim aralığında (ilk barın ilk günü .. son barın son günü) ham veride GEÇERSİZ olan günlük bar (H <= L, "
                                         "V <= 0, fiyat <= 0 ya da sonlu değil; OC.oc_veri_hazirla 'gecersiz' tarihleri: kilitli / hacimsiz / fiyat adımına "
                                         "yapışmış H = L bar) payı = geçersiz / (geçersiz + geçerli) > 0,20 -> pencere ATILIR (sınır dahil değil)"},
        "EVREN_DISI": "E2'de pencere sonu barı P2 havuzu dışında (E1 olayları taramada zaten evren içi)",
        "GIRIS_YOK": "t + 1 barı yok", "UFUK_KESIK": "t + 15 barı yok ya da tarihi > 2022-12-31 (15 mumluk pencere kesiği aşar)",
        "STOP_UST": "giriş açılışı sonlu > 0 değil ya da <= stop (pencere dibi x 0,98) (gz_olc_bir ölçülebilirliği)",
        "DONEM_DISI": "giriş tarihi hiçbir döneme düşmüyor", "T1_YOK": "aynı hisse aynı dönemde T1 için uygun gün < 30",
        "tanim": "her pencereye ilk tutan neden yazılır; TAMAM = hiçbiri; sayım evren x zaman dilimi x pazar x neden"},
    "olcu": {
        "bar": "rg = H - L; boy = rg / C; govde = |C - O| / C; gb = |C - O| / rg; ust = (H - max(O, C)) / rg; alt = (min(O, C) - L) / rg; Bollinger MI.mi_bant(C) "
               "(SMA 20, 2 x std ddof 0; yalnız o bara kadarki kapanışlar): bw = (BU - BA) / BO, bc = (C - BO) / (BU - BO)",
        "pencere": "W = s .. t (m bar); P = s - 120 .. s - 1; S3 = son tavan(m / 3) bar (16 -> 6, 21 -> 7); P60 = s - 60 .. s - 1; medyan np.median",
        "BOY_YUZDE_ORAN": "med(boy[W]) / med(boy[P])", "BOY_GRAFIK_ORAN": "med(rg[W]) / med(rg[P])", "BOY_MUTLAK": "100 x med(boy[W]) (%)",
        "GOVDE_ORAN": "med(govde[W]) / med(govde[P]) (payda 0 ise yok)", "GOVDE_BOY": "med(gb[W])", "UST_FITIL": "med(ust[W])", "ALT_FITIL": "med(alt[W])",
        "UST_ALT_PAY": "W'de üst fitil (H - max(O, C)) > alt fitil (min(O, C) - L) olan mum payı", "SON_UST_FITIL": "med(ust[S3])",
        "DARALMA": "bw[t] / bw[s] - 1", "BANT_SON": "değer = -|med(bc[S3]) - 0,85| (ham medyan ayrıca 'BANT_SON_ham'); uç BÜYÜK = 0,85'e en yakın",
        "ONCEKI_DUSUS": "100 x (min(L[W]) / max(H[P60]) - 1) (%; uç en derin)",
        "gelecek": "hiçbir ölçü t'den sonraki bar okumaz (test: t sonrası barlar bozulunca ölçüler aynı)"},
    "skor": "uç skoru u = -değer (KUCUK) ya da +değer (BUYUK); u büyüdükçe uç",
    "kesim": {
        "kesif": "ABD|d1619", "orneklem": "evren x zaman dilimi başına keşif hücresinin TAMAM pencereleri (ölçülebilir, T1 var; getirisiz), ölçü sonlu olanlar",
        "UC10": 0.90, "UC2": 0.98, "besli": [0.2, 0.4, 0.6, 0.8],
        "tanim": "UÇ10 <=> u >= keşif u'nun 0,90 yüzdeliği (np.quantile, linear; eşitler dahil); UÇ2 <=> u >= 0,98 yüzdeliği; beşlik = 1 + #{sınır <= u} (5 = en "
                 "uç); kesimler keşif dışındaki hücrelere AYNEN uygulanır (yeniden hesaplanmaz)",
        "bilesik": "B1 / B2 / B3: bileşen ölçülerin keşif ECDF yüzdelikleri p = searchsorted(keşif u sıralı, u, 'right') / n_keşif ortalaması (bileşenlerin hepsi "
                   "sonlu); bileşik değerin UÇ10 / UÇ2 / beşlik kesimleri yine keşiften (aynı kural)",
        "B4": {"UC10": 0.70, "UC2": 0.90,
               "tanim": "B4 HEPSI_VE: ölçü 1, 5, 6, 7, 10, 11'in HER BİRİ kendi uç %30'unda (u_i >= keşif u_i'nin 0,70 yüzdeliği) -> satır 'UC10'; her biri kendi uç "
                        "%10'unda (0,90 yüzdeliği) -> satır 'UC2' (B4'ün ikinci basamağı; iş tanımında tek basamak vardı, aile sayısı 128 için ikinci basamak "
                        "önceden böyle sabit); beşlik: altı bileşen p'sinin EN KÜÇÜĞÜ, keşif beşlikleri"}},
    "sonuc": {
        "olcu": "HV.hv25_olc_dizi AYNEN (= GZ.gz_olc_bir; ufuk 15, stop çarpanı 0,98; giriş t + 1 barı açılışı (haftalıkta haftanın ilk günü); R15 = t + 15 "
                "barının kapanışı / giriş - 1; d5 / d10 = günlük High >= giriş x (1 + x) ilk günü Low <= stop ilk gününden ÖNCE (aynı gün stop önce)); "
                "pencerenin stop'u = pencere dibi (t - m + 1 .. t barlarının Low en küçüğü) x 0,98; denetim: her blokta 200 rastgele pencerede GZ.gz_olc_bir "
                "ile R15 / d5 / d10 birebir (DUR)",
        "T1": {"m": 16, "en_az": 30, "tanim": "aynı hisse, aynı zaman dilimi, aynı dönem (giriş tarihine göre): HV.hv25_uygun(A, 16, haric yok, dönem) uygun "
                                             "BÜTÜN karar barlarının R15 ortalaması (hisse-dönem başına bir kez); uygun < 30 ise pencere T1_YOK"},
        "taban_hedef": {"cekim": 200, "tanim": "aynı hisse-dönemin uygun günlerinden yerine koymadan 200 (az ise hepsi; tohum tür 1) -> d5 / d10 payı; pencere "
                                                "başına taban payı = kendi hisse-döneminin payı; satırda TABAN PAYI = pencerelerin taban paylarının ortalaması; "
                                                "KAT = satırın hedef payı / taban payı"},
        "PIYASA": {"en_az_hisse": 5,
                   "gunluk": "PİYASA(d) = HV.hv25_piyasa_R(M, d, d + 14, haric yok): pazar takviminde (bütün işlem günlerinin birleşimi) d günü açılışında işlem "
                             "gören bütün hisselerin d .. d + 14 son geçerli kapanış / d açılışı - 1 eşit ağırlıklı ortalaması; pencerenin d'si = giriş günü",
                   "haftalik": "PİYASA(w) = hv25_piyasa_R(M, d_w, e_w): d_w = ISO haftası w'nin pazar takvimindeki ilk günü, e_w = w + 14. ISO haftasının (yoksa ondan "
                               "önceki en yakın haftanın) son günü; pencerenin w'si = giriş gününün ISO haftası",
                   "donem_ort": "dönem piyasa ortalaması = dönem içindeki BÜTÜN d (günlük) / w (haftalık) PİYASA değerlerinin ortalaması (pazar x zaman dilimi x "
                                "dönem; d / w'nin tarihi dönem içinde, e tarihi <= 2022-12-31)"},
        "fark": {"TOPLAM_FARK": "R15 - T1 (pencere başına)", "ZAMANLAMA": "PİYASA(t) - dönem piyasa ortalaması", "SECIM": "R15 - PİYASA(t)"},
        "birim": "raporda yüzde puan (x 100)"},
    "boot": {"B": 10000, "kume": "giriş ayı (YYYY-AA)",
             "tanim": "ay kümeli bootstrap: aylar yerine koyarak (multinomial ağırlık), ortalama = ağırlıklı toplam / ağırlıklı sayı; %95 = 2,5 / 97,5 yüzdelik; "
                      "tek yönlü p (+ yön) = (1 + #{boot ort <= 0}) / (B + 1)"},
    "hucre": {"donem": HV.HV_ESIK["hucre"]["donem"], "atama": "giriş tarihine göre (HV.hv_hucre_ad)", "kesif": "ABD|d1619", "dogrulama": "ABD|d2022",
              "yon": ["AVR|d1619", "AVR|d2022"], "bilgi": ["BIST|d1619", "BIST|d2022", "ABD|o16", "AVR|o16", "BIST|o16"]},
    "bh": {"q": 0.10, "aile": "16 satır x 2 uç x 2 evren x 2 zaman dilimi = 128; p = doğrulama (ABD|d2022) TOPLAM FARK tek yönlü bootstrap p; HV._hv_bh"},
    "hukum": {
        "kesif_artı": "keşif TOPLAM FARK ort > 0 VE ay kümeli alt ucu > 0",
        "dogrulama_artı": "ABD|d2022 n >= 30 VE farklı ay >= 12 VE TOPLAM FARK ort > 0 VE alt ucu > 0",
        "AVR": "AVR|d1619 ve AVR|d2022 hücrelerinden n >= 10 olanların HER BİRİNDE TOPLAM FARK ort > 0 (n < 10 hücre denetlenmez)",
        "sira": "(1) doğrulamada n < 30 ya da ay < 12 -> ÖLÇÜLEMEDİ; (2) keşif artı VE doğrulama artı VE BH q <= 0,10 VE AVR -> TUTAR; (3) doğrulamada üst ucu < 0 -> "
                "TERS; (4) keşif artı VE doğrulama artı ama BH ya da AVR geçmedi -> KISMİ; (5) yalnız biri artı -> TEK DÖNEM; (6) öteki -> TUTMADI",
        "doz": "beşlik (1..5) ile beşlik TOPLAM FARK ortalamasının Spearman'ı keşifte ve doğrulamada ayrı; ikisinde de >= 0,9 -> 'TEK YÖNLÜ ARTIŞ' (uç radikalleştikçe "
               "iyi); ikisinde de <= -0,9 -> 'TEK YÖNLÜ AZALIŞ' (bilgi); öteki -> 'YOK'",
        "genel": "evren x zaman dilimi ve hepsi için: en az bir TUTAR -> 'AÇIK VERİDE ADAY (kasa açılmaz; ileri test)'; TUTAR yok ama TEK DÖNEM ya da KISMİ var -> "
                 "'TUTARSIZ'; hiçbiri yoksa: o evren x zaman diliminin 15 UÇ10 satırının (12 ölçü + B1-B3; B4 getirisiz sayımda n ~ 100 olduğu için güç "
                 "şartından ayrı tutulur ve kendi satırında hüküm alır) hepsinde keşif ve doğrulama n >= 1.000 -> 'UÇLARDA İZ YOK (<evren> <zaman>)', değilse "
                 "'ÖLÇÜLEMEDİ'; n < 1.000 UÇ10 / UÇ2 satırları 'güç yetersiz' listesinde yazılır; hepsi için: TUTAR ya da TUTARSIZ yoksa E2 günlük hükmü",
        "not": "evren bugün yaşayanlar (yukarı yanlı); tek hisse çarpıklığı için medyan ve artıda payı da yazılır"},
    "takvim": {
        "kapsam": "yalnız B3 ve B4, E2, günlük; pazar ABD / AVR (karar), BIST (bilgi)",
        "SAYI": "SAYI(g) = pencere SONU takvimde g - 4 .. g olan (son 5 işlem günü, g dahil) E2 günlük pencerelerden B3 UÇ10 (B4: B4 'UC10' bayrağı) olanların sayısı; "
                "sayılan pencereler: atılmamış (ONCEKI_YOK / KILITLI / EVREN_DISI değil) ve bileşiği sonlu (ölçülebilirlikten bağımsız; geleceğe bakma yok: "
                "pencere sonu <= g); HV.hv25_sayi",
        "durum": ["SAYI = 0", "SAYI = 1-5", "SAYI >= 6"],
        "PIYASA15": "PİYASA15(g) = hv25_piyasa_R(M, g + 1, g + 15) (olay dışlaması yok) = PİYASA(g + 1)",
        "gun": "HV.hv25_takvim_gunler (g >= 20, g + 1 tarihi 2016-01-01 .. 2022-12-31, g + 15 tarihi <= 2022-12-31); dönem g + 1 tarihine göre; bootstrap kümesi g'nin ayı",
        "farklar": ["(SAYI >= 1) - (SAYI = 0)", "(SAYI = 1-5) - (SAYI = 0)", "(SAYI >= 6) - (SAYI = 0)"],
        "okuma": "EK 25 2b kalıbı: iki dönemde de (SAYI >= 1) - (SAYI = 0) > 0 ve alt ucu > 0 -> 'PİYASA YÜKSELİŞİNİ ÖNCELİYOR'; yalnız birinde -> 'TEK DÖNEM'; aksi "
                 "'GÖSTERİLEMEDİ' (ikisinde de üst ucu < 0 ise '(ters yönde)'); bir durumda gün < 30 ya da ay < 12 ise o fark ÖLÇÜLEMEDİ"},
    "bilgi": {"ONCEKI_DUSUS_B1": "ONCEKI_DUSUS UÇ10 VE B1 UÇ10 birlikte (çöküş dibinde en küçük mum) satırı; hükme / BH'ye girmez",
              "HEPSI_PENCERE": "hücrenin bütün TAMAM pencereleri (uç seçimi yok): evren tabanı; hükme girmez"},
    "kesik": "veri en büyük tarihi <= 2022-12-31 (HV.hv_kesik_kapi her blok) + KASA.kasa_kapisi (açık kopya / haftalık tam / p1 dosyaları)",
}

UC_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban T1 = aynı hissenin aynı dönemdeki bütün uygun giriş günleri (aynı giriş / 15 mum / stop geometrisi, stop önceki 16 bar); taban hedef payı "
                   "aynı hisse-dönemin 200 rastgele günü; PİYASA(t) aynı giriş günü bütün pazar; ZAMANLAMA dönem piyasa ortalamasına göre; HEPSI_PENCERE evren "
                   "tabanı satırı; mekanik üstünlük: E2 yapı şartsız, uçlar keşif kesimleriyle (doğrulama hücresinde yeniden seçilmez)"),
    "K2": ("EVET", "12 ölçü yalnız t'ye kadarki barlardan (Bollinger o bara kadarki kapanışlarla; test: t sonrası barlar bozulunca ölçüler aynı); E2 evreni pencere "
                   "sonu barında; E1 olayları tarama anında; kesimler keşiften getirisiz; giriş t + 1 açılışı; takvimde pencere sonu <= g; veri <= 2022-12-31 "
                   "assert + KASA kapısı"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0; OC.oc_veri_hazirla); geçersiz bar payı > %20 pencere KILITLI atılır (sayısı yazılır); haftalıkta "
                   "boşluklu pencere atılır; tamamlanmış ISO haftaları (MV.mv_haftalik_panel)"),
    "K4": ("EVET", "E1: aynı hissede < 15 bar arayla ikinci olay atılır (HV.hv_tekil); E2: sonuç pencereleri örtüşmez (adım 15, test); bootstrap ay kümeli; "
                   "ortalama yanında medyan ve artıda payı"),
    "K5": ("EVET", "giriş = pencereden sonraki ilk geçerli bar açılışı (hv25_olc_dizi = gz_olc_bir; haftalıkta sonraki haftanın ilk günü); giriş <= stop ölçülmez "
                   "(STOP_UST sayılır)"),
    "K6": ("EVET", "MI bölünme düzeltmeli fiyatlar; ölçüler oransal (BOY_GRAFIK_ORAN hissenin kendi fiyat birimiyle oran; birim bağımsız); getiriler oransal, "
                   "yerel para; karşılaştırmalar aynı hisse / aynı pazar içinde"),
    "K7": ("EVET", "evren bugün yaşayan hisseler: hem pencere hem taban yukarı yanlı; T1 aynı hisseden olduğu için yanlılık farkta kısmen düşer, kalkmaz; raporda "
                   "yazılır; kasa açılmaz"),
    "K8": ("EVET", "doğrulamada n >= 30 VE ay >= 12 şartı; en kalabalık 3 ay payı her satırda; iki dönem + iki pazar; 128 deneme BH q 0,10; keşifte iyi doğrulamada "
                   "tutmayan satır 'tutmadı'; küçük hücreden 'bulgu' denmez"),
    "K9": ("EVET", "MUM_IZI27_ON_KAYIT.md: KOD27_SHA, ESIK27_SHA, KESIM27_SHA, SAYIM27_SHA, pencere dosyası sha'ları + getirisiz sayım + kesimler + yorum noktaları; "
                   "getiriler ön kayıt commit + push'tan sonra; uc_kapi: kontrol kapısı + sha + commit + temiz ağaç"),
    "K10": ("EVET", "E1 ham dosyası mühürle (sha mum_izi8_tarama.json); olay t'si takvimde tarihle (DUR); pencere dosyaları hesapta sha ile; giriş / 15. mum tarihi, "
                    "E0 / stop getirisiz ve hesap aşamasında birebir (DUR); APPN sağlaması elle hesaplanmış değerlerle"),
    "K11": ("EVET", "hv25_olc_dizi = GZ.gz_olc_bir her blokta 200 pencerede (DUR); APPN sağlaması; rapordan önce 3 satır olay dosyasından bağımsız kısa kodla "
                    "yeniden üretilir"),
    "K12": ("EVET", "başlık 'UÇ PENCERELER (kodun ölçtüğü)'; 'kalıp' sözü yok; 'tutar / aday' yalnız hüküm kuralıyla; sayı ile yorum ayrı cümlede; 128 deneme yazılır"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_uc); MUM_IZI* / defter dosyaları değişmez (yalnız import); yalnız kendi yolları commit; sızıntı taraması "
                    "MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez, kasa açılmaz"),
}


# ================================================================ 0) YARDIMCI
def _uc_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or UC_YOL["cikti"], UC_DOSYA[ad])


def uc_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or UC_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def uc_json_sha(J: Any) -> str:
    return hashlib.sha256(json.dumps(MI._mi_json(J), sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _uc_rng(tur: int, anahtar: str) -> np.random.Generator:
    return np.random.default_rng([int(UC_ESIK["tohum"]), int(tur), zlib.crc32(str(anahtar).encode("utf-8"))])


def uc_kesik_kapi(V: Dict[str, pd.DataFrame], ad: str = "veri") -> pd.Timestamp:
    try:
        return HV.hv_kesik_kapi(V, ad, UC_KESIK)
    except HV.HVHata as ex:
        raise UCHata(str(ex)) from ex


def _uc_ay(s: Any) -> np.ndarray:
    return pd.to_datetime(pd.Series(s)).dt.strftime("%Y-%m").to_numpy() if len(s) else np.array([], str)


def uc_ay_ozet(giris: Any) -> Dict[str, Any]:
    a = _uc_ay(giris)
    if not len(a):
        return {"n": 0, "ay": 0, "ust3_pay": None, "ust3": []}
    v = pd.Series(a).value_counts()
    return {"n": int(len(a)), "ay": int(len(v)), "ust3_pay": float(v.iloc[:3].sum() / len(a)), "ust3": [[k, int(c)] for k, c in v.iloc[:3].items()]}


def _uc_pencere_yol(zaman: str, pazar: str) -> str:
    return os.path.join(UC_YOL["ham"], f"pencere_{zaman}_{pazar}.pkl")


def _uc_getiri_yol(zaman: str, pazar: str) -> str:
    return os.path.join(UC_YOL["ham"], f"getiri_{zaman}_{pazar}.pkl")


# ================================================================ 1) ÖLÇÜLER (vektörlü; yalnız t'ye kadarki barlar)
def uc_bar(O: Any, H: Any, L: Any, C: Any) -> Dict[str, np.ndarray]:
    """Bar başına büyüklükler + Bollinger (MI.mi_bant; nedensel)."""
    O, H, L, C = (np.asarray(x, float) for x in (O, H, L, C))
    rg = H - L; mx = np.maximum(O, C); mn = np.minimum(O, C)
    with np.errstate(divide="ignore", invalid="ignore"):
        boy = rg / C; gov = np.abs(C - O) / C; gb = np.abs(C - O) / rg; ust = (H - mx) / rg; alt = (mn - L) / rg
        BU, BO, BA = MI.mi_bant(C)
        bw = (BU - BA) / BO; bc = (C - BO) / (BU - BO)
    kot = ~(rg > 0) | ~(C > 0)
    for x in (boy, gov, gb, ust, alt):
        x[kot | ~np.isfinite(x)] = np.nan
    bw[~np.isfinite(bw)] = np.nan; bc[~np.isfinite(bc)] = np.nan
    return {"H": H, "L": L, "C": C, "oc": (O == C).astype(float), "rg": np.where(rg > 0, rg, np.nan), "boy": boy, "gov": gov, "gb": gb, "ust": ust, "alt": alt,
            "ua": ((H - mx) > (mn - L)).astype(float), "bw": bw, "bc": bc, "n": len(C)}


def _uc_med(A: np.ndarray, ix: np.ndarray) -> np.ndarray:
    return np.median(A[ix], axis=1)


def uc_olcu(D: Dict[str, np.ndarray], t: Any, m: int) -> Dict[str, np.ndarray]:
    """Pencereler (sonu t, uzunluk m; aynı m) için 12 ölçü + BANT_SON_ham. s - 120 >= 0 çağıranda denetlenir (DUR)."""
    t = np.asarray(t, np.int64); m = int(m); s = t - m + 1; Pn = int(UC_ESIK["pencere"]["onceki"]); P6 = int(UC_ESIK["pencere"]["onceki60"])
    out = {a: np.full(len(t), np.nan) for a in UC_OLCU_AD + UC_EK_KOL}
    if not len(t):
        return out
    if (s - Pn < 0).any() or (t >= D["n"]).any():
        raise UCHata("uc_olcu: önceki 120 bar yok ya da t seri dışında")
    W = s[:, None] + np.arange(m)[None, :]; P = (s - Pn)[:, None] + np.arange(Pn)[None, :]
    q = int(math.ceil(m / 3.0)); S3 = (t - q + 1)[:, None] + np.arange(q)[None, :]; P60 = (s - P6)[:, None] + np.arange(P6)[None, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        bw_, bp = _uc_med(D["boy"], W), _uc_med(D["boy"], P)
        out["BOY_YUZDE_ORAN"] = bw_ / bp
        out["BOY_GRAFIK_ORAN"] = _uc_med(D["rg"], W) / _uc_med(D["rg"], P)
        out["BOY_MUTLAK"] = 100.0 * bw_
        gp = _uc_med(D["gov"], P); out["GOVDE_ORAN"] = np.where(gp > 0, _uc_med(D["gov"], W) / np.where(gp > 0, gp, 1.0), np.nan)
        out["GOVDE_BOY"] = _uc_med(D["gb"], W); out["UST_FITIL"] = _uc_med(D["ust"], W); out["ALT_FITIL"] = _uc_med(D["alt"], W)
        out["UST_ALT_PAY"] = D["ua"][W].mean(1); out["SON_UST_FITIL"] = _uc_med(D["ust"], S3)
        b0 = D["bw"][s]; out["DARALMA"] = np.where(b0 > 0, D["bw"][t] / np.where(b0 > 0, b0, 1.0) - 1, np.nan)
        bh = _uc_med(D["bc"], S3); out["BANT_SON_ham"] = bh; out["BANT_SON"] = -np.abs(bh - 0.85)
        out["ONCEKI_DUSUS"] = 100.0 * (D["L"][W].min(1) / D["H"][P60].max(1) - 1)
        out["govdesiz_pay"] = D["oc"][W].mean(1); out["fiyat_med"] = np.median(D["C"][W], axis=1)      # bilgi (fiyat adımı / birim)
    for a in out:
        out[a] = np.where(np.isfinite(out[a]), out[a], np.nan)
    return out


def uc_skor(X: pd.DataFrame, ad: str) -> np.ndarray:
    """Uç skoru: KUCUK -> -değer, BUYUK -> +değer."""
    y = dict(UC_OLCU)[ad]; v = X[ad].to_numpy(float)
    return -v if y == "KUCUK" else v


# ================================================================ 2) PENCERELER (GETİRİSİZ)
def uc_e2_uclar(n: int) -> np.ndarray:
    E = UC_ESIK["pencere"]["E2"]
    return np.arange(int(E["ilk_son"]), int(n), int(E["adim"]), dtype=np.int64)


def uc_e1_olaylar() -> pd.DataFrame:
    """MUM_IZI8 ham taraması 'R4' (M yok), evren içi, 15 bar tekil."""
    J = json.load(open(UC_YOL["tarama8"], encoding="utf-8"))
    if not os.path.exists(UC_YOL["ham8"]):
        raise UCHata(f"MUM_IZI8 tarama ham dosyası yok: {UC_YOL['ham8']} (MUM_IZI_V5.py tarama ile yeniden üretilir)")
    if MI._mi_sha(UC_YOL["ham8"]) != J["ham_sha"]:
        raise UCHata("MUM_IZI8 tarama ham dosyası mühürle uyuşmuyor")
    ham = json.load(open(UC_YOL["ham8"], encoding="utf-8"))["olay"]["R4"]
    X0 = pd.DataFrame([o for o in ham if o["evren"]])
    if X0.duplicated(["zaman", "sembol", "tarih"]).any():
        raise UCHata("K4: R4 havuzunda aynı bölge iki kez")
    X, at = HV.hv_tekil(X0, 15)
    X.attrs["ham_hepsi"] = len(ham); X.attrs["ham_evren"] = len(X0); X.attrs["tekil_atilan"] = at
    return X


def uc_kilitli_pay(gec: pd.DatetimeIndex, gun: pd.DatetimeIndex, bas: Any, son: Any) -> np.ndarray:
    """[bas, son] günlük takvim aralığında geçersiz bar payı = geçersiz / (geçersiz + geçerli)."""
    bas = pd.DatetimeIndex(bas); son = pd.DatetimeIndex(son); gec = pd.DatetimeIndex(gec).sort_values(); gun = pd.DatetimeIndex(gun)
    g = gec.searchsorted(son, side="right") - gec.searchsorted(bas, side="left")
    v = gun.searchsorted(son, side="right") - gun.searchsorted(bas, side="left")
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(g + v > 0, g / np.maximum(g + v, 1), 0.0).astype(float)


def uc_blok_veri(zaman: str, pazar: str) -> Tuple[Dict[str, pd.DataFrame], Optional[Dict[str, pd.DataFrame]], Dict[str, pd.DatetimeIndex]]:
    """(Vd günlük, W haftalık ya da None, geçersiz tarihler) — HV.hv_blok ile aynı yükleyiciler; kesik assert."""
    if zaman == "gunluk":
        R = MI.mi_veri(pazar, MV.MV_YOL["gunluk"]); Vd = R["V"]; uc_kesik_kapi(Vd, f"{zaman} {pazar}")
        return {s: d for s, d in Vd.items() if len(d) >= 40}, None, R.get("gecersiz", {})
    R = MI.mi_veri(pazar, MH.MH_YOL["tam"]); Vd = R["V"]; uc_kesik_kapi(Vd, f"{zaman} {pazar}")
    return Vd, MV.mv_haftalik_panel(Vd), R.get("gecersiz", {})


def uc_evren_e2(zaman: str, pazar: str, B: Dict[str, pd.DataFrame], aday: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """E2 pencere sonlarının P2 evren bayrağı (MUM_IZI8 taramasının kuralı aynen)."""
    import MUM_IZI_ETIKET2 as E6
    out = {s: np.zeros(len(t), bool) for s, t in aday.items()}
    if pazar in ("ABD", "AVR"):
        for (a, b), kl in E6.e6_parcalar(zaman, pazar):
            P = E6.e6_p2_hazirla(pazar, kl)
            for s, t in aday.items():
                if not len(t):
                    continue
                ix = B[s].index[t]; j = np.flatnonzero((ix >= pd.Timestamp(a)) & (ix <= pd.Timestamp(b)))
                if len(j):
                    out[s][j] = E6.e6_p2_maske(P, s, ix[j])
            del P; gc.collect()
    else:
        med = E6.e6_bist_medyan(B, zaman)
        for s, t in aday.items():
            if not len(t):
                continue
            d = B[s]; dv = (d.Close * d.Volume).to_numpy(float)[t]; ix = d.index[t]
            mv = med.reindex(E6._e6_anahtar(ix, zaman)).to_numpy(float); out[s] = np.isfinite(mv) & (dv > mv)
    return out


def uc_t1_say(A: Dict[str, Any]) -> Dict[str, int]:
    """Hisse-dönem başına T1 uygun gün sayısı (getirisiz)."""
    m = int(UC_ESIK["sonuc"]["T1"]["m"]); out = {}
    for d, (a, b) in UC_ESIK["hucre"]["donem"].items():
        out[d] = int(len(HV.hv25_uygun(A, m, [], a, b, UC_KESIK)))
    return out


def uc_blok_pencere(zaman: str, pazar: str, E1: pd.DataFrame) -> pd.DataFrame:
    """Bir blok (zaman, pazar): E1 ve E2 pencereleri, durum, ölçüler, getirisiz ölçü geometrisi (giriş / 15. mum tarihi, E0, stop), T1 uygun sayısı."""
    Vd, W, GEC = uc_blok_veri(zaman, pazar); B = W if zaman == "haftalik" else Vd
    U = 15; Pn = int(UC_ESIK["pencere"]["onceki"]); ara = UC_ESIK["pencere"]["tarama"][zaman]; a0, a1 = pd.Timestamp(ara[0]), pd.Timestamp(ara[1])
    m2 = int(UC_ESIK["pencere"]["E2"]["uzunluk"]); kp = float(UC_ESIK["atma"]["KILITLI"]["pay"]); sc = float(GZ.GZ_ESIK["olcu"]["stop_carpan"])
    e1 = E1[(E1.zaman == zaman) & (E1.pazar == pazar)]
    aday2: Dict[str, np.ndarray] = {}
    for s, d in B.items():
        t = uc_e2_uclar(len(d)); ix = d.index[t] if len(t) else d.index[:0]
        aday2[s] = t[(ix >= a0) & (ix <= a1)] if len(t) else t
    ev2 = uc_evren_e2(zaman, pazar, B, aday2)
    parca = []
    for s in sorted(set(B) | set(e1.sembol)):
        d = B.get(s)
        if d is None:
            raise UCHata(f"K10: {zaman} {pazar} {s}: E1 olayı var, seri yok")
        Dg = Vd[s]; A = HV.hv25_dizi(Dg, W[s] if W is not None else None); Db = uc_bar(d.Open, d.High, d.Low, d.Close)
        t1n = uc_t1_say(A); bos = np.r_[0, np.cumsum(d.bosluk.to_numpy(bool).astype(np.int64))] if "bosluk" in d.columns else None
        for ev, tt, mm, ek in (("E2", aday2.get(s, np.array([], np.int64)), None, ev2.get(s)),
                               ("E1", None, None, None)):
            if ev == "E1":
                r = e1[e1.sembol == s]
                if not len(r):
                    continue
                tt = r.t.to_numpy(np.int64); mm = r.m.to_numpy(np.int64)
                if (d.index[tt] != pd.DatetimeIndex(pd.to_datetime(r.tarih))).any():
                    raise UCHata(f"K10: {zaman} {pazar} {s}: E1 olay t'si takvimle uyuşmuyor")
                ek = np.ones(len(tt), bool)
            else:
                if not len(tt):
                    continue
                mm = np.full(len(tt), m2, np.int64)
            n = len(d); bas_i = tt - mm + 1
            Y = pd.DataFrame({"evren": ev, "zaman": zaman, "pazar": pazar, "sembol": s, "t": tt, "m": mm})
            Y["son"] = d.index[tt]
            Y["bas"] = (pd.DatetimeIndex(d.bas.iloc[np.maximum(bas_i, 0)]) if zaman == "haftalik" else d.index[np.maximum(bas_i, 0)])
            dur = np.array([""] * len(tt), dtype=object)
            dur[(bas_i - Pn) < 0] = "ONCEKI_YOK"
            if bos is not None:
                bb = (bos[tt + 1] - bos[np.maximum(bas_i + 1, 0)]) > 0
                dur[(dur == "") & bb] = "BOSLUK"
            kpay = uc_kilitli_pay(GEC.get(s, pd.DatetimeIndex([])), Dg.index, Y.bas, Dg.index[A["ei"][tt]])
            Y["kilitli_pay"] = kpay; dur[(dur == "") & (kpay > kp)] = "KILITLI"
            dur[(dur == "") & ~np.asarray(ek, bool)] = "EVREN_DISI"
            gir = np.where(tt + 1 < n, tt + 1, n - 1); Y["giris"] = A["giris_tarih"][gir]; Y.loc[tt + 1 >= n, "giris"] = pd.NaT
            dur[(dur == "") & (tt + 1 >= n)] = "GIRIS_YOK"
            e15 = np.where(tt + U < n, tt + U, n - 1); s15 = A["tarih"][e15]
            Y["son15"] = s15; Y.loc[tt + U >= n, "son15"] = pd.NaT
            dur[(dur == "") & ((tt + U >= n) | (s15 > UC_KESIK))] = "UFUK_KESIK"
            E0 = np.where(tt + 1 < n, A["DO"][A["gi"][gir]], np.nan)
            st = np.full(len(tt), np.nan)
            for mu in np.unique(mm):
                j = np.flatnonzero((mm == mu) & (bas_i >= 0))
                if len(j):
                    st[j] = HV._hv25_rmin(A, int(mu))[bas_i[j]] * sc
            Y["E0"] = E0; Y["stop"] = st
            with np.errstate(invalid="ignore"):
                dur[(dur == "") & ~(np.isfinite(E0) & (E0 > 0) & (E0 > st))] = "STOP_UST"
            hc = [HV.hv_hucre_ad(g, pazar) if pd.notna(g) else f"{pazar}|yok" for g in Y.giris]; Y["hucre"] = hc
            don = [h.split("|")[1] for h in hc]
            dur[(dur == "") & np.isin(np.asarray(don), ["dis", "yok"])] = "DONEM_DISI"
            Y["t1_n"] = [t1n.get(x, 0) for x in don]
            dur[(dur == "") & (Y.t1_n.to_numpy() < int(UC_ESIK["sonuc"]["T1"]["en_az"]))] = "T1_YOK"
            dur[dur == ""] = "TAMAM"; Y["durum"] = dur
            olc = {a: np.full(len(tt), np.nan) for a in UC_OLCU_AD + UC_EK_KOL}
            ok = (bas_i - Pn) >= 0
            for mu in np.unique(mm[ok]):
                j = np.flatnonzero(ok & (mm == mu)); O_ = uc_olcu(Db, tt[j], int(mu))
                for a in olc:
                    olc[a][j] = O_[a]
            for a in olc:
                Y[a] = olc[a]
            parca.append(Y)
    X = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame()
    if len(X) and X.duplicated(["evren", "sembol", "t"]).any():
        raise UCHata("K4: pencere iki kez")
    del Vd, W, B; gc.collect()
    uclog.info("pencere %s %s: %s", zaman, pazar, X.groupby(["evren", "durum"]).size().to_dict() if len(X) else {})
    return X


def uc_pencere_kos() -> Dict[str, Any]:
    """Bütün bloklar -> /root/.kasa/ham/mum_izi27/pencere_<zaman>_<pazar>.pkl (getirisiz). KASA kapısı önce."""
    import KASA as KS
    yol = [os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in UC_PAZAR] + [os.path.join(MH.MH_YOL["tam"], f"V_{p}.pkl") for p in UC_PAZAR] + \
          [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")]
    kasa = KS.kasa_kapisi(yol, "2022-12-31"); E1 = uc_e1_olaylar(); os.makedirs(UC_YOL["ham"], exist_ok=True); sha = {}
    for z in UC_ZAMAN:
        for p in UC_PAZAR:
            t0 = time.time(); X = uc_blok_pencere(z, p, E1); y = _uc_pencere_yol(z, p)
            X.to_pickle(y + ".tmp"); os.replace(y + ".tmp", y); sha[f"{z}_{p}"] = MI._mi_sha(y)
            uclog.info("%s %s: %d pencere, %.0f sn", z, p, len(X), time.time() - t0); del X; gc.collect()
    J = {"kasa": kasa, "E1_huni": {"ham_hepsi": E1.attrs["ham_hepsi"], "ham_evren": E1.attrs["ham_evren"], "tekil_atilan": E1.attrs["tekil_atilan"],
                                   "tekil": int(len(E1))}, "sha": sha}
    MI._mi_jyaz(os.path.join(UC_YOL["ham"], "pencere_ozet.json"), J, "pencere özeti 27")
    return J


def uc_pencere_yukle(sha_bek: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    parca = []
    for z in UC_ZAMAN:
        for p in UC_PAZAR:
            y = _uc_pencere_yol(z, p)
            if not os.path.exists(y):
                raise UCHata(f"pencere dosyası yok: {y} (python MUM_IZI_UC.py pencere)")
            if sha_bek is not None and MI._mi_sha(y) != sha_bek[f"{z}_{p}"]:
                raise UCHata(f"K9 / K10: pencere dosyası mühürle uyuşmuyor: {y}")
            parca.append(pd.read_pickle(y))
    return pd.concat(parca, ignore_index=True)


# ================================================================ 3) KESİMLER (YALNIZ KEŞİF) ve UYGULAMA
def uc_kesif_maske(X: pd.DataFrame) -> np.ndarray:
    return ((X.hucre == UC_ESIK["kesim"]["kesif"]) & (X.durum == "TAMAM")).to_numpy()


def uc_kesim(X: pd.DataFrame) -> Dict[str, Any]:
    """evren x zaman dilimi başına keşif kesimleri (X: o evren x zaman diliminin bütün pencereleri; yalnız keşif satırları okunur)."""
    K = X[uc_kesif_maske(X)]; G = UC_ESIK["kesim"]; out: Dict[str, Any] = {"n_kesif": int(len(K)), "olcu": {}, "bilesik": {}}
    sir: Dict[str, np.ndarray] = {}
    for a in UC_OLCU_AD:
        u = uc_skor(K, a); u = u[np.isfinite(u)]
        if len(u) < 50:
            raise UCHata(f"kesim: {a} keşif örneği {len(u)} < 50")
        sir[a] = np.sort(u)
        out["olcu"][a] = {"n": int(len(u)), "UC10": float(np.quantile(u, G["UC10"])), "UC2": float(np.quantile(u, G["UC2"])),
                          "besli": [float(np.quantile(u, q)) for q in G["besli"]], "B4_30": float(np.quantile(u, G["B4"]["UC10"])),
                          "B4_10": float(np.quantile(u, G["B4"]["UC2"])), "_sirali": sir[a]}
    P = uc_yuzdelik(K, out)
    for b, comp in UC_BILESIK.items():
        v = P[b]; v = v[np.isfinite(v)]
        if b == "B4_HEPSI_VE":
            out["bilesik"][b] = {"n": int(len(v)), "besli": [float(np.quantile(v, q)) for q in G["besli"]]}
        else:
            out["bilesik"][b] = {"n": int(len(v)), "UC10": float(np.quantile(v, G["UC10"])), "UC2": float(np.quantile(v, G["UC2"])),
                                 "besli": [float(np.quantile(v, q)) for q in G["besli"]]}
    return out


def uc_yuzdelik(X: pd.DataFrame, KS: Dict[str, Any]) -> Dict[str, np.ndarray]:
    """Bileşik değerleri: B1-B3 = bileşen keşif ECDF yüzdeliklerinin ortalaması; B4 beşlik değeri = altı bileşenin en küçük yüzdeliği."""
    p = {}
    for a in UC_OLCU_AD:
        u = uc_skor(X, a); sr = KS["olcu"][a]["_sirali"]; v = np.searchsorted(sr, u, side="right") / float(len(sr)); v[~np.isfinite(u)] = np.nan; p[a] = v
    out = {}
    for b, comp in UC_BILESIK.items():
        M = np.stack([p[a] for a in comp], 1); fin = np.isfinite(M).all(1)
        out[b] = np.where(fin, (M.mean(1) if b != "B4_HEPSI_VE" else M.min(1)), np.nan)
    return out


def uc_uygula(X: pd.DataFrame, KS: Dict[str, Any]) -> pd.DataFrame:
    """Keşif kesimlerini X'e uygular: <satır>_UC10, <satır>_UC2 (bool), <satır>_BES (0 = değer yok, 1..5)."""
    X = X.copy(); P = uc_yuzdelik(X, KS); yeni = {}
    for a in UC_OLCU_AD:
        u = uc_skor(X, a); k = KS["olcu"][a]; f = np.isfinite(u)
        yeni[f"{a}_UC10"] = f & (u >= k["UC10"]); yeni[f"{a}_UC2"] = f & (u >= k["UC2"])
        yeni[f"{a}_BES"] = np.where(f, 1 + (u[:, None] >= np.asarray(k["besli"])[None, :]).sum(1), 0)
    for b in UC_BILESIK:
        v = P[b]; f = np.isfinite(v); k = KS["bilesik"][b]; yeni[f"{b}_DEG"] = v
        if b == "B4_HEPSI_VE":
            U30 = np.ones(len(X), bool); U10 = np.ones(len(X), bool)
            for a in UC_BILESIK[b]:
                u = uc_skor(X, a); U30 &= np.isfinite(u) & (u >= KS["olcu"][a]["B4_30"]); U10 &= np.isfinite(u) & (u >= KS["olcu"][a]["B4_10"])
            yeni[f"{b}_UC10"] = U30; yeni[f"{b}_UC2"] = U10
        else:
            yeni[f"{b}_UC10"] = f & (v >= k["UC10"]); yeni[f"{b}_UC2"] = f & (v >= k["UC2"])
        yeni[f"{b}_BES"] = np.where(f, 1 + (np.nan_to_num(v, nan=-1)[:, None] >= np.asarray(k["besli"])[None, :]).sum(1), 0)
    yeni["ONCEKI_DUSUS_B1_UC10"] = yeni["ONCEKI_DUSUS_UC10"] & yeni["B1_KUCUK_MUM_UC10"]
    return pd.concat([X.reset_index(drop=True), pd.DataFrame(yeni)], axis=1)


def uc_kesim_hepsi(X: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    out = {}
    for ev in UC_EVREN:
        for z in UC_ZAMAN:
            out[f"{ev}|{z}"] = uc_kesim(X[(X.evren == ev) & (X.zaman == z)])
    return out


def uc_kesim_json(KS: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Kesimlerin yayımlanan / mühürlenen hali (sıralı keşif dizisi yerine sha'sı)."""
    J = {}
    for k, v in KS.items():
        J[k] = {"n_kesif": v["n_kesif"], "bilesik": v["bilesik"],
                "olcu": {a: {kk: vv for kk, vv in o.items() if kk != "_sirali"} | {"sirali_sha": hashlib.sha256(np.ascontiguousarray(o["_sirali"]).tobytes()).hexdigest()}
                         for a, o in v["olcu"].items()}}
    return J


def uc_hazir(X: pd.DataFrame, KS: Optional[Dict[str, Dict[str, Any]]] = None) -> Tuple[pd.DataFrame, Dict[str, Dict[str, Any]]]:
    KS = KS or uc_kesim_hepsi(X); parca = []
    for ev in UC_EVREN:
        for z in UC_ZAMAN:
            Y = X[(X.evren == ev) & (X.zaman == z)]
            if len(Y):
                parca.append(uc_uygula(Y, KS[f"{ev}|{z}"]))
    return pd.concat(parca, ignore_index=True), KS


# ================================================================ 4) GETİRİSİZ SAYIM
_UC_HUC = ["ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022", "BIST|d1619", "BIST|d2022", "ABD|o16", "AVR|o16", "BIST|o16"]


def uc_sayim(X: pd.DataFrame, KS: Dict[str, Dict[str, Any]], P0: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Getirisiz: pencere / atılan sayıları, keşif kesimleri, uçta kalan pencere sayısı ve farklı ay, sıra ilişkisi matrisi, B4, takvim durum sayıları."""
    S: Dict[str, Any] = {"surum": UC_SURUM, "huni": {}, "hucre": {}, "uc": {}, "spearman": {}, "B4": {}, "takvim": {}, "E1": (P0 or {}).get("E1_huni")}
    for (ev, z, p), g in X.groupby(["evren", "zaman", "pazar"]):
        S["huni"][f"{ev}|{z}|{p}"] = {"toplam": int(len(g)), **{k: int(v) for k, v in g.durum.value_counts().items()}}
    T = X[X.durum == "TAMAM"]
    for (ev, z), g in T.groupby(["evren", "zaman"]):
        k = f"{ev}|{z}"; S["hucre"][k] = {h: uc_ay_ozet(g.giris[g.hucre == h]) for h in _UC_HUC}; S["uc"][k] = {}
        for a in UC_SATIR + ["ONCEKI_DUSUS_B1"]:
            for u in (UC_UC if a != "ONCEKI_DUSUS_B1" else ("UC10",)):
                c = f"{a}_{u}"
                S["uc"][k][f"{a}|{u}"] = {h: {"n": int(g[c][g.hucre == h].sum()), "ay": int(pd.Series(_uc_ay(g.giris[(g.hucre == h) & g[c]])).nunique())
                                              if g[c][g.hucre == h].any() else 0} for h in _UC_HUC}
        K = g[g.hucre == UC_ESIK["kesim"]["kesif"]]
        R = K[UC_OLCU_AD].rank().corr(method="pearson")
        S["spearman"][k] = {a: {b: (round(float(R.loc[a, b]), 3) if np.isfinite(R.loc[a, b]) else None) for b in UC_OLCU_AD} for a in UC_OLCU_AD}
        S["B4"][k] = {h: int(g["B4_HEPSI_VE_UC10"][g.hucre == h].sum()) for h in _UC_HUC}
        S.setdefault("adim", {})[k] = {"HEPSI": _uc_adim(K)}               # bilgi: fiyat adımı / birim (keşif hücresi)
        for a in UC_SATIR:
            S["adim"][k][f"{a}|UC2"] = _uc_adim(K[K[f"{a}_UC2"].to_numpy(bool)])
    return S


def _uc_adim(K: pd.DataFrame) -> Dict[str, Any]:
    if not len(K):
        return {"n": 0}
    gp = K.govdesiz_pay.to_numpy(float); f = K.fiyat_med.to_numpy(float)
    return {"n": int(len(K)), "govdesiz_ort": float(np.nanmean(gp)), "govdesiz_yarim_pay": float(np.nanmean(gp >= 0.5)), "fiyat_medyan": float(np.nanmedian(f)),
            "fiyat_5_alti_pay": float(np.nanmean(f < 5))}


def uc_takvim_sayim(X: pd.DataFrame, cal: Dict[str, pd.DatetimeIndex]) -> Dict[str, Any]:
    """Takvim durum sayıları (getirisiz): pazar x dönem x bileşik x durum -> gün sayısı."""
    out: Dict[str, Any] = {}
    for p, c in cal.items():
        for b in ("B3_HEPSI", "B4_HEPSI_VE"):
            sy, g, don = uc_takvim_seri(X, p, b, c)
            ds = _uc_durum(sy[g])
            out[f"{p}|{b}"] = {d: {s: int(((don == d) & (ds == s)).sum()) for s in UC_ESIK["takvim"]["durum"]} for d in ("d1619", "d2022")}
    return out


def _uc_durum(sy: np.ndarray) -> np.ndarray:
    return np.where(sy <= 0, "SAYI = 0", np.where(sy <= 5, "SAYI = 1-5", "SAYI >= 6"))


def uc_takvim_seri(X: pd.DataFrame, pazar: str, b: str, cal: pd.DatetimeIndex) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """SAYI(g) (bütün takvim), uygun g'ler, g'lerin dönemi."""
    Y = X[(X.evren == "E2") & (X.zaman == "gunluk") & (X.pazar == pazar) & ~X.durum.isin(["ONCEKI_YOK", "BOSLUK", "KILITLI", "EVREN_DISI"])]
    Y = Y[np.isfinite(Y[f"{b}_DEG"].to_numpy(float)) & Y[f"{b}_UC10"].to_numpy(bool)]
    sy = HV.hv25_sayi(cal, Y.son.to_numpy(), 5)
    g = HV.hv25_takvim_gunler(cal, UC_KESIK)
    don = np.array([HV.hv25_donem(cal[i + 1]) for i in g], dtype=object)
    return sy, g, don


def uc_takvim_veri(pazar: str) -> Dict[str, pd.DataFrame]:
    """Takvim / piyasa için pazarın günlük açık verisi (bütün hisseler); kesik assert."""
    Vd = MI.mi_veri(pazar, MV.MV_YOL["gunluk"])["V"]; uc_kesik_kapi(Vd, f"takvim {pazar}")
    return Vd


def uc_takvim_cal(pazar: str) -> pd.DatetimeIndex:
    Vd = uc_takvim_veri(pazar)
    return pd.DatetimeIndex(np.unique(np.concatenate([d.index.values.astype("datetime64[ns]") for d in Vd.values()])))


def uc_sayim_kos() -> Tuple[pd.DataFrame, Dict[str, Any], Dict[str, Dict[str, Any]]]:
    P0 = json.load(open(os.path.join(UC_YOL["ham"], "pencere_ozet.json"), encoding="utf-8"))
    X0 = uc_pencere_yukle(P0["sha"]); X, KS = uc_hazir(X0); S = uc_sayim(X, KS, P0)
    S["takvim"] = uc_takvim_sayim(X, {p: uc_takvim_cal(p) for p in UC_PAZAR}); S["pencere_sha"] = P0["sha"]
    return X, S, KS


# ================================================================ 5) HESAP (GETİRİLER; yalnız ön kayıt kapısından sonra)
def uc_piyasa(Vd: Dict[str, pd.DataFrame], zaman: str) -> Dict[str, Any]:
    """PİYASA(d) (günlük) ya da PİYASA(w) (haftalık; ISO hafta anahtarı) + dönem ortalamaları."""
    M = HV.hv25_piyasa_matris(Vd); cal = M["cal"]; n = len(cal); out: Dict[str, Any] = {}
    if zaman == "gunluk":
        d = np.arange(n - 14); ok = cal[d + 14] <= UC_KESIK; R = np.full(n, np.nan)
        for i in d[ok]:
            R[i] = HV.hv25_piyasa_R(M, int(i), int(i) + 14, [])[0]
        out["anahtar"] = {pd.Timestamp(cal[i]): float(R[i]) for i in range(n) if np.isfinite(R[i])}
        tar = cal; deg = R
    else:
        wk = _uc_iso(cal); hn = uc_hafta_no(cal)
        uh, ilk = np.unique(hn, return_index=True); son = np.r_[ilk[1:] - 1, n - 1]
        R = np.full(len(uh), np.nan); key = {}
        for j, h in enumerate(uh):
            k = int(np.searchsorted(uh, h + 14, side="right")) - 1          # w + 14. hafta (yoksa ondan önceki en yakın hafta)
            if k <= j or (uh[k] != h + 14 and k == len(uh) - 1):            # veri w + 14'ten önce bitiyor
                continue
            e = int(son[k])
            if cal[e] > UC_KESIK:
                continue
            R[j] = HV.hv25_piyasa_R(M, int(ilk[j]), e, [])[0]
            if np.isfinite(R[j]):
                key[int(wk[ilk[j]])] = float(R[j])
        out["anahtar"] = key; tar = cal[ilk]; deg = R
    out["donem"] = {}
    for dn, (a, b) in UC_ESIK["hucre"]["donem"].items():
        msk = (tar >= pd.Timestamp(a)) & (tar <= pd.Timestamp(b)) & np.isfinite(deg)
        out["donem"][dn] = {"ort": float(np.mean(deg[msk])) if msk.any() else None, "n": int(msk.sum())}
    out["M"] = M
    return out


def _uc_iso(g: Any) -> np.ndarray:
    c = pd.DatetimeIndex(g).isocalendar()
    return c.year.to_numpy().astype(np.int64) * 100 + c.week.to_numpy().astype(np.int64)


def uc_hafta_no(cal: Any) -> np.ndarray:
    """Ardışık hafta numarası (pazartesi tabanlı; 1970'ten hafta sayısı)."""
    cal = pd.DatetimeIndex(cal); mon = (cal - pd.to_timedelta(cal.dayofweek, unit="D")).normalize()
    return (mon.values.astype("datetime64[D]").astype(np.int64)) // 7


def uc_getiri_blok(zaman: str, pazar: str, X: pd.DataFrame, denetim: int = 200) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Blok TAMAM pencereleri: R15, d5, d10, T1, taban d5 / d10, PİYASA, dönem piyasa ortalaması. Getirisiz geometri birebir (DUR); gz_olc_bir denetimi."""
    Vd, W, _ = uc_blok_veri(zaman, pazar); B = W if zaman == "haftalik" else Vd
    Y = X[(X.zaman == zaman) & (X.pazar == pazar) & (X.durum == "TAMAM")].copy()
    kol = {c: np.full(len(Y), np.nan) for c in ("R15", "d5", "d10", "T1", "tb5", "tb10", "PIY", "PIY_don")}
    T1c: Dict[Tuple[str, str], Tuple[float, float, float, int]] = {}; m16 = int(UC_ESIK["sonuc"]["T1"]["m"]); cek = int(UC_ESIK["sonuc"]["taban_hedef"]["cekim"])
    pos = {i: k for k, i in enumerate(Y.index)}
    for s, g in Y.groupby("sembol"):
        A = HV.hv25_dizi(Vd[s], W[s] if W is not None else None)
        for mu in np.unique(g.m):
            gg = g[g.m == mu]; o = HV.hv25_olc_dizi(A, gg.t.to_numpy(np.int64), int(mu))
            if (np.abs(o["E0"] - gg.E0.to_numpy(float)) > 1e-12 * np.abs(o["E0"]) + 1e-12).any() or \
               (np.abs(o["stop"] - gg.stop.to_numpy(float)) > 1e-12 * np.abs(o["stop"]) + 1e-12).any():
                raise UCHata(f"K10: {zaman} {pazar} {s}: E0 / stop getirisiz aşamayla uyuşmuyor")
            if (A["giris_tarih"][gg.t.to_numpy() + 1] != pd.DatetimeIndex(gg.giris)).any() or (A["tarih"][gg.t.to_numpy() + 15] != pd.DatetimeIndex(gg.son15)).any():
                raise UCHata(f"K10: {zaman} {pazar} {s}: giriş / 15. mum tarihi uyuşmuyor")
            for c, kk in (("R15", "R15"), ("d5", "d5"), ("d10", "d10")):
                kol[c][[pos[i] for i in gg.index]] = o[kk]
        for dn in g.hucre.str.split("|").str[1].unique():
            a, b = UC_ESIK["hucre"]["donem"][dn]; tu = HV.hv25_uygun(A, m16, [], a, b, UC_KESIK)
            o = HV.hv25_olc_dizi(A, tu, m16); rng = _uc_rng(1, f"{zaman}|{pazar}|{s}|{dn}")
            sec = rng.choice(len(tu), size=min(cek, len(tu)), replace=False)
            T1c[(s, dn)] = (float(np.mean(o["R15"])), float(np.mean(o["d5"][sec])), float(np.mean(o["d10"][sec])), int(len(tu)))
    dn_ = Y.hucre.str.split("|").str[1].to_numpy()
    for k, (s, dn) in enumerate(zip(Y.sembol, dn_)):
        v = T1c[(s, dn)]
        if v[3] != int(Y.t1_n.iloc[k]):
            raise UCHata(f"K10: {zaman} {pazar} {s} {dn}: T1 uygun gün sayısı getirisiz sayımla uyuşmuyor")
        kol["T1"][k], kol["tb5"][k], kol["tb10"][k] = v[0], v[1], v[2]
    PI = uc_piyasa(Vd, zaman)
    if zaman == "gunluk":
        kol["PIY"] = np.array([PI["anahtar"].get(pd.Timestamp(g), np.nan) for g in Y.giris], float)
    else:
        kol["PIY"] = np.array([PI["anahtar"].get(int(w), np.nan) for w in _uc_iso(Y.giris)], float)
    kol["PIY_don"] = np.array([PI["donem"][d]["ort"] if PI["donem"][d]["ort"] is not None else np.nan for d in dn_], float)
    for c, v in kol.items():
        Y[c] = v
    # K11: gz_olc_bir ile birebir (rastgele pencereler)
    rng = np.random.default_rng([27, 9, zlib.crc32(f"{zaman}|{pazar}".encode())]); jj = rng.choice(len(Y), size=min(denetim, len(Y)), replace=False) if len(Y) else []
    for j in jj:
        r = Y.iloc[int(j)]; rec = GZ.gz_olc_bir(Vd[r.sembol], W[r.sembol] if W is not None else None,
                                                {"zaman": zaman, "tarih": str(pd.Timestamp(r.son).date()), "m": int(r.m)}, UC_KESIK)
        if not rec["olculdu"] or abs(rec["R15"] - r.R15) > 1e-12 or (zaman == "gunluk" and (rec["d5"] != r.d5 or rec["d10"] != r.d10)) or \
           (zaman == "haftalik" and rec["d10"] != r.d10):
            raise UCHata(f"K11: {zaman} {pazar} {r.sembol} {r.son}: hv25_olc_dizi != gz_olc_bir")
    PJ = {"donem": PI["donem"], "n_gun": int(len(PI["anahtar"])), "denetim_gz": int(len(jj))}
    del Vd, W, B, PI; gc.collect()
    return Y, PJ


# ================================================================ 6) İSTATİSTİK
def uc_boot(x: Any, ay: Any, anahtar: str, B: Optional[int] = None) -> Dict[str, Any]:
    """Ay kümeli bootstrap ortalama: ort, medyan, alt, üst, tek yönlü p (+ yön)."""
    x = np.asarray(x, float); ay = np.asarray(ay, str); B = int(B or UC_ESIK["boot"]["B"])
    if len(x) < 2:
        return {"ort": float(x.mean()) if len(x) else None, "medyan": float(np.median(x)) if len(x) else None, "alt": None, "ust": None, "p": None}
    u, k = np.unique(ay, return_inverse=True); K = len(u)
    s = np.bincount(k, weights=x, minlength=K); n = np.bincount(k, minlength=K).astype(float)
    Wm = _uc_rng(2, anahtar).multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (Wm @ s) / (Wm @ n)
    d = d[np.isfinite(d)]
    return {"ort": float(x.mean()), "medyan": float(np.median(x)), "alt": float(np.quantile(d, 0.025)), "ust": float(np.quantile(d, 0.975)),
            "p": float((1 + np.sum(d <= 0)) / (len(d) + 1))}


def uc_boot_fark(xa: Any, aya: Any, xb: Any, ayb: Any, anahtar: str, B: Optional[int] = None) -> Dict[str, Any]:
    xa = np.asarray(xa, float); xb = np.asarray(xb, float); B = int(B or UC_ESIK["boot"]["B"])
    if len(xa) < 2 or len(xb) < 2:
        return {"fark": None, "alt": None, "ust": None}
    u = np.unique(np.r_[np.asarray(aya, str), np.asarray(ayb, str)]); ix = {a: i for i, a in enumerate(u)}; K = len(u)
    ka = np.array([ix[a] for a in np.asarray(aya, str)]); kb = np.array([ix[a] for a in np.asarray(ayb, str)])
    sa = np.bincount(ka, weights=xa, minlength=K); na = np.bincount(ka, minlength=K).astype(float)
    sb = np.bincount(kb, weights=xb, minlength=K); nb = np.bincount(kb, minlength=K).astype(float)
    Wm = _uc_rng(3, anahtar).multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (Wm @ sa) / (Wm @ na) - (Wm @ sb) / (Wm @ nb)
    d = d[np.isfinite(d)]
    return {"fark": float(xa.mean() - xb.mean()), "alt": float(np.quantile(d, 0.025)) if len(d) else None, "ust": float(np.quantile(d, 0.975)) if len(d) else None}


def uc_bh(p: List[Optional[float]], q: Optional[float] = None) -> List[Optional[float]]:
    """Benjamini-Hochberg düzeltilmiş p (HV._hv_bh aynen)."""
    return HV._hv_bh(p, float(q if q is not None else UC_ESIK["bh"]["q"]))


def uc_satir(Y: pd.DataFrame, anahtar: str) -> Dict[str, Any]:
    """Bir satır (seçili pencereler; hepsi TAMAM ve getirili): n, ay, R15, TOPLAM FARK / ZAMANLAMA / SEÇİM (ay kümeli), hedef payları, KAT."""
    A = uc_ay_ozet(Y.giris); out: Dict[str, Any] = {**A}
    if not len(Y):
        return out
    ay = _uc_ay(Y.giris); R = Y.R15.to_numpy(float); TF = R - Y.T1.to_numpy(float)
    pm = np.isfinite(Y.PIY.to_numpy(float)) & np.isfinite(Y.PIY_don.to_numpy(float))
    out["R15_ort"] = float(R.mean()); out["R15_med"] = float(np.median(R)); out["T1_ort"] = float(Y.T1.mean())
    out["TF"] = uc_boot(TF, ay, anahtar + "|TF"); out["TF_arti"] = float((TF > 0).mean())
    out["ZAM"] = uc_boot((Y.PIY - Y.PIY_don).to_numpy(float)[pm], ay[pm], anahtar + "|ZAM")
    out["SEC"] = uc_boot((R - Y.PIY.to_numpy(float))[pm], ay[pm], anahtar + "|SEC"); out["n_piy"] = int(pm.sum())
    for x in ("5", "10"):
        d = float(Y[f"d{x}"].mean()); tb = float(Y[f"tb{x}"].mean())
        out[f"d{x}"] = d; out[f"tb{x}"] = tb; out[f"KAT{x}"] = (d / tb) if tb > 0 else None
    return out


def _uc_tf(r: Dict[str, Any]) -> Dict[str, Any]:
    v = r.get("TF")
    return v if isinstance(v, dict) else {}


def _uc_pos(s: Optional[Dict[str, Any]]) -> bool:
    return bool(isinstance(s, dict) and s.get("ort") is not None and s.get("alt") is not None and s["ort"] > 0 and s["alt"] > 0)


def uc_hukum(kes: Dict[str, Any], dog: Dict[str, Any], avr: List[Dict[str, Any]], q_bh: Optional[float]) -> str:
    """UC_ESIK['hukum']['sira'] aynen."""
    n = dog.get("n") or 0; ay = dog.get("ay") or 0
    if n < 30 or ay < 12 or not _uc_tf(dog):
        return "ÖLÇÜLEMEDİ"
    k_ok = _uc_pos(_uc_tf(kes)); d_ok = _uc_pos(_uc_tf(dog))
    a_ok = all((_uc_tf(c).get("ort") or 0) > 0 for c in avr if (c.get("n") or 0) >= 10)
    b_ok = q_bh is not None and q_bh <= float(UC_ESIK["bh"]["q"])
    if k_ok and d_ok and b_ok and a_ok:
        return "TUTAR"
    if _uc_tf(dog).get("ust") is not None and _uc_tf(dog)["ust"] < 0:
        return "TERS"
    if k_ok and d_ok:
        return "KISMİ"
    if k_ok or d_ok:
        return "TEK DÖNEM"
    return "TUTMADI"


def uc_spearman5(y: List[Optional[float]]) -> Optional[float]:
    v = np.array([np.nan if a is None else a for a in y], float)
    if not np.isfinite(v).all():
        return None
    r = pd.Series(v).rank().to_numpy(); x = np.arange(1, 6, dtype=float)
    return float(np.corrcoef(x, r)[0, 1]) if np.std(r) > 0 else None


def uc_tablolar(X: pd.DataFrame, PJ: Dict[str, Any], TK: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Bütün satırlar, hüküm, BH, doz - yanıt, genel hüküm."""
    T = X[(X.durum == "TAMAM") & np.isfinite(X.R15.to_numpy(float)) & np.isfinite(X.T1.to_numpy(float))]
    sat: List[Dict[str, Any]] = []; hk: Dict[str, Any] = {}; doz: Dict[str, Any] = {}
    for ev in UC_EVREN:
        for z in UC_ZAMAN:
            G = T[(T.evren == ev) & (T.zaman == z)]
            for h in _UC_HUC:
                gh = G[G.hucre == h]
                sat.append({"evren": ev, "zaman": z, "satir": "HEPSI_PENCERE", "uc": "-", "hucre": h, **uc_satir(gh, f"{ev}|{z}|HEPSI|{h}")})
                for a in UC_SATIR + ["ONCEKI_DUSUS_B1"]:
                    for u in (UC_UC if a != "ONCEKI_DUSUS_B1" else ("UC10",)):
                        sel = gh[gh[f"{a}_{u}"].to_numpy(bool)]
                        sat.append({"evren": ev, "zaman": z, "satir": a, "uc": u, "hucre": h, **uc_satir(sel, f"{ev}|{z}|{a}|{u}|{h}")})
            for a in UC_SATIR:
                d = {}
                for h in ("ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022"):
                    gh = G[G.hucre == h]; b = gh[f"{a}_BES"].to_numpy(); TF = (gh.R15 - gh.T1).to_numpy(float)
                    d[h] = {"ort": [float(TF[b == i].mean()) if (b == i).any() else None for i in range(1, 6)], "n": [int((b == i).sum()) for i in range(1, 6)]}
                    d[h]["spearman"] = uc_spearman5(d[h]["ort"])
                sk, sd = d["ABD|d1619"]["spearman"], d["ABD|d2022"]["spearman"]
                d["okuma"] = ("TEK YÖNLÜ ARTIŞ" if (sk is not None and sd is not None and sk >= 0.9 and sd >= 0.9) else
                              "TEK YÖNLÜ AZALIŞ" if (sk is not None and sd is not None and sk <= -0.9 and sd <= -0.9) else "YOK")
                doz[f"{ev}|{z}|{a}"] = d
    S = pd.DataFrame(sat)
    idx = {(r["evren"], r["zaman"], r["satir"], r["uc"], r["hucre"]): i for i, r in S.iterrows()}
    aile = [(ev, z, a, u) for ev in UC_EVREN for z in UC_ZAMAN for a in UC_SATIR for u in UC_UC]
    pv = [(S.loc[idx[(ev, z, a, u, "ABD|d2022")], "TF"] or {}).get("p") if isinstance(S.loc[idx[(ev, z, a, u, "ABD|d2022")], "TF"], dict) else None
          for ev, z, a, u in aile]
    qv = uc_bh(pv)
    for (ev, z, a, u), p, q in zip(aile, pv, qv):
        r = lambda h: S.loc[idx[(ev, z, a, u, h)]].to_dict()
        kes, dog = r("ABD|d1619"), r("ABD|d2022"); avr = [r("AVR|d1619"), r("AVR|d2022")]
        hk[f"{ev}|{z}|{a}|{u}"] = {"evren": ev, "zaman": z, "satir": a, "uc": u, "p": p, "q_bh": q, "hukum": uc_hukum(kes, dog, avr, q),
                                   "doz": doz[f"{ev}|{z}|{a}"]["okuma"]}
    genel = {}
    for ev in UC_EVREN:
        for z in UC_ZAMAN:
            L = [v for v in hk.values() if v["evren"] == ev and v["zaman"] == z]
            genel[f"{ev}|{z}"] = _uc_genel(L, S, idx, ev, z)
    L = list(hk.values())
    if any(v["hukum"] == "TUTAR" for v in L):
        genel["hepsi"] = "AÇIK VERİDE ADAY (kasa açılmaz; ileri test)"
    elif any(v["hukum"] in ("TEK DÖNEM", "KISMİ") for v in L):
        genel["hepsi"] = "TUTARSIZ"
    else:
        genel["hepsi"] = genel["E2|gunluk"]
    return {"satir": S.to_dict("records"), "hukum": hk, "doz": doz, "genel": genel, "piyasa": PJ, "takvim": TK or {},
            "bh_gecen": [k for k, v in hk.items() if v["q_bh"] is not None and v["q_bh"] <= float(UC_ESIK["bh"]["q"])],
            "guc_yetersiz": [f"{ev}|{z}|{a}|{u}" for ev, z, a, u in aile if min(int(S.loc[idx[(ev, z, a, u, h)], "n"]) for h in ("ABD|d1619", "ABD|d2022")) < 1000]}


def _uc_genel(L: List[Dict[str, Any]], S: pd.DataFrame, idx: Dict[Any, int], ev: str, z: str) -> str:
    if any(v["hukum"] == "TUTAR" for v in L):
        return "AÇIK VERİDE ADAY (kasa açılmaz; ileri test)"
    if any(v["hukum"] in ("TEK DÖNEM", "KISMİ") for v in L):
        return "TUTARSIZ"
    guc = all(int(S.loc[idx[(ev, z, a, "UC10", h)], "n"]) >= 1000 for a in UC_SATIR if a != "B4_HEPSI_VE" for h in ("ABD|d1619", "ABD|d2022"))
    return f"UÇLARDA İZ YOK ({ev} {z})" if guc else "ÖLÇÜLEMEDİ"


def uc_takvim_hesap(X: pd.DataFrame) -> Dict[str, Any]:
    """Takvim (B3, B4; E2 günlük): durumlara göre PİYASA15 ve farklar (ay kümeli)."""
    out: Dict[str, Any] = {}
    for p in UC_PAZAR:
        Vd = uc_takvim_veri(p); M = HV.hv25_piyasa_matris(Vd); cal = M["cal"]
        for b in ("B3_HEPSI", "B4_HEPSI_VE"):
            sy, g, don = uc_takvim_seri(X, p, b, cal)
            P15 = np.array([HV.hv25_piyasa_R(M, int(i) + 1, int(i) + 15, [])[0] for i in g], float)
            ay = np.array([cal[i].strftime("%Y-%m") for i in g]); ds = _uc_durum(sy[g]); ok = np.isfinite(P15); R: Dict[str, Any] = {}
            for dn in ("d1619", "d2022"):
                m = ok & (don == dn); r: Dict[str, Any] = {"durum": {}, "fark": {}}
                for s_ in UC_ESIK["takvim"]["durum"]:
                    mm = m & (ds == s_); r["durum"][s_] = {"gun": int(mm.sum()), "ay": int(len(set(ay[mm]))), "ort": float(P15[mm].mean()) if mm.any() else None}
                z0 = m & (ds == "SAYI = 0")
                for ad, mm in (("(SAYI >= 1) - (SAYI = 0)", m & (ds != "SAYI = 0")), ("(SAYI = 1-5) - (SAYI = 0)", m & (ds == "SAYI = 1-5")),
                               ("(SAYI >= 6) - (SAYI = 0)", m & (ds == "SAYI >= 6"))):
                    yet = mm.sum() >= 30 and z0.sum() >= 30 and len(set(ay[mm])) >= 12 and len(set(ay[z0])) >= 12
                    f = uc_boot_fark(P15[mm], ay[mm], P15[z0], ay[z0], f"takvim|{p}|{b}|{dn}|{ad}")
                    r["fark"][ad] = {**f, "olculdu": bool(yet)}
                R[dn] = r
            F = [R[dn]["fark"]["(SAYI >= 1) - (SAYI = 0)"] for dn in ("d1619", "d2022")]
            if not all(f["olculdu"] for f in F):
                ok_ = "ÖLÇÜLEMEDİ"
            else:
                pz = [f["fark"] > 0 and f["alt"] > 0 for f in F]
                ok_ = ("PİYASA YÜKSELİŞİNİ ÖNCELİYOR" if all(pz) else "TEK DÖNEM" if any(pz) else
                       "GÖSTERİLEMEDİ (ters yönde)" if all(f["ust"] < 0 for f in F) else "GÖSTERİLEMEDİ")
            R["okuma"] = ok_; out[f"{p}|{b}"] = R
        del Vd, M; gc.collect()
    return out


# ================================================================ 7) ÖN KAYIT / KAPI / KOŞU / RAPOR
def uc_sha_simdi() -> Dict[str, str]:
    return {"KOD27_SHA": MI._mi_sha(UC_YOL["kod"]), "ESIK27_SHA": uc_esik_sha(), "HAVUZ_KOD_SHA": MI._mi_sha(UC_YOL["havuz_kod"]),
            "GZ_KOD_SHA": MI._mi_sha(os.path.join(KOK_UC, "MUM_IZI_GOZ.py")), "HAM8_SHA": MI._mi_sha(UC_YOL["ham8"]),
            "IS_TANIMI27_SHA": MI._mi_sha(UC_YOL["is_tanimi"])}


def uc_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or UC_YOL["cikti"]; yol = _uc_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise UCHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = uc_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise UCHata(f"ön kayıt kapısı (EK 27): {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_UC); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise UCHata("ön kayıt (EK 27) commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_UC.py"]):
        raise UCHata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def _uc_f(x: Any, n: int = 2, yuzde: bool = False) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    v = float(x) * (100 if yuzde else 1)
    return f"{v:.{n}f}".replace(".", ",")


def uc_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or UC_YOL["cikti"]; y = _uc_yol("onkayit", cikti)
    S = json.load(open(os.path.join(UC_YOL["gecici"], "sayim27.json"), encoding="utf-8"))
    KJ = json.load(open(os.path.join(UC_YOL["gecici"], "kesim27.json"), encoding="utf-8"))
    YN = open(os.path.join(UC_YOL["gecici"], "yorum27.md"), encoding="utf-8").read()
    AP = json.load(open(os.path.join(UC_YOL["gecici"], "appn27.json"), encoding="utf-8"))
    sh = {**uc_sha_simdi(), "KESIM27_SHA": uc_json_sha(KJ), "SAYIM27_SHA": uc_json_sha(S)}
    sh.update({f"PENCERE_{k}_SHA": v for k, v in S["pencere_sha"].items()})
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_UC.py"])
    kt = "\n".join(f"| {k} | {dict((r['kod'], r.get('ad', r['kod'])) for r in IK.IK_KONTROL)[k]} | {v[0]} | {v[1]} |" for k, v in UC_KONTROL.items())
    s = [f"# MUM_IZI27 ÖN KAYIT — UÇ PENCERELER: en küçük mumlu ve fitil şartları en radikal bölgeler ({MI._mi_simdi()})", "",
         "İş tanımı MUM_IZI27_IS_TANIMI.md. Bu dosya R15, T1, hedef payı, PİYASA ve takvim getirileri hesaplanmadan ÖNCE commit + push edilir; tanımlar, kesimler, "
         "hüküm kuralı sonra değişmez (değişirse SAPMA). Pencereler ve ölçüler getirisizdir; kesimler yalnız keşif (ABD 2016-19) örneğinden. Evren bugün yaşayan "
         "hisseler (yukarı yanlı). KASA açılmaz (veri <= 2022-12-31). 128 deneme (16 satır x 2 uç x 2 evren x 2 zaman dilimi).", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_UC.py commit'i: {kc or 'yok'}",
         f"- Pencere dosyaları: {UC_YOL['ham']}/pencere_<zaman>_<pazar>.pkl (repo dışı; sha yukarıda)", "",
         "## APPN sağlaması (MUM_IZI26_IKI_BOLGE.md elle hesaplanmış değerler; getiri yok)", "", *_uc_appn_tablo(AP), "",
         "## GETİRİSİZ SAYIM", "", *_uc_sayim_tablo(S), "",
         "## KEŞİF KESİMLERİ (ABD 2016-19; öteki hücrelere aynen)", "", *_uc_kesim_tablo(KJ), "",
         "## Yorum gerektiren noktalar (ölçümden ÖNCE sabit)", "", YN.strip(), "",
         "## Tanımlar (UC_ESIK; sha yukarıda)", "", "```", json.dumps(UC_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ", "", "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 27")


def _uc_appn_tablo(AP: Dict[str, Any]) -> List[str]:
    s = ["| ölçü | pencere | MUM_IZI26 değeri | MUM_IZI_UC | tolerans | sonuç |", "|---|---|---|---|---|---|"]
    for r in AP["satir"]:
        s.append(f"| {r['olcu']} | {r['pencere']} | {_uc_f(r['beklenen'], 3)} | {_uc_f(r['bulunan'], 3)} | {_uc_f(r['tol'], 3)} | {'TUTTU' if r['tuttu'] else 'TUTMADI'} |")
    s.append(f"- Genel: {'TUTTU' if AP['tuttu'] else 'TUTMADI'} ({sum(r['tuttu'] for r in AP['satir'])} / {len(AP['satir'])}); bilgi (MUM_IZI26'da yok): "
             + "; ".join(f"{k} {_uc_f(v, 3)}" for k, v in AP["bilgi"].items()))
    return s


def _uc_sayim_tablo(S: Dict[str, Any]) -> List[str]:
    nd = UC_ESIK["atma"]["sira"]
    s = ["### Huni: evren x zaman dilimi x pazar (pencere sayısı ve atılma nedeni; her pencereye ilk tutan neden)", "",
         "| evren\\|zaman\\|pazar | toplam | " + " | ".join(nd) + " | TAMAM |", "|---|---|" + "---|" * (len(nd) + 1)]
    for k, v in S["huni"].items():
        s.append(f"| {k} | {v['toplam']} | " + " | ".join(str(v.get(a, 0)) for a in nd) + f" | {v.get('TAMAM', 0)} |")
    if S.get("E1"):
        s += ["", f"- E1 huni: R4 ham {S['E1']['ham_hepsi']}, evren içi {S['E1']['ham_evren']}, 15 bar tekil atılan {S['E1']['tekil_atilan']}, kalan {S['E1']['tekil']}"]
    s += ["", "### TAMAM pencereler hücreye göre (n, farklı ay, en kalabalık 3 ay payı)", "", "| evren\\|zaman | " + " | ".join(_UC_HUC) + " |", "|---|" + "---|" * len(_UC_HUC)]
    for k, v in S["hucre"].items():
        s.append(f"| {k} | " + " | ".join(f"{v[h]['n']} / {v[h]['ay']} / {_uc_f(v[h]['ust3_pay'], 2)}" for h in _UC_HUC) + " |")
    s += ["", "### Uçta kalan TAMAM pencere sayısı / farklı ay (karar hücreleri)", ""]
    for k, v in S["uc"].items():
        s += [f"#### {k}", "", "| satır\\|uç | ABD 2016-19 | ABD 2020-22 | AVR 2016-19 | AVR 2020-22 | BIST 2016-19 | BIST 2020-22 | ABD o16 | AVR o16 |", "|---|---|---|---|---|---|---|---|---|"]
        for a, w in v.items():
            s.append(f"| {a} | " + " | ".join(f"{w[h]['n']} / {w[h]['ay']}" for h in _UC_HUC[:8]) + " |")
        s.append("")
    s += ["### B4 (hepsi birden uç %30'unda) TAMAM pencere sayısı", "", "| evren\\|zaman | " + " | ".join(_UC_HUC) + " |", "|---|" + "---|" * len(_UC_HUC)]
    for k, v in S["B4"].items():
        s.append(f"| {k} | " + " | ".join(str(v[h]) for h in _UC_HUC) + " |")
    s += ["", "### Ölçüler arası sıra ilişkisi (Spearman; keşif hücresi)", ""]
    kis = {a: f"{i + 1}" for i, a in enumerate(UC_OLCU_AD)}
    for k, R in S["spearman"].items():
        s += [f"#### {k} (1 {UC_OLCU_AD[0]} .. 12 {UC_OLCU_AD[-1]}; numara sırası ölçü listesi)", "", "| | " + " | ".join(kis[a] for a in UC_OLCU_AD) + " |",
              "|---|" + "---|" * 12]
        for a in UC_OLCU_AD:
            s.append(f"| {kis[a]} {a} | " + " | ".join(_uc_f(R[a][b], 2) for b in UC_OLCU_AD) + " |")
        s.append("")
    s += ["### Bilgi: fiyat adımı / birim (keşif hücresi; UÇ2 pencereleri; hükme girmez)", "",
          "| evren\\|zaman | satır | n | gövdesiz (O = C) mum payı ort | gövdesiz payı >= 0,5 pencere payı | fiyat medyanı | fiyat < 5 payı |", "|---|---|---|---|---|---|---|"]
    for k, v in S.get("adim", {}).items():
        for a, w in v.items():
            if w.get("n"):
                s.append(f"| {k} | {a} | {w['n']} | {_uc_f(w['govdesiz_ort'], 3)} | {_uc_f(w['govdesiz_yarim_pay'], 3)} | {_uc_f(w['fiyat_medyan'], 2)} | "
                         f"{_uc_f(w['fiyat_5_alti_pay'], 3)} |")
    s += ["", "### Takvim durumları (gün sayısı; E2 günlük; getirisiz)", "", "| pazar\\|bileşik | dönem | SAYI = 0 | SAYI = 1-5 | SAYI >= 6 |", "|---|---|---|---|---|"]
    for k, v in S["takvim"].items():
        for d, w in v.items():
            s.append(f"| {k} | {d} | " + " | ".join(str(w[x]) for x in UC_ESIK["takvim"]["durum"]) + " |")
    return s


def _uc_kesim_tablo(KJ: Dict[str, Any]) -> List[str]:
    s = []
    for k, v in KJ.items():
        s += [f"### {k} (keşif TAMAM n = {v['n_kesif']}; değerler ham ölçü biriminde, uç yönüyle)", "",
              "| ölçü | yön | n | UÇ10 sınırı | UÇ2 sınırı | beşlik sınırları (skor) | B4 %30 / %10 |", "|---|---|---|---|---|---|---|"]
        for a, y in UC_OLCU:
            o = v["olcu"][a]; f = (lambda z: -z) if y == "KUCUK" else (lambda z: z)
            s.append(f"| {a} | {y} | {o['n']} | {_uc_f(f(o['UC10']), 4)} | {_uc_f(f(o['UC2']), 4)} | " + " / ".join(_uc_f(b, 4) for b in o["besli"]) +
                     f" | {_uc_f(f(o['B4_30']), 4)} / {_uc_f(f(o['B4_10']), 4)} |")
        for b, o in v["bilesik"].items():
            s.append(f"| {b} | BUYUK | {o['n']} | {_uc_f(o.get('UC10'), 4)} | {_uc_f(o.get('UC2'), 4)} | " + " / ".join(_uc_f(x, 4) for x in o["besli"]) + " | - |")
        s.append("")
    s.append("- KUCUK yönlü ölçülerde sınır ham değerdir (uç = değer <= sınır); BUYUK yönlülerde uç = değer >= sınır. BANT_SON değeri -|ham - 0,85|. Beşlik "
             "sınırları uç skorundadır (KUCUK yönlüde -değer).")
    return s


# ---------------------------------------------------------------- APPN sağlaması
UC_APPN = {"sembol": "APPN", "SOL": ("2021-05-07", "2021-06-07", 21), "SAG": ("2021-08-16", "2021-09-07", 16),
           "beklenen": {"SOL": {"BOY_YUZDE_ORAN": 0.95, "BOY_MUTLAK": 7.06, "GOVDE_ORAN": 0.83, "BOY_GRAFIK_ORAN": 0.50, "GOVDE_BOY": 0.42, "UST_ALT_PAY": 10 / 21,
                                "DARALMA": -0.55, "BANT_SON_ham": 0.54},
                        "SAG": {"BOY_YUZDE_ORAN": 0.63, "BOY_MUTLAK": 4.13, "GOVDE_ORAN": 0.58, "BOY_GRAFIK_ORAN": 0.57, "GOVDE_BOY": 0.42, "UST_ALT_PAY": 12 / 16,
                                "DARALMA": -0.43, "BANT_SON_ham": 0.60}},
           "tol": {"BOY_MUTLAK": 0.006, "UST_ALT_PAY": 1e-9, "DARALMA": 0.006, "_": 0.006}}


def uc_appn(D: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    if D is None:
        D = MI.mi_veri("ABD", MV.MV_YOL["gunluk"])["V"][UC_APPN["sembol"]]
    Db = uc_bar(D.Open, D.High, D.Low, D.Close); sat = []; bilgi = {}
    for ad in ("SOL", "SAG"):
        a, b, m = UC_APPN[ad]; s = int(D.index.get_loc(pd.Timestamp(a))); t = int(D.index.get_loc(pd.Timestamp(b)))
        if t - s + 1 != m:
            raise UCHata(f"APPN {ad}: pencere {t - s + 1} bar (beklenen {m})")
        O = uc_olcu(Db, [t], m)
        for k, v in UC_APPN["beklenen"][ad].items():
            tol = UC_APPN["tol"].get(k, UC_APPN["tol"]["_"]); f = float(O[k][0])
            tut = abs(round(f, 2) - v) <= tol if k not in ("UST_ALT_PAY",) else abs(f - v) <= tol
            sat.append({"olcu": k, "pencere": f"{ad} {a}..{b} ({m})", "beklenen": v, "bulunan": f, "tol": tol, "tuttu": bool(tut)})
        for k in ("UST_FITIL", "ALT_FITIL", "SON_UST_FITIL", "ONCEKI_DUSUS", "BANT_SON"):
            bilgi[f"{ad} {k}"] = float(O[k][0])
    return {"satir": sat, "tuttu": all(r["tuttu"] for r in sat), "bilgi": bilgi}


# ---------------------------------------------------------------- koşu
UC_OLAY_KOL = ["evren", "zaman", "pazar", "sembol", "t", "m", "bas", "son", "giris", "son15", "hucre", "durum", "E0", "stop", "R15", "d5", "d10", "T1", "tb5", "tb10",
               "PIY", "PIY_don"]


def uc_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or UC_YOL["cikti"]
    if os.path.exists(_uc_yol("sonuc", cikti)):
        raise UCHata("sonuç zaten var (ikinci koşu DURUR)")
    G0 = uc_kapi(cikti); metin = open(_uc_yol("onkayit", cikti), encoding="utf-8").read()
    P0 = json.load(open(os.path.join(UC_YOL["ham"], "pencere_ozet.json"), encoding="utf-8"))
    for k, v in P0["sha"].items():
        if f"PENCERE_{k}_SHA: {v}" not in metin:
            raise UCHata(f"K9: pencere {k} sha ön kayıtta yok")
    X0 = uc_pencere_yukle(P0["sha"]); X, KS = uc_hazir(X0); KJ = uc_kesim_json(KS)
    if f"KESIM27_SHA: {uc_json_sha(KJ)}" not in metin:
        raise UCHata("K9: kesimler ön kayıttakiyle aynı değil -> DURDU")
    parca = []; PJ = {}
    for z in UC_ZAMAN:
        for p in UC_PAZAR:
            Y, pj = uc_getiri_blok(z, p, X); parca.append(Y); PJ[f"{z}|{p}"] = pj; uclog.info("getiri %s %s: %d (%.0f sn)", z, p, len(Y), time.time() - t0)
    G = pd.concat(parca)
    for c in ("R15", "d5", "d10", "T1", "tb5", "tb10", "PIY", "PIY_don"):
        X[c] = np.nan
        X.loc[G.index, c] = G[c]
    TK = uc_takvim_hesap(X); T = uc_tablolar(X, PJ, TK)
    os.makedirs(UC_YOL["ham"], exist_ok=True); oy = os.path.join(UC_YOL["ham"], "olay27.pkl")
    kol = UC_OLAY_KOL + UC_OLCU_AD + UC_EK_KOL + [c for c in X.columns if c.endswith(("_UC10", "_UC2", "_BES", "_DEG"))]
    X[kol].to_pickle(oy + ".tmp"); os.replace(oy + ".tmp", oy)
    J = {"surum": UC_SURUM, "kapi": G0, "esik_sha": uc_esik_sha(), "kesim": KJ, "tablo": T, "olay_dosya": oy, "olay_sha": MI._mi_sha(oy),
         "olay_n": int(len(X)), "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_uc_yol("sonuc", cikti), J, "sonuç 27")
    uc_ozet_csv(J, cikti)
    return J


def uc_ozet_csv(J: Dict[str, Any], cikti: Optional[str] = None) -> str:
    rows = []
    for r in J["tablo"]["satir"]:
        d = {k: r.get(k) for k in ("evren", "zaman", "satir", "uc", "hucre", "n", "ay", "ust3_pay", "R15_ort", "R15_med", "T1_ort", "TF_arti", "n_piy",
                                    "d5", "tb5", "KAT5", "d10", "tb10", "KAT10")}
        for m in ("TF", "ZAM", "SEC"):
            b = r.get(m) if isinstance(r.get(m), dict) else {}
            for k in ("ort", "medyan", "alt", "ust", "p"):
                d[f"{m}_{k}"] = b.get(k)
        h = J["tablo"]["hukum"].get(f"{r['evren']}|{r['zaman']}|{r['satir']}|{r['uc']}")
        d["hukum"] = h["hukum"] if h else ""; d["q_bh"] = h["q_bh"] if h else None; d["doz"] = h["doz"] if h else ""
        rows.append(d)
    y = _uc_yol("ozet", cikti); pd.DataFrame(rows).to_csv(y + ".tmp", index=False, float_format="%.6g"); os.replace(y + ".tmp", y)
    return y


def _uc_b(b: Any, yuzde: bool = True) -> str:
    if not isinstance(b, dict) or b.get("ort") is None:
        return "-"
    return f"{_uc_f(b['ort'], 2, yuzde)} [{_uc_f(b.get('alt'), 2, yuzde)}; {_uc_f(b.get('ust'), 2, yuzde)}]"


def uc_rapor_tablo(J: Dict[str, Any]) -> str:
    T = J["tablo"]; S = pd.DataFrame(T["satir"]); s = []
    ix = {(r.evren, r.zaman, r.satir, r.uc, r.hucre): r for r in S.itertuples()}
    for ev in UC_EVREN:
        for z in UC_ZAMAN:
            s += [f"### OLASILIK TABLOSU {ev} {z} (genel: {T['genel'][f'{ev}|{z}']})", "",
                  "| satır | uç | keşif n | keşif TOPLAM FARK [%95] | doğr. n / ay | doğr. TOPLAM FARK [%95] | doğr. +%5 payı | taban payı | KAT | AVR 16-19 n / TF | "
                  "AVR 20-22 n / TF | q (BH) | hüküm | doz |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
            for a in ["HEPSI_PENCERE"] + UC_SATIR + ["ONCEKI_DUSUS_B1"]:
                for u in (("-",) if a == "HEPSI_PENCERE" else ("UC10",) if a == "ONCEKI_DUSUS_B1" else UC_UC):
                    k, d = ix[(ev, z, a, u, "ABD|d1619")], ix[(ev, z, a, u, "ABD|d2022")]; a1, a2 = ix[(ev, z, a, u, "AVR|d1619")], ix[(ev, z, a, u, "AVR|d2022")]
                    h = T["hukum"].get(f"{ev}|{z}|{a}|{u}", {})
                    s.append(f"| {a} | {u} | {k.n} | {_uc_b(k.TF)} | {d.n} / {d.ay} | {_uc_b(d.TF)} | {_uc_f(getattr(d, 'd5', None), 1, True)} | "
                             f"{_uc_f(getattr(d, 'tb5', None), 1, True)} | {_uc_f(getattr(d, 'KAT5', None), 2)} | {a1.n} / {_uc_f((a1.TF or {}).get('ort') if isinstance(a1.TF, dict) else None, 2, True)} | "
                             f"{a2.n} / {_uc_f((a2.TF or {}).get('ort') if isinstance(a2.TF, dict) else None, 2, True)} | {_uc_f(h.get('q_bh'), 3)} | "
                             f"{h.get('hukum', 'bilgi')} | {h.get('doz', '-')} |")
            s.append("")
    s += ["### ZAMANLAMA ve SEÇİM (E2 günlük; keşif / doğrulama)", "", "| satır | uç | keşif ZAMANLAMA | keşif SEÇİM | doğr. ZAMANLAMA | doğr. SEÇİM |", "|---|---|---|---|---|---|"]
    for a in ["HEPSI_PENCERE"] + UC_SATIR:
        for u in (("-",) if a == "HEPSI_PENCERE" else UC_UC):
            k, d = ix[("E2", "gunluk", a, u, "ABD|d1619")], ix[("E2", "gunluk", a, u, "ABD|d2022")]
            s.append(f"| {a} | {u} | {_uc_b(k.ZAM)} | {_uc_b(k.SEC)} | {_uc_b(d.ZAM)} | {_uc_b(d.SEC)} |")
    s += ["", "### DOZ - YANIT (beşlik TOPLAM FARK ortalaması, puan; 1 = en az uç, 5 = en uç)", "", "| evren\\|zaman\\|satır | keşif 1..5 | ρ | doğr. 1..5 | ρ | okuma |",
          "|---|---|---|---|---|---|"]
    for k, d in T["doz"].items():
        f = lambda h: " / ".join(_uc_f(x, 2, True) for x in d[h]["ort"])
        s.append(f"| {k} | {f('ABD|d1619')} | {_uc_f(d['ABD|d1619']['spearman'], 2)} | {f('ABD|d2022')} | {_uc_f(d['ABD|d2022']['spearman'], 2)} | {d['okuma']} |")
    s += ["", "### TAKVİM (B3 / B4 UÇ10, E2 günlük): pazarın sonraki 15 günü (PİYASA15) durumlara göre", "",
          "| pazar\\|bileşik | dönem | SAYI = 0 gün / ort | 1-5 gün / ort | >= 6 gün / ort | (>= 1) - (0) [%95] | (1-5) - (0) | (>= 6) - (0) | okuma |", "|---|---|---|---|---|---|---|---|---|"]
    for k, R in T["takvim"].items():
        for dn in ("d1619", "d2022"):
            r = R[dn]; du = r["durum"]
            ff = lambda ad: (f"{_uc_f(r['fark'][ad]['fark'], 2, True)} [{_uc_f(r['fark'][ad]['alt'], 2, True)}; {_uc_f(r['fark'][ad]['ust'], 2, True)}]"
                             + ("" if r["fark"][ad]["olculdu"] else " (ölçülemedi)"))
            s.append(f"| {k} | {dn} | " + " | ".join(f"{du[x]['gun']} / {_uc_f(du[x]['ort'], 2, True)}" for x in UC_ESIK["takvim"]["durum"]) +
                     f" | {ff('(SAYI >= 1) - (SAYI = 0)')} | {ff('(SAYI = 1-5) - (SAYI = 0)')} | {ff('(SAYI >= 6) - (SAYI = 0)')} | {R['okuma']} |")
    s += ["", f"- BH q 0,10'u geçen satırlar: {', '.join(T['bh_gecen']) if T['bh_gecen'] else 'yok'}",
          f"- Güç yetersiz (keşif ya da doğrulama n < 1.000) satırlar: {len(T.get('guc_yetersiz', []))} / 128",
          f"- Hüküm sayıları: {pd.Series([v['hukum'] for v in T['hukum'].values()]).value_counts().to_dict()}", f"- GENEL: {T['genel']}"]
    return "\n".join(s)


def uc_png(J: Dict[str, Any], cikti: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    T = J["tablo"]; S = pd.DataFrame(T["satir"]); ix = {(r.evren, r.zaman, r.satir, r.uc, r.hucre): r for r in S.itertuples()}
    ad_tr = {"BOY_YUZDE_ORAN": "Mum boyu (% , önceki 120'ye göre)", "BOY_GRAFIK_ORAN": "Mum boyu (grafikte, önceki 120'ye göre)", "BOY_MUTLAK": "Mum boyu (% mutlak)",
             "GOVDE_ORAN": "Gövde (önceki 120'ye göre)", "GOVDE_BOY": "Gövde / boy", "UST_FITIL": "Üst fitil uzun", "ALT_FITIL": "Alt fitil kısa",
             "UST_ALT_PAY": "Üst fitil > alt fitil payı", "SON_UST_FITIL": "Son 1/3 üst fitil uzun", "DARALMA": "Bollinger daralması",
             "BANT_SON": "Son 1/3 üst bandın hemen altında", "ONCEKI_DUSUS": "Öncesinde derin düşüş", "B1_KUCUK_MUM": "B1 küçük mum (1-5)",
             "B2_FITIL": "B2 fitil (6-9)", "B3_HEPSI": "B3 hepsi (1-11)", "B4_HEPSI_VE": "B4 altısı birden"}
    fig, axs = plt.subplots(1, 2, figsize=(9, 16), sharey=True); y = np.arange(len(UC_SATIR))[::-1]
    for ax, u in zip(axs, UC_UC):
        for j, (h, renk, ofs, et) in enumerate((("ABD|d1619", "#4C78A8", 0.18, "keşif ABD 2016-19"), ("ABD|d2022", "#E45756", -0.18, "doğrulama ABD 2020-22"))):
            v = []; lo = []; hi = []
            for a in UC_SATIR:
                b = getattr(ix[("E2", "gunluk", a, u, h)], "TF"); b = b if isinstance(b, dict) else {}
                v.append(100 * (b.get("ort") or np.nan)); lo.append(100 * (b.get("alt") if b.get("alt") is not None else np.nan)); hi.append(100 * (b.get("ust") if b.get("ust") is not None else np.nan))
            v = np.array(v); lo = np.array(lo); hi = np.array(hi)
            ax.barh(y + ofs, v, height=0.34, color=renk, label=et)
            ax.errorbar(v, y + ofs, xerr=[np.nan_to_num(v - lo), np.nan_to_num(hi - v)], fmt="none", ecolor="#333333", elinewidth=0.8, capsize=2)
        ax.axvline(0, color="black", lw=0.8); ax.set_title({"UC10": "En uç %10", "UC2": "En uç %2"}[u], fontsize=14)
        ax.set_xlabel("Rastgele güne göre fark (15 mum, puan)", fontsize=10); ax.grid(axis="x", alpha=0.3)
        for i, a in enumerate(UC_SATIR):
            hk = T["hukum"][f"E2|gunluk|{a}|{u}"]["hukum"]
            ax.text(1.01, y[i], hk, transform=ax.get_yaxis_transform(), fontsize=8, va="center", color="#B22222" if hk in ("TERS",) else "#2E7D32" if hk == "TUTAR" else "#555555")
    axs[0].set_yticks(y); axs[0].set_yticklabels([ad_tr[a] for a in UC_SATIR], fontsize=10)
    axs[0].legend(loc="lower left", fontsize=9)
    fig.suptitle(f"Uç pencereler (her 16 mumluk pencere, günlük): sonrası rastgele güne göre\nGENEL: {T['genel']['hepsi']}", fontsize=13)
    fig.text(0.02, 0.005, "Çubuk = 15 mumluk getiri eksi aynı hissenin rastgele günü (puan); çizgi = %95 aralık (ay kümeli). Sağdaki etiket = önceden yazılı hüküm. "
                          "Evren bugün yaşayanlar.", fontsize=8, wrap=True)
    fig.tight_layout(rect=(0, 0.02, 0.93, 0.95))
    y_ = _uc_yol("png", cikti); fig.savefig(y_, dpi=110); plt.close(fig)
    return y_


def uc_rapor_yaz(cikti: Optional[str] = None) -> str:
    J = json.load(open(_uc_yol("sonuc", cikti), encoding="utf-8")); os.makedirs(UC_YOL["gecici"], exist_ok=True)
    uc_png(J, cikti)
    return MI._mi_yaz(os.path.join(UC_YOL["gecici"], "rapor_tablo27.md"), uc_rapor_tablo(J), "rapor tablo 27")


# ================================================================ 8) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_uc(_once=_CK_ONCE_UC, _dosya="MUM_IZI_UC.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_UC",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_uc()


def _uc_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_UC")
    ap.add_argument("komut", choices=["appn", "pencere", "sayim", "onkayit", "kos", "rapor", "sha"])
    a = ap.parse_args(argv)
    try:
        os.makedirs(UC_YOL["gecici"], exist_ok=True)
        if a.komut == "appn":
            AP = uc_appn(); MI._mi_jyaz(os.path.join(UC_YOL["gecici"], "appn27.json"), AP, "appn 27"); print(json.dumps(MI._mi_json(AP), ensure_ascii=False, indent=1))
        elif a.komut == "pencere":
            print(json.dumps(MI._mi_json(uc_pencere_kos()), ensure_ascii=False, indent=1))
        elif a.komut == "sayim":
            _, S, KS = uc_sayim_kos(); KJ = uc_kesim_json(KS)
            MI._mi_jyaz(os.path.join(UC_YOL["gecici"], "sayim27.json"), S, "sayım 27"); MI._mi_jyaz(os.path.join(UC_YOL["gecici"], "kesim27.json"), KJ, "kesim 27")
            print(json.dumps(MI._mi_json({"huni": S["huni"], "SAYIM27_SHA": uc_json_sha(S), "KESIM27_SHA": uc_json_sha(KJ)}), ensure_ascii=False, indent=1))
        elif a.komut == "onkayit":
            print(uc_onkayit_yaz())
        elif a.komut == "kos":
            J = uc_kos(); print(json.dumps(MI._mi_json({"genel": J["tablo"]["genel"], "bh": J["tablo"]["bh_gecen"], "sure_sn": J["sure_sn"]}), ensure_ascii=False, indent=1))
        elif a.komut == "rapor":
            print(uc_rapor_yaz())
        elif a.komut == "sha":
            print(json.dumps(uc_sha_simdi(), indent=1))
    except UCHata as ex:
        uclog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_uc_ana())
