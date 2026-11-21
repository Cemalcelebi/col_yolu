export const meta = {
  name: 'k57-hipotez-onerileri',
  description: 'Yeni araştırma kartları: 10 alan için öneri, üç eleştirmen (yenilik / veri gerçekçiliği / yanlılık), üç hakemli sıralama',
  phases: [
    { title: 'Oneri', detail: '10 alan ajanı: 2-3 araştırma kartı' },
    { title: 'Elestiri', detail: '3 bağımsız eleştirmen: yenilik, veri, yanlılık' },
    { title: 'Siralama', detail: '3 jüri üyesi: puan + sıra' },
  ],
}
const REPO = '/home/user/col_yolu'
const K57 = `${REPO}/arastirma_cikti/k57_denetim`
const ALANLAR = [
  ['A1', 'Fiyat davranışı'], ['A2', 'Hacim ve işlem akışı'], ['A3', 'Volatilite ve risk rejimi'], ['A4', 'Zaman ve süre davranışı'], ['A5', 'Piyasa mikro yapısı'],
  ['A6', 'Göreceli güç ve piyasa konumu'], ['A7', 'Şirket temelleri'], ['A8', 'Sahiplik, sermaye ve kurumsal olaylar'], ['A9', 'Sektör, makroekonomi ve dış etkenler'], ['A10', 'Birleşik davranışlar ve alanlar arası ilişkiler'],
]
const ANA = `ANA AMAÇ (Cemal): Yeni bir teknik indikatör, Çöl Yolu varyasyonu ya da fiyat tahmin modeli üretmek DEĞİL. ABD hisse senetleri başta olmak üzere, fiyatı düşen, yatay kalan veya yükselen şirketlerde henüz tanımlanmamış davranışları keşfetmek ve gerçek piyasa mekanizmalarıyla ilişkisini araştırmak. Önemli olan daha fazla kod değil, daha doğru sorular ve gerçek davranışı ayırt edebilen testler.`
const YASAK = `KESİN YASAKLAR: Eski başarısız sonuçları yeni eşiklerle kurtarmak; aynı OHLCV göstergelerini farklı isimlerle tekrar taramak; sadece korelasyonu mekanizma / nedensellik diye sunmak; küçük ve tekrarlanmayan etkileri iz olarak ilan etmek; eksik veriyi sıfır ya da olumsuz kanıt saymak; 13F / Form 4 kayıtlarını gerçek zamanlı işlem akışı gibi yorumlamak; bir testin geçmesini hipotezin doğrulanmasıyla karıştırmak. K51-K56 sonuçları (K51 İZ DEĞİL, K53 desteklenmeyen, K55 mekanik, K56 bağımsız dönem sonucu) değiştirilemez; kapalı konular (COL_OZET.md: giriş zamanlaması / onay / hacim, stop / erken kesme, sektör ısısı, KNN, VIX / DXY, 90'dan fazla şekil ölçüsü) yeniden açılamaz. Bir hipotez için gerekli veri yoksa veri yokluğu açıkça yazılır; vekil ölçüm gerçek veriymiş gibi sunulamaz.`
const KURALLAR = `ÇALIŞMA KURALLARI: Depo ${REPO}; YALNIZ OKU (dosya yazma, ağ isteği, boru hattı koşturma yok). Hiçbir bilgi uydurma. Girdiler (${K57}): TEST_ENVANTERI.csv (denetlenmiş testler: id, ad, soru, alanlar, sinif A-D, sonuc, kusurlar, negatif_dislananlar / dislanmayanlar), HIPOTEZ_ENVANTERI_ONCEKI.csv (önceki hipotezler), ACIK_SORULAR.md / acik_sorular.json (açık sorular, AS-xxx), ALAN_HARITASI.md, MEKANIZMA_SORULARI.md, VERI_KAYNAKLARI.csv (74 kaynak: kapsam, point_in_time, erisim_testi), VERI_BOSLUKLARI.json. Test kimliklerini, açık soru kimliklerini ve veri kaynağı kimliklerini yalnız bu dosyalarda gerçekten var olanlardan ver. Türkçe, kısa ve somut (metin alanı ~400 karakter).`
const KART = {
  type: 'object',
  properties: {
    kart_id: { type: 'string', description: 'H57-A1-01 biçimi' },
    ana_alan: { type: 'string' },
    hipotez: { type: 'string' },
    gozlenen_veya_varsayilan_davranis: { type: 'string' },
    olculebilir_mekanizma: { type: 'string' },
    gerekli_veri_kaynagi: { type: 'string' },
    veri_kaynak_idleri: { type: 'array', items: { type: 'string' } },
    veri_durumu: { type: 'string', enum: ['VAR', 'KISMEN', 'YOK', 'YALNIZ VEKİL'] },
    veri_durumu_aciklamasi: { type: 'string' },
    gozlem_birimi: { type: 'string' },
    karsilastirma_grubu: { type: 'string' },
    alternatif_aciklamalar: { type: 'array', items: { type: 'string' } },
    yanlilik_ve_sizinti_riskleri: { type: 'array', items: { type: 'string' } },
    onceden_belirlenmis_test: { type: 'string' },
    basari_ve_basarisizlik_kriteri: { type: 'string' },
    bagimsiz_dogrulama_gereksinimi: { type: 'string' },
    yenilik_gerekcesi: { type: 'string', description: 'neden yeni; önceki çalışmalardan nasıl ayrılıyor; hangi önceki test / açık soruyla ilişkili' },
    ilgili_onceki_testler: { type: 'array', items: { type: 'string' } },
    kapattigi_acik_sorular: { type: 'array', items: { type: 'string' } },
    mekanizma_sorulari: { type: 'array', items: { type: 'string' }, description: '4.1-a gibi' },
    maliyet_ve_sure_tahmini: { type: 'string' },
    onerilen_durum: { type: 'string', enum: ['BEKLEMEDE', 'VERİ BEKLİYOR', 'TESTE HAZIR'] },
  },
  required: ['kart_id', 'ana_alan', 'hipotez', 'gozlenen_veya_varsayilan_davranis', 'olculebilir_mekanizma', 'gerekli_veri_kaynagi', 'veri_kaynak_idleri', 'veri_durumu', 'veri_durumu_aciklamasi', 'gozlem_birimi', 'karsilastirma_grubu', 'alternatif_aciklamalar', 'yanlilik_ve_sizinti_riskleri', 'onceden_belirlenmis_test', 'basari_ve_basarisizlik_kriteri', 'bagimsiz_dogrulama_gereksinimi', 'yenilik_gerekcesi', 'ilgili_onceki_testler', 'kapattigi_acik_sorular', 'mekanizma_sorulari', 'maliyet_ve_sure_tahmini', 'onerilen_durum'],
}
const ONERI_SCHEMA = { type: 'object', properties: { kartlar: { type: 'array', items: KART }, bu_alanda_oneri_olmamasi_gerekce: { type: 'string' } }, required: ['kartlar', 'bu_alanda_oneri_olmamasi_gerekce'] }
const ELESTIRI_SCHEMA = {
  type: 'object',
  properties: {
    kartlar: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          kart_id: { type: 'string' },
          karar: { type: 'string', enum: ['UYGUN', 'DÜZELTME GEREKLİ', 'ELENMELİ'] },
          sorun: { type: 'string' },
          kanit: { type: 'string' },
          duzeltme_onerisi: { type: 'string' },
        },
        required: ['kart_id', 'karar', 'sorun', 'kanit', 'duzeltme_onerisi'],
      },
    },
    genel_not: { type: 'string' },
  },
  required: ['kartlar', 'genel_not'],
}
const JURI_SCHEMA = {
  type: 'object',
  properties: {
    puanlar: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          kart_id: { type: 'string' },
          mekanizma_ayirt_etme_gucu: { type: 'integer', minimum: 1, maximum: 5 },
          veri_hazirligi: { type: 'integer', minimum: 1, maximum: 5 },
          maliyet_sure_uygunlugu: { type: 'integer', minimum: 1, maximum: 5 },
          yenilik: { type: 'integer', minimum: 1, maximum: 5 },
          yanlilik_sizinti_guvenligi: { type: 'integer', minimum: 1, maximum: 5 },
          kisa_gerekce: { type: 'string' },
        },
        required: ['kart_id', 'mekanizma_ayirt_etme_gucu', 'veri_hazirligi', 'maliyet_sure_uygunlugu', 'yenilik', 'yanlilik_sizinti_guvenligi', 'kisa_gerekce'],
      },
    },
    sira: { type: 'array', items: { type: 'string' }, description: 'kart kimlikleri, en öncelikliden en aza; hepsi yer almalı' },
    sira_gerekcesi: { type: 'string' },
  },
  required: ['puanlar', 'sira', 'sira_gerekcesi'],
}

