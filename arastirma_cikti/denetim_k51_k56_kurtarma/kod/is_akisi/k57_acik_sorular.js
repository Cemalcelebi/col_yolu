export const meta = {
  name: 'k57-acik-sorular-birlestirme',
  description: 'Açık sorular listesi (38) ile tamlık eleştirmeninin 27 adayını birleştir: tekrarları ele, gerçekten eksik olanları tam alanlarla ekle, hatalı satırları düzelt',
  phases: [{ title: 'Birlestir', detail: 'tek ajan; kimlikler korunur, yeniler AS-039+' }],
}
const REPO = '/home/user/col_yolu'
const K57 = `${REPO}/arastirma_cikti/k57_denetim`
const SORU = {
  type: 'object',
  properties: {
    id: { type: 'string' }, soru: { type: 'string' }, neden_acik: { type: 'string' },
    kategori: { type: 'string', enum: ['E hiç test edilmedi', 'D veri yok', 'C yöntemsel kusur', 'B sınırlı kapsam', 'ölçüm ayırt edemiyor', 'alternatif açıklama dışlanamadı', 'bağımsız doğrulama yok'] },
    alanlar: { type: 'array', items: { type: 'string' } }, mekanizma_sorulari: { type: 'array', items: { type: 'string' } }, ilgili_testler: { type: 'array', items: { type: 'string' } },
    gerekli_veri: { type: 'string' }, veri_durumu: { type: 'string' }, onem: { type: 'string', enum: ['YÜKSEK', 'ORTA', 'DÜŞÜK'] }, onem_gerekcesi: { type: 'string' },
    kaynak_notu: { type: 'string', description: 'ilk listeden mi, eleştirmen adayından mı eklendi; birleştirilen adaylar' },
  },
  required: ['id', 'soru', 'neden_acik', 'kategori', 'alanlar', 'mekanizma_sorulari', 'ilgili_testler', 'gerekli_veri', 'veri_durumu', 'onem', 'onem_gerekcesi', 'kaynak_notu'],
}
const SCHEMA = { type: 'object', properties: { sorular: { type: 'array', items: SORU }, birlestirme_notu: { type: 'string' }, elenen_adaylar: { type: 'array', items: { type: 'string' }, description: 'eleştirmen adaylarından mevcut bir soruyla aynı olduğu için eklenmeyenler (hangi AS ile birleşti)' } }, required: ['sorular', 'birlestirme_notu', 'elenen_adaylar'] }
const r = await agent(`K57: AÇIK SORULAR LİSTESİNİ BİRLEŞTİR. İki dosya oku (Bash + python; Read kullanma; dosyaları değiştirme): ${K57}/ham/sentez_acik-sorular.json (38 soru, AS-001..AS-038, tam alanlı) ve ${K57}/ham/sentez_tamlik.json (tamlık eleştirmeninin 27 'eksik soru adayı' + 1 hatalı satır notu; eleştirmen listeyi görememişti, bu yüzden adayların çoğu mevcut sorularla örtüşebilir). Görev: (1) 38 soruyu kimlik ve içerik olarak KORU (küçük düzeltme gerekiyorsa yap ve kaynak_notu'na yaz). (2) 27 adayı tek tek mevcut 38 ile karşılaştır: aynı soruysa ekleme, elenen_adaylar'a 'aday -> AS-xxx' yaz; mevcut bir soruyu genişletiyorsa o soruya ekle; gerçekten yeni ise AS-039'dan başlayarak tam alanlı yeni soru yaz (neden_acik, kategori, alanlar A1..A10, mekanizma_sorulari 4.1-a biçimi, ilgili_testler yalnız ${K57}/TEST_ENVANTERI.csv'deki gerçek kimlikler, gerekli_veri, veri_durumu, onem + gerekçe). (3) Sorular yalnız sorudur: hipotez / sinyal / çözüm önerisi yazma; 'ücretsiz hesap / anahtar' türü işletme konuları açık araştırma sorusu değildir, elenen listesine 'kapsam dışı' diye yaz. (4) Hiçbir bilgi uydurma; kaynak yoksa KAYITLI DEĞİL. Türkçe, kısa. Depo ${REPO} yalnız okunur; ağ yok.`, { label: 'acik:birlestir', phase: 'Birlestir', schema: SCHEMA })
log(`soru ${r ? r.sorular.length : '?'}, elenen aday ${r ? r.elenen_adaylar.length : '?'}`)
return { soru: r ? r.sorular.length : null, elenen: r ? r.elenen_adaylar.length : null }
