export const meta = {
  name: 'k57-rapor-duzeltme',
  description: 'Bağımsız doğrulayıcının 17 düzeltmesini rapor sentezine uygula (düzeltilmiş JSON; orijinal saklanır)',
  phases: [{ title: 'Duzelt', detail: 'tek ajan: her düzeltmeyi metne işle, değişiklik günlüğü' }],
}
const K57 = '/home/user/col_yolu/arastirma_cikti/k57_denetim'
const BULGU = {
  type: 'object',
  properties: { baslik: { type: 'string' }, aciklama: { type: 'string' }, etkilenen_testler: { type: 'array', items: { type: 'string' } }, etki_yonu: { type: 'string' }, eski_sonuclara_etkisi: { type: 'string' }, siddet: { type: 'string', enum: ['YÜKSEK', 'ORTA', 'DÜŞÜK'] }, kanit: { type: 'string' } },
  required: ['baslik', 'aciklama', 'etkilenen_testler', 'etki_yonu', 'eski_sonuclara_etkisi', 'siddet', 'kanit'],
}
const SCHEMA = {
  type: 'object',
  properties: {
    yontemsel_ana_bulgular: { type: 'array', items: BULGU },
    sinif_dagilimi_yorumu: { type: 'string' },
    guvenilir_dayanaklar: { type: 'array', items: { type: 'object', properties: { dayanak: { type: 'string' }, testler: { type: 'array', items: { type: 'string' } }, sinir: { type: 'string' } }, required: ['dayanak', 'testler', 'sinir'] } },
    guvenilmemesi_gerekenler: { type: 'array', items: { type: 'object', properties: { iddia: { type: 'string' }, testler: { type: 'array', items: { type: 'string' } }, neden: { type: 'string' } }, required: ['iddia', 'testler', 'neden'] } },
    negatif_sonuclarin_genel_siniri: { type: 'string' },
    zorunlu_tasarim_ilkeleri: { type: 'array', items: { type: 'string' } },
    sinirlamalar: { type: 'array', items: { type: 'string' } },
    uygulanan_duzeltmeler: { type: 'array', items: { type: 'string' }, description: 'her düzeltme için: hangi bulgu / dayanak, ne değişti (eski -> yeni, kısa)' },
    uygulanmayan_duzeltmeler: { type: 'array', items: { type: 'string' }, description: 'uygulanmayan düzeltme ve nedeni' },
  },
  required: ['yontemsel_ana_bulgular', 'sinif_dagilimi_yorumu', 'guvenilir_dayanaklar', 'guvenilmemesi_gerekenler', 'negatif_sonuclarin_genel_siniri', 'zorunlu_tasarim_ilkeleri', 'sinirlamalar', 'uygulanan_duzeltmeler', 'uygulanmayan_duzeltmeler'],
}
const r = await agent(`K57 yöntemsel denetim raporu: bağımsız doğrulayıcının düzeltmelerini sentez metnine UYGULA. Girdiler: ${K57}/ham/rapor_sentez.json (sentez; alanlar yontemsel_ana_bulgular[14], sinif_dagilimi_yorumu, guvenilir_dayanaklar[11], guvenilmemesi_gerekenler[14], negatif_sonuclarin_genel_siniri, zorunlu_tasarim_ilkeleri, sinirlamalar) ve ${K57}/ham/rapor_dogrulama.json (kontrol[45]: baslik, durum DOĞRU / DÜZELTME GEREKLİ / KANITSIZ, sorun, duzeltme). Bash + python ile oku (Read aracını kullanma); dosyaları DEĞİŞTİRME.

Kurallar: (1) Her 'DÜZELTME GEREKLİ' ve 'KANITSIZ' kontrol satırının düzeltmesini ilgili bulgu / dayanak / iddia metnine işle (sayıyı düzelt, yanlış kimliği çıkar, cümleyi daralt, 'KANITSIZ' sayıyı doğrulayıcının önerdiği ifadeyle değiştir). Doğrulayıcının 'baslik' alanı sentezdekiyle birebir aynı olmayabilir (B1, B4 ... önekleri, 'Güvenilir dayanak 2: ...' gibi): içerikten eşleştir. (2) 'DOĞRU' satırları değiştirme. (3) Yeni bulgu ekleme, yeni iddia üretme; yalnız doğrulayıcının kanıtlı düzeltmelerini uygula. Doğrulayıcının düzeltmesi sentezin kendi kanıtıyla çelişiyorsa uygulama ve uygulanmayan_duzeltmeler'e nedenini yaz. (4) Her uygulanan düzeltmeyi uygulanan_duzeltmeler'e kısa yaz (hangi madde, eski -> yeni). (5) Test kimliklerini yalnız TEST_ENVANTERI.csv'de var olanlardan bırak (${K57}/TEST_ENVANTERI.csv 'id' sütunu). (6) Türkçe; metin uzunlukları orijinale yakın kalsın; 'ABD-ADAY' gibi iz kategorisi etiketlerini doğrulayıcının dediği gibi kaldır. Depo yalnız okunur; ağ yok.`, { label: 'rapor:duzeltme', phase: 'Duzelt', schema: SCHEMA })
log(`uygulanan ${r ? r.uygulanan_duzeltmeler.length : '?'}, uygulanmayan ${r ? r.uygulanmayan_duzeltmeler.length : '?'}`)
return { uygulanan: r ? r.uygulanan_duzeltmeler.length : null, uygulanmayan: r ? r.uygulanmayan_duzeltmeler.length : null }
