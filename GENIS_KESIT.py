"""GENIS_KESIT — fon krizinde çökmüş 64 BIST hissesinde Kasım dönüşünü 31.10.2026'da BİLİNEN hangi özellik önceden gösteriyordu? (13 Kasım 2026). Tek dosya.

Soru (ters bakış): fon krizinde %80+ düşmüş 64 BIST hissesinden (TAVAN_SERISI canli, cokmus == True) bazıları dipten 2-3 kat çıktı, bazıları dipte
kaldı. 31.10.2026 itibarıyla BİLİNEN hangi özellik 1-13 Kasım dönüşünün büyüklüğünü önceden gösteriyordu? Kesit; n küçük, AÇIKLAYICI.
GELECEĞE BAKMA YOK: her açıklayıcı yalnız <= 31.10.2026 bilgisiyle kurulur (fiyat 30.10 son barında kesilir, KAP yayın zamanı <= 31.10 23:59;
kural `gk_ileri_denetim` ile mekanik sınanır).

Akış (her adım ayrı komut; ön kayıt kapısı ölçümden önce):
  python GENIS_KESIT.py topla       KAP'tan eksik metinler / ekler / şirket sayfaları / geçmiş liste (yalnız kap.org.tr; önbellek /tmp/tavan/kesit)
  python GENIS_KESIT.py x           açıklayıcı tablosu X (yalnız <= 31.10 bilgisi) -> /tmp/tavan/kesit/X.csv (+ kanıt satırları)
  python GENIS_KESIT.py onkayit     arastirma_cikti/genis_bakis/KESIT_ON_KAYIT.md (eşik mührü, kod / X / veri sha256; üzerine yazmaz)
  -> commit + push (ÖLÇÜMDEN ÖNCE)
  python GENIS_KESIT.py sonuc_indir 64 hissenin 13.11 fiyatı Yahoo'dan ayrı klasöre (TAVAN_SERISI.ts_indir; kesit/yahoo_son)
  python GENIS_KESIT.py kos [--sapma G]  kapı (ön kayıt git'te + mühür + X sha + kod sha) -> Y1/Y2/Y3, Spearman + permütasyon + BH,
                                    derinlik-2 ağaç (LOO), 4 hisse çöl tablosu -> kesit_sonuc.json + KESIT_RAPOR.md
  python GENIS_KESIT.py rapor       raporu sonuç JSON'undan yeniden yazar
Colab:  exec(open('GENIS_KESIT.py').read())  (TAVAN_SERISI.py, K60_veri.py, COL_v1.py, FON_IZI.py aynı klasörde)
SINIR:  IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md'ye dokunmaz; TAVAN_SERISI.py / COL_v1.py / FON_IZI.py DEĞİŞTİRİLMEZ
        (yalnız okunur). Ağ yalnız `topla` (kap.org.tr) ve `sonuc_indir` (Yahoo). E-posta / anahtar / kişisel bilgi gönderilmez; veri repoya girmez.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_GK = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import glob  # noqa: E402
import hashlib  # noqa: E402
import html as _html  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_GK = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_GK not in sys.path:
    sys.path.insert(0, KOK_GK)
import TAVAN_SERISI as TS  # noqa: E402  (fiyat okuma, tavan tanımı, git denetimi; DEĞİŞTİRİLMEZ)

gklog = logging.getLogger("col.genis_kesit")
if not gklog.handlers:
    _gk_h = logging.StreamHandler(sys.stderr)
    _gk_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s kesit: %(message)s", "%H:%M:%S"))
    gklog.addHandler(_gk_h)
    gklog.setLevel(logging.INFO)
    gklog.propagate = False

GK_ETIKET = "genis_kesit_20261113"
GK_SURUM = "GENIS_KESIT v1.0 (genis_kesit_20261113): çökmüş 64 BIST hissesi, 31.10'da bilinen özellik vs 1-13 Kasım dönüşü (kesit, ön kayıtlı)"

GK_YOL: Dict[str, str] = {
    "cikti": os.environ.get("GK_CIKTI", os.path.join(KOK_GK, "arastirma_cikti", "genis_bakis")),
    "tavan": os.environ.get("GK_TAVAN", "/tmp/tavan"),
    "is": os.environ.get("GK_IS", "/tmp/tavan/kesit"),
    "veri": os.environ.get("GK_VERI", "/tmp/veri"),
    "yahoo": os.environ.get("GK_YAHOO", "/tmp/tavan/yahoo"),
    "yahoo_son": os.environ.get("GK_YAHOO_SON", "/tmp/tavan/kesit/yahoo_son"),
}
GK_DOSYA: Dict[str, str] = {"onkayit": "KESIT_ON_KAYIT.md", "sonuc": "kesit_sonuc.json", "rapor": "KESIT_RAPOR.md", "X": "X.csv",
                            "kanit": "X_kanit.json", "Y": "Y.csv"}
_GK_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")
_GK_KAP = "https://www.kap.org.tr"
_GK_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

# ---------------------------------------------------------------- ÖN KAYITLI TANIMLAR (sha256 mührü ön kayıtta; sonuç görüldükten sonra değişmez)
GK_ESIK: Dict[str, Any] = {
    "surum_etiket": GK_ETIKET,
    "orneklem": {"kaynak": "/tmp/tavan/canli_cokmus.csv (TAVAN_SERISI canli, 13.11.2026)",
                 "kural": "cokmus == True: 1 Haz - 31 Ağu 2026 en yüksek kapanıştan 1 Eyl 2026 sonrası en düşük kapanışa düşüş <= -%80, tepe sonrası "
                          "veri kırığı yok", "n": 64},
    "kesim": "2026-10-31",
    "kesim_tanim": "BİLGİ KESİMİ 31.10.2026 23:59 (TR). Fiyat: tarihi <= 31.10 olan son bar (30.10.2026 Cuma kapanışı; 29.10 tatil). KAP: yayın "
                   "zamanı <= 31.10.2026 23:59. Bilanço: açıklama tarihi <= 31.10. Fon raporu: bilinme <= 31.10. Bu tarihten sonraki hiçbir bilgi X'e girmez.",
    "sonuc": {
        "Y1": "C(13.11.2026 son bar) / C(kesim barı); fiyat Yahoo, 64 hisse için ayrı klasöre (kesit/yahoo_son) yeniden indirilir "
              "(TAVAN_SERISI.ts_indir); indirme 13.11 15:10 UTC (18:10 TR, seans kapanışı sonrası) SONRASINDA yapılır (kapanış); kapanış "
              "alınamazsa gün içi son bar kullanılır ve raporda 'gün içi' yazılır",
        "Y2": "02.11 - 13.11.2026 barlarında tavan günü sayısı (TAVAN_SERISI.ts_tavan tanımı; 13.11 gün içiyse o bar da sayılır)",
        "Y3": "C(13.11) / en düşük kapanış (01.09.2026 - 13.11.2026)",
        "birincil": "Y1 (karar Y1 üzerinden; Y2 yön teyidi; Y3 BİLGİ)",
        "fiyat": "Yahoo bölünme düzeltmeli kapanış (TAVAN_SERISI.ts_yahoo_oku); oranlar ölçekten bağımsız"},
    "x": {
        "x01_tepe250": "C(kesim) / son 250 barın (<= kesim) en yüksek kapanışı - 1 (en az 20 bar; yeni halka arzda mevcut barlar)",
        "x02_log_fiyat": "log10(ekran fiyatı) kesim barında (Yahoo kapanış x sonraki bölünme çarpanı = o günkü ekran fiyatı)",
        "x03_fon_kriz": "kriz öncesi fon payı = canli_cokmus.csv fon_pay_kriz_oncesi (FON_IZI.fi_k25_pay_tablo, KAP fon raporu bilinme <= 31.08.2026); "
                        "hisse hiçbir fon raporunda yoksa 0 (serbest fonlar KAP raporunda eksik olabilir: sınır)",
        "x04_tasfiye_kalan": "TASFİYE FONU KALAN PAYI (%): MKK eşik tabloları (esik_tum.csv; KAP 'Kamuyu Aydınlatma Platformu Duyurusu' 12-(4) ekleri, günlük) "
                             "satırlarından sahibi tasfiye kapsamındaki portföy şirketlerinin (COL_v1.FON_TASFIYE: TERA, PUSULA, HEDEF, ATLAS, A1, PARDUS, "
                             "BULLS PORTFÖY) bir FONU olanlar; her (hisse, fon) için yayın <= 31.10 olan son satırın 'sonraki %' değeri; fonlar toplanır. "
                             "Kayıt yoksa 0 (eşik altı bilinmez)",
        "x04b_satis_bitti": "SATIŞ BİTTİ (1/0) = 17.10 - 31.10.2026 yayınlı eşik satırlarında hisse için hiçbir sahipten AZALIŞ (sonraki % < önceki %) yok "
                            "(son 2 haftada azalış bildirimi yok)",
        "x05_azalis_sayisi": "Eylül - Ekim (yayın 01.09 - 31.10) eşik tablolarında hisse için AZALIŞ satırı sayısı (her sahip; satış baskısı yoğunluğu)",
        "x06_leke": "LEKE (1/0): (a) SPK bülteni (yayın <= 31.10; 2026/56 - 2026/78) metninde '(KOD)' ya da 'KOD Pay Piyasas' geçen satırın 3 satır "
                    "öncesi - 6 satır sonrası içinde 'suç duyurusu' / 'işlem yasağı' / '107/1' / '106/1' (idari para cezası tek başına sayılmaz); YA DA (b) hissenin kendi KAP bildirimi (stockCodes; yayın 01.09 - 31.10) "
                    "konu / özet / metninde kayyım|kayyum|TMSF|Tasarruf Mevduatı Sigorta Fonu|tutukla|gözaltı; aynı cümlede olumsuzlama (bulunmamak|yoktur|"
                    "olmamış|alınmamış|söz konusu değil|ilgisi) varsa sayılmaz",
        "x06b_mkk_yasak": "MKK 'SPK İşlem Yasağı Nedeniyle Pay Duyurusu' (yayın <= 31.10) ilgili paylarında (relatedStocks) geçiyor (1/0)",
        "x07_geri_alim": "GERİ ALIM (1/0): hissenin kendi 'Payların Geri Alınmasına İlişkin Bildirim'i (program ilanı ya da işlem), yayın 01.09 - 31.10",
        "x07b_geri_alim_sayi": "aynı bildirimlerden özeti program başlatma / program kararı OLMAYANLARIN sayısı (gerçekleşen geri alım işlemi yoğunluğu vekili)",
        "x08_pddd": "PD/DD = sermaye_lot (dol.pkl) x ekran kapanış(kesim) / özkaynak; özkaynak = temel_duz.csv son dönem (açıklama <= 31.10); yoksa KAP "
                    "Finansal Rapor (yayın <= 31.10, en son iki rapor) 'Ana Ortaklığa Ait Özkaynaklar', yoksa 'Toplam Özkaynaklar', yoksa 'ÖZKAYNAKLAR' "
                    "(finans şirketi biçimi) cari dönem, 'Sunum Para Birimi' çarpanıyla (1.000 TL -> x1000). Özkaynak <= 0 -> 1e6 "
                    "(en pahalı sıra); bulunamazsa eksik",
        "x09_halka_aciklik": "halka açıklık oranı (dol.pkl 'hao', %; kriz öncesi MKK / KAP değeri)",
        "x10_hacim_oran": "son 10 bar (<= kesim) ortalama TL hacim / önceki 60 bar ortalama TL hacim (TL hacim = Yahoo kapanış x hacim; satış tükenmesi)",
        "x11_dipten_gun": "kesim barına kadar 01.09 sonrası en düşük kapanıştan bu yana geçen bar sayısı (dip kesim barıysa 0)",
        "x12_col": "ÇÖL (1/0): COL_v1.col_olc(fiyat <= kesim) çöl kutusu döndürüyor (D13 dip2 + MIN_UZ / MAX_YUK kapıları) YA DA FON_IZI.fi_k24_tara "
                   "(fiyat <= kesim) 'kural' günü son 20 barda",
        "x13_bist100": "BIST 100 üyesi (1/0): KAP şirket sayfası 'Şirketin Dahil Olduğu Endeksler' listesinde tam 'BIST 100' (01.10 - 31.12.2026 dönemi; "
                       "21.09.2026'da ilan, dönem içinde değişmez; sayfa 13.11'de okunur; liste okunamazsa eksik). MSCI üyeliği ÖLÇÜLMEZ: <= 31.10 "
                       "tarihli ücretsiz liste yok",
        "x13b_bist500": "BIST 500 üyesi (1/0): aynı liste, tam 'BIST 500' (BIST 100 bu örneklemde tek değerli çıktığı için ön kayıttan önce eklendi)",
        "x14_ortak_alim": "EKİM ORTAK / YÖNETİCİ ALIMI (1/0): (a) KAP 'Pay Alım Satım Bildirimi' (ilgili kodlarda hisse; yayın 01.10 - 31.10; yayımlayan "
                          "portföy şirketi değil; metin Merrill Lynch / Bank of America değil) metin kuralıyla NET ALIŞ (gk_alim_yonu: MKK formunda 'X TL toplam "
                          "nominal tutarlı alış' toplamı > satış toplamı; 'adet alış işlemi'; ek PDF metni pdftotext); YA DA (b) Ekim yayınlı eşik "
                          "satırında artış (sonraki % > önceki %) ve sahip fon / portföy / banka / aracı kurum / yabancı kurum / ihraççının kendisi değil",
        "x15_ayni": "AYNİ ÖDEME ADAYI (1/0): Ziraat'in tasfiye ettiği PUSULA / ATLAS portföy fonlarının hissede son bilinen payı > 0: FON_IZI G "
                    "(bilinme <= 31.10, son ay, PUSULA / ATLAS fonları toplam pay >= %0,5) ya da eşik tablosunda PUSULA / ATLAS fonunun son 'sonraki %' > 0 "
                    "(Ziraat 15.10 duyurusu: bazı fonlarda bakiye hisse aktarımıyla ayni)",
    },
    "isaret_beklenen": "yön ön kayıtta beklenmez (iki yönlü test)",
    "test": {"rho": "Spearman (ortalama sıra; eşitlik düzeltmeli Pearson sıra korelasyonu)", "perm": 10000, "tohum": 20261113,
             "p": "iki yönlü permütasyon p = (1 + #{|rho*| >= |rho| - 1e-12}) / (1 + B); Y karıştırılır; eksik değerli hisse o değişkende dışarıda",
             "bh_q": 0.10, "bh_aile": "Y1 permütasyon p'leri, SINANAN bütün açıklayıcılar (Benjamini-Hochberg)",
             "aday": "ADAY EMARE <=> BH sonrası anlamlı (Y1, q = 0,10) VE rho_Y2 işareti rho_Y1 ile aynı (rho_Y2 != 0)",
             "sinanmaz": "geçerli değeri < 20 hisse, tek değerli ya da ikili değişkende küçük grup < 5 hisse -> SINANMAZ (BH ailesine girmez, nedeni yazılır)",
             "yari_fark": "üst yarı / alt yarı farkı = medyan Y1 (X >= medyan X) - medyan Y1 (X < medyan X); ikili X'te medyan Y1 (X=1) - medyan Y1 (X=0); "
                          "medyan en küçük değere eşitse (sıfır yığılması) üst = X > medyan; Y2 için aynı (ortalama tavan sayısı farkı)"},
    "agac": {"hedef": "Y1 >= medyan(Y1) -> 1, değilse 0", "degisken": "SINANAN açıklayıcılar içinde |rho_Y1| en büyük 2 (her LOO katında eğitim "
             "kümesinde yeniden seçilir)", "derinlik": 2, "yaprak_min": 5, "bolme": "Gini; aday eşik = ardışık farklı değerlerin ortası",
             "eksik": "eğitim medyanıyla doldurulur", "loo": "64 kat: seçim + ağaç 63 hissede, tahmin dışarıdaki 1 hissede; LOO doğruluk ve taban (%50 civarı)",
             "not": "YALNIZ AÇIKLAMA; ağaç kural değildir"},
    "col4": {"hisseler": ["TEHOL", "KTLEV", "DSTKF", "BINBN"],
             "T5": "fon payı ilk %5 tarihi = en erken: (a) FON_IZI.fi_k25_pay_tablo'da pay >= 0,05 olan ilk rapor ayının İLK günü (pay o ay sonunda "
                   ">= %5; alış ay içinde olabilir); (b) KAP geçmişinde (2024-01-01 - 2026-08-31) yayımlayanı portföy yönetim şirketi olan 'Pay Alım "
                   "Satım Bildirimi'nde (ilgili kodlarda hisse) mevzuat alıntısı dışında '%5' ardından 'ulaş' / 'aşmış' / 'aşarak' / 'üzerine' geçiyorsa (yukarı "
                   "geçiş) metindeki ilk işlem tarihi (yoksa yayın günü)",
             "pencere": 120, "pencere_tanim": "T5'ten ÖNCEKİ 120 işlem günü (kendi barları, T5 hariç)",
             "olcu": "her gün t: COL_v1.col_olc(fiyat <= t) çöl kutusu (tespit) ve GECER; AL kırılımı = col_olc(fiyat <= t-1) kutusu var ve C_t > "
                     "tavan x COL_v1.AL_PAY; K24 = FON_IZI.fi_k24_tara(fiyat < T5) 'kural' günleri",
             "not": "Ç97 (fon girmeyen eşlerde çöl sıklığı: ilişkisiz) tekrar edilmez; yalnız 4 hisse için tarih tablosu (BİLGİ)"},
    "sinir": "n = 64 tek kesit (tek olay: 2-13 Kasım dönüşü; hisseler aynı günlerde ortak piyasa hareketine maruz, bağımsız değil); permütasyon p "
             "bağımsızlık varsayar; 18+ açıklayıcı: BH'ye rağmen şans bulgusu olabilir; eşik tabloları yalnız %3 / %5 sınır geçişlerini gösterir; "
             "serbest fonlar KAP fon raporlarında eksik; açıklama, kural değil",
}


class GkHata(RuntimeError):
    """GENIS_KESIT'e özgü durdurucu hata (veri yok, ön kayıt yok / değişmiş / git'e işlenmemiş, mühür / X / kod sha tutmuyor, geleceğe bakma)."""


# ---------------------------------------------------------------- 0) YARDIMCILAR
def _gk_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _gk_yol(ad: str, kl: Optional[str] = None) -> str:
    if ad in ("X", "kanit", "Y"):
        return os.path.join(GK_YOL["is"], GK_DOSYA[ad])
    return os.path.join(kl or GK_YOL["cikti"], GK_DOSYA.get(ad, ad))


def _gk_yaz(yol: str, metin: str) -> str:
    if _GK_EPOSTA.search(metin):
        raise GkHata(f"{os.path.basename(yol)}: metinde e-posta biçimli parça var; yazılmadı")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _gk_json(yol: str, obj: Any) -> str:
    return _gk_yaz(yol, json.dumps(TS._ts_kayit(obj), ensure_ascii=False, indent=1, sort_keys=True, default=str))


def _gk_json_oku(yol: str) -> Any:
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as ex:
        raise GkHata(f"{yol} okunamadı ({type(ex).__name__}: {ex})") from ex


def gk_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or GK_ESIK, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")).hexdigest()


def gk_kod_sha(yol: Optional[str] = None) -> str:
    return TS.ts_sha_dosya(yol or os.path.join(KOK_GK, "GENIS_KESIT.py"))


def _gk_tr(s: Any) -> str:
    """Türkçe harfleri sadeleştir, büyük harf, noktalama -> boşluk."""
    t = str(s).translate(str.maketrans("ÇĞİÖŞÜçğıöşüÂâÎîÛû", "CGIOSUcgiosuAaIiUu")).upper()
    return re.sub(r"\s+", " ", re.sub(r"[^A-Z0-9 ]", " ", t)).strip()


_GK_SIRKET_EK = re.compile(r"\b(A S|AS|ANONIM SIRKETI|ANONIM|SIRKETI|SANAYI|VE|TICARET|SAN|TIC|LTD|STI)\b")


def _gk_ad(s: Any) -> str:
    """Şirket adı eşleme anahtarı: sade harf, şirket türü ekleri atılır."""
    return re.sub(r"\s+", " ", _GK_SIRKET_EK.sub(" ", _gk_tr(s))).strip()


def _gk_yuzde(s: Any) -> float:
    """'7,05%' / '49,814%' / '0,00%' -> 7.05 (yüzde puan); okunamazsa NaN."""
    m = re.search(r"(-?\d+(?:[.,]\d+)?)\s*%", str(s))
    if not m:
        return np.nan
    return float(m.group(1).replace(",", "."))


def _gk_kodlar(*xs: Any) -> List[str]:
    out: List[str] = []
    for x in xs:
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            continue
        out += [k.strip().upper() for k in str(x).split(",") if k.strip()]
    return out


def gk_kesim_ts(E: Optional[Dict[str, Any]] = None) -> pd.Timestamp:
    """Bilgi kesimi: 31.10.2026 23:59:59."""
    return pd.Timestamp((E or GK_ESIK)["kesim"]) + pd.Timedelta(hours=23, minutes=59, seconds=59)


def gk_ileri_denetim(ad: str, tarihler: Any, E: Optional[Dict[str, Any]] = None) -> None:
    """GELECEĞE BAKMA KAPISI: verilen tarihlerden biri kesimden sonraysa durur."""
    t = pd.to_datetime(pd.Series(list(tarihler) if not isinstance(tarihler, pd.Series) else tarihler), errors="coerce").dropna()
    if len(t) and t.max() > gk_kesim_ts(E):
        raise GkHata(f"GELECEĞE BAKMA: {ad} içinde kesimden ({(E or GK_ESIK)['kesim']}) sonraki bilgi var ({t.max()})")


# ---------------------------------------------------------------- 1) ÖRNEKLEM VE FİYAT
def gk_orneklem(yol: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    E = E or GK_ESIK; yol = yol or os.path.join(GK_YOL["tavan"], "canli_cokmus.csv")
    try:
        C = pd.read_csv(yol)
    except OSError as ex:
        raise GkHata(f"örneklem dosyası yok: {yol} ({ex})") from ex
    C = C[C["cokmus"].astype(str).str.lower() == "true"].copy()
    if len(C) != int(E["orneklem"]["n"]):
        raise GkHata(f"örneklem {len(C)} hisse, ön kayıtta {E['orneklem']['n']} (YANLIŞ EVREN)")
    return C.sort_values("sembol").reset_index(drop=True)


def gk_fiyat_kes(d: pd.DataFrame, kesim: pd.Timestamp) -> pd.DataFrame:
    """Fiyatı kesim gününde keser (gün sonu dahil); kesim sonrası bar kalırsa durur."""
    x = d[d.index <= kesim.normalize()]
    gk_ileri_denetim("fiyat", x.index)
    return x


def gk_ohlcv(d: pd.DataFrame) -> pd.DataFrame:
    """TAVAN_SERISI biçimi (o, h, l, c, v) -> COL_v1 / FON_IZI biçimi (Open, High, Low, Close, Volume)."""
    return pd.DataFrame({"Open": d.o, "High": d.h, "Low": d.l, "Close": d.c, "Volume": d.v}, index=d.index)


# ---------------------------------------------------------------- 2) KAP: LİSTE, METİN, EŞİK TABLOLARI
def gk_kap_liste(E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Eylül - 13 Kasım KAP listesi (kap2/tum.json) + Ağustos finansal rapor listesi (kap2/agustos_fr.json) + kesit/kap_gecmis haftalık listeler."""
    yollar = [os.path.join(GK_YOL["tavan"], "kap2", "tum.json"), os.path.join(GK_YOL["tavan"], "kap2", "agustos_fr.json")]
    yollar += sorted(glob.glob(os.path.join(GK_YOL["is"], "kap_gecmis", "*.json")))
    parca = []
    for y in yollar:
        try:
            J = _gk_json_oku(y)
        except GkHata as ex:
            if y == yollar[0]:
                raise
            gklog.warning("%s", ex); continue
        if isinstance(J, list) and J:
            parca.append(pd.DataFrame(J))
    if not parca:
        raise GkHata("KAP listesi boş")
    L = pd.concat(parca, ignore_index=True).drop_duplicates("disclosureIndex")
    L["t"] = pd.to_datetime(L.publishDate, format="%d.%m.%Y %H:%M:%S", errors="coerce")
    L["own"] = [_gk_kodlar(a) for a in L.stockCodes]
    L["kod"] = [_gk_kodlar(a, b) for a, b in zip(L.stockCodes, L.relatedStocks)]
    for c in ("subject", "summary", "kapTitle"):
        L[c] = L[c].fillna("").astype(str)
    return L.sort_values("t").reset_index(drop=True)


