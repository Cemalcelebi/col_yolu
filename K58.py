"""K58 — CETVEL SAĞLAMASI (ölçüm aletinin kalibrasyonu), tek dosya (10 Kasım 2026; ana oturum iş tanımı).

Soru: ~150 çalışmada iz çıkmadı. 'İz bulamamamızın nedeni piyasa değil ölçüm aletimiz (FI_OLCUT olay cetveli) mi?'
Ana model denetimi: FI_OLCUT 60 gün eşli farkının %95 aralık yarı genişliği n <= 30'da ≈ %17, n 30-100'de ≈ %13, n 300-1000'de ≈ %3,4,
n > 1000'de ≈ %2,3. Gerçekçi sağlam anomaliler 60 günde %1-3; üstelik 60 gün momentum x likidite eşlemesi bilinen etkileri tasarım
gereği siler (K42). K58 aleti bilinen girdilerle sınar:
  A  GÜÇ: gerçek V_ABD panelinde rastgele plasebo olaylara bilinen δ eklenir, FI_OLCUT dört şartlı hücre testi (FON_IZI'den içe alınır,
     kopya yok) 200 tekrar -> güç = hücrenin TUTTUĞU tekrar payı; δ = 0 yanlış pozitif oranı.
  B  POZİTİF KONTROL: Kenneth French veri kütüphanesi aylık faktörleri (MKT-RF, SMB, HML, RMW, CMA, UMD), 1963-2026; hayatta kalma
     yanlılığı yok, onlarca yıl.
  C  PORTFÖY CETVELİ (önerilen, henüz benimsenmedi): aylık dengelenen uzun-yalnız üst %10 portföyü vs eşit ağırlıklı evren; C1 12-1
     momentum (pozitif kontrol), C2 200 rastgele sinyal (plasebo yanlış pozitif), C4 trend filtresi (a endeks SMA200, b hisse SMA atılımı).
  D  Karar kuralları (ön kayıtta; sonuçtan sonra değişmez).

Komut:  python K58.py onkayit           ön kaydı yazar (ölçümden ÖNCE; eşiklerin sha256'sı içinde; varsa üzerine yazmaz)
        python -I K58.py kos [--bolum A|B|C|hepsi] [--islem 4]
                                        ölçüm (mühür doğrulanır; A kaldığı yerden sürer) + rapor
        python K58.py rapor             K58_RAPOR.md'yi çıktılardan yeniden yazar
Colab:  exec(open('K58.py').read()); k58_kos()
Veri:   /tmp/veri/V_ABD.pkl, V_BIST.pkl (islenmis-veri 'veri' paketi; yoksa `git worktree add /tmp/iv origin/islenmis-veri` +
        `python FON_IZI.py vpac /tmp/iv/veri /tmp/veri`). French zip'leri /tmp/k58_french/, Yahoo (SPY, XU100.IS) /tmp/k58_yahoo/
        (güvenilmeyen veri: yalnız zipfile / json ile bellekte okunur, French ayrıştırma ayrı `python -I` alt sürecinde, boş klasörde).
        Kişisel e-posta / anahtar yok. Çıktılar arastirma_cikti/k58_cetvel_sagla/.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K58 = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import ssl  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import time  # noqa: E402
import urllib.error  # noqa: E402
import urllib.parse  # noqa: E402
import urllib.request  # noqa: E402
import zipfile  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K58 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K58 not in sys.path:
    sys.path.insert(0, KOK_K58)

import FON_IZI as FI  # noqa: E402

k58log = logging.getLogger("col.k58")
if not k58log.handlers:
    _k58_h = logging.StreamHandler(sys.stderr)
    _k58_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k58: %(message)s", "%H:%M:%S"))
    k58log.addHandler(_k58_h)
    k58log.setLevel(logging.INFO)
    k58log.propagate = False

K58_SURUM = "K58 v1.0 (2026-11-10): cetvel sağlaması (FI_OLCUT gücü, French pozitif kontrol, portföy cetveli kalibrasyonu, C4 trend filtresi)"
K58_UA = "col-yolu-arastirma/1.0"
K58_YAHOO_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
K58_YOL = {
    "cikti": os.path.join(KOK_K58, "arastirma_cikti", "k58_cetvel_sagla"),
    "veri": os.environ.get("K58_VERI", "/tmp/veri"),
    "french": os.environ.get("K58_FRENCH", "/tmp/k58_french"),
    "yahoo": os.environ.get("K58_YAHOO", "/tmp/k58_yahoo"),
    "ca": "/root/.ccr/ca-bundle.crt",
}

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256'sı K58_ON_KAYIT.md'de; sonradan değişmez)
K58_ESIK: Dict[str, Any] = {
    "A": {"pazar": "ABD", "n": [30, 100, 300, 1000, 3000], "delta": [0.0, 0.01, 0.02, 0.04, 0.08, 0.16], "tekrar": 200,
          "bas": "2016-01-01", "bit": "2026-08-31", "min_es": 3, "tohum": 58},
    "B": {"kok": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/",
          "zip": {"ff5": "F-F_Research_Data_5_Factors_2x3_CSV.zip", "mom": "F-F_Momentum_Factor_CSV.zip"},
          "faktor": ["MKT_RF", "SMB", "HML", "RMW", "CMA", "UMD"],
          "donem": [["1963-2026", "1963-07", "2026-12"], ["2000-2026", "2000-01", "2026-12"], ["2000-09", "2000-01", "2009-12"],
                    ["2010-19", "2010-01", "2019-12"], ["2020-26", "2020-01", "2026-12"]],
          "alt_donem": ["2000-09", "2010-19", "2020-26"], "cetvel_donem": "2000-2026", "nw_lag": 6, "eksik": [-99.99, -999.0]},
    "C": {"pazar": ["ABD", "BIST"], "dilim": 0.10, "maliyet": {"ABD": 0.001, "BIST": 0.003}, "bas": "2016-01-01", "kriz": "2026-08-31",
          "mom_uzun": 12, "mom_kisa": 1, "gecmis_ay": 12, "min_evren": 50, "nw_lag": 6, "t_esik": 2.0, "alt_donem_n": 3,
          "alt_donem_min": 2, "son_pay": 0.30, "plasebo_n": 200, "plasebo_tohum": 5800, "karar_pazar": "ABD"},
    "C4": {"endeks": {"ABD": "SPY", "BIST": "XU100.IS"}, "sma": 200, "maliyet": {"ABD": 0.001, "BIST": 0.003},
           "abd_bas": "2000-01-01", "kes": "2026-08-31", "yahoo_bas": "1990-01-01", "yahoo_bit": "2026-09-01",
           "alt_donem": [["2000-09", "2000-01-01", "2009-12-31"], ["2010-19", "2010-01-01", "2019-12-31"], ["2020-26", "2020-01-01", "2026-08-31"]],
           "getiri_oran": 0.90, "mdd_kucuk": 1.0 / 3.0, "yil_gun": 252, "sifir_atma": [10.0, 1000.0],
           "sma_kisa": [20, 50], "atilim_gun": 20, "esli_plasebo_n": 200, "esli_plasebo_tohum": 5900},
    "D": {"guc_delta": 0.02, "guc_n_max": 300, "guc_esik": 0.20, "yp_esik": 0.05},
}
K58_DOSYA = {"onkayit": "K58_ON_KAYIT.md", "a_ham": "A_guc_ham.csv", "a": "A_guc.csv", "b": "B_french.csv", "b_cetvel": "B_french_cetvel.csv",
             "c": "C_portfoy.csv", "c_plasebo": "C_plasebo.csv", "c4a": "C4a_endeks.csv", "c4b_plasebo": "C4b_esli_plasebo.csv",
             "rapor": "K58_RAPOR.md", "meta": "k58_kos_meta.json"}
_K58_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")


class K58Hata(RuntimeError):
    """K58'e özgü durdurucu hata (ön kayıt yok / değişmiş, veri bozuk, indirme başarısız)."""


def _k58_olcut() -> Dict[str, Any]:
    return dict(FI.FI_OLCUT)


def k58_esik_sha() -> str:
    """Ön kayıt mührü: K58_ESIK + FI_OLCUT birlikte; biri değişirse koşu durur."""
    s = json.dumps({"K58_ESIK": K58_ESIK, "FI_OLCUT": _k58_olcut()}, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _k58_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K58_YOL["cikti"], K58_DOSYA[ad])


def _k58_dosya_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for parca in iter(lambda: f.read(1 << 20), b""):
            h.update(parca)
    return h.hexdigest()


def _yz(x: Any, nokta: int = 1) -> str:
    """Türkçe yüzde: +%5,0."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    if not np.isfinite(v):
        return "—"
    return ("+" if v >= 0 else "-") + "%" + f"{abs(v) * 100:.{nokta}f}".replace(".", ",")


def _sy(x: Any, nokta: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return f"{v:.{nokta}f}".replace(".", ",") if np.isfinite(v) else "—"


def _k58_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


# ---------------------------------------------------------------- 0) ÖN KAYIT
def k58_onkayit_metin(zaman: str, veri_sha: Dict[str, str]) -> str:
    A = K58_ESIK["A"]; B = K58_ESIK["B"]; C = K58_ESIK["C"]; C4 = K58_ESIK["C4"]; D = K58_ESIK["D"]; O = _k58_olcut()
    vs = "; ".join(f"{k} sha256 {v}" for k, v in veri_sha.items()) or "veri dosyası bulunamadı (koşu açarken yazılır)"
    return f"""# K58 ÖN KAYIT — cetvel sağlaması (ölçüm aletinin kalibrasyonu)

Yazım zamanı: {zaman} (ölçümden ÖNCE; gerçek getiriler üzerinde hiçbir ölçüm koşulmadı). Sürüm: {K58_SURUM}
ESIK_SHA256: {k58_esik_sha()}
(K58_ESIK + FI_OLCUT'un sha256'sı. `python -I K58.py kos` bu mühürle başlar; eşik değişirse koşu durur.)
Veri: {vs}

## 0. Soru
~150 çalışmada iz çıkmadı. Hipotez: 'hiçbir şey bulamamamızın nedeni piyasa değil ölçüm aletimiz'. Ana model denetimi (K57 hücreleri):
FI_OLCUT 60 gün eşli farkının %95 aralık yarı genişliği n <= 30'da ≈ %17, n 30-100'de ≈ %13, n 300-1000'de ≈ %3,4, n > 1000'de ≈ %2,3.
Gerçekçi sağlam anomaliler 60 günde ≈ %1-3. Ayrıca 60 gün momentum x likidite eşlemesi bilinen etkileri tasarım gereği siler (K42).
K58 aleti bilinen girdilerle sınar; yeni iz aramaz.

