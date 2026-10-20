# =====================================================================
#  COL SISTEMI v2 — TEK DOSYA  (2026-09-18 DENETIM DUZELTMELERI)
#
#  Kullanim:  exec(open('/content/drive/MyDrive/col_tarayici/BASLAT.py').read())
#             A,P,Kp = gun()
#
#  KURAL:
#    SEGMENT : yerel=5 dip penceresi + cekirdek/genisletme, >=20 bar, <=6 ATR
#    clv >= -0.164 | bant_son >= 0.509 | ortaust >= 0.40   (agirlik, filtre degil)
#    GIRIS   : kapanis > tavan * AL_PAY (1.002)
#    CIKIS   : %20 hedef -> TRAIL (kapanis < SMA20). Hedefsizde 120 bar. STOP YOK.
#    POZISYON: %6 x CDS x BORC x DOJI x FITIL x DAR x KURAL, ust sinir %12
#              -> tek yer: carpanlar_hesapla()  (takip.py ve DENETIM.py bunu kullanir)
#
#  ================== 2026-09-18 DUZELTMELER (denetim) ==========================
#  D1) H==L veya hacim==0 barlar (islemsiz / tavana kilitli) doji sayiliyordu ve
#      alt fitili 0 cikiyordu -> en likit olmayan hisse 1.5x2.5 carpan aliyordu.
#      Simdi doji/alt_fitil SADECE gecerli barlarda (H>L ve V>0) hesaplanir,
#      'gecerli_oran' raporlanir; gecerli_oran < LIKIT_ESIK ise doji/fitil
#      carpanlari notr (1.0) ve LIKIT_CARPAN uygulanir.
#  D2) DAR HAFTA carpani ozet'te vardi, kodda yoktu. Eklendi: dar_hafta_olc().
#      Tanim: segmentteki haftalarin, haftalik araligi < 0.7 x haftalik ATR
#      olanlarinin orani. Haftalik ATR = segment oncesi 26 haftanin ort araligi.
#      >=0.47 -> 1.3 | <0.30 -> 0.8 | arasi 1.0
#  D3) Butun carpanlar tek fonksiyonda: carpanlar_hesapla(). Sinyal gunundeki
#      segment olculeri kullanilir (kirilim gunu yeniden hesaplanmaz).
#  D4) rapor(): 'beklenti' medyanla degil ortalamayla (gercek beklenti).
#  D5) portfoy_simulasyon(): 'YILLIK' (ort getiri ^ 252/medyan sure) kaldirildi,
#      yukari sapmaliydi. Gercek yillik/drawdown icin DENETIM.portfoy().
#  D6) AL_PAY (1.002) burada tanimli; test ve canli ayni esigi kullanir.
#  ================== 2026-10-17 D7: KUCUK MUM = GUN ARALIGI ==========================
#  D7) col_segment'te 'kucuk mum' olcusu govde (|C-O|) yerine fitil dahil gun araligi (H-L).
#      Olcum (10 yil, 583 hisse, ayni gun piyasaya gore): ruzgarli sektorde dar-colden kirilim
#      20-22: n125 hedef %90 60g +18 120g +11 | 23-26: n97 hedef %83 60g +5 120g +9;
#      govde tanimi ayni kosulda 0/-1. Sinyal sayisi ~1/5'e iner. MUM_OLCU='govde' eski davranis.
#  D8) FON SUZGECI (Eylul 2026 fon tasfiye krizi, Cemal'in kurali): tasfiye kapsamindaki portfoy
#      sirketlerinin fonlarinin payi >= FON_ESIK olan hisse bugun_liste'ye girmez, 'FON ELENDI' diye yazilir.
#      Kaynak: col_tarayici/kap_fon_paylari.json + kap_nobet_ayar.json (PC'deki kap klasorunden kopyala);
#      dosya yoksa FON_BILINEN tablosu (KTLEV, GUNDG, DSTKF, PASEU, ODINE, HEDEF, TERA, IZFAS, LIDER).
#  ================== 2026-10-18 D9: UZUN COL + SEKTOR RUZGARI ==========================
#  D9) Cemal'in buyuk-resim colu: aylarca (6-12 ay) suren dar bant, dipte, silkelemeler dahil;
#      sektor ruzgari varken alinir, ruzgar yokken col aranmaz ("fal bakmak gibi").
#      Olcum (10 yil, 583 hisse, BIST alt endeks sepetleri; 120 bar icinde once +%20 mi, once -%10 mu):
#        ruzgarli sektorde >=1 yil dip colu: 16-19 %61 | 20-22 %58 | 23-26 %56  (piyasa 58/54/44, sektor colsuz 45-55/49-55/41-46)
#        -> uc donemde de piyasanin ve sektor akranlarinin ustunde (tek basina yon, "yuzde yuz" degil).
#      Tanim: UZUN_W bar kapanislarin %5-%95 araligi <= UZUN_BANT; ort gun araligi/fiyat <= UZUN_MUM;
#             pencere medyani onceki 500 barin alt yarisinda (UZUN_KONUM). Ruzgar: alt sektor sepeti (hisse haric)
#             RUZ_GERI gunluk getirisi - piyasa medyani >= RUZ_ESIK.
#      Sektor dosyasi: col_tarayici/sektor_BIST.csv (BIST alt endeksleri, 'alt_bist' sutunu); yoksa sektor_TR.csv (Yahoo).
#      bugun_liste(): adaylara 'uzun' (6ay/12ay) ve 'ruz' (sektor ruzgari %) sutunu; sonunda RUZGAR LISTESI:
#      ruzgarli sektorlerde uzun colde olan TUM hisseler (col_segment adayi olmasa da). Kapatmak: RUZGAR_LISTE=False.
#  D9b) 2026-10-18: ruzgar = sepet - piyasa >= RUZ_ESIK VE sepetin kendisi > RUZ_MUTLAK (0). Neden: Eylul 2026 fon
#      krizinde piyasa medyani 60g -%28 iken XBANK -%20, XSGRT -%14, XMANA -%19 'ruzgarli' gorunuyordu (az dusen != ruzgar).
#      10 yil testinde bu sart sonucu degistirmedi (2631 olaydan 46'si sepet<=0) — sadece cokuste sahte ruzgari keser.
#      ruzgar_listesi() artik her ruzgarli sektorun UYELERINI 60g getirileriyle basar (ruzgari kim tasiyor) ve
#      sepet<=0 olan 'az dusen' sektorleri ayri satirda gosterir.
#  ================== 2026-10-20 D10: RUZGAR TUTARLILIGI (inceleme) ==========================
#  D10a) bugun_liste 'ruz' sutunu yalniz sayiydi; D9b sarti (sepet > RUZ_MUTLAK) yalniz ruzgar_listesi'nde ve takip
#      BEKLE'deki 'RUZGAR' etiketinde vardi -> cokus haftasinda 'az dusen' sektordeki aday 'ruz +15' gibi ruzgarli
#      gorunuyordu. Simdi sektor_ruzgar() 'ruzgar' sutununu (ruz >= RUZ_ESIK ve sepet > RUZ_MUTLAK) tek yerde hesaplar;
#      bugun_liste 'ruzgar' sutununa takip BEKLE ile ayni 'RUZGAR' etiketini yazar. Sayi ('ruz') aynen kalir.
#  D10b) sektor_ruzgar tarih hizasi: getiri her hissenin kendi son RUZ_GERI+1 barindan hesaplaniyordu.
#      (1) Verisi durmus hisse (yfinance 'no data'; BASLAT eski veriyi tutar) eski donemin getirisiyle piyasa medyanina
#          ve sepete giriyordu -> son bari ortak son tarihten RUZ_BAYAT is gunu eski hisse hesaba girmez (log'a yazilir).
#      (2) Arada islem gormedigi gunler olan hissenin penceresi geriye uzuyordu -> baslangic kapanisi her hisse icin ayni
#          takvim gunu: piyasanin RUZ_GERI bar oncesi (hisselerin o tarihlerinin medyani), o gun ve oncesindeki son kapanis.
#      Tam takvimli hissede sonuc birebir ayni (sentetik sinama). AL kurali, segment ve carpanlar DEGISMEDI.
#  ================== 2026-10-20 D11: VERISI DURMUS (BAYAT) HISSE ==========================
#  D11) veri_bayat(): son bari ortak son tarihten VERI_BAYAT (5) is gunu eski hisse 'verisi durmus' (yfinance 'no data',
#      islem durdurma; BASLAT eski veriyi tutar). Boyle hisse eski veriyle aday olabiliyor, takip'te 60 bar suresi hic
#      dolmadigi icin listede kaliyordu. bugun_liste artik bu hisseleri aday saymaz ('VERI DURDU' satiri); takip T9
#      aday listesinden dusurur. Bayat orani VERI_BAYAT_UST (%10) ustundeyse bu delist degil toplu guncelleme sorunudur:
#      suzgec uygulanmaz, uyari basilir. sektor_ruzgar'in kendi bayat sarti (D10b, RUZ_BAYAT) ayridir, degismedi.
#  ================== 2026-10-20 D12: DIP COLU (Cemal'in tarifi) ==========================
#  D12) Goz testi (GOZ_ESLE, 19 Eki): D7 col_segment Cemal'in 29 colunden 1'ini buluyordu (ATR30 colun icinde de
#      kuculdugu icin 'kucuk mum' esigi asilamiyor). Cemal'in tarifi: col dusus sonrasi DIPTE olusur; bir noktadan sonra
#      fiyat yeni dip yapmaz; fiyat dusmeyince mumlar kuculur, Bollinger daralir, doji olusur, hacim kurur.
#      col_dip(): (1) BOLGE: GOZ_ESLE.bolge_col v1.3 ile birebir ayni kural (hisseye ozel normal gun = 250 bar medyan
#      gun araligi; cekirdek bant <= 6x, cok ayrilma ve pespese 3 buyuk mum bolgeyi bitirir, inis mumlari kirpilir);
#      (2) DIPTE: bolge medyani, bolge + onceki 250 barin araliginin alt DIP_KONUM'unda; (3) YENI DIP YOK: bolgenin son
#      DIP_SON_PAY kisminda onceki dibin altina (yarim normal gunden fazla) inis yok; (4) IMZA: kucuk mum (bolge barlarinin
#      >= IMZA_KUCUK'u normal gunden kucuk), Bollinger daralma (bolgedeki en dar bant son 250 gunun en dar IMZA_BB'sinde),
#      doji artisi (oran >= bolge oncesi 250 barin IMZA_DOJI kati), hacim kuruma (medyan hacim <= bolge oncesi 60 barin
#      IMZA_HACIM'i) — 4'ten en az IMZA_MIN. Cikti col_segment ile ayni alanlar (+ konum, imza...), col_olc SEGMENT_MOD'a
#      gore col_dip ya da col_segment kullanir. col_segment DEGISMEDI (olcum modulleri onu acikca cagiriyor).
#      Goz testi (37 etiket): eski 1/29, col_dip 12/29 tam pencere (+4 kismi); bolge kurali GOZ_ESLE ile 2379/2379 ayni.
#      COL_DIP_TEST (20 Eki; atilimda ertesi gun acilis alim, %20 sonra SMA20 trail / 120 bar, tekil; taban = her taze 20 gun
#      zirvesi kirilimi): beklenti dip / taban — BIST 16-19 +14.7/+13.8 | 20-22 +15.9/+24.1 | 2023 +42.0/+28.8 | 24-26 +6.9/+9.2 |
#      ABD 22-23 +1.6/+3.2 | ABD 24-26 +11.3/+5.6 -> 6 donemin 3'unde tabandan iyi: TABANI GECMEDI (iz degil; atilim + trail
#      yine asil kaynak, COL_OZET 8. bolum ile ayni). Eski col_segment ile ayni orneklemde dip daha iyi: 2023 +47.1/+29.5,
#      24-26 +8.6/+6.4. Uretimde SEGMENT_MOD='dip' (20 Eki): eski tespitten iyi ve Cemal'in collerini goruyor; kural degil.
#  ============================================================================
#
#  CDS REJIMI: pct250 <0.3 ->0.5x | 0.3-0.6 ->1.0x | >=0.6 ->1.5x
#  BORC: net_borc/ozkaynak <0 ->1.5x | 0-0.3 ->1.0x | >0.3 ->0.7x | ozkaynak<=0 ->0.7x
#  DOJI (gecerli barlarda |C-O|/(H-L)<0.15): >=0.23 ->1.5 | <0.13 ->0.7
#  FITIL (gecerli barlarda ort alt fitil / ATR): <0.12 -> 2.5
#  TRAIL: 3 sette hedefi yendi. STOP: her seviyede kotu.
# =====================================================================
import logging, numpy as np, pandas as pd

