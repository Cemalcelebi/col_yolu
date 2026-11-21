# -*- coding: utf-8 -*-
"""HIPOTEZ_ENVANTERI.md ureticisi (21 Kasim 2026). Olcum yok, ag yok.
Ana tablo IK_KAYIT'tan mekanik cikar; aile / karar / guvenilirlik siniflamasi asagidaki
elle doldurulmus sozluklerden (kayit metni okunarak) gelir. Kullanim:
  python arastirma_cikti/kasa/hipotez_envanteri.py
Yalniz okur: IZ_KARNE (IK_KAYIT, IK_HATA, IK_ILERI), kural_defteri, k60_kutuphane, dusus_sonrasi.
Yazar: arastirma_cikti/kasa/HIPOTEZ_ENVANTERI.md. Defter dosyalarina dokunmaz."""
import os, re, sys, collections
KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, KOK)
import IZ_KARNE as IK
AC = os.path.join(KOK, 'arastirma_cikti')
CIKTI = os.path.join(AC, 'kasa', 'HIPOTEZ_ENVANTERI.md')

# ---------- cakisma kapisi: modul adlari bellekte baska bir seyi ezmesin ----------
for _ad in ('KARAR', 'AILE', 'CETVEL_ARALIK'):
    pass

YKPER = {}
C204_NOT = (" | Ç204 (CETVEL2 R15 yeniden koşu, 21 Kas): eski h5 farkları (+9..+34 puan) R15'te −0,2..+0,7 puana indi, aralıklar 0'ı kesiyor: "
            "dipteki 'daha sık +%5' üstünlüğü yön değil oynaklıkmış")
AILE = {'SEK': 'şekil / yapı', 'HAC': 'hacim / tavan-taban', 'MOM': 'momentum / gösterge / makine / sinyal kütüphanesi',
        'TEM': 'temel / bilanço', 'ICE': 'içeriden / açığa satış', 'FON': 'fon izi / büyük alıcı / BofA',
        'OLA': 'KAP olay', 'SEKT': 'sektör / makro', 'KRI': 'kripto', 'GOZ': "Cemal'in göz kuralları / kör test",
        'SIK': 'sıkışma / oynaklık', 'WEB': 'web hipotezleri (DS / DEVİR)', 'CET': 'cetvel / altyapı / denetim',
        'EVR': 'evren / mekanizma / veri', 'CIK': 'giriş-çıkış / portföy kuralı'}

KAR = {'IZD': 'İZ DEĞİL', 'OLC': 'ÖLÇÜLEMEDİ', 'EMA': 'EMARE', 'ADY': 'ADAY', 'KAP': 'KAPALI',
       'KYK': 'KARAR KAYITTA YOK', 'ALT': 'ALTYAPI / DENETİM (hipotez değil)', 'SIN': 'SINANMADI', 'IZ': 'İZ'}

# kod ; aile ; karar ; kisa ek
META = """
Ç01;CIK;KAP;
Ç02;CIK;KAP;
Ç03;CIK;KAP;
Ç04;SEK;ADY;eski 'TUTAN' (alt fitil<0,12, doji, dar hafta); doji col_ogren'de ayırmadı, yeniden doğrulanmadı
Ç05;SEKT;KAP;
Ç06;MOM;KAP;
Ç07;GOZ;ALT;göz kalibrasyonu (13/26 → 23/26)
Ç08;CET;ALT;
Ç09;SEK;KAP;
Ç10;SEK;ADY;AÇIK: bek +1,6, n 105
Ç11;SIK;IZD;
Ç12;SEK;IZD;sektör dalgası / genişlik / konum52 1,24-1,29 hafif iz
Ç13;CIK;IZD;zayıf (+1,0; 2026 −2,1)
Ç14;SEK;IZD;tutarsız
Ç15;OLA;ADY;eski 'GEÇERLİ' (ar60 −12/−6)
Ç16;HAC;ADY;eski 'GEÇERLİ' (ar60 −11/−15)
Ç17;HAC;ADY;eski 'GEÇERLİ' (ar60 −4,8/−4,7)
Ç18;OLA;ADY;eski 'GEÇERLİ' (ar60 −7/−8)
Ç19;SEKT;IZD;eski 'GEÇERLİ ama nötrden farkı küçük'; Ç71'de tek cetvelle İZ DEĞİL
Ç20;OLA;ADY;eski ADAY, n 26/46
Ç21;OLA;ADY;eski ADAY, n 29/20; sözleşme tutarı kap_ozet'te yok, puanlanamadı
Ç22;ICE;IZD;eski 'ÇÜRÜDÜ'; veri elde yok
Ç23;HAC;ADY;eski ADAY
Ç24;HAC;ADY;eski ADAY-zayıf
Ç25;HAC;ADY;eski ADAY-zayıf
Ç26;OLA;ADY;eski 'GEÇERLİ' (ar60 +4,9/+2,4)
Ç27;OLA;ADY;eski 'GEÇERLİ?'
Ç28;SEKT;IZD;eski 'ÇÜRÜDÜ' (tek hisse tekrarı)
Ç29;SEKT;ADY;eski 'GEÇERLİ' (sistem filtresi); tanım defterde tam yazılı değil
Ç30;SEKT;ADY;eski ADAY / REJİME BAĞLI; veri bu turda yok
Ç31;HAC;ADY;eski ADAY yön (B13 sonradan bilgi); olay dosyası yok
Ç32;OLA;OLC;test edilemez (hayatta kalma; çıkmış hisse verisi yok)
Ç33;SEK;IZD;eski 'ÇÜRÜDÜ / iz değil'
Ç34;HAC;IZD;
Ç35;SEK;IZD;tahtacı GEÇMEDİ
Ç36;SEK;IZD;
Ç37;SEK;IZD;14 Kas Ç181: D9 uzun çöl İZ DEĞİL; D9 + rüzgâr ÖLÇÜLEMEDİ
Ç38;SEK;ADY;eski BIST 'GEÇERLİ' risk; denetimde etkinin çoğu dipte olmaktan (B_dip 0,94 / 0,97 / 0,90)
Ç39;SEK;IZD;0,90-1,02
Ç40;GOZ;ALT;
Ç41;SEK;IZD;6 dönemin 3'ü
Ç42;CET;ALT;
Ç43;SEK;IZD;denetim: hiçbir şekil ölçüsü çölü ayırmıyor (AUC 0,37-0,60)
Ç44;SEK;IZD;eski 'ADAY yön'; denetimde yön izi de yok (mekanikti)
Ç45;CIK;IZD;portföy kuralı; T10 getiri dayanağı ters döndü
Ç46;CIK;IZD;üretim yolu içi ölçüm, BIST'e özgü
Ç47;SEK;IZD;'alım +12..26p' mekanikti
Ç48;GOZ;ALT;746 kutu gözle (%6 çöl)
Ç49;SEK;IZD;0,96-1,04
Ç50;SEK;IZD;
Ç51;SEK;IZD;kısa ufuk; 60 gün cetveli uygun değil
Ç52;SEKT;KYK;ölçüm, karar yazılmadı
Ç53;SEKT;KYK;ölçüm, karar yazılmadı
Ç54;HAC;KYK;ölçüm 117 olay, karar yazılmadı
Ç55;FON;IZD;
Ç56;SEK;IZD;
Ç57;SEK;IZD;ABD 2,45 / BIST 0,97
Ç58;MOM;IZD;LightGBM; BIST yok, ABD oynaklık
Ç59;MOM;IZD;yukarı hiçbiri 1,3 değil; 62 sinyalin olay dosyası saklanmadı
Ç60;HAC;IZD;eski 'ÇÜRÜDÜ' (eşli 0,91-1,73)
Ç61;OLA;IZD;eski 'ÇÜRÜDÜ' (eşli 1,14-1,17)
Ç62;OLA;IZD;eski 'ÇÜRÜDÜ' (eşli 1,02-1,14)
Ç63;CET;ALT;
Ç64;FON;ALT;betimleyici: fonlar koşu fazında giriyor
Ç65;FON;IZD;0,80-1,07
Ç66;FON;IZD;oynaklık
Ç67;SEK;IZD;
Ç68;SEK;IZD;BIST'te aşağı risk düşük
Ç69;SEK;ADY;gözlem: BIST 0,45-0,68, ABD yok
Ç70;HAC;IZD;'yeni deneme'; sonuç satırı yok (Ç175: ÖLÇÜLEMEDİ)
Ç71;SEKT;IZD;Ç19 notundan (tek cetvel)
Ç72;SEK;IZD;
Ç73;SEK;IZD;Ç76 sonucu İZ DEĞİL
Ç74;SEK;KYK;sonuç kayıtta yok
Ç75;SEK;IZD;Ç179 düzeltmesi: ABD ÖLÇÜLEMEDİ / TUTMADI
Ç76;SEK;IZD;
Ç77;SEK;IZD;
Ç78;SEK;IZD;Ç179 düzeltmesi: dip kümeleri PİYANGO
Ç79;SEK;IZD;ayırıcı değil (BIST 735'in 688'i düzgün dipli)
Ç80;SEK;IZD;
Ç81;SEK;KYK;sonuç kayıtta yok (tur 2)
Ç82;SEK;KYK;önce −%20 BIST 0,51-0,71 ama tek cetvelde ters kat; karar yazılmadı
Ç83;SEK;KYK;sonuç kayıtta yok (tur 2)
Ç84;CET;ALT;6 bağımsız denetçi, ~30 ölçüm hatası
Ç85;GOZ;IZD;profil ayırmıyor (7/9 koşan, 2/3 koşmayan profilde)
Ç86;GOZ;IZD;
Ç87;GOZ;KYK;sonuç kayıtta yok (Ç175: ÖLÇÜLEMEDİ)
Ç88;GOZ;IZD;
Ç89;GOZ;IZD;BIST 2023 0,86 (n 25); oynak hisse
Ç90;GOZ;KYK;sonuç kayıtta yok (Ç175: ÖLÇÜLEMEDİ)
Ç91;CIK;IZD;12 hücrenin hiçbiri eşli hisseden üstün değil
Ç92;SEK;IZD;hiçbir sinyal dört hücrede geçmedi
Ç93;SEK;IZD;sıra 0,45-0,53
Ç94;SEK;IZD;fark atılım mumunda (sonradan bilinen)
Ç95;GOZ;IZD;göz izi değil (v4: ✓ %54, ✗ %57, havuz %60)
Ç96;SEK;IZD;tarif eşliden iyi değil (ABD); BIST n küçük hücreler Ç175'e göre ölçülemedi
Ç97;FON;IZD;fon payı çölle ilişkili değil
Ç98;SEK;IZD;profil 1,02
Ç99;ICE;IZD;KAP net alım BIST −%4,5 / −%2,6
Ç100;TEM;IZD;hiçbiri dört hücrede tutmadı
Ç101;TEM;IZD;
Ç102;ICE;IZD;çölde alım ABD 2023 dört şart tuttu, 2024-26 tutmadı, örneklem dışı güçlenmedi
Ç103;ICE;IZD;
Ç104;CIK;ALT;düzen ölçümü (iz testi değil)
Ç105;MOM;IZD;sıçrayan hisse profili: asimetrik özellik yok
Ç106;TEM;IZD;ABD-ADAY GEÇERSİZ (hayatta kalma yanlılığı)
Ç107;TEM;IZD;batanlar dahil; 2024-26 sıra 0,48
Ç108;SEKT;IZD;AYIRMIYOR (iki kohort)
Ç109;SEKT;IZD;AYIRMIYOR
Ç110;SEKT;IZD;sebep önce gelmiyor
Ç111;SEKT;IZD;
Ç112;HAC;IZD;blok taban ABD 2024-26 dört şart tutar, 2023 tutmaz
Ç113;SEK;IZD;
Ç114;SEKT;IZD;
Ç115;SEKT;IZD;boşluk +%0,23 üç dönemde aralık artı; gün içi yalnız 2023
Ç116;MOM;IZD;sekizi de; ABD Fibonacci ortalama artı, sıra 0,52 / 0,50
Ç117;SEKT;IZD;
Ç118;TEM;IZD;
Ç119;SEKT;IZD;AVR kalıntı dört hücrenin ikisi; sağlam değil, bilgi
Ç120;CET;ALT;ölçüm hattı kontrolü
Ç121;CET;ALT;bilinen etkiler kıyası
Ç122;MOM;IZD;alınabilir iz yok; küçüklük ADAY (hayatta kalma)
Ç123;SEK;IZD;INTEM izi; piyasayı geçmiyor
Ç124;SEK;EMA;sıkışma ailesindeki tek EMARE; ileri testte ÖLÇÜLEMEDİ (Ç180)
Ç125;MOM;IZD;ABD 2023 +3,6 eşiğin altında
Ç126;SEK;IZD;
Ç127;MOM;IZD;
Ç128;MOM;IZD;ABD 2023 +6,9 (eşik 10) altında; AVR +10,8 / +11,3
Ç129;MOM;IZD;AVR +1,7 / +0,6
Ç130;MOM;IZD;pazar izi üç pazarda 0
Ç131;MOM;IZD;üç pazarda portföy piyasanın altı
Ç132;SEK;IZD;P1 +2,5 / +2,4 puan (eşik 5)
Ç133;SEK;IZD;
Ç134;CET;IZD;beş hipotezin beşi desteklenmiyor
Ç135;TEM;IZD;analist revizyonu ek bilgi katmıyor
Ç136;TEM;IZD;T1 / T5 / T6 hiçbiri desteklenmiyor
Ç137;EVR;ALT;evren sağlamlık denetimi
Ç138;EVR;IZD;K55 keşif taraması (iz yok)
Ç139;EVR;ALT;mekanizma envanteri
Ç140;EVR;IZD;gerçek etki 0 / 125
Ç141;EVR;IZD;gerçek etki 0 / 125
Ç142;EVR;ALT;evren v2 hazırlığı
Ç143;EVR;ALT;
Ç144;EVR;ALT;PBO / DSR
Ç145;EVR;ALT;
Ç146;EVR;IZD;K55 NİHAİ: İZ YOK
Ç147;KRI;IZD;
Ç148;TEM;IZD;YEOTK profili V1-V3
Ç149;TEM;IZD;
Ç150;TEM;IZD;
Ç151;CET;ALT;K58 cetvel sağlaması
Ç152;MOM;IZD;K59 TUTMAZ
Ç153;MOM;IZD;TUTMAZ; (b) cetvel GÜVENİLMEZ
Ç154;MOM;IZD;K60: iz adayı yok; asimetrik fırsat yok; güvenli uç COMP4 / DOSYA_Y (bilgi)
Ç155;MOM;EMA;BİLGİ düzeyi: 2 koşullu fırsat (BETA_BAB ALT, NDF_BS ALT) + 8 koruma; yalnız ABD, yalnız yaşayanlar
Ç156;TEM;IZD;22 değişken-yönün hepsi
Ç157;EVR;ALT;veri erişim araştırması
Ç158;TEM;IZD;makale yeniden üretildi; alınabilir bacak tutmadı
Ç159;ICE;IZD;8 değişken-yön
Ç160;TEM;IZD;4 değişken-yön
Ç161;TEM;IZD;16 değişken-yön
Ç162;SIK;IZD;Ç175: ABD İZ DEĞİL, BIST ÖLÇÜLEMEDİ
Ç163;SIK;IZD;Ç175: 'bölgeyi bulmak başarılı' tanımsal; ABD İZ DEĞİL, BIST ÖLÇÜLEMEDİ
Ç164;SIK;IZD;mutlak harekette başarısız; BIST olay 6 / 12 ÖLÇÜLEMEDİ
Ç165;CET;ALT;Tiingo batan doğrulama pilotu (7 / 12 KISMEN)
Ç166;GOZ;OLC;İŞARET YOK = VERİ YETERSİZ (işaretli grafik < 8)
Ç167;GOZ;IZD;G5 Cemal'in çöllerinin 1/29'unu yakalıyor
Ç168;HAC;IZD;
Ç169;HAC;IZD;ana n 11
Ç170;OLA;EMA;tek olay (çöküş), q 0,003
Ç171;FON;IZD;BofA AKD alım listesi; güç yeterli
Ç172;FON;IZD;YOL YOK (BIST-ADAY ancak)
Ç173a;FON;OLC;BofA dipte yolu ölçülemez (kriz öncesi olay 0)
Ç173b;SEK;IZD;−%80 dip kurulumu: ABD 2023 TUTTU +%24,8, 2024-26 sıra tutmadı; piyango
Ç174;SIK;IZD;güç yeterli, eğilim TERS
Ç175;CET;ALT;VDYT denetimi + eski çöl yeniden etiketleme
Ç176;SIK;ALT;S1 duyarlılığı (bilgi)
Ç177;CET;ALT;ORTAK CETVEL v1.0
Ç178;SEK;OLC;K24 iki evre çöl
Ç179;SEK;OLC;dip + çöl ayrımı
Ç180;SEK;OLC;INTEM ileri test; EMARE desteklenmedi, iddia kapanmadı
Ç181a;SEK;IZD;D9 uzun çöl; güç yeterli
Ç181b;SEKT;OLC;D9 + rüzgâr (T8)
Ç181c;SEKT;EMA;yalnız sektör rüzgârı ABD; portföy şartı tutmadı, AVR ölçülemez
Ç182a;SEK;EMA;P1 büyük mumdan önceki profil
Ç182b;SEK;EMA;H1 çok günlü büyük hareket öncesi profil
Ç183;SIK;OLC;S4 Cemal tanımlı sıkışma
Ç184;SIK;EMA;S5 DİP öbek sıkışması (ABD büyük gün 1,14-1,17 kat)
Ç185;SEKT;OLC;rüzgâr Avrupa'da
Ç186;SEKT;OLC;çöküş sonrası oynak hisse; tamamlanmış çöküş 1 < 2
Ç187;SEK;OLC;fitil öbeği; 2024-26 hücreleri TUTMADI, 2023 güç %52
Ç188;SEK;ALT;fitil öbeği hata nerede (tanım bağlamı)
Ç189;SEK;OLC;S+ v2
Ç190;SEK;OLC;Y1-Y5, 15 bar
Ç191;SEK;OLC;Y6 / Y8; yön aleyhte
Ç192;GOZ;OLC;göz skoru; yön ters
Ç193;SEK;OLC;Y9 dipte S6 (bakılmış ABD KAT5 1,15 / 1,21)
Ç194;SEK;OLC;S7 / Y10
Ç195;SEK;OLC;Ş9 U dip / Y11
Ç196;SEK;OLC;G2 dip vs G1 trend içi raf
Ç197;MOM;OLC;F1-F29 puan üst %20
Ç198;WEB;OLC;devir 1 (F30-F42)
Ç199;WEB;OLC;devir 2
Ç200;WEB;OLC;devir 3
Ç201;SEK;OLC;Ş10 MACD pozitif uyumsuzluk
Ç202;WEB;OLC;DS 25 / 25 ÖLÇÜLEMEDİ
Ç203;CET;ALT;pozitif kontrol
Ç204;CET;ALT;CETVEL2 (R15) pozitif kontrol v2 + Ç194-Ç202 yeniden koşusu (124 hipotez)
"""

