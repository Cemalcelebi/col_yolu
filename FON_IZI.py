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

FI_SURUM = "FON_IZI v1.5 (2026-10-24, yukselis izi + hacim esligi + gosterge/uyumsuzluk/Fibonacci/blok hacim/KAP; denetim duzeltmeleri; KAP fon raporlari: defter + fon girisi testi)"
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
def fi_duzelt(d: pd.DataFrame, A: FIAyar, bedelsiz: Optional[pd.DatetimeIndex] = None) -> Tuple[pd.DataFrame, int]:
    """BIST ham fiyat: gunluk siniri asan sicramalari geriye dogru carpanla duzeltir. Donus: (duzeltilmis, sicrama sayisi).
    v1.4: sinir 13.03.2020'ye kadar %20 (eskiden 01.03.2020 aliniyordu; Mart 2020 cokusunun 537 gunu bolunme sanilip siliniyordu).
    Gecis donemi (13.03.2020-28.02.2021): %10,5-21 sicrama ancak `bedelsiz` (KAP bedelsiz bildirim tarihleri) yakininda bolunme sayilir;
    kayit yoksa gercek hareket kabul edilir."""
    d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float).copy()
    oran = d.Close / d.Close.shift()
    lim = np.where(d.index >= pd.Timestamp(A.limit_tarih), A.limit_yeni, A.limit_eski)
    kir = (oran - 1).abs() > lim
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
    out = {}
    for s, d in V.items():
        try:
            if "Volume" not in d.columns:
                continue
            d = d.dropna(subset=["Open", "High", "Low", "Close"])
            d = d[(d.High >= d.Low) & (d.Close > 0)].sort_index()
            if pazar == "BIST":
                d, _ = fi_duzelt(d, A, bdz.get(str(s)))
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
    iz["iz"] = np.where(iz.yon == "yukari", (iz.gecti_k20 == iz.dilim) | (iz.gecti_x2 == iz.dilim), iz.gecti_dus == iz.dilim) & (iz.dilim >= 4)
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
    # hisse-ay toplu: iki ay da raporu olan fonlarda toplam nominal ve onceki ay sahip sayisi
    ikili = KP[[(f, a - 1) in var for f, a in zip(KP.fon, KP.ay)]][["fon", "ay"]]
    simdi = G.merge(ikili, on=["fon", "ay"]).groupby(["kod", "ay"]).nominal.sum().rename("top_simdi")
    gecen = G.assign(ay=G.ay + 1).merge(ikili, on=["fon", "ay"]).groupby(["kod", "ay"]).agg(
        top_gecen=("nominal", "sum"), sahip_gecen=("fon", "nunique"))
    T = pd.concat([simdi, gecen], axis=1).fillna(0).reset_index()
    E = E.merge(T, on=["kod", "ay"], how="left")
    E["ilk"] = E.sahip_gecen.fillna(0) == 0
    E["artis"] = (E.top_simdi / E.top_gecen.where(E.top_gecen > 0)).fillna(np.inf) - 1 >= FI_K10_ESIK["artis"]
    E["buyuk"] = E.agirlik >= FI_K10_ESIK["buyuk"]
    E["tasfiye"] = E.sirket.astype(str).str.contains("|".join(s.split(" PORTF")[0] for s in FI_FON_SIRKET))
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
        tasf = g[g.sirket.astype(str).str.contains("|".join(x.split(" PORTF")[0] for x in FI_FON_SIRKET))].groupby("ay").nominal.sum()
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
            ay["pay_sermaye"] = ay.duz_tasfiye / (r.sermaye_lot * ay.oran.iloc[-1]) if r.sermaye_lot > 0 else np.nan
            ay["pay_halka_acik"] = ay.duz_tasfiye / (r.dolasim_lot * ay.oran.iloc[-1]) if r.dolasim_lot > 0 else np.nan
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
    tl["tasfiye_lot"] = np.where(tl.sirket.astype(str).str.contains("|".join(s.split(" PORTF")[0] for s in FI_FON_SIRKET)), tl.nominal, 0.0)
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
    if len(sys.argv) > 1 and sys.argv[1] == "gosterge":
        R = fon_izi_gosterge()
        print(R["iz"].round(2).to_string(index=False))
        sys.exit(0)
    R = fon_izi()
    print(R["iz"].round(2).to_string(index=False))
    print(R["fazlar"].groupby("faz").median(numeric_only=True).round(2).to_string())
