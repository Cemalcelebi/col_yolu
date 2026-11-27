"""DOJI_OBEK — aynı fiyat seviyesinde, aralarında en çok iki mum olan DOJİ ÖBEKLERİ: tespit, sıklık, Cemal için gerçek örnekler ve doji sayısına göre
SONRASI (yön, hareketin büyüklüğü, öbek bandından çıkış yönü ve devamı, önceki yöne göre dönüş / devam, doz - yanıt) (27 Kasım 2026).

İş tanımı: arastirma_cikti/doji_obek/DJ_IS_TANIMI.md (ana model; eşikler sabit). Günlük mum ANA; haftalık ve D15 (gövde <= 0,15 boy) BİLGİ.
Veri: YUKSELIS_ONCESI ham bar deposu (ham_{ABD,AVR}.npz; YO ön kaydında sha ile mühürlü; MUM_IZI.mi_veri geçerli barları + KART_TUR2 P2 evreni).
Evren, giriş, 15 bar penceresi, ATRP20, KONUM120, T1 (aynı hissenin aynı hücredeki örnek günlerinin R15 ortalaması), PİYASA(t) = P15(d), 'önce hangisine
dokundu' vektörü, hücre adı: YUKSELIS_ONCESI / MUM_IZI_HAVUZ ile aynı (içe alınır, kopyalanmaz). Veri <= 2022-12-31 (assert). KASA AÇILMAZ.

Komut:  python DOJI_OBEK.py hazirla    doji / öbek tespiti -> olay + taban dosyaları (GETİRİSİZ) -> /root/.kasa/ham/doji_obek
        python DOJI_OBEK.py sayim      GETİRİSİZ SAYIM (dj_sayim.json; R15 hesaplanmaz)
        python DOJI_OBEK.py ornek      DJ_ORNEKLER.pdf (gerçek örnekler; sonrası çizilmez)
        python DOJI_OBEK.py onkayit    DJ_ON_KAYIT.md (mühürler + sayım + yorum noktaları + kontrol tablosu)
        python DOJI_OBEK.py olcum      kapı (ön kayıt commit + push + kontrol + sha) -> ölçüm (BİR KEZ) -> dj_sonuc.json + dj_ozet.csv
        python DOJI_OBEK.py rapor      DJ_RAPOR.md (sonuç json'undan; yeniden üretim ve HATA / SAPMA ham klasördeki dj_rapor_ek.json'dan)
        python DOJI_OBEK.py sha        kod / eşik sha
Colab:  exec(open('DOJI_OBEK.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7: sonuç yukarı yanlı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_DJ = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import time  # noqa: E402
import zlib  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_DJ = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_DJ not in sys.path:
    sys.path.insert(0, KOK_DJ)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ; yazma + sızıntı taraması, sha, git, mum çizimi)
import MUM_IZI_HAVUZ as HV  # noqa: E402  (DEĞİŞTİRİLMEZ; ay özeti, BH, hücre adı, json sha)
import YUKSELIS_ONCESI as YO  # noqa: E402  (DEĞİŞTİRİLMEZ; örnek maskesi, ATRP20 / KONUM120, dokunma, P15, bootstrap yüzdeliği)

djlog = logging.getLogger("col.doji_obek")
if not djlog.handlers:
    _dj_h = logging.StreamHandler(sys.stderr)
    _dj_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s doji_obek: %(message)s", "%H:%M:%S"))
    djlog.addHandler(_dj_h)
    djlog.setLevel(logging.INFO)
    djlog.propagate = False


class DJHata(RuntimeError):
    """Durdurucu hata: kapı / şema / veri / kesik / sıra / yeniden üretim uyuşmazlığı."""


DJ_SURUM = "DOJI_OBEK v1.0 (2026-11-27): aynı seviyede doji öbekleri; doji sayısına göre sonrası"
DJ_YOL = {"cikti": os.path.join(KOK_DJ, "arastirma_cikti", "doji_obek"), "kod": os.path.join(KOK_DJ, "DOJI_OBEK.py"),
          "ham": os.environ.get("DJ_HAM", "/root/.kasa/ham/doji_obek"), "kaynak": os.environ.get("DJ_KAYNAK", YO.YO_YOL["ham"]),
          "is_tanimi": os.path.join(KOK_DJ, "arastirma_cikti", "doji_obek", "DJ_IS_TANIMI.md")}
DJ_DOSYA = {"onkayit": "DJ_ON_KAYIT.md", "rapor": "DJ_RAPOR.md", "sonuc": "dj_sonuc.json", "ozet": "dj_ozet.csv", "pdf": "DJ_ORNEKLER.pdf"}
DJ_KESIK = pd.Timestamp("2022-12-31")
DJ_PAZAR = ("ABD", "AVR")
DJ_HUCRE = ("ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022")
DJ_ABD = ("ABD|d1619", "ABD|d2022")
DJ_AVR = ("AVR|d1619", "AVR|d2022")
DJ_KSIN = (1, 2, 3, 4)                       # 4 = '4+' (öbeğin 4. dojisi; öbek başına bir olay)
DJ_KAD = {1: "k=1 (tek doji)", 2: "k=2", 3: "k=3", 4: "k=4+"}
DJ_KOL = ("ANA", "D15", "HAFTA")

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
DJ_ESIK: Dict[str, Any] = {
    "surum": "DJ-1.0",
    "tohum": 2712,
    "tohum_tanim": "np.random.default_rng([2712, crc32(anahtar)]); bootstrap anahtarı satır adı; PDF örnek seçimi anahtar 'ornek|k'",
    "veri": "YUKSELIS_ONCESI ham bar deposu ham_{pazar}.npz (O/H/L/C hissenin kendi geçerli barları: MUM_IZI.mi_veri H > L, V > 0, O/H/L/C sonlu > 0; POS = "
            "birleşik takvim satırı; Op / Cl / P2 = pazar paneli; KART_TUR2.k2_panel P2 evreni); sha YO_ON_KAYIT.md 'DOJSA_ham_*' ile aynı olmalı (DUR)",
    "doji": {"govde": 0.10, "govde_D15": 0.15, "boy_oran": 0.5, "ort_boy_bar": 10, "adim_pencere": 20, "adim_kat": 3,
             "tanim": "DOJİ(t) <=> |C - O| <= govde x (H - L) VE (H - L) >= 0,5 x ORT_BOY(t) VE (H - L) > 0 VE ölü değil; ORT_BOY(t) = t - 10 .. t - 1 "
                      "barlarının (H - L) medyanı (10 önceki bar yoksa doji değil); ÖLÜ = (a) geçersiz bar (veride yok: H <= L, V = 0, kilitli; MI.mi_veri), "
                      "(b) FİYAT ADIMINA YAPIŞMIŞ: (H - L) <= 3 x ADIM(t), ADIM(t) = t - 19 .. t barlarının O/H/L/C değerlerinin sıralı farklarının en küçük "
                      "pozitifi (> 1e-9 x C_t; 20 bar yoksa bu süzgeç uygulanmaz, doji zaten ORT_BOY şartından düşer); ayrıca öbek içinde iki doji arası "
                      "takvim satırı farkı > 6 ise (arada kilitli / işlemsiz günler) bağlanmaz"},
    "seviye": "SEVİYE(t) = (O_t + C_t) / 2",
    "obek": {"ara_en_cok": 3, "takvim_ara_en_cok": 6, "bant_atr": 0.5, "atr": "ATR20(t) = ATRP20(t) x C_t (YO.yo_hisse_ozellik ATRP20: son 20 barın TR ortalaması)",
             "tanim": "dojiler sırayla gezilir; yeni doji d, açık öbeğe katılır <=> d - son_doji <= 3 (kendi geçerli bar sırası; aralarında en çok 2 mum) VE "
                      "POS(d) - POS(son_doji) <= 6 VE maks(seviye) - min(seviye) (öbekteki bütün dojiler + d) <= 0,5 x ATR20(d) (sınır DAHİL; göreli 1e-12 "
                      "pay) VE ATR20(d) sonlu; katılmazsa açık öbek biter ve d yeni öbeği başlatır (k = 1); öbek bandı = öbekteki dojilerin maks H / min L"},
    "olay": {"tanim": "olay = öbeğin k'inci dojisinin barı t (yalnız t'ye kadarki bilgi); k = 1 (öbeği başlatan doji: o an ikincisi yok = TEK DOJİ tabanı), "
                      "k = 2, k = 3, k = 4+ (= öbeğin 4. dojisi; 5. ve sonraki dojiler yeni olay üretmez: her satırda bir öbek bir kez)",
             "uygunluk": "YO.yo_ornek_maske kuralları HER BAR için (adım 5 yerine 1): t + 15 hissenin verisinde; POS(t + 1) - POS(t) <= 10; POS(t + 15) - "
                         "POS(t + 1) <= 29; giriş satırında P2; giriş tarihi 2016-01-01 .. 2022-12-31; 15. bar <= 2022-12-31; ATRP20(t) sonlu > 0"},
    "taban": "HERHANGİ GÜN = YO.yo_ornek_maske örnek günleri (hissenin her 5. geçerli barı; aynı uygunluk); T1 ve 'aynı hissenin rastgele günü' karşılıkları "
             "(hisse x hücre ortalaması) bu günlerden; olayın kendi hücresindeki hisse ortalaması yoksa olay düşer (sayılır)",
    "baglam": {"konum": [1 / 3, 2 / 3], "onceki_bar": 10,
               "tanim": "KONUM120 (YO; son 120 kapanış aralığında konum) < 1/3 DİPTE, < 2/3 ORTADA, aksi TEPEDE; ÖNCEKİ YÖN = C_t / C_{t-10} - 1 < 0 DÜŞÜŞ, > 0 "
                        "YÜKSELİŞ (= 0 ya da yok: ikisine de girmez)"},
    "sonuc": {"ufuk": 15, "hedef_atr": 2.0, "stop_atr": 1.0, "cikis_ufuk": 15, "devam": 10, "devam_satir": 19,
              "R15": "C_{t+15} / E0 - 1, E0 = O_{t+1} (giriş = sonraki geçerli bar açılışı)",
              "SECIM": "R15 - P15(d) (d = giriş satırı; YO.yo_P15: P2 hisselerinin eşit ağırlıklı 15 satır getirisi)",
              "TOPLAM_FARK": "R15 - T1(hisse, hücre)",
              "U2": "barlar t + 1 .. t + 15: ilk High >= E0 (1 + 2 ATRP20_t) barı, ilk Low <= E0 (1 - 1 ATRP20_t) barından ÖNCE (aynı bar = stop önce; "
                    "YO.yo_ilk_dokunma)", "D2": "ayna: ilk Low <= E0 (1 - 2 ATRP20_t), ilk High >= E0 (1 + 1 ATRP20_t)'den önce",
              "ASIMETRI": "(U2 - D2) - (p_h - q_h); p_h / q_h = aynı hissenin aynı hücredeki örnek günlerinin U2 / D2 ortalaması",
              "BUYUKLUK": "|R15| / (ATRP20_t x karekök 15); BUYUKLUK_FARK = BUYUKLUK - h_h (aynı hissenin örnek günleri); KAT = toplam BUYUKLUK / toplam h_h",
              "CIKIS": "barlar t + 1 .. t + 15 içinde ilk KAPANIŞ > bant üstü (YUKARI) ya da < bant altı (AŞAĞI); hiçbiri yoksa HİÇ; çıkış barı e",
              "DEVAM": "R10 = C_{e+10} / O_{e+1} - 1; DEVAM = R10 x (+1 yukarı, -1 aşağı); e + 10 verinin dışında ya da POS(e + 10) - POS(e + 1) > 19 ise "
                       "yok (sayılır); bilgi: T10 = aynı hissenin örnek günlerinde C_{t+10} / O_{t+1} - 1 ortalaması (sürüklenme)",
              "DONUS": "ÖNCEKİ YÖN DÜŞÜŞ: dönüş = R15 > 0; YÜKSELİŞ: dönüş = R15 < 0; taban = aynı hücrenin örnek günlerinde aynı önceki yöndeki dönüş payı "
                       "(havuz); DONUS_FARK = dönüş - taban"},
    "boot": {"B": 10000, "kume": "giriş ayı (YYYY-AA)",
             "tanim": "ay kümeli bootstrap: aylar yerine koyarak (multinomial ağırlık, tohum 2712); oran / ortalama her tekrarda ağırlıklı toplamlardan; "
                      "%95 = 2,5 / 97,5 yüzdelik (YO._q); k farkları (k - 1) aynı ağırlıklarla (iki grup aynı ay kümeleri); iki yönlü p = 2 x min(#(<= 0), "
                      "#(>= 0)) / B (en çok 1; (1 + #) / (B + 1) düzeltmeli)"},
    "bh": {"q": 0.10, "aile": "k (1, 2, 3, 4+) x ölçü (TOPLAM_FARK, SECIM, ASIMETRI, BUYUKLUK_FARK, DEVAM_YUKARI, DEVAM_ASAGI, DONUS_DUSUS, DONUS_YUKSELIS) = 32 "
                              "satır; satır p'si = ABD 2016-19 ve ABD 2020-22 iki yönlü p'lerinin büyüğü"},
    "hukum": {"n_min": 1000, "n_az": 30,
              "ARTI": "ABD iki dönemde TOPLAM FARK > 0 ve alt > 0 VE AVR iki dönemde nokta > 0 VE BH geçer",
              "EKSI": "ABD iki dönemde üst < 0 VE AVR iki dönemde nokta < 0 VE BH geçer",
              "sira": "ARTI / EKSİ > 'ABD İKİ DÖNEM, AVR UYMADI' (ABD şartı var, AVR işareti uymuyor) > 'BH GEÇMEDİ' (ABD + AVR şartı var, BH yok) > ÇELİŞKİLİ "
                      "(iki dönem zıt yönde ayrışıyor) > TEK DÖNEM (yalnız bir ABD döneminde aralık sıfırı dışlıyor) > AYRIŞMIYOR (iki dönemde aralık sıfırı "
                      "içeriyor ve iki dönemde n >= 1.000) > ÖLÇÜLEMEDİ (aralık sıfırı içeriyor, bir ABD döneminde n < 1.000)",
              "olcu": "aynı kural bütün ölçülere uygulanır (TOPLAM_FARK ana; SECIM, ASIMETRI, BUYUKLUK_FARK, DONUS_FARK, DEVAM satırları)",
              "DOZ": "'DOJİ SAYISI ETKİLİ' <=> üç ölçüden (TOPLAM_FARK, BUYUKLUK_FARK, YUKARI_CIKIS payı) en az biri için: (a) k = 1 -> 2 -> 3 -> 4+ nokta "
                     "değerleri ABD iki döneminde de tek yönlü (art arda farkların hepsi > 0 ya da hepsi < 0) ve iki dönemde aynı yönde, VE (b) (k = 3 - k = 1) "
                     "ya da (k = 4+ - k = 1) farkının aralığı iki ABD döneminde de sıfırı dışlıyor ve işareti (a)'daki yönle aynı; aksi 'DOJİ SAYISI ETKİSİZ' "
                     "(bu tanımla)",
              "CIKIS": "'ÇIKIŞ DEVAM EDİYOR' <=> DEVAM (yukarı çıkış ve aşağı çıkış ayrı satır) > 0 ve alt > 0 iki ABD döneminde; 'ÇIKIŞ TERSE DÖNÜYOR (tuzak)' "
                       "<=> iki dönemde üst < 0; aksi genel sıra (TEK DÖNEM / AYRIŞMIYOR / ÖLÇÜLEMEDİ)",
              "GENEL": "ARTI ya da EKSİ olan k satırı ya da DOJİ SAYISI ETKİLİ varsa 'AÇIK VERİDE EMARE (kasa açılmaz; KASA KURALI)'; yoksa 'DOJİ ÖBEĞİ SONRASI "
                       "AYIRT EDİCİ DEĞİL (bu tanımla)'"},
    "bilgi": {"D15": "gövde <= 0,15 boy (öteki her şey aynı); TOPLAM FARK k başına (bilgi, hüküm yok)",
              "HAFTA": "haftalık mumlar günlük geçerli barlardan (W-FRI haftası: O ilk, H maks, L min, C son); aynı doji / öbek kuralı (bar = hafta, ATR20 "
                       "haftalık, takvim satırı = hafta sırası); giriş = sonraki hafta açılışı; R15 = 15 hafta; T1 = hissenin aynı hücredeki bütün uygun "
                       "haftaları; giriş haftasının ilk günlük satırında P2; 15 hafta <= 29 hafta satırı; giriş 2016-2022, 15. hafta <= 2022-12-31; bilgi"},
    "ornek": {"k_basina": 4, "sayilmayan": 2, "once": 60, "yakin": 8,
              "tanim": "ANA olaylardan (iki pazar, iki dönem) k = 2 / 3 / 4+ için tohumla rastgele 4'er; sayılmayan 2 örnek: (a) önceki dojiyle arası <= 3 bar "
                       "ama seviye farkı > 0,5 ATR20 (SEVİYE FARKLI), (b) seviye farkı <= 0,5 ATR20 ama arası 4-6 bar (ARA UZAK); grafik olay barında biter "
                       "(sonrası yok), yüzde ekseni olay kapanışına göre; altta yakın görünüm (öbek + önceki 8 mum); hisse adı / tarih yok (pazar ve dönem yazılır)"},
    "kesik": "veri en büyük tarihi <= 2022-12-31 (assert; npz tarih)",
    "sira": "kod + sentetik test -> getirisiz sayım + DJ_ORNEKLER.pdf -> ön kayıt commit + push -> ik_kontrol_kapisi -> ölçüm (bir kez) -> rapor",
}

DJ_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban aynı hissenin aynı hücredeki rastgele (her 5. bar) günleri: TOPLAM FARK = R15 - T1, U2 / D2 / büyüklük için p_h / q_h / h_h aynı hisseden; "
                   "ATR ölçekli eşikler (oynaklığın mekanik etkisi ATRP20 ile ölçeklenir); D2 aynası ve asimetri mekanik üstünlüğü ölçer; tek doji (k = 1) ve herhangi "
                   "gün iki taban; k farkları aynı ay ağırlıklarıyla; SEÇİM = R15 - PİYASA(t)"),
    "K2": ("EVET", "doji / öbek / k t barına kadarki barlarla (test: t + 1 ve sonrası bozulunca olaylar aynı); ORT_BOY t - 10 .. t - 1; ATR20 ve ADIM t'ye kadar; "
                   "sonuç sütunları ayrı fonksiyonda, yalnız kapıdan sonra; olay dosyası ile getiri dosyası ayrı; öbeğin son uzunluğu yalnız sayımda (bilgi); veri "
                   "<= 2022-12-31 assert"),
    "K3": ("EVET", "MI.mi_veri geçerli barları (H > L, V > 0, O/H/L/C sonlu > 0); ölü / fiyat adımına yapışmış bar doji sayılmaz (ADIM kuralı, test); öbekte "
                   "takvim satırı farkı > 6 bağlanmaz; 15 bar <= 30 takvim satırı; giriş P2 evreninde"),
    "K4": ("EVET", "öbek başına her k satırında bir olay (4+ = 4. doji; sonrakiler olay değil); olaylar örtüşebilir, çıkarım ay kümeli bootstrap; n ve farklı ay "
                   "ayrı yazılır; medyan R15 yazılır; taban her 5. bar"),
    "K5": ("EVET", "giriş = t + 1 barının açılışı; çıkış devamı çıkış barından sonraki açılıştan (e + 1); P15 de giriş satırından"),
    "K6": ("EVET", "OS / MI bölünme düzeltmeli açık kopya (YO ile aynı depo); getiriler oransal, yerel para; pazar içi karşılaştırma; eşikler ATR oranlı (birimden "
                   "bağımsız); fiyat adımı kuralı birimden bağımsız (kendi fiyat farklarından)"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma yanlılığı): sonuç yukarı yanlı; TOPLAM FARK aynı hisseye göre olduğu için yanlılık kısmen düşer; "
                   "raporda yazılır; kasa açılmaz"),
    "K8": ("EVET", "n >= 1.000 değilse ÖLÇÜLEMEDİ (n < 30 'örneklem yetersiz'); iki ABD dönemi + iki AVR dönemi; BH q 0,10 (32 satır aile); en kalabalık 3 ay payı "
                   "her satırda"),
    "K9": ("EVET", "DJ_ON_KAYIT.md: DJ_KOD_SHA, DJ_ESIK_SHA, olay / taban dosya sha'ları, SAYIM_SHA, yorum noktaları; ölçüm kapısı: kontrol + sha + ön kayıt commit "
                   "+ push + kod temiz; getiri dosyası varsa ikinci koşu DURUR; eşikler sonuca göre değişmez"),
    "K10": ("EVET", "doji / öbek kuralı sentetik pozitif / negatif serilerle (yakalama >= %95, yanlış kabul <= %5); uygunluk maskesi YO.yo_ornek_maske ile 5. barlarda "
                    "birebir; dokunma YO.yo_ilk_dokunma; kaynak npz sha YO ön kaydıyla aynı; PDF'te gerçek örnekler gözle denetlenir"),
    "K11": ("EVET", "rapordan önce >= 3 satır olay + getiri dosyalarından bağımsız kısa kodla yeniden üretilir; rapordaki sayılar dj_sonuc.json'dan basılır"),
    "K12": ("EVET", "'emare / etkili' sözü yalnız hüküm kuralıyla; ABD tek dönem 'TEK DÖNEM'; sayı ile yorum ayrı cümlede; evren bugün yaşayanlar; fiyat değişimi "
                    "gerçek kâr değil (komisyon / kayma yok)"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_dj); mevcut modüller ve defter dosyaları değişmez (yalnız import; SEKIL_DEVAM / WEB_DESEN içe alınmaz); yalnız "
                    "kendi yolları commit; sızıntı taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez, kasa açılmaz"),
}


# ================================================================ 0) YARDIMCI
def _dj_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or DJ_YOL["cikti"], DJ_DOSYA[ad])


def _dj_ham(ad: str, ham: Optional[str] = None) -> str:
    return os.path.join(ham or DJ_YOL["ham"], ad)


def dj_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or DJ_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def dj_kod_sha() -> str:
    return MI._mi_sha(DJ_YOL["kod"])


def _dj_rng(anahtar: str) -> np.random.Generator:
    return np.random.default_rng([int(DJ_ESIK["tohum"]), zlib.crc32(str(anahtar).encode("utf-8"))])


def dj_kesik_kapi(tarih: Any, ad: str = "veri") -> pd.Timestamp:
    """Kasa kapısı (mekanik): en büyük tarih > 2022-12-31 ise DUR."""
    t = pd.DatetimeIndex(tarih)
    if not len(t):
        raise DJHata(f"{ad}: tarih boş")
    en = pd.Timestamp(t.max())
    if en > DJ_KESIK:
        raise DJHata(f"KESİK AŞIMI: {ad} en geç {en.date()} > {DJ_KESIK.date()} (KASA açılmaz)")
    assert en <= DJ_KESIK
    return en


def dj_hucre(giris: Any, pazar: str) -> np.ndarray:
    """Vektör hücre adı (HV.hv_hucre_ad ile aynı dönemler; test birebir)."""
    g = pd.DatetimeIndex(giris); out = np.full(len(g), f"{pazar}|dis", dtype=object)
    for ad, (a, b) in HV.HV_ESIK["hucre"]["donem"].items():
        out[(g >= pd.Timestamp(a)) & (g <= pd.Timestamp(b))] = f"{pazar}|{ad}"
    return out


def dj_depo(pazar: str, kaynak: Optional[str] = None) -> Dict[str, np.ndarray]:
    yol = os.path.join(kaynak or DJ_YOL["kaynak"], f"ham_{pazar}.npz")
    if not os.path.exists(yol):
        raise DJHata(f"kaynak bar deposu yok: {yol} (YUKSELIS_ONCESI hazirla)")
    z = np.load(yol); D = {k: z[k] for k in z.files}
    for k in ("O", "H", "L", "C", "POS", "off", "Op", "Cl", "P2", "tarih", "sembol"):
        if k not in D:
            raise DJHata(f"K10: {yol} şeması eksik: {k}")
    dj_kesik_kapi(D["tarih"], f"bar deposu {pazar}")
    return D


# ================================================================ 1) DOJİ ve ÖBEK (yalnız t'ye kadarki barlar)
def dj_adim(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, w: Optional[int] = None) -> np.ndarray:
    """ADIM(t): t - w + 1 .. t barlarının O/H/L/C değerlerinin sıralı farklarının en küçük pozitifi (> 1e-9 x C_t); w bar yoksa NaN."""
    w = int(w or DJ_ESIK["doji"]["adim_pencere"]); m = len(C); out = np.full(m, np.nan)
    if m < w:
        return out
    V = np.stack([O, H, L, C], 1).astype(float)
    Wv = np.lib.stride_tricks.sliding_window_view(V, (w, 4))[:, 0].reshape(m - w + 1, 4 * w)
    S = np.sort(Wv, axis=1); d = np.diff(S, axis=1); eps = 1e-9 * C[w - 1:][:, None]
    d = np.where(d > eps, d, np.inf); mn = d.min(1)
    out[w - 1:] = np.where(np.isfinite(mn), mn, np.nan)
    return out


def dj_doji(O: Any, H: Any, L: Any, C: Any, govde: Optional[float] = None) -> Dict[str, np.ndarray]:
    """Doji bayrağı ve nedenleri (t barında yalnız t ve öncesi)."""
    E = DJ_ESIK["doji"]; govde = float(E["govde"] if govde is None else govde)
    O, H, L, C = (np.asarray(a, float) for a in (O, H, L, C)); m = len(C)
    boy = H - L
    ort = pd.Series(boy).rolling(int(E["ort_boy_bar"]), min_periods=int(E["ort_boy_bar"])).median().shift(1).to_numpy(float)
    with np.errstate(invalid="ignore"):
        g_ok = np.abs(C - O) <= govde * boy
        b_ok = (boy > 0) & np.isfinite(ort) & (boy >= float(E["boy_oran"]) * ort)
        adim = dj_adim(O, H, L, C)
        yapis = np.isfinite(adim) & (boy <= float(E["adim_kat"]) * adim)
    return {"doji": g_ok & b_ok & ~yapis, "govde_ok": g_ok, "boy_ok": b_ok, "yapis": yapis, "ort_boy": ort, "adim": adim, "m": np.int64(m)}


def dj_obek(doji: np.ndarray, O: Any, H: Any, L: Any, C: Any, atr: Any, pos: Optional[np.ndarray] = None) -> pd.DataFrame:
    """Dojileri sırayla öbeklere bağlar. Döner: her doji bir satır (t, k, obek, ilk, son_ara, bant_H, bant_L, sev_gen_atr, red). red = yeni öbek başlatan
    dojinin önceki dojiye neden bağlanmadığı (ILK / ARA_UZAK / SEVIYE_FARKLI / TAKVIM / ATR_YOK). Karar her dojide yalnız o ana kadarki dojilerle."""
    Eo = DJ_ESIK["obek"]; ara = int(Eo["ara_en_cok"]); tara = int(Eo["takvim_ara_en_cok"]); ba = float(Eo["bant_atr"])
    O, H, L, C, atr = (np.asarray(a, float) for a in (O, H, L, C, atr)); pos = np.arange(len(C)) if pos is None else np.asarray(pos)
    ix = np.flatnonzero(np.asarray(doji, bool)); sev = (O + C) / 2.0
    rows = []; ob = -1; k = 0; son = -10 ** 9; smin = smax = np.nan; bh = bl = np.nan; ilk = -1
    for t in ix:
        lv = sev[t]; a = atr[t]; red = ""
        if ob >= 0:
            g = t - son
            yeni_min = min(smin, lv); yeni_max = max(smax, lv)
            if g > ara:
                red = "ARA_UZAK"
            elif pos[t] - pos[son] > tara:
                red = "TAKVIM"
            elif not (np.isfinite(a) and a > 0):
                red = "ATR_YOK"
            elif yeni_max - yeni_min > ba * a * (1 + 1e-12):
                red = "SEVIYE_FARKLI"
        else:
            red = "ILK"
        if red:
            prev_son = son; ob += 1; k = 1; ilk = t; smin = smax = lv; bh = H[t]; bl = L[t]
            # bilgi: önceki dojiyle seviye farkı / ATR (red nedeni gösterimi için)
            onc_ara = int(t - prev_son) if prev_son > -10 ** 8 else -1
            onc_sev = float(abs(lv - sev[prev_son]) / a) if (prev_son > -10 ** 8 and np.isfinite(a) and a > 0) else np.nan
        else:
            k += 1; smin = min(smin, lv); smax = max(smax, lv); bh = max(bh, H[t]); bl = min(bl, L[t])
            onc_ara = int(t - son); onc_sev = float(abs(lv - sev[son]) / a)
        gen = float((smax - smin) / a) if (np.isfinite(a) and a > 0) else np.nan
        rows.append((int(t), int(k), int(ob), int(ilk), onc_ara, onc_sev, float(bh), float(bl), gen, red if k == 1 else ""))
        son = t
    D = pd.DataFrame(rows, columns=["t", "k", "obek", "ilk", "onc_ara", "onc_sev_atr", "bant_H", "bant_L", "sev_gen_atr", "red"])
    if len(D):
        D["obek_boy"] = D.groupby("obek").k.transform("max").astype(int)   # BİLGİ (öbeğin son uzunluğu; ölçüde kullanılmaz)
    else:
        D["obek_boy"] = pd.Series(dtype=int)
    return D


def dj_uygun(m: int, pos: np.ndarray, p2: np.ndarray, tarih: pd.DatetimeIndex, k: np.ndarray) -> np.ndarray:
    """YO.yo_ornek_maske kuralları rastgele k'ler için (adım 5 yerine verilen k'ler). Döner bool (k ile aynı boy)."""
    E = YO.YO_ESIK["ornek"]; U = int(YO.YO_ESIK["yukselis"]["ufuk"]); k = np.asarray(k, np.int64); ok = np.zeros(len(k), bool)
    v = (k >= 0) & (k + U < m)
    if not v.any():
        return ok
    kk = k[v]
    o = (pos[kk + 1] - pos[kk] <= int(E["giris_bosluk"])) & (pos[kk + U] - pos[kk + 1] <= int(E["pencere_satir"]) - 1) & p2[pos[kk + 1]]
    gt = tarih[pos[kk + 1]]
    o &= np.asarray((gt >= pd.Timestamp("2016-01-01")) & (gt <= pd.Timestamp("2022-12-31")) & (tarih[pos[kk + U]] <= YO.YO_KESIK))
    ok[np.flatnonzero(v)] = o
    return ok


def _dj_ozellik(O, H, L, C) -> Dict[str, np.ndarray]:
    F = YO.yo_hisse_ozellik(O, H, L, C, np.ones(len(C)))
    with np.errstate(invalid="ignore", divide="ignore"):
        onc = np.full(len(C), np.nan); b = int(DJ_ESIK["baglam"]["onceki_bar"])
        if len(C) > b:
            onc[b:] = C[b:] / C[:-b] - 1
    return {"ATRP20": F["ATRP20"], "KONUM120": F["KONUM120"], "ONCEKI10": onc}


def dj_tara_hisse(O, H, L, C, pos, p2, tarih, govde: Optional[float] = None, F: Optional[Dict[str, np.ndarray]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Bir hisse: dojiler -> öbekler -> olay satırları (uygunluk + ATRP sonlu). Getirisiz. Döner (olaylar, sayaç)."""
    O, H, L, C = (np.asarray(a, float) for a in (O, H, L, C)); m = len(C)
    F = F or _dj_ozellik(O, H, L, C)
    Dj = dj_doji(O, H, L, C, govde)
    atr = F["ATRP20"] * C
    B = dj_obek(Dj["doji"], O, H, L, C, atr, pos)
    say = {"bar": int(m), "aday_govde": int((Dj["govde_ok"]).sum()), "boy_dustu": int((Dj["govde_ok"] & ~Dj["boy_ok"]).sum()),
           "yapis_dustu": int((Dj["govde_ok"] & Dj["boy_ok"] & Dj["yapis"]).sum()), "doji": int(Dj["doji"].sum())}
    if not len(B):
        return B.assign(ATRP20=[], KONUM120=[], ONCEKI10=[]), say
    B = B[B.k <= 4].reset_index(drop=True)
    t = B.t.to_numpy(np.int64)
    ok = dj_uygun(m, pos, p2, tarih, t) & np.isfinite(F["ATRP20"][t]) & (F["ATRP20"][t] > 0)
    B = B[ok].reset_index(drop=True); t = B.t.to_numpy(np.int64)
    for c in ("ATRP20", "KONUM120", "ONCEKI10"):
        B[c] = F[c][t]
    return B, say


