# ===== OZET BOLUM 9 (2026-10-19) — COL_OZET.md'ye 25 Eyl - 18 Eki donemini ekler
# Kullanim (Colab): exec(open('/content/drive/MyDrive/col_tarayici/ozet_bolum9.py', encoding='utf-8').read())
# Once COL_OZET_yedek_YYYYMMDD.md yedegi alir. Bolum 9 zaten varsa ya da aranan metin yoksa DOKUNMADAN durur.
import os, shutil, datetime as _d
_K = '/content/drive/MyDrive/col_tarayici'
_Y = f'{_K}/COL_OZET.md'

_B9 = r'''## 9. 25 EYLÜL – 18 EKİM 2026 — SON DURUM (en güncel bölüm budur)

### 9.0 ÇALIŞMA ÇERÇEVESİ — BU DOSYANIN ROLÜ
- Sistem TEST AŞAMASINDA, nihai sürüm yok. Bu MD kural defteri değil; bağlam kopukluğuna karşı SİGORTA.
- Bir ölçü ancak tam iz bulunup (iki dönem aynı yön, simetrik etiket, plasebo/taban kıyası) testleri ve metrik hesabı
  doğru çıkınca KURAL olur. O zamana kadar her şey "deneme".
- Bölüm 1'deki "güncel kurallar" 18 Eylül durumudur. GEÇERLİ TESPİT ŞARTI aşağıdaki 9.1'dir (V1 = COL_v1.py).
- Çöl şekil metrikleri iz vermedi (9.2); bu yüzden tespit küçük muma dayandırıldı.

### 9.1 GÜNCEL TESPİT ŞARTI — KÜÇÜK MUM (V1 D7, 17 Ekim, son test)
- col_segment'te "küçük mum" = GÜN ARALIĞI (H−L, fitil dahil) ≤ 0.65 × ATR30. Eski tanım gövde |C−O| (MUM_OLCU='govde').
- Ölçüm (10 yıl, 583 hisse, aynı gün piyasaya göre), rüzgârlı sektörde dar çölden kırılım:
  2020-22: n=125 hedef %90, 60g +18, 120g +11 | 2023-26: n=97 hedef %83, 60g +5, 120g +9.
  Gövde tanımı aynı koşulda 0 / −1. Sinyal sayısı ~1/5'e iner.
- D9 uzun çöl + sektör rüzgârı (18 Eki): rüzgârlı sektörde ≥1 yıl dip çölü, 120 bar içinde önce +%20 mi önce −%10 mu:
  2016-19 %61 | 2020-22 %58 | 2023-26 %56 (piyasa 58/54/44; sektör çölsüz 45-55/49-55/41-46). Tek başına yön, "yüzde yüz" değil.
  D9b: rüzgâr = sepet − piyasa ≥ %10 VE sepet > 0 (çöküşte "az düşen" sahte rüzgârı keser; 10 yılda sonucu değiştirmedi).
- Durum: V1'de uygulandı, test sürüyor. Kural sayılmaz (9.0).

### 9.2 İZ VERMEYEN ÇÖL METRİKLERİ (küçük muma gidilmesinin nedeni)
- col_ogren v1.3 (9 Eki): 9419 tekil çöl; ayıran ölçüler yalnız tavan/taban etiketinde (geometri payı), simetrik ±%10 etikette
  hiçbiri ayırmıyor → GERÇEK İZ YOK. Doji çekirdeği (5–8 doji) ayırmıyor.
- col_tanim2 (9 Eki): Cemal'in 12 EVET çölünden 4'ünü geçiriyor, 3 HAYIR'dan 0; ayıran K2 (dip başta), K6 (en dip).
- BUYUK_YUKSELIS: büyük yükselişlerin yalnız %5'i çölden (kat 0.78). SIKISMA_TESTI: çöl içi/dışı fark yok.
- Boyut çarpanları (doji, alt fitil, dar hafta) Eylül ölçümleri; col_ogren'de doji ayırmadı → yeniden doğrulanmalı.
  Alt fitil <0.12 col_v2'de hâlâ ayrışıyor (+32 / +8.9; n=31).

### 9.3 FON TASFİYE KRİZİ — UNUTMA
- Eylül 2026'dan beri tasfiye fonu krizi: Tera, Pusula, Hedef, Atlas, A1, Pardus, Bulls portföy (COL_v1 FON_TASFIYE).
  Bu fonların payı olan hisselerde art arda taban serileri; piyasa medyanı 60 günde yaklaşık −%28 (COL_v1 D9b notu).
- 6 Ekim itibarıyla seri: ODINE 26, ANELE 19, GUNDG 18, DSTKF/ALKLC/BIGEN/IEYHO/OZATD/TEHOL/TRHOL 15, TERA/UFUK 14 gün.
  16 Ekim: ODINE, GUNDG, PRZMA, PEKGY ilk tavan; TERA, DSTKF, TRHOL, BINBN, UFUK, DURDO tabanda. SPK TERA'nın ihraç/bedelsiz başvurularını işlemden kaldırdı.
- **BU DÜŞÜŞLER GERÇEKTİR — BÖLÜNME / VERİ HATASI DEĞİL.** veri_koru_gunluk.csv'de bu hisseler için sıçrama kaydı yok;
  taban_serisi_izleme.csv fiyatları birebir tutuyor (TERA 16 Eki 22.20, DSTKF 242.80).
  Büyük düşüş görünce ÖNCE taban_serisi_izleme.csv + veri_koru_gunluk.csv'ye bak, bölünme varsayma.
- Günlük izleme: COLAB_VERILER/col_tarayici/atlas/taban_serisi_izleme.csv (eski günler *_eski_TARIH.csv) ve
  motor_karne.csv (silkeleme / zıplama_kağıt / kalkış_kağıt — kâğıt işlemler; 16 Eki: 5 STOP, kalanı açık).

### 9.4 CANLI TAKİP (16 Ekim verisi, 18 Ekim çalıştırması)
- aday 47 | açık 10 | kapanan 6, hepsi zarar: PETKM −10.7 (trail), ISSEN −28, GUBRF −26, GARFA −22.6, TERA −88.6, DSTKF −90.1 (taban, T6).
- Açık: ISDMR ALARK AKBNK BIMAS GARAN YKBNK ISCTR TRCAS DURDO ZRGYO (Eylül 7–15 girişli). 9'unda kayıtlı taban yoktu → giriş×0.85 (yedek).
  DURDO 15–16 Eki iki taban (5.68), yedek tabanı 4.43.
- 17 Eki ilk T6 çalışmasında 81 aday ÇÖL BOZULDU ile düştü (çöküş haftası).

### 9.5 KOD DEĞİŞİKLİKLERİ (üretim)
- 8 Eki bolunme_onar.py: 69 bedelsiz onarıldı. A/B (col_ab_rapor.txt) sonuç değişmedi: 2024-26 bekl +10.4→+10.6, 2023 +40.4→+40.5.
- 9 Eki BASLAT + veri_koru.py (VK_YAMA v1.0): yenileme sonrası bölünme onarımı, B2_NEDEN; olaylar veri_koru_gunluk.csv. Seans açıkken bugünün yarım barı atılır.
- COL_v1 D7 (17 Eki): küçük mum = H−L → bkz. 9.1.
- COL_v1 D8 (17 Eki): fon süzgeci — tasfiye fonu payı ≥ FON_ESIK %5 olan hisse aday olmaz (kap_fon_paylari.json, kap_nobet_ayar.json, yoksa FON_BILINEN).
- COL_v1 D9/D9b (18 Eki): uzun çöl (6/12 ay dar bant, dipte) + sektör rüzgârı (sepet − piyasa ≥ %10 VE sepet > 0), ruzgar_listesi(); sektor_BIST.csv.
- takip T6 (17 Eki): taban kırılınca çık (TABAN_TOL %2; taban yoksa col_segment, o da yoksa giriş×0.85). Cemal'in kuralı.
  DİKKAT: bölüm 3'te "taban kırılınca çık" ve "taban kırılması düşürme" testte kötü çıkmıştı — karar bekliyor.
- takip T7: fon süzgeci (açık pozisyonda yalnız uyarı). T8: D9 uzun çöl + rüzgâr gun() ekranında.

### 9.6 DİĞER ÖLÇÜMLER (tekil, ertesi açılış, onarılmış veri)
- col_v2 / yeniden_tara (8 Eki; bugünkü col_olc): 2024-26 yeni liste n=989 %69 bekl +10.8, portföy eşit +140% (yıllık +45, DD −14);
  eski liste n=555 %70 +10.3, eşit +72% (yıllık +27, DD −11). 2023 yeni n=415 %86 +40.5 eşit +133%; eski n=379 %87 +40.0 eşit +107%.
  XU100 aynı dönem +20/+73, mevduat %40.
- tahtaci_oyunu v1.3 (8 Eki): klimaks n=304 r10 −2.35, plasebodan kötü → GEÇMEDİ; teyit ve sessiz de geçmedi.
- BUYUK_YUKSELIS (2 Eki; 13 hf +%40, 3328 olay): ÇÖL deseni kazananların %5'i (kat 0.78) — büyük yükselişler çölden gelmiyor.
  Hafif iz: sektör dalgası ≥3 (kat 1.25), genişlik >70 (1.29), konum_52 ≥0.7 (1.24). Haber izi yok.
- TEYIT_BILETI (2 Eki): ertesi açılış, hedef +20, stop teyit dibi: bilet net +1.01; 2022-26 +0.41; 2026 −2.13 → zayıf.
- SIKISMA_TESTI (1 Eki): çöl içinde bilet +0.07, dışında −0.02, çöl+sivrilmiş −1.33 → fark yok.
- COL_KIRILIM_ATLAS (2 Eki): öncü/rüzgâr sırası tutarsız ("öncü yok + rüzgâr var" +8.0, "öncü var + rüzgâr" +0.4).
- QMLS_Tarayici (4 Eki): 4s bant salınımı, QMLS 2 işlem +33; salınım bulucu 266'dan 8 aday (ANGX, PUSA, BMM...). n çok az.
- KAP arşivi (3–4 Eki): kap_bildirimler.csv, kap_ozet (2017–26), fiyat_ozet, m1–m5 tabloları; KAP_ARSIV.py.

### 9.7 KLASÖRLER
- Üretim: MyDrive/col_tarayici. Araştırma çıktıları: MyDrive/COLAB_VERILER/col_tarayici/
  (atlas, sikisma, sikisma_ABD, buyuk_yukselis, teyit_bileti, kap, kap_ozet, fiyat_ozet). teshis/ = islem_goster çıktıları.
- Kod yedekleri: dosya.py.YYYYMMDD_SSDD biçiminde ayrı klasörde.

### 9.8 AÇIK / BEKLEYEN
- Küçük mum (D7) + D9: test sürüyor; tam iz ve doğru metrik hesabı gelince kural.
- T6 (taban kırılınca çık) testle çelişiyor: tut ya da kaldır.
- Boyut çarpanları (doji/fitil/dar) yeniden doğrulama.
- DURDO açık pozisyonda taban serisinde.
- 9 açık pozisyonda gerçek taban yok (yedek ×0.85).
- motor_karne kâğıt işlemleri sürüyor.

---

'''

