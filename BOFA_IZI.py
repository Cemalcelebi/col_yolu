"""BOFA_IZI — 'BofA (Bank of America aracı kurum kodu) net alım listesinde üst sıralarda' bir BIST hissesinin sonraki getirisi (13 Kasım 2026). Tek dosya.

Soru (Cemal, 13 Kasım 2026: 'BofA almışsa emaredir; en erken nasıl bulunur; ölç'): hisse.net (ForInvest AKD aktarımı), YatırımX ve Rota Borsa'nın
yayımladığı BofA gün içi / gün sonu / haftalık alım-satım listelerinde ilk sıralarda görünen hisse, sonra kontrolünden iyi gidiyor mu? Ne kadar erken
bilinebiliyor?

ANA ÖLÇÜ (Cemal'in 13.11 talimatı, ön kayıttan önce): 'BofA TUTMA DÖNEMİ'. Giriş = BofA'nın o hisseyi (lot sıralı) alım listesinde ilk 3'te gösterdiği
ilk haberin yayınından sonraki ilk işlem günü açılışı (açık dönem varken yeni alım haberi yeni olay açmaz); çıkış = girişten sonra yayımlanan ilk
satış listesi haberinde (gün içi / gün sonu / haftalık) ilk 5'te görünmesinden sonraki ilk işlem günü açılışı; satış haberi yoksa 250 işlem günü ya
da veri sonu ('satış görülmedi'). Kontrol = aynı giriş ve aynı çıkış günleriyle aynı 60 gün momentum beşliği x 20 gün likidite üçlüsündeki öteki
hisseler (eşli fark), ay kümeli bootstrap, 200 rastgele portföy. İKİNCİL: FON_IZI.FI_OLCUT 60 gün ölçütü (standart gereği), 5 / 20 gün getiri,
P(+%50, 20g), P(-%30, 20g). Fon krizi: 31.08.2026'yı aşan dönem / pencere ana sonuca girmez; Eylül - Kasım 2026 dönemleri tek tek BİLGİ.

Komut:  python BOFA_IZI.py topla [--site hissenet,yatirimx,rotaborsa] [--sinir N]   site haritası -> BofA haberleri -> /tmp/bofa/ham (önbellek,
                                    istekler arası >= 2 sn, aynı sayfa bir kez) -> /tmp/bofa/bofa_liste.csv + bofa_haber.csv + bofa_kapsam.json
        python BOFA_IZI.py onkayit     ön kayıt (BI_ESIK mührü, kod / veri sha256; varsa üzerine yazmaz) -> arastirma_cikti/bofa_izi/BOFA_ON_KAYIT.md
        python BOFA_IZI.py kos [--sapma G]  ön kayıt git'te ve mühürler tutuyorsa ölçüm -> bofa_sonuc.json + BOFA_RAPOR.md
        python BOFA_IZI.py rapor       raporu sonuç JSON'undan yeniden yazar
        python BOFA_IZI.py izle --tek  hisse.net haber site haritasından yeni BofA listelerini TEK TUR çeker (dakikada en çok 1 istek). Zamanlanmış
                                       değildir; sürekli izleme kurulmadı.
        python BOFA_IZI.py karonkayit  BofA KÂRI (A) + haber sonrası YOL (B) ön kaydı (BK_ESIK mührü, sayımlar; getiri yok)
                                       -> arastirma_cikti/bofa_izi/BOFA_KAR_ON_KAYIT.md
        python BOFA_IZI.py karkos [--sapma G]  kâr ön kaydı git'te ve mühürler tutuyorsa A + B ölçümü -> bofa_kar_sonuc.json + BOFA_KAR_RAPOR.md
                                       (satır verisi /tmp/bofa/kar_*.csv.gz)
        python BOFA_IZI.py karrapor    kâr raporunu sonuç JSON'undan yeniden yazar
Colab:  exec(open('BOFA_IZI.py').read())  (TAVAN_SERISI.py, K60_veri.py, FON_IZI.py aynı klasörde)
Veri:   fiyat /tmp/tavan/yahoo (TAVAN_SERISI.ts_fiyatlar; Yahoo günlük, bölünme düzeltmeli). Ham HTML / csv repoya girmez.
SINIR:  IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md'ye dokunmaz. Ücretli kaynak / abonelik / kayıt yok; e-posta yok.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_BI = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import http.client  # noqa: E402
import html as _html  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import urllib.error  # noqa: E402
import urllib.parse  # noqa: E402
import urllib.request  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_BI = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_BI not in sys.path:
    sys.path.insert(0, KOK_BI)

bilog = logging.getLogger("col.bofa_izi")
if not bilog.handlers:
    _bi_h = logging.StreamHandler(sys.stderr)
    _bi_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s bofa: %(message)s", "%H:%M:%S"))
    bilog.addHandler(_bi_h)
    bilog.setLevel(logging.INFO)
    bilog.propagate = False

BI_ETIKET = "bofa_izi_20261113"
BI_SURUM = "BOFA_IZI v1.0 (bofa_izi_20261113): BofA AKD alım listesi ilk sıraları -> tutma dönemi getirisi (ön kayıtlı)"

BI_YOL: Dict[str, str] = {
    "cikti": os.environ.get("BI_CIKTI", os.path.join(KOK_BI, "arastirma_cikti", "bofa_izi")),
    "is": os.environ.get("BI_IS", "/tmp/bofa"),
    "ham": os.environ.get("BI_HAM", "/tmp/bofa/ham"),
    "harita": os.environ.get("BI_HARITA", "/tmp/bofa/harita"),
}
BI_DOSYA: Dict[str, str] = {"liste": "bofa_liste.csv", "haber": "bofa_haber.csv", "kapsam": "bofa_kapsam.json", "onkayit": "BOFA_ON_KAYIT.md",
                            "sonuc": "bofa_sonuc.json", "rapor": "BOFA_RAPOR.md", "donem": "bofa_donemler.csv.gz", "olay": "bofa_olaylar.csv.gz",
                            "log": "bofa.log"}
BI_SITE: Dict[str, Dict[str, str]] = {
    "hissenet": {"index": "https://www.hisse.net/sitemaps/hissenet-index.xml", "alt": r"/sitemaps/monthly/hissenet/\d{4}-\d{2}\.xml$",
                 "haber": r"^https://www\.hisse\.net/haber/", "govde": "detail-content-inner"},
    "yatirimx": {"index": "https://www.yatirimx.com.tr/sitemap.xml", "alt": r"/sitemap/news-\d{4}-\d{2}\.xml$",
                 "haber": r"^https://www\.yatirimx\.com\.tr/", "govde": 'property="articleBody"'},
    "rotaborsa": {"index": "https://rotaborsa.com/sitemap_index.xml", "alt": r"/post-sitemap\d+\.xml$",
                  "haber": r"^https://rotaborsa\.com/", "govde": "entry-content"},
}
BI_HABER_HARITA = "https://www.hisse.net/sitemaps/news-sitemap.xml"   # Google News site haritası (son ~100 haber, yayın saatiyle)
BI_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
BI_AG: Dict[str, Any] = {"bekle": 2.0, "zaman_asimi": 40, "deneme": 3, "izle_bekle": 60.0, "harita_taze_saat": 6.0}
BI_URL_KURUM = re.compile(r"bofa|bank-of-america|merrill|(?:^|[-/])citi(?:bank|group)?(?:[-/]|$)|deutsche|jp-?morgan|hsbc|morgan-stanley|goldman|"
                          r"(?:^|[-/])ubs(?:[-/]|$)|barclays|credit-suisse", re.I)
BI_URL_MAKRO = re.compile(r"altin|gumus|bitcoin|btc|kripto|ethereum|ons-|anket|petrol|faiz|enflasyon|ceza|bilanco|resesyon|nasdaq|wall-street|"
                          r"fed-|s-p-500|dolar-|euro-", re.I)
BI_URL_LISTE = re.compile(r"alim|alis|satim|satis|aldi|satti|liste|topla|cikis|cikti|cikar|hisse|tahta|lot|net-|zirve|sira|basinda|tavan|taban", re.I)
BI_URL_TEK = re.compile(r"hedef-fiyat|sinirini|sinirin|pay-sahipligi|esigi|esigin|-orani|oranini|hisselerinde|hissesinde|-kap-|kapa-|rapor|"
                        r"tahmin|tavsiye|beklenti", re.I)   # tek hisse haberi, KAP pay bildirimi, hedef fiyat / rapor: liste değil
_BI_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")
_BI_YASAK = ("IZ_DEFTERI.md", "IZ_KARNE.py", "CLAUDE.md", "COL_OZET.md", "ONERI_DEFTERI.md")

# Yabancı kurum anahtarları (normalize edilmiş metinde; sıra önemli: 'jp morgan' 'morgan stanley'den önce)
BI_KURUM: List[Tuple[str, str]] = [("BofA", r"bofa|bank of america"), ("Merrill", r"merrill"), ("JPM", r"jp ?morgan|j\.p\. ?morgan"),
                                   ("MS", r"morgan stanley"), ("Citi", r"\bciti"), ("Deutsche", r"deutsche"), ("HSBC", r"\bhsbc"),
                                   ("Goldman", r"goldman"), ("UBS", r"\bubs\b"), ("Barclays", r"barclays"), ("CS", r"credit suisse")]
BI_KURUM_ANA = "BofA"

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256 mührü ön kayıtta; sonuç görüldükten sonra değişmez)
BI_ESIK: Dict[str, Any] = {
    "surum_etiket": BI_ETIKET,
    "liste": {"kurum": "BofA", "ana_birim": "hepsi",
              "ana_kaynak": "ANA: haberde yayımlanan BofA listesi, birimi ne olursa olsun (lot sıralı hisse.net ForInvest tabloları ve TL sıralı "
                            "YatırımX / Rota Borsa / hisse.net listeleri; Cemal'in tanımı 'haberde ilk 3'). DUYARLILIK: yalnız lot sıralı, yalnız TL "
                            "sıralı, yalnız yapılandırılmış (tablo / satır; düz yazıdan çıkarılan sıra hariç)",
              "bicim": "tablo; satir ('PAHOL: 16.561.430 lot (...)'); baslik_tablo (Rota Borsa); duzyazi (aynı kurum + yön için yapılandırılmış liste "
                       "yoksa metindeki geçiş sırası: geçerli kod + 90 karakter içinde 'sayı (milyon) lot / TL')",
              "blok": "bir haberde aynı kurum + yön için birden çok liste varsa ilki; sıra = listede yayımlanan sıra ('Diğer' satırı sayılmaz)",
              "tur": "haftalık <=> başlık / spot 'haftal'; gün içi <=> metinde veri saati < 18:00 ('saat 12:25 verilerine göre', '12:30 itibarıyla') "
                     "ya da yayın 09:55-18:05 arası ve gün sonu ibaresi yok; gün sonu <=> başlık / spot / ilk paragrafta 'gün sonu' ya da yayın >= 18:05 "
                     "ya da < 09:55; hafta sonu yayın + 'hafta' ibaresi -> haftalık",
              "veri_gunu": "gün içi / gün sonu: yayın >= 09:55 ise yayın günü (işlem günü değilse önceki işlem günü), < 09:55 ise önceki işlem günü"},
    "giris": {"kural": "haberin yayınından SONRAKİ ilk işlem günü açılışı: yayın < 09:55 ve gün işlem günüyse o gün, değilse ertesi işlem günü "
                       "(seans içindeki haber de ertesi açılış)",
              "bilgi_kapanis": "BİLGİ: gün içi listede (yayın < 18:00, işlem günü) aynı gün kapanışından giriş",
              "takvim": "en az 50 hissenin işlem gördüğü günler (Yahoo önbelleği)"},
    "donem": {"giris_sira": 3, "cikis_sira": 5, "cikis_tur": ["gun_ici", "gun_sonu", "haftalik"], "giris_tur": ["gun_ici", "gun_sonu", "haftalik"],
              "tavan_gun": 250,
              "tanim": "her hisse için alım haberleri zaman sırasıyla: ilk 3'te görüldüğü ilk haber DÖNEM AÇAR (giriş = yayından sonraki ilk açılış); "
                       "çıkış haberi = giriş günü 10:00'dan SONRA yayımlanan ilk BofA satış listesi haberi (her tür) ve hisse orada ilk 5'te; çıkış = "
                       "o haberin yayınından sonraki ilk açılış. Satış haberi yoksa çıkış = giriş + 250 işlem günü ya da veri sonu ('satış görülmedi' "
                       "ayrı sayılır). Dönem açıkken gelen alım haberleri yeni dönem açmaz; çıkış haberinden sonra gelen alım haberi yeni dönem açar.",
              "varyant": "çıkış = BofA satış listesi haberleri zaman sırasıyla dizildiğinde hissenin İKİ ARDIŞIK haberde ilk 3'te görülmesi (ikinci "
                         "haberin yayınından sonraki ilk açılış)",
              "getiri": "dönem getirisi = O(çıkış) / O(giriş) - 1; çıkış günü açılış yoksa (durdurma) 5 gün içindeki ilk açılış, o da yoksa son kapanış",
              "uc": "dönem en yüksek = max H[giriş .. çıkış-1] / O(giriş) - 1; en düşük = min L[aynı] / O(giriş) - 1",
              "olasilik": "P(dönem getirisi >= +%50); P(dönemde -%30'a dokunma: en düşük <= -0,30)",
              "gec_kalma": "O(giriş) / BofA'nın açılış haberindeki ortalama maliyeti - 1 (maliyet yazılıysa)",
              "kontrol": "aynı giriş günü d ve aynı çıkış günü x: d günü aynı 60 gün momentum beşliği x 20 gün TL likidite üçlüsündeki (FI_OLCUT "
                         "tanımı: momentum C[d-1]/C[d-61]-1, likidite önceki 20 günün medyan C*V) öteki hisselerin aynı kuralla dönem getirisi "
                         "ortalaması; EŞLİ FARK = olay - eş ortalaması; SIRA = olayın eşler içindeki yeri (0-1)",
              "portfoy": "10 yuva, dönem boyunca tut (yuva çıkış günü boşalır), olay getirileri vs her olay yerine aynı gün aynı hücreden rastgele "
                         "eş alınan 200 portföy (aynı giriş / çıkış günleri)",
              "bootstrap": "ay kümeli (giriş ayı), 2000 tekrar, tohum 27, %95 aralık ortalama eşli fark için"},
    "olay60": {"ana_sira": 3, "duyarlilik_sira": [1, 5], "ardisik": 2, "tekil_gun": 60,
               "secim": "her veri günü için BİR liste: gün sonu varsa en erken yayımlanan gün sonu, yoksa en geç gün içi (ana: her birim); haftalık ayrı BİLGİ",
               "tanim": "olay = o günün seçilen alım listesinde ilk K; ardışık = iki ardışık işlem gününün seçilen listelerinde ilk 3 (olay günü ikinci "
                        "gün); aynı hissede 60 işlem gününde tek olay (ilki); ölçüt FON_IZI.FI_OLCUT (r60, eşli fark, ay kümeli bootstrap, hücre içi "
                        "sıra, 10 yuva portföy vs 200 rastgele); ayrıca r5, r20, P(+%50'ye dokunma 20g: max H >= 1,5 O), P(-%30'a dokunma 20g: "
                        "min L <= 0,7 O) ve aynı gün aynı hücre eşlerinin aynı olasılıkları (kat = olay / eş)",
               "ters": "satış listesi ilk 3 aynı ölçülerle (ters sınama: BofA bilgiliyse eşli fark < 0 beklenir)"},
    "kurum": {"kodlar": [k for k, _ in BI_KURUM],
              "tanim": "her yabancı kod (haberlerde alım / satım listesi bulunan) AYNI tutma dönemi ölçüsüyle (BI_ESIK['donem']), kodun kendi "
                       "listeleriyle; Merrill haberde BofA'dan ayrı geçiyorsa ayrı kod",
              "birim": "her kodda bütün birimler (ana ile aynı)",
              "toplu": "TOPLU satır: herhangi bir yabancı kodun (BofA dahil) alım listesinde ilk 3 dönem açar, herhangi bir yabancı kodun satış "
                       "listesinde ilk 5 kapatır (her liste kendi sırasıyla, birim ayrımı yok)",
              "bh": "Benjamini-Hochberg q = 0,10; p = ay kümeli bootstrap tek yönlü P(ortalama eşli dönem farkı <= 0) ((say + 1) / (B + 1)); "
                    "m = kesik içinde en az 1 ölçülmüş dönemi olan kod sayısı (toplu hariç)",
              "karar": "kod 'iz adayı' <=> ana karar şartları (n >= 30, ortalama eşli fark > 0, alt uç > 0, A ve B > 0) VE BH ile reddedilen; "
                       "arşivde listesi olmayan kod 'veri yok'",
              "kriz": "kriz dönemi (giriş >= 01.09.2026) açık dönemler kod bazında tablo (BİLGİ)",
              "kaynak": "Cemal 13.11.2026 eki, ön kayıttan önce"},
    "alt_kume": {"cokmus": -0.60, "tanim": "çökmüş <=> giriş öncesi kapanış / önceki 250 günün en yüksek kapanışı - 1 <= -0,60 (en az 120 bar); diğer"},
    "kriz": {"kesik": "2026-08-31",
             "kural": "ana sonuç: çıkış günü (dönem) / 60. gün (r60) / 20. gün (20 gün ölçüleri) <= 31.08.2026. Aşanlar ana sonuca girmez, sayılır. "
                      "Giriş günü >= 01.09.2026 dönemleri tek tek BİLGİ tablosunda (açık dönem: bugüne getiri, BofA hâlâ tutuyor mu)"},
    "yari": {"sinir": "2025-01-01",
             "tanim": "alt dönemler giriş tarihine göre: A < 01.01.2025 <= B. Veri aralığı (ilk liste veri günü 17.04.2023 - kriz kesiği 31.08.2026) "
                      "takvim orta noktası 08.01.2025'e en yakın ay başı; veri toplandıktan, getiri hesaplanmadan seçildi"},
    "karar": {"n_min": 30,
              "metin": "ANA (tutma dönemi): n >= 30 VE ortalama eşli dönem farkı > 0 VE ay kümeli bootstrap %95 alt uç > 0 VE iki alt dönemde (A, B) "
                       "ortalama eşli fark aynı yönde (ikisi de > 0) -> 'BofA tutma dönemi BIST'te iz adayı'; değilse 'kanıt yok' ve hangi şart "
                       "tutmadı. Sıra ve portföy raporlanır, karara girmez (Cemal'in tutma dönemi kararı). İKİNCİL (FI_OLCUT 60 gün, alım ilk 3): "
                       "n >= 30, ortalama eşli fark > 0 ve alt uç > 0, sıra > 0,50, portföy > rastgele %90 VE iki alt dönem aynı yön -> 'iz adayı' "
                       "(ikincil); değilse 'kanıt yok'. Tek pazar (BIST): FI_OLCUT'un ABD + Avrupa karar hücreleri bu veride yok, en fazla 'BIST iz "
                       "adayı' denir. FI_OLCUT dönem hücreleri (2023, 2024-26) BİLGİ olarak ayrıca yazılır.",
              "coklu": "ana dışındaki satırlar (ilk 1, ilk 5, ardışık, varyant çıkış, TL listeleri, alt kümeler) BİLGİ / duyarlılık; çoklu deneme"},
    "yanlilik": "AKD kodu kurum kimliği değildir (savcılık 'yabancı görünümlü yerli işlem' inceliyor). Arşiv haber sitesinin seçtiği günlerdir (her gün "
                "liste yok; eksik günler sayılır). Liste ilk 5 ile sınırlı: 'ilk 5'te görülmedi' satış olmadığı anlamına gelmez. Fiyat evreni bugün "
                "işlem gören hisseler (hayatta kalma yanlılığı yukarı). İşlem maliyeti yok.",
}


class BiHata(RuntimeError):
    """BOFA_IZI'ye özgü durdurucu hata (veri yok, ön kayıt yok / değişmiş / git'e işlenmemiş, mühür tutmuyor)."""


# ---------------------------------------------------------------- 0) YARDIMCILAR
def _bi_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _bi_yol(ad: str, kl: Optional[str] = None) -> str:
    return os.path.join(kl or BI_YOL["cikti"], BI_DOSYA.get(ad, ad))


def _bi_is(ad: str) -> str:
    return os.path.join(BI_YOL["is"], BI_DOSYA.get(ad, ad))


def _bi_yaz(yol: str, metin: str) -> str:
    if _BI_EPOSTA.search(metin):
        raise BiHata(f"{os.path.basename(yol)}: metinde e-posta biçimli parça var; yazılmadı")
    if os.path.basename(yol) in _BI_YASAK:
        raise BiHata(f"{yol}: defter dosyasına yazılmaz")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _bi_kayit(x: Any) -> Any:
    if isinstance(x, pd.DataFrame):
        return [_bi_kayit(r) for r in x.to_dict(orient="records")]
    if isinstance(x, dict):
        return {str(k): _bi_kayit(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_bi_kayit(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        x = x.item()
    if isinstance(x, float) and not np.isfinite(x):
        return None
    if isinstance(x, pd.Timestamp):
        return str(x) if (x.hour or x.minute) else str(x.date())
    if isinstance(x, (_dt.date, _dt.datetime)):
        return str(x)
    return x


def _bi_json(yol: str, obj: Any) -> str:
    return _bi_yaz(yol, json.dumps(_bi_kayit(obj), ensure_ascii=False, indent=1, sort_keys=True, default=str))


def bi_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for p in iter(lambda: f.read(1 << 20), b""):
            h.update(p)
    return h.hexdigest()


def bi_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or BI_ESIK, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")).hexdigest()


def bi_kod_sha(yol: Optional[str] = None) -> str:
    return bi_sha_dosya(yol or os.path.join(KOK_BI, "BOFA_IZI.py"))


def bi_git_durum(yol: str) -> Dict[str, str]:
    """Dosya git'e işlenmiş ve çalışma kopyası HEAD ile aynı mı? Değilse BiHata. Döner son commit ve zamanı."""
    kl = os.path.dirname(os.path.abspath(yol)); ad = os.path.basename(yol)
    try:
        r = subprocess.run(["git", "-C", kl, "ls-files", "--error-unmatch", ad], capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            raise BiHata(f"{ad} git'e işlenmemiş (ön kayıt önce commit edilmeli)")
        r = subprocess.run(["git", "-C", kl, "diff", "--quiet", "HEAD", "--", ad], capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            raise BiHata(f"{ad} işlenmiş sürümden farklı (commit sonrası değişmiş)")
        r = subprocess.run(["git", "-C", kl, "log", "-1", "--format=%H|%cI", "--", ad], capture_output=True, text=True, timeout=30)
        h, z = (r.stdout.strip().split("|") + [""])[:2]
        if not h:
            raise BiHata(f"{ad}: git geçmişi yok")
        return {"commit": h, "commit_zamani": z}
    except (OSError, subprocess.SubprocessError) as ex:
        raise BiHata(f"git denetimi yapılamadı ({type(ex).__name__}: {ex})") from ex


_BI_TR = str.maketrans({"İ": "i", "I": "i", "ı": "i", "Ş": "s", "ş": "s", "Ğ": "g", "ğ": "g", "Ü": "u", "ü": "u", "Ö": "o", "ö": "o",
                        "Ç": "c", "ç": "c", "’": "'", "‘": "'", "Â": "a", "â": "a", "Î": "i", "î": "i", "Û": "u", "û": "u"})


def bi_norm(s: str) -> str:
    """Türkçe harfleri ASCII'ye indirip küçük harf; boşlukları teke indirir."""
    return re.sub(r"\s+", " ", (s or "").translate(_BI_TR).lower()).strip()


def bi_sayi(s: Any) -> float:
    """'40.428.769' -> 40428769; '-32.189.870' -> -32189870; '0,856' -> 0.856; '%29,67' -> 29.67; '1,5 milyar' -> 1.5e9; '+146.270.000 TL'."""
    if s is None:
        return np.nan
    t = str(s).replace("−", "-").replace("–", "-").replace("\xa0", " ").strip()
    n = bi_norm(t); kat = 1e9 if "milyar" in n else 1e6 if ("milyon" in n or re.search(r"\bmn\b", n)) else 1.0
    m = re.search(r"([-+]?)\s*(\d[\d.]*(?:,\d+)?|\d+)", t)
    if not m:
        return np.nan
    g = m.group(2)
    if "," in g:
        g = g.replace(".", "").replace(",", ".")
    elif g.count(".") >= 1 and all(len(p) == 3 for p in g.split(".")[1:]) and kat == 1.0:
        g = g.replace(".", "")
    try:
        v = float(g) * kat
    except ValueError:
        return np.nan
    return -v if m.group(1) == "-" else v


def bi_kurum(n: str) -> Optional[str]:
    for ad, rx in BI_KURUM:
        if re.search(rx, n):
            return ad
    return None


def bi_yon(n: str) -> Optional[str]:
    """Normalize metinden yön: alım / satım; ikisi birden ya da hiçbiri -> None. '(net alım)' / '(net satış)' önceliklidir."""
    na, ns = bool(re.search(r"net alim", n)), bool(re.search(r"net sati[sm]", n))
    if na != ns:
        return "alim" if na else "satim"
    a = bool(re.search(r"\balim|\baldi|\baldig|\balis\b|\balin|\btopla|\balici|\balima\b|al(?:dig|di)i hisse", n))
    s = bool(re.search(r"\bsatis|\bsatti|\bsattig|\bsatil|\bcikis|elden cikar|\bsatici|\bsatisa\b|\bsatarken", n))
    if a and not s:
        return "alim"
    if s and not a:
        return "satim"
    return None


# ---------------------------------------------------------------- 1) AĞ (nazik: ana bilgisayar başına >= 2 sn, önbellek, aynı sayfa bir kez)
_BI_SON_ISTEK: Dict[str, float] = {}


def bi_onbellek_adi(url: str) -> str:
    """URL -> önbellek dosya adı: yol bölümleri '_' ile (ör. /haber/slug-123 -> haber_slug-123.html)."""
    p = urllib.parse.urlparse(url); yol = p.path.strip("/") or "kok"
    ad = re.sub(r"[^A-Za-z0-9._-]+", "_", yol.replace("/", "_"))[:180]
    return ad if ad.endswith((".xml", ".html")) else ad + ".html"


def bi_getir(url: str, yol: str, bekle: Optional[float] = None, tazele: bool = False) -> Optional[str]:
    """Önbellekte varsa oradan; yoksa (ya da tazele) indirir, aynı ana bilgisayara istekler arası >= bekle sn. 404 -> '.yok' işareti, None."""
    if not tazele:
        if os.path.exists(yol) and os.path.getsize(yol) > 0:
            with open(yol, encoding="utf-8", errors="replace") as f:
                return f.read()
        if os.path.exists(yol + ".yok"):
            return None
    bekle = BI_AG["bekle"] if bekle is None else max(float(bekle), BI_AG["bekle"])
    host = urllib.parse.urlparse(url).netloc; son_hata = None
    for d in range(BI_AG["deneme"]):
        gecen = time.time() - _BI_SON_ISTEK.get(host, 0.0)
        if gecen < bekle:
            time.sleep(bekle - gecen)
        _BI_SON_ISTEK[host] = time.time()
        try:
            r = urllib.request.Request(url, headers={"User-Agent": BI_UA, "Accept-Language": "tr-TR,tr;q=0.9"})
            with urllib.request.urlopen(r, timeout=BI_AG["zaman_asimi"]) as yan:
                veri = yan.read()
            metin = veri.decode("utf-8", errors="replace")
            os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
            with open(yol, "w", encoding="utf-8") as f:
                f.write(metin)
            return metin
        except urllib.error.HTTPError as ex:
            if ex.code in (404, 410):
                os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
                open(yol + ".yok", "w").close(); return None
            son_hata = f"HTTP {ex.code}"
            time.sleep(bekle * (2 + 3 * d))
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as ex:
            son_hata = f"{type(ex).__name__}: {ex}"
            time.sleep(bekle * (2 + 3 * d))
    bilog.warning("indirilemedi (%s): %s", son_hata, url)
    return None


def bi_harita_oku(xml: str) -> List[Tuple[str, Optional[str]]]:
    """Site haritası (urlset ya da sitemapindex) -> [(loc, lastmod)]."""
    out = []
    for blok in re.findall(r"<(?:url|sitemap)>(.*?)</(?:url|sitemap)>", xml or "", re.S):
        m = re.search(r"<loc>\s*(.*?)\s*</loc>", blok, re.S)
        if m:
            lm = re.search(r"<lastmod>\s*(.*?)\s*</lastmod>", blok, re.S)
            out.append((_html.unescape(m.group(1).strip()), lm.group(1).strip() if lm else None))
    return out


def _bi_harita_eski_mi(yol: str) -> bool:
    return (not os.path.exists(yol)) or (time.time() - os.path.getmtime(yol)) > BI_AG["harita_taze_saat"] * 3600


def bi_aday_url(url: str) -> bool:
    """BofA başlıklı ve makro (altın, kripto, faiz...) olmayan ya da liste kelimesi taşıyan haber URL'si."""
    yol = urllib.parse.urlparse(url).path
    if not BI_URL_KURUM.search(yol) or BI_URL_TEK.search(yol.rstrip("/").split("/")[-1]):
        return False
    return (not BI_URL_MAKRO.search(yol)) or bool(BI_URL_LISTE.search(yol))


def bi_harita(site: str, getir: Callable[..., Optional[str]] = bi_getir) -> pd.DataFrame:
    """Bir sitenin bütün aday BofA haber URL'leri (site haritası indeksi -> alt haritalar). En yeni alt harita ve indeks 6 saatten eskiyse tazelenir."""
    S = BI_SITE[site]; kl = os.path.join(BI_YOL["harita"], site)
    iy = os.path.join(kl, os.path.basename(urllib.parse.urlparse(S["index"]).path))
    idx = getir(S["index"], iy, tazele=_bi_harita_eski_mi(iy))
    if not idx:
        raise BiHata(f"{site}: site haritası indeksi alınamadı")
    alt = [(u, lm) for u, lm in bi_harita_oku(idx) if re.search(S["alt"], u)]
    en_yeni = max((lm or "" for _, lm in alt), default="")
    sat = []
    for u, lm in alt:
        y = os.path.join(kl, os.path.basename(urllib.parse.urlparse(u).path))
        x = getir(u, y, tazele=bool(lm and lm == en_yeni and _bi_harita_eski_mi(y)))
        for loc, lm2 in bi_harita_oku(x or ""):
            if re.search(S["haber"], loc) and bi_aday_url(loc):
                sat.append({"site": site, "url": loc, "lastmod": lm2})
    D = pd.DataFrame(sat, columns=["site", "url", "lastmod"]).drop_duplicates("url")
    bilog.info("%s: %d alt harita, %d aday BofA haberi", site, len(alt), len(D))
    return D


# ---------------------------------------------------------------- 2) AYRIŞTIRICI
_BI_KOD = r"[A-Z][A-Z0-9]{2,5}"
_BI_SATIR1 = re.compile(r"^\s*(?:[\u2022\u00b7*\u25cf\u25aa]\s*)?(?:\d{1,2}[.)]\s*)?(?:[^:()]{0,60}\()?(?P<t>" + _BI_KOD + r")\)?\s*(?:\([^)]{0,60}\))?\s*[:–—-]\s*"
                        r"(?P<v>[-+−]?\s*\d[\d.]*(?:,\d+)?)\s*(?P<b>milyar\s*TL|milyon\s*TL|milyon\s*lot|mn\s*TL|mn\s*lot|lot|TL|adet)?(?P<r>.*)$")
_BI_SAAT = [re.compile(r"\bsaat\s*(\d{1,2})[:.](\d{2})\b"),
            re.compile(r"\b(\d{1,2})[:.](\d{2})\s*(?:'?\s*(?:te|ta|de|da)\b\s*)?(?:itibar|verileri|sulari|'?(?:e|a|ye|ya) kadar|'?(?:te|ta|de|da)\b)")]
_BI_BLOK = re.compile(r"<(table)\b.*?</table>|<(h[1-6])\b[^>]*>(.*?)</h[1-6]>|<(p|li|div|figcaption)\b[^>]*>|</(p|li|div)>|<br\s*/?>", re.S | re.I)


def _bi_metin(h: str) -> str:
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", h or ""))).strip()


def bi_tablo_satirlari(t: str) -> List[List[str]]:
    sat = []
    for tr in re.findall(r"<tr\b.*?</tr>", t, re.S | re.I):
        sat.append([_bi_metin(c) for c in re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", tr, re.S | re.I)])
    return [s for s in sat if any(s)]


def bi_govde(h: str, site: str) -> str:
    """Haber gövdesi (script / stil temizlenmiş). Başlangıç işareti sitenin gövde sınıfı; bitiş 'Yasal Uyarı' / ilgili haberler."""
    h = re.sub(r"<(script|style|noscript|template)\b.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    isaret = BI_SITE.get(site, {}).get("govde")
    i = h.find(isaret) if isaret else -1
    if i < 0:
        i = max(h.find("<article"), 0)
    j = h.find("Yasal Uyar", i + 50)
    if j > 0:
        return h[i:j]
    son = len(h)
    for bit in ("related-posts", "yarpp", "sharedaddy", "post-tags", "comment-respond", "ng-other-news-container-title"):
        j = h.find(bit, i + 50)
        if 0 < j < son:
            son = j
    return h[i:son]


def bi_meta(h: str) -> Dict[str, Any]:
    """Başlık, spot, yayın zamanı (JSON-LD datePublished > meta published_time > <time>), Türkiye saatine (UTC+3) göre naif."""
    m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', h) or re.search(r'<meta[^>]+(?:article:published_time|datePublished)[^>]+content="([^"]+)"', h)
    yayin = None
    if m:
        try:
            z = pd.Timestamp(m.group(1))
            yayin = (z.tz_convert("Europe/Istanbul").tz_localize(None) if z.tzinfo else z)
        except (ValueError, TypeError):
            yayin = None
    if yayin is None:
        m = re.search(r"<time[^>]*>\s*(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}):(\d{2})\s*</time>", h)
        if m:
            yayin = pd.Timestamp(int(m.group(3)), int(m.group(2)), int(m.group(1)), int(m.group(4)), int(m.group(5)))
    b = re.search(r"<h1\b[^>]*>(.*?)</h1>", h, re.S | re.I) or re.search(r'<meta property="og:title" content="([^"]*)"', h)
    sp = re.search(r'<h2 class="post-spot"[^>]*>(.*?)</h2>', h, re.S) or re.search(r'<meta name="description" content="([^"]*)"', h)
    return {"baslik": _bi_metin(b.group(1)) if b else "", "spot": _bi_metin(sp.group(1)) if sp else "", "yayin": yayin}


def bi_veri_saati(n: str) -> Optional[str]:
    """Normalize metinde AKD veri saati ('saat 12:25 verilerine gore', '12:30 itibariyla'); 09:30-18:30 arası ilk eşleşme 'HH:MM'."""
    for rx in _BI_SAAT:
        for m in rx.finditer(n[:2500]):
            sa, dk = int(m.group(1)), int(m.group(2))
            if 9 <= sa <= 18 and not (sa == 18 and dk > 30) and not (sa == 9 and dk < 30):
                return f"{sa:02d}:{dk:02d}"
    return None


def bi_tur(baslik: str, spot: str, ilk: str, yayin: Optional[pd.Timestamp], veri_saati: Optional[str]) -> str:
    """Liste türü: haftalik / aylik / gun_ici / gun_sonu (BI_ESIK['liste']['tur'])."""
    bs = bi_norm(baslik + " " + spot); n0 = bi_norm(ilk)[:700]
    if "haftal" in bs or "gecen hafta" in bs or "hafta boyunca" in bs or re.search(r"hafta (basindan|boyunca)|haftalik", n0[:300]):
        return "haftalik"
    if re.search(r"\baylik\b|ayi karnesi|aylik karne", bs):
        return "aylik"
    if yayin is not None and yayin.dayofweek >= 5:
        return "haftalik" if "hafta" in (bs + " " + n0) else "gun_sonu"
    if veri_saati and veri_saati < "18:00":
        return "gun_ici"
    gs = bool(re.search(r"gun sonu|gun sonunda|gunu .{0,60}(tamamladi|kapatti)|kapanis itibar", bs + " " + n0))
    if gs or veri_saati:
        return "gun_sonu"
    if yayin is not None:
        hm = yayin.strftime("%H:%M")
        if hm >= "18:05" or hm < "09:55":
            return "gun_sonu"
    return "gun_ici"


_BI_DUZ_SAYI = re.compile(r"([-+\u2212]?\s*\d[\d.]*(?:,\d+)?)\s*(milyar|milyon|mn|bin)?\s*(lot|TL|lira)", re.I)


def bi_duzyazi(sat: str, gecerli: Optional[set], hedef: List[Tuple[str, float, str]]) -> None:
    """Düz yazıdaki liste: geçerli kod (gecerli yoksa parantez içi kod) + 90 karakter içinde 'sayı (milyon) lot / TL'. Sıra = geçiş sırası; aynı kod
    bir kez. Örnek: 'Satış listesini sırasıyla -14,54 milyon lotla PAHOL, -12,21 milyon lotla TEHOL ... izledi'."""
    var = {k for k, _, _ in hedef}
    for m in re.finditer(r"(\()?\b(" + _BI_KOD + r")\b(\))?", sat):
        kod = m.group(2)
        if kod in var or (not m.group(1) and (gecerli is None or kod not in gecerli)):   # parantez içi kod her zaman (sıra korunur)
            continue
        pen = sat[max(0, m.start() - 70): m.end() + 90]; orta = m.start() - max(0, m.start() - 70)
        adaylar = [(abs(x.start() - orta), x) for x in _BI_DUZ_SAYI.finditer(pen)]
        if not adaylar:
            if re.search(r"sirasiyla|takip etti|izledi|ilk (5|10|bes|on)|listesinde|listenin|yer aldi|one cikti", bi_norm(sat)):
                hedef.append((kod, np.nan, "?")); var.add(kod)   # sıralama cümlesinde sayısız geçen kod ('sırasıyla BTCIM, KTLEV ... takip etti')
            continue
        x = min(adaylar, key=lambda a: (not (a[1].group(2) or abs(bi_sayi(a[1].group(1))) >= 1e5), a[0]))[1]
        v = bi_sayi(x.group(1) + " " + (x.group(2) or "")) * (1e3 if (x.group(2) or "").lower() == "bin" else 1.0)
        if not np.isfinite(v):
            continue
        hedef.append((kod, v, "lot" if x.group(3).lower() == "lot" else "TL")); var.add(kod)


def bi_ayristir(h: str, url: str, site: str, gecerli: Optional[set] = None, varsayilan_kurum: Optional[str] = None) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Haber HTML -> (meta, liste satırları). Tablolar (Hisse | Net lot | Pay | Maliyet; Şirket | BIST Kodu | Net Alım Tutarı), satırlar
    ('PAHOL: 16.561.430 lot (%13,05 pay - ortalama maliyet: 0,649 TL)') ve Rota Borsa düzeni ('Şirket (KOD)' başlığı + 'Net alım (TL)' tablosu).
    Kurum ve yön bağlamı başlıklardan; değer eksiyse satım. Sıra = blok içindeki yayın sırası."""
    M = bi_meta(h); g = bi_govde(h, site)
    tum = bi_norm(_bi_metin(g)); vs = bi_veri_saati(tum)
    M.update({"site": site, "url": url, "veri_saati": vs})
    M["tur"] = bi_tur(M["baslik"], M["spot"], _bi_metin(g)[:900], M["yayin"], vs)
    slug = bi_norm(urllib.parse.urlparse(url).path.replace("-", " ").replace("/", " "))
    baglam = {"kurum": bi_kurum(bi_norm(M["baslik"])) or bi_kurum(slug) or varsayilan_kurum or BI_KURUM_ANA, "yon": bi_yon(bi_norm(M["baslik"]))}
    bloklar: List[Dict[str, Any]] = []; cur: Optional[Dict[str, Any]] = None; bekleyen: Optional[str] = None
    tablo_kurum = 0

    duz: Dict[Tuple[str, str], List[Tuple[str, float, str]]] = {}
    bicim_ = "tablo"

    def yeni_blok(kurum: str, yon: Optional[str], birim: str) -> Dict[str, Any]:
        b = {"kurum": kurum, "yon": yon, "birim": birim, "satir": [], "bicim": bicim_}; bloklar.append(b); return b

    def ekle(b: Dict[str, Any], kod: str, net: float, pay: float, mal: float) -> None:
        b["satir"].append({"hisse": kod, "net": net, "pay": pay, "maliyet": mal})

    parcalar: List[Tuple[str, str]] = []; i = 0
    for m in _BI_BLOK.finditer(g):
        if m.start() > i:
            parcalar.append(("metin", g[i:m.start()]))
        if m.group(1):
            parcalar.append(("tablo", m.group(0)))
        elif m.group(2):
            parcalar.append(("baslik", m.group(3)))
        else:
            parcalar.append(("ayrac", ""))
        i = m.end()
    parcalar.append(("metin", g[i:]))
    for tip, icerik in parcalar:
        if tip == "ayrac":
            continue
        if tip == "baslik" or (tip == "metin" and re.fullmatch(r"\s*<strong>[^<]{5,120}</strong>\s*", icerik or "")):
            t = _bi_metin(icerik); n = bi_norm(t)
            if not t:
                continue
            mk = re.search(r"\((" + _BI_KOD + r")\)\s*$", t)
            if mk and len(t) < 160:
                bekleyen = mk.group(1); continue
            k = bi_kurum(n); y = bi_yon(n)
            if k:
                baglam["kurum"] = k
            if y:
                baglam["yon"] = y
            if k or y:
                cur = None
            continue
        if tip == "tablo":
            S = bi_tablo_satirlari(icerik)
            if not S:
                continue
            bas = [bi_norm(c) for c in S[0]]
            if any(re.search(r"\bkurum|araci", c) for c in bas):
                ilk = [r[0] for r in S[1:] if r and not bi_norm(r[0]).startswith("diger")]
                if not ilk or sum(bool(re.fullmatch(_BI_KOD, c)) for c in ilk) < 0.5 * len(ilk):
                    tablo_kurum += 1; continue
                bas = ["hisse" if re.search(r"\bkurum|araci", c) else c for c in bas]   # başlığı yanlış 'Aracı Kurum' yazılmış hisse listesi
            if bekleyen and len(S) <= 3 and max(len(s) for s in S) <= 2 and any("net" in c for c in bas):
                v = bi_sayi(S[-1][-1]); y = bi_yon(" ".join(bas)) or baglam["yon"] or ("satim" if v < 0 else "alim")
                birim = "TL" if re.search(r"\btl\b|tutar", " ".join(bas)) else "lot"
                if cur is None or cur["yon"] != y or cur["birim"] != birim or cur["kurum"] != baglam["kurum"] or cur["bicim"] != "baslik_tablo":
                    bicim_ = "baslik_tablo"; cur = yeni_blok(baglam["kurum"], y, birim); bicim_ = "tablo"
                ekle(cur, bekleyen, v, np.nan, np.nan); bekleyen = None; continue
            baslikli = not any(re.fullmatch(_BI_KOD, c or "") for c in S[0][:2]) and not np.isfinite(bi_sayi(S[0][-1]))
            if baslikli:
                govde = S[1:]
                hc = next((j for j, c in enumerate(bas) if re.search(r"\bkod|sembol", c)), None)
                if hc is None:
                    hc = next((j for j, c in enumerate(bas) if "hisse" in c), 0)
                nc = next((j for j, c in enumerate(bas) if re.search(r"\bnet|\blot|tutar|adet|miktar", c) and j != hc), None)
                pc = next((j for j, c in enumerate(bas) if re.search(r"\bpay|oran|%", c) and j not in (hc, nc)), None)
                mc = next((j for j, c in enumerate(bas) if re.search(r"maliyet|\bort", c) and j not in (hc, nc)), None)
                hb = " ".join(bas)
                birim = "TL" if (nc is not None and re.search(r"\btl\b|tutar", bas[nc])) else "lot"
                y_bas = bi_yon(bas[nc]) if nc is not None else None
            else:
                govde = S; hc, nc, pc, mc, birim, y_bas, hb = 0, 1, None, None, "lot", None, ""
            if nc is None:
                continue
            satirlar = []
            for r in govde:
                if len(r) <= max(hc, nc):
                    continue
                mk = re.findall(r"\((" + _BI_KOD + r")\)", r[hc]) or re.findall(r"\b(" + _BI_KOD + r")\b", r[hc])
                if not mk or bi_norm(r[hc]).startswith("diger"):
                    continue
                satirlar.append((mk[-1], bi_sayi(r[nc]), bi_sayi(r[pc]) if pc is not None and pc < len(r) else np.nan,
                                 bi_sayi(r[mc]) if mc is not None and mc < len(r) else np.nan))
            if not satirlar:
                continue
            isaret = [np.sign(s[1]) for s in satirlar if np.isfinite(s[1])]
            y = y_bas or ("satim" if isaret and all(x < 0 for x in isaret) else baglam["yon"] or "alim")
            cur = yeni_blok(baglam["kurum"], y, birim)
            for s in satirlar:
                ekle(cur, *s)
            cur = None; bekleyen = None
            continue
        # metin: satır satır (paragraf başındaki kalın yazı yön bağlamı verir: '• En Çok Satılan Hisse SASA Oldu:')
        ld = re.match(r"\s*<strong>(.*?)</strong>", icerik or "", re.S)
        if ld:
            y = bi_yon(bi_norm(_bi_metin(ld.group(1))))
            if y and y != baglam["yon"]:
                baglam["yon"] = y; cur = None
        t = _html.unescape(re.sub(r"<[^>]+>", " ", icerik or ""))
        for sat in [x.strip() for x in re.split(r"[\r\n]+", t) if x.strip()]:
            m = _BI_SATIR1.match(sat)
            if not m:
                n = bi_norm(sat)
                if len(sat) < 200 and not re.search(r"\d[\d.]{4,}", sat):
                    y = bi_yon(n)
                    if y and y != baglam["yon"]:
                        baglam["yon"] = y; cur = None
                if baglam["yon"]:
                    bi_duzyazi(sat, gecerli, duz.setdefault((baglam["kurum"], baglam["yon"]), []))
                continue
            kod = m.group("t"); v = bi_sayi(m.group("v") + " " + (m.group("b") or ""))
            if kod in ("BIST", "TL", "USD", "EUR", "XU100") or not np.isfinite(v):
                continue
            birim = "TL" if (m.group("b") and "TL" in m.group("b")) else "lot"
            r = m.group("r") or ""
            mm = (re.search(r"(\d[\d.]*,\d+)\s*TL\s*(?:ortalama\s*)?maliyet", r, re.I)
                  or re.search(r"maliyet\s*:?\s*(\d[\d.]*(?:,\d+)?)", r, re.I))
            pp = re.search(r"(?:%|y[uü]zde)\s*(\d+(?:,\d+)?)", r, re.I)
            isr = m.group("v").strip()[:1]
            y = "satim" if v < 0 else "alim" if isr == "+" else (baglam["yon"] or "alim")
            if cur is None or cur["yon"] != y or cur["birim"] != birim or cur["kurum"] != baglam["kurum"] or cur["bicim"] != "satir":
                bicim_ = "satir"; cur = yeni_blok(baglam["kurum"], y, birim); bicim_ = "tablo"
            ekle(cur, kod, v, bi_sayi(pp.group(1)) if pp else np.nan, bi_sayi(mm.group(1)) if mm else np.nan)
    # düz yazı: yalnız aynı kurum + yön için yapılandırılmış liste yoksa (sıra = metindeki geçiş sırası)
    yapili = {(b["kurum"], b["yon"]) for b in bloklar if b["satir"]}
    duz_izin = bool(re.search(r"araci kurum|\bakd\b|forinvest|en (cok|fazla|yuksek) (net )?(alim|satis|aldig|sattig|al|sat)|alim listesi|"
                              r"satis listesi|alim tarafinda|satis tarafinda|net alim|net satis|alim yaptig|satis yaptig|toplam alis", tum)) and not re.search(r"pay oran|esig|sinir|kap'a|bildirim|hedef fiyat",
                                                                                          bi_norm(M["baslik"]))
    M["duzyazi_izin"] = duz_izin
    for (ku, yo), x in duz.items():
        if (ku, yo) in yapili or not x or not duz_izin:
            continue
        bicim_ = "duzyazi"; b = yeni_blok(ku, yo, max(("lot", "TL"), key=lambda u: sum(1 for e in x if e[2] == u)))
        for kod, v, _u in x:
            ekle(b, kod, v, np.nan, np.nan)
    rows: List[Dict[str, Any]] = []; say: Dict[Tuple[str, str], int] = {}
    for b in bloklar:
        if not b["satir"]:
            continue
        k = (b["kurum"], b["yon"]); say[k] = say.get(k, 0) + 1
        for j, s in enumerate(b["satir"], 1):
            rows.append({"kurum": b["kurum"], "yon": b["yon"], "blok": say[k], "sira": j, "birim": b["birim"], "bicim": b["bicim"], "hisse": s["hisse"],
                         "net": s["net"], "pay": s["pay"], "maliyet": s["maliyet"],
                         "gecerli": (s["hisse"] in gecerli) if gecerli is not None else None})
    M["n_satir"] = len(rows); M["kurum_tablosu"] = tablo_kurum
    return M, rows


# ---------------------------------------------------------------- 3) TOPLA
def bi_gecerli_kodlar(klasor: str = "/tmp/tavan/yahoo") -> Optional[set]:
    try:
        return {f[:-8] for f in os.listdir(klasor) if f.endswith(".IS.json")}
    except OSError:
        return None


def bi_haber_id(url: str) -> str:
    return bi_onbellek_adi(url)[:-5]


def bi_topla(siteler: Tuple[str, ...] = ("hissenet", "yatirimx", "rotaborsa"), sinir: Optional[int] = None,
             getir: Callable[..., Optional[str]] = bi_getir, gecerli: Optional[set] = None) -> Dict[str, Any]:
    """Site haritalarından BofA haberleri -> ham HTML önbelleği -> ayrıştırılmış liste + haber tablosu + kapsam."""
    gecerli = gecerli if gecerli is not None else bi_gecerli_kodlar()
    H, L, kapsam = [], [], {"zaman": _bi_simdi(), "site": {}}
    for site in siteler:
        try:
            D = bi_harita(site, getir)
        except BiHata as ex:
            bilog.error("%s", ex); kapsam["site"][site] = {"hata": str(ex)}; continue
        if sinir:
            D = D.head(sinir)
        ok = yok = 0
        for k, r in enumerate(D.itertuples(index=False), 1):
            y = os.path.join(BI_YOL["ham"], site, bi_onbellek_adi(r.url))
            h = getir(r.url, y)
            if not h:
                yok += 1; continue
            ok += 1
            try:
                M, rows = bi_ayristir(h, r.url, site, gecerli)
            except Exception as ex:  # tek haber bozuksa diğerleri sürer; sayılır
                bilog.warning("ayrıştırılamadı %s: %s", r.url, ex); M, rows = {"site": site, "url": r.url, "hata": str(ex)}, []
            hid = bi_haber_id(r.url); M["haber_id"] = hid; M["lastmod"] = r.lastmod
            H.append(M)
            for x in rows:
                L.append({"site": site, "haber_id": hid, "url": r.url, "yayin": M.get("yayin"), "tur": M.get("tur"),
                          "veri_saati": M.get("veri_saati"), **x})
            if k % 50 == 0:
                bilog.info("%s: %d / %d haber", site, k, len(D))
        kapsam["site"][site] = {"aday": int(len(D)), "indirilen": ok, "inmeyen": yok}
    Hd = pd.DataFrame(H); Ld = pd.DataFrame(L)
    os.makedirs(BI_YOL["is"], exist_ok=True)
    Hd.to_csv(_bi_is("haber"), index=False); Ld.to_csv(_bi_is("liste"), index=False)
    kapsam.update(bi_kapsam_ozet(Hd, Ld))
    kapsam["liste_sha256"] = bi_sha_dosya(_bi_is("liste")); kapsam["haber_sha256"] = bi_sha_dosya(_bi_is("haber"))
    _bi_json(_bi_is("kapsam"), kapsam)
    return kapsam


def bi_kapsam_ozet(Hd: pd.DataFrame, Ld: pd.DataFrame) -> Dict[str, Any]:
    out: Dict[str, Any] = {"haber": int(len(Hd))}
    if not len(Ld):
        out["liste_haber"] = 0; return out
    B = Ld[Ld.kurum == "BofA"]
    lh = Hd[Hd.haber_id.isin(B.haber_id.unique())]
    y = pd.to_datetime(lh.yayin)
    out.update({"liste_haber": int(len(lh)), "liste_satir": int(len(B)), "ilk": str(y.min()), "son": str(y.max()),
                "tur": lh.tur.value_counts().to_dict(), "site_liste": lh.site.value_counts().to_dict(),
                "birim": {f"{a}/{b}": int(v) for (a, b), v in B.drop_duplicates(["haber_id", "yon"]).groupby(["site", "birim"]).size().items()},
                "bicim": {f"{a}/{b}": int(v) for (a, b), v in B.drop_duplicates(["haber_id", "yon"]).groupby(["site", "bicim"]).size().items()}
                if "bicim" in B else {},
                "kurum_liste_haber": Ld.drop_duplicates(["haber_id", "kurum"]).kurum.value_counts().to_dict(),
                "diger_kurum": Ld[Ld.kurum != "BofA"].drop_duplicates(["haber_id", "kurum"]).kurum.value_counts().to_dict()})
    return out


# ---------------------------------------------------------------- 4) FİYAT, TAKVİM, PANEL
def bi_fiyat(bas: str = "2022-01-01") -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
    """TAVAN_SERISI.ts_fiyatlar (Yahoo önbelleği) -> {sembol: DataFrame(Open, High, Low, Close, Volume)} bas'tan."""
    import TAVAN_SERISI as TS  # noqa: WPS433 (yalnız fiyat okuyucu; DEĞİŞTİRİLMEZ)
    S, K = TS.ts_fiyatlar()
    V = {}
    for s, d in S.items():
        d = d[d.index >= pd.Timestamp(bas)]
        if len(d) >= 20:
            V[s] = pd.DataFrame({"Open": d.o, "High": d.h, "Low": d.l, "Close": d.c, "Volume": d.v})
    return V, {k: v for k, v in K.items() if k != "eksik"}


def bi_takvim(V: Dict[str, pd.DataFrame], en_az: Optional[int] = None) -> pd.DatetimeIndex:
    """İşlem günleri: en az 50 hissenin (evren 100'den küçükse yarısının) barı olan günler."""
    en_az = en_az if en_az is not None else min(50, max(1, len(V) // 2))
    say = pd.Series(1, index=pd.DatetimeIndex(np.concatenate([d.index.values for d in V.values()]))).groupby(level=0).size()
    return pd.DatetimeIndex(sorted(say[say >= en_az].index))


def bi_giris_gunu(yayin: pd.Timestamp, takvim: pd.DatetimeIndex) -> Optional[pd.Timestamp]:
    """Yayından sonraki ilk işlem günü açılışı: yayın < 09:55 ve işlem günü -> o gün; değilse sonraki işlem günü."""
    if yayin is None or pd.isna(yayin):
        return None
    yayin = pd.Timestamp(yayin); g = yayin.normalize()
    if yayin.strftime("%H:%M") < "09:55" and g in takvim:
        return g
    i = takvim.searchsorted(g, side="right")
    return takvim[i] if i < len(takvim) else None


def bi_veri_gunu(yayin: pd.Timestamp, takvim: pd.DatetimeIndex) -> Optional[pd.Timestamp]:
    """Gün içi / gün sonu listenin veri günü: yayın >= 09:55 -> yayın günü (işlem günü değilse önceki); < 09:55 -> önceki işlem günü."""
    if yayin is None or pd.isna(yayin):
        return None
    yayin = pd.Timestamp(yayin); g = yayin.normalize()
    if yayin.strftime("%H:%M") < "09:55":
        i = takvim.searchsorted(g, side="left") - 1
    else:
        i = takvim.searchsorted(g, side="right") - 1
    return takvim[i] if i >= 0 else None


def bi_panel(V: Dict[str, pd.DataFrame], O: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Birleşik takvimde Op / Hh / Ll / Cf (kapanış, en çok 5 gün ileri taşınmış) dizileri ve her gün momentum beşliği x likidite üçlüsü hücresi
    (FI_OLCUT tanımı; r60 şartı YOK, dönem ölçüsü için). Hücre: giriş günü açılışı olan, momentum ve likiditesi tanımlı hisseler (>= 30)."""
    if O is None:
        import FON_IZI as FI  # noqa: WPS433
        O = FI.FI_OLCUT
    S = sorted(V); idx = pd.DatetimeIndex(sorted(set().union(*[V[s].index for s in S])))
    Op = pd.DataFrame({s: V[s].Open for s in S}).reindex(idx).to_numpy(float)
    Hh = pd.DataFrame({s: V[s].High for s in S}).reindex(idx).to_numpy(float)
    Ll = pd.DataFrame({s: V[s].Low for s in S}).reindex(idx).to_numpy(float)
    Cl = pd.DataFrame({s: V[s].Close for s in S}).reindex(idx)
    Cf = Cl.ffill(limit=5).to_numpy(float)
    Tl = pd.DataFrame({s: V[s].Close * V[s].Volume for s in S}).reindex(idx)
    Vv = pd.DataFrame({s: V[s].Volume for s in S}).reindex(idx).to_numpy(float)
    n, u = Op.shape; mom = O["mom"]
    with np.errstate(all="ignore"):
        Mo = np.full((n, u), np.nan); Mo[mom + 1:] = Cf[mom:-1] / Cf[:-mom - 1] - 1
    Lq = Tl.rolling(O["likit"], min_periods=10).median().shift(1).to_numpy()
    ok = np.isfinite(Mo) & np.isfinite(Lq) & np.isfinite(Op) & (Op > 0)
    Hc = np.full((n, u), -1, int)
    for d in range(n):
        g = ok[d]
        if g.sum() < 30:
            continue
        mq = pd.qcut(pd.Series(Mo[d, g]).rank(method="first"), O["mom_kova"], labels=False).to_numpy()
        lq = pd.qcut(pd.Series(Lq[d, g]).rank(method="first"), O["likit_kova"], labels=False).to_numpy()
        Hc[d, g] = mq * O["likit_kova"] + lq
    with np.errstate(all="ignore"):
        tepe = Cl.rolling(250, min_periods=120).max().shift(1).to_numpy()
        dd = Cf / tepe - 1   # dd[d] = C[d] / max(C[d-250..d-1]); giriş için d-1 kullanılır
    return {"tarih": idx, "sembol": S, "kol": {s: i for i, s in enumerate(S)}, "Op": Op, "Hh": Hh, "Ll": Ll, "Cf": Cf, "H": Hc, "ok": ok, "dd": dd,
            "Vv": Vv}


def _bi_cikis_fiyat(A: Dict[str, Any], x: int, j: Any) -> Any:
    """Çıkış günü x açılışı; yoksa 5 gün içindeki ilk açılış; o da yoksa x günü (ileri taşınmış) kapanışı. j tek sütun ya da dizi."""
    Op, Cf = A["Op"], A["Cf"]; n = len(Op)
    v = Op[x, j].astype(float) if np.ndim(j) else np.array([Op[x, j]], float)
    for k in range(1, 6):
        if x + k >= n:
            break
        bos = ~np.isfinite(v)
        if not bos.any():
            break
        w = Op[x + k, j] if np.ndim(j) else np.array([Op[x + k, j]])
        v = np.where(bos, w, v)
    c = Cf[x, j] if np.ndim(j) else np.array([Cf[x, j]])
    v = np.where(np.isfinite(v), v, c)
    return v if np.ndim(j) else float(v[0])


# ---------------------------------------------------------------- 5) LİSTELER -> OLAYLAR / DÖNEMLER
def bi_liste_hazirla(Ld: pd.DataFrame, takvim: pd.DatetimeIndex, birim: Optional[str] = None, kurum: Optional[str] = "BofA",
                     yapisal: bool = False) -> pd.DataFrame:
    """Kurumun ilk bloğu (haber x kurum x yön), birim süzgeci (None: hepsi), geçerli kod; yayın, veri günü, giriş günü.
    kurum None -> bütün yabancı kodlar (toplu satır)."""
    m = (Ld.blok == 1) & Ld.tur.isin(["gun_ici", "gun_sonu", "haftalik"])
    m &= Ld.kurum.isin([k for k, _ in BI_KURUM]) if kurum is None else (Ld.kurum == kurum)
    if birim is not None:
        m &= Ld.birim == birim
    if yapisal and "bicim" in Ld:
        m &= Ld.bicim != "duzyazi"
    L = Ld[m].copy()
    if "gecerli" in L:
        L = L[L.gecerli.astype(str).isin(["True", "true", "1", "None", "nan"])]
    L["yayin"] = pd.to_datetime(L.yayin)
    L = L.dropna(subset=["yayin"])
    L["veri_gunu"] = [bi_veri_gunu(t, takvim) if tr != "haftalik" else None for t, tr in zip(L.yayin, L.tur)]
    L["giris"] = [bi_giris_gunu(t, takvim) for t in L.yayin]
    return L.sort_values(["yayin", "haber_id", "yon", "sira"]).reset_index(drop=True)


def bi_gunluk_secim(L: pd.DataFrame) -> pd.DataFrame:
    """Her veri günü için BİR alım ve BİR satım listesi: en erken gün sonu, yoksa en geç gün içi (haftalık hariç)."""
    G = L[L.tur.isin(["gun_ici", "gun_sonu"])].dropna(subset=["veri_gunu"])
    sec = []
    for (vg, yon), g in G.groupby(["veri_gunu", "yon"]):
        hb = g.drop_duplicates("haber_id")[["haber_id", "yayin", "tur"]]
        gs = hb[hb.tur == "gun_sonu"].sort_values("yayin")
        h = gs.iloc[0] if len(gs) else hb.sort_values("yayin").iloc[-1]
        sec.append(g[g.haber_id == h.haber_id])
    return pd.concat(sec, ignore_index=True) if sec else G.iloc[:0]


def bi_tekil(X: pd.DataFrame, takvim: pd.DatetimeIndex, gun: int = 60) -> pd.DataFrame:
    """Aynı hissede `gun` işlem günü içinde tek olay (ilki)."""
    if not len(X):
        return X
    ti = {t: i for i, t in enumerate(takvim)}; tut = []; son: Dict[str, int] = {}
    for r in X.sort_values("giris").itertuples():
        i = ti.get(pd.Timestamp(r.giris))
        if i is None:
            continue
        if r.hisse in son and i - son[r.hisse] < gun:
            continue
        son[r.hisse] = i; tut.append(r.Index)
    return X.loc[tut].sort_values("giris").reset_index(drop=True)


def bi_olaylar60(L: pd.DataFrame, takvim: pd.DatetimeIndex, yon: str, k: int, ardisik: int = 1, tekil: int = 60) -> pd.DataFrame:
    """Günlük seçilmiş listelerden olaylar: ilk k (ardisik >= 2 ise art arda işlem günlerinde ilk k; olay günü sonuncusu)."""
    Gs = bi_gunluk_secim(L); G = Gs[(Gs.yon == yon) & (Gs.sira <= k)].copy()
    if ardisik > 1 and len(G):
        ti = {t: i for i, t in enumerate(takvim)}; G["vi"] = G.veri_gunu.map(lambda t: ti.get(pd.Timestamp(t), -10))
        gunler = G.groupby("hisse").vi.apply(set).to_dict()
        G = G[[all((r.vi - j) in gunler[r.hisse] for j in range(1, ardisik)) for r in G.itertuples()]]
    G = G.dropna(subset=["giris"])
    return bi_tekil(G, takvim, tekil) if tekil else G.sort_values("giris").reset_index(drop=True)


def bi_donemler(L: pd.DataFrame, takvim: pd.DatetimeIndex, son_gun: pd.Timestamp, E: Optional[Dict[str, Any]] = None,
                varyant: bool = False) -> pd.DataFrame:
    """BofA tutma dönemleri (BI_ESIK['donem']). Döner: hisse, acilis haberi (yayin, tur, sira, net, maliyet), giris, cikis, cikis haberi, neden."""
    E = E or BI_ESIK; D = E["donem"]
    A = L[(L.yon == "alim") & (L.sira <= D["giris_sira"]) & L.tur.isin(D["giris_tur"])].sort_values("yayin")
    Sx = L[(L.yon == "satim") & L.tur.isin(D["cikis_tur"])].sort_values("yayin")
    sat_haber = Sx.drop_duplicates("haber_id")[["haber_id", "yayin"]].sort_values("yayin").reset_index(drop=True)
    ilk3 = {(r.haber_id, r.hisse) for r in Sx[Sx.sira <= 3].itertuples()}
    ti = {t: i for i, t in enumerate(takvim)}; ki = takvim.searchsorted(son_gun, side="right") - 1
    out = []
    for hisse, g in A.groupby("hisse"):
        kapanis = pd.Timestamp.min
        sh = Sx[(Sx.hisse == hisse) & (Sx.sira <= D["cikis_sira"])]
        for r in g.drop_duplicates("haber_id").itertuples():
            if r.yayin <= kapanis or r.giris is None or pd.isna(r.giris):
                continue
            gi = ti.get(pd.Timestamp(r.giris))
            if gi is None:
                continue
            giris_ani = pd.Timestamp(r.giris) + pd.Timedelta(hours=10)
            cik = None
            if not varyant:
                c = sh[sh.yayin > giris_ani]
                if len(c):
                    cik = c.iloc[0]
            else:
                hs = sat_haber[sat_haber.yayin > giris_ani].reset_index(drop=True)
                for j in range(len(hs) - 1):
                    if (hs.haber_id[j], hisse) in ilk3 and (hs.haber_id[j + 1], hisse) in ilk3:
                        cik = Sx[(Sx.haber_id == hs.haber_id[j + 1]) & (Sx.hisse == hisse)].iloc[0]; break
            if cik is not None:
                cg = bi_giris_gunu(cik.yayin, takvim)
                if cg is None or ti.get(pd.Timestamp(cg), 10 ** 9) > ki:
                    cx, neden, kapanis = takvim[ki], "acik_veri_sonu", pd.Timestamp.max
                else:
                    cx, neden, kapanis = cg, "satis", cik.yayin
            else:
                xi = gi + D["tavan_gun"]
                if xi <= ki:
                    cx, neden, kapanis = takvim[xi], "satis_gorulmedi_250", takvim[xi] + pd.Timedelta(hours=10)
                else:
                    cx, neden, kapanis = takvim[ki], "acik_veri_sonu", pd.Timestamp.max
            out.append({"hisse": hisse, "acilis_haber": r.haber_id, "acilis_yayin": r.yayin, "acilis_tur": r.tur, "acilis_sira": r.sira,
                        "acilis_net": r.net, "bofa_maliyet": r.maliyet, "veri_gunu": r.veri_gunu, "giris": pd.Timestamp(r.giris),
                        "cikis": pd.Timestamp(cx), "neden": neden,
                        "cikis_haber": None if cik is None else cik.haber_id, "cikis_yayin": None if cik is None else cik.yayin,
                        "cikis_sira": None if cik is None else cik.sira, "cikis_tur": None if cik is None else cik.tur})
    return pd.DataFrame(out).sort_values("giris").reset_index(drop=True) if out else pd.DataFrame(
        columns=["hisse", "giris", "cikis", "neden", "acilis_yayin", "veri_gunu"])


# ---------------------------------------------------------------- 6) ÖLÇÜM
def bi_donem_olc(A: Dict[str, Any], X: pd.DataFrame, cokmus: float = -0.60) -> pd.DataFrame:
    """Her dönem: getiri, en yüksek / en düşük, eş ortalaması (aynı giriş / çıkış, aynı hücre), eşli fark, sıra, eş getirileri, geç kalma, çökmüş."""
    ti = {t: i for i, t in enumerate(A["tarih"])}; sat = []
    for r in X.itertuples():
        d = ti.get(pd.Timestamp(r.giris)); x = ti.get(pd.Timestamp(r.cikis)); j = A["kol"].get(r.hisse)
        bos = {"ret": np.nan, "max": np.nan, "min": np.nan, "esli": np.nan, "fark": np.nan, "sira": np.nan, "_esler": None, "gun": np.nan,
               "gec": np.nan, "cokmus": None, "olcuk": False}
        if d is None or x is None or j is None or not np.isfinite(A["Op"][d, j]) or A["Op"][d, j] <= 0:
            sat.append(bos); continue
        o = A["Op"][d, j]; gun = x - d
        ret = (_bi_cikis_fiyat(A, x, j) / o - 1) if gun > 0 else 0.0
        hi = np.nanmax(A["Hh"][d:max(x, d + 1), j]) / o - 1; lo = np.nanmin(A["Ll"][d:max(x, d + 1), j]) / o - 1
        dd = A["dd"][d - 1, j] if d >= 1 else np.nan
        es, esli, sira, fark = None, np.nan, np.nan, np.nan
        if A["H"][d, j] >= 0:
            m = (A["H"][d] == A["H"][d, j]) & A["ok"][d]; m[j] = False
            cols = np.where(m)[0]
            if len(cols) >= 3:
                with np.errstate(all="ignore"):
                    e = (_bi_cikis_fiyat(A, x, cols) / A["Op"][d, cols] - 1) if gun > 0 else np.zeros(len(cols))
                e = e[np.isfinite(e)]
                if len(e) >= 3:
                    es = e; esli = float(e.mean()); fark = ret - esli; sira = float(((e < ret).sum() + 0.5 * (e == ret).sum()) / len(e))
        mal = getattr(r, "bofa_maliyet", np.nan)
        sat.append({"ret": ret, "max": hi, "min": lo, "esli": esli, "fark": fark, "sira": sira, "_esler": es, "gun": gun,
                    "gec": (o / mal - 1) if (mal is not None and np.isfinite(mal) and mal > 0) else np.nan,
                    "cokmus": bool(dd <= cokmus) if np.isfinite(dd) else None, "olcuk": True,
                    "hacim0": bool("Vv" in A and not (A["Vv"][d, j] > 0))})
    Y = X.copy().reset_index(drop=True)
    for k in ("ret", "max", "min", "esli", "fark", "sira", "_esler", "gun", "gec", "cokmus", "olcuk", "hacim0"):
        Y[k] = [s.get(k) for s in sat]
    return Y


def bi_boot(f: np.ndarray, ay: np.ndarray, B: int = 2000, tohum: int = 27) -> Tuple[float, float, float]:
    """Ay kümeli bootstrap: (%2,5, %97,5, tek yönlü p = P(ortalama <= 0) (+1 düzeltmeli))."""
    aylar = np.unique(ay)
    if len(f) < 2 or len(aylar) < 2:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(tohum); grup = {a: f[ay == a] for a in aylar}; ort = []
    for _ in range(B):
        sec = rng.choice(aylar, len(aylar), replace=True); ort.append(np.concatenate([grup[a] for a in sec]).mean())
    ort = np.asarray(ort)
    return float(np.quantile(ort, 0.025)), float(np.quantile(ort, 0.975)), float(((ort <= 0).sum() + 1) / (B + 1))


def bi_slot(giris: np.ndarray, cikis: np.ndarray, getiri: np.ndarray, yuva: int = 10) -> float:
    """10 yuvalı portföy: olay sırasıyla, boş yuva (çıkış günü <= giriş) varsa alır, çıkışta yuva boşalır; toplam getiri."""
    bos = np.zeros(yuva, dtype="int64"); deger = np.ones(yuva) / yuva
    for gi, ci, ri in zip(giris, cikis, getiri):
        k = int(np.argmin(bos))
        if bos[k] <= gi and np.isfinite(ri):
            deger[k] *= 1 + ri; bos[k] = ci
    return float(deger.sum() - 1)


def bi_donem_ozet(Y: pd.DataFrame, yari: str, port_n: int = 200, tohum: int = 27) -> Dict[str, Any]:
    Z = Y[Y.olcuk.astype(bool)].dropna(subset=["fark"]).sort_values("giris")
    n_tum = int(Y.olcuk.astype(bool).sum())
    if not len(Z):
        return {"n": 0, "n_olculen": n_tum}
    f = Z.fark.to_numpy(float); ay = pd.to_datetime(Z.giris).dt.to_period("M").astype(str).to_numpy()
    a, b, pb = bi_boot(f, ay, tohum=tohum)
    g = pd.to_datetime(Z.giris).to_numpy().astype("datetime64[D]").astype(np.int64)
    c = pd.to_datetime(Z.cikis).to_numpy().astype("datetime64[D]").astype(np.int64)
    rng = np.random.default_rng(tohum)
    rast = [bi_slot(g, c, np.array([rng.choice(e) if e is not None and len(e) else x for e, x in zip(Z._esler, Z.ret.to_numpy(float))]))
            for _ in range(port_n)]
    s = pd.Timestamp(yari); A_ = Z[pd.to_datetime(Z.giris) < s]; B_ = Z[pd.to_datetime(Z.giris) >= s]
    return {"n": int(len(Z)), "n_olculen": n_tum, "hisse": int(Z.hisse.nunique()), "gun_medyan": float(Z.gun.median()),
            "gun_q": [float(Z.gun.quantile(q)) for q in (0.1, 0.25, 0.5, 0.75, 0.9)],
            "ort_ret": float(Z.ret.mean()), "medyan_ret": float(Z.ret.median()), "ort_esli": float(Z.esli.mean()),
            "ort_fark": float(f.mean()), "medyan_fark": float(np.median(f)), "alt95": a, "ust95": b, "p_boot": pb, "sira": float(Z.sira.mean()),
            "kazanan": float((f > 0).mean()), "p_ret50": float((Z.ret >= 0.5).mean()), "p_min30": float((Z["min"] <= -0.30).mean()),
            "ort_max": float(Z["max"].mean()), "ort_min": float(Z["min"].mean()),
            "gec_medyan": float(Z.gec.median()) if Z.gec.notna().any() else None, "gec_n": int(Z.gec.notna().sum()),
            "portfoy": bi_slot(g, c, Z.ret.to_numpy(float)), "portfoy_esli_p50": float(np.quantile(rast, 0.5)),
            "portfoy_esli_p90": float(np.quantile(rast, 0.9)),
            "yari_A": {"n": int(len(A_)), "ort_fark": float(A_.fark.mean()) if len(A_) else None},
            "yari_B": {"n": int(len(B_)), "ort_fark": float(B_.fark.mean()) if len(B_) else None},
            "neden": Z.neden.value_counts().to_dict() if "neden" in Z else {}}


def bi_donem_karar(o: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or BI_ESIK; K = E["karar"]
    if o.get("n", 0) < K["n_min"]:
        return {"karar": "kanıt yok", "tutmayan": [f"n = {o.get('n', 0)} < {K['n_min']} (örneklem yetersiz)"]}
    t = []
    if not o["ort_fark"] > 0:
        t.append("ortalama eşli fark <= 0")
    if not (o["alt95"] is not None and o["alt95"] > 0):
        t.append("bootstrap alt uç <= 0")
    fa, fb = o["yari_A"]["ort_fark"], o["yari_B"]["ort_fark"]
    if not (fa is not None and fb is not None and fa > 0 and fb > 0):
        t.append("iki alt dönem aynı yönde (> 0) değil")
    return {"karar": "BofA tutma dönemi BIST'te iz adayı" if not t else "kanıt yok", "tutmayan": t}


def bi_bh(p: Dict[str, float], q: float = 0.10) -> Dict[str, bool]:
    """Benjamini-Hochberg: {ad: p} -> {ad: reddedildi mi}. NaN p reddedilmez, m'ye sayılır."""
    ad = list(p); m = len(ad)
    if not m:
        return {}
    v = np.array([p[a] if p[a] is not None and np.isfinite(p[a]) else np.inf for a in ad]); s = np.argsort(v)
    k = 0
    for i, j in enumerate(s, 1):
        if v[j] <= i / m * q:
            k = i
    red = set(s[:k].tolist())
    return {a: (i in red) for i, a in enumerate(ad)}


def bi_olay_olc(P: Dict[str, Any], A: Dict[str, Any], X: pd.DataFrame, kesik: str) -> pd.DataFrame:
    """60 gün olayları: FI_OLCUT r60 / eşli fark / sıra (FON_IZI.fi_olcut_olay) + r5, r20, P(+%50 / -%30 dokunma, 20g) ve eş oranları; çökmüş."""
    import FON_IZI as FI  # noqa: WPS433
    if not len(X):
        return X.assign(r60=[], fark=[])
    O = X.rename(columns={"hisse": "sembol"})[["sembol", "giris"]].copy()
    Y = FI.fi_olcut_olay(P, O)
    ti = {t: i for i, t in enumerate(A["tarih"])}; ki = A["tarih"].searchsorted(pd.Timestamp(kesik), side="right") - 1
    ek = []
    for r in X.itertuples():
        d = ti.get(pd.Timestamp(r.giris)); j = A["kol"].get(r.hisse)
        e = dict(r5=np.nan, r20=np.nan, up50=np.nan, dn30=np.nan, b_up50=np.nan, b_dn30=np.nan, b_r20=np.nan, cokmus=None, p20=False)
        if d is not None and j is not None and np.isfinite(A["Op"][d, j]) and A["Op"][d, j] > 0 and d + 19 < len(A["tarih"]):
            o = A["Op"][d, j]; e["p20"] = d + 19 <= ki
            e["r5"] = A["Cf"][d + 4, j] / o - 1; e["r20"] = A["Cf"][d + 19, j] / o - 1
            with np.errstate(all="ignore"):
                e["up50"] = float(np.nanmax(A["Hh"][d:d + 20, j]) >= 1.5 * o); e["dn30"] = float(np.nanmin(A["Ll"][d:d + 20, j]) <= 0.7 * o)
                if A["H"][d, j] >= 0:
                    m = (A["H"][d] == A["H"][d, j]) & A["ok"][d]; m[j] = False; c = np.where(m)[0]
                    if len(c) >= 3:
                        oc = A["Op"][d, c]
                        e["b_up50"] = float(np.nanmean(np.nanmax(A["Hh"][d:d + 20, c], axis=0) >= 1.5 * oc))
                        e["b_dn30"] = float(np.nanmean(np.nanmin(A["Ll"][d:d + 20, c], axis=0) <= 0.7 * oc))
                        e["b_r20"] = float(np.nanmean(A["Cf"][d + 19, c] / oc - 1))
            dd = A["dd"][d - 1, j] if d >= 1 else np.nan
            e["cokmus"] = bool(dd <= BI_ESIK["alt_kume"]["cokmus"]) if np.isfinite(dd) else None
        ek.append(e)
    for k in ("r5", "r20", "up50", "dn30", "b_up50", "b_dn30", "b_r20", "cokmus", "p20"):
        Y[k] = [e[k] for e in ek]
    Y["hisse"] = X.hisse.values
    for k in ("veri_gunu", "yayin", "sira", "tur", "net", "maliyet"):
        if k in X:
            Y["liste_sira" if k == "sira" else k] = X[k].values   # 'sira' FI_OLCUT hücre içi sırasıdır; liste sırası ayrı sütun
    return Y


def bi_olay_ozet(Y: pd.DataFrame, yari: str) -> Dict[str, Any]:
    """60 gün satırı: FI_OLCUT hücresi (kriz kesiği içindekiler) + 20 gün olasılıkları ve katları (20 gün penceresi kesik içinde)."""
    import FON_IZI as FI  # noqa: WPS433
    out: Dict[str, Any] = {"n_olay": int(len(Y))}
    if not len(Y):
        return out
    Z = Y[Y.p20.astype(bool) & Y.up50.notna()]
    if len(Z):
        bu, bd = Z.b_up50.mean(), Z.b_dn30.mean()
        out.update({"n20": int(len(Z)), "p_up50": float(Z.up50.mean()), "b_up50": float(bu), "kat_up50": float(Z.up50.mean() / bu) if bu > 0 else None,
                    "p_dn30": float(Z.dn30.mean()), "b_dn30": float(bd), "kat_dn30": float(Z.dn30.mean() / bd) if bd > 0 else None,
                    "r5": float(Z.r5.mean()), "r20": float(Z.r20.mean()), "b_r20": float(Z.b_r20.mean())})
    H = FI.fi_olcut_hucre(Y.dropna(subset=["fark"]))
    out["fi"] = {k: v for k, v in H.items()}
    W = Y.dropna(subset=["fark"]); s = pd.Timestamp(yari)
    out["yari_A"] = float(W[pd.to_datetime(W.giris) < s].fark.mean()) if (pd.to_datetime(W.giris) < s).any() else None
    out["yari_B"] = float(W[pd.to_datetime(W.giris) >= s].fark.mean()) if (pd.to_datetime(W.giris) >= s).any() else None
    return out


def bi_olay_karar(o: Dict[str, Any]) -> Dict[str, Any]:
    H = o.get("fi") or {}; t = []
    if H.get("n", 0) < BI_ESIK["karar"]["n_min"]:
        return {"karar": "kanıt yok", "tutmayan": [f"n = {H.get('n', 0)} < 30"]}
    if not H["ort_fark"] > 0:
        t.append("ortalama eşli fark <= 0")
    if not H["alt95"] > 0:
        t.append("alt uç <= 0")
    if not H["sira"] > 0.5:
        t.append("sıra <= 0,50")
    if not H["portfoy"] > H["portfoy_esli_p90"]:
        t.append("portföy rastgele %90'ı geçmedi")
    if not ((o.get("yari_A") or -1) > 0 and (o.get("yari_B") or -1) > 0):
        t.append("iki alt dönem aynı yönde (> 0) değil")
    return {"karar": "iz adayı (ikincil)" if not t else "kanıt yok", "tutmayan": t}


# ---------------------------------------------------------------- 7) EN ERKEN BİLGİ
def bi_saat_ozet(Hd: pd.DataFrame, Ld: pd.DataFrame) -> Dict[str, Any]:
    """BofA liste haberlerinin yayın saati dağılımı (tür ve site bazında), veri saati ve gecikme (yayın - veri saati)."""
    ids = set(Ld[Ld.kurum == "BofA"].haber_id)
    H = Hd[Hd.haber_id.isin(ids)].copy(); H["yayin"] = pd.to_datetime(H.yayin); H = H.dropna(subset=["yayin"])
    H = H[H.yayin.dt.dayofweek < 5]

    def q(s: pd.Series) -> Dict[str, Any]:
        if not len(s):
            return {"n": 0}
        m = s.dt.hour * 60 + s.dt.minute
        f = lambda v: f"{int(v) // 60:02d}:{int(v) % 60:02d}"  # noqa: E731
        return {"n": int(len(s)), "en_erken": f(m.min()), "q10": f(m.quantile(0.1)), "medyan": f(m.median()), "q90": f(m.quantile(0.9)),
                "saat": (s.dt.hour.value_counts().sort_index()).to_dict()}
    out = {"tur": {t: q(g.yayin) for t, g in H.groupby("tur")}, "site_tur": {f"{s}/{t}": q(g.yayin) for (s, t), g in H.groupby(["site", "tur"])}}
    G = H[(H.tur == "gun_ici") & H.veri_saati.notna()]
    if len(G):
        vs = pd.to_datetime(G.yayin.dt.strftime("%Y-%m-%d") + " " + G.veri_saati.astype(str))
        gec = (G.yayin - vs).dt.total_seconds() / 60
        gec = gec[(gec >= 0) & (gec < 600)]
        out["gun_ici_veri_saati"] = q(vs); out["gecikme_dk"] = {"n": int(len(gec)), "medyan": float(gec.median()) if len(gec) else None,
                                                               "q10": float(gec.quantile(0.1)) if len(gec) else None,
                                                               "q90": float(gec.quantile(0.9)) if len(gec) else None}
    return out


# ---------------------------------------------------------------- 8) İZLEME (fonksiyon; zamanlanmış DEĞİL)
def bi_izle_tur(gorulen: set, getir: Optional[Callable[[str], Optional[str]]] = None, k: int = 3,
                gecerli: Optional[set] = None) -> Tuple[pd.DataFrame, set]:
    """TEK TUR: hisse.net Google News site haritası (1 istek) -> başlığında / adresinde BofA geçen ve daha önce görülmemiş haberler -> her biri 1 istek
    -> ayrıştır -> BofA alım / satım ilk k. getir(url) -> metin (varsayılan: önbelleksiz, istekler arası >= 60 sn). Döner (tablo, güncel gorulen)."""
    if getir is None:
        def getir(u: str) -> Optional[str]:   # noqa: E306
            y = os.path.join(BI_YOL["is"], "izle", bi_onbellek_adi(u))
            return bi_getir(u, y, bekle=BI_AG["izle_bekle"], tazele=True)
    xml = getir(BI_HABER_HARITA) or ""
    yeni = []
    for blok in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>\s*(.*?)\s*</loc>", blok, re.S); bas = re.search(r"<news:title>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</news:title>", blok, re.S)
        tarih = re.search(r"<news:publication_date>\s*(.*?)\s*</news:publication_date>", blok, re.S)
        if not loc:
            continue
        u = loc.group(1).strip(); b = (bas.group(1).strip() if bas else "")
        if u in gorulen or not (BI_URL_KURUM.search(u) or re.search(r"bofa|bank of america|merrill", bi_norm(b))):
            continue
        yeni.append((u, b, tarih.group(1) if tarih else None))
    sat = []
    for u, b, t in yeni:
        h = getir(u); gorulen = gorulen | {u}
        if not h:
            continue
        M, rows = bi_ayristir(h, u, "hissenet", gecerli)
        for r in rows:
            if r["kurum"] == "BofA" and r["blok"] == 1 and r["sira"] <= k:
                sat.append({"yayin": M["yayin"], "tur": M["tur"], "veri_saati": M["veri_saati"], "baslik": M["baslik"], "url": u, **r})
    return pd.DataFrame(sat), gorulen


# ---------------------------------------------------------------- 9) ÖN KAYIT VE KAPI
def bi_sayim(Ld: pd.DataFrame, Hd: pd.DataFrame, takvim: pd.DatetimeIndex) -> Dict[str, Any]:
    """Ön kayıt için tanım sayımı (getiri yok): liste haberleri, veri günleri, eksik işlem günleri, dönem / olay sayıları."""
    L = bi_liste_hazirla(Ld, takvim)
    out: Dict[str, Any] = {"liste_haber": int(L.haber_id.nunique())}
    if not len(L):
        return out
    vg = L.dropna(subset=["veri_gunu"]); ilk, son = vg.veri_gunu.min(), vg.veri_gunu.max()
    aralik = takvim[(takvim >= ilk) & (takvim <= son)]
    al = set(vg[vg.yon == "alim"].veri_gunu); st = set(vg[vg.yon == "satim"].veri_gunu)
    out.update({"veri_gunu_ilk": str(ilk.date()), "veri_gunu_son": str(son.date()), "islem_gunu": int(len(aralik)),
                "alim_listesi_olan_gun": int(len(al)), "satim_listesi_olan_gun": int(len(st)),
                "alim_listesi_eksik_gun": int(len([t for t in aralik if t not in al])),
                "tur_haber": L.drop_duplicates("haber_id").tur.value_counts().to_dict(),
                "ay_alim_gun": vg[vg.yon == "alim"].drop_duplicates("veri_gunu").veri_gunu.dt.to_period("M").astype(str).value_counts().sort_index().to_dict()})
    D = bi_donemler(L, takvim, takvim[-1])
    out["donem"] = {"toplam": int(len(D)), "neden": D.neden.value_counts().to_dict() if len(D) else {},
                    "cikis_kesik_ici": int((D.cikis <= pd.Timestamp(BI_ESIK["kriz"]["kesik"])).sum()) if len(D) else 0}
    out["olay60_alim_ilk3"] = int(len(bi_olaylar60(L, takvim, "alim", 3)))
    return out


def bi_onkayit_metin(zaman: str, sayim: Dict[str, Any], kapsam: Dict[str, Any], fiyat: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or BI_ESIK
    return "\n".join([
        "# BOFA İZİ ÖN KAYDI (veri toplandıktan sonra, getiri hesaplanmadan önce)", "",
        f"{BI_SURUM}. Yazılma {zaman}. Bu dosya git'e işlenmeden `python BOFA_IZI.py kos` çalışmaz (mühür kapısı).", "",
        "## Soru", "",
        "BofA aracı kurum kodunun (ForInvest AKD, haber sitelerine yansıyan) alım listesinde ilk sıralarda görünen BIST hissesi, BofA'nın tuttuğu "
        "dönem boyunca (satış listesinde görünene kadar) ve 60 gün içinde, aynı gün aynı momentum x likidite hücresindeki öteki hisselerden iyi gidiyor mu?", "",
        "## Ana ölçü değişikliği (Cemal, 13.11.2026, ön kayıttan önce)", "",
        "Ana ölçü sabit 60 gün değil, 'BofA tutma dönemi'dir (BI_ESIK['donem']). FI_OLCUT 60 gün ölçüsü ikincil olarak kalır (BI_ESIK['olay60']).", "",
        "## Tanımlar ve eşikler (BI_ESIK, değişmez)", "",
        "```json", json.dumps(E, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
        "## Karar cümlesi (önceden yazılı)", "", E["karar"]["metin"], "", E["karar"]["coklu"], "",
        "## Ölçülecekler", "",
        "- ANA: tutma dönemleri (giriş ilk 3, çıkış satış ilk 5): n, süre dağılımı, dönem getirisi, en yüksek / en düşük, P(getiri >= +%50), "
        "P(-%30'a dokunma), geç kalma bedeli, eşli fark + ay kümeli %95 aralık, sıra, 10 yuva portföy vs 200 rastgele, alt dönem A / B.",
        "- Varyant çıkış (satış ilk 3, iki ardışık haber); alt kümeler çökmüş / diğer; TL sıralı listeler (duyarlılık).",
        "- İKİNCİL (FI_OLCUT 60 gün): alım ilk 3 (ana), ilk 1, ilk 5, ardışık 2+ gün ilk 3, çökmüş / diğer, satış ilk 3 (ters), haftalık alım ilk 3 (bilgi); "
        "her satırda r5, r20, P(+%50, 20g), P(-%30, 20g) ve eş katları. BİLGİ: gün içi listede aynı gün kapanıştan giriş.",
        "- Kriz dönemi (giriş >= 01.09.2026): dönemler tek tek (açık dönem bugüne, BofA hâlâ tutuyor mu).",
        "- En erken bilgi: liste haberlerinin yayın saati dağılımı (gün içi / gün sonu / haftalık, site), gün içi veri saati ve gecikme.", "",
        "## Veri ve tanım sayımı (sonuç içermez)", "",
        f"- Arşiv: {json.dumps(_bi_kayit({k: v for k, v in kapsam.items() if k not in ('liste_sha256', 'haber_sha256')}), ensure_ascii=False)}",
        f"- Fiyat: {json.dumps(_bi_kayit(fiyat), ensure_ascii=False)}",
        f"- Sayım: {json.dumps(_bi_kayit(sayim), ensure_ascii=False)}", "",
        "## Ön kayıttan önce görülenler (sonuç değil)", "",
        "- Arşiv kapsamı, liste türleri, ayrıştırma örnekleri; 27.10 / 28.10 / 2.11 PEKGY, 20-26.10 ODINE / GUNDG haberleri (iş tanımında; kriz dönemi, "
        "ana sonuca girmez). Getiri, eşli fark, dokunma oranı hesaplanmadı.",
        "- Alt dönem sınırı (BI_ESIK['yari']) veri aralığından seçildi (sonuçtan değil).", "",
        "## Bilinen yanlılıklar", "", E["yanlilik"], "",
        f"ESIK_SHA256: {bi_esik_sha(E)}",
        f"KOD_SHA256: {bi_kod_sha()}",
        f"LISTE_SHA256: {kapsam.get('liste_sha256')}",
        f"HABER_SHA256: {kapsam.get('haber_sha256')}", ""])


def _bi_veri_oku() -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    try:
        Ld = pd.read_csv(_bi_is("liste"), dtype={"veri_saati": str}, low_memory=False)
        Hd = pd.read_csv(_bi_is("haber"), dtype={"veri_saati": str}, low_memory=False)
        with open(_bi_is("kapsam"), encoding="utf-8") as f:
            K = json.load(f)
    except (OSError, ValueError) as ex:
        raise BiHata(f"arşiv yok / okunamadı ({ex}); önce `python BOFA_IZI.py topla`") from ex
    return Ld, Hd, K


def bi_onkayit(kl: Optional[str] = None) -> str:
    y = _bi_yol("onkayit", kl)
    if os.path.exists(y):
        raise BiHata(f"ön kayıt zaten var, üzerine yazılmaz: {y}")
    Ld, Hd, K = _bi_veri_oku()
    K["liste_sha256"] = bi_sha_dosya(_bi_is("liste")); K["haber_sha256"] = bi_sha_dosya(_bi_is("haber"))
    V, F = bi_fiyat(); takvim = bi_takvim(V)
    return _bi_yaz(y, bi_onkayit_metin(_bi_simdi(), bi_sayim(Ld, Hd, takvim), K, F))


def bi_onkayit_oku(yol: str) -> Dict[str, str]:
    try:
        with open(yol, encoding="utf-8") as f:
            t = f.read()
    except OSError as ex:
        raise BiHata(f"ön kayıt okunamadı: {ex}") from ex
    out = {}
    for k in ("ESIK_SHA256", "KOD_SHA256", "LISTE_SHA256", "HABER_SHA256"):
        m = re.search(rf"^{k}: ([0-9a-f]{{64}}|None)$", t, re.M)
        if not m:
            raise BiHata(f"ön kayıtta {k} yok")
        out[k] = m.group(1)
    return out


def bi_kapi(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None,
            liste_sha: Optional[str] = None, haber_sha: Optional[str] = None) -> Dict[str, Any]:
    """Ön kayıt kapısı: ön kayıt var + git'e işlenmiş ve değişmemiş + eşik mührü + liste / haber sha256 tutar + kod sha (ya da --sapma)."""
    E = E or BI_ESIK; y = _bi_yol("onkayit", kl)
    if not os.path.exists(y):
        raise BiHata("ön kayıt yok: önce `python BOFA_IZI.py onkayit` ve commit")
    O = bi_onkayit_oku(y); out: Dict[str, Any] = {"onkayit": y}
    if git:
        out["onkayit_git"] = bi_git_durum(y)
    if O["ESIK_SHA256"] != bi_esik_sha(E):
        raise BiHata("eşik mührü tutmuyor (BI_ESIK ön kayıttan sonra değişmiş)")
    if liste_sha is not None and O["LISTE_SHA256"] != liste_sha:
        raise BiHata("liste verisi ön kayıttakiyle aynı değil (bofa_liste.csv değişmiş)")
    if haber_sha is not None and O["HABER_SHA256"] != haber_sha:
        raise BiHata("haber tablosu ön kayıttakiyle aynı değil (bofa_haber.csv değişmiş)")
    ks = bi_kod_sha(); out["kod_sha256"] = ks; out["kod_ayni"] = ks == O["KOD_SHA256"]
    if not out["kod_ayni"]:
        if not sapma:
            raise BiHata("BOFA_IZI.py ön kayıttan sonra değişmiş: yalnız `--sapma GEREKCE` ile koşar (gerekçe sonuca yazılır)")
        out["sapma"] = sapma
    out["esik_sha256"] = O["ESIK_SHA256"]
    return out


# ---------------------------------------------------------------- 10) KOŞU
def _bi_kriz_tablo(Yd: pd.DataFrame, A: Dict[str, Any], son: pd.Timestamp) -> List[Dict[str, Any]]:
    ti = {t: i for i, t in enumerate(A["tarih"])}; sat = []
    alan = ("hisse", "veri_gunu", "acilis_yayin", "acilis_tur", "acilis_sira", "bofa_maliyet", "giris", "cikis", "neden", "cikis_yayin",
            "ret", "max", "min", "esli", "fark", "gun", "gec")
    for r in Yd.to_dict(orient="records"):
        d = ti.get(pd.Timestamp(r["giris"])); j = A["kol"].get(r["hisse"])
        x = {k: r.get(k) for k in alan}; x["acik"] = r.get("neden") == "acik_veri_sonu"
        if d is not None and j is not None and np.isfinite(A["Op"][d, j]):
            o = A["Op"][d, j]; x["giris_fiyat"] = o
            x["hacim0"] = bool("Vv" in A and not (A["Vv"][d, j] > 0))   # giriş günü hacim 0: askı / bayat Yahoo fiyatı (yalnız işaret)
            x["son_kapanis"] = A["Cf"][-1, j]; x["bugune"] = A["Cf"][-1, j] / o - 1
            with np.errstate(all="ignore"):
                x["bugune_max"] = np.nanmax(A["Hh"][d:, j]) / o - 1; x["bugune_min"] = np.nanmin(A["Ll"][d:, j]) / o - 1
                g = A["ok"][d]; x["bist_bugune"] = float(np.nanmean(A["Cf"][-1, g] / A["Op"][d, g] - 1))
        sat.append(x)
    return sat


def bi_kos(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None,
           V: Optional[Dict[str, pd.DataFrame]] = None, F: Optional[Dict[str, Any]] = None,
           Ld: Optional[pd.DataFrame] = None, Hd: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    import FON_IZI as FI  # noqa: WPS433
    E = E or BI_ESIK
    if Ld is None:
        Ld, Hd, _ = _bi_veri_oku()
        Kp = bi_kapi(kl, git, sapma, E, bi_sha_dosya(_bi_is("liste")), bi_sha_dosya(_bi_is("haber")))
    else:
        Kp = bi_kapi(kl, git, sapma, E)
    t0 = _bi_simdi(); bilog.info("kapı geçti (mühür %s)", Kp["esik_sha256"][:12])
    if V is None:
        V, F = bi_fiyat()
    takvim = bi_takvim(V); kes = E["kriz"]["kesik"]; yari = E["yari"]["sinir"]
    P = FI.fi_olcut_panel(V); A = bi_panel(V)
    son = takvim[-1]
    sonuc: Dict[str, Any] = {"surum": BI_SURUM, "baslangic": t0, "kapi": Kp, "fiyat": F, "sayim": bi_sayim(Ld, Hd, takvim), "esik_sha": bi_esik_sha(E)}
    L = bi_liste_hazirla(Ld, takvim, None); Ll_ = bi_liste_hazirla(Ld, takvim, "lot"); Lt = bi_liste_hazirla(Ld, takvim, "TL")
    Ly = bi_liste_hazirla(Ld, takvim, None, yapisal=True)
    kesT = pd.Timestamp(kes)
    # ANA: tutma dönemleri
    dons: Dict[str, pd.DataFrame] = {}
    for ad, LL, var in (("ana", L, False), ("varyant", L, True), ("lot", Ll_, False), ("tl", Lt, False), ("yapisal", Ly, False)):
        D = bi_donemler(LL, takvim, son, E, varyant=var)
        dons[ad] = bi_donem_olc(A, D, E["alt_kume"]["cokmus"]) if len(D) else D
    sonuc["donem"] = {}
    for ad, Y in dons.items():
        if not len(Y):
            sonuc["donem"][ad] = {"n": 0}; continue
        Yk = Y[(pd.to_datetime(Y.cikis) <= kesT) & (Y.neden != "acik_veri_sonu")]
        o = bi_donem_ozet(Yk, yari); o["toplam_donem"] = int(len(Y)); o["giris_hacim0"] = int(Yk.hacim0.fillna(False).astype(bool).sum())
        o["kesik_disi"] = int(((pd.to_datetime(Y.giris) <= kesT) & ~Y.index.isin(Yk.index)).sum())
        o["kriz_sonrasi_giris"] = int((pd.to_datetime(Y.giris) > kesT).sum())
        sonuc["donem"][ad] = o
        if ad == "ana":
            sonuc["karar"] = bi_donem_karar(o, E)
            sonuc["donem"]["ana_fi_donem"] = {d: bi_donem_ozet(Yk[(pd.to_datetime(Yk.giris) >= pd.Timestamp(a)) & (pd.to_datetime(Yk.giris) <= pd.Timestamp(b))], yari)
                                              for d, a, b in FI.FI_OLCUT["donem"]}
            for k, m in (("cokmus", Yk.cokmus == True), ("diger", Yk.cokmus == False), ("satis_cikisli", Yk.neden == "satis")):  # noqa: E712
                sonuc["donem"][f"ana_{k}"] = bi_donem_ozet(Yk[m.fillna(False).astype(bool)], yari)
    # YABANCI KODLAR (aynı tutma dönemi ölçüsü) + TOPLU + BH
    sonuc["kurum"] = {}; pk: Dict[str, float] = {}; kurum_don = []
    for kod in [k for k, _ in BI_KURUM] + ["TOPLU"]:
        birim = "hepsi"
        if kod == "TOPLU":
            LL = bi_liste_hazirla(Ld, takvim, None, None)
        else:
            if not len(Ld[(Ld.kurum == kod) & (Ld.blok == 1)]):
                sonuc["kurum"][kod] = {"veri": "veri yok"}; continue
            LL = bi_liste_hazirla(Ld, takvim, None, kod)
        Dk = bi_donemler(LL, takvim, son, E) if len(LL) else pd.DataFrame()
        if not len(Dk):
            sonuc["kurum"][kod] = {"veri": "dönem yok", "birim": birim, "liste_haber": int(LL.haber_id.nunique()) if len(LL) else 0}; continue
        Yk_ = bi_donem_olc(A, Dk, E["alt_kume"]["cokmus"])
        kurum_don.append(Yk_.drop(columns=["_esler"], errors="ignore").assign(tanim="kurum_" + kod))
        Yc = Yk_[(pd.to_datetime(Yk_.cikis) <= kesT) & (Yk_.neden != "acik_veri_sonu")]
        o = bi_donem_ozet(Yc, yari); o.update({"birim": birim, "liste_haber": int(LL.haber_id.nunique()), "toplam_donem": int(len(Yk_)),
                                              "ilk": str(LL.yayin.min())[:10], "son": str(LL.yayin.max())[:10]})
        o["karar"] = bi_donem_karar(o, E)
        Ykr = Yk_[pd.to_datetime(Yk_.giris) >= pd.Timestamp("2026-09-01")]
        o["kriz_acik"] = [r for r in _bi_kriz_tablo(Ykr, A, son) if r.get("acik")] if len(Ykr) else []
        o["kriz_n"] = int(len(Ykr))
        sonuc["kurum"][kod] = o
        if kod != "TOPLU" and o.get("n", 0) >= 1:
            pk[kod] = o.get("p_boot", np.nan)
    bh = bi_bh(pk, 0.10)
    for kod, o in sonuc["kurum"].items():
        if "n" not in o:
            continue
        o["bh_red"] = bh.get(kod) if kod != "TOPLU" else None
        if kod != "TOPLU":
            o["karar_bh"] = "iz adayı" if (o["karar"]["karar"] != "kanıt yok" and bh.get(kod)) else "kanıt yok"
    sonuc["bh_m"] = len(pk)
    # İKİNCİL: FI_OLCUT 60 gün
    sonuc["olay60"] = {}
    tanim = [("alim_ilk3", L, "alim", 3, 1), ("alim_ilk1", L, "alim", 1, 1), ("alim_ilk5", L, "alim", 5, 1), ("alim_ardisik2", L, "alim", 3, 2),
             ("satim_ilk3", L, "satim", 3, 1), ("lot_alim_ilk3", Ll_, "alim", 3, 1), ("tl_alim_ilk3", Lt, "alim", 3, 1)]
    olaylar = []
    for ad, LL, yon, k, ard in tanim:
        X = bi_olaylar60(LL, takvim, yon, k, ard, E["olay60"]["tekil_gun"])
        Y = bi_olay_olc(P, A, X, kes) if len(X) else X
        Yk = Y[pd.to_datetime(Y.giris) <= kesT] if len(Y) else Y
        sonuc["olay60"][ad] = bi_olay_ozet(Yk, yari) if len(Yk) else {"n_olay": 0}
        if ad == "alim_ilk3" and len(Yk):
            sonuc["karar60"] = bi_olay_karar(sonuc["olay60"][ad])
            sonuc["olay60"]["alim_ilk3_fi_donem"] = {d: bi_olay_ozet(Yk[(pd.to_datetime(Yk.giris) >= pd.Timestamp(a)) & (pd.to_datetime(Yk.giris) <= pd.Timestamp(b))], yari)
                                                     for d, a, b in FI.FI_OLCUT["donem"]}
            for kk, m in (("cokmus", Yk.cokmus == True), ("diger", Yk.cokmus == False)):  # noqa: E712
                sonuc["olay60"][f"alim_ilk3_{kk}"] = bi_olay_ozet(Yk[m.fillna(False).astype(bool)], yari)
            # BİLGİ: gün içi listeden aynı gün kapanış girişi
            gi = Yk[Yk.tur == "gun_ici"] if "tur" in Yk else Yk.iloc[:0]
            ti = {t: i for i, t in enumerate(A["tarih"])}; rr = []
            for r in gi.itertuples():
                d0 = ti.get(pd.Timestamp(r.veri_gunu)); j = A["kol"].get(r.hisse)
                if d0 is None or j is None or d0 + 61 >= len(A["tarih"]) or A["tarih"][d0 + 61] > kesT or pd.Timestamp(r.yayin).strftime("%H:%M") >= "18:00":
                    continue
                c0 = A["Cf"][d0, j]
                rr.append({"r5k": A["Cf"][d0 + 5, j] / c0 - 1, "r20k": A["Cf"][d0 + 20, j] / c0 - 1, "r60k": A["Cf"][d0 + 60, j] / c0 - 1,
                           "r60_acilis": r.r60})
            R = pd.DataFrame(rr)
            sonuc["olay60"]["bilgi_ayni_gun_kapanis"] = {"n": int(len(R)), **({k: float(R[k].mean()) for k in R} if len(R) else {})}
        if len(Y):
            olaylar.append(Y.drop(columns=["_esler"], errors="ignore").assign(tanim=ad))
    Xh = L[(L.tur == "haftalik") & (L.yon == "alim") & (L.sira <= 3)].dropna(subset=["giris"])
    Xh = bi_tekil(Xh, takvim, 60)
    Yh = bi_olay_olc(P, A, Xh, kes) if len(Xh) else Xh
    sonuc["olay60"]["haftalik_alim_ilk3"] = bi_olay_ozet(Yh[pd.to_datetime(Yh.giris) <= kesT], yari) if len(Yh) else {"n_olay": 0}
    # KRİZ DÖNEMİ (BİLGİ)
    Y = dons["ana"]
    Yb = Y[pd.to_datetime(Y.giris) >= pd.Timestamp("2026-09-01")] if len(Y) else Y
    sonuc["kriz"] = {"son_gun": str(son.date()), "donemler": _bi_kriz_tablo(Yb, A, son) if len(Yb) else []}
    if len(Yb):
        sonuc["kriz"]["ozet"] = {"n": int(len(Yb)), "acik": int((Yb.neden == "acik_veri_sonu").sum()), "ort_ret": float(Yb.ret.mean()),
                                 "medyan_ret": float(Yb.ret.median()), "ort_esli": float(Yb.esli.mean()), "ort_fark": float(Yb.fark.mean()),
                                 "p_min30": float((Yb["min"] <= -0.30).mean()), "p_ret50": float((Yb.ret >= 0.5).mean())}
    Ok = [x for x in olaylar if len(x)]
    if Ok:
        Z = pd.concat(Ok, ignore_index=True)
        sonuc["kriz"]["alim_ilk3_olay"] = _bi_kayit(Z[(Z.tanim == "alim_ilk3") & (pd.to_datetime(Z.giris) > kesT)][
            [c for c in ("hisse", "veri_gunu", "yayin", "liste_sira", "tur", "giris", "r5", "r20") if c in Z]].sort_values("giris"))
    # EN ERKEN BİLGİ
    sonuc["saat"] = bi_saat_ozet(Hd, Ld)
    sonuc["bitis"] = _bi_simdi()
    os.makedirs(BI_YOL["is"], exist_ok=True)
    pd.concat([d.drop(columns=["_esler"], errors="ignore").assign(tanim=k) for k, d in dons.items() if len(d)] + kurum_don,
              ignore_index=True).to_csv(_bi_is("donem"), index=False)
    if Ok:
        pd.concat(Ok, ignore_index=True).to_csv(_bi_is("olay"), index=False)
    _bi_json(_bi_yol("sonuc", kl), sonuc); _bi_yaz(_bi_yol("rapor", kl), bi_rapor_md(_bi_kayit(sonuc), E))
    return sonuc


# ---------------------------------------------------------------- 11) RAPOR
def _p(x: Any, n: int = 1) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    if not np.isfinite(v):
        return "—"
    return f"{v * 100:+.{n}f}%".replace(".", ",")


def _o(x: Any, n: int = 0) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return f"%{v * 100:.{n}f}".replace(".", ",") if np.isfinite(v) else "—"


def _k(x: Any) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return f"{v:.2f}".replace(".", ",") if np.isfinite(v) else "—"


def bi_rapor_md(S: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or BI_ESIK; sy = S.get("sayim", {}); D = S.get("donem", {}); O6 = S.get("olay60", {}); kr = S.get("karar", {}); k6 = S.get("karar60", {})
    sat = ["# BofA alım listesi izi — sonuç (13 Kasım 2026)", "",
           f"Soru: BofA (AKD kodu) alım listesinde ilk 3'te görünen BIST hissesi, BofA tutarken ve 60 gün içinde benzer hisselerden iyi gidiyor mu? "
           f"Veri: {sy.get('liste_haber', '—')} BofA liste haberi, veri günleri {sy.get('veri_gunu_ilk', '—')} – {sy.get('veri_gunu_son', '—')} "
           f"({sy.get('islem_gunu', '—')} işlem günü; {sy.get('alim_listesi_eksik_gun', '—')} günde alım listesi yok). Fon krizi kuralı: çıkışı / penceresi "
           f"31.08.2026'yı aşan ana sonuca girmez.", "",
           f"**KARAR (ana, tutma dönemi): {kr.get('karar', '—')}**" + (f" — tutmayan: {'; '.join(kr.get('tutmayan', []))}" if kr.get("tutmayan") else ""), "",
           f"**İkincil (FI_OLCUT 60 gün, alım ilk 3): {k6.get('karar', '—')}**" + (f" — tutmayan: {'; '.join(k6.get('tutmayan', []))}" if k6.get("tutmayan") else ""), "",
           *bi_ozet_satirlari(S), "",
           "## 1. BofA tutma dönemi (giriş: alım ilk 3 haberinden sonraki açılış; çıkış: satış ilk 5 haberinden sonraki açılış)", "",
           "| satır | n | süre medyan (gün) | dönem getirisi ort. | eş ort. | eşli fark ort. [%95] | sıra | P(getiri >= +%50) | P(-%30 dokunma) | portföy / rastgele %90 | A / B fark |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    adlar = {"ana": "ANA", "varyant": "çıkış: satış ilk 3, 2 ardışık", "lot": "yalnız lot sıralı listeler", "tl": "yalnız TL sıralı listeler",
             "yapisal": "düz yazı hariç", "ana_cokmus": "ana: çökmüş (<= -%60)",
             "ana_diger": "ana: diğer", "ana_satis_cikisli": "ana: yalnız satışla kapanan"}
    for k, ad in adlar.items():
        o = D.get(k) or {}
        if not o.get("n"):
            sat.append(f"| {ad} | 0 | | | | | | | | | |"); continue
        sat.append(f"| {ad} | {o['n']} | {_k(o.get('gun_medyan'))} | {_p(o.get('ort_ret'))} | {_p(o.get('ort_esli'))} | {_p(o.get('ort_fark'))} "
                   f"[{_p(o.get('alt95'))}, {_p(o.get('ust95'))}] | {_k(o.get('sira'))} | {_o(o.get('p_ret50'))} | {_o(o.get('p_min30'))} | "
                   f"{_p(o.get('portfoy'), 0)} / {_p(o.get('portfoy_esli_p90'), 0)} | {_p((o.get('yari_A') or {}).get('ort_fark'))} / "
                   f"{_p((o.get('yari_B') or {}).get('ort_fark'))} |")
    a = D.get("ana") or {}
    sat += ["", f"Ana: toplam {a.get('toplam_donem', '—')} dönem; kesik içinde biten {a.get('n', '—')}; kesiği aşan {a.get('kesik_disi', '—')}, "
                f"kriz sonrası açılan {a.get('kriz_sonrasi_giris', '—')}. Kapanış nedeni: {a.get('neden', {})}. Süre (gün) %10/25/50/75/90: "
                f"{a.get('gun_q', '—')}. Giriş günü hacmi 0 olan (bayat fiyat) dönem: {a.get('giris_hacim0', '—')}. Geç kalma (bizim giriş / BofA maliyeti - 1) medyan {_p(a.get('gec_medyan'))} (n {a.get('gec_n', '—')}). "
                f"Dönem içi ort. en yüksek {_p(a.get('ort_max'))}, en düşük {_p(a.get('ort_min'))}.", "",
            "FI_OLCUT dönem kırılımı (BİLGİ): " + "; ".join(
                f"tutma dönemi {d}: n {(o or {}).get('n', 0)}, eşli fark {_p((o or {}).get('ort_fark'))} [{_p((o or {}).get('alt95'))}, {_p((o or {}).get('ust95'))}]"
                for d, o in (D.get("ana_fi_donem") or {}).items()) + " | " + "; ".join(
                f"60 gün {d}: n {((o or {}).get('fi') or {}).get('n', 0)}, eşli fark {_p(((o or {}).get('fi') or {}).get('ort_fark'))} "
                f"[{_p(((o or {}).get('fi') or {}).get('alt95'))}, {_p(((o or {}).get('fi') or {}).get('ust95'))}]"
                for d, o in (O6.get("alim_ilk3_fi_donem") or {}).items()) + ".", "",
            "## 2. Olasılık tablosu (ikincil, 60 gün ölçütü; 20 gün olasılıkları dokunma, eş = aynı gün aynı hücre)", "",
            "| olay | n (20g) | P(+%50, 20g) | kat | P(-%30, 20g) | kat | r20 ort. / eş | n (60g) | 60g eşli fark [%95] | sıra | portföy / rastgele %90 |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    adlar6 = {"alim_ilk3": "alım ilk 3 (ana)", "alim_ilk1": "alım ilk 1", "alim_ilk5": "alım ilk 5", "alim_ardisik2": "ardışık 2+ gün ilk 3",
              "alim_ilk3_cokmus": "alım ilk 3, çökmüş", "alim_ilk3_diger": "alım ilk 3, diğer", "satim_ilk3": "SATIŞ ilk 3 (ters)",
              "lot_alim_ilk3": "lot listesi alım ilk 3", "tl_alim_ilk3": "TL listesi alım ilk 3", "haftalik_alim_ilk3": "haftalık alım ilk 3 (bilgi)"}
    for k, ad in adlar6.items():
        o = O6.get(k) or {}; H = o.get("fi") or {}
        sat.append(f"| {ad} | {o.get('n20', 0)} | {_o(o.get('p_up50'))} | {_k(o.get('kat_up50'))} | {_o(o.get('p_dn30'))} | {_k(o.get('kat_dn30'))} | "
                   f"{_p(o.get('r20'))} / {_p(o.get('b_r20'))} | {H.get('n', 0)} | {_p(H.get('ort_fark'))} [{_p(H.get('alt95'))}, {_p(H.get('ust95'))}] | "
                   f"{_k(H.get('sira'))} | {_p(H.get('portfoy'), 0)} / {_p(H.get('portfoy_esli_p90'), 0)} |")
    sat += ["", f"## 2b. Yabancı kodlar, aynı tutma dönemi ölçüsü (BH q = 0,10, m = {S.get('bh_m', '—')})", "",
            "| kod | birim | liste haberi | n dönem | süre medyan | getiri medyan / ort. | P(>= +%50) | P(-%30) | eşli fark [%95] | p | BH | karar |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for kod, o in (S.get("kurum") or {}).items():
        if "n" not in o:
            sat.append(f"| {kod} | {o.get('birim', '')} | {o.get('liste_haber', 0)} | {o.get('veri')} | | | | | | | | |"); continue
        kk = o.get("karar_bh") or (o.get("karar") or {}).get("karar", "—")
        sat.append(f"| {kod} | {o.get('birim')} | {o.get('liste_haber')} | {o.get('n')} | {_k(o.get('gun_medyan'))} | {_p(o.get('medyan_ret'))} / "
                   f"{_p(o.get('ort_ret'))} | {_o(o.get('p_ret50'))} | {_o(o.get('p_min30'))} | {_p(o.get('ort_fark'))} [{_p(o.get('alt95'))}, "
                   f"{_p(o.get('ust95'))}] | {_k(o.get('p_boot'))} | {'red' if o.get('bh_red') else ('—' if kod == 'TOPLU' else 'yok')} | {kk} |")
    acik = [(kod, r) for kod, o in (S.get("kurum") or {}).items() if kod != "TOPLU" for r in (o.get("kriz_acik") or [])]
    if acik:
        sat += ["", "Kriz dönemi AÇIK dönemler (kod hâlâ satış listesinde ilk 5'te göstermedi; bugüne getiri):", "",
                "| kod | hisse | ilk alım haberi | giriş | bugüne | en düşük | BIST aynı gün -> bugün |", "|---|---|---|---|---|---|---|"]
        for kod, r in sorted(acik, key=lambda x: (x[0], str(x[1].get("giris"))))[:15]:
            sat.append(f"| {kod} | {r.get('hisse')}{' (giriş hacim 0: bayat fiyat)' if r.get('hacim0') else ''} | {str(r.get('acilis_yayin'))[:16]} | {str(r.get('giris'))[:10]} | {_p(r.get('bugune'))} | "
                       f"{_p(r.get('bugune_min'))} | {_p(r.get('bist_bugune'))} |")
        if len(acik) > 15:
            sat.append(f"| … {len(acik) - 15} daha (bofa_sonuc.json 'kurum' / 'kriz_acik') | | | | | | |")
    b = O6.get("bilgi_ayni_gun_kapanis") or {}
    sat += ["", f"BİLGİ (gün içi listede aynı gün kapanıştan giriş, n {b.get('n', 0)}): r5 {_p(b.get('r5k'))}, r20 {_p(b.get('r20k'))}, r60 {_p(b.get('r60k'))} "
                f"(aynı olayların ertesi açılış r60'ı {_p(b.get('r60_acilis'))}).", "",
            "## 3. Kriz dönemi (giriş >= 01.09.2026; BİLGİ, karara girmez)", ""]
    kz = S.get("kriz", {}); oz = kz.get("ozet") or {}
    if oz:
        sat.append(f"{oz.get('n')} dönem ({oz.get('acik')} hâlâ açık: BofA satış listesinde ilk 5'te görülmedi). Ort. dönem getirisi {_p(oz.get('ort_ret'))} "
                   f"(medyan {_p(oz.get('medyan_ret'))}), eş ort. {_p(oz.get('ort_esli'))}, eşli fark {_p(oz.get('ort_fark'))}; P(-%30 dokunma) "
                   f"{_o(oz.get('p_min30'))}, P(>= +%50) {_o(oz.get('p_ret50'))}. Son veri {kz.get('son_gun')} (son bar gün içi olabilir).")
    sat += ["", "| hisse | ilk alım haberi | sıra | BofA maliyet | giriş | çıkış / durum | dönem getirisi | eş | en düşük | en yüksek | bugüne | BIST aynı gün -> bugün |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    on = ("PEKGY", "ODINE", "GUNDG", "KTLEV", "PAHOL", "TEHOL", "KARCL")
    T = sorted(kz.get("donemler", []), key=lambda r: (r.get("hisse") not in on, str(r.get("giris"))))
    for r in T[:15]:
        dur = "AÇIK (BofA tutuyor)" if r.get("acik") else f"{str(r.get('cikis'))[:10]} ({r.get('neden')})"
        sat.append(f"| {r.get('hisse')}{' (giriş günü hacim 0: bayat fiyat)' if r.get('hacim0') else ''} | {str(r.get('acilis_yayin'))[:16]} ({r.get('acilis_tur')}) | {r.get('acilis_sira')} | {_k(r.get('bofa_maliyet'))} | "
                   f"{str(r.get('giris'))[:10]} | {dur} | {_p(r.get('ret'))} | {_p(r.get('esli'))} | {_p(r.get('min'))} | {_p(r.get('max'))} | "
                   f"{_p(r.get('bugune'))} | {_p(r.get('bist_bugune'))} |")
    if len(T) > 15:
        sat.append(f"| … {len(T) - 15} dönem daha (bofa_sonuc.json 'kriz') | | | | | | | | | | | |")
    s = S.get("saat", {}); tu = s.get("tur", {})
    sat += ["", "## 4. En erken bilgi (hafta içi yayın saatleri, TR)", ""]
    for t, ad in (("gun_ici", "gün içi liste"), ("gun_sonu", "gün sonu liste"), ("haftalik", "haftalık")):
        q = tu.get(t) or {}
        if q.get("n"):
            sat.append(f"- {ad}: n {q['n']}, en erken {q['en_erken']}, %10 {q['q10']}, medyan {q['medyan']}, %90 {q['q90']}.")
    vq = s.get("gun_ici_veri_saati") or {}; gk = s.get("gecikme_dk") or {}
    if vq.get("n"):
        sat.append(f"- Gün içi listenin veri saati: medyan {vq['medyan']} (en erken {vq['en_erken']}); yayın gecikmesi medyan {_k(gk.get('medyan'))} dk "
                   f"(%10 {_k(gk.get('q10'))}, %90 {_k(gk.get('q90'))}).")
    sat += ["- Ücretsiz en erken yol: hisse.net Google News site haritası (sitemaps/news-sitemap.xml; son ~100 haber, yayın dakikasıyla; hisse.net'te "
            "RSS yok, /rss 404). Rota Borsa'nın RSS'i var (rotaborsa.com/feed/), YatırımX'in yok. `BOFA_IZI.bi_izle_tur` hisse.net haritasını tek tur "
            "çeker, dakikada en çok 1 istek; zamanlanmadı. Ücretli AKD (ForInvest, Matriks) seans içinde canlıdır; abonelik başlatılmadı.", "",
            "## 5. Sınırlar", "", E["yanlilik"], "",
            f"Arşiv haber sitelerinin yazdığı listelerdir ({sy.get('veri_gunu_ilk', '—')} öncesi yok; liste çoğunlukla ilk 5 / ilk 10). Tek pazar "
            "(BIST): FI_OLCUT'un ABD / Avrupa karar hücreleri bu veride yoktur. Ana dışındaki satırlar çoklu denemedir.", "",
            f"Mühür {S.get('esik_sha', '')[:12]}; kapı {json.dumps(S.get('kapi', {}).get('onkayit_git', {}), ensure_ascii=False)}"
            + (f"; SAPMA: {S['kapi']['sapma']}" if S.get("kapi", {}).get("sapma") else "") + ".", ""]
    return "\n".join(sat)


def bi_ozet_satirlari(S: Dict[str, Any]) -> List[str]:
    """Raporun başındaki düz dil özet (bulgu cümleleri, yalnız sonuç JSON'undaki sayılardan)."""
    D = S.get("donem", {}); O6 = S.get("olay60", {}); KU = S.get("kurum", {}); a = D.get("ana") or {}; lt = D.get("lot") or {}
    i3 = O6.get("alim_ilk3") or {}; l3 = O6.get("lot_alim_ilk3") or {}; s3 = O6.get("satim_ilk3") or {}; c3 = O6.get("alim_ilk3_cokmus") or {}
    H = KU.get("HSBC") or {}; tp = KU.get("TOPLU") or {}; kz = (S.get("kriz") or {}).get("ozet") or {}; tu = (S.get("saat") or {}).get("tur") or {}
    f = lambda o: f"{_p(o.get('ort_fark'))} [{_p(o.get('alt95'))}, {_p(o.get('ust95'))}]"  # noqa: E731
    g = lambda o: f"{_p((o.get('fi') or {}).get('ort_fark'))} [{_p((o.get('fi') or {}).get('alt95'))}, {_p((o.get('fi') or {}).get('ust95'))}]"  # noqa: E731
    return ["## Özet (düz dil)", "",
            f"- BofA alım listesinde ilk 3'e giren hisse, BofA satış listesinde ilk 5'e girene kadar (medyan {_k(a.get('gun_medyan'))} işlem günü) "
            f"benzer hisselerden ortalama {f(a)} ayrıştı (n {a.get('n', '—')}); 2023-24'te {_p((a.get('yari_A') or {}).get('ort_fark'))}, "
            f"2025-26'da {_p((a.get('yari_B') or {}).get('ort_fark'))}. Fark sıfırdan ayrılmıyor.",
            f"- 60 gün (FI_OLCUT): alım ilk 3 eşli fark {g(i3)} (n {(i3.get('fi') or {}).get('n', '—')}); 20 günde +%50'ye dokunma {_o(i3.get('p_up50'))} "
            f"(eşlerin {_k(i3.get('kat_up50'))} katı), -%30'a dokunma {_o(i3.get('p_dn30'))} ({_k(i3.get('kat_dn30'))} kat).",
            f"- Lot sıralı listeler (PEKGY tipi kuruş hisseler, çoğu hisse.net): 60 günde eşli fark {g(l3)} (n {(l3.get('fi') or {}).get('n', '—')}); "
            f"tutma döneminde {f(lt)} (n {lt.get('n', '—')}). İşaret ters: bu listelerde öne çıkan hisse benzerlerinden kötü gitmiş.",
            f"- Çökmüş hisse (250 gün tepesinden -%60): 60 gün eşli fark {g(c3)} (n {(c3.get('fi') or {}).get('n', '—')}), 20 günde -%30'a dokunma "
            f"{_o(c3.get('p_dn30'))} ({_k(c3.get('kat_dn30'))} kat). Örneklem küçük.",
            f"- Ters sınama (satış ilk 3): 60 gün eşli fark {g(s3)}: satış listesi de bir şey söylemiyor.",
            f"- Öteki yabancı kodlar: HSBC tutma dönemi {f(H)} (n {H.get('n', '—')}); bütün kodlar birlikte {f(tp)} (n {tp.get('n', '—')}). "
            f"Citi, Deutsche, JPM, Goldman, UBS, Merrill, MS, Barclays, CS: arşivde liste yok ya da n < 30.",
            f"- Kriz dönemi (Eylül-Kasım 2026, BİLGİ): {kz.get('n', '—')} BofA dönemi, {kz.get('acik', '—')} hâlâ açık; ortalama dönem getirisi "
            f"{_p(kz.get('ort_ret'))}, eşli fark {_p(kz.get('ort_fark'))}.",
            f"- En erken: gün içi BofA listesi medyan {(tu.get('gun_ici') or {}).get('medyan', '—')}'te (veri saati ~12:30-13:00), gün sonu listesi medyan "
            f"{(tu.get('gun_sonu') or {}).get('medyan', '—')}'da yayımlanıyor; ücretsiz kaynakla en erken işlem gün içi haberle aynı gün kapanışta ya da "
            "ertesi açılışta mümkün."]


def bi_rapor(kl: Optional[str] = None) -> str:
    try:
        with open(_bi_yol("sonuc", kl), encoding="utf-8") as f:
            S = json.load(f)
    except (OSError, ValueError) as ex:
        raise BiHata(f"sonuç okunamadı: {ex}") from ex
    return _bi_yaz(_bi_yol("rapor", kl), bi_rapor_md(S))


# ---------------------------------------------------------------- 13) BofA KÂRI (A, betimleyici) VE HABER SONRASI YOL (B, ön kayıtlı) — 13 Kasım 2026
# Cemal (13.11.2026): 'BofA bir hissede %40-80 zarar etmez; senin mantığın bunu alıyor mu? Bana bir yol gösterecekse ölç.' Önceki ölçüm (BI_ESIK)
# BofA'nın kârını değil listedeki hisselerin bizim girişimizden getirisini ölçtü. Bu bölüm (A) BofA'nın yayımlanan ortalama maliyetinden getirisini
# betimler, (B) haber anında bilinen 6 koşulla 'Cemal haberden sonra girerse' yolunu ön kayıtlı karar kuralıyla sınar. Yukarıdaki bölümlere dokunmaz.
BK_ETIKET = "bofa_kar_20261113"
BK_SURUM = ("BOFA_IZI KÂR v1.0 (bofa_kar_20261113): BofA'nın kendi maliyetinden getirisi (A, betimleyici) + haber sonrası giriş yolu, 6 koşul "
            "(B, ön kayıtlı)")
BK_DOSYA: Dict[str, str] = {"onkayit": "BOFA_KAR_ON_KAYIT.md", "sonuc": "bofa_kar_sonuc.json", "rapor": "BOFA_KAR_RAPOR.md",
                            "temiz": "kar_temiz.csv.gz", "a": "kar_a.csv.gz", "fifo": "kar_fifo.csv.gz", "b": "kar_b.csv.gz",
                            "b60": "kar_b60.csv.gz", "tetik": "kar_tetik.csv.gz"}
BK_KOSUL: Tuple[str, ...] = ("K1", "K2", "K3", "K4", "K5", "K6")
BK_SATIR: Tuple[str, ...] = BK_KOSUL + ("TUM",)
BK_YOLLAR: Tuple[Tuple[str, str, str], ...] = (("G1C1", "g1", "c1"), ("G1C2", "g1", "c2"), ("G2C1", "g2", "c1"), ("G2C2", "g2", "c2"))

# ---------------------------------------------------------------- ÖN KAYITLI TANIM VE EŞİKLER (sha256 mührü BOFA_KAR_ON_KAYIT.md'de; sonuçtan sonra değişmez)
BK_ESIK: Dict[str, Any] = {
    "surum_etiket": BK_ETIKET,
    "soru": "A) BofA yayımlanan kendi ortalama maliyetinden kâr ediyor mu, nerede ediyor (betimleyici)? B) BofA'nın alımları haber yayımlandığı anda "
            "bilinen bilgiyle ayrılabilir mi ve Cemal haber saatinden sonra girerek bunun bir kısmını yakalayabilir mi (karar)? Kaynak: Cemal 13.11.2026 "
            "itirazı ('BofA bir hissede %40-80 zarar etmez'; listedeki 'BofA' bir aracı kurum akışıdır, liste ilk 5-10 ile sınırlıdır).",
    "kapsam": {"kurum": "BofA", "blok": 1, "tur": ["gun_ici", "gun_sonu", "haftalik"], "yon": ["alim", "satim"],
               "tanim": "bofa_liste.csv'de kurum BofA, haberdeki ilk blok (blok 1), tür gün içi / gün sonu / haftalık (aylık dışarıda)"},
    "temizlik": {"maliyet_bant": [0.97, 1.03], "lot_min": 1000, "lot_tl_min": 100000.0, "tl_min": 1000000.0, "haftalik_bant_gun": 5,
                 "neden_sira": ["veri_gunu_yok", "fiyat_paneli_yok", "veri_gunu_bar_yok", "net_yok", "esik_alti", "maliyet_bant_disi"],
                 "tanim": "satır GEÇERLİ <=> (1) veri günü belirlenebilir (BOFA_IZI.bi_veri_gunu; haftalık listede de aynı işlev: yayın günü ya da önceki "
                          "işlem günü); (2) hisse fiyat panelinde (Yahoo önbelleği, bi_panel) var; (3) veri günü barı var (H, L, C sonlu); (4) net sayısı "
                          "yazılı; (5) birim lot ise |net| >= 1.000 lot VE |net| x fiyat >= 100.000 TL (fiyat = maliyet, maliyet yoksa veri günü kapanışı); "
                          "birim TL ise |net| >= 1.000.000 TL; (6) maliyet yazılıysa veri günü [Low x 0,97, High x 1,03] aralığında (haftalık listede "
                          "veri günü ve önceki 4 işlem gününün en düşük Low / en yüksek High'ı). Düşen satır İLK tutmayan nedenle sayılır (neden_sira). "
                          "Net işareti kullanılmaz (satış tablolarının çoğu tutarı işaretsiz yazıyor; |net| kullanılır). 'duzyazi' biçimli satırlar ayrı "
                          "sayılır; B ana sonucu ayrıca düz yazı hariç raporlanır (A'da düz yazı satırında maliyet yazılı değildir)."},
    "tekil": {"A": "A'da aynı veri günü + hisse + yön için birden çok GEÇERLİ MALİYETLİ satır varsa: gün sonu varsa en erken yayımlanan gün sonu, yoksa "
                   "en geç yayımlanan gün içi (gün içi / gün sonu). Haftalık satırlar ayrı tutulur (veri günü + hisse + yön başına en erken yayın).",
              "B": "B'de tetik HABER ANIDIR: aynı veri günü + hisse için hissenin alım ilk 3'te göründüğü geçerli gün içi / gün sonu haberlerinden EN ERKEN "
                   "yayımlanan tetiktir (Cemal'in o hisseyi ilk öğrendiği an; A'daki gün sonu önceliği B'de G1'in 'gün içi haber 17:30'dan önce' "
                   "kuralını boşa çıkaracağından B'de uygulanmaz). Koşul değerleri (pay, maliyet, sıra, birim) o tetik satırından alınır."},
    "A": {"ufuk": [5, 20, 60], "uc": 0.30, "fiyat_kova": [2.0, 10.0, 50.0], "pay_esik": 20.0, "cokmus": -0.60,
          "donem": [["2023-24", "2023-01-01", "2024-12-31"], ["2025-26", "2025-01-01", "2026-08-31"]],
          "getiri": "her geçerli, maliyetli ALIM satırı (tekilleştirilmiş): r_k = Kapanış(veri günü + k işlem günü) / BofA maliyeti - 1, k = 5, 20, 60 "
                    "(işlem günü takvimi bi_takvim; kapanış en çok 5 gün ileri taşınmış)",
          "kontrol": "aynı veri günü, aynı FI_OLCUT momentum beşliği x likidite üçlüsü hücresindeki (bi_panel H; hisse kendisi hariç, en az 3) öteki "
                     "hisselerin veri günü tipik fiyatı (H + L + C) / 3'ten Kapanış(veri günü + k)'ya getirisi; eş ortalaması; EŞLİ FARK = r_k - eş "
                     "ortalaması. Eşlerin P(>= +%30) ve P(<= -%30) oranları da (kat = olay / eş)",
          "olcu": "kâr oranı P(r_k > 0), medyan, ortalama, P(r_k >= +%30), P(r_k <= -%30), ortalama / medyan eşli fark, eş ortalaması",
          "kirilim": "fiyat kovası (maliyet < 2 TL, 2-10, 10-50, > 50); çökmüş (veri gününden önceki kapanış / önceki 250 günün en yüksek kapanışı - 1 "
                     "<= -0,60, en az 120 bar) / değil; birim lot / TL; BofA payı >= %20 / < %20 / yazılı değil; dönem 2023-24 / 2025-26 (pencere "
                     "sonu <= 31.08.2026); kriz sonrası (veri günü >= 01.09.2026) BİLGİ",
          "kriz": "ana A tablosu: pencere sonu (veri günü + k) <= 31.08.2026; veri günü <= 31.08 < pencere sonu 'kesik aşan' (sayılır, girmez); veri "
                  "günü >= 01.09.2026 'kriz sonrası' BİLGİ (penceresi veride bitenler)",
          "fifo": "aynı hissede geçerli, maliyetli, LOT birimli gün içi / gün sonu satırları (A tekilleştirmesi, alım ve satım) yayın sırasıyla; alımlar "
                  "kuyruğa (lot, maliyet), satışlar en eski alımdan eşlenir. Eşleşme getirisi = satış maliyeti / alış maliyeti - 1; gerçekleşen TL = lot x "
                  "(satış - alış); tutma günü = işlem günü farkı; KAPSAM = eşlenen lot / alınan lot; eşleşmeyen satış lotu ayrı sayılır; kalan alımlar "
                  "son kapanışla BİLGİ. Aynı yayın anında alım önce. Kriz: satış veri günü <= 31.08.2026 / sonrası ayrı",
          "satis_bilgi": "BİLGİ: geçerli maliyetli SATIM satırlarında işaretli getiri -(Kapanış(veri günü + k) / maliyet - 1) (BofA'nın sattıktan sonra "
                         "kaçındığı düşüş pozitif)"},
    "B": {"giris_sira": 3, "tur": ["gun_ici", "gun_sonu"], "g1_saat": "17:30", "cikis_sira": 5, "cikis_tur": ["gun_ici", "gun_sonu", "haftalik"],
          "tavan_gun": 250, "c2_gun": 20, "K1_pay": 20.0, "K2_kovalama": 0.05, "K3_gun": 5, "K3_en_az": 2, "K4_gun": 20, "K4_sira": 5,
          "K5_cokmus": -0.60, "K6_birim": "lot", "ana": "G1C1",
          "tetik": "geçerli (temizlik) BofA ALIM listesi satırı, sıra <= 3, tür gün içi ya da gün sonu (haftalık B'de tetik değil); veri günü + hisse "
                   "başına en erken yayımlanan (BI tekil kuralı B)",
          "giris": {"G1": "tetik gün içi haberi ve yayın veri gününde 17:30 TR'den önce -> veri günü KAPANIŞI (giriş anı 18:10); değilse yayından sonraki "
                          "ilk işlem günü AÇILIŞI (bi_giris_gunu; giriş anı 10:00)",
                    "G2": "her zaman yayından sonraki ilk işlem günü açılışı (bi_giris_gunu)"},
          "cikis": {"C1": "BOFA_IZI tutma dönemi kuralı: G1 giriş anından SONRA yayımlanan ilk BofA satış listesi haberinde (gün içi / gün sonu / haftalık; "
                          "BOFA_IZI.bi_liste_hazirla satırları, blok 1) hisse ilk 5'te -> o yayından sonraki ilk açılış (durdurmada 5 gün içindeki ilk "
                          "açılış, o da yoksa kapanış); satış haberi yoksa G1 giriş günü + 250 işlem günü açılışı; veri sonunda hâlâ açıksa 'açık'",
                    "C2": "sabit 20 işlem günü: açılış girişinde giriş günü + 19, kapanış girişinde giriş günü + 20 işlem günü KAPANIŞI"},
          "olay": "her koşul (ve TÜMÜ) için ayrı olay kümesi: koşulu sağlayan tetikler hisse başına yayın sırasıyla; tetik bir dönem açar, dönem açıkken "
                  "(tetik yayını <= çıkış haberi yayını / 250. gün / veri sonu) gelen tetikler yeni dönem açmaz. Olay kümesi ANA yolla (G1 + C1) "
                  "kurulur; G1C2, G2C1, G2C2 aynı olayların başka giriş / çıkış uygulamasıdır (BİLGİ). Tamamlayıcı = koşul bilinen ve sağlanmayan "
                  "tetikler (BİLGİ); koşulu bilinmeyen (pay / maliyet yazılı değil, çökmüşlük ölçülemiyor) tetik ikisine de girmez",
          "kosul": {"K1": "BofA günlük hacim payı >= %20 (tetik satırında pay yazılı)",
                    "K2": "kovalamama: G1 giriş fiyatı / tetik satırındaki BofA maliyeti - 1 <= +%5 (maliyet yazılı)",
                    "K3": "birikim: veri günü dahil son 5 işlem gününde (veri günü - 4 .. veri günü) en az 2 FARKLI veri gününde geçerli gün içi / gün sonu "
                          "alım listesinde ilk 3; önceki günler yalnız tetik yayınından ÖNCE yayımlanmış haberlerden",
                    "K4": "dönüş: tetik yayınından ÖNCE ve veri gününden 20 işlem günü önceki gün 00:00'dan SONRA yayımlanmış bir BofA satış listesi "
                          "haberinde (C1'deki satış satırları, her tür) hisse ilk 5'te",
                    "K5": "çökmüş: G1 giriş gününden önceki kapanış / önceki 250 günün en yüksek kapanışı - 1 <= -0,60 (bi_panel dd)",
                    "K6": "lot sıralı liste (tetik satırı birim lot)"},
          "olcu": "BOFA_IZI dönem ölçüsü (bi_donem_ozet ile aynı tanım): getiri = çıkış fiyatı / giriş fiyatı - 1; eş = giriş günü aynı FI_OLCUT "
                  "momentum beşliği x likidite üçlüsü hücresindeki öteki hisseler, AYNI giriş (açılış ya da kapanış) ve AYNI çıkış (açılış ya da "
                  "kapanış) günü ve türüyle; EŞLİ FARK = olay - eş ortalaması; SIRA = olayın eşler içindeki yeri; 10 yuva slot portföy (yuva çıkış günü "
                  "boşalır) vs her olay yerine aynı hücreden rastgele eş alınan 200 portföy; ay kümeli bootstrap (giriş ayı, 2000, tohum 27); ayrıca "
                  "en yüksek / en düşük, P(getiri >= +%50) ve eşlerin aynı oranı (kat)"},
    "karar": {"n_min": 30, "port_yuzde": 0.90, "port_n": 200, "bh_q": 0.10, "bh_m": 7, "yari": "2025-01-01",
              "alt_donem": ["2023-04 .. 2024-12 (A)", "2025-01 .. 2026-08 (B)"],
              "metin": "Her satır (K1..K6, TÜMÜ), ANA yol G1 + C1, çıkışı <= 31.08.2026 olan kapanmış dönemlerle: n >= 30 VE ortalama eşli fark > 0 VE ay "
                       "kümeli bootstrap %95 alt uç > 0 VE ortalama sıra > 0,50 VE 10 yuva portföy > 200 rastgele eş portföyün %90'ı VE iki alt dönemde "
                       "(giriş < 01.01.2025 / >= 01.01.2025) ortalama eşli fark > 0 VE Benjamini-Hochberg q = 0,10 ile reddedilen (7 satır, p = bootstrap "
                       "tek yönlü P(ortalama <= 0)) -> 'YOL ADAYI (BIST)'; değilse 'yol yok' ve tutmayan şartlar. AKD verisi yalnız BIST'te var: ABD / "
                       "Avrupa karar hücresi YOK; karar en fazla 'BIST-ADAY' düzeyindedir (CLAUDE.md 28 Eki karar hücreleri: İZ değildir).",
              "bilgi": "G1C2, G2C1, G2C2, düz yazı hariç, tamamlayıcılar, ikincil 60 gün ve olasılıklar BİLGİ / duyarlılıktır; karar değiştirmez"},
    "ikincil": {"tekil_gun": 60,
                "tanim": "aynı koşullu tetikler, BOFA_IZI olay60 tanımıyla: giriş = yayından sonraki ilk açılış, aynı hissede 60 işlem gününde tek olay, "
                         "FON_IZI.FI_OLCUT r60 eşli fark / sıra / portföy (bi_olay_olc, bi_olay_ozet, bi_olay_karar); 20 gün P(+%50'ye dokunma) ve "
                         "P(-%30'a dokunma), eşlerin kaç katı (60 gün penceresi / 20 gün penceresi 31.08.2026 içinde)"},
    "kriz": {"kesik": "2026-08-31", "kriz_bas": "2026-09-01",
             "kural": "çıkışı 31.08.2026'dan sonra olan ya da veri sonunda açık dönem karara girmez (sayılır); G1 giriş günü >= 01.09.2026 olan TÜMÜ "
                      "dönemleri ayrı BİLGİ tablosunda (açık olanlar bugüne getiri)"},
    "yanlilik": "AKD kodu kurum kimliği değildir (müşteri akışı; BofA'nın kendi pozisyonu değil). Liste ilk 5-10 ile sınırlı: BofA'nın listede "
                "görünmeyen alım / satımları yok; FIFO yalnız yayımlanmış lot listeleriyle, kapsamı düşüktür. Maliyet yalnız bazı hisse.net / YatırımX "
                "listelerinde yazılı (çoğu 2025-26). Gün içi maliyet o saate kadarki ortalamadır. Fiyatlar Yahoo bölünme düzeltmeli: bölünme öncesi "
                "maliyet bant dışı kalır ve düşer. Fiyat evreni bugün işlem gören hisseler (hayatta kalma yanlılığı). İşlem maliyeti / kayma yok.",
}


def _bk_yol(ad: str, kl: Optional[str] = None) -> str:
    return os.path.join(kl or BI_YOL["cikti"], BK_DOSYA.get(ad, ad))


def _bk_is(ad: str) -> str:
    return os.path.join(BI_YOL["is"], BK_DOSYA.get(ad, ad))


def _bk_sonlu(x: Any) -> bool:
    try:
        return bool(np.isfinite(float(x)))
    except (TypeError, ValueError):
        return False


def bk_temizle(Ld: pd.DataFrame, A: Dict[str, Any], takvim: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Kapsamdaki BofA satırları + veri günü + temizlik nedeni ('' = geçerli). BK_ESIK['temizlik']."""
    E = E or BK_ESIK; T = E["temizlik"]; K = E["kapsam"]
    m = (Ld.kurum == K["kurum"]) & (Ld.blok == K["blok"]) & Ld.tur.isin(K["tur"]) & Ld.yon.isin(K["yon"])
    L = Ld[m].copy().reset_index(drop=True)
    L["yayin"] = pd.to_datetime(L.yayin, errors="coerce")
    ti = {t: i for i, t in enumerate(A["tarih"])}; lo_b, hi_b = T["maliyet_bant"]; hg = int(T["haftalik_bant_gun"])
    vg_l, vgi_l, nd_l = [], [], []
    for r in L.itertuples():
        v = bi_veri_gunu(r.yayin, takvim) if not pd.isna(r.yayin) else None
        vg_l.append(v); i = ti.get(pd.Timestamp(v)) if v is not None else None; vgi_l.append(i if i is not None else -1)
        if v is None:
            nd_l.append("veri_gunu_yok"); continue
        j = A["kol"].get(r.hisse)
        if j is None:
            nd_l.append("fiyat_paneli_yok"); continue
        if i is None or not (np.isfinite(A["Hh"][i, j]) and np.isfinite(A["Ll"][i, j]) and np.isfinite(A["Cf"][i, j])):
            nd_l.append("veri_gunu_bar_yok"); continue
        net = float(r.net) if _bk_sonlu(r.net) else np.nan
        if not np.isfinite(net):
            nd_l.append("net_yok"); continue
        mal = float(r.maliyet) if _bk_sonlu(r.maliyet) else np.nan
        if r.birim == "lot":
            fy = mal if (np.isfinite(mal) and mal > 0) else A["Cf"][i, j]
            if abs(net) < T["lot_min"] or abs(net) * fy < T["lot_tl_min"]:
                nd_l.append("esik_alti"); continue
        elif abs(net) < T["tl_min"]:
            nd_l.append("esik_alti"); continue
        if np.isfinite(mal):
            if r.tur == "haftalik":
                with np.errstate(all="ignore"):
                    lo, hi = np.nanmin(A["Ll"][max(0, i - hg + 1):i + 1, j]), np.nanmax(A["Hh"][max(0, i - hg + 1):i + 1, j])
            else:
                lo, hi = A["Ll"][i, j], A["Hh"][i, j]
            if not (mal > 0 and lo * lo_b <= mal <= hi * hi_b):
                nd_l.append("maliyet_bant_disi"); continue
        nd_l.append("")
    L["veri_gunu"] = vg_l; L["vgi"] = vgi_l; L["neden"] = nd_l
    return L


def bk_temiz_sayim(T: pd.DataFrame) -> Dict[str, Any]:
    """Temizlik sayımı (getiri yok): neden x yön, biçim, tür; geçerli maliyetli satırlar."""
    G = T[T.neden == ""]
    out: Dict[str, Any] = {"kapsam_satir": int(len(T)), "gecerli": int(len(G)),
                           "dusen": {k: int(v) for k, v in T[T.neden != ""].neden.value_counts().items()},
                           "dusen_yon": {f"{a}/{b}": int(v) for (a, b), v in T[T.neden != ""].groupby(["yon", "neden"]).size().items()},
                           "gecerli_yon_tur": {f"{a}/{b}": int(v) for (a, b), v in G.groupby(["yon", "tur"]).size().items()},
                           "gecerli_bicim": {k: int(v) for k, v in G.bicim.value_counts().items()} if "bicim" in G else {},
                           "duzyazi_kapsam": int((T.bicim == "duzyazi").sum()) if "bicim" in T else 0,
                           "duzyazi_gecerli": int((G.bicim == "duzyazi").sum()) if "bicim" in G else 0,
                           "gecerli_maliyetli": {f"{a}/{b}": int(v) for (a, b), v in G[G.maliyet.notna()].groupby(["yon", "birim"]).size().items()},
                           "gecerli_payli": int(G.pay.notna().sum())}
    return out


def bk_a_tekil(X: pd.DataFrame) -> pd.DataFrame:
    """A tekilleştirmesi (BK_ESIK['tekil']['A']): veri günü + hisse + yön başına gün sonu (en erken) > gün içi (en geç); haftalık: en erken."""
    if not len(X):
        return X
    sec = []
    for _, g in X.groupby(["veri_gunu", "hisse", "yon", X.tur == "haftalik"], sort=False):
        if (g.tur == "haftalik").all():
            sec.append(g.sort_values("yayin").index[0]); continue
        gs = g[g.tur == "gun_sonu"]
        sec.append(gs.sort_values("yayin").index[0] if len(gs) else g.sort_values("yayin").index[-1])
    return X.loc[sorted(sec)].sort_values(["yayin", "hisse"]).reset_index(drop=True)


def _bk_esler(A: Dict[str, Any], d: int, j: int) -> np.ndarray:
    """Giriş günü d'de j ile aynı hücredeki öteki hisselerin sütunları (ok[d]); hücre tanımsızsa boş."""
    if A["H"][d, j] < 0:
        return np.array([], int)
    m = (A["H"][d] == A["H"][d, j]) & A["ok"][d]; m[j] = False
    return np.where(m)[0]


def bk_a_olc(A: Dict[str, Any], takvim: pd.DatetimeIndex, X: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """A: her satır için r_k (BofA maliyetinden), eş ortalaması (veri günü tipik fiyatından), eşli fark, eş P(>= +%30) / P(<= -%30), pencere grubu."""
    E = E or BK_ESIK; Ae = E["A"]; kes = pd.Timestamp(E["kriz"]["kesik"]); kb = pd.Timestamp(E["kriz"]["kriz_bas"]); u = Ae["uc"]
    ti = {t: i for i, t in enumerate(A["tarih"])}; pos = {t: i for i, t in enumerate(takvim)}
    Y = X.copy().reset_index(drop=True); ek: Dict[str, list] = {}
    for r in Y.itertuples():
        j = A["kol"][r.hisse]; i = ti[pd.Timestamp(r.veri_gunu)]; p = pos.get(pd.Timestamp(r.veri_gunu)); mal = float(r.maliyet)
        dd = A["dd"][i - 1, j] if i >= 1 else np.nan
        ek.setdefault("cokmus", []).append(bool(dd <= Ae["cokmus"]) if np.isfinite(dd) else None)
        c = _bk_esler(A, i, j)
        with np.errstate(all="ignore"):
            tp = (A["Hh"][i, c] + A["Ll"][i, c] + A["Cf"][i, c]) / 3.0
        for k in Ae["ufuk"]:
            rk = ek_ = fk = pu = pa = np.nan; grup = "pencere_yok"; son = None
            if p is not None and p + k < len(takvim) and ti.get(takvim[p + k]) is not None:
                x = ti[takvim[p + k]]; son = takvim[p + k]
                rk = A["Cf"][x, j] / mal - 1
                if len(c):
                    with np.errstate(all="ignore"):
                        e = A["Cf"][x, c] / tp - 1
                    e = e[np.isfinite(e)]
                    if len(e) >= 3:
                        ek_ = float(e.mean()); fk = rk - ek_; pu = float((e >= u).mean()); pa = float((e <= -u).mean())
                v = pd.Timestamp(r.veri_gunu)
                grup = "ana" if son <= kes else ("kriz_sonrasi" if v >= kb else "kesik_asan")
            elif pd.Timestamp(r.veri_gunu) >= kb:
                grup = "kriz_sonrasi_pencere_yok"
            for ad, val in ((f"r{k}", rk), (f"e{k}", ek_), (f"f{k}", fk), (f"eu{k}", pu), (f"ea{k}", pa), (f"grup{k}", grup), (f"son{k}", son)):
                ek.setdefault(ad, []).append(val)
    for k, v in ek.items():
        Y[k] = v
    return Y


def bk_a_ozet(Y: pd.DataFrame, k: int, u: float = 0.30) -> Dict[str, Any]:
    r = pd.to_numeric(Y[f"r{k}"], errors="coerce"); Z = Y[r.notna()]; r = r[r.notna()]
    if not len(Z):
        return {"n": 0}
    f = pd.to_numeric(Z[f"f{k}"], errors="coerce"); eu = pd.to_numeric(Z[f"eu{k}"], errors="coerce"); ea = pd.to_numeric(Z[f"ea{k}"], errors="coerce")
    pu, pa = float((r >= u).mean()), float((r <= -u).mean())
    zu, za = (r[eu.notna()] >= u).mean(), (r[ea.notna()] <= -u).mean()
    return {"n": int(len(Z)), "hisse": int(Z.hisse.nunique()), "kar_orani": float((r > 0).mean()), "medyan": float(r.median()), "ort": float(r.mean()),
            "p_ust30": pu, "p_alt30": pa, "n_es": int(f.notna().sum()), "esli_fark_ort": float(f.mean()) if f.notna().any() else None,
            "esli_fark_medyan": float(f.median()) if f.notna().any() else None,
            "es_ort": float(pd.to_numeric(Z[f"e{k}"], errors="coerce").mean()) if f.notna().any() else None,
            "es_p_ust30": float(eu.mean()) if eu.notna().any() else None, "es_p_alt30": float(ea.mean()) if ea.notna().any() else None,
            "kat_ust30": float(zu / eu.mean()) if eu.notna().any() and eu.mean() > 0 else None,
            "kat_alt30": float(za / ea.mean()) if ea.notna().any() and ea.mean() > 0 else None}


def bk_a_kirilim(Y: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """A kırılımları (BK_ESIK['A']['kirilim']) her ufuk için; ana = pencere sonu <= kesik."""
    E = E or BK_ESIK; Ae = E["A"]; u = Ae["uc"]; out: Dict[str, Any] = {}
    if not len(Y):
        return out
    fk = Ae["fiyat_kova"]
    kova = pd.cut(pd.to_numeric(Y.maliyet), [-np.inf] + list(fk) + [np.inf], right=False,
                  labels=[f"<{fk[0]:g}", f"{fk[0]:g}-{fk[1]:g}", f"{fk[1]:g}-{fk[2]:g}", f">={fk[2]:g}"])
    pay = pd.to_numeric(Y.pay, errors="coerce")
    for k in Ae["ufuk"]:
        g = Y[f"grup{k}"]; ana = g == "ana"; o: Dict[str, Any] = {"tum": bk_a_ozet(Y[ana], k, u)}
        for lab in kova.cat.categories:
            o[f"fiyat {lab}"] = bk_a_ozet(Y[ana & (kova == lab)], k, u)
        o["cokmus"] = bk_a_ozet(Y[ana & (Y.cokmus == True)], k, u)  # noqa: E712
        o["cokmus_degil"] = bk_a_ozet(Y[ana & (Y.cokmus == False)], k, u)  # noqa: E712
        for b in ("lot", "TL"):
            o[f"birim {b}"] = bk_a_ozet(Y[ana & (Y.birim == b)], k, u)
        o["pay >= %20"] = bk_a_ozet(Y[ana & (pay >= Ae["pay_esik"])], k, u)
        o["pay < %20"] = bk_a_ozet(Y[ana & (pay < Ae["pay_esik"])], k, u)
        o["pay yok"] = bk_a_ozet(Y[ana & pay.isna()], k, u)
        for ad, a, b in Ae["donem"]:
            v = pd.to_datetime(Y.veri_gunu)
            o[f"dönem {ad}"] = bk_a_ozet(Y[ana & (v >= pd.Timestamp(a)) & (v <= pd.Timestamp(b))], k, u)
        o["gun_ici"] = bk_a_ozet(Y[ana & (Y.tur == "gun_ici")], k, u)
        o["gun_sonu"] = bk_a_ozet(Y[ana & (Y.tur == "gun_sonu")], k, u)
        o["kriz_sonrasi (BİLGİ)"] = bk_a_ozet(Y[g == "kriz_sonrasi"], k, u)
        o["_sayim"] = {kk: int(v) for kk, v in g.value_counts().items()}
        out[str(k)] = o
    return out


def bk_a_hisse(Y: pd.DataFrame, k: int = 20, en_az: int = 3) -> List[Dict[str, Any]]:
    """Hisse bazında A (ana pencere): en az `en_az` satırı olan hisseler, ortalama r_k ve eşli fark (BİLGİ, çoklu)."""
    Z = Y[(Y[f"grup{k}"] == "ana") & pd.to_numeric(Y[f"r{k}"], errors="coerce").notna()]
    sat = []
    for h, g in Z.groupby("hisse"):
        if len(g) >= en_az:
            sat.append({"hisse": h, "n": int(len(g)), "ort": float(g[f"r{k}"].mean()), "medyan": float(g[f"r{k}"].median()),
                        "kar_orani": float((g[f"r{k}"] > 0).mean()), "esli_fark": float(pd.to_numeric(g[f"f{k}"], errors="coerce").mean()),
                        "ilk": str(pd.Timestamp(g.veri_gunu.min()).date()), "son": str(pd.Timestamp(g.veri_gunu.max()).date())})
    return sorted(sat, key=lambda x: -x["n"])


def bk_fifo(R: pd.DataFrame, A: Dict[str, Any], takvim: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """FIFO (BK_ESIK['A']['fifo']). R: geçerli, maliyetli, lot birimli, A tekilleştirilmiş gün içi / gün sonu alım + satım satırları."""
    E = E or BK_ESIK; kes = pd.Timestamp(E["kriz"]["kesik"]); pos = {t: i for i, t in enumerate(takvim)}
    from collections import deque
    S = R.assign(_y=(R.yon != "alim").astype(int)).sort_values(["yayin", "_y", "hisse"]).reset_index(drop=True)
    q: Dict[str, Any] = {}; es = []; alinan = 0.0; eslesmeyen = 0.0; satilan = 0.0
    for r in S.itertuples():
        lot = abs(float(r.net)); mal = float(r.maliyet); v = pd.Timestamp(r.veri_gunu)
        if r.yon == "alim":
            q.setdefault(r.hisse, deque()).append([lot, mal, v]); alinan += lot; continue
        satilan += lot; kalan = lot; d = q.get(r.hisse)
        while kalan > 0 and d:
            b = d[0]; m = min(b[0], kalan)
            es.append({"hisse": r.hisse, "alis_gunu": b[2], "satis_gunu": v, "lot": m, "alis": b[1], "satis": mal, "ret": mal / b[1] - 1,
                       "gun": pos.get(v, np.nan) - pos.get(b[2], np.nan), "tl": m * (mal - b[1]), "maliyet_tl": m * b[1]})
            b[0] -= m; kalan -= m
            if b[0] <= 1e-9:
                d.popleft()
        eslesmeyen += kalan
    M = pd.DataFrame(es, columns=["hisse", "alis_gunu", "satis_gunu", "lot", "alis", "satis", "ret", "gun", "tl", "maliyet_tl"])
    acik = []
    for h, d in q.items():
        j = A["kol"].get(h)
        for b in d:
            if b[0] > 0 and j is not None:
                c = A["Cf"][-1, j]
                acik.append({"hisse": h, "alis_gunu": b[2], "lot": b[0], "alis": b[1], "son_kapanis": c, "ret": c / b[1] - 1 if np.isfinite(c) else np.nan})
    Ac = pd.DataFrame(acik)

    def oz(Mx: pd.DataFrame) -> Dict[str, Any]:
        if not len(Mx):
            return {"n": 0}
        return {"n": int(len(Mx)), "hisse": int(Mx.hisse.nunique()), "lot": float(Mx.lot.sum()), "ret_lot_agirlik": float(Mx.tl.sum() / Mx.maliyet_tl.sum()),
                "ret_medyan": float(Mx.ret.median()), "ret_ort": float(Mx.ret.mean()), "kar_orani": float((Mx.ret > 0).mean()),
                "kar_orani_lot": float(Mx[Mx.ret > 0].lot.sum() / Mx.lot.sum()), "gun_medyan": float(Mx.gun.median()),
                "p_ust30": float((Mx.ret >= 0.30).mean()), "p_alt30": float((Mx.ret <= -0.30).mean())}
    out = {"alim_satir": int((S.yon == "alim").sum()), "satim_satir": int((S.yon == "satim").sum()), "alinan_lot": alinan, "satilan_lot": satilan,
           "eslesen_lot": float(M.lot.sum()) if len(M) else 0.0, "eslesmeyen_satis_lot": eslesmeyen,
           "kapsam": float(M.lot.sum() / alinan) if alinan > 0 and len(M) else 0.0,
           "tum": oz(M), "kesik_ici": oz(M[pd.to_datetime(M.satis_gunu) <= kes]) if len(M) else {"n": 0},
           "kriz_sonrasi": oz(M[pd.to_datetime(M.satis_gunu) > kes]) if len(M) else {"n": 0},
           "acik": {"n": int(len(Ac)), "lot": float(Ac.lot.sum()) if len(Ac) else 0.0,
                    "ret_lot_agirlik": float(((Ac.son_kapanis - Ac.alis) * Ac.lot).sum() / (Ac.alis * Ac.lot).sum()) if len(Ac) else None}}
    if len(M):
        H = M.groupby("hisse").agg(n=("ret", "size"), lot=("lot", "sum"), tl=("tl", "sum"), mtl=("maliyet_tl", "sum"), gun=("gun", "median")).reset_index()
        H["ret"] = H.tl / H.mtl
        out["hisse"] = _bi_kayit(H.sort_values("mtl", ascending=False).head(15).drop(columns=["mtl"]))
    return M, out


# ---------------------------------------------------------------- B) TETİKLER, KOŞULLAR, OLAYLAR
def bk_satis5(Ld: pd.DataFrame, takvim: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """C1 ve K4 satış satırları: BOFA_IZI.bi_liste_hazirla (BofA, blok 1, her tür, geçerli kod), yön satım, sıra <= 5."""
    E = E or BK_ESIK; b = E["B"]
    L = bi_liste_hazirla(Ld, takvim, None)
    return L[(L.yon == "satim") & (L.sira <= b["cikis_sira"]) & L.tur.isin(b["cikis_tur"])].sort_values("yayin").reset_index(drop=True)


def bk_tetikler(T: pd.DataFrame, S5: pd.DataFrame, A: Dict[str, Any], takvim: pd.DatetimeIndex,
                E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Tetikler (BK_ESIK['B']['tetik']) + G1 / G2 giriş + K1..K6 (True / False / None = bilinmiyor). Yalnız tetik yayınından önceki bilgi."""
    E = E or BK_ESIK; b = E["B"]
    V = T[(T.neden == "") & (T.yon == "alim") & T.tur.isin(b["tur"]) & (T.sira <= b["giris_sira"])].copy()
    if not len(V):
        return V.assign(**{k: [] for k in ("g1", "g1_tip", "g2", "g1_fiyat") + BK_KOSUL})
    V = V.sort_values(["yayin", "haber_id"])
    X = V.groupby(["veri_gunu", "hisse"], sort=False).head(1).sort_values("yayin").reset_index(drop=True)
    ti = {t: i for i, t in enumerate(A["tarih"])}; pos = {t: i for i, t in enumerate(takvim)}
    gecmis = {h: list(zip(pd.to_datetime(g.veri_gunu), g.yayin)) for h, g in V.groupby("hisse")}
    sgec = {h: g.yayin.sort_values().to_numpy() for h, g in S5.groupby("hisse")}
    sat = []
    for r in X.itertuples():
        v = pd.Timestamp(r.veri_gunu); y = pd.Timestamp(r.yayin); j = A["kol"][r.hisse]; p = pos.get(v)
        if r.tur == "gun_ici" and y.normalize() == v and y.strftime("%H:%M") < b["g1_saat"]:
            g1, tip = v, "kapanis"
        else:
            g1, tip = bi_giris_gunu(y, takvim), "acilis"
        g2 = bi_giris_gunu(y, takvim)
        d1 = ti.get(pd.Timestamp(g1)) if g1 is not None else None
        fy = np.nan
        if d1 is not None and np.isfinite(A["Op"][d1, j]):
            fy = A["Cf"][d1, j] if tip == "kapanis" else A["Op"][d1, j]
        pay = float(r.pay) if _bk_sonlu(r.pay) else np.nan; mal = float(r.maliyet) if _bk_sonlu(r.maliyet) else np.nan
        k1 = bool(pay >= b["K1_pay"]) if np.isfinite(pay) else None
        k2 = bool(fy / mal - 1 <= b["K2_kovalama"]) if (np.isfinite(mal) and mal > 0 and np.isfinite(fy)) else None
        if p is None:
            k3 = k4 = None
        else:
            pencere = set(takvim[max(0, p - b["K3_gun"] + 1):p])
            onceki = {vv for vv, yy in gecmis.get(r.hisse, []) if vv in pencere and yy < y}
            k3 = bool(1 + len(onceki) >= b["K3_en_az"])
            bas = takvim[max(0, p - b["K4_gun"])]
            s = sgec.get(r.hisse)
            k4 = bool(s is not None and ((s >= np.datetime64(bas)) & (s < np.datetime64(y))).any())
        dd = A["dd"][d1 - 1, j] if (d1 is not None and d1 >= 1) else np.nan
        k5 = bool(dd <= b["K5_cokmus"]) if np.isfinite(dd) else None
        k6 = bool(r.birim == b["K6_birim"])
        sat.append({"g1": g1, "g1_tip": tip, "g2": g2, "g1_fiyat": fy, "gec": (fy / mal - 1) if (np.isfinite(mal) and mal > 0) else np.nan,
                    "K1": k1, "K2": k2, "K3": k3, "K4": k4, "K5": k5, "K6": k6})
    Z = pd.DataFrame(sat)
    for c in Z.columns:
        X[c] = Z[c].values
    return X


def bk_olaylar(Tc: pd.DataFrame, S5: pd.DataFrame, takvim: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Bir koşulun tetiklerinden olaylar (BK_ESIK['B']['olay']): ANA yol (G1 giriş anı, C1 çıkış) ile dönem; C2 / G2 tarihleri de yazılır."""
    E = E or BK_ESIK; b = E["B"]; pos = {t: i for i, t in enumerate(takvim)}; ki = len(takvim) - 1
    kol = ["hisse", "haber_id", "yayin", "veri_gunu", "tur", "sira", "birim", "bicim", "net", "pay", "maliyet", "g1", "g1_tip", "g2", "g1_fiyat", "gec",
           *BK_KOSUL, "c1", "c1_neden", "c1_haber", "c1_yayin", "c2", "c2_g2", "c2_acik", "c2_g2_acik"]
    out = []
    for h, g in Tc.sort_values("yayin").groupby("hisse"):
        kapanis = pd.Timestamp.min
        sh = S5[S5.hisse == h]
        for r in g.itertuples():
            if r.yayin <= kapanis or r.g1 is None or pd.isna(r.g1) or pd.Timestamp(r.g1) not in pos:
                continue
            g1 = pd.Timestamp(r.g1); p = pos[g1]
            an = g1 + (pd.Timedelta(hours=18, minutes=10) if r.g1_tip == "kapanis" else pd.Timedelta(hours=10))
            c = sh[sh.yayin > an]; ch = cy = None
            if len(c):
                cg = bi_giris_gunu(c.yayin.iloc[0], takvim)
                if cg is None or pos.get(pd.Timestamp(cg), 10 ** 9) > ki:
                    cx, nd, kapanis = takvim[ki], "acik_veri_sonu", pd.Timestamp.max
                else:
                    cx, nd, kapanis = pd.Timestamp(cg), "satis", c.yayin.iloc[0]
                ch, cy = c.haber_id.iloc[0], c.yayin.iloc[0]
            elif p + b["tavan_gun"] <= ki:
                cx, nd = takvim[p + b["tavan_gun"]], "satis_gorulmedi_250"; kapanis = cx + pd.Timedelta(hours=10)
            else:
                cx, nd, kapanis = takvim[ki], "acik_veri_sonu", pd.Timestamp.max
            x2 = p + b["c2_gun"] - (0 if r.g1_tip == "kapanis" else 1)
            g2 = pd.Timestamp(r.g2) if r.g2 is not None and not pd.isna(r.g2) else None
            p2 = pos.get(g2) if g2 is not None else None
            x22 = p2 + b["c2_gun"] - 1 if p2 is not None else None
            d = {k: getattr(r, k) for k in kol if hasattr(r, k)}
            d.update({"c1": cx, "c1_neden": nd, "c1_haber": ch, "c1_yayin": cy, "c2": takvim[min(x2, ki)], "c2_acik": x2 > ki,
                      "c2_g2": takvim[min(x22, ki)] if x22 is not None else None, "c2_g2_acik": (x22 is None) or x22 > ki})
            out.append(d)
    return pd.DataFrame(out, columns=kol).sort_values("g1").reset_index(drop=True) if out else pd.DataFrame(columns=kol)


def bk_yol_olc(A: Dict[str, Any], ev: pd.DataFrame, yol: str = "G1C1", cokmus: float = -0.60) -> pd.DataFrame:
    """Bir yolun (G1C1 / G1C2 / G2C1 / G2C2) dönem ölçüsü: getiri, en yüksek / en düşük, eş ortalaması (aynı hücre, aynı giriş / çıkış günü ve
    türü), eşli fark, sıra, eş getirileri, P(>= +%50) eş oranı, geç kalma, çökmüş. Sütunlar bi_donem_ozet ile uyumlu (giris, cikis, neden)."""
    gk, ck = {"G1C1": ("g1", "c1"), "G1C2": ("g1", "c2"), "G2C1": ("g2", "c1"), "G2C2": ("g2", "c2_g2")}[yol]
    ti = {t: i for i, t in enumerate(A["tarih"])}; Op, Cf, Hh, Ll = A["Op"], A["Cf"], A["Hh"], A["Ll"]; sat = []
    for r in ev.itertuples():
        g = getattr(r, gk); c = getattr(r, ck); gt = r.g1_tip if gk == "g1" else "acilis"; ct = "acilis" if ck == "c1" else "kapanis"
        if ck == "c1":
            nd = r.c1_neden
        else:
            nd = "acik_veri_sonu" if bool(getattr(r, "c2_acik" if ck == "c2" else "c2_g2_acik")) else "sabit_20"
        bos = {"giris": g, "cikis": c, "neden": nd, "giris_tip": gt, "cikis_tip": ct, "ret": np.nan, "max": np.nan, "min": np.nan, "esli": np.nan,
               "fark": np.nan, "sira": np.nan, "_esler": None, "gun": np.nan, "gec": np.nan, "cokmus": None, "olcuk": False, "b_ret50": np.nan}
        d = ti.get(pd.Timestamp(g)) if g is not None and not pd.isna(g) else None
        x = ti.get(pd.Timestamp(c)) if c is not None and not pd.isna(c) else None
        j = A["kol"].get(r.hisse)
        if d is None or x is None or j is None or not np.isfinite(Op[d, j]) or Op[d, j] <= 0 or x < d:
            sat.append(bos); continue
        o = Cf[d, j] if gt == "kapanis" else Op[d, j]
        if not (np.isfinite(o) and o > 0):
            sat.append(bos); continue
        hareket = x > d or (gt == "acilis" and ct == "kapanis")

        def cik(cols: Any) -> Any:
            return _bi_cikis_fiyat(A, x, cols) if ct == "acilis" else Cf[x, cols]
        ret = (cik(j) / o - 1) if hareket else 0.0
        a_, b_ = (d if gt == "acilis" else d + 1), (x if ct == "acilis" else x + 1)
        with np.errstate(all="ignore"):
            hi = (np.nanmax(Hh[a_:b_, j]) / o - 1) if b_ > a_ and np.isfinite(Hh[a_:b_, j]).any() else max(ret, 0.0)
            lo = (np.nanmin(Ll[a_:b_, j]) / o - 1) if b_ > a_ and np.isfinite(Ll[a_:b_, j]).any() else min(ret, 0.0)
        dd = A["dd"][d - 1, j] if d >= 1 else np.nan
        es, esli, sira, fark, br = None, np.nan, np.nan, np.nan, np.nan
        cols = _bk_esler(A, d, j)
        if len(cols) >= 3:
            oc = Cf[d, cols] if gt == "kapanis" else Op[d, cols]
            with np.errstate(all="ignore"):
                e = (cik(cols) / oc - 1) if hareket else np.zeros(len(cols))
            e = e[np.isfinite(e)]
            if len(e) >= 3:
                es = e; esli = float(e.mean()); fark = ret - esli; sira = float(((e < ret).sum() + 0.5 * (e == ret).sum()) / len(e))
                br = float((e >= 0.5).mean())
        mal = float(r.maliyet) if _bk_sonlu(r.maliyet) else np.nan
        sat.append({**bos, "ret": ret, "max": hi, "min": lo, "esli": esli, "fark": fark, "sira": sira, "_esler": es, "gun": x - d,
                    "gec": (o / mal - 1) if (np.isfinite(mal) and mal > 0) else np.nan, "cokmus": bool(dd <= cokmus) if np.isfinite(dd) else None,
                    "olcuk": True, "b_ret50": br, "giris_fiyat": o})
    Y = ev.drop(columns=[k for k in ("gec",) if k in ev]).rename(columns={"sira": "liste_sira"}).copy().reset_index(drop=True)
    for k in ("giris", "cikis", "neden", "giris_tip", "cikis_tip", "ret", "max", "min", "esli", "fark", "sira", "_esler", "gun", "gec", "cokmus",
              "olcuk", "b_ret50", "giris_fiyat"):
        Y[k] = [s.get(k, np.nan) for s in sat]
    Y["yol"] = yol
    return Y


def bk_yol_ozet(Y: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kesik içinde kapanmış dönemler -> bi_donem_ozet (BOFA_IZI dönem ölçüsü) + eş P(>= +%50) katı + sayımlar."""
    E = E or BK_ESIK; kes = pd.Timestamp(E["kriz"]["kesik"]); K = E["karar"]
    if not len(Y):
        return {"n": 0, "toplam": 0}
    kap = (pd.to_datetime(Y.cikis) <= kes) & (Y.neden != "acik_veri_sonu")
    Yk = Y[kap]
    o = bi_donem_ozet(Yk, K["yari"], K["port_n"]) if len(Yk) else {"n": 0}
    Z = Yk[Yk.olcuk.astype(bool)].dropna(subset=["fark"])
    if len(Z):
        br = pd.to_numeric(Z.b_ret50, errors="coerce").mean()
        o["b_ret50"] = float(br) if np.isfinite(br) else None
        o["kat_ret50"] = float(o["p_ret50"] / br) if (np.isfinite(br) and br > 0) else None
        o["b_min30_yok"] = "eşlerin dönem içi en düşüğü tutulmadı; -%30 katı 20 gün ölçüsündedir"
    o["toplam"] = int(len(Y)); o["kesik_disi_ya_da_acik"] = int((~kap).sum())
    o["kriz_sonrasi_giris"] = int((pd.to_datetime(Y.giris) >= pd.Timestamp(E["kriz"]["kriz_bas"])).sum())
    return o


def bk_karar(o: Dict[str, Any], bh_red: Optional[bool], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """BK_ESIK['karar']: FI_OLCUT dört şartı + iki alt dönem + BH. Geçerse 'YOL ADAYI (BIST)'."""
    E = E or BK_ESIK; K = E["karar"]; t = []
    if o.get("n", 0) < K["n_min"]:
        t.append(f"n = {o.get('n', 0)} < {K['n_min']} (örneklem yetersiz)")
    else:
        if not o["ort_fark"] > 0:
            t.append("ortalama eşli fark <= 0")
        if not (o.get("alt95") is not None and np.isfinite(o["alt95"]) and o["alt95"] > 0):
            t.append("bootstrap %95 alt uç <= 0")
        if not o["sira"] > 0.5:
            t.append("ortalama sıra <= 0,50")
        if not o["portfoy"] > o["portfoy_esli_p90"]:
            t.append("portföy rastgele eş portföylerin %90'ını geçmedi")
        fa, fb = (o.get("yari_A") or {}).get("ort_fark"), (o.get("yari_B") or {}).get("ort_fark")
        if not (fa is not None and fb is not None and fa > 0 and fb > 0):
            t.append("iki alt dönemde de > 0 değil")
    if not bh_red:
        t.append("BH q = 0,10 ile reddedilmedi")
    return {"karar": "YOL ADAYI (BIST)" if not t else "yol yok", "tutmayan": t}


def bk_kosul_tetik(X: pd.DataFrame, ad: str, tamam: bool = False) -> pd.DataFrame:
    """Satır adı -> tetik alt kümesi. TUM: hepsi; Kx: koşul True (tamam: koşul False; None ikisine de girmez)."""
    if ad == "TUM":
        return X
    v = X[ad].map(lambda z: z if isinstance(z, (bool, np.bool_)) else None)
    return X[v.map(lambda z: z is not None and bool(z) == (not tamam))]


def bk_b_sayim(X: pd.DataFrame, S5: pd.DataFrame, takvim: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ön kayıt için B sayımı (getiri yok): tetik, G1 türü, koşul bayrakları, olay sayıları (ANA yol, kesik içi kapanmış)."""
    E = E or BK_ESIK; kes = pd.Timestamp(E["kriz"]["kesik"]); out: Dict[str, Any] = {"tetik": int(len(X))}
    if not len(X):
        return out
    out["g1_tip"] = {k: int(v) for k, v in X.g1_tip.value_counts().items()}
    out["tetik_bicim"] = {k: int(v) for k, v in X.bicim.value_counts().items()} if "bicim" in X else {}
    out["bayrak"] = {k: {"evet": int((X[k] == True).sum()), "hayir": int((X[k] == False).sum()), "bilinmiyor": int(X[k].isna().sum())}  # noqa: E712
                     for k in BK_KOSUL}
    out["olay"] = {}
    for ad in BK_SATIR:
        ev = bk_olaylar(bk_kosul_tetik(X, ad), S5, takvim, E)
        kap = (pd.to_datetime(ev.c1) <= kes) & (ev.c1_neden != "acik_veri_sonu") if len(ev) else pd.Series([], dtype=bool)
        out["olay"][ad] = {"toplam": int(len(ev)), "kesik_ici_kapanmis": int(kap.sum()),
                           "kriz_sonrasi_giris": int((pd.to_datetime(ev.g1) >= pd.Timestamp(E["kriz"]["kriz_bas"])).sum()) if len(ev) else 0}
    return out


def bk_hazirla(Ld: pd.DataFrame, A: Dict[str, Any], takvim: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Temizlik + A satırları + FIFO girdisi + B tetikleri (getiri hesaplamaz)."""
    E = E or BK_ESIK
    T = bk_temizle(Ld, A, takvim, E); G = T[T.neden == ""]
    Ma = G[G.maliyet.notna()]
    Ag = bk_a_tekil(Ma[Ma.tur.isin(["gun_ici", "gun_sonu"])]); Ah = bk_a_tekil(Ma[Ma.tur == "haftalik"])
    S5 = bk_satis5(Ld, takvim, E)
    X = bk_tetikler(T, S5, A, takvim, E)
    Bo = Ld[Ld.kurum == E["kapsam"]["kurum"]]; dis = Bo[(Bo.blok != E["kapsam"]["blok"]) | ~Bo.tur.isin(E["kapsam"]["tur"])]
    kd = {"satir": int(len(dis)), "maliyetli": int(dis.maliyet.notna().sum()), "blok_2_ve_sonrasi": int((dis.blok != E["kapsam"]["blok"]).sum()),
          "tur_disi": {str(k): int(v) for k, v in dis[~dis.tur.isin(E["kapsam"]["tur"])].tur.value_counts().items()}}
    return {"T": T, "A_gun": Ag, "A_haf": Ah, "S5": S5, "X": X, "kapsam_disi": kd}


def bk_sayim(H: Dict[str, Any], takvim: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or BK_ESIK; Ag, Ah = H["A_gun"], H["A_haf"]; kes = pd.Timestamp(E["kriz"]["kesik"]); kb = pd.Timestamp(E["kriz"]["kriz_bas"])
    pos = {t: i for i, t in enumerate(takvim)}

    def pencere(Z: pd.DataFrame, k: int) -> Dict[str, int]:
        if not len(Z):
            return {}
        s = {"ana": 0, "kesik_asan": 0, "kriz_sonrasi": 0, "pencere_yok": 0}
        for v in pd.to_datetime(Z.veri_gunu):
            p = pos.get(v)
            if p is None or p + k >= len(takvim):
                s["pencere_yok"] += 1
            elif takvim[p + k] <= kes:
                s["ana"] += 1
            elif v >= kb:
                s["kriz_sonrasi"] += 1
            else:
                s["kesik_asan"] += 1
        return s
    a_al = Ag[Ag.yon == "alim"]
    return {"temizlik": {**bk_temiz_sayim(H["T"]), "kapsam_disi_BofA": H.get("kapsam_disi", {})},
            "A": {"alim_gun_satir": int(len(a_al)), "alim_haftalik_satir": int((Ah.yon == "alim").sum()) if len(Ah) else 0,
                  "satim_gun_satir": int((Ag.yon == "satim").sum()),
                  "alim_ceyrek": {str(k): int(v) for k, v in pd.to_datetime(a_al.veri_gunu).dt.to_period("Q").value_counts().sort_index().items()},
                  "pencere": {str(k): pencere(a_al, k) for k in E["A"]["ufuk"]},
                  "fifo_lot": {"alim": int(((Ag.birim == "lot") & (Ag.yon == "alim")).sum()), "satim": int(((Ag.birim == "lot") & (Ag.yon == "satim")).sum())}},
            "B": bk_b_sayim(H["X"], H["S5"], takvim, E)}


# ---------------------------------------------------------------- ÖN KAYIT, KAPI, KOŞU
def bk_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or BK_ESIK, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")).hexdigest()


def bk_onkayit_metin(zaman: str, sayim: Dict[str, Any], kapsam: Dict[str, Any], fiyat: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or BK_ESIK
    return "\n".join([
        "# BofA KÂRI VE HABER SONRASI YOL — ÖN KAYIT (getiri hesaplanmadan önce)", "",
        f"{BK_SURUM}. Yazılma {zaman}. Bu dosya git'e işlenmeden ve mühürler tutmadan `python BOFA_IZI.py karkos` çalışmaz.", "",
        "## Soru", "", E["soru"], "",
        "## Ne ölçülecek", "",
        "- A (betimleyici): her geçerli, maliyetli BofA ALIM satırında BofA'nın yayımlanan maliyetinden 5 / 20 / 60 işlem günü getirisi; aynı gün aynı "
        "hücredeki eşlerin tipik fiyattan getirisi; eşli fark; kırılımlar; FIFO eşlemeyle gerçekleşen kâr ve kapsam; satış satırları BİLGİ.",
        "- B (karar): BofA alım ilk 3 tetiği, 6 koşul (K1..K6) + TÜMÜ = 7 satır; ANA yol G1 + C1; FI_OLCUT dört şartı + iki alt dönem + BH q = 0,10.",
        "- B BİLGİ: G1C2, G2C1, G2C2; düz yazı hariç; tamamlayıcılar; ikincil FI_OLCUT 60 gün; 20 gün P(+%50) / P(-%30) ve eş katları; kriz sonrası "
        "açık dönemler.", "",
        "## Tanımlar ve eşikler (BK_ESIK; değişmez)", "",
        "```json", json.dumps(E, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
        "## Karar cümlesi (önceden yazılı)", "", E["karar"]["metin"], "", E["karar"]["bilgi"], "",
        "## Veri ve temizlik sayımı (getiri içermez)", "",
        f"- Arşiv (BOFA_IZI topla, değişmedi): {json.dumps(_bi_kayit({k: kapsam.get(k) for k in ('liste_haber', 'liste_satir', 'ilk', 'son')}), ensure_ascii=False)}",
        f"- Fiyat: {json.dumps(_bi_kayit(fiyat), ensure_ascii=False)}",
        f"- Temizlik: {json.dumps(_bi_kayit(sayim.get('temizlik', {})), ensure_ascii=False)}",
        f"- A sayımı: {json.dumps(_bi_kayit(sayim.get('A', {})), ensure_ascii=False)}",
        f"- B sayımı: {json.dumps(_bi_kayit(sayim.get('B', {})), ensure_ascii=False)}", "",
        "## Ön kayıttan önce görülenler (sonuç değil)", "",
        "- Önceki BOFA_IZI ölçümü (Ç171: tutma dönemi eşli fark +%0,6 [-0,6, +2,0]; lot listeleri 60 gün -%10,3) ve iş tanımındaki PEKGY örneği "
        "(27.10.2026 gün sonu alım maliyet 0,856; 11.11.2026 gün içi satış maliyet 1,219; kriz sonrası, karara girmez). Bu bölümün hiçbir getirisi, "
        "eşli farkı, kâr oranı hesaplanmadı; yukarıdaki sayımlar yalnız satır / tetik / olay sayısıdır.",
        "- Maliyet ve pay sütunlarının dağılımı (kaç satırda yazılı, hangi çeyrekte) ve net işaretinin satış tablolarında çoğunlukla işaretsiz yazıldığı "
        "(bu yüzden |net|) görüldü.", "",
        "## Bilinen yanlılıklar", "", E["yanlilik"], "",
        f"ESIK_SHA256: {bk_esik_sha(E)}",
        f"KOD_SHA256: {bi_kod_sha()}",
        f"LISTE_SHA256: {kapsam.get('liste_sha256')}",
        f"HABER_SHA256: {kapsam.get('haber_sha256')}", ""])


def bk_onkayit(kl: Optional[str] = None) -> str:
    y = _bk_yol("onkayit", kl)
    if os.path.exists(y):
        raise BiHata(f"ön kayıt zaten var, üzerine yazılmaz: {y}")
    Ld, Hd, K = _bi_veri_oku()
    K["liste_sha256"] = bi_sha_dosya(_bi_is("liste")); K["haber_sha256"] = bi_sha_dosya(_bi_is("haber"))
    V, F = bi_fiyat(); takvim = bi_takvim(V); A = bi_panel(V)
    H = bk_hazirla(Ld, A, takvim)
    return _bi_yaz(y, bk_onkayit_metin(_bi_simdi(), bk_sayim(H, takvim), K, F))


def bk_kapi(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None,
            liste_sha: Optional[str] = None, haber_sha: Optional[str] = None) -> Dict[str, Any]:
    """BOFA_KAR ön kayıt kapısı (bi_kapi deseni): ön kayıt var + git'e işlenmiş ve değişmemiş + BK_ESIK mührü + veri sha + kod sha (ya da sapma)."""
    E = E or BK_ESIK; y = _bk_yol("onkayit", kl)
    if not os.path.exists(y):
        raise BiHata("BofA kâr ön kaydı yok: önce `python BOFA_IZI.py karonkayit` ve commit")
    O = bi_onkayit_oku(y); out: Dict[str, Any] = {"onkayit": y}
    if git:
        out["onkayit_git"] = bi_git_durum(y)
    if O["ESIK_SHA256"] != bk_esik_sha(E):
        raise BiHata("eşik mührü tutmuyor (BK_ESIK ön kayıttan sonra değişmiş)")
    if liste_sha is not None and O["LISTE_SHA256"] != liste_sha:
        raise BiHata("liste verisi ön kayıttakiyle aynı değil (bofa_liste.csv değişmiş)")
    if haber_sha is not None and O["HABER_SHA256"] != haber_sha:
        raise BiHata("haber tablosu ön kayıttakiyle aynı değil (bofa_haber.csv değişmiş)")
    ks = bi_kod_sha(); out["kod_sha256"] = ks; out["kod_ayni"] = ks == O["KOD_SHA256"]
    if not out["kod_ayni"]:
        if not sapma:
            raise BiHata("BOFA_IZI.py BofA kâr ön kaydından sonra değişmiş: yalnız `--sapma GEREKCE` ile koşar (gerekçe sonuca yazılır)")
        out["sapma"] = sapma
    out["esik_sha256"] = O["ESIK_SHA256"]
    return out


def bk_kos(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None,
           V: Optional[Dict[str, pd.DataFrame]] = None, F: Optional[Dict[str, Any]] = None,
           Ld: Optional[pd.DataFrame] = None, Hd: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Kapı -> A (getiri, kırılım, FIFO, satış BİLGİ) -> B (7 satır x 4 yol, BH, karar, düz yazı hariç, tamamlayıcı, ikincil 60 gün, kriz)."""
    import FON_IZI as FI  # noqa: WPS433
    E = E or BK_ESIK
    if Ld is None:
        Ld, Hd, _ = _bi_veri_oku()
        Kp = bk_kapi(kl, git, sapma, E, bi_sha_dosya(_bi_is("liste")), bi_sha_dosya(_bi_is("haber")))
    else:
        Kp = bk_kapi(kl, git, sapma, E)
    t0 = _bi_simdi(); bilog.info("BofA kâr kapısı geçti (mühür %s)", Kp["esik_sha256"][:12])
    if V is None:
        V, F = bi_fiyat()
    takvim = bi_takvim(V); A = bi_panel(V); P = FI.fi_olcut_panel(V); son = takvim[-1]
    kes = pd.Timestamp(E["kriz"]["kesik"]); kb = pd.Timestamp(E["kriz"]["kriz_bas"]); yari = E["karar"]["yari"]
    H = bk_hazirla(Ld, A, takvim, E)
    S: Dict[str, Any] = {"surum": BK_SURUM, "baslangic": t0, "kapi": Kp, "fiyat": F, "esik_sha": bk_esik_sha(E), "son_gun": str(son.date()),
                         "sayim": bk_sayim(H, takvim, E)}
    # ---- A
    Ag = H["A_gun"]
    Ya = bk_a_olc(A, takvim, Ag[Ag.yon == "alim"], E) if len(Ag) else Ag
    Ys = bk_a_olc(A, takvim, Ag[Ag.yon == "satim"], E) if len(Ag) else Ag
    Yh = bk_a_olc(A, takvim, H["A_haf"][H["A_haf"].yon == "alim"], E) if len(H["A_haf"]) else H["A_haf"]
    S["A"] = {"kirilim": bk_a_kirilim(Ya, E), "haftalik": bk_a_kirilim(Yh, E) if len(Yh) else {},
              "hisse20": bk_a_hisse(Ya, 20) if len(Ya) else [], "hisse60": bk_a_hisse(Ya, 60) if len(Ya) else []}
    if len(Ys):
        sb = {}
        for k in E["A"]["ufuk"]:
            r = pd.to_numeric(Ys[f"r{k}"], errors="coerce"); m = (Ys[f"grup{k}"] == "ana") & r.notna(); w = -r[m]
            f = -pd.to_numeric(Ys[f"f{k}"], errors="coerce")[m]
            sb[str(k)] = {"n": int(m.sum()), "isaretli_ort": float(w.mean()) if len(w) else None, "isaretli_medyan": float(w.median()) if len(w) else None,
                          "kar_orani": float((w > 0).mean()) if len(w) else None, "isaretli_esli_fark": float(f.mean()) if f.notna().any() else None}
        S["A"]["satis_bilgi"] = sb
    R = Ag[Ag.birim == "lot"]
    M, S["A"]["fifo"] = bk_fifo(R, A, takvim, E) if len(R) else (pd.DataFrame(), {"n": 0})
    ka = Ya[(Ya.grup5 != "ana") & (pd.to_datetime(Ya.veri_gunu) >= kb)] if len(Ya) else Ya
    S["A"]["kriz_satir"] = _bi_kayit(ka[[c for c in ("hisse", "veri_gunu", "yayin", "tur", "sira", "birim", "net", "pay", "maliyet", "r5", "f5", "r20", "f20",
                                                      "r60") if c in ka]].sort_values("veri_gunu")) if len(ka) else []
    # ---- B
    X = H["X"]; S5 = H["S5"]; B: Dict[str, Any] = {}; satirlar = []
    evs: Dict[str, pd.DataFrame] = {}
    for ad in BK_SATIR:
        ev = bk_olaylar(bk_kosul_tetik(X, ad), S5, takvim, E); evs[ad] = ev; B[ad] = {"yol": {}}
        for yol, _, _ in BK_YOLLAR:
            Y = bk_yol_olc(A, ev, yol, E["B"]["K5_cokmus"]) if len(ev) else ev
            B[ad]["yol"][yol] = bk_yol_ozet(Y, E) if len(ev) else {"n": 0, "toplam": 0}
            if len(Y):
                satirlar.append(Y.drop(columns=["_esler"], errors="ignore").assign(satir=ad))
        evy = bk_olaylar(bk_kosul_tetik(X[X.bicim != "duzyazi"], ad), S5, takvim, E) if "bicim" in X else ev
        B[ad]["duzyazi_haric"] = bk_yol_ozet(bk_yol_olc(A, evy, "G1C1"), E) if len(evy) else {"n": 0}
        if ad != "TUM":
            evt = bk_olaylar(bk_kosul_tetik(X, ad, tamam=True), S5, takvim, E)
            B[ad]["tamamlayici"] = bk_yol_ozet(bk_yol_olc(A, evt, "G1C1"), E) if len(evt) else {"n": 0}
    ana = E["B"]["ana"]
    pk = {ad: (B[ad]["yol"][ana].get("p_boot") if B[ad]["yol"][ana].get("n", 0) else np.nan) for ad in BK_SATIR}
    pk = {k: (v if v is not None else np.nan) for k, v in pk.items()}
    bh = bi_bh(pk, E["karar"]["bh_q"])
    for ad in BK_SATIR:
        B[ad]["bh_red"] = bh.get(ad); B[ad]["p"] = pk[ad]
        B[ad]["karar"] = bk_karar(B[ad]["yol"][ana], bh.get(ad), E)
    S["B"] = B
    S["B_karar"] = {ad: B[ad]["karar"]["karar"] for ad in BK_SATIR}
    S["B_ozet_karar"] = ("YOL ADAYI (BIST): " + ", ".join(a for a in BK_SATIR if B[a]["karar"]["karar"] != "yol yok")
                         if any(B[a]["karar"]["karar"] != "yol yok" for a in BK_SATIR) else "yol yok (7 satırın hiçbiri bütün şartları geçmedi)")
    # ---- ikincil 60 gün
    S["ikincil"] = {}; b60 = []
    for ad in BK_SATIR:
        Tc = bk_kosul_tetik(X, ad)
        X6 = Tc.assign(giris=Tc.g2).dropna(subset=["giris"])
        X6 = bi_tekil(X6[["hisse", "giris", "veri_gunu", "yayin", "sira", "tur", "net", "maliyet"]], takvim, E["ikincil"]["tekil_gun"]) if len(X6) else X6
        Y6 = bi_olay_olc(P, A, X6, E["kriz"]["kesik"]) if len(X6) else X6
        Yk = Y6[pd.to_datetime(Y6.giris) <= kes] if len(Y6) else Y6
        o = bi_olay_ozet(Yk, yari) if len(Yk) else {"n_olay": 0}
        o["karar"] = bi_olay_karar(o) if len(Yk) else {"karar": "kanıt yok", "tutmayan": ["olay yok"]}
        S["ikincil"][ad] = o
        if len(Y6):
            b60.append(Y6.drop(columns=["_esler"], errors="ignore").assign(satir=ad))
    # ---- kriz sonrası açık (TÜMÜ, ANA yol)
    ev = evs["TUM"]
    Yt = bk_yol_olc(A, ev, ana) if len(ev) else ev
    kz = []
    if len(Yt):
        ti = {t: i for i, t in enumerate(A["tarih"])}
        for r in Yt[pd.to_datetime(Yt.giris) >= kb].itertuples():
            j = A["kol"].get(r.hisse); d = ti.get(pd.Timestamp(r.giris))
            x = {"hisse": r.hisse, "tetik_yayin": str(r.yayin)[:16], "tur": r.tur, "sira": r.liste_sira, "birim": r.birim, "maliyet": r.maliyet,
                 "giris": str(pd.Timestamp(r.giris).date()), "giris_tip": r.giris_tip, "giris_fiyat": getattr(r, "giris_fiyat", np.nan),
                 "durum": "AÇIK" if r.neden == "acik_veri_sonu" else f"{str(pd.Timestamp(r.cikis).date())} ({r.neden})", "ret": r.ret, "esli": r.esli,
                 "min": r.min, "max": r.max, "K": "".join(k[1] for k in BK_KOSUL if isinstance(getattr(r, k), (bool, np.bool_)) and bool(getattr(r, k)))}
            if j is not None and d is not None and _bk_sonlu(x["giris_fiyat"]):
                x["bugune"] = A["Cf"][-1, j] / x["giris_fiyat"] - 1
            kz.append(x)
    S["kriz"] = {"n": len(kz), "acik": sum(1 for r in kz if r["durum"] == "AÇIK"), "donemler": kz}
    S["bitis"] = _bi_simdi()
    os.makedirs(BI_YOL["is"], exist_ok=True)
    H["T"].to_csv(_bk_is("temiz"), index=False)
    pd.concat([Ya.assign(yon="alim"), Ys.assign(yon="satim")], ignore_index=True).to_csv(_bk_is("a"), index=False) if len(Ya) else None
    if len(M):
        M.to_csv(_bk_is("fifo"), index=False)
    X.to_csv(_bk_is("tetik"), index=False)
    if satirlar:
        pd.concat(satirlar, ignore_index=True).to_csv(_bk_is("b"), index=False)
    if b60:
        pd.concat(b60, ignore_index=True).to_csv(_bk_is("b60"), index=False)
    _bi_json(_bk_yol("sonuc", kl), S); _bi_yaz(_bk_yol("rapor", kl), bk_rapor_md(_bi_kayit(S), E))
    return S


# ---------------------------------------------------------------- RAPOR
def bk_ozet_satirlari(S: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> List[str]:
    """Raporun başındaki düz dil özet (yalnız sonuç JSON'undaki sayılardan)."""
    E = E or BK_ESIK; A = S.get("A") or {}; Kr = A.get("kirilim") or {}; B = S.get("B") or {}; ana = E["B"]["ana"]
    a20 = (Kr.get("20") or {}).get("tum") or {}; a60 = (Kr.get("60") or {}).get("tum") or {}; a5 = (Kr.get("5") or {}).get("tum") or {}
    ff = A.get("fifo") or {}; ft = ff.get("tum") or {}
    sat = ["## Özet (düz dil)", ""]
    sat.append(f"- BofA'nın yayımlanan maliyetinden (kesik içi, n {a20.get('n', 0)} alım satırı, {a20.get('hisse', '—')} hisse): 5 gün sonra medyan "
               f"{_p(a5.get('medyan'))}, 20 gün sonra medyan {_p(a20.get('medyan'))} (kâr oranı {_o(a20.get('kar_orani'))}, ortalama {_p(a20.get('ort'))}), "
               f"60 gün sonra medyan {_p(a60.get('medyan'))} (kâr oranı {_o(a60.get('kar_orani'))}, n {a60.get('n', 0)}). Aynı gün benzer hisselere göre "
               f"20 gün eşli fark ortalaması {_p(a20.get('esli_fark_ort'))}, 60 gün {_p(a60.get('esli_fark_ort'))}.")
    k20 = (Kr.get("20") or {}).get("kriz_sonrasi (BİLGİ)") or {}
    if k20.get("n"):
        sat.append(f"- Kriz sonrası (veri günü >= 01.09.2026, BİLGİ): BofA alımları 20 gün sonra kendi maliyetinden medyan {_p(k20.get('medyan'))}, kâr oranı "
                   f"{_o(k20.get('kar_orani'))}, P(<= -%30) {_o(k20.get('p_alt30'))} (n {k20.get('n')}); benzer hisselere göre eşli fark {_p(k20.get('esli_fark_ort'))}.")
    en = []
    for k in ("20", "60"):
        for ad, o in (Kr.get(k) or {}).items():
            if ad.startswith("_") or ad == "tum" or not isinstance(o, dict) or (o.get("n") or 0) < 20 or o.get("esli_fark_ort") is None:
                continue
            en.append((k, ad, o))
    if en:
        iy = max(en, key=lambda z: z[2]["esli_fark_ort"]); ko = min(en, key=lambda z: z[2]["esli_fark_ort"])
        sat.append(f"- En iyi kırılım (n >= 20): {iy[0]} gün '{iy[1]}' eşli fark {_p(iy[2]['esli_fark_ort'])} (kâr oranı {_o(iy[2]['kar_orani'])}, "
                   f"n {iy[2]['n']}); en kötü: {ko[0]} gün '{ko[1]}' {_p(ko[2]['esli_fark_ort'])} (kâr oranı {_o(ko[2]['kar_orani'])}, n {ko[2]['n']}). "
                   "Kırılımlar çoklu karşılaştırmadır, BİLGİ.")
    sat.append(f"- FIFO (yayımlanan lot listeleri, alım -> sonraki satış): {ft.get('n', 0)} eşleşme, lot ağırlıklı gerçekleşen getiri "
               f"{_p(ft.get('ret_lot_agirlik'))}, medyan {_p(ft.get('ret_medyan'))}, kârlı eşleşme {_o(ft.get('kar_orani'))}, tutma medyan "
               f"{_k(ft.get('gun_medyan'))} gün; kesik içi {(ff.get('kesik_ici') or {}).get('n', 0)} eşleşme, kriz sonrası {(ff.get('kriz_sonrasi') or {}).get('n', 0)} "
               f"(BİLGİ). Kapsam düşük: alınan lotun {_o(ff.get('kapsam'))}'i yayımlanmış bir satışla eşlenebildi (denetim notu: bölüm 9).")
    t = B.get("TUM") or {}; to = (t.get("yol") or {}).get(ana) or {}
    sat.append(f"- Haber sonrası giriş (Cemal'in yolu, G1 + C1, TÜMÜ): n {to.get('n', 0)}, eşli fark {_p(to.get('ort_fark'))} "
               f"[{_p(to.get('alt95'))}, {_p(to.get('ust95'))}], sıra {_k(to.get('sira'))}; geç kalma (giriş / BofA maliyeti - 1) medyan "
               f"{_p(to.get('gec_medyan'))} (n {to.get('gec_n', 0)}).")
    tum_ = [(ad, (B.get(ad) or {}).get("yol", {}).get(ana) or {}) for ad in BK_SATIR]
    iyi = [z for z in tum_ if (z[1].get("n") or 0) >= E["karar"]["n_min"]]
    if iyi:
        b_ = max(iyi, key=lambda z: z[1]["ort_fark"])
        sat.append(f"- 7 satır içinde (n >= 30) en yüksek eşli fark: {b_[0]} ({E['B']['kosul'].get(b_[0], 'TÜMÜ')}) {_p(b_[1].get('ort_fark'))} "
                   f"[{_p(b_[1].get('alt95'))}, {_p(b_[1].get('ust95'))}], n {b_[1].get('n')}; karar: {(B.get(b_[0]) or {}).get('karar', {}).get('karar')}.")
    kuc = [z for z in tum_ if 0 < (z[1].get("n") or 0) < E["karar"]["n_min"]]
    if kuc:
        sat.append("- n < 30 (örneklem yetersiz, karar dışı): " + "; ".join(
            f"{a} {_p(o.get('ort_fark'))} [{_p(o.get('alt95'))}, {_p(o.get('ust95'))}] n {o.get('n')}" for a, o in kuc) + ".")
    sat.append(f"- KARAR: {S.get('B_ozet_karar', '—')}. Karar en fazla BIST-ADAY olabilir (AKD verisi yalnız BIST'te; ABD / Avrupa hücresi yok).")
    kz = S.get("kriz") or {}
    sat.append(f"- Kriz sonrası (01.09.2026'dan, BİLGİ): {kz.get('n', 0)} BofA dönemi, {kz.get('acik', 0)} hâlâ açık (tablo bölüm 6).")
    return sat


def bk_rapor_md(S: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or BK_ESIK; A = S.get("A") or {}; Kr = A.get("kirilim") or {}; B = S.get("B") or {}; I6 = S.get("ikincil") or {}; ana = E["B"]["ana"]
    sy = S.get("sayim") or {}; tz = sy.get("temizlik") or {}
    sat = ["# BofA kendi maliyetinden kâr ediyor mu; haber sonrası yol var mı — sonuç (13 Kasım 2026)", "",
           "Soru (Cemal, 13.11.2026): 'BofA bir hissede %40-80 zarar etmez; senin mantığın bunu alıyor mu? Bana bir yol gösterecekse ölç.' "
           "A: BofA'nın yayımlanan ortalama maliyetinden getiri (betimleyici). B: haber anında bilinen 6 koşulla haber sonrası giriş (ön kayıtlı karar).", "",
           *bk_ozet_satirlari(S, E), "",
           "## 1. A — BofA'nın kendi maliyetinden getirisi (alım satırları, pencere sonu <= 31.08.2026)", "",
           "| kırılım | ufuk | n | kâr oranı | medyan | ortalama | P(>= +%30) | eş P | kat | P(<= -%30) | eş P | kat | eşli fark ort. / medyan |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in [str(x) for x in E["A"]["ufuk"]]:
        for ad, o in (Kr.get(k) or {}).items():
            if ad.startswith("_") or not isinstance(o, dict):
                continue
            if not o.get("n"):
                sat.append(f"| {ad} | {k} | 0 | | | | | | | | | | |"); continue
            sat.append(f"| {ad} | {k} | {o['n']} | {_o(o.get('kar_orani'))} | {_p(o.get('medyan'))} | {_p(o.get('ort'))} | {_o(o.get('p_ust30'))} | "
                       f"{_o(o.get('es_p_ust30'))} | {_k(o.get('kat_ust30'))} | {_o(o.get('p_alt30'))} | {_o(o.get('es_p_alt30'))} | {_k(o.get('kat_alt30'))} | "
                       f"{_p(o.get('esli_fark_ort'))} / {_p(o.get('esli_fark_medyan'))} |")
    sat += ["", f"Pencere sayımı (ana / kesik aşan / kriz sonrası / pencere yok): " + "; ".join(
        f"{k} gün {json.dumps((Kr.get(k) or {}).get('_sayim', {}), ensure_ascii=False)}" for k in [str(x) for x in E["A"]["ufuk"]]) + ".", ""]
    hf = A.get("haftalik") or {}
    if hf:
        sat.append("Haftalık listeler (BİLGİ, haftalık maliyet): " + "; ".join(
            f"{k} gün n {((hf.get(k) or {}).get('tum') or {}).get('n', 0)}, medyan {_p(((hf.get(k) or {}).get('tum') or {}).get('medyan'))}, kâr oranı "
            f"{_o(((hf.get(k) or {}).get('tum') or {}).get('kar_orani'))}, eşli fark {_p(((hf.get(k) or {}).get('tum') or {}).get('esli_fark_ort'))}"
            for k in [str(x) for x in E["A"]["ufuk"]]) + ".")
    sb = A.get("satis_bilgi") or {}
    if sb:
        sat.append("Satış satırları (BİLGİ; işaretli: BofA sattıktan sonra fiyat düşerse +): " + "; ".join(
            f"{k} gün n {(sb.get(k) or {}).get('n', 0)}, işaretli medyan {_p((sb.get(k) or {}).get('isaretli_medyan'))}, kâr oranı "
            f"{_o((sb.get(k) or {}).get('kar_orani'))}, işaretli eşli fark {_p((sb.get(k) or {}).get('isaretli_esli_fark'))}" for k in sb) + ".")
    ff = A.get("fifo") or {}
    sat += ["", "### FIFO: yayımlanan lot alımları -> sonraki yayımlanan lot satışları", "",
            f"Alım satırı {ff.get('alim_satir', 0)}, satış satırı {ff.get('satim_satir', 0)}; alınan {_k(ff.get('alinan_lot'))} lot, eşlenen "
            f"{_k(ff.get('eslesen_lot'))} (kapsam {_o(ff.get('kapsam'))}); eşleşmeyen satış {_k(ff.get('eslesmeyen_satis_lot'))} lot (BofA'nın listede görünmeyen "
            f"eski pozisyonu ya da açığa satış). Açıkta kalan alım: {json.dumps(_bi_kayit(ff.get('acik', {})), ensure_ascii=False)}.", "",
            "| küme | eşleşme | hisse | lot ağırlıklı getiri | medyan | ortalama | kârlı (adet / lot) | tutma medyan (gün) | P(>= +%30) | P(<= -%30) |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for ad in ("tum", "kesik_ici", "kriz_sonrasi"):
        o = ff.get(ad) or {}
        sat.append(f"| {ad} | {o.get('n', 0)} | {o.get('hisse', '')} | {_p(o.get('ret_lot_agirlik'))} | {_p(o.get('ret_medyan'))} | {_p(o.get('ret_ort'))} | "
                   f"{_o(o.get('kar_orani'))} / {_o(o.get('kar_orani_lot'))} | {_k(o.get('gun_medyan'))} | {_o(o.get('p_ust30'))} | {_o(o.get('p_alt30'))} |")
    if ff.get("hisse"):
        sat += ["", "FIFO hisse bazında (en çok eşlenen TL, BİLGİ): " + "; ".join(
            f"{r['hisse']} {r['n']} eşleşme, {_p(r['ret'])}, tutma {_k(r['gun'])} g" for r in ff["hisse"][:10]) + "."]
    h20 = A.get("hisse20") or []
    if h20:
        sat += ["", "Hisse bazında 20 gün (en az 3 satır, BİLGİ): " + "; ".join(
            f"{r['hisse']} n {r['n']} medyan {_p(r['medyan'])} eşli {_p(r['esli_fark'])}" for r in h20[:12]) + "."]
    ks = A.get("kriz_satir") or []
    if ks:
        sat += ["", f"Kriz sonrası maliyetli alım satırları (BİLGİ, ilk 12 / {len(ks)}): " + "; ".join(
            f"{r.get('hisse')} {str(r.get('veri_gunu'))[:10]} maliyet {_k(r.get('maliyet'))} r5 {_p(r.get('r5'))} r20 {_p(r.get('r20'))}" for r in ks[:12]) + "."]
    sat += ["", f"## 2. B — KARAR TABLOSU (ANA yol {ana}: {E['B']['giris']['G1']}; çıkış {E['B']['cikis']['C1'][:60]}...)", "",
            "| satır | koşul | n | eşli fark ort. [%95] | sıra | portföy / rastgele %90 | A (2023-24) / B (2025-26) | p | BH | KARAR | tutmayan |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for ad in BK_SATIR:
        b = B.get(ad) or {}; o = (b.get("yol") or {}).get(ana) or {}; kk = b.get("karar") or {}
        sat.append(f"| {ad} | {E['B']['kosul'].get(ad, 'TÜMÜ (koşulsuz)')[:70]} | {o.get('n', 0)} | {_p(o.get('ort_fark'))} [{_p(o.get('alt95'))}, "
                   f"{_p(o.get('ust95'))}] | {_k(o.get('sira'))} | {_p(o.get('portfoy'), 0)} / {_p(o.get('portfoy_esli_p90'), 0)} | "
                   f"{_p((o.get('yari_A') or {}).get('ort_fark'))} (n {(o.get('yari_A') or {}).get('n', 0)}) / {_p((o.get('yari_B') or {}).get('ort_fark'))} "
                   f"(n {(o.get('yari_B') or {}).get('n', 0)}) | {_k(b.get('p'))} | {'red' if b.get('bh_red') else 'yok'} | **{kk.get('karar', '—')}** | "
                   f"{'; '.join(kk.get('tutmayan', []))} |")
    sat += ["", "## 3. OLASILIK TABLOSU (ana tablo; kat = olay / aynı gün aynı hücre eşleri)", "",
            "| satır | dönem n | dönem getirisi ort. / medyan | P(dönem >= +%50) | eş | kat | P(dönemde -%30'a dokunma) | 20g n | P(+%50, 20g) | kat | "
            "P(-%30, 20g) | kat | r20 ort. / eş |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for ad in BK_SATIR:
        o = ((B.get(ad) or {}).get("yol") or {}).get(ana) or {}; i6 = I6.get(ad) or {}
        sat.append(f"| {ad} | {o.get('n', 0)} | {_p(o.get('ort_ret'))} / {_p(o.get('medyan_ret'))} | {_o(o.get('p_ret50'))} | {_o(o.get('b_ret50'))} | "
                   f"{_k(o.get('kat_ret50'))} | {_o(o.get('p_min30'))} | {i6.get('n20', 0)} | {_o(i6.get('p_up50'))} | {_k(i6.get('kat_up50'))} | "
                   f"{_o(i6.get('p_dn30'))} | {_k(i6.get('kat_dn30'))} | {_p(i6.get('r20'))} / {_p(i6.get('b_r20'))} |")
    sat += ["", "12 ay +%100 olasılığı bu veride ölçülmedi (maliyetli listeler 2025-26, kriz kesiği): 20 gün ve dönem olasılıkları yazıldı.", "",
            "## 4. Yol varyantları ve duyarlılık (BİLGİ; eşli fark ort. [%95], n)", "",
            "| satır | G1C1 (ANA) | G1C2 (20 gün) | G2C1 (ertesi açılış) | G2C2 | düz yazı hariç (G1C1) | tamamlayıcı (koşul yok, G1C1) | süre medyan | geç kalma medyan |",
            "|---|---|---|---|---|---|---|---|---|"]
    f_ = lambda o: f"{_p(o.get('ort_fark'))} [{_p(o.get('alt95'))}, {_p(o.get('ust95'))}] n {o.get('n', 0)}" if o.get("n") else "n 0"  # noqa: E731
    for ad in BK_SATIR:
        b = B.get(ad) or {}; y = b.get("yol") or {}
        sat.append(f"| {ad} | {f_(y.get('G1C1') or {})} | {f_(y.get('G1C2') or {})} | {f_(y.get('G2C1') or {})} | {f_(y.get('G2C2') or {})} | "
                   f"{f_(b.get('duzyazi_haric') or {})} | {f_(b.get('tamamlayici') or {}) if ad != 'TUM' else '—'} | {_k((y.get(ana) or {}).get('gun_medyan'))} | "
                   f"{_p((y.get(ana) or {}).get('gec_medyan'))} |")
    sat += ["", "## 5. İkincil: FI_OLCUT 60 gün (giriş ertesi açılış, 60 günde tek olay)", "",
            "| satır | n (60g) | eşli fark [%95] | sıra | portföy / rastgele %90 | A / B | karar (ikincil) |", "|---|---|---|---|---|---|---|"]
    for ad in BK_SATIR:
        i6 = I6.get(ad) or {}; fi = i6.get("fi") or {}
        sat.append(f"| {ad} | {fi.get('n', 0)} | {_p(fi.get('ort_fark'))} [{_p(fi.get('alt95'))}, {_p(fi.get('ust95'))}] | {_k(fi.get('sira'))} | "
                   f"{_p(fi.get('portfoy'), 0)} / {_p(fi.get('portfoy_esli_p90'), 0)} | {_p(i6.get('yari_A'))} / {_p(i6.get('yari_B'))} | "
                   f"{(i6.get('karar') or {}).get('karar', '—')} |")
    kz = S.get("kriz") or {}
    sat += ["", f"## 6. Kriz sonrası BofA dönemleri (giriş >= 01.09.2026, TÜMÜ, G1C1; BİLGİ, karara girmez). {kz.get('n', 0)} dönem, {kz.get('acik', 0)} açık", "",
            "| hisse | tetik haberi | tür / sıra / birim | BofA maliyet | giriş (tür) | durum | dönem getirisi | eş | en düşük | en yüksek | bugüne | koşullar |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    T_ = sorted(kz.get("donemler", []), key=lambda r: (r.get("durum") != "AÇIK", r.get("giris", "")))
    for r in T_[:30]:
        sat.append(f"| {r.get('hisse')} | {r.get('tetik_yayin')} | {r.get('tur')} / {r.get('sira')} / {r.get('birim')} | {_k(r.get('maliyet'))} | "
                   f"{r.get('giris')} ({r.get('giris_tip')}) | {r.get('durum')} | {_p(r.get('ret'))} | {_p(r.get('esli'))} | {_p(r.get('min'))} | "
                   f"{_p(r.get('max'))} | {_p(r.get('bugune'))} | {r.get('K') or '—'} |")
    if len(T_) > 30:
        sat.append(f"| … {len(T_) - 30} dönem daha (bofa_kar_sonuc.json 'kriz') | | | | | | | | | | | |")
    sat += ["", "## 7. Temizlik sayımı", "",
            f"Kapsam satırı {tz.get('kapsam_satir', '—')}, geçerli {tz.get('gecerli', '—')}. Düşen (ilk tutmayan neden): "
            f"{json.dumps(tz.get('dusen', {}), ensure_ascii=False)}; yön x neden {json.dumps(tz.get('dusen_yon', {}), ensure_ascii=False)}. Düz yazı satırı "
            f"{tz.get('duzyazi_kapsam', '—')} (geçerli {tz.get('duzyazi_gecerli', '—')}). Geçerli maliyetli: {json.dumps(tz.get('gecerli_maliyetli', {}), ensure_ascii=False)}; "
            f"payı yazılı {tz.get('gecerli_payli', '—')}. B tetik sayımı: {json.dumps(_bi_kayit((sy.get('B') or {}).get('bayrak', {})), ensure_ascii=False)}.", "",
            "## 8. Sınırlar", "", E["yanlilik"], "",
            "Kapsam dışı BofA satırları (haberdeki 2. ve sonraki listeler, aylık): "
            f"{json.dumps(_bi_kayit(tz.get('kapsam_disi_BofA', {})), ensure_ascii=False)}.", "",
            "AKD verisi yalnız BIST'te: CLAUDE.md karar hücreleri (ABD 2023 / 2024-26, Avrupa 2023 / 2024-26) bu soruda yoktur; en iyi sonuç 'BIST-ADAY' olur, "
            "İZ değildir. Kırılımlar ve varyantlar çoklu karşılaştırmadır.", "",
            f"Mühür {S.get('esik_sha', '')[:12]}; kapı {json.dumps(_bi_kayit((S.get('kapi') or {}).get('onkayit_git', {})), ensure_ascii=False)}"
            + (f"; SAPMA: {S['kapi']['sapma']}" if (S.get("kapi") or {}).get("sapma") else "") + f". Son veri {S.get('son_gun', '—')}.", "",
            "## 9. Denetim notu (ölçümden sonra; gösterim, SAPMA değil; karar değişmez)", "",
            "- 01.09.2026 11:40 hisse.net 'Bank of America Ağustos'ta bu BIST hisselerine milyarlar yatırdı' haberi AYLIK özettir; ayrıştırıcı gün içi "
            "liste ve 'lot' birimli okudu (tutarlar TL; maliyet Ağustos ortalaması). Etkisi: A'da 7 kriz sonrası satır, B'de 2 kriz sonrası tetik "
            "(TRALT, ASTOR; kesik dışı, karara girmez) ve FIFO'nun lot toplamları (alınan / eşleşmeyen lot ve kapsam şişkin). Bu haber hariç FIFO "
            "(denetim yeniden hesabı): 84 eşleşme, lot ağırlıklı -%3,2, medyan -%2,2, kârlı %37, kapsam %40; yine yalnız kriz sonrası. 17.06.2025 "
            "YatırımX 'TERA bastırıyor' gibi bazı lot etiketli satırlar da TL tutarı olabilir; lot ağırlıkları bu yüzden kaba.",
            "- DUNYH (12.11.2026) giriş fiyatı bayat Yahoo fiyatı (giriş günü hacim 0, Ç171'de işaretlendi); -%85 gerçek değildir.", ""]
    return "\n".join(sat)


def bk_rapor(kl: Optional[str] = None) -> str:
    try:
        with open(_bk_yol("sonuc", kl), encoding="utf-8") as f:
            S = json.load(f)
    except (OSError, ValueError) as ex:
        raise BiHata(f"BofA kâr sonucu okunamadı: {ex}") from ex
    return _bi_yaz(_bk_yol("rapor", kl), bk_rapor_md(S))


# ---------------------------------------------------------------- 12) ÇAKIŞMA KAPISI
def _cakisma_kontrol_bi(_once=_CK_ONCE_BI, _dosya="BOFA_IZI.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_BI", "_CK_KAYIT", "_cakisma_kontrol_bi", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "re", "hashlib", "http", "subprocess", "time", "_dt", "_html", "urllib", "annotations",
           "Any", "Callable", "Dict", "List", "Optional", "Tuple", "_p", "_o", "_k")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_bi()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=BI_SURUM)
    ap.add_argument("komut", choices=["topla", "onkayit", "kos", "rapor", "izle", "karonkayit", "karkos", "karrapor"])
    ap.add_argument("--site", default="hissenet,yatirimx,rotaborsa")
    ap.add_argument("--sinir", type=int, default=None)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--sapma", default=None, help="kos: ön kayıttan sonra kod değiştiyse gerekçe (sonuca yazılır)")
    ap.add_argument("--tek", action="store_true", help="izle: tek tur (zorunlu; sürekli izleme bu dosyada kurulmaz)")
    a_ = ap.parse_args()
    try:
        _fh = logging.FileHandler(_bi_is("log"), encoding="utf-8") if os.path.isdir(BI_YOL["is"]) else None
        if _fh:
            _fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s")); bilog.addHandler(_fh)
        if a_.komut == "topla":
            print(json.dumps(_bi_kayit(bi_topla(tuple(a_.site.split(",")), a_.sinir)), ensure_ascii=False))
        elif a_.komut == "onkayit":
            y_ = bi_onkayit(a_.cikti); print(y_, "mühür", bi_esik_sha(), "kod", bi_kod_sha(), "dosya", bi_sha_dosya(y_))
        elif a_.komut == "kos":
            s_ = bi_kos(a_.cikti, sapma=a_.sapma); print(json.dumps(_bi_kayit({"ana": s_.get("karar"), "ikincil": s_.get("karar60")}), ensure_ascii=False))
            print(_bi_yol("rapor", a_.cikti))
        elif a_.komut == "izle":
            if not a_.tek:
                raise BiHata("izle yalnız --tek ile (tek tur) çalışır; sürekli izleme kurulmadı")
            T_, _g = bi_izle_tur(set()); print(T_.to_string() if len(T_) else "yeni BofA listesi yok")
        elif a_.komut == "karonkayit":
            y_ = bk_onkayit(a_.cikti); print(y_, "mühür", bk_esik_sha(), "kod", bi_kod_sha(), "dosya", bi_sha_dosya(y_))
        elif a_.komut == "karkos":
            s_ = bk_kos(a_.cikti, sapma=a_.sapma); print(json.dumps(_bi_kayit({"B": s_.get("B_karar"), "ozet": s_.get("B_ozet_karar")}), ensure_ascii=False))
            print(_bk_yol("rapor", a_.cikti))
        elif a_.komut == "karrapor":
            print(bk_rapor(a_.cikti))
        else:
            print(bi_rapor(a_.cikti))
    except (BiHata, FileNotFoundError) as ex:
        bilog.error("%s", ex); sys.exit(1)
