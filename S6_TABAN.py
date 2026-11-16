"""S6_TABAN — Cemal'in çöl kurallarından TABAN (çöl bölgesi) algoritması: Python referans + tasarım sınaması, tek dosya (v1.0 15 Kas, v1.1 16 Kas 2026).

Kaynak: arastirma_cikti/sikisma_obek/CEMAL_COL_KURALLARI.md (K1-K8, K6b; 16 etiket), arastirma_cikti/sikisma_s6/S6_TABAN_IS_TANIMI.md (v1.0) ve
S6_V11_IS_TANIMI.md (v1.1: S7 fikirleri; referans ATR pencere öncesi, Bollinger daralması, onay günü, sönme, tarih etiketleri).
Bu bir TASARIM ve GÖZ ARACIDIR: getiri / iz ölçmez (ölçüm sonra, ayrı ön kayıtla). Pine karşılığı: arastirma_cikti/sikisma_s6/COL_S6_TABAN.pine.

TANIM (her geçerli bar t için yalnız t ve öncesi; geçerli bar = H > L ve V > 0; i = t'nin geçerli bar sırası, 0'dan):
  Ölçülür bar: i >= atrGun (ATR% için 250 tam TR/C_önceki değeri). Pencere W(t, n) = son n geçerli bar [i-n+1, i].
  (1) BANT    max H(W) / min L(W) - 1 <= bantMax
  (2) SAKİN   |C_i / C_{i-n+1} - 1| <= netMax
  (3) DİP     h = n // 2; L1 = min L ilk h bar [i-n+1, i-n+h]; L2 = min L son n-h bar [i-n+h+1, i]; L2 >= L1 x (1 - dipTol)
  (4) MUM     medyan((H-L)/C, W) <= kM x ATR%. refOnce = False (v1.0): ATR% = ort(TR / önceki geçerli C) son atrGun geçerli bar [i-atrGun+1, i].
              refOnce = True (v1.1): ATR% = ort(TR / önceki C) pencereden ÖNCEKİ cnt = min(refGun, i-n) geçerli bar [i-n-cnt+1, i-n];
              cnt < refMin ise şart tutmaz (kümülatif toplam, her n için O(1)).
  (5) DARALMA ort((H-L)/C, W) <= daralmaOran x ort((H-L)/C, [i-n-daralmaGun+1, i-n]) ; daralmaOran = 0 -> şart yok (kapalı)
  (6) BB      bbSart = True (v1.1): bbw = 2 x bbK x std(ddof 0) / SMA (bbGun geçerli kapanış); bbp(i) = önceki bbDagilim bbw'den bbw(i)'ye <= olanların
              payı (SIKISMA_OBEK.so_s5 tanımı); bbp(i) <= bbEsik (pencerenin son gününde; n'den bağımsız).
  TABAN(t) = şartları sağlayan EN BÜYÜK n (nMax'tan nMin'e, ilk tutan). bas = i-n+1, TAVAN = max H(W) (tavan mumu = o High'ın İLK barı), DİP = min L(W).
  SINIF (bilgi): DİP = konum120 = (C - min C) / (max C - min C) (son 120 geçerli kapanış) <= 0,25 VE C / max C - 1 <= -%10;
                 YOL = C > SMA50 VE SMA50_i > SMA50_{i-20}; ikisi de değilse ORTA (öncelik DİP > YOL > ORTA).
  DURUM MAKİNESİ (Python ve Pine birebir; sıra önemli):
    AL_i = TABAN(i-1) var VE C_i > TAVAN(i-1). KIRILDI_i = TABAN(i-1) var VE AL değil VE C_i < DİP(i-1) x (1 - kirTol)  (iş tanımının harfi).
    AL / KIRILDI: açık bölge varsa i'de biter (kutu i'yi içerir; üst / alt i ile değişmez); i hiçbir bölgeye girmez. Açık bölge yoksa (önceki bar
    tabanlı ama bölgede değil: art arda ikinci AL ya da AL / KIRILDI sonrası kutu nMin bar dolmadan) işaret 'bölgesiz' basılır (AL_BOLGESIZ).
    Değilse ve TABAN(i) var:
       acik                                  -> AYNI bölge (pencere açık bölgeye değiyor; başlangıç ileri / geri oynasa da: 'bitişik parçalar tek bölge', K2)
       acik değil, son bölge kendiliğinden söndü (AL / KIRILDI değil) ve bas_i <= son bölgenin son barı -> SÖNEN BÖLGE SÜRER (aynı kutu)
       aksi -> YENİ bölge (sınıf = açılış barının sınıfı); sinir = önceki bölgenin son barı (yoksa -1; AL / KIRILDI'dan sonra o bar);
               yeni bölge yalnız i - max(bas_i, sinir + 1) + 1 >= nMin ise açılır (kırpılmış kutu en az nMin bar), değilse bar bölgesiz (KISA)
       kutu: sol = min(max(bas, sinir + 1)) (kutular üst üste binmez), sağ = i, üst = max TAVAN, alt = min DİP (bölgenin barları boyunca)
    Değilse acik ise bölge SÖNER (son bar i-1; durum SÖNDÜ; Pine: gri kenar + 'sonme' etiketi; pencere dönerse YENİDEN ile geri alınır).
    v1.1 ONAY günü = bölgenin açıldığı bar (durum YENİ; n ilk kez şartları sağlayıp kutu >= nMin olduğu gün). Kutunun [sol, onay) kısmı geriye
    uzatmadır (o gün bilinmiyordu; Pine'da kesik kenarlı soluk kutu). bolge_son_tur (her bar, as-of t): ACIK / AL / KIRILDI / SONDU.
    (surTol >= 0 yalnız Python BİLGİ kipi: iş tanımının harfi 'başlangıç en çok surTol bar ileri kayarsa aynı bölge, yoksa yeni bölge'; Pine'da yok.)
Komut:  python S6_TABAN.py tasarim [--veri D]        v1.0 etiket sınaması + 108 noktalı ızgara + ters sınama + evren sayımı -> S6_TASARIM.md, s6_tasarim.json
        python S6_TABAN.py tasarim11 [--veri D]      v1.1: refOnce x bbEsik (8 nokta) + v1.0 kipi birebirliği + CCOLA + evren -> json 'v11', md v1.1 bölümü
        python S6_TABAN.py liste SEMBOL BAS SON        bölge listesi (seçilen eşiklerle)
        python S6_TABAN.py pine                        Pine sabitleri ve 6 etiketin beklenen çıktısı (Pine üretmez)
        python S6_TABAN.py ascii                       COL_S6_TABAN_ascii.pine üretir ve doğrular (ASCII dışı 0, kod birebir)
Colab:  exec(open('S6_TABAN.py').read()); s6_tasarim()   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   V_BIST.pkl (FON_IZI.fi_k1_veri; düzeltilmiş fiyat), SIKISMA_YENIDEN.sy_veri_hazirla ile geçerli barlar (kriz kesiği 31.08.2026 dahil).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_S6 = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_S6 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_S6 not in sys.path:
    sys.path.insert(0, KOK_S6)

import SIKISMA_YENIDEN as SY  # noqa: E402

s6log = logging.getLogger("col.s6_taban")
if not s6log.handlers:
    _s6_h = logging.StreamHandler(sys.stderr)
    _s6_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s s6_taban: %(message)s", "%H:%M:%S"))
    s6log.addHandler(_s6_h)
    s6log.setLevel(logging.INFO)
    s6log.propagate = False

S6_SURUM = ("S6_TABAN v1.1 (2026-11-16): Cemal'in çöl kuralları -> taban bölgesi (bant, sakin, dip savunulur, küçük mum [referans pencere öncesi], "
            "daralma, Bollinger daralması) + al mumu / taban kırılımı / sönme; v1.0 kipi refOnce = False, bbSart = False")
S6_YOL = {"cikti": os.path.join(KOK_S6, "arastirma_cikti", "sikisma_s6"), "veri": os.environ.get("S6_VERI", "/tmp/veri"),
          "kod": os.path.join(KOK_S6, "S6_TABAN.py")}
S6_DOSYA = {"tasarim": "S6_TASARIM.md", "tasarim_json": "s6_tasarim.json"}
S6_ELLE = "<!-- ELLE YAZILAN BÖLÜMLER (s6_tasarim yeniden yazarken bu satırdan sonrasını korur) -->"

# Varsayılan (yapısal) parametreler. Eşik alanları (bantMax, netMax, kM, dipTol, daralmaOran) tasarım sınamasının SEÇTİĞİ değerlerdir
# (S6_TASARIM.md; seçim kuralı S6_IZGARA['secim_kurali']). Pine girdileri bunlarla birebir aynıdır.
S6_PRM: Dict[str, Any] = {
    "nMin": 8, "nMax": 70,
    "bantMax": 0.12, "netMax": 0.03, "kM": 0.90, "dipTol": 0.05, "daralmaOran": 0.0,
    "kirTol": 0.02, "atrGun": 250, "daralmaGun": 60, "konumGun": 120, "smaGun": 50, "smaEgimGun": 20,
    "dipKonum": 0.25, "dipDusus": -0.10, "surTol": -1, "hacimGun": 20,
    # v1.1 (S7 fikirleri; iş tanımı S6_V11_IS_TANIMI.md). Varsayılanlar v1.1 tasarım sınamasının SEÇTİĞİ değerlerdir (S6_IZGARA_V11).
    "refOnce": True, "refGun": 250, "refMin": 120,
    "bbSart": True, "bbEsik": 0.30, "bbGun": 20, "bbK": 2.0, "bbDagilim": 250,
}
S6_V10_KIP = {"refOnce": False, "bbSart": False}       # v1.0 davranışı (eski sonuçlar birebir)
S6_ESIK_ALAN = ("bantMax", "netMax", "kM", "dipTol", "daralmaOran")
S6_V11_ALAN = ("refOnce", "bbSart", "bbEsik")

# TASARIM IZGARASI (iş tanımı §4; sonuç görülmeden yazıldı). daralmaOran 0.0 = kapalı.
S6_IZGARA: Dict[str, Any] = {
    "bantMax": [0.12, 0.20], "netMax": [0.03, 0.05, 0.08], "kM": [0.75, 0.90, 1.00], "dipTol": [0.02, 0.05], "daralmaOran": [0.8, 0.9, 0.0],
    "sade": {"daralmaOran": 0.0, "dipTol": 0.05, "kM": 0.90, "netMax": 0.05, "bantMax": 0.20},
    "secim_kurali": "puan = DOĞRU bulunan (10) + YANLIŞ elenen (3) + AL mumu tutan (3); en yüksek puan; eşitlikte EN SADE: sözlük sırasıyla "
                    "(daralma kapalı -> 0, 0,9 -> 1, 0,8 -> 2), |dipTol - 0,05|, |kM - 0,90|, |netMax - 0,05|, |bantMax - 0,20| en küçük",
    "dogru_kurali": "DOĞRU bulundu: tek bir S6 bölgesinin kutusu [sol, sağ] ile Cemal aralığının kesişimi (geçerli bar) / Cemal aralığı (geçerli bar) >= 0,5",
    "yanlis_kurali": "YANLIŞ elendi: hiçbir S6 bölgesinin kutusu bu pencerenin >= 0,5'ini örtmüyor YA DA pencerenin son günü (S5 karar günü) "
                     "S6 bölgesi açık değil (o gün bölge bitmiş: AL / KIRILDI / söndü; iş tanımı §4)",
    "al_kurali": "AL tuttu: etiket gününe ±k geçerli bar içinde bir AL işareti var",
}

# v1.1 TASARIM IZGARASI (iş tanımı S6_V11_IS_TANIMI.md; v1.1 koşusundan ÖNCE yazıldı, sonuç görülünce değişmez). v1.0 eşikleri (bant 0,12 · net 0,03 ·
# kM 0,90 · dipTol 0,05 · daralma kapalı) sabit; yalnız yeni iki girdi taranır. Puan: 16 etiketten KNFRT'nin iki etiketi (D7, A1; 'tarih yanlış,
# Cemal'den beklenir') PUAN DIŞI -> 14 puanlı etiket. Taban çizgisi = v1.0 kipinin aynı 14 etiketteki puanı (v1.0: 13/16 = 13/14, KNFRT ikisi de tutmuyordu).
S6_IZGARA_V11: Dict[str, Any] = {
    "refOnce": [True, False], "bbEsik": [0.15, 0.20, 0.30, None],         # None = bbSart kapalı
    "puan_disi": ["D7 KNFRT 2022-06/09", "A1 KNFRT al mumu 2022-09-14"],
    "sade_sira": [(True, 0.20), (True, 0.30), (True, 0.15), (True, None), (False, 0.20), (False, 0.30), (False, 0.15), (False, None)],
    "secim_kurali": "taban = v1.0 kipinin 14 puanlı etiketteki puanı. Aday sırası (sadelik; S7 fikirleri açık olan önce, BB eşiği SIKISMA_OBEK "
                    "varsayılanı 0,20 önce, sonra gevşek 0,30, sonra sıkı 0,15): (ref açık, BB 0,20), (açık, 0,30), (açık, 0,15), (açık, BB kapalı), "
                    "(ref kapalı, 0,20), (kapalı, 0,30), (kapalı, 0,15), (kapalı, kapalı = v1.0). Puanı tabanın ALTINA DÜŞMEYEN ilk aday seçilir "
                    "(kötüleştiren yeni şart varsayılan KAPALI kalır); en yüksek puan aranmaz.",
    "ccola": {"sembol": "CCOLA", "ilk": "2025-10-02", "son": "2025-10-20"},
}

# 16 puanlı etiket + BİLGİ etiketleri (CEMAL_COL_KURALLARI.md; iş tanımı §4). 'yaklasik' = aralık fotoğraftan okunmuş.
S6_ETIKET: List[Dict[str, Any]] = [
    {"ad": "D1 FENER 2025-10", "tur": "DOGRU", "sembol": "FENER", "ilk": "2025-10-14", "son": "2025-11-07", "yaklasik": False},
    {"ad": "D2 CCOLA 2025-10", "tur": "DOGRU", "sembol": "CCOLA", "ilk": "2025-10-02", "son": "2025-10-15", "yaklasik": False},
    {"ad": "D3 ENJSA 2021-11 (tamamı)", "tur": "DOGRU", "sembol": "ENJSA", "ilk": "2021-10-26", "son": "2021-11-16", "yaklasik": False,
     "not": "Kasım kümesi yaklaşık 2021-10-20..12-05 (bilgi)"},
    {"ad": "D4 ENJSA 2025-02", "tur": "DOGRU", "sembol": "ENJSA", "ilk": "2025-01-20", "son": "2025-02-18", "yaklasik": True},
    {"ad": "D5 ENJSA 2025-05/06", "tur": "DOGRU", "sembol": "ENJSA", "ilk": "2025-05-08", "son": "2025-06-27", "yaklasik": False},
    {"ad": "D6 DESA 2021-10/12", "tur": "DOGRU", "sembol": "DESA", "ilk": "2021-10-27", "son": "2021-12-23", "yaklasik": False,
     "not": "uzun seçenek 2022-02-02'ye kadar (bilgi)"},
    {"ad": "D7 KNFRT 2022-06/09", "tur": "DOGRU", "sembol": "KNFRT", "ilk": "2022-06-15", "son": "2022-09-13", "yaklasik": True},
    {"ad": "D8 TUCLK 2025-06/08", "tur": "DOGRU", "sembol": "TUCLK", "ilk": "2025-06-10", "son": "2025-08-21", "yaklasik": True},
    {"ad": "D9 YKSLN 2026-03/05", "tur": "DOGRU", "sembol": "YKSLN", "ilk": "2026-03-19", "son": "2026-05-15", "yaklasik": True},
    {"ad": "D10 PAPIL küçük taban", "tur": "DOGRU", "sembol": "PAPIL", "ilk": "2025-11-13", "son": "2025-12-10", "yaklasik": False},
    {"ad": "Y1 ENJSA 2021-08/09 (net +%8,0)", "tur": "YANLIS", "sembol": "ENJSA", "ilk": "2021-08-11", "son": "2021-09-01", "yaklasik": False},
    {"ad": "Y2 ENJSA 2021-09/10 (net +%9,7)", "tur": "YANLIS", "sembol": "ENJSA", "ilk": "2021-09-28", "son": "2021-10-18", "yaklasik": False},
    {"ad": "Y3 TUCLK 2026-07/08 (kayan düşüş)", "tur": "YANLIS", "sembol": "TUCLK", "ilk": "2026-07-24", "son": "2026-08-13", "yaklasik": False},
    {"ad": "A1 KNFRT al mumu 2022-09-14", "tur": "AL", "sembol": "KNFRT", "gun": "2022-09-14", "tol": 3},
    {"ad": "A2 TUCLK al mumu 2025-08-22", "tur": "AL", "sembol": "TUCLK", "gun": "2025-08-22", "tol": 3},
    {"ad": "A3 PAPIL al mumu 2025-12-11", "tur": "AL", "sembol": "PAPIL", "gun": "2025-12-11", "tol": 1},
    # BİLGİ (puana girmez)
    {"ad": "B1 PAPIL büyük taban (bilgi)", "tur": "BILGI_DOGRU", "sembol": "PAPIL", "ilk": "2025-10-27", "son": "2026-03-02", "yaklasik": False},
    {"ad": "B2 ENJSA 2025-07/09 bant %23 (bilgi)", "tur": "BILGI_YANLIS", "sembol": "ENJSA", "ilk": "2025-07-28", "son": "2025-09-12", "yaklasik": False},
    {"ad": "B3 DESA taban bitişi (bilgi)", "tur": "BILGI_AL", "sembol": "DESA", "gun": "2021-12-23", "gun2": "2022-02-02", "tol": 3},
]
S6_PINE_ETIKET = ["D7 KNFRT 2022-06/09", "D8 TUCLK 2025-06/08", "D10 PAPIL küçük taban", "D5 ENJSA 2025-05/06", "D6 DESA 2021-10/12",
                  "Y3 TUCLK 2026-07/08 (kayan düşüş)"]
S6_EVREN = {"bas": "2016-01-01", "son": "2026-08-31", "ters_n": 40, "tohum": 615}

S6_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "tasarım / göz aracı; getiri ve eş karşılaştırması yok (ölçüm sonra, ayrı ön kayıtla, eşli taban + 200 rastgele eş portföy ile)"),
    "K2": ("EVET", "s6_taban her bar t için yalnız t ve öncesi; test_s6_taban.py önek değişmezliği (d.iloc[:T] ile tam serinin ilk T satırı birebir, "
                   "al / kirildi / bolge_id dahil) ve t sonrası bozma testi; kutunun sol kenarı (min bas) yalnız çizim / etiket kıyası"),
    "K3": ("EVET", "SY.sy_veri_hazirla: H>L, V>0, C>0, O>0 olmayan bar atılır; bütün pencereler geçerli bar dizisinde; Pine aynı 'gecerli' süzgeci"),
    "K4": ("EVET", "bölge = durum makinesi bölgesi (bir bölge bir kez sayılır); AL / KIRILDI bölge başına en çok bir kez; evren sayımı bölge açılış yılına göre"),
    "K5": ("UYGULANMAZ", "giriş / getiri yok; AL günü yalnız işaret (ölçüm işinde giriş = AL barından sonraki ilk açılış yazılacak)"),
    "K6": ("EVET", "tek kip: V_BIST düzeltilmiş fiyat (TradingView ADJ açık ile aynı); mum ve ATR yüzde; PAPIL tavanı 20,32 veriyle denetlendi"),
    "K7": ("EVET", "evren bugünün listesi (V_BIST 581 hisse): batanlar yok; evren sayımı yukarı / aşağı yanlı olabilir, raporda yazılı"),
    "K8": ("EVET", "16 etiket küçük örneklem: sonuç 'bulgu' değil, tasarım uyumu; ızgaranın 108 noktası tamamı raporlanır; aşırı uyum riski yazılı"),
    "K9": ("EVET", "ızgara, puan ve sadelik kuralı iş tanımında (commit 2460e39) koşudan önce; S6_IZGARA birebir; eşik değerleri hiç değişmedi. "
                   "UYARI: tanımda üç düzeltme ilk koşulardan SONRA yapıldı (YANLIŞ kuralının ikinci yarısı, AL kuralının harfe dönmesi, kutu >= nMin); "
                   "hepsi iş tanımının harfine yaklaştırma, sürüm sürüm sonuçları S6_TASARIM.md 'SÜRÜM KAYDI'nda"),
    "K10": ("UYGULANMAZ", "metin ayrıştırma yok; etiket tarihleri CEMAL_COL_KURALLARI.md'den elle girildi ve raporda tek tek yazılı"),
    "K11": ("EVET", "test_s6_taban.py: vektörel s6_taban ile Pine aynası döngü (s6_pine_ayna) 4 gerçek hissede birebir; D8 / D6 örtüşmesi (0,673 / 0,561) "
                    "ve DESA 2021-12-06 AL (tavan 1,0458, kapanış 1,0743), TUCLK 2025-08-05 tavanı ham OHLC'den bağımsız kodla yeniden üretildi"),
    "K12": ("EVET", "getiri / iz / emare sözü yok; 'tasarım uyumu' ve 'göz aracı' dili; PAPIL büyük taban başarısız kırılım uyarısı yazılı"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_s6; yasak dosyalara dokunulmadı (git status); e-posta taraması çıktıda; commit yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


class S6Hata(RuntimeError):
    """Durdurucu hata (veri yok / parametre geçersiz / sembol yok)."""


_S6_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _s6_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or S6_YOL["cikti"], S6_DOSYA.get(ad, ad))


def s6_prm(prm: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Varsayılanlarla birleştirir ve denetler."""
    P = dict(S6_PRM)
    if prm:
        bilinmeyen = [k for k in prm if k not in S6_PRM]
        if bilinmeyen:
            raise S6Hata(f"bilinmeyen parametre: {bilinmeyen}")
        P.update(prm)
    for k in ("nMin", "nMax", "atrGun", "daralmaGun", "konumGun", "smaGun", "smaEgimGun", "surTol", "hacimGun", "refGun", "refMin", "bbGun", "bbDagilim"):
        P[k] = int(P[k])
    for k in ("refOnce", "bbSart"):
        if not isinstance(P[k], (bool, np.bool_)):
            raise S6Hata(f"{k} True / False olmalı")
        P[k] = bool(P[k])
    if not (1 <= P["refMin"] <= P["refGun"]):
        raise S6Hata("1 <= refMin <= refGun olmalı")
    if not (0.0 < float(P["bbEsik"]) <= 1.0) or P["bbGun"] < 2 or P["bbDagilim"] < 10 or not (float(P["bbK"]) > 0):
        raise S6Hata("bbEsik (0, 1], bbGun >= 2, bbDagilim >= 10, bbK > 0 olmalı")
    if not (2 <= P["nMin"] <= P["nMax"]):
        raise S6Hata(f"nMin / nMax geçersiz: {P['nMin']} / {P['nMax']}")
    if P["nMax"] + P["daralmaGun"] > P["atrGun"]:
        raise S6Hata("nMax + daralmaGun <= atrGun olmalı (ölçülür barda bütün pencereler tanımlı)")
    if max(P["konumGun"], P["smaGun"] + P["smaEgimGun"], P["hacimGun"] + 1) > P["atrGun"] + 1:
        raise S6Hata("konumGun / SMA / hacim günü atrGun'dan uzun olamaz")
    for k in ("bantMax", "netMax", "kM", "dipTol", "kirTol"):
        if not (float(P[k]) > 0):
            raise S6Hata(f"{k} > 0 olmalı")
    if float(P["daralmaOran"]) < 0:
        raise S6Hata("daralmaOran >= 0 (0 = kapalı)")
    return P


