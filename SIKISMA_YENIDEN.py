"""SIKISMA_YENIDEN — sıkışmadan sonra büyük hareket: BAĞIMSIZ YENİDEN ÖLÇÜM, tek dosya (14 Kasım 2026; ana oturum iş tanımı).

Soru (Cemal, 14 Kas 2026): küçük mumlar bir noktada sıkışıyor; sonra büyük mumlar geliyor mu, ne zaman, yönsüz stoplu işlemle yararlanılır mı.
Yön tahmini BU İŞTE YOK. Üç ölçü:
  (A) HABERCİ   P(B1 | sıkışma) / P(B1 | eş) = KAT; eş = aynı gün, aynı pazar, aynı 250 gün oynaklık ondalığı x likidite üçlüsü, sıkışma DIŞI.
               Ayrıca aynı hissede rastgele günler (200 çekiliş, aynı takvim yılı) ve ay kümeli bootstrap %95. B2, B3 aynı; B0 (göreli) bilgi.
  (B) ZAMAN    ilk büyük günün t'den kaç gün sonra geldiği; pencere (1-5 / 6-10 / 11-15 / 16-20) eşli oranları; sıkışma süresi kovalarına
               göre 5 günlük B1 olasılığı (eşli); yalnız t'ye kadarki bilgilerle lojistik model walk-forward (2016-22 eğit, 2023+ test),
               Brier skill (taban: eğitimde aynı oynaklık ondalığının oranı). Bilanço takvimi YOK (veri yok).
  (C) YÖNSÜZ   10 gün bandının %1 dışında ilk kapanış -> o yönde ertesi açılış girişi; stop bandın öteki kenarı; çıkış stop ya da 20 gün.
               Eş: aynı gün, aynı momentum beşliği x likidite üçlüsü, sıkışma dışı hisseler aynı kuralla (kendi 10 gün bandı). FI_OLCUT dört şart.
Tanımlar ve eşikler SY_ESIK'tedir; ön kayıtta sha256 ile mühürlenir. Kod sha256'sı da ön kayıtta; koşuda farklıysa koşu durur.

Komut:  python SIKISMA_YENIDEN.py onkayit   ön kayıt (tanım, mühür, kod sha, kontrol listesi, olay SAYIMI: sonuç / getiri hesaplanmaz)
        python SIKISMA_YENIDEN.py kos       kontrol kapısı (IZ_KARNE.ik_kontrol_kapisi) + mühür + kod sha + git kapısı -> ölçüm -> çıktılar
        python SIKISMA_YENIDEN.py rapor     SIKISMA_RAPOR.md'yi sikisma_sonuc.json'dan yeniden yazar
        python SIKISMA_YENIDEN.py duyarlilik --asama onkayit|kos|rapor   DUYARLILIK (bilgi; büyük mum ölçeği k x REF x sıkışma uzunluğu p; SY_DUY, kendi ön kaydı)
Colab:  exec(open('SIKISMA_YENIDEN.py').read()); sy_kos()   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_BIST.pkl, V_ABD.pkl, V_AVR.pkl (FON_IZI.fi_k1_veri çıktıları; SY_VERI ile değişir). Satır verisi /tmp/sikisma (repoya girmez).
Çıktı:  arastirma_cikti/sikisma_yeniden/ SIKISMA_ON_KAYIT.md, sikisma_sonuc.json, SIKISMA_RAPOR.md.
Komisyon / kayma YOK (yazılır). Yalnız bugün listede olan hisseler (hayatta kalma yanlılığı; yazılır).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_SY = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
import zlib  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_SY = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_SY not in sys.path:
    sys.path.insert(0, KOK_SY)

sylog = logging.getLogger("col.sikisma")
if not sylog.handlers:
    _sy_h = logging.StreamHandler(sys.stderr)
    _sy_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sikisma: %(message)s", "%H:%M:%S"))
    sylog.addHandler(_sy_h)
    sylog.setLevel(logging.INFO)
    sylog.propagate = False

SY_SURUM = "SIKISMA_YENIDEN v1.0 (2026-11-14): sıkışma -> büyük hareket (A haberci, B zaman, C yönsüz stoplu işlem); bağımsız yeniden ölçüm"
SY_YOL = {"cikti": os.path.join(KOK_SY, "arastirma_cikti", "sikisma_yeniden"), "veri": os.environ.get("SY_VERI", "/tmp/veri"),
          "satir": os.environ.get("SY_SATIR", "/tmp/sikisma"), "kod": os.path.join(KOK_SY, "SIKISMA_YENIDEN.py")}
SY_DOSYA = {"onkayit": "SIKISMA_ON_KAYIT.md", "sonuc": "sikisma_sonuc.json", "rapor": "SIKISMA_RAPOR.md"}
SY_PAZAR = ("BIST", "ABD", "AVR")

# ÖN KAYITTAKİ BÜTÜN SABİTLER. Sonuç görüldükten sonra değiştirilmez: mühür (sy_esik_sha) bozulur, koşu durur.
SY_ESIK: Dict[str, Any] = {
    "kriz": "2026-08-31",                                    # fiyat kesiği (fon krizi)
    "donem": [["2016-22", "2016-01-01", "2022-12-31"], ["2023", "2023-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-08-31"]],
    "kesif": "2016-22", "dogrulama": ["2023", "2024-26"],
    "karar_pazar": ["ABD", "AVR"], "karar_donem": ["2023", "2024-26"], "bilgi_pazar": ["BIST"],
    "gecmis_min": 260,                                       # en az 260 geçerli bar geçmiş (250 gün dağılım + 10 gün pencere)
    "gecerli_bar": "H>L ve V>0",
    "likidite": {"gun": 20, "olcu": "önceki 20 gün medyan C*V (AVR: *Kur, EUR)", "alt_kesik": 0.20, "kova": 3},
    "bolunme": {"esik": 0.25, "geri_gun": 10, "geri_pay": 0.5, "oranlar": [1.5, 2, 3, 4, 5, 6, 8, 10, 15, 20, 25, 30, 40, 50, 100],
                "oran_tol": 0.04, "pencere": [-260, 41],
                "tanim": "ANA: |günlük| > %25, 10 gün sonra sıçramanın en az yarısı duruyor, önceki 10 gün düz (öncekinin yarısından az hareket; geri dönüş bacağı sayılmaz) VE oran bir bölünme oranına (ya da tersine) ±%4 yakın; "
                         "KATI (duyarlılık): oran şartı yok. Şüpheli günü [t-260, t+41] içinde olan hisse-gün olay ve eş havuzundan birlikte çıkar."},
    "S1": {"pencere": 10, "dagilim": 250, "yuzdelik": 0.20, "bant": {"BIST": 0.08, "ABD": 0.06, "AVR": 0.06}, "ara": 20,
           "tanim": "ort(TR/C_önceki, son 10 gün) <= TR/C'nin önceki 250 gündeki (t-259..t-10) %20 yüzdeliği VE (max C - min C)/C_t (son 10 gün) <= bant"},
    "S2": {"bb_gun": 20, "bb_k": 2.0, "dagilim": 250, "yuzdelik": 0.10, "ara": 20,
           "tanim": "Bollinger genişliği 4*std20(C)/ort20(C); son 250 gün içindeki yüzdelik sırası (t dahil) <= %10"},
    "S3": {"gun": 20, "dagilim": 250, "yuzdelik": 0.15, "ara": 20,
           "tanim": "son 20 gün ort |ln getiri|; son 250 gün değerleri içindeki yüzdelik sırası (t dahil) <= %15 (sıra pct; 'altı' = <=)"},
    "dusus": {"gun": 120, "esik": -0.30, "tanim": "C_t / max(C, t-120..t) - 1 <= -%30 (Cemal'in çölü; ayrı alt küme, eşler de aynı şartla)"},
    "B": {"ufuk": 20, "b1_kat": 3.0, "b2_min": 0.15, "b2_kat": 3.0, "b3_kat": 2.0, "b0_kat": 3.0, "atr_gun": 250, "sig_gun": 250,
          "tanim": {"B1": "t+1..t+20 içinde bir günün TR/C_önceki >= 3 x ATR250% (t-249..t ortalama TR/C_önceki; sıkışma dönemi dahil)",
                    "B2": "max_k |ln(C_t+k / C_t)|, k=1..20 >= max(%15, 3 x σ250 x √20)",
                    "B3": "|ln(C_t+20 / C_t)| >= 2 x σ250 x √20",
                    "B0": "t+1..t+20 içinde bir günün TR/C_önceki >= 3 x son 10 gün ort TR/C (göreli; tanımsal, yalnız bilgi)"},
          "atr_birim": "ATR yüzde cinsinden (TR / önceki kapanış): 250 günde fiyat değişince mutlak ATR yanlı olur (K6 birim)"},
    "eslesme": {"A": "aynı gün, aynı pazar, σ250 ondalığı (10) x likidite üçlüsü (3), sıkışma koşulu (S) yanlış olan hisse-günler",
                "C": "aynı gün (t), aynı pazar, 60 gün momentum beşliği x likidite üçlüsü (FI_OLCUT hücresi), S1 koşulu yanlış; aynı işlem kuralı",
                "oyn_kova": 10, "mom_gun": 60, "mom_kova": 5, "min_es": 3},
    "rastgele_gun": {"cekilis": 200, "takvim": "aynı hisse, aynı takvim yılı, uygun (eligible) günler"},
    "bootstrap": {"n": 2000, "kume": "olay ayı (t)", "guven": [0.025, 0.975], "tohum": 1414},
    "zaman": {"pencere": [[1, 5], [6, 10], [11, 15], [16, 20]], "tehlike_ufuk": 5,
              "sure_kova": [[1, 1], [2, 3], [4, 6], [7, 10], [11, 20], [21, 100000]], "kisa": [1, 3], "uzun": [11, 100000],
              "sure_tanim": "S1 koşulunun t'de biten kesintisiz gün sayısı (eşitlik çok olduğu için ondalık yerine sabit kovalar)",
              "model": {"ozellik": ["ln(sure)", "ln(ort10 TR/C / ATR250%)", "ln(ort hacim 10 / ort hacim 50)", "ln(bant10)"],
                        "taban": "eğitimde aynı σ250 ondalığının 5 gün B1 oranı", "egit_son": "2022-12-31", "test_bas": "2023-01-01",
                        "hedef": "B1_5 (t+1..t+5)", "ridge": 1.0e-4, "orneklem": "S1 koşulu doğru, uygun bütün hisse-günler",
                        "skill": "1 - Brier(model) / Brier(taban); ay kümeli bootstrap; alt uç > 0 => 'zaman tahmini var'"}},
    "C": {"bant_gun": 10, "tasma": 0.01, "bekle": 20, "tut": 20, "hedef": 0.20, "ters": 0.10, "slot": 10, "port_n": 200, "port_yuzde": 0.90,
          "n_esik": 30, "gelecek_bar": 41, "maliyet": 0.0,
          "tanim": "t+1..t+20 içinde C > bant_üst*1,01 (uzun) ya da C < bant_alt*0,99 (kısa) ilk kapanış j; giriş Open(j+1); stop öteki kenar "
                   "(gün içi; açılış stopun ötesindeyse açılış); çıkış stop ya da girişten 20. bar kapanışı; kısa getiri = 1 - çıkış/giriş; "
                   "P(+%20 önce) / P(-%10 önce): giriş sonrası 20 barda lehte %20 ile aleyhte %10'dan hangisi önce (aynı gün = aleyhte), stop yok sayılır"},
    "karar": {"n_min": 30, "n_guc": 300,
              "A": "hücre: n<30 ÖLÇÜLEMEDİ; n>=300: alt>1 TUTAR, üst<1 TERS, değilse TUTMADI; 30<=n<300: alt>1 EMARE (güç sınırlı), değilse ÖLÇÜLEMEDİ",
              "C": "hücre: FI_OLCUT dört şart (n>=30, ort eşli fark>0 ve ay kümeli alt95>0, sıra>0,50, slot portföy > 200 rastgele eş portföyün %90'ı); "
                   "tutmazsa n>=300 TUTMADI, n<300 ÖLÇÜLEMEDİ",
              "iz": "İZ = ABD 2023 + ABD 2024-26 + AVR 2023 + AVR 2024-26 dördü TUTAR ve keşif (2016-22) ABD ile AVR aynı yön; BIST bilgi"},
}

SY_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "(A) eş = aynı gün/pazar, σ250 ondalığı x likidite üçlüsü, sıkışma dışı; aynı B tanımı (sy_es_ortalama). Rastgele gün (200 çekiliş, aynı hisse aynı yıl). "
                   "(C) eş aynı t, momentum beşliği x likidite üçlüsü, aynı giriş/stop/çıkış kuralı, 200 rastgele eş portföy. Mekanik üstünlük: ATR250 sıkışmayı içerir, B0 tanımsal (yalnız bilgi)"),
    "K2": ("EVET", "geçmiş özellikler sy_gecmis yalnız t'ye kadar; kos'ta sy_gelecek_denetimi 40 olayda seriyi t'de kesip aynı tespiti mekanik denetler; "
                   "test_sikisma_yeniden.py kesme testi; likidite t-1'e kadar; hücreler t günü kesitinden"),
    "K3": ("EVET", "sy_veri_hazirla: H>L ve V>0 olmayan bar atılır (bayat fiyat); günlük veri, yarım bar yok (kesik 31.08.2026)"),
    "K4": ("EVET", "aynı hissede olay en az 20 bar arayla (iş tanımı; 60 değil, sıkışma olayı için iş tanımında 20); n = olay sayısı; "
                   "tehlike analizinde bütün sıkışık günler kullanılır ve ay kümeli bootstrap ile; ortalama yanında medyan (C) yazılır"),
    "K5": ("EVET", "(C) giriş = kırılım kapanışından sonraki ilk bar açılışı (Open j+1); (A)/(B) getiri değil olasılık, t kapanışı karar anı"),
    "K6": ("EVET", "tek kip: fi_k1_veri düzeltilmiş fiyat; ATR yüzde (TR/C önceki); AVR likidite EUR (Kur); bölünme şüphesi sy_bolunme_supheli ile çıkarılır (ANA + KATI duyarlılık)"),
    "K7": ("EVET", "evren bugünün listesi (V_*.pkl): batanlar yok; raporda yazılı; büyük hareket olasılığı batanlar yokken AŞAĞI yanlı olabilir, işlem getirisi yukarı yanlı"),
    "K8": ("EVET", "3 pazar x 3 dönem (2016-22 keşif, 2023, 2024-26/08); n<30 ÖLÇÜLEMEDİ, n>=300 güç; iki doğrulama dönemi aynı yön şartı; çoklu ölçü (B1 ana; B2/B3/S2/S3 duyarlılık, karar yalnız B1/S1)"),
    "K9": ("EVET", "SY_ESIK sha256 mühür + kod sha256 ön kayıtta; ön kayıt commit+push sonra kos; kos git kapısı (commit'li ve değişmemiş) + kod sha eşitliği; eşik sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV. Ham veriden 3 olay elle doğrulanır (rapor denetim bölümü)"),
    "K11": ("EVET", "iki hücre /tmp/sikisma satır CSV'sinden bağımsız kodla yeniden üretilir; 3 olay ham veriden elle (rapor denetim)"),
    "K12": ("EVET", "'İZ / EMARE' yalnız karar kuralı geçince; büyük hareket olasılığı ile işlem getirisi ayrı tablolarda; komisyon yok yazılır"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_sy; yasak dosyalara dokunulmaz (git diff denetimi); e-posta / anahtar taraması testte; ücretli veri yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; yalnız ölçüm (yön tahmini yok, öneri yok)"),
}


class SYHata(RuntimeError):
    """Durdurucu hata (ön kayıt yok / mühür ya da kod sha tutmuyor / git'e işlenmemiş / veri yok / geleceğe bakma denetimi tutmadı)."""


# ---------------------------------------------------------------- 0) ORTAK
_SY_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _sy_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _sy_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sy_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    s = json.dumps(E or SY_ESIK, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _sy_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or SY_YOL["cikti"], SY_DOSYA.get(ad, ad))


def _sy_git_islenmis(yol: str) -> Dict[str, str]:
    """Dosya git'e işlenmiş ve işlendikten sonra değişmemiş olmalı."""
    kl, ad = os.path.dirname(os.path.abspath(yol)), os.path.basename(yol)
    try:
        r = subprocess.run(["git", "-C", kl, "log", "-1", "--format=%H %cI", "--", ad], capture_output=True, text=True, timeout=60)
        d = subprocess.run(["git", "-C", kl, "status", "--porcelain", "--", ad], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as ex:
        raise SYHata(f"git çalıştırılamadı ({ex}); ön kaydın işlendiği doğrulanamadı")
    if r.returncode != 0 or not r.stdout.strip():
        raise SYHata(f"ön kayıt git'e işlenmemiş ({yol}): önce commit + push")
    if d.returncode != 0 or d.stdout.strip():
        raise SYHata(f"ön kayıt git'e işlendikten sonra değişmiş ({d.stdout.strip() or d.stderr.strip()})")
    h, z = r.stdout.strip().split(" ", 1)
    return {"commit": h, "commit_zamani": z}


def _sy_donem(t: pd.Series, E: Dict[str, Any]) -> np.ndarray:
    out = np.array([""] * len(t), dtype=object)
    for ad, a, b in E["donem"]:
        out[(t >= pd.Timestamp(a)) & (t <= pd.Timestamp(b))] = ad
    return out


# ---------------------------------------------------------------- 1) VERİ
def sy_veri_hazirla(d: pd.DataFrame, E: Dict[str, Any]) -> pd.DataFrame:
    """Geçerli bar (H>L, V>0, sonlu, C>0), fiyat kesiği (kriz), Kur sütunu (yoksa 1)."""
    d = d.copy()
    if "Kur" not in d.columns:
        d["Kur"] = 1.0
    d = d[["Open", "High", "Low", "Close", "Volume", "Kur"]].astype(float)
    d = d[d.index <= pd.Timestamp(E["kriz"])]
    ok = (d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0) & np.isfinite(d[["Open", "High", "Low", "Close"]]).all(axis=1)
    d = d[ok].sort_index()
    d = d[~d.index.duplicated(keep="last")]
    d["Kur"] = d["Kur"].ffill().bfill().fillna(1.0)
    return d


def sy_veri_yukle(pazar: str, E: Optional[Dict[str, Any]] = None, veri: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    E = E or SY_ESIK
    yol = os.path.join(veri or SY_YOL["veri"], f"V_{pazar}.pkl")
    if not os.path.exists(yol):
        raise SYHata(f"veri yok: {yol} (git worktree add /tmp/iv origin/islenmis-veri; python FON_IZI.py vpac /tmp/iv/veri /tmp/veri)")
    V = pd.read_pickle(yol)
    if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
        V = V["veri"]
    out = {}
    for s, d in V.items():
        try:
            x = sy_veri_hazirla(d, E)
            if len(x) >= E["gecmis_min"] + 25:
                out[str(s)] = x
        except Exception as ex:  # tek hisse bozuksa diğerleri sürer
            sylog.warning("%s %s atlandı: %s", pazar, s, ex)
    sylog.info("%s: %d hisse (%s)", pazar, len(out), yol)
    return out


def sy_bolunme_supheli(C: np.ndarray, E: Dict[str, Any], kati: bool = False) -> np.ndarray:
    """Bölünme şüphesi günleri (bool, bar i: C[i-1] -> C[i]). ANA: |getiri| > eşik, geri dönmeyen, oran bir bölünme oranına yakın. KATI: oran şartı yok."""
    B = E["bolunme"]; n = len(C); s = np.zeros(n, bool)
    if n < 2:
        return s
    r = np.r_[np.nan, np.log(C[1:] / C[:-1])]
    aday = np.where(np.abs(np.r_[np.nan, C[1:] / C[:-1] - 1]) > B["esik"])[0]
    for i in aday:
        j = min(n - 1, i + B["geri_gun"])
        kalici = abs(math.log(C[j] / C[i - 1])) >= B["geri_pay"] * abs(r[i])
        once = max(0, i - 1 - B["geri_gun"])
        duz_once = abs(math.log(C[i - 1] / C[once])) < B["geri_pay"] * abs(r[i])   # sıçramanın kendisinin geri dönüşü değil
        if not (kalici and duz_once):
            continue
        if kati:
            s[i] = True; continue
        lr = abs(r[i])
        if any(abs(lr - math.log(k)) < B["oran_tol"] for k in B["oranlar"]):
            s[i] = True
    return s


def _sy_pencere_var(s: np.ndarray, a: int, b: int) -> np.ndarray:
    """out[i] = s[i+a .. i+b] içinde True var mı (a<0<b)."""
    n = len(s); cs = np.r_[0, np.cumsum(s.astype(int))]
    lo = np.clip(np.arange(n) + a, 0, n); hi = np.clip(np.arange(n) + b + 1, 0, n)
    return (cs[hi] - cs[lo]) > 0


def _sy_ileri(x: np.ndarray, h: int) -> np.ndarray:
    """M[i, k-1] = x[i+k], k=1..h; dışı NaN."""
    n = len(x); p = np.r_[x.astype(float), np.full(h, np.nan)]
    return np.lib.stride_tricks.sliding_window_view(p[1:], h)[:n]


def _sy_kosu(b: np.ndarray) -> np.ndarray:
    """Kesintisiz True koşu uzunluğu (i'de biten)."""
    out = np.zeros(len(b), int); c = 0
    for i, v in enumerate(b):
        c = c + 1 if v else 0; out[i] = c
    return out


def _sy_olay(kosul: np.ndarray, ara: int, bas: int) -> np.ndarray:
    """Koşulun doğru olduğu gün olay; aynı hissede yeni olay en az `ara` bar sonra."""
    ev = np.zeros(len(kosul), bool); son = -10 ** 9
    for i in np.where(kosul)[0]:
        if i >= bas and i - son >= ara:
            ev[i] = True; son = i
    return ev


# ---------------------------------------------------------------- 2) GEÇMİŞ ÖZELLİKLER (yalnız t'ye kadar)
def sy_gecmis(d: pd.DataFrame, pazar: str, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Her bar i için yalnız i'ye kadarki barlardan hesaplanan özellikler (geleceğe bakma yok; kesme testi bunu sınar)."""
    E = E or SY_ESIK
    O, H, L, C, V, K = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume", "Kur"))
    n = len(C); Cp = np.r_[np.nan, C[:-1]]
    tr = np.fmax(H, Cp) - np.fmin(L, Cp); tr[0] = H[0] - L[0]
    trc = tr / Cp
    r = np.r_[np.nan, np.log(C[1:] / C[:-1])]
    S1, S2, S3, B = E["S1"], E["S2"], E["S3"], E["B"]
    T = pd.Series(trc); R = pd.Series(r); Cs = pd.Series(C)
    atr = T.rolling(B["atr_gun"], min_periods=B["atr_gun"]).mean().to_numpy()
    sig = R.rolling(B["sig_gun"], min_periods=B["sig_gun"]).std().to_numpy()
    m10 = T.rolling(S1["pencere"], min_periods=S1["pencere"]).mean().to_numpy()
    p20 = T.rolling(S1["dagilim"], min_periods=S1["dagilim"]).quantile(S1["yuzdelik"]).shift(S1["pencere"]).to_numpy()
    band = ((Cs.rolling(S1["pencere"]).max() - Cs.rolling(S1["pencere"]).min()) / Cs).to_numpy()
    hi10 = Cs.rolling(E["C"]["bant_gun"]).max().to_numpy(); lo10 = Cs.rolling(E["C"]["bant_gun"]).min().to_numpy()
    with np.errstate(invalid="ignore"):
        s1c = (m10 <= p20) & (band <= S1["bant"][pazar])
    bbw = (2 * S2["bb_k"] * Cs.rolling(S2["bb_gun"]).std() / Cs.rolling(S2["bb_gun"]).mean())
    bbr = bbw.rolling(S2["dagilim"], min_periods=S2["dagilim"]).rank(pct=True).to_numpy()
    a20 = R.abs().rolling(S3["gun"], min_periods=S3["gun"]).mean()
    a20r = a20.rolling(S3["dagilim"], min_periods=S3["dagilim"]).rank(pct=True).to_numpy()
    with np.errstate(invalid="ignore"):
        s2c = bbr <= S2["yuzdelik"]
        s3c = a20r <= S3["yuzdelik"]
    gm = E["gecmis_min"]; ok_g = np.arange(n) >= gm
    s1c &= ok_g; s2c &= ok_g; s3c &= ok_g
    D = E["dusus"]
    tepe = Cs.rolling(D["gun"] + 1, min_periods=D["gun"] + 1).max().to_numpy()
    dusus = C / tepe - 1
    Lq = pd.Series(C * V * K).rolling(E["likidite"]["gun"], min_periods=E["likidite"]["gun"]).median().shift(1).to_numpy()
    mg = E["eslesme"]["mom_gun"]
    mom = np.r_[np.full(mg, np.nan), C[mg:] / C[:-mg] - 1]
    Vs = pd.Series(V)
    vk = (Vs.rolling(10).mean() / Vs.rolling(50).mean()).to_numpy()
    return pd.DataFrame({"i": np.arange(n), "trc": trc, "atr": atr, "sig": sig, "m10": m10, "p20": p20, "band": band, "hi10": hi10, "lo10": lo10,
                         "s1c": s1c, "s2c": s2c, "s3c": s3c, "run": _sy_kosu(s1c), "dusus": dusus, "liq": Lq, "mom": mom, "vk": vk,
                         "ev1": _sy_olay(s1c, S1["ara"], gm), "ev2": _sy_olay(s2c, S2["ara"], gm), "ev3": _sy_olay(s3c, S3["ara"], gm)},
                        index=d.index)


# ---------------------------------------------------------------- 3) SONUÇLAR (t'den sonrası; yalnız kos'ta)
def sy_sonuc(d: pd.DataFrame, G: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """B0-B3, ilk büyük gün, 5 gün B1 ve (C) işlem sonucu. G = sy_gecmis(d)."""
    E = E or SY_ESIK
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    n = len(C); B = E["B"]; h = B["ufuk"]
    trc = G.trc.to_numpy(); atr = G.atr.to_numpy(); sig = G.sig.to_numpy(); m10 = G.m10.to_numpy()
    Tf = _sy_ileri(trc, h)
    gel = np.arange(n) + h <= n - 1
    with np.errstate(invalid="ignore"):
        buyuk = Tf >= B["b1_kat"] * atr[:, None]
        b1 = buyuk.any(axis=1)
        k1 = np.where(b1, buyuk.argmax(axis=1) + 1, 0)
        b15 = buyuk[:, :E["zaman"]["tehlike_ufuk"]].any(axis=1)
        b0 = (Tf >= B["b0_kat"] * m10[:, None]).any(axis=1)
        lc = np.log(C); Lf = _sy_ileri(lc, h) - lc[:, None]
        sk = sig * math.sqrt(h)
        b2 = np.nanmax(np.abs(Lf), axis=1) >= np.fmax(B["b2_min"], B["b2_kat"] * sk)
        b3 = np.abs(Lf[:, -1]) >= B["b3_kat"] * sk
    out = pd.DataFrame({"gel": gel, "B1": b1 & gel, "k1": np.where(gel, k1, 0), "B1_5": b15 & gel, "B0": b0 & gel, "B2": b2 & gel, "B3": b3 & gel},
                       index=d.index)
    out = pd.concat([out, sy_islem(d, G, E)], axis=1)
    return out


def sy_islem(d: pd.DataFrame, G: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """(C) her bar t için yönsüz kırılım işlemi (vektörel). c_ok: t+41 bar var. yon 0 = 20 günde kırılım yok."""
    E = E or SY_ESIK
    P = E["C"]; O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    n = len(C); hi = G.hi10.to_numpy(); lo = G.lo10.to_numpy(); w = P["bekle"]; tut = P["tut"]
    c_ok = np.arange(n) + P["gelecek_bar"] <= n - 1
    Cf = _sy_ileri(C, w)
    with np.errstate(invalid="ignore"):
        yuk = Cf > hi[:, None] * (1 + P["tasma"]); asg = Cf < lo[:, None] * (1 - P["tasma"])
    olay = yuk | asg
    var = olay.any(axis=1) & c_ok & np.isfinite(hi) & np.isfinite(lo)
    j = np.where(var, olay.argmax(axis=1) + 1, 0)
    yon = np.zeros(n, int)
    ii = np.where(var)[0]
    yon[ii] = np.where(yuk[ii, j[ii] - 1], 1, -1)
    getiri = np.full(n, np.nan); cikis_bar = np.full(n, -1); ilk20 = np.full(n, np.nan); ilk10 = np.full(n, np.nan); giris_bar = np.full(n, -1)
    if len(ii):
        e = ii + j[ii] + 1
        idx = e[:, None] + np.arange(tut)[None, :]
        Ow, Hw, Lw, Cw = O[idx], H[idx], L[idx], C[idx]
        gir = Ow[:, 0]; y = yon[ii]
        stop = np.where(y == 1, lo[ii], hi[ii])
        vur = np.where(y[:, None] == 1, Lw <= stop[:, None], Hw >= stop[:, None])
        vk = vur.any(axis=1); kk = vur.argmax(axis=1)
        acil = Ow[np.arange(len(ii)), kk]
        cik_stop = np.where(y == 1, np.fmin(acil, stop), np.fmax(acil, stop))
        cik = np.where(vk, cik_stop, Cw[:, -1])
        g = np.where(y == 1, cik / gir - 1, 1 - cik / gir)
        getiri[ii] = g; giris_bar[ii] = e; cikis_bar[ii] = np.where(vk, e + kk, e + tut - 1)
        leh = np.where(y[:, None] == 1, Hw >= gir[:, None] * (1 + P["hedef"]), Lw <= gir[:, None] * (1 - P["hedef"]))
        ale = np.where(y[:, None] == 1, Lw <= gir[:, None] * (1 - P["ters"]), Hw >= gir[:, None] * (1 + P["ters"]))
        BIG = 10 ** 6
        fl = np.where(leh.any(axis=1), leh.argmax(axis=1), BIG); fa = np.where(ale.any(axis=1), ale.argmax(axis=1), BIG)
        ilk20[ii] = ((fl < fa) & (fl < BIG)).astype(float)
        ilk10[ii] = ((fa <= fl) & (fa < BIG)).astype(float)
    tar = d.index.to_numpy()
    gt = np.full(n, np.datetime64("NaT"), dtype="datetime64[ns]"); ct = gt.copy()
    m = giris_bar >= 0
    gt[m] = tar[giris_bar[m]]; ct[m] = tar[cikis_bar[m]]
    return pd.DataFrame({"c_ok": c_ok, "c_yon": yon, "c_r": getiri, "c_giris": gt, "c_cikis": ct, "c_ilk20": ilk20, "c_ilk10": ilk10}, index=d.index)


# ---------------------------------------------------------------- 4) PANEL (pazar başına uzun tablo + uygunluk + hücreler)
_SY_GECMIS_KOL = ["atr", "sig", "m10", "p20", "band", "s1c", "s2c", "s3c", "run", "dusus", "liq", "mom", "vk", "ev1", "ev2", "ev3"]


def sy_panel(V: Dict[str, pd.DataFrame], pazar: str, E: Optional[Dict[str, Any]] = None, sonuc: bool = True) -> pd.DataFrame:
    """Bütün hisse-günler: geçmiş özellikler, (sonuc=True ise) sonuçlar, uygunluk (uygun / uygun_c), dönem, hücreler."""
    E = E or SY_ESIK
    parca = []
    for s, d in V.items():
        try:
            G = sy_gecmis(d, pazar, E)
            C = d.Close.to_numpy(float)
            sup = sy_bolunme_supheli(C, E); supk = sy_bolunme_supheli(C, E, kati=True)
            a, b = E["bolunme"]["pencere"]
            X = G[_SY_GECMIS_KOL].copy()
            X["sup"] = _sy_pencere_var(sup, a, b); X["supk"] = _sy_pencere_var(supk, a, b)
            X["gel"] = np.arange(len(d)) + E["B"]["ufuk"] <= len(d) - 1
            X["c_ok"] = np.arange(len(d)) + E["C"]["gelecek_bar"] <= len(d) - 1
            if sonuc:
                S = sy_sonuc(d, G, E)
                for c in S.columns:
                    if c not in ("gel", "c_ok"):
                        X[c] = S[c].to_numpy()
            X["sembol"] = s; X["tarih"] = d.index
            X = X[(G.i.to_numpy() >= E["gecmis_min"])]
            parca.append(X)
        except Exception as ex:
            sylog.warning("%s %s panel dışı: %s", pazar, s, ex)
    P = pd.concat(parca, ignore_index=True)
    P["pazar"] = pazar
    P["donem"] = _sy_donem(P.tarih, E)
    # likidite alt %20: o gün, o pazarda likiditesi sonlu bütün hisseler arasında
    P["liq_pct"] = P.groupby("tarih").liq.rank(pct=True)
    temel = (P.donem != "") & np.isfinite(P.atr) & np.isfinite(P.sig) & np.isfinite(P.p20) & np.isfinite(P.m10) & np.isfinite(P.liq) \
        & (P.liq_pct > E["likidite"]["alt_kesik"]) & P.gel & ~P.sup & (P.sig > 0) & (P.atr > 0)
    P["uygun"] = temel
    P["uygun_c"] = temel & P.c_ok & np.isfinite(P.mom)
    # hücreler (uygunlar arasında, gün kesiti)
    P["oyn"] = -1; P["lq3"] = -1; P["mom5"] = -1
    u = P.uygun
    g = P[u].groupby("tarih")
    P.loc[u, "oyn"] = (np.ceil(g.sig.rank(pct=True, method="first") * E["eslesme"]["oyn_kova"]) - 1).astype(int)
    P.loc[u, "lq3"] = (np.ceil(g.liq.rank(pct=True, method="first") * E["likidite"]["kova"]) - 1).astype(int)
    uc = P.uygun_c
    P.loc[uc, "mom5"] = (np.ceil(P[uc].groupby("tarih").mom.rank(pct=True, method="first") * E["eslesme"]["mom_kova"]) - 1).astype(int)
    P["hucA"] = P.oyn * 10 + P.lq3
    P["hucC"] = P.mom5 * 10 + P.lq3
    P["dsert"] = P.dusus <= E["dusus"]["esik"]
    for c in ("s1c", "s2c", "s3c", "ev1", "ev2", "ev3", "sup", "supk", "gel", "c_ok"):
        P[c] = P[c].astype(bool)
    return P


def sy_sayim(P: pd.DataFrame) -> Dict[str, Any]:
    """Olay SAYIMI (sonuç / getiri kullanmaz)."""
    out = {}
    for ev in ("ev1", "ev2", "ev3"):
        x = P[P.uygun & P[ev]]
        out[ev] = {d: int((x.donem == d).sum()) for d in ("2016-22", "2023", "2024-26")}
        xs = x[x.dsert]
        out[ev + "_sert"] = {d: int((xs.donem == d).sum()) for d in ("2016-22", "2023", "2024-26")}
    x = P[P.uygun_c & P.ev1]
    out["ev1_c_uygun"] = {d: int((x.donem == d).sum()) for d in ("2016-22", "2023", "2024-26")}
    out["hisse"] = int(P.sembol.nunique()); out["uygun_gun"] = int(P.uygun.sum())
    out["bolunme_supheli_gun_disi"] = int(P.sup.sum()); out["bolunme_kati_gun"] = int(P.supk.sum())
    return out


# ---------------------------------------------------------------- 5) EŞLEME ve İSTATİSTİK
def sy_es_ortalama(P: pd.DataFrame, olay: pd.Series, es_maske: pd.Series, huc: str, degerler: List[str]) -> pd.DataFrame:
    """Olay satırları için aynı gün, aynı hücre eş ortalaması (eş = es_maske; olay satırı eş değil). Döner: olay satırları + es_<deger> + es_n."""
    E_ = P.loc[es_maske, ["tarih", huc] + degerler].copy()
    for c in degerler:
        E_[c] = E_[c].astype(float)
    g = E_.groupby(["tarih", huc])[degerler].agg(["sum", "count"])
    g.columns = [f"{a}_{b}" for a, b in g.columns]
    X = P.loc[olay].copy()
    X = X.merge(g, left_on=["tarih", huc], right_index=True, how="left")
    for c in degerler:
        X["es_" + c] = X[f"{c}_sum"] / X[f"{c}_count"]
    X["es_n"] = X[f"{degerler[0]}_count"].fillna(0).astype(int)
    return X.drop(columns=[f"{c}_{b}" for c in degerler for b in ("sum", "count")])


def sy_oran_boot(pay: np.ndarray, payda: np.ndarray, ay: np.ndarray, E: Dict[str, Any], tohum_ek: int = 0) -> Tuple[float, float, float]:
    """KAT = sum(pay)/sum(payda); ay kümeli bootstrap %95."""
    if len(pay) == 0 or payda.sum() <= 0:
        return (np.nan, np.nan, np.nan)
    aylar, inv = np.unique(ay, return_inverse=True)
    sp = np.bincount(inv, weights=pay, minlength=len(aylar)); sq = np.bincount(inv, weights=payda, minlength=len(aylar))
    rng = np.random.default_rng(E["bootstrap"]["tohum"] + tohum_ek)
    W = rng.multinomial(len(aylar), np.full(len(aylar), 1 / len(aylar)), size=E["bootstrap"]["n"])
    with np.errstate(invalid="ignore", divide="ignore"):
        k = (W @ sp) / (W @ sq)
    a, b = E["bootstrap"]["guven"]
    return (float(pay.sum() / payda.sum()), float(np.nanquantile(k, a)), float(np.nanquantile(k, b)))


def sy_ort_boot(x: np.ndarray, ay: np.ndarray, E: Dict[str, Any], tohum_ek: int = 0) -> Tuple[float, float, float]:
    return sy_oran_boot(x, np.ones(len(x)), ay, E, tohum_ek)


def sy_karar_A(n: int, alt: float, ust: float, E: Dict[str, Any]) -> str:
    K = E["karar"]
    if n < K["n_min"] or not np.isfinite(alt):
        return "ÖLÇÜLEMEDİ"
    if n >= K["n_guc"]:
        if alt > 1:
            return "TUTAR"
        if ust < 1:
            return "TERS"
        return "TUTMADI"
    return "EMARE (güç sınırlı)" if alt > 1 else "ÖLÇÜLEMEDİ (güç sınırlı)"


def sy_rastgele_gun(P: pd.DataFrame, X: pd.DataFrame, deger: str, E: Dict[str, Any], tohum_ek: int = 0) -> Dict[str, float]:
    """(K-b) aynı hisse, aynı takvim yılı, uygun günlerden rastgele; 200 çekiliş. Döner: rastgele ortalama oran, olay oranı yüzdeliği."""
    if not len(X):
        return {"rast_p": np.nan, "rast_p05": np.nan, "rast_p95": np.nan, "olay_yuzdelik": np.nan}
    U = P.loc[P.uygun, ["sembol", "tarih", deger]].copy()
    U["yil"] = U.tarih.dt.year
    U = U.sort_values(["sembol", "yil"]).reset_index(drop=True)
    anahtar = U.sembol + "|" + U.yil.astype(str)
    ilk = anahtar.ne(anahtar.shift()).to_numpy()
    bas = np.where(ilk)[0]; say = np.diff(np.r_[bas, len(U)])
    harita = dict(zip(anahtar.to_numpy()[bas], range(len(bas))))
    xk = (X.sembol + "|" + X.tarih.dt.year.astype(str)).map(harita)
    m = xk.notna().to_numpy(); gi = xk[m].astype(int).to_numpy()
    rng = np.random.default_rng(E["bootstrap"]["tohum"] + 7 + tohum_ek)
    u = rng.random((E["rastgele_gun"]["cekilis"], len(gi)))
    sec = bas[gi][None, :] + np.floor(u * say[gi][None, :]).astype(int)
    v = U[deger].astype(float).to_numpy()[sec].mean(axis=1)
    olay = X.loc[m, deger].astype(float).mean()
    return {"rast_p": float(v.mean()), "rast_p05": float(np.quantile(v, 0.05)), "rast_p95": float(np.quantile(v, 0.95)),
            "olay_yuzdelik": float((v < olay).mean())}


# ---------------------------------------------------------------- 6) (A) HABERCİ
def sy_olc_A(P: pd.DataFrame, E: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Tablo: pazar x dönem x sıkışma tanımı (S1/S2/S3, S1 sert düşüş, S1 katı bölünme) x B ölçüsü. İkinci dönüş: S1 olay satırları (eşli)."""
    pazar = P.pazar.iat[0]; sat = []; olaylar = None
    Bs = ["B1", "B2", "B3", "B0", "B1_5"]
    tanim = [("S1", "ev1", "s1c", None), ("S2", "ev2", "s2c", None), ("S3", "ev3", "s3c", None), ("S1_sert", "ev1", "s1c", "dsert"),
             ("S1_kati", "ev1", "s1c", "kati")]
    for ad, ev, kos, alt in tanim:
        u = P.uygun.copy()
        if alt == "kati":
            u &= ~P.supk
        olay = u & P[ev]; es = u & ~P[kos]
        if alt == "dsert":
            olay &= P.dsert; es &= P.dsert
        X = sy_es_ortalama(P, olay, es, "hucA", Bs + ["f1", "f2", "f3", "f4"] if "f1" in P else Bs)
        X = X[X.es_n >= E["eslesme"]["min_es"]]
        if ad == "S1":
            olaylar = X
        for dn in [d[0] for d in E["donem"]] + ["2023+"]:
            Y = X[(X.donem == dn)] if dn != "2023+" else X[X.donem.isin(["2023", "2024-26"])]
            ay = Y.tarih.dt.to_period("M").astype(str).to_numpy()
            for b in Bs:
                kat, alt95, ust95 = sy_oran_boot(Y[b].astype(float).to_numpy(), Y["es_" + b].to_numpy(), ay, E, zlib.crc32(f'{ad}|{dn}|{b}'.encode()) % 1000)
                r = {"pazar": pazar, "donem": dn, "sikisma": ad, "olcu": b, "n": int(len(Y)), "p_olay": float(Y[b].mean()) if len(Y) else np.nan,
                     "p_es": float(Y["es_" + b].mean()) if len(Y) else np.nan, "kat": kat, "alt95": alt95, "ust95": ust95,
                     "es_n_medyan": float(Y.es_n.median()) if len(Y) else np.nan}
                if ad == "S1" and b in ("B1", "B2", "B3"):
                    r.update(sy_rastgele_gun(P[P.donem == dn] if dn != "2023+" else P[P.donem.isin(["2023", "2024-26"])], Y, b, E))
                r["karar"] = sy_karar_A(r["n"], alt95, ust95, E)
                sat.append(r)
    # taban (bilgi): uygun bütün hisse-günlerde B1 oranı
    for dn in [d[0] for d in E["donem"]]:
        U = P[P.uygun & (P.donem == dn)]
        sat.append({"pazar": pazar, "donem": dn, "sikisma": "TABAN_tum_gunler", "olcu": "B1", "n": int(len(U)), "p_olay": float(U.B1.mean()) if len(U) else np.nan})
    return pd.DataFrame(sat), olaylar


# ---------------------------------------------------------------- 7) (B) ZAMAN
def _sy_lojistik(X: np.ndarray, y: np.ndarray, ridge: float, tur: int = 50) -> np.ndarray:
    """IRLS lojistik (sabit terim X'te). Döner: katsayı."""
    w = np.zeros(X.shape[1])
    for _ in range(tur):
        z = np.clip(X @ w, -30, 30); p = 1 / (1 + np.exp(-z))
        W = p * (1 - p)
        Hs = X.T @ (X * W[:, None]) + ridge * np.eye(X.shape[1]); g = X.T @ (y - p) - ridge * w
        adim = np.linalg.solve(Hs, g); w = w + adim
        if np.max(np.abs(adim)) < 1e-8:
            break
    return w


def sy_olc_B(P: pd.DataFrame, X1: pd.DataFrame, E: Dict[str, Any]) -> Dict[str, Any]:
    """Zaman: ilk büyük gün dağılımı (olay vs eş), pencere eşli oranları, süre kovalarına göre 5 gün tehlikesi (eşli), lojistik walk-forward."""
    pazar = P.pazar.iat[0]; Z = E["zaman"]; out: Dict[str, Any] = {"pazar": pazar}
    # 1) ilk büyük gün dağılımı (S1 olayları, B1 gerçekleşen)
    dag = []
    for dn in [d[0] for d in E["donem"]] + ["2023+"]:
        Y = X1[X1.donem == dn] if dn != "2023+" else X1[X1.donem.isin(["2023", "2024-26"])]
        k = Y.loc[Y.B1, "k1"].to_numpy()
        r = {"donem": dn, "n_olay": int(len(Y)), "n_b1": int(len(k))}
        if len(k):
            r.update({"medyan": float(np.median(k)), "c25": float(np.quantile(k, 0.25)), "c75": float(np.quantile(k, 0.75)),
                      "hist": [int((k == i).sum()) for i in range(1, E["B"]["ufuk"] + 1)]})
        ay = Y.tarih.dt.to_period("M").astype(str).to_numpy()
        for wi, (a, b) in enumerate(Z["pencere"], 1):
            kat, lo, hi = sy_oran_boot(Y[f"f{wi}"].astype(float).to_numpy(), Y[f"es_f{wi}"].to_numpy(), ay, E, 300 + wi)
            r[f"p_{a}_{b}"] = float(Y[f"f{wi}"].mean()) if len(Y) else np.nan
            r[f"es_{a}_{b}"] = float(Y[f"es_f{wi}"].mean()) if len(Y) else np.nan
            r[f"kat_{a}_{b}"] = kat; r[f"alt_{a}_{b}"] = lo; r[f"ust_{a}_{b}"] = hi
        # eşlerde ilk büyük gün dağılımı (B1 gerçekleşen eşler; olay günleri ile aynı gün-hücre)
        dag.append(r)
    out["dagilim"] = dag
    # 2) süre kovalarına göre 5 gün tehlikesi (bütün S1-koşullu uygun günler; eşli)
    sq = P.uygun & P.s1c; es = P.uygun & ~P.s1c
    S = sy_es_ortalama(P, sq, es, "hucA", ["B1_5"])
    S = S[S.es_n >= E["eslesme"]["min_es"]]
    teh = []
    for dn in [d[0] for d in E["donem"]] + ["2023+"]:
        Y = S[S.donem == dn] if dn != "2023+" else S[S.donem.isin(["2023", "2024-26"])]
        ay = Y.tarih.dt.to_period("M").astype(str).to_numpy()
        for a, b in Z["sure_kova"]:
            m = (Y.run >= a) & (Y.run <= b)
            kat, lo, hi = sy_oran_boot(Y.loc[m, "B1_5"].astype(float).to_numpy(), Y.loc[m, "es_B1_5"].to_numpy(), ay[m.to_numpy()], E, 400 + a)
            teh.append({"donem": dn, "sure": f"{a}-{b if b < 1000 else '+'}", "n_gun": int(m.sum()), "p5": float(Y.loc[m, "B1_5"].mean()) if m.any() else np.nan,
                        "es_p5": float(Y.loc[m, "es_B1_5"].mean()) if m.any() else np.nan, "kat": kat, "alt95": lo, "ust95": hi})
        # uzun / kısa kat oranı (ay kümeli bootstrap birlikte)
        ku = (Y.run >= Z["kisa"][0]) & (Y.run <= Z["kisa"][1]); uz = (Y.run >= Z["uzun"][0]) & (Y.run <= Z["uzun"][1])
        if ku.any() and uz.any():
            aylar, inv = np.unique(ay, return_inverse=True)
            def sm(mm, c):
                return np.bincount(inv[mm.to_numpy()], weights=Y.loc[mm, c].astype(float).to_numpy(), minlength=len(aylar))
            a1, b1_, a2, b2_ = sm(uz, "B1_5"), sm(uz, "es_B1_5"), sm(ku, "B1_5"), sm(ku, "es_B1_5")
            rng = np.random.default_rng(E["bootstrap"]["tohum"] + 500)
            W = rng.multinomial(len(aylar), np.full(len(aylar), 1 / len(aylar)), size=E["bootstrap"]["n"])
            with np.errstate(all="ignore"):
                rr = ((W @ a1) / (W @ b1_)) / ((W @ a2) / (W @ b2_))
            teh.append({"donem": dn, "sure": "UZUN/KISA", "n_gun": int(uz.sum() + ku.sum()), "kat": float((a1.sum() / b1_.sum()) / (a2.sum() / b2_.sum())),
                        "alt95": float(np.nanquantile(rr, 0.025)), "ust95": float(np.nanquantile(rr, 0.975))})
    out["tehlike"] = teh
    # 3) lojistik walk-forward (S1 koşullu uygun günler; hedef B1_5)
    M = Z["model"]
    D = P[sq].copy()
    with np.errstate(all="ignore"):
        F = np.column_stack([np.log(D.run.clip(lower=1)), np.log(D.m10 / D.atr), np.log(D.vk), np.log(D.band.clip(lower=1e-4))])
    ok = np.isfinite(F).all(axis=1)
    D = D[ok]; F = F[ok]
    tr_son = pd.Timestamp(M["egit_son"]) - pd.Timedelta(days=10)    # hedef penceresi (5 bar) eğitim sonunu aşmasın
    egit = (D.tarih <= tr_son).to_numpy(); test = (D.tarih >= pd.Timestamp(M["test_bas"])).to_numpy()
    model = []
    if egit.sum() >= 200 and test.sum() >= 30:
        mu = F[egit].mean(0); sd = F[egit].std(0) + 1e-12
        Fz = (F - mu) / sd
        y = D.B1_5.astype(float).to_numpy()
        tab_oran = pd.Series(y[egit]).groupby(D.oyn.to_numpy()[egit]).mean()
        oyn_d = np.eye(10)[D.oyn.clip(0, 9).to_numpy()][:, 1:]
        Xm = np.column_stack([np.ones(len(D)), Fz, oyn_d])
        w = _sy_lojistik(Xm[egit], y[egit], M["ridge"])
        pm = 1 / (1 + np.exp(-np.clip(Xm @ w, -30, 30)))
        pb = D.oyn.map(tab_oran).fillna(y[egit].mean()).to_numpy()
        for dn in ("2023", "2024-26", "2023+"):
            m = test & ((D.donem == dn).to_numpy() if dn != "2023+" else D.donem.isin(["2023", "2024-26"]).to_numpy())
            if m.sum() < 30:
                model.append({"donem": dn, "n": int(m.sum())}); continue
            em = (pm[m] - y[m]) ** 2; eb = (pb[m] - y[m]) ** 2
            ay = D.tarih[m].dt.to_period("M").astype(str).to_numpy()
            aylar, inv = np.unique(ay, return_inverse=True)
            sm_ = np.bincount(inv, weights=em, minlength=len(aylar)); sb_ = np.bincount(inv, weights=eb, minlength=len(aylar))
            rng = np.random.default_rng(E["bootstrap"]["tohum"] + 600)
            W = rng.multinomial(len(aylar), np.full(len(aylar), 1 / len(aylar)), size=E["bootstrap"]["n"])
            sk = 1 - (W @ sm_) / (W @ sb_)
            # tepe ondalık: modelin en yüksek %10'unda gerçekleşen oran / taban
            q = np.quantile(pm[m], 0.9); tepe = pm[m] >= q
            model.append({"donem": dn, "n": int(m.sum()), "y_ort": float(y[m].mean()), "brier_model": float(em.mean()), "brier_taban": float(eb.mean()),
                          "skill": float(1 - em.mean() / eb.mean()), "alt95": float(np.quantile(sk, 0.025)), "ust95": float(np.quantile(sk, 0.975)),
                          "tepe10_oran": float(y[m][tepe].mean()), "tepe10_taban": float(pb[m][tepe].mean())})
        out["model_katsayi"] = {"ad": ["sabit"] + M["ozellik"] + [f"oyn{i}" for i in range(1, 10)], "w": [float(v) for v in w],
                                "egit_n": int(egit.sum()), "egit_y": float(y[egit].mean())}
    out["model"] = model
    return out


# ---------------------------------------------------------------- 8) (C) YÖNSÜZ İŞLEM
def _sy_slot_atama(giris: np.ndarray, cikis: np.ndarray, slot: int) -> np.ndarray:
    """Sırayla 10 yuva; yuva çıkış gününden sonra boşalır. Döner: yuva no (alınmayan -1). Atama getiriden bağımsız."""
    bos = np.full(slot, np.datetime64("1900-01-01", "ns")); out = np.full(len(giris), -1)
    for i, (g, c) in enumerate(zip(giris, cikis)):
        k = int(np.argmin(bos))
        if bos[k] < g:
            out[i] = k; bos[k] = c
    return out


def _sy_slot_deger(R: np.ndarray, yuva: np.ndarray, slot: int) -> np.ndarray:
    """R: (çekiliş x olay). Her yuva 1/slot ile başlar, getirileri bileşik. Döner: toplam getiri (çekiliş başına)."""
    R = np.atleast_2d(R); top = np.zeros(R.shape[0])
    for k in range(slot):
        m = yuva == k
        top += np.prod(1 + R[:, m], axis=1) / slot if m.any() else 1.0 / slot
    return top - 1


def sy_olc_C(P: pd.DataFrame, E: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """S1 olayları (uygun_c) + aynı t, aynı momentum x likidite hücresi, S1 dışı eşler (aynı kural). FI_OLCUT dört şart."""
    pazar = P.pazar.iat[0]; Pc = E["C"]
    olay = P.uygun_c & P.ev1; es = P.uygun_c & ~P.s1c & (P.c_yon != 0)
    X = P.loc[olay].copy()
    Es = P.loc[es, ["tarih", "hucC", "c_r"]].sort_values(["tarih", "hucC"]).reset_index(drop=True)
    anahtar = Es.tarih.astype("int64").astype(str) + "|" + Es.hucC.astype(str)
    ilk = anahtar.ne(anahtar.shift()).to_numpy(); bas = np.where(ilk)[0]; say = np.diff(np.r_[bas, len(Es)])
    harita = dict(zip(anahtar.to_numpy()[bas], range(len(bas))))
    X["_g"] = (X.tarih.astype("int64").astype(str) + "|" + X.hucC.astype(str)).map(harita)
    er = Es.c_r.to_numpy()
    es_ort, sira, es_n = [], [], []
    for r_, g_ in zip(X.c_r.to_numpy(), X._g.to_numpy()):
        if g_ is None or (isinstance(g_, float) and not np.isfinite(g_)):
            es_ort.append(np.nan); sira.append(np.nan); es_n.append(0); continue
        g_ = int(g_); e = er[bas[g_]:bas[g_] + say[g_]]
        es_n.append(len(e)); es_ort.append(float(e.mean()))
        sira.append(float(((e < r_).sum() + 0.5 * (e == r_).sum()) / len(e)) if np.isfinite(r_) else np.nan)
    X["es_r"] = es_ort; X["sira"] = sira; X["es_n"] = es_n
    X["islem"] = X.c_yon != 0
    sat = []
    for dn in [d[0] for d in E["donem"]] + ["2023+"]:
        Y0 = X[X.donem == dn] if dn != "2023+" else X[X.donem.isin(["2023", "2024-26"])]
        Y = Y0[Y0.islem & (Y0.es_n >= E["eslesme"]["min_es"])].sort_values("c_giris")
        r = {"pazar": pazar, "donem": dn, "n_olay": int(len(Y0)), "islem_orani": float(Y0.islem.mean()) if len(Y0) else np.nan, "n": int(len(Y))}
        if len(Y) >= 1:
            f = (Y.c_r - Y.es_r).to_numpy(); ay = Y.tarih.dt.to_period("M").astype(str).to_numpy()
            ort, lo, hi = sy_ort_boot(f, ay, E, 700)
            yuva = _sy_slot_atama(Y.c_giris.to_numpy(), Y.c_cikis.to_numpy(), Pc["slot"])
            port = float(_sy_slot_deger(Y.c_r.to_numpy()[None, :], yuva, Pc["slot"])[0])
            rng = np.random.default_rng(E["bootstrap"]["tohum"] + 800)
            Rr = np.empty((Pc["port_n"], len(Y)))
            for i, g_ in enumerate(Y._g.astype(int).to_numpy()):
                Rr[:, i] = er[bas[g_] + rng.integers(0, say[g_], Pc["port_n"])]
            rast = _sy_slot_deger(Rr, yuva, Pc["slot"])
            r.update({"ort_r": float(Y.c_r.mean()), "medyan_r": float(Y.c_r.median()), "ort_es_r": float(Y.es_r.mean()), "ort_fark": ort,
                      "alt95": lo, "ust95": hi, "medyan_fark": float(np.median(f)), "sira": float(Y.sira.mean()), "kazanan": float((Y.c_r > 0).mean()),
                      "uzun_pay": float((Y.c_yon == 1).mean()), "p_ilk20": float(Y.c_ilk20.mean()), "p_ilk10": float(Y.c_ilk10.mean()),
                      "portfoy": port, "port_es_p50": float(np.quantile(rast, 0.5)), "port_es_p90": float(np.quantile(rast, Pc["port_yuzde"])),
                      "slot_islem": int((yuva >= 0).sum())})
            # eşlerin kendi P(+20 önce) / P(-10 önce) (aynı gün-hücre ortalaması; bilgi)
            tut = bool(len(Y) >= Pc["n_esik"] and lo > 0 and r["sira"] > 0.5 and port > r["port_es_p90"])
            r["tutar"] = tut
            r["karar"] = ("TUTAR" if tut else ("TUTMADI" if len(Y) >= E["karar"]["n_guc"] else "ÖLÇÜLEMEDİ")) if len(Y) >= E["karar"]["n_min"] else "ÖLÇÜLEMEDİ"
        else:
            r["karar"] = "ÖLÇÜLEMEDİ"
        sat.append(r)
    # eş havuzunun P(+20 önce)/P(-10 önce) (olay günleri-hücreleri ağırlıklı)
    Xe = sy_es_ortalama(P, olay & (P.c_yon != 0), es, "hucC", ["c_ilk20", "c_ilk10"])
    for r in sat:
        dn = r["donem"]
        Y = Xe[Xe.donem == dn] if dn != "2023+" else Xe[Xe.donem.isin(["2023", "2024-26"])]
        r["es_p_ilk20"] = float(Y.es_c_ilk20.mean()) if len(Y) else np.nan
        r["es_p_ilk10"] = float(Y.es_c_ilk10.mean()) if len(Y) else np.nan
    return pd.DataFrame(sat), X.drop(columns=["_g"])


# ---------------------------------------------------------------- 9) ÖN KAYIT
_SY_OC_DESEN = {"muhur": r"MÜHÜR \(SY_ESIK sha256\): `([0-9a-f]{64})`", "kod": r"KOD \(SIKISMA_YENIDEN\.py sha256\): `([0-9a-f]{64})`",
                "zaman": r"ZAMAN \(UTC\): `([^`]+)`"}


def sy_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = SY_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def sy_onkayit_metni(sayim: Dict[str, Dict[str, Any]], veri_sha: Dict[str, str], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or SY_ESIK
    s = [f"# SIKISMA_YENIDEN — ÖN KAYIT\n", f"{SY_SURUM}\n",
         f"- MÜHÜR (SY_ESIK sha256): `{sy_esik_sha(E)}`",
         f"- KOD (SIKISMA_YENIDEN.py sha256): `{_sy_sha_dosya(SY_YOL['kod'])}`",
         f"- ZAMAN (UTC): `{_sy_simdi()}`",
         "- Bu dosya ölçümden ÖNCE yazılır ve commit + push edilir; `kos` bu dosya git'te işlenmiş ve değişmemiş değilse, mühür ya da kod sha farklıysa durur.",
         "- Bağımsızlık: eski VDYT / VDYT2 rapor ve sonuçları okunmadı; tanımlar yalnız iş tanımından.", "",
         "## Soru", "Sıkışmadan sonra büyük hareket geliyor mu (hissenin OLAĞAN ölçüsüyle, göreli değil), ne zaman, yönsüz stoplu kırılım işlemi eşlerden iyi mi. Yön tahmini yok.", "",
         "## Tanımlar (SY_ESIK)", ""]
    for k in ("S1", "S2", "S3"):
        s.append(f"- **{k}**: {E[k]['tanim']}; aynı hissede yeni olay en az {E[k]['ara']} bar sonra." + (f" Bant: BIST %8, ABD/AVR %6." if k == "S1" else ""))
    s.append(f"- **Sert düşüş alt kümesi**: {E['dusus']['tanim']}")
    for k, v in E["B"]["tanim"].items():
        s.append(f"- **{k}**: {v}")
    s += [f"- ATR birimi: {E['B']['atr_birim']}", f"- Geçerli bar: {E['gecerli_bar']}; en az {E['gecmis_min']} bar geçmiş; fiyat kesiği {E['kriz']}.",
          f"- Likidite: {E['likidite']['olcu']}; gün kesitinde alt %20 dışarıda; üçlü kova.", f"- Bölünme şüphesi: {E['bolunme']['tanim']}",
          f"- Eşleme (A): {E['eslesme']['A']}; en az {E['eslesme']['min_es']} eş.", f"- Eşleme (C): {E['eslesme']['C']}.",
          f"- Rastgele gün (K-b): {E['rastgele_gun']['takvim']}, {E['rastgele_gun']['cekilis']} çekiliş.",
          f"- Bootstrap: {E['bootstrap']['n']} tekrar, küme = {E['bootstrap']['kume']}.",
          f"- (B) zaman: pencereler {E['zaman']['pencere']}; süre = {E['zaman']['sure_tanim']}; kovalar {E['zaman']['sure_kova']}; UZUN/KISA = run>=11 / run 1-3.",
          f"- (B) model: özellikler {E['zaman']['model']['ozellik']} + σ250 ondalığı; hedef {E['zaman']['model']['hedef']}; eğitim <= {E['zaman']['model']['egit_son']} "
          f"(hedef penceresi aşmasın diye 10 gün pay), test >= {E['zaman']['model']['test_bas']}; taban {E['zaman']['model']['taban']}; {E['zaman']['model']['skill']}. "
          "Bilanço takvimi YOK (veri yok): zaman tahmini bilanço gününü bilmeden yapılır.",
          f"- (C) işlem: {E['C']['tanim']}. Komisyon / kayma YOK.",
          f"- Dönemler: {E['donem']} (keşif 2016-22; doğrulama 2023 ve 2024-26/08).",
          f"- Karar (A): {E['karar']['A']}", f"- Karar (C): {E['karar']['C']}", f"- İZ: {E['karar']['iz']}",
          "- Yorumlama sırası: ANA = S1 x B1. S2, S3, B2, B3, B0, KATI bölünme filtresi duyarlılıktır; karar etiketini değiştirmez.", "",
          "## Eşik sözlüğü (SY_ESIK, kararlı JSON)", "", "```json", json.dumps(E, sort_keys=True, ensure_ascii=False, indent=1, default=str), "```", "",
          "## Veri", ""]
    for p, h in veri_sha.items():
        s.append(f"- V_{p}.pkl sha256: `{h}`")
    s += ["", "## Olay SAYIMI (sonuç / getiri hesaplanmadan; uygun = likidite, geçmiş, 20 gün gelecek barı var, bölünme şüphesi dışı)", "",
          "| Pazar | Tanım | 2016-22 | 2023 | 2024-26 |", "|---|---|---|---|---|"]
    for p, c in sayim.items():
        for k in ("ev1", "ev1_sert", "ev2", "ev3", "ev1_c_uygun"):
            ad = {"ev1": "S1", "ev1_sert": "S1 sert düşüş", "ev2": "S2", "ev3": "S3", "ev1_c_uygun": "S1 (C için 41 bar gelecek)"}[k]
            s.append(f"| {p} | {ad} | {c[k]['2016-22']} | {c[k]['2023']} | {c[k]['2024-26']} |")
    s += ["", "| Pazar | hisse | uygun hisse-gün | bölünme şüpheli (ANA) dışlanan gün | KATI şüpheli gün |", "|---|---|---|---|---|"]
    for p, c in sayim.items():
        s.append(f"| {p} | {c['hisse']} | {c['uygun_gun']} | {c['bolunme_supheli_gun_disi']} | {c['bolunme_kati_gun']} |")
    s += ["", "## Sınırlar (önceden)", "- Evren bugünün listesi: batan / kottan çıkan hisseler yok (hayatta kalma yanlılığı).",
          "- Bilanço takvimi yok: büyük günlerin bir kısmı bilanço günüdür; model bunu bilmez.", "- Komisyon, kayma, açığa satış maliyeti yok.",
          "- BIST verisi düzeltilmiş (fi_duzelt); ABD/AVR Yahoo düzeltilmiş fiyat.", "", sy_kontrol_tablosu(), ""]
    return "\n".join(s)


def sy_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False) -> str:
    yol = _sy_yol("onkayit", cikti)
    if os.path.exists(yol) and not uzerine:
        raise SYHata(f"ön kayıt zaten var ({yol}); üzerine yazılmaz")
    if os.path.exists(yol):
        try:
            _sy_git_islenmis(yol)
            raise SYHata(f"ön kayıt git'e işlenmiş ({yol}); üzerine yazılmaz")
        except SYHata as ex:
            if "işlenmemiş" not in str(ex):
                raise
    sayim, vsha = {}, {}
    for p in SY_PAZAR:
        yolp = os.path.join(veri or SY_YOL["veri"], f"V_{p}.pkl")
        vsha[p] = _sy_sha_dosya(yolp)
        V = sy_veri_yukle(p, SY_ESIK, veri)
        P = sy_panel(V, p, SY_ESIK, sonuc=False)
        sayim[p] = sy_sayim(P)
        sylog.info("%s sayım: %s", p, sayim[p]["ev1"])
    metin = sy_onkayit_metni(sayim, vsha)
    if _SY_EPOSTA.search(metin):
        raise SYHata("ön kayıtta e-posta biçimli parça var")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    sylog.info("ön kayıt yazıldı: %s", yol)
    return yol


def sy_onkayit_dogrula(yol: Optional[str] = None, git: bool = True, kod_sha: bool = True) -> Dict[str, Any]:
    yol = yol or _sy_yol("onkayit")
    if not os.path.exists(yol):
        raise SYHata(f"ön kayıt yok ({yol}): önce `python SIKISMA_YENIDEN.py onkayit`")
    metin = open(yol, encoding="utf-8").read(); oc = {}
    for ad, desen in _SY_OC_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise SYHata(f"ön kayıt bozuk: '{ad}' yok")
        oc[ad] = m.group(1)
    if oc["muhur"] != sy_esik_sha():
        raise SYHata("ön kayıt mührü tutmuyor: eşikler ön kayıttan sonra değişmiş, koşu durdu")
    if kod_sha and oc["kod"] != _sy_sha_dosya(SY_YOL["kod"]):
        raise SYHata("kod sha256 ön kayıttakinden farklı: kod ön kayıttan sonra değişmiş (SAPMA), koşu durdu")
    out = {"yol": yol, **oc}
    if git:
        out["git"] = _sy_git_islenmis(yol)
    return out


# ---------------------------------------------------------------- 10) GELECEĞE BAKMA DENETİMİ (koşu içinde, mekanik)
def sy_gelecek_denetimi(V: Dict[str, pd.DataFrame], X: pd.DataFrame, pazar: str, E: Dict[str, Any], n: int = 40) -> int:
    """Rastgele n olayda seriyi t'de keser, geçmiş özellikleri yeniden hesaplar: tam seriyle aynı olmalı."""
    rng = np.random.default_rng(E["bootstrap"]["tohum"] + 9)
    sec = X.iloc[rng.choice(len(X), min(n, len(X)), replace=False)] if len(X) else X
    kol = ["atr", "sig", "m10", "p20", "band", "s1c", "run", "dusus", "liq", "mom", "vk", "ev1"]
    for r in sec.itertuples():
        d = V[r.sembol]
        G1 = sy_gecmis(d, pazar, E).loc[r.tarih, kol]
        G2 = sy_gecmis(d[d.index <= r.tarih], pazar, E).iloc[-1][kol]
        a = pd.to_numeric(G1, errors="coerce").astype(float).to_numpy(); b = pd.to_numeric(G2, errors="coerce").astype(float).to_numpy()
        if not np.allclose(a, b, equal_nan=True, rtol=1e-9, atol=1e-12):
            raise SYHata(f"geleceğe bakma denetimi tutmadı: {pazar} {r.sembol} {r.tarih.date()}")
    return len(sec)


# ---------------------------------------------------------------- 11) KOŞU
def sy_kos(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True, pazarlar: Tuple[str, ...] = SY_PAZAR,
           satir: Optional[str] = None) -> Dict[str, Any]:
    E = SY_ESIK; t0 = time.time()
    warnings.filterwarnings("ignore", category=RuntimeWarning)   # boş hücrede nan ortalama / bölme uyarıları (sonuç NaN olarak yazılır)
    yol = _sy_yol("onkayit", cikti)
    if kontrol:
        import IZ_KARNE as IK
        IK.ik_kontrol_kapisi(yol)
    oc = sy_onkayit_dogrula(yol, git=git)
    kos_zaman = _sy_simdi()
    satir = satir or SY_YOL["satir"]; os.makedirs(satir, exist_ok=True)
    A_, C_, B_, den = [], [], [], {}
    for p in pazarlar:
        V = sy_veri_yukle(p, E, veri)
        P = sy_panel(V, p, E, sonuc=True)
        for wi, (a, b) in enumerate(E["zaman"]["pencere"], 1):
            P[f"f{wi}"] = P.B1 & (P.k1 >= a) & (P.k1 <= b)
        tA, X1 = sy_olc_A(P, E)
        den[p] = {"gelecek_denetimi_olay": sy_gelecek_denetimi(V, X1, p, E)}
        B = sy_olc_B(P, X1, E)
        tC, XC = sy_olc_C(P, E)
        A_.append(tA); C_.append(tC); B_.append(B)
        kolA = ["pazar", "sembol", "tarih", "donem", "hucA", "oyn", "lq3", "run", "dsert", "m10", "atr", "sig", "band", "vk",
                "B1", "k1", "B1_5", "B0", "B2", "B3", "f1", "f2", "f3", "f4", "es_B1", "es_B2", "es_B3", "es_B0", "es_B1_5",
                "es_f1", "es_f2", "es_f3", "es_f4", "es_n"]
        X1[kolA].to_csv(os.path.join(satir, f"olay_A_{p}.csv.gz"), index=False)
        es = P.loc[P.uygun & ~P.s1c, ["tarih", "hucA", "B1", "B2", "B3"]]
        es.groupby(["tarih", "hucA"]).agg(B1_t=("B1", "sum"), B2_t=("B2", "sum"), B3_t=("B3", "sum"), n=("B1", "size")).reset_index() \
            .to_csv(os.path.join(satir, f"es_A_{p}.csv.gz"), index=False)
        kolC = ["pazar", "sembol", "tarih", "donem", "hucC", "c_yon", "c_r", "c_giris", "c_cikis", "c_ilk20", "c_ilk10", "es_r", "sira", "es_n", "islem"]
        XC[kolC].to_csv(os.path.join(satir, f"olay_C_{p}.csv.gz"), index=False)
        P.loc[P.uygun_c & ~P.s1c & (P.c_yon != 0), ["tarih", "hucC", "sembol", "c_r"]].to_csv(os.path.join(satir, f"es_C_{p}.csv.gz"), index=False)
        sylog.info("%s bitti (%.0f sn)", p, time.time() - t0)
        del P, V
    TA = pd.concat(A_, ignore_index=True); TC = pd.concat(C_, ignore_index=True)
    karar = sy_karar_genel(TA, TC, B_, E)
    sonuc = {"surum": SY_SURUM, "onkayit": oc, "kos_zaman_utc": kos_zaman, "sure_sn": round(time.time() - t0, 1), "muhur": sy_esik_sha(),
             "A": json.loads(TA.to_json(orient="records", force_ascii=False)), "C": json.loads(TC.to_json(orient="records", force_ascii=False)),
             "B": json.loads(json.dumps(B_, default=float)), "karar": karar, "denetim": den, "pazarlar": list(pazarlar)}
    os.makedirs(cikti or SY_YOL["cikti"], exist_ok=True)
    with open(_sy_yol("sonuc", cikti), "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1, default=str)
    rapor = sy_rapor(cikti)
    return {"sonuc": sonuc, "rapor": rapor}


def sy_karar_genel(TA: pd.DataFrame, TC: pd.DataFrame, B_: List[Dict[str, Any]], E: Dict[str, Any]) -> Dict[str, str]:
    out = {}
    A = TA[(TA.sikisma == "S1") & (TA.olcu == "B1")]
    def k(T, p, d, kol="karar"):
        x = T[(T.pazar == p) & (T.donem == d)]
        return x[kol].iat[0] if len(x) else "ÖLÇÜLEMEDİ"
    for ad, T, tut in (("A", A, "TUTAR"), ("C", TC, "TUTAR")):
        hucre = {f"{p} {d}": k(T, p, d) for p in E["karar_pazar"] for d in E["karar_donem"]}
        kesif = {p: (float(T[(T.pazar == p) & (T.donem == E["kesif"])][("kat" if ad == "A" else "ort_fark")].iat[0])
                     if len(T[(T.pazar == p) & (T.donem == E["kesif"])]) else np.nan) for p in E["karar_pazar"]}
        yon_ok = all(np.isfinite(v) and (v > 1 if ad == "A" else v > 0) for v in kesif.values())
        v_ = list(hucre.values())
        olumsuz = [v for v in v_ if v in ("TUTMADI", "TERS")]
        olcmez = [v for v in v_ if v.startswith("ÖLÇÜLEMEDİ")]
        if all(v == tut for v in v_) and yon_ok:
            g = "İZ"
        elif all(v == tut for v in v_):
            g = "İZ DEĞİL (keşif dönemi ters yön)"
        elif len(olumsuz) == len(v_):
            g = "İZ DEĞİL" + (" (TERS: sıkışma büyük hareketi azaltıyor)" if all(v == "TERS" for v in v_) else "")
        elif olumsuz:
            g = "İZ DEĞİL (hücreler çelişkili: " + ", ".join(f"{a}={b}" for a, b in hucre.items()) + ")"
        elif olcmez:
            g = "ÖLÇÜLEMEDİ" + (" (öteki hücreler olumlu)" if any(v == tut or v.startswith("EMARE") for v in v_) else "")
        else:
            g = "ADAY (dört hücre olumlu, güç sınırlı hücre var)" if yon_ok else "ADAY DEĞİL (keşif dönemi ters yön)"
        bist = {d: k(T, "BIST", d) for d in E["karar_donem"]}
        out[ad] = g; out[ad + "_hucre"] = json.dumps(hucre, ensure_ascii=False); out[ad + "_bist"] = json.dumps(bist, ensure_ascii=False)
    sk = {}
    for b in B_:
        for m in b.get("model", []):
            if m.get("donem") in E["karar_donem"]:
                sk[f"{b['pazar']} {m['donem']}"] = m.get("alt95", np.nan)
    karar_sk = {k_: v for k_, v in sk.items() if k_.split()[0] in E["karar_pazar"]}
    us = {}
    for b in B_:
        for r in b.get("tehlike", []):
            if r.get("sure") == "UZUN/KISA" and r.get("donem") in E["karar_donem"]:
                us[f"{b['pazar']} {r['donem']}"] = r.get("alt95", np.nan)
    karar_us = {k_: v for k_, v in us.items() if k_.split()[0] in E["karar_pazar"]}
    out["B_sure_tehlike"] = ("ARTIYOR" if len(karar_us) == 4 and all(np.isfinite(v) and v > 1 for v in karar_us.values()) else "ARTIŞ KANITI YOK") + \
        " (UZUN/KISA kat alt95: " + ", ".join(f"{k_} {v:.2f}" for k_, v in us.items()) + ")"
    out["B_zaman_tahmini"] = ("VAR" if len(karar_sk) == 4 and all(np.isfinite(v) and v > 0 for v in karar_sk.values()) else "YOK") + " (skill alt95: " + \
        ", ".join(f"{k_} {v:+.4f}" for k_, v in sk.items()) + ")"
    return out


# ---------------------------------------------------------------- 12) RAPOR
def _yz(x: Any, n: int = 1) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "—"
    return "—" if not np.isfinite(x) else ("%" + f"{100 * x:.{n}f}").replace(".", ",")


def _sy(x: Any, n: int = 2) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "—"
    return "—" if not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


def sy_rapor(cikti: Optional[str] = None) -> str:
    yol = _sy_yol("sonuc", cikti)
    if not os.path.exists(yol):
        raise SYHata(f"sonuç yok: {yol}")
    S = json.load(open(yol, encoding="utf-8"))
    A = pd.DataFrame(S["A"]); C = pd.DataFrame(S["C"]); K = S["karar"]
    a1 = A[(A.sikisma == "S1") & (A.olcu == "B1")]
    def h(p, d):
        x = a1[(a1.pazar == p) & (a1.donem == d)]
        return x.iloc[0] if len(x) else None
    oz = []
    for p in S["pazarlar"]:
        x = h(p, "2023+")
        if x is not None:
            oz.append(f"{p}: sıkışmadan sonra 20 günde büyük gün olasılığı {_yz(x.p_olay)}, eşlerde {_yz(x.p_es)} -> kat {_sy(x.kat)} ({_sy(x.alt95)}-{_sy(x.ust95)}), n {int(x.n)} (2023-26/08)")
    s = [f"# SIKISMA_YENIDEN — RAPOR\n", f"{S['surum']}. Ön kayıt mühür `{S['onkayit']['muhur'][:12]}`, ön kayıt commit `{S['onkayit'].get('git', {}).get('commit', '')[:10]}` "
         f"({S['onkayit'].get('git', {}).get('commit_zamani', '')}); koşu {S['kos_zaman_utc']} ({S['sure_sn']} sn).\n",
         "## DÜZ DİL ÖZET", "",
         f"- **Sıkışmadan sonra büyük hareket geliyor mu?** (A) karar: **{K['A']}** (hücreler {K['A_hucre']}; BIST bilgi {K['A_bist']}).",
         *[f"  - {o}" for o in oz]]
    bz = {b["pazar"]: b for b in S["B"]}
    for p in S["pazarlar"]:
        d = [r for r in bz[p]["dagilim"] if r["donem"] == "2023+"]
        if d and "medyan" in d[0]:
            d = d[0]
            s.append(f"- **Ne zaman?** {p}: ilk büyük gün medyan {_sy(d['medyan'], 0)}. gün (%25-75: {_sy(d['c25'], 0)}-{_sy(d['c75'], 0)}); "
                     f"1-5. gün penceresi kat {_sy(d.get('kat_1_5'))} ({_sy(d.get('alt_1_5'))}-{_sy(d.get('ust_1_5'))}).")
    s.append(f"- **Sıkışma uzadıkça 5 gün içinde büyük gün olasılığı artıyor mu?** {K.get('B_sure_tehlike', '—')}.")
    s.append(f"- **Önceden tahmin (zaman)**: {K['B_zaman_tahmini']}.")
    s.append(f"- **Yönsüz stoplu işlem kazandırıyor mu?** (C) karar: **{K['C']}** (hücreler {K['C_hucre']}; BIST bilgi {K['C_bist']}).")
    for r in C[C.donem == "2023+"].itertuples():
        s.append(f"  - {r.pazar} 2023-26/08: işlem başı ortalama {_yz(getattr(r, 'ort_r', np.nan))}, eşler {_yz(getattr(r, 'ort_es_r', np.nan))}, "
                 f"eşli fark {_yz(getattr(r, 'ort_fark', np.nan), 2)} ({_yz(getattr(r, 'alt95', np.nan), 2)} / {_yz(getattr(r, 'ust95', np.nan), 2)}), n {r.n}")
    s += ["- Komisyon / kayma yok; evren bugünün listesi (batanlar yok); bilanço takvimi yok.", "",
          "## (A) OLASILIK TABLOSU — S1 sıkışma x B1 büyük gün (ANA)", "",
          "| Pazar | Dönem | n olay | P(B1 / sıkışma) | P(B1 / eş) | KAT | alt95 | üst95 | aynı hisse rastgele gün P | olay yüzdeliği | Karar |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in a1.itertuples():
        s.append(f"| {r.pazar} | {r.donem} | {r.n} | {_yz(r.p_olay)} | {_yz(r.p_es)} | {_sy(r.kat)} | {_sy(r.alt95)} | {_sy(r.ust95)} | "
                 f"{_yz(getattr(r, 'rast_p', np.nan))} | {_sy(getattr(r, 'olay_yuzdelik', np.nan))} | {r.karar} |")
    s += ["", "### Duyarlılık: tanım x ölçü (KAT, alt95-üst95, n)", "", "| Pazar | Dönem | Sıkışma | B1 | B2 | B3 | B0 (göreli, tanımsal) | B1_5 (5 gün) |", "|---|---|---|---|---|---|---|---|"]
    for (p, d, sk), g in A[A.sikisma != "TABAN_tum_gunler"].groupby(["pazar", "donem", "sikisma"], sort=False):
        hc = []
        for b in ("B1", "B2", "B3", "B0", "B1_5"):
            x = g[g.olcu == b]
            hc.append(f"{_sy(x.kat.iat[0])} ({_sy(x.alt95.iat[0])}-{_sy(x.ust95.iat[0])}) n{int(x.n.iat[0])}" if len(x) else "—")
        s.append(f"| {p} | {d} | {sk} | " + " | ".join(hc) + " |")
    tb = A[A.sikisma == "TABAN_tum_gunler"]
    s += ["", "Taban (bütün uygun hisse-günler, B1 oranı): " + "; ".join(f"{r.pazar} {r.donem} {_yz(r.p_olay)} (n {int(r.n)})" for r in tb.itertuples()), "",
          "## (B) ZAMAN", "", "### İlk büyük gün (S1 olayları, B1 gerçekleşenler) ve pencere katları (eşli)", "",
          "| Pazar | Dönem | n olay | n B1 | medyan gün | %25-%75 | 1-5 kat (alt-üst) | 6-10 | 11-15 | 16-20 |", "|---|---|---|---|---|---|---|---|---|---|"]
    for b in S["B"]:
        for r in b["dagilim"]:
            s.append(f"| {b['pazar']} | {r['donem']} | {r['n_olay']} | {r['n_b1']} | {_sy(r.get('medyan'), 0)} | {_sy(r.get('c25'), 0)}-{_sy(r.get('c75'), 0)} | " +
                     " | ".join(f"{_sy(r.get(f'kat_{a}_{c}'))} ({_sy(r.get(f'alt_{a}_{c}'))}-{_sy(r.get(f'ust_{a}_{c}'))})" for a, c in ((1, 5), (6, 10), (11, 15), (16, 20))) + " |")
    s += ["", "Günlere göre ilk büyük gün sayısı (2023+; 1..20. gün): " + "; ".join(
        f"{b['pazar']} {[r.get('hist') for r in b['dagilim'] if r['donem'] == '2023+'][0]}" for b in S["B"]), "",
          "### Sıkışma süresine göre 5 gün içinde büyük gün (bütün sıkışık günler, eşli)", "",
          "| Pazar | Dönem | Süre (gün) | n gün | P5 sıkışık | P5 eş | KAT | alt95 | üst95 |", "|---|---|---|---|---|---|---|---|---|"]
    for b in S["B"]:
        for r in b["tehlike"]:
            s.append(f"| {b['pazar']} | {r['donem']} | {r['sure']} | {r['n_gun']} | {_yz(r.get('p5'))} | {_yz(r.get('es_p5'))} | {_sy(r.get('kat'))} | {_sy(r.get('alt95'))} | {_sy(r.get('ust95'))} |")
    s += ["", "### Önceden tahmin: lojistik walk-forward (2016-22 eğit, 2023+ test; hedef 5 gün içinde B1; yalnız t'ye kadarki bilgi; bilanço takvimi YOK)", "",
          "| Pazar | Test dönemi | n gün | gerçek oran | Brier model | Brier taban | SKILL | alt95 | üst95 | model tepe %10 gerçek oran | aynı günlerde taban |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for b in S["B"]:
        for r in b["model"]:
            s.append(f"| {b['pazar']} | {r['donem']} | {r['n']} | {_yz(r.get('y_ort'))} | {_sy(r.get('brier_model'), 4)} | {_sy(r.get('brier_taban'), 4)} | "
                     f"{_sy(r.get('skill'), 4)} | {_sy(r.get('alt95'), 4)} | {_sy(r.get('ust95'), 4)} | {_yz(r.get('tepe10_oran'))} | {_yz(r.get('tepe10_taban'))} |")
    s += ["", "Model katsayıları (standart ölçek): " + "; ".join(
        f"{b['pazar']}: " + ", ".join(f"{a} {w:+.3f}" for a, w in zip(b["model_katsayi"]["ad"][:5], b["model_katsayi"]["w"][:5])) for b in S["B"] if "model_katsayi" in b), "",
          "## (C) YÖNSÜZ STOPLU KIRILIM İŞLEMİ (S1 olayları; FI_OLCUT dört şart)", "",
          "| Pazar | Dönem | n olay | işlem oranı | n işlem | ort getiri | medyan | eş ort | eşli fark | alt95 | üst95 | sıra | kazanan | uzun payı | P(+%20 önce) | eş | P(-%10 önce) | eş | portföy | eş p90 | Karar |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in C.itertuples():
        g = lambda a: getattr(r, a, np.nan)
        s.append(f"| {r.pazar} | {r.donem} | {r.n_olay} | {_yz(r.islem_orani)} | {r.n} | {_yz(g('ort_r'), 2)} | {_yz(g('medyan_r'), 2)} | {_yz(g('ort_es_r'), 2)} | "
                 f"{_yz(g('ort_fark'), 2)} | {_yz(g('alt95'), 2)} | {_yz(g('ust95'), 2)} | {_sy(g('sira'))} | {_yz(g('kazanan'))} | {_yz(g('uzun_pay'))} | "
                 f"{_yz(g('p_ilk20'))} | {_yz(g('es_p_ilk20'))} | {_yz(g('p_ilk10'))} | {_yz(g('es_p_ilk10'))} | {_yz(g('portfoy'))} | {_yz(g('port_es_p90'))} | {r.karar} |")
    s += ["", "## Denetim (koşu içi)", "", "- Geleceğe bakma: " + "; ".join(f"{p} {v['gelecek_denetimi_olay']} olayda seri t'de kesildi, özellikler aynı" for p, v in S["denetim"].items()),
          "", "## Sınırlar", "- Evren bugünün listesi (batanlar yok): büyük hareket olasılığı ve işlem getirisi bu yüzden yanlı olabilir.",
          "- Bilanço takvimi yok; komisyon / kayma / açığa satış maliyeti yok.", "- B1 eşiği ATR250'yi kullanır; sıkışma dönemi ATR'yi biraz düşürür (mekanik, eşleme oynaklık ondalığıyla kısmen dengelenir); B0 tanımsaldır, karar dışı.", ""]
    metin = "\n".join(s)
    with open(_sy_yol("rapor", cikti), "w", encoding="utf-8") as f:
        f.write(metin)
    return metin


# ---------------------------------------------------------------- 13) DUYARLILIK (Ç176 adayı; 14 Kasım 2026, Cemal'in itirazı: "büyük mum" ölçeği ve sıkışma uzunluğu)
# Bilgi çalışmasıdır: Ç174 kararı (sy_kos, SY_ESIK) DEĞİŞMEZ. Kendi eşik sözlüğü (SY_DUY), kendi mührü ve kendi ön kaydı vardır.
SY_DUY_DOSYA = {"onkayit": "DUYARLILIK_ON_KAYIT.md", "sonuc": "duyarlilik_sonuc.json", "rapor": "DUYARLILIK_RAPOR.md",
                "pdf": "SIKISMA_ORNEK_40.pdf", "anahtar": "ornek_anahtar.json"}
SY_DUY_GRAFIK_KL = os.environ.get("SY_GRAFIK", "/tmp/sikisma/grafik")

SY_DUY: Dict[str, Any] = {
    "surum": "SIKISMA_YENIDEN duyarlilik v1.0 (2026-11-14)",
    "c174_muhur": "1eb406a20091e4cb54c6cf3986f27f36e5c5ba3cbc61868ba83be53d8e7105b0",   # Ç174 SY_ESIK mührü (taban tanımlar oradan)
    "k": [1.5, 2.0, 2.5, 3.0, 4.0],
    "ref": {"ATR250": "t-249..t ortalama TR/C_önceki (Ç174 ile aynı; sıkışma dönemi dahil)",
            "ATR60": "t-p-60..t-p-1 ortalama TR/C_önceki (60 gün, sıkışma penceresi HARİÇ; p=10 için t-70..t-11)",
            "ATR_sik": "sıkışma penceresi ortalama TR/C_önceki (t-p+1..t; GÖRELİ, tanımsal: sıkışma tanımı bunu küçük yapar; yalnız kıyas, yorum dışı)"},
    "ufuk": {"20": [1, 20], "5": [1, 5]},
    "buyuk_tanim": "t+a..t+b içinde en az bir günün TR/C_önceki >= k x REF (TR = max(H, C_önceki) - min(L, C_önceki))",
    "pencere": [10, 20, 40, 60],
    "sikisma": {"yuzdelik": 0.20, "dagilim": 250, "ara": 20, "bas": "i >= 250 + p (geçerli bar sırası)",
                "bant": "SY_ESIK S1 bandı (BIST %8, ABD/AVR %6) x sqrt(p/10)",
                "tanim": "ort(TR/C_önceki, son p gün) <= TR/C'nin t-p-249..t-p yüzdelik %20'si VE (max C - min C)/C_t (son p gün) <= bant x sqrt(p/10); "
                         "p=10 Ç174 S1 ile birebir aynı (koşuda mekanik denetlenir); aynı hissede yeni olay en az 20 bar sonra"},
    "gecerli": "Ç174 'uygun' (likidite alt %20 dışı, 260 bar geçmiş, 20 gün gelecek barı var, bölünme şüphesi dışı) VE p için yüzdelik ile ATR60 tanımlı",
    "es": {"es1": "Ç174 eşi: aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü (hucA), p sıkışma koşulu yanlış, geçerli",
           "es2": "EK KONTROL (Ç175 önerisi): aynı gün, aynı pazar, (ort TR/C son p gün / ATR250) oranının gün içi 20'liği x likidite üçlüsü, "
                  "p sıkışma koşulu yanlış, geçerli (p=10'da oran = ATR10 / ATR250)",
           "oran_kova": 20, "min_es": 3, "olay_secimi": "olay her eş kümesinde ayrı ayrı en az 3 eşle kalır (iki kümede n farklı olabilir)"},
    "donem": [["2016-22", "2016-01-01", "2022-12-31"], ["2023", "2023-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-08-31"]],
    "birlesik": {"2023+": ["2023", "2024-26"]},
    "ana": "ABD ve AVR, 2023 / 2024-26 / 2023+ (bilgi); BIST ve 2016-22 bilgi",
    "olcu": "KAT = olay oranı / eş oranı (eş oranı = olay başına aynı hücre eş ortalaması); ay kümeli bootstrap %95",
    "bootstrap": {"n": 2000, "kume": "olay ayı (t)", "guven": [0.025, 0.975], "tohum": 1476,
                  "p": "iki yönlü bootstrap p = 2 x min(P(KAT_b <= 1), P(KAT_b >= 1)), en az 1/n"},
    "bh": {"q": 0.10, "aile": "REF ATR250 ve ATR60, üç ayrı dönem (2023+ hariç), iki eş kümesi, bütün k, ufuk, p, pazar (5x2x2x4x2x3x3 = 1440 sınama)",
           "not": "BH yalnız BİLGİ; hiçbir hücre tek başına bulgu değildir; karar Ç174'tedir"},
    "yon": "n < 30 ÖLÇÜLEMEDİ; alt95 > 1 'KAT>1'; üst95 < 1 'KAT<1'; değilse 'belirsiz' (etiket bilgi, karar değil)",
    "dagilim_olcu": {"R_sik": "ilk 20 günün en büyük TR/C_önceki / sıkışma penceresi ort TR/C_önceki (Cemal'in gözü: küçük mumlardan sonra gelen mum)",
                     "R_250": "ilk 20 günün en büyük TR/C_önceki / ATR250", "R_60": "ilk 20 günün en büyük TR/C_önceki / ATR60",
                     "es_agirlik": "eş dağılımı: her olayın hücresindeki eşler 1 / (hücre eş sayısı) ağırlıkla (her olay toplam 1 ağırlık)",
                     "yuzdelik": [0.25, 0.50, 0.75]},
    "tutarlilik_c174": "p=10, eş1, ufuk 20: k=3 ATR250 = Ç174 B1; k=3 ATR_sik = Ç174 B0; ufuk 5, k=3 ATR250 = Ç174 B1_5; "
                       "her pazar x dönemde n, olay oranı, eş oranı, KAT sikisma_sonuc.json ile 1e-9 içinde aynı olmalı, değilse koşu durur",
    "grafik": {"pazar": "ABD", "donem": ["2023", "2024-26"], "kume": "Ç174 S1 olayları (p=10, eş1 ile en az 3 eş)", "n_olay": 20, "n_es": 20, "tohum": 27,
               "es_secimi": "her seçilen olay için aynı gün, aynı hucA hücresindeki eşlerden (S1 koşulu yanlış, geçerli) rastgele bir hisse-gün",
               "sira": "40 grafik aynı tohumla karıştırılır; numara 1-40; 'olay' / 'eş' etiketi yalnız anahtarda",
               "once": 120, "sonra": 20, "px_ln110": 40, "genislik": 1200, "dpi": 100, "fiyat_min_px": 260, "fiyat_max_px": 760, "alt_px": 210,
               "esik": [2.0, 3.0], "golge": "son 10 gün (t-9..t) gri gölge; t ile t+1 arası kesikli dikey çizgi",
               "alt_panel": "günlük TR/C_önceki (%) çubukları; yatay çizgiler 2 x ve 3 x ATR250(t)", "normal": "fiyat / C_t x 100, ln ekseni"},
    "denetim_hucre": [{"pazar": "ABD", "p": 10, "ref": "ATR250", "k": 2.0, "ufuk": "20", "es": "es1", "donem": "2023+"},
                      {"pazar": "AVR", "p": 40, "ref": "ATR60", "k": 3.0, "ufuk": "20", "es": "es2", "donem": "2024-26"}],
}
_SY_DUY_REF = ("ATR250", "ATR60", "ATR_sik")

SY_DUY_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş1 = Ç174 eşi (aynı gün/pazar, σ250 ondalığı x likidite üçlüsü, p sıkışma dışı); eş2 = aynı gün, (ort TR/C son p / ATR250) 20'liği x likidite üçlüsü "
                   "(sıkışmanın ATR250'yi düşürmesinden gelen mekanik farkı dengeler); aynı büyük mum tanımı eşlere de uygulanır; ATR_sik göreli/tanımsal: yorum dışı"),
    "K2": ("EVET", "sy_duy_gecmis yalnız t'ye kadar (sıkışma, ATR250, ATR60, oran); büyük mum sy_duy_sonuc'ta t+1..t+20; test_sikisma_yeniden.py 12) kesme testi; "
                   "hücreler t günü kesiti; ATR60 t-p-60..t-p-1"),
    "K3": ("EVET", "sy_veri_hazirla (Ç174): H>L ve V>0 olmayan bar atılır; günlük veri; fiyat kesiği 31.08.2026"),
    "K4": ("EVET", "aynı hissede olay en az 20 bar arayla (her p için); n = olay sayısı; ay kümeli bootstrap; dağılımlarda medyan + %25-75"),
    "K5": ("UYGULANMAZ", "getiri / işlem yok; yalnız t kapanışındaki bilgiyle t+1..t+20 gün aralığı olasılığı ve dağılımı"),
    "K6": ("EVET", "tek kip fi_k1_veri düzeltilmiş fiyat; TR yüzde (TR / önceki kapanış) her REF için aynı birim; bölünme şüphesi Ç174 sy_bolunme_supheli ile dışarıda"),
    "K7": ("EVET", "evren bugünün listesi (batanlar yok); raporda yazılı; büyük gün olasılığı olay ve eşte birlikte etkilenir, KAT yönü yazılı sınır"),
    "K8": ("EVET", "3 pazar x 3 dönem (+2023+); n<30 ÖLÇÜLEMEDİ; 1440 sınamalık aile BH q 0,10 yalnız bilgi; hiçbir hücre tek başına bulgu değil; karar Ç174"),
    "K9": ("EVET", "SY_DUY sha256 mühür + SIKISMA_YENIDEN.py sha256 + olay SAYIMI (sonuçsuz) DUYARLILIK_ON_KAYIT.md'de; commit + push sonra `duyarlilik`; "
                   "kos öncesi kontrol kapısı + mühür + kod sha + git kapısı; eşik sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV; 2 grafik ham veriden elle doğrulanır (rapor denetim)"),
    "K11": ("EVET", "p=10 Ç174 hücreleri koşu içinde mekanik eşitlik denetimi (durdurucu); 2 hücre (SY_DUY denetim_hucre) satır dosyasından bağımsız kodla yeniden üretilir"),
    "K12": ("EVET", "'bulgu / iz' sözü yok: duyarlılık bilgidir; KAT>1 / KAT<1 yalnız güven aralığı etiketi; sayı ile yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_sy korunur; yasak defter dosyalarına dokunulmaz (git diff); e-posta / anahtar taraması testte; ücretli veri yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; yalnız ölçüm"),
}


def sy_duy_sha(D: Optional[Dict[str, Any]] = None) -> str:
    s = json.dumps(D or SY_DUY, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _sy_duy_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or SY_YOL["cikti"], SY_DUY_DOSYA.get(ad, ad))


def sy_duy_gecmis(d: pd.DataFrame, pazar: str, D: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Her bar i için yalnız i'ye kadarki barlardan: her p için ort TR/C (m_p), yüzdelik (q_p), bant (b_p), sıkışma koşulu (s_p), olay (e_p), ATR60 (a60_p);
    ATR250 (atr). Geleceğe bakma yok (test 12 kesme testi)."""
    D = D or SY_DUY; E = E or SY_ESIK; S = D["sikisma"]
    H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close"))
    n = len(C); Cp = np.r_[np.nan, C[:-1]]
    tr = np.fmax(H, Cp) - np.fmin(L, Cp); tr[0] = H[0] - L[0]
    T = pd.Series(tr / Cp); Cs = pd.Series(C)
    out = {"atr": T.rolling(E["B"]["atr_gun"], min_periods=E["B"]["atr_gun"]).mean().to_numpy()}
    q = T.rolling(S["dagilim"], min_periods=S["dagilim"]).quantile(S["yuzdelik"])
    r60 = T.rolling(60, min_periods=60).mean()
    ii = np.arange(n)
    for p in D["pencere"]:
        m = T.rolling(p, min_periods=p).mean().to_numpy()
        qp = q.shift(p).to_numpy()
        b = ((Cs.rolling(p).max() - Cs.rolling(p).min()) / Cs).to_numpy()
        with np.errstate(invalid="ignore"):
            s = (m <= qp) & (b <= E["S1"]["bant"][pazar] * math.sqrt(p / 10.0)) & (ii >= S["dagilim"] + p)
        out[f"m{p}"] = m; out[f"q{p}"] = qp; out[f"s{p}"] = s; out[f"e{p}"] = _sy_olay(s, S["ara"], S["dagilim"] + p)
        out[f"a60_{p}"] = r60.shift(p + 1).to_numpy()
    return pd.DataFrame(out, index=d.index)


def sy_duy_sonuc(d: pd.DataFrame, D: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """t'den SONRASI (yalnız ölçümde): ilk 20 ve ilk 5 günün en büyük TR/C_önceki."""
    D = D or SY_DUY
    H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close"))
    Cp = np.r_[np.nan, C[:-1]]
    tr = np.fmax(H, Cp) - np.fmin(L, Cp); tr[0] = H[0] - L[0]
    out = {}
    for u, (a, b) in D["ufuk"].items():
        F = _sy_ileri(tr / Cp, b)[:, a - 1:b]
        with np.errstate(invalid="ignore"), warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            mx = np.nanmax(F, axis=1)
        mx[np.isnan(F).any(axis=1)] = np.nan          # pencere tam değilse tanımsız
        out[f"mx{u}"] = mx
    return pd.DataFrame(out, index=d.index)


def sy_duy_panel(V: Dict[str, pd.DataFrame], pazar: str, D: Optional[Dict[str, Any]] = None, sonuc: bool = True) -> pd.DataFrame:
    """Ç174 paneli (sy_panel, sonuc=False: uygun, hucA, lq3, donem) + duyarlılık özellikleri; yalnız uygun satırlar. Hücre eş2 her p için gün kesitinde."""
    D = D or SY_DUY; E = SY_ESIK
    P = sy_panel(V, pazar, E, sonuc=False)
    P = P.loc[P.uygun, ["sembol", "tarih", "pazar", "donem", "hucA", "lq3", "s1c", "ev1", "atr"]].reset_index(drop=True)
    parca = []
    for s, d in V.items():
        try:
            G = sy_duy_gecmis(d, pazar, D, E)
            if sonuc:
                G = pd.concat([G, sy_duy_sonuc(d, D)], axis=1)
            G = G.drop(columns=["atr"])
            G["sembol"] = s; G["tarih"] = d.index
            parca.append(G.reset_index(drop=True))
        except Exception as ex:
            sylog.warning("%s %s duyarlılık dışı: %s", pazar, s, ex)
    Z = pd.concat(parca, ignore_index=True)
    P = P.merge(Z, on=["sembol", "tarih"], how="left", validate="one_to_one")
    if P["m10"].isna().any():
        raise SYHata(f"{pazar}: duyarlılık özellikleri {int(P['m10'].isna().sum())} uygun satırda eşleşmedi")
    if not (P.s10.astype(bool).to_numpy() == P.s1c.to_numpy()).all() or not (P.e10.astype(bool).to_numpy() == P.ev1.to_numpy()).all():
        raise SYHata(f"{pazar}: p=10 sıkışma / olay Ç174 S1 ile aynı değil (tanım kayması)")
    for p in D["pencere"]:
        P[f"g{p}"] = np.isfinite(P[f"q{p}"]) & np.isfinite(P[f"a60_{p}"]) & np.isfinite(P[f"m{p}"])
        P[f"s{p}"] = P[f"s{p}"].astype(bool); P[f"e{p}"] = P[f"e{p}"].astype(bool) & P[f"g{p}"]
        g = P[f"g{p}"]
        oran = (P.loc[g, f"m{p}"].astype(float) / P.loc[g, "atr"].astype(float))
        rk = oran.groupby(P.loc[g, "tarih"]).rank(pct=True, method="first")
        P[f"h2_{p}"] = -1
        P.loc[g, f"h2_{p}"] = ((np.ceil(rk * D["es"]["oran_kova"]) - 1).astype(int) * 10 + P.loc[g, "lq3"]).astype(int)
    return P


def sy_duy_sayim(P: pd.DataFrame, D: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, int]]:
    """Olay SAYIMI (sonuç kullanmaz): her p için geçerli olay ve eş1 / eş2 ile en az 3 eşi olan olay sayısı."""
    D = D or SY_DUY; out = {}
    for p in D["pencere"]:
        g = P[f"g{p}"]; ol = g & P[f"e{p}"]; es = g & ~P[f"s{p}"]
        r = {}
        for ek, huc in (("es1", "hucA"), ("es2", f"h2_{p}")):
            say = P[es].groupby(["tarih", huc]).size().rename("es_n")
            X = P.loc[ol, ["tarih", huc, "donem"]].merge(say, left_on=["tarih", huc], right_index=True, how="left")
            X = X[X.es_n.fillna(0) >= D["es"]["min_es"]]
            for dn in [x[0] for x in D["donem"]]:
                r[f"{ek} {dn}"] = int((X.donem == dn).sum())
        r["olay_tum"] = int(ol.sum())
        out[f"p{p}"] = r
    return out


def _sy_duy_boot(Pay: np.ndarray, Payda: np.ndarray, ay: np.ndarray, D: Dict[str, Any], tohum: int) -> Dict[str, np.ndarray]:
    """Sütun başına KAT = sum(pay) / sum(payda); ortak ay kümeli bootstrap (aynı çekilişler bütün sütunlarda). Döner kat, alt, ust, p."""
    M = Pay.shape[1]
    if len(Pay) == 0:
        z = np.full(M, np.nan); return {"kat": z, "alt": z, "ust": z, "p": z}
    aylar, inv = np.unique(ay, return_inverse=True)
    SP = np.zeros((len(aylar), M)); SQ = np.zeros((len(aylar), M))
    np.add.at(SP, inv, Pay); np.add.at(SQ, inv, Payda)
    B = D["bootstrap"]; rng = np.random.default_rng(B["tohum"] + tohum)
    W = rng.multinomial(len(aylar), np.full(len(aylar), 1 / len(aylar)), size=B["n"]).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        KB = (W @ SP) / (W @ SQ); kat = Pay.sum(0) / Payda.sum(0)
    a, b = B["guven"]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        alt = np.nanquantile(KB, a, axis=0); ust = np.nanquantile(KB, b, axis=0)
        gec = np.isfinite(KB)
        pl = (np.where(gec, KB <= 1, False).sum(0)) / np.maximum(gec.sum(0), 1)
        pu = (np.where(gec, KB >= 1, False).sum(0)) / np.maximum(gec.sum(0), 1)
    p = np.clip(2 * np.minimum(pl, pu), 1.0 / B["n"], 1.0)
    p[~np.isfinite(kat)] = np.nan
    return {"kat": kat, "alt": alt, "ust": ust, "p": p}


def _sy_duy_yon(n: int, alt: float, ust: float) -> str:
    if n < SY_ESIK["karar"]["n_min"] or not np.isfinite(alt):
        return "ÖLÇÜLEMEDİ"
    return "KAT>1" if alt > 1 else ("KAT<1" if ust < 1 else "belirsiz")


def _sy_duy_kolon(D: Dict[str, Any]) -> List[Tuple[str, str, float, str]]:
    """(sütun adı, REF, k, ufuk) listesi."""
    return [(f"b_{r}_{k:g}_{u}", r, k, u) for u in D["ufuk"] for r in _SY_DUY_REF for k in D["k"]]


def _sy_wq(x: np.ndarray, w: np.ndarray, qs: List[float]) -> List[float]:
    m = np.isfinite(x) & np.isfinite(w) & (w > 0)
    x, w = x[m], w[m]
    if not len(x):
        return [np.nan] * len(qs)
    o = np.argsort(x, kind="mergesort"); x, w = x[o], w[o]
    c = (np.cumsum(w) - 0.5 * w) / w.sum()
    return [float(np.interp(q, c, x)) for q in qs]


def sy_duy_olc(P: pd.DataFrame, D: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, pd.DataFrame]]:
    """Döner: KAT tablosu, dağılım tablosu, olay satırları (anahtar 'p{p}_{es}': olay + eş ortalamaları; denetim / yeniden üretim için)."""
    D = D or SY_DUY
    pazar = P.pazar.iat[0]; kol = _sy_duy_kolon(D); ad = [c[0] for c in kol]
    sat, dag, olaylar = [], [], {}
    qs = D["dagilim_olcu"]["yuzdelik"]
    for p in D["pencere"]:
        g = P[f"g{p}"]; ol = g & P[f"e{p}"]; es = g & ~P[f"s{p}"]
        ref = {"ATR250": P.atr.to_numpy(float), "ATR60": P[f"a60_{p}"].to_numpy(float), "ATR_sik": P[f"m{p}"].to_numpy(float)}
        mx = {u: P[f"mx{u}"].to_numpy(float) for u in D["ufuk"]}
        Bm = {}
        with np.errstate(invalid="ignore"):
            for c, r, k, u in kol:
                Bm[c] = (mx[u] >= k * ref[r]).astype(float)
        Q = pd.DataFrame(Bm, index=P.index)
        Q["R_sik"] = mx["20"] / ref["ATR_sik"]; Q["R_250"] = mx["20"] / ref["ATR250"]; Q["R_60"] = mx["20"] / ref["ATR60"]
        Q["tarih"] = P.tarih; Q["donem"] = P.donem; Q["sembol"] = P.sembol; Q["hucA"] = P.hucA; Q[f"h2_{p}"] = P[f"h2_{p}"]
        Q["mx20"] = P.mx20; Q["mx5"] = P.mx5; Q["atr"] = P.atr; Q["a60"] = P[f"a60_{p}"]; Q["msik"] = P[f"m{p}"]
        for ek, huc in (("es1", "hucA"), ("es2", f"h2_{p}")):
            X = sy_es_ortalama(Q, ol, es, huc, ad)
            X = X[X.es_n >= D["es"]["min_es"]].copy()
            olaylar[f"p{p}_{ek}"] = X
            # eş dağılımı ağırlıkları: hücredeki olay sayısı / hücredeki eş sayısı
            ne = X.groupby(["tarih", huc]).size().rename("n_ol")
            Es = Q.loc[es, ["tarih", huc, "donem", "R_sik", "R_250", "R_60"]].merge(ne, left_on=["tarih", huc], right_index=True, how="inner")
            Es = Es.merge(X.groupby(["tarih", huc]).es_n.first().rename("nes"), left_on=["tarih", huc], right_index=True, how="left")
            Es["w"] = Es["n_ol"] / Es["nes"]
            for dn in [x[0] for x in D["donem"]] + list(D["birlesik"]):
                dl = D["birlesik"].get(dn, [dn])
                Y = X[X.donem.isin(dl)]
                ay = Y.tarih.dt.to_period("M").astype(str).to_numpy()
                bt = _sy_duy_boot(Y[ad].to_numpy(float), Y[["es_" + c for c in ad]].to_numpy(float), ay, D,
                                  zlib.crc32(f"{pazar}|{p}|{ek}|{dn}".encode()) % 100000)
                for j, (c, r, k, u) in enumerate(kol):
                    n = int(len(Y))
                    sat.append({"pazar": pazar, "p": p, "es": ek, "donem": dn, "ref": r, "k": k, "ufuk": u, "n": n,
                                "p_olay": float(Y[c].mean()) if n else np.nan, "p_es": float(Y["es_" + c].mean()) if n else np.nan,
                                "kat": float(bt["kat"][j]), "alt95": float(bt["alt"][j]), "ust95": float(bt["ust"][j]), "p_boot": float(bt["p"][j]),
                                "es_n_medyan": float(Y.es_n.median()) if n else np.nan,
                                "yon": _sy_duy_yon(n, float(bt["alt"][j]), float(bt["ust"][j]))})
                Ed = Es[Es.donem.isin(dl)]
                for olc in ("R_sik", "R_250", "R_60"):
                    qo = [float(np.nanquantile(Y[olc].to_numpy(float), q)) if len(Y) else np.nan for q in qs]
                    qe = _sy_wq(Ed[olc].to_numpy(float), Ed.w.to_numpy(float), qs)
                    dag.append({"pazar": pazar, "p": p, "es": ek, "donem": dn, "olcu": olc, "n_olay": int(len(Y)), "n_es_satir": int(len(Ed)),
                                "olay_q25": qo[0], "olay_medyan": qo[1], "olay_q75": qo[2], "es_q25": qe[0], "es_medyan": qe[1], "es_q75": qe[2]})
        del Q
    return pd.DataFrame(sat), pd.DataFrame(dag), olaylar


def sy_duy_c174_denetim(T: pd.DataFrame, c174: Dict[str, Any]) -> List[Dict[str, Any]]:
    """p=10, eş1: Ç174 B1 / B0 / B1_5 hücreleri ile n, olay oranı, eş oranı, KAT aynı olmalı (1e-9); değilse SYHata."""
    A = pd.DataFrame(c174["A"]); A = A[A.sikisma == "S1"]
    es = {"B1": ("ATR250", 3.0, "20"), "B0": ("ATR_sik", 3.0, "20"), "B1_5": ("ATR250", 3.0, "5")}
    out = []
    for r in A[A.olcu.isin(list(es))].itertuples():
        if r.pazar not in set(T.pazar):
            continue
        ref, k, u = es[r.olcu]
        x = T[(T.pazar == r.pazar) & (T.p == 10) & (T.es == "es1") & (T.donem == r.donem) & (T.ref == ref) & (T.k == k) & (T.ufuk == u)]
        if len(x) != 1:
            raise SYHata(f"Ç174 tutarlılık: {r.pazar} {r.donem} {r.olcu} satırı yok")
        x = x.iloc[0]
        ciftler = [(float(x.n), float(r.n)), (x.p_olay, r.p_olay), (x.p_es, r.p_es), (x.kat, r.kat)]
        fark = 0.0
        for a_, b_ in ciftler:
            a_, b_ = float(a_), float(b_)
            if np.isnan(a_) and np.isnan(b_):
                continue
            fark = max(fark, abs(a_ - b_) if np.isfinite(a_) and np.isfinite(b_) else np.inf)
        out.append({"pazar": r.pazar, "donem": r.donem, "olcu": r.olcu, "n": int(x.n), "kat_duy": float(x.kat), "kat_c174": float(r.kat), "fark": float(fark)})
        if not fark < 1e-9:
            raise SYHata(f"Ç174 tutarlılık TUTMADI: {r.pazar} {r.donem} {r.olcu} fark {fark}")
    return out


def sy_duy_bh(T: pd.DataFrame, D: Optional[Dict[str, Any]] = None) -> pd.Series:
    """Önceden yazılı aile (ATR250 / ATR60, üç ayrı dönem) içinde BH q; aile dışı satır NaN. Döner bool (aile içinde 'reddedildi')."""
    D = D or SY_DUY
    aile = T.ref.isin(["ATR250", "ATR60"]) & T.donem.isin([x[0] for x in D["donem"]]) & np.isfinite(T.p_boot)
    pv = T.loc[aile, "p_boot"].to_numpy(float); m = len(pv)
    out = pd.Series(np.nan, index=T.index, dtype=object)
    if not m:
        return out
    o = np.argsort(pv); esik = D["bh"]["q"] * np.arange(1, m + 1) / m
    ok = pv[o] <= esik
    kmax = np.max(np.where(ok)[0]) + 1 if ok.any() else 0
    red = np.zeros(m, bool); red[o[:kmax]] = True
    out.loc[aile] = red
    return out


# ---------- görsel örnek (kör; deterministik)
def sy_duy_ornek_sec(P: pd.DataFrame, X: pd.DataFrame, D: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """X = ABD p=10 eş1 olay satırları (Ç174 S1 olay kümesi). 20 olay + aynı gün aynı hücreden 20 eş, karışık numara. Sonuç (t sonrası) kullanılmaz."""
    D = D or SY_DUY; Gc = D["grafik"]
    X = X[X.donem.isin(Gc["donem"])].sort_values(["tarih", "sembol"]).reset_index(drop=True)
    rng = np.random.default_rng(Gc["tohum"])
    sec = np.sort(rng.choice(len(X), Gc["n_olay"], replace=False))
    es_m = P.g10 & ~P.s10
    havuz = P.loc[es_m, ["tarih", "hucA", "sembol"]].sort_values(["tarih", "hucA", "sembol"])
    kayit = []
    for i in sec:
        r = X.iloc[i]
        aday = havuz[(havuz.tarih == r.tarih) & (havuz.hucA == r.hucA)]
        if len(aday) < D["es"]["min_es"]:
            raise SYHata(f"örnek: {r.tarih.date()} hücresinde eş yok")
        e = aday.iloc[int(rng.integers(len(aday)))]
        kayit.append({"tip": "olay", "sembol": r.sembol, "tarih": str(r.tarih.date())})
        kayit.append({"tip": "eş", "sembol": e.sembol, "tarih": str(e.tarih.date())})
    sira = rng.permutation(len(kayit))
    return [dict(kayit[j], numara=int(n + 1)) for n, j in enumerate(sira)]


def sy_duy_grafik_veri(d: pd.DataFrame, tarih: str, D: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Grafik penceresi: t-120..t+20 bar; fiyat / C_t x 100; günlük TR/C_önceki (%); ATR250(t) (%)."""
    D = D or SY_DUY; Gc = D["grafik"]
    i = int(d.index.get_indexer([pd.Timestamp(tarih)])[0])
    if i < 0:
        raise SYHata(f"grafik: {tarih} seride yok")
    a, b = i - Gc["once"], i + Gc["sonra"]
    if a < 1 or b >= len(d):
        raise SYHata(f"grafik: {tarih} için {Gc['once']} / {Gc['sonra']} bar yok")
    H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close"))
    Cp = np.r_[np.nan, C[:-1]]; trc = (np.fmax(H, Cp) - np.fmin(L, Cp)) / Cp
    atr = float(np.mean(trc[i - SY_ESIK["B"]["atr_gun"] + 1:i + 1]))
    W = d.iloc[a:b + 1]; c0 = C[i]
    return {"o": W.Open.to_numpy(float) / c0 * 100, "h": W.High.to_numpy(float) / c0 * 100, "l": W.Low.to_numpy(float) / c0 * 100,
            "c": W.Close.to_numpy(float) / c0 * 100, "trc": trc[a:b + 1] * 100, "atr250": atr * 100, "x": np.arange(a, b + 1) - i}


def sy_duy_ciz(G: Dict[str, Any], numara: int, D: Optional[Dict[str, Any]] = None) -> Any:
    """Kör grafik: ln fiyat ekseni, ortak ölçek (ln(1,10) = px_ln110 piksel; panel sınırı aşılırsa küçültülür ve yazılır), son 10 gün gölgeli,
    alt panelde günlük TR/C (%) ve 2 x / 3 x ATR250(t) çizgileri. Ad / tarih / olay-eş etiketi yok."""
    D = D or SY_DUY; Gc = D["grafik"]
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection, PolyCollection
    x = G["x"]; lo, lh, ll, lc = (np.log(G[k]) for k in ("o", "h", "l", "c"))
    olcek = Gc["px_ln110"] / math.log(1.10); alt_, ust_ = float(np.min(ll)), float(np.max(lh)); R = (ust_ - alt_) * 1.08
    Pp = R * olcek; kucuk = 1.0
    if Pp < Gc["fiyat_min_px"]:
        Pp = Gc["fiyat_min_px"]
    elif Pp > Gc["fiyat_max_px"]:
        kucuk = Gc["fiyat_max_px"] / Pp; Pp = Gc["fiyat_max_px"]; olcek *= kucuk
    span = Pp / olcek; orta = (alt_ + ust_) / 2
    ustk, ara, altk, sol, sag = 40, 30, 40, 70, 90
    Wp = Gc["genislik"]; Hp = int(ustk + Pp + ara + Gc["alt_px"] + altk); dpi = Gc["dpi"]
    with matplotlib.rc_context({"axes.unicode_minus": False, "font.size": 9, "svg.hashsalt": "sy", "path.simplify": False}):
        fig = plt.figure(figsize=(Wp / dpi, Hp / dpi), dpi=dpi)
        en = Wp - sol - sag
        ax = fig.add_axes([sol / Wp, (altk + Gc["alt_px"] + ara) / Hp, en / Wp, Pp / Hp])
        axb = fig.add_axes([sol / Wp, altk / Hp, en / Wp, Gc["alt_px"] / Hp], sharex=ax)
        yuk = G["c"] >= G["o"]; renk = np.where(yuk, "#2e7d32", "#c62828")
        ax.add_collection(LineCollection([[(xi, a), (xi, b)] for xi, a, b in zip(x, ll, lh)], colors=list(renk), linewidths=0.8))
        a_ = np.minimum(lo, lc); u_ = np.maximum(np.maximum(lo, lc), a_ + 1.0 / olcek)
        ax.add_collection(PolyCollection([[(xi - .35, a), (xi + .35, a), (xi + .35, b), (xi - .35, b)] for xi, a, b in zip(x, a_, u_)],
                                         facecolors=list(renk), edgecolors=list(renk), linewidths=0.3))
        for a_x in (ax, axb):
            a_x.axvspan(-9.5, 0.5, color="#9e9e9e", alpha=0.22, linewidth=0)
            a_x.axvline(0.5, color="#424242", linestyle="--", linewidth=0.8)
        ax.set_ylim(orta - span / 2, orta + span / 2); ax.set_xlim(x[0] - 1, x[-1] + 1)
        tik = [v for v in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 175, 200, 250, 300, 400, 500)
               if orta - span / 2 <= math.log(v) <= orta + span / 2]
        ax.set_yticks([math.log(v) for v in tik], labels=[str(v) for v in tik])
        ax.grid(axis="y", color="#e0e0e0", linewidth=0.6); ax.set_axisbelow(True); ax.tick_params(axis="x", labelbottom=False)
        y0 = orta - span / 2 + 0.06 * span
        ax.plot([x[-1] + 0.6] * 2, [y0, y0 + math.log(1.10)], color="#1565c0", linewidth=2, clip_on=False)
        ax.text(x[-1] + 1.4, y0 + math.log(1.10) / 2, "%10", color="#1565c0", va="center", fontsize=8, clip_on=False)
        ax.set_title(f"Grafik {numara:02d}" + (f"   (ölçek x{kucuk:.2f})" if kucuk < 1 else ""), loc="left", fontsize=11)
        axb.bar(x, G["trc"], width=0.7, color="#78909c", linewidth=0)
        for kk, rn in zip(Gc["esik"], ("#ef6c00", "#b71c1c")):
            axb.axhline(kk * G["atr250"], color=rn, linewidth=1.0)
            axb.text(x[-1] + 1.4, kk * G["atr250"], f"{kk:g}x ATR250", color=rn, va="center", fontsize=8, clip_on=False)
        axb.set_ylim(0, max(float(np.nanmax(G["trc"])), 3.2 * G["atr250"]) * 1.08)
        axb.set_ylabel("gün aralığı %"); axb.grid(axis="y", color="#eeeeee", linewidth=0.5)
        xt = [-120, -100, -80, -60, -40, -20, -9, 0, 10, 20]
        axb.set_xticks(xt, labels=[str(t) for t in xt])
    return fig


def sy_duy_grafikler(V: Dict[str, pd.DataFrame], sec: List[Dict[str, Any]], pdf_yol: str, png_kl: Optional[str] = None,
                     D: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """40 PNG + tek PDF (deterministik: üst veri tarih / yazılım yok). Döner sha'lar."""
    D = D or SY_DUY
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    png_kl = png_kl or SY_DUY_GRAFIK_KL; os.makedirs(png_kl, exist_ok=True); os.makedirs(os.path.dirname(pdf_yol), exist_ok=True)
    pngs = {}
    with PdfPages(pdf_yol, metadata={"Creator": None, "Producer": None, "CreationDate": None}) as pdf:
        for r in sorted(sec, key=lambda z: z["numara"]):
            G = sy_duy_grafik_veri(V[r["sembol"]], r["tarih"], D)
            fig = sy_duy_ciz(G, r["numara"], D)
            yol = os.path.join(png_kl, f"grafik_{r['numara']:02d}.png")
            fig.savefig(yol, dpi=D["grafik"]["dpi"], metadata={"Software": None})
            pdf.savefig(fig)
            plt.close(fig)
            pngs[os.path.basename(yol)] = _sy_sha_dosya(yol)
    return {"pdf": os.path.basename(pdf_yol), "pdf_sha256": _sy_sha_dosya(pdf_yol), "pdf_bayt": int(os.path.getsize(pdf_yol)), "png_sha256": pngs}


# ---------- ön kayıt / koşu / rapor
def sy_duy_onkayit_metni(sayim: Dict[str, Any], D: Optional[Dict[str, Any]] = None) -> str:
    D = D or SY_DUY
    s = ["# SIKISMA_YENIDEN — DUYARLILIK ÖN KAYDI\n", f"{D['surum']}\n",
         f"- MÜHÜR (SY_DUY sha256): `{sy_duy_sha(D)}`",
         f"- KOD (SIKISMA_YENIDEN.py sha256): `{_sy_sha_dosya(SY_YOL['kod'])}`",
         f"- ZAMAN (UTC): `{_sy_simdi()}`",
         f"- Taban tanımlar Ç174 SY_ESIK (mühür `{D['c174_muhur']}`); bu çalışma BİLGİDİR, Ç174 kararı değişmez.",
         "- Bu dosya ölçümden ÖNCE commit + push edilir; `python SIKISMA_YENIDEN.py duyarlilik` kontrol kapısı + mühür + kod sha + git kapısı geçmezse durur.", "",
         "## Soru (Cemal'in itirazı, 14 Kas 2026)",
         "\"Gözüm küçük mumlardan sonra gelen mumları neden büyük görsün ki?\" Hangi büyük mum ölçeğinde (k x REF) ve hangi sıkışma uzunluğunda (p) "
         "sıkışma sonrası gün aralığı eşlerden büyük çıkıyor (çıkıyorsa)? Ayrıca 'göz ne görür': ilk 20 günün en büyük mumu sıkışma mumunun kaç katı.", "",
         "## Tanımlar (SY_DUY)", "",
         f"- Büyük mum: {D['buyuk_tanim']}; k ∈ {D['k']}; ufuk {D['ufuk']}.",
         *[f"- REF {k}: {v}" for k, v in D["ref"].items()],
         f"- Sıkışma (p ∈ {D['pencere']}): {D['sikisma']['tanim']}; bant {D['sikisma']['bant']}; başlangıç {D['sikisma']['bas']}.",
         f"- Geçerli satır: {D['gecerli']}.",
         f"- Eş 1: {D['es']['es1']}.", f"- Eş 2: {D['es']['es2']}.", f"- En az {D['es']['min_es']} eş; {D['es']['olay_secimi']}.",
         f"- Ölçü: {D['olcu']}; bootstrap {D['bootstrap']['n']} tekrar, küme {D['bootstrap']['kume']}; {D['bootstrap']['p']}.",
         f"- Dönemler: {D['donem']} + birleşik {D['birlesik']}. Ana okuma: {D['ana']}.",
         f"- Çoklu karşılaştırma: BH q {D['bh']['q']}; aile: {D['bh']['aile']}. {D['bh']['not']}.",
         f"- Yön etiketi: {D['yon']}.",
         *[f"- Dağılım {k}: {v}" for k, v in D["dagilim_olcu"].items() if k != "yuzdelik"],
         f"- Ç174 tutarlılık (durdurucu): {D['tutarlilik_c174']}.",
         f"- Görsel örnek: {D['grafik']['kume']}, {D['grafik']['pazar']} {D['grafik']['donem']}; {D['grafik']['n_olay']} olay + {D['grafik']['n_es']} eş, tohum {D['grafik']['tohum']}; "
         f"{D['grafik']['es_secimi']}; {D['grafik']['sira']}; {D['grafik']['once']} bar önce + {D['grafik']['sonra']} bar sonra; ln(1,10) = {D['grafik']['px_ln110']} piksel; "
         f"{D['grafik']['golge']}; alt panel {D['grafik']['alt_panel']}.",
         f"- Bağımsız yeniden üretilecek hücreler (önceden): {json.dumps(D['denetim_hucre'], ensure_ascii=False)}.", "",
         "## Eşik sözlüğü (SY_DUY, kararlı JSON)", "", "```json", json.dumps(D, sort_keys=True, ensure_ascii=False, indent=1, default=str), "```", "",
         "## Olay SAYIMI (sonuç hesaplanmadan; en az 3 eşi olan olay)", "",
         "| Pazar | p | olay (geçerli, tümü) | eş1 2016-22 | eş1 2023 | eş1 2024-26 | eş2 2016-22 | eş2 2023 | eş2 2024-26 |", "|---|---|---|---|---|---|---|---|---|"]
    for pz, c in sayim.items():
        for pk, r in c.items():
            s.append(f"| {pz} | {pk[1:]} | {r['olay_tum']} | " + " | ".join(str(r[f'{e} {d}']) for e in ("es1", "es2") for d in ("2016-22", "2023", "2024-26")) + " |")
    s += ["", "## Sınırlar (önceden)", "- Evren bugünün listesi (batanlar yok). Bilanço takvimi yok. Uzun pencerede (p=40, 60) olaylar aynı uzun sıkışmanın ardışık günleri olabilir "
          "(20 bar ara; ay kümeli bootstrap bunu kısmen taşır).",
          "- Sıkışma koşulu p günlük ORTALAMAYI tek gün dağılımının %20 yüzdeliğiyle kıyaslar: uzun p'de pencerenin yalnız bir kısmı dar olsa da koşul doğru olabilir "
          "(sentetik testte 60 günlük dar bölgede p=60 koşulu dar bölgenin ~15. gününde doğru oldu); yani p = 'en az p gün dar' değil, 'son p günün ortalaması dar'dır.",
          "- Ç174 tutarlılık farkı ~1e-11 olabilir: sikisma_sonuc.json pandas to_json 10 basamak yazar; eşik 1e-9.", "- ATR_sik REF göreli ve tanımsaldır (sıkışma tanımı onu küçük yapar); yalnız 'göz' kıyası, yorum dışı.",
          "- 5 k x 3 REF x 2 ufuk x 4 p x 2 eş x 3 pazar x 4 dönem = 2.880 satır: tek hücre bulgu değildir.", "", sy_duy_kontrol_tablosu(), ""]
    return "\n".join(s)


def sy_duy_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = SY_DUY_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def sy_duy_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False, pazarlar: Tuple[str, ...] = SY_PAZAR) -> str:
    yol = _sy_duy_yol("onkayit", cikti)
    if os.path.exists(yol):
        if not uzerine:
            raise SYHata(f"duyarlılık ön kaydı zaten var ({yol}); üzerine yazılmaz")
        try:
            _sy_git_islenmis(yol)
            raise SYHata(f"duyarlılık ön kaydı git'e işlenmiş ({yol}); üzerine yazılmaz")
        except SYHata as ex:
            if "işlenmemiş" not in str(ex):
                raise
    sayim = {}
    for p in pazarlar:
        V = sy_veri_yukle(p, SY_ESIK, veri)
        P = sy_duy_panel(V, p, SY_DUY, sonuc=False)
        sayim[p] = sy_duy_sayim(P)
        sylog.info("%s duyarlılık sayım: %s", p, {k: v["olay_tum"] for k, v in sayim[p].items()})
        del P, V
    metin = sy_duy_onkayit_metni(sayim)
    if _SY_EPOSTA.search(metin):
        raise SYHata("duyarlılık ön kaydında e-posta biçimli parça var")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def sy_duy_onkayit_dogrula(yol: Optional[str] = None, git: bool = True, kod_sha: bool = True) -> Dict[str, Any]:
    yol = yol or _sy_duy_yol("onkayit")
    if not os.path.exists(yol):
        raise SYHata(f"duyarlılık ön kaydı yok ({yol}): önce `python SIKISMA_YENIDEN.py duyarlilik --asama onkayit`")
    metin = open(yol, encoding="utf-8").read(); oc = {}
    for ad, desen in (("muhur", r"MÜHÜR \(SY_DUY sha256\): `([0-9a-f]{64})`"), ("kod", _SY_OC_DESEN["kod"]), ("zaman", _SY_OC_DESEN["zaman"])):
        m = re.search(desen, metin)
        if not m:
            raise SYHata(f"duyarlılık ön kaydı bozuk: '{ad}' yok")
        oc[ad] = m.group(1)
    if oc["muhur"] != sy_duy_sha():
        raise SYHata("duyarlılık mührü tutmuyor: SY_DUY ön kayıttan sonra değişmiş, koşu durdu")
    if kod_sha and oc["kod"] != _sy_sha_dosya(SY_YOL["kod"]):
        raise SYHata("kod sha256 duyarlılık ön kaydındakinden farklı (SAPMA), koşu durdu")
    out = {"yol": yol, **oc}
    if git:
        out["git"] = _sy_git_islenmis(yol)
    return out


def sy_duy_kos(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True, pazarlar: Tuple[str, ...] = SY_PAZAR,
               satir: Optional[str] = None, c174: Optional[str] = None, png_kl: Optional[str] = None) -> Dict[str, Any]:
    D = SY_DUY; t0 = time.time()
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    yol = _sy_duy_yol("onkayit", cikti)
    if kontrol:
        import IZ_KARNE as IK
        IK.ik_kontrol_kapisi(yol)
    oc = sy_duy_onkayit_dogrula(yol, git=git)
    kos_zaman = _sy_simdi()
    c174_yol = c174 or _sy_yol("sonuc")
    if not os.path.exists(c174_yol):
        raise SYHata(f"Ç174 sonuç dosyası yok ({c174_yol}); tutarlılık denetimi yapılamaz")
    C174 = json.load(open(c174_yol, encoding="utf-8"))
    if C174.get("muhur") != D["c174_muhur"] and git:
        raise SYHata("Ç174 sonuç dosyasının mührü SY_DUY'daki ile aynı değil")
    satir = satir or SY_YOL["satir"]; os.makedirs(satir, exist_ok=True)
    T_, Dg_, ornek, gr = [], [], None, None
    for pz in pazarlar:
        V = sy_veri_yukle(pz, SY_ESIK, veri)
        P = sy_duy_panel(V, pz, D, sonuc=True)
        T, Dg, X = sy_duy_olc(P, D)
        T_.append(T); Dg_.append(Dg)
        for anah, Xk in X.items():
            Xk.to_csv(os.path.join(satir, f"duy_olay_{pz}_{anah}.csv.gz"), index=False)
        for h in D["denetim_hucre"]:
            if h["pazar"] == pz:   # bağımsız yeniden üretim için o p'nin geçerli satırları (ham; sonuç sütunlarıyla)
                p = h["p"]
                P.loc[P[f"g{p}"], ["sembol", "tarih", "donem", "hucA", f"h2_{p}", f"s{p}", f"e{p}", "atr", f"a60_{p}", f"m{p}", "mx20", "mx5"]] \
                    .to_pickle(os.path.join(satir, f"duy_panel_{pz}_p{p}.pkl"))
        if pz == D["grafik"]["pazar"]:
            ornek = sy_duy_ornek_sec(P, X["p10_es1"], D)
            gr = sy_duy_grafikler(V, ornek, _sy_duy_yol("pdf", cikti), png_kl, D)
            with open(_sy_duy_yol("anahtar", cikti), "w", encoding="utf-8") as f:
                json.dump({"surum": D["surum"], "muhur": sy_duy_sha(), "tohum": D["grafik"]["tohum"], "kume": D["grafik"]["kume"],
                           "grafik": sorted(ornek, key=lambda z: z["numara"]), "dosya": gr}, f, ensure_ascii=False, indent=1)
        sylog.info("%s duyarlılık bitti (%.0f sn)", pz, time.time() - t0)
        del P, V
    T = pd.concat(T_, ignore_index=True); Dg = pd.concat(Dg_, ignore_index=True)
    T["bh_red"] = sy_duy_bh(T, D)
    tut = sy_duy_c174_denetim(T, C174)
    sonuc = {"surum": D["surum"], "onkayit": oc, "kos_zaman_utc": kos_zaman, "sure_sn": round(time.time() - t0, 1), "muhur": sy_duy_sha(),
             "pazarlar": list(pazarlar), "c174_tutarlilik": tut, "grafik": gr,
             "kat": json.loads(T.to_json(orient="records", force_ascii=False)), "dagilim": json.loads(Dg.to_json(orient="records", force_ascii=False))}
    with open(_sy_duy_yol("sonuc", cikti), "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1, default=str)
    return {"sonuc": sonuc, "rapor": sy_duy_rapor(cikti)}


def _sy_kat_hucre(x: Optional[pd.Series]) -> str:
    if x is None:
        return "—"
    y = {"KAT>1": " ▲", "KAT<1": " ▼"}.get(x.yon, "")
    return f"{_sy(x.kat)} ({_sy(x.alt95)}-{_sy(x.ust95)}){y}"


def sy_duy_rapor(cikti: Optional[str] = None) -> str:
    yol = _sy_duy_yol("sonuc", cikti)
    if not os.path.exists(yol):
        raise SYHata(f"duyarlılık sonucu yok: {yol}")
    S = json.load(open(yol, encoding="utf-8")); D = SY_DUY
    T = pd.DataFrame(S["kat"]); Dg = pd.DataFrame(S["dagilim"]); ks = D["k"]

    def sat(pz, p, es, dn, ref, k, u):
        x = T[(T.pazar == pz) & (T.p == p) & (T.es == es) & (T.donem == dn) & (T.ref == ref) & (T.k == k) & (T.ufuk == u)]
        return x.iloc[0] if len(x) else None

    ana = ["ABD", "AVR"]
    s = ["# SIKISMA_YENIDEN — DUYARLILIK RAPORU (büyük mum ölçeği x sıkışma uzunluğu)\n",
         f"{S['surum']}. Mühür `{S['muhur'][:12]}`, ön kayıt commit `{S['onkayit'].get('git', {}).get('commit', '')[:10]}` "
         f"({S['onkayit'].get('git', {}).get('commit_zamani', '')}); koşu {S['kos_zaman_utc']} ({S['sure_sn']} sn). BİLGİ çalışması: Ç174 kararı değişmez.\n",
         "## DÜZ DİL ÖZET", ""]
    # 1) hangi eşikte KAT > 1 / < 1 (ana: ABD, AVR 2023+, REF ATR250 / ATR60)
    for es, ead in (("es1", "eş 1 (Ç174 eşi)"), ("es2", "eş 2 (anlık/250 gün oynaklık oranı eşli)")):
        for pz in ana:
            X = T[(T.pazar == pz) & (T.es == es) & (T.donem == "2023+") & T.ref.isin(["ATR250", "ATR60"])]
            ust = X[X.yon == "KAT>1"]; alt = X[X.yon == "KAT<1"]
            ornek_u = "; ".join(f"p{r.p} {r.ref} k{_sy(r.k, 1)} {r.ufuk}g {_sy(r.kat)}" for r in ust.sort_values("kat", ascending=False).head(4).itertuples())
            s.append(f"- **{pz} 2023-26/08, {ead}**: {len(X)} kombinasyonun (p x REF ATR250/ATR60 x k x ufuk) {len(ust)} tanesinde KAT güvenle > 1, "
                     f"{len(alt)} tanesinde güvenle < 1, {len(X) - len(ust) - len(alt)} belirsiz / ölçülemedi." + (f" En yüksek KAT>1: {ornek_u}." if len(ust) else ""))
    for pz in ana:
        hc = []
        for p in D["pencere"]:
            a = sat(pz, p, "es1", "2023+", "ATR250", 3.0, "20"); b = sat(pz, p, "es1", "2023+", "ATR60", 2.0, "20"); c = sat(pz, p, "es2", "2023+", "ATR250", 3.0, "20")
            hc.append(f"p{p}: 3xATR250 {_sy(a.kat) if a is not None else '—'}, 2xATR60 {_sy(b.kat) if b is not None else '—'}, eş2 3xATR250 {_sy(c.kat) if c is not None else '—'}")
        s.append(f"- {pz} 2023+ uzunluğa göre KAT: " + "; ".join(hc) + ".")
    # 2) göz ne görür
    for pz in ana + ["BIST"]:
        for p in (10, 60):
            r = Dg[(Dg.pazar == pz) & (Dg.p == p) & (Dg.es == "es1") & (Dg.donem == "2023+")]
            g = {o: r[r.olcu == o].iloc[0] for o in ("R_sik", "R_250", "R_60") if len(r[r.olcu == o])}
            if len(g) == 3:
                s.append(f"- **Göz ne görür ({pz}, p={p}, 2023+)**: sıkışma sonrası ilk 20 günün en büyük mumu, sıkışma mumunun medyan {_sy(g['R_sik'].olay_medyan)} katı "
                         f"(%25-75: {_sy(g['R_sik'].olay_q25)}-{_sy(g['R_sik'].olay_q75)}); eşlerde kendi son {p} gün mumunun {_sy(g['R_sik'].es_medyan)} katı. "
                         f"ATR250'nin olayda {_sy(g['R_250'].olay_medyan)} katı, eşte {_sy(g['R_250'].es_medyan)} katı; ATR60'ın olayda {_sy(g['R_60'].olay_medyan)}, eşte {_sy(g['R_60'].es_medyan)} katı.")
    bh = T[T.bh_red == True]  # noqa: E712
    s += [f"- Çoklu karşılaştırma (BİLGİ): 1.440 sınamalık ailede BH q 0,10 ile {len(bh)} hücre seçildi; bunların {int((bh.kat > 1).sum())} tanesi KAT > 1, "
          f"{int((bh.kat < 1).sum())} tanesi KAT < 1. Hiçbir hücre tek başına bulgu değildir; karar Ç174'tedir.",
          "- ATR_sik (göreli) REF sıkışmanın kendi küçük mumuna göredir: tanım gereği KAT > 1 çıkar; yalnız 'göz' kıyasıdır.", "",
          "## Ç174 tutarlılık (p=10, eş1; durdurucu denetim)", "",
          "| Pazar | Dönem | Ölçü | n | KAT (duyarlılık) | KAT (Ç174) | en büyük fark |", "|---|---|---|---|---|---|---|"]
    for r in S["c174_tutarlilik"]:
        s.append(f"| {r['pazar']} | {r['donem']} | {r['olcu']} | {r['n']} | {_sy(r['kat_duy'], 4)} | {_sy(r['kat_c174'], 4)} | {r['fark']:.1e} |")
    # ana tablolar
    for pz in ana + ["BIST"]:
        for es in ("es1", "es2"):
            for dn in ("2023+",):
                s += ["", f"## KAT tablosu — {pz} {dn} — {'eş 1 (Ç174)' if es == 'es1' else 'eş 2 (oynaklık oranı)'} " + ("(BİLGİ)" if pz == "BIST" else "(ana okuma)"), "",
                      "KAT (alt95-üst95); ▲ güvenle > 1, ▼ güvenle < 1. n = olay sayısı.", "",
                      "| p | REF | ufuk | n | " + " | ".join(f"k={_sy(k, 1)}" for k in ks) + " |", "|---|---|---|---|" + "---|" * len(ks)]
                for p in D["pencere"]:
                    for ref in _SY_DUY_REF:
                        for u in D["ufuk"]:
                            xs = [sat(pz, p, es, dn, ref, k, u) for k in ks]
                            n = int(xs[0].n) if xs[0] is not None else 0
                            s.append(f"| {p} | {ref} | {u} | {n} | " + " | ".join(_sy_kat_hucre(x) for x in xs) + " |")
    s += ["", "## Dönemlere göre (k = 2 ve 3; REF ATR250 / ATR60; ufuk 20; iki eş kümesi; bütün pazarlar)", "",
          "| Pazar | Dönem | p | eş | n | 2xATR250 | 3xATR250 | 2xATR60 | 3xATR60 |", "|---|---|---|---|---|---|---|---|---|"]
    for pz in ana + ["BIST"]:
        for dn in [x[0] for x in D["donem"]] + ["2023+"]:
            for p in D["pencere"]:
                for es in ("es1", "es2"):
                    xs = [sat(pz, p, es, dn, r, k, "20") for r, k in (("ATR250", 2.0), ("ATR250", 3.0), ("ATR60", 2.0), ("ATR60", 3.0))]
                    n = int(xs[0].n) if xs[0] is not None else 0
                    s.append(f"| {pz} | {dn} | {p} | {es} | {n} | " + " | ".join(_sy_kat_hucre(x) for x in xs) + " |")
    s += ["", "## 'Göz ne görür' dağılımları (ilk 20 günün en büyük mumu; medyan ve %25-75; eş ağırlıklı)", "",
          "| Pazar | Dönem | p | eş | n olay | ölçü | olay medyan | olay %25-75 | eş medyan | eş %25-75 |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in Dg.sort_values(["pazar", "donem", "p", "es", "olcu"]).itertuples():
        s.append(f"| {r.pazar} | {r.donem} | {r.p} | {r.es} | {r.n_olay} | {r.olcu} | {_sy(r.olay_medyan)} | {_sy(r.olay_q25)}-{_sy(r.olay_q75)} | "
                 f"{_sy(r.es_medyan)} | {_sy(r.es_q25)}-{_sy(r.es_q75)} |")
    g = S.get("grafik") or {}
    s += ["", "## Görsel örnek (kör)", "",
          f"- {D['grafik']['kume']}, {D['grafik']['pazar']} {', '.join(D['grafik']['donem'])}: rastgele {D['grafik']['n_olay']} olay + aynı gün aynı hücreden {D['grafik']['n_es']} eş (tohum {D['grafik']['tohum']}), "
          f"numaralar karışık; anahtar `{SY_DUY_DOSYA['anahtar']}`. PDF `{SY_DUY_DOSYA['pdf']}` ({g.get('pdf_bayt', '—')} bayt, sha256 `{str(g.get('pdf_sha256', ''))[:16]}`).",
          f"- Her grafik: {D['grafik']['once']} bar önce + {D['grafik']['sonra']} bar sonra; ln ekseni, ln(1,10) = {D['grafik']['px_ln110']} piksel (aşan grafikte ölçek küçültülür ve başlıkta yazılır); "
          "son 10 gün gölgeli; alt panelde günlük aralık % ve 2x / 3x ATR250(t) çizgileri.", "",
          "## Sınırlar", "- Evren bugünün listesi (batanlar yok); bilanço takvimi yok.",
          "- p = 40 / 60'ta olaylar aynı uzun sıkışmanın 20 bar arayla ardışık günleri olabilir; ay kümeli bootstrap bunu kısmen taşır.",
          "- 2.880 satır: tek hücre bulgu değildir; BH yalnız bilgi.", ""]
    metin = "\n".join(s)
    with open(_sy_duy_yol("rapor", cikti), "w", encoding="utf-8") as f:
        f.write(metin)
    return metin


# ---------------------------------------------------------------- ÇAKIŞMA KAPISI
def _cakisma_kontrol_sy(_once=_CK_ONCE_SY, _dosya="SIKISMA_YENIDEN.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_SY", "_CK_KAYIT", "_cakisma_kontrol_sy", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "subprocess", "zlib", "warnings", "_dt",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_sy()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=SY_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "duyarlilik"])
    ap.add_argument("--asama", choices=["onkayit", "kos", "rapor"], default="kos", help="duyarlilik: onkayit | kos | rapor")
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true", help="onkayit: git'e İŞLENMEMİŞ ön kaydı yeniden yaz")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(sy_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "duyarlilik":
            if a.asama == "onkayit":
                print(sy_duy_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
            elif a.asama == "kos":
                R_ = sy_duy_kos(a.cikti, a.veri)
                print(R_["rapor"].split("## Ç174")[0])
            else:
                print(sy_duy_rapor(a.cikti))
        elif a.komut == "kos":
            R_ = sy_kos(a.cikti, a.veri)
            print(json.dumps(R_["sonuc"]["karar"], ensure_ascii=False, indent=1))
        else:
            print(sy_rapor(a.cikti))
    except SYHata as ex:
        sylog.error("%s", ex); sys.exit(1)
