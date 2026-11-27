"""COL_SKOR6 — Cemal'in eski çöl puanı (GEN10_COL_OGREN v5: altı ölçü) örneklem dışında (27 Kasım 2026).

İş tanımı: arastirma_cikti/col_skor6/CS_IS_TANIMI.md (ana model). Altı ölçü (tanımlar iş tanımı 1. bölümde 'eski koddaki gibi AYNEN'; SABİT):
  F1 doji oranı (gövde / boy < 0,40), F2 Bollinger genişliği daralması, F3 daralmanın yüksekten başlaması, F4 fiyat sıkışması, F5 sol bacak düşüşü,
  F6 hacim azalması. PUAN_ESIT = ortalama x 100; PUAN_OGR = eski kodun ağırlık yöntemi, ağırlıklar YALNIZ ABD 2016-19'dan (eski etiket SAG10).
(a) KİTAPLIK TESPİTİ: Cemal'in 20 çölünün (BIST 2024-26) puanı BIST 2016-22 pencere dağılımının neresinde (YALNIZ puan; bölge bitişinden sonra hiçbir bar
    okunmaz: seri bolge_bit'te kesilir, assert).
(b) Ölçüm: ABD / AVR (karar), BIST (bilgi); 2016-19 ve 2020-22; pencere L = 20 / 40 / 80 bar, her hissede her 5 barda bir pencere sonu; yüksek puanlı
    pencerelerden sonra SAG10 / SOL10 (eski etiket ve aynası), ATRP20 beşliği içinde KAT ve ASİMETRİ, TOPLAM FARK (R15 - aynı hissenin ortalaması),
    +2 ATR / -1 ATR payları, SEÇİM (R15 - PİYASA(t)); ay kümeli bootstrap (10.000; tohum 2713); BH q 0,10; hüküm önceden.
Veri <= 2022-12-31 (assert + KASA kapısı); TEK İSTİSNA kitaplık puanı (BIST tam veri, yalnız bölge bitişine kadar). KASA AÇILMAZ.
Mevcut modüller DEĞİŞTİRİLMEZ; içe alınır (YUKSELIS_ONCESI: dokunma vektörü, P15, beşlik, dönem; MUM_IZI_UC: kilitli pay; MUM_IZI / MUM_IZI_HAVUZ: veri,
yazma, git, ay özeti, BH; KART_TUR2: P2 evreni).

Komut:  python COL_SKOR6.py hazirla   üç pazarın pencere panelleri (getirisiz) -> /root/.kasa/ham/col_skor6
        python COL_SKOR6.py sayim     GETİRİSİZ SAYIM + getirisiz kesimler + KİTAPLIK TESPİTİ (sayim.json, kitaplik.json)
        python COL_SKOR6.py onkayit   CS_ON_KAYIT.md (mühürler + sayım + kitaplık + yorum noktaları + kontrol tablosu)
        python COL_SKOR6.py kesif     kapı -> YALNIZ ABD 2016-19 SAG10 -> PUAN_OGR ağırlıkları -> cs_kesim.json + CS_KESIM.md
        python COL_SKOR6.py olcum     kapı + kesim kapısı -> ölçüm (bir kez) -> cs_sonuc.json + cs_ozet.csv
        python COL_SKOR6.py rapor     CS_RAPOR.md (sonuç json'undan)
        python COL_SKOR6.py sha       kod / eşik sha
Colab:  exec(open('COL_SKOR6.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7: sonuç yukarı yanlı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_CS = {k: id(v) for k, v in globals().items()}

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

KOK_CS = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_CS not in sys.path:
    sys.path.insert(0, KOK_CS)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ; veri, yazma, git, sha)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ; açık kopya yolu)
import MUM_IZI_HAVUZ as HV  # noqa: E402  (DEĞİŞTİRİLMEZ; kesik, dönem, ay özeti, BH, json sha)
import YUKSELIS_ONCESI as YO  # noqa: E402  (DEĞİŞTİRİLMEZ; dokunma vektörü, P15, beşlik)

cslog = logging.getLogger("col.col_skor6")
if not cslog.handlers:
    _cs_h = logging.StreamHandler(sys.stderr)
    _cs_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s col_skor6: %(message)s", "%H:%M:%S"))
    cslog.addHandler(_cs_h)
    cslog.setLevel(logging.INFO)
    cslog.propagate = False


class CSHata(RuntimeError):
    """Durdurucu hata: kapı / şema / veri / kesik / sıra / yeniden üretim uyuşmazlığı."""


CS_SURUM = "COL_SKOR6 v1.0 (2026-11-27): eski çöl puanı (altı ölçü) örneklem dışında + kitaplık tespiti"
CS_YOL = {"cikti": os.path.join(KOK_CS, "arastirma_cikti", "col_skor6"), "kod": os.path.join(KOK_CS, "COL_SKOR6.py"),
          "ham": "/root/.kasa/ham/col_skor6", "acik": MV.MV_YOL["gunluk"], "tam_bist": "/tmp/veri",
          "is_tanimi": os.path.join(KOK_CS, "arastirma_cikti", "col_skor6", "CS_IS_TANIMI.md")}
CS_DOSYA = {"onkayit": "CS_ON_KAYIT.md", "kesim_md": "CS_KESIM.md", "kesim": "cs_kesim.json", "sonuc": "cs_sonuc.json", "ozet": "cs_ozet.csv",
            "rapor": "CS_RAPOR.md"}
CS_KESIK = pd.Timestamp("2022-12-31")
CS_PAZAR = ("ABD", "AVR", "BIST")
CS_DONEM = ("d1619", "d2022")
CS_KESIF = "ABD|d1619"
CS_L = (20, 40, 80)
CS_F = ["F1", "F2", "F3", "F4", "F5", "F6"]
CS_F_AD = {"F1": "doji oranı", "F2": "BBW daralması", "F3": "BBW başlangıcı", "F4": "fiyat sıkışması", "F5": "sol bacak düşüşü", "F6": "hacim azalması"}
CS_KOL = ["PUAN_ESIT", "PUAN_OGR"] + CS_F

# KİTAPLIK (eski koddan aynen; sembol, col_bas, col_bit; BIST)
CS_KITAPLIK: List[Tuple[str, str, str]] = [
    ("BINBN", "2024-12-23", "2025-01-22"), ("NUGYO", "2024-12-08", "2024-12-22"), ("ENSRI", "2025-05-27", "2025-07-22"),
    ("TEHOL", "2024-11-06", "2024-12-12"), ("PAPIL", "2024-09-02", "2025-02-28"), ("ESCAR", "2024-09-22", "2025-03-02"),
    ("KTLEV", "2024-07-01", "2025-03-31"), ("TEHOL", "2026-01-26", "2026-03-02"), ("HDFGS", "2025-04-28", "2025-06-23"),
    ("ASELS", "2025-11-17", "2025-12-08"), ("VENUS", "2025-05-26", "2025-06-23"), ("BURLS", "2026-03-10", "2026-04-08"),
    ("EUREN", "2026-04-01", "2026-04-07"), ("ECOGR", "2025-12-01", "2026-03-19"), ("SURGT", "2025-12-23", "2026-01-26"),
    ("SMRVA", "2026-03-03", "2026-04-08"), ("DOGUB", "2026-02-02", "2026-03-02"), ("MANAS", "2025-10-13", "2025-11-27"),
    ("KAPLM", "2025-07-14", "2025-08-25"), ("KRVGD", "2025-04-01", "2025-09-01"),
]

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
CS_ESIK: Dict[str, Any] = {
    "surum": "CS-1.0",
    "tohum": 2713,
    "tohum_tanim": "np.random.default_rng([2713, crc32(anahtar)]); bootstrap anahtarı 'kol|uç|L|hücre'; sıra bağımsız, tekrarlanabilir",
    "veri": "MUM_IZI.mi_veri(pazar, MUM_IZI_V2.MV_YOL['gunluk']) (açık kopya <= 2022-12-30; geçerli bar O/H/L/C > 0 sonlu, H > L, V > 0; ABD evren dışı "
            "fon listesi; açılış H-L dışıysa kırpılır); kitaplık: MUM_IZI.mi_veri('BIST', '/tmp/veri') (tam BIST; yalnız bölge bitişine kadar)",
    "olcu": {
        "F1": "penceredeki mumlardan |C - O| / (H - L) < 0,40 olanların payı (geçerli barlarda H > L)",
        "F2": "(BBW[s] - min BBW[s..t]) / BBW[s]; BBW = 4 x std20 / SMA20 (kapanış; std pandas rolling varsayılanı ddof 1; yalnız o bara kadarki kapanışlar)",
        "F3": "kırp(BBW[s] / 0,6; 0..1)",
        "F4": "kırp(1 - (maks H[s..t] - min L[s..t]) / ((maks + min) / 2); 0..1)",
        "F5": "kırp((maks H[s-30..s-1] - min L[s..t]) / maks H[s-30..s-1]; 0..1)",
        "F6": "kırp(1 - ort V[s..t] / ort V[maks(0, s-200)..s-1]; 0..1); önceki bar sayısı >= 20",
        "bbw_bolen": 0.6, "doji_esik": 0.40, "sol": 30, "hacim_onceki": 200, "hacim_en_az": 20,
        "pencere": "pencere = hissenin kendi geçerli barları s..t (s = t - L + 1); ön şart s >= 30 (F5'in önceki 30 barı tam; F2 / F3 BBW[s] ve F6 önceki "
                   ">= 20 bar bununla sağlanır)",
        "PUAN_ESIT": "100 x ortalama(F1..F6)",
        "PUAN_OGR": "100 x sum(w_i F_i); w_i = |ort(F_i | SAG10 = 1) - ort(F_i | SAG10 = 0)| / std(F_i) (ddof 0, popülasyon), sum w = 1; YALNIZ ABD 2016-19 "
                    "ölçüm popülasyonundan, L başına ayrı; öteki pazar / dönemlere aynen",
    },
    "pencere": {"L": [20, 40, 80], "adim": 5,
                "tanim": "her hissede pencere sonu t = hissenin kendi geçerli bar indeksi k, k % 5 == 0 (0'dan; YUKSELIS_ONCESI ile aynı örnekleme); "
                         "pencere sonu tarihi 2015-12-01 .. 2022-12-31 tutulur",
                "kilitli": {"pay": 0.20, "tanim": "MUM_IZI_UC.uc_kilitli_pay: pencerenin takvim aralığında (s barı günü .. t barı günü) ham veride geçersiz "
                                                  "(H <= L, V <= 0, fiyat <= 0 / sonlu değil: kilitli / hacimsiz / fiyat adımına yapışmış H = L) bar payı "
                                                  "> 0,20 -> pencere ATILIR"}},
    "evren": {"ABD_AVR": "TEZGÂH 2 P2 havuzu: KART_TUR2.k2_panel(Vd, pazar) -> P2[d, j]; pencere ölçümde <=> giriş barı t + 1'in satırında P2 "
                         "(YUKSELIS_ONCESI ile aynı)",
              "BIST": "MUM_IZI8 / MUM_IZI_UC E2 kuralı: pencere sonu barı t'de işlem değeri (C x V) aynı gün BIST kesit medyanının (o gün geçerli barı olan "
                      "bütün hisseler) üstünde; PİYASA(t) kümesi giriş satırı d için d - 1 satırındaki bu bayrak",
              "kitaplik_dagilim": "KİTAPLIK karşılaştırması: BIST bütün pencereleri (evren süzgeci YOK; kitaplık bölgeleri de süzülmedi), pencere sonu "
                                  "2016-01-01 .. 2022-12-31, ön şart + kilitli değil + altı ölçü sonlu"},
    "sonuc": {"SAG10": "maks H[t+1..t+20] >= C_t x 1,10 (eski etiket: pencere son kapanışına göre sonraki 20 bar)",
              "SOL10": "min L[t+1..t+20] <= C_t x 0,90 (ayna)",
              "R15": "C[t+15] / O[t+1] - 1 (giriş = sonraki geçerli bar açılışı)",
              "ATR2_YUK": "giriş E0 = O[t+1]; t+1..t+15 barlarında ilk H >= E0 (1 + 2 ATRP20_t), ilk L <= E0 (1 - ATRP20_t) barından ÖNCE (aynı bar = stop "
                          "önce; YO.yo_ilk_dokunma)",
              "ATR2_ASG": "ayna: ilk L <= E0 (1 - 2 ATRP20_t), ilk H >= E0 (1 + ATRP20_t) barından önce",
              "P15": "PİYASA(t) = YO.yo_P15 (giriş satırı d'de küme açılışından 15 satırlık eşit ağırlıklı getiri); SECIM = R15 - P15",
              "uygun": "t + 1 var ve pos[t+1] - pos[t] <= 10 takvim satırı; t + 20 var ve pos[t+20] - pos[t+1] <= 39 (2 x 20 - 1); giriş tarihi 2016-01-01 "
                       ".. 2022-12-31; t + 20 barının tarihi <= 2022-12-31; ATRP20_t sonlu",
              "ATRP20": "son 20 barın TR (önceki kapanışla; ilk bar H - L) ortalaması / C_t (YUKSELIS_ONCESI ATRP20 formülü)"},
    "hucre": {"tanim": "giriş tarihine göre MUM_IZI_HAVUZ.hv_hucre_ad (d1619 = 2016-19, d2022 = 2020-22)", "kesif": "ABD|d1619",
              "karar": ["ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022"], "bilgi": ["BIST|d1619", "BIST|d2022"]},
    "kesim": {"uc": [0.10, 0.02], "besli": [0.2, 0.4, 0.6, 0.8],
              "tanim": "üst dilim = değer >= kendi pazarının 2016-19 ölçüm popülasyonu dağılımının %90 (%98) yüzdeliği (eşitler dahil; gerçek pay yazılır); "
                       "pazar ve L başına; beşlik sınırları %20/40/60/80 aynı kural; ATRP20 beşlik sınırları aynı popülasyondan; PUAN_ESIT ve F1..F6 kesimleri "
                       "GETİRİSİZ (ön kayıtta); PUAN_OGR kesimleri ağırlıklar öğrenildikten sonra aynı kuralla (getirisiz dağılım) KEŞİF aşamasında",
              "nump": "np.quantile (doğrusal)"},
    "olc": {"populasyon": "hücrede (pazar x dönem) ölçüme uygun (evren + sonuç penceresi), ön şart + kilitli değil + altı ölçü sonlu + ATRP20 sonlu "
                          "pencereler; taban da bu küme",
            "KAT_HAM": "P(SAG10 | uç) / P(SAG10)",
            "KAT": "ATRP içi: sum(SAG10 uçta) / sum(p_q) uçta; p_q = hücrede ATRP20 beşliği q'nun P(SAG10)'u (olay ağırlıklı)",
            "ASIMETRI": "[P(SAG10) - P(SOL10)] uçta - sum_q (n_uq / n_u) [P(SAG10 | q) - P(SOL10 | q)]",
            "TOPLAM_FARK": "R15 - T1; T1 = aynı hissenin aynı hücredeki ölçüme uygun BÜTÜN pencere sonlarının (L'den bağımsız; ön şart / kilitli / ölçü "
                           "aranmaz) R15 ortalaması (rastgele gün tabanı)",
            "bilgi": "R15 ortalaması, SECIM = R15 - P15, ATR2_YUK / ATR2_ASG payları (uç ve taban)",
            "mantik": "YUKSELIS_ONCESI.yo_olc ile aynı hesap (nokta değerleri birebir, testte); bootstrap tohumu 2713"},
    "boot": {"B": 10000, "kume": "giriş ayı (YYYY-AA)", "tanim": "ay kümeli bootstrap (multinomial ağırlık); %95 = 2,5 / 97,5 yüzdelik",
             "p": "tek yönlü p = (1 + #(KAT* <= 1)) / (B + 1), ABD 2020-22"},
    "bh": {"q": 0.10, "aile": "(2 puan + 6 ölçü) x 2 uç x 3 uzunluk = 48 satır; p = ABD 2020-22 ATRP içi KAT p'si"},
    "hukum": {"n_min": 1000, "ay_min": 12,
              "sira": "ÖLÇÜLEMEDİ > TUTAR > YALNIZ OYNAKLIK > TEK DÖNEM > TERS > TUTMADI",
              "OLCULEMEDI": "ABD 2016-19 ya da ABD 2020-22'de n < 1000 ya da farklı ay < 12",
              "TUTAR": "ABD'nin iki döneminde de KAT > 1 ve alt > 1 VE ASİMETRİ > 0 ve alt > 0 VE TOPLAM FARK > 0 ve alt > 0 VE AVR'nin iki döneminde (n >= 30) "
                       "(KAT - 1), ASİMETRİ, TOPLAM FARK nokta değerleri > 0 VE BH (q 0,10) geçer",
              "YALNIZ_OYNAKLIK": "KAT_HAM alt > 1 iki ABD döneminde, ama birinde ATRP içi KAT alt <= 1 ya da ASİMETRİ <= 0",
              "TEK_DONEM": "üç şart (KAT, ASİMETRİ, TOPLAM FARK alt uçları > eşik) iki ABD döneminden yalnız birinde",
              "TERS": "ABD 2020-22'de KAT üst < 1 VE ASİMETRİ üst < 0", "TUTMADI": "ötekiler",
              "doz": "beşliklerde ATRP içi KAT; DOZ-YANIT VAR <=> iki ABD döneminde de Spearman(beşlik no, KAT) >= 0,9 VE en üst beşlik KAT alt > 1 (bilgi)",
              "GENEL": "en az bir satır TUTAR ise 'AÇIK VERİDE ADAY (KASA KURALI: tek iz kasa açmaz; ileri test)'; aksi 'ESKİ ÇÖL PUANI ÖRNEKLEM DIŞINDA "
                       "AYIRT EDİCİ DEĞİL (bu tanımlarla)'"},
    "kitaplik": {"tanim": "her bölge: tam BIST serisi bolge_bit'te KESİLİR (assert), pencere = bas <= tarih <= bit geçerli barlar; altı ölçü + PUAN_ESIT; L* = "
                          "20 / 40 / 80'den bar sayısına en yakını (eşitlikte küçük); yüzdelik sıra = BIST 2016-22 dağılımında ((küçük + 0,5 eşit) / n); "
                          "kilitli payı bilgi (atılmaz, yazılır)",
                 "olcu": "üst %10 (sıra >= 0,90), üst %30 (>= 0,70), medyan altı (< 0,50) sayıları; ölçü ölçü aynı; ölçü başına kitaplık yüzdelik "
                         "sıralarının medyanı",
                 "veri_yok": "sembol tam BIST panelinde yok / bölge kapsanmıyor / s < 30 / bar < 2 -> 'veri yok'"},
    "kesik": "ölçüm verisi en büyük tarihi <= 2022-12-31 (HV.hv_kesik_kapi her pazar) + KASA.kasa_kapisi(açık V dosyaları, '2022-12-31')",
    "sira": "kod + sentetik test -> getirisiz sayım + kitaplık -> ön kayıt commit + push -> ik_kontrol_kapisi -> KEŞİF (yalnız ABD 2016-19 SAG10; ağırlıklar) "
            "-> cs_kesim.json + CS_KESIM.md commit + push -> ölçüm (bir kez) -> rapor",
}

CS_YORUM = [
    "Eski kodun (GEN10_COL_OGREN v5) metni repoda yok; formüller iş tanımı 1. bölümden ('eski koddaki tanımlar AYNEN') birebir kodlandı. BBW'nin standart "
    "sapması pandas rolling varsayılanıyla (ddof 1) alındı (Colab kodu pandas `.rolling(20).std()` ile yazılmış varsayımı); F2'de kırpma yok (tanım gereği 0..1).",
    "Pencere hissenin kendi GEÇERLİ barlarıdır (kilitli / hacimsiz / H = L barlar veriden önce çıkar); pencerenin takvim aralığında geçersiz bar payı > %20 "
    "ise pencere atılır (MUM_IZI_UC kuralı). Kalan geçersiz barlar sayılmaz (doji sayımında 'fiyat adımına yapışmış' bar doji sayılmaz).",
    "Pencere sonu t her hissede k % 5 == 0 barları; pencereler L > 5 olduğu için ÖRTÜŞÜR; çıkarım ay kümeli bootstrap ile (günler bağımsız sayılmaz).",
    "Ön şart s >= 30 (pencere başından önce 30 bar): F5 tanımındaki 'önceki 30 bar' tam olsun diye; F6 'önceki 200 bar' eksikse mevcut (>= 20) bar.",
    "F6 hacmi yerel birimde (BIST lot, AVR yerel); oran olduğu için birim etkisizdir.",
    "Dönem giriş tarihine göre (t + 1). ABD / AVR evreni giriş satırında P2 (YO ile aynı); BIST evreni pencere sonu barında işlem değeri > kesit medyanı.",
    "KİTAPLIK dağılımı evren süzgeçsizdir (BIST bütün pencereleri, pencere sonu 2016-22); L* en yakın uzunluk (5 barlık EUREN -> 20; 190 barlık KTLEV -> 80). "
    "Ölçü başına 'kitaplık medyanının yüzdelik sırası' = bölgelerin kendi L*'larındaki yüzdelik sıralarının medyanı.",
    "Kitaplık verisi tam BIST dosyasından (2024-26; /tmp/veri/V_BIST.pkl); bu veri yalnız puan için okunur, sonrası (bitişten sonraki tek bar) okunmaz; "
    "kod seriyi bolge_bit'te keser ve assert eder.",
    "Üst dilim yönü sabit: altı ölçünün hepsinde ve iki puanda 'yüksek = daha çöl' (eski kodun yönü); uç = değer >= %90 (%98) yüzdeliği, eşitler dahil "
    "(F3 ve F6 kırpmada 1 / 0'a yığılabilir; gerçek pay yazılır).",
    "PUAN_OGR ağırlıkları ABD 2016-19'da öğrenilir: bu hücrede PUAN_OGR örneklem İÇİDİR; örneklem dışı sınama ABD 2020-22 ve AVR'dir. Hüküm iş tanımındaki "
    "gibi iki ABD dönemini ister (keşif hücresinin örneklem içi olduğu raporda yazılır).",
    "ATRP20 beşlik sınırları ve bütün kesimler pazarın kendi 2016-19 ölçüm popülasyonundan (L başına); 2020-22'ye aynen uygulanır.",
    "Aynı barda hedef ve stop (ATR2): stop önce (YO.yo_ilk_dokunma; kötümser, iki yönde aynı). SAG10 / SOL10 yalnız uç fiyat (eski etiket; ikisi birden 1 olabilir).",
    "TOPLAM FARK tabanı (T1) L'den bağımsızdır: hissenin o hücredeki ölçüme uygun bütün pencere sonlarının R15 ortalaması (rastgele gün; YO ile aynı).",
    "BH p'si ABD 2020-22 ATRP içi KAT'ın tek yönlü bootstrap p'si; aile 48 satır. AVR yönü nokta değerlerle (aralık aranmaz), AVR hücresi n >= 30.",
    "BIST yalnız bilgi: hükme girmez; aynı tablo kalıbıyla yazılır.",
    "Kitaplık bölgelerinin altı ölçüsü kendi başlangıç - bitişiyle (bar sayısı değişken); karşılaştırma dağılımı sabit L* pencereleridir.",
    "Kesikli / yığılmalı ölçüler (getirisiz sayımda görüldü): F1 kesikli (k / L), F6 pencerelerin ~%40'ında 0 (kırpma), F3 BIST'te %98 yüzdeliği 1 (kırpma). "
    "Beşlik sınırları çakışırsa (F6: %20 = %40 = 0) boş beşlik KAT'ı yazılmaz ('-'), o hücrede doz - yanıt rho'su hesaplanmaz; uç satırların gerçek payı n ile yazılır.",
    "F2 ve F3 Bollinger genişliğinden gelir; F3 (başlangıç BBW'si) oynaklığın kendisidir: bu yüzden ham KAT ile ATRP içi KAT ayrı yazılır, hüküm ATRP içiyle.",
]

CS_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban aynı hücre (pazar x dönem) aynı evren aynı L popülasyonu; ATRP20 beşliği içi KAT ve ASİMETRİ (oynaklığın mekanik etkisi dışlanır; "
                   "K60 / Ç255 dersi); SOL10 aynası mekanik üstünlüğü ölçer; TOPLAM FARK aynı hissenin rastgele gün ortalamasına göre (T1); SEÇİM = R15 - PİYASA(t)"),
    "K2": ("EVET", "altı ölçü yalnız s..t ve öncesi barlardan (test: t + 1 ve sonrası bozulunca aynı); giriş t + 1 açılışı; sonuç ayrı fonksiyonda ve KEŞİF'te "
                   "yalnız ABD 2016-19 (assert); ağırlıklar yalnız ABD 2016-19 (assert); kitaplık seri bolge_bit'te kesilir (assert); veri <= 2022-12-31 assert + KASA"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0, O/H/L/C sonlu > 0); geçersiz bar payı > %20 pencere atılır (MUM_IZI_UC.uc_kilitli_pay); sonuç penceresi "
                   "20 bar <= 40 takvim satırı"),
    "K4": ("EVET", "hisse başına her 5 barda bir pencere sonu (örtüşme ay kümeli bootstrap ile); n pencere ve farklı ay ayrı yazılır; en kalabalık 3 ay payı"),
    "K5": ("EVET", "R15 / ATR2 / P15 girişi t + 1 açılışı; SAG10 / SOL10 eski etiket gereği pencere son kapanışına göre (iş tanımı; ayrıca yazıldı)"),
    "K6": ("EVET", "OS / MI bölünme düzeltmeli açık kopya; ölçüler oransal (birim etkisiz); hacim oranı yerel birim / kendi geçmişi"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma): sonuç yukarı yanlı; raporda yazılır; kasa açılmaz"),
    "K8": ("EVET", "n >= 1.000 ve farklı ay >= 12 olmayan satır ÖLÇÜLEMEDİ; iki dönem + iki pazar; BH q 0,10 (48 satır aile); kitaplık n = 20 'tespit' (bulgu değil)"),
    "K9": ("EVET", "CS_ON_KAYIT.md: CS_KOD_SHA, CS_ESIK_SHA, panel sha'ları, SAYIM_SHA, KITAPLIK_SHA + yorum noktaları; KEŞİF ön kayıt commit + push'tan sonra "
                   "(kapı); ölçüm cs_kesim.json commit'inden sonra (kapı); ikinci koşu durur"),
    "K10": ("EVET", "altı ölçü elle hesaplanmış örnekler + bağımsız döngü uygulamasıyla birebir (test); panel şeması / satır sayısı sayım sha ile; dokunma YO ile aynı fonksiyon"),
    "K11": ("EVET", "rapordan önce >= 3 satır panel + sonuç dosyalarından bağımsız kısa kodla yeniden üretilir (raporda)"),
    "K12": ("EVET", "'iz / aday' sözü yalnız hüküm kuralıyla; oynaklıkla açıklanan satır 'YALNIZ OYNAKLIK'; PUAN_OGR ABD 2016-19'da örneklem içi diye yazılır; "
                    "kitaplık 'kodun puanı Cemal'in çölünü tanıyor mu' tespiti, sonrası ölçülmez"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_cs); mevcut modüller / defter dosyaları değişmez (yalnız import); yalnız kendi yolları commit; sızıntı "
                    "taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez, kasa açılmaz"),
}


# ================================================================ 0) YARDIMCI
def _cs_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or CS_YOL["cikti"], CS_DOSYA[ad])


def _cs_ham(ad: str, ham: Optional[str] = None) -> str:
    return os.path.join(ham or CS_YOL["ham"], ad)


def cs_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or CS_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def cs_kod_sha() -> str:
    return MI._mi_sha(CS_YOL["kod"])


def _cs_rng(anahtar: str) -> np.random.Generator:
    return np.random.default_rng([int(CS_ESIK["tohum"]), zlib.crc32(str(anahtar).encode("utf-8"))])


def cs_kesik_kapi(V: Dict[str, pd.DataFrame], ad: str = "veri") -> pd.Timestamp:
    try:
        return HV.hv_kesik_kapi(V, ad, CS_KESIK)
    except HV.HVHata as ex:
        raise CSHata(str(ex)) from ex


def _kirp(x: np.ndarray) -> np.ndarray:
    return np.clip(x, 0.0, 1.0)


def _roll(x: np.ndarray, w: int, f: str) -> np.ndarray:
    return getattr(pd.Series(np.asarray(x, float)).rolling(w, min_periods=w), f)().to_numpy(float)


# ================================================================ 1) ALTI ÖLÇÜ (yalnız s..t ve öncesi barlar)
def cs_bbw(C: np.ndarray) -> np.ndarray:
    """BBW = 4 x std20 (ddof 1) / SMA20 (kapanış); i barındaki değer yalnız i - 19 .. i kapanışlarından."""
    s = pd.Series(np.asarray(C, float))
    with np.errstate(invalid="ignore", divide="ignore"):
        return (4.0 * s.rolling(20, min_periods=20).std() / s.rolling(20, min_periods=20).mean()).to_numpy(float)


def cs_dizi(O: Any, H: Any, L: Any, C: Any, V: Any) -> Dict[str, np.ndarray]:
    """Bir hissenin L'den bağımsız ön dizileri (geçerli barlar)."""
    O, H, L, C, V = (np.asarray(a, float) for a in (O, H, L, C, V))
    E = CS_ESIK["olcu"]
    with np.errstate(invalid="ignore", divide="ignore"):
        dj = (np.abs(C - O) / (H - L) < float(E["doji_esik"])) & (H > L)
    return {"O": O, "H": H, "L": L, "C": C, "V": V, "BBW": cs_bbw(C), "cdj": np.r_[0.0, np.cumsum(dj.astype(float))],
            "cV": np.r_[0.0, np.cumsum(V)], "mxH30": _roll(H, int(E["sol"]), "max")}