## A. FI_OLCUT GÜCÜ (gerçek {A['pazar']} paneli, plasebo olay + bilinen δ)
- Panel: V_{A['pazar']}.pkl, FON_IZI fi_olcut_panel (FI_OLCUT değiştirilmeden; kod içe alınır, kopyalanmaz).
- Plasebo olay: rastgele (gün, hisse) hücresi; giriş günü {A['bas']} .. {A['bit']} (kriz kesiği {O['kriz']}: r60 penceresi kesiği aşan
  olay zaten 'ok' değildir). Geçerli hücre = FI 'ok' (r60, momentum, likidite, açılış var) VE aynı gün aynı momentum x likidite
  hücresinde en az {A['min_es']} eş (fi_olcut_olay'ın eş şartı). Bütün geçerli hücreler arasından eşit olasılıkla, yerine koymadan çekilir
  (uzun geçmişli hisse daha çok çıkar; gerçek olaylar gibi).
- n ∈ {A['n']}; δ ∈ {[f'{d * 100:g}%' for d in A['delta']]}; her (n, tekrar) için olay kümesi BİR KEZ çekilir ve bütün δ'larda
  aynı küme kullanılır (ortak rastgele sayı). Tohum = numpy default_rng([{A['tohum']}, n, tekrar]). {A['tekrar']} tekrar.
- δ enjeksiyonu: olayın r60'ına δ eklenir (eşler dokunulmadan): r60' = r60 + δ, fark' = r60' - eşli r60, sıra' = eşlerin r60'ından
  küçük olanların payı (eşitlik yarım) r60' ile yeniden; slot portföyü r60' ile, rastgele eş portföyleri eşlerin değişmemiş r60'ı ile.
- Hücre testi: FON_IZI fi_olcut_hucre (bootstrap {O['bootstrap']}, tohum {O['tohum']}, slot {O['slot']}, {O['port_n']} rastgele portföy) ve
  TUTAR kararı FON_IZI fi_olcut_karar ile (dört karar hücresi aynı sonuçla doldurulur; 'İZ' dönerse hücre TUTAR): n >= {O['n_esik']},
  ortalama eşli fark > 0 ve %95 alt uç > 0, sıra > 0,50, portföy > rastgele %{O['port_yuzde'] * 100:.0f}.
- GÜÇ(n, δ) = tutan tekrar payı; δ = 0 yanlış pozitif oranı. Bilgi: şart başına geçme payı, ortalama aralık yarı genişliği
  ((üst - alt) / 2), dört hücrenin birlikte tutma olasılığı ≈ güç^4 (bağımsızlık varsayımıyla; gerçek İZ kararı dört hücre ister).
- Not: plasebo olaylar on yıla yayılır (gerçek karar hücresi bir-üç yıl); ay kümeli aralık ay sayısına bağlıdır, bu yüzden buradaki güç
  gerçek hücreninkinden İYİMSER (üst sınır) okunur.

## B. POZİTİF KONTROL: Kenneth French veri kütüphanesi (hayatta kalma yanlılığı yok)
- Dosyalar: {B['kok']}{B['zip']['ff5']} ve {B['zip']['mom']} (aylık, %); /tmp/k58_french/ altına inerler,
  güvenilmeyen veri: zip açılmaz, bellekte okunur, ayrıştırma ayrı `python -I` alt sürecinde boş bir klasörde.
- Faktörler: {', '.join(B['faktor'])} (UMD = 'Mom'). Aylık bölüm alınır, yıllık bölüm atılır; {B['eksik']} eksik sayılır.
- Dönemler: {', '.join(d[0] for d in B['donem'])}. Her faktör x dönem: aylık ortalama %, yıllık (x12), t (ortalama / (sd / √T)),
  Newey-West t (gecikme {B['nw_lag']}), Sharpe (ortalama / sd x √12; faktörler zaten fazla getiri), artı ay payı.
- İşaret tutarlılığı: alt dönemlerde ({', '.join(B['alt_donem'])}) ortalaması > 0 olanların sayısı ve tam dönemle aynı işaret.
- BİLGİ: portföy cetvelinin (C) şartları {B['cetvel_donem']} dönemine uzun-kısa faktörlere uygulanır (ortalama > 0, NW t > {C['t_esik']},
  3 alt dönemin en az {C['alt_donem_min']}'sinde > 0, son %{C['son_pay'] * 100:.0f} ayda > 0). Karar rolü yok; 'bilinen etki cetvelden geçer mi'.
- Beklenti (önceden): MKT-RF, RMW, UMD 1963-2026'da t > 2; HML ve SMB 2000 sonrası zayıf; UMD 2020-26'da zayıf/eksi olabilir.

## C. PORTFÖY CETVELİ (önerilen; burada kalibre edilir, benimsenmez)
- Panel: V_ABD ve V_BIST (fi_k1_veri çıktısı), günlük kapanış {C['kriz']}'de kesik (iki pazar için aynı FI_OLCUT kesiği).
- Ay sonu = her ayın panel takvimindeki son işlem günü. Ay sonu kapanışı = o güne kadar son kapanış (en çok 5 gün ileri taşıma).
  Ay getirisi (k -> k+1) = sonraki ay sonu kapanışı (sınırsız ileri taşıma: işlem görmeyen hisse son fiyatında kalır) / ay sonu kapanışı - 1.
- Evren U(k) = ay sonu k, k-1 ve k-{C['gecmis_ay']} kapanışı olan hisseler (bütün sinyaller için aynı; yalnız k ve öncesi bilgi).
  U < {C['min_evren']} olan ay atlanır. Oluşum ayları: ay sonu >= {C['bas']} ve sonraki ay sonu <= kesik.
- Sinyal ay sonu k'da yalnız k ve öncesi kapanışlarla hesaplanır (GELECEĞE BAKMA YOK; test_k58 sınar). İşlem ay sonu kapanışında.
- Portföy: U içinde sinyale göre en üst %{C['dilim'] * 100:.0f} (sayı = max(1, yuvarla({C['dilim']} x |U|))), eşit ağırlık, aylık yeniden dengeleme.
  Maliyet tek yön ABD {C['maliyet']['ABD'] * 1e4:.0f} bp, BIST {C['maliyet']['BIST'] * 1e4:.0f} bp: maliyet = oran x devir, devir = Σ|w_yeni - w_kaymış|
  (ilk ay alım = 1). Kıyas: U'nun eşit ağırlıklı getirisi (maliyetsiz; strateji için sert).
- İstatistik: aylık fazla e = net portföy - kıyas. Yıllık fazla = 12 x ortalama e; Newey-West t (gecikme {C['nw_lag']}); portföy Sharpe
  (net, rf = 0, x √12) ve bilgi oranı (ort e / sd e x √12).
- CETVEL TUTAR ⇔ (1) tam örneklemde ortalama e > 0 VE NW t > {C['t_esik']}; (2) ayların ardışık eşit {C['alt_donem_n']} parçasının
  en az {C['alt_donem_min']}'sinde ortalama e > 0; (3) son %{C['son_pay'] * 100:.0f} ayda (yukarı yuvarlanmış) ortalama e > 0 (örneklem dışı).
- C1 POZİTİF KONTROL: 12-1 momentum = kapanış(k-{C['mom_kisa']}) / kapanış(k-{C['mom_uzun']}) - 1 (ay sonları).
- C2 PLASEBO: {C['plasebo_n']} rastgele sinyal (her ay U içinde rastgele sıra; tohum {C['plasebo_tohum']} + i). Yanlış pozitif oranı = TUTAN payı,
  hem maliyetli (cetvelin kendisi) hem maliyetsiz (brüt) cetvelle. Maliyet yüksek devirli rastgele portföyü zaten cezalandırdığı için
  karar (D2) BRÜT orana bakar (daha sert olanı; düşük devirli gerçek sinyal maliyetle elenmez).
- C3: K57 V1 benzeri olay kuralının aylık sinyale çevrilmesi K58'in KAPSAMINDA DEĞİL.
- HAYATTA KALMA: V_ABD yalnız bugün yaşayan hisseler (survivors); evren ve portföy aynı yanlılığı taşır, fark kısmen silinir ama sıfır
  değildir (batanlar momentum kaybedenlerinde yoğun). Yanlılıksız kontrol B'dir (French).

## C4. TREND FİLTRESİ (Cemal: 'SMA üstüne atılımla kazanılır mı?'; ana oturum ek işi, ölçümden önce)
- (a) ENDEKS DÜZEYİ: {C4['endeks']['ABD']} (ABD) ve {C4['endeks']['BIST']} (BIST), Yahoo chart API günlük veri ({C4['yahoo_bas']} .. {C4['yahoo_bit']}), {C4['kes']}'de kesik.
  SPY temettü düzeltmeli (adjclose oranı açılış ve kapanışa); XU100 fiyat endeksi (temettüsüz; iki strateji için aynı). Endeks
  günlük kapanış oranı 1/{C4['sifir_atma'][1]:g} - 1/{C4['sifir_atma'][0]:g} ya da {C4['sifir_atma'][0]:g} - {C4['sifir_atma'][1]:g} aralığında ise sıfır atma / yeniden tabanlama sayılır,
  önceki seri o oranla ölçeklenir ve raporda yazılır.
  Kural: gün t kapanışı > SMA{C4['sma']}(t) (t dahil son {C4['sma']} kapanış) ise ELDE, değilse NAKİT (getiri 0; faiz yok: filtre aleyhine).
  İşlem ertesi gün AÇILIŞINDA; maliyet tek yön ABD {C4['maliyet']['ABD'] * 1e4:.0f} bp / BIST {C4['maliyet']['BIST'] * 1e4:.0f} bp. Gece getirisi (kapanış t-1 -> açılış t)
  önceki gün pozisyonuyla, gün içi (açılış t -> kapanış t) yeni pozisyonla kazanılır. Al-tut: hep elde.
  Dönem: SPY {C4['abd_bas']} .. {C4['kes']}; XU100 verinin başladığı yıldan (SMA{C4['sma']}'ün tanımlı olduğu ilk takvim yılı başı) .. {C4['kes']};
  alt dönemler {', '.join(d[0] for d in C4['alt_donem'])} (verinin olduğu kadar). Ölçüler: yıllık getiri (bileşik, {C4['yil_gun']} gün), en büyük
  düşüş (MDD), Sharpe (günlük, rf = 0, x √{C4['yil_gun']}), piyasada kalma payı, işlem sayısı.
  KARAR (tam dönem, endeks başına): 'RİSK FİLTRESİ OLARAK TUTAR' ⇔ filtre yıllık getirisi al-tut'un %{C4['getiri_oran'] * 100:.0f}'ından az değil
  (al-tut yıllık getirisi <= 0 ise filtre >= al-tut) VE |MDD filtre| <= (1 - {C4['mdd_kucuk']:.4f}) x |MDD al-tut| (en az 1/3 küçük). Aksi 'TUTMAZ'.
- (b) HİSSE DÜZEYİ (C'nin evreni, ay sonları, maliyeti ve PORTFÖY CETVELİ şartlarıyla; üst %10 değil, şartı sağlayan bütün hisseler eşit ağırlık):
  C4b-1 'SMA200 üstü': ay sonu kapanışı > günlük SMA{C4['sma']}.
  C4b-2 'atılım': ay sonu kapanışı > SMA{C4['sma']} VE kapanış > SMA{C4['sma_kisa'][0]} ve > SMA{C4['sma_kisa'][1]} VE önceki {C4['atilim_gun']} işlem gününün en az birinde
  kapanış SMA{C4['sma_kisa'][0]} ya da SMA{C4['sma_kisa'][1]}'nin üstünde DEĞİLDİ (son {C4['atilim_gun']} günde ikisinin üstüne çıkmış).
  SMA'lar günlük kapanıştan (5 gün ileri taşımalı), tam pencere şart. Şartı sağlayan hisse yoksa ay nakit (getiri 0).
  KARAR: portföy cetvelinin (C) üç şartı, pazar başına (ABD karar, BIST bilgi).
  BİLGİ (karar rolü yok): eşli plasebo = her ay aynı sayıda hisse U'dan rastgele ({C4['esli_plasebo_n']} tekrar, tohum {C4['esli_plasebo_tohum']} + i);
  sinyalin NW t'sinin plasebo dağılımındaki yüzdeliği (geniş tutulan portföyde üst %10 plasebosu kıyaslanamaz).

## D. KARAR KURALLARI (şimdi yazıldı; sonuçtan sonra değişmez)
1. FI_OLCUT gücü δ = +%{D['guc_delta'] * 100:.0f} ve n <= {D['guc_n_max']} (n ∈ {[n for n in A['n'] if n <= D['guc_n_max']]}) için en yüksek değer < %{D['guc_esik'] * 100:.0f} ise
   BULGU olarak yazılır: 'FI_OLCUT küçük etkiyi göremiyor'.
2. Portföy cetveli ABD'de C1 momentumu kabul ederse (maliyetli) VE C2 plasebo yanlış pozitif oranı (brüt; maliyetli de ayrıca) <= %{D['yp_esik'] * 100:.0f}
   ise 'KALİBRE ADAY STANDART' olarak yazılır. BIST bilgi olarak raporlanır. Benimsemek Cemal'in kararıdır (CLAUDE.md test standardı değişikliği).
   C1 ABD'de tutmazsa ve French UMD 2010-19 / 2020-26'da da zayıfsa başarısızlık döneme yazılır; yine de benimseme önerilmez.
3. C4a: endeks başına yukarıdaki risk filtresi kuralı. C4b: portföy cetveli şartları. Tutan C4 sonucu İZ değildir; CLAUDE.md test standardı
   (FI_OLCUT, ABD + AVR) değişmedikçe yalnız 'cetvel C altında tutar' diye raporlanır.
4. Yukarıdaki bütün eşikler sabittir; sonuç görüldükten sonra değiştirilmez. Kod hatası düzeltmesi gerekirse ön kayıt değişmez, düzeltme
   raporda ayrıca yazılır.

## E. Beklenti (önceden)
A: δ = 0'da yanlış pozitif ≈ %0-3; n = 30-300'de δ = +%2 gücü düşük (< %20) beklenir, n = 3000'de δ = +%2 orta-yüksek. C1: ABD 2016-26
momentum zayıf dönem (2020-22 çöküşleri); cetvelin kabul etmemesi olası. C2: brüt yanlış pozitif ≈ %2-5. C4a: SPY'de MDD belirgin küçülür,
getiri al-tut'un %90'ının altında kalabilir; XU100'de TL enflasyonu yüzünden filtre uzun süre elde kalır. C4b: belirsiz.

## F. Faz 2 komutu (ön kayıt git'e işlendikten SONRA)
`cd /home/user/col_yolu && python -I K58.py kos --bolum hepsi --islem 4`
"""


def k58_veri_sha() -> Dict[str, str]:
    out = {}
    for pz in ("ABD", "BIST"):
        y = os.path.join(K58_YOL["veri"], f"V_{pz}.pkl")
        if os.path.exists(y):
            out[f"V_{pz}.pkl"] = _k58_dosya_sha(y)
    return out


def k58_onkayit(cikti: Optional[str] = None) -> str:
    """Ön kaydı yazar. Dosya varsa ÜZERİNE YAZMAZ: mühür aynıysa yolu döndürür, değilse durur."""
    yol = _k58_yol("onkayit", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True)
    if os.path.exists(yol):
        mevcut = _k58_onkayit_sha(yol)
        if mevcut != k58_esik_sha():
            raise K58Hata(f"ön kayıt zaten var ve mühür farklı ({mevcut} != {k58_esik_sha()}): eşikler ön kayıttan sonra değişmiş")
        k58log.info("ön kayıt zaten var (mühür aynı): %s", yol)
        return yol
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    with open(yol, "w", encoding="utf-8") as f:
        f.write(k58_onkayit_metin(zaman, k58_veri_sha()))
    k58log.info("ön kayıt yazıldı: %s (mühür %s)", yol, k58_esik_sha()[:12])
    return yol


def _k58_onkayit_sha(yol: str) -> Optional[str]:
    with open(yol, encoding="utf-8") as f:
        m = re.search(r"^ESIK_SHA256: ([0-9a-f]{64})$", f.read(), re.M)
    return m.group(1) if m else None


def k58_onkayit_dogrula(cikti: Optional[str] = None) -> Dict[str, Any]:
    yol = _k58_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise K58Hata(f"ön kayıt yok ({yol}): önce `python K58.py onkayit`")
    sha = _k58_onkayit_sha(yol)
    if sha != k58_esik_sha():
        raise K58Hata(f"ön kayıt mührü tutmuyor ({sha} != {k58_esik_sha()}): eşikler ön kayıttan sonra değişmiş, koşu durdu")
    metin = open(yol, encoding="utf-8").read()
    m = re.search(r"^Yazım zamanı: (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC", metin, re.M)
    veri = dict(re.findall(r"(V_[A-Z]+\.pkl) sha256 ([0-9a-f]{64})", metin))
    return {"yol": yol, "sha": sha, "zaman_utc": m.group(1) if m else "", "dosya_sha256": _k58_dosya_sha(yol), "veri": veri}


# ---------------------------------------------------------------- 1) VERİ
def k58_fiyat(pazar: str, beklenen_sha: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    """İşlenmiş fiyat sözlüğü (islenmis-veri veri/ paketi). Ön kayıttaki sha256 verilirse dosya aynı olmalı (yoksa durur)."""
    yol = os.path.join(K58_YOL["veri"], f"V_{pazar}.pkl")
    if not os.path.exists(yol):
        raise FileNotFoundError(f"{yol} yok: `git worktree add /tmp/iv origin/islenmis-veri` + `python FON_IZI.py vpac /tmp/iv/veri /tmp/veri`")
    if beklenen_sha and _k58_dosya_sha(yol) != beklenen_sha:
        raise K58Hata(f"{yol} ön kayıttaki veriyle aynı değil (sha256 farklı): koşu durdu")
    with open(yol, "rb") as f:
        V = pickle.load(f)
    if not isinstance(V, dict) or not V:
        raise K58Hata(f"{yol}: sözlük değil / boş")
    gerek = {"Open", "High", "Low", "Close", "Volume"}
    bozuk = [s for s, d in V.items() if not isinstance(d, pd.DataFrame) or not gerek <= set(d.columns)]
    if bozuk:
        raise K58Hata(f"{yol}: OHLCV eksik hisse {len(bozuk)} (ör. {bozuk[:3]})")
    k58log.info("%s fiyat: %d hisse", pazar, len(V))
    return V


def _k58_ssl() -> ssl.SSLContext:
    return ssl.create_default_context(cafile=K58_YOL["ca"]) if os.path.exists(K58_YOL["ca"]) else ssl.create_default_context()


def _k58_indir(url: str, hedef: str, ua: str, deneme: int = 4) -> str:
    """Tek dosya indirme (yarım dosya bırakmaz); varsa dokunmaz."""
    if os.path.exists(hedef) and os.path.getsize(hedef) > 0:
        return hedef
    os.makedirs(os.path.dirname(hedef), exist_ok=True); son = ""
    for k in range(deneme):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "*/*"})
            with urllib.request.urlopen(req, context=_k58_ssl(), timeout=60) as r:
                ham = r.read()
            if not ham:
                raise ValueError("boş yanıt")
            with open(hedef + ".yarim", "wb") as f:
                f.write(ham)
            os.replace(hedef + ".yarim", hedef)
            k58log.info("indirildi: %s (%d bayt)", os.path.basename(hedef), len(ham))
            return hedef
        except urllib.error.HTTPError as e:
            son = f"HTTP {e.code}"
            if e.code == 404:
                break
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
            son = str(e)[:200]
        time.sleep(3 * (k + 1))
    raise K58Hata(f"indirilemedi: {url} ({son})")


# ---------------------------------------------------------------- A) FI_OLCUT GÜCÜ
def k58_gecerli_hucreler(P: Dict[str, Any], bas: str, bit: str, min_es: int) -> Tuple[np.ndarray, np.ndarray]:
    """Plasebo olay çekilebilecek (gün, hisse) hücreleri: FI 'ok', giriş günü [bas, bit], aynı gün aynı hücrede >= min_es eş."""
    T = P["tarih"]; ok = P["ok"]; H = P["H"]
    g0 = T.searchsorted(pd.Timestamp(bas), side="left"); g1 = T.searchsorted(pd.Timestamp(bit), side="right")
    dd, jj = [], []
    for d in range(g0, g1):
        g = ok[d] & (H[d] >= 0)
        if not g.any():
            continue
        say = np.bincount(H[d][g], minlength=int(H[d].max()) + 1)
        j = np.flatnonzero(g); j = j[say[H[d, j]] - 1 >= min_es]
        dd.append(np.full(len(j), d)); jj.append(j)
    if not dd:
        return np.array([], int), np.array([], int)
    return np.concatenate(dd), np.concatenate(jj)


def k58_tutar(h: Dict[str, Any], O: Dict[str, Any]) -> bool:
    """FI_OLCUT dört şartlı hücre kararı, FON_IZI fi_olcut_karar ile (dört karar hücresi aynı sonuçla; 'İZ' dönerse TUTAR)."""
    if not h or not h.get("n"):
        return False
    pazar = list(O.get("karar", ("ABD", "AVR")))
    Z = pd.DataFrame([{"pazar": p, "donem": d[0], **{k: h[k] for k in ("n", "alt95", "sira", "portfoy", "portfoy_esli_p90")}}
                      for p in pazar for d in O["donem"]])
    return FI.fi_olcut_karar(Z, O) == "İZ"


def k58_delta_ekle(X: pd.DataFrame, delta: float) -> pd.DataFrame:
    """Olayın r60'ına δ ekler; eşler dokunulmaz: fark ve sıra yeni r60 ile, eşli ortalama aynı."""
    Y = X.copy()
    Y["r60"] = X.r60.to_numpy(float) + delta
    Y["fark"] = Y.r60 - Y.esli_r60
    Y["sira"] = [float(((e < x).sum() + 0.5 * (e == x).sum()) / len(e)) if e is not None and len(e) else np.nan
                 for e, x in zip(X["_esler"], Y.r60.to_numpy(float))]
    return Y


def k58_guc_tekrar(P: Dict[str, Any], hucre: Tuple[np.ndarray, np.ndarray], n: int, tekrar: int,
                   A: Optional[Dict[str, Any]] = None, O: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Bir (n, tekrar): olay kümesi bir kez çekilir, her δ için FI_OLCUT hücre testi. Döner: δ başına satır."""
    A = A or K58_ESIK["A"]; O = O or _k58_olcut()
    dd, jj = hucre
    if len(dd) < n:
        raise K58Hata(f"geçerli hücre {len(dd)} < n {n}")
    rng = np.random.default_rng([A["tohum"], n, tekrar])
    sec = rng.choice(len(dd), n, replace=False)
    olay = pd.DataFrame({"sembol": [P["sembol"][j] for j in jj[sec]], "giris": P["tarih"][dd[sec]]})
    X = FI.fi_olcut_olay(P, olay)
    if X.fark.isna().any():
        raise K58Hata(f"plasebo olayda eşli fark yok ({int(X.fark.isna().sum())}): geçerli hücre süzgeci FI ile uyuşmuyor")
    out = []
    for delta in A["delta"]:
        h = FI.fi_olcut_hucre(k58_delta_ekle(X, delta), O)
        ay = int(pd.to_datetime(X.giris).dt.to_period("M").nunique())
        out.append({"n": n, "tekrar": tekrar, "delta": delta, "n_olcum": h.get("n", 0), "ay": ay, "ort_fark": h.get("ort_fark"),
                    "alt95": h.get("alt95"), "ust95": h.get("ust95"), "yari": (h.get("ust95", np.nan) - h.get("alt95", np.nan)) / 2,
                    "sira": h.get("sira"), "portfoy": h.get("portfoy"), "portfoy_esli_p90": h.get("portfoy_esli_p90"),
                    "s_n": bool(h.get("n", 0) >= O["n_esik"]), "s_aralik": bool(h.get("alt95", -1) > 0 and h.get("ort_fark", -1) > 0),
                    "s_sira": bool(h.get("sira", 0) > 0.5), "s_port": bool(h.get("portfoy", -1) > h.get("portfoy_esli_p90", np.inf)),
                    "tutar": k58_tutar(h, O)})
    return out


_K58_HAVUZ: Dict[str, Any] = {}


def _k58_guc_isci(is_: Tuple[int, int]) -> List[Dict[str, Any]]:
    n, t = is_
    return k58_guc_tekrar(_K58_HAVUZ["P"], _K58_HAVUZ["hucre"], n, t, _K58_HAVUZ["A"], _K58_HAVUZ["O"])


def k58_guc(P: Dict[str, Any], ham_yol: str, A: Optional[Dict[str, Any]] = None, islem: int = 1) -> pd.DataFrame:
    """Bütün (n, tekrar) işleri; ham sonuç ham_yol'a parça parça eklenir, kaldığı yerden sürer. islem > 1: fork havuzu."""
    A = A or K58_ESIK["A"]; O = _k58_olcut()
    hucre = k58_gecerli_hucreler(P, A["bas"], A["bit"], A["min_es"])
    k58log.info("A: geçerli plasebo hücresi %d (gün %d, hisse %d)", len(hucre[0]), len(np.unique(hucre[0])), len(np.unique(hucre[1])))
    bitti = set()
    if os.path.exists(ham_yol):
        try:
            E = pd.read_csv(ham_yol)
            tam = E.groupby(["n", "tekrar"]).delta.nunique()
            bitti = {k for k, v in tam.items() if v == len(A["delta"])}
            if len(bitti) < len(tam):     # yarım (n, tekrar) satırları atılır
                E[[(a, b) in bitti for a, b in zip(E.n, E.tekrar)]].to_csv(ham_yol, index=False)
        except (OSError, ValueError, KeyError) as ex:
            k58log.warning("A ham dosyası okunamadı (%s); baştan", ex); os.remove(ham_yol)
    isler = [(n, t) for n in sorted(A["n"], reverse=True) for t in range(A["tekrar"]) if (n, t) not in bitti]
    k58log.info("A: %d iş (%d önceden bitmiş), %d süreç", len(isler), len(bitti), islem)
    _K58_HAVUZ.update({"P": P, "hucre": hucre, "A": A, "O": O})
    t0 = time.time(); yaz_bas = not os.path.exists(ham_yol)

    def ekle(sat: List[Dict[str, Any]]) -> None:
        nonlocal yaz_bas
        pd.DataFrame(sat).to_csv(ham_yol, mode="a", header=yaz_bas, index=False); yaz_bas = False
    try:
        if islem > 1 and isler:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(islem) as havuz:
                for k, sat in enumerate(havuz.imap_unordered(_k58_guc_isci, isler, chunksize=1), 1):
                    ekle(sat)
                    if k % 50 == 0 or k == len(isler):
                        k58log.info("A: %d / %d iş (%.0f sn)", k, len(isler), time.time() - t0)
        else:
            for k, is_ in enumerate(isler, 1):
                ekle(_k58_guc_isci(is_))
                if k % 50 == 0 or k == len(isler):
                    k58log.info("A: %d / %d iş (%.0f sn)", k, len(isler), time.time() - t0)
    finally:
        _K58_HAVUZ.clear()
    return pd.read_csv(ham_yol)


def k58_guc_ozet(E: pd.DataFrame) -> pd.DataFrame:
    """(n, δ) başına güç ve şart başına geçme payı; dört hücre ≈ güç^4."""
    g = E.groupby(["n", "delta"])
    Z = g.agg(tekrar=("tutar", "size"), guc=("tutar", "mean"), s_aralik=("s_aralik", "mean"), s_sira=("s_sira", "mean"),
              s_port=("s_port", "mean"), ort_fark=("ort_fark", "mean"), yari=("yari", "mean"), ay=("ay", "mean")).reset_index()
    Z["guc4"] = Z.guc ** 4
    return Z


# ---------------------------------------------------------------- B) FRENCH POZİTİF KONTROL
def k58_french_oku(zip_yol: str) -> pd.DataFrame:
    """French zip'inin içindeki CSV'nin AYLIK bölümü (yıllık bölüm atılır). Zip açılmaz; bellekte okunur. Değerler % (ham)."""
    with zipfile.ZipFile(zip_yol) as z:
        adlar = [a for a in z.namelist() if a.lower().endswith((".csv", ".txt")) and "/" not in a.strip("/")]
        if len(adlar) != 1:
            raise K58Hata(f"{os.path.basename(zip_yol)}: beklenen tek CSV, bulunan {adlar}")
        bilgi = z.getinfo(adlar[0])
        if bilgi.file_size > 50 * 1024 * 1024:
            raise K58Hata(f"{adlar[0]}: beklenmedik büyüklük {bilgi.file_size}")
        metin = z.read(adlar[0]).decode("latin-1")
    satir = metin.splitlines(); bas = None
    for i, s in enumerate(satir):
        p = [x.strip() for x in s.split(",")]
        if len(p) >= 2 and p[0] == "" and any(x for x in p[1:]) and i + 1 < len(satir) and re.match(r"^\s*\d{6}\s*,", satir[i + 1]):
            bas = i; break
    if bas is None:
        raise K58Hata(f"{os.path.basename(zip_yol)}: aylık başlık satırı bulunamadı")
    kol = [x.strip() for x in satir[bas].split(",")][1:]; kayit = []
    for s in satir[bas + 1:]:
        if not re.match(r"^\s*\d{6}\s*,", s):
            break
        p = [x.strip() for x in s.split(",")]
        kayit.append([p[0]] + [float(x) if x else np.nan for x in p[1:1 + len(kol)]])
    D = pd.DataFrame(kayit, columns=["ay"] + kol)
    D.index = pd.PeriodIndex(pd.to_datetime(D.pop("ay"), format="%Y%m"), freq="M")
    D = D.rename(columns={"Mkt-RF": "MKT_RF", "Mom": "UMD"})
    for e in K58_ESIK["B"]["eksik"]:
        D = D.mask(np.isclose(D, e))
    return D


def k58_french_isolated(zip_yol: str) -> pd.DataFrame:
    """Güvenilmeyen zip'i ayrı `python -I` alt sürecinde, boş geçici klasörde ayrıştırır; sonucu CSV olarak alır."""
    kod = ("import sys; sys.path.insert(0, sys.argv[1]); import K58; "
           "sys.stdout.write(K58.k58_french_oku(sys.argv[2]).to_csv())")
    with tempfile.TemporaryDirectory() as bos:
        r = subprocess.run([sys.executable, "-I", "-c", kod, KOK_K58, os.path.abspath(zip_yol)], cwd=bos, capture_output=True,
                           text=True, timeout=300)
    if r.returncode != 0:
        raise K58Hata(f"French ayrıştırma alt süreci hata: {r.stderr[-500:]}")
    D = pd.read_csv(io.StringIO(r.stdout), index_col=0)
    D.index = pd.PeriodIndex(D.index.astype(str), freq="M")
    return D


def k58_nw_t(x: np.ndarray, lag: int) -> float:
    """Ortalamanın Newey-West (Bartlett) t'si."""
    x = np.asarray(x, float); x = x[np.isfinite(x)]; T = len(x)
    if T < 3:
        return np.nan
    e = x - x.mean(); s = float(e @ e) / T
    for l in range(1, min(lag, T - 1) + 1):
        s += 2 * (1 - l / (lag + 1)) * float(e[l:] @ e[:-l]) / T
    return float(x.mean() / math.sqrt(s / T)) if s > 0 else np.nan


def k58_cetvel(e: np.ndarray, K: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """PORTFÖY CETVELİ: aylık fazla serisi e -> istatistik ve TUTAR (ön kayıt C)."""
    K = K or K58_ESIK["C"]; e = np.asarray(e, float); e = e[np.isfinite(e)]; T = len(e)
    if T < max(12, K["alt_donem_n"] * 2):
        return {"ay": T, "tutar": False}
    sd = float(e.std(ddof=1))
    alt = [float(p.mean()) for p in np.array_split(e, K["alt_donem_n"])]
    son = float(e[-int(math.ceil(K["son_pay"] * T)):].mean())
    nw = k58_nw_t(e, K["nw_lag"])
    s1 = bool(e.mean() > 0 and np.isfinite(nw) and nw > K["t_esik"]); s2 = bool(sum(a > 0 for a in alt) >= K["alt_donem_min"]); s3 = bool(son > 0)
    return {"ay": T, "ort_aylik": float(e.mean()), "yillik_fazla": float(12 * e.mean()), "nw_t": nw,
            "bilgi_orani": float(e.mean() / sd * math.sqrt(12)) if sd > 0 else np.nan,
            "alt1": alt[0], "alt2": alt[1], "alt3": alt[2] if len(alt) > 2 else np.nan, "son30": son,
            "s_t": s1, "s_alt": s2, "s_son": s3, "tutar": bool(s1 and s2 and s3)}


def k58_french_olc(D: pd.DataFrame, B: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Faktör x dönem istatistikleri ve (bilgi) portföy cetveli şartları 2000-2026."""
    B = B or K58_ESIK["B"]; Z = []
    for f in B["faktor"]:
        if f not in D:
            raise K58Hata(f"French verisinde {f} yok (sütunlar {list(D.columns)})")
        for ad, a, b in B["donem"]:
            x = D.loc[pd.Period(a, "M"):pd.Period(b, "M"), f].dropna().to_numpy(float) / 100.0
            if len(x) < 12:
                Z.append({"faktor": f, "donem": ad, "ay": len(x)}); continue
            sd = float(x.std(ddof=1))
            Z.append({"faktor": f, "donem": ad, "ay": len(x), "ilk": str(D.loc[pd.Period(a, "M"):pd.Period(b, "M"), f].dropna().index[0]),
                      "son": str(D.loc[pd.Period(a, "M"):pd.Period(b, "M"), f].dropna().index[-1]), "ort_aylik": float(x.mean()),
                      "yillik": float(12 * x.mean()), "t": float(x.mean() / (sd / math.sqrt(len(x)))), "nw_t": k58_nw_t(x, B["nw_lag"]),
                      "sharpe": float(x.mean() / sd * math.sqrt(12)), "arti_ay": float((x > 0).mean())})
    Z = pd.DataFrame(Z)
    for k in ("ilk", "son", "ort_aylik", "yillik", "t", "nw_t", "sharpe", "arti_ay"):
        if k not in Z:
            Z[k] = np.nan
    tut = []
    for f in B["faktor"]:
        g = Z[(Z.faktor == f) & Z.donem.isin(B["alt_donem"])]
        tam = Z[(Z.faktor == f) & (Z.donem == "1963-2026")].ort_aylik.iloc[0]
        tut.append({"faktor": f, "alt_arti": int((g.ort_aylik > 0).sum()), "alt_ayni_isaret": int((np.sign(g.ort_aylik) == np.sign(tam)).sum())})
        _, a, b = next(d for d in B["donem"] if d[0] == B["cetvel_donem"])
        x = D.loc[pd.Period(a, "M"):pd.Period(b, "M"), f].dropna().to_numpy(float) / 100.0
        tut[-1].update({"cetvel_" + k: v for k, v in k58_cetvel(x).items()})
    T = pd.DataFrame(tut)
    Z = Z.merge(T[["faktor", "alt_arti", "alt_ayni_isaret"]], on="faktor", how="left")
    return Z, T


# ---------------------------------------------------------------- C) PORTFÖY CETVELİ
def k58_aylik(V: Dict[str, pd.DataFrame], K: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ay sonu kapanışları, ay getirileri (k -> k+1), evren U(k) ve günlük kapanış (5 gün ileri taşımalı). Kesik K['kriz']."""
    K = K or K58_ESIK["C"]; kes = pd.Timestamp(K["kriz"])
    S = sorted(V)
    Cd = pd.DataFrame({s: V[s].Close.astype(float) for s in S}).sort_index()
    Cd = Cd[Cd.index <= kes]
    Cd = Cd.where(Cd > 0)
    C5 = Cd.ffill(limit=5); Cinf = Cd.ffill()
    me = pd.DatetimeIndex(Cd.index.to_series().groupby(Cd.index.to_period("M")).max().to_numpy())
    Cm = C5.loc[me]; Cx = Cinf.loc[me]
    R = np.array((Cx.shift(-1) / Cm - 1).to_numpy(float), copy=True)
    g = K["gecmis_ay"]
    U = np.array((Cm.notna() & Cm.shift(1).notna() & Cm.shift(g).notna()).to_numpy(bool), copy=True)
    olusum = np.zeros(len(me), bool); olusum[:-1] = True
    olusum &= np.asarray(me >= pd.Timestamp(K["bas"]))
    olusum &= U.sum(axis=1) >= K["min_evren"]
    U[~olusum] = False
    R[~U] = np.nan
    return {"ay_sonu": me, "sembol": S, "Cm": Cm, "R": R, "U": U, "olusum": olusum, "C5": C5}


def k58_sinyal_momentum(M: Dict[str, Any], K: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """12-1 momentum, ay sonu k'da kapanış(k-1) / kapanış(k-12) - 1 (yalnız k ve öncesi)."""
    K = K or K58_ESIK["C"]; Cm = M["Cm"]
    S = np.array((Cm.shift(K["mom_kisa"]) / Cm.shift(K["mom_uzun"]) - 1).to_numpy(float), copy=True)
    S[~M["U"]] = np.nan
    return S


def k58_sinyal_sma(M: Dict[str, Any], C4: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """C4b: ay sonu k'da (yalnız k ve öncesi günlük kapanış) 'SMA200 üstü' ve 'atılım' seçimleri (bool, U içinde)."""
    C4 = C4 or K58_ESIK["C4"]; C5 = M["C5"]; me = M["ay_sonu"]
    s200 = C5.rolling(C4["sma"], min_periods=C4["sma"]).mean()
    a, b = C4["sma_kisa"]
    sa = C5.rolling(a, min_periods=a).mean(); sb = C5.rolling(b, min_periods=b).mean()
    ust = (C5 > sa) & (C5 > sb)
    once_degil = (~ust).astype(float).shift(1).rolling(C4["atilim_gun"], min_periods=C4["atilim_gun"]).max() >= 1
    u200 = (C5 > s200)
    at = u200 & ust & once_degil
    U = M["U"]
    return {"C4b1_sma200_ustu": u200.loc[me].to_numpy(bool) & U, "C4b2_atilim": at.loc[me].to_numpy(bool) & U}


def k58_ust_dilim(S: np.ndarray, U: np.ndarray, dilim: float) -> np.ndarray:
    """Her ay U içinde sinyali en yüksek %dilim (sayı max(1, yuvarla(dilim x |U|))); eşitlikte sütun sırası (kararlı)."""
    sec = np.zeros_like(U, bool)
    for k in range(len(U)):
        j = np.flatnonzero(U[k] & np.isfinite(S[k]))
        if not len(j):
            continue
        m = max(1, int(round(dilim * U[k].sum())))
        sira = j[np.argsort(-S[k, j], kind="stable")][:m]
        sec[k, sira] = True
    return sec


def k58_portfoy(R: np.ndarray, sec: np.ndarray, U: np.ndarray, olusum: np.ndarray, maliyet: float) -> Dict[str, np.ndarray]:
    """Eşit ağırlıklı aylık dengelenen portföy: brüt, net (maliyet x devir), devir; kıyas = U eşit ağırlıklı (maliyetsiz)."""
    N = R.shape[1]; w_k = np.zeros(N); br, nt, dv, kb = [], [], [], []
    for k in np.flatnonzero(olusum):
        s = sec[k] & U[k]; m = int(s.sum())
        w = s / m if m else np.zeros(N)
        devir = float(np.abs(w - w_k).sum())
        r = float(np.nansum(w * np.nan_to_num(R[k]))) if m else 0.0
        net = (1 - maliyet * devir) * (1 + r) - 1
        if m and (1 + r) != 0:
            w_k = w * (1 + np.nan_to_num(R[k])) / (1 + r)
        else:
            w_k = np.zeros(N)
        br.append(r); nt.append(net); dv.append(devir); kb.append(float(np.nanmean(R[k][U[k]])))
    return {"brut": np.array(br), "net": np.array(nt), "devir": np.array(dv), "kiyas": np.array(kb)}


def k58_portfoy_olc(Pf: Dict[str, np.ndarray], K: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    K = K or K58_ESIK["C"]; net = Pf["net"]; sd = float(np.std(net, ddof=1)) if len(net) > 1 else np.nan
    c = k58_cetvel(Pf["net"] - Pf["kiyas"], K); cb = k58_cetvel(Pf["brut"] - Pf["kiyas"], K)
    return {**c, "port_sharpe": float(net.mean() / sd * math.sqrt(12)) if sd and sd > 0 else np.nan,
            "port_yillik": float(np.prod(1 + net) ** (12 / len(net)) - 1) if len(net) else np.nan,
            "kiyas_yillik": float(np.prod(1 + Pf["kiyas"]) ** (12 / len(net)) - 1) if len(net) else np.nan,
            "ort_devir": float(Pf["devir"][1:].mean()) if len(net) > 1 else np.nan,
            "brut_yillik_fazla": cb.get("yillik_fazla"), "brut_nw_t": cb.get("nw_t"), "brut_tutar": cb.get("tutar", False)}


def k58_plasebo(M: Dict[str, Any], maliyet: float, K: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """C2: plasebo_n rastgele sinyal (tohum plasebo_tohum + i), üst %dilim; maliyetli ve brüt cetvel."""
    K = K or K58_ESIK["C"]; Z = []
    for i in range(K["plasebo_n"]):
        rng = np.random.default_rng(K["plasebo_tohum"] + i)
        S = rng.random(M["R"].shape); S[~M["U"]] = np.nan
        o = k58_portfoy_olc(k58_portfoy(M["R"], k58_ust_dilim(S, M["U"], K["dilim"]), M["U"], M["olusum"], maliyet), K)
        Z.append({"plasebo": i, **o})
    return pd.DataFrame(Z)


def k58_esli_plasebo(M: Dict[str, Any], sec: np.ndarray, maliyet: float, C4: Optional[Dict[str, Any]] = None,
                     K: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """C4b bilgi: her ay aynı sayıda hisse U'dan rastgele (tohum esli_plasebo_tohum + i)."""
    C4 = C4 or K58_ESIK["C4"]; K = K or K58_ESIK["C"]; Z = []
    say = (sec & M["U"]).sum(axis=1)
    for i in range(C4["esli_plasebo_n"]):
        rng = np.random.default_rng(C4["esli_plasebo_tohum"] + i); S = np.zeros_like(sec)
        for k in np.flatnonzero(M["olusum"]):
            j = np.flatnonzero(M["U"][k])
            if say[k] and len(j):
                S[k, rng.choice(j, min(int(say[k]), len(j)), replace=False)] = True
        Z.append({"plasebo": i, **k58_portfoy_olc(k58_portfoy(M["R"], S, M["U"], M["olusum"], maliyet), K)})
    return pd.DataFrame(Z)


# ---------------------------------------------------------------- C4a) ENDEKS TREND FİLTRESİ
def _k58_yahoo_url(T: str) -> str:
    C4 = K58_ESIK["C4"]
    p1 = int(pd.Timestamp(C4["yahoo_bas"], tz="UTC").timestamp()); p2 = int(pd.Timestamp(C4["yahoo_bit"], tz="UTC").timestamp())
    return (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(T, safe='')}"
            f"?period1={p1}&period2={p2}&interval=1d&events=div%2Csplits&includeAdjustedClose=true")


def k58_yahoo_oku(yol: str, C4: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, List[str]]:
    """Yahoo chart JSON -> günlük Open/Close (adjclose oranıyla düzeltilmiş), kesik; sıfır atma düzeltmesi. (df, notlar)."""
    C4 = C4 or K58_ESIK["C4"]; notlar: List[str] = []
    J = json.load(open(yol, encoding="utf-8"))
    res = ((J.get("chart") or {}).get("result") or [None])[0]
    if not res or not res.get("timestamp"):
        raise K58Hata(f"{os.path.basename(yol)}: Yahoo yanıtında veri yok")
    tz = (res.get("meta") or {}).get("exchangeTimezoneName") or "America/New_York"
    idx = pd.to_datetime(res["timestamp"], unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()
    q = (res.get("indicators") or {}).get("quote", [{}])[0]
    d = pd.DataFrame({"Open": q.get("open"), "Close": q.get("close")}, index=idx, dtype=float)
    adj = ((res.get("indicators") or {}).get("adjclose") or [{}])[0].get("adjclose")
    if adj is not None and len(adj) == len(d):
        f = np.asarray(pd.Series(adj, dtype=float), float) / d.Close.to_numpy(float)
        if np.isfinite(f).any():
            d["Open"] = d.Open * f; d["Close"] = d.Close * f; notlar.append("temettü düzeltmeli (adjclose)")
    d = d[~d.index.duplicated(keep="last")].sort_index()
    d = d[(d.Close > 0) & (d.index <= pd.Timestamp(C4["kes"]))].copy()
    d.loc[~(d.Open > 0), "Open"] = d.Close.shift(1)       # açılış yoksa önceki kapanış (gece getirisi 0)
    d = d.dropna()
    lo, hi = C4["sifir_atma"]
    oran = (d.Close / d.Close.shift(1)).to_numpy(float)
    for i in np.flatnonzero(np.isfinite(oran) & (((oran >= lo) & (oran <= hi)) | ((oran <= 1 / lo) & (oran >= 1 / hi)))):
        k = oran[i]; d.iloc[:i, :] = d.iloc[:i, :].to_numpy() * k
        notlar.append(f"{d.index[i].date()} günü kapanış oranı {k:.6g}: sıfır atma / yeniden tabanlama sayıldı, önceki seri ölçeklendi")
    return d, notlar


def k58_trend_getiri(d: pd.DataFrame, maliyet: float, C4: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Günlük filtre ve al-tut getirisi. Sinyal kapanış t > SMA(t); işlem t+1 açılışı; gece getirisi önceki pozisyonla."""
    C4 = C4 or K58_ESIK["C4"]
    o = d.Open.to_numpy(float); c = d.Close.to_numpy(float)
    sma = d.Close.rolling(C4["sma"], min_periods=C4["sma"]).mean().to_numpy(float)
    sig = np.where(np.isfinite(sma), (c > sma).astype(float), np.nan)
    p = np.full(len(c), np.nan); p[1:] = sig[:-1]                    # gün t'nin gün içi pozisyonu = t-1 kapanış sinyali
    gece = np.full(len(c), np.nan); gece[1:] = o[1:] / c[:-1] - 1; gun = c / o - 1
    p_once = np.full(len(c), np.nan); p_once[1:] = p[:-1]
    deg = np.abs(p - p_once)
    r = (1 + p_once * gece) * (1 - maliyet * deg) * (1 + p * gun) - 1
    al = np.full(len(c), np.nan); al[1:] = c[1:] / c[:-1] - 1
    return pd.DataFrame({"filtre": r, "al_tut": al, "poz": p, "degisim": deg, "sma_tanimli": np.isfinite(sma)}, index=d.index)


def k58_trend_olc(G: pd.DataFrame, a: str, b: str, C4: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    C4 = C4 or K58_ESIK["C4"]; Y = C4["yil_gun"]
    g = G[(G.index >= pd.Timestamp(a)) & (G.index <= pd.Timestamp(b))].dropna(subset=["filtre", "al_tut"])
    if len(g) < 60:
        return {"gun": len(g)}
    out = {"gun": len(g), "ilk": str(g.index[0].date()), "son": str(g.index[-1].date()), "elde_pay": float(g.poz.mean()),
           "islem": int((g.degisim > 0).sum())}
    for ad in ("filtre", "al_tut"):
        x = g[ad].to_numpy(float); eq = np.cumprod(1 + x)
        out[ad + "_yillik"] = float(eq[-1] ** (Y / len(x)) - 1)
        out[ad + "_mdd"] = float((eq / np.maximum.accumulate(np.concatenate([[1.0], eq]))[1:] - 1).min())
        sd = float(x.std(ddof=1)); out[ad + "_sharpe"] = float(x.mean() / sd * math.sqrt(Y)) if sd > 0 else np.nan
    return out


def k58_trend_karar(o: Dict[str, Any], C4: Optional[Dict[str, Any]] = None) -> str:
    """C4a karar: getiri al-tut'un %90'ından az değil VE |MDD| en az 1/3 küçük -> 'RİSK FİLTRESİ OLARAK TUTAR'."""
    C4 = C4 or K58_ESIK["C4"]
    if "filtre_yillik" not in o:
        return "ÖLÇÜLEMEDİ"
    fy, ay = o["filtre_yillik"], o["al_tut_yillik"]
    getiri_ok = fy >= C4["getiri_oran"] * ay if ay > 0 else fy >= ay
    mdd_ok = abs(o["filtre_mdd"]) <= (1 - C4["mdd_kucuk"]) * abs(o["al_tut_mdd"])
    return "RİSK FİLTRESİ OLARAK TUTAR" if getiri_ok and mdd_ok else "TUTMAZ"


def k58_endeks_bas(G: pd.DataFrame, pazar: str, C4: Optional[Dict[str, Any]] = None) -> str:
    """Tam dönem başı: ABD sabit; BIST SMA'nın tanımlı olduğu ilk günden sonraki ilk takvim yılı başı (o gün tanımlıysa o yıl)."""
    C4 = C4 or K58_ESIK["C4"]
    if pazar == "ABD":
        return C4["abd_bas"]
    ilk = G.index[np.flatnonzero(G.sma_tanimli.to_numpy())[0]]
    return str(ilk.year if (ilk.month, ilk.day) == (1, 1) else ilk.year + 1) + "-01-01"


# ---------------------------------------------------------------- KOŞU
def _k58_meta_yaz(meta: Dict[str, Any], cikti: Optional[str]) -> None:
    with open(_k58_yol("meta", cikti), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1, default=str)


def k58_kos(cikti: Optional[str] = None, bolum: str = "hepsi", islem: int = 1) -> Dict[str, Any]:
    """Faz 2: mühür doğrulanır, A / B / C (C4 dahil) ölçülür, rapor yazılır."""
    oc = k58_onkayit_dogrula(cikti); cik = cikti or K58_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    meta_yol = _k58_yol("meta", cikti)
    meta = json.load(open(meta_yol, encoding="utf-8")) if os.path.exists(meta_yol) else {}
    meta.update({"surum": K58_SURUM, "onkayit": oc, "isolated": bool(sys.flags.isolated)})
    meta.setdefault("kos_baslangic", _k58_simdi()); meta.setdefault("bolum", {})
    if oc["zaman_utc"] and pd.Timestamp(oc["zaman_utc"]) > pd.Timestamp(meta["kos_baslangic"].replace(" UTC", "")):
        raise K58Hata("ön kayıt koşu başlangıcından sonra: sıra bozuk")
    _k58_meta_yaz(meta, cikti)
    bol = ["A", "B", "C"] if bolum == "hepsi" else [bolum]
    Vs: Dict[str, Dict[str, pd.DataFrame]] = {}

    def V(pz: str) -> Dict[str, pd.DataFrame]:
        if pz not in Vs:
            Vs[pz] = k58_fiyat(pz, oc["veri"].get(f"V_{pz}.pkl"))
        return Vs[pz]
    if "A" in bol:
        t0 = time.time(); A = K58_ESIK["A"]
        P = FI.fi_olcut_panel(V(A["pazar"]), _k58_olcut())
        E = k58_guc(P, _k58_yol("a_ham", cikti), A, islem)
        k58_guc_ozet(E).to_csv(_k58_yol("a", cikti), index=False)
        meta["bolum"]["A"] = {"bitis": _k58_simdi(), "sn": round(time.time() - t0), "satir": len(E)}; _k58_meta_yaz(meta, cikti)
    if "B" in bol:
        t0 = time.time(); B = K58_ESIK["B"]; Dl = []; sha = {}
        for ad, z in B["zip"].items():
            y = _k58_indir(B["kok"] + z, os.path.join(K58_YOL["french"], z), K58_UA)
            if not zipfile.is_zipfile(y):
                raise K58Hata(f"{y}: zip değil")
            sha[z] = _k58_dosya_sha(y); Dl.append(k58_french_isolated(y))
        D = Dl[0].join(Dl[1][["UMD"]], how="left")
        Z, T = k58_french_olc(D, B)
        Z.to_csv(_k58_yol("b", cikti), index=False); T.to_csv(_k58_yol("b_cetvel", cikti), index=False)
        meta["bolum"]["B"] = {"bitis": _k58_simdi(), "sn": round(time.time() - t0), "zip_sha256": sha,
                              "ilk_ay": str(D.index.min()), "son_ay": str(D.dropna(how="all").index.max())}
        _k58_meta_yaz(meta, cikti)
    if "C" in bol:
        t0 = time.time(); C = K58_ESIK["C"]; C4 = K58_ESIK["C4"]; satir, pl, epl = [], [], []
        for pz in C["pazar"]:
            M = k58_aylik(V(pz), C); mal = C["maliyet"][pz]
            ay = M["ay_sonu"][M["olusum"]]
            k58log.info("C %s: %d oluşum ayı (%s .. %s), evren ort %d", pz, len(ay), ay.min().date(), ay.max().date(),
                        int(M["U"][M["olusum"]].sum(axis=1).mean()))
            sec_m = k58_ust_dilim(k58_sinyal_momentum(M, C), M["U"], C["dilim"])
            satir.append({"pazar": pz, "sinyal": "C1_momentum_12_1", "ilk_ay": str(ay.min().date()), "son_ay": str(ay.max().date()),
                          **k58_portfoy_olc(k58_portfoy(M["R"], sec_m, M["U"], M["olusum"], mal), C)})
            P2 = k58_plasebo(M, mal, C).assign(pazar=pz); pl.append(P2)
            k58log.info("C %s plasebo: maliyetli yanlış pozitif %.3f, brüt %.3f", pz, P2.tutar.mean(), P2.brut_tutar.mean())
            for ad, sec in k58_sinyal_sma(M, C4).items():
                o = k58_portfoy_olc(k58_portfoy(M["R"], sec, M["U"], M["olusum"], mal), C)
                Ep = k58_esli_plasebo(M, sec, mal, C4, C).assign(pazar=pz, sinyal=ad); epl.append(Ep)
                o["esli_plasebo_yuzdelik"] = float((Ep.nw_t < o.get("nw_t", np.nan)).mean())
                o["ort_hisse"] = float((sec & M["U"])[M["olusum"]].sum(axis=1).mean())
                satir.append({"pazar": pz, "sinyal": ad, "ilk_ay": str(ay.min().date()), "son_ay": str(ay.max().date()), **o})
        pd.DataFrame(satir).to_csv(_k58_yol("c", cikti), index=False)
        pd.concat(pl, ignore_index=True).to_csv(_k58_yol("c_plasebo", cikti), index=False)
        pd.concat(epl, ignore_index=True).to_csv(_k58_yol("c4b_plasebo", cikti), index=False)
        # C4a endeks
        Za = []; yh = {}
        for pz, T in C4["endeks"].items():
            y = _k58_indir(_k58_yahoo_url(T), os.path.join(K58_YOL["yahoo"], re.sub(r"[^A-Za-z0-9._-]", "_", T) + ".json"), K58_YAHOO_UA)
            yh[T] = _k58_dosya_sha(y)
            d, notlar = k58_yahoo_oku(y, C4); G = k58_trend_getiri(d, C4["maliyet"][pz], C4); bas = k58_endeks_bas(G, pz, C4)
            for dn, a, b in [["tam", bas, C4["kes"]]] + [[x, max(a_, bas), b_] for x, a_, b_ in C4["alt_donem"]]:
                o = k58_trend_olc(G, a, b, C4)
                Za.append({"pazar": pz, "endeks": T, "donem": dn, "bas": a, "veri_ilk": str(d.index[0].date()), **o,
                           "karar": k58_trend_karar(o, C4) if dn == "tam" else "", "not": " | ".join(notlar)})
        pd.DataFrame(Za).to_csv(_k58_yol("c4a", cikti), index=False)
        meta["bolum"]["C"] = {"bitis": _k58_simdi(), "sn": round(time.time() - t0), "yahoo_sha256": yh}
        _k58_meta_yaz(meta, cikti)
    meta["kos_bitis"] = _k58_simdi(); _k58_meta_yaz(meta, cikti)
    return {"meta": meta, "rapor": k58_rapor(cikti)}


# ---------------------------------------------------------------- RAPOR
def _k58_oku(ad: str, cikti: Optional[str]) -> Optional[pd.DataFrame]:
    y = _k58_yol(ad, cikti)
    return pd.read_csv(y) if os.path.exists(y) else None


def k58_karar(cikti: Optional[str] = None) -> Dict[str, Any]:
    """D kuralları çıktılardan: D1 (FI_OLCUT gücü), D2 (portföy cetveli kalibrasyonu), C4a, C4b."""
    D = K58_ESIK["D"]; C = K58_ESIK["C"]; out: Dict[str, Any] = {}
    Ag = _k58_oku("a", cikti)
    if Ag is not None:
        g = Ag[(np.isclose(Ag.delta, D["guc_delta"])) & (Ag.n <= D["guc_n_max"])]
        gerek = {n for n in K58_ESIK["A"]["n"] if n <= D["guc_n_max"]}
        tam = gerek <= set(g.n.astype(int)) and bool((g.tekrar >= K58_ESIK["A"]["tekrar"]).all())
        mx = float(g.guc.max()) if len(g) else np.nan
        out["D1"] = {"max_guc": mx, "tam": tam, "bulgu": bool(tam and np.isfinite(mx) and mx < D["guc_esik"]),
                     "yp": float(Ag[Ag.delta == 0].guc.max()) if (Ag.delta == 0).any() else np.nan}
    Cc = _k58_oku("c", cikti); Cp = _k58_oku("c_plasebo", cikti)
    if Cc is not None and Cp is not None:
        for pz in C["pazar"]:
            m = Cc[(Cc.pazar == pz) & (Cc.sinyal == "C1_momentum_12_1")]; p = Cp[Cp.pazar == pz]
            yp_n, yp_b = float(p.tutar.mean()), float(p.brut_tutar.mean())
            c1 = bool(len(m) and m.tutar.iloc[0])
            out[f"D2_{pz}"] = {"c1_tutar": c1, "yp_net": yp_n, "yp_brut": yp_b,
                               "aday": bool(c1 and yp_n <= D["yp_esik"] and yp_b <= D["yp_esik"])}
        out["D2"] = out.get(f"D2_{C['karar_pazar']}", {}).get("aday", False)
        out["C4b"] = {f"{r.pazar} {r.sinyal}": bool(r.tutar) for r in Cc[Cc.sinyal.str.startswith("C4b")].itertuples()}
    Ca = _k58_oku("c4a", cikti)
    if Ca is not None:
        out["C4a"] = {r.endeks: r.karar for r in Ca[Ca.donem == "tam"].itertuples()}
    return out


def _k58_guc_al(cikti: Optional[str], n: int, delta: float) -> float:
    Ag = _k58_oku("a", cikti)
    if Ag is None:
        return np.nan
    g = Ag[(Ag.n == n) & np.isclose(Ag.delta, delta)]
    return float(g.guc.iloc[0]) if len(g) else np.nan


def _k58_duz_dil(kr: Dict[str, Any], cikti: Optional[str]) -> str:
    """Raporun başındaki düz dil paragrafı (sayılar çıktılardan)."""
    c = []
    if "D1" in kr:
        g2 = " / ".join(f"%{_sy(_k58_guc_al(cikti, n, 0.02) * 100, 0)}" for n in K58_ESIK["A"]["n"])
        g4 = " / ".join(f"%{_sy(_k58_guc_al(cikti, n, 0.04) * 100, 0)}" for n in K58_ESIK["A"]["n"])
        c.append(f"Ölçüm aletimiz (FI_OLCUT olay cetveli), olaylara bilerek eklenen 60 günde +%2'lik gerçek bir üstünlüğü "
                 f"{'/'.join(str(n) for n in K58_ESIK['A']['n'])} olayda sırasıyla {g2} olasılıkla görüyor (+%4 için {g4}); "
                 f"üstünlük yokken yanlış alarm en çok %{_sy(kr['D1']['yp'] * 100, 1)}. Gerçek İZ dört hücre birden ister, olasılık "
                 f"yaklaşık bu sayıların dördüncü kuvvetidir. "
                 + ("Yani alet küçük ama gerçek etkileri büyük ölçüde KAÇIRIYOR: 'iz yok' sonuçlarının bir kısmı piyasadan değil aletten." if kr["D1"]["bulgu"]
                    else "Alet küçük etkileri ön kayıttaki eşiğin üstünde bir olasılıkla görebiliyor."))
    Bt = _k58_oku("b_cetvel", cikti)
    if Bt is not None:
        tut = [r.faktor for r in Bt.itertuples() if r.cetvel_tutar]
        c.append(f"Bilinen faktörlerden (French, 2000-2026) portföy cetvelinden geçenler: {', '.join(tut) if tut else 'hiçbiri'}; "
                 f"yani bu cetvel de yalnız güçlü etkileri görür.")
    if "D2_ABD" in kr:
        Cc = _k58_oku("c", cikti); m = Cc[(Cc.pazar == "ABD") & (Cc.sinyal == "C1_momentum_12_1")].iloc[0]
        c.append(f"Önerilen portföy cetveli ABD'de 12-1 momentumu {'kabul etti' if m.tutar else 'kabul etmedi'} (maliyetli yıllık fazla {_yz(m.yillik_fazla)}, "
                 f"NW t {_sy(m.nw_t)}); rastgele sinyallerin yanlış geçme oranı maliyetli %{_sy(kr['D2_ABD']['yp_net'] * 100, 1)}, maliyetsiz "
                 f"%{_sy(kr['D2_ABD']['yp_brut'] * 100, 1)}. "
                 + ("Bu yüzden cetvel 'kalibre aday standart'; benimsemek Cemal'in kararı." if kr.get("D2") else "Cetvel kalibre aday değil.")
                 + (f" BIST'te momentum {'geçti' if kr.get('D2_BIST', {}).get('c1_tutar') else 'geçmedi'} (bilgi)." if "D2_BIST" in kr else ""))
    Ca = _k58_oku("c4a", cikti)
    if Ca is not None:
        par = []
        for r in Ca[Ca.donem == "tam"].itertuples():
            par.append(f"{r.endeks}: filtre yıllık {_yz(r.filtre_yillik)} / al-tut {_yz(r.al_tut_yillik)}, en büyük düşüş {_yz(r.filtre_mdd)} / "
                       f"{_yz(r.al_tut_mdd)} -> {r.karar}")
        c.append("SMA200 trend filtresi (endeks): " + "; ".join(par) + ".")
    if "C4b" in kr:
        c.append("Hisse düzeyinde 'SMA200 üstü' ve 'SMA atılımı' portföyleri: " + "; ".join(f"{k} {'TUTAR' if v else 'tutmaz'}" for k, v in kr["C4b"].items()) + ".")
    return " ".join(c) if c else "(henüz çıktı yok)"


def _k58_c151(kr: Dict[str, Any], oc: Dict[str, Any], meta: Dict[str, Any], cikti: Optional[str]) -> str:
    """IZ_KARNE Ç151 kaydı (dize değerlerinde yalnız tek tırnak, ters bölü yok)."""
    def t(x: str) -> str:
        return str(x).replace('"', "'").replace("\\", "/").replace("\n", " ")
    sonuc = []
    if "D1" in kr:
        sonuc.append(f"A güç (δ +%2, n 30/100/300/1000/3000): " + "/".join(f"%{_sy(_k58_guc_al(cikti, n, 0.02) * 100, 0)}" for n in K58_ESIK["A"]["n"])
                     + f", δ 0 yanlış pozitif en çok %{_sy(kr['D1']['yp'] * 100, 1)}; D1 " + ("BULGU: FI_OLCUT küçük etkiyi göremiyor" if kr["D1"]["bulgu"] else "bulgu yok"))
    if "D2_ABD" in kr:
        sonuc.append(f"C portföy cetveli: ABD C1 momentum {'TUTAR' if kr['D2_ABD']['c1_tutar'] else 'tutmaz'}, plasebo yanlış pozitif "
                     f"%{_sy(kr['D2_ABD']['yp_net'] * 100, 1)} (brüt %{_sy(kr['D2_ABD']['yp_brut'] * 100, 1)}); D2 {'KALİBRE ADAY STANDART (benimseme Cemal kararı)' if kr.get('D2') else 'aday değil'}; "
                     f"BIST C1 {'TUTAR' if kr.get('D2_BIST', {}).get('c1_tutar') else 'tutmaz'}")
    if "C4a" in kr:
        sonuc.append("C4a SMA200 endeks filtresi: " + ", ".join(f"{k} {v}" for k, v in kr["C4a"].items()))
    if "C4b" in kr:
        sonuc.append("C4b: " + ", ".join(f"{k} {'TUTAR' if v else 'tutmaz'}" for k, v in kr["C4b"].items()))
    notu = t("; ".join(sonuc) + ". İz iddiası yok (ölçüm aleti sağlaması); seviye 0.")
    return (f'_ik_k("Ç151", "2026-11-10", "{t("K58 CETVEL SAĞLAMASI: FI_OLCUT gücü (plasebo olay + bilinen δ), French faktörleri pozitif kontrol, portföy cetveli (aylık üst %10) kalibrasyonu, SMA200 trend filtresi (endeks ve hisse)")}", '
            f'"K58.py, test_k58.py", "{t("İz bulamamamızın nedeni piyasa mı, ölçüm aletimiz mi?")}", '
            f'"{t("Ön kayıt K58_ON_KAYIT.md (sha " + oc["sha"][:12] + ", git 657c2a1, ölçümden önce); FI_OLCUT değişmedi; portföy cetveli yalnız aday")}", "", 0, '
            f'cikti="arastirma_cikti/k58_cetvel_sagla/ (K58_ON_KAYIT.md, K58_RAPOR.md, A_guc.csv, B_french.csv, C_portfoy.csv, C_plasebo.csv, C4a_endeks.csv)", '
            f'notu="{notu}"),')


def k58_rapor(cikti: Optional[str] = None) -> str:
    oc = k58_onkayit_dogrula(cikti); meta_yol = _k58_yol("meta", cikti)
    meta = json.load(open(meta_yol, encoding="utf-8")) if os.path.exists(meta_yol) else {}
    kr = k58_karar(cikti); D = K58_ESIK["D"]; parca = []
    Ag = _k58_oku("a", cikti)
    if Ag is not None:
        tab = ["| n | " + " | ".join(f"δ {_yz(d, 0)}" for d in K58_ESIK["A"]["delta"]) + " | aralık yarı genişliği (δ 0) | ay |",
               "|---|" + "---|" * (len(K58_ESIK["A"]["delta"]) + 2)]
        for n in sorted(Ag.n.unique()):
            g = Ag[Ag.n == n].set_index("delta")
            tab.append(f"| {n} | " + " | ".join(f"%{_sy(g.guc.get(d, np.nan) * 100, 0)}" for d in K58_ESIK["A"]["delta"])
                       + f" | %{_sy(g.yari.get(0.0, np.nan) * 100, 1)} | {_sy(g.ay.get(0.0, np.nan), 0)} |")
        sart = ["| n | δ | aralık şartı | sıra şartı | portföy şartı | güç | dört hücre ≈ güç^4 |", "|---|---|---|---|---|---|---|"]
        for r in Ag[Ag.delta.isin([0.0, 0.02, 0.04])].itertuples():
            sart.append(f"| {r.n} | {_yz(r.delta, 0)} | %{_sy(r.s_aralik * 100, 0)} | %{_sy(r.s_sira * 100, 0)} | %{_sy(r.s_port * 100, 0)} | "
                        f"%{_sy(r.guc * 100, 0)} | %{_sy(r.guc4 * 100, 1)} |")
        d1 = kr.get("D1", {})
        parca.append(f"""## A. FI_OLCUT gücü (V_ABD, plasebo olay + bilinen δ, {K58_ESIK['A']['tekrar']} tekrar)
Güç = hücrenin dört şartla TUTTUĞU tekrar payı (δ 0 = yanlış pozitif).

{chr(10).join(tab)}

Şart başına geçme payı (seçili δ):

{chr(10).join(sart)}

D1: δ +%{D['guc_delta'] * 100:.0f}, n <= {D['guc_n_max']} en yüksek güç %{_sy(d1.get('max_guc', np.nan) * 100, 1)} -> {"BULGU: 'FI_OLCUT küçük etkiyi göremiyor'" if d1.get('bulgu') else ('bulgu şartı sağlanmadı (güç >= %20)' if d1.get('tam') else 'ÖLÇÜM EKSİK (n 30/100/300 x 200 tekrar tamamlanmadı)')}.
""")
    Bz = _k58_oku("b", cikti); Bt = _k58_oku("b_cetvel", cikti)
    if Bz is not None:
        tab = ["| Faktör | Dönem | Ay | Aylık ort. | Yıllık | t | NW t | Sharpe |", "|---|---|---|---|---|---|---|---|"]
        for r in Bz.itertuples():
            tab.append(f"| {r.faktor} | {r.donem} | {r.ay} | {_yz(r.ort_aylik, 2)} | {_yz(r.yillik)} | {_sy(r.t)} | {_sy(r.nw_t)} | {_sy(r.sharpe)} |")
        tt = ["| Faktör | Alt dönem > 0 (3) | Cetvel C 2000-2026: yıllık | NW t | alt dönem | son %30 | TUTAR |", "|---|---|---|---|---|---|---|"]
        for r in Bt.itertuples():
            tt.append(f"| {r.faktor} | {r.alt_arti} | {_yz(r.cetvel_yillik_fazla)} | {_sy(r.cetvel_nw_t)} | {'evet' if r.cetvel_s_alt else 'hayır'} | "
                      f"{'evet' if r.cetvel_s_son else 'hayır'} | {'TUTAR' if r.cetvel_tutar else 'tutmaz'} |")
        parca.append(f"""## B. Pozitif kontrol: French faktörleri (uzun-kısa, hayatta kalma yanlılığı yok)
Veri ayları: {meta.get('bolum', {}).get('B', {}).get('ilk_ay', '—')} .. {meta.get('bolum', {}).get('B', {}).get('son_ay', '—')}.

{chr(10).join(tab)}

Bilgi (karar rolü yok): portföy cetveli şartları uzun-kısa faktörlere, 2000-2026:

{chr(10).join(tt)}
""")
    Cc = _k58_oku("c", cikti); Cp = _k58_oku("c_plasebo", cikti)
    if Cc is not None:
        tab = ["| Pazar | Sinyal | Ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Portföy yıllık | Kıyas yıllık | Sharpe | Devir | Brüt fazla | TUTAR |",
               "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in Cc.itertuples():
            tab.append(f"| {r.pazar} | {r.sinyal} | {r.ay} | {_yz(r.yillik_fazla)} | {_sy(r.nw_t)} | {_yz(r.alt1, 2)} / {_yz(r.alt2, 2)} / {_yz(r.alt3, 2)} | "
                       f"{_yz(r.son30, 2)} | {_yz(r.port_yillik)} | {_yz(r.kiyas_yillik)} | {_sy(r.port_sharpe)} | %{_sy(r.ort_devir * 100, 0)} | "
                       f"{_yz(r.brut_yillik_fazla)} | {'TUTAR' if r.tutar else 'tutmaz'} |")
        pl = [f"- {pz}: {K58_ESIK['C']['plasebo_n']} rastgele sinyal, yanlış pozitif maliyetli %{_sy(kr[f'D2_{pz}']['yp_net'] * 100, 1)}, brüt %{_sy(kr[f'D2_{pz}']['yp_brut'] * 100, 1)}; "
              f"C1 {'TUTAR' if kr[f'D2_{pz}']['c1_tutar'] else 'tutmaz'} -> {'KALİBRE ADAY' if kr[f'D2_{pz}']['aday'] else 'aday değil'}"
              for pz in K58_ESIK["C"]["pazar"] if f"D2_{pz}" in kr]
        epl = [f"- {r.pazar} {r.sinyal}: ortalama {_sy(r.ort_hisse, 0)} hisse; NW t eşli plasebonun %{_sy(r.esli_plasebo_yuzdelik * 100, 0)}'ından büyük"
               for r in Cc[Cc.sinyal.str.startswith("C4b")].itertuples()]
        parca.append(f"""## C. Portföy cetveli (aylık, uzun-yalnız, eşit ağırlıklı evrene karşı; V_ABD hayatta kalanlar)
{chr(10).join(tab)}

C2 plasebo ve D2:
{chr(10).join(pl)}
D2 (karar pazarı {K58_ESIK['C']['karar_pazar']}): {'KALİBRE ADAY STANDART (benimseme Cemal kararı)' if kr.get('D2') else 'kalibre aday değil'}.

C4b eşli plasebo (bilgi):
{chr(10).join(epl)}
""")
    Ca = _k58_oku("c4a", cikti)
    if Ca is not None:
        tab = ["| Endeks | Dönem | Gün | Elde payı | İşlem | Filtre yıllık | Al-tut yıllık | Filtre MDD | Al-tut MDD | Filtre Sharpe | Al-tut Sharpe | Karar |",
               "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in Ca.itertuples():
            tab.append(f"| {r.endeks} | {r.donem} ({r.bas}) | {r.gun} | %{_sy(getattr(r, 'elde_pay', np.nan) * 100, 0)} | {_sy(getattr(r, 'islem', np.nan), 0)} | "
                       f"{_yz(getattr(r, 'filtre_yillik', np.nan))} | {_yz(getattr(r, 'al_tut_yillik', np.nan))} | {_yz(getattr(r, 'filtre_mdd', np.nan))} | "
                       f"{_yz(getattr(r, 'al_tut_mdd', np.nan))} | {_sy(getattr(r, 'filtre_sharpe', np.nan))} | {_sy(getattr(r, 'al_tut_sharpe', np.nan))} | "
                       f"{r.karar if isinstance(r.karar, str) else ''} |")
        notlar = sorted({str(x) for x in Ca["not"].dropna() if str(x)})
        parca.append(f"""## C4a. Endeks trend filtresi (kapanış > SMA200 elde, değilse nakit; ertesi açılışta işlem)
{chr(10).join(tab)}

Veri notları: {'; '.join(notlar) if notlar else 'yok'}.
""")
    for dos, baslik in (("a", "## A. FI_OLCUT gücü"), ("b", "## B. Pozitif kontrol: French faktörleri"), ("c", "## C. Portföy cetveli"),
                        ("c4a", "## C4a. Endeks trend filtresi")):
        if not os.path.exists(_k58_yol(dos, cikti)):
            parca.append(f"{baslik}: VERİ YOK (bölüm koşulmadı ya da veri inemedi; ötekiler sürdü)\n")
    ozet = []
    if "D1" in kr:
        ozet.append(f"- A (FI_OLCUT gücü): {'küçük etkiyi GÖREMİYOR (D1 bulgusu)' if kr['D1']['bulgu'] else ('D1 bulgu şartı sağlanmadı' if kr['D1']['tam'] else 'ölçüm eksik')}; "
                    f"δ 0 yanlış pozitif en çok %{_sy(kr['D1']['yp'] * 100, 1)}.")
    if "D2" in kr:
        ozet.append(f"- C (portföy cetveli): {'KALİBRE ADAY' if kr['D2'] else 'kalibre aday değil'} (ABD karar; BIST bilgi).")
    if "C4a" in kr:
        ozet.append("- C4a: " + "; ".join(f"{k} {v}" for k, v in kr["C4a"].items()) + ".")
    if "C4b" in kr:
        ozet.append("- C4b: " + "; ".join(f"{k} {'TUTAR' if v else 'tutmaz'}" for k, v in kr["C4b"].items()) + ".")
    metin = f"""# K58 — cetvel sağlaması: RAPOR

Ön kayıt: {oc['zaman_utc']} UTC (mühür {oc['sha'][:12]}, dosya sha256 {oc['dosya_sha256'][:12]}); koşu {meta.get('kos_baslangic', '—')} → {meta.get('kos_bitis', '—')}. {K58_SURUM}

## Düz dille
{_k58_duz_dil(kr, cikti)}

## Özet (D kuralları, ön kayıttan)
{chr(10).join(ozet) if ozet else '- (henüz çıktı yok)'}

{chr(10).join(parca)}
## Sınırlar
- A'daki plasebo olaylar on yıla yayılır; gerçek karar hücresi (bir-üç yıl) daha az ay içerir, aralığı daha geniştir: buradaki güç üst sınırdır.
- V_ABD yalnız bugün yaşayan hisseler (hayatta kalma yanlılığı); French verisi bunun yanlılıksız kontrolüdür.
- C4a nakit getirisi 0 (faiz yok; filtre aleyhine). XU100 fiyat endeksidir (temettüsüz), TL bazında.
- Tutan C4 sonucu İZ değildir; CLAUDE.md test standardı (FI_OLCUT, ABD + AVR) değişmedikçe 'cetvel C altında tutar' diye okunur.

## IZ_KARNE önerisi (Ç151; IZ_KARNE.py'ye ana oturum işler)
```
{_k58_c151(kr, oc, meta, cikti)}
```
"""
    yol = _k58_yol("rapor", cikti)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k58log.info("K58 rapor: %s", yol)
    return yol


def _cakisma_kontrol_k58(_once=_CK_ONCE_K58, _dosya="K58.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K58", "_CK_KAYIT", "_cakisma_kontrol_k58", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "hashlib", "io", "json", "logging", "math", "pickle", "re", "ssl", "subprocess", "tempfile", "time",
           "urllib", "zipfile", "annotations", "Any", "Dict", "List", "Optional", "Tuple", "FI", "_dt")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k58()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    ap = argparse.ArgumentParser(description=K58_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--bolum", choices=["A", "B", "C", "hepsi"], default="hepsi")
    ap.add_argument("--islem", type=int, default=1)
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(k58_onkayit(a.cikti)); print("ESIK_SHA256:", k58_esik_sha())
        elif a.komut == "kos":
            R = k58_kos(a.cikti, a.bolum, max(1, a.islem))
            print("K58 KARAR:", json.dumps(k58_karar(a.cikti), ensure_ascii=False, default=str)); print(R["rapor"])
        else:
            print(k58_rapor(a.cikti))
    except K58Hata as ex:
        k58log.error("%s", ex); sys.exit(1)
