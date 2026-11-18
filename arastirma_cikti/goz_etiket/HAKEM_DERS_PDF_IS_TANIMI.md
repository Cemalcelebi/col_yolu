# İŞ TANIMI: HAKEM DERS PDF'i — Cemal'in çizimleri + sonrası + puan + ders (18 Kas 2026)

## YASAKLAR
GOZ_ETIKET_IS_TANIMI.md §2 aynen (defter dosyalarına dokunma; `git add -A` yok; push yok). Yeni ölçü hesaplama; sayılar hakem_cevap_cemal.json, hakem_anahtar.json, anahtar.json, olay_Y1.csv.gz ve HAKEM_DERSLER.md'den. GOZ_ETIKET.py'ye dokunma (ayrı betik: arastirma_cikti/goz_etiket/hakem_ders_pdf.py).

## AMAÇ (Cemal: 'puan ver; aynı hataları yapmayalım; göz aşinalığı; ders çıkarmaya odaklan; önce eski PDF'teki yanlışlarımı ve doğrularımı aynı çizim PDF'inde görmeliyim')
Cemal'in el yazısıyla işaretlediği hakem PDF'i: /tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/hakem_ders/CEMAL_ISARETLI_HAKEM.pdf (40 sayfa; sayfa k = hakem sayfası k). Bu sayfaların görüntüsü (pdftoppm, 110 dpi) ders PDF'inin sol yarısına konur; sağ yarıya AYNI olayın grafiği SONRASI AÇIK çizilir (sinyal öncesi 60 bar + giriş + sonraki 20 bar; giriş noktası, +%5 / +%10 çizgileri, stop0, gerçekleşen çıkış; hacim; fiyat gerçek fiyat; HİSSE ADI YİNE YOK, yalnız pazar). Her olayın kimliği: hakem_anahtar.json 'sayfa' -> no -> anahtar.json 'olay' -> olay_Y1 satırı (h5, h10, st5, k5, getiri, cikis_bar, cikis_tur); veri /tmp/veri (OC_VERI) ile grafik.

## SAYFA DÜZENİ (A4 yatay, 40 ders sayfası + 1 kapak + 1 özet)
- Başlık: 'Sayfa k · Cemal: OLUR / OLMAZ / BELİRSİZ (kör) ya da DOĞRU / YANLIŞ (açık; vekil kararı: ...) · SONUÇ: +%5 gün g / +%10 gün g / STOP gün g / sönük · PUAN: +1 / -1 / 0'.
- PUAN kuralı (CLAUDE.md Hakem turları): OLUR ve +%5 geldi = +1; OLUR ve gelmedi = -1; OLMAZ ve gelmedi = +1; OLMAZ ve geldi = -1; BELİRSİZ / yanıtsız = 0 (ayrı sayılır). Açık yarıda Cemal'in etkin kararı: DOĞRU -> vekil kararı; YANLIŞ -> tersi (OLMAZ -> OLUR; OLUR / BELİRSİZ -> OLMAZ). Vekil için aynı puan.
- Altta 3 satır: (1) Cemal'in notu (hakem_cevap_cemal.json 'not'); (2) vekilin kararı ve neden kodları (hakem_anahtar.json); (3) DERS: HAKEM_DERSLER.md'deki ilgili CD / VD maddesi (sayfa eşlemesi orada); ders yoksa 'doğru karar: ...' tek cümle (hangi kural tuttu). Yanlış sayfalarda ders kutusu kırmızı çerçeveli, doğru sayfalarda yeşil.
- Kapak: puan tablosu (kör yarı / açık yarı / toplam: Cemal ve vekil; karar sayısı, +1, -1, başarı %, taban = eş payı), 'aynı hatayı yapmama listesi' (CD1-CD7 kısa), göz aşinalığı notu (hangi şekiller hedefe gitti: kazan + dönüş; hangileri gitmedi: tepede raf, en güzel taban).
- Özet sayfa: 40 satırlık tablo (sayfa, Cemal, vekil, sonuç, puan C, puan V, ders kodu).

## ÇIKTI
arastirma_cikti/goz_etiket/HAKEM_DERS_2026-11-18.pdf (< 15 MB) + hakem_ders_pdf.py. Commit (adlı dosyalar; mesaj Türkçe, sonuna "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" ve "Claude-Session: https://claude.ai/code/session_01F7vgWZPNpBhrsGQEHDtRis"). Raporunda: SONUÇ (puan tablosu sayıları), HATA, ÖNERİLEN KAYIT; sayfa görüntülerinin Cemal'in PDF'inden alındığını ve hisse adı olmadığını doğrula (pdftotext).