phase('Oneri')
const oneri = await parallel(ALANLAR.map(([kod, ad]) => () => agent(`K57: YENİ ARAŞTIRMA KARTLARI önerisi, alan ${kod} ${ad}. ${ANA}

Önce alanı oku: ALAN_HARITASI.md bölümü ${kod}, ACIK_SORULAR (bu alana bağlı olanlar), TEST_ENVANTERI.csv'de ${kod} testleri ve kusurları, VERI_KAYNAKLARI.csv'de ${kod} kaynakları. Sonra bu alan için 2-3 (gerçekten değerli değilse daha az; hiç yoksa kartsız bırak ve gerekçeyi yaz) YENİ araştırma kartı öner. Bir kart: (a) bir MEKANİZMA sorusudur (hangi gerçek piyasa süreci, neyle ayırt edilir), sinyal / indikatör / tahmin modeli DEĞİL; (b) ölçülebilir ve mevcut veriyle (VERI_KAYNAKLARI.csv'deki gerçek durumla) ya da açıkça adlandırılmış eksik veriyle ilişkilendirilmiş; (c) alternatif açıklamaları (likidite, seçim etkisi, hayatta kalma, sulanma, bildirim gecikmesi vb.) ve nasıl ayırt edileceğini içerir; (d) açık başarı VE başarısızlık kriteri ve bağımsız doğrulama gereksinimi taşır; (e) önceki testlerle ilişkisi ve NEDEN YENİ olduğu açık (aynı OHLCV göstergesinin yeniden adlandırılması değil; önceki bir testin yöntemsel kusurunu düzelten kartlar 'yeni' sayılır ama önceki sonucu değiştirmez ve bunu açıkça yaz). Mümkünse kartı ölçüm-mekanizma ayrımına odakla: 'bu ölçüm hangi iki açıklamayı birbirinden ayırır?'.

${YASAK}

${KURALLAR}`, { label: `oneri:${kod}`, phase: 'Oneri', schema: ONERI_SCHEMA })))

