"""K59 — BASİT SİNYALLER x PORTFÖY CETVELİ v2 (aylık, binlerce hisse), tek dosya (11 Kasım 2026; ana oturum iş tanımı, yol haritası Y1).

Soru: nedeni bilinen, basit, SÜREKLİ sinyaller (momentum, dönüş, küçüklük, bilanço tepkisi, kârlılık, düşük ihraç, satış ivmesi, düşük
oynaklık, 52 hafta zirvesine yakınlık) ve önceden yazılı 4'lü bileşik (COMP4 = momentum + PEAD + kârlılık + düşük ihraç sıra ortalaması)
aylık dengelenen uzun-yalnız üst %10 portföyünde, maliyetten sonra, eşit ağırlıklı uygun evreni geçiyor mu? Olay sayısı sorunu yok:
her ay binlerce hisse sıralanır.
  Evrenler  U1 = V_ABD (2016-2026), U2 = K57-B geniş ABD Yahoo önbelleği (2020-2026), BIST = V_BIST (bilgi). Hepsi yalnız yaşayanlar.
  Cetvel v2 = K58 C şartları (NW t > 2, 3 alt dönemin 2'si, son %30) + beta düzeltmeli alfa (portföy = alfa + beta x evren; NW t(alfa) > 2).
  Plasebo   = U2'de 200 rastgele sinyal aynı cetvelden; yanlış pozitif > %5 ise cetvel güvenilmez, hüküm verilmez.
K57 / K58 / FON_IZI fonksiyonları MODÜL olarak içe alınır (kopya yok, o dosyalar değişmez). SEC'e istek atılmaz (frames önbelleği yoksa durur).

Komut:  python K59.py onkayit            ön kaydı yazar (ölçümden ÖNCE; mühür + veri sha256; varsa üzerine yazmaz)
        python -I K59.py kos             ölçüm (mühür, veri sha256 ve ön kaydın git'e işlenmiş olması doğrulanır) + rapor
        python K59.py rapor              K59_RAPOR.md'yi çıktılardan yeniden yazar
        python -I K59.py kapsam [yol]    yalnız kapsam sayımı (hisse / ay / sinyal başına kaç hisse); portföy getirisi HESAPLAMAZ
K59-B (K59 §6'daki önceden yazılı üç deneme; ayrı ön kayıt K59B_ON_KAYIT.md, ayrı mühür; K59 ölçüm kodu ve K59 mührü değişmez):
        python K59.py b_onkayit          K59-B ön kaydını yazar (ölçümden ÖNCE; K59B mührü + K59 mührü + veri sha256; varsa üzerine yazmaz)
        python -I K59.py b_kos           (a) küçük-orta, (b) 3 ay tutma + örtüşen kohort, (c) French harmanı; iki mühür + veri + git doğrulanır
        python K59.py b_rapor            K59B_RAPOR.md'yi çıktılardan yeniden yazar
        python -I K59.py b_kapsam [yol]  yalnız sayım (alt evren ve sinyal başına hisse sayıları); portföy getirisi HESAPLAMAZ
Colab:  exec(open('K59.py').read()); k59_kos()
Veri:   /tmp/veri/V_ABD.pkl, V_BIST.pkl (yoksa `git worktree add /tmp/iv origin/islenmis-veri` + `python FON_IZI.py vpac /tmp/iv/veri /tmp/veri`),
        /tmp/k57b_fiyat/ (K57-B Yahoo önbelleği), /tmp/secframes/ (SEC frames), /tmp/secfs/ (SEC finansal özütler), /tmp/k58_french/.
        Kişisel e-posta / anahtar yok. Çıktılar arastirma_cikti/k59_basit_sinyaller/.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K59 = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import zipfile  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K59 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K59 not in sys.path:
    sys.path.insert(0, KOK_K59)

import FON_IZI as FI  # noqa: E402
import K57  # noqa: E402
import K58  # noqa: E402

k59log = logging.getLogger("col.k59")
if not k59log.handlers:
    _k59_h = logging.StreamHandler(sys.stderr)
    _k59_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k59: %(message)s", "%H:%M:%S"))
    k59log.addHandler(_k59_h)
    k59log.setLevel(logging.INFO)
    k59log.propagate = False

K59_SURUM = ("K59 v1.1 (2026-11-11): basit sinyaller (S1-S9, COMP4, COMP9) + DOSYA ailesi (DOSYA_Y, DOSYA_D, DOSYA_YD) + UCUZLUK koşullu testi x "
             "portföy cetveli v2 (K58 C + beta düzeltmeli alfa); ABD iki evren karar, BIST bilgi")
K59_YOL = {"cikti": os.path.join(KOK_K59, "arastirma_cikti", "k59_basit_sinyaller")}
K59_SIRA = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256'sı K59_ON_KAYIT.md'de; sonradan değişmez)
K59_ESIK: Dict[str, Any] = {
    "evren": {
        "U1": {"ad": "V_ABD (islenmis-veri; bugün yaşayan ~1.400 ABD hissesi)", "kaynak": "V_ABD", "rol": "KARAR", "bas": "2016-01-01",
               "kes": "2026-08-31", "fiyat_min": 2.0, "likit_min": 1.0e6, "maliyet": 0.001, "min_evren": 100, "min_sinyal": 100,
               "boyut": "islem_degeri", "sinyal": K59_SIRA, "french": True},
        "U2": {"ad": "geniş ABD evreni (K57-B Yahoo önbelleği; bugün yaşayan ~4.260 hisse)", "kaynak": "K57B_YAHOO", "rol": "KARAR",
               "bas": "2020-01-01", "kes": "2026-08-31", "fiyat_min": 2.0, "likit_min": 1.0e6, "maliyet": 0.001, "min_evren": 100,
               "min_sinyal": 100, "boyut": "piyasa_degeri", "sinyal": K59_SIRA, "french": True, "min_hisse": 3000},
        "BIST": {"ad": "V_BIST (islenmis-veri; bugün yaşayan ~580 hisse)", "kaynak": "V_BIST", "rol": "BİLGİ", "bas": "2016-01-01",
                 "kes": "2026-08-31", "fiyat_min": None, "likit_min": None, "maliyet": 0.003, "min_evren": 50, "min_sinyal": 30,
                 "boyut": "islem_degeri", "sinyal": ["S1", "S2", "S3", "S8", "S9"], "french": False},
    },
    "uygunluk": {"gecmis_gun": 252, "likit_gun": 20, "likit_min_gun": 15, "ileri_tasima": 5},
    "sinyal": {
        "S1": {"ad": "momentum 12-1", "uzun": 12, "kisa": 1},
        "S2": {"ad": "1 ay dönüş (geçen ayın en çok düşenleri)"},
        "S3": {"ad": "küçüklük", "pay_kapsam_min": 0.50},
        "S4": {"ad": "bilanço tepkisi (PEAD)", "pencere_gun": 63},
        "S5": {"ad": "kârlılık (son 4 çeyrek net kâr / özkaynak)", "ceyrek": 4},
        "S6": {"ad": "düşük net ihraç (yıllık pay değişimi)", "aykiri_kat": 5.0},
        "S7": {"ad": "satış ivmesi (son çeyrek / önceki iki çeyrek ortalaması)"},
        "S8": {"ad": "düşük oynaklık (60 gün)", "gun": 60, "min_gun": 40},
        "S9": {"ad": "52 hafta zirvesine yakınlık", "gun": 252, "min_gun": 200},
    },
    "temel_max_gun": 200,
    # ek bileşenler: yalnız DOSYA bileşiklerinin üyesidir, tek başına portföy olarak ÖLÇÜLMEZ (ek deneme sayılmasın diye)
    "ek_bilesen": {"X1": {"ad": "çeyrek geliri yıllık büyümesi (son çeyrek / bir yıl önceki aynı çeyrek - 1)"},
                   "X2": {"ad": "düşük kaldıraç (toplam yükümlülük / özkaynak; düşük iyi)"},
                   "X3": {"ad": "252 gün zirvesinden uzaklık (S9'un tersi; düşmüş iyi)"}},
    "bilesik": {"COMP4": {"ad": "bileşik: momentum + PEAD + kârlılık + düşük ihraç", "uye": ["S1", "S4", "S5", "S6"], "min": 3, "rol": "KARAR"},
                "COMP9": {"ad": "bileşik: dokuz sinyalin hepsi", "uye": K59_SIRA, "min": 5, "rol": "BİLGİ"},
                "DOSYA_Y": {"ad": "YEOTK tipi: ivmelenen, kârlı, seyrelmesiz büyüme", "uye": ["S7", "X1", "S5", "S6", "S4"], "min": 4, "rol": "DOSYA"},
                "DOSYA_D": {"ad": "DGXX tipi (vekil): sağlam bilanço + büyüme + düşmüş fiyat", "uye": ["X2", "X1", "X3"], "min": 3, "rol": "DOSYA"},
                "DOSYA_YD": {"ad": "DOSYA_Y + düşük kaldıraç", "uye": ["S7", "X1", "S5", "S6", "S4", "X2"], "min": 5, "rol": "DOSYA"}},
    "portfoy": {"dilim": 0.10},
    "cetvel": {"nw_lag": 6, "t_esik": 2.0, "alt_donem_n": 3, "alt_donem_min": 2, "son_pay": 0.30, "min_ay": 36},
    "karar": {"t_guclu": 2.8, "buyukluk_yillik": 0.04, "aday_evren": ["U1", "U2"], "bilesik": "COMP4",
              "dosya": ["DOSYA_Y", "DOSYA_D", "DOSYA_YD"], "t_guclu_dosya": 2.9},
    "ucuzluk": {"bilesik": "COMP4", "dilim": 0.20, "bol": "S9"},
    "plasebo": {"evren": "U2", "n": 200, "tohum": 59000, "yp_esik": 0.05},
    "french": {"faktor": ["MKT_RF", "SMB", "HML", "RMW", "CMA", "UMD"], "rf": "RF"},
    "sonraki": {"a": "yalnız küçük-orta hisseler (her ay uygun evrenin boyut medyanının altı), aynı sinyaller ve cetvel",
                "b": "3 ay tutma, örtüşen portföyler (her ay üçte biri yenilenir), aynı sinyaller ve cetvel",
                "c": "French veri kütüphanesinde 2000-2026 momentum + kârlılık bileşiğinin yinelemesi (hayatta kalma yanlılığı yok)"},
}
# Ön kaydın ilk yazımı (ölçümden önce genişletildi; metne girer, mühre girmez)
K59_ONCEKI = {"zaman": "2026-11-11 05:28:28 UTC", "muhur": "6f4aca9fd2e26afe3caae6c0675d588cba017c9203ac17fddf2354234b169fa1",
              "dosya_sha256": "df5663675e7d02e38cedad652408596bfdb3401f602f3712bcb58675b7952e44", "git": "d1a2dff"}
# Faz 1 kapsam sayımı (`python -I K59.py kapsam`; yalnız hisse SAYILARI, getiri yok). Ön kayıt metnine girer; mühre girmez (eşik değil).
K59_KAPSAM_NOTU = """Faz 1 kapsam sayımı (11 Kas 2026, yalnız hisse sayıları; getiri hesaplanmadı):
  U1: 1.411 hisse, 123 oluşum ayı (2016-05-31 .. 2026-07-31), uygun evren ortalama 1.084 (799-1.406). S1, S2, S3, S8, S9 2016'dan (122-123 ay);
      S7 2020-12'den (68 ay), S4 / S5 / COMP4 2021-02'den (66 ay), S6 2022-02'den (54 ay). S3 her ay işlem değeri. COMP9 2021 öncesi beş fiyat
      sinyalinin ortalamasıdır (bileşimi zamanla değişir; bilgi).
  U2: 4.261 hisse (1.151'inde 2020-26 arasında bölünme / ters bölünme var), 68 oluşum ayı (2020-12-31 .. 2026-07-31), uygun evren ortalama 2.146
      (1.916-2.477). S1 2021-01'den (67 ay), S4 / S5 / COMP4 2021-02'den (66 ay), S6 2022-02'den (54 ay), ötekiler 68 ay. S3: ilk 3 ay işlem
      değeri, sonraki 65 ay piyasa değeri. COMP4 2022-02'ye kadar üç üyeyle (S1, S4, S5) kurulur (S6 henüz yok).
  BIST: 581 hisse, 123 oluşum ayı, uygun evren ortalama 423 (357-581).
  DOSYA ailesi (ikinci kapsam sayımı, yine yalnız hisse sayıları): X1 2021-04'ten (bir yıl önceki çeyrek 2020'de başlar), X2 U1'de 2020-06'dan,
      U2'de 2020-12'den. DOSYA_Y / DOSYA_D / DOSYA_YD iki evrende de 2021-04-30'dan (64 ay); sinyali olan uygun hisse ortalaması U1'de
      867 / 822 / 795, U2'de 1.710 / 1.669 / 1.614. BIST'te X1 / X2 ve DOSYA yok. UCUZLUK COMP4 ile aynı 66 ay. İlk sayımdaki sütunlar değişmedi."""
K59_DOSYA = {"onkayit": "K59_ON_KAYIT.md", "sonuc": "sinyal_sonuc.csv", "aylik": "aylik_getiri.csv", "plasebo": "plasebo.csv",
             "kapsam": "kapsam.csv", "ucuzluk": "ucuzluk.csv", "saglama": "bagimsiz_saglama.csv", "rapor": "K59_RAPOR.md", "meta": "k59_kos_meta.json"}
_K59_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")


class K59Hata(RuntimeError):
    """K59'a özgü durdurucu hata (ön kayıt yok / değişmiş / git'e işlenmemiş, veri yok ya da ön kayıttakinden farklı)."""


def _k59_bagimli() -> Dict[str, Any]:
    """Mühre giren dış tanımlar (içe alınan K57 / K57-B / K58-B / FON_IZI kuralları); ortam yolu taşıyan 'klasor' anahtarları hariç."""
    return {"K57_ESIK": K57.K57_ESIK, "K57B_ESIK": K57.K57B_ESIK, "K57_ABD_GELIR": list(K57.K57_ABD_GELIR), "K58_B": K58.K58_ESIK["B"],
            "FI_K28": {k: v for k, v in FI.FI_K28.items() if k != "klasor"}, "FI_K31": {k: v for k, v in FI.FI_K31.items() if k != "klasor"}}


def k59_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: K59_ESIK + içe alınan dış tanımlar birlikte; biri değişirse koşu durur."""
    s = json.dumps({"K59_ESIK": E or K59_ESIK, "bagimli": _k59_bagimli()}, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _k59_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K59_YOL["cikti"], K59_DOSYA[ad])


def _k59_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


_k59_yz, _k59_sy = K58._yz, K58._sy


# ---------------------------------------------------------------- 0) VERİ SHA256 + ÖN KAYIT
def _k59_klasor_sha(dosyalar: List[str]) -> str:
    """Bir dosya kümesinin tek özeti: ada göre sıralı 'ad:sha256' satırlarının sha256'sı."""
    h = hashlib.sha256()
    for y in sorted(dosyalar, key=os.path.basename):
        h.update(f"{os.path.basename(y)}:{K58._k58_dosya_sha(y)}\n".encode("utf-8"))
    return h.hexdigest()


def k59_veri_sha() -> Dict[str, Tuple[str, int]]:
    """Koşunun okuyacağı bütün veri dosyalarının sha256'sı: ad -> (sha256, dosya sayısı). Olmayan kaynak sözlükte yer almaz."""
    import glob
    out: Dict[str, Tuple[str, int]] = {}
    for a in ("V_ABD.pkl", "V_BIST.pkl"):
        y = os.path.join(K58.K58_YOL["veri"], a)
        if os.path.exists(y):
            out[a] = (K58._k58_dosya_sha(y), 1)
    for z in K58.K58_ESIK["B"]["zip"].values():
        y = os.path.join(K58.K58_YOL["french"], z)
        if os.path.exists(y):
            out[z] = (K58._k58_dosya_sha(y), 1)
    fr = sorted({y for y in (K57._k57_frame_yol(t, d) for t, d in K57.k57_sec_listesi()) if y})
    if fr:
        out["secframes"] = (_k59_klasor_sha(fr), len(fr))
    sf = sorted(glob.glob(os.path.join(K57.K57_YOL["secfs"], "fs_*.csv.gz")) + glob.glob(os.path.join(K57.K57_YOL["secfs"], "company_tickers.json")))
    if sf:
        out["secfs"] = (_k59_klasor_sha(sf), len(sf))
    yh = sorted(y for y in glob.glob(os.path.join(K57.K57B_YOL["fiyat"], "*.json")) if not os.path.basename(y).startswith("_"))
    if yh:
        out["k57b_fiyat"] = (_k59_klasor_sha(yh), len(yh))
    y = os.path.join(K57.K57_YOL["onbellek"], "pead", "liste_abd.csv.gz")
    if os.path.exists(y):
        out["liste_abd.csv.gz"] = (K58._k58_dosya_sha(y), 1)
    return out


