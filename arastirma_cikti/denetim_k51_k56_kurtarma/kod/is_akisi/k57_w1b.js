export const meta = {
  name: 'k57-veri-kaynaklari',
  description: 'VERI_KAYNAKLARI.csv: K51-K56 veri kaynaklarının ve 10 alan için gereken kaynakların kapsam / gecikme / erişim testi envanteri; bağımsız doğrulama',
  phases: [{ title: 'Envanter', detail: 'iki ajan: fiyat-hacim-makro ve temel-sahiplik-olay kaynakları' }, { title: 'Dogrulama', detail: 'tek bağımsız doğrulayıcı, eksik kaynak taraması' }],
}
const REPO = '/home/user/col_yolu'
const ALANLAR = 'A1 Fiyat davranışı; A2 Hacim ve işlem akışı; A3 Volatilite ve risk rejimi; A4 Zaman ve süre davranışı; A5 Piyasa mikro yapısı; A6 Göreceli güç ve piyasa konumu; A7 Şirket temelleri; A8 Sahiplik, sermaye ve kurumsal olaylar; A9 Sektör, makroekonomi ve dış etkenler; A10 Birleşik davranışlar ve alanlar arası ilişkiler'
const KURALLAR = `ÇALIŞMA KURALLARI (kesin):
- Depo: ${REPO}. YALNIZ OKU: dosya yazma / düzenleme, git (status/log/show/diff dışında), ağ isteği, K55 / K56 boru hattı koşturma YOK. Hafif okuma serbest.
- Hiçbir bilgi uydurma. Kaynakta yoksa "KAYITLI DEĞİL". Her satıra kaynak_atiflari (dosya + bölüm / satır / sütun) ekle.
- ERİŞİM TESTİ DURUMU yalnız K56'nın gerçekten yaptığı testlerden okunur (arastirma_cikti/k56_mekanizma/K56_VERI_ERISIM_TESTI.csv, K56_VERI_KAYNAKLARI.csv sütunları erisim_testi / erisim_durumu / kesif_kapsam, K56_KOSU_ERISIM.json, K56_ERISIM_*.csv). Yapılmamış testi "YAPILMADI" yaz; asla GEÇTİ varsayma. Bilgin dışarıdan (bellek) geliyorsa kaynak "genel bilgi, doğrulanmadı" diye işaretle ve erişim durumunu YAPILMADI bırak.
- Vekil (proxy) ölçümü gerçek veri gibi sunma: bir alan için doğrudan veri yoksa "DOĞRUDAN VERİ YOK; vekil: ..." yaz.
- Türkçe, kısa ve somut (metin alanı ~350 karakter).
- Bu görevin kapsamı: ABD hisse senetleri başta olmak üzere (K51-K56'da kullanılan ve 10 araştırma alanı için gerekli) veri kaynakları. K51 öncesi BIST kaynakları kapsam dışı (yalnız ABD'de kullanılmadıysa not düşme).`
const ROW = {
  type: 'object',
  properties: {
    kaynak_id: { type: 'string' },
    ad: { type: 'string' },
    tur: { type: 'string', description: 'fiyat / işlem / sahiplik / temel / kurumsal olay / analist / makro / sektör / diğer' },
    alanlar: { type: 'array', items: { type: 'string' }, description: 'A1..A10' },
    kapsam: { type: 'string', description: 'tarih aralığı, evren, eksik yerler' },
    point_in_time: { type: 'string', description: 'EVET / HAYIR / KISMEN + gerekçe (yayın / bildirim gecikmesi, sonradan revizyon)' },
    gecikme_ve_sinirlar: { type: 'string' },
    hayatta_kalma_delist_kapsami: { type: 'string' },
    maliyet_lisans: { type: 'string' },
    projede_kullanildi: { type: 'string', description: 'hangi K5x çalışmasında, hangi amaçla; kullanılmadıysa HAYIR' },
    erisim_testi: { type: 'string', enum: ['GEÇTİ', 'KISMEN GEÇTİ', 'BAŞARISIZ', 'YAPILMADI'] },
    erisim_testi_kaniti: { type: 'string' },
    yerel_kopya: { type: 'string', description: 'repoda / islenmis-veri dalında / Drive / yok' },
    olcebilen: { type: 'string' },
    olcemeyen: { type: 'string' },
    kaynak_atiflari: { type: 'array', items: { type: 'string' } },
  },
  required: ['kaynak_id', 'ad', 'tur', 'alanlar', 'kapsam', 'point_in_time', 'gecikme_ve_sinirlar', 'hayatta_kalma_delist_kapsami', 'maliyet_lisans', 'projede_kullanildi', 'erisim_testi', 'erisim_testi_kaniti', 'yerel_kopya', 'olcebilen', 'olcemeyen', 'kaynak_atiflari'],
}
const SCHEMA = { type: 'object', properties: { satirlar: { type: 'array', items: ROW }, alan_bosluklari: { type: 'array', items: { type: 'string' }, description: '10 alandan her biri için doğrudan veri olmayan boşluklar' }, notlar: { type: 'array', items: { type: 'string' } } }, required: ['satirlar', 'alan_bosluklari', 'notlar'] }
const VSCHEMA = {
  type: 'object',
  properties: {
    duzeltmeler: { type: 'array', items: { type: 'object', properties: { kaynak_id: { type: 'string' }, alan: { type: 'string' }, dogru_deger: { type: 'string' }, kanit: { type: 'string' } }, required: ['kaynak_id', 'alan', 'dogru_deger', 'kanit'] } },
    kanitlanamayan: { type: 'array', items: { type: 'string' } },
    eksik_kaynaklar: { type: 'array', items: ROW, description: '10 alan için gerekli olup tabloda olmayan kaynaklar (erişim testi YAPILMADI ise öyle yaz)' },
    genel_not: { type: 'string' },
  },
  required: ['duzeltmeler', 'kanitlanamayan', 'eksik_kaynaklar', 'genel_not'],
}
phase('Envanter')
const [a, b] = await parallel([
  () => agent(`K57 denetiminde VERİ KAYNAKLARI envanteri (bölüm 1/2): fiyat / hacim / işlem akışı / mikro yapı vekilleri / volatilite / göreceli güç / makro-sektör kaynakları. K51-K56'da gerçekten kullanılan kaynakları (Yahoo OHLCV V_ABD, K34 Yahoo, Tiingo adj fiyat + sembol listesi + batan şirketler, endeks / SPY / VIX vb., sektör sınıfları, bölünme / temettü düzeltmesi, kur) ve K56 Faz 0'ın 28 kaynaklı tablosundaki aynı alanlara ait kaynakları (FINRA kısa pozisyon, işlem raporu / ATS, FRED, vb., hangisi varsa) satır satır yaz. Bölünme-düzeltilmiş fiyat, hisse sayısı, işlem hacmi tanımı ve yuvarlak lot / TRF sorunları gibi veri-tanımı sınırlarını gecikme_ve_sinirlar'a işle.

${KURALLAR}

Başlangıç: ${REPO}/arastirma_cikti/k56_mekanizma/K56_VERI_KAYNAKLARI.csv (28 satır), K56_VERI_ERISIM_TESTI.csv, K56_FAZ0_RAPOR.md §4-5, K56/ortak.py ve K56/*.py veri modülleri, COL_YOLU_ABD.py (cy_veri_yukle, K34), arastirma_cikti/col_yolu_abd/K51_VERI_DENETIMI.md, K54_RAPOR.md, arastirma_cikti/k55_dallanma/K55_VERI_KAPSAMI.md, ${REPO}/CLAUDE.md (Veri bölümü). ALANLAR: ${ALANLAR}`, { label: 'veri:fiyat-hacim-makro', phase: 'Envanter', schema: SCHEMA }),
  () => agent(`K57 denetiminde VERİ KAYNAKLARI envanteri (bölüm 2/2): şirket temelleri, sahiplik, sermaye ve kurumsal olaylar, analist, sektör kaynakları. K51-K56'da kullanılan kaynakları (Yahoo analist not günlüğü, SEC EDGAR submissions / companyfacts / başvuru geçmişi, SEC 8-K 1.03 / 2.01 / 25-NSE, 13F veri setleri, Form 4 [K30; ABD], SC 13D/G, S-3 / 424B / ATM / dönüştürülebilir / warrant, finansal tablo veri setleri, SIC kodları, company_tickers, OpenFIGI vb.) ve K56 Faz 0'ın 28 kaynaklı tablosundaki aynı alanlara ait kaynakları satır satır yaz. Gecikme ve point-in-time sorunlarını (başvuru tarihi vs dönem sonu, 13F 45 gün, Form 4 2 gün, sonradan revizyon, yalnız bugünün şirket-kimlik eşlemesi) açıkça yaz.

${KURALLAR}

Başlangıç: ${REPO}/arastirma_cikti/k56_mekanizma/K56_VERI_KAYNAKLARI.csv (28 satır), K56_VERI_ERISIM_TESTI.csv, K56_ERISIM_*.csv, K56_FAZ0_RAPOR.md §4-5, K56/kurumsal_sahiplik.py, iceriden_islemler.py, finansal_mekanizma.py, kurumsal_olaylar.py, K56/ortak.py, arastirma_cikti/col_yolu_abd/K51_ANALIST_VERI_KAPSAMI.csv ve K51_ANALIST_TARIHSEL_VERI_DENETIMI.md, K54_RAPOR.md, ${REPO}/CLAUDE.md (SEC / Form 4 / Tiingo kuralları). ALANLAR: ${ALANLAR}`, { label: 'veri:temel-sahiplik-olay', phase: 'Envanter', schema: SCHEMA }),
])
phase('Dogrulama')
const v = await agent(`K57 denetiminde VERİ KAYNAKLARI envanterinin BAĞIMSIZ DOĞRULAYICISISIN. İki ajan aşağıdaki tabloları üretti. (1) Her satırın olgusal iddialarını (kapsam, gecikme, erişim testi durumu ve kanıtı, projede kullanım) kaynak dosyalara dönüp doğrula; yanlışları düzelt (kaynak_id, alan, doğru değer, kanıt). Özellikle "erişim_testi" alanı: K56'nın gerçekten yaptığı test sonucuyla birebir mi? (2) 10 araştırma alanı (${ALANLAR}) için gerekli olup tabloda olmayan kaynakları eksik_kaynaklar altında satır olarak ekle (erişim testi YAPILMADI ise öyle yaz; bellek bilgisi doğrulanmış sayılmaz). (3) Her alan için doğrudan veri boşluklarını (alan_bosluklari) kontrol et, eksikse genel_not'a yaz.

${KURALLAR}

TABLO 1:
${JSON.stringify(a)}

TABLO 2:
${JSON.stringify(b)}`, { label: 'veri:dogrulama', phase: 'Dogrulama', schema: VSCHEMA })
log(`satır: ${(a ? a.satirlar.length : 0)} + ${(b ? b.satirlar.length : 0)}; düzeltme ${v ? v.duzeltmeler.length : '?'}; eksik kaynak ${v ? v.eksik_kaynaklar.length : '?'}`)
return { satir1: a ? a.satirlar.length : 0, satir2: b ? b.satirlar.length : 0, duzeltme: v ? v.duzeltmeler.length : null, eksik: v ? v.eksik_kaynaklar.length : null }