const kartlar = oneri.filter(Boolean).flatMap(o => o.kartlar)
log(`${kartlar.length} kart önerildi`)

phase('Elestiri')
const LENS = [
  ['yenilik', `YENİLİK ELEŞTİRMENİSİN. Her kartı TEST_ENVANTERI.csv, HIPOTEZ_ENVANTERI_ONCEKI.csv, K56 M01-M19 (K56_HIPOTEZLER.csv) ve COL_OZET.md kapalı konularıyla karşılaştır: aynı ölçüm / aynı OHLCV göstergesi / kapalı konu / önceki testin yeniden adlandırması mı? Önceki sonucu 'kurtarma' girişimi mi? 'yenilik_gerekcesi' doğru mu?`],
  ['veri', `VERİ GERÇEKÇİLİĞİ ELEŞTİRMENİSİN. Her kartın veri iddiasını VERI_KAYNAKLARI.csv'ye (erişim testi, point_in_time, kapsam, gecikme, hayatta kalma) ve K56 erişim testi dosyalarına (arastirma_cikti/k56_mekanizma/K56_VERI_ERISIM_TESTI.csv) karşı doğrula: veri gerçekten var mı, point-in-time mı, delist / batan şirketleri kapsıyor mu, erişim testi yapıldı mı? Vekili gerçek veri gibi sunan ya da eksik veriyi görmezden gelen kartları işaretle.`],
  ['yanlilik', `YANLILIK VE SIZINTI ELEŞTRİMENİSİN. Her kartın tasarımında gelecek bilgisi sızıntısı, seçim yanlılığı (olay tanımı, ilk geçiş etkisi, hayatta kalma), bağımlı gözlem / kümeleme, çoklu test, eşleştirmenin mekanizmayı sızdırması, 'bağımsız' dönemin bağımsız olmaması, korelasyon-nedensellik karıştırması, 13F / Form 4 gecikmesi ve sahiplik ≠ işlem akışı hatası var mı? Başarı / başarısızlık kriteri önceden ve ayırt edici mi?`],
]
const el = await parallel(LENS.map(([ad, tanim]) => () => agent(`K57: Aşağıdaki araştırma kartlarının ${tanim}

${YASAK}

${KURALLAR}

Her kart için bir karar ver (UYGUN / DÜZELTME GEREKLİ / ELENMELİ), sorunu kanıtla (dosya + satır / kimlik), düzeltme öner. Kartlar:
${JSON.stringify(kartlar)}`, { label: `elestiri:${ad}`, phase: 'Elestiri', schema: ELESTIRI_SCHEMA })))