# Ç175'in 'ÖLÇÜLEMEDİ' diye yeniden etiketlediği eski çöl kayıtları ve 'İZ DEĞİL'i hak eden gövde
C175_OLC = ['Ç38', 'Ç39', 'Ç50', 'Ç57', 'Ç67', 'Ç68', 'Ç69', 'Ç70'] + ['Ç%d' % i for i in range(73, 84)] + ['Ç87', 'Ç89', 'Ç90']
C175_HAK = ['Ç34', 'Ç41', 'Ç44', 'Ç47', 'Ç49', 'Ç56', 'Ç72', 'Ç85', 'Ç86', 'Ç88', 'Ç91', 'Ç93', 'Ç96', 'Ç104', 'Ç132', 'Ç134', 'Ç156']
# Güçlü kararlar (A): kayıtta güç yeterli / cetvel güvenilir yazılı
A_KOD = {'Ç171': 'n 1.789 güç yeterli', 'Ç174': 'n 1.266-9.540 güç yeterli', 'Ç181a': 'n 1.102-4.556 güç yeterli',
         'Ç152': 'cetvel v2 GÜVENİLİR', 'Ç154': 'cetvel v2 GÜVENİLİR (yalnız yaşayanlar)',
         'Ç155': 'cetvel v2 (yalnız yaşayanlar)', 'Ç153': 'cetvel (a) GÜVENİLİR, (b) GÜVENİLMEZ',
         'Ç158': '5.430 olay, makale yeniden üretildi', 'Ç116': 'on binlerce olay',
         'Ç159': 'cetvel v2 (çöl içi n kayıtta yok)', 'Ç160': 'cetvel v2 (çöl içi n kayıtta yok)',
         'Ç161': '35.698 olay'}
# Hata defterinde bu çalışmaya bağlanan notlar (kayıt metninde 'DÜZELTME' ya da 'Denetim 24 Eki' geçenler otomatik eklenir)

def aralik(a, b):
    return ['Ç%d' % i for i in range(a, b + 1)]


def kod_say(k):
    m = re.match(r'Ç(\d+)', k)
    return int(m.group(1)) if m else 0


def cetvel(k):
    n = kod_say(k)
    if k in ('Ç154', 'Ç155', 'Ç152', 'Ç153'):
        return 'portföy cetveli v2 + olasılık tablosu (12 ay +%100 / −%50 katı; K59 / K60)'
    if n <= 98:
        if k in ('Ç76', 'Ç77', 'Ç78', 'Ç80', 'Ç85', 'Ç89', 'Ç72'):
            return 'eski tek cetvel + eşli kutu (önce +%20 oranı ≥ 1,3 kat)'
        if n in (7, 40, 42, 43, 48):
            return 'göz kalibrasyonu / araç'
        return 'eski tek cetvel (önce +%20 oranı ≥ 1,3 kat; ar60)'
    if n <= 123 or n in (156, 157, 158, 159, 160, 161):
        return 'FI_OLCUT 60 gün eşli (dört şart)'
    if n == 104:
        return 'portföy düzeni (iz testi değil)'
    if n <= 131:
        return 'diğer: +%8 önce kısa ufuk (20 gün, oynaklık eşli) / makine (h5 akrabası)'
    if n <= 146:
        return 'diğer: K51-K56 akademik (isabet farkı / Δ puan, ay kümeli bootstrap; mekanizma)'
    if n == 147:
        return 'diğer: kripto olay ölçüsü (eşli taban yok)'
    if n in (148, 149, 150):
        return 'FI_OLCUT 60 gün eşli (dört şart)'
    if n == 151:
        return 'FI_OLCUT güç + portföy cetveli kalibrasyonu'
    if n in (162, 163, 164, 165, 175):
        return 'diğer: VDYT (Brier skill, büyük hareket olasılığı)'
    if n in (166, 167):
        return 'göz-etiket (kör test)'
    if n in (168, 169, 170):
        return 'FI_OLCUT 60 gün eşli (dört şart) / geniş kesit'
    if n in (171, 172, 173):
        return 'FI_OLCUT 60 gün eşli (dört şart) + 250 gün olasılık'
    if n in (174, 176):
        return 'diğer: S1 KAT (20 gün büyük gün, oynaklık eşli)'
    if n in (177, 178, 179, 180, 181, 182, 183, 184, 185, 186):
        return 'ORTAK_CETVEL v1.0 (60 gün eşli + 250 gün olasılık)'
    if n in (187, 188, 189):
        return 'ORTAK_CETVEL v1.0 (60 gün r60)'
    if 194 <= n <= 202:
        return "15 bar h5 (+%5 / +%10 stop'tan önce, eş ATRP × likidite); Ç204'te CETVEL2 R15 (stop'suz) ile yeniden koşuldu"
    if 190 <= n <= 193:
        return '15 bar h5 (+%5 / +%10 stop\'tan önce, eş ATRP × likidite)'
    if n == 204:
        return "CETVEL2 R15 (15. geçerli bar kapanışı / t+1 açılış − 1, stop yok; eş = ATRP × likidite × F15 çeyreği)"
    if n == 203:
        return 'pozitif kontrol (h5 + r15 + r60 yan yana)'
    return 'diğer'


def veri_elde(k, aile):
    n = kod_say(k)
    if k in ('Ç21', 'Ç22', 'Ç30', 'Ç31', 'Ç32'):
        return 'YOK (kayıt: veri / olay dosyası yok)'
    if k in ('Ç107', 'Ç142', 'Ç165'):
        return 'İNDİR (Tiingo; lisans gereği repoya konmaz)'
    if k == 'Ç147':
        return 'İNDİR (Binance / OKX)'
    if aile == 'ICE' and n in (102, 103, 159):
        return 'EVET (SEC Form 4 / FINRA; fi_k30_indir ile yeniden iner)'
    if aile == 'FON' or n in (99, 64):
        return 'EVET (kapfon-veri dalı / BofA arşivi; git dışı)'
    if aile == 'TEM':
        return 'EVET (KAP / SEC secfs; islenmis-veri dalı)'
    if n in (166, 167, 192):
        return 'EVET (grafik); Cemal etiketi sınırlı'
    return 'EVET (V_BIST / V_ABD / V_AVR; islenmis-veri dalı)'


def t_bilinir(k, aile, karar):
    n = kod_say(k)
    if karar == 'ALT':
        return '-'
    if aile == 'GOZ':
        return 'HAYIR (Cemal gözü; sayısal karşılığı vekil)'
    if k in ('Ç75', 'Ç78'):
        return 'HAYIR → düzeltildi (n < 400 uzunluk şartı geleceğe bakıyordu, Ç179)'
    if n >= 99 or k.startswith('Ç17') or k.startswith('Ç18'):
        return 'EVET (ön kayıtlı sabit eşik; kayıt: karar önceden)'
    if n >= 85:
        return 'KISMEN (karar önceden yazılı; sayısal tanım kayıtta yok)'
    return 'KAYITTA YOK'


def kasa_adayi(k, aile, karar, guv, veri, tb):
    if karar == 'ALT':
        return 'HAYIR: hipotez değil (altyapı / denetim)'
    if karar == 'KAP' or aile == 'CIK':
        return 'HAYIR: kapalı konu (COL_OZET: giriş / çıkış / filtre)'
    if veri.startswith('YOK'):
        return 'HAYIR: veri yok'
    if karar == 'KYK':
        return 'HAYIR: sonuç kayıtta yok (önce sonuç dosyası bulunmalı)'
    if aile == 'GOZ':
        return "HAYIR: Cemal gözü; kasa fiyat bloğu değil, kör etiket gerekir"
    if aile in ('KRI', 'EVR'):
        return 'HAYIR: kripto kapandı / mekanizma işi'
    if aile in ('TEM', 'ICE', 'FON', 'OLA'):
        return 'HAYIR (şimdilik): olay / temel verisi kasa bloğunda yok (yalnız fiyat-hacim); ayrı kasa gerekir'
    if guv.startswith('A') and karar == 'IZD':
        return 'HAYIR: zaten A (güç yeterli İZ DEĞİL)'
    if aile == 'SEKT':
        return 'HAYIR (şimdilik): sektör ısısı kapalı konu; Cemal kararı gerekir'
    if tb.startswith('KAYITTA YOK') or tb.startswith('HAYIR'):
        return 'HAYIR: t\'de bilinir sayısal tanım yok / eski cetvel'
    return 'EVET: fiyat-hacim, sayısal tanım ve eşik kayıtlı'


def kayit_cek():
    d = {}
    for k in IK.IK_KAYIT:
        d[k['kod']] = k
    return d


def hata_haritasi():
    """IK_HATA satırlarını 'kayit' + 'etki' alanındaki Ç numaralarına bağlar (aralıklar açılır)."""
    h = collections.defaultdict(list)
    for r in IK.IK_HATA:
        s = (r.get('kayit', '') or '') + ' ' + (r.get('etki', '') or '')
        kodlar = set()
        for m in re.finditer(r'Ç(\d+)\s*[-–]\s*Ç?(\d+)', s):
            a, b = int(m.group(1)), int(m.group(2))
            if 0 < b - a <= 40:
                kodlar.update('Ç%d' % i for i in range(a, b + 1))
        for m in re.finditer(r'Ç(\d+)', s):
            kodlar.add('Ç%d' % int(m.group(1)))
        for c in kodlar:
            h[c].append(r)
    return h


def kisalt(s, n):
    s = re.sub(r'\s+', ' ', str(s)).strip().replace('|', '/')
    return s if len(s) <= n else s[:n - 1].rstrip() + '…'


