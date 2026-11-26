# MUM_IZI24 ÖN KAYIT — KODUN SEÇTİĞİ BÖLGELER (2026-11-26T17:01:41Z)

Aday kuralı havuzu (MUM_IZI8 v5M, evren içi) + mum boyu kapısı (ORAN <= 0,70) = 'kodun seçtiği bölgeler'; göz onayı YOK. Cemal'in göz onayı (geçmişli sayfa, 24 bölge): kodun gösterdiği bölgelerin %42'si BENZİYOR, %75'i BENZİYOR ya da KISMEN; bu yüzden sonuç 'kalıbın sonucu' diye okunmaz. Bu dosya bütün getiriler (olay ve KAPISIZ kontrol) hesaplanmadan ÖNCE commit + push edilir; tanımlar, eşikler, hücreler ve hüküm kuralı sonra değişmez (değişirse SAPMA). Evren bugün yaşayan hisseler: sonuç yukarı yanlı. KASA açılmaz (veri <= 2022-12-31).

## Mühürler

KOD24_SHA: d8b69d84178acd6f1ee36038acc9f0ecfb82cd97c725cc7f1c40c45380789369
ESIK24_SHA: 9ed1542a127183edfe8a014173ef4bc37b9222a17a5bdf741c4770552fc585eb
HK_KOD_SHA: c0c7dbfad35634d67e88629f1fbed32be825dfcef1cd6ff9fc686e7324a0578a
GZ_KOD_SHA: f0b0381a4eabe14a015dc6eb929fcc34a1d95d2a399412cc05a5620c4ffb68d5
ESIK11_SHA: ea7535ce7ba59c64e6c5e934aa3722cbedb3786ddfe1f52d05b676d8bb315d75
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9
MV_KOD_SHA: 1bb586cb825b8b437b97df4ec193a682bc626ecc796e9130d27e4906b68d81dc
MH_KOD_SHA: 8f7440d199dfcf018f838da77da5cf0eabd89062fdc67cf26a0a5678ed4da200
HAVUZ_HAM_SHA: d0d919f16a1a9e7af04a57650a0627a80a7fe6592c2f79d7ff1eb72837583698
HARIC21_SHA: 0e1b3d34e5a93d8cc7ff523168c1cecdba06733503cc0fbc54faa929b00d3946
HARIC22_SHA: c36ca3e2b78a5226f786beb10e094a9f198a1cf229d3526a7895dd6894bda069
IS_TANIMI_SHA: 453a397171195d4920676ef2364b05fbf343e0578873fff9b67272a62e36db42
SAYIM_SHA: e60726df77c6e0693e99e2aaf504f02a306c2bd5c73069890992ed5b50721d10

- MUM_IZI_HAVUZ.py commit'i: ae2a235b7016acbbc7c5bc435741435064de168a 2026-11-26T16:57:50+00:00

## GETİRİSİZ SAYIM (olay ve eş getirisi hesaplanmadı; yalnız ORAN, kapı, hariç, veri kapıları, takvim, eş uygunluğu)

- Huni: {"ham_evren": 6011, "tekil_atilan": 0} (havuz tekilse 15 bar tekilleştirme 0 atar)
- gunluk: havuz 4612 (ORAN olan 4607, ORAN_YOK 5; KAPILI payı 0,066)
  - KAPILI: toplam 306, hariç tam 49 / yakın 1, ANA 256, ANA ölçülebilen 256, ANA eşli 231; hepsi ölçülebilen 305, hepsi eşli 273; ölçülemedi {"giris_stop_altinda": 1}; eşsiz {"es_az": 20, "kova_yok": 12}; ANA eşli pazar {"ABD": 138, "BIST": 76, "AVR": 17}; en geç 15. mum 2022-09-20
  - KAPISIZ: toplam 4301, hariç tam 44 / yakın 6, ANA 4251, ANA ölçülebilen 4245, ANA eşli 4056; hepsi ölçülebilen 4295, hepsi eşli 4103; ölçülemedi {"ufuk_kesik": 4, "giris_stop_altinda": 2}; eşsiz {"es_az": 154, "kova_yok": 38}; ANA eşli pazar {"ABD": 3084, "BIST": 588, "AVR": 384}; en geç 15. mum 2022-12-28