def _gk_html_metin(t: str) -> str:
    s = re.sub(r"<script.*?</script>", "", t, flags=re.S); s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    s = re.sub(r"<(br|/p|/tr|/div|/li|/h\d)[^>]*>", "\n", s); s = re.sub(r"<t[dh][^>]*>", " | ", s)
    s = re.sub(r"<[^>]+>", " ", s); s = _html.unescape(s); s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s)


def _gk_istek(url: str, bekle: float = 0.8, deneme: int = 4, ikili: bool = False) -> Optional[Any]:
    """Yalnız kap.org.tr (GET). Başarısızsa None."""
    if not url.startswith(_GK_KAP):
        raise GkHata(f"izin dışı adres: {url}")
    import requests  # noqa: WPS433
    for i in range(deneme):
        try:
            r = requests.get(url, headers={"User-Agent": _GK_UA}, timeout=90)
            if r.status_code == 200:
                time.sleep(bekle)
                return r.content if ikili else r.text
            gklog.warning("HTTP %s %s", r.status_code, url)
        except Exception as ex:  # noqa: BLE001  (ağ hatası türleri çok; hepsi yeniden denenir)
            gklog.warning("ağ hatası %s (%s)", url, type(ex).__name__)
        time.sleep(3 * (i + 1))
    return None


