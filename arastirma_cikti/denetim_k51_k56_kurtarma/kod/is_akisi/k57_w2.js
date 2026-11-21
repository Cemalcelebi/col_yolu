export const meta = {
  name: 'k57-harita-mekanizma-hipotez',
  description: 'TEST_ENVANTERI üzerinden: 10 alan haritası, mekanizma soruları 4.1-4.6, önceki hipotez envanteri, açık sorular (bağımsız eleştirmenle)',
  phases: [
    { title: 'Mekanizma', detail: '6 ajan: 4.1-4.6 alt soruları, geçmiş testler ve yeterlilik' },
    { title: 'Alan', detail: '10 ajan: alan başına tamamlanan / eksik / hiç yapılmayan' },
    { title: 'Hipotez', detail: '2 ajan: K51-K56 önceki hipotezleri için durum satırları' },
    { title: 'Sentez', detail: 'açık sorular listesi + tamlık eleştirmeni' },
  ],
}
const REPO = '/home/user/col_yolu'
const K57 = `${REPO}/arastirma_cikti/k57_denetim`
const ALANLAR = [
  ['A1', 'Fiyat davranışı'], ['A2', 'Hacim ve işlem akışı'], ['A3', 'Volatilite ve risk rejimi'], ['A4', 'Zaman ve süre davranışı'], ['A5', 'Piyasa mikro yapısı'],
  ['A6', 'Göreceli güç ve piyasa konumu'], ['A7', 'Şirket temelleri'], ['A8', 'Sahiplik, sermaye ve kurumsal olaylar'], ['A9', 'Sektör, makroekonomi ve dış etkenler'], ['A10', 'Birleşik davranışlar ve alanlar arası ilişkiler'],
]
const SINIFLAR = `Test sınıfları (TEST_ENVANTERI.csv 'sinif'): A = geçerli ve yeterli; B = geçerli fakat sınırlı; C = yöntemsel olarak sorunlu; D = veri yetersizliği nedeniyle cevaplanamayan. E = hiç test edilmemiş soru (soru düzeyinde; test satırı yok).`
const ILKE = `İLKELER: Bir sorunun daha önce test edilmiş olması doğru test edildiği anlamına gelmez; yöntemsel kusur bulunması hipotezi otomatik doğru yapmaz. Negatif sonuç yalnız gerçekten dışladığı alternatifleri dışlar. Eksik veriyi sıfır ya da olumsuz kanıt sayma. 13F / Form 4 kayıtlarını gerçek zamanlı işlem akışı gibi yorumlama; sahiplik verisi ile günlük işlem davranışını karıştırma; korelasyonu mekanizma / nedensellik diye sunma; vekil (proxy) ölçümü gerçek veri gibi sunma.`
const KURALLAR = `ÇALIŞMA KURALLARI (kesin): Depo ${REPO}; YALNIZ OKU (dosya yazma, düzenleme, ağ isteği, boru hattı koşturma yok; git yalnız status/log/show/diff). Hiçbir bilgi uydurma; kaynak yoksa "KAYITLI DEĞİL". Test kimliklerini yalnız TEST_ENVANTERI.csv'de gerçekten var olanlardan ver (kimlik biçimi örn. K51B-T07); veri kaynağı kimliklerini yalnız VERI_KAYNAKLARI.csv'de var olanlardan ver. Türkçe, kısa ve somut (metin alanı ~400 karakter).
Girdiler (K57 klasörü ${K57}): TEST_ENVANTERI.csv (denetlenmiş test satırları; sütunlar: id, calisma_birimi, ad, soru, alanlar, sinif, sonuc, kusurlar, negatif_dislananlar, negatif_dislanmayanlar, mekanizma_ayirt_edebilir_mi ...; pandas ile oku, ilgili satırları süz), VERI_KAYNAKLARI.csv (74 kaynak: kapsam, point_in_time, erisim_testi), VERI_BOSLUKLARI.json, KAYNAK_MANIFEST.csv. Ek: ${REPO}/arastirma_cikti/k56_mekanizma/K56_HIPOTEZLER.csv (M01-M19), K56_HIPOTEZ_VERI.csv, K56_ACIKLANMAMIS_BULGULAR.csv, K56_ETKI_ENVANTERI.csv, K56_FAZ0_RAPOR.md; ${REPO}/IZ_DEFTERI.md; ${REPO}/CLAUDE.md; ${REPO}/COL_OZET.md. Kapsam: K51-K56 (ABD); K51 öncesi BIST çalışmaları (K1-K50, FON_IZI.py) yalnız ad olarak 'kapsam dışı ilgili çalışma' diye an.`