# ---------------------------------------------------------------- 1) BİLEŞENLER (eşikten bağımsız; her n için)
def _s6_kaydir(x: np.ndarray, k: int) -> np.ndarray:
    """out[i] = x[i-k] (k >= 0)."""
    if k <= 0:
        return x.copy()
    return np.r_[np.full(k, np.nan), x[:-k]] if len(x) > k else np.full(len(x), np.nan)


def s6_bb(C: np.ndarray, P: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
    """Bollinger genişliği bbw = 2 x bbK x std(ddof=0) / SMA (bbGun geçerli kapanış) ve yüzdeliği bbp(t) = önceki bbDagilim günün bbw'lerinden
    bbw(t)'ye <= olanların payı (SIKISMA_OBEK.so_s5 tanımı; ta.percentrank DEĞİL). Toplamlar Pine'daki gibi SIRALI (k = 0..bbGun-1) yapılır:
    Python ile Pine aritmetiği bit düzeyinde aynı olsun diye (pandas rolling std çevrimiçi algoritmadır, son ondalıkta ayrışabilir)."""
    g, nb = int(P["bbGun"]), int(P["bbDagilim"]); N = len(C)
    bbw = np.full(N, np.nan); bbp = np.full(N, np.nan)
    if N >= g:
        W = np.lib.stride_tricks.sliding_window_view(C.astype(float), g)          # satır r = C[r .. r+g-1], bar t = r+g-1
        sm = np.zeros(W.shape[0])
        for k in range(g):
            sm = sm + W[:, k]
        mn = sm / g
        vs = np.zeros(W.shape[0])
        for k in range(g):
            dk = W[:, k] - mn
            vs = vs + dk * dk
        sd = np.sqrt(vs / g)
        with np.errstate(invalid="ignore", divide="ignore"):
            bbw[g - 1:] = 2.0 * float(P["bbK"]) * sd / mn
    if N > nb:
        Wb = np.lib.stride_tricks.sliding_window_view(bbw, nb)[:N - nb]             # satır j: bbw[j .. j+nb-1] = t-nb .. t-1, t = j+nb
        t_ = np.arange(nb, N)
        with np.errstate(invalid="ignore"):
            ok = np.isfinite(Wb).all(axis=1) & np.isfinite(bbw[t_])
            bbp[t_] = np.where(ok, (Wb <= bbw[t_][:, None]).sum(axis=1) / float(nb), np.nan)
    return bbw, bbp


def s6_bilesen(d: pd.DataFrame, prm: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """d = geçerli barlar (SY.sy_veri_hazirla). Sütun j <-> n = nMax - j. Eşikten bağımsız bileşenler (ızgara için bir kez hesaplanır)."""
    P = s6_prm(prm)
    for c in ("Open", "High", "Low", "Close", "Volume"):
        if c not in d.columns:
            raise S6Hata(f"sütun yok: {c}")
    H, L, C, V = (d[c].to_numpy(float) for c in ("High", "Low", "Close", "Volume"))
    N = len(C)
    ns = np.arange(P["nMax"], P["nMin"] - 1, -1)
    Cp = np.r_[np.nan, C[:-1]]
    tr = np.fmax(H, Cp) - np.fmin(L, Cp)
    with np.errstate(invalid="ignore", divide="ignore"):
        trp = tr / Cp
    trp[0] = np.nan
    atr = pd.Series(trp).rolling(P["atrGun"], min_periods=P["atrGun"]).mean().to_numpy()
    # v1.1 referans ATR%: pencereden ÖNCEKİ refGun geçerli bar (yoksa en az refMin). Kümülatif toplam SIRALI (np.cumsum = Pine'daki cumT += ...).
    cum = np.cumsum(np.r_[0.0, trp[1:]]) if N > 0 else np.zeros(0)
    mum = (H - L) / C
    sH, sL, sC, sM = pd.Series(H), pd.Series(L), pd.Series(C), pd.Series(mum)
    K = len(ns)
    B = {k: np.full((N, K), np.nan) for k in ("maxH", "minL", "cBas", "L1", "L2", "med", "ortW", "ortOnce", "atrRef")}
    ii = np.arange(N)
    once = sM.rolling(P["daralmaGun"], min_periods=P["daralmaGun"]).mean().to_numpy()
    for j, n in enumerate(ns):
        n = int(n); h = n // 2
        B["maxH"][:, j] = sH.rolling(n, min_periods=n).max().to_numpy()
        B["minL"][:, j] = sL.rolling(n, min_periods=n).min().to_numpy()
        B["cBas"][:, j] = _s6_kaydir(C, n - 1)
        B["L1"][:, j] = _s6_kaydir(sL.rolling(h, min_periods=h).min().to_numpy(), n - h)
        B["L2"][:, j] = sL.rolling(n - h, min_periods=n - h).min().to_numpy()
        B["med"][:, j] = sM.rolling(n, min_periods=n).median().to_numpy()
        B["ortW"][:, j] = sM.rolling(n, min_periods=n).mean().to_numpy()
        B["ortOnce"][:, j] = _s6_kaydir(once, n)
        kk = ii - n                                                      # pencereden önceki son bar; referans [kk-cnt+1, kk]
        cnt = np.minimum(P["refGun"], kk)
        okr = (kk >= 0) & (cnt >= P["refMin"])
        kkc = np.where(okr, kk, 0); c0 = np.where(okr, kk - cnt, 0)
        B["atrRef"][:, j] = np.where(okr, (cum[kkc] - cum[c0]) / np.where(okr, cnt, 1), np.nan)
    # sınıf (geçerli kapanışlar üzerinde)
    kg = P["konumGun"]
    mx = sC.rolling(kg, min_periods=kg).max().to_numpy(); mn = sC.rolling(kg, min_periods=kg).min().to_numpy()
    sma = sC.rolling(P["smaGun"], min_periods=P["smaGun"]).mean().to_numpy()
    sma_once = _s6_kaydir(sma, P["smaEgimGun"])
    with np.errstate(invalid="ignore", divide="ignore"):
        konum = np.where(mx > mn, (C - mn) / (mx - mn), np.nan)
        dd = C / mx - 1
        dip = (konum <= P["dipKonum"]) & (dd <= P["dipDusus"])
        yol = (C > sma) & (sma > sma_once)
    olculur = np.arange(N) >= P["atrGun"]
    sinif = np.where(olculur, np.where(dip, "DIP", np.where(yol, "YOL", "ORTA")), "")     # yalnız ölçülür barda (Pine ile aynı)
    hort = _s6_kaydir(pd.Series(V).rolling(P["hacimGun"], min_periods=P["hacimGun"]).mean().to_numpy(), 1)   # önceki 20 geçerli bar
    bbw, bbp = s6_bb(C, P)
    return {"P": P, "ns": ns, "B": B, "atr": atr, "bbw": bbw, "bbp": bbp, "mum": mum, "H": H, "L": L, "C": C, "V": V, "sinif": sinif, "konum": konum, "dd": dd,
            "sma": sma, "hort": hort, "olculur": olculur, "index": d.index}


def s6_sec(Z: Dict[str, Any], esik: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Her bar için TABAN n'i (0 = yok). esik: S6_ESIK_ALAN alanları; yoksa Z['P']."""
    P = dict(Z["P"]); P.update(esik or {})
    B = Z["B"]; atr = Z["atr"][:, None]
    with np.errstate(invalid="ignore", divide="ignore"):
        ok = (B["maxH"] / B["minL"] - 1.0 <= P["bantMax"])
        ok &= (np.abs(Z["C"][:, None] / B["cBas"] - 1.0) <= P["netMax"])
        ok &= (B["L2"] >= B["L1"] * (1.0 - P["dipTol"]))
        if P["refOnce"]:
            ok &= (B["med"] <= P["kM"] * B["atrRef"])                   # v1.1: referans pencereden önceki 250 bar
        else:
            ok &= (B["med"] <= P["kM"] * atr)                            # v1.0: t'deki ATR250 (pencere dahil)
        if float(P["daralmaOran"]) > 0:
            ok &= (B["ortW"] <= P["daralmaOran"] * B["ortOnce"])
        if P["bbSart"]:
            ok &= (Z["bbp"] <= float(P["bbEsik"]))[:, None]               # (6) BB genişliği yüzdeliği pencerenin son gününde
    ok &= Z["olculur"][:, None]
    var = ok.any(axis=1)
    j = np.argmax(ok, axis=1)
    return np.where(var, Z["ns"][j], 0).astype(int)


# ---------------------------------------------------------------- 2) DURUM MAKİNESİ (Pine ile birebir)
def s6_durum(Z: Dict[str, Any], nsec: np.ndarray, esik: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Her bar: taban (n, bas, tavan, dip, tavan_bar), AL / KIRILDI, bölge (id, kutu sol / sağ / üst / alt as-of t), sınıf ve ölçüler."""
    P = dict(Z["P"]); P.update(esik or {})
    H, L, C, N = Z["H"], Z["L"], Z["C"], len(Z["C"])
    nS = np.full(N, np.nan); basS = np.full(N, np.nan); tavS = np.full(N, np.nan); dipS = np.full(N, np.nan); tbarS = np.full(N, np.nan)
    al = np.zeros(N, bool); kir = np.zeros(N, bool); bid = np.full(N, -1, int); durum = np.array([""] * N, dtype=object)
    kSol = np.full(N, np.nan); kSag = np.full(N, np.nan); kUst = np.full(N, np.nan); kAlt = np.full(N, np.nan)
    onay = np.zeros(N, bool); sonTurA = np.array([""] * N, dtype=object); onayI = np.full(N, np.nan)
    acik = False; rid = -1; rBas = -1; rSon = -1; rTop = np.nan; rBot = np.nan; dogal = False; sinir = -1
    oncBas = -1; oncTav = np.nan; oncDip = np.nan; sonTur = ""; rOnay = -1
    for i in range(N):
        n = int(nsec[i])
        if n > 0:
            b = i - n + 1
            seg = H[b:i + 1]
            tbar = b + int(np.argmax(seg))           # ilk en yüksek High
            tav = float(seg.max()); dp = float(L[b:i + 1].min())
            nS[i] = n; basS[i] = b; tavS[i] = tav; dipS[i] = dp; tbarS[i] = tbar
        if not Z["olculur"][i]:
            continue
        a_ = bool(C[i] > oncTav)                                   # önceki barda taban yoksa oncTav = NaN -> yanlış
        k_ = bool((not a_) and C[i] < oncDip * (1.0 - P["kirTol"]))
        if a_ or k_:
            al[i] = a_; kir[i] = k_
            durum[i] = ("AL" if a_ else "KIRILDI") + ("" if acik else "_BOLGESIZ")
            if acik:
                rSon = i; acik = False; dogal = False; bid[i] = rid; sonTur = "AL" if a_ else "KIRILDI"
        elif n > 0:
            b = i - n + 1
            if acik and (P["surTol"] < 0 or b <= oncBas + P["surTol"]):
                durum[i] = "SURER"
            elif (not acik) and dogal and rid >= 0 and b <= rSon:
                acik = True; durum[i] = "YENIDEN"; sonTur = "ACIK"
            else:
                sinir_y = rSon if (rid >= 0 and not acik) else -1   # yeni kutu önceki bölgenin son barını geçmez
                if i - max(b, sinir_y + 1) + 1 >= P["nMin"]:          # kırpılmış kutu en az nMin bar (tek mumluk bölge yok)
                    sinir = sinir_y
                    rid += 1; acik = True; rBas = max(b, sinir + 1); rTop = tavS[i]; rBot = dipS[i]; durum[i] = "YENI"
                    onay[i] = True; rOnay = i; sonTur = "ACIK"                 # v1.1 ONAY günü: kutu ilk bu gün bilinir
                else:
                    durum[i] = "KISA"
            if durum[i] != "KISA":
                rBas = min(rBas, max(b, sinir + 1)); rTop = max(rTop, tavS[i]); rBot = min(rBot, dipS[i]); rSon = i
                bid[i] = rid
        else:
            if acik:
                acik = False; dogal = True; durum[i] = "SONDU"; sonTur = "SONDU"
        if bid[i] >= 0:
            kSol[i] = rBas; kSag[i] = rSon; kUst[i] = rTop; kAlt[i] = rBot
        sonTurA[i] = sonTur
        if rid >= 0:
            onayI[i] = rOnay
        if n > 0:
            oncBas = i - n + 1; oncTav = tavS[i]; oncDip = dipS[i]
        else:
            oncBas = -1; oncTav = np.nan; oncDip = np.nan
    # ölçüler (bilgi; tabanın kendi penceresinde)
    j = np.where(nS > 0, Z["P"]["nMax"] - np.nan_to_num(nS).astype(int), 0)
    r = np.arange(N); var = nS > 0
    B = Z["B"]

    def _al(x):
        return np.where(var, x[r, j], np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        bant = _al(B["maxH"] / B["minL"] - 1.0); net = _al(Z["C"][:, None] / B["cBas"] - 1.0)
        mumAtr = _al(B["med"] / (B["atrRef"] if P["refOnce"] else Z["atr"][:, None])); darOran = _al(B["ortW"] / B["ortOnce"]); dipSav = _al(B["L2"] / B["L1"] - 1.0)
        alBoy = np.where(al, (H - L) / C, np.nan); alHac = np.where(al, Z["V"] / Z["hort"], np.nan)
    idx = Z["index"]
    return pd.DataFrame({"n": nS, "bas_i": basS, "tavan": tavS, "dip": dipS, "tavan_i": tbarS, "bant": bant, "net": net, "mum_atr": mumAtr,
                         "daralma": darOran, "dip_sav": dipSav, "sinif": Z["sinif"], "al": al, "kirildi": kir, "bolge_id": bid, "durum": durum,
                         "kutu_sol_i": kSol, "kutu_sag_i": kSag, "kutu_ust": kUst, "kutu_alt": kAlt, "al_boy": alBoy, "al_hacim": alHac,
                         "atr": Z["atr"], "olculur": Z["olculur"], "bbp": Z["bbp"], "onay": onay, "onay_i": onayI,
                         "bolge_son_tur": sonTurA}, index=idx)


def s6_taban(d: pd.DataFrame, prm: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """d = SY.sy_veri_hazirla çıktısı. Her bar: n, bas (tarih), tavan, dip, sinif, al, kirildi, bolge_id, durum ve ölçüler. Yalnız t'ye kadar."""
    if d is None or len(d) == 0:
        raise S6Hata("boş veri")
    if not d.index.is_monotonic_increasing or d.index.has_duplicates:
        raise S6Hata("indeks artan ve tekil olmalı (SY.sy_veri_hazirla)")
    Z = s6_bilesen(d, prm)
    T = s6_durum(Z, s6_sec(Z))           # Z["P"] = s6_prm(prm): eşikler ve v1.1 girdileri prm'den
    ix = d.index
    T["bas"] = [ix[int(b)] if b == b else pd.NaT for b in T["bas_i"]]
    return T


def s6_bolgeler(T: pd.DataFrame) -> List[Dict[str, Any]]:
    """Bölge listesi (son bar itibarıyla kutular). durum: AL / KIRILDI / SONDU / ACIK."""
    ix = T.index; out = []
    if (T["bolge_id"] >= 0).sum() == 0:
        return out
    for rid, g in T[T["bolge_id"] >= 0].groupby("bolge_id", sort=True):
        son = g.iloc[-1]
        sol = int(son["kutu_sol_i"]); sag = int(son["kutu_sag_i"])
        dur = "AL" if bool(son["al"]) else "KIRILDI" if bool(son["kirildi"]) else None
        if dur is None:
            konum = ix.get_loc(g.index[-1])
            dur = "ACIK" if konum == len(T) - 1 else "SONDU"
        ilk = g.iloc[0]
        out.append({"id": int(rid), "sol_i": sol, "sag_i": sag, "bas": str(ix[sol].date()), "bitis": str(ix[sag].date()), "gun": sag - sol + 1,
                    "acilis": str(g.index[0].date()), "onay": str(g.index[0].date()), "onay_i": int(ix.get_loc(g.index[0])),
                    "onay_once_gun": int(ix.get_loc(g.index[0])) - sol, "sinif": str(ilk["sinif"]), "durum": dur,
                    "al_gun": str(g.index[-1].date()) if dur == "AL" else "", "kir_gun": str(g.index[-1].date()) if dur == "KIRILDI" else "",
                    "bolge_son_tur": dur, "tavan": float(son["kutu_ust"]), "dip": float(son["kutu_alt"]),
                    "al_boy": float(son["al_boy"]) if dur == "AL" else None, "al_hacim": float(son["al_hacim"]) if dur == "AL" else None})
    return out


# ---------------------------------------------------------------- 3) PINE AYNASI (Pine kodunun satır satır Python karşılığı; test için)
def s6_pine_ayna(d: pd.DataFrame, prm: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """COL_S6_TABAN.pine'ın döngü mantığının birebir Python çevirisi (yavaş). Test: s6_taban ile aynı n / al / kirildi / bolge_id / kutu."""
    P = s6_prm(prm)
    if P["surTol"] >= 0:
        raise S6Hata("Pine aynası yalnız surTol = -1 (birleşim kipi)")
    O_, H_, L_, C_, V_ = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    aH: List[float] = []; aL: List[float] = []; aC: List[float] = []; aM: List[float] = []; aTRP: List[float] = []; aV: List[float] = []
    aCum: List[float] = []; aBB: List[float] = []
    N = len(C_); nMin, nMax = P["nMin"], P["nMax"]
    out = {k: np.full(N, np.nan) for k in ("n", "tavan", "dip", "kutu_sol_i", "kutu_sag_i", "kutu_ust", "kutu_alt", "bbp", "onay_i")}
    alA = np.zeros(N, bool); kirA = np.zeros(N, bool); bidA = np.full(N, -1, int); sinA = np.array([""] * N, dtype=object)
    onA = np.zeros(N, bool); turA = np.array([""] * N, dtype=object)
    acik = False; rid = -1; rBas = -1; rSon = -1; rTop = np.nan; rBot = np.nan; dogal = False; sinir = -1
    oncTav = np.nan; oncDip = np.nan; cumT = 0.0; sonTur = ""; rOnay = -1
    g_, nb_, bbK = P["bbGun"], P["bbDagilim"], float(P["bbK"])
    for i in range(N):
        cOnce = aC[-1] if aC else np.nan
        trv = (H_[i] - L_[i]) if np.isnan(cOnce) else max(H_[i], cOnce) - min(L_[i], cOnce)
        aH.append(H_[i]); aL.append(L_[i]); aC.append(C_[i]); aV.append(V_[i]); aM.append((H_[i] - L_[i]) / C_[i])
        aTRP.append(np.nan if np.isnan(cOnce) else trv / cOnce)
        if not np.isnan(cOnce):
            cumT += trv / cOnce
        aCum.append(cumT)
        sz = len(aC)
        # Bollinger genişliği (sıralı toplam) ve yüzdeliği (önceki nb_ değer)
        bw = np.nan
        if sz >= g_:
            sm = 0.0
            for j in range(sz - g_, sz):
                sm += aC[j]
            mnb = sm / g_
            vs = 0.0
            for j in range(sz - g_, sz):
                dv = aC[j] - mnb
                vs += dv * dv
            bw = 2.0 * bbK * np.sqrt(vs / g_) / mnb
        aBB.append(bw)
        bbP = np.nan
        if sz > nb_ and not np.isnan(bw):
            say = 0; tam = True
            for j in range(sz - 1 - nb_, sz - 1):
                if np.isnan(aBB[j]):
                    tam = False
                elif aBB[j] <= bw:
                    say += 1
            bbP = say / float(nb_) if tam else np.nan
        out["bbp"][i] = bbP
        tN = 0; tTav = np.nan; tDip = np.nan
        bbOk = (not P["bbSart"]) or ((not np.isnan(bbP)) and bbP <= float(P["bbEsik"]))
        if i >= P["atrGun"]:
            s = 0.0
            for j in range(sz - P["atrGun"], sz):
                s += aTRP[j]
            atrP = s / P["atrGun"]
            # sonek dizileri (k = 1..nMax): en yüksek H, en düşük L
            sufH = [np.nan] * (nMax + 1); sufL = [np.nan] * (nMax + 1)
            mh = -np.inf; ml = np.inf
            for k in range(1, nMax + 1):
                mh = max(mh, aH[sz - k]); ml = min(ml, aL[sz - k]); sufH[k] = mh; sufL[k] = ml
            for kk in range(0, nMax - nMin + 1 if bbOk else 0):
                n = nMax - kk
                h = n // 2
                c1 = sufH[n] / sufL[n] - 1.0 <= P["bantMax"]
                c2 = c1 and abs(C_[i] / aC[sz - n] - 1.0) <= P["netMax"]
                c3 = False
                if c2:
                    l1 = aL[sz - n]
                    for j in range(sz - n, sz - n + h):
                        l1 = min(l1, aL[j])
                    c3 = sufL[n - h] >= l1 * (1.0 - P["dipTol"])
                c5 = False
                if c3:
                    if P["daralmaOran"] > 0:
                        sw = 0.0
                        for j in range(sz - n, sz):
                            sw += aM[j]
                        so = 0.0
                        for j in range(sz - n - P["daralmaGun"], sz - n):
                            so += aM[j]
                        c5 = sw / n <= P["daralmaOran"] * (so / P["daralmaGun"])
                    else:
                        c5 = True
                c4 = False
                if c5:
                    w = sorted(aM[sz - n:sz])
                    m2 = n // 2
                    med = w[m2] if n % 2 == 1 else (w[m2 - 1] + w[m2]) / 2.0
                    if P["refOnce"]:
                        cnt = min(P["refGun"], i - n)
                        if cnt >= P["refMin"]:
                            ref = (aCum[sz - 1 - n] - aCum[sz - 1 - n - cnt]) / cnt
                            c4 = med <= P["kM"] * ref
                    else:
                        c4 = med <= P["kM"] * atrP
                if c4:
                    tN = n
                    break
            if tN > 0:
                tTav = aH[sz - tN]; tDip = aL[sz - tN]
                for j in range(sz - tN, sz):
                    if aH[j] > tTav:
                        tTav = aH[j]
                    tDip = min(tDip, aL[j])
            # sınıf
            mx = C_[i]; mn = C_[i]
            for j in range(sz - P["konumGun"], sz):
                mx = max(mx, aC[j]); mn = min(mn, aC[j])
            konum = (C_[i] - mn) / (mx - mn) if mx > mn else np.nan
            dd = C_[i] / mx - 1.0
            sma = sum(aC[sz - P["smaGun"]:sz]) / P["smaGun"]
            smaO = sum(aC[sz - P["smaGun"] - P["smaEgimGun"]:sz - P["smaEgimGun"]]) / P["smaGun"]
            dipK = (not np.isnan(konum)) and konum <= P["dipKonum"] and dd <= P["dipDusus"]
            yolK = C_[i] > sma and sma > smaO
            sinA[i] = "DIP" if dipK else "YOL" if yolK else "ORTA"
            # durum makinesi
            a_ = (not np.isnan(oncTav)) and C_[i] > oncTav
            k_ = (not np.isnan(oncDip)) and (not a_) and C_[i] < oncDip * (1.0 - P["kirTol"])
            if a_ or k_:
                alA[i] = a_; kirA[i] = k_
                if acik:
                    rSon = i; acik = False; dogal = False; bidA[i] = rid; sonTur = "AL" if a_ else "KIRILDI"
            elif tN > 0:
                b = i - tN + 1
                if acik:
                    kisa = False
                elif dogal and rid >= 0 and b <= rSon:
                    acik = True; sonTur = "ACIK"
                    kisa = False
                else:
                    sinirY = rSon if rid >= 0 else -1
                    kisa = not (i - max(b, sinirY + 1) + 1 >= nMin)
                    if not kisa:
                        sinir = sinirY
                        rid += 1; acik = True; rBas = max(b, sinir + 1); rTop = tTav; rBot = tDip
                        onA[i] = True; rOnay = i; sonTur = "ACIK"
                if not kisa:
                    rBas = min(rBas, max(b, sinir + 1)); rTop = max(rTop, tTav); rBot = min(rBot, tDip); rSon = i; bidA[i] = rid
            elif acik:
                acik = False; dogal = True; sonTur = "SONDU"
            if bidA[i] >= 0:
                out["kutu_sol_i"][i] = rBas; out["kutu_sag_i"][i] = rSon; out["kutu_ust"][i] = rTop; out["kutu_alt"][i] = rBot
            turA[i] = sonTur
            if rid >= 0:
                out["onay_i"][i] = rOnay
            if tN > 0:
                oncTav = tTav; oncDip = tDip
            else:
                oncTav = np.nan; oncDip = np.nan
        if tN > 0:
            out["n"][i] = tN; out["tavan"][i] = tTav; out["dip"][i] = tDip
    R = pd.DataFrame(out, index=d.index)
    R["al"] = alA; R["kirildi"] = kirA; R["bolge_id"] = bidA; R["sinif"] = sinA; R["onay"] = onA; R["bolge_son_tur"] = turA
    return R


# ---------------------------------------------------------------- 4) VERİ
def s6_veri(veri: Optional[str] = None, semboller: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
    yol = os.path.join(veri or S6_YOL["veri"], "V_BIST.pkl")
    if not os.path.exists(yol):
        raise S6Hata(f"veri yok: {yol} (git worktree add /tmp/iv origin/islenmis-veri; python FON_IZI.py vpac /tmp/iv/veri /tmp/veri)")
    V = pd.read_pickle(yol)
    if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
        V = V["veri"]
    out = {}
    for s, d in V.items():
        if semboller is not None and s not in semboller:
            continue
        try:
            out[str(s)] = SY.sy_veri_hazirla(d, SY.SY_ESIK)
        except Exception as ex:  # tek hisse bozuksa diğerleri sürer
            s6log.warning("BIST %s atlandı: %s", s, ex)
    if semboller is not None:
        eksik = [s for s in semboller if s not in out]
        if eksik:
            raise S6Hata(f"sembol yok: {eksik}")
    s6log.info("V_BIST: %d hisse (%s)", len(out), yol)
    return out


# ---------------------------------------------------------------- 5) ETİKET SINAMASI
def _s6_ara_i(ix: pd.DatetimeIndex, ilk: str, son: str) -> Tuple[int, int]:
    a = int(ix.searchsorted(pd.Timestamp(ilk), side="left")); b = int(ix.searchsorted(pd.Timestamp(son), side="right")) - 1
    return a, b


def s6_etiket_sina(T_: Dict[str, pd.DataFrame], R_: Dict[str, List[Dict[str, Any]]], et: Dict[str, Any]) -> Dict[str, Any]:
    """Tek etiketin sonucu. T_: sembol -> s6_durum tablosu; R_: sembol -> bölge listesi."""
    T = T_[et["sembol"]]; R = R_[et["sembol"]]; ix = T.index
    if et["tur"] in ("AL", "BILGI_AL"):
        g = int(ix.searchsorted(pd.Timestamp(et["gun"])))
        al_i = np.where(T["al"].to_numpy())[0]
        yakin = [int(k) for k in al_i if abs(int(k) - g) <= et["tol"]]
        sonuc = {"ad": et["ad"], "tur": et["tur"], "tuttu": bool(yakin), "al_gun": [str(ix[k].date()) for k in yakin],
                 "fark_bar": [int(k) - g for k in yakin]}
        if et["tur"] == "BILGI_AL":
            g2 = int(ix.searchsorted(pd.Timestamp(et["gun2"])))
            yakin2 = [int(k) for k in al_i if abs(int(k) - g2) <= et["tol"]]
            kir_i = np.where(T["kirildi"].to_numpy())[0]
            sonuc.update({"al_gun2": [str(ix[k].date()) for k in yakin2],
                          "civar": [{"gun": str(ix[k].date()), "tur": "AL"} for k in al_i if g - 20 <= k <= g2 + 20]
                          + [{"gun": str(ix[k].date()), "tur": "KIRILDI"} for k in kir_i if g - 20 <= k <= g2 + 20]})
        return sonuc
    a, b = _s6_ara_i(ix, et["ilk"], et["son"])
    uz = b - a + 1
    en = 0.0; enR = None; birlesim = np.zeros(max(uz, 0), bool)
    for r in R:
        kes = max(0, min(b, r["sag_i"]) - max(a, r["sol_i"]) + 1)
        if kes > 0:
            birlesim[max(a, r["sol_i"]) - a:min(b, r["sag_i"]) - a + 1] = True
        o = kes / uz if uz > 0 else 0.0
        if o > en:
            en, enR = o, r
    bulundu = en >= 0.5
    acik_son = bool(b >= 0 and T["bolge_id"].iat[b] >= 0 and T["durum"].iat[b] not in ("AL", "KIRILDI"))   # Cemal aralığının son günü bölge açık mı
    tuttu = bulundu if et["tur"] in ("DOGRU", "BILGI_DOGRU") else (not bulundu or not acik_son)
    return {"ad": et["ad"], "tur": et["tur"], "tuttu": bool(tuttu), "ortusme": round(en, 3), "acik_son": acik_son, "birlesim": round(float(birlesim.mean()) if uz > 0 else 0, 3),
            "cemal_bar": uz, "bolge": ({k: enR[k] for k in ("bas", "bitis", "gun", "sinif", "durum", "al_gun", "kir_gun", "tavan", "dip", "onay", "onay_once_gun")}
                                       if enR else None)}


def _s6_ust_uste(R: List[Dict[str, Any]]) -> int:
    """Kutuları üst üste binen bölge çifti sayısı."""
    return int(sum(1 for a in range(len(R)) for b in range(a + 1, len(R)) if R[b]["sol_i"] <= R[a]["sag_i"] and R[a]["sol_i"] <= R[b]["sag_i"]))


def _s6_sade_anahtar(e: Dict[str, Any]) -> Tuple[float, ...]:
    S = S6_IZGARA["sade"]
    dar = {0.0: 0, 0.9: 1, 0.8: 2}[float(e["daralmaOran"])]
    return (dar, abs(e["dipTol"] - S["dipTol"]), abs(e["kM"] - S["kM"]), abs(e["netMax"] - S["netMax"]), abs(e["bantMax"] - S["bantMax"]))


def s6_izgara(Z_: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """108 nokta: her nokta için 16 puanlı etiket + bilgi etiketleri."""
    sat = []
    alanlar = list(S6_ESIK_ALAN)
    for deg in itertools.product(*[S6_IZGARA[k] for k in alanlar]):
        e = dict(zip(alanlar, deg)); e10 = dict(e, **S6_V10_KIP)           # v1.0 ızgarası v1.0 kipinde (eski sonuçlar birebir)
        T_ = {s: s6_durum(Z, s6_sec(Z, e10), e10) for s, Z in Z_.items()}
        R_ = {s: s6_bolgeler(T) for s, T in T_.items()}
        S_ = [s6_etiket_sina(T_, R_, et) for et in S6_ETIKET]
        puanli = [x for x in S_ if not x["tur"].startswith("BILGI")]
        sat.append({"esik": e, "puan": int(sum(x["tuttu"] for x in puanli)),
                    "dogru": int(sum(x["tuttu"] for x in puanli if x["tur"] == "DOGRU")),
                    "yanlis": int(sum(x["tuttu"] for x in puanli if x["tur"] == "YANLIS")),
                    "al": int(sum(x["tuttu"] for x in puanli if x["tur"] == "AL")),
                    "etiket": S_})
    return sat


def s6_secim(sat: List[Dict[str, Any]]) -> Dict[str, Any]:
    enp = max(x["puan"] for x in sat)
    aday = [x for x in sat if x["puan"] == enp]
    aday.sort(key=lambda x: _s6_sade_anahtar(x["esik"]))
    return {"en_puan": enp, "aday_sayi": len(aday), "secilen": aday[0]["esik"], "secilen_satir": aday[0],
            "aday_esikler": [x["esik"] for x in aday]}


# ---------------------------------------------------------------- 6) EVREN SAYIMI VE TERS SINAMA
def s6_evren_aday(V: Dict[str, pd.DataFrame], adaylar: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """BİLGİ: en yüksek puanlı noktaların evrende ne kadar sık bölge ürettiği (seçimi değiştirmez). Hisse başına bileşen bir kez hesaplanır."""
    bas, son = pd.Timestamp(S6_EVREN["bas"]), pd.Timestamp(S6_EVREN["son"])
    top = [{"bolge": 0, "al": 0, "acik": 0, "olc": 0, "uz": [], "durum": {}} for _ in adaylar]
    hy = set()
    for s, d in V.items():
        if len(d) < S6_PRM["atrGun"] + 30:
            continue
        try:
            Z = s6_bilesen(d)
        except S6Hata as ex:
            s6log.warning("%s atlandı: %s", s, ex); continue
        ix = Z["index"]; ol = Z["olculur"] & (ix >= bas) & (ix <= son)
        if ol.sum() == 0:
            continue
        hy |= {(s, int(y)) for y in np.unique(ix[ol].year)}
        for k, e in enumerate(adaylar):
            e = dict(S6_V10_KIP, **e)                                        # v1.1 alanları verilmezse v1.0 kipi
            T = s6_durum(Z, s6_sec(Z, e), e)
            top[k]["acik"] += int(((T["bolge_id"].to_numpy() >= 0) & ol).sum()); top[k]["olc"] += int(ol.sum())
            for r in s6_bolgeler(T):
                if bas <= pd.Timestamp(r["acilis"]) <= son:
                    top[k]["bolge"] += 1; top[k]["al"] += int(r["durum"] == "AL"); top[k]["uz"].append(r["gun"])
                    top[k]["durum"][r["durum"]] = top[k]["durum"].get(r["durum"], 0) + 1
    out = []
    for e, t in zip(adaylar, top):
        out.append({"esik": e, "bolge_hisse_yil": round(t["bolge"] / max(len(hy), 1), 2), "al_hisse_yil": round(t["al"] / max(len(hy), 1), 2),
                    "acik_bar_orani": round(t["acik"] / max(t["olc"], 1), 4), "uzunluk_medyan": float(np.median(t["uz"])) if t["uz"] else None,
                    "uzunluk_p90": float(np.percentile(t["uz"], 90)) if t["uz"] else None, "hisse_yil": len(hy), "bolge": t["bolge"], "al": t["al"],
                    "durum": t["durum"]})
    return out


def s6_evren(V: Dict[str, pd.DataFrame], esik: Dict[str, Any]) -> Dict[str, Any]:
    E_ = S6_EVREN; bas, son = pd.Timestamp(E_["bas"]), pd.Timestamp(E_["son"])
    yil_bolge: Dict[Tuple[str, int], int] = {}; yil_al: Dict[Tuple[str, int], int] = {}; yil_var: Dict[Tuple[str, int], int] = {}
    uzun: List[int] = []; sinif: Dict[str, int] = {}; durum: Dict[str, int] = {}
    nokta: List[Tuple[str, int]] = []; acik_oran: List[float] = []; kutu_oran: List[float] = []
    TT: Dict[str, pd.DataFrame] = {}
    al_sinyal = [0, 0, 0]
    for s, d in V.items():
        if len(d) < S6_PRM["atrGun"] + 30:
            continue
        try:
            Z = s6_bilesen(d, esik)
            T = s6_durum(Z, s6_sec(Z))
        except S6Hata as ex:
            s6log.warning("%s atlandı: %s", s, ex); continue
        TT[s] = T
        ix = T.index; ol = T["olculur"].to_numpy() & (ix >= bas) & (ix <= son)
        if ol.sum() == 0:
            continue
        for y in np.unique(ix[ol].year):
            yil_var[(s, int(y))] = int(((ix.year == y) & ol).sum())
        R = s6_bolgeler(T)
        kutu = np.zeros(len(T), bool)
        for r in R:
            kutu[r["sol_i"]:r["sag_i"] + 1] = True
            ac = pd.Timestamp(r["acilis"])
            if not (bas <= ac <= son):
                continue
            yil_bolge[(s, ac.year)] = yil_bolge.get((s, ac.year), 0) + 1
            uzun.append(r["gun"]); sinif[r["sinif"]] = sinif.get(r["sinif"], 0) + 1; durum[r["durum"]] = durum.get(r["durum"], 0) + 1
            if r["durum"] == "AL":
                y = pd.Timestamp(r["al_gun"]).year
                yil_al[(s, y)] = yil_al.get((s, y), 0) + 1
        acik_oran.append(float((T["bolge_id"].to_numpy() >= 0)[ol].mean())); kutu_oran.append(float(kutu[ol].mean()))
        al_sinyal[0] += int((T["al"].to_numpy() & ol).sum()); al_sinyal[1] += int((T["durum"].to_numpy() == "AL_BOLGESIZ")[ol].sum())
        al_sinyal[2] += int((T["kirildi"].to_numpy() & ol).sum())
        for k in np.where(ol)[0]:
            nokta.append((s, int(k)))
    hy = sorted(yil_var)
    nb = np.array([yil_bolge.get(k, 0) for k in hy]); na_ = np.array([yil_al.get(k, 0) for k in hy])
    yillik = {}
    for y in sorted({k[1] for k in hy}):
        ks = [k for k in hy if k[1] == y]
        yillik[str(y)] = {"hisse": len(ks), "bolge": int(sum(yil_bolge.get(k, 0) for k in ks)), "al": int(sum(yil_al.get(k, 0) for k in ks))}
    U = np.array(uzun) if uzun else np.array([0])
    # ters sınama: rastgele 40 hisse-tarih noktası
    rng = np.random.default_rng(E_["tohum"])
    sec = [nokta[int(k)] for k in rng.choice(len(nokta), size=min(E_["ters_n"], len(nokta)), replace=False)] if nokta else []
    ters = []
    for s, k in sec:
        T = TT[s]
        r_in = [r for r in s6_bolgeler(T) if r["sol_i"] <= k <= r["sag_i"]]
        ters.append({"sembol": s, "tarih": str(T.index[k].date()), "acik_t": bool(T["bolge_id"].iat[k] >= 0), "kutu": bool(r_in),
                     "n": None if np.isnan(T["n"].iat[k]) else int(T["n"].iat[k])})
    return {"hisse_yil": len(hy), "bolge_toplam": int(nb.sum()), "al_toplam": int(na_.sum()),
            "al_sinyal": al_sinyal[0], "al_bolgesiz": al_sinyal[1], "kirildi_sinyal": al_sinyal[2],
            "hisse_yil_basina_bolge": round(float(nb.mean()), 3) if len(nb) else None,
            "hisse_yil_basina_al": round(float(na_.mean()), 3) if len(na_) else None,
            "hisse_yil_bolge_dagilim": {str(k): int((nb == k).sum()) for k in range(0, 6)} | {"6+": int((nb >= 6).sum())},
            "uzunluk": {"n": len(uzun), "min": int(U.min()), "p10": float(np.percentile(U, 10)), "p25": float(np.percentile(U, 25)),
                        "medyan": float(np.median(U)), "p75": float(np.percentile(U, 75)), "p90": float(np.percentile(U, 90)), "max": int(U.max()),
                        "kova": {f"{a}-{b}": int(((U >= a) & (U <= b)).sum()) for a, b in ((8, 14), (15, 29), (30, 49), (50, 70), (71, 100), (101, 10 ** 6))}},
            "sinif": sinif, "durum": durum, "yillik": yillik,
            "acik_bar_orani_ort": round(float(np.mean(acik_oran)), 4) if acik_oran else None,
            "kutu_bar_orani_ort": round(float(np.mean(kutu_oran)), 4) if kutu_oran else None,
            "ters": ters, "ters_acik_orani": round(float(np.mean([x["acik_t"] for x in ters])), 3) if ters else None,
            "ters_kutu_orani": round(float(np.mean([x["kutu"] for x in ters])), 3) if ters else None}


# ---------------------------------------------------------------- 7) TASARIM KOMUTU VE RAPOR
def _yz(x: Any, n: int = 1) -> str:
    try:
        return "%" + f"{float(x) * 100:.{n}f}".replace(".", ",")
    except (TypeError, ValueError):
        return "-"


def _sy(x: Any, n: int = 2) -> str:
    try:
        return f"{float(x):.{n}f}".replace(".", ",")
    except (TypeError, ValueError):
        return "-"


def _s6_esik_md(e: Dict[str, Any]) -> str:
    dar = "kapalı" if float(e["daralmaOran"]) == 0 else _sy(e["daralmaOran"], 1)
    return f"bant {_sy(e['bantMax'])} · net {_sy(e['netMax'])} · kM {_sy(e['kM'])} · dipTol {_sy(e['dipTol'])} · daralma {dar}"


def _s6_etiket_satir(x: Dict[str, Any], et: Dict[str, Any]) -> str:
    isaret = "✓" if x["tuttu"] else "✗"
    if x["tur"] in ("AL", "BILGI_AL"):
        ek = (", 2. tarih (" + et.get("gun2", "") + ") ±3: " + (", ".join(x.get("al_gun2", [])) or "AL yok")) if x["tur"] == "BILGI_AL" else ""
        civ = ("; civar işaretler: " + ", ".join(f"{c['gun']} {c['tur']}" for c in x.get("civar", []))) if x["tur"] == "BILGI_AL" else ""
        return (f"| {x['ad']} | {et['gun']} ±{et['tol']} | - | - | {', '.join(x['al_gun']) or 'AL yok'}{ek}{civ} | "
                f"{isaret if x['tur'] == 'AL' else ('bilgi ' + isaret)} |")
    b = x["bolge"]
    s6 = f"{b['bas']} .. {b['bitis']} ({b['gun']} bar, {b['sinif']}, {b['durum']})" if b else "bölge yok"
    alg = (b["al_gun"] or (("KIRILDI " + b["kir_gun"]) if b["kir_gun"] else "-")) if b else "-"
    yak = " (yaklaşık)" if et.get("yaklasik") else ""
    son = isaret if not x["tur"].startswith("BILGI") else "bilgi " + isaret
    if x["tur"] in ("YANLIS", "BILGI_YANLIS"):
        alg += f"; {et['son']} günü bölge {'AÇIK' if x.get('acik_son') else 'kapalı'}"
    return f"| {x['ad']} | {et['ilk']} .. {et['son']}{yak} | {s6} | {_sy(x['ortusme'])} (birleşim {_sy(x['birlesim'])}) | {alg} | {son} |"


def s6_rapor_md(J: Dict[str, Any], cikti: Optional[str] = None) -> str:
    sec = J["secim"]; e = sec["secilen"]; satir = sec["secilen_satir"]; EV = J["evren"]
    s = ["# S6 TABAN — TASARIM SINAMASI (15 Kasım 2026)", "",
         f"Üreten: `python S6_TABAN.py tasarim` ({S6_SURUM}). Veri: V_BIST.pkl (düzeltilmiş fiyat), geçerli barlar SY.sy_veri_hazirla. "
         f"Bu bir tasarım ve göz aracıdır: getiri / iz ölçülmedi.", "", "## ÖZET", "",
         f"- Seçilen eşikler: {_s6_esik_md(e)} (nMin {S6_PRM['nMin']}, nMax {S6_PRM['nMax']}, kirTol {_sy(S6_PRM['kirTol'])}).",
         f"- Bu noktada 16 puanlı etiketten {satir['puan']} / 16 tutuyor: DOĞRU bölge {satir['dogru']}/10, YANLIŞ elenen {satir['yanlis']}/3, AL mumu {satir['al']}/3.",
         f"- 108 noktanın en yüksek puanı {sec['en_puan']}/16; bu puanı {sec['aday_sayi']} nokta alıyor; seçim sadelik sırasıyla.",
         f"- Evren (V_BIST 2016-26, {EV['hisse_yil']} hisse-yıl): hisse-yıl başına {_sy(EV['hisse_yil_basina_bolge'])} bölge, {_sy(EV['hisse_yil_basina_al'])} AL; "
         f"bölge uzunluğu medyan {_sy(EV['uzunluk']['medyan'], 0)} bar (%10-%90: {_sy(EV['uzunluk']['p10'], 0)}-{_sy(EV['uzunluk']['p90'], 0)}).",
         f"- Ters sınama: rastgele {len(EV['ters'])} hisse-tarihin {_yz(EV['ters_acik_orani'], 0)} kadarı o gün açık bir S6 bölgesinde "
         f"(kutu içinde: {_yz(EV['ters_kutu_orani'], 0)}); bütün ölçülür barlarda ortalama {_yz(EV['acik_bar_orani_ort'], 0)}. " + ("Bu tanımla çöl NADİR DEĞİL (açık bar oranı > %10; aşağıda aday sıklığı)." if (EV['acik_bar_orani_ort'] or 0) > 0.10 else "Çöl nadir (açık bar oranı <= %10)."),
         "", "## ALGORİTMA (son hâli)", "", "```", "TANIM" + __doc__.split("\nTANIM", 1)[1].split("Komut:")[0].rstrip(), "```", "",
         "Sabitler: " + ", ".join(f"{k} = {v}" for k, v in S6_PRM.items() if k not in S6_ESIK_ALAN) + ".", "",
         "İş tanımında açık bırakılan noktalar (kod ve Pine'da aynı karar): (i) yarılar h = n // 2 (tek n'de fazladan bar ikinci yarıda); "
         "(ii) ölçülür bar i >= 250 (ATR% tam); (iii) tavan mumu = pencerede en yüksek High'ın İLK barı; (iv) SÜREKLİLİK (iş tanımından SAPMA, gerekçe HATA bölümünde): "
         "açık bölgede taban sürdükçe başlangıç ne kadar oynarsa oynasın aynı bölge (pencereler birleşir); iş tanımının harfi (±2 bar) BİLGİ olarak "
         "aşağıda ayrıca koşuldu; yeni kutu önceki bölgenin son barını geçmez; "
         "(v) taban bir gün kaybolup pencere eski bölgenin son barına dokunarak dönerse aynı bölge sürer (K2 'bitişik parçalar tek bölge'); "
         "(vi) AL / KIRILDI iş tanımının harfiyle: önceki barda taban varsa (bölge şartı yok; ilk sürümdeki 'kilit' ve 'açık bölge' şartları kaldırıldı, HATA bölümü); "
         "AL / KIRILDI barı hiçbir bölgeye girmez, sonraki kutu o bardan sonra başlar; (vii) önceki bar tabanlı ama açık bölge yoksa AL 'bölgesiz' işarettir (kutusuz); yeni kutu kırpıldıktan sonra en az nMin bar olmalı; "
         "(viii) sınıf için 120 gün aralığı ve SMA50 geçerli bar kapanışlarıyla, 'SMA50 yükseliyor' = SMA50_t > SMA50_t-20 (S5 ile aynı).", "",
         "## ETİKET TABLOSU (seçilen eşikler)", "", "| etiket | Cemal aralığı / günü | S6 bölgesi (en çok örten) | örtüşme | AL günü | sonuç |", "|---|---|---|---|---|---|"]
    etd = {et["ad"]: et for et in S6_ETIKET}
    s += [_s6_etiket_satir(x, etd[x["ad"]]) for x in satir["etiket"]]
    s += ["", "Örtüşme = en çok örten TEK bölge kutusunun Cemal aralığıyla kesişimi / Cemal aralığı (geçerli bar); birleşim = bütün bölgelerin birlikte örttüğü pay (bilgi). "
          "YANLIŞ etiketlerde ✓ = örtüşme < 0,5 ya da aralığın son günü (S5 karar günü) bölge açık değil (elendi). AL etiketinde ✓ = etiket gününe ±tol geçerli bar içinde AL.", "",
          "## IZGARA (108 nokta, tamamı)", "", f"Seçim kuralı: {S6_IZGARA['secim_kurali']}.", "",
          "Puan dağılımı: " + ", ".join(f"{p}/16: {n} nokta" for p, n in sorted(J["puan_dagilim"].items(), key=lambda z: -int(z[0]))) + ".", "",
          f"En yüksek puanlı {sec['aday_sayi']} nokta: " + "; ".join(_s6_esik_md(x) for x in sec["aday_esikler"][:12])
          + (" ..." if sec["aday_sayi"] > 12 else "") + ".", "",
          "Etiket başına tutan nokta sayısı (108 içinde): " + "; ".join(f"{k}: {v}" for k, v in J["etiket_tutan"].items()) + ".", "",
          "| # | bantMax | netMax | kM | dipTol | daralma | puan | DOĞRU | YANLIŞ | AL | tutmayan puanlı etiketler |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, x in enumerate(J["izgara"], 1):
        ee = x["esik"]; tm = [y["ad"].split(" ")[0] for y in x["etiket"] if not y["tur"].startswith("BILGI") and not y["tuttu"]]
        isar = " **seçilen**" if ee == e else ""
        s.append(f"| {k}{isar} | {_sy(ee['bantMax'])} | {_sy(ee['netMax'])} | {_sy(ee['kM'])} | {_sy(ee['dipTol'])} | "
                 f"{'kapalı' if float(ee['daralmaOran']) == 0 else _sy(ee['daralmaOran'], 1)} | {x['puan']} | {x['dogru']} | {x['yanlis']} | {x['al']} | {', '.join(tm) or '-'} |")
    s += ["", "## SÜREKLİLİK KURALI: seçilen (birleşim) ile iş tanımının harfi (±2 bar) — seçilen eşiklerde, 8 etiket hissesinin tamamında", "",
          "| kip | puan /16 | bölge sayısı | kutusu üst üste binen çift | tutmayan puanlı etiketler |", "|---|---|---|---|---|"]
    for ad, k in J["sureklilik_kip"].items():
        tm = [x["ad"].split(" ")[0] for x in k["etiket"] if not x["ad"].startswith("B") and not x["tuttu"]]
        s.append(f"| {ad} | {k['puan']} | {k['bolge']} | {k['ust_uste']} | {', '.join(tm) or '-'} |")
    s += ["", "## TERS SINAMA ve EVREN SAYIMI (seçilen eşikler; V_BIST 2016-01-01 .. 2026-08-31, ölçülür barlar)", "",
          f"- Hisse-yıl: {EV['hisse_yil']}; bölge (açılış yılına göre): {EV['bolge_toplam']}; AL: {EV['al_toplam']}.",
          f"- Bütün AL işaretleri {EV.get('al_sinyal', '-')} (bunun {EV.get('al_bolgesiz', '-')} tanesi bölgesiz: önceki bar tabanlı ama açık bölge yok — art arda AL ya da AL / KIRILDI sonrası kutu 8 bar dolmadan; kutusuz üçgen); KIRILDI işaretleri {EV.get('kirildi_sinyal', '-')}.",
          f"- Hisse-yıl başına bölge {_sy(EV['hisse_yil_basina_bolge'])}, AL {_sy(EV['hisse_yil_basina_al'])} (bölgeyi kapatan AL). Hisse-yıl başına bölge sayısı dağılımı: "
          + ", ".join(f"{k}: {v}" for k, v in EV["hisse_yil_bolge_dagilim"].items()) + ".",
          f"- Bölge uzunluğu (geçerli bar, kutu sol..sağ): min {EV['uzunluk']['min']}, %10 {_sy(EV['uzunluk']['p10'], 0)}, %25 {_sy(EV['uzunluk']['p25'], 0)}, "
          f"medyan {_sy(EV['uzunluk']['medyan'], 0)}, %75 {_sy(EV['uzunluk']['p75'], 0)}, %90 {_sy(EV['uzunluk']['p90'], 0)}, en çok {EV['uzunluk']['max']}. "
          "Kovalar: " + ", ".join(f"{k}: {v}" for k, v in EV["uzunluk"]["kova"].items()) + ".",
          "- Sınıf (açılış günü): " + ", ".join(f"{k}: {v}" for k, v in sorted(EV["sinif"].items())) + ". Bitiş: "
          + ", ".join(f"{k}: {v}" for k, v in sorted(EV["durum"].items())) + ".",
          "- Yıllara göre (hisse / bölge / AL): " + "; ".join(f"{y}: {v['hisse']} / {v['bolge']} / {v['al']}" for y, v in EV["yillik"].items()) + ".",
          f"- Hisse başına ortalama: ölçülür barların {_yz(EV['acik_bar_orani_ort'])} kadarı o gün açık bölgede, {_yz(EV['kutu_bar_orani_ort'])} kadarı sonradan çizilen bir kutunun içinde.",
          f"- Ters sınama (tohum {S6_EVREN['tohum']}, {len(EV['ters'])} rastgele hisse-tarih): o gün açık bölge {_yz(EV['ters_acik_orani'], 0)}, kutu içinde {_yz(EV['ters_kutu_orani'], 0)}."]
    s += ["", f"BİLGİ (seçimi değiştirmez): en yüksek puanlı {len(EV.get('aday_sikligi', []))} noktanın evrende sıklığı (aynı evren ve dönem).", "",
          "| eşikler | bölge / hisse-yıl | AL / hisse-yıl | açık bar oranı (bütün barlar havuzu) | uzunluk medyan | uzunluk %90 |", "|---|---|---|---|---|---|"]
    s += [f"| {_s6_esik_md(x['esik'])}{' **seçilen**' if x['esik'] == e else ''} | {_sy(x['bolge_hisse_yil'])} | {_sy(x['al_hisse_yil'])} | "
          f"{_yz(x['acik_bar_orani'])} | {_sy(x['uzunluk_medyan'], 0)} | {_sy(x['uzunluk_p90'], 0)} |" for x in EV.get("aday_sikligi", [])]
    s += ["", "Ters sınama noktaları:", "", "| sembol | tarih | o gün açık bölge | kutu içinde | taban n |", "|---|---|---|---|---|"]
    s += [f"| {x['sembol']} | {x['tarih']} | {'evet' if x['acik_t'] else '-'} | {'evet' if x['kutu'] else '-'} | {x['n'] if x['n'] else '-'} |" for x in EV["ters"]]
    s += ["", "Not: evren bugünün listesi (hayatta kalma yanlılığı); likidite süzgeci yok; sayım ölçüm değildir.", ""]
    metin = "\n".join(s)
    yol = _s6_yol("tasarim", cikti)
    elle = ""
    if os.path.exists(yol):
        with open(yol, encoding="utf-8") as f:
            eski = f.read()
        if S6_ELLE in eski:
            elle = eski.split(S6_ELLE, 1)[1]
    metin = metin + "\n" + S6_ELLE + elle
    if _S6_EPOSTA.search(metin):
        raise S6Hata("raporda e-posta biçimli parça var")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin if metin.endswith("\n") else metin + "\n")
    return yol


def s6_tasarim(veri: Optional[str] = None, cikti: Optional[str] = None, evren: bool = True) -> Dict[str, Any]:
    """Etiket sınaması + 108 noktalı ızgara + ters sınama + evren sayımı. Çıktı: S6_TASARIM.md, s6_tasarim.json."""
    sem = sorted({et["sembol"] for et in S6_ETIKET})
    V = s6_veri(veri)
    eksik = [s for s in sem if s not in V]
    if eksik:
        raise S6Hata(f"etiket sembolü veride yok: {eksik}")
    Z_ = {s: s6_bilesen(V[s]) for s in sem}
    s6log.info("ızgara: %d nokta", int(np.prod([len(S6_IZGARA[k]) for k in S6_ESIK_ALAN])))
    sat = s6_izgara(Z_)
    sec = s6_secim(sat)
    s6log.info("seçilen: %s (puan %d, %d aday)", sec["secilen"], sec["en_puan"], sec["aday_sayi"])
    pd_ = {}
    for x in sat:
        pd_[str(x["puan"])] = pd_.get(str(x["puan"]), 0) + 1
    et_tutan = {et["ad"].split(" ")[0]: int(sum(1 for x in sat for y in x["etiket"] if y["ad"] == et["ad"] and y["tuttu"])) for et in S6_ETIKET}
    kip = {}
    for ad, st in (("birlesim (seçilen)", -1), ("is_tanimi_harfi_2bar", 2)):
        e2 = dict(sec["secilen"], **S6_V10_KIP); e2["surTol"] = st
        T_ = {s: s6_durum(Z, s6_sec(Z, e2), e2) for s, Z in Z_.items()}
        R_ = {s: s6_bolgeler(T) for s, T in T_.items()}
        S_ = [s6_etiket_sina(T_, R_, et) for et in S6_ETIKET]
        kip[ad] = {"puan": int(sum(x["tuttu"] for x in S_ if not x["tur"].startswith("BILGI"))), "bolge": int(sum(len(r) for r in R_.values())),
                   "ust_uste": int(sum(_s6_ust_uste(r) for r in R_.values())),
                   "etiket": [{"ad": x["ad"], "tuttu": x["tuttu"], "ortusme": x.get("ortusme")} for x in S_]}
    EV = s6_evren(V, dict(sec["secilen"], **S6_V10_KIP)) if evren else {}
    if evren:
        EV["aday_sikligi"] = s6_evren_aday(V, sec["aday_esikler"])
    J = {"surum": S6_SURUM, "zaman": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "prm": S6_PRM, "izgara_tanim": S6_IZGARA,
         "etiketler": S6_ETIKET, "izgara": sat, "secim": sec, "sureklilik_kip": kip, "puan_dagilim": pd_, "etiket_tutan": et_tutan, "evren": EV,
         "secilen_varsayilan_ayni": all(abs(float(sec["secilen"][k]) - float(S6_PRM[k])) < 1e-12 for k in S6_ESIK_ALAN)}
    yj = _s6_yol("tasarim_json", cikti)
    os.makedirs(os.path.dirname(yj), exist_ok=True)
    metin = json.dumps(J, ensure_ascii=False, indent=1, default=str)
    if _S6_EPOSTA.search(metin):
        raise S6Hata("json'da e-posta biçimli parça var")
    with open(yj, "w", encoding="utf-8") as f:
        f.write(metin)
    if evren:
        s6_rapor_md(J, cikti)
    if not J["secilen_varsayilan_ayni"]:
        s6log.warning("SEÇİLEN eşikler S6_PRM varsayılanından farklı: %s -> S6_PRM ve Pine güncellenmeli", sec["secilen"])
    return J


# ---------------------------------------------------------------- 7b) v1.1 TASARIM SINAMASI (S7 fikirleri; S6_IZGARA_V11)
S6_V11_ISARET = ("<!-- V1.1 OTOMATİK BAŞ (s6_tasarim_v11 yazar; elle düzenleme YOK) -->", "<!-- V1.1 OTOMATİK SON -->")


def _s6_v11_esik(e5: Dict[str, Any], ref: bool, bb: Optional[float]) -> Dict[str, Any]:
    return dict(e5, refOnce=bool(ref), bbSart=bb is not None, bbEsik=float(bb) if bb is not None else float(S6_PRM["bbEsik"]))


def _s6_v11_ad(ref: bool, bb: Optional[float]) -> str:
    return f"ref {'açık' if ref else 'kapalı'} · BB {'kapalı' if bb is None else _sy(bb)}"


def s6_v11_nokta(Z_: Dict[str, Dict[str, Any]], e: Dict[str, Any]) -> Dict[str, Any]:
    """Bir v1.1 noktası: 16 etiket, 14 puanlı (KNFRT puan dışı) ve 16 ölçekli puan, CCOLA Ekim 2025 kutusu, etiket hisselerinde bölge / sönme sayısı."""
    T_ = {s: s6_durum(Z, s6_sec(Z, e), e) for s, Z in Z_.items()}
    R_ = {s: s6_bolgeler(T) for s, T in T_.items()}
    S_ = [s6_etiket_sina(T_, R_, et) for et in S6_ETIKET]
    disi = set(S6_IZGARA_V11["puan_disi"])
    p16 = [x for x in S_ if not x["tur"].startswith("BILGI")]
    p14 = [x for x in p16 if x["ad"] not in disi]
    cc = S6_IZGARA_V11["ccola"]; Tc = T_[cc["sembol"]]; a, b = _s6_ara_i(Tc.index, cc["ilk"], cc["son"])
    kut = [r for r in R_[cc["sembol"]] if r["sag_i"] >= a and r["sol_i"] <= b]
    ccola = {"aralik": f"{cc['ilk']} .. {cc['son']}", "cemal_bar": b - a + 1,
             "kutular": [{k: r[k] for k in ("bas", "bitis", "gun", "onay", "sinif", "durum", "al_gun", "kir_gun", "tavan", "dip")}
                         | {"ortusme": round((min(b, r["sag_i"]) - max(a, r["sol_i"]) + 1) / (b - a + 1), 3)} for r in kut]}
    ccola["kutu_var"] = any(k["ortusme"] >= 0.5 for k in ccola["kutular"])
    dur: Dict[str, int] = {}
    for R in R_.values():
        for r in R:
            dur[r["durum"]] = dur.get(r["durum"], 0) + 1
    return {"esik": e, "puan14": int(sum(x["tuttu"] for x in p14)), "puan16": int(sum(x["tuttu"] for x in p16)),
            "dogru": int(sum(x["tuttu"] for x in p14 if x["tur"] == "DOGRU")), "yanlis": int(sum(x["tuttu"] for x in p14 if x["tur"] == "YANLIS")),
            "al": int(sum(x["tuttu"] for x in p14 if x["tur"] == "AL")), "etiket": S_, "ccola": ccola,
            "bolge_etiket_hisse": int(sum(len(r) for r in R_.values())), "durum_etiket_hisse": dur}


def _s6_json_esit(a: Any, b: Any) -> bool:
    return json.loads(json.dumps(a, default=str, ensure_ascii=False)) == json.loads(json.dumps(b, default=str, ensure_ascii=False))


def s6_tasarim_v11(veri: Optional[str] = None, cikti: Optional[str] = None, evren: bool = True) -> Dict[str, Any]:
    """v1.1 sınaması: v1.0 eşikleri sabit; refOnce x bbEsik ızgarası (8 nokta), seçim S6_IZGARA_V11['secim_kurali'], v1.0 kipinin birebirliği,
    CCOLA 2-20 Eki 2025, evren sıklığı (8 noktanın tamamı). Çıktı: s6_tasarim.json 'v11' anahtarı, S6_TASARIM.md v1.1 otomatik bölümü."""
    yj = _s6_yol("tasarim_json", cikti)
    if not os.path.exists(yj):
        raise S6Hata(f"v1.0 tasarım json'u yok: {yj} (önce python S6_TABAN.py tasarim)")
    J0 = json.load(open(yj, encoding="utf-8"))
    e5 = {k: float(J0["secim"]["secilen"][k]) for k in S6_ESIK_ALAN}
    if any(abs(e5[k] - float(S6_PRM[k])) > 1e-12 for k in S6_ESIK_ALAN):
        raise S6Hata(f"v1.0 seçilen eşikler S6_PRM'den farklı: {e5}")
    sem = sorted({et["sembol"] for et in S6_ETIKET} | {S6_IZGARA_V11["ccola"]["sembol"]})
    V = s6_veri(veri)
    eksik = [x for x in sem if x not in V]
    if eksik:
        raise S6Hata(f"etiket sembolü veride yok: {eksik}")
    Z_ = {x: s6_bilesen(V[x]) for x in sem}
    noktalar = [(r, b) for r in S6_IZGARA_V11["refOnce"] for b in S6_IZGARA_V11["bbEsik"]]
    sat = []
    for r, b in noktalar:
        x = s6_v11_nokta(Z_, _s6_v11_esik(e5, r, b)); x["ad"] = _s6_v11_ad(r, b); x["ref"] = r; x["bb"] = b
        sat.append(x)
        s6log.info("v1.1 %s: puan %d/14 (%d/16), CCOLA kutu %s", x["ad"], x["puan14"], x["puan16"], x["ccola"]["kutu_var"])
    taban = [x for x in sat if x["ref"] is False and x["bb"] is None][0]
    # v1.0 kipi birebir: 16 etiket çıktısı (v1.0 json'daki alanlar) aynı mı
    eski = J0["secim"]["secilen_satir"]["etiket"]
    yeni_ = [{k: y.get(k) if k != "bolge" else ({kk: y["bolge"][kk] for kk in (e_["bolge"] or {})} if y.get("bolge") else None) for k in e_}
             for e_, y in zip(eski, taban["etiket"])]
    v10_birebir = len(eski) == len(taban["etiket"]) and _s6_json_esit(eski, yeni_)
    if not v10_birebir:
        s6log.error("v1.0 kipi eski 16 etiket sonucunu BİREBİR vermiyor")
    secilen = None
    for r, b in S6_IZGARA_V11["sade_sira"]:
        x = [y for y in sat if y["ref"] == r and y["bb"] == b][0]
        if x["puan14"] >= taban["puan14"]:
            secilen = x; break
    sec_e = {"refOnce": secilen["ref"], "bbSart": secilen["bb"] is not None, "bbEsik": secilen["bb"] if secilen["bb"] is not None else float(S6_PRM["bbEsik"])}
    EV = s6_evren_aday(V, [x["esik"] for x in sat]) if evren else []
    J1 = {"surum": S6_SURUM, "zaman": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "izgara_tanim": S6_IZGARA_V11, "esik_sabit": e5,
          "taban_puan14": taban["puan14"], "taban_puan16": taban["puan16"], "v10_kipi_birebir": bool(v10_birebir),
          "izgara": sat, "secilen": sec_e, "secilen_ad": secilen["ad"],
          "secilen_varsayilan_ayni": all(S6_PRM[k] == sec_e[k] for k in ("refOnce", "bbSart")) and (not sec_e["bbSart"] or abs(S6_PRM["bbEsik"] - sec_e["bbEsik"]) < 1e-12),
          "evren": EV, "evren_v10_rapor": {"bolge_hisse_yil": J0.get("evren", {}).get("hisse_yil_basina_bolge"),
                                           "al_hisse_yil": J0.get("evren", {}).get("hisse_yil_basina_al")}}
    J0["v11"] = J1
    metin = json.dumps(J0, ensure_ascii=False, indent=1, default=str)
    if _S6_EPOSTA.search(metin):
        raise S6Hata("json'da e-posta biçimli parça var")
    with open(yj, "w", encoding="utf-8") as f:
        f.write(metin)
    s6_rapor_v11_md(J1, cikti)
    if not J1["secilen_varsayilan_ayni"]:
        s6log.warning("v1.1 SEÇİLEN %s S6_PRM varsayılanından farklı -> S6_PRM ve Pine güncellenmeli", sec_e)
    return J1


def s6_rapor_v11_md(J: Dict[str, Any], cikti: Optional[str] = None) -> str:
    """S6_TASARIM.md'de v1.1 otomatik bölümünü yazar (işaretler arası); v1.0 bölümü ve elle yazılanlar korunur."""
    etd = {et["ad"]: et for et in S6_ETIKET}
    sat = J["izgara"]; sec = [x for x in sat if x["ad"] == J["secilen_ad"]][0]; tab = [x for x in sat if x["ref"] is False and x["bb"] is None][0]
    s = [S6_V11_ISARET[0], "", "## v1.1 TASARIM SINAMASI (otomatik; `python S6_TABAN.py tasarim11`)", "",
         f"Sabit eşikler (v1.0 seçimi): {_s6_esik_md(J['esik_sabit'])}. Puan 14 etiket üzerinden (KNFRT'nin D7 ve A1 etiketi puan dışı: "
         "'tarih yanlış, Cemal'den beklenir'); parantezde 16 ölçekli puan.", "",
         f"- v1.0 kipi (refOnce kapalı, BB kapalı) eski 16 etiket sonucunu birebir veriyor mu: **{'EVET' if J['v10_kipi_birebir'] else 'HAYIR'}**.",
         f"- Taban çizgisi (v1.0 kipi): {tab['puan14']}/14 ({tab['puan16']}/16).",
         f"- Seçilen: **{J['secilen_ad']}** ({sec['puan14']}/14, {sec['puan16']}/16).", "",
         f"Seçim kuralı (koşudan önce kodda): {S6_IZGARA_V11['secim_kurali']}", "",
         "| nokta | puan /14 | /16 | DOĞRU /9 | YANLIŞ /3 | AL /2 | tutmayan puanlı etiketler | CCOLA 2-20 Eki 2025 kutu | etiket hisselerinde bölge | bitiş (AL / KIRILDI / SONDU / ACIK) |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    disi = set(S6_IZGARA_V11["puan_disi"])
    for x in sat:
        tm = [y["ad"].split(" ")[0] for y in x["etiket"] if not y["tur"].startswith("BILGI") and y["ad"] not in disi and not y["tuttu"]]
        cc = x["ccola"]; ck = "; ".join(f"{k['bas']}..{k['bitis']} onay {k['onay']} örtüşme {_sy(k['ortusme'])} {k['durum']}" for k in cc["kutular"]) or "kutu yok"
        d_ = x["durum_etiket_hisse"]
        s.append(f"| {x['ad']}{' **seçilen**' if x is sec else ''}{' (v1.0)' if x is tab else ''} | {x['puan14']} | {x['puan16']} | {x['dogru']} | {x['yanlis']} | {x['al']} | "
                 f"{', '.join(tm) or '-'} | {'VAR' if cc['kutu_var'] else 'YOK'}: {ck} | {x['bolge_etiket_hisse']} | "
                 f"{d_.get('AL', 0)} / {d_.get('KIRILDI', 0)} / {d_.get('SONDU', 0)} / {d_.get('ACIK', 0)} |")
    for baslik, x in (("SEÇİLEN v1.1", sec), ("v1.0 kipi", tab)):
        s += ["", f"### Etiket tablosu: {baslik} ({x['ad']})", "",
              "| etiket | Cemal aralığı / günü | S6 bölgesi (en çok örten; onay günü) | örtüşme | AL günü | sonuç |", "|---|---|---|---|---|---|"]
        for y in x["etiket"]:
            satir = _s6_etiket_satir(y, etd[y["ad"]])
            if y.get("bolge") and y["bolge"].get("onay"):
                satir = satir.replace(f"{y['bolge']['durum']})", f"{y['bolge']['durum']}; onay {y['bolge']['onay']}, öncesi {y['bolge']['onay_once_gun']} bar kesik)", 1)
            if y["ad"] in disi:
                satir = satir.rsplit("|", 2)[0] + "| puan dışı (" + ("✓" if y["tuttu"] else "✗") + ") |"
            s.append(satir)
    if J["evren"]:
        v0 = J["evren_v10_rapor"]
        s += ["", f"### Evren sıklığı (V_BIST {S6_EVREN['bas']} .. {S6_EVREN['son']}, bölge açılış yılına göre; v1.0 raporu: {_sy(v0['bolge_hisse_yil'])} bölge, "
              f"{_sy(v0['al_hisse_yil'])} AL / hisse-yıl)", "",
              "| nokta | hisse-yıl | bölge / hisse-yıl | AL / hisse-yıl | açık bar oranı | uzunluk medyan | %90 | bitiş AL / KIRILDI / SONDU / ACIK |", "|---|---|---|---|---|---|---|---|"]
        for x, ev in zip(sat, J["evren"]):
            d_ = ev.get("durum", {})
            s.append(f"| {x['ad']}{' **seçilen**' if x is sec else ''}{' (v1.0)' if x is tab else ''} | {ev['hisse_yil']} | {_sy(ev['bolge_hisse_yil'])} | {_sy(ev['al_hisse_yil'])} | "
                     f"{_yz(ev['acik_bar_orani'])} | {_sy(ev['uzunluk_medyan'], 0)} | {_sy(ev['uzunluk_p90'], 0)} | "
                     f"{d_.get('AL', 0)} / {d_.get('KIRILDI', 0)} / {d_.get('SONDU', 0)} / {d_.get('ACIK', 0)} |")
    s += ["", S6_V11_ISARET[1]]
    blok = "\n".join(s)
    yol = _s6_yol("tasarim", cikti)
    eski = open(yol, encoding="utf-8").read() if os.path.exists(yol) else ""
    if S6_V11_ISARET[0] in eski and S6_V11_ISARET[1] in eski:
        on, kalan = eski.split(S6_V11_ISARET[0], 1)
        metin = on + blok + kalan.split(S6_V11_ISARET[1], 1)[1]
    else:
        if S6_ELLE not in eski:
            eski = eski.rstrip("\n") + "\n\n" + S6_ELLE + "\n"
        metin = eski.rstrip("\n") + "\n\n" + blok + "\n"
    if _S6_EPOSTA.search(metin):
        raise S6Hata("raporda e-posta biçimli parça var")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin if metin.endswith("\n") else metin + "\n")
    return yol


def s6_liste(sembol: str, bas: str, son: str, veri: Optional[str] = None) -> str:
    V = s6_veri(veri, [sembol])
    T = s6_taban(V[sembol])
    R = [r for r in s6_bolgeler(T) if r["bitis"] >= bas and r["bas"] <= son]
    s = [f"{sembol} S6 bölgeleri {bas} .. {son} ({_s6_esik_md(S6_PRM)}; refOnce {S6_PRM['refOnce']}, BB {S6_PRM['bbEsik'] if S6_PRM['bbSart'] else 'kapalı'})",
         "bas        bitis      gün  onay       sınıf durum    AL / KIRILDI  tavan     dip"]
    for r in R:
        s.append(f"{r['bas']} {r['bitis']} {r['gun']:>4} {r['onay']} {r['sinif']:<5} {r['durum']:<8} {(r['al_gun'] or r['kir_gun'] or '-'):<13} "
                 f"{r['tavan']:<9.4g} {r['dip']:<9.4g}")
    if not R:
        s.append("(bölge yok)")
    return "\n".join(s)


def s6_pine(veri: Optional[str] = None) -> str:
    """Pine girdi varsayılanları ve 6 etiketin beklenen çıktısı (Pine dosyası sonundaki yorumla aynı olmalı)."""
    s = ["Pine varsayılanları (COL_S6_TABAN.pine girdileri):"] + [f"  {k} = {v}" for k, v in S6_PRM.items()]
    sem = sorted({et["sembol"] for et in S6_ETIKET if et["ad"] in S6_PINE_ETIKET})
    V = s6_veri(veri, sem)
    T_ = {x: s6_taban(V[x]) for x in sem}
    for ad in S6_PINE_ETIKET:
        et = [x for x in S6_ETIKET if x["ad"] == ad][0]
        T = T_[et["sembol"]]
        a, b = _s6_ara_i(T.index, et["ilk"], et["son"])
        R = [r for r in s6_bolgeler(T) if r["sag_i"] >= a - 5 and r["sol_i"] <= b + 25]
        s.append(f"{ad}: Cemal {et['ilk']} .. {et['son']}")
        for r in R:
            s.append(f"   kutu {r['bas']} .. {r['bitis']} ({r['gun']} bar, onay {r['onay']}, {r['sinif']}, {r['durum']}"
                     + (f", AL {r['al_gun']}" if r["al_gun"] else "") + (f", KIRILDI {r['kir_gun']}" if r["kir_gun"] else "")
                     + f", tavan {r['tavan']:.4g}, dip {r['dip']:.4g})")
        if not R:
            s.append("   bölge yok")
    return "\n".join(s)


# ---------------------------------------------------------------- 8) PINE ASCII KOPYASI
S6_ASCII = {"ç": "c", "Ç": "C", "ğ": "g", "Ğ": "G", "ı": "i", "İ": "I", "ö": "o", "Ö": "O", "ş": "s", "Ş": "S", "ü": "u", "Ü": "U", "â": "a",
            "σ": "s", "–": "-", "—": "-", "’": "'", "‘": "'", "“": '"', "”": '"', "×": "x", "≤": "<=", "≥": ">=", "→": "->", "≈": "~", "±": "+-"}


def _s6_kod_kismi(satir: str) -> str:
    """Pine satırının yorum ve dize DIŞI kısmı (dizelerin içi boşaltılır)."""
    out = []; i = 0; q = None
    while i < len(satir):
        ch = satir[i]
        if q is None:
            if satir.startswith("//", i):
                break
            if ch in "\"'":
                q = ch; out.append(ch)
            else:
                out.append(ch)
        else:
            if ch == "\\":
                i += 2; continue
            if ch == q:
                q = None; out.append(ch)
        i += 1
    return "".join(out).rstrip()


def s6_ascii(kaynak: Optional[str] = None, hedef: Optional[str] = None) -> Dict[str, Any]:
    """COL_S6_TABAN.pine -> COL_S6_TABAN_ascii.pine (S6_ASCII eşlemesi) ve doğrulama: ASCII dışı 0; yorum / dize dışı kod birebir; satır sayısı aynı."""
    kaynak = kaynak or _s6_yol("COL_S6_TABAN.pine"); hedef = hedef or _s6_yol("COL_S6_TABAN_ascii.pine")
    metin = open(kaynak, encoding="utf-8").read()
    asc = "".join(S6_ASCII.get(ch, ch) for ch in metin)
    kalan = sorted({ch for ch in asc if ord(ch) > 127})
    if kalan:
        raise S6Hata(f"ASCII eşlemesinde olmayan karakter: {kalan}")
    a1, a2 = metin.splitlines(), asc.splitlines()
    kod_ascii_disi = [k + 1 for k, ln in enumerate(a1) if any(ord(ch) > 127 for ch in _s6_kod_kismi(ln))]
    fark = [k + 1 for k, (x, y) in enumerate(zip(a1, a2)) if _s6_kod_kismi(x) != _s6_kod_kismi(y)]
    if len(a1) != len(a2) or fark or kod_ascii_disi:
        raise S6Hata(f"ASCII doğrulama: satır {len(a1)}/{len(a2)}, kod farkı {fark[:5]}, kodda ASCII dışı {kod_ascii_disi[:5]}")
    with open(hedef, "w", encoding="ascii", newline="\n") as f:
        f.write(asc)
    return {"satir": len(a2), "ascii_disi": 0, "kod_farki": 0, "hedef": hedef}


# ---------------------------------------------------------------- 9) ÇAKIŞMA KAPISI
def _cakisma_kontrol_s6(_once=_CK_ONCE_S6, _dosya="S6_TABAN.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_S6", "_CK_KAYIT", "_cakisma_kontrol_s6", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "re", "itertools", "_dt", "SY", "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_s6()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=S6_SURUM)
    ap.add_argument("komut", choices=["tasarim", "tasarim11", "liste", "pine", "ascii"])
    ap.add_argument("arg", nargs="*", help="liste: SEMBOL BAS SON")
    ap.add_argument("--veri", default=None)
    ap.add_argument("--cikti", default=None)
    a = ap.parse_args()
    try:
        if a.komut == "tasarim":
            J_ = s6_tasarim(a.veri, a.cikti)
            print(json.dumps({"secilen": J_["secim"]["secilen"], "puan": J_["secim"]["en_puan"], "aday": J_["secim"]["aday_sayi"],
                              "varsayilan_ayni": J_["secilen_varsayilan_ayni"]}, ensure_ascii=False))
        elif a.komut == "tasarim11":
            J_ = s6_tasarim_v11(a.veri, a.cikti)
            print(json.dumps({"secilen": J_["secilen_ad"], "taban14": J_["taban_puan14"], "v10_birebir": J_["v10_kipi_birebir"],
                              "puan": {x["ad"]: [x["puan14"], x["puan16"], x["ccola"]["kutu_var"]] for x in J_["izgara"]},
                              "varsayilan_ayni": J_["secilen_varsayilan_ayni"]}, ensure_ascii=False))
        elif a.komut == "liste":
            if len(a.arg) != 3:
                raise S6Hata("kullanım: python S6_TABAN.py liste SEMBOL BAS SON")
            print(s6_liste(a.arg[0], a.arg[1], a.arg[2], a.veri))
        elif a.komut == "ascii":
            print(json.dumps(s6_ascii(), ensure_ascii=False))
        else:
            print(s6_pine(a.veri))
    except S6Hata as ex:
        s6log.error("%s", ex); sys.exit(1)