def dj_uygun_bar_say(m: int, pos: np.ndarray, p2: np.ndarray, tarih: pd.DatetimeIndex, atrp: np.ndarray) -> np.ndarray:
    """Uygun hisse-gün barları (sıklık paydası): her bar için dj_uygun + ATRP sonlu > 0."""
    k = np.arange(m, dtype=np.int64)
    return dj_uygun(m, pos, p2, tarih, k) & np.isfinite(atrp) & (atrp > 0)


# ================================================================ 2) HAZIRLIK (getirisiz)
def _dj_kol_govde(kol: str) -> float:
    return float(DJ_ESIK["doji"]["govde_D15"] if kol == "D15" else DJ_ESIK["doji"]["govde"])


def dj_hazirla_pazar(pazar: str, ham: Optional[str] = None, kaynak: Optional[str] = None, D: Optional[Dict[str, np.ndarray]] = None) -> Dict[str, Any]:
    """Olay dosyaları (ANA, D15), haftalık olaylar (HAFTA), taban (her 5. bar) ve uygun bar sayıları. Getiri hesaplanmaz."""
    t0 = time.time(); ham = ham or DJ_YOL["ham"]; os.makedirs(ham, exist_ok=True)
    D = D if D is not None else dj_depo(pazar, kaynak)
    tarih = pd.DatetimeIndex(D["tarih"]); S = np.asarray(D["sembol"]).astype(str); off = D["off"]; P2 = D["P2"]
    ev = {"ANA": [], "D15": []}; tb = []; uyg = []; say = {"ANA": {}, "D15": {}}
    for j, s in enumerate(S):
        a, b = int(off[j]), int(off[j + 1]); m = b - a
        if m < 30:
            continue
        O, H, L, C = (D[c][a:b].astype(float) for c in ("O", "H", "L", "C")); pos = D["POS"][a:b].astype(np.int64); p2 = P2[:, j]
        F = _dj_ozellik(O, H, L, C)
        for kol in ("ANA", "D15"):
            B, sy = dj_tara_hisse(O, H, L, C, pos, p2, tarih, _dj_kol_govde(kol), F)
            for kk, v in sy.items():
                say[kol][kk] = say[kol].get(kk, 0) + v
            if len(B):
                B.insert(0, "j", j); ev[kol].append(B)
        # uygun barlar (payda) ve taban günleri
        u = dj_uygun_bar_say(m, pos, p2, tarih, F["ATRP20"])
        if u.any():
            uyg.append(pd.DataFrame({"j": j, "d_row": pos[np.flatnonzero(u) + 1]}))
        kk = YO.yo_ornek_maske(m, pos, p2, tarih)
        if len(kk):
            kk = kk[np.isfinite(F["ATRP20"][kk]) & (F["ATRP20"][kk] > 0)]
            Dj = dj_doji(O, H, L, C)
            tb.append(pd.DataFrame({"j": j, "t": kk, "ATRP20": F["ATRP20"][kk], "KONUM120": F["KONUM120"][kk], "ONCEKI10": F["ONCEKI10"][kk],
                                    "doji": Dj["doji"][kk]}))
    out: Dict[str, Any] = {"pazar": pazar, "sayac": say}
    POS = D["POS"]
    for kol in ("ANA", "D15"):
        X = pd.concat(ev[kol], ignore_index=True)
        X["t_row"] = POS[off[X.j.to_numpy()] + X.t.to_numpy()]; X["d_row"] = POS[off[X.j.to_numpy()] + X.t.to_numpy() + 1]
        X["tarih"] = tarih[X.t_row.to_numpy()]; X["giris"] = tarih[X.d_row.to_numpy()]
        X["hucre"] = dj_hucre(X.giris, pazar); X["ay"] = X.giris.dt.strftime("%Y-%m"); X["pazar"] = pazar; X["sembol"] = S[X.j.to_numpy()]
        X = X.sort_values(["giris", "sembol", "k"], kind="stable").reset_index(drop=True)
        dj_kesik_kapi(X.giris, f"olay {pazar} {kol}")
        X.to_pickle(_dj_ham(f"olay_{kol}_{pazar}.pkl", ham), protocol=4); out[kol] = int(len(X))
    T = pd.concat(tb, ignore_index=True)
    T["d_row"] = POS[off[T.j.to_numpy()] + T.t.to_numpy() + 1]; T["giris"] = tarih[T.d_row.to_numpy()]
    T["hucre"] = dj_hucre(T.giris, pazar); T["ay"] = T.giris.dt.strftime("%Y-%m"); T["sembol"] = S[T.j.to_numpy()]
    T.to_pickle(_dj_ham(f"taban_{pazar}.pkl", ham), protocol=4); out["taban"] = int(len(T))
    Ug = pd.concat(uyg, ignore_index=True); Ug["hucre"] = dj_hucre(tarih[Ug.d_row.to_numpy()], pazar)
    Us = {"hisse_gun": {h: int(n) for h, n in Ug.hucre.value_counts().items()}}
    with open(_dj_ham(f"uygun_{pazar}.json", ham), "w", encoding="utf-8") as f:
        json.dump(Us, f, ensure_ascii=False, indent=1)
    W = dj_hafta_olay(pazar, D)
    W.to_pickle(_dj_ham(f"olay_HAFTA_{pazar}.pkl", ham), protocol=4); out["HAFTA"] = int((W.tip == "olay").sum())
    djlog.info("%s: ANA %d, D15 %d, HAFTA %d olay, taban %d (%.0f sn)", pazar, out["ANA"], out["D15"], out["HAFTA"], out["taban"], time.time() - t0)
    gc.collect()
    return out