- haftalik: havuz 1399 (ORAN olan 1361, ORAN_YOK 38; KAPILI payı 0,108)
  - KAPILI: toplam 147, hariç tam 14 / yakın 0, ANA 133, ANA ölçülebilen 127, ANA eşli 122; hepsi ölçülebilen 141, hepsi eşli 136; ölçülemedi {"ufuk_kesik": 6}; eşsiz {"es_az": 5}; ANA eşli pazar {"ABD": 91, "BIST": 17, "AVR": 14}; en geç 15. mum 2022-12-30
  - KAPISIZ: toplam 1214, hariç tam 35 / yakın 8, ANA 1171, ANA ölçülebilen 1147, ANA eşli 1088; hepsi ölçülebilen 1190, hepsi eşli 1131; ölçülemedi {"ufuk_kesik": 24}; eşsiz {"es_az": 57, "kova_yok": 2}; ANA eşli pazar {"ABD": 839, "BIST": 146, "AVR": 103}; en geç 15. mum 2022-12-30

| zaman | hücre | rol | KAPILI ANA ölçülebilen | KAPILI ANA eşli | güç (karar eğrisi) | güç cetvel2 / plasebo | KAPILI hepsi eşli | KAPISIZ ANA eşli | beklenen |
|---|---|---|---|---|---|---|---|---|---|
| gunluk | ABD|d1619 | KARAR | 64 | 63 | 0,26 | 0,26 / 0,49 | 76 | 1616 | beklenen ÖLÇÜLEMEDİ ya da TUTAR (güç < 0,80: TUTMADI yazılamaz) |
| gunluk | ABD|d2022 | KARAR | 75 | 75 | 0,24 | 0,24 / 0,27 | 96 | 1468 | beklenen ÖLÇÜLEMEDİ ya da TUTAR (güç < 0,80: TUTMADI yazılamaz) |
| gunluk | AVR|d1619 | KARAR | 11 | 11 | 0,09 | 0,09 / 0,24 | 12 | 236 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| gunluk | AVR|d2022 | KARAR | 6 | 6 | 0,06 | 0,06 / 0,16 | 8 | 148 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| gunluk | BIST|d1619 | BİLGİ | 39 | 31 | 0,18 | 0,18 / 0,12 | 32 | 298 | beklenen ÖLÇÜLEMEDİ ya da TUTAR (güç < 0,80: TUTMADI yazılamaz) |
| gunluk | BIST|d2022 | BİLGİ | 61 | 45 | 0,19 | 0,19 / 0,16 | 49 | 290 | beklenen ÖLÇÜLEMEDİ ya da TUTAR (güç < 0,80: TUTMADI yazılamaz) |
| gunluk | ABD|o16 | BİLGİ | 0 | 0 | - | - / - | 0 | 0 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| gunluk | AVR|o16 | BİLGİ | 0 | 0 | - | - / - | 0 | 0 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| gunluk | BIST|o16 | BİLGİ | 0 | 0 | - | - / - | 0 | 0 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| haftalik | ABD|d1619 | KARAR | 13 | 13 | 0,06 | - / 0,06 | 14 | 143 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| haftalik | ABD|d2022 | KARAR | 8 | 8 | 0,03 | - / 0,03 | 8 | 288 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| haftalik | AVR|d1619 | KARAR | 3 | 3 | 0,05 | - / 0,05 | 3 | 23 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| haftalik | AVR|d2022 | KARAR | 1 | 1 | 0,04 | - / 0,04 | 1 | 32 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| haftalik | BIST|d1619 | BİLGİ | 10 | 7 | 0,04 | - / 0,04 | 8 | 85 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| haftalik | BIST|d2022 | BİLGİ | 11 | 10 | 0,03 | - / 0,03 | 14 | 61 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| haftalik | ABD|o16 | BİLGİ | 71 | 70 | 0,19 | - / 0,19 | 78 | 408 | beklenen ÖLÇÜLEMEDİ ya da TUTAR (güç < 0,80: TUTMADI yazılamaz) |
| haftalik | AVR|o16 | BİLGİ | 10 | 10 | 0,07 | - / 0,07 | 10 | 48 | beklenen ÖLÇÜLEMEDİ (n < 30) |
| haftalik | BIST|o16 | BİLGİ | 0 | 0 | - | - / - | 0 | 0 | beklenen ÖLÇÜLEMEDİ (n < 30) |