def n_cek(k):
    s = k['not'] + ' ' + k['eski']
    bulunan = re.findall(r'\bn(?:\s*[=≥<]\s*|\s+)(\d[\d\.]*(?:\s*/\s*\d[\d\.]*)*)', s)
    if not bulunan:
        return 'kayıtta yok'
    # Türkçe binlik noktası: 1.789 -> sayı
    ilk = bulunan[:3]
    return 'n ' + '; '.join(ilk)


def max_n(k):
    s = k['not'] + ' ' + k['eski']
    sayilar = []
    for g in re.findall(r'\bn(?:\s*[=≥<]\s*|\s+)(\d[\d\.]*(?:\s*/\s*\d[\d\.]*)*)', s):
        for x in re.findall(r'\d[\d\.]*', g):
            try:
                sayilar.append(int(x.replace('.', '')))
            except ValueError:
                pass
    return max(sayilar) if sayilar else None


def pazar_donem(k):
    s = k['not'] + ' ' + k['eski'] + ' ' + k['ad']
    p = [x for x in ('ABD', 'AVR', 'BIST', 'kripto') if (x in s or (x == 'AVR' and 'Avrupa' in s))]
    d = [x for x in ('2016-22', '2023', '2024-26', '2022-26', '2017-21') if x in s]
    return (', '.join(p) if p else 'kayıtta yok') + '; ' + (', '.join(d) if d else 'dönem kayıtta yok')


def guvenilirlik(k, aile, karar, n, hata):
    h = []
    if karar == 'ALT':
        return '-', ''
    num = kod_say(k)
    ek = []
    if k in A_KOD:
        h.append('A'); ek.append('A: ' + A_KOD[k])
    elif k in C175_HAK:
        h.append('A'); ek.append('A: Ç175 "İZ DEĞİL\'i hak eden gövde"')
    elif k in C175_OLC:
        h.append('B'); ek.append('B: Ç175 ÖLÇÜLEMEDİ olarak yeniden etiketledi')
    if not h:
        if 190 <= num <= 202:
            h.append('C'); h.append('B'); ek.append('C: h5 cetveli (Ç203 oynaklık kusuru); B: karar hücreleri n < 1.000 / güç < %80')
        elif 124 <= num <= 131:
            h.append('C'); ek.append("C: '+%8 önce' hedef-önce cetveli (Ç124: ilk koşuda oynaklık karışımı; Ç203 h5 kusuruyla akraba)")
            if num == 124:
                h.append('B')
        elif karar == 'OLC' or (n is not None and n < 1000) or n is None:
            h.append('B')
            if n is None:
                ek.append('B*: kayıtta n yok, güç bilinmiyor')
            elif n < 1000:
                ek.append('B: kayıtta yazılı en büyük n %d (< 1.000; kayıtta bütün hücre n\'leri yok)' % n)
            else:
                ek.append('B: karar ÖLÇÜLEMEDİ')
            if 99 <= num <= 151:
                ek.append('K58: FI_OLCUT n < 1.000 hücrede küçük etkiyi görmez')
        else:
            h.append('A?'); ek.append('A?: en büyük kayıtlı n ≥ 1.000, hücre bazı doğrulanmadı')
    if hata:
        h.append('D')
        ek.append('D: ' + kisalt(hata[0]['hata'], 95) + (' (+%d satır)' % (len(hata) - 1) if len(hata) > 1 else ''))
    return ' + '.join(h), ' | '.join(ek)


def satirlari_kur():
    global YKPER
    YKPER, _yk = yk_tablosu()
    kayit = kayit_cek()
    hmap = hata_haritasi()
    satirlar = []
    for ln in META.strip().split('\n'):
        kod, aile, kar, ek = [x.strip() for x in ln.split(';', 3)]
        ana = re.match(r'(Ç\d+)', kod).group(1)
        k = kayit[ana]
        n = max_n(k)
        hata = list(hmap.get(ana, []))
        # kayıt notunda düzeltme geçiyorsa D (hata satırı yoksa da)
        dnot = re.search(r'DÜZELTME|Denetim 24 Eki|hata vardı|yanlıştı', k['not'])
        guv, gek = guvenilirlik(kod, aile, kar, n, hata)
        if dnot and 'D' not in guv and guv != '-':
            guv += ' + D'
            gek += ' | D: kayıt notunda düzeltme / denetim bulgusu var'
        veri = veri_elde(kod, aile)
        tb = t_bilinir(kod, aile, kar)
        karar_s = KAR[kar]
        num = kod_say(ana)
        if 194 <= num <= 202 and ana in YKPER:
            cs = ', '.join('%s %d' % (a_, b_) for a_, b_ in YKPER[ana].items())
            karar_s = 'ÖLÇÜLEMEDİ (h5) → Ç204 CETVEL2 R15 yeniden koşu: ' + cs
            guv = 'A / B (CETVEL2 R15)' + (' + D' if 'D' in guv.split(' + ') else '')
            gek = ("h5 etiketi Ç204'te yeniden koşuldu (R15 etiketleri: %s); Ç204 kaydı: güç ≥ 0,80 dört hücrede olup hiçbir hücresi tutmayan hipotezler "
                   "(52 kod) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü etki için)', güçsüz hücreler ÖLÇÜLEMEDİ; A = güç ≥ 0,80 hücreler, B = güçsüzler" % cs) + (' | ' + gek if 'D:' in gek else '')
        if ana in C175_OLC and kar == 'IZD':
            karar_s = 'ÖLÇÜLEMEDİ (kayıtta İZ DEĞİL; Ç175 yeniden etiketledi)'
        if kar == 'IZD' and ana in ('Ç162', 'Ç163', 'Ç164'):
            karar_s = 'İZ DEĞİL (ABD; BIST ÖLÇÜLEMEDİ)'
        kasa = kasa_adayi(kod, aile, kar, guv, veri, tb)
        if ana in C175_OLC:
            kasa = kasa.replace('HAYIR: t\'de bilinir sayısal tanım yok / eski cetvel', 'HAYIR: t\'de bilinir sayısal tanım yok / eski cetvel (B)')
        satirlar.append(dict(kod=kod, ana=ana, tarih=k['tarih'], aile=aile, hip=kisalt(k['ad'], 110) + ' — ' + kisalt(k['soru'], 110),
                             cet=cetvel(ana), pd=pazar_donem(k), n=n_cek(k), karar=karar_s, kar=kar,
                             sayi=kisalt(ek if ek else (k['not'][:150] if k['not'] else k['eski']), 170), guv=guv, gek=gek, veri=veri, tb=tb, kasa=kasa,
                             ad=k['ad']))
    return satirlar, kayit


def yk_tablosu():
    """cetvel2/YENIDEN_KOSU.md bölüm 4 (yalnız okunur): Ç194-Ç202 hipotezlerinin CETVEL2 R15 etiketi."""
    yol = os.path.join(AC, 'cetvel2', 'YENIDEN_KOSU.md')
    if not os.path.exists(yol):
        return {}, {}
    t = open(yol, encoding='utf-8').read()
    a = t.index('## 4. ETİKET TABLOSU'); b = t.index('## 5. YENİDEN ÜRETİM')
    per = collections.defaultdict(collections.Counter)
    kod = {}
    for ln in t[a:b].split('\n'):
        if ln.startswith('| C'):
            c = [x.strip() for x in ln.strip().strip('|').split('|')]
            if len(c) >= 10:
                kk = 'Ç' + c[0][1:]
                per[kk][c[8]] += 1
                kod[(kk, c[1])] = (c[8], c[5])
    return per, kod


def ds_tablosu():
    t = open(os.path.join(AC, 'dusus_sonrasi', 'DS_ELESTIRI.md'), encoding='utf-8').read()
    a = t.index('## 1.'); b = t.index('## 2.')
    rows = re.findall(r'^\| (DS\d+) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$', t[a:b], re.M)
    r2 = open(os.path.join(AC, 'dusus_sonrasi', 'DS_RAPOR.md'), encoding='utf-8').read()
    olculen = {}
    for m in re.finditer(r'^\| (DS\d+) \| ABD \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$', r2, re.M):
        olculen[m.group(1)] = dict(egit=m.group(2), sin=m.group(3), boot=m.group(4), guc=m.group(5), etiket=m.group(8).replace('*', ''))
    return rows, olculen


def k60_tablosu():
    t = open(os.path.join(AC, 'k60_kutuphane', 'olasilik_tablosu.md'), encoding='utf-8').read()
    kay = {}
    for ln in t.split('\n'):
        m = re.match(r'^\| ([A-Za-z0-9_]+) \((ÜST|ALT)\)(?: — [^|]*)? \| (KEŞİF|DOĞRULAMA|KASA) \| (\d+) \| (%[\d,]+) \| (%[\d,]+) \| ([\d,]+) \[[^\]]*\] \| (%[\d,]+) \| (%[\d,]+) \| ([\d,]+) \[[^\]]*\] \|.*\| (.*) \|$', ln)
        if m:
            kay.setdefault((m.group(1), m.group(2)), {})[m.group(3)] = (m.group(7), m.group(10), m.group(11))
        else:
            m2 = re.match(r'^\| ([A-Za-z0-9_]+) \((ÜST|ALT)\) \| (DOĞRULAMA|KASA) \| (\d+) \| (%[\d,]+) \| (%[\d,]+) \| ([\d,]+) \[[^\]]*\] \| (%[\d,]+) \| (%[\d,]+) \| ([\d,]+) \[', ln)
            if m2:
                kay.setdefault((m2.group(1), m2.group(2)), {})[m2.group(3)] = (m2.group(7), m2.group(10), '')
    return kay


def kural_tablolari():
    t = open(os.path.join(AC, 'kural_defteri', 'KURAL_DEFTERI_TASLAK.md'), encoding='utf-8').read()
    a = t.index('### A. '); b = t.index('### K. ')
    ust = []
    for ln in t[a:b].split('\n'):
        m = re.match(r'^\| ([A-J]\d+) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$', ln)
        if m:
            ust.append(m.groups())
    c = t.index('### K. '); d = t.index('## 3. ')
    kk = []
    for ln in t[c:d].split('\n'):
        m = re.match(r'^\| (K\d+) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$', ln)
        if m:
            kk.append(m.groups())
    return ust, kk


# ----------------------------------------------------------------------------------------------
# Cemal'in göz kuralları C1-C13 ve CD / VD dersleri (GOZ_ETIKET_IS_TANIMI.md, HAKEM_DERSLER.md)
C_KURAL = [
 ('C1', 'Taban net: hat ≥ 3 dokunuş, aynı seviye, eğim aşağı değil; 1-2 mumluk hat = OLMAZ', 'F1 (hat dokunuş), Y6 / Ş2', 'Ç191 (Y6 / Y8, 15 bar h5): ölçülemedi, yön aleyhte (KAT5 0,59-0,90)', 'B + C'),
 ('C2', 'Dip savunulmuş: alçalan dipler zinciri yok', 'S6 dip şartı, F15, Y9, Y11', 'Ç193 (Y9): ölçülemedi; bakılmış ABD KAT5 1,15 / 1,21', 'B + C'),
 ('C3', 'Mumlar küçük (fitil dahil, öncesine göre)', 'MUM_OLCU aralik; S5 / S4 eşikleri', 'Ç174 (S1) İZ DEĞİL güç yeterli; Ç183 ölçülemedi; Ç184 EMARE', 'A (S1) / B'),
 ('C4', 'Mum şekli: alt fitil kısa, açılış dibe yakın, üst fitil biraz uzun', 'FITIL_OBEK ASİM ≥ 0,20, fitilsiz payı ≥ 0,50, k = 10', 'Ç187: ölçülemedi (2024-26 TUTMADI); Ç189', 'B'),
 ('C5', 'Kırılım mumu belirgin (kapanış tavanı net aşmış, gövdeli)', 'Y6 gerçek kırılım: kapanış > tavan × 1,01 ve gövde ≥ bölge medyanı', 'Ç191: ölçülemedi', 'B + C'),
 ('C6', 'Büyük desen: 120-250 bar alçalan kanal ise küçük taban OLMAZ', 'Y6 büyük desen şartı', 'Ç191: ölçülemedi; vekil etiket VD2 / VD3', 'B + C'),
 ('C7', 'Yapı boyu düşüşe göre yeterli', 'S6 nMin, FITIL_V2 10 bar sabit', 'ölçülmedi (K7)', 'E'),
 ('C8', 'Kağıt hafızası: önceki yapı patladıysa OLMAZ', 'Y4 / Y8 (farklı tanım)', 'Ç190: Y4 Y1\'i iyileştirmiyor (AVR aleyhte)', 'B + C'),
 ('C9', 'Kubbe: kazan OLUR, şemsiye OLMAZ; dönüş görülmeden BELİRSİZ', 'Ş9 U dip (a > 0, çanak, R²)', 'Ç195: Y11 n 1-20 ölçülemedi; Y11c KAT5 ~1', 'B + C'),
 ('C10', 'Yol almış: tabandan uzaklaşmışsa kovalama yok', 'FITIL_V2 yol şartı', 'Ç189 içinde (ölçülemedi)', 'B'),
 ('C11', 'Stop uzaklığı: kapanış hattan %10\'dan uzaksa işlem yok', 'stop0 = hat × 0,98; Y1 stop ≤ %10', 'vekil etiket: hedefe gidenleri eliyor (VD2); ölçüt dar stop sorunu CD20', 'D (vekil dersi)'),
 ('C12', 'Çekiştirme / oluşum yok = BELİRSİZ', '-', 'sinyal değil etiket', 'E'),
 ('C13', 'Dev tek mum / şüphe: geçmişte dev mum = riskli', 'K12 / J4 (kodda YOK)', 'ölçülmedi', 'E'),
]
CD_VD = [
 ('CD1', 'Fitil teorisi bağlamsız yön vermez', 'HAKEM: iki sayfada iki yönde yanıldı', 'SINANMADI', 'E'),
 ('CD2', 'Tepede raf OLMAZ / BELİRSİZ', 'Y9c (tepede) ters', 'Ç193 (Y9c) ölçülemedi', 'B + C'),
 ('CD3', 'Kazan çizmek yetmez; sağ kenar dönmeli', 'Ş9 / C9', 'Ç195 ölçülemedi', 'B + C'),
 ('CD5', 'En güzel taban stop olabilir (şekil güzelliği garanti değil)', 'Ş9 R² uyumu', 'CD23: R² 0,9+ gitti 3, stop 4 / 7', 'SINANMADI'),
 ('CD6 / CD7', 'Eleme ve teyit refleksleri karışık: tavana değiyor elemesi yanılttı, iki gün teyit korudu', 'AL_PAY, 2 gün teyit (kapalı konu \'giriş onayı\')', 'SINANMADI', 'E / KAPALI'),
 ('CD8 / CD9', 'Kodun bölgesi yanlış ile fiyat gitmez ayrı hükümler', '-', 'SINANMADI (süreç)', 'E'),
 ('CD15', 'Kod iki aday bölgeden kötüsünü seçmişse OLMAZ (mahkeme: ÖNCEKİ BÖLGE DAHA UYGUN)', 'mahkeme kuralı (TUR 4)', 'SINANMADI; TUR 4: 5 / 5 gelmedi', 'E'),
 ('CD16', "'Zaman / haber ister' = DOSYA GEREKLİ (kör sette ölçülemez)", 'dosya bilgisi (K57)', 'puana girmez', 'E'),
 ('CD17', 'Önceki toparlanma sert / hızlıysa bu da hızlı olur (C8)', 'önceki yükseliş hızı', 'TUR 4: 2 / 4', 'SINANMADI'),
 ('CD20', 'Hat × 0,98 stopu U dip havuzunda dar', 'stop eşiği', 'TUR 4: 4 / 9 yanlış stop; Ç203: ARRY, JBLU, CAPR (ikinci bağımsız olay)', 'C'),
 ('CD21', "'Önceki kazan bitmedi / ikinci kazan daha derin' OLMAZ gerekçeleri 4 / 4 yanılttı", '-', 'TUR 4 ters emare', 'SINANMADI'),
 ('CD22', 'Sert düşüş sonrası hemen toparlanma beklenmez tezi 3 / 3 ters', 'dd ≤ −%50', 'TUR 6', 'SINANMADI'),
 ('CD23', 'Çanak uyumu iyi ('+"R² 0,9+"+') tek başına ayırmadı', 'Ş9 R²', 'TUR 6: İYİ 13 sayfanın 6\'sı gitti (%46 = taban)', 'SINANMADI'),
 ('VD1', 'Kuralların toplamı Cemal\'in gözü değil (OLUR 6 sayfanın hiçbiri gitmedi)', 'GOZ_ETIKET C1-C13 toplamı', 'Ç192: vekil OLUR 6 / 300', 'C + D'),
 ('VD2', 'Stop %10 ve kırılım payı süzgeçleri hedefe gidenleri eliyor', 'C11, C5', 'Ç192; Ç191', 'C + D'),
 ('VD3', 'Vekilin BELİRSİZ grubu en iyi grup', '-', 'TUR 1-2', 'SINANMADI'),
 ('VD4', 'Önce hakem sonra eğitim', 'süreç', 'Ç192 hata satırı', 'süreç'),
 ('VD6-VD8', 'Dipte kazan OLUR için dönüş + gövdeli kırılım; tepe rafı iki tür', 'TUR 2 model kuralı', 'SINANMADI', 'E'),
 ('VD9 / VD10', 'OLUR için iki şart (dönüş + gövdeli ortalayan kırılım); büyük resim yükselen şartı dipte uygulanmaz', 'TUR 3-5 model kuralı', 'TUR 2: model OLUR isabeti %48 = taban', 'SINANMADI'),
 ('VD11', 'TUR 6 modeli \'hep OLMAZ\' ile aynı (%52,5)', '-', 'TUR 6', 'SINANMADI'),
]

