export const meta = {
  name: 'k57-denetim-test-envanteri',
  description: 'K51-K56 testlerini birim birim denetle (13 soru + A-D sınıfı), iki bağımsız doğrulayıcı, itirazlı sınıflara hakem',
  phases: [
    { title: 'Denetim', detail: 'her çalışma birimi için kaynak + kod + ön kayıt okunarak test satırları' },
    { title: 'Dogrulama', detail: 'V1 kaynak doğruluğu, V2 sınıf / mantık / eksiklik (bağımsız)' },
    { title: 'Tamamlama', detail: 'V2 eksik test bulduysa aynı şemayla doldur' },
    { title: 'Hakem', detail: 'sınıf itirazlarında üçüncü okuyucu' },
  ],
}

const REPO = '/home/user/col_yolu'
const ALANLAR = 'A1 Fiyat davranışı; A2 Hacim ve işlem akışı; A3 Volatilite ve risk rejimi; A4 Zaman ve süre davranışı; A5 Piyasa mikro yapısı; A6 Göreceli güç ve piyasa konumu; A7 Şirket temelleri; A8 Sahiplik, sermaye ve kurumsal olaylar; A9 Sektör, makroekonomi ve dış etkenler; A10 Birleşik davranışlar ve alanlar arası ilişkiler'
const SINIFLAR = `A = Geçerli ve yeterli test: soruyu cevaplayacak biçimde tasarlanmış; veri, örneklem ve yöntem yeterli; yanlılık / sızıntı / bağımlılık / çoklu test kontrol edilmiş; sonuç (olumlu ya da olumsuz) ilgili soruya güvenle bağlanabilir.
B = Geçerli fakat sınırlı test: yöntem sağlam ama kapsam, veri, güç, dönem ya da evren sınırlı; sonuç yalnız dar bir soruya cevap verir.
C = Yöntemsel olarak sorunlu test: sonucu geçersiz kılabilecek ya da yanıltabilecek tasarım / uygulama kusuru var (sızıntı, seçim etkisi, yanlış gözlem birimi, bağımlılığın ihmali, ölçümün sorulan mekanizmayı ayırt etmemesi, kontrolün yetersizliği).
D = Veri yetersizliği nedeniyle cevaplanamayan test: planlandı / koşuldu ama veri yetersiz; sonuç VERİ YETERSİZ ya da yalnız vekil (proxy) ölçüme dayanıyor.
(E = hiç test edilmemiş soru: test satırı değil, soru düzeyinde tutulur; bu görevde E yazma.)`
const KURALLAR = `ÇALIŞMA KURALLARI (kesin):
- Depo: ${REPO}. YALNIZ OKU: dosya yazma, düzenleme, git komutu (status/log/show/diff dışında), ağ isteği, K55 / K56 boru hattı koşturma YOK. Hafif okuma serbest (cat, sed -n, grep, head, python ile küçük CSV okuma).
- Hiçbir bilgi uydurma. Kaynakta yoksa o alana "KAYITLI DEĞİL" yaz. Her iddiayı kaynak_atiflari içinde dosya yolu + bölüm / satır / sütun ile ilişkilendir.
- Önemli ilke: Bir sorunun önceden test edilmiş olması doğru test edildiği anlamına gelmez; yöntemsel kusur bulunması da hipotezi otomatik doğru yapmaz. Sonucu bu iki yanlışlıktan ayrı tut.
- Kendi bulgunu yumuşatma: gerçek kusurları somut yaz (hangi adım, neden sonucu etkiler, etkinin yönü). Kusur yoksa "belirgin kusur bulunamadı" de ve bunu neyi okuyarak söylediğini yaz.
- Türkçe yaz, kısa ve somut. Her metin alanı en çok ~450 karakter. Sayıları kaynaktaki gibi ver.
- Gözlem kapsamı: K51-K56 (ABD Çöl Yolu araştırma hattı). K51 öncesi BIST çalışmaları (K1-K50, FON_IZI.py, COL_OZET.md kapalı konular) denetim kapsamı dışıdır; yalnız ilgili olduğunda "onceki_ilgili_calismalar" içinde ad olarak an.
- Başlangıç noktaları: ${REPO}/IZ_DEFTERI.md (ilgili Ç satırları ve DERS bölümleri; 'grep -n "K5x" IZ_DEFTERI.md'), ${REPO}/CLAUDE.md (Cemal'in tanımları), ${REPO}/COL_OZET.md, ilgili ön kayıt dosyaları, çıktı klasörleri ve kod.`
const ALAN13 = `HER TEST İÇİN CEVAPLANACAK SORULAR (Cemal'in listesi): (1) Hangi soruya cevap vermek üzere tasarlandı? (2) Hangi davranışı ölçüyor? (3) Veri kaynağı ve veri kapsamı? (4) Örneklem hangi şirketleri içeriyor? (5) Batan, delist olmuş, birleşmiş şirketler nasıl ele alındı? (6) Olay başlangıcı nasıl tanımlandı? (7) Gözlem birimi hisse / gün / olay / işlem / şirket? (8) Aynı şirketten gelen bağımlı gözlemler nasıl ele alındı? (9) Eşleştirme hangi değişkenlerle yapıldı? (10) Gelecek bilgisi sızıntısı ve seçim yanlılığı nasıl kontrol edildi? (11) Çoklu test ve aşırı uyum nasıl kontrol edildi? (12) Ölçüm, sorulan mekanizmayı gerçekten ayırt edebiliyor mu? (13) Negatif sonuç hangi alternatif açıklamaları dışlıyor, hangilerini dışlamıyor?`

