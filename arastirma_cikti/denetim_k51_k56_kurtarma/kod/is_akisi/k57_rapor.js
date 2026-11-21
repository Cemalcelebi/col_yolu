export const meta = {
  name: 'k57-rapor-sentezi',
  description: 'TEST_ENVANTERI.csv üzerinden yöntemsel denetim raporunun ana bulguları (kanıt kimlikli) + ayrı doğrulama',
  phases: [{ title: 'Sentez', detail: 'tek ajan: ana yöntemsel bulgular' }, { title: 'Dogrulama', detail: 'bağımsız doğrulayıcı: atıf ve genelleme kontrolü' }],
}
const REPO = '/home/user/col_yolu'
const K57 = `${REPO}/arastirma_cikti/k57_denetim`
const KURALLAR = `ÇALIŞMA KURALLARI (kesin): Depo ${REPO}; YALNIZ OKU (dosya yazma, ağ isteği, boru hattı koşturma yok). Hiçbir bilgi uydurma; her bulguyu TEST_ENVANTERI.csv'deki gerçek test kimlikleriyle kanıtla (kimlik biçimi örn. K51B-T07; var olmayan kimlik yazma). Girdiler: ${K57}/TEST_ENVANTERI.csv (137 test satırı; sütunlar: id, calisma_birimi, ad, soru, alanlar, sinif A-D, sinif_gerekcesi, kusurlar, negatif_dislananlar, negatif_dislanmayanlar, mekanizma_ayirt_edebilir_mi, sonuc, onkayit_dosya, kod_dosya, onkayit_kod_hash, dogrulama_durumu, duzeltme_kaydi, v2_notlari ...), ${K57}/ham/denetim_*.json (birim_geneli_kusurlar), ${K57}/ham/v2_*.json (genel_not). Türkçe, kısa ve somut. İLKE: yöntemsel kusur bulunması hipotezi doğru yapmaz, test edilmiş olması doğru test edildiği anlamına gelmez; K51-K56 sonuçları DEĞİŞTİRİLEMEZ — burada yalnız yorum sınırı yazılır. Sinyal / iz iddiası yazma.`
const BULGU = {
  type: 'object',
  properties: {
    baslik: { type: 'string' },
    aciklama: { type: 'string' },
    etkilenen_testler: { type: 'array', items: { type: 'string' } },
    etki_yonu: { type: 'string', description: 'sonucu hangi yönde / ne kadar yanıltabilir; belirsizse belirsiz de' },
    eski_sonuclara_etkisi: { type: 'string', description: 'sonuç değişmez; yalnız hangi yorumun artık yapılamayacağı' },
    siddet: { type: 'string', enum: ['YÜKSEK', 'ORTA', 'DÜŞÜK'] },
    kanit: { type: 'string' },
  },
  required: ['baslik', 'aciklama', 'etkilenen_testler', 'etki_yonu', 'eski_sonuclara_etkisi', 'siddet', 'kanit'],
}
const SCHEMA = {
  type: 'object',
  properties: {
    yontemsel_ana_bulgular: { type: 'array', items: BULGU, description: '8-14 madde, şiddete göre sıralı' },
    sinif_dagilimi_yorumu: { type: 'string' },
    guvenilir_dayanaklar: { type: 'array', items: { type: 'object', properties: { dayanak: { type: 'string' }, testler: { type: 'array', items: { type: 'string' } }, sinir: { type: 'string' } }, required: ['dayanak', 'testler', 'sinir'] }, description: 'A / B sınıfı testlerin gerçekten desteklediği dar sonuçlar ve sınırları' },
    guvenilmemesi_gerekenler: { type: 'array', items: { type: 'object', properties: { iddia: { type: 'string' }, testler: { type: 'array', items: { type: 'string' } }, neden: { type: 'string' } }, required: ['iddia', 'testler', 'neden'] } },
    negatif_sonuclarin_genel_siniri: { type: 'string' },
    zorunlu_tasarim_ilkeleri: { type: 'array', items: { type: 'string' }, description: 'bundan sonraki her araştırma kartının uyması gereken, bulgulardan çıkan tasarım kuralları (kanıt kimlikli)' },
    sinirlamalar: { type: 'array', items: { type: 'string' }, description: 'bu denetimin kendi sınırları (okunamayan kaynak, kanıtlanamayan iddialar, tek denetçi vb.)' },
  },
  required: ['yontemsel_ana_bulgular', 'sinif_dagilimi_yorumu', 'guvenilir_dayanaklar', 'guvenilmemesi_gerekenler', 'negatif_sonuclarin_genel_siniri', 'zorunlu_tasarim_ilkeleri', 'sinirlamalar'],
}
const DSCHEMA = {
  type: 'object',
  properties: {
    kontrol: { type: 'array', items: { type: 'object', properties: { baslik: { type: 'string' }, durum: { type: 'string', enum: ['DOĞRU', 'DÜZELTME GEREKLİ', 'KANITSIZ'] }, sorun: { type: 'string' }, duzeltme: { type: 'string' } }, required: ['baslik', 'durum', 'sorun', 'duzeltme'] } },
    gecersiz_kimlikler: { type: 'array', items: { type: 'string' } },
    genel_not: { type: 'string' },
  },
  required: ['kontrol', 'gecersiz_kimlikler', 'genel_not'],
}
phase('Sentez')
const s = await agent(`K57 yöntemsel denetim RAPORU için ANA BULGULARI sentezle. 137 test satırını (TEST_ENVANTERI.csv) ve birim genel kusurlarını oku; birden çok testi / çalışmayı etkileyen ORTAK yöntemsel kusurları (örn. hayatta kalma ve batan şirket ele alışı, 'bağımsız' dönemlerin bağımsız olmaması, olay tanımının seçim etkisi, ölçüm-mekanizma boşluğu / vekil ölçüm, çoklu test ailesinin kapsamı, bağımlı gözlemler, sonradan eklenen ön kayıt maddeleri, aynı yazar / kod / panel, veri tanımı belirsizlikleri) ve bunların hangi testleri, hangi yönde etkilediğini çıkar. Yalnız TEST_ENVANTERI'nde gerçekten görülen kusurları yaz (frekans say: kaç test, hangi kimlikler). Ayrıca A/B sınıfı testlerin gerçekten desteklediği DAR sonuçları ve güvenilmemesi gereken yorumları, negatif sonuçların genel sınırını ve bu bulgulardan çıkan ZORUNLU TASARIM İLKELERİNİ (sonraki araştırma kartları için) yaz.

${KURALLAR}`, { label: 'rapor:sentez', phase: 'Sentez', schema: SCHEMA })
phase('Dogrulama')
const d = s ? await agent(`K57 yöntemsel denetim raporunun ana bulgularını BAĞIMSIZ DOĞRULA. Her bulgu için: (a) etkilenen_testler kimlikleri TEST_ENVANTERI.csv'de var mı, gerçekten o kusuru taşıyor mu (kusurlar / sinif_gerekcesi / v2_notlari sütunlarını oku); (b) genelleme abartılı mı (sayı, kapsam); (c) 'eski sonuçlara etkisi' ilkeye uyuyor mu (sonuç değiştirilmiyor; yalnız yorum sınırı). Her kontrol satırı için durum + sorun + düzeltme yaz; var olmayan kimlikleri gecersiz_kimlikler'e yaz. guvenilir_dayanaklar ve guvenilmemesi_gerekenler için de aynı kontrolü yap (kontrol satırı olarak ekle).

${KURALLAR}

RAPOR SENTEZİ:
${JSON.stringify(s)}`, { label: 'rapor:dogrulama', phase: 'Dogrulama', schema: DSCHEMA }) : null
log(`bulgu ${s ? s.yontemsel_ana_bulgular.length : '?'}; doğrulama düzeltme ${d ? d.kontrol.filter(k => k.durum !== 'DOĞRU').length : '?'}`)
return { bulgu: s ? s.yontemsel_ana_bulgular.length : null, duzeltme: d ? d.kontrol.filter(k => k.durum !== 'DOĞRU').length : null }