# 25 KASA KART TASLAGI (oncelik sirasi; yeni esik uydurulmadi: kayittaki esik ya da 'ana model sabitleyecek')
CK = 'FI_OLCUT dört şart (n ≥ 30; eşli fark > 0 ve ay kümeli alt uç > 0; sıra > 0,50; portföy > rastgele p90) + n ≥ 1.000 / güç ≥ %80 (K58 / Ç175)'
OLCU = 'ölçü: karar için stop\'suz r15 eşli fark + r60 (Ç203 öneri 1); h5 yalnız bilgi (Ç203); plasebo sapması sıfırlanmadan AVR karar vermez (Ç203 öneri 2)'
KARTLAR = [
 ('KK01', 'Ç187 / K30', 'Son 10 barda üst fitili uzun, alt fitili kısa mum öbeği (S+) görülürse sonraki 15 barda eşlerinden daha çok yükselir; tersi (S−) düşer.',
  'ASİM = ort(üst fitil) − ort(alt fitil), son 10 geçerli bar; ASİM ≥ 0,20 ve alt fitilsiz payı ≥ 0,50 (Ç187 kaydı, FITIL_OBEK k = 10); t\'de bilinir',
  'FITIL_OBEK sabit: k = 10, ASİM 0,20, fitilsiz payı 0,50 (kayıt). Ölçü eşiği: ' + CK, 'S+ yukarı, S− aşağı',
  '60 gün, ORTAK_CETVEL: 2024-26 hücreleri n 1.557-2.367 TUTMADI (fark ±%0,3, sıra 0,49-0,51); 2023 n 592-928 güç %52 → ÖLÇÜLEMEDİ', 'B + C (60 gün kapandı; 15 bar hiç koşulmadı, IK_ILERI UFUK15)'),
 ('KK02', 'Ç193 / Y9', 'Sert düşüş sonrası dipte (120 gün konumu düşük) S6 taban kırılımı, 15 barda eşlerinden ve konum eşlerinden daha sık hedefe (+%5 / +%10) gider.',
  'S6 AL + F15 ≤ 0,25 (120 gün konumu) + bölge öncesi 60 gün düşüş ≥ %20 (F17 ≤ −0,20); kaynak Ç193 / YAPI_HEDEF Y9',
  'YAPI_HEDEF Y9 eşikleri sabit (F15 ≤ 0,25, F17 ≤ −0,20; ön kayıt d32c2b1)', 'yukarı',
  '15 bar h5: Y9 n 146 / 231 / 20 / 55 güç ≤ %57; bakılmış ABD KAT5 1,15 [1,05; 1,29] ve 1,21 [1,06; 1,36]; konum eşli 1,15 / 1,20; AVR n küçük', 'B; Ç204 sonrası h5 üstünlüğü kalktı: kart yalnız stop\'suz R15 / r60 ölçüsüyle (Cemal\'in çöl tanımı olduğu için tutuldu)'),
 ('KK03', 'Ç189 / K1-K29', 'Fitil öbeği + savunma hattı + dönüm + yol almamış + dipte (S+ v2 \'tam girilir\') 15 barda eşlerinden iyi.',
  'S+ (ASİM ≥ 0,20, alt fitilsiz payı ≥ 0,50) + savunma hattı (10 bar dibi, önceki 30 barın dibini kırmamış) + yol almamış (t hariç) + dipte; kaynak FITIL_V2 N30',
  'FITIL_V2 N30 eşikleri sabit (ön kayıt cc02f7fa)', 'yukarı', '60 gün: n 34-187, güç %10-29, eşli fark −3,8..+1,1; −%50 katı > 1', 'B + C'),
 ('KK04', 'Ç196 / K19', 'Düşüş sonrası dip grubu (G2), trend içi raf (G1) ve rastgele (G3) gruplarından 15 barda daha çok hedefe ulaşır.',
  'G2 = Ş1 (F15 ≤ 0,25 ve F17 ≤ −0,20); G1 = F14 ≥ 0 ve F15 ≥ 0,50; G3 = G2 ile aynı n rastgele', 'YAPI_HEDEF YH_ESIK6 sabit (ön kayıt 3833f78)', 'G2 > G1; G2 > G3',
  '15 bar h5: G2 − G1 ABD +18 / +27 / +13, AVR +22 / +34 / +18 puan (alt uçlar > 0); G2 n 20-346 güç < %80; G1 ters' + C204_NOT, 'B; Ç204 sonrası h5 farkı oynaklık: kart R15 / r60 ile'),
 ('KK05', 'Ç173b', 'Tepeden ≥ %80 düşmüş, son 10 günde yeni dip yapmamış, dipten ≤ 1,5 kat uzaktaki hisse (D1-D3 kurulumu) eşlerinden iyi.',
  '250 gün tepeden ≤ −%80 + son 10 günde yeni dip yok + dipten ≤ 1,5 kat; 60 gün ayrı olay', 'BOFA_DIP kurulum D1-D3 sabit; FI_OLCUT dört şart + 250 gün olasılık',
  'yukarı (piyango riski: P+%100 ve P−%50 ikisi de ~2 kat)', 'FI_OLCUT: ABD 2023 n 81 +%24,8 [+8,9; +43,0] sıra 0,55 TUTTU; 2024-26 n 146 +%20,6 sıra 0,48 portföy tutmadı; AVR n 3 / 8', 'B (AVR n yetersiz) + yön çelişkisi'),
 ('KK06', 'Ç184', "Cemal'in öbek sıkışması (dip sınıfı) sonrası 20 günde büyük gün (≥ 3 × ATR250) eşlerinin 1,14-1,17 katı sıklıkla gelir.",
  '15 bar, en büyük 1 mum hariç medyan mum ≤ 0,75 × ATR250, 1 uç gün hariç kapanış bandı ≤ %8 (BIST) / %6, eğim −%2..; SIKISMA_OBEK mühür de384bbd', 'SIKISMA_OBEK mühür de384bbd sabit: p 15, k_m 0,75, bant 8 / 6, bb 0,20',
  'büyük gün olasılığı yukarı; getiri / yön yok', 'ABD n 579 / 649 (< 1.000) KAT 1,14-1,17 EMARE; AVR n 292 / 389 ölçülemedi', 'B'),
 ('KK07', 'Ç178 / K24 / A1', 'İki evre çöl (düşüş sonrası SMA20 altı → SMA20 üstü 5 gün dizilme, ≤ 2 delen, BB sıkışması; üretimdeki tek çöl sinyali) eşlerinden ayrışır.',
  'FI_K24 fi_k24_tara değişmeden; ORTAK_CETVEL v1.0', 'ORTAK_CETVEL v1.0 (4763c458) + FI_K24 sabit; SAPMA-1: t\'ye kadar 200 bar',
  'yukarı', 'ABD 2024-26 n 2.869 −%1,1 [−2,7; +0,9] TUTMADI (güç yeterli); ABD 2023 n 941 +%1,3 güç %52; AVR n 100 / 286 güç %29; iki yönde büyük hareket (piyango)', 'B (2023 / AVR güç)'),
 ('KK08', 'Ç179', 'Düzgün dip + çöl birlikteliği (C), yalnız dipten (A) ya da yalnız çölden (B) ayrılır.',
  'dip16 / dip17 / K24 parametreleri sabit (DIP_COL_AYRIM); A yalnız dip, B yalnız çöl, C 60 günde ikisi', 'ORTAK_CETVEL v1.0; ön kayıtlı: ayrım kuralı',
  'C > A ve C > B', 'ABD C n250 381 / 723 (< 1.000); AVR C n250 11 / 33; ABD\'de C ≈ A, +%100 katı 1,41 / 1,42 ve 1,40 / 1,33, aralık 0\'ı kapsıyor', 'B'),
 ('KK09', 'Ç182 P1', 'Son mum büyük (≥ 1,22 × ATR250) + 250 gün tepesine yakın + 40 günde küçük mum dizisi yok olan hissede 20 günde büyük mum olasılığı eşlerinden yüksek.',
  'P1: son mum ≥ 1,22 × ATR250, 250 gün tepesine yakın, 40 günde küçük mum dizisi yok; eşler σ250 ondalığında', 'P1 eşikleri sabit (ters_kurallar.json sha); BH q',
  'büyük mum olasılığı yukarı (yön yok)', 'ABD n 3.145 / 16.258, AVR 838 / 4.679; dört hücre alt uç > 1; BH q 0,001 EMARE; IK_ILERI: anlık oynaklık (ATR10 / ATR250) eşlemeli kontrolle yeniden', 'B/D (oynaklık karışımı şüphesi; IK_ILERI maddesi)'),
 ('KK10', 'Ç183 / S4', 'Cemal tanımlı sıkışma (15 gün küçük mum + dar BB + yatay) büyük hareketin habercisidir.',
  '15 gün küçük mum (250 gün %20 yüzdeliği) + dar Bollinger (BB 20, 2σ genişliği 250 gün %20 yüzdeliği) + yatay (|net| ≤ %3...)', 'SC_ESIK mühür 2533e1f0 sabit',
  'büyük hareket yukarı', 'ABD n 843 / 787, AVR 513 / 479 (< 1.000); B1 KAT ~1, BH2 < 1 nokta; ÖLÇÜLEMEDİ', 'B'),
 ('KK11', 'Ç194 / K32-K42', "S6 taban kırılımına Cemal'in 8 mekanik kuralı (Ş1-Ş8) süzgeç olarak eklenince 15 barda eşlerinden iyi.",
  'Ş1 dipte (F15 ≤ 0,25, F17 ≤ −0,20), Ş2 hat net (F1 ≥ 3), Ş3 dip savunusu … Ş8; kaynak YAPI_HEDEF Y10 / Y10b / Y10c', 'YAPI_HEDEF Y10 / Y10b / Y10c eşikleri sabit (ön kayıt b4b701c)', 'yukarı',
  'Huni: 8 kural S6 bölgelerinin ~%0,6\'sını geçiriyor; Y10 n 6-25 (güç %0); Y10c n 118-467; KAT5 ~1; Ç204: Y10 / Y10b ÖLÇÜLEMEDİ, Y10c SORGULA (1 / 4 hücre tutar)', 'B (kasada n çok küçük kalır; yalnız Y10c; Ç204 R15 sonrası)'),
 ('KK12', 'Ç201 / K47', 'MACD pozitif uyumsuzluğu (fiyat aynı / daha derin dip, MACD daha yukarıda dip) olan S6 kırılımları 15 barda eşlerinden iyi.',
  '[t−60, t−1] iki salınım dibi (5 bar yerel min; L2 ≤ t−6, L1 ≥ 8 bar önce), F65 Low(L2) ≤ Low(L1) × 1,0…; MACD (12, 26, 9)', 'YH_ESIK8 Ş10 eşikleri sabit (ön kayıt c642b1c)', 'yukarı',
  'n 77-378 karar hücreleri, KAT 0,98-1,20, alt uçlar < 1; AVR 2016-22 1,16 [1,02; 1,33]; BH 0 / 6', 'B + C'),
 ('KK13', 'Ç191 / K19-K23', "Cemal'in süzgeçleriyle (net hat, gerçek kırılım, stop ≤ %10, büyük desen, hafıza) seçilen S6 kırılımı (Y6 / Y8) 15 barda eşlerinden iyi.",
  'Y6 = S6 AL + hat ≥ 3 dokunuş eğimsiz + gerçek kırılım (kapanış > tavan × 1,01, gövde ≥ bölge medyanı) + stop ≤ %10 …; Y8 + hafıza', 'YAPI_HEDEF YH_ESIK Y6 / Y8 sabit (ön kayıt 8b246d1)', 'yukarı',
  'n 80-310, güç ≤ %57; YÖN ALEYHTE: KAT5 0,59-0,90, üç hücrede üst uç < 1 (Ç203: stop süzgeci hedefe gidenleri eliyor)', 'B + C + D (VD2)'),
 ('KK14', 'K2 / K9 (E)', 'Düz tavan (ilk dip yapısının tavanı) 15 barda aşağı kırılırsa (SAT mumu = tavandan kopan ilk büyük kırmızı mum) ilk düşüş hedefi gelir; S6 ayna sürümü.',
  'S6 taban kırılımının aynası: düz tavan çizgisi (K29: ilk yapının tavanı) + aşağı kırılım mumu; hedef: önceki dip', 'kayıtta eşik yok, ana model sabitleyecek (ön kayıt gerekir)', 'aşağı (kısa kol / kaçınma)',
  'hiç ölçülmedi (SM_TEPE fitil aynasıydı, düz tavan değil; K2 SINANMADI)', 'E'),
 ('KK15', 'K8 / C8 (E)', 'Aynı hissede önceki benzer yapılar hedefe gittiyse (kağıt hafızası) yeni yapı da gider; patladıysa girilmez.',
  'hisse bazlı formasyon karnesi: önceki S6 / yapı olaylarının +%5 hedefine ulaşma payı (t\'ye kadar)', 'kayıtta eşik yok, ana model sabitleyecek', 'yukarı (önceki başarı) / aşağı (önceki patlama)',
  'hiç ölçülmedi (Y4 / Y8 farklı tanım: AVR 2024-26 0,87 aleyhte; Cemal\'in en ağır şartı)', 'E'),
 ('KK16', 'Ç124', 'INTEM tipi kısa ufuk kutu çıkışı: birebir eşleşen bölgelerden sonra +%8 hedefi −%8 stop\'tan önce görme payı, oynaklık eşli rastgeleden yüksek (sıkışma ailesindeki tek EMARE).',
  'FI_K44 parmak izi (8 ölçü, band ±0,125) + K45 kısa ufuk kutu çıkışı; ileri test Ç180 değişmeden', 'Ç124 eşikleri sabit: ABD + AVR 2016-26 n ≥ 30, +%8 önce payı rastgeleden ≥ +10 puan ve aralık artı', 'yukarı',
  'ÖLÇÜLEMEDİ: ABD 2023 n 26 −%3,2; 2024-26 n 42 −%7,5 (güç %10); AVR görülmemiş (Ç180)', 'B + C (hedef-önce cetveli)'),
 ('KK17', 'Ç202 DS06', 'Dip süpürme + geri alma (Turtle Soup / spring / likidite süpürme) 15 barda eşlerinden iyi.',
  'ds_esik.json DS06 tanımı (sabit; kaynak ön kayıt 5cc3cad)', 'ds_esik.json sabit; eşik değişmez', 'yukarı',
  'ABD sınama +6,9 puan; tutan alt kümeler n 6-317, güç 0,04-0,53; BH geçen yok; AVR sınama plasebo sapması (+2,2 puan, yanlış pozitif %15-20) şişkin', 'B + C + D'),
 ('KK18', 'Ç202 DS13 / DS28 / DS23', 'TD Sequential setup 9 / countdown 13 (DS13), düşüş derinliği (DS28), yukarıda mıknatıs: dolmamış boşluk / eşit tepeler (DS23) 15 barda eşlerinden iyi.',
  'ds_esik.json DS13 / DS28 / DS23 tanımları', 'ds_esik.json sabit', 'ilgili yönler ds_esik.json\'da',
  'AVR sınama FARK DS28 +12,1, DS13 +11,4, DS23 +5,7 (plasebo sapmasıyla şişkin); en küçük p_DS 0,26-0,57; q 1,000; ÖLÇÜLEMEDİ', 'B + C + D'),
 ('KK19', 'Ç197', 'F1-F29 ile öğrenilen puanın üst %20 dilimi 15 barda eşlerinden iyi ve stop payı eşten büyük değil (basit ölçüyü geçmiyorsa seçilmez).',
  'M1 lojistik + M2 HistGradientBoosting sabit ayar; F1-F29 mühürlü (YAPI_HEDEF 7. tur)', 'YAPI_HEDEF 7. tur model ayarları sabit (ön kayıt 6275192)', 'yukarı',
  'üst %20: A ABD 2024-26 %50,7 / %44,2 KAT 1,15 [1,06; 1,24] (plasebo %95 %46,9), AVR 2023 1,46 [1,18], AVR 2024-26 1,20; ama stop payı eşten büyük (oynaklık)', 'C (h5) + B'),
 ('KK20', 'Ç128 / Ç125', 'Geniş parmak izi makinesi (166 ölçü; Ç125 36 ölçülü dönüş noktası makinesi) üst %5 sinyali oynaklık eşli rastgeleden +%8 hedefi daha sık görür (AVR).',
  'sabit model katsayıları (K46 / K48 kuralı), ABD + AVR 2023 ve 2024-26 üst %5', 'üst %5 fark ≥ +10 puan, aralık artı, işlem > 0 (kayıt)', 'yukarı',
  'Ç128: ABD 2023 +6,9 (aralık +5,2) eşiğin altı; 2024-26 +12,4; AVR +10,8 / +11,3 (geçti); BIST +23,5 / +9,3; AUC 0,59-0,71. Ç125: ABD +3,6 / +12,2, AVR +4,6 / +12,8 (2023 eşik altı)', 'C (+%8 önce cetveli) — oynaklık karışımı şüphesi'),
 ('KK21', 'Ç112', 'ABD\'de blok hacimli sert düşüş (taban) günü sonrası hisse eşlerinden iyi (BIST\'te ters).',
  'A14 blok hacimli taban günü (hacim ≥ blok eşiği, taban günü)', 'FI_OLCUT dört şart (Ç112 kaydı)', 'yukarı (ABD)',
  'ABD 2024-26 +%14,9 dört şart tutar; 2023 +%4,4 aralık 0\'ı içerir; AVR n 8 / 24; BIST −%23 / −%30 (n 9 / 31); Ç60 BIST eski ÇÜRÜDÜ', 'B + yön çelişkisi'),
 ('KK22', 'Ç115', 'ABD güçlü günü (eşit ağırlıklı ≥ +%1,5) sonrası Avrupa ertesi gün açılış boşluğuna alınabilir fazla girer.',
  'ABD eşit ağırlık ≥ +%1,5 gün; Avrupa ertesi gün fazla = taban üstü; gün içi (açılıştan) fazla', 'alınabilir gecikme = açılıştan sonraki fazla ≥ +%0,2 ve aralık artı; günlük 2023 + 2024-26 ve saatlik en az 2 endeks',
  'yukarı', 'boşluk +%0,23 / +%0,19 / +%0,23 üç dönemde aralık artı; gün içi +%0,10 / +%0,24 / +%0,03 (yalnız 2023 aralık artı); 5 gün sıfır', 'B (saatlik veri son 730 gün); sektör / makro (Cemal kararı)'),
 ('KK23', 'Ç155', 'Oynak hisse havuzunda düşük beta olmayan (yüksek beta) hisse ikiye katlanmayı artırır, yarıya inmeyi artırmaz (BETA_BAB ALT, koşullu fırsat).',
  'BETA_BAB (K60 tanımı) havuz içi ALT %20; havuz = ayda 60 günlük oynaklığı en yüksek %20', 'K60B kuralı: kazanma katı > 1 ve batma katı ≤ 1 üç dönemde (ön kayıt K60B_ON_KAYIT sha256 b74f3e2d2656)', 'yukarı (+%100 olasılığı)',
  '+%100 katı 1,34 / 1,45 / 1,36; −%50 katı 0,91 / 0,73 / 0,98; aylık portföy havuzu +%5 / +%16 / +%16 geçti; yalnız ABD, yalnız yaşayanlar, 2024-25 yükseliş etkisi olabilir', 'B + hayatta kalma (K7)'),
 ('KK24', 'Ç154 DOSYA_Y', "Cemal'in 'sıkı dosya' ölçüsü (DOSYA_Y ÜST) yarıya inme olasılığını azaltır, ikiye katlanmayı azaltmaz (güvenli uç).",
  'DOSYA_Y (K59 YEOTK / DGXX mantığı, SEC finansal özütleri, t\'de bilinen) ÜST %10', 'K60 ön kayıt: üç dönemde −%50 katı < 1 ve +%100 katı ≥ 1 (kayıt)', 'koruma (−%50 azalır)',
  '−%50 katı 0,62 / 0,54 / 0,61; +%100 katı 0,95 / 1,08 / 0,98; medyan evrenin üstünde; havuz içinde 0,65 / 0,81 / 0,73 (Ç155); yalnız ABD, yalnız yaşayanlar', 'B (KASA ikinci kullanım; hayatta kalma)'),
 ('KK25', 'Ç154 COMP4', 'COMP4 bileşiği (K59 önceden yazılı sıra ortalaması) ÜST %10 yarıya inmeyi azaltır; portföyde piyasayı geçmez.',
  'COMP4 = K59 §3 sıra ortalaması bileşiği (4 aile); ÜST %10', 'K60 ön kayıt eşikleri; U1 / U2 TUTMAZ (K59)', 'koruma',
  '−%50 katı 0,43 / 0,25 / 0,47; +%100 katı 0,70 / 1,02 / 0,74; K59 U2 yıllık fazla +%5,5 NW t 2,30 TUTMAZ; K59-B (a) U2 +%7,0 t 2,39 TUTAR (yineleme)', 'B'),
]