const TEST_ITEM = {
  type: 'object',
  properties: {
    test_id: { type: 'string', description: 'birim öneki + sıra, örn. K51A-T03' },
    ad: { type: 'string' },
    soru: { type: 'string' },
    olculen_davranis: { type: 'string' },
    alanlar: { type: 'array', items: { type: 'string' }, description: 'A1..A10 kodları, ana alan ilk' },
    veri_kaynagi_kapsam: { type: 'string' },
    orneklem: { type: 'string' },
    batan_delist_birlesme: { type: 'string' },
    olay_baslangici: { type: 'string' },
    gozlem_birimi: { type: 'string' },
    bagimli_gozlem: { type: 'string' },
    eslestirme: { type: 'string' },
    sizinti_secim_yanliligi: { type: 'string' },
    coklu_test_asiri_uyum: { type: 'string' },
    mekanizma_ayirt_edebilir_mi: { type: 'string', description: 'EVET / KISMEN / HAYIR + gerekçe' },
    negatif_dislananlar: { type: 'string' },
    negatif_dislanmayanlar: { type: 'string' },
    sonuc: { type: 'string', description: 'kayıtlı karar + ana sayılar' },
    sinif: { type: 'string', enum: ['A', 'B', 'C', 'D'] },
    sinif_gerekcesi: { type: 'string' },
    kusurlar: { type: 'array', items: { type: 'string' }, description: 'somut kusur: adım + etki yönü; yoksa boş dizi' },
    onceki_ilgili_calismalar: { type: 'array', items: { type: 'string' } },
    onkayit_dosya: { type: 'string' },
    kod_dosya: { type: 'string' },
    kosu_kimligi: { type: 'string' },
    kaynak_atiflari: { type: 'array', items: { type: 'string' } },
  },
  required: ['test_id', 'ad', 'soru', 'olculen_davranis', 'alanlar', 'veri_kaynagi_kapsam', 'orneklem', 'batan_delist_birlesme', 'olay_baslangici', 'gozlem_birimi', 'bagimli_gozlem', 'eslestirme', 'sizinti_secim_yanliligi', 'coklu_test_asiri_uyum', 'mekanizma_ayirt_edebilir_mi', 'negatif_dislananlar', 'negatif_dislanmayanlar', 'sonuc', 'sinif', 'sinif_gerekcesi', 'kusurlar', 'onkayit_dosya', 'kod_dosya', 'kosu_kimligi', 'kaynak_atiflari'],
}
const AUDIT_SCHEMA = {
  type: 'object',
  properties: {
    birim: { type: 'string' },
    kapsam_ozeti: { type: 'string' },
    testler: { type: 'array', items: TEST_ITEM },
    birim_geneli_kusurlar: { type: 'array', items: { type: 'string' } },
    okunamayan_kaynaklar: { type: 'array', items: { type: 'string' } },
  },
  required: ['birim', 'kapsam_ozeti', 'testler', 'birim_geneli_kusurlar', 'okunamayan_kaynaklar'],
}
const V1_SCHEMA = {
  type: 'object',
  properties: {
    kontrol: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          test_id: { type: 'string' },
          durum: { type: 'string', enum: ['DOĞRU', 'DÜZELTME GEREKLİ', 'KANITLANAMADI'] },
          duzeltmeler: { type: 'array', items: { type: 'object', properties: { alan: { type: 'string' }, dogru_deger: { type: 'string' }, kanit: { type: 'string' } }, required: ['alan', 'dogru_deger', 'kanit'] } },
          not: { type: 'string' },
        },
        required: ['test_id', 'durum', 'duzeltmeler'],
      },
    },
    genel_not: { type: 'string' },
  },
  required: ['kontrol', 'genel_not'],
}
const V2_SCHEMA = {
  type: 'object',
  properties: {
    sinif_itirazlari: { type: 'array', items: { type: 'object', properties: { test_id: { type: 'string' }, onerilen_sinif: { type: 'string', enum: ['A', 'B', 'C', 'D'] }, gerekce: { type: 'string' }, kanit: { type: 'string' } }, required: ['test_id', 'onerilen_sinif', 'gerekce', 'kanit'] } },
    mantik_hatalari: { type: 'array', items: { type: 'object', properties: { test_id: { type: 'string' }, alan: { type: 'string' }, sorun: { type: 'string' }, onerilen_metin: { type: 'string' } }, required: ['test_id', 'alan', 'sorun'] } },
    gozden_kacan_kusurlar: { type: 'array', items: { type: 'object', properties: { test_id: { type: 'string' }, kusur: { type: 'string' }, kanit: { type: 'string' } }, required: ['test_id', 'kusur', 'kanit'] } },
    eksik_testler: { type: 'array', items: { type: 'object', properties: { ad: { type: 'string' }, kaynak: { type: 'string' }, aciklama: { type: 'string' } }, required: ['ad', 'kaynak', 'aciklama'] } },
    genel_not: { type: 'string' },
  },
  required: ['sinif_itirazlari', 'mantik_hatalari', 'gozden_kacan_kusurlar', 'eksik_testler', 'genel_not'],
}
const HAKEM_SCHEMA = {
  type: 'object',
  properties: { test_id: { type: 'string' }, nihai_sinif: { type: 'string', enum: ['A', 'B', 'C', 'D'] }, gerekce: { type: 'string' }, kanit: { type: 'string' } },
  required: ['test_id', 'nihai_sinif', 'gerekce', 'kanit'],
}