def k59_onkayit_metin(zaman: str, veri_sha: Dict[str, Tuple[str, int]]) -> str:
    E = K59_ESIK; ev = E["evren"]; Sg = E["sinyal"]; C = E["cetvel"]; Kr = E["karar"]; Pl = E["plasebo"]; uy = E["uygunluk"]
    B4, B9 = E["bilesik"]["COMP4"], E["bilesik"]["COMP9"]; K57E = K57.K57_ESIK; Y = K57.K57B_ESIK["yahoo"]
    Bl = E["bilesik"]; Xb = E["ek_bilesen"]; Uc = E["ucuzluk"]; On = K59_ONCEKI
    vs = "\n".join(f"- {k}: sha256 {v[0]} ({v[1]} dosya)" for k, v in veri_sha.items()) or "- (veri dosyası bulunamadı)"
    return f"""# K59 ÖN KAYIT — basit sinyaller, portföy cetveli v2 (aylık, geniş evren)

Yazım zamanı: {zaman} (ölçümden ÖNCE; gerçek veride hiçbir sinyal portföyü getirisi hesaplanmadı, sonuç görülmedi). Sürüm: {K59_SURUM}
ESIK_SHA256: {k59_esik_sha()}
(K59_ESIK + içe alınan K57_ESIK / K57B_ESIK / K58 B / FI_K28 / FI_K31 tanımlarının sha256'sı. `python -I K59.py kos` bu mühürle, aşağıdaki
veri sha256'larıyla ve bu dosya git'e işlenmiş, sonradan değişmemişse başlar; biri tutmazsa koşu durur.)

## Veri (sha256; koşu başında yeniden hesaplanır)
{vs}
Klasör özeti = ada göre sıralı 'dosya adı:sha256' satırlarının sha256'sı. SEC'e istek atılmaz; frames önbelleği yoksa koşu durur.

## 0. Soru ve önceden bilinenler
Yol haritası (11 Kas) Y1: ~150 çalışmada şart ekleyip daralttık (n küçüldü, olay cetveli kördü). Burada tersi: nedeni bilinen, basit,
SÜREKLİ sinyaller her ay binlerce hissede sıralanır; ölçüm portföy düzeyinde, aylık, maliyetli, beta düzeltmeli.
Bu ön kayıttan ÖNCE görülmüş ilgili sonuçlar (kör olmayan kısım): K58 C1 = V_ABD'de 12-1 momentum, K58 evreniyle (fiyat / likidite tabanı
yok) net yıllık fazla +%8,5, NW t 2,10, K58 C 'TUTAR'. Bu yüzden S1 / U1 kör değildir (evren süzgeci ve alfa şartı yeni). Öteki sinyaller
ve bileşikler bu evrenlerde portföy olarak hiç ölçülmedi; K57 / B / C bilanço tepkisini olay cetveliyle (FI_OLCUT) ölçtü, İZ DEĞİL çıktı.
Faz 1'de gerçek veride yalnız `kapsam` komutu koşuldu (hisse / ay / sinyal başına hisse SAYISI); getiri, fazla, t hesaplanmadı.
SÜRÜM NOTU: bu, ön kaydın İKİNCİ yazımıdır. İlk yazım ({On['zaman']}; mühür {On['muhur']}; dosya sha256
{On['dosya_sha256']}; git {On['git']}) hiçbir ölçüm yapılmadan, ana oturumun ek işiyle (Cemal'in isteği: 'YEOTK ve DGXX'i
seçtiren mantık geçmişte sınansın; eski cetvelle tutmadı denenler çöpe atılmasın') genişletildi: DOSYA ailesi (§2, §4.6) ve UCUZLUK koşullu
testi (§5b) EKLENDİ. İlk yazımdaki hiçbir eşik, tanım, evren ya da karar kuralı değişmedi.

## 1. Evrenler (ABD = karar, BIST = bilgi)
- U1: {ev['U1']['ad']}. Oluşum ayları ay sonu >= {ev['U1']['bas']}, fiyat {ev['U1']['kes']}'de kesik (K58 C ile aynı kriz kesiği).
- U2: {ev['U2']['ad']}. Üyelik = SEC frames'te gelir + net kâr + özkaynak etiketi ve borsa kodu olan CIK (K57 k57b_evren), Yahoo türü
  EQUITY, en az {K57.K57B_ESIK['evren']['min_gun']} gün fiyat (K57 k57b_fiyat_genis). Fiyatlar {Y['bas']} .. {Y['kes']}; en az {ev['U2']['min_hisse']} hisse yüklenemezse koşu durur.
- BIST: {ev['BIST']['ad']}, kriz kesiği {ev['BIST']['kes']}, maliyet tek yön {ev['BIST']['maliyet'] * 1e4:.0f} bp; yalnız fiyat / hacim sinyalleri
  ({', '.join(ev['BIST']['sinyal'])}) ve bunların ortalaması (COMP9, 5 üye). Karar rolü yok.
- Ay sonu = panel takviminin her aydaki son işlem günü (K58 k58_aylik). Ay getirisi (k -> k+1) = sonraki ay sonu kapanışı (ileri taşımalı)
  / ay sonu kapanışı - 1; fiyatlar temettü / bölünme düzeltmeli. Son oluşum ayı kesikten önceki ay sonu.
- UYGUNLUK (her ay sonu t, yalnız t ve öncesi bilgi): (1) t'ye kadar en az {uy['gecmis_gun']} günlük kapanış; (2) ABD: o günkü fiyat >= {ev['U1']['fiyat_min']:g} $;
  (3) ABD: son {uy['likit_gun']} işlem gününün (en az {uy['likit_min_gun']} gözlem) medyan işlem değeri (kapanış x hacim) >= {ev['U1']['likit_min'] / 1e6:g} milyon $;
  (4) ay sonu k ve k-1 kapanışı var (en çok {uy['ileri_tasima']} gün ileri taşıma). BIST'te (2) ve (3) yok (TL eşiği zamanla anlamını yitirir).
  'O günkü fiyat': U2'de Yahoo HAM kapanışı (bölünme düzeltmeli, temettüsüz) x t'den SONRAKİ bölünmelerin çarpımı = o gün işlem gören fiyat
  (sonradan ters bölünen kuruşluk hisse tabanı geçemez); işlem değeri de ham kapanışla. U1'de (V_ABD'de bölünme kaydı ve ham fiyat yok)
  düzeltilmiş kapanış kullanılır: sonradan ters bölünen hisse olduğundan pahalı, sonradan bölünen / temettü ödeyen ucuz görünür (yanlılık).
  U2 sınırı: Yahoo kapanışı indirme gününe (9 Kas 2026) kadarki bölünmelere göre düzeltilmiştir, bölünme kaydı ise {Y['bit']}'de biter; bu
  arada bölünen az sayıda hissede o günkü fiyat ve piyasa değeri bölünme oranı kadar sapar.
  Uygun hisse sayısı < {ev['U1']['min_evren']} (BIST {ev['BIST']['min_evren']}) olan ay atlanır.
- HAYATTA KALMA YANLILIĞI: üç evren de yalnız BUGÜN işlem gören hisselerdir. Batan / borsadan çıkan hisseler yok; bu, kaybedenleri taşıyan
  sinyalleri (dönüş S2, küçüklük S3) olduğundan iyi, düşük oynaklık / kârlılık gibi 'kaliteli' sinyalleri olduğundan kötü gösterebilir.
  Kıyas (eşit ağırlıklı evren) aynı yanlılığı taşır, fark kısmen silinir ama sıfır değildir. Yanlılıksız kontrol sıradaki deneme (c).
- U1 ve U2 BAĞIMSIZ DEĞİL: U1'in ~1.100 hissesi U2'de de var ve temel veri (aşağıda) 2020'de başladığı için S4-S7 ve COMP4 iki evrende de
  aynı 2021-2026 dönemini ölçer. 'İki evrende tutar' bağımsız yineleme değil, evren genişliğine dayanıklılıktır.

## 2. Sinyaller (ay sonu t'de yalnız t ve öncesi bilgi; her sinyalde 'yüksek = iyi' yönü)
Temel veri: SEC XBRL frames önbelleği (K57 k57_abd_temel_tablo; çeyrekler {K57E['sec_ceyrek'][0]} .. {K57E['sec_ceyrek'][1]}, 4. çeyrek yıllıktan türetilir).
BİLGİ TARİHİ = o çeyreğin ilk 10-Q / 10-K başvurusunun SEC 'filed' günü (dönem sonu ±10 gün eşleşen, K57 _k57_abd_bilgi_tarihleri, Nasdaq
takvimi VERİLMEDEN: basın açıklaması günü kullanılmaz); başvuru özütlerde yoksa (2021 öncesi başvurular) çeyrek sonu + {K57E['bilgi_yedek_gun']} gün.
Bir çeyrek ancak bilgi tarihi <= t ise kullanılır; en son bilinen çeyreğin sonu t'den en çok {E['temel_max_gun']} gün önce olmalı (bayat veri yok).
Sınır: frames değerleri şirketin EN SON bildirdiği değerdir (sonradan düzeltilmiş olabilir); tarih özgün başvuru günüdür.
- S1 {Sg['S1']['ad']}: kapanış(k-{Sg['S1']['kisa']}) / kapanış(k-{Sg['S1']['uzun']}) - 1 (ay sonları; K58 k58_sinyal_momentum). Yüksek iyi.
- S2 {Sg['S2']['ad']}: -(kapanış(k) / kapanış(k-1) - 1). En çok düşen iyi.
- S3 {Sg['S3']['ad']}: U2'de piyasa değeri = o günkü fiyat x pay sayısı (SEC finansal özütleri, FON_IZI fi_k31_finansal; başvuru 'filed' <= t,
  pay tarihi t'den en çok {E['temel_max_gun']} gün önce; pay tarihinden sonraki bölünmelerle düzeltilir). Bir ayda uygun hisselerin en az
  %{Sg['S3']['pay_kapsam_min'] * 100:.0f}'sinin pay sayısı varsa o ay piyasa değeri kullanılır (payı olmayan hisse S3'e girmez); yoksa o ay 20 günlük medyan işlem
  değeri. U1 ve BIST'te HER AY 20 günlük medyan işlem değeri (V_ABD'de bölünme kaydı yok: düzeltilmiş fiyat x eski pay sayısı, sonradan
  bölünen = iyi giden hisseyi küçük gösterir, geleceğe bakma olur). En küçük iyi. Hangi ay hangi ölçü: kapsam.csv 'S3_olcu'.
- S4 {Sg['S4']['ad']}: K57 k57_olay_abd olayları (Nasdaq bilanço takvimi {K57E['nasdaq_bas']} sonrası; öncesinde {K57E['abd_bas']}'den itibaren SEC 10-Q / 10-K
  başvuru günü). 'ear' = açıklama gününden önceki son kapanıştan sonraki ilk kapanışa getiri - aynı pencerede evren medyanı (FON_IZI
  fi_k28_olaylar). Tepki penceresi t'ye kadar bitmiş ve son {Sg['S4']['pencere_gun']} işlem günü içinde olan EN SON olayın 'ear'ı. Olayı olmayan hisse S4'e
  girmez; üst %10 olayı olanlar arasındadır. Yüksek iyi. Sınır: 2021-22'de olay günü başvuru günüdür (basın açıklamasından sonra olabilir).
- S5 {Sg['S5']['ad']}: NetIncomeLoss son {Sg['S5']['ceyrek']} çeyrek toplamı / StockholdersEquity (en son bilinen çeyrek sonu); özkaynak > 0 şart. Yüksek iyi.
- S6 {Sg['S6']['ad']}: en son başvurunun ('filed' <= t) yıllık pay değişimi (fi_k31_finansal pay_yil: {FI.FI_K31['yil_min']}-{FI.FI_K31['yil_max']} gün önceki paya oran).
  Bölünme K57 F4 gibi: oran (1 + değişim) bir tamsayıya (>= 2) ±%{K57E['F4_bolunme_tol'] * 100:.0f} yakınsa bölünme, değişim = oran / tamsayı - 1. EK (F4'te gerekmiyordu):
  ters bölünme aynı kuralla (1 / oran tamsayıya yakınsa değişim = oran x tamsayı - 1); yoksa ters bölünme dev geri alım gibi görünür.
  Oran > {Sg['S6']['aykiri_kat']:g} ya da < 1/{Sg['S6']['aykiri_kat']:g} ise veri YOK sayılır. En düşük değişim iyi.
- S7 {Sg['S7']['ad']}: gelir (K57 etiket sırası: {', '.join(K57.K57_ABD_GELIR)}; üç çeyreği de olan ilk etiket)
  son çeyrek / önceki iki çeyreğin ortalaması; ortalama > 0 şart. Yüksek iyi.
- S8 {Sg['S8']['ad']}: -(son {Sg['S8']['gun']} işlem gününün günlük getiri standart sapması; en az {Sg['S8']['min_gun']} gözlem). En düşük iyi.
- S9 {Sg['S9']['ad']}: ay sonu kapanışı / son {Sg['S9']['gun']} işlem gününün en yüksek gün içi fiyatı (en az {Sg['S9']['min_gun']} gözlem). Yüksek iyi.
- COMP4 (KARAR; önceden yazıldı, seçim yok): {', '.join(B4['uye'])} sinyallerinin ay içi yüzdelik sıralarının ((sıra - 0,5) / n; uygun ve o sinyali
  olan hisseler arasında, eşitlikte ortalama sıra) ortalaması; hissenin dördün en az {B4['min']}'ünde değeri olmalı. Üst %10.
- COMP9 (BİLGİ): dokuz sinyalin sıra ortalaması; en az {B9['min']} sinyal. (BIST'te beş fiyat / hacim sinyali.)
- EK BİLEŞENLER (yalnız DOSYA bileşiklerinin üyesidir; tek başına portföy olarak ÖLÇÜLMEZ, ek deneme sayılmaz):
  X1 {Xb['X1']['ad']}: gelir (S7 ile aynı etiket sırası; iki çeyreği de olan ilk etiket);
  ikisi de > 0 ve ikisinin de bilgi tarihi <= t (K57 F1 'satis_yoy' tanımı). Yüksek iyi.
  X2 {Xb['X2']['ad']}: -(yükümlülük / özkaynak), en son bilinen çeyrek sonu; özkaynak > 0 şart; Liabilities
  yoksa LiabilitiesAndStockholdersEquity - özkaynak (K57 F3 gibi); yükümlülük < 0 ise veri yok.
  X3 {Xb['X3']['ad']}: -S9, yani kapanış / 252 gün zirvesi DÜŞÜK olan iyi.
- DOSYA AİLESİ (KENDİ BAŞINA TUTAR / TUTMAZ; ölçümden önce yazıldı, seçim yok; sıra ortalaması COMP4 ile aynı yöntem, üst %10):
  DOSYA_Y ({Bl['DOSYA_Y']['ad']}): {', '.join(Bl['DOSYA_Y']['uye'])} (gelir ivmesi, gelir yıllık büyümesi, kârlılık, düşük ihraç, PEAD);
  hissenin beşin en az {Bl['DOSYA_Y']['min']}'ünde değeri olmalı.
  DOSYA_D ({Bl['DOSYA_D']['ad']}): {', '.join(Bl['DOSYA_D']['uye'])} (düşük kaldıraç, gelir yıllık büyümesi, zirveden
  uzaklık); üçün {Bl['DOSYA_D']['min']}'ü de olmalı. NOT: gerçek DGXX seçiminde belirleyici olan 'SEC'e ekli bağlayıcı sözleşme' yapısal veride YOK (8-K madde 1.01
  verisi K60'ta); DOSYA_D yalnız ölçülebilir kısmın VEKİLİDİR. Tutmaması DGXX mantığını çürütmez, tutması da sözleşme şartını kanıtlamaz.
  DOSYA_YD ({Bl['DOSYA_YD']['ad']}): {', '.join(Bl['DOSYA_YD']['uye'])}; altının en az {Bl['DOSYA_YD']['min']}'i olmalı.
  BIST: bu çalışmada BIST temel verisi yüklenmez; DOSYA bileşikleri BIST'te ÖLÇÜLMEZ (yalnız U1 ve U2). BIST ölçümü ayrı iş olur.
KAPSAM (veriden ötürü, sonuçtan bağımsız): temel veri 2020'de başlar; pay sayısı özütleri 2021'de başlar, yıllık değişim bir yıl ister.
Bir sinyalin ölçüm dönemi = o sinyali olan uygun hisse sayısının ilk kez >= {ev['U1']['min_sinyal']} (BIST {ev['BIST']['min_sinyal']}) olduğu aydan sona.
{K59_KAPSAM_NOTU}

## 3. Portföy ve cetvel v2
- Portföy: sinyali olan uygun hisselerin en üst %{E['portfoy']['dilim'] * 100:.0f}'u (sayı = max(1, yuvarla(0,10 x sinyali olan uygun hisse)); eşitlikte kod sırası),
  eşit ağırlık, aylık yeniden dengeleme, ay sonu kapanışında işlem (K58 k58_ust_dilim / k58_portfoy). Maliyet tek yön ABD {ev['U1']['maliyet'] * 1e4:.0f} bp,
  BIST {ev['BIST']['maliyet'] * 1e4:.0f} bp x devir (devir = Σ|w_yeni - w_kaymış|, ilk ay 1). Kıyas = BÜTÜN uygun evrenin eşit ağırlıklı getirisi (maliyetsiz).
  Aykırı getiri kırpması yok (K58 C ile aynı).
- CETVEL v2 TUTAR ⇔ dört şart birden, MALİYETTEN SONRA:
  (1) aylık fazla e = net portföy - kıyas: ortalama > 0 ve Newey-West (gecikme {C['nw_lag']}) t > {C['t_esik']};
  (2) ayların ardışık eşit {C['alt_donem_n']} parçasının en az {C['alt_donem_min']}'sinde ortalama e > 0;
  (3) son %{C['son_pay'] * 100:.0f} ayda (yukarı yuvarlanmış) ortalama e > 0;
  (4) BETA DÜZELTMELİ ALFA: net portföy getirisi = alfa + beta x kıyas getirisi + hata (sabitli EKK); alfa > 0 ve Newey-West (gecikme {C['nw_lag']},
      Bartlett, serbestlik düzeltmesi yok) t(alfa) > {C['t_esik']}.
  Ölçüm ayı < {C['min_ay']} ise 'ÖLÇÜLEMEDİ' (tutar sayılmaz).
- BİLGİ (karar rolü yok): FF5 + UMD alfası (net portföy - RF'nin MKT-RF, SMB, HML, RMW, CMA, UMD üzerine sabitli EKK'si; French dosyaları K58
  ile aynı, RF 5 faktör dosyasından; ortak aylar), yıllık fazla (12 x ortalama e), Sharpe ((portföy - RF) ort / sd x √12), en büyük düşüş,
  aylık devir, ortalama hisse sayısı ve aynı istatistiklerin maliyetsiz (brüt) hali. BIST'te French alfası yok, Sharpe'ta rf = 0.

## 4. Karar kuralları (şimdi yazıldı; sonuçtan sonra değişmez)
1. Bir sinyal bir evrende TUTAR ⇔ cetvel v2'nin dört şartı maliyetten sonra sağlanır. Etiket: 'TUTAR (yineleme)' (t > {C['t_esik']}; bilinen etkinin
   yinelemesi eşiği); hem NW t(fazla) hem t(alfa) > {Kr['t_guclu']} ise 'GÜÇLÜ' (dokuz tekil sinyal için Bonferroni'ye dayanıklı). Aksi 'TUTMAZ'.
2. PORTFÖY-ADAY ⇔ {Kr['bilesik']} hem U1 hem U2'de TUTAR VE iki evrende de net yıllık fazla >= +{Kr['buyukluk_yillik'] * 100:.0f} puan. İkisinde tutar ama birinde
   yıllık fazla < +{Kr['buyukluk_yillik'] * 100:.0f} puan ise 'TUTAR AMA KÜÇÜK'. Birinde tutmazsa 'TUTMAZ'. Tekil sinyallerde yıllık fazla < +{Kr['buyukluk_yillik'] * 100:.0f} puan 'küçük' diye işaretlenir.
3. İZ ilan EDİLEMEZ: CLAUDE.md standardı (FI_OLCUT, ABD + Avrupa) değişmedi ve Avrupa'da temel veri yok. Standart değişikliği Cemal'in kararı.
4. Seçim yok: karar yalnız COMP4'e bakar. Tekil sinyaller ve COMP9 bilgi içindir; 'en iyi tutan sinyali seçip' yeni bileşik kurulmaz.
5. BIST bilgi olarak raporlanır; karara girmez.
6. DOSYA AİLESİ: {', '.join(Kr['dosya'])} her evrende kendi başına cetvel v2 ile 'TUTAR (yineleme)' / 'TUTMAZ' etiketi alır ve ayrı aile
   olarak raporlanır ('küçük' işareti aynı: net yıllık fazla < +{Kr['buyukluk_yillik'] * 100:.0f} puan). Çoklu deneme: dokuz tekil sinyale 3 ek deneme (toplam 12) sayılır;
   DOSYA'da 'GÜÇLÜ' eşiği iki t de > {Kr['t_guclu_dosya']} (12 deneme için Bonferroni; tekil sinyallerin {Kr['t_guclu']} eşiği değişmedi). PORTFÖY-ADAY kararı
   yine YALNIZ COMP4'e bağlıdır; DOSYA sonucu o kararı değiştirmez, DOSYA için 'aday' etiketi yoktur ve İZ ilan edilemez (madde 3).

## 5. Plasebo (cetvelin kendisinin sınaması)
{Pl['evren']}'de {Pl['n']} rastgele sinyal (her ay uygun hisselere rastgele sıra; numpy default_rng({Pl['tohum']} + i)), aynı üst %10 portföyü ve cetvel v2.
Yanlış pozitif oranı = TUTAN payı; hem maliyetli hem maliyetsiz (brüt) cetvelle hesaplanır, İKİSİ de <= %{Pl['yp_esik'] * 100:.0f} olmalı (maliyet yüksek devirli
rastgele portföyü zaten cezalandırır; brüt oran sert olanıdır). Biri > %{Pl['yp_esik'] * 100:.0f} ise cetvel v2 GÜVENİLMEZ ilan edilir ve hiçbir sinyal için hüküm verilmez.

## 5b. Koşullu test 'UCUZLUK' (BİLGİ; karar yok)
K57'de 'tepeden düşmüş' şartı (F6) eklenince sonuç bozulmuştu (olay cetveli, küçük n); güçlü cetvelle yeniden bakılır. U1 ve U2'de her ay
{Uc['bilesik']} sırasının üst %{Uc['dilim'] * 100:.0f}'si (sayı = max(1, yuvarla(0,20 x {Uc['bilesik']}'ü olan uygun hisse))) {Uc['bol']}'a göre ikiye bölünür: 'düşmüş yarı' = {Uc['bol']}'u en düşük
yarı, 'zirveye yakın yarı' = en yüksek yarı (tek sayıda ortadaki hisse iki portföyün de dışında). İkisi de eşit ağırlıklı, aylık dengelenen,
aynı maliyetli UZUN portföydür; ölçüm dönemi {Uc['bilesik']}'ünkiyle aynı. Raporlanır: her birinin evrene göre net fazlası, NW t, alfa ve t(alfa); ve
aylık net fark (düşmüş - zirveye yakın; uzun-kısa değil, iki uzun portföyün farkı) ile NW t'si (gecikme {C['nw_lag']}). Karar kuralı ve etiket YOK.

## 6. COMP4 tutmazsa önceden yazılı sıradaki üç deneme (Faz 2'de KOŞULMAZ; ana oturum karar verir)
- (a) {E['sonraki']['a']}.
- (b) {E['sonraki']['b']}.
- (c) {E['sonraki']['c']}.

## 7. Değişmezlik
Yukarıdaki bütün eşikler, tanımlar ve evren kuralları sabittir; sonuç görüldükten sonra değiştirilmez. Kod hatası düzeltmesi gerekirse ön
kayıt değişmez, düzeltme raporda ayrıca yazılır.

## 8. Faz 2 komutu (bu dosya git'e işlendikten SONRA)
`cd /home/user/col_yolu && python -I K59.py kos`
"""


def _k59_onkayit_oku(yol: str) -> Dict[str, Any]:
    with open(yol, encoding="utf-8") as f:
        metin = f.read()
    m = re.search(r"^ESIK_SHA256: ([0-9a-f]{64})$", metin, re.M)
    z = re.search(r"^Yazım zamanı: (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC", metin, re.M)
    veri = {a: (h, int(n)) for a, h, n in re.findall(r"^- ([\w.\-]+): sha256 ([0-9a-f]{64}) \((\d+) dosya\)$", metin, re.M)}
    return {"sha": m.group(1) if m else None, "zaman_utc": z.group(1) if z else "", "veri": veri}


def k59_onkayit(cikti: Optional[str] = None, veri_sha: Optional[Dict[str, Tuple[str, int]]] = None) -> str:
    """Ön kaydı yazar. Dosya varsa ÜZERİNE YAZMAZ: mühür aynıysa yolu döndürür, değilse durur. veri_sha None ise veri özetleri hesaplanır."""
    yol = _k59_yol("onkayit", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True)
    if os.path.exists(yol):
        mevcut = _k59_onkayit_oku(yol)["sha"]
        if mevcut != k59_esik_sha():
            raise K59Hata(f"ön kayıt zaten var ve mühür farklı ({mevcut} != {k59_esik_sha()}): eşikler ön kayıttan sonra değişmiş")
        k59log.info("ön kayıt zaten var (mühür aynı): %s", yol)
        return yol
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    with open(yol, "w", encoding="utf-8") as f:
        f.write(k59_onkayit_metin(zaman, k59_veri_sha() if veri_sha is None else veri_sha))
    k59log.info("ön kayıt yazıldı: %s (mühür %s)", yol, k59_esik_sha()[:12])
    return yol