_E1 = '## KISA BLOK'
_E2 = '(bölüm 8 = son durum).'
_YENI = ('(bölüm 9 = son durum).\n'
         'SİSTEM TEST AŞAMASINDA; bu MD bağlam sigortası, kural defteri değil. Tam iz + doğru metrik hesabı gelince kural olur.\n'
         'GÜNCEL TESPİT ŞARTI (V1 D7): küçük mum = gün aralığı H-L ≤ 0.65×ATR30 (gövde değil). Çöl şekil metrikleri iz vermedi (col_ogren).\n'
         'EYLÜL-EKİM 2026 FON TASFİYE KRİZİ: TERA/DSTKF/ODINE/GUNDG/TRHOL... taban serileri GERÇEK düşüş, bölünme değil. '
         'Büyük düşüşte önce COLAB_VERILER/col_tarayici/atlas/taban_serisi_izleme.csv + veri_koru_gunluk.csv.\n'
         'Ekim eklemeleri: D8 fon süzgeci, D9 uzun çöl + sektör rüzgârı; takip T6 taban kırılınca çık (testle çelişiyor), T7, T8; veri_koru.')

# 19 Eki ilk surumun ekledigi KISA BLOK satirlari (eski surum calistirildiysa bunlar degistirilir)
_ESKI_YENI = ('(bölüm 9 = son durum).\n'
              'EYLÜL-EKİM 2026 FON TASFİYE KRİZİ: TERA/DSTKF/ODINE/GUNDG/TRHOL... taban serileri GERÇEK düşüş, bölünme değil. '
              'Büyük düşüşte önce COLAB_VERILER/col_tarayici/atlas/taban_serisi_izleme.csv + veri_koru_gunluk.csv.\n'
              'Ekim eklemeleri: COL_v1 D7 küçük mum=H-L, D8 fon süzgeci, D9 uzun çöl + sektör rüzgârı; takip T6 taban kırılınca çık (testle çelişiyor), T7, T8; veri_koru.')