const SORU_SCHEMA = {
  type: 'object',
  properties: {
    sorular: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          soru_id: { type: 'string', description: 'örn. 4.1-a' },
          soru_metni: { type: 'string' },
          ilgili_testler: { type: 'array', items: { type: 'string' } },
          ilgili_k56_hipotezleri: { type: 'array', items: { type: 'string' }, description: 'M01..M19 (K56_HIPOTEZLER.csv)' },
          kapsam_durumu: { type: 'string', enum: ['A', 'B', 'C', 'D', 'E'], description: 'soru düzeyinde: A geçerli ve yeterli test var; B geçerli fakat sınırlı; C yalnız yöntemsel olarak sorunlu test var; D veri yetersizliğiyle cevaplanamadı; E hiç test edilmemiş' },
          neyi_cevapladi: { type: 'string' },
          neyi_cevaplayamadi: { type: 'string' },
          negatif_sonuc_dislananlar: { type: 'string' },
          negatif_sonuc_dislanmayanlar: { type: 'string' },
          gerekli_dogrudan_veri: { type: 'string' },
          veri_durumu: { type: 'string', enum: ['VAR', 'KISMEN', 'YOK', 'YALNIZ VEKİL'] },
          veri_kaynak_idleri: { type: 'array', items: { type: 'string' } },
          kapsam_disi_onceki_calismalar: { type: 'array', items: { type: 'string' } },
          acik_sorular: { type: 'array', items: { type: 'string' } },
          kaynak_atiflari: { type: 'array', items: { type: 'string' } },
        },
        required: ['soru_id', 'soru_metni', 'ilgili_testler', 'ilgili_k56_hipotezleri', 'kapsam_durumu', 'neyi_cevapladi', 'neyi_cevaplayamadi', 'negatif_sonuc_dislananlar', 'negatif_sonuc_dislanmayanlar', 'gerekli_dogrudan_veri', 'veri_durumu', 'veri_kaynak_idleri', 'kapsam_disi_onceki_calismalar', 'acik_sorular', 'kaynak_atiflari'],
      },
    },
    genel_not: { type: 'string' },
  },
  required: ['sorular', 'genel_not'],
}
const MEK = [
  ['4.1 Dağıtım ve emilim', ['4.1-a Büyük satışlar gerçekten pozisyon azaltımı mı?', '4.1-b Satışları başka yatırımcılar mı karşılıyor?', '4.1-c Satış miktarı ile fiyat etkisi arasında nasıl bir ilişki var?', '4.1-d Fiyat düşmeden yüksek satış hacmi gerçekleşebiliyor mu?', '4.1-e Görünür dağıtım ile gerçek sahiplik değişimi birbirinden ayrılabiliyor mu?']],
  ['4.2 Görünür zayıflık ve birikim', ['4.2-a Zayıf fiyat davranışı hangi koşullarda alıcı emilimiyle birlikte görülüyor?', '4.2-b Fiyatın düşmemesi, satışların karşılandığını kanıtlıyor mu?', '4.2-c Fiyatın yükselmesi, gerçek birikim anlamına mı geliyor?', '4.2-d Aynı görüntüyü düşük likidite veya işlem seyrekliği üretebilir mi?']],
  ['4.3 Likidite ve sermaye', ['4.3-a Likidite azalması fiyat hareketini nasıl değiştiriyor?', '4.3-b Yeni hisse ihracı, ATM programı, dönüştürülebilir borç ve warrant kaynaklı sulanma nasıl etkiliyor?', '4.3-c Hisse sayısındaki değişim düzeltilmiş fiyat verisinde nasıl temsil ediliyor?', '4.3-d Şirketin nakit ihtiyacı ve finansman riski fiyat davranışını nasıl etkiliyor?']],
  ['4.4 Şirketin temel bozulması', ['4.4-a Gelir, nakit akışı, borç, marj ve faaliyet kalitesi bozulması fiyat hareketinden önce görülebiliyor mu?', '4.4-b Analist tahmin değişiklikleri ile gerçekleşen finansal veriler ayrıştırılabiliyor mu?', '4.4-c Şirketin kötüleşmesi ile piyasa tarafından geç fark edilmesi birbirinden ayrılabiliyor mu?']],
  ['4.5 Büyük yatırımcı davranışı', ['4.5-a 13F, Form 4, kurumsal sahiplik ve diğer kayıtlar hangi soruları cevaplayabilir?', '4.5-b Bildirim gecikmesi ve raporlama eşiği nedeniyle hangi davranışlar görünmez?', '4.5-c Sahiplik verisi ile günlük işlem davranışı birbirine karıştırılmamalı (ayrımın kaynaklar düzeyinde nasıl yapıldığı)', '4.5-d Bir yatırımcının sahipliğinin değişmesi tek başına fiyat hareketinin sebebi kabul edilmemeli (testlerde nasıl ele alındı)']],
  ['4.6 Bağımsız kanıt', ['4.6-a Fiyat verisinde bulunan bir davranış, şirket finansallarında da iz bırakıyor mu?', '4.6-b Sahiplik kayıtları aynı davranışı destekliyor mu?', '4.6-c Kurumsal olay kayıtları alternatif açıklama sunuyor mu?', '4.6-d İşlem bazlı veri aynı sonucu doğruluyor mu?', '4.6-e Bağımsız veri kaynakları aynı olayı farklı ölçüm hatalarıyla mı açıklıyor?']],
]
const ALAN_SCHEMA = {
  type: 'object',
  properties: {
    alan: { type: 'string' },
    tamamlanan: { type: 'array', items: { type: 'object', properties: { test_id: { type: 'string' }, ne_yapildi: { type: 'string' }, sinif: { type: 'string' }, ne_kadar_guvenilir: { type: 'string' } }, required: ['test_id', 'ne_yapildi', 'sinif', 'ne_kadar_guvenilir'] } },
    eksik_kalan: { type: 'array', items: { type: 'object', properties: { konu: { type: 'string' }, neden_eksik: { type: 'string' }, ilgili_testler: { type: 'array', items: { type: 'string' } }, gerekli_veri: { type: 'string' } }, required: ['konu', 'neden_eksik', 'ilgili_testler', 'gerekli_veri'] } },
    hic_yapilmayan: { type: 'array', items: { type: 'object', properties: { konu: { type: 'string' }, neden_onemli: { type: 'string' }, veri_durumu: { type: 'string' }, veri_kaynak_idleri: { type: 'array', items: { type: 'string' } } }, required: ['konu', 'neden_onemli', 'veri_durumu', 'veri_kaynak_idleri'] } },
    acik_sorular: { type: 'array', items: { type: 'string' } },
    alan_degerlendirmesi: { type: 'string', description: 'bu alanda bugüne kadar ne öğrenildi / öğrenilemedi (dürüst; sinyal iddiası yok)' },
    kaynak_atiflari: { type: 'array', items: { type: 'string' } },
  },
  required: ['alan', 'tamamlanan', 'eksik_kalan', 'hic_yapilmayan', 'acik_sorular', 'alan_degerlendirmesi', 'kaynak_atiflari'],
}
const HIP_SCHEMA = {
  type: 'object',
  properties: {
    hipotezler: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'önceki çalışmadaki kimlik: K51-H-A, K52-H0-P1, K53-T1, K55-D01, K56-M03 vb.' },
          ana_alan: { type: 'string', description: 'A1..A10' },
          hipotez: { type: 'string' },
          onceki_ilgili_calismalar: { type: 'array', items: { type: 'string' } },
          onceki_test_sonucu: { type: 'string' },
          test_gecerliligi: { type: 'string', description: 'A / B / C / D / E + kısa gerekçe (TEST_ENVANTERI sınıflarına dayan)' },
          ilgili_test_idleri: { type: 'array', items: { type: 'string' } },
          eksik_veri: { type: 'string' },
          acik_kalan_soru: { type: 'string' },
          sonraki_islem: { type: 'string' },
          durum: { type: 'string', enum: ['BEKLEMEDE', 'DENETLENİYOR', 'VERİ BEKLİYOR', 'TESTE HAZIR', 'DEVAM EDİYOR', 'TAMAMLANDI', 'REDDEDİLDİ', 'YÖNTEMSEL OLARAK GEÇERSİZ'] },
          durum_gerekcesi: { type: 'string' },
          kaynak_atiflari: { type: 'array', items: { type: 'string' } },
        },
        required: ['id', 'ana_alan', 'hipotez', 'onceki_ilgili_calismalar', 'onceki_test_sonucu', 'test_gecerliligi', 'ilgili_test_idleri', 'eksik_veri', 'acik_kalan_soru', 'sonraki_islem', 'durum', 'durum_gerekcesi', 'kaynak_atiflari'],
      },
    },
    genel_not: { type: 'string' },
  },
  required: ['hipotezler', 'genel_not'],
}
const ACIK_SCHEMA = {
  type: 'object',
  properties: {
    sorular: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'AS-001...' },
          soru: { type: 'string' },
          neden_acik: { type: 'string', description: 'ÖNCEKİ TESTLER NEDEN CEVAPLAYAMADI: yöntemsel kusur / veri yok / hiç test edilmedi / ölçüm mekanizmayı ayırt etmiyor / güç yetersiz' },
          kategori: { type: 'string', enum: ['E hiç test edilmedi', 'D veri yok', 'C yöntemsel kusur', 'B sınırlı kapsam', 'ölçüm ayırt edemiyor', 'alternatif açıklama dışlanamadı', 'bağımsız doğrulama yok'] },
          alanlar: { type: 'array', items: { type: 'string' } },
          mekanizma_sorulari: { type: 'array', items: { type: 'string' }, description: '4.1-a gibi' },
          ilgili_testler: { type: 'array', items: { type: 'string' } },
          gerekli_veri: { type: 'string' },
          veri_durumu: { type: 'string' },
          onem: { type: 'string', enum: ['YÜKSEK', 'ORTA', 'DÜŞÜK'] },
          onem_gerekcesi: { type: 'string' },
        },
        required: ['id', 'soru', 'neden_acik', 'kategori', 'alanlar', 'mekanizma_sorulari', 'ilgili_testler', 'gerekli_veri', 'veri_durumu', 'onem', 'onem_gerekcesi'],
      },
    },
    birlestirme_notu: { type: 'string' },
  },
  required: ['sorular', 'birlestirme_notu'],
}
const TAMLIK_SCHEMA = {
  type: 'object',
  properties: {
    eksik_sorular: { type: 'array', items: { type: 'object', properties: { soru: { type: 'string' }, neden_onemli: { type: 'string' }, kaynak: { type: 'string' } }, required: ['soru', 'neden_onemli', 'kaynak'] } },
    hatali_satirlar: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, sorun: { type: 'string' } }, required: ['id', 'sorun'] } },
    genel_not: { type: 'string' },
  },
  required: ['eksik_sorular', 'hatali_satirlar', 'genel_not'],
}