def cs_olcu(D: Dict[str, np.ndarray], s: Any, t: Any) -> Dict[str, np.ndarray]:
    """Pencereler [s_i, t_i] (hissenin bar indeksleri) için F1..F6 + PUAN_ESIT. Ön şart s >= 30 ve t < m (aksi NaN). Yalnız t_i'ye kadarki barlar."""
    E = CS_ESIK["olcu"]; s = np.asarray(s, np.int64); t = np.asarray(t, np.int64); N = len(s); m = len(D["C"])
    out = {a: np.full(N, np.nan) for a in CS_F + ["PUAN_ESIT"]}
    ok = (s >= int(E["sol"])) & (t < m) & (t >= s)
    if not ok.any():
        return out
    Lw = (t - s + 1)
    for Lu in np.unique(Lw[ok]):
        j = np.flatnonzero(ok & (Lw == Lu)); ss = s[j]; tt = t[j]; Lu = int(Lu)
        bmin = _roll(D["BBW"], Lu, "min")[tt]; mxH = _roll(D["H"], Lu, "max")[tt]; mnL = _roll(D["L"], Lu, "min")[tt]
        b0 = D["BBW"][ss]
        a0 = np.maximum(0, ss - int(E["hacim_onceki"])); cnt = ss - a0
        with np.errstate(invalid="ignore", divide="ignore"):
            F1 = (D["cdj"][tt + 1] - D["cdj"][ss]) / Lu
            F2 = (b0 - bmin) / b0
            F3 = _kirp(b0 / float(E["bbw_bolen"]))
            F4 = _kirp(1.0 - (mxH - mnL) / ((mxH + mnL) / 2.0))
            m30 = D["mxH30"][ss - 1]
            F5 = _kirp((m30 - mnL) / m30)
            vw = (D["cV"][tt + 1] - D["cV"][ss]) / Lu; vp = (D["cV"][ss] - D["cV"][a0]) / np.maximum(cnt, 1)
            F6 = np.where(cnt >= int(E["hacim_en_az"]), _kirp(1.0 - vw / vp), np.nan)
        for a, v in zip(CS_F, (F1, F2, F3, F4, F5, F6)):
            v = np.asarray(v, float); v[~np.isfinite(v)] = np.nan; out[a][j] = v
    M = np.stack([out[a] for a in CS_F], 1)
    out["PUAN_ESIT"] = np.where(np.isfinite(M).all(1), 100.0 * M.mean(1), np.nan)
    return out


