# -*- coding: utf-8 -*-
# ozet_guncelle.py — COL_OZET.md'ye bölüm 8 + yeni KISA BLOK yazar (yerinde, tek sefer).
# Kullanım (Colab):  exec(open('/content/drive/MyDrive/col_tarayici/ozet_guncelle.py').read())
# Aynı dosya tekrar çalışırsa eski bölüm 8 ve KISA BLOK silinip yenisi yazılır (tek kopya kalır).
import os, shutil, logging
_oz_log = logging.getLogger('col.ozet')

_OZ_K = '/content/drive/MyDrive/col_tarayici'
_OZ_YOL = f'{_OZ_K}/COL_OZET.md'
_OZ_CIT = chr(96) * 3          # üç ters tırnak; metin içinde düz yazılmadı ki sohbet kod kutusu bozulmasın

_OZ_BOLUM8 = """## 8. 24–25 EYLÜL 2026 — DÖRT SET ÖLÇÜMLERİ, KLASÖR DÜZENİ, ÇAKIŞMA KAPISI

Test setleri: OB24 BIST 24-26 n=2064 · OB23 BIST 2023 n=820 · OBUS ABD 24-26 n=3595 · OBUS21 ABD 22-23 n=3138
(onbellek_ABD_2022_23.pkl). Ölçüm: tekil + ertesi açılış + 120 bar + %0.4 (islemler_olc), bootstrap %90 bant, eşli portföy + plasebo.
Eski %74/+14.8 = aynı sinyaller, ufuk 250 + tekilsiz + maliyetsiz; bugünkü %64/+8.9 temkinli cetvel. Segment kodu (YEREL=5) değişmedi.

KAPANANLAR (4 sette, hiçbiri kural olmadı):
- Sıcak sektör: BIST'te ağır kayıp düşük, ABD 24-26 nötr, ABD 22-23 TERS. Rejime bağlı.
- Hisse momentum 60g: işaret sette göre dönüyor. onc250: bant sıfırı kapsıyor (ABD'de U şekli).
- konum250 (çöl yıllık aralığın neresinde): dipte çöl bek yüksek AMA ağır kayıp da yüksek (3/4 set). Oynaklık.
- Taban koruması / kırılma sayısı: kırılan = daha geniş dağılım (ağır kayıp 4/4 yüksek, bek ABD'de yüksek). Oynaklık.
- Çöl kalitesi (küçük mum, taban, eğim, doji): kayıtların ~%15'i; kazanan %70 / ağır %10 vs %63 / %14.6; bek aynı.
  Tutunma/silkeleme beklemek geç giriş (bek +4 vs +9). Sıkı kapılar 4126 kayıtta 3 işlem bırakır.
- Alt dilim (4h/1h) çöl ölçüleri salınım dibinde: BIST 4h/1h ve yerleşik ABD 1h — hiçbiri (1h CLV BIST'te tek set, ABD'de yok).
TEK CÜMLE: Temiz çöl ağır kayıbı azaltır, beklentiyi artırmaz; büyük kazananlar kirli sıkışmalardan. Sistem = sıkışma kırılımı + trail;
boyut çarpanları (doji, alt fitil, dar hafta, CDS, borç/öz, üç şart) kaliteyi zaten taşır. Oynaklığa göre boyut: DENETIM.portfoy(mod='atr') — karar bekliyor.

QMLS / SALINIM (QMLS_Tarayici): yerleşik evrende 3. dip yazı-tura (ABD 1909: +0.1; BIST 410: −0.8). QMLS o evrende YOKTU (halka arz 16 Tem 2026).
Genç halka arz evreni (evren_kur --genc-ay 24 --genc-min-gun 40, fiyat 1–20$, 169 hisse): 105 sinyal, bek +1.6 [−0.7,+3.9], HEDEF +14.9 / STOP −10.6,
QMLS 15 Eyl sinyali HEDEF +29. 1h dipte CLV düşük (kapitülasyon) ve doji az iyi görünüyor, n=112, bant sıfırı kapsıyor; 1h veri 730 günle sınırlı,
büyütmek için Twelve Data anahtarı (ücretsiz) ya da günlük bar ölçüsü. Açık kalan tek soru budur.

KLASÖR DÜZENİ (25 Eyl): col_tarayici = üretim (BASLAT, COL_v1, DENETIM, onbellek, takip, temel, fon_takip, KALIBRE) + OLCUM.py (ölçüm).
arsiv/desen/ = DESEN_TAM ve desen çıktıları (kapalı proje; OLCUM ile aynı oturumda yüklenmez). QMLS_Tarayici = evren_kur v2.1, salinim_arsivi v1.1d,
dip_olcum v1.2, SEKTOR v1.4, tahtaci/nakit kapıları. ÇAKIŞMA KAPISI: ölçüm dosyaları yüklenirken bellekteki bir adı ezerse durur ve adı yazar.
Uzun iş kuralı: her adımda CSV, kaldığı yerden devam, süre ilk adımdan ölçülür. Drive: Colab'dan yerinde yaz; -1/-2 kopyaları adla düzelt.
"""