C204_NOT = (" | Ç204 (CETVEL2 R15 yeniden koşu, 21 Kas): eski h5 farkları (+9..+34 puan) R15'te −0,2..+0,7 puana indi, aralıklar 0'ı kesiyor: "
            "dipteki 'daha sık +%5' üstünlüğü yön değil oynaklıkmış")
YENI_KART = {
 'K50': ('K50 / H2 (Cemal, Ekim eşleri)', "120 günün tam dibine son 5 günde düşerek gelen hisse (dip savunulmadan) 15 barda eşlerinden kötü kaybeder; 'dip savunulmadan giriş yok'.",
         'F15 ≤ 0,05 (120 gün konumu) ve r5 ≤ −%3 (kural defteri K50); t\'de bilinir', 'tanım eşikleri kayıtlı (F15 ≤ 0,05, r5 ≤ −%3); karar eşiği kayıtta yok, ana model sabitleyecek (9. tur ön kayıt, BH 3)',
         'aşağı (kaçınma)', 'hiç ölçülmedi; Ekim eşleri (sonradan bakma, n 77): h5 %64 / st5 %32 vs %71 / %18 (K50 kaydı)', 'E'),
 'K12': ('K12 (Cemal, kör set 2 No 1)', 'Geçmişinde dev tek mum (fitil > +%100) olan hissenin kağıdı şüphelidir (kripto gibi): yapıları 15 barda eşlerinden kötü sonuç verir.',
         'geçmişte tek mum fitili > +%100 (kural metni); fiyat-hacim, t\'de bilinir; ters bölünme / OTC sıçraması ayıklanmalı (Ç175: k60 verisinde 4.678 hissenin 1.235\'inde > 3x sıçrama ya da H-L > 2 x kapanış)',
         'kayıtta eşik yok, ana model sabitleyecek (yalnız "> +%100" kural metninde)', 'aşağı (kaçınma)', 'hiç ölçülmedi (SINANMADI; devir notu J4 / C13 ile akraba; K6 birim denetimi şart)', 'E'),
 'C186': ('Ç186', "Çöküş sonrası en oynak / en çok düşmüş hisse 250 günde +%100'ü eşlerinden daha sık görür, −%50'yi daha sık görmez (Cemal'in tezi).",
          'çöküş = evren medyan 120 gün getirisi ≤ −0,30; OYNAK = σ250 üst beşlik; giriş = çöküşten +5 gün (COKUS_OYNAK)', 'COKUS_OYNAK eşikleri sabit (IK_ILERI: medyan r120 ≤ −0,30; σ250 üst beşlik; giriş +5 gün); olasılık katı: ORTAK_CETVEL',
          'yukarı (+%100 katı > 1, −%50 katı ≤ 1)', 'ÖLÇÜLEMEDİ: tamamlanmış çöküş 1 < 2 (2023-05-22; 2026-10-13); 2023 OYNAK n 69, P+%100 %73,9, P−%50 %2,9, kat 0,95 (alt uç −15). Not: 2026-10-13 çöküşü fon krizi (31.08.2026) sonrasıdır: CLAUDE.md gereği testlere girmez, yalnız bilgi; kasa kullanımı Cemal kararı', 'B (tek olay)'),
 'K49': ('K49 / H1 (Cemal, Ekim eşleri)', "Giriş ile 15. bar arasında bilanço duyurusu olan olaylarda hem en iyi hem en kötü sonuçlar toplanır (bilanço penceresi = kuyruk büyüteci, yön değil).",
         'BIL15: giriş-15. bar arasında bilanço duyurusu var mı (duyuru ≤ t); ABD Nasdaq takvimi (Ç100) elde, BIST KAP', 'kayıtta eşik yok, ana model sabitleyecek (9. tur ön kayıt, BH 3)',
         'yön yok (kuyruk genişliği: hem +%5 hem stop payı artar)', 'hiç ölçülmedi (Ekim eşleri sonradan bakma: kazanan 20 / 20, kaybeden %70); olay verisi (bilanço takvimi) fiyat bloğunda yok, ayrı kasa bloğu gerekir', 'E'),
}
KART_SIRA = ['KK01', 'KK02', 'KK03', 'K50', 'K12', 'KK14', 'KK15', 'KK04', 'KK05', 'KK06', 'KK07', 'KK08', 'KK09', 'KK10', 'KK11', 'KK13', 'C186', 'KK16', 'KK20', 'KK21', 'KK22', 'KK23', 'KK24', 'KK25', 'K49']
KART_DUSEN = [('KK12', 'Ç201 Ş10 MACD pozitif uyumsuzluk (Cemal K47)', "Ç204: Ç201 3 hipotezin 2'si SORGULA (0 / 4 hücre tutar, güç yeterli → İZ DEĞİL +2 puan ve üstü için); kasaya alınmadı"),
              ('KK17', 'Ç202 DS06 dip süpürme (Turtle Soup)', "Ç204: ABD sınama FARK +6,9 → +0,21 (R15); etki yok"),
              ('KK18', 'Ç202 DS13 / DS28 / DS23', "Ç204 R15: DS13 ÖLÇÜLEMEDİ, DS28 ve DS23 SORGULA (0 / 4 hücre tutar); AVR plasebo sapması Ç204'te giderildi"),
              ('KK19', 'Ç197 F1-F29 puan üst %20', "Ç204: dört hipotezin dördü SORGULA; eski KAT 1,15 R15'te kalmadı; karmaşık ölçü basit ölçüyü geçmiyor (CLAUDE.md: basit seçilir)")]