- Güç: günlük karar eğrisi cetvel2_guc_v2.2 (H 15); haftalık karar eğrisi plasebo (eş üyelerinin farkı; olay getirisi kullanılmaz); delta +0,02, eşik 0,80.
- Güç eğrisi bilgisi ve hücre başı ayrıntı: sayım json'u (SAYIM_SHA; /tmp/mum_izi/havuz/sayim.json, sonuç json'una da yazılır).
- BEKLENEN ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80; ölçüm yine koşulur): günlük ['ABD|d1619', 'ABD|d2022', 'AVR|d1619', 'AVR|d2022']; haftalık ['ABD|d1619', 'ABD|d2022', 'AVR|d1619', 'AVR|d2022'].

## Ölçü, eş, hücre, hüküm (HV_ESIK; sha yukarıda; sonuçtan sonra değişmez)

```
{
 "surum": "HV-1.0",
 "havuz": "MUM_IZI8 taramasının v5M ('R4+M') VAR olayları, evren içi (HK.hk_olaylar; ham dosya sha mum_izi8_tarama.json ile); günlük ve haftalık ayrı zaman dilimi",
 "oran": "HK.hk_olay_oran (hk_boy_olcu; ORAN = bölge barlarında (H - L) / C medyanı / bölgeden önceki 120 barın medyanı, en az 40 bar; yalnız bölge sonu t'ye kadarki barlar); ikinci tanım yok",
 "kapi": {
  "oran_en_cok": 0.7,
  "tanim": "KAPILI = HK.hk_kapi(ORAN) (sonlu ve <= 0,70, sınır dahil); KAPISIZ = ORAN sonlu ve > 0,70; ORAN yok (önceki < 40 bar) -> 'ORAN_YOK' (iki gruba da girmez; sayısı yazılır)"
 },
 "tekil": {
  "bar": 15,
  "tanim": "aynı zaman dilimi ve hissede olaylar bölge sonu bar sırasıyla; son TUTULAN olaydan < 15 bar sonraki olay atılır (ilki kalır); havuzun tamamında (KAPILI + KAPISIZ + ORAN_YOK birlikte), kapıdan önce"
 },
 "haric": {
  "yakin_bar": 15,
  "tanim": "mum_izi21_olay.csv (181 bölge; zaman, sembol, bolge_son) + MUM_IZI22_onay_anahtar.json (24 bölge; zaman, sembol, bolge_son): aynı zaman dilimi + aynı hisse + bölge sonu bar farkı <= 15 (tam eşleşme 0 dahil; sonrası örtüşür) -> HARİÇ (ANA ÖRNEK'e girmez; DUYARLILIK'ta dahil); hem KAPILI hem KAPISIZ olaylarda aynı kural; tam / yakın sayıları ayrı yazılır"
 },
 "olcu": {
  "tanim": "GZ.gz_olc_bir AYNEN (GZ_ESIK['olcu']; ESIK11_SHA): giriş = bölgeden sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk günü), ufuk 15 mum, R15 = 15. mumun kapanışı / giriş - 1, stop = bölge dibi x 0,98, giriş <= stop ölçülmez, 15. mum > 2022-12-31 ölçülmez (ufuk_kesik), dokunma = High >= giriş x (1 + x) ilk gün Low <= stop ilk günden ÖNCE (aynı gün stop önce)",
  "hedef": "+%5 ve +%10 her iki dilimde: günlük GZ d5 / d10; haftalık d10 = GZ d10, d5 = G2.k17_dokunma (aynı kural; denetim: k17_dokunma +%10 = GZ d10, değilse DUR)",
  "getirisiz_gecit": "G2.k17_gecit_bir (gz_olc_bir kapıları aynen; getiri hesaplamaz); hesapta gz_olc_bir ile birebir aynı olmalı (DUR)"
 },
 "es": {
  "tanim": "GZ.gz_es_grup AYNEN (CETVEL2 v2.2 c2_panel22_al ufuk 15 önbelleksiz; aynı giriş günü, aynı kova KV, >= 5 eş, aynı takvim aralığı, eş stop'u bölge takvim aralığında eşin dibi x 0,98, giriş > stop); panel GZ.gz_es kuralı (günlük açık kopya; haftalık bölge sonu <= 2015-12-31 -> p1, değilse açık kopya; BIST p1 yok -> panel_yok); eş hedefleri +%5 / +%10 için olay satırı gz_es_grup'a zaman 'gunluk' ile verilir (gz_es_grup zamanı yalnız hedef listesi için okur)",
  "dislama": "aynı gün KAPILI ya da KAPISIZ (ya da ORAN_YOK) olayı olan hisseler eşten dışlanır: o pazardaki havuzun BÜTÜN olaylarının (iki zaman dilimi, hariç dahil) giriş günleri; olayın kendisi gz_es_grup içinde dışlanır",
  "uye": "slot portföyü ve güç plasebosu için eş üyelerinin R'leri hv_es_uye ile (gz_es_grup'un uygunluk adımları aynen); denetim: üye sayısı = n_es ve üye ortalaması = es_R15 (1e-9), değilse DUR"
 },
 "hucre": {
  "donem": {
   "o16": [
    "1990-01-01",
    "2015-12-31"
   ],
   "d1619": [
    "2016-01-01",
    "2019-12-31"
   ],
   "d2022": [
    "2020-01-01",
    "2022-12-31"
   ]
  },
  "atama": "giriş tarihine göre (pazar x dönem)",
  "karar": [
   "ABD|d1619",
   "ABD|d2022",
   "AVR|d1619",
   "AVR|d2022"
  ],
  "bilgi": [
   "BIST|d1619",
   "BIST|d2022",
   "ABD|o16",
   "AVR|o16",
   "BIST|o16"
  ]
 },
 "istat": {
  "c2_hucre": "C2.c2_hucre(R15, es_R15, sira, giris, '+', tohum_ek, egri=None, perm=True): n (eşli), ort / medyan FARK, ort SIRA, AY KÜMELİ bootstrap %95 (YH.yh_d3_boot_l3o; C2_ESIK boot B 2000, tohum 2111), p = DS.ds_perm_p ay kümeli işaret permütasyonu (R 10.000, tohum 2113 + tohum_ek, tek yönlü +); L3O yalnız bilgi (hükme girmez)",
  "tohum_ek": "zaman 0 / 1 x 1000 + grup (KAPILI 0, KAPISIZ 1, KAPILI_DUY 2, KAPISIZ_DUY 3) x 100 + hücre sırası (karar 0-3, bilgi 4-8, hepsi 9)",
  "hedef_payi": "+%5 payı (d5) ve +%10 payı (d10) ölçülen olaylarda; EŞLİ HEDEF PAYI = eşli olaylarda d5 payı - es_d5 ortalaması (d10 aynı)",
  "esinden_iyi": "fark > 0 payı (eşli olaylar)"
 },
 "slot": {
  "yuva": 10,
  "rastgele": 200,
  "tohum": 26112401,
  "esik": 0.9,
  "tanim": "BOFA_IZI.bi_slot AYNEN: eşli olaylar giriş günü sırasıyla (eşitlikte sembol), yuva serbest ise (önceki çıkış günü <= giriş günü) alınır, 15. mumun son günü çıkar, getiri R15; rastgele: her olay yerine aynı gün aynı kovadan rastgele bir eş üyesinin R'si (aynı giriş / çıkış günleri), 200 portföy; YÜZDELİK = rastgele portföylerin gerçekten küçük olanlarının payı; şart: gerçek > rastgelelerin %90 yüzdeliği (np.quantile 0,90)"
 },
 "guc": {
  "delta": 0.02,
  "esik": 0.8,
  "tohum": 26112402,
  "gunluk": "C2.c2_guc(n, C2._c2_egri22_al(pazar, dönem, 15, None)) (cetvel2_guc_v2.2.json H 15; 'o16' -> 'acik' eğrisi)",
  "haftalik": "cetvel2'de 15 haftalık ufuk yok -> plasebo eğrisi: hücrenin ANA olaylarının (KAPILI + KAPISIZ) >= 6 üyeli her eş kümesinden rastgele bir üye (tohum 26112402), fark = üye R - öteki üyelerin ortalaması; C2.c2_guc_egri(fark, tohum_ek) ve C2.c2_guc(n, eğri); olay getirisi kullanılmaz",
  "bilgi": "günlükte plasebo eğrisi güçü de bilgi olarak yazılır"
 },
 "hukum": {
  "tutar": "n >= 30 VE ort FARK > 0 VE ay kümeli boot alt > 0 VE ort SIRA > 0,50 VE slot portföyü > 200 rastgele portföyün %90 yüzdeliği",
  "tutmadi": "TUTAR değil VE n >= 30 VE güç >= 0,80",
  "olculemedi": "ötekiler (n < 30 ya da güç < 0,80)",
  "anlamli": "pozitif anlamlı = n >= 30, FARK > 0, boot alt > 0; negatif anlamlı = n >= 30, FARK < 0, boot üst < 0",
  "genel": "zaman dilimi başına dört karar hücresi: (1) en az bir pozitif anlamlı VE en az bir negatif anlamlı -> 'ÇELİŞKİLİ'; (2) dördü TUTAR -> 'AÇIK VERİDE TUTUYOR (birleşik iz bileşeni adayı; kasa açılmaz)'; (3) en az biri TUTMADI ve hiçbiri TUTAR değil -> 'TUTMADI'; (4) ötekiler -> 'ÖLÇÜLEMEDİ' (eksik hücreler yazılır)",
  "ornek": "hüküm ANA ÖRNEK KAPILI ile; DUYARLILIK (hepsi dahil) ayrı satır; KAPISIZ bilgi"
 },
 "kapi_etkisi": {
  "perm": 10000,
  "tohum": 26112403,
  "boot": 2000,
  "tohum_boot": 26112404,
  "tanim": "KAPILI - KAPISIZ ort eşli FARK farkı (ANA örnek; eşli olaylar); p = tabakalı permütasyon: grup etiketleri (pazar x giriş ayı) tabakaları içinde karıştırılır, iki yönlü, 10.000; %95 = giriş ayı kümeli bootstrap (aylar yerine koyarak, B 2000); zaman dilimine göre (bütün pazar / dönemler) ve dört karar hücresinde ayrı"
 },
 "bh": {
  "q": 0.1,
  "aile": "2 zaman dilimi x 4 karar hücresi (ANA KAPILI); p = c2_hucre p (ay kümeli işaret, tek yönlü +); BİLGİ satırı (hükme girmez)"
 },
 "kesik": "veri en büyük tarihi <= 2022-12-31 (assert, her blok) + KASA.kasa_kapisi (gz_kos ile aynı dosyalar)"
}
```

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = GZ.gz_es_grup (aynı giriş günü, aynı kova, aynı takvim aralığı, aynı stop geometrisi, >= 5 eş); eş dışlama havuzun bütün olayları (KAPILI + KAPISIZ + ORAN_YOK, iki zaman dilimi); slot tabanı 200 eşli rastgele portföy (aynı gün aynı kova); aynı bağlam kontrolü KAPISIZ = aynı aday kuralının ORAN > 0,70 olayları (KAPI ETKİSİ, tabakalı permütasyon) |
| K2 | geleceğe bakma | EVET | ORAN yalnız bölge sonu t'ye kadarki barlardan (HK.hk_boy_olcu assert); aday kuralı olayları tarama anında o güne kadarki veriyle; giriş bölgeden SONRAKİ ilk geçerli bar açılışı; eş kovası giriş günü KV satırı; hariç listesi ve kapı getiriden bağımsız; veri <= 2022-12-31 assert + KASA kapısı |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar (H > L, V > 0); haftalık barlar tamamlanmış ISO haftaları (MH / MV aynen); GZ kapıları aynen |
| K4 | tekilleştirme | EVET | aynı hissede < 15 bar arayla ikinci olay atılır (hv_tekil; havuz tekil ise 0 yazılır); bölge kimliği zaman + sembol + bölge sonu tekil (DUR); ortalama yanında medyan |
| K5 | giriş fiyatı | EVET | giriş = bölgeden sonraki ilk geçerli barın açılışı (gz_olc_bir; haftalıkta sonraki haftanın ilk günü açılışı); giriş <= stop ölçülmez (sayısı yazılır) |
| K6 | veri birimi | EVET | MI bölünme düzeltmeli fiyatlar (GZ aynen); getiriler oransal; ABD USD, AVR yerel para, BIST TL; karar eşli farkla (aynı pazar aynı gün) |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı): sonuç 'yukarı yanlı' okunur; eşli fark aynı evrenle kurulduğu için yanlılık kısmen düşer, kalkmaz; kasa açılmaz |
| K8 | örneklem ve dönem | EVET | n < 30 hücre ÖLÇÜLEMEDİ (getirisiz sayımda beklenen yazılır); iki alt dönem (2016-19, 2020-22) ve iki pazar ayrı hücre; BH q 0,10 bilgi satırı (2 x 4 aile); küçük hücreden 'bulgu' denmez |
| K9 | ön kayıt | EVET | MUM_IZI24_ON_KAYIT.md: KOD24_SHA, ESIK24_SHA, GZ / G2 / HK / MI kod sha, ham havuz sha, hariç dosya sha, SAYIM_SHA + getirisiz sayım + güç; getiriler bu commit + push'tan sonra; hv_kapi: kontrol kapısı + sha + commit + temiz ağaç + sayım eşitliği |
| K10 | ayrıştırma | EVET | havuz ham dosyası mühürle (HK.hk_olaylar); olay indeksi taramayla (hk_olay_oran DUR); hariç dosyalarının şeması (sütun / anahtar) denetlenir; bölge kimliği tekil (DUR); bölge başı / sonu / giriş / 15. mum tarihleri getirisiz ve hesap aşamasında birebir (DUR) |
| K11 | yeniden üretim | EVET | getirisiz geçit = gz_olc_bir (DUR); k17_dokunma +%10 = GZ d10 (DUR); eş üyeleri = gz_es_grup n_es / es_R15 (DUR); rapordan önce >= 2 hücre olay csv'sinden bağımsız kısa kodla yeniden üretilir |
| K12 | ifade | EVET | başlık 'KODUN SEÇTİĞİ BÖLGELER'; 'kalıbın sonucu' denmez (göz onayı %42 BENZİYOR / %75 BENZİYOR ya da KISMEN); 'iz' sözü yalnız hüküm kuralıyla; sayı ile yorum ayrı cümlede |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_hv); MUM_IZI_HAKEM / GOZ / GOZ2 ve defter dosyaları değişmez (yalnız import); yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez, kasa açılmaz |

## SAPMA

(ön kayıt anında yok)
