export const meta = {
  name: 'k57-tamamlama-dogrulama',
  description: 'V2 eksik-test bulgusundan türeyen 26 tamamlama satırını (ham/tamamla_*.json) bağımsız kaynak doğrulamasından geçir',
  phases: [{ title: 'Dogrulama', detail: '3 ajan, birim grupları' }],
}
const REPO = '/home/user/col_yolu'
const K57 = `${REPO}/arastirma_cikti/k57_denetim`
const KURALLAR = `ÇALIŞMA KURALLARI (kesin): Depo ${REPO}. YALNIZ OKU (dosya yazma, düzenleme, ağ isteği, boru hattı koşturma yok; git yalnız status/log/show/diff). Hiçbir bilgi uydurma; kaynakta yoksa "KAYITLI DEĞİL". Türkçe, kısa ve somut. Başlangıç noktaları: ${REPO}/IZ_DEFTERI.md (ilgili Ç satırları), ilgili ön kayıt dosyaları, çıktı klasörleri (arastirma_cikti/col_yolu_abd, k55_dallanma, k56_mekanizma), kod (COL_YOLU_ABD.py, K55/, K56/), ${REPO}/CLAUDE.md.`
const V1_SCHEMA = {
  type: 'object',
  properties: {
    kontrol: { type: 'array', items: { type: 'object', properties: { test_id: { type: 'string' }, durum: { type: 'string', enum: ['DOĞRU', 'DÜZELTME GEREKLİ', 'KANITLANAMADI'] }, duzeltmeler: { type: 'array', items: { type: 'object', properties: { alan: { type: 'string' }, dogru_deger: { type: 'string' }, kanit: { type: 'string' } }, required: ['alan', 'dogru_deger', 'kanit'] } }, not: { type: 'string' } }, required: ['test_id', 'durum', 'duzeltmeler'] } },
    genel_not: { type: 'string' },
  },
  required: ['kontrol', 'genel_not'],
}
const GRUPLAR = [['K51A', 'K51B'], ['K52', 'K53', 'K55'], ['K56A', 'K56B', 'K56C']]
const sonuc = await parallel(GRUPLAR.map((g, i) => () => agent(`Sen K57 denetiminde BAĞIMSIZ KAYNAK DOĞRULAYICISISIN (V1, tamamlama satırları). Eleştirel okuyucunun işaret ettiği eksik testler için bir başka ajan test satırları üretti; bu satırlar henüz hiç doğrulanmadı. Dosyalar: ${g.map(u => `${K57}/ham/tamamla_${u}.json`).join(' , ')} (her biri {birim, kapsam_ozeti, testler[], ...}; Bash + python ile oku, dosyaları DEĞİŞTİRME; dosya yoksa o birimde tamamlama yoktur, atla). Her test_id için bir kontrol satırı döndür (hepsini kapsa). Satırdaki olgusal iddiaları (veri kaynağı / kapsam, örneklem, batan-delist ele alışı, olay tanımı, gözlem birimi, bağımlılık, eşleştirme, sızıntı kontrolü, çoklu test, sonuç ve sayılar, ön kayıt / kod / koşu kimliği, sınıf gerekçesinin dayandığı olgular) KAYNAK DOSYALARA dönüp doğrula. Yanlış ya da kanıtsız alan için alan adı (satırdaki anahtar adı) + doğru değer + kanıt (dosya:bölüm / satır) ver; emin değilsen KANITLANAMADI. Kaynakta karar üretmeyen / var olmayan bir test ise durum DÜZELTME GEREKLİ yaz ve alan 'sonuc' altında bunu açıkla.

${KURALLAR}`, { label: `v1t:grup${i + 1}`, phase: 'Dogrulama', schema: V1_SCHEMA })))
log(`tamamlama doğrulama: ${sonuc.filter(Boolean).length}/3; kontrol ${sonuc.filter(Boolean).reduce((s, r) => s + r.kontrol.length, 0)}`)
return { ajan: sonuc.filter(Boolean).length, kontrol: sonuc.filter(Boolean).map(r => r.kontrol.length) }