def cs_atrp20(H: Any, L: Any, C: Any) -> np.ndarray:
    """YUKSELIS_ONCESI ATRP20 formülü (test: YO.yo_hisse_ozellik ile birebir)."""
    H, L, C = (np.asarray(a, float) for a in (H, L, C)); pc = np.r_[np.nan, C[:-1]]
    TR = np.where(np.isfinite(pc), np.maximum(H, pc) - np.minimum(L, pc), H - L)
    with np.errstate(invalid="ignore", divide="ignore"):
        return _roll(TR, 20, "mean") / C


def cs_puan_ogr(F: Dict[str, np.ndarray], w: Dict[str, float]) -> np.ndarray:
    M = np.stack([np.asarray(F[a], float) for a in CS_F], 1); ww = np.array([float(w[a]) for a in CS_F])
    return np.where(np.isfinite(M).all(1), 100.0 * (M @ ww), np.nan)


def cs_agirlik(F: Dict[str, np.ndarray], y: np.ndarray) -> Dict[str, float]:
    """Eski kodun ağırlık yöntemi: w_i = |ort(F_i | y = 1) - ort(F_i | y = 0)| / std(F_i) (ddof 0), toplam 1."""
    y = np.asarray(y, float); r = {}
    for a in CS_F:
        x = np.asarray(F[a], float); f = np.isfinite(x) & np.isfinite(y)
        x, yy = x[f], y[f]
        if (yy == 1).sum() < 2 or (yy == 0).sum() < 2:
            raise CSHata(f"ağırlık: {a} için iki sınıf da yok")
        sd = float(np.std(x))
        r[a] = abs(float(x[yy == 1].mean()) - float(x[yy == 0].mean())) / sd if sd > 0 else 0.0
    t = sum(r.values())
    if not t > 0:
        raise CSHata("ağırlık toplamı 0")
    return {a: v / t for a, v in r.items()}


# ================================================================ 2) KİTAPLIK (yalnız puan; bölge bitişinden sonrası OKUNMAZ)
def cs_kitaplik_bolge(d: pd.DataFrame, bas: Any, bit: Any, gecersiz: Optional[pd.DatetimeIndex] = None) -> Dict[str, Any]:
    """Tek bölge: seri bolge_bit'te KESİLİR (assert), pencere = bas <= tarih <= bit geçerli barlar; altı ölçü + PUAN_ESIT + kilitli payı."""
    from MUM_IZI_UC import uc_kilitli_pay
    bas = pd.Timestamp(bas); bit = pd.Timestamp(bit)
    x = d[d.index <= bit]
    assert (not len(x)) or x.index.max() <= bit, "kitaplık: bölge bitişinden sonraki bar okundu"
    if gecersiz is not None:
        gecersiz = pd.DatetimeIndex(gecersiz); gecersiz = gecersiz[gecersiz <= bit]
    ix = np.flatnonzero((x.index >= bas) & (x.index <= bit))
    if len(ix) < 2:
        return {"durum": "veri yok", "neden": "bölge kapsanmıyor (geçerli bar < 2)", "bar": int(len(ix))}
    s, t = int(ix[0]), int(ix[-1])
    if s < int(CS_ESIK["olcu"]["sol"]):
        return {"durum": "veri yok", "neden": f"bölgeden önce {s} bar (< 30)", "bar": int(t - s + 1)}
    D = cs_dizi(x.Open, x.High, x.Low, x.Close, x.Volume)
    assert len(D["C"]) == len(x) and x.index[t] <= bit
    o = cs_olcu(D, [s], [t])
    kp = float(uc_kilitli_pay(gecersiz if gecersiz is not None else pd.DatetimeIndex([]), x.index, [x.index[s]], [x.index[t]])[0])
    n = t - s + 1; Ls = min(CS_L, key=lambda L: (abs(n - L), L))
    return {"durum": "tamam", "bar": int(n), "L": int(Ls), "ilk": str(x.index[s].date()), "son": str(x.index[t].date()), "kilitli_pay": kp,
            **{a: (float(o[a][0]) if np.isfinite(o[a][0]) else None) for a in CS_F + ["PUAN_ESIT"]}}


