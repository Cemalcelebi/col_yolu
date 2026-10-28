# =====================================================================
#  FON_IZI — tasfiye fonlarinin topladigi hisselerin yukselis oncesi/sirasi izi   (2026-10-23, v1.2)
#
#  CEMAL (22 Eki): "Fonlar Eylul'e kadar onca alis yapmis, hisseler yuzde bin yukselmis; o para girisi nasil bir iz birakti?
#    Benim dusuncem: balina girisi zamanina denk gelen bolgede kucuk mum ve ufak ufak yukari yuvarlanma. TEHOL, TERA, PASEU,
#    HEDEF... bunlara bak, bu iz nedir? Bu bize buyuk bir ders verir."
#  VAKA LISTESI (FON_HISSE): tasfiye fonlarinin fiili dolasimda en buyuk paya sahip oldugu hisseler (borsaningundemi / hisse.net
#    18 Eyl 2026: TEHOL %77,7 ANELE %68,1 TRHOL %60,1 OZATD %57,5 PEKGY %54,7 IEYHO %43,1 DSTKF %34,5 ISKPL %26,4 SELEC %20,6
#    BIGEN %20,2) + COL_v1 FON_BILINEN (KTLEV GUNDG PASEU ODINE HEDEF TERA IZFAS LIDER) + taban serisine giren ALKLC UFUK PRZMA
#    BINBN DURDO. Cemal'in "Ata" dedigi hisse (ATATR?) veride yok.
#  VERI: BIST fiyatlari ham (auto_adjust=False). K1, BIST'te gunluk sinirin (2020-03 sonrasi %10, oncesi %20) otesindeki
#    sicramalari bolunme/bedelsiz sayar ve geriye dogru carpanla duzeltir (hacim ters carpanla).
#  FAZLAR (vaka): dip = tepe oncesi 900 gundeki en dusuk kapanis; ONCE = dipten onceki 120 bar; ERKEN = dip -> fiyatin ilk 2 kati;
#    KOSU = 2 kat -> tepe (15 Eyl 2026 oncesi en yuksek kapanis); COKUS = tepe -> bugun.
#  IZ OLCULERI (son W=60 bar, gercek zamanli): g = 60 bar getiri; taban = gunluk <= -%9,5 gun sayisi; tavan = >= +%9,5;
#    dd = pencere icindeki en derin geri cekilme; mk = pencere medyan mum boyu (H-L / onceki kapanis) / AYNI hissenin onceki
#    250 bar medyani (k < 1 = mumlar kendi gecmisine gore kuculdu); verim = net log getiri / gunluk log hareketlerin toplami;
#    tlk = son 60 bar TL hacim medyani / onceki 60 bar; r2 = son 120 barda log fiyatin dogruya uyumu (grafikteki duz cizgi kosu).
#  EVREN TESTI: olay = 60 barda +%30..+%100 yukselmis hisse (ayni hissede 60 bar icinde bir kez); IZ varyantlari bu olaylarin alt
#    kumesi, TABAN = ayni yukselisin izi tasimayan geri kalani. Sonuc: 250 bar icinde once 2 kat mi (High) once -%30 mu (Low);
#    250 bar sonraki getiri; 250 bardaki en yuksek / giris. Iz = 4 dilimde (BIST/ABD x 2016-21/2022-26) kat >= 1,3.
#  v1.1 (23 Eki) HACIM ESLIGI. CEMAL: "Hacmine eslik edenlere ayrica bak; balina girisine denk gelen bolgede kucuk mum ve ufak ufak
#    yukari yuvarlanma olur, o bolgeleri net goremedik." SESSIZ YUVARLANMA bolgesi (Z0, son hW=20 bar): +%5..+%30 yukselis, medyan
#    mum hissenin kendi 250 bar normalinin <= 0,85'i, verim >= 0,3, taban gunu yok, geri cekilme >= -%10. Bolge icindeki hacim:
#    hk = hacim medyani / kendi 250 bar normali; udvr = yukselis gunu hacmi / dusus gunu hacmi; dh = dusus gunu ort. hacmi / yukselis
#    gunu ort. hacmi; emilim = hk / mum kucuklugu (caba-sonuc: hacim buyuk, mum kucuk); emilim_gun = hacim >= 1,5 normal VE mum <= 0,8
#    normal olan gun sayisi; vcv = hacim degiskenlik katsayisi. K3b: fon hisselerinin dip->tepe donemindeki Z0 bolgeleri ile diger
#    BIST hisselerinin 2024-26 Z0 bolgeleri karsilastirilir. K4b: evrende Z0 olaylari (ayni hissede 20 bar icinde bir kez), hacim
#    varyantlari Z0'in hacim izi tasimayan kismina karsi; sonuc 250 barda once 2 kat / -%30 ve 60 barda once +%20 / -%10.
#  v1.2 (23 Eki) GOSTERGE BATARYASI. CEMAL: "Iz yok diyorsun ama hisseler alindi; yalniz mum ve hacme bakma, her gostergeye
#    bak: ters uyumsuzluk, Fibonacci, hepsi." K6: 40+ gosterge (RSI, Stokastik, Williams %R, CCI, MFI, CMF, OBV, A/D, MACD, ADX/DI,
#    Aroon, Bollinger %B + genislik, Keltner sikismasi, Ichimoku, SMA50/200, ROC, ATR%, Force, Ulcer, Fibonacci konum/geri cekilme)
#    + pivot tabanli UYUMSUZLUK (duz/gizli boga, ayi; RSI, MACD hist, OBV, MFI, CMF; pivot p+-k barin en dusugu/yuksegi, sinyal
#    pivotun dogrulandigi p+k gununde -> gelecege bakmaz). K7 BLOK HACIM: hacim >= 20x onceki 20 gun medyani (OZATD 14 May 2026:
#    fonlar tek gunde 13,6 mn lot, komsu kilitli tavan gunlerinde ~0,1 mn; onceki olculer kilitli O=H=L=C gunlerini disliyordu).
#    K8 KAP OLAYLARI (BIST, 2017-26, kap_ozet konu kodlari): VBTS/BISTECH tedbiri, borsada islem goren tipe donusum, toptan alis
#    satis, pay alim satim bildirimi, devre kesici, olagan disi fiyat, SPK islem yasagi, fiili dolasim degisikligi, piyasa yapicilik,
#    soylenti aciklamasi. Saat 18:00 sonrasi bildirim ertesi islem gunune sayilir. K6a fon hisselerinde faz basina 100 gunde sinyal
#    sikligi vs diger BIST (2024-26); K6b evren: her sinyal (ayni hissede 20 bar icinde bir kez) vs her 5. gun tabani; sonuc 60 bar
#    once +%20/-%10 (k20), 250 bar once 2 kat/-%30 (x2), 60 bar once -%20/+%20 (dus). Iz = 4 dilimde kat >= 1,3 (KAP yalniz BIST: 2 dilim).
#  v1.4 (23 Eki) BAGIMSIZ DENETIM DUZELTMELERI: (1) bolunme duzeltmesinde BIST marji 13.03.2020'ye kadar %20 (eskiden 01.03.2020;
#    Mart 2020 cokusunun 537 gunu bolunme sanilip siliniyordu); 13.03.2020-28.02.2021 gecisinde %10,5-21 sicrama yalniz KAP bedelsiz
#    kaydi yakininda bolunme sayilir. (2) asagi sinyallerde ESLI TABAN (ayni gun kosulu, sinyalsiz): blok_taban <-> bloksuz taban gunu,
#    kap_olagan_disi <-> 20 barda >= +%40, kap_vbts_tedbir <-> tavan gunu; kat_*_esli sutunlari. (3) _fi_ilk ayni barda iki esik -> asagi.
#    ABD'de 'tavan/taban' = +-%9,5 gun (gunluk sinir yok).
#  v1.5 (24 Eki) FAZ 1 — FON ISLEM DEFTERI. CEMAL: "Hangi gun kac lot alinmis, dolasimdaki lot, hacim; iz bulmak zorundasin."
#    K9: KAP 'Portfoy Dagilim Raporu' listesi konu suzgeciyle (2022-12 -> bugun, 45.740 rapor; tasfiyedeki fonlarin haftalik
#    raporlari ayrilir), BIST hissesi tasiyabilen fonlarin son (duzeltilmis) raporlari indirilir ve metne cevrilir. Ayristirici sirasi:
#    SPK sablonu (III-, Turk/ABD sayi), Atlas ailesi (3-), genel ISIN ayristiricisi (banka portfoy sirketleri); her rapor kendi hisse
#    grubu toplamiyla mutabakattan gecer (tutmayan kullanilmaz). Nitelikli yatirimciya satilan fonlar rapor vermez (muaf).
#    K10: fon girisi / cikisi / ilk giris / coklu giris / buyuk giris / toplu artis / tasfiye sirketi / fonlarin sermaye payi %5-%10'u
#    ilk asti (yogun5/10); bilgi ani = KAP yayini, giris = ertesi islem gunu acilisi, cikis = uretim (T10 maliyet + trail);
#    taban her 5. gun, esli taban ayni ay x 60 gun momentum besligi x likidite uclusu; 30 slot vs ayni sayida rastgele.
#    K11: fon hisselerinde ay ay raporlu tasfiye fonu pozisyonu (bolunmeden arindirilmis lot, sermaye payi, faz) ve islem dokumu
#    veren sirketlerde gun gun alim/satim lotu ve borsa hacmindeki payi; vaka PDF'i.
#  KURAL_MOTORU: K1 veri+duzeltme  K2 gunluk/pencere olculeri  K3 vaka fazlari  K4 evren olaylari + ozet  K5 rapor
#                K6 gosterge/uyumsuzluk/Fibonacci  K7 blok hacim  K8 KAP olaylari (v1.2: fon_izi_gosterge)
#                K9 KAP fon raporlari  K10 fon girisi testi  K11 fon defteri  K12 ders PDF'i (v1.5: fon_izi_k10)
#  Calistirma: FI_VERI_BIST=... FI_VERI_ABD=... python FON_IZI.py   (v1.2: ... FI_KAP=<kap_ozet klasoru> python FON_IZI.py gosterge)
#    v1.5: FI_KAPFON=<klasor> python FON_IZI.py k9indir  (~5,5 saat, KAP hiz siniri; kaldigi yerden devam eder)
#          FI_KAPFON=... FI_ISY=<Is Yatirim temel degerler HTML> FI_KAP=... FI_VERI_BIST=... python FON_IZI.py k10  (~11 dk)
#          Artirimli: k9indir yalniz yeni raporlari indirir, k10 yalniz yeni raporlari ayristirir (k9_*.csv.gz tablolarina ekler).
#          Paket: FI_KAPFON=... python FON_IZI.py k9paket <klasor>  /  k9ac <klasor> (repo 'kapfon-veri' dali; sha256 dogrulamali)
#  Cikti: arastirma_cikti/fon_izi/
# =====================================================================
from __future__ import annotations

import logging
import os
import pickle
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_CK_ONCE_FI = {k: id(v) for k, v in globals().items()}

FI_SURUM = "FON_IZI v1.31 (2026-10-28, K42 bilinen etkiler kıyası; denetim düzeltmeleri: r60 çıkış ffill, K39 küçükler, K40 saat barı, AVR Kur; K41 klasikler + rüzgâr sürekliliği + ABD çöl süzgeci + K40 kalıntı; K40 saat farkı; K39 ABD öncü Avrupa takip; karar pazarları ABD + AVR, K38 en yakın adaylar 3 pazarda + K38-B şekiller (çöl, ikili dip, ters OBO, uyumsuzluk); K37 büyükler önce küçükler sonra; K36 rüzgârın sebebi; K35 rüzgâr batanları ayırır mı + K35-C patlayanların arkasında rüzgâr; K34 batanlar dahil nakit tükenmesi testi; K33 sıçrayan hisse profili + K33-B nakit tükenmesi grubunda iyi çıkanların izi; K32 sade portföy ölçümü; K31 analist izleri (içeriden satış, seyrelme, nakit tükenmesi, açığa satış); K30 ABD içeriden alım (SEC Form 4); K29 risk süzgeci + portföy; K28 bilanço sürprizi (PEAD) BIST + ABD; K27 içeriden alım + yeni ölçüt (eşli fark, güven aralığı, portföy); işlenmiş veri paketi (islenmis-veri dalı); K26 ortak parmak izi (MANAS x2, BINBN, KZBGY); kör set v4 sonucu + ders 10c; v4 kutu + alış mumu + geri zum; v3 net mum grafiği; K25 çöl = büyük alıcının izi mi; K24 iki evre kuralı; K23 bölge parmak izi + benzer bölgeler; K22 çöl tavanında bekleyen alış emri; K21 sağ ayak mum mum vs aynı gün bütün hisseler + en sıkı çöl; K19 sistem rastgeleden iyi mi; K18 Cemal'in vakaları: ortak iz; denetim v1.6: fi_duzelt yukari/piyasa gunu, K13 pencere, esli kutu gecmis bilgi, K10 o an bilinen; yukselis izi + hacim esligi + gosterge/uyumsuzluk/Fibonacci/blok hacim/KAP; denetim duzeltmeleri; KAP fon raporlari: defter + fon girisi testi)"
filog = logging.getLogger("col.fon_izi")
if not filog.handlers:
    _fi_h = logging.StreamHandler(sys.stderr)
    _fi_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s fon_izi: %(message)s", "%H:%M:%S"))
    filog.addHandler(_fi_h)
    filog.setLevel(logging.INFO)
    filog.propagate = False

FON_HISSE = ["TEHOL", "ANELE", "TRHOL", "OZATD", "PEKGY", "IEYHO", "DSTKF", "ISKPL", "SELEC", "BIGEN", "KTLEV", "GUNDG",
             "PASEU", "ODINE", "HEDEF", "TERA", "IZFAS", "LIDER", "ALKLC", "UFUK", "PRZMA", "BINBN", "DURDO"]


@dataclass
class FIAyar:
    W: int = 60
    normal: int = 250
    normal_min: int = 120
    limit_tarih: str = "2020-03-13"     # v1.4: Borsa Istanbul marji %20 -> %10, 13.03.2020 (duyuru 12.03.2020)
    limit_yeni: float = 0.105           # %10 donemi: otesi sicrama = bolunme/bedelsiz
    limit_eski: float = 0.21            # %20 donemi
    limit_gecis_bit: str = "2021-03-01"  # v1.4: 13.03.2020-28.02.2021 veride ayda 50-90 gercek %10,5-19,5 hareket var; bu donemde
    #                                     %10,5-21 arasi sicrama yalniz KAP bedelsiz kaydi varsa bolunme sayilir
    bedelsiz_once: int = 180            # KAP bedelsiz bildiriminden sonra en fazla bu kadar takvim gunu icindeki sicrama
    bedelsiz_sonra: int = 5             # bildirimden en fazla bu kadar gun once gelen sicrama (gec bildirim)
    sinir_gun: float = 0.095        # tavan/taban gunu esigi (her iki pazarda sabit)
    kriz_tarih: str = "2026-09-15"  # fon tasfiye cokusu oncesi tepe arama siniri
    dip_gun: int = 900
    g_alt: float = 0.30
    g_ust: float = 1.00
    ufuk: int = 250
    hedef_kat: float = 2.0
    zarar: float = 0.30
    tekrar: int = 60
    donem_siniri: str = "2022-01-01"
    # v1.1 hacim esligi
    hW: int = 20
    z0_g: Tuple[float, float] = (0.05, 0.30)
    z0_mk: float = 0.85
    z0_verim: float = 0.30
    z0_dd: float = -0.10
    hacim_tekrar: int = 20
    hacim_bas: str = "2024-01-01"   # K3b diger hisseler karsilastirma donemi baslangici (bitis kriz_tarih)
    # v1.2 gosterge bataryasi
    piv_k: int = 5                  # uyumsuzluk pivotu: p-k..p+k araliginin en dusugu/yuksegi; sinyal p+k gunu
    piv_ara: int = 60               # iki pivot arasi en fazla bar
    g_tekrar: int = 20              # ayni hissede ayni sinyal 20 bar icinde bir kez
    ornek_adim: int = 5             # taban: her 5. gun
    blok_kat: float = 20.0          # blok hacim: onceki 20 gun medyaninin 20 kati
    once_bar: int = 120             # fon vakasi ONCE fazi (dipten onceki bar)
    kap: str = os.environ.get("FI_KAP", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/kap_ozet")
    # v1.3 fon islem defteri (KAP portfoy dagilim raporlari)
    kapfon: str = os.environ.get("FI_KAPFON", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/kapfon")
    kapfon_bas: str = "2023-01-01"
    kapfon_bit: str = os.environ.get("FI_KAPFON_BIT", str(pd.Timestamp.today().date()))
    kapfon_konu: str = "8aca490d502e34b801502e380044002b"   # KAP konu OID: 'Portfoy Dagilim Raporu' (v1.5: konu suzgeci, 2000 sinirsiz)
    kapfon_bekle: float = 0.3       # KAP'a nezaket beklemesi (sn, istek basina)
    kapfon_is: int = 3              # paralel indirme is parcacigi
    isy: str = os.environ.get("FI_ISY", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/isy/temel_degerler.html")   # fiili dolasim
    veri: Dict[str, str] = field(default_factory=lambda: {
        "BIST": os.environ.get("FI_VERI_BIST", "/content/drive/MyDrive/col_tarayici/veri_1d_turkey.pkl"),
        "ABD": os.environ.get("FI_VERI_ABD", "/content/drive/MyDrive/col_tarayici/veri_1d_america.pkl"),
    })
    cikti: str = "arastirma_cikti/fon_izi"


# ---------------------------------------------------------------- K1 veri
def fi_duzelt(d: pd.DataFrame, A: FIAyar, bedelsiz: Optional[pd.DatetimeIndex] = None,
              piyasa: Optional[Dict[str, set]] = None) -> Tuple[pd.DataFrame, int]:
    """BIST ham fiyat: gunluk siniri asan sicramalari geriye dogru carpanla duzeltir. Donus: (duzeltilmis, sicrama sayisi).
    v1.4: sinir 13.03.2020'ye kadar %20 (eskiden 01.03.2020 aliniyordu; Mart 2020 cokusunun 537 gunu bolunme sanilip siliniyordu).
    Gecis donemi (13.03.2020-28.02.2021): %10,5-21 sicrama ancak `bedelsiz` (KAP bedelsiz bildirim tarihleri) yakininda bolunme sayilir;
    kayit yoksa gercek hareket kabul edilir.
    v1.6 (denetim 24 Eki): (a) bolunme/bedelsiz fiyati DUSURUR; +%30'a kadar yukari sicrama gercek harekettir (tavan gunu, Yahoo
    kapanisi ile baz fiyat farki); eskiden BIST'te 1.068 gercek tavan gunu silinip gecmis carpanla oynatiliyordu. (b) `piyasa`
    {'yukari': gunler, 'asagi': gunler}: ayni gun hisselerin >= %2'si ayni yonde siniri astiysa (15.02.2023 deprem kapanisi sonrasi
    acilis 375 hisse, 12.03.2020 bayat bar 99 hisse, bayram arifesi) o gunun sicramasi bolunme sayilmaz."""
    d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float).copy()
    oran = d.Close / d.Close.shift()
    lim = np.where(d.index >= pd.Timestamp(A.limit_tarih), A.limit_yeni, A.limit_eski)
    kir = (oran - 1).abs() > lim
    kir &= ~((oran > 1) & (oran < 1.30))
    if piyasa:
        kir &= ~((oran > 1) & d.index.isin(list(piyasa.get("yukari", ()))))
        kir &= ~((oran < 1) & d.index.isin(list(piyasa.get("asagi", ()))))
    gecis = (d.index >= pd.Timestamp(A.limit_tarih)) & (d.index < pd.Timestamp(A.limit_gecis_bit)) & ((oran - 1).abs() <= A.limit_eski)
    if gecis.any():
        kanit = np.zeros(len(d), bool)
        if bedelsiz is not None and len(bedelsiz):
            b = np.sort(pd.DatetimeIndex(bedelsiz).values)
            ix = d.index.values
            j = np.searchsorted(b, ix, side="right") - 1            # son bildirim (gun <= t)
            once = (j >= 0) & ((ix - b[np.clip(j, 0, None)]) <= np.timedelta64(A.bedelsiz_once, "D"))
            k = np.searchsorted(b, ix, side="left")                 # sonraki bildirim (gun >= t)
            sonra = (k < len(b)) & ((b[np.clip(k, None, len(b) - 1)] - ix) <= np.timedelta64(A.bedelsiz_sonra, "D"))
            kanit = once | sonra
        kir = kir & (~gecis | kanit)
    carp = oran.where(kir, 1.0)[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
    for c in ("Open", "High", "Low", "Close"):
        d[c] = d[c] * carp
    d["Volume"] = d.Volume / carp
    return d, int(kir.sum())


def fi_piyasa_sicrama(V: Dict[str, pd.DataFrame], A: FIAyar, oran_esik: float = 0.02) -> Dict[str, set]:
    """v1.6: piyasa geneli sicrama gunleri. Hisselerin >= oran_esik'i ayni gun ayni yonde gunluk siniri astiysa (kapanis / onceki
    kapanis) bu bir piyasa olayidir (kapanis sonrasi acilis, bayat bar), bolunme degil. Donus {'yukari': set, 'asagi': set}."""
    C = pd.DataFrame({s: d.Close for s, d in V.items() if "Close" in d}).sort_index()
    C = C.where(C > 0)
    O = C / C.ffill().shift()
    lim = pd.Series(np.where(C.index >= pd.Timestamp(A.limit_tarih), A.limit_yeni, A.limit_eski), index=C.index)
    n = C.notna().sum(axis=1).clip(lower=1)
    yuk = O.sub(1).gt(lim, axis=0).sum(axis=1) / n
    asa = O.sub(1).lt(-lim, axis=0).sum(axis=1) / n
    out = {"yukari": set(C.index[yuk >= oran_esik]), "asagi": set(C.index[asa >= oran_esik])}
    filog.info("piyasa geneli sicrama gunleri: yukari %d, asagi %d", len(out["yukari"]), len(out["asagi"]))
    return out


def fi_k1_veri(yol: str, pazar: str, A: FIAyar) -> Dict[str, pd.DataFrame]:
    if not os.path.exists(yol):
        raise FileNotFoundError(f"veri yok: {yol}")
    with open(yol, "rb") as f:
        V = pickle.load(f)
    if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
        V = V["veri"]
    bdz: Dict[str, pd.DatetimeIndex] = {}
    if pazar == "BIST":
        try:
            bdz = fi_bedelsiz_tarihleri(A)
        except Exception as ex:
            filog.warning("KAP bedelsiz kaydi okunamadi (%s); gecis donemindeki %%10,5-21 sicramalar gercek hareket sayilacak", ex)
    piy = fi_piyasa_sicrama(V, A) if pazar == "BIST" else {}
    out = {}
    for s, d in V.items():
        try:
            if "Volume" not in d.columns:
                continue
            d = d.dropna(subset=["Open", "High", "Low", "Close"])
            d = d[(d.High >= d.Low) & (d.Close > 0)].sort_index()
            if pazar == "BIST":
                d, _ = fi_duzelt(d, A, bdz.get(str(s)), piy)
            else:
                d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float)
            if len(d) >= 150:
                out[str(s)] = d
        except Exception as ex:  # tek hisse bozuksa digerleri devam eder
            filog.warning("%s atlandi: %s", s, ex)
    filog.info("%s %s: %d hisse", pazar, yol, len(out))
    return out


def _fi_kap_dosyalar(A: FIAyar) -> List[str]:
    yol = A.kap
    if os.path.isdir(yol):
        return sorted(os.path.join(yol, f) for f in os.listdir(yol) if f.startswith("kap_20") and f.endswith(".csv.gz"))
    return [yol] if os.path.exists(yol) else []


def fi_bedelsiz_tarihleri(A: FIAyar) -> Dict[str, pd.DatetimeIndex]:
    """v1.4: KAP ozetinden (tur == BEDELSIZ) sembol -> bildirim tarihleri. fi_duzelt'in gecis donemi kaniti."""
    dosyalar = _fi_kap_dosyalar(A)
    if not dosyalar:
        raise FileNotFoundError(f"KAP ozeti yok: {A.kap}")
    K = pd.concat([pd.read_csv(f, usecols=["tarih", "sembol", "tur"]) for f in dosyalar], ignore_index=True)
    K = K[K.tur == "BEDELSIZ"].drop_duplicates()
    K["tarih"] = pd.to_datetime(K.tarih, errors="coerce")
    out = {str(s): pd.DatetimeIndex(sorted(g.tarih.dropna().unique())) for s, g in K.groupby("sembol")}
    filog.info("KAP bedelsiz: %d bildirim, %d sembol", len(K), len(out))
    return out


# ---------------------------------------------------------------- K2 olculer
def fi_gunluk(d: pd.DataFrame, A: FIAyar) -> pd.DataFrame:
    pc = d.Close.shift(); r = d.Close / pc - 1; hl = (d.High - d.Low).replace(0, np.nan); v = d.Volume.replace(0, np.nan)
    return pd.DataFrame({"r": r, "rng": (d.High - d.Low) / pc, "up": (r > 0).astype(float),
                         "tavan": (r >= A.sinir_gun).astype(float), "taban": (r <= -A.sinir_gun).astype(float),
                         "clv": (d.Close - d.Low) / hl, "govde": (d.Close - d.Open).abs() / hl,
                         "gapup": (d.Open / pc - 1 > 0.01).astype(float),
                         "vk": v / v.rolling(60, min_periods=30).median().shift(), "tl": np.log10(d.Close * d.Volume + 1)})


def fi_pencere(d: pd.DataFrame, A: FIAyar) -> pd.DataFrame:
    """Son W bar iz olculeri (gercek zamanli)."""
    W = A.W; c = d.Close; pc = c.shift(); r = c / pc - 1; rng = (d.High - d.Low) / pc
    net = np.log(c / c.shift(W)); yol = np.log(c / pc).abs().rolling(W).sum()
    tl = c * d.Volume
    return pd.DataFrame({"g": c / c.shift(W) - 1,
                         "taban": (r <= -A.sinir_gun).astype(int).rolling(W).sum(),
                         "tavan": (r >= A.sinir_gun).astype(int).rolling(W).sum(),
                         "dd": (c / c.rolling(W).max() - 1).rolling(W).min(),
                         "mk": rng.rolling(W).median() / rng.shift(W).rolling(A.normal, min_periods=A.normal_min).median(),
                         "verim": net / yol,
                         "tlk": tl.rolling(W).median() / tl.shift(W).rolling(W).median(),
                         "r2": _fi_r2(np.log(c), 2 * W)})


def _fi_r2(y: pd.Series, n: int) -> pd.Series:
    """Son n barda log fiyatin zamana dogrusal uyumu (R^2): 1'e yakin = dumduz cizgi yukselis (grafikteki 'merdiven')."""
    x = pd.Series(np.arange(len(y), dtype=float), index=y.index)
    cxy = (x * y).rolling(n).mean() - x.rolling(n).mean() * y.rolling(n).mean()
    vx = x.rolling(n).var(ddof=0); vy = y.rolling(n).var(ddof=0)
    return (cxy ** 2 / (vx * vy)).where(vy > 0)


def fi_izler(Z: pd.DataFrame) -> Dict[str, pd.Series]:
    """Vaka fazlarindan cikan izler (sabit esikler) ve birlesimleri."""
    tb = Z.taban == 0; dd = Z.dd >= -0.20; mk = Z.mk < 1.0; ve = Z.verim >= 0.25; tl = Z.tlk >= 1.5; tv = Z.tavan >= 3
    return {"taban_yok": tb, "sig_geri": dd, "mum_kucul": mk, "verim": ve, "tl_artis": tl, "tavan3": tv,
            "A_tb_dd_mk": tb & dd & mk, "B_A_verim": tb & dd & mk & ve, "C_A_tl": tb & dd & mk & tl,
            "D_tb_dd_ve_tl": tb & dd & ve & tl, "E_tek_yon": tv & tb,
            "F_duz_cizgi": (Z.r2 >= 0.85) & tb, "G_duz_cizgi_sig": (Z.r2 >= 0.85) & tb & dd}


def fi_hacim_olc(d: pd.DataFrame, A: FIAyar) -> pd.DataFrame:
    """v1.1: son hW barin sessiz yuvarlanma (Z0) bayragi ve hacim esligi olculeri (gercek zamanli)."""
    W = A.hW; c = d.Close; pc = c.shift(); r = c / pc - 1; rng = (d.High - d.Low) / pc; v = d.Volume.replace(0, np.nan)
    up = r > 0; dn = r < 0
    mr = rng.shift(W).rolling(A.normal, min_periods=A.normal_min).median()
    mv = v.shift(W).rolling(A.normal, min_periods=A.normal_min).median()
    o = pd.DataFrame(index=d.index)
    o["g"] = c / c.shift(W) - 1
    o["mk"] = rng.rolling(W).median() / mr
    o["verim"] = np.log(c / c.shift(W)) / np.log(c / pc).abs().rolling(W).sum()
    o["taban"] = (r <= -A.sinir_gun).astype(int).rolling(W).sum()
    o["dd"] = (c / c.rolling(W).max() - 1).rolling(W).min()
    o["udvr"] = v.where(up, 0).rolling(W).sum() / v.where(dn, 0).rolling(W).sum()
    o["hk"] = v.rolling(W).median() / mv
    o["emilim"] = o.hk / o.mk
    o["vcv"] = v.rolling(W).std() / v.rolling(W).mean()
    o["dh"] = v.where(dn).rolling(W, min_periods=3).mean() / v.where(up).rolling(W, min_periods=3).mean()
    o["emilim_gun"] = ((v / mv >= 1.5) & (rng / mr <= 0.8)).astype(int).rolling(W).sum()
    o["Z0"] = ((o.g >= A.z0_g[0]) & (o.g <= A.z0_g[1]) & (o.mk <= A.z0_mk) & (o.verim >= A.z0_verim)
               & (o.taban == 0) & (o.dd >= A.z0_dd))
    return o


def fi_hacim_varyant(O: pd.DataFrame) -> Dict[str, pd.Series]:
    """v1.1 hacim varyantlari (sabit esikler; K3b'deki fon/diger farkinin yonune gore)."""
    return {"hacim_kuru": O.hk <= 0.6, "yukari_hacim": O.udvr >= 2.5, "kuru_ve_yukari": (O.hk <= 0.6) & (O.udvr >= 2.5),
            "emilim": O.emilim >= 1.5, "emilim_gun": O.emilim_gun >= 2, "dusus_hacmi_kuru": O.dh <= 0.6, "hacim_artan": O.hk >= 1.5}


_FI_HKOL = ["udvr", "hk", "emilim", "vcv", "dh", "emilim_gun", "mk", "g"]


def fi_k3b_hacim_vaka(V: Dict[str, pd.DataFrame], kos: pd.DataFrame, A: FIAyar) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, pd.Series]]:
    """Fon hisselerinin dip->tepe donemindeki Z0 bolgeleri vs diger BIST hisselerinin ayni yillardaki Z0 bolgeleri."""
    fon, diger, zbayrak = [], [], {}
    kosd = kos.set_index("sembol")
    a0, b0 = pd.Timestamp(A.hacim_bas), pd.Timestamp(A.kriz_tarih)
    for s, d in V.items():
        try:
            o = fi_hacim_olc(d, A)
            if s in kosd.index:
                k = kosd.loc[s]; zbayrak[s] = o.Z0
                o = o.loc[k.dip:k.tepe].assign(sembol=s); fon.append(o)
            else:
                diger.append(o.loc[a0:b0].assign(sembol=s))
        except Exception as ex:
            filog.warning("hacim %s atlandi: %s", s, ex)
    Fo = pd.concat(fon); Do = pd.concat(diger)
    ozet = pd.DataFrame({"fon_Z0": Fo[Fo.Z0][_FI_HKOL].median(), "diger_Z0": Do[Do.Z0][_FI_HKOL].median(),
                         "fon_tum": Fo[_FI_HKOL].median(), "diger_tum": Do[_FI_HKOL].median()})
    ozet.loc["Z0_gun_orani_%"] = [Fo.Z0.mean() * 100, Do.Z0.mean() * 100, np.nan, np.nan]
    ozet.loc["Z0_hisse_medyan_%"] = [Fo.groupby("sembol").Z0.mean().median() * 100, Do.groupby("sembol").Z0.mean().median() * 100, np.nan, np.nan]
    hisse = Fo[Fo.Z0].groupby("sembol")[["udvr", "hk", "emilim", "dh", "emilim_gun", "mk"]].median()
    hisse["Z0_gun"] = Fo.groupby("sembol").Z0.sum()
    return ozet.reset_index().rename(columns={"index": "olcu"}), hisse.reset_index(), zbayrak


# ---------------------------------------------------------------- K3 vaka fazlari
def fi_kosu(d: pd.DataFrame, A: FIAyar) -> Optional[Dict[str, Any]]:
    c = d.Close[d.index < pd.Timestamp(A.kriz_tarih)]
    if len(c) < 30:
        return None
    tepe = c.idxmax(); onc = c.loc[:tepe]; dip = onc[onc.index >= tepe - pd.Timedelta(days=A.dip_gun)].idxmin()
    yol = c.loc[dip:tepe]; x2 = yol[yol >= c[dip] * 2].index
    return {"dip": dip, "x2": x2[0] if len(x2) else None, "tepe": tepe, "kat": float(c[tepe] / c[dip]), "bar": len(yol)}


def fi_faz_olc(d: pd.DataFrame, g: pd.DataFrame, rng_yzd: pd.Series, tl_yzd: pd.Series, a, b) -> Dict[str, float]:
    gg = g.loc[a:b]; c = d.Close.loc[a:b]
    if len(gg) < 5:
        return {}
    yol = np.log(c / c.shift()).abs().sum()
    return {"bar": len(gg), "gunluk_get": gg.r.mean() * 100, "yukari_gun": gg.up.mean() * 100,
            "tavan100": gg.tavan.mean() * 100, "taban100": gg.taban.mean() * 100, "mum_med": gg.rng.median() * 100,
            "mum_evren_yzd": rng_yzd.loc[a:b].median() * 100, "tl_evren_yzd": tl_yzd.loc[a:b].median() * 100,
            "hacim_kat": gg.vk.median(), "clv": gg.clv.mean(), "gapup": gg.gapup.mean() * 100,
            "verim": np.log(c.iloc[-1] / c.iloc[0]) / yol if yol > 0 else np.nan, "maks_dd": (c / c.cummax() - 1).min() * 100}


def fi_k3_vaka(V: Dict[str, pd.DataFrame], A: FIAyar) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    G = {s: fi_gunluk(d, A) for s, d in V.items()}
    rng = pd.concat({s: g.rng for s, g in G.items()}, axis=1, sort=True)
    tl = pd.concat({s: g.tl for s, g in G.items()}, axis=1, sort=True)
    rng_yzd = rng.rank(axis=1, pct=True); tl_yzd = tl.rank(axis=1, pct=True)
    kos, faz, tet = [], [], []
    for s in FON_HISSE:
        if s not in V:
            filog.warning("vaka %s veride yok", s); continue
        d = V[s]; k = fi_kosu(d, A)
        if k is None:
            continue
        kos.append({"sembol": s, **k})
        ix = d.index; i0 = ix.get_loc(k["dip"])
        fz = {"ONCE": (ix[max(0, i0 - 120)], ix[max(0, i0 - 1)]), "ERKEN": (k["dip"], k["x2"]),
              "KOSU": (k["x2"], k["tepe"]), "COKUS": (k["tepe"], ix[-1])}
        for f, (a, b) in fz.items():
            if a is None or b is None or (f == "ONCE" and i0 < 30):
                continue
            o = fi_faz_olc(d, G[s], rng_yzd[s], tl_yzd[s], a, b)
            if o:
                faz.append({"sembol": s, "faz": f, **o})
        Z = fi_pencere(d, A); m = fi_izler(Z)["B_A_verim"] & (Z.g >= A.g_alt) & (Z.g < A.g_ust)
        m = m[(m.index >= k["dip"]) & (m.index <= k["tepe"])]
        t = m[m].index.min() if m.any() else None
        c = d.Close
        tet.append({"sembol": s, "kat_dip_tepe": k["kat"], "ilk_iz": t,
                    "iz_aninda_dipten_kat": c[t] / c[k["dip"]] if t is not None else np.nan,
                    "izden_tepeye_kat": c[k["tepe"]] / c[t] if t is not None else np.nan,
                    "izden_bugune_kat": c.iloc[-1] / c[t] if t is not None else np.nan,
                    "tepeden_bugun_pct": (c.iloc[-1] / c[k["tepe"]] - 1) * 100})
    return pd.DataFrame(kos), pd.DataFrame(faz), pd.DataFrame(tet)


# ---------------------------------------------------------------- K4 evren olaylari
def _fi_sonuc(d: pd.DataFrame, i: int, A: FIAyar) -> Optional[Dict[str, float]]:
    c = d.Close.to_numpy(); h = d.High.to_numpy(); l = d.Low.to_numpy(); n = len(c)
    if i + A.ufuk >= n:
        return None
    up = c[i] * A.hedef_kat; dn = c[i] * (1 - A.zarar); s = 0.0
    for j in range(i + 1, i + A.ufuk + 1):
        if l[j] <= dn:
            s = 0.0; break
        if h[j] >= up:
            s = 1.0; break
    return {"x2_once": s, "maks": h[i + 1:i + A.ufuk + 1].max() / c[i], "r_son": c[i + A.ufuk] / c[i] - 1}


def fi_k4_olaylar(V: Dict[str, pd.DataFrame], pazar: str, A: FIAyar) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []; t0 = time.time()
    for no, (s, d) in enumerate(V.items(), 1):
        try:
            if len(d) < 400:
                continue
            Z = fi_pencere(d, A); ok = ((Z.g >= A.g_alt) & (Z.g < A.g_ust) & Z.mk.notna()).to_numpy()
            iz = {k: v.to_numpy() for k, v in fi_izler(Z).items()}
            son = -10 ** 9
            for i in np.flatnonzero(ok):
                if i - son < A.tekrar:
                    continue
                o = _fi_sonuc(d, i, A)
                if o is None:
                    continue
                son = i
                rows.append({"pazar": pazar, "sembol": s, "tarih": d.index[i], **{k: bool(v[i]) for k, v in iz.items()},
                             **{k: float(Z[k].iat[i]) for k in Z.columns}, **o})
        except Exception as ex:
            filog.warning("%s atlandi: %s", s, ex)
        if no % 300 == 0:
            filog.info("%s %d/%d hisse, %d olay, %.0f sn", pazar, no, len(V), len(rows), time.time() - t0)
    O = pd.DataFrame(rows)
    if not O.empty:
        O = O[pd.to_datetime(O.tarih) >= pd.Timestamp("2016-01-01")].copy()
        O["donem"] = np.where(pd.to_datetime(O.tarih) < pd.Timestamp(A.donem_siniri), "2016-21", "2022-26")
    return O


def _fi_once(d: pd.DataFrame, i: int, ufuk: int, yukari: float, asagi: float) -> float:
    c = d.Close.to_numpy(); h = d.High.to_numpy(); l = d.Low.to_numpy()
    for j in range(i + 1, i + ufuk + 1):
        if l[j] <= c[i] * (1 - asagi):
            return 0.0
        if h[j] >= c[i] * (1 + yukari):
            return 1.0
    return 0.0


def fi_k4b_hacim_olaylar(V: Dict[str, pd.DataFrame], pazar: str, A: FIAyar) -> pd.DataFrame:
    """v1.1: evrende Z0 (sessiz yuvarlanma) olaylari ve hacim olculeri; sonuc 250 bar 2 kat / -%30 ve 60 bar +%20 / -%10."""
    rows: List[Dict[str, Any]] = []; t0 = time.time()
    for no, (s, d) in enumerate(V.items(), 1):
        try:
            if len(d) < 400:
                continue
            o = fi_hacim_olc(d, A); z = o.Z0.to_numpy(); son = -10 ** 9; n = len(d); c = d.Close.to_numpy()
            for i in np.flatnonzero(z):
                if i - son < A.hacim_tekrar or i + A.ufuk >= n:
                    continue
                son = i
                rows.append({"pazar": pazar, "sembol": s, "tarih": d.index[i], **{k: float(o[k].iat[i]) for k in _FI_HKOL},
                             "x2_once": _fi_once(d, i, A.ufuk, A.hedef_kat - 1, A.zarar), "k20_once": _fi_once(d, i, 60, 0.20, 0.10),
                             "r60": c[i + 60] / c[i] - 1, "r_son": c[i + A.ufuk] / c[i] - 1})
        except Exception as ex:
            filog.warning("hacim olay %s atlandi: %s", s, ex)
        if no % 300 == 0:
            filog.info("hacim %s %d/%d hisse, %d olay, %.0f sn", pazar, no, len(V), len(rows), time.time() - t0)
    O = pd.DataFrame(rows)
    if not O.empty:
        O = O[pd.to_datetime(O.tarih) >= pd.Timestamp("2016-01-01")].copy()
        O["donem"] = np.where(pd.to_datetime(O.tarih) < pd.Timestamp(A.donem_siniri), "2016-21", "2022-26")
    return O


def fi_ozet_hacim(O: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for ad, m in fi_hacim_varyant(O).items():
        for (p, dn), g in O.groupby(["pazar", "donem"]):
            mm = m.loc[g.index]; s = g[mm]; t = g[~mm]
            if len(s) == 0 or len(t) == 0:
                continue
            rows.append({"iz": ad, "pazar": p, "donem": dn, "n": len(s),
                         "x2_once": s.x2_once.mean() * 100, "t_x2_once": t.x2_once.mean() * 100, "kat_x2": s.x2_once.mean() / t.x2_once.mean(),
                         "k20_once": s.k20_once.mean() * 100, "t_k20_once": t.k20_once.mean() * 100, "kat_k20": s.k20_once.mean() / t.k20_once.mean(),
                         "r60_med": s.r60.median() * 100, "t_r60_med": t.r60.median() * 100})
    oz = pd.DataFrame(rows)
    oz["gecti_x2"] = (oz.kat_x2 >= 1.3) & (oz.n >= 30); oz["gecti_k20"] = (oz.kat_k20 >= 1.3) & (oz.n >= 30)
    iz = oz.groupby("iz").agg(dilim=("n", "size"), gecti_x2=("gecti_x2", "sum"), kat_x2_min=("kat_x2", "min"),
                              gecti_k20=("gecti_k20", "sum"), kat_k20_min=("kat_k20", "min"), n_min=("n", "min")).reset_index()
    return oz, iz.sort_values(["gecti_x2", "gecti_k20", "kat_x2_min"], ascending=False)


def fi_ozet(O: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    adlar = [c for c in O.columns if O[c].dtype == bool]
    rows = []
    for ad in adlar:
        for (p, dn), g in O.groupby(["pazar", "donem"]):
            s = g[g[ad]]; t = g[~g[ad]]
            if len(s) == 0 or len(t) == 0:
                continue
            rows.append({"iz": ad, "pazar": p, "donem": dn, "n": len(s), "x2_once": s.x2_once.mean() * 100,
                         "t_x2_once": t.x2_once.mean() * 100, "kat": s.x2_once.mean() / t.x2_once.mean() if t.x2_once.mean() > 0 else np.nan,
                         "r250_med": s.r_son.median() * 100, "t_r250_med": t.r_son.median() * 100,
                         "maks5x": (s.maks >= 5).mean() * 100, "t_maks5x": (t.maks >= 5).mean() * 100})
    oz = pd.DataFrame(rows)
    oz["gecti"] = (oz.kat >= 1.3) & (oz.n >= 30)
    iz = oz.groupby("iz").agg(dilim=("n", "size"), gecti=("gecti", "sum"), ayni_yon=("kat", lambda k: int((k > 1).sum())),
                              kat_min=("kat", "min"), kat_ort=("kat", "mean"), n_min=("n", "min")).reset_index()
    return oz, iz.sort_values(["gecti", "ayni_yon", "kat_ort"], ascending=False)


# ---------------------------------------------------------------- K6 gosterge bataryasi + uyumsuzluk + Fibonacci (v1.2)
def _fi_ema(x: pd.Series, n: int) -> pd.Series:
    return x.ewm(span=n, adjust=False, min_periods=n).mean()


def _fi_wilder(x: pd.Series, n: int) -> pd.Series:
    return x.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def _fi_bar_once(x: np.ndarray, n: int, en_buyuk: bool) -> np.ndarray:
    """Her bar icin son n+1 bardaki en yuksek (en_buyuk) / en dusuk degerin kac bar once oldugu (Aroon, Fibonacci bacagi)."""
    out = np.full(len(x), np.nan)
    if len(x) <= n:
        return out
    w = np.lib.stride_tricks.sliding_window_view(x, n + 1)
    k = np.argmax(w, axis=1) if en_buyuk else np.argmin(w, axis=1)
    out[n:] = n - k
    return out


def _fi_uyumsuzluk(fiyat: np.ndarray, gosterge: np.ndarray, k: int, ara: int, dip: bool) -> Tuple[np.ndarray, np.ndarray]:
    """Pivot tabanli uyumsuzluk, gelecege bakmadan. Pivot p = p-k..p+k araliginin en dusugu (dip) / en yuksegi (tepe); sinyal
    pivotun dogrulandigi p+k gunu. Ardisik iki pivot (k <= ara farki <= `ara`). Dip: duz boga = fiyat daha dusuk dip, gosterge daha
    yuksek dip; gizli boga = fiyat daha yuksek dip, gosterge daha dusuk dip. Tepe: duz ayi = fiyat daha yuksek tepe, gosterge daha
    dusuk tepe; gizli ayi tersi. Donus: (duz, gizli) bool dizileri."""
    n = len(fiyat); duz = np.zeros(n, bool); gizli = np.zeros(n, bool)
    if n < 2 * k + 2:
        return duz, gizli
    w = np.lib.stride_tricks.sliding_window_view(fiyat, 2 * k + 1)
    ext = w.min(axis=1) if dip else w.max(axis=1)
    tek = (w == ext[:, None]).sum(axis=1) == 1          # kesin uc nokta (duz rafin her bari pivot sayilmaz)
    piv = np.flatnonzero((fiyat[k:n - k] == ext) & tek) + k
    piv = piv[~np.isnan(gosterge[piv])]
    for a, b in zip(piv[:-1], piv[1:]):
        if b - a < k or b - a > ara:
            continue
        fa, fb, ga, gb = fiyat[a], fiyat[b], gosterge[a], gosterge[b]
        t = b + k
        if dip:
            if fb < fa and gb > ga:
                duz[t] = True
            elif fb > fa and gb < ga:
                gizli[t] = True
        else:
            if fb > fa and gb < ga:
                duz[t] = True
            elif fb < fa and gb > ga:
                gizli[t] = True
    return duz, gizli


_FI_UY = (("rsi", "rsi"), ("macd", "macd_hist"), ("obv", "obv"), ("mfi", "mfi"), ("cmf", "cmf"))
_FI_FIB = np.array([0.236, 0.382, 0.5, 0.618, 0.786])


def fi_gostergeler(d: pd.DataFrame, A: FIAyar) -> pd.DataFrame:
    """v1.2 gunluk gosterge tablosu (hepsi yalniz o gune kadarki veriyle)."""
    c, h, l = d.Close, d.High, d.Low; v = d.Volume.astype(float); pc = c.shift(); dc = c.diff(); tp = (h + l + c) / 3
    G = pd.DataFrame(index=d.index)
    G["r"] = c / pc - 1
    up = _fi_wilder(dc.clip(lower=0), 14); dn = _fi_wilder((-dc).clip(lower=0), 14)
    G["rsi"] = 100 * up / (up + dn).replace(0, np.nan)
    hh = h.rolling(14).max(); ll = l.rolling(14).min()
    G["stoch"] = 100 * (c - ll) / (hh - ll).replace(0, np.nan)
    G["wr"] = G.stoch - 100
    m = tp.rolling(20).mean()
    G["cci"] = (tp - m) / (0.015 * (tp - m).abs().rolling(20).mean()).replace(0, np.nan)   # sapma kayan ortalamaya gore (yaklasik)
    rmf = tp * v; pos = rmf.where(tp > tp.shift(), 0.0).rolling(14).sum(); neg = rmf.where(tp < tp.shift(), 0.0).rolling(14).sum()
    G["mfi"] = 100 * pos / (pos + neg).replace(0, np.nan)
    mfm = (((c - l) - (h - c)) / (h - l).replace(0, np.nan)).fillna(0.0)
    G["cmf"] = (mfm * v).rolling(20).sum() / v.rolling(20).sum().replace(0, np.nan)
    obv = (np.sign(dc).fillna(0.0) * v).cumsum(); ad = (mfm * v).cumsum(); v20 = v.rolling(20).sum().replace(0, np.nan)
    G["obv"] = obv
    G["obv20"] = (obv - obv.shift(20)) / v20
    G["ad20"] = (ad - ad.shift(20)) / v20
    G["obv_60tepe"] = obv >= obv.rolling(60).max()
    macd = _fi_ema(c, 12) - _fi_ema(c, 26); sig = _fi_ema(macd, 9)
    G["macd"] = macd / c; G["macd_sinyal"] = sig / c; G["macd_hist"] = (macd - sig) / c
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1); atr = _fi_wilder(tr, 14)
    upm = h.diff(); dnm = -l.diff()
    pdm = upm.where((upm > dnm) & (upm > 0), 0.0); ndm = dnm.where((dnm > upm) & (dnm > 0), 0.0)
    G["pdi"] = 100 * _fi_wilder(pdm, 14) / atr.replace(0, np.nan)
    G["ndi"] = 100 * _fi_wilder(ndm, 14) / atr.replace(0, np.nan)
    G["adx"] = _fi_wilder(100 * (G.pdi - G.ndi).abs() / (G.pdi + G.ndi).replace(0, np.nan), 14)
    hn = h.to_numpy(float); ln = l.to_numpy(float)
    G["aroon_up"] = 100 * (25 - _fi_bar_once(hn, 25, True)) / 25
    G["aroon_dn"] = 100 * (25 - _fi_bar_once(ln, 25, False)) / 25
    m20 = c.rolling(20).mean(); s20 = c.rolling(20).std(ddof=0)
    G["bb_b"] = (c - (m20 - 2 * s20)) / (4 * s20).replace(0, np.nan)
    bw = 4 * s20 / m20
    G["bb_gen"] = bw / bw.rolling(A.normal, min_periods=A.normal_min).median()
    e20 = _fi_ema(c, 20); atr20 = _fi_wilder(tr, 20)
    G["sikisma"] = ((m20 + 2 * s20) < (e20 + 1.5 * atr20)) & ((m20 - 2 * s20) > (e20 - 1.5 * atr20))
    tenkan = (h.rolling(9).max() + l.rolling(9).min()) / 2; kijun = (h.rolling(26).max() + l.rolling(26).min()) / 2
    spa = ((tenkan + kijun) / 2).shift(26); spb = ((h.rolling(52).max() + l.rolling(52).min()) / 2).shift(26)
    G["bulut_ust"] = c > pd.concat([spa, spb], axis=1).max(axis=1, skipna=False)
    G["tk_ust"] = tenkan > kijun
    sma50 = c.rolling(50).mean(); sma200 = c.rolling(200).mean()
    G["sma50_mes"] = c / sma50 - 1; G["sma200_mes"] = c / sma200 - 1; G["sma50_200"] = sma50 > sma200
    G["roc20"] = c / c.shift(20) - 1
    G["c_60tepe"] = c / c.rolling(60).max()
    G["atr_yzd"] = atr / c
    G["force"] = _fi_ema(dc * v, 13) / (c * v.rolling(20).mean()).replace(0, np.nan)
    dd14 = 100 * (c / c.rolling(14).max() - 1)
    G["ulcer"] = np.sqrt((dd14 ** 2).rolling(14).mean())
    n = A.normal; lo = l.rolling(n).min(); hi = h.rolling(n).max()
    G["fib_konum"] = (c - lo) / (hi - lo).replace(0, np.nan)
    yukselis = _fi_bar_once(ln, n - 1, False) > _fi_bar_once(hn, n - 1, True)   # bacak dipten tepeye (dip once)
    geri = ((hi - c) / (hi - lo).replace(0, np.nan)).where(yukselis)
    G["fib_geri"] = geri
    gn = geri.to_numpy(float)
    G["fib_yakin"] = np.min(np.abs(gn[:, None] - _FI_FIB[None, :]), axis=1)
    G["vk"] = v / v.shift().rolling(20, min_periods=10).median().replace(0, np.nan)
    G["kilit_tavan"] = (G.r >= A.sinir_gun) & ((h - l) / c < 0.002)
    for ad, kol in _FI_UY:
        x = G[kol].to_numpy(float)
        a, b = _fi_uyumsuzluk(ln, x, A.piv_k, A.piv_ara, True)
        G[f"uy_{ad}_boga"] = a; G[f"uy_{ad}_gizli_boga"] = b
        a, _ = _fi_uyumsuzluk(hn, x, A.piv_k, A.piv_ara, False)
        G[f"uy_{ad}_ayi"] = a
    return G


def _fi_yukari_kes(x: pd.Series, e: float) -> pd.Series:
    return (x > e) & (x.shift() <= e)


def _fi_yeni(x: pd.Series) -> pd.Series:
    return x & ~x.shift(1, fill_value=False).astype(bool)


# v1.4 esli taban: sinyalin kendi baglamini tasiyan ama sinyali tasimayan gunler (ABD'de 'tavan/taban' = +-%9,5 gun; sinir yok).
FI_ESLI = {"blok_taban": "_es_taban_bloksuz", "blok_tavan": "_es_tavan_bloksuz", "blok_seri_ici": "_es_tavan_bloksuz",
           "kap_olagan_disi": "_es_sicrama20", "kap_vbts_tedbir": "_es_tavan"}
# Asagi yonlu (satis/kacinma) sinyalleri: bunlarda iz = 'dus' sonucunda kat >= 1,3.
FI_AYI = {"rsi_70_ustu", "mfi_80_ustu", "cmf_negatif", "bb_alt_kirilim", "fib_tepe_bolge", "blok_taban",
          "uy_rsi_ayi", "uy_macd_ayi", "uy_obv_ayi", "uy_mfi_ayi", "uy_cmf_ayi",
          "kap_devre_kesici", "kap_olagan_disi", "kap_spk_yasak", "kap_vbts_tedbir", "kap_tipe_donusum"}


def fi_gosterge_sinyal(G: pd.DataFrame, A: FIAyar) -> Dict[str, pd.Series]:
    """Sabit esikli ikili sinyaller (gosterge ders kitabi esikleri; veriye gore ayarlanmadi)."""
    blok = G.vk >= A.blok_kat; tavan = G.r >= A.sinir_gun
    S = {"rsi_30_alti": G.rsi < 30, "rsi_70_ustu": G.rsi > 70, "rsi_50_kesme": _fi_yukari_kes(G.rsi, 50),
         "stoch_20_donus": _fi_yukari_kes(G.stoch, 20), "wr_80_alti": G.wr < -80,
         "cci_100_alti": G.cci < -100, "cci_100_ustu": G.cci > 100,
         "mfi_20_alti": G.mfi < 20, "mfi_80_ustu": G.mfi > 80,
         "cmf_pozitif": G.cmf > 0.10, "cmf_negatif": G.cmf < -0.10,
         "obv_lider": G.obv_60tepe & (G.c_60tepe < 0.95),
         "ad_birikim_yatay": (G.ad20 > 0.20) & (G.roc20.abs() < 0.03),
         "macd_al_sifir_alti": _fi_yukari_kes(G.macd - G.macd_sinyal, 0.0) & (G.macd < 0),
         "macd_sifir_kesme": _fi_yukari_kes(G.macd, 0.0),
         "adx_25_trend": _fi_yukari_kes(G.adx, 25) & (G.pdi > G.ndi),
         "aroon_yukari": (G.aroon_up > 70) & (G.aroon_dn < 30),
         "bb_sikisma": G.bb_gen < 0.6, "bb_ust_kirilim": G.bb_b > 1, "bb_alt_kirilim": G.bb_b < 0,
         "squeeze_yukari_cozulme": (~G["sikisma"]) & G["sikisma"].shift(1, fill_value=False).astype(bool) & (G.macd_hist > 0),
         "bulut_ustu_kesme": _fi_yeni(G.bulut_ust), "tenkan_kijun_kesme": _fi_yeni(G.tk_ust), "altin_kesisim": _fi_yeni(G.sma50_200),
         "fib_618_bolge": (G.fib_geri >= 0.55) & (G.fib_geri <= 0.68), "fib_382_bolge": (G.fib_geri >= 0.33) & (G.fib_geri <= 0.43),
         "fib_dip_bolge": G.fib_konum < 0.15, "fib_tepe_bolge": G.fib_konum > 0.90,
         "force_guclu": G.force > 0.01, "ulcer_sakin_trend": (G.ulcer < 3) & (G.roc20 > 0.05),
         "blok_hacim": blok, "blok_tavan": blok & tavan,
         "blok_seri_ici": blok & tavan & (G.kilit_tavan.astype(int).rolling(5).sum().shift() >= 2),
         "blok_taban": blok & (G.r <= -A.sinir_gun), "kilit_tavan": G.kilit_tavan,
         # v1.4 esli tabanlar (denetim 23 Eki): ayni gun kosulu, sinyalsiz. Iz tablosuna girmez, kat_esli icin.
         "_es_taban_bloksuz": (G.r <= -A.sinir_gun) & ~blok, "_es_tavan_bloksuz": tavan & ~blok,
         "_es_tavan": tavan, "_es_sicrama20": G.roc20 >= 0.40}
    for ad, _ in _FI_UY:
        for t in ("boga", "gizli_boga", "ayi"):
            S[f"uy_{ad}_{t}"] = G[f"uy_{ad}_{t}"]
    return {k: v.fillna(False).astype(bool) for k, v in S.items()}


def _fi_ilk(c: np.ndarray, h: np.ndarray, l: np.ndarray, ufuk: int, yukari: float, asagi: float) -> Tuple[np.ndarray, np.ndarray]:
    """Her gun icin ufuk bar icinde once +yukari (High) mi once -asagi (Low) mu; (once_yukari, once_asagi) 1/0, ufuk dolmadiysa NaN.
    Ayni barda ikisi birden: asagi sayilir (temkinli; _fi_once ile ayni)."""
    n = len(c); u = np.full(n, np.nan); a = np.full(n, np.nan)
    m = n - ufuk
    if m <= 0:
        return u, a
    Hw = np.lib.stride_tricks.sliding_window_view(h[1:], ufuk)[:m]; Lw = np.lib.stride_tricks.sliding_window_view(l[1:], ufuk)[:m]
    yu = Hw >= (c[:m] * (1 + yukari))[:, None]; ya = Lw <= (c[:m] * (1 - asagi))[:, None]
    iu = np.where(yu.any(1), yu.argmax(1), ufuk + 1); ia = np.where(ya.any(1), ya.argmax(1), ufuk + 1)
    u[:m] = (iu < ia).astype(float); a[:m] = ((ia < iu) | ((ia == iu) & (ia <= ufuk))).astype(float)   # v1.4: ayni bar -> asagi
    return u, a


_FI_SONUC = ("k20", "x2", "dus")


def _fi_sonuclar(d: pd.DataFrame) -> Dict[str, np.ndarray]:
    c = d.Close.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float)
    k20, _ = _fi_ilk(c, h, l, 60, 0.20, 0.10); x2, _ = _fi_ilk(c, h, l, 250, 1.00, 0.30); _, dus = _fi_ilk(c, h, l, 60, 0.20, 0.20)
    return {"k20": k20, "x2": x2, "dus": dus}


# ---------------------------------------------------------------- K8 KAP olaylari (v1.2)
FI_KAP_KONU = {"kap_vbts_tedbir": (14,), "kap_tipe_donusum": (13,), "kap_toptan": (84, 119, 140), "kap_pay_alim_satim": (6,),
               "kap_devre_kesici": (0,), "kap_olagan_disi": (42,), "kap_spk_yasak": (30,), "kap_fiili_dolasim": (61,),
               "kap_piyasa_yapici": (3,), "kap_soylenti": (79,)}


def fi_kap_yukle(A: FIAyar) -> Dict[str, Dict[str, pd.DataFrame]]:
    """kap_ozet (tarih, saat, sembol, konu_id) -> {sembol: {grup: DataFrame(tarih, saat)}}. Klasor (kap_20*.csv.gz) ya da tek dosya."""
    yol = A.kap
    if os.path.isdir(yol):
        dosyalar = sorted(os.path.join(yol, f) for f in os.listdir(yol) if f.startswith("kap_20") and f.endswith(".csv.gz"))
    else:
        dosyalar = [yol]
    if not dosyalar or not all(os.path.exists(f) for f in dosyalar):
        raise FileNotFoundError(f"KAP ozeti yok: {yol}")
    K = pd.concat([pd.read_csv(f, usecols=["tarih", "saat", "sembol", "konu_id"]) for f in dosyalar], ignore_index=True)
    K = K.drop_duplicates()
    ters = {k: g for g, ks in FI_KAP_KONU.items() for k in ks}
    K = K[K.konu_id.isin(ters)].copy(); K["grup"] = K.konu_id.map(ters)
    K["tarih"] = pd.to_datetime(K.tarih, errors="coerce"); K = K.dropna(subset=["tarih"])
    out: Dict[str, Dict[str, pd.DataFrame]] = {}
    for (s, g), t in K.groupby(["sembol", "grup"]):
        out.setdefault(str(s), {})[g] = t[["tarih", "saat"]]
    filog.info("KAP: %d bildirim, %d sembol (%s .. %s)", len(K), len(out), K.tarih.min().date(), K.tarih.max().date())
    return out


def fi_kap_sinyal(idx: pd.DatetimeIndex, olay: Optional[Dict[str, pd.DataFrame]]) -> Dict[str, pd.Series]:
    """Bildirimleri islem gunune esler: saat 18:00 ve sonrasi -> ertesi islem gunu (D0), aksi halde ayni gun (ya da sonraki ilk islem gunu)."""
    S = {}
    for g in FI_KAP_KONU:
        b = np.zeros(len(idx), bool)
        if olay and g in olay:
            t = olay[g]
            gun = t.tarih + pd.to_timedelta((t.saat.astype(str) >= "18:00").astype(int), unit="D")
            j = idx.searchsorted(gun.to_numpy(), side="left")
            j = j[j < len(idx)]
            b[j] = True
        S[g] = pd.Series(b, index=idx)
    return S


# ---------------------------------------------------------------- K6a fon vakalari / K6b evren
_FI_GKOL = ["rsi", "mfi", "cmf", "obv20", "ad20", "adx", "bb_gen", "fib_konum", "atr_yzd", "macd_hist", "vk", "roc20", "ulcer", "force"]


def fi_k6_vaka(V: Dict[str, pd.DataFrame], kos: pd.DataFrame, kap: Dict[str, Dict[str, pd.DataFrame]], A: FIAyar
               ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Fon hisselerinin ONCE / ERKEN / KOSU fazlarinda 100 gunde sinyal sikligi ve gosterge medyanlari vs diger BIST (2024-26).
    Donus: (sinyal profili, gosterge profili, fon hisselerinin blok hacim gunleri)."""
    say: Dict[str, Dict[str, float]] = {}; gun: Dict[str, int] = {}; deger: Dict[str, List[pd.DataFrame]] = {}; blok = []
    kosd = kos.set_index("sembol"); a0, b0 = pd.Timestamp(A.hacim_bas), pd.Timestamp(A.kriz_tarih)
    for s, d in V.items():
        try:
            G = fi_gostergeler(d, A); S = fi_gosterge_sinyal(G, A); S.update(fi_kap_sinyal(d.index, kap.get(s)))
            Sd = pd.DataFrame(S)
            if s in kosd.index:
                k = kosd.loc[s]; i_dip = d.index.get_loc(k.dip)
                bitis_erken = k.x2 if pd.notna(k.x2) else k.tepe
                fazlar = {"ONCE": d.index[max(0, i_dip - A.once_bar):i_dip], "ERKEN": d.loc[k.dip:bitis_erken].index,
                          "KOSU": d.loc[bitis_erken:k.tepe].index[1:] if pd.notna(k.x2) else d.index[:0]}
                b = G.loc[k.dip:k.tepe]; b = b[b.vk >= A.blok_kat]
                for t, row in b.iterrows():
                    blok.append({"sembol": s, "tarih": t.date(), "r_yzd": row.r * 100, "hacim_kat": row.vk,
                                 "kilit_tavan_onceki5": int(G.kilit_tavan.loc[:t].iloc[-6:-1].sum()),
                                 "faz": "ERKEN" if t <= bitis_erken else "KOSU"})
            else:
                fazlar = {"DIGER": d.loc[a0:b0].index}
            for f, ix in fazlar.items():
                if len(ix) == 0:
                    continue
                q = say.setdefault(f, {})
                for c in Sd.columns:
                    q[c] = q.get(c, 0.0) + float(Sd.loc[ix, c].sum())
                gun[f] = gun.get(f, 0) + len(ix)
                deger.setdefault(f, []).append(G.loc[ix, _FI_GKOL])
        except Exception as ex:
            filog.warning("gosterge vaka %s atlandi: %s", s, ex)
    fz = [f for f in ("ONCE", "ERKEN", "KOSU", "DIGER") if f in gun]
    P = pd.DataFrame({f: {c: 100.0 * v / gun[f] for c, v in say[f].items() if not c.startswith("_es_")} for f in fz})
    if "DIGER" in P:
        for f in ("ONCE", "ERKEN", "KOSU"):
            if f in P:
                P[f"{f}/DIGER"] = P[f] / P["DIGER"].replace(0, np.nan)
    P.loc["_gun_sayisi"] = [gun.get(f, np.nan) for f in fz] + [np.nan] * (P.shape[1] - len(fz))
    D = pd.DataFrame({f: pd.concat(deger[f]).median() for f in fz})
    return P.reset_index().rename(columns={"index": "sinyal"}), D.reset_index().rename(columns={"index": "gosterge"}), pd.DataFrame(blok)


def fi_k6_evren(V: Dict[str, pd.DataFrame], pazar: str, kap: Optional[Dict[str, Dict[str, pd.DataFrame]]], A: FIAyar) -> pd.DataFrame:
    """Her sinyal (ayni hissede g_tekrar bar icinde bir kez) ve taban (her ornek_adim. gun) icin sonuc sayaclari, donem bazinda."""
    top: Dict[Tuple[str, str], List[float]] = {}; t0 = time.time(); bas = pd.Timestamp("2016-01-01"); sinir = pd.Timestamp(A.donem_siniri)

    def ekle(ad: str, ix: np.ndarray, Y: Dict[str, np.ndarray], dn: np.ndarray) -> None:
        for donem in ("2016-21", "2022-26"):
            j = ix[dn[ix] == donem]
            if len(j) == 0:
                continue
            q = top.setdefault((ad, donem), [0.0] * 7)
            q[0] += len(j)
            for k, y in enumerate(_FI_SONUC):
                yy = Y[y][j]; ok = ~np.isnan(yy)
                q[1 + 2 * k] += ok.sum(); q[2 + 2 * k] += yy[ok].sum()

    for no, (s, d) in enumerate(V.items(), 1):
        try:
            if len(d) < 400:
                continue
            G = fi_gostergeler(d, A); S = fi_gosterge_sinyal(G, A)
            if kap is not None:
                S.update(fi_kap_sinyal(d.index, kap.get(s)))
            Y = _fi_sonuclar(d)
            gecerli = (d.index >= bas)
            dn = np.where(d.index < sinir, "2016-21", "2022-26")
            taban = np.flatnonzero(gecerli & (np.arange(len(d)) % A.ornek_adim == 0) & G.rsi.notna().to_numpy())
            ekle("_TABAN", taban, Y, dn)
            for ad, sg in S.items():
                ix = np.flatnonzero(sg.to_numpy() & gecerli)
                if len(ix) == 0:
                    continue
                tut = []; son = -10 ** 9
                for i in ix:
                    if i - son >= A.g_tekrar:
                        tut.append(i); son = i
                ekle(ad, np.asarray(tut, dtype=int), Y, dn)
        except Exception as ex:
            filog.warning("gosterge evren %s %s atlandi: %s", pazar, s, ex)
        if no % 300 == 0:
            filog.info("gosterge %s %d/%d hisse, %.0f sn", pazar, no, len(V), time.time() - t0)
    rows = [{"pazar": pazar, "sinyal": a, "donem": dn, "n": q[0], "n_k20": q[1], "k20": q[2], "n_x2": q[3], "x2": q[4],
             "n_dus": q[5], "dus": q[6]} for (a, dn), q in top.items()]
    return pd.DataFrame(rows)


def fi_k6_ozet(E: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Oranlar ve kat (sinyal / taban); iz: yukari sinyalde k20 ya da x2, asagi sinyalde dus katinin >= 1,3 oldugu dilim sayisi."""
    E = E.copy()
    for y in _FI_SONUC:
        E[f"{y}_yzd"] = 100 * E[y] / E[f"n_{y}"].replace(0, np.nan)
    T = E[E.sinyal == "_TABAN"].set_index(["pazar", "donem"])
    S = E[E.sinyal != "_TABAN"].copy()
    for y in _FI_SONUC:
        S[f"t_{y}_yzd"] = [T.loc[(p, dn), f"{y}_yzd"] for p, dn in zip(S.pazar, S.donem)]
        S[f"kat_{y}"] = S[f"{y}_yzd"] / S[f"t_{y}_yzd"]
    for y in _FI_SONUC:                                   # v1.4 esli taban katlari
        es = S.set_index(["sinyal", "pazar", "donem"])[f"{y}_yzd"]
        S[f"kat_{y}_esli"] = [r / es.get((FI_ESLI[g], p, dn), np.nan) if g in FI_ESLI else np.nan
                              for g, p, dn, r in zip(S.sinyal, S.pazar, S.donem, S[f"{y}_yzd"])]
    S["esli_taban"] = S.sinyal.map(FI_ESLI)
    S = S[~S.sinyal.str.startswith("_es_")].copy()
    S["yon"] = np.where(S.sinyal.isin(FI_AYI), "asagi", "yukari")
    S["gecti_k20"] = (S.yon == "yukari") & (S.kat_k20 >= 1.3) & (S.n_k20 >= 30)
    S["gecti_x2"] = (S.yon == "yukari") & (S.kat_x2 >= 1.3) & (S.n_x2 >= 30)
    S["gecti_dus"] = (S.yon == "asagi") & (S.kat_dus >= 1.3) & (S.n_dus >= 30)
    iz = S.groupby(["sinyal", "yon"]).agg(dilim=("n", "size"), n_min=("n", "min"),
                                          gecti_k20=("gecti_k20", "sum"), kat_k20_min=("kat_k20", "min"), kat_k20_ort=("kat_k20", "mean"),
                                          gecti_x2=("gecti_x2", "sum"), kat_x2_min=("kat_x2", "min"),
                                          gecti_dus=("gecti_dus", "sum"), kat_dus_min=("kat_dus", "min"), kat_dus_ort=("kat_dus", "mean"),
                                          kat_dus_esli_min=("kat_dus_esli", "min"), kat_dus_esli_ort=("kat_dus_esli", "mean"),
                                          kat_k20_esli_min=("kat_k20_esli", "min"), kat_k20_esli_ort=("kat_k20_esli", "mean"),
                                          esli_taban=("esli_taban", "first")).reset_index()
    iz["iz"] = np.where(iz.yon == "yukari", (iz.gecti_k20 == iz.dilim) | (iz.gecti_x2 == iz.dilim), iz.gecti_dus == iz.dilim) & (iz.dilim >= np.where(iz.sinyal.astype(str).str.startswith("kap_"), 2, 4))   # denetim: KAP yalniz BIST, 2 dilim
    esli_ok = np.where(iz.yon == "asagi", iz.kat_dus_esli_min >= 1.3, iz.kat_k20_esli_min >= 1.3)   # v1.4: esli tabani da gecmeli
    iz["iz"] = iz.iz & (iz.esli_taban.isna() | esli_ok)
    iz["sira"] = np.where(iz.yon == "yukari", iz.kat_k20_min, iz.kat_dus_min)
    return S, iz.sort_values(["iz", "sira"], ascending=False).drop(columns="sira")


def fi_k6_rapor(P: pd.DataFrame, D: pd.DataFrame, blok: pd.DataFrame, iz: pd.DataFrame, S: pd.DataFrame, kos: pd.DataFrame) -> str:
    gosterge = [r for r in iz.sinyal if not r.startswith("kap_")]
    sat = [f"# FON_IZI gosterge bataryasi — {FI_SURUM}", "",
           "Soru (Cemal, 23 Eki): fonlar hisseleri alirken iz birakmadi mi? Mum ve hacim disinda her gosterge, uyumsuzluk, Fibonacci.", "",
           "## Fon hisselerinde blok hacim gunleri (hacim >= 20x onceki 20 gun medyani, dip -> tepe)", "",
           blok.round(2).to_markdown(index=False) if len(blok) else "(yok)", "",
           "## Fon hisseleri: 100 gunde sinyal sikligi (ONCE = dipten onceki 120 bar, ERKEN = dip -> 2 kat, KOSU = 2 kat -> tepe;"
           " DIGER = fon disi BIST 2024-26)", "", P.round(2).to_markdown(index=False), "",
           "## Fon hisseleri: gosterge medyanlari", "", D.round(3).to_markdown(index=False), "",
           "## Evren testi: gostergeler (4 dilim BIST/ABD x 2016-21/2022-26; kat = sinyal orani / her 5. gun tabani)", "",
           iz[iz.sinyal.isin(gosterge)].round(2).to_markdown(index=False), "",
           "## Evren testi: KAP olaylari (yalniz BIST, 2 dilim; 2017 oncesi KAP verisi yok)", "",
           iz[~iz.sinyal.isin(gosterge)].round(2).to_markdown(index=False), "",
           "## Vaka kosulari", "", kos.assign(**{c: pd.to_datetime(kos[c]).dt.date for c in ("dip", "x2", "tepe")}).round(2).to_markdown(index=False), ""]
    return "\n".join(sat)


def fon_izi_gosterge(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    """v1.2 ana giris: K6 gosterge/uyumsuzluk/Fibonacci + K7 blok hacim + K8 KAP olaylari; vaka profili ve evren testi."""
    A = A or FIAyar()
    os.makedirs(A.cikti, exist_ok=True)
    veri = {}
    for pazar, yol in A.veri.items():
        try:
            veri[pazar] = fi_k1_veri(yol, pazar, A)
        except Exception as ex:
            filog.error("%s verisi okunamadi (%s); bu pazar atlandi", pazar, ex)
    if "BIST" not in veri:
        raise RuntimeError("BIST verisi yok; vaka incelemesi yapilamaz")
    try:
        kap = fi_kap_yukle(A)
    except Exception as ex:
        filog.error("KAP ozeti okunamadi (%s); KAP sinyalleri bos", ex); kap = {}
    kos = []
    for s in FON_HISSE:
        if s in veri["BIST"]:
            k = fi_kosu(veri["BIST"][s], A)
            if k:
                kos.append({"sembol": s, **k})
    kos = pd.DataFrame(kos)
    P, D, blok = fi_k6_vaka(veri["BIST"], kos, kap, A)
    E = pd.concat([fi_k6_evren(V, p, kap if p == "BIST" else None, A) for p, V in veri.items()], ignore_index=True)
    S, iz = fi_k6_ozet(E)
    P.to_csv(os.path.join(A.cikti, "fon_gosterge_profil.csv"), index=False)
    D.to_csv(os.path.join(A.cikti, "fon_gosterge_deger.csv"), index=False)
    blok.to_csv(os.path.join(A.cikti, "fon_blok_gunleri.csv"), index=False)
    S.to_csv(os.path.join(A.cikti, "fon_gosterge_evren.csv"), index=False)
    iz.to_csv(os.path.join(A.cikti, "fon_gosterge_iz.csv"), index=False)
    with open(os.path.join(A.cikti, "FON_IZI_gosterge.md"), "w", encoding="utf-8") as f:
        f.write(fi_k6_rapor(P, D, blok, iz, S, kos))
    return {"profil": P, "deger": D, "blok": blok, "evren": S, "iz": iz, "kosular": kos}


# ---------------------------------------------------------------- K9 fon islem defteri (v1.3): KAP portfoy dagilim raporlari
FI_TASFIYE_RE = r"^\s*(TERA|PUSULA|HEDEF|ATLAS|A1|PARDUS|BULLS)( CAP[İI]TAL)?( PORTF.*)?\s*$"   # v1.6: sirket adinin tamami (alt dizgi degil)
FI_FON_SIRKET = ("TERA PORTF", "PUSULA PORTF", "HEDEF PORTF", "ATLAS PORTF", "A1 CAPITAL PORTF", "A1 PORTF", "PARDUS PORTF", "BULLS PORTF")
_FI_KAP = "https://www.kap.org.tr"


def _fi_kap_oturum():
    import requests
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
                      "Accept": "application/json, text/plain, */*", "Content-Type": "application/json;charset=UTF-8",
                      "Origin": _FI_KAP, "Referer": _FI_KAP + "/tr/bildirim-sorgu"})
    try:
        s.get(_FI_KAP + "/tr/bildirim-sorgu", timeout=30)
    except Exception as ex:
        filog.warning("KAP acilis sayfasi: %s", ex)
    return s


def _fi_kap_istek(s, yontem: str, url: str, deneme: int = 4, **kw):
    """KAP istegi; 403/429/5xx ve ag hatasinda artan beklemeyle tekrar. Basarisizsa None."""
    for i in range(deneme):
        try:
            r = s.request(yontem, url, timeout=60, **kw)
            if r.status_code == 200:
                return r
            filog.warning("KAP %s %s -> HTTP %s (deneme %d)", yontem, url[-60:], r.status_code, i + 1)
            if r.status_code == 404:
                return None
        except Exception as ex:
            filog.warning("KAP %s %s -> %s (deneme %d)", yontem, url[-60:], str(ex)[:100], i + 1)
            r = None
        time.sleep((20 if r is not None and r.status_code == 429 else 3) * (i + 1))   # 429: KAP hiz siniri, uzun bekle
    return None


FI_K9_SURUM = "v1.5"   # ayristirici surumu: degisirse eski raporlar (metni varsa) yeniden ayristirilir
FI_K9_HARIC = ("PARA PİYASASI", "PARA PIYASASI", "BORÇLANMA ARAÇLARI", "KISA VADELİ", "ALTIN", "GÜMÜŞ", "KIYMETLİ MADEN", "EUROBOND",
               "DÖVİZ", "KİRA SERTİFİKA", "FON SEPETİ", "GİRİŞİM SERMAYESİ", "GAYRİMENKUL", "LİKİT")   # BIST hissesi tasimayan fon turleri


def fi_k9_liste(A: FIAyar) -> pd.DataFrame:
    """KAP 'Portfoy Dagilim Raporu' listesi (butun fonlar). v1.5: konu suzgeciyle haftalik sorgu; 2000 kayit sinirina carpan
    aralik ikiye bolunur (v1.3 gun gun konusuz sorguda 13 ceyrek basi gunu sinira takiliyor, ayin 15'inden sonra yayimlanan
    raporlar hic taranmiyordu). Kaldigi yerden devam eder; liste.csv birlesik yazilir."""
    import json
    os.makedirs(A.kapfon, exist_ok=True)
    yol = os.path.join(A.kapfon, "liste.csv"); yol_h = os.path.join(A.kapfon, "liste_haftalar.txt")
    L = pd.read_csv(yol) if os.path.exists(yol) else pd.DataFrame()
    bitti = set(open(yol_h).read().split()) if os.path.exists(yol_h) else set()
    son = pd.Timestamp(A.kapfon_bit)
    haftalar = [b for b in pd.date_range(A.kapfon_bas, son, freq="7D")]
    s = _fi_kap_oturum(); t0 = time.time()

    def sorgu(a: pd.Timestamp, b: pd.Timestamp) -> List[Dict[str, Any]]:
        r = _fi_kap_istek(s, "POST", _FI_KAP + "/tr/api/disclosure/funds/byCriteria", deneme=6,
                          data=json.dumps({"fromDate": str(a.date()), "toDate": str(b.date()), "mkkMemberOidList": [],
                                           "subjectList": [A.kapfon_konu]}))
        if r is None:
            raise RuntimeError(f"KAP liste {a.date()}..{b.date()} alinamadi")
        J = r.json(); time.sleep(A.kapfon_bekle)
        if len(J) >= 2000:
            if a == b:
                raise RuntimeError(f"KAP liste {a.date()}: tek gunde 2000 rapor, sinir asilamiyor")
            m = a + pd.Timedelta(days=int((b - a).days // 2))
            return sorgu(a, m) + sorgu(m + pd.Timedelta(days=1), b)
        return J

    for no, bas in enumerate(haftalar, 1):
        bit = min(bas + pd.Timedelta(days=6), son)
        anahtar = f"{bas.date()}_{bit.date()}"
        if anahtar in bitti and bit < son - pd.Timedelta(days=45):   # son 45 gun her calistirmada yeniden (gec raporlar)
            continue
        try:
            J = sorgu(bas, bit)
        except Exception as ex:
            filog.error("%s; sonraki calistirmada tekrar denenecek", ex); continue
        yeni = [{"yayin": j.get("publishDate"), "fon": j.get("fundCode"), "unvan": j.get("kapTitle"),
                 "indeks": j.get("disclosureIndex"), "yil": j.get("year"), "donem": j.get("period"), "ek": j.get("attachmentCount"),
                 "duzeltme": j.get("modifyStatus"), "kural": j.get("ruleType")}
                for j in J if (j.get("subject") or "").strip() == "Portföy Dağılım Raporu"]
        if yeni:
            L = pd.concat([L, pd.DataFrame(yeni)], ignore_index=True).drop_duplicates("indeks", keep="last")
        bitti.add(anahtar)
        if no % 20 == 0 or no == len(haftalar):
            L.to_csv(yol, index=False)
            with open(yol_h, "w") as f:
                f.write("\n".join(sorted(bitti)))
            filog.info("KAP liste %d/%d hafta, %d rapor, %.0f sn", no, len(haftalar), len(L), time.time() - t0)
    L.to_csv(yol, index=False)
    return L


def _fi_muaf(metin: str) -> bool:
    """Nitelikli yatirimciya satilan fonun 'portfoy dagilim raporu hazirlama yukumlulugunden muaftir' bildirimi (satir kirilmasi olabilir)."""
    return "yükümlülüğünden muaf" in _fi_re.sub(r"\s+", " ", metin[:5000])


def fi_k9_secim(L: pd.DataFrame) -> pd.DataFrame:
    """Indirilecek raporlar: BIST hissesi tasiyabilecek fon turleri (FI_K9_HARIC disi); ayni fon-donemin yalniz son (duzeltilmis) raporu."""
    u = L.unvan.astype(str).str.upper()
    H = L[~u.apply(lambda x: any(k in x for k in FI_K9_HARIC))].copy()
    if "kural" in H:                                                   # tasfiyedeki fonlarin haftalik raporlari (aylik seriye girmez)
        H = H[~H.kural.fillna("").astype(str).str.contains("Hafta")]
    H["indeks"] = H.indeks.astype(int)
    H = H.sort_values("indeks").groupby(["fon", "yil", "donem"], as_index=False).tail(1)
    # indirme sirasi (KAP hiz siniri ~1 rapor/sn; yarida kalirsa eldeki fonlarin butun donemleri tam olsun): hedef sirketler,
    # hisse senedi fonlari, degisken/katilim/endeks, digerleri; her grupta fon fon
    uu = H.unvan.astype(str).str.upper()
    H["_oncelik"] = np.select([uu.str.contains("|".join(FI_FON_SIRKET)), uu.str.contains("HİSSE SENEDİ"),
                               uu.str.contains("DEĞİŞKEN|KATILIM|ENDEKS|ÇOKLU VARLIK")], [0, 1, 2], 3)
    return H.sort_values(["_oncelik", "fon", "indeks"]).drop(columns="_oncelik")


def _fi_metne(pdf: bytes, hedef_txt: str) -> int:
    """PDF baytlari -> duzen korumali metin dosyasi. Donus: karakter sayisi (0 = metin cikmadi)."""
    import subprocess, tempfile
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(pdf); gecici = f.name
    try:
        t = subprocess.run(["pdftotext", "-layout", gecici, "-"], capture_output=True, timeout=120).stdout.decode("utf-8", "replace")
    except Exception:
        try:
            from pypdf import PdfReader
            t = "\n".join((p.extract_text(extraction_mode="layout") or "") for p in PdfReader(gecici).pages)
        except Exception:
            t = ""
    finally:
        os.unlink(gecici)
    with open(hedef_txt, "w", encoding="utf-8") as f:
        f.write(t)
    return len(t.strip())


def fi_k9_indir(L: pd.DataFrame, A: FIAyar) -> pd.DataFrame:
    """Secilen raporlari indirir ve metne cevirir (PDF tutulmaz; metin cikmayan PDF 'pdf/' altinda saklanir).
    Rapor sayfasindaki ekler; eki olmayan raporda bildirimin kendi PDF'i (BildirimPdf). Nitelikli yatirimciya satilan fonlarin
    'portfoy dagilim raporu hazirlama yukumlulugunden muaftir' bildirimi durum='muaf' yazilir.
    ekler.csv: indeks, dosya (metin yolu, ; ile birden fazla), durum (ok / muaf / bos / hata). Kaldigi yerden devam eder."""
    import re, threading
    from concurrent.futures import ThreadPoolExecutor, as_completed
    kt = os.path.join(A.kapfon, "txt"); kp = os.path.join(A.kapfon, "pdf")
    os.makedirs(kt, exist_ok=True); os.makedirs(kp, exist_ok=True)
    yol = os.path.join(A.kapfon, "ekler.csv")
    E = fi_k9_ekler_oku(A)
    tamam = set(E[E.durum.isin(["ok", "muaf", "bos"])].indeks.astype(int))
    H = fi_k9_secim(L); H = H[~H.indeks.isin(tamam)]
    yerel = threading.local(); kilit = threading.Lock(); sonuc: List[Dict[str, Any]] = []; t0 = time.time()

    def oturum():
        if not hasattr(yerel, "s"):
            yerel.s = _fi_kap_oturum()
        return yerel.s

    def bir(row) -> Dict[str, Any]:
        s = oturum(); ind = int(row.indeks)
        r = _fi_kap_istek(s, "GET", f"{_FI_KAP}/tr/Bildirim/{ind}", deneme=6); time.sleep(A.kapfon_bekle)
        if r is None:
            return {"indeks": ind, "dosya": "", "durum": "hata"}
        linkler = sorted(set(re.findall(r"https://www\.kap\.org\.tr/tr/api/file/download/[0-9a-f]+", r.text)))
        if not linkler:
            linkler = [f"{_FI_KAP}/tr/api/BildirimPdf/{ind}"]
        dosyalar, muaf = [], False
        for k, u in enumerate(linkler):
            d = _fi_kap_istek(s, "GET", u, deneme=6); time.sleep(A.kapfon_bekle)
            if d is None:
                return {"indeks": ind, "dosya": "", "durum": "hata"}
            b = d.content; i = b.find(b"%PDF"); b = b[i:] if i >= 0 else b
            txt = os.path.join(kt, f"{ind}__{row.fon}_{int(row.yil)}_{int(row.donem)}_{k}.txt")
            n = _fi_metne(b, txt)
            if n < 200:
                with open(os.path.join(kp, os.path.basename(txt)[:-4] + ".pdf"), "wb") as f:
                    f.write(b)
            with open(txt, encoding="utf-8") as f:
                muaf |= _fi_muaf(f.read())
            dosyalar.append(os.path.relpath(txt, A.kapfon))           # goreli yol: klasor tasinabilir (Drive, Colab, paket)
        durum = "muaf" if muaf else ("ok" if dosyalar else "bos")
        return {"indeks": ind, "dosya": ";".join(dosyalar), "durum": durum}

    with ThreadPoolExecutor(max_workers=A.kapfon_is) as ex:
        isler = [ex.submit(bir, row) for row in H.itertuples(index=False)]
        for no, f in enumerate(as_completed(isler), 1):
            try:
                x = f.result()
            except Exception as hata:
                filog.warning("KAP ek: %s", str(hata)[:150]); continue
            with kilit:
                sonuc.append(x)
                if no % 100 == 0 or no == len(isler):
                    E = pd.concat([E, pd.DataFrame(sonuc)], ignore_index=True).drop_duplicates("indeks", keep="last"); sonuc = []
                    E.to_csv(yol, index=False)
                    filog.info("KAP ek %d/%d rapor, %.0f sn", no, len(isler), time.time() - t0)
    if sonuc:
        E = pd.concat([E, pd.DataFrame(sonuc)], ignore_index=True).drop_duplicates("indeks", keep="last")
    E.to_csv(yol, index=False)
    return E


def fi_k9_ekler_oku(A: FIAyar) -> pd.DataFrame:
    """ekler.csv'yi okur; v1.3 bicimini (PDF yolu) cevirir; mutlak yollari A.kapfon'a goreli yapar (klasor tasinabilir olsun)."""
    yol = os.path.join(A.kapfon, "ekler.csv")
    E = pd.read_csv(yol) if os.path.exists(yol) else pd.DataFrame(columns=["indeks", "dosya", "durum"])
    if len(E) and "durum" not in E.columns:   # v1.3 ekler.csv (PDF yolu) -> v1.5 (metin yolu); eski PDF'ler bir kez metne cevrilir
        E = _fi_k9_eski_ekler(E, os.path.join(A.kapfon, "txt"))
    E["dosya"] = E.dosya.fillna("").astype(str).map(
        lambda s: ";".join(os.path.join("txt", os.path.basename(d)) for d in s.split(";") if d))
    return E


def _fi_k9_yol(d: str, A: FIAyar) -> str:
    """ekler.csv'deki metin yolu (goreli 'txt/...' ya da eski mutlak yol) -> mevcut dosya."""
    for aday in (d, os.path.join(A.kapfon, d), os.path.join(A.kapfon, "txt", os.path.basename(d))):
        if os.path.exists(aday):
            return aday
    raise FileNotFoundError(f"rapor metni yok: {d}")


def _fi_k9_eski_ekler(E: pd.DataFrame, kt: str) -> pd.DataFrame:
    """v1.3 ekler.csv'yi (indeks, PDF yolu) v1.5 bicimine cevirir. Eki olmayan eski kayitlar 'hata' sayilir -> yeniden indirilir."""
    sat = []
    for ind, g in E.groupby(E.indeks.astype(int)):
        yollar = [p for p in g.dosya.dropna().astype(str) if p and os.path.exists(p)]
        txtler = []
        for k, p in enumerate(yollar):
            with open(p, "rb") as f:
                b = f.read()
            txt = os.path.join(kt, f"{ind}__eski_{k}.txt")
            if _fi_metne(b, txt) >= 200:
                txtler.append(txt)
        sat.append({"indeks": ind, "dosya": ";".join(txtler), "durum": "ok" if txtler else "hata"})
    return pd.DataFrame(sat)


def _fi_pdf_metin(dosya: str) -> str:
    """PDF -> duz metin (sutun duzeni korunur). Once pdftotext, yoksa pypdf. Metin dosyasi verilirse oldugu gibi okunur."""
    import subprocess
    if dosya.endswith(".txt"):
        with open(dosya, encoding="utf-8", errors="replace") as f:
            return f.read()
    try:
        return subprocess.run(["pdftotext", "-layout", dosya, "-"], capture_output=True, timeout=60, check=True).stdout.decode("utf-8", "replace")
    except Exception:
        from pypdf import PdfReader
        return "\n".join((p.extract_text(extraction_mode="layout") or "") for p in PdfReader(dosya).pages)


import re as _fi_re
# v1.5 ayristirici. Iki bicim: 'S' = SPK sablonu (III-FON PORTFOY DEGERI TABLOSU, ISIN'li satir; VII-PORTFOYDEN SATISLAR /
# IX-PORTFOYE ALISLAR 'A) HISSE SENETLERI(ALISLAR)' satiri: kod .. gg/aa/yy fiyat deger nominal; Turk sayi bicimi 1.234,56)
# ve 'A' = Atlas bicimi (3- FON PORTFOY DEGERI TABLOSU 'A) HISSE SENETLERI' kod ihracci nominal rayic %; 8-PORTFOYDEN SATISLAR /
# 9- PORTFOYE ALISLAR 'Hisse KOD ihracci g-Aaa-yy nominal tutar'; ABD sayi bicimi 1,234.56). Her bolum raporun kendi TOPLAM
# satiriyla mutabakat yapilir (kontrol); mutabakati tutmayan bolum tabloya 'tutmadi' bayragiyla girer, sonuc hesabinda kullanilmaz.
_FI_TR_NUM = r"-?\d{1,3}(?:\.\d{3})+,\d+|-?\d+,\d+"
_FI_US_NUM = r"-?\d{1,3}(?:,\d{3})+\.\d+|-?\d+\.\d+"
_FI_AYLAR = {"OCA": 1, "ŞUB": 2, "SUB": 2, "MAR": 3, "NİS": 4, "NIS": 4, "MAY": 5, "HAZ": 6, "TEM": 7, "AĞU": 8, "AGU": 8,
             "EYL": 9, "EKİ": 10, "EKI": 10, "KAS": 11, "ARA": 12}
_FI_ISIN = _fi_re.compile(r"\b([A-Z]{2}[A-Z0-9]{9}\d)\b")
_FI_KOD = r"([A-Z][A-Z0-9]{2,5})"


def _fi_sayi(x: str, yerel: str = "tr") -> float:
    x = x.strip()
    return float(x.replace(".", "").replace(",", ".")) if yerel == "tr" else float(x.replace(",", ""))


def _fi_tarih(x: str) -> Optional[str]:
    """gg/aa/yy, gg/aa/yyyy, gg.aa.yyyy, g-Aaa-yy, gg.Aaa.yy -> 'yyyy-aa-gg'."""
    m = _fi_re.match(r"^(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})$", x)
    if m:
        g, a, y = m.groups()
    else:
        m = _fi_re.match(r"^(\d{1,2})[-.]([^\W\d_]{3})[-.](\d{2,4})$", x)
        if not m or m.group(2).upper() not in _FI_AYLAR:
            return None
        g, a, y = m.group(1), str(_FI_AYLAR[m.group(2).upper()]), m.group(3)
    y = ("20" + y) if len(y) == 2 else y
    try:
        return str(pd.Timestamp(int(y), int(a), int(g)).date())
    except Exception:
        return None


def _fi_carpim(sayilar: List[float]) -> Optional[Tuple[float, float, float]]:
    """Uc sayidan fiyat x nominal = deger uclusunu bulur. Once SPK sablon sirasi (fiyat, deger, nominal) denenir; tutmazsa diger
    siralar (fiyat = deger oldugu 1 lotluk islemde sira tahmini yanlis lot uretiyordu: TTRAK 539,30 x 1). Donus (fiyat, deger, nominal)."""
    import itertools
    adaylar = [tuple(sayilar)] + [(a, c, b) for a, b, c in itertools.permutations(sayilar, 3)]   # once sablon sirasi: fiyat deger nominal
    for f, d, n in adaylar:
        if f > 0 and n > 0 and abs(f * n - d) <= max(0.05, 0.005 * abs(d)):
            return f, d, n
    return None


def _fi_esit(a: float, b: float) -> bool:
    return abs(a - b) <= max(1.0, 1e-4 * abs(b))


def fi_k9_ayristir(metin: str) -> Dict[str, Any]:
    """Portfoy dagilim raporu metni -> {'bicim', 'poz', 'islem', 'kontrol'}.
    poz: hisse pozisyonlari (kod, isin, nominal = pay adedi, deger). islem: hisse alis/satislari (kod, yon, tarih, fiyat, deger, lot).
    kontrol: bolum toplamlari ve raporun kendi toplam satirlari (poz_rapor/poz_ayr, alis_rapor/alis_ayr, satis_rapor/satis_ayr).
    Sira: SPK sablonu ('III-'), Atlas ailesi ('3- '), genel ISIN ayristiricisi (bankalarin sirket bicimleri). Pozisyon mutabakati
    tutan ilk ayristiricinin sonucu doner; hicbiri tutmazsa en cok satir bulan (kontrolde 'tutmadi' kalir)."""
    satirlar = metin.splitlines(); U = [s.upper() for s in satirlar]
    us = len(_fi_re.findall(r"\d,\d{3}\.\d\d\b", metin)); tr = len(_fi_re.findall(r"\d\.\d{3},\d\d\b", metin))
    yerel = "us" if us > tr else "tr"
    adaylar = []
    if any(_fi_re.match(r"^\s*III\s*-\s*FON PORTF", u) for u in U):
        adaylar.append(lambda: _fi_k9_spk(satirlar, U, yerel))
    if any(_fi_re.match(r"^\s*\d+\s*-\s*FON PORTF[ÖO]Y DE[ĞG]ER[İI] TABLOSU", u) for u in U):
        adaylar.append(lambda: _fi_k9_atlas(satirlar, U, yerel))
    adaylar.append(lambda: _fi_k9_genel(satirlar, U, yerel))
    sonuc = []
    for f in adaylar:
        r = f()
        if _fi_k9_poz_tuttu(r):
            if sonuc and sonuc[0]["islem"] and not r["islem"]:   # islemler ilk ayristiricida bulunduysa koru
                r = {**r, "islem": sonuc[0]["islem"], "kontrol": {**r["kontrol"], **{k: v for k, v in sonuc[0]["kontrol"].items()
                                                                                     if k.startswith(("alis", "satis", "atlanan"))}}}
            return r
        sonuc.append(r)
    return max(sonuc, key=lambda x: len(x["poz"]))


_FI_KATLA = str.maketrans("İIĞÜŞÖÇ", "IIGUSOC")


def _fi_sayi_belirtec(tok: str, yerel: str) -> Optional[float]:
    """Butun belirtec sayi mi (tarih, yuzde, tamsayi degil)? Turk: 1.234,56 / 12,5; ABD: 1,234.56 / 12.5."""
    if yerel == "tr":
        ok = _fi_re.fullmatch(r"-?\d{1,3}(?:\.\d{3})+,\d+|-?\d+,\d+", tok)
    else:
        ok = _fi_re.fullmatch(r"-?\d{1,3}(?:,\d{3})+\.\d+|-?\d+\.\d+", tok)
    return _fi_sayi(tok, yerel) if ok else None


def _fi_k9_genel(satirlar: List[str], U: List[str], yerel: str) -> Dict[str, Any]:
    """Genel ISIN ayristiricisi: portfoy tablosu ('... PORTFOY DEGERI TABLOSU' -> 'FON TOPLAM DEGER') icinde hisse grubu basligi
    ('A) HISSE SENETLERI', 'A.PAY', 'PAY', 'HISSE TURK') ile bir sonraki grup arasindaki ISIN'li satirlar. Nominal = ISIN'den sonraki
    ilk sayi (yuzde, tarih, tamsayi atlanir). Kod = ISIN'den hemen onceki kod bicimli belirtec, yoksa satirin ilk belirteci
    ('AKBNK.E' -> AKBNK). Mutabakat: iki toplam satiri arasindaki satirlar o toplamin ilk sayisina esit olmali."""
    poz: List[Dict[str, Any]] = []
    k: Dict[str, Any] = {"poz_rapor": np.nan, "poz_ayr": 0.0, "alis_rapor": 0.0, "alis_ayr": 0.0, "satis_rapor": 0.0, "satis_ayr": 0.0,
                         "alis_bolum": False, "satis_bolum": False, "atlanan_islem": 0, "poz_bolum": False, "hisse_baslik": False}
    bolum = False; hisse = False; parca: List[Dict[str, Any]] = []; rapor_t = ayr_t = 0.0; toplam_var = False; tutmayan = 0
    for s, u in zip(satirlar, U):
        f = u.translate(_FI_KATLA)
        if not bolum and "PORTF" in f and "DEGER" in f and "TABLO" in f and "TOPLAM" not in f:
            bolum = True; k["poz_bolum"] = True; continue
        if not bolum and f.strip() == "TABLOSU":                       # 'FON PORTFOY DEGERI' + alt satirda 'TABLOSU'
            bolum = True; k["poz_bolum"] = True; continue
        if bolum and "TOPLAM DEGER" in f and ("TABLO" in f or f.strip().startswith(("IV", "4"))):
            break
        if not bolum:
            continue
        g = f.strip().rstrip(":").strip()
        if _fi_re.fullmatch(r"(?:[A-Z][.)]\s*)?(?:HISSE SENETLERI|HISSE SENEDI|PAY SENETLERI|PAY|HISSE TURK|HISSE)", g):
            hisse = True; k["hisse_baslik"] = True; parca = []; continue
        if not hisse:
            continue
        if _fi_re.match(r"^(?:[B-Z][.)]\s*\S|[B-Z]\.\d)", g) or g in ("HISSE YABANCI",):
            hisse = False; continue
        if _fi_re.search(r"\bTOPLAM", f):
            sayilar = [x for x in (_fi_sayi_belirtec(tok, yerel) for tok in s.split()) if x is not None]
            if parca and sayilar:
                rapor_t += sayilar[0]; a = sum(x["nominal"] for x in parca); ayr_t += a; toplam_var = True
                tutmayan += not _fi_esit(a, sayilar[0]); poz += parca
            parca = []
            if _fi_re.search(r"ANA GRUP|GRUP TOPLAM|^\s*TOPLAM", f):
                hisse = False
            continue
        im = _FI_ISIN.search(s)
        if not im:
            continue
        sayilar = [x for x in (_fi_sayi_belirtec(tok, yerel) for tok in s[im.end():].split()) if x is not None]
        if not sayilar:
            continue
        once = s[:im.start()].split()
        kod = once[-1] if once and _fi_re.fullmatch(r"[A-Z][A-Z0-9]{2,6}", once[-1]) else (once[0].split(".")[0] if once else "")
        parca.append({"kod": kod, "isin": im.group(1), "nominal": sayilar[0], "fiyat": np.nan,
                      "deger": sayilar[1] if len(sayilar) > 1 else np.nan})
    if toplam_var:
        k["poz_rapor"] = rapor_t if tutmayan == 0 else np.nan; k["poz_ayr"] = ayr_t
    return {"bicim": "G", "poz": poz, "islem": [], "kontrol": k}


def _fi_k9_spk(satirlar: List[str], U: List[str], yerel: str = "tr") -> Dict[str, Any]:
    """SPK sablonu (III-FON PORTFOY DEGERI TABLOSU). Is, Istanbul gibi sirketler ayni sablonu ABD sayi bicimiyle basar."""
    N = _FI_TR_NUM if yerel == "tr" else _FI_US_NUM
    num = _fi_re.compile(N)
    poz, islem = [], []
    k: Dict[str, Any] = {"poz_rapor": np.nan, "poz_ayr": 0.0, "alis_rapor": 0.0, "alis_ayr": 0.0, "satis_rapor": 0.0, "satis_ayr": 0.0,
                         "alis_bolum": False, "satis_bolum": False, "atlanan_islem": 0, "poz_bolum": False, "hisse_baslik": False}
    # --- pozisyonlar (III ... IV). Hisse grubu 'Hisse Turk' / 'Hisse Yabanci' alt gruplarina ayrilabilir; her alt grubun satirlari
    # kendi GRUP TOPLAMI satiriyla karsilastirilir (parca = iki toplam satiri arasindaki satirlar). Yabanci alt grup tabloya girmez.
    bolum = False; hisse = False; alt = ""; parca: List[Dict[str, Any]] = []; rapor_t = 0.0; ayr_t = 0.0; toplam_var = False
    yabanci_var = False
    for s, u in zip(satirlar, U):
        if _fi_re.match(r"^\s*III\s*-\s*FON PORTF", u):
            bolum = True; k["poz_bolum"] = True; continue
        if _fi_re.match(r"^\s*IV\s*-", u):
            bolum = False; hisse = False
        if not bolum:
            continue
        if u.strip() in ("HİSSE SENETLERİ", "HISSE SENETLERI", "HİSSE SENETLERİ (TL)"):
            hisse = True; k["hisse_baslik"] = True; continue
        if not hisse:
            continue
        if _fi_re.match(r"^\s*H[İI]SSE\s+YABANCI", u):
            alt = "yabanci"; continue
        if _fi_re.match(r"^\s*H[İI]SSE\s+T[ÜU]RK", u):
            alt = "turk"; continue
        if u.strip().startswith("GRUP TOPLAMI"):
            n = num.findall(s)
            if parca and n:
                if alt != "yabanci":
                    rapor_t += _fi_sayi(n[0], yerel); ayr_t += sum(x["nominal"] for x in parca); poz += parca; toplam_var = True
                else:
                    yabanci_var = True
                parca = []
            if not s.startswith(" "):                       # sutun 0'daki GRUP TOPLAMI = hisse grubunun sonu
                hisse = False
            continue
        m = _fi_re.match(r"^\s*(?:Tem\.\s?Ver\.\s+)?([A-Z][A-Z0-9]{2,7})\b(?!\s+TOPLAM)", s)   # 'Tem.Ver.' = teminattaki pay
        para = _fi_re.match(r"^\s*(?:Tem\.\s?Ver\.\s+)?[A-Z][A-Z0-9]{2,7}\s+(?:TL|TRY|USD|EUR|GBP)\b", s)
        if not _fi_re.search(r"\b\d{2}/\d{2}/\d{2}\b", s) and not para:   # satir = kod/ISIN + alis tarihi ya da kod + doviz
            continue                                                          # (Istanbul: tarih ve ISIN alt satira tasar)
        im = _FI_ISIN.search(s)
        if not m and not (im and not s[:im.start()].strip()):                # kodsuz satir: yalniz ISIN (kod ISIN eslemesinden)
            continue
        n = [_fi_sayi(x, yerel) for x in num.findall(s[(im or m).end():])]   # ISIN bos olabilir (yeni halka arz, GEDZA Ara 2022)
        if not n:
            continue
        fiyat = deger = np.nan
        for j in range(len(n) - 1, 0, -1):          # borsa fiyati x nominal = toplam deger (sondan ara: alis fiyati degil borsa)
            for d in n[j + 1:]:
                if n[j] > 0 and abs(n[0] * n[j] - d) <= max(1.0, 0.005 * abs(d)):
                    fiyat, deger = n[j], d; break
            if not np.isnan(fiyat):
                break
        parca.append({"kod": m.group(1) if m else "", "isin": im.group(1) if im else "", "nominal": n[0], "fiyat": fiyat, "deger": deger})
    if toplam_var:
        k["poz_rapor"] = rapor_t; k["poz_ayr"] = ayr_t
    elif yabanci_var:                                                  # yalniz yabanci hisse tasiyan fon: BIST pozisyonu 0
        k["poz_rapor"] = 0.0; k["poz_ayr"] = 0.0
    # --- islemler (A) HISSE SENETLERI(ALISLAR)/(SATISLAR))
    yon = None
    for s, u in zip(satirlar, U):
        m = _fi_re.search(r"H[İI]SSE SENETLER[İI]\s*\((ALIŞLAR|SATIŞLAR|ALISLAR|SATISLAR)\)", u)
        if m:
            yon = "alis" if m.group(1).startswith("AL") else "satis"; k[f"{yon}_bolum"] = True; continue
        if yon is None:
            continue
        if _fi_re.match(r"^\s*[B-Z]\s?\)", u) or _fi_re.match(r"^\s*(V|VI|VII|VIII|IX|X|XI)\s*-", u):
            if not _fi_re.match(r"^\s*(VII|IX)\s*-\s*PORTF", u):   # sayfa basinda tekrar eden bolum basligi bolumu bitirmez
                yon = None; continue
        if "TOPLAMI:" in u:
            n = num.findall(s)
            if len(n) >= 2:
                k[f"{yon}_rapor"] += _fi_sayi(n[-1], yerel)       # 'Toplami: deger nominal' -> nominal
            continue
        # kod = satirin ilk alani (iki bosluga kadar): BIST kodu, '13X GF', 'ZS US', 'ALTINS1'. BIST disi kodlar mutabakata girer,
        # tabloda kalir; BIST evreni suzgeci sonuc asamasinda.
        r = _fi_re.match(r"^\s*(\S+(?: \S+)?)\s{2,}.*?(\d{2}/\d{2}/\d{2,4})\s+(" + N + r")\s+(" + N + r")\s+("
                         + N + r")\s*$", s)
        if not r:
            if _fi_re.match(r"^\s*\S+.*\d{2}/\d{2}/\d{2}", s):
                k["atlanan_islem"] += 1
            continue
        uc = _fi_carpim([_fi_sayi(r.group(3), yerel), _fi_sayi(r.group(4), yerel), _fi_sayi(r.group(5), yerel)])
        t = _fi_tarih(r.group(2))
        if uc is None or t is None:
            k["atlanan_islem"] += 1; continue
        fiyat, deger, lot = uc
        islem.append({"kod": r.group(1), "yon": yon, "tarih": t, "fiyat": fiyat, "deger": deger, "lot": lot})
        k[f"{yon}_ayr"] += lot
    return {"bicim": "S", "poz": poz, "islem": islem, "kontrol": k}


def _fi_k9_atlas(satirlar: List[str], U: List[str], yerel: str = "us") -> Dict[str, Any]:
    """Atlas ailesi: 2022-25 ABD sayi bicimi, 2026'dan itibaren Turk sayi bicimi ve '04.May.26' tarihi (ayni yerlesim)."""
    num = _FI_US_NUM if yerel == "us" else _FI_TR_NUM
    poz, islem = [], []
    k: Dict[str, Any] = {"poz_rapor": np.nan, "poz_ayr": 0.0, "alis_rapor": 0.0, "alis_ayr": 0.0, "satis_rapor": 0.0, "satis_ayr": 0.0,
                         "alis_bolum": False, "satis_bolum": False, "atlanan_islem": 0, "poz_bolum": False, "hisse_baslik": False}
    bolum = None; hisse = False; son_tur = None; bekleyen = ""
    for s, u in zip(satirlar, U):
        if _fi_re.match(r"^\s*\d+\s*-\s*FON PORTF[ÖO]Y DE[ĞG]ER[İI] TABLOSU", u):
            bolum = "poz"; k["poz_bolum"] = True; continue
        if _fi_re.match(r"^\s*\d+\s*-\s*FON TOPLAM DE", u):
            bolum = None; hisse = False; continue
        if _fi_re.match(r"^\s*\d+\s*-\s*PORTF[ÖO]YDEN SATI", u):
            bolum = "satis"; k["satis_bolum"] = True; son_tur = None; continue
        if _fi_re.match(r"^\s*\d+\s*-\s*PORTF[ÖO]YE ALI", u):
            bolum = "alis"; k["alis_bolum"] = True; son_tur = None; continue
        if bolum in ("alis", "satis") and _fi_re.match(r"^\s*1?\d\s*-\s*[A-ZÇĞİÖŞÜ]", u) and not _fi_re.match(r"^\s*\d+\s*-\s*PORTF", u):
            bolum = None; continue
        if bolum == "poz":
            if _fi_re.match(r"^\s*A\)\s*H[İI]SSE SENETLER", u):
                hisse = True; k["hisse_baslik"] = True; continue
            if hisse and _fi_re.match(r"^\s*[B-Z]\)", u):
                if not poz and np.isnan(k["poz_rapor"]):
                    k["poz_rapor"] = 0.0                            # bos hisse grubu: baslik var, satir yok
                hisse = False; continue
            if hisse and u.strip().startswith("TOPLAM:"):
                n = _fi_re.findall(num, s)
                if n:
                    k["poz_rapor"] = _fi_sayi(n[0], yerel)
                hisse = False; continue
            if hisse:
                girinti = len(s) - len(s.lstrip()); bas = s.split()[0] if s.split() else ""
                kodlu = girinti <= 15 and bool(_fi_re.match(r"^[A-Z0-9][A-Z0-9./-]{1,11}$", bas))   # ihracci devami ~33. sutunda
                m = _fi_re.search(r"(" + num + r")\s+(" + num + r")\s+(?:%(?:" + num + r")|(?:" + num + r")%)\s*$", s)   # %1.76 ya da 1.76%
                if kodlu and not m:
                    bekleyen = bas; continue
                if m and (kodlu or bekleyen):
                    kod = bas if kodlu else bekleyen; bekleyen = ""
                    n0 = _fi_sayi(m.group(1), yerel); d = _fi_sayi(m.group(2), yerel)
                    poz.append({"kod": kod, "isin": kod if _FI_ISIN.fullmatch(kod) else "", "nominal": n0,
                                "fiyat": d / n0 if n0 else np.nan, "deger": d})
                    k["poz_ayr"] += n0
        elif bolum in ("alis", "satis"):
            if u.strip().startswith("TOPLAM:"):
                n = _fi_re.findall(num, s)
                if son_tur == "Hisse" and n:
                    k[f"{bolum}_rapor"] += _fi_sayi(n[0], yerel)
                son_tur = None if n else son_tur
                continue
            r = _fi_re.match(r"^\s*(\S+)\s+" + _FI_KOD + r"\s+.*?(\d{1,2}[-.][^\W\d_]{3}[-.]\d{2,4})\s+(?:\d{1,2}[-.][^\W\d_]{3}[-.]\d{2,4}\s+)?("
                             + num + r")\s+(" + num + r")\s*$", s)
            if r:
                son_tur = r.group(1)
            if r and r.group(1) == "Hisse":
                t = _fi_tarih(r.group(3)); n0 = _fi_sayi(r.group(4), yerel); d = _fi_sayi(r.group(5), yerel)
                if t is None or n0 <= 0:
                    k["atlanan_islem"] += 1; continue
                islem.append({"kod": r.group(2), "yon": bolum, "tarih": t, "fiyat": d / n0, "deger": d, "lot": n0})
                k[f"{bolum}_ayr"] += n0
            elif _fi_re.match(r"^\s*Hisse\s", s):
                k["atlanan_islem"] += 1
    return {"bicim": "A", "poz": poz, "islem": islem, "kontrol": k}


def fi_k9_paketle(A: FIAyar, hedef: str, parca_mb: int = 45) -> Dict[str, Any]:
    """KAP fon verisini tasinabilir pakete yazar (artirimli guncellemenin baslangici): liste, ekler, ayristirilmis tablolar ve
    ham rapor metinleri (tar.xz, GitHub dosya siniri icin parca_mb MB parcalar). manifest.json: her dosyanin boyu ve sha256'si."""
    import gzip, hashlib, json, shutil, subprocess
    os.makedirs(hedef, exist_ok=True)
    E = fi_k9_ekler_oku(A)
    E.to_csv(os.path.join(hedef, "ekler.csv.gz"), index=False)
    with open(os.path.join(A.kapfon, "liste.csv"), "rb") as f, gzip.open(os.path.join(hedef, "liste.csv.gz"), "wb") as g:
        shutil.copyfileobj(f, g)
    for ad in ("liste_haftalar.txt", "k9_pozisyon.csv.gz", "k9_islem.csv.gz", "k9_kontrol.csv.gz"):
        if os.path.exists(os.path.join(A.kapfon, ad)):
            shutil.copy2(os.path.join(A.kapfon, ad), os.path.join(hedef, ad))
    metinler = sorted({d for s in E[E.durum == "ok"].dosya for d in str(s).split(";")
                       if d and os.path.exists(os.path.join(A.kapfon, d))})
    for eski in [f for f in os.listdir(hedef) if f.startswith("metin.tar.xz.")]:
        os.unlink(os.path.join(hedef, eski))
    liste_yol = os.path.join(hedef, "_metin_listesi.txt")
    with open(liste_yol, "w", encoding="utf-8") as f:
        f.write("\n".join(metinler))
    tar = subprocess.Popen(["tar", "-cf", "-", "-C", A.kapfon, "-T", liste_yol], stdout=subprocess.PIPE)
    xz = subprocess.Popen(["xz", "-T0", "-6", "-c"], stdin=tar.stdout, stdout=subprocess.PIPE)
    tar.stdout.close()
    no, boy = 0, parca_mb * 1024 * 1024
    while True:
        blok = xz.stdout.read(boy)
        if not blok:
            break
        with open(os.path.join(hedef, f"metin.tar.xz.{no:03d}"), "wb") as f:
            f.write(blok)
        no += 1
    if xz.wait() != 0 or tar.wait() != 0:
        raise RuntimeError("metin paketi olusturulamadi (tar/xz hatasi)")
    os.unlink(liste_yol)
    man = {"surum": FI_SURUM, "ayristirici": FI_K9_SURUM, "olusturma": str(pd.Timestamp.now()), "metin_sayisi": len(metinler),
           "rapor": int((E.durum == "ok").sum()), "muaf": int((E.durum == "muaf").sum()), "dosyalar": {}}
    for ad in sorted(os.listdir(hedef)):
        if ad == "manifest.json":
            continue
        h = hashlib.sha256()
        with open(os.path.join(hedef, ad), "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        man["dosyalar"][ad] = {"boy": os.path.getsize(os.path.join(hedef, ad)), "sha256": h.hexdigest()}
    with open(os.path.join(hedef, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    filog.info("K9 paket: %d metin, %d parca, %s", len(metinler), no, hedef)
    return man


def fi_k9_paket_ac(kaynak: str, A: FIAyar) -> Dict[str, Any]:
    """fi_k9_paketle paketini A.kapfon'a acar; her dosya once manifest sha256'siyla dogrulanir (bozuk/eksik parca -> durur)."""
    import gzip, hashlib, json, shutil, subprocess
    with open(os.path.join(kaynak, "manifest.json"), encoding="utf-8") as f:
        man = json.load(f)
    for ad, bilgi in man["dosyalar"].items():
        yol = os.path.join(kaynak, ad)
        if not os.path.exists(yol):
            raise FileNotFoundError(f"paket eksik: {ad}")
        h = hashlib.sha256()
        with open(yol, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        if h.hexdigest() != bilgi["sha256"]:
            raise RuntimeError(f"paket bozuk: {ad} (sha256 tutmuyor)")
    os.makedirs(A.kapfon, exist_ok=True)
    for ad in ("liste.csv.gz", "ekler.csv.gz"):
        with gzip.open(os.path.join(kaynak, ad), "rb") as f, open(os.path.join(A.kapfon, ad[:-3]), "wb") as g:
            shutil.copyfileobj(f, g)
    for ad in ("liste_haftalar.txt", "k9_pozisyon.csv.gz", "k9_islem.csv.gz", "k9_kontrol.csv.gz"):
        if ad in man["dosyalar"]:
            shutil.copy2(os.path.join(kaynak, ad), os.path.join(A.kapfon, ad))
    parcalar = sorted(a for a in man["dosyalar"] if a.startswith("metin.tar.xz."))
    xz = subprocess.Popen(["xz", "-d", "-c"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    tar = subprocess.Popen(["tar", "-xf", "-", "-C", A.kapfon], stdin=xz.stdout)
    xz.stdout.close()
    for ad in parcalar:
        with open(os.path.join(kaynak, ad), "rb") as f:
            shutil.copyfileobj(f, xz.stdin)
    xz.stdin.close()
    if xz.wait() != 0 or tar.wait() != 0:
        raise RuntimeError("metin paketi acilamadi (xz/tar hatasi)")
    filog.info("K9 paket acildi: %s -> %s (%d metin)", kaynak, A.kapfon, man["metin_sayisi"])
    return man

# İŞLENMİŞ VERİ PAKETİ (Cemal 26 Eki: 'koy'; yeni oturumda veri yeniden kurulmasın). KAP paketinin (kapfon-veri) eşi: repoda ayrı
# 'islenmis-veri' dalı, main'e birleştirilmez. İçerik fi_k1_veri çıktıları (BIST/ABD düzeltilmiş günlük fiyat sözlükleri) ve K25 fon
# tabloları; her dosya xz ile sıkıştırılıp GitHub sınırı için parca_mb MB parçalara bölünür, manifest.json boy + sha256 tutar.
# Açma: python FON_IZI.py vpac <paket_klasoru> <hedef_klasor>  ->  pickle'lar hedefte, sürücülere V_hazir olarak verilir.
def fi_veri_paketle(kaynak: Dict[str, str], hedef: str, parca_mb: int = 45) -> Dict[str, Any]:
    """kaynak: paket adı -> dosya yolu. Her dosya xz'lenip parçalanır; manifest.json (sürüm, tarih, her parça boy + sha256)."""
    import hashlib, json, subprocess
    os.makedirs(hedef, exist_ok=True)
    for eski in [f for f in os.listdir(hedef) if ".xz." in f or f == "manifest.json"]:
        os.unlink(os.path.join(hedef, eski))
    man: Dict[str, Any] = {"surum": FI_SURUM, "olusturma": str(pd.Timestamp.now()), "veri": {}, "dosyalar": {}}
    boy = parca_mb * 1024 * 1024
    for ad, yol in kaynak.items():
        if not os.path.exists(yol):
            raise FileNotFoundError(f"veri paketi kaynağı yok: {ad} -> {yol}")
        xz = subprocess.Popen(["xz", "-T0", "-6", "-c", yol], stdout=subprocess.PIPE); no = 0
        while True:
            blok = xz.stdout.read(boy)
            if not blok:
                break
            with open(os.path.join(hedef, f"{ad}.xz.{no:03d}"), "wb") as f:
                f.write(blok)
            no += 1
        if xz.wait() != 0:
            raise RuntimeError(f"veri paketi oluşturulamadı: {ad} (xz hatası)")
        man["veri"][ad] = {"kaynak_boy": os.path.getsize(yol), "parca": no}
    for ad in sorted(os.listdir(hedef)):
        if ".xz." in ad:
            h = hashlib.sha256()
            with open(os.path.join(hedef, ad), "rb") as f:
                for b in iter(lambda: f.read(1 << 20), b""):
                    h.update(b)
            man["dosyalar"][ad] = {"boy": os.path.getsize(os.path.join(hedef, ad)), "sha256": h.hexdigest()}
    with open(os.path.join(hedef, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    filog.info("veri paketi: %s -> %s (%d parça)", list(kaynak), hedef, len(man["dosyalar"]))
    return man


def fi_veri_paket_ac(kaynak: str, hedef: str) -> Dict[str, str]:
    """fi_veri_paketle paketini hedefe açar; her parça önce sha256 ile doğrulanır (eksik/bozuk -> durur), açılan dosyanın boyu
    manifestle karşılaştırılır. Dönüş: paket adı -> açılan dosya yolu."""
    import hashlib, json, subprocess
    with open(os.path.join(kaynak, "manifest.json"), encoding="utf-8") as f:
        man = json.load(f)
    for ad, bilgi in man["dosyalar"].items():
        yol = os.path.join(kaynak, ad)
        if not os.path.exists(yol):
            raise FileNotFoundError(f"veri paketi eksik: {ad}")
        h = hashlib.sha256()
        with open(yol, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        if h.hexdigest() != bilgi["sha256"]:
            raise RuntimeError(f"veri paketi bozuk: {ad} (sha256 tutmuyor)")
    os.makedirs(hedef, exist_ok=True); cikan = {}
    for ad, bilgi in man["veri"].items():
        yol = os.path.join(hedef, ad)
        with open(yol, "wb") as g:
            xz = subprocess.Popen(["xz", "-d", "-c"], stdin=subprocess.PIPE, stdout=g)
            for no in range(bilgi["parca"]):
                with open(os.path.join(kaynak, f"{ad}.xz.{no:03d}"), "rb") as f:
                    xz.stdin.write(f.read())
            xz.stdin.close()
            if xz.wait() != 0:
                raise RuntimeError(f"veri paketi açılamadı: {ad} (xz hatası)")
        if os.path.getsize(yol) != bilgi["kaynak_boy"]:
            raise RuntimeError(f"veri paketi boyu tutmuyor: {ad}")
        cikan[ad] = yol
    filog.info("veri paketi açıldı: %s -> %s (%s)", kaynak, hedef, list(cikan))
    return cikan


def fi_k9_tablolar_guncel(L: pd.DataFrame, E: pd.DataFrame, A: FIAyar) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Artirimli ayristirma: A.kapfon'daki k9_pozisyon / k9_islem / k9_kontrol tablolarini okur, yalniz yeni raporlari (ya da
    ayristirici surumu degismis raporlari) ayristirip ekler ve kaydeder. Ham metni olmayan eski rapor tablodan korunur."""
    yollar = {ad: os.path.join(A.kapfon, f"{ad}.csv.gz") for ad in ("k9_pozisyon", "k9_islem", "k9_kontrol")}
    if all(os.path.exists(y) for y in yollar.values()):
        P0 = pd.read_csv(yollar["k9_pozisyon"], low_memory=False); I0 = pd.read_csv(yollar["k9_islem"], low_memory=False)
        K0 = pd.read_csv(yollar["k9_kontrol"], low_memory=False, dtype={"ayristirici": str})
    else:
        P0 = I0 = K0 = pd.DataFrame(columns=["indeks"])
    surum = K0.get("ayristirici", pd.Series(dtype=object)).astype(str)
    gecerli = set(K0.loc[surum == FI_K9_SURUM, "indeks"].astype(int)) if len(K0) else set()
    eski = set(K0.indeks.astype(int)) - gecerli if len(K0) else set()
    metinli = set(E[(E.durum == "ok")].indeks.astype(int))
    yeniden = {i for i in eski if i in metinli and all(
        os.path.exists(os.path.join(A.kapfon, d)) or os.path.exists(d) for d in str(E.set_index("indeks").dosya.get(i, "")).split(";") if d)}
    atla = gecerli | (eski - yeniden)
    t0 = time.time()
    P1, I1, K1 = fi_k9_tablolar(L, E, A, atla=atla)
    cik = set(K1.indeks.astype(int)) if len(K1) else set()
    P = pd.concat([P0[~P0.indeks.astype(int).isin(cik)] if len(P0) else P0, P1], ignore_index=True)
    I = pd.concat([I0[~I0.indeks.astype(int).isin(cik)] if len(I0) else I0, I1], ignore_index=True)
    K = pd.concat([K0[~K0.indeks.astype(int).isin(cik)] if len(K0) else K0, K1], ignore_index=True)
    if len(I):
        I["tarih"] = pd.to_datetime(I.tarih, errors="coerce")
    for ad, x in (("k9_pozisyon", P), ("k9_islem", I), ("k9_kontrol", K)):
        x.to_csv(yollar[ad], index=False)
    filog.info("K9 artirimli: %d yeni/yenilenen rapor ayristirildi (%d eski korundu), %.0f sn", len(cik), len(atla), time.time() - t0)
    return P, I, K


def _fi_k9_poz_tuttu(r: Dict[str, Any]) -> bool:
    """Pozisyon mutabakati: portfoy tablosu bulunmali; hisse basligi yoksa (hisse tasimayan fon) satir da olmamali; baslik varsa
    satir toplami raporun hisse grubu toplamina esit olmali. Taninmayan yerlesim (tablo yok) 'tutmadi' sayilir."""
    k = r["kontrol"]
    if not k.get("poz_bolum", False):
        return False
    if not k.get("hisse_baslik", False):
        return len(r["poz"]) == 0
    return not np.isnan(k["poz_rapor"]) and _fi_esit(k["poz_ayr"], k["poz_rapor"])


def fi_k9_tablolar(L: pd.DataFrame, E: pd.DataFrame, A: FIAyar,
                   atla: Optional[set] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Indirilen raporlari ayristirir. Bir raporun birden fazla eki varsa (TR/EN kopya ya da parca) pozisyon en cok hisse satiri
    bulunan ekten, islemler en cok islem bulunan ekten alinir (toplanmaz -> kopya ek cift sayilmaz).
    Donus: (pozisyonlar, islemler, kontrol) — fon, sirket, donem, yayin bilgisiyle. Mutabakat: poz_tuttu / alis_tuttu / satis_tuttu."""
    meta = L.assign(indeks=L.indeks.astype(int)).drop_duplicates("indeks").set_index("indeks")
    P, I, K = [], [], []
    secili = E[(E.durum == "ok") & E.indeks.astype(int).isin(meta.index)]
    if atla:
        secili = secili[~secili.indeks.astype(int).isin(atla)]
    for row in secili.itertuples(index=False):
        ind = int(row.indeks); m = meta.loc[ind]
        ek = {"indeks": ind, "fon": m.fon, "sirket": str(m.unvan).upper().split(" PORTF")[0], "yil": int(m.yil), "donem": int(m.donem),
              "yayin": m.yayin, "kural": str(m.get("kural", "") or "")}
        try:
            metinler = [_fi_pdf_metin(_fi_k9_yol(d, A)) for d in str(row.dosya).split(";") if d]
            if metinler and all(_fi_muaf(x) for x in metinler):
                K.append({**ek, "muaf": True, "ayristirici": FI_K9_SURUM}); continue
            R = [fi_k9_ayristir(x) for x in metinler]
        except Exception as ex:
            filog.warning("rapor %s ayristirilamadi: %s", ind, ex); K.append({**ek, "hata": str(ex)[:100]}); continue
        if not R:
            continue
        rp = max(R, key=lambda x: len(x["poz"])); ri = max(R, key=lambda x: len(x["islem"]))
        kp, ki = rp["kontrol"], ri["kontrol"]
        kon = {**ek, "ayristirici": FI_K9_SURUM, "bicim": rp["bicim"], "n_poz": len(rp["poz"]), "n_islem": len(ri["islem"]), "poz_rapor": kp["poz_rapor"],
               "poz_ayr": kp["poz_ayr"], "alis_rapor": ki["alis_rapor"], "alis_ayr": ki["alis_ayr"], "satis_rapor": ki["satis_rapor"],
               "satis_ayr": ki["satis_ayr"], "islem_bolum": ki["alis_bolum"] or ki["satis_bolum"], "atlanan_islem": ki["atlanan_islem"]}
        kon["poz_tuttu"] = _fi_k9_poz_tuttu(rp)
        kon["alis_tuttu"] = _fi_esit(ki["alis_ayr"], ki["alis_rapor"]) and not (ki["alis_rapor"] == 0 and ki["atlanan_islem"] > 0)
        kon["satis_tuttu"] = _fi_esit(ki["satis_ayr"], ki["satis_rapor"]) and not (ki["satis_rapor"] == 0 and ki["atlanan_islem"] > 0)
        K.append(kon)
        P += [{**ek, **x, "tuttu": kon["poz_tuttu"]} for x in rp["poz"]]
        I += [{**ek, **x, "tuttu": kon[f"{x['yon']}_tuttu"]} for x in ri["islem"]]
    P = pd.DataFrame(P); I = pd.DataFrame(I); K = pd.DataFrame(K)
    if len(I):
        I["tarih"] = pd.to_datetime(I.tarih, errors="coerce")
    return P, I, K


# ---------------------------------------------------------------- K10 fon girisi testi + K11 fon defteri (v1.5)
# CEMAL (23 Eki): "Iz illaki var; hangi gun kac lot alinmis, dolasimdaki lot, hacim; didik didik yapsan bulursun."
# Kaynak: KAP aylik portfoy dagilim raporlari (K9). Bilgi ani = raporun KAP yayin zamani; giris = yayin gununden SONRAKI ilk islem
# gununun acilisi (gun ici yayin da ertesi acilis: temkinli, gelecege bakmaz). Olay: fon f, ay m raporunda hissede pozisyon var,
# m-1 raporunda yok (iki rapor da mutabakattan gecmis). Ayni hissede 60 islem gunu icinde bir olay.
FI_K10_ESIK = {"buyuk": 0.03, "artis": 0.50}   # buyuk giris: fonun hisse portfoyunun >= %3'u; toplu artis: fonlarin toplam payi +%50


def fi_k10_pozisyon(P: pd.DataFrame, K: pd.DataFrame, evren: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Mutabakati tutan raporlardan (fon, ay, kod) nominal/deger tablosu ve fon-ay kapsami. Kodsuz satir ISIN eslemesiyle,
    evrende olmayan eski kod (unvan degisikligi) ayni ISIN'in evrendeki koduyla doldurulur."""
    K = K[K.get("poz_tuttu", False) == True].copy()   # noqa: E712
    kural = K.get("kural", pd.Series("", index=K.index)).fillna("").astype(str)
    aylik = (kural.str.contains("Ay") | (kural == "")) & K.donem.astype(int).between(1, 12)   # tasfiyedeki fonlarin haftalik raporlari disari
    K = K[aylik].copy()
    K["ay"] = K.yil.astype(int) * 12 + K.donem.astype(int) - 1
    K["bilinme"] = pd.to_datetime(K.yayin, format="%d.%m.%Y %H:%M:%S", errors="coerce")
    yay_ay = K.bilinme.dt.year * 12 + K.bilinme.dt.month - 1
    tutarsiz = (K.ay >= yay_ay) | (K.ay < yay_ay - 13)                # KAP yil/donem alani hatali (or. 2028 yili)
    if tutarsiz.any():
        filog.warning("K10: donemi yayin tarihiyle tutarsiz %d rapor atildi", int(tutarsiz.sum()))
    K = K[~tutarsiz]
    K = K.sort_values("indeks").drop_duplicates(["fon", "ay"], keep="last")
    P = P[P.indeks.isin(K.indeks)].copy()
    P["kod"] = P.kod.astype(str).str.strip().str.upper(); P["isin"] = P["isin"].fillna("").astype(str)
    ev = set(evren)
    es = P[(P["isin"] != "") & P.kod.isin(ev)].groupby("isin").kod.agg(lambda x: x.value_counts().index[0])
    eksik = (~P.kod.isin(ev)) & P["isin"].isin(es.index)
    P.loc[eksik, "kod"] = P.loc[eksik, "isin"].map(es)
    P = P[P.kod.isin(ev)]
    G = P.groupby(["indeks", "kod"], as_index=False).agg(nominal=("nominal", "sum"), deger=("deger", "sum"))
    G = G.merge(K[["indeks", "fon", "sirket", "ay", "bilinme"]], on="indeks")
    G = G[G.nominal > 0]
    top = G.groupby("indeks").deger.transform("sum")
    G["agirlik"] = G.deger / top.where(top > 0)
    return G, K[["indeks", "fon", "sirket", "ay", "bilinme"]]


def fi_k10_olaylar(G: pd.DataFrame, KP: pd.DataFrame, oran: Optional[pd.DataFrame] = None,
                   dol: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Fon bazinda giris olaylari ve hisse-ay bazinda toplu ozellikler. Donus: her (kod, fon, ay) girisi; sutunlar:
    ilk (onceki ay kapsanan hicbir fonda yok), cok (ayni ay >= 2 fon girdi; bilinme = 2. fonun yayini), buyuk, artis, tasfiye.
    Ek olaylar: cikis (fon pozisyonu kapatti); oran (kod, ay, oran = ham/duzeltilmis kapanis) ve dol (kod, dolasim_lot) verilirse
    yogun5 / yogun10 = iki ayi da raporlu fonlarin toplam payi sermayenin %5 / %10'unu ilk kez asti (bilinme = o ay o hisseyi
    tasiyan fon raporlarinin en gec yayini; sermaye bugunku deger, eski lotlar bolunme oraniyla bugune cevrilir)."""
    kap = KP.set_index(["fon", "ay"]).bilinme
    var = set(zip(KP.fon, KP.ay))
    onceki = G.assign(ay=G.ay + 1)[["fon", "ay", "kod", "nominal"]].rename(columns={"nominal": "nom_once"})
    X = G.merge(onceki, on=["fon", "ay", "kod"], how="left")
    X["kapsam"] = [(f, a - 1) in var for f, a in zip(X.fon, X.ay)]
    E = X[X.kapsam & X.nom_once.isna()].copy()                       # giris: bu ay var, gecen ay (rapor var) yok
    E["bilinme"] = [kap.get((f, a), pd.NaT) for f, a in zip(E.fon, E.ay)]   # bilgi ani = bu ayin raporunun yayini
    # hisse-ay toplu: iki ay da raporu olan fonlarda toplam nominal ve onceki ay sahip sayisi.
    # v1.6 (denetim 24 Eki): yalniz olayin bilinme anina kadar YAYIMLANMIS bu ay raporlari sayilir (eskiden o ayin butun
    # raporlari; 34.643 giris olayinin 31.095'inde toplamda henuz yayimlanmamis rapor vardi, 905 'artis' o an bilinemezdi).
    ikili = KP[[(f, a - 1) in var for f, a in zip(KP.fon, KP.ay)]][["fon", "ay", "bilinme"]].rename(columns={"bilinme": "bil_m"})
    E = E.reset_index(drop=True)
    ev_ = E[["kod", "ay", "bilinme"]].reset_index().rename(columns={"index": "_e"})
    def _pit(T: pd.DataFrame) -> pd.DataFrame:
        x = ev_.merge(T, on=["kod", "ay"], how="inner")
        return x[x.bil_m <= x.bilinme]
    xs = _pit(G[["fon", "ay", "kod", "nominal"]].merge(ikili, on=["fon", "ay"]))
    xg = _pit(G[["fon", "ay", "kod", "nominal"]].assign(ay=G.ay + 1).merge(ikili, on=["fon", "ay"]))
    E["top_simdi"] = xs.groupby("_e").nominal.sum().reindex(E.index, fill_value=0.0).to_numpy()
    E["top_gecen"] = xg.groupby("_e").nominal.sum().reindex(E.index, fill_value=0.0).to_numpy()
    E["sahip_gecen"] = xg.groupby("_e").fon.nunique().reindex(E.index, fill_value=0).to_numpy()
    # yogun5/10 icin hisse-ay toplami (o ayin butun raporlari; bilinme = en gec rapor -> o an bilinir)
    ikili2 = ikili[["fon", "ay"]]
    simdi = G.merge(ikili2, on=["fon", "ay"]).groupby(["kod", "ay"]).nominal.sum().rename("top_simdi")
    gecen = G.assign(ay=G.ay + 1).merge(ikili2, on=["fon", "ay"]).groupby(["kod", "ay"]).nominal.sum().rename("top_gecen")
    T = pd.concat([simdi, gecen], axis=1).fillna(0).reset_index()
    E["ilk"] = E.sahip_gecen.fillna(0) == 0
    E["artis"] = (E.top_simdi / E.top_gecen.where(E.top_gecen > 0)).fillna(np.inf) - 1 >= FI_K10_ESIK["artis"]
    E["buyuk"] = E.agirlik >= FI_K10_ESIK["buyuk"]
    E["tasfiye"] = E.sirket.astype(str).str.upper().str.match(FI_TASFIYE_RE)    # denetim 24 Eki: alt dizgi 'MUTLAK GETIRI HEDEFLI' fonlarini da yakaliyordu
    E = E.sort_values("bilinme")
    E["sira"] = E.groupby(["kod", "ay"]).cumcount() + 1               # ayni hisseye o ay kacinci giren fon
    E["cok"] = E.sira == 2                                             # ikinci fonun raporu yayimlandiginda bilinir
    E["ilk"] = E.ilk & (E.sira == 1)
    E["tur"] = "giris"
    # cikis: gecen ay pozisyon var, bu ay (rapor var) yok -> bu ayin yayininda bilinir
    C = G.assign(ay=G.ay + 1)[["fon", "sirket", "ay", "kod", "nominal", "agirlik"]]
    C = C[[(f, a) in var for f, a in zip(C.fon, C.ay)]]
    C = C.merge(G[["fon", "ay", "kod"]].assign(_v=1), on=["fon", "ay", "kod"], how="left")
    C = C[C._v.isna()].drop(columns="_v")
    C["bilinme"] = [kap.get((f, a), pd.NaT) for f, a in zip(C.fon, C.ay)]
    C["tur"] = "cikis"; C["cikis"] = True
    E["cikis"] = False
    parcalar = [E, C]
    if oran is not None and dol is not None and len(T):
        Y = T.merge(dol[["kod", "sermaye_lot"]], on="kod").merge(oran, on=["kod", "ay"], how="left")
        Y = Y.merge(oran.assign(ay=oran.ay + 1).rename(columns={"oran": "oran_gecen"}), on=["kod", "ay"], how="left")
        Y["pay"] = Y.top_simdi * Y.oran / Y.sermaye_lot; Y["pay_gecen"] = Y.top_gecen * Y.oran_gecen / Y.sermaye_lot
        son = G.groupby(["kod", "ay"]).bilinme.max().rename("bilinme") if "bilinme" in G else \
            G.merge(KP, on=["fon", "ay"]).groupby(["kod", "ay"]).bilinme.max().rename("bilinme")
        Y = Y.join(son, on=["kod", "ay"])
        for esik in (0.05, 0.10):
            y = Y[(Y.pay >= esik) & (Y.pay_gecen < esik)].copy()
            y["tur"] = f"yogun{int(esik * 100)}"; y[f"yogun{int(esik * 100)}"] = True
            parcalar.append(y[["kod", "ay", "bilinme", "tur", f"yogun{int(esik * 100)}", "pay", "pay_gecen"]])
    return pd.concat(parcalar, ignore_index=True).sort_values("bilinme").reset_index(drop=True)


def _fi_k10_cikis(o: np.ndarray, h: np.ndarray, l: np.ndarray, c: np.ndarray, sma: np.ndarray, e: int,
                  ufuk: int = 120, hedef: float = 0.20, maliyet: float = 0.08) -> Tuple[float, int]:
    """Uretim cikisi (takip T10 + trail): giris o[e]; +%8 onceki barlarda goruldukten sonra Low <= giris -> 0 (maliyet);
    +%20 goruldukten sonra kapanis < SMA20 -> sat (trail, ufuk uygulanmaz); 120 bar dolunca kapanis. Veri biterse NaN
    (trail'deyse son kapanis). Donus (getiri, cikis bari)."""
    g = o[e]; n = len(c); hg = False; mal = False
    if not (g > 0):
        return np.nan, e
    j = e
    while j < n:
        if mal and l[j] <= g:
            return 0.0, j
        if h[j] >= g * (1 + hedef):
            hg = True
        if hg and c[j] < sma[j]:
            return c[j] / g - 1, j
        if not hg and j >= e + ufuk - 1:
            return c[j] / g - 1, j
        if h[j] >= g * (1 + maliyet):
            mal = True
        j += 1
    return (c[-1] / g - 1, n - 1) if hg else (np.nan, n - 1)


def fi_k10_sonuc(V: Dict[str, pd.DataFrame], kodlar: pd.Series, gunler: pd.Series) -> pd.DataFrame:
    """Her (kod, bilgi gunu) icin: giris = sonraki islem gununun acilisi. k20 = 60 barda once +%20 (High) mi -%10 (Low) mu;
    dus = 60 barda once -%20 mi +%20 mi; r60 = 60. bar kapanisi / giris; trail = uretim cikisi getirisi (-%0,4 maliyet);
    on60 = bilgi gunune kadar 60 bar getiri; lik60 = 60 bar medyan TL hacim; giris tarihi."""
    out = []
    for kod, idx in pd.Series(range(len(kodlar)), index=kodlar.values).groupby(level=0):
        d = V.get(kod)
        if d is None:
            continue
        o = d.Open.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float); c = d.Close.to_numpy(float)
        sma = pd.Series(c).rolling(20).mean().to_numpy(); tl = pd.Series(c * d.Volume.to_numpy(float)).rolling(60).median().to_numpy()
        tar = d.index.to_numpy(); n = len(c)
        for i in idx.values:
            g = pd.Timestamp(gunler.iloc[i]).normalize()
            e = int(np.searchsorted(tar, np.datetime64(g + pd.Timedelta(days=1)), side="left"))
            if e >= n or e < 61:
                continue
            gi = o[e]; r = {"i": i, "giris": pd.Timestamp(tar[e]), "on60": c[e - 1] / c[e - 61] - 1, "lik60": tl[e - 1]}
            if e + 60 <= n:
                hw = h[e:e + 60]; lw = l[e:e + 60]
                iu = np.argmax(hw >= gi * 1.2) if (hw >= gi * 1.2).any() else 99
                ia = np.argmax(lw <= gi * 0.9) if (lw <= gi * 0.9).any() else 99
                ia2 = np.argmax(lw <= gi * 0.8) if (lw <= gi * 0.8).any() else 99
                r["k20"] = float(iu < ia); r["dus"] = float(ia2 < iu or (ia2 == iu and ia2 < 99))
                r["r60"] = c[e + 59] / gi - 1
            t, j = _fi_k10_cikis(o, h, l, c, sma, e)
            r["trail"] = t - 0.004 if not np.isnan(t) else np.nan; r["cikis_tarih"] = pd.Timestamp(tar[j])
            out.append(r)
    R = pd.DataFrame(out)
    return R.set_index("i").sort_index() if len(R) else R


def fi_k10_taban(V: Dict[str, pd.DataFrame], bas: str, bit: str, adim: int = 5) -> pd.DataFrame:
    """Taban: her hissenin her 5. islem gunu (bilgi gunu), ayni giris/sonuc mekanigi."""
    kod, gun = [], []
    for s, d in V.items():
        t = d.index[(d.index >= bas) & (d.index <= bit)][::adim]
        kod += [s] * len(t); gun += list(t)
    B = pd.DataFrame({"kod": kod, "bilgi": gun})
    R = fi_k10_sonuc(V, B.kod, B.bilgi)
    return B.join(R, how="inner")


def _fi_k10_hucre(D: pd.DataFrame, ref: pd.DataFrame) -> pd.Series:
    """Eslesme hucresi: giris ayi x on60 besligi x lik60 uclusu. Sinirlar referansin (taban) o ayki dagilimindan."""
    ay = D.giris.dt.to_period("M").astype(str); ray = ref.giris.dt.to_period("M").astype(str)
    out = pd.Series("", index=D.index, dtype=object)
    for a, idx in D.groupby(ay).groups.items():
        r = ref[ray == a]
        if len(r) < 30:
            continue
        qs = np.nanquantile(r.on60, [0.2, 0.4, 0.6, 0.8]); ts = np.nanquantile(r.lik60, [1 / 3, 2 / 3])
        x = D.loc[idx]
        out.loc[idx] = [f"{a}_{int(np.searchsorted(qs, o))}_{int(np.searchsorted(ts, v))}" for o, v in zip(x.on60, x.lik60)]
    return out


FI_K10_VARYANT = {"giris": "tur_giris", "ilk": "ilk", "cok": "cok", "buyuk": "buyuk", "artis": "artis", "tasfiye": "tasfiye",
                  "cikis": "cikis", "yogun5": "yogun5", "yogun10": "yogun10"}


def fi_k10_ozet(E: pd.DataFrame, B: pd.DataFrame, tekrar: int = 60, slot: int = 30, rastgele: int = 20,
                tohum: int = 7) -> pd.DataFrame:
    """Varyant x donem: n, k20/dus orani ve taban (her 5. gun) ile esli taban (ayni ay, ayni momentum besligi, ayni likidite
    uclusu) katlari, r60 ve trail ortalama/medyan, 30 slot portfoy (sabit pay, bilesiksiz) ve ayni sayida rastgele taban isleminin
    medyani. Varyant olaylari hisse basina 60 islem gununde bir (ilk olay)."""
    rng = np.random.default_rng(tohum)
    B = B.copy(); B["donem"] = np.where(B.giris.dt.year <= 2023, "2023", "2024-26"); B["hucre"] = _fi_k10_hucre(B, B)
    sat = []
    for ad, kol in FI_K10_VARYANT.items():
        if kol not in E:
            continue
        X = E[E[kol].fillna(False).astype(bool)]
        X = X.dropna(subset=["giris"]).sort_values("giris")
        tut, son = [], {}
        for r in X.itertuples():
            if r.kod in son and (r.giris - son[r.kod]).days < tekrar * 1.45:
                continue
            son[r.kod] = r.giris; tut.append(r.Index)
        X = X.loc[tut].copy()
        X["donem"] = np.where(X.giris.dt.year <= 2023, "2023", "2024-26")
        if len(X):
            X["hucre"] = _fi_k10_hucre(X, B)
        for dn in ("2023", "2024-26"):
            x = X[X.donem == dn]; b = B[B.donem == dn]
            if len(x) == 0:
                continue
            satir = {"varyant": ad, "donem": dn, "n": len(x), "hisse": x.kod.nunique()}
            hb = b.groupby("hucre")[["k20", "dus", "r60", "trail"]].mean()
            for m in ("k20", "dus"):
                xv = x[m].dropna(); bv = b[m].dropna()
                es = hb[m].reindex(x.loc[xv.index, "hucre"]).dropna()
                satir[m] = xv.mean(); satir[f"{m}_taban"] = bv.mean(); satir[f"{m}_kat"] = xv.mean() / bv.mean() if bv.mean() else np.nan
                satir[f"{m}_esli"] = es.mean(); satir[f"{m}_kat_esli"] = xv.mean() / es.mean() if len(es) and es.mean() else np.nan
            for m in ("r60", "trail"):
                xv = x[m].dropna(); es = hb[m].reindex(x.loc[xv.index, "hucre"]).dropna()
                satir[f"{m}_ort"] = xv.mean(); satir[f"{m}_med"] = xv.median(); satir[f"{m}_taban_ort"] = b[m].mean()
                satir[f"{m}_esli_ort"] = es.mean()
            satir["slot"] = _fi_k10_slot(x, slot)
            bt = b.dropna(subset=["trail"])
            sl = [_fi_k10_slot(bt.iloc[np.sort(rng.choice(len(bt), size=min(len(x), len(bt)), replace=False))], slot)
                  for _ in range(rastgele)] if len(bt) else [np.nan]
            satir["slot_rastgele"] = float(np.nanmedian(sl))
            sat.append(satir)
    return pd.DataFrame(sat)


def _fi_k10_slot(X: pd.DataFrame, slot: int) -> float:
    """30 slot, her islem sermayenin 1/30'u, bilesiksiz; slot cikis gunu bosalir, doluysa yeni islem atlanir. Donus: toplam getiri (%)."""
    X = X.dropna(subset=["trail"]).sort_values("giris")
    acik: List[pd.Timestamp] = []; top = 0.0
    for r in X.itertuples():
        acik = [t for t in acik if t >= r.giris]
        if len(acik) >= slot:
            continue
        acik.append(r.cikis_tarih); top += r.trail / slot
    return 100 * top


def fi_k11_defter(I: pd.DataFrame, G: pd.DataFrame, V: Dict[str, pd.DataFrame], kos: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Fon hisselerinde (FON_HISSE) gun gun fon islemleri: borsa hacmi (lot), raporlu fonlarin aldigi/sattigi lot, hacim payi, faz.
    Aylik: raporlu fonlarin toplam pozisyonu (lot). Donus: (gunluk defter, faz ozeti)."""
    I = I[(I.tuttu == True) & I.kod.isin(FON_HISSE)].copy()   # noqa: E712
    I["tarih"] = pd.to_datetime(I.tarih)
    gun = I.pivot_table(index=["kod", "tarih"], columns="yon", values="lot", aggfunc="sum").fillna(0).reset_index()
    gun = gun.rename(columns={"alis": "fon_alis", "satis": "fon_satis"})
    for c in ("fon_alis", "fon_satis"):
        if c not in gun:
            gun[c] = 0.0
    tutar = I.assign(t=I.deger).pivot_table(index=["kod", "tarih"], columns="yon", values="t", aggfunc="sum").fillna(0)
    gun = gun.merge(tutar.rename(columns={"alis": "alis_tl", "satis": "satis_tl"}).reset_index(), on=["kod", "tarih"], how="left")
    sat = []
    for s in FON_HISSE:
        d = V.get(s)
        if d is None:
            continue
        g = gun[gun.kod == s].set_index("tarih").reindex(d.index).fillna({"fon_alis": 0, "fon_satis": 0})
        g["kod"] = s; g["hacim"] = d.Volume; g["kapanis"] = d.Close
        k = kos[kos.sembol == s]
        if len(k):
            dip, x2, tepe = (pd.Timestamp(k.iloc[0][c]) for c in ("dip", "x2", "tepe"))
            g["faz"] = np.select([g.index < dip, g.index < x2, g.index <= tepe], ["ONCE", "ERKEN", "KOSU"], "COKUS")
        else:
            g["faz"] = ""
        g.index.name = "tarih"; sat.append(g.reset_index())
    D = pd.concat(sat, ignore_index=True) if sat else pd.DataFrame()
    if len(D):
        D["fon_net"] = D.fon_alis - D.fon_satis
        D["fon_hacim_payi"] = (D.fon_alis + D.fon_satis) / D.hacim.where(D.hacim > 0)
        D = D[D.tarih >= I.tarih.min() - pd.Timedelta(days=31)] if len(I) else D
    Z = D.groupby(["kod", "faz"]).agg(gun=("tarih", "size"), islem_gunu=("fon_alis", lambda x: int((x > 0).sum())),
                                      alis_lot=("fon_alis", "sum"), satis_lot=("fon_satis", "sum"), hacim_lot=("hacim", "sum"),
                                      alis_tl=("alis_tl", "sum")).reset_index() if len(D) else pd.DataFrame()
    if len(Z):
        Z["alis_hacim_payi"] = Z.alis_lot / Z.hacim_lot.where(Z.hacim_lot > 0)
        Z["ort_alis_fiyat"] = Z.alis_tl / Z.alis_lot.where(Z.alis_lot > 0)
    return D, Z


def fi_k10_oran(V: Dict[str, pd.DataFrame], ham: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Ay sonu ham kapanis / bolunme duzeltilmis kapanis: eski lot x oran = bugunku paya esdeger lot (bedelsiz sonrasi)."""
    sat = []
    for s, d in V.items():
        h = ham.get(s)
        if h is None:
            continue
        o = (h.Close.reindex(d.index).ffill() / d.Close).replace([np.inf, -np.inf], np.nan)
        m = o.groupby(d.index.year * 12 + d.index.month - 1).last()
        sat.append(pd.DataFrame({"kod": s, "ay": m.index.astype(int), "oran": m.to_numpy()}))
    return pd.concat(sat, ignore_index=True) if sat else pd.DataFrame(columns=["kod", "ay", "oran"])


def fi_isy_dolasim(yol: str) -> pd.DataFrame:
    """Is Yatirim 'Temel Degerler ve Oranlar' sayfasi (kaydedilmis HTML) -> kod, halka aciklik (%), sermaye (lot), fiili dolasim (lot).
    Degerler sayfanin alindigi gunun (bugunun) degerleridir; gecmis aylarda bedelsiz/bedelli oncesi sermaye daha kucuktu."""
    import io
    with open(yol, encoding="utf-8") as f:
        T = pd.read_html(io.StringIO(f.read()), decimal=",", thousands=".")
    T = next(t for t in T if "Halka Açıklık Oranı (%)" in t.columns)
    T = T.rename(columns={"Kod": "kod", "Halka Açıklık Oranı (%)": "hao", "Sermaye (mn TL)": "sermaye_mn"})[["kod", "hao", "sermaye_mn"]]
    T["sermaye_lot"] = T.sermaye_mn * 1e6; T["dolasim_lot"] = T.sermaye_lot * T.hao / 100
    return T


def fi_k11_aylik(G: pd.DataFrame, V: Dict[str, pd.DataFrame], ham: Dict[str, pd.DataFrame], kos: pd.DataFrame,
                 dol: Optional[pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Fon hisselerinde ay ay raporlu tasfiye fonlarinin toplam pozisyonu; pay = sermayeye (KAP %5 esik tanimi) ve halka aciklik
    oranina gore (Is Yatirim; MKK fiili dolasimi degil, pay %100'u asabilir). Lotlar bolunme/bedelsiz etkisinden arindirilir:
    duz_lot = lot x (ham kapanis / duzeltilmis kapanis) ay sonunda -> aylar arasi fark gercek alim/satim. Ay ici borsa hacmi
    (duzeltilmis) ile oranlanir: |fark| / hacim > 1 ise alim borsa emir defterinden daha buyuk -> blok/halka arz/borsa disi devir.
    Donus: (aylik tablo, hisse ozeti: fazlara gore birikim, ilk %5 / %20 dolasim payi ayi ve o gunku fiyat / dip)."""
    sat = []
    for s in FON_HISSE:
        g = G[G.kod == s]; d = V.get(s); h = ham.get(s)
        if d is None or h is None or g.empty:
            continue
        ay = g.groupby("ay").agg(lot=("nominal", "sum"), fon_sayisi=("fon", "nunique"), deger=("deger", "sum"))
        tasf = g[g.sirket.astype(str).str.upper().str.match(FI_TASFIYE_RE)].groupby("ay").nominal.sum()
        ay["tasfiye_lot"] = tasf.reindex(ay.index).fillna(0)
        oran = (h.Close.reindex(d.index).ffill() / d.Close).replace([np.inf, -np.inf], np.nan)
        dm = pd.DataFrame({"kapanis": d.Close, "hacim": d.Volume, "oran": oran})
        dm["ay"] = dm.index.year * 12 + dm.index.month - 1
        am = dm.groupby("ay").agg(kapanis=("kapanis", "last"), hacim=("hacim", "sum"), oran=("oran", "last"), son=("kapanis", lambda x: x.index[-1]))
        ay = ay.join(am, how="left")
        ay["duz_lot"] = ay.lot * ay.oran; ay["duz_tasfiye"] = ay.tasfiye_lot * ay.oran
        ay["fark"] = ay.duz_lot.diff(); ay["fark_hacim"] = ay.fark / ay.hacim.where(ay.hacim > 0)
        k = kos[kos.sembol == s]
        if len(k):
            dip, x2, tepe = (pd.Timestamp(k.iloc[0][c]) for c in ("dip", "x2", "tepe"))
            ay["faz"] = np.select([ay.son < dip, ay.son < x2, ay.son <= tepe], ["ONCE", "ERKEN", "KOSU"], "COKUS")
            ay["fiyat_dip"] = ay.kapanis / d.Close.loc[dip] if dip in d.index else np.nan
        else:
            ay["faz"] = ""; ay["fiyat_dip"] = np.nan
        if dol is not None and s in set(dol.kod):
            r = dol[dol.kod == s].iloc[0]
            # v1.6 (denetim): duz_tasfiye zaten bugunku pay tabaninda; ek oran bolmesi kaldirildi (fi_k10_olaylar ile ayni formul)
            ay["pay_sermaye"] = ay.duz_tasfiye / r.sermaye_lot if r.sermaye_lot > 0 else np.nan
            ay["pay_halka_acik"] = ay.duz_tasfiye / r.dolasim_lot if r.dolasim_lot > 0 else np.nan
        else:
            ay["pay_sermaye"] = ay["pay_halka_acik"] = np.nan
        ay["kod"] = s; sat.append(ay.reset_index())
    M = pd.concat(sat, ignore_index=True) if sat else pd.DataFrame()
    oz = []
    for s, a in (M.groupby("kod") if len(M) else []):
        r: Dict[str, Any] = {"kod": s, "ilk_ay": a.ay.min(), "en_cok_pay_sermaye": a.pay_sermaye.max(),
                             "en_cok_pay_halka_acik": a.pay_halka_acik.max()}
        for esik in (0.05, 0.20):
            x = a[a.pay_sermaye >= esik]
            r[f"pay{int(esik * 100)}_ay"] = x.ay.iloc[0] if len(x) else np.nan
            r[f"pay{int(esik * 100)}_faz"] = x.faz.iloc[0] if len(x) else ""
            r[f"pay{int(esik * 100)}_fiyat_dip"] = x.fiyat_dip.iloc[0] if len(x) else np.nan
        for fz in ("ONCE", "ERKEN", "KOSU", "COKUS"):
            r[f"alim_{fz}"] = a.loc[a.faz == fz, "fark"].clip(lower=0).sum()
        top = sum(r[f"alim_{fz}"] for fz in ("ONCE", "ERKEN", "KOSU", "COKUS"))
        for fz in ("ONCE", "ERKEN", "KOSU", "COKUS"):
            r[f"alim_{fz}_yzd"] = r[f"alim_{fz}"] / top if top > 0 else np.nan
        r["hacimden_buyuk_ay"] = int((a.fark_hacim > 1).sum()); r["alim_ay"] = int((a.fark > 0).sum())
        oz.append(r)
    Z = pd.DataFrame(oz)
    if len(M):
        M["ay"] = [f"{x // 12}-{x % 12 + 1:02d}" for x in M.ay]
    for c in ("ilk_ay", "pay5_ay", "pay20_ay"):
        if c in Z:
            Z[c] = [f"{int(x) // 12}-{int(x) % 12 + 1:02d}" if pd.notna(x) else "" for x in Z[c]]
    return M, Z


def fi_k11_grafik(MA: pd.DataFrame, D: pd.DataFrame, V: Dict[str, pd.DataFrame], kos: pd.DataFrame, yol: str) -> int:
    """Fon hisseleri vaka PDF'i: duzeltilmis fiyat (log), fazlar (ONCE/ERKEN/KOSU/COKUS), raporlu tasfiye fonlarinin sermaye payi
    (ay sonu, basamak) ve raporda gun gun gorunen fon alim/satim gunleri. Donus: sayfa sayisi."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    renk = {"ONCE": "#e8eef7", "ERKEN": "#e6f4ea", "KOSU": "#fff4d6", "COKUS": "#fbe3e3"}
    sayfa = 0
    with PdfPages(yol) as pdf:
        for s in [x for x in FON_HISSE if x in set(MA.kod)]:
            d = V.get(s)
            if d is None:
                continue
            a = MA[MA.kod == s].copy(); a["t"] = pd.to_datetime(a.ay + "-01") + pd.offsets.MonthEnd(0)
            bas = min(a.t.min() - pd.Timedelta(days=120), d.index.max() - pd.Timedelta(days=900)); d = d[d.index >= bas]
            fig, ax = plt.subplots(figsize=(11.7, 6.2)); ax2 = ax.twinx()
            k = kos[kos.sembol == s]
            if len(k):
                dip, x2, tepe = (pd.Timestamp(k.iloc[0][c]) for c in ("dip", "x2", "tepe"))
                for (b, e, f) in ((d.index.min(), dip, "ONCE"), (dip, x2, "ERKEN"), (x2, tepe, "KOSU"), (tepe, d.index.max(), "COKUS")):
                    ax.axvspan(b, e, color=renk[f], zorder=0); ax.text(b, 0.97, " " + f, transform=ax.get_xaxis_transform(), fontsize=8, va="top")
            ax.semilogy(d.index, d.Close, color="#1f2a44", lw=1.1, zorder=3); ax.set_ylabel("fiyat (log, bolunme duzeltilmis)")
            ps = a.set_index("t").pay_sermaye.fillna(0)
            ps = ps.reindex(pd.date_range(ps.index.min(), ps.index.max(), freq="ME"), fill_value=0.0)   # raporda yoksa pay 0
            ax2.step(ps.index, 100 * ps.to_numpy(), where="post", color="#c0392b", lw=1.6, zorder=4)
            ax2.set_ylabel("raporlu tasfiye fonlarinin sermaye payi %", color="#c0392b"); ax2.set_ylim(bottom=0)
            g = D[(D.kod == s) & ((D.fon_alis > 0) | (D.fon_satis > 0))] if len(D) else pd.DataFrame()
            if len(g):
                g = g[pd.to_datetime(g.tarih) >= bas]
                ax.scatter(pd.to_datetime(g[g.fon_alis > 0].tarih), d.Close.reindex(pd.to_datetime(g[g.fon_alis > 0].tarih)),
                           marker="^", color="#1e8449", s=18, zorder=5, label="raporda fon alim gunu")
                ax.scatter(pd.to_datetime(g[g.fon_satis > 0].tarih), d.Close.reindex(pd.to_datetime(g[g.fon_satis > 0].tarih)),
                           marker="v", color="#922b21", s=18, zorder=5, label="raporda fon satis gunu")
                ax.legend(loc="lower right", fontsize=8)
            en = a.pay_sermaye.max()
            ax.set_title(f"{s}  |  raporlu tasfiye fonlarinin en yuksek sermaye payi %{100 * en:.1f}  |  kaynak: KAP aylik portfoy raporlari",
                         fontsize=10)
            fig.tight_layout(); pdf.savefig(fig); plt.close(fig); sayfa += 1
    return sayfa


# ---------------------------------------------------------------- K12 ders PDF'i (v1.5)
# CEMAL (24 Eki): "Fon izi nasil bir iz, ben bunu grafiklerde gorebilir miyim? Her yeni buldugun iz icin bana da ders ver."
def fi_k12_ders(V: Dict[str, pd.DataFrame], MA: pd.DataFrame, D: pd.DataFrame, kos: pd.DataFrame, Oz: pd.DataFrame, yol: str) -> int:
    """Fon izi dersi (A4 dikey, telefonda okunur): iz nedir, nerede saklanir, uc vaka grafigi (TEHOL ay ay pay, OZATD blok gunleri,
    IEYHO gun gun fon alimi), grafikte gorunen / gorunmeyen, test sonucu (kat cubuklari, 1,3 cizgisi), kendin nasil bakarsin.
    Sayilar cikti tablolarindan okunur (MA = k11_aylik_birikim, D = k11_defter_gunluk, Oz = k10_ozet). Donus: sayfa sayisi."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    renk = {"ONCE": "#e8eef7", "ERKEN": "#e6f4ea", "KOSU": "#fff4d6", "COKUS": "#fbe3e3"}
    ad = {"ONCE": "dip öncesi", "ERKEN": "dip → 2 kat", "KOSU": "2 kat → tepe", "COKUS": "çöküş"}
    A4 = (8.27, 11.69)

    def yazi(fig, y, baslik, satirlar, boy=10.5, gen=88):
        fig.text(0.07, y, baslik, fontsize=15, weight="bold", va="top", color="#1f2a44"); y -= 0.045
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= 0.024
            y -= 0.006
        return y

    def fazlar(ax, s, d):
        k = kos[kos.sembol == s]
        if not len(k):
            return
        dip, x2, tepe = (pd.Timestamp(k.iloc[0][c]) for c in ("dip", "x2", "tepe"))
        for b, e, f in ((d.index.min(), dip, "ONCE"), (dip, x2, "ERKEN"), (x2, tepe, "KOSU"), (tepe, d.index.max(), "COKUS")):
            if e > b:
                ax.axvspan(b, e, color=renk[f], zorder=0)
                ax.text(b, 0.98, " " + ad[f], transform=ax.get_xaxis_transform(), fontsize=7.5, va="top", color="#555")

    def pay_serisi(s):
        a = MA[MA.kod == s].copy(); a["t"] = pd.to_datetime(a.ay + "-01") + pd.offsets.MonthEnd(0)
        ps = a.set_index("t").pay_sermaye.fillna(0)
        return ps.reindex(pd.date_range(ps.index.min(), ps.index.max(), freq="ME"), fill_value=0.0)

    sayfa = 0
    with PdfPages(yol) as pdf:
        # 1) ozet
        fig = plt.figure(figsize=A4)
        y = yazi(fig, 0.95, "DERS: FON İZİ NEDİR?", [
            "Kısa cevap: fonun izi FİYAT GRAFİĞİNDE değil, SAHİPLİK KAYDINDA. Fon bir hisseyi aldığında bunu her ay KAP'taki "
            "'Portföy Dağılım Raporu'nda yazar. Rapor ay bitiminden yaklaşık 1 hafta sonra (medyan 7 gün) yayımlanır.",
            "",
            "5 cümlede fon izi:",
            "- 1) Tasfiye fonları 23 hissede sermayenin %37'sine kadar pay topladı (TEHOL, OZATD, IEYHO, TRHOL...). Rakamlar basınla aynı.",
            "- 2) Bu payı KOŞU fazında topladılar: 23 hissenin 21'inde net alımın en az %80'i fiyat dipten 2 kat olduktan sonra geldi.",
            "- 3) Payın sermayenin %5'ini geçtiği ay fiyat dipten medyan 11,9 kat yukarıdaydı (4 ile 84 kat arası).",
            "- 4) Dipteki ilk toplama raporlarda YOK: savcılık anlatımına göre hisseler önce kişisel hesaplarda toplandı, sonra fonlara satıldı.",
            "- 5) Bütün BIST'te 'fon girdi' bilgisiyle alım yapmak (rapor yayınının ertesi günü) para kazandırmadı: kat 0,8-1,1.",
            "",
            "Bu derste:",
            "- Sayfa 2: iz nerede saklanıyor (akış şeması)",
            "- Sayfa 3-5: üç vaka grafiği (ay ay fon payı, blok günleri, gün gün fon alımı)",
            "- Sayfa 6: grafikte ne görürsün, ne göremezsin",
            "- Sayfa 7: test sonucu (neden 'iz değil' dedik)",
            "- Sayfa 8: kendin nasıl bakarsın + dersin özeti",
        ])
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        # 2) akis
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.95, "İZ NEREDE SAKLANIYOR?", [
            "Paranın yolu dört adımdır. İlk adım hiçbir kamu kaydında yok; ikinci ve üçüncü adım KAP raporlarında var; dördüncü adım "
            "grafikte çöküş olarak görünür."])
        ax = fig.add_axes([0.05, 0.12, 0.9, 0.72]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        kutular = [
            (0.86, "1) DİPTE TOPLAMA", "Fon sahipleri hisseyi kişisel hesaplarında topluyor.\nGÖRÜNMEZ: fon raporu yok; yalnız aracı kurum dağılımı (AKD, ücretli).", "#e8eef7"),
            (0.62, "2) FONA DEVİR", "Hisseler fonlara satılıyor (blok günler: OZATD 14 May 2026 13,6 mn lot).\nGÖRÜNÜR: aylık fon raporu + bazen tek günde dev hacim.", "#fff4d6"),
            (0.38, "3) FON PAYI BÜYÜR", "Fonun payı sermayenin %5-37'sine, halka açık kısmın çoğunluğuna çıkar.\nGÖRÜNÜR: her ay KAP'ta, ~1 hafta gecikmeyle. %5 eşiğinde pay bildirimi.", "#fff4d6"),
            (0.14, "4) TEK ALICI ÇEKİLİR", "Fon tasfiyeye girer, satıcı kalır, alıcı yok.\nGRAFİKTE GÖRÜNÜR: taban serisi, -%85..-98.", "#fbe3e3")]
        for yk, bas, metin, rk in kutular:
            ax.add_patch(plt.Rectangle((0.05, yk - 0.09), 0.9, 0.18, facecolor=rk, edgecolor="#1f2a44", lw=1.2))
            ax.text(0.08, yk + 0.055, bas, fontsize=12, weight="bold", va="center")
            ax.text(0.08, yk - 0.02, metin, fontsize=9.5, va="center")
            if yk > 0.2:
                ax.annotate("", xy=(0.5, yk - 0.14), xytext=(0.5, yk - 0.095), arrowprops=dict(arrowstyle="->", lw=2))
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        # 3) TEHOL ay ay pay
        for s, baslik, notlar in (
                ("TEHOL", "VAKA 1 — TEHOL: fon payı bir ayda ortaya çıkıyor",
                 ["Üst panel: fiyat (log). Renkli bantlar: fazlar. Alt panel: raporlu tasfiye fonlarının SERMAYE payı (ay sonu).",
                  "Nisan 2025 raporunda fonların payı birden ortaya çıkıyor; o ay fiyat dipten ~10,6 kat yukarıda (KOŞU). Dipte (Ekim 2024) "
                  "pay sıfıra yakın. Kasım 2025'te raporlu pay düşüyor (fonlar sattı ya da paylar rapor vermeyen fonlara geçti). "
                  "Yani fon izi fiyat grafiğinde değil, alt paneldeki rapor serisinde; ve geç geliyor."]),
                ("OZATD", "VAKA 2 — OZATD: blok günleri + fon payı",
                 ["Orta panel: günlük hacim (kırmızı = önceki 20 gün medyanının 20 katından büyük blok gün).",
                  "30 Nis ve 14 May 2026 blok günleri ile Mayıs raporunda fon payının sermayenin ~%26'sına çıkması aynı ay. Blok günü "
                  "grafikte GÖRÜNÜR ama fiyat zaten dipten ~5 kat yukarıdaydı; ve aynı büyüklükte blok günler fon olmayan pek çok hissede de var."])):
            d = V.get(s)
            if d is None or s not in set(MA.kod):
                continue
            ps = pay_serisi(s); d = d[d.index >= ps.index.min() - pd.Timedelta(days=200)]
            fig = plt.figure(figsize=A4)
            yazi(fig, 0.96, baslik, notlar, boy=10)
            ax = fig.add_axes([0.11, 0.50 if s == "TEHOL" else 0.56, 0.84, 0.27 if s == "TEHOL" else 0.21])
            fazlar(ax, s, d); ax.semilogy(d.index, d.Close, color="#1f2a44", lw=1.1); ax.set_ylabel("fiyat (log)")
            if s == "OZATD":
                axv = fig.add_axes([0.11, 0.36, 0.84, 0.17], sharex=ax)
                med = d.Volume.shift(1).rolling(20).median(); blok = d.Volume >= 20 * med
                axv.bar(d.index, d.Volume / 1e6, color=np.where(blok, "#c0392b", "#9aa5b1"), width=1.5)
                axv.set_ylabel("hacim (mn lot)")
                for t in d.index[blok]:
                    axv.annotate(t.strftime("%d %b %Y"), (t, d.Volume[t] / 1e6), fontsize=7, rotation=90, va="bottom", ha="center")
                axp = fig.add_axes([0.11, 0.08, 0.84, 0.24], sharex=ax)
            else:
                axp = fig.add_axes([0.11, 0.10, 0.84, 0.33], sharex=ax)
            axp.bar(ps.index, 100 * ps.to_numpy(), width=25, color="#c0392b")
            axp.set_ylabel("fon payı, sermayenin %'si"); axp.grid(alpha=0.3)
            pdf.savefig(fig); plt.close(fig); sayfa += 1
        # 5) IEYHO gun gun
        s = "IEYHO"; d = V.get(s); g = D[(D.kod == s)].copy() if len(D) else pd.DataFrame()
        if d is not None and len(g):
            g["tarih"] = pd.to_datetime(g.tarih); g = g.set_index("tarih")
            bas = pd.Timestamp("2025-06-01"); bit = pd.Timestamp("2026-01-31")
            dd = d[(d.index >= bas) & (d.index <= bit)]; gg = g[(g.index >= bas) & (g.index <= bit)]
            fig = plt.figure(figsize=A4)
            yazi(fig, 0.96, "VAKA 3 — IEYHO: fon hangi gün kaç lot aldı?", [
                "İşlem dökümü veren şirketlerde (Atlas tam; Tera hiç) fonun her alımı gün gün var. Alt panel: fonun o gün aldığı lot / "
                "borsanın o günkü toplam hacmi.",
                "Eylül 2025'te Atlas fonları 78 mn lot aldı; en büyük gün 22 Eyl: 15,4 mn lot = günlük hacmin %13'ü. Fiyat o sırada dipten "
                "3-6 kat yukarıda (KOŞU). Günlük payı %10-20 olan alıcı grafikte 'özel bir mum' bırakmıyor: hacim zaten yüksek, "
                "fiyat zaten yükseliyor."], boy=10)
            ax = fig.add_axes([0.11, 0.47, 0.84, 0.28]); fazlar(ax, s, dd)
            ax.plot(dd.index, dd.Close, color="#1f2a44", lw=1.1); ax.set_ylabel("fiyat")
            al = gg[gg.fon_alis > 0]
            ax.scatter(al.index, dd.Close.reindex(al.index), marker="^", color="#1e8449", s=22, zorder=5, label="fon alım günü")
            ax.legend(loc="upper left", fontsize=8)
            axp = fig.add_axes([0.11, 0.10, 0.84, 0.31], sharex=ax)
            axp.bar(gg.index, 100 * (gg.fon_alis / gg.hacim.where(gg.hacim > 0)).fillna(0), color="#1e8449", width=1.5)
            axp.set_ylabel("fon alımı, günlük hacmin %'si"); axp.grid(alpha=0.3); ax.set_xlim(bas, bit)
            pdf.savefig(fig); plt.close(fig); sayfa += 1
        # 6) gorunen / gorunmeyen
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.95, "GRAFİKTE NE GÖRÜRSÜN, NE GÖREMEZSİN?", [
            "GÖRÜRSÜN (fon hissesinin KOŞU görüntüsü):",
            "- Taban günü yok, geri çekilmeler sığ (medyan -%19), log grafikte aylarca düz çizgi gibi yükseliş.",
            "- Kilitli tavan serileri, RSI>70, Bollinger üst bant kırılımları, borsanın 'olağan dışı fiyat' sorusu ve VBTS tedbiri.",
            "- Bazen tek günde dev hacim (blok devir: OZATD 14 May 2026, TRHOL 10 Oca 2025 192 kat hacim).",
            "",
            "AMA: bu görüntü fon olmayan yüzlerce yükselen hissede de var. Aynı görüntüden sonra 2 kat görme oranı BIST'te izsiz "
            "yükselişle aynı (kat 1,09-1,19), ABD'de daha kötü (0,38-0,55). Görüntü 'yükselen hisse' demek, 'fon topluyor' demek değil.",
            "",
            "GÖREMEZSİN:",
            "- Dipteki ilk toplama (kişisel hesaplar): fon raporunda yok, grafikte de özel bir iz yok (sessiz yuvarlanma bölgesinde hacim "
            "hatta KURUYOR: kendi normalinin %57'si).",
            "- Kimin aldığı: fiyat-hacim, alıcının kim olduğunu söylemez. Bunu yalnız sahiplik kaydı (fon raporu, KAP pay bildirimi) ve "
            "aracı kurum dağılımı (AKD, ücretli) söyler.",
            "",
            "PRATİK SONUÇ: Grafikte 'fon geliyor' diye alım işareti aranmaz. Fon payı raporda yüksekse bu bir RİSK bilgisidir: tek alıcı "
            "çekilirse taban serisi gelir (TERA -88, DSTKF -90). COL_v1'deki D8 fon süzgeci tam bunu yapar.",
        ], boy=10)
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        # 7) test sonucu
        if len(Oz):
            fig = plt.figure(figsize=A4)
            yazi(fig, 0.95, "TEST: 'FON GİRDİ' BİLGİSİYLE ALSAYDIN?", [
                "Bütün BIST, 22.600 fon raporu. Rapor KAP'ta yayımlandıktan sonraki gün açılışta alım, üretimdeki çıkış kuralı. "
                "Çubuk = 60 günde önce +%20'yi görme oranı / aynı ay ve aynı momentumdaki diğer hisselerin oranı (eşli kat). "
                "İz sayılması için iki dönemde de 1,3 çizgisini geçmeli. Soluk çubuk = 100'den az olay (güvenilmez).", "",
                "Sonuç: bol olaylı hiçbir çubuk çizgiye yaklaşmıyor. Tek yaklaşan 'pay sermayenin %10'unu aştı' 2024-26: yalnız 26 olay, "
                "2023'te 2 olay; büyük kazançların hepsi zaten fon hisselerinden (OZATD, PASEU, GUNDG). Fon çıkışı da düşüşü haber "
                "vermiyor (önce -%20 kat 0,89-0,96)."], boy=10)
            ax = fig.add_axes([0.25, 0.08, 0.68, 0.56])
            x = Oz[Oz.varyant != "cikis"].copy()
            etiket = {"giris": "fon girişi", "ilk": "ilk kez giriş", "cok": "aynı ay 2+ fon", "buyuk": "büyük giriş (≥%3)",
                      "artis": "toplu artış ≥%50", "tasfiye": "tasfiye şirketi girişi", "yogun5": "pay sermayenin %5'ini aştı",
                      "yogun10": "pay sermayenin %10'unu aştı"}
            sira = [v for v in etiket if v in set(x.varyant)]
            yk = np.arange(len(sira))
            for j, (dn, rk) in enumerate((("2023", "#7f8fa6"), ("2024-26", "#1f2a44"))):
                deg = [x[(x.varyant == v) & (x.donem == dn)].k20_kat_esli.mean() for v in sira]
                nn = [int(x[(x.varyant == v) & (x.donem == dn)].n.sum()) for v in sira]
                ax.barh(yk + (0.2 if j == 0 else -0.2), deg, height=0.38, color=rk, label=dn)
                for yy, dv, n_ in zip(yk + (0.2 if j == 0 else -0.2), deg, nn):   # 100'den az olay: soluk (guvenilmez)
                    if n_ < 100 and dv == dv:
                        ax.barh(yy, dv, height=0.38, color="white", alpha=0.65)
                for yy, dv, n_ in zip(yk + (0.2 if j == 0 else -0.2), deg, nn):
                    ax.text((dv if dv == dv else 0) + 0.02, yy, f"n={n_}", va="center", fontsize=7)
            ax.axvline(1.0, color="#999", lw=1); ax.axvline(1.3, color="#c0392b", lw=2, ls="--")
            ax.text(1.31, len(sira) - 0.4, "iz sınırı 1,3", color="#c0392b", fontsize=8)
            ax.set_yticks(yk); ax.set_yticklabels([etiket[v] for v in sira], fontsize=9); ax.invert_yaxis()
            ax.set_xlabel("eşli kat (1 = sıradan hisseyle aynı)"); ax.legend(loc="lower right", fontsize=8); ax.set_xlim(0, 1.8)
            pdf.savefig(fig); plt.close(fig); sayfa += 1
        # 8) kendin bak + ozet
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.95, "KENDİN NASIL BAKARSIN?", [
            "- KAP > Bildirim Sorgu > Fon bildirimleri > konu 'Portföy Dağılım Raporu' > fonu seç. Rapor her ay, ay bitiminden ~1 hafta "
            "sonra çıkar. 'III-FON PORTFÖY DEĞERİ TABLOSU' bölümünde hisse kodu ve NOMİNAL = lot sayısı.",
            "- Hisse sayfasında (KAP > şirket > bildirimler) 'Pay Alım Satım Bildirimi': bir yatırımcı %5, 10, 15, 20, 25, 33, 50 eşiklerini "
            "geçince bildirir. Fonun payının hızla büyüdüğü en erken burada görünür.",
            "- Dikkat: yalnız nitelikli yatırımcıya satılan serbest fonlar rapor vermez (Pardus, A1, Pusula serbest fonları). Onlar görünmez.",
            "- Ben her ay yeni raporları 10 dakikada ekleyebilirim; istersen 'fon payı yüksek hisseler' listesini her ay çıkarırım "
            "(üretime almak senin 'yaz' kararın).",
            "",
            "DERSİN ÖZETİ",
            "- İz nedir? Bir ölçünün sonrasını ayırması: iki dönemde (2023, 2024-26) ve ABD'de, sabit eşikle, aynı koşuldaki sıradan "
            "hisseye göre en az 1,3 kat. Tek vakada görmek iz değildir.",
            "- Fon izi var ama SAHİPLİKTE; fiyat grafiğinde yok. Fonlar fiyatı yükselmiş hisseye giriyor; 'fon girdi' bilgisi alım "
            "işareti değil.",
            "- Fon payı yüksek hisse = tek alıcı riski. Kullanımı: kaçınma / pozisyon boyutu, alım değil.",
            "- Dipteki asıl toplama elde yok (kişisel hesaplar). Günlük kesinlik için AKD gerekir (ücretli).",
        ], boy=10)
        pdf.savefig(fig); plt.close(fig); sayfa += 1
    return sayfa


def fi_k12_ders_u(V: Dict[str, pd.DataFrame], MA: pd.DataFrame, X: pd.DataFrame, Dv: pd.DataFrame, yol: str, kod: str = "TEHOL",
                  bas: str = "2024-09-01", bit: str = "2025-03-31", u_bas: str = "2024-10-04", u_bit: str = "2024-12-20") -> int:
    """Ders 2 (Cemal, 24 Eki): 'TEHOL'deki Ara 2024 - Oca 2025 U sekli fon doneminin izi mi? Oyleyse bir daha goremem, iz degil.'
    Sayfalar: cevap; U bolgesi + D13 tespitleri + raporlu fon payi; ayni hissede fon oncesi yillarda ayni sekil (D13 tespitleri);
    D13 evren testi (6 donem, alim gelme orani ve alim sonrasi getiri, taban ile); balinalar nasil iz birakir + yeni SPK kurallari.
    X = col_tespit_sinyal (D13 = N120, bar>=15, inis>=10, parabol, obek>=2), Dv = col_tespit_varyant_donem (vid 3094 = D13)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    A4 = (8.27, 11.69)
    AYLAR = ("Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara")

    def tr(x) -> str:
        x = pd.Timestamp(x)
        return f"{x.day} {AYLAR[x.month - 1]} {x.year}"

    def yazi(fig, y, baslik, satirlar, boy=10.5, gen=88):
        fig.text(0.07, y, baslik, fontsize=15, weight="bold", va="top", color="#1f2a44"); y -= 0.045
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= 0.024
            y -= 0.006
        return y

    d = V.get(kod)
    if d is None:
        raise KeyError(f"{kod} fiyat verisinde yok")
    q = X[(X.sembol == kod) & (X.N == 120) & (X.konum <= 1.01) & (X.bar >= 15) & (X.inis >= 10) & (X.parabol == True)   # noqa: E712
          & (X.obek >= 2)].copy()
    q["sinyal"] = pd.to_datetime(q.sinyal)
    a = MA[MA.kod == kod].copy(); a["t"] = pd.to_datetime(a.ay + "-01") + pd.offsets.MonthEnd(0)
    ps = a.set_index("t").pay_sermaye.fillna(0)
    ps = ps.reindex(pd.date_range(min(ps.index.min(), pd.Timestamp(bas)), ps.index.max(), freq="ME"), fill_value=0.0)
    on = d[d.index < pd.Timestamp("2024-01-01")]; qo = q[q.sinyal < pd.Timestamp("2024-01-01")]
    t = Dv[Dv.vid == 3094].copy()
    t["taban_alim"] = t.alim_a - t.f_alim_a; t["kat"] = t.alim_a / t.taban_alim
    sayfa = 0
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.95, f"DERS 2: {kod}'ÜN U ŞEKLİ — FON İZİ Mİ, ÇÖL İZİ Mİ?", [
            "Soru: 'TEHOL'de ilk gördüğüm U şekli fon döneminin iziyse onu bir daha göremem; demek ki iz değilmiş.'",
            "",
            "Cevap kısaca:",
            f"- 1) U bölgesi ({tr(u_bas)} – {tr(u_bit)}) oluşurken raporlu fonların payı SIFIR. "
            "Fonların payı Nisan 2025'te, fiyat dipten 10 kat yukarıdayken ortaya çıkıyor. Yani U'yu raporlu fonlar çizmedi.",
            f"- 2) Kodumuz (D13) bu U'yu {', '.join(tr(x) for x in q[(q.sinyal >= u_bas) & (q.sinyal <= bit)].sinyal)} "
            f"günlerinde yakaladı. Aynı şekli aynı hissede 2017–2023 arasında da {len(qo)} kez buldu; o yıllarda raporlu fonlar "
            "TEHOL'de yoktu (2023'te hiç, 2024 Mayıs'a kadar hiç; 2023 öncesi için fon verimiz yok).",
            "- 3) Bu şekil bütün borsada ve ABD'de var: 2016–26 arasında 18.700 kez. Bir daha GÖRECEKSİN.",
            "- 4) Şeklin izi YÖN izidir: U'dan sonra yukarı kırılım (alım) gelme oranı sıradan günden 12–26 puan fazla, 6 dönemin 6'sında; "
            "5 dönemde 1,3 katın üstünde.",
            "- 5) Göremeyeceğin şey TEHOL'ün 10 katlık koşusu: o büyüklük fon döngüsünün (al, fona sat, fiyatı it) ürünüydü. U sonrası "
            "sıradan kazanç: alımdan sonra üretim çıkışıyla ortalama +%1 ile +%20 arası, tabandan biraz iyi.",
            "",
            "Uyarı: U bölgesinde kimin aldığını veri söylemiyor. Savcılık anlatımındaki 'önce kişisel hesaplarda toplama' bu döneme "
            "denk gelebilir; ama bu fon raporunda da, fiyat grafiğinde de ayırt edici bir iz bırakmıyor.",
        ])
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        # U bolgesi
        w = d[(d.index >= bas) & (d.index <= bit)]
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, f"{kod}: U BÖLGESİ, KODUN TESPİTİ VE FON PAYI", [
            "Üst: fiyat (log). Sarı bant = U (dip → yukarı kırılım). Mavi üçgen = D13 tespit günü (dip savunuldu, dipler yukarı "
            "yuvarlandı, küçük mum öbekleri). Alt: raporlu tasfiye fonlarının sermaye payı.",
            "U sırasında fon payı 0. Pay, fiyat zaten 10 kat çıktıktan sonra (Nisan 2025) beliriyor. Kırmızı üçgen (12 Eyl 2024): "
            "aynı kuralın çöküş öncesi yakaladığı bir kutu; aşağı kırıldı (bozuldu). Şekil her seferinde tutmuyor."], boy=10)
        ax = fig.add_axes([0.11, 0.40, 0.84, 0.32])
        ax.axvspan(pd.Timestamp(u_bas), pd.Timestamp(u_bit), color="#fff4d6", zorder=0)
        ax.semilogy(w.index, w.Close, color="#1f2a44", lw=1.2); ax.set_ylabel("fiyat (log)")
        qq = q[(q.sinyal >= bas) & (q.sinyal <= bit)]
        iyi = qq[qq.bozulma != 1]; kot = qq[qq.bozulma == 1]
        ax.scatter(iyi.sinyal, w.Close.reindex(iyi.sinyal), marker="^", s=70, color="#1f77b4", zorder=5, label="D13 tespit")
        ax.scatter(kot.sinyal, w.Close.reindex(kot.sinyal), marker="^", s=70, color="#c0392b", zorder=5, label="D13 tespit, bozuldu")
        ax.legend(loc="upper left", fontsize=8)
        axp = fig.add_axes([0.11, 0.08, 0.84, 0.25], sharex=ax)
        p2 = ps[(ps.index >= bas) & (ps.index <= pd.Timestamp(bit) + pd.Timedelta(days=60))]
        axp.bar(p2.index, 100 * p2.to_numpy(), width=25, color="#c0392b"); axp.set_ylabel("fon payı, sermayenin %'si")
        axp.grid(alpha=0.3); ax.set_xlim(pd.Timestamp(bas), pd.Timestamp(bit) + pd.Timedelta(days=60))
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        # fon oncesi yillar
        if len(on):
            fig = plt.figure(figsize=A4)
            yazi(fig, 0.96, f"{kod}: FON DÖNEMİNDEN ÖNCE DE AYNI ŞEKİL", [
                f"2016–2023. Üçgenler: kodun aynı kuralla bulduğu U şekilleri ({len(qo)} gün; mavi = sonra alım geldi ya da bozulmadı, "
                "kırmızı = aşağı bozuldu). Raporlu fonlar TEHOL'e 2024 Mayıs'tan önce girmedi (2023 öncesi için fon verimiz yok). "
                "Şekil fon döneminden önce de vardı; fon döneminde farklı olan U'dan sonraki koşunun büyüklüğüydü.",
                ], boy=10)
            ax = fig.add_axes([0.11, 0.12, 0.84, 0.66])
            ax.semilogy(on.index, on.Close, color="#1f2a44", lw=0.9); ax.set_ylabel("fiyat (log, bölünme düzeltilmiş)")
            ax.scatter(qo[qo.bozulma != 1].sinyal, on.Close.reindex(qo[qo.bozulma != 1].sinyal), marker="^", s=40, color="#1f77b4", zorder=5)
            ax.scatter(qo[qo.bozulma == 1].sinyal, on.Close.reindex(qo[qo.bozulma == 1].sinyal), marker="^", s=40, color="#c0392b", zorder=5)
            ax.grid(alpha=0.3)
            pdf.savefig(fig); plt.close(fig); sayfa += 1
        # evren testi
        if len(t):
            fig = plt.figure(figsize=A4)
            yazi(fig, 0.96, "TEST: U ŞEKLİ (D13) BÜTÜN BORSADA NE YAPIYOR?", [
                "BIST 4 dönem + ABD 2 dönem, 18.700 U tespiti. Üst: tespitten sonraki 60 barda yukarı kırılım (alım) gelme oranı; "
                "gri = sıradan gün (her 5. gün). Alt: alım geldiyse üretim çıkışıyla (+%8 sonrası maliyet, +%20 sonrası SMA20 trail) "
                "getiri farkı, puan (artı = U'dan sonra daha iyi).",
                "Okuma: YÖN izi güçlü ve tutarlı (6/6). KAZANÇ izi küçük: 6/6 artı ama çoğu 1-2 puan; 2023'te +6,8.",
            ], boy=10)
            ax = fig.add_axes([0.12, 0.47, 0.83, 0.30]); x = np.arange(len(t))
            ax.bar(x - 0.2, 100 * t.taban_alim, width=0.38, color="#9aa5b1", label="sıradan gün")
            ax.bar(x + 0.2, 100 * t.alim_a, width=0.38, color="#1f2a44", label="U tespiti (D13)")
            for xi, k_, v in zip(x, t.kat, t.alim_a):
                ax.text(xi + 0.2, 100 * v + 1, f"{k_:.2f}x", ha="center", fontsize=8, color="#c0392b" if k_ >= 1.3 else "#555")
            ax.set_xticks(x); ax.set_xticklabels(t.donem, fontsize=8); ax.set_ylabel("alım gelme oranı %"); ax.set_ylim(0, 100)
            ax.legend(loc="lower right", fontsize=8)
            axg = fig.add_axes([0.12, 0.10, 0.83, 0.28])
            axg.bar(x, t.f_getiri_a, color=np.where(t.f_getiri_a > 0, "#1e8449", "#c0392b"))
            axg.axhline(0, color="#555", lw=1); axg.set_xticks(x); axg.set_xticklabels(t.donem, fontsize=8)
            axg.set_ylabel("alım sonrası getiri farkı (puan)"); axg.grid(alpha=0.3)
            pdf.savefig(fig); plt.close(fig); sayfa += 1
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.95, "BALİNALAR NASIL İZ BIRAKIR?", [
            "Büyük alıcının parası fiyatı iter; ama fiyat ve hacim ALICININ KİM OLDUĞUNU söylemez. Ölçtüklerimiz:",
            "- Hacim patlaması / blok gün: var, ama fon olmayan hisselerde de aynı sıklıkta → ayırmıyor (A14 çürüdü).",
            "- Hacim kuruması + küçük mum (sessiz toplama): fon hisselerinde VAR (hacim normalin %57'si) ama aynı görüntü sıradan "
            "hisselerde de var, sonrası ayrışmıyor.",
            "- OBV / CMF / A-D birikim ayrışması: ABD'de kâr getirmiyor, BIST'te her kutuda aynı → fona özgü değil.",
            "- 62 gösterge, uyumsuzluk, Fibonacci: yukarı yönlü hiçbiri iki dönemde 1,3 değil.",
            "",
            "Balinanın GERÇEK izleri fiyat dışında:",
            "- Sahiplik kaydı: fon portföy raporu (aylık, ~1 hafta gecikme), KAP pay alım satım bildirimi.",
            "- Aracı kurum dağılımı (AKD): hangi kurum her gün net alıcı (ücretli; elimizde yok).",
            "- Borsanın kendi bayrakları: olağan dışı fiyat sorusu, VBTS tedbiri, toptan alış satış.",
            "",
            "YENİ KURALLAR (SPK, 28 Ağustos ve 8 Eylül 2026 kararları; basından):",
            "- Serbest fon bir şirkette fiili dolaşımdaki payların en fazla %2–8'ine sahip olabilir (halka açıklık düştükçe sınır artar).",
            "- Fon portföyünde %5'ten büyük pozisyonların toplamı %20'yi geçemez (BIST 30 hariç). Uyum takvimi kaynaklara göre farklı.",
            "- Pay sahipliği bildirim eşiği %5'ten %3'e iniyor: balina girişi KAP'ta daha erken görünecek.",
            "→ Haklısın: fonların %30–78 pay toplaması bir daha yasal olarak olmayacak. Ama U şekli fonla gelmiyordu; o kalıyor.",
            "",
            "DERSİN ÖZETİ",
            "- Bir şekil, ancak sonrasını sıradan günden iki dönemde ve ABD'de ayırırsa iz sayılır. U şekli 'yön' için bunu yapıyor, "
            "'büyük kazanç' için yapmıyor.",
            "- TEHOL'deki koşunun büyüklüğü fon döngüsündendi; U'nun kendisi değil.",
            "- Balinayı grafikte değil, sahiplik kaydında ara (yeni %3 eşiği). Grafikte gördüğün şekil herkesin şekli.",
        ], boy=9.6)
        pdf.savefig(fig); plt.close(fig); sayfa += 1
    return sayfa


# ---------------------------------------------------------------- K13 TEHOL-tipi cöl benzerlik taramasi (v1.5)
# CEMAL (24 Eki): "TEHOL'deki 7 Ekim - 16 Aralik 2024 bolgesi col; kod aynisini ayni hissede daha once gordu diyorsun, ben niye
# goremiyorum?" Cevap olcuyle: referans kutunun olculeri sabit esiklere cevrilir, ayni hissede ve evrende aranir, en yakin ornekler
# yan yana cizilir. Esikler TEHOL 2024 kutusundan (dusus -%69, 50 bar, kapanis bandi %17, mum normalin 0,71'i, dipler +%8,5).
FI_K13_ESIK = {"dusus": -0.40, "bar": (30, 80), "bant": 0.25, "mum": 0.85, "u": 1.02, "egim": (-0.05, 0.30)}


def fi_k13_olc(d: pd.DataFrame, i0: int, i1: int) -> Dict[str, float]:
    """Kutu [i0, i1] olculeri: once 60 bar tepesinden dibe dusus, bar, kapanis bandi, mum (H-L / onceki kapanis medyani) ve bunun
    hissenin kendi normaline (kutudan 60-310 bar once) orani, son 10 bar dibi / ilk 10 bar dibi (U), log egim (kutu boyunca)."""
    c = d.Close.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float)
    w = slice(i0, i1 + 1); n = i1 - i0 + 1
    tepe = c[max(0, i0 - 60):i0].max() if i0 > 0 else np.nan
    mum = np.median((h[w] - l[w]) / c[max(i0 - 1, 0):i1][: n]) if i0 > 0 else np.nan
    a, b = max(0, i0 - 310), max(1, i0 - 60)
    norm = np.median((h[a:b] - l[a:b]) / c[max(a - 1, 0):b - 1][: b - a]) if b - a > 50 and a > 0 else np.nan
    return {"bar": n, "dusus": l[w].min() / tepe - 1 if tepe == tepe else np.nan, "bant": c[w].max() / c[w].min() - 1,
            "mum_norm": mum / norm if norm == norm and norm > 0 else np.nan, "u": l[i1 - 9:i1 + 1].min() / l[i0:i0 + 10].min(),
            "egim": float(np.polyfit(np.arange(n), np.log(c[w]), 1)[0] * n),
            # K13b (Cemal 24 Eki: 'Ekim 2024 bölgesinin dibi düzgün, 2021'inki değil'): dip tabanı = kutudaki barların ne kadarı
            # dibe yakın (Low <= kutu dibi x (1 + 2 x kutunun medyan mum boyu)). Tek günlük iğne (V) dip ~0; haftalarca test edilen
            # düz zemin yüksek. TEHOL 2024: 0,26; TEHOL 2021: 0,06.
            "dip_taban": float(np.mean(l[w] <= l[w].min() * (1 + 2 * mum))) if mum == mum else np.nan}


# K13b eşiği sonuç görülmeden yazıldı: TEHOL 2024 değerinin (0,26) biraz altı.
FI_K13B_ESIK = {**FI_K13_ESIK, "dip_taban": 0.20}


def fi_k13_tara(V: Dict[str, pd.DataFrame], E: Dict[str, Any] = FI_K13_ESIK) -> pd.DataFrame:
    """Her hissede her gun t icin: dip j = [t-80, t-30] araligindaki en dusuk Low ve onceki 60 barin da dibi; dipten sonra yeni dip yok; kutu [j, t] butun
    esikleri sagliyorsa aday. Ayni dip icin ilk gun olay (bilgi gunu = t, giris ertesi acilis). Donus: sembol, dip, t, olculer."""
    sat: List[Dict[str, Any]] = []
    b0, b1 = E["bar"]
    for s, d in V.items():
        try:
            n = len(d)
            if n < 400:
                continue
            l = d.Low.to_numpy(float); c = d.Close.to_numpy(float)
            Lw = np.lib.stride_tricks.sliding_window_view(l, b1 - b0 + 1)          # pencere [t-b1, t-b0]
            jrel = Lw.argmin(axis=1); jmin = Lw.min(axis=1)
            sonmin = pd.Series(l).rolling(b0).min().to_numpy()                    # [t-b0+1, t] (denetim 24 Eki: t-b0+1 bari atlaniyordu)
            gorulen = set(); son_olay = -10 ** 9
            for t in range(max(b1, 320), n):
                k = t - b1
                if k >= len(jrel):
                    break
                j = k + jrel[k]
                if j in gorulen or not (sonmin[t] >= jmin[k]):
                    continue
                if j > 0 and l[j] > l[max(0, j - 60):j].min():                  # pencere kenari degil, gercek dip (60 bar)
                    continue
                if t - j + 1 < b0:
                    continue
                tepe = c[max(0, j - 60):j].max()
                if l[j] / tepe - 1 > E["dusus"]:
                    continue
                if c[j:t + 1].max() / c[j:t + 1].min() - 1 > E["bant"]:
                    continue
                o = fi_k13_olc(d, j, t)
                if not (o["mum_norm"] <= E["mum"] and o["u"] >= E["u"] and E["egim"][0] <= o["egim"] <= E["egim"][1]):
                    continue
                if "dip_taban" in E and not (o["dip_taban"] >= E["dip_taban"]):       # K13b düzgün dip (yalnız istenirse)
                    continue
                gorulen.add(j)
                if t - son_olay < 60:                                         # ayni hissede 60 bar icinde tek olay
                    continue
                son_olay = t
                sat.append({"sembol": s, "dip": d.index[j], "bilgi": d.index[t], **o})
        except Exception as ex:   # tek hisse bozuksa digerleri devam eder
            filog.warning("K13 %s atlandi: %s", s, ex)
    return pd.DataFrame(sat)


def fi_k13_ozet(V: Dict[str, pd.DataFrame], O: pd.DataFrame, pazar: str, donemler: List[Tuple[str, str, str]]) -> pd.DataFrame:
    """Olay ve taban (her hissenin her 5. gunu) icin K10 giris/sonuc mekanigi: k20 (60 barda once +%20 / -%10), dus (once -%20),
    trail (uretim cikisi). Donem basina oran, kat ve trail ortalamasi."""
    R = fi_k10_sonuc(V, O.sembol, O.bilgi) if len(O) else pd.DataFrame()
    X = O.reset_index(drop=True).join(R, how="inner") if len(R) else O.iloc[0:0]
    sat = []
    for ad, b, e in donemler:
        x = X[(X.bilgi >= b) & (X.bilgi <= e)]
        T = fi_k10_taban(V, b, e)
        r = {"pazar": pazar, "donem": ad, "n": len(x), "k20": x.k20.mean(), "k20_taban": T.k20.mean(), "dus": x.dus.mean(),
             "dus_taban": T.dus.mean(), "trail": x.trail.mean(), "trail_taban": T.trail.mean()}
        r["k20_kat"] = r["k20"] / r["k20_taban"] if r["k20_taban"] else np.nan
        r["dus_kat"] = r["dus"] / r["dus_taban"] if r["dus_taban"] else np.nan
        sat.append(r)
    return pd.DataFrame(sat), X


def fi_k12_ders3(VP: Dict[str, Dict[str, pd.DataFrame]], X: pd.DataFrame, Z: pd.DataFrame, yol: str, kod: str = "TEHOL",
                 ref: Tuple[str, str] = ("2024-10-07", "2024-12-16"), ornek: int = 12) -> int:
    """Ders 3 (Cemal, 24 Eki): 'Kod aynisini daha once gordu diyorsun, ben niye goremiyorum?' Referans kutunun olculeri (K13),
    ayni hissede olculere uyan eski kutu, evrende en yakin ornekler (hisse adi yok; en yakinlar sonuctan bagimsiz secilir), test
    sonucu (BIST/ABD x 3 donem, kat + 1,3 cizgisi). VP = {pazar: V}, X = K13 olaylari (pazar sutunlu, sonuc sutunlariyla), Z = ozet."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    A4 = (8.27, 11.69)
    AYLAR = ("Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara")

    def tr(x) -> str:
        x = pd.Timestamp(x)
        return f"{x.day} {AYLAR[x.month - 1]} {x.year}"

    def yazi(fig, y, baslik, satirlar, boy=10.5, gen=88):
        fig.text(0.07, y, baslik, fontsize=15, weight="bold", va="top", color="#1f2a44"); y -= 0.045
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= 0.024
            y -= 0.006
        return y

    def kutu_ciz(ax, d, b, e, baslik, oncesi=70, sonrasi=60, kucuk=False):
        i0 = d.index.get_loc(d.index[d.index >= pd.Timestamp(b)][0]); i1 = d.index.get_loc(d.index[d.index <= pd.Timestamp(e)][-1])
        w = d.iloc[max(0, i0 - oncesi):min(len(d), i1 + sonrasi + 1)]
        taban = d.Close.iloc[i0:i1 + 1].min()
        ax.axvspan(d.index[i0], d.index[i1], color="#fff4d6", zorder=0)
        ax.semilogy(w.index, w.Close / taban, color="#1f2a44", lw=0.9 if kucuk else 1.2)
        ax.set_title(baslik, fontsize=8 if kucuk else 10)
        ax.tick_params(labelsize=6 if kucuk else 8); ax.set_xticks([])
        ax.axhline(1.0, color="#999", lw=0.6, ls=":")
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}x"))
        ax.yaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}x" if round(v, 2) in (0.5, 1.5, 2, 3, 5) else ""))

    VB = VP.get("BIST", {}); d = VB.get(kod)
    if d is None:
        raise KeyError(f"{kod} fiyat verisinde yok")
    i0 = d.index.get_loc(d.index[d.index >= pd.Timestamp(ref[0])][0]); i1 = d.index.get_loc(d.index[d.index <= pd.Timestamp(ref[1])][-1])
    R = fi_k13_olc(d, i0, i1)
    X = X.copy()
    X["uzak"] = (abs(X.dusus - R["dusus"]) / 0.2 + abs(X.bar - R["bar"]) / 20 + abs(X.bant - R["bant"]) / 0.08
                 + abs(X.mum_norm - R["mum_norm"]) / 0.15 + abs(X.u - R["u"]) / 0.05 + abs(X.egim - R["egim"]) / 0.1)
    kendi = X[(X.sembol == kod) & (X.pazar == "BIST") & (X.bilgi < pd.Timestamp(ref[0]))]
    diger = X[~((X.sembol == kod) & (X.pazar == "BIST"))].sort_values("uzak").head(ornek)
    yil = max((X.bilgi.max() - X.bilgi.min()).days / 365.25, 1.0)
    ZB = Z[Z.pazar == "BIST"]; XB = X[X.pazar == "BIST"]
    yb, ya = (X.pazar == "BIST").sum() / yil, (X.pazar == "ABD").sum() / yil
    k20b = XB.k20.mean() if "k20" in XB and len(XB) else np.nan
    k20t = float((ZB.k20_taban * ZB.n).sum() / ZB.n.sum()) if len(ZB) and ZB.n.sum() else np.nan
    kat = lambda m: f"{ZB[m].min():.2f}–{ZB[m].max():.2f}".replace(".", ",") if len(ZB) else "?"
    sayfa = 0
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        nb = int((X.pazar == "BIST").sum()); na = int((X.pazar == "ABD").sum())
        yazi(fig, 0.95, "DERS 3: SENİN GÖRDÜĞÜN ÇÖL NE, KOD NE GÖRDÜ?", [
            "Haklısın, önceki sözüm fazlaydı. Kodun (D13) TEHOL'de 'daha önce gördüğü' kutuların çoğu senin bölgenin AYNISI değildi: "
            "D13 gevşek bir kural (dip savunuldu + dipler yükseliyor + küçük mum öbekleri). Çoğu uzun ve geniş bantlı yükseliş parçalarıydı. "
            "COL_GOZ'da da görmüştük: kodun kutularının ancak %6'sı gözle çöl çıkıyordu.",
            "",
            f"Bu kez SENİN bölgeni ({tr(ref[0])} – {tr(ref[1])}) ölçtüm ve aynı ölçülerle aradım:",
            f"- Öncesinde düşüş: %{100 * R['dusus']:.0f} (60 günlük tepeden dibe)",
            f"- Süre: {R['bar']} işlem günü; kapanış bandı: %{100 * R['bant']:.0f} (en yüksek / en düşük kapanış)",
            f"- Mum boyu: hissenin kendi normalinin {R['mum_norm']:.2f}'i (küçük mum)",
            f"- Dipler: son 10 günün dibi ilk 10 günün dibinden %{100 * (R['u'] - 1):.1f} yukarıda (U); bütün kutu eğimi %{100 * R['egim']:+.0f}",
            "",
            f"Arama eşikleri (sabit): düşüş ≤ -%40, 30–80 gün, bant ≤ %25, mum ≤ normalin 0,85'i, dipler ≥ +%2, eğim -%5 ile +%30 arası.",
            "",
            "Sonuç:",
            f"- TEHOL'de 2024 öncesi bu ölçülere uyan TEK bölge var: {', '.join(tr(x) for x in kendi.dip) if len(kendi) else 'yok'} "
            "dibinden sonraki taban (sayfa 2).",
            f"- Bütün BIST'te 2016–2026 arasında {nb}, ABD'de {na} kez. Yılda BIST'te ~{yb:.0f} kez görürsün (sayfa 3–4).",
            "- AMA BIST'te sonrasını ayırmıyor: önce +%20 gelme oranı sıradan günle aynı (sayfa 5). ABD'de iki yöne de oynaklık artıyor.",
        ], boy=10)
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, f"{kod}: 2024 BÖLGESİ VE AYNI ÖLÇÜLERE UYAN ESKİ BÖLGE", [
            "Sarı bant = taban. Fiyat tabanın en düşük kapanışına bölündü (aynı ölçek). Bantın solu düşüş, sağı sonrası (60 gün)."], boy=10)
        ax = fig.add_axes([0.10, 0.50, 0.85, 0.33]); kutu_ciz(ax, d, ref[0], ref[1], f"{kod} {tr(ref[0])} – {tr(ref[1])} (senin bölgen)")
        if len(kendi):
            k = kendi.iloc[0]
            ax2 = fig.add_axes([0.10, 0.08, 0.85, 0.33])
            kutu_ciz(ax2, d, k.dip, k.bilgi, f"{kod} {tr(k.dip)} – {tr(k.bilgi)} (aynı ölçüler; düşüş %{100 * k.dusus:.0f}, "
                                            f"bant %{100 * k.bant:.0f}, mum {k.mum_norm:.2f})")
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        for parca in (diger.iloc[:6], diger.iloc[6:12]):
            if not len(parca):
                continue
            fig = plt.figure(figsize=A4)
            yazi(fig, 0.96, "AYNI ÖLÇÜLERE EN YAKIN ÖRNEKLER (hisse adı yok)", [
                "Sıralama yalnız ölçü benzerliğine göre; sonuca bakılmadan seçildi. Başlıkta: pazar-yıl, sonra 60 günde önce ne geldi."],
                boy=10)
            for kk, r in enumerate(parca.itertuples()):
                V_ = VP.get(r.pazar, {}); dd = V_.get(r.sembol)
                if dd is None:
                    continue
                sonuc = "önce +%20" if r.k20 == 1 else ("önce -%20" if r.dus == 1 else "yatay / -%10")
                ax = fig.add_axes([0.08 + (kk % 2) * 0.46, 0.62 - (kk // 2) * 0.27, 0.40, 0.21])
                kutu_ciz(ax, dd, r.dip, r.bilgi, f"{r.pazar} {pd.Timestamp(r.bilgi).year} — {sonuc}", oncesi=60, sonrasi=60, kucuk=True)
            pdf.savefig(fig); plt.close(fig); sayfa += 1
        if len(Z):
            fig = plt.figure(figsize=A4)
            yazi(fig, 0.96, "TEST: BU ŞEKİLDEN SONRA NE GELİYOR?", [
                "Olay = ölçülere uyan bölge (aynı hissede 60 günde bir). Giriş: bilgi gününün ertesi açılış. Çubuk = olayın oranı / "
                "sıradan günün (her hissenin her 5. günü) oranı. Üst: 60 günde önce +%20 (önce -%10 değil). Alt: 60 günde önce -%20.",
                "İz için iki dönemde ve ABD'de üstte 1,3'ü geçmeli, altta artmamalı. BIST: yukarı kat " + kat("k20_kat") + ". ABD: iki yön "
                "birden artıyor = oynaklık, yön değil."], boy=10)
            for kk, (m, bas_) in enumerate((("k20_kat", "önce +%20, kat"), ("dus_kat", "önce -%20, kat"))):
                ax = fig.add_axes([0.12, 0.47 - kk * 0.36, 0.83, 0.28])
                et = [f"{p} {dn}\nn={int(n)}" for p, dn, n in zip(Z.pazar, Z.donem, Z.n)]
                ax.bar(range(len(Z)), Z[m], color=["#1f2a44" if p == "BIST" else "#7f8fa6" for p in Z.pazar])
                ax.axhline(1.0, color="#999", lw=1); ax.axhline(1.3, color="#c0392b", lw=2, ls="--")
                ax.set_xticks(range(len(Z))); ax.set_xticklabels(et, fontsize=7); ax.set_ylabel(bas_)
            pdf.savefig(fig); plt.close(fig); sayfa += 1
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.95, "DERSİN ÖZETİ", [
            "- Neden göremedin: kodun D13 kuralı senin gözünden çok gevşek. 'Kod buldu' demek 'senin çölünün aynısı' demek değil. "
            "Bundan sonra karşılaştırmayı hep ÖLÇÜYLE yapacağım: senin işaretlediğin bölgenin ölçüleri → sabit eşik → arama → yan yana grafik.",
            f"- Senin bölgen nadir ama tekrar ediyor: TEHOL'de bir kez daha (2021), BIST'te yılda ~{yb:.0f}, ABD'de ~{ya:.0f} kez.",
            "- Bu şekil BIST'te yukarı kırılımı önceden haber vermiyor (kat " + kat("k20_kat") + "); aşağı risk sıradan günden düşük "
            "ya da aynı (önce -%20 kat " + kat("dus_kat") + "). "
            "Yani 'kolay kolay dibi kırılmayan sakin taban' diyebiliriz, 'sonra uçar' diyemeyiz.",
            f"- TEHOL'deki büyük yükseliş bu şekilden okunamazdı: aynı şekli taşıyan BIST bölgelerinin %{100 * k20b:.0f}'i 60 günde önce +%20 gördü, "
            f"sıradan günlerde de oran %{100 * k20t:.0f}. Fon alımları TEHOL'de yükselişin içinde geldi (Ders 2).",
            f"- Senin gözün ölçülerden fazlasını görüyor olabilir (ör. sektör rüzgârı, haber). İstersen bu {len(XB)} BIST örneğini adsız "
            "işaretleme sayfası yapayım: hangilerini 'çöl' sayıyorsun, ayıran ne, onu ölçelim.",
        ], boy=10)
        pdf.savefig(fig); plt.close(fig); sayfa += 1
    return sayfa


def fi_k10_rapor(Oz: pd.DataFrame, MZ: pd.DataFrame, K: pd.DataFrame, E: pd.DataFrame, ek_muaf: int = 0) -> str:
    """v1.5 raporu: kapsam, fon hisselerinde birikim zamani, fon girisi/cikisi/yogunlasma testi (BIST 2023 / 2024-26).
    ek_muaf: indirme sirasinda 'muaf' isaretlenen (tabloya hic girmeyen) rapor sayisi."""
    mu = K.get("muaf", pd.Series(False, index=K.index)).fillna(False).astype(bool)
    kk = K[~mu]
    kap = pd.DataFrame([{"rapor": len(K) + ek_muaf, "muaf (nitelikli yatirimci fonu)": int(mu.sum()) + ek_muaf, "ayristirilan": len(kk),
                         "pozisyon mutabakati %": 100 * kk.poz_tuttu.fillna(False).astype(bool).mean() if len(kk) else np.nan,
                         "islem bolumu olan %": 100 * kk.islem_bolum.fillna(False).astype(bool).mean() if len(kk) else np.nan}])
    iz = []
    for v, g in Oz.groupby("varyant", sort=False):
        k = g.set_index("donem")
        al = v != "cikis"
        m, me = ("k20_kat", "k20_kat_esli") if al else ("dus_kat", "dus_kat_esli")
        iz.append({"varyant": v, "olcu": "once +%20" if al else "once -%20",
                   "kat 2023 / esli": f"{k[m].get('2023', np.nan):.2f} / {k[me].get('2023', np.nan):.2f}",
                   "kat 2024-26 / esli": f"{k[m].get('2024-26', np.nan):.2f} / {k[me].get('2024-26', np.nan):.2f}",
                   "n": "/".join(str(int(x)) for x in k.n.reindex(["2023", "2024-26"]).fillna(0)),
                   "iz (BIST, 2 donem, kat ve esli >= 1,3)": bool((k[[m, me]].reindex(["2023", "2024-26"]) >= 1.3).all().all())})
    kolon = ["varyant", "donem", "n", "hisse", "k20", "k20_taban", "k20_kat", "k20_esli", "k20_kat_esli", "dus", "dus_kat", "dus_kat_esli",
             "r60_ort", "r60_med", "r60_esli_ort", "trail_ort", "trail_med", "trail_esli_ort", "slot", "slot_rastgele"]
    mz = ["kod", "ilk_ay", "en_cok_pay_sermaye", "pay5_ay", "pay5_faz", "pay5_fiyat_dip", "pay20_ay", "pay20_fiyat_dip",
          "alim_ONCE_yzd", "alim_ERKEN_yzd", "alim_KOSU_yzd", "alim_COKUS_yzd", "alim_ay", "hacimden_buyuk_ay"]
    sat = [f"# FON_IZI K9-K11 — {FI_SURUM}", "",
           "Soru (Cemal, 23 Eki): fonlar hangi gun kac lot aldi; fon girisi ise yayin gununden sonra islem yapilabilir bir iz mi?", "",
           "Kaynak: KAP aylik portfoy dagilim raporlari (2022-12 -> bugun). Her rapor kendi toplam satiriyla mutabakattan gecer; tutmayan rapor",
           "kullanilmaz. Nitelikli yatirimciya satilan serbest fonlar rapor vermez (muaf) -> gorunmez. Bilgi ani = KAP yayini; giris = ertesi",
           "islem gunu acilisi. Cikis = uretim (+%8 sonrasi maliyet, +%20 sonrasi SMA20 trail, 120 bar), -%0,4 maliyet.", "",
           "## Kapsam", "", kap.round(1).to_markdown(index=False), "",
           "## Fon hisselerinde birikim zamani (raporlu tasfiye fonlari; pay = sermayeye gore, lotlar bolunmeden arindirilmis)", "",
           MZ[[c for c in mz if c in MZ]].round(2).to_markdown(index=False) if len(MZ) else "(veri yok)", "",
           "## Iz karari (BIST; ABD karsiligi bu turda kurulmadi)", "", pd.DataFrame(iz).to_markdown(index=False), "",
           "## Ayrinti", "", Oz[[c for c in kolon if c in Oz]].round(3).to_markdown(index=False), ""]
    return "\n".join(sat)


FI_K13_DONEM = [("2016-22", "2016-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31")]


def fon_izi_k13(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    """K13 surucu (Ders 3): TEHOL 7 Eki - 16 Ara 2024 tabaninin olculeriyle sabit esikli arama (BIST + ABD, 3 donem), sonuc testi,
    olay/ozet CSV ve FON_IZI_ders3_col_olcu.pdf."""
    A = A or FIAyar(); os.makedirs(A.cikti, exist_ok=True)
    VP, Xs, Zs = {}, [], []
    for pazar in ("BIST", "ABD"):
        try:
            VP[pazar] = fi_k1_veri(A.veri[pazar], pazar, A)
        except Exception as ex:
            filog.warning("K13 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        O = fi_k13_tara(VP[pazar])
        Z, X = fi_k13_ozet(VP[pazar], O, pazar, FI_K13_DONEM)
        filog.info("K13 %s: %d olay", pazar, len(O))
        Xs.append(X.assign(pazar=pazar)); Zs.append(Z)
    if not Xs:
        raise RuntimeError("K13: hicbir pazar verisi okunamadi")
    X = pd.concat(Xs, ignore_index=True); Z = pd.concat(Zs, ignore_index=True)
    X.to_csv(os.path.join(A.cikti, "k13_tehol_tipi_olaylar.csv"), index=False)
    Z.to_csv(os.path.join(A.cikti, "k13_tehol_tipi_ozet.csv"), index=False)
    try:
        fi_k12_ders3(VP, X, Z, os.path.join(A.cikti, "FON_IZI_ders3_col_olcu.pdf"))
    except Exception as ex:
        filog.error("K13 ders PDF uretilemedi: %s", ex)
    return {"olay": X, "ozet": Z}


# ---------------------------------------------------------------- K14 K13'un uc devam denemesi (v1.5)
# CEMAL (24 Eki): "Iz yok cikarsa durma: ne denedigini, esige en cok yaklasanlari ve siradaki 3 denemeyi yaz, sonra kendin dene."
# Sartlar SONUC GORULMEDEN yazildi: ana olcu, esli kutuya (ayni cokus baglami: >= %40 dusus, 30 gun yeni dip yok, ama K13 sekil
# sartini hic saglamamis dip) gore BIST 2023, BIST 2024-26, ABD 2023, ABD 2024-26 hucrelerinin HEPSINDE >= 1,3; asagi olcu
# (once -%20) ayni hucrelerde < 1,3; hucrede olay n < 30 ise 'kucuk orneklem' (iz sayilmaz).
# D1 RUZGAR: Cemal'in tanimi 'sektor ruzgari olmadan col aranmaz' -> K13 + D9b ruzgari bilgi gunu (sepet 60g - piyasa medyani
#    >= %10 ve sepet > 0; BIST alt endeks, ABD endustri; uye >= 4, hisse haric). Esli kutu da ruzgarli olanlarla sinirli.
# D2 YUKSELIS: 'col ardindan gelen yukselisle degerlendirilir' -> 250 barda, kapanis kutu dibinin %2 altina inmeden once 2 kat.
# D3 KIRILIM: uc evre -> kutu tavani (kutudaki en yuksek kapanis) x1,002 ustunde kapanis, 60 bar icinde, dip kirilmadan; giris
#    ertesi acilis. Ana olcu 2 kat (D2 kurali), yaninda once +%20 ve uretim cikisi.
FI_K14_ESIK = {"ruz": 0.10, "ruz_gun": 60, "ruz_uye": 4, "kat": 1.0, "kat_yarim": 0.5, "ufuk": 250, "dip_tol": 0.02,
               "bekle": 60, "tavan": 1.002, "n_min": 30, "kat_esik": 1.3}
FI_K14_HUCRE = [("BIST", "2023"), ("BIST", "2024-26"), ("ABD", "2023"), ("ABD", "2024-26")]


def fi_k14_sektor(pazar: str, kok: Optional[str] = None) -> Dict[str, str]:
    """{sembol: alt sektor}. BIST: sektor_BIST.csv 'alt_bist' (Yahoo etiketleri hatali); ABD: sektor_ABD.csv 'endustri',
    sembol uzantisi ('.AM') atilir. Dosya repo kokunde (bu dosyanin klasoru)."""
    kok = kok or os.path.dirname(os.path.abspath(__file__))
    if pazar == "BIST":
        t = pd.read_csv(os.path.join(kok, "sektor_BIST.csv")); kol = "alt_bist"
    else:
        t = pd.read_csv(os.path.join(kok, "sektor_ABD.csv")); kol = "endustri"
    t = t.dropna(subset=[kol])
    return {str(s).split(".")[0].upper().strip(): str(a) for s, a in zip(t.sembol, t[kol])}


def fi_k14_ruzgar(V: Dict[str, pd.DataFrame], sek: Dict[str, str], E: Dict[str, Any] = FI_K14_ESIK) -> pd.DataFrame:
    """Gunluk ruzgar paneli (index tarih, sutun sembol, bool): sepet (ayni alt sektor, hisse haric, ort. 60g getiri) - piyasa
    medyani >= E['ruz'] ve sepet > 0 (COL_v1 D9b ile ayni tanim, her gun icin). Uyesi < E['ruz_uye'] olan sektor: ruzgar yok."""
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index().ffill(limit=5)
    r = C / C.shift(E["ruz_gun"]) - 1
    piy = r.median(axis=1)
    W = pd.DataFrame(False, index=r.index, columns=r.columns)
    grup: Dict[str, List[str]] = {}
    for s in r.columns:
        a = sek.get(str(s).upper())
        if a:
            grup.setdefault(a, []).append(s)
    for a, uy in grup.items():
        R = r[uy]; S = R.sum(axis=1, min_count=1); N = R.notna().sum(axis=1)
        for s in uy:
            kendi = R[s]
            sep = (S - kendi.fillna(0)) / (N - kendi.notna().astype(int))
            uye = N - kendi.notna().astype(int)
            W[s] = ((sep - piy) >= E["ruz"]) & (sep > 0) & (uye >= E["ruz_uye"])
    return W


def fi_k14_esli(V: Dict[str, pd.DataFrame], O: pd.DataFrame, E: Dict[str, Any] = FI_K13_ESIK) -> pd.DataFrame:
    """Esli kutu: K13 ile ayni cokus baglami (dip [t-80, t-30] icinde ve onceki 60 barin dibi, dipten beri yeni dip yok, once
    >= %40 dusus) ama bilgi gunune kadar bu dipten olay cikmamis (v1.6: yalniz gecmis bilgi). Bilgi gunu = dipten 30. bar (K13'un en erken olabilecegi gun); hissede
    60 barda tek. Donus K13 ile ayni sutunlar."""
    sat: List[Dict[str, Any]] = []
    b0, b1 = E["bar"]
    # v1.6 (denetim 24 Eki): eskiden 'bu dipten HIC olay cikmamis' ve 'olaya +-60 bar yakin degil' GELECEGE bakiyordu (olay dip+80'e
    # kadar cikabilir): kontrol grubu sonuc penceresindeki fiyat yoluna gore seciliyordu. Simdi yalniz bilgi gunune kadar bilinen:
    # ayni dipten bilgi gunu ya da oncesinde olay cikmissa, ya da son 60 barda olay varsa esli olmaz.
    ilk_olay: Dict[Tuple[str, pd.Timestamp], pd.Timestamp] = {}
    for s_, x, y in (zip(O.sembol, O.dip, O.bilgi) if len(O) else ()):
        k_ = (s_, pd.Timestamp(x)); ilk_olay[k_] = min(ilk_olay.get(k_, pd.Timestamp(y)), pd.Timestamp(y))
    for s, d in V.items():
        try:
            n = len(d)
            if n < 400:
                continue
            l = d.Low.to_numpy(float); c = d.Close.to_numpy(float)
            sonmin = pd.Series(l).rolling(b0 - 1).min().to_numpy()
            yakin = d.index.get_indexer(pd.DatetimeIndex(O.bilgi[O.sembol == s])) if len(O) else np.array([], int)
            son_olay = -10 ** 9
            for t in range(max(b1, 320), n):
                j = t - b0 + 1
                if not (l[j] <= l[max(0, j - 60):j].min() and sonmin[t] >= l[j]):          # gercek dip, sonra yeni dip yok
                    continue
                io = ilk_olay.get((s, d.index[j]))
                gec = yakin[(yakin >= 0) & (yakin <= t)] if len(yakin) else yakin
                if (io is not None and io <= d.index[t]) or t - son_olay < 60 or (len(gec) and (t - gec).min() < 60):
                    continue
                tepe = c[max(0, j - 60):j].max()
                if l[j] / tepe - 1 > E["dusus"]:
                    continue
                son_olay = t
                sat.append({"sembol": s, "dip": d.index[j], "bilgi": d.index[t], **fi_k13_olc(d, j, t)})
        except Exception as ex:   # tek hisse bozuksa digerleri devam eder
            filog.warning("K14 esli %s atlandi: %s", s, ex)
    return pd.DataFrame(sat)


def fi_k14_yukselis(V: Dict[str, pd.DataFrame], O: pd.DataFrame, E: Dict[str, Any] = FI_K14_ESIK) -> pd.DataFrame:
    """D2: giris = bilgi gununden sonraki acilis; kutu dibi = [dip, bilgi] en dusuk Low. E['ufuk'] barda kapanis dibin
    E['dip_tol'] altina inmeden once High >= giris x (1+E['kat']) -> kat2 = 1; ayni sekilde +%50 -> kat15; max_yuk = dip
    kirilana (ya da ufka) kadar en yuksek High / giris - 1. Ufuk dolmamissa NaN."""
    out = []
    for i, r in enumerate(O.itertuples()):
        d = V.get(r.sembol)
        if d is None:
            continue
        tar = d.index; e = int(tar.searchsorted(pd.Timestamp(r.bilgi), side="right"))
        if e + E["ufuk"] > len(d):
            continue
        a = int(tar.searchsorted(pd.Timestamp(r.dip), side="left"))
        dip = d.Low.iloc[a:e].min(); g = d.Open.iloc[e]
        if not (g > 0 and dip > 0):
            continue
        c = d.Close.to_numpy(float)[e:e + E["ufuk"]]; h = d.High.to_numpy(float)[e:e + E["ufuk"]]
        kir = np.flatnonzero(c < dip * (1 - E["dip_tol"])); k = kir[0] if len(kir) else len(c)
        ilk = lambda m: (np.flatnonzero(h >= g * (1 + m)) if (h >= g * (1 + m)).any() else np.array([10 ** 6]))[0]
        out.append({"i": i, "kat2": float(ilk(E["kat"]) <= k and ilk(E["kat"]) < len(c)),
                    "kat15": float(ilk(E["kat_yarim"]) <= k and ilk(E["kat_yarim"]) < len(c)),
                    "max_yuk": h[:max(k, 1)].max() / g - 1, "dip_kirildi": float(k < len(c))})
    R = pd.DataFrame(out)
    return R.set_index("i") if len(R) else R


def fi_k14_kirilim(V: Dict[str, pd.DataFrame], O: pd.DataFrame, E: Dict[str, Any] = FI_K14_ESIK) -> pd.DataFrame:
    """D3: kutu [dip, bilgi]; tavan = kutudaki en yuksek kapanis. Bilgi gununden sonraki E['bekle'] barda kapanis dibin
    E['dip_tol'] altina inmeden tavan x E['tavan'] ustune cikarsa o gun yeni bilgi gunu (giris ertesi acilis). Donus: kirilan
    satirlar, 'bilgi' = kirilim gunu, 'kutu_bilgi' = eski bilgi gunu."""
    sat = []
    for r in O.itertuples():
        d = V.get(r.sembol)
        if d is None:
            continue
        tar = d.index; a = int(tar.searchsorted(pd.Timestamp(r.dip), side="left"))
        b = int(tar.searchsorted(pd.Timestamp(r.bilgi), side="right"))
        c = d.Close.to_numpy(float); tavan = c[a:b].max(); dip = d.Low.iloc[a:b].min()
        for k in range(b, min(len(c), b + E["bekle"])):
            if c[k] < dip * (1 - E["dip_tol"]):
                break
            if c[k] > tavan * E["tavan"]:
                x = r._asdict(); x.pop("Index", None); x["kutu_bilgi"] = x["bilgi"]; x["bilgi"] = tar[k]
                sat.append(x); break
    return pd.DataFrame(sat)


def fi_k14_kiyas(Ol: pd.DataFrame, Es: pd.DataFrame, pazar: str, donemler: List[Tuple[str, str, str]],
                 olculer: Tuple[str, ...] = ("kat2", "kat15", "k20", "dus", "trail")) -> pd.DataFrame:
    """Donem basina olay ve esli kutu oranlari, kat = olay / esli. 'trail' ortalama getiri (kat yerine fark)."""
    sat = []
    for ad, b, e in donemler:
        x = Ol[(Ol.bilgi >= b) & (Ol.bilgi <= e)] if len(Ol) else Ol
        y = Es[(Es.bilgi >= b) & (Es.bilgi <= e)] if len(Es) else Es
        r = {"pazar": pazar, "donem": ad, "n": len(x), "n_esli": len(y)}
        for m in olculer:
            a_ = x[m].mean() if m in x and len(x) else np.nan; t_ = y[m].mean() if m in y and len(y) else np.nan
            r[m] = a_; r[m + "_esli"] = t_
            if m == "trail":
                r["trail_fark"] = a_ - t_
            else:
                r[m + "_kat"] = a_ / t_ if t_ and t_ == t_ else np.nan
        sat.append(r)
    return pd.DataFrame(sat)


def fi_k14_karar(Z: pd.DataFrame, ana: str, E: Dict[str, Any] = FI_K14_ESIK) -> Tuple[str, pd.DataFrame]:
    """Onceden yazilan sart: FI_K14_HUCRE hucrelerinin hepsinde ana_kat >= 1,3, dus_kat < 1,3, n >= 30."""
    H = Z.set_index(["pazar", "donem"]).reindex(FI_K14_HUCRE)
    kucuk = (H.n.fillna(0) < E["n_min"]).any()
    gecti = (H[ana + "_kat"] >= E["kat_esik"]).all() and (H.dus_kat < E["kat_esik"]).all()
    return ("IZ" if gecti and not kucuk else ("KUCUK ORNEKLEM" if gecti else "IZ DEGIL")), H.reset_index()


def fon_izi_k14(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    """K14 surucu: K13 olaylari + esli kutular (BIST + ABD), D1 ruzgar, D2 yukselis, D3 kirilim; CSV + rapor tablosu."""
    A = A or FIAyar(); os.makedirs(A.cikti, exist_ok=True)
    Z: Dict[str, List[pd.DataFrame]] = {"D1": [], "D2": [], "D3": []}
    X: List[pd.DataFrame] = []
    for pazar in ("BIST", "ABD"):
        try:
            V = fi_k1_veri(A.veri[pazar], pazar, A)
        except Exception as ex:
            filog.warning("K14 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        O = fi_k13_tara(V); Es = fi_k14_esli(V, O)
        filog.info("K14 %s: %d olay, %d esli kutu", pazar, len(O), len(Es))
        W = fi_k14_ruzgar(V, fi_k14_sektor(pazar))
        tum = []
        for tur, T in (("olay", O), ("esli", Es)):
            if not len(T):
                continue
            T = T.reset_index(drop=True)
            T = T.join(fi_k10_sonuc(V, T.sembol, T.bilgi), how="left").join(fi_k14_yukselis(V, T), how="left")
            T["ruzgar"] = [bool(W.at[pd.Timestamp(b), s]) if pd.Timestamp(b) in W.index and s in W.columns else False
                           for s, b in zip(T.sembol, T.bilgi)]
            K = fi_k14_kirilim(V, T[["sembol", "dip", "bilgi"]])
            if len(K):
                K = K.reset_index(drop=True)
                K = K.join(fi_k10_sonuc(V, K.sembol, K.bilgi), how="left").join(fi_k14_yukselis(V, K), how="left")
            T["tur"] = tur; K["tur"] = tur
            tum.append((tur, T, K))
        d = {t: (T, K) for t, T, K in tum}
        (Ot, Ok), (Et, Ek) = d.get("olay", (O.iloc[0:0], O.iloc[0:0])), d.get("esli", (O.iloc[0:0], O.iloc[0:0]))
        Z["D1"].append(fi_k14_kiyas(Ot[Ot.ruzgar], Et[Et.ruzgar], pazar, FI_K13_DONEM))
        Z["D2"].append(fi_k14_kiyas(Ot, Et, pazar, FI_K13_DONEM))
        Z["D3"].append(fi_k14_kiyas(Ok, Ek, pazar, FI_K13_DONEM))
        for tur, T, K in tum:
            X.append(T.assign(pazar=pazar, asama="kutu")); X.append(K.assign(pazar=pazar, asama="kirilim"))
    if not X:
        raise RuntimeError("K14: hicbir pazar verisi okunamadi")
    Xa = pd.concat(X, ignore_index=True); Xa.to_csv(os.path.join(A.cikti, "k14_olaylar.csv.gz"), index=False)
    ana = {"D1": "k20", "D2": "kat2", "D3": "kat2"}
    sonuc = {}
    for k, L in Z.items():
        Zk = pd.concat(L, ignore_index=True); Zk.to_csv(os.path.join(A.cikti, f"k14_{k}_ozet.csv"), index=False)
        sonuc[k] = (Zk,) + fi_k14_karar(Zk, ana[k])
    return {"olay": Xa, "sonuc": sonuc}


# ---------------------------------------------------------------- K15 ikinci tur (K14'un uc denemesi de IZ DEGIL, v1.5)
# Sartlar SONUC GORULMEDEN yazildi (K14 ile ayni karar kurali, FI_K14_HUCRE; ana olcu 2 kat, R3'te 3 kat):
# R1 GENISLIK: K14'te ruzgarli olay cok az (4-15). Pazar duzeyinde zemin: bilgi gunu hisselerin >= %50'si SMA200 ustunde
#    (IZ_DEFTERI B8 'piyasa genisligi' GECERLI zamanlama izi). Olay ve esli kutu ayni sartla.
# R2 OYNAKLIK ESLI: K14'te esli kutular daha sik 2 kat yapti; esli kutular daha oynak olabilir. Esli oran, olaylarin
#    (kutudan once 60-310 bar medyan (H-L)/onceki kapanis) pazar ici uclusu x yil hucrelerine gore agirlikli (dogrudan
#    standartlastirma). Kat = olay orani / agirlikli esli orani.
# R3 BUYUK YUKSELIS: TEHOL'un yaptigi -> 250 barda dip kirilmadan once 3 kat (kat3), olay vs esli; R2 agirligiyla da.
FI_K15_ESIK = {"genislik": 0.50, "sma": 200, "kat3": 2.0}


FI_K15_DERS = [("D1", "K13 + sektör rüzgârı (D9b), ana ölçü önce +%20", "k20"),
               ("D2", "K13, ana ölçü 250 günde dip kırılmadan 2 kat", "kat2"),
               ("D3", "K13 kutu tavanı kırılımı (60 gün içinde), ana ölçü 2 kat", "kat2"),
               ("R1", "K13 + piyasa genişliği ≥%50 (SMA200 üstü), ana ölçü 2 kat", "kat2"),
               ("R2", "K13 vs oynaklığı eşlenmiş eşli kutu, ana ölçü 2 kat", "kat2"),
               ("R3", "K13, ana ölçü 3 kat (TEHOL'ün yaptığı)", "kat3")]


def fi_k15_genislik(V: Dict[str, pd.DataFrame], E: Dict[str, Any] = FI_K15_ESIK) -> pd.Series:
    """Gunluk piyasa genisligi: kapanisi SMA200 ustunde olan hisse payi (SMA'si hesaplanabilen hisseler icinde)."""
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index().ffill(limit=5)
    M = C.rolling(E["sma"], min_periods=E["sma"]).mean()
    ust = (C > M) & M.notna()
    return ust.sum(axis=1) / M.notna().sum(axis=1).replace(0, np.nan)


def fi_k15_oynaklik(V: Dict[str, pd.DataFrame], O: pd.DataFrame) -> pd.Series:
    """Kutudan once oynaklik: dipten 60-310 bar once medyan (H-L)/onceki kapanis (K13 mum normuyla ayni pencere)."""
    out = []
    for r in O.itertuples():
        d = V.get(r.sembol)
        if d is None:
            out.append(np.nan); continue
        j = int(d.index.searchsorted(pd.Timestamp(r.dip), side="left")); a, b = max(1, j - 310), max(1, j - 60)
        h = d.High.to_numpy(float); l = d.Low.to_numpy(float); c = d.Close.to_numpy(float)
        out.append(float(np.median((h[a:b] - l[a:b]) / c[a - 1:b - 1])) if b - a > 50 else np.nan)
    return pd.Series(out, index=O.index)


def fi_k15_kiyas(Ol: pd.DataFrame, Es: pd.DataFrame, pazar: str, donemler: List[Tuple[str, str, str]],
                 olculer: Tuple[str, ...] = ("kat2", "kat3", "dus"), agirlik: bool = False) -> pd.DataFrame:
    """fi_k14_kiyas gibi; agirlik=True ise esli orani olaylarin 'hucre' (oynaklik uclusu x yil) dagilimina gore agirlikli."""
    sat = []
    for ad, b, e in donemler:
        x = Ol[(Ol.bilgi >= b) & (Ol.bilgi <= e)]; y = Es[(Es.bilgi >= b) & (Es.bilgi <= e)]
        r = {"pazar": pazar, "donem": ad, "n": len(x), "n_esli": len(y)}
        for m in olculer:
            a_ = x[m].mean() if len(x) else np.nan
            if agirlik and len(x):
                ey = y.groupby("hucre")[m].mean(); w = x.hucre.value_counts(normalize=True)
                ort = w.index.intersection(ey.dropna().index)
                t_ = float((ey[ort] * w[ort]).sum() / w[ort].sum()) if len(ort) else np.nan
            else:
                t_ = y[m].mean() if len(y) else np.nan
            r[m] = a_; r[m + "_esli"] = t_; r[m + "_kat"] = a_ / t_ if t_ and t_ == t_ else np.nan
        sat.append(r)
    return pd.DataFrame(sat)


def fon_izi_k15(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    """K15 surucu: k14_olaylar.csv.gz kutu satirlari + veri -> R1 genislik, R2 oynaklik esli, R3 3 kat; CSV + karar."""
    A = A or FIAyar()
    X = pd.read_csv(os.path.join(A.cikti, "k14_olaylar.csv.gz"), parse_dates=["dip", "bilgi"])
    X = X[X.asama == "kutu"].reset_index(drop=True)
    Z: Dict[str, List[pd.DataFrame]] = {"R1": [], "R2": [], "R3": []}
    Y = []
    for pazar in ("BIST", "ABD"):
        try:
            V = fi_k1_veri(A.veri[pazar], pazar, A)
        except Exception as ex:
            filog.warning("K15 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        T = X[X.pazar == pazar].reset_index(drop=True)
        G = fi_k15_genislik(V)
        T["genislik"] = G.reindex(pd.DatetimeIndex(T.bilgi)).to_numpy()
        T["oyn"] = fi_k15_oynaklik(V, T)
        q = np.nanquantile(T.oyn[T.tur == "esli"], [1 / 3, 2 / 3])
        T["hucre"] = [f"{int(np.searchsorted(q, v))}_{b.year}" if v == v else "" for v, b in zip(T.oyn, T.bilgi)]
        K3 = fi_k14_yukselis(V, T, {**FI_K14_ESIK, "kat": FI_K15_ESIK["kat3"]})
        T["kat3"] = K3.kat2.reindex(T.index) if len(K3) else np.nan
        Ol, Es = T[T.tur == "olay"], T[T.tur == "esli"]
        gn = FI_K15_ESIK["genislik"]
        Z["R1"].append(fi_k15_kiyas(Ol[Ol.genislik >= gn], Es[Es.genislik >= gn], pazar, FI_K13_DONEM))
        Z["R2"].append(fi_k15_kiyas(Ol[Ol.hucre != ""], Es[Es.hucre != ""], pazar, FI_K13_DONEM, agirlik=True))
        Z["R3"].append(fi_k15_kiyas(Ol, Es, pazar, FI_K13_DONEM, olculer=("kat3", "kat2", "dus")))
        Y.append(T)
    if not Y:
        raise RuntimeError("K15: hicbir pazar verisi okunamadi")
    pd.concat(Y, ignore_index=True).to_csv(os.path.join(A.cikti, "k15_olaylar.csv.gz"), index=False)
    ana = {"R1": "kat2", "R2": "kat2", "R3": "kat3"}
    sonuc = {}
    for k, L in Z.items():
        Zk = pd.concat(L, ignore_index=True); Zk.to_csv(os.path.join(A.cikti, f"k15_{k}_ozet.csv"), index=False)
        sonuc[k] = (Zk,) + fi_k14_karar(Zk, ana[k])
    try:
        D = [(k, ACIK, pd.read_csv(os.path.join(A.cikti, f"k14_{k}_ozet.csv")), m) for k, ACIK, m in FI_K15_DERS[:3]]
        D += [(k, ACIK, sonuc[k][0], m) for k, ACIK, m in FI_K15_DERS[3:]]
        fi_k12_ders4(D, os.path.join(A.cikti, "FON_IZI_ders4_tehol_denemeler.pdf"))
    except Exception as ex:
        filog.error("K15 ders 4 PDF uretilemedi: %s", ex)
    return {"sonuc": sonuc}


def fi_k12_ders4(D: List[Tuple[str, str, pd.DataFrame, str]], yol: str) -> int:
    """Ders 4 (curuyen olcu dersi): K13'un iki tur devam denemesi. D = [(kod, aciklama, ozet Z, ana olcu)]; her deneme icin
    BIST/ABD x donem ana kat ve asagi (dus) kat cubuklari, 1,3 cizgisi, n. Son sayfa: ders ve 'kendin nasil bakarsin'."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    A4 = (8.27, 11.69)

    def yazi(fig, y, baslik, satirlar, boy=10, gen=90):
        fig.text(0.07, y, baslik, fontsize=15, weight="bold", va="top", color="#1f2a44"); y -= 0.045
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= 0.023
            y -= 0.005
        return y

    sayfa = 0
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.95, "DERS 4: TEHOL TİPİ TABAN — ALTI DENEME, İZ YOK", [
            "Ders 3'te senin TEHOL bölgenin ölçüleriyle aranan taban (K13) iz çıkmadı. Kural gereği durmadım: altı deneme daha yaptım. "
            "Şartları sonuca bakmadan yazdım: ana ölçü 'eşli kutuya' göre BIST 2023, BIST 2024-26, ABD 2023, ABD 2024-26 dört hücrenin "
            "hepsinde ≥1,3 olmalı, aşağı ölçü (önce −%20) 1,3'ü geçmemeli, her hücrede en az 30 olay olmalı.",
            "Eşli kutu = aynı çöküş (≥%40 düşüş, 30 gün yeni dip yok) ama senin şekline (dar bant, küçük mum, yükselen dipler) hiç "
            "uymamış dip. Yani soru: 'çöküşten sonraki herhangi bir tabana göre, SENİN şeklin fark yaratıyor mu?'",
            "",
            *[f"- {k}: {a}" for k, a, _, _ in D],
            "",
            "Sonraki sayfalarda her deneme bir çubuk grafik: koyu = BIST, açık = ABD; kırmızı kesikli çizgi 1,3. Üst grafik ana ölçü, "
            "alt grafik aşağı ölçü. Çubuğun altında n (olay sayısı).",
        ])
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        for i in range(0, len(D), 2):
            fig = plt.figure(figsize=A4)
            for kk, (kod, acik, Z, ana) in enumerate(D[i:i + 2]):
                y0 = 0.52 - kk * 0.47
                fig.text(0.07, y0 + 0.42, f"{kod}: {acik}"[:110], fontsize=10, weight="bold", va="top", color="#1f2a44")
                for jj, (m, bas_) in enumerate(((ana + "_kat", f"{ana}, kat"), ("dus_kat", "önce −%20, kat"))):
                    ax = fig.add_axes([0.10 + jj * 0.45, y0 + 0.05, 0.38, 0.30])
                    et = [f"{p[0]} {dn}\nn={int(n)}" for p, dn, n in zip(Z.pazar, Z.donem, Z.n)]
                    ax.bar(range(len(Z)), Z[m].fillna(0), color=["#1f2a44" if p == "BIST" else "#7f8fa6" for p in Z.pazar])
                    ax.axhline(1.0, color="#999", lw=1); ax.axhline(1.3, color="#c0392b", lw=1.5, ls="--")
                    ax.set_xticks(range(len(Z))); ax.set_xticklabels(et, fontsize=5.5); ax.set_title(bas_, fontsize=8)
                    ax.tick_params(axis="y", labelsize=7)
            pdf.savefig(fig); plt.close(fig); sayfa += 1
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.95, "NEDEN İZ DEĞİL, NE ÖĞRENDİK, SEN NASIL BAKARSIN", [
            "- Senin şeklin (dar, sakin, yükselen dipli taban) büyük yükselişi DAHA SIK getirmiyor; ABD'de çoğu hücrede daha SEYREK. "
            "Geniş, oynak çöküş tabanları 2 katı daha sık yapıyor: oynak hisse iki yöne de çok gider.",
            "- Oynaklığı eşleyince de (R2) sonuç aynı: yalnız BIST 2024-26 hücresi 1,3'ü geçiyor, diğer beş hücre geçmiyor. Tek dönemde "
            "geçen ölçü iz değildir (DERS 1).",
            "- Rüzgâr (D1) şartı olay sayısını hücre başına 4–15'e, genişlik (R1) BIST 2023'te 3'e düşürüyor; bu kadar az olaydan "
            "karar çıkmaz. Olanlar da 1,3'ü dört hücrede birden geçmiyor.",
            "- Tutarlı tek görüntü: BIST'te bu tabanlardan sonra önce −%20 gelme oranı eşli kutunun yarısı ile üçte ikisi arası (3 dönemde de). "
            "ABD'de yok. Yani BIST'te 'dibi kolay kırılmayan sakin taban' ama 'sonra uçar' değil. A13 doji kutusu ile aynı aile.",
            "- TEHOL'ü 10 kat yapan şekil değil, sonrasında gelen alıcıydı (Ders 2: fonlar yükselişin içinde girdi).",
            "",
            "Kendin bakarken: bir tabanı gördüğünde aynı hissenin ve aynı dönemin GENİŞ çöküş tabanlarını yanına koy. Senin "
            "sevdiğin dar taban onlardan daha iyi gitmiyorsa, karar şekilden değil başka bir şeyden (rüzgâr, alıcı, haber) gelmeli.",
        ])
        pdf.savefig(fig); plt.close(fig); sayfa += 1
    return sayfa


# ---------------------------------------------------------------- K16 düzgün dip devam denemeleri (Cemal 24 Eki; şartlar önceden)
# Ç75: düzgün dip tek başına (çöküş sonrası taban, K13'ün bant/mum/U/eğim şartları gevşek). Ç76/Ç77: Cemal'in başarı ölçüsü (250 günde
# dip kırılmadan 2 kat) Ç73 (K13b) ve Ç75 olaylarında, eşli kutuya göre; karar fi_k14_karar (dört hücre >= 1,3, n >= 30).
FI_K16_GEVSEK = {**FI_K13_ESIK, "bant": 10.0, "mum": 99.0, "u": 0.0, "egim": (-9.0, 9.0), "dip_taban": 0.20}


def fon_izi_k16(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    """K13b (FI_K13B_ESIK) ve gevşek düzgün dip (FI_K16_GEVSEK) olayları -> 2 kat / +%50 / önce -%20, eşli kutuya göre; CSV."""
    A = A or FIAyar(); os.makedirs(A.cikti, exist_ok=True)
    Z: Dict[str, List[pd.DataFrame]] = {"k13b": [], "gevsek": []}
    for pazar in ("BIST", "ABD"):
        try:
            V = fi_k1_veri(A.veri[pazar], pazar, A)
        except Exception as ex:
            filog.warning("K16 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        for ad, E in (("k13b", FI_K13B_ESIK), ("gevsek", FI_K16_GEVSEK)):
            O = fi_k13_tara(V, E).reset_index(drop=True); Es = fi_k14_esli(V, O).reset_index(drop=True)
            O = O.join(fi_k10_sonuc(V, O.sembol, O.bilgi), how="left").join(fi_k14_yukselis(V, O), how="left") if len(O) else O
            Es = Es.join(fi_k10_sonuc(V, Es.sembol, Es.bilgi), how="left").join(fi_k14_yukselis(V, Es), how="left") if len(Es) else Es
            filog.info("K16 %s %s: %d olay, %d esli kutu", pazar, ad, len(O), len(Es))
            Z[ad].append(fi_k14_kiyas(O, Es, pazar, FI_K13_DONEM))
            O.assign(pazar=pazar).to_csv(os.path.join(A.cikti, f"k16_{ad}_{pazar}_olaylar.csv.gz"), index=False)
    sonuc = {}
    for ad, L in Z.items():
        if L:
            Zk = pd.concat(L, ignore_index=True); Zk.to_csv(os.path.join(A.cikti, f"k16_{ad}_ozet.csv"), index=False)
            sonuc[ad] = (Zk,) + fi_k14_karar(Zk, "kat2")
    return {"sonuc": sonuc}


def fi_k12_ders5(V: Dict[str, pd.DataFrame], O: pd.DataFrame, KH: pd.DataFrame, K16: Dict[str, pd.DataFrame], yol: str,
                 kod: str = "TEHOL") -> int:
    """Ders 5 (Cemal 24 Eki: 'Ekim 2024 bölgesinin dibi düzgün, 2021'inki değil'): (1) iki TEHOL bölgesi, dip bandı (dip ile dip x
    (1 + 2 mum) arası) gölgeli, banda değen barlar işaretli, dip tabanı ölçüsü; (2) evrende düzgün dipli 6 örnek (hisse adı yok,
    ölçüye göre sıralı, sonuç başlıkta); (3) test: tek cetvel (önce +%20, eşli taban) ve 2 kat (eşli kutu), 1,3 çizgisi; (4) özet.
    O = K13b olayları (BIST, sonuç sütunlarıyla), KH = karne_hucre (Ç73, Ç75), K16 = {'k13b': ozet, 'gevsek': ozet}."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    A4 = (8.27, 11.69)
    AYLAR = ("Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara")
    tr = lambda x: f"{pd.Timestamp(x).day} {AYLAR[pd.Timestamp(x).month - 1]} {pd.Timestamp(x).year}"

    def yazi(fig, y, baslik, satirlar, boy=10, gen=90):
        fig.text(0.07, y, baslik, fontsize=14, weight="bold", va="top", color="#1f2a44"); y -= 0.042
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= 0.023
            y -= 0.005
        return y

    def kutu(ax, d, b, e, baslik, oncesi=40, sonrasi=40, kucuk=False):
        i0 = d.index.get_loc(d.index[d.index >= pd.Timestamp(b)][0]); i1 = d.index.get_loc(d.index[d.index <= pd.Timestamp(e)][-1])
        o = fi_k13_olc(d, i0, i1)
        w = d.iloc[max(0, i0 - oncesi):min(len(d), i1 + sonrasi + 1)]
        L = d.Low.iloc[i0:i1 + 1]; dip = L.min()
        mum = float(np.median((d.High.iloc[i0:i1 + 1] - L) / d.Close.shift(1).iloc[i0:i1 + 1]))
        ust = dip * (1 + 2 * mum)
        ax.axvspan(d.index[i0], d.index[i1], color="#fff4d6", zorder=0)
        ax.fill_between([d.index[i0], d.index[i1]], dip, ust, color="#27ae60", alpha=0.25, zorder=1)
        ax.vlines(w.index, w.Low, w.High, color="#7f8c8d", lw=0.6 if kucuk else 0.8)
        ax.plot(w.index, w.Close, color="#1f2a44", lw=0.8 if kucuk else 1.1)
        t = L[L <= ust]
        ax.scatter(t.index, t.values, color="#c0392b", s=6 if kucuk else 12, zorder=3)
        ax.set_yscale("log"); ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.set_xticks([]); ax.tick_params(labelsize=6 if kucuk else 8)
        ax.set_title(f"{baslik} · dip tabanı {o['dip_taban']:.2f}".replace(".", ","), fontsize=8 if kucuk else 10)
        return o

    d = V[kod]
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "DERS 5: DÜZGÜN DİP — SENİN GÖZÜN NE GÖRÜYOR?", [
            "Sen: 'Ekim 2024 bölgesinin dibi düzgün, 2021'inki değil.' Ölçüye çevirdim: kutudaki barların ne kadarı dibin hemen yanında "
            "(dip ile dip + 2 mum boyu arası, yeşil bant)? Kırmızı nokta = banda değen gün. Bu orana 'dip tabanı' dedim.",
            "2024: dip haftalarca test edilmiş, zemin düz (senin 50 günlük bölgende 0,26; kodun 4 Eki dibinden başlayan 31 günlük "
            "kutusunda 0,45). 2021: dip tek günlük iğne, fiyat hemen %12-21 yukarıda oturmuş (0,06). Eşik sonuç görülmeden yazıldı: "
            "dip tabanı ≥ 0,20.",
        ], boy=9.5)
        kutu(fig.add_axes([0.08, 0.43, 0.88, 0.25]), d, "2024-10-07", "2024-12-16", f"{kod} {tr('2024-10-07')} – {tr('2024-12-16')}")
        kutu(fig.add_axes([0.08, 0.08, 0.88, 0.25]), d, "2021-04-21", "2021-06-08", f"{kod} {tr('2021-04-21')} – {tr('2021-06-08')}")
        pdf.savefig(fig); plt.close(fig)
        X = O[O.sembol != kod].sort_values("dip_taban", ascending=False).head(6)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "EVRENDE DÜZGÜN DİPLİ 6 ÖRNEK (BIST, hisse adı yok)", [
            "Dip tabanı en yüksek 6 olay (sonuca bakılmadan seçildi). Başlıkta yıl ve 60 günde önce ne geldi. Kendi gözünle bak: "
            "senin 'düzgün dip' dediğin bunlar mı?"], boy=9.5)
        for k, r in enumerate(X.itertuples()):
            s = "önce +%20" if getattr(r, "k20", np.nan) == 1 else ("önce −%20" if getattr(r, "dus", np.nan) == 1 else "yatay")
            kutu(fig.add_axes([0.07 + (k % 2) * 0.47, 0.62 - (k // 2) * 0.28, 0.41, 0.21]), V[r.sembol], r.dip, r.bilgi,
                 f"{pd.Timestamp(r.bilgi).year} — {s}", oncesi=30, sonrasi=60, kucuk=True)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "TEST: DÜZGÜN DİP FARK YARATIYOR MU?", [
            "Üst: tek cetvel (60 günde önce +%20, eşli taban: aynı ay × momentum × likidite). Ç73 = TEHOL tipi taban + düzgün dip; "
            "Ç75 = yalnız düzgün dip (çöküş sonrası taban). Alt: senin ölçün — 250 günde dip kırılmadan 2 kat, eşli kutuya (aynı "
            "çöküş, şekilsiz) göre. Kırmızı çizgi 1,3: dört hücrede (BIST/ABD 2023 ve 2024-26) geçmesi gerekir."], boy=9.5)
        ax = fig.add_axes([0.10, 0.50, 0.85, 0.30])
        et, deg, renk = [], [], []
        for kd, rk in (("Ç73", "#1f2a44"), ("Ç75", "#7f8fa6")):
            for r in KH[KH.kod == kd].itertuples():
                et.append(f"{kd}\n{r.pazar} {r.donem}\nn={int(r.n)}"); deg.append(r.ana_kat); renk.append(rk)
        ax.bar(range(len(deg)), deg, color=renk); ax.axhline(1.3, color="#c0392b", ls="--", lw=2); ax.axhline(1.0, color="#999")
        ax.set_xticks(range(len(deg))); ax.set_xticklabels(et, fontsize=5.5); ax.set_ylabel("önce +%20, eşli kat")
        ax = fig.add_axes([0.10, 0.10, 0.85, 0.30])
        et, deg, renk = [], [], []
        for ad, rk in (("k13b", "#1f2a44"), ("gevsek", "#7f8fa6")):
            Z = K16.get(ad)
            if Z is None:
                continue
            for r in Z.itertuples():
                et.append(f"{'Ç76' if ad == 'k13b' else 'Ç77'}\n{r.pazar} {r.donem}\nn={int(r.n)}"); deg.append(r.kat2_kat); renk.append(rk)
        ax.bar(range(len(deg)), np.nan_to_num(np.array(deg, float)), color=renk)
        ax.axhline(1.3, color="#c0392b", ls="--", lw=2); ax.axhline(1.0, color="#999")
        ax.set_xticks(range(len(deg))); ax.set_xticklabels(et, fontsize=5.5); ax.set_ylabel("2 kat (dip kırılmadan), eşli kutu katı")
        pdf.savefig(fig); plt.close(fig)
    return 3


# ---------------------------------------------------------------- K17 iki yuvarlama: önce aşağı (∩), hemen ardından yukarı (∪)
# CEMAL (24 Eki, TEHOL 21 Nis - 8 Haz 2021 grafiği): "1'de aşağı yuvarlama var, sonraki 2. bölge istenilen bölge; bu iki bölge peş peşe
# gelmiş, daha önce böyle görmedim." 2019 örneğine: "bir yükseliş gelmiş, bu kadar bir yükseliş yeterli" -> başarı ölçüsü önce +%20 (k20).
# Ölçü (gün t, gerçek zamanlı): dip j = [t-120, t-25] en düşük Low, önceki 60 barın da dibi, dipten sonra yeni dip yok, öncesinde
# >= %40 düşüş. p = [j+5, t-10] en yüksek kapanış (1'in tepesi); m = [p, t] en düşük kapanış (2'nin dibi). 1 = log kapanış [j+1, m]:
# parabol a < 0, tepe noktası ortada (x 0,15-0,85), uyum R2 >= r2. 2 = log kapanış [p, t]: a > 0, dip noktası ortada, son eğim > 0,
# R2 >= r2. 2'nin en düşük Low'u dipten >= %3 yukarıda; 1'in tepesinden 2'nin dibine -%5..-%30; iki bölge >= 10 bar; m t'den >= 5 bar önce.
# Eşikler TEHOL 2021'den (1: 22 Nis dip -> 20 May tepe -> 28 May dip -%12, R2 0,43; 2: R2 0,92, ilk sinyal 3 Haz) ve evren sonucu
# görülmeden yazıldı. Y2: + 2'nin dip tabanı >= 0,20 (K13b ölçüsü 2. bölgeye). Y3: Y1 kutusunun tavanı (en yüksek kapanış) 60 barda
# dip kırılmadan geçilirse kırılım günü (fi_k14_kirilim). Eşli kutu: aynı çöküş bağlamı, desen yok (fi_k14_esli).
FI_K17_ESIK = {"dusus": -0.40, "bar": (25, 120), "yan": 10, "m_son": 5, "tepe": (0.15, 0.85), "r2": 0.40, "derin": (-0.30, -0.05),
               "ust_dip": 1.03}
FI_K17_Y2 = {**FI_K17_ESIK, "dip_taban": 0.20}
# Tur 2 (Y1-Y3 iz değil çıktıktan sonra, sonuç görülmeden yazıldı): Y4 sıkı yuvarlama (iki bölgede de R2 >= 0,70: gözle 'temiz yay');
# Y5 Y1 + sektör rüzgârı bilgi gününde (D9b, fi_k14_ruzgar; CLAUDE.md 'rüzgâr olmadan çöl aranmaz'); Y6 hafif silkeleme (1'in tepesinden
# 2'nin dibine -%5..-%15; Cemal'in 'iki kutu' kuralında giriş = 2. kutudan sonraki hafif silkeleme; TEHOL 2021 -%12).
FI_K17_Y4 = {**FI_K17_ESIK, "r2": 0.70}
FI_K17_Y6 = {**FI_K17_ESIK, "derin": (-0.15, -0.05)}
K17_VARYANT = ("Y1", "Y2", "Y3", "Y4", "Y5", "Y6")


def _fi_k17_parabol(y: np.ndarray) -> Tuple[float, float, float, float]:
    """y'ye x = 0..1 üzerinde 2. derece parabol: (a, tepe/dip noktası x*, R2, x=1'deki eğim)."""
    x = np.linspace(0.0, 1.0, len(y)); a, b, c0 = np.polyfit(x, y, 2)
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float(((y - (a * x * x + b * x + c0)) ** 2).sum()) / ss if ss > 0 else 0.0
    return float(a), float(-b / (2 * a)) if a else np.nan, r2, float(2 * a + b)


def fi_k17_olc(d: pd.DataFrame, j: int, p: int, m: int, t: int) -> Dict[str, float]:
    """Bölge 1 = [j+1, m] (aşağı yuvarlama), bölge 2 = [p, t] (yukarı yuvarlama) ölçüleri + 2'nin dip tabanı."""
    c = d.Close.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float)
    a1, x1, r1, _ = _fi_k17_parabol(np.log(c[j + 1:m + 1]))
    a2, x2, r2, e2 = _fi_k17_parabol(np.log(c[p:t + 1]))
    w = slice(p, t + 1); mum = float(np.median((h[w] - l[w]) / c[p - 1:t])) if p > 0 else np.nan
    return {"bar": t - j + 1, "bar1": m - j, "bar2": t - p + 1, "a1": a1, "x1": x1, "r2_1": r1, "a2": a2, "x2": x2, "r2_2": r2,
            "egim2": e2, "derin": c[m] / c[p] - 1, "ust_dip": l[w].min() / l[j],
            "dip_taban2": float(np.mean(l[w] <= l[w].min() * (1 + 2 * mum))) if mum == mum else np.nan,
            "tepe1": d.index[p], "dip2": d.index[m]}


def fi_k17_tara(V: Dict[str, pd.DataFrame], E: Dict[str, Any] = FI_K17_ESIK) -> pd.DataFrame:
    """Her hissede her gün t: FI_K17_ESIK şartları (yukarıdaki blok). Aynı dip için ilk gün olay; hissede 60 barda tek.
    Dönüş: sembol, dip, bilgi (= t, giriş ertesi açılış), ölçüler."""
    sat: List[Dict[str, Any]] = []
    b0, b1 = E["bar"]; yan = E["yan"]; t0, t1 = E["tepe"]
    for s, d in V.items():
        try:
            n = len(d)
            if n < 400:
                continue
            l = d.Low.to_numpy(float); c = d.Close.to_numpy(float)
            Lw = np.lib.stride_tricks.sliding_window_view(l, b1 - b0 + 1)          # pencere [t-b1, t-b0]
            jrel = Lw.argmin(axis=1)
            sonmin = pd.Series(l).rolling(b0).min().to_numpy()                    # [t-b0+1, t]
            gorulen = set(); son_olay = -10 ** 9
            for t in range(max(b1, 320), n):
                k = t - b1
                if k >= len(jrel):
                    break
                j = k + jrel[k]
                if j in gorulen or t - son_olay < 60 or not (sonmin[t] >= l[j]) or l[j] > l[max(0, j - 60):j].min():
                    continue
                if not (l[j] > 0) or l[j] / c[max(0, j - 60):j].max() - 1 > E["dusus"]:
                    continue
                p = j + 5 + int(np.argmax(c[j + 5:t - yan + 1]))
                m = p + int(np.argmin(c[p:t + 1]))
                if m - j < yan or t - p + 1 < yan or t - m < E["m_son"]:
                    continue
                o = fi_k17_olc(d, j, p, m, t)
                if not (o["a1"] < 0 and t0 <= o["x1"] <= t1 and o["r2_1"] >= E["r2"] and o["a2"] > 0 and t0 <= o["x2"] <= t1
                        and o["r2_2"] >= E["r2"] and o["egim2"] > 0 and E["derin"][0] <= o["derin"] <= E["derin"][1]
                        and o["ust_dip"] >= E["ust_dip"]):
                    continue
                if "dip_taban" in E and not (o["dip_taban2"] >= E["dip_taban"]):   # Y2: 2. bölgenin dibi düzgün
                    continue
                gorulen.add(j); son_olay = t
                sat.append({"sembol": s, "dip": d.index[j], "bilgi": d.index[t], **o})
        except Exception as ex:   # tek hisse bozuksa digerleri devam eder
            filog.warning("K17 %s atlandi: %s", s, ex)
    return pd.DataFrame(sat)


def fon_izi_k17(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    """K17 sürücü: Y1 (iki yuvarlama), Y2 (+ 2'nin düzgün dibi), Y3 (Y1 + kutu tavanı kırılımı), tur 2 Y4-Y6 olayları ve eşli kutular, BIST + ABD;
    k20 / dus / trail (fi_k10_sonuc) ve 2 kat (fi_k14_yukselis). Karar fi_k14_karar(k20). Çıktı k17_olaylar.csv.gz, k17_ozet.csv."""
    A = A or FIAyar(); os.makedirs(A.cikti, exist_ok=True)
    Z: List[pd.DataFrame] = []; X: List[pd.DataFrame] = []
    for pazar in ("BIST", "ABD"):
        try:
            V = fi_k1_veri(A.veri[pazar], pazar, A)
        except Exception as ex:
            filog.warning("K17 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        Y1 = fi_k17_tara(V, FI_K17_ESIK).reset_index(drop=True)
        Y2 = fi_k17_tara(V, FI_K17_Y2).reset_index(drop=True)
        Y3 = fi_k14_kirilim(V, Y1).reset_index(drop=True) if len(Y1) else Y1
        Es = fi_k14_esli(V, Y1).reset_index(drop=True)
        Y4 = fi_k17_tara(V, FI_K17_Y4).reset_index(drop=True)
        Y6 = fi_k17_tara(V, FI_K17_Y6).reset_index(drop=True)
        try:
            W = fi_k14_ruzgar(V, fi_k14_sektor(pazar))
            Y5 = Y1[[bool(W.at[pd.Timestamp(b), s_]) if pd.Timestamp(b) in W.index and s_ in W.columns else False
                     for s_, b in zip(Y1.sembol, Y1.bilgi)]].reset_index(drop=True) if len(Y1) else Y1
        except Exception as ex:   # sektör dosyası yoksa Y5 boş kalır, diğerleri sürer
            filog.warning("K17 %s rüzgâr hesaplanamadı, Y5 boş: %s", pazar, ex); Y5 = Y1.iloc[0:0]
        P: Dict[str, pd.DataFrame] = {}
        for ad, O in (("Y1", Y1), ("Y2", Y2), ("Y3", Y3), ("Y4", Y4), ("Y5", Y5), ("Y6", Y6), ("esli", Es)):
            if len(O):
                O = O.join(fi_k10_sonuc(V, O.sembol, O.bilgi), how="left").join(fi_k14_yukselis(V, O), how="left")
            filog.info("K17 %s %s: %d olay", pazar, ad, len(O))
            P[ad] = O; X.append(O.assign(pazar=pazar, varyant=ad))
        for ad in K17_VARYANT:
            Z.append(fi_k14_kiyas(P[ad], P["esli"], pazar, FI_K13_DONEM).assign(varyant=ad))
    if not Z:
        raise RuntimeError("K17: hiçbir pazarın verisi okunamadı")
    Zk = pd.concat(Z, ignore_index=True); Zk.to_csv(os.path.join(A.cikti, "k17_ozet.csv"), index=False)
    pd.concat([x for x in X if len(x)], ignore_index=True).to_csv(os.path.join(A.cikti, "k17_olaylar.csv.gz"), index=False)
    sonuc = {ad: (Zk[Zk.varyant == ad],) + fi_k14_karar(Zk[Zk.varyant == ad], "k20") for ad in K17_VARYANT}
    return {"sonuc": sonuc, "ozet": Zk}


def fi_k12_ders6(V: Dict[str, pd.DataFrame], O: pd.DataFrame, KH: pd.DataFrame, yol: str, kod: str = "TEHOL") -> int:
    """Ders 6 (Cemal 24 Eki: '1'de aşağı yuvarlama, 2. bölge istenen, ikisi peş peşe'): (1) TEHOL 2021 şablonu: dip, 1. bölge yayı,
    2. bölge kâsesi, sinyal günü, giriş, +%20 / -%10 çizgileri, hacim; (2) evrende 6 örnek (BIST Y1, yay uyumuna göre sıralı, sonuca
    bakılmadan; hisse adı yok); (3) test: tek cetvel Ç78-Ç83 karar hücreleri, 1,3 çizgisi. O = k17 olayları (BIST, sonuçlu),
    KH = karne_hucre."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    A4 = (8.27, 11.69)
    AYLAR = ("Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara")
    tr = lambda x: f"{pd.Timestamp(x).day} {AYLAR[pd.Timestamp(x).month - 1]} {pd.Timestamp(x).year}"

    def yazi(fig, y, baslik, satirlar, boy=9.5, gen=92):
        fig.text(0.07, y, baslik, fontsize=14, weight="bold", va="top", color="#1f2a44"); y -= 0.040
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= 0.021
            y -= 0.004
        return y

    def sablon(ax, axh, d, dip, bilgi, baslik, kucuk=False, sonrasi=60):
        tar = d.index; j = int(tar.searchsorted(pd.Timestamp(dip))); t = int(tar.searchsorted(pd.Timestamp(bilgi)))
        c = d.Close.to_numpy(float)
        p = j + 5 + int(np.argmax(c[j + 5:t - FI_K17_ESIK["yan"] + 1])); m = p + int(np.argmin(c[p:t + 1]))
        w = d.iloc[max(0, j - 30):min(len(d), t + sonrasi + 1)]
        ax.axvspan(tar[j], tar[t], color="#fff4d6", zorder=0)
        ax.vlines(w.index, w.Low, w.High, color="#95a5a6", lw=0.5 if kucuk else 0.8)
        ax.plot(w.index, w.Close, color="#1f2a44", lw=0.7 if kucuk else 1.0)
        for (a, b), renk, et in (((j + 1, m), "#e67e22", "1 aşağı yuvarlama"), ((p, t), "#27ae60", "2 yukarı yuvarlama")):
            y = np.log(c[a:b + 1]); x = np.linspace(0, 1, len(y)); k_ = np.polyfit(x, y, 2)
            ax.plot(tar[a:b + 1], np.exp(np.polyval(k_, x)) * (1.06 if renk == "#e67e22" else 0.95), color=renk, lw=2.2 if not kucuk else 1.5)
            if not kucuk:
                ax.text(tar[(a + b) // 2], np.exp(np.polyval(k_, 0.5)) * (1.12 if renk == "#e67e22" else 0.89), et, color=renk,
                        fontsize=9, ha="center", weight="bold")
        ax.scatter([tar[j]], [d.Low.iloc[j]], color="#c0392b", s=14 if kucuk else 30, zorder=4)
        if t + 1 < len(d):
            g = d.Open.iloc[t + 1]
            ax.axvline(tar[t], color="#2c3e50", ls=":", lw=1)
            ax.scatter([tar[t + 1]], [g], marker="^", color="#2980b9", s=20 if kucuk else 50, zorder=5)
            ax.axhline(g * 1.2, color="#27ae60", ls="--", lw=0.8); ax.axhline(g * 0.9, color="#c0392b", ls="--", lw=0.8)
            if not kucuk:
                ax.text(w.index[-1], g * 1.2, " +%20", color="#27ae60", fontsize=8, va="bottom", ha="right")
                ax.text(w.index[-1], g * 0.9, " −%10", color="#c0392b", fontsize=8, va="top", ha="right")
                ax.text(tar[t], ax.get_ylim()[1], " sinyal günü → ertesi açılış giriş (▲)", fontsize=7.5, va="top")
        ax.set_yscale("log"); ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.set_xticks([]); ax.tick_params(labelsize=6 if kucuk else 8); ax.set_title(baslik, fontsize=8 if kucuk else 10)
        if axh is not None:
            axh.bar(w.index, w.Volume, color="#7f8c8d", width=1.0); axh.set_xticks([]); axh.set_yticks([]); axh.set_ylabel("hacim", fontsize=7)

    d = V[kod]
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "DERS 6: İKİ YUVARLAMA — ÖNCE AŞAĞI, HEMEN ARDINDAN YUKARI", [
            "Sen (TEHOL 21 Nis – 8 Haz 2021): '1'de aşağı yuvarlama var, sonraki 2. bölge istenen bölge; ikisi peş peşe gelmiş, daha "
            "önce böyle görmedim.' 2019 örneğine de: 'bir yükseliş gelmiş, bu kadar yükseliş yeterli' → başarı ölçüsü: 60 günde önce +%20.",
            "Ölçü (sonuç görülmeden, TEHOL 2021'e göre): çöküş (≥ %40) dibinden sonra yeni dip yok; 1 = dipten 2'nin dibine kapanışlar "
            "tepesi ortada bir yay (∩, turuncu); 2 = 1'in tepesinden bugüne kapanışlar dibi ortada bir kâse (∪, yeşil), sonu yukarı "
            "dönmüş; 2'nin dibi asıl dibin ≥ %3 üstünde; 1'in tepesinden 2'nin dibine −%5…−%30. Kâse yukarı döndüğü ilk gün sinyal.",
            "Grafikte: kırmızı nokta = dip, sarı = kutu, noktalı çizgi = sinyal günü, ▲ = ertesi açılış giriş, kesikli = +%20 / −%10.",
        ])
        sablon(fig.add_axes([0.08, 0.30, 0.88, 0.36]), fig.add_axes([0.08, 0.22, 0.88, 0.07]), d, "2021-04-22", "2021-06-04",
               f"{kod} {tr('2021-04-22')} – {tr('2021-06-04')} (senin işaretlediğin bölge)")
        yazi(fig, 0.17, "Grafikte nasıl görünür, nasıl görünmez", [
            "- Görünür: dipten sonra fiyat bir süre yükselip yavaşça geri döner (yay), sonra daha yukarıda yeni bir küçük çukur açar "
            "ve çukurun sağ kenarı yukarı kıvrılır.",
            "- Görünmez: hangisinin +%20'ye gideceği. Aynı şekil evrende yüzlerce kez çıkıyor; sonrası yazı-tura (3. sayfa)."], boy=9)
        pdf.savefig(fig); plt.close(fig)
        X = O[(O.varyant == "Y1") & (O.sembol != kod)].assign(r=lambda x: x.r2_1 + x.r2_2).sort_values("r", ascending=False).head(6)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "EVRENDE İKİ YUVARLAMA: 6 ÖRNEK (BIST, hisse adı yok)", [
            "Yayı ve kâsesi en düzgün 6 olay (iki parabol uyumunun toplamı; sonuca bakılmadan seçildi). Başlıkta yıl ve 60 günde önce "
            "ne geldi. Kendi gözünle bak: senin '1 aşağı, 2 yukarı' dediğin bunlar mı?"])
        for k, r in enumerate(X.itertuples()):
            s = "önce +%20" if getattr(r, "k20", np.nan) == 1 else ("önce −%20" if getattr(r, "dus", np.nan) == 1 else "yatay")
            sablon(fig.add_axes([0.07 + (k % 2) * 0.47, 0.62 - (k // 2) * 0.28, 0.41, 0.21]), None, V[r.sembol], r.dip, r.bilgi,
                   f"{pd.Timestamp(r.bilgi).year} — {s}", kucuk=True)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "TEST: İKİ YUVARLAMA FARK YARATIYOR MU?", [
            "Tek cetvel: 60 günde önce +%20 (önce −%10'dan), eşli taban (aynı ay × momentum × likidite). Kırmızı çizgi 1,3: dört "
            "karar hücresinin (BIST/ABD 2023 ve 2024-26) hepsinde geçmeli. Ç78 iki yuvarlama · Ç79 + 2'nin dibi düzgün · Ç80 + kutu "
            "tavanı kırılımı · tur 2 (önceden yazıldı): Ç81 sıkı yay · Ç82 + sektör rüzgârı · Ç83 hafif silkeleme (−%5…−%15)."])
        ax = fig.add_axes([0.10, 0.42, 0.85, 0.40])
        et, deg, renk = [], [], []
        RENK = {"BIST": "#1f2a44", "ABD": "#7f8fa6"}
        for kd in ("Ç78", "Ç79", "Ç80", "Ç81", "Ç82", "Ç83"):
            for r in KH[(KH.kod == kd) & (KH.donem.isin(["2023", "2024-26"]))].itertuples():
                et.append(f"{kd}\n{r.pazar}\n{r.donem}\nn={int(r.n)}"); deg.append(r.ana_kat); renk.append(RENK.get(r.pazar, "#999"))
        ax.bar(range(len(deg)), np.nan_to_num(np.array(deg, float)), color=renk)
        ax.axhline(1.3, color="#c0392b", ls="--", lw=2); ax.axhline(1.0, color="#999")
        ax.set_xticks(range(len(deg))); ax.set_xticklabels(et, fontsize=4.6); ax.set_ylabel("önce +%20, eşli kat")
        yazi(fig, 0.34, "Sonuç ve ders", [
            "- İZ DEĞİL: altı denemenin hiçbiri dört hücrede 1,3'e çıkmadı; çoğu hücre 0,85-1,25 (= sıradan hisse). En yakın: Ç78 "
            "ABD 2023 1,41 ve Ç83 ABD 2023 1,37 — tek hücre, öteki hücreler 1,0 civarı.",
            "- Önce −%20 de eşli tabandan sık (1,0-1,6): çöküş sonrası hisse oynak; şekil bu oynaklığı azaltmıyor.",
            f"- 2'nin dibinin düzgün olması (Ç79) neredeyse her kâsede var ({int((O.varyant == 'Y1').sum())}'in "
            f"{int((O.varyant == 'Y2').sum())}'i): ayırıcı değil.",
            "- Senin gözün doğru bir şekli görüyor ve kod da aynı şekli buluyor (TEHOL 2021 dahil); ama şekil tek başına sonrasını "
            "söylemiyor. Karar yine kırılım + trail + boyutta."], boy=9)
        pdf.savefig(fig); plt.close(fig)
    return 3


# ---------------------------------------------------------------- K18 Cemal'in kendi vakaları: ortak iz var mı? (Cemal 25 Eki)
# CEMAL (25 Eki): "TEHOL'de Ekim çölü vardı, koştu; BINBN'i önceden test etmiştim, sabırsız olduğum için sattım; KTLEV'de dev U tabanı,
# aldım sattım, çok uzun sürdü; ESCAR küçüktü, silkelemede zararına sattım; Vişne maden koşmadı (dalavere); Euro'da 24 Aralık 2024 dev
# hacim barı; BORLS; VERUS'u kod o zamanlar bulmuştu; MANAS 21 Temmuz 2025 atılım barı, 29 Ekim 2025 yeniden oluştu, silkeleme çölün
# biraz altına sarktı, Kasım 2025'te koştu; PAPIL zarar. Bu dediklerimin ortak izleri var mı yok mu, bölgeleri önce test ederek bul,
# bana sormadan; 'doğru' deme: kod bunları buldu dediğin hisselerde bu ortak iz var, bunlar koştu, şu koşmadı de."
# VAKALAR (FI_K18_VAKA): bölge Cemal'in kalibre_etiketler.csv etiketi varsa o, yoksa grafikten (atılımdan önceki sıkışma). 'Euro' =
# EUHOL: 24.12.2024 TL hacmi önceki 60 gün medyanının 13,6 katı (o gün BIST'te 2. en büyük; aynı gün EUYO 6x, TEHOL 5,5x). 'Hakiş'
# veride eşlenemedi (HATSN, HKTM, HRKET, HTTBT grafiklerinde çöl + koşu yok). VERUS: v1_final_BIST 21.04.2025 sinyali (sonra +%38).
# ÖLÇÜ (gün t, gerçek zamanlı; yalnız t ve öncesi): t'de kapanış son 20 barın en yüksek gövde üstünü ve kutu tavanını x1,002 geçer
# (ATILIM). Kutu = [i0, t-1]: t-1'de biten, bandı (en yüksek gövde üstü / en düşük Low - 1) <= bant olan en uzun pencere
# (bar[0]..bar[1]); kutu, pencerenin dip bölgesine (en düşük Low x 1,05) İLK değdiği günden başlar (D13 kural 1: çöl yeni dipten
# sonra sayılır; dip kutunun sonunda yeniden test edilse de başlangıç kaymaz: BINBN, MANAS). Önce düşüş = kutu dibi / kutudan önceki
# 250 barın en yüksek High - 1. PROFİL: mum_kat = kutu medyan mum (H-L / önceki kapanış) / kutudan önceki 40 bar (düşüş mumları);
# hacim_kat = kutu medyan TL hacmi / kutudan önceki 60 bar.
# EŞİKLER Cemal'in KOŞAN vakalarından, evren sonucu görülmeden (25 Eki): düşüş <= -%30, kutu 20-130 bar, bant <= %50, mum_kat <= 1,0,
# hacim_kat <= 1,0. Atılım günü ölçüsü: TEHOL 0,65/0,71, BINBN 0,42/0,59, KTLEV 0,96/0,62, ESCAR 0,37/0,53, BORLS 0,75/0,27, MANAS 0,83/0,87;
# VERUS 1,48/1,70 (tutmuyor), EUHOL düşüş sonrası değil (koşu sonrası raf), MANAS-b kutusu 20 bardan kısa.
# EŞLİ: aynı bağlam (aynı düşüş, bant, kutu boyu, aynı atılım), profili tutmayan (mum_kat > 1 ya da hacim_kat > 1); ayrı taranır.
# Varyant (önceden yazıldı): C1 profil; C2 profil + kutu >= 40 bar ('aylarca'); C3 profil + düşüş <= -%50 ('sert çöküş').
# Sonuç: k20 / dus / trail (fi_k10_sonuc), 2 kat kutu dibi kırılmadan 250 bar (fi_k14_yukselis, Cemal'in 'koştu' ölçüsü).
FI_K18_ESIK = {"bar": (20, 130), "son20": 20, "bant": 0.50, "dip_bolge": 0.05, "dusus": -0.30, "mum": 1.0, "hacim": 1.0, "tekrar": 60}
FI_K18_C2 = {**FI_K18_ESIK, "bar": (40, 130)}
FI_K18_C3 = {**FI_K18_ESIK, "dusus": -0.50}
# Tur 2 (C1-C3 İZ DEĞİL çıktıktan sonra, sonuç görülmeden yazıldı, 25 Eki): C4 dar kutu (bant <= %20; TEHOL 0,20, BINBN 0,04,
# ESCAR 0,18, MANAS 0,16/0,18 dar; KTLEV, VERUS, BORLS geniş); C5 kutuda dev hacim barı (kutu içindeki en büyük TL hacim >= kutu
# medyanının 10 katı; Cemal'in EUHOL 24.12.2024 izi: 27 kat); C6 C1 + bilgi gününde sektör rüzgârı (D9b, fi_k14_ruzgar; CLAUDE.md
# 'rüzgâr veya katalizör olmadan çöl aranmaz').
FI_K18_C4 = {**FI_K18_ESIK, "bant": 0.20}
FI_K18_C5 = {**FI_K18_ESIK, "dev_hacim": 10.0}
K18_VARYANT = ("C1", "C2", "C3", "C4", "C5", "C6")
FI_K18_VAKA = [   # (ad, sembol, kutu başı, kutu sonu, Cemal'in sonucu, kaynak)
    ("TEHOL-24", "TEHOL", "2024-10-07", "2024-12-12", "koştu", "Cemal etiketi"),
    ("BINBN-24", "BINBN", "2024-12-17", "2025-01-21", "koştu", "Cemal etiketi (sabırsız sattım)"),
    ("KTLEV-24", "KTLEV", "2024-06-10", "2024-10-15", "koştu", "grafik: dev U tabanı"),
    ("ESCAR-25", "ESCAR", "2025-09-19", "2025-12-11", "koştu", "Cemal etiketi (silkelemede zararına sattım)"),
    ("EUHOL-24", "EUHOL", "2024-11-01", "2025-03-07", "koştu", "24 Ara 2024 dev hacim barı"),
    ("BORLS-26", "BORLS", "2026-01-12", "2026-04-09", "koştu", "grafik"),
    ("VERUS-25", "VERUS", "2025-03-03", "2025-06-30", "koştu", "kod 21 Nis 2025'te bulmuştu"),
    ("MANAS-25a", "MANAS", "2025-06-01", "2025-07-18", "koştu", "Cemal: 21 Tem 2025 atılım barı"),
    ("MANAS-25b", "MANAS", "2025-10-01", "2025-10-28", "koştu", "Cemal: 29 Eki 2025 yeniden, silkeleme, Kasım'da koştu"),
    ("VSNMD-26", "VSNMD", "2025-12-05", "2026-02-27", "koşmadı", "Cemal: koşmadı, dalavere, göz altı"),
    ("PAPIL-25", "PAPIL", "2025-11-12", "2025-12-09", "koşmadı", "Cemal etiketi (OLUMSUZ, zarar)"),
    ("BINBN-26", "BINBN", "2026-02-25", "2026-04-15", "koşmadı", "Cemal etiketi (ÇÖL), sonrası çöküş"),
]


def fi_k18_olc(d: pd.DataFrame, i0: int, t: int) -> Dict[str, Any]:
    """Kutu [i0, t-1] ve t günü (atılım) ölçüleri; yalnız t ve öncesi. Önce düşüş, bant, mum_kat, hacim_kat, atılım getirisi ve hacmi."""
    o = d.Open.to_numpy(float); c = d.Close.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float)
    v = (d.Volume * d.Close).to_numpy(float); m = (h - l) / np.r_[np.nan, c[:-1]]
    w = slice(i0, t); tavan = float(np.maximum(o[w], c[w]).max()); taban = float(l[w].min()); a = max(0, i0 - 250)
    mv = np.median(v[w])
    m0 = np.nanmedian(m[max(1, i0 - 40):i0]) if i0 >= 21 else np.nan          # düşüş mumları (kilitli/işlemsiz günlerde 0 olabilir)
    v0 = np.median(v[max(0, i0 - 60):i0]) if i0 >= 20 else np.nan
    return {"kutu_bas": d.index[i0], "bar": t - i0, "dusus": taban / h[a:i0].max() - 1 if i0 - a >= 20 else np.nan,
            "bant": tavan / taban - 1,
            "mum_kat": float(np.nanmedian(m[w]) / m0) if m0 > 0 else np.nan,
            "hacim_kat": float(mv / v0) if v0 > 0 else np.nan,
            "atilim_getiri": c[t] / c[t - 1] - 1, "atilim_hacim": v[t] / mv if mv > 0 else np.nan,
            "dev_hacim": float(v[w].max() / mv) if mv > 0 else np.nan, "tavan": tavan, "taban": taban}


def _fi_k18_kutu(top: np.ndarray, l: np.ndarray, t: int, E: Dict[str, Any]) -> int:
    """t-1'de biten, bandı <= E['bant'] olan en uzun pencere [t-N, t-1] içinde dip bölgesine ilk değilen bar (kutu başı); yoksa -1."""
    b0, b1 = E["bar"]; a = max(0, t - b1)
    rt = np.maximum.accumulate(top[a:t][::-1]); rl = np.minimum.accumulate(l[a:t][::-1])
    asan = np.flatnonzero(rt / rl - 1 > E["bant"])
    N = int(asan[0]) if len(asan) else t - a
    if N < b0:
        return -1
    lw = l[t - N:t]
    return t - N + int(np.flatnonzero(lw <= lw.min() * (1 + E["dip_bolge"]))[0])


def fi_k18_tara(V: Dict[str, pd.DataFrame], E: Dict[str, Any] = FI_K18_ESIK, profil: Optional[bool] = True) -> pd.DataFrame:
    """Her hissede atılım günleri (FI_K18_ESIK bloğu). profil=True: mum_kat ve hacim_kat eşik altı (C1-C3); False: en az biri
    eşik üstü (EŞLİ); None: hepsi. Hissede E['tekrar'] barda tek olay. Dönüş: sembol, dip (= kutu başı), bilgi (= t), ölçüler."""
    sat: List[Dict[str, Any]] = []
    b0 = E["bar"][0]
    for s, d in V.items():
        try:
            n = len(d)
            if n < b0 + 80:
                continue
            o = d.Open.to_numpy(float); c = d.Close.to_numpy(float); l = d.Low.to_numpy(float)
            if not (l > 0).all():
                continue
            top = np.maximum(o, c)
            hh = pd.Series(top).rolling(E["son20"]).max().shift(1).to_numpy()
            son = -10 ** 9
            for t in np.flatnonzero(c > hh * 1.002):
                if t < b0 + 21 or t - son < E["tekrar"]:
                    continue
                i0 = _fi_k18_kutu(top, l, int(t), E)
                if i0 < 0 or t - i0 < b0 or not (c[t] > top[i0:t].max() * 1.002):
                    continue
                r = fi_k18_olc(d, i0, int(t))
                if not (r["dusus"] <= E["dusus"]):
                    continue
                if not (r["mum_kat"] == r["mum_kat"] and r["hacim_kat"] == r["hacim_kat"]):   # ölçülemeyen (kilitli/işlemsiz) kutu: ne profil ne eşli
                    continue
                ok = bool(r["mum_kat"] <= E["mum"] and r["hacim_kat"] <= E["hacim"])
                if profil is not None and ok != profil:
                    continue
                if "dev_hacim" in E and profil and not (r["dev_hacim"] >= E["dev_hacim"]):      # C5: kutuda dev hacim barı
                    continue
                son = int(t)
                sat.append({"sembol": s, "dip": r["kutu_bas"], "bilgi": d.index[t], "profil": ok, **r})
        except Exception as ex:   # tek hisse bozuksa digerleri devam eder
            filog.warning("K18 %s atlandi: %s", s, ex)
    return pd.DataFrame(sat)


def fi_k18_d13(kok: str = ".") -> Optional[Dict[str, Any]]:
    """Üretimdeki D13 tespiti (COL_v1._col_dip2_e) ayrı ad alanında; yoksa None (vaka tablosunda 'kod gördü mü' boş kalır)."""
    import contextlib
    import io
    yol = os.path.join(kok, "COL_v1.py")
    if not os.path.exists(yol):
        filog.warning("K18: %s yok, D13 kontrolü atlandı", yol); return None
    ns: Dict[str, Any] = {"__name__": "col_v1_k18", "VERI": {}}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(open(yol, encoding="utf-8").read(), yol, "exec"), ns)
    except Exception as ex:
        filog.warning("K18: COL_v1 yüklenemedi (%s), D13 kontrolü atlandı", ex); return None
    return ns if "_col_dip2_e" in ns else None


def fi_k18_fon_pay(A: FIAyar, V: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
    """Raporlu fonların (KAP portföy raporları) hisse-ay toplam payı, sermayeye oran (bugünkü sermaye, bölünmeden arındırılmış lot);
    'bil' = o ayın son raporunun yayın anı (gerçek zamanlı kullanım). Veri yoksa None."""
    try:
        L = pd.read_csv(os.path.join(A.kapfon, "liste.csv")); Ek = fi_k9_ekler_oku(A)
        P, _, K = fi_k9_tablolar_guncel(L, Ek, A)
        G, _ = fi_k10_pozisyon(P, K, list(V))
        with open(A.veri["BIST"], "rb") as f:
            ham = pickle.load(f)
        ham = ham["veri"] if isinstance(ham, dict) and "veri" in ham else ham
        M = G.groupby(["kod", "ay"]).agg(nominal=("nominal", "sum"), fon=("fon", "nunique"), bil=("bilinme", "max")).reset_index()
        M = M.merge(fi_k10_oran(V, ham), on=["kod", "ay"], how="left").merge(fi_isy_dolasim(A.isy)[["kod", "sermaye_lot"]], on="kod", how="left")
        M["pay"] = M.nominal * M.oran.fillna(1.0) / M.sermaye_lot
        return M
    except Exception as ex:
        filog.warning("K18: fon payı hesaplanamadı (%s); vaka tablosunda fon sütunları boş", ex); return None


def _fi_k18_pay_an(M: Optional[pd.DataFrame], s: str, t: pd.Timestamp) -> float:
    """t anında bilinen son ayın raporlu fon payı; rapor ayı t'den 3 aydan eskiyse 0 (fonlar çıkmış); fon verisi başlamadan NaN."""
    if M is None or t < M.bil.min():
        return np.nan
    x = M[(M.kod == s) & (M.bil <= t)]
    if not len(x):
        return 0.0
    x = x.sort_values("ay").iloc[-1]
    return float(x.pay) if (t.year * 12 + t.month - 1) - x.ay <= 3 else 0.0


def fi_k18_vaka(V: Dict[str, pd.DataFrame], C1: pd.DataFrame, Es: pd.DataFrame, ns: Optional[Dict[str, Any]],
                M: Optional[pd.DataFrame], E: Dict[str, Any] = FI_K18_ESIK) -> pd.DataFrame:
    """Her vaka: elle kutu ölçüleri (fi_k18_olc; atılım = kutu sonundan sonra kapanışın kutu tavanını x1,002 ilk geçtiği gün), sonuç
    (k20, 2 kat dip kırılmadan, 250 bar en yüksek), fon payı (kutu başı / atılım), üretim D13'ün kutu + atılım arasında 'çöl' dediği gün
    sayısı, K18 tarayıcısının vaka hissesinde [kutu başı - 20, atılım + 20] içinde verdiği C1 / eşli olayı."""
    sat = []
    for ad, s, b, e, cemal, kaynak in FI_K18_VAKA:
        d = V.get(s)
        if d is None:
            filog.warning("K18 vaka %s: veri yok", ad); continue
        o = d.Open.to_numpy(float); c = d.Close.to_numpy(float); n = len(d)
        i0 = int(d.index.searchsorted(pd.Timestamp(b))); i1 = int(d.index.searchsorted(pd.Timestamp(e), side="right")) - 1
        tavan = np.maximum(o[i0:i1 + 1], c[i0:i1 + 1]).max()
        ka = next((t for t in range(i1 + 1, min(n, i1 + 150)) if c[t] > tavan * 1.002), None)
        r: Dict[str, Any] = {"ad": ad, "sembol": s, "bas": b, "son": e, "cemal": cemal, "kaynak": kaynak}
        if ka is None:
            r["atilim"] = pd.NaT; sat.append(r); continue
        r.update({k: v for k, v in fi_k18_olc(d, i0, i1 + 1).items() if k not in ("kutu_bas", "atilim_getiri", "atilim_hacim")})
        v = (d.Volume * d.Close).to_numpy(float); lo = d.Low.to_numpy(float)
        r["atilim"] = d.index[ka]; r["atilim_bekle"] = ka - i1
        r["atilim_getiri"] = c[ka] / c[ka - 1] - 1; r["atilim_hacim"] = v[ka] / np.median(v[i0:i1 + 1])
        r["kutu_alti"] = bool(lo[i1 + 1:ka].min() < r["taban"]) if ka > i1 + 1 else False          # atılımdan önce kutu dibi kırıldı mı
        r["sonra20_tavan"] = lo[ka + 1:ka + 21].min() / r["tavan"] - 1 if ka + 1 < n else np.nan     # atılımdan sonra kutuya geri dönüş
        r["sonra60_dip"] = lo[ka + 1:ka + 61].min() / r["taban"] - 1 if ka + 1 < n else np.nan       # 60 barda kutu dibine göre en derin
        R1 = fi_k10_sonuc(V, pd.Series([s]), pd.Series([d.index[ka]]))
        if len(R1):
            r.update({k: R1.iloc[0][k] for k in ("k20", "dus", "trail") if k in R1})
        Y = fi_k14_yukselis(V, pd.DataFrame({"sembol": [s], "dip": [d.index[i0]], "bilgi": [d.index[ka]]}),
                            {**FI_K14_ESIK, "ufuk": min(250, n - ka - 2)})
        if len(Y):
            r.update({"kat2": Y.iloc[0].kat2, "max_yuk": Y.iloc[0].max_yuk})
        r["ufuk_bar"] = n - ka - 1
        r["fon_pay_kutu"] = _fi_k18_pay_an(M, s, d.index[i0]); r["fon_pay_atilim"] = _fi_k18_pay_an(M, s, d.index[ka])
        r["fon_pay_atilim60"] = _fi_k18_pay_an(M, s, d.index[min(n - 1, ka + 60)])
        if ns is not None:
            gun = [str(d.index[t].date()) for t in range(i0, ka + 1) if ns["_col_dip2_e"](d, t)[0] is not None]
            r["d13_gun"] = len(gun); r["d13_ilk"] = gun[0] if gun else ""
        lo, hi = d.index[max(0, i0 - 20)], d.index[min(n - 1, ka + 20)]
        for et, X in (("c1", C1), ("esli", Es)):
            x = X[(X.sembol == s) & (X.bilgi >= lo) & (X.bilgi <= hi)] if len(X) else X
            r[et + "_gun"] = str(pd.Timestamp(x.bilgi.iloc[0]).date()) if len(x) else ""
        sat.append(r)
    return pd.DataFrame(sat)


def fi_k18_liste(O: pd.DataFrame, bas: str = "2024-01-01") -> pd.DataFrame:
    """Kodun bulduğu (C1, BIST) olaylar, Cemal'in sorduğu biçimde: KOŞTU = 250 barda kutu dibi kırılmadan 2 kat; +%20 GÖRDÜ = 60 barda
    önce +%20 (2 kat değil); KOŞMADI = ikisi de yok; BEKLİYOR = 60 bar dolmadı; fon hissesi işareti (FON_HISSE)."""
    X = O[(O.bilgi >= bas)].copy()
    if not len(X):
        return X
    def sonuc(r) -> str:
        if r.kat2 == 1:
            return "KOŞTU (2 kat)"
        if r.k20 == 1:
            return "+%20 GÖRDÜ"
        return "KOŞMADI" if r.k20 == 0 else "BEKLİYOR"
    X["sonuc"] = [sonuc(r) for r in X.itertuples()]
    X["fon_hissesi"] = X.sembol.isin(FON_HISSE)
    return X.sort_values("bilgi")[["sembol", "dip", "bilgi", "bar", "dusus", "bant", "mum_kat", "hacim_kat", "atilim_getiri",
                                   "k20", "kat2", "max_yuk", "trail", "sonuc", "fon_hissesi"]]


def fon_izi_k18(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    """K18 sürücü: C1-C3 ve eşli taramalar (BIST + ABD), sonuçlar (fi_k10_sonuc, fi_k14_yukselis), dönem kıyası (fi_k14_kiyas,
    k20 ve 2 kat), karar (fi_k14_karar k20); vaka tablosu (BIST; D13 ve fon payı varsa) ve kodun bulduğu liste.
    Çıktı k18_olaylar.csv.gz, k18_ozet.csv, k18_vaka.csv, k18_liste_BIST.csv."""
    A = A or FIAyar(); os.makedirs(A.cikti, exist_ok=True)
    Z: List[pd.DataFrame] = []; X: List[pd.DataFrame] = []; vaka = pd.DataFrame(); liste = pd.DataFrame()
    for pazar in ("BIST", "ABD"):
        try:
            V = fi_k1_veri(A.veri[pazar], pazar, A)
        except Exception as ex:
            filog.warning("K18 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        P: Dict[str, pd.DataFrame] = {}
        for ad, E, pr in (("C1", FI_K18_ESIK, True), ("C2", FI_K18_C2, True), ("C3", FI_K18_C3, True), ("C4", FI_K18_C4, True),
                          ("C5", FI_K18_C5, True), ("esli", FI_K18_ESIK, False)):
            P[ad] = fi_k18_tara(V, E, pr).reset_index(drop=True)
        try:
            W = fi_k14_ruzgar(V, fi_k14_sektor(pazar)); C1 = P["C1"]
            P["C6"] = C1[[bool(W.at[pd.Timestamp(b), s_]) if pd.Timestamp(b) in W.index and s_ in W.columns else False
                          for s_, b in zip(C1.sembol, C1.bilgi)]].reset_index(drop=True) if len(C1) else C1
        except Exception as ex:   # sektör dosyası yoksa C6 boş kalır, diğerleri sürer
            filog.warning("K18 %s rüzgâr hesaplanamadı, C6 boş: %s", pazar, ex); P["C6"] = P["C1"].iloc[0:0]
        for ad in K18_VARYANT + ("esli",):
            O = P[ad]
            if len(O):
                O = O.join(fi_k10_sonuc(V, O.sembol, O.bilgi), how="left").join(fi_k14_yukselis(V, O), how="left")
            filog.info("K18 %s %s: %d olay", pazar, ad, len(O))
            P[ad] = O; X.append(O.assign(pazar=pazar, varyant=ad))
        for ad in K18_VARYANT:
            Z.append(fi_k14_kiyas(P[ad], P["esli"], pazar, FI_K13_DONEM).assign(varyant=ad))
        if pazar == "BIST":
            vaka = fi_k18_vaka(V, P["C1"], P["esli"], fi_k18_d13(), fi_k18_fon_pay(A, V))
            liste = fi_k18_liste(P["C1"]) if len(P["C1"]) else pd.DataFrame()
    if not Z:
        raise RuntimeError("K18: hiçbir pazarın verisi okunamadı")
    Zk = pd.concat(Z, ignore_index=True); Zk.to_csv(os.path.join(A.cikti, "k18_ozet.csv"), index=False)
    pd.concat([x for x in X if len(x)], ignore_index=True).to_csv(os.path.join(A.cikti, "k18_olaylar.csv.gz"), index=False)
    vaka.to_csv(os.path.join(A.cikti, "k18_vaka.csv"), index=False); liste.to_csv(os.path.join(A.cikti, "k18_liste_BIST.csv"), index=False)
    sonuc = {ad: (Zk[Zk.varyant == ad],) + fi_k14_karar(Zk[Zk.varyant == ad], "k20") for ad in K18_VARYANT}
    return {"sonuc": sonuc, "ozet": Zk, "vaka": vaka, "liste": liste}


def fi_k12_ders7(V: Dict[str, pd.DataFrame], vaka: pd.DataFrame, Zk: pd.DataFrame, KH: pd.DataFrame, liste: pd.DataFrame,
                 esli: pd.DataFrame, yol: str) -> int:
    """Ders 7 (Cemal 25 Eki: 'bu dediklerimin ortak izleri var mı; kod bunları buldu dediğin hisselerde bu iz var, bunlar koştu,
    şu koşmadı de'): (1) soru, yöntem, kısa cevap; (2) 12 vaka grafikte: kutu, tavan/taban, atılım ve ertesi açılış girişi, üretim
    D13'ün 'çöl' dediği günler, K18 sinyali, ölçüler, sonuç; (3) ortak iz tablosu (koşan / koşmayan); (4) evren testi: tek cetvel
    Ç85-Ç90 karar hücreleri (1,3 çizgisi) ve önce -%20; (5) kodun bulduğu liste (BIST 2024-26): koştu / +%20 / koşmadı, eşli ile kıyas.
    vaka = k18_vaka.csv, Zk = k18_ozet.csv, KH = karne_hucre.csv, liste = k18_liste_BIST.csv, esli = BIST eşli olaylar (2024-26)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    A4 = (8.27, 11.69)
    AYLAR = ("Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara")
    tr = lambda x: f"{pd.Timestamp(x).day} {AYLAR[pd.Timestamp(x).month - 1]} {pd.Timestamp(x).year}"
    yz = lambda x: (("−" if x < 0 else "") + f"%{abs(100 * x):.0f}") if x == x else "—"
    vg = lambda x, k=2: (f"{x:.{k}f}".replace(".", ",") if x == x else "—")

    def yazi(fig, y, baslik, satirlar, boy=9.5, gen=92):
        if baslik:
            fig.text(0.07, y, baslik, fontsize=14, weight="bold", va="top", color="#1f2a44"); y -= 0.040
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= boy * 0.0022
            y -= 0.004
        return y

    def vaka_ciz(ax, axh, r):
        d = V[r.sembol]; tar = d.index
        i0 = int(tar.searchsorted(pd.Timestamp(r.bas))); i1 = int(tar.searchsorted(pd.Timestamp(r.son), side="right")) - 1
        ka = int(tar.searchsorted(pd.Timestamp(r.atilim))) if r.atilim == r.atilim else i1
        w = d.iloc[max(0, i0 - 60):min(len(d), ka + 121)]
        ax.axvspan(tar[i0], tar[i1], color="#fff4d6", zorder=0)
        ax.vlines(w.index, w.Low, w.High, color="#95a5a6", lw=0.6); ax.plot(w.index, w.Close, color="#1f2a44", lw=0.8)
        if r.tavan == r.tavan:
            ax.hlines([r.tavan, r.taban], tar[i0], tar[i1], colors=["#27ae60", "#c0392b"], lw=1.1, ls="--")
        if ka + 1 < len(d) and r.atilim == r.atilim:
            ax.axvline(tar[ka], color="#2c3e50", ls=":", lw=1)
            ax.scatter([tar[ka + 1]], [d.Open.iloc[ka + 1]], marker="^", color="#2980b9", s=45, zorder=5)
        if isinstance(r.d13_ilk, str) and r.d13_ilk:
            j = int(tar.searchsorted(pd.Timestamp(r.d13_ilk)))
            ax.scatter([tar[j]], [d.Low.iloc[j] * 0.97], marker="s", color="#e67e22", s=22, zorder=5)
        if isinstance(r.c1_gun, str) and r.c1_gun:
            j = int(tar.searchsorted(pd.Timestamp(r.c1_gun)))
            ax.scatter([tar[j]], [d.High.iloc[j] * 1.04], marker="*", color="#8e44ad", s=70, zorder=6)
        ax.set_yscale("log"); ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); ax.tick_params(labelsize=6.5); ax.set_xticks([])
        son = (f"koştu: 2 kat (en yüksek {vg(1 + r.max_yuk, 1)} x)" if r.kat2 == 1 else
               (f"önce +%20 geldi, 2 kat olmadı (en yüksek {vg(1 + r.max_yuk, 1)} x)" if r.k20 == 1 else "koşmadı"))
        ax.set_title(f"{r.ad} — sen: {r.cemal} · ölçü: {son}", fontsize=8.5, loc="left")
        axh.bar(w.index, w.Volume * w.Close, color="#7f8c8d", width=1.0); axh.set_yticks([]); axh.tick_params(labelsize=6)
        axh.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%y-%m"))

    def vaka_metin(r) -> str:
        d13 = f"D13 (üretim) {int(r.d13_gun)} gün 'çöl' dedi ({tr(r.d13_ilk)}'den)" if r.d13_gun == r.d13_gun and r.d13_gun > 0 else \
            "D13 (üretim) GÖRMEDİ"
        k18 = f"K18 sinyali {tr(r.c1_gun)}" if isinstance(r.c1_gun, str) and r.c1_gun else "K18 profil sinyali yok"
        return (f"kutu {tr(r.bas)} – {tr(r.son)} ({int(r.bar)} bar) · önce düşüş {yz(r.dusus)} · bant {yz(r.bant)} · mum düşüşün "
                f"{vg(r.mum_kat)}'i · hacim düşüşün {vg(r.hacim_kat)}'i · kutudaki en büyük hacim {vg(r.dev_hacim, 1)} x · atılım "
                f"{tr(r.atilim)} ({yz(r.atilim_getiri)}, hacim {vg(r.atilim_hacim, 1)} x) · fon payı {vg(100 * r.fon_pay_atilim, 1)}% · "
                f"{d13} · {k18}. Kaynak: {r.kaynak}.")

    kos = vaka[vaka.cemal == "koştu"]; kosm = vaka[vaka.cemal == "koşmadı"]
    prof = (vaka.dusus <= FI_K18_ESIK["dusus"]) & (vaka.mum_kat <= FI_K18_ESIK["mum"]) & (vaka.hacim_kat <= FI_K18_ESIK["hacim"])
    p_kos, p_kosm = int(prof[kos.index].sum()), int(prof[kosm.index].sum())
    gordu = (vaka.d13_gun.fillna(0) > 0) | vaka.c1_gun.fillna("").astype(str).str.len().gt(0)
    d13 = vaka[vaka.d13_gun.fillna(0) > 0]
    HK = KH[KH.kod.isin(["Ç85", "Ç86", "Ç87", "Ç88", "Ç89", "Ç90"]) & KH.donem.isin(["2023", "2024-26"])]
    H85 = HK[HK.kod == "Ç85"]
    ara = lambda x: f"{vg(np.nanmin(x))}-{vg(np.nanmax(x))}"
    sayfa = 0
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        y = yazi(fig, 0.96, "DERS 7: SENİN VAKALARIN — ORTAK İZ VAR MI?", [
            "Sen: 'TEHOL Ekim çölü koştu; BINBN'i gördüm, sabırsız sattım; KTLEV dev U tabanı; ESCAR'ı silkelemede zararına sattım; "
            "Vişne maden koşmadı; Euro'da 24 Aralık 2024 dev hacim barı; BORLS; VERUS'u kod o zaman bulmuştu; MANAS 21 Temmuz 2025 "
            "atılım barı, 29 Ekim'de yeniden, silkeleme, Kasım'da koştu; PAPIL zarar. Ortak iz var mı? Bölgeleri kendin bul, test et.'",
            "Ne yaptım: 12 bölgeyi veride buldum (senin eski etiketin varsa o: TEHOL, BINBN, ESCAR, PAPIL; yoksa grafikten). 'Euro' = "
            "EUHOL: 24.12.2024 hacmi önceki 60 günün 13,6 katı. 'Hakiş'i veride eşleyemedim. Her bölgede aynı ölçüleri aldım, sonra koşan "
            "vakaların ortak profilini sabit eşikle 2.000 hissede (BIST + ABD, 2016-26) aradım ve sonrasına baktım.",
            "",
            "KISA CEVAP",
            f"- ORTAK İZ VAR: koşan {len(kos)} vakanın hepsinde önce sert düşüş (−%32 … −%92), ardından mumları düşüş mumlarından küçük "
            f"(düşüşün {ara(kos.mum_kat)}'i) dar bir kutu ve kapanışla kutu tavanının kırıldığı bir atılım günü var; {int((kos.hacim_kat <= 1).sum())}/"
            f"{len(kos)} vakada kutu hacmi de düşüştekinden düşük.",
            "- AMA bu iz koşmayanlarda da var: " + ", ".join(f"{r.ad} (mum {vg(r.mum_kat)}, hacim {vg(r.hacim_kat)})" for r in kosm.itertuples())
            + f". Tam profil (düşüş + küçük mum + düşük hacim): koşanların {p_kos}/{len(kos)}'unda, koşmayanların {p_kosm}/{len(kosm)}'ünde.",
            f"- Evrende bu profil (C1) önce +%20'yi sıradan hisseden daha sık getirmiyor (eşli taban katı {ara(H85.ana_kat)}); önce "
            f"−%20'yi {ara(H85.ters_kat)} kat daha sık getiriyor. Altı denemenin (aylarca kutu, sert çöküş, dar kutu, kutuda dev hacim "
            f"barı, sektör rüzgârı) hiçbiri dört karar hücresinde 1,3'e çıkmadı (en yüksek {vg(np.nanmax(HK.ana_kat))}) → İZ DEĞİL.",
            f"- Kodun bulduğu: 2024-26'da BIST'te bu profille {len(liste)} atılım. Sonucu belli olanların %{100 * (liste.kat2 == 1).sum() / max(1, liste.kat2.notna().sum()):.0f}'i "
            f"koştu (2 kat), %{100 * ((liste.k20 == 1) & (liste.kat2 != 1)).sum() / max(1, liste.k20.notna().sum()):.0f}'i +%20 gördü ama "
            f"2 kat olmadı, %{100 * (liste.k20 == 0).sum() / max(1, liste.k20.notna().sum()):.0f}'i koşmadı. Profili tutmayan aynı "
            f"bağlamdaki atılımlarda koşan oranı %{100 * (esli.kat2 == 1).sum() / max(1, esli.kat2.notna().sum()):.0f} (aynı).",
            f"- Üretimdeki D13 senin {len(vaka)} bölgenden yalnız {len(d13)}'ini 'çöl' dedi: "
            + ", ".join(f"{r.ad} ({int(r.d13_gun)} gün)" for r in d13.itertuples())
            + ". Görmedikleri: " + ", ".join(vaka[vaka.d13_gun.fillna(0) == 0].ad) + ".",
        ], boy=9.3)
        yazi(fig, y - 0.01, "Grafiklerde", [
            "Sarı alan = kutu (çöl), yeşil/kırmızı kesikli = kutu tavanı/dibi, noktalı dikey = atılım günü, ▲ = ertesi açılış giriş, "
            "turuncu kare = üretim D13'ün ilk 'çöl' dediği gün, mor yıldız = K18 profil sinyali (bu ölçünün tarayıcısı). Alt şerit TL hacim."],
             boy=9)
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        V_ = vaka[vaka.atilim.notna()].reset_index(drop=True)
        for p in range(0, len(V_), 3):
            fig = plt.figure(figsize=A4)
            for k, r in enumerate(V_.iloc[p:p + 3].itertuples()):
                y0 = 0.68 - k * 0.32
                vaka_ciz(fig.add_axes([0.08, y0 + 0.085, 0.88, 0.19]), fig.add_axes([0.08, y0 + 0.045, 0.88, 0.04]), r)
                for j, parca in enumerate(textwrap.wrap(vaka_metin(r), 125)[:4]):
                    fig.text(0.08, y0 + 0.030 - j * 0.0125, parca, fontsize=6.6, va="top")
            pdf.savefig(fig); plt.close(fig); sayfa += 1
        fig = plt.figure(figsize=A4)
        y = yazi(fig, 0.96, "ORTAK İZ TABLOSU", [
            "Her satır bir bölge. Profil = önce düşüş ≤ −%30, mum ve hacim düşüştekinden küçük (≤ 1,0). Koşan vakalarla koşmayanlar "
            "arasında hiçbir sütun temiz ayrılmıyor: aynı şekil iki tarafta da var."], boy=9.3)
        sut = ["vaka", "sen", "düşüş", "bar", "bant", "mum", "hacim", "dev bar", "atılım", "fon %", "D13", "K18", "sonuç"]
        hucre = []
        for r in vaka.itertuples():
            hucre.append([r.ad, r.cemal, yz(r.dusus), f"{int(r.bar)}", yz(r.bant), vg(r.mum_kat), vg(r.hacim_kat), vg(r.dev_hacim, 1),
                          yz(r.atilim_getiri), vg(100 * r.fon_pay_atilim, 1),
                          f"{int(r.d13_gun)}" if r.d13_gun == r.d13_gun else "—", "var" if isinstance(r.c1_gun, str) and r.c1_gun else "yok",
                          ("2 kat" if r.kat2 == 1 else ("+%20" if r.k20 == 1 else "yok")) + (" ✓" if prof[r.Index] else "")])
        ax = fig.add_axes([0.03, y - 0.40, 0.94, 0.38]); ax.axis("off")
        T = ax.table(cellText=hucre, colLabels=sut, loc="upper center", cellLoc="center")
        T.auto_set_font_size(False); T.set_fontsize(6.6); T.scale(1, 1.45)
        for (i, j), c in T.get_celld().items():
            if i > 0 and hucre[i - 1][1] == "koşmadı":
                c.set_facecolor("#fdecea")
        yazi(fig, y - 0.44, "Okuma", [
            f"- ✓ = profil tutuyor. Koşan {len(kos)} vakanın {p_kos}'sinde, koşmayan {len(kosm)} vakanın {p_kosm}'sinde ✓ var: iz koşanı "
            "koşmayandan ayırmıyor.",
            "- Fon payı (KAP portföy raporlarındaki fonların sermayedeki payı) çöl sırasında hepsinde ~%0-2: 'fonlar alırken çöl oluştu' "
            "raporlu fonlarda görünmüyor. Dipteki toplama (varsa) bireysel hesaplar ve rapor vermeyen fonlardaydı; elimizde yok.",
            f"- Atılım günü hacmi ayırmıyor, tersine: koşmayanlarda kutu medyanının {ara(kosm.atilim_hacim)} katı, koşanlarda medyan "
            f"{vg(kos.atilim_hacim.median(), 1)} katı (en büyüğü MANAS-a {vg(kos.atilim_hacim.max(), 1)}).",
            "- Profilin dışında kalan koşanlar: " + ", ".join(f"{r.ad} (mum {vg(r.mum_kat)}, hacim {vg(r.hacim_kat)})"
                                                             for r in kos[~prof[kos.index]].itertuples()) + "."],
             boy=9)
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "EVREN TESTİ: PROFİL FARK YARATIYOR MU?", [
            "Tek cetvel: sinyal günü (atılım), ertesi açılış giriş, 60 günde önce +%20 (önce −%10'dan); eşli taban = aynı ay × 60 gün "
            "momentum × likidite. Kırmızı çizgi 1,3: dört karar hücresinin (BIST/ABD 2023 ve 2024-26) hepsinde geçmeli. Ç85 profil · "
            "Ç86 kutu ≥ 40 bar · Ç87 düşüş ≤ −%50 · tur 2 (önceden yazıldı): Ç88 dar kutu (bant ≤ %20) · Ç89 kutuda dev hacim barı (≥ 10x) "
            "· Ç90 sektör rüzgârı."], boy=9.3)
        RENK = {"BIST": "#1f2a44", "ABD": "#7f8fa6"}
        for k_, (kol, et_y, y0) in enumerate((("ana_kat", "önce +%20, eşli kat", 0.50), ("ters_kat", "önce −%20, eşli kat", 0.15))):
            ax = fig.add_axes([0.10, y0, 0.85, 0.24]); et, deg, renk = [], [], []
            for kd in ("Ç85", "Ç86", "Ç87", "Ç88", "Ç89", "Ç90"):
                for r in KH[(KH.kod == kd) & (KH.donem.isin(["2023", "2024-26"]))].itertuples():
                    et.append(f"{kd}\n{r.pazar}\n{r.donem}\nn={int(r.n)}"); deg.append(getattr(r, kol)); renk.append(RENK.get(r.pazar, "#999"))
            ax.bar(range(len(deg)), np.nan_to_num(np.array(deg, float)), color=renk)
            if kol == "ana_kat":                                   # 1,3 geçme çizgisi yalnız yukarı ölçüde anlamlı
                ax.axhline(1.3, color="#c0392b", ls="--", lw=2)
            ax.axhline(1.0, color="#999")
            ax.set_xticks(range(len(deg))); ax.set_xticklabels(et, fontsize=4.3); ax.set_ylabel(et_y, fontsize=8)
        fig.text(0.10, 0.765, f"Üst: yukarı (önce +%20) — hiçbir hücre 1,3'e çıkmıyor ({ara(HK.ana_kat)}).", fontsize=8.5)
        fig.text(0.10, 0.415, f"Alt: aşağı (önce −%20) — hücreler {ara(HK.ters_kat)}: profil oynak hisseyi seçiyor.", fontsize=8.5)
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        fig = plt.figure(figsize=A4)
        L = liste.copy(); L["bilgi"] = pd.to_datetime(L.bilgi)
        say = L.sonuc.value_counts()
        y = yazi(fig, 0.96, "KODUN BULDUKLARI (BIST 2024-26, profil C1)", [
            f"Bu profili taşıyan {len(L)} atılım ({L.sembol.nunique()} hisse): KOŞTU (250 günde kutu dibi kırılmadan 2 kat) "
            f"{say.get('KOŞTU (2 kat)', 0)}, +%20 GÖRDÜ (2 kat değil) {say.get('+%20 GÖRDÜ', 0)}, KOŞMADI (60 günde önce +%20 "
            f"gelmedi) {say.get('KOŞMADI', 0)}, "
            f"BEKLİYOR (60 gün dolmadı) {say.get('BEKLİYOR', 0)}. Tam liste: arastirma_cikti/fon_izi/k18_liste_BIST.csv.",
            f"- Aynı bağlamda profili tutmayan atılımlar ({len(esli)}): koşan %{100 * (esli.kat2 == 1).sum() / max(1, esli.kat2.notna().sum()):.0f} "
            f"vs profil %{100 * (L.kat2 == 1).sum() / max(1, L.kat2.notna().sum()):.0f}; önce +%20 %{100 * esli.k20.mean():.0f} vs "
            f"%{100 * L.k20.mean():.0f}.",
            f"- Fon hisselerinde (sonradan seçilmiş 23 hisse) {int(L.fon_hissesi.sum())} sinyalin {int(((L.kat2 == 1) & L.fon_hissesi).sum())}'si "
            f"koştu; diğerlerinde {int((~L.fon_hissesi).sum())} sinyalin {int(((L.kat2 == 1) & ~L.fon_hissesi).sum())}'i. Bu fark ileriye "
            "dönük değil: o 23 hisse zaten 10-170 kat gittikten sonra listeye alındı.",
            "Sonucu belli son 40 sinyal (60 günü dolmuş; en yeni üstte; 'koştu' = 2 kat):"], boy=9.2)
        X = L[L.sonuc != "BEKLİYOR"].sort_values("bilgi", ascending=False).head(40)
        hucre = [[r.sembol, tr(r.bilgi), yz(r.dusus), f"{int(r.bar)}", vg(r.mum_kat), vg(r.hacim_kat), yz(r.trail), r.sonuc]
                 for r in X.itertuples()]
        ax = fig.add_axes([0.05, 0.04, 0.90, y - 0.06]); ax.axis("off")
        T = ax.table(cellText=hucre, colLabels=["hisse", "atılım", "düşüş", "bar", "mum", "hacim", "üretim çıkışı", "sonuç"],
                     loc="upper center", cellLoc="center")
        T.auto_set_font_size(False); T.set_fontsize(6.6); T.scale(1, 1.18)
        for (i, j), c in T.get_celld().items():
            if i > 0:
                s_ = hucre[i - 1][-1]
                c.set_facecolor("#e8f6ec" if s_.startswith("KOŞTU") else ("#fdecea" if s_ == "KOŞMADI" else "#ffffff"))
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "DERS: NEDEN İZ DEĞİL, SEN NASIL BAKARSIN", [
            "- Senin gözün doğru şekli görüyor: koşan hisselerinin hepsinde düşüşten sonra sakinleşen, küçük mumlu bir kutu ve kutu "
            f"tavanını kapanışla geçen bir gün var. Kod da bu şekli buluyor ({len(vaka)} bölgenin {int(gordu.sum())}'unda K18 sinyali ya da "
            "üretim D13).",
            "- Ama aynı şekil koşmayanlarda da var (VSNMD, PAPIL) ve evrende binlerce kez çıkıyor; sonrası sıradan hisseyle aynı, düşüş "
            "riski biraz daha fazla. Yani şekil 'bu hisse koşar' demiyor; 'bu hisse sakinleşti ve kutudan çıktı' diyor.",
            "- Koşanı koşmayandan ayıran şey kutunun içinde değil, kutudan SONRA: " + "; ".join(
                f"{r.ad} atılımdan önce kutu dibini kırdı (60 günde dibin {yz(r.sonra60_dip)} altı)" if r.kutu_alti else
                f"{r.ad} atılımdan sonra en çok {yz(r.max_yuk)} yükselip geri döndü" for r in kosm.itertuples())
            + ". Bunu atılım günü bilmek mümkün değil; sistemin yaptığı da bu: kırılımda gir, trail ile tut, bozulunca çık (bölüm 8 dersi).",
            "- Fonların payı çöl sırasında raporlarda ~0. 'Fon aldığı için koştu' doğru olabilir ama iz fiyat grafiğinde değil, "
            "sahiplik kaydında ve sonradan geliyor (K10 fon defteri: fonlar koşu fazında giriyor).",
            "- Silkeleme: " + "; ".join(
                f"{r.ad} kutusu {tr(r.bas)} – {tr(r.son)}, dip {vg(r.taban)}, atılım {tr(r.atilim)} "
                + ("(arada kutu dibi kırıldı)" if r.kutu_alti else "(arada kutu dibi kırılmadı)")
                for r in vaka[vaka.ad.isin(["ESCAR-25", "MANAS-25b", "KTLEV-24"])].itertuples())
            + ". Bu vakalarda sabır ve zarar sınırını kutu dibinde tutmak kazandırdı; ama evrende aynı profil önce −%20'yi "
            f"{ara(HK.ters_kat)} kat daha sık getiriyor, yani aynı sabır koşmayanlarda kutu dibine kadar zarar yazdırıyor.",
            "",
            "Sen nasıl bakarsın: 1) düşüş sonrası küçük mumlu kutu → aday (kod bunu buluyor); 2) kutu tavanını kapanışla geçen gün → giriş; "
            "3) kutu dibi → zarar sınırı; 4) +%20'den sonra SMA20 trail. Hangisinin 40 kat gideceğini şekil söylemiyor; boyut ve "
            "sabır söylüyor.",
            "",
            "Sıradaki (kararın): bu profili üretime 'yaz' gerekmiyor, D13 zaten benzer; ama D13 senin bölgelerinden BINBN, KTLEV, "
            "MANAS'ı göremiyor (dip yeni / parabol yok). Kutuyu 'dibe ilk değdiği gün'den başlatan K18 kutusu bunları gördü. D13'ün "
            "yakalama oranını artırmak istersen bu bir üretim kararı ('yaz')."], boy=9.3)
        pdf.savefig(fig); plt.close(fig); sayfa += 1
    return sayfa


# ---------------------------------------------------------------- K19 SİSTEM rastgeleden iyi mi? (Cemal 25 Eki)
# CEMAL (25 Eki): "'Kazandıran şey sistemin zaten yaptığı: kırılımda gir, zarar sınırı kutu dibinde, sonra trail' diyorsun; ama bunun
# rastgele bir hissede ya da rastgele bir noktadan çok daha fazla kazandırması lazım; bu test yok, burada bir aptallık var." Haklı: o
# cümle ölçülmeden yazıldı; tek cetvel de 'önce +%20'yi ölçüyordu, sistemin kâr/zararını değil (CLAUDE.md standardı trail + slot).
# KURAL (sonuç görülmeden yazıldı, 25 Eki): sinyal günü t, giriş t+1 açılışı g; stop = kutu dibi x 0,98 (takip T6 TABAN_TOL); kapanış
# stopun altındaysa o kapanıştan çık; High >= g x 1,20 görülünce ertesi bardan itibaren kapanış < SMA20 -> çık (trail, ufuk yok);
# hedef de stop da yoksa 120. bar kapanışı. Maliyet %0,4. Trail'deyken veri biterse son kapanış (açık işlem işaretli); trail'siz ve
# 120 bar dolmamışsa işlem sayılmaz (sistemde de rastgelede de aynı).
# SİNYALLER: S1 cemal = K18 C1 (Cemal'in vaka profili); S2 kutu = K18 C1 + eşli (düşüş sonrası bütün kutu kırılımları, profil şartı yok);
# S3 donchian = kapanış önceki 20 barın en yüksek gövde üstünü x1,002 geçer (çöl/düşüş şartı yok), stop = önceki 20 barın dibi x 0,98;
# hissede 60 barda tek.
# RASTGELE (her sinyal için 3 çekiliş, AYNI çıkış kuralı ve AYNI stop mesafesi d = 1 - stop/g): R_hisse = aynı gün rastgele başka hisse;
# R_esli = aynı gün, aynı 60 gün momentum beşliği x 60 gün likidite üçlüsü; R_nokta = aynı hisse, aynı dönemde rastgele gün.
# EK (aynı gün, sonuç görülmeden): her işlemde 'tut120' = stopsuz, trailsiz 120 bar tut (çıkış kuralının kendi katkısı, betimsel).
# K20 (Cemal 25 Eki: 'çöl bitişi, sağ ayak rastgele hisseden iyi değilse her şey hikâye; çöl nadir'; önceden yazıldı): ek sinyaller dar
# (K18 C4, bant <= %20) ve nadir (C4 + düşüş <= -%50); ek ölçüler max120 (120 barda en yüksek / giriş), x2_250 (250 barda stop kırılmadan
# 2 kat). Sağ ayak kararı: max120'nin R_esli'ye eşli farkı ay kümeli %90 alt sınırı > 0, dört karar hücresinde.
# KARAR (önceden): hücre (pazar x 2023 / 2024-26) 'sistem üstün' = R_esli'ye göre işlem başı fark ay kümeli bootstrap %90 alt sınırı > 0
# VE 30 slot portföy toplamı R_esli'nin >= 1,3 katı (R_esli <= 0 ise sistem > 0). Dört karar hücresinin hepsi -> sistem rastgeleden üstün.
FI_K19 = {"stop_tol": 0.02, "hedef": 0.20, "ufuk": 120, "maliyet": 0.004, "cekilis": 3, "slot": 30, "bas": "2023-01-01",
          "donchian": 20, "tekrar": 60, "d_ust": 0.60, "boot": 1000, "kat_esik": 1.3}
K19_DONEM = [("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31")]


def fi_k19_cikis(c: np.ndarray, h: np.ndarray, sma: np.ndarray, e: int, g: float, stop: float, E: Dict[str, Any] = FI_K19
                 ) -> Tuple[float, int, bool]:
    """Sistem çıkışı (K19 KURAL). Dönüş (getiri - maliyet, tutulan bar, açık mı); sayılmayan işlemde getiri NaN."""
    n = len(c)
    if not (g > 0) or e >= n:
        return np.nan, 0, False
    w = c[e:e + E["ufuk"]]; hw = h[e:e + E["ufuk"]]
    ih = np.flatnonzero(hw >= g * (1 + E["hedef"])); ih = int(ih[0]) if len(ih) else None
    ist = np.flatnonzero(w < stop); ist = int(ist[0]) if len(ist) else None
    if ist is not None and (ih is None or ist <= ih):                      # aynı bar: kapanış stopun altındaysa stop önce
        return w[ist] / g - 1 - E["maliyet"], ist + 1, False
    if ih is not None:
        j0 = e + ih + 1
        tj = np.flatnonzero(c[j0:] < sma[j0:])
        if len(tj):
            j = j0 + int(tj[0]); return c[j] / g - 1 - E["maliyet"], j - e + 1, False
        return c[-1] / g - 1 - E["maliyet"], n - e, True
    if len(w) < E["ufuk"]:
        return np.nan, len(w), False
    return w[-1] / g - 1 - E["maliyet"], E["ufuk"], False


def fi_k19_dizi(V: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Hisse dizileri (o, h, c, sma20) ve günlük kesit: 60 gün momentum beşliği, 60 gün medyan TL hacim üçlüsü (o gün bilinen)."""
    A = {s: (d.index, d.Open.to_numpy(float), d.High.to_numpy(float), d.Close.to_numpy(float),
             d.Close.rolling(20).mean().to_numpy()) for s, d in V.items()}
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index()
    TL = pd.DataFrame({s: d.Close * d.Volume for s, d in V.items()}).reindex(C.index)
    mom = (C / C.shift(60) - 1).rank(axis=1, pct=True)
    lik = TL.rolling(60, min_periods=40).median().rank(axis=1, pct=True)
    grp = (np.ceil(mom * 5).clip(1, 5) * 10 + np.ceil(lik * 3).clip(1, 3))
    return {"A": A, "grp": grp, "var": C.notna()}


def fi_k19_islem(D: Dict[str, Any], s: str, t: pd.Timestamp, d: Optional[float] = None, stop: Optional[float] = None,
                 E: Dict[str, Any] = FI_K19) -> Optional[Dict[str, Any]]:
    """(hisse, sinyal günü t) için giriş t+1 açılışı ve çıkış. stop verilirse sinyal, d verilirse rastgele (stop = g x (1 - d))."""
    a = D["A"].get(s)
    if a is None:
        return None
    idx, o, h, c, sma = a
    i = int(idx.searchsorted(t, side="right"))                              # t'den sonraki ilk işlem günü = giriş
    if i >= len(c) or i < 61:
        return None
    g = o[i]
    if stop is None:
        stop = g * (1 - d)
    r, b, acik = fi_k19_cikis(c, h, sma, i, g, stop, E)
    if r != r:
        return None
    tut = c[i + E["ufuk"] - 1] / g - 1 - E["maliyet"] if i + E["ufuk"] <= len(c) else np.nan   # kıyas: stopsuz, trailsiz 120 bar tut
    # K20 'sağ ayak' (atılımdan SONRAKİ yükseliş, çıkış kuralından bağımsız): 120 barda en yüksek High / giriş; 250 barda stop
    # (kapanış) kırılmadan 2 kat. Pencere dolmamışsa NaN.
    mx = h[i:i + E["ufuk"]].max() / g - 1 if i + E["ufuk"] <= len(c) else np.nan
    x2 = np.nan
    if i + 250 <= len(c):
        hi = np.flatnonzero(h[i:i + 250] >= 2 * g); ki = np.flatnonzero(c[i:i + 250] < stop)
        x2 = float(len(hi) > 0 and (len(ki) == 0 or hi[0] < ki[0]))
    return {"sembol": s, "bilgi": t, "giris": idx[i], "cikis": idx[min(len(idx) - 1, i + b - 1)], "r": r, "bar": b, "acik": acik,
            "d": 1 - stop / g if g > 0 else np.nan, "tut120": tut, "max120": mx, "x2_250": x2}


def fi_k19_donchian(V: Dict[str, pd.DataFrame], E: Dict[str, Any] = FI_K19) -> pd.DataFrame:
    """S3: kapanış önceki 20 barın en yüksek gövde üstünü x1,002 geçer; stop = önceki 20 barın dibi x (1 - stop_tol); 60 barda tek."""
    sat = []
    for s, d in V.items():
        o = d.Open.to_numpy(float); c = d.Close.to_numpy(float); l = d.Low.to_numpy(float)
        top = pd.Series(np.maximum(o, c)).rolling(E["donchian"]).max().shift(1).to_numpy()
        dip = pd.Series(l).rolling(E["donchian"]).min().shift(1).to_numpy()
        son = -10 ** 9
        for t in np.flatnonzero(c > top * 1.002):
            if t < 61 or t - son < E["tekrar"] or d.index[t] < pd.Timestamp(E["bas"]):
                continue
            son = int(t); sat.append({"sembol": s, "bilgi": d.index[t], "stop": dip[t] * (1 - E["stop_tol"])})
    return pd.DataFrame(sat)


def fi_k19_rastgele(D: Dict[str, Any], X: pd.DataFrame, tur: str, cek: int, E: Dict[str, Any] = FI_K19,
                    tohum: int = 19) -> pd.DataFrame:
    """Her sistem işlemi (X: sembol, bilgi, d, donem) için `cek` rastgele işlem, aynı çıkış ve aynı stop mesafesi.
    tur: 'hisse' aynı gün rastgele hisse; 'esli' aynı gün aynı momentum x likidite grubu; 'nokta' aynı hisse, aynı dönemde rastgele gün."""
    rng = np.random.default_rng(tohum); sat = []
    grp, var = D["grp"], D["var"]; kolon = np.array(var.columns)
    for k, r in enumerate(X.itertuples()):
        t = pd.Timestamp(r.bilgi); dd = min(r.d, E["d_ust"])
        if tur in ("hisse", "esli"):
            if t not in var.index:
                continue
            aday = kolon[var.loc[t].to_numpy() & (kolon != r.sembol)]
            if tur == "esli":
                gs = grp.loc[t]; g0 = gs.get(r.sembol, np.nan)
                es = aday[(gs.reindex(aday).to_numpy() == g0)] if g0 == g0 else np.array([])
                aday = es if len(es) >= 3 else aday
            for j in range(cek):
                if not len(aday):
                    break
                y = fi_k19_islem(D, str(rng.choice(aday)), t, d=dd, E=E)
                if y:
                    sat.append({**y, "i": k, "cek": j})
        else:
            idx = D["A"][r.sembol][0]
            b, e_ = pd.Timestamp(r.don_bas), pd.Timestamp(r.don_bit)
            gun = idx[(idx >= b) & (idx <= e_)]
            for j in range(cek):
                if not len(gun):
                    break
                y = fi_k19_islem(D, r.sembol, pd.Timestamp(rng.choice(gun)), d=dd, E=E)
                if y:
                    sat.append({**y, "i": k, "cek": j})
    return pd.DataFrame(sat)


def fi_k19_slot(X: pd.DataFrame, slot: int = 30) -> float:
    """30 slot: işlemler giriş sırasıyla; boş slot yoksa ya da hisse elde ise atlanır; her işlem sermayenin 1/slot'u (toplam getiri)."""
    if not len(X):
        return np.nan
    acik: List[Tuple[pd.Timestamp, str]] = []; top = 0.0
    for r in X.sort_values("giris").itertuples():
        g = pd.Timestamp(r.giris)
        acik = [(c_, s_) for c_, s_ in acik if c_ >= g]                # çıkış günü >= bugün olan slot dolu
        if len(acik) >= slot or any(s_ == r.sembol for _, s_ in acik):
            continue
        acik.append((pd.Timestamp(r.cikis), r.sembol)); top += r.r / slot
    return top


def fi_k19_kiyas(S: pd.DataFrame, R: Dict[str, pd.DataFrame], E: Dict[str, Any] = FI_K19, tohum: int = 19) -> Dict[str, Any]:
    """Bir hücrede sistem (S) ve rastgele gruplar: işlem başı ort/medyan/kazanan/ağır kayıp/bar, 30 slot (rastgelede çekiliş ortalaması),
    R_esli ve R_hisse'ye göre eşli fark (sinyal başına rastgele ortalaması) ve ay kümeli bootstrap %90 aralığı."""
    rng = np.random.default_rng(tohum)
    out: Dict[str, Any] = {"n": len(S)}
    def ozet(X, on):
        out[on + "ort"] = X.r.mean(); out[on + "med"] = X.r.median(); out[on + "kaz"] = (X.r > 0).mean()
        out[on + "agir"] = (X.r <= -0.15).mean(); out[on + "bar"] = X.bar.mean()
        k = X.tut120.notna()                                               # aynı işlemlerde çıkış kuralı mı, 120 bar tutmak mı
        out[on + "kural_tut"] = X.r[k].mean(); out[on + "tut120"] = X.tut120[k].mean(); out[on + "tut_agir"] = (X.tut120[k] <= -0.15).mean()
        out[on + "max120"] = X.max120.mean(); out[on + "max120_med"] = X.max120.median(); out[on + "x2"] = X.x2_250.mean()
    ozet(S, "s_"); out["s_slot"] = fi_k19_slot(S, E["slot"]); out["s_acik"] = S.acik.mean()
    for ad, Rx in R.items():
        if not len(Rx):
            continue
        ozet(Rx, ad + "_")
        out[ad + "_slot"] = float(np.nanmean([fi_k19_slot(Rx[Rx.cek == j], E["slot"]) for j in sorted(Rx.cek.unique())]))
        m = Rx.groupby("i").r.mean()
        P = pd.DataFrame({"s": S.r.to_numpy()}, index=S.index).join(m.rename("r"), how="inner")
        P["fark"] = P.s - P.r; P["ay"] = pd.to_datetime(S.loc[P.index, "bilgi"]).dt.to_period("M").astype(str)
        aylar = P.ay.unique(); G = {a: P.fark[P.ay == a].to_numpy() for a in aylar}
        bs = [np.concatenate([G[a] for a in rng.choice(aylar, len(aylar))]).mean() for _ in range(E["boot"])]
        out[ad + "_fark"] = P.fark.mean(); out[ad + "_alt"], out[ad + "_ust"] = np.percentile(bs, [5, 95])
        # K20 sağ ayak: 120 barda en yüksek yükselişin eşli farkı (aynı ay kümeli bootstrap)
        m2 = Rx.groupby("i").max120.mean()
        Q = pd.DataFrame({"s": S.max120.to_numpy()}, index=S.index).join(m2.rename("r"), how="inner").dropna()
        if len(Q):
            Q["fark"] = Q.s - Q.r; Q["ay"] = pd.to_datetime(S.loc[Q.index, "bilgi"]).dt.to_period("M").astype(str)
            ay2 = Q.ay.unique(); G2 = {a: Q.fark[Q.ay == a].to_numpy() for a in ay2}
            b2 = [np.concatenate([G2[a] for a in rng.choice(ay2, len(ay2))]).mean() for _ in range(E["boot"])]
            out[ad + "_maxfark"] = Q.fark.mean(); out[ad + "_maxalt"], out[ad + "_maxust"] = np.percentile(b2, [5, 95])
    se, rs = out.get("s_slot", np.nan), out.get("esli_slot", np.nan)
    slot_ok = (se >= E["kat_esik"] * rs) if rs > 0 else (se > 0)
    out["ustun"] = bool(out.get("esli_alt", -1) > 0 and slot_ok)
    out["sag_ayak_ustun"] = bool(out.get("esli_maxalt", -1) > 0)      # K20: atılım sonrası yükseliş eşli hisseden büyük mü
    return out


def fon_izi_k19(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    """K19 sürücü: S1 cemal / S2 kutu (k18_olaylar.csv.gz) ve S3 donchian; BIST + ABD, 2023 ve 2024-26; R_hisse, R_esli, R_nokta;
    karar fi_k19_kiyas 'ustun'. Çıktı k19_islem.csv.gz (sistem + rastgele işlemler), k19_ozet.csv."""
    A = A or FIAyar(); E = FI_K19
    K18 = pd.read_csv(os.path.join(A.cikti, "k18_olaylar.csv.gz"), parse_dates=["bilgi"], low_memory=False)
    Z: List[Dict[str, Any]] = []; T: List[pd.DataFrame] = []
    for pazar in ("BIST", "ABD"):
        try:
            V = fi_k1_veri(A.veri[pazar], pazar, A)
        except Exception as ex:
            filog.warning("K19 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        D = fi_k19_dizi(V)
        K = K18[(K18.pazar == pazar) & (K18.bilgi >= E["bas"])]
        st = lambda x: x.assign(stop=x.taban * (1 - E["stop_tol"]))
        sinyal = {"cemal": st(K[K.varyant == "C1"]), "kutu": st(K[K.varyant.isin(["C1", "esli"])]), "donchian": fi_k19_donchian(V, E),
                  # K20 (Cemal 25 Eki: 'çöl nadir'): sıkı çöl = dar kutu (C4, bant <= %20) ve sert çöküş (düşüş <= -%50) birlikte
                  "dar": st(K[K.varyant == "C4"]), "nadir": st(K[(K.varyant == "C4") & (K.dusus <= -0.50)])}
        for sad, X0 in sinyal.items():
            S = pd.DataFrame([y for y in (fi_k19_islem(D, r.sembol, pd.Timestamp(r.bilgi), stop=r.stop, E=E)
                                          for r in X0.itertuples()) if y]) if len(X0) else pd.DataFrame()
            if not len(S):
                continue
            for dad, b, e_ in K19_DONEM:
                Sx = S[(S.bilgi >= b) & (S.bilgi <= e_)].reset_index(drop=True).assign(don_bas=b, don_bit=e_)
                if not len(Sx):
                    continue
                R = {tur: fi_k19_rastgele(D, Sx, tur, E["cekilis"], E) for tur in ("hisse", "esli", "nokta")}
                z = fi_k19_kiyas(Sx, R, E); z.update({"pazar": pazar, "donem": dad, "sinyal": sad}); Z.append(z)
                filog.info("K19 %s %s %s: n %d sistem %.3f esli %.3f slot %.2f / %.2f ustun %s", pazar, dad, sad, z["n"],
                           z["s_ort"], z.get("esli_ort", np.nan), z["s_slot"], z.get("esli_slot", np.nan), z["ustun"])
                T.append(Sx.assign(pazar=pazar, donem=dad, sinyal=sad, grup="sistem"))
                for tur, Rx in R.items():
                    T.append(Rx.assign(pazar=pazar, donem=dad, sinyal=sad, grup=tur))
    if not Z:
        raise RuntimeError("K19: sonuç yok")
    Zk = pd.DataFrame(Z); Zk.to_csv(os.path.join(A.cikti, "k19_ozet.csv"), index=False)
    pd.concat(T, ignore_index=True).to_csv(os.path.join(A.cikti, "k19_islem.csv.gz"), index=False)
    karar = {s: bool(Zk[Zk.sinyal == s].ustun.all() and len(Zk[Zk.sinyal == s]) == 4) for s in Zk.sinyal.unique()}
    return {"ozet": Zk, "karar": karar}


def fi_k12_ders8(Zk: pd.DataFrame, T: pd.DataFrame, yol: str) -> int:
    """Ders 8 (Cemal 25 Eki: 'sistem rastgele hisseden / rastgele noktadan çok daha fazla kazandırmalı; bu test yok'): (1) soru, kural,
    kısa cevap; (2) işlem başı ortalama getiri: sistem vs aynı gün eşli hisse / rastgele hisse / aynı hisse rastgele gün, farkın %90 aralığı;
    (3) çıkış kuralı (kutu dibi stop + trail) vs 120 gün tut: ortalama, medyan, −%30 altı kayıp. Zk = k19_ozet.csv, T = k19_islem.csv.gz."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    A4 = (8.27, 11.69)
    yz = lambda x: (("−" if x < 0 else "+") + f"%{abs(100 * x):.1f}").replace(".", ",") if x == x else "—"

    def yazi(fig, y, baslik, satirlar, boy=9.4, gen=92):
        if baslik:
            fig.text(0.07, y, baslik, fontsize=14, weight="bold", va="top", color="#1f2a44"); y -= 0.040
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= boy * 0.0022
            y -= 0.004
        return y

    HUC = [("BIST", "2023"), ("BIST", "2024-26"), ("ABD", "2023"), ("ABD", "2024-26")]
    C = Zk[Zk.sinyal == "cemal"].set_index(["pazar", "donem"])
    fark = Zk.esli_fark; T1 = T[T.tut120.notna() & (T.grup == "sistem")]
    G = T1.groupby(["pazar", "donem", "sinyal"])
    kural = G.r.agg(["mean", "median"]); tut = G.tut120.agg(["mean", "median"])
    k30 = G.r.apply(lambda x: (x <= -0.30).mean()); t30 = G.tut120.apply(lambda x: (x <= -0.30).mean())
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "DERS 8: SİSTEM RASTGELEDEN İYİ Mİ?", [
            "Sen: 'Kazandıran şey kırılımda gir, kutu dibinde zarar sınırı, sonra trail diyorsun; ama bu rastgele bir hisseden ya da "
            "rastgele bir noktadan çok daha fazla kazandırmalı. Bu test yok; burada bir aptallık var.' Haklıydın: o cümleyi ölçmeden "
            "yazmıştım ve tek cetvel sistemin kâr/zararını değil 'önce +%20'yi ölçüyordu.",
            "Kural (sonuç görülmeden): atılım günü sinyal, ertesi açılış giriş; kapanış kutu dibinin %2 altına inerse çık; +%20 görülünce "
            "SMA20 trail; ikisi de yoksa 120. gün; %0,4 maliyet. Üç sinyal: senin profilin (K18 C1), bütün düşüş sonrası kutu kırılımları, "
            "düz 20 gün kırılımı (çölsüz).",
            "Rastgele (her sinyale 3 çekiliş, AYNI çıkış, AYNI stop mesafesi): aynı gün eşli hisse (aynı momentum × likidite), aynı gün "
            "rastgele hisse, aynı hisse rastgele gün. Geçme şartı (önceden): eşli hisseye göre işlem başı fark %90 aralıkta sıfırın üstünde "
            "VE 30 slot portföy en az 1,3 kat; dört karar hücresinin hepsinde.",
            "",
            "KISA CEVAP",
            f"- GİRİŞ rastgeleden iyi değil: 12 hücrenin hiçbiri geçmedi. Sistem ile aynı gün eşli hisse arasındaki işlem başı fark "
            f"{yz(fark.min())} … {yz(fark.max())}; aralıklar sıfırı içeriyor. Senin profilin BIST 2023'te işlem başı "
            f"{yz(C.loc[('BIST', '2023'), 's_ort'])}, aynı gün eşli hisse {yz(C.loc[('BIST', '2023'), 'esli_ort'])}: kazancın tamamı "
            "piyasadan.",
            "- ÇIKIŞ kazancı artırmıyor, riskin şeklini değiştiriyor: aynı girişlerde stopsuz 120 gün tutmak ortalamada her hücrede daha "
            "çok getiriyor (trail büyük kazananı erken kesiyor). Yatay piyasada (BIST 2024-26, ABD) kural medyanı ve kazanan oranını "
            f"artırıyor; −%30 altı kayıp BIST 2024-26'da {yz(t30.get(('BIST', '2024-26', 'cemal')))} → {yz(k30.get(('BIST', '2024-26', 'cemal')))}, "
            f"ABD 2024-26'da {yz(t30.get(('ABD', '2024-26', 'cemal')))} → {yz(k30.get(('ABD', '2024-26', 'cemal')))}, ABD 2023'te aynı. "
            "Boğada (BIST 2023) tutmak her ölçüde iyi.",
            "- Yani para 'sistemden' değil 'piyasada olmaktan' geliyor. Çöl + atılım bir giriş üstünlüğü vermiyor; stop + trail bir "
            "risk ayarı, kazanç kaynağı değil.",
        ])
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "GİRİŞ: SİSTEM vs RASTGELE (işlem başı ortalama, aynı çıkış)", [
            "Koyu = sistem, diğerleri aynı çıkış ve aynı stop mesafesiyle rastgele girişler. Çubuklar neredeyse aynı boyda: girişin seçimi "
            "fark yaratmıyor."])
        for k, sad in enumerate(("cemal", "kutu", "donchian")):
            ax = fig.add_axes([0.10, 0.62 - k * 0.27, 0.85, 0.20]); X = Zk[Zk.sinyal == sad].set_index(["pazar", "donem"])
            for j, (kol, renk, et) in enumerate((("s_ort", "#1f2a44", "sistem"), ("esli_ort", "#7f8fa6", "eşli hisse aynı gün"),
                                                 ("hisse_ort", "#b8c4d6", "rastgele hisse aynı gün"), ("nokta_ort", "#e0c38c", "aynı hisse rastgele gün"))):
                ax.bar(np.arange(4) + j * 0.2 - 0.3, [100 * X.loc[h, kol] if h in X.index else 0 for h in HUC], 0.2, color=renk, label=et)
            ax.set_xticks(range(4)); ax.set_xticklabels([f"{p} {d}" for p, d in HUC], fontsize=8); ax.axhline(0, color="#999", lw=0.8)
            ax.set_ylabel("işlem başı %", fontsize=8); ax.set_title({"cemal": "senin profilin (K18 C1)", "kutu": "düşüş sonrası bütün kutu kırılımları",
                                                                     "donchian": "düz 20 gün kırılımı (çöl şartı yok)"}[sad], fontsize=9)
            if k == 0:
                ax.legend(fontsize=7, ncol=2)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "ÇIKIŞ: KUTU DİBİ STOP + TRAIL vs 120 GÜN TUT (aynı girişler, senin profilin)", [
            "Aynı işlemler, iki çıkış. Ortalama: tutmak hep önde (büyük kazananlar trail'de erken satılıyor). Medyan ve −%30 altı kayıp: "
            "yatay piyasada kural önde, boğada (BIST 2023) tutmak önde."])
        for k, (ad, f1, f2) in enumerate((("ortalama", kural["mean"], tut["mean"]), ("medyan", kural["median"], tut["median"]),
                                          ("−%30 altı kayıp oranı", k30, t30))):
            ax = fig.add_axes([0.10, 0.62 - k * 0.27, 0.85, 0.20])
            a_ = [100 * f1.get((p, d, "cemal"), np.nan) for p, d in HUC]; b_ = [100 * f2.get((p, d, "cemal"), np.nan) for p, d in HUC]
            ax.bar(np.arange(4) - 0.18, a_, 0.36, color="#1f2a44", label="kutu dibi stop + trail")
            ax.bar(np.arange(4) + 0.18, b_, 0.36, color="#e0a458", label="120 gün tut")
            ax.set_xticks(range(4)); ax.set_xticklabels([f"{p} {d}" for p, d in HUC], fontsize=8); ax.axhline(0, color="#999", lw=0.8)
            ax.set_ylabel("%", fontsize=8); ax.set_title(ad, fontsize=9)
            if k == 0:
                ax.legend(fontsize=7)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        N = Zk[Zk.sinyal == "nadir"].set_index(["pazar", "donem"])
        yazi(fig, 0.96, "SAĞ AYAK: ÇÖL BİTTİKTEN SONRAKİ YÜKSELİŞ (çıkış kuralı yok)", [
            "Sen: 'çöl oluşurken günlerdeki kazanç değil; çöl bitişi, sağ ayak rastgele hisseden iyi değilse her şey hikâye; çöl nadir.' "
            "Burada çıkış kuralı yok: atılımdan sonraki 120 günde ulaşılan en yüksek fiyat (giriş = ertesi açılış) ve 250 günde kutu dibi "
            "kırılmadan 2 kat. Aynı gün, aynı momentum × likiditede rastgele hisse ile kıyas. 'Nadir' = dar kutu (bant ≤ %20) + sert çöküş "
            "(≤ −%50): BIST 2024-26'da yılda ~120 sinyal.",
            f"- Senin profilin, BIST 2024-26: 120 günde en yüksek ort. {yz(Zk[(Zk.sinyal == 'cemal') & (Zk.pazar == 'BIST') & (Zk.donem == '2024-26')].s_max120.iloc[0])}, "
            f"aynı gün eşli hisse {yz(Zk[(Zk.sinyal == 'cemal') & (Zk.pazar == 'BIST') & (Zk.donem == '2024-26')].esli_max120.iloc[0])}.",
            f"- Nadir çöl, BIST 2024-26: 2 kat oranı {yz(N.loc[('BIST', '2024-26'), 's_x2'])}, aynı gün eşli hisse {yz(N.loc[('BIST', '2024-26'), 'esli_x2'])}. "
            "Kodun bulduğu her 5 nadir çölden 1'i 2 kat oldu; aynı gün rastgele seçilen hisseden de 5'te 1'i.",
            f"- Sağ ayak geçme şartı (önceden: eşli farkın %90 alt sınırı > 0, dört hücre): hiçbir sinyal geçmedi; geçen hücreler yalnız ABD "
            f"({int(Zk.sag_ayak_ustun.sum())} hücre), BIST'te hiçbiri."])
        ax = fig.add_axes([0.10, 0.36, 0.85, 0.30]); et = []; a_ = []; b_ = []
        for s_ in ("cemal", "dar", "nadir"):
            for p, d_ in HUC:
                r = Zk[(Zk.sinyal == s_) & (Zk.pazar == p) & (Zk.donem == d_)]
                if len(r):
                    et.append(f"{s_}\n{p} {d_}"); a_.append(100 * r.s_max120.iloc[0]); b_.append(100 * r.esli_max120.iloc[0])
        ax.bar(np.arange(len(a_)) - 0.18, a_, 0.36, color="#1f2a44", label="çöl atılımı")
        ax.bar(np.arange(len(b_)) + 0.18, b_, 0.36, color="#7f8fa6", label="aynı gün eşli rastgele hisse")
        ax.set_xticks(range(len(et))); ax.set_xticklabels(et, fontsize=5.5); ax.set_ylabel("120 günde en yüksek, ort. %", fontsize=8); ax.legend(fontsize=7)
        yazi(fig, 0.31, "", [
            "- MANAS 16 Haz – 28 Tem 2025: kod (K18) buldu, sinyal 22 Tem 2025; hisse sonra 9 kat gitti. Trail çıkışı 19 Ağu'da +%34'te "
            "sattı (120 gün tutsaydın +%156). MANAS 20 Eki – 5 Kas 2025: kod bulmadı (kutu 12 işlem günü, eşik 20). Üretim D13 ikisini de görmedi.",
            "- Gördüklerin halüsinasyon değil: o çöller vardı ve koştu. Ama aynı şekil o yıllarda yüzlerce kez çıktı; koşanları sen hatırlıyorsun, "
            "koşmayanları (VSNMD, PAPIL gibi) unutuyoruz. Şekil koşanı seçmiyor; sağ ayaktaki koşu aynı gün rastgele hissenin koşusu kadar."],
             boy=9)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "DERS: NEREDE APTALLIK VARDI, ŞİMDİ NE BİLİYORUZ", [
            "- Aptallık: aylarca 'çöl iz mi?' diye girişi ölçtük ve her seferinde 'iz değil, kazanç kırılım + trail'den' dedik. Kırılım + "
            "trail'in kendisini rastgele girişle hiç kıyaslamadık. Kıyaslayınca o da tutmadı.",
            "- Geçmişteki 'BIST 2023 işlem başı +%38-40' gibi sayılar sistemin değil, o yılın piyasasının sayısıydı: aynı gün rastgele hisse de "
            "aynısını yaptı. Sistemin 'gerçek sayısı' rastgele girişe göre farktır: ~0.",
            "- Senin koşan vakaların (TEHOL, MANAS, KTLEV…) gerçek, ama aynı kural binlerce sinyalde rastgeleden ayrışmıyor. Büyük kazancı "
            "seçmek değil, piyasada olup büyük kazananı kesmemek belirliyor (trail onları erken satıyor).",
            "- Çıkış kuralı bir sigorta: yatay piyasada derin kaybı azaltıyor (BIST 2024-26'da en çok), karşılığında ortalamadan veriyor.",
            "",
            "Karar gereken (senin):",
            "- Sistemin amacı: (a) piyasada kalıp büyük kazananı kesmemek (tut / gevşek trail) mi, (b) derin kaybı sınırlamak (mevcut stop + "
            "trail) mı? Veri ikisinin birden olmadığını söylüyor.",
            "- Üretim değişmedi. Çıkış ya da tespit değişikliği 'yaz' kararı.",
            "",
            "Sıradaki (önceden yazılı, kararın sonrası): aynı rastgele kıyas üretimdeki D13 + T6/T10 + trail zinciri için ve 2016-22 ayı "
            "döneminde (piyasa düşerken giriş seçimi ve stop daha mı değerli?)."])
        pdf.savefig(fig); plt.close(fig)
    return 5


# ---------------------------------------------------------------- K21 sağ ayak mum mum (Cemal 25 Eki)
# CEMAL (25 Eki): 'Tam çölden çıkan, koşmaya başlayan hisse ile rastgele günde alınan yolun eşit olma ihtimali sıfır; büyük bir yanlışın
# içindesin; çıkış kuralı değil, mumları kıyasla: kim yüzde olarak daha çok yol almış?' DENETİM (önceden yazıldı, sonuç görülmeden):
# (1) çıkış kuralı yok; her sinyal için girişten (atılım ertesi açılış) sonraki 1..120. gün kapanış yolu; aynı gün BORSADAKİ BÜTÜN hisselerin
# aynı girişle yolu (eşleştirme yok, örnekleme yok); sinyalin o gün bütün hisseler içindeki sırası (0 = en kötü, 0,5 = orta, 1 = en iyi).
# (2) EN SIKI ÇÖL (Cemal: 'çöl nadir'): K18 C1 + kutu >= 30 bar + bant <= %20 + düşüş <= -%50 + mum ve hacim <= düşüştekinin 0,80'i
# (MANAS Haz-Tem 2025 geçer: 32 bar, %16, -%62, 0,74 / 0,63). K20 ile aynı karar: 120 günde en yüksek, aynı gün eşli hisseye göre fark
# ay kümeli %90 alt sınırı > 0, dört hücre. (3) 'Mum mum üstün' = 60. ve 120. günde ortalama sıra %90 alt sınırı > 0,5, dört hücre.
FI_K21 = {"bar_min": 30, "bant": 0.20, "dusus": -0.50, "mum": 0.80, "hacim": 0.80, "ufuk": 120, "gun": (1, 5, 20, 60, 120), "boot": 1000}


def fi_k21_siki(K18: pd.DataFrame, E: Dict[str, Any] = FI_K21) -> pd.DataFrame:
    """K18 olaylarından en sıkı çöl (önceden yazılı eşikler, C1 profili içinde)."""
    K = K18[K18.varyant == "C1"]
    return K[(K.bar >= E["bar_min"]) & (K.bant <= E["bant"]) & (K.dusus <= E["dusus"]) & (K.mum_kat <= E["mum"])
             & (K.hacim_kat <= E["hacim"])]


def fi_k21_yol(V: Dict[str, pd.DataFrame], S: pd.DataFrame, E: Dict[str, Any] = FI_K21) -> Dict[str, Any]:
    """S (sembol, giris) için mum mum yol: P[j, k] = sinyal kapanış(giriş + k) / giriş açılışı - 1 (k = 0..ufuk-1), M[j, k] = aynı gün
    bütün diğer hisselerin aynı yolunun medyanı, R[j, k] = sinyalin o gün diğer hisseler içindeki sırası (altında kalan oran).
    Giriş günü işlem görmeyen ya da pencere dolmayan sinyal atlanır. Dönüş {'P','M','R','meta'}."""
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index(); O = pd.DataFrame({s: d.Open for s, d in V.items()}).reindex(C.index)
    Cv, Ov, kol, idx, u = C.to_numpy(float), O.to_numpy(float), {s: j for j, s in enumerate(C.columns)}, C.index, E["ufuk"]
    P, M, R, meta, onb = [], [], [], [], {}
    for r in S.itertuples():
        i = int(idx.searchsorted(pd.Timestamp(r.giris))); j = kol.get(r.sembol)
        if j is None or i + u > len(idx) or idx[i] != pd.Timestamp(r.giris):
            continue
        if i not in onb:
            with np.errstate(divide="ignore", invalid="ignore"):
                onb[i] = Cv[i:i + u] / Ov[i] - 1                                       # (ufuk x hisse)
        Y = onb[i]; p = Y[:, j]
        if not np.isfinite(p).all():
            continue
        D_ = np.delete(Y, j, axis=1); ok = np.isfinite(D_)
        P.append(p); M.append(np.nanmedian(np.where(ok, D_, np.nan), axis=1))
        R.append((np.where(ok, D_ < p[:, None], False).sum(1)) / np.maximum(ok.sum(1), 1)); meta.append((r.sembol, idx[i]))
    return {"P": np.array(P), "M": np.array(M), "R": np.array(R), "meta": pd.DataFrame(meta, columns=["sembol", "giris"])}


def fon_izi_k21(A: Optional[FIAyar] = None, V_hazir: Optional[Dict[str, Dict[str, pd.DataFrame]]] = None) -> Dict[str, Any]:
    """K21 sürücü: (1) en sıkı çöl K19/K20 kıyası (aynı gün eşli / rastgele hisse); (2) cemal, nadir, en_siki için mum mum yol ve sıra,
    BIST + ABD, 2023 / 2024-26. Çıktı k21_ozet.csv (kıyas + sıra kararı), k21_yol.csv (gün gün medyan yol), k21_islem.csv.gz."""
    A = A or FIAyar(); E, E19 = FI_K21, FI_K19
    K18 = pd.read_csv(os.path.join(A.cikti, "k18_olaylar.csv.gz"), parse_dates=["bilgi"], low_memory=False)
    T19 = pd.read_csv(os.path.join(A.cikti, "k19_islem.csv.gz"), parse_dates=["bilgi", "giris"], low_memory=False)
    rng = np.random.default_rng(21); Z: List[Dict[str, Any]] = []; Y: List[pd.DataFrame] = []; T: List[pd.DataFrame] = []
    for pazar in ("BIST", "ABD"):
        try:
            V = V_hazir[pazar] if V_hazir and pazar in V_hazir else fi_k1_veri(A.veri[pazar], pazar, A)
        except Exception as ex:
            filog.warning("K21 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        D = fi_k19_dizi(V)
        K = fi_k21_siki(K18[(K18.pazar == pazar) & (K18.bilgi >= E19["bas"])]); K = K.assign(stop=K.taban * (1 - E19["stop_tol"]))
        S21 = pd.DataFrame([y for y in (fi_k19_islem(D, r.sembol, pd.Timestamp(r.bilgi), stop=r.stop, E=E19) for r in K.itertuples()) if y])
        for dad, b, e_ in K19_DONEM:
            sin = {s_: T19[(T19.pazar == pazar) & (T19.donem == dad) & (T19.grup == "sistem") & (T19.sinyal == s_)] for s_ in ("cemal", "nadir")}
            Sx = S21[(S21.bilgi >= b) & (S21.bilgi <= e_)].reset_index(drop=True).assign(don_bas=b, don_bit=e_) if len(S21) else pd.DataFrame()
            sin["en_siki"] = Sx; z: Dict[str, Any] = {}
            if len(Sx):
                R = {tur: fi_k19_rastgele(D, Sx, tur, E19["cekilis"], E19) for tur in ("hisse", "esli")}
                z = fi_k19_kiyas(Sx, R, E19)
                T.append(Sx.assign(pazar=pazar, donem=dad, grup="sistem"))
                for tur, Rx in R.items():
                    T.append(Rx.assign(pazar=pazar, donem=dad, grup=tur))
            for s_, X in sin.items():
                if not len(X):
                    continue
                W = fi_k21_yol(V, X, E); n = len(W["P"])
                if not n:
                    continue
                zz: Dict[str, Any] = {"pazar": pazar, "donem": dad, "sinyal": s_, "n_yol": n, **(z if s_ == "en_siki" else {})}
                ay = W["meta"].giris.dt.to_period("M").astype(str).to_numpy(); aylar = np.unique(ay)
                for g in E["gun"]:
                    k = g - 1; rk = W["R"][:, k]; G = {a: rk[ay == a] for a in aylar}
                    bs = [np.concatenate([G[a] for a in rng.choice(aylar, len(aylar))]).mean() for _ in range(E["boot"])]
                    zz.update({f"g{g}_sinyal_med": float(np.median(W["P"][:, k])), f"g{g}_evren_med": float(np.median(W["M"][:, k])),
                               f"g{g}_sinyal_ort": float(W["P"][:, k].mean()), f"g{g}_sira": float(rk.mean()),
                               f"g{g}_sira_alt": float(np.percentile(bs, 5)), f"g{g}_ust_ceyrek": float((rk >= 0.75).mean()),
                               f"g{g}_alt_ceyrek": float((rk < 0.25).mean())})
                zz["mum_ustun"] = bool(zz["g60_sira_alt"] > 0.5 and zz["g120_sira_alt"] > 0.5)
                Z.append(zz)
                Y.append(pd.DataFrame({"pazar": pazar, "donem": dad, "sinyal": s_, "gun": np.arange(1, E["ufuk"] + 1),
                                       "sinyal_med": np.median(W["P"], 0), "sinyal_q25": np.percentile(W["P"], 25, 0),
                                       "sinyal_q75": np.percentile(W["P"], 75, 0), "evren_med": np.median(W["M"], 0), "sira": W["R"].mean(0)}))
                filog.info("K21 %s %s %s: n %d sira g60 %.3f g120 %.3f (alt %.3f) mum_ustun %s", pazar, dad, s_, n, zz["g60_sira"],
                           zz["g120_sira"], zz["g120_sira_alt"], zz["mum_ustun"])
    if not Z:
        raise RuntimeError("K21: sonuç yok")
    Zk = pd.DataFrame(Z); Zk.to_csv(os.path.join(A.cikti, "k21_ozet.csv"), index=False)
    Yk = pd.concat(Y, ignore_index=True); Yk.to_csv(os.path.join(A.cikti, "k21_yol.csv"), index=False)
    if T:
        pd.concat(T, ignore_index=True).to_csv(os.path.join(A.cikti, "k21_islem.csv.gz"), index=False)
    karar = {s: bool(Zk[Zk.sinyal == s].mum_ustun.all() and len(Zk[Zk.sinyal == s]) == 4) for s in Zk.sinyal.unique()}
    siki = Zk[Zk.sinyal == "en_siki"]
    karar["en_siki_sag_ayak"] = bool(len(siki) == 4 and siki.get("sag_ayak_ustun", pd.Series(False)).fillna(False).astype(bool).all())
    return {"ozet": Zk, "yol": Yk, "karar": karar}


# ---------------------------------------------------------------- K22 bekleyen alış emri (Cemal 25 Eki, MANAS 18 Tem - 8 Ağu 2025)
# CEMAL: 'MANAS Haziran-Temmuz çöl mumlarını bulup "dip oluştu, artık aşağı düşmeyecek" dediğimiz an; adil ölçmeni istediğim 18 Temmuz -
# 8 Ağustos, çölün sağ ayağı; buradaki yükseliş sıradan bir hisseden fazla olmalı.' K21 bulgusu: çölün son gününden ölçülünce (atılım mumu
# dahil) çöl hisseleri aynı gün bütün hisselerin üstünde (sıra ~0,6), atılım kapanışından sonra ortada (~0,5): fark atılım mumunda.
# Atılım mumunu alınabilir kılan tek emir: çöl tavanının üstünde BEKLEYEN alış emri (gün içinde dolar). ÖNCEDEN YAZILDI (sonuç görülmeden):
# kutu t-1'de biter (K18 kutusu, profil ölçüleri yalnız kutu), emir seviyesi = max(kutu tavanı, önceki 20 bar gövde tepesi) x 1,002;
# High[t] >= seviye -> dolum max(Open[t], seviye); kapanış geri kutuya dönse de işlem (sahte kırılım dahil); hissede 60 barda tek.
# Ölçü: dolumdan k gün sonra kapanış / dolum - 1 (k = 15 Cemal'in penceresi, 60, 120); aynı gün bütün hisseler kapanış(t+k) / açılış(t) - 1;
# sıra. Karar: 60 ve 120. gün sıra ay kümeli %90 alt sınırı > 0,5, dört hücre (BIST / ABD x 2023 / 2024-26). Sinyaller: profil (C1
# eşikleri), nadir (+ bant <= %20, düşüş <= -%50).
FI_K22 = {"gun": (0, 15, 60, 120), "boot": 1000}


def fi_k22_emir_tara(V: Dict[str, pd.DataFrame], E: Dict[str, Any] = FI_K18_ESIK, bas: str = "2023-01-01") -> pd.DataFrame:
    """Bekleyen alış emri dolumları: sembol, bilgi (= t, dolum günü), seviye, dolum, sahte (kapanış < seviye), kutu ölçüleri."""
    sat: List[Dict[str, Any]] = []; b0 = E["bar"][0]; t0 = pd.Timestamp(bas)
    for s, d in V.items():
        try:
            if len(d) < b0 + 80:
                continue
            o = d.Open.to_numpy(float); c = d.Close.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float)
            if not (l > 0).all():
                continue
            top = np.maximum(o, c); hh = pd.Series(top).rolling(E["son20"]).max().shift(1).to_numpy()
            son = -10 ** 9; ib = int(d.index.searchsorted(t0))
            for t in np.flatnonzero(h > hh * 1.002):
                if t < max(ib, b0 + 21) or t - son < E["tekrar"]:
                    continue
                i0 = _fi_k18_kutu(top, l, int(t), E)
                if i0 < 0 or t - i0 < b0:
                    continue
                sev = max(top[i0:t].max(), hh[t]) * 1.002
                if not (h[t] >= sev):
                    continue
                r = fi_k18_olc(d, i0, int(t))
                if not (r["dusus"] <= E["dusus"] and r["mum_kat"] <= E["mum"] and r["hacim_kat"] <= E["hacim"]):
                    continue
                son = int(t)
                sat.append({"sembol": s, "bilgi": d.index[t], "seviye": sev, "dolum": max(o[t], sev), "sahte": bool(c[t] < sev),
                            **{k: r[k] for k in ("bar", "dusus", "bant", "mum_kat", "hacim_kat")}})
        except Exception as ex:   # tek hisse bozuksa digerleri devam eder
            filog.warning("K22 %s atlandi: %s", s, ex)
    return pd.DataFrame(sat)


def fi_k22_sira(V: Dict[str, pd.DataFrame], S: pd.DataFrame, E: Dict[str, Any] = FI_K22) -> pd.DataFrame:
    """Her dolum için k gün sonra getiri (dolumdan) ve aynı gün bütün diğer hisselerin açılıştan getirisi içindeki sırası."""
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index(); O = pd.DataFrame({s: d.Open for s, d in V.items()}).reindex(C.index)
    Cv, Ov, kol, idx = C.to_numpy(float), O.to_numpy(float), {s: j for j, s in enumerate(C.columns)}, C.index
    sat = []
    for r in S.itertuples():
        j = kol.get(r.sembol); t = int(idx.searchsorted(pd.Timestamp(r.bilgi)))
        if j is None or t >= len(idx) or idx[t] != pd.Timestamp(r.bilgi):
            continue
        z = {"sembol": r.sembol, "bilgi": idx[t], "sahte": r.sahte}
        for k in E["gun"]:
            if t + k >= len(idx):
                z[f"r{k}"] = z[f"s{k}"] = z[f"m{k}"] = np.nan; continue
            with np.errstate(divide="ignore", invalid="ignore"):
                y = Cv[t + k] / Ov[t] - 1
            p = Cv[t + k, j] / r.dolum - 1; y = np.delete(y, j); y = y[np.isfinite(y)]
            z[f"r{k}"], z[f"s{k}"], z[f"m{k}"] = p, (float((y < p).mean()) if len(y) and p == p else np.nan), (float(np.median(y)) if len(y) else np.nan)
        sat.append(z)
    return pd.DataFrame(sat)


def fi_k22_pencere(V: Dict[str, pd.DataFrame], K: pd.DataFrame, g: int = 15) -> pd.DataFrame:
    """Cemal'in penceresi: çölün son günü kapanışından (atılımdan önceki gün, t-1) g işlem günü sonrasına (atılım mumu DAHİL, sonradan
    bilinen) ve atılım kapanışından (t) g gün sonrasına (alınabilen); aynı pencerede bütün diğer hisseler içindeki sıra. K: sembol, bilgi."""
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index(); Cv, idx = C.to_numpy(float), C.index
    kol = {s: j for j, s in enumerate(C.columns)}; sat = []
    for r in K.itertuples():
        j = kol.get(r.sembol); t = int(idx.searchsorted(pd.Timestamp(r.bilgi)))
        if j is None or t < 1 or t + g >= len(idx) or idx[t] != pd.Timestamp(r.bilgi):
            continue
        z = {"sembol": r.sembol, "bilgi": idx[t]}
        for ad, a in (("dahil", t - 1), ("sonra", t)):
            with np.errstate(divide="ignore", invalid="ignore"):
                y = Cv[a + g] / Cv[a] - 1
            p = y[j]; y = np.delete(y, j); y = y[np.isfinite(y)]
            z[f"{ad}_r"], z[f"{ad}_evren"], z[f"{ad}_sira"] = p, (float(np.median(y)) if len(y) else np.nan), (float((y < p).mean()) if len(y) and p == p else np.nan)
        sat.append(z)
    return pd.DataFrame(sat)


def fon_izi_k22(A: Optional[FIAyar] = None, V_hazir: Optional[Dict[str, Dict[str, pd.DataFrame]]] = None) -> Dict[str, Any]:
    """K22 sürücü: profil ve nadir çölde bekleyen alış emri, BIST + ABD, 2023 / 2024-26; sıra kararı. Çıktı k22_ozet.csv, k22_islem.csv.gz."""
    A = A or FIAyar(); E = FI_K22; rng = np.random.default_rng(22); Z: List[Dict[str, Any]] = []; T: List[pd.DataFrame] = []
    PN: List[Dict[str, Any]] = []
    for pazar in ("BIST", "ABD"):
        try:
            V = V_hazir[pazar] if V_hazir and pazar in V_hazir else fi_k1_veri(A.veri[pazar], pazar, A)
        except Exception as ex:
            filog.warning("K22 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        S0 = fi_k22_emir_tara(V)
        if not len(S0):
            continue
        X0 = fi_k22_sira(V, S0, E).merge(S0[["sembol", "bilgi", "bant", "dusus"]], on=["sembol", "bilgi"], how="left")
        for sad, X1 in (("profil", X0), ("nadir", X0[(X0.bant <= FI_K18_C4["bant"]) & (X0.dusus <= -0.50)])):
            for dad, b, e_ in K19_DONEM:
                X = X1[(X1.bilgi >= b) & (X1.bilgi <= e_)]
                if not len(X):
                    continue
                z: Dict[str, Any] = {"pazar": pazar, "donem": dad, "sinyal": sad, "n": len(X), "sahte": float(X.sahte.mean())}
                for k in E["gun"]:
                    x = X.dropna(subset=[f"s{k}"]); ay = x.bilgi.dt.to_period("M").astype(str).to_numpy(); aylar = np.unique(ay)
                    if not len(x):
                        continue
                    G = {a: x[f"s{k}"].to_numpy()[ay == a] for a in aylar}
                    bs = [np.concatenate([G[a] for a in rng.choice(aylar, len(aylar))]).mean() for _ in range(E["boot"])]
                    z.update({f"g{k}_n": len(x), f"g{k}_med": float(x[f"r{k}"].median()), f"g{k}_ort": float(x[f"r{k}"].mean()),
                              f"g{k}_evren_med": float(x[f"m{k}"].median()), f"g{k}_sira": float(x[f"s{k}"].mean()),
                              f"g{k}_sira_alt": float(np.percentile(bs, 5)), f"g{k}_ust_ceyrek": float((x[f"s{k}"] >= 0.75).mean())})
                z["emir_ustun"] = bool(z.get("g60_sira_alt", 0) > 0.5 and z.get("g120_sira_alt", 0) > 0.5)
                Z.append(z); T.append(X.assign(pazar=pazar, donem=dad, sinyal=sad))
                filog.info("K22 %s %s %s: n %d sahte %.2f sira g15 %.3f g60 %.3f g120 %.3f (alt %.3f) ustun %s", pazar, dad, sad, z["n"],
                           z["sahte"], z.get("g15_sira", np.nan), z.get("g60_sira", np.nan), z.get("g120_sira", np.nan),
                           z.get("g120_sira_alt", np.nan), z["emir_ustun"])
        try:                                                                   # Cemal'in penceresi, K18 atılımlarında (kapanışla kırılım)
            K18 = pd.read_csv(os.path.join(A.cikti, "k18_olaylar.csv.gz"), parse_dates=["bilgi"], low_memory=False)
            K18 = K18[(K18.pazar == pazar) & (K18.bilgi >= FI_K19["bas"])]
            for sad, Kx in (("profil", K18[K18.varyant == "C1"]), ("nadir", K18[(K18.varyant == "C4") & (K18.dusus <= -0.50)])):
                for dad, b, e_ in K19_DONEM:
                    Pw = fi_k22_pencere(V, Kx[(Kx.bilgi >= b) & (Kx.bilgi <= e_)])
                    if len(Pw):
                        PN.append({"pazar": pazar, "donem": dad, "sinyal": sad, "n": len(Pw),
                                   **{f"{a}_{m}": float(getattr(Pw[f"{a}_{x}"], m)()) for a in ("dahil", "sonra") for x, m in (("r", "median"), ("sira", "mean"))},
                                   "dahil_evren": float(Pw.dahil_evren.median())})
        except Exception as ex:
            filog.warning("K22 %s pencere ölçülemedi: %s", pazar, ex)
    if PN:
        pd.DataFrame(PN).to_csv(os.path.join(A.cikti, "k22_pencere.csv"), index=False)
    if not Z:
        raise RuntimeError("K22: sonuç yok")
    Zk = pd.DataFrame(Z); Zk.to_csv(os.path.join(A.cikti, "k22_ozet.csv"), index=False)
    pd.concat(T, ignore_index=True).to_csv(os.path.join(A.cikti, "k22_islem.csv.gz"), index=False)
    karar = {s: bool(Zk[Zk.sinyal == s].emir_ustun.all() and len(Zk[Zk.sinyal == s]) == 4) for s in Zk.sinyal.unique()}
    return {"ozet": Zk, "karar": karar}


# ---------------------------------------------------------------- K23 bölge parmak izi + birebir benzer bölgeler (Cemal 25 Eki)
# CEMAL (25 Eki, MANAS grafiğinde iki bölge işaretli): 'Şu işaretli bölgenin her özelliğini kaydet: eğim, küçük mum, kırmızı-yeşil oranı,
# alt fitil, üst fitil, birbirine yakınlık, düzeni bozan mum sayısı, hacim oranı, RSI, MACD... Birebir aynı görünümdeki bölgelerin yüzde kaçı
# yukarı çıkmış, yüzde kaçı aşağı düşmüş, yüzde kaçı yatayda kalmış? Bu bir halüsinasyon mu? Ben ısrarla değil diyorum.' (KNN kapalı konu;
# Cemal'in doğrudan isteğiyle açıldı.) ÖNCEDEN YAZILDI (sonuç görülmeden): bölgeler FI_K23['bolge'] (aşağıdaki düzeltme notu). Parmak izi (yalnız bölge ve öncesi): eğim (log kapanış OLS, bar
# başı), mum (bölge H-L medyanı / önceki 60 bar), yeşil oranı, alt fitil ve üst fitil (H-L'ye oran, medyan), yakınlık (kapanış std / ort.),
# bozan (H-L > 2 x bölge medyanı olan mum oranı), hacim (TL hacim medyanı / önceki 60 bar), RSI14 ve MACD histogramı / fiyat (bitiş günü),
# düşüş (bölge dibi / önceki 120 bar tepesi - 1), konum (bitiş kapanışının bölge aralığındaki yeri). Benzerlik: her ölçü hücrenin bütün
# pencerelerinin medyan / IQR'si ile ölçeklenir (±5 kırpılır), Öklid uzaklığı; en yakın K (100) pencere, aynı hissede 60 bar içinde tek
# (en yakını). Sonuç bitiş kapanışından: 60 barda önce +%15 (High) -> YUKARI, önce -%15 (Low) -> AŞAĞI, ikisi yok -> YATAY (aynı bar ikisi
# -> aşağı); kısa: 20 barda ±%10. Karar: en yakın K'nin yukarı oranı / hücrenin bütün pencerelerinin yukarı oranı >= 1,3, dört hücrede
# (BIST / ABD x 2023 / 2024-26). MANAS'ın kendisi (bölge ±120 bar) kıyastan çıkarılır.
# DÜZELTME (Cemal aynı gün tarihleri verdi; ilk okumamın yerine onunkiler): 1 = 13.06-21.07.2025 (ilk çöl, 21 Tem atılım barı dahil),
# 2 = 20.10-05.11.2025 (ikinci çöl). Grafikten okuduğum 17.11-04.12.2025 silkelemesi (S) kayıtta kalır; ilk okumam 29.09-05.11 (A) bıraktım.
# DÜZELTME 2 (Cemal: 'yanlış yazdım, birincisi 13 Haziran - 13 Temmuz') ve EK ÖLÇÜLER (Cemal: 'birinci evre kırmızı SMA altında, ikinci
# evre kırmızı SMA üstünde dizilme, muntazam, delen yok neredeyse'; BB 20,2 orta bandı): seri (bitişteki SMA20 üstü kapanış serisi / L =
# 2. evrenin payı), once_alt (serinin öncesindeki pencere kısmında SMA20 altı kapanış oranı = 1. evre), delen (serideki Low < SMA20 oranı),
# bbw (bitişte BB genişliği 4 sigma / SMA20, pencere içindeki en yükseğine oran = sıkışma).
# EK (Cemal aynı gün: 'BINBN de var, 27 Aralık - 21 Ocak arası'): bölge 3 = BINBN 27.12.2024-21.01.2025 (düşüş sonrası SMA20 altında yatay,
# BB 0,61 -> 0,027 sıkışma; 21 Ocak SMA20 üstündeki ilk kapanış). Aynı ölçü ve karar; sonuç görülmeden eklendi.
FI_K23 = {"bolge": {"1": ("MANAS", "2025-06-13", "2025-07-13"), "2": ("MANAS", "2025-10-20", "2025-11-05"),
                    "S": ("MANAS", "2025-11-17", "2025-12-04"), "3": ("BINBN", "2024-12-27", "2025-01-21")}, "k": 100, "ayri": 60,
          "ufuk": 60, "esik": 0.15, "kisa_ufuk": 20, "kisa_esik": 0.10, "kirp": 5.0, "kat_esik": 1.3,
          "olcu": ("egim", "mum", "yesil", "alt_fitil", "ust_fitil", "yakinlik", "bozan", "hacim", "rsi", "macd", "dusus", "konum",
                   "seri", "once_alt", "delen", "bbw")}


def fi_k23_parmak(d: pd.DataFrame, L: int) -> pd.DataFrame:
    """Her bitiş günü t için [t-L+1, t] penceresinin parmak izi (yalnız t ve öncesi) ve t kapanışından sonraki sonuçlar (yon60, yon20)."""
    import warnings
    from numpy.lib.stride_tricks import sliding_window_view as swv
    warnings.filterwarnings("ignore", message="All-NaN slice encountered")   # kilitli (H = L) günlerden oluşan pencere: ölçü NaN, atlanır
    o = d.Open.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float); c = d.Close.to_numpy(float)
    v = (d.Close * d.Volume).to_numpy(float); n = len(c); E = FI_K23
    if n < L + 200:
        return pd.DataFrame()
    pc = np.r_[np.nan, c[:-1]]
    with np.errstate(divide="ignore", invalid="ignore"):
        m = (h - l) / pc; rg = h - l
        alt = np.where(rg > 0, (np.minimum(o, c) - l) / rg, np.nan); ust = np.where(rg > 0, (h - np.maximum(o, c)) / rg, np.nan)
    e = np.arange(L - 1, n)                                                   # pencere bitiş indeksleri
    Mw, Aw, Uw, Cw = swv(m, L), swv(alt, L), swv(ust, L), swv(c, L)
    with np.errstate(all="ignore"):
        mmed = np.nanmedian(Mw, 1)
        on_m = pd.Series(m).rolling(60, min_periods=40).median().shift(L).to_numpy()[e]
        on_v = pd.Series(v).rolling(60, min_periods=40).median().shift(L).to_numpy()[e]
        x = np.arange(L, dtype=float); xc = x - x.mean(); ly = np.log(Cw)
        egim = (ly * xc).sum(1) / (xc ** 2).sum()
        hl = swv(h, L).max(1); ll = swv(l, L).min(1)
        tepe = pd.Series(h).rolling(120, min_periods=20).max().shift(L).to_numpy()[e]   # 20: genç halka arz da ölçülür (BINBN 55 bar)
        dl = np.diff(c, prepend=np.nan); up = pd.Series(np.clip(dl, 0, None)).ewm(alpha=1 / 14, adjust=False).mean()
        dn = pd.Series(np.clip(-dl, 0, None)).ewm(alpha=1 / 14, adjust=False).mean(); rsi = (100 - 100 / (1 + up / dn)).to_numpy()
        cs = pd.Series(c); mac = cs.ewm(span=12, adjust=False).mean() - cs.ewm(span=26, adjust=False).mean()
        mh = ((mac - mac.ewm(span=9, adjust=False).mean()) / cs).to_numpy()
        F = pd.DataFrame({"egim": egim, "mum": mmed / on_m, "yesil": (swv(c, L) > swv(o, L)).mean(1),
                          "alt_fitil": np.nanmedian(Aw, 1), "ust_fitil": np.nanmedian(Uw, 1), "yakinlik": Cw.std(1) / Cw.mean(1),
                          "bozan": (Mw > 2 * mmed[:, None]).mean(1), "hacim": np.median(swv(v, L), 1) / on_v, "rsi": rsi[e], "macd": mh[e],
                          "dusus": ll / tepe - 1, "konum": (c[e] - ll) / np.where(hl > ll, hl - ll, np.nan)}, index=d.index[e])
    # iki evre (Cemal): SMA20 altı (1. evre) -> SMA20 üstünde dizilme (2. evre); kümülatif toplamlarla
    sma = cs.rolling(20).mean().to_numpy(); bw = (4 * cs.rolling(20).std() / cs.rolling(20).mean()).to_numpy()
    ust_ = c > sma; seri = np.zeros(n, int)
    for t in range(n):
        seri[t] = seri[t - 1] + 1 if (ust_[t] and t > 0) else int(ust_[t])
    alt_c = np.r_[0, np.cumsum(c < sma)]; del_c = np.r_[0, np.cumsum(l < sma)]
    s_ = np.minimum(seri[e], L); bas = e - L + 1; orta = e - s_ + 1                       # 1. evre [bas, orta-1], 2. evre [orta, e]
    with np.errstate(all="ignore"):
        F["seri"] = s_ / L
        F["once_alt"] = np.where(orta > bas, (alt_c[orta] - alt_c[bas]) / (orta - bas), 0.0)
        F["delen"] = np.where(s_ > 0, (del_c[e + 1] - del_c[orta]) / np.maximum(s_, 1), 1.0)
        F["bbw"] = bw[e] / swv(bw, L).max(1)
    F["i"] = e
    # sonuç: t kapanışından sonra (t+1 ... t+ufuk) önce +esik (High) mi, önce -esik (Low) mu
    def yon(u, s):
        out = np.full(len(e), np.nan)
        for j, t in enumerate(e):
            if t + u >= n:
                continue
            g = c[t]; hu = np.flatnonzero(h[t + 1:t + 1 + u] >= g * (1 + s)); lo = np.flatnonzero(l[t + 1:t + 1 + u] <= g * (1 - s))
            a, b = (hu[0] if len(hu) else 10 ** 9), (lo[0] if len(lo) else 10 ** 9)
            out[j] = 1.0 if a < b else (-1.0 if b <= a and b < 10 ** 9 else 0.0)
        return out
    F["yon60"] = yon(E["ufuk"], E["esik"]); F["yon20"] = yon(E["kisa_ufuk"], E["kisa_esik"])
    return F.replace([np.inf, -np.inf], np.nan)


def fi_k23_esle(P: pd.DataFrame, hedef: pd.Series, E: Dict[str, Any] = FI_K23) -> pd.DataFrame:
    """P (bir hücrenin bütün pencereleri: sembol, tarih, ölçüler) içinde hedef parmak izine en yakın K pencere; ölçek hücrenin medyan/IQR'si;
    aynı hissede E['ayri'] bar içinde tek (en yakın)."""
    O = list(E["olcu"]); X = P[O]
    med = X.median(); iqr = (X.quantile(0.75) - X.quantile(0.25)).replace(0, np.nan)
    Z = ((X - med) / iqr).clip(-E["kirp"], E["kirp"]); z0 = ((hedef[O].astype(float) - med) / iqr).clip(-E["kirp"], E["kirp"])
    P = P.assign(uzak=np.sqrt(((Z - z0) ** 2).sum(1, min_count=len(O)))).dropna(subset=["uzak"]).sort_values("uzak")
    sec, son = [], {}
    for r in P.itertuples():
        if any(abs(r.i - k) < E["ayri"] for k in son.get(r.sembol, [])):
            continue
        son.setdefault(r.sembol, []).append(r.i); sec.append(r.Index)
        if len(sec) >= E["k"]:
            break
    return P.loc[sec]


def fon_izi_k23(A: Optional[FIAyar] = None, V_hazir: Optional[Dict[str, Dict[str, pd.DataFrame]]] = None) -> Dict[str, Any]:
    """K23 sürücü: bölge A ve B'nin parmak izi; BIST + ABD bütün pencereleri; hücre (pazar x 2016-22 / 2023 / 2024-26) içinde en yakın K ve
    yukarı / aşağı / yatay oranları, hücre tabanına göre kat. Çıktı k23_ozet.csv, k23_esler.csv, k23_parmak.csv."""
    A = A or FIAyar(); E = FI_K23; donem = [("2016-22", "2016-01-01", "2022-12-31")] + K19_DONEM
    Vb = V_hazir["BIST"] if V_hazir and "BIST" in V_hazir else fi_k1_veri(A.veri["BIST"], "BIST", A)
    H: Dict[str, pd.Series] = {}
    for ad, (s, b, e_) in E["bolge"].items():
        d = Vb[s]; L = int(((d.index >= b) & (d.index <= e_)).sum())
        son_g = d.index[d.index <= pd.Timestamp(e_)][-1]                       # bölge sonu tatile düşerse önceki işlem günü
        F = fi_k23_parmak(d, L); H[ad] = F.loc[son_g].copy(); H[ad]["L"] = L; H[ad]["sembol"] = s; H[ad]["son"] = son_g
    Z: List[Dict[str, Any]] = []; ES: List[pd.DataFrame] = []
    for pazar in ("BIST", "ABD"):
        try:
            V = Vb if pazar == "BIST" else (V_hazir["ABD"] if V_hazir and "ABD" in V_hazir else fi_k1_veri(A.veri["ABD"], "ABD", A))
        except Exception as ex:
            filog.warning("K23 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        for ad, h0 in H.items():
            L = int(h0["L"]); parca = []
            for s, d in V.items():
                try:
                    F = fi_k23_parmak(d, L)
                    if len(F):
                        parca.append(F.assign(sembol=s))
                except Exception as ex:   # tek hisse bozuksa digerleri devam eder
                    filog.warning("K23 %s atlandi: %s", s, ex)
            P = pd.concat(parca).rename_axis("tarih").reset_index()
            s0, b0 = h0["sembol"], pd.Timestamp(h0["son"])
            P = P[~((P.sembol == s0) & ((P.tarih - b0).abs() <= pd.Timedelta(days=180)))].dropna(subset=list(E["olcu"]) + ["yon60"])
            for dad, b, e_ in donem:
                Px = P[(P.tarih >= b) & (P.tarih <= e_)].reset_index(drop=True)
                if len(Px) < 1000:
                    continue
                M = fi_k23_esle(Px, h0, E); z: Dict[str, Any] = {"bolge": ad, "pazar": pazar, "donem": dad, "n_pencere": len(Px), "k": len(M),
                                                               "uzak_med": float(M.uzak.median())}
                for u in ("yon60", "yon20"):
                    x = M[u].dropna(); t_ = Px[u].dropna()
                    z.update({f"{u}_yukari": float((x == 1).mean()), f"{u}_asagi": float((x == -1).mean()), f"{u}_yatay": float((x == 0).mean()),
                              f"{u}_taban_yukari": float((t_ == 1).mean()), f"{u}_taban_asagi": float((t_ == -1).mean()),
                              f"{u}_taban_yatay": float((t_ == 0).mean())})
                z["kat60"] = z["yon60_yukari"] / z["yon60_taban_yukari"] if z["yon60_taban_yukari"] > 0 else np.nan
                z["kat20"] = z["yon20_yukari"] / z["yon20_taban_yukari"] if z["yon20_taban_yukari"] > 0 else np.nan
                Z.append(z); ES.append(M.assign(bolge=ad, pazar=pazar, donem=dad))
                filog.info("K23 %s %s %s: n %d en yakin %d yukari %.2f (taban %.2f, kat %.2f) asagi %.2f yatay %.2f", ad, pazar, dad, len(Px),
                           len(M), z["yon60_yukari"], z["yon60_taban_yukari"], z["kat60"], z["yon60_asagi"], z["yon60_yatay"])
    if not Z:
        raise RuntimeError("K23: sonuç yok")
    Zk = pd.DataFrame(Z); Zk.to_csv(os.path.join(A.cikti, "k23_ozet.csv"), index=False)
    pd.concat(ES, ignore_index=True).to_csv(os.path.join(A.cikti, "k23_esler.csv"), index=False)
    pd.DataFrame(H).T.to_csv(os.path.join(A.cikti, "k23_parmak.csv"))
    karar = {}
    for ad in H:
        X = Zk[(Zk.bolge == ad) & (Zk.donem != "2016-22")]
        karar[ad] = bool(len(X) == 4 and (X.kat60 >= E["kat_esik"]).all())
    return {"ozet": Zk, "parmak": pd.DataFrame(H).T, "karar": karar}


# ---------------------------------------------------------------- K24 iki evre kuralı (Cemal 25 Eki)
# CEMAL: 'Birinci evre kırmızı SMA (BB 20 orta bandı) altında, ikinci evre kırmızı SMA üstünde dizilme, muntazam, delen yok neredeyse.'
# ÖNCEDEN YAZILDI (eşikler MANAS 13.06-11.07.2025 ve 20.10-05.11.2025'ten, evren sonucu görülmeden): t günü SMA20 üstündeki kapanış
# serisi tam 5'e ulaşır (dizilme teyidi); serinin öncesindeki 10 barın >= %80'i SMA20 altında kapanmış (1. evre); serideki 5 mumun en
# fazla 2'sinin dibi SMA20'yi deler; BB genişliği (4 sigma / SMA20) son 15 barın en yükseğinin <= %70'i (sıkışma); son 15 barın dibi önceki
# 120 bar tepesinin <= -%30 altında (düşüş sonrası); hissede 60 barda tek. MANAS 10.07.2025 ve 05.11.2025'te tetikler.
# EŞLİ: aynı gün yapısı (düşüş <= -%30 ve SMA20 üstünde 5. gün) ama 1. evre / delen / sıkışma şartlarından en az biri tutmayan günler.
# Sonuç t kapanışından (K23 ile aynı): 60 barda önce +%15 / önce -%15 / yatay; 20 barda ±%10. Karar: yukarı oranı eşlinin >= 1,3 katı,
# dört hücre (BIST / ABD x 2023 / 2024-26), n >= 30.
# Ayar (evren sonucu görülmeden): MANAS 1. bölgede serinin 5 mumundan 2'si SMA20'yi deliyor (04.07 ve 08.07); 'en fazla 1' iki örneğin
# birini dışarıda bıraktığı için 'en fazla 2' yapıldı (kalibrasyon iki vakaya, sonuç ölçülmeden).
FI_K24 = {"seri": 5, "once": 10, "once_alt": 0.80, "delen_en_cok": 2, "bbw_oran": 0.70, "bbw_pencere": 15, "dusus": -0.30, "tekrar": 60}


def _fi_k23_yon(c: np.ndarray, h: np.ndarray, l: np.ndarray, t: int, u: int, s: float) -> float:
    """t kapanışından sonraki u barda önce +s (High) -> 1, önce -s (Low) -> -1 (aynı bar -> -1), ikisi yok -> 0; pencere dolmamışsa NaN."""
    if t + u >= len(c):
        return np.nan
    g = c[t]; hu = np.flatnonzero(h[t + 1:t + 1 + u] >= g * (1 + s)); lo = np.flatnonzero(l[t + 1:t + 1 + u] <= g * (1 - s))
    a, b = (hu[0] if len(hu) else 10 ** 9), (lo[0] if len(lo) else 10 ** 9)
    return 1.0 if a < b else (-1.0 if b < 10 ** 9 else 0.0)


def fi_k24_tara(d: pd.DataFrame, E: Dict[str, Any] = FI_K24) -> pd.DataFrame:
    """Bir hissede iki evre günleri: kural (sinyal) ve eşli (aynı düşüş + SMA20 üstü 5. gün, kuralın geri kalanı tutmayan)."""
    c = d.Close.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float); n = len(c); E3 = FI_K23
    if n < 200:
        return pd.DataFrame()
    cs = pd.Series(c); sma = cs.rolling(20).mean().to_numpy(); bw = (4 * cs.rolling(20).std() / cs.rolling(20).mean()).to_numpy()
    tepe = pd.Series(h).rolling(120, min_periods=20).max().to_numpy()      # 20: genç halka arz da ölçülür
    seri = np.zeros(n, int)
    for t in range(1, n):
        seri[t] = seri[t - 1] + 1 if c[t] > sma[t] else 0
    sat, son = [], {True: -10 ** 9, False: -10 ** 9}
    w = E["bbw_pencere"]; k = E["seri"]
    for t in np.flatnonzero(seri == k):
        a = t - k + 1; b0 = a - E["once"]
        if b0 < 20 or not np.isfinite(tepe[t - w]):
            continue
        dus = l[t - w + 1:t + 1].min() / tepe[t - w] - 1
        if not (dus <= E["dusus"]):
            continue
        once = float((c[b0:a] < sma[b0:a]).mean()); delen = int((l[a:t + 1] < sma[a:t + 1]).sum())
        bo = float(bw[t] / np.nanmax(bw[t - w + 1:t + 1])) if np.isfinite(bw[t]) else np.nan
        kural = bool(once >= E["once_alt"] and delen <= E["delen_en_cok"] and bo <= E["bbw_oran"])
        if t - son[kural] < E["tekrar"]:
            continue
        son[kural] = int(t)
        sat.append({"tarih": d.index[t], "kural": kural, "once_alt": once, "delen": delen, "bbw": bo, "dusus": dus,
                    "yon60": _fi_k23_yon(c, h, l, int(t), E3["ufuk"], E3["esik"]),
                    "yon20": _fi_k23_yon(c, h, l, int(t), E3["kisa_ufuk"], E3["kisa_esik"]),
                    "r120": c[t + 120] / c[t] - 1 if t + 120 < n else np.nan})
    return pd.DataFrame(sat)


def fon_izi_k24(A: Optional[FIAyar] = None, V_hazir: Optional[Dict[str, Dict[str, pd.DataFrame]]] = None) -> Dict[str, Any]:
    """K24 sürücü: iki evre kuralı vs eşli, BIST + ABD, 2016-22 / 2023 / 2024-26. Çıktı k24_ozet.csv, k24_olaylar.csv.gz."""
    A = A or FIAyar(); E = FI_K24; donem = [("2016-22", "2016-01-01", "2022-12-31")] + K19_DONEM
    Z: List[Dict[str, Any]] = []; T: List[pd.DataFrame] = []
    for pazar in ("BIST", "ABD"):
        try:
            V = V_hazir[pazar] if V_hazir and pazar in V_hazir else fi_k1_veri(A.veri[pazar], pazar, A)
        except Exception as ex:
            filog.warning("K24 %s verisi okunamadi, atlandi: %s", pazar, ex); continue
        parca = []
        for s, d in V.items():
            try:
                X = fi_k24_tara(d, E)
                if len(X):
                    parca.append(X.assign(sembol=s, pazar=pazar))
            except Exception as ex:   # tek hisse bozuksa digerleri devam eder
                filog.warning("K24 %s atlandi: %s", s, ex)
        if not parca:
            continue
        P = pd.concat(parca, ignore_index=True); T.append(P)
        for dad, b, e_ in donem:
            Px = P[(P.tarih >= b) & (P.tarih <= e_)]
            S, Q = Px[Px.kural].dropna(subset=["yon60"]), Px[~Px.kural].dropna(subset=["yon60"])
            if not len(S) or not len(Q):
                continue
            z = {"pazar": pazar, "donem": dad, "n": len(S), "n_esli": len(Q)}
            for u in ("yon60", "yon20"):
                z.update({f"{u}_yukari": float((S[u] == 1).mean()), f"{u}_asagi": float((S[u] == -1).mean()), f"{u}_yatay": float((S[u] == 0).mean()),
                          f"{u}_esli_yukari": float((Q[u] == 1).mean()), f"{u}_esli_asagi": float((Q[u] == -1).mean()),
                          f"{u}_esli_yatay": float((Q[u] == 0).mean())})
            z["kat60"] = z["yon60_yukari"] / z["yon60_esli_yukari"] if z["yon60_esli_yukari"] > 0 else np.nan
            z["kat20"] = z["yon20_yukari"] / z["yon20_esli_yukari"] if z["yon20_esli_yukari"] > 0 else np.nan
            z["r120_med"], z["r120_esli_med"] = float(S.r120.median()), float(Q.r120.median())
            Z.append(z)
            filog.info("K24 %s %s: n %d (esli %d) yukari %.2f vs %.2f kat %.2f", pazar, dad, len(S), len(Q), z["yon60_yukari"],
                       z["yon60_esli_yukari"], z["kat60"])
    if not Z:
        raise RuntimeError("K24: sonuç yok")
    Zk = pd.DataFrame(Z); Zk.to_csv(os.path.join(A.cikti, "k24_ozet.csv"), index=False)
    pd.concat(T, ignore_index=True).to_csv(os.path.join(A.cikti, "k24_olaylar.csv.gz"), index=False)
    X = Zk[Zk.donem != "2016-22"]
    return {"ozet": Zk, "karar": bool(len(X) == 4 and ((X.kat60 >= FI_K23["kat_esik"]) & (X.n >= 30)).all())}


# ---------------------------------------------------------------- K25 çöl = büyük alıcının izi mi? (Cemal 25 Eki)
# CEMAL: 'Ben bu çöl formasyonunu fon ilişkisi olup olmadığını bilmeden inceleyip gördüm; sonra söylediklerimin çoğu fon hisselerinde çıktı.
# Demek ki bir hisseyi fazla alıcı olunca o bölgede öyle bir yapı oluşur. Bu mantıkla yola çıktım.' + 'TERA'nın düşüşü fon krizinden; ona
# bakmamak lazım.' ÖNCEDEN YAZILDI (sonuç görülmeden): büyük alıcının görünen izi = KAP raporlu fonların payı (sermayeye oran, rapor yayın
# anıyla, o an bilinen). Sinyaller: K24 iki evre kuralı vs eşli, K18 C1 profil vs eşli; BIST, sinyal 2023-01-01..2025-10-31 (fon verisi
# Ara 2022'den; 12 ay ileri pencere). SORU 1 (çöl -> büyük alıcı): sinyalde pay < %2 iken sonraki 365 günde yayımlanan raporlarda pay >= %5
# (ve >= %2) olma oranı, sinyal vs eşli. SORU 2 (büyük alıcı -> öncesinde çöl): payın ilk kez %5'i geçtiği rapor (önceki bilinen pay < %2)
# olayları; önceki 365 günde K24 / K18 sinyali olma oranı vs aynı tarihte fon girmemiş (±365 gün pay < %2) rastgele 10 hisse. Karar: iki
# soruda da kat >= 1,3 -> 'çöl = büyük alıcının izi' adayı (BIST; ABD fon verisi yok). Fiyat sonuçları fon krizi dışarıda (31.08.2026'da kesik).
FI_K25 = {"esik": 0.05, "esik2": 0.02, "once_en_cok": 0.02, "ufuk_gun": 365, "bas": "2023-01-01", "bit": "2025-10-31",
          "kriz": "2026-08-31", "kontrol": 10, "kat_esik": 1.3}


def fi_k25_pay_tablo(G: pd.DataFrame, oran: pd.DataFrame, dol: pd.DataFrame) -> pd.DataFrame:
    """Hisse x ay raporlu fon payı (fi_k18_fon_pay ile aynı hesap): nominal x bölünme oranı / bugünkü sermaye lotu; bil = o ayın son raporu."""
    M = G.groupby(["kod", "ay"]).agg(nominal=("nominal", "sum"), fon=("fon", "nunique"), bil=("bilinme", "max")).reset_index()
    M = M.merge(oran, on=["kod", "ay"], how="left").merge(dol[["kod", "sermaye_lot"]], on="kod", how="left")
    M["pay"] = M.nominal * M.oran.fillna(1.0) / M.sermaye_lot
    return M.dropna(subset=["pay"]).assign(bil=lambda x: pd.to_datetime(x.bil)).sort_values(["kod", "bil"]).reset_index(drop=True)


def fi_k25_sonra(M: pd.DataFrame, X: pd.DataFrame, E: Dict[str, Any] = FI_K25) -> pd.DataFrame:
    """Soru 1: her sinyal (sembol, tarih) için o an bilinen pay (pay0) ve sonraki ufukta yayımlanan raporlardaki en yüksek pay (pay_max)."""
    gr = {k: g for k, g in M.groupby("kod")}; p0, pm = [], []
    for r in X.itertuples():
        t = pd.Timestamp(r.tarih); g = gr.get(r.sembol)
        p0.append(_fi_k18_pay_an(M if g is None else g, r.sembol, t) if g is not None else 0.0)
        if g is None:
            pm.append(0.0); continue
        w = g[(g.bil > t) & (g.bil <= t + pd.Timedelta(days=E["ufuk_gun"]))]
        pm.append(float(w.pay.max()) if len(w) else 0.0)
    X = X.assign(pay0=p0, pay_max=pm)
    X["giris5"] = (X.pay0 < E["once_en_cok"]) & (X.pay_max >= E["esik"])
    X["giris2"] = (X.pay0 < E["once_en_cok"]) & (X.pay_max >= E["esik2"])
    return X


def fi_k25_girisler(M: pd.DataFrame, E: Dict[str, Any] = FI_K25) -> pd.DataFrame:
    """Soru 2 olayları: payın ilk kez E['esik']'i geçtiği rapor (önceki bilinen pay < E['once_en_cok'] ya da hiç rapor yok)."""
    sat = []
    for k, g in M.groupby("kod"):
        g = g.sort_values("bil"); once = 0.0
        for r in g.itertuples():
            if r.pay >= E["esik"] and once < E["once_en_cok"]:
                sat.append({"sembol": k, "bil": r.bil, "pay": r.pay}); break
            once = r.pay
    return pd.DataFrame(sat)


def fon_izi_k25(G: pd.DataFrame, oran: pd.DataFrame, dol: pd.DataFrame, V: Dict[str, pd.DataFrame], A: Optional[FIAyar] = None,
                tohum: int = 25) -> Dict[str, Any]:
    """K25 sürücü (yalnız BIST). Çıktı k25_soru1.csv, k25_soru2.csv, k25_ozet.csv."""
    A = A or FIAyar(); E = FI_K25; rng = np.random.default_rng(tohum)
    M = fi_k25_pay_tablo(G, oran, dol)
    k24 = pd.read_csv(os.path.join(A.cikti, "k24_olaylar.csv.gz"), parse_dates=["tarih"])
    k24 = k24[k24.pazar == "BIST"].assign(grup=lambda x: np.where(x.kural, "K24 kural", "K24 eşli"))[["sembol", "tarih", "grup"]]
    k18 = pd.read_csv(os.path.join(A.cikti, "k18_olaylar.csv.gz"), parse_dates=["bilgi"], low_memory=False)
    k18 = k18[(k18.pazar == "BIST") & k18.varyant.isin(["C1", "esli"])].rename(columns={"bilgi": "tarih"})
    k18 = k18.assign(grup=np.where(k18.varyant == "C1", "K18 profil", "K18 eşli"))[["sembol", "tarih", "grup"]]
    X = pd.concat([k24, k18], ignore_index=True)
    X = X[(X.tarih >= E["bas"]) & (X.tarih <= E["bit"]) & X.sembol.isin(list(V))]
    S1 = fi_k25_sonra(M, X, E)
    oz = S1.groupby("grup").agg(n=("sembol", "size"), giris5=("giris5", "mean"), giris2=("giris2", "mean"), pay0_med=("pay0", "median"))
    # Soru 2: fon girişi olaylarından önceki 365 günde sinyal var mı (vs aynı tarihte fon girmemiş rastgele hisseler)
    Gi = fi_k25_girisler(M, E); Gi = Gi[(Gi.bil >= pd.Timestamp(E["bas"]) + pd.Timedelta(days=E["ufuk_gun"])) & Gi.sembol.isin(list(V))]
    hep = sorted(V); fon_var = {k: g for k, g in M.groupby("kod")}
    def temiz(k, t):
        g = fon_var.get(k)
        if g is None:
            return True
        w = g[(g.bil >= t - pd.Timedelta(days=E["ufuk_gun"])) & (g.bil <= t + pd.Timedelta(days=E["ufuk_gun"]))]
        return not len(w) or w.pay.max() < E["once_en_cok"]
    sat = []
    for r in Gi.itertuples():
        t = pd.Timestamp(r.bil); kont = [k for k in rng.permutation(hep) if k != r.sembol and len(V[k].loc[:t]) > 250 and temiz(k, t)][:E["kontrol"]]
        for k, tip in [(r.sembol, "fon girişi")] + [(k, "kontrol") for k in kont]:
            Y = X[(X.sembol == k) & (X.tarih < t) & (X.tarih >= t - pd.Timedelta(days=E["ufuk_gun"]))]
            sat.append({"olay": r.sembol, "bil": t, "sembol": k, "tip": tip, **{f"var_{g_}": bool((Y.grup == g_).any()) for g_ in X.grup.unique()}})
    S2 = pd.DataFrame(sat)
    oz2 = S2.groupby("tip")[[c for c in S2.columns if c.startswith("var_")]].mean() if len(S2) else pd.DataFrame()
    S1.to_csv(os.path.join(A.cikti, "k25_soru1.csv"), index=False); S2.to_csv(os.path.join(A.cikti, "k25_soru2.csv"), index=False)
    oz.to_csv(os.path.join(A.cikti, "k25_ozet.csv"))
    return {"M": M, "soru1": S1, "ozet1": oz, "girisler": Gi, "soru2": S2, "ozet2": oz2}


def fi_k12_ders9(V: Dict[str, pd.DataFrame], Zk: pd.DataFrame, Yk: pd.DataFrame, Ek: pd.DataFrame, Pn: pd.DataFrame, yol: str,
                 vaka: Tuple[str, str] = ("MANAS", "2025-07-22"), pencere: Tuple[str, str] = ("2025-07-18", "2025-08-08")) -> int:
    """Ders 9 (Cemal 25 Eki: 'mumları kıyasla, kim yüzde olarak daha çok yol almış'): (1) soru, nasıl ölçüldü, kısa cevap; (2) gün gün
    medyan yol: sinyal vs aynı gün bütün hisseler; (3) sıra (0 = en kötü, 1 = en iyi) gün gün; (4) vaka: MANAS atılımı ve aynı gün bütün
    hisselerin yol bandı; (5) Cemal'in penceresi (çölün son günü -> 15 gün, atılım mumu dahil) ve bekleyen alış emri (K22); (6) neden, karar.
    V = BIST (vaka için); Zk = k21_ozet.csv, Yk = k21_yol.csv, Ek = k22_ozet.csv, Pn = k22_pencere.csv."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    A4 = (8.27, 11.69)
    yz = lambda x: (("−" if x < 0 else "+") + f"%{abs(100 * x):.1f}").replace(".", ",") if x == x else "—"
    sz = lambda x: f"{x:.2f}".replace(".", ",") if x == x else "—"

    def yazi(fig, y, baslik, satirlar, boy=9.4, gen=92):
        if baslik:
            fig.text(0.07, y, baslik, fontsize=14, weight="bold", va="top", color="#1f2a44"); y -= 0.040
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= boy * 0.0022
            y -= 0.004
        return y

    HUC = [("BIST", "2023"), ("BIST", "2024-26"), ("ABD", "2023"), ("ABD", "2024-26")]
    ET = {"cemal": "senin profilin", "nadir": "nadir çöl", "en_siki": "en sıkı çöl"}
    Zi = Zk.set_index(["pazar", "donem", "sinyal"])
    g = lambda p, d, s, k: Zi.loc[(p, d, s), k] if (p, d, s) in Zi.index and k in Zi.columns else np.nan
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        sat = ["Sen: 'Tam çölden çıkan, koşmaya başlayan hisse ile rastgele günde alınan yolun eşit olma ihtimali sıfır. Çıkış kuralını bırak, "
               "mumları kıyasla: kim yüzde olarak daha çok yol almış?' Bu sayfalarda çıkış kuralı YOK, eşleştirme YOK, kura YOK.",
               "Nasıl ölçüldü: her çöl atılımında giriş ertesi gün açılış. Sonra 1., 2., … 120. günün kapanışı girişe göre yüzde kaç? Aynı günü "
               "borsadaki BÜTÜN hisseler için de aynı şekilde hesapladım (aynı giriş günü, aynı açılış). Sonra her gün sordum: senin çöl hissen o "
               "gün bütün hisseler arasında kaçıncı? 0 = en kötü, 0,5 = tam orta, 1 = en iyi. Çöl gerçekten öne geçiyorsa bu sayı 0,5'in "
               "üstüne çıkmalı.",
               "Ayrıca kod hatası aradım: giriş günü hizası (her sinyalde giriş günü hissenin kendi verisinde var mı), bozuk mum (2022 sonrası "
               "%10,5 üstü sıçrama: çoğu 15 Şubat 2023 deprem açılışı, iki grupta da), ortalamayı birkaç uçan hissenin şişirmesi (medyan ayrıca "
               "yazıldı). Hata bulunmadı.", "", "KISA CEVAP"]
        for s_ in ("cemal", "nadir", "en_siki"):
            sat.append(f"- {ET[s_]}: 120. gün sırası " + ", ".join(f"{p} {d} {sz(g(p, d, s_, 'g120_sira'))}"
                                                                for p, d in HUC if g(p, d, s_, "n_yol") == g(p, d, s_, "n_yol"))
                       + f" (n BIST 2024-26 {int(g('BIST', '2024-26', s_, 'n_yol')) if g('BIST', '2024-26', s_, 'n_yol') == g('BIST', '2024-26', s_, 'n_yol') else 0}).")
        sat += [f"- BIST 2024-26 senin profilin: 120. gün medyan yol {yz(g('BIST', '2024-26', 'cemal', 'g120_sinyal_med'))}, aynı gün bütün "
                f"hisselerin medyanı {yz(g('BIST', '2024-26', 'cemal', 'g120_evren_med'))}. Nadir çöl {yz(g('BIST', '2024-26', 'nadir', 'g120_sinyal_med'))} "
                f"vs {yz(g('BIST', '2024-26', 'nadir', 'g120_evren_med'))}.",
                "- Yani çöl atılımından sonra hisse, aynı gün alınabilecek bütün hisseler arasında ORTADA, BIST'te biraz altında. 'Sıfır ihtimal' "
                "dediğin şey veride her gün oluyor: atılım günü 100 çöl hissesinden ~23'ü koşuyor, aynı gün borsadan rastgele 100 hisseden de ~22'si.",
                "- Mum mum geçme şartı (önceden: 60. ve 120. gün sıranın %90 alt sınırı > 0,5, dört hücre): hiçbir çöl tanımı geçmedi.",
                "- SENİN PENCERENDE (çölün son gününden 15 gün, atılım mumu dahil) çöl hissesi borsanın ÜSTÜNDE: sıra "
                f"{sz(Pn.dahil_mean.min())}-{sz(Pn.dahil_mean.max())}. Bu kısımda haklısın. Ama fark atılım mumunun kendisinde: atılım "
                f"kapanışından sonra sıra {sz(Pn.sonra_mean.min())}-{sz(Pn.sonra_mean.max())}. Atılım mumunu tavanda bekleyen emirle almak "
                f"da üstünlük vermiyor (her iki dolumdan biri sahte kırılım; sıra {sz(Ek.g120_sira.min())}-{sz(Ek.g120_sira.max())}). Sayfa 6-7."]
        yazi(fig, 0.96, "DERS 9: SAĞ AYAK MUM MUM — KİM DAHA ÇOK YOL ALDI?", sat)
        pdf.savefig(fig); plt.close(fig)
        for s_ in ("cemal", "nadir"):
            fig = plt.figure(figsize=A4)
            yazi(fig, 0.96, f"GÜN GÜN YOL: {ET[s_].upper()} vs AYNI GÜN BÜTÜN HİSSELER", [
                "Koyu çizgi: çöl hisselerinin girişten bu yana yüzde yolu (medyan), gölge: ortadaki yarısı. Turuncu: aynı gün bütün hisselerin "
                "medyan yolu. İki çizgi üst üste ise çöl, aynı gün rastgele alınan hisseden fazla yol almamış demektir."])
            for k, (p, d) in enumerate(HUC):
                y_ = Yk[(Yk.pazar == p) & (Yk.donem == d) & (Yk.sinyal == s_)]
                ax = fig.add_axes([0.10 + (k % 2) * 0.46, 0.50 - (k // 2) * 0.40, 0.38, 0.30])
                if len(y_):
                    ax.fill_between(y_.gun, 100 * y_.sinyal_q25, 100 * y_.sinyal_q75, color="#1f2a44", alpha=0.15, lw=0)
                    ax.plot(y_.gun, 100 * y_.sinyal_med, color="#1f2a44", lw=2, label="çöl atılımı (medyan)")
                    ax.plot(y_.gun, 100 * y_.evren_med, color="#e0a458", lw=2, label="aynı gün bütün hisseler")
                    ax.set_title(f"{p} {d}  (n {int(g(p, d, s_, 'n_yol'))}, 120. gün sıra {sz(g(p, d, s_, 'g120_sira'))})", fontsize=8.5)
                ax.axhline(0, color="#999", lw=0.8); ax.set_xlabel("girişten sonraki işlem günü", fontsize=8); ax.set_ylabel("yol %", fontsize=8)
                ax.tick_params(labelsize=7)
                if k == 0:
                    ax.legend(fontsize=7, loc="upper left")
            pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "SIRA: ÇÖL HİSSESİ O GÜN BÜTÜN HİSSELER ARASINDA KAÇINCI?", [
            "0,5 çizgisi = tam orta (rastgele). Çöl öne geçseydi çizgiler girişten sonra yükselip 0,6-0,7'ye gitmeliydi. 60. ve 120. günde "
            f"sıra {sz(Zk[Zk.n_yol >= 30][['g60_sira', 'g120_sira']].min().min())} ile {sz(Zk[Zk.n_yol >= 30][['g60_sira', 'g120_sira']].max().max())} "
            "arasında (30'dan az sinyalli hücreler hariç): çöl hissesi aynı gün borsanın ortasında, BIST'te biraz altında."])
        for k, (p, d) in enumerate(HUC):
            ax = fig.add_axes([0.10 + (k % 2) * 0.46, 0.50 - (k // 2) * 0.40, 0.38, 0.30])
            for s_, renk in (("cemal", "#1f2a44"), ("nadir", "#c0392b"), ("en_siki", "#27ae60")):
                y_ = Yk[(Yk.pazar == p) & (Yk.donem == d) & (Yk.sinyal == s_)]
                if len(y_):
                    ax.plot(y_.gun, y_.sira, color=renk, lw=1.6, label=f"{ET[s_]} (n {int(g(p, d, s_, 'n_yol'))})")
            ax.axhline(0.5, color="#e0a458", lw=1.5, ls="--"); ax.set_ylim(0.2, 0.8); ax.set_title(f"{p} {d}", fontsize=9)
            ax.set_xlabel("girişten sonraki işlem günü", fontsize=8); ax.set_ylabel("sıra (0,5 = orta)", fontsize=8); ax.tick_params(labelsize=7)
            ax.legend(fontsize=6.5, loc="upper right")
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        vs, vt = vaka; d0 = V.get(vs)
        yazi(fig, 0.96, f"VAKA: {vs} ATILIMI ({pd.Timestamp(vt):%d.%m.%Y}) vs AYNI GÜN BÜTÜN HİSSELER", [
            f"Senin örneğin. Üstte {vs}'ın mumları (atılım günü dikey çizgi). Altta girişten sonraki yolu (kalın) ve aynı gün alınabilecek bütün "
            "hisselerin yolları (gri bant: ortadaki yarısı, açık bant: %10-%90). Bu vaka koşanlardan; ama çöl hisselerinin çoğu bandın ortasında "
            "kaldı (önceki sayfalar)."])
        if d0 is not None:
            C = pd.DataFrame({s: x.Close for s, x in V.items()}).sort_index(); O = pd.DataFrame({s: x.Open for s, x in V.items()}).reindex(C.index)
            i = int(C.index.searchsorted(pd.Timestamp(vt), side="right")); u = min(120, len(C) - i)
            ax = fig.add_axes([0.10, 0.50, 0.85, 0.30]); w = d0.loc[C.index[max(0, i - 60)]:C.index[i + u - 1]]
            x = np.arange(len(w)); renk = np.where(w.Close >= w.Open, "#27ae60", "#c0392b")
            ax.vlines(x, w.Low, w.High, color=renk, lw=0.7); ax.bar(x, (w.Close - w.Open).abs().clip(lower=1e-9), bottom=np.minimum(w.Open, w.Close), color=renk, width=0.7)
            j0 = int(np.flatnonzero(w.index == C.index[i - 1])[0]) if (w.index == C.index[i - 1]).any() else 0
            ax.axvline(j0, color="#1f2a44", ls="--", lw=1); ax.set_xticks(x[::20]); ax.set_xticklabels([f"{t:%d.%m.%y}" for t in w.index[::20]], fontsize=7)
            ax.set_ylabel("fiyat", fontsize=8); ax.set_title(f"{vs} günlük mumlar (atılım = kesikli çizgi)", fontsize=9)
            with np.errstate(divide="ignore", invalid="ignore"):
                Yv = C.iloc[i:i + u].to_numpy(float) / O.iloc[i].to_numpy(float) - 1
            ax2 = fig.add_axes([0.10, 0.07, 0.85, 0.33]); gg = np.arange(1, u + 1)
            q = np.nanpercentile(Yv, [10, 25, 50, 75, 90], axis=1)
            ax2.fill_between(gg, 100 * q[0], 100 * q[4], color="#bbb", alpha=0.35, lw=0, label="bütün hisseler %10-%90")
            ax2.fill_between(gg, 100 * q[1], 100 * q[3], color="#888", alpha=0.45, lw=0, label="bütün hisseler ortadaki yarı")
            ax2.plot(gg, 100 * q[2], color="#e0a458", lw=1.8, label="bütün hisseler medyan")
            pv = C[vs].iloc[i:i + u].to_numpy(float) / O[vs].iloc[i] - 1
            ax2.plot(gg, 100 * pv, color="#1f2a44", lw=2.2, label=vs)
            sira = np.nanmean(Yv < pv[:, None], axis=1)
            ax2.set_title(f"girişten sonraki yol: {vs} 60. gün {yz(pv[min(59, u - 1)])} (sıra {sz(sira[min(59, u - 1)])}), "
                          f"120. gün {yz(pv[u - 1])} (sıra {sz(sira[u - 1])})", fontsize=8.5)
            ax2.set_yscale("symlog", linthresh=50); ax2.axhline(0, color="#999", lw=0.8)
            ax2.set_xlabel("girişten sonraki işlem günü", fontsize=8); ax2.set_ylabel("yol % (ölçek sıkıştırılmış)", fontsize=8); ax2.legend(fontsize=7, loc="upper left")
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        Pi = Pn.set_index(["pazar", "donem", "sinyal"]); Ei = Ek.set_index(["pazar", "donem", "sinyal"])
        tra = lambda x: f"{pd.Timestamp(x).day} " + ("Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık".split()[pd.Timestamp(x).month - 1])
        pg = lambda T_, p, d, s_, k: T_.loc[(p, d, s_), k] if (p, d, s_) in T_.index and k in T_.columns else np.nan
        C = pd.DataFrame({s: x.Close for s, x in V.items()}).sort_index()
        a, b = C.index.searchsorted(pd.Timestamp(pencere[0])), C.index.searchsorted(pd.Timestamp(pencere[1]))
        yv = (C.iloc[b] / C.iloc[a] - 1).dropna(); pv_ = yv.get(vs, np.nan); yo = yv.drop(vs, errors="ignore")
        y = yazi(fig, 0.96, f"SENİN PENCEREN: {vs} {pd.Timestamp(pencere[0]):%d.%m} – {pd.Timestamp(pencere[1]):%d.%m.%Y}", [
            f"Sen: '{vs} Haziran-Temmuz çöl mumlarını bulup dip oluştu dediğimiz an; adil ölçmeni istediğim {tra(pencere[0])} – "
            f"{tra(pencere[1])}, çölün sağ ayağı.' Bu pencere {b - a} işlem günü; çölün son gününden başlıyor, atılım mumunu da içine alıyor.",
            f"- {vs} bu pencerede {yz(pv_)}; aynı pencerede bütün hisselerin medyanı {yz(float(yo.median()))}. {len(yo)} hissenin "
            f"{int((yo > pv_).sum())}'i daha çok gitti (sıra {sz(float((yo < pv_).mean()))}). Senin vakan gerçekten en iyi %1'de.",
            "- Aynı pencere tanımı (çölün son günü kapanışından 15 işlem günü), kodun bulduğu BÜTÜN çöl atılımlarında:"]
            +
            [f"- {'profilin' if s_ == 'profil' else 'nadir çöl'} {p} {d} (n {int(pg(Pi, p, d, s_, 'n'))}): atılım mumu DAHİL sıra "
             f"{sz(pg(Pi, p, d, s_, 'dahil_mean'))} (medyan {yz(pg(Pi, p, d, s_, 'dahil_median'))} vs bütün hisseler {yz(pg(Pi, p, d, s_, 'dahil_evren'))}); "
             f"atılım kapanışından sonra sıra {sz(pg(Pi, p, d, s_, 'sonra_mean'))}"
             for s_ in ("profil", "nadir") for p, d in HUC if (p, d, s_) in Pi.index]
            + ["- BU KISIMDA HAKLISIN: senin pencerende çöl hissesi borsanın üstünde (sıra 0,5'in üstü). Ama farkın tamamı ATILIM MUMUNDA: "
               "atılım kapanışından sonra sıra yine ~0,5. Atılım mumu 'çöl bitti' dediğimiz mumun kendisi; kapanışta yukarıda kaldığını ancak "
               "kapanışta biliyorsun."], boy=8.6)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "ATILIM MUMUNU ALMANIN TEK YOLU: TAVANDA BEKLEYEN ALIŞ EMRİ (K22)", [
            "Kural (önceden yazıldı): çöl kutusu dün bitti; emir kutu tavanının (ve son 20 günün tepesinin) %0,2 üstünde bekler; fiyat değerse "
            "dolar. Kapanış geri kutuya dönse de işlem sayılır (gerçekte öyle olur). Karar: 60. ve 120. gün sırası %90 alt sınırı > 0,5, dört hücre."]
            + [f"- {'profilin' if s_ == 'profil' else 'nadir çöl'} {p} {d}: n {int(pg(Ei, p, d, s_, 'n'))}, sahte kırılım (kapanış kutuya döndü) "
               f"{yz(pg(Ei, p, d, s_, 'sahte'))}; sıra 15. gün {sz(pg(Ei, p, d, s_, 'g15_sira'))}, 60. gün {sz(pg(Ei, p, d, s_, 'g60_sira'))}, "
               f"120. gün {sz(pg(Ei, p, d, s_, 'g120_sira'))}" for s_ in ("profil", "nadir") for p, d in HUC if (p, d, s_) in Ei.index]
            + [f"- Sonuç: {'hiçbir hücre geçmedi' if not Ek.emir_ustun.any() else str(int(Ek.emir_ustun.sum())) + ' hücre geçti, dört hücre değil'}. "
               "Tavanda bekleyen emir atılımı yakalıyor ama sahte kırılımları da alıyor (her iki dolumdan biri). İkisi toplanınca yine borsanın ortası."])
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "NEDEN GÖZÜN 'İMKÂNSIZ' DİYOR — VE SENİN KARARIN", [
            "- 'Tam çölden çıkan, koşmaya başlayan hisse' cümlesi sonucu içeriyor: 'koşmaya başlayan' ancak sonradan bilinir. Atılım günü elimizde "
            "yalnız şekil var; o gün aynı şekle sahip 100 hisseden ~23'ü koşuyor, ~50'si geri kutuya ya da altına dönüyor (VSNMD, PAPIL gibi).",
            "- Grafikte hatırladığın ve gördüğün çöller koşanlar; koşmayan aynı şekiller ekrandan düşüyor, akılda kalmıyor. Mum mum ölçünce "
            "koşanlar ile dönenler toplanıyor ve ortaya borsanın ortası çıkıyor.",
            "- Atılım GÜNÜNÜN kendisi (+%4-5) çöl hissesinde büyük, ama o mum zaten 'atılım' tanımı; kapanışta görüp ertesi gün alan onu kazanamaz. "
            "Ertesi günden sonra fark kalmıyor.",
            "- Bu, çöllerin olmadığı ya da gözünün yanlış gördüğü demek değil: şekli doğru görüyorsun, kod da buluyor. Söylenen şu: şekil, "
            "o gün başka bir hisseyi almaktan daha çok yol vermiyor. Kazancı belirleyen piyasanın yönü ve büyük kazananı erken satmamak.",
            "",
            "Karar gereken (senin):",
            "- Sistemin amacı: büyük kazananı tutmak (tut / gevşek trail) mı, derin kaybı sınırlamak (mevcut stop + trail) mı? (Ders 8)",
            "- Üretim değişmedi. Değişiklik 'yaz' kararı.",
            "",
            "Sıradaki (önceden yazılı): aynı mum mum kıyas üretim D13 + T6/T10 zinciri ve 2016-22 ayı dönemi için; ve çöl + KATALİZÖR (sektör "
            "rüzgârı ya da KAP haberi aynı hafta) birlikteyken sıra 0,5'in üstüne çıkıyor mu (CLAUDE.md: 'rüzgâr ya da katalizör olmadan çöl "
            "aranmaz')."])
        pdf.savefig(fig); plt.close(fig)
    return 8


# KÖR SET v2 (Cemal 25 Eki: 'birebir benzerini ver, kodun en iyi puanladığını; hisse adı ve sonraki mumlar olmasın; ben benzer ya da değil
# diyeceğim, kaçtan kaçı yukarı çıkmış' + '1. evre düşüş (yapı dipte olsun), 2. evre çöl mumları: dip oluşmuş, yatay, çok net küçük mum, eğim
# yukarı ya da yatay; 3. evre sağ ayak: kod bilmeyecek, yalnız test için'). ÖNCEDEN YAZILDI: aday havuzu BIST 2016-26 bütün pencereleri, sert
# süzgeç düşüş <= -%30 ve eğim >= -0,001 (bar başı; bölge boyunca ~-%2); ölçek havuzun medyan/IQR'si; her örneğe en yakın 16 (aynı hissede 60
# barda tek, örneğin kendisi ±180 gün hariç, Cemal'in daha önce gördüğü 8 bölge hariç); grafikte bölgeden önceki 40 bar + bölge, bölge sonunda
# kesik. Değerlendirme: Cemal'in ✓'lerinin 60 gün ±%15 yukarı oranı vs ✗'ler vs aynı süzgeçten geçen bütün pencereler; ✓ >= 1,3 x süzgeç
# tabanı ise 'göz izi adayı' -> 16 ölçünün ✓/✗ ayrımı (AUC) -> Cemal ağırlıklı benzerlik ABD'de ve görülmemiş dönemde (dört hücre).
FI_K23_KOR = {"k": 16, "dusus": -0.30, "egim": -0.001, "once": 40}


def fi_k23_en_benzer(V: Dict[str, pd.DataFrame], h0: pd.Series, k: int, haric: Tuple[Tuple[str, str], ...] = (),
                     E: Dict[str, Any] = FI_K23, K: Dict[str, Any] = FI_K23_KOR) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Bir örnek bölgeye (h0: parmak izi + L + sembol + son) BIST havuzunda sert süzgeçten geçen en yakın k pencere ve süzgeçli havuz."""
    L = int(h0["L"]); parca = []
    for s, d in V.items():
        try:
            F = fi_k23_parmak(d, L)
            if len(F):
                parca.append(F.assign(sembol=s))
        except Exception as ex:   # tek hisse bozuksa digerleri devam eder
            filog.warning("K23 kor %s atlandi: %s", s, ex)
    P = pd.concat(parca).rename_axis("tarih").reset_index().dropna(subset=list(E["olcu"]))
    P = P[(P.dusus <= K["dusus"]) & (P.egim >= K["egim"])]
    P = P[~((P.sembol == h0["sembol"]) & ((P.tarih - pd.Timestamp(h0["son"])).abs() <= pd.Timedelta(days=180)))]
    hx = {(s, pd.Timestamp(t)) for s, t in haric}
    if hx:
        P = P[[(r.sembol, r.tarih) not in hx for r in P.itertuples()]]
    P = P.reset_index(drop=True)
    return fi_k23_esle(P, h0, {**E, "k": k}), P


def fi_k23_kor_pdf(V: Dict[str, pd.DataFrame], H: Dict[str, pd.Series], yol: str, anahtar: str, tohum: int = 23,
                   haric: Tuple[Tuple[str, str], ...] = (), K: Dict[str, Any] = FI_K23_KOR) -> pd.DataFrame:
    """Kör set v2: her örnek (H: bölge adı -> parmak izi) için en benzer K['k'] bölge, numaralı, adsız, sonu kesik; örnek grafiği bölümün
    başında. Anahtar CSV: no, bölge, sembol, tarih, uzaklık, sonuç (yon60, yon20) ve süzgeçli havuz tabanı."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    rng = np.random.default_rng(tohum); parca = []; no = 1

    def ciz(ax, d, t, L, baslik, renk="#1f2a44"):
        m = d.Close.rolling(20).mean(); sd = d.Close.rolling(20).std()
        i = d.index.get_loc(t); w = d.iloc[max(0, i - L - K["once"]):i + 1]; mm, ss = m.loc[w.index], sd.loc[w.index]
        x = np.arange(len(w)); r = np.where(w.Close >= w.Open, "#27ae60", "#c0392b")
        ax.vlines(x, w.Low, w.High, color=r, lw=0.7)
        ax.bar(x, (w.Close - w.Open).abs().clip(lower=1e-9), bottom=np.minimum(w.Open, w.Close), color=r, width=0.7)
        ax.plot(x, mm, color="#e67e22", lw=1.3); ax.plot(x, mm + 2 * ss, color="#3498db", lw=0.8); ax.plot(x, mm - 2 * ss, color="#3498db", lw=0.8)
        ax.axvspan(len(w) - L - 0.5, len(w) - 0.5, color="#999", alpha=0.18); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(baslik, fontsize=13, weight="bold", loc="left", color=renk)

    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.text(0.07, 0.95, "KÖR SET: SENİN ÇÖLÜNE BENZİYOR MU?", fontsize=15, weight="bold", va="top", color="#1f2a44")
        for k_, s_ in enumerate(["Kodun en yüksek puan verdiği benzer bölgeler. Her bölümde önce SENİN örneğin, sonra 16 aday.",
                                 "Grafik çölün bittiği gün KESİK: sağ ayak, hisse adı, tarih yok. Gri = çöl; solundaki düşüş = 1. evre.",
                                 "Süzgeç (senin tarifin): öncesinde en az -%30 düşüş, çölde eğim yatay ya da yukarı. Sıra karışık.",
                                 "Cevap tek satır: '✓: 3, 7, 12 …' (yazmadıkların ✗). Sonra kaçının yukarı gittiğini açarım.",
                                 "Bölüm A = MANAS Haz-Tem 2025 · Bölüm B = MANAS Eki-Kas 2025 · Bölüm C = BINBN Ara 2024-Oca 2025."]):
            fig.text(0.07, 0.90 - k_ * 0.024, s_, fontsize=9.5, va="top")
        pdf.savefig(fig); plt.close(fig)
        for harf, b in zip("ABC", ("1", "2", "3")):
            h0 = H[b]; M, P = fi_k23_en_benzer(V, h0, K["k"], haric, K=K)
            M = M.sample(frac=1, random_state=int(rng.integers(1e9))).reset_index(drop=True)
            M["no"] = np.arange(no, no + len(M)); no += len(M)
            M["bolum"] = harf; M["bolge"] = b; M["havuz_n"] = len(P)
            M["havuz_yukari"] = float((P.yon60 == 1).sum() / P.yon60.notna().sum()) if P.yon60.notna().any() else np.nan
            parca.append(M); L = int(h0["L"])
            gruplar = [M.iloc[0:4]] + [M.iloc[j:j + 6] for j in range(4, len(M), 6)]   # 1. sayfa: örnek + 4 aday, sonra 6'şar
            for gi, sat in enumerate(gruplar):
                if not len(sat):
                    continue
                fig = plt.figure(figsize=(8.27, 11.69))
                if gi == 0:
                    ciz(fig.add_axes([0.08, 0.66, 0.86, 0.28]), V[h0["sembol"]], pd.Timestamp(h0["son"]), L, f"BÖLÜM {harf} — SENİN ÖRNEĞİN",
                        "#c0392b")
                    yer = [(0.06, 0.34), (0.53, 0.34), (0.06, 0.04), (0.53, 0.04)]
                else:
                    yer = [(0.06 + (j % 2) * 0.47, 0.69 - (j // 2) * 0.32) for j in range(6)]
                for (x0, y0), r in zip(yer, sat.itertuples()):
                    ciz(fig.add_axes([x0, y0, 0.42, 0.26]), V[r.sembol], pd.Timestamp(r.tarih), L, f"{harf}{r.no}")
                pdf.savefig(fig); plt.close(fig)
    A = pd.concat(parca, ignore_index=True)
    A[["no", "bolum", "bolge", "sembol", "tarih", "uzak", "yon60", "yon20", "havuz_n", "havuz_yukari"]].to_csv(anahtar, index=False)
    return A


# KÖR SET v3 NET GRAFİK (Cemal 26 Eki: 'sendeki grafiklerde mumun yapısı neredeyse görünmüyor; gerçek grafikte başka değerlendirirdim'
# + aracı kurum uygulamasının günlük grafiği). Adaylar, numaralar ve anahtar v2 ile AYNI (k23_kor_anahtar.csv); yalnız çizim değişir:
# sayfa başına 2 grafik, tam genişlik, bölgeden önce K_NET['once'] mum, kalın gövde + fitil, hacim alt panelde, Bollinger yok, SMA20
# ince (1. evre / 2. evre için), çöl açık gri zemin. Hisse adı, tarih, eksen rakamı ve sağ ayak yine yok.
FI_K23_KOR_NET = {"once": 20, "sayfa_grafik": 2, "yesil": "#26a69a", "kirmizi": "#ef5350", "sma": "#e57373"}


def fi_k23_kor_ciz_net(ax, axh, d: pd.DataFrame, t: pd.Timestamp, L: int, K: Dict[str, Any] = FI_K23_KOR_NET) -> None:
    """Uygulama görünümlü mum grafiği: bölge (t'de biten L mum) + öncesinde K['once'] mum; alt eksende hacim."""
    m = d.Close.rolling(20).mean()
    i = int(d.index.get_loc(pd.Timestamp(t))); w = d.iloc[max(0, i - L - K["once"] + 1):i + 1]
    x = np.arange(len(w)); yuk = (w.Close >= w.Open).to_numpy(); r = np.where(yuk, K["yesil"], K["kirmizi"])
    ax.vlines(x, w.Low, w.High, color=r, lw=1.1, zorder=2)
    govde = (w.Close - w.Open).abs().to_numpy(); asgari = 0.0015 * float(w.Close.median())   # doji görünür kalsın
    ax.bar(x, np.maximum(govde, asgari), bottom=np.minimum(w.Open, w.Close) - np.where(govde < asgari, asgari / 2, 0),
           color=r, width=0.62, zorder=3, linewidth=0)
    ax.plot(x, m.loc[w.index].to_numpy(), color=K["sma"], lw=0.9, alpha=0.8, zorder=1)
    ax.axvspan(len(w) - L - 0.5, len(w) - 0.5, color="#9e9e9e", alpha=0.10, zorder=0)
    alt, ust = float(w.Low.min()), float(w.High.max()); pay = (ust - alt) * 0.06
    ax.set_ylim(alt - pay, ust + pay); ax.set_xlim(-0.8, len(w) - 0.2)
    axh.bar(x, w.Volume.to_numpy(float), color=r, alpha=0.45, width=0.62, linewidth=0)
    axh.set_xlim(-0.8, len(w) - 0.2)
    for a in (ax, axh):
        a.set_xticks([]); a.set_yticks([])
        for s in a.spines.values():
            s.set_visible(False)


def fi_k23_kor_pdf_net(V: Dict[str, pd.DataFrame], anahtar: pd.DataFrame, Hk: pd.DataFrame, yol: str,
                       K: Dict[str, Any] = FI_K23_KOR_NET) -> int:
    """Kör set v3: v2 anahtarındaki 48 aday aynı numarayla, sayfa başına 2 net grafik; her bölüm senin örneğinle açılır. Sayfa sayısı döner."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    Hk = Hk.set_index("Unnamed: 0") if "Unnamed: 0" in Hk.columns else Hk
    Hk.index = Hk.index.astype(str)
    A = anahtar.assign(bolge=anahtar.bolge.astype(str), tarih=pd.to_datetime(anahtar.tarih)).sort_values("no")
    eksik = sorted(set(A.sembol) - set(V)) + sorted({str(Hk.loc[b, "sembol"]) for b in A.bolge.unique()} - set(V))
    if eksik:
        raise KeyError(f"K23 kor net: veride olmayan sembol {eksik}")
    sayfa = 0

    def kutu(fig, y0, h, d, t, L, baslik, renk):
        ax = fig.add_axes([0.05, y0 + h * 0.22, 0.90, h * 0.70]); axh = fig.add_axes([0.05, y0, 0.90, h * 0.18])
        fi_k23_kor_ciz_net(ax, axh, d, t, L, K)
        ax.set_title(baslik, fontsize=15, weight="bold", loc="left", color=renk)

    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.text(0.07, 0.95, "KÖR SET v3 — NET MUMLAR", fontsize=16, weight="bold", va="top", color="#1f2a44")
        for k_, s_ in enumerate(["Aynı 48 aday, aynı numaralar; yalnız çizim senin uygulamandaki gibi: büyük mum, fitil, altta hacim.",
                                 f"Her grafik: çölden önce {K['once']} mum + gri zemin = çöl. Çöl bittiği gün KESİK (sağ ayak yok).",
                                 "Bollinger kaldırıldı. İnce kırmızı çizgi = SMA20 (1. evre altında, 2. evre üstünde dizilme).",
                                 "Hisse adı, tarih, fiyat rakamı yok. Her bölüm önce SENİN örneğinle başlar.",
                                 "Cevap: '✓: 3, 7, 12 …' (yazmadıkların ✗). Önceki 20 işaretin yerine bu set geçer.",
                                 "Kural yine önceden yazılı: kutu tepesi ×1,002 bekleyen alış, 60 gün önce +%15 / −%15, 250 gün 2 kat."]):
            fig.text(0.07, 0.90 - k_ * 0.026, s_, fontsize=10, va="top")
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        for harf, b in (("A", "1"), ("B", "2"), ("C", "3")):
            if b not in set(A.bolge):
                continue
            h0 = Hk.loc[b]; L = int(float(h0["L"]))
            ogeler = [("ornek", str(h0["sembol"]), pd.Timestamp(h0["son"]))] + \
                     [(int(r.no), r.sembol, r.tarih) for r in A[A.bolge == b].itertuples()]
            n = K["sayfa_grafik"]
            for j in range(0, len(ogeler), n):
                fig = plt.figure(figsize=(8.27, 11.69))
                for q, (no, s, t) in enumerate(ogeler[j:j + n]):
                    y0 = 0.53 - q * 0.49
                    if no == "ornek":
                        kutu(fig, y0, 0.42, V[s], t, L, f"BÖLÜM {harf} — SENİN ÖRNEĞİN", "#c0392b")
                    else:
                        kutu(fig, y0, 0.42, V[s], t, L, f"{harf}{no}", "#1f2a44")
                pdf.savefig(fig); plt.close(fig); sayfa += 1
    return sayfa

# KÖR SET v4 — KUTU + ALIŞ MUMU + GERİ ZUM (Cemal 26 Eki: 'geriye zum, ilerisi olmadan; veriyi görmüyorum' + 'kutu yeşil mumla geçiliyor
# mu bilmiyorum; alış mumu varsa kutu çizilsin, yoksa çöl mumları yeterli değil'). ÖNCEDEN YAZILDI (işaretler görülmeden):
#   kutu = bölgenin (t'de biten L mum) en yüksek High'ı / en düşük Low'u; ALIŞ MUMU = bölge bittikten sonraki K['alis_gun'] işlem gününde
#   kapanışı kutu tepesinin üstünde olan İLK YEŞİL mum (kapanış > açılış). Alış mumu yoksa aday yok (Cemal: çöl mumları yeterli değil).
#   Grafik alış mumunun kapanışında KESİK (sonrası gizli): üstte 1 yıl geri zum, altta yakın görünüm (bölgeden önce 20 mum -> alış mumu).
#   Adaylar: her örneğe süzgeçli BIST havuzunda (düşüş <= -%30, eğim yatay/yukarı) en yakın bölgelerden, alış mumu olan ve sonucu ölçülebilen
#   (giriş + 60 gün fon krizi 31.08.2026'dan önce) ilk K['k']'si. Giriş = alış mumundan sonraki gün açılış (yan ölçü: alış mumu kapanışı).
#   Sonuç: 60 günde önce +%15 / önce -%15 / yatay, 250 günde 2 kat (krizde kesik). Kıyas: ✓ vs ✗ vs havuzdan aynı şartı (alış mumu var)
#   taşıyan K['havuz_n'] rastgele bölge. Karar: ✓ yukarı oranı hem ✗'nin hem havuzun >= 1,3 katı -> 'göz izi adayı'.
FI_K23_KOR4 = {"k": 16, "aday_k": 400, "alis_gun": 60, "ufuk": 60, "esik": 0.15, "uzun": 250, "kriz": "2026-08-31", "havuz_n": 2000,
               "havuz_dene": 12000, "kat_esik": 1.3, "genis": 250, "yakin_once": 20, "tohum": 24}


def fi_k23_alis_mumu(d: pd.DataFrame, t: pd.Timestamp, L: int, K: Dict[str, Any] = FI_K23_KOR4) -> Dict[str, Any]:
    """Bölge (t'de biten L mum) kutusu, alış mumu (kutu tepesi üstünde kapanan ilk yeşil mum) ve ertesi açılış girişinin sonucu."""
    i = int(d.index.get_loc(pd.Timestamp(t))); o = d.Open.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float)
    c = d.Close.to_numpy(float); son = int(d.index.searchsorted(pd.Timestamp(K["kriz"]), side="right"))
    ust, alt = float(h[i - L + 1:i + 1].max()), float(l[i - L + 1:i + 1].min())
    out: Dict[str, Any] = {"kutu_ust": ust, "kutu_alt": alt, "alis": False, "alis_i": np.nan, "olculur": False,
                           "y60": np.nan, "x2": np.nan, "y60_kap": np.nan}
    j = next((k for k in range(i + 1, min(i + 1 + K["alis_gun"], son)) if c[k] > ust and c[k] > o[k]), None)
    if j is None:
        return out
    out.update({"alis": True, "alis_i": j, "alis_tarih": d.index[j], "olculur": j + 1 + K["ufuk"] <= son})
    def yon(g: float, k0: int) -> float:
        u = min(k0 + K["ufuk"], son)
        if u - k0 < 20:
            return np.nan
        a = np.flatnonzero(h[k0:u] >= g * (1 + K["esik"])); b = np.flatnonzero(l[k0:u] <= g * (1 - K["esik"]))
        a0, b0 = (a[0] if len(a) else 10 ** 9), (b[0] if len(b) else 10 ** 9)
        return 1.0 if a0 < b0 else (-1.0 if b0 < 10 ** 9 else 0.0)
    if j + 1 < son:
        g = o[j + 1]; out["y60"] = yon(g, j + 1)
        w = h[j + 1:min(j + 1 + K["uzun"], son)]
        out["x2"] = float(w.max() >= 2 * g) if len(w) >= 60 else np.nan
    out["y60_kap"] = yon(c[j], j + 1)
    return out


def fi_k23_kor4_sec(V: Dict[str, pd.DataFrame], h0: pd.Series, K: Dict[str, Any] = FI_K23_KOR4,
                    haric: Tuple[Tuple[str, str], ...] = ()) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Bir örneğe en yakın bölgelerden alış mumu olan ve ölçülebilen ilk K['k'] aday + aynı şartı taşıyan rastgele havuz örneği."""
    L = int(float(h0["L"])); M, P = fi_k23_en_benzer(V, h0, K["aday_k"], haric)
    def ekle(X: pd.DataFrame, n: int) -> pd.DataFrame:
        sat = []
        for r in X.itertuples():
            try:
                R = fi_k23_alis_mumu(V[r.sembol], r.tarih, L, K)
            except Exception as ex:   # tek pencere bozuksa digerleri devam eder
                filog.warning("K23 kor4 %s %s atlandi: %s", r.sembol, r.tarih, ex); continue
            if R["alis"] and R["olculur"]:
                sat.append({"sembol": r.sembol, "tarih": r.tarih, "uzak": getattr(r, "uzak", np.nan), **R})
                if len(sat) >= n:
                    break
        return pd.DataFrame(sat)
    A = ekle(M, K["k"])
    if len(A) < K["k"]:
        filog.warning("K23 kor4 bolge L=%d: alis mumlu aday %d < %d", L, len(A), K["k"])
    H = ekle(P.sample(min(K["havuz_dene"], len(P)), random_state=K["tohum"]), K["havuz_n"])
    return A, H


def fi_k23_kor4_ciz(ax, axh, d: pd.DataFrame, i0: int, j: int, b0: int, b1: int, ust: float, alt: float, ince: bool,
                    K: Dict[str, Any] = FI_K23_KOR_NET) -> None:
    """i0..j aralığını mum olarak çizer (j = alış mumu, son mum); kutu [b0, b1] x [alt, ust] çerçeve, alış mumu işaretli."""
    from matplotlib.patches import Rectangle
    w = d.iloc[i0:j + 1]; x = np.arange(len(w)); r = np.where((w.Close >= w.Open).to_numpy(), K["yesil"], K["kirmizi"])
    ax.vlines(x, w.Low, w.High, color=r, lw=0.6 if ince else 1.1, zorder=2)
    govde = (w.Close - w.Open).abs().to_numpy(); asgari = 0.0015 * float(w.Close.median())
    ax.bar(x, np.maximum(govde, asgari), bottom=np.minimum(w.Open, w.Close) - np.where(govde < asgari, asgari / 2, 0),
           color=r, width=0.7 if ince else 0.62, zorder=3, linewidth=0)
    if not ince:
        ax.plot(x, d.Close.rolling(20).mean().iloc[i0:j + 1].to_numpy(), color=K["sma"], lw=0.9, alpha=0.8, zorder=1)
    ax.add_patch(Rectangle((b0 - i0 - 0.5, alt), b1 - b0 + 1, ust - alt, fill=True, facecolor="#9e9e9e", alpha=0.12,
                           edgecolor="#5d4037", lw=1.4, zorder=1))
    ax.hlines(ust, b1 - i0 + 0.5, len(w) - 0.5, colors="#5d4037", linestyles="--", lw=0.9, zorder=1)
    lo, hi = float(w.Low.min()), float(w.High.max()); pay = (hi - lo) * 0.07
    ax.set_ylim(lo - pay, hi + pay); ax.set_xlim(-0.8, len(w) - 0.2)
    ax.annotate("alış mumu", (len(w) - 1, float(w.Low.iloc[-1])), xytext=(len(w) - 1, lo - pay * 0.2), ha="right", va="top",
                fontsize=8 if ince else 10, color="#1565c0", weight="bold", arrowprops={"arrowstyle": "->", "color": "#1565c0"})
    if axh is not None:
        axh.bar(x, w.Volume.to_numpy(float), color=r, alpha=0.45, width=0.62, linewidth=0); axh.set_xlim(-0.8, len(w) - 0.2)
    for a in (ax, axh):
        if a is None:
            continue
        a.set_xticks([]); a.set_yticks([])
        for s in a.spines.values():
            s.set_visible(False)


def fi_k23_kor4_pdf(V: Dict[str, pd.DataFrame], Hk: pd.DataFrame, yol: str, anahtar: str, havuz_yol: str,
                    K: Dict[str, Any] = FI_K23_KOR4, haric: Tuple[Tuple[str, str], ...] = ()) -> pd.DataFrame:
    """Kör set v4: bölüm başına örnek + K['k'] aday, sayfa başına bir aday (üstte 1 yıl geri zum, altta yakın + hacim), alış mumunda kesik.
    Anahtar (sonuçlar gizli) ve havuz CSV'si yazılır."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    Hk = Hk.set_index("Unnamed: 0") if "Unnamed: 0" in Hk.columns else Hk
    Hk.index = Hk.index.astype(str); rng = np.random.default_rng(K["tohum"]); parca, havuz, no = [], [], 1

    def sayfa(pdf, d, t, L, baslik, renk, alt_yazi):
        i = int(d.index.get_loc(pd.Timestamp(t))); b0 = i - L + 1; R = fi_k23_alis_mumu(d, t, L, K)
        fig = plt.figure(figsize=(8.27, 11.69)); fig.text(0.05, 0.965, baslik, fontsize=17, weight="bold", color=renk, va="top")
        if not R["alis"]:
            fig.text(0.05, 0.92, "60 gün içinde alış mumu gelmedi -> işlem yok", fontsize=11, va="top")
            pdf.savefig(fig); plt.close(fig); return
        j = int(R["alis_i"]); fig.text(0.05, 0.935, alt_yazi.format(n=j - i), fontsize=9.5, va="top", color="#555")
        ax1 = fig.add_axes([0.05, 0.62, 0.90, 0.27]); ax1.set_title("1 YIL GERİ (kutu çerçeveli)", fontsize=10, loc="left", color="#555")
        fi_k23_kor4_ciz(ax1, None, d, max(0, j - K["genis"] + 1), j, b0, i, R["kutu_ust"], R["kutu_alt"], True)
        ax2 = fig.add_axes([0.05, 0.17, 0.90, 0.39]); axh = fig.add_axes([0.05, 0.05, 0.90, 0.10])
        ax2.set_title("YAKIN: çölden önce 20 mum -> kutu -> alış mumu", fontsize=10, loc="left", color="#555")
        fi_k23_kor4_ciz(ax2, axh, d, max(0, b0 - K["yakin_once"]), j, b0, i, R["kutu_ust"], R["kutu_alt"], False)
        pdf.savefig(fig); plt.close(fig)

    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.text(0.07, 0.95, "KÖR SET v4 — KUTU + ALIŞ MUMU", fontsize=16, weight="bold", va="top", color="#1f2a44")
        for k_, s_ in enumerate(["Her sayfa bir aday. Üstte 1 yıl geri zum (düşüşü görürsün), altta yakın görünüm + hacim.",
                                 "Kahverengi çerçeve = kutu (çöl bölgesinin en yükseği / en düşüğü). Kesikli çizgi = kutu tepesi.",
                                 "Yalnız ALIŞ MUMU gelen adaylar var: kutu tepesinin üstünde kapanan ilk yeşil mum (60 gün içinde).",
                                 "Grafik alış mumunun kapanışında KESİK: sonrası, hisse adı, tarih, fiyat yok.",
                                 "Soru: 'Bu çöl + bu alış mumu, ben alırdım' mı? Cevap: '✓: 3, 7, 12 …' (yazmadıkların ✗).",
                                 "Ölçü önceden yazılı: giriş alış mumundan sonraki gün açılış; 60 günde önce +%15 mi −%15 mi; 250 günde 2 kat.",
                                 "Bu set v3'ün yerine geçer (v3 işaretlenmedi). Her bölüm senin örneğinle açılır."]):
            fig.text(0.07, 0.90 - k_ * 0.026, s_, fontsize=10, va="top")
        pdf.savefig(fig); plt.close(fig)
        for harf, b, ad in (("A", "1", "MANAS Haz-Tem 2025"), ("B", "2", "MANAS Eki-Kas 2025"), ("C", "3", "BINBN Ara 2024-Oca 2025")):
            h0 = Hk.loc[b]; L = int(float(h0["L"]))
            S, P = fi_k23_kor4_sec(V, h0, K, haric)
            S = S.sample(frac=1, random_state=int(rng.integers(1e9))).reset_index(drop=True)
            S["no"] = np.arange(no, no + len(S)); no += len(S); S["bolum"] = harf; S["bolge"] = b; parca.append(S)
            havuz.append(P.assign(bolge=b))
            sayfa(pdf, V[str(h0["sembol"])], pd.Timestamp(h0["son"]), L, f"BÖLÜM {harf} — SENİN ÖRNEĞİN ({ad})", "#c0392b",
                  f"Kutu {L} mum; alış mumu kutu bittikten {{n}} mum sonra.")
            for r in S.itertuples():
                sayfa(pdf, V[r.sembol], r.tarih, L, f"{harf}{r.no}", "#1f2a44", f"Kutu {L} mum; alış mumu kutu bittikten {{n}} mum sonra.")
    A = pd.concat(parca, ignore_index=True); Hv = pd.concat(havuz, ignore_index=True)
    A[["no", "bolum", "bolge", "sembol", "tarih", "uzak", "kutu_ust", "kutu_alt", "alis_tarih", "y60", "x2", "y60_kap"]].to_csv(anahtar, index=False)
    Hv[["bolge", "sembol", "tarih", "alis_tarih", "y60", "x2", "y60_kap"]].to_csv(havuz_yol, index=False)
    return A


def fi_k23_kor4_degerlendir(anahtar: pd.DataFrame, isaret: List[int], havuz: pd.DataFrame,
                            K: Dict[str, Any] = FI_K23_KOR4) -> Dict[str, Any]:
    """Cemal'in ✓ numaraları: ✓ / ✗ / havuz için 60 gün yukarı-aşağı, 250 gün 2 kat (giriş ertesi açılış; yan ölçü alış mumu kapanışı)."""
    A = anahtar.assign(isaret=anahtar.no.isin(isaret))
    def oz(X: pd.DataFrame) -> Dict[str, Any]:
        y = X.y60.dropna(); yk = X.y60_kap.dropna(); x2 = X.x2.dropna()
        return {"n": len(X), "yukari": float((y == 1).mean()) if len(y) else np.nan, "asagi": float((y == -1).mean()) if len(y) else np.nan,
                "x2": float(x2.mean()) if len(x2) else np.nan, "yukari_kap": float((yk == 1).mean()) if len(yk) else np.nan}
    Z = pd.DataFrame([{"grup": g, **oz(X)} for g, X in (("✓", A[A.isaret]), ("✗", A[~A.isaret]), ("hepsi", A), ("havuz", havuz))]).set_index("grup")
    karar = bool(Z.loc["✓", "yukari"] >= K["kat_esik"] * Z.loc["✗", "yukari"] and Z.loc["✓", "yukari"] >= K["kat_esik"] * Z.loc["havuz", "yukari"])
    return {"aday": A, "ozet": Z.reset_index(), "karar": karar}

# K26 ORTAK PARMAK İZİ (Cemal 26 Eki: 'KZBGY 4 Şubat - 13 Mart 2025 bölgesinin parmak izini çıkar, daha önceki hissedekiyle karşılaştır;
# belki karşılaştırmada iz çıkar'). ÖNCEDEN YAZILDI (sonuç görülmeden):
#   Örnekler (çöl = alış mumundan önceki gün biter): MANAS 13.06-11.07.2025, MANAS 20.10-05.11.2025, BINBN 27.12.2024-21.01.2025,
#   KZBGY 04.02-11.03.2025 (12.03 +%10 ilk ayak, 13.03 alış mumu). Her örneğin 16 ölçüsü kendi uzunluğunda; yüzdelik = BIST süzgeçli
#   havuzda (düşüş <= -%30, eğim >= -0,001; 20 mumluk pencereler) sırası. ORTAK ÖLÇÜ = dört örneğin yüzdelik aralığı <= K['ortak_aralik'].
#   ORTAK PROFİL = her ortak ölçüde yüzdelik [en küçük - pay, en büyük + pay] (pazarın kendi süzgeçli havuzunun yüzdeliği; ABD'de ABD'nin).
#   Ortak ölçü < 2 ise 'ortak iz yok'. Sinyal: profil + süzgeç tutan 20 mumluk pencere, aynı hissede 60 günde tek (ilk gün). İşlem: v4 alış
#   mumu (60 gün içinde kutu tepesinin üstünde kapanan ilk yeşil mum), ertesi açılış, 60 gün önce +%15 / -%15, 250 gün 2 kat, fon krizi
#   31.08.2026'da kesik. Taban: aynı süzgeçli havuzdan rastgele pencere, aynı alış mumu kuralı, aynı hücre. Hücre = alış mumu yılı
#   (2023 / 2024-26) x pazar. İZ = dört hücrede önce +%15 katı >= 1,3 (n >= 30) ve önce -%15 katı < 1,3.
FI_K26 = {"ornek": {"MANAS-1": ("MANAS", "2025-06-13", "2025-07-11"), "MANAS-2": ("MANAS", "2025-10-20", "2025-11-05"),
                    "BINBN": ("BINBN", "2024-12-27", "2025-01-21"), "KZBGY": ("KZBGY", "2025-02-04", "2025-03-11")},
          "L": 20, "ortak_aralik": 0.40, "pay": 0.05, "ayri": 60, "taban_n": 40000, "tohum": 26, "kat_esik": 1.3, "n_esik": 30,
          "donem": (("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31"))}


def fi_k26_havuz(V: Dict[str, pd.DataFrame], L: int, K: Dict[str, Any] = FI_K23_KOR) -> pd.DataFrame:
    """Bir pazarın bütün L mumluk pencerelerinin parmak izi, süzgeçli (düşüş <= K['dusus'], eğim >= K['egim'])."""
    parca = []
    for s, d in V.items():
        try:
            F = fi_k23_parmak(d, L)
            if len(F):
                parca.append(F.assign(sembol=s))
        except Exception as ex:   # tek hisse bozuksa digerleri devam eder
            filog.warning("K26 havuz %s atlandi: %s", s, ex)
    P = pd.concat(parca).rename_axis("tarih").reset_index().dropna(subset=list(FI_K23["olcu"]))
    return P[(P.dusus <= K["dusus"]) & (P.egim >= K["egim"])].reset_index(drop=True)


def fi_k26_yuzdelik(P: pd.DataFrame, X: pd.DataFrame) -> pd.DataFrame:
    """X'in her ölçüsünün P havuzundaki yüzdelik sırası (0-1)."""
    out = {}
    for k in FI_K23["olcu"]:
        s = np.sort(P[k].to_numpy(float)); x = X[k].to_numpy(float)
        out[k] = (np.searchsorted(s, x, "left") + np.searchsorted(s, x, "right")) / (2 * len(s))
    return pd.DataFrame(out, index=X.index)


def fi_k26_ortak(V: Dict[str, pd.DataFrame], Pb: pd.DataFrame, K: Dict[str, Any] = FI_K26) -> Dict[str, Any]:
    """Dört örneğin ölçüleri, BIST havuz yüzdelikleri, ortak ölçüler ve ortak profil (yüzdelik aralıkları)."""
    sat = {}
    for ad, (s, a, b) in K["ornek"].items():
        d = V[s]; i0 = int(d.index.searchsorted(pd.Timestamp(a))); i1 = int(d.index.searchsorted(pd.Timestamp(b), side="right")) - 1
        L = i1 - i0 + 1; F = fi_k23_parmak(d, L)
        sat[ad] = F.loc[d.index[i1], list(FI_K23["olcu"])].astype(float).rename(ad); sat[ad]["L"] = L
    O = pd.DataFrame(sat).T; Y = fi_k26_yuzdelik(Pb, O)
    aralik = Y.max() - Y.min(); ortak = [k for k in FI_K23["olcu"] if aralik[k] <= K["ortak_aralik"]]
    profil = {k: (max(0.0, Y[k].min() - K["pay"]), min(1.0, Y[k].max() + K["pay"])) for k in ortak}
    return {"olcu": O, "yuzdelik": Y, "aralik": aralik, "ortak": ortak, "profil": profil}


def fi_k26_tara(V: Dict[str, pd.DataFrame], P: pd.DataFrame, profil: Dict[str, Tuple[float, float]], pazar: str,
                K: Dict[str, Any] = FI_K26) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Profil sinyalleri (aynı hissede K['ayri'] günde tek) ve rastgele taban; ikisine de v4 alış mumu + sonuç."""
    Y = fi_k26_yuzdelik(P, P); m = np.ones(len(P), bool)
    for k, (a, b) in profil.items():
        m &= (Y[k].to_numpy() >= a) & (Y[k].to_numpy() <= b)
    return fi_k26_sec_islem(V, P, m, pazar, K)


def fi_k26_sec_islem(V: Dict[str, pd.DataFrame], P: pd.DataFrame, m: np.ndarray, pazar: str,
                     K: Dict[str, Any] = FI_K26) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Maske m'yi tutan pencerelerden aynı hissede K['ayri'] günde tek sinyal + rastgele taban; ikisine v4 alış mumu ve sonuç."""
    S = P[m].sort_values(["sembol", "tarih"]); sec, son = [], {}
    for r in S.itertuples():
        if r.sembol in son and r.i - son[r.sembol] < K["ayri"]:
            continue
        son[r.sembol] = r.i; sec.append(r.Index)
    def islem(X: pd.DataFrame) -> pd.DataFrame:
        sat = []
        for r in X.itertuples():
            try:
                R = fi_k23_alis_mumu(V[r.sembol], r.tarih, K["L"])
            except Exception as ex:   # tek pencere bozuksa digerleri devam eder
                filog.warning("K26 %s %s %s atlandi: %s", pazar, r.sembol, r.tarih, ex); continue
            if R["alis"] and R["olculur"]:
                sat.append({"pazar": pazar, "sembol": r.sembol, "tarih": r.tarih, **R})
        return pd.DataFrame(sat)
    T = P.sample(min(K["taban_n"], len(P)), random_state=K["tohum"])
    return islem(P.loc[sec]), islem(T)


def fi_k26_ozet(Sg: pd.DataFrame, Tb: pd.DataFrame, K: Dict[str, Any] = FI_K26) -> Tuple[pd.DataFrame, bool]:
    """Hücre (pazar x alış mumu yılı) başına sinyal / taban: önce +%15, önce -%15, 2 kat, katlar; karar."""
    Z = []
    for pz in sorted(set(Sg.pazar) | set(Tb.pazar)):
        for ad, a, b in K["donem"]:
            def oz(X):
                X = X[(X.pazar == pz) & (X.alis_tarih >= a) & (X.alis_tarih <= b)]; y = X.y60.dropna()
                return len(y), (y == 1).mean() if len(y) else np.nan, (y == -1).mean() if len(y) else np.nan, X.x2.dropna().mean()
            ns, us, as_, xs = oz(Sg); nt, ut, at, xt = oz(Tb)
            Z.append({"pazar": pz, "donem": ad, "n": ns, "yukari": us, "asagi": as_, "x2": xs, "taban_n": nt, "taban_yukari": ut,
                      "taban_asagi": at, "taban_x2": xt, "kat_yukari": us / ut if ut else np.nan, "kat_asagi": as_ / at if at else np.nan,
                      "kat_x2": xs / xt if xt else np.nan})
    Z = pd.DataFrame(Z)
    karar = bool(len(Z) == 4 and (Z.n >= K["n_esik"]).all() and (Z.kat_yukari >= K["kat_esik"]).all() and (Z.kat_asagi < K["kat_esik"]).all())
    return Z, karar


def fon_izi_k26(A: Optional[FIAyar] = None, V_hazir: Optional[Dict[str, Dict[str, pd.DataFrame]]] = None,
                K: Dict[str, Any] = FI_K26) -> Dict[str, Any]:
    """K26 sürücü: ortak parmak izi + BIST/ABD taraması. Çıktı k26_ornek.csv, k26_ozet.csv, k26_sinyal.csv."""
    A = A or FIAyar()
    Vb = V_hazir["BIST"] if V_hazir and "BIST" in V_hazir else fi_k1_veri(A.veri["BIST"], "BIST", A)
    Va = V_hazir["ABD"] if V_hazir and "ABD" in V_hazir else fi_k1_veri(A.veri["ABD"], "ABD", A)
    Pb = fi_k26_havuz(Vb, K["L"]); O = fi_k26_ortak(Vb, Pb, K)
    T = pd.concat([O["olcu"].add_prefix("deger_"), O["yuzdelik"].add_prefix("yuzdelik_")], axis=1)
    T.to_csv(os.path.join(A.cikti, "k26_ornek.csv"))
    filog.info("K26 ortak olcu: %s", O["ortak"])
    if len(O["ortak"]) < 2:
        return {"ortak": O, "ozet": pd.DataFrame(), "karar": False}
    Sb, Tb = fi_k26_tara(Vb, Pb, O["profil"], "BIST", K)
    Pa = fi_k26_havuz(Va, K["L"]); Sa, Ta = fi_k26_tara(Va, Pa, O["profil"], "ABD", K)
    Sg, Tt = pd.concat([Sb, Sa], ignore_index=True), pd.concat([Tb, Ta], ignore_index=True)
    Z, karar = fi_k26_ozet(Sg, Tt, K)
    Z.to_csv(os.path.join(A.cikti, "k26_ozet.csv"), index=False); Sg.to_csv(os.path.join(A.cikti, "k26_sinyal.csv"), index=False)
    return {"ortak": O, "ozet": Z, "karar": karar, "sinyal": Sg, "taban": Tt}

# K26 DEVAM (İz yok çıkarsa durma; ÖNCEDEN YAZILDI, ilk tur sonucu kat 1,01-1,02 görüldükten sonra, ikinci tur sonuçları görülmeden):
#   D1 SIKI: ortak aralık <= 0,30, pay 0 (yalnız en sıkı paylaşılan ölçüler, tam aralık).
#   D2 ÜÇ ÖRNEK: BINBN (bbw 0,00, yeşil %18 ile en ayrık) çıkarılır; MANAS-1, MANAS-2, KZBGY ile ortak aralık 0,40, pay 0,05.
#   D3 MERKEZ: dört örneğin 16 yüzdelik vektörünün ortalamasına (merkez) en yakın %1 pencere (pazarın kendi yüzdelikleriyle, Öklid).
#   Aynı işlem, taban, hücre ve karar (dört hücrede önce +%15 katı >= 1,3, n >= 30, önce -%15 katı < 1,3).
FI_K26_DENEME = {"D1": {"ortak_aralik": 0.30, "pay": 0.0}, "D2": {"cikar": "BINBN"}, "D3": {"en_yakin": 0.01}}


def fon_izi_k26_deneme(Vb: Dict[str, pd.DataFrame], Va: Dict[str, pd.DataFrame], Pb: pd.DataFrame, Pa: pd.DataFrame, Tt: pd.DataFrame,
                       A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K26, D: Dict[str, Any] = FI_K26_DENEME) -> pd.DataFrame:
    """K26'nın önceden yazılı üç devam denemesi; Tt = ilk turun tabanı (aynı taban kullanılır). Çıktı k26_deneme.csv."""
    A = A or FIAyar(); sat = []
    for ad in ("D1", "D2", "D3"):
        try:
            if ad == "D3":
                O = fi_k26_ortak(Vb, Pb, K); mer = O["yuzdelik"].mean()
                Sg = []
                for pz, V, P in (("BIST", Vb, Pb), ("ABD", Va, Pa)):
                    Y = fi_k26_yuzdelik(P, P); u = np.sqrt(((Y - mer) ** 2).sum(1)).to_numpy()
                    Sg.append(fi_k26_sec_islem(V, P, u <= np.quantile(u, D["D3"]["en_yakin"]), pz, {**K, "taban_n": 1})[0])
                Sg = pd.concat(Sg, ignore_index=True); ortak = list(FI_K23["olcu"])
            else:
                K2 = {**K, **{k: v for k, v in D[ad].items() if k != "cikar"}}
                if "cikar" in D[ad]:
                    K2["ornek"] = {k: v for k, v in K["ornek"].items() if k != D[ad]["cikar"]}
                O = fi_k26_ortak(Vb, Pb, K2); ortak = O["ortak"]
                if len(ortak) < 2:
                    sat.append({"deneme": ad, "ortak": ",".join(ortak), "not": "ortak ölçü < 2"}); continue
                Sg = pd.concat([fi_k26_sec_islem(V, P, fi_k26_maske(P, O["profil"]), pz, {**K, "taban_n": 1})[0]
                                for pz, V, P in (("BIST", Vb, Pb), ("ABD", Va, Pa))], ignore_index=True)
            Z, karar = fi_k26_ozet(Sg, Tt, K)
            for r in Z.itertuples(index=False):
                sat.append({"deneme": ad, "ortak": ",".join(ortak), **r._asdict(), "karar": karar})
        except Exception as ex:   # bir deneme bozulursa digerleri devam eder
            filog.error("K26 %s hata: %s", ad, ex); sat.append({"deneme": ad, "not": f"hata: {ex}"})
    Z = pd.DataFrame(sat); Z.to_csv(os.path.join(A.cikti, "k26_deneme.csv"), index=False)
    return Z


def fi_k26_maske(P: pd.DataFrame, profil: Dict[str, Tuple[float, float]]) -> np.ndarray:
    """Profilin bütün ölçülerinde yüzdelik aralığı tutan pencereler."""
    Y = fi_k26_yuzdelik(P, P); m = np.ones(len(P), bool)
    for k, (a, b) in profil.items():
        m &= (Y[k].to_numpy() >= a) & (Y[k].to_numpy() <= b)
    return m

# YENİ ÖLÇÜT (Cemal 26 Eki: 'ölçütü değiştir'; K27'den itibaren, test sonuçları görülmeden yazıldı). Eski 'önce +%20 oranı >= 1,3 kat'
# cetveli eski çalışmaların kaydı olarak kalır. Olay başına: giriş = olaydan sonraki ilk işlem günü açılışı; r60 = 60. gün kapanışı /
# giriş - 1 (fon krizi 31.08.2026'da kesik). EŞLİ FARK = r60 - aynı giriş günü, aynı 60 gün momentum beşliği x likidite üçlüsündeki öteki
# hisselerin ortalama r60'ı. HÜCRE (pazar x giriş yılı 2023 / 2024-26) İZ şartı: n >= 30; ortalama eşli fark > 0 ve ay kümeli bootstrap
# %95 güven aralığının alt ucu > 0; ortalama HÜCRE İÇİ SIRA > 0,50 (olayın r60'ı aynı gün aynı hücrede kaçıncı; 0 en kötü, 1 en iyi);
# SLOT PORTFÖYÜ (10 yuva, 60 gün tut, sırayla) olay getirileriyle, her olay yerine aynı gün aynı hücreden rastgele bir hisse alınan 200
# portföyün %90'ından büyük. İZ = dört hücre (BIST 2023, BIST 2024-26, ABD 2023, ABD 2024-26); ABD verisi yoksa en fazla BIST-ADAY.
# Düzeltme (26 Eki, içeriden alım sonuçları görülmeden, rastgele olay sağlamasıyla): ilk yazımdaki 'medyan eşli fark > 0' tek hisse
# getirisinin çarpıklığı yüzünden rastgele olayda -%6,8 çıkıyordu (hep elerdi), 'portföy > eşli ortalama getirilerin portföyü' rastgele
# olayda da olaydan yana çıkıyordu; yerlerine hücre içi sıra ve eşli rastgele portföy dağılımı kondu.
FI_OLCUT = {"ufuk": 60, "mom": 60, "likit": 20, "mom_kova": 5, "likit_kova": 3, "kriz": "2026-08-31", "bootstrap": 2000, "tohum": 27,
            "slot": 10, "n_esik": 30, "port_n": 200, "port_yuzde": 0.90, "donem": (("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31")),
            "karar": ("ABD", "AVR")}   # 28 Eki (Cemal): karar pazarları ABD + Avrupa; BIST bilgi, Çin sonra


def fi_olcut_panel(V: Dict[str, pd.DataFrame], O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """Bütün hisseler için giriş günü başına r60 (açılıştan 60. gün kapanışına), giriş öncesi 60 gün momentumu ve 20 gün TL likiditesi;
    her gün için momentum beşliği x likidite üçlüsü hücresi ve hücre ortalaması (eşli taban)."""
    S = sorted(V); T = sorted(set().union(*[V[s].index for s in S]))
    idx = pd.DatetimeIndex(T); kriz = idx.searchsorted(pd.Timestamp(O["kriz"]), side="right")
    Op = pd.DataFrame({s: V[s].Open for s in S}).reindex(idx).to_numpy(float)
    Cl = pd.DataFrame({s: V[s].Close for s in S}).reindex(idx).to_numpy(float)
    Tl = pd.DataFrame({s: V[s].Close * V[s].Volume * (V[s]["Kur"] if "Kur" in V[s] else 1.0) for s in S}).reindex(idx)   # Kur: Avrupa (EUR)
    n, u = Cl.shape; h = O["ufuk"]
    R = np.full((n, u), np.nan)
    son = min(n, kriz)
    Cf = pd.DataFrame(Cl).ffill(limit=5).to_numpy()
    # Denetim 28 Eki (ayrı model): çıkış günü (d+59) kapanışı NaN ise olay düşüyordu (birleşik takvimde kendi borsası tatil, askı);
    # çıkış kapanışı son bilinen kapanıştan (ffill, en çok 5 gün) alınır. Giriş açılışı yine o günün gerçek açılışı.
    if son - h + 1 > 0:
        with np.errstate(all="ignore"):
            R[:son - h + 1] = Cf[h - 1:son] / Op[:son - h + 1] - 1
    with np.errstate(all="ignore"):
        M = np.full((n, u), np.nan); M[O["mom"] + 1:] = Cf[O["mom"]:-1] / Cf[:-O["mom"] - 1] - 1   # giriş öncesi (d-1 / d-61)
    Lq = Tl.rolling(O["likit"], min_periods=10).median().shift(1).to_numpy()
    ok = np.isfinite(R) & np.isfinite(M) & np.isfinite(Lq) & np.isfinite(Op) & (Op > 0)
    H = np.full((n, u), -1, int)
    for d in range(n):
        g = ok[d]
        if g.sum() < 30:
            continue
        mq = pd.qcut(pd.Series(M[d, g]).rank(method="first"), O["mom_kova"], labels=False).to_numpy()
        lq = pd.qcut(pd.Series(Lq[d, g]).rank(method="first"), O["likit_kova"], labels=False).to_numpy()
        H[d, g] = mq * O["likit_kova"] + lq
    return {"tarih": idx, "sembol": S, "kol": {s: i for i, s in enumerate(S)}, "R": R, "H": H, "ok": ok}


def fi_olcut_olay(P: Dict[str, Any], olay: pd.DataFrame) -> pd.DataFrame:
    """olay: sembol, giris (giriş günü). Döner: r60, eşli ortalama r60 (aynı gün, aynı hücre, hisse kendisi hariç), eşli fark."""
    ti = {t: i for i, t in enumerate(P["tarih"])}; sat = []
    for r in olay.itertuples():
        d = ti.get(pd.Timestamp(r.giris)); j = P["kol"].get(r.sembol)
        if d is None or j is None or not P["ok"][d, j]:
            sat.append((np.nan, np.nan, np.nan, None)); continue
        m = (P["H"][d] == P["H"][d, j]) & P["ok"][d]; m[j] = False
        if m.sum() < 3:
            sat.append((P["R"][d, j], np.nan, np.nan, None)); continue
        e = P["R"][d, m]; x = P["R"][d, j]
        sat.append((x, float(e.mean()), float(((e < x).sum() + 0.5 * (e == x).sum()) / len(e)), e))
    X = olay.copy()
    X["r60"], X["esli_r60"], X["sira"] = [a[0] for a in sat], [a[1] for a in sat], [a[2] for a in sat]
    X["fark"] = X.r60 - X.esli_r60; X["_esler"] = [a[3] for a in sat]
    return X


def fi_olcut_hucre(X: pd.DataFrame, O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """Bir hücrenin olayları (fark, r60, esli_r60, giris): n, ortalama/medyan fark, ay kümeli bootstrap %95 aralık, slot portföyü."""
    X = X.dropna(subset=["fark"]).sort_values("giris")
    if not len(X):
        return {"n": 0}
    ay = pd.to_datetime(X.giris).dt.to_period("M").astype(str).to_numpy(); aylar = np.unique(ay)
    rng = np.random.default_rng(O["tohum"]); f = X.fark.to_numpy(float)
    grup = {a: f[ay == a] for a in aylar}; ort = []
    for _ in range(O["bootstrap"]):
        sec = rng.choice(aylar, len(aylar), replace=True)
        v = np.concatenate([grup[a] for a in sec]); ort.append(v.mean())
    gun = pd.to_datetime(X.giris).to_numpy().astype("datetime64[D]").astype(np.int64)
    def slot(getiri: np.ndarray) -> float:
        bos = np.zeros(O["slot"]); deger = np.ones(O["slot"]) / O["slot"]
        for gi, ri in zip(gun, getiri):
            k = int(np.argmin(bos))
            if bos[k] <= gi:
                deger[k] *= 1 + ri; bos[k] = gi + int(O["ufuk"] * 1.45)
        return float(deger.sum() - 1)
    esler = list(X["_esler"]) if "_esler" in X else [None] * len(X)
    rast = [slot(np.array([rng.choice(e) if e is not None and len(e) else x for e, x in zip(esler, X.r60.to_numpy(float))]))
            for _ in range(O["port_n"])]
    return {"n": len(X), "ort_fark": float(f.mean()), "medyan_fark": float(np.median(f)), "alt95": float(np.quantile(ort, 0.025)),
            "ust95": float(np.quantile(ort, 0.975)), "ort_r60": float(X.r60.mean()), "ort_esli": float(X.esli_r60.mean()),
            "sira": float(X.sira.mean()), "kazanan": float((f > 0).mean()), "portfoy": slot(X.r60.to_numpy(float)),
            "portfoy_esli_p50": float(np.quantile(rast, 0.5)), "portfoy_esli_p90": float(np.quantile(rast, O["port_yuzde"])),
            "portfoy_esli_p10": float(np.quantile(rast, 1 - O["port_yuzde"]))}


def fi_olcut_karar(Z: pd.DataFrame, O: Dict[str, Any] = FI_OLCUT) -> str:
    """Z: pazar, donem ve fi_olcut_hucre sütunları. O['karar'] pazarlarının (28 Eki: ABD + AVR; K27-K37 kayıtları BIST + ABD ile
    verildi) iki döneminde de tutarsa İZ; BIST bilgi: tutuyorsa 'İZ + BIST'. Karar pazarlarından biri yoksa en fazla '<var olan>-ADAY'."""
    def tut(r) -> bool:
        return bool(r.n >= O["n_esik"] and r.alt95 > 0 and r.sira > 0.5 and r.portfoy > r.portfoy_esli_p90)
    t = {(r.pazar, r.donem): tut(r) for r in Z.itertuples()}
    return _fi_olcut_karar_ortak(t, O)


def _fi_olcut_karar_ortak(t: Dict[Tuple[str, str], bool], O: Dict[str, Any], kacinma: bool = False) -> str:
    pazarlar = tuple(O.get("karar", ("ABD", "AVR"))); var = [p for p in pazarlar if any(k[0] == p for k in t)]
    hepsi = {p: all(t.get((p, d[0]), False) for d in O["donem"]) for p in pazarlar}
    bist = any(k[0] == "BIST" for k in t) and all(t.get(("BIST", d[0]), False) for d in O["donem"])
    ad = "KAÇINMA İZİ" if kacinma else "İZ"
    if len(var) == len(pazarlar) and all(hepsi.values()):
        return ad + (" + BIST" if bist else "")
    if var and len(var) < len(pazarlar) and all(hepsi[p] for p in var):
        return "-".join(var) + "-ADAY (" + ", ".join(p for p in pazarlar if p not in var) + " verisi yok)"
    return "İZ DEĞİL"


# K27 İÇERİDEN ALIM (Cemal 26 Eki: '1 + 3 ile başla'). ÖNCEDEN YAZILDI: KAP 'Pay Alım Satım Bildirimi' (konu 8aca490d50286f620150287614ae005c),
# 2022-07 -> bugün. Aracı kurum / portföy şirketi bildirimleri dışarıda (piyasa yapıcı ve fon işlemleri). Bildirimin satırlarında
# gün sonu - gün başı nominal toplamı > 0 ve sermaye oranı artmışsa NET ALIM. Hisse = relatedStocks (yoksa stockCodes; birden çoksa ilki).
# Giriş = yayın gününden SONRAKİ ilk işlem günü açılışı. Aynı hissede 60 işlem gününde tek olay (ilki). Olaylar:
#   O1 net alım; O1b büyük alım (sermaye oranı >= 0,25 puan arttı); O3 çölde net alım (yayından önceki son işlem gününde biten 20 mumluk
#   pencere: düşüş <= -%30, eğim >= -0,001, mum <= 1,0 = K23 süzgeci + küçük mum); bilgi: net satış. Ölçüt FI_OLCUT (yeni).
FI_K27 = {"konu": "8aca490d50286f620150287614ae005c", "bas": "2022-07-01", "is": 3, "bekle": 0.35,
          "klasor": os.environ.get("FI_KAPIC", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/kap_iceriden"),
          "haric": r"MENKUL DE[ĞG]ER|YATIRIM MENKUL|PORTF[ÖO]Y Y[ÖO]NET|B[ÜU]Y[ÜU]KŞEH|MENKUL KIYMET", "buyuk": 0.25, "ayri": 60}


def fi_k27_liste(K: Dict[str, Any] = FI_K27, bit: Optional[str] = None) -> pd.DataFrame:
    """KAP 'Pay Alım Satım Bildirimi' listesi, ay ay (2000 sınırına çarpan ay ikiye bölünür). liste.csv'ye yazar, kaldığı yerden sürer."""
    import json
    os.makedirs(K["klasor"], exist_ok=True); yol = os.path.join(K["klasor"], "liste.csv")
    L = pd.read_csv(yol) if os.path.exists(yol) else pd.DataFrame()
    s = _fi_kap_oturum(); son = pd.Timestamp(bit or pd.Timestamp.today().date())

    def sorgu(a: pd.Timestamp, b: pd.Timestamp) -> List[Dict[str, Any]]:
        r = _fi_kap_istek(s, "POST", _FI_KAP + "/tr/api/disclosure/members/byCriteria", deneme=6,
                          data=json.dumps({"fromDate": str(a.date()), "toDate": str(b.date()), "mkkMemberOidList": [],
                                           "subjectList": [K["konu"]]}))
        if r is None:
            raise RuntimeError(f"KAP içeriden liste {a.date()}..{b.date()} alınamadı")
        J = r.json(); time.sleep(K["bekle"])
        if len(J) >= 2000:
            if a == b:
                raise RuntimeError(f"KAP içeriden liste {a.date()}: tek günde 2000")
            m = a + pd.Timedelta(days=int((b - a).days // 2))
            return sorgu(a, m) + sorgu(m + pd.Timedelta(days=1), b)
        return J

    for bas in pd.date_range(K["bas"], son, freq="MS"):
        bit_ = min(bas + pd.offsets.MonthEnd(0), son)
        try:
            J = sorgu(bas, bit_)
        except Exception as ex:
            filog.error("%s; sonraki çalıştırmada tekrar denenecek", ex); continue
        yeni = [{"yayin": j.get("publishDate"), "unvan": j.get("kapTitle"), "kod": j.get("stockCodes"), "ilgili": j.get("relatedStocks"),
                 "ozet": j.get("summary"), "indeks": j.get("disclosureIndex")} for j in J
                if (j.get("subject") or "").strip() == "Pay Alım Satım Bildirimi"]
        if yeni:
            L = pd.concat([L, pd.DataFrame(yeni)], ignore_index=True).drop_duplicates("indeks", keep="last")
    L.to_csv(yol, index=False)
    filog.info("K27 liste: %d bildirim", len(L))
    return L


def fi_k27_ayristir(html: str) -> List[Dict[str, Any]]:
    """Bildirim sayfasındaki 'Pay Alım Satım Bilgileri' tablosunun satırları: tarih, alım, satım, gün başı/sonu nominal ve sermaye oranı."""
    from bs4 import BeautifulSoup
    def sayi(x: str) -> float:
        x = (x or "").replace("%", "").replace("\xa0", " ").strip().replace(".", "").replace(",", ".")
        try:
            return float(x) if x not in ("", "-") else np.nan
        except ValueError:
            return np.nan
    sat = []
    for tb in BeautifulSoup(html, "html.parser").find_all("table"):
        for tr in tb.find_all("tr"):
            c = [td.get_text(" ", strip=True) for td in tr.find_all("td", recursive=False)]
            if len(c) >= 10 and _fi_re.match(r"^\d{2}[/.]\d{2}[/.]\d{4}$", c[0] or ""):
                sat.append({"tarih": pd.to_datetime(c[0].replace(".", "/"), format="%d/%m/%Y", errors="coerce"),
                            "alim": sayi(c[1]), "satim": sayi(c[2]), "bas": sayi(c[4]), "son": sayi(c[5]),
                            "oran_bas": sayi(c[6]), "oran_son": sayi(c[8])})
        if sat:
            break
    return sat


def fi_k27_pdf_ayristir(metin: str) -> List[Dict[str, Any]]:
    """MKK'nın KAP'a aktardığı bildirimin PDF metni (kişi / tüzel kişi formu): 'X TL toplam nominal tutarlı alış işlemi ve/veya Y TL ...
    satış'; tutar yoksa konu satırındaki ALIM/SATIM yönü (tutar 1/-1). Tarih ilk gg/aa/yyyy, oran '%z sınırına', görev 'Görevi :'."""
    m = _fi_re.sub(r"[ \t]+", " ", metin)
    def tl(x: Optional[str]) -> float:
        return float(x.replace(".", "").replace(",", ".")) if x else np.nan
    a = _fi_re.search(r"(\d[\d.,]*)\s*(?:TL\s*)?(?:toplam\s*)?(?:nominal\s*)?(?:tutarl[ıi]|de[ğg]erli)\s*(?:pay\s*)?al[ıi][şsm]", m, _fi_re.I)
    b = _fi_re.search(r"(\d[\d.,]*)\s*(?:TL\s*)?(?:toplam\s*)?(?:nominal\s*)?(?:tutarl[ıi]|de[ğg]erli)\s*(?:pay\s*)?sat[ıi][şsm]", m, _fi_re.I)
    alim, satim = tl(a.group(1) if a else None), tl(b.group(1) if b else None)
    if not (np.isfinite(alim) or np.isfinite(satim)):
        k = _fi_re.search(r"Konu[ \t]*:[ \t]*([^\n]+)", m)
        k = (k.group(1) if k else "").upper()
        al, sa = bool(_fi_re.search(r"ALIM|ALI[ŞS]", k)), bool(_fi_re.search(r"SATIM|SATI[ŞS]", k))
        if al == sa:
            return []
        alim, satim = (1.0, 0.0) if al else (0.0, 1.0)
    t = _fi_re.search(r"(\d{2})[/.](\d{2})[/.](\d{4})", m)
    o = _fi_re.findall(r"%\s*(\d[\d,]*)\s*(?:iken|s[ıi]n[ıi]r|seviye|olarak|oran|olmu)", m)
    o_bas = _fi_re.search(r"%\s*(\d[\d,]*)\s*iken", m)
    g = _fi_re.search(r"G[öo]revi[ \t]*:[ \t]*([^\n]*)", m)
    return [{"tarih": pd.Timestamp(f"{t.group(3)}-{t.group(2)}-{t.group(1)}") if t else pd.NaT, "alim": np.nan_to_num(alim),
             "satim": np.nan_to_num(satim), "bas": np.nan, "son": np.nan, "oran_bas": tl(o_bas.group(1)) if o_bas else np.nan,
             "oran_son": tl(o[-1]) if o else np.nan, "gorev": (g.group(1).strip()[:60] if g else ""), "kaynak": "pdf"}]


def fi_k27_indir(L: pd.DataFrame, K: Dict[str, Any] = FI_K27, sinir: Optional[int] = None) -> pd.DataFrame:
    """Listedeki (aracı kurum / portföy şirketi hariç) bildirimlerin sayfalarını paralel indirip ayrıştırır; islem.csv.gz'ye ekler,
    kaldığı yerden sürer. Döner: bildirim başına satırlar (indeks + fi_k27_ayristir sütunları)."""
    from concurrent.futures import ThreadPoolExecutor
    yol = os.path.join(K["klasor"], "islem.csv.gz"); yol_b = os.path.join(K["klasor"], "bos.txt")
    I = pd.read_csv(yol, parse_dates=["tarih"]) if os.path.exists(yol) else pd.DataFrame(columns=["indeks"])
    bos = set(int(x) for x in open(yol_b).read().split()) if os.path.exists(yol_b) else set()
    Lx = L[~L.unvan.astype(str).str.upper().str.contains(K["haric"], regex=True)]
    yap = [int(i) for i in Lx.indeks if int(i) not in set(I.indeks.astype(int)) | bos][:sinir]
    filog.info("K27 indirme: %d bildirim (%d zaten var)", len(yap), len(Lx) - len(yap))

    def is_(parca: List[int]) -> Tuple[List[Dict[str, Any]], List[int]]:
        s = _fi_kap_oturum(); sat, b = [], []
        for i in parca:
            r = _fi_kap_istek(s, "GET", _FI_KAP + f"/tr/Bildirim/{i}", deneme=4)
            time.sleep(K["bekle"])
            if r is None:
                continue
            try:
                R = [{**x, "kaynak": "tablo"} for x in fi_k27_ayristir(r.text)]
                if not R:                                                      # MKK aktarımı: içerik PDF ekinde
                    ek = _fi_re.findall(r"https://www\.kap\.org\.tr/tr/api/file/download/[0-9a-f]{32}", r.text)
                    if ek:
                        p_ = _fi_kap_istek(s, "GET", ek[0], deneme=3); time.sleep(K["bekle"])
                        bas_ = p_.content.find(b"%PDF", 0, 4096) if p_ is not None else -1   # KAP eki Java seri başlığıyla gelir
                        if bas_ >= 0:
                            gecici = os.path.join(K["klasor"], f"_ek_{i}.txt")
                            _fi_metne(p_.content[bas_:], gecici)
                            with open(gecici, encoding="utf-8") as f:
                                R = fi_k27_pdf_ayristir(f.read())
                            os.unlink(gecici)
            except Exception as ex:   # tek sayfa bozuksa digerleri devam eder
                filog.warning("K27 %s ayrıştırılamadı: %s", i, ex); R = []
            (sat.extend({"indeks": i, **x} for x in R) if R else b.append(i))
        return sat, b
    t0 = time.time()
    for k in range(0, len(yap), 300):
        blok = yap[k:k + 300]; parcalar = [blok[j::K["is"]] for j in range(K["is"])]
        with ThreadPoolExecutor(K["is"]) as ex:
            for sat, b in ex.map(is_, parcalar):
                if sat:
                    I = pd.concat([I, pd.DataFrame(sat)], ignore_index=True)
                bos |= set(b)
        I.to_csv(yol, index=False)
        with open(yol_b, "w") as f:
            f.write("\n".join(map(str, sorted(bos))))
        filog.info("K27 indirme %d/%d, %d satır, %d boş, %.0f sn", min(k + 300, len(yap)), len(yap), len(I), len(bos), time.time() - t0)
    return I


def fi_k27_olaylar(L: pd.DataFrame, I: pd.DataFrame, V: Dict[str, pd.DataFrame], K: Dict[str, Any] = FI_K27) -> pd.DataFrame:
    """Bildirim başına net alım/satım, hisse, giriş günü; O1, O1b, O3 (çöl), satış bayrakları; aynı hissede K['ayri'] işlem gününde tek."""
    I = I.assign(_net=np.where(np.isfinite(I.son) & np.isfinite(I.bas), I.son - I.bas, I.alim.fillna(0) - I.satim.fillna(0)))
    G = I.groupby("indeks").agg(net=("_net", "sum"), oran_bas=("oran_bas", "first"), oran_son=("oran_son", "last"))
    B = L.merge(G, left_on="indeks", right_index=True)
    B["sembol"] = B.ilgili.where(B.ilgili.notna() & (B.ilgili.astype(str).str.len() > 0), B.kod).astype(str).str.split(",").str[0].str.strip()
    B["yayin_t"] = pd.to_datetime(B.yayin, format="%d.%m.%Y %H:%M:%S", errors="coerce")
    B = B[B.sembol.isin(V)].dropna(subset=["yayin_t"])
    sat = []
    for r in B.itertuples():
        d = V[r.sembol]; j = int(d.index.searchsorted(r.yayin_t.normalize(), side="right"))
        if j >= len(d) or j < 1:
            continue
        sat.append({"indeks": r.indeks, "sembol": r.sembol, "yayin": r.yayin_t, "giris": d.index[j], "d0": d.index[j - 1],
                    "net": r.net, "doran": r.oran_son - r.oran_bas, "unvan": r.unvan})
    X = pd.DataFrame(sat)
    X["alim"] = (X.net > 0) & ((X.doran > 0) | X.doran.isna()); X["satim"] = (X.net < 0)   # PDF bildirimlerinde gün başı oranı yok
    X["buyuk"] = X.alim & (X.doran >= K["buyuk"])
    col = []
    for s, g in X.groupby("sembol"):
        F = fi_k23_parmak(V[s], 20)
        for r in g.itertuples():
            p = F.loc[r.d0] if r.d0 in F.index else None
            col.append((r.Index, bool(p is not None and p.dusus <= FI_K23_KOR["dusus"] and p.egim >= FI_K23_KOR["egim"] and p.mum <= 1.0)))
    X["col"] = pd.Series(dict(col)); X["col_alim"] = X.alim & X.col.fillna(False)
    return X.sort_values("giris").reset_index(drop=True)


def fi_k27_tekil(X: pd.DataFrame, bayrak: str, V: Dict[str, pd.DataFrame], ayri: int = FI_K27["ayri"]) -> pd.DataFrame:
    """Bayrağı taşıyan olaylardan aynı hissede ayri işlem gününde tek (ilki)."""
    sec, son = [], {}
    for r in X[X[bayrak]].itertuples():
        i = int(V[r.sembol].index.get_loc(r.giris))
        if r.sembol in son and i - son[r.sembol] < ayri:
            continue
        son[r.sembol] = i; sec.append(r.Index)
    return X.loc[sec]


def fon_izi_k27(V: Dict[str, pd.DataFrame], A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K27, O: Dict[str, Any] = FI_OLCUT,
                indir: bool = True) -> Dict[str, Any]:
    """K27 sürücü: liste -> indirme/ayrıştırma -> olaylar -> yeni ölçüt (BIST; ABD verisi yok). Çıktı k27_olay.csv, k27_ozet.csv."""
    A = A or FIAyar()
    L = fi_k27_liste(K) if indir else pd.read_csv(os.path.join(K["klasor"], "liste.csv"))
    I = fi_k27_indir(L, K) if indir else pd.read_csv(os.path.join(K["klasor"], "islem.csv.gz"), parse_dates=["tarih"])
    X = fi_k27_olaylar(L, I, V, K); P = fi_olcut_panel(V, O); Z = []; Ev = []
    for bayrak in ("alim", "buyuk", "col_alim", "satim"):
        T = fi_olcut_olay(P, fi_k27_tekil(X, bayrak, V, K["ayri"])[["sembol", "giris", "indeks"]]); T["olay"] = bayrak; Ev.append(T)
        for ad, a, b in O["donem"]:
            H = T[(T.giris >= a) & (T.giris <= b)]
            Z.append({"olay": bayrak, "pazar": "BIST", "donem": ad, **fi_olcut_hucre(H, O)})
    Z = pd.DataFrame(Z); E = pd.concat(Ev, ignore_index=True).drop(columns="_esler")
    karar = {b: fi_olcut_karar(Z[Z.olay == b], O) for b in ("alim", "buyuk", "col_alim")}
    Z.to_csv(os.path.join(A.cikti, "k27_ozet.csv"), index=False); E.to_csv(os.path.join(A.cikti, "k27_olay.csv"), index=False)
    return {"ozet": Z, "olay": E, "karar": karar, "bildirim": X}

# K27 DEVAM (İz yok çıkarsa durma; ÖNCEDEN YAZILDI, ilk tur 'alim / buyuk / col_alim' sonucu görüldükten sonra, bu üçünün sonucu
# görülmeden; aynı ölçüt FI_OLCUT). Literatür: rutin / destek alımları bilgi taşımaz, 'fırsatçı' ve kümeli alımlar taşır.
#   D1 YÖNETİCİ: bildirimdeki görev yönetici (YÖNETİM KURULU / GENEL MÜDÜR / MÜDÜR / DİREKTÖR / CEO / CFO / BAŞKAN) ve net alım.
#   D2 KÜMELİ: aynı hissede 30 takvim gününde >= 3 ayrı net alım bildirimi; olay = 3. bildirimin girişi.
#   D3 DESTEK DEĞİL: net alım ve alım gününden önceki 60 işlem günü getirisi >= 0 (düşen fiyata destek alımı dışarıda).
FI_K27_DENEME = {"yonetici": r"Y[ÖO]NET[İI]M KURULU|GENEL M[ÜU]D[ÜU]R|M[ÜU]D[ÜU]R|D[İI]REKT[ÖO]R|\bCEO\b|\bCFO\b|BA[ŞS]KAN",
                 "kume_gun": 30, "kume_n": 3, "once_gun": 60}


def fi_k27_deneme(X: pd.DataFrame, I: pd.DataFrame, V: Dict[str, pd.DataFrame], P: Dict[str, Any], A: Optional[FIAyar] = None,
                  K: Dict[str, Any] = FI_K27, D: Dict[str, Any] = FI_K27_DENEME, O: Dict[str, Any] = FI_OLCUT) -> pd.DataFrame:
    """Önceden yazılı üç devam denemesi; X = fi_k27_olaylar çıktısı, I = ayrıştırılmış satırlar. Çıktı k27_deneme.csv."""
    A = A or FIAyar(); X = X.copy()
    gor = I.groupby("indeks").gorev.first().fillna("").astype(str).str.upper()
    X["yonetici"] = X.alim & X.indeks.map(gor).fillna("").str.contains(D["yonetici"], regex=True)
    X["kumeli"] = False
    for s, g in X[X.alim].groupby("sembol"):
        t = g.yayin.sort_values()
        for i, (ix, ti) in enumerate(t.items()):
            if ((t <= ti) & (t > ti - pd.Timedelta(days=D["kume_gun"]))).sum() >= D["kume_n"]:
                X.loc[ix, "kumeli"] = True
    once = []
    for r in X.itertuples():
        d = V[r.sembol]; j = int(d.index.get_loc(r.d0))
        once.append(d.Close.iloc[j] / d.Close.iloc[j - D["once_gun"]] - 1 if j >= D["once_gun"] else np.nan)
    X["once60"] = once; X["destek_degil"] = X.alim & (X.once60 >= 0)
    Z = []
    for bayrak in ("yonetici", "kumeli", "destek_degil"):
        T = fi_olcut_olay(P, fi_k27_tekil(X, bayrak, V, K["ayri"])[["sembol", "giris", "indeks"]])
        for ad, a, b in O["donem"]:
            Z.append({"olay": bayrak, "pazar": "BIST", "donem": ad, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
    Z = pd.DataFrame(Z); Z.to_csv(os.path.join(A.cikti, "k27_deneme.csv"), index=False)
    return Z

# K28 BİLANÇO SÜRPRİZİ (PEAD) (Cemal 27 Eki: 'başla'; yol 2). ÖNCEDEN YAZILDI (sonuç görülmeden), ölçüt FI_OLCUT:
#   Açıklama günü D: BIST = KAP 'Finansal Rapor' (konu 4028328c594bfdca01594c0af9aa0057) yayın günü, aynı hisse-yıl-dönemin ilk raporu;
#   ABD = Nasdaq bilanço takvimi günü. TEPKİ (EAR) = D'den önceki son işlem günü kapanışından D'den sonraki ilk işlem günü kapanışına
#   getiri - aynı pencerede bütün hisselerin medyan getirisi (BIST akşam, ABD açılış öncesi / kapanış sonrası açıklamalarını kapsar).
#   Giriş = tepki penceresinin bittiği günden sonraki işlem günü açılışı (geleceğe bakmaz). Sıralama açıklamanın takvim çeyreği x pazar
#   içinde. E1 = tepki en üst %20 ('iyi sürpriz'); E2 = E1 + çöl (D'den önceki son işlem gününde biten 20 mum: düşüş <= -%30, eğim >=
#   -0,001, mum <= 1,0); E3 = (yalnız ABD) analist beklentisini aşma yüzdesi en üst %20. Bilgi: tepki en alt %20 ('kötü sürpriz').
FI_K28 = {"konu": "4028328c594bfdca01594c0af9aa0057", "bas": "2022-07-01", "abd_bas": "2022-12-01", "dilim": 0.20, "bekle": 0.35,
          "klasor": os.environ.get("FI_PEAD", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/pead")}


def fi_k28_liste_bist(K: Dict[str, Any] = FI_K28, bit: Optional[str] = None) -> pd.DataFrame:
    """KAP 'Finansal Rapor' listesi ay ay (2000 sınırında ay ikiye bölünür): yayın, kodlar, yıl, dönem. liste_bist.csv."""
    import json
    os.makedirs(K["klasor"], exist_ok=True); s = _fi_kap_oturum(); son = pd.Timestamp(bit or pd.Timestamp.today().date()); sat = []

    def sorgu(a: pd.Timestamp, b: pd.Timestamp) -> List[Dict[str, Any]]:
        r = _fi_kap_istek(s, "POST", _FI_KAP + "/tr/api/disclosure/members/byCriteria", deneme=6,
                          data=json.dumps({"fromDate": str(a.date()), "toDate": str(b.date()), "mkkMemberOidList": [],
                                           "subjectList": [K["konu"]]}))
        if r is None:
            raise RuntimeError(f"KAP finansal rapor listesi {a.date()}..{b.date()} alınamadı")
        J = r.json(); time.sleep(K["bekle"])
        if len(J) >= 2000:
            if a == b:
                raise RuntimeError(f"KAP finansal rapor {a.date()}: tek günde 2000")
            m = a + pd.Timedelta(days=int((b - a).days // 2))
            return sorgu(a, m) + sorgu(m + pd.Timedelta(days=1), b)
        return J
    for bas in pd.date_range(K["bas"], son, freq="MS"):
        try:
            J = sorgu(bas, min(bas + pd.offsets.MonthEnd(0), son))
        except Exception as ex:
            filog.error("%s", ex); continue
        sat += [{"yayin": j.get("publishDate"), "kod": j.get("stockCodes"), "yil": j.get("year"), "donem": j.get("period"),
                 "unvan": j.get("kapTitle"), "indeks": j.get("disclosureIndex")} for j in J]
    L = pd.DataFrame(sat).drop_duplicates("indeks"); L.to_csv(os.path.join(K["klasor"], "liste_bist.csv"), index=False)
    filog.info("K28 BIST finansal rapor: %d", len(L))
    return L


def fi_k28_liste_abd(K: Dict[str, Any] = FI_K28, bit: Optional[str] = None) -> pd.DataFrame:
    """Nasdaq bilanço takvimi gün gün (hafta içi): tarih, sembol, sürpriz yüzdesi, saat, mali çeyrek. Kaldığı yerden sürer. liste_abd.csv."""
    import requests
    os.makedirs(K["klasor"], exist_ok=True); yol = os.path.join(K["klasor"], "liste_abd.csv")
    L = pd.read_csv(yol) if os.path.exists(yol) else pd.DataFrame(columns=["tarih"])
    bitti = set(L.tarih.astype(str)); s = requests.Session(); s.headers.update({"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    son = pd.Timestamp(bit or pd.Timestamp.today().date()); yeni = []
    for g in pd.bdate_range(K["abd_bas"], son):
        if str(g.date()) in bitti:
            continue
        J = None
        for i in range(4):
            try:
                r = s.get("https://api.nasdaq.com/api/calendar/earnings", params={"date": str(g.date())}, timeout=40)
                if r.status_code == 200:
                    J = r.json(); break
            except Exception as ex:
                filog.warning("Nasdaq %s: %s", g.date(), str(ex)[:80])
            time.sleep(3 * (i + 1))
        rows = ((J or {}).get("data") or {}).get("rows") or []
        yeni += [{"tarih": str(g.date()), "sembol": x.get("symbol"), "surpriz": x.get("surprise"), "saat": x.get("time"),
                  "ceyrek": x.get("fiscalQuarterEnding")} for x in rows] or [{"tarih": str(g.date()), "sembol": None}]
        time.sleep(K["bekle"])
        if len(yeni) > 3000:
            L = pd.concat([L, pd.DataFrame(yeni)], ignore_index=True); yeni = []; L.to_csv(yol, index=False)
    L = pd.concat([L, pd.DataFrame(yeni)], ignore_index=True); L.to_csv(yol, index=False)
    filog.info("K28 ABD takvim: %d satır", len(L))
    return L


def fi_k28_olaylar(A_: pd.DataFrame, V: Dict[str, pd.DataFrame], pazar: str, K: Dict[str, Any] = FI_K28) -> pd.DataFrame:
    """A_: sembol, D (açıklama günü), [surpriz]. Tepki (EAR, piyasa medyanına göre), giriş günü, çeyrek içi dilimler, çöl bayrağı."""
    S = sorted(V); idx = pd.DatetimeIndex(sorted(set().union(*[V[s].index for s in S])))
    C = pd.DataFrame({s: V[s].Close for s in S}).reindex(idx)
    sat = []
    for r in A_.itertuples():
        if r.sembol not in V:
            continue
        a = idx.searchsorted(pd.Timestamp(r.D)) - 1; b = idx.searchsorted(pd.Timestamp(r.D), side="right")
        if a < 0 or b + 1 >= len(idx):
            continue
        c0, c1 = C.iloc[a][r.sembol], C.iloc[b][r.sembol]
        if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
            continue
        p = (C.iloc[b] / C.iloc[a] - 1).median()
        sat.append({"sembol": r.sembol, "D": pd.Timestamp(r.D), "d0": idx[a], "tepki_son": idx[b], "giris": idx[b + 1],
                    "ear": c1 / c0 - 1 - p, "surpriz": getattr(r, "surpriz", np.nan)})
    X = pd.DataFrame(sat)
    X["ceyrek"] = X.D.dt.to_period("Q").astype(str)
    X["ust"] = X.groupby("ceyrek").ear.transform(lambda e: e >= e.quantile(1 - K["dilim"]))
    X["alt"] = X.groupby("ceyrek").ear.transform(lambda e: e <= e.quantile(K["dilim"]))
    sp = pd.to_numeric(X.surpriz, errors="coerce"); X["surpriz"] = sp
    X["analist_ust"] = sp.notna() & X.assign(sp=sp).groupby("ceyrek").sp.transform(lambda e: e >= e.quantile(1 - K["dilim"]))
    col = {}
    for s, g in X[X.ust].groupby("sembol"):
        F = fi_k23_parmak(V[s], 20)
        for r in g.itertuples():
            p = F.loc[r.d0] if r.d0 in F.index else None
            col[r.Index] = bool(p is not None and p.dusus <= FI_K23_KOR["dusus"] and p.egim >= FI_K23_KOR["egim"] and p.mum <= 1.0)
    X["col_ust"] = X.ust & pd.Series(col).reindex(X.index).fillna(False).astype(bool)
    X["pazar"] = pazar
    return X


# K28 EK (27 Eki, BIST sonuçları görüldükten SONRA, ABD sonuçları görülmeden yazıldı): 'alt' (kötü sürpriz) için AYNA ölçütü = KAÇINMA
# İZİ. Hücre tutar: n >= 30; ortalama eşli fark < 0 ve %95 aralığın üst ucu < 0; ortalama sıra < 0,50; slot portföyü 200 eşli rastgele
# portföyün %10'undan küçük. BIST hücreleri bu kural yazılmadan görüldüğü için kanıt değeri ABD hücrelerindedir (örneklem dışı doğrulama).
def fi_olcut_karar_kacinma(Z: pd.DataFrame, O: Dict[str, Any] = FI_OLCUT) -> str:
    """Kaçınma izi kararı (aşağı sinyaller): karar pazarlarının dört hücresinde ayna şartları; BIST bilgi."""
    def tut(r) -> bool:
        return bool(r.n >= O["n_esik"] and r.ust95 < 0 and r.sira < 0.5 and r.portfoy < r.portfoy_esli_p10)
    t = {(r.pazar, r.donem): tut(r) for r in Z.itertuples()}
    return _fi_olcut_karar_ortak(t, O, kacinma=True)

def fon_izi_k28(Vb: Dict[str, pd.DataFrame], Va: Dict[str, pd.DataFrame], A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K28,
                O: Dict[str, Any] = FI_OLCUT, indir: bool = True) -> Dict[str, Any]:
    """K28 sürücü: BIST (KAP) + ABD (Nasdaq) açıklama günleri -> tepki dilimleri -> yeni ölçüt. Çıktı k28_ozet.csv, k28_olay.csv."""
    A = A or FIAyar()
    Lb = fi_k28_liste_bist(K) if indir else pd.read_csv(os.path.join(K["klasor"], "liste_bist.csv"))
    La = fi_k28_liste_abd(K) if indir else pd.read_csv(os.path.join(K["klasor"], "liste_abd.csv"))
    Lb = Lb.assign(t=pd.to_datetime(Lb.yayin, format="%d.%m.%Y %H:%M:%S", errors="coerce"))
    Lb["sembol"] = [next((x.strip() for x in str(k).split(",") if x.strip() in Vb), None) for k in Lb.kod]
    Lb = Lb.dropna(subset=["sembol", "t"]).sort_values("t").drop_duplicates(["sembol", "yil", "donem"])
    Lb = Lb.assign(D=Lb.t.dt.normalize() + pd.to_timedelta((Lb.t.dt.hour >= 18).astype(int), unit="D"))   # 18:00 sonrası: ertesi gün
    La = La.dropna(subset=["sembol"]).assign(D=lambda x: pd.to_datetime(x.tarih)).drop_duplicates(["sembol", "D"])
    Xb = fi_k28_olaylar(Lb[["sembol", "D"]], Vb, "BIST", K); Xa = fi_k28_olaylar(La[["sembol", "D", "surpriz"]], Va, "ABD", K)
    Z, Ev = [], []
    for pz, X, V in (("BIST", Xb, Vb), ("ABD", Xa, Va)):
        P = fi_olcut_panel(V, O)
        for bayrak in ("ust", "col_ust", "analist_ust", "alt"):
            if not X[bayrak].any():
                continue
            T = fi_olcut_olay(P, X[X[bayrak]][["sembol", "giris", "ear", "surpriz"]]); T["olay"] = bayrak; T["pazar"] = pz; Ev.append(T)
            for ad, a, b in O["donem"]:
                Z.append({"olay": bayrak, "pazar": pz, "donem": ad, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
    Z = pd.DataFrame(Z); E = pd.concat(Ev, ignore_index=True).drop(columns="_esler")
    karar = {b: fi_olcut_karar(Z[Z.olay == b], O) for b in ("ust", "col_ust")}
    karar["alt (kaçınma)"] = fi_olcut_karar_kacinma(Z[Z.olay == "alt"], O)
    Z.to_csv(os.path.join(A.cikti, "k28_ozet.csv"), index=False); E.to_csv(os.path.join(A.cikti, "k28_olay.csv"), index=False)
    return {"ozet": Z, "olay": E, "karar": karar, "BIST": Xb, "ABD": Xa}

# K28 DEVAM (İz yok çıkarsa durma; ÖNCEDEN YAZILDI 27 Eki, ilk tur görüldükten sonra, bu üç denemenin sonucu görülmeden; aynı ölçüt
# FI_OLCUT). İlk turda eşiğe en yakın: çöl + iyi sürpriz (dört hücrede ortalama fark +%0,8 / +%2,6 / +%5,4 / +%5,6, alt uçlar eksi).
#   D1 GENİŞ ÇÖL: iyi sürpriz (üst %20) + K23 süzgeci (düşüş <= -%30, eğim >= -0,001), mum şartı yok (n büyür).
#   D2 GÜÇLÜ SÜRPRİZ: tepki üst %10 + çöl (K23 süzgeci + mum <= 1,0).
#   D3 İKİ EVRE: iyi sürpriz (üst %20) + açıklamadan önceki 60 işlem gününde K24 iki evre kuralı sinyali (Cemal'in tarifi).
FI_K28_DENEME = {"guclu": 0.10, "iki_evre_gun": 60}


def fi_k28_deneme(X: pd.DataFrame, V: Dict[str, pd.DataFrame], P: Dict[str, Any], pazar: str, D: Dict[str, Any] = FI_K28_DENEME,
                  O: Dict[str, Any] = FI_OLCUT) -> pd.DataFrame:
    """X = fi_k28_olaylar çıktısı (bir pazar). Önceden yazılı üç deneme için hücre özetleri."""
    X = X.copy()
    X["guclu"] = X.groupby("ceyrek").ear.transform(lambda e: e >= e.quantile(1 - D["guclu"]))
    gen, guc, iki = {}, {}, {}
    for s, g in X[X.ust | X.guclu].groupby("sembol"):
        F = fi_k23_parmak(V[s], 20); K24 = fi_k24_tara(V[s])
        k24 = pd.DatetimeIndex(K24.loc[K24.kural, "tarih"]) if len(K24) and "kural" in K24 else pd.DatetimeIndex([])
        ix = V[s].index
        for r in g.itertuples():
            p = F.loc[r.d0] if r.d0 in F.index else None
            suz = bool(p is not None and p.dusus <= FI_K23_KOR["dusus"] and p.egim >= FI_K23_KOR["egim"])
            gen[r.Index] = r.ust and suz
            guc[r.Index] = r.guclu and suz and bool(p is not None and p.mum <= 1.0)
            j = int(ix.get_loc(r.d0)); bas = ix[max(0, j - D["iki_evre_gun"] + 1)]
            iki[r.Index] = r.ust and bool(((k24 >= bas) & (k24 <= r.d0)).any())
    Z = []
    for ad_, sozluk in (("genis_col", gen), ("guclu_col", guc), ("iki_evre", iki)):
        m = pd.Series(sozluk).reindex(X.index).fillna(False).astype(bool)
        T = fi_olcut_olay(P, X[m][["sembol", "giris", "ear"]])
        for ad, a, b in O["donem"]:
            Z.append({"olay": ad_, "pazar": pazar, "donem": ad, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
    return pd.DataFrame(Z)

# K28 ÖRNEKLEM DIŞI (ÖNCEDEN YAZILDI 27 Eki, 2016-22 verisine hiç bakılmadan): en tutarlı aday 'güçlü_col' (tepki üst %10 + çöl: K23
# süzgeci + mum <= 1,0; 2023/2024-26'da dört hücrede ortalama fark +%3..+%11, sıra 0,54-0,56, ama aralıklar sıfırı içeriyor) ve ana
# 'col_ust', hiç kullanılmamış 2016-09 -> 2022-12 döneminde, aynı ölçütle (FI_OLCUT) iki hücrede (2016-19, 2020-22) x BIST/ABD sınanır.
# Aday GÜÇLENİR: dört eski hücrede ortalama fark > 0 ve sıra > 0,50 (yön); ayrıca hücre tutma (dört şart) sayısı yazılır.
FI_K28_DIS = {"bas_bist": "2016-07-01", "bas_abd": "2016-09-01", "bit": "2022-12-31",
              "donem": (("2016-19", "2016-09-01", "2019-12-31"), ("2020-22", "2020-01-01", "2022-12-31"))}

# K29 RİSK SÜZGECİ + PORTFÖY (Cemal 27 Eki: 'devam et'; öneri b + a). ÖNCEDEN YAZILDI (sonuç görülmeden), ölçüt FI_OLCUT:
#   ADAY = K24 iki evre kuralı sinyalleri (Cemal'in çöl tarifi), BIST + ABD. Sinyal günü d'de yalnız d ve öncesi bilgisiyle üç RİSK
#   işareti: R1 kötü bilanço sürprizi (K28 'alt': tepki penceresi d'den önceki 60 takvim gününde bitmiş); R2 A11 (son 20 işlem gününde
#   hacim >= 60 gün medyanının 3 katı + gün <= -%5 + o gün 20 gün getirisi <= -%20); R3 A14 (son 20 günde hacim >= 20 gün medyanının 20
#   katı + gün <= -%9,5). TEMİZ = işaretsiz, RİSKLİ = en az bir işaret. Karar: RİSKLİ için kaçınma ölçütü (fi_olcut_karar_kacinma) dört
#   hücrede tutarsa 'RİSK SÜZGECİ İZİ'. Bilgi: TEMİZ ve HEPSİ aynı ölçütle (eşli fark, sıra, portföy).
FI_K29 = {"r1_gun": 60, "r2_hacim": 3.0, "r2_gun": -0.05, "r2_20g": -0.20, "r3_hacim": 20.0, "r3_gun": -0.095, "pencere": 20}


def fi_k29_isaretler(d: pd.DataFrame, K: Dict[str, Any] = FI_K29) -> pd.DataFrame:
    """Bir hissenin her günü için R2 (A11) ve R3 (A14) işaretinin son K['pencere'] işlem gününde görülüp görülmediği."""
    c = d.Close; v = d.Volume.astype(float); g = c.pct_change()
    a11 = (v >= K["r2_hacim"] * v.rolling(60, min_periods=40).median().shift(1)) & (g <= K["r2_gun"]) & (c / c.shift(20) - 1 <= K["r2_20g"])
    a14 = (v >= K["r3_hacim"] * v.rolling(20, min_periods=15).median().shift(1)) & (g <= K["r3_gun"])
    w = K["pencere"]
    return pd.DataFrame({"r2": a11.astype(int).rolling(w, min_periods=1).max().astype(bool),
                         "r3": a14.astype(int).rolling(w, min_periods=1).max().astype(bool)}, index=d.index)


def fi_k29_adaylar(V: Dict[str, pd.DataFrame], X28: pd.DataFrame, pazar: str, K: Dict[str, Any] = FI_K29) -> pd.DataFrame:
    """K24 kural sinyalleri + R1/R2/R3 işaretleri; giriş = sinyal gününden sonraki ilk işlem günü."""
    kotu = X28[X28.alt][["sembol", "tepki_son"]] if len(X28) else pd.DataFrame(columns=["sembol", "tepki_son"])
    kotu_s = {s: pd.DatetimeIndex(g.tepki_son) for s, g in kotu.groupby("sembol")}
    sat = []
    for s, d in V.items():
        try:
            T = fi_k24_tara(d)
            if not len(T) or "kural" not in T:
                continue
            T = T[T.kural]
            if not len(T):
                continue
            I = fi_k29_isaretler(d, K); ix = d.index
            for t in T.tarih:
                j = int(ix.get_loc(t))
                if j + 1 >= len(ix):
                    continue
                k = kotu_s.get(s)
                r1 = bool(k is not None and ((k <= t) & (k > t - pd.Timedelta(days=K["r1_gun"]))).any())
                sat.append({"sembol": s, "sinyal": t, "giris": ix[j + 1], "r1": r1, "r2": bool(I.r2.iloc[j]), "r3": bool(I.r3.iloc[j]),
                            "pazar": pazar})
        except Exception as ex:   # tek hisse bozuksa digerleri devam eder
            filog.warning("K29 %s %s atlandi: %s", pazar, s, ex)
    X = pd.DataFrame(sat); X["riskli"] = X.r1 | X.r2 | X.r3; X["temiz"] = ~X.riskli; X["hepsi"] = True
    return X


# K29 DEVAM (ÖNCEDEN YAZILDI 27 Eki; ilk turda RİSKLİ ile TEMİZ ayrışmadı, bu üçünün sonucu görülmeden): her işaret ayrı ayrı kaçınma
# ölçütüyle: D1 yalnız R1 (kötü bilanço), D2 yalnız R2 (A11), D3 yalnız R3 (A14; n küçük olabilir). Aynı ölçüt ve karar.
FI_K29_DENEME = ("r1", "r2", "r3")

def fon_izi_k29(Vb: Dict[str, pd.DataFrame], Va: Dict[str, pd.DataFrame], X28b: pd.DataFrame, X28a: pd.DataFrame,
                Pb: Dict[str, Any], Pa: Dict[str, Any], A: Optional[FIAyar] = None, O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K29 sürücü: adaylar -> TEMİZ / RİSKLİ / HEPSİ yeni ölçütle; RİSKLİ için kaçınma kararı. Çıktı k29_ozet.csv, k29_aday.csv."""
    A = A or FIAyar(); Z, Ev = [], []
    for pz, V, X28, P in (("BIST", Vb, X28b, Pb), ("ABD", Va, X28a, Pa)):
        X = fi_k29_adaylar(V, X28, pz); Ev.append(X)
        for grup in ("hepsi", "temiz", "riskli"):
            T = fi_olcut_olay(P, X[X[grup]][["sembol", "giris"]])
            for ad, a, b in O["donem"]:
                Z.append({"olay": grup, "pazar": pz, "donem": ad, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
    Z = pd.DataFrame(Z); E = pd.concat(Ev, ignore_index=True)
    karar = {"riskli (kaçınma)": fi_olcut_karar_kacinma(Z[Z.olay == "riskli"], O), "temiz": fi_olcut_karar(Z[Z.olay == "temiz"], O)}
    Z.to_csv(os.path.join(A.cikti, "k29_ozet.csv"), index=False); E.to_csv(os.path.join(A.cikti, "k29_aday.csv"), index=False)
    return {"ozet": Z, "aday": E, "karar": karar}

# K30 ABD İÇERİDEN ALIM (SEC Form 4) (Cemal 27 Eki: 'ABD verisi izin vereyim, devam edelim; BIST hep manipülasyon'). ÖNCEDEN YAZILDI
# (sonuç görülmeden), ölçüt FI_OLCUT. Kaynak: SEC 'Insider Transactions Data Sets' (çeyreklik form345 zip; SEC adil erişim kuralı gereği
# User-Agent'ta iletişim e-postası, Cemal'in izniyle). Form '4' (düzeltme 4/A hariç), NONDERIV_TRANS işlem kodu 'P' (açık piyasa alımı),
# edinme 'A'. Bildirim değeri = adet x fiyat toplamı; olay günü = FILING_DATE (kamuya açıklandığı gün), giriş = sonraki işlem günü açılışı.
# Hisse = ISSUERTRADINGSYMBOL, ABD evrenimizde (1.411) olanlar. Aynı hissede 60 işlem gününde tek olay. Olaylar:
#   A1 alım (değer >= 10 bin $); A2 büyük alım (>= 250 bin $); A3 yönetici (Officer ya da Director; yalnız %10 ortak hariç);
#   A4 kümeli (aynı hissede 30 takvim gününde >= 3 farklı içeriden alımcı; olay = 3. kişinin bildirimi); A5 çölde alım (bildirimden
#   önceki son işlem gününde biten 20 mum: K23 süzgeci + mum <= 1,0). Hücreler ABD 2023 / ABD 2024-26 (veri 2026 1. çeyrekte biter).
#   BIST karşılığı K27'de İZ DEĞİL çıktığı için dört hücreli İZ olamaz; iki ABD hücresi tutarsa 'ABD-ADAY' yazılır (standart kararı Cemal'in).
FI_K30 = {"url": "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{c}_form345.zip",
          "ceyrekler": [f"{y}q{q}" for y in range(2022, 2027) for q in range(1, 5)], "kucuk": 10_000, "buyuk": 250_000,
          "kume_gun": 30, "kume_n": 3, "ayri": 60, "klasor": os.environ.get("FI_SEC", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/sec")}


def fi_k30_indir(eposta: str, K: Dict[str, Any] = FI_K30) -> List[str]:
    """Çeyreklik form345 zip dosyalarını indirir (var olanı atlar; yayımlanmamış çeyrek 404 -> atlanır). eposta: SEC User-Agent iletişimi."""
    import requests
    os.makedirs(K["klasor"], exist_ok=True); s = requests.Session(); s.headers.update({"User-Agent": f"Col Yolu arastirma {eposta}"})
    var = []
    for c in K["ceyrekler"]:
        yol = os.path.join(K["klasor"], f"{c}_form345.zip")
        if os.path.exists(yol) and os.path.getsize(yol) > 0:
            var.append(yol); continue
        try:
            r = s.get(K["url"].format(c=c), timeout=180)
            if r.status_code == 200:
                with open(yol, "wb") as f:
                    f.write(r.content)
                var.append(yol)
            else:
                filog.info("SEC %s: HTTP %s (yayımlanmamış olabilir)", c, r.status_code)
        except Exception as ex:
            filog.warning("SEC %s indirilemedi: %s", c, ex)
        time.sleep(0.5)
    return var


def fi_k30_alimlar(dosyalar: List[str], K: Dict[str, Any] = FI_K30) -> pd.DataFrame:
    """Form 4 açık piyasa alımları: bildirim başına sembol, açıklama günü, değer, alımcı (CIK), rol."""
    import zipfile
    parca = []
    for yol in dosyalar:
        try:
            z = zipfile.ZipFile(yol)
            S = pd.read_csv(z.open("SUBMISSION.tsv"), sep="\t", usecols=["ACCESSION_NUMBER", "FILING_DATE", "DOCUMENT_TYPE",
                                                                          "ISSUERTRADINGSYMBOL"], dtype=str)
            T = pd.read_csv(z.open("NONDERIV_TRANS.tsv"), sep="\t", usecols=["ACCESSION_NUMBER", "TRANS_CODE", "TRANS_SHARES",
                                                                              "TRANS_PRICEPERSHARE", "TRANS_ACQUIRED_DISP_CD"],
                            dtype={"ACCESSION_NUMBER": str, "TRANS_CODE": str, "TRANS_ACQUIRED_DISP_CD": str}, low_memory=False)
            R = pd.read_csv(z.open("REPORTINGOWNER.tsv"), sep="\t", usecols=["ACCESSION_NUMBER", "RPTOWNERCIK", "RPTOWNER_RELATIONSHIP"],
                            dtype=str)
        except Exception as ex:   # tek çeyrek bozuksa digerleri devam eder
            filog.warning("SEC %s okunamadı: %s", yol, ex); continue
        T = T[(T.TRANS_CODE == "P") & (T.TRANS_ACQUIRED_DISP_CD == "A")].copy()
        T["deger"] = pd.to_numeric(T.TRANS_SHARES, errors="coerce") * pd.to_numeric(T.TRANS_PRICEPERSHARE, errors="coerce")
        T = T.groupby("ACCESSION_NUMBER", as_index=False).deger.sum()
        R = R.groupby("ACCESSION_NUMBER", as_index=False).agg(cik=("RPTOWNERCIK", "first"), rol=("RPTOWNER_RELATIONSHIP", "first"))
        X = T.merge(S[S.DOCUMENT_TYPE == "4"], on="ACCESSION_NUMBER").merge(R, on="ACCESSION_NUMBER", how="left")
        parca.append(X)
    X = pd.concat(parca, ignore_index=True).drop_duplicates("ACCESSION_NUMBER")
    X["sembol"] = X.ISSUERTRADINGSYMBOL.astype(str).str.upper().str.strip()
    X["D"] = pd.to_datetime(X.FILING_DATE, format="%d-%b-%Y", errors="coerce")
    X.loc[X.D.isna(), "D"] = pd.to_datetime(X.loc[X.D.isna(), "FILING_DATE"], errors="coerce")
    return X.dropna(subset=["D"])[["ACCESSION_NUMBER", "sembol", "D", "deger", "cik", "rol"]]


def fon_izi_k30(Va: Dict[str, pd.DataFrame], P: Dict[str, Any], dosyalar: List[str], A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K30,
                O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K30 sürücü: Form 4 alımları -> A1..A5 olayları -> yeni ölçüt (ABD). Çıktı k30_ozet.csv, k30_olay.csv."""
    A = A or FIAyar(); X = fi_k30_alimlar(dosyalar, K); X = X[X.sembol.isin(Va) & (X.deger >= K["kucuk"])].copy()
    sat = []
    for r in X.itertuples():
        ix = Va[r.sembol].index; j = int(ix.searchsorted(r.D, side="right"))
        if 1 <= j < len(ix):
            sat.append((r.Index, ix[j], ix[j - 1]))
    X = X.loc[[a for a, _, _ in sat]].assign(giris=[b for _, b, _ in sat], d0=[c for _, _, c in sat]).sort_values("D")
    rol = X.rol.fillna("").astype(str)
    X["A1"] = True; X["A2"] = X.deger >= K["buyuk"]; X["A3"] = rol.str.contains("Officer|Director")
    X["A4"] = False
    for s, g in X.groupby("sembol"):
        for ix_, r in g.iterrows():
            w = g[(g.D <= r.D) & (g.D > r.D - pd.Timedelta(days=K["kume_gun"]))]
            X.loc[ix_, "A4"] = w.cik.nunique() >= K["kume_n"]
    col = {}
    for s, g in X.groupby("sembol"):
        F = fi_k23_parmak(Va[s], 20)
        for r in g.itertuples():
            p = F.loc[r.d0] if r.d0 in F.index else None
            col[r.Index] = bool(p is not None and p.dusus <= FI_K23_KOR["dusus"] and p.egim >= FI_K23_KOR["egim"] and p.mum <= 1.0)
    X["A5"] = pd.Series(col).reindex(X.index).fillna(False).astype(bool)
    Z, Ev = [], []
    for b in ("A1", "A2", "A3", "A4", "A5"):
        T = fi_olcut_olay(P, fi_k27_tekil(X, b, Va, K["ayri"])[["sembol", "giris", "deger"]]); T["olay"] = b; Ev.append(T)
        for ad, a, bb in O["donem"]:
            Z.append({"olay": b, "pazar": "ABD", "donem": ad, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= bb)], O)})
    Z = pd.DataFrame(Z); E = pd.concat(Ev, ignore_index=True).drop(columns="_esler")
    def abd(Zb):
        t = [bool(r.n >= O["n_esik"] and r.alt95 > 0 and r.sira > 0.5 and r.portfoy > r.portfoy_esli_p90) for r in Zb.itertuples()]
        return "ABD-ADAY" if len(t) == 2 and all(t) else "İZ DEĞİL"
    karar = {b: abd(Z[Z.olay == b]) for b in ("A1", "A2", "A3", "A4", "A5")}
    Z.to_csv(os.path.join(A.cikti, "k30_ozet.csv"), index=False); E.to_csv(os.path.join(A.cikti, "k30_olay.csv"), index=False)
    return {"ozet": Z, "olay": E, "karar": karar, "alim": X}

# K30 DEVAM (ÖNCEDEN YAZILDI 27 Eki; ilk turda yalnız A5 'çölde alım' ABD 2023'te dört şartı geçti (+%7,3), 2024-26 +%7,2 aralık sıfırı
# içeriyor; bu üçünün sonucu görülmeden): D1 çölde YÖNETİCİ alımı (A5 + A3); D2 çölde alım, değer >= 100 bin $; D3 ÖRNEKLEM DIŞI: A5
# kuralı hiç kullanılmamış 2016-01 -> 2022-12 SEC verisinde (hücreler 2016-19, 2020-22). A5 GÜÇLENİR: iki eski hücrede ortalama fark > 0
# ve sıra > 0,50, en az birinde dört şart. Aynı ölçüt (FI_OLCUT), aynı tekilleştirme.
FI_K30_DENEME = {"orta": 100_000, "dis_ceyrek": [f"{y}q{q}" for y in range(2016, 2022) for q in range(1, 5)],
                 "dis_donem": (("2016-19", "2016-01-01", "2019-12-31"), ("2020-22", "2020-01-01", "2022-12-31"))}

# K31 ANALİST İZLERİ (Cemal 27 Eki: 'en başarılı analistlerin izlediği 4 veri: seyrelme, içeriden satış, nakit tükenmesi, kurumsal
# sahiplik; yapılanları ayıkla, yapılmayanları dene; tıkanırsan çözüm bul, bulamazsan başka veriyi irdele'). Yapılanlar: içeriden ALIM
# (K27, K30), BIST fon sahipliği (K10, K25). ÖNCEDEN YAZILDI (sonuç görülmeden), ABD, hücreler 2023 / 2024-26, aynı hissede 60 işlem
# gününde tek olay, giriş olayın kamuya çıktığı günden sonraki ilk işlem günü açılışı, ölçüt FI_OLCUT (kaçınma için ayna ölçütü):
#   M1 İÇERİDEN SATIŞ (SEC Form 4, kod S, elden çıkarma D; 10b5-1 planlı bildirim hariç; Officer/Director; değer >= 100 bin $) -> kaçınma.
#      M1b kümeli satış (30 günde >= 3 farklı satıcı) -> kaçınma.
#   M2 SEYRELME (SEC finansal tablo veri seti, 10-Q / 10-K, dei EntityCommonStockSharesOutstanding): pay sayısı bir yıl önceki (300-430
#      gün önceki en yakın) değere göre >= +%10 -> kaçınma; M2b >= +%30 -> kaçınma; M2c GERİ ALIM <= -%3 -> yukarı ölçüt (FI_OLCUT).
#   M3 NAKİT TÜKENMESİ: faaliyet nakit akışı < 0 ve nakit / (çeyrek başı yakma) < 4 çeyrek -> kaçınma; M3b < 2 çeyrek -> kaçınma.
#   M4 AÇIĞA SATIŞ (13F yerine: 13F'te CUSIP -> sembol eşlemesi bedava yok; FINRA konsolide açığa satış): ABD evreninde ödeme günü
#      kapatma süresi (days to cover) en üst %10 -> kaçınma; giriş = ödeme gününden >= 12 takvim günü sonraki ilk işlem günü (yayın gecikmesi).
# Karar: iki ABD hücresinde kaçınma (ya da yukarı) ölçütü tutarsa 'ABD-ADAY'; tutan ölçü sonra BIST'te (İş Yatırım / KAP) sınanır.
FI_K31 = {"satis_min": 100_000, "kume_gun": 30, "kume_n": 3, "seyrelme": 0.10, "agir_seyrelme": 0.30, "geri_alim": -0.03,
          "yil_min": 300, "yil_max": 430, "pist": 4.0, "pist_agir": 2.0, "dtc_ust": 0.90, "gecikme": 12, "ayri": 60,
          "finra": "https://api.finra.org/data/group/otcMarket/name/consolidatedShortInterest",
          "klasor": os.environ.get("FI_SECFS", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/secfs")}


def fi_k31_satislar(dosyalar: List[str], K: Dict[str, Any] = FI_K31) -> pd.DataFrame:
    """Form 4 açık piyasa satışları (kod S, D), 10b5-1 planlı hariç: bildirim başına sembol, gün, değer, satıcı, rol."""
    import zipfile
    parca = []
    for yol in dosyalar:
        try:
            z = zipfile.ZipFile(yol)
            S = pd.read_csv(z.open("SUBMISSION.tsv"), sep="\t", dtype=str,
                            usecols=lambda c: c in ("ACCESSION_NUMBER", "FILING_DATE", "DOCUMENT_TYPE", "ISSUERTRADINGSYMBOL", "AFF10B5ONE"))
            T = pd.read_csv(z.open("NONDERIV_TRANS.tsv"), sep="\t", usecols=["ACCESSION_NUMBER", "TRANS_CODE", "TRANS_SHARES",
                            "TRANS_PRICEPERSHARE", "TRANS_ACQUIRED_DISP_CD"], dtype={"ACCESSION_NUMBER": str, "TRANS_CODE": str,
                            "TRANS_ACQUIRED_DISP_CD": str}, low_memory=False)
            R = pd.read_csv(z.open("REPORTINGOWNER.tsv"), sep="\t", usecols=["ACCESSION_NUMBER", "RPTOWNERCIK", "RPTOWNER_RELATIONSHIP"],
                            dtype=str)
        except Exception as ex:   # tek çeyrek bozuksa digerleri devam eder
            filog.warning("SEC %s okunamadı: %s", yol, ex); continue
        T = T[(T.TRANS_CODE == "S") & (T.TRANS_ACQUIRED_DISP_CD == "D")].copy()
        T["deger"] = pd.to_numeric(T.TRANS_SHARES, errors="coerce") * pd.to_numeric(T.TRANS_PRICEPERSHARE, errors="coerce")
        T = T.groupby("ACCESSION_NUMBER", as_index=False).deger.sum()
        S = S[S.DOCUMENT_TYPE == "4"]
        if "AFF10B5ONE" in S:
            S = S[~S.AFF10B5ONE.fillna("").astype(str).str.strip().str.lower().isin(("1", "true", "y", "yes"))]
        R = R.groupby("ACCESSION_NUMBER", as_index=False).agg(cik=("RPTOWNERCIK", "first"), rol=("RPTOWNER_RELATIONSHIP", "first"))
        parca.append(T.merge(S, on="ACCESSION_NUMBER").merge(R, on="ACCESSION_NUMBER", how="left"))
    X = pd.concat(parca, ignore_index=True).drop_duplicates("ACCESSION_NUMBER")
    X["sembol"] = X.ISSUERTRADINGSYMBOL.astype(str).str.upper().str.strip()
    X["D"] = pd.to_datetime(X.FILING_DATE, format="%d-%b-%Y", errors="coerce")
    return X.dropna(subset=["D"])[["sembol", "D", "deger", "cik", "rol"]]


def fi_k31_finansal(K: Dict[str, Any] = FI_K31) -> pd.DataFrame:
    """SEC finansal tablo özütleri (fs_YYYYqQ.csv.gz) -> bildirim başına sembol, açıklama günü, pay sayısı, yıllık pay değişimi, pist."""
    import glob, json
    tk = json.load(open(os.path.join(K["klasor"], "company_tickers.json")))
    cik2 = {}
    for v in tk.values():
        cik2.setdefault(str(int(v["cik_str"])), v["ticker"].upper().replace(".", "-"))
    N = pd.concat([pd.read_csv(f, dtype=str) for f in sorted(glob.glob(os.path.join(K["klasor"], "fs_*.csv.gz")))], ignore_index=True)
    N["value"] = pd.to_numeric(N.value, errors="coerce"); N["qtrs"] = pd.to_numeric(N.qtrs, errors="coerce")
    N["filed"] = pd.to_datetime(N.filed, format="%Y%m%d", errors="coerce"); N["ddate"] = pd.to_datetime(N.ddate, format="%Y%m%d", errors="coerce")
    N["sembol"] = N.cik.astype(str).str.lstrip("0").map(cik2)
    N = N.dropna(subset=["sembol", "filed", "value"])
    # Düzeltme (27 Eki, M2/M3 sonucu görülmeden): dei EntityCommonStockSharesOutstanding bu veri setinde neredeyse yok (çeyrekte ~1 satır;
    # kapak sayfası). Pay sayısı bilançodaki CommonStockSharesOutstanding (anlık), yoksa çeyreklik ağırlıklı ortalama temel pay sayısı
    # (WeightedAverageNumberOfSharesOutstandingBasic, qtrs = 1), yoksa dei kalemi. Eşikler aynı.
    oncelik = {"CommonStockSharesOutstanding": 0, "WeightedAverageNumberOfSharesOutstandingBasic": 1, "EntityCommonStockSharesOutstanding": 2}
    Pn = N[N.tag.isin(oncelik) & ((N.tag != "WeightedAverageNumberOfSharesOutstandingBasic") | (N.qtrs == 1))].copy()
    Pn["_o"] = Pn.tag.map(oncelik)
    pay = Pn.sort_values(["ddate", "_o"], ascending=[True, False]).groupby("adsh").agg(
        sembol=("sembol", "first"), filed=("filed", "first"), pay=("value", "last"), pay_t=("ddate", "last"))
    nak = N[N.tag.isin(["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"])]
    nak = nak.sort_values(["ddate", "tag"]).groupby("adsh").value.last().rename("nakit")
    ocf = N[(N.tag == "NetCashProvidedByUsedInOperatingActivities") & (N.qtrs >= 1)]
    ocf = ocf.sort_values(["ddate", "qtrs"]).groupby("adsh").apply(lambda g: g.value.iloc[-1] / g.qtrs.iloc[-1]).rename("ocf_ceyrek")
    F = pay.join(nak).join(ocf).reset_index().sort_values(["sembol", "filed"])
    yil = []
    for s, g in F.groupby("sembol"):
        t, p = g.pay_t.to_numpy(), g.pay.to_numpy(float)
        for i in range(len(g)):
            d = (t[i] - t[:i]).astype("timedelta64[D]").astype(float) if i else np.array([])
            m = np.flatnonzero((d >= K["yil_min"]) & (d <= K["yil_max"]))
            yil.append(p[i] / p[m[np.argmin(np.abs(d[m] - 365))]] - 1 if len(m) and p[m].all() else np.nan)
    F["pay_yil"] = yil
    F["pist"] = np.where(F.ocf_ceyrek < 0, F.nakit / (-F.ocf_ceyrek), np.inf)
    return F


def fi_k31_aciga(semboller: List[str], bas: str, bit: str, K: Dict[str, Any] = FI_K31) -> pd.DataFrame:
    """FINRA konsolide açığa satış (ödeme günü, sembol, kapatma süresi), sembol grupları ve ay ay sayfalı."""
    import requests
    sat = []
    for a in pd.date_range(bas, bit, freq="MS"):
        b = a + pd.offsets.MonthEnd(0)
        for k in range(0, len(semboller), 400):
            ofs = 0
            while True:
                gov = {"limit": 5000, "offset": ofs, "fields": ["symbolCode", "settlementDate", "daysToCoverQuantity"],
                       "dateRangeFilters": [{"fieldName": "settlementDate", "startDate": str(a.date()), "endDate": str(b.date())}],
                       "domainFilters": [{"fieldName": "symbolCode", "values": semboller[k:k + 400]}]}
                J = None
                for i in range(4):
                    try:
                        r = requests.post(K["finra"], json=gov, headers={"Accept": "application/json"}, timeout=90)
                        if r.status_code == 200:
                            J = r.json(); break
                    except Exception as ex:
                        filog.warning("FINRA %s: %s", a.date(), str(ex)[:80])
                    time.sleep(3 * (i + 1))
                J = J or []; sat += J; ofs += 5000
                if len(J) < 5000:
                    break
                time.sleep(0.3)
    X = pd.DataFrame(sat)
    if len(X):
        X["settlementDate"] = pd.to_datetime(X.settlementDate); X["dtc"] = pd.to_numeric(X.daysToCoverQuantity, errors="coerce")
    return X

def fon_izi_k31(Va: Dict[str, pd.DataFrame], P: Dict[str, Any], form4: List[str], Fin: pd.DataFrame, SI: pd.DataFrame,
                A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K31, O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K31 sürücü: M1..M4 olayları (ABD) -> yeni ölçüt; kaçınma ölçüleri ayna kararla, M2c yukarı ölçütle. Çıktı k31_ozet.csv."""
    A = A or FIAyar(); olay: Dict[str, pd.DataFrame] = {}

    def giris_ekle(X: pd.DataFrame, sol: bool = False) -> pd.DataFrame:
        sat = []
        for r in X.itertuples():
            if r.sembol not in Va:
                continue
            ix = Va[r.sembol].index; j = int(ix.searchsorted(r.D, side="left" if sol else "right"))
            if 1 <= j < len(ix):
                sat.append({"sembol": r.sembol, "D": r.D, "giris": ix[j]})
        return pd.DataFrame(sat)
    Sx = fi_k31_satislar(form4, K); Sx = Sx[Sx.sembol.isin(Va) & (Sx.deger >= K["satis_min"])]
    Sx = Sx[Sx.rol.fillna("").astype(str).str.contains("Officer|Director")].sort_values("D")
    olay["M1_iceriden_satis"] = giris_ekle(Sx)
    kume = []
    for s, g in Sx.groupby("sembol"):
        for r in g.itertuples():
            if g[(g.D <= r.D) & (g.D > r.D - pd.Timedelta(days=K["kume_gun"]))].cik.nunique() >= K["kume_n"]:
                kume.append({"sembol": s, "D": r.D})
    olay["M1b_kumeli_satis"] = giris_ekle(pd.DataFrame(kume))
    Fn = Fin.rename(columns={"filed": "D"})
    olay["M2_seyrelme"] = giris_ekle(Fn[Fn.pay_yil >= K["seyrelme"]])
    olay["M2b_agir_seyrelme"] = giris_ekle(Fn[Fn.pay_yil >= K["agir_seyrelme"]])
    olay["M2c_geri_alim"] = giris_ekle(Fn[Fn.pay_yil <= K["geri_alim"]])
    olay["M3_nakit_tukenmesi"] = giris_ekle(Fn[Fn.pist < K["pist"]])
    olay["M3b_agir_nakit"] = giris_ekle(Fn[Fn.pist < K["pist_agir"]])
    if len(SI):
        T = SI[SI.symbolCode.isin(Va)].dropna(subset=["dtc"])
        T = T[T.dtc >= T.groupby("settlementDate").dtc.transform(lambda x: x.quantile(K["dtc_ust"]))]
        olay["M4_aciga_satis"] = giris_ekle(pd.DataFrame({"sembol": T.symbolCode, "D": T.settlementDate + pd.Timedelta(days=K["gecikme"])}),
                                            sol=True)
    Z = []
    for ad_, X in olay.items():
        if not len(X):
            continue
        X = X.sort_values("giris").assign(_b=True)
        T = fi_olcut_olay(P, fi_k27_tekil(X, "_b", Va, K["ayri"])[["sembol", "giris"]])
        for ad, a, b in O["donem"]:
            Z.append({"olay": ad_, "pazar": "ABD", "donem": ad, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
    Z = pd.DataFrame(Z)

    def iki(Zb: pd.DataFrame, yukari: bool) -> str:
        if yukari:
            t = [bool(r.n >= O["n_esik"] and r.alt95 > 0 and r.sira > 0.5 and r.portfoy > r.portfoy_esli_p90) for r in Zb.itertuples()]
        else:
            t = [bool(r.n >= O["n_esik"] and r.ust95 < 0 and r.sira < 0.5 and r.portfoy < r.portfoy_esli_p10) for r in Zb.itertuples()]
        return ("ABD-ADAY" + ("" if yukari else " (kaçınma)")) if len(t) == 2 and all(t) else "İZ DEĞİL"
    karar = {o: iki(Z[Z.olay == o], o == "M2c_geri_alim") for o in Z.olay.unique()}
    Z.to_csv(os.path.join(A.cikti, "k31_ozet.csv"), index=False)
    return {"ozet": Z, "karar": karar, "olay": olay}

# K31 DEVAM (ÖNCEDEN YAZILDI 27 Eki; ilk turda dört ölçünün hiçbiri iki ABD hücresinde tutmadı, bu üçünün sonucu görülmeden):
#   D1 İFLAS PROFİLİ: aynı bildirimde seyrelme >= +%10 VE nakit pisti < 4 çeyrek -> kaçınma.
#   D2 TEMİZ ÇÖL: K24 iki evre sinyali (ABD) ve sinyalden önceki son finansal bildirimde seyrelme < +%3 ve (faaliyet nakit akışı >= 0 ya
#      da pist >= 8 çeyrek) -> yukarı ölçüt (FI_OLCUT).
#   D3 ÇÖL TUZAĞI: K24 iki evre sinyali ve son bildirimde seyrelme >= +%10 ya da pist < 4 -> kaçınma.
FI_K31_DENEME = {"temiz_seyrelme": 0.03, "temiz_pist": 8.0}


def fi_k31_deneme(Va: Dict[str, pd.DataFrame], P: Dict[str, Any], Fin: pd.DataFrame, aday: pd.DataFrame, K: Dict[str, Any] = FI_K31,
                  D: Dict[str, Any] = FI_K31_DENEME, O: Dict[str, Any] = FI_OLCUT) -> pd.DataFrame:
    """aday = K29 aday tablosunun ABD satırları (sembol, sinyal, giris). Üç deneme için hücre özetleri."""
    Fn = Fin[Fin.sembol.isin(Va)].sort_values("filed")
    E1 = Fn[(Fn.pay_yil >= K["seyrelme"]) & (Fn.pist < K["pist"])]
    sat = []
    for r in E1.itertuples():
        ix = Va[r.sembol].index; j = int(ix.searchsorted(r.filed, side="right"))
        if 1 <= j < len(ix):
            sat.append({"sembol": r.sembol, "giris": ix[j]})
    gruplar = {"D1_iflas_profili": pd.DataFrame(sat)}
    A_ = aday.sort_values("sinyal").copy(); son = []
    for r in A_.itertuples():
        g = Fn[(Fn.sembol == r.sembol) & (Fn.filed <= r.sinyal)]
        son.append(g.iloc[-1] if len(g) else None)
    A_["pay_yil"] = [x.pay_yil if x is not None else np.nan for x in son]
    A_["pist"] = [x.pist if x is not None else np.nan for x in son]
    A_["ocf"] = [x.ocf_ceyrek if x is not None else np.nan for x in son]
    temiz = (A_.pay_yil < D["temiz_seyrelme"]) & ((A_.ocf >= 0) | (A_.pist >= D["temiz_pist"]))
    tuzak = (A_.pay_yil >= K["seyrelme"]) | (A_.pist < K["pist"])
    gruplar["D2_temiz_col"] = A_[temiz]; gruplar["D3_col_tuzagi"] = A_[tuzak]
    Z = []
    for ad_, X in gruplar.items():
        if not len(X):
            continue
        X = X.sort_values("giris").assign(_b=True)
        T = fi_olcut_olay(P, fi_k27_tekil(X, "_b", Va, K["ayri"])[["sembol", "giris"]])
        for ad, a, b in O["donem"]:
            Z.append({"olay": ad_, "pazar": "ABD", "donem": ad, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
    return pd.DataFrame(Z)

# K32 SADE PORTFÖY ÖLÇÜMÜ (Cemal 27 Eki: 'a ile devam et, sade portföy ölçümü'). İz testi değil, DÜZEN ölçümü; beklenti gerçekçi kurulur.
# ÖNCEDEN YAZILDI (sonuç görülmeden). Her pazar (BIST, ABD) ve dönem (2016-22, 2023, 2024-26; fiyat 31.08.2026'da kesik) ayrı, başlangıç
# sermayesi 1, 10 eşit yuva, nakit faiz getirmez (BIST'te mevduat getirisi yok sayılır: düzen aleyhine), işlem maliyeti tek yön BIST %0,2,
# ABD %0,1. Düzenler:
#   P0 PİYASA: bütün hisselere eşit ağırlık, her gün yeniden dengelenen al-tut (günlük getiri ±%50'de kırpılır).
#   P1 RASTGELE + 60 GÜN: boş yuva olduğu her gün ertesi açılışta rastgele hisse, 60 işlem günü tut (50 tohum; ortanca + dağılım).
#   P2 ÇÖL + 60 GÜN: K24 iki evre sinyalleri (sinyal sırasıyla, boş yuva varsa), ertesi açılış, 60 gün tut.
#   P3 ÇÖL + ÇIKIŞ: P2 girişleri; çıkış = kapanış sinyal öncesi 20 gün dibinin %2 altına inerse (kutu dibi), +%20 görüldükten sonra
#      kapanış SMA20 altına inerse (trail), en çok 120 işlem günü.
#   P4 RASTGELE + ÇIKIŞ: P1 girişleri, P3 çıkışı (çıkış kuralının katkısı).
# Ölçüler: toplam getiri, yıllık getiri, en büyük düşüş (MDD), getiri / |MDD|, yatırımda geçen gün oranı, işlem sayısı, kazanan oranı,
# en kötü işlem. KULLANILABİLİR DÜZEN (önceden): P3 dört karar hücresinin (BIST/ABD x 2023/2024-26) hepsinde MDD <= 0,8 x P0 MDD ve
# getiri/|MDD| >= P0'ınki. Ayrıca P3, P4'ün (50 tohum) en az %75'inden iyi değilse 'girişin katkısı yok' yazılır.
FI_K32 = {"slot": 10, "tut": 60, "azami": 120, "kar_esik": 0.20, "dip_gun": 20, "dip_pay": 0.98, "maliyet": {"BIST": 0.002, "ABD": 0.001},
          "tohum_n": 50, "kirp": 0.5, "kriz": "2026-08-31",
          "donem": (("2016-22", "2016-10-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-08-31"))}


def fi_k32_piyasa(V: Dict[str, pd.DataFrame], bas: str, bit: str, K: Dict[str, Any] = FI_K32) -> pd.Series:
    """P0: eşit ağırlıklı, günlük dengelenen piyasa değeri (bas..bit, 1'den)."""
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index().loc[bas:bit]
    g = C.pct_change(fill_method=None).clip(-K["kirp"], K["kirp"]).mean(axis=1).fillna(0.0)
    return (1 + g).cumprod()


def fi_k32_islem(d: pd.DataFrame, j: int, kural: str, K: Dict[str, Any] = FI_K32, son: Optional[int] = None) -> Tuple[int, List[float]]:
    """d'de j günü açılışında giren işlemin günlük değer çarpanları (giriş fiyatına göre, j..çıkış günü kapanışı) ve çıkış indeksi."""
    o = d.Open.to_numpy(float); c = d.Close.to_numpy(float); n = len(c) if son is None else min(len(c), son)
    g = o[j]
    if not (g > 0):
        return j, [1.0]
    if kural == "tut":
        e = min(j + K["tut"] - 1, n - 1)
        return e, list(c[j:e + 1] / g)
    dip = np.nanmin(d.Low.to_numpy(float)[max(0, j - K["dip_gun"]):j]) * K["dip_pay"] if j > 0 else 0.0
    sma = d.Close.rolling(20).mean().to_numpy(); yol, gordu = [], False
    for k in range(j, min(j + K["azami"], n)):
        yol.append(c[k] / g); gordu = gordu or c[k] >= g * (1 + K["kar_esik"])
        if c[k] < dip or (gordu and np.isfinite(sma[k]) and c[k] < sma[k]):
            return k, yol
    return min(j + K["azami"], n) - 1, yol


def fi_k32_benzet(V: Dict[str, pd.DataFrame], giris: List[Tuple[pd.Timestamp, str]], kural: str, bas: str, bit: str, maliyet: float,
                  K: Dict[str, Any] = FI_K32, rastgele: Optional[np.random.Generator] = None,
                  C: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Yuva benzetimi (gün sırası: açılışta giriş, kapanışta değerleme, kapanışta çıkış; çıkışın nakdi ertesi gün kullanılır).
    giris: (gün, sembol) sırası (P2/P3; aynı gün sıra = verilen sıra); rastgele verilirse her gün boş yuva kadar, o gün verisi olan ve
    en az dip_gun geçmişi bulunan hisselerden rastgele seçilir (P1/P4)."""
    C = pd.DataFrame({s_: d.Close for s_, d in V.items()}).sort_index() if C is None else C
    gun = C.loc[bas:bit].index
    if not len(gun):
        return {}
    sem = np.array(C.columns); gecmis = C.notna().cumsum().loc[gun].to_numpy() > K["dip_gun"]; var = C.loc[gun].notna().to_numpy() & gecmis
    gs: Dict[pd.Timestamp, List[str]] = {}
    for t, s_ in giris:
        gs.setdefault(pd.Timestamp(t), []).append(s_)
    deger = np.zeros(len(gun)); nakit = 1.0; acik: List[Dict[str, Any]] = []; islem: List[float] = []; onceki = 1.0
    for i, t in enumerate(gun):
        if rastgele is not None:
            bos = K["slot"] - len(acik); havuz = sem[var[i]]
            adaylar = list(rastgele.choice(havuz, size=min(bos, len(havuz)), replace=False)) if bos > 0 and len(havuz) else []
        else:
            adaylar = gs.get(t, [])
        for s_ in adaylar:
            if len(acik) >= K["slot"] or any(p["s"] == s_ for p in acik):
                continue
            d = V[s_]
            if t not in d.index:
                continue
            j = int(d.index.get_loc(t)); son_ = int(d.index.searchsorted(pd.Timestamp(bit), side="right"))
            e, yol = fi_k32_islem(d, j, kural, K, son_)
            if not len(yol) or not np.isfinite(yol).all():
                continue
            tutar = min(onceki / K["slot"], nakit / (1 + maliyet))
            if tutar <= 0:
                continue
            nakit -= tutar * (1 + maliyet)
            yt = pd.Series(yol, index=d.index[j:j + len(yol)]).reindex(gun[i:]).ffill()
            yt = yt.loc[:d.index[e]].to_numpy()
            acik.append({"s": s_, "tutar": tutar, "i0": i, "yol": yt})
        deger[i] = nakit + sum(p["tutar"] * p["yol"][min(i - p["i0"], len(p["yol"]) - 1)] for p in acik)
        onceki = deger[i]
        for p in [p for p in acik if i - p["i0"] >= len(p["yol"]) - 1]:
            nakit += p["tutar"] * p["yol"][-1] * (1 - maliyet); islem.append(p["yol"][-1] * (1 - maliyet) / (1 + maliyet) - 1)
            acik.remove(p)
            deger[i] -= p["tutar"] * p["yol"][-1] * maliyet
    for p in acik:
        islem.append(p["yol"][-1] / (1 + maliyet) - 1)
    return {"deger": pd.Series(deger, index=gun), "islem": np.array(islem)}


def fi_k32_olc(D: pd.Series, islem: Optional[np.ndarray] = None) -> Dict[str, float]:
    """Toplam / yıllık getiri, en büyük düşüş, getiri/|MDD|, işlem istatistikleri."""
    if D is None or not len(D):
        return {}
    top = float(D.iloc[-1] / D.iloc[0] - 1); yil = (D.index[-1] - D.index[0]).days / 365.25
    mdd = float((D / D.cummax() - 1).min())
    o = {"toplam": top, "yillik": (1 + top) ** (1 / yil) - 1 if yil > 0 and top > -1 else np.nan, "mdd": mdd,
         "getiri_mdd": top / abs(mdd) if mdd < 0 else np.nan}
    if islem is not None and len(islem):
        o.update({"islem_n": len(islem), "kazanan": float((islem > 0).mean()), "en_kotu": float(islem.min()),
                  "ort_islem": float(islem.mean())})
    return o


def fon_izi_k32(Vb: Dict[str, pd.DataFrame], Va: Dict[str, pd.DataFrame], aday: pd.DataFrame, A: Optional[FIAyar] = None,
                K: Dict[str, Any] = FI_K32) -> Dict[str, Any]:
    """K32 sürücü: P0..P4, pazar x dönem. aday = K24 sinyalleri (pazar, sembol, giris). Çıktı k32_ozet.csv."""
    A = A or FIAyar(); Z = []
    aday = aday.assign(giris=pd.to_datetime(aday.giris))
    for pz, V in (("BIST", Vb), ("ABD", Va)):
        mal = K["maliyet"][pz]; ad_p = aday[aday.pazar == pz].sort_values(["giris", "sembol"])
        C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index()
        for dn, bas, bit in K["donem"]:
            P0 = fi_k32_piyasa(V, bas, bit, K); Z.append({"pazar": pz, "donem": dn, "duzen": "P0_piyasa", **fi_k32_olc(P0)})
            gir = [(r.giris, r.sembol) for r in ad_p[(ad_p.giris >= bas) & (ad_p.giris <= bit)].itertuples() if r.sembol in V]
            filog.info("K32 %s %s: %d çöl girişi", pz, dn, len(gir))
            for ad_, kural in (("P2_col_60gun", "tut"), ("P3_col_cikis", "cikis")):
                R = fi_k32_benzet(V, gir, kural, bas, bit, mal, K, C=C)
                Z.append({"pazar": pz, "donem": dn, "duzen": ad_, "giris_n": len(gir), **fi_k32_olc(R.get("deger"), R.get("islem"))})
            for ad_, kural in (("P1_rastgele_60gun", "tut"), ("P4_rastgele_cikis", "cikis")):
                sat = []
                for tt in range(K["tohum_n"]):
                    R = fi_k32_benzet(V, [], kural, bas, bit, mal, K, np.random.default_rng(tt), C)
                    sat.append(fi_k32_olc(R.get("deger"), R.get("islem")))
                S = pd.DataFrame(sat)
                Z.append({"pazar": pz, "donem": dn, "duzen": ad_, **S.median().to_dict(),
                          "getiri_mdd_p75": float(S.getiri_mdd.quantile(0.75)), "toplam_p25": float(S.toplam.quantile(0.25)),
                          "toplam_p75": float(S.toplam.quantile(0.75))})
    Z = pd.DataFrame(Z); Z.to_csv(os.path.join(A.cikti, "k32_ozet.csv"), index=False)
    karar = []
    for pz in ("BIST", "ABD"):
        for dn in ("2023", "2024-26"):
            g = Z[(Z.pazar == pz) & (Z.donem == dn)].set_index("duzen")
            karar.append(bool(g.loc["P3_col_cikis", "mdd"] >= 0.8 * g.loc["P0_piyasa", "mdd"]
                              and g.loc["P3_col_cikis", "getiri_mdd"] >= g.loc["P0_piyasa", "getiri_mdd"]))
    katki = []
    for pz in ("BIST", "ABD"):
        for dn in ("2023", "2024-26"):
            g = Z[(Z.pazar == pz) & (Z.donem == dn)].set_index("duzen")
            katki.append(bool(g.loc["P3_col_cikis", "getiri_mdd"] > g.loc["P4_rastgele_cikis", "getiri_mdd_p75"]))
    return {"ozet": Z, "karar": "KULLANILABİLİR DÜZEN" if all(karar) else "KULLANILABİLİR DEĞİL", "hucre": karar,
            "giris_katkisi": "VAR" if all(katki) else "YOK", "katki_hucre": katki}


# K32 DEVAM (ÖNCEDEN YAZILDI 27 Eki; ilk turda P3 dört karar hücresinin yalnız BIST 2023'te tuttu, bu üçünün sonucu görülmeden).
# Karar aynı: dört hücrede MDD >= 0,8 x P0 MDD ve getiri/|MDD| >= P0'ınki. Yuva, maliyet, dönem, çıkış FI_K32'deki gibi.
#   D1 TEMİZ ÇÖL: yalnız K29 risk işaretsiz adaylar (k29_aday 'temiz'), P3 çıkışı.
#   D2 LİKİT ÇÖL: sinyal günü 20 gün ortalama işlem değeri (kapanış x hacim) o gün pazarın üst üçte birinde olan adaylar, P3 çıkışı.
#   D3 UZUN TUT: bütün adaylar, 250 işlem günü tut (çöl ardından gelen aylarca yükselişle değerlendirilir), çıkış kuralı yok.
FI_K32_DENEME = {"likit_gun": 20, "likit_dilim": 2 / 3, "uzun": 250}


def fi_k32_likit(V: Dict[str, pd.DataFrame], K: Dict[str, Any] = FI_K32_DENEME) -> pd.DataFrame:
    """Her gün, her hissenin 20 gün ortalama işlem değerinin o günkü pazar içi yüzdelik sırası."""
    T = pd.DataFrame({s: (d.Close * d.Volume).rolling(K["likit_gun"], min_periods=K["likit_gun"]).mean() for s, d in V.items()}).sort_index()
    return T.rank(axis=1, pct=True)


def fon_izi_k32_deneme(Vb: Dict[str, pd.DataFrame], Va: Dict[str, pd.DataFrame], aday: pd.DataFrame, A: Optional[FIAyar] = None,
                       K: Dict[str, Any] = FI_K32, D: Dict[str, Any] = FI_K32_DENEME) -> Dict[str, Any]:
    """K32 devam: D1..D3 ve P0, pazar x dönem. Çıktı k32_deneme.csv."""
    A = A or FIAyar(); Z = []
    aday = aday.assign(giris=pd.to_datetime(aday.giris), sinyal=pd.to_datetime(aday.sinyal))
    for pz, V in (("BIST", Vb), ("ABD", Va)):
        mal = K["maliyet"][pz]; C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index(); L = fi_k32_likit(V, D)
        ad_p = aday[(aday.pazar == pz) & aday.sembol.isin(list(V))].sort_values(["giris", "sembol"]).copy()
        ad_p["likit"] = [L.at[r.sinyal, r.sembol] if r.sinyal in L.index else np.nan for r in ad_p.itertuples()]
        gruplar = {"D1_temiz_cikis": (ad_p[ad_p.temiz.astype(bool)], "cikis", K),
                   "D2_likit_cikis": (ad_p[ad_p.likit >= D["likit_dilim"]], "cikis", K),
                   "D3_uzun_250": (ad_p, "tut", {**K, "tut": D["uzun"]})}
        for dn, bas, bit in K["donem"]:
            Z.append({"pazar": pz, "donem": dn, "duzen": "P0_piyasa", **fi_k32_olc(fi_k32_piyasa(V, bas, bit, K))})
            for ad_, (G, kural, KK) in gruplar.items():
                gir = [(r.giris, r.sembol) for r in G[(G.giris >= bas) & (G.giris <= bit)].itertuples()]
                R = fi_k32_benzet(V, gir, kural, bas, bit, mal, KK, C=C)
                Z.append({"pazar": pz, "donem": dn, "duzen": ad_, "giris_n": len(gir), **fi_k32_olc(R.get("deger"), R.get("islem"))})
    Z = pd.DataFrame(Z); Z.to_csv(os.path.join(A.cikti, "k32_deneme.csv"), index=False)
    karar = {}
    for ad_ in ("D1_temiz_cikis", "D2_likit_cikis", "D3_uzun_250"):
        h = []
        for pz in ("BIST", "ABD"):
            for dn in ("2023", "2024-26"):
                g = Z[(Z.pazar == pz) & (Z.donem == dn)].set_index("duzen")
                h.append(bool(g.loc[ad_, "mdd"] >= 0.8 * g.loc["P0_piyasa", "mdd"] and g.loc[ad_, "getiri_mdd"] >= g.loc["P0_piyasa", "getiri_mdd"]))
        karar[ad_] = ("KULLANILABİLİR DÜZEN" if all(h) else "KULLANILABİLİR DEĞİL", h)
    return {"ozet": Z, "karar": karar}

# K33 SIÇRAYAN HİSSE PROFİLİ (Cemal 27 Eki: 'birkaç piyango gibi sıçrayan hisse ortalamayı çekiyor; o hisselerin neden ayrıştığını
# araştır, özellik belirgin olma ihtimali yüksek'). ÖNCEDEN YAZILDI (sonuç görülmeden).
# ÖRNEK: her ayın ilk işlem günü d, o gün FI_OLCUT paneline giren bütün hisseler; giriş d açılışı, r60 panelden (kriz kesiği dahil).
# ETİKET: SIÇRAMA = r60 - d günü pazar ortancası >= +%40; ÇÖKÜŞ = <= -%30 (ayna).
# ÖZELLİKLER (yalnız d-1 ve öncesi; 12 tane, kapalı konular dışında): vol60 (günlük getiri std), max20 (en büyük gün getirisi), r20,
# konum252 ((C-min)/(max-min), 252 gün), dd252 (C/max252-1), hacim_art (20g/120g hacim ortancası), likit (20g işlem değeri ortancası),
# fiyat, aralik_oran (20g ortalama (H-L)/C / 120g ortalaması: sıkışma), skew60, tavan60 (60 günde >= +%9,5 gün sayısı), yukari_hacim
# (20 günde yükselen günlerin hacim payı).
# KEŞİF 2016-10..2022-12, iki pazar ayrı: her özellik d günü kesitinde onda birliğe bölünür; uç dilim (D1 ya da D10) için sıçrama
# kaldıracı = dilimdeki sıçrama oranı / genel oran, çöküş kaldıracı aynı. SEÇİM: iki pazarda da sıçrama kaldıracı >= 1,5 VE sıçrama /
# çöküş kaldıracı >= 1,2 (yalnız oynaklık değil, yukarı eğik). TEST (2023, 2024-26): seçilen her uç dilim olay kümesi (aynı hissede 60
# işlem gününde tek) FI_OLCUT ile; KOMBİNE = seçilenlerden asimetrisi (iki pazarın küçüğü) en yüksek en çok 3'ünün işaretli sıra
# ortalaması, d günü üst onda biri. Karar fi_olcut_karar (dört hücre). Bilgi: test dönemlerinde de kaldıraçlar.
# DEVAM (iz yoksa; aynı anda önceden yazıldı, sonuçları ilk turdan bağımsız):
#   D2 ÇÖL İÇİ: yalnız K24 iki evre adayları (k29_aday) içinde, beşte birlik uç dilimler, aynı seçim/ test kuralı (kaldıraç grup içi).
#   D3 NAKİT TÜKENMESİ İÇİ (ABD): K31 M3 olayları (pist < 4 çeyrek) içinde; 12 özellik + pist, pay_yil (seyrelme); keşif 2021-22, test
#      ABD 2023 / 2024-26, beşte birlik; en çok ABD-ADAY.
#   D4 ÇÖKÜŞ PROFİLİ (kaçınma): uç onda bir dilimde iki pazarda çöküş kaldıracı >= 1,5 ve çöküş / sıçrama >= 1,2 -> fi_olcut_karar_kacinma.
FI_K33 = {"sicrama": 0.40, "cokus": -0.30, "kesif": ("2016-10-01", "2022-12-31"), "dilim": 10, "dilim_grup": 5, "kaldirac": 1.5,
          "asimetri": 1.2, "kombine_n": 3, "tavan": 0.095, "ayri": 60, "d3_kesif": ("2021-01-01", "2022-12-31"),
          "ozellik": ("vol60", "max20", "r20", "konum252", "dd252", "hacim_art", "likit", "fiyat", "aralik_oran", "skew60", "tavan60",
                      "yukari_hacim")}


def fi_k33_ozellik(d: pd.DataFrame, K: Dict[str, Any] = FI_K33) -> pd.DataFrame:
    """Bir hissenin her günü için 12 özellik; d günü satırı yalnız d-1 ve öncesini kullanır (shift(1))."""
    c, h, l, v = d.Close.astype(float), d.High.astype(float), d.Low.astype(float), d.Volume.astype(float)
    g = c.pct_change(fill_method=None)
    mx, mn = c.rolling(252, min_periods=120).max(), c.rolling(252, min_periods=120).min()
    ar = ((h - l) / c).rolling(20).mean()
    yuk = (v.where(g > 0, 0.0)).rolling(20).sum() / v.rolling(20).sum()
    F = pd.DataFrame({"vol60": g.rolling(60, min_periods=40).std(), "max20": g.rolling(20).max(), "r20": c / c.shift(20) - 1,
                      "konum252": (c - mn) / (mx - mn), "dd252": c / mx - 1,
                      "hacim_art": v.rolling(20).median() / v.rolling(120, min_periods=80).median(),
                      "likit": (c * v).rolling(20).median(), "fiyat": c, "aralik_oran": ar / ar.rolling(120, min_periods=80).mean(),
                      "skew60": g.rolling(60, min_periods=40).skew(), "tavan60": (g >= K["tavan"]).astype(float).rolling(60).sum(),
                      "yukari_hacim": yuk}, index=d.index)
    return F.replace([np.inf, -np.inf], np.nan).shift(1)


def fi_k33_satir(V: Dict[str, pd.DataFrame], P: Dict[str, Any], olay: pd.DataFrame, K: Dict[str, Any] = FI_K33) -> pd.DataFrame:
    """olay (sembol, giris, ek sütunlar): panelde olanlar; r60, fazla (r60 - giriş günü pazar ortancası), etiketler, 12 özellik."""
    ti = {x: i for i, x in enumerate(P["tarih"])}; med: Dict[int, float] = {}; tut, r60, fz = [], [], []
    for k, r in enumerate(olay.itertuples()):
        i = ti.get(pd.Timestamp(r.giris)); j = P["kol"].get(r.sembol)
        if i is None or j is None or not P["ok"][i, j]:
            continue
        if i not in med:
            med[i] = float(np.nanmedian(P["R"][i][P["ok"][i]]))
        tut.append(k); r60.append(P["R"][i, j]); fz.append(P["R"][i, j] - med[i])
    X = olay.iloc[tut].reset_index(drop=True).assign(giris=lambda x: pd.to_datetime(x.giris), r60=r60, fazla=fz)
    if not len(X):
        return X
    parca = []
    for s_, g in X.groupby("sembol"):
        F = fi_k33_ozellik(V[s_], K).reindex(g.giris)
        parca.append(pd.concat([g.reset_index(drop=True), F.reset_index(drop=True)], axis=1))
    X = pd.concat(parca, ignore_index=True)
    X["sicrama"] = X.fazla >= K["sicrama"]; X["cokus"] = X.fazla <= K["cokus"]
    return X.sort_values(["giris", "sembol"]).reset_index(drop=True)


def fi_k33_ornek(V: Dict[str, pd.DataFrame], P: Dict[str, Any], K: Dict[str, Any] = FI_K33) -> pd.DataFrame:
    """Aylık örnek: her ayın ilk panel günü, o gün panele giren bütün hisseler."""
    t = pd.Series(P["tarih"]); ilk = t.groupby(t.dt.to_period("M")).first(); ti = {x: i for i, x in enumerate(P["tarih"])}
    sat = [(P["sembol"][j], g) for g in ilk for j in np.flatnonzero(P["ok"][ti[g]]) if P["ok"][ti[g]].sum() >= 30]
    return fi_k33_satir(V, P, pd.DataFrame(sat, columns=["sembol", "giris"]), K)


def fi_k33_dilim(X: pd.DataFrame, oz: str, n: int, grup_gun: bool = True, ref: Optional[pd.Series] = None) -> pd.Series:
    """Özelliğin dilimi (0..n-1). grup_gun: her giriş günü kesitinde; değilse ref (keşif dönemi değerleri) eşikleriyle, ref yoksa
    grubun kendisiyle (keşifte). Böylece testte gelecekten eşik sızmaz."""
    def q(s: pd.Series) -> pd.Series:
        s = s.dropna()
        if len(s) < n:
            return pd.Series(np.nan, index=s.index)
        return pd.Series(pd.qcut(s.rank(method="first"), n, labels=False), index=s.index)
    if grup_gun:
        return X.groupby("giris", group_keys=False)[oz].apply(q).reindex(X.index)
    if ref is None:
        return q(X[oz]).reindex(X.index)
    kes = np.nanquantile(ref.to_numpy(float), np.linspace(0, 1, n + 1)[1:-1])
    v = X[oz].to_numpy(float)
    return pd.Series(np.where(np.isfinite(v), np.searchsorted(kes, v, side="right"), np.nan), index=X.index)


def fi_k33_kaldirac(X: pd.DataFrame, ozellikler: Tuple[str, ...], n: int, grup_gun: bool = True) -> pd.DataFrame:
    """Her özellik ve uç dilim (D1 = 0, Dn = n-1) için sıçrama / çöküş oranı ve kaldıraçları."""
    bs, bc = X.sicrama.mean(), X.cokus.mean(); Z = []
    for oz in ozellikler:
        D = fi_k33_dilim(X, oz, n, grup_gun)
        for uc, k in (("alt", 0), ("ust", n - 1)):
            m = D == k
            if m.sum() == 0:
                continue
            js, jc = X.sicrama[m].mean(), X.cokus[m].mean()
            Z.append({"ozellik": oz, "uc": uc, "n": int(m.sum()), "sicrama_oran": js, "cokus_oran": jc,
                      "sicrama_k": js / bs if bs > 0 else np.nan, "cokus_k": jc / bc if bc > 0 else np.nan})
    Z = pd.DataFrame(Z)
    if len(Z):
        Z["asimetri"] = Z.sicrama_k / Z.cokus_k
    return Z


def fi_k33_sec(Kz: Dict[str, pd.DataFrame], K: Dict[str, Any] = FI_K33, yon: str = "sicrama") -> pd.DataFrame:
    """Kz: pazar -> keşif kaldıraç tablosu. Bütün pazarlarda şartı geçen (özellik, uç); 'cokus' yönünde ayna şart."""
    birlesik = None
    for pz, Z in Kz.items():
        Z = Z.copy()
        if yon == "sicrama":
            Z["gec"] = (Z.sicrama_k >= K["kaldirac"]) & (Z.asimetri >= K["asimetri"]); Z["skor"] = Z.asimetri
        else:
            Z["gec"] = (Z.cokus_k >= K["kaldirac"]) & (1 / Z.asimetri >= K["asimetri"]); Z["skor"] = 1 / Z.asimetri
        Z = Z.set_index(["ozellik", "uc"])[["gec", "skor"]].add_suffix("_" + pz)
        birlesik = Z if birlesik is None else birlesik.join(Z, how="inner")
    if birlesik is None:
        return pd.DataFrame(columns=["ozellik", "uc", "skor"])
    gec = birlesik[[c for c in birlesik if c.startswith("gec_")]].all(axis=1)
    S = birlesik[gec].copy(); S["skor"] = S[[c for c in S if c.startswith("skor_")]].min(axis=1)
    return S.reset_index()[["ozellik", "uc", "skor"]].sort_values("skor", ascending=False).reset_index(drop=True)


def fi_k33_olay(X: pd.DataFrame, Sec: pd.DataFrame, n: int, grup_gun: bool, K: Dict[str, Any] = FI_K33,
                ref: Optional[pd.DataFrame] = None) -> Dict[str, pd.DataFrame]:
    """Seçilen her uç dilim ve KOMBİNE (en çok kombine_n özelliğin işaretli sıra ortalaması, üst dilim) için olay kümesi.
    ref: keşif satırları (grup_gun=False iken eşik ve sıra kaynağı)."""
    O: Dict[str, pd.DataFrame] = {}; isaretli = []

    def sira(oz: str) -> pd.Series:
        if grup_gun:
            return X.groupby("giris")[oz].rank(pct=True)
        r = np.sort(ref[oz].dropna().to_numpy(float)); v = X[oz].to_numpy(float)
        return pd.Series(np.where(np.isfinite(v), np.searchsorted(r, v, side="right") / max(len(r), 1), np.nan), index=X.index)
    for r in Sec.itertuples():
        D = fi_k33_dilim(X, r.ozellik, n, grup_gun, None if ref is None else ref[r.ozellik])
        O[f"{r.ozellik}_{r.uc}"] = X.loc[D == (n - 1 if r.uc == "ust" else 0), ["sembol", "giris"]]
        if len(isaretli) < K["kombine_n"]:
            rk = sira(r.ozellik); isaretli.append(rk if r.uc == "ust" else 1 - rk)
    if len(isaretli) >= 2:
        sk = pd.concat(isaretli, axis=1).mean(axis=1, skipna=False)
        if grup_gun:
            X_ = X.assign(_sk=sk).dropna(subset=["_sk"]); X_["_d"] = fi_k33_dilim(X_, "_sk", n, True)
            O["KOMBINE"] = X_.loc[X_._d == n - 1, ["sembol", "giris"]]
        else:
            O["KOMBINE"] = X.loc[sk >= 1 - 1 / n, ["sembol", "giris"]]
    return O


def fi_k33_test(Ol: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], Vs: Dict[str, Dict[str, pd.DataFrame]],
                K: Dict[str, Any] = FI_K33, O: Dict[str, Any] = FI_OLCUT) -> pd.DataFrame:
    """Ol: pazar -> {küme adı: olaylar}. Tekilleştirip FI_OLCUT hücreleri (2023, 2024-26)."""
    Z = []
    for pz, kumeler in Ol.items():
        for ad_, E in kumeler.items():
            if not len(E):
                continue
            E = E.sort_values("giris").assign(_b=True).reset_index(drop=True)
            T = fi_olcut_olay(Pn[pz], fi_k27_tekil(E, "_b", Vs[pz], K["ayri"])[["sembol", "giris"]])
            for dn, a, b in O["donem"]:
                Z.append({"kume": ad_, "pazar": pz, "donem": dn, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
    return pd.DataFrame(Z)


def fi_k33_karar(Zk: pd.DataFrame, kacinma: bool = False, yalniz_abd: bool = False, O: Dict[str, Any] = FI_OLCUT) -> str:
    """Bir kümenin hücreleri -> karar (dört hücre; yalnız ABD ise iki ABD hücresi -> ABD-ADAY)."""
    if not yalniz_abd:
        return fi_olcut_karar_kacinma(Zk, O) if kacinma else fi_olcut_karar(Zk, O)
    if kacinma:
        t = [bool(r.n >= O["n_esik"] and r.ust95 < 0 and r.sira < 0.5 and r.portfoy < r.portfoy_esli_p10) for r in Zk.itertuples()]
    else:
        t = [bool(r.n >= O["n_esik"] and r.alt95 > 0 and r.sira > 0.5 and r.portfoy > r.portfoy_esli_p90) for r in Zk.itertuples()]
    return "ABD-ADAY" if len(t) == 2 and all(t) else "İZ DEĞİL"


def fon_izi_k33(Vs: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], aday: pd.DataFrame, Fin: pd.DataFrame,
                A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K33, O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K33 sürücü: ana (aylık örnek), D2 çöl içi, D3 nakit tükenmesi içi (ABD), D4 çöküş profili. Çıktı k33_kaldirac.csv, k33_ozet.csv."""
    A = A or FIAyar(); kb, ks = pd.Timestamp(K["kesif"][0]), pd.Timestamp(K["kesif"][1]); tb = pd.Timestamp(O["donem"][0][1])
    oz = tuple(K["ozellik"]); KAL, Z, SEC = [], [], {}

    def kaldirac_kaydi(X: pd.DataFrame, calisma: str, pz: str, n: int, gg: bool, ref: Optional[pd.DataFrame], ozl: Tuple[str, ...]) -> None:
        for dn, a, b in (("kesif", K["kesif"][0], K["kesif"][1]),) + tuple(O["donem"]):
            Xd = X[(X.giris >= a) & (X.giris <= b)]
            if not len(Xd):
                continue
            if gg or dn == "kesif":
                T = fi_k33_kaldirac(Xd, ozl, n, gg)
            else:
                bs, bc = Xd.sicrama.mean(), Xd.cokus.mean(); T = []
                for o in ozl:
                    D = fi_k33_dilim(Xd, o, n, False, ref[o])
                    for uc, k in (("alt", 0), ("ust", n - 1)):
                        m = D == k
                        if m.sum():
                            T.append({"ozellik": o, "uc": uc, "n": int(m.sum()), "sicrama_oran": Xd.sicrama[m].mean(),
                                      "cokus_oran": Xd.cokus[m].mean(), "sicrama_k": Xd.sicrama[m].mean() / bs if bs else np.nan,
                                      "cokus_k": Xd.cokus[m].mean() / bc if bc else np.nan})
                T = pd.DataFrame(T)
                if len(T):
                    T["asimetri"] = T.sicrama_k / T.cokus_k
            KAL.append(T.assign(calisma=calisma, pazar=pz, donem=dn, taban_sicrama=Xd.sicrama.mean(), taban_cokus=Xd.cokus.mean()))

    # ANA + D4
    Xs = {}
    for pz in Vs:
        X = fi_k33_ornek(Vs[pz], Pn[pz], K); Xs[pz] = X
        filog.info("K33 %s: %d aylık örnek, sıçrama %.3f, çöküş %.3f", pz, len(X), X.sicrama.mean(), X.cokus.mean())
        kaldirac_kaydi(X, "ana", pz, K["dilim"], True, None, oz)
    Kz = {pz: fi_k33_kaldirac(X[(X.giris >= kb) & (X.giris <= ks)], oz, K["dilim"]) for pz, X in Xs.items()}
    for calisma, yon in (("ana", "sicrama"), ("D4_cokus", "cokus")):
        Sec = fi_k33_sec(Kz, K, yon); SEC[calisma] = Sec
        Ol = {pz: fi_k33_olay(X[X.giris >= tb], Sec, K["dilim"], True, K) for pz, X in Xs.items()}
        Zc = fi_k33_test(Ol, Pn, Vs, K, O)
        Z.append(Zc.assign(calisma=calisma) if len(Zc) else Zc)
    # D2 ÇÖL İÇİ
    Xg, Kg = {}, {}
    for pz in Vs:
        ad_ = aday[(aday.pazar == pz) & aday.sembol.isin(list(Vs[pz]))][["sembol", "giris"]]
        X = fi_k33_satir(Vs[pz], Pn[pz], ad_.assign(giris=pd.to_datetime(ad_.giris)), K); Xg[pz] = X
        ref = X[(X.giris >= kb) & (X.giris <= ks)]; Kg[pz] = fi_k33_kaldirac(ref, oz, K["dilim_grup"], False)
        kaldirac_kaydi(X, "D2_col_ici", pz, K["dilim_grup"], False, ref, oz)
    Sec = fi_k33_sec(Kg, K); SEC["D2_col_ici"] = Sec
    Ol = {pz: fi_k33_olay(X[X.giris >= tb], Sec, K["dilim_grup"], False, K, X[(X.giris >= kb) & (X.giris <= ks)]) for pz, X in Xg.items()}
    Zc = fi_k33_test(Ol, Pn, Vs, K, O); Z.append(Zc.assign(calisma="D2_col_ici") if len(Zc) else Zc)
    # D3 NAKİT TÜKENMESİ İÇİ (ABD)
    if "ABD" in Vs and len(Fin):
        Va = Vs["ABD"]; sat = []
        for r in Fin[(Fin.pist < FI_K31["pist"]) & Fin.sembol.isin(list(Va))].sort_values("filed").itertuples():
            ix = Va[r.sembol].index; j = int(ix.searchsorted(r.filed, side="right"))
            if 1 <= j < len(ix):
                sat.append({"sembol": r.sembol, "giris": ix[j], "pist": r.pist, "pay_yil": r.pay_yil})
        E = pd.DataFrame(sat).assign(_b=True)
        E = fi_k27_tekil(E.sort_values("giris").reset_index(drop=True), "_b", Va, K["ayri"]).drop(columns="_b")
        X = fi_k33_satir(Va, Pn["ABD"], E, K); oz3 = oz + ("pist", "pay_yil")
        a3, b3 = pd.Timestamp(K["d3_kesif"][0]), pd.Timestamp(K["d3_kesif"][1]); ref = X[(X.giris >= a3) & (X.giris <= b3)]
        KAL.append(fi_k33_kaldirac(ref, oz3, K["dilim_grup"], False).assign(calisma="D3_nakit_ici", pazar="ABD", donem="kesif_2021_22",
                                                                             taban_sicrama=ref.sicrama.mean(), taban_cokus=ref.cokus.mean()))
        Sec = fi_k33_sec({"ABD": fi_k33_kaldirac(ref, oz3, K["dilim_grup"], False)}, K); SEC["D3_nakit_ici"] = Sec
        Zc = fi_k33_test({"ABD": fi_k33_olay(X[X.giris >= tb], Sec, K["dilim_grup"], False, K, ref)}, Pn, Vs, K, O)
        Z.append(Zc.assign(calisma="D3_nakit_ici") if len(Zc) else Zc)
    Z = pd.concat([z for z in Z if len(z)], ignore_index=True) if any(len(z) for z in Z) else pd.DataFrame()
    KAL = pd.concat(KAL, ignore_index=True)
    karar = {}
    for (c, k), g in (Z.groupby(["calisma", "kume"]) if len(Z) else []):
        karar[f"{c}:{k}"] = fi_k33_karar(g, kacinma=c == "D4_cokus", yalniz_abd=c == "D3_nakit_ici", O=O)
    KAL.to_csv(os.path.join(A.cikti, "k33_kaldirac.csv"), index=False)
    if len(Z):
        Z.drop(columns=[c for c in Z if c.startswith("_")]).to_csv(os.path.join(A.cikti, "k33_ozet.csv"), index=False)
    return {"ozet": Z, "kaldirac": KAL, "secim": SEC, "karar": karar, "ornek": Xs}

# K33-B NAKİT TÜKENMESİ GRUBUNDA İYİ ÇIKANLARIN İZİ (Cemal 27 Eki: 'ABD nakit tükenmesi araştırmasında bazıları daha iyi çıkmıştı; iyi
# çıkanları iyi yapan izleri araştır'). ÖNCEDEN YAZILDI (K33 sonuçları görülmeden). Grup = K31 M3 olayları (ABD, nakit pisti < 4 çeyrek,
# bildirim ertesi işlem günü giriş, aynı hissede 60 işlem gününde tek). İYİ ÇIKAN = K33 SIÇRAMA (r60 - gün ortancası >= +%40).
# Özellikler = K33'ün 12 fiyat/hacim özelliği + şirket verisi (yalnız bildirimde ve d-1'de bilinen):
#   pist, pay_yil (seyrelme), piyasa_degeri (pay x C[d-1]), nakit_pd (nakit / piyasa değeri), yakma_pd (-4 x çeyreklik faaliyet nakit
#   akışı / piyasa değeri), ocf_iyilesme ((ocf - önceki bildirimin ocf'si) / |önceki ocf|, ±5 kırpılır), iceriden_alim90 (d'den önceki 90
#   günde Form 4 açık piyasa alımı var mı; veri 2022-01'den, öncesi boş).
# PROFİL: her dönemde (2021-22, 2023, 2024-26) iyi çıkanlarla ötekilerin özellik ortancası ve AUC (rastgele bir iyi çıkanın rastgele bir
# ötekinden yüksek olma olasılığı). BELİRGİN ÖZELLİK = üç dönemin hepsinde AUC >= 0,60 (ya da hepsinde <= 0,40).
# TEST: her belirgin özellik için iyi yönde uç beşte bir (eşik 2021-22 değerlerinden), iceriden_alim90 için değer 1; FI_OLCUT ABD 2023 /
# 2024-26; iki hücre tutarsa ABD-ADAY (BIST'te bu veri yok, İZ olamaz).
FI_K33B = {"auc_esik": 0.60, "kirp": 5.0, "alim_gun": 90, "alim_bas": "2022-01-01", "donem": (("2021-22", "2021-01-01", "2022-12-31"),
           ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31")),
           "sirket": ("pist", "pay_yil", "piyasa_degeri", "nakit_pd", "yakma_pd", "ocf_iyilesme", "iceriden_alim90")}


def fi_k33b_auc(x: np.ndarray, y: np.ndarray) -> float:
    """x (iyi çıkanlar) ile y (ötekiler) arasında AUC = P(x > y) + 0,5 P(x = y), sıra toplamıyla."""
    x, y = x[np.isfinite(x)], y[np.isfinite(y)]
    if len(x) < 5 or len(y) < 5:
        return np.nan
    r = pd.Series(np.concatenate([x, y])).rank().to_numpy()
    return float((r[:len(x)].sum() - len(x) * (len(x) + 1) / 2) / (len(x) * len(y)))


def fi_k33b_grup(Va: Dict[str, pd.DataFrame], P: Dict[str, Any], Fin: pd.DataFrame, alim: pd.DataFrame, K: Dict[str, Any] = FI_K33,
                 B: Dict[str, Any] = FI_K33B) -> pd.DataFrame:
    """M3 olayları + şirket özellikleri + K33 satırı (r60, fazla, sıçrama, 12 özellik)."""
    Fn = Fin[Fin.sembol.isin(list(Va))].sort_values(["sembol", "filed"]).copy()
    Fn["ocf_once"] = Fn.groupby("sembol").ocf_ceyrek.shift(1)
    sat = []
    for r in Fn[Fn.pist < FI_K31["pist"]].itertuples():
        d = Va[r.sembol]; ix = d.index; j = int(ix.searchsorted(r.filed, side="right"))
        if not 1 <= j < len(ix):
            continue
        pdg = r.pay * float(d.Close.iloc[j - 1]) if r.pay and r.pay > 0 else np.nan
        iy = (r.ocf_ceyrek - r.ocf_once) / abs(r.ocf_once) if r.ocf_once and np.isfinite(r.ocf_once) and r.ocf_once != 0 else np.nan
        sat.append({"sembol": r.sembol, "giris": ix[j], "pist": r.pist, "pay_yil": r.pay_yil, "piyasa_degeri": pdg,
                    "nakit_pd": r.nakit / pdg if pdg and pdg > 0 else np.nan,
                    "yakma_pd": -4 * r.ocf_ceyrek / pdg if pdg and pdg > 0 else np.nan,
                    "ocf_iyilesme": float(np.clip(iy, -B["kirp"], B["kirp"])) if np.isfinite(iy) else np.nan})
    E = pd.DataFrame(sat).sort_values("giris").reset_index(drop=True).assign(_b=True)
    E = fi_k27_tekil(E, "_b", Va, K["ayri"]).drop(columns="_b").reset_index(drop=True)
    al = {s_: pd.DatetimeIndex(g.D) for s_, g in alim.groupby("sembol")}; ab = pd.Timestamp(B["alim_bas"]); gun = pd.Timedelta(days=B["alim_gun"])
    E["iceriden_alim90"] = [np.nan if r.giris - gun < ab else float(((al.get(r.sembol, pd.DatetimeIndex([])) < r.giris)
                                                                      & (al.get(r.sembol, pd.DatetimeIndex([])) >= r.giris - gun)).any())
                            for r in E.itertuples()]
    return fi_k33_satir(Va, P, E, K)


def fi_k33b_profil(X: pd.DataFrame, K: Dict[str, Any] = FI_K33, B: Dict[str, Any] = FI_K33B) -> pd.DataFrame:
    """Dönem x özellik: iyi çıkan / öteki ortancası, AUC, n."""
    Z = []
    for dn, a, b in B["donem"]:
        Xd = X[(X.giris >= a) & (X.giris <= b)]
        for oz in tuple(K["ozellik"]) + tuple(B["sirket"]):
            x = Xd.loc[Xd.sicrama, oz].to_numpy(float); y = Xd.loc[~Xd.sicrama, oz].to_numpy(float)
            Z.append({"donem": dn, "ozellik": oz, "n_iyi": int(np.isfinite(x).sum()), "n_oteki": int(np.isfinite(y).sum()),
                      "iyi_ortanca": float(np.nanmedian(x)) if np.isfinite(x).any() else np.nan,
                      "oteki_ortanca": float(np.nanmedian(y)) if np.isfinite(y).any() else np.nan, "auc": fi_k33b_auc(x, y),
                      "iyi_oran": float(Xd.sicrama.mean()) if len(Xd) else np.nan})
    return pd.DataFrame(Z)


def fon_izi_k33b(Va: Dict[str, pd.DataFrame], P: Dict[str, Any], Fin: pd.DataFrame, alim: pd.DataFrame, A: Optional[FIAyar] = None,
                 K: Dict[str, Any] = FI_K33, B: Dict[str, Any] = FI_K33B, O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K33-B sürücü: profil (AUC) -> belirgin özellikler -> FI_OLCUT ABD testi. Çıktı k33b_profil.csv, k33b_ozet.csv."""
    A = A or FIAyar(); X = fi_k33b_grup(Va, P, Fin, alim, K, B); Pr = fi_k33b_profil(X, K, B)
    a0, b0 = B["donem"][0][1], B["donem"][0][2]; ref = X[(X.giris >= a0) & (X.giris <= b0)]
    belirgin = []
    for oz, g in Pr.groupby("ozellik"):
        au = g.auc.to_numpy(float)
        if len(au) == 3 and np.isfinite(au).all() and ((au >= B["auc_esik"]).all() or (au <= 1 - B["auc_esik"]).all()):
            belirgin.append((oz, "ust" if au[0] >= 0.5 else "alt"))
    kume: Dict[str, pd.DataFrame] = {}; Xt = X[X.giris >= pd.Timestamp(O["donem"][0][1])]
    for oz, uc in belirgin:
        if oz == "iceriden_alim90":
            kume[f"{oz}_{uc}"] = Xt.loc[Xt[oz] == (1.0 if uc == "ust" else 0.0), ["sembol", "giris"]]
        else:
            D = fi_k33_dilim(Xt, oz, K["dilim_grup"], False, ref[oz])
            kume[f"{oz}_{uc}"] = Xt.loc[D == (K["dilim_grup"] - 1 if uc == "ust" else 0), ["sembol", "giris"]]
    kume["HEPSI_nakit_tukenmesi"] = Xt[["sembol", "giris"]]
    Z = fi_k33_test({"ABD": kume}, {"ABD": P}, {"ABD": Va}, K, O)
    karar = {k: fi_k33_karar(g, yalniz_abd=True, O=O) for k, g in Z.groupby("kume")} if len(Z) else {}
    Pr.to_csv(os.path.join(A.cikti, "k33b_profil.csv"), index=False)
    if len(Z):
        Z.drop(columns=[c for c in Z if c.startswith("_")]).to_csv(os.path.join(A.cikti, "k33b_ozet.csv"), index=False)
    return {"grup": X, "profil": Pr, "belirgin": belirgin, "ozet": Z, "karar": karar}

# K34 BATANLAR DAHİL NAKİT TÜKENMESİ TESTİ (Cemal 27 Eki: 'batanlar da test edilsin; parmak izine o dönem uyan bütün hisseler katılsın';
# Tiingo ücretsiz hesap, anahtar .env TIINGO_TOKEN). ÖNCEDEN YAZILDI (fiyatlar inmeden, sonuç görülmeden).
# EVREN: SEC finansal tablo veri setlerinde 2021-01-01 .. 2026-06-05 arası verilen bütün 10-K / 10-Q (düzeltmeler dahil) bildirimleri;
#   OLAY = nakit pisti < 4 çeyrek VE nakit >= 1 M$ (kabuk şirketler dışarıda); giriş = bildirimden sonraki ilk işlem günü açılışı; aynı
#   şirkette 60 işlem gününde tek olay. Batanlar ayrılmaz: SEC'te o gün bildirim veren her şirket evrendedir.
# FİYAT: bugün borsa kodu olan (SEC company_tickers) şirketler Yahoo'dan (düzeltilmiş). Kodu olmayanlar (batan / çıkan / birleşen):
#   eski kod son 3 bildirimin SEC kapak sayfasından (Trading Symbol); kapakta sembol yoksa hisse işlem görmüyor demektir, dışarıda
#   (sayısı yazılır). Tiingo eşlemesi: aday kodlar [eski, eski+'Q']; Tiingo listesinde başlangıç <= şirketin ilk olayından 30 gün önce ve
#   bitiş >= son SEC bildiriminden 180 gün önce olan ilk aday geçerli (kod başka şirkete geçmişse başlangıç tarihi tutmaz). Geçerli
#   eşleşenlerden rastgele (tohum 34) en çok 450 şirket indirilir (Tiingo ücretsiz: ayda 500 sembol, saatte 50 istek); ağırlık = geçerli
#   sayısı / örnek sayısı. Eşleşmeyen sembollü şirket sayısı yazılır.
# r60 = 60. işlem günü kapanışı / giriş açılışı - 1; seri 60 günden önce biterse (borsadan çıkış) son kapanış; 31.08.2026 kesiği (pencere
#   aşarsa ve seri sürüyorsa olay ölçülmez). r60 +5'te (+%500) kırpılır (tek kuruşluk hisse sıçraması); kırpılmamış ortalama da yazılır.
# PARMAK İZİ (K33-B'nin bulduğu): piyasa değeri (SEC pay sayısı x giriş öncesi kapanış) aynı takvim çeyreğindeki olayların (ağırlıklı)
#   en küçük beşte birinde. EŞ = aynı takvim ayındaki öteki olaylar (ağırlıklı ortalama r60); fark = r60 - eş ortalaması; sıra = eşlerden
#   yüksek olma payı (ağırlıklı). Hücre: 2021-22 (bilgi), 2023, 2024-26. TUTAR: n >= 30, ağırlıklı ortalama fark > 0, ay kümeli bootstrap
#   %95 alt ucu > 0, sıra > 0,50. KARAR: 2023 ve 2024-26 tutarsa 'ABD-ADAY (batanlar dahil)', yoksa İZ DEĞİL. Yanlılık ölçüsü: aynı
#   hesap yalnız bugün kodu olanlarla (hayatta kalanlar) da yapılır.
FI_K34 = {"bas": "2021-01-01", "bit": "2026-06-05", "pist": 4.0, "nakit_min": 1e6, "ufuk": 60, "ayri": 60, "kriz": "2026-08-31",
          "orneklem": 450, "tohum": 34, "kirp": 5.0, "dilim": 5, "n_esik": 30, "bootstrap": 2000, "saat_istek": 45,
          "basla_pay": 30, "bitis_pay": 180, "klasor": os.environ.get("FI_K34", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/k34"),
          "formlar": ("10-K", "10-Q", "10-K/A", "10-Q/A"),
          "donem": (("2021-22", "2021-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31"))}


def fi_k34_env(yol: str = ".env") -> Dict[str, str]:
    """.env dosyasını okur (KEY=VALUE); değerler loglanmaz."""
    d: Dict[str, str] = {}
    try:
        for satir in open(yol, encoding="utf8"):
            satir = satir.strip()
            if satir and not satir.startswith("#") and "=" in satir:
                k, v = satir.split("=", 1); d[k.strip()] = v.strip().strip('"').strip("'")
    except OSError as e:
        filog.warning("K34: .env okunamadı (%s)", e)
    return d


def fi_k34_bildirim(klasor_fs: str) -> pd.DataFrame:
    """SEC özütleri (fs_*.csv.gz, company_tickers.json) -> bildirim başına cik, filed, form, nakit, çeyreklik faaliyet nakit akışı, pist,
    pay sayısı (bilanço > ağırlıklı ortalama > dei), bugünkü borsa kodu, şirketin son bildirim günü. fi_k31_finansal'dan farkı: kodsuz
    (batmış / çıkmış) şirketler de kalır."""
    import glob, json
    tk = json.load(open(os.path.join(klasor_fs, "company_tickers.json")))
    cs = {}
    for v in tk.values():
        cs.setdefault(str(int(v["cik_str"])), v["ticker"].upper().replace(".", "-"))
    N = pd.concat([pd.read_csv(f, dtype=str) for f in sorted(glob.glob(os.path.join(klasor_fs, "fs_*.csv.gz")))], ignore_index=True)
    N["value"] = pd.to_numeric(N.value, errors="coerce"); N["qtrs"] = pd.to_numeric(N.qtrs, errors="coerce")
    N["filed"] = pd.to_datetime(N.filed, format="%Y%m%d", errors="coerce"); N["ddate"] = pd.to_datetime(N.ddate, format="%Y%m%d", errors="coerce")
    N["cik"] = N.cik.astype(str).str.lstrip("0"); N = N.dropna(subset=["filed", "value"])
    son = N.groupby("cik").filed.max()
    oncelik = {"CommonStockSharesOutstanding": 0, "WeightedAverageNumberOfSharesOutstandingBasic": 1, "EntityCommonStockSharesOutstanding": 2}
    Pn = N[N.tag.isin(oncelik) & ((N.tag != "WeightedAverageNumberOfSharesOutstandingBasic") | (N.qtrs == 1))].copy()
    Pn["_o"] = Pn.tag.map(oncelik)
    pay = Pn.sort_values(["ddate", "_o"], ascending=[True, False]).groupby("adsh").value.last().rename("pay")
    nak = N[N.tag.isin(["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"])]
    nak = nak.sort_values(["ddate", "tag"]).groupby("adsh").value.last().rename("nakit")
    ocf = N[(N.tag == "NetCashProvidedByUsedInOperatingActivities") & (N.qtrs >= 1)]
    ocf = ocf.sort_values(["ddate", "qtrs"]).groupby("adsh").apply(lambda g: g.value.iloc[-1] / g.qtrs.iloc[-1]).rename("ocf")
    B = N.groupby("adsh").agg(cik=("cik", "first"), filed=("filed", "first"), form=("form", "first")).join(nak).join(ocf).join(pay)
    B = B.reset_index().dropna(subset=["nakit", "ocf"])
    B["pist"] = np.where(B.ocf < 0, B.nakit / (-B.ocf), np.inf); B["kod"] = B.cik.map(cs); B["son"] = B.cik.map(son)
    return B


def fi_k34_olaylar(B: pd.DataFrame, K: Dict[str, Any] = FI_K34) -> pd.DataFrame:
    """Olay bildirimleri (pist < 4, nakit >= 1 M$, dönem içi, 10-K / 10-Q)."""
    return B[B.form.isin(K["formlar"]) & (B.pist < K["pist"]) & (B.nakit >= K["nakit_min"]) & (B.filed >= K["bas"])
             & (B.filed <= K["bit"])].sort_values(["cik", "filed"]).reset_index(drop=True)


def fi_k34_tiingo_eslem(eski: pd.DataFrame, T: pd.DataFrame, olay: pd.DataFrame, K: Dict[str, Any] = FI_K34) -> pd.DataFrame:
    """eski: cik, kod (| ile çoklu). T: Tiingo supported_tickers (ticker, startDate, endDate, assetType). Şirket başına geçerli Tiingo kodu."""
    T = T[T.assetType.astype(str).str.lower() == "stock"].copy()
    T["ticker"] = T.ticker.astype(str).str.upper(); T["startDate"] = pd.to_datetime(T.startDate, errors="coerce")
    T["endDate"] = pd.to_datetime(T.endDate, errors="coerce"); Ti = T.drop_duplicates("ticker").set_index("ticker")
    ilk = olay.groupby("cik").filed.min(); son = olay.groupby("cik").son.first(); sat = []
    for r in eski.itertuples():
        kodlar = [k for k in str(r.kod).split("|") if k and k != "nan"]
        bulundu = None
        for k in kodlar:
            for aday in (k.replace(".", "-"), k.replace(".", "-") + "Q"):
                if aday in Ti.index:
                    t = Ti.loc[aday]
                    if (pd.notna(t.startDate) and t.startDate <= ilk.get(r.cik, pd.Timestamp.max) - pd.Timedelta(days=K["basla_pay"])
                            and pd.notna(t.endDate) and t.endDate >= son.get(r.cik, pd.Timestamp.min) - pd.Timedelta(days=K["bitis_pay"])):
                        bulundu = aday; break
            if bulundu:
                break
        sat.append({"cik": r.cik, "sembollu": bool(kodlar), "tiingo": bulundu})
    return pd.DataFrame(sat)


def fi_k34_tiingo_indir(kodlar: List[str], token: str, klasor: str, K: Dict[str, Any] = FI_K34) -> Dict[str, str]:
    """Tiingo günlük fiyatları (2020-10-01 .. bugün), kod başına csv; var olan atlanır; saatte en çok K['saat_istek'] istek.
    Anahtar URL'ye değil başlığa konur, loglanmaz."""
    import requests
    os.makedirs(klasor, exist_ok=True); s = requests.Session()
    s.headers.update({"Content-Type": "application/json", "Authorization": f"Token {token}"})
    durum, zaman = {}, []
    for k in kodlar:
        yol = os.path.join(klasor, f"{k}.csv")
        if os.path.exists(yol):
            durum[k] = "var"; continue
        while len(zaman) >= K["saat_istek"] and time.time() - zaman[-K["saat_istek"]] < 3600:
            time.sleep(30)
        try:
            x = s.get(f"https://api.tiingo.com/tiingo/daily/{k}/prices", params={"startDate": "2020-10-01", "format": "csv",
                      "columns": "date,open,high,low,close,volume,adjOpen,adjHigh,adjLow,adjClose,adjVolume"}, timeout=60)
            zaman.append(time.time())
            if x.status_code == 200 and x.text.startswith("date"):
                open(yol, "w").write(x.text); durum[k] = "indi"
            else:
                durum[k] = f"HTTP {x.status_code}"; filog.warning("K34 Tiingo %s: HTTP %s %s", k, x.status_code, x.text[:120])
                if x.status_code == 429:
                    time.sleep(600)
        except Exception as e:
            zaman.append(time.time()); durum[k] = f"hata {type(e).__name__}"; filog.warning("K34 Tiingo %s: %s", k, e)
        filog.info("K34 Tiingo %s: %s (%d/%d)", k, durum[k], len(durum), len(kodlar))
    return durum


def fi_k34_tiingo_oku(yol: str) -> pd.DataFrame:
    """Tiingo csv -> Open/High/Low/Close/Volume (düzeltilmiş)."""
    d = pd.read_csv(yol, parse_dates=["date"]).set_index("date").sort_index()
    d.index = d.index.tz_localize(None) if d.index.tz is not None else d.index
    return d.rename(columns={"adjOpen": "Open", "adjHigh": "High", "adjLow": "Low", "adjClose": "Close", "adjVolume": "Volume"})[
        ["Open", "High", "Low", "Close", "Volume"]]


def fi_k34_r60(d: pd.DataFrame, filed: pd.Timestamp, K: Dict[str, Any] = FI_K34) -> Tuple[Optional[pd.Timestamp], float, float, bool]:
    """Bildirimden sonraki ilk işlem günü giriş; (giriş, r60, giriş öncesi kapanış, borsadan çıkış ile bitti mi)."""
    ix = d.index; j = int(ix.searchsorted(pd.Timestamp(filed), side="right"))
    if j < 1 or j >= len(ix):
        return None, np.nan, np.nan, False
    g = float(d.Open.iloc[j]); once = float(d.Close.iloc[j - 1])
    if not (g > 0) or not np.isfinite(g):
        return ix[j], np.nan, once, False
    e = j + K["ufuk"] - 1; kriz = pd.Timestamp(K["kriz"])
    if e < len(ix):
        if ix[e] > kriz:
            return ix[j], np.nan, once, False
        return ix[j], float(d.Close.iloc[e]) / g - 1, once, False
    # seri 60 günden önce bitti: bugüne kadar sürüyorsa (henüz dolmadı) ölçülmez; eskiden bittiyse borsadan çıkış, son kapanış
    if ix[-1] >= pd.Timestamp.today().normalize() - pd.Timedelta(days=10) or ix[-1] > kriz:
        return ix[j], np.nan, once, False
    return ix[j], float(d.Close.iloc[-1]) / g - 1, once, True


def fi_k34_hucre(X: pd.DataFrame, K: Dict[str, Any] = FI_K34) -> Dict[str, Any]:
    """X: iz olayları (fark, sira, w, giris, r60). Ağırlıklı ortalama fark, ay kümeli bootstrap %95, ağırlıklı sıra."""
    X = X.dropna(subset=["fark"])
    if not len(X):
        return {"n": 0}
    w = X.w.to_numpy(float); f = X.fark.to_numpy(float); ay = X.giris.dt.to_period("M").astype(str).to_numpy(); aylar = np.unique(ay)
    rng = np.random.default_rng(K["tohum"]); grup = {a: (f[ay == a] * w[ay == a], w[ay == a]) for a in aylar}; ort = []
    for _ in range(K["bootstrap"]):
        sec = rng.choice(aylar, len(aylar), replace=True)
        ort.append(sum(grup[a][0].sum() for a in sec) / sum(grup[a][1].sum() for a in sec))
    return {"n": len(X), "n_batan": int(X.batan.sum()), "agirlik": float(w.sum()), "ort_fark": float((f * w).sum() / w.sum()),
            "alt95": float(np.quantile(ort, 0.025)), "ust95": float(np.quantile(ort, 0.975)),
            "sira": float((X.sira.to_numpy(float) * w).sum() / w.sum()), "ort_r60": float((X.r60.to_numpy(float) * w).sum() / w.sum()),
            "ort_r60_kirpilmamis": float((X.r60_ham.to_numpy(float) * w).sum() / w.sum()),
            "cikis_payi": float((X.cikis.to_numpy(float) * w).sum() / w.sum())}


def fi_k34_olc(E: pd.DataFrame, K: Dict[str, Any] = FI_K34, yanlilik: bool = True) -> Tuple[pd.DataFrame, str]:
    """E: ölçülmüş olaylar (cik, giris, r60, r60_ham, pd, w, batan, cikis). İz = çeyreklik en küçük beşte bir piyasa değeri; eş = aynı ay."""
    E = E.dropna(subset=["r60"]).copy(); E["ay"] = E.giris.dt.to_period("M"); E["ceyrek"] = E.giris.dt.to_period("Q")

    def agirlikli_dilim(g: pd.DataFrame) -> pd.Series:
        g = g.dropna(subset=["pd"]).sort_values("pd")
        c = g.w.cumsum() / g.w.sum()
        return pd.Series(c.to_numpy() <= 1 / K["dilim"] + 1e-12, index=g.index)
    E["iz"] = pd.concat([agirlikli_dilim(g) for _, g in E.groupby("ceyrek")]).reindex(E.index).fillna(False).astype(bool)
    fark, sira = np.full(len(E), np.nan), np.full(len(E), np.nan); pos = {ix: k for k, ix in enumerate(E.index)}
    for _, g in E.groupby("ay"):
        r = g.r60.to_numpy(float); w = g.w.to_numpy(float)
        for k, ix in enumerate(g.index):
            m = np.ones(len(g), bool); m[k] = False
            if w[m].sum() <= 0:
                continue
            fark[pos[ix]] = r[k] - (r[m] * w[m]).sum() / w[m].sum()
            sira[pos[ix]] = (w[m] * ((r[m] < r[k]) + 0.5 * (r[m] == r[k]))).sum() / w[m].sum()
    E["fark"], E["sira"] = fark, sira
    Z = []
    for kume, M in (("iz_batanlar_dahil", E[E.iz]), ("hepsi_batanlar_dahil", E)):
        for dn, a, b in K["donem"]:
            Z.append({"kume": kume, "donem": dn, **fi_k34_hucre(M[(M.giris >= a) & (M.giris <= b)], K)})
    # yanlılık ölçüsü: yalnız hayatta kalanlar (bugün kodu olanlar) aynı hesapla
    H = E[~E.batan].drop(columns=["iz", "fark", "sira", "ay", "ceyrek"])
    if yanlilik and len(H):
        Zh, _ = fi_k34_olc(H, K, yanlilik=False)
        Zh = Zh[Zh.kume.isin(["iz_batanlar_dahil", "hepsi_batanlar_dahil"])].copy()
        Zh["kume"] = Zh.kume.str.replace("batanlar_dahil", "yalniz_hayatta"); Z += Zh.to_dict("records")
    Z = pd.DataFrame(Z)

    def tut(r) -> bool:
        return bool(r.n >= K["n_esik"] and r.ort_fark > 0 and r.alt95 > 0 and r.sira > 0.5)
    t = Z[Z.kume == "iz_batanlar_dahil"].set_index("donem")
    karar = "ABD-ADAY (batanlar dahil)" if all(d in t.index and tut(t.loc[d]) for d in ("2023", "2024-26")) else "İZ DEĞİL"
    return Z, karar


def fi_k34_eski_kod(kodsuz: pd.DataFrame, B: pd.DataFrame, ua: str, cikti: str) -> pd.DataFrame:
    """Kodsuz şirketlerin son 3 bildiriminin SEC kapak sayfasından (R1/R2.htm) eski borsa kodu, ad, borsa. Sürdürülebilir (csv'ye ekler).
    ua: SEC kuralı gereği iletişim e-postalı User-Agent (koda / repoya yazılmaz)."""
    import requests, html as _h
    bitti = set(pd.read_csv(cikti, dtype=str).cik) if os.path.exists(cikti) else set()
    s = requests.Session(); s.headers.update({"User-Agent": ua})

    def kapak(cik: str, adsh: str) -> Tuple[List[str], List[str], List[str]]:
        for R in ("R1.htm", "R2.htm"):
            try:
                x = s.get(f"https://www.sec.gov/Archives/edgar/data/{cik}/{adsh.replace('-', '')}/{R}", timeout=30)
            except Exception as e:
                filog.warning("K34 SEC %s %s: %s", cik, R, e); time.sleep(2); continue
            time.sleep(0.15)
            if x.status_code != 200:
                continue
            t = _fi_re.sub(r"\s+", " ", _h.unescape(_fi_re.sub(r"<[^>]+>", " ", x.text)))
            m = _fi_re.findall(r"Trading Symbol\s+([A-Za-z][A-Za-z0-9.\-]{0,7})", t)
            n = _fi_re.findall(r"Entity Registrant Name\s+(.{1,80}?)\s{1,3}(?:Entity|Document|Amendment)", t)
            e = _fi_re.findall(r"Security Exchange Name\s+([A-Za-z]+)", t)
            if m or "Cover" in t[:300] or "Document and Entity" in t[:400]:
                return m, n, e
        return [], [], []
    with open(cikti, "a") as f:
        if not bitti:
            f.write("cik,adsh,kod,ad,borsa\n")
        for r in kodsuz.itertuples():
            if r.cik in bitti:
                continue
            ads = list(B[B.cik == r.cik].sort_values("filed", ascending=False).adsh.head(3)); m, n, e = [], [], []
            for a in ads:
                m, n, e = kapak(r.cik, a)
                if m:
                    break
            ad = (n[0] if n else "").replace('"', "")
            f.write(f'{r.cik},{ads[0] if ads else ""},{"|".join(dict.fromkeys(x.upper() for x in m))},"{ad}",{"|".join(dict.fromkeys(e))}\n')
            f.flush()
    return pd.read_csv(cikti, dtype=str)


def fi_k34_yahoo(kodlar: List[str], klasor: str) -> Dict[str, pd.DataFrame]:
    """Bugün kodu olan şirketlerin Yahoo günlük fiyatları (düzeltilmiş, 2020-10-01'den), 100'lük paketlerle; pickle önbellek."""
    import yfinance as yf
    yol = os.path.join(klasor, "yahoo.pkl"); V: Dict[str, pd.DataFrame] = pd.read_pickle(yol) if os.path.exists(yol) else {}
    eksik = [k for k in kodlar if k not in V]
    for i in range(0, len(eksik), 100):
        paket = eksik[i:i + 100]
        try:
            D = yf.download(paket, start="2020-10-01", auto_adjust=True, progress=False, group_by="ticker", threads=True)
        except Exception as e:
            filog.warning("K34 Yahoo paket %d: %s", i, e); continue
        for k in paket:
            try:
                d = D[k] if isinstance(D.columns, pd.MultiIndex) else D
                d = d[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
                V[k] = d if len(d) else pd.DataFrame()
            except Exception:
                V[k] = pd.DataFrame()
        pd.to_pickle(V, yol); filog.info("K34 Yahoo %d/%d", min(i + 100, len(eksik)), len(eksik))
    return V


def fon_izi_k34(klasor_fs: str, eski: pd.DataFrame, T: pd.DataFrame, A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K34,
                token: Optional[str] = None, indir: bool = True) -> Dict[str, Any]:
    """K34 sürücü: SEC olayları -> eşleme -> örneklem -> fiyatlar (Yahoo + Tiingo) -> r60 -> iz / eş ölçüsü. Çıktı k34_ozet.csv, k34_olay.csv."""
    A = A or FIAyar(); os.makedirs(K["klasor"], exist_ok=True)
    B = fi_k34_bildirim(klasor_fs); O = fi_k34_olaylar(B, K)
    es = fi_k34_tiingo_eslem(eski[eski.cik.isin(O[O.kod.isna()].cik)], T, O, K)
    gecerli = es[es.tiingo.notna()].sort_values("cik").reset_index(drop=True)
    rng = np.random.default_rng(K["tohum"]); n_s = min(K["orneklem"], len(gecerli))
    ornek = gecerli.iloc[np.sort(rng.choice(len(gecerli), n_s, replace=False))] if n_s else gecerli
    w_batan = len(gecerli) / n_s if n_s else 0.0
    sayim = {"olay": len(O), "sirket": O.cik.nunique(), "kodlu_sirket": O[O.kod.notna()].cik.nunique(),
             "kodsuz_sirket": O[O.kod.isna()].cik.nunique(), "kodsuz_sembollu": int(es.sembollu.sum()),
             "kodsuz_sembolsuz": int((~es.sembollu).sum()), "tiingo_gecerli": len(gecerli), "orneklem": n_s, "batan_agirlik": w_batan}
    filog.info("K34 sayım: %s", sayim)
    tk = token or os.environ.get("TIINGO_TOKEN") or fi_k34_env().get("TIINGO_TOKEN")
    if indir:
        if not tk:
            raise RuntimeError("K34: TIINGO_TOKEN yok (.env)")
        fi_k34_tiingo_indir(list(ornek.tiingo), tk, os.path.join(K["klasor"], "tiingo"), K)
    Vy = fi_k34_yahoo(sorted(O.kod.dropna().unique()), K["klasor"]) if indir else pd.read_pickle(os.path.join(K["klasor"], "yahoo.pkl"))
    seri: Dict[str, Tuple[pd.DataFrame, bool, float]] = {}
    for r in ornek.itertuples():
        yol = os.path.join(K["klasor"], "tiingo", f"{r.tiingo}.csv")
        if os.path.exists(yol):
            seri[r.cik] = (fi_k34_tiingo_oku(yol), True, w_batan)
    for cik, kod in O[O.kod.notna()].groupby("cik").kod.first().items():
        d = Vy.get(kod)
        if d is not None and len(d):
            seri[cik] = (d, False, 1.0)
    sat = []
    for cik, g in O.groupby("cik"):
        if cik not in seri:
            continue
        d, batan, w = seri[cik]; son_i = -10 ** 9
        for r in g.itertuples():
            giris, r60, once, cikis = fi_k34_r60(d, r.filed, K)
            if giris is None:
                continue
            i = int(d.index.get_loc(giris))
            if i - son_i < K["ayri"]:
                continue
            son_i = i
            sat.append({"cik": cik, "kod": r.kod, "filed": r.filed, "giris": giris, "r60_ham": r60,
                        "r60": min(r60, K["kirp"]) if np.isfinite(r60) else np.nan,
                        "pd": r.pay * once if r.pay and r.pay > 0 and np.isfinite(once) else np.nan, "pist": r.pist,
                        "batan": batan, "w": w, "cikis": cikis})
    E = pd.DataFrame(sat)
    Z, karar = fi_k34_olc(E, K)
    Z.to_csv(os.path.join(A.cikti, "k34_ozet.csv"), index=False)
    E.to_csv(os.path.join(K["klasor"], "k34_olay.csv"), index=False)
    return {"ozet": Z, "karar": karar, "sayim": sayim, "olay": E}

# K35 RÜZGÂR BATANLARI AYIRIR MI (Cemal 28 Eki: 'nakdi yetmeyen, batan şirketlerin arkasında rüzgâr olanlar da batıyor mu bakılmalı;
# rüzgâra göre alım yapacağım; rüzgârı olan daha iyi mi; BIST'te tekstil batıyor, güneş enerjisi kolay batmaz'). Sektör rüzgârı
# CLAUDE.md'de kapalı konu 'sektör ısısı'na dokunur; Cemal kendisi istedi. ÖNCEDEN YAZILDI (sonuç görülmeden).
# EVREN: K34 olayları (ABD, nakdi 4 çeyrekten kısa yeten, nakdi >= 1 M$, 2021-01 .. 2026-06, batanlar dahil). SEKTÖR = SEC SIC kodu
#   (batanlar dahil herkeste var): ilk 3 hane, fiyat evreninde o 3 haneden < 8 şirket varsa ilk 2 hane.
# RÜZGÂR = üretimdeki D9b tanımı (COL_v1, fi_k14_ruzgar): aynı sektör sepeti (hisse hariç) 60 gün ortalama getirisi - piyasa ortancası
#   >= +%10 VE sepet > 0, üye >= 4; girişten önceki son işlem günü. Sepet / piyasa evreni: V_ABD + K34 fiyatları (Yahoo + Tiingo).
# Ö1 BATMA: bildirimden sonra 730 gün içinde SEC bildirimi kesildi mi (birleşme / satın alma da 'kesilme' sayılır; ayrılamıyor).
#   Kohortlar: 2021-22 ve 2023-01 .. 2024-06 (2 yıl gözlenebilsin); şirket başına kohortta ilk olay; fiyat gerekmez, bütün sembollü
#   şirketler (Tiingo örneğine girmeyen batanlar dahil). Oran = batma(rüzgârlı) / batma(rüzgârsız), şirketlerden bootstrap %95.
#   'RÜZGÂR BATMAYI AZALTIR' = iki kohortta da oran <= 0,8 ve üst uç < 1. Aynısı en küçük beşte bir nakit dilimi içinde (bilgi).
# Ö2 GETİRİ: K34 ölçüsü (aynı ay nakdi biten eşlere fark, ağırlıklı, batanlar dahil). Kümeler: R = rüzgârlı; RK = rüzgârlı ve en küçük
#   beşte bir piyasa değeri (K34 izi). Hücre 2023 / 2024-26, K34 kuralı (n >= 30, fark > 0, alt uç > 0, sıra > 0,50) -> ABD-ADAY.
# BİLGİ: SIC ana grup (2 hane) başına batma oranı (2021-22 kohortu), n >= 30 gruplar.
FI_K35 = {"sic_min": 8, "batma_gun": 730, "kohort": (("2021-22", "2021-01-01", "2022-12-31"), ("2023-24", "2023-01-01", "2024-06-30")),
          "oran_esik": 0.8, "bootstrap": 2000, "tohum": 35, "grup_n": 30}


def fi_k35_sektor(sic: pd.Series, evren_sic: pd.Series, K: Dict[str, Any] = FI_K35) -> pd.Series:
    """SIC -> sektör kodu: 3 hane; fiyat evreninde (evren_sic) o 3 haneden < sic_min şirket varsa 2 hane. Boş SIC -> NaN."""
    s3 = sic.astype(str).str.zfill(4).str[:3].where(sic.notna() & (sic.astype(str).str.len() > 0))
    say = evren_sic.dropna().astype(str).str.zfill(4).str[:3].value_counts()
    az = s3.map(say).fillna(0) < K["sic_min"]
    return s3.where(~az, "G" + s3.str[:2])


def fi_k35_batma(Ol: pd.DataFrame, K: Dict[str, Any] = FI_K35) -> pd.DataFrame:
    """Ol: cik, filed, son, ruzgar, kucuk (bool). Kohort x küme: rüzgârlı / rüzgârsız batma oranı, oran, şirket bootstrap %95."""
    rng = np.random.default_rng(K["tohum"]); Z = []
    for kh, a, b in K["kohort"]:
        X = Ol[(Ol.filed >= a) & (Ol.filed <= b)].sort_values("filed").groupby("cik").head(1).dropna(subset=["ruzgar"])
        X = X.assign(batti=(X.son < X.filed + pd.Timedelta(days=K["batma_gun"])).astype(float))
        for kume, M in (("hepsi", X), ("en_kucuk_nakit", X[X.kucuk])):
            r = M[M.ruzgar.astype(bool)].batti.to_numpy(); y = M[~M.ruzgar.astype(bool)].batti.to_numpy()
            if len(r) < 10 or len(y) < 10:
                Z.append({"kohort": kh, "kume": kume, "n_ruzgarli": len(r), "n_ruzgarsiz": len(y)}); continue
            bs = [rng.choice(r, len(r)).mean() / max(rng.choice(y, len(y)).mean(), 1e-9) for _ in range(K["bootstrap"])]
            Z.append({"kohort": kh, "kume": kume, "n_ruzgarli": len(r), "n_ruzgarsiz": len(y), "batma_ruzgarli": r.mean(),
                      "batma_ruzgarsiz": y.mean(), "oran": r.mean() / y.mean() if y.mean() > 0 else np.nan,
                      "alt95": float(np.quantile(bs, 0.025)), "ust95": float(np.quantile(bs, 0.975))})
    return pd.DataFrame(Z)


def fi_k35_esfark(E: pd.DataFrame) -> pd.DataFrame:
    """K34 eş farkı (aynı takvim ayındaki öteki olayların ağırlıklı ortalaması) ve ağırlıklı sıra; E'ye fark, sira ekler."""
    E = E.dropna(subset=["r60"]).copy(); E["ay"] = E.giris.dt.to_period("M")
    fark, sira = pd.Series(np.nan, index=E.index), pd.Series(np.nan, index=E.index)
    for _, g in E.groupby("ay"):
        r = g.r60.to_numpy(float); w = g.w.to_numpy(float)
        for k, ix in enumerate(g.index):
            m = np.ones(len(g), bool); m[k] = False
            if w[m].sum() > 0:
                fark[ix] = r[k] - (r[m] * w[m]).sum() / w[m].sum()
                sira[ix] = (w[m] * ((r[m] < r[k]) + 0.5 * (r[m] == r[k]))).sum() / w[m].sum()
    E["fark"], E["sira"] = fark, sira
    return E


def fon_izi_k35(E34: pd.DataFrame, B: pd.DataFrame, eski: pd.DataFrame, sic: pd.DataFrame, fiyat: Dict[str, pd.DataFrame],
                A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K35, K34: Dict[str, Any] = FI_K34) -> Dict[str, Any]:
    """K35 sürücü. E34: K34 ölçülmüş olaylar; B: SEC bildirimleri (fi_k34_bildirim); eski: kodsuzların eski kodu; sic: cik, sic, sic_ad;
    fiyat: {cik: günlük fiyat} (sepet / piyasa evreni). Çıktı k35_batma.csv, k35_getiri.csv, k35_sektor_batma.csv."""
    A = A or FIAyar()
    sic = sic.assign(cik=sic.cik.astype(str), sic=pd.to_numeric(sic.sic, errors="coerce").astype("Int64").astype(str).replace("<NA>", np.nan))
    sek = fi_k35_sektor(sic.set_index("cik").sic, sic[sic.cik.isin(list(fiyat))].sic, K).dropna().to_dict()
    W = fi_k14_ruzgar(fiyat, sek); ti = W.index

    def ruz(cik: str, gun: pd.Timestamp) -> float:
        if cik not in W.columns or cik not in sek:
            return np.nan
        j = int(ti.searchsorted(pd.Timestamp(gun), side="left")) - 1
        return float(W[cik].iloc[j]) if j >= 0 else np.nan
    # Ö1 batma: bütün sembollü olaylar (kodlu + kodsuz sembollü), fiyat gerekmez; olay günü = bildirim ertesi
    O = fi_k34_olaylar(B, K34); semb = set(eski[eski.kod.fillna("").astype(str).str.len() > 0].cik)
    Ol = O[O.kod.notna() | O.cik.isin(semb)].copy()
    Ol["ruzgar"] = [ruz(c, f) if c in sek else np.nan for c, f in zip(Ol.cik, Ol.filed + pd.Timedelta(days=1))]
    if any(c not in W.columns for c in Ol.cik.unique()):
        # sepette fiyatı olmayan şirket: rüzgârı sektör sepetinin kendisinden (hisse hariç tutulacak fiyat yok) aynı tanımla
        C = pd.DataFrame({c: d.Close for c, d in fiyat.items()}).sort_index().ffill(limit=5); r = C / C.shift(60) - 1; piy = r.median(axis=1)
        gr: Dict[str, List[str]] = {}
        for c in r.columns:
            if c in sek:
                gr.setdefault(sek[c], []).append(c)
        sep = {g: (r[u].mean(axis=1), r[u].notna().sum(axis=1)) for g, u in gr.items()}
        eks = Ol.ruzgar.isna() & Ol.cik.isin([c for c in sek if c not in W.columns])
        v = []
        for c, f in zip(Ol.loc[eks, "cik"], Ol.loc[eks, "filed"] + pd.Timedelta(days=1)):
            g = sek.get(c); j = int(r.index.searchsorted(pd.Timestamp(f), side="left")) - 1
            if g not in sep or j < 0:
                v.append(np.nan); continue
            m, n = sep[g][0].iloc[j], sep[g][1].iloc[j]
            v.append(float(n >= FI_K14_ESIK["ruz_uye"] and m > 0 and m - piy.iloc[j] >= FI_K14_ESIK["ruz"]))
        Ol.loc[eks, "ruzgar"] = v
    Ol["kucuk"] = Ol.groupby(Ol.filed.dt.to_period("Q")).nakit.transform(lambda x: x <= x.quantile(0.2))
    Zb = fi_k35_batma(Ol, K)
    # bilgi: SIC ana grup batma oranı (2021-22 kohortu)
    a, b = K["kohort"][0][1], K["kohort"][0][2]
    X = Ol[(Ol.filed >= a) & (Ol.filed <= b)].sort_values("filed").groupby("cik").head(1).copy()
    X["batti"] = X.son < X.filed + pd.Timedelta(days=K["batma_gun"])
    sad = sic.set_index("cik"); X["sic2"] = X.cik.map(sad.sic).astype(str).str.zfill(4).str[:2]; X["ornek_ad"] = X.cik.map(sad.sic_ad)
    Zs = X.groupby("sic2").agg(n=("cik", "size"), batma=("batti", "mean"), ornek=("ornek_ad", lambda x: x.mode().iat[0] if len(x.mode()) else ""))
    Zs = Zs[Zs.n >= K["grup_n"]].sort_values("batma")
    # Ö2 getiri
    E = fi_k35_esfark(E34.assign(giris=pd.to_datetime(E34.giris), cik=E34.cik.astype(str)))
    E["ruzgar"] = [ruz(c, g) for c, g in zip(E.cik, E.giris)]
    E["ceyrek"] = E.giris.dt.to_period("Q")

    def kucuk(g: pd.DataFrame) -> pd.Series:
        g = g.dropna(subset=["pd"]).sort_values("pd"); c = g.w.cumsum() / g.w.sum()
        return pd.Series(c.to_numpy() <= 0.2 + 1e-12, index=g.index)
    E["iz"] = pd.concat([kucuk(g) for _, g in E.groupby("ceyrek")]).reindex(E.index).fillna(False).astype(bool)
    Zg = []
    R = E[E.ruzgar == 1.0]
    for kume, M in (("R_ruzgarli", R), ("RK_ruzgarli_kucuk", R[R.iz]), ("K_ruzgarsiz_kucuk", E[(E.ruzgar == 0.0) & E.iz])):
        for dn, a_, b_ in K34["donem"]:
            Zg.append({"kume": kume, "donem": dn, **fi_k34_hucre(M[(M.giris >= a_) & (M.giris <= b_)], K34)})
    Zg = pd.DataFrame(Zg)

    def tut(r) -> bool:
        return bool(r.n >= K34["n_esik"] and r.ort_fark > 0 and r.alt95 > 0 and r.sira > 0.5)
    karar = {}
    for kume in ("R_ruzgarli", "RK_ruzgarli_kucuk"):
        t = Zg[Zg.kume == kume].set_index("donem")
        karar[kume] = "ABD-ADAY (batanlar dahil)" if all(d in t.index and tut(t.loc[d]) for d in ("2023", "2024-26")) else "İZ DEĞİL"
    h = Zb[Zb.kume == "hepsi"]
    karar["batma"] = ("RÜZGÂR BATMAYI AZALTIR" if len(h) == 2 and h.oran.notna().all() and (h.oran <= K["oran_esik"]).all()
                      and (h.ust95 < 1).all() else "AYIRMIYOR")
    Zb.to_csv(os.path.join(A.cikti, "k35_batma.csv"), index=False); Zg.to_csv(os.path.join(A.cikti, "k35_getiri.csv"), index=False)
    Zs.reset_index().to_csv(os.path.join(A.cikti, "k35_sektor_batma.csv"), index=False)
    return {"batma": Zb, "getiri": Zg, "sektor": Zs, "karar": karar, "olay_batma": Ol, "olay_getiri": E, "ruzgar": W}

# K35-C PATLAYANLARIN ARKASINDA RÜZGÂR (Cemal 28 Eki: 'patlayanların arkasında rüzgâr var mıydı, patlama zamanında rüzgâr var mıydı').
# ÖNCEDEN YAZILDI (K35 sonuçları görülmeden). Olaylar = K34 ölçülmüş olaylar (batanlar dahil, ağırlıklı). PATLAYAN = aynı ay eşlerine
# fark >= +%40 (K33 sıçrama eşiği). Rüzgâr (D9b, sepette hisse hariç, yani hissenin kendi sıçraması rüzgâr yaratmaz):
#   GİRİŞTE = girişten önceki son işlem günü; ZİRVEDE = 60 günlük penceredeki en yüksek kapanış günü (patlama zamanı). Aynı iki ölçü
#   patlamayanlarda da (onların penceresindeki en yüksek kapanış günü) alınır.
# Ölçü: dönem (2021-22, 2023, 2024-26) başına rüzgârlı payı patlayan / öteki ve oran (kaldıraç), şirketlerden bootstrap %95.
#   'PATLAMA ANINDA RÜZGÂR' = üç dönemde de zirve oranı >= 1,5 ve alt uç > 1. 'GİRİŞTE RÜZGÂR PATLAMAYI ÖNCELER' = 2023 ve 2024-26'da
#   giriş oranı >= 1,5 ve alt uç > 1 (alınabilir bilgi; değilse rüzgâr patlamanın sebebi değil, eşlikçisi).
FI_K35C = {"patlama": 0.40, "kaldirac": 1.5}


def fi_k35_zirve(d: pd.DataFrame, giris: pd.Timestamp, ufuk: int = 60) -> Optional[pd.Timestamp]:
    """Giriş gününden itibaren ufuk işlem günündeki en yüksek kapanış günü (seri erken biterse var olan kısım)."""
    if d is None or not len(d) or pd.Timestamp(giris) not in d.index:
        return None
    j = int(d.index.get_loc(pd.Timestamp(giris))); p = d.Close.iloc[j:j + ufuk]
    return p.idxmax() if len(p) and p.notna().any() else None


def fon_izi_k35c(E: pd.DataFrame, W: pd.DataFrame, fiyat: Dict[str, pd.DataFrame], A: Optional[FIAyar] = None,
                 K: Dict[str, Any] = FI_K35, C: Dict[str, Any] = FI_K35C, K34: Dict[str, Any] = FI_K34) -> Dict[str, Any]:
    """E: fi_k35_esfark çıktısı (cik, giris, fark, w); W: rüzgâr paneli (fi_k14_ruzgar, sütun cik). Çıktı k35c_patlama.csv."""
    A = A or FIAyar(); ti = W.index

    def ruz(cik: str, gun: Optional[pd.Timestamp], once: bool) -> float:
        if gun is None or cik not in W.columns:
            return np.nan
        j = int(ti.searchsorted(pd.Timestamp(gun), side="left")) - (1 if once else 0)
        if not once and (j >= len(ti) or ti[j] != pd.Timestamp(gun)):
            j -= 1
        return float(W[cik].iloc[j]) if 0 <= j < len(ti) else np.nan
    E = E.dropna(subset=["fark"]).copy(); E["patlayan"] = E.fark >= C["patlama"]
    E["zirve"] = [fi_k35_zirve(fiyat.get(c), g) for c, g in zip(E.cik, E.giris)]
    E["ruz_giris"] = [ruz(c, g, True) for c, g in zip(E.cik, E.giris)]
    E["ruz_zirve"] = [ruz(c, z, False) for c, z in zip(E.cik, E.zirve)]
    rng = np.random.default_rng(K["tohum"]); Z = []
    for dn, a, b in K34["donem"]:
        X = E[(E.giris >= a) & (E.giris <= b)]
        for ol in ("ruz_giris", "ruz_zirve"):
            Y = X.dropna(subset=[ol])
            if not len(Y) or Y.patlayan.sum() < 10:
                Z.append({"donem": dn, "olcu": ol, "n_patlayan": int(Y.patlayan.sum()) if len(Y) else 0}); continue

            def pay(T: pd.DataFrame) -> Tuple[float, float, float]:
                p, o = T[T.patlayan], T[~T.patlayan]
                pp = (p[ol] * p.w).sum() / p.w.sum(); oo = (o[ol] * o.w).sum() / o.w.sum()
                return pp, oo, pp / oo if oo > 0 else np.nan
            pp, oo, kd = pay(Y); sirket = Y.cik.unique(); gi = {c: g.index for c, g in Y.groupby("cik")}; bs = []
            for _ in range(K["bootstrap"]):
                sec = rng.choice(sirket, len(sirket)); T = Y.loc[np.concatenate([gi[c] for c in sec])]
                if T.patlayan.any() and (~T.patlayan).any():
                    bs.append(pay(T)[2])
            Z.append({"donem": dn, "olcu": ol, "n_patlayan": int(Y.patlayan.sum()), "n_oteki": int((~Y.patlayan).sum()),
                      "ruzgarli_pay_patlayan": pp, "ruzgarli_pay_oteki": oo, "oran": kd,
                      "alt95": float(np.nanquantile(bs, 0.025)), "ust95": float(np.nanquantile(bs, 0.975)),
                      "patlama_orani_ruzgarli": float((Y[Y[ol] == 1].patlayan * Y[Y[ol] == 1].w).sum() / max(Y[Y[ol] == 1].w.sum(), 1e-9)),
                      "patlama_orani_ruzgarsiz": float((Y[Y[ol] == 0].patlayan * Y[Y[ol] == 0].w).sum() / max(Y[Y[ol] == 0].w.sum(), 1e-9))})
    Z = pd.DataFrame(Z)

    def gec(dn: str, ol: str) -> bool:
        r = Z[(Z.donem == dn) & (Z.olcu == ol)]
        return bool(len(r) and pd.notna(r.oran.iat[0]) and r.oran.iat[0] >= C["kaldirac"] and r.alt95.iat[0] > 1)
    karar = {"zirvede": "PATLAMA ANINDA RÜZGÂR VAR" if all(gec(d[0], "ruz_zirve") for d in K34["donem"]) else "AYIRMIYOR",
             "giriste": "GİRİŞTE RÜZGÂR PATLAMAYI ÖNCELER" if all(gec(d, "ruz_giris") for d in ("2023", "2024-26")) else "AYIRMIYOR"}
    Z.to_csv(os.path.join(A.cikti, "k35c_patlama.csv"), index=False)
    return {"ozet": Z, "karar": karar, "olay": E}

# K36 RÜZGÂRIN SEBEBİ (Cemal 28 Eki: 'rüzgâr fiyattan görülünce geç kalınır; 1 ile başla, sebebe bak'). Kapalı konu 'sektör ısısı' ve
# 'VIX/DXY'ye komşu; Cemal istedi (DXY kullanılmaz, kur USDTRY / EURUSD). ÖNCEDEN YAZILDI (sürücü verisi inmeden, sonuç görülmeden).
# SEBEP -> SEKTÖR eşlemesi (iktisadi mantıkla önceden; ABD endüstri adları sektor_ABD.csv, BIST alt endeksler sektor_BIST.csv):
#   BIST: XBANK, XGMYO <- Türkiye CDS DÜŞER (cds_2022.csv; 2022'den); XMADN <- altın YÜKSELİR (GC=F); XTEKS <- USDTRY YÜKSELİR (ihracatçı);
#         XMANA <- sıcak haddelenmiş çelik YÜKSELİR (HRC=F); XULAS <- petrol DÜŞER (CL=F).
#   ABD:  Gold <- altın; Silver <- gümüş (SI=F); Oil & Gas E&P, Oil & Gas Equipment & Services <- petrol YÜKSELİR; Airlines <- petrol DÜŞER;
#         Steel <- HRC YÜKSELİR; Copper, Other Industrial Metals & Mining <- bakır YÜKSELİR (HG=F); Aluminum <- ALI=F YÜKSELİR;
#         Agricultural Inputs <- buğday YÜKSELİR (ZW=F); Banks - Regional <- ABD 10 yıllık faiz YÜKSELİR (^TNX, ders kitabı: faiz marjı);
#         REIT - * (hepsi), Residential Construction, Utilities - Regulated Electric, Biotechnology, Solar <- 10 yıllık faiz DÜŞER.
#   Teşvik / yasa gibi sayısallaşmayan sebepler (güneş enerjisi teşviki) bu turda yok; Solar yalnız faizle.
# SEBEP SİNYALİ: sürücünün 20 günlük log değişimi (CDS ve 'düşer' sürücülerde işaret ters) son 250 günün 20 günlük değişimlerine göre
#   z-skor (pencere d-1'e kadar, geleceğe bakmaz); sinyal günü = z >= 1,0'a geçiş (önceki gün < 1,0). Aralık kuralı yok: gürültü
#   geçişinden hemen sonra gelen gerçek hareket yutulmasın (sonuç görülmeden, test 47 ile fark edildi); hisse başına 60 günde tek olay.
# Ö1 ÖNCELİK (sebep rüzgârdan önce mi gelir): sinyal günü d'de sektörün fiyat rüzgârı (D9b, fi_k14_ruzgar; sektör üyesi hisselerin
#   çoğunluğu rüzgârlı) VAR mı; yoksa sonraki 60 işlem gününde çıkıyor mu. Taban = rüzgârsız rastgele günlerden sonraki 60 günde rüzgâr
#   çıkma oranı (aynı sektör). ÖNCÜ ORANI = P(60 günde rüzgâr | sinyal, d'de rüzgâr yok) / taban. 'SEBEP ÖNCE GELİR' = iki pazarda da
#   öncü oranı >= 1,5 ve sinyalde zaten rüzgârlı payı < %50 (2016-26 birleşik; BIST CDS çiftleri 2022'den).
# Ö2 GETİRİ (FI_OLCUT, dört hücre): olay = sektör üyesi hisse, giriş = sinyal gününden sonraki ilk açılış, aynı hissede 60 günde tek.
#   Kümeler: HEPSİ; ERKEN = sinyal günü sektörde fiyat rüzgârı henüz yok (Cemal'in sorusu: rüzgâr görünmeden binmek); ERKEN+ÇÖL = ERKEN ve
#   hisse K23 çöl süzgecinde (düşüş <= -%30, eğim >= -0,001, mum <= 1,0, 20 bar, sinyal gününde). Karar fi_olcut_karar; bilgi: sürücü başına.
# Hayatta kalma: V_BIST / V_ABD bugün işlem görenler (K34 notu); sektör sepetleri de öyle. ABD petrol / biyoteknoloji gibi sektörlerde
#   iyimserlik payı var, kayda yazılır.
FI_K36 = {"z_pencere": 20, "z_gecmis": 250, "z_esik": 1.0, "ruz_bekle": 60, "oncu_esik": 1.5, "zaten_esik": 0.5, "coğunluk": 0.5,
          "ayri_hisse": 60, "tohum": 36, "taban_n": 2000, "cds": "cds_2022.csv",
          "surucu": {"GC=F": "altın", "SI=F": "gümüş", "CL=F": "petrol", "HG=F": "bakır", "ZW=F": "buğday", "HRC=F": "çelik",
                     "ALI=F": "alüminyum", "USDTRY=X": "USDTRY", "^TNX": "ABD10y", "CDS": "TR_CDS"},
          "esleme": {"BIST": [("XBANK", "CDS", -1), ("XGMYO", "CDS", -1), ("XMADN", "GC=F", 1), ("XTEKS", "USDTRY=X", 1),
                              ("XMANA", "HRC=F", 1), ("XULAS", "CL=F", -1)],
                     "ABD": [("Gold", "GC=F", 1), ("Silver", "SI=F", 1), ("Oil & Gas E&P", "CL=F", 1),
                             ("Oil & Gas Equipment & Services", "CL=F", 1), ("Airlines", "CL=F", -1), ("Steel", "HRC=F", 1),
                             ("Copper", "HG=F", 1), ("Other Industrial Metals & Mining", "HG=F", 1), ("Aluminum", "ALI=F", 1),
                             ("Agricultural Inputs", "ZW=F", 1), ("Banks - Regional", "^TNX", 1), ("REIT - *", "^TNX", -1),
                             ("Residential Construction", "^TNX", -1), ("Utilities - Regulated Electric", "^TNX", -1),
                             ("Biotechnology", "^TNX", -1), ("Solar", "^TNX", -1)]},
          "klasor": os.environ.get("FI_K36", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/k36")}


def fi_k36_surucu_indir(K: Dict[str, Any] = FI_K36, kok: Optional[str] = None) -> Dict[str, pd.Series]:
    """Sürücü serileri: Yahoo (kapanış, 2015'ten) + repo cds_2022.csv. Pickle önbellek K['klasor']/surucu.pkl."""
    import yfinance as yf
    os.makedirs(K["klasor"], exist_ok=True); yol = os.path.join(K["klasor"], "surucu.pkl")
    if os.path.exists(yol):
        return pd.read_pickle(yol)
    kok = kok or os.path.dirname(os.path.abspath(__file__)); S: Dict[str, pd.Series] = {}
    for t in K["surucu"]:
        if t == "CDS":
            c = pd.read_csv(os.path.join(kok, K["cds"]), parse_dates=["date"]).set_index("date").price.astype(float)
            S[t] = c.sort_index(); continue
        try:
            d = yf.download(t, start="2015-01-01", progress=False, auto_adjust=False)
            s = d["Close"] if "Close" in d else d.xs("Close", axis=1, level=0)
            s = s.iloc[:, 0] if isinstance(s, pd.DataFrame) else s
            S[t] = s.dropna().astype(float); S[t].index = pd.DatetimeIndex(S[t].index).tz_localize(None)
        except Exception as e:
            filog.warning("K36 sürücü %s inmedi: %s", t, e)
    pd.to_pickle(S, yol)
    return S


def fi_k36_sinyal(s: pd.Series, yon: int, K: Dict[str, Any] = FI_K36) -> pd.Series:
    """Sürücü sinyal günleri (bool, sürücü takvimi): 20 günlük log değişimi x yön, son 250 günün (d-1'e kadar) z-skoru >= z_esik'e geçiş."""
    s = s[s > 0].dropna().sort_index(); x = np.log(s).diff(K["z_pencere"]) * yon
    mu = x.rolling(K["z_gecmis"], min_periods=120).mean().shift(1); sd = x.rolling(K["z_gecmis"], min_periods=120).std().shift(1)
    z = (x - mu) / sd
    return ((z >= K["z_esik"]) & (z.shift(1) < K["z_esik"])).fillna(False)


def fi_k36_sektor_ruzgar(W: pd.DataFrame, uyeler: List[str], K: Dict[str, Any] = FI_K36) -> pd.Series:
    """Sektör düzeyinde rüzgâr (bool, gün): üyelerin (hisse hariç sepetle ölçülen) rüzgârlı payı > çoğunluk."""
    u = [s for s in uyeler if s in W.columns]
    return (W[u].mean(axis=1) > K["coğunluk"]) if u else pd.Series(False, index=W.index)


def fi_k36_uyeler(sek: Dict[str, str], ad: str) -> List[str]:
    """Eşlemedeki sektör adı -> üyeler; 'REIT - *' gibi yıldızlı ad önekle eşleşir."""
    if ad.endswith("*"):
        on = ad[:-1]; return [s for s, a in sek.items() if a.startswith(on)]
    return [s for s, a in sek.items() if a == ad]


def fi_k36_oncelik(G: pd.Series, sinyal_gun: List[pd.Timestamp], rng: np.random.Generator, K: Dict[str, Any] = FI_K36) -> Dict[str, Any]:
    """Bir sektör-sürücü çifti: sinyal günlerinde rüzgâr zaten var mı; yoksa 60 günde çıkıyor mu; taban (rastgele rüzgârsız günler)."""
    ix = G.index; g = G.to_numpy(bool); n = len(g); h = K["ruz_bekle"]
    sonra = np.array([g[i + 1:i + 1 + h].any() if i + 1 < n else False for i in range(n)])
    pos = [int(ix.searchsorted(t, side="right")) - 1 for t in sinyal_gun]
    pos = [p for p in pos if 0 <= p < n - h]
    if not pos:
        return {"n_sinyal": 0}
    zaten = np.array([g[p] for p in pos]); yok = [p for p, z in zip(pos, zaten) if not z]
    cik = float(np.mean([sonra[p] for p in yok])) if yok else np.nan
    aday = np.flatnonzero(~g[:n - h]); taban = float(sonra[rng.choice(aday, min(K["taban_n"], len(aday)), replace=False)].mean()) if len(aday) else np.nan
    return {"n_sinyal": len(pos), "zaten_ruzgarli": float(zaten.mean()), "n_yok": len(yok), "sonra_cikis": cik, "taban": taban,
            "oncu_orani": cik / taban if taban and taban > 0 and np.isfinite(cik) else np.nan}


def fon_izi_k36(Vs: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], S: Dict[str, pd.Series],
                A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K36, O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K36 sürücü: sebep sinyali -> Ö1 öncelik, Ö2 getiri (HEPSİ / ERKEN / ERKEN+ÇÖL). Çıktı k36_oncelik.csv, k36_ozet.csv, k36_olay.csv."""
    A = A or FIAyar(); rng = np.random.default_rng(K["tohum"]); ONC, OLAY = [], []
    sin = {}
    for pz in Vs:
        V = Vs[pz]; sek = fi_k14_sektor(pz); W = fi_k14_ruzgar(V, sek); gun = W.index
        for ad, sur, yon in K["esleme"][pz]:
            if sur not in S:
                continue
            uy = [s for s in fi_k36_uyeler(sek, ad) if s in V]
            if len(uy) < FI_K14_ESIK["ruz_uye"]:
                ONC.append({"pazar": pz, "sektor": ad, "surucu": K["surucu"][sur], "uye": len(uy), "n_sinyal": 0}); continue
            if (sur, yon) not in sin:
                sin[(sur, yon)] = fi_k36_sinyal(S[sur], yon, K)
            sg = list(sin[(sur, yon)][sin[(sur, yon)]].index); G = fi_k36_sektor_ruzgar(W, uy, K)
            ONC.append({"pazar": pz, "sektor": ad, "surucu": K["surucu"][sur], "uye": len(uy), **fi_k36_oncelik(G, sg, rng, K)})
            for t in sg:
                j = int(gun.searchsorted(t, side="right"))      # sinyal gününden sonraki ilk işlem günü (sinyal günü işlem günü ise j = o+1)
                if j >= len(gun):
                    continue
                d0 = gun[j - 1] if j >= 1 else None
                erken = not bool(G.iloc[j - 1]) if j >= 1 else False
                for s in uy:
                    d = V[s]
                    if gun[j] not in d.index or d0 is None or d0 not in d.index:
                        continue
                    OLAY.append({"pazar": pz, "sektor": ad, "surucu": K["surucu"][sur], "sembol": s, "sinyal": t, "giris": gun[j],
                                 "d0": d0, "erken": erken})
    X = pd.DataFrame(OLAY)
    if len(X):
        col = []
        for s, g in X.groupby(["pazar", "sembol"]):
            F = fi_k23_parmak(Vs[s[0]][s[1]], 20)
            for r in g.itertuples():
                p = F.loc[r.d0] if r.d0 in F.index else None
                col.append((r.Index, bool(p is not None and p.dusus <= FI_K23_KOR["dusus"] and p.egim >= FI_K23_KOR["egim"] and p.mum <= 1.0)))
        X["col"] = pd.Series(dict(col)).reindex(X.index).fillna(False).astype(bool)
        X["erken_col"] = X.erken & X.col; X["hepsi"] = True
    Z = []
    for kume in ("hepsi", "erken", "erken_col"):
        for pz in Vs:
            Xp = X[(X.pazar == pz) & X[kume]].sort_values("giris") if len(X) else X
            if not len(Xp):
                continue
            T = pd.concat([fi_olcut_olay(Pn[pz], fi_k27_tekil(g.assign(_b=True).reset_index(drop=True), "_b", Vs[pz], K["ayri_hisse"])[["sembol", "giris"]])
                           for _, g in Xp.groupby("sektor")], ignore_index=True)
            for dn, a, b in O["donem"]:
                Z.append({"kume": kume, "pazar": pz, "donem": dn, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
            if kume == "hepsi":
                for sur, g in T.assign(surucu=T.sembol.map(Xp.drop_duplicates("sembol").set_index("sembol").surucu)).groupby("surucu"):
                    for dn, a, b in O["donem"]:
                        Z.append({"kume": f"hepsi:{sur}", "pazar": pz, "donem": dn, **fi_olcut_hucre(g[(g.giris >= a) & (g.giris <= b)], O)})
    Z = pd.DataFrame(Z); ONC = pd.DataFrame(ONC)
    karar = {k: fi_olcut_karar(Z[Z.kume == k], O) for k in ("hepsi", "erken", "erken_col") if len(Z) and (Z.kume == k).any()}
    o = ONC.dropna(subset=["oncu_orani"]) if "oncu_orani" in ONC else ONC.iloc[0:0]
    toplu = {}
    for pz in Vs:
        g = o[o.pazar == pz]
        toplu[pz] = {"oncu_orani": float((g.sonra_cikis * g.n_yok).sum() / g.n_yok.sum() / ((g.taban * g.n_yok).sum() / g.n_yok.sum()))
                     if len(g) and g.n_yok.sum() else np.nan,
                     "zaten_ruzgarli": float((g.zaten_ruzgarli * g.n_sinyal).sum() / g.n_sinyal.sum()) if len(g) and g.n_sinyal.sum() else np.nan}
    karar["oncelik"] = ("SEBEP ÖNCE GELİR" if all(np.isfinite(t["oncu_orani"]) and t["oncu_orani"] >= K["oncu_esik"]
                                                  and t["zaten_ruzgarli"] < K["zaten_esik"] for t in toplu.values()) else "ÖNCE GELMİYOR")
    ONC.to_csv(os.path.join(A.cikti, "k36_oncelik.csv"), index=False)
    if len(Z):
        Z.drop(columns=[c for c in Z if c.startswith("_")]).to_csv(os.path.join(A.cikti, "k36_ozet.csv"), index=False)
    if len(X):
        X.to_csv(os.path.join(A.cikti, "k36_olay.csv"), index=False)
    return {"oncelik": ONC, "toplu": toplu, "ozet": Z, "karar": karar, "olay": X}


# K36 DEVAM (ÖNCEDEN YAZILDI 28 Eki; ilk turda sebep sinyali rüzgârdan önce gelmedi (öncü oranı BIST 1,03 / ABD 1,08) ve getiri dört
# hücrede tutmadı; bu üçünün sonucu görülmeden). Aynı eşleme, aynı ölçütler (öncelik + FI_OLCUT dört hücre):
#   D1 GÜÇLÜ SEBEP: z eşiği 2,0 (sürücüde nadir, büyük hareket).
#   D2 YAVAŞ SEBEP: 60 günlük değişimin z-skoru (trend; 20 gün yerine), eşik 1,0.
#   D3 KÖTÜ SEBEP = KAÇINMA: yön ters (sürücü sektör aleyhine hareket eder), olaylar aynı; karar fi_olcut_karar_kacinma (ayna).
FI_K36_DENEME = {"D1_guclu": {"z_esik": 2.0}, "D2_yavas": {"z_pencere": 60}, "D3_kacinma": {"ters": True}}


def fon_izi_k36_deneme(Vs: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], S: Dict[str, pd.Series],
                       A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K36, D: Dict[str, Any] = FI_K36_DENEME,
                       O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K36 devam: D1..D3 fon_izi_k36 ile; D3'te eşleme yönleri ters ve kaçınma kararı. Çıktı k36_deneme.csv."""
    A = A or FIAyar(); Z, karar = [], {}
    for ad, dk in D.items():
        Kd = {**K, **{k: v for k, v in dk.items() if k != "ters"}}
        if dk.get("ters"):
            Kd["esleme"] = {pz: [(a, s_, -y) for a, s_, y in L] for pz, L in K["esleme"].items()}
        Kd["klasor"] = K["klasor"]
        Ad = FIAyar(); Ad.cikti = os.path.join(A.cikti, "k36_" + ad); os.makedirs(Ad.cikti, exist_ok=True)
        R = fon_izi_k36(Vs, Pn, S, Ad, Kd, O)
        Zr = R["ozet"]; Zr = Zr[Zr.kume.isin(["hepsi", "erken", "erken_col"])].assign(deneme=ad); Z.append(Zr)
        for k in ("hepsi", "erken", "erken_col"):
            g = Zr[Zr.kume == k]
            if len(g):
                karar[f"{ad}:{k}"] = fi_olcut_karar_kacinma(g, O) if dk.get("ters") else fi_olcut_karar(g, O)
        karar[f"{ad}:oncelik"] = R["karar"]["oncelik"]; karar[f"{ad}:toplu"] = R["toplu"]
    Z = pd.concat(Z, ignore_index=True) if Z else pd.DataFrame()
    if len(Z):
        Z.drop(columns=[c for c in Z if c.startswith("_")]).to_csv(os.path.join(A.cikti, "k36_deneme.csv"), index=False)
    return {"ozet": Z, "karar": karar}

# K37 BÜYÜKLER ÖNCE, KÜÇÜKLER SONRA (Cemal 28 Eki: '2 ile başla'; dikkat: para akışı OBV / CMF / A-D iyileşmesi tek başına yetmez; temel
# durum = gerçek faaliyet, gelir, aşırı borç ve sürekli hisse ihracı olmaması; haber zamanlaması = sonraki haberden önce oluşan sinyal
# geçmişte tekrarlanabilir olmalı; küçük hissede düşük likidite / sert hareket / manipülasyon riski). Kapalı 'sektör ısısı'na dokunur,
# Cemal istedi. ÖNCEDEN YAZILDI (sonuç görülmeden).
# SEKTÖR: K14 sektörü (BIST alt endeks, ABD endüstri), üye >= 6. BÜYÜKLÜK: 60 günlük medyan işlem değeri (fiyat x hacim, d-1'e kadar),
#   sektör içinde her gün üst üçte bir = BÜYÜK, alt üçte bir = KÜÇÜK (BIST'te piyasa değeri yok; işlem değeri büyüklük vekili).
# SİNYAL (sektör, gün d): büyük sepeti ortalama 20 günlük getirisi - piyasa medyanı >= +%10 ve sepet > 0 VE küçük sepeti - piyasa < +%5
#   (küçükler henüz gelmedi); geçiş günü (önceki gün şart yok). OLAY: d'deki küçük üyeler; giriş d'den sonraki ilk açılış; hissede 60
#   günde tek. ÖLÇÜ: FI_OLCUT dört hücre (eşli fark; eşler aynı gün aynı momentum x likidite hücresi -> sığ hisse kendi likidite dilimiyle
#   kıyaslanır, 'küçük hisse riski' ortak payda). Bilgi: fark - %1 (sığ hissede gidiş-dönüş maliyeti), en kötü olay, -%30 altı payı.
# SÜZGEÇLER (d'de bilinen):
#   P PARA AKIŞI: CMF(20) > 0 VE OBV > OBV'nin 20 günlük ortalaması (A/D çizgisi aynı para akışı hacmine dayanır, ayrıca sayılmaz).
#   T TEMEL: BIST temel_duz.csv, d'den önce açıklanmış son çeyrek: (satış TTM büyümesi > 0 ya da net kâr > 0) VE borç/özkaynak < 1,0 VE
#     özkaynak pozitif (BIST'te hisse ihracı verisi yok). ABD K31 SEC özeti, d'den önceki son bildirim: yıllık pay artışı < %10 (sürekli
#     ihraç yok) VE (faaliyet nakit akışı >= 0 ya da nakit pisti >= 8 çeyrek) (borç kalemi SEC özetinde çekilmedi, not).
#   Kümeler: HEPSİ, P, P+T, T (bilgi). Karar fi_olcut_karar her küme.
# H HABER ZAMANLAMASI (süzgeç değil, sınama; ileriye bakar): sinyalden sonraki 60 işlem günü içinde hissenin bilanço açıklaması (K28) var
#   ve tepkisi 'ust' (çeyreğin en iyi beşte biri) ise 'sinyal haberden önce oluştu, haber iyi geldi'. Yıl yıl (2023, 2024, 2025)
#   P(ust | sinyal ve haber) / 0,20 >= 1,3 ise o pazarda TEKRARLANIYOR; iki pazarda da tutmalı.
# DEVAM (aynı anda önceden yazıldı): D1 GEVŞEK eşik (büyük >= +%5, küçük < +%2); D2 YAVAŞ pencere 60 gün (büyük >= +%15, küçük < +%5);
#   D3 AYNA kaçınma: büyükler piyasanın %10 altına düşmüş, küçükler henüz düşmemiş -> küçük üyelerde fi_olcut_karar_kacinma.
FI_K37 = {"uye_min": 6, "likit_gun": 60, "getiri_gun": 20, "buyuk_esik": 0.10, "kucuk_esik": 0.05, "ayri": 60, "haber_gun": 60,
          "haber_kat": 1.3, "haber_taban": 0.20, "haber_yil": (2023, 2024, 2025), "maliyet": 0.01, "cmf_gun": 20, "obv_gun": 20,
          "borc_oz": 1.0, "pay_yil": 0.10, "pist": 8.0, "temel": "temel_duz.csv",
          "deneme": {"D1_gevsek": {"buyuk_esik": 0.05, "kucuk_esik": 0.02}, "D2_yavas": {"getiri_gun": 60, "buyuk_esik": 0.15},
                     "D3_ayna": {"ayna": True}}}


def fi_k37_para_akisi(d: pd.DataFrame, K: Dict[str, Any] = FI_K37) -> pd.Series:
    """P süzgeci (bool, gün): CMF(20) > 0 ve OBV > OBV'nin 20 günlük ortalaması; d günü kapanışıyla."""
    h, l, c, v = d.High.astype(float), d.Low.astype(float), d.Close.astype(float), d.Volume.astype(float)
    mfm = ((c - l) - (h - c)) / (h - l).replace(0, np.nan); mfv = (mfm * v).fillna(0.0)
    cmf = mfv.rolling(K["cmf_gun"]).sum() / v.rolling(K["cmf_gun"]).sum().replace(0, np.nan)
    obv = (np.sign(c.diff()).fillna(0.0) * v).cumsum()
    return ((cmf > 0) & (obv > obv.rolling(K["obv_gun"]).mean())).fillna(False)


def fi_k37_temel_bist(kok: Optional[str] = None, K: Dict[str, Any] = FI_K37) -> pd.DataFrame:
    """temel_duz.csv -> sembol, aciklama (gün), temel_ok."""
    kok = kok or os.path.dirname(os.path.abspath(__file__))
    t = pd.read_csv(os.path.join(kok, K["temel"]), parse_dates=["aciklama"])
    sb = pd.to_numeric(t.st_buyume, errors="coerce").replace([np.inf, -np.inf], np.nan)
    ok = ((sb > 0) | (t.nk_pozitif == 1)) & (pd.to_numeric(t.borc_oz, errors="coerce") < K["borc_oz"]) & (t.oz_negatif == 0)
    return pd.DataFrame({"sembol": t.sembol.astype(str).str.upper(), "aciklama": t.aciklama, "temel_ok": ok.fillna(False)}).dropna(
        subset=["aciklama"]).sort_values("aciklama")


def fi_k37_temel_abd(Fin: pd.DataFrame, K: Dict[str, Any] = FI_K37) -> pd.DataFrame:
    """K31 SEC özeti -> sembol, aciklama (filed), temel_ok (pay artışı < %10 ve (ocf >= 0 ya da pist >= 8))."""
    ok = (Fin.pay_yil < K["pay_yil"]) & ((Fin.ocf_ceyrek >= 0) | (Fin.pist >= K["pist"]))
    return pd.DataFrame({"sembol": Fin.sembol.astype(str).str.upper(), "aciklama": pd.to_datetime(Fin.filed),
                         "temel_ok": ok.fillna(False)}).dropna(subset=["aciklama"]).sort_values("aciklama")


def fi_k37_son_temel(T: pd.DataFrame, sembol: str, gun: pd.Timestamp) -> Optional[bool]:
    """gun'den önce açıklanmış son temel kaydının temel_ok'u; yoksa None."""
    g = T[(T.sembol == sembol) & (T.aciklama < gun)]
    return bool(g.temel_ok.iloc[-1]) if len(g) else None


def fi_k37_sinyal(V: Dict[str, pd.DataFrame], sek: Dict[str, str], K: Dict[str, Any] = FI_K37, ayna: bool = False
                  ) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
    """Sektör sinyal günleri: satırlar (sektor, gun, buyuk_fark, kucuk_fark); ayrıca gün -> o günkü küçük üyeler (olay adayları)."""
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index().ffill(limit=5)
    r = C / C.shift(K["getiri_gun"]) - 1; piy = r.median(axis=1)
    L = pd.DataFrame({s: (d.Close * d.Volume) for s, d in V.items()}).sort_index().rolling(K["likit_gun"], min_periods=40).median().shift(1)
    grup: Dict[str, List[str]] = {}
    for s in C.columns:
        a = sek.get(str(s).upper())
        if a:
            grup.setdefault(a, []).append(s)
    sat, kucuk_uye = [], {}
    for a, uy in grup.items():
        if len(uy) < K["uye_min"]:
            continue
        Lu = L[uy]; Ru = r[uy]; rank = Lu.rank(axis=1, pct=True); n = Lu.notna().sum(axis=1)
        buyuk = (rank > 2 / 3); kucuk = (rank <= 1 / 3)
        rb = Ru.where(buyuk).mean(axis=1) - piy; rk = Ru.where(kucuk).mean(axis=1) - piy; sb = Ru.where(buyuk).mean(axis=1)
        if ayna:
            sart = (rb <= -K["buyuk_esik"]) & (sb < 0) & (rk > -K["kucuk_esik"]) & (n >= K["uye_min"])
        else:
            sart = (rb >= K["buyuk_esik"]) & (sb > 0) & (rk < K["kucuk_esik"]) & (n >= K["uye_min"])
        gec = sart & ~sart.shift(1).fillna(False).astype(bool)
        for t in gec[gec].index:
            sat.append({"sektor": a, "gun": t, "buyuk_fark": float(rb[t]), "kucuk_fark": float(rk[t])})
            kucuk_uye[(a, t)] = [s for s in uy if bool(kucuk.at[t, s])]
    return pd.DataFrame(sat), kucuk_uye


def fon_izi_k37(Vs: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], Fin: pd.DataFrame, X28: Dict[str, pd.DataFrame],
                A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K37, O: Dict[str, Any] = FI_OLCUT, ad: str = "k37") -> Dict[str, Any]:
    """K37 sürücü (ana ve devam için ortak; devamda K değişir, ad 'k37_D1' gibi). X28: pazar -> K28 olay tablosu (D, sembol, ust).
    Çıktı <ad>_sinyal.csv, <ad>_ozet.csv, <ad>_haber.csv."""
    A = A or FIAyar(); ayna = bool(K.get("ayna")); SIN, OL, Z, HB = [], [], [], []
    T_ = {"BIST": fi_k37_temel_bist(K=K), "ABD": fi_k37_temel_abd(Fin, K) if Fin is not None and len(Fin) else pd.DataFrame(columns=["sembol", "aciklama", "temel_ok"])}
    for pz, V in Vs.items():
        sek = fi_k14_sektor(pz); S, KU = fi_k37_sinyal(V, sek, K, ayna); SIN.append(S.assign(pazar=pz))
        gun = pd.DatetimeIndex(sorted(set().union(*[d.index for d in V.values()]))); PA: Dict[str, pd.Series] = {}
        for r in S.itertuples():
            j = int(gun.searchsorted(r.gun, side="right"))
            if j >= len(gun):
                continue
            for s in KU.get((r.sektor, r.gun), []):
                d = V[s]
                if gun[j] not in d.index or r.gun not in d.index:
                    continue
                if s not in PA:
                    PA[s] = fi_k37_para_akisi(d, K)
                tm = fi_k37_son_temel(T_[pz], s, r.gun)
                OL.append({"pazar": pz, "sektor": r.sektor, "sembol": s, "sinyal": r.gun, "giris": gun[j], "P": bool(PA[s].get(r.gun, False)),
                           "T": tm, "hepsi": True})
    X = pd.DataFrame(OL)
    if len(X):
        X["T"] = X["T"].astype("boolean"); X["PT"] = X.P & X["T"].fillna(False).astype(bool); X["T_"] = X["T"].fillna(False).astype(bool)
    for kume in ("hepsi", "P", "PT", "T_"):
        for pz in Vs:
            Xp = X[(X.pazar == pz) & X[kume].astype(bool)].sort_values("giris") if len(X) else X
            if not len(Xp):
                continue
            E = fi_k27_tekil(Xp.assign(_b=True).reset_index(drop=True), "_b", Vs[pz], K["ayri"])
            T = fi_olcut_olay(Pn[pz], E[["sembol", "giris"]])
            for dn, a, b in O["donem"]:
                Td = T[(T.giris >= a) & (T.giris <= b)]; h = fi_olcut_hucre(Td, O); f = Td.fark.dropna()
                Z.append({"kume": kume, "pazar": pz, "donem": dn, **h, "ort_fark_maliyetli": h.get("ort_fark", np.nan) - K["maliyet"],
                          "en_kotu": float(Td.r60.min()) if Td.r60.notna().any() else np.nan,
                          "eksi30_payi": float((Td.r60 <= -0.30).mean()) if Td.r60.notna().any() else np.nan})
            if kume == "hepsi" and pz in X28 and len(X28[pz]):
                H = X28[pz].assign(D=pd.to_datetime(X28[pz].D)); hs = {s: g.sort_values("D") for s, g in H.groupby("sembol")}
                for r in E.itertuples():
                    g = hs.get(r.sembol)
                    if g is None:
                        continue
                    ix = Vs[pz][r.sembol].index; j = int(ix.get_loc(r.giris)); son = ix[min(j + K["haber_gun"], len(ix) - 1)]
                    w = g[(g.D > r.sinyal) & (g.D <= son)]
                    if len(w):
                        HB.append({"pazar": pz, "yil": r.sinyal.year, "sembol": r.sembol, "sinyal": r.sinyal, "haber": w.D.iloc[0], "ust": bool(w.ust.iloc[0])})
    Z = pd.DataFrame(Z); HB = pd.DataFrame(HB); SIN = pd.concat(SIN, ignore_index=True) if SIN else pd.DataFrame()
    karar = {k: (fi_olcut_karar_kacinma if ayna else fi_olcut_karar)(Z[Z.kume == k], O) for k in ("hepsi", "P", "PT", "T_") if len(Z) and (Z.kume == k).any()}
    hz = {}
    if len(HB):
        for pz, g in HB.groupby("pazar"):
            y = g.groupby("yil").ust.agg(["mean", "size"]); y["kat"] = y["mean"] / K["haber_taban"]
            hz[pz] = {int(k): (round(float(v["kat"]), 2), int(v["size"])) for k, v in y.iterrows()}
        tut = all(all(hz.get(pz, {}).get(y, (0, 0))[0] >= K["haber_kat"] for y in K["haber_yil"]) for pz in Vs)
        karar["haber"] = "HABER ÖNCESİ SİNYAL TEKRARLANIYOR" if tut else "TEKRARLANMIYOR"
    SIN.to_csv(os.path.join(A.cikti, f"{ad}_sinyal.csv"), index=False)
    if len(Z):
        Z.drop(columns=[c for c in Z if c.startswith("_")]).to_csv(os.path.join(A.cikti, f"{ad}_ozet.csv"), index=False)
    if len(HB):
        HB.to_csv(os.path.join(A.cikti, f"{ad}_haber.csv"), index=False)
    return {"sinyal": SIN, "olay": X, "ozet": Z, "haber": HB, "haber_yil": hz, "karar": karar}


def fon_izi_k37_deneme(Vs: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], Fin: pd.DataFrame,
                       X28: Dict[str, pd.DataFrame], A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K37,
                       O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K37 devam: D1 gevşek, D2 yavaş, D3 ayna kaçınma."""
    out = {}
    for ad, dk in K["deneme"].items():
        out[ad] = fon_izi_k37(Vs, Pn, Fin, X28, A, {**K, **dk}, O, ad=f"k37_{ad}")
    return out

# K38 EN YAKIN ADAYLAR 3 PAZARDA (Cemal 28 Eki: 'üçünü de yaz, evreni kur, adayları 3 pazarda ölç; Amerika ve Avrupa tutan iz kabul
# edilsin, BIST bilgi, Çin sonra'). ÖNCEDEN YAZILDI (Avrupa verisi inmeden, sonuç görülmeden). Karar FI_OLCUT 'karar' = (ABD, AVR).
# ADAYLAR (tek cetvelde ABD iki hücreye en yakın olanlar ve BIST'te üç dönemde tutan; tanımlar IZ_KARNE ile birebir, fiyat-hacim):
#   S1 TAVAN GÜNÜ KAÇINMASI (Ç16): gün kapanışı >= +%9 (H > L, hacim > 0); giriş ertesi açılış -> aşağı (kaçınma) ölçüt.
#   S2 GERİDE KALAN + HACİM ARTIŞI KAÇINMASI (Ç25 A12): ayın son işlem günü, 250 gün getirisi pazar içinde en düşük %20 VE hacim artışı
#      (son 250 gün medyanı / önceki 250 gün medyanı) en yüksek %20 -> kaçınma.
#   S3 BLOK HACİMLİ TABAN GÜNÜ (Ç60 A14): hacim >= 20 x önceki 20 gün medyanı VE gün <= -%9,5 -> yukarı ölçüt.
#   Çölde içeriden alım (K27 / K30) Avrupa'da ölçülemez (bedava içeriden işlem verisi yok): en fazla ABD-ADAY; bu turda yeniden koşulmaz.
# Hisse başına 60 işlem gününde tek olay. Her sinyal ABD, AVR, BIST 2023 / 2024-26 hücrelerinde; karar fi_olcut_karar(_kacinma).
# Avrupa notu: STOXX 600 + FTSE 250, yalnız bugün işlem görenler; Londra fiyatı peni (getiri etkilenmez), likidite EUR'ya çevrili.
FI_K38 = {"tavan": 0.09, "blok_kat": 20.0, "blok_gun": -0.095, "blok_pencere": 20, "geride_dilim": 0.2, "ayri": 60}


def _fi_k38_panel(V: Dict[str, pd.DataFrame], kol: str) -> pd.DataFrame:
    """IZ_KARNE._ik_panel ile aynı: ince günler (hisselerin yarısından azının barı olan) tablodan çıkar."""
    P = pd.DataFrame({s: d[kol] for s, d in V.items()}).sort_index()
    return P.loc[P.notna().sum(axis=1) >= 0.5 * P.ffill().notna().sum(axis=1)]


def _fi_k38_olay(M: pd.DataFrame) -> pd.DataFrame:
    s = M.stack(); s = s[s.astype(bool)]
    return pd.DataFrame({"sembol": s.index.get_level_values(1), "gun": s.index.get_level_values(0)})


def fi_k38_sinyaller(V: Dict[str, pd.DataFrame], K: Dict[str, Any] = FI_K38) -> Dict[str, pd.DataFrame]:
    """S1 tavan, S2 geride_hacim, S3 blok_taban olay günleri (sembol, gun); tanımlar IZ_KARNE ik_s_* ile birebir."""
    C = _fi_k38_panel(V, "Close"); H = _fi_k38_panel(V, "High"); L = _fi_k38_panel(V, "Low"); Vo = _fi_k38_panel(V, "Volume")
    gecerli = (H > L) & (Vo > 0); r = C / C.shift(1) - 1
    S1 = _fi_k38_olay((r >= K["tavan"]) & gecerli)
    med = Vo.shift(1).rolling(K["blok_pencere"], min_periods=int(K["blok_pencere"] * 0.8)).median()
    S3 = _fi_k38_olay((Vo >= K["blok_kat"] * med) & (med > 0) & (r <= K["blok_gun"]) & gecerli)
    r250 = C / C.shift(250) - 1; h1 = Vo.rolling(250, min_periods=200).median(); h0 = h1.shift(250); hk = h1 / h0.where(h0 > 0)
    ay_sonu = C.index.to_series().groupby(C.index.to_period("M")).max().values
    R = r250.loc[ay_sonu]; Kk = hk.loc[ay_sonu]
    S2 = _fi_k38_olay((R.rank(axis=1, pct=True) <= K["geride_dilim"]) & (Kk.rank(axis=1, pct=True) >= 1 - K["geride_dilim"]) & R.notna() & Kk.notna())
    return {"S1_tavan_kacinma": S1, "S2_geride_hacim_kacinma": S2, "S3_blok_taban_yukari": S3}


def fon_izi_k38(Vs: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], A: Optional[FIAyar] = None,
                K: Dict[str, Any] = FI_K38, O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K38 sürücü: üç aday x pazarlar (ABD, AVR, BIST) x dönemler; karar pazarları O['karar']. Çıktı k38_ozet.csv."""
    A = A or FIAyar(); Z = []
    for pz, V in Vs.items():
        gun = pd.DatetimeIndex(sorted(set().union(*[d.index for d in V.values()])))
        for ad, S in fi_k38_sinyaller(V, K).items():
            if not len(S):
                continue
            j = gun.searchsorted(pd.DatetimeIndex(S.gun), side="right")
            ok = j < len(gun); S = S[ok].assign(giris=gun[j[ok]])
            S = S[[g in V[s].index for s, g in zip(S.sembol, S.giris)]].sort_values("giris").assign(_b=True).reset_index(drop=True)
            E = fi_k27_tekil(S, "_b", V, K["ayri"]); T = fi_olcut_olay(Pn[pz], E[["sembol", "giris"]])
            for dn, a, b in O["donem"]:
                Z.append({"sinyal": ad, "pazar": pz, "donem": dn, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
    Z = pd.DataFrame(Z)
    karar = {ad: (fi_olcut_karar_kacinma if ad.endswith("kacinma") else fi_olcut_karar)(Z[Z.sinyal == ad], O) for ad in Z.sinyal.unique()} if len(Z) else {}
    if len(Z):
        Z.drop(columns=[c for c in Z if c.startswith("_")]).to_csv(os.path.join(A.cikti, "k38_ozet.csv"), index=False)
    return {"ozet": Z, "karar": karar}


def fi_avr_evren(ham: Dict[str, Any], evren: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Avrupa ham indirme ({'V': {kod: OHLCV}, 'fx': {para: EUR kuru}}) + evren listesi (kod, ulke) -> V_AVR: OHLCV + Kur (yerel -> EUR;
    Londra peni: GBP/100). EUR ülkelerinde Kur = 1."""
    para = {"United Kingdom": "GBp", "Bermuda": "GBp", "Israel": "GBp", "Switzerland": "CHF", "Sweden": "SEK", "Denmark": "DKK", "Norway": "NOK", "Poland": "PLN"}
    ulke = evren.set_index("kod").ulke.to_dict(); V = {}
    for kod, d in ham["V"].items():
        p = para.get(ulke.get(kod, ""), "EUR"); d = d.copy()
        # Veri temizliği (28 Eki, ilk koşuda görüldü: Londra'da peni / sterlin geçişi 100x sıçrama; DIA.MC 1000x): bir günde kapanış
        # oranı 80-125x ya da tersi -> o günden sonrası 100'e bölünür / çarpılır (fiyat sütunları); başka >= 20x sıçrama -> hisse dışarıda.
        r = (d.Close / d.Close.shift(1)).to_numpy(float); kot = False; carpan = np.ones(len(d))
        for i in np.flatnonzero((r >= 20) | (r <= 0.05)):
            if 80 <= r[i] <= 125:
                carpan[i:] /= 100.0
            elif 1 / 125 <= r[i] <= 1 / 80:
                carpan[i:] *= 100.0
            else:
                kot = True
        if kot:
            filog.warning("K38 AVR %s: açıklanamayan fiyat sıçraması, dışarıda", kod); continue
        if (carpan != 1).any():
            for kol in ("Open", "High", "Low", "Close"):
                d[kol] = d[kol] * carpan
            if p == "GBp" and carpan[-1] < 1:          # denetim 28 Eki: seri sterline indirildiyse Kur peni (/100) değil sterlin olmalı
                p = "GBP"
        if p == "EUR":
            d["Kur"] = 1.0
        else:
            fx = ham["fx"].get("GBp" if p == "GBP" else p)
            if fx is None:
                continue
            k = fx.reindex(d.index).ffill().bfill().astype(float); d["Kur"] = (k / 100.0) if p == "GBp" else k
        V[kod] = d
    return V

# K38-B ŞEKİLLER 3 PAZARDA (Cemal 28 Eki: 'çöl, ikili dip, ters omuz baş omuz, RSI / MACD uyumsuzluk ayrı ayrı karşılaştırma olarak
# koştur'). 23 Eki gösterge / uyumsuzluk turu BIST + ABD eski cetvelle İZ DEĞİL'di; yeni karar pazarlarıyla (ABD + AVR) Cemal'in isteğiyle
# yeniden. ÖNCEDEN YAZILDI (sonuç görülmeden). Tanımlar (yalnız d ve öncesi; giriş d'den sonraki ilk açılış; hissede 60 günde tek):
#   F1 ÇÖL: K24 iki evre kuralı (fi_k24_tara 'kural' günü).
#   F2 İKİLİ DİP: d günü kapanışı 'boyun'un üstünde; boyun = iki dip arasındaki en yüksek kapanış; dipler = 20 günlük kapanış minimumları,
#      aralarında 20-120 bar, seviyeleri birbirine +-%3 içinde, boyun diplerin >= +%8 üstünde, ikinci dip d'den en çok 40 bar önce; d
#      boyunun üstündeki İLK kapanış.
#   F3 TERS OMUZ BAŞ OMUZ: üç 20 günlük dip (sol omuz, baş, sağ omuz), her biri arası 10-60 bar; baş iki omuzdan >= %5 aşağıda, omuzlar
#      birbirine +-%6 içinde; boyun = iki ara tepe kapanışlarının en yükseği; d = sağ omuzdan sonra boyunun üstündeki ilk kapanış (en çok 40 bar).
#   F4 RSI BOĞA UYUMSUZLUĞU: d kapanışı son 20 günün en düşüğü VE [d-120, d-20] aralığındaki en düşük kapanıştan düşük (daha alçak dip),
#      RSI14(d) >= o eski dip günü RSI14'ü + 3 ve RSI14(d) < 40. (Cemal 'negatif uyumsuzluk' dedi; dipte fiyat düşerken göstergenin
#      yükselmesi boğa / pozitif uyumsuzluktur; ayna olarak F6 ayı uyumsuzluğu kaçınma ölçütüyle koşulur.)
#   F5 MACD BOĞA UYUMSUZLUĞU: F4 ile aynı fiyat şartı; MACD çizgisi (12-26) d'de eski dip günündekinden yüksek ve < 0.
#   F6 RSI AYI UYUMSUZLUĞU (kaçınma): d kapanışı son 20 günün en yükseği ve [d-120, d-20] en yüksek kapanışından yüksek, RSI14(d) <= eski
#      tepe RSI14'ü - 3 ve RSI14(d) > 60 -> fi_olcut_karar_kacinma.
FI_K38B = {"dip_pencere": 20, "ikili_ara": (20, 120), "ikili_tol": 0.03, "ikili_boyun": 0.08, "onay_bar": 40, "obo_ara": (10, 60),
           "obo_bas": 0.05, "obo_omuz": 0.06, "uyum_eski": (120, 20), "uyum_rsi_fark": 3.0, "uyum_rsi_dip": 40.0, "uyum_rsi_tepe": 60.0,
           "ayri": 60}


def _fi_k38b_rsi(c: pd.Series, n: int = 14) -> pd.Series:
    d = c.diff(); up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def _fi_k38b_dipler(c: np.ndarray, w: int) -> np.ndarray:
    """w günlük yerel dip günleri: c[i] = min(c[i-w..i+w]) (geleceğe bakar; yalnız ONAY günü d'den önce bitmiş dipler kullanılır)."""
    s = pd.Series(c); m = s.rolling(2 * w + 1, center=True).min(); ix = np.flatnonzero((s == m).to_numpy())
    out: List[int] = []                                   # w bar içindeki eş dipler (plato, eşit kapanış) tek dip: en düşük / ilk
    for i in ix:
        if out and i - out[-1] < w:
            if c[i] < c[out[-1]]:
                out[-1] = int(i)
        else:
            out.append(int(i))
    return np.array(out, dtype=int)


def fi_k38b_ikili_dip(d: pd.DataFrame, K: Dict[str, Any] = FI_K38B) -> List[pd.Timestamp]:
    c = d.Close.to_numpy(float); n = len(c); w = K["dip_pencere"]; dip = _fi_k38b_dipler(c, w); out = []; a0, a1 = K["ikili_ara"]
    for k in range(1, len(dip)):
        j, i = dip[k], dip[k - 1]
        if not (a0 <= j - i <= a1) or abs(c[j] / c[i] - 1) > K["ikili_tol"]:
            continue
        boyun = c[i + 1:j].max() if j > i + 1 else np.nan
        if not np.isfinite(boyun) or boyun < min(c[i], c[j]) * (1 + K["ikili_boyun"]):
            continue
        for t in range(j + w, min(j + K["onay_bar"], n - 1) + 1):       # dip ancak j + w'de kesinleşir
            if c[t] > boyun:
                out.append(d.index[t]); break
    return out


def fi_k38b_ters_obo(d: pd.DataFrame, K: Dict[str, Any] = FI_K38B) -> List[pd.Timestamp]:
    c = d.Close.to_numpy(float); n = len(c); w = K["dip_pencere"]; dip = _fi_k38b_dipler(c, w); out = []; a0, a1 = K["obo_ara"]
    for k in range(2, len(dip)):
        i, h, j = dip[k - 2], dip[k - 1], dip[k]
        if not (a0 <= h - i <= a1 and a0 <= j - h <= a1):
            continue
        if c[h] > min(c[i], c[j]) * (1 - K["obo_bas"]) or abs(c[j] / c[i] - 1) > K["obo_omuz"]:
            continue
        boyun = max(c[i + 1:h].max(), c[h + 1:j].max())
        for t in range(j + w, min(j + K["onay_bar"], n - 1) + 1):
            if c[t] > boyun:
                out.append(d.index[t]); break
    return out


def fi_k38b_uyumsuzluk(d: pd.DataFrame, K: Dict[str, Any] = FI_K38B) -> Dict[str, List[pd.Timestamp]]:
    c = d.Close.astype(float); rsi = _fi_k38b_rsi(c); macd = _fi_ema(c, 12) - _fi_ema(c, 26); e0, e1 = K["uyum_eski"]
    cv, rv, mv = c.to_numpy(), rsi.to_numpy(), macd.to_numpy(); n = len(cv); F4, F5, F6 = [], [], []
    for t in range(e0, n):
        if cv[t] == cv[t - 19:t + 1].min():
            seg = cv[t - e0:t - e1 + 1]; k = t - e0 + int(np.argmin(seg))
            if cv[t] < seg.min() and np.isfinite(rv[t]) and np.isfinite(rv[k]):
                if rv[t] >= rv[k] + K["uyum_rsi_fark"] and rv[t] < K["uyum_rsi_dip"]:
                    F4.append(d.index[t])
                if np.isfinite(mv[t]) and np.isfinite(mv[k]) and mv[t] > mv[k] and mv[t] < 0:
                    F5.append(d.index[t])
        if cv[t] == cv[t - 19:t + 1].max():
            seg = cv[t - e0:t - e1 + 1]; k = t - e0 + int(np.argmax(seg))
            if cv[t] > seg.max() and np.isfinite(rv[t]) and np.isfinite(rv[k]) and rv[t] <= rv[k] - K["uyum_rsi_fark"] and rv[t] > K["uyum_rsi_tepe"]:
                F6.append(d.index[t])
    return {"F4_rsi_boga_uyumsuzluk": F4, "F5_macd_boga_uyumsuzluk": F5, "F6_rsi_ayi_uyumsuzluk_kacinma": F6}


def fi_k38b_sinyaller(V: Dict[str, pd.DataFrame], K: Dict[str, Any] = FI_K38B) -> Dict[str, pd.DataFrame]:
    """F1..F6 olay günleri (sembol, gun) bütün hisselerde."""
    S: Dict[str, List[Tuple[str, pd.Timestamp]]] = {k: [] for k in ("F1_col_k24", "F2_ikili_dip", "F3_ters_obo", "F4_rsi_boga_uyumsuzluk",
                                                                     "F5_macd_boga_uyumsuzluk", "F6_rsi_ayi_uyumsuzluk_kacinma")}
    for s, d in V.items():
        if len(d) < 300:
            continue
        try:
            T = fi_k24_tara(d)
            if len(T) and "kural" in T:
                S["F1_col_k24"] += [(s, t) for t in T[T.kural].tarih]
            S["F2_ikili_dip"] += [(s, t) for t in fi_k38b_ikili_dip(d, K)]
            S["F3_ters_obo"] += [(s, t) for t in fi_k38b_ters_obo(d, K)]
            for k, L in fi_k38b_uyumsuzluk(d, K).items():
                S[k] += [(s, t) for t in L]
        except Exception as e:
            filog.warning("K38-B %s: %s", s, e)
    return {k: pd.DataFrame(v, columns=["sembol", "gun"]) for k, v in S.items()}


def fon_izi_k38b(Vs: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], A: Optional[FIAyar] = None,
                 K: Dict[str, Any] = FI_K38B, O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K38-B sürücü: F1..F6 x pazarlar x dönemler; karar pazarları O['karar']. Çıktı k38b_ozet.csv."""
    A = A or FIAyar(); Z = []
    for pz, V in Vs.items():
        gun = pd.DatetimeIndex(sorted(set().union(*[d.index for d in V.values()])))
        for ad, S in fi_k38b_sinyaller(V, K).items():
            if not len(S):
                continue
            j = gun.searchsorted(pd.DatetimeIndex(S.gun), side="right"); ok = j < len(gun); S = S[ok].assign(giris=gun[j[ok]])
            S = S[[g in V[s].index for s, g in zip(S.sembol, S.giris)]].sort_values("giris").assign(_b=True).reset_index(drop=True)
            E = fi_k27_tekil(S, "_b", V, K["ayri"]); T = fi_olcut_olay(Pn[pz], E[["sembol", "giris"]])
            for dn, a, b in O["donem"]:
                Z.append({"sinyal": ad, "pazar": pz, "donem": dn, **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
    Z = pd.DataFrame(Z)
    karar = {ad: (fi_olcut_karar_kacinma if ad.endswith("kacinma") else fi_olcut_karar)(Z[Z.sinyal == ad], O) for ad in Z.sinyal.unique()} if len(Z) else {}
    if len(Z):
        Z.drop(columns=[c for c in Z if c.startswith("_")]).to_csv(os.path.join(A.cikti, "k38b_ozet.csv"), index=False)
    return {"ozet": Z, "karar": karar}

# K39 ABD ÖNCÜ, AVRUPA TAKİP (Cemal 28 Eki: 'Amerika verileri öncü, sonra Avrupa ve Asya takip eder; Amerika'da asıl izleri ararken üstüne
# git, her olasılığı ayrıca değerlendir'). Kapalı 'sektör ısısı'na komşu, Cemal istedi. ÖNCEDEN YAZILDI (sonuç görülmeden).
# KABA SEKTÖR: üç pazarın etiketleri 13 ortak gruba eşlenir (anahtar kelime kuralları, fi_k39_kaba): ENERJI, BANKA, SIGORTA, FINANS,
#   GAYRIMENKUL, SAGLIK, TEKNOLOJI, SANAYI, ULASIM, MADEN, KIMYA, TUKETIM, KAMU_TELEKOM. Grupta üye < 5 ise o pazar-grup ölçülmez.
# SEPET: pazar içinde grubun eşit ağırlıklı P günlük getirisi - pazar medyanı (göreli). LİDER pazar L, HEDEF pazar H.
# SİNYAL (grup, gün d, lider takviminde): lider göreli >= E ve lider sepet > 0 VE ('henüz' şartı varsa) hedef göreli < E/2 (hedef henüz
#   gelmedi); geçiş günü (önceki gün şart yok). OLAY: hedef pazardaki grup üyeleri; giriş = d'den sonraki ilk hedef işlem günü açılışı
#   (ABD kapanışı -> Avrupa ertesi gün); hissede 60 günde tek. ÖLÇÜ: FI_OLCUT (hedef pazarın eşleri), hücreler 2016-22 (dış örnek),
#   2023, 2024-26.
# OLASILIKLAR (önceden sabit): P in {20, 60} x E in {0,10, 0,20} x henüz {evet, hayır} = 8 çeşit; ANA = (20, 0,10, evet). Yönler:
#   ABD -> AVR (Cemal'in savı), AVR -> ABD (ayna: eşit tutarsa öncülük değil, birlikte hareket), ABD -> BIST (bilgi).
#   Alt küme (yalnız ANA): hedefte küçükler (60 günlük işlem değeri alt üçte bir).
# KARAR (önceden): 'ABD ÖNCÜLÜK İZİ' = ANA çeşit ABD -> AVR, AVR 2023 ve 2024-26'da FI_OLCUT dört şartı tutar VE aynı çeşit AVR -> ABD iki
#   ABD hücresinin en az birinde tutmaz. ANA dışı bir çeşit ancak 2016-22'de de tutarsa iz sayılabilir (çok deneme düzeltmesi).
FI_K39 = {"uye_min": 5, "likit_gun": 60, "ayri": 60, "ana": (20, 0.10, True),
          "cesit": [(20, 0.10, True), (20, 0.10, False), (20, 0.20, True), (20, 0.20, False), (60, 0.10, True), (60, 0.10, False),
                    (60, 0.20, True), (60, 0.20, False)],
          "yon": [("ABD", "AVR"), ("AVR", "ABD"), ("ABD", "BIST")],
          "donem": (("2016-22", "2016-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31")),
          "bist": {"XBANK": "BANKA", "XSGRT": "SIGORTA", "XFINK": "FINANS", "XYORT": "FINANS", "XHOLD": "FINANS", "XAKUR": "FINANS",
                   "XVARLIK": "FINANS", "XGMYO": "GAYRIMENKUL", "XSAGLIK": "SAGLIK", "XBLSM": "TEKNOLOJI", "XILTM": "KAMU_TELEKOM",
                   "XELKT": "KAMU_TELEKOM", "XKMYA": "KIMYA", "XMANA": "MADEN", "XMADN": "MADEN", "XMESY": "SANAYI", "XINSA": "SANAYI",
                   "XSAVUNMA": "SANAYI", "XKAGT": "SANAYI", "XGIDA": "TUKETIM", "XTCRT": "TUKETIM", "XTEKS": "TUKETIM", "XTRZM": "TUKETIM",
                   "XSPOR": "TUKETIM", "XYAYIN": "TUKETIM", "XKIRALAMA": "TUKETIM", "XULAS": "ULASIM"}}
_FI_K39_KURAL: List[Tuple[str, Tuple[str, ...]]] = [
    ("BANKA", ("bank",)), ("SIGORTA", ("insurance",)),
    ("GAYRIMENKUL", ("reit", "real estate", "home construction", "residential construction", "household goods & home")),
    ("FINANS", ("asset management", "capital markets", "credit", "financial", "investment", "equity investments", "collective", "hedge",
                "mortgage finance", "exchanges")),
    ("SAGLIK", ("health", "pharma", "biotech", "medical", "drug manufacturers", "diagnostics")),
    ("ENERJI", ("oil", "gas", "coal", "energy", "uranium", "solar")),
    ("ULASIM", ("airline", "airport", "shipping", "freight", "trucking", "railroad", "transportation")),
    ("MADEN", ("metal", "mining", "steel", "copper", "aluminum", "gold", "silver", "basic resources", "precious")),
    ("KIMYA", ("chemical",)),
    ("TEKNOLOJI", ("software", "semiconductor", "computer", "electronic", "information technology", "internet", "technology",
                   "communication equipment", "scientific", "digital")),
    ("KAMU_TELEKOM", ("utilities", "utility", "electricity", "water", "telecom")),
    ("TUKETIM", ("consumer", "retail", "food", "beverage", "apparel", "footwear", "household", "personal", "luxury", "restaurant", "leisure",
                 "travel", "lodging", "gambling", "casino", "media", "entertainment", "advertising", "publishing", "broadcasting", "auto",
                 "confectioner", "grocery", "tobacco", "education", "recreational", "furnishings", "department", "discount", "staples")),
    ("SANAYI", ("industrial", "machinery", "aerospace", "defen", "engineering", "construction", "building", "electrical", "conglomerate",
                "packaging", "waste", "pollution", "security", "staffing", "consulting", "business", "rental", "tools", "metal fabrication",
                "support services", "general")),
]


def fi_k39_kaba(etiket: str) -> Optional[str]:
    """Sektör etiketi -> kaba grup (ilk eşleşen kural); eşleşmezse None."""
    e = str(etiket).lower()
    for grup, anahtarlar in _FI_K39_KURAL:
        if any(a in e for a in anahtarlar):
            return grup
    return None


def fi_k39_gruplar(pazar: str, V: Dict[str, pd.DataFrame], K: Dict[str, Any] = FI_K39, avr_liste: Optional[pd.DataFrame] = None) -> Dict[str, str]:
    """{sembol: kaba grup} pazar başına (BIST alt endeks tablosu; ABD endustri; AVR Wikipedia ICB etiketi)."""
    if pazar == "BIST":
        sek = fi_k14_sektor("BIST"); m = {s: K["bist"].get(a) for s, a in sek.items()}
    elif pazar == "ABD":
        m = {s: fi_k39_kaba(a) for s, a in fi_k14_sektor("ABD").items()}
    else:
        m = {str(r.kod): fi_k39_kaba(r.sektor) for r in avr_liste.itertuples()}
    return {s: g for s, g in m.items() if g and s in V}


def fi_k39_sepet(V: Dict[str, pd.DataFrame], grup: Dict[str, str], P: int, K: Dict[str, Any] = FI_K39) -> Tuple[pd.DataFrame, pd.Series]:
    """Grup başına göreli sepet getirisi (P günlük, eşit ağırlık, pazar medyanı çıkarılmış) ve mutlak sepet getirisi."""
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index().ffill(limit=5); r = C / C.shift(P) - 1; piy = r.median(axis=1)
    uy: Dict[str, List[str]] = {}
    for s, g in grup.items():
        if s in r.columns:
            uy.setdefault(g, []).append(s)
    mut = pd.DataFrame({g: r[u].mean(axis=1) for g, u in uy.items() if len(u) >= K["uye_min"]})
    return mut.sub(piy, axis=0), mut


def fi_k39_sinyal(lid_rel: pd.DataFrame, lid_mut: pd.DataFrame, hed_rel: pd.DataFrame, E: float, henuz: bool) -> Dict[str, List[pd.Timestamp]]:
    """Grup başına sinyal günleri (lider takvimi): lider göreli >= E ve sepet > 0 [ve hedef göreli (lider gününe kadar bilinen) < E/2]."""
    out = {}
    for g in lid_rel.columns:
        if g not in hed_rel.columns:
            continue
        sart = (lid_rel[g] >= E) & (lid_mut[g] > 0)
        if henuz:
            h = hed_rel[g].reindex(lid_rel.index, method="ffill"); sart &= (h < E / 2)
        gec = sart & ~sart.shift(1).fillna(False).astype(bool)
        out[g] = list(gec[gec].index)
    return out


def fon_izi_k39(Vs: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], avr_liste: pd.DataFrame, A: Optional[FIAyar] = None,
                K: Dict[str, Any] = FI_K39, O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K39 sürücü: yönler x çeşitler; ana çeşitte küçükler alt kümesi. Çıktı k39_ozet.csv, k39_grup.csv."""
    A = A or FIAyar(); G = {pz: fi_k39_gruplar(pz, Vs[pz], K, avr_liste) for pz in Vs}
    say = pd.DataFrame([{"pazar": pz, "grup": g, "uye": n} for pz, m in G.items() for g, n in pd.Series(m).value_counts().items()])
    filog.info("K39 grup üyeleri:\n%s", say.pivot(index="grup", columns="pazar", values="uye").fillna(0).astype(int).to_string())
    sep: Dict[Tuple[str, int], Tuple[pd.DataFrame, pd.DataFrame]] = {}
    for pz in Vs:
        for P in sorted({c[0] for c in K["cesit"]}):
            sep[(pz, P)] = fi_k39_sepet(Vs[pz], G[pz], P, K)
    L: Dict[str, pd.Series] = {}
    for pz in Vs:
        Tl = pd.DataFrame({s: d.Close * d.Volume * (d["Kur"] if "Kur" in d else 1.0) for s, d in Vs[pz].items()}).sort_index()
        L[pz] = Tl.rolling(K["likit_gun"], min_periods=40).median()
    Z = []
    for lid, hed in K["yon"]:
        if lid not in Vs or hed not in Vs:
            continue
        gun = pd.DatetimeIndex(sorted(set().union(*[d.index for d in Vs[hed].values()]))); uy: Dict[str, List[str]] = {}
        for s, g in G[hed].items():
            uy.setdefault(g, []).append(s)
        for P, E, henuz in K["cesit"]:
            S = fi_k39_sinyal(sep[(lid, P)][0], sep[(lid, P)][1], sep[(hed, P)][0], E, henuz); OL = []
            for g, gl in S.items():
                for t in gl:
                    j = int(gun.searchsorted(t, side="right"))
                    if j >= len(gun):
                        continue
                    for s in uy.get(g, []):
                        if gun[j] in Vs[hed][s].index:
                            OL.append({"grup": g, "sembol": s, "sinyal": t, "giris": gun[j]})
            X = pd.DataFrame(OL)
            if not len(X):
                continue
            kumeler = {"hepsi": X}
            if (P, E, henuz) == K["ana"]:
                rk = L[hed].rank(axis=1, pct=True); rix = rk.index          # denetim 28 Eki: giriş - 1 takvim günü hafta sonuna düşüyordu
                def _kucuk(s: str, g: pd.Timestamp) -> bool:
                    j0 = int(rix.searchsorted(g)) - 1
                    return bool(j0 >= 0 and s in rk.columns and pd.notna(rk.iat[j0, rk.columns.get_loc(s)]) and rk.iat[j0, rk.columns.get_loc(s)] <= 1 / 3)
                X["kucuk"] = [_kucuk(s, g) for s, g in zip(X.sembol, X.giris)]
                kumeler["kucukler"] = X[X.kucuk]
            for kad, Xk in kumeler.items():
                Xk = Xk.sort_values("giris").assign(_b=True).reset_index(drop=True)
                Ev = fi_k27_tekil(Xk, "_b", Vs[hed], K["ayri"]); T = fi_olcut_olay(Pn[hed], Ev[["sembol", "giris"]])
                for dn, a, b in K["donem"]:
                    Z.append({"yon": f"{lid}->{hed}", "P": P, "E": E, "henuz": henuz, "kume": kad, "pazar": hed, "donem": dn,
                              "n_sinyal": sum(len(v) for v in S.values()), **fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)})
    Z = pd.DataFrame(Z)

    def tut(r) -> bool:
        return bool(r.n >= O["n_esik"] and r.alt95 > 0 and r.sira > 0.5 and r.portfoy > r.portfoy_esli_p90)
    P0, E0, H0 = K["ana"]
    def hucreler(yon: str, P: int, E: float, henuz: bool, kume: str = "hepsi") -> Dict[str, bool]:
        g = Z[(Z.yon == yon) & (Z.P == P) & (Z.E == E) & (Z.henuz == henuz) & (Z.kume == kume)]
        return {r.donem: tut(r) for r in g.itertuples()}
    ana = hucreler("ABD->AVR", P0, E0, H0); ayna = hucreler("AVR->ABD", P0, E0, H0)
    karar = {"ana": "ABD ÖNCÜLÜK İZİ" if ana.get("2023") and ana.get("2024-26") and not (ayna.get("2023") and ayna.get("2024-26")) else "İZ DEĞİL",
             "ana_hucre": ana, "ayna_hucre": ayna}
    olasilik = {}
    for P, E, henuz in K["cesit"]:
        h = hucreler("ABD->AVR", P, E, henuz); a = hucreler("AVR->ABD", P, E, henuz)
        olasilik[(P, E, henuz)] = {"AVR": h, "ayna": a, "iz": bool(h.get("2016-22") and h.get("2023") and h.get("2024-26")
                                                                        and not (a.get("2023") and a.get("2024-26")))}
    karar["olasilik"] = olasilik
    Z.drop(columns=[c for c in Z if c.startswith("_")]).to_csv(os.path.join(A.cikti, "k39_ozet.csv"), index=False)
    say.to_csv(os.path.join(A.cikti, "k39_grup.csv"), index=False)
    return {"ozet": Z, "karar": karar, "grup": say}

# K40 SAAT FARKI: ABD YÜKSELİŞİ AVRUPA'YA NE KADAR GECİKMELİ GEÇER, GECİKMEDEN ALIM KAZANDIRIR MI (Cemal 28 Eki: 'Avrupa ile Amerika
# arasında gün değil saat farkı; Amerika'da yükseliş yapan Avrupa'da ne kadar gecikmeli, bu gecikme esas alınıp alım yapılır mı').
# ÖNCEDEN YAZILDI (sonuç görülmeden). Saat sırası (TR): Avrupa 10:00-18:30, ABD 16:30-23:00; örtüşme 16:30-18:30. ABD'nin Avrupa
# kapanışından sonraki hareketi (18:30-23:00 TR) Avrupa'ya ancak ertesi sabah açılış BOŞLUĞUNDA ya da gün içinde geçebilir. Alınabilir
# olan yalnız açılıştan sonrasıdır; boşluk alınamaz.
# A) GÜNLÜK, HİSSE DÜZEYİ 2016-26 (V_ABD, V_AVR): ABD eşit ağırlık günlük getirisi >= +%1,5 (güçlü gün d) -> Avrupa eşit ağırlık ertesi gün
#    (ilk işlem günü): BOŞLUK = açılış(d+1) / kapanış(d) - 1, GÜN İÇİ = kapanış(d+1) / açılış(d+1) - 1, 5 GÜN = kapanış(d+5) / açılış(d+1) - 1.
#    Taban = bütün günlerin aynı ölçüleri. Fazla = sinyal ortalaması - taban; ay kümeli bootstrap %95. Dönemler 2016-22, 2023, 2024-26.
#    Sektör: ABD kaba sektör sepeti (K39) günlük göreli >= +%2 -> Avrupa aynı sektör göreli (sektör sepeti - Avrupa medyanı) gün içi ve 5 gün.
#    Ayna (bilgi): güçlü ABD düşüşü (<= -%1,5) -> Avrupa ertesi gün.
# B) SAATLİK, ENDEKS (Yahoo 1 saat, son 730 gün; ^GSPC lider, ^STOXX50E / ^GDAXI / ^FTSE hedef): ABD'nin Avrupa kapanışından (11:30 ET)
#    kendi kapanışına (16:00 ET) hareketi >= +%0,7 -> Avrupa ertesi gün: boşluk (önceki kapanış -> açılış), İLK SAAT (açılış -> +1 saat),
#    GÜN (açılış -> kapanış). Taban = bütün günler. Örtüşme bilgisi: ABD ilk 2 saat (9:30-11:30 ET) ile Avrupa aynı gün son 2 saati
#    korelasyonu (eşzamanlı fiyatlama kanıtı).
# KARAR (önceden): 'ALINABİLİR GECİKME' = A'da Avrupa GÜN İÇİ fazlası >= +%0,2 ve alt uç > 0 hem 2023 hem 2024-26'da VE B'de GÜN fazlası
#    >= +%0,2 ve alt uç > 0 en az iki endekste. Boşluk fazlası büyük ama gün içi fazlası yoksa: 'GECİKME YOK, AÇILIŞTA FİYATLANIYOR'.
#    Maliyet notu: büyük Avrupa hissesinde gidiş-dönüş ~%0,1; fazla bunun altındaysa kazanç yok.
FI_K40 = {"abd_gun": 0.015, "sektor_gun": 0.02, "saat_esik": 0.007, "fazla_esik": 0.002, "bootstrap": 2000, "tohum": 40,
          "endeks": {"lider": "^GSPC", "hedef": ("^STOXX50E", "^GDAXI", "^FTSE")}, "bes": 5,
          "donem": (("2016-22", "2016-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31"))}


def _fi_k40_fazla(x: pd.Series, taban: pd.Series, rng: np.random.Generator, n_boot: int) -> Dict[str, float]:
    """x: sinyal günleri ölçüsü (tarih indeksli), taban: bütün günler. Fazla = ort(x) - ort(taban), ay kümeli bootstrap (x üzerinde)."""
    x = x.dropna(); t = taban.dropna()
    if len(x) < 10 or len(t) < 30:
        return {"n": int(len(x)), "fazla": np.nan, "alt95": np.nan, "ust95": np.nan, "ort": float(x.mean()) if len(x) else np.nan, "taban": float(t.mean()) if len(t) else np.nan}
    ay = x.index.to_period("M").astype(str).to_numpy(); aylar = np.unique(ay); grup = {a: x.to_numpy()[ay == a] for a in aylar}; bs = []
    for _ in range(n_boot):
        sec = rng.choice(aylar, len(aylar), replace=True); bs.append(np.concatenate([grup[a] for a in sec]).mean() - t.mean())
    return {"n": int(len(x)), "fazla": float(x.mean() - t.mean()), "alt95": float(np.quantile(bs, 0.025)), "ust95": float(np.quantile(bs, 0.975)),
            "ort": float(x.mean()), "taban": float(t.mean())}


def fi_k40_gunluk(Va: Dict[str, pd.DataFrame], Vr: Dict[str, pd.DataFrame], Ga: Dict[str, str], Gr: Dict[str, str],
                  K: Dict[str, Any] = FI_K40) -> pd.DataFrame:
    """A) günlük: ABD güçlü gün / güçlü düşüş / sektör günü -> Avrupa ertesi gün boşluk, gün içi, 5 gün (pazar ve sektör düzeyi)."""
    rng = np.random.default_rng(K["tohum"])
    Ca = pd.DataFrame({s: d.Close for s, d in Va.items()}).sort_index(); ra = (Ca / Ca.shift(1) - 1)
    Co = pd.DataFrame({s: d.Close for s, d in Vr.items()}).sort_index(); Oo = pd.DataFrame({s: d.Open for s, d in Vr.items()}).sort_index()
    abd_gun = ra.mean(axis=1)                                                     # eşit ağırlık ABD günü
    bosluk = (Oo / Co.shift(1) - 1).mean(axis=1); gunici = (Co / Oo - 1).mean(axis=1); bes = (Co.shift(-K["bes"] + 1) / Oo - 1).mean(axis=1)
    avr_gun = Co.index
    def ertesi(t: pd.Timestamp) -> Optional[pd.Timestamp]:
        j = int(avr_gun.searchsorted(t, side="right")); return avr_gun[j] if j < len(avr_gun) else None
    Z = []
    sinyaller = {"ABD_guclu_gun": abd_gun[abd_gun >= K["abd_gun"]].index, "ABD_guclu_dusus_ayna": abd_gun[abd_gun <= -K["abd_gun"]].index}
    for ad, gl in sinyaller.items():
        e = list(dict.fromkeys(x for x in (ertesi(t) for t in gl) if x is not None))   # denetim 28 Eki: çift sayım yok
        for dn, a, b in K["donem"]:
            m = [x for x in e if pd.Timestamp(a) <= x <= pd.Timestamp(b)]; t_ = (bosluk.index >= a) & (bosluk.index <= b)
            for olcu, ser in (("bosluk", bosluk), ("gun_ici", gunici), ("bes_gun", bes)):
                Z.append({"duzey": "pazar", "sinyal": ad, "olcu": olcu, "donem": dn, **_fi_k40_fazla(ser.reindex(m), ser[t_], rng, K["bootstrap"])})
    # sektör düzeyi
    ua: Dict[str, List[str]] = {}; ur: Dict[str, List[str]] = {}
    for s, g in Ga.items():
        if s in ra.columns:
            ua.setdefault(g, []).append(s)
    for s, g in Gr.items():
        if s in Co.columns:
            ur.setdefault(g, []).append(s)
    piy_a = ra.median(axis=1); gi_med = (Co / Oo - 1).median(axis=1); b5_med = (Co.shift(-K["bes"] + 1) / Oo - 1).median(axis=1)
    sx: Dict[str, List[Tuple[pd.Timestamp, str]]] = {"gun_ici": [], "bes_gun": []}; tab = {"gun_ici": [], "bes_gun": []}
    for g in ua:
        if g not in ur or len(ua[g]) < 5 or len(ur[g]) < 5:
            continue
        rel_a = ra[ua[g]].mean(axis=1) - piy_a; gi = (Co[ur[g]] / Oo[ur[g]] - 1).mean(axis=1) - gi_med
        b5 = (Co[ur[g]].shift(-K["bes"] + 1) / Oo[ur[g]] - 1).mean(axis=1) - b5_med
        tab["gun_ici"].append(gi.rename(g)); tab["bes_gun"].append(b5.rename(g))
        for t in rel_a[rel_a >= K["sektor_gun"]].index:
            x = ertesi(t)
            if x is not None:
                sx["gun_ici"].append((x, float(gi.get(x, np.nan)))); sx["bes_gun"].append((x, float(b5.get(x, np.nan))))
    for olcu in ("gun_ici", "bes_gun"):
        X = pd.Series([v for _, v in sx[olcu]], index=pd.DatetimeIndex([t for t, _ in sx[olcu]])); T = pd.concat(tab[olcu], axis=1).stack()
        T.index = T.index.get_level_values(0)
        for dn, a, b in K["donem"]:
            Z.append({"duzey": "sektor", "sinyal": "ABD_sektor_gunu", "olcu": olcu, "donem": dn,
                      **_fi_k40_fazla(X[(X.index >= a) & (X.index <= b)], T[(T.index >= a) & (T.index <= b)], rng, K["bootstrap"])})
    return pd.DataFrame(Z)


def fi_k40_saatlik_indir(K: Dict[str, Any] = FI_K40) -> Dict[str, pd.DataFrame]:
    """Yahoo 1 saatlik endeks verisi (son 730 gün), zaman damgaları yerel borsa saatinde (tz korunur)."""
    import yfinance as yf
    out = {}
    for t in (K["endeks"]["lider"],) + tuple(K["endeks"]["hedef"]):
        d = yf.download(t, period="730d", interval="1h", progress=False, auto_adjust=False)
        if isinstance(d.columns, pd.MultiIndex):
            d.columns = d.columns.get_level_values(0)
        out[t] = d[["Open", "High", "Low", "Close"]].dropna()
    return out


def fi_k40_saatlik(H: Dict[str, pd.DataFrame], K: Dict[str, Any] = FI_K40) -> pd.DataFrame:
    """B) saatlik: ABD geç seans (11:30 -> 16:00 ET, Avrupa kapandıktan sonra) >= eşik -> Avrupa ertesi gün boşluk / ilk saat / gün."""
    rng = np.random.default_rng(K["tohum"]); L = H[K["endeks"]["lider"]].copy(); L["gun"] = L.index.tz_convert("America/New_York").date
    gec = {}
    for g, x in L.groupby("gun"):
        saat = x.index.tz_convert("America/New_York").hour + x.index.tz_convert("America/New_York").minute / 60
        a = x[(saat >= 11.4) & (saat <= 11.6)]; b = x[saat >= 15.4]     # denetim 28 Eki: 11:30 barının AÇILIŞI (bar zamanı = başlangıç)
        if len(a) and len(b):
            gec[pd.Timestamp(g)] = float(b.Close.iloc[-1] / a.Open.iloc[0] - 1)
    gec = pd.Series(gec).sort_index(); Z = []
    for t in K["endeks"]["hedef"]:
        E = H[t].copy(); E["gun"] = E.index.tz_convert(E.index.tz).date; sat = []
        gunler = sorted(set(E.gun)); onceki_kapanis = None
        for g in gunler:
            x = E[E.gun == g].sort_index()
            if onceki_kapanis is not None and len(x) >= 2:
                sat.append({"gun": pd.Timestamp(g), "bosluk": x.Open.iloc[0] / onceki_kapanis - 1, "ilk_saat": x.Close.iloc[0] / x.Open.iloc[0] - 1,
                            "gun_ici": x.Close.iloc[-1] / x.Open.iloc[0] - 1})
            onceki_kapanis = float(x.Close.iloc[-1])
        D = pd.DataFrame(sat).set_index("gun")
        # sinyal: ABD günü g_abd -> Avrupa'nın g_abd'den sonraki ilk günü
        sg = gec[gec >= K["saat_esik"]].index; ix = D.index
        e = list(dict.fromkeys(ix[int(ix.searchsorted(t_, side="right"))] for t_ in sg if int(ix.searchsorted(t_, side="right")) < len(ix)))
        for olcu in ("bosluk", "ilk_saat", "gun_ici"):
            Z.append({"endeks": t, "olcu": olcu, **_fi_k40_fazla(D[olcu].reindex(e), D[olcu], rng, K["bootstrap"])})
        # örtüşme: ABD ilk 2 saat (9:30-11:30 ET) ile Avrupa aynı gün son 2 saati korelasyonu
        ilk2 = {}
        for g, x in L.groupby("gun"):
            saat = x.index.tz_convert("America/New_York").hour + x.index.tz_convert("America/New_York").minute / 60
            a = x[saat <= 9.6]; b = x[(saat >= 11.4) & (saat <= 11.6)]
            if len(a) and len(b):
                ilk2[pd.Timestamp(g)] = float(b.Open.iloc[0] / a.Open.iloc[0] - 1)       # 9:30 açılış -> 11:30 (barın açılışı)
        son2 = {}
        for g, x in E.groupby("gun"):
            if len(x) >= 3:
                son2[pd.Timestamp(g)] = float(x.Close.iloc[-1] / x.Close.iloc[-3] - 1)
        c = pd.concat([pd.Series(ilk2).rename("abd"), pd.Series(son2).rename("avr")], axis=1).dropna()
        Z.append({"endeks": t, "olcu": "ortusme_korelasyon", "n": int(len(c)), "fazla": float(c.abd.corr(c.avr)) if len(c) > 10 else np.nan})
    return pd.DataFrame(Z)


def fon_izi_k40(Va: Dict[str, pd.DataFrame], Vr: Dict[str, pd.DataFrame], avr_liste: pd.DataFrame, H: Optional[Dict[str, pd.DataFrame]] = None,
                A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K40) -> Dict[str, Any]:
    """K40 sürücü: A günlük + B saatlik; karar önceden. Çıktı k40_gunluk.csv, k40_saatlik.csv."""
    A = A or FIAyar(); Ga = fi_k39_gruplar("ABD", Va); Gr = fi_k39_gruplar("AVR", Vr, avr_liste=avr_liste)
    Zg = fi_k40_gunluk(Va, Vr, Ga, Gr, K); H = H or fi_k40_saatlik_indir(K); Zs = fi_k40_saatlik(H, K)
    def ok_g(dn: str) -> bool:
        r = Zg[(Zg.duzey == "pazar") & (Zg.sinyal == "ABD_guclu_gun") & (Zg.olcu == "gun_ici") & (Zg.donem == dn)]
        return bool(len(r) and r.fazla.iat[0] >= K["fazla_esik"] and r.alt95.iat[0] > 0)
    s_ok = Zs[(Zs.olcu == "gun_ici") & (Zs.fazla >= K["fazla_esik"]) & (Zs.alt95 > 0)]
    bos = Zs[(Zs.olcu == "bosluk")]
    karar = ("ALINABİLİR GECİKME" if ok_g("2023") and ok_g("2024-26") and len(s_ok) >= 2 else
             ("GECİKME YOK, AÇILIŞTA FİYATLANIYOR" if len(bos) and (bos.alt95 > 0).all() else "İZ DEĞİL"))
    Zg.to_csv(os.path.join(A.cikti, "k40_gunluk.csv"), index=False); Zs.to_csv(os.path.join(A.cikti, "k40_saatlik.csv"), index=False)
    return {"gunluk": Zg, "saatlik": Zs, "karar": karar}

# K41 DÖRT ÇALIŞMA (Cemal 28 Eki: 'd ve e seçeneklerini yap; K40 sektör 5 gün kalıntısını dış örnekle ayrıca ölç; eski adamların icat ettiği
# formasyonlar (Bollinger, RSI, MACD, Fibonacci) başarılı mı, benim çölüm halüsinasyon mu?'). ÖNCEDEN YAZILDI (sonuç görülmeden).
# Karar pazarları ABD + AVR (BIST bilgi). Olay = sinyal günü, giriş ertesi açılış, hissede 60 günde tek, FI_OLCUT.
# A) KLASİKLER (fiyat-hacim, üç pazar):
#   A1 Bollinger alt bant dönüşü: dün kapanış < SMA20 - 2σ, bugün kapanış bandın içinde -> yukarı. A2 Bollinger üst bant: kapanış >
#      SMA20 + 2σ -> kaçınma (satış sinyali). A3 RSI14 < 30 -> yukarı. A4 RSI14 > 70 -> kaçınma. A5 MACD(12,26) sinyal çizgisini (9)
#      yukarı keser ve MACD < 0 -> yukarı. A6 Altın kesişim SMA50 > SMA200 (geçiş) -> yukarı. A7 Ölüm kesişimi -> kaçınma.
#   A8 Fibonacci %61,8: son 120 günde dip -> tepe (tepe >= dip x 1,3), tepe sonra; fiyat 61,8 düzeltme seviyesine +-%2 geldi ve bugün
#      kapanış dünden yüksek (dönüş) -> yukarı. Her kural için fi_olcut_karar / _kacinma.
# B) RÜZGÂR SÜREKLİLİĞİ (kapalı 'sektör ısısı', Cemal 'd'yi yap' dedi): sektör rüzgârı başlangıcı = D9b rüzgârı (fi_k14_ruzgar; hisse
#   hariç sepet) sektör üyelerinin çoğunluğunda ilk kez görülen gün (fi_k36_sektor_ruzgar geçişi). Olay: o gün sektörün bütün üyeleri.
#   Ölçü: FI_OLCUT eşli fark (eşler momentum beşliği + likidite: hissenin kendi momentumu düşülmüş; 'rüzgâr momentumun üstüne ne katıyor')
#   ve bilgi olarak HAM fark (r60 - pazar medyanı r60). Alt küme: rüzgâr başlamadan önceki 60 günde K24 çöl sinyali vermiş üyeler (çöl +
#   rüzgâr, Cemal'in tanımı). Karar fi_olcut_karar.
# C) ABD ÇÖL ADAYI SÜZGECİ (olay verisi; Avrupa'da yok -> en fazla ABD-ADAY): K24 çöl sinyalleri ABD. C1 son 60 günde iyi bilanço tepkisi
#   (K28 'ust', tepki_son <= sinyal); C2 son 90 günde içeriden açık piyasa alımı (K30, D <= sinyal); C3 temiz temel (K31 son bildirim:
#   pay artışı < %10 ve (ocf >= 0 ya da pist >= 8)); C4 = C1 ve C3; C5 = C2 ve C3; C0 hepsi (taban). İki ABD hücresi tutarsa ABD-ADAY.
# D) K40 SEKTÖR 5 GÜN KALINTISI DIŞ ÖRNEK + MALİYET: aynı ölçü (ABD sektör günü >= +%2 göreli -> Avrupa aynı sektör 5 gün göreli), hücreler
#   2016-19, 2020-22, 2023, 2024-26; 'KALINTI SAĞLAM' = dört hücrede (fazla - %0,1) > 0 ve alt uç > %0,1. BIST hedef bilgi.
FI_K41 = {"ayri": 60, "bb_n": 20, "bb_k": 2.0, "rsi_alt": 30.0, "rsi_ust": 70.0, "fib_pencere": 120, "fib_kat": 1.3, "fib_tol": 0.02,
          "col_once": 60, "bilanco_gun": 60, "alim_gun": 90, "maliyet": 0.001,
          "d_donem": (("2016-19", "2016-01-01", "2019-12-31"), ("2020-22", "2020-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"),
                      ("2024-26", "2024-01-01", "2026-12-31"))}


def fi_k41_klasik(d: pd.DataFrame, K: Dict[str, Any] = FI_K41) -> Dict[str, List[pd.Timestamp]]:
    """Bir hissede A1..A8 sinyal günleri."""
    c = d.Close.astype(float); n = K["bb_n"]; sma = c.rolling(n).mean(); sd = c.rolling(n).std(); alt = sma - K["bb_k"] * sd; ust = sma + K["bb_k"] * sd
    rsi = _fi_k38b_rsi(c); macd = _fi_ema(c, 12) - _fi_ema(c, 26); sig = _fi_ema(macd, 9); s50 = c.rolling(50).mean(); s200 = c.rolling(200).mean()
    out = {"A1_bollinger_alt_donus": c.index[((c.shift(1) < alt.shift(1)) & (c >= alt)).fillna(False)],
           "A2_bollinger_ust_kacinma": c.index[(c > ust).fillna(False)], "A3_rsi30": c.index[(rsi < K["rsi_alt"]).fillna(False)],
           "A4_rsi70_kacinma": c.index[(rsi > K["rsi_ust"]).fillna(False)],
           "A5_macd_kesisim": c.index[((macd > sig) & (macd.shift(1) <= sig.shift(1)) & (macd < 0)).fillna(False)],
           "A6_altin_kesisim": c.index[((s50 > s200) & (s50.shift(1) <= s200.shift(1))).fillna(False)],
           "A7_olum_kesisim_kacinma": c.index[((s50 < s200) & (s50.shift(1) >= s200.shift(1))).fillna(False)]}
    cv = c.to_numpy(); fib = []; P = K["fib_pencere"]
    for t in range(P, len(cv)):
        seg = cv[t - P:t]; j_dip = int(np.argmin(seg)); tepe = seg[j_dip:].max() if j_dip < P - 1 else np.nan
        if not np.isfinite(tepe) or tepe < seg[j_dip] * K["fib_kat"]:
            continue
        sev = tepe - 0.618 * (tepe - seg[j_dip])
        if abs(cv[t] / sev - 1) <= K["fib_tol"] and cv[t] > cv[t - 1] and cv[t - 1] <= sev * (1 + K["fib_tol"]):
            fib.append(c.index[t])
    out["A8_fibonacci_618"] = fib
    return {k: list(v) for k, v in out.items()}


def _fi_k41_olc(S: pd.DataFrame, V: Dict[str, pd.DataFrame], P: Dict[str, Any], pz: str, ad: str, K: Dict[str, Any], O: Dict[str, Any],
                ham: bool = False) -> List[Dict[str, Any]]:
    """S: sembol, gun -> giriş ertesi açılış, tekil, FI_OLCUT hücreleri (ham=True: r60 - pazar medyanı da)."""
    if not len(S):
        return []
    gun = pd.DatetimeIndex(sorted(set().union(*[d.index for d in V.values()]))); j = gun.searchsorted(pd.DatetimeIndex(S.gun), side="right")
    ok = j < len(gun); S = S[ok].assign(giris=gun[j[ok]]); S = S[[g in V[s].index for s, g in zip(S.sembol, S.giris)]]
    S = S.sort_values("giris").assign(_b=True).reset_index(drop=True); E = fi_k27_tekil(S, "_b", V, K["ayri"])
    T = fi_olcut_olay(P, E[["sembol", "giris"]]); Z = []
    if ham:
        ti = {t: i for i, t in enumerate(P["tarih"])}
        T["ham"] = [T.r60.iat[k] - float(np.nanmedian(P["R"][ti[g]][P["ok"][ti[g]]])) if g in ti else np.nan for k, g in enumerate(T.giris)]
    for dn, a, b in O["donem"]:
        Td = T[(T.giris >= a) & (T.giris <= b)]; h = fi_olcut_hucre(Td, O)
        if ham and len(Td):
            h["ham_fark"] = float(Td.ham.mean())
        Z.append({"sinyal": ad, "pazar": pz, "donem": dn, **h})
    return Z


def fon_izi_k41(Vs: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], avr_liste: pd.DataFrame, X28: pd.DataFrame,
                alim: pd.DataFrame, Fin: pd.DataFrame, A: Optional[FIAyar] = None, K: Dict[str, Any] = FI_K41, O: Dict[str, Any] = FI_OLCUT
                ) -> Dict[str, Any]:
    """K41 sürücü: A klasikler, B rüzgâr sürekliliği, C ABD çöl süzgeci, D K40 kalıntısı. Çıktı k41_a/b/c/d.csv."""
    A = A or FIAyar(); out: Dict[str, Any] = {}
    # A
    Za = []
    for pz, V in Vs.items():
        S: Dict[str, List[Tuple[str, pd.Timestamp]]] = {}
        for s, d in V.items():
            if len(d) < 260:
                continue
            for k, L in fi_k41_klasik(d, K).items():
                S.setdefault(k, []).extend((s, t) for t in L)
        for k, L in S.items():
            Za += _fi_k41_olc(pd.DataFrame(L, columns=["sembol", "gun"]), V, Pn[pz], pz, k, K, O)
    Za = pd.DataFrame(Za)
    out["A"] = {"ozet": Za, "karar": {k: (fi_olcut_karar_kacinma if k.endswith("kacinma") else fi_olcut_karar)(Za[Za.sinyal == k], O) for k in Za.sinyal.unique()}}
    # B
    Zb = []
    for pz, V in Vs.items():
        sek = fi_k39_gruplar(pz, V, avr_liste=avr_liste) if pz == "AVR" else fi_k14_sektor(pz)
        sek = {s: a for s, a in sek.items() if s in V}; W = fi_k14_ruzgar(V, sek); uy: Dict[str, List[str]] = {}
        for s, a in sek.items():
            uy.setdefault(a, []).append(s)
        col: Dict[str, pd.DatetimeIndex] = {}
        for s, d in V.items():
            try:
                T = fi_k24_tara(d); col[s] = pd.DatetimeIndex(T[T.kural].tarih) if len(T) and "kural" in T else pd.DatetimeIndex([])
            except Exception:
                col[s] = pd.DatetimeIndex([])
        L_h, L_c = [], []
        for a, u in uy.items():
            if len(u) < FI_K14_ESIK["ruz_uye"]:
                continue
            G = fi_k36_sektor_ruzgar(W, u); gec = G & ~G.shift(1).fillna(False).astype(bool)
            for t in gec[gec].index:
                for s in u:
                    L_h.append((s, t))
                    if ((col[s] <= t) & (col[s] >= t - pd.Timedelta(days=int(K["col_once"] * 1.45)))).any():
                        L_c.append((s, t))
        Zb += _fi_k41_olc(pd.DataFrame(L_h, columns=["sembol", "gun"]), V, Pn[pz], pz, "B1_ruzgar_baslangici_uyeler", K, O, ham=True)
        Zb += _fi_k41_olc(pd.DataFrame(L_c, columns=["sembol", "gun"]), V, Pn[pz], pz, "B2_col_sonra_ruzgar", K, O, ham=True)
    Zb = pd.DataFrame(Zb)
    out["B"] = {"ozet": Zb, "karar": {k: fi_olcut_karar(Zb[Zb.sinyal == k], O) for k in Zb.sinyal.unique()}} if len(Zb) else {"ozet": Zb, "karar": {}}
    # C (ABD)
    Va = Vs["ABD"]; sat = []
    for s, d in Va.items():
        try:
            T = fi_k24_tara(d)
            if len(T) and "kural" in T:
                sat += [(s, t) for t in T[T.kural].tarih]
        except Exception:
            pass
    C = pd.DataFrame(sat, columns=["sembol", "gun"])
    X = X28.assign(tepki_son=pd.to_datetime(X28.tepki_son)); iyi = {s: pd.DatetimeIndex(g.tepki_son) for s, g in X[X.ust].groupby("sembol")}
    al = {s: pd.DatetimeIndex(g.D) for s, g in alim.groupby("sembol")}; Fn = Fin.assign(filed=pd.to_datetime(Fin.filed)).sort_values("filed")
    temiz_ok = (Fn.pay_yil < 0.10) & ((Fn.ocf_ceyrek >= 0) | (Fn.pist >= 8.0)); Fn = Fn.assign(ok=temiz_ok.fillna(False))
    fin_s = {s: g for s, g in Fn.groupby("sembol")}
    def son_temel(s: str, t: pd.Timestamp) -> Optional[bool]:
        g = fin_s.get(s)
        if g is None:
            return None
        g = g[g.filed <= t]; return bool(g.ok.iloc[-1]) if len(g) else None
    C["C1"] = [((iyi.get(s, pd.DatetimeIndex([])) <= t) & (iyi.get(s, pd.DatetimeIndex([])) >= t - pd.Timedelta(days=K["bilanco_gun"]))).any() for s, t in zip(C.sembol, C.gun)]
    C["C2"] = [((al.get(s, pd.DatetimeIndex([])) <= t) & (al.get(s, pd.DatetimeIndex([])) >= t - pd.Timedelta(days=K["alim_gun"]))).any() for s, t in zip(C.sembol, C.gun)]
    C["C3"] = [bool(son_temel(s, t)) for s, t in zip(C.sembol, C.gun)]; C["C4"] = C.C1 & C.C3; C["C5"] = C.C2 & C.C3; C["C0"] = True
    Zc = []
    for k in ("C0", "C1", "C2", "C3", "C4", "C5"):
        Zc += _fi_k41_olc(C[C[k]][["sembol", "gun"]], Va, Pn["ABD"], "ABD", k, K, O)
    Zc = pd.DataFrame(Zc)
    out["C"] = {"ozet": Zc, "karar": {k: fi_olcut_karar(Zc[Zc.sinyal == k], O) for k in Zc.sinyal.unique()}, "sayim": C[["C1", "C2", "C3", "C4", "C5"]].sum().to_dict(), "n": len(C)}
    # D
    Kd = {**FI_K40, "donem": K["d_donem"]}; Ga = fi_k39_gruplar("ABD", Vs["ABD"]); Gr = fi_k39_gruplar("AVR", Vs["AVR"], avr_liste=avr_liste)
    Zd = fi_k40_gunluk(Vs["ABD"], Vs["AVR"], Ga, Gr, Kd); Zd["hedef"] = "AVR"
    if "BIST" in Vs:
        Zdb = fi_k40_gunluk(Vs["ABD"], Vs["BIST"], Ga, fi_k39_gruplar("BIST", Vs["BIST"]), Kd); Zdb["hedef"] = "BIST"; Zd = pd.concat([Zd, Zdb], ignore_index=True)
    r = Zd[(Zd.hedef == "AVR") & (Zd.duzey == "sektor") & (Zd.olcu == "bes_gun")]
    saglam = bool(len(r) == 4 and ((r.fazla - K["maliyet"]) > 0).all() and (r.alt95 > K["maliyet"]).all())
    out["D"] = {"ozet": Zd, "karar": "KALINTI SAĞLAM" if saglam else "KALINTI SAĞLAM DEĞİL"}
    for ad, R in out.items():
        R["ozet"].drop(columns=[c for c in R["ozet"] if c.startswith("_")]).to_csv(os.path.join(A.cikti, f"k41_{ad.lower()}.csv"), index=False)
    return out

# K42 BİLİNEN ETKİLER KIYASI (Cemal 28 Eki: 'hiçbir yerde iz yok, o zaman kesin sen hata yapıyorsun'). ÖNCEDEN YAZILDI (sonuç görülmeden).
# Amaç: hat, LİTERATÜRDE kırk yıldır belgelenmiş üç etkiyi görüyor mu? Görüyorsa hat sağlamdır ve 'iz yok' sonucu ölçütün sertliğinden
# gelir (eşler aynı momentum ve likidite diliminden seçilir; momentum / küçüklük gibi etkiler eşli farkta TASARIM GEREĞİ silinir).
#   E1 MOMENTUM 12-1: her ayın ilk işlem günü, son 250 günün (son 20 gün hariç) getirisi pazar içinde en yüksek onda bir -> alım.
#   E2 KISA VADE TERSİNE DÖNÜŞ: son 20 gün getirisi en düşük onda bir -> alım (1 aylık kaybedenler toparlar).
#   E3 KÜÇÜKLÜK: 60 günlük işlem değeri medyanı en düşük onda bir -> alım.
# İki cetvel: HAM = r60 - aynı gün pazar medyanı r60 (literatürün ölçtüğü); EŞLİ = FI_OLCUT (bizim ölçüt). Hücreler 2016-22 / 2023 /
# 2024-26, üç pazar. BEKLENTİ (önceden): E1 ve E3 HAM cetvelde birden çok hücrede artı ve aralık artı (hat görür), EŞLİ cetvelde sıfıra
# yakın (eşleme siler). E2 ham cetvelde ABD'de artı beklenir (literatür), BIST'te belirsiz. Hat bunları ham cetvelde görmezse HAT KUSURLU.
FI_K42 = {"dilim": 0.10, "mom_uzun": 250, "mom_kisa": 20, "likit_gun": 60, "ayri": 60,
          "donem": (("2016-22", "2016-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31"))}


def fi_k42_sinyaller(V: Dict[str, pd.DataFrame], K: Dict[str, Any] = FI_K42) -> Dict[str, pd.DataFrame]:
    """Aylık kesit sinyalleri (sembol, gun): E1 momentum, E2 tersine dönüş, E3 küçüklük (hepsi d-1'e kadar bilgi, ay başı günü)."""
    C = pd.DataFrame({s: d.Close for s, d in V.items()}).sort_index().ffill(limit=5)
    Tl = pd.DataFrame({s: d.Close * d.Volume * (d["Kur"] if "Kur" in d else 1.0) for s, d in V.items()}).sort_index()
    mom = (C.shift(K["mom_kisa"]) / C.shift(K["mom_uzun"]) - 1).shift(1); kisa = (C / C.shift(K["mom_kisa"]) - 1).shift(1)
    lik = Tl.rolling(K["likit_gun"], min_periods=40).median().shift(1)
    ay_basi = C.index.to_series().groupby(C.index.to_period("M")).min().values
    out = {}
    for ad, M, ust in (("E1_momentum_12_1", mom, True), ("E2_tersine_donus_1ay", kisa, False), ("E3_kucukluk", lik, False)):
        R = M.loc[ay_basi]; rk = R.rank(axis=1, pct=True)
        S = (rk >= 1 - K["dilim"]) if ust else (rk <= K["dilim"]); S = S & R.notna()
        st = S.stack(); st = st[st]
        out[ad] = pd.DataFrame({"sembol": st.index.get_level_values(1), "gun": st.index.get_level_values(0)})
    return out


def fon_izi_k42(Vs: Dict[str, Dict[str, pd.DataFrame]], Pn: Dict[str, Dict[str, Any]], A: Optional[FIAyar] = None,
                K: Dict[str, Any] = FI_K42, O: Dict[str, Any] = FI_OLCUT) -> Dict[str, Any]:
    """K42 sürücü: üç bilinen etki x üç pazar x üç dönem, ham ve eşli cetvel. Çıktı k42_ozet.csv."""
    A = A or FIAyar(); Od = {**O, "donem": K["donem"]}; Z = []
    for pz, V in Vs.items():
        P = Pn[pz]; ti = {t: i for i, t in enumerate(P["tarih"])}; gun = pd.DatetimeIndex(sorted(set().union(*[d.index for d in V.values()])))
        for ad, S in fi_k42_sinyaller(V, K).items():
            j = gun.searchsorted(pd.DatetimeIndex(S.gun), side="right"); ok = j < len(gun); S = S[ok].assign(giris=gun[j[ok]])
            S = S[[g in V[s].index for s, g in zip(S.sembol, S.giris)]].sort_values("giris").assign(_b=True).reset_index(drop=True)
            E = fi_k27_tekil(S, "_b", V, K["ayri"]); T = fi_olcut_olay(P, E[["sembol", "giris"]])
            T["ham"] = [T.r60.iat[k] - float(np.nanmedian(P["R"][ti[g]][P["ok"][ti[g]]])) if g in ti else np.nan for k, g in enumerate(T.giris)]
            for dn, a, b in K["donem"]:
                Td = T[(T.giris >= a) & (T.giris <= b)]; h = fi_olcut_hucre(Td, Od); hm = Td.ham.dropna()
                rng = np.random.default_rng(42); ay = Td.dropna(subset=["ham"]).giris.dt.to_period("M").astype(str).to_numpy(); aylar = np.unique(ay)
                grup = {x: hm.to_numpy()[ay == x] for x in aylar}
                bs = [np.concatenate([grup[x] for x in rng.choice(aylar, len(aylar), replace=True)]).mean() for _ in range(1000)] if len(aylar) else [np.nan]
                Z.append({"etki": ad, "pazar": pz, "donem": dn, "n": h.get("n", 0), "ham_fark": float(hm.mean()) if len(hm) else np.nan,
                          "ham_alt95": float(np.nanquantile(bs, 0.025)), "ham_ust95": float(np.nanquantile(bs, 0.975)),
                          "esli_fark": h.get("ort_fark", np.nan), "esli_alt95": h.get("alt95", np.nan), "esli_sira": h.get("sira", np.nan)})
    Z = pd.DataFrame(Z); Z["ham_tutar"] = (Z.ham_fark > 0) & (Z.ham_alt95 > 0); Z["esli_tutar"] = (Z.esli_fark > 0) & (Z.esli_alt95 > 0) & (Z.esli_sira > 0.5)
    hat = {ad: int(Z[(Z.etki == ad)].ham_tutar.sum()) for ad in Z.etki.unique()}
    karar = "HAT BİLİNEN ETKİLERİ GÖRÜYOR" if hat.get("E1_momentum_12_1", 0) >= 2 and hat.get("E3_kucukluk", 0) >= 2 else "HAT KUSURLU OLABİLİR"
    Z.to_csv(os.path.join(A.cikti, "k42_ozet.csv"), index=False)
    return {"ozet": Z, "ham_tutan_hucre": hat, "karar": karar}

# KÖR SET DEĞERLENDİRME (Cemal 26 Eki: 'önceki tepeler aşılmıyorsa çok risk var; çoğu kutu içindeki tepe aşılıp alış emri gelmiş gibi
# işaret koydum'). ÖNCEDEN YAZILDI (✓/✗ görülmeden): ✓ = 'benzer + kutu içindeki tepe aşılırsa alırım'. Emir: bölge sonundan sonraki 60 iş
# gününde bölgenin en yüksek High'ı x 1,002'de bekleyen alış (yan ölçü: gövde tepesi max(O,C) x 1,002); dolum max(Open, seviye); dolmazsa
# işlem yok. Sonuç dolum gününden SONRA: 60 barda önce +%15 (High) / önce -%15 (Low) / yatay; 250 barda dolumun 2 katı; fiyat 31.08.2026'da
# kesik (fon krizi dışarıda). Kıyas: ✓ vs ✗ vs süzgeçli havuzdan 2.000 rastgele pencere (aynı emir). Karar: ✓ yukarı oranı hem ✗'nin hem
# havuzun >= 1,3 katı -> 'göz izi adayı' (sonra ✓/✗'yi ayıran ölçüler, ABD ve görülmemiş dönem).
FI_K23_DEG = {"emir_gun": 60, "pay": 1.002, "ufuk": 60, "esik": 0.15, "uzun": 250, "kriz": "2026-08-31", "havuz_n": 2000, "kat_esik": 1.3}


def fi_k23_emir_sonuc(d: pd.DataFrame, t: pd.Timestamp, L: int, E: Dict[str, Any] = FI_K23_DEG) -> Dict[str, Any]:
    """Bir bölge (bitiş t, uzunluk L) için iki emir seviyesi (en yüksek High / gövde tepesi): dolum günü, dolum, 60 gün yön, 250 gün 2 kat."""
    i = int(d.index.get_loc(pd.Timestamp(t))); o = d.Open.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float)
    c = d.Close.to_numpy(float); son = int(d.index.searchsorted(pd.Timestamp(E["kriz"]), side="right"))
    out: Dict[str, Any] = {}
    for ad, sev in (("tepe", h[i - L + 1:i + 1].max() * E["pay"]), ("govde", np.maximum(o, c)[i - L + 1:i + 1].max() * E["pay"])):
        j = next((k for k in range(i + 1, min(i + 1 + E["emir_gun"], son)) if h[k] >= sev), None)
        out[f"{ad}_doldu"] = j is not None
        if j is None:
            out.update({f"{ad}_y60": np.nan, f"{ad}_x2": np.nan}); continue
        g = max(o[j], sev); u = min(j + 1 + E["ufuk"], son)
        a = np.flatnonzero(h[j + 1:u] >= g * (1 + E["esik"])); b = np.flatnonzero(l[j + 1:u] <= g * (1 - E["esik"]))
        a0, b0 = (a[0] if len(a) else 10 ** 9), (b[0] if len(b) else 10 ** 9)
        out[f"{ad}_y60"] = (1.0 if a0 < b0 else (-1.0 if b0 < 10 ** 9 else 0.0)) if u - (j + 1) >= 20 else np.nan
        w = h[j + 1:min(j + 1 + E["uzun"], son)]
        out[f"{ad}_x2"] = float(len(w) > 0 and w.max() >= 2 * g) if len(w) >= 60 else np.nan
    return out


def fi_k23_havuz_ornek(V: Dict[str, pd.DataFrame], H: Dict[str, pd.Series], E: Dict[str, Any] = FI_K23_DEG, tohum: int = 23,
                       haric: Tuple[Tuple[str, str], ...] = ()) -> pd.DataFrame:
    """Her örnek bölge için süzgeçli havuzdan (fi_k23_en_benzer ile aynı süzgeç) rastgele E['havuz_n'] pencere + emir sonucu."""
    sat = []
    for b, h0 in H.items():
        _, P = fi_k23_en_benzer(V, h0, 1, haric)
        P = P.sample(min(E["havuz_n"], len(P)), random_state=tohum)
        for r in P.itertuples():
            try:
                sat.append({"bolge": b, "sembol": r.sembol, "tarih": r.tarih, **fi_k23_emir_sonuc(V[r.sembol], r.tarih, int(h0["L"]), E)})
            except Exception as ex:   # tek pencere bozuksa digerleri devam eder
                filog.warning("K23 havuz %s %s atlandi: %s", r.sembol, r.tarih, ex)
    return pd.DataFrame(sat)


def fi_k23_kor_degerlendir(V: Dict[str, pd.DataFrame], anahtar: pd.DataFrame, isaret: List[int], havuz: pd.DataFrame,
                           E: Dict[str, Any] = FI_K23_DEG) -> Dict[str, Any]:
    """Cemal'in ✓ numaraları (isaret) ile anahtar: her aday için emir sonucu; ✓ / ✗ / havuz özetleri ve karar."""
    Lb = {"1": 21, "2": 12, "3": 17}
    A = anahtar.assign(bolge=anahtar.bolge.astype(str), tarih=pd.to_datetime(anahtar.tarih))
    A = A.assign(isaret=A.no.isin(isaret)).reset_index(drop=True)
    R = pd.DataFrame([fi_k23_emir_sonuc(V[r.sembol], r.tarih, Lb[r.bolge], E) for r in A.itertuples()])
    A = pd.concat([A, R], axis=1)
    def oz(X, k):
        d = X[X[f"{k}_doldu"]]; y = d[f"{k}_y60"].dropna(); x2 = d[f"{k}_x2"].dropna()
        return {"n": len(X), "doldu": float(X[f"{k}_doldu"].mean()) if len(X) else np.nan, "n_islem": len(y),
                "yukari": float((y == 1).mean()) if len(y) else np.nan, "asagi": float((y == -1).mean()) if len(y) else np.nan,
                "x2": float(x2.mean()) if len(x2) else np.nan}
    Z = []
    for k in ("tepe", "govde"):
        for ad, X in (("✓", A[A.isaret]), ("✗", A[~A.isaret]), ("havuz", havuz)):
            Z.append({"emir": k, "grup": ad, **oz(X, k)})
    Z = pd.DataFrame(Z); t = Z[Z.emir == "tepe"].set_index("grup")
    karar = bool(t.loc["✓", "yukari"] >= E["kat_esik"] * t.loc["✗", "yukari"] and t.loc["✓", "yukari"] >= E["kat_esik"] * t.loc["havuz", "yukari"])
    return {"aday": A, "ozet": Z, "karar": karar}


def fi_k12_ders10b(D: pd.DataFrame, T: pd.DataFrame, P: pd.DataFrame, yol: str) -> int:
    """Ders 10b (Cemal 26 Eki, kör set işaretleri): ✓ / ✗ / kodun en benzer 48'i / havuz; kutu tepesi aşılırsa alış emri, 60 gün ±%15,
    250 gün 2 kat. D = Cemal'in etiketli adayları (k23_kor_cemal_etiket.csv), T = 48 adayın emir sonucu, P = havuz (k23_kor_havuz.csv)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    yz = lambda x: f"%{100 * x:.0f}" if x == x else "—"

    def oz(X):
        d = X[X.tepe_doldu.astype(bool)]; y = d.tepe_y60.dropna()
        return len(X), len(d), (y == 1).mean() if len(y) else np.nan, (y == -1).mean() if len(y) else np.nan, d.tepe_x2.dropna().mean()
    G = [("✓ senin benzer dediklerin", D[D.isaret == "✓"]), ("✗ benzemez dediklerin", D[D.isaret == "✗"]),
         ("kodun en benzer 48'i (hepsi)", T), ("süzgeçli havuz (6.000)", P)]
    S = [(ad, *oz(X)) for ad, X in G]
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69)); y = 0.96
        fig.text(0.07, y, "DERS 10b: KÖR SET — GÖZÜN AYIRDI MI?", fontsize=14, weight="bold", va="top", color="#1f2a44"); y -= 0.045
        sat = ["Senin kuralın: ✓ = 'benzer ve kutu içindeki tepe aşılırsa alırım'. Her adayda bölge bittikten sonra 60 gün boyunca kutu "
               "tepesinin %0,2 üstünde bekleyen alış emri; tepe aşılmazsa işlem yok. Sonuç dolumdan: 60 günde önce +%15 / önce −%15, 250 günde "
               "2 kat; fon krizi dışarıda. Kural ve karar işaretlerin görülmeden yazıldı. 48 adayın 20'sini işaretledin (7 ✓, 13 ✗)."]
        sat += [f"- {ad}: aday {n}, emir doldu {k}, dolanlarda önce +%15 {yz(u)}, önce −%15 {yz(a)}, 2 kat {yz(x)}" for ad, n, k, u, a, x in S]
        sat += ["", "SONUÇ: ✓'lerin yukarı oranı ✗'lerden yüksek değil (karar şartı: ✗ ve havuzun 1,3 katı) → göz izi adayı DEĞİL. Dolan emir "
                "sayısı çok az (✓ 4, ✗ 9): bu bir ön deneme, kesin hüküm değil.",
                "Yan gözlem: kodun en benzer 48'inde tepe aşılınca dolanların yukarı oranı havuzdan biraz yüksek (1,16 kat), 1,3 değil; dolanların "
                "üçte biri 2023 boğasından.",
                "Sıradaki (önceden yazılı): kalan 28 grafiği işaretlersen aynı kuralla tamamlanır; tutarsa ✓/✗'yi ayıran ölçüler ABD'de ve "
                "görülmemiş dönemde denenir."]
        for s in sat:
            for k, p in enumerate(textwrap.wrap(s, 92) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, p, fontsize=9.4, va="top"); y -= 0.021
            y -= 0.004
        ax = fig.add_axes([0.12, 0.08, 0.80, y - 0.13])
        x = np.arange(len(S))
        ax.bar(x - 0.2, [100 * s[3] for s in S], 0.4, color="#27ae60", label="önce +%15 (dolanlarda)")
        ax.bar(x + 0.2, [100 * s[5] for s in S], 0.4, color="#1f2a44", label="250 günde 2 kat")
        ax.set_xticks(x); ax.set_xticklabels([f"{s[0]}\n(dolan {s[2]})" for s in S], fontsize=7.5); ax.set_ylabel("%", fontsize=8)
        ax.legend(fontsize=8); ax.set_ylim(0, 100)
        pdf.savefig(fig); plt.close(fig)
    return 1

def fi_k12_ders10c(E: pd.DataFrame, H: pd.DataFrame, yol: str) -> int:
    """Ders 10c (Cemal 26 Eki, kör set v4 işaretleri): ✓ / net ✗ / belirsiz / havuz için alış mumundan sonraki gün açılışta giriş, 60 gün
    ±%15, 250 gün 2 kat; gözün ✓'de neyi seçtiği (alış mumu gecikmesi, boyu, hacmi, kutu bandı, kutudaki yer). E = k23_kor4_cemal_etiket.csv,
    H = k23_kor4_havuz.csv."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    yz = lambda x: f"%{100 * x:.0f}" if x == x else "—"
    sz = lambda x, k=1: f"{x:.{k}f}".replace(".", ",") if x == x else "—"

    def oz(X):
        y = X.y60.dropna(); yk = X.y60_kap.dropna()
        return (len(X), (y == 1).mean() if len(y) else np.nan, (y == -1).mean() if len(y) else np.nan,
                X.x2.dropna().mean() if X.x2.notna().any() else np.nan, (yk == 1).mean() if len(yk) else np.nan)
    G = [("✓ alırdım", E[E.isaret == "✓"]), ("✗ almazdım", E[E.isaret == "✗"]), ("? belirsiz", E[E.isaret == "?"]),
         ("havuz", H)]
    S = [(ad, *oz(X)) for ad, X in G]

    def yaz(fig, y, satirlar, boy=9.4):
        for s in satirlar:
            for k, p in enumerate(textwrap.wrap(s, 92) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, p, fontsize=boy, va="top"); y -= boy * 0.0022
            y -= 0.004
        return y

    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.text(0.07, 0.96, "DERS 10c — KÖR SET v4: KUTU + ALIŞ MUMU", fontsize=15, weight="bold", va="top", color="#1f2a44")
        n_ok, n_x, n_b = (int((E.isaret == g).sum()) for g in ("✓", "✗", "?"))
        y = yaz(fig, 0.915, [
            f"Ne yapıldı: 48 aday (kutu + kutu tepesinin üstünde kapanan ilk yeşil mum, 1 yıl geri zum, sonrası gizli). Sen {n_ok} ✓, "
            f"{n_x} ✗ koydun; {n_b} sayfa belirsiz ('zor', '?', 'kararsız alış mumu', 'oransız büyük', bir boş).",
            "Ölçü (işaretlerden önce yazılı): alış mumundan sonraki gün açılışta al; 60 günde önce +%15 mi −%15 mi; 250 günde 2 kat. "
            "Havuz = aynı süzgeçten geçen ve alış mumu gelmiş 6.000 rastgele bölge.",
            f"- ✓: önce +%15 {yz(S[0][2])}, önce −%15 {yz(S[0][3])}, 2 kat {yz(S[0][4])}",
            f"- ✗: {yz(S[1][2])}, {yz(S[1][3])}, {yz(S[1][4])} · belirsiz (n {S[2][1]}): {yz(S[2][2])}, {yz(S[2][3])}, {yz(S[2][4])}",
            f"- havuz: {yz(S[3][2])}, {yz(S[3][3])}, {yz(S[3][4])}",
            f"- yan ölçü (alış mumunun kapanışında al): ✓ {yz(S[0][5])}, ✗ {yz(S[1][5])}, havuz {yz(S[3][5])}",
            "KARAR: ✓'nin yukarı oranı ne ✗'nin ne havuzun 1,3 katı → göz izi değil. 2 kat oranında ✓ en geride. n küçük (28 / 14).",
            "Ne öğrendik: kutu + alış mumu kuralının kendisi havuzda zaten %60 'önce +%15' veriyor (alış mumu gelmeyenleri dışarıda "
            "bıraktığımız için). Gözün bunun üstüne bir şey eklemedi; aynı kutu + alış mumu görüntüsünde sonrasını ayıramıyor."])
        ax = fig.add_axes([0.12, 0.08, 0.80, y - 0.13]); x = np.arange(len(S))
        for k, (i, renk, et) in enumerate(((2, "#27ae60", "önce +%15"), (3, "#c0392b", "önce −%15"), (4, "#1f2a44", "250 günde 2 kat"))):
            ax.bar(x + (k - 1) * 0.27, [100 * s[i] for s in S], 0.27, color=renk, label=et)
        ax.set_xticks(x); ax.set_xticklabels([f"{s[0]}\n(n {s[1]})" for s in S], fontsize=8); ax.set_ylabel("%", fontsize=8)
        ax.set_ylim(0, 100); ax.legend(fontsize=8)
        pdf.savefig(fig); plt.close(fig)

        fig = plt.figure(figsize=(8.27, 11.69))
        fig.text(0.07, 0.96, "GÖZÜN ✓'DE NEYİ SEÇTİ (medyan)", fontsize=15, weight="bold", va="top", color="#1f2a44")
        M = E.groupby("isaret")[["gecikme", "alis_boy", "alis_hacim", "bant", "dusus", "konum"]].median()
        ad = [("gecikme", "alış mumu kutudan kaç mum sonra", lambda v: sz(v, 0)), ("alis_boy", "alış mumu boyu / kutu mumu", sz),
              ("alis_hacim", "alış mumu hacmi / kutu hacmi", sz), ("bant", "kutu bandı (tepe/dip − 1)", yz),
              ("dusus", "kutudan önceki düşüş", yz), ("konum", "kutunun 1 yıllık aralıktaki yeri (0 dip, 1 tepe)", lambda v: sz(v, 2))]
        y = 0.90; fig.text(0.07, y, "ölçü", fontsize=10, weight="bold"); fig.text(0.62, y, "✓", fontsize=10, weight="bold")
        fig.text(0.74, y, "✗", fontsize=10, weight="bold"); fig.text(0.86, y, "?", fontsize=10, weight="bold"); y -= 0.03
        for k, et, f in ad:
            fig.text(0.07, y, et, fontsize=9.5)
            for xx, g in ((0.62, "✓"), (0.74, "✗"), (0.86, "?")):
                fig.text(xx, y, f(M.loc[g, k]) if g in M.index else "—", fontsize=9.5)
            y -= 0.026
        yaz(fig, y - 0.02, [
            "Okuma: ✓ dediklerinde alış mumu kutudan daha geç geldi (kutu olgunlaştıktan sonra), mum ve hacmi daha büyük, kutu daha dar ve "
            "1 yıllık aralığın daha alt kısmında. Yani gözün belirli bir tip seçiyor; ama bu tipin sonrası seçmediklerinden iyi değil.",
            "Neden iz değil: aynı görüntü (dar kutu + güçlü yeşil kırılım mumu) yükselen ve çöken hisselerde aynı sıklıkta. Fark kutunun "
            "içinde değil, alış mumundan sonra; o da önceden görünmüyor (DERS 10, 13 ile aynı).",
            "Kendin nasıl bakarsın: 'kutu tepesinin üstünde yeşil kapanış' tek başına havuzun ortalaması; ✓ demen oranı değiştirmiyor. "
            "Bu yüzden alış mumundan sonra korumayı (kutu dibi zarar sınırı) sen koy; kazanç kırılımdan sonra piyasanın verdiği kadar.",
            "Dikkat: alış mumu hacmi ve giriş onayı 'kapalı konu' (COL_OZET). Bu ölçüleri kural olarak denemek senin kararın."])
        pdf.savefig(fig); plt.close(fig)
    return 2

def fi_k12_ders12(V: Dict[str, pd.DataFrame], T: pd.DataFrame, Z: pd.DataFrame, Zd: pd.DataFrame, yol: str) -> int:
    """Ders 12 (Cemal 26 Eki, KZBGY 4 Şub-13 Mar 2025 + önceki parmak izleriyle karşılaştırma): (1) KZBGY kutu + alış mumu, dört örneğin
    16 ölçüsünün havuz yüzdeliği ve ortak ölçüler; (2) ortak profil + üç devam denemesi, hücre katları, ders. V = BIST; T = k26_ornek.csv,
    Z = k26_ozet.csv, Zd = k26_deneme.csv."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    T = T.set_index(T.columns[0]) if T.columns[0].startswith("Unnamed") else T
    Y = T[[c for c in T.columns if c.startswith("yuzdelik_")]].rename(columns=lambda c: c[9:])
    ad = {"egim": "eğim", "mum": "mum boyu", "yesil": "yeşil oranı", "alt_fitil": "alt fitil", "ust_fitil": "üst fitil",
          "yakinlik": "kapanış yakınlığı", "bozan": "düzeni bozan", "hacim": "hacim", "rsi": "RSI", "macd": "MACD", "dusus": "önceki düşüş",
          "konum": "kutudaki yer", "seri": "SMA20 üstü dizilme", "once_alt": "1. evre SMA altı", "delen": "2. evre delen", "bbw": "BB sıkışma"}
    ortak = [k for k in Y.columns if Y[k].max() - Y[k].min() <= FI_K26["ortak_aralik"]]
    sz = lambda x: f"{x:.2f}".replace(".", ",") if x == x else "—"

    def yaz(fig, y, satirlar, boy=9.4):
        for s in satirlar:
            for k, p in enumerate(textwrap.wrap(s, 92) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, p, fontsize=boy, va="top"); y -= boy * 0.0022
            y -= 0.004
        return y

    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.text(0.07, 0.965, "DERS 12 — DÖRT ÇÖLÜN ORTAK PARMAK İZİ", fontsize=15, weight="bold", va="top", color="#1f2a44")
        fig.text(0.07, 0.935, "KZBGY 4 Şub - 11 Mar 2025 kutusu, 13 Mar alış mumu (12 Mar +%10 ilk ayak, kutu tepesinin altında kapandı)",
                 fontsize=9.5, va="top")
        d = V["KZBGY"]; i = int(d.index.searchsorted(pd.Timestamp("2025-03-11"), side="right")) - 1
        b0 = int(d.index.searchsorted(pd.Timestamp("2025-02-04"))); R = fi_k23_alis_mumu(d, d.index[i], i - b0 + 1)
        ax = fig.add_axes([0.07, 0.66, 0.88, 0.25]); axh = fig.add_axes([0.07, 0.60, 0.88, 0.05])
        fi_k23_kor4_ciz(ax, axh, d, b0 - 40, int(R["alis_i"]), b0, i, R["kutu_ust"], R["kutu_alt"], False)
        axm = fig.add_axes([0.25, 0.10, 0.70, 0.44])
        im = axm.imshow(Y.T.to_numpy(float), aspect="auto", cmap="RdYlGn", vmin=0, vmax=1)
        axm.set_xticks(range(len(Y.index))); axm.set_xticklabels(Y.index, fontsize=8)
        axm.set_yticks(range(len(Y.columns))); axm.set_yticklabels([ad[k] + (" ★" if k in ortak else "") for k in Y.columns], fontsize=8)
        for a in range(len(Y.columns)):
            for b in range(len(Y.index)):
                axm.text(b, a, sz(Y.iloc[b, a]), ha="center", va="center", fontsize=7)
        axm.set_title("Havuz yüzdeliği (0 en düşük, 1 en yüksek; ★ = dördünde ortak)", fontsize=9, loc="left")
        pdf.savefig(fig); plt.close(fig)

        fig = plt.figure(figsize=(8.27, 11.69))
        fig.text(0.07, 0.965, "ORTAK PROFİL SONRASINI AYIRIYOR MU?", fontsize=15, weight="bold", va="top", color="#1f2a44")
        def kat(X, pz, dn):
            r = X[(X.pazar == pz) & (X.donem == dn)]
            return (float(r.kat_yukari.iloc[0]), int(r.n.iloc[0])) if len(r) else (np.nan, 0)
        hucre = [("BIST", "2023"), ("BIST", "2024-26"), ("ABD", "2023"), ("ABD", "2024-26")]
        satir = [("ortak profil (4 ölçü)", Z)] + [(f"{k} {e}", Zd[Zd.deneme == k]) for k, e in
                                                 (("D1", "sıkı"), ("D2", "BINBN'siz"), ("D3", "merkeze en yakın %1"))]
        y = yaz(fig, 0.925, [
            f"Ortak ölçüler (dört örneğin yüzdelik aralığı ≤ 0,40): {', '.join(ad[k] for k in ortak)}. Yani dördünde de mumlar küçük, "
            "üst fitiller uzun (kutu tepesine satış), RSI düşük. Bu profil BIST + ABD'de 20 mumluk pencerelerde arandı; sinyalden sonra "
            "v4 alış mumu (kutu tepesinin üstünde kapanan ilk yeşil mum), ertesi açılış, 60 günde önce +%15 / −%15. Taban: aynı süzgeç + "
            "aynı alış mumu kuralıyla rastgele pencereler. Eşikler sonuçtan önce yazıldı.",
            "Önce +%15 katı (sinyal / taban), parantezde n:"])
        fig.text(0.07, y, "deneme", fontsize=9, weight="bold")
        for j, (pz, dn) in enumerate(hucre):
            fig.text(0.40 + j * 0.14, y, f"{pz} {dn}", fontsize=9, weight="bold")
        y -= 0.025
        for et, X in satir:
            fig.text(0.07, y, et, fontsize=9)
            for j, (pz, dn) in enumerate(hucre):
                k_, n_ = kat(X, pz, dn); fig.text(0.40 + j * 0.14, y, f"{sz(k_)} ({n_})", fontsize=9,
                                                  color="#27ae60" if k_ >= FI_K26["kat_esik"] and n_ >= FI_K26["n_esik"] else "#333")
            y -= 0.022
        yaz(fig, y - 0.02, [
            "KARAR: hiçbir deneme dört hücrede 1,3'e ulaşmadı → İZ DEĞİL. Ortak profil 1,01-1,02 (taban ile aynı), D1 0,97-1,06, D3 0,92-1,07. En yakın: D2 BIST "
            "2024-26 1,26 ama n 15 (küçük örnek, diğer hücreler 0,77).",
            "Ne öğrendik: dört çölün gerçek bir ortak yüzü var (küçük mum, uzun üst fitil, düşük RSI), ölçüler bunu yakalıyor. Ama aynı "
            "yüz süzgeçten geçen binlerce bölgede var ve alış mumundan sonraki yol sıradan bölgelerle aynı. Koşan dört örnek ortak yüzü "
            "değil, sonrasını paylaşıyor; o da önceden görünmüyor (DERS 10, 13, 14).",
            "Not: tarama 20 mumluk pencerelerle yapıldı; senin bölgelerin 12-26 mum. KZBGY 2025 ve MANAS 2025 bölgeleri 20 mumluk pencerede "
            "profile girmedi (kendi uzunluklarında girer).",
            "Kendin nasıl bakarsın: uzun üst fitilli küçük mumlu dip kutusu 'satıcı kutunun tepesinde bekliyor' der; tepe kapanışla "
            "geçilirse (alış mumu) satıcı bitmiş olabilir. Ama bu, rastgele bir kutunun kırılımından daha iyi sonuç vermiyor: alış "
            "mumundan sonra kutu dibi zarar sınırın olsun."])
        pdf.savefig(fig); plt.close(fig)
    return 2


def fi_k12_ders10(V: Dict[str, pd.DataFrame], Zk: pd.DataFrame, Hk: pd.DataFrame, Es: pd.DataFrame, Z24: pd.DataFrame, yol: str) -> int:
    """Ders 10 (Cemal 25 Eki: 'işaretli bölgenin her özelliğini kaydet; birebir aynı görünümdeki bölgelerin yüzde kaçı yukarı, aşağı, yatay?
    halüsinasyon mu?'): (1) soru, iki bölgenin parmak izi; (2) MANAS bölgeleri grafikte (SMA20, BB, iki evre); (3) en yakın 100 benzer bölge
    yukarı / aşağı / yatay vs bütün bölgeler; (4) iki evre kuralı vs eşli; (5) BIST 2024-26 en yakın 8 benzer bölge ve sonrası; (6) sonuç.
    V = BIST; Zk = k23_ozet.csv, Hk = k23_parmak.csv, Es = k23_esler.csv, Z24 = k24_ozet.csv."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    A4 = (8.27, 11.69)
    yz = lambda x: f"%{100 * x:.0f}" if x == x else "—"
    sz = lambda x, k=2: f"{x:.{k}f}".replace(".", ",") if x == x else "—"

    def yazi(fig, y, baslik, satirlar, boy=9.4, gen=92):
        if baslik:
            fig.text(0.07, y, baslik, fontsize=14, weight="bold", va="top", color="#1f2a44"); y -= 0.040
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= boy * 0.0022
            y -= 0.004
        return y

    def mumlar(ax, w, renk_sma=True):
        x = np.arange(len(w)); r = np.where(w.Close >= w.Open, "#27ae60", "#c0392b")
        ax.vlines(x, w.Low, w.High, color=r, lw=0.7)
        ax.bar(x, (w.Close - w.Open).abs().clip(lower=1e-9), bottom=np.minimum(w.Open, w.Close), color=r, width=0.7)
        if renk_sma:
            ax.plot(x, w.sma, color="#e67e22", lw=1.3); ax.plot(x, w.ust, color="#3498db", lw=0.8); ax.plot(x, w.alt, color="#3498db", lw=0.8)
        return x

    def hazir(d):
        d = d.copy(); m = d.Close.rolling(20).mean(); sd = d.Close.rolling(20).std()
        return d.assign(sma=m, ust=m + 2 * sd, alt=m - 2 * sd)

    E = FI_K23; HUC = [("BIST", "2023"), ("BIST", "2024-26"), ("ABD", "2023"), ("ABD", "2024-26")]
    Zk = Zk.assign(bolge=Zk.bolge.astype(str)); Hk = Hk.set_index("Unnamed: 0") if "Unnamed: 0" in Hk.columns else Hk
    Hk.index = Hk.index.astype(str); Zi = Zk.set_index(["bolge", "pazar", "donem"])
    BB = [b for b in ("1", "2", "3") if b in Hk.index]
    g = lambda b, p, d_, k: Zi.loc[(b, p, d_), k] if (b, p, d_) in Zi.index else np.nan
    Zj = Z24.set_index(["pazar", "donem"]); g24 = lambda p, d_, k: Zj.loc[(p, d_), k] if (p, d_) in Zj.index else np.nan
    ETK = {"egim": "eğim (bar başı)", "mum": "mum boyu / düşüştekiler", "yesil": "yeşil mum oranı", "alt_fitil": "alt fitil oranı",
           "ust_fitil": "üst fitil oranı", "yakinlik": "yakınlık (std/ort)", "bozan": "düzeni bozan mum oranı", "hacim": "hacim / önceki 60 gün",
           "rsi": "RSI14 (bitiş)", "macd": "MACD hist / fiyat", "dusus": "öncesindeki düşüş", "konum": "bitişin bölgedeki yeri",
           "seri": "2. evre payı (SMA20 üstü seri)", "once_alt": "1. evrede SMA20 altı", "delen": "2. evrede SMA'yı delen", "bbw": "BB genişliği / bölge en yükseği"}
    BL = {"1": "1. bölge MANAS 13 Haz – 11 Tem 2025", "2": "2. bölge MANAS 20 Eki – 5 Kas 2025", "3": "3. bölge BINBN 27 Ara 2024 – 21 Oca 2025",
          "S": "silkeleme 17 Kas – 4 Ara 2025 (benim okumam)"}
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        y = yazi(fig, 0.96, "DERS 10: İŞARETLİ BÖLGENİN PARMAK İZİ — BENZERLERİ NE YAPTI?", [
            "Sen: 'Şu işaretli bölgenin her özelliğini kaydet: eğim, küçük mum, kırmızı-yeşil oranı, alt fitil, üst fitil, birbirine yakınlık, "
            "düzeni bozan mum sayısı, hacim, RSI, MACD… Birebir aynı görünümdeki bölgelerin yüzde kaçı yukarı, yüzde kaçı aşağı, yüzde kaçı "
            "yatay? Bu bir halüsinasyon mu?' Ve: '1. evre kırmızı SMA altında, 2. evre kırmızı SMA üstünde dizilme, muntazam, delen yok neredeyse.'",
            "Nasıl ölçüldü (sonuç görülmeden yazıldı): üç bölgenin 16 ölçüsü aşağıda. Borsadaki BÜTÜN hisselerin BÜTÜN günlerinde aynı "
            "uzunluktaki bölgeler aynı 16 ölçüyle ölçüldü; senin bölgene en yakın 100 bölge alındı (aynı hissede üst üste binen tek sayıldı, "
            "MANAS'ın kendisi hariç). Sonra her birinin bitişinden sonraki 60 günde: önce +%15 gördüyse YUKARI, önce −%15 gördüyse AŞAĞI, "
            "ikisi de yoksa YATAY. Kıyas: aynı pazar ve dönemdeki bütün bölgeler. Geçme şartı: yukarı oranı 1,3 kat, dört hücrede."])
        ax = fig.add_axes([0.07, 0.10, 0.86, y - 0.13]); ax.axis("off")
        sat = [[ETK[o]] + [sz(float(Hk.loc[b, o]), 3) for b in BB] for o in E["olcu"] if o in Hk.columns]
        tb = ax.table(cellText=sat, colLabels=["ölçü"] + [f"{b}. bölge ({int(float(Hk.loc[b, 'L']))} gün)" for b in BB], loc="upper center",
                      cellLoc="center", colWidths=[0.40] + [0.60 / len(BB)] * len(BB))
        tb.auto_set_font_size(False); tb.set_fontsize(8.5); tb.scale(1, 1.35)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "SENİN BÖLGELERİN GRAFİKTE (turuncu SMA20, mavi Bollinger 20,2)", [
            "Gri gölge: işaretlediğin çöl. Önce düşüş (yapı dipte), sonra küçük mumlu yatay bölge; MANAS'ta mumlar SMA20 altından üstüne "
            "diziliyor, BINBN'de SMA20 fiyatın üstüne iniyor ve bant aşırı daralıyor (0,61 -> 0,027). Sağdaki kısım sağ ayak: kod bunu bilmez."])
        for k, b in enumerate(BB):
            s_, b0, e0 = E["bolge"][b]; d0 = hazir(V[s_])
            w = d0.loc[pd.Timestamp(b0) - pd.Timedelta(days=60):pd.Timestamp(e0) + pd.Timedelta(days=45)]
            ax = fig.add_axes([0.08, 0.60 - k * 0.285, 0.88, 0.21]); x = mumlar(ax, w)
            ib = np.flatnonzero((w.index >= b0) & (w.index <= e0)); ax.axvspan(ib[0] - 0.5, ib[-1] + 0.5, color="#999", alpha=0.18)
            ax.set_xticks(x[::10]); ax.set_xticklabels([f"{t:%d.%m}" for t in w.index[::10]], fontsize=7); ax.set_title(BL[b], fontsize=9)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        yazi(fig, 0.96, "EN YAKIN 100 BENZER BÖLGE: YUKARI / AŞAĞI / YATAY (60 gün, ±%15)", [
            "Her hücrede sol çubuk: senin bölgene en yakın 100 bölge; sağ çubuk: aynı pazar ve dönemdeki bütün bölgeler. Yeşil yukarı, kırmızı "
            "aşağı, gri yatay. Benzerlerin yukarı oranı tabandan belirgin ve her dönemde yüksek olsaydı şekil bir şey söylüyor olurdu."])
        for k, b in enumerate(BB):
            ax = fig.add_axes([0.10, 0.62 - k * 0.285, 0.85, 0.20]); et = []
            for j, (p, d_) in enumerate([("BIST", "2016-22")] + HUC[:2] + [("ABD", "2016-22")] + HUC[2:]):
                for q, (on, ad) in enumerate((("yon60_", "benzer"), ("yon60_taban_", "hepsi"))):
                    xx = j * 2.6 + q; u, a_, y_ = g(b, p, d_, on + "yukari"), g(b, p, d_, on + "asagi"), g(b, p, d_, on + "yatay")
                    ax.bar(xx, 100 * u, color="#27ae60", width=0.9); ax.bar(xx, 100 * y_, bottom=100 * u, color="#bbb", width=0.9)
                    ax.bar(xx, 100 * a_, bottom=100 * (u + y_), color="#c0392b", width=0.9)
                    ax.text(xx, 100 * u / 2, yz(u), ha="center", va="center", fontsize=6.5, color="white")
                et.append((j * 2.6 + 0.5, f"{p} {d_}\nkat {sz(g(b, p, d_, 'kat60'))}"))
            ax.set_xticks([a for a, _ in et]); ax.set_xticklabels([b_ for _, b_ in et], fontsize=7); ax.set_ylim(0, 100)
            ax.set_ylabel("%", fontsize=8); ax.set_title(BL[b] + " — her hücrede sol: en yakın 100, sağ: hepsi", fontsize=9)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        y = yazi(fig, 0.96, "İKİ EVRE KURALI (SMA20 altı → SMA20 üstünde dizilme) vs EŞLİ", [
            "Senin tarifin doğrudan kural olarak (eşikler MANAS'taki iki bölgenden, sonuç görülmeden; BINBN'i de 27 Ocak 2025'te yakalıyor): önce en az −%30 düşüş; dizilmeden önceki "
            "10 günün en az %80'i SMA20 altında; SMA20 üstünde 5. gün; bu 5 mumun en fazla 2'si SMA'yı deler; bant genişliği son 15 günün "
            "en yükseğinin en fazla %70'i. Eşli: aynı düşüş ve aynı 5. gün, ama 1. evre / delen / sıkışma şartı tutmayan günler."]
            + [f"- {p} {d_}: kural n {int(g24(p, d_, 'n'))}, yukarı {yz(g24(p, d_, 'yon60_yukari'))} / aşağı {yz(g24(p, d_, 'yon60_asagi'))} / "
               f"yatay {yz(g24(p, d_, 'yon60_yatay'))}; eşli yukarı {yz(g24(p, d_, 'yon60_esli_yukari'))} / aşağı {yz(g24(p, d_, 'yon60_esli_asagi'))} "
               f"(kat {sz(g24(p, d_, 'kat60'))})" for p, d_ in [("BIST", "2016-22")] + HUC[:2] + [("ABD", "2016-22")] + HUC[2:] if (p, d_) in Zj.index]
            + [f"- Geçme şartı (dört hücrede kat ≥ 1,3): {'GEÇTİ' if ((Zj.loc[[h for h in HUC if h in Zj.index], 'kat60'] >= 1.3).all() and len([h for h in HUC if h in Zj.index]) == 4) else 'GEÇMEDİ'}. "
               "Senin tarifine uyan günler, aynı düşüşten sonra SMA üstüne çıkan ama tarife uymayan günlerden daha sık yukarı gitmiyor."])
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        X = Es[(Es.bolge == "2") & (Es.pazar == "BIST") & (Es.donem == "2024-26")].sort_values("uzak").head(8)
        yazi(fig, 0.96, "2. BÖLGEYE EN BENZER 8 BÖLGE (BIST 2024-26) VE SONRASI", [
            "Gri gölge benzer bölge, sağı sonraki 60 gün. Başlıkta sonuç. Hepsi senin 2. bölgene ölçülerde çok yakın; kimi koştu, kimi düştü, "
            "kimi yatay kaldı. Şekil bunu önceden ayırmıyor."])
        for k, r in enumerate(X.itertuples()):
            d = hazir(V[r.sembol]); t = d.index.get_loc(pd.Timestamp(r.tarih)); w = d.iloc[max(0, t - 30):t + 61]
            ax = fig.add_axes([0.07 + (k % 2) * 0.47, 0.70 - (k // 2) * 0.21, 0.42, 0.16]); x = mumlar(ax, w)
            i0 = t - max(0, t - 30); ax.axvspan(i0 - 11.5, i0 + 0.5, color="#999", alpha=0.18); ax.set_xticks([])
            ax.tick_params(labelsize=6)
            ax.set_title(f"{r.sembol} {pd.Timestamp(r.tarih):%d.%m.%Y}: {({1.0: 'YUKARI', -1.0: 'AŞAĞI', 0.0: 'YATAY'}).get(r.yon60, '—')}", fontsize=8)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        b1 = Zk[(Zk.bolge.astype(str).isin(BB)) & (Zk.donem != "2016-22")]
        yazi(fig, 0.96, "SONUÇ: HALÜSİNASYON MU?", [
            "- Hayır, gördüğün şekil gerçek: üç bölge ölçülerde de birbirine benziyor (küçük mum, düşüşten sonra, SMA altı → SMA üstü dizilme, "
            "bant sıkışması) ve kod bu şekli binlerce kez buluyor.",
            f"- Ama aynı şeklin sonrası yazı-tura değil, 'piyasa ne yaparsa': en yakın 100 benzer bölgenin yukarı oranı karar hücrelerinde "
            f"{yz(b1.yon60_yukari.min())}-{yz(b1.yon60_yukari.max())}, aynı dönemin bütün bölgelerinde {yz(b1.yon60_taban_yukari.min())}-"
            f"{yz(b1.yon60_taban_yukari.max())}. Kat {sz(b1.kat60.min())}-{sz(b1.kat60.max())}: BIST 2024-26'da biraz önde, BIST 2023'te geride; "
            "ABD'de önde ama aşağı oranı da yüksek (benzer bölgeler daha oynak hisseler).",
            "- İki evre kuralı (senin tarifin) eşli günlerle aynı ya da kötü. Dört hücrede tutan bir üstünlük yok → standarda göre İZ DEĞİL.",
            "- Senin üç bölgen gerçekten koştu; benzerlerinin ~10'da 6'sı da +%15'i önce gördü. Ama aynı gün herhangi bir bölgenin de ~10'da 5-6'sı "
            "görüyor. Fark, kazanmayı garantileyecek ya da sistemi rastgeleden ayıracak büyüklükte değil.",
            "",
            "Sıradaki (önceden yazılı): aynı benzerlik araması oynaklığı eşitleyerek (benzer bölgelerin tabanı aynı oynaklıktaki bölgeler) ve "
            "katalizörle (sektör rüzgârı / KAP haberi aynı hafta) birlikte — CLAUDE.md: 'rüzgâr ya da katalizör olmadan çöl aranmaz'."])
        pdf.savefig(fig); plt.close(fig)
    return 6


def fi_k12_ders11(S1: pd.DataFrame, S2: pd.DataFrame, D: pd.DataFrame, yol: str, fon: Tuple[str, ...] = tuple(FON_HISSE)) -> int:
    """Ders 11 (Cemal 25 Eki: 'bir hisseyi fazla alıcı olunca o bölgede öyle bir yapı oluşur'): (1) mantık, nasıl ölçüldü, soru 1 (çöl ->
    sonra fon) ve soru 2 (fon -> önce çöl) çubukları; (2) deneme 2 (çölde fon var / yok) ve 3 (fon hisseleri hariç), fon krizi dışarıda; sonuç.
    S1 = k25_soru1.csv, S2 = k25_soru2.csv, D = k25_deneme.csv."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import textwrap
    A4 = (8.27, 11.69); yz = lambda x: (f"%{100 * x:.1f}" if x < 0.1 else f"%{100 * x:.0f}").replace(".", ",") if x == x else "—"

    def yazi(fig, y, baslik, satirlar, boy=9.4, gen=92):
        if baslik:
            fig.text(0.07, y, baslik, fontsize=14, weight="bold", va="top", color="#1f2a44"); y -= 0.040
        for s in satirlar:
            for k, parca in enumerate(textwrap.wrap(s, gen) or [""]):
                fig.text(0.07 if not s.startswith("- ") or k == 0 else 0.095, y, parca, fontsize=boy, va="top"); y -= boy * 0.0022
            y -= 0.004
        return y

    G = ["K24 kural", "K24 eşli", "K18 profil", "K18 eşli"]; R = ["#1f2a44", "#9aa5b8", "#c0392b", "#e6a39b"]
    o1 = S1.groupby("grup")[["giris5", "giris2"]].mean()
    o2 = S2.groupby("tip")[[f"var_{g}" for g in G if f"var_{g}" in S2.columns]].mean() if len(S2) else pd.DataFrame()
    n2 = int((S2.tip == "fon girişi").sum()) if len(S2) else 0
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=A4)
        y = yazi(fig, 0.96, "DERS 11: ÇÖL, BÜYÜK ALICININ İZİ Mİ?", [
            "Sen: 'Bu çöl formasyonunu fon ilişkisini bilmeden gördüm; sonra söylediklerimin çoğu fon hisselerinde çıktı. Demek ki bir hisseyi "
            "fazla alıcı olunca o bölgede öyle bir yapı oluşur.' Mantık doğru kurulmuş: o zaman çöl, büyük alıcının ayak izi olmalı. Bunu fiyattan "
            "değil SAHİPLİKTEN ölçtüm: KAP'taki fon portföy raporları (Ara 2022'den, her raporun yayın anıyla; o gün bilinen pay).",
            "Soru 1 — çölden SONRA büyük alıcı geldi mi? Sinyalde fon payı %2'nin altındayken sonraki 12 ayda raporlu fonların payı sermayenin "
            "%5'ine (ve %2'sine) çıktı mı; çöl sinyali vs aynı düşüş sonrası tarife uymayan günler (eşli). Soru 2 — büyük alıcı gelmeden ÖNCE çöl "
            "var mıydı? Fonun ilk kez %5'i geçtiği hisselerde önceki 12 ayda sinyal oranı vs aynı tarihte fon girmemiş 10 rastgele hisse. "
            "Geçme şartı (önceden): iki soruda da 1,3 kat."])
        ax = fig.add_axes([0.10, 0.40, 0.84, y - 0.45])
        for j, g in enumerate(G):
            if g in o1.index:
                ax.bar(np.arange(2) + j * 0.2 - 0.3, [100 * o1.loc[g, "giris5"], 100 * o1.loc[g, "giris2"]], 0.2, color=R[j], label=g)
        ax.set_xticks(range(2)); ax.set_xticklabels(["12 ayda fon payı ≥ %5", "12 ayda fon payı ≥ %2"], fontsize=8.5)
        ax.set_ylabel("sinyallerin %'si", fontsize=8); ax.legend(fontsize=7.5); ax.set_title("Soru 1: çölden sonra fon geldi mi?", fontsize=9.5)
        ax = fig.add_axes([0.10, 0.07, 0.84, 0.25])
        if len(o2):
            for j, tip in enumerate(["fon girişi", "kontrol"]):
                if tip in o2.index:
                    ax.bar(np.arange(o2.shape[1]) + (j - 0.5) * 0.36, 100 * o2.loc[tip].to_numpy(), 0.36, color=["#1f2a44", "#9aa5b8"][j],
                           label=f"{tip} ({n2} olay)" if tip == "fon girişi" else "fon girmemiş kontrol (10 hisse / olay)")
            ax.set_xticks(range(o2.shape[1])); ax.set_xticklabels([c.replace("var_", "") for c in o2.columns], fontsize=8)
            ax.legend(fontsize=7.5)
        ax.set_ylabel("önceki 12 ayda sinyal görülme %", fontsize=8); ax.set_title("Soru 2: fon gelmeden önce çöl var mıydı?", fontsize=9.5)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=A4)
        d2 = lambda g, m: D[(D.grup == g) & m(D)]
        sat = []
        for g in ("K24 kural", "K18 profil"):
            a, b = d2(g, lambda x: x.pay0 >= 0.02), d2(g, lambda x: x.pay0 < 0.005)
            sat.append(f"- {g}: çölde fon VAR (pay ≥ %2, n {len(a)}): 250 günde 2 kat {yz((a.mx >= 1).mean())}, 60 günde önce +%15 "
                       f"{yz((a.y60 == 1).mean())}; fon YOK (n {len(b)}): 2 kat {yz((b.mx >= 1).mean())}, +%15 {yz((b.y60 == 1).mean())}.")
        sat3 = []
        for g in G:
            x = D[(D.grup == g) & ~D.sembol.isin(fon)]
            sat3.append(f"- {g} (n {len(x)}): 2 kat {yz((x.mx >= 1).mean())}, 60 günde önce +%15 {yz((x.y60 == 1).mean())}, önce −%15 {yz((x.y60 == -1).mean())}")
        yazi(fig, 0.96, "ÖNCEDEN YAZILAN İKİ DENEME (fon krizi dışarıda: 31.08.2026'da kesik)", [
            "Sen: 'TERA'nın düşüşü fon krizinden; ona bakmamak lazım.' Doğru: Eylül 2026 krizi şekille ilgisiz bir dış olay. Aşağıdaki bütün "
            "sonuçlarda fiyat 31 Ağustos 2026'da kesildi. Kriz dışarıda kalınca kuralın −%30'a düşen oranı %43'ten %32'ye iniyor; eşlide %30.",
            "DENEME 2 — çöl + fon birlikte: sinyal anında fon zaten içerideyse çöl daha mı iyi?"] + sat + [
            "DENEME 3 — fon hisseleri (23 hisse) evrenden çıkarılınca kural vs eşli:"] + sat3 + [
            "",
            "SONUÇ",
            "- Görünen büyük alıcı (raporlu fon) çölden sonra eşli günlerden belirgin daha sık gelmiyor (1,1 kat civarı); fon girişlerinden önce "
            "çöl de daha sık değil. Çölde fon zaten varsa sonrası daha KÖTÜ. Fon hisseleri çıkarılınca çöl = eşli. → Senin mantığın (çok alıcı -> "
            "çöl) fon raporlarında görünmüyor.",
            "- Açık kalan: savcılık anlatımına göre fon hissesi önce kişisel hesaplarda toplandı, sonra fonlara satıldı. Bu GÖRÜNMEYEN alıcı fon "
            "raporunda yok. Onu görmek için aracı kurum dağılımı (AKD, günlük hangi kurum ne aldı) gerekir; ücretli veri — senin kararın.",
            "- Senin gözün fon hisselerindeki çölleri doğru gördü (TEHOL, BIGEN, ANELE, HEDEF); ama aynı şekil fon olmayan yüzlerce hissede de var "
            "ve onların sonrası sıradan. Şekil 'burada büyük alıcı var' demiyor.",
            "",
            "Sıradaki (önceden yazılı): (1) kör set ✓/✗ ile gözünün ayırdığı şey; (2) AKD verisi gelirse çölde tek kurumun net alıcı olduğu "
            "günler; (3) KAP %5 pay değişim bildirimleri (ortaklık yapısı) çölden sonra daha sık mı."])
        pdf.savefig(fig); plt.close(fig)
    return 2


def fon_izi_k10(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    """v1.5 surucu: K9 tablolar -> K10 fon girisi/cikisi testi (BIST 2023 / 2024-26) -> K11 fon hisseleri defteri -> rapor."""
    A = A or FIAyar(); os.makedirs(A.cikti, exist_ok=True)
    L = pd.read_csv(os.path.join(A.kapfon, "liste.csv")); Ek = fi_k9_ekler_oku(A)
    P, I, K = fi_k9_tablolar_guncel(L, Ek, A)
    V = fi_k1_veri(A.veri["BIST"], "BIST", A)
    G, KP = fi_k10_pozisyon(P, K, list(V))
    with open(A.veri["BIST"], "rb") as f:
        ham = pickle.load(f)
    ham = ham["veri"] if isinstance(ham, dict) and "veri" in ham else ham
    try:
        dol = fi_isy_dolasim(A.isy)
    except Exception as ex:
        filog.warning("fiili dolasim okunamadi (%s); pay ve yogun olaylari hesaplanmaz", ex); dol = None
    oran = fi_k10_oran(V, ham)
    E = fi_k10_olaylar(G, KP, oran, dol)
    E["tur_giris"] = E.tur == "giris"
    E = E.dropna(subset=["bilinme"]).reset_index(drop=True)
    R = fi_k10_sonuc(V, E.kod, E.bilinme)
    E = E.join(R, how="inner")
    B = fi_k10_taban(V, "2023-01-15", str(pd.Timestamp.today().date()))
    Oz = fi_k10_ozet(E, B)
    kos_yol = os.path.join(A.cikti, "fon_kosular.csv")
    kos = pd.read_csv(kos_yol) if os.path.exists(kos_yol) else fi_k3_vaka(V, A)[0]
    D, Z = fi_k11_defter(I, G, V, kos)
    MA, MZ = fi_k11_aylik(G, V, ham, kos, dol)
    MA.to_csv(os.path.join(A.cikti, "k11_aylik_birikim.csv"), index=False); MZ.to_csv(os.path.join(A.cikti, "k11_birikim_ozet.csv"), index=False)
    tl = G[G.kod.isin(FON_HISSE)].copy()
    tl["tasfiye_lot"] = np.where(tl.sirket.astype(str).str.upper().str.match(FI_TASFIYE_RE), tl.nominal, 0.0)
    M = tl.groupby(["kod", "ay"]).agg(fon_sayisi=("fon", "nunique"), lot=("nominal", "sum"), tasfiye_lot=("tasfiye_lot", "sum")).reset_index()
    M["ay"] = [f"{a // 12}-{a % 12 + 1:02d}" for a in M.ay]
    kap = K.assign(sirket=K.sirket.astype(str), muaf=K.get("muaf", pd.Series(False, index=K.index)).fillna(False).astype(bool),
                   poz_tuttu=K.poz_tuttu.fillna(False).astype(bool), islem_bolum=K.islem_bolum.fillna(False).astype(bool))
    kap = kap.groupby("sirket").agg(rapor=("indeks", "size"), muaf=("muaf", "sum"), poz_tuttu=("poz_tuttu", "sum"),
                                    islem_bolum=("islem_bolum", "sum")).reset_index().sort_values("rapor", ascending=False)
    E.to_csv(os.path.join(A.cikti, "k10_olaylar.csv.gz"), index=False)
    Oz.to_csv(os.path.join(A.cikti, "k10_ozet.csv"), index=False)
    D.to_csv(os.path.join(A.cikti, "k11_defter_gunluk.csv.gz"), index=False)
    Z.to_csv(os.path.join(A.cikti, "k11_defter_faz.csv"), index=False)
    M.to_csv(os.path.join(A.cikti, "k11_aylik_pozisyon.csv"), index=False)
    kap.to_csv(os.path.join(A.cikti, "k9_kapsam_sirket.csv"), index=False)
    with open(os.path.join(A.cikti, "FON_IZI_k10_rapor.md"), "w", encoding="utf-8") as f:
        f.write(fi_k10_rapor(Oz, MZ, K, E, int((Ek.durum == "muaf").sum())))
    try:
        fi_k11_grafik(MA, D, V, kos, os.path.join(A.cikti, "FON_IZI_fon_birikim.pdf"))
    except Exception as ex:   # grafik bozulursa tablolar yine yazilir
        filog.error("birikim grafigi cizilemedi: %s", ex)
    try:
        fi_k12_ders(V, MA, D, kos, Oz, os.path.join(A.cikti, "FON_IZI_ders.pdf"))
    except Exception as ex:   # ders bozulursa tablolar yine yazilir
        filog.error("ders PDF'i cizilemedi: %s", ex)
    try:
        tespit = os.path.join(os.path.dirname(A.cikti.rstrip("/")), "col_tespit")
        fi_k12_ders_u(V, MA, pd.read_csv(os.path.join(tespit, "col_tespit_sinyal.csv.gz"), low_memory=False),
                      pd.read_csv(os.path.join(tespit, "col_tespit_varyant_donem.csv")), os.path.join(A.cikti, "FON_IZI_ders2_U.pdf"))
    except Exception as ex:   # COL_TESPIT ciktisi yoksa ders 2 atlanir
        filog.error("ders 2 (U sekli) PDF'i cizilemedi: %s", ex)
    return {"P": P, "I": I, "K": K, "G": G, "olaylar": E, "taban": B, "ozet": Oz, "defter": D, "faz": Z, "aylik": M, "kapsam": kap,
            "birikim": MA, "birikim_ozet": MZ}


# ---------------------------------------------------------------- K5 rapor
def fi_k5_rapor(kos: pd.DataFrame, faz: pd.DataFrame, tet: pd.DataFrame, oz: pd.DataFrame, iz: pd.DataFrame,
                ekler: Optional[Dict[str, pd.DataFrame]] = None) -> str:
    fm = faz.groupby("faz").median(numeric_only=True).reindex(["ONCE", "ERKEN", "KOSU", "COKUS"])
    kos = kos.copy(); tet = tet.copy()
    for t, kol in ((kos, ("dip", "x2", "tepe")), (tet, ("ilk_iz",))):
        for c in kol:
            t[c] = pd.to_datetime(t[c]).dt.date
    sat = [f"# FON_IZI — {FI_SURUM}", "",
           "Soru (Cemal, 22 Eki): tasfiye fonlarinin topladigi hisseler (20-290 kat) yukselise giderken nasil bir iz birakti?", "",
           "## Vaka kosulari (dip -> tepe, 15 Eyl 2026 oncesi; duzeltilmis fiyat)", "", kos.round(2).to_markdown(index=False), "",
           "## Faz medyanlari (23 hisse)", "", fm.round(2).to_markdown(), "",
           "## Faz ayrintisi", "", faz.round(2).to_markdown(index=False), "",
           "## Iz B ilk tetik (gercek zamanli) ve sonrasi", "", tet.round(2).to_markdown(index=False), "",
           "## Evren testi: iz varyantlari (4 dilim, kat = once 2 kat orani / ayni yukselisin izsiz kismi)", "",
           iz.round(2).to_markdown(index=False), "", "## Dilim ayrintisi", "", oz.round(2).to_markdown(index=False), ""]
    for baslik, t in (ekler or {}).items():
        sat += [f"## {baslik}", "", t.round(2).to_markdown(index=False), ""]
    return "\n".join(sat)


def fon_izi(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    A = A or FIAyar()
    os.makedirs(A.cikti, exist_ok=True)
    veri = {}
    for pazar, yol in A.veri.items():
        try:
            veri[pazar] = fi_k1_veri(yol, pazar, A)
        except Exception as ex:
            filog.error("%s verisi okunamadi (%s); bu pazar atlandi", pazar, ex)
    if "BIST" not in veri:
        raise RuntimeError("BIST verisi yok; vaka incelemesi yapilamaz")
    kos, faz, tet = fi_k3_vaka(veri["BIST"], A)
    O = pd.concat([fi_k4_olaylar(V, p, A) for p, V in veri.items()], ignore_index=True)
    oz, iz = fi_ozet(O)
    ekler: Dict[str, pd.DataFrame] = {}; zbayrak: Dict[str, pd.Series] = {}
    try:
        hoz, hhisse, zbayrak = fi_k3b_hacim_vaka(veri["BIST"], kos, A)
        HO = pd.concat([fi_k4b_hacim_olaylar(V, p, A) for p, V in veri.items()], ignore_index=True)
        hev, hiz = fi_ozet_hacim(HO)
        hoz.to_csv(os.path.join(A.cikti, "fon_hacim_vaka.csv"), index=False)
        hhisse.to_csv(os.path.join(A.cikti, "fon_hacim_hisse.csv"), index=False)
        HO.to_csv(os.path.join(A.cikti, "fon_hacim_olaylar.csv.gz"), index=False)
        hev.to_csv(os.path.join(A.cikti, "fon_hacim_ozet.csv"), index=False)
        pd.DataFrame([{"sembol": s, "tarih": t} for s, z in zbayrak.items() for t in z[z].index]).to_csv(
            os.path.join(A.cikti, "fon_z0_gunleri.csv"), index=False)
        ekler = {"v1.1 HACIM ESLIGI: fon hisselerinin sessiz yuvarlanma (Z0) bolgeleri vs diger BIST hisseleri (2024-26)": hoz,
                 "v1.1 Fon hisseleri Z0 icindeki hacim (hisse basina medyan)": hhisse,
                 "v1.1 Evren testi: Z0 + hacim varyantlari (kat = varyant / Z0'in geri kalani)": hiz,
                 "v1.1 Evren dilim ayrintisi": hev}
    except Exception as ex:  # hacim eki bozulursa v1.0 sonuclari yine yazilir
        filog.error("v1.1 hacim esligi yazilamadi: %s", ex)
    kos.to_csv(os.path.join(A.cikti, "fon_kosular.csv"), index=False)
    faz.to_csv(os.path.join(A.cikti, "fon_fazlar.csv"), index=False)
    tet.to_csv(os.path.join(A.cikti, "fon_iz_tetik.csv"), index=False)
    O.to_csv(os.path.join(A.cikti, "fon_izi_olaylar.csv.gz"), index=False)
    oz.to_csv(os.path.join(A.cikti, "fon_izi_ozet.csv"), index=False)
    rapor = fi_k5_rapor(kos, faz, tet, oz, iz, ekler)
    with open(os.path.join(A.cikti, "FON_IZI_rapor.md"), "w", encoding="utf-8") as f:
        f.write(rapor)
    return {"kosular": kos, "fazlar": faz, "tetik": tet, "olaylar": O, "ozet": oz, "iz": iz, "veri": veri, "ekler": ekler}


def _cakisma_kontrol_fi(_once=_CK_ONCE_FI, _dosya='FON_IZI.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_FI', '_CK_KAYIT', '_cakisma_kontrol_fi', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'time', 'pickle', 'logging', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass', 'field')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_fi()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "k9indir":       # v1.5: KAP portfoy dagilim raporlari listesi + metin
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _A = FIAyar(); _E = fi_k9_indir(fi_k9_liste(_A), _A)
        print(_E.durum.value_counts().to_string())
        sys.exit(0)
    if len(sys.argv) > 3 and sys.argv[1] == "vpac":          # işlenmiş veri paketini (islenmis-veri dalı) aç: vpac <paket> <hedef>
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        print(fi_veri_paket_ac(sys.argv[2], sys.argv[3]))
        sys.exit(0)
    if len(sys.argv) > 2 and sys.argv[1] in ("k9paket", "k9ac"):   # v1.5: tasinabilir KAP fon verisi paketi (yaz / ac)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _M = fi_k9_paketle(FIAyar(), sys.argv[2]) if sys.argv[1] == "k9paket" else fi_k9_paket_ac(sys.argv[2], FIAyar())
        print({k: v for k, v in _M.items() if k != "dosyalar"})
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k10":           # v1.5: fon girisi testi + fon defteri
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k10()
        print(_R["ozet"].round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k13":           # TEHOL tipi taban olcusu (Ders 3)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k13()
        print(_R["ozet"].round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k14":           # K13'un uc devam denemesi (ruzgar, yukselis, kirilim)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k14()
        for _k, (_Z, _karar, _H) in _R["sonuc"].items():
            print(_k, _karar); print(_Z.round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k15":           # K14'un ikinci turu (genislik, oynaklik esli, 3 kat)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k15()
        for _k, (_Z, _karar, _H) in _R["sonuc"].items():
            print(_k, _karar); print(_Z.round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k16":           # duzgun dip devam denemeleri (2 kat, esli kutu)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k16()
        for _k, (_Z, _karar, _H) in _R["sonuc"].items():
            print(_k, _karar); print(_Z.round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k17":           # iki yuvarlama (önce aşağı, ardından yukarı)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k17()
        for _k, (_Z, _karar, _H) in _R["sonuc"].items():
            print(_k, _karar); print(_Z.round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k17ders":       # Ders 6 (k17 ve IZ_KARNE Ç78-Ç83 çıktılarından)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _A = FIAyar(); _O = pd.read_csv(os.path.join(_A.cikti, "k17_olaylar.csv.gz"), low_memory=False)
        _O = _O[_O.pazar == "BIST"]
        _KH = pd.read_csv(os.path.join(os.path.dirname(_A.cikti.rstrip("/")), "iz_karne", "karne_hucre.csv"))
        fi_k12_ders6(fi_k1_veri(_A.veri["BIST"], "BIST", _A), _O, _KH, os.path.join(_A.cikti, "FON_IZI_ders6_iki_yuvarlama.pdf"))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k18":           # Cemal'in vakaları: ortak iz (çöl + atılım profili), evren + liste
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k18()
        for _k, (_Z, _karar, _H) in _R["sonuc"].items():
            print(_k, _karar); print(_Z.round(3).to_string(index=False))
        print(_R["vaka"].round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k18ders":       # Ders 7 (k18 ve IZ_KARNE Ç85-Ç90 çıktılarından)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _A = FIAyar(); _O = pd.read_csv(os.path.join(_A.cikti, "k18_olaylar.csv.gz"), low_memory=False)
        _O = _O[(_O.pazar == "BIST") & (_O.varyant == "esli") & (pd.to_datetime(_O.bilgi) >= "2024-01-01")]
        _KH = pd.read_csv(os.path.join(os.path.dirname(_A.cikti.rstrip("/")), "iz_karne", "karne_hucre.csv"))
        print(fi_k12_ders7(fi_k1_veri(_A.veri["BIST"], "BIST", _A), pd.read_csv(os.path.join(_A.cikti, "k18_vaka.csv")),
                           pd.read_csv(os.path.join(_A.cikti, "k18_ozet.csv")), _KH, pd.read_csv(os.path.join(_A.cikti, "k18_liste_BIST.csv")),
                           _O, os.path.join(_A.cikti, "FON_IZI_ders7_cemal_vakalar.pdf")), "sayfa")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k19":           # sistem (kırılım + kutu dibi stop + trail) rastgeleden iyi mi
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k19()
        print(_R["karar"]); print(_R["ozet"].round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k19ders":       # Ders 8 (k19 çıktılarından)
        _A = FIAyar()
        print(fi_k12_ders8(pd.read_csv(os.path.join(_A.cikti, "k19_ozet.csv")),
                           pd.read_csv(os.path.join(_A.cikti, "k19_islem.csv.gz"), low_memory=False),
                           os.path.join(_A.cikti, "FON_IZI_ders8_sistem_rastgele.pdf")), "sayfa")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k21":           # sağ ayak mum mum: çöl atılımı vs aynı gün bütün hisseler + en sıkı çöl
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k21()
        print(_R["karar"]); print(_R["ozet"].round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k22":           # çöl tavanında bekleyen alış emri (atılım mumu dahil) vs aynı gün bütün hisseler
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k22()
        print(_R["karar"]); print(_R["ozet"].round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k23":           # işaretli bölgenin parmak izi + birebir benzer bölgeler (yukarı / aşağı / yatay)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k23()
        print(_R["karar"]); print(_R["parmak"].to_string()); print(_R["ozet"].round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k24":           # iki evre kuralı (SMA20 altı -> SMA20 üstünde dizilme) vs eşli
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k24()
        print(_R["karar"]); print(_R["ozet"].round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k21ders":       # Ders 9 (k21 + k22 çıktılarından)
        _A = FIAyar()
        print(fi_k12_ders9(fi_k1_veri(_A.veri["BIST"], "BIST", _A), pd.read_csv(os.path.join(_A.cikti, "k21_ozet.csv")),
                           pd.read_csv(os.path.join(_A.cikti, "k21_yol.csv")), pd.read_csv(os.path.join(_A.cikti, "k22_ozet.csv")),
                           pd.read_csv(os.path.join(_A.cikti, "k22_pencere.csv")), os.path.join(_A.cikti, "FON_IZI_ders9_sag_ayak_mum.pdf")), "sayfa")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k23ders":       # Ders 10 (k23 + k24 çıktılarından)
        _A = FIAyar()
        print(fi_k12_ders10(fi_k1_veri(_A.veri["BIST"], "BIST", _A), pd.read_csv(os.path.join(_A.cikti, "k23_ozet.csv")),
                            pd.read_csv(os.path.join(_A.cikti, "k23_parmak.csv")), pd.read_csv(os.path.join(_A.cikti, "k23_esler.csv")),
                            pd.read_csv(os.path.join(_A.cikti, "k24_ozet.csv")), os.path.join(_A.cikti, "FON_IZI_ders10_bolge_parmak.pdf")), "sayfa")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k23kornet":     # kör set v3: aynı 48 aday, net mum grafiği
        _A = FIAyar()
        print(fi_k23_kor_pdf_net(fi_k1_veri(_A.veri["BIST"], "BIST", _A), pd.read_csv(os.path.join(_A.cikti, "k23_kor_anahtar.csv")),
                                 pd.read_csv(os.path.join(_A.cikti, "k23_parmak.csv")),
                                 os.path.join(_A.cikti, "FON_IZI_kor_set_net.pdf")), "sayfa")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k23kor4":       # kör set v4: kutu + alış mumu + 1 yıl geri zum
        _A = FIAyar()
        print(len(fi_k23_kor4_pdf(fi_k1_veri(_A.veri["BIST"], "BIST", _A), pd.read_csv(os.path.join(_A.cikti, "k23_parmak.csv")),
                                  os.path.join(_A.cikti, "FON_IZI_kor_set_v4.pdf"), os.path.join(_A.cikti, "k23_kor4_anahtar.csv"),
                                  os.path.join(_A.cikti, "k23_kor4_havuz.csv"))), "aday")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "k26":           # dört örneğin ortak parmak izi + BIST/ABD taraması
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
        _R = fon_izi_k26()
        print(_R["karar"], _R["ortak"]["ortak"]); print(_R["ozet"].round(3).to_string(index=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "gosterge":
        R = fon_izi_gosterge()
        print(R["iz"].round(2).to_string(index=False))
        sys.exit(0)
    R = fon_izi()
    print(R["iz"].round(2).to_string(index=False))
    print(R["fazlar"].groupby("faz").median(numeric_only=True).round(2).to_string())