KASAK = {'K1': 'HAYIR: ölçüt (cetvel kuralı)', 'K15': 'HAYIR: ölçüt (ufuk 15; cetvele girer)', 'K18': 'HAYIR: ölçüt (test standardı)',
         'K16': 'HAYIR: tez; büyük çöl aranmaz (kapalı)', 'K17': 'HAYIR: tez / ders; K30 ve KK01-KK04 içinde',
         'K2': 'EVET → KK06', 'K9': 'EVET → KK06', 'K29': 'EVET → KK06 içinde (tavan tanımı)', 'K8': 'EVET → KK07', 'K25': 'EVET → KK07', 'K12': 'EVET → KK05', 'K49': 'EVET → KK25', 'K50': 'EVET → KK04',
         'K30': 'EVET → KK01', 'K32': 'EVET → KK01 ile birleşir', 'K47': "HAYIR (Ç204): Ş10 R15'te etki yok; kart düştü", 'K19': 'EVET → KK16', 'K20': 'EVET → KK16', 'K21': 'EVET → KK16',
         'K23': 'EVET → KK16', 'K26': 'EVET → KK16', 'K22': 'EVET sonra (Ş9; kart yok, Ç195 n 1-20)', 'K31': 'HAYIR: kapalı konu (giriş onayı); Cemal kararı',
         'K33': 'HAYIR: vekil göz / kör set', 'K34': 'HAYIR: hakem dersi, 100 sayfalık set bekler', 'K35': 'HAYIR: vekil dersi (bırakıldı)',
         'K42': 'HAYIR: dosya bilgisi kör sette yok', 'K51': 'HAYIR: katalizör takvimi verisi yok', 'K48': 'EVET sonra: Ş11 eşiği yok', 'K36': 'HAYIR: tek tur dersi', 'K37': 'HAYIR: tek tur dersi',
         'K38': 'HAYIR: tek tur dersi', 'K39': 'HAYIR: tek tur dersi', 'K41': 'HAYIR: tek tur dersi (mahkeme)', 'K43': 'HAYIR: tek tur dersi', 'K44': 'HAYIR: tek tur dersi',
         'K45': 'HAYIR: tek tur dersi', 'K46': 'HAYIR: tek tur dersi', 'K40': 'EVET sonra (Ş9)'}

KAPALI = [
 ('Giriş noktası / zamanlaması / teyit / retest / kırılım hacmi', 'Ç01 (KAPALI: hiçbiri geçmedi)', 'sistem kuralı, olay izi değil; Ç01 denetimi yön aynı'),
 ('Aday filtreleri (E_ONC, üç şart kapısı, taban kırılması düşürme)', 'Ç02', 'her filtre para kaybettirdi'),
 ('Çıkış varyantları / stop / erken kesme', 'Ç03, Ç45, Ç46, Ç91', 'trail SMA20 en iyi; T10 getiri dayanağı ters döndü (Ç45); stop darlığı CD20 ayrı ölçüt (Ç203) olarak yeniden açılmaz, cetvel revizyonu işidir'),
 ('Rejim / dış veri: VIX / DXY / USDTRY / CDS / temel', 'Ç05, Ç110 (DXY yok)', 'tutarsız'),
 ('4h / haftalık / KNN / ML kâr eklemesi', 'Ç06, Ç95 (Cemal isteğiyle KNN), Ç58', 'rejime bağlı, ML kâr eklemedi'),
 ('90+ şekil ölçüsü', 'Ç04, Ç09, Ç43, Ç128 (166 ölçü)', 'şekil ölçüsü çölü ayırmıyor (Ç43 AUC 0,37-0,60); Ç09 oynaklık'),
 ('Sektör ısısı', 'Ç28, Ç108-Ç111, Ç114, Ç117, Ç181c (Cemal istedi)', 'kapalı konu; Ç181c EMARE ve IK_ILERI maddeleri Cemal kararıyla yürür (kasa kartı değil)'),
 ('Büyük çöl (20-60 mum, çok katlı hedef)', 'K16 (17 Kas)', 'fon / manipülasyon sınıfı; aranmaz; yalnız fon izi (K12) ile birlikte görülürse not'),
 ('Kripto', 'Ç147', 'İZ DEĞİL; Cemal 9 Kas: kripto kapandı'),
 ('60 gün sabit ufuk yapı ölçümü', 'K15 / UFUK 15 MUM', 'yapı kuralları 15 barla ölçülür; 60 gün yalnız bilgi (kapalı değil, ölçüt değişti)'),
]