log = logging.getLogger('col')
if not log.handlers:
    _h = logging.StreamHandler(); _h.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    log.addHandler(_h); log.setLevel(logging.WARNING)

# ---------------- PARAMETRELER ----------------
E_CLV, E_BS, E_OU = -0.164, 0.509, 0.40
MIN_UZ, MAX_YUK   = 20, 6.0
E_ONC = -28.2      # eski esik, KULLANILMIYOR
HEDEF = 20
BIST_MODU = False
CIKIS = 'trail'
POZISYON_TABAN = 6.0
POZISYON_UST   = 12.0
YEREL = 5
MUM_OLCU = 'aralik'     # D7: 'aralik' (H-L, fitil dahil) | 'govde' (|C-O|, 2026-10-17 oncesi davranis)
FON_ELE = True          # D8: tasfiye fonu payi olan hisseyi aday listesinden dusur (Cemal'in Eylul 2026 kurali)
FON_ESIK = 5.0          # D8: fiili dolasim / sermaye payi (%) bu esik ve ustundeyse 'FON' — elenir
FON_TASFIYE = ['TERA PORTFOY','PUSULA PORTFOY','HEDEF PORTFOY','ATLAS PORTFOY','A1 PORTFOY','PARDUS PORTFOY','BULLS PORTFOY']
# D8: json yoksa da calissin diye bilinen paylar (KAP/basin, Agu-Eyl 2026; kaynak: Euronews 17.09, T24, KAP). Guncelleme: kap_fon_paylari.json
FON_BILINEN = [('KTLEV','PUSULA PORTFOY',25.59),('GUNDG','PUSULA PORTFOY',38.67),('DSTKF','TERA PORTFOY',39.41),
               ('PASEU','PUSULA PORTFOY',44.5),('ODINE','PUSULA PORTFOY',28.2),('HEDEF','PUSULA PORTFOY',17.5),
               ('TERA','TERA PORTFOY',16.08),('IZFAS','PUSULA PORTFOY',5.0),('LIDER','PARDUS PORTFOY',5.61)]
# D9: uzun col + sektor ruzgari
UZUN_W = 250            # D9: uzun col penceresi (bar). 250 ~ 1 yil; 120 ~ 6 ay da raporlanir
UZUN_BANT = 1.50        # D9: pencere icinde kapanis %95 yuzdelik / %5 yuzdelik <= 1.5 (bant <= %50)
UZUN_MUM = 0.04         # D9: ort gun araligi (TR) / ort fiyat <= 0.04 (kucuk mum)
UZUN_KONUM = 0.5        # D9: pencere medyani, onceki 500 barin (min..max) araliginda bu orandan asagida (dipte)
RUZ_GERI = 60           # D9: sektor ruzgari penceresi (gun)
RUZ_ESIK = 0.10         # D9: sepet getirisi (hisse haric) - piyasa medyani >= %10 -> ruzgar var
RUZ_MIN_UYE = 4         # D9: sepet icin en az uye
RUZ_MUTLAK = 0.0        # D9b: sepetin kendi RUZ_GERI getirisi bundan buyuk olmali (0 = sepet yukseliyor)
RUZ_BAYAT = 5           # D10b: son bari ortak son tarihten bu kadar is gunu eski hisse ruzgar hesabina girmez (verisi durmus)
VERI_BAYAT = 5          # D11: son bari ortak son tarihten bu kadar is gunu eski hisse aday olmaz (verisi durmus)
VERI_BAYAT_UST = 0.10   # D11: bayat orani bunu asarsa toplu veri sorunu sayilir -> bayat suzgeci uygulanmaz
# D12: dip colu (Cemal'in tarifi). Bolge parametreleri GOZ_ESLE v1.3 (GozAyar) ile ayni tutulur.
SEGMENT_MOD = 'dip'     # D12: 'dip' (col_dip: bolge + dip + imza) | 'eski' (col_segment, D7)
BOLGE_BANT_KAT = 6.0    # D12: cekirdek (%10-%90 kapanis) bandi <= bu kadar normal gun araligi
BOLGE_UZAK_KAT = 1.5    # D12: cekirdekten bu kadar normal gun otesindeki kapanis = bolgeden cok ayrilma
BOLGE_SOL_KAT = 1.5     # D12: bolge basindaki bu kadar normal gunden buyuk (inis) mumlar kirpilir
BOLGE_BUYUK_KAT = 2.0   # D12: buyuk mum = normal gun araliginin 2 kati
BOLGE_ARDISIK = 3       # D12: pespese 3 ayni yonlu buyuk mum = bolgeden ayrilma
BOLGE_MIN_BAR = 15      # D12: en kisa bolge (col_olc ayrica MIN_UZ ister)
BOLGE_EN_COK = 250      # D12: en uzun bolge (bar)
DIP_KONUM = 0.35        # D12: bolge medyani, (bolge + onceki 250 bar) araliginin alt %35'inde -> dipte
DIP_SON_PAY = 0.40      # D12: bolgenin son %40'inda onceki dibin altina inis yok (dip savunuluyor)
IMZA_MIN = 3            # D12: 4 imzadan en az bu kadari (kucuk mum, Bollinger daralma, doji artisi, hacim kuruma)
IMZA_KUCUK = 0.60       # D12: bolge barlarinin en az %60'i hissenin normal gun araligindan kucuk
IMZA_BB = 0.15          # D12: bolgedeki en dar Bollinger genisligi, son 250 gunun en dar %15'inde
IMZA_DOJI = 1.0         # D12: bolgedeki doji orani >= bolge oncesi 250 barin doji orani x bu kat
IMZA_HACIM = 0.90       # D12: bolge medyan hacmi <= bolge oncesi 60 bar medyan hacminin %90'i
RUZGAR_LISTE = True     # D9: bugun_liste sonunda ruzgar listesi bas
SEKTOR_DOSYALAR = ['sektor_BIST.csv', 'sektor_TR.csv']   # D9: col_tarayici'da sirayla aranir
AL_PAY = 1.002          # kirilim esigi: kapanis > tavan * AL_PAY  (test = canli)
DOJI_ESIK = 0.15
LIKIT_ESIK = 0.90       # segmentte gecerli bar orani bunun altindaysa doji/fitil notr
LIKIT_CARPAN = 0.5      # ... ve pozisyon yariya iner
DAR_HAFTA_ORAN = 0.7    # haftalik aralik < 0.7 x haftalik ATR -> dar hafta
CARPAN = {              # tek tablo — degistirmek icin sadece burasi
    'cds':   lambda p: 1.0 if not np.isfinite(p) else (0.5 if p < 0.3 else (1.5 if p >= 0.6 else 1.0)),
    'borc':  lambda b: 1.0 if not np.isfinite(b) else (1.5 if b < 0 else (0.7 if b > 0.3 else 1.0)),
    'doji':  lambda d: 1.0 if not np.isfinite(d) else (1.5 if d >= 0.23 else (0.7 if d < 0.13 else 1.0)),
    'fitil': lambda f: 1.0 if not np.isfinite(f) else (2.5 if f < 0.12 else 1.0),
    'dar':   lambda w: 1.0 if not np.isfinite(w) else (1.3 if w >= 0.47 else (0.8 if w < 0.30 else 1.0)),
    'kural': lambda k: 1.0 if k else 0.7,
}