def cs_yuzdelik(x: Optional[float], dag: np.ndarray) -> Optional[float]:
    if x is None or not len(dag):
        return None
    return float(((dag < x).sum() + 0.5 * (dag == x).sum()) / len(dag))


def cs_kitaplik(dagilim: Dict[int, Dict[str, np.ndarray]], tam: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """20 bölge: altı ölçü, PUAN_ESIT, L*; BIST 2016-22 dağılımında (dagilim[L][kol]) yüzdelik sıra. tam = MI.mi_veri('BIST', tam yol) çıktısı."""
    if tam is None:
        tam = MI.mi_veri("BIST", CS_YOL["tam_bist"])
    V = tam["V"]; G = tam.get("gecersiz", {}); sat = []
    for sem, bas, bit in CS_KITAPLIK:
        d = V.get(sem)
        if d is None:
            r = {"durum": "veri yok", "neden": "sembol tam BIST panelinde yok", "bar": 0}
        else:
            r = cs_kitaplik_bolge(d, bas, bit, G.get(sem))
        r = {"sembol": sem, "bas": bas, "bit": bit, **r}
        if r["durum"] == "tamam":
            for a in CS_F + ["PUAN_ESIT"]:
                r[f"{a}_sira"] = cs_yuzdelik(r[a], dagilim[r["L"]][a])
        sat.append(r)
    ok = [r for r in sat if r["durum"] == "tamam"]
    oz: Dict[str, Any] = {"bolge": len(sat), "veri_var": len(ok)}
    for a in CS_F + ["PUAN_ESIT"]:
        v = np.array([r[f"{a}_sira"] for r in ok if r.get(f"{a}_sira") is not None], float)
        oz[a] = {"ust10": int((v >= 0.90).sum()), "ust30": int((v >= 0.70).sum()), "medyan_alti": int((v < 0.50).sum()),
                 "sira_medyan": float(np.median(v)) if len(v) else None, "n": int(len(v))}
    del V; gc.collect()
    return {"satir": sat, "ozet": oz}


# ================================================================ 3) PENCERE PANELİ (getirisiz)
def cs_pencere_hisse(d: pd.DataFrame, pos: np.ndarray, idx: pd.DatetimeIndex, gec: Optional[pd.DatetimeIndex]) -> Dict[str, np.ndarray]:
    """Bir hisse: pencere sonları t (k % 5 == 0), sonuç uygunluğu (getirisiz), ATRP20, her L için F1..F6, PUAN_ESIT, kilitli payı."""
    from MUM_IZI_UC import uc_kilitli_pay
    m = len(d); P = CS_ESIK["pencere"]
    D = cs_dizi(d.Open, d.High, d.Low, d.Close, d.Volume)
    t = np.arange(0, m, int(P["adim"]), dtype=np.int64)
    dt = d.index[t]; t = t[(dt >= pd.Timestamp("2015-12-01")) & (dt <= CS_KESIK)]
    out: Dict[str, np.ndarray] = {"t": t, "t_row": pos[t]}
    if not len(t):
        return out
    at = cs_atrp20(D["H"], D["L"], D["C"]); out["ATRP20"] = at[t]
    g1 = np.minimum(t + 1, m - 1); g20 = np.minimum(t + 20, m - 1)
    gt = d.index[g1]; s20 = d.index[g20]
    uy = (t + 20 < m) & (pos[g1] - pos[t] <= 10) & (pos[g20] - pos[g1] <= 39) & (gt >= pd.Timestamp("2016-01-01")) & (gt <= CS_KESIK) & (s20 <= CS_KESIK)
    uy &= np.isfinite(out["ATRP20"])
    out["uygun"] = uy; out["d_row"] = np.where(t + 1 < m, pos[g1], -1); out["giris"] = np.where(t + 1 < m, gt.values, np.datetime64("NaT"))
    gec = pd.DatetimeIndex(gec) if gec is not None else pd.DatetimeIndex([])
    for L in CS_L:
        s = t - L + 1; o = cs_olcu(D, s, t)
        for a in CS_F + ["PUAN_ESIT"]:
            out[f"{a}_{L}"] = o[a].astype(np.float32)
        kp = np.full(len(t), np.nan); okp = s >= 0
        if okp.any():
            kp[okp] = uc_kilitli_pay(gec, d.index, d.index[s[okp]], d.index[t[okp]])
        out[f"KIL_{L}"] = kp.astype(np.float32); out[f"ON_{L}"] = s >= int(CS_ESIK["olcu"]["sol"])
    return out


def cs_bist_evren(Vd: Dict[str, Any], idx: pd.DatetimeIndex, S: List[str]) -> np.ndarray:
    """BIST: EV[r, j] = o satırda geçerli barı olan hisseler arasında işlem değeri (C x V) kesit medyanının üstü."""
    n, u = len(idx), len(S); DV = np.full((n, u), np.nan)
    for j, s in enumerate(S):
        d = Vd["V"][s]; p = idx.get_indexer(d.index); DV[p, j] = (d.Close * d.Volume).to_numpy(float)
    with np.errstate(invalid="ignore"):
        med = np.nanmedian(np.where(np.isfinite(DV), DV, np.nan), axis=1)
        return np.isfinite(DV) & (DV > med[:, None])


def cs_hazirla_pazar(pazar: str, ham: Optional[str] = None, Vd: Optional[Dict[str, Any]] = None, P2: Optional[np.ndarray] = None,
                     idx: Optional[pd.DatetimeIndex] = None, S: Optional[List[str]] = None) -> Dict[str, Any]:
    """Veri -> evren -> pencere paneli (özellik, getirisiz) + sonuç bar deposu (ayrı dosya). Getiri hesaplanmaz."""
    t0 = time.time(); ham = ham or CS_YOL["ham"]; os.makedirs(ham, exist_ok=True)
    if Vd is None:
        Vd = MI.mi_veri(pazar, CS_YOL["acik"])
    cs_kesik_kapi(Vd["V"], f"günlük {pazar}")
    for s0, d0 in list(Vd["V"].items())[:50]:
        if "Volume" not in d0.columns:
            raise CSHata(f"{pazar} {s0}: hacim sütunu yok")
    if P2 is None and pazar in ("ABD", "AVR"):
        import KART_TUR2 as KT2
        Pn, P2 = KT2.k2_panel(Vd, pazar); idx = Pn["tarih"]; S = list(Pn["sembol"]); del Pn; gc.collect()
    if idx is None:
        idx = pd.DatetimeIndex(sorted(set().union(*[d.index for d in Vd["V"].values()])))
    S = list(S) if S is not None else sorted(Vd["V"])
    if not set(Vd["V"]) <= set(S):
        raise CSHata(f"{pazar}: veri sembolleri panel sembollerinde değil")
    n, u = len(idx), len(S)
    Op = np.full((n, u), np.nan); Cl = np.full((n, u), np.nan)
    EVB = cs_bist_evren(Vd, idx, S) if P2 is None else None
    if P2 is None:                                               # BIST: PİYASA(t) kümesi d satırında d - 1 bayrağı
        P2 = np.zeros((n, u), bool); P2[1:] = EVB[:-1]
    parca = []; Ob, Hb, Lb, Cb, POSb, off = [], [], [], [], [], [0]
    for j, s in enumerate(S):
        d = Vd["V"].get(s)
        if d is None:
            off.append(off[-1]); continue
        pos = idx.get_indexer(d.index)
        if (pos < 0).any():
            raise CSHata(f"K10: {pazar} {s}: tarih takvimde yok")
        Op[pos, j] = d.Open.to_numpy(float); Cl[pos, j] = d.Close.to_numpy(float)
        Ob.append(d.Open.to_numpy(float)); Hb.append(d.High.to_numpy(float)); Lb.append(d.Low.to_numpy(float)); Cb.append(d.Close.to_numpy(float))
        POSb.append(pos.astype(np.int64)); off.append(off[-1] + len(d))
        if len(d) < 2:
            continue
        W = cs_pencere_hisse(d, pos, idx, Vd.get("gecersiz", {}).get(s))
        if not len(W["t"]):
            continue
        W["j"] = np.full(len(W["t"]), j, np.int64)
        if EVB is not None:
            W["EVREN"] = EVB[W["t_row"], j]
        else:
            dr = W["d_row"]; W["EVREN"] = np.where(dr >= 0, P2[np.maximum(dr, 0), j], False)
        parca.append(pd.DataFrame(W))
    X = pd.concat(parca, ignore_index=True)
    X["pazar"] = pazar; X["sembol"] = np.asarray(S, object)[X.j.to_numpy()]; X["tarih"] = idx[X.t_row.to_numpy()]
    X["giris"] = pd.to_datetime(X.giris)
    X["hucre"] = [HV.hv_hucre_ad(g, pazar) if pd.notna(g) else f"{pazar}|yok" for g in X.giris]
    X["ay"] = X.giris.dt.strftime("%Y-%m").fillna("")
    yol_x = _cs_ham(f"pencere_{pazar}.pkl", ham); yol_h = _cs_ham(f"depo_{pazar}.npz", ham)
    with open(yol_x, "wb") as f:
        pickle.dump(X, f, protocol=4)
    np.savez(yol_h, O=np.concatenate(Ob), H=np.concatenate(Hb), L=np.concatenate(Lb), C=np.concatenate(Cb), POS=np.concatenate(POSb),
             off=np.asarray(off, np.int64), Op=Op, Cl=Cl, P2=P2, tarih=np.asarray(idx.values.astype("datetime64[ns]")), sembol=np.asarray(S, dtype="U32"))
    cslog.info("%s: %d pencere sonu, %d hisse (%.0f sn)", pazar, len(X), u, time.time() - t0)
    del Op, Cl, P2; gc.collect()
    return {"pazar": pazar, "satir": int(len(X)), "hisse": u, "dosya": {"pencere": yol_x, "depo": yol_h}}


def cs_hazirla(ham: Optional[str] = None) -> Dict[str, Any]:
    out = {}
    for p in CS_PAZAR:
        out[p] = cs_hazirla_pazar(p, ham); gc.collect()
    return out


def cs_yukle(pazar: str, ham: Optional[str] = None) -> pd.DataFrame:
    with open(_cs_ham(f"pencere_{pazar}.pkl", ham), "rb") as f:
        return pickle.load(f)


def cs_dosya_sha(ham: Optional[str] = None) -> Dict[str, str]:
    return {ad: MI._mi_sha(_cs_ham(ad, ham)) for p in CS_PAZAR for ad in (f"pencere_{p}.pkl", f"depo_{p}.npz")}


def cs_pop(X: pd.DataFrame, L: int) -> np.ndarray:
    """Ölçüm popülasyonu (getirisiz): uygun + evren + ön şart + kilitli değil + altı ölçü sonlu + ATRP20 sonlu + dönem içi."""
    kp = float(CS_ESIK["pencere"]["kilitli"]["pay"])
    m = X.uygun.to_numpy(bool) & X.EVREN.to_numpy(bool) & X[f"ON_{L}"].to_numpy(bool) & ~(X[f"KIL_{L}"].to_numpy(float) > kp)
    m &= np.isfinite(X[f"PUAN_ESIT_{L}"].to_numpy(float)) & np.isfinite(X.ATRP20.to_numpy(float))
    m &= X.hucre.str.split("|").str[1].isin(CS_DONEM).to_numpy(bool)
    return m


def cs_dag_maske(X: pd.DataFrame, L: int) -> np.ndarray:
    """Kitaplık karşılaştırma dağılımı (BIST; evren süzgeçsiz): pencere sonu 2016-22, ön şart, kilitli değil, altı ölçü sonlu."""
    kp = float(CS_ESIK["pencere"]["kilitli"]["pay"]); tr = X.tarih
    return ((tr >= pd.Timestamp("2016-01-01")) & (tr <= CS_KESIK)).to_numpy(bool) & X[f"ON_{L}"].to_numpy(bool) & \
        ~(X[f"KIL_{L}"].to_numpy(float) > kp) & np.isfinite(X[f"PUAN_ESIT_{L}"].to_numpy(float))


# ================================================================ 4) GETİRİSİZ SAYIM + KESİMLER
def cs_kesim_getirisiz(XS: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Pazar x L: PUAN_ESIT ve F1..F6 için uç %90 / %98 ve beşlik sınırları; ATRP20 beşlik sınırları (kendi 2016-19 popülasyonu)."""
    K = CS_ESIK["kesim"]; out: Dict[str, Any] = {}
    for p, X in XS.items():
        for L in CS_L:
            m = cs_pop(X, L) & (X.hucre.to_numpy() == f"{p}|d1619")
            g = X[m]; r: Dict[str, Any] = {"n": int(m.sum())}
            a = g.ATRP20.to_numpy(float); r["ATRP20_besli"] = [float(np.quantile(a, q)) for q in K["besli"]]
            for c in ["PUAN_ESIT"] + CS_F:
                v = g[f"{c}_{L}"].to_numpy(float)
                r[c] = {"uc10": float(np.quantile(v, 1 - K["uc"][0])), "uc2": float(np.quantile(v, 1 - K["uc"][1])),
                        "besli": [float(np.quantile(v, q)) for q in K["besli"]]}
            out[f"{p}|{L}"] = r
    return out


def cs_sayim(XS: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Pazar x dönem x L: pencere sayısı, atılanlar (neden), farklı ay, en kalabalık 3 ay; altı ölçünün dağılımı; Spearman (getirisiz)."""
    kp = float(CS_ESIK["pencere"]["kilitli"]["pay"]); qs = [0.02, 0.10, 0.25, 0.50, 0.75, 0.90, 0.98]
    S: Dict[str, Any] = {"hucre": {}, "dag": {}, "spearman": {}, "hacim": {}}
    for p, X in XS.items():
        S["hacim"][p] = {"Volume_var": True}
        don = X.hucre.str.split("|").str[1].to_numpy()
        for dd in CS_DONEM:
            h = f"{p}|{dd}"; base = (don == dd) & X.uygun.to_numpy(bool)
            for L in CS_L:
                at: Dict[str, int] = {}
                m0 = base.copy(); at["aday"] = int(m0.sum())
                e = m0 & ~X.EVREN.to_numpy(bool); at["EVREN_DISI"] = int(e.sum()); m0 &= ~e
                e = m0 & ~X[f"ON_{L}"].to_numpy(bool); at["ONCEKI_YOK"] = int(e.sum()); m0 &= ~e
                e = m0 & (X[f"KIL_{L}"].to_numpy(float) > kp); at["KILITLI"] = int(e.sum()); m0 &= ~e
                e = m0 & ~np.isfinite(X[f"PUAN_ESIT_{L}"].to_numpy(float)); at["OLCU_YOK"] = int(e.sum()); m0 &= ~e
                pm = cs_pop(X, L) & (don == dd)
                if (pm != m0).any():
                    raise CSHata(f"K10: sayım popülasyonu cs_pop ile aynı değil ({h} L{L})")
                g = X[pm]; ao = HV.hv25_ay_ozet([f"{a}-01" for a in g.ay])
                S["hucre"][f"{h}|{L}"] = {"n": int(pm.sum()), "atilan": at, "ay": ao["ay"], "ust3_pay": ao["ust3_pay"], "hisse": int(g.sembol.nunique())}
                S["dag"][f"{h}|{L}"] = {c: [float(x) for x in np.quantile(g[f"{c}_{L}"].to_numpy(float), qs)] if len(g) else [] for c in ["PUAN_ESIT"] + CS_F}
                if len(g):
                    R = g[[f"{c}_{L}" for c in CS_F + ["PUAN_ESIT"]]].rank().corr(method="pearson").to_numpy()
                    S["spearman"][f"{h}|{L}"] = [[round(float(x), 3) for x in row] for row in R]
    S["kesim"] = cs_kesim_getirisiz(XS)
    return S


def cs_dagilim_bist(X: pd.DataFrame) -> Dict[int, Dict[str, np.ndarray]]:
    out = {}
    for L in CS_L:
        m = cs_dag_maske(X, L)
        out[L] = {c: np.sort(X.loc[m, f"{c}_{L}"].to_numpy(float)) for c in CS_F + ["PUAN_ESIT"]}
    return out


def cs_sayim_kos(ham: Optional[str] = None, kitaplik: bool = True) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    XS = {p: cs_yukle(p, ham) for p in CS_PAZAR}
    S = cs_sayim(XS)
    KT = None
    if kitaplik:
        dag = cs_dagilim_bist(XS["BIST"]); KT = cs_kitaplik(dag)
        KT["dagilim_n"] = {str(L): int(len(dag[L]["PUAN_ESIT"])) for L in CS_L}
    return S, KT


# ================================================================ 5) SONUÇ KAPISI (getiri yalnız buradan)
_CS_ASAMA_IZIN = {"kesif": {CS_KESIF}, "olcum": {f"{p}|{d}" for p in CS_PAZAR for d in CS_DONEM}, "test": {f"{p}|{d}" for p in CS_PAZAR for d in CS_DONEM}}


def cs_sonuc_dizi(dep: Dict[str, np.ndarray], j: np.ndarray, t: np.ndarray, atrp: np.ndarray) -> Dict[str, np.ndarray]:
    """Pencere sonları (hisse j, kendi bar t): SAG10, SOL10, R15, ATR2_YUK, ATR2_ASG, E0. t + 20 hissenin verisinde olmalı (uygunluk çağıranda)."""
    j = np.asarray(j, np.int64); t = np.asarray(t, np.int64); N = len(j); atrp = np.asarray(atrp, float)
    out = {a: np.full(N, np.nan) for a in ("E0", "SAG10", "SOL10", "R15", "ATR2_YUK", "ATR2_ASG")}
    if not N:
        return out
    g = dep["off"][j] + t; son = dep["off"][j + 1] - 1
    if (g + 20 > son).any():
        raise CSHata("K10: sonuç penceresi hissenin verisini aşıyor")
    W20 = g[:, None] + 1 + np.arange(20)[None, :]; W15 = W20[:, :15]
    C0 = dep["C"][g]; E0 = dep["O"][g + 1]
    out["E0"] = E0; out["R15"] = dep["C"][g + 15] / E0 - 1
    out["SAG10"] = (dep["H"][W20].max(1) >= C0 * 1.10).astype(float)
    out["SOL10"] = (dep["L"][W20].min(1) <= C0 * 0.90).astype(float)
    a = atrp[:, None]
    out["ATR2_YUK"] = YO.yo_ilk_dokunma(E0, dep["H"][W15], dep["L"][W15], 2.0 * a, 1.0 * a, "yukari")
    out["ATR2_ASG"] = YO.yo_ilk_dokunma(E0, dep["H"][W15], dep["L"][W15], 2.0 * a, 1.0 * a, "asagi")
    return out


def cs_sonuc(pazar: str, X: pd.DataFrame, asama: str, ham: Optional[str] = None, depo: Optional[Dict[str, np.ndarray]] = None) -> pd.DataFrame:
    """Sonuç sütunları YALNIZ izin verilen hücrelerin uygun satırları için (KEŞİF'te yalnız ABD|d1619; assert)."""
    if asama not in _CS_ASAMA_IZIN:
        raise CSHata(f"aşama: {asama}")
    hx = set(X.hucre.unique())
    if not hx <= _CS_ASAMA_IZIN[asama]:
        raise CSHata(f"SIRA: {asama} aşamasında izin dışı hücre sonucu istendi: {sorted(hx - _CS_ASAMA_IZIN[asama])}")
    if asama == "kesif" and (pazar != "ABD" or hx != {CS_KESIF}):
        raise CSHata("SIRA: KEŞİF yalnız ABD 2016-19 satırlarıyla")
    if not X.uygun.all():
        raise CSHata("K10: sonuç yalnız uygun pencere sonları için")
    if depo is None:
        z = np.load(_cs_ham(f"depo_{pazar}.npz", ham)); depo = {k: z[k] for k in z.files}
    dep = {k: depo[k] for k in ("O", "H", "L", "C", "POS", "off")}
    R = cs_sonuc_dizi(dep, X.j.to_numpy(np.int64), X.t.to_numpy(np.int64), X.ATRP20.to_numpy(float))
    P15, _ = YO.yo_P15(depo["Op"], depo["Cl"], depo["P2"])
    Sx = pd.DataFrame(R, index=X.index); Sx["P15"] = P15[X.d_row.to_numpy(np.int64)]; Sx["SECIM"] = Sx.R15 - Sx.P15
    return Sx


# ================================================================ 6) İSTATİSTİK (YO.yo_olc mantığı; tohum 2713)
def cs_ay_W(ay: np.ndarray, anahtar: str, B: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    B = int(B or CS_ESIK["boot"]["B"]); u, k = np.unique(np.asarray(ay, str), return_inverse=True); K = len(u)
    W = _cs_rng(anahtar).multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)
    return k, W


def _q(v: np.ndarray) -> Tuple[Optional[float], Optional[float]]:
    v = v[np.isfinite(v)]
    if not len(v):
        return None, None
    return float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))