def dj_hafta_bar(O, H, L, C, tarih_bar: pd.DatetimeIndex, pos: np.ndarray) -> pd.DataFrame:
    """Günlük geçerli barlardan W-FRI haftalık mumlar (O ilk, H maks, L min, C son); 'ilk_row' haftanın ilk günlük satırı."""
    hf = tarih_bar.to_period("W-FRI")
    df = pd.DataFrame({"O": O, "H": H, "L": L, "C": C, "row": pos, "hf": hf})
    g = df.groupby("hf", sort=True)
    W = pd.DataFrame({"O": g.O.first(), "H": g.H.max(), "L": g.L.min(), "C": g.C.last(), "ilk_row": g.row.first(), "son_row": g.row.last()})
    W["hno"] = np.array([p.ordinal for p in W.index], np.int64)
    W["bitis"] = W.index.end_time.normalize()
    return W.reset_index(drop=True)


def dj_hafta_olay(pazar: str, D: Dict[str, np.ndarray]) -> pd.DataFrame:
    """HAFTA kolu (bilgi): olaylar ve taban haftaları (tip = 'olay' / 'taban'), sonuç girdileri (E0 / C15 / ATRP) AYRI: yalnız t, giriş haftası tutulur."""
    tarih = pd.DatetimeIndex(D["tarih"]); S = np.asarray(D["sembol"]).astype(str); off = D["off"]; P2 = D["P2"]; U = int(DJ_ESIK["sonuc"]["ufuk"])
    parca = []
    for j, s in enumerate(S):
        a, b = int(off[j]), int(off[j + 1])
        if b - a < 200:
            continue
        pos = D["POS"][a:b].astype(np.int64)
        W = dj_hafta_bar(D["O"][a:b], D["H"][a:b], D["L"][a:b], D["C"][a:b], tarih[pos], pos)
        m = len(W)
        if m < U + 25:
            continue
        O, H, L, C = (W[c].to_numpy(float) for c in ("O", "H", "L", "C"))
        F = _dj_ozellik(O, H, L, C); hno = W.hno.to_numpy()
        Dj = dj_doji(O, H, L, C)
        B = dj_obek(Dj["doji"], O, H, L, C, F["ATRP20"] * C, hno)
        k = np.arange(m - U - 1)
        ok = (hno[k + U] - hno[k + 1] <= 29) & (hno[k + 1] - hno[k] <= 2) & P2[W.ilk_row.to_numpy()[k + 1], j]
        g0 = tarih[W.ilk_row.to_numpy()[k + 1]]
        ok &= np.asarray((g0 >= pd.Timestamp("2016-01-01")) & (g0 <= pd.Timestamp("2022-12-31"))) & (pd.DatetimeIndex(W.bitis.to_numpy()[k + U]) <= DJ_KESIK)
        ok &= np.isfinite(F["ATRP20"][k]) & (F["ATRP20"][k] > 0)
        uy = np.zeros(m, bool); uy[k[ok]] = True
        if len(B):
            B = B[(B.k <= 4) & uy[B.t.to_numpy()]]
            if len(B):
                parca.append(pd.DataFrame({"j": j, "t": B.t.to_numpy(), "k": B.k.to_numpy(), "tip": "olay",
                                           "giris": tarih[W.ilk_row.to_numpy()[B.t.to_numpy() + 1]]}))
        tt = np.flatnonzero(uy)
        if len(tt):
            parca.append(pd.DataFrame({"j": j, "t": tt, "k": 0, "tip": "taban", "giris": tarih[W.ilk_row.to_numpy()[tt + 1]]}))
    X = pd.concat(parca, ignore_index=True)
    X["hucre"] = dj_hucre(X.giris, pazar); X["ay"] = pd.DatetimeIndex(X.giris).strftime("%Y-%m"); X["sembol"] = S[X.j.to_numpy()]
    return X


