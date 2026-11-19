# YAPI_HEDEF 5. TUR — Ş9 "U DİP + PARABOLİK DEVAM" (Y11 / Y11b / Y11c) — İŞ TANIMI
Yazan: ana model, 19 Kas 2026. Kaynak: Cemal, S7 PDF'i No 38 (AVR 2016-22, gelmedi) üzerine: "önce bir dip, sonradan gelen dip o dibin parabolik devamı değil, daha derin bir dip; en son dibin nerede oluşacağını kimse bilemez. İstediğim: seçilen sıkışma bölgesi U dip çizmeli ve parabolik bir devam var görüntüsü olmalı." (CEMAL_COL_KURALLARI K47, kural defteri K40; SINANMADI.)
Yasaklar ve kurallar 4. tur iş tanımıyla AYNI (YAPI_HEDEF_IS_TANIMI_4.md §0 ve giriş): defter dosyalarına, tur/1-3'e, üretim zincirine dokunma; `git add -A` yok; push yok; çakışma kapıları; e-posta / anahtar yok; `python IZ_KARNE.py kontrol istanimi` tablosu ön kayıtta; ik_kontrol_kapisi koşudan önce.

## 1. AMAÇ
S7'nin "kazan sağ kenarı dönmüş" şartı (Ş6: son 5 barın dibi > önceki 10 barın dibi) No 38 gibi alçalan dipler zincirindeki durakları geçirdi. Cemal'in istediği: bölge ve öncesi bir U (çanak) çizsin, dip pencerenin içinde olsun, dipten sonra daha derin dip gelmesin, sağ kenar kalkmış olsun. Bunu tek mekanik şart (Ş9) olarak yaz, Ş6'nın yerine koy ve ölç.

## 2. Ş9 TANIMI (sabit; yalnız [t-40, t-1] geçerli barlar; t = sinyal günü)
W = son 40 geçerli barın Low serisi L_x, x = 0..39 (x = 39 -> t-1). 40 bar yoksa NaN = tutmaz. ATR = ATR250 (öncesi; GOZ_ETIKET F3'teki tanım).
İkinci derece en küçük kareler: L ≈ a x² + b x + c. Özellikler (ozellik_Y1_s9.csv.gz; sembol, tarih):
- F24 = a / ATR (çanak katsayısı; > 0 çanak, < 0 şemsiye),
- F25 = x* / 39, x* = -b / (2a) (dip konumu; a <= 0 ise NaN),
- F26 = R² (uyum iyiliği),
- F27 = (uyum(0) - uyum(x*)) / ATR (sol derinlik; x* pencere dışındaysa uyum(min(max(x*,0),39))),
- F28 = (uyum(39) - uyum(x*)) / ATR (sağ kalkış = parabolik devam),
- F29 = argmin(L) - x* (gerçek en düşük dibin uyum dibinden bar uzaklığı; daha derin dip sonra geldiyse büyük pozitif).
Ş9 TUTAR ⇔ F24 > 0 VE 0,20 <= F25 <= 0,75 VE F26 >= 0,40 VE F27 >= 1,0 VE F28 >= 0,5 VE |F29| <= 5.
TASARIM KONTROLÜ (sonuç OKUMADAN, ön kayıttan ÖNCE, bir kez): (a) S7 PDF'i No 38 olayı (s7_bolge_pdf.py'nin sırasıyla AVR 2016-22 listesinden 7. olay; betikle bul) Ş9'u GEÇMEMELİ; (b) Cemal'in OLUR deyip kazan çizdiği TUR 2 sayfaları 1, 3, 11, 22 (tur_2_anahtar.json) Ş9'u en az 3 / 4 GEÇMELİ. (a) ya da (b) tutmazsa yalnız F26 eşiği (0,30..0,50) ve F25 aralığı (alt 0,15..0,25) BİR KEZ ayarlanabilir; ayar ve gerekçesi ON_KAYIT_5.md'ye yazılır; sonra eşik kilitlenir. Bu kontrol h5 / st5 / getiri OKUMAZ.

## 3. DENEMELER (yön +, giriş t+1 açılış, hat / stop0 Y1 ile aynı)
- **Y11 U DİP ÇEKİRDEK**: Y1 olayı VE Ş1 dipte VE Ş2 hat net VE Ş9. (Az şart: n korunsun.)
- **Y11b S7 v2**: Y10'un sekiz şartı, Ş6 yerine Ş9 (Ş1, Ş2, Ş3, Ş4, Ş5, Ş9, Ş7, Ş8).
- **Y11c Ş9 TEK BAŞINA (bilgi, konumsuz)**: Y1 olayı VE Ş9.
- Huni getirisiz (ön kayıt): Y1 -> +Ş1 -> +Ş2 -> +Ş9 = Y11; Y10 -> Ş6 çıkar Ş9 koy = Y11b; Y1 -> +Ş9 = Y11c; pazar x dönem.

## 4. ÖLÇÜM, ETİKET, KAPILAR: 4. turla AYNI (YAPI_HEDEF_IS_TANIMI_4.md §3), aile 'bh_tur5' (Y11 / Y11b x 4 hücre); BH yalnız n >= 30 hücrelere basılır (4. tur H-d dersi); 'bağımsız' sözü yerine 'kısmen bakılmış (Y9 alt kümesi)' yazılır (H-c). Regresyon: Y1-Y10 eşik sha'ları aynen; Y11* satırları olay_Y1 ile 9 sütunda eşit.
## 5. CEMAL UYUMU: 4. tur §4 gibi (79 sayfa: hakem KÖR 19 + TUR 1 + TUR 2); Ş9 ve Y11 / Y11b / Y11c için tutar / tutmaz x OLUR / OLMAZ / BELİRSİZ; ayrıca S7 PDF'inin 50 olayında Ş9 tutan sayısı (bilgi; No 38 dahil).
## 6. TUR 4 KURU SAYIM: T1.5 = T1.4 ama deneme Y11; gösterilmemiş uygun olay sayıları; `tur ac --no 4` KOŞULMAZ.
## 7. ÇIKTILAR: YAPI_HEDEF.py (yh_s9_ozellik, Y11*), test_yapi_hedef.py (F24-F29 yapay vakalar: tam parabol geçer, alçalan zincir geçmez, düz taban F27 < 1 geçmez, şemsiye a < 0 geçmez; prefix), GOZ_ETIKET.py ge_tur_esik(5) T1.5 (TUR 1-3 kapısı), ON_KAYIT_5.md (tasarım kontrolü sonucu dahil; koşudan ÖNCE commit), RAPOR_5.md (4. tur biçimi + 'İLERLEME' tablosu: Y1, Y9, Y9b, Y10, Y11, Y11b için hücre başına n ve P(+5) olay / eş; satır dosyalarından), olay_Y11*.csv.gz, sonuc.json. İki commit (ön kayıt; koşu), mesaj sonu:
  Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01F7vgWZPNpBhrsGQEHDtRis
## 8. RAPOR: 4. tur biçimi + tasarım kontrolü sonucu (No 38 geçti mi, TUR 2 kazan sayfaları kaçı geçti, ayar yapıldı mı) + ilerleme tablosu + HATA + KONTROL LİSTESİ + Colab notu.