def cs_olc(uc: np.ndarray, q: np.ndarray, Y: np.ndarray, D: np.ndarray, TF: np.ndarray, ay: np.ndarray, anahtar: str,
           B: Optional[int] = None, ek: Optional[Dict[str, np.ndarray]] = None, nq: int = 5) -> Dict[str, Any]:
    """Bir satır x hücre: ham KAT, ATRP beşliği içi KAT, ASİMETRİ, TOPLAM FARK (YO.yo_olc ile aynı hesap); ay kümeli bootstrap (tohum 2713)."""
    uc = np.asarray(uc, bool); q = np.asarray(q, np.int64); Y = np.asarray(Y, float); D = np.asarray(D, float); TF = np.asarray(TF, float)
    ay = np.asarray(ay, str); nu = int(uc.sum()); N = len(uc)
    out: Dict[str, Any] = {"n": nu, "N": int(N)}
    ao = HV.hv25_ay_ozet([f"{a}-01" for a in ay[uc]]) if nu else {"ay": 0, "ust3_pay": None, "ust3": []}
    out.update({"ay": ao["ay"], "ust3_pay": ao["ust3_pay"]})
    if nu < 2 or N < 10:
        return out
    pq = np.array([Y[q == i].mean() if (q == i).any() else np.nan for i in range(nq)]); dq = np.array([D[q == i].mean() if (q == i).any() else np.nan for i in range(nq)])
    nuq = np.array([(uc & (q == i)).sum() for i in range(nq)], float)
    E = float(np.nansum(nuq * pq)); O = float(Y[uc].sum())
    out["P_uc"] = O / nu; out["P_taban"] = float(Y.mean()); out["P_beklenen"] = E / nu; out["D_uc"] = float(D[uc].mean()); out["D_taban"] = float(D.mean())
    out["KAT_HAM"] = (O / nu) / out["P_taban"] if out["P_taban"] > 0 else None
    out["KAT"] = O / E if E > 0 else None
    out["ASIMETRI"] = (O - D[uc].sum()) / nu - float(np.nansum(nuq * (pq - dq))) / nu
    tfu = TF[uc]; out["TOPLAM_FARK"] = float(np.nanmean(tfu)) if np.isfinite(tfu).any() else None
    k, W = cs_ay_W(ay, anahtar, B); K = W.shape[1]
    bc = lambda v: np.bincount(k, weights=v, minlength=K)  # noqa: E731
    TFz = np.where(np.isfinite(TF), TF, 0.0); TFn = np.isfinite(TF)
    Nq = np.stack([bc((q == i).astype(float)) for i in range(nq)], 1); Yq = np.stack([bc(Y * (q == i)) for i in range(nq)], 1)
    Dq = np.stack([bc(D * (q == i)) for i in range(nq)], 1); NUq = np.stack([bc((uc & (q == i)).astype(float)) for i in range(nq)], 1)
    YU = bc(Y * uc); DU = bc(D * uc); TFU = bc(np.where(uc, TFz, 0.0)); NTF = bc((uc & TFn).astype(float)); NU = bc(uc.astype(float))
    YA = bc(Y); NA = bc(np.ones(N))
    with np.errstate(invalid="ignore", divide="ignore"):
        wN = W @ Nq; pq_ = (W @ Yq) / wN; dq_ = (W @ Dq) / wN; wNU = W @ NUq
        E_ = np.nansum(wNU * pq_, axis=1); O_ = W @ YU; nu_ = W @ NU
        kat = O_ / E_; kh = (O_ / nu_) / ((W @ YA) / (W @ NA))
        asm = (O_ - W @ DU) / nu_ - np.nansum(wNU * (pq_ - dq_), axis=1) / nu_
        tf = (W @ TFU) / (W @ NTF)
    for ad, v in (("KAT", kat), ("KAT_HAM", kh), ("ASIMETRI", asm), ("TOPLAM_FARK", tf)):
        a, b = _q(v); out[f"{ad}_alt"] = a; out[f"{ad}_ust"] = b
    kv = kat[np.isfinite(kat)]
    out["p"] = float((1 + (kv <= 1).sum()) / (len(kv) + 1)) if len(kv) else None
    if ek:
        for ad, v in ek.items():
            v = np.asarray(v, float); f = uc & np.isfinite(v); fa = np.isfinite(v)
            out[ad] = float(v[f].mean()) if f.any() else None
            out[f"{ad}_taban"] = float(v[fa].mean()) if fa.any() else None
    return out