def main():
    satirlar, kayit = satirlari_kur()
    ykper, ykkod = yk_tablosu()
    ds_rows, ds_olc = ds_tablosu()
    k60 = k60_tablosu()
    ust, kk = kural_tablolari()
    hmap = hata_haritasi()
    L = []
    w = L.append
    # ---------------- sayimlar
    ana_kodlar = {s['ana'] for s in satirlar}
    eksik = [k['kod'] for k in IK.IK_KAYIT if k['kod'] not in ana_kodlar]
    fazla = [a for a in ana_kodlar if a not in {k['kod'] for k in IK.IK_KAYIT}]
    karar_say = collections.Counter(s['kar'] for s in satirlar)
    aile_say = collections.Counter(s['aile'] for s in satirlar)
    guv_say = collections.Counter()
    for s in satirlar:
        for h in re.findall(r'\b[A-E]\b', re.sub(r'\(.*?\)', '', s['guv']).replace('A?', 'A')):
            guv_say[h] += 1
    guv_tek = collections.Counter()
    for s in satirlar:
        if s['guv'] == '-':
            guv_tek['-'] += 1
        else:
            guv_tek[s['guv'].split(' + ')[0].replace('A?', 'A?')] += 1
    kasa_evet = [s for s in satirlar if s['kasa'].startswith('EVET')]

    w('# HİPOTEZ ENVANTERİ (21 Kasım 2026)\n')
    w('Derleyen: alt ajan (derleme; ölçüm yok, web yok). Ana tablo `arastirma_cikti/kasa/hipotez_envanteri.py` ile IK_KAYIT\'tan mekanik çıkarıldı; aile / karar / güvenilirlik sınıfları kayıt metni okunarak doldurulan sözlüklerdedir (betiğin başında). Uydurma yok: bulunamayan yerde "kayıtta yok" yazıldı.\n')
    w('Dayanak: IK_KAYIT (%d Ç), IK_ILERI (%d satır), IK_HATA (%d satır), KURAL_DEFTERI_TASLAK (A-K), HAKEM_DERSLER + GOZ_ETIKET (C1-C13, CD / VD), SINYAL_ENVANTERI + K60 olasılık tablosu, DS_ELESTIRI + DS_RAPOR, COL_OZET (kapalı konular).\n' % (len(IK.IK_KAYIT), len(IK.IK_ILERI), len(IK.IK_HATA)))

    # ---------------- 1. OZET
    w('## 1. BİR SAYFALIK ÖZET (Cemal için)\n')
    n_dis = sum(1 for s in satirlar if s['kar'] != 'ALT')
    w('- **Kaç çalışma:** kayıt defterinde %d Ç çalışması (Ç01-Ç%d). Üç kaydı parçalara böldüm (Ç173 iki, Ç181 üç, Ç182 iki parça) → %d satır. Bunlardan %d satır araç / denetim / altyapı (hipotez değil), **%d satır gerçek hipotez**. Yanına: K60 sinyal kütüphanesinden %d sinyal-uç çifti, düşüş sonrası (DS) web hipotezlerinden 87, Cemal\'in sözlerinden 140 kural + K1-K51 + C1-C13 + dersler.' % (
        len(IK.IK_KAYIT), len(IK.IK_KAYIT), len(satirlar), karar_say['ALT'], n_dis, len(k60)))
    w('- **Sonuç özeti (Ç satırları, gerçek hipotezler):** ' + ' · '.join('%s %d' % (KAR[k], karar_say[k]) for k in ('IZD', 'OLC', 'EMA', 'ADY', 'KAP', 'KYK') if karar_say[k]) + '. Hiçbiri İZ değil.')
    izd = [s for s in satirlar if s['kar'] == 'IZD']
    izd_a = sum(1 for s in izd if s['guv'].startswith('A'))
    izd_olc = sum(1 for s in izd if s['karar'].startswith('ÖLÇÜLEMEDİ'))
    izd_b = sum(1 for s in izd if s['guv'].startswith('B')) - izd_olc
    w('- **Asıl bulgu:** kayıtta "İZ DEĞİL" yazılı %d satırdan yalnız **%d**\'i güç yeterli (A: Ç175 "hak eden gövde" + kayıtta güç yeterli yazılı); %d\'i Ç175\'in kendi yeniden etiketlemesiyle **ÖLÇÜLEMEDİ**; %d\'inde hücre n < 1.000 ya da n kayıtta yok (B / B*; K58); kalan %d: h5 (C) ya da doğrulanmamış A?. Yani çoğu "iz yok" aslında "bakamadık".' % (len(izd), izd_a, izd_olc, izd_b, len(izd) - izd_a - izd_olc - izd_b))
    w("- **Cetvel sorunu ve Ç204:** Ç190-Ç203 arasında 15 bar h5 cetveli oynaklığı ödüllendirdi (Ç203). Ç204 (21 Kas) Ç194-Ç202'yi düzeltilmiş CETVEL2 R15 (stop'suz) ile yeniden koştu: KATKI+ 0, KATKI− 0, 66 etiket değişti; eski h5 üstünlükleri (+9..+34 puan) R15'te −0,2..+0,7 puana indi (oynaklıkmış); 52 hipotez 'İZ DEĞİL (+2 puan ve üstü için)', güçsüz hücreler ÖLÇÜLEMEDİ. Ç190-Ç193 yeniden koşulmadı, h5 etiketiyle duruyor. Ç124-Ç131 '+%8 önce' cetveli de h5 akrabası.")
    w('- **Kasaya aday:** ana tabloda %d Ç satırı kasa adayı (EVET); bunlardan öncelikle 25 kart taslağı bölüm 4\'tedir (Cemal\'in kendi kuralları önde).' % len(kasa_evet))
    w('')
    w('**Aileye göre sayım (Ç satırları):**\n')
    w('| aile | satır |\n|---|---|')
    for a, c in aile_say.most_common():
        w('| %s | %d |' % (AILE[a], c))
    w('')
    w('**Karara göre sayım (kayıttaki etiket, normalize):**\n')
    w('| karar | satır |\n|---|---|')
    for k in ('IZ', 'EMA', 'ADY', 'IZD', 'OLC', 'SIN', 'KAP', 'KYK', 'ALT'):
        w('| %s | %d |' % (KAR[k], karar_say.get(k, 0)))
    w('| (not) İZ DEĞİL satırlarının Ç175 ile ÖLÇÜLEMEDİ\'ye çevrilenleri | %d |' % sum(1 for s in satirlar if s['karar'].startswith('ÖLÇÜLEMEDİ (kayıtta')))
    ds_say = len(ds_rows); ds_olc_say = len(ds_olc)
    w('| (ek) DS web hipotezleri: 87 tekilleştirilmiş; ölçülen %d → hepsi ÖLÇÜLEMEDİ; ölçülmeyen %d → SINANMADI | %d |' % (ds_olc_say, ds_say - ds_olc_say, ds_say))
    w('| (ek) K60 sinyal-uç çiftleri: %d (ölçüldü; İZ ADAYI 0) | %d |' % (len(k60), len(k60)))
    w('')
    w('**Güvenilirlik sayımı (bir satır birden çok harf alabilir):**\n')
    w('| sınıf | anlam | satır |\n|---|---|---|')
    for h, ad in (('A', 'güç yeterli, cetvel sorunsuz (karar sağlam)'), ('B', 'n < 1.000 ya da güç yetersiz → aslında ÖLÇÜLEMEDİ (K58); "B*" kayıtta n yok'),
                  ('C', 'h5 (+%5 stop\'tan önce) cetveli: oynaklık karışımı (Ç203)'), ('D', 'hata defterinde ya da kayıt notunda düzeltme var'), ('E', 'hiç ölçülmedi (SINANMADI)')):
        if h == 'E':
            c = 'Ç içinde yok; DS 62 + SINYAL_ENVANTERI + K-kuralları satırlarında (bölüm 2b-2d, 3)'
        else:
            c = guv_say[h]
        w('| %s | %s | %s |' % (h, ad, c))
    w('')
    # en cok yaklasanlar
    w('**En çok yaklaşanlar, ilk 15 (kayıttaki sayıyla; eşik dört şart ya da önceden yazılı hücre kuralı; son üçü Ç204 CETVEL2 R15 sonrası geçersiz):**\n')
    w('| # | kod | ne | kayıttaki sayı | neden hâlâ iz değil |\n|---|---|---|---|---|')
    YAK = [
     ('Ç173b', '−%80 dip kurulumu (ABD)', 'ABD 2023 n 81 +%24,8 [+8,9; +43,0] sıra 0,55 TUTTU; 2024-26 n 146 +%20,6 sıra 0,48', '2024-26 sıra / portföy tutmadı; AVR n 3 / 8; piyango profili (P+%100 ve P−%50 ~2 kat)'),
     ('Ç181c', 'Yalnız sektör rüzgârı (ABD)', 'ABD 2024-26 n 5.873 +%3,6 [+1,9; +5,4], +%100 katı 1,35 / 1,39', 'portföy şartı tutmadı; −%50 üst ucu 1\'i aşıyor; AVR ölçülemez (kapalı konu)'),
     ('Ç193', 'Dipte S6 kırılımı Y9 (ABD, 15 bar)', 'KAT5 1,15 [1,05; 1,29] ve 1,21 [1,06; 1,36]; konum eşli 1,15 / 1,20', 'bakılmış hücreler; n 146 / 231; h5 cetveli (C); Ç204: dipte (Ş1) fark R15\'te −0,2..+0,7 puan, aralık 0\'ı kesiyor → oynaklıkmış'),
     ('Ç197', 'F1-F29 puan üst %20 (15 bar)', 'ABD 2024-26 %50,7 vs %44,2, KAT 1,15 [1,06; 1,24]; AVR 2023 1,46 [1,18]', 'TUTAR hücre yok; stop payı eşten büyük; Ç204 R15: KATKI+ 0 (4 hipotez SORGULA)'),
     ('Ç196', 'Dip grubu G2 − trend içi raf G1', 'ABD +18 / +27 / +13, AVR +22 / +34 / +18 puan (alt uç > 0)', 'G2 n 20-346 güç < %80; Ç204: h5 farkları R15\'te −0,2..+0,7 puana indi (oynaklık)'),
     ('Ç128', 'Geniş makine üst %5 (+%8 önce)', 'ABD 2024-26 +12,4, AVR +10,8 / +11,3; ABD 2023 +6,9', 'ABD 2023 eşiğin (10) altında; oynaklık eşli rastgele cetvel'),
     ('Ç125', 'Dönüş noktası makinesi üst %5', 'ABD +3,6 / +12,2, AVR +4,6 / +12,8, BIST +27,7 / +12,6', '2023 hücreleri eşik altı'),
     ('Ç127', 'Sert düşüş sonrası makine üst %5', 'ABD +21,8 / +16,6 puan, işlem +%2,9 / +%2,4; AVR 2023 +15,3 (n 59), 2024-26 0,0', 'AVR 2024-26 sıfır; portföy piyasanın altı'),
     ('Ç182a', 'Büyük mum öncesi profil P1', 'ABD n 3.145 / 16.258, AVR 838 / 4.679; dört hücre alt uç > 1; BH q 0,001', 'yön yok; oynaklık (ATR10 / ATR250) eşlemeli kontrol bekliyor'),
     ('Ç118', 'K24 çöl + iyi bilanço (ABD)', 'ABD 2023 +%7,7 (n 52, aralık artı); 2024-26 −%0,4 (n 170)', 'iki hücrede tutmadı; portföy tabanın altında'),
     ('Ç112', 'Blok hacimli taban günü (ABD)', 'ABD 2024-26 +%14,9 dört şart tutar; 2023 +%4,4', '2023 aralık 0\'ı içeriyor; AVR n 8 / 24; BIST ters'),
     ('Ç155', 'BETA_BAB ALT havuz içi (ABD)', '+%100 katı 1,34 / 1,45 / 1,36; −%50 katı 0,91 / 0,73 / 0,98', 'İZ değil (yalnız ABD, yalnız yaşayanlar); yükseliş etkisi olabilir'),
     ('Ç154', 'DOSYA_Y / COMP4 güvenli uç (ABD)', '−%50 katı COMP4 0,43 / 0,25 / 0,47; DOSYA_Y 0,62 / 0,54 / 0,61; +%100 katı ~1', 'kazanma artmıyor (koruma); yalnız yaşayanlar'),
     ('Ç115', 'ABD gece hareketi → Avrupa açılış boşluğu', 'boşluk +%0,23 / +%0,19 / +%0,23 (üç dönem aralık artı)', 'alınabilir gün içi fazla yalnız 2023 (+%0,24)'),
     ('Ç102', 'Çölde içeriden alım (ABD)', '+%7,3 (aralık +0,3..+16,1, dört şart tuttu) 2023; 2024-26 +%7,2 aralık 0\'ı içeriyor', 'örneklem dışı 2016-22 −%4,5 / −%3,5; aday güçlenmedi'),
    ]
    YAK = [y for y in YAK if y[0] not in ('Ç193', 'Ç196', 'Ç197')] + [y for y in YAK if y[0] in ('Ç193', 'Ç196', 'Ç197')]
    for i, (kod, ne, say, neden) in enumerate(YAK, 1):
        w('| %d | %s | %s | %s | %s |' % (i, kod, ne, say, neden))
    w('')

    # ---------------- 2. ANA TABLO
    w('## 2. ANA TABLO (her Ç kaydı bir satır)\n')
    w('Satır sayısı kontrolü: IK_KAYIT uzunluğu = **%d**; tablo satırı = **%d** (Ç173 → 173a / 173b, Ç181 → a / b / c, Ç182 → a / b ile +%d); eksik kayıt: %s; fazla: %s.\n' % (
        len(IK.IK_KAYIT), len(satirlar), len(satirlar) - len(IK.IK_KAYIT), eksik or 'yok', fazla or 'yok'))
    w("Ç204 okuma notu: CETVEL2 R15 yeniden koşusunda 'SORGULA' = karar hücrelerinin 0 / 4 (az sayıda 1 / 4) hücresi beklenen yönde tutar ve güç yeterli; Ç204 kaydı bu sınıfta güç ≥ 0,80 olanları (52 kod: Ç196 9, Ç197 3, Ç198 16, Ç199 8, Ç200 3, Ç201 2, Ç202 11) 'İZ DEĞİL (15 mum ufku, +2 puan ve üstü etki için)' diye yorumlar; 'ÖLÇÜLEMEDİ' = n < 30 ya da güç < 0,80.\n")
    w('Sütunlar: kod | tarih | aile | hipotez | cetvel | pazar ve dönem (kayıt metninden) | n (kayıttaki ilk üç ifade) | karar | kayıttaki ana sayı / not | GÜVENİLİRLİK | veri | t\'de bilinir ve sayısal | KASA ADAYI.\n')
    w('| kod | tarih | aile | hipotez | cetvel | pazar / dönem | n | karar | ana sayı / not | GÜV | veri | t\'de sayısal | KASA |')
    w('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for s in satirlar:
        w('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            s['kod'], s['tarih'], AILE[s['aile']], kisalt(s['hip'], 160), s['cet'], s['pd'], kisalt(s['n'], 40), s['karar'],
            kisalt(s['sayi'], 160), kisalt(s['guv'] + (' (' + s['gek'] + ')' if s['gek'] else ''), 230), s['veri'].split(' (')[0], s['tb'].split(' (')[0].split(' →')[0], s['kasa'].split(':')[0] + (':' + s['kasa'].split(':', 1)[1] if ':' in s['kasa'] else '')))
    w('')
    # 2b K60
    w('### 2b. K60 sinyal kütüphanesi (Ç154 içinde; %d sinyal-uç çifti; ölçüm: 12 ay +%%100 / −%%50 olasılık katı, üç dönem KEŞİF / DOĞRULAMA / KASA)\n' % len(k60))
    w('Hepsi ABD, yalnız yaşayanlar (K7), cetvel R1 / R2 (K60). Karar: İZ ADAYI 0; "K60-OLASILIK İZİ" etiketleri oynaklık etkisi (karar bilgisi değil). Sütun: kat = (+%100 katı / −%50 katı) KEŞİF → DOĞRULAMA → KASA. GÜV: A (cetvel v2 güvenilir) + D (oynaklık karışımı: Ç154).\n')
    w('| sinyal (uç) | +%100 katı KE / DO / KA | −%50 katı KE / DO / KA |\n|---|---|---|')
    for (sg, uc), d in sorted(k60.items()):
        def g(donem, i):
            return d.get(donem, ('', '', ''))[i] or '-'
        ya = ' / '.join(g(x, 0) for x in ('KEŞİF', 'DOĞRULAMA', 'KASA'))
        ba = ' / '.join(g(x, 1) for x in ('KEŞİF', 'DOĞRULAMA', 'KASA'))
        w('| %s (%s) | %s | %s |' % (sg, uc, ya, ba))
    w('')
    # 2c DS
    w('### 2c. Düşüş sonrası (DS) web hipotezleri (Ç202; 87 DS = 123 web hipotezi tekilleştirildi; ölçülen 25 / 25 ÖLÇÜLEMEDİ)\n')
    w('| DS | hipotez | kaynak kodları (WEB A-D) | süzgeç sınıfı | ölçüldü mü / ABD sınama FARK / güç / etiket | karar | GÜV | KASA |\n|---|---|---|---|---|---|---|---|')
    for r in ds_rows:
        o = ds_olc.get(r[0])
        if o:
            ol = 'EVET: ' + kisalt(o['sin'], 40) + ' / boot ' + kisalt(o['boot'], 22) + ' / güç ' + o['guc']
            y = ykkod.get(('Ç202', r[0]))
            kr = 'ÖLÇÜLEMEDİ (h5)' + ((' → Ç204 R15: ' + y[0] + ' (' + y[1] + ')') if y else '')
            gv = 'A / B (CETVEL2 R15, Ç204); h5 etiketi geçersiz'
            ks = 'EVET: sayısal, ds_esik.json sabit' if r[4].startswith('I') else 'HAYIR'
        else:
            ol = 'HAYIR'
            kr = 'SINANMADI'
            gv = 'E'
            ks = ('EVET (öncelik dışı kaldı; ds_esik.json yok, kayıtta eşik yok)' if r[4].startswith('I') else 'HAYIR: ' + kisalt(r[4], 40))
        w('| %s | %s | %s | %s | %s | %s | %s | %s |' % (r[0], kisalt(r[1], 90), r[3], kisalt(r[4], 30), ol, kr, gv, ks))
    w('')
    # 2d SINYAL ENVANTERI K60'a girmeyenler
    envt = open(os.path.join(AC, 'yol_haritasi', 'SINYAL_ENVANTERI.md'), encoding='utf-8').read()
    a = envt.index('## A. Sinyal tablosu'); b = envt.index('## B. Olay tablosu')
    env_rows = []
    for ln in envt[a:b].split('\n'):
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if len(c) == 10 and re.match(r'^[A-Z][A-Z0-9_a-z]+$', c[0]) and c[0] != 'kod':
            env_rows.append((c[0], c[1], c[2], c[3], c[4], c[7], c[8], c[9]))
    k60_kod = {s for (s, u) in k60}
    k60_kod |= {'COMP4', 'DOSYA_Y'}
    yok = [r for r in env_rows if r[0] not in k60_kod and not r[0].startswith('AILE_')]
    w('### 2d. SINYAL_ENVANTERI satırları (120 satır; yukarıdaki %d sinyal K60\'ta ölçüldü) K60 tablosunda adı geçmeyenler (ad eşleşmesiyle; K60 farklı kod kullanmış olabilir) → %d satır, SINANMADI (E)\n' % (len(k60_kod), len(yok)))
    w('(Not: envanterde %d satır ayrıştırıldı; 4 satır "YOK" = ücretsiz veriyle hesaplanamaz. Bu satırlar ölçülmedi; kayıtta hangi nedenle K60\'a girmediği ayrıca yazılı değil: "kayıtta yok".)\n' % len(env_rows))
    w('| kod | aile | tanım (kısa) | yön | bizde var mı | KASA ADAYI |\n|---|---|---|---|---|---|')
    for r in yok:
        var = r[5]
        ks = 'HAYIR: veri YOK' if var.strip().startswith('YOK') else ('EVET: fiyat / SEC özütü elde, tanım sayısal' if var.strip().startswith('EVET') else 'HAYIR (şimdilik): İNDİR gerekir')
        w('| %s | %s | %s | %s | %s | %s |' % (r[0], r[1], kisalt(r[2], 110), r[3], kisalt(var, 40), ks))
    w('')

    # ---------------- 3. CEMAL KURALLARI
    w('## 3. CEMAL\'İN KURALLARI TABLOSU\n')
    w('Kaynak: KURAL_DEFTERI_TASLAK.md (A-J: %d kural, K1-K51: %d kural; taslak, ana model işler), GOZ_ETIKET_IS_TANIMI (C1-C13), HAKEM_DERSLER (CD / VD). Güvenilirlik harfi bu tabloda: A = güç yeterli ve cetvel sorunsuz TUTTU / TUTMADI; B = ölçülemedi / n küçük (K58); C = 15 bar h5 ya da vekil cetveli; E = hiç ölçülmedi. "Kodda" sütunu kural defterinden alındı.\n' % (len(ust), len(kk)))
    w('### 3a. K1-K51 (kural defteri bölüm K: kör set 2 dersleri, YAPI_HEDEF değerlendirmesi, hakem / TUR dersleri, Ekim eşleri)\n')
    w('| kural | düz dil | sayısal tanım (F / Ş kodu) | şimdiye kadarki ölçüm (Ç, cetvel, sonuç) | GÜV | kasa adayı |\n|---|---|---|---|---|---|')
    KSAY = {  # K -> (F/S kodu, kasa notu)
        'K1': 'cetvel kuralı (h5 / r15)', 'K2': 'YOK (S6 ayna sürümü)', 'K3': 'Ş9 (a > 0) yakın', 'K4': 'FITIL_V2 s4 (ters)', 'K5': 'FITIL_V2 s2 kısmen', 'K6': 'FITIL_V2 s2 kısmen',
        'K7': 'S6 nMin sabit', 'K8': 'YOK', 'K9': 'YOK', 'K10': 'YOK', 'K11': 'YOK', 'K12': 'YOK', 'K13': 'YOK', 'K14': 'COL_v1 yorum', 'K15': 'ORTAK_CETVEL ufuk 15', 'K16': 'FON_IZI K12',
        'K17': 'FITIL_V2 s1', 'K18': 'cetvel', 'K19': 'Y6 / F-büyük desen', 'K20': 'Y6 F1 (hat dokunuş)', 'K21': 'Y6 gerçek kırılım', 'K22': 'Ş9 / Y3', 'K23': 'Y6 stop ≤ %10', 'K24': 'YOK',
        'K25': 'Y4 / Y8', 'K26': 'Y6', 'K27': 'YOK', 'K28': 'Y5 nMin', 'K29': 'S6 pencere', 'K30': 'FITIL_OBEK ASİM', 'K31': 'COL_v1 AL tek kapanış', 'K32': 'FITIL_OBEK k 10',
        'K47': 'Ş10 / F65-F68', 'K48': 'Ş11 / F69 a_high', 'K49': 'BIL15', 'K50': 'F15 ≤ 0,05 ve r5 ≤ −%3', 'K51': 'katalizör takvimi (veri gerekir)'}
    for r in kk:
        no, kural, kaynak, sinandi, sonuc, neden, kodda, durum = r
        guv = {'SINANMADI': 'E', 'ÖLÇÜLEMEDİ': 'B', 'TUTMADI (uyum)': 'C', 'TUTMADI (vekil)': 'C + D', 'SINANMAZ (kör)': '-'}.get(sonuc.strip(), 'E' if 'SINANMADI' in sonuc else 'B')
        sd = KSAY.get(no, kodda)
        olc = sinandi if sinandi.strip() != 'Hayır' else 'Hayır'
        kasa = KASAK.get(no, 'EVET sonra: kart sırası dışı; eşik yazılmalı (kayıtta eşik yok)')
        w('| %s | %s | %s | %s: %s | %s | %s |' % (no, kisalt(kural, 160), kisalt(sd, 50), kisalt(olc, 55), kisalt(sonuc, 40), guv, kasa))
    w('')
    w('### 3b. C1-C13 (Cemal\'in göz kuralları; vekil göz bunlarla etiketledi, GOZ_ETIKET)\n')
    w('| kural | düz dil | sayısal tanım | ölçüm | GÜV |\n|---|---|---|---|---|')
    for r in C_KURAL:
        w('| %s | %s | %s | %s | %s |' % r)
    w('')
    w('### 3c. CD / VD dersleri (HAKEM_DERSLER; hepsi SINANMADI ya da tek tur n küçük)\n')
    w('| ders | düz dil | sayısal karşılık | ölçüm | GÜV |\n|---|---|---|---|---|')
    for r in CD_VD:
        w('| %s | %s | %s | %s | %s |' % r)
    w('')
    w('### 3d. A-J grupları (kural defteri; %d kural, ayrıntı ve durumlar orada; burada yalnız sonuç sayımı)\n' % len(ust))
    sc = collections.Counter(u[4].strip() for u in ust)
    w('Sonuç sayımı: ' + ' · '.join('%s %d' % (k, v) for k, v in sc.most_common()) + '.\n')
    w('| no | kural (kısa) | sonuç | kodda | durum |\n|---|---|---|---|---|')
    for u in ust:
        w('| %s | %s | %s | %s | %s |' % (u[0], kisalt(u[1], 120), kisalt(u[4], 22), kisalt(u[6], 40), kisalt(u[7], 45)))
    w('')

    # ---------------- 4. KARTLAR
    w('## 4. KASA KART TASLAKLARI (25; öncelik sırası)\n')
    w('Seçim ölçütü (önceden): (i) Cemal\'in kendi kuralı, (ii) eşiğe en çok yaklaşmış ve B / C sınıfı, (iii) sayısal tanımı ve eşiği kayıtta hazır, (iv) veri elde, (v) aile çeşitliliği. Yeni eşik yazılmadı; eşik kayıtta yoksa "kayıtta eşik yok, ana model sabitleyecek". Hepsinde ortak ölçü notu: ' + OLCU + '. Ortak başarı şartı (kayıttaki FI_OLCUT / ORTAK_CETVEL): ' + CK + '.\n')
    kd = {k[0]: k for k in KARTLAR}
    for kno, (kay, cumle, gor, esik, yon, onc, neden) in YENI_KART.items():
        kd[kno] = (kno, kay, cumle, gor, esik, yon, onc, neden)
    assert len(KART_SIRA) == 25 and len(set(KART_SIRA)) == 25
    for i_, anah in enumerate(KART_SIRA, 1):
        _, kay, cumle, gor, esik, yon, onc, neden = kd[anah]
        w('### KK%02d (%s)' % (i_, kay))
        w('- **CÜMLE:** %s' % cumle)
        w('- **GÖRÜLEN ŞEY:** %s' % gor)
        w('- **EŞİK:** %s' % esik)
        w('- **YÖN:** %s' % yon)
        w('- **ÖNCEKİ SONUÇ:** %s' % onc)
        w('- **NEDEN YENİDEN:** %s' % neden)
        w('')
    w('### Ç204 sonrası kart yapılmayanlar (ilk taslakta vardı; CETVEL2 R15 yeniden koşusunda etki yok)\n')
    for _, ne, why in KART_DUSEN:
        w('- %s: %s' % (ne, why))
    w('')

    # ---------------- 5. KAPALI
    w('## 5. KAPALI KONULAR ve gerekçesi (COL_OZET / CLAUDE.md; kart olmaz)\n')
    w('| konu | kayıt | gerekçe |\n|---|---|---|')
    for r in KAPALI:
        w('| %s | %s | %s |' % r)
    w('')
    w('Not: Ç175 kapalı konuların çoğunun (n < 1.000 hücre) aslında ÖLÇÜLEMEDİ olduğunu, "İZ DEĞİL"i hak eden gövdenin Ç34, Ç41, Ç44, Ç47, Ç49, Ç56, Ç72, Ç85, Ç86, Ç88, Ç91, Ç93, Ç96 (ABD), Ç104, Ç132, Ç134, Ç156 olduğunu yazar. Kapalı konuların yeniden açılması Cemal kararıdır (CLAUDE.md), bu envanter açmaz.\n')

    # ---------------- 6. HATA + KONTROL
    w('## 6. HATA (derlerken bulunan çelişkiler)\n')
    hatalar = HATALAR(satirlar, kayit, hmap)
    for i, h in enumerate(hatalar, 1):
        w('%d. %s' % (i, h))
    w('')
    w('## KONTROL LİSTESİ (python IZ_KARNE.py kontrol; bu iş derleme olduğu için yalnız ilgili satırlar dolduruldu)\n')
    w('| madde | durum | kanıt |\n|---|---|---|')
    KL = [
     ('K1 kontrol grubu', 'UYGULANMAZ', 'yeni ölçüm yok'),
     ('K2 geleceğe bakma', 'EVET', 'yeni ölçüm yok; kart taslaklarında "t\'de bilinir" tanım alanı ayrı yazıldı; Ç75 / Ç78 geleceğe bakma düzeltmeleri satırında işaretli'),
     ('K3 geçerli bar', 'UYGULANMAZ', 'ölçüm yok'),
     ('K4 tekilleştirme', 'UYGULANMAZ', 'ölçüm yok'),
     ('K5 giriş fiyatı', 'UYGULANMAZ', 'ölçüm yok'),
     ('K6 veri birimi', 'UYGULANMAZ', 'veri okunmadı'),
     ('K7 hayatta kalma', 'EVET', 'K60 / Ç155 / Ç154 satırlarında "yalnız yaşayanlar" yazıldı'),
     ('K8 örneklem ve dönem', 'EVET', 'n < 1.000 → B sınıfı (K58 / Ç175); n kayıtta yoksa "kayıtta yok / B*"; n < 30 hücreler kart taslağında yazılı'),
     ('K9 ön kayıt', 'UYGULANMAZ', 'ön kayıt değil derleme; kartlar ön kayıt değildir (kasa öncesi ana model sabitler)'),
     ('K10 ayrıştırma', 'EVET', 'ana tablo IK_KAYIT\'tan mekanik; IK_KAYIT %d, tablo %d satır (Ç173 / Ç181 / Ç182 bölünmesi); DS 87 / 87, K60 %d çift, kural defteri A-J %d + K %d, Ç204 R15 etiketi cetvel2 YENIDEN_KOSU.md bölüm 4\'ten (yalnız okundu) sayıldı; rastgele 3 satır kayıt metniyle elle karşılaştırıldı (Ç203, Ç181, Ç154)' % (len(IK.IK_KAYIT), len(satirlar), len(k60), len(ust), len(kk))),
     ('K11 yeniden üretim', 'UYGULANMAZ', 'ölçüm yok'),
     ('K12 ifade', 'EVET', 'sayı ile yorum ayrı sütunda; "iz" sözü yalnız kayıttaki etiketten; hiçbir satır İZ yazılmadı'),
     ('K13 süreç', 'EVET', 'yasak defter dosyalarına, .py modüllerine, cetvel2 / KASA dosyalarına dokunulmadı; yeni dosya yalnız hipotez_envanteri.py ve HIPOTEZ_ENVANTERI.md; e-posta / anahtar yok'),
     ('K14 boyut', 'UYGULANMAZ', 'öneri işi değil'),
    ]
    for r in KL:
        w('| %s | %s | %s |' % r)
    w('')
    os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
    with open(CIKTI, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('yazildi', CIKTI, 'satir', len(satirlar), 'kayit', len(IK.IK_KAYIT), 'eksik', eksik, 'fazla', fazla)
    print('karar', dict(karar_say)); print('guv_say', dict(guv_say)); print('kasa evet', len(kasa_evet))
    print('ds', len(ds_rows), len(ds_olc), 'k60', len(k60), 'env', len(env_rows), len(yok), 'ust', len(ust), 'kk', len(kk))
    print('hata sayisi', len(hatalar))


def HATALAR(satirlar, kayit, hmap):
    h = []
    h.append("Kayıtlarda iki ayrı 'K' numaralaması var: kural defteri bölüm K (K1-K51, Cemal'in kör set / hakem dersleri) ile CEMAL_COL_KURALLARI.md (K1-K8, K6b, K10-K49, 15 Kas taslağı; numaralar aynı değil, ör. 'K30 UFUK 15 MUM' orada, kural defterinde K30 fitil teorisi). Ayrıca FON_IZI / K51 / K58 gibi deneme kodları kural numarası değil. Bu envanterde K1-K51 = kural defteri bölüm K; deneme kodları Ç numarasıyla anıldı.")
    h.append("Etiket ile sayı uyumsuzluğu: Ç37 kaydında 'D9 yön ADAY (%56-61); test sürüyor' duruyor; Ç181 ve Ç175 aynı hipotezi 'İZ DEĞİL' (güç yeterli) yazıyor. Ç37 satırı bu envanterde İZ DEĞİL olarak sayıldı; IK_ILERI'de Ç37 ve Ç181a iki ayrı satır (ileri test çift sayılabilir).")
    h.append("Ç175 'İZ DEĞİL'i hak eden gövde' listesine Ç72, Ç86, Ç88, Ç156'yı koyuyor ama Ç72 / Ç86 / Ç88'in kendi satırında ana sayı yok (Ç72 'yeni deneme', Ç86 / Ç88 notu boş). Bu satırlar karar alanı kayıtta olmadan Ç175'ten alındı: kayıtta yok kısmı doğrulanamadı.")
    bos = [s['kod'] for s in satirlar if s['kar'] == 'KYK']
    h.append("Kayıtta sonuç / karar olmayan (not alanı boş ya da 'karar yazılmadı') çalışmalar: %s. Bunlar ölçüldü mü, hangi sonuç çıktı, kayıtta yok; kasa adayı yapılmadı." % ', '.join(bos))
    nn = [s['kod'] for s in satirlar if s['n'] == 'kayıtta yok' and s['kar'] != 'ALT']
    h.append("Kayıtta n (örneklem) hiç yazılı olmayan %d gerçek hipotez satırı var: %s. Bunlar B* (güç bilinmiyor) sayıldı; K8 gereği n olmadan karar sağlam değil." % (len(nn), ', '.join(nn[:60]) + (' ...' if len(nn) > 60 else '')))
    h.append("Aynı kayıt iki farklı cetvelle iki farklı karar taşıyor: Ç37 / Ç181 (D9: 'ADAY' → 'İZ DEĞİL'); Ç75 / Ç78 / Ç179 (düzgün dip, iki yuvarlama: eski 'İZ DEĞİL' → ORTAK_CETVEL 'ÖLÇÜLEMEDİ / PİYANGO'); Ç96 / Ç178 (K24: eski 'İZ DEĞİL' → 'ÖLÇÜLEMEDİ'). Tabloda eski etiket korundu, yeni hüküm 'ana sayı' sütununda.")
    h.append("Ç203 pozitif kontrol (momentum ALT onda h5 +5,3) h5'in oynaklığı ödüllendirdiğini gösterdi; Ç204 CETVEL2 R15 ile Ç194-Ç202'yi yeniden koştu (66 etiket değişti, KATKI+ 0). Ama Ç190-Ç193 yeniden koşulmadı ve Ç124-Ç131 '+%8 önce' cetveli de h5 akrabası: bu satırlarda etiketler h5'e dayanıyor. İlk kart taslağım Ç193 / Ç196 / Ç197 / Ç201 / Ç202 sayılarını 'en yakın' diye öne almıştı; Ç204 geldikten sonra bunlar düşürüldü ya da Ç204 notuyla işaretlendi (kayıttaki Ç193 'en yakın aday' ifadesi Ç204 öncesidir; Ç193 R15 ile yeniden koşulmadı, ancak Ç204 (3) 'Ş1 dipte' sonucu aynı çekirdeği kapsıyor).")
    h.append("K58 yalnız Ç100-Ç151 için yazıldı (IK_ILERI ilk satır); Ç01-Ç98'in eski tek cetveli (önce +%20 ≥ 1,3 kat) için güç ölçülmedi. Bu satırlar B* sayıldı (kayıt: Ç175 yalnız 'en az 20 kayıt' diyor, listesi yukarıdaki Ç38-Ç90 aralığı).")
    h.append("CLAUDE.md 'Test ve bulgu standardı' karar hücrelerini iki kez tanımlıyor: 26 Ekim (BIST 2023, BIST 2024-26, ABD 2023, ABD 2024-26) ve 28 Ekim 'KARAR HÜCRELERİ DEĞİŞTİ' (ABD + AVR dört hücre, BIST bilgi). 26-28 Ekim arası kayıtlar (Ç99-Ç111) eski dört hücre dilini kullanıyor; eski 'iz yok' satırları aynı ölçütle karşılaştırılamaz (kayıtta yazılı hücre kümesi satırdan satıra değişiyor).")
    h.append("SINYAL_ENVANTERI '120 satır' diyor ve tablo A-bölümünde 120 satır ayrıştırıldı (uyuşuyor); ama K60 olasılık tablosundaki ayrı sinyal sayısı 84, K60 kaydı (Ç154) '77 sinyal + 12 bileşik' diyor: 120 - 77 = 43 satırın K60'a girmeme nedeni kayıtta tek tek yazılı değil (veri YOK 4; geri kalanı kayıtta yok).")
    return h


if __name__ == '__main__':
    main()