phase('Mekanizma')
const mek = await parallel(MEK.map(([baslik, alt]) => () => agent(`K57 denetiminde MEKANİZMA SORULARI (${baslik}). Aşağıdaki her alt soru için, K51-K56 çalışmalarında gerçekten yapılmış testleri TEST_ENVANTERI.csv'den (ve gerekirse kaynak dosyalardan) bularak değerlendir: hangi test(ler) bu soruya dokunuyor, ne cevaplıyor, ne cevaplayamıyor, negatif sonuç neyi dışlıyor / dışlamıyor, gerekli doğrudan veri var mı (VERI_KAYNAKLARI.csv, erişim testi durumu), soru düzeyinde durum (A-E). Bir test soruyla yalnızca konu olarak komşuysa onu ilgili test sayma; ölçtüğü şeyin soruyu gerçekten ayırt edip etmediğini yaz. Hiç test yoksa durum E; test var ama veri yoksa D; test yöntemsel kusurluysa C.

${ILKE}
${SINIFLAR}

ALT SORULAR:
${alt.join('\n')}

${KURALLAR}`, { label: `mekanizma:${baslik.split(' ')[0]}`, phase: 'Mekanizma', schema: SORU_SCHEMA })))

phase('Alan')
const alan = await parallel(ALANLAR.map(([kod, ad]) => () => agent(`K57 denetiminde ALAN HARİTASI: ${kod} ${ad}. TEST_ENVANTERI.csv'de bu alanı (alanlar sütununda ${kod}, ana alan ya da ikincil) içeren testleri süz; K56_HIPOTEZLER.csv ve K55 dal yapısı (D01..D10) ile eşleştir. Üç liste çıkar: (1) TAMAMLANAN: bu alanda yapılmış testler, sınıfları, ne kadar güvenilir (güvenilirlik = sınıf + kusurlar); (2) EKSİK KALAN: kısmen yapılmış, veri / güç / yöntem eksikliğiyle kalmış konular; (3) HİÇ YAPILMAYAN: bu alan için mekanizma açısından önemli olup hiçbir testte ele alınmamış konular (ör. mikro yapı için gün içi veri, sahiplik için 13F vb.; veri durumunu VERI_KAYNAKLARI.csv'den ver). Ayrıca açık soruları ve alanın dürüst bir değerlendirmesini yaz (sinyal iddiası yok; "bu alanda ne öğrenildi / öğrenilemedi"). K55'in D07 temel, D08 sahiplik, D09 makro dallarının koşulmadığını unutma: bunlar "hiç yapılmayan" tarafında olabilir ama K56 Faz 0 / Faz 1 başka yollarla dokunmuş olabilir; TEST_ENVANTERI'ne bak.

${ILKE}
${SINIFLAR}

${KURALLAR}`, { label: `alan:${kod}`, phase: 'Alan', schema: ALAN_SCHEMA })))