# ---------------- YARDIMCILAR ----------------
def _atr_ref(x, bas_i, geri=30):
    on = x.iloc[max(0,bas_i-geri):bas_i]
    if len(on) < 8: return np.nan
    h,l,c = on["High"],on["Low"],on["Close"]
    tr = pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    return float(tr.mean())

def _egim(y, atr):
    if len(y)<3 or not np.isfinite(atr) or atr<=0: return np.nan
    return float(np.polyfit(np.arange(len(y)),y,1)[0])/atr

def gecerli_bar_maskesi(O, H, L, C, V):
    """D1: islem gormus, araligi olan bar. H>L ve V>0. NaN'lar gecersiz."""
    O,H,L,C,V = (np.asarray(a,float) for a in (O,H,L,C,V))
    m = np.isfinite(O)&np.isfinite(H)&np.isfinite(L)&np.isfinite(C)&(H>L)
    m &= np.where(np.isfinite(V), V>0, True)   # hacim yoksa (NaN) sadece H>L'ye bak
    return m

def dar_hafta_olc(x, bas_i, geri_hafta=26):
    """D2: segment [bas_i:] icindeki haftalarin, araligi < DAR_HAFTA_ORAN x haftalik ATR
    olanlarinin orani. Haftalik ATR = segment oncesi geri_hafta haftanin ort (H-L).
    Yetersiz veri -> nan."""
    try:
        w = x[['High','Low']].resample('W-FRI').agg({'High':'max','Low':'min'}).dropna()
        if len(w) < 8: return np.nan
        bas_t = x.index[bas_i]
        onc = w[w.index < bas_t].tail(geri_hafta); seg = w[w.index >= bas_t]
        # segmentin ilk haftasi bas_t'den once baslamis olabilir: o haftayi da al
        ilk = w[w.index >= bas_t - pd.Timedelta(days=7)]
        seg = ilk if len(ilk) > len(seg) else seg
        if len(onc) < 4 or len(seg) < 2: return np.nan
        w_atr = float((onc.High-onc.Low).mean())
        if not np.isfinite(w_atr) or w_atr <= 0: return np.nan
        return float(((seg.High-seg.Low) < DAR_HAFTA_ORAN*w_atr).mean())
    except Exception as e:
        log.debug(f'dar_hafta_olc hata: {e}'); return np.nan

# ---------------- SEGMENT ----------------
def col_segment(df, tarih=None, esik=0.65, tolerans=2, en_cok=120, min_bar=8,
                min_cekirdek=5, cek_tol=2, band_tol=0.35, max_egim=0.05,
                yerel=None, ihlal_tol=0.5, yazdir=False):
    yerel = YEREL if yerel is None else yerel
    x = df[df.index<=pd.Timestamp(tarih)] if tarih is not None else df
    n = len(x)
    if n < 60: return None
    O=x["Open"].to_numpy(float); C=x["Close"].to_numpy(float)
    H=x["High"].to_numpy(float); L=x["Low"].to_numpy(float); V=x["Volume"].to_numpy(float)
    # 2026-10-17 D7: 'kucuk mum' olcusu MUM_OLCU'ye gore: 'aralik' = fitil dahil gun araligi (H-L), 'govde' = |C-O| (eski)
    govde=(H-L) if MUM_OLCU=='aralik' else np.abs(C-O); D=n-1
    kucuk=np.zeros(n,bool)
    for i in range(max(0,D-60), D+1):
        a=_atr_ref(x,i,30)
        if np.isfinite(a) and a>0: kucuk[i]=govde[i]<=esik*a
    cb=None; pen=min_cekirdek+cek_tol
    for bas_i in range(D-pen+1, max(30,D-60), -1):
        if int(kucuk[bas_i:D+1].sum())>=min_cekirdek and kucuk[bas_i]: cb=bas_i
        if D-bas_i+1>=pen and int(kucuk[D-pen+1:D+1].sum())<min_cekirdek: break
    if cb is None:
        if int(kucuk[max(0,D-pen+1):D+1].sum())>=min_cekirdek:
            cb=int(np.argmax(kucuk[max(0,D-pen+1):D+1]))+max(0,D-pen+1)
        else: return None
    cek=x.iloc[cb:D+1]; atr_c=_atr_ref(x,cb,30)
    if not np.isfinite(atr_c) or atr_c<=0: return None
    ct=float(cek["Low"].min()); cu=float(np.maximum(cek["Open"],cek["Close"]).max())
    bas=cb; hata=0; kayit=[]
    for j in range(cb-1, max(0,D-en_cok)-1, -1):
        a=_atr_ref(x,j,30)
        if not np.isfinite(a) or a<=0: break
        oran=govde[j]/a; kc=oran<=esik
        band=(C[j]>=ct-band_tol*a) and (C[j]<=cu+band_tol*a)
        ye=_egim(C[j:D+1],a); eok=np.isfinite(ye) and abs(ye)<=max_egim
        kayit.append({"i":j,"tarih":x.index[j],"govde_atr":round(oran,2),"band":"OK" if band else "DISI",
                      "egim":round(ye,4) if np.isfinite(ye) else np.nan,"ok":bool(kc and band and eok)})
        if kc and band and eok: hata=0; bas=j
        else:
            hata+=1
            if hata>tolerans: break
    i2=bas
    for j in range(bas+yerel, D+1):
        a=_atr_ref(x,j,30); t_=ihlal_tol*a if (np.isfinite(a) and a>0) else 0.0
        if C[j] < float(L[max(bas,j-yerel):j].min())-t_: i2=j+1
    if i2>bas: bas=i2
    uz=D-bas+1
    if uz<min_bar: return None
    seg=x.iloc[bas:D+1]; atr_s=_atr_ref(x,bas,30)
    if not np.isfinite(atr_s) or atr_s<=0: return None
    Hs,Ls,Cs,Os,Vs=(seg[c].to_numpy(float) for c in ("High","Low","Close","Open","Volume"))
    gu=np.maximum(Os,Cs)
    # ---- D1: doji / alt fitil SADECE gecerli barlarda ----
    g = gecerli_bar_maskesi(Os,Hs,Ls,Cs,Vs); ng = int(g.sum()); gecerli_oran = ng/len(seg)
    if ng >= 5:
        rng=Hs[g]-Ls[g]
        doji=float((np.abs(Cs[g]-Os[g])/rng<DOJI_ESIK).mean())
        alt_fitil=float(((np.minimum(Os[g],Cs[g])-Ls[g])/atr_s).mean())
    else:
        doji=np.nan; alt_fitil=np.nan
    dar=dar_hafta_olc(x, bas)
    cs=x["Close"]; m=cs.rolling(20,min_periods=5).mean(); sd=cs.rolling(20,min_periods=5).std(ddof=0)
    bbw=((m+2*sd)-(m-2*sd))/m.replace(0,np.nan); ref=bbw.tail(100).dropna()
    bb=float((ref<=bbw.iloc[-1]).mean()) if len(ref)>20 else np.nan
    ov=float(V[max(0,bas-30):bas].mean()) if bas>0 else np.nan
    out={"bas_tarih":str(seg.index[0].date()),"son_tarih":str(seg.index[-1].date()),
         "uzunluk":int(uz),"hafta_bar":round(uz/5.0,1),"cekirdek_bar":int(D-cb+1),"atr_ref":round(atr_s,4),
         "govde_ort":round(float(np.abs(Cs-Os).mean())/atr_s,2),
         "doji":round(doji,3) if np.isfinite(doji) else np.nan,
         "alt_fitil":round(alt_fitil,3) if np.isfinite(alt_fitil) else np.nan,
         "dar":round(dar,3) if np.isfinite(dar) else np.nan,
         "gecerli_oran":round(gecerli_oran,3),
         "taban":round(float(Ls.min()),2),"tavan":round(float(gu.max()),2),
         "yukseklik_atr":round((float(Hs.max())-float(Ls.min()))/atr_s,2),
         "egim":round(_egim(Cs,atr_s),4),"bb_rank":round(bb,3) if np.isfinite(bb) else np.nan,
         "hacim_orani":round(float(Vs.mean())/ov,2) if (np.isfinite(ov) and ov>0) else np.nan}
    if yazdir:
        print(f"  SEGMENT {out['bas_tarih']} -> {out['son_tarih']} ({out['uzunluk']} bar, yerel={yerel}, gecerli %{100*gecerli_oran:.0f})")
        print(f"  band {out['taban']}-{out['tavan']} ({out['yukseklik_atr']} ATR) govde {out['govde_ort']} DOJI {out['doji']} fitil {out['alt_fitil']} dar {out['dar']} egim {out['egim']}")
        print(f"\n  {'tarih':11s} {'gov/ATR':>8s} {'band':>6s} {'egim':>9s} {'ok':>6s}")
        for kk in kayit[:25]:
            im="  <-- BAS" if kk["i"]==bas else ""
            eg=f"{kk['egim']:9.4f}" if np.isfinite(kk["egim"]) else "      nan"
            print(f"  {str(kk['tarih'].date()):11s} {kk['govde_atr']:8.2f} {kk['band']:>6s} {eg} {str(kk['ok']):>6s}{im}")
    return out