_OZ_KISA_GOVDE = """ÇÖL YOLU / BIST+ABD; tam özet Drive: col_tarayici/COL_OZET.md (bölüm 8 = son durum).
Kural: col_segment (yerel=5, ≥20 bar ≤6 ATR) → aday; kapanış>tavan×1.002 → AL; %20 → SMA20 trail; 120 bar; stop yok.
Boyut %6×CDS×borç×doji×fitil×dar×kural, max %12. Aday filtresi yok. Segment kodu değişmedi.
Gerçek sayı (tekil, ertesi açılış, 120 bar): BIST 24-26 %64/+8.9 · BIST 23 %88/+38 · ABD 24-26 %62/+8.3 · ABD 22-23 %62/+4.7.
Test setleri OB24/OB23/OBUS (BASLAT) + OBUS21 (onbellek_ABD_2022_23.pkl). Ölçüm: exec OLCUM.py → islemler_olc/dilim/kiyas/esli_kiyas.
Çakışma kapısı: ölçüm dosyası üretim adını ezerse durur. DESEN_TAM arsiv/desen/ altında, kapalı; OLCUM ile birlikte yüklenmez.
Kapananlar: sektör, momentum, onc250, konum250, taban koruması/kırılma, çöl kalitesi filtresi, tutunma/silkeleme, 4h/1h çöl ölçüleri salınım dibinde,
QMLS tahtacı/nakit/onay/dip sırası, giriş zamanlaması, stoplar, 90+ şekil, KNN, VIX/DXY. Tutanlar: alt fitil<0.12, doji, dar hafta, CDS, borç/öz, üç şart.
Açık: genç halka arz (--genc-ay 24) 3. dip bek +1.6 (n=105), 1h kapitülasyon yönü (n=112) — daha uzun 1h veri (Twelve Data) ya da günlük ölçü.
Kurallar: kod yazmadan önce "yaz"; tek dosya, üretim kalitesi; eski doğru kısımlar korunur; uzun tarama = her adımda CSV + devam; süre ilk adımdan;
test resimlerinde hisse adı yok; Drive'a Colab'dan yerinde yaz. Cemal grafiği okur, karar verir; ben ölçerim. Basit hatayı makineye buldur (kapı, test)."""

def ozet_guncelle(yol=_OZ_YOL):
    if not os.path.exists(yol):
        raise FileNotFoundError(f'{yol} yok — Drive bağlı mı? (drive.mount)')
    s = open(yol, encoding='utf-8').read()
    yedek = yol.replace('.md', '_yedek_20260925.md')
    if not os.path.exists(yedek):
        shutil.copyfile(yol, yedek)                     # tek seferlik yedek, bir şey ters giderse geri dönülür
    for isaret in ('## 8. 24–25 EYLÜL', '## KISA BLOK'):
        i = s.find(isaret)
        if i > 0:
            s = s[:i]
    kisa = '## KISA BLOK (yeni sohbete yapıştır)\n\n' + _OZ_CIT + '\n' + _OZ_KISA_GOVDE + '\n' + _OZ_CIT + '\n'
    s = s.rstrip().rstrip('-').rstrip() + '\n\n---\n\n' + _OZ_BOLUM8 + '\n---\n\n' + kisa
    tmp = yol + '.tmp'
    open(tmp, 'w', encoding='utf-8').write(s); os.replace(tmp, yol)
    print(f'[ok] COL_OZET güncellendi: {len(s):,} karakter -> {yol}')
    print(f'     yedek: {yedek}')
    print('     bölüm 8 var:', '## 8. 24–25 EYLÜL' in s, '| KISA BLOK sayısı:', s.count('## KISA BLOK'))
    return s

_OZ_S = ozet_guncelle()