phase('Hipotez')
const hip = await parallel([
  () => agent(`K57 denetiminde ÖNCEKİ HİPOTEZ ENVANTERİ (K51-K55). K51 (H1-H10 / B1-B9 / D1 ve model merdiveni karşılıkları), K51 v1.2 (H-A..H-E), K52 (H0-H6), K53 (G1-G5, T1-T8, BDS/ADE/KGS), K54 (sınıflama hipotezi / eski-yeni karşılaştırma) ve K55 (dal başına: D01 fiyat, D02 hacim, D03 oynaklık, D04 zaman, D05 mikro yapı vekilleri, D06 göreli güç, D10 bileşik; D07 / D08 / D09 koşulmadı: durumları BEKLEMEDE ya da VERİ BEKLİYOR) hipotezlerinin her biri için bir satır üret. Durum kuralı: geçerli (A/B) test koşulmuş ve karar çıkmışsa TAMAMLANDI (olumsuz karar REDDEDİLDİ yazılabilir ama yalnız ön kayıtlı ret kuralı işlediyse); yöntemsel kusurlu (C) testse YÖNTEMSEL OLARAK GEÇERSİZ; veri yetersizse VERİ BEKLİYOR; hiç koşulmadıysa BEKLEMEDE. 'ilgili_test_idleri' yalnız TEST_ENVANTERI.csv'deki gerçek kimlikler. Aynı hipotezi farklı adla ikinci kez yazma.

${ILKE}
${SINIFLAR}

${KURALLAR}`, { label: 'hipotez:K51-K55', phase: 'Hipotez', schema: HIP_SCHEMA }),
  () => agent(`K57 denetiminde ÖNCEKİ HİPOTEZ ENVANTERİ (K56). K56_HIPOTEZLER.csv'deki M01-M19 mekanizma hipotezlerinin her biri için bir satır üret, ayrıca K56 Faz 1 / BAĞIMSIZ / EVREN2'nin sorduğu ayrı hipotezleri (A1 seçimsiz kontrol, A2 kalan etki, A3 haber-birleşme bileşimi, B1-B4, AYR, PBO, SIZ, EVREN2 etkisi) satırlandır. Hangi M hipotezinin gerçekten test edildiğini (yalnız M01 seçim etkisi sentetik sıfır sınaması + Faz 1 türevleri gibi) TEST_ENVANTERI.csv'den doğrula; test edilmeyenler için durum BEKLEMEDE (E) ya da veri yoksa VERİ BEKLİYOR. EVREN2 hâlâ sürüyor: DEVAM EDİYOR. Aynı hipotezi farklı adla ikinci kez yazma.

${ILKE}
${SINIFLAR}

${KURALLAR}`, { label: 'hipotez:K56', phase: 'Hipotez', schema: HIP_SCHEMA }),
])