def cs_hukum(o: Dict[str, Dict[str, Any]], bh_gecti: bool) -> str:
    """Satır hükmü (CS_ESIK['hukum']); o: hücre -> ölçü."""
    Hk = CS_ESIK["hukum"]; a = o.get("ABD|d1619", {}); b = o.get("ABD|d2022", {})
    for x in (a, b):
        if x.get("n", 0) < Hk["n_min"] or x.get("ay", 0) < Hk["ay_min"] or x.get("KAT") is None:
            return "ÖLÇÜLEMEDİ"
    gt = lambda v, e: v is not None and v > e  # noqa: E731
    uc3 = lambda x: gt(x.get("KAT"), 1) and gt(x.get("KAT_alt"), 1) and gt(x.get("ASIMETRI"), 0) and gt(x.get("ASIMETRI_alt"), 0) and \
        gt(x.get("TOPLAM_FARK"), 0) and gt(x.get("TOPLAM_FARK_alt"), 0)  # noqa: E731
    avr = all(o.get(h, {}).get("n", 0) >= 30 and gt(o[h].get("KAT"), 1) and gt(o[h].get("ASIMETRI"), 0) and gt(o[h].get("TOPLAM_FARK"), 0)
              for h in ("AVR|d1619", "AVR|d2022"))
    if uc3(a) and uc3(b) and bh_gecti and avr:
        return "TUTAR"
    if gt(a.get("KAT_HAM_alt"), 1) and gt(b.get("KAT_HAM_alt"), 1) and \
            any((not gt(x.get("KAT_alt"), 1)) or (not gt(x.get("ASIMETRI"), 0)) for x in (a, b)):
        return "YALNIZ OYNAKLIK"
    if uc3(a) != uc3(b):
        return "TEK DÖNEM"
    if b.get("KAT_ust") is not None and b["KAT_ust"] < 1 and b.get("ASIMETRI_ust") is not None and b["ASIMETRI_ust"] < 0:
        return "TERS"
    return "TUTMADI"


def cs_spearman5(y: List[Optional[float]]) -> Optional[float]:
    v = np.array([np.nan if x is None else x for x in y], float)
    if not np.isfinite(v).all():
        return None
    return float(pd.Series(np.arange(5)).corr(pd.Series(v), method="spearman"))


# ================================================================ 7) KAPILAR
def cs_kapi(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    """Ön kayıt kapısı: kontrol listesi + mühürler + commit + temiz ağaç + panel sha + sayım sha + KASA."""
    import IZ_KARNE as IK
    import KASA as KS
    cikti = cikti or CS_YOL["cikti"]; yol = _cs_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise CSHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read()
    bek = {"CS_KOD_SHA": cs_kod_sha(), "CS_ESIK_SHA": cs_esik_sha(), **{f"DOSYA_{a}": v for a, v in cs_dosya_sha(ham).items()}}
    for a, v in bek.items():
        if f"{a}: {v}" not in metin:
            raise CSHata(f"ön kayıt kapısı: {a} farklı -> DURDU")
    S, _ = cs_sayim_kos(ham, kitaplik=False)
    if f"SAYIM_SHA: {HV.hv_json_sha(S)}" not in metin:
        raise CSHata("getirisiz sayım ön kayıttakiyle aynı değil -> DURDU")
    rel = os.path.relpath(yol, KOK_CS); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise CSHata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "COL_SKOR6.py"]):
        raise CSHata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    try:
        kasa = KS.kasa_kapisi([os.path.join(CS_YOL["acik"], f"V_{p}.pkl") for p in CS_PAZAR], "2022-12-31")
    except KS.KasaHata as ex:
        raise CSHata(f"KASA kapısı KAPALI: {ex}") from ex
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, "kasa": kasa, "sayim": S, **bek}


def cs_kesim_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or CS_YOL["cikti"]; yj = _cs_yol("kesim", cikti); ym = _cs_yol("kesim_md", cikti)
    if not (os.path.exists(yj) and os.path.exists(ym)):
        raise CSHata("SIRA: cs_kesim.json / CS_KESIM.md yok (KEŞİF önce)")
    sha = MI._mi_sha(yj)
    if f"KESIM_SHA: {sha}" not in open(ym, encoding="utf-8").read():
        raise CSHata("CS_KESIM.md kesim sha'sı uyuşmuyor -> DURDU")
    out = {"KESIM_SHA": sha}
    for f in (yj, ym):
        rel = os.path.relpath(f, KOK_CS); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
        if not c:
            raise CSHata(f"SIRA: {os.path.basename(f)} commit'li değil -> DURDU")
        if MI._mi_git(["status", "--porcelain", "--", rel]):
            raise CSHata(f"{os.path.basename(f)} çalışma ağacında değişmiş -> DURDU")
        out[os.path.basename(f)] = c
    return out