def dj_hazirla(ham: Optional[str] = None, kaynak: Optional[str] = None) -> Dict[str, Any]:
    return {p: dj_hazirla_pazar(p, ham, kaynak) for p in DJ_PAZAR}


def dj_yukle(pazar: str, kol: str = "ANA", ham: Optional[str] = None) -> pd.DataFrame:
    return pd.read_pickle(_dj_ham(f"olay_{kol}_{pazar}.pkl", ham))


def dj_dosya_sha(ham: Optional[str] = None, kaynak: Optional[str] = None) -> Dict[str, str]:
    out = {}
    for p in DJ_PAZAR:
        for ad in (f"olay_ANA_{p}.pkl", f"olay_D15_{p}.pkl", f"olay_HAFTA_{p}.pkl", f"taban_{p}.pkl", f"uygun_{p}.json"):
            out[ad] = MI._mi_sha(_dj_ham(ad, ham))
        out[f"KAYNAK_ham_{p}.npz"] = MI._mi_sha(os.path.join(kaynak or DJ_YOL["kaynak"], f"ham_{p}.npz"))
    return out


# ================================================================ 3) GETİRİSİZ SAYIM
def dj_sayim(ham: Optional[str] = None) -> Dict[str, Any]:
    """Hücre x k: olay sayısı, bin uygun hisse-günde sıklık, farklı ay, hisse; öbek son uzunluğu dağılımı; red nedenleri; D15 / HAFTA sayıları. R15 yok."""
    S: Dict[str, Any] = {"ANA": {}, "D15": {}, "HAFTA": {}, "obek_boy": {}, "red": {}, "uygun": {}, "taban_doji_pay": {}}
    for p in DJ_PAZAR:
        U = json.load(open(_dj_ham(f"uygun_{p}.json", ham), encoding="utf-8"))["hisse_gun"]
        T = pd.read_pickle(_dj_ham(f"taban_{p}.pkl", ham))
        for h in [x for x in DJ_HUCRE if x.startswith(p)]:
            S["uygun"][h] = int(U.get(h, 0))
            tg = T[T.hucre == h]; S["taban_doji_pay"][h] = {"n": int(len(tg)), "doji_pay": float(tg.doji.mean()) if len(tg) else None}
        for kol in ("ANA", "D15"):
            X = dj_yukle(p, kol, ham)
            for h, g in X.groupby("hucre"):
                if h not in DJ_HUCRE:
                    continue
                d = {}
                for k in DJ_KSIN:
                    gk = g[g.k == k]; ao = HV.hv25_ay_ozet(gk.giris.dt.strftime("%Y-%m-%d").tolist())
                    d[str(k)] = {"n": int(len(gk)), "bin_hisse_gun": float(1000 * len(gk) / max(S["uygun"][h], 1)), "ay": ao["ay"], "ust3_pay": ao["ust3_pay"],
                                 "hisse": int(gk.sembol.nunique())}
                S[kol][h] = d
                if kol == "ANA":
                    g1 = g[g.k == 1]
                    vb = g1.obek_boy.clip(upper=6).value_counts().sort_index()
                    S["obek_boy"][h] = {("6+" if int(i) == 6 else str(int(i))): int(c) for i, c in vb.items()}
                    S["red"][h] = {str(r): int(c) for r, c in g1.red.value_counts().items()}
        W = pd.read_pickle(_dj_ham(f"olay_HAFTA_{p}.pkl", ham))
        for h, g in W.groupby("hucre"):
            if h not in DJ_HUCRE:
                continue
            nt = int((g.tip == "taban").sum())
            S["HAFTA"][h] = {"taban_hafta": nt, **{str(k): {"n": int(((g.tip == "olay") & (g.k == k)).sum()),
                                                              "bin_hisse_hafta": float(1000 * ((g.tip == "olay") & (g.k == k)).sum() / max(nt, 1))} for k in DJ_KSIN}}
    return S


# ================================================================ 4) SONUÇ ÇEKİRDEĞİ (yalnız dj_olcum kapısından sonra)
def dj_getiri_dizi(dep: Dict[str, np.ndarray], j: Any, t: Any, atrp: Any, bH: Any = None, bL: Any = None) -> Dict[str, np.ndarray]:
    """Olay / taban satırları (hisse j, kendi bar t): E0, R15, U2, D2, BUYUKLUK, R10B (t+1 açılış -> t+10 kapanış); bant verilirse CIKIS (+1 / -1 / 0),
    CIKIS_BAR (t'den uzaklık), DEVAM (çıkış yönünde R10). Uygunluk çağıranda (t + 15 verinin içinde; aksi DUR)."""
    E = DJ_ESIK["sonuc"]; U = int(E["ufuk"]); dv = int(E["devam"])
    j = np.asarray(j, np.int64); t = np.asarray(t, np.int64); atrp = np.asarray(atrp, float); N = len(j)
    ad = ["E0", "R15", "U2", "D2", "BUYUKLUK", "R10B", "CIKIS", "CIKIS_BAR", "DEVAM"]
    out = {a: np.full(N, np.nan) for a in ad}
    if not N:
        return out
    off = dep["off"]; g = off[j] + t; son = off[j + 1] - 1
    if (g + U > son).any():
        raise DJHata("K10: sonuç penceresi hissenin verisini aşıyor (uygunluk bozuk)")
    W = g[:, None] + 1 + np.arange(U)[None, :]
    E0 = dep["O"][g + 1]; Hs = dep["H"][W]; Ls = dep["L"][W]; Cs = dep["C"][W]
    out["E0"] = E0; out["R15"] = dep["C"][g + U] / E0 - 1; out["R10B"] = dep["C"][g + dv] / E0 - 1
    a = atrp[:, None]
    out["U2"] = YO.yo_ilk_dokunma(E0, Hs, Ls, float(E["hedef_atr"]) * a, float(E["stop_atr"]) * a, "yukari")
    out["D2"] = YO.yo_ilk_dokunma(E0, Hs, Ls, float(E["hedef_atr"]) * a, float(E["stop_atr"]) * a, "asagi")
    out["BUYUKLUK"] = np.abs(out["R15"]) / (atrp * np.sqrt(U))
    if bH is not None:
        bH = np.asarray(bH, float)[:, None]; bL = np.asarray(bL, float)[:, None]; BIG = 10 ** 9
        up = Cs > bH; dn = Cs < bL
        ku = np.where(up.any(1), up.argmax(1), BIG); kd = np.where(dn.any(1), dn.argmax(1), BIG)
        yon = np.where(ku < kd, 1.0, np.where(kd < ku, -1.0, 0.0)); kb = np.minimum(ku, kd)
        out["CIKIS"] = yon; out["CIKIS_BAR"] = np.where(yon != 0, kb + 1, np.nan)
        e = np.where(yon != 0, g + 1 + np.minimum(kb, U - 1), g)
        okd = (yon != 0) & (e + dv <= son)
        if okd.any():
            ee = e[okd]; span = dep["POS"][ee + dv] - dep["POS"][ee + 1]
            r10 = dep["C"][ee + dv] / dep["O"][ee + 1] - 1
            r10[span > int(E["devam_satir"])] = np.nan
            dvm = np.full(N, np.nan); dvm[okd] = r10 * yon[okd]; out["DEVAM"] = dvm
    return out


def dj_hafta_getiri(D: Dict[str, np.ndarray], X: pd.DataFrame) -> pd.DataFrame:
    """HAFTA kolu sonuçları (R15 haftalık) — yalnız kapıdan sonra."""
    tarih = pd.DatetimeIndex(D["tarih"]); off = D["off"]; U = int(DJ_ESIK["sonuc"]["ufuk"]); R = np.full(len(X), np.nan)
    for j, ii in X.groupby("j").indices.items():
        a, b = int(off[j]), int(off[j + 1]); pos = D["POS"][a:b].astype(np.int64)
        W = dj_hafta_bar(D["O"][a:b], D["H"][a:b], D["L"][a:b], D["C"][a:b], tarih[pos], pos)
        t = X.t.to_numpy()[ii]
        R[ii] = W.C.to_numpy()[t + U] / W.O.to_numpy()[t + 1] - 1
    return pd.DataFrame({"R15": R}, index=X.index)


# ================================================================ 5) İSTATİSTİK
def dj_ay_W(ay: np.ndarray, anahtar: str, B: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    B = int(B or DJ_ESIK["boot"]["B"]); u, k = np.unique(np.asarray(ay, str), return_inverse=True); K = len(u)
    W = _dj_rng(anahtar).multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)
    return u, k, W


def _dj_p(v: np.ndarray) -> Optional[float]:
    v = v[np.isfinite(v)]
    if not len(v):
        return None
    a = (v <= 0).sum(); b = (v >= 0).sum()
    return float(min(1.0, 2 * (1 + min(a, b)) / (len(v) + 1)))


