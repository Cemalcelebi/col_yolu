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
       "D9 yön ADAY (%56-61); test sürüyor", "COL_OZET §9.1", 2, notu="Olay dosyası yok."),
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
          "Düzgün dip, TEHOL'ün öteki ölçüleri olmadan da fark yaratır mı?", "Yeni deneme", "IZ C", 2, "duz_dip_gevsek", "yukari"),
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
          notu="Eşli kutuya (aynı çöküş, desen yok) göre de önce +%20 katı BIST 0,99 / 1,08 / 0,87, ABD 1,03 / 1,02 / 0,86 → İZ DEĞİL."),
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
]
IK_ACIK: List[str] = [
    "ÜRETİM (denetim 24 Eki, 'yaz' bekliyor): takip.py çıkışları yalnız son güne bakıyor (atlanan günlerde çıkış kaçıyor); bedelsiz/bölünmede "
    "pozisyon ve aday fiyatları ölçeklenmiyor (sahte −%48 satış); AL ekran satırı yanlış sütunlar; T10 boşluk dolumu ve taban önceliği; T9 ölü; "
    "_yarim_bar_at ad çakışması (XU100); listedeki fon hisselerine süzgeç yok; boş hedef_vurdu; trail aynı bar; pkl biçimi; test_takip log yan etkisi.",
    "T10 kararı yeniden (Cemal): düzeltilmiş COL_YOL'da T10 getiriyi artırmıyor (BIST +144 vs +155, ABD 0 vs +6), yalnız ağır kaybı azaltıyor.",
    "DENETIM.py / STOP_TEST.py düzeltildi (veri sonunda açık işlem) ama OB önbellekleri Drive'da; Colab'da yeniden koşulmalı.",
    "ABD 13F: SEC indirmesi e-posta içeren istek olduğu için izin sisteminde engellendi; Cemal açık izin/ayar verirse yapılır.",
    "Seviye 4 (sistem/çıkış/portföy: B15-T10, B5/B6/B8) tek cetvelle değil slot simülasyonuyla yeniden ölçülecek.",
    "ABD olay dosyası olmayan madde (A13 doji kutusu): BIST'te zaten tutmadığı için ABD taraması ertelendi (D13'ün ABD olayları "
    "denetimde bulundu ve puanlandı).",
    "Karar bekleyen standart sorusu (Cemal): yalnız BIST'te güçlü risk izleri (A11, A14: BIST 3 dönemde 1,5-2,6 kat, ABD 1,0-1,4) "
    "'BIST'e özgü risk süzgeci' diye ayrı sınıf olsun mu? Şu anki standartla iz değil.",
    "Puanlanamayan eski maddeler: A7 (veri yok), A8 (sözleşme tutarı yok), B10/B11 (kriz takvimi), B12/B13 ve D7 (çöl segment olay dosyası yok).",
    "D13 yakalama (Cemal'in vakaları, 25 Eki): üretim D13 Cemal'in koşan BINBN-24, KTLEV-24, MANAS-25a/b bölgelerini görmedi (dip yeni / parabol "
    "yok); K18 kutusu (bandı <= %50 en uzun pencere, dibe ilk değdiği günden) bunları gördü. Tespit kuralını değiştirmek üretim kararı ('yaz'); "
    "kazanç değil yalnız yakalama değişir (K18 profili iz değil).",
]


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
    if len(sys.argv) > 1 and sys.argv[1] == "ders":
        print(ik_ders(IKAyar())); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "denetimders":
        print(ik_ders_denetim(IKAyar())); sys.exit(0)
    if len(sys.argv) > 2 and sys.argv[1] == "seviye":
        sv = [int(x) for x in sys.argv[2].split(",")]
        kod = sys.argv[3].split(",") if len(sys.argv) > 3 else None
        print(ik_seviye(IKAyar(), sv, kod)[["kod", "sinyal", "yon", "karar", "neden"]].to_string(index=False)); sys.exit(0)
    print("kullanım: python IZ_KARNE.py indeks | ders | denetimders | seviye 1[,2,3] [Ç16,Ç17]")