const BIRIMLER = [
  { id: 'K51A', ad: 'K51 v1.0 / v1.1: ABD Çöl Yolu akademik araştırma (P1 sıkışma, P2 kırılım, üçlü bariyer, meta-etiketleme, LR→GBM→CNN→LSTM merdiveni, 8 özellik grubu, PBO / DSR, kontroller, portföy, Avrupa ve BIST çoğaltma) + K51-D1 kırılım devamlılığı + hacimli taban tekrarı',
    ipucu: `Kod: ${REPO}/COL_YOLU_ABD.py (cy_* fonksiyonları; ön kayıt v1.0 / v1.1 dosya başında), test: test_col_yolu_abd.py. Çıktı: ${REPO}/arastirma_cikti/col_yolu_abd/ (cy_rapor.md, K51_OZET.md, K51_D1_onkayit.md, cy_hipotez.csv, cy_b_*.csv, cy_olay_*.csv.gz, cy_evren.csv). IZ_DEFTERI.md Ç132 ve Ç133 (grep -n "Ç132\\|Ç133").` },
  { id: 'K51B', ad: 'K51 sonrası bağımsız denetim v1.2: veri bütünlüğü (sayı uzlaşması, point-in-time evren, çıkış sınıflaması, delist / ham fiyat / kod yeniden kullanımı duyarlılığı, eski-yeni kod), kırılganlık (kaynak, hisse katkısı, yıl, rejim, kümeleme) ve beş hipotez H-A..H-E (Holm)',
    ipucu: `Kod: ${REPO}/COL_YOLU_ABD.py (cy_v12_calistir ve çağırdıkları). Ön kayıt: ${REPO}/arastirma_cikti/col_yolu_abd/K51_v12_onkayit.md. Çıktı: K51_VERI_DENETIMI.md, K51_KIRILGANLIK.md, K51_TEKRAR_URETIM.md, K51_HIPOTEZ_KARARLARI.csv, K51_ESLESMIS_KONTROL.csv.gz, K51_EVREN_PIT.csv (hepsi arastirma_cikti/col_yolu_abd/). IZ_DEFTERI.md Ç134.` },
  { id: 'K52', ad: 'K52: grafik izi + analist revizyonları (Yahoo analist not günlüğü; dört grup G1 / G2a / G2b / G3-G4; H0-H6, Holm, kırılganlık)',
    ipucu: `Kod: ${REPO}/COL_YOLU_ABD.py (cy_v13_calistir ve çağırdıkları). Ön kayıt: ${REPO}/arastirma_cikti/col_yolu_abd/K52_onkayit.md. Çıktı: K51_GRAFIK_ANALIST_ARASTIRMA.md, K51_ANALIST_TARIHSEL_VERI_DENETIMI.md, K51_ANALIST_VERI_KAPSAMI.csv, K51_ANALIST_EK_KATKI_TESTI.csv, K51_GRAFIK_ANALIST_4GRUP.csv (dosya adlarında K51 öneki var ama K52 işidir). IZ_DEFTERI.md Ç135.` },
  { id: 'K53', ad: 'K53: bilgi direnci (BDS 0-3), analist dağınıklığı (ADE), karar gecikmesi (KGS), G1-G5, T1-T8, Holm',
    ipucu: `Kod: ${REPO}/COL_YOLU_ABD.py (cy_v14_calistir ve çağırdıkları). Ön kayıt: ${REPO}/arastirma_cikti/col_yolu_abd/K53_onkayit.md. Çıktı: K53_RAPOR.md, K53_VERI_DENETIMI.md, K53_HIPOTEZ_TESTI.csv, K53_GRUPLAR.csv, K53_DENGE.csv, K53_OLAYLAR.csv.gz. IZ_DEFTERI.md Ç136 (+ K53 EK denetim notları).` },
  { id: 'K54', ad: 'K54: tarihsel hisse evreni sağlamlık denetimi (SEC başvuru geçmişi + Tiingo sembol listesi ile 6 sınıf; düzeltilmiş evrende K51 / K52 / K53 eski-yeni karşılaştırması)',
    ipucu: `Kod: ${REPO}/COL_YOLU_ABD.py (cy_v15_calistir ve çağırdıkları). Ön kayıt: ${REPO}/arastirma_cikti/col_yolu_abd/K54_onkayit.md. Çıktı: K54_RAPOR.md, K54_SIRKET_DURUMU.csv, K54_EVREN_ESLESTIRME.csv, K54_ESKI_YENI_TEST_KARSILASTIRMA.csv, K54_DELIST_DUYARLILIK.csv. IZ_DEFTERI.md Ç137.` },
  { id: 'K55', ad: 'K55: dallanmalı iz arama (OHLCV; D01 fiyat, D02 hacim, D03 oynaklık, D04 zaman / süre, D05 mikro yapı vekilleri, D06 göreli güç, D10 bileşik; Faz 0 tam evren + sızıntı testleri, Faz 1 63 hücre / 1.318 varyant satırı yalnız KEŞİF 2016-21, vekil kıyası; A olay öncesi, B eşleşmiş ileri, C CUSUM; Holm + BH)',
    ipucu: `Kod: ${REPO}/K55/*.py, ${REPO}/K55.py, test: test_k55.py. Ön kayıt: ${REPO}/K55/ONKAYIT_K55.md (v1.0-v1.4), plan: arastirma_cikti/k55_dallanma/K55_PLAN.md. Çıktı: arastirma_cikti/k55_dallanma/ (tam_evren/ alt klasörü asıl koşu; K55_FAZ0_RAPOR.md, K55_FAZ1_RAPOR.md [çok büyük, bölüm bölüm oku], K55_VEKIL.md, K55_SIZINTI_TESTI.md, K55_VERI_KAPSAMI.md). IZ_DEFTERI.md Ç138. Birim = dal düzeyinde testler (D01..D06, D10 ayrı satır; hücre kimlikleri not alanına) + Faz 0 sızıntı / veri kalitesi + vekil kıyası. D07 temel, D08 sahiplik, D09 makro dalları bu çalışmada koşulmadıysa test satırı AÇMA; onları birim_geneli_kusurlar altında "koşulmadı" diye an.` },
  { id: 'K56A', ad: 'K56 Faz 0: K51-K55 etki envanteri (265 bulgu), mekanizma hipotezleri M01-M19, hipotez başına gerekli veri, 28 veri kaynağı ve küçük örneklem erişim testi (12 sembol), M01 seçim etkisi sentetik sıfır sınaması, bağımsız gözden geçirme bulguları',
    ipucu: `Kod: ${REPO}/K56/ (ortak.py, etki_envanteri.py, mekanizma.py, kurumsal_sahiplik.py, iceriden_islemler.py, finansal_mekanizma.py, kurumsal_olaylar.py, islem_davranisi.py, karsit_ornekler.py, mekanizma_raporu.py), test_k56.py. Ön kayıt: ${REPO}/K56/ONKAYIT_K56.md (v1.0, v1.0-a, v1.1). Çıktı: ${REPO}/arastirma_cikti/k56_mekanizma/K56_FAZ0_RAPOR.md (170 KB; bölüm bölüm oku), K56_VERI_KAYNAKLARI.csv, K56_VERI_ERISIM_TESTI.csv, K56_SECIM_SENTETIK*.csv, K56_RISKLER.csv, K56_TALIMAT_SUZGECI.csv, K56_UYGULAMA_SIRASI.csv, K56_KOSU_*.json. IZ_DEFTERI.md Ç139. Birim = Faz 0'ın kendi testleri (erişim testi, sentetik sıfır sınaması, envanter yöntemi / mekanizma testleri tasarımı); M01-M19 hipotezlerinin her biri için ayrı test satırı AÇMA (onlar hipotezdir; bunları kapsam_ozeti ve birim_geneli_kusurlar'da özetle; hangi M hipotezinin Faz 0'da gerçekten test edildiğini açıkça ayır).` },
  { id: 'K56B', ad: 'K56 Faz 1: K56-F1A (seçimsiz kontrol A1, kalan etki A2, haber / birleşme bileşimi A3, kalibre sentetik), K56-IC (İÇ doğrulama 2022-23: B1 K55 A, B2 seçimsiz kontrol, B3 K55 B eşleşmiş ileri, B4), K56-BAG (BAĞIMSIZ 2024-26 tek açılış K55_125_B + BAGIMSIZ_B duyarlılık + K55 nihai karar eşlemesi)',
    ipucu: `Kod: ${REPO}/K56/faz1_yerel.py, K56/surucu.py (faz1a_kos, ic_kos, bagimsiz_kos, k55_nihai_karar), K56/mekanizma.py, K56/ortak.py (dönem kapısı, kilit, açılış kaydı). Ön kayıt: ${REPO}/K56/ONKAYIT_K56.md v1.2 (A, B), v1.2-a, v1.2-b, v1.3 (D, H), v1.3-a..d, ${REPO}/K56/ONKAYIT_K56_SATIRLAR.csv. Çıktı: ${REPO}/arastirma_cikti/k56_mekanizma/faz1_yerel/, ic_dogrulama/, bagimsiz/ (RAPOR_ASIL.md, RAPOR_DUYARLILIK_B.md, K56BAG_*.csv), K56_NIHAI_RAPOR.md, K56_BAGIMSIZ_KILIT.json, K56_BAGIMSIZ_ACILIS.csv. IZ_DEFTERI.md Ç140, Ç141, Ç146. Geçersiz sayılan ilk koşuların NOT.md dosyalarını da oku.` },
  { id: 'K56C', ad: 'K56 yan denetimleri: K56-AYR ((iii) rastgele gün / bütün günler ayrışması, olay düzeyi kümeler, konum bantları, yapay veri), K56-PBO (PBO / Deflated Sharpe), K56-SIZ (İÇ → BAĞIMSIZ dolaylı erişim sınaması T0 / T1 / T2), K56-EVREN2 (batan şirketlerle evren v2; aday ve hazırlık aşaması, indirme sürüyor)',
    ipucu: `Kod: ${REPO}/K56/ayrisma.py, pbo_dsr.py, sizinti_denetimi.py, batan_evren.py, evren_v2.py, surucu.py (ayrisma_kos, pbo_kos, sizinti_kos, evren2_*). Ön kayıt: ${REPO}/K56/ONKAYIT_K56.md v1.3 (E, F, G, I), v1.3-a..d. Çıktı: ${REPO}/arastirma_cikti/k56_mekanizma/ayrisma/, pbo_dsr/, sizinti/ (geçersiz koşuların NOT.md dosyaları dahil), evren_v2/. IZ_DEFTERI.md Ç142-Ç145. EVREN2'nin fiyat indirmesi hâlâ sürüyor: sonucu olmayan kısım için sinif D ya da B yazma; "sonuç yok, aday / hazırlık aşaması" diye açıkça belirt ve en uygun sınıfı gerekçelendir.` },
]