def gk_metin(idx: int, ag: bool = False, ekler: bool = False) -> Optional[str]:
    """Bildirim metni: önce mevcut önbellekler (kap2/txt, raw/metin, kesit/metin), yoksa ag=True ise KAP'tan indirir (+ PDF ekleri pdftotext)."""
    for y in (os.path.join(GK_YOL["is"], "metin", f"{idx}.txt"), os.path.join(GK_YOL["tavan"], "kap2", "txt", f"{idx}.txt"),
              os.path.join(GK_YOL["tavan"], "raw", "metin", f"{idx}.txt")):
        if os.path.exists(y):
            with open(y, encoding="utf-8", errors="replace") as f:
                t = f.read()
            if not ekler or "=== EK" in t or "EKLER:" not in t or not ag:
                return t
    if not ag:
        return None
    t = _gk_istek(f"{_GK_KAP}/tr/Bildirim/{idx}")
    if t is None:
        return None
    ek = sorted(set(re.findall(r"https://www\.kap\.org\.tr/tr/api/file/download/[0-9a-f]+", t)))
    s = _gk_html_metin(t) + (f"\nEKLER: {len(ek)}" if ek else "")
    if ekler:
        for j, u in enumerate(ek[:4]):
            b = _gk_istek(u, ikili=True)
            j0 = bytes(b).find(b"%PDF") if b else -1          # KAP eki Java dizisi sarmalında gelir: PDF başına kadar atılır
            if j0 < 0:
                continue
            b = bytes(b)[j0:]
            pdf = os.path.join(GK_YOL["is"], "metin", f"{idx}_{j}.pdf"); os.makedirs(os.path.dirname(pdf), exist_ok=True)
            with open(pdf, "wb") as f:
                f.write(b)
            try:
                r = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, timeout=120)
                s += f"\n=== EK {j} ===\n" + r.stdout
            except (OSError, subprocess.SubprocessError) as ex:
                gklog.warning("pdftotext %s (%s)", pdf, type(ex).__name__)
    y = os.path.join(GK_YOL["is"], "metin", f"{idx}.txt")
    _gk_yaz(y, _GK_EPOSTA.sub("[e-posta]", s))
    return s


def gk_esik_tablo(L: pd.DataFrame, yol: Optional[str] = None) -> pd.DataFrame:
    """esik_tum.csv (MKK eşik tabloları) -> tip A satırları (sahip, ihraççı, kod, önceki %, sonraki %, yayın zamanı). Fon payı tabloları (Rehber 9.8:
    ihraççı sütunu 3 harfli fon kodu) atılır. Kod sütunu varsa o, yoksa KAP unvan -> kod eşlemesi."""
    yol = yol or os.path.join(GK_YOL["tavan"], "kap2", "esik_tum.csv")
    try:
        R = pd.read_csv(yol, header=0, dtype=str)
    except OSError as ex:
        raise GkHata(f"eşik tablosu yok: {yol} ({ex})") from ex
    R.columns = [f"c{i}" for i in range(R.shape[1])]
    yay = L.drop_duplicates("disclosureIndex").set_index("disclosureIndex").t
    ad2kod: Dict[str, str] = {}
    for a, o in zip(L.kapTitle, L.own):
        uz = [k for k in o if len(k) >= 4]          # 'INFO, IYF' / 'SEK, SKBNK': pay kodu 4-6 harf
        if a and (len(o) == 1 or len(uz) == 1):
            ad2kod.setdefault(_gk_ad(a), o[0] if len(o) == 1 else uz[0])
    kod_re = re.compile(r"^[A-Z][A-Z0-9]{3,5}$"); fon_re = re.compile(r"^[A-Z0-9]{3}$")
    sat = []
    for r in R.itertuples(index=False):
        c = [("" if (isinstance(v, float) or v is None) else str(v).strip()) for v in r]
        if fon_re.match(c[3]):
            continue
        if kod_re.match(c[4]):
            kod = c[4]; nums = c[5:11]
        else:
            nums = c[4:10]; kod = ad2kod.get(_gk_ad(c[3]), "")
        try:
            idx = int(float(c[0]))
        except ValueError:
            continue
        sat.append({"idx": idx, "islem": pd.to_datetime(c[1], format="%d/%m/%Y", errors="coerce"), "sahip": c[2], "ihracci": c[3], "kod": kod,
                    "p0": _gk_yuzde(nums[2]), "p1": _gk_yuzde(nums[3]), "yay": yay.get(idx, pd.NaT)})
    T = pd.DataFrame(sat)
    eksik = T[T.kod == ""].ihracci.unique()
    if len(eksik):
        gklog.info("eşik: %d ihraççı adı koda eşlenemedi (örnek: %s)", len(eksik), "; ".join(map(str, eksik[:5])))
    return T


def gk_tasfiye_fonu(sahip: str) -> bool:
    """Sahip, tasfiye kapsamındaki portföy şirketlerinden birinin FONU mu (portföy şirketinin kendisi ya da aracı kurum değil)?"""
    import COL_v1 as CV  # noqa: WPS433
    s = _gk_tr(sahip)
    return bool(re.search(r"\bFON(U)?\b", s)) and any(_gk_tr(p) in s for p in CV.FON_TASFIYE)


def gk_ziraat_fonu(sahip: str) -> bool:
    s = _gk_tr(sahip)
    return bool(re.search(r"\bFON(U)?\b", s)) and ("PUSULA PORTFOY" in s or "ATLAS PORTFOY" in s)


_GK_KURUM = re.compile(r"\b(FON|FONU|PORTFOY|BANK|BANKASI|BANKA|SECURITIES|MENKUL|YATIRIM BANKASI|INTERNATIONAL|LIMITED|LTD|PLC|INC|LLC|"
                       r"MERRILL|EMEKLILIK|SIGORTA|TAKASBANK|KATILIM)\b")


def gk_ortak_mi(sahip: str, ihracci: str) -> bool:
    """Eşik satırı sahibi 'ortak / yönetici' sayılır mı: fon, portföy, banka, aracı kurum, yabancı kurum, sigorta değil ve ihraççının kendisi değil."""
    s = _gk_tr(sahip)
    return not _GK_KURUM.search(s) and _gk_ad(sahip) != _gk_ad(ihracci)


# ---------------------------------------------------------------- 3) AÇIKLAYICILAR
_GK_LEKE = re.compile(r"kayy[ıiu]m|TMSF|Tasarruf Mevduat[ıi] Sigorta|tutuklan|tutuklama|g[öo]zalt[ıi]", re.I)
_GK_OLUMSUZ = re.compile(r"bulunmama|bulunmamakta|yoktur|olmam[ıi][sş]|al[ıi]nmam[ıi][sş]|s[öo]z konusu de[ğg]il|ilgisi|atanmam[ıi][sş]", re.I)


def gk_leke_kap_metin(t: str) -> List[str]:
    """Metinde olumsuzlanmamış leke cümleleri (kayyım, TMSF, tutuklama, gözaltı)."""
    out = []
    for c in re.split(r"(?<=[.!?\n])\s+", t or ""):
        if _GK_LEKE.search(c) and not _GK_OLUMSUZ.search(c):
            out.append(re.sub(r"\s+", " ", c.strip())[:240])
    return out