def dj_boot(x: np.ndarray, ay: np.ndarray, anahtar: str, B: Optional[int] = None, pay: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """Ay kümeli bootstrap ortalama (pay verilirse oran = sum(x) / sum(pay))."""
    x = np.asarray(x, float); f = np.isfinite(x)
    if pay is not None:
        pay = np.asarray(pay, float); f &= np.isfinite(pay)
    x = x[f]; ay = np.asarray(ay, str)[f]; n = int(len(x))
    o: Dict[str, Any] = {"n": n, "ort": None, "alt": None, "ust": None, "p": None}
    if n < 2:
        if n:
            o["ort"] = float(x.mean()) if pay is None else float(x.sum() / pay[f].sum())
        return o
    _, k, W = dj_ay_W(ay, anahtar, B); K = W.shape[1]
    s = np.bincount(k, weights=x, minlength=K)
    d_ = np.bincount(k, minlength=K).astype(float) if pay is None else np.bincount(k, weights=pay[f], minlength=K)
    with np.errstate(invalid="ignore", divide="ignore"):
        v = (W @ s) / (W @ d_)
    a, b = YO._q(v)
    o["ort"] = float(x.mean()) if pay is None else float(x.sum() / pay[f].sum()); o["alt"] = a; o["ust"] = b
    o["p"] = _dj_p(v if pay is None else v - 1.0)
    return o


def dj_boot_fark(x1: np.ndarray, ay1: np.ndarray, x0: np.ndarray, ay0: np.ndarray, anahtar: str, B: Optional[int] = None) -> Dict[str, Any]:
    """ort(x1) - ort(x0); iki grup aynı ay ağırlıklarıyla (ortak ay kümeleri)."""
    x1 = np.asarray(x1, float); x0 = np.asarray(x0, float); f1 = np.isfinite(x1); f0 = np.isfinite(x0)
    x1, ay1, x0, ay0 = x1[f1], np.asarray(ay1, str)[f1], x0[f0], np.asarray(ay0, str)[f0]
    o: Dict[str, Any] = {"n1": int(len(x1)), "n0": int(len(x0)), "fark": None, "alt": None, "ust": None, "p": None}
    if len(x1) < 2 or len(x0) < 2:
        return o
    u, k, W = dj_ay_W(np.r_[ay1, ay0], anahtar, B); K = len(u); k1 = k[:len(x1)]; k0 = k[len(x1):]
    s1 = np.bincount(k1, weights=x1, minlength=K); n1 = np.bincount(k1, minlength=K).astype(float)
    s0 = np.bincount(k0, weights=x0, minlength=K); n0 = np.bincount(k0, minlength=K).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        v = (W @ s1) / (W @ n1) - (W @ s0) / (W @ n0)
    a, b = YO._q(v)
    o.update({"fark": float(x1.mean() - x0.mean()), "alt": a, "ust": b, "p": _dj_p(v)})
    return o


def dj_etiket(o: Dict[str, Dict[str, Any]], ad: str = "ort", bh_gecti: Optional[bool] = None, avr: bool = True) -> str:
    """Önceden yazılı hüküm sırası (DJ_ESIK['hukum']['sira']). o: hücre -> {n, ort, alt, ust}."""
    H = DJ_ESIK["hukum"]; nmin = int(H["n_min"]); A = [o.get(h) or {} for h in DJ_ABD]

    def art(r):
        return r.get("alt") is not None and r["alt"] > 0 and (r.get(ad) or 0) > 0

    def eks(r):
        return r.get("ust") is not None and r["ust"] < 0

    def avr_isaret(sgn):
        if not avr:
            return True
        v = [(o.get(h) or {}).get(ad) for h in DJ_AVR]
        return all(x is not None and np.sign(x) == sgn for x in v)
    yon = None
    if all(art(r) for r in A):
        yon = 1
    elif all(eks(r) for r in A):
        yon = -1
    if yon is not None:
        if not avr_isaret(yon):
            return "ABD İKİ DÖNEM, AVR UYMADI"
        if bh_gecti is False:
            return "BH GEÇMEDİ"
        return "ARTI" if yon > 0 else "EKSİ"
    ay = [1 if art(r) else (-1 if eks(r) else 0) for r in A]
    if 1 in ay and -1 in ay:
        return "ÇELİŞKİLİ"
    if any(ay):
        return "TEK DÖNEM"
    if all((r.get("n") or 0) >= nmin for r in A):
        return "AYRIŞMIYOR"
    return "ÖLÇÜLEMEDİ"


def dj_doz(seri: Dict[str, Dict[int, Optional[float]]], fark: Dict[str, Dict[int, Dict[str, Any]]]) -> Dict[str, Any]:
    """DOZ kuralı (bir ölçü): seri[hücre][k] nokta; fark[hücre][k] = (k - 1) bootstrap (k = 3, 4)."""
    yon = []
    for h in DJ_ABD:
        v = [seri.get(h, {}).get(k) for k in DJ_KSIN]
        if any(x is None for x in v):
            yon.append(0); continue
        d = np.diff(np.asarray(v, float))
        yon.append(1 if (d > 0).all() else (-1 if (d < 0).all() else 0))
    tek = yon[0] != 0 and yon[0] == yon[1]
    ayr = False
    if tek:
        for k in (3, 4):
            ok = True
            for h in DJ_ABD:
                r = fark.get(h, {}).get(k) or {}
                if yon[0] > 0:
                    ok &= r.get("alt") is not None and r["alt"] > 0
                else:
                    ok &= r.get("ust") is not None and r["ust"] < 0
            ayr |= ok
    return {"yon": yon, "tek_yonlu": bool(tek), "fark_ayrisiyor": bool(ayr), "etkili": bool(tek and ayr)}


# ================================================================ 6) KAPI + ÖLÇÜM (bir kez)
def dj_kapi(cikti: Optional[str] = None, ham: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    """Ölçüm kapısı: ön kayıt var + IZ_KARNE kontrol kapısı + mühürler (kod / eşik / dosya sha) + ön kayıt ve kod commit + push edilmiş ve temiz + getiri
    dosyası YOK (ikinci koşu durur)."""
    import IZ_KARNE as IK
    yol = _dj_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise DJHata(f"SIRA: ön kayıt yok: {yol}")
    try:
        kk = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise DJHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read()

    def muhur(ad):
        for sat in metin.splitlines():
            if sat.startswith(ad + ":"):
                return sat.split(":", 1)[1].strip()
        raise DJHata(f"K9: ön kayıtta mühür yok: {ad}")
    if muhur("DJ_KOD_SHA") != dj_kod_sha():
        raise DJHata("K9: kod ön kayıttan sonra değişti (DJ_KOD_SHA)")
    if muhur("DJ_ESIK_SHA") != dj_esik_sha():
        raise DJHata("K9: eşik sözlüğü değişti (DJ_ESIK_SHA)")
    for ad, sh in dj_dosya_sha(ham).items():
        if muhur(f"DOSYA_{ad}") != sh:
            raise DJHata(f"K9: olay / taban dosyası değişti: {ad}")
    if os.path.exists(_dj_ham("getiri_ANA_ABD.pkl", ham)):
        raise DJHata("SIRA: getiri dosyası zaten var: ikinci ölçüm koşusu yasak")
    out = {"kontrol": kk["gecti"], "onkayit": yol}
    if git:
        rel = os.path.relpath(yol, KOK_DJ); relk = os.path.relpath(DJ_YOL["kod"], KOK_DJ)
        c = MI._mi_git(["log", "-1", "--format=%H|%cI", "--", rel])
        if not c:
            raise DJHata("K9: ön kayıt commit edilmemiş")
        if MI._mi_git(["status", "--porcelain", "--", rel, relk]):
            raise DJHata("K9: ön kayıt ya da kod commit'ten sonra değişmiş (temiz değil)")
        uz = MI._mi_git(["branch", "-r", "--contains", c.split("|")[0]])
        if not uz:
            raise DJHata("K9: ön kayıt commit'i push edilmemiş")
        out["onkayit_commit"] = c
    return out


def _dj_taban_hisse(Tg: pd.DataFrame) -> pd.DataFrame:
    """Hisse x hücre taban ortalamaları (T1, p_h, q_h, h_h, T10)."""
    return Tg.groupby(["j", "hucre"]).agg(T1=("R15", "mean"), p_h=("U2", "mean"), q_h=("D2", "mean"), h_h=("BUYUKLUK", "mean"), T10=("R10B", "mean"))


def dj_olc_kol(X: pd.DataFrame, T: pd.DataFrame, B: Optional[int] = None, tam: bool = True) -> Dict[str, Any]:
    """Bir pazarın olay (getirili) ve taban (getirili) satırlarından hücre x k ölçüleri."""
    th = _dj_taban_hisse(T)
    X = X.join(th, on=["j", "hucre"])
    dus = int(X.T1.isna().sum()); X = X[X.T1.notna()].copy()
    X["TF"] = X.R15 - X.T1; X["SEC"] = X.R15 - X.P15
    X["ASM"] = (X.U2 - X.D2) - (X.p_h - X.q_h); X["BUYF"] = X.BUYUKLUK - X.h_h
    X["YUK"] = (X.CIKIS == 1).astype(float); X["ASA"] = (X.CIKIS == -1).astype(float); X["HIC"] = (X.CIKIS == 0).astype(float)
    X["DEVAM_SUR"] = X.DEVAM - np.where(X.CIKIS == 1, X.T10, np.where(X.CIKIS == -1, -X.T10, np.nan))
    # önceki yön: dönüş
    for ad, sgn in (("DUS", -1), ("YUKS", 1)):
        T_ = T[np.sign(T.ONCEKI10) == sgn]
        tp = (np.sign(T_.R15) == -sgn).astype(float).groupby(T_.hucre).mean()
        m = np.sign(X.ONCEKI10) == sgn
        X[f"DON_{ad}"] = np.where(m, (np.sign(X.R15) == -sgn).astype(float), np.nan)
        X[f"DONF_{ad}"] = X[f"DON_{ad}"] - X.hucre.map(tp).astype(float)
        X.attrs[f"don_taban_{ad}"] = {h: float(v) for h, v in tp.items()}
    out: Dict[str, Any] = {"dusen_tabansiz": dus, "hucre": {}, "fark": {}}
    pz = set(str(h).split("|")[0] for h in X.hucre.unique()) | set(str(h).split("|")[0] for h in T.hucre.unique())
    if len(pz) != 1:
        raise DJHata(f"K10: tek pazar bekleniyordu: {sorted(pz)}")
    hucreler = [h for h in DJ_HUCRE if h.split("|")[0] in pz]          # öteki pazarın boş hücreleri birleştirmede ezmesin
    for h in hucreler:
        g = X[X.hucre == h]; Hh: Dict[str, Any] = {}
        for k in DJ_KSIN:
            gk = g[g.k == k]; ay = gk.ay.to_numpy(str); an = f"{h}|{k}"
            ao = HV.hv25_ay_ozet([f"{a}-01" for a in ay]) if len(gk) else {"ay": 0, "ust3_pay": None}
            r: Dict[str, Any] = {"n": int(len(gk)), "ay": ao["ay"], "ust3_pay": ao["ust3_pay"],
                                 "R15_ort": float(gk.R15.mean()) if len(gk) else None, "R15_med": float(gk.R15.median()) if len(gk) else None,
                                 "TOPLAM_FARK": dj_boot(gk.TF.to_numpy(), ay, an + "|TF", B)}
            if tam:
                r["SECIM"] = dj_boot(gk.SEC.to_numpy(), ay, an + "|SEC", B)
                r["U2"] = float(gk.U2.mean()) if len(gk) else None; r["p_h"] = float(gk.p_h.mean()) if len(gk) else None
                r["D2"] = float(gk.D2.mean()) if len(gk) else None; r["q_h"] = float(gk.q_h.mean()) if len(gk) else None
                r["ASIMETRI"] = dj_boot(gk.ASM.to_numpy(), ay, an + "|ASM", B)
                r["BUYUKLUK"] = float(gk.BUYUKLUK.mean()) if len(gk) else None; r["h_h"] = float(gk.h_h.mean()) if len(gk) else None
                r["BUYUKLUK_FARK"] = dj_boot(gk.BUYF.to_numpy(), ay, an + "|BUYF", B)
                r["BUYUKLUK_KAT"] = dj_boot(gk.BUYUKLUK.to_numpy(), ay, an + "|BUYK", B, pay=gk.h_h.to_numpy())
                r["CIKIS_PAY"] = {"YUKARI": float(gk.YUK.mean()) if len(gk) else None, "ASAGI": float(gk.ASA.mean()) if len(gk) else None,
                                  "HIC": float(gk.HIC.mean()) if len(gk) else None,
                                  "CIKIS_BAR_med": float(gk.CIKIS_BAR.median()) if gk.CIKIS_BAR.notna().any() else None}
                r["YUKARI_PAY"] = dj_boot(gk.YUK.to_numpy(), ay, an + "|YUK", B)
                for yad, c in (("DEVAM_YUKARI", 1), ("DEVAM_ASAGI", -1)):
                    gg = gk[gk.CIKIS == c]
                    r[yad] = dj_boot(gg.DEVAM.to_numpy(), gg.ay.to_numpy(str), an + "|" + yad, B)
                    r[yad + "_SUR"] = dj_boot(gg.DEVAM_SUR.to_numpy(), gg.ay.to_numpy(str), an + "|" + yad + "_SUR", B)
                    r[yad + "_yok"] = int(gg.DEVAM.isna().sum())
                for ad in ("DUS", "YUKS"):
                    gg = gk[gk[f"DON_{ad}"].notna()]
                    r[f"DONUS_{ad}"] = {"n": int(len(gg)), "pay": float(gg[f"DON_{ad}"].mean()) if len(gg) else None,
                                        "taban": X.attrs[f"don_taban_{ad}"].get(h)}
                    r[f"DONUS_FARK_{ad}"] = dj_boot(gg[f"DONF_{ad}"].to_numpy(), gg.ay.to_numpy(str), an + f"|DONF_{ad}", B)
                bg = {}
                for i, (ad, lo, hi) in enumerate((("DIPTE", -np.inf, 1 / 3), ("ORTADA", 1 / 3, 2 / 3), ("TEPEDE", 2 / 3, np.inf))):
                    gg = gk[(gk.KONUM120 >= lo) & (gk.KONUM120 < hi)] if i else gk[gk.KONUM120 < hi]
                    bg[ad] = dj_boot(gg.TF.to_numpy(), gg.ay.to_numpy(str), an + f"|BAG_{ad}", B)
                r["BAGLAM"] = bg
            Hh[str(k)] = r
        out["hucre"][h] = Hh
        if tam:
            F: Dict[str, Any] = {}
            g1 = g[g.k == 1]
            for k in (2, 3, 4):
                gk = g[g.k == k]
                F[str(k)] = {c: dj_boot_fark(gk[c].to_numpy(), gk.ay.to_numpy(str), g1[c].to_numpy(), g1.ay.to_numpy(str), f"{h}|fark{k}|{c}", B)
                             for c in ("TF", "BUYF", "YUK")}
            out["fark"][h] = F
    # taban (herhangi gün) satırı: rastgele günlerin kendi değerleri (bilgi)
    tb = {}
    for h in hucreler:
        tg = T[T.hucre == h]
        if len(tg):
            tb[h] = {"n": int(len(tg)), "R15_ort": float(tg.R15.mean()), "R15_med": float(tg.R15.median()), "U2": float(tg.U2.mean()),
                     "D2": float(tg.D2.mean()), "BUYUKLUK": float(tg.BUYUKLUK.mean())}
    out["taban"] = tb
    return out


def _dj_birlestir(A: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Pazar sonuçlarını hücre anahtarlı tek sözlükte birleştirir."""
    o = {"hucre": {}, "fark": {}, "taban": {}, "dusen_tabansiz": {}}
    for p, r in A.items():
        o["hucre"].update(r["hucre"]); o["fark"].update(r.get("fark", {})); o["taban"].update(r.get("taban", {})); o["dusen_tabansiz"][p] = r["dusen_tabansiz"]
    return o


DJ_BH_OLCU = ("TOPLAM_FARK", "SECIM", "ASIMETRI", "BUYUKLUK_FARK", "DEVAM_YUKARI", "DEVAM_ASAGI", "DONUS_FARK_DUS", "DONUS_FARK_YUKS")


def dj_hukum(R: Dict[str, Any]) -> Dict[str, Any]:
    """BH + satır hükümleri + doz + çıkış + genel."""
    Hc = R["hucre"]; satir = []; p = []
    for k in DJ_KSIN:
        for ad in DJ_BH_OLCU:
            ps = [(Hc.get(h, {}).get(str(k), {}).get(ad) or {}).get("p") for h in DJ_ABD]
            satir.append((k, ad)); p.append(max(ps) if all(x is not None for x in ps) else None)
    q = HV._hv_bh(p, float(DJ_ESIK["bh"]["q"]))
    bh = {f"{k}|{ad}": {"p": pp, "q": qq, "gecti": (qq is not None and qq <= float(DJ_ESIK["bh"]["q"]))} for (k, ad), pp, qq in zip(satir, p, q)}
    H: Dict[str, Any] = {"bh": bh, "satir": {}}
    for k in DJ_KSIN:
        for ad in DJ_BH_OLCU:
            o = {h: Hc.get(h, {}).get(str(k), {}).get(ad) or {} for h in DJ_HUCRE}
            et = dj_etiket(o, "ort", bh[f"{k}|{ad}"]["gecti"], avr=True)
            if ad.startswith("DEVAM"):
                ab = [o[h] for h in DJ_ABD]
                if all(r.get("alt") is not None and r["alt"] > 0 for r in ab):
                    et = "ÇIKIŞ DEVAM EDİYOR" + ("" if bh[f"{k}|{ad}"]["gecti"] else " (BH GEÇMEDİ)")
                elif all(r.get("ust") is not None and r["ust"] < 0 for r in ab):
                    et = "ÇIKIŞ TERSE DÖNÜYOR (tuzak)" + ("" if bh[f"{k}|{ad}"]["gecti"] else " (BH GEÇMEDİ)")
                else:
                    et = dj_etiket(o, "ort", None, avr=False)
            H["satir"][f"{k}|{ad}"] = et
    doz = {}
    for ad, fk in (("TOPLAM_FARK", "TF"), ("BUYUKLUK_FARK", "BUYF"), ("YUKARI_PAY", "YUK")):
        seri = {h: {k: (Hc.get(h, {}).get(str(k), {}).get(ad) or {}).get("ort") for k in DJ_KSIN} for h in DJ_ABD}
        fark = {h: {k: R["fark"].get(h, {}).get(str(k), {}).get(fk) for k in (3, 4)} for h in DJ_ABD}
        doz[ad] = dj_doz(seri, fark)
    H["doz"] = doz; H["doz_hukum"] = "DOJİ SAYISI ETKİLİ" if any(d["etkili"] for d in doz.values()) else "DOJİ SAYISI ETKİSİZ (bu tanımla)"
    emare = any(H["satir"][f"{k}|TOPLAM_FARK"] in ("ARTI", "EKSİ") for k in DJ_KSIN) or H["doz_hukum"] == "DOJİ SAYISI ETKİLİ"
    H["genel"] = ("AÇIK VERİDE EMARE (kasa açılmaz; KASA KURALI: tek iz kasa açmaz; ileri test)" if emare
                  else "DOJİ ÖBEĞİ SONRASI AYIRT EDİCİ DEĞİL (bu tanımla)")
    return H


def dj_olcum(cikti: Optional[str] = None, ham: Optional[str] = None, kaynak: Optional[str] = None, git: bool = True, B: Optional[int] = None) -> Dict[str, Any]:
    """Kapı -> getiri (olay + taban) -> ölçüm (ANA tam; D15 ve HAFTA bilgi) -> dj_sonuc.json + dj_ozet.csv. BİR KEZ."""
    t0 = time.time(); kapi = dj_kapi(cikti, ham, git)
    A: Dict[str, Any] = {}; A15: Dict[str, Any] = {}; AH: Dict[str, Any] = {}
    for p in DJ_PAZAR:
        D = dj_depo(p, kaynak); dep = {k: D[k] for k in ("O", "H", "L", "C", "POS", "off")}
        P15, _ = YO.yo_P15(D["Op"], D["Cl"], D["P2"])
        T = pd.read_pickle(_dj_ham(f"taban_{p}.pkl", ham))
        Rt = pd.DataFrame(dj_getiri_dizi(dep, T.j, T.t, T.ATRP20), index=T.index)
        T = pd.concat([T, Rt[["E0", "R15", "U2", "D2", "BUYUKLUK", "R10B"]]], axis=1)
        T.to_pickle(_dj_ham(f"getiri_taban_{p}.pkl", ham), protocol=4)
        for kol, hedef in (("ANA", A), ("D15", A15)):
            X = dj_yukle(p, kol, ham)
            Rx = pd.DataFrame(dj_getiri_dizi(dep, X.j, X.t, X.ATRP20, X.bant_H, X.bant_L), index=X.index); Rx["P15"] = P15[X.d_row.to_numpy()]
            Rx.to_pickle(_dj_ham(f"getiri_{kol}_{p}.pkl", ham), protocol=4)
            hedef[p] = dj_olc_kol(pd.concat([X, Rx], axis=1), T, B, tam=(kol == "ANA"))
        W = pd.read_pickle(_dj_ham(f"olay_HAFTA_{p}.pkl", ham)); Rw = dj_hafta_getiri(D, W); Rw.to_pickle(_dj_ham(f"getiri_HAFTA_{p}.pkl", ham), protocol=4)
        W = pd.concat([W, Rw], axis=1); Tw = W[W.tip == "taban"]; t1 = Tw.groupby(["j", "hucre"]).R15.mean().rename("T1")
        Xw = W[W.tip == "olay"].join(t1, on=["j", "hucre"]); Xw = Xw[Xw.T1.notna()]; Xw["TF"] = Xw.R15 - Xw.T1
        AH[p] = {h: {str(k): dj_boot(Xw[(Xw.hucre == h) & (Xw.k == k)].TF.to_numpy(), Xw[(Xw.hucre == h) & (Xw.k == k)].ay.to_numpy(str),
                                     f"HAFTA|{h}|{k}", B) for k in DJ_KSIN} for h in DJ_HUCRE if h.startswith(p)}
        del D, dep; gc.collect()
    R = _dj_birlestir(A); R15_ = _dj_birlestir(A15)
    H = dj_hukum(R)
    J = {"surum": DJ_SURUM, "esik_sha": dj_esik_sha(), "kod_sha": dj_kod_sha(), "kapi": kapi, "zaman": MI._mi_simdi(),
         "ANA": R, "D15": {"hucre": {h: {k: {"n": v["n"], "TOPLAM_FARK": v["TOPLAM_FARK"]} for k, v in d.items()} for h, d in R15_["hucre"].items()}},
         "HAFTA": {h: d for p in AH for h, d in AH[p].items()}, "hukum": H, "sure_sn": round(time.time() - t0, 1)}
    MI._mi_jyaz(_dj_yol("sonuc", cikti), J, "dj sonuç")
    dj_ozet_csv(J, _dj_yol("ozet", cikti))
    djlog.info("ölçüm bitti (%.0f sn): %s", time.time() - t0, H["genel"])
    return J


def dj_ozet_csv(J: Dict[str, Any], yol: str) -> str:
    rows = []
    for h in DJ_HUCRE:
        for k in DJ_KSIN:
            r = J["ANA"]["hucre"].get(h, {}).get(str(k))
            if not r:
                continue
            g = lambda ad, f="ort": (r.get(ad) or {}).get(f)  # noqa: E731
            rows.append({"hucre": h, "k": DJ_KAD[k], "n": r["n"], "ay": r["ay"], "R15_ort": r["R15_ort"], "R15_med": r["R15_med"],
                         "TF": g("TOPLAM_FARK"), "TF_alt": g("TOPLAM_FARK", "alt"), "TF_ust": g("TOPLAM_FARK", "ust"),
                         "SECIM": g("SECIM"), "U2": r.get("U2"), "p_h": r.get("p_h"), "D2": r.get("D2"), "q_h": r.get("q_h"),
                         "ASM": g("ASIMETRI"), "ASM_alt": g("ASIMETRI", "alt"), "ASM_ust": g("ASIMETRI", "ust"),
                         "BUY_KAT": g("BUYUKLUK_KAT"), "BUY_KAT_alt": g("BUYUKLUK_KAT", "alt"), "BUY_KAT_ust": g("BUYUKLUK_KAT", "ust"),
                         "YUKARI": (r.get("CIKIS_PAY") or {}).get("YUKARI"), "ASAGI": (r.get("CIKIS_PAY") or {}).get("ASAGI"),
                         "HIC": (r.get("CIKIS_PAY") or {}).get("HIC"),
                         "DEVAM_YUK": g("DEVAM_YUKARI"), "DEVAM_YUK_alt": g("DEVAM_YUKARI", "alt"), "DEVAM_YUK_ust": g("DEVAM_YUKARI", "ust"),
                         "DEVAM_ASA": g("DEVAM_ASAGI"), "DEVAM_ASA_alt": g("DEVAM_ASAGI", "alt"), "DEVAM_ASA_ust": g("DEVAM_ASAGI", "ust"),
                         "DONUS_DUS": (r.get("DONUS_DUS") or {}).get("pay"), "DONUS_DUS_taban": (r.get("DONUS_DUS") or {}).get("taban"),
                         "DONUS_YUKS": (r.get("DONUS_YUKS") or {}).get("pay"), "DONUS_YUKS_taban": (r.get("DONUS_YUKS") or {}).get("taban"),
                         "hukum_TF": J["hukum"]["satir"].get(f"{k}|TOPLAM_FARK")})
    pd.DataFrame(rows).to_csv(yol + ".tmp", index=False, float_format="%.6g"); os.replace(yol + ".tmp", yol)
    return yol


# ================================================================ 7) ÖN KAYIT
DJ_YORUM = [
    "Kaynak veri YUKSELIS_ONCESI'nin bar deposudur (ham_*.npz; YO ön kaydındaki sha ile aynı): evren, geçerli bar, P2 ve takvim YO ile birebir; yeni veri indirilmez.",
    "ORT_BOY 'önceki 10 bar' = t - 10 .. t - 1 (t hariç) medyanı; ATR20 = YO ATRP20 x C_t (t dahil son 20 barın TR ortalaması): t barı kapanışında bilinir.",
    "'Ölü / fiyat adımına yapışmış' bar: geçersiz barlar veride hiç yok (MI.mi_veri); ayrıca (H - L) <= 3 x ADIM (son 20 barın en küçük fiyat farkı) olan bar doji "
    "sayılmaz (MUM_IZI_UC 'fiyat adımına yapışmış H = L' kuralının genişletilmiş hali; eşik önceden).",
    "'Aralarında en çok 2 mum' = kendi geçerli bar sırası farkı <= 3; ek olarak takvim satırı farkı <= 6 (arada kilitli / işlemsiz günler varsa bağlanmaz).",
    "Bant genişliği her yeni dojide o dojinin ATR20'si ile denetlenir (öbek bütün seviyeleri + yeni seviye); sınır dahil.",
    "Bir doji öbeğe katılmazsa YENİ öbeği başlatır (k = 1); öbek bir kez bittikten sonra eski öbeğe geri dönülmez.",
    "k = 4+ satırı = öbeğin 4. dojisi (öbek başına bir olay); 5. ve sonraki dojiler olay üretmez. k = 1 satırı = öbeği başlatan her doji (o an ikincisi bilinmiyor).",
    "Aynı öbek k = 1, 2, 3, 4 satırlarının her birine bir kez girer; k satırları ayrı ölçülür (bağımsız değil); k farkları aynı ay ağırlıklarıyla.",
    "Olay uygunluğu YO örnek kuralının her bar sürümü (dj_uygun; 5. barlarda YO.yo_ornek_maske ile birebir, test); ATRP20 sonlu > 0.",
    "HERHANGİ GÜN tabanı = YO örnek günleri (her 5. bar); T1 / p_h / q_h / h_h / T10 hisse x hücre ortalamaları; olayın hissesinin o hücrede taban günü yoksa olay "
    "düşer (sayısı rapora).",
    "+2 ATR / -1 ATR eşikleri E0'a göre oran olarak: hedef = E0 (1 + 2 ATRP20_t), stop = E0 (1 - ATRP20_t); ayna simetrik; aynı bar = stop önce (YO kuralı).",
    "Hareket büyüklüğü KAT = olayların toplam |R15| / (ATRP20 x karekök 15) / aynı hisselerin rastgele gün ortalamalarının toplamı; BUYUKLUK_FARK = fark ortalaması "
    "(hüküm ve BH bu satırda).",
    "Çıkış: barlar t + 1 .. t + 15 kapanışları; bant = olay anındaki öbek bandı (k doji); aynı kapanış hem üstte hem altta olamaz; HİÇ = 15 barda çıkış yok.",
    "Çıkış devamı R10 = C_{e+10} / O_{e+1} - 1, çıkış yönüyle çarpılır; e + 10 verinin dışında ya da 20 takvim satırını aşıyorsa yok (sayılır); kesik zaten veride.",
    "Çıkış devamı sürüklenmeden arındırılmış hali (DEVAM - yön x T10) BİLGİ satırıdır; hüküm iş tanımındaki ham devamla (> 0, alt > 0).",
    "Önceki yön C_t / C_{t-10} - 1 işaretiyle; dönüş tabanı aynı hücrenin taban günlerinde aynı önceki yönün dönüş payı (havuz; hisseye göre değil).",
    "Hüküm sırası ve BH ailesi DJ_ESIK['hukum'] / ['bh']: ARTI / EKSİ yalnız BH geçerse; aksi 'BH GEÇMEDİ'. AVR işareti iki AVR döneminde de.",
    "DOZ kuralında 'tek yönlü' = k = 1 -> 2 -> 3 -> 4+ art arda üç farkın hepsi aynı işaretli (eşit = tek yönlü değil), iki ABD döneminde aynı yönde.",
    "Bağlam (DİPTE / ORTADA / TEPEDE) ve D15, HAFTA kolları yalnız BİLGİ; hükmü değiştirmez; KONUM120 yoksa (120 bar yok) bağlam satırına girmez.",
    "Haftalık kol: mumlar günlük geçerli barlardan; giriş haftasının ilk günlük satırında P2; haftalar arası boşluk (giriş) <= 2 hafta, 15 hafta <= 29 hafta satırı.",
    "Evren bugün yaşayan hisseler: sonuç yukarı yanlı; TOPLAM FARK aynı hisseye göre olduğu için yanlılık kısmen düşer.",
    "Ölçüm bir kez koşar; getiri dosyası varsa kapı durur. Sonuçtan sonra yalnız gösterim değişebilir; aksi SAPMA.",
    "Getirisiz sayım: k = 4+ ABD iki döneminde n < 1.000 (844 / 532): bu satırda aralık sıfırı içerirse hüküm ÖLÇÜLEMEDİ olur (iddia kapanmaz); AVR k = 4+ "
    "n 140 / 58 (bilgi; işaret yine okunur, n < 30 değil). DOZ kuralı k = 4+ nokta değerini n'ye bakmadan kullanır (kural önceden böyle).",
    "Düşen (tabansız) olay sayısı ve DEVAM'ı ölçülemeyen çıkışlar rapora yazılır; dışlanır, yerine konmaz.",
]


def dj_onkayit_yaz(cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    S = dj_sayim(ham); sh = dj_dosya_sha(ham); yo_ok = open(os.path.join(KOK_DJ, "arastirma_cikti", "yukselis_oncesi", "YO_ON_KAYIT.md"), encoding="utf-8").read()
    for p in DJ_PAZAR:
        if sh[f"KAYNAK_ham_{p}.npz"] not in yo_ok:
            raise DJHata(f"K10: kaynak ham_{p}.npz sha YO ön kaydındakiyle aynı değil")
    L = [f"# DJ ÖN KAYIT — aynı seviyede doji öbekleri: doji sayısına göre sonrası ({MI._mi_simdi()})", "",
         "İş tanımı DJ_IS_TANIMI.md (ana model). Bu dosya R15 / U2 / D2 / çıkış / P15 HİÇBİR hücrede hesaplanmadan ÖNCE commit + push edilir; tanımlar, eşikler, "
         "okuma ve hüküm kuralları sonra değişmez (değişirse SAPMA). Evren bugün yaşayan hisseler (yukarı yanlı). KASA açılmaz (veri <= 2022-12-31).", "",
         "## Mühürler", "", f"DJ_KOD_SHA: {dj_kod_sha()}", f"DJ_ESIK_SHA: {dj_esik_sha()}"]
    L += [f"DOSYA_{a}: {v}" for a, v in sh.items()]
    L += [f"SAYIM_SHA: {HV.hv_json_sha(S)}", f"IS_TANIMI_SHA: {MI._mi_sha(DJ_YOL['is_tanimi'])}", "",
          f"- Olay / taban dosyaları (repo dışı): {DJ_YOL['ham']} (olay_*: getirisiz; getiri_* ölçümde ayrı dosya)", "",
          "## Eşik sözlüğü (DJ_ESIK; sha yukarıda)", "", "```json", json.dumps(DJ_ESIK, ensure_ascii=False, indent=1), "```", "",
          "## GETİRİSİZ SAYIM (R15 hesaplanmadı)", "", "| hücre | uygun hisse-gün | k | olay | bin hisse-günde | farklı ay | en kalabalık 3 ay payı | hisse |",
          "|---|---|---|---|---|---|---|---|"]
    for h in DJ_HUCRE:
        for k in DJ_KSIN:
            r = S["ANA"].get(h, {}).get(str(k), {})
            L.append(f"| {h} | {S['uygun'].get(h)} | {DJ_KAD[k]} | {r.get('n')} | {_f(r.get('bin_hisse_gun'), 2)} | {r.get('ay')} | {_f(r.get('ust3_pay'), 3)} | "
                     f"{r.get('hisse')} |")
    L += ["", "Öbek son uzunluğu dağılımı (öbek sayısı; BİLGİ): " + "; ".join(f"{h}: {S['obek_boy'].get(h)}" for h in DJ_HUCRE),
          "", "Yeni öbek başlatan dojilerin önceki dojiye bağlanmama nedeni: " + "; ".join(f"{h}: {S['red'].get(h)}" for h in DJ_HUCRE),
          "", "Taban günlerinde doji payı: " + "; ".join(f"{h}: {_f((S['taban_doji_pay'].get(h) or {}).get('doji_pay'), 4)}" for h in DJ_HUCRE),
          "", "D15 kolu olay sayıları: " + "; ".join(f"{h}: " + ", ".join(f"{DJ_KAD[k]} {S['D15'].get(h, {}).get(str(k), {}).get('n')}" for k in DJ_KSIN)
                                                for h in DJ_HUCRE),
          "", "HAFTA kolu olay sayıları: " + "; ".join(f"{h}: taban {S['HAFTA'].get(h, {}).get('taban_hafta')}, " +
                                                       ", ".join(f"{DJ_KAD[k]} {S['HAFTA'].get(h, {}).get(str(k), {}).get('n')}" for k in DJ_KSIN) for h in DJ_HUCRE),
          "", "## Yorum noktaları (ölçümden önce)", ""]
    L += [f"{i + 1}. {y}" for i, y in enumerate(DJ_YORUM)]
    L += ["", "## KONTROL LİSTESİ", "", "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    ad = {k["kod"]: k["ad"] for k in IK.IK_KONTROL}
    for k in IK.IK_KONTROL:
        y, kn = DJ_KONTROL[k["kod"]]
        L.append(f"| {k['kod']} | {ad[k['kod']]} | {y} | {kn} |")
    L += ["", "## SAPMA", "", "(yok; ölçümden sonra doldurulur)", ""]
    return MI._mi_yaz(_dj_yol("onkayit", cikti), "\n".join(L), "dj ön kayıt")


def _f(x: Any, n: int = 2, yuzde: bool = False) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    v = float(x) * (100 if yuzde else 1)
    return (f"{v:.{n}f}".replace(".", ",")) + ("%" if yuzde else "")


# ================================================================ 8) ÖRNEK PDF (sonrası çizilmez)
def _dj_pencere(D: Dict[str, np.ndarray], j: int, ilk: int, t: int, once: int) -> Dict[str, np.ndarray]:
    a = int(D["off"][j]); s = max(0, ilk - once)
    sl = slice(a + s, a + t + 1)   # olay barında biter: SONRASI YOK
    w = {c: D[c][sl].astype(float) for c in ("O", "H", "L", "C")}
    assert len(w["C"]) == t - s + 1, "geleceğe bakma kapısı: olay barından sonraki bar çizime girdi"
    w["s"] = s
    return w


def _dj_obek_dojiler(D: Dict[str, np.ndarray], j: int, ilk: int, t: int) -> List[int]:
    """Örnek sayfası için öbeğin dojileri: hissenin 0 .. t barlarıyla yeniden tespit (uygunluk süzgeci yok; yalnız t'ye kadarki barlar)."""
    a = int(D["off"][j]); O, H, L, C = (D[c][a:a + t + 1].astype(float) for c in ("O", "H", "L", "C"))
    F = _dj_ozellik(O, H, L, C); Dj = dj_doji(O, H, L, C)
    B = dj_obek(Dj["doji"], O, H, L, C, F["ATRP20"] * C, D["POS"][a:a + t + 1])
    out = B[(B.ilk == ilk) & (B.t <= t)].t.tolist()
    if not out or out[-1] != t:
        raise DJHata(f"örnek: öbek yeniden tespit edilemedi (j={j}, t={t})")
    return out


def _dj_ciz(ax, w: Dict[str, np.ndarray], dojiler: List[int], bH: float, bL: float, ilk: int, t: int, renk: str = "#1f4e9e", red: Optional[Tuple[int, int]] = None) -> None:
    import MUM_IZI_HAKEM as HK
    from matplotlib.patches import Rectangle
    s = w["s"]; O, H, L, C = w["O"], w["H"], w["L"], w["C"]; ref = float(C[-1])
    MI._mi_mum_ciz(ax, O, H, L, C, genislik=0.62)
    ax.add_patch(Rectangle((ilk - s - 0.5, bL), t - ilk + 1, bH - bL, facecolor="#ffb347", alpha=0.25, edgecolor="#ff7f00", linewidth=1.6, zorder=2))
    for y in (bH, bL):
        ax.hlines(y, ilk - s - 0.5, t - s + 0.5, color="#ff7f00", linewidth=1.2, linestyle="--", zorder=5)
    lo = float(np.nanmin(L)); hi = float(np.nanmax(H)); pad = 0.06 * (hi - lo)
    for d in dojiler:
        ax.plot(d - s, H[d - s] + pad * 0.5, marker="v", color=renk, markersize=9, zorder=6)
    if red is not None:
        for d in red:
            ax.plot(d - s, L[d - s] - pad * 0.5, marker="^", color="#c62828", markersize=9, zorder=6)
    y0, y1 = lo - pad, hi + pad; ax.set_ylim(y0, y1); ax.set_xlim(-0.8, len(C) - 0.2)
    _, yz = HK.hk_yuzde_adim(y0, y1, ref, HK.HK_ESIK_OLCEK)
    for p in yz:
        ax.axhline(ref * (1 + p / 100), color="#000000" if abs(p) < 1e-9 else "#9a9a9a", linewidth=1.0 if abs(p) < 1e-9 else 0.5,
                   linestyle="-" if abs(p) < 1e-9 else ":", zorder=1)
    ax.yaxis.tick_right(); ax.set_yticks([ref * (1 + p / 100) for p in yz]); ax.set_yticklabels([HK._hk_yuzde_yazi(p) for p in yz], fontsize=12)
    ax.set_xticks([]); ax.axvline(len(C) - 0.5, color="#555555", linewidth=0.8, linestyle="-.")


def dj_ornek_sec(ham: Optional[str] = None) -> Dict[str, Any]:
    """Tohumla rastgele örnekler (ANA olayları, iki pazar): k = 2 / 3 / 4+ için 4'er; sayılmayan 2 (SEVIYE_FARKLI, ARA_UZAK)."""
    E = DJ_ESIK["ornek"]; X = pd.concat([dj_yukle(p, "ANA", ham) for p in DJ_PAZAR], ignore_index=True)
    X = X[X.hucre.isin(DJ_HUCRE)].sort_values(["pazar", "sembol", "t", "k"], kind="stable").reset_index(drop=True)
    sec: Dict[str, Any] = {}
    for k in (2, 3, 4):
        g = X[X.k == k]; r = _dj_rng(f"ornek|{k}"); ii = r.choice(len(g), size=min(int(E["k_basina"]), len(g)), replace=False)
        sec[str(k)] = g.iloc[np.sort(ii)].to_dict("records")
    for ad in ("SEVIYE_FARKLI", "ARA_UZAK"):
        g = X[(X.k == 1) & (X.red == ad)]
        if ad == "ARA_UZAK":
            g = g[(g.onc_ara >= 4) & (g.onc_ara <= 6) & (g.onc_sev_atr <= 0.5)]
        r = _dj_rng(f"ornek|{ad}"); sec[ad] = [g.iloc[int(r.integers(len(g)))].to_dict()] if len(g) else []
    return {"X": X, "sec": sec}


def dj_ornek_pdf(cikti: Optional[str] = None, ham: Optional[str] = None, kaynak: Optional[str] = None, S: Optional[Dict[str, Any]] = None) -> str:
    """DJ_ORNEKLER.pdf: kapak (kural üç satır + sıklık) + k = 2 / 3 / 4+ 4'er gerçek örnek + 2 sayılmayan. Telefon ekranı (dikey); sonrası yok."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import MUM_IZI_HAKEM as HK
    from matplotlib.backends.backend_pdf import PdfPages
    S = S or dj_sayim(ham); Sc = dj_ornek_sec(ham); X = Sc["X"]; once = int(DJ_ESIK["ornek"]["once"])
    Dp = {p: dj_depo(p, kaynak) for p in DJ_PAZAR}
    yol = _dj_yol("pdf", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True); boy = (6.2, 10.4)
    don = {"d1619": "2016-19", "d2022": "2020-22"}
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=boy); fig.text(0.06, 0.95, "Doji öbekleri: gerçek örnekler", fontsize=19, weight="bold", va="top")
        kur = ("1) Doji: gövde mum boyunun en çok %10'u, mum boyu son 10 mumun\n    ortalama boyunun en az yarısı (ölü / tek fiyat adımı mumlar sayılmaz).\n"
               "2) Öbek: iki doji arasında en çok 2 mum var ve öbekteki bütün\n    dojilerin orta noktası (açılış + kapanış) / 2, yarım ATR'lik bir\n"
               "    bandın içinde (aynı fiyat seviyesi).\n"
               "3) Sayı k: öbekteki doji sayısı. Öbek, k'inci dojinin gününde,\n    yalnız o güne kadarki mumlarla tanınır (sonrası bilinmez).")
        fig.text(0.06, 0.88, kur, fontsize=11.2, va="top", linespacing=1.45)
        sat = ["Ne kadar sık? (bin işlem gününde kaç olay)", "", f"{'':10s}{'tek doji':>10s}{'k=2':>9s}{'k=3':>9s}{'k=4+':>9s}"]
        for h in DJ_HUCRE:
            v = [S["ANA"].get(h, {}).get(str(k), {}).get("bin_hisse_gun") for k in DJ_KSIN]
            sat.append(f"{h.replace('|d1619', ' 16-19').replace('|d2022', ' 20-22'):10s}" + "".join(f"{_f(x, 1):>9s} " for x in v))
        sat += ["", "Olay sayısı:"]
        for h in DJ_HUCRE:
            v = [S["ANA"].get(h, {}).get(str(k), {}).get("n") for k in DJ_KSIN]
            sat.append(f"{h.replace('|d1619', ' 16-19').replace('|d2022', ' 20-22'):10s}" + "".join(f"{str(x):>9s} " for x in v))
        fig.text(0.06, 0.52, "\n".join(sat), fontsize=10.5, va="top", family="monospace", linespacing=1.4)
        fig.text(0.06, 0.12, "Sayfalarda: mavi ok = doji, turuncu kutu = öbek bandı (dojilerin en\nyüksek / en düşük fiyatı). Grafik öbeğin tanındığı günde biter:\n"
                             "SONRASI YOK. Hisse adı ve tarih yazılmaz. Sağ eksen: son kapanışa\ngöre yüzde.", fontsize=10.5, va="top", linespacing=1.4)
        pdf.savefig(fig); plt.close(fig)
        no = 0
        for k in (2, 3, 4):
            for i, r in enumerate(Sc["sec"][str(k)]):
                no += 1; D = Dp[r["pazar"]]; j = int(r["j"]); t = int(r["t"]); ilk = int(r["ilk"])
                dj = _dj_obek_dojiler(D, j, ilk, t)
                w = _dj_pencere(D, j, ilk, t, once)
                fig = plt.figure(figsize=boy); ax = fig.add_axes([0.04, 0.53, 0.80, 0.37]); az = fig.add_axes([0.04, 0.24, 0.80, 0.24])
                _dj_ciz(ax, w, dj, float(r["bant_H"]), float(r["bant_L"]), ilk, t)
                _dj_ciz(az, _dj_pencere(D, j, ilk, t, int(DJ_ESIK["ornek"]["yakin"])), dj, float(r["bant_H"]), float(r["bant_L"]), ilk, t)
                az.set_title("yakından: öbek ve önceki 8 mum", fontsize=11, loc="left")
                fig.text(0.05, 0.965, f"{DJ_KAD[k].replace('k=4+', '4 ve üstü')} doji öbeği — örnek {i + 1} / 4", fontsize=16, weight="bold", va="top")
                fig.text(0.05, 0.925, f"{r['pazar']}, {don.get(r['hucre'].split('|')[1], '')}; öncesi {t - w['s'] - (t - ilk)} mum, öbek {t - ilk + 1} mum",
                         fontsize=11.5, va="top")
                ara = np.diff(dj) - 1 if len(dj) > 1 else []
                fig.text(0.05, 0.19, f"Doji sayısı: {len(dj)}; aradaki mum sayıları: {', '.join(str(int(a)) for a in ara)}\n"
                                     f"Seviyelerin yayılımı: {_f(r['sev_gen_atr'], 2)} ATR (sınır 0,50)\n"
                                     f"Öbek bandı (son kapanışa göre): {HK._hk_yuzde_yazi(round((r['bant_L'] / w['C'][-1] - 1) * 100, 1))} .. "
                                     f"{HK._hk_yuzde_yazi(round((r['bant_H'] / w['C'][-1] - 1) * 100, 1))}",
                         fontsize=12, va="top", linespacing=1.5)
                pdf.savefig(fig); plt.close(fig)
        for ad, yazi in (("SEVIYE_FARKLI", "SAYILMADI: seviye farklı. İki doji arasında en çok 2 mum var, ama\norta noktaları yarım ATR'den uzak: "
                                            "aynı fiyat seviyesi değil."),
                         ("ARA_UZAK", "SAYILMADI: ara uzak. İki doji aynı seviyede (yarım ATR içinde),\nama arada 3'ten çok mum var.")):
            for r in Sc["sec"].get(ad, []):
                D = Dp[r["pazar"]]; j = int(r["j"]); t = int(r["t"]); onc = t - int(r["onc_ara"])
                Xi = X[(X.pazar == r["pazar"]) & (X.j == j) & (X.t == onc)]
                w = _dj_pencere(D, j, onc, t, once)
                a = int(D["off"][j]); bH = float(max(D["H"][a + onc], D["H"][a + t])); bL = float(min(D["L"][a + onc], D["L"][a + t]))
                fig = plt.figure(figsize=boy); ax = fig.add_axes([0.04, 0.53, 0.80, 0.37]); az = fig.add_axes([0.04, 0.24, 0.80, 0.24])
                _dj_ciz(ax, w, [], bH, bL, onc, t, red=(onc, t))
                _dj_ciz(az, _dj_pencere(D, j, onc, t, int(DJ_ESIK["ornek"]["yakin"])), [], bH, bL, onc, t, red=(onc, t))
                az.set_title("yakından: iki doji ve önceki 8 mum", fontsize=11, loc="left")
                fig.text(0.05, 0.965, "Sayılmayan örnek", fontsize=16, weight="bold", va="top")
                fig.text(0.05, 0.925, f"{r['pazar']}, {don.get(r['hucre'].split('|')[1], '')}; kırmızı ok = iki doji", fontsize=11.5, va="top")
                fig.text(0.05, 0.19, yazi + f"\nAradaki mum: {int(r['onc_ara']) - 1}; seviye farkı: {_f(r['onc_sev_atr'], 2)} ATR (sınır 0,50)"
                         + ("" if len(Xi) else "\n(önceki doji uygunluk dışı bir günde)"), fontsize=12, va="top", linespacing=1.5)
                pdf.savefig(fig); plt.close(fig)
    return yol


# ================================================================ 9) RAPOR
def _dj_ar(o: Optional[Dict[str, Any]], n: int = 2, yuzde: bool = True, ad: str = "ort") -> str:
    o = o or {}
    return f"{_f(o.get(ad), n, yuzde)} [{_f(o.get('alt'), n, yuzde)}; {_f(o.get('ust'), n, yuzde)}]"


def dj_rapor_yaz(cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    J = json.load(open(_dj_yol("sonuc", cikti), encoding="utf-8")); ekyol = _dj_ham("dj_rapor_ek.json", ham)
    EK = json.load(open(ekyol, encoding="utf-8")) if os.path.exists(ekyol) else {}
    R = J["ANA"]["hucre"]; H = J["hukum"]
    L = [f"# DJ RAPOR — aynı seviyede doji öbekleri: doji sayısına göre sonrası", "",
         f"Kod sha {J['kod_sha'][:12]}, eşik sha {J['esik_sha'][:12]}; ön kayıt commit {J['kapi'].get('onkayit_commit', '—')}. Evren bugün yaşayan hisseler "
         "(yukarı yanlı). Getiriler fiyat değişimidir (komisyon / kayma yok). Kasa açılmadı (veri <= 2022-12-31).", "",
         "## SONUÇ", "", f"GENEL: {H['genel']}", f"DOZ - YANIT: {H['doz_hukum']}", "",
         "### Yön (R15, TOPLAM FARK = R15 - aynı hissenin rastgele günü)", "",
         "| hücre | k | n | ay | R15 ort | R15 medyan | TOPLAM FARK [%95] | SEÇİM [%95] | +2ATR önce | rastgele | -2ATR önce | rastgele | ASİMETRİ [%95] |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for h in DJ_HUCRE:
        for k in DJ_KSIN:
            r = R.get(h, {}).get(str(k)) or {}
            L.append(f"| {h} | {DJ_KAD[k]} | {r.get('n')} | {r.get('ay')} | {_f(r.get('R15_ort'), 2, True)} | {_f(r.get('R15_med'), 2, True)} | "
                     f"{_dj_ar(r.get('TOPLAM_FARK'))} | {_dj_ar(r.get('SECIM'))} | {_f(r.get('U2'), 1, True)} | {_f(r.get('p_h'), 1, True)} | "
                     f"{_f(r.get('D2'), 1, True)} | {_f(r.get('q_h'), 1, True)} | {_dj_ar(r.get('ASIMETRI'), 1)} |")
        tb = J["ANA"]["taban"].get(h)
        if tb:
            L.append(f"| {h} | herhangi gün | {tb['n']} | — | {_f(tb['R15_ort'], 2, True)} | {_f(tb['R15_med'], 2, True)} | — | — | {_f(tb['U2'], 1, True)} | — | "
                     f"{_f(tb['D2'], 1, True)} | — | — |")
    L += ["", "Hüküm (TOPLAM FARK): " + "; ".join(f"{DJ_KAD[k]} {H['satir'][f'{k}|TOPLAM_FARK']}" for k in DJ_KSIN),
          "Hüküm (ASİMETRİ): " + "; ".join(f"{DJ_KAD[k]} {H['satir'][f'{k}|ASIMETRI']}" for k in DJ_KSIN),
          "Hüküm (SEÇİM): " + "; ".join(f"{DJ_KAD[k]} {H['satir'][f'{k}|SECIM']}" for k in DJ_KSIN), "",
          "### Hareketin büyüklüğü (|R15| / (ATRP20 x karekök 15); KAT = olay / aynı hissenin rastgele günü)", "",
          "| hücre | k | olay | rastgele | KAT [%95] | FARK [%95] |", "|---|---|---|---|---|---|"]
    for h in DJ_HUCRE:
        for k in DJ_KSIN:
            r = R.get(h, {}).get(str(k)) or {}
            L.append(f"| {h} | {DJ_KAD[k]} | {_f(r.get('BUYUKLUK'), 3)} | {_f(r.get('h_h'), 3)} | {_dj_ar(r.get('BUYUKLUK_KAT'), 3, False)} | "
                     f"{_dj_ar(r.get('BUYUKLUK_FARK'), 3, False)} |")
    L += ["", "Hüküm (BÜYÜKLÜK FARKI): " + "; ".join(f"{DJ_KAD[k]} {H['satir'][f'{k}|BUYUKLUK_FARK']}" for k in DJ_KSIN), "",
          "### Çıkış yönü (öbek bandı; 15 bar içinde ilk kapanış) ve devam (çıkıştan sonraki 10 bar, çıkış yönünde)", "",
          "| hücre | k | yukarı | aşağı | hiç | çıkış barı (medyan) | DEVAM yukarı [%95] (n) | DEVAM aşağı [%95] (n) | sürüklenmesiz yukarı | sürüklenmesiz aşağı |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for h in DJ_HUCRE:
        for k in DJ_KSIN:
            r = R.get(h, {}).get(str(k)) or {}; c = r.get("CIKIS_PAY") or {}
            L.append(f"| {h} | {DJ_KAD[k]} | {_f(c.get('YUKARI'), 1, True)} | {_f(c.get('ASAGI'), 1, True)} | {_f(c.get('HIC'), 1, True)} | {_f(c.get('CIKIS_BAR_med'), 0)} | "
                     f"{_dj_ar(r.get('DEVAM_YUKARI'))} ({(r.get('DEVAM_YUKARI') or {}).get('n')}) | {_dj_ar(r.get('DEVAM_ASAGI'))} "
                     f"({(r.get('DEVAM_ASAGI') or {}).get('n')}) | {_dj_ar(r.get('DEVAM_YUKARI_SUR'))} | {_dj_ar(r.get('DEVAM_ASAGI_SUR'))} |")
    L += ["", "Hüküm (DEVAM yukarı): " + "; ".join(f"{DJ_KAD[k]} {H['satir'][f'{k}|DEVAM_YUKARI']}" for k in DJ_KSIN),
          "Hüküm (DEVAM aşağı): " + "; ".join(f"{DJ_KAD[k]} {H['satir'][f'{k}|DEVAM_ASAGI']}" for k in DJ_KSIN), "",
          "### Önceki 10 bara göre (dönüş payı = R15 işareti önceki yönün tersi)", "",
          "| hücre | k | düşüş sonrası n | dönüş | taban | FARK [%95] | yükseliş sonrası n | dönüş | taban | FARK [%95] |", "|---|---|---|---|---|---|---|---|---|---|"]
    for h in DJ_HUCRE:
        for k in DJ_KSIN:
            r = R.get(h, {}).get(str(k)) or {}; a = r.get("DONUS_DUS") or {}; b = r.get("DONUS_YUKS") or {}
            L.append(f"| {h} | {DJ_KAD[k]} | {a.get('n')} | {_f(a.get('pay'), 1, True)} | {_f(a.get('taban'), 1, True)} | {_dj_ar(r.get('DONUS_FARK_DUS'), 1)} | "
                     f"{b.get('n')} | {_f(b.get('pay'), 1, True)} | {_f(b.get('taban'), 1, True)} | {_dj_ar(r.get('DONUS_FARK_YUKS'), 1)} |")
    L += ["", "Hüküm (dönüş, düşüş sonrası): " + "; ".join(f"{DJ_KAD[k]} {H['satir'][f'{k}|DONUS_FARK_DUS']}" for k in DJ_KSIN),
          "Hüküm (dönüş, yükseliş sonrası): " + "; ".join(f"{DJ_KAD[k]} {H['satir'][f'{k}|DONUS_FARK_YUKS']}" for k in DJ_KSIN), "",
          "### Doz - yanıt (k = 1 -> 2 -> 3 -> 4+)", ""]
    for ad, d in H["doz"].items():
        L.append(f"- {ad}: yön (ABD 16-19, 20-22) {d['yon']}, tek yönlü {d['tek_yonlu']}, k3 / k4+ - k1 farkı ayrışıyor {d['fark_ayrisiyor']} -> "
                 f"{'ETKİLİ' if d['etkili'] else 'etkisiz'}")
    L += ["", "k - tek doji farkları (TOPLAM FARK, ABD):"]
    for h in DJ_ABD:
        L.append(f"- {h}: " + "; ".join(f"k={k} - 1: {_dj_ar(J['ANA']['fark'][h][str(k)]['TF'], 2, True, 'fark')}" for k in (2, 3, 4)))
    L += ["", "### BİLGİ satırları (hükmü değiştirmez)", "", "Bağlam (TOPLAM FARK, KONUM120 üçte biri):"]
    for h in DJ_HUCRE:
        L.append(f"- {h}: " + " | ".join(f"{DJ_KAD[k]}: " + ", ".join(f"{b} {_dj_ar((R.get(h, {}).get(str(k)) or {}).get('BAGLAM', {}).get(b), 2)} "
                                                                     f"(n {((R.get(h, {}).get(str(k)) or {}).get('BAGLAM', {}).get(b) or {}).get('n')})"
                                                                     for b in ("DIPTE", "ORTADA", "TEPEDE")) for k in DJ_KSIN))
    L += ["", "D15 kolu (gövde <= 0,15 boy; TOPLAM FARK):"]
    for h in DJ_HUCRE:
        L.append(f"- {h}: " + "; ".join(f"{DJ_KAD[k]} n {(J['D15']['hucre'].get(h, {}).get(str(k)) or {}).get('n')} "
                                         f"{_dj_ar((J['D15']['hucre'].get(h, {}).get(str(k)) or {}).get('TOPLAM_FARK'))}" for k in DJ_KSIN))
    L += ["", "HAFTA kolu (haftalık mum, 15 hafta; TOPLAM FARK):"]
    for h in DJ_HUCRE:
        L.append(f"- {h}: " + "; ".join(f"{DJ_KAD[k]} n {(J['HAFTA'].get(h, {}).get(str(k)) or {}).get('n')} {_dj_ar(J['HAFTA'].get(h, {}).get(str(k)))}"
                                         for k in DJ_KSIN))
    L += ["", f"Tabanı olmayan (hissenin o hücrede rastgele günü yok) düşen olay: {J['ANA']['dusen_tabansiz']}", "",
          "## KONTROL LİSTESİ", "", "| Kod | Yanıt | Kanıt |", "|---|---|---|"]
    L += [f"| {k} | {y} | {kn} |" for k, (y, kn) in DJ_KONTROL.items()]
    L += ["", "## Yeniden üretim (bağımsız kısa kod)", ""] + [f"- {x}" for x in EK.get("yeniden", ["(yok)"])]
    L += ["", "## HATA", ""] + [f"- {x}" for x in EK.get("hata", ["(yok)"])]
    L += ["", "## SAPMA", ""] + [f"- {x}" for x in EK.get("sapma", ["(yok)"])]
    L += ["", "## ÖNERİLEN DEFTER SATIRLARI", ""] + [f"- {x}" for x in EK.get("defter", ["(ana model yazar)"])]
    return MI._mi_yaz(_dj_yol("rapor", cikti), "\n".join(L) + "\n", "dj rapor")


# ================================================================ 10) ÇAKIŞMA KAPISI + KOMUT
def _cakisma_kontrol_dj(_once=_CK_ONCE_DJ, _dosya="DOJI_OBEK.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_DJ",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_dj()


def _dj_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="DOJI_OBEK")
    ap.add_argument("komut", choices=["hazirla", "sayim", "ornek", "onkayit", "olcum", "rapor", "sha"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "hazirla":
            print(json.dumps(MI._mi_json(dj_hazirla()), ensure_ascii=False, indent=1))
        elif a.komut == "sayim":
            S = dj_sayim(); MI._mi_jyaz(_dj_ham("dj_sayim.json"), S, "dj sayım")
            print(json.dumps(MI._mi_json({k: S[k] for k in ("ANA", "obek_boy", "red", "uygun")}), ensure_ascii=False, indent=1)); print("SAYIM_SHA:", HV.hv_json_sha(S))
        elif a.komut == "ornek":
            print(dj_ornek_pdf())
        elif a.komut == "onkayit":
            print(dj_onkayit_yaz())
        elif a.komut == "olcum":
            J = dj_olcum(); print(json.dumps(MI._mi_json({"genel": J["hukum"]["genel"], "doz": J["hukum"]["doz_hukum"]}), ensure_ascii=False, indent=1))
        elif a.komut == "rapor":
            print(dj_rapor_yaz())
        elif a.komut == "sha":
            print(json.dumps({"kod": dj_kod_sha(), "esik": dj_esik_sha()}, indent=1))
    except DJHata as ex:
        djlog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_dj_ana())