phase('Sentez')
const acik = await agent(`K57 denetiminde AÇIK SORULAR LİSTESİ (önceki testlerin cevaplayamadığı sorular). Aşağıdaki üç girdiyi (6 mekanizma ajanının soru tabloları, 10 alan ajanının açık soruları, K56_ACIKLANMAMIS_BULGULAR.csv + K56_FAZ0_RAPOR.md §2 ve §7) birleştir, tekrarları tek soruda topla, her soru için neden açık olduğunu (hangi test neden cevaplayamadı), kategoriyi, gerekli veriyi ve önemini yaz. Hiçbir önemi uydurma: önem = mekanizmayı ayırt etme değeri + cevabın başka soruları kapatma gücü; gerekçeyi yaz. Soruların yalnız soru olduğunu unutma: hipotez / sinyal ya da çözüm önerisi yazma.

${ILKE}
${SINIFLAR}

MEKANİZMA AJANLARI:
${JSON.stringify(mek.filter(Boolean).flatMap(m => m.sorular.map(s => ({ id: s.soru_id, durum: s.kapsam_durumu, cevaplayamadi: s.neyi_cevaplayamadi, acik: s.acik_sorular, testler: s.ilgili_testler, veri: s.veri_durumu }))))}

ALAN AJANLARI:
${JSON.stringify(alan.filter(Boolean).map(a => ({ alan: a.alan, acik: a.acik_sorular, hic_yapilmayan: a.hic_yapilmayan.map(h => h.konu + ' [' + h.veri_durumu + ']'), eksik: a.eksik_kalan.map(e => e.konu) })))}

${KURALLAR}`, { label: 'sentez:acik-sorular', phase: 'Sentez', schema: ACIK_SCHEMA })
const tam = await agent(`K57 denetiminde AÇIK SORULAR LİSTESİ için BAĞIMSIZ TAMLIK ELEŞTİRMENİSİN. Listede (a) kaynaklarda açıkça işaretlenmiş ama listeye girmemiş açık sorular (K56_ACIKLANMAMIS_BULGULAR.csv, K56_FAZ0_RAPOR.md §2 / §7, K56_RISKLER.csv, TEST_ENVANTERI.csv'deki 'mekanizma_ayirt_edebilir_mi = HAYIR / KISMEN' ve 'kusurlar' alanları, 4.1-4.6 soruları) ve (b) hatalı / kaynaksız satırlar var mı? Her bulguyu kaynakla kanıtla.

LİSTE:
${JSON.stringify(acik ? acik.sorular.map(s => ({ id: s.id, soru: s.soru, kategori: s.kategori, mekanizma: s.mekanizma_sorulari })) : [])}

${KURALLAR}`, { label: 'sentez:tamlik', phase: 'Sentez', schema: TAMLIK_SCHEMA })
log(`mekanizma ${mek.filter(Boolean).length}/6, alan ${alan.filter(Boolean).length}/10, hipotez ${hip.filter(Boolean).length}/2, açık soru ${acik ? acik.sorular.length : '?'}, tamlık eksik ${tam ? tam.eksik_sorular.length : '?'}`)
return { mekanizma: mek.filter(Boolean).length, alan: alan.filter(Boolean).length, hipotez: hip.filter(Boolean).length, acik_soru: acik ? acik.sorular.length : null, tamlik_eksik: tam ? tam.eksik_sorular.length : null }