phase('Siralama')
const elenmis = new Set()
for (const e of el.filter(Boolean)) for (const k of e.kartlar) if (k.karar === 'ELENMELİ') elenmis.add(k.kart_id)
const kalan = kartlar.filter(k => !elenmis.has(k.kart_id))
log(`${elenmis.size} kart bir eleştirmence ELENMELİ; ${kalan.length} kart jüriye gidiyor (elenenler de kayıtta tutulur)`)
const JURI = [
  ['bilgi', 'MEKANİZMA AYIRMA GÜCÜ ağırlıklı jüri üyesisin: hangi kartın cevabı en çok açık soruyu kapatır ve iki rakip mekanizmayı en iyi birbirinden ayırır?'],
  ['pratik', 'VERİ HAZIRLIĞI ve MALİYET ağırlıklı jüri üyesisin: hangi kart eldeki / kolay edinilen gerçek veriyle, makul sürede ve düşük kotayla en güvenilir biçimde test edilebilir?'],
  ['risk', 'YANLILIK / SIZINTI GÜVENLİĞİ ve YENİLİK ağırlıklı jüri üyesisin: hangi kart yanlış pozitif / seçim etkisi / bağımlılık riskine en az açık ve önceki çalışmalardan en gerçek biçimde ayrışıyor?'],
]
const jr = await parallel(JURI.map(([ad, tanim]) => () => agent(`K57: Aşağıdaki araştırma kartlarını sıralayan JÜRİ üyesisin. ${tanim} Her kart için 1-5 puan ver (5 en iyi): mekanizma_ayirt_etme_gucu, veri_hazirligi, maliyet_sure_uygunlugu, yenilik, yanlilik_sizinti_guvenligi; puanlarına dayanarak tüm kartları en öncelikliden en aza sırala (hiçbirini atlama). Eleştirmen notlarını dikkate al ama kartları kendin değerlendir.

${YASAK}

${KURALLAR}

KARTLAR:
${JSON.stringify(kalan)}

ELEŞTİRMEN NOTLARI (yalnız sorun bildirenler):
${JSON.stringify(el.filter(Boolean).flatMap((e, i) => e.kartlar.filter(k => k.karar !== 'UYGUN').map(k => ({ lens: LENS[i][0], ...k }))))}`, { label: `juri:${ad}`, phase: 'Siralama', schema: JURI_SCHEMA })))
log(`oneri ${oneri.filter(Boolean).length}/10, kart ${kartlar.length}, elestiri ${el.filter(Boolean).length}/3, juri ${jr.filter(Boolean).length}/3`)
return { alan_ajani: oneri.filter(Boolean).length, kart: kartlar.length, elenen: [...elenmis], juri: jr.filter(Boolean).length }
