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
    return {"tarih": idx, "sembol": S, "kol": {s: i for i, s in enumerate(S)}, "Op": Op, "Hh": Hh, "Ll": Ll, "Cf": Cf, "H": Hc, "ok": ok, "dd": dd}


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
                    "cokmus": bool(dd <= cokmus) if np.isfinite(dd) else None, "olcuk": True})
    Y = X.copy().reset_index(drop=True)
    for k in ("ret", "max", "min", "esli", "fark", "sira", "_esler", "gun", "gec", "cokmus", "olcuk"):
        Y[k] = [s[k] for s in sat]
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
        o = bi_donem_ozet(Yk, yari); o["toplam_donem"] = int(len(Y))
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
                f"{a.get('gun_q', '—')}. Geç kalma (bizim giriş / BofA maliyeti - 1) medyan {_p(a.get('gec_medyan'))} (n {a.get('gec_n', '—')}). "
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
        for kod, r in sorted(acik, key=lambda x: (x[0], str(x[1].get("giris"))))[:30]:
            sat.append(f"| {kod} | {r.get('hisse')} | {str(r.get('acilis_yayin'))[:16]} | {str(r.get('giris'))[:10]} | {_p(r.get('bugune'))} | "
                       f"{_p(r.get('bugune_min'))} | {_p(r.get('bist_bugune'))} |")
        if len(acik) > 30:
            sat.append(f"| … {len(acik) - 30} daha (bofa_sonuc.json) | | | | | | |")
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
    for r in T[:22]:
        dur = "AÇIK (BofA tutuyor)" if r.get("acik") else f"{str(r.get('cikis'))[:10]} ({r.get('neden')})"
        sat.append(f"| {r.get('hisse')} | {str(r.get('acilis_yayin'))[:16]} ({r.get('acilis_tur')}) | {r.get('acilis_sira')} | {_k(r.get('bofa_maliyet'))} | "
                   f"{str(r.get('giris'))[:10]} | {dur} | {_p(r.get('ret'))} | {_p(r.get('esli'))} | {_p(r.get('min'))} | {_p(r.get('max'))} | "
                   f"{_p(r.get('bugune'))} | {_p(r.get('bist_bugune'))} |")
    if len(T) > 22:
        sat.append(f"| … {len(T) - 22} dönem daha (bofa_sonuc.json 'kriz') | | | | | | | | | | | |")
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


def bi_rapor(kl: Optional[str] = None) -> str:
    try:
        with open(_bi_yol("sonuc", kl), encoding="utf-8") as f:
            S = json.load(f)
    except (OSError, ValueError) as ex:
        raise BiHata(f"sonuç okunamadı: {ex}") from ex
    return _bi_yaz(_bi_yol("rapor", kl), bi_rapor_md(S))


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
    ap.add_argument("komut", choices=["topla", "onkayit", "kos", "rapor", "izle"])
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
        else:
            print(bi_rapor(a_.cikti))
    except (BiHata, FileNotFoundError) as ex:
        bilog.error("%s", ex); sys.exit(1)