def ozet_bolum9():
    t = open(_Y, encoding='utf-8').read()
    if '### 9.0 ÇALIŞMA ÇERÇEVESİ' in t:
        print('[dur] bolum 9 (son surum) zaten var, dokunulmadi'); return
    if '## 9. 25 EYLÜL' in t:   # ilk surum calistirilmis -> o bolumu ve KISA BLOK satirlarini yenisiyle degistir
        i, j = t.find('## 9. 25 EYLÜL'), t.find(_E1)
        if not (0 <= i < j) or t.count(_ESKI_YENI) != 1:
            print('[dur] eski bolum 9 beklenen bicimde degil — dosyaya dokunulmadi'); return
        y = f'{_K}/COL_OZET_yedek_{_d.date.today():%Y%m%d}_b9eski.md'
        shutil.copy(_Y, y)
        t = t[:i] + _B9 + t[j:]
        t = t.replace(_ESKI_YENI, _YENI)
        tmp = _Y + '.tmp'
        open(tmp, 'w', encoding='utf-8').write(t); os.replace(tmp, _Y)
        print(f'[ok] eski bolum 9 yenisiyle degistirildi | yedek: {os.path.basename(y)}'); return
    if t.count(_E1) != 1 or t.count(_E2) != 1:
        print(f"[dur] aranan metin bulunamadi ('{_E1}': {t.count(_E1)}, '{_E2}': {t.count(_E2)}) — dosyaya dokunulmadi"); return
    y = f'{_K}/COL_OZET_yedek_{_d.date.today():%Y%m%d}.md'
    shutil.copy(_Y, y)
    t = t.replace(_E1, _B9 + _E1).replace(_E2, _YENI)
    tmp = _Y + '.tmp'
    open(tmp, 'w', encoding='utf-8').write(t); os.replace(tmp, _Y)
    print(f'[ok] COL_OZET.md bolum 9 eklendi, KISA BLOK guncellendi | yedek: {os.path.basename(y)}')

ozet_bolum9()
