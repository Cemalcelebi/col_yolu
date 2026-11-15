# =====================================================================
#  IZ_KARNE.py — ÇÖL YOLU çalışma indeksi + "tek cetvel" iz yeniden denetimi
# ---------------------------------------------------------------------
#  CEMAL (24 Eki 2026): "İz defterine bir indeks yaz: hangi çalışmayı ne zaman yaptık, adı neydi, neler vardı, neler yoktu.
#  Her şey karıştı; öncesinde iz dediğin sonrasında iz olmuyor. Neler izdir, neler değildir, kesinleştirelim. En basitinden
#  en karmaşığa adım adım; yaptığımızı indekse yaz; indeks metrik geliştirmede kendini yenilesin."
#
#  Bu dosya üç iş yapar:
#   1) IK_KAYIT: Eylül 2026'dan bu yana yapılan BÜTÜN çalışmaların kaydı (kod Ç01..; tarih, dosya, soru, eski karar, defter
#      maddesi, seviye). Yeni her çalışma buraya bir satır ekler (test_iz_karne bunu zorlar).
#   2) TEK CETVEL: eski kararlar farklı cetvellerle verilmişti (ar60 / piy / her 5. gün tabanı / eşli taban; 17-21 & 22-26 /
#      2023 & 2024-26; ABD'li / ABD'siz). Burada her iz AYNI kuralla yeniden puanlanır:
#        - olay: sinyal (bilgi) günü; giriş ertesi işlem günü açılışı; hisse başına 60 işlem gününde (~87 takvim günü) tek olay
#        - sonuç: k20 = 60 barda önce +%20 mi (-%10'dan önce); dus = 60 barda önce -%20 mi (+%20'den önce);
#                 trail = üretim çıkışı getirisi (+%8 sonrası maliyet stopu, +%20 sonrası SMA20 trail, 120 bar, -%0,4 maliyet)
#        - kıyas: EŞLİ TABAN = her hissenin her 5. günü, olayla aynı ay x 60 gün momentum beşliği x likidite üçlüsü hücresinde
#                 (FON_IZI K10 ile aynı); kat = olay oranı / eşli oran
#        - hücreler: BIST 2016-22, BIST 2023, BIST 2024-26, ABD 2016-22, ABD 2023, ABD 2024-26 (giriş tarihine göre)
#        - KARAR (sonuç görülmeden yazıldı, CLAUDE.md test standardı):
#            İZ          : 4 karar hücresinde (BIST 2023, BIST 2024-26, ABD 2023, ABD 2024-26) ana kat >= 1,3, her hücrede
#                          n >= 30, ters yön katı < 1,3 (oynaklık değil), BIST 2016-22 ters işaretli değil (kat >= 1,0)
#            ADAY        : 4 karar hücresinin 3'ünde >= 1,3, hiçbirinde < 1,0
#            BIST-ADAY   : ABD verisi yok (KAP vb.); BIST 3 dönemde ana kat >= 1,3, n >= 30, ters < 1,3
#            KÜÇÜK ÖRNEK : kat şartı tutuyor ama bir karar hücresinde n < 30
#            İZ DEĞİL    : diğer her durum
#        - Ana ölçü yöne göre: 'yukari' iz -> k20, 'asagi' (kaçınma/risk) iz -> dus, 'koruma' (riski DÜŞÜK iddiası) -> dus
#          ve kat <= 1/1,3 (0,77) olmalı; ters (k20) katı da <= 0,77 ise yalnız oynaklık düşüklüğüdür, iz sayılmaz.
#   3) İNDEKS: IZ_DEFTERI.md başındaki "0. İNDEKS" bölümü bu dosyadan üretilir (iki işaret arası). Elle düzenlenmez;
#      `python IZ_KARNE.py indeks` yeniden yazar, `python IZ_KARNE.py seviye N` puanlar ve indeksi yeniler.
#
#  Seviyeler (en basitten karmaşığa): 1 tek gün fiyat-hacim olayı · 2 çok günlük şekil/tespit · 3 dış veri (KAP, fon raporu)
#  · 4 sistem/çıkış/portföy kuralı · 0 altyapı/ölçüm (iz iddiası yok).
#  Veri: BIST 581 + ABD 1411 hisse (FON_IZI.fi_k1_veri, bölünme düzeltmeli); KAP özeti (kap_ozet, 2017-2026).
#  Sürüm: v1.0 (2026-10-24)
# =====================================================================
from __future__ import annotations

import hashlib
import inspect
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_CK_ONCE_IK = {k: id(v) for k, v in globals().items()}

IK_SURUM = "IZ_KARNE v1.0 (2026-10-24, indeks + tek cetvel yeniden denetim)"
iklog = logging.getLogger("iz_karne")

_IK_KOK = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/content/drive/MyDrive/col_tarayici"
if _IK_KOK not in sys.path:
    sys.path.insert(0, _IK_KOK)


@dataclass
class IKAyar:
    veri: Dict[str, str] = field(default_factory=lambda: {
        "BIST": os.environ.get("IK_VERI_BIST", "/content/drive/MyDrive/col_tarayici/veri_1d_turkey.pkl"),
        "ABD": os.environ.get("IK_VERI_ABD", "/content/drive/MyDrive/col_tarayici/veri_1d_america.pkl")})
    kap: str = os.environ.get("IK_KAP", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/kap_ozet")
    kok: str = _IK_KOK
    cikti: str = os.path.join(_IK_KOK, "arastirma_cikti", "iz_karne")
    onbellek: str = os.environ.get("IK_ONBELLEK", os.path.join(_IK_KOK, "arastirma_cikti", "iz_karne", "onbellek"))
    defter: str = os.path.join(_IK_KOK, "IZ_DEFTERI.md")
    tekrar: int = 60                 # hisse başına olaylar arası en az işlem günü
    n_min: int = 30
    kat_esik: float = 1.3


IK_DONEM = [("2016-22", "2016-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31")]
IK_KARAR_HUCRE = [("BIST", "2023"), ("BIST", "2024-26"), ("ABD", "2023"), ("ABD", "2024-26")]
IK_ISARET = ("<!-- IZ_KARNE INDEKS BASLA (otomatik; elle duzenleme, `python IZ_KARNE.py indeks`) -->",
             "<!-- IZ_KARNE INDEKS BITTI -->")
IK_YON_IM = {"yukari": "↑ önce +%20", "asagi": "↓ önce −%20", "koruma": "⊥ önce −%20 düşük"}
IK_SEVIYE_AD = {0: "altyapı / ölçüm", 1: "tek gün fiyat-hacim", 2: "çok günlük şekil / tespit", 3: "dış veri (KAP, fon)",
                4: "sistem / çıkış / portföy"}


def _ik_k(kod, tarih, ad, dosya, soru, eski, defter="", seviye=0, sinyal="", yon="", cikti="", notu=""):
    return {"kod": kod, "tarih": tarih, "ad": ad, "dosya": dosya, "soru": soru, "eski": eski, "defter": defter,
            "seviye": seviye, "sinyal": sinyal, "yon": yon, "cikti": cikti, "not": notu}


# ---------------------------------------------------------------- 1) ÇALIŞMA KAYDI (indeksin kaynağı)
# sinyal: IK_SINYAL anahtarı (tek cetvelle puanlanabiliyorsa); boşsa neden 'not'ta yazılı. Sıra kronolojik.
IK_KAYIT: List[Dict[str, Any]] = [
    _ik_k("Ç01", "2026-09", "Giriş noktası / zamanlaması", "giris_testleri.py, kirilim_sonrasi.py, mfe_analiz.py",
       "Tavan tanımı, teyit, retest, kırılım hacmi, ilk 8 bar kırılımda girmeyi geçer mi?", "KAPALI: hiçbiri geçmedi",
       "COL_OZET §3", 4, notu="Kapalı konu (CLAUDE.md). Sistem kuralı, olay izi değil. Denetim 24 Eki: mfe_analiz 'stopsuz' satırı "
       "stoplardan farklı örneklemdendi (stop maliyeti ~2 kat abartılı: +19,3 → aynı örneklemde +10,2); yön aynı, düzeltildi."),
    _ik_k("Ç02", "2026-09", "Aday filtreleri (E_ONC, üç şart kapısı, taban kırılması düşürme)", "COL_v1.py (eski sürümler arsiv/)",
       "Kırılım öncesi eleme kâr ekler mi?", "KAPALI: her filtre para kaybettirdi", "COL_OZET §3, §4 ders 1", 4),
    _ik_k("Ç03", "2026-09", "Çıkış varyantları (fiyat/zaman stopu, desen sat, şelale, SMA200)", "STOP_TEST.py, selale.py",
       "Trail SMA20'yi yenen çıkış var mı?", "KAPALI: trail SMA20 en iyi", "COL_OZET §3", 4),
    _ik_k("Ç04", "2026-09", "Segment / şekil 90+ ölçü (alt iğne, doji, dar hafta…)", "COL_v1.py",
       "Çöl şekli sonrasını ayırır mı?", "Alt fitil<0,12, doji, dar hafta boyut çarpanı olarak TUTAN; diğerleri fark yok",
       "COL_OZET §3, §9.2", 2, notu="Eylül ölçümü (tekilsiz, maliyetsiz); col_ogren'de doji ayırmadı → yeniden doğrulanmadı."),
    _ik_k("Ç05", "2026-09", "Rejim / dış veri (CDS, EEM, VIX, DXY, temel)", "rejim.py, temel.py",
       "Piyasa rejimi sinyal sonucunu değiştirir mi?", "CDS ve borç/öz çarpan; VIX/DXY/USDTRY tutarsız (KAPALI)", "COL_OZET §3", 3),
    _ik_k("Ç06", "2026-09", "4h / haftalık / KNN", "col_atilim_TEK.py (arşiv)", "Başka zaman dilimi ya da ML kâr ekler mi?",
       "KAPALI: rejime bağlı, ML kâr eklemedi", "COL_OZET §3", 4),
    _ik_k("Ç07", "2026-09-18", "Göz kalibrasyonu v3 (29 çöl + 8 olumsuz)", "KALIBRE.py, kalibrasyon.py",
       "Kod Cemal'in çöllerini buluyor mu?", "Ölçüm: eski 13/26, v3 23/26; şekil olumsuzu ayırmıyor", "COL_OZET §7", 0),
    _ik_k("Ç08", "2026-09-18", "Kod denetimi (12 sorun)", "DENETIM.py", "Sonucu şişiren hata var mı?",
       "Düzeltildi: tekil işlem, ertesi açılış, drawdown", "COL_OZET §6", 0),
    _ik_k("Ç09", "2026-09-25", "Dört set ölçümü (sıcak sektör, momentum, onc250, konum250, taban koruması, çöl kalitesi)", "OLCUM.py",
       "Aday özellikleri 4 sette beklentiyi artırır mı?", "KAPALI: oynaklık, iz yok", "COL_OZET §8", 2),
    _ik_k("Ç10", "2026-09-25", "QMLS salınım / genç halka arz 3. dip", "QMLS_Tarayici (Drive)", "3. dip alımı çalışır mı?",
       "AÇIK: bek +1,6 (n 105), 1h veri kısa", "COL_OZET §8", 2, notu="Küçük örnek; Twelve Data verisi gerekir."),
    _ik_k("Ç11", "2026-10-01", "SIKISMA_TESTI", "arsiv/col_kodlarim", "Çöl içi/dışı bilet farkı", "Fark yok", "COL_OZET §9.6", 2),
    _ik_k("Ç12", "2026-10-02", "BUYUK_YUKSELIS", "arsiv/col_kodlarim", "Büyük yükselişler çölden mi gelir?",
       "Hayır (%5, kat 0,78); hafif iz sektör dalgası/genişlik/konum52 1,24-1,29", "COL_OZET §9.6", 2),
    _ik_k("Ç13", "2026-10-02", "TEYIT_BILETI", "arsiv/col_kodlarim", "Teyit sonrası bilet", "Zayıf (+1,0; 2026 −2,1)", "COL_OZET §9.6", 4),
    _ik_k("Ç14", "2026-10-02", "COL_KIRILIM_ATLAS (öncü/rüzgâr)", "arsiv/col_kodlarim", "Öncü + rüzgâr sırası", "Tutarsız",
       "COL_OZET §9.6", 2),
    _ik_k("Ç15", "2026-10-04", "A1 bedelsiz bildirimi", "KAP_ARSIV.py (Drive)", "Bedelsiz başvurusu/onayı sonrası düşüş?",
       "GEÇERLİ (ar60 −12/−6)", "IZ A1", 3, "kap_bedelsiz", "asagi"),
    _ik_k("Ç16", "2026-10-04", "A2 tavan günü (+%9)", "KAP_ARSIV.py (Drive)", "Tavan günü sonrası düşüş?", "GEÇERLİ (ar60 −11/−15)",
       "IZ A2", 1, "tavan", "asagi"),
    _ik_k("Ç17", "2026-10-04", "A3 taban günü (−%5 altı)", "KAP_ARSIV.py (Drive)", "Sert düşüş günü sonrası düşüş?",
       "GEÇERLİ (ar60 −4,8/−4,7)", "IZ A3", 1, "taban", "asagi"),
    _ik_k("Ç18", "2026-10-04", "A4 koşmuşken iş ilişkisi haberi", "KAP_ARSIV.py (Drive)", "20 günde +%25 koşmuş hissede sözleşme haberi",
       "GEÇERLİ (ar60 −7/−8)", "IZ A4", 3, "kap_sozlesme_kosmus", "asagi"),
    _ik_k("Ç19", "2026-10-04", "A9 OLGUN rüzgâr + sözleşme/teşvik", "KAP_ARSIV.py (Drive)", "Olgun sektör rüzgârında haber",
       "GEÇERLİ ama nötrden farkı küçük", "IZ A9", 3, notu="Tek cetvelle Ç71'de puanlandı (İZ DEĞİL)."),
    _ik_k("Ç20", "2026-10-04", "A5 söylentiye açıklama + o gün −%5", "KAP_ARSIV.py (Drive)", "Söylenti açıklaması günü düşüş",
       "ADAY (n 26/46)", "IZ A5", 3, "kap_soylenti_dus", "asagi"),
    _ik_k("Ç21", "2026-10-04", "A8 sözleşme tutarı > yıllık ciro %50", "KAP_ARSIV.py (Drive)", "Büyük sözleşme sonrası",
       "ADAY (n 29/20)", "IZ A8", 3, notu="Sözleşme tutarı kap_ozet'te yok → tek cetvelle puanlanamaz."),
    _ik_k("Ç22", "2026-10-04", "A7 açığa satış", "—", "Açığa satış sonrası", "ÇÜRÜDÜ", "IZ A7", 3, notu="Veri elde yok."),
    _ik_k("Ç23", "2026-10-04", "A10 hacim patlaması + gün −%5 altı", "KAP_ARSIV.py (Drive)", "Hacimli düşüş günü sonrası",
       "ADAY (piy20 −3,5/−2,8)", "IZ A10", 1, "hacim_dus", "asagi"),
    _ik_k("Ç24", "2026-10-04", "A11 A10 + 20 günde zaten −%20", "KAP_ARSIV.py (Drive)", "Düşmüş hissede hacimli düşüş",
       "ADAY-zayıf", "IZ A11", 1, "hacim_dus_20", "asagi"),
    _ik_k("Ç25", "2026-10-04", "A12 1 yıl en geride + hacim en çok artan", "KAP_ARSIV.py (Drive)", "Düşerken hacim = çıkış?",
       "ADAY-zayıf", "IZ A12", 1, "geride_hacim", "asagi"),
    _ik_k("Ç26", "2026-10-04", "B1 geri alım bildirimi", "KAP_ARSIV.py (Drive)", "Geri alım sonrası yükseliş?", "GEÇERLİ (ar60 +4,9/+2,4)",
       "IZ B1", 3, "kap_geri_alim", "yukari"),
    _ik_k("Ç27", "2026-10-04", "B1'' geri alım + koşmamış", "KAP_ARSIV.py (Drive)", "Koşmamış hissede geri alım",
       "GEÇERLİ?", "IZ B1''", 3, "kap_geri_alim_kosmamis", "yukari", notu="'Nötr rüzgâr' şartı bu turda yok (koşmamış = 20 gün < +%10)."),
    _ik_k("Ç28", "2026-10-04", "B9 yeni rüzgâr + sözleşme", "KAP_ARSIV.py (Drive)", "Yeni rüzgârda haber", "ÇÜRÜDÜ (tek hisse tekrarı)",
       "IZ B9", 3),
    _ik_k("Ç29", "2026-10-04", "B5 teyit günü / B6 likidite / B8 genişlik yılları", "—", "Teyit, likidite, piyasa genişliği",
       "GEÇERLİ (küçük / filtre / zamanlama)", "IZ B5, B6, B8", 4, notu="Tanımları defterde tam yazılı değil; sistem filtresi."),
    _ik_k("Ç30", "2026-10-04", "B10 kriz teyidi + küçük PD / B11 dayanıklı", "—", "Kriz sonrası küçük şirket", "ADAY / REJİME BAĞLI",
       "IZ B10, B11", 3, notu="Kriz takvimi + sermaye verisi gerekir; bu turda yok."),
    _ik_k("Ç31", "2026-10-04", "B12-B13 çöl kırılım günü hacim yönü", "—", "Çölün son 4 haftası hacmi kırılım yönünü verir mi?",
       "ADAY yön (B13 sonradan bilgi)", "IZ B12, B13", 2, notu="Çöl segment olay dosyası yok."),
    _ik_k("Ç32", "2026-10-04", "Ölü eşek (KAP kötü haber, bilanço, geride)", "—", "Ölü şirketten kaçınma", "Test edilemez (hayatta kalma)",
       "IZ C", 3, notu="Borsadan çıkmış hisse verisi yok."),
    _ik_k("Ç33", "2026-10-04", "Çölde erken giriş / güvenilir isim V / para izi", "—", "Çöl içinde erken alım", "ÇÜRÜDÜ / iz değil",
       "IZ C", 2),
    _ik_k("Ç34", "2026-10-04", "Hacimli yukarı kırılım (+%5 kapanış)", "—", "Hacimli kırılım devam eder mi?", "İz değil",
       "IZ C", 1, "hacimli_kirilim", "yukari"),
    _ik_k("Ç35", "2026-10-08", "col_v2 / yeniden_tara, tahtaci_oyunu", "yeniden_tara.py, tahtaci_oyunu.py",
       "Yeni liste / tahtacı klimaksı", "Ölçüm; tahtacı GEÇMEDİ", "COL_OZET §9.6", 2),
    _ik_k("Ç36", "2026-10-09", "col_ogren / col_tanim2", "col_ogren.py, col_tanim2.py", "Çöl metrikleri simetrik etikette ayırır mı?",
       "İz yok", "COL_OZET §9.2", 2),
    _ik_k("Ç37", "2026-10-17", "D7 küçük mum (H−L) + D9 uzun çöl + rüzgâr", "COL_v1.py", "Küçük mum tanımı ve uzun çöl yönü",
       "D9 yön ADAY (%56-61); test sürüyor", "COL_OZET §9.1", 2, notu="Olay dosyası yok. DÜZELTME / KAPANIŞ (14 Kas, Ç181): 'test sürüyor' kaydı kapandı: D9 uzun çöl İZ DEĞİL (sakin hisse seçer, +%100 katı 0,40); D9 + rüzgâr ÖLÇÜLEMEDİ; yalnız rüzgâr ABD'de +%3,6 ama portföy şartı tutmadı; eski '%56-61 yön' doğrulanmadı."),
    _ik_k("Ç38", "2026-10-19", "A13 dipte doji kutusu → sert düşüş riski", "DOJI_KUTU_TEST.py", "Doji kutusundan sonra sert düşüş azalır mı?",
       "BIST GEÇERLİ risk (ABD bekliyor)", "IZ A13", 2, "doji_kutu", "koruma", "arastirma_cikti/doji_kutu",
       "Denetim 24 Eki: aynı kutu kayınca yeniden A sayılıyordu (düzeltildi) ve A_dip'in kontrolü yoktu; eşi B_dip (dojisiz dip kutusu) "
       "ile sert aşağı kat 0,94 / 0,97 / 0,90 → etkinin çoğu 'dipte' olmaktan, dojiden değil."),
    _ik_k("Ç39", "2026-10-19", "Doji kutusu → sert yukarı hareket", "DOJI_KUTU_TEST.py", "Doji kutusu yukarı hareketi haber verir mi?",
       "İz değil (0,90-1,02)", "IZ C", 2, "doji_kutu", "yukari", "arastirma_cikti/doji_kutu"),
    _ik_k("Ç40", "2026-10-19", "GOZ_ESLE bölge kuralı + çöl karnesi", "GOZ_ESLE.py", "Bölge kuralı Cemal'in gözüyle eşleşiyor mu?",
       "Ölçüm (altyapı)", "COL_OZET §9.5", 0),
    _ik_k("Ç41", "2026-10-20", "D12 dip çölü (COL_DIP_TEST)", "COL_DIP_TEST.py", "Dip çölünden atılım tabanı geçer mi?",
       "İZ DEĞİL (6 dönemin 3'ü)", "IZ C", 2, "d12_atilim", "yukari", "arastirma_cikti/col_dip",
       "Denetim 24 Eki: hedefli işlem 120. barda kesilip verinin son barına atlıyordu, kazananlar 'açık' diye atılıyordu (düzeltildi). "
       "Yeni beklenti dip/taban: 17,5/16,1 · 18,7/25,5 · 41,8/31,2 · 7,7/10,5 · ABD 2,1/2,3 · 13,1/7,0 → yine 3/6, karar aynı."),
    _ik_k("Ç42", "2026-10-20", "COL_GECMIS (geçmiş gün taraması)", "COL_GECMIS.py", "Kod geçmişte hangi çölleri bulurdu?", "Araç",
       "COL_OZET §9.5", 0, cikti="arastirma_cikti/col_gecmis"),
    _ik_k("Ç43", "2026-10-21", "COL_BUGUN / COL_SEKIL / etiketler", "COL_BUGUN.py, COL_SEKIL.py", "Bugünkü kutular + şekil ölçüleri",
       "Ölçüm, n küçük", "COL_OZET §9.8", 0, cikti="arastirma_cikti/col_bugun, col_sekil",
       notu="Denetim 24 Eki: COL_SEKIL'in 'ayıran ölçüleri' (dip_pos, dipten sonra bar, öbek, retest, hacim) kıyaslanamaz negatiflerden "
            "geliyordu (21 'bugün' kutusu kodun kendi ret nedenine göre seçilmişti). Aynı yoldan çizilmiş 8 OLUMSUZ'a göre bütün AUC 0,37-0,60: "
            "hiçbir şekil ölçüsü çölü ayırmıyor."),
    _ik_k("Ç44", "2026-10-21", "B14 yuvarlanma öbeği (COL_OBEK)", "COL_OBEK.py", "Öbekten sonra alım gelir mi, kazanç artar mı?",
       "ADAY yalnız yön; kazanç yok", "IZ B14", 2, "obek", "yukari", "arastirma_cikti/col_obek",
       "Denetim 24 Eki: 'alım oranı tabandan +15-20p' mekanikti (taban kutusu tavana ~2 kat uzak). Tavan/dip uzaklığı eşli tabana göre "
       "ALIM %70/%78/%67/%71 vs %67/%76/%70/%67 (+3/+2/−3/+4p) → yön izi de yok. İşlemlerin yarısı kopyaydı (düzeltildi)."),
    _ik_k("Ç45", "2026-10-21", "B15 çıkış kuralı (COL_YOL) → T10 üretimde", "COL_YOL.py", "+%8 maliyet stopu + trail kazancı artırır mı?",
       "İZ DEĞİL (ABD 3/6); ağır kayıp yarıya", "IZ B15", 4, cikti="arastirma_cikti/col_yol",
       notu="Portföy kuralı; olay cetveli uygulanmaz. Denetim 24 Eki (kopya işlemler atıldı, hisse başına tek slot, trail ufuksuz, "
            "20 rastgele sıra ortalaması): BIST 4 dönem slot ort. maliyet8_sma20 (T10) +144 vs mevcut +155; ABD 0 vs +6. T10'un "
            "'+157 vs +144' getiri dayanağı TERS döndü; tutarlı kalan tek etki ağır kaybın azalması (%9,1 → %5,4)."),
    _ik_k("Ç46", "2026-10-21", "COL_KAZANC ek şart + K7 küçük alım mumu + K8 NVI/CMF", "COL_KAZANC.py", "Üretim yoluna şart eklemek kazanç artırır mı?",
       "İZ DEĞİL (BIST'e özgü)", "IZ C", 2, cikti="arastirma_cikti/col_kazanc", notu="Üretim yolu içi ölçüm; olay cetveli değil."),
    _ik_k("Ç47", "2026-10-21", "D13 tespit motoru (COL_TESPIT, col_dip2)", "COL_TESPIT.py, COL_v1.py", "Cemal'in 3 kuralıyla tespit",
       "Tespit bulgusu: alım oranı +12..26p 6/6; iz değil", "IZ C", 2, "d13", "yukari", "arastirma_cikti/col_tespit",
       "Denetim 24 Eki: ABD olayları dosyada vardı ('.US' ekli), adaptör okumuyordu → düzeltildi (ABD 2023 0,97, 2024-26 0,98). "
       "COL_TESPIT v1.1 yeniden koşum: mesafe-eşli tabana göre alım farkı +0,5..+3,8p (ham +11..+26p mekanikti), bozulma eşli "
       "tabanın 0,3-0,65'i; seçim ölçütü 'alım > taban+10p, 4/4' artık 3456 varyantın hiçbirinde tutmuyor. Göz testi 17/29, 2/29 aynı."),
    _ik_k("Ç48", "2026-10-21", "COL_GOZ (746 kutu gözle) + Cemal kararı", "goz_esle/arastirma", "Kodun kutuları gözle çöl mü?",
       "%6 çöl; etiket 'atılım geldi mi' etiketi", "COL_OZET §9.8", 0, cikti="arastirma_cikti/col_goz"),
    _ik_k("Ç49", "2026-10-22", "MUM_SUKUN v1.1 hisseye özel mum küçülmesi", "MUM_SUKUN.py", "Düşüş sonrası sakin 3-4 mum",
       "İZ DEĞİL (0,96-1,04)", "IZ C", 2, "mum_sukun", "yukari", "arastirma_cikti/mum_sukun"),
    _ik_k("Ç50", "2026-10-22", "MUM_SUKUN v1.2 düz zemine yapışan sıra", "MUM_SUKUN.py", "Sert düşüş sonrası zemin sırası",
       "İZ DEĞİL", "IZ C", 2, "zemin", "yukari", "arastirma_cikti/mum_sukun"),
    _ik_k("Ç51", "2026-10-22", "MUM_SUKUN v1.3 kısa ufuk + ayrılma sertliği", "MUM_SUKUN.py", "Zeminden 3-10 günlük hareket",
       "İZ DEĞİL", "IZ C", 2, notu="Kısa ufuk ölçüsü; 60 günlük cetvel uygun değil."),
    _ik_k("Ç52", "2026-10-22", "Faiz kararı günleri (TCMB) sektör/borç tepkisi", "goz_esle/arastirma/faiz_olay.py",
       "Faiz kararında hangi grup ayrışır?", "Ölçüm, karar yazılmadı", "—", 3, cikti="arastirma_cikti/faiz"),
    _ik_k("Ç53", "2026-10-22", "Derin dip sonrası oynaklık tercilleri", "goz_esle/arastirma/dip_vol.py",
       "Piyasa dipteyken oynak hisse önce mi gider?", "Ölçüm, karar yazılmadı", "—", 2, cikti="arastirma_cikti/faiz/dip_vol.csv"),
    _ik_k("Ç54", "2026-10-22", "Tavan-taban olayı (≥4 tavan sonra ≥3 taban)", "goz_esle/arastirma/tavan_taban_olay.py",
       "Tavan serisi sonrası taban serisi sonrası ne olur?", "Ölçüm (117 olay), karar yazılmadı", "—", 1,
       cikti="arastirma_cikti/tavan_taban"),
    _ik_k("Ç55", "2026-10-22", "FON_IZI v1.0 fon hisselerinin yükseliş izi (iz B)", "FON_IZI.py", "Tek yönlü fiyat izi evrende ayırır mı?",
       "İZ DEĞİL", "IZ C", 2, "fon_iz_b", "yukari", "arastirma_cikti/fon_izi"),
    _ik_k("Ç56", "2026-10-23", "FON_IZI v1.1 sessiz yuvarlanma (Z0) + hacim", "FON_IZI.py", "Küçük mum + ufak yukarı + kuru hacim",
       "İZ DEĞİL", "IZ C", 2, "z0", "yukari", "arastirma_cikti/fon_izi"),
    _ik_k("Ç57", "2026-10-23", "Z0 + hacim kuru (≤0,6)", "FON_IZI.py", "Sessiz bölgede kuru hacim", "İZ DEĞİL (ABD 2,45 / BIST 0,97)",
       "IZ C", 2, "z0_kuru", "yukari", "arastirma_cikti/fon_izi"),
    _ik_k("Ç58", "2026-10-23", "SESSIZ_ML (LightGBM alış/satış + öğretmen)", "SESSIZ_ML.py", "Makine öğrenmesi iz bulur mu?",
       "İZ DEĞİL (BIST yok, ABD oynaklık)", "IZ C", 2, cikti="arastirma_cikti/sessiz_ml", notu="Model; olay cetveli yerine yıl yıl ileri test."),
    _ik_k("Ç59", "2026-10-23", "FON_IZI v1.2 62 gösterge / uyumsuzluk / Fibonacci", "FON_IZI.py", "Göstergeler iz verir mi?",
       "İZ DEĞİL (yukarı hiçbiri 1,3 değil)", "IZ C", 2, cikti="arastirma_cikti/fon_izi/fon_gosterge_*.csv",
       notu="62 sinyalin olay dosyası saklanmadı; özet var."),
    _ik_k("Ç60", "2026-10-23", "A14 blok hacimli taban günü", "FON_IZI.py", "Blok hacimli sert düşüş günü ek risk mi?",
       "ÇÜRÜDÜ (eşli 0,91-1,73)", "IZ A14", 1, "blok_taban", "asagi"),
    _ik_k("Ç61", "2026-10-23", "A15a borsa sorusu: olağan dışı fiyat (KAP 42)", "FON_IZI.py", "Borsa bayrağı sonrası düşüş",
       "ÇÜRÜDÜ (eşli 1,14-1,17)", "IZ A15", 3, "kap_olagan_disi", "asagi"),
    _ik_k("Ç62", "2026-10-23", "A15b VBTS / BISTECH tedbiri (KAP 14)", "FON_IZI.py", "Tedbir sonrası düşüş", "ÇÜRÜDÜ (eşli 1,02-1,14)",
       "IZ A15", 3, "kap_vbts", "asagi"),
    _ik_k("Ç63", "2026-10-23", "Bağımsız denetim + v1.4 düzeltmeleri (Mart 2020 marjı)", "FON_IZI.py, SESSIZ_ML.py",
       "Kod/veri hatası var mı?", "Veri hatası düzeltildi; kararlar değişmedi", "IZ C", 0),
    _ik_k("Ç64", "2026-10-24", "K9-K11 KAP fon portföy defteri", "FON_IZI.py (k9indir, k10)", "Fonlar hangi gün kaç lot aldı?",
       "Ölçüm: fonlar koşu fazında giriyor", "IZ C", 3, cikti="arastirma_cikti/fon_izi, kapfon-veri dalı"),
    _ik_k("Ç65", "2026-10-24", "K10 fon girişi (rapor yayını sonrası)", "FON_IZI.py", "'Fon girdi' bilgisi sonrasını ayırır mı?",
       "İZ DEĞİL (0,80-1,07)", "IZ C", 3, "fon_giris", "yukari", "arastirma_cikti/fon_izi"),
    _ik_k("Ç66", "2026-10-24", "K10 fon payı sermayenin %5'ini aştı", "FON_IZI.py", "Yoğunlaşma sonrası", "İZ DEĞİL (oynaklık)",
       "IZ C", 3, "fon_yogun5", "asagi", "arastirma_cikti/fon_izi"),
    _ik_k("Ç67", "2026-10-24", "K13 TEHOL tipi taban (Ders 3)", "FON_IZI.py (k13)", "Cemal'in TEHOL bölgesinin ölçüsüyle arama",
       "İZ DEĞİL", "IZ C", 2, "k13", "yukari", "arastirma_cikti/fon_izi"),
    _ik_k("Ç68", "2026-10-24", "K14-K15 TEHOL tipi 6 devam denemesi (Ders 4)", "FON_IZI.py (k14, k15)", "Rüzgâr, 2/3 kat, kırılım, genişlik, oynaklık eşli",
       "İZ DEĞİL; BIST'te aşağı risk düşük", "IZ C", 2, cikti="arastirma_cikti/fon_izi/k14_*, k15_*",
       notu="Zaten eşli kutuya göre ölçüldü."),
    _ik_k("Ç69", "2026-10-24", "TEHOL tipi taban → BIST'te aşağı risk düşük", "FON_IZI.py (k14, k15)",
          "Sakin dar tabandan sonra önce −%20 daha seyrek mi?", "Gözlem: BIST 0,45-0,68, ABD yok", "IZ C", 2, "k13", "koruma",
          "arastirma_cikti/fon_izi"),
    # --- 24 Eki tek cetvel turu 1 izsiz -> sıradaki 3 deneme (sonuç görülmeden yazıldı)
    _ik_k("Ç70", "2026-10-24", "A11 oynaklık ölçekli (−3σ gün + hacim 3x + 20 günde −%20)", "IZ_KARNE.py",
          "BIST'te güçlü A11 ABD'de aynı anlamla tutar mı?", "Yeni deneme", "IZ A11", 1, "hacim_dus_20_oyn", "asagi"),
    _ik_k("Ç71", "2026-10-24", "A9 OLGUN rüzgâr + sözleşme/teşvik (tek cetvel)", "IZ_KARNE.py",
          "Puanlanmamış tek GEÇERLİ madde", "Yeni deneme", "IZ A9", 3, "kap_olgun_sozlesme", "asagi"),
    _ik_k("Ç72", "2026-10-24", "D13 tespiti aşağı riski düşürür mü (koruma)", "IZ_KARNE.py",
          "COL_TESPIT 'bozulma %2-9 vs %31-44' eşli tabanla tutar mı?", "Yeni deneme", "IZ C", 2, "d13", "koruma",
          notu="Denetim 24 Eki: ABD olayları artık puanlanıyor (adaptör düzeltildi)."),
    _ik_k("Ç73", "2026-10-24", "TEHOL tipi taban + DÜZGÜN DİP (K13b)", "FON_IZI.py (FI_K13B_ESIK), IZ_KARNE.py",
          "Cemal: 'Ekim 2024 dibi düzgün, 2021'inki değil' — dibi haftalarca test edilen taban sonrası yükseliş?",
          "Yeni deneme (TEHOL 2024 geçer, 2021 elenir)", "IZ C", 2, "k13_duz_dip", "yukari",
          notu="Eylül'deki 'dip sabitliği' (çöl segmenti) kapalıydı; bu deneme Cemal'in doğrudan isteği, yalnız TEHOL tipi taban."),
    _ik_k("Ç74", "2026-10-24", "TEHOL tipi taban + düzgün dip → aşağı risk düşük mü", "IZ_KARNE.py",
          "Düzgün dipli taban sonrası önce −%20 daha seyrek mi?", "Yeni deneme", "IZ C", 2, "k13_duz_dip", "koruma"),
    _ik_k("Ç75", "2026-10-24", "Düzgün dip tek başına (çöküş sonrası taban, şekil şartı gevşek)", "FON_IZI.py (FI_K16_GEVSEK)",
          "Düzgün dip, TEHOL'ün öteki ölçüleri olmadan da fark yaratır mı?", "Yeni deneme", "IZ C", 2, "duz_dip_gevsek", "yukari", notu="DÜZELTME (14 Kas, Ç179): fi_k13 tarayıcısı 'n < 400' toplam uzunluk şartı geleceğe bakıyordu; ortak cetvelle A (yalnız dip) ABD ÖLÇÜLEMEDİ / TUTMADI, olasılık PİYANGO."),
    _ik_k("Ç76", "2026-10-24", "Ç73 olayları, Cemal'in ölçüsü: 250 günde dip kırılmadan 2 kat (eşli kutu)", "FON_IZI.py (k16)",
          "Düzgün dipli TEHOL tipi tabandan sonra büyük yükseliş daha sık mı?", "Yeni deneme", "IZ C", 2,
          cikti="arastirma_cikti/fon_izi/k16_k13b_ozet.csv",
          notu="Eşli kutu kıyası. SONUÇ İZ DEĞİL. Denetim sonrası (K13 pencere + eşli kutu geçmiş bilgi + fi_duzelt): 2 kat katı "
               "BIST 0,79 / 0,00 (n2) / 1,30 (n41), ABD 0,33 / 0,31 / 0,92."),
    _ik_k("Ç77", "2026-10-24", "Ç75 olayları, 250 günde dip kırılmadan 2 kat (eşli kutu)", "FON_IZI.py (k16)",
          "Düzgün dip tek başına büyük yükselişi daha sık getirir mi?", "Yeni deneme", "IZ C", 2,
          cikti="arastirma_cikti/fon_izi/k16_gevsek_ozet.csv",
          notu="Eşli kutu kıyası. SONUÇ İZ DEĞİL. Denetim sonrası 2 kat katı BIST 0,71 / 0,96 / 1,06, ABD 0,73 / 1,08 / 0,91; "
               "önce −%20 katı 0,75-1,31 (eskiden 1,00-1,93: eşli kutu geleceğe göre seçiliyordu → 'çok test edilen dip daha sık "
               "kırılıyor' gözlemi düştü)."),
    _ik_k("Ç78", "2026-10-24", "İKİ YUVARLAMA: dipten sonra önce aşağı (∩), hemen ardından yukarı (∪) yuvarlama (K17 Y1)", "FON_IZI.py (k17)",
          "Cemal (TEHOL 2021): '1'de aşağı yuvarlama, 2. bölge istenen; ikisi peş peşe' — bu sıra sonrası önce +%20 daha sık mı?",
          "Yeni deneme (TEHOL 21 Nis-8 Haz 2021 kalibre)", "IZ C", 2, "iki_yuvarlama", "yukari", cikti="arastirma_cikti/fon_izi/k17_ozet.csv",
          notu="Eşli kutuya (aynı çöküş, desen yok) göre de önce +%20 katı BIST 0,99 / 1,08 / 0,87, ABD 1,03 / 1,02 / 0,86 → İZ DEĞİL. DÜZELTME (14 Kas, Ç179): fi_k17 'n < 400' toplam uzunluk şartı geleceğe bakıyordu; ortak cetvelle dip kümeleri PİYANGO, çölle ayrım ölçülemedi."),
    _ik_k("Ç79", "2026-10-24", "İki yuvarlama + 2. bölgenin dibi düzgün (K17 Y2)", "FON_IZI.py (k17)",
          "∪ bölgesinin dibi haftalarca test edilmişse fark var mı?", "Yeni deneme", "IZ C", 2, "iki_yuvarlama_duz", "yukari",
          notu="Kâselerin çoğu zaten düzgün dipli (BIST 735'in 688'i); ayırıcı değil."),
    _ik_k("Ç80", "2026-10-24", "İki yuvarlama + kutu tavanı kırılımı (K17 Y3)", "FON_IZI.py (k17)",
          "İki yuvarlamalı kutunun tavanı kırılınca girmek fark yaratır mı?", "Yeni deneme", "IZ C", 2, "iki_yuvarlama_kir", "yukari",
          notu="Eşli kutuya göre BIST 2023 1,46 (önce −%20 0,46), 2024-26 0,94, ABD 0,73-0,97 → İZ DEĞİL."),
    _ik_k("Ç81", "2026-10-24", "İki yuvarlama, sıkı yay (iki bölgede R2 >= 0,70; K17 Y4)", "FON_IZI.py (k17)",
          "Gözle temiz yay olanlar ayrışır mı? (Ç78-Ç80 iz değil sonrası tur 2, eşik önceden)", "Yeni deneme", "IZ C", 2,
          "iki_yuvarlama_siki", "yukari"),
    _ik_k("Ç82", "2026-10-24", "İki yuvarlama + sektör rüzgârı (K17 Y5)", "FON_IZI.py (k17)",
          "Rüzgârlı sektörde iki yuvarlama ayrışır mı? (tur 2)", "Yeni deneme", "IZ C", 2, "iki_yuvarlama_ruz", "yukari",
          notu="Eşli kutuya göre önce −%20 BIST 0,51-0,71 (aşağı risk düşük) ama tek cetvelde ters kat 1,0-1,4; BIST 2023 n=29 küçük."),
    _ik_k("Ç83", "2026-10-24", "İki yuvarlama, hafif silkeleme (-%5..-%15; K17 Y6)", "FON_IZI.py (k17)",
          "Cemal'in 'iki kutu' girişi gibi sığ ikinci çukur ayrışır mı? (tur 2)", "Yeni deneme", "IZ C", 2, "iki_yuvarlama_hafif", "yukari"),
    _ik_k("Ç84", "2026-10-24", "GERİYE DÖNÜK KOD DENETİMİ (6 bağımsız denetçi; ölçüm + üretim kodu)", "IZ_KARNE.py, FON_IZI.py, COL_*.py, "
          "SESSIZ_ML.py, DOJI_KUTU_TEST.py, MUM_SUKUN.py, DENETIM.py, STOP_TEST.py, mfe_analiz.py, zincir_denetimi.py",
          "Cemal: 'eski modeller sık hata yaptı; yanlışları bul, doğrula, düzelt, yeniden koştur'", "Denetim", "IZ C", 0,
          cikti="arastirma_cikti/iz_karne/IZ_KARNE_ders7_denetim.pdf",
          notu="Ölçüm kodunda ~30 doğrulanmış hata düzeltildi, etkilenen her çalışma yeniden koşuldu: tek cetvel İZ 0 (değişmedi). "
               "Düşen iddialar: T10 getiri dayanağı (ters döndü), öbek 'yön' izi (mekanik), D13 'alım +12..26p' (mekanik), düzgün dip "
               "'−%20 daha sık' (kontrol grubu hatası), COL_SEKIL 'ayıran ölçüler' (kıyaslanamaz negatif). Üretimde 11 hata: 'yaz' bekliyor."),
    _ik_k("Ç85", "2026-10-25", "CEMAL'İN VAKA PROFİLİ: düşüş sonrası dar kutu, mum ve hacim düşüştekinden küçük, tavan kırılımı (K18 C1)",
          "FON_IZI.py (k18)", "Cemal: 'TEHOL, BINBN, KTLEV, ESCAR, BORLS, VERUS, MANAS koştu; VSNMD, PAPIL koşmadı. Ortak iz var mı?' — "
          "koşanların ortak profili evrende önce +%20'yi daha sık getiriyor mu?", "Yeni deneme (eşikler koşan vakalardan)", "IZ C", 2,
          "cemal_profil", "yukari", cikti="arastirma_cikti/fon_izi/k18_ozet.csv",
          notu="Vakalar: koşan 9 bölgenin 7'si, koşmayan 3'ünün 2'si (VSNMD, PAPIL) profilde → profil ayırmıyor. Eşli kutuya (aynı bağlam, "
               "profil tutmayan atılım) göre önce +%20 BIST 0,90 / 1,06, ABD 0,87 / 1,04; 2 kat 1,15 / 1,04 / 0,97 / 1,22. Tek cetvelde önce "
               "−%20 1,24-1,39 (oynak). BIST 2024-26'da 1.254 sinyal: %23'ü 2 kat (eşli %22). Üretim D13 Cemal'in 12 bölgesinin 5'ini gördü "
               "(VSNMD dahil), BINBN, KTLEV, EUHOL, MANAS'ı görmedi. Ders: FON_IZI_ders7_cemal_vakalar.pdf."),
    _ik_k("Ç86", "2026-10-25", "Cemal'in vaka profili, kutu >= 40 bar ('aylarca'; K18 C2)", "FON_IZI.py (k18)",
          "Aylarca süren kutu ayrışır mı?", "Yeni deneme", "IZ C", 2, "cemal_profil_uzun", "yukari"),
    _ik_k("Ç87", "2026-10-25", "Cemal'in vaka profili, önce düşüş <= -%50 ('sert çöküş'; K18 C3)", "FON_IZI.py (k18)",
          "Sert çöküş sonrası kutu ayrışır mı?", "Yeni deneme", "IZ C", 2, "cemal_profil_sert", "yukari"),
    _ik_k("Ç88", "2026-10-25", "Cemal'in vaka profili, dar kutu (bant <= %20; K18 C4)", "FON_IZI.py (k18)",
          "TEHOL/BINBN/ESCAR/MANAS gibi dar çöl ayrışır mı? (Ç85-Ç87 iz değil sonrası tur 2, eşik önceden)", "Yeni deneme", "IZ C", 2,
          "cemal_profil_dar", "yukari"),
    _ik_k("Ç89", "2026-10-25", "Cemal'in vaka profili + kutuda dev hacim barı (>= 10 kat; K18 C5)", "FON_IZI.py (k18)",
          "Cemal'in EUHOL 24 Ara 2024 izi: çölün içindeki dev hacim barı ayrışır mı? (tur 2)", "Yeni deneme", "IZ C", 2,
          "cemal_profil_dev", "yukari",
          notu="Eşli kutuya göre 2 kat katı BIST 2024-26 1,55, ABD 2023 1,67, ABD 2024-26 1,43 ama BIST 2023 0,86 (n 25) ve önce −%20 de "
               "1,2-1,85 kat sık: oynak hisse. Tek cetvel önce +%20 0,84-1,10."),
    _ik_k("Ç90", "2026-10-25", "Cemal'in vaka profili + sektör rüzgârı (K18 C6)", "FON_IZI.py (k18)",
          "Rüzgârlı sektörde profil ayrışır mı? (tur 2)", "Yeni deneme", "IZ C", 2, "cemal_profil_ruz", "yukari"),
    _ik_k("Ç91", "2026-10-25", "SİSTEM vs RASTGELE: kırılımda gir + kutu dibi stop + trail, aynı çıkışla rastgele girişe göre (K19)",
          "FON_IZI.py (k19)", "Cemal: 'kırılım + kutu dibi + trail rastgele hisseden / rastgele noktadan çok daha fazla kazandırmalı; bu test yok'",
          "Yeni deneme (karar önceden)", "IZ C", 4, cikti="arastirma_cikti/fon_izi/k19_ozet.csv",
          notu="Portföy testi (tek cetvel değil). 3 sinyal (Cemal profili, bütün kutu kırılımları, düz 20 gün kırılımı) × BIST/ABD × 2023/"
               "2024-26: 12 hücrenin hiçbiri aynı gün eşli hisseden üstün değil (işlem başı fark −1,8..+1,7 puan, %90 aralık sıfırı içeriyor). "
               "BIST 2023 işlem başı +%38 = aynı gün rastgele hisse +%40 (piyasa). Çıkış kuralı aynı girişlerde 120 gün tutmaktan ortalamada "
               "hep düşük; yatay piyasada medyan ve −%30 altı kayıpta iyi (BIST 2024-26 %11 → %4). Ders: FON_IZI_ders8_sistem_rastgele.pdf."),
    _ik_k("Ç92", "2026-10-25", "SAĞ AYAK: çöl atılımından sonraki yükseliş (120 gün en yüksek, 250 gün 2 kat) vs aynı gün eşli hisse; nadir çöl (K20)",
          "FON_IZI.py (k19)", "Cemal: 'çöl bitişi, sağ ayak rastgele hisseden iyi değilse her şey hikâye; çöl nadir'", "Yeni deneme (karar önceden)",
          "IZ C", 4, cikti="arastirma_cikti/fon_izi/k19_ozet.csv",
          notu="Çıkış kuralı yok. 5 sinyal (profil, kutu, düz kırılım, dar kutu, nadir = dar + düşüş ≤ −%50) × BIST/ABD × 2023/2024-26: "
               "hiçbir sinyal dört hücrede geçmedi; BIST'te hiçbir hücre geçmedi (profil 2024-26 120 gün en yüksek +%53,5 vs eşli +%51,0; "
               "nadir 2 kat oranı %20,7 vs %20,5). ABD'de 3 hücre geçti (profil ve kutu 2024-26, nadir 2023). MANAS 16 Haz-28 Tem 2025 K18 "
               "buldu (22 Tem), 20 Eki-5 Kas 2025 kutusu 12 gün, bulmadı; D13 ikisini de görmedi."),
    _ik_k("Ç93", "2026-10-25", "SAĞ AYAK MUM MUM: çöl atılımından sonra her gün yüzde yol ve aynı gün BÜTÜN hisseler içindeki sıra; en sıkı çöl (K21)",
          "FON_IZI.py (k21)", "Cemal: 'çölden çıkan hisse ile rastgele günde alınan yolun eşit olma ihtimali sıfır; büyük bir yanlışın içindesin; "
          "çıkış kuralını bırak, mumları kıyasla'", "Denetim + yeni deneme (karar önceden)", "IZ C", 4, cikti="arastirma_cikti/fon_izi/k21_ozet.csv",
          notu="Çıkış kuralı, eşleştirme, kura yok. Kod hatası aranıp bulunmadı (giriş günü hizası, bozuk mum, ortalama şişmesi). Sıra 60. ve 120. "
               "günde 0,45-0,53 (profil, nadir; n ≥ 30 hücreler); BIST 2024-26 profil 120. gün medyan −%2,5 vs bütün hisseler −%1,7. En sıkı çöl "
               "(kutu ≥ 30, bant ≤ %20, düşüş ≤ −%50, mum ve hacim ≤ 0,8; MANAS Haz-Tem 2025 geçer) BIST 2024-26 n 29-36: sıra 0,38-0,43, "
               "120 gün en yüksek +%44 vs eşli +%43, 2 kat %12 vs %19. Hiçbir çöl tanımı mum mum üstün değil. Ders: FON_IZI_ders9_sag_ayak_mum.pdf."),
    _ik_k("Ç94", "2026-10-25", "CEMAL'İN PENCERESİ + TAVANDA BEKLEYEN ALIŞ EMRİ: çölün son gününden 15 gün (atılım mumu dahil) ve atılım mumunu "
          "alan bekleyen emir (K22)", "FON_IZI.py (k22)",
          "Cemal: 'MANAS 18 Temmuz - 8 Ağustos 2025, çölün sağ ayağı; buradaki yükseliş sıradan bir hisseden fazla olmalı'",
          "Yeni deneme (karar önceden)", "IZ C", 4, cikti="arastirma_cikti/fon_izi/k22_ozet.csv",
          notu="MANAS 18.07-08.08.2025 +%84,5 vs bütün hisseler +%9,0 (580 hissenin 5'i daha çok; sıra 0,99). Aynı pencere bütün çöl "
               "atılımlarında: atılım mumu DAHİL sıra 0,57-0,66 (çöl önde; BIST 2024-26 profil medyan +%6,5 vs +%1,8), atılım kapanışından "
               "sonra 0,46-0,54: fark atılım mumunda (sonradan bilinen). Atılım mumunu alan tek emir (kutu tavanı ×1,002'de bekleyen alış, "
               "sahte kırılım dahil): dolumların %44-55'i aynı gün kutuya döndü; sıra 15. gün 0,44-0,53, 120. gün 0,42-0,52; 8 hücrenin "
               "hiçbiri geçmedi. Ders 9 s.6-7."),
    _ik_k("Ç95", "2026-10-25", "BÖLGE PARMAK İZİ + BİREBİR BENZER BÖLGELER: MANAS 13 Haz-11 Tem ve 20 Eki-5 Kas 2025'in 16 ölçüsü, en yakın 100 "
          "bölge yukarı / aşağı / yatay (K23)", "FON_IZI.py (k23)",
          "Cemal: 'işaretli bölgenin her özelliğini kaydet; birebir aynı görünümdeki bölgelerin yüzde kaçı yukarı, aşağı, yatay; halüsinasyon mu?'",
          "Yeni deneme (karar önceden; KNN kapalı konu, Cemal'in isteğiyle)", "IZ C", 2, cikti="arastirma_cikti/fon_izi/k23_ozet.csv",
          notu="16 ölçü (eğim, mum, yeşil oranı, alt/üst fitil, yakınlık, düzeni bozan, hacim, RSI, MACD, düşüş, konum, 2. evre payı, 1. evrede "
               "SMA20 altı, 2. evrede delen, BB sıkışması). En yakın 100 bölgenin 60 günde önce +%15 oranı / bütün bölgeler: 1. bölge BIST 2023 "
               "%42 / %58 (0,72), BIST 2024-26 %62 / %54 (1,15), ABD 2023 1,45, ABD 2024-26 1,46; 2. bölge 0,91 / 1,19 / 1,50 / 1,19; 3. bölge "
               "(BINBN 27 Ara 2024-21 Oca 2025, Cemal'in eki) 0,60 / 1,15 / 1,05 / 1,14. Dört hücrede tutmuyor (BIST 2023 ters); ABD'de "
               "benzerlerin aşağı oranı da yüksek (oynak hisseler). Kör etiket seti (her örneğe en yakın 16, düşüş <= -%30 + eğim yatay/yukarı "
               "süzgeci, sonu kesik, adsız; FON_IZI_kor_set_bolge.pdf): Cemal 20'sini işaretledi (7 ✓, 13 ✗); ✓ = 'benzer + kutu tepesi aşılırsa "
               "alırım', tepe x 1,002 bekleyen alış emri, 60 gün ±%15: ✓ dolan 4, önce +%15 %75; ✗ dolan 9, %89; kodun en benzer 48'i dolan 37, "
               "%70; havuz %61 (48'i 1,16 kat). Göz izi adayı değil (ön deneme, n küçük); SONRA GEÇERSİZ: Cemal küçük grafikte mum yapısını göremedi, aynı 48 aday net mum grafiğiyle yeniden çizildi (FON_IZI_kor_set_net.pdf), yeniden işaret bekleniyor. v4 (kutu + alış mumu + 1 yıl zum, 48 aday): Cemal 28 ✓ / 14 ✗ / 6 belirsiz; önce +%15 ✓ %54, ✗ %57, havuz %60, 2 kat ✓ %29 / ✗ %36 / havuz %42 -> göz izi değil. Ders: FON_IZI_ders10c_kor_set_v4.pdf. Ders: FON_IZI_ders10_bolge_parmak.pdf, "
               "FON_IZI_ders10b_kor_set.pdf."),
    _ik_k("Ç96", "2026-10-25", "İKİ EVRE KURALI: düşüş sonrası SMA20 altı (1. evre) → SMA20 üstünde 5 gün dizilme, en fazla 2 delen, BB "
          "sıkışması (K24)", "FON_IZI.py (k24)",
          "Cemal: '1. evre kırmızı SMA altında, 2. evre kırmızı SMA üstünde dizilme, muntazam, delen yok neredeyse'", "Yeni deneme (karar önceden)",
          "IZ C", 2, cikti="arastirma_cikti/fon_izi/k24_ozet.csv",
          notu="Eşikler MANAS'ın iki bölgesinden (iki örnek de tetikler). Eşli = aynı düşüş + SMA20 üstü 5. gün, tarif tutmayan. 60 gün önce "
               "+%15: BIST 2023 %46 vs %62 (0,74, n 516), BIST 2024-26 %58 vs %56 (1,04, n 967), ABD 2023 0,92, ABD 2024-26 0,97; 2016-22 "
               "BIST 1,13, ABD 1,01 (düşüş ölçüsü genç halka arzlar için 20 barla, BINBN'i 27.01.2025'te yakalar). Tarif eşliden iyi değil. "
               "Ders 10 s.4. DÜZELTME (14 Kas, Ç178): fi_k24_tara 'n < 200' şartı toplam seri uzunluğuna bakıyordu (geleceğe bakma); ortak cetvelle ABD 2024-26 TUTMADI, öteki hücreler ÖLÇÜLEMEDİ; ABD 2023 +%3,1 artısı kalmadı."),
    _ik_k("Ç97", "2026-10-25", "ÇÖL = BÜYÜK ALICININ İZİ Mİ: çölden sonra fon payı geliyor mu, fon girişinden önce çöl var mı; çölde fon var/yok; fon "
          "hisseleri hariç (K25)", "FON_IZI.py (k25)",
          "Cemal: 'bir hisseyi fazla alıcı olunca o bölgede öyle bir yapı oluşur; bu mantıkla yola çıktım' + 'TERA'nın düşüşü fon krizinden'",
          "Yeni deneme (karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k25_ozet.csv",
          notu="KAP raporlu fon payı (o an bilinen), BIST 2023-2025. Soru 1: sinyalde pay < %2 iken 12 ayda pay >= %5: K24 kural %1,64 vs eşli "
               "%1,49 (1,10), K18 profil %2,12 vs %1,85 (1,15); >= %2: 1,05-1,11. Soru 2: fonun ilk kez %5'i geçtiği 19 olayda önceki 12 ayda "
               "K24 sinyali %32 vs fon girmemiş kontrol %30 (1,07). Deneme 2: çölde fon varken (pay >= %2) 250 gün 2 kat %28 / %19 vs fonsuz %36 "
               "/ %37 (kötü). Deneme 3: fon hisseleri hariç kural %37 vs eşli %35 (2 kat), 60 gün +%15 %56 vs %59. Fiyat 31.08.2026'da kesik (fon "
               "krizi dışarıda; kuralın -%30 oranı %43 -> %32, eşli %30). Görünen alıcı (fon) çölle ilişkili değil; görünmeyen alıcı için AKD "
               "verisi gerekir (ücretli). Ders: FON_IZI_ders11_buyuk_alici.pdf."),
    _ik_k("Ç98", "2026-10-26", "DÖRT ÇÖLÜN ORTAK PARMAK İZİ: MANAS x2, BINBN, KZBGY 04.02-11.03.2025; dördünde ortak ölçüler profil olarak "
          "BIST + ABD'de, v4 alış mumu ile (K26)", "FON_IZI.py (k26)",
          "Cemal: 'KZBGY 4 Şubat - 13 Mart bölgesinin parmak izini çıkar, daha önceki hissedekiyle karşılaştır; belki karşılaştırmada iz çıkar'",
          "Yeni deneme (karar önceden)", "IZ C", 2, cikti="arastirma_cikti/fon_izi/k26_ozet.csv",
          notu="Dört örneğin 16 ölçüsü BIST süzgeçli havuz yüzdeliğinde; ortak (aralık <= 0,40): mum boyu küçük, üst fitil uzun, düzeni "
               "bozan orta, RSI düşük. Profil (20 mumluk pencere, aynı hissede 60 günde tek) + v4 alış mumu, ertesi açılış, 60 gün önce +%15 "
               "vs aynı süzgeç + alış mumlu rastgele taban: BIST 2023 %80 vs %78 (1,02, n 109), BIST 2024-26 1,02 (n 309), ABD 2023 1,02, ABD "
               "2024-26 1,01. Önceden yazılı 3 devam: D1 sıkı (üst fitil + bozan) 0,97-1,06; D2 BINBN'siz (8 ortak ölçü) n 5-26, BIST 2024-26 "
               "1,26 (n 15), diğerleri 0,77; D3 merkeze en yakın %1 0,92-1,07. Ortak yüz gerçek, sonrası tabanla aynı. Ders: "
               "FON_IZI_ders12_ortak_parmak.pdf."),
    _ik_k("Ç99", "2026-10-26", "İÇERİDEN ALIM (KAP Pay Alım Satım Bildirimi) ve ÇÖLDE İÇERİDEN ALIM, YENİ ÖLÇÜTLE (K27)", "FON_IZI.py (k27)",
          "Cemal: '1 + 3 ile başla, ölçütü değiştir' (yol önerisi: şekil yerine bilgi olayı; görünen alıcı = içeriden alan)",
          "Yeni deneme (yeni ölçüt FI_OLCUT, karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k27_ozet.csv",
          notu="KAP 2022-07 -> 2026-10: 8.609 bildirim, aracı kurum / portföy şirketi hariç 7.313, ayrıştırılan 6.637 (%91; 6.265'i MKK "
               "aktarımı PDF). Net alım 3.477, net satış 2.324 bildirim. Yeni ölçüt: giriş ertesi gün açılış, 60 gün eşli fark (aynı gün, "
               "momentum beşliği x likidite üçlüsü), ay kümeli %95 aralık, hücre içi sıra, 10 yuvalı portföy vs 200 eşli rastgele portföy. "
               "Net alım: BIST 2023 eşli fark -%4,5 (aralık -10,0..+2,1, n 201, sıra 0,46), 2024-26 -%2,6 (-5,8..+0,6, n 418, sıra 0,48). "
               "Büyük alım (oran >= 0,25 puan) n 12 / 30, -%13 / -%5. Çölde alım (K23 süzgeci + küçük mum) n 36 / 62: +%0,9 (-20,9..+22,6) / "
               "-%6,0. Önceden yazılı 3 devam: yönetici alımı -%7,2 / -%2,3; kümeli (30 günde >= 3) -%8,2 (-14,6..-2,0) / -%2,6; düşüş "
               "sonrası olmayan -%9,2 / -%1,9; sıra 0,44-0,51. ABD (SEC Form 4) izin bekliyor. İçeriden alım bildirimi BIST 2022-26'da "
               "olumlu bilgi taşımıyor (2023'te eşlerin gerisinde); Avcı 2023'ün 2008-19 bulgusu bu dönemde yok."),
    _ik_k("Ç100", "2026-10-27", "BİLANÇO SÜRPRİZİ (PEAD): bilanço tepkisi en üst / alt %20, çöl + iyi sürpriz, ABD analist sürprizi (K28)",
          "FON_IZI.py (k28)", "Cemal: 'başla' (yol 2: bilanço sürprizi)", "Yeni deneme (yeni ölçüt FI_OLCUT, karar önceden)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k28_ozet.csv",
          notu="Açıklama günleri: BIST KAP 'Finansal Rapor' (9.176 hisse-dönem, 2022-07 -> 2026-10), ABD Nasdaq takvimi (65.474 kayıt). "
               "Tepki = açıklama öncesi son kapanış -> sonraki ilk kapanış, piyasa medyanına göre; giriş ertesi gün açılış; çeyrek içi dilim. "
               "Eşli fark (60 gün), BIST 2023 / BIST 2024-26 / ABD 2023 / ABD 2024-26: iyi sürpriz (üst %20) +%5,0 / +%1,0 / +%3,1 / "
               "-%1,4 (alt uçlar -0,7 / -0,7 / +1,5 / -3,6); kötü sürpriz (alt %20) -%5,1 / -%3,0 (BIST'te aralığın tamamı eksi) ama ABD "
               "-%1,1 / +%0,3 (ayna kaçınma ölçütü ABD görülmeden yazıldı, tutmadı); çöl + iyi sürpriz +%0,8 / +%2,6 / +%5,4 / +%5,6; ABD "
               "analist sürprizi üst %20 +%1,2 / -%1,8. Önceden yazılı 3 devam: geniş çöl +%2,0 / -%1,4 / +%4,9 / +%2,3; güçlü sürpriz (üst "
               "%10) + çöl +%3,3 (n 19) / +%11,0 / +%4,6 / +%6,3 (sıra 0,54-0,56); iki evre + iyi sürpriz +%14,5 / +%4,1 / +%5,6 / -%0,4. "
               "Hiçbiri dört hücrede tutmadı. En tutarlı aday (güçlü sürpriz + çöl) önceden yazılı ÖRNEKLEM DIŞINDA (BIST 2016-19 / "
               "2020-22, hiç bakılmamış) tersine döndü: -%0,9 / -%13,6 (çöl + iyi sürpriz -%5,4 / -%11,5, 2020-22 aralığı tamamen eksi); "
               "ABD 2016-22 sonucu kararı değiştiremeyeceği için indirmesi durduruldu."),
    _ik_k("Ç101", "2026-10-27", "RİSK SÜZGECİ: K24 çöl sinyallerinde kötü bilanço / A11 / A14 işaretli adaylar kaçınılmalı mı; temiz adaylar (K29)",
          "FON_IZI.py (k29)", "Cemal: 'devam et' (öneri b + a: BIST'e özgü risk süzgeci + portföy)",
          "Yeni deneme (yeni ölçüt FI_OLCUT + ayna kaçınma ölçütü, karar önceden)", "IZ C", 4, cikti="arastirma_cikti/fon_izi/k29_ozet.csv",
          notu="Aday = K24 iki evre sinyalleri (BIST 2023 504 / 2024-26 902; ABD 643 / 1.818). İşaretli (riskli) pay BIST %18, ABD %35. "
               "Eşli fark 60 gün, BIST 2023 / BIST 2024-26 / ABD 2023 / ABD 2024-26: hepsi -%1,4 / -%0,7 / +%3,1 / -%0,5; temiz -%1,3 / "
               "-%0,7 / +%4,1 / -%0,8; riskli -%1,7 / -%1,0 / +%1,4 / +%0,1 (aralıkların hepsi sıfırı içeriyor). Önceden yazılı 3 devam "
               "(işaretler ayrı): kötü bilanço +%0,5 / -%1,7 / -%1,5 / -%0,2; A11 -%8,5 (n 15) / +%5,0 / +%9,7 / -%3,0; A14 n 1-4. Risk "
               "işaretleri çöl adaylarını ayırmıyor; temiz adaylar da eşlerinden iyi değil. İZ DEĞİL."),
    _ik_k("Ç102", "2026-10-27", "ABD İÇERİDEN ALIM (SEC Form 4 açık piyasa alımı) ve ÇÖLDE İÇERİDEN ALIM (K30)", "FON_IZI.py (k30)",
          "Cemal: 'ABD verisi izin vereyim, devam edelim; BIST hep manipülasyon'",
          "Yeni deneme (yeni ölçüt FI_OLCUT, karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k30_ozet.csv",
          notu="SEC çeyreklik Form 4 veri setleri 2016-01 -> 2026-03 (41 çeyrek; SEC kuralı gereği e-posta, Cemal'in izniyle; e-posta koda "
               "yazılmadı). 2022-26'da evrenimizde 7.821 açık piyasa alım bildirimi (>= 10 bin $). Eşli fark 60 gün, ABD 2023 / 2024-26: "
               "alım +%0,1 / +%0,2; büyük (>= 250 bin $) -%1,6 / -%0,9; yönetici -%0,1 / -%0,2; kümeli (30 günde >= 3 kişi) -%1,8 / +%1,6; "
               "çölde alım +%7,3 (aralık +0,3..+16,1, dört şart tuttu) / +%7,2 (aralık sıfırı içeriyor). Önceden yazılı 3 devam: çölde "
               "yönetici alımı +%9,7 (2023 dört şart tuttu) / +%6,1 (tutmadı); çölde >= 100 bin $ -%0,6 / +%7,4; ÖRNEKLEM DIŞI (2016-22, hiç "
               "bakılmamış) çölde alım -%4,5 / -%3,5, sıra 0,46 / 0,49 -> aday güçlenmedi. 2016-19'da büyük alım (+%1,8, aralık artı) ve "
               "kümeli alım (+%2,3) hafif artı; 2023-26'da yok (literatürdeki etki zamanla sönmüş). İZ DEĞİL (ABD-ADAY da değil)."),
    _ik_k("Ç103", "2026-10-27", "ANALİST İZLERİ: içeriden satış, seyrelme, nakit tükenmesi, açığa satış (13F yerine FINRA) ve çöl adaylarına "
          "uygulanması (K31)", "FON_IZI.py (k31)",
          "Cemal: 'en başarılı analistlerin izlediği 4 veri: seyrelme, içeriden satış, nakit tükenmesi, kurumsal sahiplik; yapılmayanları dene'",
          "Yeni deneme (yeni ölçüt + ayna kaçınma, karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k31_ozet.csv",
          notu="Veri: SEC Form 4 (10b5-1 planlı satışlar hariç), SEC finansal tablo veri setleri 2021-2026 (pay sayısı bilanço kaleminden; "
               "dei kalemi veri setinde yok, sonuç görülmeden düzeltildi), FINRA konsolide açığa satış 2022-11 -> 2026-08 (13F'te CUSIP -> "
               "sembol eşlemesi bedava yok). Eşli fark ABD 2023 / 2024-26: içeriden satış (yönetici, >= 100 bin $) +%0,0 / -%0,5; kümeli "
               "satış +%1,2 / -%1,2; seyrelme >= %10 +%0,1 / +%1,2; ağır seyrelme >= %30 +%0,4 / +%2,6; geri alım <= -%3 -%0,9 / +%2,0; nakit "
               "pisti < 4 çeyrek +%2,8 / +%5,1; < 2 çeyrek +%3,4 / +%7,5 (aralık artı) ama sıra 0,47-0,50 (birkaç sıçrayan hisse); açığa "
               "satış kapatma süresi en üst %10 -%0,5 / -%0,8. Önceden yazılı 3 devam: iflas profili (seyrelme + pist < 4) +%1,5 / +%5,5; "
               "temiz çöl (K24 + seyrelme yok + nakit sağlam) +%0,3 / -%1,5; çöl tuzağı +%6,9 / +%0,9. Hiçbir kaçınma ya da yukarı ölçüt iki "
               "ABD hücresinde tutmadı. İZ DEĞİL."),
    _ik_k("Ç104", "2026-10-27", "SADE PORTFÖY ÖLÇÜMÜ: çöl adayları 10 yuvalı portföyde, çıkış kuralıyla; piyasa ve rastgele girişle "
          "karşılaştırma (K32)", "FON_IZI.py (k32)", "Cemal: 'a ile devam et, sade portföy ölçümü'",
          "Düzen ölçümü (iz testi değil; karar önceden: dört hücrede MDD <= 0,8 x piyasa MDD ve getiri/MDD >= piyasa)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k32_ozet.csv",
          notu="Aday = K24 iki evre sinyalleri; 10 yuva, ertesi açılış, maliyet BIST %0,2 / ABD %0,1 tek yön; fiyat 31.08.2026'da kesik. "
               "Toplam getiri (en büyük düşüş) BIST 2023 / BIST 2024-26 / ABD 2023 / ABD 2024-26: piyasa eşit ağırlık +%34 (-%35) / "
               "+%114 (-%19) / +%29 (-%18) / +%89 (-%24); çöl + çıkış (kutu dibi, +%20 sonrası SMA20, en çok 120 gün) +%61 (-%27) / +%29 "
               "(-%35) / +%17 (-%27) / +%42 (-%42); çöl 60 gün tut +%14 / +%21 / +%42 / +%19; rastgele 10 hisse 60 gün tut (50 tohum "
               "ortancası) +%25 / +%107 / +%24 / +%95. Yalnız BIST 2023 tuttu; girişin rastgeleye üstünlüğü de yalnız orada. Önceden yazılı "
               "3 devam: temiz çöl (K29 işaretsiz) +%54 / +%3 / +%37 / +%3; likit çöl +%15 / +%0 / +%16 / -%3; 250 gün tut +%27 / +%155 (-%26) / +%26 / +%28. "
               "Hiçbiri dört hücrede tutmadı. KULLANILABİLİR DÜZEN DEĞİL: 2024-26'da çöl portföyü piyasanın çok altında, düşüşü daha derin."),
    _ik_k("Ç105", "2026-10-27", "SIÇRAYAN HİSSE PROFİLİ: 60 günde ortancanın +%40 üstüne çıkanları önceden ayıran özellik (12 fiyat/hacim "
          "özelliği; keşif 2016-22, test 2023 / 2024-26) + çöl içi, nakit tükenmesi içi, çöküş profili (K33)", "FON_IZI.py (k33)",
          "Cemal: 'piyango gibi sıçrayan hisseler neden ayrışıyor; özellik belirgin olma ihtimali yüksek'",
          "Yeni deneme (keşif / test ayrımı, yeni ölçüt, karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k33_kaldirac.csv",
          notu="Aylık örnek BIST 56 bin, ABD 154 bin satır; sıçrama oranı BIST %9,7, ABD %5,1. Keşifte en güçlü kaldıraçlar: ABD düşük "
               "fiyat 3,4 kat (çöküş de 1,9 kat), yüksek oynaklık 3,3 (çöküş 3,9), çok tavan günü 3,3 (çöküş 3,4); BIST düşük likidite 1,6, "
               "düşük fiyat 1,5. Sıçramayı çöküşten fazla artıran (asimetri >= 1,2) ve iki pazarda da >= 1,5 kat olan özellik YOK: sıçrayan "
               "hissenin önceden görünen izi 'oynak, ucuz, sığ' olmak; aynı iz çöküşü de getiriyor (piyango bileti). Çöl içi ve çöküş "
               "profilinde de seçilen özellik çıkmadı. İZ DEĞİL."),
    _ik_k("Ç106", "2026-10-27", "NAKİT TÜKENMESİ GRUBUNDA İYİ ÇIKANLARIN İZİ (ABD, K31 M3 içinde; 12 özellik + şirket verisi, AUC profili; "
          "K33 D3 + K33-B)", "FON_IZI.py (k33b)", "Cemal: 'nakit tükenmesi araştırmasında bazıları iyi çıkmıştı; onları iyi yapan izi araştır'",
          "Yeni deneme (keşif 2021-22, test ABD 2023 / 2024-26; en çok ABD-ADAY)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k33b_profil.csv",
          notu="Grup 2021-26 1,8 bin olay; iyi çıkan oranı %7 / %14 / %17. Üç dönemin hepsinde ayıran (AUC >= 0,60 ya da <= 0,40): küçük "
               "piyasa değeri (0,35 / 0,29 / 0,31), düşük fiyat, düşük likidite, 52 hafta tepesinden uzak, yüksek oynaklık, büyük tek gün "
               "sıçraması, çok tavan günü. Şirket verisi (nakit / değer, yakma hızı, nakit akışı iyileşmesi, içeriden alım) belirgin değil. "
               "Test: en küçük beşte bir piyasa değeri ABD 2023 +%18 (aralık +2,5 / +30), 2024-26 +%36 (+19 / +57), sıra 0,54 / 0,55, portföy "
               "üstte -> kurala göre ABD-ADAY. ANCAK GEÇERSİZ: evrende yalnız bugün işlem gören hisseler var (ABD 1411, BIST 581; 2026-09 "
               "öncesi biten hisse 0). SEC verisinde nakit tükenen şirketlerin %52 (2021) / %48 (2022) / %39 (2023) / %26 (2024) bildirimi "
               "2026'dan önce kesilmiş (batma, birleşme, borsadan çıkma); bizim evrendeki aynı şirketlerde %0. Küçük ve nakdi biten şirkette "
               "'iyi çıkma' büyük ölçüde hayatta kalanı seçmekten geliyor. Sonuç: ABD-ADAY GEÇERSİZ (hayatta kalma yanlılığı); dürüst test "
               "için borsadan çıkmış hisselerin fiyatı gerek (ücretli veri)."),
    _ik_k("Ç107", "2026-10-27", "BATANLAR DAHİL NAKİT TÜKENMESİ TESTİ: SEC'te o gün bildirim veren bütün şirketler, eski kod kapak "
          "sayfasından, batanların fiyatı Tiingo'dan (rastgele 450 / 824, ağırlıklı); iz = çeyreğin en küçük beşte bir piyasa değeri (K34)",
          "FON_IZI.py (k34)", "Cemal: 'batanlar da test edilsin; parmak izine o dönem uyan bütün hisseler katılsın'",
          "Yeni deneme (hayatta kalma yanlılığı giderildi; karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k34_ozet.csv",
          notu="Evren 2021-01 .. 2026-06: nakdi 4 çeyrekten kısa yeten, nakdi >= 1 M$ 3.564 şirket (bugün kodu olan 2.261, olmayan 1.303; "
               "bunların 306'sının hissesi işlem görmüyor, 173'ü Tiingo'da eşlenmedi, 824 geçerli, 450 örnek, ağırlık 1,83); ölçülen 11.402 "
               "olay (1.590 batan şirket olayı). En küçük beşte bir, aynı ay eşlerine göre ABD 2021-22 / 2023 / 2024-26: YALNIZ HAYATTA "
               "KALANLAR +%6,1 / +%11,0 / +%9,3 (sıra 0,55 / 0,56 / 0,51; hepsi tutar); BATANLAR DAHİL +%2,8 / +%7,9 / +%5,8 (aralık 2023 "
               "+0,8 / +15, 2024-26 +2 / +10; sıra 0,54 / 0,51 / 0,48). Batanlar etkinin üçte birini siliyor; 2024-26'da tipik küçük şirket "
               "eşlerinden KÖTÜ (sıra 0,48), ortalamayı birkaç sıçrayan çekiyor. Karar: İZ DEĞİL (2024-26 sıra şartı tutmadı). K33-B'nin "
               "ABD-ADAY'ı batanlar eklenince düştü. Not: kırpılmamış ortalamada veri hatası (ters bölünme) +%4.800'e çıkıyor; önceden yazılı "
               "+%500 kırpması bunu sınırladı. Borsadan çıkışta son kapanış alındı (iflasta gerçek kayıp daha büyük olabilir)."),
    _ik_k("Ç108", "2026-10-28", "RÜZGÂR BATANLARI AYIRIR MI: nakdi biten ABD şirketlerinde sektör rüzgârı (üretim D9b, SEC SIC sektörü) "
          "varken 2 yılda batma oranı ve getiri (K35)", "FON_IZI.py (k35)",
          "Cemal: 'nakdi yetmeyen şirketlerin arkasında rüzgâr olanlar da batıyor mu; rüzgâra göre alım yapacağım'",
          "Yeni deneme (kapalı 'sektör ısısı'na dokunur, Cemal istedi; karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k35_batma.csv",
          notu="Batma (2 yılda SEC bildirimi kesildi; birleşme dahil), rüzgârlı / rüzgârsız: 2021-22 kohortu %12,7 / %21,6 (oran 0,59, "
               "aralık 0,45-0,74); 2023-24 kohortu %21,2 / %21,1 (oran 1,0). İki kohortta tutmadı -> AYIRMIYOR. Sonradan bakılan (karar "
               "değil): 2021-22 farkın çoğu SPAC'lerden (SIC 6770 boş çek şirketleri, %68 'batma', sektörleri hiç rüzgârlı olmuyor); SPAC "
               "hariç oran 0,83 (0,64-1,07). En küçük nakit dilimde rüzgârlılar biraz az batıyor (%14 / %20, %15 / %23) ama aralık 1'i "
               "içeriyor. Getiri: rüzgârlı nakdi biten şirket eşlerine 2023 -%10 (aralık eksi), 2024-26 +%1,5; rüzgârlı + küçük 2023 -%8, "
               "2024-26 +%10 (sıra 0,49). İZ DEĞİL. Sektör başına batma (2021-22): petrol saha ekipmanı %7,5, elektrik %10, tıbbi cihaz %13, "
               "yarı iletken %13, ilaç %16, yazılım %17, tıbbi laboratuvar %21, SPAC %68."),
    _ik_k("Ç109", "2026-10-28", "PATLAYANLARIN ARKASINDA RÜZGÂR: 60 günde eşlerinin +%40 üstüne çıkan nakdi biten ABD hisselerinde girişte "
          "ve zirve gününde sektör rüzgârı (K35-C)", "FON_IZI.py (k35c)",
          "Cemal: 'patlayanların arkasında rüzgâr var mıydı, patlama zamanında rüzgâr var mıydı'",
          "Yeni deneme (karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k35c_patlama.csv",
          notu="Patlayan 296 / 281 / 646 (2021-22 / 2023 / 2024-26). Zirve gününde rüzgârlı payı patlayan / öteki: %27 / %23 (1,19), "
               "%35 / %17 (2,11), %64 / %50 (1,28): üç dönemde de patlayanlar daha sık rüzgârlı ama >= 1,5 kat yalnız 2023 -> AYIRMIYOR. "
               "Girişte: %22 / %23 (0,97), %6 / %11 (0,54, tersi), %56 / %47 (1,20): girişteki rüzgâr patlamayı önceden haber vermiyor. "
               "Rüzgâr patlamaya EŞLİK ediyor (sektör birlikte yükseliyor) ama alım anında görünmüyor; 60 günlük sepet +%10'u geçtiğinde "
               "hareket çoğu zaman başlamış oluyor."),
    _ik_k("Ç110", "2026-10-28", "RÜZGÂRIN SEBEBİ: sektörü kaldıran sebep (altın, petrol, bakır, çelik, buğday, USDTRY, ABD 10y faiz, TR CDS) "
          "fiyat rüzgârından önce görünür mü; sebep sinyalinde sektör üyelerinin getirisi (K36 + 3 devam)", "FON_IZI.py (k36)",
          "Cemal: 'rüzgâr fiyattan görülünce geç kalınır; önce sebebe bak (1), 2 ondan sonra'",
          "Yeni deneme (kapalı 'sektör ısısı' / 'VIX-DXY'ye komşu, Cemal istedi; DXY yok; eşleme ve karar önceden)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k36_oncelik.csv",
          notu="22 sektör-sebep çifti (BIST 6, ABD 16), sinyal = sebebin 20 günlük değişimi son 250 güne göre z >= 1. ÖNCELİK: sinyalde "
               "sektör zaten rüzgârlı BIST %36 / ABD %24; rüzgârsızken 60 günde rüzgâr çıkma oranı tabana göre BIST 1,03 / ABD 1,08 kat -> "
               "sebep ÖNCE GELMİYOR (tek tek: XBANK-CDS 1,7 ama 13 olay; REIT-faiz 3,0 ama rüzgâr tabanı %4). GETİRİ (eşli fark, BIST 2023 / "
               "2024-26 / ABD 2023 / 2024-26): hepsi -%8,9 / -%0,5 / +%0,9 / +%0,9; erken (rüzgâr henüz yok) -%6,8 / -%1,6 / +%1,1 / -%0,5; "
               "erken + çöl -%2,6 / -%1,4 / +%3,7 / -%8,3. Sebep başına: altın ABD 2024-26 +%15,5 tutar ama 2023 -%17 (ters). Devam: güçlü "
               "sebep (z >= 2) ve yavaş sebep (60 gün) öncelik 1,0-1,2, getiri sıfır civarı; kötü sebep kaçınması hepsi -%4 / -%3 / -%4 / "
               "-%2 (yön doğru, ayna şart iki hücrede tutmadı). İZ DEĞİL. Not: ölçülebilen sebepler de fiyattır (emtia, kur, faiz); sektör "
               "fiyatı onlarla aynı anda hareket ediyor. Teşvik / yasa gibi fiyat olmayan sebepler bedava veride yok."),
    _ik_k("Ç111", "2026-10-28", "BÜYÜKLER ÖNCE, KÜÇÜKLER SONRA: sektörün büyükleri (işlem değeri üst üçte bir) 20 günde piyasayı +%10 "
          "geçmiş, küçükleri (alt üçte bir) henüz gelmemişken küçükleri almak; para akışı (CMF + OBV), temel (BIST temel_duz, ABD SEC), "
          "haber zamanlaması (K28) ve 3 devam (K37)", "FON_IZI.py (k37)",
          "Cemal: '2 ile başla; para akışı tek başına yetmez; temel durum ve haber zamanlamasını atlama; küçük hisse riski sonucu değiştirir mi'",
          "Yeni deneme (kapalı 'sektör ısısı', Cemal istedi; kurallar ve devamlar önceden)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k37_ozet.csv",
          notu="2.700 sektör sinyali (BIST 1.023, ABD 1.677), 11.609 küçük üye olayı. Eşli fark (BIST 2023 / 2024-26 / ABD 2023 / 2024-26): "
               "hepsi +%6,0 / +%1,8 / -%6,4 / +%0,8 (BIST 2023 aralığı 0'ı içeriyor); para akışı iyi +%4 / +%2 / -%1 / -%1; para akışı + temel "
               "-%1 / +%2 / +%2 / -%5; temel -%3 / +%2 / -%4 / -%4. Sığ hisse maliyeti (%1) düşülünce hepsi sıfırın altı. -%30 altı olay payı "
               "BIST %2-3, ABD %7-9; en kötü olay -%60 .. -%89. Haber zamanlaması: sinyalden sonraki 60 günde bilanço gelen olaylarda iyi "
               "tepki olasılığı tabana göre ABD 1,5 / 1,4 / 1,6 (2023 / 24 / 25: tekrarlıyor), BIST 1,2 / 1,3 / 1,05 (tekrarlamıyor) -> şart "
               "iki pazarda da tutmadı. Devam: gevşek eşik, 60 günlük pencere, ayna kaçınma da tutmadı. İZ DEĞİL. Küçük hisse riskine "
               "cevap: eşli ölçü zaten aynı likidite dilimindeki hisseyle kıyaslar; risk bilinince sonuç değişmez, maliyetle birlikte "
               "aleyhe döner. Notlar: BIST büyüklük vekili işlem değeri (piyasa değeri yok); BIST'te hisse ihracı ve ABD'de borç verisi yok."),
    _ik_k("Ç112", "2026-10-28", "EN YAKIN ADAYLAR 3 PAZARDA (yeni karar pazarları ABD + AVRUPA, BIST bilgi): tavan günü kaçınması, geride "
          "kalan + hacim artışı kaçınması, blok hacimli taban günü (K38)", "FON_IZI.py (k38)",
          "Cemal: 'Amerika ve Avrupa tutan iz kabul edilsin, BIST bilgi, Çin sonra; adayları 3 pazarda ölç'",
          "Yeni deneme (Avrupa evreni STOXX 600 + FTSE 250, 581 hisse; karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k38_ozet.csv",
          notu="Eşli fark (ABD 2023 / 2024-26, AVR 2023 / 2024-26, BIST 2023 / 2024-26): tavan günü sonrası +%3,5 / +%1,6, -%0,9 / -%0,8, "
               "-%1,3 / -%0,6 -> ABD'de tavan sonrası hisse eşlerinden İYİ (kaçınmanın tersi), BIST'te hafif kötü; geride + hacim +%3,3 / "
               "+%10,9, +%0,1 / +%0,1, -%5,3 / -%1,5 -> yine ABD'de tersi; blok hacimli taban +%4,4 / +%14,9 (2024-26 dört şart tutar, 2023 "
               "aralık 0'ı içerir), AVR n 8 / 24, BIST -%23 / -%30 (n 9 / 31). Üçü de İZ DEĞİL. BIST'in kaçınma izleri ABD'de ters çalışıyor: "
               "BIST'te tavan ve hacimli düşüş sonrası zayıflık BIST'e özgü (tedbir, tavan kuyruğu, manipülasyon); ABD'de aynı günler "
               "güç belirtisi. Avrupa'da ikisi de yok (sıfır civarı). Avrupa veri temizliği: Londra peni / sterlin 100x geçişleri (5 hisse) "
               "düzeltildi, DIA.MC dışarıda; ilk koşudaki -%18 / +%42 gibi değerler bu hatadandı."),
    _ik_k("Ç113", "2026-10-28", "ŞEKİLLER 3 PAZARDA: çöl (K24), ikili dip, ters omuz baş omuz, RSI / MACD boğa uyumsuzluğu, RSI ayı "
          "uyumsuzluğu kaçınması (K38-B)", "FON_IZI.py (k38b)",
          "Cemal: 'çöl, ikili dip, ters OBO, RSI MACD uyumsuzluk şartlarını ayrı ayrı karşılaştırma olarak koştur'",
          "Yeni deneme (23 Eki gösterge turu eski cetvelle İZ DEĞİL'di; yeni karar pazarlarıyla yeniden, karar önceden)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k38b_ozet.csv",
          notu="Eşli fark ABD 2023 / 2024-26, AVR 2023 / 2024-26, BIST 2023 / 2024-26: çöl K24 +%3,1 (aralık artı) / -%0,5, +%0,4 / +%0,5, "
               "-%1,4 / -%0,7; ikili dip (boyun kırılımı) 0 / 0, -%1,6 / -%1,0, +%10 (n 71, aralık 0'ı içerir) / -%0,6; ters OBO -%2 / +%3, "
               "+%4 (n 18) / -%5, -%25 (n 7) / -%6; RSI boğa uyumsuzluğu 0 / -%1, 0 / -%1, 0 / 0; MACD boğa -%1 / -%1, 0 / -%1, -%1 / +%1; "
               "RSI ayı uyumsuzluğu (kaçınma) -%1 / -%1,5 (ABD 2024-26 aralık eksi ama sıra 0,50), +%1 / 0, +%2 / +%1. Altısı da İZ DEĞİL. "
               "Şekil ve gösterge sinyalleri üç pazarda da eşlerinden ayrışmıyor; en büyük sapmalar küçük örneklemlerde (ters OBO)."),
    _ik_k("Ç114", "2026-10-28", "ABD ÖNCÜ, AVRUPA TAKİP: ABD kaba sektör sepeti piyasayı geçince Avrupa'daki (ve BIST'teki) aynı sektör "
          "üyeleri; 8 olasılık (pencere 20 / 60, eşik %10 / %20, hedef henüz gelmedi / şartsız), ayna yön AVR -> ABD (K39)", "FON_IZI.py (k39)",
          "Cemal: 'Amerika verileri öncü, Avrupa ve Asya takip eder; üstüne git, her olasılığı ayrıca değerlendir'",
          "Yeni deneme (13 kaba sektör üç pazarda eşlendi; ana çeşit ve karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k39_ozet.csv",
          notu="ABD -> AVR, ana çeşit (20 gün, %10, Avrupa henüz gelmedi; 203 sinyal): eşli fark 2016-22 -%0,3, 2023 0, 2024-26 +%1,0; "
               "Avrupa küçükleri +%1 / -%1 / -%1; sekiz çeşidin hepsi -%0,5 .. +%1,3 arasında, sıra 0,49-0,53, hiçbiri tutmadı. "
               "ABD -> BIST de sıfır civarı (en iyi 20 gün %20 eşik 2024-26 +%7 ama sıra 0,56, portföy altta; 2023 olay yok). Ayna AVR -> "
               "ABD: 2023 -%7 / -%13 (Avrupa öne geçince ABD sektörü geride kalıyor, az sinyal), 2024-26 sıfır civarı. İZ DEĞİL. ABD sektör "
               "hareketi Avrupa'ya 'sonradan' geçmiyor; Avrupa aynı gün ya da ertesi açılışta fiyatlıyor, 60 günlük eşli farkta iz kalmıyor."),
    _ik_k("Ç115", "2026-10-28", "SAAT FARKI: ABD güçlü günü / sektör günü / geç seansı -> Avrupa ertesi gün boşluk, ilk saat, gün içi, 5 gün "
          "(günlük hisse 2016-26 + saatlik endeks son 730 gün) (K40)", "FON_IZI.py (k40)",
          "Cemal: 'Avrupa ile Amerika arasında gün değil saat farkı; Amerika'da yükseliş Avrupa'da ne kadar gecikmeli; gecikmeden alım kazandırır mı'",
          "Yeni deneme (karar önceden: alınabilir gecikme = açılıştan sonraki fazla >= +%0,2 ve aralık artı, günlük 2023 + 2024-26 ve saatlik en az 2 endeks)",
          "IZ C", 3, cikti="arastirma_cikti/fon_izi/k40_gunluk.csv",
          notu="GÜNLÜK (ABD eşit ağırlık >= +%1,5 gün; Avrupa ertesi gün, fazla = taban üstü): BOŞLUK +%0,23 / +%0,19 / +%0,23 (2016-22 / "
               "2023 / 2024-26; üçünde aralık artı) -> ABD'nin gece hareketi Avrupa açılış boşluğuna giriyor; GÜN İÇİ (açılıştan alınabilir) "
               "+%0,10 / +%0,24 / +%0,03 (yalnız 2023 aralık artı); 5 GÜN -%0,1 / +%0,1 / +%0,1. Ayna (ABD güçlü düşüş): boşluk -%0,3 .. "
               "-%0,5, gün içi 2016-22 -%0,2, sonra sıfır. SEKTÖR (ABD sektör günü >= +%2 göreli; Avrupa aynı sektör göreli): gün içi +%0,21 "
               "/ +%0,12 / +%0,12 (2016-22 aralık artı, 2024-26 alt uç 0,0000), 5 gün +%0,33 / -%0,02 / +%0,52 (2016-22 ve 2024-26 aralık "
               "artı, 2023 yok). SAATLİK (S&P 500 Avrupa kapanışından sonra >= +%0,7; 29 sinyal / 730 gün): DAX boşluk +%1,1 (aralık artı), "
               "ilk saat -%0,2, gün -%0,04 -> hepsi açılış boşluğunda; Euro Stoxx 50 ve FTSE 'boşluk' ~0 ama ilk saat +%0,5 / +%0,6: bu iki "
               "endeksin açılış değeri eski bileşen fiyatlarıyla basılır (gerçek açılış kotasyonu değil), boşluk ilk dakikalara kayar; DAX "
               "gerçek açılış ihalesi olduğu için doğru ölçü. Örtüşme saatlerinde (16:30-18:30 TR) S&P ile Avrupa eşzamanlı: korelasyon "
               "0,36-0,48. Karar: İZ DEĞİL (günlük gün içi 2024-26 tutmadı). En iyi kalıntı: sektör düzeyinde 5 günde +%0,3-0,5 (iki dönem), "
               "%0,1 maliyet sonrası küçük artı, 2023'te yok."),
    _ik_k("Ç116", "2026-10-28", "KLASİK GÖSTERGELER 3 PAZARDA: Bollinger alt bant dönüşü / üst bant, RSI 30 / 70, MACD kesişimi, altın / "
          "ölüm kesişimi, Fibonacci %61,8 dönüşü (K41-A)", "FON_IZI.py (k41)",
          "Cemal: 'eski adamların icat ettiği formasyonlar, Bollinger / RSI / MACD / Fibo ile al-sat ne kadar başarılı'",
          "Yeni deneme (8 kural, karar pazarları ABD + AVR, BIST bilgi; karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k41_a.csv",
          notu="Eşli fark ABD 2023 / 2024-26, AVR 2023 / 2024-26, BIST 2023 / 2024-26 (on binlerce olay): Bollinger alt dönüş +%0,5 / +%1,7, "
               "-%0,1 / -%0,2, -%0,2 / -%0,7; Bollinger üst (kaçınma) +%0,5 / +%0,6, +%0,5 / +%0,3, -%2 / +%0,3; RSI < 30 -%0,4 / 0, +%0,1 / "
               "-%0,4, +%1,3 / +%0,1; RSI > 70 (kaçınma) +%0,4 / +%0,8, +%0,1 / -%0,2, -%0,8 / -%0,5; MACD kesişimi +%0,3 / +%0,4, +%0,2 / "
               "+%0,1, -%1,9 / -%0,4; altın kesişim 0 / -%0,3, -%0,7 / -%1,1, -%0,8 / -%0,1; ölüm kesişimi (kaçınma) -%1 / -%1, +%0,2 / "
               "+%0,4, -%1,5 / +%1,7; Fibonacci %61,8 +%3,7 / +%4,6 (ABD aralık artı ama sıra 0,52 / 0,50 ve 2023 portföy tabanın altında), "
               "-%0,6 / +%0,1, +%0,6 / -%1,0. Sekizi de İZ DEĞİL. Klasik al-sat kuralları üç pazarda eşlerinden ayrışmıyor; tek kalıntı "
               "ABD Fibonacci (ortalama artı, tipik olay değil)."),
    _ik_k("Ç117", "2026-10-28", "RÜZGÂR SÜREKLİLİĞİ: sektör rüzgârı başladığı gün üyeleri almak (eşli fark + ham fark) ve çöl + rüzgâr (K41-B)",
          "FON_IZI.py (k41)", "Cemal: 'd seçeneğini yap (rüzgâr göründükten sonra ne kadar sürüyor)'",
          "Yeni deneme (kapalı 'sektör ısısı', Cemal istedi; karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k41_b.csv",
          notu="Rüzgâr başlangıcında üyeler, HAM fark (pazar medyanına göre r60): ABD +%1,2 / +%5,7, BIST +%11,8 / +%8,3, AVR -%3,8 / +%0,9; "
               "EŞLİ fark (aynı momentum ve likidite dilimindeki hisseye göre): ABD -%0,7 / +%0,9, AVR -%4,1 / -%0,1, BIST +%1,0 / -%0,1. "
               "Çöl + rüzgâr (rüzgârdan önceki 60 günde K24 çölü): ABD -%1,3 / -%0,4, BIST +%0,4 / -%0,8, AVR n 3 / 35. İZ DEĞİL. Rüzgârlı "
               "sektörün üyeleri pazarı geçiyor ama aynı momentumdaki başka hisseleri geçmiyor: rüzgâr = üyelerin kendi momentumu, üstüne "
               "bir şey katmıyor."),
    _ik_k("Ç118", "2026-10-28", "ABD ÇÖL ADAYI OLAY SÜZGECİ: K24 çöl sinyalleri + son 60 günde iyi bilanço (K28) / son 90 günde içeriden alım "
          "(K30) / temiz temel (K31) ve birleşimleri (K41-C)", "FON_IZI.py (k41)", "Cemal: 'e seçeneğini yap'",
          "Yeni deneme (yalnız ABD, en fazla ABD-ADAY; karar önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k41_c.csv",
          notu="6.912 çöl sinyali; iyi bilanço 253, içeriden alım 710, temiz temel 1.821. Eşli fark ABD 2023 / 2024-26: hepsi +%3,1 / -%0,5; "
               "iyi bilanço +%7,7 / -%0,4 (n 52 / 170; 2023 aralık artı, portföy tabanın altında); içeriden alım +%9,3 / -%1,7 (aralık 0'a "
               "değiyor); temiz temel +%0,3 / -%1,5; bilanço + temel +%0,2 / +%3,3 (n 19 / 71); alım + temel +%3,7 / -%1,5. Hiçbiri iki "
               "hücrede tutmadı -> İZ DEĞİL. 2023'teki artılar 2024-26'da yok (K30'daki 'çölde alım' sonucuyla aynı: tek dönem)."),
    _ik_k("Ç119", "2026-10-28", "K40 SEKTÖR 5 GÜN KALINTISI DIŞ ÖRNEK + MALİYET: hücreler 2016-19 / 2020-22 / 2023 / 2024-26, BIST hedef bilgi (K41-D)",
          "FON_IZI.py (k41)", "Cemal: 'kalıntıyı dış örnekle ayrıca ölç'", "Yeni deneme (karar önceden: dört hücrede fazla - %0,1 > 0 ve alt uç > %0,1)",
          "IZ C", 3, cikti="arastirma_cikti/fon_izi/k41_d.csv",
          notu="Avrupa aynı sektör 5 gün fazlası: 2016-19 +%0,73 (aralık artı), 2020-22 +%0,11 (aralık 0'ı içerir), 2023 -%0,02, 2024-26 "
               "+%0,52 (aralık artı); gün içi +%0,26 / +%0,18 / +%0,12 / +%0,12 (ilk ikisi aralık artı). BIST hedef: sıfır civarı. KALINTI "
               "SAĞLAM DEĞİL (dört hücreden ikisi). Bilgi olarak kalır."),
    _ik_k("Ç120", "2026-10-28", "ÖLÇÜM HATTI KONTROLÜ: geleceğe bakan sinyal (pozitif), yarı pozitif ve rastgele sinyal (negatif, 20 tohum) "
          "üç pazarda FI_OLCUT'tan geçirildi", "scratchpad kontrol.py / kontrol.csv", "Cemal: 'ya sen hata yapıyorsun, görmüyorsun'",
          "Kontrol (iz testi değil)", "IZ C", 0, cikti="arastirma_cikti/fon_izi/kontrol_hat.csv",
          notu="POZİTİF (60 gün sonra >= +%20 olacağı bilinen olaylar): altı hücrede de tutar (eşli fark +%21 .. +%40, sıra 0,68-0,95). "
               "YARI POZİTİF (yarısı iyi, yarısı rastgele): altı hücrede de tutar (+%11 .. +%23, sıra 0,62-0,71); ilk koşuda kontrol "
               "betiğimde hata vardı (tarih sırasına göre ilk 1.500 olay alınmış, test hücrelerine yalnız rastgele düşmüştü), düzeltildi. "
               "NEGATİF (rastgele, 20 tohum x 3 pazar x 2 dönem = 120 hücre): yanlış 'tutar' 0 / 120; aralık alt ucu > 0 oranı %1,7 "
               "(beklenen <= %2,5); dört karar hücresi birden tutan tohum 0 / 20. Hat kör değil (gerçek izi görüyor), sağır da değil "
               "(gürültüye iz demiyor). BAĞIMSIZ KOD DENETİMİ (ayrı model, K38-K41 + ölçüt zinciri, yapay evrende sayısal doğrulama): iz lehine "
               "ağır geleceğe bakma YOK; giriş zamanı, kriz kesiği, eş seçimi, bootstrap, karar mantığı doğrulandı. Düzeltilen 4 orta / küçük "
               "bulgu (sonuç görüldükten sonra, hepsi yeniden koşuldu, hiçbir karar değişmedi): (1) r60 çıkış günü kapanışı NaN ise olay "
               "düşüyordu (Avrupa birleşik takviminde tatil, askı) -> son bilinen kapanış; (2) K39 küçükler alt kümesi giriş - 1 takvim günü "
               "hafta sonuna düşünce boş kalıyordu; (3) K40 saatlik bar etiketi (Yahoo bar zamanı başlangıç; 11:30 barı açılışı) ve aynı "
               "Avrupa gününe düşen iki sinyalin çift sayımı; (4) sterline inen Londra hisselerinde Kur birimi. Not edilen, düzeltilmeyen: "
               "K28 'iyi bilanço' etiketi çeyrek içi dağılımla (etiket sızıntısı, yön belirsiz; K41-C zaten İZ DEĞİL)."),
    _ik_k("Ç121", "2026-10-28", "BİLİNEN ETKİLER KIYASI: momentum 12-1, 1 ay tersine dönüş, küçüklük; ham cetvel (pazar medyanına göre) ve "
          "eşli cetvel (FI_OLCUT) yan yana, üç pazar (K42)", "FON_IZI.py (k42)",
          "Cemal: 'hiçbir yerde iz yok, o zaman kesin sen hata yapıyorsun'", "Hat sınaması (beklenti önceden yazıldı)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k42_ozet.csv",
          notu="HAM cetvel (literatürün ölçtüğü), r60 - pazar medyanı: momentum ABD +%4,5 / +%2,5 / +%7,6 (2016-22 / 2023 / 2024-26), BIST "
               "+%6,5 / +%9,5 / +%8,0, AVR +%0,5 / +%0,4 / +%3,4; 1 ay tersine dönüş ABD +%3,8 / +%7,2 / +%8,4, BIST +%5,0 / +%8,8 / +%5,5, "
               "AVR +%1,0 / +%1,7 / +%0,6; küçüklük ABD +%6,6 / +%10,3 / +%22,0, BIST +%19,5 / +%38,5 / +%11,7, AVR +%2,0 / +%1,4 / +%3,7. "
               "27 hücrenin 21'inde aralık artı -> HAT BİLİNEN ETKİLERİ GÖRÜYOR. EŞLİ cetvelde (aynı momentum ve likidite dilimindeki rastgele "
               "hisseye göre) momentum ve tersine dönüş sıfıra iner (tasarım gereği eşleme siler); küçüklük ABD 2023 / 2024-26'da tutar (+%4,5 / "
               "+%10,7), AVR 2016-22 / 2024-26'da tutar, 2023'te değil, BIST 2023'te tutar -> dört karar hücresinin üçü; ayrıca evren yalnız "
               "hayatta kalanlar (K34 dersi: küçüklük bu veride şişer). Sonuç: 'hiçbir yerde iz yok' doğru değil; ham cetvelde momentum, "
               "tersine dönüş ve küçüklük var, hat onları görüyor. Bizim ölçüt bunların ÜSTÜNE bir şey arıyor; çöl, şekiller, göstergeler, "
               "olaylar o üstüne bir şey katmıyor. DÜZELTME (aynı gün, K43 ile fark edildi): ham cetvelin tabanı pazar MEDYANI idi; r60 "
               "sağa çarpık olduğundan medyan ortalamanın altında kalır ve RASTGELE hisse bile 'medyanı geçer' görünür (K43'te kaçınma "
               "sinyalleri bile +%3-13 çıktı). Taban pazar ORTALAMASINA (eşit ağırlıklı piyasa) çevrildi ve yeniden koşuldu: momentum ABD "
               "+%1,2 / -%0,5 / +%2,7 (yalnız 2024-26 aralık artı), BIST -%1,5 / -%0,9 / +%0,5 (YOK), AVR 0 / 0 / +%2,7; tersine dönüş ABD "
               "+%0,6 / +%4,4 / +%3,5 (son iki aralık artı), BIST -%2,6 / -%1,2 / -%1,9 (ters), AVR sıfır; küçüklük ABD +%3,5 / +%7,3 / "
               "+%17,1, BIST +%11,8 / +%28,1 / +%4,5, AVR +%1,5 / +%0,9 / +%2,9 (7 / 9 aralık artı; hayatta kalma yanlılığıyla şişkin). "
               "Yukarıdaki 'BIST momentum +%7-10' ifadesi medyan hatasıydı; geçersiz. Hat yine bilinen etkiyi (küçüklük) görüyor; momentum "
               "bu verilerde ABD'de zayıf, BIST'te yok."),
    _ik_k("Ç122", "2026-10-28", "ALINABİLİR İZ KARNESİ: 23 sinyal (trend 7, dip 9, öteki 7; çöl yalnız biri) x 3 pazar x 3 dönem; ham fark "
          "(eşit ağırlıklı piyasaya göre) + 10 yuvalı maliyetli portföy (piyasa ve rastgele kıyası) (K43)", "FON_IZI.py (k43)",
          "Cemal: 'çölü boş ver; bir iz var mı, alım satımla kâr edebilir miyiz; tek başına kazandıran varsa kaydet; yükselişte alınca zarar az'",
          "Alınabilirlik testi (karar önceden: ABD 3 dönem + AVR 2 dönem ham fark aralık artı VE portföy > piyasa)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k43_karar.csv",
          notu="Eşit ağırlıklı piyasaya göre 60 gün farkı (ABD 2016-22 / 2023 / 2024-26): TREND: 52 hafta zirve -%0,6 / -%2,0 / +%0,1; trendde "
               "geri çekilme -%1,1 / -%1,2 / -%1,0; SMA200 üstü -%2,1 / -%0,6 / +%0,5; altın kesişim -%0,8 / -%0,6 / +%0,7; MACD -%0,9 / +%0,5 / 0; "
               "momentum +%1,2 / -%0,5 / +%2,7; Fibonacci -%0,1 / +%3,9 / +%4,6. DİP: Bollinger alt +%0,2 / +%0,5 / +%1,0; RSI<30 +%7,7 / +%0,1 / "
               "-%0,7; tersine dönüş +%0,6 / +%4,4 / +%3,5; çöl K24 -%0,8 / +%5,1 / +%1,0; ikili dip -%1 / -%1 / -%1; ters OBO -%2,5 / -%2,7 / "
               "+%3,5; RSI uyumsuzluk +%8,3 / +%3,3 / -%0,5; MACD uyumsuzluk +%5,9 / +%2,0 / -%0,6; blok taban +%1,1 / +%9,2 / +%19,9. ÖTEKİ: "
               "küçüklük +%3,5 / +%7,3 / +%17,1 (üçü aralık artı); tavan günü +%2,1 / +%5,0 / +%4,1; geride + hacim +%1,4 / +%6,4 / +%13,3; "
               "RSI>70, Bollinger üst, ölüm kesişimi, RSI ayı uyumsuzluğu -%2 .. +%1. AVRUPA: hemen her şey -%1 .. +%1 (küçüklük +%1,5 / +%0,9 / "
               "+%2,9). BIST: her şey -%3 .. +%3, küçüklük +%12 / +%28 / +%4,5, ikili dip +%2 / +%9 / +%0 (aralık 0 içerir). PORTFÖY (10 yuva, "
               "60 gün, maliyetli) piyasayı iki gelişmiş pazarda tutarlı geçen sinyal YOK. Karar: ALINABİLİR İZ yok; küçüklük ADAY + BIST (ABD "
               "3 / 3, AVR 2024-26, BIST 2 / 2) ama evren yalnız hayatta kalanlar (K34: batanlar eklenince küçüklük etkisi üçte bir eriyor). "
               "Cemal'in gözlemi veride: 'yükselişte almak' (trend grubu) zarar ettirmiyor ama piyasayı da geçmiyor (-%2 .. +%1); 'dipte "
               "dönüş' grubu ABD'de 2023'te artı, 2024-26'da sıfır, Avrupa ve BIST'te sıfır / eksi."),
    _ik_k("Ç123", "2026-10-28", "INTEM BÖLGESİNİN PARMAK İZİ: 28 Eyl - 9 Eki 2026 sıkışması (düşüş sonrası 195-200), 8 ölçü, iki pencere "
          "(20 / 10 bar), yüzdelik bandında birebir eşleşen bölgeler 3 pazarda, bütün olasılık testleri (K44)", "FON_IZI.py (k44)",
          "Cemal: 'bu bölgenin parmak izini çıkart; bu bölgeler özel; iz çıkacaksa burada çıkar; birebir uyanlarda bütün olasılıklarla test et'",
          "Yeni deneme (çöl tanımı yok, yalnız INTEM'in izi; band ve testler önceden)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k44_ozet.csv",
          notu="INTEM izi (20 bar): 120 gün tepesinden -%42, eğim -0,009 (BIST havuzunda %8'lik dilim: sert düşen), mum 1,42 (mumlar büyümüş, "
               "%85'lik dilim: 'küçük mum' DEĞİL), konum 0,17, RSI 34 (%8'lik), Bollinger genişliği orta, hacim azalan (%25), yeşil payı %35. "
               "10 bar: eğim 0 (yatay), mum 1,1, yeşil %50. Birebir eşleşme (8 ölçü +-0,125 yüzdelik): 20 bar ABD 222 / 26 / 48, AVR 81 / 8 / "
               "16, BIST 56 / 33 / 30 (2016-22 / 2023 / 2024-26); 10 bar ABD 23 / 5 / 9, AVR (band 0,20) 165 / 36 / 51, BIST 13 / 12 / 12. EŞLİ "
               "fark: ABD -%4 / -%9 / -%1, AVR +%2 / +%5 (n 8) / -%2, BIST +%5 / -%2 / +%3; hiçbir hücrede aralık artı (BIST 2016-22 10 bar "
               "+%6, n 13 hariç). HAM (piyasaya göre): hepsi -%3 .. +%5, aralık 0'ı içerir. r60 ortalama ABD +%6 / +%18 / +%15 ama ortanca "
               "+%4 / +%16 / +%1 ve piyasa +%29 / +%89 (2024-26); portföy 18 hücrenin 17'sinde piyasanın altında. Önce +%20 / önce -%20: ABD "
               "%46-58 / %27-38 (pazar tabanıyla aynı). Karar: İZ DEĞİL, PİYASAYI GEÇMİYOR. INTEM'in kendisi: bölge bitiminden 9 işlem günü "
               "sonra -%22 (9 Eki 198 -> 22 Eki 151). Not: bu iz Cemal'in 'küçük mumlu çöl' tanımına uymuyor (mumlar büyümüş, düşüş sert); "
               "düşüş sonrası 10 günlük duraklama, veride bir dönüş noktası değil."),
    _ik_k("Ç124", "2026-10-28", "KISA UFUK, KUTU ÇIKIŞI: INTEM'e birebir eşleşen bölgelerden sonra ilk +-%5 / 8 / 12 hangisi önce (20 gün), kutu "
          "çıkış yönü, kırılımda al kuralı; oynaklık eşli rastgele taban (K45)", "FON_IZI.py (k45)",
          "Cemal: '60 gün bakarsan orası küçük bir durak; altı ve üstü çıkışlarını hemen ara; bana +%8 iz; 60 günlük hedef olamaz'",
          "Yeni deneme (karar önceden: ABD + AVR 2016-26 birleşik, n >= 30, +%8'e önce ulaşma payı rastgeleden >= +10 puan ve aralık artı)",
          "IZ C", 3, cikti="arastirma_cikti/fon_izi/k45_ozet.csv",
          notu="İlk koşu düz rastgele tabanla ABD / AVR +20 puan gösterdi AMA -%8'e ulaşma da +8 puan yüksekti: eşleşen bölgeler çok oynak "
               "(20 günde +-%8'e ulaşan %98'e karşı rastgele %70); oynak hisse iki yöne de çabuk gider. Taban OYNAKLIK EŞLİ rastgeleye "
               "çevrildi (aynı yıl, aynı 20 gün oynaklık dilimi). 20 BARLIK İZ, +%8 önce / -%8 önce: ABD %54,9 / %43,2 (rastgele %43,7 / "
               "%43,2; fark +11,2 puan, aralık +6 .. +17), AVR %50,4 / %41,9 (rastgele %35,5 / %35,9; +15,0, aralık +6 .. +24), BIST %40,4 / "
               "%44,7 (rastgele %48,3; -8,0, TERS). Önceden yazılı kural gereği 'KISA İZ' (ABD + AVR birleşik). DÖNEM SINAMASI (sonradan, "
               "sağlamlık): fark ABD 2016-22 +12,7 (n 240), 2023 +3,1 (n 26), 2024-26 +6,3 (n 51); AVR 2016-22 +15,0 (n 92), 2023 n 8, "
               "2024-26 +32,9 (n 17); BIST 2023 -29, 2024-26 -14. GERÇEKÇİ İŞLEM (+%8 hedef, -%8 stop, boşlukta açılıştan dolum, %0,3 "
               "maliyet, 20 gün): ABD işlem başına +%0,7 (2016-22) / -%0,2 (2023) / +%0,3 (2024-26), rastgele +%0,1 / -%0,6 / +%0,1; AVR "
               "+%0,2 / -%1,6 / +%2,5 (n 17); BIST +%1,8 / -%3,8 / -%1,7. 10 barlık iz: yalnız AVR +14 (ABD 0, BIST +3). Kutu yukarı "
               "kırılımında al kuralı: ABD +10,9 (aralık 0'a değiyor), AVR +1,9 -> tutmadı. SONUÇ: kural harfiyen tutuyor ama etki eski "
               "(2016-22), son dönemlerde ABD'de işlem başına +%0,2-0,3 (çok ince), Avrupa'da örnek az, BIST'te ters. 'KISA İZ (ZAYIF, "
               "2016-22 ağırlıklı)'; ALINABİLİR İZ listesine girmez, canlı izlemeye aday. İLERİ TEST 1 (14 Kas, Ç180): görülmemiş ABD k34 hisselerinde ÖLÇÜLEMEDİ; kendi ölçüsüyle +2,7 puan [-6,8; +12,2] (eski +11,2): yön zayıfladı, kanıt yok; fi_k23_parmak uzunluk şartı geleceğe bakıyordu."),
    _ik_k("Ç125", "2026-10-28", "DÖNÜŞ NOKTASINI MAKİNEYE ÖĞRETME: 1,09 milyon hisse-günü (ABD + AVR + BIST, her 5. gün, 2016-26), 36 özellik, "
          "etiket = 20 günde +%8 -%8'den önce; yıl yıl ileri yürüyen LightGBM; üst %5 sinyal vs oynaklık eşli rastgele; portföy (K46)",
          "FON_IZI.py (k46)", "Cemal: 'tipik dönüş noktasını bul; sen ara, makineye öğret'",
          "Keşif (karar önceden: ABD + AVR 2023 ve 2024-26'da üst %5 fark >= +10 puan, aralık artı, işlem > 0)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k46_ozet.csv",
          notu="Makine öğreniyor: AUC ABD 0,59-0,70, AVR 0,64-0,70, BIST 0,47-0,58 (yıl yıl, görmediği yılda); etiket karıştırılınca 0,505 "
               "(sızıntı yok). ÜST %5 sinyalde +%8 önce gelme payı - oynaklık eşli rastgele: ABD 2023 +3,6 puan (aralık +2), 2024-26 +12,2 "
               "(+11,3); AVR 2023 +4,6 (+1,9), 2024-26 +12,8 (+11,1); BIST 2023 +27,7, 2024-26 +12,6. Gerçekçi işlem (+%8 hedef, -%8 stop, "
               "maliyet) sinyalde ABD +%0,4 / +%2,1, AVR 0 / +%1,2, BIST +%4,4 / +%2,2 (rastgele ~0). KARAR: önceden yazılı kural 2023 "
               "hücrelerinde tutmadı (+4-5 puan < 10) -> İZ DEĞİL; 2024-26'da ikisinde de tutuyor. PORTFÖY (10 yuva, 20 gün tut, sinyal "
               "sırasıyla): ABD 2023 +%27 (piyasa +%29), 2024-26 +%90 (piyasa +%89, düşüş -%30'a karşı -%24); AVR -%2 / +%7 (piyasa +%10 / "
               "+%41); BIST 2023 +%147 (piyasa +%34), 2024-26 +%69 (piyasa +%114). Satır düzeyindeki avantaj portföye taşınmıyor: sinyaller "
               "çöküş günlerinde kümeleniyor, 10 yuva ilk gelenleri alıyor, 20 gün tutma +8 / -8 kuralı değil. MAKİNENİN BULDUĞU TİPİK "
               "DÖNÜŞ NOKTASI (ABD / AVR üst %5 ortanca yüzdelikleri): oynaklık %70-95, son 20 gün en büyük gün %65-85, 20 gün getirisi "
               "%15-35 (düşmüş), 52 hafta konumu %10-35, tepeden düşüş derin, SMA20 / 50 / 200 altında (%15-40), RSI %25-40, piyasanın 20 gün "
               "getirisi düşük (%5-40) = 'düşen piyasada aşırı satılmış oynak hisse'. BIST'te tam tersi profil: yükselen piyasada (piyasa "
               "%93-95) trendde güçlü hisse (r20 %70-80, SMA'ların üstü). En önemli özellikler: piyasanın 60 / 20 gün getirisi, oynaklık, "
               "pazar, SMA200, fiyat, düşüş, likidite."),
    _ik_k("Ç126", "2026-10-28", "ECOGR HAFTALIK YUKARI YUVARLANMA + BBIO DÜŞÜŞ -> İKİ DİP -> YUVARLANMA: parmak izi eşleşmeleri (haftalık ve "
          "günlük) ve açık kural, üç pazar, eşli / piyasa / kısa ufuk / portföy (K47)", "FON_IZI.py (k47)",
          "Cemal: 'birinci slayt haftalık yukarı yuvarlanma, eğim pozitif; ikinci slayt sert düşüş, ufak dip, derin dip, orta bandın altı, "
          "sonra orta-üst bant arası yuvarlanma; bunlarda iz yok mu'",
          "Yeni deneme (karar önceden: eşli ABD + AVR, piyasa ABD + AVR 2023 / 2024-26, kısa ufuk K45 kuralı)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k47_ozet.csv",
          notu="A) ECOGR haftalık (13 hafta, 9 kendi-içi ölçü; eşleşme ABD 154, AVR 122, BIST 59; band 0,20): eşli fark ABD -%1 / +%7 (n 12) / "
               "-%7, AVR 0 / 0 / -%1, BIST -%4 / - / +%1; piyasaya fark sıfır / eksi; kısa ufuk +%8 önce ABD -3 puan, AVR +4, BIST -2 -> hiçbiri. "
               "ECOGR'nin kendisi bölgeden sonra +%40 (tek örnek). B1) BBIO taban sonu (14 Eki; eşleşme ABD 232, AVR 121, BIST 657): eşli ABD "
               "+%3 / -%4 / -%3, AVR +%1 / +%7 (n 9) / 0, BIST -%2 / -%6 / +%5; kısa ufuk ABD +11 puan (aralık +5) ama 2023-26 +6, AVR +7 (aralık "
               "eksi) -> İZ DEĞİL. B2) BBIO yuvarlanma (22 Eki; ABD 68, AVR 27): eşli / piyasa sıfır ve eksi, kısa ufuk ABD -2 / AVR +10 (n 27). "
               "C) AÇIK KURAL (son 40 günde >= -%20, 15-40 barlık taban, iki dip ikincisi derin, kapanışların >= %60'ı SMA20 altı, SMA20 üstü "
               "ilk kapanışta al; ABD 2.988, AVR 402, BIST 1.515 olay): ABD piyasaya fark +%0,6 / +%7,2 / +%12,5 (2023 ve 2024-26 aralık artı), "
               "portföy 2023 +%68 (piyasa +%29), 2024-26 +%207 (piyasa +%89, düşüş -%39'a karşı -%24); AMA eşli fark +%0,8 / +%9,0 (aralık "
               "-%1; aynı momentum ve likidite dilimindeki rastgele hisseye göre fark yok); AVR -%5 / +%1,5; BIST -%5 / 0; kısa ufuk ABD +7 "
               "puan, AVR +8, BIST +4 (hepsi < 10). Dördü de İZ DEĞİL. BBIO kuralının ABD'deki piyasa üstü getirisi, çökmüş hisselerin "
               "2023-26'da sıçraması (K42 tersine dönüş etkisi); aynı momentum dilimindeki öteki çökmüş hisse de aynı sıçrıyor, kuralın "
               "kendisi ayırmıyor; Avrupa ve BIST'te yok."),
    _ik_k("Ç127", "2026-10-28", "SERT DÜŞÜŞ SONRASI MAKİNE: K46 makinesi yalnız son 40 gün tepesinden >= %20 düşmüş hisse-günlerinde (135 bin "
          "satır) (K46-B)", "FON_IZI.py (k46, filtre)", "Cemal: 'burada makine çalıştır; belki ben yanlış tarif ediyorum; sert düşüşten sonra olan bir şey'",
          "Keşif (K46 kuralı: ABD + AVR 2023 ve 2024-26'da üst %5 fark >= +10 puan, aralık artı, işlem > 0)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k46b_ozet.csv",
          notu="AUC 0,50-0,60 (K46'nın 0,6-0,7'sinden zayıf; alt küme zaten 'düşmüş' olduğundan ayrım azalıyor); karışık etiket 0,508. ÜST %5 "
               "vs oynaklık eşli rastgele: ABD 2023 +21,8 puan (aralık +17,5), 2024-26 +16,6 (+14,3), işlem +%2,9 / +%2,4; AVR 2023 +15,3 "
               "(n 59, aralık +3), 2024-26 0,0 (aralık -8) -> İZ DEĞİL; BIST +18,8 / +7,7. PORTFÖY (10 yuva, 20 gün): ABD 2023 +%19 (piyasa "
               "+%29), 2024-26 +%43 (piyasa +%89); AVR +%7 / +%10 (piyasa +%10 / +%41); BIST +%35 / +%118 (piyasa +%34 / +%114): hiçbirinde "
               "piyasayı geçmiyor. Makinenin sert düşüş sonrasında seçtiği: piyasanın kendisi düşmüşken (piyasa 20 / 60 gün getirisi en alt "
               "%5-30), Bollinger genişliği yüksek, mumlar büyük, likit ve fiyatı yüksek hisse = 'piyasa çöküşünde büyük hisse sıçrar'. "
               "Yine piyasa hâli, hisse biçimi değil."),
    _ik_k("Ç128", "2026-10-28", "GENİŞ PARMAK İZİ MAKİNESİ: TradingView örneğindeki üç aile (mum fiziği, trend / konum, kesişim) çok pencereli "
          "ve ölçeksiz + osilatör, para akışı, Fibonacci = 166 yeni ölçü, K46'nın 37'siyle 204 ölçü; aynı makine ve karar (K48)",
          "FON_IZI.py (k48)", "Cemal: 'makineye çok metrik yüklesem belki bir şey bulur; bunun gibi çok detaylı düzgün kod yaz'",
          "Keşif (K46 kuralı: ABD + AVR 2023 ve 2024-26'da üst %5 fark >= +10 puan, aralık artı, işlem > 0)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k48_ozet.csv",
          notu="AUC K46 ile aynı (0,59-0,71; 166 yeni ölçü bilgi eklemiyor); karışık etiket 0,497. ÜST %5 vs oynaklık eşli rastgele: ABD 2023 "
               "+6,9 puan (aralık +5,2), 2024-26 +12,4 (+11,4); AVR +10,8 (+8,2) / +11,3 (+9,6); BIST +23,5 / +9,3. ABD 2023 eşiğin (10) "
               "altında -> İZ DEĞİL (K46'dan iyi: ABD 2023 +3,6 -> +6,9, AVR 2023 +4,6 -> +10,8). İşlem başına ABD +%0,6 / +%2,0, AVR "
               "+%0,4 / +%1,0, BIST +%4,3 / +%2,1. PORTFÖY (10 yuva, 20 gün tut): ABD +%11 / +%218 (piyasa +%29 / +%89), AVR -%1 / +%52 "
               "(+%10 / +%41), BIST +%110 / +%150 (+%34 / +%114); 2022'de (ayı yılı) ABD ve AVR farkı sıfır, BIST 2026 -13 puan. En "
               "önemli ölçüler yine piyasanın 60 / 20 gün getirisi, pazar, 250 gün dibinden bu yana geçen gün, oynaklık, mum boyu, "
               "likidite. Örnek Pine kodundaki 'gap = ta.pvt' hatalı (PVT hacim göstergesi), düzeltilerek kullanıldı."),
    _ik_k("Ç129", "2026-10-28", "GENİŞ MAKİNE SERT DÜŞÜŞ SONRASI: K48'in 204 ölçüsü, yalnız dd40 <= -%20 satırları (135 bin) (K48-B)",
          "FON_IZI.py (k48, filtre)", "Cemal: 'sert düşüşten sonra olan bir şey' (K46-B'nin geniş ölçülü tekrarı)",
          "Keşif (K46 kuralı)", "IZ C", 3, cikti="arastirma_cikti/fon_izi/k48b_ozet.csv",
          notu="AUC 0,49-0,57. ÜST %5: ABD 2023 +15,1 puan (aralık +11,1), 2024-26 +19,5 (+17,2), işlem +%2,2 / +%2,8; AVR +1,7 / +0,6 "
               "(aralık eksi) -> İZ DEĞİL; BIST +32,6 / +8,6. PORTFÖY (20 gün): ABD +%26 / +%125 (piyasa +%29 / +%89), AVR +%4 / +%3, BIST "
               "+%10 / +%165 (+%34 / +%114)."),
    _ik_k("Ç130", "2026-10-28", "KABUK DIŞI DERLEME: her ölçü iki yönde (normal / ters, olayda açığa satış), pazar pazar, bütün birleşimi; "
          "banka = K48'in 203 sürekli ölçüsü + 114 olay kümesi (K43 bankası, K47 BBIO, K24 çöl, K26, K18 kutular, K36 rüzgâr, K27, K28, "
          "K30; 1,01 milyon olay); yön ve seçim yalnız 2016-22'de, karar 2023 ve 2024-26'da; şans denetimi 3 karıştırma (K49)",
          "FON_IZI.py (k49)", "Cemal: 'kural bizi sınırlıyor olabilir, kabuğumuzdan çıkalım; her ölçünün tersi olursa ne olur; bütünü ile ele "
          "alalım; iz değil dediklerimizi derle, tekrar koştur'",
          "Keşif (önceden: öğrenmede >= +5 puan, aralık artı, işlem > 0 seçilir; aynı pazarda iki test döneminde aynı şart = PAZAR İZİ)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k49_derleme.csv",
          notu="Öğrenmede seçilen ölçü-yön (yaklaşık 470 aday / pazar): ABD 4, AVR 10, BIST 9; etiketler karıştırılınca ortalama ABD 1,3, "
               "AVR 2,3, BIST 4,3 (gerçek seçim şansın biraz üstü, en çok AVR). PAZAR İZİ: üç pazarda 0 (şansta da 0). En yakınlar: BIST "
               "'blok taban yukarı' AÇIĞA SATIŞ 2023 +28,9 puan (n 9, az), 2024-26 +28,1 (n 31, aralık +9,6, işlem +%4,5); BIST 'tavan "
               "sonrası' açığa satış 2024-26 +6,6 (aralık +2,7) ama 2023 -1,6; AVR RSI 30 alımı +7,6 / +5,7 (aralık sıfır / eksi). "
               "BÜTÜN (seçilenlerin yönlü ortalaması + olay oyları, haftalık üst %5): test farkı ABD -2,5 / -0,2, AVR -1,9 / +0,7, BIST "
               "-2,2 / +0,8 puan (sıfır); portföy AVR +%13 / +%103 (piyasa +%10,5 / +%41, düşüş -%10) piyasayı geçiyor, ABD +%13 / +%85 "
               "(+%29 / +%89) ve BIST +%10 / +%163 (+%34 / +%114) geçmiyor -> BÜTÜN İZİ yok. Sonuç: kural gevşetilince (iki yön, pazar "
               "pazar, birleşim) de görülmemiş dönemde tutan ölçü yok; 'iz değil' kararlarını eşik sertliği değil, ölçülerin kendisi "
               "veriyor. Not: ikili ölçülerde (fib_tepe_once, p_yesil_1) haftalık yüzdelik eşik bazı dönemlerde boş kalıyor (hepsi zaten "
               "geçmedi)."),
    _ik_k("Ç131", "2026-10-28", "MAKİNE SİNYALİYLE GERÇEKÇİ PORTFÖY: K48 / K48-B üst %5 sinyalleri, 10 yuva, günde en çok 2 yeni giriş, +%8 "
          "hedef / -%8 stop ya da 20 gün; piyasa ve aynı kurallı 20 rastgele portföy (K50)", "FON_IZI.py (k50)",
          "K49 'iz yok çıkarsa durma' sıradaki deneme; Cemal: 'kâr getirecek mi, tek derdimiz bu'",
          "Keşif (önceden: pazar başına 2023 ve 2024-26'da portföy hem piyasayı hem rastgeleyi geçerse ALINABİLİR)", "IZ C", 3,
          cikti="arastirma_cikti/fon_izi/k50_portfoy.csv",
          notu="K48: ABD 2023 +%1 (rastgele +%6, piyasa +%29), 2024-26 +%67 (+%20 / +%89); AVR -%8 / +%4 (+%4 / +%19; piyasa +%10 / "
               "+%41); BIST +%15 / +%38 (+%10 / +%43; piyasa +%34 / +%114); 2019-22 ABD -%30, AVR -%22. K48-B: ABD +%11 / +%31, AVR "
               "+%5 / +%15, BIST +%10 / +%51; hepsi piyasanın altında. Karar: üç pazarda DEĞİL. İşlem başına ortalama artı (BIST +%1,6-2,7, "
               "ABD 2024-26 +%1,2-1,3) ama sinyal seyrek (pazar başına yılda 20-160 işlem), para çoğu zaman nakitte ve +%8 tavanı "
               "kazananı kesiyor: piyasanın güçlü yükseldiği 2023-26'da elde tutmanın gerisinde kalıyor."),
    _ik_k("Ç132", "2026-10-29", "ABD ÇÖL YOLU, AKADEMİK YÖNTEMLERLE: sert düşüş -> küçük mumlu sıkışma (P1 oluşurken) -> kırılım (P2); batanlar dahil ABD "
          "evreni (1.411 + 1.435 nakdi biten + 422 batan); üçlü bariyer (+%20 / -%10 / 60 gün; ayrıca oynaklığa bağlı); meta-etiketleme; "
          "LR -> GBM -> CNN (grafik resmi) -> LSTM merdiveni; özellik grubu katkısı; PBO / DSR; kontroller; Avrupa ve BIST çoğaltma (K51)",
          "COL_YOLU_ABD.py", "Cemal'in iki araştırma görevi (29 Eki): 'formasyon oluşurken gelecekteki performans ihtimali'; birleştirilmiş plan",
          "Keşif (ön kayıt v1.0 + v1.1 dosya başında; denetim düzeltmeleri sonuç görülmeden)", "IZ C", 2,
          cikti="arastirma_cikti/col_yolu_abd/K51_OZET.md",
          notu="İZ DEĞİL. P1 (n 906 / 1.316) üst bariyer isabeti aynı gün aynı oynaklıktaki rastgeleden +2,5 / +2,4 puan (eşik 5; aralık "
               "-0,5 / +0,1), işlem başına net -%1,8 / -%1,1 (taban kadar). İmzasız eşlerden fark yok (H2), kırılım (P2) +1 / +0,6. Oynaklığa "
               "bağlı bariyerle P1 2024-26 +4,3 [+1,6] ama 2023 +2,6 [-0,7] (en yakın aday). Meta-etiketleme +6,6 / +2,6 puan (aralık 0 "
               "içinde); LR, GBM, CNN, LSTM merdiveninde hiçbir basamak kabul edilmedi (CNN sayısal modelden kötü; yığma katkısı yok); 8 "
               "özellik grubunun hiçbiri ek bilgi taşımıyor (akış CMF/OBV/A-D olumlu değil). Kontroller doğru: karışık etiket AUC ~0,5, "
               "geleceği gören özellik 0,78-0,83, plasebo 0. Portföy: P1 bütün adaylar 2024-26 -%48 (beta 0,85), meta 2023 +%12,5 / "
               "2024-26 -%29,5; SPY +%26,7 / +%67,7. PBO ızgara 0,39, DSR 0,03; model x pay PBO 0,57. Önceki aday 'hacimli taban' "
               "tekrarlanmadı (TB -5,5 / -1,2 puan; FI_OLCUT 2024-26 +%12,5 [-3,3]). Resmi ölçüt FI_OLCUT P1 / P2 / HT İZ DEĞİL. Avrupa ve "
               "BIST'te de tutmuyor. Bilgi: kırılımdan sonra 10 gün kutu üstünde kalan P2'ler +13 / +19 puan ama bu gelecekle ayrılmış "
               "grup (bkz. Ç133). Kısıt: 2016-20 yalnız bugün işlem görenler; batan örneklemi 2020-10 sonrası. SONUÇ DENETÇİSİ: küçük artı etkinin "
               "tamamı bugün işlem görenlerden (V_ABD +5,3 / +6,4 puan); sıkıntılı ve batmışlarda -3,2 / -2,5 (Tiingo -9,7 / -5,9); bu ayrım "
               "gelecekle seçim, alınabilir değil; 'rüzgâr yok' kırılımı ve FI_OLCUT paneli de aynı yanlılığı taşıyor; en iyi 20 hisse çıkınca "
               "fark 0; imza 4, imza 3'ten kötü. Ders: yalnız hayatta kalanlarla yapılan küçük hisse testleri iyimser çıkar."),
    _ik_k("Ç133", "2026-10-29", "KIRILIM DEVAMLILIĞI GİRİŞİ: P2 kırılımından sonra 10 gün kapanışlar kutu tavanı üstünde kalırsa 11. gün al (K51-D1; "
          "veri esinli, bağımsız hücreler ABD 2016-22 + Avrupa)", "COL_YOLU_ABD.py (betik k51d1)",
          "K51 'iz yok çıkarsa durma' sıradaki deneme", "Keşif (ön kayıt arastirma_cikti/col_yolu_abd/K51_D1_onkayit.md)", "IZ C", 2,
          cikti="arastirma_cikti/col_yolu_abd/cy_d1.csv",
          notu="İZ DEĞİL. ABD 2016-22 -7,5 puan (n 210), Avrupa 2016-26 +4,6 [-1,6] (n 138); esin dönemi ABD 2023 +2,2, 2024-26 -0,8; BIST "
               "0. Ders: 'süren kırılım' grubunun iyi görünmesi tamamen sonradan bilinen bilgiydi; 10 gün bekleyip girince avantaj yok."),
    _ik_k("Ç134", "2026-10-29", "K51 SONRASI BAĞIMSIZ DENETİM (v1.2): veri bütünlüğü (sayı uzlaşması, point-in-time evren, çıkış sınıflaması, delist / "
          "ham fiyat / kod yeniden kullanımı duyarlılığı, eski-yeni kod), kırılganlık (kaynak, hisse katkısı, yıl, rejim, iki kümeleme), eşleşmiş "
          "kontrollerle beş önceden tanımlı hipotez (H-A sert düşüş + yataylaşma, H-B küçük mum, H-C hacim kuruması, H-D hacimli taban, H-E rejim), "
          "Holm", "COL_YOLU_ABD.py (cy_v12_calistir)", "Cemal'in 'K51 sonrası bağımsız araştırma planı' + 11 maddelik ön kayıt eki (29 Eki)",
          "Keşif (ön kayıt commit 8e99902 / 8e99902+V8; karar koşulları: n >= 30, isabet farkı >= +5 puan, ay kümeli alt uç > 0, net fark > 0, üç "
          "dönemde; 2023-26 bağımsız değil)", "IZ C", 2, cikti="arastirma_cikti/col_yolu_abd/K51_HIPOTEZ_KARARLARI.csv",
          notu="K51 kararı korundu (İZ DEĞİL). Beş hipotezin beşi DESTEKLENMİYOR (H-E AYI 2024-26 yetersiz örneklem). H-A (ÇEK, n 2.300 / 1.104 / "
               "2.536, kapsam %57): eşleşmiş kontrole fark 0,0 / +2,9 / +3,2 puan; 2023-26 birleşik +3,1 [+0,8] (Holm p 0,027) ama eşik 5'in altı "
               "ve 2016-22'de sıfır. H-B (P1 vs imzasız eş, kapsam %17): -1,2 / -1,5 / +4,1. H-C (hacim kuruması, kapsam %10): -3,2 / +6,1 / +9,3 "
               "(aralıklar 0'ı içerir). H-D (HT, kapsam %68): +9,2 / +2,7 / -3,0; HT'den önceki 60 günde ÇEK payı %30 (bağımsız). H-E: AYI 2016-22 "
               "+3,0, 2023 +5,5 (n 35), 2024-26 n 28; BOĞA +3,9 / +2,0 / +3,1. VERİ: 3.267 tekil sembol (1.410 + 1.435 + 422), 2.752 likit; 4 "
               "yinelenen sembol farklı CIK (şirket yeniden kaydı). Tiingo 'batan' 422'nin yalnız 51'i batma benzeri; 171 satın alma benzeri, "
               "153'ünün serisi şirket SEC bildirimini kestikten sonra da sürüyor (kod yeniden kullanımı şüphesi 249 hisse). Delist -30 / 0 / "
               "-100 ve kod kesme senaryoları hücreleri <= 0,3 puan oynatıyor; ham-düzeltilmiş etiket uyumu %99,7; eski kod (b3835d8) ile yeni "
               "kod olay sayıları birebir, farklar <= 0,6 puan. KIRILGANLIK: P1 artısı yalnız bugün işlem görenlerde (2023 +5,3 [+1,9], 2024-26 "
               "+6,4); batanlarda eksi; 2026 (kısmi) -4,3 [-7,5, -2,3] TERS YÖN; en iyi 20 hisse çıkınca 2024-26 +0,6; ilk 20 hisse farkın "
               "%89-139'u. Ders: sert düşüş + yataylaşmanın ~3 puanlık küçük, eşik altı, hayatta kalanlara bağlı etkisi var; küçük mum, hacim "
               "ve hacimli taban ek bilgi taşımıyor. İleri doğrulama: sinyal >= 01.09.2026 (fon krizi istisnası kalkınca), en erken Mart 2027."),
    _ik_k("Ç135", "2026-10-29", "K52 GRAFİK İZİ + ANALİST REVİZYONLARI (v1.3): Yahoo analist not günlüğü ile K51 izlerine (P1, P2) olay öncesi 20 "
          "işlem günü içindeki yeni olumlu revizyonun (tavsiye yükseltme / hedef fiyat yükseltme / alım notuyla başlangıç) ek bilgi katıp "
          "katmadığı; dört grup (G1 iz + teyit, G2a veri var teyit yok, G2b veri yok, G3 / G4 iz yok), H0-H6, Holm, kırılganlık",
          "COL_YOLU_ABD.py (cy_v13_calistir)", "Cemal'in 'K51 — grafik izi + analist revizyonları: yeni araştırma görevi' (29 Eki)",
          "Keşif (ön kayıt commit c33a10e; birincil ölçüt Δ = ortalama(y - e_y | G1) - ortalama(y - e_y | G2a); koşullar n >= 30, Δ >= +5 puan, ay "
          "kümeli alt uç > 0, net fark > 0, üç dönemde; AL sinyali yok; K51 kararı değişmez)", "IZ C", 2,
          cikti="arastirma_cikti/col_yolu_abd/K51_ANALIST_EK_KATKI_TESTI.csv",
          notu="K51 kararı korundu (İZ DEĞİL); analist revizyonu grafik izine EK BİLGİ KATMIYOR. VERİ: Yahoo not günlüğü 310.568 kayıt, 2.515 / "
               "3.267 hisse (V_ABD %99, K34 Yahoo %75, Tiingo 'batan' %10; borsadan çıkanlarda yok); alanlar tarih-saat (UTC, 10-16 yoğun; "
               "aynı gün kayıtları dışarıda), kurum, eski / yeni tavsiye, eylem, hedef fiyat eylemi ve değeri; EPS revizyonu, gerekçe, analist "
               "kişi kimliği, rapor kimliği / tarihsel sürüm YOK (H1 ölçülemez). P1 / P2 olaylarında kaydı olan pay %94. SONUÇ: H0-P1 (n 178 / "
               "122 / 197 vs 990 / 626 / 985) Δ +1,7 / +2,1 / -2,0 puan DESTEKLENMİYOR; H0-P2 (108 / 79 / 128 vs 377 / 320 / 493) +11,4 "
               "[+1,7] / +5,5 [-7,7] / +2,0 [-5,1]: yalnız 2016-22 tutar, DESTEKLENMİYOR (Holm p 0,90). G1 - G2b (veri yok) P1 +10 puan "
               "ama hayatta kalma / takipsizlikle karışık. H2 (tavsiye vs hedef) yetersiz / tutmaz; H3 (>= 2 kurum) TERS işaretli (-5 "
               "puan); H4-P2: olumlu revizyonların %50,4'ü pencere dibinden >= %10 yükseliş SONRASI gelmiş ve H0 tutmuyor -> H4 "
               "DESTEKLENİYOR (P1'de %38,6); H5 eşleşme n < 30 kararsız; H6 AYI yetersiz, BOĞA tutmaz; olumsuz teyit P1 2016-22 -5,7 TERS "
               "YÖN; kurum geçmiş doğruluğu fark yaratmıyor. DENGESİZLİK: G1'in son 60 gün getirisi (+8) G2a'dan (+0,6) ve kapsaması "
               "(15 vs 11,5 kayıt / yıl) yüksek: teyit alan izler zaten yükselmeye başlamış, takip edilen hisseler. KIRILGANLIK: en iyi "
               "20 hisse çıkınca P1 eksi; 2026 kısmi P2 -8,9 ters; V_ABD'de P2 +7,3 [+0,9] (hayatta kalanlar). Ders: analist revizyonu "
               "fiyatı izliyor, grafik izine bağımsız bilgi eklemiyor; sonraki adım analist verisi değil, ileri doğrulama."),
    _ik_k("Ç136", "2026-10-29", "K53 BİLGİ DİRENCİ (v1.4): ilk olumlu analist revizyonundan sonraki 5 günde fiyat zayıf + satış baskısı azalıyor + "
          "oynaklık düşüyor (BDS 0-3); analist dağınıklığı (ADE, hedef fiyat değişim katsayısı); karar gecikmesi (KGS, SPY göreli +%5'e ilk "
          "ulaşma günü: hızlı 1-5 / geç 6-20 / yok); G1-G5 ve destekleyen + çürüten testler (T1-T8)", "COL_YOLU_ABD.py (cy_v14_calistir)",
          "Cemal'in K53 mesajı (29 Eki; ADE / KGS tanımları kesik geldi, Claude ön kayıtta sabitledi)",
          "Keşif (ön kayıt commit 488a407; Δ = ortalama(y - e_y | A) - ortalama(y - e_y | B); n >= 30, Δ >= +5 puan, ay kümeli alt uç > 0, net "
          "fark > 0, üç dönem; T1 / T5 / T6 hiçbiri desteklenmezse hipotez kapanır, eşik uydurulmaz)", "IZ C", 2,
          cikti="arastirma_cikti/col_yolu_abd/K53_HIPOTEZ_TESTI.csv",
          notu="K53 KAPANDI: T1, T5, T6 hiçbiri desteklenmiyor; K51 kararı değişmedi. OLAY: 166 bin olumlu kayıt -> 43.153 ilk olay -> 33.955 "
               "ölçülen (karar günü d0+4 likit); BDS 3 olan %5,9 (1.991). T1 (BDS 3 vs < 3): +0,8 / -1,2 / +2,0 puan; doz-yanıt yok (BDS 2 vs 0 "
               "2024-26 -2,6 ters). T2 (vs grafik var revizyon yok) -0,1 / -4,1 / 0,0; T3 (vs hiçbiri) +0,4 / -2,7 / +1,4; T4 (vs aynı şekil "
               "bilgi yok, G5) +1,2 / -4,0 / +3,5 [0,0]: bilgi eklemiyor; desenin kendi etkisi de yok (G5 - G4 -0,8 / +1,3 / -2,1). T5 KGS: "
               "geç - hızlı -1,2 / -0,3 / -0,1; geç - yok -0,9 / -1,3 / +1,4; hızlı - yok +0,3 / -0,9 / +1,5: gecikmiş tepki primi yok. T6 ADE "
               "üst - alt üçte bir: ham isabet 0,32 vs 0,16 ama tabanla ayarlı +2,4 [+0,2] / +2,8 / +2,5 [+0,6] (Holm p 0,017): dağınıklık "
               "oynaklıkla aynı şey, eşik altı. T7: BDS 3 olayların %74'ü 20 günde hiç tepki vermiyor (BDS 0'da %25), hızlı tepki yalnız %3: "
               "yüksek direnç = haberin yok sayılması; geç ∧ BDS 3 2016-22 +6,9 tutar ama 2024-26 -0,1 (n 184). T8: revizyon yükselişten "
               "sonra / önce fark yok. Bileşenler tek tek: hiçbiri. Kırılganlık: en iyi 20 çıkınca T1 eksi; yıl yıl -1,2 / +1,8 / +4,8 / -3,8. "
               "Ders: 'olumlu habere tepki vermeme' bir iz değil; tepkisizlik çoğunlukla kalıcı. EK DENETİM (Cemal'in 6 maddesi, sonuç "
               "görüldükten sonra; karar değişmedi): eksik SPY / OHLC / hacim ölçülemez sayılır (0 olay düştü); G1 ile G5 dengesiz (kapsama SMD "
               "0,68, likidite 0,72, oynaklık ondalığı -0,85), v1.2 eşleştirmesiyle yalnız %6 (121) olaya eş bulundu, eşleşince denge SMD <= "
               "0,26 ve fark -3,9 / yetersiz / +3,0 (negatif kontrol, nedensel değil); KGS-sonra (d0 kapanışı) geç - hızlı -0,8 / -3,3 / -1,4, "
               "ulaşmayan %57; günlük 311.015 ham kayıt, 447 kopya atıldı, 393 kurum adı -> 371; hedef fiyatı eksik %8; d0+4 panel dışı 9.162 "
               "olay (likit değil / delist K51 kuralı)."),
    _ik_k("Ç137", "2026-10-30", "K54 TARİHSEL HİSSE EVRENİ SAĞLAMLIK DENETİMİ (v1.5): 3.267 sembol SEC başvuru geçmişi (8-K 1.03 / 2.01, 25-NSE, "
          "birleşme belgeleri, 10-K / 10-Q devamı, güncel semboller) + Tiingo sembol listesi (bitiş tarihi) + company_tickers ile 6 sınıfa ayrıldı; "
          "düzeltilmiş evrende (iflas -%100, satın alma ek kayıp yok, kod yeniden kullanımı kesim, belirsiz K51 kuralı, doğrulanamayan çıkar) K51 "
          "P1 / P2 / ES / HT / ÇEK, H-B / H-C / H-D, sessiz ML, K52 H0, K53 T1 / T5 / T6 eski-yeni karşılaştırması", "COL_YOLU_ABD.py (cy_v15_calistir)",
          "Cemal'in K54 görevi (30 Eki)", "Denetim (ön kayıt d4dcdfb; SAĞLAM <= 2 puan + aynı karar + örtüşen aralık; ETKİLENMİŞ; GEÇERSİZ > %30 "
          "belirsiz ya da evren kurulamıyor; K51 / K52 / K53 kararları değişmez)", "IZ C", 2, cikti="arastirma_cikti/col_yolu_abd/K54_ESKI_YENI_TEST_KARSILASTIRMA.csv",
          notu="SINIFLAR: 3.001 halen işlem gören, 19 iflas / tasfiye (hepsi Tiingo, 8-K 1.03), 159 birleşme / satın alma, 9 sembol-kod yeniden "
               "kullanımı (AXP, BG, NE, ZYME gibi aynı şirketin yeni CIK'i de dahil; kesim muhafazakâr), 79 belirsiz (hepsi Tiingo), 0 "
               "doğrulanamayan (3.262 CIK'in hepsi indi, hata 0). K51'in eski 'batma benzeri' 51 tahmininin 19'u iflas, 21'i birleşme, 11'i "
               "belirsiz çıktı. SONUÇ: 66 hücrenin 64'ü SAĞLAM; fark_fark en çok 1,1 puan (H-C 2023 -1,1); ETKİLENMİŞ yalnız K51 P1 2024-26 "
               "(etki +2,39 -> +2,30 puan, aralık alt ucu +0,07'den -0,04'e; karar TUTMAZ aynı; sınırda); GEÇERSİZ: BB sıkışması / EMA (K48 / "
               "K49 / K50 yalnız hayatta kalan V_ABD evreninde koştu, kod K34 evrenini almıyor). Delist bandı (-%0 / -%30 / -%100) P1 / P2 "
               "isabetini 4 ondalıkta oynatmıyor: seri erken biten şirketlerde olay az (P1'de 27 / 42 / 23) ve pencere nadiren seri sonuna "
               "çarpıyor. Sessiz ML AUC 0,51 her iki evrende. K52 / K53: analist kaydı payı sınıf 1'de %84, iflas ve belirsizde %0, birleşmede "
               "%1; sonuçlar yalnız Yahoo kapsamındaki (hayatta kalan) şirketler için geçerli; batıklara sıfır revizyon atanmadı, Tiingo fiyatı "
               "analist yerine kullanılmadı. SINIR: 'SAĞLAM' yalnız mevcut evren içindeki düzeltme için; evren çoğunlukla hayatta kalanlardan "
               "(266 çıkış / 3.267), eksik batanlar olmadan hayatta kalma yanlılığı tam ölçülemez (Kasım Tiingo kotası açık madde). "
               "EK 8 DÜZELTİLMİŞ KOŞU (30 Eki, ön kayıt eki 5fa687d sonuç görülmeden): (1) sınıf 1'de SEC sembolü tek başına kanıt değil: "
               "2.831 Tiingo + SEC, 159 yalnız Tiingo, 11 belirsiz (6 gerçek ETF: DBA / DBB / DBO / UNG / UNL / UUP = evren temizliği maddesi; "
               "BOXL / CIRC / FIEE Tiingo'da 'ETF' türlü; NGTF / SNBRQ Tiingo'da yok); belirsizler çıkarılınca P1 / P2 en çok 0,10 puan oynuyor. "
               "(2) sınıf 2 kronolojisi: 19 iflasın 18'inde 8-K 1.03 T'den ÖNCE (medyan 174 gün; -322 .. 0), hisse iflas sonrası pembe tahtada "
               "sürmüş; T'den sonra başvuru yok. (3) sınıf 4a: son kapanış otomatik nakit bedel değil, bağlama doğrulaması (yeni sembol evrende, "
               "T ±30 gün, oran 1:1 ±%2) kodda ve testte; bu evrende 4a kaydı yok (n = 0; Yahoo serileri bugünkü sembolle geriye dolu). "
               "(4) sınıf 6 = 0, bu yüzden -%30 / -%100 varyantları B ile aynı; hayatta kalma sınırı sınıf 6'dan değil evrende hiç olmayan "
               "batıklardan. ORTAK ÖRNEKLEM: C-yeni = B (B, A'nın alt kümesi); evren etkisi (satır çıkarma) en çok 1,1 puan (H-C 2023, 68 -> 67 "
               "olay), etiket etkisi (çıkış işlemi) en çok 0,06 puan; ML dört örneklemde AUC 0,512 / 0,513, üst-alt üçte bir farkı +0,3 / +0,4 "
               "puan. 55 ana hücrenin 54'ü SAĞLAM, 1 sınırda ETKİLENMİŞ (P1 2024-26: aralık alt ucu +0,02 -> -0,02 puan, karar TUTMAZ aynı; "
               "C-eski'de de -0,08, yani evren etkisi), 1 GEÇERSİZ (BB / EMA). K51 İZ DEĞİL değişmedi."),
    _ik_k("Ç138", "2026-10-30", "K55 DALLANMALI İZ ARAMA — FAZ 0 (tam evren) + FAZ 1 (63 OHLCV hücresi, yalnız KEŞİF 2016-21) + vekil kıyası: "
          "büyük yükselişlerden (Y60 +%30 / Y120 +%50 / Y250 +%100; giriş ertesi gün açılışı; örtüşmez) ÖNCE yalnız o güne kadar bilinen OHLCV "
          "ölçülerinde (D01 fiyat, D02 hacim, D03 oynaklık, D04 zaman / süre, D05 mikro yapı vekilleri, D06 göreli güç, D10 bileşik) fark var mı? "
          "A olay öncesi (gün × oynaklık ondalığı z; Cohen d, ay / blok kümeli aralık, AUC, yıl tekrarı, rejim), B eşleşmiş ileri (beşte bir sinyal, "
          "r60 − kontrol, slot portföyü), C CUSUM; hücre içi Holm + aile BH q 0,10", "K55.py + K55/ (faz0, faz1, vekil; kilit ONKAYIT_K55.md v1.0-v1.4)",
          "Cemal'in K55 planı (30 Eki) ve 'Tam evren Faz 0 koşusu ve Faz 1 başlatma onayı. Kostur'", "Keşif taraması (iz kararı değil: KEŞİF = A etkisi "
          "+ FDR + yıl tekrarı ≥ 5 / 6 + rejim tutarlı YA DA B TUTAR; iz için B tutması + İÇ DOĞRULAMA 2022-23 + BAĞIMSIZ 2024-26 gerekir, ikisi "
          "açılmadı)", "IZ C", 2, cikti="arastirma_cikti/k55_dallanma/tam_evren/K55_FAZ1_RAPOR.md",
          notu="FAZ 0 (koşu K55-20261030-131453-8e47761, evren sürümü 0d00d2c9): 3.260 sembol (sınıf 1: 2.994, 2: 19, 3: 159, 4: 9, 5: 79); dışlama "
               "kısa seri 60, fon 7, 4b kesim 9; 22.502 olay (Y60 13.894); veri kalitesi: kullanılabilir 3.012, hatalı 9, yetersiz 242; sızıntı "
               "testleri (kesme, olumlu / olumsuz kontrol, etiket, eşleşme) geçti. FAZ 1 (K55-20261030-132822-f0034d6, 81,5 dk, 4 işçi; 63 hücre, "
               "1.318 varyant satırı, HATA 0): KEŞİF 25, REDDEDİLDİ 36, VERİ YETERSİZ 2 (D04-S01, D04-S03; eksik pay > %20). B (ileri getiri) "
               "HİÇBİR varyantta TUTMAZ (0 / 164; en büyük eşleşmiş fark +0,010, eşik +0,05); KEŞİF'lerin hepsi A'dan. 25 KEŞİF'in 19'u varsayılan "
               "yönün TERSİNE: olaydan önceki son 5-20 günde hızlanan düşüş (D01-S02 d −0,25, D01-S08 −0,22), zayıf kapanışlar (D05-S01 / S02 / S04 / S08 "
               "d −0,27 .. −0,40), aşağı günlerde hacim payı yüksek (D02-S02 +0,32), SPY / sektör / IWM'ye göre negatif göreli güç (D06-S01 −0,43, "
               "D06-S03 −0,39, D06-S09 −0,28). Bu tek bir bilinen tablodur (sert düşüş sonrası tepki; Ç121) ve olay başlangıcı seçiminin (t0 = +%30'u "
               "ilk yakalayan gün, giriş bir önceki güne göre düşük) mekanik izidir. Yön uyumlu 6: D01-S07 (mum dizisi düzenli, d −0,13), D01-S10 "
               "(KS sapması +0,12), D02-S06 (olağan dışı hacim günü +0,14), D10-S09 (lider−takipçi +0,25), D10-S10 (Mahalanobis +0,14); hepsi küçük "
               "etki ve B'de sıfır. VEKİL KIYASI (bölüm 2.7; 26 hücre; r20, r60, mom12_1, dd250, vol60, log_dv20, ar20, hacim oranı; Spearman; 12,9 dk): "
               "VEKİL 1 (D03-S02 yarı-varyans oranı ← r20 ρ −0,87); eşiğe yakın D06-S09 (r20 +0,79), D10-S09 (r20 −0,79); dd250 katmanlı A'da d'ler "
               "≈ aynı (düşüş derinliği açıklamıyor). C (CUSUM) yanlış pozitif payı 0,61-0,85, tek başına KEŞİF üretmedi. SONUÇ: Faz 1'de İZ YOK; "
               "OHLCV'den türetilen 63 ölçünün hiçbiri eşleşmiş kontrole göre ileri 60 gün getirisi vermiyor; A farkları bilinen tersine dönüş + seçim "
               "etkisi. Dallanma (10 alt hücre) yalnız yön uyumlu ve vekil olmayan 5 hücre için anlamlı, Cemal'in kararı; Faz 2 (D07 / D08: 13F, Form 4) "
               "ve Faz 3 (D09) Cemal'in onayını bekliyor. Çıktılar: tam_evren/ K55_FAZ0_RAPOR, VERI_KAPSAMI, VERI_KALITESI, EVREN, EVREN_DISI, KESIM, "
               "K54_TUTARLILIK, OLAYLAR, SIZINTI_TESTI, HUCRE_ISKELE, FAZ1_RAPOR (+ koşu sonrası notlar), ADAYLAR, HUCRE_SONUC, VARYANTLAR, "
               "COKLU_TEST, VEKIL, KOSU / KOSU_FAZ1 / KOSU_VEKIL json (kod + veri + ayar sha)."),
    _ik_k("Ç139", "2026-10-30", "K56 K51-K55 ETKİ VE MEKANİZMA ARAŞTIRMASI — FAZ 0: bütün K51-K55 bulgularının envanteri, mekanizma hipotezleri (M01-M19), "
          "veri kaynakları (28; kapsam / gecikme / maliyet / lisans), küçük örneklem erişim testi (12 sembol, G1 / G2 / G3 / G6), M01 olay başlangıcı "
          "seçim etkisi için sentetik sıfır sınaması, dört bağımsız denetim", "K56.py + K56/ (ortak, etki_envanteri, mekanizma, kurumsal_sahiplik, "
          "iceriden_islemler, finansal_mekanizma, kurumsal_olaylar, islem_davranisi, karsit_ornekler, mekanizma_raporu, surucu; kilit ONKAYIT_K56.md v1.0 / v1.0-a / v1.1)",
          "Cemal'in 'K51-K55 Etki ve Mekanizma Araştırması' talimatı (30 Eki)", "Mekanizma araştırması Faz 0 (iz kararı yok; K51 İZ DEĞİL ve K55 İZ YOK değişmedi)",
          "IZ C", 2, cikti="arastirma_cikti/k56_mekanizma/K56_FAZ0_RAPOR.md",
          notu="ENVANTER 265 bulgu (K51 90, K52 34, K53 22, K54 52, K55 67); K55 sayıları CSV'den otomatik, öteki metinler okuyucu ajanlardan, kaynak "
               "kararlarıyla mekanik denetimli (her kaynak kodu envanterde; 1 kürasyon düzeltmesi). Ön sınıf (ön kayıtlı mekanik kural): ETKİ YOK 103, "
               "ETKİ SAĞLAM DEĞİL 49, YÖNTEM DENETİMİ 39, VERİ YETERSİZ 29, YANLIŞ BULGU ADAYI 22 (21 M01 + K53-T7 tanımsal), BETİMLEYİCİ 18, İLİŞKİ VAR "
               "NEDEN BELİRSİZ 4 (K55 D01-S05, D02-S05, D04-S04, D06-S04), ALTERNATİF AÇIKLAMA 1 (K52 H4: revizyonlar fiyatı izliyor). K51-K54'te "
               "kaynakta desteklenen ve eser adayı olmayan etki YOK. M01 SENTETİK (bilgisiz yapay veri, 4 evren × 400 hisse, K55'in olay tanımı ve aynı "
               "kod; kilit sentetik koşudan önce): 25 KEŞİF hücresinin Y60'ta 21'inde yapay veri gerçek A farkının >= %50'sini üretiyor (oran medyanı "
               "1,18); KEŞİF'i sağlayan 125 (varyant, ufuk) satırında 109 mekanik, hücre çoğunluğu 18 / 25. Denetçinin ön kayıt dışı kontrolü (K55 paneli, "
               "KEŞİF, Y60): olay etiketi seçimsiz kurulunca gerçek d -0,25..-0,43'ten -0,016..-0,049'a iniyor (ters farkların ~%90'ı olay tanımından; "
               "küçük kısa dönem dönüş kalıntısı). Ters yönlü KEŞİF 20 (Ç138'deki 19, D03-S02 vekil sayılmıştı). ERİŞİM (temiz önbellek, 131,9 MB): "
               "GECTI 27 / KISMI 9 / ATLANDI 1. 13F 2013q2+ (KEŞİF ~1,1 GB; OpenFIGI adi hisse CUSIP 9/10, örneklem geri eşleme 5/7; kapanmış eski "
               "CUSIP'ler bulunamıyor), Form 4 2006q1+ (KEŞİF ~248 MB; 10b5-1 işareti 2023q2+, öncesi dipnot vekili %43,5), companyfacts 12/12 (CIK "
               "değişimi ve IFRS boşluğu; hisse sayısı bölünme / birleşme düzeltmesiz), SEC başvuru özeti YEREL (8-K madde kodu tam), MIDAS 2012+ (2016q1 "
               "K55 kapsamı %66: REIT / yabancı yok), Reg SHO hacmi 2009-08+ (tesis dosyaları), FINRA SI 2017-12+, ATS genel API'de KEŞİF yok, FTD 2004+, "
               "SEC askıya alma 1.349 (resmî kuşku kaydı; tarih şartlı 9 eşleşme, panelde 0). DENETİM: 4 bağımsız denetçi 45 bulgu; 42 düzeltildi, 3 kısmen "
               "(DGP kalibrasyonu, bölünme denetimi, oran yorumu -> Faz 1). Kasıt kanıtı yalnız kesinleşmiş karar. Ön kayıt v1.1 (sonuç sonrası, Faz 1 "
               "öncesi): seçimsiz kontrol protokolü, aday etiketi, hipotez kaydı donduruldu. test_k56 15/15. Çıktılar arastirma_cikti/k56_mekanizma/."),
    _ik_k("Ç140", "2026-10-31", "K56-F1A FAZ 1 YEREL (KEŞİF 2016-21, keşif verisi yeniden kullanımı): K55'in KEŞİF'i sağlayan 125 (hücre, varyant, ufuk) "
          "satırında seçimsiz kontrol (A1: (i) ilk geçiş, (ii) bütün nitelikli günler, (iii) olay dizisinden rastgele gün), kalan etki denetimi (A2: oynaklık, "
          "COVID, beta, sektör), haber ve birleşme bileşimi (A3: SEC başvuruları, G1 olay / G7 eş, ÖNCESİ sızıntısız, SONRASI açıklayıcı), kalibre sentetik",
          "K56.py faz1a + K56/faz1_yerel.py (K55 kodu aynen: degisken_hesapla, _z_gun_vd, d_boot_ay); ön kayıt ONKAYIT_K56 v1.2-A, v1.2-b",
          "Cemal'in Faz 1 kararları (31 Eki): ilk üç analiz, yeni veri yok", "Mekanizma (iz kararı yok; K55 İZ YOK değişmedi)", "IZ C", 2,
          cikti="arastirma_cikti/k56_mekanizma/faz1_yerel/ (SON.json)",
          notu="(i) K55'i birebir üretiyor (d farkı < 1e-7). A1 satır: MEKANİK 116 (gerçek + sentetik 104, gerçek veri 12), KISMEN MEKANİK 2, TERS KALINTI 7, "
               "GERÇEK ETKİ KALIYOR 0 / 125; d(i) medyanı -0,265 -> d(ii) -0,014 (oran medyanı 0,04). Hücre: MEKANİK 22, KISMEN 1 (D04-S04), TERS KALINTI 2 "
               "(D10-S02, D10-S10; tek satır, |d(ii)| < 0,08). (iii) duyarlılık 123 / 125 'GERÇEK ETKİ KALIYOR' (ön kayıt: yalnız duyarlılık): olay başına "
               "bir gün; açıklayıcı tanıda aynı dizilerin bütün günleri bir arada d -0,016 (ayrışma olay / gün ağırlığı; neden doğrulanmadı). A2: 9 satırın 2'sini "
               "beta / COVID denetimi açıklıyor (D02-S08 Y120 ters kalıntı); öteki küçük kalıntılar açıklanmadı. A3: ÖNCESİ'nde fark küçük (Y60 8-K 2.02 +1,5 puan, "
               "Y250 herhangi 8-K +5,1); SONRASI (açıklayıcı): yükselişten sonra hisse ihracı Y120 +6,6 / Y250 +10 puan, birleşme Y60 -2,1 puan: büyük "
               "yükselişler birleşme / haberle açıklanmıyor. Kalibre sentetik (GJR, sıçrama): 119 / 116 satırda bilgisiz yapay veri farkı tam üretiyor (oran "
               "medyanı 1,45 / 1,41); yapay olay oranı gerçeğin altında. İlk koşu (6cf01ae) denetimde dönem sızıntısı bulunduğu için geçersiz, saklandı."),
    _ik_k("Ç141", "2026-10-31", "K56-IC İÇ DOĞRULAMA 2022-23: yalnız önceden belirlenmiş 125 satır / 64 varyant; B1 K55 A (ilk geçiş), B2 seçimsiz kontrol "
          "(belirleyici), B3 K55 B (eşleşmiş ileri getiri), B4 bileşim + A2; BAĞIMSIZ 2024-26 kapalı (kod kapısı), kilit dosyası üretildi (açılmadı)",
          "K56.py ic + K56/faz1_yerel.py, ortak.donem_kapisi, K56_BAGIMSIZ_KILIT.json; ön kayıt v1.2-B, v1.2-b",
          "Cemal'in Faz 1 kararları (31 Eki): İÇ açılabilir, BAĞIMSIZ kapalı", "İÇ doğrulama (iz kararı yok)", "IZ C", 2,
          cikti="arastirma_cikti/k56_mekanizma/ic_dogrulama/ (SON.json)",
          notu="B1: 119 / 125 satır geçti -> 23 hücre 'DOĞRULAMA BEKLİYOR (A, ilk geçiş)', 2 hücre İÇ'TE TUTMADI (D01-S05, D01-S10). Ama B2 seçimsiz kontrol: "
               "MEKANİK 112, KISMEN 10, TERS KALINTI 3, GERÇEK ETKİ KALIYOR 0 / 125 (d(i) medyanı -0,369 -> d(ii) -0,007); hücre MEKANİK 21, KISMEN 2 "
               "(D01-S10, D02-S05), TERS 1 (D01-S05), BELİRSİZ 1 (D01-S08). Yani K55 A farkları 2022-23'te tekrarlıyor ama tekrar eden şey olay tanımının "
               "seçim etkisi. B3: 64 / 64 TUTMAZ. B4: A2 13 satırın 1'ini açıklıyor; A3'te yalnız Y250 SC 13D / 13G (önceki 20 gün) +6 puan. Yeni eşik / "
               "değişken türetilmedi. Kilit: kod (K56 + bütün K55 + COL_YOLU_ABD + FON_IZI), ön kayıt, hipotez, eşik, veri tanımı (açılışta yeniden hesap)."),
    _ik_k("Ç142", "2026-10-31", "K56-EVREN2 BATAN ŞİRKETLERLE EVREN v2 (aday ve hazırlık): Ö1 K34 eşleme kuralı (212), Ö2 Tiingo listesinden KEŞİF döneminde "
          "biten adi hisseler (278, tohum 56; havuz 1.626); SEC geçmişi ve ön sınıf; Tiingo indirici (1 Kasım'dan önce istek yok), evren v2 / etki sürücüsü",
          "K56.py evren2_aday / evren2_indir / evren2_kur + K56/batan_evren.py, K56/evren_v2.py (K55 evren_insa / panel_kur / olaylar aynen); ön kayıt v1.2-C, v1.2-a, v1.2-b",
          "Cemal'in Faz 1 kararları (31 Eki): Tiingo Kasım kotasıyla batanlar, yeni evren sürümü", "Veri / evren (iz kararı yok)", "IZ C", 2,
          cikti="arastirma_cikti/k56_mekanizma/evren_v2/",
          notu="Ö2 ilk tanımı (25-NSE sembolü) 3 aday verdi: EFTS sembolü SEC'in GÜNCEL tablosundan, batan şirkette yok (v1.2-a sapma, fiyat görülmeden). "
               "Ö1 ön sınıf: BİRLEŞME 149, VERİ SAĞLAYICISI KAYBOLMASI 27, İFLAS 25, TASFİYE 10, SEMBOL DEĞİŞİKLİĞİ 1; 40 birim / varant / hak ve 4 sembol "
               "çakışması indirilmeyecek (v1.2-b). Ö2'nin CIK'i indirme sonrası Tiingo adı + 25-NSE tarihiyle (4.825 başvuru). Getiri asıl kural: seri bitince "
               "TANIMSIZ, son fiyat tasfiye ödemesi sayılmaz, delist getirisi uydurulmaz. İndirme ve evren v2 / etki 1-2 Kasım (AÇIK)."),
    _ik_k("Ç143", "2026-10-31", "K56-AYR (iii) RASTGELE GÜN / BÜTÜN GÜNLER AYRIŞMASI (KEŞİF + İÇ, yapay veri denetimiyle): 125 satırda olay ağırlıklı E1 ile "
          "gün ağırlıklı E2 farkı (G = işaret × (E1 − E2) = −Cov(L, f) / ort L), olay düzeyi kümeler (ay, sembol|yıl, blok60 karar; olay, zincir bilgi), "
          "konum bantları (1 / 2-5 / 6-20 / 21+), dört Faz 0 + iki kalibre yapay spek; BAĞIMSIZ'da koşulmaz",
          "K56.py ayrisma + K56/ayrisma.py; ön kayıt ONKAYIT_K56 v1.3-E, v1.3-a, v1.3-c",
          "Cemal'in BAĞIMSIZ kararı (31 Eki) madde 4", "Mekanizma (iz kararı yok)", "IZ C", 2,
          cikti="arastirma_cikti/k56_mekanizma/ayrisma/ (SON.json)",
          notu="KEŞİF: 107 / 125 satır mekanik (AĞIRLIK ETKİSİ + MEKANİK 99, MEKANİK 8), BELİRSİZ (yapay) 8, AYRIŞMA YOK 5, AĞIRLIK ETKİSİ (gerçek veriye "
               "özgü) 3, AÇIKLANMADI 2; hücre MEKANİK 17 / 25. İÇ: 97 mekanik (54 + 43), AYRIŞMA YOK 21, BELİRSİZ 3, gerçeğe özgü 3, AÇIKLANMADI 1; hücre "
               "MEKANİK 16 / 25. Medyanlar E1 / E2 / G: KEŞİF -0,278 / -0,020 / +0,280, İÇ -0,340 / -0,081 / +0,250. Konum bantları: dizinin ilk günü -0,30 "
               "(KEŞİF) / -0,38 (İÇ), 2-5. gün -0,33 / -0,37, 6-20. gün -0,13, 21+ +0,12 / +0,15. Yapay (bilgisiz) veri aynı deseni üretiyor (G +0,30..+0,40). "
               "Anlamı: (iii) tek rastgele gün olay başına eşit ağırlık verir, kısa dizilerin ilk günleri (en düşük z) ağır basar; (ii) bütün günler uzun "
               "dizilerin sonraki (sıfıra dönen) günlerini sayar. Ayrışma büyük ölçüde olay tanımının ağırlık mekaniği, gerçek bilgi değil. İlk koşu (3b61627) "
               "geçersiz, saklandı; son koşu a6cbe6a (önceki 255ae9d / bab4d5d koşularıyla birebir)."),
    _ik_k("Ç144", "2026-10-31", "K56-PBO PBO / DEFLATED SHARPE (K55 ön kaydı §7; KEŞİF + İÇ, donem60): 64 KEŞİF yapısı, K55 B seçiminin eşleşmiş net "
          "farkının aylık serisi; CSCV 16 blok, DSR N = 64; yön A (keşfedilen) ve kayıt (K55 B); BAĞIMSIZ'da koşulmaz",
          "K56.py pbo + K56/pbo_dsr.py (COL_YOLU_ABD.cy_pbo / cy_dsr aynen); ön kayıt v1.3-F, v1.3-b",
          "K55 ön kaydı §7 + Cemal'in BAĞIMSIZ kararı (31 Eki)", "Aşırı uyum denetimi (iz kararı yok)", "IZ C", 2,
          cikti="arastirma_cikti/k56_mekanizma/pbo_dsr/ (SON.json)",
          notu="A yönü: PBO 0,332, DSR 0,665 (en iyi yapı D01-S08|20, aylık SR 0,30; etkin T ile DSR 0,596, bilgi). Kayıt yönü: PBO 0,236, DSR 0,390 (en "
               "iyi D06-S05|tek; etkin T 0,437). K51 H8 (PBO < 0,5 VE DSR >= 0,95) ikisinde de tutmuyor: 'aşırı uyum riski yüksek'. 87 ay. DSR alt "
               "örneklem bilgi sütunu ilk koşuda yanlış yöntemle hesaplanmıştı (v1.3-b düzeltildi; karar vermiyordu)."),
    _ik_k("Ç145", "2026-10-31", "K56-SIZ İÇ → BAĞIMSIZ DOLAYLI ERİŞİM SINAMASI: T0 K55 panel / olay tablosunun baştan yeniden üretimi; T1 aynı evren, fiyat / "
          "endeks / SEC özeti 2023-12-31'de kesik, İÇ motoru (S / H / B3), bileşim, ayrışma İÇ ve PBO / DSR yeniden; T2a / T2b evren de kesik veriden "
          "(T2b kesimden sonra giren K34 dışarıda); tolerans 0 (ayrışma 1e-12 + kimlik özdeşliği, v1.3-c)",
          "K56.py sizinti + K56/sizinti_denetimi.py; ön kayıt v1.3-G, v1.3-a, v1.3-b, v1.3-c",
          "Cemal'in BAĞIMSIZ kararı (31 Eki) madde 2: 'İç doğrulama sırasında bağımsız döneme dolaylı erişim olmadığı doğrulanacak'",
          "Denetim (iz kararı yok)", "IZ C", 2, cikti="arastirma_cikti/k56_mekanizma/sizinti/ (SON.json)",
          notu="KARAR: İÇ hesaplarında 2023-12-31 sonrası bilgiye dolaylı erişim YOK. T0 panel 4.909.423 satır ve 22.502 olay birebir. T1b S (125) / H (25) / "
               "B3 (64) birebir; T1a bileşim birebir; T1 ayrışma (125 satır, karar dahil) ve PBO / DSR birebir. Beklenen fark (v1.3-G): İÇ A3 bileşimi başvuru "
               "geçmişini tam SEC özetinden okuyor; kesik özetle Y60 2731 -> 2711 olay, bir satırın sınıfı değişiyor (Y120 8-K 2.02 önceki: fark yok -> G1 > G7; "
               "açıklayıcı tablo, karar vermez). T2a (evren kesik veriden, 3.061 sembol) en büyük d farkı 0,0015, T2b 0,0104; sınıf değişimi 0, aralık "
               "yarı genişliğinin %25'ini aşan 0: ihmal edilebilir. İlk iki tam deneme test hatasıyla geçersiz (tohum etiketi; yapay karar sütunları), "
               "NOT.md ile saklandı; düzeltme v1.3-c. Görünmeyen sınırlamalar beyan: hayatta kalma, 2026 bölünme / temettü düzeltmesi, güncel sektör / CIK."),
    _ik_k("Ç146", "2026-11-01", "K56-BAG BAĞIMSIZ DOĞRULAMA 2024-26 (TEK AÇILIŞ, K55_125_B) + K55 NİHAİ KARAR: yalnız ön kayıtlı 125 satır / 64 varyant; B1 K55 A "
          "(ilk geçiş), B2 seçimsiz kontrol (belirleyici), B3 K55 B (eşleşmiş ileri getiri), A2 / A3; asıl K55 etiketleri, duyarlılık BAGIMSIZ_B (pencere "
          "sonu <= 2026-08-31); yeni keşif / eşik / gösterge yok",
          "K56.py bagimsiz + K56/faz1_yerel.py; kilit K56-BAG-KILIT-20261031-231806 (kod a6cbe6a, kilit commit 711a17b); ön kayıt v1.2-B, v1.3-D, v1.3-H, v1.3-d",
          "Cemal'in BAĞIMSIZ kararı (31 Eki), madde 1-5 ve 9", "Doğrulama + K55 nihai karar", "IZ C", 2,
          cikti="arastirma_cikti/k56_mekanizma/bagimsiz/K56-BAG-20261031-231920-f993f1f/ (açılış kaydı K56_BAGIMSIZ_ACILIS.csv: TAMAMLANDI)",
          notu="K55 NİHAİ: İZ YOK (hücre çoğunluğu TERS KALINTI; MEKANİK çoğunluk yok, GERÇEK ETKİ çoğunluğu yok). B2 satır: MEKANİK 62, TERS KALINTI 56, "
               "KISMEN 3, GERÇEK ETKİ KALIYOR 4 (hepsi D06-S03 Y120 / Y250; d(i) ~0, d(ii) +0,14..+0,21; hücre çoğunluğu değil, KEŞİF / İÇ'te yok, "
               "duyarlılık-B'de 0: dağınık, iz sayılmaz). Hücre: TERS KALINTI 12, MEKANİK 10, KISMEN 2, BELİRSİZ 1. d(i) medyanı -0,175 -> d(ii) +0,008 "
               "(TERS satırlarda d(ii) medyanı +0,041: K55 yönünün tersine küçük kalıntı). B1 64 / 125 (hücre 13 TEKRARLADI / 12 TUTMADI): K55 A farkı "
               "kısmen tekrarlıyor ama seçim etkisiyle (B2). B3 64 / 64 TUTMAZ. (iii) 116 'GERÇEK ETKİ' etiketi seçimsiz kontrol değildir (yapay veride "
               "d(iii) ≈ d(i)). Duyarlılık-B: GERÇEK 0 / 125, TERS 61, MEKANİK 62; hücre TERS 13, MEKANİK 10; B3 64 / 64 TUTMAZ. Üç dönemde (KEŞİF, İÇ, "
               "BAĞIMSIZ) seçimsiz etiketle gerçek etki yok; karar yeni eşikle kurtarılmaz (madde 9). Ayrışma ve PBO / DSR ön kayıt gereği BAĞIMSIZ'da "
               "koşulmadı (Ç143, Ç144). EVREN2 (Ç142) bu kararı değiştirmez (ayrı rapor, 1-2 Kasım)."),
    _ik_k("Ç147", "2026-11-08", "KRİPTO YENİ TOKEN +%100 GÜNÜ: önceden tespit ve sonrası (RITUAL/USDT vakası); 759 yeni token (2024-01 .. 2026-09 listelenen, "
          "Binance aynası data-api.binance.vision + OKX v5 + Gate v4; 454.984 token-gün, 7 Kas 2026'da kesik); liste sonrası getiriler, +%50 / +%100 gün "
          "sıklığı, olay sonrası getiriler, OHLCV öncü sinyaller (eğitim: liste < 2025-07-01, test: sonrası; eşikler eğitimde seçildi, yazıldı, sonra test)",
          "arastirma_cikti/kripto_yukselis/kod/ (indir.py, panel.py, olc.py, esikler.json)",
          "Cemal (8 Kas 2026): 'Bu gibi yükseliş nasıl tespit edilir, derin araştırma yap'", "Yeni deneme (kripto, BIST / ABD dışı pazar)", "", 1,
          cikti="arastirma_cikti/kripto_yukselis/reports/Kripto yeni token yükselişi tespiti.md (+ research_notes/, kod/sonuc_*.md)",
          notu="İZ DEĞİL. Liste günü kapanışından medyan: 7 g -%14, 30 g -%30, 90 g -%53, 180 g -%68. +%100 günü (406 olay) ertesi açılıştan medyan: "
               "+1 g -%16, +7 g -%35, +30 g -%49 (taban: aynı tokenların herhangi günü 30 g -%11); 30 günde artıda %16. En iyi öncü 'önceki gün >= +%11,5': "
               "test lift 5,4 (eğitim 4,9) ama mutlak olasılık %0,12 -> %0,64; sinyal gününde alım test 7 g medyan -%9,7 vs taban -%2,9. Literatür: yeni "
               "tokenlarda 2025 kuşağının ~%85'i TGE fiyatının altında; pump-and-dump katılımcıları çoğunlukla kaybeder. RITUAL: TGE 26 Eki 2026, float %18, "
               "doğrulanmış katalizör yok; +%99,88 24 saatlik kayan değişim. Sınır: Binance ana API (451) ve Bybit (403) erişilemedi; OKX / Gate delist "
               "edilenler yok (hayatta kalma yanlılığı); komisyon / kayma ve güven aralığı yok."),
    _ik_k("Ç148", "2026-11-09", "YEOTK PROFİLİ ('SIKI DOSYA') ÖN KAYITLI GEÇMİŞ TESTİ: bilanço günü güçlü tepki (F7, kayan üst %20 + ham >= +%5) + satış büyümesi (F1) + çeyrek ivmesi ve kâr sıçraması (F2) + sağlam bilanço (F3) + seyrelme yok (F4, ABD) + fon payı < %2 (F5, BIST) + tepeden %30-70 aşağıda ve 60 gün pazarın altında (F6); V0-V4, önceden yazılı 3 devam (F2 1,2 kat, 120 gün, iki ivmeli çeyrek)", "K57.py, test_k57.py", "Cemal (9 Kas 2026, tek ve son talimat): YEOTK gibi sıkı dosyalar BIST'te ve ABD'de eşlerini geçiyor mu?", "Yeni deneme (ön kayıt K57_ON_KAYIT.md, sha 2a6cc6f6d1fd; ölçüt FI_OLCUT; karar ABD 2023 + 2024-26, Avrupa verisi yok)", "", 3, cikti="arastirma_cikti/k57_yeotk_profili/ (K57_ON_KAYIT.md, K57_RAPOR.md, hucre.csv, olaylar_bist.csv, olaylar_abd.csv)", notu="İZ DEĞİL. Olay: BIST 9046 (V3 22), ABD 29678 (V3 kısmi 10). BIST V3 (bilgi) 2022-23: n 1, +%23,8 (+%23,8 .. +%23,8), sıra 0,82, tutmaz; 2024-26: n 20, -%5,9 (-%14,1 .. +%1,3), sıra 0,47, tutmaz. ABD V3 2021-22: n 2, -%11,0 (-%20,7 .. -%1,2), sıra 0,37, tutmaz; 2023: n 2, -%2,5 (-%2,5 .. -%2,5), sıra 0,55, tutmaz; 2024-26: n 5, -%17,3 (-%60,5 .. +%19,9), sıra 0,46, tutmaz. Tutan hücreler: yok. ABD TEMEL VERİSİ VAR; SEC durumu: tamam (9 Kas, Cemal'in e-posta izniyle; e-posta koda / repoya yazılmadı). Yorum: tam profil ABD evreninde (V_ABD 1.411 hayatta kalan) çok seyrek (n 2-5). Eşiğe en yakın: V1 (güçlü tepki + büyüme + ivme + sağlam bilanço, fiyat şartı YOK) ABD 2023 +%19,7 (n 7), ABD 2024-26 +%10,3 (n 31, aralık -%7,9..+%29,7, portföy %89,5), BIST 2024-26 +%6,3 (n 96, portföy %99); 'tepeden düşmüş' şartı (F6) eklenince fark eksiye dönüyor (V2 / V3). Basit okuma: iyi bilanço + güçlü tepki tek başına yaklaşıyor, dipte alma şartı bozuyor."),
    _ik_k("Ç149", "2026-11-09", "K57-B: YEOTK profili V1 (güçlü tepki + büyüme + ivme + sağlam bilanço, fiyat şartı yok) çevresinde önceden yazılı 3 devam: B1 geniş ABD evreni (SEC frames + Yahoo fiyat, 20 gün medyan işlem değeri >= 1 milyon $), B2 20 gün ufuk, B3 F3'süz", "K57.py, test_k57.py", "K57 eşiğe en yakın V1 geniş evrende / kısa ufukta / bilanço şartsız tutar mı?", "Devam (ön kayıt K57B_ON_KAYIT.md, sha abc73b49f1df; ölçüt FI_OLCUT; karar ABD 2023 + 2024-26, Avrupa verisi yok)", "", 3, cikti="arastirma_cikti/k57_yeotk_profili/ (K57B_ON_KAYIT.md, K57B_RAPOR.md, hucre_b.csv, olaylar_b1_abd.csv.gz, evren_b1.csv, k57b_kos_meta.json)", notu="İZ DEĞİL. B1 geniş ABD evreni [İZ DEĞİL]: ABD 2021-22: n 64, +%3,9 (-%1,7 .. +%8,5), sıra 0,56, portföy %83,0, tutmaz; ABD 2023: n 16, +%11,4 (-%5,0 .. +%28,8), sıra 0,59, portföy %91,0, tutmaz; ABD 2024-26: n 58, +%4,8 (-%10,2 .. +%18,7), sıra 0,57, portföy %72,5, tutmaz. B2 20 gün ufuk [İZ DEĞİL]: BIST 2022-23: n 8, +%3,8 (+%1,2 .. +%22,4), sıra 0,57, portföy %76,0, tutmaz; BIST 2024-26: n 96, +%2,5 (-%2,0 .. +%7,8), sıra 0,53, portföy %98,5, tutmaz; ABD 2021-22: n 29, +%1,8 (-%1,7 .. +%5,8), sıra 0,56, portföy %83,0, tutmaz; ABD 2023: n 7, +%20,0 (+%14,4 .. +%24,2), sıra 0,84, portföy %100,0, tutmaz; ABD 2024-26: n 34, +%4,3 (-%5,3 .. +%13,5), sıra 0,53, portföy %77,5, tutmaz. B3 F3'süz (F7+F1+F2) [İZ DEĞİL]: BIST 2022-23: n 8, +%14,0 (+%5,0 .. +%76,9), sıra 0,59, portföy %85,0, tutmaz; BIST 2024-26: n 99, +%5,4 (-%5,2 .. +%21,2), sıra 0,53, portföy %89,5, tutmaz; ABD 2021-22: n 48, +%3,8 (-%4,8 .. +%13,6), sıra 0,55, portföy %44,5, tutmaz; ABD 2023: n 11, +%8,8 (-%11,4 .. +%42,9), sıra 0,55, portföy %86,5, tutmaz; ABD 2024-26: n 46, +%14,9 (-%0,1 .. +%31,5), sıra 0,62, portföy %98,5, tutmaz. B1 evreni: 4475 aday, 4261 hisse fiyatlı (Yahoo durumları: fiyat 4261, kısa 117, veri yok 45, yok 33, inmedi 14, tür dışı 5), taban üstü olay 50161 (3126 hisse), V1 150."),
    _ik_k("Ç150", "2026-11-09", "K57-C: YEOTK profili V1 geniş ABD evreninde önceden yazılı son 3 deneme: C1 V1 + F4 (seyrelme yok), C2 likidite tabanı 5 milyon $, C3 F7 yerine yalnız 'ear' üst %10; hat kapanış önerisi", "K57.py, test_k57.py", "K57-B önceden yazılı C1-C3 iki ABD karar hücresinde tutar mı; YEOTK profili hattı kapanmalı mı?", "Devam (ön kayıt K57C_ON_KAYIT.md, sha b81b5fb148be; boşluklar ölçümden önce dolduruldu; ölçüt FI_OLCUT; karar ABD 2023 + 2024-26, Avrupa verisi yok; BIST uygulanmaz)", "", 3, cikti="arastirma_cikti/k57_yeotk_profili/ (K57C_ON_KAYIT.md, K57C_RAPOR.md, hucre_c.csv, olaylar_c_abd.csv.gz, k57c_kos_meta.json)", notu="İZ DEĞİL. C1 V1 + F4 (seyrelme yok) [İZ DEĞİL]: ABD 2021-22: n 26, +%4,4 (-%8,5 .. +%9,7), sıra 0,59, portföy %92,5, tutmaz; ABD 2023: n 10, +%5,9 (-%4,3 .. +%15,8), sıra 0,56, portföy %79,5, tutmaz; ABD 2024-26: n 41, -%0,1 (-%15,6 .. +%16,5), sıra 0,54, portföy %66,0, tutmaz. C2 likidite tabanı 5 milyon $ [İZ DEĞİL]: ABD 2021-22: n 46, +%2,5 (-%4,8 .. +%10,2), sıra 0,54, portföy %87,5, tutmaz; ABD 2023: n 9, +%17,6 (-%5,2 .. +%44,2), sıra 0,63, portföy %98,5, tutmaz; ABD 2024-26: n 47, +%8,9 (-%6,3 .. +%22,5), sıra 0,61, portföy %93,0, tutmaz. C3 F7 yerine 'ear' üst %10 [İZ DEĞİL]: ABD 2021-22: n 46, +%4,0 (+%0,7 .. +%7,0), sıra 0,57, portföy %84,5, tutmaz; ABD 2023: n 11, +%8,2 (-%3,9 .. +%21,9), sıra 0,63, portföy %86,5, tutmaz; ABD 2024-26: n 30, +%9,9 (-%4,4 .. +%25,3), sıra 0,61, portföy %96,5, tutmaz. Geniş evren 4261 hisse (yeni SEC / Yahoo isteği yok, önbellek), 1 milyon $ taban üstü olay 50161; B1 V1 yeniden üretimi tuttu (ABD 2021-22 n 64, ABD 2023 n 16, ABD 2024-26 n 58). Hat kapanışı: K57 + K57-B + K57-C 48 ABD karar hücresi, 0 tuttu, iki hücrede birden tutan deneme 0; kapanış önerildi (karar ana oturumda)."),
    _ik_k("Ç151", "2026-11-10", "K58 CETVEL SAĞLAMASI: FI_OLCUT gücü (plasebo olay + bilinen δ), French faktörleri pozitif kontrol, portföy cetveli (aylık üst %10) kalibrasyonu, SMA200 trend filtresi (endeks ve hisse)", "K58.py, test_k58.py", "İz bulamamamızın nedeni piyasa mı, ölçüm aletimiz mi?", "Ön kayıt K58_ON_KAYIT.md (sha 5aec67198fe9, git 657c2a1, ölçümden önce); FI_OLCUT değişmedi; portföy cetveli yalnız aday", "", 0, cikti="arastirma_cikti/k58_cetvel_sagla/ (K58_ON_KAYIT.md, K58_RAPOR.md, A_guc.csv, B_french.csv, C_portfoy.csv, C_plasebo.csv, C4a_endeks.csv)", notu="A güç (δ +%2, n 30/100/300/1000/3000): %4/%8/%11/%13/%21, δ 0 yanlış pozitif en çok %1,5; D1 BULGU: FI_OLCUT küçük etkiyi göremiyor; C portföy cetveli: ABD C1 momentum TUTAR, plasebo yanlış pozitif %0,0 (brüt %0,0); D2 KALİBRE ADAY STANDART (benimseme Cemal kararı); BIST C1 tutmaz; C4a SMA200 endeks filtresi: SPY TUTMAZ, XU100.IS TUTMAZ; C4b: ABD C4b1_sma200_ustu tutmaz, ABD C4b2_atilim tutmaz, BIST C4b1_sma200_ustu tutmaz, BIST C4b2_atilim tutmaz. İz iddiası yok (ölçüm aleti sağlaması); seviye 0."),
    _ik_k("Ç152", "2026-11-11", "K59 BASİT SİNYALLER: dokuz sürekli sinyal + önceden yazılı COMP4 bileşiği + DOSYA ailesi (YEOTK / DGXX mantığı) + UCUZLUK koşullu testi, aylık üst %10 portföy, portföy cetveli v2 (K58 C + beta düzeltmeli alfa), ABD iki evren + BIST bilgi", "K59.py, test_k59.py", "Basit, nedeni bilinen sürekli sinyaller ve sıra ortalaması bileşiği maliyetten sonra evreni geçiyor mu?", "Ön kayıt K59_ON_KAYIT.md (mühür 6fe8bb385667, ölçümden önce git kaydına işlendi); eşikler değişmedi", "", 0, cikti="arastirma_cikti/k59_basit_sinyaller/ (K59_ON_KAYIT.md, K59_RAPOR.md, sinyal_sonuc.csv, aylik_getiri.csv, plasebo.csv, kapsam.csv, ucuzluk.csv)", notu="Karar: TUTMAZ (U1 TUTMAZ, U2 TUTMAZ); cetvel v2 GÜVENİLİR (plasebo yanlış pozitif net %0,0, brüt %1,5); U1 COMP4 yıllık fazla -%1,6, NW t -0,49, t(alfa) 0,16, TUTMAZ; U2 COMP4 yıllık fazla +%5,5, NW t 2,30, t(alfa) 2,87, TUTMAZ. DOSYA ailesi: U1 DOSYA_Y TUTMAZ; U2 DOSYA_Y TUTMAZ; U1 DOSYA_D TUTMAZ; U2 DOSYA_D TUTMAZ; U1 DOSYA_YD TUTMAZ; U2 DOSYA_YD TUTMAZ. İZ ilan edilemez (standart değişikliği Cemal'in kararı); seviye 0."),
    _ik_k("Ç153", "2026-11-11", "K59-B: K59 §6daki önceden yazılı üç deneme: (a) yalnız küçük-orta hisseler, (b) 3 ay tutma + örtüşen üç kohort, (c) French kütüphanesinde momentum + kârlılık harmanı; COMP4, DOSYA_Y, S5, S1; cetvel v2 aynı", "K59.py, test_k59.py", "K59da tutmayan bileşik küçük-orta hisselerde ya da 3 ay tutmayla tutuyor mu; uzun tarihte (French) bu tür bileşik var mı?", "Ön kayıt K59B_ON_KAYIT.md (mühür 54591b5ffdcd; K59 mührü 6fe8bb385667 değişmedi; ölçümden önce git kaydına işlendi)", "", 0, cikti="arastirma_cikti/k59_basit_sinyaller/ (K59B_ON_KAYIT.md, K59B_RAPOR.md, k59b_sonuc.csv, k59b_aylik.csv, k59b_plasebo.csv, k59b_kapsam.csv, k59b_french.csv, k59b_french_aylik.csv)", notu="Karar: TUTMAZ; cetvel (a) GÜVENİLİR, (b) GÜVENİLMEZ; (a) U1 COMP4 yıllık fazla -%2,5, NW t -0,55, t(alfa) 0,09, TUTMAZ; (a) U2 COMP4 yıllık fazla +%7,0, NW t 2,39, t(alfa) 3,09, TUTAR (yineleme); (b) U1 COMP4 yıllık fazla -%1,2, NW t -0,37, t(alfa) 0,12, HÜKÜM YOK; (b) U2 COMP4 yıllık fazla +%5,8, NW t 2,50, t(alfa) 2,88, HÜKÜM YOK. French (c): VW_MKT: bileşik uzun dönemde tutmuyor (1963-son: TUTAR, 2000-son: TUTMAZ); 2020 sonrası güçlü; EW_EW10: bileşik uzun dönemde tutmuyor (1963-son: TUTMAZ, 2000-son: TUTMAZ); 2020 sonrası zayıf. İZ ilan edilemez; seviye 0. Sonraki: K60 (uzun tarih, batanlar dahil evren, sinyal kütüphanesinin tamamı); bu dokuz sinyalin 2021-26 örnekleminde başka çeşitlemesi denenmez."),
    _ik_k("Ç154", "2026-11-11", "K60: sinyal kütüphanesi (77 sinyal + 12 bileşik, 13 aile) x iki cetvel (R1 portföy cetveli v2; R2 OLASILIK TABLOSU: 12 ayda +%100 ve -%50 olasılık katları) x üç dönem (KEŞİF 2012-21, DOĞRULAMA 2022-23, KASA 2024-26 tek açılış); BH %10 + 200 plasebo; EK: asimetri ölçütü (ASIM = +%100 katı / -%50 katı)", "K60.py, test_k60.py, arastirma_cikti/k60_kutuphane/k60_ek.py", "Hangi ölçülebilir özellik bir hissenin 12 ayda ikiye katlanma olasılığını taban orana göre kaç kat artırıyor, yarıya inme olasılığını kaç kat artırıyor; hangisi piyasayı geçen portföy veriyor; üç dönemde tutuyor mu?", "Ön kayıt K60_ON_KAYIT.md (mühür e1749249eeb8; git f740ed4 12:13, KEŞİF 12:14); secili.json git fad6b11 12:16 (DOĞRULAMA 12:16:19); dogrulama_gecen.json + K60_EK_ON_KAYIT.md git 317bb85 12:18:59 (KASA açılış 12:19:40)", "", 0, cikti="arastirma_cikti/k60_kutuphane/ (K60_ON_KAYIT.md, K60_EK_ON_KAYIT.md, K60_RAPOR.md, olasilik_tablosu.md, K60_EK_RAPOR.md, secili.json, dogrulama_gecen.json, kasa_acildi.json, *_meta.json; csv çıktılar git dışı)", notu="Karar: İZ ADAYI YOK; ASİMETRİK FIRSAT YOK; iki kalıcı bulgu var. Evren: 4.666 ABD hissesi (yalnız yaşayanlar), uygun evren ort. 1.642 / 2.274 / 2.516. TABAN ORAN (12 ay): +%100 olasılığı %4,1 / %3,7 / %6,8; -%50 olasılığı %5,8 / %7,0 / %7,3 (KEŞİF / DOĞRULAMA / KASA). R1: KEŞİF'te 88 hipotezden 2 seçildi (NEF ÜST t(alfa) 4,51; REV_SURP ÜST 3,08); DOĞRULAMA'da REV_SURP düştü (-%2,1), NEF tuttu (+%4,9, t 2,81); KASA'da NEF düştü (-%4,3 / yıl, t -0,06). K60-İZ ADAYI = 0. COMP4 ÜST net fazla +%1,9 / +%5,8 / +%0,3; DOSYA_Y ÜST +%1,8 / +%4,0 / +%2,3; SP ÜST +%8,2 / +%8,3 / +%1,6 (KASA alfa eksi). R2: 167 hipotezin 106'sı seçildi, 109 çift DOĞRULAMA'dan, 97'si KASA'dan geçti; ama bu OYNAKLIK etkisi (uç onluk oynak hisse toplar, iki kuyruk birlikte şişer; ln katlar arası korelasyon 0,89): 'K60-OLASILIK İZİ' 86 ve 'K60-KAÇINMA İZİ' 86 etiketi karar bilgisi DEĞİL. EK (KASA'dan önce yazıldı): 'ASİMETRİK FIRSAT' (kazanma katı batma katından büyük, üç dönem) 0 çift; en yakın SP ÜST (+%100 katı 2,17 / 1,71, -%50 katı 1,04 / 0,91) KASA'da bozuldu (1,18'e karşı 1,29); YAKIN: BETA_BAB ALT (yüksek beta: 2,41 / 2,39 / 2,71'e karşı 1,89 / 1,80 / 2,24), NDF_BS ALT. 'GÜVENLİ UÇ' 2 çift: COMP4 ÜST (-%50 katı 0,43 / 0,25 / 0,47; +%100 katı 0,70 / 1,02 / 0,74) ve DOSYA_Y ÜST (-%50 katı 0,62 / 0,54 / 0,61; +%100 katı 0,95 / 1,08 / 0,98; medyan evrenin üstünde). 'PİYANGO UCU (kaçın)' 59 çift, üç dönemde aynı: yüksek oynaklık, düşük fiyat, zirveden uzak, zarar eden, nakdi kısa, küçük, geniş alım-satım farkı, raf / hisse ihracı, ters bölünme: +%100 katı 2,0-2,7 ama -%50 katı 2,8-3,8 ve medyan 12 ay getirisi eksi (DOĞRULAMA -%13..-%20, KASA -%4..-%12); ters bölünme -%50 katı 4,3 / 3,9 / 5,5. Birleşik model (10 aile, lojistik) üst %10: +%100 olasılığı %10,4 / %9,7 / %14,9 (kat 2,5 / 2,6 / 2,2) ama -%50 olasılığı %16,4 / %22,3 / %23,3 (kat 2,9 / 3,2 / 3,2), medyan +%1,2 / -%12,7 / -%8,4: 'kazananı' değil 'oynağı' seçiyor. Denetim: mühür ve kod sha üç koşuda aynı, sıra git zamanlarıyla doğrulandı, 11 hücre aylık dosyalardan bağımsız yeniden üretildi ve tuttu, ek hesabı r2.csv ile birebir. Sınır: yalnız yaşayanlar (batma olasılıkları alt sınır), KASA R2 20 oluşum ayı. Sonraki (önceden yazıldı): K60-B piyango havuzu İÇİNDE koşullu ayrım; K61 dalga 2 (Form 4, açığa satış, 8-K 1.01); batanları içeren veri."),
    _ik_k("Ç155", "2026-11-11", "K60-B: piyango havuzu (her ay 60 günlük oynaklığı en yüksek %20) İÇİNDE koşullu ayrım; 77 sinyal + 12 bileşik, havuz içi ÜST / ALT %20; kat = uç olasılığı / havuz olasılığı; ASIM; 200 havuz içi plasebo", "K60B.py, test_k60b.py", "Oynak hisseler arasında hangi özellik ikiye katlananı yarıya inenden ayırıyor (kazanma olasılığını artırıp batmayı artırmıyor ya da batmayı azaltıyor)?", "Ön kayıt K60B_ON_KAYIT.md (sha256 b74f3e2d2656; git 5aac5de 12:25:59, koşu 12:35:25); K60 mührü ve K60.py değişmedi", "", 0, cikti="arastirma_cikti/k60_kutuphane/ (K60B_ON_KAYIT.md, K60B_RAPOR.md, k60b_meta.json; csv çıktılar git dışı)", notu="Karar: BİLGİ düzeyinde 2 KOŞULLU FIRSAT + 8 KOŞULLU KORUMA etiketi (üç dönem); İZ değil (yalnız ABD, yalnız yaşayanlar, KASA ikinci kullanım). HAVUZ TABANI (12 ay; KEŞİF / DOĞRULAMA / KASA): +%100 olasılığı %10,1 / %8,5 / %15,8; -%50 olasılığı %16,9 / %21,4 / %19,8; medyan -%0,5 / -%13,5 / -%3,9 (evren +%9,5 / +%4,6 / +%5,1). KORUMA (havuz içinde yarıya inme olasılığını düşürüp ikiye katlanmayı düşürmeyenler; -%50 katı üç dönem): COMP4 ÜST 0,57 / 0,63 / 0,67 (+%100 katı 0,93 / 0,96 / 0,97); DOSYA_Y ÜST 0,65 / 0,81 / 0,73 (+%100 katı 0,93 / 1,09 / 1,06); ROA_Q ÜST (kârlı) 0,71 / 0,71 / 0,69; TAX_CHG ÜST 0,75 / 0,63 / 0,68; AMIHUD ALT (likit) 0,76 / 0,69 / 0,59; NDF_BS ALT 0,72 / 0,79 / 0,72; MOM_FIP ÜST, ISKEW ÜST (zayıf, 0,84-0,93). FIRSAT: BETA_BAB ALT (havuz içi yüksek beta: +%100 katı 1,34 / 1,45 / 1,36; -%50 katı 0,91 / 0,73 / 0,98; aylık portföy havuzu +%5 / +%16 / +%16 geçti; 2024-25 yükseliş etkisi olabilir) ve NDF_BS ALT (+%100 katı 1,42 / 1,21 / 1,24; NDF_BS'nin iki ucu da benzer: yön değil KAPSAM etkisi: havuzda bu kalemi bildiren hisse %35-39, 'bildiren / havuz' -%50 katı 0,72 / 0,79 / 0,82; uç / bildiren ASIM 1,12 / 1,03 / 1,40: etiketin çoğu sıralama değil). TAX_CHG ÜST KEŞİF'te de kapsam etkisi (uç / bildiren 1,00), sonraki iki dönemde gerçek (0,70 / 0,84). Kapsamı temiz olanlar: BETA_BAB ALT, COMP4 ÜST, ROA_Q ÜST, AMIHUD ALT; DOSYA_Y ÜST uç / bildiren -%50 katı 0,74 / 0,86 / 0,80. Havuz içinde oynaklık hâlâ ayırıyor (en az oynak beşte bir -%50 katı 0,66 / 0,68 / 0,65): KORUMA etiketlerinin bir kısmı 'havuzun sakin tarafı' ile örtüşebilir, ayrıştırılmadı. KIRMIZI BAYRAKLAR (havuz içinde -%50 katı; etiket kuralı dışında, üç dönemde aynı yön): ters bölünme 1,42 / 1,98 / 2,39 (yarıya inme olasılığı %46 / %37 / %47; +%100 katı 0,76 / 0,82 / 0,59); zarar eden (ROA_Q ALT) 1,51 / 1,51 / 1,59; raf kaydı (E_S3) 1,43 / 1,42 / 1,34; raftan satış (E_424B5) 1,43 / 1,43 / 1,61; nakit yakan (RUNWAY ALT) 1,42 / 1,37 / 1,56; hisse ihraç eden (NSI_1Y ALT) 1,39 / 1,24 / 1,37; zirveden en uzak (HIGH52 ALT) 1,45 / 1,36 / 1,41; en küçük (SIZE_ME ÜST) 1,45 / 1,30 / 1,68; en düşük fiyat 1,38 / 1,40 / 1,24. Bunlarda +%100 katı 1,0-1,3: batma riski artıyor, kazanma şansı belirgin artmıyor. K60'ta asimetrik görünen SP ÜST havuz içinde de KASA'da bozuldu (ASIM 2,05 / 1,71 / 0,90); NEF, NSI_1Y, HIGH52 ÜST koruması KASA'da ikiye katlanmayı da kıstı (+%100 katı 0,73-0,84). Plasebo: tek dönemde şart sağlama KEŞİF %2,5-3, DOĞRULAMA %9,5-12, KASA %5,5-10,5 (kısa dönemlerde aralık dar; etiketler üç dönem şartına dayanıyor). Denetim: ön kayıt sha ve git zamanı koşudan önce, 5 hücre aylık sayımlardan bağımsız yeniden üretildi ve tuttu, testler geçti. Sonraki (önceden yazıldı): K60-C kırmızı bayrak sayısına göre olasılık tablosu (tanımlayıcı); K61 dalga 2 (Form 4, açığa satış, 8-K 1.01 sözleşme); batanları içeren veri."),
    _ik_k("Ç156", "2026-11-12", "K64 + K65: çöl sinyaline (K24, değişmeden) EK BİLGİ: 52 hafta zirvesi ailesi (Z52 zirveye uzaklık, D52 dipten uzaklık, HIZ zirveye yaklaşma, DUSUS çöl öncesi düşüş) ve şirket kalitesi ailesi (GP brüt kârlılık, OP faaliyet kârlılığı, FCF serbest nakit, BORC borçluluk, SATIS_B satış büyümesi, KAR_B kâr büyümesi, PAY_D hisse sayısı değişimi); çöl olayları içinde üst / alt üçte bir, FI_OLCUT eşli fark", "K64.py, test_k64.py", "Cemal: 'aynı fiyat şekillerini ölçmek yerine çöl sonrası getiriyi açıklayan dış bilgileri araştır; çöl tanımı ve cetvel değişmesin'", "Ön kayıt K64_K65_ON_KAYIT.md (mühür a4c6da913a10; git 3155208 18:28:07, koşu 18:28:35); karar sırası K64 ailesinde çöl içi, K65'te evren içi (kapsam sayılarına bakılarak, getiri görülmeden)", "", 0, cikti="arastirma_cikti/col_dis_bilgi/ (K64_K65_ON_KAYIT.md, K64_K65_RAPOR.md, k64_meta.json; csv git dışı)", notu="Karar: 22 değişken-yönün hepsi İZ DEĞİL (BIST PAY_D ölçülemez); BH'den geçen yok (m = 84). TEMEL (yalnız çöl) eşli fark 60 gün, 2017-21 / 2022-26 / 2023-26: ABD -%2,6 / +%0,2 / +%0,4, BIST +%2,0 / -%1,6 / -%1,0 (hiçbiri tutmaz; medyan eşli fark hep -%4..-%7). ÜST - ALT (ABD): GP +4,0 / -8,3 [-14,3; -2,2] / -9,3; OP -2,3 / -4,6 / -7,4; FCF +2,2 / -5,3 / -7,4: 2022-26'da KALİTESİZ çöl daha iyi, 2017-21'de yok (rejim; K60 piyango bulgusuyla uyumlu). D52 -1,6 / +5,0 [1,0; 9,0] / +6,7; PAY_D (çok hisse basan) +2,5 / +3,3 / +4,7; BORC (borçlu) +4,9 / +3,1 / +3,2 ve BIST +1,2 / +5,0 / +4,7: işaret her yerde aynı ama aralıklar sıfırı içeriyor. BIST en yakın: SATIS_B (satışı büyüyen) +6,6 [0,5; 12,6] / +4,0 / +4,8 (ikinci dönem aralık sıfırı içeriyor). Zirveye yakın çöl (George-Hwang) ABD'de daha İYİ DEĞİL (-2,6 / -2,6 / -4,9). Denetim: 4 hücre olay dosyasından bağımsız yeniden üretildi ve tuttu; mühür ve kod sha aynı; koşu commit'ten sonra. Sınır: yalnız yaşayanlar (kalitesiz grubun batanları yok: kalitesiz-çöl üstünlüğü yukarı yanlı), K58 gücü (+%2 etkiyi n=300'de %11)."),
    _ik_k("Ç157", "2026-11-12", "K63: veri erişim araştırması: analist revizyonu, emir akışı, hisse ödünç verme (BIST ve ABD)", "arastirma_cikti/col_dis_bilgi/K63_VERI_ERISIM.md", "Cemal: analist revizyonları, emir akışı (OFI) ve ödünç ücreti için tarihsel veri var mı, maliyeti ne?", "Web + ücretsiz uçların gerçek denenmesi; örnekler /tmp/k63_ornek", "", 0, cikti="arastirma_cikti/col_dis_bilgi/K63_VERI_ERISIM.md", notu="ABD: açık pozisyon (FINRA, 2017-12+, ücretsiz) ve günlük açığa satış hacmi (Reg SHO 2009-08+) VAR; analist EPS konsensüs görüntüsü Alpha Vantage 2017-06+ (ücretsiz 25 istek / gün ya da 49,99 $ bir ay; görüntü günü belirsiz); Yahoo not günlüğü 2011+ (K52'de var); ödünç ücreti / kullanılabilir adet ücretsiz YOK (IBorrowDesk 29 $/ay, 2015+); emir defteri yalnız IEX (tek borsa, 2017+, TB boyutu) ya da hesaplı Alpaca. BIST: analist tarihsel VERİ YOK (İş Yatırım yalnız 54 hisse, güncel); emir defteri VERİ YOK (DataStore fiyatı doğrulanamadı); açığa satış 2020'den beri yalnız 30-50 hissede (çöl evreni için kullanılamaz); Takasbank ödünç pay bülteni 2008+ ücretsiz (günde 35-90 kıymet). OFI / derinlik / iptal ölçüleri BIST'te bugün hesaplanamaz."),
    _ik_k("Ç158", "2026-11-12", "K62: BIST PEAD birebir tekrar (Ahlatcıoğlu & Okay 2021, Borsa Istanbul Review 21(1); doi 10.1016/j.bir.2020.09.001): SUETF (geçmiş kazanca göre sürpriz), EAR (açıklama günü getirisi), SUEAF (analist; VERİ YOK); çeyrek içi tertil, CAR[2,61] 2x3 büyüklük-DD/PD portföyüne göre; dönemler 2017-21 / 2022-26 / 2023-26; ayrıca FI_OLCUT (geleceğe bakmayan tertil, giriş t+2 açılış)", "K62.py, test_k62.py", "Cemal: 'BIST PEAD makalesini birebir yeniden üret, %2,9 / %2,9 / %2,2 farklarını yakala, sonra dönemlere ve K28'e karşı'", "Ön kayıt K62_ON_KAYIT.md (mühür 7dbda78a5d6f; git 0ea9023 04:14:19, koşu 04:14:36); KAP 2009-06'dan, İş Yatırım fiyat ve mali tablo (kotasyondan çıkanlar dahil)", "", 0, cikti="arastirma_cikti/col_dis_bilgi/ (K62_ON_KAYIT.md, K62_RAPOR.md, k62_meta.json, k62_kapsam.json; csv git dışı)", notu="Karar: MAKALE YENİDEN ÜRETİLDİ; PEAD BIST'te 2022-26'da büyüdü; alınabilir uzun bacak proje cetvelinde TUTMADI (İZ DEĞİL; BIST zaten bilgi). A (2009Ç2-2018Ç4, 5.430 olay, makale 6.471): PEAD[2,61] SUETF %4,05 [2,65; 5,39] t 5,99 (makale %2,94), EAR %2,82 [1,76; 3,84] (makale %2,18); [2,21] %1,25 / %1,43 (makale %1,18 / %0,76); kontrollü regresyon %3,93 / %2,70 (makale %2,78 / %2,26); SUEAF VERİ YOK (BIST'te ücretsiz tarihsel analist tahmini yok; Investing / Fintables 403, Rasyonet / Bloomberg / I/B/E/S kurumsal). B: 2017-21 SUETF %3,45 (TUTAR; kazancın tamamı kötü sürpriz bacağı: Q1 -%3,35, Q3 +%0,10), EAR %1,28 (TUTMAZ); 2022-26 SUETF %7,85 (TMS 29 temiz çeyrekler; Q3 +%4,04, Q1 -%3,81), EAR %6,48 (Q3 +%3,60); 2023-26 %8,29 / %6,50; 18 sınamanın 14'ü BH'den geçti; maliyet sonrası (4 x 30 bp) 2022-26 %6,7 / %5,3. C (FI_OLCUT, yalnız bugün yaşayan V_BIST, giriş t+2 açılışı): iyi sürpriz (Q3) SUETF eşli fark BIST 2023 +%3,6 [-2,7; 9,1], 2024-26 +%2,85 [0,86; 4,40] sıra 0,56 ama slot portföyü rastgelenin %90'ını geçmedi; EAR Q3 +%4,3 / +%1,7 (aralık sıfırı içeriyor); kötü sürpriz (Q1) SUETF -%5,4 / -%1,0, EAR -%2,9 [-5,9; -0,9] / -%2,8 [-5,1; -0,7] (kaçınma yönü tutarlı, dört şart portföyde düştü). K28 ile fark: K28 tepkiye göre üst / alt %20, boyut süzgeci yok, giriş tepki sonrası; K62 SUETF (kazanç büyümesi / piyasa değeri) ve > 100 mn $ süzgeci; iki çalışma aynı yönde: kötü sürpriz BIST'te sonraki 60 günde eşlerinin 3-5 puan gerisinde. SAPMA: 2007Ç1-2009Ç1 yok (KAP 2009-06'da başlıyor), İş Yatırım yıllık değerleri yeniden sunulmuş (TMS 29; 2022Ç4 sonrası 7 çeyrek SUETF'te kirli sayıldı), IO yok. Denetim: 3 hücre (A SUETF / EAR, B 2022-26 EAR) olay dosyasından bağımsız yeniden üretildi ve tuttu; test 13/13."),
    _ik_k("Ç159", "2026-11-12", "K66: ABD açığa satış talebi (FINRA iki haftalık açık pozisyon, 2017-12+) çöl sinyaline ek bilgi: SI_PAY (açık pozisyon / pay), DTC (kapatma günü), SI_DEG (3 ay değişim), SI_DEG1 (son rapor değişimi); çöl içi üst / alt üçte bir; bilgi tarihi ödeme günü + 12 işlem günü", "K66.py, test_k66.py", "Cemal: 'hisse ödünç verme ve açığa satış talebi çöl sonrası getiriyi açıklıyor mu'", "Ön kayıt K66_ON_KAYIT.md (mühür 1d820a4e2638; git 89fb9f6 04:42:43, koşu 04:43:01); karar sırası çöl içi (kapsamda çöller yüksek açığa satışta toplanıyor; getiri görülmeden)", "", 0, cikti="arastirma_cikti/col_dis_bilgi/ (K66_ON_KAYIT.md, K66_RAPOR.md, k66_meta.json; csv git dışı)", notu="Karar: 8 değişken-yönün hepsi İZ DEĞİL; hiçbir dönemde ek katkı yok, BH'den geçen yok (m = 16). ÜST - ALT (çöl içi; 2018-21 / 2022-26 / 2023-26): SI_PAY +1,6 / +2,7 [-1,1; 6,4] / +2,9; DTC -2,7 / -0,2 / -0,5; çöl dışı evrende açığa satış oranı ayırmıyor (-0,1 / -0,5 / -0,2) ama KAPATMA GÜNÜ (DTC) ayırıyor: yüksek DTC 60 günde eşlerinin -2,5 [-3,7; -1,4] / -1,6 [-2,5; -0,6] / -1,5 gerisinde (iki bağımsız dönemde anlamlı; çöl içinde aynı yön, ek bilgi yok; bilgi). Temel çöl eşli fark -%2,9 / +%0,2 / +%0,4. Akademik beklenti (yüksek açığa satış = kötü) bu evrende ve ufukta görülmedi. Ödünç ücreti / kullanılabilir adet: VERİ YOK (IBorrowDesk 29 $/ay; karar Cemal'de). BIST: açığa satış 2020'den beri yalnız 30-50 hissede, VERİ YOK. Denetim: 4 hücre olay dosyasından bağımsız yeniden üretildi ve tuttu; test 12/12; koşu commit'ten sonra."),
    _ik_k("Ç160", "2026-11-12", "K62-B: bilanço sürprizi (çöl günü bilinen son açıklamanın SUETF ve EAR'ı, en çok 90 gün önce) çöl sinyaline ek bilgi; BIST + ABD; K64 tasarımı; bilgi grubu ÇÖL + SÜRPRİZ (iki ölçü de üst üçte bir)", "K62B.py, test_k62b.py", "Cemal: 'çöl sonrası getiriyi açıklayan dış bilgi: PEAD makalesinin ölçüleri çöle ek katkı veriyor mu'", "Ön kayıt K62B_ON_KAYIT.md (mühür 2686fef68b91; git fdb6be8 04:45:50, koşu 04:46:06); karar sırası SUETF evren, EAR çöl içi (kapsama göre, getiri görülmeden)", "", 0, cikti="arastirma_cikti/col_dis_bilgi/ (K62B_ON_KAYIT.md, K62B_RAPOR.md, k62b_meta.json; csv git dışı)", notu="Karar: 4 değişken-yönün hepsi İZ DEĞİL (BH m = 16, geçen yok). Çöl içi ÜST - ALT 60 gün (2017-21 / 2022-26 / 2023-26): SUETF BIST +1,8 / +2,4 / +4,1, ABD +4,5 [-0,7; 9,2] / +1,4 / +0,4; EAR BIST -1,1 / +3,9 [-0,2; 9,0] / +4,4, ABD işaret değişiyor. EN DİKKAT ÇEKİCİ (bilgi): BIST'te kötü bilanço tepkisinden (EAR alt üçte bir) sonra gelen çöl 2022-26'da eşlerinin -%5,8 [-9,5; -2,7], 2023-26'da -%5,6 [-9,0; -2,7] gerisinde (2017-21'de +%2,6: tutarsız); son 90 günde bilançosu olmayan BIST çölü -%5,4 / -%5,0. ÇÖL + SÜRPRİZ (iki ölçü de üstte) BIST +%4,2 / -%0,2 / +%2,1, ABD -%2,5 / +%0,2: K28'in 'çöl + iyi sürpriz' artısı (+%0,8 / +%2,6 / +%5,4 / +%5,6) bu tanımla yinelenmedi. Çöl DIŞINDA SUETF BIST 2022-26 +%4,1 [2,6; 5,7] (K62 ile uyumlu): bilanço sürprizi BIST'te genel olarak çalışıyor ama çöl olayına EK bilgi vermiyor. Denetim: 2 hücre olay dosyasından bağımsız yeniden üretildi ve tuttu; test 12/12."),
    _ik_k("Ç161", "2026-11-12", "K67: bilanço sonrası analist revizyonları (Yahoo not günlüğü: hedef fiyat ve tavsiye değişimleri, 2011-12+, 262.976 kayıt, 1.400 ABD hissesi): N_UP, N_DOWN, NET, BUYUKLUK (hedef değişim medyanı), AYRISMA, YON_UYUM (revizyon x sürpriz); açıklamadan sonraki 5 işlem günü, giriş 6. gün açılışı; bilanço olaylarında (S1, sürpriz katmanlı) ve çöl içinde (S2)", "K67.py, test_k67.py", "Cemal: 'bilanço sonrası analist EPS ve hedef fiyat revizyonlarını ölç; veri yoksa hangi sağlayıcıda hangi alan eksik yaz'", "Ön kayıt K67_ON_KAYIT.md (mühür 377b4fffeb71; git 14e63c0 06:05:13, koşu 06:05:28); 60 gün tekilleştirme Cemal'in protokolü gereği", "", 0, cikti="arastirma_cikti/col_dis_bilgi/ (K67_ON_KAYIT.md, K67_RAPOR.md, k67_meta.json, k67_kapsam_ozet.json; Yahoo önbelleği git dışı)", notu="Karar: 16 değişken-yönün hepsi İZ DEĞİL; BH'den geçen yok (m = 32). 35.698 bilanço olayı (2017-21 15.840, 2022-26 18.174). Fark büyüklükleri küçük: 60 günlük eşli fark ÜST / ALT grupları -%2,3 .. +%1,1 arasında; NET 2022-26 ÜST -0,7 / ALT -1,5; N_DOWN (çok kurum hedef düşürdü) 2022-26 -1,2 [-2,2; -0,1] ama 2017-21'de ayrışmıyor. Revizyonun sürprizle aynı / ters olması fark yaratmıyor (AO -0,7, TO -1,1, TU +0,7, AU -1,5; aralıklar sıfırı içeriyor). Çöl içinde NET ayırmıyor. VERİ: hedef fiyat / tavsiye VAR (Yahoo, ücretsiz, 2012+ hedef dolu %62-98); EPS tahmin revizyonu VERİ YOK (Alpha Vantage 49,99 $ / ay ya da EODHD 59,99 $ / ay, 2017-06+ çeyreklik görüntü; analist bazında I/B/E/S kurumsal); gelir tahmini revizyonu YOK; analist kişi kimliği YOK (yalnız kurum); BIST ve Avrupa VERİ YOK. Yanlılık: Yahoo kaydı bugünkü görüntü, yaşayan evren. Denetim: 3 hücre olay dosyasından bağımsız yeniden üretildi ve tuttu; test 17/17."),
    _ik_k("Ç162", "2026-11-12", "VDYT (Volatilite Denge ve Yön Tahmini; ayrı motor, Çöl Yolu değişmedi): 5 sıkışma tanımı (ATR oranı, RV yüzdeliği, BB genişliği, dar bant, bileşik) + duyarlılık; süre / hazard, Motor 1 (5 / 10 / 20 günde genişleme), Motor 2 (genişlerse yön), olay pencereleri, savunma hattı H1-H5, karşılaştırma grupları K1-K6; BIST (V_BIST 2015+), ABD (4.678 hisse 2010+), BIST_K62 (kotasyondan çıkanlar dahil, kapanış); walk-forward 2019-23 + KASA 2024-26/08 tek açılış", "VDYT.py, test_vdyt.py", "Cemal: 'uzun sıkışma ne zaman ve hangi yöne biter; süre, kendi geçmişi, haber, bilanço, savunma hattı birlikte basit piyasa kontrollerinden iyi tahmin ediyor mu'", "Ön kayıt VDYT_ON_KAYIT.md (mühür b999ffc73273; git b8737af 06:31; SAPMA 17 kod hatası düzeltmesi sonuç görülmeden 06aa1b5 07:02); KASA 07:22:20 UTC", "", 0, cikti="arastirma_cikti/vdyt/ (VDYT_ON_KAYIT.md, VDYT_VERI_ENVANTERI.md, VDYT_EKSIKLER.md, VDYT_KAPSAM.md, VDYT_RAPOR.md, VDYT_RAPOR_WF.md, VDYT_HATA_VE_EKSIK.md, vdyt_sonuc_*.json; grafik/ ve tablolar git dışı)", notu="Karar (ön kayıtlı 4 ana hücre): Motor 1 genişleme BIST ve ABD BASİTTEN İYİ (Brier skill WF / KASA: BIST +0,122 / +0,083, ABD +0,087 / +0,075; alt sınırlar > 0); Motor 2 yön ABD BASİTTEN İYİ (+0,147 / +0,112), BIST DEĞİL (WF alt sınır < 0). AMA: (1) Motor 1 üstünlüğü sıkışmaya özgü DEĞİL: sıkışma şartı olmayan rastgele bölgelerde (P2) aynı skill (ABD +0,08..+0,11, BIST +0,12..+0,15); kaynak bilanço takvimi (ABD OLAY katkısı +0,04) ve genişlemenin zaten başlamış olması (VOL; 3 günlük aralık penceresi çoğu kez karar gününde açık): büyük ölçüde mekanik. (2) SÜRE bilgisi işe yaramıyor: sıkışma uzadıkça bitme olasılığı ARTMIYOR, AZALIYOR (hazard yaş 10-19 / 20-39 / 60-89: ABD 0,045 / 0,038 / 0,021, BIST 0,076 / 0,060 / 0,054); yalnız süre / hisse geçmişi / rejim modelleri ABD'de basit tablodan iyi değil (KASA -0,012..+0,003), BIST'te küçük (+0,02..+0,03). (3) Bilanço günü sıkışmayı gerçekten bitiriyor: ABD bilanço sonrası 1-5 gün içinde aynı yaştaki habersiz sıkışmalara göre bitiş olasılığı +25 puan (WF) / +33 puan (KASA), yaklaşık 3 kat; bilanço öncesi 20-11 gün genişleme daha seyrek. (4) Yön: savunma hattı korunmuşsa yukarı kırılma payı +10..+22 puan (BIST, KASA'da tuttu; ABD T2-T5 +5..+9), ama süre ve olay modeldeyken hattın bağımsız katkısı yok (H5); yön tahmininin çoğu fiyatın bölge içindeki konumundan (yakın kenar önce kırılır). (5) Para etmiyor: genişleme + yön portföyü (bilgi, maliyet sonrası) ABD WF 249 işlem -%33, KASA +%0,6; BIST WF +%12, KASA +%2. (6) Olay testlerinde plasebo yanlış pozitif yüksek (rastgele olay günlerinde tekrarların %43-65'inde en az bir 'keşif'): bilanço dışındaki olay bulguları güvenilmez. K62 (batanlar dahil) aynı yön. Doğrulanmış alım sinyali DEĞİL. Denetim: ana 4 hücre tahmin dosyalarından bağımsız yeniden hesaplandı ve tuttu; test 14/14; KASA tek açılış. Veri eksikleri: BIST KAP özel durum, ABD 8-K içeriği, CPI / istihdam / TÜİK, sektör haberi, batan ABD şirket fiyatı. DÜZELTME (14 Kas, Ç175 denetimi): Motor 1 'basitten iyi' mekanik (hedef penceresi karar gününü içerir), Motor 2 yön bölge içi konumdan: ABD İZ DEĞİL, BIST ÖLÇÜLEMEDİ."),
    _ik_k("Ç163", "2026-11-12", "VDYT2 (v2_20261112; Cemal'in tek ve değişmez hedefi): küçük mum sessiz bölgesi G5 = küçük mum + dar bant + (yaklaşan tepe-dip ya da savunulan destek), sert düşüş ön koşulu P1 (120 günde <= -%30), geçerli karar günü (büyük hareket başlamadan), büyük hareket = t'den sonraki ilk onaylı büyük mum; üç başarı ayrı: (1) bölgeyi önceden bulmak, (2) genişlemeyi önceden tahmin, (3) yönü önceden tahmin; kontroller: sıkışma dışı aynı oynaklık ondalığı ve rastgele bölge; BIST + ABD, WF 2019-23 + KASA 2024-26/08", "VDYT2.py, test_vdyt2.py", "Cemal: 'sessiz bölgeyi büyük hareketten önce bul; ne zaman, hangi yöne; üç başarı ayrı ayrı kanıtlansın, biri başarısızsa başarılı sunulmasın'", "Ön kayıt VDYT2_ON_KAYIT.md (mühür 3051e5b8ddd9; git f13b96e 09:51:05, koşu 09:51:29); KASA 10:19 UTC tek açılış", "", 0, cikti="arastirma_cikti/vdyt/v2_20261112/ (ön kayıt, raporlar, sonuç json, grafik paketi; canlı tablo git dışı, Drive'da)", notu="(1) BÖLGEYİ BULMAK: BAŞARILI (BIST ve ABD; WF ve KASA). Sert düşüş sonrası küçük mum bölgesinde 20 günde büyük hareket olasılığı BIST %49-52 / ABD %34-43; aynı oynaklıktaki sıkışma dışı günlerde %35-39 / %27-35 (1,24-1,32 kat), rastgele bölgelerde %22-31 (1,6-1,75 kat). AMA: duyarlılık çok düşük (bütün büyük hareketlerin yalnız %0,8-2,4'ü önceden tespit edilmiş bölgeden geliyor) ve büyük mum bölgenin kendi küçük mumlarına göre tanımlandığı için üstünlüğün bir kısmı mekanik olabilir (bölgeler 60 günde %75-90 oranında 'büyük mumla' bitiyor); mutlak hareketle sağlama yapılmadı. (2) GENİŞLEME ZAMANI: BAŞARISIZ (iki pazar): ana alt kümede WF skill ~0; aynı model sıkışma dışı ve rastgele bölgelerde DAHA İYİ (fark -0,02..-0,07): zamanlama bilgisi sıkışmaya özgü değil. Süre uzadıkça bitiş olasılığı artmıyor (hazard düz); hisseye özgü süre ortak süreden iyi değil. Tek tutarlı zamanlama bilgisi ABD bilanço günü (bölgeyi bitiriyor, gözlenen - beklenen +0,32..+0,43, plasebo üstü). (3) YÖN: BAŞARISIZ (iki pazar): piyasanın 60 günlük yönünü geçmiyor; savunma hattının ve bölge içi konumun bağımsız katkısı yok; işlem sonucu fark yok. G3 (yaklaşan tepe-dip) ve G4 (savunulan destek) tek başına bölge bulmada da başarısız; işi küçük mum + dar bant yapıyor. CANLI (12 Kas, test dışı): (2) ve (3) geçmediği için 'genişlemeye yaklaşan' ve 'kırılma adayı' sınıfı kural gereği verilmedi; BIST 581 hissede 22 oluşuyor / 5 devam / 1 başladı, ABD 4.701 hissede 415 / 119 / 21; güvenilirlik DÜŞÜK. Denetim: (1) iki pazarın KASA hücreleri satır tablolarından bağımsız yeniden hesaplandı ve birebir tuttu; test 16/16; grafik paketten (VDYT.py + VDYT2.py ile) çiziliyor, tespit günü grafiğinde gelecek bar yok. Not: sınıf değerlendirme tablosu (bilgi) yön satırlarının seçiminden dolayı yanlı, kullanılmaz. DÜZELTME (14 Kas, Ç175): (1) tanımsal; KASA dönemi v1'de açıldıktan sonra v2 tasarlandı (bekletme temiz değil); eşler aynı yıl, aynı gün değil. ABD İZ DEĞİL, BIST ÖLÇÜLEMEDİ."),
    _ik_k("Ç164", "2026-11-12", "VDYT2-B test A: VDYT2 başarı (1) için MUTLAK HAREKET sağlaması (bölgeden bağımsız etiket): MA1 (ANA) = 20 günde en büyük |ln hareket| >= max(%15, 3 x σ250 x √20); MA2 = 20 gün sonu |ln getiri| >= 2 x σ250 x √20; MA3 = 20 günde bir gün gerçek aralık >= 3 x ATR250; aynı satırlar, aynı kontroller (DIŞARI, RASTGELE), WF + KASA", "VDYT2B.py, test_vdyt2b.py", "Cemal: 'ikisini de yap; önce ön kayıt ve ölçütleri sabitle; başarısız örnekleri dışarıda bırakma'", "Ön kayıt VDYT2B_ON_KAYIT.md (mühür 279d7f9f7064; git 8581767 17:43:46, koşu 17:50); VDYT2 sonuçları ve Ç163 kararı değişmez (sağlama)", "", 0, cikti="arastirma_cikti/vdyt/v2_20261112/ (VDYT2B_ON_KAYIT.md, VDYT2B_RAPOR_A.md, vdyt2b_sonuc_A.json)", notu="Karar: (1)-MUTLAK BAŞARISIZ (BIST ve ABD, WF ve KASA). Mutlak ölçünce küçük mum bölgeleri büyük hareketi kontrollerden DAHA AZ üretiyor: MA2 (20 gün sonu büyük hareket) ABD bölge %3,0 / %3,0 vs sıkışma dışı %4,5 / %5,0, rastgele %5,2 / %5,1; MA3 (büyük gün) ABD %6,7 / %8,5 vs %11,1 / %15,8; BIST aynı yön (MA3 %1,8 vs %8,9 WF). Aynı satırlarda bölge göreli etiket (BH1) 1,24-1,75 kat üstünlüğü veriyor: VDYT2 başarı (1) büyük ölçüde TANIMSAL (büyük mum, bölgenin kendi küçük mumlarına göre ölçülüyordu). Sonuç: sessiz bölge 'kendine göre' büyük mumla bitiyor ama piyasanın ve hissenin olağan ölçüsüyle büyük hareket habercisi DEĞİL; tersine sakin hisse sakin kalma eğiliminde. VDYT2 karar kaydı (Ç163) değişmez; bu bulgu onun yorumunu sınırlar. B (batanlar dahil, Tiingo) anahtar doğrulanamadığı için koşulmadı. Denetim: aynı satırlardaki BH1 oranları VDYT2 KASA sonuçlarıyla birebir aynı (satır kümesi doğrulandı); test geçti. DÜZELTME (14 Kas, Ç175): 'sakin hisse sakin kalır / bölge DAHA AZ üretir' yorumu geçersiz (oran eşleşmesiyle fark kayboluyor); sağlam yargı yalnız 'bölge mutlak büyük hareketi FAZLA üretmiyor'; BIST MA1 olay 6 / 12 ÖLÇÜLEMEDİ. Bağımsız Ç174 aynı yönde (KAT < 1)."),
    _ik_k("Ç165", "2026-11-12", "VDYT2-B test B (batanlar dahil, Tiingo): doğrulama pilotu 12 bilinen başarısız sembol; ardından 450 sembollük tabakalı örneklem çekimi", "VDYT2B.py", "Cemal: 'Tiingo'nun batanları eksiksiz verdiğini varsayma, önce bilinen başarısız sembollerle doğrula; başarısız örnekleri dışarıda bırakma'", "Ön kayıt VDYT2B_ON_KAYIT.md (git 8581767); pilot 12 Kas 19:45 UTC", "", 0, cikti="arastirma_cikti/vdyt/v2_20261112/vdyt2b_pilot.json", notu="PİLOT: KISMEN (7 / 12; önceden yazılı kural 7-9 = KISMEN). Seri 12 / 12 sembolde var, son işlem günleri iflas / delist tarihleriyle tutarlı, eksik gün yok denecek kadar az, SVB 9 Mart 2023 kapanışı basınla birebir (106,04 $). Kalanlar: OTC dönemindeki kuruşluk fiyatlarda >10 kat günlük sıçramalar (SIVBQ, RADCQ, YELLQ; kural K6) ve kod yeniden kullanımında iki şirketin serisinin boşluksuz birleştirilmesi (SUNE, CHK: KARIŞIK). Sonuç: Tiingo batanların fiyatını veriyor ama OTC ve kod değişimi dönemleri temizlik kuralı ister (ön kayıtta D1-D4 yazılı). ÇEKİM: ilk sembolde durdu; Tiingo hesabının Kasım ayı 500 farklı sembol kotası dolu (K56 EVREN2 işi 1-2 Kasım'da ~490 sembol kullanmıştı; pilot son payı yedi). B ölçülmedi. Kota takvim ayıyla 1 Aralık 2026'da yenilenir; sürdürme ya da 'VERİ YOK (kota)' kararı Cemal'de. Kotayı aşmanın yolları (yalnız bu ay sorgulanmış sembolleri çekmek, ücretli plan) kural dışı."),
    _ik_k("Ç166", "2026-11-13", "VDYT2 G5 sessiz bölge dedektörü insan gözü kör testi (40 grafik: 16 G5, 16 kontrol, 8 batan) + Tiingo batan OHLC doğrulaması", "KOR_TEST.py", "Cemal: 'algoritma insan gözünün gördüğü sıkışmayı yakalıyor mu, önce ölçülebilir işaret; Aralık kotası kanıtlanmamış fikre harcanmasın'", "Ön kayıt KOR_TEST_ON_KAYIT.md (git 7ef1e9d, anahtar 73da87f12549); SAPMA 1 v1.1 gösterim (git 9f0c987)", "", 0, cikti="arastirma_cikti/vdyt/v2_20261112/KOR_TEST_ON_KAYIT.md", notu="SONUÇ: İŞARET YOK (önceden yazılı kural: işaretli grafik < 8 -> VERİ YETERSİZ = İŞARET YOK). Cemal v1.0 (120 bar, grafik başına otomatik ölçek) için 'hepsi aynı görünüyor', v1.1 (250 bar, ortak log ölçek) için 'hiçbir belirti / özellik yok, rastgele seçilen bölge' dedi; tek tek işaretlemedi (cevap uydurulmadı, olc koşulmadı, anahtar açılmadı). Sonuç: G5 Cemal'in gözündeki sıkışmayı görünür biçimde seçmiyor; Ç164 (VDYT2 bölge başarısı tanımsal) ile tutarlı. KARAR (önceden yazılı): Aralık Tiingo kotası VDYT2-B testi B'ye HARCANMAZ; dedektör önce Cemal'in mevcut göz etiketlerine göre sınanır (GOZ_G5). Tiingo batan OHLC: 12 bilinen batan sembolün 8'inde tam, 3'ünde kısmen (SIVBQ, WEWKQ, CHK), SUNE yanlış seri (VDYT2B_OHLC_DOGRULAMA.md)."),
    _ik_k("Ç167", "2026-11-13", "GOZ_G5: G5 sessiz bölge dedektörü ve 10 basit şekil ölçüsü x Cemal'in mevcut göz etiketleri (kalibre 29 COL + 8 OLUMSUZ; C seti etiket_2026-10-20 21 DEĞİL + ARZUM 3 ÖBEK + 1 DEĞİL; COL_GOZ Claude'un gözü olduğu için dışarıda)", "GOZ_G5.py", "Kör test (Ç166) işaretsiz kalınca: G5 Cemal'in daha önce gözle seçtiği çöllere uyuyor mu; hangi basit ölçü gözün gördüğünü yakalıyor", "Ön kayıt GOZ_G5_ON_KAYIT.md (git a8e6509 11:09:25 UTC, mühür f4e6b492a436); ölçüm 03b5aa0", "", 0, cikti="arastirma_cikti/goz_g5/GOZ_G5_RAPOR.md", notu="A UYMUYOR: G5 (bölge günlerinin >= yarısında) Cemal'in çöllerinin 1/29'unu yakalıyor (0,03 [0,00; 0,11]); rastgele pencere 0,005 (580), olumsuz 2/8 = 0,25: G5 olumsuzda çölden sık yanıyor (gün payı çöl %5, rastgele %3, olumsuz %15). B ADAY YOK: en iyi LOSO AUC (çöl - rastgele) 0,77 (kapanış bandı, gövde / ATR250, 250 günlük konum); çöl - olumsuz en iyi 0,68 (konum, eşik 0,70). Cemal'in çölü aynı hissenin rastgele penceresinden kısmen ayrılıyor ama olumsuz dediği bölgelerden şekil olarak ayrılmıyor (Ç07 ile aynı). C yapılmadı (B'de aday yok; bilgi: G5 C setinde 0/22 DEĞİL, 0/3 öbek). Denetim: grup oranları ve iki AUC (kapanış bandı 0,773, konum 0,769) sonuç JSON'dan yeniden üretildi, tuttu; ön kayıt ölçümden önce."),
    _ik_k("Ç168", "2026-11-13", "TAVAN SERİSİ: çökmüş BIST hissesinde (250 gün tepeden >= %80 aşağı) k. ardışık tavandan sonra katılmak (k = 1..10), kontrol aynı gün tavansız çökmüş eş; BIST 2016 - 31.08.2026; canlı tarama 13.11.2026 (64 çökmüş, 26 tavan serisinde)", "TAVAN_SERISI.py", "Cemal: fon krizinde 1 TL'ye inmiş hisseler art arda tavan yapıyor; tavana katılmak mantıklı mı, rastgele mi", "Ön kayıt TAVAN_ON_KAYIT.md (git 4c5da06, mühür b6cccebae0a0); ölçüm 596b8d2", "", 0, cikti="arastirma_cikti/tavan_serisi/TAVAN_RAPOR.md", notu="İZ DEĞİL. k=1 (n 120, 38 hisse): ertesi gün tavan %35, 60g medyan -%10, +%100 %9, -%50 %7 (kontrol %0); medyan fark -%3,9 [-14,5; +9,4] = KUMAR. k >= 2 ana tanımda örneklem yetersiz (k=2 n 42, fark -%11,6). Duyarlılık (-%60 / -%70): n >= 30 olan bütün k'larda fark -%12..-%29, aralık tamamen 0'ın altında. Çökmemiş hissede ertesi gün tavan k ile %24 -> %79 artar, çökmüşte %35-40. Fon krizi sonrası (BİLGİ): çökmüş hissede ertesi gün tavan %56-82 (geçmişin iki katı), sonuç açık (Mart 2027 sonrası ölçülür). Denetim: k=1 sayıları olay dosyasından yeniden üretildi, tuttu."),
    _ik_k("Ç169", "2026-11-13", "TAVAN SERİSİ HACİM (Cemal'in itirazı): H1 çökmüş + hacim >= 10x 20g medyan + tavan; H2 dipte tavansız hacim; H3 '1 liradan nereye düşer' (çökmüş hisse-ay, fiyat kovası)", "TAVAN_SERISI.py (hacim)", "Cemal: 'hepsi kumar değil; TEHOL'de devasa hacimli alım barı var; 1 liradan daha nereye düşer'", "Ön kayıt HACIM_ON_KAYIT.md (git eb53803, mühür 65ff181df8d4); ölçüm 8f6dac4", "", 0, cikti="arastirma_cikti/tavan_serisi/HACIM_RAPOR.md", notu="İZ DEĞİL. H1 ana n 11 (9 hisse, 8'i 2016-19): +%61 / 20g %18, -%50 / 60g %18, 60g medyan -%6; kontrollü 5 olayda fark -%7 -> KANIT YOK (örneklem). Geniş hücre -%60 / 5x (n 201, 122 hisse): +%61 olasılığı %10 vs kontrol %4 (2,5 kat) ama 60g medyan fark -%14,8 [-17,1; -12,3]; n >= 30 olan 32 hücrenin 27'sinde aralık tamamen 0 altında, hiçbiri üstünde değil: hacimli tavan piyango profili (büyük sıçrama olasılığı artar, tipik sonuç kötü). H2 KANIT YOK. H3: çökmüş < 1 TL 120 günde -%50 %2 (n 54, 11 hisse; çoğu 2016-19, batanlar evrende yok), 1-2 TL %22, >= 2 TL %10. Kriz sonrası açık: TEHOL H2 05.11 (4.291x), H1 09.11 (581x). KAP dosyası (26 hisse, 21.944 bildirim): ortak tetik bulunmadı (dönüş 4 Kas piyasa geneliyle; 9-11 Kas SPK borsa dışı geri alım yolu, Kanun 7596 m.3, dönüşten sonra); şirketin kendisi tasfiye fonundan geri aldı: TKNKA 6,31 mn pay 31,10 TL (KAP 1697810, denetlendi), GIPTA, SVGYO; TEHOL ve PEKGY TMSF kayyımında (KAP 1684073 denetlendi), MSCI küçük endeksten 30 Kas'ta çıkıyor; 'yabancı bu hisseleri alıyor' söylenti (toplam yabancı alımı 6 Kas haftası +367 mn USD; hisse bazında yok). Denetim: H1 ana ve -%60/5x hücreleri olay dosyasından yeniden üretildi, tuttu."),
    _ik_k("Ç170", "2026-11-13", "GENİŞ KESİT: çökmüş 64 BIST hissesi, 31.10'da bilinen 19 özellik vs 31.10 -> 13.11 dönüşü (Y1 kat, Y2 tavan sayısı); Spearman + permütasyon, BH q 0,10; derinlik 2 ağaç (açıklama)", "GENIS_KESIT.py", "Cemal: 'emare vardır; geniş açıdan bak, bütün olasılıkları kat, fazla ajan, web'", "Ön kayıt KESIT_ON_KAYIT.md (git 125616d, mühür a019c04ea327, X 5fcf56e652ca); ölçüm 24f5831", "", 0, cikti="arastirma_cikti/genis_bakis/KESIT_RAPOR.md", notu="İZ DEĞİL (tek olay, emare). Tek aday: 31.10'a kadar KAP'ta geri alım bildirimi: rho Y1 +0,44 (q 0,003), Y2 +0,22; geri alımlı 17 hisse medyan x1,52 vs 47 hisse x1,26; +%50 dönme %53 vs %15; 17'nin hiçbiri 30.10 altında kalmadı (en kötü LIDER x1,08). Mekanizma: 5'i (GIPTA, SVGYO, SELEC, TKNKA, LIDER) 11-13 Kas tasfiye fonundaki payı borsa dışı geri aldı (SPK 11.11). Öteki 18 özellik (fon payı, tasfiye kalan, leke, PD/DD, fiyat, hacim, ortak alımı...) BH sonrası anlamsız; Y2'de fon stoku / leke daha çok tavan ama daha çok kazanç değil. Çöl tablosu: TEHOL fon girişinden önce çöl EVET (Kas-Ara 2024), KTLEV / DSTKF ölçülemez (kısa geçmiş), BINBN fon %5 yok. Denetim: rho 0,440 / 0,224, 17 vs 47 medyan ve %53 / %15 X.csv-Y.csv'den yeniden üretildi, tuttu; ön kayıt ölçüm commit'inde değişmedi. Sıradaki: geri alım emaresi 2018 ve 2020 BIST çöküşlerinde."),
    _ik_k("Ç171", "2026-11-13", "BofA İZİ: AKD alım listesi ilk 3 -> tutma dönemi (çıkış satış ilk 5 haberi; yoksa 250 gün), eşli fark + 200 rastgele portföy; öteki yabancı kodlar aynı ölçü (BH q 0,10); ikincil FI_OLCUT 60g; en erken yayın saati", "BOFA_IZI.py", "Cemal: 'BofA almış, emare; alımından satımına kadar takip et, 60 gün değil; diğer yabancı kodları da'", "Ön kayıt BOFA_ON_KAYIT.md (git b7943a1, mühür 6b544f940e23); ölçüm f3b7834 (sapma yalnız gösterim: hacim 0 işareti)", "", 0, cikti="arastirma_cikti/bofa_izi/BOFA_RAPOR.md", notu="İZ DEĞİL (kanıt yok). Arşiv 2.774 liste haberi (Rota Borsa, hisse.net, YatırımX), 17.04.2023-13.11.2026. ANA n 1.751, tutma medyan 3 gün, eşli fark +%0,6 [-0,6; +2,0], 2023-24 -%0,6 / 2025-26 +%1,6, portföy rastgele %90'ı geçmedi. Lot sıralı listeler (kuruş hisseler, PEKGY tipi) ters: tutma -%6,4 (n 79), 60g -%10,3 [-15,0; -5,2] (n 76). Çökmüş hisse -%11,8 (n 23). 60g alım ilk 3 -%0,8 (n 411); satış ilk 3 de bilgi yok. HSBC -%2,1 [-4,2; -0,1] (n 586); bütün kodlar -%0,0 (n 2.632); Deutsche n 11. Kriz (BİLGİ): 197 dönem, ort. -%3,5; PEKGY 28.10-12.11 +%48,8 ama 19-26.10 -%33; TEHOL 15.09 alım -> -%97,5; ODINE açık, dip -%43,7. En erken: gün içi liste medyan 13:41 (veri 12:50), gün sonu 19:13; hisse.net news-sitemap, rotaborsa RSS; bi_izle_tur yazıldı, çalıştırılmadı; ücretli AKD başlatılmadı. Denetim: ana +%0,58 n 1.751, HSBC -%2,14 n 586, lot 60g -%10,33 n 76 olay dosyasından yeniden üretildi, tuttu; ön kayıt sonrası kod değişikliği yalnız gösterim. DÜZELTME (13.11.2026, ana model denetimi; commit 763ae34 + a9c00ea): ayrıştırma hataları giderildi: çok kurumlu haberde tablo kurumu önceki başlıktan (belirsiz BİLİNMİYOR, ölçüm dışı; 94283 blok 1 İş Yatırım'ınmış), kurum adı hisse satırları düştü, aylık / dönemsel özet 45 haber kapsam dışı, hisse.net'te aynı adreste biriken günlük güncellemeler (2 haber, 208 bölüm, 1.399 satır) kendi tarihini taşıyor (Eylül listesi Haziran sayılıyordu: GELECEĞE BAKMA giderildi), YatırımX / Rota kenar kuşağı çöpü (SSAAT 100 satır, 79'u BofA ilk 3'teydi) gövde dışı. Liste mührü 7020587f -> 28014e1a, eşikler aynı, --sapma ile koşuldu. YENİ: ANA n 1.789 eşli +%0,6 [-0,5; +1,9] sıra 0,51 KANIT YOK değişmedi; lot n 131 +%2,4 [-6,3; +11,4] (eski -%6,4 ters işaret kalktı); HSBC n 618 -%2,7 [-4,9; -0,6]; TOPLU -%0,1. Ana model: ANA (n 1.789, +%0,57, sıra 0,511) ve lot (n 131, +%2,43) satır dosyasından yeniden üretildi, tuttu. Eski çıktılar arastirma_cikti/bofa_izi/eski_v1/."),
    _ik_k("Ç172", "2026-11-13", "BofA KENDİ MALİYETİNDEN KÂRI + HABER SONRASI YOL: A betimleyici (maliyetli alım satırı -> 5/20/60g, eşli; FIFO alım-satım eşleme); B 6 koşul (K1 pay >= %20, K2 giriş <= maliyet +%5, K3 5 günde 2 alım, K4 önce sattı şimdi alıyor, K5 çökmüş, K6 lot listesi) + TÜMÜ, G1 (gün içi 17:30 öncesi -> aynı gün kapanış) + C1 (satış ilk 5), FI_OLCUT dört şart + iki alt dönem + BH q 0,10", "BOFA_IZI.py (karonkayit / karkos)", "Cemal: 'BofA bir hissede %40-80 zarar etmez; bana bir yol gösterecekse ölç'", "Ön kayıt BOFA_KAR_ON_KAYIT.md (git fd3e980, mühür f50d11088ccb); ölçüm 9cb7d78 (sonrası yalnız gösterim)", "", 0, cikti="arastirma_cikti/bofa_izi/BOFA_KAR_RAPOR.md", notu="İZ DEĞİL, YOL YOK (en fazla BIST-ADAY olabilirdi: AKD yalnız BIST). A: kriz öncesi maliyetli 72 alım (46 hisse, çoğu 2025): 20g maliyetinden medyan +%3,2, kâr %57, eşli +%0,7; 60g medyan +%5,5, eşli +%1,3: piyasa gibi. Kriz sonrası (BİLGİ) n 87: 20g medyan -%9,9, kâr %22, P(-%30) %16, eşli +%1,2 (piyasayla birlikte kaybetti; KTLEV -%64,5, EUPWR -%43,9, ASTOR -%36,2). FIFO yalnız kriz sonrası: -%3 ile -%9,5, kârlı %36-37. B: TÜMÜ +%0,6 [-0,3; +1,6] n 1.567; K3 +%0,2 n 732; K4 +%0,1 n 1.417; K6 lot -%6,4 [-13,3; -0,5] ters; K2 +%5,9 n 22 ve K1 +%17,8 n 11 örneklem yetersiz; K5 -%7,8 n 20. 60g ikincil hepsi kanıt yok (K5 -%22,6). Sınır: maliyet yalnız 320 satırda; aylık özet haberi bir kez gün içi okunmuş (kriz sonrası, karar etkisiz). Denetim: B TÜMÜ / K6 / K2 / K3 ve A 20g (n 72, medyan +%3,2, kâr %57, eşli +%0,69) satır CSV'sinden yeniden üretildi, tuttu; ön kayıt sonrası diff yalnız rapor gösterimi. DÜZELTME (13.11.2026, aynı ayrıştırma düzeltmesi, commit a9c00ea): YOL YOK değişmedi. TÜMÜ n 1.620 +%0,6 aynı; K2 n 57 +%1,5 [-1,1; +4,5]; K6 n 87 -%0,8 [-5,1; +2,3] (eski 'anlamlı ters' kalktı, sıfırı kapsıyor); K1 n 15. A: kriz öncesi 20g n 120 medyan -%3,9, kâr oranı %39, eşli -%1,5 (eski +%3,2 / %57 / +%0,7 güncelleme damgalı Nisan-Eylül listeleriyle değişti); 60g n 79 medyan +%3,5 kâr %56; kriz sonrası 20g n 194 medyan -%15,2 eşli +%0,5; FIFO n 302 medyan -%4,3. Ana model: A 20g (n 120, -%3,9, %39,2, eşli -%1,51), TÜMÜ, K6, K2 satır dosyasından yeniden üretildi, tuttu. Cemal'in 'BofA %40-80 zarar etmez' itirazına yanıt: -%40..-%65 sayıları gerçekleşen zarar değil, alım günü maliyetinden 20 gün sonraki fiyat; görünen eşleşmiş alım-satımda KTLEV -%11 (67 mn lot alım ort 7,40 / 26 mn lot satış ort 6,55), TURSG -%22, PEKGY +%36, INFO +%37; listeler ilk 5'le sınırlı, geri kalan satış görünmez; AKD kodu kurum pozisyonu değil müşteri akışı."),
    _ik_k("Ç173", "2026-11-13", "DİPTE BofA: KURULUM = 250g tepeden <= -%80 + son 10 günde yeni dip yok + dipten <= 1,5 kat (60 gün ayrı olay); (1) kurulum tek başına FI_OLCUT 60g + 250g olasılık (BIST, ABD, Avrupa); (2) kurulum + BofA alım ilk 5 (G1 giriş), BofA'sız kurulumla kıyas; (3) bugünkü izleme", "BOFA_IZI.py (diponkayit / dipkos)", "Cemal: 'her BofA alımında değil; dipte %80-90 düşmüş, artık düşmeyecek, çok ucuzlamış noktada BofA alımıyla gir'", "Ön kayıt BOFA_DIP_ON_KAYIT.md (git 22750ff, mühür cac944c2b07c); sonuç 478c580 (sonrası yalnız gösterim)", "", 0, cikti="arastirma_cikti/bofa_izi/BOFA_DIP_RAPOR.md", notu="İZ DEĞİL; BofA YOLU ÖLÇÜLEMEZ (kriz öncesi olay 0). (1) Kurulum: ABD 2023 n 81 +%24,8 [+8,9; +43,0] sıra 0,55 TUTTU; ABD 2024-26 n 146 +%20,6 [+0,4; +46,2] sıra 0,48, portföy tutmadı; Avrupa n 3 / 8, BIST 2023 n 4, BIST 2024-26 n 28 yetersiz; BIST 2016-22 n 56 -%6,0; ABD 2016-22 n 508 -%2,7. 250g: ABD P(+%100) eşin 1,6-2,0 katı, P(-%50) de 1,7-2,0 katı (piyango, seçici değil); BIST 2016-22 P(+%100) 0,94 kat, P(-%50) 1,96 kat. Hayatta kalma yanlılığı ABD'yi yukarı iter. (2) 5.519 BofA alım tetiğinden kurulumdaki: kriz öncesi 0; kriz sonrası HDFGS 21.10 (BİLGİ: 13.11'e +%18,5; 09.11 BofA satışıyla dönem +%17,6). BofA ±20 gün kurulum n 2 (KLRHO -%16,7, SMRVA -%45,1 eşli). (3) 13.11 kurulumda 10 BIST hissesi: SKBNK, KLRHO, PRZMA, BORLS, OTTO, A1CAP, IZFAS, BURVA, USAK, IHLAS; 20 günde BofA ilk 5'te yalnız SKBNK (05.11, 3,65 -> 3,83). Denetim: ABD 2023, ABD 2024-26, BIST 2016-22, ABD 2016-22 (n, eşli fark, sıra) satır verisinden yeniden üretildi, tuttu. DÜZELTME (13.11.2026, commit a9c00ea): değişmedi; BofA tetik 5.679, tetikli kurulum 1 (HDFGS), izleme 10 aynı."),
    _ik_k("Ç174", "2026-11-14", "SIKISMA_YENIDEN (bağımsız yeniden ölçüm, VDYT raporları okunmadan): S1 sıkışma (10 gün ort. TR/C <= 250 günün %20 yüzdeliği; bant <= %6 / BIST %8) sonrası 20 günde MUTLAK büyük gün B1 (aralık >= 3 x ATR250) olasılığı vs aynı gün / σ250 ondalığı / likidite eşleri; (B) ilk büyük günün zamanı, hazard, walk-forward lojistik; (C) yönsüz stoplu kırılım işlemi; BIST, ABD, AVR x 2016-22 / 2023 / 2024-26", "SIKISMA_YENIDEN.py", "Cemal: 'şu kesin ki sıkışmadan sonra büyük mumlar geliyor; başlama zamanını tahmin edebilir miyiz, stoplu işlemle fayda sağlar mıyız'", "Ön kayıt SIKISMA_ON_KAYIT.md (git bde587c 08:39:03, koşu 08:39:08; mühür 1eb406a2; KONTROL LİSTESİ dolu, ik_kontrol_kapisi geçti: kapıyı kullanan ilk modül); sonuç a22e418", "", 0, cikti="arastirma_cikti/sikisma_yeniden/SIKISMA_RAPOR.md", notu="(A) İZ DEĞİL, eğilim TERS (güç yeterli, n 1.266-9.540): KAT ABD 2023 0,98 [0,86; 1,12], ABD 2024-26 0,78 [0,69; 0,86], AVR 2023 0,87 [0,72; 1,01], AVR 2024-26 0,75 [0,62; 0,88]; keşif 2016-22 de < 1; BIST 0,45-0,65 (bilgi; ±%10 sınırı B1'i kısıtlar). Göreli ölçüyle (B0: sıkışmanın kendi mumlarına göre 3x) KAT 1,6-1,9: 'büyük mum geliyor' algısı TANIMSAL; mutlak ölçüyle artmıyor (Ç164 ile aynı yön, bağımsız). (B) İlk büyük gün medyan 10-12. gün, %25-75 6-16; erken yığılma yok; süre uzadıkça artmıyor; WF skill ABD ~0 (alt < 0), AVR +0,002: ZAMAN TAHMİNİ YOK (bilanço takvimi yok). (C) 12 hücrenin 12'si TUTMADI: eşli fark ABD +%0,06 [-0,21; +0,33], AVR +%0,08, sıra 0,51; P(+%20 önce) ve P(-%10 önce) ikisi de eşlerden düşük (dar stop iki yönü de daraltıyor). Sert düşüş alt kümesi ABD KAT ~1,0 n 108-151 ÖLÇÜLEMEDİ. SINIR: eşler σ250 ondalığında; sıkışmanın anlık / 250 gün oynaklık oranı tanım gereği düşük, 3 x ATR250 eşiği sıkışan hisse için daha zor (VDYT denetimi Ç175); bu, Cemal'in sorusunun ('olağan ölçüde büyük mum gelir mi') doğrudan yanıtıdır ama 'sıkışma başka bir şey ekler mi' sorusu için ileri testte oran eşleşmesi de koşulacak. Hayatta kalma yanlılığı var, komisyon yok. Denetim (ana model): A ABD 2024-26 (n 2.392, %14,6 / %18,7, 0,78), A AVR 2023 (0,868), A ABD 2023 (0,979), C ABD 2023 (n 3.381, +%0,18, sıra 0,51) satır verisinden yeniden üretildi, tuttu; ön kayıt < koşu; yasak dosyalar değişmedi."),
    _ik_k("Ç175", "2026-11-14", "VDYT AİLESİ DENETİMİ (Ç162-Ç164) + ESKİ ÇÖL KAYITLARININ YENİDEN ETİKETLENMESİ: 14 maddelik kontrol listesiyle kod + rapor denetimi; 24 hücre satır verisinden yeniden üretildi; eski 'İZ DEĞİL' kararları güç kuralıyla (n >= 1.000 ya da güç kanıtı) yeniden sınıflandı", "VDYT.py, VDYT2.py, VDYT2B.py (salt okunur denetim)", "Cemal: 'eski çöller iz değil diye kaldı; bu kadar yanlıştan sonra bunlarda da yanlışlık olma ihtimali yüksek; yeni kontroller ışığında tekrar bak'", "Denetim raporu scratchpad/vdyt_denetim.md (6 bölüm); IK_HATA'ya 9 satır", "", 0, cikti="IZ_KARNE.py IK_HATA (14 Kas satırları)", notu="TUTANLAR: dört ön kayıt koşudan önce; VDYT2 karar günü seçimi yalnız t ve öncesi (geleceğe bakma yok); WF ölçekleyici / eşikler yalnız eğitimden; VDYT2B 24 hücre satır verisinden birebir (ABD MA3 %6,68 / %11,08; BIST %1,80 / %8,88). HATALAR: (1) Ç162 Motor 1 'basitten iyi' mekanik (hedef penceresi karar gününü içeriyor), Motor 2 yön bölge içi konumdan: ikisi İZ DEĞİL; (2) Ç163 (1) 'bölgeyi bulmak başarılı' tanımsal (Ç164 bulmuştu); (3) Ç164 'sakin hisse sakin kalır' yorumu kısmen mekanik: eşler aynı NATR ondalığında ama bölgenin NATR14 / ATR250 oranı düşük (0,51-0,53 vs 0,62-0,64); oranla düzeltince ABD WF MA3 farkı kayboluyor, BIST KASA işaret dönüyor (ön kayıtsız, bilgi); sağlam kalan yargı: bölge mutlak büyük hareketi kontrollerden FAZLA üretmiyor; (4) BIST MA1 olay 6 / 12: ÖLÇÜLEMEDİ; (5) ABD k60 fiyat verisinde 4.678 hissenin 1.235'inde > 3x sıçrama ya da H-L > 2 x kapanış (ters bölünme / OTC), SUNE ATR250 fiyatın 600 katı: ATR / σ tabanlı ölçüler o satırlarda anlamsız; (6) eşler aynı yıl, aynı gün değil; (7) KASA dönemi v1'de açıldıktan sonra v2 tasarlandı (bekletme temiz değil); (8) satır verisi yalnız konteynerde. YENİ ETİKET: Ç162-Ç164 ABD İZ DEĞİL, BIST ÖLÇÜLEMEDİ; VDYT ailesinde olumlu iddia yok. ESKİ ÇÖL: en az 20 kayıt 'İZ DEĞİL' yazılı ama ÖLÇÜLEMEDİ (Ç38, Ç39, Ç50, Ç57, Ç67-Ç70, Ç73-Ç83, Ç87, Ç89, Ç90 ve Eylül cetveliyle ölçülenler); İZ DEĞİL'i hak eden gövde Ç34, Ç41, Ç44, Ç47, Ç49, Ç56, Ç72, Ç85, Ç86, Ç88, Ç91, Ç93, Ç96 (ABD), Ç104, Ç132, Ç134, Ç156; Ç37 D9 hiç kapanmamış ama üretim ekranında; Ç124 INTEM sıkışma ailesindeki tek EMARE, ileri testi yok. YENİDEN KOŞU ÖNERİSİ: (1) VDYT2 mutlak hareket aynı gün + oran eşleşmesi + batanlar; (2) K24 iki evre çöl (ABD 2023 +%3,1 / 2024-26 -%0,5 çelişkili) PV2 + olasılık tablosu, batanlar dahil; (3) Ç37 D9 uzun çöl + rüzgâr; (4) Ç75 / Ç78 düzgün dip, iki yuvarlama (ABD 1,25 n 730; 1,41 n 307); (5) Ç124 ileri test. Ana model denetimi: Ç175 bulgularından (5) k60 sıçrama ve (6) aynı yıl eşleme kodda doğrulandı (VDYT2.py:913, 1259); kurala yorum: n >= 1.000 HÜCRE başına (CLAUDE.md'ye yazıldı)."),
    _ik_k("Ç176", "2026-11-14", "SIKISMA DUYARLILIĞI (Cemal'in 'gözüm neden büyük görsün' itirazı): büyük mum eşiği k {1,5; 2; 2,5; 3; 4} x referans {ATR250, ATR60 (sıkışma hariç), ATR_sıkışma}, ufuk 20 / 5 gün, sıkışma uzunluğu p {10, 20, 40, 60}; eş 1 (Ç174) + eş 2 (anlık / 250 gün oynaklık oranı 20'liği x likidite); 'göz ölçüsü' dağılımları; 40 kör grafik (20 olay + 20 eş, tohum 27)", "SIKISMA_YENIDEN.py (duyarlilik)", "Cemal: 'gözüm küçük mumlardan sonra gelen mumları neden büyük görsün ki, burada ayrılık var'", "Ön kayıt DUYARLILIK_ON_KAYIT.md (git 0382244 10:48:16, koşu 10:48:21; mühür ac472e8b1e91; KONTROL LİSTESİ dolu, kapı geçti); sonuç 4acbe37", "", 0, cikti="arastirma_cikti/sikisma_yeniden/DUYARLILIK_RAPOR.md, SIKISMA_ORNEK_40.pdf, ornek_anahtar.json", notu="BİLGİ; Ç174 kararı (İZ DEĞİL) değişmez. Eş 1 ile ATR250 / ATR60 eşiklerinin HİÇBİRİNDE, hiçbir p'de KAT güvenle > 1 yok: ABD 2023+ 80 kombinasyonun 36'sı güvenle < 1, 44 belirsiz; AVR 47 < 1. Eşik gevşeyince (k 1,5-2, ATR60) KAT 0,90-1,00'e yaklaşıyor, geçmiyor; p uzadıkça artmıyor (AVR p60 0,58). EŞ 2 (aynı derecede sakinleşmiş hisseler): ABD KAT ~1,00 [0,88; 1,12] -> Ç174'teki 'ters' etki mekanik (oynaklığı yakın zamanda düşmüş her hissede var), sıkışma desenine özgü değil; AVR eş 2 ile yine 0,79 [0,69; 0,90]. GÖZ ÖLÇÜSÜ: ilk 20 günün en büyük mumu, sıkışma mumunun medyan 2,7 katı (ABD 2,73, AVR 2,75, BIST 2,94); eş 1'de 2,1-2,2; eş 2'de de 2,6-2,8 (fark yok); ATR250 katı olarak olay 1,70, eş 1,8-1,9. Yani Cemal'in gözü doğru görüyor (mum 2,7 kat büyüyor) ama bu oynaklığın ortalamaya dönüşü; hissenin kendi normaline göre büyük değil ve sıkışma desenine özgü değil. BH q 0,10 (1.440 sınama): 630 seçilen hücrenin 621'i < 1; > 1 olan 9'un 3'ü dejenere (BIST 2023, büyük gün < 10), 4'ü ABD eş 2 p60 2023 (2024-26'da ters), 2'si k 1,5 (1,04-1,05). Ana model denetimi: ABD p10 eş1 2xATR250 2023+ (n 5.868, 0,8434), ABD p10 eş2 3xATR250 (n 5.515, 1,0041), AVR p40 eş2 3xATR60 2024-26 (n 71, 0,8062), göz oranı medyan 2,73 / 1,70 satır verisinden yeniden üretildi, tuttu. HATA: yön etiketi n olay >= 30'a bakıyor, büyük gün sayısı < 10 hücreler dejenere (okunmaz)."),
    _ik_k("Ç177", "2026-11-14", "ORTAK CETVEL v1.0 (Aşama 1 / 4): dört aşamalı yeniden ölçüm (K24 iki evre, D9 uzun çöl + rüzgâr, düzgün dip vs çöl ayrımı, INTEM ileri test) için tek, mühürlü ölçüm cetveli; FI_OLCUT eş hücresi birebir (geçmiş bilgili havuz), beş şartlı hücre kuralı (dört şart + iki yarı aynı yön), olasılık tablosu (+%100 / -%50, 250 gün, eş katı), etiketler (İZ / İZ + BIST / EMARE / ABD-ADAY / İZ DEĞİL / ÖLÇÜLEMEDİ; SEÇİCİ / PİYANGO / YOK), oc_kapi (cetvel sha + kod sha + güç sha + git + kontrol listesi), güç simülasyonu", "ORTAK_CETVEL.py, test_ortak_cetvel.py", "Cemal: 'her aşamada aynı ölçüm kriterleri; sonucu beğenmediğimiz için eşikle oynanmaz' -> mekanik: aşamalar cetvel sha'sı farklıysa koşmaz", "Ön kayıt CETVEL_ON_KAYIT.md (commit a0ee21f 13:25:44; CETVEL_SHA 4763c458, KOD 7bd6f6db, GÜÇ 7921963e); sinyal ölçülmedi", "", 0, cikti="arastirma_cikti/ortak_cetvel/ (CETVEL_ON_KAYIT.md, GUC_TABLOSU.md)", notu="GÜÇ (ABD 2023-26 gerçek eş farkı dağılımı, 1,72 mn hisse-gün, 200 tekrar, beş şart): δ +%10 n >= 100'de %91+; δ +%5 en çok %65 (n 1.000); δ +%2 en çok %25; yanlış pozitif <= %2,5; K58 ile tutarlı. PORTFÖY ŞARTI GÜCÜ TAVANLIYOR: 10 yuvalı slot portföyü olayların küçük kısmını alır, n büyüse de güç artmaz; 'güç >= %80' yolu gerçek veride açılmıyor -> İZ DEĞİL fiilen yalnız n >= 1.000 hücrede; gerçek +%5 etki dört hücreyi birlikte ~%13 olasılıkla geçer. Bu FI_OLCUT'un kendi özelliği; Cemal'in şartı gereği cetvel değiştirilmedi, sınır olarak yazıldı. Bilinçli sapmalar (ana model onayladı): ileri pencerede bölünme dışlaması KALDIRILDI (ANA kuralın yakaladığı günlerin %89'u 1,5-2x gerçek hareket; ABD 2023-25 pencerelerinin %5-9'unu silip +%100 / -%50 sıçramalarını yok ederdi = sonuca göre seçim); havuz 'geçmiş' kipinde (FON_IZI havuzu ileri r60'ı olan hisselerle kurulur: küçük ileri bilgi); iki yarı aynı yön. Test 14/14; kapı AÇIK (ana model çalıştırdı). Sınır: hayatta kalma (bugünün listesi + k34 1.472 hisse, batan yok, Tiingo yok); V_BIST 2023-06'dan (BIST 2016-22 boş); 250 gün dokunma en geç Ağu 2025 girişleri; komisyon yok. evren_disi_ABD.csv hiçbir dalda yok, fon listesi K55_EVREN_DISI.csv'den (7 fon)."),
    _ik_k("Ç178", "2026-11-14", "K24 İKİ EVRE ÇÖL YENİDEN (Aşama 2 / 4, ORTAK CETVEL v1.0): FON_IZI fi_k24_tara değişmeden; BIST (bilgi), ABD (+k34), AVR; 2016-22 / 2023 / 2024-26; çöl uzunluğu ve derinlik kovaları bilgi", "K24_YENIDEN.py", "Cemal: 'temel çöl yapısının tespit başarısını ölç'", "Ön kayıt K24_YENIDEN_ON_KAYIT.md (git 5ddff64 13:37:19, koşu 13:37:27; FI_K24 sha dondurulmuş; SAPMA-1 t'ye kadar 200 bar, SAPMA-2 OC temiz veri; cetvel kapısı geçti); sonuç de08c4b", "", 0, cikti="arastirma_cikti/k24_yeniden/K24_YENIDEN_RAPOR.md", notu="GENEL: ÖLÇÜLEMEDİ; olasılık etiketi YOK. Temel çöl yapısı (K24) sonraki 60 günde eşlerden ayrışmıyor: ABD 2024-26 n 2.869 -%1,1 [-2,7; +0,9] TUTMADI (güç yeterli); ABD 2023 n 941 +%1,3 [-1,0; +3,7] ÖLÇÜLEMEDİ (güç %52); AVR 2023 n 100 +%0,5, AVR 2024-26 n 286 +%0,1 ÖLÇÜLEMEDİ (güç %29); BIST -%1,5 / +%0,3; ABD 2016-22 n 3.271 -%0,6 TUTMADI. OLASILIK: ABD iki dönem PİYANGO (+%100 katı 1,17 / 1,19; -%50 katı 1,15 / 1,21), AVR 2024-26 PİYANGO (1,97 / 1,81), AVR 2023 YOK; eşler oynaklıkla eşlenmediği için -%30 düşmüş hissenin iki yöne daha sık dokunması büyük ölçüde mekanik olabilir. Çöl uzunluğu tercili ve derinlik kovası: hiçbir alt küme tutmadı. Eski Ç113 ABD 2023 +%3,1 'aralık artı' sonucu yeni cetvelde yok (k34 hisseleri, OC havuzu, SAPMA-1). HATA: fi_k24_tara 'n < 200' şartı serinin TOPLAM uzunluğuna bakıyordu (geleceğe bakma; 1.430 sinyal düştü; eski Ç96 / Ç113 / Ç118 bunları içeriyordu); oc_hucre iki yarı sıralaması kararlı değil (0,1-0,3 puan oynama, etiket değişmedi). Denetim (ana model): ABD 2024-26 (n 2.869, -%1,09, sıra 0,49, +%100 1,19, -%50 1,21), ABD 2023 (n 941, +%1,26), AVR 2024-26 (n 286, +%0,08, 1,97 / 1,81) satır verisinden yeniden üretildi, tuttu."),
    _ik_k("Ç179", "2026-11-14", "DÜZGÜN DİP vs ÇÖL AYRIMI (Aşama 4 / 4, ORTAK CETVEL v1.0): dip16 (Ç75 FI_K16_GEVSEK) / dip17 (Ç78 k17) ile K24 çöl; A yalnız dip, B yalnız çöl, C 60 günde ikisi, D rastgele; ayrım ölçüsü C-A ve C-B kat farkı (%95)", "DIP_COL_AYRIM.py", "Cemal: 'çöl formasyonuyla gerçek dip oluşumunu ayırabiliyor muyuz, denetle'", "Ön kayıt DIP_COL_AYRIM_ON_KAYIT.md (git b1d2a42 13:41:19, koşu 13:41:24; parametreler dondurulmuş; cetvel kapısı geçti); sonuç a4bbb48", "", 0, cikti="arastirma_cikti/dip_col_ayrim/DIP_COL_AYRIM_RAPOR.md", notu="AYRIM ÖLÇÜLEMEDİ (ön kayıtlı kural). ABD'de C ≈ A: +%100 katı 1,41 / 1,42 (2023) ve 1,40 / 1,33 (2024-26), fark aralığı 0'ı kapsıyor. C > B (+%100 1,41 vs 1,10) ama -%50 katı da büyük (1,48 vs 1,08): dip içeren kümeler iki yöne de daha çok hareket ediyor, PİYANGO tipi, seçici değil. 60 gün eşli fark C-A ve C-B bütün karar hücrelerinde 0'ı kapsıyor. AVR C n250 11 / 33 (ölçülemez). Hiçbir kümede İZ ya da EMARE yok; ABD 2024-26'da A, B, C, D hepsi TUTMADI. Dipten çöle uzaklık ayırıcı değil. Eski Ç75 1,25 / Ç78 1,41 (önce +%20 katı) yeni cetvelde A 1,13-1,26, C 1,11-1,18: yön aynı, daha küçük. HATA: FON_IZI fi_k13 / fi_k17 (n < 400) ve fi_k24 (n < 200) tarayıcıları seri TOPLAM uzunluğuna bakıyor (geleceğe bakma; burada i >= 399 / 199 ile düzeltildi; eski Ç75-Ç78 / K24 küçük ölçüde etkilenmiş olabilir). Denetim (ana model): C / A / B ABD 2024-26 (n 1.059 / 1.248 / 2.518; fark +%0,72 / +%1,1 / -%0,81; +%100 katı 1,402 / 1,332 / 1,144; -%50 1,377 / 1,475 / 1,149) satır verisinden yeniden üretildi, tuttu."),
    _ik_k("Ç180", "2026-11-14", "INTEM İLERİ TEST (Aşama 5, ORTAK CETVEL v1.0): Ç124 kuralı (FI_K44 parmak izi + K45 kısa ufuk kutu çıkışı, değişmeden; cetvel Ç124 ABD havuzu, eşleşmeler 317 / 317 ve 39 / 39 birebir) GÖRÜLMEMİŞ veride: yalnız ABD k34 ekinin 1.465 hissesi (2021+); Avrupa Ç124'te görülmüştü (k44_eslesme.csv 117 + 271), kullanılmamış dönem yok", "INTEM_ILERI.py", "Cemal: 'önceki aşamalardan çıkan kuralları değiştirmeden, görülmemiş veride dene'", "Ön kayıt INTEM_ILERI_ON_KAYIT.md (git bf0334d 14:18:21, koşu 14:18:31; eşikler ve band 0,125 değişmedi; SAPMA 1-4 sonuç görülmeden); sonuç 370e0d1", "", 0, cikti="arastirma_cikti/intem_ileri/INTEM_ILERI_RAPOR.md", notu="ÖLÇÜLEMEDİ; EMARE yeni veride desteklenmedi, iddia kapanmadı. Aşama 2 ve 4 kural üretmediği için ileri test edilecek başka kural yok. ORTAK CETVEL L20: ABD 2023 n 26 -%3,2 [-19,8; +31,6] (n < 30); ABD 2024-26 n 42 -%7,5 [-17,8; +2,9] (güç %10); AVR görülmemiş veri yok. Olasılık ABD 2024-26 (n250 33, bilgi): +%100 0,58 kat [0,29; 0,91], -%50 1,42 kat [1,04; 1,84] (SEÇİCİ'nin tersi yönde, küçük örneklem). Ç124'ün kendi ölçüsü (20 günde önce +%8 vs oynaklık eşli rastgele): +2,7 puan [-6,8; +12,2] n 105 (eski Ç124 ABD +11,2 [+6; +17]); 2021-22 +8,6, 2023 +0,8, 2024-26 +0,5. Görülmemiş evren farklı nüfus (nakit yakan küçük şirketler). HATA: iş tanımı 'Avrupa Ç124'te hiç yok' demişti, yanlıştı (ana model); fi_k23_parmak 'n < L+200' toplam uzunluk şartı geleceğe bakıyordu (SAPMA-1 ile t anına indirildi; Ç124 küçük ölçüde etkilenir); rapordaki 'ABD 2016-22' fiilen 2021-22. Denetim (ana model): L20 ABD 2023 (n 26, -%3,16, medyan -%8,14, sıra 0,46, katlar 1,03 / 1,02) ve ABD 2024-26 (n 42, -%7,51, -%10,47, 0,459, 0,58 / 1,42) satır verisinden yeniden üretildi, tuttu."),
    _ik_k("Ç181", "2026-11-14", "D9 UZUN ÇÖL + SEKTÖR RÜZGÂRI YENİDEN (Aşama 3 / 4, ORTAK CETVEL v1.0; Ç37'nin kapanmamış testi): (a) D9 tek başına, (b) D9 + rüzgâr (üretim T8 listesi), (c) yalnız rüzgâr; COL_v1 D9 / D9b parametreleri değişmeden (kopya birebir doğrulandı); BIST bilgi, ABD karar, AVR yalnız (a) (sektör listesi yok)", "D9_YENIDEN.py", "Cemal: 'uzun süren sıkışmanın ve rüzgâr etkisinin tespit performansını ölç'", "Ön kayıt D9_YENIDEN_ON_KAYIT.md (git 90558af 13:46:03, koşu 13:46:09-13:55; SAPMA: piyasa = COL_v1 medyanı, ABD sektör = 'endustri'); sonuç fe68b00 (15:40; koşu bitiminden 105 dk sonra commit, süreç hatası)", "", 0, cikti="arastirma_cikti/d9_yeniden/D9_YENIDEN_RAPOR.md", notu="(a) UZUN ÇÖL İZ DEĞİL (güç yeterli), olasılık YOK: ABD 2023 n 2.399 -%0,6 [alt -2,1], ABD 2024-26 n 4.556 -%1,7 [alt -2,8], AVR 2023 n 1.102 -%0,4, AVR 2024-26 n 2.102 -%1,1: dört karar hücresi TUTMADI; +%100 katı ABD 0,40-0,43 [0,33; 0,52], -%50 katı 0,42-0,54: D9 SAKİN HİSSE SEÇİYOR, iki yöne de eşlerin yarısı kadar hareket; çöl süresi 6-9 / 9-12 / >= 12 ay hiçbiri eşlerin üstünde (>= 12 ay +%100 katı 0,31). (b) D9 + RÜZGÂR (T8) ÖLÇÜLEMEDİ: ABD 2023 n 870 -%1,0 (güç %52), ABD 2024-26 n 1.556 -%1,1 TUTMADI, BIST 2 / 383. (c) YALNIZ RÜZGÂR, günün en güçlü adayı ama cetveli geçmedi: ABD 2024-26 n 5.873 +%3,6 [+1,9; +5,4], sıra 0,516, iki yarı +2,3 / +4,8, PORTFÖY ŞARTI TUTMADI (+%97 vs plasebo p90 +%151); ABD 2023 n 2.001 +%2,8 [-0,3; +5,7] alt uç ve portföy tutmadı; +%100 katı 1,35 [1,25; 1,44] / 1,39 [1,07; 1,59], -%50 katı 0,97 [0,82; 1,10] / 1,03 [0,90; 1,15]: SEÇİCİ'ye yakın ama -%50 üst ucu 1'i aşıyor -> YOK; BIST 2024-26 +%1,0 TUTMADI. Etiket (ana model düzeltmesi): ajanın 'İZ DEĞİL (AVR verisi yok)' etiketi kurala aykırı; AVR sektör verisi olmadan karar en fazla ABD-ADAY olabilir, ABD'de de portföy şartı tutmadığı için (c) = 'ABD TUTMADI (portföy şartı), AVR ÖLÇÜLEMEZ'; kesinleşmiş iz değil ama kapanmış da değil. Bilgi (çoklu karşılaştırma, tercil dengesiz): rüzgâr orta + güçlü tercil ABD 2024-26 TUTAR (+%5,3 / +%9,7), ABD 2023 n 270 / 50 ölçülemedi; BIST orta tercil iki dönemde tutar. Eski Ç37 '%56-61 yön ADAY' doğrulanmadı. T8 önerisi: D9 etiketi üretimden kaldırılsın (Cemal kararı). Denetim (ana model): (c) ABD 2023 / 2024-26 (n 2.001 / 5.873; +%2,84 / +%3,58; sıra 0,513 / 0,516; katlar 1,39 / 1,03 ve 1,35 / 0,97) satır verisinden yeniden üretildi, tuttu; hangi şartın düştüğü JSON'dan doğrulandı (s_port False; 2023 s_fark False)."),
    _ik_k("Ç182", "2026-11-15", "TERSTEN PARMAK İZİ (Cemal: 'büyük mumdan geriye git, önceki mumların dizilimi / boyu / fitili / eğimi; bölge profili bul, sonra o profilden büyük mum olasılığını ölç'): KEŞİF ABD + AVR 2016-22 (B1 tek günlük büyük mum >= 3 x ATR250 ve |getiri| >= 2σ; BH2 20 günde çok günlü |ln| >= max(%15, 3σ√20); 30 ölçeksiz önceki-pencere ölçüsü vs aynı ay / σ250 ondalığı / likidite eşli rastgele kontrol x5; d, AUC, BH) -> en çok 3 koşullu kurallar P1-P3 (B1), H1-H3 (BH2) ön kayıtla donduruldu -> DOĞRULAMA ileriye doğru 2023 / 2024-26 (ABD, AVR karar; BIST bilgi); 40 kör grafik", "TERS_PARMAK.py", "Cemal: 'sıkışma tanımın rastgele bölge seçiyor; tersten gidelim; su yolunu bulur gibi: çölde engelde birikip sonra birikmiş potansiyelle hızlı akış'", "Keşif koşusu 05:32 (panel 2023-01-01'de kesik: doğrulama etiketleri keşifte görülmedi; commit 9a66102 05:36) < ön kayıt B 37934b8 05:38:10 < doğrulama 05:38:14 (cefcc8a 05:49); kontrol kapısı geçti", "", 0, cikti="arastirma_cikti/ters_parmak/ (TERS_KESIF_RAPOR.md, TERS_ON_KAYIT_B.md, TERS_RAPOR.md, TERS_ORNEK_40.pdf + anahtar)", notu="BULGU: büyük muma has bölge profili VAR ama Cemal'in hipotezinin TERSİ: büyük mumdan önceki bölge KÜÇÜK mumlu sessiz bölge değil, zaten BÜYÜMÜŞ mumlu bölge. Keşif (B1, 17.735 büyük mum vs 88.675 kontrol): en ayırıcı ölçüler son mumun boyu (olay 1,31 x ATR vs 0 kontrol 1,13; d +0,26, AUC 0,60), 250 gün aralığındaki konum (tepeye yakın, d +0,18), son günlerde küçük mum OLMAMASI (kucuk_son d -0,18; küçük mum dizisi d -0,14); hacim kuruluğu, fitil, gövde ve sessiz gün oranı ayırmıyor (d ~0); yukarı / aşağı büyük mum öncesi profil hemen hemen aynı (yön bilgisi yok). Küçük mum ölçüleri hep NEGATİF yönde: küçük mumlu bölge büyük mum olasılığını DÜŞÜRÜYOR (Ç174 / Ç176 ile tutarlı, bu kez tersten). DOĞRULAMA (ileriye doğru, 2023 / 2024-26): P1 = son mum >= 1,22 x ATR250 VE konum_250 >= 0,81 VE 40 günde küçük mum dizisi <= 1: PARMAK İZİ VAR (BH q 0,001): KAT ABD 2023 1,69 [1,55; 1,90] n 3.145, ABD 2024-26 1,62 [1,51; 1,76] n 16.258, AVR 2023 1,30 [1,13; 1,52], AVR 2024-26 1,27 [1,18; 1,37]; duyarlılık %21-44 (büyük mumların dörtte biri ile yarısı bu profilden); ilk 5 gün KAT 1,4-2,1; BIST (bilgi) 2,6-2,9. P2 (son mum büyük VE 120 günde düşüş yok) VAR (KAT 1,54 / 1,54 / 1,19 / 1,20); P3 (son mum büyük VE 40 gün eğim yukarı) EMARE (AVR 2023 alt uç 0,99). YÖN: profil günlerinde yukarı payı %49 vs eş %54 (ABD): profil yönü söylemiyor, hatta hafif aşağı. 60 GÜN GETİRİ (ORTAK CETVEL, bilgi): P1 eşli fark ABD -%0,2 / +%0,5, AVR +%0,1 / +%0,8, sıra 0,50-0,52: para kazandırmıyor; bu bir OYNAKLIK tahmini, getiri izi değil. BH2 (çok günlü, Cemal'in EUKYO tipi örneği): H1 = 5 gün bandı geniş VE 120 günde sert düşüş VE 250 gün dibine yakın: EMARE (BH q 0,52): ABD 2023 KAT 3,16 [2,66; 4,11] n 1.473, 2024-26 1,69 [1,43; 2,07]; AVR n 253 / 1.5 aralık 1'i kapsıyor; duyarlılık %15-24; yani çökmüş, geniş bantlı hisse yine büyük hareket yapıyor (piyango ile aynı aile); H2 / H3 duyarlılık < %7, ÖLÇÜLEMEDİ. YORUM: 'su birikip yolunu bulur' benzetmesi bu veride doğrulanmadı; veri 'hareket hareketi doğurur' diyor (oynaklık kümelenmesi, bilinen etki); sessiz bölge büyük hareketin habercisi değil, tersine freni. KÖR SET: TERS_ORNEK_40.pdf (20 P1 günü + 20 kontrol, anahtar ayrı) Cemal'in gözü için. Denetim (ana model): doğrulama KAT'ları P1 ABD 2024-26 1,62, P1 AVR 2023 1,30, P2 ABD 2023 1,54, H1 ABD 2023 3,16 profil_gunleri satır verisinden birebir; keşif son_mum d 0,23 (ana model, kırpmasız) vs 0,257 (rapor, %1-%99 kırpılmış): kaynak kırpma, ajan doğruladı; karar değişmez; ön kayıt sırası tuttu; yasak dosyalar değişmedi. SINIR: hayatta kalma yanlılığı; eşler σ250 ondalığında (anlık oynaklık eşlenmedi: P1'in bir kısmı bilinen kümelenme); komisyon yok; BIST ±%10 sınırı B1'i bozar (BH2 bilgi)."),
    _ik_k("Ç183", "2026-11-15", "CEMAL TANIMLI SIKIŞMA S4 (FENER itirazı üzerine): 15 gün küçük mum (250 gün %20 yüzdeliği) + dar Bollinger (BB 20,2σ genişliği 250 gün %20 yüzdeliği) + YATAY (|net| <= %3, bant <= %8 / %6, aşağı açılış payı <= %50) + uzunluk ((i)+(ii) >= 10 ardışık gün); ileri ölçüm: B1 / BH2 KAT (eş 1 σ250; eş 2 anlık / 250 oynaklık oranı), zaman, yön, ORTAK CETVEL 60 gün, yönsüz işlem; BIST bilgi, ABD + AVR karar; Cemal'in gözü için S4 bölge listesi", "SIKISMA_CEMAL.py", "Cemal (FENER grafiği): 'kod 3-16 Aralık'ı seçmiş, mumlar küçük ama kayıyor ve Bollinger en geniş yerinde; asıl sıkışma 14 Ekim - 7 Kasım'", "Ön kayıt SIKISMA_CEMAL_ON_KAYIT.md (git 0370788 08:12:14, koşu 08:12:20; mühür 2533e1f0; FENER tanı kontrolü ön kayıtta, eşik oynanmadı); sonuç 1efea57", "", 0, cikti="arastirma_cikti/sikisma_cemal/ (RAPOR, BOLGE_LISTESI_S4.md)", notu="ÖLÇÜLEMEDİ (dört karar hücresinde n 467-843 < 1.000); haberci kanıtı yok. S4 olayı S1'den 2-4 kat az (ABD 843 / 787, AVR 513 / 479, BIST 83 / 961); S4 ile S1 büyük ölçüde farklı bölgeler (aynı gün payı %16-35). FENER: Aralık bölgesi doğru dışlandı (net -%10, BB yüzdelik 0,70); Cemal'in 14 Eki - 7 Kas bölgesi YAKALANMADI: (iv) uzunluk koşulu (15 günlük mum ortalaması ve 20 günlük BB bölgeden önceki düşüşü içerdiği için ancak 31 Ekim'den sonra sağlanıyor, ardışık 3 gün < 10); S4 25 bardan kısa sıkışmayı tanımı gereği kaçırıyor; eşik oynanmadı, tasarım hatası ana modelin (IK_HATA). KAT 2023+: B1 ABD 1,01 [0,91; 1,14] / eş 2 1,10 [0,99; 1,21], AVR 0,92 / 0,88; BH2 ABD 0,48 [0,14; 0,86], AVR 0,53 (taban %0,4-1,3, aralık geniş); B0 (göreli) 1,34-1,48 eş 1, eş 2 ile ~1 (tanımsal). İlk büyük gün medyan 10. gün [5; 16], eşlerle aynı; yön payı ABD %51 / eş %48, AVR %54 / %45 (belirgin değil). 60 gün eşli +%0,1..+%1,3 (0'ı kapsar); P(-%50) ABD eşin 0,39-0,42 katı, P(+%100) 0,51-0,66 katı: S4 hisseleri iki uçta da daha sakin; yönsüz işlem TUTMADI. Denetim (ana model): ABD 2023+ B1 1,01 (%16,9 / %16,7), BH2 0,48, B0 1,44; AVR B1 0,92, BH2 0,53, B0 1,34 satır verisinden yeniden üretildi, tuttu; FENER elle sayıları tuttu (mum / ATR 0,60 vs 0,74 tanım farkı). KARAR CEMAL'DE: (iv) uzunluk koşulu bölge içi ölçülerle mi sayılsın (yeni ön kayıt)?"),
    _ik_k("Ç184", "2026-11-15", "S5 ÖBEK SIKIŞMASI (Cemal'in üç grafiğinden): 15 bar, en büyük 1 mum (zıplama) hariç MEDYAN mum <= 0,75 x ATR250, 1 uç gün hariç kapanış bandı <= %8 (BIST) / %6, eğim -%2..+%10, aşağı açılış <= %50, BOLLINGER ŞART (BB 20,2σ genişliği 250 gün yüzdeliği <= 0,20); iki sınıf: DİP (konum120 <= 0,25, tepeden <= -%10) ve YOL ÜSTÜ (SMA50 üstü ve yükselen, konum120 >= 0,60, taban korunuyor); önce TASARIM SINAMASI (3 seçmeli + 4 seçmemeli örnek x 2 fiyat kaynağı, 72 noktalı ızgara), sonra ön kayıt ve ileri ölçüm; TradingView Pine göstergesi (COL_S5_OBEK.pine) kodun gördüğünü Cemal'in grafiğine basar", "SIKISMA_OBEK.py; COL_S5_OBEK.pine", "Cemal: 'öbek gibi yan yana sıkışmış mumlar, zıplama mumunu görmezden gel, Bollinger daralması bütün bölgelerde şart, yükselişteki bölge dinlenme olmalı taban korunmalı; dipte de olur; sen ayarlarını kendin yaptır koda'", "Tasarım 886a8d0 09:10 (14 / 14 sınama tuttu; en sade orta nokta seçildi) < ön kayıt b279457 09:14:36 < koşu 09:14:42 (0b3cbc0); Pine 1d2dc25", "", 0, cikti="arastirma_cikti/sikisma_obek/ (TASARIM, ON_KAYIT, RAPOR, BOLGE_LISTESI_S5.md, COL_S5_OBEK.pine, PINE_NASIL.md)", notu="TASARIM: FENER 14 Eki-7 Kas (DİP, karar 31 Eki), CCOLA 2-20 Eki (DİP), ENJSA 10 Tem-14 Ağu (YOL, karar 6 Ağu) seçildi; FENER Aralık, CCOLA Tem-Ağu (sınıf dışı, konum 0,28-0,31), ENJSA Oca-Şub ve Ara-Oca atlandı: 14 / 14. Cemal'in sonradan verdiği ENJSA 28 Tem-12 Eyl aralığı S5'e girmez (bant 64-79 = %23, içinde yükseliş + düşüş bacağı; yalnız 28 Tem-15 Ağu parçası sıkışma): göz ile kodun ölçeği burada ayrışıyor, Pine göstergesiyle çözülecek. OLAY: BIST 350 / 2.002, ABD 1.633 / 2.900, AVR 918 / 1.471 (2023 / 2024-26); DİP ABD 579 / 649, AVR 292 / 389. SONUÇ (B1 = 20 günde gün aralığı >= 3 x ATR250, KAT eş 1 / eş 2): S5 bütün: ABD 2023 1,13 [1,03; 1,22] / 1,21 GEÇER, ABD 2024-26 0,99 / 1,08 TUTMADI, AVR 0,93 / 0,96 ve 0,94 / 1,02 -> EMARE (tek hücre); S5_DİP: ABD 2023 1,14 [1,02; 1,35] / 1,31 GEÇER, ABD 2024-26 1,17 [1,02; 1,32] / 1,26 GEÇER, AVR 0,99 / 1,05 (n 292 / 389) ÖLÇÜLEMEDİ -> EMARE (ABD iki dönem; güç yetersiz, n < 1.000; Avrupa'da tutmuyor); S5_YOL: TUTMADI (ABD 2024-26 0,93; AVR 0,91). BH2 (çok günlü) hepsi ÖLÇÜLEMEDİ / TUTMADI. CEMAL'İN SORUSU (bölge sonundan 20 gün; olay / eş): sıkışma mumunun 2 katı BIST %91 / %72, ABD %84 / %70; 3 katı %54 / %30 ve %41 / %28; yıllık ATR'nin 2 katı %50 / %49, %51 / %48; 3 katı %8 / %9, %23 / %19: göreli büyüme var, mutlak büyük mum eşlerle aynı ya da hafif üstü. 60 gün eşli (bilgi): DİP ABD +%0,2 / +%0,0, alt uç < 0; olasılık YOK; yönsüz işlem TUTMADI. YORUM: Cemal'in tanımı rastgele bölgeleri eledi (14 / 14) ve dip sınıfında ABD'de zayıf ama iki dönemde tutarlı bir oynaklık emaresi çıktı (1,14-1,17 kat); getiri / yön yok; Avrupa'da yok. Denetim (ana model): DİP ABD 2023 1,144 (%13,7 / %11,9, n 578) ve 2024-26 1,172 (%26,0 / %22,2, n 649) satır verisinden yeniden üretildi, tuttu; tasarım < ön kayıt < koşu; Pine çevirisi Python'la 3 hissenin tam serisinde 0 gün fark (Pine TradingView'de derlenmedi, Cemal deneyecek)."),
    _ik_k("Ç185", "2026-11-15", "SEKTÖR RÜZGÂRI AVRUPA'DA (Ç181c devamı; Cemal 'sektör derle'): STOXX 600 + FTSE 250 evreni için sektor_AVR.csv (581 sembol, Wikipedia ICB; 21 sınıf: 20 süpersektör + Investment Trusts; en küçük sınıf 8 üye), D9_AVR.py = D9_YENIDEN değişmeden yalnız AVR, aynı D9_PARAM, aynı ORTAK CETVEL v1.0, satırlar (a) D9, (b) D9 VE RÜZGÂR, (c) RÜZGÂR VE D9 DEĞİL; rüzgâr sütunu 'ust' ön kayıtla sabit", "D9_AVR.py", "Cemal: 'UZUN ÇÖL ETİKETİNİ KALDIR sektör derle' (15 Kas)", "Ön kayıt D9_AVR_ON_KAYIT.md (git 4a48789 11:15:29 UTC, koşu 11:15:54; önceden yazılı dört dallı karar; kontrol listesi 14/14; eşik / sütun oynanmadı; SAPMA yok)", "", 0, cikti="arastirma_cikti/d9_avr/D9_AVR_RAPOR.md", notu="ÖLÇÜLEMEDİ; Ç181c EMARE DEĞİŞMEDİ. (c) AVR 2023 n 125 eşli fark -%1,7 [alt uç -5,9], sıra 0,449, güç %29; AVR 2024-26 n 447 +%0,9 [-0,9], sıra 0,514, portföy +%10,7 < plasebo p90 +%46,4, güç %52: iki hücre de güç yetersiz, TUTMADI yazılamaz. (a) D9 AVR n'leri Ç181a ile birebir (1.102 / 2.102, TUTMADI). (b) n 110 / 201 ÖLÇÜLEMEDİ. Olasılık: hiçbir hücre seçici / piyango değil ((c) 2024-26 +%100 katı 1,35 [0,85; 1,97], -%50 katı 1,16). Investment Trusts hiç rüzgâr almadı (fon olayı 0). Ana model 4 hücreyi satır verisinden yeniden üretti (birebir). Sıradaki: Mart 2027 kriz sonrası AVR + ABD aynı komutla; AVR n büyümedikçe karar değişmez."),
]


# ---------------------------------------------------------------- 1b) GÖREV GÜNLÜĞÜ (Cemal'in verdiği işler; indekste görünür)
# Her görev bitince buraya bir satır eklenir: tarih, istek (Cemal'in sözüyle kısa), yapılan, sonuç, durum (TAMAMLANDI / AÇIK:
# neden). Cemal: "görev verdikten sonra görevin tamamlandığını görmek", "ne oldu ne bitti, ders almam gerekiyor".
IK_GOREV: List[Dict[str, str]] = [
    {"tarih": "2026-10-24", "istek": "Fon işlem defteri: hangi gün kaç lot, dolaşım, hacim (Faz 1)",
     "yapilan": "24.526 KAP fon raporu indirildi, 22.600 ayrıştırıldı (%97,1 tuttu); defter + fon girişi testi",
     "sonuc": "Fonlar koşu fazında giriyor; fon girişi iz değil (Ç64-Ç66)", "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-24", "istek": "Ham KAP verisini sakla, güncelleme yalnız yenileri eklesin",
     "yapilan": "kapfon-veri dalı (220 MB) + artırımlı güncelleme (k9indir, k10, k9paket)", "sonuc": "Açma: python FON_IZI.py k9ac kapfon",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-24", "istek": "Fon izi nasıl bir iz, grafikte görebilir miyim; her ize ders",
     "yapilan": "FON_IZI_ders.pdf + CLAUDE.md ders kuralı", "sonuc": "İz sahiplikte, fiyat grafiğinde değil", "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-24", "istek": "TEHOL Ara 2024-Oca 2025 U şekli fon izi mi?", "yapilan": "FON_IZI_ders2_U.pdf",
     "sonuc": "U sırasında fon payı 0; U fon izi değil", "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-24", "istek": "TEHOL 7 Eki-16 Ara 2024 çölünün aynısını ben niye göremiyorum?",
     "yapilan": "K13 ölçü + arama, FON_IZI_ders3_col_olcu.pdf", "sonuc": "D13'ün eski kutuları aynısı değildi; tek eş Nis-Haz 2021; iz değil (Ç67)",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-24", "istek": "İz yok çıkarsa durma: denenen, yaklaşan, sıradaki 3 deneme, kendin dene",
     "yapilan": "CLAUDE.md kuralı; K14-K15 6 deneme; FON_IZI_ders4_tehol_denemeler.pdf", "sonuc": "6 deneme iz değil (Ç68)",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-24", "istek": "İz defterine indeks; neler iz neler değil kesinleştir; en basitten karmaşığa; indeks kendini yenilesin",
     "yapilan": "IZ_KARNE.py: 72 çalışmalık kayıt, tek cetvel (eşli taban, 4 karar hücresi), seviye 1-3'te 31 madde puanlandı, "
                "indeks IZ_DEFTERI başında otomatik; IZ_KARNE_ders.pdf",
     "sonuc": "Tek cetvelde İZ 0, ADAY 0. Eski 'GEÇERLİ' A1-A4, A13, B1 eşli tabanda tutmadı; en yakın BIST'e özgü A11/A14",
     "durum": "TAMAMLANDI (seviye 4 sistem/çıkış ve ABD olay dosyası eksik maddeler AÇIK, aşağıda)"},
    {"tarih": "2026-10-24", "istek": "Görev bitince 'tamamlandı' de, ne oldu ne bitti indekse yaz, son mesaj madde madde, iz şablonu grafikte",
     "yapilan": "CLAUDE.md kuralı + bu görev günlüğü + ders PDF'inde grafik şablon", "sonuc": "Bundan sonra her görevde uygulanır",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-24", "istek": "Kodun 'benzer' dediği 2021 bölgesinin dibi düzgün değil; Ekim 2024'ünki düzgün",
     "yapilan": "'Dip tabanı' ölçüsü (kutu barlarının dibe 2 mum yakın oranı; 2024: 0,26, 2021: 0,06); K13b tarama (eşik 0,20, önceden); "
                "tek cetvel Ç73-Ç75 + 2 kat Ç76-Ç77; FON_IZI_ders5_duzgun_dip.pdf",
     "sonuc": "Ölçü gözünü yakalıyor (2021 elendi, 2024 kaldı) ama iz değil; düzgün dip tek başına 2 katı daha seyrek, −%20'yi daha sık getiriyor. "
              "Ortalama getiriyi TEHOL'ün kendisi (+%797) şişiriyordu; TEHOL hariç +%4, medyan %0",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-24", "istek": "TEHOL 2021: 1'de aşağı yuvarlama, 2. bölge istenen, ikisi peş peşe (daha önce görmedim); "
                                     "2019 örneği: bu kadar yükseliş yeterli",
     "yapilan": "K17 'iki yuvarlama' ölçüsü (∩ sonra ∪, TEHOL 2021'e kalibre, eşik önceden); 3 deneme + önceden yazılan tur 2'de 3 deneme "
                "(sıkı yay, sektör rüzgârı, hafif silkeleme); tek cetvel Ç78-Ç83 + eşli kutu; FON_IZI_ders6_iki_yuvarlama.pdf",
     "sonuc": "Kod deseni buluyor (TEHOL 2021 dahil; BIST 735, ABD 2471 olay) ama 6 denemenin hiçbiri iz değil; hücrelerin çoğu 0,85-1,25. "
              "En yakın Ç78 ve Ç83 ABD 2023 (1,41 / 1,37), tek hücre. Başarı ölçüsü olarak 'önce +%20' Cemal'in onayıyla kullanıldı",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-24", "istek": "Eski modeller sık hata yaptı: geriye dönük test ve kodlardaki yanlışları bul, doğrula, düzelt, yeniden koştur",
     "yapilan": "6 bağımsız denetçi (cetvel, FON_IZI, şekil, çıkış/ML, üretim, eski kod); her bulgu yeniden üretildi; ~30 ölçüm hatası düzeltildi; "
                "FON_IZI (K1, K10, K13-K17, gösterge, ana), COL_DIP_TEST, COL_OBEK, COL_YOL, COL_KAZANC, COL_TESPIT, SESSIZ_ML, DOJI_KUTU, "
                "MUM_SUKUN, COL_SEKIL ve tek cetvel (41 çalışma) yeniden koşuldu; IZ_KARNE_ders7_denetim.pdf",
     "sonuc": "İZ 0 (değişmedi). Düşen iddialar: T10 getiri dayanağı ters döndü (BIST +144 vs +155, ABD 0 vs +6; yalnız ağır kayıp %9→%5), "
              "öbek ve D13 'alım oranı' üstünlüğü mekanikti, düzgün dip '−%20 daha sık' ve COL_SEKIL 'ayıran ölçüler' karşılaştırma hatasıydı. "
              "Üretimde 11 doğrulanmış hata (çıkış yalnız son güne bakıyor, bedelsiz ölçeği, AL satırı, T9, XU100 yarım bar, fon süzgeci...)",
     "durum": "TAMAMLANDI, AÇIK: üretim düzeltmeleri Cemal'in 'yaz' kararını bekliyor; 13F izin engelinde"},
    {"tarih": "2026-10-25", "istek": "TEHOL, BINBN, KTLEV, ESCAR, Euro (24 Ara 2024 hacim barı), BORLS, VERUS, MANAS koştu; Vişne, PAPIL koşmadı: "
                                     "ortak iz var mı? Bölgeleri kendin bul, test et; kodun bulduklarında koştu / koşmadı de",
     "yapilan": "12 bölge veride bulundu (Euro = EUHOL; 'Hakiş' eşlenemedi); her bölgede aynı ölçüler + fon payı + üretim D13; koşanların ortak "
                "profili sabit eşikle BIST + ABD 2016-26'da tarandı (K18, 3 + önceden yazılan 3 deneme); tek cetvel Ç85-Ç90; kodun bulduğu BIST "
                "2024-26 listesi; FON_IZI_ders7_cemal_vakalar.pdf",
     "sonuc": "Ortak iz VAR (sert düşüş → mumu ve hacmi düşüştekinden küçük dar kutu → kapanışla tavan kırılımı) ama koşmayan VSNMD ve PAPIL'de "
              "de var; evrende önce +%20 eşli tabanın 0,84-1,16'sı, önce −%20 1,05-1,49 → İZ DEĞİL. BIST 2024-26'da 1.254 sinyal: 211 koştu (2 kat), "
              "340 +%20, 638 koşmadı (eşlide oranlar aynı). Fon payı çöl sırasında ~0. Üretim D13 12 bölgenin 5'ini gördü",
     "durum": "TAMAMLANDI, AÇIK: D13'ün kaçırdığı bölgeler (BINBN, KTLEV, MANAS) için kutu başlangıcı üretim kararı ('yaz')"},
    {"tarih": "2026-10-25", "istek": "'Kazandıran kırılım + kutu dibi stop + trail' diyorsun ama rastgele hisseden / rastgele noktadan çok daha fazla "
                                     "kazandırmalı; bu test yok, burada bir aptallık var",
     "yapilan": "K19: aynı çıkış ve aynı stop mesafesiyle sistem vs aynı gün eşli hisse / rastgele hisse / aynı hisse rastgele gün (3 sinyal, BIST + ABD, "
                "2023 ve 2024-26, karar önceden); aynı girişlerde çıkış kuralı vs 120 gün tut; IZ_KARNE Ç91; FON_IZI_ders8_sistem_rastgele.pdf",
     "sonuc": "Haklı: o cümle ölçülmemişti. Giriş rastgeleden iyi değil (12/12 hücre, fark ~0; BIST 2023 +%38 = piyasa). Çıkış kuralı kazanç "
              "kaynağı değil: 120 gün tutmak ortalamada hep önde; kural yalnız yatay piyasada derin kaybı azaltıyor. Para piyasada olmaktan geliyor",
     "durum": "TAMAMLANDI, AÇIK: sistemin amacı (büyük kazananı tutmak mı, derin kaybı sınırlamak mı) Cemal'in kararı; üretim değişmedi"},
    {"tarih": "2026-10-25", "istek": "MANAS 16 Haz-28 Tem 2025 ve 20 Eki-5 Kas 2025 çöllerini bulamıyor mu? Çöl nadir; çöl bitişi (sağ ayak) rastgele "
                                     "hisseden iyi değilse her şey hikâye; çöl oluşurken kazancı ölçüyorsan yanlış",
     "yapilan": "MANAS kontrolü; K19'a sağ ayak ölçüleri (120 gün en yüksek, 250 gün 2 kat; çıkış kuralı yok) ve nadir/dar çöl sinyalleri eklendi, "
                "aynı gün eşli rastgele hisseye göre koşuldu (karar önceden); IZ_KARNE Ç92; ders 8'e sağ ayak sayfası",
     "sonuc": "Ölçülen zaten sağ ayaktı (atılımdan sonrası), çöl içi değil. MANAS Haz-Tem K18 buldu (sonra 9 kat; trail +%34'te sattı), "
              "Eki-Kas kutusu 12 gün, bulmadı; D13 ikisini de görmedi. Sağ ayak BIST'te hiçbir hücrede rastgeleden iyi değil (nadir çöl 2 kat %20,7 vs %20,5); "
              "ABD'de 3 hücre iyi, dört hücre değil",
     "durum": "TAMAMLANDI, AÇIK: sistemin amacı ve D13 kapsamı Cemal'in kararı; üretim değişmedi"},
    {"tarih": "2026-10-25", "istek": "Çölden çıkan, koşmaya başlayan hisse ile rastgele günde alınanın yolu eşit olamaz; büyük bir yanlış var; "
                                     "mumları kıyasla, kim yüzde olarak daha çok yol almış? MANAS 18 Tem-8 Ağu 2025 sağ ayağı sıradan hisseden fazla olmalı",
     "yapilan": "Kod denetimi (gün hizası, bozuk mum, ortalama/medyan); K21: her sinyalin 1-120. gün yolu ve aynı gün BÜTÜN hisseler içindeki sırası "
                "(eşleştirmesiz) + en sıkı çöl; K22: Cemal'in penceresi (çölün son günü → 15 gün) ve tavanda bekleyen alış emri; BIST + ABD, "
                "karar önceden; IZ_KARNE Ç93-Ç94; FON_IZI_ders9_sag_ayak_mum.pdf",
     "sonuc": "Kod hatası yok. Atılımdan sonra çöl hissesi aynı gün borsanın ortasında (sıra 0,45-0,53). Cemal'in penceresinde (atılım mumu dahil) "
              "çöl ÖNDE (sıra 0,57-0,66): fark yalnız atılım mumunda, o da kapanışta bilinir; tavanda bekleyen emir onu yakalasa da dolumların yarısı "
              "sahte kırılım, sıra yine ~0,5. MANAS 18 Tem-8 Ağu +%84,5 (en iyi %1) ama koşan vaka",
     "durum": "TAMAMLANDI, AÇIK: sistemin amacı ve D13 kapsamı Cemal'in kararı; üretim değişmedi"},
    {"tarih": "2026-10-25", "istek": "İşaretli MANAS bölgelerinin (13 Haz-13 Tem, 20 Eki-5 Kas 2025) her özelliğini kaydet (eğim, küçük mum, kırmızı-yeşil, "
                                     "fitiller, yakınlık, düzeni bozan, hacim, RSI, MACD); 1. evre SMA altı, 2. evre SMA üstünde dizilme, delen yok; birebir "
                                     "benzer bölgelerin yüzde kaçı yukarı / aşağı / yatay; halüsinasyon mu?",
     "yapilan": "K23: 16 ölçülü parmak izi, BIST + ABD bütün pencerelerde en yakın 100 bölge, 60 gün ±%15 yukarı / aşağı / yatay vs bütün bölgeler; "
                "K24: iki evre tarifi doğrudan kural olarak vs eşli; karar önceden; IZ_KARNE Ç95-Ç96; FON_IZI_ders10_bolge_parmak.pdf",
     "sonuc": "Şekil gerçek ve kod buluyor. En yakın 100 benzer bölge BIST 2024-26'da %62-64 yukarı (hepsi %54), BIST 2023'te %42-54 (hepsi %58); "
              "ABD'de 1,2-1,5 kat ama aşağı oranı da yüksek. İki evre kuralı eşliyle aynı (0,75-1,03). Dört hücrede tutmuyor → iz değil",
     "durum": "TAMAMLANDI, AÇIK: sistemin amacı ve D13 kapsamı Cemal'in kararı; üretim değişmedi"},
    {"tarih": "2026-10-25", "istek": "BINBN 27 Ara 2024-21 Oca 2025 de var; 1. evre düşüş (dipte olsun), 2. evre çöl (yatay, çok net küçük mum, eğim "
                                     "yatay/yukarı), 3. evre sağ ayak kod bilmeden; kodun en iyi puanladığı birebir benzerleri ver, hisse adı ve sonraki mumlar "
                                     "olmasın, ben benzer/değil diyeyim, kaçtan kaçı yukarı çıkmış",
     "yapilan": "BINBN K23'e 3. bölge (genç halka arz için düşüş ölçüsü 20 barla); K23/K24 yeniden; kör set v2: her örneğe BIST 2016-26 havuzunda "
                "düşüş <= -%30 ve eğim yatay/yukarı süzgeciyle en yakın 16 (48 grafik, adsız, çöl sonunda kesik, sonuç anahtarda gizli); ders 10'a "
                "3. bölge; IZ_KARNE Ç95-Ç96 notları",
     "sonuc": "BINBN benzerleri BIST 2023 %35 yukarı (hepsi %58), BIST 2024-26 %62 (%54), ABD 1,05-1,14 kat; K24 BINBN'i yakalıyor, sonuç değişmedi "
              "(0,74-1,04). Kör set Cemal'de",
     "durum": "TAMAMLANDI, AÇIK: Cemal'in kör set ✓/✗'i bekleniyor (sonra ✓'lerin yukarı oranı vs süzgeç tabanı, önceden yazılı)"},
    {"tarih": "2026-10-25", "istek": "BINBN'i fon almış, %1000 yükselmiş; sıradan hisseyle niye aynı kazandırsın? TERA'nın düşüşü fon krizinden, ona bakmamak "
                                     "lazım. Çöl formasyonunu fon ilişkisini bilmeden gördüm; demek ki bir hisseyi fazla alıcı olunca o bölgede öyle bir yapı oluşur",
     "yapilan": "Açıklama: 0,74-1,04 kuralın 907 sinyalinin karnesi, BINBN'in değil; BINBN'de kural 3 kez tetikledi (+%179; +%8 sonra -%89; +%49 "
                "sonra -%80); ham veride Oca 2025 92,5 -> tepe 290,8 (3 kat). K25: fon raporlarıyla çöl -> fon ve fon -> önce çöl, çölde fon var/yok, "
                "fon hisseleri hariç; fon krizi dışarıda; IZ_KARNE Ç97; FON_IZI_ders11_buyuk_alici.pdf",
     "sonuc": "Görünen büyük alıcı (raporlu fon) çölden sonra daha sık gelmiyor (1,10-1,15), fon girişinden önce çöl daha sık değil (1,07), çölde "
              "fon varken sonrası daha kötü, fon hisseleri hariç çöl = eşli. Kriz dışarıda -%30 oranı %43 -> %32 ama eşli de %30",
     "durum": "TAMAMLANDI, AÇIK: görünmeyen alıcı için AKD verisi (ücretli) Cemal'in kararı; kör set ✓/✗ bekleniyor"},
    {"tarih": "2026-10-26", "istek": "AKD beleş yok mu, Midas aylık 1200 TL, gerek var mı? Kör seti işaretledim; açık: kutu içindeki tepe aşılmıyorsa risk "
                                     "çok, ✓'leri tepe aşılıp alış emri gelmiş gibi koydum",
     "yapilan": "AKD: ücretsiz, bütün hisseler için geçmişe dönük kaynak bulunamadı; kurum düzeyi (kişi değil) ve geçmiş indirme zor -> alınmadı (Cemal "
                "'gerek yok'). Kör set değerlendirmesi önceden yazıldı (kutu tepesi x 1,002 bekleyen alış, 60 gün ±%15, 250 gün 2 kat, fon krizi "
                "dışarıda); 20 işaret (7 ✓, 13 ✗) değerlendirildi; FON_IZI_ders10b_kor_set.pdf",
     "sonuc": "✓ dolan 4, önce +%15 %75, 2 kat %25; ✗ dolan 9, %89, %78; kodun en benzer 48'i %70 (havuz %61, 1,16 kat). ✓ ✗'den iyi değil -> "
              "göz izi adayı değil (ön deneme, n küçük)",
     "durum": "TAMAMLANDI (kör set sonucu sonradan geçersiz sayıldı: grafik net değildi, bir alttaki satır)"},
    {"tarih": "2026-10-26", "istek": "Sendeki grafiklerde mumun yapısı neredeyse görünmüyor; gerçek grafikte (uygulama) başka değerlendirirdim; "
                                     "üstteki gerçek grafik, alttaki çok farklı",
     "yapilan": "Haklı: kör set v2 sayfada 6 küçük kutu, Bollinger + 40 mum öncesiyle çizilmişti. Kör set v3: aynı 48 aday aynı numarayla, sayfa "
                "başına 2 tam genişlik grafik, çölden önce 20 mum, kalın gövde + fitil, altta hacim, Bollinger yok, ince SMA20; ad / tarih / "
                "rakam / sağ ayak yine yok (FON_IZI v1.10 fi_k23_kor_pdf_net, test 33); FON_IZI_kor_set_net.pdf (28 sayfa)",
     "sonuc": "İlk 20 işaretin sonucu (✓ ✗'den iyi değil) geçersiz sayıldı; değerlendirme kuralı değişmedi (önceden yazılı)",
     "durum": "TAMAMLANDI (v3 işaretlenmeden v4 yerine geçti, bir alttaki satır)"},
    {"tarih": "2026-10-26", "istek": "Bu güzel ama geriye zum lazım (ilerisi olmadan), veriyi görmüyorum; kutu yeşil mumla geçiliyor mu bilmiyorum; "
                                     "alış mumu varsa kutu çizilsin, yoksa çöl mumları yeterli değil",
     "yapilan": "Kör set v4 (önceden yazılı kural): kutu = bölgenin en yüksek / en düşüğü; alış mumu = bölgeden sonraki 60 günde kutu tepesinin "
                "üstünde kapanan ilk yeşil mum; yalnız alış mumu gelen ve sonucu ölçülebilen adaylar (her örneğe en yakın 16, toplam 48); "
                "sayfa başına bir aday: üstte 1 yıl geri zum, altta yakın görünüm + hacim, kutu çerçeveli, alış mumunda kesik. Giriş ertesi "
                "açılış, 60 gün ±%15, 250 gün 2 kat; kıyas aynı şartlı havuz (bölge başına 2.000). FON_IZI v1.11 (fi_k23_alis_mumu, "
                "fi_k23_kor4_sec/_pdf/_degerlendir, test 34); FON_IZI_kor_set_v4.pdf (52 sayfa), k23_kor4_anahtar.csv, k23_kor4_havuz.csv",
     "sonuc": "Set Cemal'de; sonuç işaretlerden sonra açılır (anahtar gizli)",
     "durum": "TAMAMLANDI (işaretler bir alttaki satırda değerlendirildi)"},
    {"tarih": "2026-10-26", "istek": "İşaretli PDF'i indirilenlerimden sen bakar mısın, yüklersem limit gidiyor (Drive'a yükledim)",
     "yapilan": "Drive'daki 'FON_IZI_kor_set_v4 (2).pdf' indirildi; 50 sayfadaki el çizimi işaretler (PDF Ink) tek tek okundu: 28 ✓, 14 ✗, "
                "6 belirsiz ('zor', '?', 'kararsız alış mumu', 'oransız büyük', dalga çizimi, boş); önceden yazılı kuralla değerlendirildi "
                "(fi_k23_kor4_degerlendir); k23_kor4_cemal_etiket.csv; FON_IZI_ders10c_kor_set_v4.pdf",
     "sonuc": "Önce +%15: ✓ %54, ✗ %57 (belirsizlerle %50), havuz %60; 2 kat: ✓ %29, ✗ %36, havuz %42; kapanışta alışta ✓ %68 vs havuz %63. "
              "Göz izi değil. Gözün ✓'de geç gelen, büyük ve hacimli alış mumu, dar ve dipte kutu seçiyor; sonrası farklı değil",
     "durum": "TAMAMLANDI, AÇIK: sıradaki denemeler (alış mumu boyu/hacmi, gecikme) kapalı konuya (giriş onayı/hacim) dokunuyor -> Cemal'in kararı"},
    {"tarih": "2026-10-26", "istek": "KZBGY 4 Şubat - 13 Mart 2025 bölgesinin parmak izini çıkar, önceki hissedekiyle karşılaştır; belki "
                                     "karşılaştırmada iz çıkar",
     "yapilan": "K26 (önceden yazılı): KZBGY kutusu 04.02-11.03 (12.03 +%10 ilk ayak, 13.03 alış mumu); MANAS x2 ve BINBN ile 16 ölçü havuz "
                "yüzdeliğinde karşılaştırıldı; dördünde ortak ölçüler profil olarak BIST + ABD'de tarandı, v4 alış mumu ile; iz çıkmayınca "
                "önceden yazılı 3 devam denemesi (sıkı, BINBN'siz, merkeze en yakın %1); IZ_KARNE Ç98; FON_IZI_ders12_ortak_parmak.pdf",
     "sonuc": "Ortak yüz: küçük mum, uzun üst fitil, orta düzeni bozan, düşük RSI. Profil sinyalleri tabanla aynı (kat 1,01-1,02, dört "
              "hücre); devam denemeleri 0,77-1,26 (1,26 n 15). İz değil",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-26", "istek": "Yalnız gerçek iz çıkınca PDF ver; iz çıkmayanları nereye koyarsan koy; her mesajdan sonra neden 'yapıtlar' "
                                     "yazısı görüyorum",
     "yapilan": "CLAUDE.md ders kuralı değişti: PDF yalnız gerçek izde; iz çıkmayanda dosya gönderilmez, sonuç mesajda birkaç satır + "
                "IZ_DEFTERI/IZ_KARNE. 'Yapıtlar' = gönderilen dosya kartları; artık yalnız istenince / işaretlenecek dosyada / gerçek izde",
     "sonuc": "Kural yazıldı", "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-26", "istek": "Her mesajdan sonra 'Yapıtlar · 2' görüyorum, yeni bir şey mi; ikisini sil",
     "yapilan": "Kart uygulamanın konuşma düzeyindeki listesi; Cemal'in onayıyla 22 Ekim'in iki eski işaretleme sayfası (Çöl İşaretleme, "
                "Çöl İşaretleme Kapalı) kalıcı silindi",
     "sonuc": "İki sayfa silindi", "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-26", "istek": "Yeni konuşmada bir şey yazmadan devam edebilir misin, her şeyi hatırlayacak mısın",
     "yapilan": "CLAUDE.md'ye yeni oturum kuralı (indeksin görev günlüğü + açık kalanlardan devam); açık kalanlara DRIVE eşitleme maddesi",
     "sonuc": "Yeni konuşma sohbeti hatırlamaz, repodaki kayıtları okur; ilk mesaj kısa bir cümle olmalı", "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-26", "istek": "Ortam seçimi; işlenmiş veriyi koy; hiçbiri iz bulmadı, nasıl bir yol izlemeliyim, web'de düşün",
     "yapilan": "Ortam: cone. islenmis-veri dalı (V_BIST, V_ABD, K25 fon tabloları; 80 MB xz parça, sha256; FON_IZI v1.14 fi_veri_paketle / "
                "fi_veri_paket_ac, CLI vpac, test 36; CLAUDE.md istisna 2). Web: grafik desenleri maliyet sonrası örneklem dışında nadiren "
                "kazandırıyor; BIST'te içeriden alım ve bilanço sürprizi (PEAD) için akademik kanıt var, 52 hafta zirvesi zayıf",
     "sonuc": "Yol önerisi açık kalanlarda (YOL)", "durum": "TAMAMLANDI (Cemal: '1 + 3, ölçütü değiştir', bir alttaki satır)"},
    {"tarih": "2026-10-26", "istek": "1 + 3 ile başla (KAP içeriden alım; çöl + içeriden alım), ölçütü değiştir",
     "yapilan": "Yeni ölçüt FI_OLCUT (eşli fark + ay kümeli %95 aralık + hücre içi sıra + eşli rastgele portföy; rastgele olay sağlamasıyla "
                "iki yanlılık düzeltildi) CLAUDE.md'ye yazıldı. KAP Pay Alım Satım Bildirimi 2022-07 -> 2026-10 indirildi, tablo + PDF "
                "ayrıştırıldı (6.637 bildirim); K27 + önceden yazılı 3 devam; IZ_KARNE Ç99; testler 37-38",
     "sonuc": "İz değil: içeriden net alımdan sonra hisse 60 günde eşlerin %2,6-4,5 gerisinde; çölde alım, yönetici, kümeli, destek dışı "
              "alımlar da tutmadı", "durum": "TAMAMLANDI (Cemal: 'başla', bir alttaki satır)"},
    {"tarih": "2026-10-27", "istek": "Başla (yol 2: bilanço sürprizi)",
     "yapilan": "K28: BIST açıklama günleri KAP 'Finansal Rapor' listesinden (konu kodu bulundu), ABD Nasdaq bilanço takviminden (analist "
                "sürprizi dahil); bilanço tepkisi dilimleri, çöl + iyi sürpriz, ABD analist sürprizi; kötü sürpriz için ayna (kaçınma) "
                "ölçütü ABD görülmeden repoya işlendi; önceden yazılı 3 devam; en tutarlı aday için önceden yazılı örneklem dışı (BIST "
                "2016-22); IZ_KARNE Ç100; test 39",
     "sonuc": "İz değil. İyi sürpriz BIST'te ve ABD 2023'te artı ama ABD 2024-26'da eksi; kötü sürpriz yalnız BIST'te eksi; çöl + güçlü "
              "sürpriz 2023-26'da dört hücrede artıydı ama 2016-22 BIST'te tersine döndü",
     "durum": "TAMAMLANDI, AÇIK: sıradaki yol Cemal'in kararı"},
    {"tarih": "2026-10-27", "istek": "Fon krizi döneminde BIST kötü olacak; Ağustos sonundan sonraki çölü dikkate alma, olağanüstü durum",
     "yapilan": "Denetlendi: yeni ölçüt fiyatları 31.08.2026'da kesiyor; K27 / K28'de ölçülen en geç giriş 4-5 Haziran 2026, 31 Ağustos "
                "sonrası ölçülen olay 0 (60 günü krize taşanlar da dışarıda). Kural CLAUDE.md test standardına yazıldı",
     "sonuc": "Sonuçlar krizden etkilenmemiş; K28'in 2016-22 tersine dönüşü kriz dışı bir dönem", "durum": "TAMAMLANDI"},
    {"tarih": "2026-10-27", "istek": "Yine de devam et; hevesim kalmadı, yıllardır uzman / sinyal grupları para kazandığını söylüyordu, "
                                     "hepsi yalan mıymış",
     "yapilan": "Öneri b + a: K29 risk süzgeci (K24 çöl sinyalleri, kötü bilanço / A11 / A14 işaretleri, BIST + ABD, yeni ölçüt + kaçınma "
                "ölçütü) ve önceden yazılı 3 devam; IZ_KARNE Ç101",
     "sonuc": "İz değil: işaretli ve temiz adaylar eşlerinden ayrışmıyor", "durum": "TAMAMLANDI (Cemal: ABD izni, bir alttaki satır)"},
    {"tarih": "2026-10-27", "istek": "ABD verisi için izin vereyim, devam edelim; BIST hep manipülasyon",
     "yapilan": "SEC Form 4 veri setleri (2016-01 -> 2026-03) indirildi (e-posta yalnız indirmede, koda yazılmadı); K30: alım, büyük, "
                "yönetici, kümeli, çölde alım, yeni ölçütle; önceden yazılı 3 devam (çölde yönetici, çölde >= 100 bin $, 2016-22 örneklem "
                "dışı); IZ_KARNE Ç102",
     "sonuc": "İz değil: ABD içeriden alım 2023-26'da eşlerle aynı; çölde alım 2023'te güçlü göründü ama 2016-22'de tersine döndü",
     "durum": "TAMAMLANDI (Cemal: analist izleri, bir alttaki satır)"},
    {"tarih": "2026-10-27", "istek": "En başarılı analistlerin izlediği 4 veri (seyrelme, içeriden satış, nakit tükenmesi, kurumsal sahiplik): "
                                     "yapılanları ayıkla, yapılmayanları dene; tıkanırsan çözüm bul, bulamazsan başka veriyi irdele",
     "yapilan": "Ayıklandı: içeriden alım (K27, K30) ve BIST fon sahipliği (K10, K25) yapılmıştı. K31: SEC Form 4 satışları, SEC finansal "
                "tablo veri setleri (seyrelme, nakit pisti; pay kalemi hatası sonuç görülmeden düzeltildi), 13F tıkandı (CUSIP eşlemesi) -> "
                "FINRA açığa satış; önceden yazılı 3 devam (iflas profili, temiz çöl, çöl tuzağı); IZ_KARNE Ç103; test 40",
     "sonuc": "İz değil: dört analist ölçüsü ABD 2023-26'da eşlerden ayrışmıyor; seyrelen / nakdi biten şirketler ortalamada biraz iyi "
              "(birkaç sıçrayan hisse), sıra ortada", "durum": "TAMAMLANDI (Cemal: a, sade portföy ölçümü; bir alttaki satır)"},
    {"tarih": "2026-10-27", "istek": "a ile devam et, sade portföy ölçümü",
     "yapilan": "K32: çöl adayları 10 yuvalı portföyde 60 gün tut ve çıkış kuralıyla; piyasa (eşit ağırlık), rastgele giriş (50 tohum) ve "
                "rastgele giriş + aynı çıkışla karşılaştırma; BIST/ABD x 2016-22/2023/2024-26; kurallar ve karar önceden; 3 devam (temiz, "
                "likit, 250 gün tut); IZ_KARNE Ç104; test 41",
     "sonuc": "Kullanılabilir düzen değil: çöl portföyü yalnız BIST 2023'te piyasayı geçti; 2024-26'da iki pazarda da piyasanın çok altında "
              "(BIST +%29'a +%114, ABD +%42'ye +%89) ve düşüşü daha derin. Rastgele 10 hisse bile çöl adaylarından iyi",
     "durum": "TAMAMLANDI (Cemal: sıçrayan hisseler, bir alttaki satır)"},
    {"tarih": "2026-10-27", "istek": "Piyango gibi sıçrayan hisseler neden ayrışıyor araştır; ABD nakit tükenmesi grubunda iyi çıkanları iyi "
                                     "yapan izi bul",
     "yapilan": "K33: 12 fiyat/hacim özelliği, keşif 2016-22, test 2023 / 2024-26, BIST + ABD; çöl içi, çöküş profili. K33-B: ABD nakit "
                "tükenmesi grubunda iyi çıkan / öteki profili (AUC) + şirket verisi (nakit / değer, yakma hızı, nakit akışı iyileşmesi, "
                "içeriden alım); hayatta kalma denetimi (SEC bildirim kesilmesi); IZ_KARNE Ç105-Ç106; test 42-43",
     "sonuc": "Genel: sıçrayanın izi 'ucuz, sığ, oynak' olmak ama aynı iz çöküşü de getiriyor, İZ DEĞİL. Nakit grubunda en küçük şirketler "
              "test dönemlerinde belirgin iyi (ABD-ADAY şartı tuttu) ama veri yalnız hayatta kalanları içeriyor; bu şirketlerin %26-52'si "
              "bildirimi kesmiş, bizde %0 -> GEÇERSİZ",
     "durum": "TAMAMLANDI (Cemal: batanlar da katılsın, bir alttaki satır)"},
    {"tarih": "2026-10-27", "istek": "Batanlar neden test edilmiyor; 2021'de parmak izine uyan bütün hisselerin listesi yok mu, varsa katılsın",
     "yapilan": "SEC finansal tablo veri setinden 2021-23'te nakdi 4 çeyrekten kısa yeten bütün şirketler (batanlar dahil, 22.670 bildirim) "
                "çıkarıldı; akıbet = bildirimin kesilmesi; nakit büyüklüğüne göre beşte birler; ücretsiz fiyat kaynakları denendi",
     "sonuc": "Liste var. Nakdi bitenlerin %20'si 1 yılda, %36'sı 2 yılda bildirimi kesiyor (en küçük üç dilimde %42-49); bizim evren bu "
              "küçüklerin yalnız %1-2'sini içeriyor. Batanların fiyatı Yahoo / Stooq'ta yok (SIVB, FRC, WEWK boş); Tiingo, EODHD, Polygon "
              "anahtar istiyor. Fiyat olmadan r60 ölçülemez",
     "durum": "TAMAMLANDI (Cemal: Tiingo ücretsiz hesap açtı, bir alttaki satır)"},
    {"tarih": "2026-10-27", "istek": "Tiingo anahtarı verildi; batanlar dahil test",
     "yapilan": "K34: SEC'ten bütün nakdi biten şirketler (batanlar dahil), eski kodları 1.303 kapak sayfasından, bugün işlem görenler "
                "Yahoo'dan (2.246), batanlardan rastgele 450'si Tiingo'dan (saatte 45 istek, ~9 saat; sunucu yeniden başladı, kaldığı "
                "yerden sürdü); ağırlıklı eş farkı; anahtar .env'de, repoda yok; IZ_KARNE Ç107; test 44",
     "sonuc": "İz değil: küçük nakdi biten şirket, yalnız hayatta kalanlarla +%9-11 iyi görünüyordu; batanlar eklenince +%6-8'e iniyor ve "
              "2024-26'da tipik küçük şirket eşlerinden kötü (sıra 0,48). Ortalamayı birkaç piyango hissesi çekiyor",
     "durum": "TAMAMLANDI (Cemal: rüzgâr, bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "Nakdi yetmeyen / batan şirketlerin arkasında rüzgâr olanlar da batıyor mu; rüzgârı olan daha iyi mi; "
                                     "patlayanların arkasında ve patlama zamanında rüzgâr var mıydı",
     "yapilan": "K35: 4.556 şirketin SIC sektörü SEC'ten (batanlar dahil); üretim D9b rüzgârı (sepet hisse hariç); 2 yılda batma oranı "
                "(Tiingo örneğine girmeyen batanlar dahil, fiyat gerekmez) ve getiri. K35-C: patlayanlarda girişte ve zirve gününde rüzgâr. "
                "Kurallar önceden; IZ_KARNE Ç108-Ç109; test 45-46",
     "sonuc": "Rüzgâr batmayı tutarlı azaltmıyor (2021-22 farkı çoğunlukla SPAC'ler; 2023-24 yok); rüzgârlı nakdi biten şirket daha iyi "
              "getiri vermiyor. Patlayanlar zirvede daha sık rüzgârlı (eşlik) ama girişte rüzgâr patlamayı önceden göstermiyor",
     "durum": "TAMAMLANDI (Cemal: sebebe bak, bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "Rüzgâr fiyattan görülünce geç kalınır, önceden nasıl bilinsin; 1 ile başla (sebebe bak), 2 ondan sonra",
     "yapilan": "K36: 22 sektör-sebep çifti önceden eşlendi (emtia, kur, faiz, CDS; Yahoo + repo cds_2022.csv); sebep sinyali z-skor; "
                "öncelik (sinyal rüzgârdan önce mi) ve FI_OLCUT getiri (hepsi / erken / erken + çöl); 3 devam (güçlü, yavaş, kaçınma). "
                "Sinyal kuralındaki aralık hatası test 47 ile sonuç görülmeden düzeltildi. IZ_KARNE Ç110; test 47",
     "sonuc": "Sebep sinyali rüzgârdan önce gelmiyor (öncü oranı 1,0-1,2); sebep sinyalinde sektör üyeleri eşlerinden iyi değil (BIST "
              "2023 -%9). Ölçülebilen sebepler de fiyat; sektörle aynı anda hareket ediyor. İZ DEĞİL",
     "durum": "TAMAMLANDI (Cemal: 2 ile başla, bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "2 ile başla (büyükler önce, küçükler sonra); para akışı tek başına yetmez; temel durum ve haber "
                                     "zamanlamasını atlama; küçük hissede likidite / sert hareket / manipülasyon riski sonucu değiştirir mi",
     "yapilan": "K37: sektörde büyük / küçük sepet sinyali; P (CMF + OBV), T (BIST temel_duz: satış ya da kâr, borç/özkaynak < 1, özkaynak "
                "pozitif; ABD SEC: pay artışı < %10, nakit sağlam), H (K28 bilanço tepkisi, yıl yıl tekrarlanabilirlik); maliyet, en kötü "
                "olay, -%30 payı; 3 devam (gevşek, yavaş, ayna); IZ_KARNE Ç111; test 48",
     "sonuc": "İz değil: büyükler öne geçtiğinde küçükleri almak eşlerini geçmiyor (BIST 2023 +%6 ama aralık 0'ı içeriyor, ABD 2023 -%6); "
              "para akışı ve temel süzgeci düzeltmiyor; haber öncesi sinyal ABD'de tekrarlıyor (1,4-1,6 kat) ama BIST'te değil; küçük hisse "
              "riski bilinince sonuç değişmez, maliyetle aleyhe döner",
     "durum": "TAMAMLANDI (Cemal: ABD'de tutanı iz say, bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "BIST öngörülemez (siyaset, fon hırsızlığı); Amerika'da tutan bütün ölçüleri iz kabul edelim, olmazsa "
                                     "Avrupa ve Çin ile karşılaştır",
     "yapilan": "Bütün kayıtlar tarandı: tek cetvel 46 sinyal (karne.csv) ve yeni ölçüt K27-K37 özetleri, ABD 2023 + 2024-26 iki hücre şartıyla",
     "sonuc": "ABD'de iki hücrede tutan ölçü YOK: tek cetvelde 0/46 (en yakın: tavan günü kaçınması 1,20 / 1,23; geride kalan + hacim artışı "
              "kaçınması 1,37 / 1,21); yeni ölçütte yalnız nakdi biten küçük şirket tuttu, o da batanlar eklenince düştü (K34). Avrupa / Çin'e "
              "taşınacak aday yok",
     "durum": "TAMAMLANDI (Cemal: üçünü de yaz, bir alttaki satırlar)"},
    {"tarih": "2026-10-28", "istek": "Üçünü de yaz: iz kuralı (Amerika ve Avrupa tutan iz; BIST bilgi; Çin sonra), Avrupa evreni, adayları 3 "
                                     "pazarda ölç; ayrıca çöl, ikili dip, ters OBO, RSI / MACD uyumsuzluk ayrı ayrı; verileri repoya kaydet",
     "yapilan": "CLAUDE.md + FI_OLCUT 'karar' = (ABD, AVR), fi_olcut_karar ortak (BIST tutarsa 'İZ + BIST'); Avrupa evreni STOXX 600 + FTSE 250 "
                "(Wikipedia listeleri, Yahoo, 581 hisse, EUR likidite 'Kur' sütunu, peni / sterlin 100x temizliği); K38 üç aday + K38-B altı "
                "şekil 3 pazarda; veri islenmis-veri dalına (V_AVR, K34 Yahoo fiyatları, SEC özetleri, K28 / K30 / K31 tabloları, SIC, "
                "sürücüler, Avrupa listesi; Tiingo verisi lisans gereği repoya konmadı); IZ_KARNE Ç112-Ç113; test 49-51",
     "sonuc": "Dokuz ölçünün hiçbiri ABD + Avrupa dört hücrede tutmadı. BIST'in kaçınma izleri (tavan, hacimli düşüş) ABD'de ters, "
              "Avrupa'da sıfır. Blok hacimli taban ABD 2024-26'da tuttu (+%15) ama 2023'te değil. Şekiller ve uyumsuzluklar üç pazarda da "
              "eşlerinden ayrışmıyor",
     "durum": "TAMAMLANDI (Cemal: Amerika öncü, bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "Amerika verileri öncü, Avrupa ve Asya takip eder; Amerika'da asıl izi ararken üstüne git, her olasılığı "
                                     "ayrıca değerlendir",
     "yapilan": "K39: 13 kaba sektör üç pazarda eşlendi; ABD sektör sepeti piyasayı geçince Avrupa / BIST üyeleri (8 olasılık + küçükler), "
                "ayna AVR -> ABD; FI_OLCUT 2016-22 / 2023 / 2024-26; IZ_KARNE Ç114; test 52",
     "sonuc": "İz değil: ABD sektör öne geçince Avrupa'daki aynı sektör sonraki 60 günde eşlerinden ayrışmıyor (bütün olasılıklar -%0,5 .. "
              "+%1,3); BIST de öyle. Avrupa ABD'yi aynı gün / ertesi açılış fiyatlıyor, gecikme yok",
     "durum": "TAMAMLANDI (Cemal: saat farkı, bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "Avrupa ile Amerika arasında gün değil saat farkı mı; Amerika'da yükseliş Avrupa'da ne kadar gecikmeli; "
                                     "gecikme esas alınıp alım yapılır mı, kazanılır mı",
     "yapilan": "K40: günlük hisse düzeyi (ABD güçlü gün / sektör günü -> Avrupa ertesi gün boşluk, gün içi, 5 gün; ayna) 2016-26 + saatlik "
                "endeks (S&P geç seansı -> Euro Stoxx 50, DAX, FTSE ertesi gün boşluk / ilk saat / gün) son 730 gün; endeks açılış kotasyonu "
                "denetimi; IZ_KARNE Ç115; test 53",
     "sonuc": "Gecikme saat değil dakika: ABD'nin gece hareketi Avrupa'nın açılış boşluğuna giriyor (+%0,2 hisse, DAX +%1,1); açılıştan "
              "sonra alınabilir fazla yok ya da tutarsız (gün içi +%0,03 .. +%0,24). Kalıntı: sektör düzeyinde 5 günde +%0,3-0,5, iki "
              "dönemde, maliyet sonrası küçük. İZ DEĞİL",
     "durum": "TAMAMLANDI (Cemal: d ve e, klasikler, kalıntı; bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "d ve e seçeneklerini yap; K40 kalıntısını dış örnekle ölç; eski formasyonlar (Bollinger, RSI, MACD, Fibo) "
                                     "başarılı mı; benim çölüm halüsinasyon mu; ya sen hata yapıyorsun görmüyorsun",
     "yapilan": "K41: A klasik 8 kural, B rüzgâr sürekliliği (+ çöl + rüzgâr), C ABD çöl adayı olay süzgeci, D K40 kalıntısı 4 hücre + maliyet; "
                "üç pazar; IZ_KARNE Ç116-Ç119; test 54. Hat kontrolü (Ç120): pozitif / yarı pozitif / negatif sinyaller; bağımsız kod "
                "denetimi (ayrı model) K38-K41 + ölçüt fonksiyonları",
     "sonuc": "Klasik kurallar üç pazarda eşlerinden ayrışmıyor (tek kalıntı ABD Fibonacci ortalaması, tipik olay değil); rüzgâr = üyelerin "
              "momentumu, üstüne katkı yok; ABD olay süzgeçleri yalnız 2023'te artı; K40 kalıntısı dört hücreden ikisinde. Hat kontrolü: "
              "gerçek iz her hücrede yakalanıyor, rastgele sinyal 120 hücrede 0 yanlış iz. Bağımsız denetim: ağır hata yok, 4 küçük "
              "düzeltme, hepsi yeniden koşuldu, karar değişmedi",
     "durum": "TAMAMLANDI (Cemal: 'kesin hata yapıyorsun', bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "Hiçbir yerde iz yok, o zaman kesin sen hata yapıyorsun",
     "yapilan": "K42: literatürün kırk yıllık üç etkisi (momentum 12-1, 1 ay tersine dönüş, küçüklük) ham ve eşli cetvelle üç pazarda; "
                "beklenti önceden yazıldı; IZ_KARNE Ç121",
     "sonuc": "Hat bilinen etkileri görüyor: ham cetvelde 27 hücrenin 21'i artı (momentum ABD +%2-8, BIST +%7-10; tersine dönüş ABD +%4-8; "
              "küçüklük ABD +%7-22, BIST +%12-39). Eşli cetvel bunları tasarım gereği siler; küçüklük eşlide bile ABD'de tutar (hayatta "
              "kalma payıyla). 'İz yok' değil: bildiğimiz izlerin üstüne yenisi bulunamadı",
     "durum": "TAMAMLANDI (Cemal: 'çölü boş ver, alınabilir iz var mı', bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "Çölü boş ver. Bir iz var mı, bu izle alım satım yapıp kâr eder miyiz? Tek başına kazandıran (Fibo, trend) "
                                     "varsa kaydet. Yükselişte alınca zarar az, dipte dönüş varsayımıyla alınca kötüleşti",
     "yapilan": "K43: 23 sinyal (trend / dip / öteki) üç pazar üç dönemde, piyasaya göre fark + maliyetli 10 yuvalı portföy (piyasa ve "
                "rastgele kıyası), karar önceden; IZ_KARNE Ç122; test 55. K42 / K43 ham tabanı medyan hatası bulunup ortalamaya çevrildi, "
                "ikisi yeniden koşuldu (Ç121 düzeltme notu)",
     "sonuc": "Alınabilir iz yok: 23 sinyalden hiçbiri ABD + Avrupa'da tutarlı olarak piyasayı geçmiyor; tek aday küçüklük (hayatta kalma "
              "yanlılığıyla şişkin). Trend sinyalleri zarar ettirmiyor ama piyasayı geçmiyor; dip sinyalleri ABD'de yalnız 2023. Daha önce "
              "söylediğim 'BIST momentum +%7-10' medyan hatasıydı, geçersiz",
     "durum": "TAMAMLANDI (Cemal: küçüklük son yıl batanlar dahil, bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "Bu küçüklük son yılda yüzde kaç; batanları net eklersen",
     "yapilan": "Yıl yıl: (A) E3 küçüklük, V_ABD (yalnız hayatta kalanlar) ortalama / ortanca / kazanan payı; (B) K34 nakdi biten ABD şirketleri "
                "en küçük beşte bir, batanlar dahil (Tiingo örneği, ağırlıklı) ve hariç, eşit ağırlıklı piyasaya göre 60 gün farkı",
     "sonuc": "Hayatta kalanlarda ortalama büyük (2024 +%18, 2025 +%20, son 12 ay +%13,5) ama ORTANCA -%4 .. 0, kazanan payı %40-50: "
              "birkaç piyango hisse. Batanlar dahil en küçükler: 2023 +%1, 2024 +%2,4, 2025 -%0,2, 2026 -%9; son 12 ay -%2,4 (hayatta "
              "kalanlarla +%0,9); kazanan %31, -%50 altı kayıp %13. Son yıllarda batanlar henüz tam görünmüyor (sansür), gerçek daha kötü",
     "durum": "TAMAMLANDI (Cemal: INTEM bölgesi, bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "INTEM grafiği: bu bölgenin parmak izini çıkart; bu bölgeler özel; iz çıkacaksa burada çıkar; birebir uyan "
                                     "bölgelerde bütün olasılıklarla test et",
     "yapilan": "K44: bölge 28 Eyl - 9 Eki 2026; 8 ölçülük parmak izi (20 ve 10 bar), üç pazarın bütün pencerelerinde yüzdelik bandıyla "
                "birebir eşleşme (toplam ~1.000 bölge), eşli fark, piyasaya fark, r20/60/120, önce +%20 / -%20, maliyetli portföy; IZ_KARNE "
                "Ç123; test 56",
     "sonuc": "İz değil, piyasayı geçmiyor: eşleşen bölgeler sonraki 60 günde eşlerinden ve piyasadan ayrışmıyor (18 hücrenin 17'sinde "
              "portföy piyasanın altında). INTEM'in kendisi bölgeden sonra -%22. Bu bölge 'küçük mumlu çöl' değil: mumlar büyümüş, düşüş "
              "sert; 10 günlük duraklama",
     "durum": "TAMAMLANDI (Cemal: 60 gün değil, +%8 ve kutu çıkışı; bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "60 gün bakarsan orası küçük bir durak; bölgenin altı ve üstü çıkışlarını hemen ara; bana +%8 yükseliş iz; "
                                     "büyük hedef asla olmaz, 60 günlük hedef olamaz",
     "yapilan": "K45: INTEM bölgelerinden sonra ilk +-%5 / 8 / 12 (20 gün), kutu çıkış yönü, kırılımda al kuralı; düz rastgele taban oynaklık "
                "yüzünden şişince oynaklık eşli taban (ilk koşu saklandı); dönem sınaması ve gerçekçi işlem getirisi; IZ_KARNE Ç124; test 57",
     "sonuc": "Önceden yazılı kural tutuyor (ABD +11, AVR +15 puan, aralık artı) -> KISA İZ ama ZAYIF: etki 2016-22'den, 2023-26'da ABD "
              "işlem başına +%0,2-0,3, Avrupa'da az olay, BIST'te ters (INTEM'in kendisi gibi). Oynak bölge +%8'e de -%8'e de çabuk gidiyor; "
              "+%8 hedefi tek başına iz değil",
     "durum": "TAMAMLANDI (Cemal: 'makineye öğret', bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "Tipik dönüş noktasını bul; sen ara, makineye öğret",
     "yapilan": "K46: 1,09 milyon hisse-günü, 36 özellik (K33 + K23 + bağlam), etiket 20 günde +%8 -%8'den önce, yıl yıl ileri yürüyen "
                "LightGBM (2019-26), üst %5 sinyal vs oynaklık eşli rastgele, etiket karıştırma kontrolü, özellik profili, 10 yuvalı "
                "portföy; IZ_KARNE Ç125; test 58",
     "sonuc": "Makine öğreniyor (AUC 0,6-0,7, kontrol 0,5). Üst %5 sinyal 2024-26'da ABD ve Avrupa'da rastgeleye +12 puan, işlem başına "
              "+%1-2; 2023'te +4-5 (kural eşiği 10'un altı) -> İZ DEĞİL. Portföyde avantaj kayboluyor (piyasa kadar, düşüş daha derin; "
              "BIST 2023 hariç). Tipik dönüş noktası ABD / Avrupa'da 'düşen piyasada aşırı satılmış oynak hisse', BIST'te 'yükselen "
              "piyasada güçlü trend'",
     "durum": "TAMAMLANDI (Cemal: iki bölge + sert düşüş makinesi, bir alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "ECOGR haftalık yukarı yuvarlanma ve BBIO sert düşüş -> ufak dip -> derin dip -> orta bant altı -> orta-üst "
                                     "bant arası yuvarlanma: bunlarda iz yok mu, dene; burada makine çalıştır, benim dediğim sert düşüşten sonra "
                                     "olan bir şey",
     "yapilan": "K47: ECOGR haftalık parmak izi (9 kendi-içi ölçü), BBIO günlük parmak izi (taban sonu, yuvarlanma) ve açık BBIO kuralı; üç "
                "pazar; eşli, piyasa, kısa ufuk (oynaklık eşli), portföy. K46-B: makine yalnız sert düşüş sonrası satırlarda. IZ_KARNE "
                "Ç126-Ç127; test 59",
     "sonuc": "Dört bölge kümesi İZ DEĞİL. BBIO kuralı ABD'de piyasayı geçiyor (2023 +%7, 2024-26 +%12,5; portföy +%68 / +%207) ama aynı "
              "momentum dilimindeki rastgele çökmüş hisse de geçiyor (eşli fark 0): çökmüş hisse sıçraması, kuralın kendisi değil; Avrupa / "
              "BIST'te yok. Sert düşüş makinesi: ABD'de +17-22 puan, Avrupa 2024-26'da sıfır, portföyde piyasa altı; seçtiği 'piyasa "
              "çöküşünde büyük hisse'",
     "durum": "TAMAMLANDI (devam: Cemal'in geniş metrik ve kabuk dışı istekleri, alttaki satır)"},
    {"tarih": "2026-10-28", "istek": "Makineye TradingView örneğindeki gibi çok metrik yükle; sonra: kural bizi sınırlıyor olabilir, kabuktan çık, her "
                                     "ölçünün tersini de dene, bütünü ile ele al, iz değil dediklerimizi derleyip tekrar koştur",
     "yapilan": "K48: 166 yeni ölçeksiz ölçü (toplam 204) ile makine, bütün satırlar ve sert düşüş sonrası (K48-B), portföy. K49: 203 ölçü + "
                "114 olay kümesi (1,01 milyon olay) iki yönde, pazar pazar, 2016-22'de seçim, 2023 / 2024-26'da karar, 3 karıştırmalı şans "
                "denetimi, bütün birleşimi ve portföy. K50 (sıradaki deneme): makine sinyaliyle gerçekçi portföy (günde 2, +8 / -8). IZ_KARNE "
                "Ç128-Ç131; test 62",
     "sonuc": "Hiçbiri iz değil. K48 makinesi K46'dan biraz iyi (ABD 2023 +6,9, diğer hücreler +11-12 puan) ama ABD 2023 eşik altı; "
              "portföyde ABD 2024-26 +%218 / piyasa +%89, 2023 +%11 / +%29. Kabuk dışı: seçilen ölçü sayısı şansa yakın, görülmemiş "
              "dönemde tutan 0. Gerçekçi portföy (K50): üç pazarda da piyasanın altında; işlem başına küçük artı var, para nakitte bekliyor",
     "durum": "TAMAMLANDI (devam: Cemal'in makine öğrenmesi araştırma sorusu, alttaki satır)"},
    {"tarih": "2026-10-29", "istek": "Sen mi makine öğrenmesi mi yapıyor; makine öğrenmesinin en iyi yollarını araştır: daha çok metrik mi, bir iz "
                                     "üzerinde daha çok gel git mi",
     "yapilan": "Kaynak taraması (ölçüm yok): Gu-Kelly-Xiu 2020, Kelly-Malamud-Zhou 2024, Avramov-Cheng-Metzker 2023, Jiang-Kelly-Xiu "
                "2023 (grafik resminden CNN), López de Prado 2018 (üçlü bariyer, meta-etiketleme, arındırılmış doğrulama), Bailey ve ark. "
                "(backtest aşırı uyumu), Harvey-Liu-Zhu 2016 (t > 3), McLean-Pontiff 2016 (yayın sonrası -%58); K46-K50 ile kıyas",
     "sonuc": "Öğrenmeyi LightGBM yapıyor, Claude kodu / ölçüleri / etiketi / kuralı yazıp ölçüyor. Aynı fiyat-hacimden türetilen fazla metrik "
              "yeni bilgi değil (K48'de AUC değişmedi; literatürde de bütün yöntemler momentum, likidite, oynaklığı buluyor). Literatürde "
              "makine kârının çoğu mikro / sıkıntılı hisse ve oynak dönemlerden (bizim bulgumuzla aynı). Bir iz üzerinde gel gitin "
              "disiplinli hâli META-ETİKETLEME: senin kuralın yönü verir, makine yalnız 'bu sinyali al / alma / ne kadar' der; deneme "
              "sayısı kayıtlı tutulmalı. Bizde eksik: meta-etiketleme, piyasa yönünden arınmış (göreli) etiket, grafik resmi (CNN), yeni veri",
     "durum": "TAMAMLANDI (devam: Cemal'in ABD Çöl Yolu araştırma görevi, alttaki satır)"},
    {"tarih": "2026-10-29", "istek": "ABD hisselerinde Çöl Yolu formasyonu araştırması (meta-labeling, triple barrier, Gu-Kelly-Xiu, Jiang-Kelly-Xiu "
                                     "CNN, PBO; batanlar dahil; Colab tek parça; çıktılar COLAB_VERILER/OUTPUT); sonra birleştirilmiş plan "
                                     "(LR referans, oynak bariyer, LSTM, grup katkısı, hacimli taban yeniden, kalibrasyon, Sharpe/Calmar); "
                                     "ajanlarla ters düz denetim; HT kayıtlarının CSV'de olduğunu doğrula",
     "yapilan": "COL_YOLU_ABD.py (CY v1.1, tek dosya, çakışma kapılı, test 11/11): ön kayıt v1.0 + v1.1 sonuç görülmeden commit; "
                "iki bağımsız denetçinin (kod, plan uyumu) bulguları sonuç görülmeden düzeltildi; tam koşu (ABD 2.752 hisse, 3,2 milyon "
                "hisse-gün; Avrupa, BIST); resmi FI_OLCUT; olay CSV'leri HT dahil yeniden üretildi ve sayılar doğrulandı; D1 deneme; "
                "üçüncü denetçi sonuçları ters düz etti; IZ_KARNE Ç132-Ç133; K51_OZET.md",
     "sonuc": "İZ DEĞİL. P1 rastgeleden +2,5 / +2,4 puan (eşik 5), net getiri taban kadar; meta, CNN, LSTM, özellik gruplarının hiçbiri "
              "bağımsız testte katkı vermedi; portföyler SPY'nin çok altında. Önceki 'hacimli taban' adayı tekrarlanmadı. Kontroller hattın "
              "çalıştığını gösterdi",
     "durum": "TAMAMLANDI (devam: K51 sonrası bağımsız denetim, alttaki satır)"},
    {"tarih": "2026-10-29", "istek": "K51 sonrası bağımsız araştırma planı + 11 maddelik ön kayıt eki: veri bütünlüğü, kırılganlık, model eklemeden beş "
                                     "hipotezi ayır, eşleşmiş kontroller, test disiplini, beş çıktı dosyası; K51 kararını değiştirme; önce özet, "
                                     "sonra 'yaz' ile başla",
     "yapilan": "Ön kayıt (8e99902 + V8) sonuç görülmeden commit; COL_YOLU_ABD.py v1.2 (panel + senaryolar, eşleştirme, H-A..H-E, Holm, veri "
                "denetimi, kırılganlık, eski kod kıyası, tekrar üretim; test 17/17); tam koşu 10,7 dk; K51_VERI_DENETIMI.md, K51_KIRILGANLIK.md, "
                "K51_ESLESMIS_KONTROL.csv.gz, K51_HIPOTEZ_KARARLARI.csv, K51_TEKRAR_URETIM.md, K51_EVREN_PIT.csv; IZ_KARNE Ç134; Drive OUTPUT",
     "sonuc": "K51 kararı korundu: beş hipotez de DESTEKLENMİYOR. H-A'da küçük (+3 puan), eşik altı, 2016-22'de sıfır bir etki var. Veri: "
              "Tiingo 'batan' örnekleminin çoğu batan değil (51 batma benzeri, 171 satın alma, 153 kod yeniden kullanımı); duyarlılık senaryoları "
              "sonucu değiştirmiyor; P1 artısı yalnız bugün işlem görenlerde",
     "durum": "TAMAMLANDI, AÇIK: ileri doğrulama (sinyal >= 01.09.2026, en erken Mart 2027); Kasım Tiingo kotası ile gerçek batan evreni"},
    {"tarih": "2026-10-29", "istek": "K51 — grafik izi + analist revizyonları: yeni araştırma görevi (önce veri kaynağı ve tarihsel kapsam "
                                     "denetimi; A-H değişkenleri ayrı; sızıntı kuralları; dört grup; H1-H6 ön kayıt; K51 ölçütü; altı çıktı; "
                                     "K51 kararı değişmez; AL sinyali yok)",
     "yapilan": "Ön kayıt K52_onkayit.md (c33a10e) sonuç görülmeden; Yahoo analist not günlüğü 3.267 sembol için çekildi (boş dönenler iki "
                "kez yeniden denendi: 56 düzeldi, 752 kesin boş); COL_YOLU_ABD.py v1.3 (cy_v13_calistir: kapsama, pencere özellikleri, dört "
                "grup, H0-H6, Holm, kırılganlık; test 21/21); koşu 3,6 dk; altı çıktı (K51_ANALIST_VERI_KAPSAMI.csv, "
                "K51_ANALIST_REVIZYONLARI.csv.gz, K51_GRAFIK_ANALIST_4GRUP.csv, K51_ANALIST_EK_KATKI_TESTI.csv, "
                "K51_ANALIST_TARIHSEL_VERI_DENETIMI.md, K51_GRAFIK_ANALIST_ARASTIRMA.md); IZ_KARNE Ç135; Drive OUTPUT",
     "sonuc": "Analist revizyonu grafik izine ek bilgi katmıyor: H0-P1 +1,7 / +2,1 / -2,0 puan, H0-P2 +11,4 / +5,5 / +2,0 (yalnız 2016-22 "
              "tutar); H2, H3, H5, H6 desteklenmiyor / yetersiz; H4 (revizyon fiyattan sonra geliyor) P2'de destekleniyor. EPS, gerekçe ve "
              "tarihsel sürüm verisi yok; H1 ölçülemedi. K51 kararı korundu",
     "durum": "TAMAMLANDI, AÇIK: ileri doğrulama (sinyal >= 01.09.2026, en erken Mart 2027); Kasım Tiingo kotası ile gerçek batan evreni"},
    {"tarih": "2026-10-29", "istek": "K53: bilgi direnci hipotezi (olumlu analist revizyonuna rağmen fiyatın tepki vermemesi + satış baskısının "
                                     "zayıflaması, BDS), analist dağınıklık endeksi (ADE), karar gecikmesi süresi (KGS); üçünü ayrı ayrı 60 günlük "
                                     "üçlü bariyerle karşılaştır; destekleyen ve çürüten testleri birlikte koştur; hiçbiri işe yaramazsa eşik "
                                     "uydurmadan kapat; K51 ve bariyer değişmez",
     "yapilan": "Ön kayıt K53_onkayit.md (488a407; ADE / KGS tanımları Claude tarafından sabitlendi, mesaj kesikti); COL_YOLU_ABD.py v1.4 "
                "(cy_v14_calistir: olay = ilk olumlu revizyon, 5 günlük tepki + satış baskısı A10 / B10 + BDS, KGS, ADE, G1-G5, T1-T8, Holm, "
                "kırılganlık; ortak panel kurucu cy_v13_panel; test 25/25); koşu 4,3 dk; K53_OLAYLAR.csv.gz, K53_GRUPLAR.csv, "
                "K53_HIPOTEZ_TESTI.csv, K53_RAPOR.md; IZ_KARNE Ç136; Drive OUTPUT. Sonra Cemal'in 6 maddelik geçerlilik listesi (sonuç "
                "görüldükten sonra; ön kayıt EK olarak yazıldı, karar kuralları değişmedi): eksik veri ölçülemez, G1-G5 eşleşmiş negatif kontrol + "
                "denge (K53_DENGE.csv), KGS-sonra, veri denetimi (K53_VERI_DENETIMI.md), test 27/27, yeniden koşu 4,5 dk",
     "sonuc": "K53 KAPANDI: T1 (BDS) +0,8 / -1,2 / +2,0, T5 (KGS geç - hızlı) -1,2 / -0,3 / -0,1, T6 (ADE) +2,4 / +2,8 / +2,5 (Holm p 0,017 ama "
              "eşik altı, oynaklıkla aynı); aynı şekil bilgi yok kontrolü (T4) fark göstermedi; BDS 3 olayların %74'ü 20 günde tepki vermiyor. "
              "K51 kararı korundu",
     "durum": "TAMAMLANDI, AÇIK: ileri doğrulama (sinyal >= 01.09.2026, en erken Mart 2027); Kasım Tiingo kotası ile gerçek batan evreni"},
    {"tarih": "2026-10-30", "istek": "K54 tarihsel hisse evreni sağlamlık denetimi: her sembolü 6 sınıfa ayır (aktif, iflas, birleşme, sembol "
                                     "değişimi, belirsiz, doğrulanamayan), eski testleri eski ve düzeltilmiş evrenle karşılaştır, K52 / K53 "
                                     "analist kapsaması, SAĞLAM / ETKİLENMİŞ / GEÇERSİZ etiketi; K51 kararı ve kurallar değişmez; Cemal: yeni iz "
                                     "aramadan önce K54 bitsin",
     "yapilan": "Ön kayıt K54_onkayit.md (d4dcdfb + açıklama) sonuç görülmeden; SEC başvuru geçmişi 3.262 CIK (e-posta UA yalnız indirmede), "
                "Tiingo sembol listesi (ücretsiz, fiyat kotası kullanılmadı), company_tickers; COL_YOLU_ABD.py v1.5 (cy_v15_calistir: sınıflama, "
                "düzeltilmiş panel, 66 eski-yeni hücre, sessiz ML, K52 / K53 yeniden etiket; test 29/29); koşu 1,6 dk; K54_EVREN_ESLESTIRME.csv, "
                "K54_SIRKET_DURUMU.csv, K54_ESKI_YENI_TEST_KARSILASTIRMA.csv, K54_DELIST_DUYARLILIK.csv, K54_RAPOR.md; IZ_KARNE Ç137; Drive",
     "sonuc": "Evren düzeltmesi eski sonuçları değiştirmiyor: 64 / 66 hücre SAĞLAM, 1 sınırda ETKİLENMİŞ (karar aynı), BB / EMA deneyleri "
              "GEÇERSİZ (yalnız hayatta kalan evren). Teknik hipotezlerin başarısızlığı evren hatasından gelmiyor. Ama evren çoğunlukla hayatta "
              "kalanlardan; eksik batanlar olmadan hayatta kalma yanlılığı tam ölçülemez",
     "durum": "TAMAMLANDI, AÇIK: Kasım Tiingo kotasıyla eksik batan şirketler (hayatta kalma yanlılığı); ileri doğrulama Mart 2027"},
    {"tarih": "2026-10-30", "istek": "K54 v1.5 kodlama öncesi zorunlu metodoloji düzeltmeleri: sınıf 1 (SEC sembolü tek başına kanıt değil, "
                                     "Tiingo çelişirse belirsiz), sınıf 2 (8-K 1.03'ün T'ye göre zamanı), sınıf 4a (son kapanış otomatik nakit "
                                     "bedel değil; doğrulanırsa seri bağla, yoksa belirsiz + duyarlılık), sınıf 6 (-%30 / -%100 varyantı + "
                                     "hayatta kalma tartışması); her testte A eski / B düzeltilmiş / C ortak örneklem; ML'de de A / B / C sabit "
                                     "ayarlarla; sonuç dosyaları açılmadan; K51 İZ DEĞİL değişmesin",
     "yapilan": "Ön kayıt eki (K54_onkayit.md bölüm 8, commit 5fa687d) ve kod (0ad1c90) sonuç görülmeden commit'lendi; COL_YOLU_ABD.py v1.5 "
                "ek 8: cy_v15_sinifla (dogrulama / belirsiz, b103_T_fark_gun / b103_zaman / b103_tarihler, 4a doğrulama bekler), "
                "cy_v15_4a_dogrula, cy_v15_ayristir, cy_v15_calistir (A / B / C-eski / C-yeni, sınıf 6 ve sınıf 1 belirsiz varyantları, "
                "4a bağlama ve bandı, ML dört örneklem), cy_v15_yaz; test_col_yolu_abd 31/31 (28 güncel, 30-31 yeni); koşu 3,2 dk; "
                "K54_* beş çıktı yenilendi (ilk koşu ac63f0d git geçmişinde); IZ_KARNE Ç137 notu; IZ_DEFTERI DERS 43; Drive: rapor, ön kayıt, delist CSV yenilendi (bayt bayt doğrulandı), karşılaştırma CSV\'sini (56 KB) Cemal elle yükledi, Drive kopyası bayt bayt doğrulandı (sha256 aynı); dört K54 dosyası Drive\'da güncel",
     "sonuc": "Düzeltmeler sonucu değiştirmedi: 55 ana hücrenin 54'ü SAĞLAM, 1 sınırda ETKİLENMİŞ (P1 2024-26, karar aynı), 1 GEÇERSİZ; "
              "evren etkisi en çok 1,1 puan, etiket etkisi en çok 0,06 puan; sınıf 1 belirsiz 11 (6'sı ETF: evren temizliği), sınıf 2'de "
              "1.03 başvurusu 18 / 19'da T'den önce, 4a n = 0, sınıf 6 n = 0. K51 İZ DEĞİL korundu",
     "durum": "TAMAMLANDI, AÇIK: K51 evreninde 6 emtia ETF'si (DBA, DBB, DBO, UNG, UNL, UUP) var, evren temizliği Cemal'in kararı; Kasım "
              "Tiingo kotasıyla eksik batanlar; ileri doğrulama Mart 2027"},
    {"tarih": "2026-10-30", "istek": "ETF'leri evrenden çıkar (K54 ek 8'in bulduğu 6 emtia / döviz fonu)",
     "yapilan": "Evren taraması: Tiingo ETF türü + SEC SIC 6221 + ad 'Fund' -> 7 fon (DBA, DBB, DBO, UNG, UNL, UUP + BTCW kripto fonu); "
                "evren_disi_ABD.csv (sembol, neden, kaynak, tarih) repo kökünde; COL_YOLU_ABD.py cy_evren_disi_yukle (veri / kod / çalışma "
                "klasörü, yoksa main'den GH_TOKEN ile indirir, yine yoksa durur) + cy_evren_filtre, cy_veri_yukle sonunda uygulanır ve loglanır; "
                "test_col_yolu_abd 32/32 (test 32); gerçek veriyle doğrulama: 3.267 -> 3.260 sembol, 7 fon yok; CLAUDE.md ayar dosyası satırı",
     "sonuc": "Bundan sonraki her koşu (K51 zinciri, K54) fonsuz evrende. Eski K51 / K52 / K53 / K54 çıktıları fonlu evrenle kaldı; etkisi K54 "
              "duyarlılık satırlarıyla sınırlı (11 belirsiz çıkarılınca P1 / P2 en çok 0,10 puan), karar değişmez. BDC'ler (BXSL, MSDL), "
              "REIT ve MLP'ler şirket sayıldı, evrende kaldı",
     "durum": "TAMAMLANDI, AÇIK: K51 tam koşusunun (52 dk) fonsuz evrenle yenilenmesi Cemal'in kararı (gerekli görülmedi, etki <= 0,1 puan)"},
    {"tarih": "2026-10-30", "istek": "K55 KUANTUM DALLANMALI İZ ARAMA: evreni 10 ana dala, her dalı 10 hücreye böl; büyük yükselişlerden geriye "
                                     "doğru + eşleşmiş kontrol + değişim noktası; ön kayıt, FDR, kronolojik dönemler, fonsuz evren; ilk teslimat kod "
                                     "değil PLAN (veri gereksinimi, değişken, yöntem, maliyet); plan onaylanmadan büyük koşu yok",
     "yapilan": "arastirma_cikti/k55_dallanma/K55_PLAN.md: ortak kurallar (evren, dönem kilidi 2016-21 / 2022-23 / 2024-26, olay tanımları "
                "Y60 +%30 / Y120 +%50 / Y250 +%100, üç yöntem, ölçütler, FDR aile = dal, durum etiketleri, dallanma şablonu), veri envanteri "
                "(hazır / gerek / yok), 10 dal x 10 hücre = 100 hücre (kimlik, soru, değişken, veri, yöntem, not), eski çalışma çakışmaları "
                "ve kapalı konular, 4 faz maliyet, 6 karar maddesi; K51-K54 arşiv noktası commit 83e5de8 (etiket gönderimi 403)",
     "sonuc": "100 hücrenin 71'i yalnız OHLCV ile ölçülebilir; 9 hücre eski çalışmayla çakışır (yalnız yeni boyut), 6 hücre kapalı konuya "
              "dokunur (onaysız koşulmaz); D07 yalnız 2021+ (SEC FS), D08 için 13F ve Form 4 satışları indirilmeli. Kod yazılmadı, koşu yok",
     "durum": "TAMAMLANDI: Cemal 6 kararı onayladı (30 Eki), Faz 0 başlatıldı"},
    {"tarih": "2026-10-30", "istek": "K55 FAZ 0 (Cemal'in 6 kararıyla): K55/ modüller + K55.py; dönem kilidi 2016-21 / 2022-23 / 2024-26; SEC özeti ve "
                                     "Tiingo listesi islenmis-veri'de sürümlü; 13F / Form 4 yalnız Faz 2; kapalı hücreler kapalı; olay tanımı ve ölçütler "
                                     "kilitli; veri kalitesi, fonsuz evren, ortak panel, eşleştirme kontrolü, sızıntı testleri, sentetik testler, 50 "
                                     "hisselik deneme, rapor; iz sonucu optimize edilmez",
     "yapilan": "K55/ONKAYIT_K55.md kilit (commit c5304ae, koşudan önce) + v1.1 açıklamaları; islenmis-veri k55/ paketi (sec_ozet 105 MB -> 6,6 MB xz, "
                "supported_tickers, sembol_cik, company_tickers; manifest: kaynak, tarih, dönem, sürüm, sha256, işleme kodu; fce5d94); K55/ 15 modül "
                "(ortak, evren, veri_kalitesi, olay_tanimlari, panel, istatistik, eslestirme, sizinti, hucre A/B/C, hucreler D01-S01, raporlama, "
                "veri_paket, faz0) + K55.py (çakışma kapısı) + test_k55 10/10 sentetik; 50 hisselik deneme (15 sn, iki koşu aynı sonuç) ve tam evren "
                "Faz 0 (3,2 dk): arastirma_cikti/k55_dallanma/ ve tam_evren/ (K55_FAZ0_RAPOR, VERI_KAPSAMI, VERI_KALITESI, EVREN, OLAYLAR, "
                "SIZINTI_TESTI, HUCRE_ISKELE, KOSU.json)",
     "sonuc": "7 soru: eksiksiz 2.411 / 3.260 (sıkı tanım; sıçrama bayrağı 738 çoğu haber günü, Faz 1 başında elle örnek), tarihsel eksik 242, CIK "
              "eşleşen 3.259 / 3.260, delist: sınıf 2 -%100 / 3 bedel / 5 K51 kuralı, 4b kesim, sınıf 6 dışarı; sızıntı testleri HEPSİ GEÇTİ (olumlu "
              "kontrol d +1,19 AUC 0,83; olumsuz d -0,00); modüller hatasız; panel 4,9 M satır 0,6 GB, olaylar Y60 13.894 / Y120 6.201 / Y250 2.407 "
              "(örtüşme 0); Faz 1 tahmini ~3,5 saat. İskele D01-S01 ETKİ YOK / TUTMAZ (pipeline denetimi, iz sonucu değil). BAĞIMSIZ dönem açılmadı",
     "durum": "TAMAMLANDI (ilk koşu); Cemal'in 9 maddelik denetimiyle v1.2'de yeniden koşuldu (sonraki satır)"},
    {"tarih": "2026-10-30", "istek": "K55 ortak ayarlar denetimi, 9 zorunlu düzeltme: purge >= 250 + embargo ayrı; BAĞIMSIZ bitişi gerekçesi; getiri / "
                                     "düzeltme / delist / olay başlangıcı / örtüşme açık kilit; koşu kimliği (kilit sha boşsa dur, git ağacı, kod + veri sha, "
                                     "ayar özeti); dönem etiketi gün sonu / saat dilimi / NaT; MIN_GUN özellik gereksinimi, kısa seri silinmez; blok bootstrap + "
                                     "FDR ailesi + test yükü; çıktılar Drive OUTPUT altında + yol denetimi; COL_YOLU_ABD yan etkisiz içe aktarma testi; "
                                     "önce testler, sonra 50'lik deneme, sonra tam evren; kilitli kararlar sonuca bakarak değişmez",
     "yapilan": "ONKAYIT_K55.md v1.2 (koddan önce commit e4f4737, 9 madde + veri kalitesi notu); K55 v0.2: ortak (PURGE_GUN = 250, EMBARGO 10 / 14 gün, "
                "donem_etiketi_ufuk PURGE / EMBARGO / TANIMSIZ, kosu_kimligi: kilit / git kirli / 18 kod sha / 8 veri sha / ayar sha, cikti_dogrula), panel "
                "(bitis60-120-250, donem60-120-250, blok60), olay (bitis, donem), hucre (ufuk bazlı dönem, blok aralıkları), istatistik (coklu_test_ozeti), "
                "evren (kısa seri listesi, Tiingo indirme kapalı), kalite (sert hareket bilgi); test_k55 15/15 (dönem kenarları, purge / embargo, kimlik / yol, "
                "ağ kapalı içe aktarma, çoklu test); 50'lik deneme (sızıntı hepsi geçti) ve tam evren yeniden koşu 3,5 dk (commit 8bed3ef, temiz ağaç); "
                "çıktılar arastirma_cikti/k55_dallanma/ ve tam_evren/ (+ K55_EVREN_DISI_KISA.csv, K55_COKLU_TEST.csv, K55_KOSU.json sha'lı)",
     "sonuc": "Düzeltmeler bölünme / temettü doğrulamasını da içerdi (V_ABD, K34 Yahoo, Tiingo adj: AAPL 2015 kapanış 29,1; bölünme günleri sürekli); "
              "'sıçrama' bayrağı haber günleri çıktı (ABEO, AGEN, ALNY), eksiksizlikten çıkarıldı. Tam evren: eksiksiz 3.012 / 3.260, kısa geçmişli 60 "
              "(VERİ YETERSİZ, silinmedi), CIK 3.259 / 3.260; purge: Y60 KEŞİF 4.292 olay (1.427 PURGE), Y250 KEŞİF 895 (570 PURGE); sızıntı testleri "
              "hepsi geçti (olumlu d +1,18, olumsuz −0,003); iskele D01-S01 ETKİ YOK / TUTMAZ (iz değil). BAĞIMSIZ açılmadı",
     "durum": "TAMAMLANDI (v1.2 koşusu); evren modülü denetimiyle v1.3'te yeniden koşuldu (sonraki satır)"},
    {"tarih": "2026-10-30", "istek": "K55 evren modülü denetimi, 11 madde: ornek_sec tam 50 benzersiz + eksik tabaka raporu + CSV; evren sürümü K54 dosyaları, "
                                     "evren_disi, veri sha ve kurallarla; eksik cikis_islemi 'y' sayılmasın, K54 sınıf / işlem / kesim tutarlılığı; kontrollü boolean; "
                                     "SERI_SONU gerçek değerlerle, 4a halef kesin değil, 4b yanlış şirket fiyatları kesilir + satır sayıları; 320 / 260 açıklaması; "
                                     "normalize sembol (nokta / tire birleştirilmez); ağ erişimi testi (network=False); V/EV çift yönlü; dışlamalar ayrı ayrı; "
                                     "örneklem sınıf 1-5, kaynak, likidite, büyüklük; 11 sentetik test; sonra 50'lik deneme; tam evren BAŞLATILMASIN",
     "yapilan": "ONKAYIT_K55.md v1.3 notu; K55/evren.py yeniden: saf evren_insa + I/O evren_kur(network=False, ag_kapali soket kapısı), k54_tutarlilik "
                "(sınıf × izinli işlem tablosu SINIF_ISLEM; boş işlem BELİRSİZ; y_kes kesim ister; 'False' metni kontrollü; yinelenen sembol tutarsız), "
                "kesim_uygula (işlem günü olmayan kesimde son <= kesim; önce / sonra / atılan), tutarlilik_V_EV (hata -> durur), evren_surum (EV + 3 dosya sha + "
                "8 veri sha + kurallar), ornek_sec (kaynak × sınıf × likidite tabakası, tekrarsız, eksik tabaka + tamamlama CSV), yukleyici_esigi_dogrula "
                "(320 kaynak koddan), sembol_normalize; test_k55 26/26 (11 sentetik vaka dahil); 50'lik deneme koşusu (commit 7ce1627): çıktılar "
                "K55_EVREN_DISI.csv, K55_KESIM.csv, K55_K54_TUTARLILIK.csv, K55_ORNEKLEM.csv + öncekiler",
     "sonuc": "Tam evren 3.260 (sınıf 1: 2.994, 2: 19, 3: 159, 4: 9, 5: 79); dışlamalar ayrı: kısa seri 60, fon 7, CIK eşleşmesi yok 1 (evrende, bilgi); "
              "K54 tutarsızlık 0, boş çıkış işlemi 0; 4b kesim 9 sembol (satır sayıları CSV'de); V/EV tutarlılık geçti; örneklem 50 benzersiz, eksik tabaka "
              "V_ABD sınıf 1 düşük likidite (7 aday / 10 kota, 3 tamamlama ile) raporlandı; sızıntı testleri hepsi geçti; eksiksiz 46 / 50. Tam evren koşulmadı",
     "durum": "TAMAMLANDI (evren v1.3); veri kalitesi modülü denetimiyle yeniden koşuldu (sonraki satır)"},
    {"tarih": "2026-10-30", "istek": "K55 veri kalitesi modülü yeniden (8 madde): bütün EV evreni (V'de olmayanlar kaybolmasın, V fazlası, yinelenen / çoklu "
                                     "CIK), ABD işlem takvimi (tatil eksik gün değil, boşluk tarihleri, > 5 gün ciddi), normalize kopya ile tarih / saat dilimi, "
                                     "OHLCV ihlalleri ayrı sayım, sıfır / eksik hacim ayrı, %100 getiri hata değil, bölünme kesin / muhtemel / açıklanamayan / "
                                     "haber (kurumsal veri yoksa kesin denmez), CIK / ad / sektör / boolean denetimi, özellik ve sonuç pencereleri ayrı, dönem "
                                     "kapsamı, her sorun ayrı sütun ('eksiksiz' yok), 11 yapay vaka testi; K51 / K54 / ortak.py değişmez; sessiz silme / düzeltme yok",
     "yapilan": "K55/veri_kalitesi.py tek parça yeniden: NYSE takvimi (pandas holiday kuralları, Juneteenth 2022+, özel kapanışlar, 1 Ocak cumartesi "
                "istisnası), _normalize_kopya, _ohlcv_denetim, _takvim_denetim, _sicrama_sinifla, _pencere_denetim, _cik_denetim, evren_kalite (EV tam), "
                "kapsam_md; raporlama / faz0 uyarlandı; test_k55 26/26 (3 = 11 kalite vakası + takvim testleri). İlk koşuda 2022-01-03 takvim dışı "
                "sayıldı (yılbaşı cumartesi kuralı hatası), düzeltildi ve test eklendi; 50'lik deneme yeniden (commit sonrası)",
     "sonuc": "50 hisse: veri hatası 0; veri yetersiz 4 (sıfır hacim payı > %20: AEHL, AGGRU, BRBS, GORO); kullanılabilir 46; olağan piyasa davranışı 18 (bilgi); "
              "şüpheli sıçrama 11 (muhtemel bölünme 8, açıklanamayan 7; kurumsal işlem verisi YOK -> kesin yok; seriler düzeltmeli, bayrak uyarı); "
              "boşluklu 1 (1 gün); CIK geçerli 50 / 50; sektör boş 5; 4b kesilmiş 2; sonuç penceresi Y250 yeterli 46; sızıntı testleri geçti. Tam evren koşulmadı",
     "durum": "TAMAMLANDI, AÇIK: tam evren koşusu ve Faz 1 Cemal'in onayını bekliyor; kurumsal işlem (bölünme) verisi kaynağı yok (Yahoo splits ücretsiz, karar)"},
    {"tarih": "2026-10-30", "istek": "Tam evren Faz 0 koşusu ve Faz 1 başlatma onayı. Kostur",
     "yapilan": "Faz 0 tam evren (v1.3 + veri kalitesi; 3.260 sembol, 22.502 olay, sızıntı testleri geçti, 5 dk); Faz 1 kodu: dal modülleri D01-D06 + "
                "D10 (63 hücre; D03-S07 kapalı, D04-S10 bilgi, D05-S09 kontrol, D10-S05 / S07 Faz 2), hücre motoru A / B / C varyantlı, blok "
                "bootstrap, rejim, yıl tekrarı, Holm + BH, eksik payı > %20 -> VERİ YETERSİZ; 50'lik duman koşusu, sonra tam evren Faz 1 (81,5 dk); "
                "vekil kıyası modülü K55/vekil.py (ön kayıt ek v1.4; python K55.py vekil) ve koşusu (26 hücre, 12,9 dk); koşu sonrası notlar "
                "(yön uyumu, seçim etkisi, B sonucu) K55_FAZ1_RAPOR.md sonunda; test_k55 30/30; IZ_KARNE Ç138; çıktılar arastirma_cikti/k55_dallanma/tam_evren/",
     "sonuc": "63 hücre: KEŞİF 25, REDDEDİLDİ 36, VERİ YETERSİZ 2, HATA 0. B (eşleşmiş ileri getiri) hiçbir varyantta tutmadı (0 / 164). 25 KEŞİF'in "
              "19'u ters yönlü (sert düşüş sonrası tepki + olay başlangıcı seçim etkisi), yön uyumlu 5'i küçük etkili; VEKİL 1 (D03-S02 ← r20). "
              "FAZ 1'DE İZ YOK. Drive OUTPUT'a yükleme Colab'dan (connector büyük dosyada güvenilmez)",
     "durum": "TAMAMLANDI, AÇIK: dallanma (yön uyumlu 5 hücre) ve İÇ DOĞRULAMA açılsın mı, Faz 2 (13F / Form 4) ve Faz 3 (D09) Cemal'in kararı; "
              "bölünme verisi kaynağı; Kasım Tiingo kotası; IZ_DEFTERI Drive kopyası (DRIVE maddesi)"},
    {"tarih": "2026-10-30", "istek": "K51-K55 ETKİ VE MEKANİZMA ARAŞTIRMASI, Faz 0 (envanter, açıklanmamışlar, hipotezler, veri kaynakları, kapsam / maliyet, "
                                     "doğrulama yöntemleri, riskler, sıra; küçük örneklem erişim testi); 'önerileri süzgecinden geçir, yapılması gereken ne ise yap'",
     "yapilan": "K56/ ayrı paket + K56.py (çakışma kapısı); ön kayıt ONKAYIT_K56 v1.0 (sentetik koşudan önce), v1.0-a, v1.1 (denetim sonrası, Faz 1 öncesi); "
                "envanter (6 okuyucu ajan + mekanik denetim), M01 sentetik sıfır sınaması (63 hücre + 125 KEŞİF satırı), hipotez kaydı M01-M19, 28 kaynak, "
                "erişim testi (12 sembol, temiz önbellek 131,9 MB), dört bağımsız denetçi (45 bulgu, 42 düzeltildi), K56_FAZ0_RAPOR.md + 20 CSV; test_k56 15/15; "
                "K51-K55 dosyaları değişmedi (test 15); IZ_KARNE Ç139",
     "sonuc": "Mekanizması aranacak sağlam etki çok az: K51-K54'te kaynakta desteklenen ve eser adayı olmayan etki yok; K55'in ters yönlü KEŞİF'leri "
              "olay tanımı eseri ADAYI (Y60 21 / 25, KEŞİF ufku 18 / 25; denetçi kontrolünde seçimsiz etiketle etki ~%90 küçülüyor); 4 K55 hücresi neden "
              "belirsiz. Önceki ortalama getiri testleri (Ç100-Ç107) yeniden yapılmadı. Büyük indirmeler (13F, MIDAS, FS 2016-20) ertelendi (koşullu)",
     "durum": "TAMAMLANDI, AÇIK: Faz 1 adım 1 (seçimsiz kontrol, yerel) Cemal onayı; İÇ / BAĞIMSIZ dönem açma kararı; Drive kopyası (Colab: python K56.py drive); "
              "Tiingo kotası (batanlar)"},
    {"tarih": "2026-10-31", "istek": "K56 FAZ 1 KARARLARI: (1) seçimsiz kontrol, oynaklık / piyasa / tema denetimi, haber ve birleşme bileşimi (indirme yok, sızıntı "
                                     "yok); (2) İÇ 2022-23 açılsın, BAĞIMSIZ kapalı, kilit hash; (3) Tiingo Kasım kotasıyla batanlar, yeni evren sürümü, sınıflar, "
                                     "etki; (4) üç çalışma ayrı rapor / sürüm / kimlik, başarısız sonuç korunur",
     "yapilan": "ön kayıt v1.2 (+ v1.2-a Ö2 düzeltmesi, v1.2-b denetim düzeltmeleri); K56/faz1_yerel.py (ortak motor), dönem kapısı + BAĞIMSIZ kilidi, "
                "batan_evren + evren_v2; bağımsız kod denetçisi (1 kritik, 4 orta, 8 düşük; hepsi düzeltildi ya da kaydedildi; ilk koşu geçersiz, saklandı); "
                "K56-F1A ve K56-IC koşuları (koşu klasörleri + SON.json); EVREN2 aday listesi (490); test_k56 24/24; IZ_KARNE Ç140-Ç142",
     "sonuc": "KEŞİF: 125 satırın hiçbirinde seçimsiz etiketle gerçek etki kalmadı (116 MEKANİK; d medyanı -0,265 -> -0,014); kalibre sentetik de farkı "
              "tam üretiyor. İÇ: K55 A farkları tekrarlıyor (B1 119 / 125) ama yine mekanik (B2: 0 GERÇEK ETKİ); K55 B 64 / 64 TUTMAZ. Haber / birleşme "
              "büyük yükselişleri açıklamıyor; yükselişten sonra hisse ihracı artıyor (açıklayıcı). K55 ters farkları olay tanımının eseri",
     "durum": "TAMAMLANDI, AÇIK: EVREN2 Tiingo indirmesi ve evren v2 etkisi (1-2 Kasım; bekçi + zamanlı kontrol); BAĞIMSIZ açma kararı (Cemal); Drive kopyası"},
    {"tarih": "2026-11-01", "istek": "K56 / K55 BAĞIMSIZ DÖNEM KARARI (9 madde): 2024-26 yalnız ön kayıtlı testlerle açılsın; önce kod sabitlensin, ön kayıt "
                                     "yeniden üretilsin, hash'ler ve kilit, İÇ'te dolaylı erişim olmadığı doğrulansın; yeni keşif / eşik yok; (iii) / bütün günler "
                                     "ayrışması kümelenme ve yapay veriyle incelensin; 125 satır + B bir kez, sonuç olduğu gibi; Tiingo 490 aday ve yeni evren ayrı "
                                     "doğrulansın; K51-K55 değişmez; Drive ve nihai kayıt; K55 nihai karar, gerçek etki yoksa korunur",
     "yapilan": "ön kayıt v1.3 (D BAĞIMSIZ protokolü, E ayrışma, F PBO / DSR, G sızıntı, H nihai karar eşlemesi, I EVREN2) + v1.3-a / b / c / d; K56/ayrisma.py, "
                "pbo_dsr.py, sizinti_denetimi.py, bir-kez açılış kaydı, kilit (kod / ön kayıt / eşik / veri / evren / ortam sha'ları, kıyas tabanı, uzak dal "
                "çapası); çok mercekli kod incelemesi; AYR, PBO, sızıntı (iki geçersiz deneme NOT.md ile saklandı), kilit, BAĞIMSIZ tek açılış; test_k56 31/31; "
                "IZ_KARNE Ç143-Ç146; K56_NIHAI_RAPOR.md; Drive (raporlar + IZ_DEFTERI paketi)",
     "sonuc": "K55 NİHAİ: İZ YOK. İÇ'te 2023 sonrası bilgiye dolaylı erişim yok (T0 / T1 birebir, T2 ihmal edilebilir). BAĞIMSIZ'da seçimsiz kontrolle "
              "gerçek etki hücresi yok (TERS KALINTI 12, MEKANİK 10), K55 B 64 / 64 TUTMAZ. (iii) / bütün günler ayrışması olay tanımının ağırlık "
              "mekaniği (yapay veri aynı deseni üretiyor). PBO / DSR aşırı uyum riski yüksek",
     "durum": "TAMAMLANDI, AÇIK: EVREN2 (Tiingo 490 aday indirmesi 1 Kasım 06:00 UTC'den itibaren bekçiyle; evren v2 doğrulaması ve etki raporu 1-2 Kasım); "
              "Drive'da IZ_DEFTERI paketinin Colab'da açılması"},
    {"tarih": "2026-11-04", "istek": "ABD mikro-cap AI altyapı (QMLS, DGXX, AIB, VIVO) bağımsız denetim: önceki rakamlar, 10x matematiği, öncü sinyal, evren dışı "
                                     "adaylar, mevcut QMLS zararlı pozisyon (A tut / B sat / C geç)",
     "yapilan": "7 kol araştırma (EDGAR 10-Q / 8-K / 20-F / DEF 14A, ilçe ve ISO kayıtları, akran değerleme, sektör taban oranları); notlar + rapor "
                "arastirma_cikti/abd_10x/ (ABD mikro cap AI 10x denetimi.md + PDF)",
     "sonuc": "Hiçbir aday yeterince güçlü değil; sıralama DGXX > AIB > QMLS > VIVO (DGXX yalnız izleme, 13 Kas Q3 / 15 Ara RFS). Düzeltmeler: QMLS IPO değil "
              "doğrudan listeleme, 10-Q'da going-concern, $523M sözleşme yalnız PR; AIB sahası Spartanburg SC, Nebius exhibit yok; VIVO kodu VIVO, capex $411M, "
              "kiracı yok; DGXX hisse 102,06M / FD 111,54M. QMLS pozisyonu: varsayılan B (sat); A yalnız Q3 10-Q dört şartı sağlarsa, lock-up 12-16 Oca 2027",
     "durum": "TAMAMLANDI, AÇIK: karar Cemal'in; QMLS Q3 10-Q (16-25 Kas) ve DGXX Q3 (13 Kas) sonrası yeniden bakılır"},
    {"tarih": "2026-11-05", "istek": "Aynı yöntemle (gerçek varlık, bağlayıcı sözleşme, seyrelme, finansman, öncü iz, fiyatlanma, hisse başına 10x) BIST'te hangi hisse öne çıkar",
     "yapilan": "4 kol araştırma (veri merkezi / teknoloji evreni, enerji altyapısı evreni, öncü sinyal + teşvik + fon krizi, taban oran + seyrelme + kriz; "
                "K25 fon payı tablosu repodan) + rapor arastirma_cikti/bist_10x/ (BIST 10x adayları aynı yöntemle.md + PDF)",
     "sonuc": "Yöntemi tam geçen BIST hissesi yok; 'al' yok, izle: YEOTK (5/10), GWIND (5/10), EUPWR (4/10), üçü de 2-3x normalleşme adayı, 10x değil. "
              "BIST taban oranı 3 yılda 10x USD %1,85, kalıcılık %24; küçük/orta BIST'te çalışan veri merkezi kapasitesi yok (yalnız TCELL / TTKOM); "
              "ABD talebi yalnız ASTOR'da backlog (referans). Elenen: KONTR (TMSF kayyım), ODINE / ANELE / MANAS / IEYHO (SPK), GEREL, NETAS, SMRTG, MAGEN, ESEN, "
              "EMKEL, PAPIL. KAP fon payı (K25) krizi yakalayamadı: alt sınır",
     "durum": "TAMAMLANDI, AÇIK: 3Ç26 bilançoları (Kasım) ve fon tasfiye süresi (Mart 2027) sonrası yeniden bakılır; teşvik listeleri ve KAP sayfaları erişilemedi"},
    {"tarih": "2026-11-06", "istek": "Raporu anlamadım, en iyi adaylar net değil; son haber yok ama fiyatlar neden bu kadar derin",
     "yapilan": "Sade sıralama mesajla verildi (BIST: YEOTK, GWIND, EUPWR, GESAN; ABD: DGXX, DUOT, AIB); düşüş nedenleri araştırma notlarından + web (5-6 Kas)",
     "sonuc": "Şirket haberi değil: BIST'te fon tasfiyesinin zorunlu satışı (131 fon, kalan sığ pozisyonlar Mart 2027'ye kadar satılacak), SPK %8/6/4/2 fon tavanı, "
              "VBTS / BIST-100 çıkışı, endeks USD'de 2023 ortasından beri dip; ABD'de neocloud sektör satışı (borç ve capex korkusu, Musk 'konsolidasyon' yorumu, "
              "açığa satıcılar), QMLS'te tahvil dönüşü ve Ocak kilit bitişi arzı",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "YEOTK güne tavanla başladı",
     "yapilan": "Neden arandı: 5 Kas akşamı KAP 3Ç26 bilançosu (başka KAP sözleşmesi yok); rakamlar ikincil aktarımla okundu; BIST raporuna ek bölüm",
     "sonuc": "9A26 hasılat 17,5 mlr TL (+%31), FAVÖK 4,45 mlr (+%103), ana ortaklık kârı 1,53 mlr (+%64); yalnız 3Ç: hasılat ≈9,2 mlr, kâr ≈864 mn (6A toplamından fazla). "
              "Tetikleyici 1/3 geldi, puan 5 -> 6/10; açık: kârın tek seferlik EPC hakedişi olup olmadığı, Reap ihracat sözleşmesi, fiili dolaşım; borç/özkaynak ≈4,6x",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "600 BIST ve 2000+ ABD hissesinde alım yok; senin gözünle ne olacak, ne öneriyorsun",
     "yapilan": "Görüş mesajla verildi; dayanak: K42 (bilinen etkiler görünüyor), K43 (23 sinyal alınabilir iz değil), K34 / küçüklük yıl yıl (ortanca negatif), "
                "ABD ve BIST 10x raporlarının taban oranları",
     "sonuc": "'Al yok' = 10x çıtasını kanıtla geçen hisse yok; yatırım yapma demek değil. Öneri: çekirdek geniş endeks (dolar bazlı) + küçük uydu payında "
              "en fazla 2-3 seçilmiş isim, isim başına sınırlı boyut, tetikleyiciyle giriş; QMLS için önceki koşullu plan geçerli. Karar Cemal'in",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "Paraya ihtiyacım var; bugün YEOTK aldım, birkaç hafta sonra ekleyeceğim; dolarımın yarısından fazlası DGXX'te; QMLS dibe çöktü, nasıl kurtulurum",
     "yapilan": "Mesajla görüş: ihtiyaç parası ayrılsın, DGXX boyutu 13 Kas / 15 Ara öncesi küçültülsün, QMLS tek emirle çıkış planı (hemen ya da yarı yarıya, son tarih 12 Oca 2027 kilit), YEOTK'ye ekleme yalnız tetikleyiciyle ve boyut tavanıyla",
     "sonuc": "Asıl risk hisse seçimi değil boyut: ihtiyaç duyulan para mikro şirkette; QMLS'ten çıkış teknik olarak kolay (günlük hacim yeterli), zor olan zararı kabul etmek. Karar Cemal'in",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "QMLS'in yarısını bugün, kalanını bilançodan sonra satıyorum; aynı parayı DGXX'e koyacağım, risk ne",
     "yapilan": "Mesajla görüş: QMLS parasını 13 Kas DGXX bilançosuna kadar dolar nakitte tut; sonuç dört kontrolü geçerse kademeli ekle; DGXX toplam tavanı; "
                "kalan QMLS yarısı için NT 10-Q / Nasdaq uyarısı durumunda beklemeden sat",
     "sonuc": "Risk: tek hisse yoğunlaşması 13 Kas ve 15 Ara ikili tetikleyici önünde; kötü senaryo -%45..-%55; aynı sektör olduğu için QMLS'ten DGXX'e geçiş riski azaltmaz, yoğunlaştırır",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "Sen risksiz doğruyu yazıyorsun; risk almadan önceden planlayıp kazanmak olmaz",
     "yapilan": "Mesajla: itiraz kabul; risk alınır ama boyutla; DGXX için yazılı bahis planı (kaybı kabul edilen tutar, giriş / ekleme / çıkış kuralı, senaryo ağacı +%40 beklenti)",
     "sonuc": "Risk değil boyut öldürür (PAPIL, QMLS, TERA); plan = çıkışı girişten önce yazmak", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "Küçük yüzdeyle girsem ne olacak; 100 dolar 1000 olsa ne; büyük kazanmam gerekir",
     "yapilan": "Mesajla: 'büyük kazanmak' ihtiyaçtır, strateji değil; küçük sermayede tek seferde 10x ihtimali %1-3, sıfırlanma %30; sıralı 2-3x bahisler + birikim ekleme; hepsiyle giriş yalnız kaybı göze alınan parayla",
     "sonuc": "Karar Cemal'in; ölçüm: DGXX senaryo ağacı tur başına geometrik beklenti +%20 ama %30 ihtimalle -%45", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "Senaryo: ilk hissede 2x yaparsam sonraki hisselerde riski azaltırım",
     "yapilan": "Mesajla: plan kabul edilebilir (tek büyük bahis, sonra koruma); zayıf nokta ilk bahsin başarısızlığında devamın olmaması; 2x kuralı (anaparayı çek), başarısızlık kuralı (yeni bahse geçme), DGXX'te 2x = iyi senaryo (%35, 6 ay) yazıldı",
     "sonuc": "Karar Cemal'in", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "DGXX pozisyonu (175 adet, maliyet 2,01 $, portföyün %43'ü): 4,5 dolar kuralı ne",
     "yapilan": "Kural Cemal'in maliyetine göre yeniden yazıldı: 2x = 4,02 $'da 88 adet sat (anapara geri), kalan 87 adet bedava; olay bazlı çıkış kuralları",
     "sonuc": "Yazılı kural verildi; karar Cemal'in", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "Bilanço iyi gelecek; önce korkutup aldırmıyorlar, iyi gelirse göstermelik yukarı taşınır, sonra yavaş dağıtılır, sonraki yükseliş belirsiz",
     "yapilan": "Mesajla: K28 (bilanço sonrası ABD 2024-26 iyi sürprizde 60 günde eşlerine göre -%1,4: 'yükselişi sat' deseni ölçümle uyumlu) dayanak; DGXX için bilanço sıçramasında kısmi satış kuralı (ilk gün +%25 ve üstünde 1/3 sat), 2x kuralı korunur",
     "sonuc": "Cemal'in gözlemi ABD son dönem ölçümüyle tutarlı; karar Cemal'in", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "QMLS'i %44 zararla satacağım; en akıllı çıkış yolu ne",
     "yapilan": "Notlardan çıkış takvimi: ATW aylık itfa (%93 en düşük 8 gün VWAP, satış baskısı), açığa satış 1,23 M (3 gün kapatma; iyi haberde sıkışma ihtimali), 10-Q son tarih 16 Kas / NT ile 23 Kas, "
                "kilit 16 Oca 2027 (ilk işlem 19 Oca); yarı bugün limit emirle, kalan yarı olay kurallarıyla, son tarih 8 Oca 2027; vergi mahsubu notu",
     "sonuc": "Çıkış planı verildi; karar Cemal'in", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "Sektör %1 yükselirse QMLS en az %10, %2 yükselirse %20 zıplar; satışı buna göre zamanlayayım",
     "yapilan": "Ölçüldü (Yahoo, 20 Tem - 5 Kas 2026, 77 gün, 7'li neocloud sepeti): sepet > +%2 olan 24 günde QMLS ortalama +%4,4, medyan +%5,3, 4 günde eksi; > +%1 olan 29 günde 8'i eksi; sepete beta 0,59, korelasyon 0,4; QMLS günlük oynaklık %9,1",
     "sonuc": "İddia tutmuyor: QMLS sektörle aynı yönde ama 1:1 civarı hareket ediyor, 10 kat değil. 5 Kas: sektör -%10..-%17, QMLS -%19,5 (2,69 $), DGXX -%11 (1,90 $). Yeşil sektör gününde limit emirle satış mantıklı, beklenti +%5",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-06", "istek": "Sektör toparlanınca QMLS en hızlı çıkar mı; düzelme ne zaman; Microsoft olayı ne",
     "yapilan": "Microsoft (Bloomberg 5 Kas): neocloud projelerinde denetim sıkılaştı, riskli projelerden çekiliyor, yeni sözleşmeleri tartışıyor; Nscale Teksas genişlemesi ve İngiltere çapa kiracılığı bırakıldı; IREN 4 mlr $ ARR'nin Ocak'a kaydığını açıkladı (müşteri Microsoft). "
                "Ölçüm (20 Tem - 5 Kas, sepet dipten +%15 üstü 4 dalga): QMLS 1 dalgada sepeti çok geçti (+46 vs +18), 1'de eşit, 2'de yarısı kadar; DGXX 4'ünde de geride; dönem toplamı sepet -%50, QMLS -%72, DGXX -%53",
     "sonuc": "QMLS toparlanmada güvenilir şekilde en hızlı değil; düşüşte ise fazla düşüyor (ATW arzı). Düzelme tarihi bilinemez; işaretler: NBIS 11 Kas, DGXX 13 Kas, CRWV 16 Kas, Microsoft açıklaması",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-07", "istek": "QMLS işlem geçmişim (ekran görüntüsü): toplam ne kadar zarar ettim",
     "yapilan": "Gerçekleşen emirler toplandı: 7 alış 2.359,27 $, 4 satış 1.446,09 $, iptal / süresi dolan emirler hariç; net giren 913,18 $",
     "sonuc": "Kalan pozisyon ≈257 $ ise toplam sonuç ≈ -656 $ (≈ -33 bin TL, kur 50); kesin sonuç kalan adet ve fiyatla; Cemal'in daha önce söylediği 30-40 bin TL ile uyumlu",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-07", "istek": "Elde kalan QMLS (83 adet, 254,81 $, ort. maliyet 4,58 $, uygulama -125,69 $): bu yılın toplam zararı ne kadar",
     "yapilan": "Net giren 913,18 $ - kalan değer 254,81 $; uygulamanın 'toplam getiri'si yalnız kalan 83 adet içindir, önceki satışlardaki gerçekleşmiş zararı göstermez",
     "sonuc": "Toplam ≈ -658 $ (≈ -33 bin TL, kur 50): gerçekleşmiş ≈ -533 $ + açık -126 $. 6 Kas +%14 (3,07 $) satış planındaki 'yeşil gün'",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-07", "istek": "Benim QMLS'teki zararım ne kadar (tekrar soru)",
     "yapilan": "Tek rakamla sade cevap: toplam ≈ -658 $ ≈ -33 bin TL; yatırılan paraya göre oranı",
     "sonuc": "Toplam zarar ≈ 658 $; kalan 83 adet satılırsa (3,07 $) kesinleşir", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-07", "istek": "Zarar o kadar değil; QMLS'ten çıktım, DGXX'te 365 $, nakitte 445 $ var",
     "yapilan": "Hesap yöntemi açıklandı (net giren = alışlar - satışlar; satıştan gelen para zaten düşüldü); ekranda eksik işlem olabileceği kabul edildi; bağımsız kontrol: toplam yatırılan para - (DGXX + QMLS + nakit ≈ 1.065 $)",
     "sonuc": "Kesin rakam için Cemal'in hesaba toplam yatırdığı dolar tutarı gerekli; ya da işlem geçmişinin tamamı", "durum": "TAMAMLANDI, AÇIK: toplam yatırılan tutar"},
    {"tarih": "2026-11-07", "istek": "Hesap ekranı: yatırım 62.577 TL, toplam -36.833 TL (-%53,4); evet bütün zararım 33 bin",
     "yapilan": "Doğrulandı: hesap toplamı ≈ 99.400 TL yatırılmış, bugün 62.577 TL; QMLS ≈ -33 bin TL, kalan ≈ -4 bin TL öteki pozisyonlar ve kur; hesap: nakit 445 $, DGXX ≈ 370 $, QMLS 255 $, AAL 5 $",
     "sonuc": "QMLS hesabın zararının ≈ %90'ı; kalan sermayenin ≈ %58'i aynı sektörde iki mikro şirkette", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-07", "istek": "13 Kas'ı beklersek bilanço iyi gelirse %10-15 yüksekten alırız; şimdi mi girelim",
     "yapilan": "Basit karşılaştırma: şimdi almak, bilanço günü +%12..15 / -%20..30 senaryolarında ancak 'iyi gelir' ihtimali %57-71'in üstündeyse beklemekten iyi; K28 (ABD 2024-26 iyi bilanço sonrası 60 günde -%1,4) ve Cemal'in 'taşı sonra dağıt' tezi beklemeyi destekliyor; orta yol yarısı şimdi yarısı sonra",
     "sonuc": "Görüş: bekle ya da yarı yarıya; karar Cemal'in", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-07", "istek": "Nakdin yarısını pazartesi DGXX'e koyuyorum; limit emri kaça yazayım",
     "yapilan": "DGXX 6 Kas kapanış 2,085 $ (gün aralığı 1,955-2,11; 10 günlük ortalama gün içi aralık %8,7). Öneri: 108 adet limit 2,05 $ (≈221 $), gün boyu geçerli, normal seans, 18:00 TR sonrası; 2,20 üstü açılışta kovalama yok. Yeni ortalama ≈2,025 $, 2x eşiği ≈4,05 $ (142 adet satınca anapara geri)",
     "sonuc": "Emir planı verildi; DGXX hesabın ≈%55'i olur; karar Cemal'in", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-08", "istek": "RITUAL/USDT +%99,88 gibi yükseliş nasıl tespit edilir, derin araştırma yap",
     "yapilan": "3 kol (Ritual vakası, literatür, 759 yeni tokenda kendi ölçüm: Binance aynası + OKX + Gate) + rapor arastirma_cikti/kripto_yukselis/; IZ_KARNE Ç147",
     "sonuc": "İZ DEĞİL: +%100 günü önceden ancak 1 gün önce ve %1'in altında olasılıkla seçilebiliyor; sonrası medyan 30 günde -%49; kovalamak kaybettiriyor. Ritual'da doğrulanmış katalizör yok",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-09", "istek": "Kilit açılan token yükselir mi dedin, yanlış mı anladım",
     "yapilan": "Düzeltme mesajı: tersi; Keyrock çalışmasına göre açılımların ~%90'ı fiyata baskı yapar, düşüş ~30 gün önce başlar, ekip açılımlarında ~-%25; Ritual için ilk büyük açılım ~Ekim 2027",
     "sonuc": "Kilit açılımı yükseliş değil düşüş işaretidir", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-09", "istek": "Kilit öncesi yükseltip millete satıyorlar; millet niye girsin, enayi mi",
     "yapilan": "Mesajla: içeriden satış / çıkış likiditesi mekanizması; ölçüm açılım öncesi pompa değil düşüş gösteriyor (Keyrock); düşük float + yüksek FDV yapısı; kimin kazandığı; perakendenin neden girdiği (piyango tercihi, görünen kazananlar); BIST fon krizi ve QMLS ATW ile aynı desen",
     "sonuc": "Pratik kural: düşük float, yeni listeleme, sığ tahta = perakende çıkış likiditesi; uzak dur ya da sıfırlanmayı kabul ettiğin tutarla", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-09", "istek": "SON TALİMAT: kriptoyu boş ver; YEOTK gibi sıkı dosya hisseleri BIST ve özellikle ABD'de bul; bütün ölçüleri her açıdan ele al, her şeyi test et, gerekirse makine / web / ajan; bağlam kopmasın, deftere yaz; basit ve erişilebilir bilgi değerlidir",
     "yapilan": "CLAUDE.md'ye kalıcı bölüm + IK_ACIK YOL maddesi; K57 programı başlatıldı: (a) ön kayıtlı geçmiş test (K57.py), (b) BIST 3Ç26 canlı tarama, (c) ABD Q3 2026 canlı tarama (SEC XBRL frames)",
     "sonuc": "K57 (Ç148): YEOTK profili geçmişte eşlerini geçmiyor; hiçbir hücre tutmadı (ABD tam veriyle 9 Kas akşam yeniden koşuldu, sonuç aynı); eşiğe en yakın V1 (fiyat şartsız), F6 eklenince bozuluyor. Canlı: BIST 3Ç26 362 şirkette profile en yakın PNLSN ve FORTE; ABD Q3 2.128 şirkette tam profil yalnız CENX (fabrika hattı yeniden açılışı, isimli sözleşme yok); AEHR ölçüme tam girmedi",
     "durum": "TAMAMLANDI, AÇIK: 17 Kas sonrası ABD Q3 canlı taraması yinelenir (aday listesi)"},
    {"tarih": "2026-11-09", "istek": "Not: share.google bağlantısından haberleri takip edebilir misin (çalışanlar devam etsin)",
     "yapilan": "Bağlantı DonanımHaber forum 'profil düzenle' sayfasına (giriş gerekli) yönleniyor; hesaba erişim yok. Herkese açık forum konuları bağlantıyla okunabilir; haber için KAP / SEC / web araması kullanılıyor",
     "sonuc": "Not alındı; K57 kolları sürüyor", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-09", "istek": "Hangi web sayfası, forum, sosyal medya sana lazım; ne yazmam gerekiyor, açık ve net söyle",
     "yapilan": "Erişim haritası mesajla: açık (web arama, Yahoo fiyat, KAP aktarıcıları, SEC frames önceden inen), kapalı (SEC 403: e-postalı UA gerekiyor; KAP doğrudan çoğu zaman 403; X / Telegram / Instagram ve girişli forumlar). Cemal'den istenecekler: SEC için e-posta izni (açık cümleyle), isteğe bağlı ücretsiz veri anahtarı, forum konu bağlantıları, pozisyon ekranları, kritik tarihlerde otomatik kontrol onayı",
     "sonuc": "Karar Cemal'de: SEC e-posta izni ve otomatik kontrol", "durum": "TAMAMLANDI, AÇIK: Cemal'in yanıtı"},
    {"tarih": "2026-11-09", "istek": "QMLS yükseliyor; satmakta acele mi ettik",
     "yapilan": "Fiyat (Yahoo, 9 Kas 17:47 UTC): QMLS 3,32 $, 5 Kas dibinden +%23; satılan yarı ≈83 adet ≈3,10 $'dan (257,40 $); kaçan ≈18 $; aynı gün sektör toparlanması (CRWV +%5, NBIS +%8, DGXX +%9), şirket haberi yok",
     "sonuc": "Acele değil: plan yarı yarıya pişmanlığı bölmek içindi; kalan 83 adet aynı yükselişi alıyor; olay kuralları sürüyor", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-09", "istek": "DGXX alım emrim (2,05 $) gelmedi, ne öneriyorsun (fiyat 2,26, gün +%8,6, gün içi en düşük 2,02)",
     "yapilan": "Mesajla: fiyatı kovalamadan limiti 2,12 $'a çek, 104 adet, 12 Kas kapanışına kadar geçerli; dolmazsa yarı nakit bilançoyu (13 Kas) bekler; yeni ortalama ≈2,05 $, 2x ≈4,10 $",
     "sonuc": "Karar Cemal'in", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-09", "istek": "SEC için e-posta izni (ABD)",
     "yapilan": "E-posta yalnız SEC isteğinin User-Agent'ında ortam değişkeniyle kullanıldı (koda / repoya / günlüğe yazılmadı; günlükte maskeli). 178 frames dosyası indi; K57 aynı mühürle ABD tam veriyle yeniden koşuldu",
     "sonuc": "İZ DEĞİL (değişmedi): ABD tam profil çok seyrek (n 2-5) ve eksi; eşiğe en yakın V1 (fiyat şartsız) ABD 2024-26 +%10,3 n 31; F6 (tepeden düşmüş) eklenince bozuluyor. Sıradaki 3 deneme K57-B",
     "durum": "TAMAMLANDI, AÇIK: K57-B"},
    {"tarih": "2026-11-09", "istek": "E-postayı yanlış yazmışım, doğrusunu biliyorsun",
     "yapilan": "Not alındı: sonraki SEC isteklerinde Cemal'in hesabındaki doğru adres, yalnız User-Agent ortam değişkeninde kullanılır (koda / repoya yazılmaz). Bugünkü 178 dosya zaten indi ve önbellekte; yeniden indirme gerekmiyor",
     "sonuc": "Veri ve sonuç etkilenmedi", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-09", "istek": "QMLS Denver 1,2 MW beş yıllık colocation haberi; piyasa neden görmüyor",
     "yapilan": "Haber (Midas, Benzinga aktarımı, 9 Kas 15:52 TR, piyasa açılışından önce): karşı taraf, tutar, finansman yok; devreye alma 2027 Ç1. Fiyat: açılış 3,24 (+%3,5), gün içi en yüksek 3,37, 3,22'de (+%3); hacim düşük; aynı gün sektör +%5-9",
     "sonuc": "Colocation = QMLS büyük ihtimalle kiracı (gider ve yükümlülük); gelir için GPU alımı ve müşteri gerekir, bu da finansman / seyrelme demek; ölçek küçük (sözleşmeli 11,75 MW'ın ~%10'u); şirketin PR-yalnız sözleşme haberleri Ağu-Eki'de de fiyatı yükseltmedi. Kalan yarı için kurallar değişmez",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-09", "istek": "K57-B: K57 iz çıkmayınca önceden yazılı 3 devam (CLAUDE.md 'İz yok çıkarsa durma')",
     "yapilan": "Ön kayıt 18:12 UTC (sha abc73b49f1df), ölçüm 18:29; B1 geniş ABD evreni (4.261 şirket Yahoo fiyatı, 50.161 likit bilanço günü, V1 150 olay), B2 20 gün, B3 F3'süz; test_k57 9/9",
     "sonuc": "Üçü de İZ DEĞİL (Ç149). Ortalama farklar artı ama güven aralığı sıfırı geçmiyor; ABD 2023 hiçbir denemede n 30'a ulaşmadı; geniş evrende etki küçüldü",
     "durum": "TAMAMLANDI, AÇIK: C1-C3"},
    {"tarih": "2026-11-09", "istek": "K57-C: K57-B'de yazılı 3 devam (C1 V1+F4, C2 likidite 5 M$, C3 ear üst %10)",
     "yapilan": "Ön kayıt 18:44 UTC (sha b81b5fb148be), koşu 18:45 yalnız önbellekle (yeni SEC / Yahoo isteği yok); test_k57 10/10",
     "sonuc": "Üçü de İZ DEĞİL (Ç150). K57 + K57-B + K57-C: 48 ABD karar hücresinin hiçbiri tutmadı; YEOTK profili hattı ön kayıtlı ölçütle kapandı. Basit sonuç: iyi bilanço + güçlü tepki ortalamada hafif artı ama güvenilir değil; 'dipten alma' şartı bozuyor",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-10", "istek": "Sadece yapılan işlerin doğruluğunu sına, iş nasıl olmalı onu yaz; yapmayı alt modeller yapsın",
     "yapilan": "CLAUDE.md'ye 'Çalışma düzeni' bölümü (ana model = iş tanımı + denetim; uygulama alt ajanlarda). K57 / B / C ve canlı taramalar 11 maddede denetlendi: arastirma_cikti/k57_yeotk_profili/DENETIM_10Kas.md",
     "sonuc": "Kararlar (İZ DEĞİL) denetimden geçti: sızıntı 0, hücreler birebir yeniden üretildi, r60 ham fiyattan tuttu, e-posta repoda yok. Düzeltmeler: YEOTK 3Ç kârı ≈827 mn TL (864 değil), CENX'te S-3 kaydı var. Süreç zayıflığı: K57-C ön kaydı ölçümden önce commit edilmedi",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-10", "istek": "İz bulmamız gerekiyor, neyi yanlış yapıyoruz ya da yapmıyoruz; ayrıca AMZN'de SMA üstüne atılım iz mi",
     "yapilan": "Ana model denetimi: K57 hücrelerinde %95 aralık yarı genişliği n <= 30'da ~%17, 30-100'de ~%13 -> küçük etki görünmez. İş tanımı K58 (Ç151) alt ajana: ön kayıt 19:19 UTC, git 657c2a1 19:21, koşu 19:22-19:46; güç simülasyonu, French pozitif kontrol, portföy cetveli kalibrasyonu, SMA200 filtresi. Denetim: kodda eşik değişmedi (mühür 5aec67198fe9), güç n 300 / 3000 / δ +%2 ve UMD yıllık 7,3 / 2,5 / 3,7 bağımsız yeniden üretildi",
     "sonuc": "Yanlış yaptığımız: olay cetveli küçük etkiyi göremiyor (güç <= %21). Kalibre aday: portföy cetveli (ABD momentum tutar, plasebo 0/200). SMA atılımı: hisse düzeyinde ABD eksi, endekste düşüşü yarıya indiriyor ama getiri %68'de kalıyor (iz değil, risk aracı). Karar Cemal'de: portföy cetveli benimsensin mi",
     "durum": "TAMAMLANDI, AÇIK: Cemal'in standart kararı"},
    {"tarih": "2026-11-11", "istek": "Son iz bulma operasyonlarından hangisi doğru yol, hangisi yanlış, hangisi eksik; yol göster, diğer modeller yapsın. Defteri yalnız sen değiştir. Ana hedef iz + gerçek kazanç; artık gerçek parayla deniyoruz",
     "yapilan": "YOL_HARITASI_11Kas.md (operasyon operasyon sınıflama + araştırma programı kuralları); CLAUDE.md'ye 'Defter yetkisi' ve 'Ana hedef ve gerçek para modülü'; ONERI_DEFTERI.md (gerçek pozisyonlar, üç kapı, karne). Alt ajanlar: EVREN_SECENEKLERI.md (batanlar dahil evren), SINYAL_ENVANTERI.md (120 sinyal, 13 aile; 70 bugün hesaplanır), öneri karnesi (karne.py, KARNE_11Kas.md). Denetim: alt ajanlar defterlere dokunmadı; karnede DGXX / IWM / XU100 satırları bağımsız tuttu",
     "sonuc": "Yanlış yol: şekil / parmak izi, sıçrama kovalama, şart ekleyerek daraltma. Doğru fikir yanlış cetvel: olay süzgeçleri (n < 1.000 'İZ DEĞİL'ler ÖLÇÜLEMEDİ). Erken karne: sıralamam elediklerimi geçmedi (ABD -1,0, BIST -3,6 puan; şanstan ayrılmıyor); YEOTK +%15, DGXX maliyete göre +%7,5",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-11", "istek": "YEOTK ve DGXX'i seçtiren mantığı geçmiş olaylarda sına; tutmadı diye veriyi çöpe atma; bütün metrikleri test et, alt modellere yaptır",
     "yapilan": "K59 (Ç152): ön kayıt 05:48 UTC, git 9e04f3e 05:50, koşu 05:51-05:57; 9 sinyal + COMP4 + COMP9 + DOSYA_Y / DOSYA_D / DOSYA_YD + UCUZLUK, U1 (1.411) ve U2 (4.261) ABD, BIST bilgi; plasebo 200. Denetim: mühür aynı, kodda eşik değişmedi, 6 sonuç aylik_getiri.csv'den bağımsız yeniden hesaplandı ve tuttu",
     "sonuc": "PORTFÖY-ADAY YOK. COMP4 U2 +%5,5 / yıl (t 2,30, alfa t 2,87) ama son %30 ayda -%0,06 / ay: tutmaz; U1 -%1,6. DOSYA_Y U2 +%5,1 (aynı nedenle tutmaz), DOSYA_D -%10,5. Momentum U1 +%11,9 (Ocak 2021 GME'ye bağlı), U2 -%2,8: ters işaret. BIST'te zirveye yakınlık +%16,6 (bilgi). Asıl eksik: 66 aylık temel veri ve yaşayan evren",
     "durum": "TAMAMLANDI, AÇIK: K59-B, K60 veri hazırlığı"},
    {"tarih": "2026-11-11", "istek": "Sonuca giden işleri yaptır; bütün iz olabilecek metriklerin olasılıklarını hesaplat; 'bu yapıldı' değil 'bu var, şu yok' de",
     "yapilan": "CLAUDE.md 'Sonuç dili' (bulgu + olasılık tablosu). K59-B (Ç153): ön kayıt git 5b3475a 10:46, koşu 10:47-10:51; denetim: 3 COMP4 hücresi ve French VW 2000-son bağımsız tuttu, kodda yalnız rapor değişti. K60 veri: Yahoo 2010+ (4.678 hisse), SEC çerçeveleri 2009+ (1.781 dosya, Cemal'in e-posta izniyle; e-posta repoda yok). K60 kütüphane Faz 1 alt ajanda",
     "sonuc": "K59-B TUTMAZ. VAR: kârlılık / COMP4 geniş evrende +%5-7 / yıl (tek evren, sınırda); düşmüş hisse almak eksi; BIST zirveye yakınlık +%16,6 (bilgi). YOK: momentum ve küçüklük (ters işaret), harman 2000 sonrası piyasadan ayrışmıyor. Sıradaki sonuç: K60 olasılık tablosu",
     "durum": "TAMAMLANDI, AÇIK: K60"},
    {"tarih": "2026-11-11", "istek": "(devam) Bütün metriklerin olasılık tablosu: hangi özellik +%100 ve -%50 olasılığını kaç kat artırıyor",
     "yapilan": "K60 (Ç154): ön kayıt, KEŞİF, DOĞRULAMA, KASA sırayla; her adım öncesi git kaydı. KASA'dan önce asimetri eki yazıldı (R2 tek başına oynaklığı ölçüyordu). Denetim: mühür / kod sha aynı, 11 hücre bağımsız yeniden üretildi, sıra git zamanlarıyla tuttu",
     "sonuc": "İZ ADAYI YOK, ASİMETRİK FIRSAT YOK. VAR: piyango ucu (ikiye katlanma 2-2,7 kat, yarıya inme 2,8-3,8 kat, medyan eksi; 59 çift, üç dönem) ve güvenli uç (COMP4, DOSYA_Y: yarıya inme olasılığı yarı yarıya az). Taban: +%100 olasılığı %4-7, -%50 olasılığı %6-7",
     "durum": "TAMAMLANDI, AÇIK: K60-B, K61"},
    {"tarih": "2026-11-11", "istek": "(devam) İz yoksa durma: oynak hisseler içinde kazananı ayıran özellik",
     "yapilan": "K60-B (Ç155): ön kayıt git 5aac5de, tek koşu (KEŞİF seçimi mekanik, sonra DOĞRULAMA ve KASA). Denetim: 5 hücre bağımsız tuttu, testler geçti, defter dosyalarına alt ajan dokunmadı. ONERI_DEFTERI'ne risk süzgeci eklendi",
     "sonuc": "Oynak havuzda taban: ikiye katlanma %9-16, yarıya inme %17-21. Koruma var (kârlı + seyreltmeyen: yarıya inme 0,6-0,8 kat). Kırmızı bayraklar var (ters bölünme 2-2,4 kat; zarar, raf, nakit yakma, ihraç 1,3-1,6 kat). Kazanma olasılığını güvenilir artıran tek aday havuz içi yüksek beta (1,3-1,45 kat; boğa etkisi olabilir)",
     "durum": "TAMAMLANDI, AÇIK: K60-C, K61, Tiingo kararı"},
    {"tarih": "2026-11-12", "istek": "VDYT: volatilite sıkışması, bitiş tetikleyicileri ve yön araştırması (ayrı motor; Çöl Yolu ve IZ_KARNE ölçütleri değişmez); analist revizyonu bittikten sonra",
     "yapilan": "Faz 1 alt ajanda: veri envanteri, eksik veri raporu, test sırası ve şemalar, ön kayıt (bütün sıkışma tanımı alternatifleri, eşikler, pencereler, walk-forward, temel model ve başarı ölçütü ölçümden önce), kod + sentetik test. Hacim ve şekil ölçüleri kapalı konulara değiyor: Cemal açıkça istedi, yalnız VDYT içinde ölçülür",
     "sonuc": "Ç162: sıkışmanın bitişi basit kontrolden iyi tahmin ediliyor ama bu sıkışmaya özgü değil (rastgele bölgelerde aynı) ve büyük ölçüde mekanik; süre uzadıkça bitme olasılığı AZALIYOR; bilanço günü sıkışmayı ~3 kat sık bitiriyor; korunmuş savunma hattı yukarı kırılmayı +10..+22 puan artırıyor ama bağımsız katkısı yok; portföy para etmiyor (ABD -%33 WF)", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-12", "istek": "Çöl sonrası getiriyi açıklayan DIŞ BİLGİLER: (1) BIST PEAD birebir tekrar, (2) analist revizyonları, (3) emir akışı, (4) 52 hafta zirvesi, (5) şirket kalitesi, (6) hisse ödünç verme; çöl tanımı ve cetvel değişmeden",
     "yapilan": "Altı araştırma, her biri ön kayıt -> git -> ölçüm -> bağımsız denetim: K62 (Ç158), K62-B (Ç160), K67 (Ç161), K63 veri erişimi (Ç157), K64 + K65 (Ç156), K66 (Ç159). Denetim: her işte 2-4 hücre çıktı dosyalarından yeniden üretildi, hepsi tuttu; mühürler ve kod sha'ları koşularda aynı; koşular commit'ten sonra",
     "sonuc": "Hiçbir dış bilgi çöl sinyaline ek bilgi vermiyor (68 değişken-yön, hepsi İZ DEĞİL). VAR: BIST PEAD makalesi yeniden üretildi (SUETF %4,05, EAR %2,82; makale %2,94 / %2,18) ve 2022-26'da büyüdü (%6,5-8,3); ama alınabilir uzun bacak proje cetvelinde tutmadı. ABD çöl dışında kapatma günü yüksek = 60 günde -1,5..-2,5 (bilgi). Emir akışı ve BIST analist verisi YOK; EPS revizyonu ve ödünç ücreti ücretli",
     "durum": "TAMAMLANDI, AÇIK: VDYT (sürüyor); ücretli veri kararları (Alpha Vantage, IBorrowDesk) Cemal'de"},
    {"tarih": "2026-11-12", "istek": "VDYT son teslim kararları: grafikler Drive'a parça parça değil Colab'da mevcut tablolardan yeniden üretilsin (başarılı ve başarısız); ücretli veri yok, önce tam İZ veri envanteri ve gerçek eksikler; Alpha Vantage ücretsiz pilot (haber, duyarlılık, bilanço, olay; BIST / KAP örtüşmesi); Tiingo yalnız kanıtlanmış fiyat açığı varsa; IBorrowDesk VDYT dışı ayrı hipotez; ücretli öneri için karar tablosu; abonelik yalnız Cemal'in açık onayıyla. Ç161 değişmez",
     "yapilan": "Üç alt iş: VDYT_GRAFIK.py (paket + Colab çizimi; VDYT.py değişmez), tam İZ veri envanteri + fiyat kapsam açığı + ücretli veri karar tablosu, Alpha Vantage demo pilotu",
     "sonuc": "SÜRÜYOR", "durum": "AÇIK"},
    {"tarih": "2026-11-12", "istek": "ANA GÖREV (Cemal, 'dur, dallandı'): VDYT küçük mum kümesinden büyük hareketi önceden tespit ve yön; üç başarı ayrı; canlı her hisse çıktısı; Colab'da yeniden üretilebilir grafik; ücretli veri yok",
     "yapilan": "VDYT2 (Ç163): ön kayıt git f13b96e -> WF -> KASA tek açılış -> canlı tablo -> grafik paketi; v1 dersleri (mekanik genişleme, konum kaynaklı yön) baştan kapatıldı; denetim: (1) KASA hücreleri bağımsız tuttu, test 16/16",
     "sonuc": "(1) bölgeyi bulmak BAŞARILI ama duyarlılık çok düşük ve kısmen mekanik olabilir; (2) genişleme zamanı BAŞARISIZ (sıkışmaya özgü değil); (3) yön BAŞARISIZ; ABD bilanço günü bölgeyi bitiriyor; canlıda aday sınıfı verilmedi",
     "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-12", "istek": "Cemal: (1)'in mutlak hareket sağlaması ve Tiingo ile batanlar dahil sağlama; önce ön kayıt; başarısız örnekleri dışarıda bırakma; Tiingo'nun batanları eksiksiz verdiği varsayılmasın, önce bilinen başarısız sembollerle doğrula",
     "yapilan": "VDYT2-B ön kayıt (git 8581767): A mutlak sağlama koşuldu (Ç164); B için Tiingo listesi anahtarsız indirildi (2.219 batan / çıkmış ABD sembolü evreni, 450 tabakalı örneklem + 12 pilot, çekimden önce sabit); Tiingo anahtarı ağ vekiline kaydedildi ama Tiingo iki girişte de 'Auth Token was not correct' dedi",
     "sonuc": "A: (1) mutlak ölçüyle BAŞARISIZ; VDYT2'nin bölge bulma başarısı tanımsal. B: anahtar hatası yüzünden bekliyor (pilot ve çekim hazır)",
     "durum": "TAMAMLANDI, AÇIK: B (Tiingo anahtarı)"},
    {"tarih": "2026-11-12", "istek": "QMLS bilanço sonrası düşüyor (2,98 $, -%7,3); kalanı satıp kurtulsam mı",
     "yapilan": "Birincil kaynak (10-Q ve 8-K, 10 Kas 2026; alt ajan): gelir 14,8 M$ (çeyrekte 2,2 kat), düzeltilmiş FAVÖK +3,7 M$ (ilk pozitif), RPO 515 M$ (3 kat); ama faaliyet zararı -41,6 M$, nakit 31 M$ (kısıtlı dahil) karşısında borç + kiralama ~248 M$, 3Ç'te %9,4 seyrelme, going-concern ifadesi aynı, NT 10-Q yok; kilit 180 gün (12 Oca) ya da altı ay (19 Oca 2027) belgede çelişkili, dolaşımın ~%40'ı. Yazılı kurala göre tetik yok; karar Cemal'in",
     "sonuc": "Kural: şimdi zorunlu satış yok, en geç 8 Oca 2027; ekleme yok", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-12", "istek": "Cemal: Tiingo batanların OHLC'sini örneklerle doğrula; algoritma insan gözünün gördüğü sıkışmayı yakalıyor mu, önce ölçülebilir işaret; veri dalını kalıcılaştırmakta acele yok; Aralık kotası yalnız kanıtlanmış fikre",
     "yapilan": "Tiingo OHLC doğrulaması (12 bilinen batan sembol: 8 tam, 3 kısmen, 1 yanlış seri; VDYT2B_OHLC_DOGRULAMA.md). Kör test ön kaydı (git 7ef1e9d, mühür 6a99e21a9095, anahtar 73da87f12549): 40 grafik (16 G5, 16 kontrol, 4 batan G5, 4 batan kontrol), ad / tarih / grup yok; Cemal işaretleme sayfası (artifact FBuMnv4WhMYhdnMhQvp2yA, db 'cevap')",
     "sonuc": "Tiingo OHLC KISMEN (8/12 tam). Kör test Cemal'in işaretini bekliyor; kural önceden yazılı: BAŞARILI (p_G5>=0,70, p_K<=0,35, kappa>=0,40, Fisher p<0,05) ya da ZAYIF İŞARET (p_G5>=0,60, fark>0) ise Aralık kotası yalnız VDYT2-B testi B'ye; İŞARET YOK ise kota harcanmaz",
     "durum": "TAMAMLANDI, AÇIK: Cemal'in 40 işareti"},
    {"tarih": "2026-11-13", "istek": "Cemal: kör test grafiklerinin hepsi aynı görünüyor, mum/fitil boyu ayırt edilmiyor; gerçek mum grafiği olmalı",
     "yapilan": "Neden: veri gerçekti ama her grafik kendi 120 barlık aralığına gerilmişti (otomatik ölçek). KOR_TEST v1.1 (SAPMA 1, git 9f0c987, 0 işaret varken): aynı 40 nokta, 250 bar, ortak logaritmik ölçek (%1 mum her grafikte aynı boy), %10 cetveli; anahtar (73da87f12549), gruplar, sorular, eşikler aynı. Sayfa yenilendi (artifact sürüm 2)",
     "sonuc": "Denetlendi: anahtar sha aynı, 40/40 PNG manifestle aynı, testler geçti; grafiklerde oynaklık farkı artık görünüyor", "durum": "TAMAMLANDI, AÇIK: Cemal'in 40 işareti"},
    {"tarih": "2026-11-13", "istek": "Cemal: 'Çok aptalca, hiçbir belirti / özellik yok, rastgele seçilen bölge' (kör test v1.1 grafikleri)",
     "yapilan": "Kör test sonucu önceden yazılı kurala göre İŞARET YOK (Ç166); cevap uydurulmadı. Aralık Tiingo kotası VDYT2-B'ye harcanmayacak. Sıradaki: G5 ve basit ölçüler Cemal'in daha önce gözle işaretlediği çöllere (kalibre_etiketler 30 COL + 8 OLUMSUZ; COL_GOZ kutuları) karşı sınanıyor (GOZ_G5, ön kayıtlı)",
     "sonuc": "G5 insan gözüyle tutmadı; kota korunuyor", "durum": "TAMAMLANDI, AÇIK: GOZ_G5 ölçümü"},
    {"tarih": "2026-11-13", "istek": "(Ç166 devamı) G5'i Cemal'in mevcut göz etiketleriyle sına",
     "yapilan": "GOZ_G5 ön kayıtlı ölçüm (alt ajan); ana model denetimi: sıra, yasak dosyalar, A oranları ve iki AUC yeniden üretildi",
     "sonuc": "G5 Cemal'in çöllerinin 1/29'unu yakalıyor (rastgele %0,5, olumsuz 2/8): UYMUYOR. Basit şekil ölçüsü aday yok (en iyi 0,77; olumsuza karşı 0,68). Göz çölü olumsuzdan şekille ayırmıyor", "durum": "TAMAMLANDI, AÇIK: VDYT hattının kapanması Cemal kararı"},
    {"tarih": "2026-11-13", "istek": "Cemal: fon krizinde 1 TL'ye inmiş hisselerin tavan serileri (TEHOL, PEKER); KAP ne diyor, kim alıyor, tavana katılmak mantıklı mı; devasa hacim barı; 4-5 hisse sırala",
     "yapilan": "Canlı tarama (64 çökmüş, 26 tavan serisinde), TAVAN_SERISI k ölçümü (Ç168), hacim / taban fiyat ölçümü (Ç169), 26 hissenin KAP / SPK / bilanço dosyası (iki alt ajan, /tmp/tavan/kap_grup1-2.md); ana model denetimi: iki KAP bildirimi kaynaktan, iki hücre olay dosyasından",
     "sonuc": "Ölçülmüş sinyal yok (tavana katılmak eşlerden kötü; hacimli tavan piyango). Dosya sırası (izleme, öneri değil): SEGMN, TKNKA, GIPTA, SVGYO, KARCL; TEHOL / PEKGY kayyım: uzak", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-13", "istek": "Cemal: 'emare vardır, geniş açıdan bak, fazla ajan, web, son bir kontrol'",
     "yapilan": "4 paralel alt ajan: literatür (fire-sale, SPK manipülasyon), kim alıyor (aracı kurum dağılımı), sosyal / haber, kesit (Ç170); ana model denetimi: kesit sayıları X/Y'den yeniden",
     "sonuc": "Tek aday emare: geri alım bildirimi (tek olay, İZ DEĞİL); ortak kamu tetiği yok; dönüş sırası fon yüküyle", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-13", "istek": "Cemal: 'BofA almış PEKGY, emare; en erken nasıl bulunur; alımından satımına kadar takip et; diğer yabancı kodlar da'",
     "yapilan": "Alt ajan: 4.652 haber arşivi, tutma dönemi ölçümü (Ç171), yayın saati; ana model denetimi: üç hücre olay dosyasından yeniden, ön kayıt sonrası diff yalnız gösterim",
     "sonuc": "BofA / HSBC / bütün yabancı kodlar: İZ DEĞİL; kuruş hisse lot listelerinde işaret ters (-%10 / 60g)", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-13", "istek": "Cemal: 'BofA %40-80 zarar etmez, senin mantığın alıyor mu; bana bir yol gösterecekse ölç'",
     "yapilan": "Alt ajan: BofA maliyet satırlarıyla kendi kârı + 6 ön kayıtlı haber anı koşulu (Ç172); ana model denetimi: 5 hücre satır verisinden yeniden",
     "sonuc": "Yol yok: BofA normal dönemde piyasa gibi (+%3 / 20g), krizde piyasayla kaybetti (-%10); haber sonrası takip eşlerden farksız, kuruş hisse listelerinde ters", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-13", "istek": "Cemal: 'dipte %80-90 düşmüş, dip tutuyor, ucuz noktada BofA alımıyla girsek'",
     "yapilan": "Alt ajan: kurulum tanımı ön kayıtlı, 3 pazar ölçümü + BofA tetiği + bugünkü izleme (Ç173); ana model denetimi: 4 hücre satır verisinden yeniden",
     "sonuc": "Kurulum tek başına piyango (ABD 2023 tuttu, 2024-26 tutmadı, BIST 2016-22 eksi); BofA kriz öncesi hiç böyle dipte almamış (n 0): ölçülemez; izleme HDFGS, SKBNK", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-13", "istek": "Cemal: '5.5 modelin işini kontrol et; her işte yanlışlık var; BofA bile zarar yapıyor, mümkün değil'",
     "yapilan": "Ana model denetimi: ham HTML'den maliyetler (KTLEV 1.10 10,394; TURSG 14.10 5,513) doğru; 2 ayrıştırma hatası bulundu (çok kurumlu haber etiketi, aylık özet), alt ajan düzeltirken 3 hata daha buldu (güncelleme damgası = geleceğe bakma, kenar kuşağı çöpü, numaralı tablo); 3 ölçüm --sapma ile yeniden koşuldu; ana model 6 hücreyi yeniden üretti",
     "sonuc": "Üç karar değişmedi (kanıt yok / yol yok / örneklem yetersiz). BofA'nın kendi maliyetinden sonucu kötüleşti (kriz öncesi 20g medyan -%3,9, kâr oranı %39). Kuruş hisse listesindeki 'ters işaret' kalktı (sıfırı kapsıyor). -%40..-%65 gerçekleşen zarar değil, 20 gün sonraki fiyat; AKD kodu müşteri akışı", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-14", "istek": "Cemal: 'bir yıldır ilerleyemedik; yanlış hesapların kaydını almıyoruz; geçmişe dair bütün hataların kaydını MD defterine yaz'",
     "yapilan": "IK_HATA yapısı + indekste 'Hata defteri' bölümü + test (tam alan, tür, tarih sırası); alt ajan salt okunur tarama (IK_KAYIT Ç01-Ç173, IZ_DEFTERI, COL_OZET, ONERI_DEFTERI, CLAUDE.md, arastirma_cikti raporları, git log): 144 kaynaklı satır + Ç kaydı olmayan dersler; ana model denetimi: H001-H008 COL_OZET §6, H055 / H079 / H097 kaynaklarıyla, H120-H137 bu oturumla karşılaştırıldı, tuttu; CLAUDE.md 'Hata defteri' kuralı",
     "sonuc": "158 hata kayıtlı. En sık: veri, ölçüt (kontrol grubu yanlış kurulmuş 22 kez), süreç, hesap. Düşen iddiaların hepsi iyimserden gerçeğe düştü, tersi yok (sistematik iyimserlik). ~110 satırda karar değişmedi, ~20 iddia geri alındı, 6 madde açık", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-14", "istek": "Cemal: 'iz ararken hatalar önceden okunup göz önünde tutulsun, kod yazmaya öyle başlansın; bütün modeller için; daha iyi öneri var mı'",
     "yapilan": "Ana model: IK_KONTROL 14 maddelik ön uçuş listesi (hata defteri örüntülerinden), ik_kontrol_metni (onkayit / istanimi / defter), ik_kontrol_kapisi (ön kayıttaki tablo eksik / HAYIR ise ölçüm durur), `python IZ_KARNE.py kontrol`, indekste bölüm, test (dolu geçer, eksik durur), CLAUDE.md kuralı",
     "sonuc": "Öneri: okumak yerine mekanik kapı. Her ön kayıtta doldurulmuş kontrol listesi zorunlu; her alt ajan iş tanımı listeyle başlar; raporda KONTROL + HATA başlıkları zorunlu. Mevcut modüllere kapı bir sonraki değişiklikte eklenecek", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-14", "istek": "Cemal: 'yanlış kabul ettiğimiz kurallar sonradan doğru çıkabiliyor; nasıl emin olacağız? yolu varsa önerinden devam'",
     "yapilan": "Ana model: IK_ILERI ileri test defteri (iddia, karar etiketi İZ DEĞİL / ÖLÇÜLEMEDİ / EMARE, n-güç, sabit eşik, veri kesiği, sonraki test tarihi-koşulu, sonuç), indekste bölüm, 7 açık iddia girildi; CLAUDE.md 'Emin olma yolu' + hedefli bağımsız denetim kuralı",
     "sonuc": "Emin olmanın yolu ileri test: sabit eşikle sonraki dönemde yeniden ölç, üç art arda aynı yön = kesin. Bağımsız denetim ajanı yalnız iddia taşıyan (emare / aday / iz) ya da üretimi değiştiren işlerde; büyük n ile 'iz değil' çıkanlarda ana model denetimi yeter", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-14", "istek": "Cemal: 'eski çöller iz değil kaldı; sıkışma sonrası büyük mumların başlama zamanını tahmin eden kodu (VDYT) yeni kontroller ışığında tekrar test et'",
     "yapilan": "İki paralel alt ajan (Fable kotası dolunca başka modelde yeniden): (1) SIKISMA_YENIDEN bağımsız sıfırdan ölçüm, kontrol kapısını kullanan ilk modül (Ç174); (2) VDYT ailesi kod + rapor denetimi, 24 hücre yeniden üretim, eski çöl kayıtlarının güçle yeniden etiketlenmesi (Ç175). Ana model: 4 hücre satır verisinden yeniden, kod satırları doğrulandı, 15 hata satırı, 4 ileri test satırı",
     "sonuc": "Sıkışmadan sonra olağan ölçüde büyük mum GELMİYOR (KAT 0,75-0,98, ters eğilim; güç yeterli); büyük mum algısı tanımsal (göreli KAT 1,6-1,9); zaman tahmini yok; yönsüz stoplu işlem eşlerden farksız (12/12). VDYT ailesinde olumlu iddia kalmadı. En az 20 eski kayıt aslında ÖLÇÜLEMEDİ; yeniden koşu için 5 aday (K24 iki evre önde)", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-14", "istek": "Cemal: 'gözüm küçük mumlardan sonra gelen mumları neden büyük görsün, ayrılık var'",
     "yapilan": "Alt ajan: 5 eşik x 3 referans x 4 sıkışma uzunluğu x 2 eş kümesi duyarlılığı + göz ölçüsü dağılımı + 40 kör grafik (Ç176); ana model: 4 sayı satır verisinden yeniden, tuttu",
     "sonuc": "Göz doğru görüyor: mum sıkışma mumunun 2,7 katına çıkıyor; ama aynı derecede sakinleşmiş her hissede aynı (oynaklığın ortalamaya dönüşü) ve hissenin yıllık normaline göre büyük değil (1,7 x ATR250, eşlerde 1,8-1,9). Hiçbir eşikte / uzunlukta KAT > 1 yok; ABD'de ince eşle KAT 1,00 (nötr), Avrupa 0,79", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-14", "istek": "Cemal: dört aşamalı yeniden ölçüm (K24, D9 + rüzgâr, düzgün dip vs çöl, INTEM ileri test); tek şart: her aşamada aynı ölçüm kriterleri, eşikle oynanmaz",
     "yapilan": "Aşama 1: ORTAK_CETVEL (Ç177) mühürlü cetvel + güç tablosu; ana model kapı ve 14/14 testi çalıştırdı; Aşama 2-4 üç paralel alt ajana aynı ortak kurallar dosyasıyla verildi (K24_YENIDEN, D9_YENIDEN, DIP_COL_AYRIM); Aşama 5 (INTEM ileri test) 2-4 bitince",
     "sonuc": "Cetvel kilitli (sha); 5 aşama bitti (Ç177-Ç181). K24 çöl ÖLÇÜLEMEDİ / TUTMADI (piyango); D9 uzun çöl İZ DEĞİL (sakin hisse seçer); dip vs çöl ayrımı ÖLÇÜLEMEDİ; INTEM ileri ÖLÇÜLEMEDİ (emare zayıfladı); yalnız sektör rüzgârı ABD +%3,6 ama portföy şartı düştü (EMARE, bilinen etki). Eşik oynanmadı. 5 yeni hata (FON_IZI tarayıcı uzunluk şartı geleceğe bakma en önemlisi)", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-15", "istek": "Cemal: 'sıkışma tanımın rastgele bölge seçiyor; tersten gidelim: her büyük mumdan önceki mumların dizilimi, boyu, fitili, eğimi ölçülsün, bölge parmak izi bulunsun, sonra o parmak izinden büyük mum olasılığı ölçülsün'",
     "yapilan": "Ana model iş tanımı: TERS_PARMAK (keşif ABD / AVR 2016-22: büyük mum öncesi ~30 ölçeksiz ölçü vs eşli rastgele kontrol, d / AUC / BH, en çok 3 koşullu P1-P3 kuralı; ön kayıt B ile dondurma; doğrulama 2023 / 2024-26 ileriye doğru KAT; Cemal'in gözü için 40 kör grafik); alt ajan koşuyor",
     "sonuc": "Profil VAR ama hipotezin tersi: büyük mumdan önceki bölge küçük mumlu değil, zaten büyümüş mumlu ve tepeye yakın (P1 KAT 1,3-1,7, dört hücre, ileriye doğru tuttu); küçük mum ölçüleri olasılığı düşürüyor; yön ve 60 gün getiri yok (oynaklık tahmini). Çok günlü hareket öncesi profil: çökmüş + geniş bant (EMARE). Kör set PDF Cemal'in gözüne gönderildi", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-15", "istek": "Cemal: FENER örneğiyle 'kod 3-16 Aralık'ı seçmiş, asıl sıkışma 14 Ekim - 7 Kasım: yatay, dar Bollinger; kodun bölgesi kayıyor ve Bollinger en geniş yerinde'",
     "yapilan": "Ana model ekran fiyatıyla doğruladı (BB yüzdelik 0,02 vs 0,70; net +%4 vs -%6); bölge listesindeki bölünme kirliliği düzeltildi; S4 (Cemal tanımı: küçük mum + dar BB + yatay + >= 10 gün) ön kayıtlı ileri ölçüm alt ajana verildi (SIKISMA_CEMAL)",
     "sonuc": "S4 ÖLÇÜLEMEDİ (n < 1.000); B1 KAT ~1, BH2 < 1; S4 hisseleri iki uçta da daha sakin. FENER: Aralık doğru dışlandı, Cemal'in Ekim-Kasım bölgesi (iv) uzunluk koşulundan kaçtı (tasarım hatası, hata defterinde). Bölge listeleri (S1 düzeltilmiş 3. sürüm, S4) Cemal'e gönderildi", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-15", "istek": "Cemal (FENER, CCOLA, ENJSA grafikleri): 'öbek gibi yan yana sıkışmış mumlar, eğim yukarı olabilir, zıplama mumu görmezden gel, Bollinger daralması bütün bölgelerde şart, yükselişteki bölge dinlenme olmalı taban korunmalı, dip bölgesi de sayılır'",
     "yapilan": "Ana model: 3 seçmeli (FENER 14 Eki-7 Kas, CCOLA 2-15 Eki, ENJSA 10 Tem-14 Ağu 2025) + 4 seçmemeli örneği ekran fiyatıyla ölçtü (BB yüzdelik, konum120, taban, SMA50); S5 taslağı iki sınıf (DİP, YOL ÜSTÜ) + zorunlu BB; alt ajana tasarım sınaması -> ön kayıt -> ölçüm -> liste işi verildi (SIKISMA_OBEK); S4 listesindeki 'bölge = karar - 15 bar' gösterim hatası düzeltilecek (bölge ilk-son gün)",
     "sonuc": "Tasarım 14 / 14; S5 rastgele bölgeleri eledi. Dip sınıfı ABD'de iki dönemde büyük gün olasılığı 1,14-1,17 kat (EMARE, n < 1.000), Avrupa'da yok; yol üstü sınıfı tutmadı; getiri / yön yok. Cemal'in 2x / 3x sorusu: göreli evet, mutlak eşlerle aynı. Pine göstergesi + S5 listesi gönderildi; ENJSA 28 Tem-12 Eyl bölgesi S5'e girmiyor (bant %23)", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-15", "istek": "Yeni oturum: defterden sür (görev günlüğü, açık kalanlar, hata defteri, kontrol listesi); açık iş (4) FON_IZI tarayıcı uzunluk şartı geleceğe bakma düzeltmesi (H178)",
     "yapilan": "Ana model iş tanımı (arastirma_cikti/fon_izi/GELECEK_DUZELTME_IS_TANIMI.md, kontrol listesiyle; ön kayıt commit 9f0aa08 koşudan önce); alt ajan (opus): FON_IZI v1.40, 8 tarayıcıda (fi_k4 / k4b / k6 / k13 / k14 / k17 / k23_parmak / k24) 'toplam uzunluk < N' şartı 'karar günü konumu t >= N-1' oldu, eşikler aynı; fi_k23_parmak gecmis parametresi (bölge hedefleri gecmis=L); test_fon_izi 63 önek değişmezliği (tam seri = kesik seri, 8 fonksiyon) eklendi; gerçek veri eski / yeni sayımı; ikinci alt ajan: test_intem_ileri ve test_k24_yeniden'in eski hatayı SAPMA-1 gerekçesi olarak sınayan bölümleri yeni davranışa çevrildi. Ana model denetimi: ön kayıt sırası tuttu; test 63 eski kodda kırmızı (ayrı süreçte yeniden koşuldu), yeni kodda 63 / 63; 2 hücre bağımsız yeniden üretildi (K24 kural BIST 3.114 -> 2.905, K13 ABD 158 -> 156, birebir); diff yalnız 8 yer + 2 hedef çağrısı + sürüm; sızıntı yok; yasak dosyalar değişmedi; rapor arastirma_cikti/fon_izi/GELECEK_DUZELTME_RAPOR.md",
     "sonuc": "Geleceğe bakma kapandı: 8 tarayıcı kesik seride de aynı sinyali veriyor. Düşen sinyal (31.08.2026 kesik): K24 kural BIST -209 (%6,7) / ABD -515 (%7,6), K17 -21 / -81, K14 eşli -46 / -159, K13 0 / -2, K23 L15 pencere -%9,4 / -%8,4; yeni <= eski 12 / 12 hücre; t < N-1 günleri tekilleştirme durumuna girmediği için 9 hücrede 1-157 yeni satır (alt küme değil; iş tanımı çelişkisi hata defterinde). Eski kararlar değişmedi (Ç75-Ç78, Ç96, Ç113, Ç118, Ç124 zaten ÖLÇÜLEMEDİ ya da yeniden koşuldu). K24_YENIDEN / DIP_COL_AYRIM / INTEM_ILERI Mart 2027 ileri koşularında FON_IZI v1.40 ile sinyal kümesi az değişir (K24 kural BIST +3 / -1, ABD +18 / -1); açık kalanlara yazıldı. Colab: FON_IZI.py değişti, çalışma zamanını yeniden başlat", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-15", "istek": "Cemal: 'Pine kodunu eklerken yükselt diyor, ücretsiz sürümde gösterge sayısı sınırlı'; ekran görüntüleri: Basic planda en çok 2 gösterge; eski CEMAL TEKNIK betiği salt okunur ve satır sarma hatası veriyor; Pine Editor'de Türkçe karakterler bozuk",
     "yapilan": "PINE_NASIL.md 1b-1c: S5 tek göstergedir; grafikteki iki 'Cemal | BB + EMA (Soft Background)' kaldırılır (BB ve EMA S5'in içinde), 'CEMAL TEKNIK' hacim için kalır, toplam 2; Türkçe karakter bozulmasına karşı COL_S5_OBEK_ascii.pine (kod kısmı birebir aynı doğrulandı; ASCII dışı 0, sarmalı satır 0) Cemal'e gönderildi",
     "sonuc": "Satır sarma hatası Cemal'in eski 'CEMAL TEKNIK' betiğinde (table.cell devam satırları 4'ün katı girintili), S5'te değil. Basic planda 'komut dosyası salt okunur, yeni kaydetme için yükselt' uyarısı var: S5 ancak 'Yeni boş gösterge' ile kaydetmeden 'Grafiğe Ekle' çalışırsa kullanılabilir; çalışmazsa gösterge yolu kapalı, S6 için Cemal BOLGE_LISTESI_S5.md tarihleriyle kendi grafiğinde bakar ve hisse + tarih yazar", "durum": "TAMAMLANDI, AÇIK: S5'in Basic planda kaydetmeden eklenip eklenemediği Cemal'den gelecek"},
    {"tarih": "2026-11-15", "istek": "Cemal: 'UZUN ÇÖL ETİKETİNİ KALDIR sektör derle' (karar: T8 etiketi kalkar; AVR sektör listesi derlenip rüzgâr Avrupa'da ölçülür)",
     "yapilan": "SEKTÖR: ana model iş tanımı (D9_AVR_IS_TANIMI.md, kontrol listesiyle); alt ajan (opus): islenmis-veri avr/evren_avr_ham.csv + Wikipedia'dan sektor_AVR.csv (581 sembol, ham ad -> ICB süpersektör eşleme tablosu, 21 sınıf, boş 0), D9_AVR.py (D9_YENIDEN'in derin kopya eşiğiyle yalnız AVR; aynı cetvel; kontrol kapısı + oc_kapi), test_d9_avr 45/45, ön kayıt önceden yazılı dört dallı kararla commit (4a48789) -> koşu 25 sn sonra. Ana model denetimi: sektör dosyası V_AVR ile birebir, D9_YENIDEN globali değişmedi (test), ön kayıt < koşu, 4 hücre satır verisinden yeniden üretildi (birebir), sızıntı yok. (Ç185)",
     "sonuc": "Rüzgâr Avrupa'da ÖLÇÜLEMEDİ: (c) AVR 2023 n 125 -%1,7 [-5,9] güç %29; AVR 2024-26 n 447 +%0,9 [-0,9] güç %52; portföy plasebonun altında. Ç181c EMARE değişmedi (ne güçlendi ne zayıfladı); Mart 2027'de ABD + AVR aynı komutla. Investment Trusts rüzgâr almadı. Yan bulgu: D9_YENIDEN'de kısa + rüzgârlı hissede çökme hatası (Ç181'i etkilemedi; hata defterinde)", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-15", "istek": "Cemal: 'UZUN ÇÖL ETİKETİNİ KALDIR' (T8 / D9 etiketi üretim ekranından; Ç181a İZ DEĞİL)",
     "yapilan": "Üretim kodu değişikliği: ana model iş tanımı (T8_KALDIR_IS_TANIMI.md; §3 heredoc hatası hata defterinde), yazıcı alt ajan (opus) + AYRI bağımsız sınayıcı alt ajan (raporu görmeden 8 madde). COL_v1 D14: ruzgar_listesi artık yalnız sektör rüzgârı özeti ('=== SEKTOR RUZGARI'; uzun çöl hisse listesi ve fon süzgeci kalktı; dönüş rüzgârlı sektör tablosu), bugun_liste 'uzun' sütunu kalktı (hiçbir CSV / pkl şeması taşımıyordu); takip T12: BEKLE 'uzun' sütunu kalktı, ruz% ve RUZGAR bayrağı kaldı; uzun_col_olc, UZUN_* / RUZ_* sabitleri ve sektor_ruzgar birebir aynı (ölçüm referansı). test_takip 8a-8d (eski kodda 8a-8c kırmızı), test_d9_yeniden 22/22, COL_v1 / takip kullanan 11 test yeşil. Sınayıcı: 8/8 madde GEÇTİ, ONAY; ana model: testler + ast + diff kapsamı + sızıntı yeniden. Drive col_tarayici kökündeki COL_v1.py ve takip.py HEAD sürümüne yüklendi (bayt doğrulaması)",
     "sonuc": "Ekranda 'uzun' etiketi yok; sektör rüzgârı (EMARE, bilinen etki) duruyor. Yan bulgu: Drive COL_v1.py 20 Ekim D12'de kalmıştı, Actions D13 ile çalışıyordu (25 gün ayrışma; hata defterinde); bu yüklemeyle Colab ve Actions aynı koda döndü. Colab: COL_v1.py ve takip.py değişti, çalışma zamanını yeniden başlat. Kalan eski yorum satırları (D9 / T8 başlık notları) tarihli not olarak duruyor, D14 / T12 notu geçersiz kıldığını yazıyor", "durum": "TAMAMLANDI"},
    {"tarih": "2026-11-15", "istek": "Cemal (ENJSA ekran görüntüsü, 'COL S6 TASLAK' göstergesi): 'aynı bölge yan yana iki kez seçilmiş, ikincisi tek mum; bölge en az 5-8 mum, ideal 8, çoğu 60 muma kadar'",
     "yapilan": "Ekrandaki 'COL S6 TASLAK (göz testi)' göstergesi bu repodan değil (repoda yalnız S5 var); ama kural S5 Pine'ı da ilgilendiriyor: v1.0 şartın tuttuğu GÜNÜ boyuyordu (bgcolor), bölge ise karar gününden geriye 15 geçerli barlık pencere. Alt ajan (opus): COL_S5_OBEK.pine v1.1 — bölge KUTU olarak çizilir (sol kenar = pencerenin ilk geçerli barı, üst / alt = pencere High / Low, sınıf rengi; şart sürerken ya da ara < 20 barda aynı kutu sağa uzar: bitişik parçalar tek kutu; en az 15 bar), günlük zemin boyası isteğe bağlı (varsayılan kapalı), tabloda son bölge tarih aralığı ve uzunluğu; ölçüm tanımı ve eşikler değişmedi. ASCII kopya yeniden üretildi (kod birebir, ASCII dışı 0). PINE_NASIL güncellendi. Ana model: diff gözden geçirildi (box.new sırası, kapsamlar, tipler); TradingView derleyicisi burada yok, ilk yapıştırmada derleme Cemal'de",
     "sonuc": "KURAL (Cemal, 15 Kas; S6 tasarımına girer): bölge en az 8 mum (5 alt sınır), çoğu en çok ~60 mum; tek mumluk bölge yok; bitişik parçalar tek bölge. S5'te pencere 15 bar olduğu için alt sınır sağlanıyor; üst sınır (~60) ölçüm tanımında yok, bitişik birleşme 60'ı aşabilir (ayrı karar). S6 TASLAK göstergesinin kaynağı Cemal'e sorulur", "durum": "TAMAMLANDI, AÇIK: Pine v1.1 TradingView'de derlenecek (Cemal); S6 TASLAK'ın kaynağı"},
    {"tarih": "2026-11-15", "istek": "Cemal (ENJSA, S5 v1.1 kutusu): 'neredeyse rastgele: bölgenin bir önceki mumu ve sonraki iki mum dahil değil; onlar da kutunun içinde ve küçük mum'",
     "yapilan": "Neden: v1.1 kutusu karar gününden geriye SABİT 15 bar; sınır mumlardan değil sayıdan geliyordu (tasarım eksiği, hata defterinde). Alt ajan (opus): Pine v1.2 — bant = karar günü penceresinin High / Low'u (tolerans girdisi); kutu GERİYE bant içindeki ardışık mumlar boyunca, İLERİYE sonraki mumlar bant içinde kaldıkça (ya da S5 sürdükçe) uzar; ilk bant dışı mumda KAPANIR, en çok 60 bar (girdi); kapanmış kutudan sonraki S5 günü yeni kutu açar (üçgen yine yalnız ara >= 20 gününde); 'genislet' kapalıysa v1.1. Üç sentetik senaryo Python kopyasıyla doğrulandı; ASCII kopya kod birebir. Ölçüm tanımı, eşikler ve karar günü değişmedi; kutunun sağ kenarı sonradan belli olur (gösterim), işlem kararı üçgen günündedir",
     "sonuc": "Bölge sınırı artık mumlardan geliyor. S6 tasarımına kural: bölge = aynı bant içindeki ardışık küçük mumların tamamı; sınır mumdan, sayıdan değil; en az 8, en çok ~60 mum. Cemal v1.2'yi yapıştırıp göstergeyi kaldırıp yeniden ekler; derleme hatası çıkarsa satır ve metin", "durum": "TAMAMLANDI, AÇIK: v1.2 TradingView'de derlenecek (Cemal)"},
]
IK_ACIK: List[str] = [
    "FON_IZI v1.40 ETKİSİ (15 Kas): K24_YENIDEN, DIP_COL_AYRIM, INTEM_ILERI Mart 2027 ileri koşuları ('aynı komut') artık FON_IZI v1.40 tarayıcılarıyla çalışır; sinyal kümesi az değişir (K24 kural BIST +3 / -1, ABD +18 / -1; K23 bölge hedefleri aynı). İleri koşudan önce aynı kesikle eski / yeni sinyal sayımı rapora yazılır, karar kıyasında bu fark not edilir. test_intem_ileri ve test_k24_yeniden SAPMA-1 gerekçe bölümleri yeni davranışa çevrildi (15 Kas).",
    "PINE / TRADINGVIEW (15 Kas): Basic plan 2 gösterge ve 'komut dosyası salt okunur, yeni kaydetme için yükselt' uyarısı. Cemal: iki 'Cemal | BB + EMA' göstergesini kaldırıp S5'i (COL_S5_OBEK_ascii.pine) 'Yeni boş gösterge' ile kaydetmeden 'Grafiğe Ekle' ile dener. Olursa S6 için yanlış boyanan / boyanmayan bölgeleri HİSSE + TARİH yazar; olmazsa BOLGE_LISTESI_S5.md tarihleriyle kendi grafiğinde bakıp aynı listeyi yazar (gösterge yolu kapalı).",
    "ESKİ ETİKET DÜZELTMESİ (Ç175, 14 Kas): İZ DEĞİL yazılı ama güç yetersiz (ÖLÇÜLEMEDİ sayılır): Ç38, Ç39, Ç50, Ç57, Ç67-Ç70, Ç73-Ç83, Ç87, Ç89, Ç90 ve Eylül cetveliyle ölçülenler; indeks tablosundaki eski karar metinleri tarih kaydı olarak kalır, okunurken bu liste geçerlidir. Yeniden koşu sırası: K24 iki evre (Ç96), Ç37 D9, Ç75 / Ç78, Ç124 ileri test, VDYT2 mutlak + oran eşleşmesi; her biri ön kayıtla, PV2 + olasılık tablosu, Cemal 'koş' deyince.",
    "ABD k60 FİYAT VERİSİ (Ç175): 4.678 hissenin 1.235'inde > 3x sıçrama / aşırı aralık (ters bölünme, OTC); ATR / σ ölçüleri bu satırlarda anlamsız. K60 ailesini kullanan her yeni iş önce sıçrama temizliği (|ln getiri| > ln 3 günü ve öncesi 250 bar dışlanır) kuralını ön kayda alır. VDYT satır verisi yalnız konteynerde (/tmp/vdyt*, /tmp/sikisma): kalıcı yere alınması Cemal onayı ister (yeni veri dalı).",
    "YENİ OTURUM BAŞLANGICI (15 Kas 2026): önceki dal PR #3 ile main'e birleştirildi (96e189b); 15 Kas öğleden sonraki iş (FON_IZI v1.40, Pine notları) ccr-27195a1e-djv6v3 dalında; yeni oturum bu dal main'e birleşmişse main'den, birleşmemişse bu daldan başlar. Sıradaki işler: (1) Cemal Pine göstergesini (COL_S5_OBEK_ascii.pine v1.1, bölge = kutu) TradingView'e ekleyip (Basic plan: en çok 2 gösterge) 'yanlış boyanan / boyanmayan' bölgeleri HİSSE + TARİH olarak yazacak -> S6 tasarım sınaması (tampon ± 5 gün, örtüşme oranı, CEMAL KURALI: bölge en az 8 mum / 5 alt sınır, çoğu <= ~60 mum, tek mumluk bölge yok, bitişik parçalar tek bölge) -> yeni ön kayıt -> aynı cetvel; ekranındaki 'COL S6 TASLAK' göstergesi bu repodan değil (kaynağı sorulacak); (2) S5_DİP EMARE ileri testi Haziran 2027; (3) Cemal kararları 15 Kas: T8 etiketi kaldırıldı (D14 / T12), AVR sektör listesi derlendi (Ç185 ÖLÇÜLEMEDİ); S4 (iv) kuralı hâlâ açık; (4) FON_IZI uzunluk şartı düzeltmesi YAPILDI (15 Kas, v1.40, H178 düzeltme notu); (5) Fable kotası 18 Kas'a kadar dolu, alt ajanlar opus ile. Hata defteri son satırları ve kontrol listesi okunmadan iş başlamaz.",
    "CEMAL KARARI (15 Kas, Ç183): S4 (iv) uzunluk koşulu bölge içi ölçülerle mi sayılsın (FENER 14 Eki - 7 Kas gibi 15-25 barlık yatay bölgeler girsin diye)? Evet derse yeni ön kayıt (S5), eşikler önceden; Cemal'in işaretlediği 3-5 örnek bölge tasarım sınaması olarak ÖNCE alınır.",
    "DÖRT AŞAMA SONRASI (14 Kas, Ç177-Ç181): (1) FON_IZI tarayıcılarında seri toplam uzunluğu şartı (fi_k13 / fi_k17 n<400, fi_k24 n<200, fi_k23_parmak n<L+200) geleceğe bakıyor -> ayrı iş: t anı konumuna çevrilecek, test eklenecek (FON_IZI yasak dosya değil, ölçüm modülü; ana model iş tanımı yazar). (2) YAPILDI 15 Kas: T8 'uzun çöl' etiketi kaldırıldı (COL_v1 D14 / takip T12; bağımsız sınayıcı ONAY; Drive güncellendi). (3) YAPILDI 15 Kas: AVR sektör listesi derlendi (sektor_AVR.csv), rüzgâr Avrupa'da ÖLÇÜLEMEDİ (Ç185). (4) ORTAK_CETVEL v1.1: oc_hucre kararlı sıralama; yalnız dört aşama ileri testleri bittikten sonra, yeni sürüm olarak.",
    "KONTROL KAPISI (14 Kas): mevcut ölçüm modüllerine (FON_IZI kos, BOFA_IZI kos / karkos / dipkos, GENIS_KESIT, TAVAN_SERISI kos / hacim, KOR_TEST, GOZ_G5) ik_kontrol_kapisi çağrısı ve ön kayıtlarına KONTROL LİSTESİ eklenecek (alt ajan işi; bir sonraki değişiklikte, ön kayıt sırası bozulmadan). NOT (15 Kas): FON_IZI'de tek 'kos' yok, 20 alt komut (k9indir ... k26) ve ön kayıt dosyası yok; eski k13-k26 komutları tarihçedir, yeniden koşulmaz; kapı ancak yeni ölçüm açan bir FON_IZI komutuna ortak ön kayıt yoluyla konur (tasarım ana modelde).",
    "HATA DEFTERİ (14 Kas): doğrulanacak 4 madde: Ç84 denetim PDF'indeki ~15 küçük hata satır satır girilmedi (IZ_KARNE_ders7_denetim.pdf); H024 dar_hafta_olc ve H045 üretim 11 hatası düzeltildi mi (takip.py okunacak); 20-24 Ekim FON_IZI commit'leri git log'da yok, o dönem yalnız defter notlarından; H136 / H137 kaynağı sohbet (13 Kas).",
    "DİPTE BofA (Ç173, 13 Kas): kriz öncesi olay yok, ölçülemez; kriz sonrası HDFGS (21.10) ve SKBNK (05.11) BİLGİ olarak izlenir, karara girmez. Kurulum listesi (10 hisse) izleme; öneri değil.",
    "BofA / YABANCI AKD (Ç171-Ç172, 13 Kas): İZ DEĞİL, YOL YOK; K1 / K2 (pay >= %20, maliyete yakın giriş) n < 30: maliyetli liste arşivi büyüyünce aynı ön kayıtla yeniden koşulabilir (Haziran 2027 sonrası, kriz kuralıyla).",
    "BofA / YABANCI AKD (Ç171): BOFA_IZI bi_izle_tur zamanlanmadı (gerekmez). Ücretli canlı AKD (ForInvest / Matriks) önerilmez: ücretsiz liste sinyali yok.",
    "GERİ ALIM EMARESİ (Ç170, 13 Kas): çöküş sonrası geri alım bildirimi -> dönüş, tek olayda q 0,003; 2018 ve 2020 BIST çöküşlerinde ve ABD'de ön kayıtla sınanacak.",
    "TAVAN / FON KRİZİ DÖNÜŞÜ (13 Kas): izleme SEGMN, TKNKA, GIPTA, SVGYO, KARCL (ölçülmüş sinyal yok, ONERI_DEFTERI izleme). Kriz sonrası tavan / hacim olaylarının sonucu Mart 2027 sonrası TAVAN_SERISI ile ölçülür (ertesi gün tavan %56-82, geçmişte %35-40). Tarihler: 30 Kas MSCI çıkarması, 9 Ara TEHOL / PEKGY 3Ç.",
    "DURUM (12 Kas): DIŞ BİLGİ turu (Ç156-Ç161) ve VDYT (Ç162) bitti. Dış bilgiler çöle ek bilgi vermiyor (68 değişken-yön İZ DEĞİL); BIST PEAD makalesi yeniden üretildi. "
    "VDYT: genişleme tahmini basitten iyi ama mekanik ve sıkışmaya özgü değil; süre uzadıkça bitiş olasılığı azalıyor; bilanço günü sıkışmayı bitiriyor; savunma hattı yönle ilişkili "
    "ama bağımsız değil; portföy para etmiyor. VERİ YOK / ÜCRETLİ: emir defteri, BIST analist ve KAP özel durum, ödünç ücreti (IBorrowDesk 29 $/ay), EPS revizyonu (Alpha Vantage 49,99 $/ay), "
    "batan ABD şirket fiyatları (Tiingo): kararlar Cemal'de.",
    "KARARLAR (Cemal, 12 Kas): ücretli veri şimdilik YOK, hiçbir abonelik Cemal'in açık onayı olmadan başlatılmaz; ücretli öneri ancak karar tablosuyla (eksik tür, mevcut kaynak, eksik aralık, sağlayıcı kapatıyor mu, maliyet, beklenen katkı); Tiingo yalnız kanıtlanmış fiyat kapsam / kalite açığında; IBorrowDesk VDYT dışı, ileride ayrı hipotez (açığa satış baskısı, ödünç bulunabilirliği); Ç161 kararı değişmez, yeni sonuçlar eski karar kayıtlarını geriye dönük değiştirmez.",
    "VERİ (12 Kas, arastirma_cikti/veri_envanteri/): IZ_VERI_ENVANTERI.md: VDYT'nin 'eksik' dediklerinin bir kısmı elde (ABD 8-K madde kodları islenmis-veri k55/sec_ozet.json; ABD saatli bilanço takvimi /tmp/k67_yahoo) ya da ücretsiz (Borsa İstanbul bülteninde kotasyondan çıkanların OHLC'si; KAP özel durum API'si). Gerçekten eksik: ABD batan şirket fiyatı (kanıtlı açık: 2016'da işlem görenlerin %44'ü sonradan çıkmış; Tiingo ücretsiz katmanı 2016+ kapatır, karar Cemal'de), hisse eşlemeli tarihsel haber, makro sürpriz, gün içi veri, BIST analist. KALICILIK RİSKİ: /tmp/k67_yahoo, /tmp/k62_veri, /tmp/k60_secframes, /tmp/k60_fiyat yalnız konteynerde (islenmis-veri dalına alınmalı). evren_disi_ABD.csv repoda YOK (*.csv kuralı; COL_YOLU_ABD.py yeni ortamda durur): Drive'dan alınıp .gitignore istisnasıyla main'e konmalı. AV_PILOT.md: Alpha Vantage haberi premium (ücretsiz anahtar açmaz), bilanço verisi Yahoo ile aynı, delist listesi eksik ve fiyatsız (Tiingo yerine geçmez), BIST yok.",
    "TIINGO (12 Kas): KÖR TEST İŞARET YOK (Ç166, 13 Kas): Aralık kotası VDYT2-B'ye HARCANMAZ. GOZ_G5 (Ç167): G5 Cemal'in göz etiketlerine de uymuyor (1/29); şekil ölçüleri çölü olumsuzdan ayırmıyor. ÖNERİ (Cemal kararı): VDYT / sessiz bölge şekil hattı kapansın; Aralık kotası başka işe (ör. sıkı dosya batan kontrolü) ayrılabilir. (Eski kural:) Aralık kotası ancak kör test (KOR_TEST_ON_KAYIT.md) BAŞARILI ya da ZAYIF İŞARET çıkarsa kullanılır; İŞARET YOK ise kullanılmaz, G5 dedektörü düzeltilir. Kör test sayfası: claude.ai/artifact/FBuMnv4WhMYhdnMhQvp2yA (v1.1 grafikler: 250 bar, ortak log ölçek; Cemal 40 grafiği işaretler; sonra db cevap -> KOR_TEST.py olc). Veri dalını kalıcılaştırma Cemal kararıyla ertelendi. Batan OHLC doğrulaması: 12 bilinen sembolün 8i tam, 3ü kısmen, SUNE yanlış seri. anahtar çalışıyor; pilot KISMEN (Ç165); Kasım ayı 500 sembol kotası dolu (EVREN2 1-2 Kas). B için 1 Aralık 2026'da `TIINGO_API_KEY=proxy-injected python VDYT2B.py cek` (498 sembol; Aralık'ta başka Tiingo işi koşulmamalı) sonra `python -I VDYT2B.py kos --test B`. DİKKAT: B, /tmp/vdyt2/kasa tabloları ve /tmp/k60_fiyat'a bağlı; konteyner kaybolursa VDYT2 KASA kapısı yeniden koşuya izin vermez: veriler önceden islenmis-veri dalına alınmalı (karar Cemal'de). Sonra: python VDYT2B.py pilot (12 istek) -> GÜVENİLİR / KISMEN ise python VDYT2B.py cek (~10-11 saat, saatte 45 istek) -> python -I VDYT2B.py kos --test B. Ayda 500 sembol sınırı: bu iş 498 kullanır.",
    "DRIVE VDYT2 (12 Kas): 'COLAB_VERILER/OUTPUT/VDYT/v2_20261112/' klasöründe VDYT2_RAPOR_kasa.md, VDYT2_ON_KAYIT.md, vdyt2_canli_2026-11-12.csv, vdyt2_grafik_paket.tar; VDYT.py ve VDYT2.py 'col_tarayici' kökünde (boyutlar repoyla aynı). Grafikler Colab'da: tar açılır, VDYT2.py ciz --paket .../grafik_paket/{wf,kasa} (240 PNG; bu konteynerde Colab benzetimiyle denendi). SIRADAKİ (önceden yazılı, karar değiştirmez): (1)'in mutlak hareketle sağlaması (büyük hareket = 20 günde |getiri| >= 2 x ATR250 ya da >= %15); duyarlılığın düşüklüğü (%1-2) nedeniyle bölge tespiti pratikte nadir uyarı üretir.",
    "DRIVE (12 Kas): VDYT çıktıları 'COLAB_VERILER/OUTPUT/VDYT' klasöründe: VDYT_RAPOR.md, VDYT_raporlar.zip, vdyt_grafik_paket_wf.tar, vdyt_grafik_paket_kasa.tar; VDYT_GRAFIK.py 'col_tarayici' kökünde (yükleme boyutları repodakiyle aynı). Grafikler Colab'da paketten yeniden üretilir: !python /content/drive/MyDrive/col_tarayici/VDYT_GRAFIK.py ciz --asama hepsi (özgün kipte 240/240 PNG bayt bayt aynı; v1 sinyal grafiği başlığındaki grup adı sızıntısı normal kipte kaldırıldı).",
    "DURUM (11 Kas akşam): K60 (Ç154) + K60-B (Ç155) bitti: 77 sinyal + 12 bileşik, 2012-2026, üç dönem. İZ ADAYI YOK (piyasayı üç dönemde geçen portföy yok). "
    "OLASILIK TABLOSU VAR: taban +%100 olasılığı %4-7, -%50 olasılığı %6-7; oynak havuzda %9-16 ve %17-21, medyan eksi. Havuz İÇİNDE KORUMA: kârlı / seyreltmeyen / "
    "likit (COMP4, DOSYA_Y, ROA üst) yarıya inme olasılığını 0,6-0,8 kata indiriyor, ikiye katlanma aynı kalıyor. KIRMIZI BAYRAKLAR: ters bölünme (2-2,4 kat), zarar, raf kaydı / "
    "raftan satış, nakit yakma, hisse ihracı, zirveden uzaklık, çok küçük / çok düşük fiyat (1,3-1,6 kat batma; kazanma artmıyor). ONERI_DEFTERI'ne risk süzgeci olarak işlendi. "
    "SIRADAKİ (önceden yazıldı): K60-C kırmızı bayrak sayısına göre olasılık (tanımlayıcı); K61 dalga 2 (Form 4 içeriden alım, açığa satış, 8-K 1.01 sözleşme: DGXX tipi seçimin asıl testi); "
    "batanları içeren veri (Tiingo kararı Cemal'de).",
    "DURUM (11 Kas): K59 (Ç152) portföy cetveli v2 ile 9 basit sinyal + COMP4 + DOSYA ailesi: PORTFÖY-ADAY YOK. Cetvel güvenilir (plasebo net %0, brüt %1,5). "
    "En yakın: geniş evrende kârlılık / COMP4 / DOSYA_Y (YEOTK tipi) yıllık +%5 ama son 20 ayda sıfır (kıl payı) ve bilinen faktörlerle açıklanıyor; "
    "momentum ve küçüklük iki evrende ters işaretli; DOSYA_D (DGXX tipi vekil) -%10; 'düşmüş yarı' zirveye yakın yarının gerisinde. KÖK EKSİK: temel veri "
    "yalnız 2021-26 (66 ay) ve yalnız yaşayan hisseler. SIRADAKİ: (1) K59-B önceden yazılı 3 devam; (2) K60 veri hazırlığı: SEC temel verisini 2010'a, "
    "fiyatı 2010'a uzat (SEC indirmesini ana model Cemal'in e-posta izniyle koşar); (3) K60 kütüphane (SINYAL_ENVANTERI, üç dönem); (4) Tiingo kararı Cemal'de.",
    "YOL HARİTASI (11 Kas): arastirma_cikti/yol_haritasi/YOL_HARITASI_11Kas.md. Sınıflama: şekil / parmak izi ve sıçrama kovalama YANLIŞ YOL (kapalı); "
    "dar profil / olay süzgeçleri DOĞRU FİKİR YANLIŞ CETVEL (n < 1.000 'İZ DEĞİL'ler aslında ÖLÇÜLEMEDİ); K58 DOĞRU YOL. Sıra: Y1 K59 (portföy cetveli v2 + 9 basit "
    "sinyal + 4'lü bileşik), Y2 batanlar dahil evren notu, Y3 tutarsa aylık aday listesi, Y4 tutmazsa 3 devam, Y5 Cemal kararları (standart, hedef +%4 / yıl, "
    "Tiingo anahtarı, yazılı boyut kuralı).",
    "KARAR (10 Kas, Cemal): K58 (Ç151) cetvelin kendisini sınadı. FI_OLCUT olay cetveli küçük etkiyi göremiyor (δ +%2'de n <= 300 güç en çok %11; "
    "dört hücre birden ~%0,2): 150 çalışmada 'iz yok' sonucunun büyük kısmı ölçüm aracının kabalığından. PORTFÖY CETVELİ (aylık, üst %10, maliyetli, "
    "NW t > 2, 3 alt dönem + son %30) ABD'de momentumu kabul etti, 200 plaseboda 0 yanlış alarm: KALİBRE ADAY STANDART. Benimsemek Cemal'in kararı "
    "(CLAUDE.md test standardı). Benimsenirse eski sinyaller bu cetvelle yeniden ölçülür (önce çok olaylı / sürekli olanlar). SMA200 filtresi (C4) "
    "SPY'de düşüşü yarıya indirdi ama getiri şartını geçmedi; hisse düzeyi SMA atılımı ABD'de eksi.",
    "YOL (9 Kas akşam): K57 (Ç148) bitti: YEOTK profili geçmiş testte İZ DEĞİL; ABD tam veriyle (SEC, Cemal'in e-posta izni) yeniden koşuldu, sonuç aynı. "
    "Eşiğe en yakın V1 (fiyat şartsız; ABD 2024-26 n 31). K57-B (Ç149): V1 geniş evren, 20 gün, F3'süz; üçü de İZ DEĞİL; geniş evrende ABD 2024-26 farkı +%10,3'ten +%4,8'e indi "
    "(V_ABD sonucu örneklem şansı); en yakın B3 ABD 2024-26 (alt uç -%0,1). K57-C (Ç150): C1-C3 İZ DEĞİL. HAT KAPANDI (ön kayıtlı kapanış ölçütü, K57C_ON_KAYIT BOŞLUK 7): 48 ABD karar hücresinin 0'ı tuttu; "
    "YEOTK profili için yeni varyant açılmaz. Profil yalnız aday bulmada (tarayıcı) kullanılır, alım sinyali değildir. Canlı izleme: BIST PNLSN, FORTE (3Ç26), ABD CENX, AEHR; 17 Kas sonrası "
    "ABD Q3 taraması yinelenir (küçük şirket 10-Q son günü 16 Kas); DGXX 13 Kas, QMLS 16-23 Kas, DGXX teslim 15 Ara.",
    "YOL (9 Kas, CEMAL'İN SON TALİMATI): YEOTK profili ('sıkı dosya') hisselerini BIST ve özellikle ABD'de bul; bütün ölçüleri her açıdan test et; "
    "gerekirse makine / web / ajan; basit ve erişilebilir bilgi esas. K57 = profilin ön kayıtlı geçmiş testi (bilanço günü tepkisi + temel ivme + "
    "seyrelme yok + fon lekesi yok + tepeden düşmüş; FI_OLCUT, karar ABD 2023 + 2024-26, BIST bilgi) + canlı tarama (BIST 3Ç26, ABD Q3 2026). "
    "Pozisyon kuralları IK_GOREV 6-7 Kas satırlarında (DGXX 2x = 4,02 / 4,05 $, bilanço 13 Kas, teslim 15 Ara; QMLS kalan yarı olay kuralları).",
    "YOL (1 Kas): K55 NİHAİ: İZ YOK (Ç146). BAĞIMSIZ 2024-26 bir kez açıldı (kilit + sızıntı PASS sonrası): seçimsiz kontrolle gerçek etki hücresi yok, "
    "K55 B 64 / 64 TUTMAZ; KEŞİF ve İÇ ile birlikte üç dönemde de K55 farkları olay tanımının seçim / ağırlık mekaniği (Ç143 ayrışma, Ç144 PBO / DSR "
    "aşırı uyum riski yüksek, Ç145 sızıntı yok). Yeni eşik aranmaz. AÇIK: EVREN2 (Ç142) 1-2 Kasım: Tiingo indirmesi, kimlik / adi hisse / fiyat kapsamı / "
    "son işlem / delist sınıfı doğrulaması, evren v2 etkisi ayrı rapor (K51-K55 değişmez, BAĞIMSIZ yeniden açılmaz).",
    "YOL (31 Eki): K56 Faz 1 (Ç140-Ç141): K55'in 125 KEŞİF satırında seçimsiz kontrolle gerçek etki 0 (KEŞİF 116, İÇ 112 MEKANİK); İÇ'te A farkı "
    "tekrarlıyor ama mekanik, K55 B 64 / 64 TUTMAZ; haber / birleşme açıklamıyor. Sonuç: K55'te mekanizması aranacak gerçek etki kalmadı. AÇIK: EVREN2 "
    "(Ç142) 1-2 Kasım Tiingo indirmesi + evren v2 etkisi; BAĞIMSIZ 2024-26 kilitli, açılması Cemal'in kararı (kalan gerçek etki olmadığından açmanın "
    "beklenen katkısı düşük).",
    "YOL (30 Eki): K51 İZ DEĞİL, K52 / K53 desteklenmedi, K54 evren denetimi sonuçları değiştirmedi, K55 Faz 1 İZ YOK (Ç138). K56 Faz 0 (Ç139): "
    "265 bulguluk etki envanteri; K51-K54'te mekanizması aranacak sağlam etki yok; K55'in ters yönlü KEŞİF'leri olay tanımının eseri ADAYI (sentetik "
    "sınama Y60 21 / 25; denetçi kontrolünde seçimsiz etiketle ~%90 küçülüyor); 4 K55 hücresi neden belirsiz. KARAR (Cemal): (a) K56 Faz 1 adım 1-3 "
    "(yerel, indirmesiz: seçimsiz kontrol, oynaklık / piyasa / tema denetimi, haber ve birleşme bileşimi) başlasın mı; (b) K55 İÇ / BAĞIMSIZ dönemleri "
    "açılsın mı (DOĞRULANMIŞ sınıf ve K51-K54 bulguları için gerekli); (c) büyük indirmeler (13F ~1,1 GB, MIDAS ~0,4 GB, FS 2016-20 ~1,6 GB) yalnız "
    "kalan gerçek etki varsa; (d) dur. Olası devam: ileri doğrulama (sinyal >= 01.09.2026, Mart 2027), Kasım Tiingo kotasıyla batan evren.",
    "VERİ (27 Eki): V_BIST (581) ve V_ABD (1411) yalnız bugün işlem gören hisseleri içeriyor (hayatta kalma yanlılığı). BIST'te "
    "borsadan çıkma seyrek; ABD'de küçük / zarar eden şirketlerde büyük. K34'te ABD nakit tükenmesi testi batanlar dahil yapıldı "
    "(SEC evreni + Tiingo, ücretsiz hesap, anahtar .env TIINGO_TOKEN; ayda 500 sembol, Ekim kotasının 450'si kullanıldı). Batanlardan "
    "örneğe girmeyen 374 şirket istenirse Kasım kotasıyla eklenebilir. Bundan sonraki ABD küçük şirket testleri batanlar dahil "
    "yapılmalı.",
    "DRIVE (26 Eki; GÜNCELLENDİ 15 Kas): IZ_DEFTERI.md Drive kopyası (MyDrive/COLAB_VERILER/col_tarayici) ve COL_OZET.md (col_tarayici) 15 Kas 2026 commit 6b5f58e sürümüne yüklendi (geri indirilip bayt bayt eşit, eski kopyalar çöpe; ikisi de güncelin atasıydı, kaybolan satır yok). FON_IZI.py Drive'da yok, yalnız repoda. Eski not: Drive kopyası K26 sürümünde (17:10); sonraki görev satırları "
    "(ders PDF kuralı, iki sayfanın silinmesi, yeni oturum notu, veri paketi, K27 içeriden alım, K28 bilanço sürprizi, K29 risk süzgeci, K30 ABD içeriden alım, K31 analist izleri, K32 sade portföy, K33 sıçrayan hisse, K34 batanlar dahil, K35 rüzgâr ve batma, K36 rüzgârın sebebi, K37 büyükler önce, K38 üç pazar + kural değişikliği, K39 ABD öncü, K40 saat farkı, K41 klasikler + kontrol, K42 bilinen etkiler, K43 alınabilir iz, K44 INTEM parmak izi, K45 kısa ufuk, K46 makine, K47 iki bölge, K46-B) eksik. COL_OZET.md Drive kopyası 24 Eki (f1ce2fd) sürümünde. CLAUDE.md "
    "yöntemiyle (eskiyi doğrula, yükle, geri indir, bayt eşitse eskiyi çöpe) güncellenecek.",
    "ÜRETİM (denetim 24 Eki, 'yaz' bekliyor): takip.py çıkışları yalnız son güne bakıyor (atlanan günlerde çıkış kaçıyor); bedelsiz/bölünmede "
    "pozisyon ve aday fiyatları ölçeklenmiyor (sahte −%48 satış); AL ekran satırı yanlış sütunlar; T10 boşluk dolumu ve taban önceliği; T9 ölü; "
    "_yarim_bar_at ad çakışması (XU100); listedeki fon hisselerine süzgeç yok; boş hedef_vurdu; trail aynı bar; pkl biçimi; test_takip log yan etkisi.",
    "T10 kararı yeniden (Cemal): düzeltilmiş COL_YOL'da T10 getiriyi artırmıyor (BIST +144 vs +155, ABD 0 vs +6), yalnız ağır kaybı azaltıyor.",
    "DENETIM.py / STOP_TEST.py düzeltildi (veri sonunda açık işlem) ama OB önbellekleri Drive'da; Colab'da yeniden koşulmalı.",
    "ABD SEC: Cemal 27 Eki'de e-posta iznini verdi; Form 4 (K30) yapıldı. 13F (fon pozisyonları) istenirse aynı yolla yapılabilir.",
    "Seviye 4 (sistem/çıkış/portföy: B15-T10, B5/B6/B8) tek cetvelle değil slot simülasyonuyla yeniden ölçülecek.",
    "ABD olay dosyası olmayan madde (A13 doji kutusu): BIST'te zaten tutmadığı için ABD taraması ertelendi (D13'ün ABD olayları "
    "denetimde bulundu ve puanlandı).",
    "Karar bekleyen standart sorusu (Cemal): yalnız BIST'te güçlü risk izleri (A11, A14: BIST 3 dönemde 1,5-2,6 kat, ABD 1,0-1,4) "
    "'BIST'e özgü risk süzgeci' diye ayrı sınıf olsun mu? Şu anki standartla iz değil.",
    "Puanlanamayan eski maddeler: A7 (veri yok), A8 (sözleşme tutarı yok), B10/B11 (kriz takvimi), B12/B13 ve D7 (çöl segment olay dosyası yok).",
    "D13 yakalama (Cemal'in vakaları, 25 Eki): üretim D13 Cemal'in koşan BINBN-24, KTLEV-24, MANAS-25a/b bölgelerini görmedi (dip yeni / parabol "
    "yok); K18 kutusu (bandı <= %50 en uzun pencere, dibe ilk değdiği günden) bunları gördü. Tespit kuralını değiştirmek üretim kararı ('yaz'); "
    "kazanç değil yalnız yakalama değişir (K18 profili iz değil).",
    "KÖR SET (K23, 26 Eki): ilk 20 işaret (7 ✓, 13 ✗) küçük grafikten verildi; Cemal: 'mumun yapısı görünmüyor, gerçek grafikte başka "
    "değerlendirirdim' -> bu sonuç geçersiz sayıldı. Önce net mum (v3), sonra Cemal'in isteğiyle v4: kutu + alış mumu "
    "(kutu tepesi üstünde kapanan ilk yeşil mum) + 1 yıl geri zum, yalnız alış mumu gelen 48 aday (FON_IZI_kor_set_v4.pdf). Cemal 28 ✓ / "
    "14 ✗ / 6 belirsiz: önce +%15 ✓ %54, ✗ %57, havuz %60; 2 kat ✓ %29 -> göz izi değil (FON_IZI_ders10c_kor_set_v4.pdf). Sıradaki "
    "denemeler (alış mumu boyu/hacmi, kutudan sonra gecikme) kapalı konu 'giriş onayı/hacim'e dokunuyor: yapılması Cemal'in kararı.",
    "BÜYÜK ALICI (K25, 25 Eki): raporlu fon payı çölle ilişkili değil. AKD (aracı kurum dağılımı) alınmadı (Cemal 26 Eki: 'gerek yok'; "
    "ücretsiz geçmiş kaynak yok, kurum düzeyi kişiyi göstermez). Bedava seçenek: KAP pay alım-satım / %5 eşik bildirimleri, çölden sonra "
    "daha sık mı (önceden yazılı, sırada).",
    "SİSTEM (K19, 25 Eki): giriş (çöl/kırılım) aynı gün eşli rastgele hisseden iyi değil; çıkış (kutu dibi stop + trail) 120 gün tutmaktan "
    "ortalamada düşük, yatay piyasada derin kaybı azaltıyor. Cemal'in kararı: amaç büyük kazananı tutmak mı (gevşek trail / tut), derin kaybı "
    "sınırlamak mı. Sıradaki ölçüm: üretim zinciri (D13 + T6/T10 + trail) ve 2016-22 ayı dönemi aynı rastgele kıyasla.",
]


def _ik_h(tarih, kayit, hata, tur, bulan, etki, duzeltme, ders, kaynak):
    """HATA DEFTERİ satırı (Cemal, 14 Kas 2026: 'bütün yanlış hesapların kaydını almalıyız, yoksa ilerleyemeyiz').
    tur: hesap / veri / ayrıştırma / geleceğe bakma / yanlış yorum / süreç / karar-boyut / ölçüt / iletişim.
    bulan: Cemal / denetim / test / alt ajan. etki: karara etkisi (değişti / değişmedi / karar yoktu)."""
    return {"tarih": tarih, "kayit": kayit, "hata": hata, "tur": tur, "bulan": bulan, "etki": etki,
            "duzeltme": duzeltme, "ders": ders, "kaynak": kaynak}


IK_HATA_TUR = ("hesap", "veri", "ayrıştırma", "geleceğe bakma", "yanlış yorum", "süreç", "karar-boyut", "ölçüt", "iletişim")
IK_HATA: List[Dict[str, str]] = [
    _ik_h('2026-09', 'H009: COL_OZET §4 ders 6', '`min_cekirdek` etkisi ölçülmeden parametre "kalibre" dendi; sonra etkisiz çıktı', 'süreç', 'denetim', 'tespit ayarı', 'parametre etkisi testi', 'Parametre etkisi ölçülmeden "kalibre" denmez', 'COL_OZET.md:13, 128'),
    _ik_h('2026-09', 'H011: COL_OZET §2', 'Drive API ile yeni kopya oluşturma çift dosya (-1/-2 kopyaları) sorunu yarattı', 'süreç', 'Cemal / denetim', '—', "Colab'dan yerinde yaz kuralı; CLAUDE.md Drive doğrulamalı güncelleme", "Drive'da tek kopya, bayt bayt doğrulama", 'COL_OZET.md:68, 218; CLAUDE.md Drive düzeni'),
    _ik_h('2026-09', 'H012: COL_OZET §4 ders 7; ONERI_DEFTERI', 'Gerçek kayıplar sinyalden değil boyut ve yapı riskinden geldi', 'karar-boyut', 'Cemal + denetim', 'gerçek para', 'boyut tavanı kuralları (CLAUDE.md gerçek para modülü)', 'Koruma = pozisyon boyutu, stop değil', 'COL_OZET.md:129; ONERI_DEFTERI.md Kapanan pozisyonlar'),
    _ik_h('2026-09', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', 'ders 5 (kayıt yok; standart koydu)', 'ölçüt', 'Cemal', 'karar yoktu', 'Sonuçtan geriye bakmak (40/40, en iyi / en kötü listesi) yanıltır', 'Sonuçtan geriye bakmak (40/40, en iyi / en kötü listesi) yanıltır', 'COL_OZET.md:127'),
    _ik_h('2026-09', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', 'önbellek olmadan aylarca yavaş test (ders 8)', 'süreç', 'Cemal', 'karar yoktu', 'Test altyapısı ilk gün kurulmalıydı (15 dk -> 30 sn)', 'Test altyapısı ilk gün kurulmalıydı (15 dk -> 30 sn)', 'COL_OZET.md:130'),
    _ik_h('2026-09-17', 'H013: COL_OZET §3, §5, §9.4', 'Fon yoğunlaşması "yapı riski" görüldü ama bayrak eklenmedi ("muhakeme kuralı"); TERA −88,6, DSTKF −90,1 ile kapandı', 'karar-boyut', 'Cemal / canlı takip', 'gerçek kayıp', 'D8 fon süzgeci (17 Eki) sonradan eklendi', 'Görülen yapı riski kurala çevrilir, ertelenmez', 'COL_OZET.md:111, 140, 262, 271'),
    _ik_h('2026-09-18', 'H001: COL_OZET §6 #1 (Ç08)', 'Dar hafta çarpanı özette vardı, kodda yoktu; tanım özetteki cümleden yeniden yazıldı, eski test betiği bulunamadı', 'süreç', 'denetim', 'boyut çarpanı etkilendi; doğrulanmadı', "`dar_hafta_olc()` eklendi, iki dönemde fark yoksa 1,0'a çekilecek", 'Özet ile kod birebir tutulur; test betiği arşivlenir', 'COL_OZET.md:154'),
    _ik_h('2026-09-18', 'H002: COL_OZET §6 #2', 'Negatif özkaynakta borç/öz eksi çıkıp 1,5x boyut alıyordu', 'hesap', 'denetim', 'boyut değişti', '`oz_negatif` sütunu, çarpan 0,7', 'İşaret durumları ayrı test edilir', 'COL_OZET.md:155'),
    _ik_h('2026-09-18', 'H003: COL_OZET §6 #3', 'Doji / fitil canlıda kırılım günü yeniden hesaplanıyordu (sinyal günü değil)', 'geleceğe bakma', 'denetim', 'boyut değişti', "sinyal günü ölçüleri aday CSV'ye yazılır", 'Boyut girdisi sinyal günü dondurulur', 'COL_OZET.md:156'),
    _ik_h('2026-09-18', 'H004: COL_OZET §6 #4', 'H=L / hacim=0 barlar doji sayılıyor, fitil 0 çıkıyordu', 'veri', 'denetim', 'boyut değişti', 'yalnız geçerli bar (H>L, V>0); `gecerli_oran` < 0,90 ise nötr + 0,5x', 'Kilitli / işlemsiz bar her ölçüde dışlanır', 'COL_OZET.md:157'),
    _ik_h('2026-09-18', 'H005: COL_OZET §6 #5', 'Giriş kırılım kapanışıyla sayılıyordu, gerçek dolum ertesi açılış', 'ölçüt', 'denetim', 'sonuçlar şişikti', "`islemler(OB, giris='acilis')`", 'Giriş = sinyalden sonraki ilk işlem fiyatı', 'COL_OZET.md:160'),
    _ik_h('2026-09-18', 'H006: COL_OZET §6 #6, §8', '2 haftalık örnekleme aynı kırılımı 4-5 kez sayıyordu; n 2400/540/2100 bağımsız işlem değildi; eski %74 / +14,8 ufuk 250 + tekilsiz + maliyetsizdi', 'hesap', 'denetim', 'sayılar değişti (%74/+14,8 -> %64/+8,9)', '(sembol, kırılım tarihi) tekilleştirme; temkinli cetvel', 'Aynı işlem bir kez sayılır; n daima tekil', 'COL_OZET.md:161, 197'),
    _ik_h('2026-09-18', 'H007: COL_OZET §6 #7', '`veri_yenile` auto_adjust=True ile ekliyordu, ana veri False ile inmişti; bölünme / temettüde eski seri düzeltilmiyordu', 'veri', 'denetim', 'ölçüm', 'auto_adjust=False + örtüşen barlarda %0,5 sapma kontrolü, sapan hisse baştan iner', 'Aynı seride iki düzeltme kipi karışmaz', 'COL_OZET.md:162'),
    _ik_h('2026-09-18', 'H008: COL_OZET §6 #8', 'Evren bugünün listesi (kottan çıkanlar yok): hayatta kalma yanlılığı', 'veri', 'denetim', 'düzeltilemedi; sonuçlar yukarı sapmalı okunur', 'not edildi (sonraki K34 / K54 / Tiingo işleri bunun için)', 'Yalnız yaşayanlarla küçük hisse testi iyimser çıkar', 'COL_OZET.md:163'),
    _ik_h('2026-09-18', 'H010: COL_OZET §3 -> §7 (Ç07)', '"12 elle işaretli çöl: kod 9 doğru, 0 kaçırma" sonucu 29 çöllük geniş sette tutmadı (13/26) [yanlış yorum (küçük örneklem)]', 'yanlış yorum', 'Cemal etiketi + denetim', 'tespit v3 gündeme geldi', 'KALIBRE v3; göz seti 29+8', 'Küçük örneklemden "segment sağlam" denmez', 'COL_OZET.md:104, 183'),
    _ik_h('2026-10', 'H021: CLAUDE.md Kod standardı', 'Colab `exec()` önbelleği kod değişince eski kodu çalıştırıyor', 'süreç', 'Cemal / test', 'sahte sonuçlar riski', '"çalışma zamanını yeniden başlat" hatırlatması', 'Kod değişti -> runtime restart', 'CLAUDE.md Kod standardı'),
    _ik_h('2026-10-04', 'H014: IZ_DEFTERI DERS 2', 'Aynı hissenin tekrar haberleri tek olay sayılmadı, ortalama şişti', 'hesap', 'denetim', 'A/B izleri yeniden ölçüldü', '"60 günde tek olay" kuralı; medyan yanına yazılır', 'Ortalama tek başına yazılmaz', 'IZ_DEFTERI.md:513, 518'),
    _ik_h('2026-10-04', 'H015: IZ_DEFTERI DERS 3', 'Kaba 10 sektör grubunda TTKOM kulüp ve gazetelerle aynı gruptaydı, "ölü" çıktı; 53\'lük İşY kodunda telekom +32 puan önde [veri (sınıflama)]', 'veri', 'denetim', 'sektör sonucu tersine döndü', "53'lük sektör kodu; kaba grup kullanılmaz", 'Sınıflama sonucu değiştirir', 'IZ_DEFTERI.md:514'),
    _ik_h('2026-10-04', 'H016: IZ_DEFTERI B13, DERS 4', 'B13 girişi "çölün son günü" = sonradan bilinen bilgi; ADAY etiketi gerçek zamanda tutmadı', 'geleceğe bakma', 'denetim', 'B13 düştü', 'gerçek zamanlı yeniden kurulmadan iz sayılmaz', 'Kırılımla hizalı her test sızıntı şüphelidir', 'IZ_DEFTERI.md:437, 515'),
    _ik_h('2026-10-04', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', 'tek dönem bulgular iz sayılmıştı', 'ölçüt', 'Cemal', 'karar yoktu', "DERS 1: 22-26'da tutmayan iz iz değildir", "DERS 1: 22-26'da tutmayan iz iz değildir", 'IZ_DEFTERI.md:512'),
    _ik_h('2026-10-08', 'H017: COL_OZET §9.5', 'Fiyat serisinde 69 bedelsiz onarılmamıştı (bölünme sıçramaları)', 'veri', 'test (bolunme_onar)', 'A/B sonuç değişmedi (+10,4 -> +10,6)', 'bolunme_onar.py; veri_koru.py günlük onarım', 'Bölünme onarımı yenileme zincirine bağlanır', 'COL_OZET.md:268-269'),
    _ik_h('2026-10-16', 'H139: COL_OZET §9.4, §9.8', '9 açık pozisyonda kayıtlı taban yoktu -> giriş x 0,85 yedek; DURDO yedek tabanı 4,43 [veri / süreç]', 'veri', 'canlı takip', 'çıkış kuralı yedekle çalıştı', 'yedek taban', "Takip CSV'si tabanı sinyal günü yazar", 'COL_OZET.md:263-264, 377'),
    _ik_h('2026-10-17', 'H140: COL_OZET §9.5, §9.8', "T6 (taban kırılınca çık) üretime yazıldı ama bölüm 3 testinde 'taban kırılınca çık' kötü çıkmıştı: üretim testle çelişiyor [karar]", 'karar-boyut', 'denetim', 'açık (tut ya da kaldır)', 'Cemal kararı bekliyor', 'Üretim kuralı test sonucuyla çelişmez', 'COL_OZET.md:273-274, 370'),
    _ik_h('2026-10-19', 'H018: CLAUDE.md Veri', 'Yahoo sektör etiketleri hatalı', 'veri', 'denetim', 'sektör testleri', 'sektor_BIST.csv BIST alt endekslerinden kuruldu', 'Dış etiket doğrulanmadan kullanılmaz', 'CLAUDE.md "Repodaki tek veri istisnası"'),
    _ik_h('2026-10-19', 'H019: CLAUDE.md GitHub Actions; COL_OZET §9.8', "gunluk_tarama.yml 19 Eki 21:01'de elle kapatılmış (disabled_manually), zamanlanmış tarama hiç çalışmadı", 'süreç', 'denetim', 'günlük tarama atlandı', 'gunluk_col_tarama.yml adıyla yeniden kuruldu', 'Tarama yoksa önce iş akışı durumuna bak', 'CLAUDE.md GitHub Actions; COL_OZET.md:375'),
    _ik_h('2026-10-19', 'H025: Ç38 (A13), IZ_KARNE ik_s_doji_kutu', "Doji kutusu ilk koşuda ileriye bakan 'kirilim' sütunuyla (kutu ufuk içinde kırıldı mı) seçilmişti", 'geleceğe bakma', 'denetim 24 Eki', 'A13 "GEÇERLİ risk" -> eşlide tutmadı', 'sütun seçimden çıkarıldı', 'Seçim sütunu bilgi tarihiyle denetlenir', 'IZ_KARNE.py:166, 2075'),
    _ik_h('2026-10-20', 'H020: CLAUDE.md İletişim', "Kod kutusuna dosya yolu yazıldı, Cemal Colab'a yapıştırdı: SyntaxError", 'iletişim', 'Cemal', 'zaman kaybı', 'kutu yalnız Colab komutu için; dosya adı düz metin', 'Kutudaki her şey yapıştırılıyor', 'CLAUDE.md İletişim (20 Ekim)'),
    _ik_h('2026-10-20', 'H022: COL_OZET §9.5 D10b', 'Rüzgâr hesabında tarih hizası yoktu: boşluklu hissede eski kod −%38, doğrusu +%25', 'hesap', 'denetim (inceleme)', 'üretim rüzgâr etiketi', 'RUZ_BAYAT=5, ortak takvim gününden başlangıç', 'Panel hesaplarında takvim hizası zorunlu', 'COL_OZET.md:277-278'),
    _ik_h('2026-10-20', 'H023: COL_OZET §9.5 D11/T9, §9.8', 'Verisi durmuş hisse aday oluyor ve listeden hiç çıkmıyordu [veri / süreç]', 'veri', 'denetim', 'üretim listesi', '`veri_bayat()`, VERI_BAYAT=5', 'Bayat veri kapısı', 'COL_OZET.md:279-282, 374'),
    _ik_h('2026-10-20', 'H024: COL_OZET §9.8', '`dar_hafta_olc` segmentten önceki haftayı da segmente sayıyor ("ilk" bloğu), `dar` düşük çıkıyor', 'hesap', 'inceleme', 'boyut çarpanı; DÜZELTİLMEDİ (açık)', 'doğrulama işiyle birlikte yapılacak', 'Bulunan hata açık listede kalır', 'COL_OZET.md:372-373'),
    _ik_h('2026-10-20', 'H027: Ç41 (D12 COL_DIP_TEST)', 'Hedefli işlem 120. barda kesilip verinin son barına atlıyordu; kazananlar "açık" diye atılıyordu', 'hesap', 'denetim', 'karar aynı (3/6)', 'düzeltilip yeniden koşuldu', 'Açık işlem sonu kuralı test edilir', 'IZ_KARNE.py:174'),
    _ik_h('2026-10-21', 'H028: Ç43 (COL_SEKIL)', '"Ayıran ölçüler" kıyaslanamaz negatiflerden: 21 \'bugün\' kutusu kodun kendi ret nedenine göre seçilmişti; doğru negatifle AUC 0,37-0,60 [ölçüt (kontrol grubu)]', 'ölçüt', 'denetim', 'iddia düştü (hiçbir şekil ölçüsü ayırmıyor)', '8 OLUMSUZ ile yeniden', 'Kontrol grubu sonuçtan / koddan bağımsız seçilir', 'IZ_KARNE.py:180; COL_OZET.md:334'),
    _ik_h('2026-10-21', 'H029: Ç44 (B14 COL_OBEK)', '"Alım oranı tabandan +15-20p" mekanikti (taban kutusu tavana ~2 kat uzak); işlemlerin yarısı kopyaydı [ölçüt / hesap]', 'ölçüt', 'denetim', 'B14 ADAY (yön) düştü', 'mesafe eşli taban; kopya atıldı', "Mesafe farkı varsa 'alım oranı' mekaniktir", 'IZ_KARNE.py:185; COL_OZET.md:337'),
    _ik_h('2026-10-21', 'H030: Ç45 (B15 COL_YOL / T10)', 'T10 dayanağı "+157 vs +144": kopya işlemler, hisse başına tek slot yok, trail ufuklu; düzeltilince ters (+144 vs +155; ABD 0 vs +6)', 'hesap', 'denetim', "T10 üretime yazılmıştı; dayanak düştü, yalnız ağır kayıp azalması kaldı; karar Cemal'de", 'COL_YOL v1.3 yeniden koşuldu', 'Üretime yazmadan önce slot simülasyonu denetlenir', 'IZ_KARNE.py:189, 1937; COL_OZET.md:295-296'),
    _ik_h('2026-10-21', 'H031: Ç47 (D13 COL_TESPIT), ik_s_d13', "ABD olayları dosyada '.US' ekliydi, adaptör okumuyordu; ABD hiç puanlanmamıştı [veri / hesap]", 'veri', 'denetim', 'ABD hücreleri eklendi (0,97 / 0,98)', 'adaptör düzeltildi', 'Dosya sütunu / pazar eşlemesi test edilir', 'IZ_KARNE.py:196, 2088'),
    _ik_h('2026-10-21', 'H032: Ç47, COL_OZET §9.5 D13', 'D13 "alım +12..26p, bozulma %2-9 vs %31-44" mekanikti (taban dibe / tavana uzaklığı farklı); mesafe eşli fark +0,5..+3,8p; 3456 varyantın hiçbiri seçim ölçütünü geçmiyor', 'ölçüt', 'denetim', "üretim D13'ün dayanağı düştü; kalması Cemal kararı", 'COL_TESPIT v1.1', 'Taban sinyalle aynı geometride olmalı', 'IZ_KARNE.py:196; COL_OZET.md:303'),
    _ik_h('2026-10-21', 'H033: COL_OZET §9.8 COL_GOZ', 'Kodun sistematik hatası: kutu 120 bar dibinden başlayıp ilk uygun günde sinyal; gerçek çölde düz bölge kutudan çok önce başlıyor, kod son parçayı işaretliyor [yanlış yorum (tespit)]', 'yanlış yorum', 'göz taraması (746 kutu)', '%6 gerçek çöl', 'üretim değişmedi', 'Kutu başlangıcı kuralı gözle doğrulanır', 'COL_OZET.md:348'),
    _ik_h('2026-10-21', 'H034: COL_OZET §9.8 COL_GOZ', 'Göz grafiklerinde sonraki 40 bar görünüyordu; Cemal\'in EVET/HAYIR etiketi "çöl mü" değil "atılım geldi mi" etiketi oldu [geleceğe bakma (etiket)]', 'geleceğe bakma', 'denetim (EVET alım %98, HAYIR %76)', 'tespit kuralı bu etiketten öğrenilemez', 'sinyal sonrası gizlenerek yeniden etiketleme (yapılmadı)', 'Etiket seti gelecek kesilerek verilir', 'COL_OZET.md:348-349'),
    _ik_h('2026-10-21', 'H035: COL_OZET §9.8 (OYLUM / EUYO)', 'Kod düşüş öncesi küçük mumlu rafı + düşüşü + yeni dibi tek kutu sayıyordu [yanlış yorum (tanım)]', 'yanlış yorum', 'Cemal', 'D13 kutusu yeni dipten başladı', 'col_dip2 kural 1', 'Önceki bölge dibi kırılınca biter', 'COL_OZET.md:332'),
    _ik_h('2026-10-21', 'H036: COL_OZET §9.8 COL_SEKIL', 'D12 "hacim kuruma" imzası ters: çölde hacim kurumuyor (hacim_kat60 0,91 vs 0,72)', 'yanlış yorum', 'denetim', 'D12 imzası şüpheli', "D13'te konum / hacim şartı kaldırıldı", 'Varsayılan imza veride sınanır', 'COL_OZET.md:334'),
    _ik_h('2026-10-21', 'H138: COL_OZET §9.8', 'CDS 3 Eyl verisi bayattı: pct250 0,22 -> çarpan 0,5x; 21 Eki güncellenince 250,1 bp, 0,84 -> 1,5x; boyut %3 -> %9 (4-18 Eyl boşluk) [veri (bayat dış veri)]', 'veri', 'denetim', 'üretim boyutu 3 kat değişti', 'CDS güncellendi', 'Dış veri yaşı kontrol edilir', 'COL_OZET.md:375'),
    _ik_h('2026-10-21', 'H141: COL_OZET §9.5 B5/T11', "21 Eki 12:43'te 'veri güncel, indirme atlandı' deyip bugünün yarım barını tuttu; XU100'e hiç uygulanmıyordu", 'hesap', 'Cemal isteği / denetim', 'gün içi sinyal kirli', 'seans açıkken yarım bar her zaman atılır (B5 / T11)', 'Yarım bar kapısı indirmeden bağımsız', 'COL_OZET.md:297-298'),
    _ik_h('2026-10-21', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', "ara mesaj atıp Cemal'den yeni mesaj beklendi", 'iletişim', 'Cemal', 'karar yoktu', 'Görev bitmeden tur bitmez; "çalışıyor, bitince yazarım" yok', 'Görev bitmeden tur bitmez; "çalışıyor, bitince yazarım" yok', 'CLAUDE.md İletişim (21 Ekim)'),
    _ik_h('2026-10-22', 'H037: COL_OZET §9.8 MUM_SUKUN v1.0', "BIST sinyallerinin %24'ü kilitli / işlemsiz günlerden (H=L, V=0)", 'veri', 'test', "v1.1'de yeniden", 'geçerli mum şartı', 'H004 ile aynı ders, tekrar etti', 'COL_OZET.md:350'),
    _ik_h('2026-10-23', 'H038: Ç63; IZ_DEFTERI C', "`fi_duzelt` BIST marjını 01.03.2020'den %10 sayıyordu (gerçek 13.03.2020): Mart 2020 çöküşünün 537 günü + 590 gerçek %10,5-19,5 hareket bölünme sanılıp siliniyordu", 'veri', 'bağımsız denetçi (ayrı model)', 'kararlar değişmedi; FON_IZI v1.0-1.2, SESSIZ_ML yeniden koşuldu', 'marj 13.03.2020; geçiş döneminde yalnız KAP bedelsiz yakınında bölünme', 'Kural tarihleri birincil kaynaktan', 'IZ_KARNE.py:233; IZ_DEFTERI.md:454; COL_OZET.md:357'),
    _ik_h('2026-10-23', 'H039: COL_OZET §9.8 FON_IZI v1.2/v1.4; DERS 5', 'A14 / A15 ham katta 1,3-2,9 ama eşli taban yoktu; eşliyle (bloksuz taban günü, zaten sıçramış hisse) 0,9-1,2 [ölçüt (kontrol grubu)]', 'ölçüt', 'bağımsız denetim', 'A14, A15 ÇÜRÜDÜ', 'aşağı sinyallere eşli taban eklendi', 'Kıyas tabanı sinyalin bağlamını taşır', 'COL_OZET.md:356-357; IZ_DEFTERI DERS 5'),
    _ik_h('2026-10-23', 'H040: COL_OZET §9.8 (3)', "SESSIZ_ML işlem seçimi havuz eşiğiyle BIST'te %58-74 seçiyordu", 'hesap', 'denetim', 'model sonucu', 'pazar bazında eşik', 'Eşik pazar başına', 'COL_OZET.md:357'),
    _ik_h('2026-10-24', 'H026: Ç38', "Aynı kutu kayınca yeniden A sayılıyordu; A_dip'in kontrolü (dojisiz dip kutusu) yoktu; etki dipte olmaktan, dojiden değil (kat 0,90-0,97) [hesap / ölçüt]", 'ölçüt', 'denetim', 'A13 düştü', 'B_dip kontrolü eklendi', 'Etki, aynı bağlamdaki şekilsiz eşle kıyaslanır', 'IZ_KARNE.py:166'),
    _ik_h('2026-10-24', 'H041: IZ_DEFTERI indeks; Ç70-Ç72; COL_OZET §9.8 IZ_KARNE', 'Eski cetvelde "GEÇERLİ" A1-A4, A9, A13, B1: fark hissenin zaten düşmüş / yükselmiş / sakin olmasındandı; eşli tabanda tutmadı', 'ölçüt', 'tek cetvel yeniden ölçüm', 'İZ 0, ADAY 0', 'eşli taban (ay x momentum x likidite)', 'Piyasa medyanı kıyası yetmez', 'IZ_DEFTERI.md:23; COL_OZET.md:360'),
    _ik_h('2026-10-24', 'H042: Ç01', '`mfe_analiz` "stopsuz" satırı stoplardan farklı örneklemdendi: stop maliyeti ~2 kat abartılı (+19,3 -> +10,2)', 'hesap', 'denetim', 'yön aynı', 'aynı örneklemde yeniden', 'Kıyaslanan satırlar aynı örneklemden', 'IZ_KARNE.py:92'),
    _ik_h('2026-10-24', 'H043: IZ_KARNE ik_taban', 'Taban önbellek anahtarı yalnız dosya boyu / tarihiydi; `fi_duzelt` / hücre kodu / KAP bedelsiz kaydı değişince eski taban kullanılıyordu [süreç / hesap]', 'hesap', 'denetim', 'eski taban riski', 'kod + düzeltilmiş veri parmak izi anahtara eklendi', 'Önbellek anahtarı koda bağlı', 'IZ_KARNE.py:1995-2000 (ik_taban yorum)'),
    _ik_h('2026-10-24', 'H044: IZ_KARNE _ik_panel', "İnce gün (bayram arifesi 9 Nis 2024: 541'in 215'i) shift / rolling zincirini öteki hisselerde ~20 gün NaN yapıyordu", 'veri', 'denetim', 'sinyal sayıları', 'hisselerin yarısından azının barı olan gün tablodan çıkarılır', 'Takvim kalitesi panelden önce', 'IZ_KARNE.py:2019'),
    _ik_h('2026-10-24', 'H045: Ç84; IK_ACIK ÜRETİM', 'Geriye dönük denetim: ölçüm kodunda ~30 doğrulanmış hata; ÜRETİMDE 11: takip.py çıkışı yalnız son güne bakıyor (atlanan günlerde çıkış kaçıyor), bedelsiz / bölünmede pozisyon fiyatı ölçeklenmiyor (sahte −%48 satış), AL satırı yanlış sütunlar, T10 boşluk dolumu / taban önceliği, T9 ölü, `_yarim_bar_at` ad çakışması (XU100), fon süzgeci yok, boş hedef_vurdu, trail aynı bar, pkl biçimi, test log yan etkisi [hesap / veri / süreç]', 'veri', '6 bağımsız denetçi', "tek cetvel İZ 0 değişmedi; üretim düzeltmeleri 'yaz' BEKLİYOR (açık)", 'ölçüm kodu düzeltildi; üretim bekliyor', 'Üretim kodu da ölçüm kodu gibi denetlenir', 'IZ_KARNE.py:294, 1115-1121, 1934'),
    _ik_h('2026-10-24', 'H046: IK_ACIK', "DENETIM.py / STOP_TEST.py veri sonunda açık işlem hatası düzeltildi ama OB önbellekleri Drive'da; Colab'da yeniden koşulmadı [hesap / süreç]", 'hesap', 'denetim', 'COL_OZET §1 sayıları eski', 'açık', 'Düzeltme, ilgili sonuçlar yeniden koşulunca biter', 'IZ_KARNE.py:1938'),
    _ik_h('2026-10-24', 'H047: Ç76-Ç77 (K16)', 'Eşli kutu geleceğe göre seçiliyordu; "çok test edilen dip daha sık kırılıyor" gözlemi (1,00-1,93) düştü (0,75-1,31)', 'geleceğe bakma', 'denetim', 'gözlem geri alındı', 'fi_duzelt + eşli kutu geçmiş bilgiyle', 'Kontrol grubu da bilgi tarihine uyar', 'IZ_KARNE.py:265-270'),
    _ik_h('2026-10-24', 'H048: IK_GOREV 24 Eki (düzgün dip); DERS 8', 'Ortalama getiri tek vakadan (TEHOL +%797) şişiyordu; hariç +%4, medyan %0 [hesap (tek vaka)]', 'hesap', 'denetim', 'yorum değişti', 'medyan yanına yazıldı', 'Ortalama tek vakayla yalan söyler', 'IZ_KARNE.py:1098-1105; IZ_DEFTERI DERS 8'),
    _ik_h('2026-10-24', 'H049: Ç67 / K13; IZ_DEFTERI C', '"Kod TEHOL bölgesinin aynısını daha önce gördü" sözü fazlaydı: D13\'ün eski kutuları bu bölgeye benzemiyordu [iletişim / yanlış yorum]', 'yanlış yorum', 'Cemal ("ben niye göremiyorum")', '—', 'ölçüyle arama (K13), tek eş 2021', 'İddia ölçüsüz söylenmez', 'IZ_DEFTERI.md:466; IZ_KARNE.py:241'),
    _ik_h('2026-10-24', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', "görevin bittiği Cemal'e belli olmuyordu", 'iletişim', 'Cemal', 'karar yoktu', 'GÖREV TAMAMLANDI satırı; son mesaj madde madde; görev günlüğü', 'GÖREV TAMAMLANDI satırı; son mesaj madde madde; görev günlüğü', 'CLAUDE.md İletişim (24 Ekim)'),
    _ik_h('2026-10-24', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', "eşiğin sonuca göre oynanması riski (K56 denetimi H079'da 'hipotez kaydı sonuçtan sonra' olarak bir kez gerçekleşti)", 'süreç', 'Cemal', 'karar yoktu', 'İz yok çıkarsa durma: denenen, yaklaşan, sıradaki 3 deneme önceden yazılır; eşik sonuca göre oynanmaz', 'İz yok çıkarsa durma: denenen, yaklaşan, sıradaki 3 deneme önceden yazılır; eşik sonuca göre oynanmaz', 'CLAUDE.md Test standardı'),
    _ik_h('2026-10-25', 'H050: Ç91 (K19); COL_OZET §9.8', '"Kazandıran kırılım + kutu dibi stop + trail" cümlesi hiç rastgeleye göre ölçülmemişti; fark ~0; COL_OZET §1 "doğrulanmış sonuçlar" mutlak getiri = piyasanın sayısı', 'ölçüt', 'Cemal ("bir aptallık var")', 'sistemin kazanç dayanağı düştü', 'K19 rastgele kıyası', 'Bir kuralın değeri rastgele girişe göre farkıdır (DERS 11)', 'IZ_KARNE.py:323; COL_OZET.md:365'),
    _ik_h('2026-10-25', 'H051: Ç94 (K22); DERS 13', "Cemal'in penceresinde çöl önde (0,57-0,66) ama fark yalnız atılım mumunda = sonradan bilinen; bekleyen emirle alınca sahte kırılımlarla siliniyor", 'geleceğe bakma', 'ölçüm', 'iz değil', 'kapanıştan sonrası ayrı ölçüldü', "'Koşmaya başlayan' sonradan bilinir", 'IZ_KARNE.py (Ç94 notu); IZ_DEFTERI DERS 13'),
    _ik_h('2026-10-25', 'H052: Ç85 (K18); DERS 12', "Hatırlanan vakalar koşanlardı (hafıza yanlılığı); koşmayan VSNMD / PAPIL'de de aynı profil", 'yanlış yorum', 'ölçüm', 'profil iz değil', 'koşmayanlar da sete alındı', 'Hatırlanan örnekler koşanlardır', 'IZ_KARNE.py:301; IZ_DEFTERI DERS 12'),
    _ik_h('2026-10-25', 'H053: IK_ACIK D13 yakalama; Ç85', "Üretim D13 Cemal'in koşan BINBN-24, KTLEV-24, MANAS-25a/b bölgelerini görmedi (12 bölgenin 5'i) [yanlış yorum (tespit kapsamı)]", 'yanlış yorum', 'Cemal vakaları', "üretim değişmedi; 'yaz' kararı açık", 'K18 kutusu tanımı aday', "Tespit motoru Cemal'in vakalarına göre denetlenir", 'IZ_KARNE.py:1946, 301'),
    _ik_h('2026-10-26', 'H054: Ç95; IK_GOREV 26 Eki; IK_ACIK KÖR SET', 'Kör set v2 küçük grafik (sayfada 6 kutu, Bollinger, 40 mum): Cemal mum yapısını göremedi; ilk 20 işaret geçersiz sayıldı [iletişim / süreç]', 'iletişim', 'Cemal', 'ön sonuç geçersiz', 'v3 net mum, v4 kutu + alış mumu + 1 yıl zum', 'Gösterim yanlışsa işaret yanlıştır', 'IZ_KARNE.py:1189, 1949'),
    _ik_h('2026-10-26', 'H055: CLAUDE.md YENİ ÖLÇÜT; IK_GOREV 26 Eki', 'Eski ölçütteki "medyan fark" ve "eşli ortalama portföyü" tek hisse çarpıklığı yüzünden yanlıştı', 'ölçüt', 'rastgele olay sağlaması', 'ölçüt değişti (FI_OLCUT)', 'eşli fark + ay kümeli aralık + sıra + 200 eşli rastgele portföy', 'Her cetvel plaseboyla sınanır', 'CLAUDE.md "YENİ ÖLÇÜT (26 Ekim)"; IZ_KARNE.py:1163'),
    _ik_h('2026-10-26', 'H143: IK_ACIK DRIVE (26 Eki)', 'IZ_DEFTERI.md Drive kopyası K26 sürümünde kaldı; K27-K47 görev satırları eksik; COL_OZET Drive kopyası 24 Eki', 'süreç', 'denetim', 'Colab oturumunda eski defter riski', 'açık (CLAUDE.md yöntemiyle güncellenecek)', 'Drive eşitlemesi görev bitişinin parçası', 'IZ_KARNE.py:1931'),
    _ik_h('2026-10-26', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', 'iz çıkmayan her çalışmaya PDF gönderildi, Cemal rahatsız oldu', 'iletişim', 'Cemal', 'karar yoktu', "PDF yalnız gerçek izde; 'yapıtlar' kartı yalnız istenince", "PDF yalnız gerçek izde; 'yapıtlar' kartı yalnız istenince", 'CLAUDE.md İletişim (26 Ekim); IK_GOREV 26 Eki'),
    _ik_h('2026-10-26', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', "yeni konuşma sohbeti hatırlamıyor, Cemal'e geçmiş soruldu", 'süreç', 'Cemal', 'karar yoktu', 'Yeni oturum defterden sürer', 'Yeni oturum defterden sürer', 'CLAUDE.md İletişim (26 Ekim)'),
    _ik_h('2026-10-27', 'H056: Ç103 (K31)', "SEC finansal tablo veri setinde pay sayısı 'dei' kalemi yok; ilk kod yanlış kalem okuyordu (sonuç görülmeden düzeltildi)", 'veri', 'test', 'yok', 'bilanço kaleminden', 'Veri alanı varlığı önce doğrulanır', 'IZ_KARNE.py:436'),
    _ik_h('2026-10-27', 'H057: Ç106 (K33-B); DERS 23-24', "ABD-ADAY ilan edilecekti ama evren yalnız bugün işlem görenler; nakit tükenenlerin %26-52'si bildirimi kesmiş, bizde %0 [veri (hayatta kalma)]", 'veri', 'denetim', 'ABD-ADAY GEÇERSİZ', 'K34 batanlar dahil (Tiingo)', "Batanları görmeyen veri 'küçük şirket sıçrar' der", 'IZ_KARNE.py:468'),
    _ik_h('2026-10-27', 'H058: Ç107 (K34)', 'Kırpılmamış ortalamada ters bölünme veri hatası +%4.800', 'veri', 'ölçüm', 'önceden yazılı +%500 kırpma sınırladı', 'kırpma', 'Uç değer kırpması önceden yazılır', 'IZ_KARNE.py:480'),
    _ik_h('2026-10-27', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', 'kriz dönemi çölleri teste girme riski; denetlendi, etkilenmemiş çıktı', 'veri', 'Cemal', 'karar yoktu', 'Fon krizi istisnası (31.08.2026 kesik)', 'Fon krizi istisnası (31.08.2026 kesik)', 'CLAUDE.md Test standardı; IZ_KARNE.py:1251'),
    _ik_h('2026-10-28', 'H059: IK_GOREV 28 Eki (K36)', 'Sebep sinyali kuralında aralık hatası; test 47 ile sonuç görülmeden düzeltildi', 'hesap', 'test', 'yok', 'düzeltildi', 'Mekanik test her kuralda', 'IZ_KARNE.py:1364-1368'),
    _ik_h('2026-10-28', 'H060: Ç112 (K38)', 'Avrupa verisinde Londra peni / sterlin 100x geçişleri (5 hisse) ve DIA.MC; ilk koşudaki −%18 / +%42 bu hatadandı', 'veri', 'denetim', 'ilk koşu sayıları geçersiz', 'temizlendi, DIA.MC dışarıda', 'Yeni pazar verisi birim denetiminden geçer', 'IZ_KARNE.py:539'),
    _ik_h('2026-10-28', 'H061: Ç120', 'Hat kontrol betiğinde hata: tarih sırasına göre ilk 1.500 olay alınmış, test hücrelerine yalnız rastgele düşmüştü (yarı pozitif kontrol yanlış çıkıyordu)', 'hesap', 'denetim', 'kontrol sonucu değişti (tutuyor)', 'düzeltildi', 'Kontrol betiği de denetlenir', 'IZ_KARNE.py:617'),
    _ik_h('2026-10-28', 'H062: Ç120 (bağımsız kod denetimi)', '4 orta / küçük: r60 çıkış günü NaN olan olay düşüyordu (Avrupa tatil / askı); K39 küçükler alt kümesi hafta sonu boş; K40 saatlik bar etiketi (Yahoo bar başlangıcı) + aynı güne düşen iki sinyal çift sayım; sterline inen Londra hisselerinde Kur birimi [hesap / veri]', 'veri', 'bağımsız denetçi', 'hiçbir karar değişmedi', 'hepsi düzeltilip yeniden koşuldu', 'Takvim / birim / etiket hataları sayılır', 'IZ_KARNE.py:617-632'),
    _ik_h('2026-10-28', 'H063: Ç120 notu sonu', 'K28 "iyi bilanço" etiketi çeyrek içi dağılımla (etiket sızıntısı); DÜZELTİLMEDİ (K41-C zaten iz değil)', 'geleceğe bakma', 'bağımsız denetçi', 'yön belirsiz, karar aynı', 'not edildi', 'Çeyrek içi dilim sızıntıdır', 'IZ_KARNE.py:632'),
    _ik_h('2026-10-28', 'H064: Ç121 (K42), DERS 32-33', 'Ham cetvelin tabanı pazar MEDYANI idi; r60 sağa çarpık -> rastgele hisse bile \'medyanı geçer\'; "BIST momentum +%7-10" mesaj ve DERS 32 ifadesi geçersiz [hesap / ölçüt]', 'ölçüt', "K43'te kaçınma sinyalleri bile +%3-13 çıkınca", 'ifade geri alındı; momentum ABD zayıf, BIST yok', 'taban eşit ağırlıklı ORTALAMA, yeniden koşuldu', 'Sağa çarpık getiride medyan taban yanıltır', 'IZ_KARNE.py:632-652; IZ_KARNE.py:1377'),
    _ik_h('2026-10-28', 'H065: Ç124 (K45)', "İlk koşu düz rastgele tabanla +20 puan gösterdi ama −%8'e ulaşma da +8 puan yüksekti (oynak bölgeler) [ölçüt (kontrol)]", 'ölçüt', 'denetim', "'KISA İZ' zayıf, 2016-22 ağırlıklı", 'oynaklık eşli rastgele taban', 'İki yönlü hız oynaklıktır', 'IZ_KARNE.py:683'),
    _ik_h('2026-10-28', 'H066: Ç128 (K48)', 'Örnek Pine kodundaki `gap = ta.pvt` hatalıydı (PVT hacim göstergesi)', 'hesap', 'kod okuma', 'düzeltilerek kullanıldı', 'düzeltildi', 'Dış kod kopyalanmadan okunur', 'IZ_KARNE.py:758'),
    _ik_h('2026-10-28', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', 'eşik gevşetme (K49) de tutmadı', 'süreç', 'Cemal', 'karar yoktu', "DERS 38: 'iz değil' kararlarını eşiğin sertliği değil ölçüler veriyor", "DERS 38: 'iz değil' kararlarını eşiğin sertliği değil ölçüler veriyor", 'IZ_DEFTERI DERS 38'),
    _ik_h('2026-10-29', 'H067: Ç132 (K51) sonuç denetçisi', "Küçük artı etkinin tamamı bugün işlem görenlerden (+5,3 / +6,4); batanlarda eksi; 'rüzgâr yok' kırılımı ve FI_OLCUT paneli aynı yanlılıkta [veri (hayatta kalma)]", 'veri', 'sonuç denetçisi', "İZ DEĞİL korundu; 'en yakın aday' yorumu düştü", 'kırılganlık bölümüne yazıldı', 'Yaşayan evrenle küçük hisse testi iyimser', 'IZ_KARNE.py:792'),
    _ik_h('2026-10-29', 'H068: Ç133 (K51-D1)', '"Süren kırılım" grubunun iyi görünmesi tamamen sonradan bilinen bilgiydi (10 gün kutu üstünde kalma)', 'geleceğe bakma', 'ölçüm (11. gün giriş)', 'iz değil', '11. gün giriş testi', 'Gruplama geleceği içermez', 'IZ_KARNE.py (Ç133 notu)'),
    _ik_h('2026-10-29', 'H069: Ç134 (K51 v1.2)', "Tiingo 'batan' 422 sembolün yalnız 51'i batma benzeri; 171 satın alma; 153 kod yeniden kullanımı şüphesi", 'veri', 'denetim', 'duyarlılık senaryoları sonucu değiştirmedi', 'K54 sınıflaması', "'Batan' etiketi SEC geçmişiyle doğrulanır", 'IZ_KARNE.py:817'),
    _ik_h('2026-10-29', 'H070: Ç135 (K52)', "G1 (teyit alan iz) ile G2a dengesiz: G1'in son 60 gün getirisi +8 vs +0,6; teyit zaten yükselmiş hisselerde [ölçüt (denge)]", 'ölçüt', 'denetim', 'H0 desteklenmiyor', 'dengesizlik rapora yazıldı', 'Grup dengesi karardan önce', 'IZ_KARNE.py:835'),
    _ik_h('2026-10-29', 'H071: Ç136 (K53)', "ADE / KGS tanımları Cemal'in mesajı kesik geldiği için Claude tarafından sabitlendi; Cemal'in 6 maddelik geçerlilik listesi sonuç görüldükten sonra eklendi", 'süreç', 'Cemal', 'karar değişmedi', 'ön kayıt EK olarak yazıldı', 'Kesik talimat sorulur, tahmin edilmez', 'IZ_KARNE.py (Ç136 notu)'),
    _ik_h('2026-10-30', 'H072: Ç137 (K54 ek 8); IZ_DEFTERI indeks', "K54 ilk metodoloji: SEC sembolü tek başına kanıt sayılıyordu; son kapanış otomatik nakit bedel; K51 evreninde 6 emtia / döviz ETF'si (DBA, DBB, DBO, UNG, UNL, UUP) + BTCW [veri / süreç]", 'veri', "Cemal'in zorunlu düzeltmeleri + K54 ek 8", 'etki <= 0,1 puan, karar aynı', 'evren_disi_ABD.csv, cy_evren_filtre', 'Evren temizliği ilk adımdır', 'IZ_KARNE.py:877, 1511; IZ_DEFTERI.md:93'),
    _ik_h('2026-10-30', 'H073: Ç137', "K48 / K49 / K50 yalnız hayatta kalan V_ABD'de koşmuş; kod K34 evrenini almıyor -> GEÇERSİZ etiketi", 'veri', 'K54 denetimi', 'BB / EMA deneyleri geçersiz', 'not', 'Makine deneyleri de evren denetiminden geçer', 'IZ_KARNE.py:877'),
    _ik_h('2026-10-30', 'H074: IK_GOREV K55 ortak ayarlar (9 madde)', "K55 v1.1'de purge ufuktan kısa, embargo yok, koşu kimliği zayıf (kilit sha boşsa durmuyor), dönem etiketi gün sonu / saat dilimi / NaT belirsiz, kısa seri siliniyordu [süreç / ölçüt]", 'ölçüt', "Cemal'in denetimi", 'Faz 0 yeniden koşuldu, sonuç değişmedi', 'ONKAYIT v1.2', 'Sızıntı önlemleri (purge = ufuk) baştan', 'IZ_KARNE.py:1560; IZ_DEFTERI.md:97'),
    _ik_h('2026-10-30', 'H075: IK_GOREV K55 evren modülü (11 madde)', "Eksik `cikis_islemi` 'y' sayılıyordu; 4a halef kesin sayılıyordu; 4b yanlış şirket fiyatları kesilmiyordu; örneklem tekrarlı [veri / hesap]", 'veri', "Cemal'in denetimi", 'evren v1.3', 'k54_tutarlilik, kesim_uygula', "Boş alan 'evet' değildir", 'IZ_KARNE.py:1576; IZ_DEFTERI.md:98'),
    _ik_h('2026-10-30', 'H076: IK_GOREV K55 veri kalitesi; commit e726670', "NYSE takviminde 2022-01-03 takvim dışı sayıldı (yılbaşı cumartesi kuralı); 'sıçrama' bayrağı haber günlerini (ABEO, AGEN, ALNY) hata sayıyordu [hesap / veri]", 'veri', 'test + inceleme', 'kalite raporu', 'kural + test eklendi; sıçrama eksiksizlikten çıkarıldı', 'Takvim istisnaları test edilir', 'IZ_KARNE.py:1591-1605; git e726670'),
    _ik_h('2026-10-30', 'H077: commit aed0ee4', "K55 kısa seri listesi `attrs` içinde DataFrame olarak pandas'ı bozuyordu", 'hesap', 'test', 'yok', 'dönüş değerine taşındı', "attrs'a DataFrame konmaz", 'git aed0ee4'),
    _ik_h('2026-10-30', 'H078: Ç138-Ç140 (K55 Faz 1, K56)', "25 KEŞİF'in 19-20'si ters yönlü: olay başlangıcı seçim etkisi (t0 = +%30'u ilk yakalayan gün); bilgisiz yapay veri aynı farkı üretiyor; seçimsiz kontrolle d −0,25..−0,43 -> −0,016..−0,049 [ölçüt (olay tanımı eseri)]", 'ölçüt', 'K56 sentetik + seçimsiz kontrol', "KEŞİF'ler MEKANİK; K55 İZ YOK", 'A1 seçimsiz kontrol protokolü', 'Olay tanımı ağırlık mekaniği üretir (Ç143)', 'IZ_KARNE.py:905, 931, 953, 986'),
    _ik_h('2026-10-30', 'H079: K56_FAZ0_RAPOR denetim (45 bulgu)', "KRİTİK: 'İLİŞKİ VAR, NEDEN BELİRSİZ' ön sınıfı kaynakta başarısız 61 bulguya verildi (aşırı iddia); hipotez kaydı sonuçlar görüldükten sonra kilitsiz yazıldı; talimat süzgecinde Ç100/102/103/107 'hepsi sıfır' diye yanlış özetlendi; ters KEŞİF 19 değil 20; 'en iyi 20 hisse çıkarıldı' satırları ilişki sayılmış; TLGTQ yanlış etiket; 10b5-1 payı çelişkili [yanlış yorum / süreç]", 'yanlış yorum', '4 bağımsız denetçi', '42 düzeltildi, 3 kısmen', 'mekanik ön sınıf kuralı, v1.1 kilit', 'Ön sınıf kaynak kararından mekanik türetilir', 'arastirma_cikti/k56_mekanizma/K56_FAZ0_RAPOR.md:748-800'),
    _ik_h('2026-10-30', 'H088: IK_GOREV K55 Faz 1', "Drive bağlayıcısı büyük dosyada güvenilmez; OUTPUT yüklemesi Colab'dan", 'süreç', 'koşu', '—', 'Colab komutu', 'Büyük dosya Drive API ile gitmez', 'IZ_KARNE.py:1605-1615'),
    _ik_h('2026-10-31', 'H080: Ç140; commit d1922e5', 'K56 Faz 1 ilk koşu (6cf01ae) dönem sızıntısı (G7 eş elemesi, (iii) dizisi) -> geçersiz, saklandı', 'geleceğe bakma', 'denetim', 'yeniden koşuldu, sonuç aynı yönde', 'v1.2-b', 'İlk koşu geçersizse saklanır, silinmez', 'IZ_KARNE.py:953; git d1922e5'),
    _ik_h('2026-10-31', 'H081: Ç142; commit fad54be', "EVREN2 Ö2 ilk tanımı (25-NSE sembolü) 3 aday verdi: EFTS sembolü SEC'in GÜNCEL tablosundan, batanlarda yok", 'veri', 'sapma kaydı (fiyat görülmeden)', 'aday listesi değişti (278)', 'Tiingo bitiş listesinden', 'Güncel tablo batanı göstermez', 'IZ_KARNE.py:977; git fad54be'),
    _ik_h('2026-10-31', 'H082: commits 4949f38, 0b6d1db, 8cee92a', "K56: K34 özetinde CIK metin -> sayı; boş Tiingo satırında datetime toplama hatası; AYR koşu özeti JSON'da tuple anahtar", 'hesap', 'test', 'yok', 'düzeltildi', 'Tip hataları test eder', 'git 4949f38, 0b6d1db, 8cee92a'),
    _ik_h('2026-10-31', 'H083: Ç143', 'K56-AYR ilk koşu (3b61627) geçersiz; sonraki koşular birebir', 'hesap', 'test', 'yok', 'yeniden koşuldu', '—', 'IZ_KARNE.py:986'),
    _ik_h('2026-10-31', 'H084: Ç144', 'PBO / DSR alt örneklem bilgi sütunu ilk koşuda yanlış yöntemle hesaplandı (karar vermiyordu)', 'hesap', 'inceleme (v1.3-b)', 'yok', 'düzeltildi', 'Bilgi sütunu da doğru olmalı', 'IZ_KARNE.py:999'),
    _ik_h('2026-10-31', 'H085: K56_NIHAI_RAPOR Sapmalar; Ç145', 'İlk iki tam sızıntı denemesi test hatasıyla geçersiz (ayrışma tohum etiketi; yapay karar sütunları)', 'hesap', 'test', 'yok (NOT.md ile saklandı)', 'tek etiket sabiti, 1e-12 tolerans', '—', 'arastirma_cikti/k56_mekanizma/K56_NIHAI_RAPOR.md:59-62'),
    _ik_h('2026-10-31', 'H086: commit 5d41245', 'K56-F1A raporunda açıklayıcı tanı cümlesi sayılara uymuyordu', 'iletişim', 'inceleme', 'yok', 'cümle sayılara göre düzeltildi', 'Rapor cümlesi sayıdan türetilir', 'git 5d41245'),
    _ik_h('2026-10-31', 'H087: K56_NIHAI_RAPOR; commit a6cbe6a', "Ortamın git vekili etiket push'unu 403 ile reddetti; kilit çapası etikete dayanıyordu", 'süreç', 'koşu', 'kod değişti, AYR / PBO / sızıntı yeniden (birebir)', 'çapa çalışma dalına taşındı', 'Altyapı varsayımı test edilir', 'K56_NIHAI_RAPOR.md:62; git a6cbe6a'),
    _ik_h('2026-11-04', 'H089: IK_GOREV 4 Kas (ABD 10x denetimi)', "Önceki rakamlar yanlıştı: QMLS IPO değil doğrudan listeleme, 10-Q'da going-concern, 523 M$ sözleşme yalnız PR; AIB sahası Spartanburg SC, Nebius exhibit yok; VIVO capex 411 M$, kiracı yok; DGXX hisse 102,06 M / FD 111,54 M [yanlış yorum (dosya)]", 'yanlış yorum', 'bağımsız denetim (EDGAR)', "sıralama DGXX > AIB > QMLS > VIVO; QMLS varsayılan 'sat'", 'rapor düzeltildi', 'Birincil kaynak (SEC) olmadan dosya yazılmaz', 'IZ_KARNE.py IK_GOREV 2026-11-04 (ABD mikro-cap)'),
    _ik_h('2026-11-06', 'H090: DENETIM_10Kas #7; IK_GOREV 6 Kas', 'YEOTK 3Ç ana ortaklık kârı ≈864 mn TL yazıldı (9A 1.534 − 6A 670); enflasyon düzeltmeli 6A 707 ile doğrusu ≈827', 'hesap', 'ana model denetimi', "sonuç ('3Ç kârı ilk yarıdan büyük') değişmedi", 'düzeltme notu', 'TMS 29 verisinde çeyrek farkı düzeltilmiş tabanla alınır', 'arastirma_cikti/k57_yeotk_profili/DENETIM_10Kas.md #7; IZ_KARNE.py:1671'),
    _ik_h('2026-11-06', 'H091: IK_GOREV 6 Kas (QMLS beta)', 'Cemal\'in "sektör %1 -> QMLS %10 zıplar" varsayımı ölçüldü: beta 0,59, 1:1 civarı [yanlış yorum (Cemal\'in tezi)]', 'yanlış yorum', 'ölçüm', 'satış zamanlaması planı değişti', 'ölçüm yazıldı', 'Varsayım ölçülmeden karar olmaz', 'IZ_KARNE.py:1710'),
    _ik_h('2026-11-06', 'H107: ONERI_DEFTERI (DGXX); IK_GOREV 6-7 Kas', "DGXX portföyün %43 -> %55'i, QMLS ile aynı sektör (yoğunlaşma); YEOTK'de RİSK kapısı (boyut tavanı, çıkış olayı) yazılmadı", 'karar-boyut', 'ana model uyarısı / defter', 'açık pozisyon riski', '2x kuralı, bilanço günü kuralı yazıldı; YEOTK risk kapısı AÇIK', 'Aynı sektörde ikinci isim yoğunlaştırır', 'ONERI_DEFTERI.md Açık pozisyonlar; IZ_KARNE.py IK_GOREV 2026-11-06/07'),
    _ik_h('2026-11-06', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', 'ABD / BIST 10x raporları sade sıralama vermiyordu; mesajla verildi', 'iletişim', 'Cemal', 'karar yoktu', '"Raporu anlamadım, en iyi adaylar net değil"', '"Raporu anlamadım, en iyi adaylar net değil"', 'IZ_KARNE.py:1665'),
    _ik_h('2026-11-07', 'H092: IK_GOREV 7 Kas', 'QMLS zarar hesabı ekran görüntüsünden (≈ −658 $); Cemal "o kadar değil" dedi; işlem geçmişi eksik olabilirdi; hesap ekranıyla doğrulandı (≈ −33 bin TL, uyumlu) [hesap / iletişim]', 'iletişim', 'Cemal', 'sonuç doğrulandı', 'hesap düzeyi kontrol', 'Kısmi ekrandan toplam yazılmaz, hesap toplamı istenir', 'IZ_KARNE.py:1719-1735'),
    _ik_h('2026-11-08', 'H142: Ç147 (kripto)', "OKX / Gate'te delist edilenler yok (hayatta kalma yanlılığı); Binance ana API 451 ve Bybit 403 erişilemedi; komisyon / kayma ve güven aralığı yok [veri (sınır)]", 'veri', 'rapor sınırları', 'İZ DEĞİL yine de; sayılar iyimser', 'sınır yazıldı', 'Kripto evreni de batanları ister', 'IZ_KARNE.py:1033'),
    _ik_h('2026-11-09', 'H093: IK_GOREV 9 Kas', '"Kilit açılan token yükselir" anlaşıldı; doğrusu tersi (açılım ~%90 fiyata baskı, −%25)', 'iletişim', 'Cemal ("yanlış mı anladım")', 'düzeltme mesajı', 'tersi yazıldı', 'Yön cümlesi tek, net', 'IZ_KARNE.py:1746'),
    _ik_h('2026-11-09', 'H094: IK_GOREV 9 Kas; commit 71f74a4', 'SEC User-Agent e-postası Cemal tarafından yanlış yazılmış (veri etkilenmedi) [veri / süreç (Cemal)]', 'veri', 'Cemal', 'yok', 'doğru adres sonraki isteklerde', '—', 'IZ_KARNE.py:1772; git 71f74a4'),
    _ik_h('2026-11-09', 'H095: commit 7906203', 'IZ_KARNE Ç148 notunda tırnak hatası (dosya bozuk)', 'süreç', 'test', 'indeks yenilendi', 'düzeltildi', 'test_iz_karne her kayıtta', 'git 7906203'),
    _ik_h('2026-11-09', 'H096: Ç148-Ç150; IK_ACIK YOL 9 Kas', "K57 tam profil n 2-5; V_ABD'de ABD 2024-26 +%10,3 (n 31) geniş evrende +%4,8'e indi (örneklem şansı) [ölçüt (küçük örneklem)]", 'ölçüt', 'K57-B', 'hat kapandı', 'geniş evren', 'n < 30 hücre iz değil, ölçülemedi', 'IZ_KARNE.py:1045-1047'),
    _ik_h('2026-11-09', 'H097: DENETIM_10Kas #1', 'K57-C ön kaydı ölçümden önce commit edilmedi (ön kayıt 18:44, koşu 18:45, commit 18:51); 7 BOŞLUK git ile kanıtlanamıyor', 'süreç', 'ana model denetimi', 'karar değişmedi', 'kural: ön kayıt ayrı commit, sonra koşu', 'Ön kayıt kanıtı = git zamanı', 'DENETIM_10Kas.md #1'),
    _ik_h('2026-11-10', 'H098: DENETIM_10Kas #9', 'CENX için "finansman izi yok" denmişti; son 24 ayda S-3 kaydı var', 'yanlış yorum', 'ana model denetimi', 'izleme notu düzeltildi', 'düzeltme', "'Yok' demek için alan kontrol edilir", 'DENETIM_10Kas.md #9'),
    _ik_h('2026-11-10', 'H099: DENETIM_10Kas #6', 'K57 F4 (seyrelme yok) kuralı: CRC, IMMR pay sayısında ~1000 kat birim hatası; SLDP / TONX bölünme mi ihraç mı belirsiz', 'veri', 'ana model denetimi', "C1 kararını değiştirmez (85'te 2-4)", 'not', 'Birim denetimi', 'DENETIM_10Kas.md #6'),
    _ik_h('2026-11-10', 'H100: Ç151 (K58); IK_ACIK KARAR 10 Kas; YOL_HARITASI', "FI_OLCUT olay cetveli küçük etkiyi göremiyor: δ +%2'de n <= 300 güç en çok %11, dört hücre birden ~%0,2; 150 çalışmada 'iz yok' sonucunun büyük kısmı aracın kabalığından; n < 1.000 'İZ DEĞİL'ler aslında ÖLÇÜLEMEDİ [ölçüt (güç)]", 'ölçüt', 'K58 güç simülasyonu', 'eski kararların yorumu değişti (karar tabloları aynı); portföy cetveli kalibre aday', 'portföy cetveli v2 (plasebo 0/200)', 'Cetvelin gücü iz aramadan önce ölçülür', 'IZ_KARNE.py:1048, IK_ACIK "KARAR (10 Kas)"; arastirma_cikti/yol_haritasi/YOL_HARITASI_11Kas.md'),
    _ik_h('2026-11-10', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', 'ana model kod yazıp ölçüm koşarken denetim eksik kalıyordu ("her işte yanlışlık var")', 'süreç', 'Cemal', 'karar yoktu', 'Çalışma düzeni: ana model iş tanımı + denetim, alt ajan yapar', 'Çalışma düzeni: ana model iş tanımı + denetim, alt ajan yapar', 'CLAUDE.md Çalışma düzeni'),
    _ik_h('2026-11-11', 'H101: Ç153 (K59-B)', '3 ay tutma + örtüşen kohort cetveli (b) plaseboda GÜVENİLMEZ çıktı -> HÜKÜM YOK', 'ölçüt', 'plasebo', 'o deneme hükümsüz', 'plasebo raporda', 'Cetvel varyantı da plasebodan geçer', 'IZ_KARNE.py:1050'),
    _ik_h('2026-11-11', 'H102: Ç154 (K60)', "R2 olasılık tablosunda 106 seçilen hipotez OYNAKLIK etkisi (iki kuyruk birlikte şişer, ln katlar korelasyonu 0,89); 'K60-OLASILIK İZİ' 86 etiketi karar bilgisi değil; asimetri eki (ASIM) KASA'dan önce yazıldı", 'ölçüt', 'ön kayıt eki (KASA öncesi)', 'iz adayı 0, asimetrik fırsat 0', 'EK ölçüt', 'Tek kuyruk olasılığı oynaklığı ölçer', 'IZ_KARNE.py:1051'),
    _ik_h('2026-11-11', 'H103: Ç155 (K60-B)', "NDF_BS 'fırsat' etiketi yön değil KAPSAM etkisi (kalemi bildiren hisse %35-39); TAX_CHG KEŞİF'te kapsam etkisi", 'yanlış yorum', 'denetim', 'bilgi düzeyinde kaldı', "'uç / bildiren' katı yazıldı", 'Eksik veri grubu sinyal değildir', 'IZ_KARNE.py:1052'),
    _ik_h('2026-11-11', 'H104: commit 099b044', "K60-B rapor ifadesi yanlıştı (sayılar aynı); Ç155'e kapsam etkisi notu", 'iletişim', 'denetim', 'yok', 'düzeltildi', '—', 'git 099b044'),
    _ik_h('2026-11-11', 'H105: KARNE_11Kas; ONERI_DEFTERI Karne', 'Sıralamam (izleme 1-3) elenenleri geçmedi: ABD −1,0, BIST −3,6 puan (z −0,1 / −0,5) [karar (seçim gücü)]', 'karar-boyut', 'karne', 'öneri kapısı açılmadı', 'karne aylık', 'Erken karne kanıt değil; 16-25 ay gerekir', 'arastirma_cikti/oneri_karne/KARNE_11Kas.md:49-50; ONERI_DEFTERI.md Karne'),
    _ik_h('2026-11-11', 'H106: ONERI_DEFTERI (QMLS)', "Düşen hisseye üç ayda 7 alım, olaysız ekleme; zarar ≈ −650 $ (hesap zararının ≈%90'ı)", 'karar-boyut', 'Cemal', 'gerçek kayıp', "kalan yarı için olay kuralları; 'olaysız ekleme yok'", 'Boyut ve ekleme kuralı yazılı olmadan alım yok', 'ONERI_DEFTERI.md Kapanan pozisyonlar; IZ_KARNE.py:1719-1735'),
    _ik_h('2026-11-11', 'H108: K62_ON_KAYIT SAPMA 9', "İş Yatırım YILLIK (12 ay) değerleri sonraki yılın yeniden sunulmuş (TMS 29) değeriyle değişmiş: 4. çeyrek kazancı birim karışıklığı + GELECEK BİLGİSİ; DD/PD'de küçük ileriye bakma düzeltilemedi [geleceğe bakma (veri)]", 'geleceğe bakma', 'kanıt getiri hesabından önce (BIMAS 2022: 16,60 vs ilk açıklanan ~8,2 mlr)', "7 çeyrek SUETF'te KİRLİ sayıldı", 'kirli çeyrekler dışarıda', 'Yeniden sunulmuş veri sızıntıdır', 'arastirma_cikti/col_dis_bilgi/K62_ON_KAYIT.md:87-94'),
    _ik_h('2026-11-11', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', 'alt ajanların deftere yazması bağlam kopma riski', 'süreç', 'Cemal', 'karar yoktu', 'Defter yetkisi yalnız ana modelde', 'Defter yetkisi yalnız ana modelde', 'CLAUDE.md Defter yetkisi'),
    _ik_h('2026-11-11', 'Ç kaydı yok (CLAUDE.md / COL_OZET dersi)', 'mesajlar "bu yapıldı şu yapıldı" ile doluydu', 'iletişim', 'Cemal', 'karar yoktu', 'Sonuç dili: BULGU ile başla, süreç anlatımı yok', 'Sonuç dili: BULGU ile başla, süreç anlatımı yok', 'CLAUDE.md Sonuç dili'),
    _ik_h('2026-11-12', 'H109: K62_RAPOR', 'A / B makale tertili çeyrek içi (ileriye bakar); alınabilirlik ölçüsü yalnız C', 'ölçüt', 'ön kayıt', 'B tutar ama alınabilir değil', 'C ayrı ölçüldü', 'Makale tekrarı ile alınabilirlik ayrı', 'arastirma_cikti/col_dis_bilgi/K62_RAPOR.md:123'),
    _ik_h('2026-11-12', 'H110: K62B_ON_KAYIT SAPMA / H063 ile ilişkili', 'ABD açıklama günü 10-Q / 10-K başvuru günü alındı; şirketlerin çoğu bilançoyu 8-K basın bülteniyle GÜNLER önce açıklar -> tepki günü kayabilir [veri / ölçüt]', 'veri', 'ön kayıt', 'sonuç yorumu sınırlı', 'SAPMA yazıldı', 'Olay günü kaynağı doğrulanır', 'arastirma_cikti/col_dis_bilgi/K62B_ON_KAYIT.md:44, 110'),
    _ik_h('2026-11-12', 'H111: K66_ON_KAYIT SAPMA 5', 'Kimlik denetimi ilk taslakta İSİM eşleşmesiydi: ad değiştiren şirketlerin (XOM, NEE, SLB, MSTR, CPB) geçmişini düşürüyor; bugünkü ad sonraki bilgidir [geleceğe bakma / veri]', 'geleceğe bakma', 'kapsam incelemesi (getiri görülmeden)', 'ön kayıttan önce hacim uyumuna çevrildi', 'hacim uyumu', 'Bugünkü kimlik geçmişe uygulanmaz', 'arastirma_cikti/col_dis_bilgi/K66_ON_KAYIT.md:137-139'),
    _ik_h('2026-11-12', 'H112: K67_ON_KAYIT SAPMA 1', "İş tanımı 'Nasdaq takvimi' dedi ama takvim 2022-12'den başlıyor; 2017-21 bağımsız dönemi için bilanço günü yok [veri / süreç]", 'veri', 'ön kayıt', 'dönem tasarımı değişti', 'SAPMA 1-3', 'Veri kapsamı iş tanımından önce', 'arastirma_cikti/col_dis_bilgi/K67_ON_KAYIT.md:139-143'),
    _ik_h('2026-11-12', 'H113: VDYT_ON_KAYIT SAPMA 17; commit 06aa1b5', "wf koşusu BIST_K62'de KeyError 'T1' (K6 / P2 ana tanımı sabit 'T1'); koşu çöktü, sonuç görülmeden düzeltildi", 'hesap', 'koşu çöküşü', 'yok (eşik mührü aynı)', 'ana tanım pazarın ilk ANA kombinasyonu; pazar başına hata yakalama', 'Pazar-özel kombinasyon sabit kodlanmaz', 'arastirma_cikti/vdyt/VDYT_ON_KAYIT.md:271; git 06aa1b5'),
    _ik_h('2026-11-12', 'H114: Ç162 (VDYT)', "Motor 1 'basitten iyi' ama sıkışmaya özgü değil: rastgele bölgelerde aynı skill; kaynak bilanço takvimi + genişlemenin zaten başlamış olması (3 günlük pencere karar gününde açık) = mekanik [ölçüt (kontrol)]", 'ölçüt', 'P2 kontrol grubu', 'başarı yorumu sınırlandı', 'kontroller raporda', 'Üstünlük önce sıkışma dışı kontrolle sınanır', 'IZ_KARNE.py:1059'),
    _ik_h('2026-11-12', 'H115: commit 89d7bfa; IK_ACIK DRIVE 12 Kas', 'VDYT v1 sinyal grafiği başlığında grup adı sızıntısı (kör değerlendirmeyi bozar) [süreç (kör set)]', 'süreç', 'inceleme', '—', 'normal kipte kaldırıldı', 'Kör grafikte ad / grup yok', 'git 89d7bfa; IZ_KARNE.py IK_ACIK "DRIVE (12 Kas)"'),
    _ik_h('2026-11-12', 'H116: Ç163-Ç164 (VDYT2 / VDYT2-B A)', '"Bölgeyi bulmak BAŞARILI" ilanı tanımsaldı: büyük mum bölgenin kendi küçük mumlarına göre ölçülüyordu; mutlak ölçüyle BAŞARISIZ (bölge kontrollerden daha az büyük hareket) [ölçüt (tanımsal başarı)]', 'ölçüt', "Cemal'in sağlama isteği (mutlak hareket)", 'Ç163 kaydı değişmez, yorumu sınırlandı', 'VDYT2-B A', 'Başarı ölçüsü sinyalin kendi tanımından bağımsız olmalı', 'IZ_KARNE.py:1060-1061'),
    _ik_h('2026-11-12', 'H117: Ç165', "Tiingo Kasım kotası (500 sembol / ay) K56 EVREN2'de ~490 kullanılmış, VDYT2-B pilotu son payı yedi; B ölçülemedi, 1 Aralık'a kaldı [süreç (planlama)]", 'süreç', 'çekim ilk sembolde durdu', 'B ertelendi', "kota takvimi IK_ACIK'ta", 'Kota harcaması önceden planlanır', 'IZ_KARNE.py:1062'),
    _ik_h('2026-11-12', 'H118: IK_GOREV 12 Kas; commit 256475f', "Tiingo anahtarı ağ vekiline kaydedildi ama iki girişte 'Auth Token was not correct'; sonra çalıştı", 'süreç', 'hata mesajı', 'gecikme', 'yeniden kayıt', 'Anahtar pilotu önce', 'IZ_KARNE.py:1830; git 256475f'),
    _ik_h('2026-11-12', 'H119: VDYT2B_OHLC_DOGRULAMA; Ç165-Ç166', 'Tiingo batan OHLC: SUNE yanlış seri (iki şirket birleştirilmiş), CHK karışık, OTC döneminde >10 kat kuruş sıçramaları', 'veri', 'pilot doğrulama (12 bilinen batan)', 'KISMEN (8/12)', 'temizlik kuralları D1-D4 ön kayıtta', 'Batan verisi eksiksiz varsayılmaz', 'arastirma_cikti/vdyt/v2_20261112/VDYT2B_OHLC_DOGRULAMA.md; IZ_KARNE.py:1062-1063'),
    _ik_h('2026-11-12', 'H120: KOR_TEST_ON_KAYIT SAPMA 1; Ç166', 'Kör test v1.0 grafikleri her biri kendi 120 barlık min-max aralığına gerilmişti (otomatik ölçek, ortak ölçek yok): %1 oynayan hisse ile %8 oynayan aynı görünüyordu; Cemal işaretleyemedi [iletişim (gösterim)]', 'iletişim', 'Cemal', 'işaret alınamadı; v1.1 ortak log ölçek, 250 bar (0 işaret varken)', 'SAPMA 1', 'Karşılaştırmalı grafikte ortak ölçek zorunlu', 'arastirma_cikti/vdyt/v2_20261112/KOR_TEST_ON_KAYIT.md:196-210; IZ_KARNE.py:1063, 1840'),
    _ik_h('2026-11-12', 'H144: IK_ACIK VERİ (12 Kas)', 'evren_disi_ABD.csv repoda YOK (*.csv kuralı); COL_YOLU_ABD.py yeni ortamda durur; /tmp/k67_yahoo, k62_veri, k60_* yalnız konteynerde (kalıcılık riski)', 'süreç', 'veri envanteri', 'yeni oturumda koşu durabilir', '.gitignore istisnası + islenmis-veri dalı (açık)', 'Ayar dosyası repoda, ara veri dalda', 'IZ_KARNE.py:1879; `git ls-files` 0 sonuç'),
    _ik_h('2026-11-13', 'H121: Ç166', "v1.1'de de Cemal 'hiçbir belirti yok, rastgele bölge' dedi -> İŞARET YOK: G5 dedektörü Cemal'in gözündeki sıkışmayı seçmiyor [yanlış yorum (dedektör)]", 'yanlış yorum', 'Cemal', "Aralık Tiingo kotası VDYT2-B'ye harcanmaz", 'önceden yazılı kural uygulandı', 'İnsan gözü kör testi dedektörden önce', 'IZ_KARNE.py:1063'),
    _ik_h('2026-11-13', 'H122: Ç167 (GOZ_G5)', "G5 Cemal'in çöllerinin 1/29'unu yakalıyor, olumsuzlarda daha sık (2/8); en iyi basit ölçü AUC 0,77 / 0,68 [yanlış yorum (dedektör)]", 'yanlış yorum', 'ölçüm', 'VDYT / sessiz bölge hattı kapanış önerisi', '—', 'Ç07 ile aynı: şekil ölçüsü çölü olumsuzdan ayırmıyor', 'IZ_KARNE.py:1064'),
    _ik_h('2026-11-13', 'H123: TAVAN_RAPOR başlık (SAPMA)', "`ts_donem` kriz sonrası BİLGİ olaylarında 'tanim' anahtarında çöküyordu (döngü sırası)", 'hesap', 'koşu çöküşü', 'yok (tanım / eşik aynı)', 'döngü sırası düzeltildi', '—', 'arastirma_cikti/tavan_serisi/TAVAN_RAPOR.md:3'),
    _ik_h('2026-11-13', 'H124: Ç168 (TAVAN)', "k=1 'KUMAR' (medyan fark −%3,9 [−14,5; +9,4]); k >= 2 örneklem yetersiz (n 42) [ölçüt (örneklem)]", 'ölçüt', 'ölçüm', 'İZ DEĞİL; kriz sonrası açık', '—', "Aralık 0'ı kapsıyorsa 'kumar' yalnız betimleme", 'IZ_KARNE.py:1065'),
    _ik_h('2026-11-13', 'H125: Ç169 (HACİM); HACIM_RAPOR', "H1 ana hücre n 11 (9 hisse, 8'i 2016-19), kontrollü 5 olay: 'KANIT YOK' dendi; ilk raporda oran sütunu yalnız eşleşik oranı 'olay' diye yazıyordu (biçim düzeltmesi) [ölçüt (örneklem) / iletişim]", 'iletişim', 'ölçüm + rapor düzeltmesi', 'KANIT YOK (örneklem yetersiz)', 'rapor sütunları düzeltildi', "n 11 ile karar yazılmaz, 'ölçülemedi' yazılır", 'IZ_KARNE.py:1066; arastirma_cikti/tavan_serisi/HACIM_RAPOR.md:3'),
    _ik_h('2026-11-13', 'H126: Ç170 (GENİŞ KESİT)', 'Geri alım emaresi tek olaydan (31.10 -> 13.11, 64 hisse) [ölçüt (tek olay)]', 'ölçüt', 'ölçüm', 'İZ DEĞİL (emare)', '2018 / 2020 çöküşlerinde ön kayıtla sınanacak', 'Tek olay iz değil', 'IZ_KARNE.py:1067'),
    _ik_h('2026-11-13', 'H127: Ç171 soru alanı', "BofA için ilk tasarım 60 gün sabit ufuktu; Cemal 'alımından satımına kadar takip et, 60 gün değil' dedi [ölçüt / iletişim]", 'iletişim', 'Cemal', 'ana ölçü tutma dönemi oldu, 60g ikincil', 'tasarım değişti', "Ufuk Cemal'in sorusuna göre, sabit 60 gün varsayılmaz", 'IZ_KARNE.py:1068'),
    _ik_h('2026-11-13', 'H128: Ç171 DÜZELTME; commit 763ae34', "BofA ayrıştırma 1: çok kurumlu haberde tablo kurumu yanlış etiketlendi (94283 blok 1 İş Yatırım'ınmış)", 'ayrıştırma', 'ana model denetimi (ham HTML)', 'karar değişmedi', 'kurum önceki başlıktan; belirsiz -> BİLİNMİYOR', 'Çok tablolu sayfada etiket tablodan önceki metinden', 'IZ_KARNE.py:1068; git 763ae34'),
    _ik_h('2026-11-13', 'H129: Ç171-Ç172; BOFA_KAR_RAPOR §9', "BofA ayrıştırma 2: aylık / dönemsel özet haberleri (45) günlük liste sayıldı; 01.09 hisse.net 'Ağustos'ta milyarlar' TL tutarları lot birimli okundu -> A'da 7 kriz sonrası satır, FIFO lot toplamları şişkin", 'ayrıştırma', 'ana model denetimi', 'karar değişmedi', "tur='aylik'/'donemsel' kapsam dışı", 'Haber türü (günlük / aylık) ayrıştırmadan önce', 'arastirma_cikti/bofa_izi/BOFA_KAR_RAPOR.md:216; IZ_KARNE.py:1068-1069'),
    _ik_h('2026-11-13', 'H130: Ç171-Ç172; commit a9c00ea', "BofA ayrıştırma 3: hisse.net'te aynı adreste biriken günlük güncellemeler (2 haber, 208 bölüm, 1.399 satır) haberin ilk tarihini taşıyordu: Eylül listesi Haziran sayıldı = GELECEĞE BAKMA; düzeltince A 20g medyan +%3,2 -> −%3,9, kâr oranı %57 -> %39 [geleceğe bakma / ayrıştırma]", 'geleceğe bakma', 'alt ajan (düzeltme sırasında)', "'BofA normal dönemde piyasa gibi +%3' ifadesi değişti; kararlar (kanıt yok / yol yok) aynı", 'güncelleme damgası kendi tarihini taşır', 'Sayfa tarihi değil satır tarihi', 'IZ_KARNE.py:1068-1069; git a9c00ea'),
    _ik_h('2026-11-13', 'H131: Ç171', "BofA ayrıştırma 4: YatırımX / Rota kenar kuşağı çöpü (SSAAT 100 satır, 79'u BofA ilk 3'teydi) gövde sayıldı", 'ayrıştırma', 'alt ajan', 'karar değişmedi', 'ilgili haber kuşağı gövde dışı', 'HTML gövde sınırı test edilir', 'IZ_KARNE.py:1068'),
    _ik_h('2026-11-13', 'H132: BOFA_RAPOR düzeltme bloğu', "BofA ayrıştırma 5: kurum adı hisse sanıldı ('HSBC: −433 mn' satırı); numaralı tek satırlık tablolar ayrı listeler sayıldı", 'ayrıştırma', 'ana model denetimi', 'karar değişmedi', 'satırlar düştü; tek liste', 'Hisse sütunu sembol sözlüğüyle denetlenir', 'arastirma_cikti/bofa_izi/BOFA_RAPOR.md:5'),
    _ik_h('2026-11-13', 'H133: Ç171-Ç172', "'Kuruş hisse lot listelerinde işaret ters (−%6,4; K6 anlamlı ters)' iddiası kirli veriden; düzeltmeden sonra kalktı (+%2,4 / −%0,8, aralık 0'ı kapsıyor) [yanlış yorum (kirli veri)]", 'yanlış yorum', 'yeniden ölçüm', 'iddia geri alındı', 'raporlarda ESKİ -> YENİ tablosu', "'Anlamlı ters' iddiası ayrıştırma denetiminden sonra", 'IZ_KARNE.py:1068-1069; IZ_KARNE.py:1858'),
    _ik_h('2026-11-13', 'H134: BOFA_RAPOR eski_v1 SAPMA; BOFA_KAR_RAPOR §9', 'DUNYH 12.11 −%85 bayat Yahoo fiyatı (giriş günü hacim 0, askı); gerçek değil', 'veri', 'denetim', 'kriz tablosu bilgi', 'hacim 0 işareti (gösterim)', 'Hacim 0 gün fiyatı bayat sayılır', 'arastirma_cikti/bofa_izi/eski_v1/BOFA_RAPOR.md:129; BOFA_KAR_RAPOR.md:217'),
    _ik_h('2026-11-13', 'H135: Ç171 kriz notu; Ç172 son cümle; IK_GOREV 13 Kas', "'TEHOL 15.09 alım -> −%97,5' ve −%40..−%65 sayıları BofA'nın gerçekleşen zararı gibi yazıldı; bunlar alım günü maliyetinden 20 gün sonraki fiyat değişimi; AKD kodu kurum pozisyonu değil müşteri akışı [yanlış yorum / iletişim]", 'yanlış yorum', 'Cemal ("BofA %40-80 zarar etmez, mümkün değil")', 'mesaj düzeltildi; kararlar aynı', 'Ç172 sonuna açıklama', 'Fiyat değişimi ile gerçekleşen kâr/zarar ayrı yazılır', 'IZ_KARNE.py:1068-1069, 1858-1864'),
    _ik_h('2026-11-13', 'H136: bu oturum (ana model denetimi); repoda kayıt yok', "'2.11 PEKGY listede 1.' bilgisi yanlıştı: PEKGY o listede 4. sıradaydı [ayrıştırma / iletişim]", 'ayrıştırma', 'ana model denetimi', '—', 'mesajda düzeltildi', 'Sıra bilgisi ham tablodan okunur', 'iş tanımı (14 Kas); repoda satır yok'),
    _ik_h('2026-11-13', 'H137: bu oturum (ana model); repoda kayıt yok', "Ana model hızlı FIFO kontrolünde blok filtresi uygulamadı: KTLEV 09.09 33,8 satırı Tera'nın (blok 2+) satırıydı, BofA sanıldı [hesap (denetimde)]", 'hesap', 'ana model kendi kontrolü', 'denetim sonucu düzeltildi', 'blok_2_ve_sonrasi kapsam dışı (93 satır)', 'Denetim kontrolü de ayrıştırıcının filtresini uygular', 'iş tanımı (14 Kas); arastirma_cikti/bofa_izi/BOFA_KAR_RAPOR.md:208'),
    _ik_h('2026-11-14', 'Ç164 (VDYT2-B A) yorum', '"Bölge kontrollerden DAHA AZ büyük hareket üretiyor; sakin hisse sakin kalır" bulgu diye yazıldı. DIŞARI eşleri aynı NATR ondalığında ama bölgenin NATR14 / ATR250 oranı düşük (ABD 0,53 vs 0,62; BIST 0,51 vs 0,64). σ250 / ATR250 tabanlı mutlak eşik bölge için mekanik olarak daha zor. Oranla düzeltilince fark ABD WF MA3\'te kayboluyor, BIST KASA\'da işaret dönüyor. [yanlış yorum / ölçüt (kontrol)]', 'yanlış yorum', 'alt ajan (VDYT denetimi)', 'Ç164 kararı (bölge mutlak harekette üstün değil) kalır; "daha az / sakin kalır" ifadesi geçersiz', "Ç164'e DÜZELTME notu; yeniden koşuda oran eşleşmesi", 'Uzun pencereli oynaklıkla ölçeklenen mutlak etiket, kısa / uzun oynaklık oranında da eşleşme ister', 'scratchpad artik.py; VDYT2B.py:282-325'),
    _ik_h('2026-11-14', 'Ç164 BIST karar hücresi', 'BIST MA1 (ANA etiket) "BAŞARISIZ" yazıldı. Bölge tarafında olay sayısı 6 (WF) ve 12 (KASA), DIŞARI aralığı 0\'ı içeriyor. [ölçüt (küçük örneklem / güç)]', 'ölçüt', 'alt ajan (VDYT denetimi)', 'BIST (1)-mutlak: BAŞARISIZ → ÖLÇÜLEMEDİ', 'etiket değişikliği', "Nadir sonuçta satır n'i değil olay sayısı güç belirler", 'VDYT2B_RAPOR_A.md §2, §4'),
    _ik_h('2026-11-14', 'Ç162 (VDYT v1) Motor 2', 'ABD yön "BASİTTEN İYİ" yazıldı. Yön tanımı (bölge aralığından ilk çıkılan kenar) fiyatın bölge içi konumuyla mekanik olarak belirleniyor, B1 temeli konumu içermiyor. [ölçüt (mekanik üstünlük)]', 'ölçüt', 'alt ajan (VDYT denetimi)', 'Motor 2 ABD → İZ DEĞİL (v2 aynı sonucu doğruladı)', "Ç162'ye DÜZELTME notu", "Yön tahmininin temeli konumu içermeli (v2'de B2 vardı ama karar temeli değildi)", 'VDYT_ON_KAYIT.md §4.5; VDYT_RAPOR.md §1'),
    _ik_h('2026-11-14', 'Ç163 VDYT2 KASA', "VDYT2'nin KASA dönemi (2024-26/08), VDYT v1'de 07:22'de açılmıştı. v2 tasarımı (D1-D4) v1 KASA sonuçları görülerek yazıldı. VDYT2 ve VDYT2-B için bekletme (holdout) temiz değil. [süreç (ön kayıt / bekletme)]", 'süreç', 'alt ajan (VDYT denetimi)', 'olumsuz kararlar etkilenmez; olumlu (1) zaten tanımsal', 'yeni sürümde KASA yerine ileri test (2026-09 sonrası)', 'Bir dönem bir kez açılır; aynı soruya ikinci sürüm yeni dönem ister', 'vdyt_kasa_acildi.json; VDYT2_ON_KAYIT.md §1'),
    _ik_h('2026-11-14', 'Ç163 başarı (2b)', 'Bölgeye özgü bilgi testi Brier skill FARKI ile yapıldı. Gerçek ve kontrol gruplarının etiket tanımı (referans penceresi) ve taban oranları farklı (%16-33). Skill farkı karşılaştırılabilir değil.', 'ölçüt', 'alt ajan (VDYT denetimi)', '(2) zaten BAŞARISIZ; karar değişmez', 'yeniden koşuda aynı etiket tanımı + log loss / AUC farkı', 'Farklı tabanlı gruplarda Brier skill farkı yorumlanmaz', 'VDYT2.py:1148-1170'),
    _ik_h('2026-11-14', 'Ç162-Ç164 satır verisi', 'Satır / kontrol tabloları ve fiyat önbellekleri yalnız konteynerde (/tmp/vdyt*, /tmp/veri). Repoda ve islenmis-veri dalında yok. Bugün yeniden üretilebildi, konteyner giderse üretilemez. [süreç (kalıcılık)]', 'süreç', 'alt ajan (VDYT denetimi)', 'yeniden üretim riski', 'satir_*_G5 / kontrol_*_G5 (kasa) + fiyat_ABD.pkl özetini islenmis-veri dalına (Cemal onayı: yeni veri)', 'Ölçüm biter bitmez satır verisi kalıcı yere', 'H144 ile aynı tür'),
    _ik_h('2026-11-14', 'IZ_KARNE eski "İZ DEĞİL" etiketleri', 'Tek cetvelde n < 1.000 olan ve güç kanıtı bulunmayan en az 20 kayıt "İZ DEĞİL" yazılı (Ç38, Ç39, Ç50, Ç57, Ç67-Ç70, Ç73-Ç83, Ç87, Ç89, Ç90 ...). Yeni kurala göre ÖLÇÜLEMEDİ olmalı. [ölçüt (etiket)]', 'ölçüt', 'alt ajan (VDYT denetimi)', 'iddia kapanmamış sayılır', 'indekste etiket düzeltmesi (bölüm 3)', 'Etiket güçle birlikte yazılır', 'karne_hucre.csv; IZ_DEFTERI indeks'),
    _ik_h('2026-11-14', 'Ç37 D9', '"Test sürüyor" diye kalan D9 uzun çöl + rüzgâr hiç kapanmadı, yeni cetvelle puanlanmadı, üretim ekranında (T8) duruyor. [süreç (açık kalan)]', 'süreç', 'alt ajan (VDYT denetimi)', 'üretimde ölçülmemiş bir ölçü gösteriliyor', 'yeniden koşu sıra 3', "Açık kalan ölçüm IK_ACIK'a yazılır", 'IZ_KARNE Ç37; COL_OZET §9.1'),
    _ik_h('2026-11-14', 'Ç174 SIKISMA_YENIDEN (ön kayıt öncesi)', 'Bölünme şüphesi süzgecinin ilk hali sıçramanın geri dönüş bacağını da şüpheli sayıyordu', 'hesap', 'test', 'ön kayıttan önce düzeltildi', "'önceki 10 gün düz' şartı", 'Süzgeç sentetik veriyle iki yönlü sınanır', 'SIKISMA_ON_KAYIT.md HATA 1'),
    _ik_h('2026-11-14', 'Ç174 SIKISMA_YENIDEN (ön kayıt öncesi)', 'Bootstrap tohumu Python hash() ile türetiliyordu; her süreçte değişiyor, sonuç yeniden üretilemezdi', 'hesap', 'test', 'ön kayıttan önce düzeltildi', 'zlib.crc32 tohum', 'Tohum deterministik olmalı', 'SIKISMA_ON_KAYIT.md HATA 2'),
    _ik_h('2026-11-14', 'Ç174 SIKISMA_YENIDEN (ön kayıt öncesi)', "Genel karar fonksiyonu dört hücre 'EMARE (güç sınırlı)' iken 'İZ DEĞİL' yazıyordu", 'ölçüt', 'test', 'ön kayıttan önce düzeltildi', "etiket 'ADAY / ÖLÇÜLEMEDİ'", 'Karar etiketi güçle birlikte yazılır', 'SIKISMA_ON_KAYIT.md HATA 3'),
    _ik_h('2026-11-14', 'Ç174 BIST hücresi', "BIST ±%10 fiyat sınırı yüzünden günlük TR/C en çok ~%20; olayların %9'unda 3 x ATR250 eşiği imkânsız: BIST B1 sonuçları aşağı yanlı", 'veri', 'alt ajan', 'BIST zaten bilgi; karar değişmez', 'raporda yazılı', 'Marjlı pazarda mutlak eşik marjla kıyaslanır', 'SIKISMA_RAPOR.md sınırlar'),
    _ik_h('2026-11-14', 'Ç174 raporu', 'BIST 2023 model skill +0,46 görünüyor ama test döneminde gerçekleşen oran %0; sayı anlamsız; kod sha kilidi yüzünden raporda düzeltilmedi', 'yanlış yorum', 'alt ajan', 'karar dışı hücre', 'teslimde yazılı', 'Boş sınıfta skill basılmaz', 'SIKISMA_RAPOR.md'),
    _ik_h('2026-11-14', 'Ç174 iş tanımı (ana model)', 'Ana model alt ajan iş tanımına kontrol listesi metni yerine yanlışlıkla bir Python ifadesi (open(...).read()) yazdı; ajan listeyi dosyadan okudu, ikinci mesajla düzeltildi', 'iletişim', 'ana model kendi kontrolü', 'etkisiz (kapı geçti)', 'ikinci mesaj + yeni ajanda düz metin', 'İş tanımı gönderilmeden okunur; şablon metni düz yazılır', 'sohbet 14 Kas'),
    _ik_h('2026-11-14', 'Ç176 duyarlılık', 'Yön etiketi yalnız n olay >= 30 şartına bakıyor; büyük gün sayısı < 10 olan hücrelerde bootstrap dejenere (BIST 2023 KAT 7,50 [7,50; 7,50]; k=4 sıfır büyük gün 0,00) ve BH bunları seçti', 'ölçüt', 'alt ajan', 'bilgi hücreleri; karar değişmez', 'raporda okunmaz diye işaretli; sonraki sürümde en az 10 büyük gün şartı', 'Oran kıyasında güç olay sayısıyla değil nadir sonucun sayısıyla belirlenir', 'DUYARLILIK_RAPOR.md HATA 1'),
    _ik_h('2026-11-14', 'Ç177 iş tanımı (ana model)', "İş tanımındaki bölünme şüphesi kuralı ileri pencerede uygulansaydı sonuca göre seçim olurdu: ANA kuralın yakaladığı günlerin %89'u 1,5-2x gerçek hareket; ABD 2023-25 pencerelerinin %5-9'u silinip +%100 / -%50 sıçramaları yok edilirdi", 'ölçüt', 'alt ajan', 'cetvel düzeltildi (ileri dışlama yok); karar yoktu', 'ileri pencerede bölünme dışlaması kaldırıldı, geçmiş pencerede kaldı', 'Sonuç penceresine uygulanan hiçbir süzgeç sonucu okumaz', 'CETVEL_ON_KAYIT.md'),
    _ik_h('2026-11-14', 'Ç174 / Ç176 SIKISMA_YENIDEN', "Aynı bölünme kuralı [t-260, t+41] penceresinde uygulanmış: ileri pencerede sıçrama günleri dışlanmış olabilir (büyüklük ölçülmedi); B1 'büyük gün' olasılığını aşağı çekme ihtimali", 'ölçüt', 'alt ajan (Ç177)', 'Ç174 kararı: etki ölçülmedi, karar şimdilik aynı; ileri testte (Mart 2027) ileri dışlamasız yeniden koşulacak', 'IK_ILERI Ç174 satırına koşul eklendi', 'Süzgeç penceresi karar gününde biter', 'ORTAK_CETVEL teslimi HATA 2'),
    _ik_h('2026-11-14', "FON_IZI FI_OLCUT (K27'den beri)", "fi_olcut_panel havuzu ileri r60'ı olan hisselerle kuruluyor: eş hücresi kurulurken küçük bir ileri bilgi (60 gün sonra hâlâ fiyatı olan hisseler); önceki FI_OLCUT sonuçları etkilenebilir, etki büyük olasılıkla küçük", 'geleceğe bakma', 'alt ajan (Ç177)', 'önceki kararlar değişmedi; büyüklük ölçülmedi', "ORTAK_CETVEL havuzu geçmiş kipinde; FON_IZI'de düzeltme ayrı iş", 'Havuz yalnız karar günü bilgisiyle kurulur', 'ORTAK_CETVEL teslimi HATA 3; FON_IZI fi_olcut_panel'),
    _ik_h('2026-11-14', 'FI_OLCUT / ORTAK_CETVEL portföy şartı', "10 yuvalı slot portföy şartı gücü n'den bağımsız tavanlıyor (δ +%5'te %54-65); 'güç >= %80' yolu gerçek veride açılmıyor; gerçek +%5 etki dört hücreyi ~%13 olasılıkla geçer", 'ölçüt', 'alt ajan (güç simülasyonu)', "Cemal'in şartı gereği cetvel değiştirilmedi; İZ DEĞİL yalnız n >= 1.000 hücrede", 'sınır olarak yazıldı; ileride yuva sayısı / portföy kuralı değişikliği ancak yeni cetvel sürümüyle', 'Bir karar şartının gücü iz aramadan önce ölçülür', 'GUC_TABLOSU.md'),
    _ik_h('2026-11-14', 'FON_IZI tarayıcıları (fi_k24_tara n<200; fi_k13 / fi_k17 n<400; fi_k23_parmak n<L+200)', "Hisse atlama şartı serinin TOPLAM uzunluğuna bakıyor; toplam uzunluk gelecekteki barları içerdiği için geleceğe bakma. K24'te 1.430 sinyal etkilendi; eski Ç75-Ç78, Ç96 / Ç113 / Ç118, Ç124 bu sinyalleri içeriyordu", 'geleceğe bakma', 'alt ajan (Aşama 2, 4, 5 ayrı ayrı buldu)', 'yeni koşularda t anına indirildi (SAPMA); eski kararlar: etki küçük tahmin, ölçülmedi', 'K24_YENIDEN / DIP_COL_AYRIM / INTEM_ILERI kendi modüllerinde düzeltti; FON_IZI düzeltmesi ayrı iş (yasak dosya). DÜZELTME 15 Kas: FON_IZI v1.40, 8 tarayıcı (fi_k4 / k4b / k6 / k13 / k14 / k17 / k23_parmak / k24) karar günü konumu t >= N-1; test_fon_izi 63 önek değişmezliği eski kodda 8 / 8 kırmızı, yeni kodda yeşil; gerçek veri (V_BIST + V_ABD, 31.08.2026 kesik) düşen: K24 kural -209 / -515, K17 -21 / -81, K14 eşli -46 / -159, K13 0 / -2, K23 L15 pencere -%9,4 / -%8,4; t < N-1 günleri tekilleştirme durumuna girmediği için 9 hücrede 1-157 yeni satır (alt küme değil); ana model 2 hücreyi bağımsız yeniden üretti (K24 kural BIST 3.114 -> 2.905, K13 ABD 158 -> 156). Eski kararlar değişmedi', 'Seri uzunluğu şartı daima karar günü konumuyla (i >= N) yazılır', 'K24_YENIDEN_ON_KAYIT SAPMA-1; DIP_COL_AYRIM HATA 1; INTEM_ILERI SAPMA-1'),
    _ik_h('2026-11-14', 'ORTAK_CETVEL oc_hucre', 'İki yarı ayrımı için olaylar giriş gününe göre kararlı olmayan sıralamayla diziliyor; aynı gün girişli olayların sırası değişebildiği için iki yarı ortalaması 0,1-0,3 puan oynuyor', 'hesap', 'alt ajan (Aşama 2)', 'bu koşuda etiket değişmedi', "cetvel v1.1'de kararlı sıralama (tarih, sembol); v1.0 dört aşama bitince", 'Sıralama anahtarı tam belirlenir', 'K24_YENIDEN teslimi HATA 3'),
    _ik_h('2026-11-14', 'Ç180 iş tanımı (ana model)', "İş tanımında 'Avrupa V_AVR Ç124'te hiç yok' yazıldı; yanlış: Ç124 AVR'yi kullanmış (k44_eslesme.csv 117 + 271; Ç124 notu 'AVR 2016-22 +15,0 n 92'). Görülmemiş veri yalnız ABD k34 ekine indi", 'süreç', 'alt ajan (Aşama 5)', 'AVR karar hücreleri boş; etiket en fazla ÖLÇÜLEMEDİ', 'ajan ön kayıtta düzeltti', "İş tanımındaki 'görülmemiş' iddiası kayıttan doğrulanmadan yazılmaz", 'INTEM_ILERI teslimi HATA 1'),
    _ik_h('2026-11-14', 'asama_ortak.txt (ana model)', "'V_BIST 2023-06'dan başlar' notu yanlış: /tmp/veri/V_BIST.pkl 2015-06'dan başlıyor (CLAUDE.md'deki veri_1d_turkey.pkl notuyla karıştırıldı)", 'iletişim', 'alt ajan (Aşama 5)', 'etkisiz', 'not düzeltildi', 'Veri sınırı dosyadan okunur, hafızadan yazılmaz', 'INTEM_ILERI teslimi HATA 2'),
    _ik_h('2026-11-14', 'Ç181 D9_YENIDEN etiketi', "Ajan (c) yalnız rüzgâr satırına 'İZ DEĞİL (AVR verisi yok)' etiketi yazdı; kurala göre AVR olay verisi yoksa karar en fazla ABD-ADAY, ABD'de portföy şartı düştüğü için 'ABD TUTMADI, AVR ÖLÇÜLEMEZ' olmalı; 'İZ DEĞİL' iddiayı yanlış kapatır", 'yanlış yorum', 'ana model denetimi', 'etiket düzeltildi; iddia açık (IK_ILERI)', 'Ç181 notunda düzeltme', "Veri olmayan pazar için 'iz değil' yazılmaz", 'D9_YENIDEN teslimi'),
    _ik_h('2026-11-14', 'Ç181 D9_YENIDEN süreç', "Koşu 13:55'te bitti, sonuç dosyaları 15:40'a kadar commit'siz kaldı (ajan arka plan bildirimini bekledi); ana modelin bekleme döngüsü ajan çıktı dosyası boş olduğu için bitişi göremedi", 'süreç', 'ana model + alt ajan', 'sonuca etkisi yok', "hemen commit kuralı; ana model bekleme döngüsü git log'a bakar", "Koşu biter bitmez commit; bekleme git'ten izlenir", 'D9_YENIDEN teslimi HATA 3'),
    _ik_h('2026-11-14', 'Ç181 D9_YENIDEN tercil', "Rüzgâr şiddeti tercil sınırları bütün rüzgâr günlerinden kuruldu, tekil olaylar ABD'de alt tercilde toplandı (ABD 2023 T3 n 50): alt grup yorumu zayıf", 'ölçüt', 'alt ajan', 'bilgi tablosu; karar dışı', 'ileri testte tercil sınırları sabit (0,1402 / 0,2222) ön kayıtla', 'Alt grup sınırları olay dağılımından kurulur', 'D9_YENIDEN teslimi HATA 5'),
    _ik_h('2026-11-14', 'Ç181 D9_YENIDEN (ön kayıt öncesi)', "d9_ruzgar_panel'de pandas indeksi mikrosaniye iken nanosaniye sanıldı, rüzgâr hep NaN; sentetik test yakaladı", 'hesap', 'test', 'ön kayıttan önce düzeltildi', 'gün tamsayısına geçildi', 'Tarih birimi testle sınanır', 'D9_YENIDEN teslimi HATA 1'),
    _ik_h('2026-11-15', 'Ç174 / Ç176 sıkışma tanımı (S1) ve kör örnek PDF', "Cemal: 'bin-üç bin olay dediğin sıkışmalar gerçek sıkışma değil, rastgele seçilmiş bölgeler; son iki çıktı tamamıyla rastgele' — 10 günlük S1 tanımı ve varyantları Cemal'in çöl / sıkışma gözüyle örtüşmüyor (Ç166 kör test ve Ç167 G5 ile aynı ders: algoritmik bölge tanımı insan gözünün bölgesini bulmuyor)", 'ölçüt', 'Cemal', "Ç174 / Ç176 kararı 'S1 tanımı için' geçerli kalır; Cemal'in sıkışması için ölçülmemiş sayılır; yön değişti: tersten (büyük mumdan geriye) parmak izi (Ç182)", "TERS_PARMAK iş tanımı: keşif / doğrulama ayrımı, Cemal'in gözüne kör örnek", "Bölge tanımı önce gözle doğrulanmadan 'sıkışma' diye binlerce olay sayılmaz", 'sohbet 15 Kas; Ç166, Ç167, Ç174, Ç176'),
    _ik_h('2026-11-15', 'Ç182 iş tanımı (ana model)', "İlk iş tanımında büyük hareket yalnız tek günlük B1 idi; BIST ±%10 sınırı yüzünden Cemal'in gönderdiği örnek (3 hafta bant, 8 günde -%30 art arda taban) ölçüm dışı kalacaktı; keşiften önce BH2 (20 gün çok günlü) eklendi", 'ölçüt', "ana model (Cemal'in grafiği üzerine)", 'keşiften önce düzeltildi; sonuç etkilenmedi', 'BH2 ikinci etiket', "Marjlı pazarda 'büyük hareket' çok günlü tanımla da ölçülür", 'TERS_ON_KAYIT_B.md; sohbet 15 Kas'),
    _ik_h('2026-11-15', 'Ç182 keşif d denetimi', 'Rapor HAVUZ tablosunda son_mum d 0,257, ana modelin satır verisinden hesabı 0,228-0,232 (havuzlanmış / Glass); fark küçük, yön aynı; tanım farkı (ağırlık / pazar içi) ajandan soruldu', 'hesap', 'ana model denetimi', "karar değişmez (KAT'lar birebir)", 'ajan açıklaması beklendi; rapor yeniden koşulmadı', 'Rapor d tanımı (kırpma / ağırlık) başlıkta yazılı olmalı', 'Ç182 denetimi; ajan yanıtı: KIRPMA (%1-%99) sonrası d 0,2571, kırpmasız 0,231; karar değişmez'),
    _ik_h('2026-11-15', 'Ç182 AVR verisi', "AVR barlarının %0,2-0,4'ünde açılış ya da kapanış H-L aralığının dışında (ABD / BIST'te ~0); ham haliyle gövde / fitil oranları ±145'e çıkıyordu; keşiften önce H = max(H,O,C), L = min(L,O,C) ile düzeltildi", 'veri', 'alt ajan', 'keşiften önce düzeltildi', 'aralık genişletme', 'Yeni pazar verisinde OHLC tutarlılığı (L <= O,C <= H) kontrol edilir', 'TERS_PARMAK teslimi HATA 1'),
    _ik_h('2026-11-15', 'asama_ortak.txt / ORTAK_CETVEL notu (ana model)', "'V_BIST 2023-06'dan başlar' notu yanlış: 581 BIST hissesinin 474'ünün verisi 2015-06'dan; ön kayıt B'deki 'BIST ilk uygun gün ~2024-06' cümlesi de yanlış; BIST bilgi olduğu için karar etkilenmedi (ikinci kez: Ç180 da bulmuştu)", 'iletişim', 'alt ajan', 'etkisiz', "asama_ortak.txt düzeltilecek; ORTAK_CETVEL notu v1.1'de", 'Aynı yanlış not iki kez tekrarladı: kaynak dosyadan okunur', 'TERS_PARMAK teslimi HATA 2; INTEM_ILERI HATA 2'),
    _ik_h('2026-11-15', 'Önceki sohbet hafızası', "Cemal: 'ben bu fizik demiştim, sen değil demiştin'; önceki sohbetlerin hafızası yok, defterde / özette de kayıt yok: hipotez tartışmaları deftere yazılmamıştı", 'süreç', 'Cemal', 'doğrulanamadı', 'bundan sonra hipotez / itiraz tartışmaları IK_GOREV istek alanına yazılır', 'Sözlü anlaşmazlık da kayıttır', 'sohbet 15 Kas'),
    _ik_h('2026-11-15', 'BOLGE_LISTESI_CEMAL.md (ana model)', "Cemal'e gönderilen bölge listesi bölünme / bedelsiz süzgeci olmadan ham ekran fiyatından üretildi: FENER 16.12.2025 satırında '-%65' ve '%63,8 mum' bölünme günüydü (29.12.2025); en kötü 10 listesi kirliydi", 'veri', "ana model (Cemal'in FENER grafiği üzerine)", 'liste düzeltilip yeniden gönderildi; ölçüm kararları etkilenmedi (ölçüm modüllerinde süzgeç vardı)', '|ln getiri| > ln 1,5 süzgeci; D bölümü eklendi', "Hızlı 'bakış' listesi de K6 süzgecinden geçer; K3 / K6 ikinci kez (H004 / H037 gibi) tekrar", 'sohbet 15 Kas'),
    _ik_h('2026-11-15', "Ç174 / Ç176 S1 sıkışma tanımı (Cemal'in FENER örneği)", "S1 yalnız 'küçük mum + 10 gün bant' soruyor; FENER'de 3-16 Ara 2025'i seçti (mum 0,46 x ATR ama net -%6 kayma, Bollinger genişliği 250 gün yüzdelik 0,70); Cemal'in bölgesi 14 Eki - 7 Kas 2025 (18 bar, net +%4, BB yüzdelik 0,02) seçilmedi. Ana model ekran fiyatıyla doğruladı. Tanımda eksik: yataylık (net kayma), dar Bollinger (uzun dönem yüzdeliği), uzunluk", 'ölçüt', 'Cemal', 'Ç174 / Ç176 kararı yalnız S1 tanımı için geçerli; Cemal sıkışması S4 olarak yeniden ölçülüyor (Ç183)', 'S4 tanımı ön kayıtla: küçük mum + BB yüzdelik <= 0,20 + |net| <= %3 + aşağı açılış payı <= %50 + >= 10 gün', "Bölge tanımı Cemal'in işaretlediği gerçek örneklerle mekanik doğrulanmadan (seçmeli / seçmemeli) ölçüme girmez", 'FENER grafiği 15 Kas; ana model ölçümü'),
    _ik_h('2026-11-15', 'Ç183 S4 tanımı (iv) (ana model iş tanımı)', "Uzunluk koşulu '(i)+(ii) >= 10 ardışık gün' 15 günlük mum ortalaması ve 20 günlük Bollinger ile yazıldı; bunlar bölgeden önceki düşüşü içerdiği için kısa (< 25 bar) sıkışmalar sağlanamıyor; Cemal'in FENER bölgesi (18 bar) kaçtı; Aralık bölgesi doğru dışlandı", 'ölçüt', 'alt ajan (FENER mekanik doğrulama)', "S4 sonucu 'uzun sıkışmalar' için geçerli; Cemal'in örneği ölçülmedi; karar Cemal'de", 'yeni ön kayıtla (iv) bölge içi ölçülerle (ör. bölge içi BB / mum) yeniden tanımlanabilir', "Tanım, Cemal'in işaretlediği örnekle ön kayıttan ÖNCE mekanik sınanır; sınama ön kayıtta değil tasarımda yapılmalıydı", 'SIKISMA_CEMAL_ON_KAYIT.md FENER bölümü'),
    _ik_h('2026-11-15', 'BOLGE_LISTESI_CEMAL.md 2. sürüm (ana model)', "Bölünme süzgeci |ln| > ln 1,5 BIST için gevşekti: MRGYO 29.01.2026 satırı 'en kötü 10'da -%46,8 ile kaldı, 10.02.2026'da tek günde -%32 (bedelli / bölünme); BIST ±%10 sınırı gereği tek günde > %11 değişim ancak sermaye işlemiyle olur", 'veri', 'alt ajan (Ç183)', "liste 3. sürümde düzeltildi (BIST'e özel > %11 süzgeci); ölçümler etkilenmedi", '3. sürüm gönderildi', "Pazara özgü süzgeç (BIST'te marj sınırı) K6 maddesine yazıldı", 'Ç183 teslimi HATA 2'),
    _ik_h('2026-11-15', 'BOLGE_LISTESI_S4.md gösterimi (ana model iş tanımı)', "Bölge 'karar günü - 15 bar' olarak yazıldı; kodun bölgesi aslında koşulun sağlandığı ilk günden son güne uzanıyor (CCOLA: liste 17 Eyl-7 Eki gösterdi, bölge 2-20 Ekim; Cemal'in kırmızı çizgileri bunun içindeydi). Cemal 'kod bulamıyor' sandı", 'iletişim', 'Cemal (CCOLA grafiği) + ana model kontrolü', 'tanım değil gösterim; S5 listesinde bölge ilk-son gün yazılacak', 'S5 iş tanımına yazıldı', 'Bölge, karar günü değil aralık olarak gösterilir', 'sohbet 15 Kas; ana model CCOLA ölçümü'),
    _ik_h('2026-11-15', 'Ç184 tasarım örnekleri (ana model)', "Cemal'in fotoğraflarından bölge tarihleri okunamıyor; ana model ENJSA bölgesini tahminle (10 Tem-14 Ağu) seçmeli örnek yaptı, Cemal sonradan 28 Tem-12 Eyl dedi ve 'görüyormuş gibi yapma' diye uyardı; tahmin tasarım örneğine girdi", 'süreç', 'Cemal', "tasarım 14 / 14 tuttu ama ENJSA örneği Cemal'in bölgesi değildi; Cemal'in bölgesi S5'e girmiyor (bant %23)", "Pine göstergesi: kodun bölgeleri Cemal'in grafiğinde boyanır, tarih tahmini biter; örnek bölgeler bundan sonra yalnız Cemal'in yazdığı tarihlerle alınır", "Fotoğraftan tarih çıkarsanmaz; görülen açıkça 'gördüğüm şu, tarih tahmin' diye yazılır", 'sohbet 15 Kas'),
    _ik_h('2026-11-15', 'Ç184 TASARIM tablosu / Pine (alt ajan)', "Tasarım tablosunda CCOLA için 'S5 2025-10-02' yazıldı; bu aralıktaki ilk S5 günü, karar günü değil (bölgenin karar günü 2025-09-02; 16 bar ara < 20 olduğu için aynı bölge); grafikte üçgen 2 Eylül'de çıkar", 'iletişim', 'alt ajan (Pine)', 'karar değişmez', 'PINE_NASIL ve .pine tablosunda yazılı', "'İlk S5 günü' ile 'karar günü' ayrı adlandırılır", 'Pine teslimi HATA'),
    _ik_h('2026-11-15', 'Ç184 S5 tasarımı', "FENER'de S5 31 Ekim'de başlıyor, Cemal'in bölgesi 14 Ekim'de: Bollinger (20) yüzdelik şartı ancak 31.10'da sağlanıyor; bölgenin ilk 13 günü kaçıyor. Tasarım kuralı 'aralıkta en az bir S5 günü' olduğu için TUTTU sayıldı; Cemal'in gözüyle örtüşme kısmi", 'ölçüt', 'alt ajan', "EMARE sonucu geçerli ama 'Cemal bölgesi' ile örtüşme kısmi; gösterge ile Cemal yargılayacak", "S6'da tasarım kuralı 'bölgenin en az yarısı S5' olabilir (Cemal kararı)", 'Tasarım sınaması örtüşme oranını da ölçmeli, yalnız var / yok değil', 'SIKISMA_OBEK teslimi HATA 3'),
    _ik_h('2026-11-15', "Ç184 karar kuralı (SIKISMA_CEMAL'den aynen)", "Hücre 'TERS' etiketi eş 1 ya da eş 2'den birinin üst ucu < 1 ise veriliyor; BIST DİP B1 eş 1 0,70 TERS, eş 2 1,12 (çelişkili); iki eş birlikte okunmalı", 'ölçüt', 'alt ajan', 'BIST bilgi hücresi; karar değişmez', 'yorum satırı; cetvel sürümünde düzeltilir', 'Birden çok kontrol grubunda etiket ancak ikisi aynı yöndeyse verilir', 'SIKISMA_OBEK teslimi HATA 5'),
    _ik_h('2026-11-15', 'Ç184 tasarım örnek kuralı', "Seçmemeli aralık (ENJSA 20.01-14.02) iki iş günü sonrasında (18.02) tek günlük YOL S5 çıktı; aralıkla sınırlı kural bunu görmedi; CCOLA'da 02.10 bölgesi ayrı olay değil, 02.09'dan süren 34 günlük bölgenin parçası", 'ölçüt', 'alt ajan', 'karar değişmez', 'S6 tasarımında aralık ± 5 gün tamponu ve bölge birleştirme kuralı yazılır', 'Örnek sınaması bölge sınırlarını tamponla sınar', 'SIKISMA_OBEK teslimi HATA 1-2'),
    _ik_h('2026-11-15', 'GELECEK_DUZELTME iş tanımı (ana model)', "İş tanımı kendi içinde çelişti: tablo 'döngü alt sınırı 399' derken bölüm 2 'eski çıktının alt kümesi / K24_YENIDEN ile birebir anlam' dedi; konum şartının tekilleştirme durumundan (gorulen / son_olay) önce mi sonra mı uygulanacağı yazılmamıştı. Ayrıca fi_k23 satır süzgeci tek başına BINBN bölge hedefini (konum 70 < 214) kıracaktı; evren taraması ile tek pencere hedef çağrısı ayrılmamıştı", 'süreç', 'alt ajan', 'karar yoktu; sayım 9 hücrede alt küme olmadı (1-157 yeni satır); hedef çağrıları gecmis=L ile eskiyle aynı kaldı', 'tablonun harfi uygulandı (döngü alt sınırı); fi_k23_parmak gecmis parametresi; rapor SAPMA 2-3', 'İş tanımında konum şartının durum makinesine (tekilleştirme) göre yeri açıkça yazılır; evren taraması ile hedef bölge çağrısı ayrı düşünülür', 'GELECEK_DUZELTME_RAPOR.md bölüm 7'),
    _ik_h('2026-11-15', 'Pine göstergesi teslimi (Ç184)', "TradingView ücretsiz (Basic) plan sınırı teslimde hesaba katılmadı: grafikte en çok 2 gösterge; Cemal'in grafiğinde 3 vardı, S5 'yükselt' uyarısıyla eklenemedi. Ana model ilk yanıtta Cemal'in söylediği '3' sınırını doğrulamadan yazdı (gerçek 2, ekran görüntüsü). Dosya Cemal'in bilgisayarında yanlış kodlamayla açılınca Türkçe karakterler bozuldu (AÃ‡IK-DÄ°P). Ekrandaki satır sarma hatası Cemal'in eski 'CEMAL TEKNIK' betiğinde, S5'te değil", 'iletişim', 'Cemal', 'karar yoktu; gösterge kullanımı gecikti', "PINE_NASIL 1b-1c: iki 'Cemal | BB + EMA' göstergesi kaldırılır, S5 eklenir (toplam 2); COL_S5_OBEK_ascii.pine (kod kısmı birebir, yalnız yorum / metin ASCII; sarmalı satır 0)", "Cemal'e giden araç teslimi hedef ortamın sınırlarıyla (plan, kodlama) birlikte yazılır; Cemal'in söylediği sayı ekran görüntüsüyle doğrulanır", 'sohbet 15 Kas, ekran görüntüleri'),
    _ik_h('2026-11-15', 'D9_YENIDEN.d9_durum (Ç181)', "250 temiz bardan kısa bir hissede rüzgâr günü varsa 'bant250' sütunu olmadığı için AttributeError ile düşüyor (AVR SHAW.L 210 bar tetikledi); Ç181 koşusunda AVR'de rüzgâr olmadığı için tetiklenmedi", 'hesap', 'alt ajan (D9_AVR)', 'Ç181 sonuçları değişmedi; D9_AVR.d9a_durum kopyasında eksik bant sütununa NaN yazılarak düzeltildi, sinyal aynı', 'D9_YENIDEN bir sonraki sürümünde aynı düzeltme (ön kayıt sha değişeceği için Mart 2027 ileri koşusundan önce, yeni sürüm olarak)', 'Kısa seride türetilmiş sütunların varlığı mekanik denetlenir; sentetik testte kısa + rüzgârlı hisse örneği bulunur', 'D9_AVR_RAPOR.md HATA H-a'),
    _ik_h('2026-11-15', 'T8_KALDIR_IS_TANIMI.md (ana model)', "İş tanımı kabuk heredoc'una tırnaksız yazıldığı için metindeki ters tırnaklı komutlar (python test_d9_yeniden.py, grep, python -c ast) dosya yazılırken ÇALIŞTI; §3 TESTLER bölümüne test çıktıları yapıştı, cümleler kesildi. Alt ajan amacı doğru anlayıp uyguladı", 'süreç', 'alt ajan (T8)', 'karar yoktu; iş değişmedi; §3 düzeltildi ve not düşüldü (ön kayıt commit sonrası; içerik değişikliği değil düzeltme)', 'Bölüm yeniden yazıldı; D9_AVR iş tanımında ters tırnaklar kaçışlıydı (etkilenmedi)', "İş tanımı dosyaları heredoc'a yalnız tırnaklı sınırlayıcıyla (<<'EOF') ya da Write ile yazılır; yazdıktan sonra dosya bir kez okunur", 'T8_KALDIR_RAPOR.md HATA H-a'),
    _ik_h('2026-11-15', 'Drive col_tarayici/COL_v1.py (üretim)', "Drive'daki COL_v1.py 20 Ekim 20:44 D12 sürümünde kalmış; repo (ve GitHub Actions günlük tarama) 21 Ekim'den beri D13 (col_dip2) ile çalışıyor. Colab'daki üretim zinciri ile Actions 25 gün ayrı tespit kuralıyla çalıştı; CLAUDE.md 'Drive aynası' kuralı D13 güncellemesinde uygulanmamış", 'süreç', 'ana model (Drive doğrulaması)', 'Colab bugun_liste / gun() D12 kutularıyla üretildi; Actions raporları D13; takip CSV dosyalarının asıl yeri repo olduğu için pozisyon kayıtları etkilenmedi, yalnız Colab ekranı eski kuralı gösterdi', 'T8 değişikliğiyle birlikte COL_v1.py ve takip.py Drive kopyaları HEAD sürümüne yüklenir (bayt doğrulaması, eski çöpe)', 'Üretim dosyası repoda değişince aynı görevde Drive kopyası güncellenir ve görev satırına yazılır; yeni oturum başında Drive / repo sha kıyası yapılır', 'Drive indirme sha256 vs git show (15 Kas)'),
    _ik_h('2026-11-15', 'COL_S5_OBEK.pine v1.1 (Ç184 göstergesi)', "Kutu sınırı sabit 15 bar (karar gününden geriye sayı); bant içindeki komşu küçük mumlar (önceki 1, sonraki 2; ENJSA) dışarıda kaldı; Cemal'in gözünde bölge aynı bant içindeki ardışık mumların tamamıdır", 'yanlış yorum', 'Cemal', "ölçüm kararı değişmedi (karar günü aynı); gösterilen bölge Cemal'in bölgesinden kısa, S6 işaretlemesi için yanıltıcı olurdu", 'v1.2: kutu banda göre geriye / ileriye genişler, bant dışı mumda kapanır, en çok 60 bar', "Bölge gösterimi mumlardan türetilir (bant), sabit pencere sayısından değil; S6 tasarım sınamasında örtüşme oranı bu sınırla ölçülür", 'sohbet 15 Kas, ENJSA ekran görüntüsü'),
]


# ---------------------------------------------------------------- 1b) ÖN UÇUŞ KONTROL LİSTESİ (hata defterinden türetildi)
# Cemal, 14 Kas 2026: "iz ararken bu hatalar önceden okunup göz önünde tutulsun, kod yazmaya öyle başlansın; bütün modeller için".
# Her madde IK_HATA'daki tekrarlayan bir örüntüden çıkar. Okumak yetmez: ön kayıt dosyasında her maddeye yazılı yanıt zorunludur
# (ik_kontrol_kapisi), yanıt yoksa ya da HAYIR ise ölçüm (kos) başlamaz.
IK_KONTROL: List[Dict[str, str]] = [
    {"kod": "K1", "ad": "kontrol grubu", "soru": "Eşler aynı giriş günü, aynı momentum x likidite hücresi, aynı giriş / çıkış geometrisi mi; taban rastgele olay sağlamasıyla (200 eş portföy) mi? Mekanik üstünlük (sinyal tanımının kendiliğinden ürettiği fark) dışlandı mı?", "hata": "22 kez (H005, H006, H026-H032, H055, H064, H100...)"},
    {"kod": "K2", "ad": "geleceğe bakma", "soru": "Her girdi alanının bilgi tarihi <= karar günü ve bu KODDA mekanik denetleniyor mu? Satır tarihi mi (sayfa / haber tarihi değil)? Etiket, evren listesi, sektör karar günündeki haliyle mi?", "hata": "12 kez (H003, H016, H034, H051, H130...)"},
    {"kod": "K3", "ad": "geçerli bar", "soru": "H>L ve V>0 olmayan bar sinyal ya da ölçü üretmiyor mu; hacim 0 gün fiyatı bayat sayılıyor mu; seans açıkken yarım bar atılıyor mu?", "hata": "2 kez aynı hata (H004, H037), H134, H141"},
    {"kod": "K4", "ad": "tekilleştirme", "soru": "Aynı hissede olay 60 günde bir mi; n bağımsız olay sayısı mı; aynı işlem bir kez mi sayılıyor; ortalama yanında medyan var mı?", "hata": "H006 (n 4-5 kat şişkin), H014"},
    {"kod": "K5", "ad": "giriş fiyatı", "soru": "Giriş = sinyalden (yayın saatinden) sonraki ilk işlem fiyatı mı (ertesi açılış), sinyal günü kapanışı değil mi?", "hata": "H005, 60 gün ufuk itirazı"},
    {"kod": "K6", "ad": "veri birimi", "soru": "Fiyat tek kipte mi (ekran fiyatı ya da düzeltilmiş, karışık değil); birim (lot / TL, peni / sterlin, 100x), bölünme marjı (12.03.2020 öncesi +-%20), bedelsiz denetlendi mi; yeni pazar birim denetiminden geçti mi?", "hata": "veri 34 satır (H007, H017, H060...)"},
    {"kod": "K7", "ad": "hayatta kalma", "soru": "Evren bugünün listesi mi? Batanlar / kottan çıkanlar yoksa raporda yazılı ve sonuç 'yukarı yanlı' okunuyor mu?", "hata": "8 kez (H008, H057, H142...)"},
    {"kod": "K8", "ad": "örneklem ve dönem", "soru": "n < 30 'örneklem yetersiz' ve olaylar tek tek listeli mi; iki alt dönem aynı yönde mi; çoklu karşılaştırma BH ile mi; küçük örneklemden 'bulgu' denmiyor mu?", "hata": "H010, Ç169 n 11, K1 / K2 n < 30"},
    {"kod": "K9", "ad": "ön kayıt", "soru": "Tanım + eşik sözlüğü + kod sha ön kayıtta; ön kayıt commit zamanı < koşu zamanı; sonuçtan sonra yalnız gösterim değişti, aksi SAPMA; eşik sonuca göre oynanmadı mı?", "hata": "H079, H097 (ön kayıt geç commit)"},
    {"kod": "K10", "ad": "ayrıştırma", "soru": "Ham kaynaktan rastgele >= 3 satır elle doğrulandı mı; haber türü (günlük / aylık / dönemsel), kurum etiketi (çok kurumlu haber), kenar kuşağı çöpü, güncelleme damgası, kurum adı hisse satırı dört ayrı denetim maddesi olarak kontrol edildi mi?", "hata": "5 kez tek günde (H128-H132, H136)"},
    {"kod": "K11", "ad": "yeniden üretim", "soru": "Raporlanan >= 2 hücre satır dosyasından bağımsız kodla yeniden üretildi mi; metindeki sıra / tarih / sayı ham kayıtla aynı mı?", "hata": "H136 (PEKGY 1. / 4.), H137 (blok filtresi)"},
    {"kod": "K12", "ad": "ifade", "soru": "Fiyat değişimi ile gerçekleşen kâr / zarar ayrı mı; aracı kurum akışı ile kurum pozisyonu ayrı mı; 'anlamlı / ters / iz / emare' sözü yalnız bu liste geçince mi; sayı ile yorum ayrı cümlede mi?", "hata": "yanlış yorum 16 satır (H133, H135...)"},
    {"kod": "K13", "ad": "süreç", "soru": "Çakışma kapısı korundu mu; kod değiştiyse 'çalışma zamanını yeniden başlat' yazıldı mı; e-posta / anahtar sızıntı taraması yapıldı mı; kota / ücret / yeni dal Cemal onayıyla mı; yasak defter dosyalarına dokunulmadı mı?", "hata": "süreç 21 satır (H019, H021, H143...)"},
    {"kod": "K14", "ad": "boyut (gerçek para)", "soru": "Öneri işinde boyut tavanı, zarardaki isme ekleme yasağı, olay bazlı çıkış ve 2x kuralı alımdan önce yazılı mı; taban oranlar (10x ~%1) yazılı mı?", "hata": "karar-boyut 6 satır (H012, H013)"},
]
IK_KONTROL_YANIT = ("EVET", "UYGULANMAZ")   # HAYIR ya da boş = kapı kapalı


# ---------------------------------------------------------------- 1c) İLERİ TEST DEFTERİ (Cemal, 14 Kas 2026: "yanlış dediğimiz kural sonra doğru çıkabilir; nasıl emin olacağız?")
# Emin olmanın tek yolu ileri testtir: iddia sabit eşikle ve veri kesiğiyle kaydedilir, henüz var olmayan veride (sonraki dönem) aynı
# komutla yeniden ölçülür. Karar üç etiket alır: İZ DEĞİL (güç yeterli, tutmadı) / ÖLÇÜLEMEDİ (n ya da güç yetersiz; yeniden açılır) /
# İZ. Her 'iz değil' ya da 'emare / aday' iddiası buraya bir satır olur; sonraki test tarihi ve koşulu önceden yazılır; sonuç geldiğinde
# satır silinmez, 'sonuc' alanına yazılır (tutuyor / tutmuyor / yine ölçülemedi). Üç art arda ileri testte aynı yön = kesin.
def _ik_i(kod, iddia, karar, guc, esik, kesik, sonraki, sonuc=""):
    return {"kod": kod, "iddia": iddia, "karar": karar, "guc": guc, "esik": esik, "kesik": kesik, "sonraki": sonraki, "sonuc": sonuc}


IK_ILERI_KARAR = ("İZ DEĞİL", "ÖLÇÜLEMEDİ", "İZ", "EMARE", "ADAY", "BİLGİ")
IK_ILERI: List[Dict[str, str]] = [
    _ik_i("Ç100-Ç151 (K58)", "FI_OLCUT 60 gün cetveli n < 1.000 çalışmalarda küçük etkiyi (+%2) göremiyor; eski 'İZ DEĞİL' kararlarının çoğu aslında ölçülemedi", "ÖLÇÜLEMEDİ", "güç simülasyonu: δ +%2, n <= 300 -> güç en çok %11", "FI_OLCUT dört şart (sabit)", "veri 31.08.2026", "portföy cetveli v2 (plasebo 0/200) ile n >= 1.000 olacak şekilde aile bazında yeniden koşu; 2027 ilk çeyrek, kriz penceresi kapanınca", ""),
    _ik_i("Ç168-Ç169", "Çökmüş hissede art arda tavana katılmak eşlerden kötü; hacimli tavan piyango profili (büyük sıçrama 2,5 kat, tipik -%15)", "İZ DEĞİL", "n 201 geniş hücre; H1 ana n 11 ölçülemedi", "TAVAN_SERISI eşikleri (tavan >= %9,5; hacim >= 10x 20g medyan)", "olaylar 2016-26, kriz öncesi", "kriz sonrası 26 hisse (Eyl-Kas 2026) 60 / 120 gün sonucu Mart 2027'de aynı komutla (`python TAVAN_SERISI.py kos`); ertesi gün tavan %56-82 vs geçmiş %35-40 farkı o zaman sınanır", ""),
    _ik_i("Ç170", "Çöküş sonrası KAP geri alım bildirimi dönüşü önceden gösteriyor (17 vs 47 hisse, x1,52 vs x1,26)", "EMARE", "tek olay, 64 hisse, q 0,003", "GENIS_KESIT Spearman + permütasyon, BH q 0,10", "31.10.2026 kesit, 13.11 sonuç", "2018 (Ağu-Eyl) ve 2020 (Mar) BIST çöküşlerinde aynı tanım + ABD 2020 / 2022; ön kayıtla; tutarsa 2027'de yeni çöküşte ileri test", ""),
    _ik_i("Ç171-Ç172", "BofA (ve HSBC) AKD alım listesini takip etmek eşlerden farksız; BofA kodu müşteri akışı", "İZ DEĞİL", "n 1.789 / 618 (güç yeterli)", "tutma dönemi eşli fark, FI_OLCUT dört şart", "17.04.2023-31.08.2026", "Haziran 2027: 01.09.2026-28.02.2027 listeleriyle aynı komut (`python BOFA_IZI.py kos --sapma`); K1 pay >= %20 ve K2 maliyete yakın giriş o zaman n >= 30 olursa karar alır", ""),
    _ik_i("Ç173", "Dipte (-%80, dip tutuyor, dipten <= 1,5x) BofA alımıyla girmek", "ÖLÇÜLEMEDİ", "kriz öncesi olay 0; kriz sonrası 1 (HDFGS)", "KURULUM D1-D3 + BofA alım ilk 5, G1 giriş", "BofA arşivi 2023-26", "Mart 2027: HDFGS, SKBNK ve kriz sonrası yeni kurulum olayları 60 / 120 gün; n >= 30 olmazsa yine ÖLÇÜLEMEDİ yazılır, 'yol yok' denmez", ""),
    _ik_i("Ç173", "-%80 dip kurulumu tek başına: ABD 2023 tuttu (+%24,8), 2024-26 sıra tutmadı; piyango profili (P+%100 ve P-%50 ikisi de ~2 kat)", "İZ DEĞİL", "ABD n 81 / 146; Avrupa n 3 / 8 ölçülemedi", "FI_OLCUT dört şart + 250 gün olasılık", "veri 31.08.2026", "2027 ikinci yarı: 2026-09..2027-06 ABD kurulumları; batanlar eklenerek (Tiingo kararı Cemal'de) hayatta kalma düzeltmesi", ""),
    _ik_i("Ç166-Ç167", "Sessiz bölge / çöl şekli algoritması Cemal'in gözüyle uyuşmuyor (kör test işaret yok; G5 1/29)", "ÖLÇÜLEMEDİ", "kör test yanıtı yok; etiket 29", "KOR_TEST v1.1 ortak log ölçek", "—", "Cemal 40 grafiği işaretlerse `python KOR_TEST.py olc --cevap`; işaretlemezse hat kapalı kalır (Cemal kararı)", ""),
    _ik_i('Ç174', 'Sıkışma sonrası hissenin olağan ölçüsünde büyük gün gelir (B1 >= 3 x ATR250); yönsüz stoplu kırılım kazandırır', 'İZ DEĞİL', 'n 1.266-9.540 (güç yeterli); eğilim ters', 'S1 x B1 KAT alt95 > 1 (ABD + AVR); (C) FI_OLCUT dört şart; SY_ESIK sabit', '31.08.2026', "Mart 2027: kesik ileri alınıp 2026-09..2027-02 ayrı hücre, aynı komut (python SIKISMA_YENIDEN.py kos); ileri pencerede bölünme dışlaması kaldırılmış sürümle (Ç177 HATA 2) de koşulur; ek: NATR14 / ATR250 oranında eşleşmiş kontrol (Ç175 önerisi) ayrı ön kayıtla; batanlar dahil ABD evreni (Tiingo kararı Cemal'de)", ''),
    _ik_i('Ç124', 'INTEM tipi kısa ufuk kutu çıkışı (+%8 önce, oynaklık eşli rastgele) sıkışma ailesindeki tek EMARE', 'EMARE', 'son dönem n 26-51', 'Ç124 eşikleri sabit', '31.08.2026', '2026-09 sonrası yeni bölgeler, kriz penceresi kapanınca (Mart 2027+); yılda ABD ~25-50 olay: üç yıl birikim; ölçülemez kalırsa kapanır', "2026-11-14 ileri test 1 (görülmemiş hisse, zaman ileri testi değil; Ç180): ABD k34 1.465 hisse, ORTAK CETVEL L20 ABD 2023 n 26 -%3,2, 2024-26 n 42 -%7,5 [-17,8; +2,9] -> ÖLÇÜLEMEDİ; kendi ölçüsü +2,7 puan [-6,8; +12,2] (eski +11,2): yön zayıfladı, kanıt yok"),
    _ik_i('Ç96 / K24', 'İki evre çöl kuralı (üretimdeki tek çöl sinyali): ABD 2023 +%3,1, 2024-26 -%0,5 çelişkili', 'ÖLÇÜLEMEDİ', 'FI n < 1.000 (K58 güçsüz)', 'K24 tanımı sabit; PV2 + olasılık tablosu', '31.08.2026', "Yeniden koşu (Ç175 öneri 2): ABD batanlar dahil + AVR 2016-26/08, beklenen n ABD ~6.900; ön kayıtla; Cemal 'koş' deyince", ''),
    _ik_i('Ç37', "D9 uzun çöl (>= 1 yıl) + sektör rüzgârı; 'test sürüyor' diye hiç kapanmadı, üretim ekranında (T8)", 'ÖLÇÜLEMEDİ', 'eşsiz %56 vs piyasa %44 (2023-26), n bilinmiyor', 'aynı gün aynı sektör aynı momentum eşli + PV2', '31.08.2026', 'Yeniden koşu (Ç175 öneri 3): ABD sektör listesiyle; AVR sektör yok; ölçülemezse T8 üretimden kaldırılır (Cemal kararı)', ''),
    _ik_i('Ç178 / K24', 'K24 iki evre çöl eşlerden ayrışmıyor; büyük hareketi iki yönde artırıyor (piyango)', 'ÖLÇÜLEMEDİ', 'ABD 2024-26 n 2.869 TUTMADI; ABD 2023 n 941 güç %52; AVR n 100 / 286 güç %29', 'ORTAK_CETVEL v1.0 (4763c458) + FI_K24 sabit, SAPMA-1', '31.08.2026', 'Mart 2027: kriz sonrası 2026-09..2027-02 ayrı hücre, aynı komut (python K24_YENIDEN.py kos, yeni ön kayıt); ABD 2023 güç için 2027 verisiyle n >= 1.000; PİYANGO profili oynaklık eşlemeli kontrolle ayrı ön kayıt', ''),
    _ik_i('Ç179', 'Düzgün dip + çöl birlikteliği (C) yalnız dipten (A) ya da yalnız çölden (B) ayrılır', 'ÖLÇÜLEMEDİ', 'ABD C n250 381 / 723 (< 1.000); AVR C n250 11 / 33', 'ORTAK_CETVEL v1.0; dip16 / dip17 / K24 parametreleri sabit', '31.08.2026', 'Mart 2027: aynı komut (python DIP_COL_AYRIM.py kos), yalnız veri kesiği ileri; koşul ABD C n250 >= 1.000 bir hücrede ya da AVR C n250 >= 30 iki hücrede', ''),
    _ik_i('Ç181a / Ç37', 'D9 uzun çöl (6-12 ay dar bant, dipte) eşlerden iyi değil; sakin hisse seçer', 'İZ DEĞİL', 'ABD n 2.399 / 4.556, AVR 1.102 / 2.102 (güç yeterli); 4 hücre TUTMADI', 'ORTAK_CETVEL v1.0 + COL_v1 D9 sabit', '31.08.2026', 'Mart 2027: kriz sonrası ayrı hücre, aynı komut (python D9_YENIDEN.py kos); üç ileri testte aynı yön = kesin', ''),
    _ik_i('Ç181b / T8', 'D9 + sektör rüzgârı (üretim T8 listesi)', 'ÖLÇÜLEMEDİ', 'ABD 2023 n 870 güç %52; 2024-26 n 1.556 TUTMADI; AVR sektör yok', 'ORTAK_CETVEL v1.0 + COL_v1 D9b sabit', '31.08.2026', "Mart 2027 ABD n >= 1.000; AVR sektör listesi derlenirse (ücretsiz, STOXX / FTSE sektör; Cemal onayı) AVR'de koşulur", ''),
    _ik_i('Ç181c', "Yalnız sektör rüzgârı (sepet - piyasa >= eşik, sepet > 0): ABD'de eşli fark +%2,8 / +%3,6, +%100 katı 1,35-1,39, -%50 katı ~1,0; yalnız portföy şartı düştü", 'EMARE', 'ABD 2024-26 n 5.873 dört şartın üçü tuttu (alt uç +1,9); ABD 2023 n 2.001 alt uç -0,3; AVR yok; orta + güçlü tercil ABD 2024-26 TUTAR (bilgi)', 'ORTAK_CETVEL v1.0; rüzgâr eşiği COL_v1 RUZ_ESIK / RUZ_MUTLAK sabit; tercil sınırları 0,1402 / 0,2222 sabit', '31.08.2026', "(1) AVR sektör listesi derlenip AVR 2023 / 2024-26 aynı komutla (öncelikli, ücretsiz veri); (2) Mart 2027 kriz sonrası ABD; (3) literatür kıyası: sektör momentumu bilinen etki (Moskowitz-Grinblatt 1999), yeni iz sayılmaz, 'bilinen etki' olarak etiketlenir; cetvel değişmez", '2026-11-15 ileri test 1 (Ç185, AVR sektör listesiyle, aynı cetvel ve eşik): AVR 2023 n 125 -%1,7 [-5,9], AVR 2024-26 n 447 +%0,9 [-0,9]; güç %29 / %52 -> AVR ÖLÇÜLEMEDİ, EMARE değişmedi; sonraki: Mart 2027 kriz sonrası ABD + AVR aynı komut (python D9_YENIDEN.py kos; python D9_AVR.py kos)'),
    _ik_i('Ç182 P1', 'Büyük mumdan önceki profil = son mum büyük (>= 1,22 x ATR250) + 250 gün tepesine yakın + 40 günde küçük mum dizisi yok; 20 günde büyük mum olasılığı eşlerin 1,3-1,7 katı (oynaklık tahmini, yön yok, 60 gün getiri yok)', 'EMARE', 'ABD n 3.145 / 16.258, AVR 838 / 4.679; dört hücre alt uç > 1; BH q 0,001', 'P1 eşikleri sabit (ters_kurallar.json sha); eşler σ250 ondalığı', '31.08.2026', "(1) anlık oynaklık (ATR10 / ATR250) eşlemeli kontrolle yeniden (bilinen kümelenmeden fark kalıyor mu; ayrı ön kayıt); (2) Mart 2027 kriz sonrası ileri test aynı komut (python TERS_PARMAK.py dogrula); (3) Cemal'in kör set işareti (TERS_ORNEK_40) gelirse göz uyumu", ''),
    _ik_i('Ç182 H1', 'Çok günlü büyük hareket (BH2) öncesi profil = 5 gün bandı geniş + 120 günde sert düşüş + 250 gün dibine yakın: ABD KAT 3,2 / 1,7', 'EMARE', "ABD n 1.473 / 4.866; AVR n 253 / 1.5 aralık 1'i kapsıyor; BH q 0,52", 'H1 eşikleri sabit', '31.08.2026', 'Mart 2027 aynı komut; AVR n büyüyünce; piyango ailesiyle (Ç173, Ç178) birlikte okunur', ''),
    _ik_i('Ç183 S4', 'Cemal tanımlı sıkışma (küçük mum + dar BB + yatay + >= 10 gün) büyük hareketin habercisi mi', 'ÖLÇÜLEMEDİ', 'ABD n 843 / 787, AVR 513 / 479 (< 1.000); B1 KAT ~1, BH2 < 1 nokta', 'SC_ESIK mühür 2533e1f0 sabit', '31.08.2026', 'Mart 2027 kriz sonrası dönem eklenerek aynı komut (python SIKISMA_CEMAL.py kos); hücre başına n >= 1.000 olunca karar; (iv) değişirse YENİ ön kayıt, eski satır kalır', ''),
    _ik_i('Ç184 S5_DİP', "Cemal'in öbek sıkışması, dip sınıfı: 20 günde büyük gün (>= 3 x ATR250) olasılığı eşlerin 1,14-1,17 katı (ABD iki dönem), Avrupa'da yok; getiri / yön yok", 'EMARE', 'ABD n 579 / 649 (< 1.000); AVR n 292 / 389 ÖLÇÜLEMEDİ', 'SIKISMA_OBEK mühür de384bbd sabit; eşikler p 15, k_m 0,75, bant 8/6, bb 0,20', '31.08.2026', "(1) Cemal Pine göstergesiyle boyalı bölgeleri yargılar, 'yanlış' dediği hisse + tarihler toplanır (tanım değişirse S6, yeni ön kayıt); (2) Mart 2027 kriz sonrası dönem aynı komut (python SIKISMA_OBEK.py kos); (3) ABD n >= 1.000 olunca karar; yön / getiri için ayrı iddia yok", ''),
]


def ik_kontrol_metni(hedef: str = "onkayit") -> str:
    """Kontrol listesi metni. hedef='onkayit': ön kayıt dosyasına yapıştırılacak doldurulacak tablo;
    'istanimi': alt ajan iş tanımına girecek kısa liste; 'defter': indeks için."""
    if hedef == "onkayit":
        sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt; HAYIR ya da boş = kos çalışmaz)", "",
               "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
        sat += [f"| {k['kod']} | {k['ad']} | | |" for k in IK_KONTROL]
        return "\n".join(sat)
    if hedef == "istanimi":
        sat = ["ÖN UÇUŞ KONTROLÜ (zorunlu; hata defterinden): kod yazmaya başlamadan önce oku, ön kayıt dosyasına KONTROL LİSTESİ tablosunu "
               "(`python IZ_KARNE.py kontrol`) doldurarak koy, raporunda 'HATA' başlığıyla bulduğun her hatayı ayrı listele."]
        sat += [f"- {k['kod']} {k['ad']}: {k['soru']} [geçmiş: {k['hata']}]" for k in IK_KONTROL]
        return "\n".join(sat)
    sat = ["| Kod | Madde | Soru | Geçmişte kaç kez |", "|---|---|---|---|"]
    sat += [f"| {k['kod']} | {k['ad']} | {k['soru']} | {k['hata']} |" for k in IK_KONTROL]
    return "\n".join(sat)


def ik_kontrol_kapisi(onkayit_yolu: str, dur: bool = True) -> Dict[str, Any]:
    """Ön kayıt dosyasındaki KONTROL LİSTESİ tablosunu okur. Her IK_KONTROL kodu için yanıt EVET ya da UYGULANMAZ ve
    en az 8 karakter kanıt olmalı. Eksik / HAYIR varsa dur=True ile RuntimeError (ölçüm başlamaz)."""
    if not os.path.exists(onkayit_yolu):
        raise RuntimeError(f"kontrol kapısı: ön kayıt yok: {onkayit_yolu}")
    metin = open(onkayit_yolu, encoding="utf-8").read()
    yanit: Dict[str, Dict[str, str]] = {}
    for m in re.finditer(r"^\|\s*(K\d{1,2})\s*\|[^|]*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*$", metin, flags=re.M):
        yanit[m.group(1)] = {"yanit": m.group(2).strip().upper(), "kanit": m.group(3).strip()}
    eksik, hayir, kanitsiz = [], [], []
    for k in IK_KONTROL:
        y = yanit.get(k["kod"])
        if y is None or not y["yanit"]:
            eksik.append(k["kod"])
        elif y["yanit"] not in IK_KONTROL_YANIT:
            hayir.append(f"{k['kod']}={y['yanit']}")
        elif len(y["kanit"]) < 8:
            kanitsiz.append(k["kod"])
    sonuc = {"gecti": not (eksik or hayir or kanitsiz), "eksik": eksik, "hayir": hayir, "kanitsiz": kanitsiz,
             "n": len(IK_KONTROL), "yanit": yanit}
    if dur and not sonuc["gecti"]:
        raise RuntimeError("kontrol kapısı KAPALI: " + "; ".join(
            x for x in (f"eksik {eksik}" if eksik else "", f"HAYIR / geçersiz {hayir}" if hayir else "",
                        f"kanıtsız {kanitsiz}" if kanitsiz else "") if x) + f" ({onkayit_yolu})")
    return sonuc


# ---------------------------------------------------------------- 2) VERİ ve TABAN
def _ik_fi():
    import FON_IZI as F   # kütüphane olarak; FON_IZI kendi çakışma kapısını taşır
    return F


def ik_veri(ay: IKAyar, pazar: str) -> Dict[str, pd.DataFrame]:
    F = _ik_fi()
    A = F.FIAyar(kap=ay.kap)
    return F.fi_k1_veri(ay.veri[pazar], pazar, A)


def ik_taban(ay: IKAyar, pazar: str, V: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Taban: her hissenin her 5. işlem günü, aynı giriş/sonuç mekaniği + eşleşme hücresi. Önbellek: onbellek/taban_<pazar>.pkl
    (veri dosyasının boyutu ve tarihi anahtar; veri değişirse yeniden hesaplanır)."""
    F = _ik_fi()
    os.makedirs(ay.onbellek, exist_ok=True)
    st = os.stat(ay.veri[pazar])
    # denetim 24 Eki: anahtar yalnız dosya boyu/tarihiydi; fi_duzelt / sonuç / hücre kodu ya da KAP bedelsiz kaydı değişince eski
    # taban kullanılıyordu. Kodun ve düzeltilmiş verinin parmak izi eklendi.
    imza = hashlib.md5((inspect.getsource(F.fi_duzelt) + inspect.getsource(F.fi_piyasa_sicrama) + inspect.getsource(F.fi_k10_sonuc)
                        + inspect.getsource(F._fi_k10_hucre) + inspect.getsource(F.fi_k10_taban)
                        + str(sorted((s, len(d), round(float(d.Close.sum()), 4)) for s, d in V.items()))).encode()).hexdigest()[:12]
    anahtar = f"{st.st_size}_{int(st.st_mtime)}_{imza}"
    yol = os.path.join(ay.onbellek, f"taban_{pazar}.pkl")
    if os.path.exists(yol):
        try:
            k = pd.read_pickle(yol)
            if k.attrs.get("anahtar") == anahtar:
                return k
        except Exception as ex:
            iklog.warning("taban önbelleği okunamadı (%s), yeniden hesaplanıyor: %s", yol, ex)
    B = F.fi_k10_taban(V, "2016-01-01", "2026-12-31").dropna(subset=["giris"]).reset_index(drop=True)
    B["hucre"] = F._fi_k10_hucre(B, B)
    B.attrs["anahtar"] = anahtar
    B.to_pickle(yol)
    iklog.info("taban %s: %d gün", pazar, len(B))
    return B


# ---------------------------------------------------------------- 3) SİNYALLER (her biri -> DataFrame[sembol, gun])
def _ik_panel(V: Dict[str, pd.DataFrame], kol: str) -> pd.DataFrame:
    # denetim 24 Eki: hisselerin yarısından azının barı olan ince gün (bayram arifesi 9 Nis 2024: 541'in 215'i) shift/rolling
    # zincirini öteki hisselerde ~20 gün NaN yapıyordu; o gün tablodan çıkarılır.
    P = pd.DataFrame({s: d[kol] for s, d in V.items()}).sort_index()
    return P.loc[P.notna().sum(axis=1) >= 0.5 * P.ffill().notna().sum(axis=1)]


def _ik_gecerli(V) -> pd.DataFrame:
    H, L, Vo = _ik_panel(V, "High"), _ik_panel(V, "Low"), _ik_panel(V, "Volume")
    return (H > L) & (Vo > 0)


def _ik_olay(M: pd.DataFrame) -> pd.DataFrame:
    s = M.stack()
    s = s[s.astype(bool)]
    return pd.DataFrame({"sembol": s.index.get_level_values(1), "gun": s.index.get_level_values(0)})


def ik_s_tavan(ay, pazar, V):
    C = _ik_panel(V, "Close"); r = C / C.shift(1) - 1
    return _ik_olay((r >= 0.09) & _ik_gecerli(V))


def ik_s_taban(ay, pazar, V):
    C = _ik_panel(V, "Close"); r = C / C.shift(1) - 1
    return _ik_olay((r <= -0.05) & _ik_gecerli(V))


def _ik_hacim_dus(V, kat, esik, pencere):
    C = _ik_panel(V, "Close"); Vo = _ik_panel(V, "Volume"); r = C / C.shift(1) - 1
    med = Vo.shift(1).rolling(pencere, min_periods=int(pencere * 0.8)).median()
    return (Vo >= kat * med) & (med > 0) & (r <= esik) & _ik_gecerli(V), C


def ik_s_hacim_dus(ay, pazar, V):
    M, _ = _ik_hacim_dus(V, 3.0, -0.05, 60)
    return _ik_olay(M)


def ik_s_hacim_dus_20(ay, pazar, V):
    M, C = _ik_hacim_dus(V, 3.0, -0.05, 60)
    return _ik_olay(M & (C.shift(1) / C.shift(21) - 1 <= -0.20))


def ik_s_blok_taban(ay, pazar, V):
    M, _ = _ik_hacim_dus(V, 20.0, -0.095, 20)
    return _ik_olay(M)


def ik_s_geride_hacim(ay, pazar, V):
    """A12: her ayın son işlem günü, 250 gün getirisi en düşük %20 VE hacim artışı (son 250 gün medyanı / önceki 250 gün
    medyanı) en yüksek %20 (pazar içi kesit)."""
    C = _ik_panel(V, "Close"); Vo = _ik_panel(V, "Volume")
    r250 = C / C.shift(250) - 1
    h1 = Vo.rolling(250, min_periods=200).median(); h0 = h1.shift(250)
    hk = h1 / h0.where(h0 > 0)
    ay_sonu = C.index.to_series().groupby(C.index.to_period("M")).max().values
    R = r250.loc[ay_sonu]; K = hk.loc[ay_sonu]
    M = (R.rank(axis=1, pct=True) <= 0.2) & (K.rank(axis=1, pct=True) >= 0.8) & R.notna() & K.notna()
    return _ik_olay(M)


def ik_s_hacimli_kirilim(ay, pazar, V):
    """Gün +%5 üstü kapanış, kapanış önceki 20 günün en yüksek kapanışının üstünde, hacim >= 3x önceki 60 gün medyanı."""
    C = _ik_panel(V, "Close"); Vo = _ik_panel(V, "Volume"); r = C / C.shift(1) - 1
    med = Vo.shift(1).rolling(60, min_periods=48).median()
    return _ik_olay((r >= 0.05) & (C > C.shift(1).rolling(20).max()) & (Vo >= 3 * med) & (med > 0) & _ik_gecerli(V))


def _ik_dosya(ay, yol) -> pd.DataFrame:
    y = os.path.join(ay.kok, "arastirma_cikti", yol)
    if not os.path.exists(y):
        raise FileNotFoundError(y)
    return pd.read_csv(y, low_memory=False)


def _ik_pazar_suz(D: pd.DataFrame, pazar: str, tarih: str, kol_sembol: str = "sembol") -> pd.DataFrame:
    if "pazar" in D:
        D = D[D.pazar == pazar]
    elif pazar != "BIST":
        return pd.DataFrame(columns=["sembol", "gun"])
    return pd.DataFrame({"sembol": D[kol_sembol].values, "gun": pd.to_datetime(D[tarih]).values})


def ik_s_doji_kutu(ay, pazar, V):
    D = _ik_dosya(ay, "doji_kutu/doji_kutu_kutular.csv.gz")
    # A13 tanımı: >=3 dojili kutu (grup A) ilk görüldüğü gün, kutu önceki 250 günün alt %35'inde. 'kirilim' sütunu ileriye
    # bakar (kutu ufuk içinde kırıldı mı) -> seçimde KULLANILMAZ (v1.0 ilk koşuda kullanılmıştı, sonradan bilgi, düzeltildi).
    return _ik_pazar_suz(D[(D.grup == "A") & (D.dip <= 0.35)], pazar, "tarih")


def ik_s_obek(ay, pazar, V):
    D = _ik_dosya(ay, "col_kazanc/col_kazanc_obekler.csv.gz")
    return _ik_pazar_suz(D[D.kaynak == "obek"], pazar, "sinyal")


def ik_s_d13(ay, pazar, V):
    D = _ik_dosya(ay, "col_tespit/col_tespit_sinyal.csv.gz")
    D = D[(D.N == 120) & (D.bar >= 15) & (D.inis >= 10) & (D.parabol.astype(bool)) & (D.obek >= 2)]
    # denetim 24 Eki: dosyada 'pazar' sütunu yok, ABD sembolleri '.US' ekli; eskiden ABD olayları hiç puanlanmıyordu.
    us = D.sembol.astype(str).str.endswith(".US")
    D = D[us] if pazar == "ABD" else D[~us]
    return pd.DataFrame({"sembol": D.sembol.astype(str).str.replace(r"\.US$", "", regex=True).values, "gun": pd.to_datetime(D.sinyal).values})


def ik_s_d12_atilim(ay, pazar, V):
    D = _ik_dosya(ay, "col_dip/col_dip_islemler.csv.gz")
    return _ik_pazar_suz(D[D.grup == "dip"], pazar, "atilim")


def ik_s_mum_sukun(ay, pazar, V):
    D = _ik_dosya(ay, "mum_sukun/mum_sukun_olaylar.csv.gz")
    return _ik_pazar_suz(D[(D.k == 3) & (D.olcu == "govde") & (D.varyant == "p02")], pazar, "tarih")


def ik_s_zemin(ay, pazar, V):
    D = _ik_dosya(ay, "mum_sukun/zemin_olaylar.csv.gz")
    return _ik_pazar_suz(D[(D.k == 5) & (D.varyant == "z_siki")], pazar, "tarih")


def ik_s_fon_iz_b(ay, pazar, V):
    D = _ik_dosya(ay, "fon_izi/fon_izi_olaylar.csv.gz")
    return _ik_pazar_suz(D[D.B_A_verim.astype(bool)], pazar, "tarih")


def ik_s_z0(ay, pazar, V):
    return _ik_pazar_suz(_ik_dosya(ay, "fon_izi/fon_hacim_olaylar.csv.gz"), pazar, "tarih")


def ik_s_z0_kuru(ay, pazar, V):
    D = _ik_dosya(ay, "fon_izi/fon_hacim_olaylar.csv.gz")
    return _ik_pazar_suz(D[D.hk <= 0.6], pazar, "tarih")


def ik_s_k13(ay, pazar, V):
    D = _ik_dosya(ay, "fon_izi/k14_olaylar.csv.gz")
    return _ik_pazar_suz(D[(D.asama == "kutu") & (D.tur == "olay")], pazar, "bilgi")


def _ik_k10(ay, pazar, kol):
    if pazar != "BIST":
        return pd.DataFrame(columns=["sembol", "gun"])
    D = _ik_dosya(ay, "fon_izi/k10_olaylar.csv.gz")
    D = D[D[kol].fillna(False).astype(bool)]
    # bilgi günü = giriş gününden önceki işlem günü (giriş = yayından sonraki ilk açılış)
    g = pd.to_datetime(D.giris) - pd.offsets.BDay(1)
    return pd.DataFrame({"sembol": D.kod.values, "gun": g.values})


def ik_s_fon_giris(ay, pazar, V):
    return _ik_k10(ay, pazar, "tur_giris")


def ik_s_fon_yogun5(ay, pazar, V):
    return _ik_k10(ay, pazar, "yogun5")


_IK_KAP_CACHE: Dict[str, pd.DataFrame] = {}


def ik_kap(ay: IKAyar) -> pd.DataFrame:
    """KAP özeti (tarih, saat, sembol, tur, konu_id). Bilgi günü: 18:00 sonrası bildirim ertesi iş gününe sayılır."""
    if ay.kap in _IK_KAP_CACHE:
        return _IK_KAP_CACHE[ay.kap]
    y = ay.kap
    if os.path.isdir(y):
        tum = os.path.join(y, "kap_ozet_tum.csv.gz")
        dosyalar = [tum] if os.path.exists(tum) else sorted(os.path.join(y, f) for f in os.listdir(y)
                                                            if f.startswith("kap_20") and f.endswith(".csv.gz"))
    else:
        dosyalar = [y]
    if not dosyalar:
        raise FileNotFoundError(f"KAP özeti yok: {y}")
    K = pd.concat([pd.read_csv(f, usecols=["tarih", "saat", "sembol", "tur", "konu_id"]) for f in dosyalar], ignore_index=True)
    K = K.drop_duplicates()
    t = pd.to_datetime(K.tarih)
    gec = K.saat.astype(str).str[:2].apply(lambda x: int(x) if x.isdigit() else 0) >= 18
    K["gun"] = np.where(gec, t + pd.offsets.BDay(1), t)
    K["gun"] = pd.to_datetime(K.gun)
    _IK_KAP_CACHE[ay.kap] = K
    return K


def _ik_kap_sec(ay, pazar, V, maske: Callable[[pd.DataFrame], pd.Series]) -> pd.DataFrame:
    if pazar != "BIST":
        return pd.DataFrame(columns=["sembol", "gun"])
    K = ik_kap(ay); K = K[maske(K) & K.sembol.isin(list(V))]
    return pd.DataFrame({"sembol": K.sembol.values, "gun": K.gun.values})


def _ik_kap_kos(ay, pazar, V, maske, kos_min=None, kos_max=None, gun_min=None):
    O = _ik_kap_sec(ay, pazar, V, maske)
    if not len(O):
        return O
    C = _ik_panel(V, "Close"); r20 = C / C.shift(20) - 1; rg = C / C.shift(1) - 1
    idx = C.index
    pos = idx.searchsorted(pd.DatetimeIndex(O.gun), side="right") - 1          # bilgi günü ya da öncesindeki son işlem günü
    ok = pos >= 0
    O = O[ok].copy(); pos = pos[ok]
    O["gun"] = idx[pos]
    k = np.array([r20.iat[p, r20.columns.get_loc(s)] if s in r20.columns else np.nan for p, s in zip(pos, O.sembol)])
    g = np.array([rg.iat[p, rg.columns.get_loc(s)] if s in rg.columns else np.nan for p, s in zip(pos, O.sembol)])
    m = np.ones(len(O), bool)
    if kos_min is not None:
        m &= k >= kos_min
    if kos_max is not None:
        m &= k < kos_max
    if gun_min is not None:
        m &= g <= gun_min
    return O[m]


def ik_s_kap_bedelsiz(ay, pazar, V):
    return _ik_kap_sec(ay, pazar, V, lambda K: K.tur == "BEDELSIZ")


def ik_s_kap_geri_alim(ay, pazar, V):
    return _ik_kap_sec(ay, pazar, V, lambda K: K.tur == "GERI_ALIM")


def ik_s_kap_geri_alim_kosmamis(ay, pazar, V):
    return _ik_kap_kos(ay, pazar, V, lambda K: K.tur == "GERI_ALIM", kos_max=0.10)


def ik_s_kap_sozlesme_kosmus(ay, pazar, V):
    return _ik_kap_kos(ay, pazar, V, lambda K: K.tur == "SOZLESME", kos_min=0.25)


def ik_s_kap_soylenti_dus(ay, pazar, V):
    return _ik_kap_kos(ay, pazar, V, lambda K: K.konu_id == 79, gun_min=-0.05)


def ik_s_kap_olagan_disi(ay, pazar, V):
    return _ik_kap_sec(ay, pazar, V, lambda K: K.konu_id == 42)


def ik_s_kap_vbts(ay, pazar, V):
    return _ik_kap_sec(ay, pazar, V, lambda K: K.konu_id == 14)


def ik_s_hacim_dus_20_oyn(ay, pazar, V):
    """Ç70 (A11'in oynaklık ölçekli hali, iki pazarda aynı anlam): gün getirisi <= -3 x önceki 60 günün günlük getiri std'si,
    hacim >= 3x önceki 60 gün medyanı, önceki 20 gün <= -%20."""
    C = _ik_panel(V, "Close"); Vo = _ik_panel(V, "Volume"); r = C / C.shift(1) - 1
    sd = r.shift(1).rolling(60, min_periods=48).std()
    med = Vo.shift(1).rolling(60, min_periods=48).median()
    M = (r <= -3 * sd) & (Vo >= 3 * med) & (med > 0) & (C.shift(1) / C.shift(21) - 1 <= -0.20) & _ik_gecerli(V)
    return _ik_olay(M)


def ik_ruzgar_sayi(ay: IKAyar, V: Dict[str, pd.DataFrame], gun: int) -> pd.DataFrame:
    """IZ_DEFTERI tanımı: RÜZGÂR = sektör sepeti (alt sektör, medyan getiri) - piyasa medyanı, son 'gun' işlem günü.
    BIST: sektor_BIST.csv 'alt_bist'. Döner: tarih x sembol."""
    C = _ik_panel(V, "Close").ffill(limit=5); r = C / C.shift(gun) - 1
    sek = pd.read_csv(os.path.join(ay.kok, "sektor_BIST.csv")).dropna(subset=["alt_bist"])
    alt = dict(zip(sek.sembol.str.upper(), sek.alt_bist))
    piy = r.median(axis=1)
    W = pd.DataFrame(np.nan, index=r.index, columns=r.columns)
    grup: Dict[str, List[str]] = {}
    for s in r.columns:
        if alt.get(str(s).upper()):
            grup.setdefault(alt[str(s).upper()], []).append(s)
    for a, uy in grup.items():
        if len(uy) < 4:
            continue
        sep = r[uy].median(axis=1) - piy
        for s in uy:
            W[s] = sep
    return W


def ik_s_kap_olgun_sozlesme(ay, pazar, V):
    """Ç71 (A9): KAP SOZLESME ya da LISANS_TESVIK, bilgi günü OLGUN rüzgâr (60 gün > +%3 ve 20 gün > +%1)."""
    O = _ik_kap_kos(ay, pazar, V, lambda K: K.tur.isin(["SOZLESME", "LISANS_TESVIK"]))
    if not len(O):
        return O
    W60 = ik_ruzgar_sayi(ay, V, 60); W20 = ik_ruzgar_sayi(ay, V, 20)
    a = np.array([W60.at[g, s] if s in W60.columns else np.nan for s, g in zip(O.sembol, O.gun)])
    b = np.array([W20.at[g, s] if s in W20.columns else np.nan for s, g in zip(O.sembol, O.gun)])
    return O[(a > 0.03) & (b > 0.01)]


def ik_s_k13_duz_dip(ay, pazar, V):
    """Ç73/Ç74: K13 TEHOL tipi taban + düzgün dip (FON_IZI FI_K13B_ESIK: kutu barlarının >= %20'si dibin 2 mum boyu içinde)."""
    F = _ik_fi()
    O = F.fi_k13_tara(V, F.FI_K13B_ESIK)
    return pd.DataFrame({"sembol": O.sembol.values, "gun": pd.to_datetime(O.bilgi).values}) if len(O) \
        else pd.DataFrame(columns=["sembol", "gun"])


def ik_s_duz_dip_gevsek(ay, pazar, V):
    """Ç75: düzgün dip tek başına (FON_IZI FI_K16_GEVSEK: çöküş sonrası 30-80 günlük taban, dip tabanı >= 0,20)."""
    F = _ik_fi()
    O = F.fi_k13_tara(V, F.FI_K16_GEVSEK)
    return pd.DataFrame({"sembol": O.sembol.values, "gun": pd.to_datetime(O.bilgi).values}) if len(O) \
        else pd.DataFrame(columns=["sembol", "gun"])


def _ik_k17(ay, pazar, varyant):
    D = _ik_dosya(ay, "fon_izi/k17_olaylar.csv.gz")
    return _ik_pazar_suz(D[D.varyant == varyant], pazar, "bilgi")


def ik_s_iki_yuvarlama(ay, pazar, V):
    """Ç78: K17 Y1 — çöküş dibinden sonra önce aşağı yuvarlama (∩), hemen ardından yukarı yuvarlama (∪) (FON_IZI k17)."""
    return _ik_k17(ay, pazar, "Y1")


def ik_s_iki_yuvarlama_duz(ay, pazar, V):
    """Ç79: K17 Y2 — Y1 + 2. bölgenin dip tabanı >= 0,20."""
    return _ik_k17(ay, pazar, "Y2")


def ik_s_iki_yuvarlama_kir(ay, pazar, V):
    """Ç80: K17 Y3 — Y1 kutusunun tavanı 60 barda dip kırılmadan geçildiği gün."""
    return _ik_k17(ay, pazar, "Y3")


def ik_s_iki_yuvarlama_siki(ay, pazar, V):
    """Ç81: K17 Y4 — iki bölgede de parabol uyumu R2 >= 0,70 (temiz yay)."""
    return _ik_k17(ay, pazar, "Y4")


def ik_s_iki_yuvarlama_ruz(ay, pazar, V):
    """Ç82: K17 Y5 — Y1 + bilgi gününde sektör rüzgârı (D9b)."""
    return _ik_k17(ay, pazar, "Y5")


def ik_s_iki_yuvarlama_hafif(ay, pazar, V):
    """Ç83: K17 Y6 — Y1, 1'in tepesinden 2'nin dibine -%5..-%15 (hafif silkeleme)."""
    return _ik_k17(ay, pazar, "Y6")


def _ik_k18(ay, pazar, varyant):
    D = _ik_dosya(ay, "fon_izi/k18_olaylar.csv.gz")
    return _ik_pazar_suz(D[D.varyant == varyant], pazar, "bilgi")


def ik_s_cemal_profil(ay, pazar, V):
    """Ç85: K18 C1 — Cemal'in koşan vakalarının ortak profili: >= %30 düşüş sonrası dar kutu (bant <= %50, 20-130 bar), kutu mumu ve
    hacmi düşüştekinden küçük, kutu tavanı kırılım günü (FON_IZI k18)."""
    return _ik_k18(ay, pazar, "C1")


def ik_s_cemal_profil_uzun(ay, pazar, V):
    """Ç86: K18 C2 — C1, kutu >= 40 bar ('aylarca')."""
    return _ik_k18(ay, pazar, "C2")


def ik_s_cemal_profil_sert(ay, pazar, V):
    """Ç87: K18 C3 — C1, önce düşüş <= -%50 ('sert çöküş')."""
    return _ik_k18(ay, pazar, "C3")


def ik_s_cemal_profil_dar(ay, pazar, V):
    """Ç88: K18 C4 — profil, kutu bandı <= %20 (dar çöl; tur 2)."""
    return _ik_k18(ay, pazar, "C4")


def ik_s_cemal_profil_dev(ay, pazar, V):
    """Ç89: K18 C5 — profil + kutuda dev hacim barı (>= kutu medyanının 10 katı; EUHOL 24.12.2024; tur 2)."""
    return _ik_k18(ay, pazar, "C5")


def ik_s_cemal_profil_ruz(ay, pazar, V):
    """Ç90: K18 C6 — C1 + bilgi gününde sektör rüzgârı (D9b; tur 2)."""
    return _ik_k18(ay, pazar, "C6")


IK_SINYAL: Dict[str, Callable] = {
    "tavan": ik_s_tavan, "taban": ik_s_taban, "hacim_dus": ik_s_hacim_dus, "hacim_dus_20": ik_s_hacim_dus_20,
    "blok_taban": ik_s_blok_taban, "geride_hacim": ik_s_geride_hacim, "hacimli_kirilim": ik_s_hacimli_kirilim,
    "doji_kutu": ik_s_doji_kutu, "obek": ik_s_obek, "d13": ik_s_d13, "d12_atilim": ik_s_d12_atilim, "mum_sukun": ik_s_mum_sukun,
    "zemin": ik_s_zemin, "fon_iz_b": ik_s_fon_iz_b, "z0": ik_s_z0, "z0_kuru": ik_s_z0_kuru, "k13": ik_s_k13,
    "fon_giris": ik_s_fon_giris, "fon_yogun5": ik_s_fon_yogun5, "kap_bedelsiz": ik_s_kap_bedelsiz,
    "kap_geri_alim": ik_s_kap_geri_alim, "kap_geri_alim_kosmamis": ik_s_kap_geri_alim_kosmamis,
    "kap_sozlesme_kosmus": ik_s_kap_sozlesme_kosmus, "kap_soylenti_dus": ik_s_kap_soylenti_dus,
    "kap_olagan_disi": ik_s_kap_olagan_disi, "kap_vbts": ik_s_kap_vbts, "hacim_dus_20_oyn": ik_s_hacim_dus_20_oyn,
    "kap_olgun_sozlesme": ik_s_kap_olgun_sozlesme, "k13_duz_dip": ik_s_k13_duz_dip, "duz_dip_gevsek": ik_s_duz_dip_gevsek,
    "iki_yuvarlama": ik_s_iki_yuvarlama, "iki_yuvarlama_duz": ik_s_iki_yuvarlama_duz, "iki_yuvarlama_kir": ik_s_iki_yuvarlama_kir,
    "iki_yuvarlama_siki": ik_s_iki_yuvarlama_siki, "iki_yuvarlama_ruz": ik_s_iki_yuvarlama_ruz,
    "iki_yuvarlama_hafif": ik_s_iki_yuvarlama_hafif,
    "cemal_profil": ik_s_cemal_profil, "cemal_profil_uzun": ik_s_cemal_profil_uzun, "cemal_profil_sert": ik_s_cemal_profil_sert,
    "cemal_profil_dar": ik_s_cemal_profil_dar, "cemal_profil_dev": ik_s_cemal_profil_dev, "cemal_profil_ruz": ik_s_cemal_profil_ruz,
}
IK_ABD_YOK = {"kap_olgun_sozlesme", "kap_bedelsiz", "kap_geri_alim", "kap_geri_alim_kosmamis", "kap_sozlesme_kosmus", "kap_soylenti_dus",
              "kap_olagan_disi", "kap_vbts", "fon_giris", "fon_yogun5"}     # ABD'de karşılık verisi yok (yapısal)


# ---------------------------------------------------------------- 4) PUANLAMA
def ik_tekil(O: pd.DataFrame, tekrar: int) -> pd.DataFrame:
    """Hisse başına 'tekrar' işlem günü (~1,45 takvim günü/işlem günü) içinde ilk olay."""
    O = O.dropna(subset=["gun"]).sort_values(["sembol", "gun"]).reset_index(drop=True)
    tut, son = [], {}
    for i, s, g in zip(O.index, O.sembol, O.gun):
        if s in son and (g - son[s]).days < tekrar * 1.45:
            continue
        son[s] = g; tut.append(i)
    return O.loc[tut].reset_index(drop=True)


def ik_puan(ay: IKAyar, O: pd.DataFrame, B: pd.DataFrame, V: Dict[str, pd.DataFrame], pazar: str, yon: str) -> pd.DataFrame:
    """Olaylar -> dönem satırları: n, ana/ters oranlar, eşli oranlar, katlar, trail ortalama ve eşli trail."""
    F = _ik_fi()
    ana, ters = ("k20", "dus") if yon == "yukari" else ("dus", "k20")       # 'asagi' ve 'koruma' ana ölçüsü dus
    O = O[O.sembol.isin(list(V))]
    O = ik_tekil(O, ay.tekrar)
    sat = []
    if not len(O):
        return pd.DataFrame([{"pazar": pazar, "donem": d, "n": 0} for d, _, _ in IK_DONEM])
    R = F.fi_k10_sonuc(V, O.sembol, O.gun)
    X = O.join(R, how="inner").dropna(subset=["giris"])
    X["hucre"] = F._fi_k10_hucre(X, B) if len(X) else ""
    hb = B.groupby("hucre")[["k20", "dus", "trail"]].mean()
    for ad, b, e in IK_DONEM:
        x = X[(X.giris >= b) & (X.giris <= e)]
        tb = B[(B.giris >= b) & (B.giris <= e)]
        r = {"pazar": pazar, "donem": ad, "n": int(x[ana].notna().sum()), "hisse": int(x.sembol.nunique())}
        for m, ad_ in ((ana, "ana"), (ters, "ters")):
            xv = x[m].dropna()
            es = hb[m].reindex(x.loc[xv.index, "hucre"]).dropna()
            r[ad_] = xv.mean() if len(xv) else np.nan
            r[ad_ + "_esli"] = es.mean() if len(es) else np.nan
            r[ad_ + "_kat"] = r[ad_] / r[ad_ + "_esli"] if len(es) and r[ad_ + "_esli"] else np.nan
            r[ad_ + "_taban"] = tb[m].mean() if len(tb) else np.nan
        xt = x.trail.dropna(); et = hb["trail"].reindex(x.loc[xt.index, "hucre"]).dropna()
        r["trail"] = xt.mean() if len(xt) else np.nan; r["trail_esli"] = et.mean() if len(et) else np.nan
        r["trail_med"] = xt.median() if len(xt) else np.nan
        sat.append(r)
    return pd.DataFrame(sat)


def ik_karar(Z: pd.DataFrame, abd_yok: bool, ay: IKAyar, yon: str = "yukari") -> Tuple[str, str]:
    """Önceden yazılan kural (dosya başı). 'koruma' yönünde katlar ters çevrilir (1/kat >= 1,3 <=> kat <= 0,77).
    Döner: (karar, kısa gerekçe)."""
    H = Z.set_index(["pazar", "donem"])
    def g(p, d, k):
        try:
            v = float(H.at[(p, d), k])
        except Exception:
            return np.nan
        if yon == "koruma" and k.endswith("_kat"):
            return np.inf if v == 0 else (1 / v if v == v else np.nan)     # kat 0 = en güçlü koruma (eskiden NaN sayılıyordu)
        return v
    E = ay.kat_esik
    if abd_yok:
        hc = [("BIST", d) for d, _, _ in IK_DONEM]
        kat = [g(*h, "ana_kat") for h in hc]; ters = [g(*h, "ters_kat") for h in hc]; n = [g(*h, "n") for h in hc]
        if all(k == k and k >= E for k in kat) and all(not (t == t and t >= E) for t in ters):
            return ("BIST-ADAY" if all(x >= ay.n_min for x in n) else "KÜÇÜK ÖRNEK"), "ABD verisi yok; BIST 3 dönem ≥1,3"
        ok = sum(1 for k in kat if k == k and k >= E)
        return "İZ DEĞİL", f"BIST {ok}/3 dönem {'≤0,77' if yon == 'koruma' else '≥1,3'} (ABD verisi yok)"
    kat = [g(*h, "ana_kat") for h in IK_KARAR_HUCRE]; ters = [g(*h, "ters_kat") for h in IK_KARAR_HUCRE]
    n = [g(*h, "n") for h in IK_KARAR_HUCRE]; erken = g("BIST", "2016-22", "ana_kat")
    gecen = sum(1 for k in kat if k == k and k >= E)
    if all(x != x for x in kat[2:]):
        return ("İZ DEĞİL" if gecen < 2 else "EKSİK (ABD olayı yok)",
                f"BIST {gecen}/2 karar hücresi {'≤0,77' if yon == 'koruma' else '≥1,3'}; ABD olay dosyası yok")
    if gecen == 4 and all(not (t == t and t >= E) for t in ters) and not (erken == erken and erken < 1.0):
        return ("İZ" if all(x >= ay.n_min for x in n) else "KÜÇÜK ÖRNEK"), "4/4 hücre ≥1,3, ters yön <1,3"
    if gecen == 4:
        return "İZ DEĞİL", "4/4 ≥1,3 ama ters yön de ≥1,3 (oynaklık) ya da 2016-22 ters"
    if gecen == 3 and all(k == k and k >= 1.0 for k in kat):
        return "ADAY", "3/4 hücre ≥1,3, hiçbiri <1,0"
    return "İZ DEĞİL", f"{gecen}/4 karar hücresi {'≤0,77' if yon == 'koruma' else '≥1,3'}"


# ---------------------------------------------------------------- 5) SEVİYE KOŞUSU
def ik_seviye(ay: IKAyar, seviyeler: List[int], kodlar: Optional[List[str]] = None) -> pd.DataFrame:
    """Seçilen seviyelerdeki sinyalli kayıtları tek cetvelle puanlar; karne_hucre.csv ve karne.csv günceller; indeksi yeniler."""
    os.makedirs(ay.cikti, exist_ok=True)
    K = [r for r in IK_KAYIT if r["sinyal"] and r["seviye"] in seviyeler and (not kodlar or r["kod"] in kodlar)]
    hucre: List[pd.DataFrame] = []
    for pazar in ("BIST", "ABD"):
        if pazar == "ABD" and all(r["sinyal"] in IK_ABD_YOK for r in K):
            continue
        try:
            V = ik_veri(ay, pazar)
        except Exception as ex:
            iklog.error("%s verisi okunamadı: %s", pazar, ex); continue
        B = ik_taban(ay, pazar, V)
        sinyal_onbellek: Dict[str, pd.DataFrame] = {}
        for r in K:
            if pazar == "ABD" and r["sinyal"] in IK_ABD_YOK:
                continue
            try:
                if r["sinyal"] not in sinyal_onbellek:
                    sinyal_onbellek[r["sinyal"]] = IK_SINYAL[r["sinyal"]](ay, pazar, V)
                O = sinyal_onbellek[r["sinyal"]]
                Z = ik_puan(ay, O, B, V, pazar, r["yon"])
                Z.insert(0, "kod", r["kod"]); hucre.append(Z)
                iklog.info("%s %s %s: %d ham olay", r["kod"], pazar, r["sinyal"], len(O))
            except Exception as ex:   # tek çalışma bozuksa diğerleri sürer; hata karneye yazılır
                iklog.error("%s %s puanlanamadı: %s", r["kod"], pazar, ex)
                hucre.append(pd.DataFrame([{"kod": r["kod"], "pazar": pazar, "donem": "HATA", "n": 0, "hata": str(ex)[:200]}]))
    if not hucre:
        raise RuntimeError("IZ_KARNE: puanlanacak çalışma yok")
    Y = pd.concat(hucre, ignore_index=True)
    yol_h = os.path.join(ay.cikti, "karne_hucre.csv")
    if os.path.exists(yol_h):
        eski = pd.read_csv(yol_h)
        Y = pd.concat([eski[~eski.kod.isin(Y.kod.unique())], Y], ignore_index=True)
    Y.to_csv(yol_h, index=False)
    ozet = ik_ozet(ay, Y)
    ik_indeks(ay)
    return ozet


def ik_ozet(ay: IKAyar, Y: pd.DataFrame) -> pd.DataFrame:
    sat = []
    tarih = pd.Timestamp.today().strftime("%Y-%m-%d")
    kayit = {r["kod"]: r for r in IK_KAYIT}
    for kod, Z in Y.groupby("kod"):
        r = kayit.get(kod)
        if r is None:
            continue
        Z = Z[Z.donem != "HATA"]
        karar, neden = ik_karar(Z, r["sinyal"] in IK_ABD_YOK, ay, r["yon"]) if len(Z) else ("HATA", "puanlanamadı")
        H = Z.set_index(["pazar", "donem"]) if len(Z) else None
        def h(p, d, k):
            try:
                return float(H.at[(p, d), k])
            except Exception:
                return np.nan
        s = {"kod": kod, "tarih": tarih, "sinyal": r["sinyal"], "yon": r["yon"], "karar": karar, "neden": neden}
        for p in ("BIST", "ABD"):
            for d, _, _ in IK_DONEM:
                s[f"{p}_{d}_kat"] = h(p, d, "ana_kat"); s[f"{p}_{d}_n"] = h(p, d, "n"); s[f"{p}_{d}_ters"] = h(p, d, "ters_kat")
        sat.append(s)
    O = pd.DataFrame(sat)
    O.to_csv(os.path.join(ay.cikti, "karne.csv"), index=False)
    return O


# ---------------------------------------------------------------- 6) İNDEKS (IZ_DEFTERI.md içine)
def _ik_f(x, nd=2):
    return "—" if x is None or x != x else f"{x:.{nd}f}".replace(".", ",")


def ik_indeks_metni(ay: IKAyar) -> str:
    yol = os.path.join(ay.cikti, "karne.csv")
    KR = pd.read_csv(yol).set_index("kod") if os.path.exists(yol) else pd.DataFrame()
    satir = [IK_ISARET[0], "", "## 0. İNDEKS — bütün çalışmalar ve tek cetvel kararı", "",
             f"Üretici: {IK_SURUM}. Kaynak: IZ_KARNE.py içindeki IK_KAYIT (çalışma kaydı) + arastirma_cikti/iz_karne/karne.csv "
             "(tek cetvel puanları). Bu bölüm elle düzenlenmez: yeni çalışma IK_KAYIT'a bir satır ekler, "
             "`python IZ_KARNE.py seviye N` ya da `indeks` bölümü yeniden yazar (test_iz_karne bunu denetler).", "",
             "TEK CETVEL: olay = sinyal günü, giriş ertesi açılış, hisse başına 60 iş gününde tek olay. Ana ölçü yukarı izlerde "
             "60 günde önce +%20 (−%10'dan önce), kaçınma izlerinde 60 günde önce −%20. Kat = olay oranı / EŞLİ TABAN (aynı ay × "
             "60 gün momentum beşliği × likidite üçlüsü). İZ = BIST 2023, BIST 2024-26, ABD 2023, ABD 2024-26 dört hücrede "
             "kat ≥1,3, n ≥30, ters yön <1,3. ABD verisi olmayan (KAP) en fazla BIST-ADAY olur. Eski kararlar farklı cetvellerle "
             "verildi (ar60, piy, her 5. gün tabanı; 17-21/22-26; ABD'siz); karışıklığın kaynağı bu.", ""]
    # özet sayımlar
    if len(KR):
        sayi = KR.karar.value_counts()
        satir += ["**Tek cetvel özeti:** " + " · ".join(f"{k} {v}" for k, v in sayi.items()) +
                  f" (puanlanan {len(KR)} / kayıtlı {len(IK_KAYIT)} çalışma)", ""]
    if len(KR):
        yakin = []
        for kod, k in KR.iterrows():
            r = next((x for x in IK_KAYIT if x["kod"] == kod), None)
            if r is None:
                continue
            hc = [f"BIST_{d}_kat" for d, _, _ in IK_DONEM] + [f"ABD_{d}_kat" for d, _, _ in IK_DONEM]
            v = [k.get(c) for c in hc]
            v = [(1 / x if r["yon"] == "koruma" and x and x == x else x) for x in v]
            bist = [x for x in v[:3] if x == x]
            if bist and min(bist) >= 1.3:
                yakin.append(f"{kod} {r['ad']} (BIST {' / '.join(_ik_f(x) for x in v[:3])}; ABD {' / '.join(_ik_f(x) for x in v[3:])})")
        izler = [kod for kod, k in KR.iterrows() if k.karar == "İZ"]
        if izler:      # denetim 24 Eki: bu cümle eskiden sabitti, İZ çıksa da 'İZ yok' yazıyordu
            satir += [f"**Kesinleşen durum (tek cetvel):** dört karar hücresinde tutan İZ: {', '.join(izler)}.", ""]
        else:
            satir += ["**Kesinleşen durum (tek cetvel):** dört karar hücresinin hepsinde tutan İZ yok. Eski cetvelde 'GEÇERLİ' yazan "
                      "maddeler eşli tabanla yeniden ölçüldü; fark çoğunlukla hissenin zaten düşmüş/yükselmiş, sakin/oynak olmasından "
                      "geliyordu (eşli taban bunu eşitler).", ""]
        if yakin:
            satir += ["**Eşiğe en yakın (BIST'in 3 döneminde ≥1,3, ABD'de tutmuyor):**", ""] + [f"- {y}" for y in yakin] + [""]
    satir += ["### Görev günlüğü (Cemal'in verdiği işler)", "", "| Tarih | İstek | Yapılan | Sonuç | Durum |", "|---|---|---|---|---|"]
    satir += [f"| {g['tarih']} | {g['istek']} | {g['yapilan']} | {g['sonuc']} | **{g['durum']}** |" for g in IK_GOREV]
    satir += ["", "**Açık kalanlar:**", ""] + [f"- {a}" for a in IK_ACIK] + [""]
    satir += ["### Hata defteri (bütün yanlış hesaplar, düzeltmeler, sapmalar; Cemal 14 Kas 2026)", "",
              "Kaynak: IK_HATA. Her bulunan hata buraya bir satır olarak girer (yeni oturumda da). Kural: hata bulunur -> IK_HATA satırı "
              "-> ilgili Ç kaydına DÜZELTME notu -> karara etkisi açıkça yazılır. Hiçbir hata silinmez; düzeltilen hatanın satırı kalır.", ""]
    satir += ["**Ön uçuş kontrol listesi (IK_KONTROL; her ölçümün ön kaydında doldurulur, `ik_kontrol_kapisi` denetler, "
              "eksikse `kos` çalışmaz; alt ajan iş tanımına `python IZ_KARNE.py kontrol istanimi` çıktısı girer):**", "",
              ik_kontrol_metni("defter"), ""]
    satir += ["### İleri test defteri (yanlış dediğimiz sonra doğru çıkabilir; Cemal 14 Kas 2026)", "",
              "Kaynak: IK_ILERI. Emin olmanın yolu: iddia sabit eşik ve veri kesiğiyle kaydedilir, sonraki dönemin verisinde aynı komutla yeniden "
              "ölçülür; sonuç satıra yazılır, satır silinmez. Etiket: İZ DEĞİL = güç yeterli ve tutmadı; ÖLÇÜLEMEDİ = n ya da güç yetersiz "
              "(yeniden açılır); üç art arda ileri testte aynı yön = kesin.", "",
              "| Kayıt | İddia | Karar (şimdi) | n / güç | Sabit eşik | Veri kesiği | Sonraki test (tarih / koşul) | Sonuç |", "|---|---|---|---|---|---|---|---|"]
    satir += [f"| {i['kod']} | {i['iddia']} | **{i['karar']}** | {i['guc']} | {i['esik']} | {i['kesik']} | {i['sonraki']} | {i['sonuc'] or '—'} |" for i in IK_ILERI]
    satir.append("")
    if IK_HATA:
        sayim = {}
        for h in IK_HATA:
            sayim[h["tur"]] = sayim.get(h["tur"], 0) + 1
        bulan = {}
        for h in IK_HATA:
            bulan[h["bulan"]] = bulan.get(h["bulan"], 0) + 1
        satir += ["**Sayım:** " + str(len(IK_HATA)) + " hata · tür: " + " · ".join(f"{k} {v}" for k, v in sorted(sayim.items(), key=lambda x: -x[1]))
                  + " · bulan: " + " · ".join(f"{k} {v}" for k, v in sorted(bulan.items(), key=lambda x: -x[1])), "",
                  "| # | Tarih | Kayıt | Hata | Tür | Bulan | Karara etkisi | Düzeltme | Ders | Kaynak |", "|---|---|---|---|---|---|---|---|---|---|"]
        satir += [f"| H{n} | {h['tarih']} | {h['kayit']} | {h['hata']} | {h['tur']} | {h['bulan']} | {h['etki']} | {h['duzeltme']} | {h['ders']} | {h['kaynak']} |"
                  for n, h in enumerate(IK_HATA, 1)]
        satir.append("")
    for sv in (1, 2, 3, 4, 0):
        R = [r for r in IK_KAYIT if r["seviye"] == sv]
        if not R:
            continue
        satir += [f"### Seviye {sv} — {IK_SEVIYE_AD[sv]}", "",
                  "| Kod | Tarih | Çalışma | Dosya | Eski karar | Tek cetvel | BIST 16-22 / 23 / 24-26 | ABD 16-22 / 23 / 24-26 | Defter |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for r in R:
            if r["kod"] in KR.index:
                k = KR.loc[r["kod"]]
                kb = " / ".join(_ik_f(k.get(f"BIST_{d}_kat")) + (f" (n{int(k.get(f'BIST_{d}_n'))})"
                                if k.get(f"BIST_{d}_n") == k.get(f"BIST_{d}_n") and k.get(f"BIST_{d}_n") < 30 else "")
                                for d, _, _ in IK_DONEM)
                ka = " / ".join(_ik_f(k.get(f"ABD_{d}_kat")) + (f" (n{int(k.get(f'ABD_{d}_n'))})"
                                if k.get(f"ABD_{d}_n") == k.get(f"ABD_{d}_n") and k.get(f"ABD_{d}_n") < 30 else "")
                                for d, _, _ in IK_DONEM)
                yeni = f"**{k.karar}** ({IK_YON_IM.get(r['yon'], '')}, {k.tarih})"
            else:
                kb = ka = "—"
                yeni = "puanlanmadı" + (f": {r['not']}" if r["not"] else "")
            satir.append(f"| {r['kod']} | {r['tarih']} | {r['ad']} | {r['dosya']} | {r['eski']} | {yeni} | {kb} | {ka} | {r['defter']} |")
        satir.append("")
    satir += ["Kat sütunları ana ölçünün eşli tabana göre katıdır (↑ yukarı iz: önce +%20, ≥1,3 aranır; ↓ kaçınma izi: önce −%20, "
              "≥1,3 aranır; ⊥ koruma izi: önce −%20, ≤0,77 aranır). "
              "(nX) = o hücrede 30'dan az olay. Ayrıntı: arastirma_cikti/iz_karne/karne_hucre.csv.", "", IK_ISARET[1]]
    return "\n".join(satir)


def ik_indeks(ay: IKAyar) -> str:
    """IZ_DEFTERI.md içindeki işaretli bölümü yeniden yazar (yoksa başlık bloğundan sonra ekler)."""
    metin = open(ay.defter, encoding="utf-8").read()
    yeni = ik_indeks_metni(ay)
    if IK_ISARET[0] in metin and IK_ISARET[1] in metin:
        bas = metin.index(IK_ISARET[0]); son = metin.index(IK_ISARET[1]) + len(IK_ISARET[1])
        metin = metin[:bas] + yeni + metin[son:]
    else:
        i = metin.index("## A. ")
        metin = metin[:i] + yeni + "\n\n" + metin[i:]
    with open(ay.defter, "w", encoding="utf-8") as f:
        f.write(metin)
    return yeni


# ---------------------------------------------------------------- 7) DERS PDF (Cemal: kısa, grafikte şablon)
def ik_ders(ay: IKAyar, yol: Optional[str] = None) -> str:
    """IZ_KARNE_ders.pdf: (1) bütün puanlanan maddeler, 4 karar hücresi katı ve 1,3 çizgisi; (2) eski 'GEÇERLİ' neden düştü:
    sıradan güne göre kat vs eşli tabana göre kat; (3) eşiğe en yakın iki madde için grafik şablonu (hisse adı yok);
    (4) kendin nasıl bakarsın."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    yol = yol or os.path.join(ay.cikti, "IZ_KARNE_ders.pdf")
    KR = pd.read_csv(os.path.join(ay.cikti, "karne.csv"))
    Y = pd.read_csv(os.path.join(ay.cikti, "karne_hucre.csv"))
    kayit = {r["kod"]: r for r in IK_KAYIT}
    A4 = (8.27, 11.69)

    def yazi(fig, y, baslik, satirlar, boy=10, gen=92):
        fig.text(0.06, y, baslik, fontsize=14, weight="bold", va="top", color="#1f2a44"); y -= 0.04
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.06 if not s.startswith("- ") or k == 0 else 0.085, y, parca, fontsize=boy, va="top"); y -= 0.022
            y -= 0.004
        return y

    with PdfPages(yol) as pdf:
        # 1) özet
        fig = plt.figure(figsize=A4)
        y = yazi(fig, 0.97, "DERS: NELER İZ, NELER DEĞİL — TEK CETVEL", [
            "Sorun: eski kararlar farklı cetvellerle verilmişti (ar60, piyasaya göre fark, her 5. gün tabanı; 17-21/22-26; çoğunda ABD yok). "
            "Bu yüzden önce 'iz' denen şey sonra 'iz değil' çıkıyordu.",
            "Tek cetvel: sinyal günü → ertesi açılış giriş → 60 günde önce +%20 mi (yukarı izler) / önce −%20 mi (kaçınma izleri). "
            "Kıyas: EŞLİ TABAN = aynı ay, aynı 60 gün momentumu, aynı likiditedeki sıradan günler. İZ = 4 hücrede (BIST 2023, "
            "BIST 2024-26, ABD 2023, ABD 2024-26) ≥1,3 kat.",
            f"Sonuç: {len(KR)} madde puanlandı → İZ 0, ADAY 0. Noktalar: her maddenin 4 hücredeki katı. Kırmızı çizgiyi (1,3) "
            "dördü birden geçen yok.",
        ], boy=9.5)
        K = KR.copy()
        K["ad"] = [f"{k} {kayit[k]['ad'][:38]}" for k in K.kod]
        hc = [("BIST_2023_kat", "#1f2a44", "o", "BIST 2023"), ("BIST_2024-26_kat", "#1f2a44", "s", "BIST 24-26"),
              ("ABD_2023_kat", "#e67e22", "o", "ABD 2023"), ("ABD_2024-26_kat", "#e67e22", "s", "ABD 24-26")]
        ax = fig.add_axes([0.42, 0.05, 0.53, y - 0.08])
        for i, r in enumerate(K.itertuples()):
            inv = kayit[r.kod]["yon"] == "koruma"
            for c, renk, m, et in hc:
                v = K.at[r.Index, c]
                if v == v and v:
                    ax.scatter(1 / v if inv else v, i, color=renk, marker=m, s=18)
        ax.axvline(1.0, color="#999", lw=1); ax.axvline(1.3, color="#c0392b", lw=2, ls="--")
        ax.set_yticks(range(len(K))); ax.set_yticklabels(K.ad, fontsize=6); ax.invert_yaxis(); ax.set_xlim(0, 3)
        ax.set_xlabel("kat (eşli tabana göre; koruma maddelerinde 1/kat)", fontsize=8)
        for c, renk, m, et in hc:
            ax.scatter([], [], color=renk, marker=m, s=18, label=et)
        ax.legend(fontsize=6, loc="lower right")
        pdf.savefig(fig); plt.close(fig)
        # 2) eski GEÇERLİ neden düştü
        fig = plt.figure(figsize=A4)
        y = yazi(fig, 0.97, "ESKİ 'GEÇERLİ' NEDEN DÜŞTÜ?", [
            "Açık çubuk: sıradan güne göre kat (eski yöntem). Koyu çubuk: eşli tabana göre kat (tek cetvel). BIST 2024-26.",
            "Örnek: tavan günü sonrası düşüş sıradan güne göre 1,4 kat görünür; ama tavan yapan hisse zaten çok yükselmiş ve oynaktır. "
            "Aynı momentumdaki günlerle kıyaslayınca fark küçülür. Doji kutusu tersine sakin hissedir: 'risk düşük' görünür, sakin "
            "hisselerle kıyaslayınca fark yok.",
        ], boy=9.5)
        sec = [k for k in ("Ç15", "Ç16", "Ç17", "Ç18", "Ç23", "Ç26", "Ç38", "Ç24", "Ç60") if k in set(Y.kod)]
        ax = fig.add_axes([0.10, 0.12, 0.85, y - 0.18])
        x = np.arange(len(sec))
        ham, esl = [], []
        for k in sec:
            h = Y[(Y.kod == k) & (Y.pazar == "BIST") & (Y.donem == "2024-26")]
            ham.append(float(h.ana.iloc[0] / h.ana_taban.iloc[0]) if len(h) and h.ana_taban.iloc[0] else np.nan)
            esl.append(float(h.ana_kat.iloc[0]) if len(h) else np.nan)
        ax.bar(x - 0.2, ham, 0.4, color="#b8c4d6", label="sıradan güne göre (eski)")
        ax.bar(x + 0.2, esl, 0.4, color="#1f2a44", label="eşli tabana göre (tek cetvel)")
        ax.axhline(1.3, color="#c0392b", lw=2, ls="--"); ax.axhline(1.0, color="#999", lw=1)
        ax.set_xticks(x); ax.set_xticklabels([f"{k}\n{kayit[k]['defter'].replace('IZ ', '')}\n{IK_YON_IM.get(kayit[k]['yon'], '')[:1]}"
                                              for k in sec], fontsize=7)
        ax.legend(fontsize=8); ax.set_ylabel("kat")
        pdf.savefig(fig); plt.close(fig)
        # 3) şablonlar: eşiğe en yakın (A11, A14) — BIST örnekleri, hisse adı yok
        try:
            V = ik_veri(ay, "BIST")
            F = _ik_fi()
            for kod in ("Ç24", "Ç60"):
                r = kayit[kod]
                O = ik_tekil(IK_SINYAL[r["sinyal"]](ay, "BIST", V), ay.tekrar)
                O = O[(O.gun >= "2024-01-01") & (O.gun <= "2026-06-30")].reset_index(drop=True)
                R = F.fi_k10_sonuc(V, O.sembol, O.gun); X = O.join(R, how="inner").dropna(subset=["dus"])
                orn = [X[X.dus == 1].iloc[len(X[X.dus == 1]) // 2], X[X.dus == 0].iloc[len(X[X.dus == 0]) // 2]] \
                    if (X.dus == 1).any() and (X.dus == 0).any() else []
                h = Y[(Y.kod == kod)].set_index(["pazar", "donem"])
                fig = plt.figure(figsize=A4)
                yazi(fig, 0.97, f"ŞABLON: {r['ad']} ({r['defter'].replace('IZ ', '')})", [
                    f"Nedir: {r['soru']} Kural: {'gün ≤ −%5, hacim ≥ 3× 60 gün medyanı, önceki 20 gün ≤ −%20' if kod == 'Ç24' else 'gün ≤ −%9,5, hacim ≥ 20× 20 gün medyanı'}.",
                    "Grafikte: dikey kırmızı çizgi = sinyal günü; yeşil çizgi = ertesi açılış (giriş); kesikli çizgi = girişin %20 altı. "
                    "Altta hacim (kırmızı = sinyal günü).",
                    "Test (önce −%20, eşli kat): BIST " + " / ".join(_ik_f(h.at[("BIST", d), "ana_kat"]) for d, _, _ in IK_DONEM) +
                    " · ABD " + " / ".join(_ik_f(h.at[("ABD", d), "ana_kat"]) for d, _, _ in IK_DONEM) +
                    ". BIST'te güçlü, ABD'de tutmuyor → standartla İZ DEĞİL; 'BIST'e özgü risk süzgeci' olup olmayacağı senin kararın.",
                    "Kullanım (karar verilirse): alım sinyali değil; bu gün gelen hissede yeni alım yapma / boyutu küçült.",
                ], boy=9.5)
                for j, e in enumerate(orn):
                    d = V[e.sembol]; i = d.index.get_loc(pd.Timestamp(e.gun)); w = d.iloc[max(0, i - 60):i + 62]
                    ax = fig.add_axes([0.10, 0.45 - j * 0.38, 0.85, 0.22]); ax2 = fig.add_axes([0.10, 0.38 - j * 0.38, 0.85, 0.06])
                    ax.plot(w.index, w.Close, color="#1f2a44", lw=1)
                    ax.axvline(d.index[i], color="#c0392b", lw=1.2)
                    if i + 1 < len(d):
                        g = d.Open.iloc[i + 1]; ax.axvline(d.index[i + 1], color="#27ae60", lw=0.8)
                        ax.axhline(g * 0.8, color="#c0392b", ls="--", lw=0.8); ax.axhline(g * 1.2, color="#27ae60", ls=":", lw=0.8)
                    ax.set_xticks([]); ax.tick_params(labelsize=7)
                    ax.set_title(f"Örnek {j + 1}: {'önce −%20 geldi' if e.dus == 1 else 'önce −%20 gelmedi'} "
                                 f"({pd.Timestamp(e.gun).year})", fontsize=9)
                    ax2.bar(w.index, w.Volume, color=["#c0392b" if t == d.index[i] else "#95a5a6" for t in w.index], width=1.0)
                    ax2.set_yticks([]); ax2.set_xticks([])
                pdf.savefig(fig); plt.close(fig)
        except Exception as ex:   # şablon sayfası çizilemezse ders yine çıkar
            iklog.error("ders şablon sayfası çizilemedi: %s", ex)
        # 4) kendin nasıl bakarsın
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.97, "KENDİN NASIL BAKARSIN (5 SORU)", [
            "- 1) Bu görüntü hangi hissede çıkıyor? Zaten çok düşmüş / çok yükselmiş / çok sakin hisse mi? Öyleyse sonucu o tip "
            "hisselerle karşılaştır, sıradan hisseyle değil (eşli taban).",
            "- 2) Hem yukarı hem aşağı hareket artıyorsa (iki kat birden yükseliyorsa) bu iz değil, oynaklıktır.",
            "- 3) Aynı şey 2023'te de, 2024-26'da da, ABD'de de oluyor mu? Bir dönemde olup ötekinde olmayan iz değildir.",
            "- 4) Seçerken sonucu bilen bir bilgi kullandın mı? (örn. 'kutu kırılmadı' bilgisi sonradan öğrenilir; bu derste "
            "doji kutusunda bu hata yakalandı ve düzeltildi.)",
            "- 5) Tek vaka (TEHOL) iz değildir; evrende 30'dan fazla olay ve 4 hücre gerekir.",
            "",
            "Bundan sonra: her yeni fikir IZ_KARNE kaydına bir satır olarak girer, aynı cetvelle puanlanır, indeks kendini yeniler. "
            "Eski bir fikri sorduğunda indeksteki Ç kodundan ne zaman, hangi dosyayla, neyle ölçüldüğünü görürsün.",
        ], boy=10)
        pdf.savefig(fig); plt.close(fig)
    return yol


# ---------------------------------------------------------------- 7) DENETİM DERSİ (24 Eki 2026)
# Geriye dönük kod denetiminin (6 bağımsız denetçi, her bulgu yeniden üretildi) sonuç değiştiren kısımları. Sayılar düzeltme öncesi
# ve sonrası koşumlardan (arastirma_cikti/col_yol, col_obek, fon_izi/k16_gevsek_ozet.csv; D13 eşli taban denetçi ölçümü) alınmıştır.
IK_DENETIM_SAYI: Dict[str, Any] = {
    "t10": {"BIST": {"önce": (156.8, 144.0), "sonra": (144.1, 154.6)}, "ABD": {"önce": (17.0, 21.4), "sonra": (0.3, 6.2)}},
    "obek_alim": {"donem": ["2016-19", "2020-22", "2023", "2024-26"], "obek": [70, 78, 67, 71], "taban": [53, 62, 53, 48],
                  "esli": [67, 76, 70, 67]},
    "d13_boz": {"donem": ["BIST 16-19", "BIST 20-22", "BIST 2023", "BIST 24-26", "ABD 22-23", "ABD 24-26"], "d13": [8.5, 5.8, 2.4, 9.3, 10.5, 8.2],
                "taban": [35, 31, 41, 44, 42, 37], "esli": [13.3, 12.4, 8.4, 15.8, 16.0, 13.3]},     # COL_TESPIT v1.1 yeniden kosum
    "duzgun_dus": {"hucre": ["BIST 16-22", "BIST 2023", "BIST 24-26", "ABD 16-22", "ABD 2023", "ABD 24-26"],
                   "önce": [1.92, 1.00, 1.14, 1.32, 1.26, 1.23], "sonra": [1.30, 0.75, 0.93, 1.10, 1.07, 1.07]},
}


def ik_ders_denetim(ay: IKAyar, yol: Optional[str] = None) -> str:
    """Ders 7 (Cemal 24 Eki: 'eski modeller hata yapmış olabilir, bul, doğrula, düzelt, yeniden koştur'): (1) hata türleri ve
    hangi sonucu nasıl şişirdikleri; (2) önce/sonra grafikleri (T10, öbek alım, D13 bozulma, düzgün dip −%20); (3) karar durumu ve
    üretim hataları. Çürüyen ölçü dersi kısa tutulur (CLAUDE.md)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    yol = yol or os.path.join(ay.cikti, "IZ_KARNE_ders7_denetim.pdf")
    D = IK_DENETIM_SAYI
    A4 = (8.27, 11.69)

    def yazi(fig, y, baslik, satirlar, boy=9.5, gen=94):
        fig.text(0.06, y, baslik, fontsize=14, weight="bold", va="top", color="#1f2a44"); y -= 0.04
        for s in satirlar:
            for j, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.06 if not s.startswith("- ") or j == 0 else 0.085, y, parca, fontsize=boy, va="top"); y -= 0.021
            y -= 0.004
        return y

    def cubuk(ax, etiket, seriler, renk, baslik, ylab, cizgi=None):
        x = np.arange(len(etiket)); w = 0.8 / len(seriler)
        for i, (ad, v) in enumerate(seriler):
            ax.bar(x + (i - (len(seriler) - 1) / 2) * w, v, w, label=ad, color=renk[i])
        if cizgi is not None:
            ax.axhline(cizgi, color="#c0392b", ls="--", lw=1.5)
        ax.set_xticks(x); ax.set_xticklabels(etiket, fontsize=7, rotation=25, ha="right"); ax.set_title(baslik, fontsize=10)
        ax.set_ylabel(ylab, fontsize=8); ax.set_ylim(0, ax.get_ylim()[1] * 1.25)
        ax.legend(fontsize=6.5, frameon=False, loc="upper center", ncol=len(seriler)); ax.tick_params(labelsize=7)

    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        y = yazi(fig, 0.96, "DERS 7: GERİYE DÖNÜK DENETİM — HATALAR SONUCU NASIL ŞİŞİRDİ?", [
            "Sen: 'Eski modeller sık hata yapıyordu; testlerdeki yanlışları bul, doğrula, düzelt, yeniden koştur.' Altı bağımsız denetçi "
            "kodu bölüm bölüm okudu; her bulgu sentetik ya da gerçek veriyle yeniden üretildi, sonra düzeltilip ölçümler yeniden koşuldu.",
            "Sonuç kısaca: hiçbir 'iz değil' kararı 'iz' olmadı. Ama eskiden pozitif görünen dört iddia düştü (aşağıda), ve üretim "
            "kodunda (takip.py) gerçek para etkisi olan hatalar bulundu; onlar senin 'yaz' kararını bekliyor.",
        ])
        y = yazi(fig, y - 0.01, "Hata türleri (öğrenmen gereken altı tuzak)", [
            "- KOPYA İŞLEM: ardışık sinyaller aynı alım gününe düşüp aynı işlem 2-21 kez sayıldı (öbek işlemlerinin yarısı). n ve "
            "anlamlılık iki kat şişti; slot simülasyonu aynı hisseye birden çok slot açtı. Üretimde hisse bir kez tutulur.",
            "- GELECEĞİ GÖREN KONTROL GRUBU: eşli kutu 'bu dipten hiç olay çıkmamış' diye seçildi; olay 50 bar sonra da çıkabildiği için "
            "kontrol grubu sonucun içindeki fiyat yoluna göre seçilmiş oldu.",
            "- KIYASLANAMAZ TABAN: öbek/D13 sinyali tavana yakın ve dipten uzak; taban kutusu (son 15 bar) ise tersine. 'Alım oranı "
            "tabandan +15-20 puan' bu mesafeden geliyordu. Doğrusu: aynı tavan/dip uzaklığındaki tabanla kıyas (eşli taban).",
            "- GERÇEK HAREKETİ BÖLÜNME SANMAK: BIST verisinde %10,5-30 yukarı tavan günleri (1.068) ve 15 Şubat 2023 deprem açılışı "
            "(375 hisse) bölünme sanılıp geçmiş fiyat oynatılıyordu. Bölünme/bedelsiz fiyatı düşürür, yükseltmez.",
            "- AÇIK İŞLEMİ KAPANMIŞ SAYMAK: trail'deki işlem 120. barda kesilip verinin son gününe atlıyordu ya da veri bitince "
            "kapanmış sayılıyordu. Kazananların bir kısmı atılıyor, bir kısmı yıllarca tutulmuş gibi görünüyordu.",
            "- KÜÇÜK PENCERE KAYMASI: 'dipten sonra yeni dip yok' kontrolü bir barı atlıyordu (K13: 193 olayın 45'inde ihlal).",
        ], boy=8.8)
        pdf.savefig(fig); plt.close(fig)

        fig = plt.figure(figsize=A4)
        yazi(fig, 0.97, "ÖNCE / SONRA: DÜŞEN DÖRT İDDİA", [], boy=9)
        t = D["t10"]
        ax = fig.add_axes([0.08, 0.70, 0.38, 0.22])
        cubuk(ax, ["BIST önce", "BIST sonra", "ABD önce", "ABD sonra"],
              [("T10 (+%8 → maliyete stop)", [t["BIST"]["önce"][0], t["BIST"]["sonra"][0], t["ABD"]["önce"][0], t["ABD"]["sonra"][0]]),
               ("T10'suz mevcut", [t["BIST"]["önce"][1], t["BIST"]["sonra"][1], t["ABD"]["önce"][1], t["ABD"]["sonra"][1]])],
              ["#e67e22", "#1f2a44"], "1) T10 dayanağı: 30 slot portföy, 4 dönem ort. %", "%")
        o = D["obek_alim"]
        ax = fig.add_axes([0.56, 0.70, 0.38, 0.22])
        cubuk(ax, o["donem"], [("öbek", o["obek"]), ("ham taban (eski kıyas)", o["taban"]), ("eşli taban (düzeltme)", o["esli"])],
              ["#1f2a44", "#bdc3c7", "#27ae60"], "2) Öbekten sonra ALIM oranı %", "%")
        b = D["d13_boz"]
        ax = fig.add_axes([0.08, 0.38, 0.38, 0.22])
        cubuk(ax, b["donem"], [("D13", b["d13"]), ("ham taban", b["taban"]), ("eşli taban", b["esli"])],
              ["#1f2a44", "#bdc3c7", "#27ae60"], "3) D13 sonrası bozulma %", "%")
        g = D["duzgun_dus"]
        ax = fig.add_axes([0.56, 0.38, 0.38, 0.22])
        cubuk(ax, g["hucre"], [("önce", g["önce"]), ("sonra", g["sonra"])], ["#bdc3c7", "#1f2a44"],
              "4) Düzgün dip → önce −%20, eşli kutu katı", "kat", cizgi=1.3)
        yazi(fig, 0.30, "Okuma", [
            "- 1) T10'un 'portföyü artırır' gerekçesi tersine döndü (BIST +144 vs +155, ABD 0 vs +6). Kalan tek etkisi ağır kaybı "
            "azaltması (%9 → %5). Yani T10 bir getiri kuralı değil, bir sigorta: daha az kazanç karşılığı daha az ağır zarar.",
            "- 2) Öbek 'alım gelir mi' sorusuna da cevap vermiyor: aynı uzaklıktaki sıradan kutuyla fark −3..+4 puan.",
            "- 3) D13'ün bozulma üstünlüğü küçüldü (eşli tabanın 0,3-0,65'i, 1/5 değil); 'alım oranı +12..26 puan' mekanikti (eşli "
            "fark +0,5..+3,8). D13'ü seçtiren ölçütü artık hiçbir varyant geçmiyor; üretimde kalması senin kararın.",
            "- 4) 'Çok test edilen dip daha sık kırılıyor' gözlemi kontrol grubu hatasındandı; düzeltince tutarlı değil.",
        ], boy=8.8)
        pdf.savefig(fig); plt.close(fig)

        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "KARAR DURUMU VE ÜRETİM HATALARI", [
            "Tek cetvel yeniden koşuldu (41 çalışma): İZ 0. Eşiğe en yakın yine BIST'e özgü A11 ve A14. D13 artık ABD'de de "
            "puanlandı (2023 0,97, 2024-26 0,98): iz değil.",
            "Üretimde (takip.py / BASLAT.py) doğrulanan hatalar — kod senin 'yaz' kararın olmadan değişmez:",
            "- Çıkış yalnız SON güne bakıyor: atlanan ya da birden gelen günlerde taban/maliyet/trail çıkışı kaçıyor; kapanan "
            "işlemlerin getirisi bu yüzden yola bağlı (16 Eki satırları günlük oynatmada farklı çıkıyor).",
            "- Bedelsiz/bölünme sonrası pozisyon ve aday fiyatları ölçeklenmiyor: %100 bedelsizde sahte −%48 'taban' satışı.",
            "- AL ekran satırı yanlış sütunları basıyor (22 Eki ENTRA: pozisyon 'nan', 'OZ-', 'serbest' yanlış).",
            "- Maliyet çıkışı boşlukla açılışta da giriş fiyatından yazılıyor; taban önceliği T10 ölçümünden farklı.",
            "- Verisi durmuş hissedeki pozisyon rapordan sessizce kayboluyor (T9 fiilen çalışmıyor).",
            "- XU100 yarım bar düzeltmesi ad çakışmasıyla devre dışı; listede bekleyen fon hisselerine süzgeç uygulanmıyor.",
            "Kendin nasıl bakarsın: bir sonuç 'çok iyi' görünüyorsa önce üç soruyu sor — aynı işlem kaç kez sayıldı? kontrol grubu "
            "sonucu bilmeden mi seçildi? kıyas aynı koşulda mı (aynı uzaklık, aynı gün, aynı çöküş)?",
        ], boy=9)
        pdf.savefig(fig); plt.close(fig)
    return yol


def iz_karne(komut: str = "indeks", seviye: Optional[List[int]] = None) -> Any:
    ay = IKAyar()
    if komut == "indeks":
        return ik_indeks(ay)
    return ik_seviye(ay, seviye or [1, 2, 3])


def _cakisma_kontrol_ik(_once=_CK_ONCE_IK, _dosya_ad='IZ_KARNE.py'):
    """Çakışma kapısı (FON_IZI ile aynı): yüklenirken başka dosyanın bellekteki adını ezerse durur; aynı dosyanın yeniden
    yüklenmesi serbest (_CK_KAYIT ad -> dosya)."""
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_IK', '_CK_KAYIT', '_cakisma_kontrol_ik', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 're', 'sys', 'logging', 'annotations', 'Any', 'Callable', 'Dict', 'List', 'Optional', 'Tuple',
           'dataclass', 'field')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya_ad and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya_ad
    if ezilen:
        raise RuntimeError(f"{_dosya_ad}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ik()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    if len(sys.argv) > 1 and sys.argv[1] == "indeks":
        ik_indeks(IKAyar()); print("indeks yazıldı"); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "kontrol":
        print(ik_kontrol_metni(sys.argv[2] if len(sys.argv) > 2 else "onkayit")); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "ders":
        print(ik_ders(IKAyar())); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "denetimders":
        print(ik_ders_denetim(IKAyar())); sys.exit(0)
    if len(sys.argv) > 2 and sys.argv[1] == "seviye":
        sv = [int(x) for x in sys.argv[2].split(",")]
        kod = sys.argv[3].split(",") if len(sys.argv) > 3 else None
        print(ik_seviye(IKAyar(), sv, kod)[["kod", "sinyal", "yon", "karar", "neden"]].to_string(index=False)); sys.exit(0)
    print("kullanım: python IZ_KARNE.py indeks | kontrol [onkayit|istanimi|defter] | ders | denetimders | seviye 1[,2,3] [Ç16,Ç17]")