def gk_spk_bulten(L: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """SPK bülten metinleri (kap2/spk/<idx>_<no>.txt) + yayın zamanı; yalnız yayın <= kesim olanlar döner."""
    yay = L.drop_duplicates("disclosureIndex").set_index("disclosureIndex").t; out = []
    for y in sorted(glob.glob(os.path.join(GK_YOL["tavan"], "kap2", "spk", "*.txt"))):
        m = re.match(r"(\d+)_(\d{4}-\d+)\.txt$", os.path.basename(y))
        if not m:
            continue
        t = yay.get(int(m.group(1)), pd.NaT)
        if pd.isna(t) or t > gk_kesim_ts(E):
            continue
        with open(y, encoding="utf-8", errors="replace") as f:
            out.append({"no": m.group(2), "idx": int(m.group(1)), "t": t, "satir": f.read().splitlines()})
    return out


def gk_spk_leke(kod: str, B: List[Dict[str, Any]], once: int = 3, sonra: int = 6) -> List[str]:
    anah = re.compile(r"su[çc] duyuru|i[şs]lem yasa[ğg]|107/1|106/1", re.I)
    kre = re.compile(rf"\({re.escape(kod)}\)|\b{re.escape(kod)} Pay Piyasas")
    out = []
    for b in B:
        S = b["satir"]
        for i, s in enumerate(S):
            if kre.search(s) and any(anah.search(x) for x in S[max(0, i - once):i + sonra + 1]):
                out.append(f"SPK {b['no']} ({b['t'].date()})"); break
    return out


def gk_alim_yonu(t: str) -> str:
    """Pay alım satım bildirimi metninden net yön: 'alis' / 'satis' / 'belirsiz'. Önce 'net ... satın alınmıştır / satılmıştır' kalıbı, sonra tablo
    sözcükleri (Alış / Satış; 'alım satım' / 'alım/satım' başlık kalıpları sayılmaz)."""
    s = re.sub(r"\s+", " ", t or "")
    if re.search(r"net [\d.,]+ (adet )?pay[ı]? satın al", s, re.I):
        return "alis"
    if re.search(r"net [\d.,]+ (adet )?pay[ı]? sat[ıi]lm", s, re.I):
        return "satis"
    def tutar(x: str) -> float:
        x = x.strip().rstrip(",.")
        if re.search(r",\d{1,2}$", x):
            x = x.rsplit(",", 1)[0]
        try:
            return float(re.sub(r"[.,]", "", x))
        except ValueError:
            return 0.0
    al = [tutar(m) for m in re.findall(r"([\d.,]+) (?:TL )?toplam nominal tutarl[ıi] al[ıi][şs]", s, re.I)]
    st = [tutar(m) for m in re.findall(r"([\d.,]+) (?:TL )?toplam nominal tutarl[ıi] sat[ıi][şs]", s, re.I)]
    if al or st:                                           # MKK formu: 'X TL toplam nominal tutarlı alış ... Y TL ... satış işlemi'
        return "alis" if sum(al) > sum(st) else ("satis" if sum(st) > sum(al) else "belirsiz")
    if re.search(r"adet al[ıi][şs] i[şs]lemi", s, re.I) and not re.search(r"adet sat[ıi][şs] i[şs]lemi", s, re.I):
        return "alis"
    if re.search(r"adet sat[ıi][şs] i[şs]lemi", s, re.I) and not re.search(r"adet al[ıi][şs] i[şs]lemi", s, re.I):
        return "satis"
    s2 = re.sub(r"al[ıi][mş]\s*[/-]?\s*sat[ıi][mş]", " ", s, flags=re.I)
    a = len(re.findall(r"\b(al[ıi][şs]|al[ıi]m[ıi]?|sat[ıi]n al[ıi]nm[ıi][şs]t[ıi]r|purchase|buy)\b", s2, re.I))
    b = len(re.findall(r"\b(sat[ıi][şs][ıi]?|sat[ıi]m[ıi]?|sat[ıi]lm[ıi][şs]t[ıi]r|sale|sell)\b", s2, re.I))
    return "alis" if a > b else ("satis" if b > a else "belirsiz")


def gk_geri_alim_program(ozet: str) -> bool:
    """Geri alım bildirimi özeti yalnız program ilanı / kararı mı (işlem bildirimi değil)?"""
    o = _gk_tr(ozet)
    return "PROGRAM" in o and not re.search(r"ISLEM|GERCEKLES|KAPSAMINDA|TARIHLI", o)


def gk_fr_ozkaynak(t: str) -> Optional[float]:
    """KAP finansal rapor sayfa metninden cari dönem özkaynak (TL). Önce 'Ana Ortaklığa Ait Özkaynaklar', yoksa 'Toplam Özkaynaklar'."""
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", t or "", flags=re.S)
    s = _html.unescape(re.sub(r"¦[\s¦]*", "¦", re.sub(r"<[^>]+>", "¦", s)))
    bm = re.search(r"Sunum Para Birimi¦\s*([^¦]{1,20})¦", s)
    birim = _gk_tr(bm.group(1)) if bm else "TL"
    kat = 1e6 if re.search(r"1 ?000 ?000|MILYON", birim) else (1e3 if re.search(r"1 ?000|BIN", birim) else 1.0)
    for lab in ("Ana Ortaklığa Ait Özkaynaklar", "Toplam Özkaynaklar", "TOPLAM ÖZKAYNAKLAR", "ÖZKAYNAKLAR"):
        m = re.search(r"¦" + re.escape(lab) + r"¦((?:[^¦]*¦){1,4})", s)
        if not m:
            continue
        for h in m.group(1).split("¦")[:4]:        # dipnot (kısa sayı) / İngilizce etiket atlanır; ilk TUTAR (>= 1.000 ya da binlik ayraçlı)
            h = h.strip()
            if re.fullmatch(r"-?\d{1,3}(?:\.\d{3})+|-?\d{4,}", h):
                return float(h.replace(".", "")) * kat
    return None


def gk_sirket_sayfa(kod: str, L: pd.DataFrame, ag: bool = False) -> Optional[str]:
    """KAP şirket özet sayfası (önbellek kesit/sirket/<kod>.html). Bağlantı hissenin kendi bir bildirim sayfasından bulunur."""
    y = os.path.join(GK_YOL["is"], "sirket", f"{kod}.html")
    if os.path.exists(y):
        with open(y, encoding="utf-8", errors="replace") as f:
            return f.read()
    if not ag:
        return None
    own = L[L.own.map(lambda o: kod in o)].assign(tek=lambda z: z.own.map(len) == 1).sort_values(["tek", "t"], ascending=False)
    denenen: set = set()
    for idx in own.disclosureIndex.head(8):
        t = _gk_istek(f"{_GK_KAP}/tr/Bildirim/{int(idx)}")
        for m in re.finditer(r"sirket-bilgileri/ozet/(\d+-[a-z0-9-]+)", t or ""):
            if m.group(1) in denenen:
                continue
            denenen.add(m.group(1))
            p = _gk_istek(f"{_GK_KAP}/tr/sirket-bilgileri/ozet/{m.group(1)}")
            if p and len(re.findall(rf"\b{re.escape(kod)}\b", p)) >= 3:   # sayfa bu hissenin mi (kod en az 3 kez)
                os.makedirs(os.path.dirname(y), exist_ok=True)
                with open(y, "w", encoding="utf-8") as f:
                    f.write(p)
                return p
    gklog.warning("%s şirket sayfası bulunamadı", kod)
    return None


def gk_endeksler(p: Optional[str]) -> Optional[List[str]]:
    if not p:
        return None
    i = p.find("Şirketin Dahil Olduğu Endeksler")
    if i < 0:
        return None
    ad = re.findall(r'children\\?":\\?"(BIST[^"\\]{1,40})\\?"', p[i:i + 4000])
    return sorted(set(ad)) or None          # boş liste = okunamadı (her pay en az BIST TÜM'dedir)


def gk_x_tablo(C: pd.DataFrame, S: Dict[str, pd.DataFrame], L: pd.DataFrame, T: pd.DataFrame, E: Optional[Dict[str, Any]] = None,
               ag: bool = False) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Açıklayıcı tablosu (64 hisse) + kanıt sözlüğü. Yalnız <= kesim bilgisi; her kaynak gk_ileri_denetim'den geçer."""
    E = E or GK_ESIK; kes = gk_kesim_ts(E); kesg = kes.normalize()
    import COL_v1 as CV  # noqa: WPS433
    import FON_IZI as FI  # noqa: WPS433
    Lk = L[L.t <= kes]; gk_ileri_denetim("KAP listesi", Lk.t, E)
    Tk = T[T.yay <= kes]; gk_ileri_denetim("eşik tablosu", Tk.yay, E)
    B = gk_spk_bulten(L, E)
    dol = pd.read_pickle(os.path.join(GK_YOL["veri"], "dol.pkl")).set_index("kod")
    tem = pd.read_csv(os.path.join(KOK_GK, "temel_duz.csv"), parse_dates=["aciklama"])
    tem = tem[tem.aciklama <= kes]; gk_ileri_denetim("temel_duz", tem.aciklama, E)
    G = pd.read_pickle(os.path.join(GK_YOL["veri"], "G.pkl")); oran = pd.read_pickle(os.path.join(GK_YOL["veri"], "oran.pkl"))
    G = G[pd.to_datetime(G.bilinme) <= kes]; gk_ileri_denetim("FON_IZI G", G.bilinme, E)
    Gz = G[G.sirket.map(lambda s: _gk_tr(s) in ("PUSULA", "ATLAS"))]
    Mz = FI.fi_k25_pay_tablo(Gz, oran, dol.reset_index()) if len(Gz) else pd.DataFrame(columns=["kod", "ay", "pay"])
    mkk_yasak = Lk[Lk.subject.str.contains("SPK İşlem Yasağı Nedeniyle Pay", na=False)]
    sat, kanit = [], {}
    for r in C.itertuples(index=False):
        s = r.sembol; K: Dict[str, Any] = {}; x: Dict[str, Any] = {"sembol": s}
        d = S.get(s)
        if d is None or not len(d):
            raise GkHata(f"{s}: fiyat yok")
        dk = gk_fiyat_kes(d, kes); k = len(dk) - 1
        if k < 20 or dk.index[-1] < kesg - pd.Timedelta(days=7):
            gklog.warning("%s: kesimde fiyat yok / kısa (%s)", s, dk.index[-1] if len(dk) else None)
        c = dk.c.to_numpy(float); car = dk["carpan"].to_numpy(float); v = dk.v.to_numpy(float)
        K["kesim_bar"] = str(dk.index[-1].date())
        x["x01_tepe250"] = float(c[-1] / np.max(c[-250:]) - 1.0) if len(c) >= 20 else np.nan
        x["x02_log_fiyat"] = float(np.log10(c[-1] * car[-1]))
        fp = r.fon_pay_kriz_oncesi
        x["x03_fon_kriz"] = float(fp) if pd.notna(fp) else 0.0
        # tasfiye fonu kalan payı / satış bitti / azalış sayısı / ortak alımı (eşik tabloları)
        th = Tk[Tk.kod == s].sort_values(["yay", "idx"])
        tf = th[th.sahip.map(gk_tasfiye_fonu).astype(bool)]
        son = tf.groupby("sahip").tail(1)
        x["x04_tasfiye_kalan"] = float(son.p1.fillna(0).sum()) if len(son) else 0.0
        K["tasfiye_son"] = [f"{a} {b:.2f}% ({t.date()})" for a, b, t in zip(son.sahip, son.p1.fillna(0), son.yay)]
        iki = th[(th.yay >= pd.Timestamp("2026-10-17")) & (th.p1 < th.p0)]
        x["x04b_satis_bitti"] = 0 if len(iki) else 1
        az = th[(th.yay >= pd.Timestamp("2026-09-01")) & (th.p1 < th.p0)]
        x["x05_azalis_sayisi"] = int(len(az))
        ekim = th[(th.yay >= pd.Timestamp("2026-10-01")) & (th.p1 > th.p0)]
        ortak_esik = ekim[np.array([gk_ortak_mi(a, b) for a, b in zip(ekim.sahip, ekim.ihracci)], bool)] if len(ekim) else ekim
        K["ortak_esik"] = [f"{a} {p0:.2f}->{p1:.2f} ({t.date()})" for a, p0, p1, t in zip(ortak_esik.sahip, ortak_esik.p0, ortak_esik.p1, ortak_esik.yay)]
        # leke
        sp = gk_spk_leke(s, B)
        own = Lk[Lk.own.map(lambda o, s=s: s in o).astype(bool) & (Lk.t >= pd.Timestamp("2026-09-01"))]
        lk = []
        for q in own.itertuples(index=False):
            bas = f"{q.subject}. {q.summary}."
            hit = gk_leke_kap_metin(bas)
            if not hit and q.subject.startswith("Özel Durum"):
                hit = gk_leke_kap_metin(gk_metin(int(q.disclosureIndex), ag=ag) or "")
            if hit:
                lk.append(f"KAP {int(q.disclosureIndex)} ({q.t.date()}): {hit[0][:160]}")
        x["x06_leke"] = int(bool(sp or lk)); K["leke"] = sp + lk
        x["x06b_mkk_yasak"] = int(bool(mkk_yasak.kod.map(lambda o, s=s: s in o).any()))
        # geri alım
        ga = own[own.subject == "Payların Geri Alınmasına İlişkin Bildirim"]
        prog = ga.summary.map(gk_geri_alim_program)
        x["x07_geri_alim"] = int(len(ga) > 0); x["x07b_geri_alim_sayi"] = int((~prog).sum()) if len(ga) else 0
        K["geri_alim"] = [f"{int(i)} {t.date()} {u[:60]}" for i, t, u in zip(ga.disclosureIndex, ga.t, ga.summary)][:12]
        # PD/DD
        pd_ = float(dol.sermaye_lot.get(s, np.nan)) * float(c[-1] * car[-1])
        tt = tem[tem.sembol == s].sort_values("aciklama")
        oz, ozk = np.nan, ""
        if len(tt) and pd.notna(tt.ozkaynak.iloc[-1]):
            oz, ozk = float(tt.ozkaynak.iloc[-1]), f"temel_duz {tt.donem.iloc[-1]} ({tt.aciklama.iloc[-1].date()})"
        else:
            fr = Lk[(Lk.subject == "Finansal Rapor") & Lk.own.map(lambda o, s=s: s in o)].sort_values("t")
            for q in fr.iloc[::-1].head(2).itertuples(index=False):      # yalnız en son iki rapor
                y = os.path.join(GK_YOL["is"], "fr", f"{int(q.disclosureIndex)}.html")
                h = None
                if os.path.exists(y):
                    with open(y, encoding="utf-8", errors="replace") as f:
                        h = f.read()
                elif ag:
                    h = _gk_istek(f"{_GK_KAP}/tr/Bildirim/{int(q.disclosureIndex)}")
                    if h:
                        os.makedirs(os.path.dirname(y), exist_ok=True)
                        with open(y, "w", encoding="utf-8") as f:
                            f.write(h)
                o_ = gk_fr_ozkaynak(h) if h else None
                if o_ is not None:
                    oz, ozk = o_, f"KAP FR {int(q.disclosureIndex)} ({q.t.date()})"; break
        x["x08_pddd"] = (1e6 if oz <= 0 else pd_ / oz) if np.isfinite(oz) and np.isfinite(pd_) else np.nan
        K["ozkaynak"] = f"{oz:.4g} TL, {ozk}" if np.isfinite(oz) else "bulunamadı"
        x["x09_halka_aciklik"] = float(dol.hao.get(s, np.nan))
        tl = c * v
        x["x10_hacim_oran"] = float(np.mean(tl[-10:]) / np.mean(tl[-70:-10])) if len(tl) >= 70 and np.mean(tl[-70:-10]) > 0 else np.nan
        e9 = dk.loc["2026-09-01":]
        x["x11_dipten_gun"] = int(len(e9) - 1 - int(np.argmin(e9.c.to_numpy(float)))) if len(e9) else np.nan
        # çöl (COL_v1 D13 + K24) — fiyat <= kesim
        o = gk_ohlcv(dk)
        try:
            co = CV.col_olc(o)
        except Exception as ex:  # noqa: BLE001  (COL_v1 iç hataları: ölçülemez sayılır, loglanır)
            gklog.warning("%s col_olc (%s)", s, type(ex).__name__); co = None
        try:
            k24 = FI.fi_k24_tara(o)
            k24g = [t for t in (k24[k24.kural].tarih if len(k24) else []) if t >= dk.index[max(0, k - 19)]]
        except Exception as ex:  # noqa: BLE001
            gklog.warning("%s K24 (%s)", s, type(ex).__name__); k24g = []
        x["x12_col"] = int(bool(co) or bool(k24g)); K["col"] = {"col_olc": bool(co), "k24": [str(t.date()) for t in k24g]}
        # BIST 100
        en = gk_endeksler(gk_sirket_sayfa(s, L, ag=ag))
        x["x13_bist100"] = (int("BIST 100" in en) if en is not None else np.nan); K["endeks"] = en
        x["x13b_bist500"] = (int("BIST 500" in en) if en is not None else np.nan)
        # Ekim ortak / yönetici alımı (KAP bildirimi + eşik)
        pb = Lk[(Lk.subject == "Pay Alım Satım Bildirimi") & Lk.kod.map(lambda o, s=s: s in o) & (Lk.t >= pd.Timestamp("2026-10-01"))
                & ~Lk.kapTitle.str.contains("PORTFÖY", na=False)]
        yon = []
        for q in pb.itertuples(index=False):
            mt = gk_metin(int(q.disclosureIndex), ag=ag, ekler=True) or ""
            if re.search(r"Merrill Lynch|Bank of America|BofA", mt, re.I):
                yon.append((int(q.disclosureIndex), "yabanci")); continue
            yon.append((int(q.disclosureIndex), gk_alim_yonu(mt.split("Açıklamalar", 1)[-1])))
        K["ortak_kap"] = [f"{i} {y}" for i, y in yon]
        x["x14_ortak_alim"] = int(any(y == "alis" for _, y in yon) or len(ortak_esik) > 0)
        # ayni ödeme adayı (Pusula / Atlas)
        mz = Mz[Mz.kod == s].sort_values("ay") if len(Mz) else Mz
        g_ok = bool(len(mz) and float(mz.pay.iloc[-1]) >= 0.005)
        zf = th[th.sahip.map(gk_ziraat_fonu).astype(bool)].groupby("sahip").tail(1)
        e_ok = bool(len(zf) and (zf.p1.fillna(0) > 0).any())
        x["x15_ayni"] = int(g_ok or e_ok)
        K["ayni"] = {"G_son": (f"{float(mz.pay.iloc[-1]):.4f} ({int(mz.ay.iloc[-1]) // 12}-{int(mz.ay.iloc[-1]) % 12 + 1:02d})" if len(mz) else None),
                     "esik": [f"{a} {b:.2f}%" for a, b in zip(zf.sahip, zf.p1.fillna(0))]}
        sat.append(x); kanit[s] = K
    X = pd.DataFrame(sat)
    return X, kanit


# ---------------------------------------------------------------- 4) SONUÇ DEĞİŞKENLERİ
def gk_y_tablo(C: pd.DataFrame, S: Dict[str, pd.DataFrame], E: Optional[Dict[str, Any]] = None, simdi: Optional[_dt.datetime] = None) -> pd.DataFrame:
    E = E or GK_ESIK; kesg = gk_kesim_ts(E).normalize(); sat = []
    for s in C.sembol:
        d = S.get(s)
        if d is None or not len(d):
            sat.append({"sembol": s, "Y1": np.nan, "Y2": np.nan, "Y3": np.nan, "son_bar": None, "gun_ici": None}); continue
        X = TS.ts_tavan(d)
        c0 = d.c[d.index <= kesg]
        c1 = float(d.c.iloc[-1]); son = d.index[-1]
        nov = X.loc["2026-11-02":]
        sep = d.c.loc["2026-09-01":]
        sat.append({"sembol": s, "Y1": c1 / float(c0.iloc[-1]) if len(c0) else np.nan, "Y2": int(nov.tavan.sum()), "Y3": c1 / float(sep.min()),
                    "son_bar": str(son.date()), "gun_ici": bool(TS.ts_gun_ici(son, simdi)), "kesim_bar": str(c0.index[-1].date()) if len(c0) else None})
    return pd.DataFrame(sat)


# ---------------------------------------------------------------- 5) İSTATİSTİK
def gk_sira(a: np.ndarray) -> np.ndarray:
    """Ortalama sıra (eşitlikler ortalama alır)."""
    a = np.asarray(a, float); o = np.argsort(a, kind="mergesort"); r = np.empty(len(a)); r[o] = np.arange(1, len(a) + 1, dtype=float)
    _, inv, say = np.unique(a, return_inverse=True, return_counts=True)
    top = np.bincount(inv, weights=r)
    return top[inv] / say[inv]


def gk_spearman(x: Sequence[float], y: Sequence[float]) -> float:
    x = np.asarray(x, float); y = np.asarray(y, float); m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return np.nan
    rx, ry = gk_sira(x[m]), gk_sira(y[m])
    sx, sy = rx.std(), ry.std()
    if sx == 0 or sy == 0:
        return np.nan
    return float(np.mean((rx - rx.mean()) * (ry - ry.mean())) / (sx * sy))


def gk_perm_p(x: Sequence[float], y: Sequence[float], B: int, tohum: int) -> Tuple[float, float]:
    """İki yönlü permütasyon p (Y karıştırılır). Döner (rho, p)."""
    x = np.asarray(x, float); y = np.asarray(y, float); m = np.isfinite(x) & np.isfinite(y)
    rx, ry = gk_sira(x[m]), gk_sira(y[m]); n = len(rx)
    if n < 3 or rx.std() == 0 or ry.std() == 0:
        return np.nan, np.nan
    zx = (rx - rx.mean()) / rx.std(); zy = (ry - ry.mean()) / ry.std()
    rho = float(np.mean(zx * zy))
    rng = np.random.default_rng(tohum)
    P = np.argsort(rng.random((B, n)), axis=1)
    rp = (zy[P] @ zx) / n
    return rho, float((1 + np.sum(np.abs(rp) >= abs(rho) - 1e-12)) / (1 + B))


def gk_bh(p: Sequence[float], q: float) -> np.ndarray:
    """Benjamini-Hochberg: anlamlı mı (bool) ve düzeltilmiş q-değerleri döner (iki satır)."""
    p = np.asarray(p, float); n = len(p)
    if n == 0:
        return np.zeros((2, 0))
    o = np.argsort(p); ps = p[o]
    qv = np.minimum.accumulate((ps * n / np.arange(1, n + 1))[::-1])[::-1]
    qv = np.minimum(qv, 1.0)
    k = np.flatnonzero(ps <= q * np.arange(1, n + 1) / n)
    an = np.zeros(n, bool)
    if len(k):
        an[o[:k.max() + 1]] = True
    Q = np.empty(n); Q[o] = qv
    return np.vstack([an.astype(float), Q])


def gk_sinanir_mi(x: pd.Series, E: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
    E = E or GK_ESIK; v = pd.to_numeric(x, errors="coerce").dropna()
    if len(v) < 20:
        return False, f"geçerli değer {len(v)} < 20"
    u = v.unique()
    if len(u) < 2:
        return False, "tek değerli"
    if len(u) == 2:
        kucuk = int(v.value_counts().min())
        if kucuk < 5:
            return False, f"ikili, küçük grup {kucuk} < 5"
    return True, ""


def gk_yari_fark(x: pd.Series, y: pd.Series, f: Callable = np.median) -> float:
    x = pd.to_numeric(x, errors="coerce"); m = x.notna() & y.notna(); x, y = x[m], y[m]
    if not len(x):
        return np.nan
    if x.nunique() == 2:
        a, b = sorted(x.unique())
        return float(f(y[x == b]) - f(y[x == a]))
    med = x.median()
    u, a = (y[x > med], y[x <= med]) if x.min() == med else (y[x >= med], y[x < med])   # sıfır yığılmalı X: üst = X > medyan
    return float(f(u) - f(a)) if len(u) and len(a) else np.nan


def gk_istatistik(X: pd.DataFrame, Y: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    E = E or GK_ESIK; T = E["test"]; D = X.merge(Y, on="sembol"); sat = []
    for i, v in enumerate([c for c in X.columns if c.startswith("x")]):
        ok, neden = gk_sinanir_mi(D[v], E)
        r = {"degisken": v, "n": int(pd.to_numeric(D[v], errors="coerce").notna().sum()), "sinanir": ok, "neden": neden}
        if ok:
            r["rho_Y1"], r["p_Y1"] = gk_perm_p(D[v], D.Y1, T["perm"], T["tohum"] + i)
            r["rho_Y2"], r["p_Y2"] = gk_perm_p(D[v], D.Y2, T["perm"], T["tohum"] + 1000 + i)
            r["rho_Y3"] = gk_spearman(D[v], D.Y3)
            r["yari_Y1"] = gk_yari_fark(D[v], D.Y1); r["yari_Y2"] = gk_yari_fark(D[v], D.Y2, np.mean)
        else:
            r["rho_Y1"] = gk_spearman(D[v], D.Y1); r["rho_Y2"] = gk_spearman(D[v], D.Y2); r["rho_Y3"] = gk_spearman(D[v], D.Y3)
        sat.append(r)
    R = pd.DataFrame(sat)
    m = R.sinanir.astype(bool)
    R["q_Y1"] = np.nan; R["bh"] = False
    if m.any():
        B = gk_bh(R.loc[m, "p_Y1"].to_numpy(float), T["bh_q"])
        R.loc[m, "bh"] = B[0].astype(bool); R.loc[m, "q_Y1"] = B[1]
    R["aday"] = R.bh & (np.sign(R.rho_Y1) == np.sign(R.rho_Y2)) & (R.rho_Y2.fillna(0) != 0)
    return R


# ---------------------------------------------------------------- 6) DERİNLİK-2 AĞAÇ (açıklama, LOO)
def _gk_gini(y: np.ndarray) -> float:
    if not len(y):
        return 0.0
    p = y.mean()
    return 2 * p * (1 - p)


def _gk_en_iyi_bolme(A: np.ndarray, y: np.ndarray, yaprak: int) -> Optional[Tuple[int, float, float]]:
    en = None; n = len(y); g0 = _gk_gini(y)
    for j in range(A.shape[1]):
        u = np.unique(A[:, j])
        for t in (u[:-1] + u[1:]) / 2:
            L_ = A[:, j] <= t; nl = int(L_.sum())
            if nl < yaprak or n - nl < yaprak:
                continue
            g = (nl * _gk_gini(y[L_]) + (n - nl) * _gk_gini(y[~L_])) / n
            if g < g0 - 1e-12 and (en is None or g < en[2] - 1e-12):
                en = (j, float(t), g)
    return en


def gk_agac(A: np.ndarray, y: np.ndarray, derinlik: int = 2, yaprak: int = 5) -> Dict[str, Any]:
    y = np.asarray(y, int)
    cog = int(round(y.mean())) if len(y) else 0
    dugum: Dict[str, Any] = {"n": int(len(y)), "p1": float(y.mean()) if len(y) else np.nan, "tahmin": int(y.mean() >= 0.5) if len(y) else cog}
    if derinlik == 0 or len(y) < 2 * yaprak or len(np.unique(y)) < 2:
        return dugum
    b = _gk_en_iyi_bolme(A, y, yaprak)
    if b is None:
        return dugum
    j, t, _ = b; L_ = A[:, j] <= t
    dugum.update(j=j, esik=t, sol=gk_agac(A[L_], y[L_], derinlik - 1, yaprak), sag=gk_agac(A[~L_], y[~L_], derinlik - 1, yaprak))
    return dugum


def gk_agac_tahmin(d: Dict[str, Any], a: np.ndarray) -> int:
    while "j" in d:
        d = d["sol"] if a[d["j"]] <= d["esik"] else d["sag"]
    return int(d["tahmin"])


def gk_agac_metin(d: Dict[str, Any], adlar: List[str], girinti: str = "") -> List[str]:
    if "j" not in d:
        return [f"{girinti}-> {'GÜÇLÜ' if d['tahmin'] else 'ZAYIF'} (n {d['n']}, güçlü oranı {d['p1']:.0%})"]
    return ([f"{girinti}{adlar[d['j']]} <= {d['esik']:.4g}:"] + gk_agac_metin(d["sol"], adlar, girinti + "  ")
            + [f"{girinti}{adlar[d['j']]} > {d['esik']:.4g}:"] + gk_agac_metin(d["sag"], adlar, girinti + "  "))


def _gk_secim(D: pd.DataFrame, adlar: List[str], k: int = 2) -> List[str]:
    r = [(abs(gk_spearman(D[a], D.Y1)), a) for a in adlar]
    r = [(v, a) for v, a in r if np.isfinite(v)]
    return [a for _, a in sorted(r, key=lambda z: (-z[0], z[1]))[:k]]


def gk_agac_loo(X: pd.DataFrame, Y: pd.DataFrame, sinanan: List[str], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or GK_ESIK; Ag = E["agac"]; D = X.merge(Y, on="sembol").dropna(subset=["Y1"]).reset_index(drop=True)
    hedef = (D.Y1 >= D.Y1.median()).astype(int).to_numpy()

    def kur(Dt: pd.DataFrame, ht: np.ndarray) -> Tuple[List[str], Dict[str, Any], pd.Series]:
        sec = _gk_secim(Dt, sinanan, 2); med = Dt[sec].apply(pd.to_numeric, errors="coerce").median()
        A = Dt[sec].apply(pd.to_numeric, errors="coerce").fillna(med).to_numpy(float)
        return sec, gk_agac(A, ht, Ag["derinlik"], Ag["yaprak_min"]), med

    sec, tam, med = kur(D, hedef)
    A = D[sec].apply(pd.to_numeric, errors="coerce").fillna(med).to_numpy(float)
    ic = float(np.mean([gk_agac_tahmin(tam, a) == h for a, h in zip(A, hedef)]))
    dogru, secimler = [], []
    for i in range(len(D)):
        m = np.ones(len(D), bool); m[i] = False
        s_, t_, md = kur(D[m].reset_index(drop=True), hedef[m])
        a = pd.to_numeric(D.loc[i, s_], errors="coerce").fillna(md).to_numpy(float)
        dogru.append(gk_agac_tahmin(t_, a) == hedef[i]); secimler.append("+".join(s_))
    taban = float(max(hedef.mean(), 1 - hedef.mean()))
    return {"degiskenler": sec, "agac": tam, "metin": gk_agac_metin(tam, sec), "ic_dogruluk": ic, "loo_dogruluk": float(np.mean(dogru)),
            "taban": taban, "n": int(len(D)), "loo_secim": pd.Series(secimler).value_counts().head(5).to_dict(), "esik_Y1": float(D.Y1.median())}


# ---------------------------------------------------------------- 7) 4 HİSSE: FON %5 ÖNCESİ 120 GÜNDE ÇÖL
def gk_t5_fon_izi(kod: str) -> Optional[Dict[str, Any]]:
    import FON_IZI as FI  # noqa: WPS433
    G = pd.read_pickle(os.path.join(GK_YOL["veri"], "G.pkl")); oran = pd.read_pickle(os.path.join(GK_YOL["veri"], "oran.pkl"))
    dol = pd.read_pickle(os.path.join(GK_YOL["veri"], "dol.pkl"))
    M = FI.fi_k25_pay_tablo(G[G.kod == kod], oran, dol)
    w = M[M.pay >= 0.05].sort_values("ay")
    mx = M.sort_values("pay").tail(1)
    out = {"max_pay": float(mx.pay.iloc[0]) if len(mx) else None, "max_ay": (f"{int(mx.ay.iloc[0]) // 12}-{int(mx.ay.iloc[0]) % 12 + 1:02d}" if len(mx) else None)}
    if not len(w):
        return {**out, "T5": None}
    a = int(w.ay.iloc[0])
    return {**out, "T5": pd.Timestamp(year=a // 12, month=a % 12 + 1, day=1), "ay": f"{a // 12}-{a % 12 + 1:02d}", "pay": float(w.pay.iloc[0])}


def _gk_alintisiz(g: str) -> str:
    """Tırnak içindeki mevzuat alıntısı ve '%5, %10, ... %95' listesi atılmış metin."""
    g2 = re.sub(r"[\"“”].{0,600}?[\"“”]", " ", g or "", flags=re.S)
    return re.sub(r"%\s?5\s*,\s*%\s?10.{0,80}?%\s?95", " ", g2, flags=re.S)


def gk_esik5(g: str) -> bool:
    """Metin, payın %5 eşiğine ULAŞTIĞINI söylüyor mu? Tırnak içindeki mevzuat alıntısı ve '%5, %10, ... %95' listesi atılır."""
    g2 = _gk_alintisiz(g)
    return bool(re.search(r"%\s?5(?![\d,.])[^%\n]{0,100}?(ula[şs]|a[şs]m[ıi][şs]|a[şs]arak|[üu]zerine)", g2, re.I)
                or re.search(r"(ula[şs]|a[şs]m[ıi][şs])[^%\n]{0,60}%\s?5(?![\d,.])", g2, re.I))


def gk_t5_kap(kod: str, L: pd.DataFrame, ag: bool = False) -> Optional[Dict[str, Any]]:
    """KAP geçmişi: portföy şirketinin 'Pay Alım Satım Bildirimi' metninde '%5' + 'ulaş' -> ilk işlem tarihi (yoksa yayın)."""
    c = L[(L.subject == "Pay Alım Satım Bildirimi") & L.kapTitle.str.contains("PORTFÖY", na=False) & L.kod.map(lambda o: kod in o)
          & (L.t >= pd.Timestamp("2024-01-01")) & (L.t <= pd.Timestamp("2026-08-31 23:59:59"))].sort_values("t")
    for q in c.itertuples(index=False):
        t = gk_metin(int(q.disclosureIndex), ag=ag) or ""
        g = t.split("Açıklamalar", 1)[-1]
        if gk_esik5(g):
            m = re.search(r"(\d{2}[./]\d{2}[./]\d{4}) tarih", g)
            ti = pd.to_datetime(m.group(1).replace("/", "."), format="%d.%m.%Y", errors="coerce") if m else pd.NaT
            return {"T5": (ti if pd.notna(ti) else q.t.normalize()), "idx": int(q.disclosureIndex), "yayin": str(q.t), "sahip": q.kapTitle,
                    "parca": re.sub(r"\s+", " ", _gk_alintisiz(g)).split("uyarınca", 1)[-1][:260].strip()}
    return {"T5": None, "aday_bildirim": int(len(c))}


def gk_col4(S: Dict[str, pd.DataFrame], L: pd.DataFrame, E: Optional[Dict[str, Any]] = None, ag: bool = False) -> List[Dict[str, Any]]:
    E = E or GK_ESIK; C4 = E["col4"]; out = []
    import COL_v1 as CV  # noqa: WPS433
    import FON_IZI as FI  # noqa: WPS433
    for kod in C4["hisseler"]:
        a = gk_t5_fon_izi(kod) or {}; b = gk_t5_kap(kod, L, ag) or {}
        ad = [t for t in (a.get("T5"), b.get("T5")) if t is not None and pd.notna(t)]
        r: Dict[str, Any] = {"sembol": kod, "fon_izi": {k: (str(v.date()) if isinstance(v, pd.Timestamp) else v) for k, v in a.items()},
                             "kap": {k: (str(v.date()) if isinstance(v, pd.Timestamp) else v) for k, v in b.items()}}
        d = S.get(kod)
        if not ad or d is None:
            r["durum"] = "T5 yok (fon payı %5 bulunamadı)" if not ad else "fiyat yok"; out.append(r); continue
        T5 = min(ad); r["T5"] = str(T5.date()); r["T5_kaynak"] = "FON_IZI" if a.get("T5") is not None and T5 == a.get("T5") else "KAP"
        o = gk_ohlcv(d[d.index < T5]); w = o.index[-int(C4["pencere"]):]
        r["bar_once"] = int(len(o)); r["ilk_bar"] = str(d.index[0].date())
        kp = L[(L.subject == "Pay Alım Satım Bildirimi") & L.kapTitle.str.contains("PORTFÖY", na=False) & L.kod.map(lambda z: kod in z)]
        r["kap_ilk_portfoy_bildirimi"] = str(kp.t.min().date()) if len(kp) else None
        r["pencere"] = [str(w[0].date()), str(w[-1].date())] if len(w) else None
        tes, gec, al = [], [], []
        onceki = None
        for t in w:
            x = o[o.index <= t]
            try:
                co = CV.col_olc(x)
            except Exception as ex:  # noqa: BLE001
                gklog.warning("%s %s col_olc (%s)", kod, t.date(), type(ex).__name__); co = None
            if onceki and float(x.Close.iloc[-1]) > onceki["tavan"] * CV.AL_PAY:
                al.append(str(t.date()))
            if co:
                tes.append(str(t.date()))
                if co.get("GECER"):
                    gec.append(str(t.date()))
            onceki = co
        try:
            k24 = FI.fi_k24_tara(o)
            k24g = [str(t.date()) for t in (k24[k24.kural].tarih if len(k24) else []) if t >= w[0]]
        except Exception as ex:  # noqa: BLE001
            gklog.warning("%s K24 (%s)", kod, type(ex).__name__); k24g = []
        r.update(col_tespit_gun=len(tes), col_ilk=tes[0] if tes else None, col_son=tes[-1] if tes else None, col_gecer=gec[:10], al=al[:10],
                 k24=k24g, col_var=bool(tes or k24g))
        out.append(r)
    return out


# ---------------------------------------------------------------- 8) KOMUTLAR: TOPLA, X, ÖN KAYIT, KAPI, KOŞ
def gk_topla(E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """KAP'tan eksik parçalar (yalnız kap.org.tr): (1) 2024-01 - 2026-08 haftalık bildirim listesi (col4 T5 için), (2) gerekli metinler / ekler,
    (3) şirket sayfaları, (4) eksik özkaynak için finansal rapor sayfaları. Önbellek GK_YOL['is']."""
    E = E or GK_ESIK; import requests  # noqa: WPS433
    os.makedirs(os.path.join(GK_YOL["is"], "kap_gecmis"), exist_ok=True)
    s = requests.Session()
    s.headers.update({"User-Agent": _GK_UA, "Accept": "application/json, text/plain, */*", "Content-Type": "application/json;charset=UTF-8",
                      "Origin": _GK_KAP, "Referer": _GK_KAP + "/tr/bildirim-sorgu"})
    try:
        s.get(_GK_KAP + "/tr/bildirim-sorgu", timeout=60)
    except Exception as ex:  # noqa: BLE001
        gklog.warning("KAP açılış (%s)", type(ex).__name__)
    def sorgu(a: pd.Timestamp, b: pd.Timestamp) -> Optional[list]:
        for i in range(4):
            try:
                r = s.post(_GK_KAP + "/tr/api/disclosure/members/byCriteria",
                           data=json.dumps({"fromDate": str(a.date()), "toDate": str(b.date()), "mkkMemberOidList": [], "subjectList": []}), timeout=120)
                if r.status_code == 200:
                    time.sleep(0.8); return r.json()
            except Exception as ex:  # noqa: BLE001
                gklog.warning("liste %s (%s)", a.date(), type(ex).__name__)
            time.sleep(3 * (i + 1))
        return None

    d = pd.Timestamp("2024-01-01"); son = pd.Timestamp("2026-08-31"); say = {"hafta": 0, "gunluk": 0, "hata": 0, "kesik": 0}
    while d <= son:
        b = min(d + pd.Timedelta(days=6), son); y = os.path.join(GK_YOL["is"], "kap_gecmis", f"{d.date()}.json")
        J = _gk_json_oku(y) if os.path.exists(y) else None
        if J is None or (len(J) >= 2000 and not os.path.exists(y + ".gunluk")):
            J = sorgu(d, b)
            if J is not None and len(J) >= 2000:          # 2000 sınırı: günlük sorgularla tamamla
                J2: list = []
                for g in pd.date_range(d, b):
                    Jg = sorgu(g, g)
                    if Jg is None:
                        say["hata"] += 1; continue
                    if len(Jg) >= 2000:
                        say["kesik"] += 1; gklog.warning("%s günü 2000 sınırında (kesik)", g.date())
                    J2 += Jg; say["gunluk"] += 1
                J = J2
                with open(y + ".gunluk", "w", encoding="utf-8") as f:
                    f.write("1")
            if J is None:
                say["hata"] += 1
            else:
                with open(y, "w", encoding="utf-8") as f:
                    json.dump(J, f, ensure_ascii=False)
                say["hafta"] += 1
        d = b + pd.Timedelta(days=1)
    gklog.info("geçmiş liste: %s", say)
    L = gk_kap_liste(E); C = gk_orneklem(E=E)
    for kod in E["col4"]["hisseler"]:
        gk_t5_kap(kod, L, ag=True)
    S, _ = TS.ts_fiyatlar(GK_YOL["yahoo"], C.sembol.tolist())
    T = gk_esik_tablo(L)
    X, K = gk_x_tablo(C, S, L, T, E, ag=True)
    return {"say": say, "X_satir": len(X)}


def gk_x(E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Açıklayıcı tablosu (ağsız; önbellekten). X.csv + X_kanit.json yazar."""
    E = E or GK_ESIK
    C = gk_orneklem(E=E); L = gk_kap_liste(E); T = gk_esik_tablo(L)
    S, K = TS.ts_fiyatlar(GK_YOL["yahoo"], C.sembol.tolist())
    X, kanit = gk_x_tablo(C, S, L, T, E, ag=False)
    os.makedirs(GK_YOL["is"], exist_ok=True)
    X.to_csv(_gk_yol("X"), index=False, float_format="%.10g")
    _gk_json(_gk_yol("kanit"), kanit)
    gklog.info("X: %d hisse x %d açıklayıcı -> %s (sha %s)", len(X), X.shape[1] - 1, _gk_yol("X"), TS.ts_sha_dosya(_gk_yol("X"))[:12])
    return X, kanit


def gk_x_ozet(X: pd.DataFrame) -> List[str]:
    out = []
    for v in [c for c in X.columns if c.startswith("x")]:
        a = pd.to_numeric(X[v], errors="coerce"); ok, neden = gk_sinanir_mi(a)
        if a.dropna().nunique() <= 2:
            out.append(f"- {v}: n {a.notna().sum()}, 1 olan {int((a == 1).sum())}" + ("" if ok else f" -> SINANMAZ ({neden})"))
        else:
            out.append(f"- {v}: n {a.notna().sum()}, medyan {a.median():.4g}, min {a.min():.4g}, max {a.max():.4g}" + ("" if ok else f" -> SINANMAZ ({neden})"))
    return out


def gk_onkayit(kl: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    E = E or GK_ESIK; y = _gk_yol("onkayit", kl)
    if os.path.exists(y):
        raise GkHata(f"ön kayıt zaten var, üzerine yazılmaz: {y}")
    if not os.path.exists(_gk_yol("X")):
        raise GkHata("X.csv yok: önce `python GENIS_KESIT.py x`")
    X = pd.read_csv(_gk_yol("X"))
    veri = {ad: (TS.ts_sha_dosya(p) if os.path.exists(p) else None) for ad, p in (
        ("canli_cokmus.csv", os.path.join(GK_YOL["tavan"], "canli_cokmus.csv")), ("esik_tum.csv", os.path.join(GK_YOL["tavan"], "kap2", "esik_tum.csv")),
        ("tum.json", os.path.join(GK_YOL["tavan"], "kap2", "tum.json")), ("dol.pkl", os.path.join(GK_YOL["veri"], "dol.pkl")),
        ("G.pkl", os.path.join(GK_YOL["veri"], "G.pkl")))}
    metin = "\n".join([
        "# GENİŞ KESİT ÖN KAYDI (ölçümden önce)", "",
        f"{GK_SURUM}. Yazılma {_gk_simdi()}. Bu dosya git'e işlenmeden `python GENIS_KESIT.py kos` çalışmaz (mühür kapısı).", "",
        "## Soru", "",
        "Fon krizinde %80+ düşmüş 64 BIST hissesinde 31.10.2026'da BİLİNEN hangi özellik 1-13 Kasım dönüşünün büyüklüğünü önceden gösteriyordu? "
        "Kesit, n = 64, açıklayıcı (kural değil). Geleceğe bakma yok: her açıklayıcı yalnız <= 31.10.2026 bilgisiyle.", "",
        "## Tanımlar, test ve karar cümlesi (GK_ESIK, değişmez)", "",
        "```json", json.dumps(E, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
        "## Ölçümden önce yapılanlar (sonuç içermez)", "",
        "- Açıklayıcı tablosu X (yalnız <= 31.10 bilgisi; fiyat 30.10 barında kesildi, KAP yayın <= 31.10) ölçümden ÖNCE kuruldu ve sha256 ile "
        "donduruldu (aşağıda). Y1 / Y2 / Y3 hesaplanmadı, X ile Y arasında hiçbir ilişki bakılmadı.",
        "- Önceden görülen sonuç bilgisi (dürüst not): canli_cokmus.csv 13.11 sabah tablosunda 'dipten_kat' (Y3'e yakın) ve tavan sayıları vardı; "
        "örneklem seçimi için okundu. Tanımlar Cemal'in iş tanımındaki 15 maddeden birebir alındı; seçim sonuçla değişmedi.",
        "- X dağılımı (sınanabilirlik denetimi):", *gk_x_ozet(X), "",
        "## Bilinen sınırlar", "", E["sinir"], "",
        f"ESIK_SHA256: {gk_esik_sha(E)}",
        f"KOD_SHA256: {gk_kod_sha()}",
        f"X_SHA256: {TS.ts_sha_dosya(_gk_yol('X'))}",
        "VERI_SHA256: " + json.dumps(veri, sort_keys=True), ""])
    return _gk_yaz(y, metin)


def gk_onkayit_oku(yol: str) -> Dict[str, str]:
    try:
        with open(yol, encoding="utf-8") as f:
            t = f.read()
    except OSError as ex:
        raise GkHata(f"ön kayıt okunamadı: {ex}") from ex
    out = {}
    for k in ("ESIK_SHA256", "KOD_SHA256", "X_SHA256"):
        m = re.search(rf"^{k}: ([0-9a-f]{{64}})$", t, re.M)
        if not m:
            raise GkHata(f"ön kayıtta {k} yok")
        out[k] = m.group(1)
    return out


def gk_kapi(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ön kayıt kapısı: ön kayıt var + git'e işlenmiş ve değişmemiş + eşik mührü + X sha tutar + kod sha tutar (ya da sapma gerekçesi)."""
    E = E or GK_ESIK; y = _gk_yol("onkayit", kl)
    if not os.path.exists(y):
        raise GkHata("ön kayıt yok: önce `python GENIS_KESIT.py onkayit` ve commit + push")
    O = gk_onkayit_oku(y); out: Dict[str, Any] = {"onkayit": y}
    if git:
        try:
            out["onkayit_git"] = TS.ts_git_durum(y)
        except TS.TsHata as ex:
            raise GkHata(str(ex)) from ex
    if O["ESIK_SHA256"] != gk_esik_sha(E):
        raise GkHata("eşik mührü tutmuyor (GK_ESIK ön kayıttan sonra değişmiş)")
    if not os.path.exists(_gk_yol("X")) or TS.ts_sha_dosya(_gk_yol("X")) != O["X_SHA256"]:
        raise GkHata("X.csv ön kayıttaki sha256 ile aynı değil (açıklayıcılar ölçümden sonra değişmiş olamaz)")
    ks = gk_kod_sha(); out["kod_sha256"] = ks; out["kod_ayni"] = ks == O["KOD_SHA256"]
    if not out["kod_ayni"]:
        if not sapma:
            raise GkHata("GENIS_KESIT.py ön kayıttan sonra değişmiş: yalnız `--sapma GEREKCE` ile koşar (gerekçe sonuca yazılır)")
        out["sapma"] = sapma
    out["esik_sha256"] = O["ESIK_SHA256"]; out["X_sha256"] = O["X_SHA256"]
    return out


def gk_sonuc_indir(E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """64 hissenin güncel fiyatı Yahoo'dan ayrı klasöre (TAVAN_SERISI.ts_indir; 2026-08-01'den)."""
    C = gk_orneklem(E=E); simdi = _dt.datetime.now(_dt.timezone.utc)
    if simdi.date() == _dt.date(2026, 11, 13) and (simdi.hour, simdi.minute) < (15, 10):
        raise GkHata("13.11 seans kapanışı (15:10 UTC) gelmeden sonuç fiyatı indirilmez (ön kayıt: kapanışla ölçüm)")
    return TS.ts_indir(semboller=C.sembol.tolist(), klasor=GK_YOL["yahoo_son"], bas="2026-08-01", bit="2026-11-15")


def gk_kos(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or GK_ESIK
    Kp = gk_kapi(kl, git, sapma, E); t0 = _gk_simdi(); gklog.info("kapı geçti (mühür %s)", Kp["esik_sha256"][:12])
    C = gk_orneklem(E=E); X = pd.read_csv(_gk_yol("X"))
    if sorted(X.sembol) != sorted(C.sembol):
        raise GkHata("X hisseleri örneklemle aynı değil (YANLIŞ EVREN)")
    kl_son = GK_YOL["yahoo_son"] if os.path.isdir(GK_YOL["yahoo_son"]) else GK_YOL["yahoo"]
    Sy, Ky = TS.ts_fiyatlar(kl_son, C.sembol.tolist())
    # yahoo_son 2026-08-01'den başlar; Y3 (01.09 sonrası dip) ve Y2 (Kasım) için yeterli; kesim barı da içinde
    Y = gk_y_tablo(C, Sy, E)
    Y.to_csv(_gk_yol("Y"), index=False, float_format="%.10g")
    R = gk_istatistik(X, Y, E)
    sinanan = R[R.sinanir.astype(bool)].degisken.tolist()
    A = gk_agac_loo(X, Y, sinanan, E)
    L = gk_kap_liste(E); S, _ = TS.ts_fiyatlar(GK_YOL["yahoo"], E["col4"]["hisseler"])
    C4 = gk_col4(S, L, E, ag=False)
    sonuc = {"surum": GK_SURUM, "baslangic": t0, "bitis": _gk_simdi(), "kapi": Kp, "fiyat_kaynak": kl_son, "fiyat_son_tarih": Ky.get("son_tarih"),
             "gun_ici": bool(Y.gun_ici.fillna(False).any()), "Y": Y, "tablo": R, "agac": A, "col4": C4,
             "Y_ozet": {k: {"medyan": float(Y[k].median()), "min": float(Y[k].min()), "max": float(Y[k].max())} for k in ("Y1", "Y2", "Y3")}}
    _gk_json(_gk_yol("sonuc", kl), sonuc)
    _gk_yaz(_gk_yol("rapor", kl), gk_rapor_md(TS._ts_kayit(sonuc), X, E))
    return sonuc


# ---------------------------------------------------------------- 9) RAPOR
GK_AD: Dict[str, str] = {
    "x01_tepe250": "250 gün tepeden düşüş", "x02_log_fiyat": "31.10 fiyat (log)", "x03_fon_kriz": "kriz öncesi fon payı",
    "x04_tasfiye_kalan": "tasfiye fonu kalan payı", "x04b_satis_bitti": "satış bitti (son 2 hafta azalış yok)", "x05_azalis_sayisi": "Eyl-Eki azalış bildirimi",
    "x06_leke": "leke (SPK / kayyım / tutuklama)", "x06b_mkk_yasak": "MKK yasaklı pay listesinde", "x07_geri_alim": "geri alım ilanı / işlemi",
    "x07b_geri_alim_sayi": "geri alım işlem bildirimi sayısı", "x08_pddd": "PD/DD", "x09_halka_aciklik": "halka açıklık", "x10_hacim_oran": "hacim 10g / 60g",
    "x11_dipten_gun": "dipten bu yana gün", "x12_col": "31.10'da çöl (COL_v1 / K24)", "x13_bist100": "BIST 100 üyesi", "x14_ortak_alim": "Ekim ortak / yönetici alımı",
    "x15_ayni": "ayni ödeme adayı (Pusula / Atlas)", "x13b_bist500": "BIST 500 üyesi"}


def _gk_s(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    return f"{v:+.{n}f}".replace(".", ",")


def _gk_p(x: Any) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(v) else f"{v:.3f}".replace(".", ",")


def gk_rapor_md(S: Dict[str, Any], X: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> str:
    E = E or GK_ESIK; R = pd.DataFrame(S["tablo"]); A = S["agac"]; Yo = S["Y_ozet"]
    ad = R[R.aday.astype(bool)] if len(R) else R
    sn = R[R.sinanir.astype(bool)].copy(); sn["abs"] = sn.rho_Y1.abs(); top = sn.sort_values("abs", ascending=False).head(3)
    sat = ["# Fon krizi dönüşü: 31.10'da bilinen ne, Kasım dönüşünü gösterdi mi? (64 hisse, kesit)", "",
           f"{S['surum']}. Ölçüm {S['bitis']}. Fiyat {S['fiyat_son_tarih']}" + (" (13.11 gün içi son bar)" if S.get("gun_ici") else " (13.11 kapanış)") + ".", "",
           "## Sonuç", ""]
    if len(ad):
        sat.append("ADAY EMARE: " + "; ".join(f"{GK_AD.get(v, v)} (rho Y1 {_gk_s(r1)}, Y2 {_gk_s(r2)}, q {_gk_p(q)})"
                                               for v, r1, r2, q in zip(ad.degisken, ad.rho_Y1, ad.rho_Y2, ad.q_Y1)) + ".")
    else:
        sat.append(f"ADAY EMARE YOK: {int(R.sinanir.sum())} sınanan özelliğin hiçbiri BH (q = 0,10) sonrası anlamlı ve Y1-Y2 aynı yönde değil.")
    sat += ["", f"Dönüş (medyan): 31.10 -> 13.11 x{Yo['Y1']['medyan']:.2f} (en az {Yo['Y1']['min']:.2f}, en çok {Yo['Y1']['max']:.2f}); 2-13 Kasım tavan "
            f"sayısı medyan {Yo['Y2']['medyan']:.0f} (en çok {Yo['Y2']['max']:.0f}); dipten x{Yo['Y3']['medyan']:.2f}.", "",
            "En güçlü 3 ilişki (|rho Y1|): " + "; ".join(f"{GK_AD.get(v, v)} rho {_gk_s(r)} (p {_gk_p(p)}, üst yarı - alt yarı Y1 {_gk_s(y)})"
                                                         for v, r, p, y in zip(top.degisken, top.rho_Y1, top.p_Y1, top.yari_Y1)) + ".", "",
            "## Tablo (Spearman; p = 10.000 permütasyon, iki yönlü; q = BH, Y1 ailesi)", "",
            "| değişken | n | rho Y1 | rho Y2 | rho Y3 | üst-alt Y1 | p (Y1) | q | aday mı |", "|---|---|---|---|---|---|---|---|---|"]
    for r in R.itertuples(index=False):
        if r.sinanir:
            sat.append(f"| {GK_AD.get(r.degisken, r.degisken)} | {r.n} | {_gk_s(r.rho_Y1)} | {_gk_s(r.rho_Y2)} | {_gk_s(r.rho_Y3)} | {_gk_s(r.yari_Y1)} | "
                       f"{_gk_p(r.p_Y1)} | {_gk_p(r.q_Y1)} | {'EVET' if r.aday else 'hayır'} |")
        else:
            sat.append(f"| {GK_AD.get(r.degisken, r.degisken)} | {r.n} | {_gk_s(r.rho_Y1)} | {_gk_s(r.rho_Y2)} | {_gk_s(r.rho_Y3)} | - | - | - | "
                       f"sınanmadı ({r.neden}) |")
    sat += ["", "Y1 = 13.11 / 30.10 kapanış; Y2 = 2-13 Kasım tavan sayısı; Y3 = 13.11 / Eylül sonrası dip. rho > 0: özellik büyüdükçe dönüş büyük.", "",
            f"## Ağaç (derinlik 2, yalnız açıklama): {' + '.join(GK_AD.get(v, v) for v in A['degiskenler'])}", "",
            f"Hedef: Y1 >= medyan ({A['esik_Y1']:.2f}). İç doğruluk %{100 * A['ic_dogruluk']:.0f}; LOO doğruluk %{100 * A['loo_dogruluk']:.0f} "
            f"(taban %{100 * A['taban']:.0f}, n {A['n']}).", "", "```", *A["metin"], "```", "",
            "## Cemal'in 4 hissesi: fon %5'e çıkmadan önceki 120 günde çöl var mıydı?", "",
            "| hisse | fon %5 tarihi (kaynak) | pencere | COL_v1 çöl günü (ilk - son) | AL kırılımı | K24 iki evre | çöl var mı |", "|---|---|---|---|---|---|---|"]
    for c in S["col4"]:
        if "T5" not in c:
            fz = c.get("fon_izi") or {}
            sat.append(f"| {c['sembol']} | YOK: FON_IZI en yüksek pay {100 * (fz.get('max_pay') or 0):.2f}% ({fz.get('max_ay')}); KAP'ta %5 bildirimi "
                       f"bulunamadı | - | - | - | - | ölçülemedi |")
            continue
        kisa = c.get("bar_once", 999) < 260
        sat.append(f"| {c['sembol']} | {c['T5']} ({c['T5_kaynak']}; KAP'ta ilk portföy bildirimi {c.get('kap_ilk_portfoy_bildirimi')}) | "
                   f"{c['pencere'][0]} - {c['pencere'][1]} ({c.get('bar_once')} bar geçmiş" + (", COL_v1 için < 260: ÖLÇÜLEMEZ" if kisa else "") + f") | {c['col_tespit_gun']} gün"
                   + (f" ({c['col_ilk']} - {c['col_son']})" if c["col_tespit_gun"] else "") + f" | {', '.join(c['al']) or 'yok'} | "
                   f"{', '.join(c['k24']) or 'yok'} | {'EVET' if c['col_var'] else ('ÖLÇÜLEMEDİ' if kisa else 'HAYIR')} |")
    sat += ["", "## Sınırlar", "", E["sinir"] + ".", "",
            f"Kapı: ön kayıt {S['kapi'].get('onkayit_git', {}).get('commit', '?')[:10]}, mühür {S['kapi']['esik_sha256'][:12]}, X {S['kapi']['X_sha256'][:12]}"
            + (f"; SAPMA: {S['kapi']['sapma']}" if S["kapi"].get("sapma") else "") + "."]
    return "\n".join(sat) + "\n"


def gk_rapor(kl: Optional[str] = None) -> str:
    S = _gk_json_oku(_gk_yol("sonuc", kl)); X = pd.read_csv(_gk_yol("X"))
    return _gk_yaz(_gk_yol("rapor", kl), gk_rapor_md(S, X))


# ---------------------------------------------------------------- ÇAKIŞMA KAPISI
def _cakisma_kontrol_gk(_once=_CK_ONCE_GK, _dosya="GENIS_KESIT.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_GK", "_CK_KAYIT", "_cakisma_kontrol_gk", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "re", "hashlib", "subprocess", "time", "glob", "_dt", "_html", "annotations",
           "Any", "Callable", "Dict", "List", "Optional", "Sequence", "Tuple", "TS")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_gk()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=GK_SURUM)
    ap.add_argument("komut", choices=["topla", "x", "onkayit", "sonuc_indir", "kos", "rapor"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--sapma", default=None, help="kos: ön kayıttan sonra kod değiştiyse gerekçe (sonuca yazılır)")
    a_ = ap.parse_args()
    try:
        if a_.komut == "topla":
            print(json.dumps(TS._ts_kayit(gk_topla()), ensure_ascii=False))
        elif a_.komut == "x":
            X_, _ = gk_x(); print(_gk_yol("X")); print("\n".join(gk_x_ozet(X_)))
        elif a_.komut == "onkayit":
            y_ = gk_onkayit(a_.cikti); print(y_, "mühür", gk_esik_sha(), "kod", gk_kod_sha(), "X", TS.ts_sha_dosya(_gk_yol("X")))
        elif a_.komut == "sonuc_indir":
            print(json.dumps(TS._ts_kayit(gk_sonuc_indir()), ensure_ascii=False)[:2000])
        elif a_.komut == "kos":
            s_ = gk_kos(a_.cikti, sapma=a_.sapma); print(_gk_yol("rapor", a_.cikti))
        else:
            print(gk_rapor(a_.cikti))
    except (GkHata, TS.TsHata, FileNotFoundError) as ex:
        gklog.error("%s", ex); sys.exit(1)