phase('Denetim')
const sonuc = await pipeline(
  BIRIMLER,
  b => agent(`Sen K57 denetiminin "${b.id}" birimi için bağımsız araştırma denetçisisin. Birim: ${b.ad}

GÖREV: Bu birimdeki her testi (karar üreten, önceden tanımlı ölçüt / hipotez / denetim birimi) kaynaklarından okuyarak tek tek denetle ve şemaya göre satır üret. Test = (hipotez ya da denetim sorusu, ölçüm, karar kuralı) üçlüsü; aynı ölçümün yıl / varyant tekrarlarını tek satırda topla, kimliklerini not alanında say. Birimde kayıtlı karar üreten HER testi bul (tipik 5-14 satır); ön kayıtta tanımlı ama koşulmayan ya da veri yetersizliğiyle kalan testleri de yaz (sinif D).

${ALAN13}

SINIFLAR:
${SINIFLAR}

ALANLAR (alanlar dizisi için kodlar): ${ALANLAR}

${KURALLAR}

KAYNAK İPUÇLARI (bu birim): ${b.ipucu}

Ek denetim ölçütleri (kendi okumanla doğrula; varsayma): hayatta kalma yanlılığı ve batan / delist ele alınışı; "bağımsız" denen dönemlerin gerçekten bağımsız olup olmadığı (aynı dönem önceki çalışmalarda test dönemi olarak kullanıldıysa); olay tanımının seçim etkisi (ilk geçiş vs bütün günler); gözlem birimi ile kümeleme düzeyi uyumu; eşleştirme değişkenlerinin ölçülen mekanizmayı sızdırıp sızdırmadığı; ölçülen veri (ör. fiyat, analist notu, SEC başvurusu) ile iddia edilen mekanizma (ör. gerçek sahiplik değişimi, birikim) arasındaki boşluk; çoklu test / ızgara sayısı ve ön kayıt disiplini; negatif sonucun gücü (örneklem / etki büyüklüğü / aralık).

Çıktı: AUDIT_SCHEMA'ya uygun yapılandırılmış sonuç. test_id'leri "${b.id}-T01", "${b.id}-T02"... diye ver.`, { label: `denetim:${b.id}`, phase: 'Denetim', schema: AUDIT_SCHEMA }),

  async (denetim, b) => {
    if (!denetim || !denetim.testler) { log(`${b.id}: denetim sonucu yok`); return { birim: b.id, denetim: null } }
    log(`${b.id}: ${denetim.testler.length} test satırı; doğrulama başlıyor`)
    const json = JSON.stringify(denetim)
    const [v1, v2] = await parallel([
      () => agent(`Sen K57 denetiminde "${b.id}" birimi için BAĞIMSIZ KAYNAK DOĞRULAYICISISIN (V1). Aşağıdaki denetim JSON'unu bir başka denetçi üretti. İşin: her test satırındaki olgusal iddiaları (veri kaynağı / kapsam, örneklem, batan-delist ele alışı, olay tanımı, gözlem birimi, bağımlılık, eşleştirme, sızıntı kontrolü, çoklu test, sonuç ve sayılar, ön kayıt / kod / koşu kimliği) KAYNAK DOSYALARA dönüp doğrula. Her test_id için bir kontrol satırı döndür (hepsini kapsa). Yanlış, eksik ya da kanıtsız bulduğun alan için alan adı + doğru değer + kanıt (dosya:bölüm / satır) ver. Yalnız doğrulanabilen düzeltmeleri yaz; emin değilsen durum KANITLANAMADI. Sınıf (A-D) tartışması senin işin değil.

${KURALLAR}

KAYNAK İPUÇLARI: ${b.ipucu}

DENETİM JSON:
${json}`, { label: `v1:${b.id}`, phase: 'Dogrulama', schema: V1_SCHEMA }),
      () => agent(`Sen K57 denetiminde "${b.id}" birimi için BAĞIMSIZ ELEŞTİREL OKUYUCUSUN (V2). Aşağıdaki denetim JSON'unu bir başka denetçi üretti. Görevin onu çürütmeye çalışmak: (a) sınıf (A/B/C/D) kararları gerekçeyle tutuyor mu? Özellikle fazla iyimser A / B ve fazla sert C sınıflarını sorgula; (b) "mekanizma_ayirt_edebilir_mi" ve negatif sonucun dışladığı / dışlamadığı alternatifler mantıken doğru mu; (c) gözden kaçan yöntemsel kusurlar (sızıntı, seçim etkisi, hayatta kalma, bağımlılık, çoklu test, bağımsız olmayan dönem, ölçüm-mekanizma boşluğu); (d) birimde kaynaklarda tanımlı olup envanterde HİÇ geçmeyen testler var mı (eksik_testler). Her itiraz kaynak kanıtıyla olsun; kanıtsız itiraz yazma. Yöntemsel kusur bulmak hipotezi doğru yapmaz: bunu itirazlarında karıştırma.

SINIFLAR:
${SINIFLAR}

${KURALLAR}

KAYNAK İPUÇLARI: ${b.ipucu}

DENETİM JSON:
${json}`, { label: `v2:${b.id}`, phase: 'Dogrulama', schema: V2_SCHEMA }),
    ])

    phase('Tamamlama')
    let ek = null
    if (v2 && v2.eksik_testler && v2.eksik_testler.length) {
      ek = await agent(`Sen K57 denetiminde "${b.id}" birimi için TAMAMLAMA denetçisisin. Eleştirel okuyucu, envanterde bulunmayan şu testleri işaret etti. Her biri için kaynakları okuyarak AUDIT_SCHEMA'daki test satırlarını üret (test_id'leri "${b.id}-T51", "T52"... diye ver). Kaynakta gerçekten karar üretmeyen / var olmayan bir iddia ise o maddeyi atla ve nedenini birim_geneli_kusurlar alanına yaz.

EKSİK TESTLER:
${JSON.stringify(v2.eksik_testler)}

ALAN13:
${ALAN13}

SINIFLAR:
${SINIFLAR}

ALANLAR: ${ALANLAR}

${KURALLAR}

KAYNAK İPUÇLARI: ${b.ipucu}

MEVCUT ENVANTER ÖZETİ (tekrar üretme): ${JSON.stringify(denetim.testler.map(t => t.test_id + ' ' + t.ad))}`, { label: `tamamla:${b.id}`, phase: 'Tamamlama', schema: AUDIT_SCHEMA })
    }

    phase('Hakem')
    const itirazlar = (v2 && v2.sinif_itirazlari ? v2.sinif_itirazlari : []).filter(i => { const t = denetim.testler.find(x => x.test_id === i.test_id); return t && t.sinif !== i.onerilen_sinif })
    const hakem = itirazlar.length ? await parallel(itirazlar.map(i => () => {
      const t = denetim.testler.find(x => x.test_id === i.test_id)
      return agent(`Sen K57 denetiminde HAKEMSİN. Bir testin sınıfı için iki görüş var; kaynakları kendin okuyup nihai sınıfı seç. Denetçinin sınıfı: ${t.sinif} (gerekçe: ${t.sinif_gerekcesi}). Eleştirel okuyucunun önerisi: ${i.onerilen_sinif} (gerekçe: ${i.gerekce}; kanıt: ${i.kanit}). Test satırı: ${JSON.stringify(t)}

SINIFLAR:
${SINIFLAR}

${KURALLAR}

KAYNAK İPUÇLARI: ${b.ipucu}

Kural: kaynakta doğrulayabildiğin kanıta göre karar ver; iki tarafın da kanıtını kontrol et; emin değilsen daha temkinli (daha sınırlı) sınıfı seç ve nedenini yaz.`, { label: `hakem:${i.test_id}`, phase: 'Hakem', schema: HAKEM_SCHEMA })
    })) : []
    return { birim: b.id, denetim, v1, v2, ek, hakem: hakem.filter(Boolean) }
  },
)

const ozet = sonuc.filter(Boolean).map(r => {
  const d = r.denetim
  const say = {}
  if (d) for (const t of d.testler) say[t.sinif] = (say[t.sinif] || 0) + 1
  return {
    birim: r.birim,
    test_sayisi: d ? d.testler.length : 0,
    siniflar: say,
    v1_duzeltme_gereken: r.v1 ? r.v1.kontrol.filter(k => k.durum !== 'DOĞRU').length : null,
    v2_itiraz: r.v2 ? r.v2.sinif_itirazlari.length : null,
    v2_mantik: r.v2 ? r.v2.mantik_hatalari.length : null,
    v2_gozden_kacan: r.v2 ? r.v2.gozden_kacan_kusurlar.length : null,
    v2_eksik: r.v2 ? r.v2.eksik_testler.length : null,
    tamamlama_satiri: r.ek ? r.ek.testler.length : 0,
    hakem: r.hakem ? r.hakem.map(h => h.test_id + '→' + h.nihai_sinif) : [],
  }
})
log('birim özetleri: ' + JSON.stringify(ozet))
return { ozet, birim_sayisi: BIRIMLER.length, tamamlanan: sonuc.filter(Boolean).length }