def _k59_git_islenmis(yol: str) -> Dict[str, str]:
    """Ön kayıt dosyası git'e işlenmiş ve işlendikten sonra değişmemiş olmalı (ön kayıt ölçümden önce: git zamanı + mühür)."""
    kl, ad = os.path.dirname(os.path.abspath(yol)), os.path.basename(yol)
    try:
        r = subprocess.run(["git", "-C", kl, "log", "-1", "--format=%H %cI", "--", ad], capture_output=True, text=True, timeout=60)
        d = subprocess.run(["git", "-C", kl, "status", "--porcelain", "--", ad], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as ex:
        raise K59Hata(f"git çalıştırılamadı ({ex}): ön kaydın işlendiği doğrulanamadı, koşu durdu")
    if r.returncode != 0 or not r.stdout.strip():
        raise K59Hata(f"ön kayıt git'e işlenmemiş ({yol}): önce ana oturum denetleyip commit eder, sonra `kos`")
    if d.returncode != 0 or d.stdout.strip():
        raise K59Hata(f"ön kayıt git'e işlendikten sonra değişmiş ({d.stdout.strip() or d.stderr.strip()}): koşu durdu")
    h, z = r.stdout.strip().split(" ", 1)
    return {"commit": h, "commit_zamani": z}


def k59_onkayit_dogrula(cikti: Optional[str] = None, veri: bool = False, git: bool = False) -> Dict[str, Any]:
    """Mühür (her zaman), veri sha256'ları (veri=True) ve git'e işlenmişlik (git=True) doğrulanır; biri tutmazsa K59Hata."""
    yol = _k59_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise K59Hata(f"ön kayıt yok ({yol}): önce `python K59.py onkayit`")
    oc = _k59_onkayit_oku(yol)
    if oc["sha"] != k59_esik_sha():
        raise K59Hata(f"ön kayıt mührü tutmuyor ({oc['sha']} != {k59_esik_sha()}): eşikler ön kayıttan sonra değişmiş, koşu durdu")
    out = {"yol": yol, "sha": oc["sha"], "zaman_utc": oc["zaman_utc"], "dosya_sha256": K58._k58_dosya_sha(yol), "veri": oc["veri"]}
    if veri:
        simdi = k59_veri_sha()
        fark = sorted(k for k in set(simdi) | set(oc["veri"]) if simdi.get(k) != oc["veri"].get(k))
        if fark:
            raise K59Hata(f"veri ön kayıttakiyle aynı değil (sha256 / dosya sayısı farklı ya da eksik): {fark}; koşu durdu")
    if git:
        out["git"] = _k59_git_islenmis(yol)
    return out


# ---------------------------------------------------------------- 1) VERİ DEMETLERİ
def k59_yahoo_ham(yol: str, kes: str) -> Tuple[Optional[pd.Series], Optional[Tuple[np.ndarray, np.ndarray]]]:
    """K57-B Yahoo önbellek JSON'undan HAM kapanış (bölünme düzeltmeli, temettüsüz) ve bölünmeler (tarih, oran = pay / payda).
    K57 k57b_yahoo_oku düzeltilmiş OHLCV verir; o günkü fiyat ve piyasa değeri için ham seri ayrıca gerekir. Yalnız json ile okunur."""
    try:
        with open(yol, encoding="utf-8") as f:
            J = json.load(f)
    except (OSError, ValueError):
        return None, None
    res = ((J.get("chart") or {}).get("result") or [None])[0] if isinstance(J, dict) else None
    if not res or not res.get("timestamp"):
        return None, None
    tz = (res.get("meta") or {}).get("exchangeTimezoneName") or "America/New_York"

    def gun(ts: Any) -> pd.DatetimeIndex:
        return pd.to_datetime(ts, unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()
    q = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    c = pd.Series(q.get("close"), index=gun(res["timestamp"]), dtype=float)
    c = c[~c.index.duplicated(keep="last")].sort_index()
    c = c[(c > 0) & (c.index <= pd.Timestamp(kes))]
    bol = []
    for v in ((res.get("events") or {}).get("splits") or {}).values():
        try:
            pay, payda, t = float(v["numerator"]), float(v["denominator"]), int(v["date"])
        except (KeyError, TypeError, ValueError):
            continue
        if pay > 0 and payda > 0 and pay != payda:
            bol.append((gun([t])[0].to_datetime64().astype("datetime64[ns]"), pay / payda))
    bol.sort(key=lambda x: x[0])
    b = (np.array([x[0] for x in bol], "datetime64[ns]"), np.array([x[1] for x in bol], float)) if bol else None
    return (c if len(c) else None), b


def k59_bolunme_carpan(bol: Optional[Tuple[np.ndarray, np.ndarray]], t: np.ndarray) -> np.ndarray:
    """Her t için, tarihi t'den SONRA olan bölünme oranlarının çarpımı (bölünme yoksa 1). Ham Yahoo kapanışı x çarpan = o günkü fiyat."""
    t = np.asarray(t, "datetime64[ns]"); out = np.ones(t.shape)
    if bol is None or not len(bol[0]):
        return out
    d, r = bol
    sonek = np.r_[np.cumprod(r[::-1])[::-1], 1.0]
    gec = ~np.isnat(t)
    out[gec] = sonek[np.searchsorted(d, t[gec], side="right")]
    return out


def k59_abd_ortak() -> Dict[str, Any]:
    """U1 ve U2'nin ortak ABD verisi: SEC frames (temel), başvuru günleri (bilgi tarihi), Nasdaq takvimi, pay sayısı tablosu. SEC'e istek YOK."""
    T, neden = K57.k57_abd_temel_tablo()
    if T is None:
        raise K59Hata(f"{neden}. SEC frames önbelleği ({K57.K57_YOL['frames']}) eksik: K59 SEC'e istek atmaz (e-posta kullanılmaz), koşu durdu")
    secfs = K57._k57_secfs_klasor(); cik2s = K57.k57_cik_sembol(secfs); B = K57.k57_secfs_basvuru(secfs); N = K57.k57_nasdaq_liste()
    bos = pd.DataFrame({"sembol": pd.Series(dtype=str), "D": pd.Series(dtype="datetime64[ns]")})   # Nasdaq günü bilgi tarihi sayılmaz
    bilgi = K57._k57_abd_bilgi_tarihleri(T, bos, B, cik2s)
    F = FI.fi_k31_finansal(dict(FI.FI_K31, klasor=secfs))
    k59log.info("ABD ortak: %d (cik, çeyrek) bilgi tarihi, %d başvuru, %d pay satırı, %d takvim satırı", len(bilgi), len(B), len(F), len(N))
    return {"T": T, "bilgi": bilgi, "s2c": {v: k for k, v in cik2s.items()}, "cik2s": cik2s, "B": B, "N": N, "secfs": secfs, "pay": F}


def k59_demet(ad: str, ortak: Optional[Dict[str, Any]] = None, veri_sha: Optional[Dict[str, Tuple[str, int]]] = None) -> Dict[str, Any]:
    """Bir evrenin veri demeti: V (düzeltilmiş OHLCV), ham kapanış + bölünmeler (U2), olaylar, temel tablo, pay tablosu."""
    ev = K59_ESIK["evren"][ad]; vs = veri_sha or {}
    D: Dict[str, Any] = {"ad": ad, "evren": ev, "ham": None, "bolunme": None, "olay": None, "T": None, "bilgi": None, "s2c": None, "pay": None}
    if ev["kaynak"] == "V_BIST":
        D["V"] = K58.k58_fiyat("BIST", (vs.get("V_BIST.pkl") or (None,))[0])
        return D
    if ortak is None:
        raise K59Hata(f"{ad}: ABD ortak verisi verilmedi")
    if ev["kaynak"] == "V_ABD":
        D["V"] = K58.k58_fiyat("ABD", (vs.get("V_ABD.pkl") or (None,))[0])
    else:
        V, Ut = K57.k57b_fiyat_genis(K57.k57b_evren(ortak["T"], ortak["cik2s"]))
        if len(V) < ev["min_hisse"]:
            raise K59Hata(f"{ad}: K57-B Yahoo önbelleğinden {len(V)} hisse yüklendi (< {ev['min_hisse']}); önbellek {K57.K57B_YOL['fiyat']} eksik. "
                          "K57 k57b_yahoo_indir ile yeniden indirilir; veri sha256'ları değişeceği için ön kayıt ana oturumca yenilenir")
        seri, bol = {}, {}
        for s in V:
            c, b = k59_yahoo_ham(K57._k57b_dosya(s), ev["kes"])
            if c is not None:
                seri[s] = c
            if b is not None:
                bol[s] = b
        D.update({"V": V, "ham": pd.DataFrame(seri).sort_index(), "bolunme": bol})
        k59log.info("%s: %d hisse, ham kapanış %d, bölünmesi olan %d", ad, len(V), len(seri), len(bol))
    X = K57.k57_olay_abd(D["V"], ortak["N"], ortak["B"], ortak["cik2s"], ortak["secfs"])
    D.update({"olay": X[["sembol", "D", "tepki_son", "ear", "kaynak"]].copy(), "T": ortak["T"], "bilgi": ortak["bilgi"], "s2c": ortak["s2c"],
              "pay": ortak["pay"]})
    return D


# ---------------------------------------------------------------- 2) AYLIK PANEL + UYGUNLUK
def k59_panel(D: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """K58 k58_aylik (ay sonları, ay getirisi, kesik) + K59 uygunluğu (geçmiş, o günkü fiyat, işlem değeri). Yalnız t ve öncesi bilgi."""
    E = E or K59_ESIK; ev = D["evren"]; uy = E["uygunluk"]; V = D["V"]
    M = K58.k58_aylik(V, {"kriz": ev["kes"], "gecmis_ay": 1, "bas": ev["bas"], "min_evren": ev["min_evren"]})
    me, S, C5 = M["ay_sonu"], M["sembol"], M["C5"]; gun = C5.index; mp = gun.get_indexer(me)

    def cer(kol: str) -> pd.DataFrame:
        return pd.DataFrame({s: V[s][kol].astype(float) for s in S}).reindex(gun)
    Cd = cer("Close"); Cd = Cd.where(Cd > 0); Vol = cer("Volume"); Hi = cer("High")
    if D.get("ham") is not None:
        Ch = D["ham"].reindex(index=gun, columns=S); Ch = Ch.where(Ch > 0)
    else:
        Ch = Cd
    gecmis = np.asarray(Cd.notna().cumsum() >= uy["gecmis_gun"])[mp]
    tl = np.array((Ch * Vol).rolling(uy["likit_gun"], min_periods=uy["likit_min_gun"]).median().to_numpy(float)[mp], copy=True)
    ham_me = np.array(Ch.ffill(limit=uy["ileri_tasima"]).to_numpy(float)[mp], copy=True)
    carp = np.ones(ham_me.shape); bol = D.get("bolunme") or {}; mt = me.to_numpy("datetime64[ns]")
    for j, s in enumerate(S):
        if s in bol:
            carp[:, j] = k59_bolunme_carpan(bol[s], mt)
    fiyat_o = ham_me * carp
    uygun = gecmis & np.isfinite(fiyat_o)
    if ev.get("fiyat_min") is not None:
        uygun &= fiyat_o >= ev["fiyat_min"]
    if ev.get("likit_min") is not None:
        uygun &= np.nan_to_num(tl, nan=-1.0) >= ev["likit_min"]
    U = np.array(M["U"] & uygun, copy=True)
    ol = M["olusum"] & (U.sum(axis=1) >= ev["min_evren"])
    U[~ol] = False
    R = np.where(U, M["R"], np.nan)
    return {"ad": D["ad"], "evren": ev, "ay_sonu": me, "sembol": S, "gun": gun, "me_pos": mp, "U": U, "R": R, "olusum": ol, "Cm": M["Cm"],
            "C5": C5, "Hi": Hi, "tl_me": tl, "ham_me": ham_me if D.get("ham") is not None else None, "fiyat_o": fiyat_o}


# ---------------------------------------------------------------- 3) SİNYALLER
def k59_ihrac(pay_yil: np.ndarray, tol: float, aykiri: float) -> np.ndarray:
    """Yıllık pay değişimi -> net ihraç. Oran r = 1 + değişim bir tamsayıya (>= 2) ±tol yakınsa bölünme (r / k - 1); 1 / r tamsayıya yakınsa
    ters bölünme (r x k - 1); r > aykiri ya da r < 1 / aykiri ise veri yok (NaN)."""
    r = 1.0 + np.asarray(pay_yil, float)
    with np.errstate(invalid="ignore", divide="ignore"):
        k = np.round(r); ileri = (k >= 2) & (np.abs(r / k - 1) <= tol)
        kk = np.round(1.0 / r); geri = (kk >= 2) & (np.abs(r * kk - 1) <= tol)
        out = np.where(ileri, r / k - 1, np.where(geri, r * kk - 1, r - 1))
        gecerli = np.isfinite(r) & (r > 0) & (r <= aykiri) & (r >= 1.0 / aykiri)
    return np.where(gecerli, out, np.nan)


def k59_pay_tablo(F: pd.DataFrame, S: List[str], me: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """Her (ay sonu, hisse) için 'filed' <= t olan EN SON başvuru: pay sayısı, pay tarihi, net ihraç (bölünme kuralıyla), başvuru günü.
    Pay tarihi t'den temel_max_gun'den eskiyse (bayat) yok sayılır."""
    E = E or K59_ESIK; n, u = len(me), len(S); mt = me.to_numpy("datetime64[ns]"); kol = {s: j for j, s in enumerate(S)}
    pay = np.full((n, u), np.nan); ihr = np.full((n, u), np.nan)
    pt = np.full((n, u), np.datetime64("NaT"), "datetime64[ns]"); fl = np.full((n, u), np.datetime64("NaT"), "datetime64[ns]")
    G = F.dropna(subset=["filed", "sembol"]).sort_values(["sembol", "filed", "pay_t"], kind="mergesort")
    maxg = np.timedelta64(int(E["temel_max_gun"]), "D")
    for s, g in G.groupby("sembol", sort=False):
        j = kol.get(s)
        if j is None:
            continue
        f = g.filed.to_numpy("datetime64[ns]"); i = np.searchsorted(f, mt, side="right") - 1; ii = np.clip(i, 0, None)
        t_ = g.pay_t.to_numpy("datetime64[ns]")[ii]
        with np.errstate(invalid="ignore"):
            ok = (i >= 0) & ~np.isnat(t_) & (t_ <= mt) & (mt - t_ <= maxg)
        pay[ok, j] = g.pay.to_numpy(float)[ii][ok]; pt[ok, j] = t_[ok]; fl[ok, j] = f[ii][ok]
        ihr[ok, j] = k59_ihrac(g.pay_yil.to_numpy(float)[ii][ok], K57.K57_ESIK["F4_bolunme_tol"], E["sinyal"]["S6"]["aykiri_kat"])
    pay[~(pay > 0)] = np.nan
    return {"pay": pay, "pay_t": pt, "ihrac": ihr, "filed": fl}


def k59_pead_sinyal(olay: pd.DataFrame, S: List[str], gun: pd.DatetimeIndex, me_pos: np.ndarray, pencere: int) -> np.ndarray:
    """S4: tepki penceresi (tepki_son) ay sonu t'ye kadar bitmiş ve son `pencere` işlem günü içinde olan EN SON olayın 'ear'ı."""
    out = np.full((len(me_pos), len(S)), np.nan); kol = {s: j for j, s in enumerate(S)}
    X = olay.dropna(subset=["ear", "tepki_son", "sembol"])
    if not len(X):
        return out
    X = X.assign(_p=gun.get_indexer(pd.DatetimeIndex(pd.to_datetime(X.tepki_son))))
    X = X[X["_p"] >= 0].sort_values(["sembol", "_p"], kind="mergesort")
    for s, g in X.groupby("sembol", sort=False):
        j = kol.get(s)
        if j is None:
            continue
        p = g["_p"].to_numpy(); e = g.ear.to_numpy(float)
        i = np.searchsorted(p, me_pos, side="right") - 1; ii = np.clip(i, 0, None)
        ok = (i >= 0) & (p[ii] > me_pos - pencere)
        out[ok, j] = e[ii][ok]
    return out


def _k59_dt(x: Any) -> np.datetime64:
    return pd.Timestamp(x).to_datetime64().astype("datetime64[ns]")


def k59_temel_sinyal(T: Dict[str, Any], bilgi: Dict[Tuple[str, int], Any], s2c: Dict[str, str], S: List[str], me: pd.DatetimeIndex,
                     U: np.ndarray, E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """S5 (son 4 çeyrek net kâr / özkaynak), S7 (gelir son çeyrek / önceki iki çeyrek ortalaması), X1 (gelir son çeyrek / bir yıl önceki aynı
    çeyrek - 1; ikisi de > 0), X2 (-(yükümlülük / özkaynak); özkaynak > 0; yükümlülük yoksa toplam pasif - özkaynak, K57 F3 gibi). Bir çeyrek
    ancak bilgi tarihi (SEC 'filed') <= t ise kullanılır; en son bilinen çeyrek sonu t'den en çok temel_max_gun gün önce.
    'bilgi_son' = kullanılan en geç bilgi tarihi."""
    E = E or K59_ESIK; n, u = len(me), len(S); mt = me.to_numpy("datetime64[ns]")
    S5 = np.full((n, u), np.nan); S7 = np.full((n, u), np.nan); X1 = np.full((n, u), np.nan); X2 = np.full((n, u), np.nan)
    bs = np.full((n, u), np.datetime64("NaT"), "datetime64[ns]")
    maxg = np.timedelta64(int(E["temel_max_gun"]), "D"); nq = E["sinyal"]["S5"]["ceyrek"]; nat = np.datetime64("NaT")
    for j, s in enumerate(S):
        c = s2c.get(s); aylar = np.flatnonzero(U[:, j])
        if c is None or not len(aylar):
            continue
        son: Dict[int, np.datetime64] = {}
        for e in tuple(K57.K57_ABD_GELIR) + ("NetIncomeLoss",):
            for q, (b, _v) in T["Q"].get((c, e), {}).items():
                son[q] = _k59_dt(b)
        if not son:
            continue
        bil = {q: (_k59_dt(bilgi[(c, q)]) if (c, q) in bilgi and pd.notna(bilgi[(c, q)]) else nat) for q in son}
        qs = np.array(sorted(son)); sv = np.array([son[q] for q in qs]); bv = np.array([bil[q] for q in qs])
        kar = T["Q"].get((c, "NetIncomeLoss"), {}); oz = T["I"].get((c, "StockholdersEquity"), {})
        gel = [T["Q"].get((c, e), {}) for e in K57.K57_ABD_GELIR]
        yuk = T["I"].get((c, "Liabilities"), {}); pasif = T["I"].get((c, "LiabilitiesAndStockholdersEquity"), {})
        for k in aylar:
            t = mt[k]
            with np.errstate(invalid="ignore"):
                gec = ~np.isnat(bv) & (bv <= t) & (t - sv <= maxg)
            if not gec.any():
                continue
            q0 = int(qs[gec].max())

            def bilinen(q: int) -> bool:
                b = bil.get(q, nat)
                return (not np.isnat(b)) and b <= t

            def isle(qq: List[int]) -> None:        # kullanılan çeyreklerin en geç bilgi tarihi
                b = max(bil[q] for q in qq)
                bs[k, j] = b if np.isnat(bs[k, j]) else max(bs[k, j], b)
            ozv = float(oz[q0][1]) if q0 in oz else np.nan
            kq = [q0 - i for i in range(nq)]
            if all(q in kar and bilinen(q) for q in kq):
                top = float(sum(kar[q][1] for q in kq))
                if np.isfinite(ozv) and ozv > 0 and np.isfinite(top):
                    S5[k, j] = top / ozv; isle(kq)
            gq = [q0, q0 - 1, q0 - 2]
            for g in gel:
                if all(q in g and bilinen(q) for q in gq):
                    r0, r1, r2 = (float(g[q][1]) for q in gq); ort = (r1 + r2) / 2
                    if np.isfinite(r0) and np.isfinite(ort) and ort > 0:
                        S7[k, j] = r0 / ort; isle(gq)
                    break
            yq = [q0, q0 - 4]
            for g in gel:
                if all(q in g and bilinen(q) for q in yq):
                    a0, a4 = float(g[q0][1]), float(g[q0 - 4][1])
                    if np.isfinite(a0) and np.isfinite(a4) and a0 > 0 and a4 > 0:
                        X1[k, j] = a0 / a4 - 1; isle(yq)
                    break
            if np.isfinite(ozv) and ozv > 0:
                yk = float(yuk[q0][1]) if q0 in yuk else (float(pasif[q0][1]) - ozv if q0 in pasif else np.nan)
                if np.isfinite(yk) and yk >= 0:
                    X2[k, j] = -yk / ozv; isle([q0])
    return {"S5": S5, "S7": S7, "X1": X1, "X2": X2, "bilgi_son": bs}


def k59_sinyaller(D: Dict[str, Any], P: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
    """Evrenin istenen bütün sinyalleri (ay x hisse; 'yüksek = iyi'; uygun olmayan / verisi olmayan NaN). Yalnız t ve öncesi bilgi.
    Döner: (sinyaller, ek) ; ek: S3_olcu (ay başına 'piyasa_degeri' / 'islem_degeri'), bilgi_son, pay_filed (denetim için) ve
    'bilesen' (X1, X2, X3: yalnız DOSYA bileşiklerinin üyeleri; tek başına portföy olarak ölçülmez)."""
    E = E or K59_ESIK; Sg = E["sinyal"]; ev = D["evren"]; iste = list(ev["sinyal"])
    U, me, S, Cm, C5, mp = P["U"], P["ay_sonu"], P["sembol"], P["Cm"], P["C5"], P["me_pos"]
    n, u = U.shape; Sd: Dict[str, np.ndarray] = {}; ek: Dict[str, Any] = {"S3_olcu": [""] * n, "bilgi_son": None, "pay_filed": None, "bilesen": {}}
    cm = Cm.to_numpy(float)
    if "S1" in iste:
        Sd["S1"] = K58.k58_sinyal_momentum({"Cm": Cm, "U": U}, {"mom_kisa": Sg["S1"]["kisa"], "mom_uzun": Sg["S1"]["uzun"]})
    if "S2" in iste:
        Sd["S2"] = -(Cm / Cm.shift(1) - 1).to_numpy(float)
    if "S8" in iste:
        r = C5.pct_change(fill_method=None)
        Sd["S8"] = -r.rolling(Sg["S8"]["gun"], min_periods=Sg["S8"]["min_gun"]).std().to_numpy(float)[mp]
    if "S9" in iste:
        z = P["Hi"].rolling(Sg["S9"]["gun"], min_periods=Sg["S9"]["min_gun"]).max().to_numpy(float)[mp]
        with np.errstate(invalid="ignore", divide="ignore"):
            Sd["S9"] = np.where(z > 0, cm / z, np.nan)
    Pt = k59_pay_tablo(D["pay"], S, me, E) if D.get("pay") is not None and ({"S3", "S6"} & set(iste)) else None
    if Pt is not None:
        ek["pay_filed"] = Pt["filed"]
    if "S3" in iste:
        s3 = -np.array(P["tl_me"], copy=True); ek["S3_olcu"] = ["islem_degeri" if o else "" for o in P["olusum"]]
        if ev["boyut"] == "piyasa_degeri" and Pt is not None and P.get("ham_me") is not None:
            carp = np.ones((n, u)); bol = D.get("bolunme") or {}
            for j, s in enumerate(S):
                if s in bol:
                    carp[:, j] = k59_bolunme_carpan(bol[s], Pt["pay_t"][:, j])
            pd_ = P["ham_me"] * Pt["pay"] * carp
            var = (U & np.isfinite(pd_) & (pd_ > 0)).sum(axis=1); top = U.sum(axis=1)
            for k in np.flatnonzero(P["olusum"]):
                if top[k] and var[k] / top[k] >= Sg["S3"]["pay_kapsam_min"]:
                    s3[k] = np.where(pd_[k] > 0, -pd_[k], np.nan); ek["S3_olcu"][k] = "piyasa_degeri"
        Sd["S3"] = s3
    if "S4" in iste:
        Sd["S4"] = k59_pead_sinyal(D["olay"], S, P["gun"], mp, Sg["S4"]["pencere_gun"]) if D.get("olay") is not None else np.full((n, u), np.nan)
    bil: Dict[str, np.ndarray] = {}
    if D.get("T") is not None:
        Tm = k59_temel_sinyal(D["T"], D["bilgi"], D["s2c"], S, me, U, E); ek["bilgi_son"] = Tm["bilgi_son"]
        bil.update({"X1": Tm["X1"], "X2": Tm["X2"]})
    else:
        Tm = {"S5": np.full((n, u), np.nan), "S7": np.full((n, u), np.nan)}
    for a in ("S5", "S7"):
        if a in iste:
            Sd[a] = Tm[a]
    if "S6" in iste:
        Sd["S6"] = -Pt["ihrac"] if Pt is not None else np.full((n, u), np.nan)
    if "S9" in Sd:
        bil["X3"] = -Sd["S9"]
    maske = lambda X_: np.where(U & np.isfinite(X_), X_, np.nan)  # noqa: E731
    ek["bilesen"] = {a: maske(x) for a, x in bil.items() if a in E.get("ek_bilesen", {})}
    return {a: maske(Sd[a]) for a in iste if a in Sd}, ek


def k59_yuzde_sira(S: np.ndarray, U: np.ndarray) -> np.ndarray:
    """Ay içi yüzdelik sıra (sıra - 0,5) / n; uygun ve sinyali olan hisseler arasında, eşitlikte ortalama sıra. Yüksek sinyal -> yüksek sıra."""
    X = pd.DataFrame(np.where(U & np.isfinite(S), S, np.nan))
    r = X.rank(axis=1, method="average").to_numpy(float); say = X.notna().sum(axis=1).to_numpy(float)[:, None]
    with np.errstate(invalid="ignore", divide="ignore"):
        return (r - 0.5) / np.where(say > 0, say, np.nan)


def k59_bilesik(Sd: Dict[str, np.ndarray], U: np.ndarray, uye: List[str], min_n: int) -> np.ndarray:
    """Bileşik: üyelerin yüzdelik sıralarının ortalaması; hissenin en az min_n üyede değeri olmalı (yoksa NaN)."""
    Y = np.stack([k59_yuzde_sira(Sd[a], U) if a in Sd else np.full(U.shape, np.nan) for a in uye])
    say = np.isfinite(Y).sum(axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        ort = np.nansum(Y, axis=0) / np.where(say > 0, say, np.nan)
    ort[(say < min_n) | ~U] = np.nan
    return ort


# ---------------------------------------------------------------- 4) PORTFÖY CETVELİ v2
def k59_ols_nw(y: np.ndarray, X: Optional[np.ndarray] = None, lag: int = 6) -> Dict[str, Any]:
    """Sabitli EKK + Newey-West (Bartlett, gecikme `lag`, serbestlik düzeltmesi yok) t değerleri. katsayi[0] = sabit (alfa).
    X None ise yalnız sabit: t, K58 k58_nw_t ile aynıdır."""
    y = np.asarray(y, float); T = len(y)
    A = np.ones((T, 1)) if X is None else np.column_stack([np.ones(T), np.asarray(X, float).reshape(T, -1)])
    p = A.shape[1]; bos = {"n": T, "katsayi": np.full(p, np.nan), "t": np.full(p, np.nan)}
    if T < p + 2 or not np.isfinite(A).all() or not np.isfinite(y).all():
        return bos
    try:
        Gi = np.linalg.inv(A.T @ A)
    except np.linalg.LinAlgError:
        return bos
    b = Gi @ (A.T @ y); Z = A * (y - A @ b)[:, None]
    Sx = Z.T @ Z
    for l in range(1, min(lag, T - 1) + 1):
        G = Z[l:].T @ Z[:-l]; Sx = Sx + (1 - l / (lag + 1)) * (G + G.T)
    var = np.diag(Gi @ Sx @ Gi)
    with np.errstate(invalid="ignore", divide="ignore"):
        t = np.where(var > 0, b / np.sqrt(np.where(var > 0, var, np.nan)), np.nan)
    return {"n": T, "katsayi": b, "t": t}


def k59_cetvel_v2(port: np.ndarray, kiyas: np.ndarray, C: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """PORTFÖY CETVELİ v2: K58 k58_cetvel (fazla > 0 + NW t, alt dönemler, son %30) + beta düzeltmeli alfa (alfa > 0, NW t(alfa) > eşik)."""
    C = C or K59_ESIK["cetvel"]; port = np.asarray(port, float); kiyas = np.asarray(kiyas, float)
    c = K58.k58_cetvel(port - kiyas, C)
    out = {"ay": c["ay"], "olculdu": False, "s_alfa": False, "tutar_v2": False}
    if c["ay"] < C["min_ay"] or "nw_t" not in c:
        return out
    reg = k59_ols_nw(port, kiyas, C["nw_lag"]); alfa, beta = float(reg["katsayi"][0]), float(reg["katsayi"][1]); ta = float(reg["t"][0])
    s_alfa = bool(np.isfinite(alfa) and alfa > 0 and np.isfinite(ta) and ta > C["t_esik"])
    out.update({k: c[k] for k in ("ort_aylik", "yillik_fazla", "nw_t", "bilgi_orani", "alt1", "alt2", "alt3", "son30", "s_t", "s_alt", "s_son")})
    out.update({"olculdu": True, "k58c_tutar": bool(c["tutar"]), "alfa_aylik": alfa, "alfa_yillik": 12 * alfa, "beta": beta, "t_alfa": ta,
                "s_alfa": s_alfa, "tutar_v2": bool(c["tutar"] and s_alfa)})
    return out


def k59_french(yollar: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """French 5 faktör + momentum (K58 indirici ve yalıtılmış ayrıştırıcı), ondalık aylık getiri; sütunlar faktörler + RF."""
    B = K58.K58_ESIK["B"]; Fr = K59_ESIK["french"]; Dl = {}
    for ad, z in B["zip"].items():
        y = (yollar or {}).get(ad) or K58._k58_indir(B["kok"] + z, os.path.join(K58.K58_YOL["french"], z), K58.K58_UA)
        if not zipfile.is_zipfile(y):
            raise K59Hata(f"{y}: zip değil")
        Dl[ad] = K58.k58_french_isolated(y)
    D = Dl["ff5"].join(Dl["mom"][["UMD"]], how="left") / 100.0
    eksik = [k for k in Fr["faktor"] + [Fr["rf"]] if k not in D]
    if eksik:
        raise K59Hata(f"French verisinde sütun yok: {eksik}")
    return D[Fr["faktor"] + [Fr["rf"]]]


def _k59_ek_olcu(seri: np.ndarray, ay: pd.PeriodIndex, FF: Optional[pd.DataFrame], E: Dict[str, Any]) -> Dict[str, Any]:
    """Bilgi istatistikleri: yıllık bileşik getiri, en büyük düşüş, Sharpe (RF varsa fazla getiriyle), FF5 + UMD alfası (NW t)."""
    C = E["cetvel"]; Fr = E["french"]; T = len(seri); out: Dict[str, Any] = {"ff_ay": 0}
    if not T:
        return out
    eq = np.cumprod(1 + seri)
    out["port_yillik"] = float(eq[-1] ** (12 / T) - 1) if eq[-1] > 0 else np.nan
    out["mdd"] = float((eq / np.maximum.accumulate(np.r_[1.0, eq])[1:] - 1).min())
    x = seri; out["sharpe_rf"] = "0"
    if FF is not None:
        G = FF.reindex(ay); rf = G[Fr["rf"]].to_numpy(float); m = np.isfinite(rf)
        x = seri[m] - rf[m]; out["sharpe_rf"] = "French RF"
        mf = m & np.isfinite(G[Fr["faktor"]].to_numpy(float)).all(axis=1); out["ff_ay"] = int(mf.sum())
        if mf.sum() >= C["min_ay"]:
            reg = k59_ols_nw(seri[mf] - rf[mf], G[Fr["faktor"]].to_numpy(float)[mf], C["nw_lag"])
            out.update({"ff_alfa_yillik": float(12 * reg["katsayi"][0]), "ff_t_alfa": float(reg["t"][0])})
    sd = float(np.std(x, ddof=1)) if len(x) > 1 else np.nan
    out["sharpe"] = float(np.mean(x) / sd * math.sqrt(12)) if sd and sd > 0 else np.nan
    return out


def k59_olc(Pf: Dict[str, np.ndarray], ay: pd.PeriodIndex, FF: Optional[pd.DataFrame] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Bir portföyün cetvel v2 sonucu ve bilgi istatistikleri; maliyetli (ön eksiz) ve maliyetsiz ('brut_') ayrı ayrı."""
    E = E or K59_ESIK; out: Dict[str, Any] = {}
    for on, seri in (("", Pf["net"]), ("brut_", Pf["brut"])):
        z = {**k59_cetvel_v2(seri, Pf["kiyas"], E["cetvel"]), **_k59_ek_olcu(np.asarray(seri, float), ay, FF, E)}
        out.update({on + k: v for k, v in z.items()})
    T = len(Pf["net"])
    out["kiyas_yillik"] = float(np.prod(1 + Pf["kiyas"]) ** (12 / T) - 1) if T else np.nan
    out["ort_devir"] = float(Pf["devir"][1:].mean()) if T > 1 else np.nan
    return out


def k59_sinyal_olc(P: Dict[str, Any], S: np.ndarray, FF: Optional[pd.DataFrame] = None,
                   E: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Bir sinyalin üst %dilim portföyü (sinyali olan uygun hisseler arasında), kıyas = bütün uygun evren; ölçüm dönemi sinyali olan hisse
    sayısının ilk kez >= min_sinyal olduğu aydan sona. Döner: (sonuç satırı, aylık getiri tablosu)."""
    E = E or K59_ESIK; ev = P["evren"]; U = P["U"]
    Us = U & np.isfinite(S); say = Us.sum(axis=1); ol = np.array(P["olusum"], copy=True)
    yeter = np.flatnonzero(ol & (say >= ev["min_sinyal"]))
    if not len(yeter):
        return {"ay": 0, "olculdu": False, "tutar_v2": False, "brut_tutar_v2": False}, pd.DataFrame()
    ol[:yeter[0]] = False
    return _k59_secim_olc(P, K58.k58_ust_dilim(np.where(Us, S, np.nan), Us, E["portfoy"]["dilim"]), ol, say, FF, E)


def _k59_secim_olc(P: Dict[str, Any], sec: np.ndarray, ol: np.ndarray, say: np.ndarray, FF: Optional[pd.DataFrame],
                   E: Dict[str, Any]) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Verilen seçim (ay x hisse, bool) ve ölçüm aylarıyla eşit ağırlıklı portföy: K58 k58_portfoy + cetvel v2 + bilgi istatistikleri."""
    ev = P["evren"]; U = P["U"]; me = P["ay_sonu"]
    Pf = K58.k58_portfoy(P["R"], sec, U, ol, ev["maliyet"])
    k = np.flatnonzero(ol); ay = pd.PeriodIndex(me[k + 1], freq="M"); nh = (sec & U)[k].sum(axis=1)
    row = {**k59_olc(Pf, ay, FF if ev.get("french") else None, E), "ilk_ay": str(me[k[0]].date()), "son_ay": str(me[k[-1]].date()),
           "ort_hisse": float(nh.mean()), "bos_ay": int((nh == 0).sum()), "ort_sinyal_n": float(say[k].mean())}
    A = pd.DataFrame({"ay_sonu": [str(x.date()) for x in me[k]], "getiri_ayi": ay.astype(str), "brut": Pf["brut"], "net": Pf["net"],
                      "kiyas": Pf["kiyas"], "devir": Pf["devir"], "n_hisse": nh, "n_sinyal": say[k], "n_evren": U[k].sum(axis=1)})
    return row, A


def k59_ucuzluk(P: Dict[str, Any], Sc: np.ndarray, Sb: np.ndarray, FF: Optional[pd.DataFrame] = None,
                E: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], List[pd.DataFrame]]:
    """KOŞULLU TEST 'UCUZLUK' (bilgi, karar yok): bileşiğin (Sc) üst %dilim'i her ay bölme sinyaline (Sb = S9) göre ikiye bölünür:
    'dusmus' = Sb'si en düşük yarı, 'yakin' = en yüksek yarı (tek sayıda ortadaki hisse dışarıda; Sb'si olmayan dışarıda). İki uzun
    portföyün cetvel istatistikleri ve aylık net farkı (dusmus - yakin; uzun-kısa değil) ile NW t. Ölçüm dönemi bileşiğinkiyle aynı."""
    E = E or K59_ESIK; Uc = E["ucuzluk"]; ev = P["evren"]; U = P["U"]
    Us = U & np.isfinite(Sc); say = Us.sum(axis=1); ol = np.array(P["olusum"], copy=True)
    yeter = np.flatnonzero(ol & (say >= ev["min_sinyal"]))
    if not len(yeter):
        return [], []
    ol[:yeter[0]] = False
    ust = K58.k58_ust_dilim(np.where(Us, Sc, np.nan), Us, Uc["dilim"])
    sec = {"dusmus": np.zeros_like(U), "yakin": np.zeros_like(U)}
    for k in np.flatnonzero(ol):
        j = np.flatnonzero(ust[k] & np.isfinite(Sb[k])); m = len(j) // 2
        if m:
            sira = j[np.argsort(Sb[k, j], kind="stable")]
            sec["dusmus"][k, sira[:m]] = True; sec["yakin"][k, sira[-m:]] = True
    kol = ("ay", "ilk_ay", "son_ay", "yillik_fazla", "nw_t", "alt1", "alt2", "alt3", "son30", "alfa_yillik", "t_alfa", "beta", "ff_alfa_yillik",
           "ff_t_alfa", "sharpe", "mdd", "ort_devir", "ort_hisse", "brut_yillik_fazla", "brut_nw_t", "brut_t_alfa")
    sat, ayl = [], {}
    for ad, s_ in sec.items():
        row, A = _k59_secim_olc(P, s_, ol, say, FF, E)
        sat.append({"portfoy": ad, **{c: row.get(c) for c in kol}}); ayl[ad] = A.assign(sinyal="UCUZLUK_" + ad)
    lag = E["cetvel"]["nw_lag"]; d = ayl["dusmus"].net.to_numpy(float) - ayl["yakin"].net.to_numpy(float)
    db = ayl["dusmus"].brut.to_numpy(float) - ayl["yakin"].brut.to_numpy(float)
    sat.append({"portfoy": "fark (dusmus - yakin)", "ay": len(d), "ilk_ay": sat[0]["ilk_ay"], "son_ay": sat[0]["son_ay"],
                "yillik_fazla": float(12 * d.mean()), "nw_t": K58.k58_nw_t(d, lag), "brut_yillik_fazla": float(12 * db.mean()),
                "brut_nw_t": K58.k58_nw_t(db, lag)})
    return sat, list(ayl.values())


def k59_plasebo(P: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Plasebo: n rastgele sinyal (default_rng(tohum + i); her ay uygun hisselere rastgele sıra), aynı üst %dilim ve cetvel v2 (net ve brüt)."""
    E = E or K59_ESIK; Pl = E["plasebo"]; U = P["U"]; Z = []; kol = ("ay", "olculdu", "yillik_fazla", "nw_t", "t_alfa", "s_t", "s_alt", "s_son", "s_alfa", "tutar_v2")
    for i in range(Pl["n"]):
        rng = np.random.default_rng(Pl["tohum"] + i)
        S = rng.random(U.shape); S[~U] = np.nan
        Pf = K58.k58_portfoy(P["R"], K58.k58_ust_dilim(S, U, E["portfoy"]["dilim"]), U, P["olusum"], P["evren"]["maliyet"])
        n_ = k59_cetvel_v2(Pf["net"], Pf["kiyas"], E["cetvel"]); b_ = k59_cetvel_v2(Pf["brut"], Pf["kiyas"], E["cetvel"])
        Z.append({"plasebo": i, **{k: n_.get(k) for k in kol}, **{"brut_" + k: b_.get(k) for k in kol[2:]}})
    return pd.DataFrame(Z)


def k59_kapsam(P: Dict[str, Any], Sd: Dict[str, np.ndarray], ek: Dict[str, Any]) -> pd.DataFrame:
    """Oluşum ayı başına uygun hisse sayısı ve her sinyali olan uygun hisse sayısı (getiri içermez)."""
    k = np.flatnonzero(P["olusum"]); U = P["U"]
    Z = pd.DataFrame({"evren": P["ad"], "ay_sonu": [str(x.date()) for x in P["ay_sonu"][k]], "n_evren": U[k].sum(axis=1)})
    for a, S in Sd.items():
        Z["n_" + a] = (U & np.isfinite(S))[k].sum(axis=1)
    Z["S3_olcu"] = [ek["S3_olcu"][i] for i in k]
    return Z


# ---------------------------------------------------------------- 5) KARAR
def k59_etiket(r: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    """Tekil sonuç etiketi: ÖLÇÜLEMEDİ / TUTMAZ / TUTAR (yineleme) / GÜÇLÜ (iki t de > t_guclu; DOSYA ailesinde > t_guclu_dosya)."""
    E = E or K59_ESIK; Kr = E["karar"]; g = Kr["t_guclu_dosya"] if r.get("sinyal") in Kr["dosya"] else Kr["t_guclu"]

    def evet(x: Any) -> bool:
        return bool(x) and not (isinstance(x, float) and np.isnan(x)) and str(x).strip().lower() not in ("false", "0", "nan", "")
    if not evet(r.get("olculdu")):
        return "ÖLÇÜLEMEDİ"
    if not evet(r.get("tutar_v2")):
        return "TUTMAZ"
    return "GÜÇLÜ" if float(r.get("nw_t", np.nan)) > g and float(r.get("t_alfa", np.nan)) > g else "TUTAR (yineleme)"


def k59_karar(Z: pd.DataFrame, Pl: Optional[pd.DataFrame], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ön kayıt §4-§5: plasebo yanlış pozitif (net ve brüt) <= eşik ise etiketler ve COMP4 kararı; değilse cetvel GÜVENİLMEZ, hüküm yok."""
    E = E or K59_ESIK; Kr = E["karar"]; Pl_ = E["plasebo"]; out: Dict[str, Any] = {"etiket": {}, "kucuk": {}}
    if Pl is None or len(Pl) < Pl_["n"]:
        out.update({"cetvel": "PLASEBO ÖLÇÜLMEDİ", "bilesik": "HÜKÜM YOK (plasebo ölçülmedi)", "yp_net": np.nan, "yp_brut": np.nan})
        return out
    b = lambda s: s.astype(str).str.strip().str.lower().isin(["true", "1", "1.0"])  # noqa: E731
    yn, yb = float(b(Pl.tutar_v2).mean()), float(b(Pl.brut_tutar_v2).mean())
    out.update({"yp_net": yn, "yp_brut": yb})
    if max(yn, yb) > Pl_["yp_esik"]:
        out.update({"cetvel": "GÜVENİLMEZ", "bilesik": "HÜKÜM YOK (cetvel v2 güvenilmez: plasebo yanlış pozitif oranı eşiğin üstünde)"})
        return out
    out["cetvel"] = "GÜVENİLİR"
    for r in Z.to_dict("records"):
        a = (r["evren"], r["sinyal"]); out["etiket"][a] = k59_etiket(r, E)
        out["kucuk"][a] = bool(out["etiket"][a] not in ("ÖLÇÜLEMEDİ", "TUTMAZ") and float(r.get("yillik_fazla", np.nan)) < Kr["buyukluk_yillik"])
    et = [out["etiket"].get((e, Kr["bilesik"]), "ÖLÇÜLEMEDİ") for e in Kr["aday_evren"]]
    if all(x in ("TUTAR (yineleme)", "GÜÇLÜ") for x in et):
        kucuk = any(out["kucuk"][(e, Kr["bilesik"])] for e in Kr["aday_evren"])
        out["bilesik"] = "TUTAR AMA KÜÇÜK" if kucuk else "PORTFÖY-ADAY"
    else:
        out["bilesik"] = "TUTMAZ (" + ", ".join(f"{e} {x}" for e, x in zip(Kr["aday_evren"], et)) + ")"
    out["dosya"] = {f"{e} {d}": out["etiket"].get((e, d), "ÖLÇÜLEMEDİ") + (", küçük" if out["kucuk"].get((e, d)) else "")
                    for d in Kr["dosya"] for e in Kr["aday_evren"]}
    return out


# ---------------------------------------------------------------- 6) KOŞU
def _k59_meta_yaz(meta: Dict[str, Any], cikti: Optional[str]) -> None:
    with open(_k59_yol("meta", cikti), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1, default=str)


def k59_evren_olc(D: Dict[str, Any], FF: Optional[pd.DataFrame] = None, E: Optional[Dict[str, Any]] = None,
                  yalniz_kapsam: bool = False) -> Dict[str, Any]:
    """Bir evren: panel -> sinyaller + bileşikler -> (yalniz_kapsam değilse) her biri için portföy ve cetvel v2; plasebo evreniyse plasebo."""
    E = E or K59_ESIK; ad = D["ad"]; ev = D["evren"]
    P = k59_panel(D, E); Sd, ek = k59_sinyaller(D, P, E)
    havuz = {**Sd, **ek["bilesen"]}
    for b, tn in E["bilesik"].items():
        uye = [a for a in tn["uye"] if a in havuz]
        if len(uye) >= tn["min"]:
            Sd[b] = k59_bilesik(havuz, P["U"], uye, tn["min"])
    ay = P["ay_sonu"][P["olusum"]]
    ozet = {"hisse": len(P["sembol"]), "olusum_ayi": int(P["olusum"].sum()), "ilk_ay": str(ay.min().date()) if len(ay) else "",
            "son_ay": str(ay.max().date()) if len(ay) else "", "ort_evren": float(P["U"][P["olusum"]].sum(axis=1).mean()) if len(ay) else 0.0,
            "S3_olcu": pd.Series([x for x in ek["S3_olcu"] if x]).value_counts().to_dict()}
    k59log.info("%s: %d hisse, %d oluşum ayı (%s .. %s), uygun evren ort %.0f", ad, ozet["hisse"], ozet["olusum_ayi"], ozet["ilk_ay"],
                ozet["son_ay"], ozet["ort_evren"])
    out = {"ozet": ozet, "kapsam": k59_kapsam(P, {**Sd, **ek["bilesen"]}, ek), "sonuc": [], "aylik": [], "plasebo": None, "ucuzluk": []}
    if yalniz_kapsam:
        return out
    Ru = P["R"][P["U"]]      # veri denetimi (kırpma yok; aykırı tek hisse getirisi raporda görünsün)
    ozet.update({"hisse_ay": int(Ru.size), "maks_hisse_ay_getiri": float(np.nanmax(Ru)) if Ru.size else np.nan,
                 "getiri_ust_300_hisse_ay": int((Ru > 3.0).sum())})
    for a, S in Sd.items():
        row, A = k59_sinyal_olc(P, S, FF, E)
        tn = E["sinyal"].get(a) or E["bilesik"][a]
        out["sonuc"].append({"evren": ad, "sinyal": a, "ad": tn["ad"], "rol": "BİLGİ" if ev["rol"] == "BİLGİ" else tn.get("rol", "BİLGİ"),
                             "uye_n": len([x for x in tn.get("uye", []) if x in havuz]) or 1, **row})
        if len(A):
            out["aylik"].append(A.assign(evren=ad, sinyal=a))
    Uc = E["ucuzluk"]
    if Uc["bilesik"] in Sd and Uc["bol"] in Sd:
        sat, ayl = k59_ucuzluk(P, Sd[Uc["bilesik"]], Sd[Uc["bol"]], FF if ev.get("french") else None, E)
        out["ucuzluk"] = [{"evren": ad, **r} for r in sat]; out["aylik"] += [A.assign(evren=ad) for A in ayl]
    if ad == E["plasebo"]["evren"]:
        out["plasebo"] = k59_plasebo(P, E).assign(evren=ad)
        k59log.info("%s plasebo: yanlış pozitif net %.3f, brüt %.3f", ad, out["plasebo"].tutar_v2.mean(), out["plasebo"].brut_tutar_v2.mean())
    return out


def k59_kos(cikti: Optional[str] = None, git_sart: bool = True, demetler: Optional[Dict[str, Dict[str, Any]]] = None,
            FF: Optional[pd.DataFrame] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Faz 2: mühür + veri sha256 + git doğrulanır; üç evren ölçülür; çıktılar ve rapor yazılır.
    demetler / FF / E yalnız testler içindir (sentetik demet; gerçek veri ve veri sha256 doğrulaması atlanır, mühür yine şarttır)."""
    sentetik = demetler is not None; Ek = E or K59_ESIK
    oc = k59_onkayit_dogrula(cikti, veri=not sentetik, git=git_sart)
    cik = cikti or K59_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    meta: Dict[str, Any] = {"surum": K59_SURUM, "onkayit": oc, "isolated": bool(sys.flags.isolated), "sentetik": sentetik,
                            "kos_baslangic": _k59_simdi(), "evren": {}, "not": []}
    if oc["zaman_utc"] and pd.Timestamp(oc["zaman_utc"]) > pd.Timestamp(meta["kos_baslangic"].replace(" UTC", "")):
        raise K59Hata("ön kayıt koşu başlangıcından sonra: sıra bozuk")
    _k59_meta_yaz(meta, cikti)
    if FF is None and not sentetik:
        try:
            FF = k59_french(); g = FF.dropna(how="all")
            meta["french"] = {"ilk_ay": str(g.index.min()), "son_ay": str(g.index.max())}
        except (K58.K58Hata, K59Hata, OSError, ValueError) as ex:
            meta["not"].append(f"French faktörleri okunamadı ({str(ex)[:200]}): FF5 + UMD alfası ve RF'li Sharpe YOK (bilgi satırları); karar etkilenmez")
            k59log.warning("%s", meta["not"][-1])
    ortak = None; sonuc, aylik, kapsam, ucuz = [], [], [], []; plasebo = None
    for ad in Ek["evren"]:
        t0 = time.time()
        if sentetik:
            if ad not in demetler:
                continue
            D = demetler[ad]
        else:
            if Ek["evren"][ad]["kaynak"] != "V_BIST" and ortak is None:
                ortak = k59_abd_ortak()
            D = k59_demet(ad, ortak, oc["veri"])
        O = k59_evren_olc(D, FF, Ek); del D
        sonuc += O["sonuc"]; aylik += O["aylik"]; kapsam.append(O["kapsam"]); ucuz += O["ucuzluk"]
        if O["plasebo"] is not None:
            plasebo = O["plasebo"]
        meta["evren"][ad] = {**O["ozet"], "sn": round(time.time() - t0)}; _k59_meta_yaz(meta, cikti)
    Z = pd.DataFrame(sonuc); kr = k59_karar(Z, plasebo, Ek)
    Z["etiket"] = [kr["etiket"].get((r.evren, r.sinyal), "HÜKÜM YOK") for r in Z.itertuples()]
    Z["kucuk"] = [kr["kucuk"].get((r.evren, r.sinyal), False) for r in Z.itertuples()]
    Z.to_csv(_k59_yol("sonuc", cikti), index=False)
    (pd.concat(aylik, ignore_index=True) if aylik else pd.DataFrame()).to_csv(_k59_yol("aylik", cikti), index=False)
    pd.concat(kapsam, ignore_index=True).to_csv(_k59_yol("kapsam", cikti), index=False)
    pd.DataFrame(ucuz).to_csv(_k59_yol("ucuzluk", cikti), index=False)
    if plasebo is not None:
        plasebo.to_csv(_k59_yol("plasebo", cikti), index=False)
    meta["karar"] = {k: v for k, v in kr.items() if k not in ("etiket", "kucuk")}
    meta["kos_bitis"] = _k59_simdi(); _k59_meta_yaz(meta, cikti)
    return {"sonuc": Z, "karar": kr, "meta": meta, "rapor": k59_rapor(cikti, Ek)}


def k59_kapsam_kos(hedef: Optional[str] = None) -> pd.DataFrame:
    """Yalnız kapsam sayımı (gerçek veri): evren ve sinyal başına hisse sayıları. Portföy getirisi, fazla ya da t HESAPLANMAZ; ön kayıt gerekmez."""
    ortak = None; par = []
    for ad, ev in K59_ESIK["evren"].items():
        if ev["kaynak"] != "V_BIST" and ortak is None:
            ortak = k59_abd_ortak()
        O = k59_evren_olc(k59_demet(ad, ortak), None, K59_ESIK, yalniz_kapsam=True)
        par.append(O["kapsam"]); k59log.info("%s kapsam özeti: %s", ad, O["ozet"])
    Z = pd.concat(par, ignore_index=True)
    if hedef:
        os.makedirs(os.path.dirname(os.path.abspath(hedef)), exist_ok=True); Z.to_csv(hedef, index=False)
    return Z


# ---------------------------------------------------------------- 7) RAPOR
def _k59_oku(ad: str, cikti: Optional[str]) -> Optional[pd.DataFrame]:
    y = _k59_yol(ad, cikti)
    if not os.path.exists(y) or os.path.getsize(y) < 3:
        return None
    return pd.read_csv(y)


def _k59_g(r: Any, k: str) -> float:
    try:
        return float(getattr(r, k))
    except (AttributeError, TypeError, ValueError):
        return np.nan


def _k59_tutmayan(r: Any) -> str:
    """Cetvel v2'nin sağlanmayan şartları (rapor metni için): 'NW t', 'alt dönem', 'son %30', 'alfa'."""
    al = (lambda k: r.get(k)) if isinstance(r, (dict, pd.Series)) else (lambda k: getattr(r, k, None))
    if str(al("olculdu")).lower() != "true":
        return ""
    ad = (("s_t", "fazla NW t"), ("s_alt", "alt dönem"), ("s_son", "son %30"), ("s_alfa", "alfa"))
    return ", ".join(a for k, a in ad if str(al(k)).lower() != "true")


def _k59_satir(r: Any) -> str:
    et = str(r.etiket) + (", küçük" if str(r.kucuk).lower() == "true" else "")
    tm = _k59_tutmayan(r); et += f" (tutmayan: {tm})" if tm and str(r.etiket) == "TUTMAZ" else ""
    ilk = getattr(r, "ilk_ay", ""); ilk = ilk if isinstance(ilk, str) else "—"
    return (f"| {r.sinyal} {r.ad} | {int(r.ay)} | {ilk} | {_k59_yz(_k59_g(r, 'yillik_fazla'))} | {_k59_sy(_k59_g(r, 'nw_t'))} | "
            f"{_k59_yz(_k59_g(r, 'alt1'), 2)} / {_k59_yz(_k59_g(r, 'alt2'), 2)} / {_k59_yz(_k59_g(r, 'alt3'), 2)} | {_k59_yz(_k59_g(r, 'son30'), 2)} | "
            f"{_k59_yz(_k59_g(r, 'alfa_yillik'))} | {_k59_sy(_k59_g(r, 't_alfa'))} | {_k59_sy(_k59_g(r, 'beta'))} | {_k59_yz(_k59_g(r, 'ff_alfa_yillik'))} | "
            f"{_k59_sy(_k59_g(r, 'ff_t_alfa'))} | {_k59_sy(_k59_g(r, 'sharpe'))} | {_k59_yz(_k59_g(r, 'mdd'))} | %{_k59_sy(_k59_g(r, 'ort_devir') * 100, 0)} | "
            f"{_k59_sy(_k59_g(r, 'ort_hisse'), 0)} | {_k59_yz(_k59_g(r, 'brut_yillik_fazla'))} | {_k59_sy(_k59_g(r, 'brut_nw_t'))} | {_k59_sy(_k59_g(r, 'brut_t_alfa'))} | {et} |")


def _k59_duz_dil(Z: pd.DataFrame, kr: Dict[str, Any], E: Dict[str, Any], Uz: Optional[pd.DataFrame] = None) -> str:
    Kr = E["karar"]; c = []
    if kr["cetvel"] == "PLASEBO ÖLÇÜLMEDİ":
        return "Plasebo ölçülmedi; cetvelin güvenilirliği sınanmadığı için hüküm verilmedi."
    c.append(f"Cetvelin kendisi: {E['plasebo']['n']} rastgele sinyalden maliyetli %{_k59_sy(kr['yp_net'] * 100, 1)}, maliyetsiz %{_k59_sy(kr['yp_brut'] * 100, 1)} "
             f"'tutar' çıktı (eşik %{E['plasebo']['yp_esik'] * 100:.0f}); cetvel v2 {kr['cetvel']}.")
    if kr["cetvel"] != "GÜVENİLİR":
        return c[0] + " Bu yüzden hiçbir sinyal için hüküm verilmedi."
    for e in Kr["aday_evren"]:
        g = Z[(Z.evren == e) & (Z.sinyal == Kr["bilesik"])]
        if len(g):
            r = g.iloc[0]
            c.append(f"Önceden yazılı bileşik ({Kr['bilesik']}) {e}'de maliyetten sonra evrene göre yıllık fazlası {_k59_yz(r.get('yillik_fazla'))} "
                     f"(NW t {_k59_sy(r.get('nw_t'))}, beta düzeltmeli alfa yıllık {_k59_yz(r.get('alfa_yillik'))}, t {_k59_sy(r.get('t_alfa'))}; {int(r.ay)} ay): {r.etiket}"
                     + (f" (sağlanmayan şart: {_k59_tutmayan(r)})." if r.etiket == "TUTMAZ" and _k59_tutmayan(r) else "."))
    c.append(f"Karar: {kr['bilesik']}.")
    tut = [f"{r.evren} {r.sinyal}" for r in Z.itertuples() if r.sinyal in E["sinyal"] and r.etiket in ("TUTAR (yineleme)", "GÜÇLÜ") and r.evren in Kr["aday_evren"]]
    c.append("Tekil sinyallerden ABD'de tutanlar (bilgi; seçim yapılmaz): " + (", ".join(tut) if tut else "hiçbiri") + ".")
    bt = [f"{r.sinyal}" for r in Z.itertuples() if r.evren not in Kr["aday_evren"] and r.etiket in ("TUTAR (yineleme)", "GÜÇLÜ")]
    if (~Z.evren.isin(Kr["aday_evren"])).any():
        c.append("BIST'te (bilgi) tutanlar: " + (", ".join(bt) if bt else "hiçbiri") + ".")
    if kr.get("dosya"):
        c.append("DOSYA ailesi (YEOTK / DGXX mantığı, kendi başına): " + "; ".join(f"{k} {v}" for k, v in kr["dosya"].items()) + ".")
    if Uz is not None and len(Uz):
        for r in Uz[Uz.portfoy.astype(str).str.startswith("fark")].itertuples():
            c.append(f"UCUZLUK (bilgi) {r.evren}: bileşiğin üst %20'sinde düşmüş yarı, zirveye yakın yarıdan yılda {_k59_yz(abs(r.yillik_fazla))[1:]} "
                     f"{'fazla' if r.yillik_fazla >= 0 else 'eksik'} getirdi (NW t {_k59_sy(r.nw_t)}).")
    return " ".join(c)


def _k59_karne(Z: pd.DataFrame, kr: Dict[str, Any], oc: Dict[str, Any], E: Dict[str, Any]) -> str:
    """IZ_KARNE Ç152 kayıt önerisi (kaydı ana oturum işler; dize değerlerinde yalnız tek tırnak, ters bölü yok)."""
    def t(x: str) -> str:
        return str(x).replace('"', "'").replace("\\", "/").replace("\n", " ")
    par = []
    for e in E["karar"]["aday_evren"]:
        g = Z[(Z.evren == e) & (Z.sinyal == E["karar"]["bilesik"])]
        if len(g):
            r = g.iloc[0]
            par.append(f"{e} COMP4 yıllık fazla {_k59_yz(r.get('yillik_fazla'))}, NW t {_k59_sy(r.get('nw_t'))}, t(alfa) {_k59_sy(r.get('t_alfa'))}, {r.etiket}")
    notu = t(f"Karar: {kr['bilesik']}; cetvel v2 {kr['cetvel']} (plasebo yanlış pozitif net %{_k59_sy(kr.get('yp_net', np.nan) * 100, 1)}, brüt "
             f"%{_k59_sy(kr.get('yp_brut', np.nan) * 100, 1)}); " + "; ".join(par) + ". DOSYA ailesi: "
             + ("; ".join(f"{k} {v}" for k, v in kr["dosya"].items()) if kr.get("dosya") else "hüküm yok") + ". İZ ilan edilemez (standart değişikliği Cemal'in kararı); seviye 0.")
    return (f'_ik_k("Ç152", "2026-11-11", "{t("K59 BASİT SİNYALLER: dokuz sürekli sinyal + önceden yazılı COMP4 bileşiği + DOSYA ailesi (YEOTK / DGXX mantığı) + UCUZLUK koşullu testi, aylık üst %10 portföy, portföy cetveli v2 (K58 C + beta düzeltmeli alfa), ABD iki evren + BIST bilgi")}", '
            f'"K59.py, test_k59.py", "{t("Basit, nedeni bilinen sürekli sinyaller ve sıra ortalaması bileşiği maliyetten sonra evreni geçiyor mu?")}", '
            f'"{t("Ön kayıt K59_ON_KAYIT.md (mühür " + str(oc["sha"])[:12] + ", ölçümden önce git kaydına işlendi); eşikler değişmedi")}", "", 0, '
            f'cikti="arastirma_cikti/k59_basit_sinyaller/ (K59_ON_KAYIT.md, K59_RAPOR.md, sinyal_sonuc.csv, aylik_getiri.csv, plasebo.csv, kapsam.csv, ucuzluk.csv)", '
            f'notu="{notu}"),')


def k59_rapor(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """K59_RAPOR.md: düz dil, karar, evren başına sinyal tablosu, plasebo, kapsam, sınırlar, sıradaki üç deneme, IZ_KARNE önerisi."""
    E = E or K59_ESIK; oc = k59_onkayit_dogrula(cikti); meta_yol = _k59_yol("meta", cikti)
    meta = json.load(open(meta_yol, encoding="utf-8")) if os.path.exists(meta_yol) else {}
    Z = _k59_oku("sonuc", cikti); Pl = _k59_oku("plasebo", cikti); Kp = _k59_oku("kapsam", cikti); Uz = _k59_oku("ucuzluk", cikti)
    if Z is None:
        raise K59Hata("sinyal_sonuc.csv yok: önce `python -I K59.py kos`")
    kr = k59_karar(Z, Pl, E); C = E["cetvel"]; parca = []
    bas = ("| Sinyal | Ay | İlk ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Alfa (yıllık) | t(alfa) | Beta | FF5+UMD alfa | t | Sharpe | "
           "En büyük düşüş | Devir | Hisse | Brüt fazla | Brüt NW t | Brüt t(alfa) | Etiket |\n" + "|---" * 20 + "|")
    for ad, ev in E["evren"].items():
        g = Z[Z.evren == ad]
        if not len(g):
            parca.append(f"## {ad}: ÖLÇÜLMEDİ\n"); continue
        m = (meta.get("evren") or {}).get(ad, {})
        parca.append(f"## {ad} — {ev['ad']} ({ev['rol']})\n{m.get('hisse', '—')} hisse, {m.get('olusum_ayi', '—')} oluşum ayı ({m.get('ilk_ay', '—')} .. "
                     f"{m.get('son_ay', '—')}), ortalama uygun evren {_k59_sy(m.get('ort_evren', np.nan), 0)} hisse; maliyet tek yön {ev['maliyet'] * 1e4:.0f} bp; "
                     f"S3 ölçüsü (ay sayısı): {m.get('S3_olcu', '—')}. Veri denetimi (kırpma yok): en büyük tek hisse aylık getirisi "
                     f"{_k59_yz(m.get('maks_hisse_ay_getiri', np.nan), 0)}, +%300 üstü {m.get('getiri_ust_300_hisse_ay', '—')} / {m.get('hisse_ay', '—')} hisse-ay.\n\n{bas}\n" + "\n".join(_k59_satir(r) for r in g.itertuples()) + "\n")
    gd = Z[Z.sinyal.isin(E["karar"]["dosya"])]
    if len(gd):
        sat = ["| Bileşik | Evren | Ay | İlk ay | Yıllık fazla (net) | NW t | Alfa (yıllık) | t(alfa) | FF5+UMD alfa | t | Hisse | Brüt fazla | Etiket |", "|---" * 13 + "|"]
        for d in E["karar"]["dosya"]:
            for r in gd[gd.sinyal == d].itertuples():
                ilk = r.ilk_ay if isinstance(getattr(r, "ilk_ay", None), str) else "—"
                sat.append(f"| {r.sinyal} ({r.ad}) | {r.evren} | {int(r.ay)} | {ilk} | {_k59_yz(_k59_g(r, 'yillik_fazla'))} | {_k59_sy(_k59_g(r, 'nw_t'))} | "
                           f"{_k59_yz(_k59_g(r, 'alfa_yillik'))} | {_k59_sy(_k59_g(r, 't_alfa'))} | {_k59_yz(_k59_g(r, 'ff_alfa_yillik'))} | {_k59_sy(_k59_g(r, 'ff_t_alfa'))} | "
                           f"{_k59_sy(_k59_g(r, 'ort_hisse'), 0)} | {_k59_yz(_k59_g(r, 'brut_yillik_fazla'))} | {r.etiket}{', küçük' if str(r.kucuk).lower() == 'true' else ''}"
                           f"{' (tutmayan: ' + _k59_tutmayan(r) + ')' if r.etiket == 'TUTMAZ' and _k59_tutmayan(r) else ''} |")
        parca.append("## DOSYA ailesi (YEOTK / DGXX'i seçtiren mantık; ayrı aile, 3 ek deneme; PORTFÖY-ADAY kararına girmez)\n"
                     f"Her bileşik kendi başına cetvel v2 ile etiketlenir; 'GÜÇLÜ' eşiği iki t de > {E['karar']['t_guclu_dosya']} (12 deneme). DOSYA_D yalnız ölçülebilir kısmın "
                     "vekilidir: gerçek DGXX seçimindeki 'SEC'e ekli bağlayıcı sözleşme' yapısal veride yok (K60). BIST'te ölçülmedi (temel veri yüklenmedi).\n\n"
                     + "\n".join(sat) + "\n")
    if Uz is not None and len(Uz):
        sat = ["| Evren | Portföy | Ay | Yıllık fazla / fark (net) | NW t | Alfa (yıllık) | t(alfa) | Hisse | Devir | Brüt | Brüt NW t |", "|---" * 11 + "|"]
        for r in Uz.itertuples():
            sat.append(f"| {r.evren} | {r.portfoy} | {int(r.ay)} | {_k59_yz(_k59_g(r, 'yillik_fazla'))} | {_k59_sy(_k59_g(r, 'nw_t'))} | {_k59_yz(_k59_g(r, 'alfa_yillik'))} | "
                       f"{_k59_sy(_k59_g(r, 't_alfa'))} | {_k59_sy(_k59_g(r, 'ort_hisse'), 0)} | {'%' + _k59_sy(_k59_g(r, 'ort_devir') * 100, 0) if np.isfinite(_k59_g(r, 'ort_devir')) else '—'} | "
                       f"{_k59_yz(_k59_g(r, 'brut_yillik_fazla'))} | {_k59_sy(_k59_g(r, 'brut_nw_t'))} |")
        parca.append(f"## Koşullu test UCUZLUK (bilgi; karar yok)\n{E['ucuzluk']['bilesik']} üst %{E['ucuzluk']['dilim'] * 100:.0f}'si her ay {E['ucuzluk']['bol']}'a göre ikiye bölündü: "
                     "'dusmus' = zirvesinden en uzak yarı, 'yakin' = zirveye en yakın yarı. İlk iki satır evrene göre fazla, 'fark' satırı iki uzun portföyün "
                     "aylık net farkıdır (dusmus - yakin).\n\n" + "\n".join(sat) + "\n")
    Sg_ = _k59_oku("saglama", cikti)
    if Sg_ is not None and len(Sg_):
        sat = ["| Evren | Sinyal | Ay (K59 / bağımsız) | Yıllık net fazla: K59 | Bağımsız kod | Fark | Aylık net getiri en büyük mutlak fark |", "|---" * 7 + "|"]
        for r in Sg_.itertuples():
            g = Z[(Z.evren == r.evren) & (Z.sinyal == r.sinyal)]
            if len(g):
                sat.append(f"| {r.evren} | {r.sinyal} | {int(g.ay.iloc[0])} / {int(r.ay)} | {_k59_yz(g.yillik_fazla.iloc[0], 3)} | {_k59_yz(r.yillik_net_fazla, 3)} | "
                           f"{(r.yillik_net_fazla - g.yillik_fazla.iloc[0]) * 1e4:+.2f} bp | {_k59_g(r, 'aylik_maks_fark'):.2e} |")
        parca.append("## Bağımsız sağlama (ayrı, basit kod; K59'un panel / sinyal / bileşik / portföy fonksiyonları kullanılmadan)\n"
                     "Yalnız veri yükleyicileri ortaktır. Fiyat, uygunluk, sinyaller, sıra ortalaması, üst %10, maliyet ve kıyas baştan hesaplandı.\n\n" + "\n".join(sat) + "\n")
    if Pl is not None and len(Pl):
        parca.append(f"## Plasebo ({E['plasebo']['evren']}, {len(Pl)} rastgele sinyal)\nYanlış pozitif: maliyetli %{_k59_sy(kr.get('yp_net', np.nan) * 100, 1)}, "
                     f"maliyetsiz %{_k59_sy(kr.get('yp_brut', np.nan) * 100, 1)} (eşik %{E['plasebo']['yp_esik'] * 100:.0f}) -> cetvel v2 {kr['cetvel']}. "
                     f"Brüt NW t ortalaması {_k59_sy(Pl.brut_nw_t.mean())}, en büyüğü {_k59_sy(Pl.brut_nw_t.max())}; brüt t(alfa) en büyüğü {_k59_sy(Pl.brut_t_alfa.max())}.\n")
    if Kp is not None and len(Kp):
        sat = ["| Evren | Sinyal | İlk ay (>= eşik) | Ortalama hisse (o aydan sonra) |", "|---|---|---|---|"]
        for ad, g in Kp.groupby("evren", sort=False):
            for kol in [c for c in g.columns if c.startswith("n_") and c != "n_evren" and g[c].notna().any()]:
                y = g[g[kol] >= E["evren"][ad]["min_sinyal"]]
                sat.append(f"| {ad} | {kol[2:]} | {y.ay_sonu.iloc[0] if len(y) else '—'} | {_k59_sy(g[g.ay_sonu >= y.ay_sonu.iloc[0]][kol].mean(), 0) if len(y) else '—'} |")
        parca.append("## Kapsam (sinyali olan uygun hisse sayısı)\n" + "\n".join(sat) + "\n")
    ozet = [f"- Cetvel v2: {kr['cetvel']}" + (f" (plasebo yanlış pozitif maliyetli %{_k59_sy(kr['yp_net'] * 100, 1)}, maliyetsiz %{_k59_sy(kr['yp_brut'] * 100, 1)})" if np.isfinite(kr.get("yp_net", np.nan)) else "") + ".",
            f"- {E['karar']['bilesik']} kararı: {kr['bilesik']}.",
            "- DOSYA ailesi (kendi başına; karara girmez): " + ("; ".join(f"{k} {v}" for k, v in kr["dosya"].items()) if kr.get("dosya") else "hüküm yok") + ".",
            "- İZ ilan edilemez: CLAUDE.md standardı (FI_OLCUT, ABD + Avrupa) değişmedi, Avrupa'da temel veri yok; standart değişikliği Cemal'in kararı."]
    notlar = "\n".join(f"- {x}" for x in meta.get("not", [])) or "- yok"
    metin = f"""# K59 — basit sinyaller, portföy cetveli v2: RAPOR

Ön kayıt: {oc['zaman_utc']} UTC (mühür {oc['sha'][:12]}, dosya sha256 {oc['dosya_sha256'][:12]}, git {str((meta.get('onkayit') or {}).get('git', {}).get('commit', '—'))[:10]}); koşu {meta.get('kos_baslangic', '—')} → {meta.get('kos_bitis', '—')}. {K59_SURUM}

## Düz dille
{_k59_duz_dil(Z, kr, E, Uz)}

## Karar (ön kayıt §4-§5)
{chr(10).join(ozet)}

Cetvel v2 şartları (maliyetten sonra): ortalama fazla > 0 ve NW t > {C['t_esik']}; 3 alt dönemin en az {C['alt_donem_min']}'sinde > 0; son %{C['son_pay'] * 100:.0f} ayda > 0;
alfa > 0 ve NW t(alfa) > {C['t_esik']}. 'GÜÇLÜ' = iki t de > {E['karar']['t_guclu']}. 'küçük' = net yıllık fazla < +{E['karar']['buyukluk_yillik'] * 100:.0f} puan.

{chr(10).join(parca)}
## Koşu notları
{notlar}

## Sınırlar
- Üç evren de yalnız bugün yaşayan hisseler (hayatta kalma yanlılığı); kıyas aynı yanlılığı taşır, fark kısmen silinir.
- U1 ve U2 bağımsız değil (ortak hisseler, S4-S7 ve COMP4 iki evrende de 2021-2026): 'iki evrende tutar' bağımsız yineleme sayılmaz.
- Temel veri SEC frames'in son bildirilen değerleridir (sonradan düzeltme olabilir); bilgi tarihi özgün başvuru günüdür.
- U1'de fiyat tabanı düzeltilmiş kapanışla, U2'de o günkü fiyatla uygulanır; S3 U1 / BIST'te işlem değeri, U2'de piyasa değeridir.
- Tutan sonuç İZ değildir; en fazla 'PORTFÖY-ADAY'.

## COMP4 tutmazsa önceden yazılı sıradaki üç deneme (koşulmadı; ana oturum karar verir)
- (a) {E['sonraki']['a']}.
- (b) {E['sonraki']['b']}.
- (c) {E['sonraki']['c']}.

## IZ_KARNE önerisi: Ç152 için kayıt metni (kaydı ana oturum işler)
```
{_k59_karne(Z, kr, oc, E)}
```
"""
    yol = _k59_yol("rapor", cikti)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k59log.info("K59 rapor: %s", yol)
    return yol


# ================================================================ K59-B: K59 §6'DAKİ ÖNCEDEN YAZILI ÜÇ DENEME (11 Kasım 2026)
# K59 ölçüm kodu, K59_ESIK ve cetvel v2 DEĞİŞMEZ (K59 mührü aynı kalır). K59-B ayrı ön kayıttır: kendi eşik sözlüğü (K59B_ESIK), kendi mührü
# (K59B_ESIK + K59 mührü) ve kendi dosyaları (K59B_ON_KAYIT.md, k59b_*.csv, K59B_RAPOR.md). Paneli, sinyalleri, bileşikleri, portföyü ve
# cetveli K59 fonksiyonlarından alır; yeni olan yalnız (a) alt evren maskesi, (b) örtüşen kohort muhasebesi ve (c) French harmanıdır.
K59B_SURUM = ("K59-B v1.0 (2026-11-11): K59 §6'daki önceden yazılı üç deneme: (a) yalnız küçük-orta hisseler, (b) 3 ay tutma + örtüşen üç "
              "kohort, (c) French kütüphanesinde momentum + kârlılık harmanı; sinyaller ve cetvel v2 K59 ile aynı")
K59B_ESIK: Dict[str, Any] = {
    "evren": ["U1", "U2"],
    "sinyal": ["COMP4", "DOSYA_Y", "S5", "S1"],
    "birincil": "COMP4",
    "a": {"ad": "yalnız küçük-orta hisseler (her ay boyut medyanının altı)", "boyut": "S3", "kural": "medyanin_kesin_alti",
          "sira": "alt_evren_ici", "kiyas": "alt_evren_esit_agirlik"},
    "b": {"ad": "3 ay tutma, örtüşen üç aylık kohort", "tut": 3, "kohort_ici": "al_tut", "baslangic": "uc_kohort_canli",
          "kiyas": "tam_uygun_evren_esit_agirlik"},
    "plasebo": {"evren": "U2", "n": 200, "yp_esik": 0.05, "tohum": {"a": 59100, "b": 59200}},
    "c": {"kok": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/",
          "zip": {"mom": "10_Portfolios_Prior_12_2_CSV.zip", "op": "Portfolios_Formed_on_OP_CSV.zip"},
          "bolum": {"vw": r"^(average\s+)?value[\s-]*weight(ed)?\s+returns\s*--\s*monthly$",
                    "ew": r"^(average\s+)?equal[\s-]*weight(ed)?\s+returns\s*--\s*monthly$"},
          "kolon": {"mom": "Hi PRIOR", "op": "Hi 20",
                    "mom_hepsi": ["Lo PRIOR", "PRIOR 2", "PRIOR 3", "PRIOR 4", "PRIOR 5", "PRIOR 6", "PRIOR 7", "PRIOR 8", "PRIOR 9", "Hi PRIOR"]},
          "agirlik": {"mom": 0.5, "op": 0.5},
          "varyant": {"VW_MKT": {"harman": "vw", "kiyas": "MKT", "rol": "ANA"},
                      "EW_EW10": {"harman": "ew", "kiyas": "EW10", "rol": "ANA"},
                      "EW_MKT": {"harman": "ew", "kiyas": "MKT", "rol": "BİLGİ"}},
          "maliyet_aylik": 0.0010,
          "donem": [["1963-son", "1963-07", None], ["2000-son", "2000-01", None], ["2000-09", "2000-01", "2009-12"],
                    ["2010-19", "2010-01", "2019-12"], ["2020-son", "2020-01", None]],
          "uzun": ["1963-son", "2000-son"], "son": "2020-son", "eksik": [-99.99, -999.0]},
    "karar": {"t_guclu": 2.75, "buyukluk_yillik": 0.04, "deneme": 8, "aday": "K59-B PORTFÖY-ADAY", "degil": "TUTMAZ"},
    "sonraki": "K60 (uzun tarih, batanlar dahil evren, sinyal kütüphanesinin tamamı); bu dokuz sinyalin 2021-26 örnekleminde başka çeşitlemesi denenmez",
}
K59B_DOSYA = {"onkayit": "K59B_ON_KAYIT.md", "sonuc": "k59b_sonuc.csv", "aylik": "k59b_aylik.csv", "plasebo": "k59b_plasebo.csv",
              "kapsam": "k59b_kapsam.csv", "french": "k59b_french.csv", "french_aylik": "k59b_french_aylik.csv", "rapor": "K59B_RAPOR.md",
              "meta": "k59b_kos_meta.json"}
# K59 sonucu (ön kayıt metnine girer; mühre girmez): K59-B'nin kör OLMADIĞI kısım
K59B_GORULEN = """K59 sonucu (K59_RAPOR.md; git e5312ca) bu ön kayıttan ÖNCE görüldü; K59-B bu dört sinyal için kör DEĞİLDİR:
  COMP4:   U1 net yıllık fazla -%1,6 (NW t -0,49; dört şartın dördü de tutmadı); U2 +%5,5 (NW t 2,30; alfa t 2,87; tutmayan tek şart
           'son %30 ayda fazla > 0': -%0,06 / ay).
  DOSYA_Y: U1 +%0,8 (NW t 0,22); U2 +%5,1 (NW t 2,14; tutmayan: son %30).   S5: U1 -%1,8 (NW t -0,61); U2 +%5,4 (NW t 1,99; tutmayan: NW t, son %30).
  S1:      U1 +%11,9 (NW t 2,77; TUTAR (yineleme)); U2 -%2,8 (NW t -0,54).   S3 küçüklük: U1 +%10,8 (NW t 3,03), U2 -%11,8 (NW t -2,11):
           momentum ve küçüklük iki evrende TERS işaretli çıktı.
  Plasebo (U2, 200 rastgele sinyal, aylık tutma, tam evren): yanlış pozitif maliyetli %0,0, maliyetsiz %1,5; cetvel v2 GÜVENİLİR."""
# Faz 1 sayımı (`python -I K59.py b_kapsam`; yalnız hisse SAYILARI) ve French dosya başlıkları. Ön kayıt metnine girer; mühre girmez (eşik değil).
K59B_KAPSAM_NOTU = """Faz 1 sayımı (11 Kas 2026, `python -I K59.py b_kapsam`; yalnız hisse sayıları, getiri hesaplanmadı):
  U1: 123 oluşum ayı (2016-05-31 .. 2026-07-31, ardışık), uygun evren ortalama 1.084. (a) alt evren 123 ay, ortalama 542 (en az 399); boyut her ay
      işlem değeri. Alt evrende sinyali olan hisse / beklenen ölçüm ayı: COMP4 501 / 66 ay (2021-02-26'dan), DOSYA_Y 392 / 63 ay (2021-05-28'den; tam
      evrenden bir ay geç), S5 445 / 66 ay, S1 543 / 122 ay (2016-06-30'dan). (b) beklenen ölçüm ayı: COMP4 64, DOSYA_Y 62, S5 64, S1 120.
  U2: 68 oluşum ayı (2020-12-31 .. 2026-07-31, ardışık), uygun evren ortalama 2.146; boyutu olan ortalama 1.917 (payı bilinmeyen ~%11 alt evrene
      giremez). (a) alt evren 68 ay, ortalama 958 (en az 813); boyut 65 ay piyasa değeri, ilk 3 ay işlem değeri. Alt evrende sinyali olan hisse /
      beklenen ölçüm ayı: COMP4 875 / 66 ay, DOSYA_Y 783 / 63 ay, S5 801 / 66 ay, S1 958 / 67 ay. (b) beklenen ölçüm ayı: COMP4 64, DOSYA_Y 62, S5 64, S1 65.
  Hepsi >= 36 ay: 'ÖLÇÜLEMEDİ' beklenmez. S1'in U1'deki ölçüm dönemi (2016'dan) öteki sinyallerden (2021'den) uzundur; K59'da da böyleydi.
  French (yalnız başlık okuması): iki portföy dosyası CRSP 202609 tabanlı; momentum 1927-01 .. 2026-09 (1.197 ay), kârlılık ve 5 faktör
      1963-07 .. 2026-09 (759 ay); gerekli sütunlarda eksik hücre yok, aylar ardışık. Beklenen ay sayıları: 1963-son 759, 2000-son 321, 2000-09 120,
      2010-19 120, 2020-son 81. Momentum dosyasında değer ağırlıklı aylık bölümün başlığı 'Value Weight Returns -- Monthly', kârlılık dosyasında
      'Average Value Weight Returns -- Monthly'; eşit ağırlıklı bölüm ikisinde de 'Average Equal Weighted Returns -- Monthly'."""
_K59B_TASARIM = ("a", "b")
# French zip'ini okuyan YALITILMIŞ kod (yalnız standart kütüphane; `python -I -X utf8 -c` ile boş geçici klasörde koşar, bu süreçte ASLA koşmaz).
# argv[1] = zip yolu, argv[2] = bölüm başlığı deseni (büyük / küçük harf ayrımsız, satırın tamamı). Çıktı: 'ay,<sütunlar>' CSV (ham %).
_K59B_FRENCH_KOD = r'''
import re, sys, zipfile
yol, desen = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(yol) as z:
    adlar = [a for a in z.namelist() if a.lower().endswith((".csv", ".txt")) and "/" not in a.strip("/")]
    if len(adlar) != 1:
        sys.exit("beklenen tek CSV, bulunan %r" % (adlar,))
    if z.getinfo(adlar[0]).file_size > 50 * 1024 * 1024:
        sys.exit("beklenmedik buyukluk")
    t = z.read(adlar[0]).decode("latin-1").splitlines()
bas = [i for i, s in enumerate(t) if re.match(desen, s.strip(), re.I)]
if len(bas) != 1:
    sys.exit("bolum basligi deseni %r icin %d eslesme (tam 1 olmali)" % (desen, len(bas)))
i = bas[0] + 1
while i < len(t) and not t[i].strip():
    i += 1
kol = [x.strip() for x in t[i].split(",")] if i < len(t) else []
if len(kol) < 2 or kol[0] != "" or not all(kol[1:]) or len(set(kol[1:])) != len(kol) - 1:
    sys.exit("sutun basligi okunamadi: %r" % (kol[:4],))
out = ["ay," + ",".join('"%s"' % k.replace('"', "") for k in kol[1:])]
for s in t[i + 1:]:
    if not re.match(r"^\s*\d{6}\s*,", s):
        break
    p = [x.strip() for x in s.split(",")]
    if len(p) != len(kol):
        sys.exit("satir sutun sayisi tutmuyor: %s" % p[0])
    out.append(p[0] + "," + ",".join(repr(float(x)) for x in p[1:]))
if len(out) < 2:
    sys.exit("bolumde aylik satir yok")
sys.stdout.write("\n".join(out) + "\n")
'''


def k59b_esik_sha(B: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """K59-B mührü: K59B_ESIK + K59 mührü (K59_ESIK + içe alınan tanımlar) birlikte; biri değişirse `b_kos` durur."""
    s = json.dumps({"K59B_ESIK": B or K59B_ESIK, "K59_MUHUR": k59_esik_sha(E)}, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _k59b_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K59_YOL["cikti"], K59B_DOSYA[ad])


def _k59b_french_yol(d: str) -> str:
    return os.path.join(K58.K58_YOL["french"], K59B_ESIK["c"]["zip"][d])


def k59b_french_indir() -> Dict[str, str]:
    """(c) için iki French portföy zip'i (önbellekte varsa dokunmaz; K58 indiricisi, genel kullanıcı adı, e-posta yok)."""
    C = K59B_ESIK["c"]
    return {d: K58._k58_indir(C["kok"] + z, _k59b_french_yol(d), K58.K58_UA) for d, z in C["zip"].items()}


def k59b_veri_sha() -> Dict[str, Tuple[str, int]]:
    """K59-B'nin okuyacağı veri: K59'un bütün kaynakları (aynı özetler) + (c)'nin iki French portföy zip'i."""
    out = dict(k59_veri_sha())
    for d, z in K59B_ESIK["c"]["zip"].items():
        y = _k59b_french_yol(d)
        if os.path.exists(y):
            out[z] = (K58._k58_dosya_sha(y), 1)
    return out


def k59b_onkayit_metin(zaman: str, veri_sha: Dict[str, Tuple[str, int]], k59_bilgi: Optional[Dict[str, Any]] = None) -> str:
    E = K59_ESIK; B = K59B_ESIK; Tb = B["b"]; C = B["c"]; Pl = B["plasebo"]; Kr = B["karar"]; Cv = E["cetvel"]; ev = E["evren"]
    kb = k59_bilgi or {}; W = C["agirlik"]; Vr = C["varyant"]; K_ = C["kolon"]
    vs = "\n".join(f"- {k}: sha256 {v[0]} ({v[1]} dosya)" for k, v in veri_sha.items()) or "- (veri dosyası bulunamadı)"
    dn = "; ".join(f"'{ad}' = {a} .. {b or 'son ay'}" for ad, a, b in C["donem"])
    vr = ", ".join(f"{v} ({t['harman'].upper()} harman - {t['kiyas']}; {t['rol']})" for v, t in Vr.items())
    return f"""# K59-B ÖN KAYIT — K59 §6'daki önceden yazılı üç deneme: küçük-orta hisseler, 3 ay tutma, French yinelemesi

Yazım zamanı: {zaman} (ölçümden ÖNCE; gerçek veride hiçbir K59-B portföy getirisi, fazla ya da t hesaplanmadı, sonuç görülmedi). Sürüm: {K59B_SURUM}
K59B_ESIK_SHA256: {k59b_esik_sha()}
K59_ESIK_SHA256: {k59_esik_sha()}
(K59-B mührü = K59B_ESIK + K59 mührünün sha256'sı. K59 mührü DEĞİŞMEDİ: K59_ON_KAYIT.md dosya sha256 {kb.get('dosya_sha256', '—')},
git {kb.get('git', '—')}; K59'un ölçüm kodu, sinyal tanımları, evren kuralları ve cetvel v2 eşikleri aynen kullanılır. `python -I K59.py b_kos`
iki mühürle, aşağıdaki veri sha256'larıyla ve bu dosya git'e işlenmiş, sonradan değişmemişse başlar; biri tutmazsa koşu durur.)

## Veri (sha256; koşu başında yeniden hesaplanır)
{vs}
K59 ön kaydındaki sekiz kaynak burada da AYNI özetle yer alır (koşu iki ön kaydı karşılaştırır); son iki zip (c) içindir. Klasör özeti = ada
göre sıralı 'dosya adı:sha256' satırlarının sha256'sı. SEC'e istek atılmaz; e-posta kullanılmaz.

## 0. Neden ve önceden bilinenler
K59 kararı: PORTFÖY-ADAY yok. CLAUDE.md 'İz yok çıkarsa durma' kuralı gereği, K59_ON_KAYIT.md §6'da K59 ÖLÇÜLMEDEN ÖNCE yazılmış üç deneme
şimdi K59-B olarak koşulur. Hangi üç denemenin yapılacağı sonuca göre seçilmedi (K59 ön kaydı git {kb.get('git', '—')}, K59 koşusundan önce).
Denemelerin AYRINTILARI ise (aşağıda 'BOŞLUK n' diye işaretli; §7'de liste) K59 sonucu görüldükten SONRA, K59-B ölçümünden ÖNCE dolduruldu.
{K59B_GORULEN}
ÇOKLU DENEME: K59 bu örneklemde 12 deneme saydı (9 tekil + 3 DOSYA; COMP4 önceden yazılı karar bileşiği). K59-B aynı 2021-2026 örnekleminde
{Kr['deneme']} deneme daha ekler ({len(B['sinyal'])} sinyal x 2 tasarım). Bu yüzden K59-B'de tutan sonuç, K59'da tutmuş olsaydı taşıyacağı ağırlığı TAŞIMAZ;
'ikinci tur adayı'dır ve K60'ta (uzun tarih) doğrulanmadan kullanılmaz.
Faz 1'de gerçek veride yalnız şunlar yapıldı: (i) `python -I K59.py b_kapsam` (hisse / ay / sinyal başına hisse SAYISI; getiri yok),
(ii) iki French zip'i indirildi ve yalnız bölüm başlıkları, sütun adları ile ilk / son ay etiketleri okundu (değer okunmadı, istatistik yok).

## 1. K59'dan aynen alınanlar (değişmez)
- Evrenler U1 ({ev['U1']['ad']}) ve U2 ({ev['U2']['ad']}); K59 §1'deki uygunluk kuralları, kriz
  kesiği {ev['U1']['kes']}, maliyet tek yön {ev['U1']['maliyet'] * 1e4:.0f} bp x devir. İkisi de yalnız bugün yaşayan hisseler (hayatta kalma yanlılığı) ve bağımsız değil.
- Sinyal tanımları K59 §2 (yalnız t ve öncesi bilgi; temel veri SEC 'filed' <= t). K59-B'de ölçülenler: {B['birincil']} (BİRİNCİL), DOSYA_Y, S5, S1 (bilgi).
- Portföy: sinyali olan uygun hisselerin üst %{E['portfoy']['dilim'] * 100:.0f}'u, eşit ağırlık, ay sonu kapanışında işlem (K58 k58_ust_dilim).
- CETVEL v2 (K59 §3) aynen, MALİYETTEN SONRA: (1) aylık fazla ortalaması > 0 ve Newey-West (gecikme {Cv['nw_lag']}) t > {Cv['t_esik']}; (2) ayların ardışık eşit
  {Cv['alt_donem_n']} parçasının en az {Cv['alt_donem_min']}'sinde ortalama fazla > 0; (3) son %{Cv['son_pay'] * 100:.0f} ayda ortalama fazla > 0; (4) beta düzeltmeli alfa > 0 ve NW t(alfa) > {Cv['t_esik']}.
  Ölçüm ayı < {Cv['min_ay']} ise 'ÖLÇÜLEMEDİ' (tutar sayılmaz). Bilgi istatistikleri (FF5 + UMD alfası, Sharpe, en büyük düşüş, devir, brüt) K59 gibi.
- BOŞLUK 10: K59'un öteki sinyalleri (S2-S4, S6-S9), COMP9, DOSYA_D, DOSYA_YD ve UCUZLUK koşulmaz; BIST ölçülmez (iş tanımı yalnız U1 ve U2 diyor).

## 2. Tasarım (a): yalnız küçük-orta hisseler
- Her ay sonu t'de alt evren = uygun (K59 §1) VE boyut ölçüsü olan hisselerden, boyutu o ayın kesit medyanının ALTINDA olanlar.
- BOŞLUK 1: boyut ölçüsü = K59 S3'ün o ay kullandığı ölçü (K59 §2 S3 kuralı aynen): U2'de piyasa değeri (o günkü fiyat x pay sayısı; uygun
  hisselerin en az %{E['sinyal']['S3']['pay_kapsam_min'] * 100:.0f}'sinin payı olan aylarda), öteki aylarda ve U1'de her ay 20 günlük medyan işlem değeri. Medyan, boyutu olan uygun
  hisseler üzerinden hesaplanır; 'altı' KESİN küçüktür (medyana eşit olan dışarıda); boyutu olmayan hisse (U2'de payı bilinmeyen) alt evrene girmez.
- BOŞLUK 2: alt evren, o ay için evrenin YERİNE geçer: (i) bileşik sinyallerin (COMP4, DOSYA_Y) yüzdelik sıraları alt evren içinde yeniden
  hesaplanır (üye sinyallerin ham değerleri aynı; S4'ün 'ear'ı K57 olay tablosundaki gibi, tam panel medyanına göre kalır); (ii) üst %10 alt
  evrende sinyali olan hisseler arasından seçilir; (iii) KIYAS = alt evrenin eşit ağırlıklı getirisi (maliyetsiz); (iv) alt evren < {ev['U1']['min_evren']} hisse
  olan ay atlanır; ölçüm dönemi = alt evrende sinyali olan hisse sayısının ilk kez >= {ev['U1']['min_sinyal']} olduğu aydan sona. Aylık dengeleme, maliyet ve
  cetvel v2 K59 ile aynı. Alt evrenden çıkan (medyanı aşan) hisse o ay satılır (devir ve maliyet buna göre).

## 3. Tasarım (b): {Tb['tut']} ay tutma, örtüşen üç kohort (Jegadeesh-Titman düzeni)
- Evren, sinyaller, bileşik sıraları ve üst %10 seçimi K59 ile birebir aynı (tam uygun evren). Her ay sonu yeni bir kohort kurulur ve {Tb['tut']} ay
  tutulur; sermaye üç kohorta bölünmüştür ve her ay yalnız süresi dolan kohort yenilenir (ölçümün i. oluşum ayında i mod {Tb['tut']} numaralı kohort).
  Bir ayın getirisi = o ay canlı olan üç kohortun getirilerinin basit ortalaması. KIYAS = K59 ile aynı (bütün uygun evrenin eşit ağırlıklısı).
- BOŞLUK 3: kohort içi AL-TUT: kuruluşta eşit ağırlık, {Tb['tut']} ay boyunca ara dengeleme yok (ağırlıklar fiyatla kayar, ara ayda işlem ve maliyet yok).
  Yenilemede kohortun devri = Σ|w_yeni - w_kaymış| (yeni seçimde de kalan hisse yalnız fark kadar işlem görür; ilk kuruluşta devir 1);
  maliyet = {ev['U1']['maliyet'] * 1e4:.0f} bp x devir, yenilenen kohortun o ayki getirisinden düşülür (net = (1 - maliyet x devir) x (1 + r) - 1, K58 ile aynı biçim).
  Kohortlar arası sermayeyi her ay 1/3'e eşitlemenin maliyeti sayılmaz (yayındaki takvim-zamanı düzeni; küçük, ama net getiriyi hafif iyimser yapar).
  Raporlanan aylık devir = üç kohortun devir ortalaması (portföyün tamamına oranla).
- BOŞLUK 4: tutulan hisse sonraki aylarda uygunluğu yitirse de (fiyat < 2 $, likidite, veri boşluğu) SATILMAZ, süre dolana kadar tutulur.
  Tutma getirisi = sonsuz ileri taşımalı ay sonu kapanışlarının oranı - 1 (kapanışı olmayan ay 0 getiri; uygun hissede K59 ay getirisiyle
  aynıdır, koşu bunu doğrular). Evren yalnız yaşayanlardan oluştuğu için borsadan çıkış getirisi yoktur.
- BOŞLUK 5: başlangıç: üç kohortun üçü de canlı olana kadarki ilk {Tb['tut'] - 1} ay ölçüme GİRMEZ (ölçüm ayı = K59'daki ay sayısı - {Tb['tut'] - 1}).
  Kohortlar sinyalin K59'daki ilk ölçüm ayından (sinyali olan hisse >= {ev['U1']['min_sinyal']}) başlayarak kurulur.
- BOŞLUK 6: oluşum ayları kesintisiz olmalıdır (K59 kapsam.csv: U1 123, U2 68 ardışık ay). Kesinti çıkarsa kohort takvimi belirsizleşir; koşu durur.

## 4. Tasarım (c): French veri kütüphanesinde momentum + kârlılık harmanı (BİLGİ; hayatta kalma yanlılığı yok)
- Kaynak ({C['kok']}; CRSP'nin bütün hisseleri, batanlar dahil):
  momentum = {C['zip']['mom']} ('10 Portfolios Formed on Momentum', önceki 12-2 ay getirisi, NYSE onluk sınırları), sütun '{K_['mom']}' (en üst onluk);
  kârlılık = {C['zip']['op']} ('Portfolios Formed on Operating Profitability'), sütun '{K_['op']}' (en üst beşlik);
  piyasa ve RF = K59'un French 5 faktör dosyası (MKT = Mkt-RF + RF).
  Aylık bölümler başlık satırıyla seçilir (büyük / küçük harf ayrımsız, satırın tamamı; dosyada tam 1 eşleşme olmalı, yoksa koşu durur):
  değer ağırlıklı `{C['bolum']['vw']}`, eşit ağırlıklı `{C['bolum']['ew']}`.
  Eksik değerler ({', '.join(str(x) for x in C['eksik'])}) yok sayılır; getiriler % -> ondalık. Zip'ler ayrı `python -I` alt sürecinde, boş klasörde ayrıştırılır.
- HARMAN (uzun-yalnız, aylık dengeli): aylık getiri = {W['mom']:g} x momentum üst onluğu + {W['op']:g} x kârlılık üst beşliği. İki harman: VW (iki bacak da değer
  ağırlıklı) ve EW (iki bacak da eşit ağırlıklı).
- KIYAS: VW harman için piyasa (MKT). EW harman için EW10 = on momentum onluğunun eşit ağırlıklı getirilerinin basit ortalaması (geniş eşit
  ağırlıklı evren VEKİLİ; onluklar NYSE sınırlarıyla kurulduğu için hisse sayıları eşit değildir, tam eşit ağırlıklı piyasa değildir).
  BOŞLUK 7a: üç satır raporlanır: {vr}. EW harmanın MKT'ye göre
  fazlası küçük hisse primini de taşır; o satır yalnız bilgidir, okuma cümlesine girmez.
- MALİYET: French serilerinde işlem maliyeti yok. Brüt ve NET ayrı raporlanır; net = brüt - %{C['maliyet_aylik'] * 100:.2f} / ay ({ev['U1']['maliyet'] * 1e4:.0f} bp x %100 aylık devir varsayımı,
  üst sınır diye önceden yazıldı; her ay sabit düşülür). Okuma NET seriye bakar.
- DÖNEMLER: {dn}.
  BOŞLUK 7b: 'son ay' = harmanın dört sütununda, EW10'da, MKT ve RF'de birlikte bulunan son ay (Faz 1 başlık okuması: bütün dosyalar
  1963-07 .. 2026-09; CRSP 202609). Fon krizi kesiği (31.08.2026, BIST olayı) French ABD serisine uygulanmaz (K58 B de son aya kadar ölçtü).
  Ortak aylar ardışık değilse koşu durur.
- ÖLÇÜ: her varyant x dönem için cetvel v2 (K59 §3'ün dört şartı; portföy = harman, kıyas = yukarıdaki) brüt ve net ayrı ayrı; ayrıca yıllık
  fazla, NW t, alt dönem ortalamaları, alfa, t(alfa), beta. Dönem < {Cv['min_ay']} ay ise 'ÖLÇÜLEMEDİ'.
- BOŞLUK 7c: ÖNCEDEN YAZILI OKUMA (ANA iki varyant için ayrı ayrı; NET seri): 'uzun dönemde tutuyor' ⇔ cetvel v2 hem '{C['uzun'][0]}' hem '{C['uzun'][1]}'
  döneminde TUTAR. '2020 sonrası güçlü' ⇔ '{C['son']}' döneminde ortalama net fazla > 0; 'zayıf' ⇔ <= 0 ('güçlü' burada yalnız 'pozitif' demektir;
  NW t yanında yazılır). Cümleler: 'bileşik uzun dönemde tutuyor ve 2020 sonrası güçlü' / 'bileşik uzun dönemde tutuyor ama 2020 sonrası zayıf' /
  'bileşik uzun dönemde tutmuyor (hangi dönem tutmadı); 2020 sonrası güçlü | zayıf'.
- SINIRLAR: harman, K59 COMP4'ün (momentum + PEAD + kârlılık + düşük ihraç sıra ortalaması) kendisi DEĞİL, iki hazır portföyün yarı yarıya
  karışımıdır; kârlılık ölçüsü faaliyet kârlılığıdır (K59 S5 = net kâr / özkaynak değil); VW harman dev şirketlerin, EW harman çok küçük
  hisselerin ağırlığındadır. (c) U1 / U2 sonucunu ne doğrular ne çürütür; 'bu tür bileşik uzun tarihte ve yanlılıksız veride var mı' sorusuna bakar.

## 5. Plasebo (cetvelin her tasarımda sınanması) — BOŞLUK 8
K59 plasebosu aylık tutma ve tam evren içindi. (a) ve (b) için ayrı ayrı: {Pl['evren']}'de {Pl['n']} rastgele sinyal (her ay uygun hisselere rastgele sıra;
numpy default_rng(tohum + i); tohum (a) {Pl['tohum']['a']}, (b) {Pl['tohum']['b']}), o tasarımın portföy kuralı ve cetvel v2. Yanlış pozitif oranı = TUTAN payı; maliyetli ve
maliyetsiz (brüt) İKİSİ de <= %{Pl['yp_esik'] * 100:.0f} olmalı. Biri > %{Pl['yp_esik'] * 100:.0f} ise (ya da plasebo ölçülemediyse) o tasarımda cetvel GÜVENİLMEZ sayılır ve o tasarımın dört sinyali
için 'HÜKÜM YOK' yazılır (öteki tasarım etkilenmez).

## 6. Karar kuralları (şimdi yazıldı; sonuçtan sonra değişmez)
1. Evren düzeyi etiket (bilgi): bir sinyal bir tasarımda bir evrende cetvel v2'nin dört şartını maliyetten sonra sağlıyorsa 'TUTAR (yineleme)';
   hem NW t(fazla) hem t(alfa) > {Kr['t_guclu']} ise 'GÜÇLÜ' ({len(B['sinyal'])} sinyal x 2 tasarım = {Kr['deneme']} deneme için Bonferroni); aksi 'TUTMAZ'; ay < {Cv['min_ay']} 'ÖLÇÜLEMEDİ'.
2. Tasarım düzeyi: (a) ya da (b)'de bir sinyal 'TUTAR' ⇔ HEM U1 HEM U2'de cetvel v2 maliyetten sonra tutar VE iki evrende de net yıllık fazla
   >= +{Kr['buyukluk_yillik'] * 100:.0f} puan. İki evrende de 'GÜÇLÜ' ise tasarım düzeyinde de 'GÜÇLÜ' yazılır. BOŞLUK 9: iki evrende tutar ama birinde net yıllık fazla
   < +{Kr['buyukluk_yillik'] * 100:.0f} puan ise 'TUTMAZ (küçük)' (K59'daki 'TUTAR AMA KÜÇÜK' ara etiketi burada yok); bir evrende tutmazsa / ölçülemezse 'TUTMAZ'.
3. KARAR yalnız {B['birincil']}'e bakar: '{Kr['aday']}' ⇔ {B['birincil']} (a) YA DA (b) tasarımında 'TUTAR' (iki evrende). Aksi '{Kr['degil']}'. BOŞLUK 9: iki
   tasarımda da cetvel güvenilmez / plasebo ölçülmemiş ise karar 'HÜKÜM YOK' yazılır. DOSYA_Y, S5 ve S1 bilgidir; kararı değiştirmez, onlardan
   yeni bileşik kurulmaz.
4. (c) karara GİRMEZ; tarih hakkında bilgidir ve §4'teki önceden yazılı okuma cümlesiyle raporlanır.
5. İZ ilan EDİLEMEZ (CLAUDE.md standardı FI_OLCUT, ABD + Avrupa; Avrupa'da temel veri yok). K59-B'nin çıkabilecek etiketleri yalnız
   '{Kr['aday']}' ve '{Kr['degil']}' (ya da 'HÜKÜM YOK')'tur. '{Kr['aday']}' bir öneri kapısı (CLAUDE.md 'tarama' kapısı) SAYILMAZ; K60 doğrulaması gerekir.

## 7. BOŞLUK listesi (iş tanımında açık kalan, ölçümden önce burada doldurulan ayrıntılar)
1. (a) boyut = K59 S3'ün o ayki ölçüsü; medyan boyutu olan uygun hisselerde; kesin altı; boyutu olmayan dışarıda.
2. (a) sıralar, üst %10 ve kıyas alt evren içinde; S4 'ear' aynen; alt evren < {ev['U1']['min_evren']} ay atlanır; sinyal eşiği {ev['U1']['min_sinyal']}.
3. (b) kohort içi al-tut; devir ve maliyet yalnız yenilenen kohortta; kohortlar arası eşitleme maliyetsiz.
4. (b) tutulan hisse uygunluğu yitirse de satılmaz; tutma getirisi ileri taşımalı kapanıştan.
5. (b) ilk {Tb['tut'] - 1} ay (üç kohort canlı değil) ölçüme girmez; kıyas tam uygun evren.
6. (b) oluşum ayları kesintiliyse koşu durur.
7. (c) üç rapor satırı (EW - MKT bilgi), 'son ay' tanımı ve kriz kesiğinin uygulanmaması, okuma cümlesinin ölçülebilir tanımı, bölüm desenleri.
8. Tasarıma özel plasebo ({Pl['n']} rastgele sinyal, {Pl['evren']}; > %{Pl['yp_esik'] * 100:.0f} ise o tasarımda hüküm yok).
9. 'küçük' (< +{Kr['buyukluk_yillik'] * 100:.0f} puan) tasarım düzeyinde TUTMAZ sayılır; iki tasarım da hükümsüzse 'HÜKÜM YOK'.
10. Yalnız dört sinyal, yalnız U1 ve U2; BIST, UCUZLUK ve öteki sinyaller koşulmaz.

## 8. Kapsam (veriden ötürü, sonuçtan bağımsız)
{K59B_KAPSAM_NOTU}

## 9. K59-B'den sonra (sonuç ne olursa olsun)
Hat K60'a geçer: {B['sonraki']}.
K59-B tutsa da tutmasa da bu ön kayda yeni tasarım, yeni eşik ya da yeni sinyal eklenmez.

## 10. Değişmezlik
Yukarıdaki bütün eşikler, tanımlar ve kurallar sabittir; sonuç görüldükten sonra değiştirilmez. Kod hatası düzeltmesi gerekirse ön kayıt
değişmez, düzeltme raporda ayrıca yazılır. K59_ON_KAYIT.md ve K59 çıktıları değişmez.

## 11. Faz 2 komutu (bu dosya git'e işlendikten SONRA)
`cd /home/user/col_yolu && python -I K59.py b_kos`
"""


def _k59b_onkayit_oku(yol: str) -> Dict[str, Any]:
    with open(yol, encoding="utf-8") as f:
        metin = f.read()
    m = re.search(r"^K59B_ESIK_SHA256: ([0-9a-f]{64})$", metin, re.M); k = re.search(r"^K59_ESIK_SHA256: ([0-9a-f]{64})$", metin, re.M)
    z = re.search(r"^Yazım zamanı: (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC", metin, re.M)
    veri = {a: (h, int(n)) for a, h, n in re.findall(r"^- ([\w.\-]+): sha256 ([0-9a-f]{64}) \((\d+) dosya\)$", metin, re.M)}
    return {"sha": m.group(1) if m else None, "k59_sha": k.group(1) if k else None, "zaman_utc": z.group(1) if z else "", "veri": veri}


def k59b_onkayit(cikti: Optional[str] = None, veri_sha: Optional[Dict[str, Tuple[str, int]]] = None) -> str:
    """K59-B ön kaydını yazar. K59 ön kaydı yerinde ve mührü bugünkü K59_ESIK ile aynı olmalı. Dosya varsa ÜZERİNE YAZMAZ: mühür aynıysa yolu
    döndürür, değilse durur. veri_sha None ise French zip'leri (önbellekte yoksa) indirilir ve veri özetleri hesaplanır."""
    k59 = k59_onkayit_dogrula(cikti)
    yol = _k59b_yol("onkayit", cikti)
    if os.path.exists(yol):
        mevcut = _k59b_onkayit_oku(yol)["sha"]
        if mevcut != k59b_esik_sha():
            raise K59Hata(f"K59-B ön kaydı zaten var ve mühür farklı ({mevcut} != {k59b_esik_sha()}): eşikler ön kayıttan sonra değişmiş")
        k59log.info("K59-B ön kaydı zaten var (mühür aynı): %s", yol)
        return yol
    if veri_sha is None:
        k59b_french_indir(); veri_sha = k59b_veri_sha()
    try:
        git = _k59_git_islenmis(k59["yol"])["commit"][:10]
    except K59Hata:
        git = "—"
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    with open(yol, "w", encoding="utf-8") as f:
        f.write(k59b_onkayit_metin(zaman, veri_sha, {"dosya_sha256": k59["dosya_sha256"], "git": git}))
    k59log.info("K59-B ön kaydı yazıldı: %s (mühür %s; K59 mührü %s)", yol, k59b_esik_sha()[:12], k59_esik_sha()[:12])
    return yol


def k59b_onkayit_dogrula(cikti: Optional[str] = None, veri: bool = False, git: bool = False) -> Dict[str, Any]:
    """İKİ mühür birden: K59 ön kaydı (yerinde, mührü bugünkü K59_ESIK) ve K59-B ön kaydı (mührü bugünkü K59B_ESIK + K59 mührü; içinde yazılı
    K59 mührü aynı). veri=True: veri sha256'ları (K59 kaynakları iki ön kayıtta aynı + bugünkü dosyalar aynı). git=True: iki ön kayıt da git'e
    işlenmiş ve sonradan değişmemiş. Biri tutmazsa K59Hata."""
    k59 = k59_onkayit_dogrula(cikti, veri=False, git=git)
    yol = _k59b_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise K59Hata(f"K59-B ön kaydı yok ({yol}): önce `python K59.py b_onkayit`")
    oc = _k59b_onkayit_oku(yol)
    if oc["sha"] != k59b_esik_sha():
        raise K59Hata(f"K59-B ön kayıt mührü tutmuyor ({oc['sha']} != {k59b_esik_sha()}): eşikler ön kayıttan sonra değişmiş, koşu durdu")
    if oc["k59_sha"] != k59_esik_sha() or oc["k59_sha"] != k59["sha"]:
        raise K59Hata(f"K59-B ön kaydındaki K59 mührü tutmuyor ({oc['k59_sha']} != {k59_esik_sha()}): K59 eşikleri değişmiş, koşu durdu")
    fark = sorted(k for k, v in k59["veri"].items() if oc["veri"].get(k) != v)
    if fark:
        raise K59Hata(f"K59-B ön kaydındaki veri özetleri K59 ön kaydındakilerle aynı değil: {fark}; koşu durdu")
    out = {"yol": yol, "sha": oc["sha"], "k59_sha": oc["k59_sha"], "zaman_utc": oc["zaman_utc"], "dosya_sha256": K58._k58_dosya_sha(yol),
           "veri": oc["veri"], "k59": {"yol": k59["yol"], "dosya_sha256": k59["dosya_sha256"], "zaman_utc": k59["zaman_utc"], "git": k59.get("git")}}
    if veri:
        simdi = k59b_veri_sha()
        fark = sorted(k for k in set(simdi) | set(oc["veri"]) if simdi.get(k) != oc["veri"].get(k))
        if fark:
            raise K59Hata(f"veri K59-B ön kaydındakiyle aynı değil (sha256 / dosya sayısı farklı ya da eksik): {fark}; koşu durdu")
    if git:
        out["git"] = _k59_git_islenmis(yol)
    return out


# ---------------------------------------------------------------- B-a) ALT EVREN (küçük-orta)
def k59b_alt_evren(P: Dict[str, Any], S3: np.ndarray) -> Dict[str, Any]:
    """(a): panelin alt evreni = uygun VE boyut ölçüsü olan hisselerden boyutu o ayın kesit medyanının KESİN altında olanlar. S3 = K59'un
    küçüklük sinyali (-boyut; ay başına piyasa değeri ya da işlem değeri, yalnız t ve öncesi). Alt evren < min_evren olan ay oluşumdan çıkar.
    Döner: P'nin kopyası (U, R, olusum daraltılmış) + 'boyut', 'boyut_medyan', 'U_tam'. K59 ölçüm fonksiyonları bu panelle aynen çalışır."""
    ev = P["evren"]; U = P["U"]
    boyut = np.where(U & np.isfinite(S3), -np.asarray(S3, float), np.nan)
    med = np.full(len(U), np.nan); var = np.isfinite(boyut).any(axis=1)
    if var.any():
        med[var] = np.nanmedian(boyut[var], axis=1)
    with np.errstate(invalid="ignore"):
        Ua = np.array(U & np.isfinite(boyut) & (boyut < med[:, None]), copy=True)
    ol = np.array(P["olusum"], copy=True) & (Ua.sum(axis=1) >= ev["min_evren"])
    Ua[~ol] = False
    return {**P, "U": Ua, "R": np.where(Ua, P["R"], np.nan), "olusum": ol, "boyut": boyut, "boyut_medyan": med, "U_tam": U}


def k59b_sinyal_seti(Sd: Dict[str, np.ndarray], ek: Dict[str, Any], U: np.ndarray, E: Optional[Dict[str, Any]] = None,
                     B: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """K59-B'nin sinyalleri verilen evren maskesiyle: tekil sinyal U içine maskelenir; bileşiğin yüzdelik sıraları U İÇİNDE yeniden kurulur
    (K59 k59_evren_olc ile aynı üye ve 'en az k' kuralı). U = tam uygun evren ise K59'un bileşiğiyle birebir aynıdır."""
    E = E or K59_ESIK; B = B or K59B_ESIK; havuz = {**Sd, **ek["bilesen"]}; out: Dict[str, np.ndarray] = {}
    for s in B["sinyal"]:
        if s in E["bilesik"]:
            tn = E["bilesik"][s]; uye = [a for a in tn["uye"] if a in havuz]
            if len(uye) >= tn["min"]:
                out[s] = k59_bilesik(havuz, U, uye, tn["min"])
        elif s in Sd:
            out[s] = np.where(U & np.isfinite(Sd[s]), Sd[s], np.nan)
    return out


# ---------------------------------------------------------------- B-b) ÖRTÜŞEN KOHORTLAR (3 ay tutma)
def k59b_tutma_getiri(P: Dict[str, Any]) -> np.ndarray:
    """(b) için ay getirisi (k -> k+1), uygunluk maskesi OLMADAN: sonsuz ileri taşımalı ay sonu kapanışlarının oranı - 1 (kapanışı olmayan
    ay 0 getiri). Ay sonu kapanışı olan (uygun) hissede K58 k58_aylik getirisiyle aynıdır. Yalnız k ve k+1 ay sonu fiyatlarını kullanır."""
    Cx = P["C5"].ffill().loc[P["ay_sonu"]]
    return np.array((Cx.shift(-1) / Cx - 1).to_numpy(float), copy=True)


def k59b_ortusen_portfoy(Rh: np.ndarray, R: np.ndarray, sec: np.ndarray, U: np.ndarray, olusum: np.ndarray, maliyet: float,
                         tut: int) -> Dict[str, np.ndarray]:
    """Örtüşen kohortlar: i. oluşum ayında (i mod tut) numaralı kohort yeniden kurulur (eşit ağırlık, seçim sec & U), öteki kohortlar AL-TUT
    sürer (ağırlık fiyatla kayar, işlem yok). Yenilenen kohortun devri = Σ|w_yeni - w_kaymış| (ilk kuruluş 1), maliyeti o ayki getirisinden
    düşer. Ay getirisi = tut kohortun ortalaması; ilk tut - 1 ay (kohortların hepsi canlı değil) dışarıda. Kıyas = U eşit ağırlıklı
    (maliyetsiz, K58 k58_portfoy ile aynı). tut = 1 iken K58 k58_portfoy ile birebir aynıdır. Oluşum ayları kesintiliyse durur."""
    idx = np.flatnonzero(olusum); n = len(idx); N = R.shape[1]
    if n and (np.diff(idx) != 1).any():
        raise K59Hata("örtüşen kohort: oluşum ayları kesintili (kohort takvimi belirsiz); ön kayıt §3 BOŞLUK 6 gereği koşu durdu")
    w = [np.zeros(N) for _ in range(tut)]
    br = np.zeros((n, tut)); nt = np.zeros((n, tut)); dv = np.zeros((n, tut)); kb = np.full(n, np.nan); nh = np.zeros(n, int)
    for i, k in enumerate(idx):
        c = i % tut; s = sec[k] & U[k]; m = int(s.sum())
        wy = s / m if m else np.zeros(N)
        dv[i, c] = float(np.abs(wy - w[c]).sum()); w[c] = wy
        rr = np.nan_to_num(Rh[k]); tutulan = np.zeros(N, bool)
        for cc in range(min(tut, i + 1)):
            dolu = bool(w[cc].sum() > 0); tutulan |= w[cc] > 0
            r = float(np.sum(w[cc] * rr)) if dolu else 0.0
            br[i, cc] = r; nt[i, cc] = (1 - maliyet * dv[i, cc]) * (1 + r) - 1
            w[cc] = w[cc] * (1 + rr) / (1 + r) if dolu and (1 + r) != 0 else np.zeros(N)
        kb[i] = float(np.nanmean(R[k][U[k]])) if U[k].any() else np.nan; nh[i] = int(tutulan.sum())
    g = slice(tut - 1, None)
    return {"brut": br[g].mean(axis=1), "net": nt[g].mean(axis=1), "devir": dv[g].mean(axis=1), "kiyas": kb[g], "n_hisse": nh[g],
            "ay_idx": idx[g], "kohort_brut": br[g], "kohort_net": nt[g], "kohort_devir": dv[g]}


def k59b_ortusen_olc(P: Dict[str, Any], Rh: np.ndarray, S: np.ndarray, FF: Optional[pd.DataFrame] = None, E: Optional[Dict[str, Any]] = None,
                     B: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """(b): bir sinyalin üst %dilim seçimi (K59 k59_sinyal_olc ile aynı seçim ve aynı başlangıç ayı) örtüşen kohortlarla; cetvel v2 + bilgi
    istatistikleri (K59 k59_olc). Döner: (sonuç satırı, aylık getiri tablosu)."""
    E = E or K59_ESIK; B = B or K59B_ESIK; ev = P["evren"]; U = P["U"]; me = P["ay_sonu"]; tut = int(B["b"]["tut"])
    Us = U & np.isfinite(S); say = Us.sum(axis=1); ol = np.array(P["olusum"], copy=True)
    yeter = np.flatnonzero(ol & (say >= ev["min_sinyal"]))
    bos: Tuple[Dict[str, Any], pd.DataFrame] = ({"ay": 0, "olculdu": False, "tutar_v2": False, "brut_tutar_v2": False}, pd.DataFrame())
    if not len(yeter):
        return bos
    ol[:yeter[0]] = False
    if int(ol.sum()) < tut:
        return bos
    sec = K58.k58_ust_dilim(np.where(Us, S, np.nan), Us, E["portfoy"]["dilim"])
    Pf = k59b_ortusen_portfoy(Rh, P["R"], sec, U, ol, ev["maliyet"], tut)
    k = Pf["ay_idx"]; ay = pd.PeriodIndex(me[k + 1], freq="M")
    row = {**k59_olc(Pf, ay, FF if ev.get("french") else None, E), "ilk_ay": str(me[k[0]].date()), "son_ay": str(me[k[-1]].date()),
           "ort_hisse": float(Pf["n_hisse"].mean()), "bos_ay": int((Pf["n_hisse"] == 0).sum()), "ort_sinyal_n": float(say[k].mean())}
    A = pd.DataFrame({"ay_sonu": [str(x.date()) for x in me[k]], "getiri_ayi": ay.astype(str), "brut": Pf["brut"], "net": Pf["net"],
                      "kiyas": Pf["kiyas"], "devir": Pf["devir"], "n_hisse": Pf["n_hisse"], "n_sinyal": say[k], "n_evren": U[k].sum(axis=1)})
    return row, A


def k59b_plasebo_b(P: Dict[str, Any], Rh: np.ndarray, E: Optional[Dict[str, Any]] = None, B: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """(b) plasebosu: n rastgele sinyal (default_rng(tohum_b + i); her ay uygun hisselere rastgele sıra), üst %dilim, örtüşen kohortlar, cetvel v2."""
    E = E or K59_ESIK; B = B or K59B_ESIK; Pl = B["plasebo"]; U = P["U"]; Z = []
    kol = ("ay", "olculdu", "yillik_fazla", "nw_t", "t_alfa", "s_t", "s_alt", "s_son", "s_alfa", "tutar_v2")
    for i in range(Pl["n"]):
        rng = np.random.default_rng(Pl["tohum"]["b"] + i)
        S = rng.random(U.shape); S[~U] = np.nan
        Pf = k59b_ortusen_portfoy(Rh, P["R"], K58.k58_ust_dilim(S, U, E["portfoy"]["dilim"]), U, P["olusum"], P["evren"]["maliyet"], int(B["b"]["tut"]))
        n_ = k59_cetvel_v2(Pf["net"], Pf["kiyas"], E["cetvel"]); b_ = k59_cetvel_v2(Pf["brut"], Pf["kiyas"], E["cetvel"])
        Z.append({"plasebo": i, **{k: n_.get(k) for k in kol}, **{"brut_" + k: b_.get(k) for k in kol[2:]}})
    return pd.DataFrame(Z)


# ---------------------------------------------------------------- B-c) FRENCH HARMANI
def k59b_french_bolum(zip_yol: str, desen: str, eksik: Optional[List[float]] = None) -> pd.DataFrame:
    """French portföy zip'inin başlığı `desen`e uyan AYLIK bölümü (ondalık getiri; eksik kodları NaN). Güvenilmeyen zip ayrı `python -I`
    alt sürecinde, boş geçici klasörde, yalnız standart kütüphaneyle ayrıştırılır (_K59B_FRENCH_KOD); bu süreç yalnız CSV çıktısını okur."""
    import io
    import tempfile
    if not zipfile.is_zipfile(zip_yol):
        raise K59Hata(f"{zip_yol}: zip değil / yok")
    with tempfile.TemporaryDirectory() as bos:
        r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-c", _K59B_FRENCH_KOD, os.path.abspath(zip_yol), desen], cwd=bos,
                           capture_output=True, text=True, encoding="utf-8", timeout=300)
    if r.returncode != 0:
        raise K59Hata(f"French ayrıştırma ({os.path.basename(zip_yol)}): {r.stderr.strip()[-300:]}")
    D = pd.read_csv(io.StringIO(r.stdout), index_col=0)
    D.index = pd.PeriodIndex(pd.to_datetime(D.index.astype(str), format="%Y%m"), freq="M")
    if not D.index.is_unique or not D.index.is_monotonic_increasing:
        raise K59Hata(f"{os.path.basename(zip_yol)}: aylık bölümde yinelenen / sırasız ay")
    D = D.astype(float)
    for e in (K59B_ESIK["c"]["eksik"] if eksik is None else eksik):
        D = D.mask(np.isclose(D, e))
    return D / 100.0


def k59b_french_seri(yollar: Optional[Dict[str, str]] = None, FF: Optional[pd.DataFrame] = None, E: Optional[Dict[str, Any]] = None,
                     B: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """(c) aylık seriler (ondalık; ortak ve ardışık aylar): mom_vw, op_vw, mom_ew, op_ew, harman_vw, harman_ew, EW10, MKT, RF."""
    E = E or K59_ESIK; B = B or K59B_ESIK; C = B["c"]; K_ = C["kolon"]; W = C["agirlik"]
    if FF is None:
        FF = k59_french()
    T = {}
    for d in C["zip"]:
        y = (yollar or {}).get(d) or _k59b_french_yol(d)
        for ag, desen in C["bolum"].items():
            T[(d, ag)] = k59b_french_bolum(y, desen, C["eksik"])
            gerek = [K_[d]] + (K_["mom_hepsi"] if d == "mom" else [])
            eksik = [k for k in gerek if k not in T[(d, ag)]]
            if eksik:
                raise K59Hata(f"French {C['zip'][d]} ({ag}): sütun yok {eksik} (bulunan {list(T[(d, ag)].columns)})")
    A = pd.DataFrame({"mom_vw": T[("mom", "vw")][K_["mom"]], "op_vw": T[("op", "vw")][K_["op"]], "mom_ew": T[("mom", "ew")][K_["mom"]],
                      "op_ew": T[("op", "ew")][K_["op"]], "EW10": T[("mom", "ew")][K_["mom_hepsi"]].mean(axis=1, skipna=False)})
    A = A.join(pd.DataFrame({"MKT": FF["MKT_RF"] + FF[E["french"]["rf"]], "RF": FF[E["french"]["rf"]]}), how="inner").dropna().sort_index()
    if len(A) < 2 or ((A.index[1:] - A.index[:-1]).map(lambda x: x.n) != 1).any():
        raise K59Hata("French (c): ortak aylar yok / ardışık değil (ön kayıt §4 BOŞLUK 7b); koşu durdu")
    for ag in ("vw", "ew"):
        A["harman_" + ag] = W["mom"] * A["mom_" + ag] + W["op"] * A["op_" + ag]
    return A


def k59b_french_olc(A: pd.DataFrame, E: Optional[Dict[str, Any]] = None, B: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """(c): varyant x dönem cetvel v2 (net = brüt - sabit aylık maliyet; ön eksiz sütunlar NET, 'brut_' maliyetsiz)."""
    E = E or K59_ESIK; B = B or K59B_ESIK; C = B["c"]; Z = []
    for v, tn in C["varyant"].items():
        for ad, a, b in C["donem"]:
            m = np.asarray(A.index >= pd.Period(a, "M")) & (np.asarray(A.index <= pd.Period(b, "M")) if b else True)
            g = A[m]; brut = g["harman_" + tn["harman"]].to_numpy(float); kiy = g[tn["kiyas"]].to_numpy(float); net = brut - C["maliyet_aylik"]
            cn = k59_cetvel_v2(net, kiy, E["cetvel"]); cb = k59_cetvel_v2(brut, kiy, E["cetvel"])
            Z.append({"varyant": v, "rol": tn["rol"], "harman": tn["harman"], "kiyas": tn["kiyas"], "donem": ad,
                      "ilk": str(g.index[0]) if len(g) else "", "son": str(g.index[-1]) if len(g) else "", **cn,
                      **{"brut_" + k: x for k, x in cb.items()},
                      "harman_yillik": float(np.prod(1 + net) ** (12 / len(net)) - 1) if len(net) else np.nan,
                      "kiyas_yillik": float(np.prod(1 + kiy) ** (12 / len(kiy)) - 1) if len(kiy) else np.nan})
    return pd.DataFrame(Z)


def _k59b_dogru(x: Any) -> bool:
    return str(x).strip().lower() in ("true", "1", "1.0")


def k59b_french_okuma(Z: Optional[pd.DataFrame], B: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """Ön kayıt §4 BOŞLUK 7c: ANA varyantlar için önceden yazılı okuma cümlesi (NET seri)."""
    B = B or K59B_ESIK; C = B["c"]; out: Dict[str, str] = {}
    if Z is None or not len(Z):
        return out
    for v, tn in C["varyant"].items():
        if tn["rol"] != "ANA":
            continue
        g = Z[Z.varyant == v].set_index("donem")
        if not set(C["uzun"] + [C["son"]]) <= set(g.index) or not all(_k59b_dogru(g.loc[d, "olculdu"]) for d in C["uzun"] + [C["son"]]):
            out[v] = "ÖLÇÜLEMEDİ (dönemlerden biri yok / kısa)"; continue
        tut = {d: _k59b_dogru(g.loc[d, "tutar_v2"]) for d in C["uzun"]}
        son = "güçlü" if float(g.loc[C["son"], "ort_aylik"]) > 0 else "zayıf"
        if all(tut.values()):
            out[v] = "bileşik uzun dönemde tutuyor " + ("ve 2020 sonrası güçlü" if son == "güçlü" else "ama 2020 sonrası zayıf")
        else:
            out[v] = ("bileşik uzun dönemde tutmuyor (" + ", ".join(f"{d}: {'TUTAR' if t else 'TUTMAZ'}" for d, t in tut.items())
                      + f"); 2020 sonrası {son}")
    return out


# ---------------------------------------------------------------- B) KARAR
def k59b_karar(Z: pd.DataFrame, Pl: Optional[pd.DataFrame], B: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ön kayıt §5-§6: tasarım başına plasebo (net ve brüt yanlış pozitif <= eşik) -> evren etiketleri -> tasarım düzeyi TUTAR / GÜÇLÜ / TUTMAZ
    (iki evren + net yıllık fazla >= eşik) -> karar yalnız birincil sinyale (COMP4) bakar."""
    B = B or K59B_ESIK; Kr = B["karar"]; Pb = B["plasebo"]
    Ee = {"karar": {"t_guclu": Kr["t_guclu"], "t_guclu_dosya": Kr["t_guclu"], "dosya": []}}
    out: Dict[str, Any] = {"cetvel": {}, "yp_net": {}, "yp_brut": {}, "etiket": {}, "kucuk": {}, "sinyal": {}}
    for t in _K59B_TASARIM:
        pl = Pl[Pl.tasarim.astype(str) == t] if Pl is not None and len(Pl) and "tasarim" in Pl else None
        if pl is None or len(pl) < Pb["n"]:
            out["cetvel"][t] = "PLASEBO ÖLÇÜLMEDİ"; out["yp_net"][t] = out["yp_brut"][t] = np.nan
        else:
            yn, yb = float(pl.tutar_v2.map(_k59b_dogru).mean()), float(pl.brut_tutar_v2.map(_k59b_dogru).mean())
            out["yp_net"][t], out["yp_brut"][t] = yn, yb
            out["cetvel"][t] = "GÜVENİLMEZ" if max(yn, yb) > Pb["yp_esik"] else "GÜVENİLİR"
        g = Z[Z.tasarim.astype(str) == t] if len(Z) else Z
        for s in B["sinyal"]:
            if out["cetvel"][t] != "GÜVENİLİR":
                out["sinyal"][(t, s)] = "HÜKÜM YOK (" + ("plasebo ölçülmedi" if out["cetvel"][t] == "PLASEBO ÖLÇÜLMEDİ" else
                                                        "cetvel bu tasarımda güvenilmez: plasebo yanlış pozitif oranı eşiğin üstünde") + ")"
                continue
            et, kc = [], []
            for e in B["evren"]:
                r = g[(g.evren == e) & (g.sinyal == s)] if len(g) else g
                x = k59_etiket(r.iloc[0].to_dict(), Ee) if len(r) else "ÖLÇÜLEMEDİ"
                yf = float(r.iloc[0].get("yillik_fazla", np.nan)) if len(r) else np.nan
                out["etiket"][(t, e, s)] = x; et.append(x)
                out["kucuk"][(t, e, s)] = bool(x not in ("ÖLÇÜLEMEDİ", "TUTMAZ") and not yf >= Kr["buyukluk_yillik"]); kc.append(out["kucuk"][(t, e, s)])
            if all(x in ("TUTAR (yineleme)", "GÜÇLÜ") for x in et):
                if any(kc):
                    out["sinyal"][(t, s)] = f"TUTMAZ (küçük: iki evrende cetvel v2 tutar ama net yıllık fazla < +{Kr['buyukluk_yillik'] * 100:.0f} puan)"
                else:
                    out["sinyal"][(t, s)] = "GÜÇLÜ" if all(x == "GÜÇLÜ" for x in et) else "TUTAR"
            else:
                out["sinyal"][(t, s)] = "TUTMAZ (" + ", ".join(f"{e} {x}" for e, x in zip(B["evren"], et)) + ")"
    tutan = [t for t in _K59B_TASARIM if out["sinyal"][(t, B["birincil"])] in ("TUTAR", "GÜÇLÜ")]
    if tutan:
        out["karar"] = f"{Kr['aday']} ({B['birincil']} tasarım {', '.join('(' + t + ')' for t in tutan)} iki evrende tutar)"
    elif all(out["cetvel"][t] != "GÜVENİLİR" for t in _K59B_TASARIM):
        out["karar"] = "HÜKÜM YOK (iki tasarımda da cetvel güvenilmez ya da plasebo ölçülmedi)"
    else:
        out["karar"] = Kr["degil"]
    return out


# ---------------------------------------------------------------- B) KOŞU
def _k59b_meta_yaz(meta: Dict[str, Any], cikti: Optional[str]) -> None:
    with open(_k59b_yol("meta", cikti), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1, default=str)


def k59b_evren_olc(D: Dict[str, Any], FF: Optional[pd.DataFrame] = None, E: Optional[Dict[str, Any]] = None, B: Optional[Dict[str, Any]] = None,
                   yalniz_kapsam: bool = False) -> Dict[str, Any]:
    """Bir evren: K59 paneli ve sinyalleri -> (a) alt evren + K59 k59_sinyal_olc, (b) örtüşen kohortlar; plasebo evreniyse iki tasarımın
    plasebosu. yalniz_kapsam=True: yalnız hisse SAYILARI (getiri, portföy, plasebo HESAPLANMAZ)."""
    E = E or K59_ESIK; B = B or K59B_ESIK; ad = D["ad"]; ev = D["evren"]
    P = k59_panel(D, E); Sd, ek = k59_sinyaller(D, P, E)
    if B["a"]["boyut"] not in Sd:
        raise K59Hata(f"{ad}: boyut ölçüsü ({B['a']['boyut']}) üretilemedi; (a) tasarımı kurulamaz")
    Pa = k59b_alt_evren(P, Sd[B["a"]["boyut"]])
    Sa = k59b_sinyal_seti(Sd, ek, Pa["U"], E, B); Sb = k59b_sinyal_seti(Sd, ek, P["U"], E, B)
    eksik = [s for s in B["sinyal"] if s not in Sa or s not in Sb]
    if eksik:
        raise K59Hata(f"{ad}: K59-B sinyalleri üretilemedi: {eksik}")
    k = np.flatnonzero(P["olusum"])
    Kp = pd.DataFrame({"evren": ad, "ay_sonu": [str(x.date()) for x in P["ay_sonu"][k]], "n_evren": P["U"][k].sum(axis=1),
                       "n_boyutlu": np.isfinite(Pa["boyut"])[k].sum(axis=1), "n_alt": Pa["U"][k].sum(axis=1), "alt_olusum": Pa["olusum"][k],
                       "S3_olcu": [ek["S3_olcu"][i] for i in k]})
    for s in B["sinyal"]:
        Kp["a_n_" + s] = (Pa["U"] & np.isfinite(Sa[s]))[k].sum(axis=1); Kp["b_n_" + s] = (P["U"] & np.isfinite(Sb[s]))[k].sum(axis=1)
    ka = np.flatnonzero(Pa["olusum"])
    ozet = {"hisse": len(P["sembol"]), "olusum_ayi": int(P["olusum"].sum()), "ilk_ay": str(P["ay_sonu"][k[0]].date()) if len(k) else "",
            "son_ay": str(P["ay_sonu"][k[-1]].date()) if len(k) else "", "ort_evren": float(P["U"][k].sum(axis=1).mean()) if len(k) else 0.0,
            "alt_olusum_ayi": int(len(ka)), "ort_alt_evren": float(Pa["U"][ka].sum(axis=1).mean()) if len(ka) else 0.0,
            "olusum_ardisik": bool(len(k) < 2 or (np.diff(k) == 1).all()),
            "S3_olcu": pd.Series([x for x in ek["S3_olcu"] if x]).value_counts().to_dict()}
    k59log.info("K59-B %s: %d oluşum ayı, uygun evren ort %.0f, alt evren (a) %d ay ort %.0f", ad, ozet["olusum_ayi"], ozet["ort_evren"],
                ozet["alt_olusum_ayi"], ozet["ort_alt_evren"])
    out: Dict[str, Any] = {"ozet": ozet, "kapsam": Kp, "sonuc": [], "aylik": [], "plasebo": []}
    if yalniz_kapsam:
        return out
    Rh = k59b_tutma_getiri(P)
    if not np.allclose(Rh[P["U"]], P["R"][P["U"]], equal_nan=True):
        raise K59Hata(f"{ad}: tutma getirisi uygun hisselerde K59 ay getirisiyle aynı değil (ön kayıt §3 BOŞLUK 4); koşu durdu")
    for s in B["sinyal"]:
        tn = E["sinyal"].get(s) or E["bilesik"][s]
        for t, (row, A) in (("a", k59_sinyal_olc(Pa, Sa[s], FF, E)), ("b", k59b_ortusen_olc(P, Rh, Sb[s], FF, E, B))):
            out["sonuc"].append({"tasarim": t, "evren": ad, "sinyal": s, "ad": tn["ad"], "rol": "BİRİNCİL" if s == B["birincil"] else "BİLGİ", **row})
            if len(A):
                out["aylik"].append(A.assign(tasarim=t, evren=ad, sinyal=s))
    if ad == B["plasebo"]["evren"]:
        Ea = {**E, "plasebo": {**E["plasebo"], "n": B["plasebo"]["n"], "tohum": B["plasebo"]["tohum"]["a"]}}
        out["plasebo"] = [k59_plasebo(Pa, Ea).assign(tasarim="a", evren=ad), k59b_plasebo_b(P, Rh, E, B).assign(tasarim="b", evren=ad)]
        for pl in out["plasebo"]:
            k59log.info("K59-B %s plasebo (%s): yanlış pozitif net %.3f, brüt %.3f", ad, pl.tasarim.iloc[0], pl.tutar_v2.mean(), pl.brut_tutar_v2.mean())
    return out


def k59b_kos(cikti: Optional[str] = None, git_sart: bool = True, demetler: Optional[Dict[str, Dict[str, Any]]] = None,
             FF: Optional[pd.DataFrame] = None, E: Optional[Dict[str, Any]] = None, B: Optional[Dict[str, Any]] = None,
             french: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """K59-B Faz 2: İKİ mühür (K59 + K59-B) + veri sha256 + git doğrulanır; (a) ve (b) U1 / U2'de, (c) French'te ölçülür; çıktılar ve rapor.
    demetler / FF / E / B / french yalnız testler içindir (sentetik demet ve sentetik zip; gerçek veri ve veri sha256 doğrulaması atlanır,
    iki mühür yine şarttır; sentetikte french verilmezse (c) atlanır)."""
    sentetik = demetler is not None; Ek = E or K59_ESIK; Bk = B or K59B_ESIK
    oc = k59b_onkayit_dogrula(cikti, veri=not sentetik, git=git_sart)
    cik = cikti or K59_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    meta: Dict[str, Any] = {"surum": K59B_SURUM, "onkayit": oc, "isolated": bool(sys.flags.isolated), "sentetik": sentetik,
                            "kos_baslangic": _k59_simdi(), "evren": {}, "not": []}
    if oc["zaman_utc"] and pd.Timestamp(oc["zaman_utc"]) > pd.Timestamp(meta["kos_baslangic"].replace(" UTC", "")):
        raise K59Hata("K59-B ön kaydı koşu başlangıcından sonra: sıra bozuk")
    for a_ in ("sonuc", "aylik", "plasebo", "kapsam", "french", "french_aylik", "rapor"):      # önceki koşunun çıktısı rapora karışmasın
        if os.path.exists(_k59b_yol(a_, cikti)):
            os.remove(_k59b_yol(a_, cikti))
    _k59b_meta_yaz(meta, cikti)
    if FF is None and not sentetik:
        try:
            FF = k59_french(); g = FF.dropna(how="all")
            meta["french"] = {"ilk_ay": str(g.index.min()), "son_ay": str(g.index.max())}
        except (K58.K58Hata, K59Hata, OSError, ValueError) as ex:
            meta["not"].append(f"French faktörleri okunamadı ({str(ex)[:200]}): FF5 + UMD alfası, RF'li Sharpe ve (c) YOK; (a) / (b) kararı etkilenmez")
            k59log.warning("%s", meta["not"][-1])
    ortak = None; sonuc, aylik, kapsam, plasebo = [], [], [], []
    for ad in Bk["evren"]:
        t0 = time.time()
        if sentetik:
            if ad not in demetler:
                continue
            D = demetler[ad]
        else:
            if ortak is None:
                ortak = k59_abd_ortak()
            D = k59_demet(ad, ortak, oc["veri"])
        O = k59b_evren_olc(D, FF, Ek, Bk); del D
        sonuc += O["sonuc"]; aylik += O["aylik"]; kapsam.append(O["kapsam"]); plasebo += O["plasebo"]
        meta["evren"][ad] = {**O["ozet"], "sn": round(time.time() - t0)}; _k59b_meta_yaz(meta, cikti)
    Zc = None
    if FF is not None and (french is not None or not sentetik):
        try:
            Ac = k59b_french_seri(french, FF, Ek, Bk); Zc = k59b_french_olc(Ac, Ek, Bk)
            Zc.to_csv(_k59b_yol("french", cikti), index=False)
            Ac.rename_axis("ay").reset_index().assign(ay=lambda x: x.ay.astype(str)).to_csv(_k59b_yol("french_aylik", cikti), index=False)
            meta["c"] = {"ilk_ay": str(Ac.index[0]), "son_ay": str(Ac.index[-1]), "ay": int(len(Ac)), "okuma": k59b_french_okuma(Zc, Bk)}
        except (K59Hata, K58.K58Hata, OSError, ValueError, KeyError) as ex:
            meta["not"].append(f"(c) French harmanı ölçülemedi ({str(ex)[:300]}); (a) / (b) kararı etkilenmez")
            k59log.warning("%s", meta["not"][-1])
    else:
        meta["not"].append("(c) French harmanı ölçülmedi (French verisi yok)")
    Z = pd.DataFrame(sonuc); Pl = pd.concat(plasebo, ignore_index=True) if plasebo else None
    kr = k59b_karar(Z, Pl, Bk)
    if len(Z):
        Z["etiket"] = [kr["etiket"].get((r.tasarim, r.evren, r.sinyal), "HÜKÜM YOK") for r in Z.itertuples()]
        Z["kucuk"] = [kr["kucuk"].get((r.tasarim, r.evren, r.sinyal), False) for r in Z.itertuples()]
        Z["tasarim_etiket"] = [kr["sinyal"].get((r.tasarim, r.sinyal), "") for r in Z.itertuples()]
    Z.to_csv(_k59b_yol("sonuc", cikti), index=False)
    (pd.concat(aylik, ignore_index=True) if aylik else pd.DataFrame()).to_csv(_k59b_yol("aylik", cikti), index=False)
    (pd.concat(kapsam, ignore_index=True) if kapsam else pd.DataFrame()).to_csv(_k59b_yol("kapsam", cikti), index=False)
    if Pl is not None:
        Pl.to_csv(_k59b_yol("plasebo", cikti), index=False)
    meta["karar"] = {"karar": kr["karar"], "cetvel": kr["cetvel"], "yp_net": kr["yp_net"], "yp_brut": kr["yp_brut"],
                     "sinyal": {f"({t}) {s}": v for (t, s), v in kr["sinyal"].items()}}
    meta["kos_bitis"] = _k59_simdi(); _k59b_meta_yaz(meta, cikti)
    return {"sonuc": Z, "karar": kr, "meta": meta, "french": Zc, "rapor": k59b_rapor(cikti, Ek, Bk)}


def k59b_kapsam_kos(hedef: Optional[str] = None) -> pd.DataFrame:
    """Yalnız sayım (gerçek veri): evren, alt evren ve dört sinyal için ay başına hisse SAYILARI. Portföy getirisi, fazla ya da t HESAPLANMAZ;
    ön kayıt gerekmez. SEC'e istek atılmaz."""
    ortak = k59_abd_ortak(); par = []
    for ad in K59B_ESIK["evren"]:
        O = k59b_evren_olc(k59_demet(ad, ortak), None, K59_ESIK, K59B_ESIK, yalniz_kapsam=True)
        par.append(O["kapsam"]); k59log.info("K59-B %s kapsam özeti: %s", ad, O["ozet"])
    Z = pd.concat(par, ignore_index=True)
    if hedef:
        os.makedirs(os.path.dirname(os.path.abspath(hedef)), exist_ok=True); Z.to_csv(hedef, index=False)
    return Z


def k59b_kapsam_ozet(Kp: pd.DataFrame, E: Optional[Dict[str, Any]] = None, B: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Kapsam tablosundan tasarım x evren x sinyal özeti: ilk ay (sinyali olan hisse >= eşik), beklenen ölçüm ayı, ortalama hisse (yalnız sayılar)."""
    E = E or K59_ESIK; B = B or K59B_ESIK; Z = []
    for ad, g in Kp.groupby("evren", sort=False):
        ms = E["evren"][ad]["min_sinyal"]; ga = g[g.alt_olusum.map(_k59b_dogru)]
        for s in B["sinyal"]:
            for t, gg, kol, dus in (("a", ga, "a_n_" + s, 0), ("b", g, "b_n_" + s, int(B["b"]["tut"]) - 1)):
                y = gg[gg[kol] >= ms]
                if not len(y):
                    Z.append({"tasarim": t, "evren": ad, "sinyal": s, "ilk_ay": "", "ay": 0, "ort_sinyal_n": np.nan}); continue
                son = gg[gg.ay_sonu >= y.ay_sonu.iloc[0]]
                Z.append({"tasarim": t, "evren": ad, "sinyal": s, "ilk_ay": y.ay_sonu.iloc[0], "ay": max(0, len(son) - dus),
                          "ort_sinyal_n": float(son[kol].mean())})
    return pd.DataFrame(Z)


# ---------------------------------------------------------------- B) RAPOR
def _k59b_oku(ad: str, cikti: Optional[str]) -> Optional[pd.DataFrame]:
    y = _k59b_yol(ad, cikti)
    if not os.path.exists(y) or os.path.getsize(y) < 3:
        return None
    return pd.read_csv(y)


def _k59b_duz_dil(Z: pd.DataFrame, kr: Dict[str, Any], okuma: Dict[str, str], E: Dict[str, Any], B: Dict[str, Any]) -> str:
    c = []; ad = {"a": "yalnız küçük-orta hisselerde", "b": "3 ay tutmalı örtüşen portföylerde"}; Pb = B["plasebo"]
    for t in _K59B_TASARIM:
        if kr["cetvel"][t] != "GÜVENİLİR":
            c.append(f"Tasarım ({t}) {ad[t]}: cetvel {kr['cetvel'][t]}; bu tasarımda hüküm verilmedi."); continue
        c.append(f"Tasarım ({t}) {ad[t]}: cetvel güvenilir ({Pb['n']} rastgele sinyalden maliyetli %{_k59_sy(kr['yp_net'][t] * 100, 1)}, maliyetsiz "
                 f"%{_k59_sy(kr['yp_brut'][t] * 100, 1)} 'tutar' çıktı; eşik %{Pb['yp_esik'] * 100:.0f}).")
        for e in B["evren"]:
            g = Z[(Z.tasarim == t) & (Z.evren == e) & (Z.sinyal == B["birincil"])]
            if len(g):
                r = g.iloc[0]
                c.append(f"{B['birincil']} {e}'de maliyetten sonra kıyasa göre yıllık {_k59_yz(r.get('yillik_fazla'))} (NW t {_k59_sy(r.get('nw_t'))}, alfa t "
                         f"{_k59_sy(r.get('t_alfa'))}; {int(r.ay)} ay): {r.etiket}" + (f" (sağlanmayan şart: {_k59_tutmayan(r)})." if r.etiket == "TUTMAZ" and _k59_tutmayan(r) else "."))
        c.append(f"Tasarım ({t}) {B['birincil']} sonucu: {kr['sinyal'][(t, B['birincil'])]}.")
    c.append(f"KARAR: {kr['karar']}.")
    tut = [f"({t}) {s}" for (t, s), v in kr["sinyal"].items() if s != B["birincil"] and v in ("TUTAR", "GÜÇLÜ")]
    c.append("Öteki üç sinyalden (bilgi; seçim yapılmaz) tasarım düzeyinde tutan: " + (", ".join(tut) if tut else "hiçbiri") + ".")
    for v, x in okuma.items():
        c.append(f"French tarihi ({v}; bilgi): {x}.")
    return " ".join(c)


def _k59b_karne(kr: Dict[str, Any], okuma: Dict[str, str], oc: Dict[str, Any], Z: pd.DataFrame, B: Dict[str, Any]) -> str:
    """IZ_KARNE kayıt önerisi (kaydı ana oturum işler ve numarayı doğrular; dize değerlerinde yalnız tek tırnak, ters bölü yok)."""
    def t(x: str) -> str:
        return str(x).replace('"', "'").replace("\\", "/").replace("\n", " ")
    par = []
    for ts in _K59B_TASARIM:
        for e in B["evren"]:
            g = Z[(Z.tasarim == ts) & (Z.evren == e) & (Z.sinyal == B["birincil"])] if len(Z) else Z
            if len(g):
                r = g.iloc[0]
                par.append(f"({ts}) {e} {B['birincil']} yıllık fazla {_k59_yz(r.get('yillik_fazla'))}, NW t {_k59_sy(r.get('nw_t'))}, t(alfa) {_k59_sy(r.get('t_alfa'))}, {r.etiket}")
    notu = t(f"Karar: {kr['karar']}; cetvel (a) {kr['cetvel']['a']}, (b) {kr['cetvel']['b']}; " + "; ".join(par) + ". French (c): "
             + ("; ".join(f"{v}: {x}" for v, x in okuma.items()) or "ölçülmedi") + f". İZ ilan edilemez; seviye 0. Sonraki: {B['sonraki']}.")
    return (f'_ik_k("Ç153", "2026-11-11", "{t("K59-B: K59 §6daki önceden yazılı üç deneme: (a) yalnız küçük-orta hisseler, (b) 3 ay tutma + örtüşen üç kohort, (c) French kütüphanesinde momentum + kârlılık harmanı; COMP4, DOSYA_Y, S5, S1; cetvel v2 aynı")}", '
            f'"K59.py, test_k59.py", "{t("K59da tutmayan bileşik küçük-orta hisselerde ya da 3 ay tutmayla tutuyor mu; uzun tarihte (French) bu tür bileşik var mı?")}", '
            f'"{t("Ön kayıt K59B_ON_KAYIT.md (mühür " + str(oc["sha"])[:12] + "; K59 mührü " + str(oc["k59_sha"])[:12] + " değişmedi; ölçümden önce git kaydına işlendi)")}", "", 0, '
            f'cikti="arastirma_cikti/k59_basit_sinyaller/ (K59B_ON_KAYIT.md, K59B_RAPOR.md, k59b_sonuc.csv, k59b_aylik.csv, k59b_plasebo.csv, k59b_kapsam.csv, k59b_french.csv, k59b_french_aylik.csv)", '
            f'notu="{notu}"),')


def k59b_rapor(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None, B: Optional[Dict[str, Any]] = None) -> str:
    """K59B_RAPOR.md: düz dil, karar, tasarım x evren sinyal tabloları, plasebo, French (c) tablosu ve okuma, kapsam, sınırlar, sonraki adım,
    IZ_KARNE önerisi. Çıktı dosyalarından yeniden yazılır (ölçüm yapmaz)."""
    E = E or K59_ESIK; B = B or K59B_ESIK; oc = k59b_onkayit_dogrula(cikti); meta_yol = _k59b_yol("meta", cikti); C = B["c"]; Kr = B["karar"]
    meta = json.load(open(meta_yol, encoding="utf-8")) if os.path.exists(meta_yol) else {}
    Z = _k59b_oku("sonuc", cikti); Pl = _k59b_oku("plasebo", cikti); Kp = _k59b_oku("kapsam", cikti); Zc = _k59b_oku("french", cikti)
    if Z is None:
        raise K59Hata("k59b_sonuc.csv yok: önce `python -I K59.py b_kos`")
    kr = k59b_karar(Z, Pl, B); okuma = k59b_french_okuma(Zc, B); Cv = E["cetvel"]; parca = []
    bas = ("| Sinyal | Ay | İlk ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Alfa (yıllık) | t(alfa) | Beta | FF5+UMD alfa | t | Sharpe | "
           "En büyük düşüş | Devir | Hisse | Brüt fazla | Brüt NW t | Brüt t(alfa) | Etiket |\n" + "|---" * 20 + "|")
    tad = {"a": f"Tasarım (a): {B['a']['ad']}; kıyas = alt evrenin eşit ağırlıklısı", "b": f"Tasarım (b): {B['b']['ad']}; kıyas = tam uygun evrenin eşit ağırlıklısı"}
    for t in _K59B_TASARIM:
        yp = (f"plasebo yanlış pozitif maliyetli %{_k59_sy(kr['yp_net'][t] * 100, 1)}, maliyetsiz %{_k59_sy(kr['yp_brut'][t] * 100, 1)}"
              if np.isfinite(kr["yp_net"][t]) else "plasebo ölçülmedi")
        parca.append(f"## {tad[t]}\nCetvel: {kr['cetvel'][t]} ({yp}; eşik %{B['plasebo']['yp_esik'] * 100:.0f}).\n")
        for ad in B["evren"]:
            g = Z[(Z.tasarim == t) & (Z.evren == ad)]; m = (meta.get("evren") or {}).get(ad, {})
            if not len(g):
                parca.append(f"### ({t}) {ad}: ÖLÇÜLMEDİ\n"); continue
            ek = (f"alt evren {m.get('alt_olusum_ayi', '—')} ay, ortalama {_k59_sy(m.get('ort_alt_evren', np.nan), 0)} hisse (tam uygun evren "
                  f"{_k59_sy(m.get('ort_evren', np.nan), 0)}); boyut ölçüsü (ay sayısı): {m.get('S3_olcu', '—')}" if t == "a" else
                  f"tam uygun evren ortalama {_k59_sy(m.get('ort_evren', np.nan), 0)} hisse; 'Hisse' = üç kohortta tutulan farklı hisse sayısı, 'Devir' = portföyün tamamına oranla aylık")
            parca.append(f"### ({t}) {ad} — {ek}\n\n{bas}\n" + "\n".join(_k59_satir(r) for r in g.itertuples()) + "\n")
    sat = ["| Tasarım | Sinyal | Rol | " + " | ".join(B["evren"]) + " | Tasarım düzeyi |", "|---" * (4 + len(B["evren"])) + "|"]
    for t in _K59B_TASARIM:
        for s in B["sinyal"]:
            hu = [kr["etiket"].get((t, e, s), "HÜKÜM YOK") + (", küçük" if kr["kucuk"].get((t, e, s)) else "") for e in B["evren"]]
            sat.append(f"| ({t}) | {s} | {'BİRİNCİL' if s == B['birincil'] else 'bilgi'} | " + " | ".join(hu) + f" | {kr['sinyal'][(t, s)]} |")
    ozet_tablo = "\n".join(sat)
    if Zc is not None and len(Zc):
        sat = ["| Varyant | Dönem | Ay | Brüt yıllık fazla | Net yıllık fazla | NW t (net) | Alt 1/2/3 (net) | Son %30 (net) | Alfa (net, yıllık) | t(alfa) | Beta | "
               "Cetvel v2 net | Cetvel v2 brüt |", "|---" * 13 + "|"]
        for r in Zc.itertuples():
            v2 = lambda x, o: "ÖLÇÜLEMEDİ" if not _k59b_dogru(o) else ("TUTAR" if _k59b_dogru(x) else "TUTMAZ")  # noqa: E731
            sat.append(f"| {r.varyant} ({r.rol}) | {r.donem} ({r.ilk} .. {r.son}) | {int(r.ay)} | {_k59_yz(_k59_g(r, 'brut_yillik_fazla'))} | {_k59_yz(_k59_g(r, 'yillik_fazla'))} | "
                       f"{_k59_sy(_k59_g(r, 'nw_t'))} | {_k59_yz(_k59_g(r, 'alt1'), 2)} / {_k59_yz(_k59_g(r, 'alt2'), 2)} / {_k59_yz(_k59_g(r, 'alt3'), 2)} | {_k59_yz(_k59_g(r, 'son30'), 2)} | "
                       f"{_k59_yz(_k59_g(r, 'alfa_yillik'))} | {_k59_sy(_k59_g(r, 't_alfa'))} | {_k59_sy(_k59_g(r, 'beta'))} | {v2(r.tutar_v2, r.olculdu)} | {v2(r.brut_tutar_v2, r.brut_olculdu)} |")
        parca.append("## Tasarım (c): French kütüphanesinde momentum + kârlılık harmanı (bilgi; karara girmez)\n"
                     f"Harman = {C['agirlik']['mom']:g} x momentum üst onluğu + {C['agirlik']['op']:g} x faaliyet kârlılığı üst beşliği; net = brüt - %{C['maliyet_aylik'] * 100:.2f} / ay (varsayım, üst sınır). "
                     "VW_MKT: değer ağırlıklı harman - piyasa; EW_EW10: eşit ağırlıklı harman - on momentum onluğunun EW ortalaması; EW_MKT yalnız bilgi.\n\n"
                     + "\n".join(sat) + "\n\nÖnceden yazılı okuma (net seri): " + ("; ".join(f"{v}: {x}" for v, x in okuma.items()) or "—") + ".\n")
    else:
        parca.append("## Tasarım (c): French harmanı ÖLÇÜLMEDİ\n")
    if Pl is not None and len(Pl):
        sat = ["| Tasarım | Plasebo sayısı | Yanlış pozitif (maliyetli) | Yanlış pozitif (maliyetsiz) | Brüt NW t ortalaması | Brüt NW t en büyük | Brüt t(alfa) en büyük |", "|---" * 7 + "|"]
        for t, g in Pl.groupby("tasarim", sort=False):
            sat.append(f"| ({t}) | {len(g)} | %{_k59_sy(g.tutar_v2.map(_k59b_dogru).mean() * 100, 1)} | %{_k59_sy(g.brut_tutar_v2.map(_k59b_dogru).mean() * 100, 1)} | "
                       f"{_k59_sy(g.brut_nw_t.mean())} | {_k59_sy(g.brut_nw_t.max())} | {_k59_sy(g.brut_t_alfa.max())} |")
        parca.append(f"## Plasebo ({B['plasebo']['evren']}; tasarım başına rastgele sinyaller)\n" + "\n".join(sat) + "\n")
    if Kp is not None and len(Kp):
        Ko = k59b_kapsam_ozet(Kp, E, B)
        sat = ["| Tasarım | Evren | Sinyal | İlk ay (>= eşik) | Beklenen ölçüm ayı | Ortalama sinyalli hisse |", "|---" * 6 + "|"]
        sat += [f"| ({r.tasarim}) | {r.evren} | {r.sinyal} | {r.ilk_ay or '—'} | {int(r.ay)} | {_k59_sy(r.ort_sinyal_n, 0)} |" for r in Ko.itertuples()]
        parca.append("## Kapsam (hisse sayıları)\n" + "\n".join(sat) + "\n")
    ozet = [f"- KARAR ({B['birincil']}): {kr['karar']}."]
    ozet += [f"- Tasarım ({t}): cetvel {kr['cetvel'][t]}; {B['birincil']} {kr['sinyal'][(t, B['birincil'])]}." for t in _K59B_TASARIM]
    ozet += ["- (c) French okuması (bilgi): " + ("; ".join(f"{v}: {x}" for v, x in okuma.items()) or "ölçülmedi") + ".",
             "- İZ ilan edilemez (CLAUDE.md standardı değişmedi). K59-B PORTFÖY-ADAY öneri kapısı sayılmaz; K60 doğrulaması gerekir.",
             f"- Sonraki adım (sonuçtan bağımsız, ön kayıt §9): {B['sonraki']}."]
    notlar = "\n".join(f"- {x}" for x in meta.get("not", [])) or "- yok"
    metin = f"""# K59-B — K59 §6'daki üç deneme (küçük-orta, 3 ay tutma, French): RAPOR

Ön kayıt: {oc['zaman_utc']} UTC (K59-B mührü {oc['sha'][:12]}, dosya sha256 {oc['dosya_sha256'][:12]}, git {str((meta.get('onkayit') or {}).get('git', {}).get('commit', '—'))[:10]}; K59 mührü {oc['k59_sha'][:12]} değişmedi); koşu {meta.get('kos_baslangic', '—')} → {meta.get('kos_bitis', '—')}. {K59B_SURUM}

## Düz dille
{_k59b_duz_dil(Z, kr, okuma, E, B)}

## Karar (ön kayıt §5-§6)
{chr(10).join(ozet)}

Cetvel v2 şartları (maliyetten sonra; K59 ile aynı): ortalama fazla > 0 ve NW t > {Cv['t_esik']}; 3 alt dönemin en az {Cv['alt_donem_min']}'sinde > 0; son %{Cv['son_pay'] * 100:.0f} ayda > 0;
alfa > 0 ve NW t(alfa) > {Cv['t_esik']}. Tasarım düzeyi 'TUTAR' = iki evrende de cetvel v2 + net yıllık fazla >= +{Kr['buyukluk_yillik'] * 100:.0f} puan; 'GÜÇLÜ' = iki evrende iki t de > {Kr['t_guclu']} ({Kr['deneme']} deneme).

{ozet_tablo}

{chr(10).join(parca)}
## Koşu notları
{notlar}

## Sınırlar
- K59-B kör değildir: K59 sonucu görüldükten sonra, K59 ön kaydında önceden yazılı üç deneme koşuldu; ayrıntılar (BOŞLUK listesi) ölçümden önce yazıldı.
- Aynı 2021-2026 örnekleminde K59'un 12 denemesine {Kr['deneme']} deneme eklendi; tutan sonuç 'ikinci tur adayı'dır.
- U1 ve U2 yalnız bugün yaşayan hisseler (hayatta kalma yanlılığı) ve bağımsız değil. (a)'da kıyas alt evrendir; (b)'de kohortlar arası
  eşitleme maliyeti sayılmadı. (c) K59 COMP4'ün kendisi değil, iki hazır French portföyünün yarı yarıya harmanıdır; maliyet varsayımdır.
- Tutan sonuç İZ değildir.

## IZ_KARNE önerisi: kayıt metni (numarayı ve kaydı ana oturum işler)
```
{_k59b_karne(kr, okuma, oc, Z, B)}
```
"""
    yol = _k59b_yol("rapor", cikti)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k59log.info("K59-B rapor: %s", yol)
    return yol


def _cakisma_kontrol_k59(_once=_CK_ONCE_K59, _dosya="K59.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K59", "_CK_KAYIT", "_cakisma_kontrol_k59", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "hashlib", "json", "logging", "math", "re", "subprocess", "time", "zipfile", "annotations", "Any", "Dict",
           "List", "Optional", "Tuple", "FI", "K57", "K58", "_dt")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k59()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    ap = argparse.ArgumentParser(description=K59_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "kapsam", "b_onkayit", "b_kos", "b_rapor", "b_kapsam"])
    ap.add_argument("hedef", nargs="?", default=None, help="kapsam / b_kapsam: CSV yolu")
    ap.add_argument("--cikti", default=None)
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(k59_onkayit(a.cikti)); print("ESIK_SHA256:", k59_esik_sha())
        elif a.komut == "kos":
            R = k59_kos(a.cikti)
            print("K59 KARAR:", json.dumps(R["meta"]["karar"], ensure_ascii=False, default=str)); print(R["rapor"])
        elif a.komut == "kapsam":
            Zk = k59_kapsam_kos(a.hedef)
            print(Zk.groupby("evren", sort=False).agg(ay=("ay_sonu", "size"), ilk=("ay_sonu", "min"), son=("ay_sonu", "max"), ort_evren=("n_evren", "mean")).to_string())
        elif a.komut == "b_onkayit":
            print(k59b_onkayit(a.cikti)); print("K59B_ESIK_SHA256:", k59b_esik_sha()); print("K59_ESIK_SHA256:", k59_esik_sha())
        elif a.komut == "b_kos":
            Rb = k59b_kos(a.cikti)
            print("K59-B KARAR:", json.dumps(Rb["meta"]["karar"], ensure_ascii=False, default=str)); print(Rb["rapor"])
        elif a.komut == "b_rapor":
            print(k59b_rapor(a.cikti))
        elif a.komut == "b_kapsam":
            Zb = k59b_kapsam_kos(a.hedef)
            print(k59b_kapsam_ozet(Zb).to_string(index=False))
            print(Zb.groupby("evren", sort=False).agg(ay=("ay_sonu", "size"), ilk=("ay_sonu", "min"), son=("ay_sonu", "max"), ort_evren=("n_evren", "mean"),
                                                      ort_boyutlu=("n_boyutlu", "mean"), ort_alt=("n_alt", "mean"), min_alt=("n_alt", "min"),
                                                      alt_ay=("alt_olusum", "sum")).to_string())
        else:
            print(k59_rapor(a.cikti))
    except (K59Hata, K58.K58Hata, K57.K57Hata, FileNotFoundError) as ex:
        k59log.error("%s", ex); sys.exit(1)