# ================================================================ 8) KEŞİF (yalnız ABD 2016-19; PUAN_OGR ağırlıkları)
def cs_kesif_hesap(X: pd.DataFrame, Sx: pd.DataFrame, XS: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """X / Sx yalnız ABD|d1619 uygun satırlar; XS = bütün pazar panelleri (getirisiz; yalnız PUAN_OGR dağılımı / kesimi için)."""
    if set(X.hucre.unique()) != {CS_KESIF}:
        raise CSHata("SIRA: ağırlıklar yalnız ABD 2016-19'dan")
    K: Dict[str, Any] = {"agirlik": {}, "PUAN_OGR": {}}
    Q = CS_ESIK["kesim"]
    for L in CS_L:
        m = cs_pop(X, L); F = {a: X.loc[m, f"{a}_{L}"].to_numpy(float) for a in CS_F}
        w = cs_agirlik(F, Sx.loc[m, "SAG10"].to_numpy(float)); K["agirlik"][str(L)] = w
        K["agirlik"][f"{L}_n"] = int(m.sum()); K["agirlik"][f"{L}_SAG10_pay"] = float(Sx.loc[m, "SAG10"].mean())
        for p, Xp in XS.items():
            mp = cs_pop(Xp, L) & (Xp.hucre.to_numpy() == f"{p}|d1619")
            v = cs_puan_ogr({a: Xp.loc[mp, f"{a}_{L}"].to_numpy(float) for a in CS_F}, w)
            K["PUAN_OGR"][f"{p}|{L}"] = {"uc10": float(np.quantile(v, 1 - Q["uc"][0])), "uc2": float(np.quantile(v, 1 - Q["uc"][1])),
                                         "besli": [float(np.quantile(v, q)) for q in Q["besli"]], "n": int(mp.sum())}
    return K


def cs_kesif(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or CS_YOL["cikti"]
    if os.path.exists(_cs_yol("kesim", cikti)):
        raise CSHata("cs_kesim.json zaten var (ikinci KEŞİF DURUR)")
    G = cs_kapi(cikti, ham)
    XS = {p: cs_yukle(p, ham) for p in CS_PAZAR}
    X = XS["ABD"]; X = X[(X.hucre.to_numpy() == CS_KESIF) & X.uygun.to_numpy(bool) & X.EVREN.to_numpy(bool)]
    Sx = cs_sonuc("ABD", X, "kesif", ham)
    K = cs_kesif_hesap(X, Sx, XS)
    K.update({"surum": CS_SURUM, "zaman": pd.Timestamp.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "onkayit_commit": G["onkayit_commit"],
              "CS_KOD_SHA": G["CS_KOD_SHA"], "CS_ESIK_SHA": G["CS_ESIK_SHA"], "getirisiz": G["sayim"]["kesim"]})
    yj = MI._mi_jyaz(_cs_yol("kesim", cikti), K, "kesim")
    MI._mi_yaz(_cs_yol("kesim_md", cikti), cs_kesim_md(K, MI._mi_sha(yj)), "kesim md")
    return K


def cs_kesim_md(K: Dict[str, Any], sha: str) -> str:
    L = [f"# CS KESİM — PUAN_OGR ağırlıkları (YALNIZ ABD 2016-19, eski etiket SAG10) ({K['zaman']})", "",
         f"KESIM_SHA: {sha}", f"ön kayıt commit: {K['onkayit_commit']}", f"CS_KOD_SHA: {K['CS_KOD_SHA']}", f"CS_ESIK_SHA: {K['CS_ESIK_SHA']}", "",
         "Bu dosya ölçümden (ABD 2020-22, AVR, BIST sonuçları) ÖNCE commit + push edilir. KEŞİF'te yalnız ABD 2016-19 SAG10 hesaplandı; başka hücre "
         "sonucu görülmedi. Ağırlıklar ABD 2016-19'da öğrenildiği için PUAN_OGR o hücrede örneklem içidir.", "",
         "| L | n | SAG10 payı | " + " | ".join(f"w {a} ({CS_F_AD[a]})" for a in CS_F) + " |", "|---|---|---|" + "---|" * len(CS_F)]
    for Lx in CS_L:
        w = K["agirlik"][str(Lx)]
        L.append(f"| {Lx} | {K['agirlik'][f'{Lx}_n']} | {_f(K['agirlik'][f'{Lx}_SAG10_pay'], 1, True)} | " + " | ".join(_f(w[a], 3) for a in CS_F) + " |")
    L += ["", "## PUAN_OGR kesimleri (pazarın kendi 2016-19 dağılımı; getirisiz)", "", "| pazar\\|L | n | %90 | %98 | beşlik sınırları |", "|---|---|---|---|---|"]
    for k, v in K["PUAN_OGR"].items():
        L.append(f"| {k} | {v['n']} | {_f(v['uc10'], 2)} | {_f(v['uc2'], 2)} | " + " / ".join(_f(x, 2) for x in v["besli"]) + " |")
    return "\n".join(L) + "\n"


# ================================================================ 9) ÖLÇÜM (bir kez)
def cs_kesim_al(K: Dict[str, Any], pazar: str, L: int, kol: str) -> Dict[str, Any]:
    if kol == "PUAN_OGR":
        return K["PUAN_OGR"][f"{pazar}|{L}"]
    return K["getirisiz"][f"{pazar}|{L}"][kol]


def cs_olcum_hesap(XS: Dict[str, pd.DataFrame], SS: Dict[str, pd.DataFrame], K: Dict[str, Any], B: Optional[int] = None) -> Dict[str, Any]:
    """XS[p] = uygun + evren satırlar, SS[p] = sonuçları (aynı index). Hücre x L x kol x (uç10, uç2, beşlik 1..5) ölçüleri; hüküm; doz - yanıt."""
    R: Dict[str, Any] = {"satir": {}, "taban": {}, "besli": {}}
    for p in CS_PAZAR:
        if p not in XS:
            continue
        X = XS[p]; S = SS[p]
        T1 = S.R15.groupby([X.hucre, X.sembol]).transform("mean"); TF = (S.R15 - T1).to_numpy(float)
        for L in CS_L:
            w = {a: float(K["agirlik"][str(L)][a]) for a in CS_F}
            PO = cs_puan_ogr({a: X[f"{a}_{L}"].to_numpy(float) for a in CS_F}, w)
            pop = cs_pop(X, L); gk = K["getirisiz"][f"{p}|{L}"]
            for dd in CS_DONEM:
                h = f"{p}|{dd}"; m = pop & (X.hucre.to_numpy() == h)
                if not m.any():
                    continue
                q = YO.yo_besli(X.ATRP20.to_numpy(float)[m], gk["ATRP20_besli"])
                Y = S.SAG10.to_numpy(float)[m]; D = S.SOL10.to_numpy(float)[m]; tf = TF[m]; ay = X.ay.to_numpy()[m]
                ek = {"R15": S.R15.to_numpy(float)[m], "SECIM": S.SECIM.to_numpy(float)[m], "ATR2_YUK": S.ATR2_YUK.to_numpy(float)[m],
                      "ATR2_ASG": S.ATR2_ASG.to_numpy(float)[m]}
                R["taban"][f"{h}|{L}"] = {"n": int(m.sum()), "SAG10": float(Y.mean()), "SOL10": float(D.mean()),
                                          "SAG10_besli": [float(Y[q == i].mean()) if (q == i).any() else None for i in range(5)],
                                          **{a: float(np.nanmean(v)) for a, v in ek.items()}}
                for kol in CS_KOL:
                    x = PO[m] if kol == "PUAN_OGR" else X[f"{kol}_{L}"].to_numpy(float)[m]; kk = cs_kesim_al(K, p, L, kol)
                    for uc in ("uc10", "uc2"):
                        R["satir"].setdefault(f"{kol}|{uc}|{L}", {})[h] = cs_olc(x >= kk[uc], q, Y, D, tf, ay, f"{kol}|{uc}|{L}|{h}", B, ek)
                    bq = YO.yo_besli(x, kk["besli"])
                    R["besli"].setdefault(f"{kol}|{L}", {})[h] = [cs_olc(bq == i, q, Y, D, tf, ay, f"{kol}|b{i + 1}|{L}|{h}", B) for i in range(5)]
        gc.collect()
    # BH + hüküm
    ad = list(R["satir"]); pp = [R["satir"][a].get("ABD|d2022", {}).get("p") for a in ad]
    qb = YO.yo_bh(pp, float(CS_ESIK["bh"]["q"]))
    R["hukum"] = {}; R["bh_q"] = {}
    for a, qv in zip(ad, qb):
        R["bh_q"][a] = qv
        R["hukum"][a] = cs_hukum(R["satir"][a], qv is not None and qv <= float(CS_ESIK["bh"]["q"]))
    R["doz"] = {}
    for a, hh in R["besli"].items():
        dz = {h: {"KAT": [x.get("KAT") for x in v], "rho": cs_spearman5([x.get("KAT") for x in v]), "ust_alt": v[4].get("KAT_alt")} for h, v in hh.items()}
        var = all(dz.get(h, {}).get("rho") is not None and dz[h]["rho"] >= 0.9 and dz[h]["ust_alt"] is not None and dz[h]["ust_alt"] > 1
                  for h in ("ABD|d1619", "ABD|d2022"))
        R["doz"][a] = {"hucre": dz, "VAR": bool(var)}
    say = {}
    for v in R["hukum"].values():
        say[v] = say.get(v, 0) + 1
    R["hukum_say"] = say
    R["genel"] = ("AÇIK VERİDE ADAY (KASA KURALI: tek iz kasa açmaz; ileri test)" if say.get("TUTAR", 0)
                  else "ESKİ ÇÖL PUANI ÖRNEKLEM DIŞINDA AYIRT EDİCİ DEĞİL (bu tanımlarla)")
    return R


def cs_olcum(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or CS_YOL["cikti"]
    if os.path.exists(_cs_yol("sonuc", cikti)):
        raise CSHata("sonuç zaten var (ikinci ölçüm DURUR)")
    G = cs_kapi(cikti, ham); KK = cs_kesim_kapi(cikti)
    K = json.load(open(_cs_yol("kesim", cikti), encoding="utf-8"))
    if K["getirisiz"] != G["sayim"]["kesim"]:
        raise CSHata("K10: kesim json'undaki getirisiz kesimler sayımla aynı değil")
    XS, SS = {}, {}
    for p in CS_PAZAR:
        X = cs_yukle(p, ham); don = X.hucre.str.split("|").str[1]
        X = X[X.uygun.to_numpy(bool) & X.EVREN.to_numpy(bool) & don.isin(CS_DONEM).to_numpy(bool)]
        S = cs_sonuc(p, X, "olcum", ham)
        with open(_cs_ham(f"sonuc_{p}.pkl", ham), "wb") as f:
            pickle.dump(S, f, protocol=4)
        XS[p], SS[p] = X, S; gc.collect()
    R = cs_olcum_hesap(XS, SS, K)
    J = {"surum": CS_SURUM, "zaman": pd.Timestamp.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "kapi": {k: v for k, v in G.items() if k != "sayim"},
         "kesim_kapi": KK, "agirlik": K["agirlik"], **R,
         "sonuc_sha": {p: MI._mi_sha(_cs_ham(f"sonuc_{p}.pkl", ham)) for p in CS_PAZAR}}
    MI._mi_jyaz(_cs_yol("sonuc", cikti), J, "sonuç")
    cs_ozet_csv(J, _cs_yol("ozet", cikti))
    return J


def cs_ozet_csv(J: Dict[str, Any], yol: str) -> str:
    rows = []
    for a, hh in J["satir"].items():
        kol, uc, L = a.split("|")
        for h, o in hh.items():
            rows.append({"kol": kol, "uc": uc, "L": int(L), "hucre": h, "hukum": J["hukum"][a], "bh_q": J["bh_q"].get(a),
                         **{k: o.get(k) for k in ("n", "ay", "ust3_pay", "P_uc", "P_taban", "P_beklenen", "D_uc", "D_taban", "KAT_HAM", "KAT_HAM_alt",
                                                  "KAT_HAM_ust", "KAT", "KAT_alt", "KAT_ust", "ASIMETRI", "ASIMETRI_alt", "ASIMETRI_ust", "TOPLAM_FARK",
                                                  "TOPLAM_FARK_alt", "TOPLAM_FARK_ust", "p", "R15", "SECIM", "ATR2_YUK", "ATR2_YUK_taban", "ATR2_ASG",
                                                  "ATR2_ASG_taban")}})
    df = pd.DataFrame(rows); MI.mi_sizinti(df.to_csv(index=False), "özet csv")
    df.to_csv(yol, index=False)
    return yol


# ================================================================ 10) ÖN KAYIT + RAPOR
def _f(x: Any, n: int = 2, yuzde: bool = False) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    v = float(x) * (100 if yuzde else 1)
    return f"{v:.{n}f}".replace(".", ",")


def _kitaplik_tablo(KT: Dict[str, Any]) -> List[str]:
    L = ["| # | sembol | bölge | bar | L* | " + " | ".join(CS_F) + " | PUAN_ESIT | yüzdelik sıra (PUAN) | sıra F1..F6 | kilitli payı |",
         "|---|---|---|---|---|" + "---|" * len(CS_F) + "---|---|---|---|"]
    for i, r in enumerate(KT["satir"]):
        if r["durum"] != "tamam":
            L.append(f"| {i + 1} | {r['sembol']} | {r['bas']} .. {r['bit']} | {r.get('bar', 0)} | - | " + " | ".join("-" for _ in CS_F) +
                     f" | veri yok | {r.get('neden', '')} | - | - |")
            continue
        L.append(f"| {i + 1} | {r['sembol']} | {r['bas']} .. {r['bit']} | {r['bar']} | {r['L']} | " + " | ".join(_f(r[a], 2) for a in CS_F) +
                 f" | {_f(r['PUAN_ESIT'], 1)} | {_f(r['PUAN_ESIT_sira'], 0, True)} | " + " / ".join(_f(r[f'{a}_sira'], 0, True) for a in CS_F) +
                 f" | {_f(r['kilitli_pay'], 0, True)} |")
    oz = KT["ozet"]
    L += ["", f"Veri olan bölge: {oz['veri_var']} / {oz['bolge']}. Karşılaştırma dağılımı (BIST 2016-22, evren süzgeçsiz) pencere sayısı L=20/40/80: "
          + " / ".join(str(KT.get("dagilim_n", {}).get(str(Lx), "-")) for Lx in CS_L), "",
          "| ölçü | üst %10 | üst %30 | medyan altı | kitaplık yüzdelik sıralarının medyanı |", "|---|---|---|---|---|"]
    for a in ["PUAN_ESIT"] + CS_F:
        o = oz[a]; L.append(f"| {a} {CS_F_AD.get(a, '')} | {o['ust10']} | {o['ust30']} | {o['medyan_alti']} | {_f(o['sira_medyan'], 0, True)} |")
    return L


def cs_onkayit_yaz(cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or CS_YOL["cikti"]; S, KT = cs_sayim_kos(ham); ds = cs_dosya_sha(ham)
    MI._mi_jyaz(_cs_ham("sayim.json", ham), S, "sayım"); MI._mi_jyaz(_cs_ham("kitaplik.json", ham), KT, "kitaplık")
    L = [f"# CS ÖN KAYIT — eski çöl puanı (altı ölçü) örneklem dışında + kitaplık tespiti ({pd.Timestamp.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')})",
         "", "İş tanımı CS_IS_TANIMI.md (ana model). Bu dosya SAG10 / SOL10 / R15 / P15 HİÇBİR hücrede hesaplanmadan ÖNCE commit + push edilir; tanımlar, "
         "eşikler, okuma ve hüküm kuralları sonra değişmez (değişirse SAPMA). Evren bugün yaşayan hisseler (yukarı yanlı). KASA açılmaz (ölçüm verisi "
         "<= 2022-12-31); tek istisna kitaplık PUANI (BIST 2024-26, bölge bitişine kadar; sonrası okunmaz).", "", "## Mühürler", "",
         f"CS_KOD_SHA: {cs_kod_sha()}", f"CS_ESIK_SHA: {cs_esik_sha()}"]
    L += [f"DOSYA_{a}: {v}" for a, v in ds.items()]
    L += [f"SAYIM_SHA: {HV.hv_json_sha(S)}", f"KITAPLIK_SHA: {HV.hv_json_sha(KT)}", f"IS_TANIMI_SHA: {MI._mi_sha(CS_YOL['is_tanimi'])}", "",
          f"- Panel dosyaları (repo dışı): {CS_YOL['ham']} (pencere_*.pkl = pencere sonları + altı ölçü, getirisiz; depo_*.npz = sonuç için bar deposu; "
          "sonuç sütunu YOK)", "- Hacim sütunu (Volume) üç pazarın panelinde var (hazırlıkta her pazarda denetlendi; F6 bundan).", "",
          "## KİTAPLIK TESPİTİ (yalnız puan; sonrası YOK)", ""]
    L += _kitaplik_tablo(KT)
    L += ["", "## GETİRİSİZ SAYIM (SAG10 / R15 hesaplanmadı)", "",
          "| hücre | L | pencere (popülasyon) | aday | evren dışı | önceki yok | kilitli | ölçü yok | farklı ay | en kalabalık 3 ay | hisse |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for p in CS_PAZAR:
        for dd in CS_DONEM:
            for Lx in CS_L:
                a = S["hucre"].get(f"{p}|{dd}|{Lx}", {}); at = a.get("atilan", {})
                L.append(f"| {p}|{dd} | {Lx} | {a.get('n', 0)} | {at.get('aday', 0)} | {at.get('EVREN_DISI', 0)} | {at.get('ONCEKI_YOK', 0)} | "
                         f"{at.get('KILITLI', 0)} | {at.get('OLCU_YOK', 0)} | {a.get('ay', 0)} | {_f(a.get('ust3_pay'), 3)} | {a.get('hisse', 0)} |")
    L += ["", "### Altı ölçünün dağılımı (ABD 2016-19; %2 / %10 / %25 / %50 / %75 / %90 / %98)", "",
          "| ölçü | L | " + " | ".join(["%2", "%10", "%25", "%50", "%75", "%90", "%98"]) + " |", "|---|---|" + "---|" * 7]
    for c in ["PUAN_ESIT"] + CS_F:
        for Lx in CS_L:
            q = S["dag"].get(f"ABD|d1619|{Lx}", {}).get(c, [])
            L.append(f"| {c} | {Lx} | " + " | ".join(_f(v, 3) for v in q) + " |")
    L += ["", "### Getirisiz kesimler (pazarın kendi 2016-19 popülasyonu; %90 / %98; ATRP20 beşlik sınırları)", "",
          "| pazar\\|L | n | ATRP20 beşlik | " + " | ".join(["PUAN_ESIT"] + CS_F) + " |", "|---|---|---|" + "---|" * 7]
    for k, v in S["kesim"].items():
        L.append(f"| {k} | {v['n']} | " + " / ".join(_f(x, 4) for x in v["ATRP20_besli"]) + " | " +
                 " | ".join(f"{_f(v[c]['uc10'], 3)} / {_f(v[c]['uc2'], 3)}" for c in ["PUAN_ESIT"] + CS_F) + " |")
    L += ["", "### Altı ölçü arası sıra ilişkisi (Spearman; ABD 2016-19, L = 40)", "", "| | " + " | ".join(CS_F + ["PUAN"]) + " |", "|---|" + "---|" * 7]
    M = S["spearman"].get("ABD|d1619|40", [])
    for i, c in enumerate(CS_F + ["PUAN"]):
        L.append(f"| {c} | " + " | ".join(_f(M[i][jx], 2) if M else "-" for jx in range(7)) + " |")
    L += ["", "## Yorum gerektiren noktalar (ölçümden ÖNCE sabit)", ""]
    L += [f"{i + 1}. {t}" for i, t in enumerate(CS_YORUM)]
    L += ["", "## Tanımlar (CS_ESIK; sha yukarıda)", "", "```", json.dumps(CS_ESIK, ensure_ascii=False, indent=1), "```", "", "## KONTROL LİSTESİ", "",
          "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    ad = {k["kod"]: k.get("ad", k.get("baslik", "")) for k in IK.IK_KONTROL}
    for k, (y, kn) in CS_KONTROL.items():
        L.append(f"| {k} | {ad.get(k, '')} | {y} | {kn} |")
    L += ["", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(_cs_yol("onkayit", cikti), "\n".join(L), "ön kayıt")


def _ar(o: Dict[str, Any], ad: str, n: int = 2, yuzde: bool = False) -> str:
    return f"{_f(o.get(ad), n, yuzde)} [{_f(o.get(f'{ad}_alt'), n, yuzde)}; {_f(o.get(f'{ad}_ust'), n, yuzde)}]"


def _avr_isaret(r: Dict[str, Any]) -> str:
    s = []
    for h in ("AVR|d1619", "AVR|d2022"):
        o = r.get(h, {})
        if o.get("n", 0) < 30 or o.get("KAT") is None:
            s.append("n<30"); continue
        s.append("".join("+" if (v is not None and v > e) else "-" for v, e in ((o.get("KAT"), 1), (o.get("ASIMETRI"), 0), (o.get("TOPLAM_FARK"), 0))))
    return " / ".join(s)


def cs_rapor_yaz(cikti: Optional[str] = None, ham: Optional[str] = None, yeniden: Optional[List[str]] = None, hata: Optional[List[str]] = None,
                 sapma: Optional[List[str]] = None) -> str:
    cikti = cikti or CS_YOL["cikti"]; J = json.load(open(_cs_yol("sonuc", cikti), encoding="utf-8"))
    KT = json.load(open(_cs_ham("kitaplik.json", ham), encoding="utf-8"))
    L = [f"# CS RAPOR — eski çöl puanı (altı ölçü) örneklem dışında ({J['zaman']})", "",
         f"Ön kayıt commit: {J['kapi']['onkayit_commit']}; kesim: {J['kesim_kapi'].get('cs_kesim.json')}. Evren bugün yaşayan hisseler (yukarı yanlı). "
         "KAT = ATRP20 beşliği içinde; ham KAT oynaklığı içerir. PUAN_OGR ağırlıkları ABD 2016-19'da öğrenildi (o hücrede örneklem içi).", "",
         "## SONUÇ", "", f"- GENEL: {J['genel']}",
         "- Hüküm sayıları (48 satır): " + "; ".join(f"{k} {v}" for k, v in sorted(J["hukum_say"].items())), "",
         "## KİTAPLIK TESPİTİ (Cemal'in 20 çölü; yalnız puan)", ""]
    L += _kitaplik_tablo(KT)
    L += ["", "## OLASILIK TABLOSU (ABD karar; AVR işaret: KAT-1 / ASİMETRİ / TOPLAM FARK, 2016-19 / 2020-22)", "",
          "| satır | hücre | n | ay | SAG10 uç | taban | ham KAT | KAT (ATRP içi) | ASİMETRİ (puan) | TOPLAM FARK (puan) | +2ATR uç / taban | AVR | BH q | hüküm |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a, hh in J["satir"].items():
        for h in ("ABD|d1619", "ABD|d2022", "BIST|d1619", "BIST|d2022"):
            o = hh.get(h, {})
            L.append(f"| {a} | {h} | {o.get('n', 0)} | {o.get('ay', 0)} | {_f(o.get('P_uc'), 1, True)} | {_f(o.get('P_taban'), 1, True)} | "
                     f"{_ar(o, 'KAT_HAM')} | {_ar(o, 'KAT')} | {_ar(o, 'ASIMETRI', 1, True)} | {_ar(o, 'TOPLAM_FARK', 2, True)} | "
                     f"{_f(o.get('ATR2_YUK'), 1, True)} / {_f(o.get('ATR2_YUK_taban'), 1, True)} | {_avr_isaret(hh) if h.startswith('ABD') else 'bilgi'} | "
                     f"{_f(J['bh_q'].get(a), 3)} | {J['hukum'][a] if h.startswith('ABD') else 'bilgi'} |")
    L += ["", "## DOZ - YANIT (beşliklerde ATRP içi KAT; Q1..Q5)", "", "| satır | ABD 2016-19 | ABD 2020-22 | AVR 2016-19 | AVR 2020-22 | VAR |", "|---|---|---|---|---|---|"]
    for a, d in J["doz"].items():
        L.append(f"| {a} | " + " | ".join(" / ".join(_f(x, 2) for x in d["hucre"].get(h, {}).get("KAT", [])) + f" (rho {_f(d['hucre'].get(h, {}).get('rho'), 2)})"
                                          for h in ("ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022")) + f" | {'VAR' if d['VAR'] else 'yok'} |")
    L += ["", "## Taban (hücre x L)", "", "| hücre\\|L | n | SAG10 | SOL10 | SAG10 ATRP beşlikleri | R15 | +2ATR | -2ATR |", "|---|---|---|---|---|---|---|---|"]
    for k, v in J["taban"].items():
        L.append(f"| {k} | {v['n']} | {_f(v['SAG10'], 1, True)} | {_f(v['SOL10'], 1, True)} | " + " / ".join(_f(x, 1, True) for x in v["SAG10_besli"]) +
                 f" | {_f(v['R15'], 2, True)} | {_f(v['ATR2_YUK'], 1, True)} | {_f(v['ATR2_ASG'], 1, True)} |")
    L += ["", "## Ağırlıklar (PUAN_OGR; ABD 2016-19)", "", "| L | " + " | ".join(CS_F) + " |", "|---|" + "---|" * 6]
    for Lx in CS_L:
        L.append(f"| {Lx} | " + " | ".join(_f(J["agirlik"][str(Lx)][a], 3) for a in CS_F) + " |")
    L += ["", "## YENİDEN ÜRETİM", ""] + [f"- {x}" for x in (yeniden or ["(yok)"])]
    L += ["", "## KONTROL LİSTESİ", "", "Ön kayıttaki tablo (CS_ON_KAYIT.md) geçerli; kapı geçti: " + str(J["kapi"]["kontrol"]["gecti"]), "",
          "## HATA", ""] + [f"- {x}" for x in (hata or ["(yok)"])]
    L += ["", "## SAPMA", ""] + [f"- {x}" for x in (sapma or ["(yok)"])]
    L += ["", "## ÖNERİLEN DEFTER SATIRLARI", "",
          f"- Ç (COL_SKOR6, 27 Kas): eski çöl puanı (GEN10_COL_OGREN v5, altı ölçü) örneklem dışında. KİTAPLIK: {KT['ozet']['veri_var']}/20 bölgede veri; "
          f"PUAN_ESIT üst %10'da {KT['ozet']['PUAN_ESIT']['ust10']}, üst %30'da {KT['ozet']['PUAN_ESIT']['ust30']}, medyan altında "
          f"{KT['ozet']['PUAN_ESIT']['medyan_alti']}. Ölçüm hükmü: {J['genel']}; " + "; ".join(f"{k} {v}" for k, v in sorted(J["hukum_say"].items())) + ".",
          "- IK_ILERI: TUTAR / TEK DÖNEM satırları 2023-24 verisiyle aynı komut, aynı kesimle (kasa açılışı ancak KASA KURALI şartlarıyla).", ""]
    return MI._mi_yaz(_cs_yol("rapor", cikti), "\n".join(L), "rapor")


def cs_sha_simdi(ham: Optional[str] = None) -> Dict[str, str]:
    return {"CS_KOD_SHA": cs_kod_sha(), "CS_ESIK_SHA": cs_esik_sha()}


def _cakisma_kontrol_cs(_once=_CK_ONCE_CS, _dosya="COL_SKOR6.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_CS",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_cs()


def _cs_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="COL_SKOR6")
    ap.add_argument("komut", choices=["hazirla", "sayim", "onkayit", "kesif", "olcum", "rapor", "sha"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "hazirla":
            print(json.dumps(MI._mi_json(cs_hazirla()), ensure_ascii=False, indent=1))
        elif a.komut == "sayim":
            S, KT = cs_sayim_kos(); MI._mi_jyaz(_cs_ham("sayim.json"), S, "sayım"); MI._mi_jyaz(_cs_ham("kitaplik.json"), KT, "kitaplık")
            print(json.dumps(MI._mi_json({k: {"n": v["n"], "ay": v["ay"]} for k, v in S["hucre"].items()}), ensure_ascii=False, indent=1))
            print(json.dumps(MI._mi_json(KT["ozet"]), ensure_ascii=False, indent=1))
            print("SAYIM_SHA:", HV.hv_json_sha(S), "KITAPLIK_SHA:", HV.hv_json_sha(KT))
        elif a.komut == "onkayit":
            print(cs_onkayit_yaz())
        elif a.komut == "kesif":
            K = cs_kesif(); print(json.dumps(MI._mi_json(K["agirlik"]), ensure_ascii=False, indent=1))
        elif a.komut == "olcum":
            J = cs_olcum(); print(json.dumps(MI._mi_json({"genel": J["genel"], "say": J["hukum_say"]}), ensure_ascii=False, indent=1))
        elif a.komut == "rapor":
            ek = _cs_ham("rapor_ek.json"); E = json.load(open(ek, encoding="utf-8")) if os.path.exists(ek) else {}
            print(cs_rapor_yaz(yeniden=E.get("yeniden"), hata=E.get("hata"), sapma=E.get("sapma")))
        elif a.komut == "sha":
            print(json.dumps(cs_sha_simdi(), indent=1))
    except CSHata as ex:
        cslog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_cs_ana())