# ---------------- D12: DIP COLU (Cemal'in tarifi) ----------------
def _bolge_dizi(x):
    """D12: bolge kurali dizileri (GOZ_ESLE.bolge_hazirla ile ayni): kapanis, gun araligi %, kapanis degisimi %,
    hissenin normal gun araligi (250 bar medyan, %), govde orani."""
    O, H, L, C = (x[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    pc = np.r_[O[0], C[:-1]]
    with np.errstate(divide="ignore", invalid="ignore"):
        ar = 100 * (H - L) / pc
        dg = 100 * (C / pc - 1)
    ref = pd.Series(ar).rolling(250, min_periods=120).median().to_numpy()
    rng = H - L
    go = np.where(rng > 0, np.abs(C - O) / np.where(rng > 0, rng, 1), 1.0)
    return {"C": C, "H": H, "L": L, "ar": ar, "dg": dg, "ref": ref, "go": go}

def _bolge_kutu(D, e):
    """D12: e gununde biten bolge (s, e) ya da None — GOZ_ESLE.bolge_col v1.3 ile birebir ayni kural.
    Geriye dogru buyur; cekirdek = kapanislarin %10-%90 araligi. Durur: (a) cekirdek bandi > BOLGE_BANT_KAT x normal gun,
    (b) bir kapanis cekirdegin BOLGE_UZAK_KAT x normal gun otesinde, (c) BOLGE_ARDISIK pespese ayni yonlu buyuk mum.
    Bastaki inis mumlari (gun araligi > BOLGE_SOL_KAT x normal gun ya da cekirdek disi kapanis) kirpilir."""
    import bisect
    C, ar, dg, ref = D["C"], D["ar"], D["dg"], D["ref"]
    r = ref[e]
    if not np.isfinite(r) or r <= 0 or not np.isfinite(C[e]): return None
    buyuk = BOLGE_BUYUK_KAT * r
    s, seri, yon = e, 0, 0
    srt = [float(C[e])]
    def _yuzde(a, q):
        k = (len(a) - 1) * q; f = int(k)
        return a[f] + (a[min(f + 1, len(a) - 1)] - a[f]) * (k - f)
    for j in range(e - 1, max(-1, e - BOLGE_EN_COK), -1):
        if not np.isfinite(C[j]): break
        if ar[j] >= buyuk or abs(dg[j]) >= 0.9 * buyuk:
            y = 1 if dg[j] > 0 else -1
            seri = seri + 1 if (seri and y == yon) else 1
            yon = y
            if seri >= BOLGE_ARDISIK:
                s = max(s, j + BOLGE_ARDISIK); break
        else:
            seri = 0
        bisect.insort(srt, float(C[j]))
        lo, hi, med = _yuzde(srt, 0.10), _yuzde(srt, 0.90), _yuzde(srt, 0.50)
        if (hi - lo) / med * 100 > BOLGE_BANT_KAT * r: break
        tol = BOLGE_UZAK_KAT * r / 100 * med
        if C[j] > hi + tol or C[j] < lo - tol: break
        s = j
    z = C[s:e + 1]
    lo, hi = np.percentile(z, 10), np.percentile(z, 90)
    while s < e and (ar[s] > BOLGE_SOL_KAT * r or C[s] > hi or C[s] < lo): s += 1
    return (s, e) if e - s + 1 >= BOLGE_MIN_BAR else None

def _bb_genislik(x):
    """D12: Bollinger (20, 2 sigma) genisligi / orta bant — her bar icin (geriye bakar, ileriye bakis yok)."""
    cs = x['Close']; m = cs.rolling(20, min_periods=20).mean(); sd = cs.rolling(20, min_periods=20).std(ddof=0)
    return (4 * sd / m.replace(0, np.nan)).to_numpy(float)

def _col_dip_e(x, D, bbw, e, alanlar=True):
    """D12 cekirdek: e gununde biten dip colu. x, D (_bolge_dizi) ve bbw (_bb_genislik) e'yi iceren ayni seriden;
    yalniz e'ye kadarki barlar kullanilir (tarama tum seri icin dizileri bir kez kurup bu fonksiyonu her gun cagirir).
    alanlar=False: carpan alanlari (doji, fitil, dar hafta) hesaplanmaz — yalniz tespit + tavan/taban (tarama hizi).
    Donus: (sonuc | None, olculer)."""
    t = {'mod': 'dip'}
    if e + 1 < 130: t['red'] = 'veri kisa'; return None, t
    w = _bolge_kutu(D, e)
    if not w: t['red'] = 'bolge yok'; return None, t
    s, e = w; uz = e - s + 1
    C, H, L, ar, ref, go = D['C'], D['H'], D['L'], D['ar'], D['ref'], D['go']
    r0 = ref[s] if (np.isfinite(ref[s]) and ref[s] > 0) else ref[e]   # colden onceki normal gun araligi (%)
    t.update(bas_tarih=str(x.index[s].date()), son_tarih=str(x.index[e].date()), uz=int(uz))
    o0 = max(0, s - 250)
    if s - o0 < 60: t['red'] = 'gecmis kisa'; return None, t
    # (2) dipte: bolge medyani, (onceki 250 bar + bolge) araliginin neresinde (0 = en dip)
    lo, hi = float(np.nanmin(L[o0:e + 1])), float(np.nanmax(H[o0:e + 1]))
    konum = float((np.median(C[s:e + 1]) - lo) / (hi - lo)) if hi > lo else np.nan
    # (3) yeni dip yok: bolgenin son DIP_SON_PAY kisminda onceki dibin yarim normal gunden fazla altina inis yok
    k = s + max(1, int(round((1 - DIP_SON_PAY) * uz)))
    d1, d2 = float(np.nanmin(L[s:k])), float(np.nanmin(L[k:e + 1]))
    yeni_dip_yok = bool(d2 >= d1 * (1 - 0.5 * r0 / 100))
    # (4) imzalar
    kucuk = float(np.mean(ar[s:e + 1] <= r0))
    pen = bbw[max(0, e - 249):e + 1]; pen = pen[np.isfinite(pen)]
    kb = bbw[s:e + 1]; kb = kb[np.isfinite(kb)]
    bb = float((pen <= kb.min()).mean()) if (len(pen) >= 60 and len(kb)) else np.nan
    dj, dj0 = float((go[s:e + 1] < 0.10).mean()), float((go[o0:s] < 0.10).mean())
    doji_kat = (dj / dj0 if dj0 > 0 else (np.inf if dj > 0 else np.nan))
    V = x['Volume'].to_numpy(float)
    v1, v0 = np.nanmedian(V[s:e + 1]), np.nanmedian(V[max(0, s - 60):s])
    hacim_kat = float(v1 / v0) if (np.isfinite(v0) and v0 > 0 and np.isfinite(v1)) else np.nan
    imza = {'kucuk': kucuk >= IMZA_KUCUK, 'bollinger': bool(np.isfinite(bb) and bb <= IMZA_BB),
            'doji': bool(np.isfinite(doji_kat) and doji_kat >= IMZA_DOJI),
            'hacim': bool(np.isfinite(hacim_kat) and hacim_kat <= IMZA_HACIM)}
    t.update(konum=round(konum, 3) if np.isfinite(konum) else np.nan, yeni_dip_yok=yeni_dip_yok,
             kucuk_oran=round(kucuk, 3), bb_min=round(bb, 3) if np.isfinite(bb) else np.nan,
             doji_kat=round(doji_kat, 2) if np.isfinite(doji_kat) else (np.inf if doji_kat == np.inf else np.nan),
             hacim_kat=round(hacim_kat, 2) if np.isfinite(hacim_kat) else np.nan,
             imza=int(sum(imza.values())), imza_ok=','.join(a for a, v in imza.items() if v))
    if not (np.isfinite(konum) and konum <= DIP_KONUM): t['red'] = 'dipte degil'; return None, t
    if not yeni_dip_yok: t['red'] = 'yeni dip'; return None, t
    if t['imza'] < IMZA_MIN: t['red'] = 'imza az'; return None, t
    atr_s = _atr_ref(x, s, 30)
    if not np.isfinite(atr_s) or atr_s <= 0: t['red'] = 'atr yok'; return None, t
    Os = x['Open'].to_numpy(float)[s:e + 1]; Hs, Ls, Cs, Vs = H[s:e + 1], L[s:e + 1], C[s:e + 1], V[s:e + 1]
    gu = np.maximum(Os, Cs)
    out = {"bas_tarih": t['bas_tarih'], "son_tarih": t['son_tarih'],
           "uzunluk": int(uz), "hafta_bar": round(uz / 5.0, 1), "cekirdek_bar": int(uz), "atr_ref": round(atr_s, 4),
           "taban": round(float(Ls.min()), 2), "tavan": round(float(gu.max()), 2),
           "yukseklik_atr": round((float(Hs.max()) - float(Ls.min())) / atr_s, 2),
           **{a: t[a] for a in ('mod', 'konum', 'kucuk_oran', 'bb_min', 'doji_kat', 'hacim_kat', 'imza', 'imza_ok')}}
    if not alanlar: return out, t
    # col_segment ile ayni carpan alanlari (D1 gecerli bar, D2 dar hafta) — carpanlar_hesapla / takip bunlari kullanir
    g = gecerli_bar_maskesi(Os, Hs, Ls, Cs, Vs); ng = int(g.sum()); gecerli_oran = ng / uz
    if ng >= 5:
        rg = Hs[g] - Ls[g]
        doji = float((np.abs(Cs[g] - Os[g]) / rg < DOJI_ESIK).mean())
        alt_fitil = float(((np.minimum(Os[g], Cs[g]) - Ls[g]) / atr_s).mean())
    else:
        doji = np.nan; alt_fitil = np.nan
    dar = dar_hafta_olc(x.iloc[:e + 1], s)
    ov = float(np.nanmean(V[max(0, s - 30):s])) if s > 0 else np.nan
    out.update({"govde_ort": round(float(np.abs(Cs - Os).mean()) / atr_s, 2),
                "doji": round(doji, 3) if np.isfinite(doji) else np.nan,
                "alt_fitil": round(alt_fitil, 3) if np.isfinite(alt_fitil) else np.nan,
                "dar": round(dar, 3) if np.isfinite(dar) else np.nan,
                "gecerli_oran": round(gecerli_oran, 3),
                "egim": round(_egim(Cs, atr_s), 4), "bb_rank": t['bb_min'],
                "hacim_orani": round(float(np.nanmean(Vs)) / ov, 2) if (np.isfinite(ov) and ov > 0) else np.nan})
    return out, t

def col_dip(df, tarih=None, yazdir=False, tani=False):
    """D12 DIP COLU — Cemal'in tarifi: dususten sonra dipte bolge; bir noktadan sonra fiyat yeni dip yapmaz; fiyat
    dusmeyince mumlar kuculur, Bollinger daralir, doji olusur, hacim kurur.
    Sart: BOLGE + DIPTE (DIP_KONUM) + YENI DIP YOK (DIP_SON_PAY) + 4 imzadan en az IMZA_MIN.
    Donus: col_segment ile ayni alanlar (+ konum, kucuk_oran, bb_min, doji_kat, hacim_kat, imza) ya da None.
    tani=True -> (sonuc, olculer): olculer reddedilen colun nedenini ('red') ve butun olculeri tasir."""
    x = df[df.index <= pd.Timestamp(tarih)] if tarih is not None else df
    try:
        out, t = _col_dip_e(x, _bolge_dizi(x), _bb_genislik(x), len(x) - 1) if len(x) else (None, {'mod': 'dip', 'red': 'veri yok'})
    except Exception as ex:
        log.debug(f'col_dip: {ex}'); out, t = None, {'mod': 'dip', 'red': f'hata: {ex}'}
    if yazdir:
        print(f"  DIP COLU {t.get('bas_tarih','?')} -> {t.get('son_tarih','?')} ({t.get('uz',0)} bar) | konum {t.get('konum')} "
              f"yeni_dip_yok {t.get('yeni_dip_yok')} | imza {t.get('imza')} {t.get('imza_ok','')} | "
              f"kucuk {t.get('kucuk_oran')} bb {t.get('bb_min')} doji_kat {t.get('doji_kat')} hacim_kat {t.get('hacim_kat')}"
              + (f" | RED: {t['red']}" if 'red' in t else " | COL"))
    return (out, t) if tani else out

# ---------------- D8: FON SUZGECI ----------------
def _fon_norm(s):
    import re as _re
    tr = str.maketrans("ÇĞİÖŞÜçğıöşü", "CGIOSUcgiosu")
    return _re.sub(r"\s+", " ", str(s).translate(tr).upper()).strip()

_FON_DEFTER = None
def fon_defteri(yeniden=False):
    """kap_fon_paylari.json ({hisse:{kurucu:{pay,tarih}}}) + kap_nobet_ayar.json (bilinen_fon_paylari) + FON_BILINEN.
    Dosyalar col_tarayici'da aranir; yoksa yalniz FON_BILINEN. Donus: {hisse: (kurucu, pay)} — en yuksek tasfiye-fonu payi."""
    global _FON_DEFTER
    if _FON_DEFTER is not None and not yeniden: return _FON_DEFTER
    import os, json
    K = '/content/drive/MyDrive/col_tarayici'
    tasf = {_fon_norm(k) for k in FON_TASFIYE}
    d = {}
    def _koy(h, kurucu, pay):
        try: h = str(h).upper().strip(); pay = float(pay)
        except Exception: return
        if _fon_norm(kurucu) not in tasf: return
        if h not in d or pay > d[h][1]: d[h] = (str(kurucu), pay)
    for h, k, p in FON_BILINEN: _koy(h, k, p)
    try:
        y = f'{K}/kap_nobet_ayar.json'
        if os.path.exists(y):
            a = json.load(open(y, encoding='utf-8'))
            tasf |= {_fon_norm(k) for k in a.get('tasfiye_kurucular', [])}
            for sat in a.get('bilinen_fon_paylari', []):
                if len(sat) >= 3: _koy(sat[0], sat[1], sat[2])
    except Exception as e: log.warning(f'kap_nobet_ayar.json okunamadi: {e}')
    try:
        y = f'{K}/kap_fon_paylari.json'
        if os.path.exists(y):
            j = json.load(open(y, encoding='utf-8'))
            for h, kay in (j or {}).items():
                for kurucu, v in (kay or {}).items():
                    _koy(h, kurucu, v.get('pay', 0) if isinstance(v, dict) else v)
    except Exception as e: log.warning(f'kap_fon_paylari.json okunamadi: {e}')
    _FON_DEFTER = d
    return d

def fon_etiket(sembol):
    """(kurucu, pay) ya da None. FON_ESIK altindaki paylar None sayilir."""
    v = fon_defteri().get(str(sembol).upper())
    return v if (v and v[1] >= FON_ESIK) else None

# ---------------- D11: VERISI DURMUS (BAYAT) HISSE ----------------
def veri_bayat(veri=None, tarih=None, gun=None):
    """D11: verisi durmus hisseler (yfinance 'no data' / islem durdurma; BASLAT eski veriyi tutar).
    Ortak son tarih = verideki en yeni bar (tarih verilirse o gune kadar). Son bari bundan gun (VERI_BAYAT) is gunu
    eski olan hisse bayat. Bayat orani VERI_BAYAT_UST'u asarsa toplu guncelleme sorunudur (delist degil): toplu=True,
    cagiran suzgeci uygulamaz (aday listesi topluca silinmesin).
    Donus: (bayat {sembol: son_bar}, sinir Timestamp|None, toplu bool)."""
    veri = veri if veri is not None else VERI
    gun = VERI_BAYAT if gun is None else gun
    son = {}
    for s, df in veri.items():
        try:
            x = df[df.index <= pd.Timestamp(tarih)] if tarih is not None else df
            if len(x): son[s] = x.index[-1]
        except Exception as e: log.debug(f'{s} veri_bayat: {e}')
    if not son: return {}, None, False
    sinir = max(son.values()) - pd.offsets.BDay(gun)
    bayat = {s: t for s, t in son.items() if t < sinir}
    toplu = len(bayat) > VERI_BAYAT_UST * len(son)
    if toplu:
        log.warning(f'D11: {len(bayat)}/{len(son)} hissenin son bari {sinir.date()} oncesi — toplu veri guncelleme sorunu, bayat suzgeci uygulanmadi')
    return bayat, sinir, toplu

# ---------------- D9: UZUN COL + SEKTOR RUZGARI ----------------
def uzun_col_olc(df, tarih=None):
    """Cemal'in buyuk-resim colu. Donus: {'uzun': '12ay'|'6ay'|'', 'bant': %, 'konum': 0-1, 'mum': oran} veya None.
    12ay: UZUN_W bar; 6ay: UZUN_W//2 bar. Pencere sonu = tarih (None -> son bar)."""
    try:
        x = df[df.index <= pd.Timestamp(tarih)] if tarih is not None else df
        C = x.Close.to_numpy(float); H = x.High.to_numpy(float); L = x.Low.to_numpy(float); n = len(C)
        if n < UZUN_W // 2 + 200: return None
        pc = np.roll(C, 1); pc[0] = C[0]
        TR = np.maximum(H - L, np.maximum(np.abs(H - pc), np.abs(L - pc)))
        out = None
        for W, ad in ((UZUN_W, '12ay'), (UZUN_W // 2, '6ay')):
            if n < W + 200: continue
            w = C[n - W:]
            if not np.isfinite(w).all() or np.nanmin(w) <= 0: continue
            hi, lo = np.percentile(w, 95), np.percentile(w, 5)
            bant = hi / lo - 1
            mum = float(np.nanmean(TR[n - W:]) / np.nanmean(w))
            on_l = L[max(0, n - W - 500):n - W]; on_h = H[max(0, n - W - 500):n - W]
            on_l = on_l[np.isfinite(on_l)]; on_h = on_h[np.isfinite(on_h)]
            if len(on_l) < 200: continue
            pmin, pmax = on_l.min(), on_h.max()
            konum = float((np.median(w) - pmin) / (pmax - pmin)) if pmax > pmin else np.nan
            ok = bool(hi / lo <= UZUN_BANT and mum <= UZUN_MUM and np.isfinite(konum) and konum <= UZUN_KONUM)
            if ok:
                return {'uzun': ad, 'bant': round(100 * bant, 1), 'konum': round(konum, 2), 'mum': round(mum, 3)}
            if out is None: out = {'uzun': '', 'bant': round(100 * bant, 1), 'konum': round(konum, 2) if np.isfinite(konum) else np.nan, 'mum': round(mum, 3)}
        return out
    except Exception as e:
        log.debug(f'uzun_col_olc: {e}'); return None

_SEKTOR = None
def sektor_tablosu(yeniden=False):
    """{sembol: alt_sektor}. col_tarayici/SEKTOR_DOSYALAR sirayla; 'alt_bist' varsa o, yoksa 'alt'. Bulunamazsa {}."""
    global _SEKTOR
    if _SEKTOR is not None and not yeniden: return _SEKTOR
    import os
    K = '/content/drive/MyDrive/col_tarayici'
    d = {}
    for ad in SEKTOR_DOSYALAR:
        y = f'{K}/{ad}'
        if not os.path.exists(y): continue
        try:
            t = pd.read_csv(y)
            kol = 'alt_bist' if 'alt_bist' in t.columns else 'alt'
            t = t.dropna(subset=[kol])
            d = {str(r.sembol).upper().strip(): str(getattr(r, kol)) for r in t.itertuples()}
            log.warning(f'D9 sektor dosyasi: {ad} ({len(d)} hisse, sutun {kol})'); break
        except Exception as e: log.warning(f'{ad} okunamadi: {e}')
    if not d: log.warning('D9: sektor dosyasi yok (sektor_BIST.csv / sektor_TR.csv) — ruzgar hesaplanamaz')
    _SEKTOR = d
    return d

_RUZ_BAYAT_UYARI = None   # D10b: ayni bayat listesi her cagrida yeniden basilmasin
def sektor_ruzgar(veri=None, tarih=None):
    """Her hisse icin sektor ruzgari: sepet (hisse haric) RUZ_GERI gunluk getirisi - piyasa medyani.
    Donus: DataFrame index=sembol, sutunlar alt, ruz, sepet, piy, uye, g, ruzgar. Sektoru olmayan / sepeti kucuk hisse: ruz NaN.
    ruzgar (D10a) = ruz >= RUZ_ESIK ve sepet > RUZ_MUTLAK (D9b) — ruzgar karari burada, tek yerde.
    D10b: verisi ortak son tarihten RUZ_BAYAT is gunu eski hisse hesaba girmez; baslangic kapanisi ortak takvim gunu."""
    global _RUZ_BAYAT_UYARI
    veri = veri if veri is not None else VERI
    sek = sektor_tablosu()
    bos = pd.DataFrame(columns=['alt', 'ruz', 'sepet', 'piy', 'uye', 'g', 'ruzgar'])
    kes = {}
    for s, df in veri.items():
        try:
            x = df[df.index <= pd.Timestamp(tarih)] if tarih is not None else df
            if len(x) >= RUZ_GERI + 1: kes[s] = x
        except Exception as e: log.debug(f'{s} ruzgar: {e}')
    if not kes: return bos
    son = max(x.index[-1] for x in kes.values())                        # D10b: ortak son tarih
    sinir = son - pd.offsets.BDay(RUZ_BAYAT)
    bayat = sorted(s for s, x in kes.items() if x.index[-1] < sinir)
    if bayat and tuple(bayat) != _RUZ_BAYAT_UYARI:
        log.warning(f'D10 ruzgar: {len(bayat)} hissenin verisi durmus (son bar < {sinir.date()}), hesaba girmedi: '
                    + ', '.join(bayat[:12]) + (' ...' if len(bayat) > 12 else ''))
    _RUZ_BAYAT_UYARI = tuple(bayat)
    taze = {s: x for s, x in kes.items() if x.index[-1] >= sinir}
    t0 = pd.Series([x.index[-RUZ_GERI - 1] for x in taze.values()]).median()   # D10b: piyasanin RUZ_GERI bar oncesi
    getiri = {}
    for s, x in taze.items():
        try:
            on = x.Close[x.index <= t0]
            if on.empty: continue
            c0, c1 = float(on.iloc[-1]), float(x.Close.iloc[-1])
            if c0 > 0 and np.isfinite(c0) and np.isfinite(c1): getiri[s] = c1 / c0 - 1
        except Exception as e: log.debug(f'{s} ruzgar: {e}')
    g = pd.Series(getiri, dtype=float)
    if g.empty: return bos
    piy = float(g.median())
    alt = pd.Series({s: sek.get(str(s).upper()) for s in g.index})
    R = []
    for s in g.index:
        a = alt.get(s)
        if a is None or (isinstance(a, float) and np.isnan(a)):
            R.append({'sembol': s, 'alt': '', 'ruz': np.nan, 'sepet': np.nan, 'piy': piy, 'uye': 0, 'g': float(g[s])}); continue
        uy = [u for u in alt.index[alt == a] if u != s]
        if len(uy) < RUZ_MIN_UYE:
            R.append({'sembol': s, 'alt': a, 'ruz': np.nan, 'sepet': np.nan, 'piy': piy, 'uye': len(uy), 'g': float(g[s])}); continue
        sep = float(g[uy].mean())
        R.append({'sembol': s, 'alt': a, 'ruz': sep - piy, 'sepet': sep, 'piy': piy, 'uye': len(uy), 'g': float(g[s])})
    out = pd.DataFrame(R).set_index('sembol')
    out['ruzgar'] = (out.ruz >= RUZ_ESIK) & (out.sepet > RUZ_MUTLAK)        # D10a: D9b dahil; NaN -> False
    return out

def ruzgar_listesi(veri=None, n=40, yazdir=True):
    """D9: ruzgarli sektorlerde (ruz >= RUZ_ESIK) UZUN COLDE olan hisseler — col_segment adayi olmasa da.
    Fon suzgeci uygulanir (FON_ELE). Siralama: ruzgar buyukten kucuge, sonra bant dar olan ustte."""
    veri = veri if veri is not None else VERI
    try: rz = sektor_ruzgar(veri)
    except Exception as e:
        log.warning(f'ruzgar hesaplanamadi: {e}'); return pd.DataFrame()
    if rz.empty: return pd.DataFrame()
    ruzgarli = rz[(rz.ruz >= RUZ_ESIK) & (rz.sepet > RUZ_MUTLAK)]            # D9b: sepet de yukseliyor olmali
    az_dusen = rz[(rz.ruz >= RUZ_ESIK) & ~(rz.sepet > RUZ_MUTLAK)]
    R = []; fon_elenen = []
    for s in ruzgarli.index:
        df = veri.get(s)
        if df is None: continue
        u = uzun_col_olc(df)
        if not u or not u['uzun']: continue
        fe = fon_etiket(s)
        if fe and FON_ELE: fon_elenen.append(s); continue
        r = ruzgarli.loc[s]
        R.append({'sembol': s, 'sektor': r.alt, 'ruz%': round(100 * r.ruz, 1), 'sepet%': round(100 * r.sepet, 1), 'uye': int(r.uye),
                  'uzun': u['uzun'], 'bant%': u['bant'], 'konum': u['konum'], 'mum': u['mum'],
                  'fiyat': round(float(df.Close.iloc[-1]), 2), 'fon': (f"{fe[1]:.0f}%" if fe else '')})
    t = pd.DataFrame(R)
    if yazdir:
        piy = float(rz.piy.iloc[0])
        tum = rz[rz.alt != '']
        def _sepet_ozet(alt):                                                  # sepet = tum uyelerin ortalamasi
            uy = tum[tum.alt == alt].g.dropna()
            return float(uy.mean()), uy.sort_values(ascending=False)
        sekt = sorted(ruzgarli.alt.unique(), key=lambda a: -_sepet_ozet(a)[0])
        print(f"\n=== D9 RUZGAR LISTESI — sektor sepeti {RUZ_GERI}g > %{100*RUZ_MUTLAK:.0f} ve piyasadan >= %{100*RUZ_ESIK:.0f} iyi: {len(sekt)} sektor | piyasa medyani %{100*piy:+.1f}")
        for a in sekt:
            m, uy = _sepet_ozet(a)
            ust = (uy > 0).sum()
            print(f"  {a}: sepet %{100*m:+.0f} (piyasa farki %{100*(m-piy):+.0f}) | {ust}/{len(uy)} hisse artida")
            print("     " + ", ".join(f"{h} {100*v:+.0f}" for h, v in uy.items()))
        azs = sorted(az_dusen.alt.unique(), key=lambda a: -_sepet_ozet(a)[0])
        if azs:
            print("  AZ DUSEN (ruzgar degil — sepet eksi, piyasa daha cok dustu): " + ", ".join(f"{a} %{100*_sepet_ozet(a)[0]:+.0f}" for a in azs))
        if t.empty: print("  ruzgarli sektorde uzun colde hisse yok")
        else:
            t = t.sort_values(['ruz%', 'bant%'], ascending=[False, True]).head(n)
            print(f"  uzun colde (dipte, {UZUN_W//2}-{UZUN_W} bar dar bant) {len(R)} hisse:")
            print(t.to_string(index=False))
        if fon_elenen: print("  FON ELENDI: " + ", ".join(fon_elenen))
    return t

def _bant(df, tarih, pencere=10):
    x=df[df.index<=pd.Timestamp(tarih)]
    if len(x)<60: return None
    c=x.Close; m=c.rolling(20).mean(); sd=c.rolling(20).std(ddof=0)
    U=(m+2*sd).to_numpy(float); M=m.to_numpy(float); A=(m-2*sd).to_numpy(float)
    C=x.Close.to_numpy(float); n=len(x); s=slice(n-pencere,n)
    bk=(C[s]-A[s])/np.maximum(U[s]-A[s],1e-9)
    if not np.isfinite(bk).all(): return None
    return {'bant_son':float(bk[-1]),'ortaust':float(((C[s]>=M[s])&(C[s]<=U[s])).mean()),
            'bant_egim':float(np.polyfit(np.arange(pencere),bk,1)[0])}

def _clv(x, r):
    seg=x[(x.index>=pd.Timestamp(r['bas_tarih']))&(x.index<=pd.Timestamp(r['son_tarih']))]
    C,H,L=(seg[c].to_numpy(float) for c in ('Close','High','Low'))
    rng=np.maximum(H-L,1e-12)
    return float((((C-L)-(H-C))/rng).mean())

# ---------------- CARPANLAR (D3: tek yer) ----------------
def doji_carpan(d):  return CARPAN['doji'](d)
def fitil_carpan(f): return CARPAN['fitil'](f)
def dar_carpan(w):   return CARPAN['dar'](w)

def carpanlar_hesapla(olcu, cds_pct=np.nan, borc_oz=np.nan, oz_negatif=0, kural=1):
    """Pozisyon yuzdesi ve kirilimi. olcu = col_segment/col_olc sozlugu (sinyal gunu)
    veya aday CSV satiri (doji/alt_fitil/dar/gecerli_oran alanlari)."""
    def _g(k):
        try: v=float(olcu.get(k, np.nan)) if hasattr(olcu,'get') else float(getattr(olcu,k,np.nan))
        except Exception: v=np.nan
        return v
    doji,fitil,dar,gec = _g('doji'),_g('alt_fitil'),_g('dar'),_g('gecerli_oran')
    c = {'cds':CARPAN['cds'](cds_pct),
         'borc':0.7 if oz_negatif else CARPAN['borc'](borc_oz),
         'doji':CARPAN['doji'](doji),'fitil':CARPAN['fitil'](fitil),
         'dar':CARPAN['dar'](dar),'kural':CARPAN['kural'](kural),'likit':1.0}
    if np.isfinite(gec) and gec < LIKIT_ESIK:            # D1
        c['doji']=1.0; c['fitil']=1.0; c['likit']=LIKIT_CARPAN
    ham = POZISYON_TABAN
    for v in c.values(): ham*=v
    poz = float(min(ham, POZISYON_UST))
    return poz, c

# ---------------- OLCUM ----------------
def col_olc(df, tarih=None):
    x=df[df.index<=pd.Timestamp(tarih)] if tarih is not None else df
    r=col_dip(x) if SEGMENT_MOD=='dip' else col_segment(x)   # D12
    if not r or r['uzunluk']<MIN_UZ or r['yukseklik_atr']>MAX_YUK: return None
    if not r.get('atr_ref') or r['atr_ref']<=0: return None
    b=_bant(df, tarih if tarih is not None else df.index[-1])
    if not b: return None
    clv=_clv(x,r); C=x.Close.to_numpy(float)
    onc = (C[-1]/C[-250]-1)*100 if len(C)>=250 else np.nan
    gecer = bool(clv>=E_CLV and b['bant_son']>=E_BS and b['ortaust']>=E_OU)
    if BIST_MODU and gecer: gecer = bool(np.isfinite(onc) and onc < E_ONC)
    return {**r, **b, 'clv':round(clv,3),'onceki_250': round(onc,1) if np.isfinite(onc) else np.nan,'GECER': gecer}

def bugun_liste(veri=None, n=40, hepsi=False):
    veri=veri if veri is not None else VERI
    R=[]; FON_ELENEN=[]
    try: RZ = sektor_ruzgar(veri)                      # D9
    except Exception as e: log.warning(f'D9 ruzgar: {e}'); RZ = pd.DataFrame()
    try: BAYAT, _, _btop = veri_bayat(veri)            # D11
    except Exception as e: log.warning(f'D11 veri_bayat: {e}'); BAYAT, _btop = {}, False
    if _btop: BAYAT = {}                              # D11: toplu veri sorunu -> suzgec yok (uyari veri_bayat'ta)
    BS = ("  VERI DURDU (" + f"{VERI_BAYAT}+ is gunu veri yok, aday sayilmadi): " + ", ".join(f"{h} (son {t.date()})" for h, t in sorted(BAYAT.items())[:15])
          + (" ..." if len(BAYAT) > 15 else "")) if BAYAT else ""
    for s,df in veri.items():
        if len(df)<250: continue
        if s in BAYAT: continue                        # D11: verisi durmus hisse aday sayilmaz
        try: o=col_olc(df)
        except Exception as e: log.debug(f'{s} col_olc: {e}'); o=None
        if not o: continue
        fe = fon_etiket(s)
        if fe and FON_ELE:
            FON_ELENEN.append((s, fe[0], fe[1])); continue
        if hepsi or o['GECER']:
            u = uzun_col_olc(df) or {}                   # D9
            rz = float(RZ.ruz.get(s, np.nan)) if (not RZ.empty and s in RZ.index) else np.nan
            rv = bool(RZ.ruzgar.get(s, False)) if (not RZ.empty and s in RZ.index and 'ruzgar' in RZ.columns) else False   # D10a
            R.append({'sembol':s,'fon':(f"{fe[1]:.0f}%" if fe else ''),'uzun':u.get('uzun',''),'ruz':(round(100*rz,0) if np.isfinite(rz) else np.nan),'ruzgar':('RUZGAR' if rv else ''),'bas':o['bas_tarih'],'bar':o['uzunluk'],'doji':o['doji'],'fitil':o['alt_fitil'],'dar':o['dar'],
                      'gecerli':o['gecerli_oran'],'clv':o['clv'],'bant':round(o['bant_son'],2),'ortaust':round(o['ortaust'],2),
                      'yuk':o['yukseklik_atr'],'taban':o['taban'],'tavan':o['tavan'],'fiyat':round(float(df.Close.iloc[-1]),2),'GECER':o['GECER']})
    t=pd.DataFrame(R)
    if t.empty:
        print("aday yok" + (f" | FON ELENDI: {', '.join(h for h,_,_ in FON_ELENEN)}" if FON_ELENEN else ""))
        if BS: print(BS)                                 # D11
        if RUZGAR_LISTE: ruzgar_listesi(veri)            # D9
        return t
    t=t.sort_values(['GECER','doji'],ascending=[False,False]).head(n)
    pd.set_option('display.width',230); pd.set_option('display.max_columns',None)
    print(f"{len(veri)} hisseden {len(R)} aday ({int(t.GECER.sum())} kurali geciyor) — yuksek doji ustte")
    if FON_ELENEN: print("  FON ELENDI (tasfiye fonu payi >= %" + f"{FON_ESIK:.0f}): " + ", ".join(f"{h} ({k.split()[0].title()} %{p:.0f})" for h,k,p in FON_ELENEN))
    if BS: print(BS)                                     # D11
    print()
    print(t.to_string(index=False))
    if RUZGAR_LISTE: ruzgar_listesi(veri)                # D9
    return t

def tara(tarihler, ileri=60, veri=None):
    veri=veri if veri is not None else VERI
    R=[]
    for i,T in enumerate(tarihler,1):
        Ts=pd.Timestamp(T); say=0
        for s,df in veri.items():
            x=df[df.index<=Ts]
            if len(x)<250: continue
            try: o=col_olc(df,T)
            except Exception as e: log.debug(f'{s}@{T} col_olc: {e}'); o=None
            if not o: continue
            il=df[df.index>Ts].head(ileri)
            if len(il)<20: continue
            p0=float(x.Close.iloc[-1]); yon='YOK'
            for c in il.Close.to_numpy(float):
                if c>o['tavan']*AL_PAY: yon='YUKARI'; break
                if c<o['taban']: yon='ASAGI'; break
            if yon=='YOK': continue
            R.append({'sembol':s,'tarih':T,'yon':yon,'clv':o['clv'],'bant_son':o['bant_son'],'ortaust':o['ortaust'],
                      'uzunluk':o['uzunluk'],'doji':o['doji'],'alt_fitil':o['alt_fitil'],'dar':o['dar'],'gecerli_oran':o['gecerli_oran'],
                      'onceki_250':o.get('onceki_250'),'GECER':o['GECER'],
                      'getiri':(float(il.Close.iloc[-1])/p0-1)*100}); say+=1
        print(f"  {i}/{len(tarihler)} {T} -> {say} (toplam {len(R)})")
    return pd.DataFrame(R)

def bek(v):
    """Gercek beklenti: kazanma orani x ort kazanc + kaybetme orani x ort kayip (ORTALAMA, medyan degil)."""
    v=pd.Series(v,dtype=float).dropna()
    if not len(v): return np.nan
    kz=v[v>0].mean() if (v>0).any() else 0.0; ky=v[v<=0].mean() if (v<=0).any() else 0.0
    return float((v>0).mean()*kz+(v<=0).mean()*ky)

def rapor(d, ad="RAPOR"):
    try: from scipy.stats import binomtest
    except Exception: binomtest=None
    d=d.copy(); d['up']=(d.yon=='YUKARI').astype(int); p0=d.up.mean()
    z=d[d.GECER]
    print(f"\n{ad} TABAN n={len(d)} yukari %{100*p0:.1f} getiri medyan %{d.getiri.median():+.1f} beklenti %{bek(d.getiri):+.1f}")
    if len(z)<20: print(f"{ad} KURAL: yetersiz (n={len(z)})"); return
    k=int(z.up.sum()); n=len(z)
    p=binomtest(k,n,p0,alternative='greater').pvalue if binomtest else np.nan
    print(f"{ad} KURAL n={n} yukari %{100*k/n:.1f} getiri medyan %{z.getiri.median():+.1f} beklenti %{bek(z.getiri):+.1f} p={p:.6f}")

def portfoy_simulasyon(sec, veri=None, hedef=None, ufuk=250, maliyet=0.4, ma=20):
    """Islem basi trail P&L (sinyal gunu kapanisindan). Yillik rakam D5 ile kaldirildi:
    yillik getiri / drawdown icin DENETIM.portfoy() kullan."""
    veri = veri if veri is not None else VERI
    hedef = HEDEF if hedef is None else hedef
    R=[]
    for r in sec.itertuples():
        df=veri.get(r.sembol)
        if df is None: continue
        T=pd.Timestamp(r.tarih); x=df[df.index<=T]; il=df[df.index>T].head(ufuk)
        if len(il)<30 or len(x)<ma: continue
        p0=float(x.Close.iloc[-1])
        if p0<=0: continue
        H=il.High.to_numpy(float); C=il.Close.to_numpy(float)
        s20=pd.concat([x.Close,il.Close]).rolling(ma).mean().to_numpy(float)[-len(il):]
        m=H>=p0*(1+hedef/100)
        if m.any():
            jh=int(np.argmax(m)); alt=np.where(C[jh+1:]<s20[jh+1:])[0]
            jt=int(alt[0])+jh+1 if len(alt) else len(C)-1
            R.append({'sonuc':(C[jt]/p0-1)*100,'bar':jt+1})
        else: R.append({'sonuc':(float(C[-1])/p0-1)*100,'bar':len(C)})
    w=pd.DataFrame(R)
    if w.empty: print("kayit yok"); return w
    v=w.sonuc; kaz=(v>0).mean(); b=bek(v); net=b-maliyet; gun=float(w.bar.median())
    ay=len(sec)/22.0; ez=ay*(gun/21.0)
    print(f"\n  TRAIL (hedef %{hedef} -> SMA{ma})  n={len(w)}, ayda {ay:.1f} sinyal")
    print(f"    kazanan %{100*kaz:.0f} | ort kazanc %{v[v>0].mean():+.1f} | ort kayip %{(v[v<=0].mean() if (v<=0).any() else 0):+.1f}")
    print(f"    islem basi %{b:+.1f} (net %{net:+.1f}) | medyan sure {gun:.0f} bar | es zamanli ~{ez:.0f} pozisyon")
    print(f"    (yillik/drawdown: DENETIM.portfoy)")
    return w

# ---------------- CDS ----------------
CDS_DOSYA='cds_2022.csv'
def cds_yukle(dosya=None):
    import os
    y=f"/content/drive/MyDrive/col_tarayici/{dosya or CDS_DOSYA}"
    if not os.path.exists(y): print("  [cds] dosya yok:",y); return None
    try:
        c=pd.read_csv(y,parse_dates=['date']).set_index('date').price.sort_index()
        return c[~c.index.duplicated()]
    except Exception as e:
        log.warning(f'cds_yukle: {e}'); return None

def cds_rejim(c=None, tarih=None):
    c=c if c is not None else cds_yukle()
    if c is None or len(c)<120: return None
    cc=c[c.index<=pd.Timestamp(tarih)] if tarih is not None else c
    if len(cc)<120: return None
    pct=float((cc.tail(250)<cc.iloc[-1]).mean())
    carpan=CARPAN['cds'](pct)
    etiket='DUSUK RISK (rahat piyasa) -> YARIM pozisyon' if pct<0.3 else ('YUKSEK RISK (korku) -> 1.5x pozisyon' if pct>=0.6 else 'ORTA -> normal pozisyon')
    yas=(pd.Timestamp.now().normalize()-cc.index[-1]).days
    return {'cds':round(float(cc.iloc[-1]),1),'tarih':str(cc.index[-1].date()),'pct250':round(pct,2),
            'carpan':carpan,'etiket':etiket,'veri_yasi_gun':int(yas),'pozisyon_yuzde':round(POZISYON_TABAN*carpan,1),
            'cds_20d':round(float(cc.iloc[-1]-cc.iloc[-21]),1) if len(cc)>21 else np.nan}

def endeks_yukle(sembol='XU100.IS', period='10y'):
    import yfinance as yf
    xu=yf.download(sembol, period=period, progress=False, auto_adjust=False)
    if isinstance(xu.columns, pd.MultiIndex): xu.columns=xu.columns.get_level_values(0)
    if xu.index.tz is not None: xu.index=xu.index.tz_localize(None)
    xu.index=xu.index.normalize()
    print(f"{sembol}: {len(xu)} bar  {xu.index[0].date()} -> {xu.index[-1].date()}")
    return xu

print(f"[ok] COL SISTEMI v2  (2026-10-20 D12: col tespiti = {'DIP COLU (bolge + dip + yeni dip yok + imza >= ' + str(IMZA_MIN) + '/4)' if SEGMENT_MOD=='dip' else 'ESKI col_segment (D7)'} | D11: verisi durmus hisse aday olmaz, > {VERI_BAYAT} is gunu | D10: ruzgar etiketi D9b dahil + tarih hizasi, bayat > {RUZ_BAYAT} is gunu | 2026-10-18 D9: uzun col {UZUN_W} bar + sektor ruzgari >= %{100*RUZ_ESIK:.0f}, sepet > %{100*RUZ_MUTLAK:.0f} (D9b) | 2026-10-17 D7: kucuk mum = {MUM_OLCU} | D8: fon suzgeci {'ACIK' if FON_ELE else 'KAPALI'}, {len(fon_defteri())} hisse kayitli; 2026-09-18: gecerli bar, dar hafta, tek carpan)")
print(f"  esikler: clv>={E_CLV} bant_son>={E_BS} ortaust>={E_OU} | segment>={MIN_UZ} bar, yuk<={MAX_YUK} ATR, yerel={YEREL} | AL_PAY={AL_PAY}")
print(f"  CIKIS={CIKIS} HEDEF=%{HEDEF} | pozisyon %{POZISYON_TABAN} x CDS x BORC x DOJI x FITIL x DAR x KURAL (ust %{POZISYON_UST})")
_r=cds_rejim()
if _r:
    print(f"  CDS {_r['cds']} bp ({_r['tarih']}, {_r['veri_yasi_gun']} gun once) | yuzdelik {_r['pct250']} | {_r['etiket']}")
    if _r['veri_yasi_gun']>30: print("  [!] CDS verisi eski — investing.com'dan guncelle: cds_2022.csv")
