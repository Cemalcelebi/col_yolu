"""SIKISMA_CEMAL — CEMAL TANIMLI SIKIŞMA (S4): küçük mum + YATAY + DAR BOLLINGER + yeterli uzunluk; ileri ölçüm, tek dosya (15 Kasım 2026).

Kaynak (Cemal, 15 Kas 2026; FENER günlük): kodun S1'i (SIKISMA_YENIDEN, 10 gün) 03-16 Aralık 2025'i seçti: mumlar küçük ama fiyat aşağı kayıyor
(ilk-son gün -%6), Bollinger bandı en geniş yerinde (250 gün yüzdeliği 0,70). Asıl sıkışma 14 Ekim - 7 Kasım 2025 (18 bar, bant %7,3, net +%4,
BB genişliği yüzdeliği 0,02). Ders: sıkışma = küçük mum + YATAY (net kayma küçük) + DAR BOLLINGER (uzun dönem yüzdeliği düşük) + uzunluk.

S4 (SC_ESIK['S4']; ön kayıtta mühürlü): pencere p = 15 işlem günü (t-14..t), duyarlılık p = 20.
  (i)   küçük mum: ort((H-L)/C, pencere) <= önceki 250 günün p günlük ortalama (H-L)/C dağılımının %20 yüzdeliği (dağılım pencereden önce biter)
  (ii)  dar Bollinger: BB(20, 2σ) genişliği 4σ20/SMA20 (t) <= önceki 250 günün (t-250..t-1) %20 yüzdeliği
  (iii) YATAY: |C_t / C_t-(p-1) - 1| <= %3 VE (max C - min C)/min C (pencere) <= %8 BIST / %6 ABD, AVR VE pencerede O < önceki C günleri <= %50
  (iv)  uzunluk: (i) ve (ii) t'de biten en az 10 ardışık günde doğru
  olay: koşulun doğru olduğu ilk gün; aynı hissede yeni olay en az 20 bar sonra. Geçerli bar, likidite alt %20 dışarı, bölünme şüphesi YALNIZ
  geçmiş pencerede ([t-260, t]).
ÖLÇÜM (SIKISMA_YENIDEN sonuç tanımları İÇE ALINIR, değiştirilmez): (A) 20 günde B1 (gün TR/C_önceki >= 3 x ATR250), BH2 (= SY B2: 20 günde
  max |ln(C_t+k/C_t)| >= max(%15, 3σ250√20)), k=2 varyantları (2 x ATR250; max(%15, 2σ√20)), B0 (göreli: 3 x pencere ort TR/C); KAT = olay
  oranı / eş oranı, eş 1 = aynı gün, σ250 ondalığı x likidite üçlüsü (SY hucA), eş 2 = aynı gün, (pencere ort TR/C / ATR250) 20'liği x likidite
  üçlüsü; ikisinde de eş S4 koşulu yanlış; ay kümeli bootstrap (SY.sy_oran_boot). (B) ilk büyük hareketin zamanı (medyan, %25-75), pencere
  oranları, yön payı. (C) ORTAK_CETVEL.oc_olc (60 gün eşli getiri + olasılık tablosu; bilgi) ve SY (C) yönsüz stoplu kırılım işlemi
  (SY.sy_olc_C, S4 olayları ve S4 dışı eşlerle; kural aynen).
Komut:  python SIKISMA_CEMAL.py onkayit | kos | rapor | liste
Colab:  exec(open('SIKISMA_CEMAL.py').read()); sc_kos()   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_*.pkl (SY.sy_veri_yukle; OC.oc_veri); liste: /tmp/tavan/yahoo (TAVAN_SERISI.ts_fiyatlar, ekran fiyatı). Satır verisi /tmp/sikisma_cemal.
Çıktı:  arastirma_cikti/sikisma_cemal/ SIKISMA_CEMAL_ON_KAYIT.md, sikisma_cemal_sonuc.json, SIKISMA_CEMAL_RAPOR.md, BOLGE_LISTESI_S4.md.
Komisyon / kayma YOK. Evren bugünün listesi (hayatta kalma yanlılığı; yazılır).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_SC = {k: id(v) for k, v in globals().items()}

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

KOK_SC = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_SC not in sys.path:
    sys.path.insert(0, KOK_SC)

import ORTAK_CETVEL as OC  # noqa: E402
import SIKISMA_YENIDEN as SY  # noqa: E402

sclog = logging.getLogger("col.sikisma_cemal")
if not sclog.handlers:
    _sc_h = logging.StreamHandler(sys.stderr)
    _sc_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sikisma_cemal: %(message)s", "%H:%M:%S"))
    sclog.addHandler(_sc_h)
    sclog.setLevel(logging.INFO)
    sclog.propagate = False

SC_SURUM = "SIKISMA_CEMAL v1.0 (2026-11-15): Cemal tanımlı sıkışma S4 (küçük mum + yatay + dar Bollinger + uzunluk) -> büyük hareket; ileri ölçüm"
SC_YOL = {"cikti": os.path.join(KOK_SC, "arastirma_cikti", "sikisma_cemal"), "veri": os.environ.get("SC_VERI", "/tmp/veri"),
          "veri2": os.environ.get("OC_VERI2", "/tmp/veri2"), "satir": os.environ.get("SC_SATIR", "/tmp/sikisma_cemal"),
          "kod": os.path.join(KOK_SC, "SIKISMA_CEMAL.py"), "sy_kod": os.path.join(KOK_SC, "SIKISMA_YENIDEN.py"),
          "yahoo": os.environ.get("SC_YAHOO", "/tmp/tavan/yahoo")}
SC_DOSYA = {"onkayit": "SIKISMA_CEMAL_ON_KAYIT.md", "sonuc": "sikisma_cemal_sonuc.json", "rapor": "SIKISMA_CEMAL_RAPOR.md",
            "liste": "BOLGE_LISTESI_S4.md", "denetim": "sikisma_cemal_denetim.json"}
SC_PAZAR = ("BIST", "ABD", "AVR")

# ÖN KAYITTAKİ BÜTÜN SABİTLER (sonuç görüldükten sonra değişmez; mühür sc_esik_sha).
SC_ESIK: Dict[str, Any] = {
    "S4": {"pencere": [15, 20], "ana_pencere": 15, "dagilim": 250, "mum_yuzdelik": 0.20, "bb_gun": 20, "bb_k": 2.0, "bb_ddof": 0, "bb_yuzdelik": 0.20,
           "net": 0.03, "bant": {"BIST": 0.08, "ABD": 0.06, "AVR": 0.06}, "asagi_acilis_pay": 0.50, "uzunluk": 10, "ara": 20,
           "tanim": {"i": "ort((H-L)/C, t-p+1..t) <= m_p(s) değerlerinin %20 yüzdeliği, s = t-p-249..t-p (m_p = p günlük ort (H-L)/C; dağılım pencereden önce biter)",
                     "ii": "BBW_t = 2 x 2 x std20(C, ddof 0) / SMA20(C) <= BBW(t-250..t-1) %20 yüzdeliği",
                     "iii": "|C_t / C_t-(p-1) - 1| <= %3 VE (max C - min C) / min C (t-p+1..t) <= bant (BIST %8, ABD/AVR %6) VE "
                            "pencerede 'aşağı açılış' (O < önceki geçerli barın C'si) günlerinin payı <= %50",
                     "iv": "(i) VE (ii) t'de biten en az 10 ardışık geçerli barda doğru",
                     "olay": "S4 = (i)..(iv) hepsi doğru; olay = koşulun doğru olduğu gün, aynı hissede yeni olay en az 20 bar sonra; bölge = t-p+1..t",
                     "p20": "p = 20 duyarlılık: aynı eşikler (net %3, bant %8/%6, uzunluk 10) — p'ye göre ölçeklenmez"}},
    "gecmis_min": 290,                     # 2p + 250 (p=20) geçerli bar: (i) dağılımı tanımlı
    "bolunme_gecmis": [-260, 0],           # SY.sy_bolunme_supheli ANA; YALNIZ geçmiş pencere (SY'de [-260, +41] idi: bilgi satırı)
    "sy_bolunme_bilgi": [-260, 41],
    "sonuc": {"ana": ["B1", "BH2"], "bilgi": ["B1k2", "BH2k2", "B0"],
              "tanim": {"B1": "SY B1 aynen: t+1..t+20 içinde bir günün TR/C_önceki >= 3 x ATR250% (t-249..t)",
                        "BH2": "SY B2 aynen: max_k |ln(C_t+k / C_t)|, k=1..20 >= max(%15, 3 x σ250 x √20)",
                        "B1k2": "t+1..t+20 içinde bir günün TR/C_önceki >= 2 x ATR250%",
                        "BH2k2": "max_k |ln(C_t+k / C_t)| >= max(%15, 2 x σ250 x √20)",
                        "B0": "t+1..t+20 içinde bir günün TR/C_önceki >= 3 x pencere (t-p+1..t) ort TR/C_önceki (göreli; tanımsal, yalnız bilgi)"},
              "yon": {"B1": "ilk büyük günün kapanıştan kapanışa getirisinin işareti", "BH2": "eşiği ilk aşan günde ln(C_t+k/C_t) işareti"},
              "zaman": "ilk büyük günün t'den uzaklığı k (1..20); pencereler [1,5] [6,10] [11,15] [16,20]"},
    "es": {"es1": "aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü (SY hucA), uygun, S4(p) koşulu yanlış",
           "es2": "aynı gün, aynı pazar, (ort TR/C_önceki t-p+1..t / ATR250) oranının gün içi 20'liği x likidite üçlüsü, uygun, S4(p) koşulu yanlış "
                  "(sıkışmanın kendisinden gelen mekanik düşük oynaklığı dengeler)",
           "oran_kova": 20, "min_es": 3, "olay_secimi": "olay her eş kümesinde ayrı ayrı en az 3 eşle kalır"},
    "uygun": "SY 'uygun' ile aynı (likidite alt %20 dışı, σ250 / ATR250 / likidite tanımlı, 20 gün gelecek barı var, dönem içinde) + en az 290 geçerli bar "
             "+ bölünme şüphesi [t-260, t] içinde yok (yalnız geçmiş)",
    "donem": [["2016-22", "2016-01-01", "2022-12-31"], ["2023", "2023-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-08-31"]],
    "birlesik": {"2023+": ["2023", "2024-26"]},
    "karar_pazar": ["ABD", "AVR"], "karar_donem": ["2023", "2024-26"], "bilgi_pazar": ["BIST"],
    "bootstrap": "SY.sy_oran_boot: 2000 tekrar, ay kümeli (olay ayı), %95, tohum 1414 + crc32(etiket) % 1000",
    "karar": {"n_min": 30, "n_guc": 1000,
              "hucre": "KAT alt95 > 1 hem eş 1 hem eş 2'de ve n >= 30 (iki eş kümesinin küçük n'i) -> GEÇER; n < 30 -> ÖLÇÜLEMEDİ; n >= 1000 ve eş 1 ya "
                       "da eş 2 üst95 < 1 -> TERS; n >= 1000 ve geçmez -> TUTMADI; 30 <= n < 1000 ve geçmez -> ÖLÇÜLEMEDİ (güç)",
              "etiket": "her ana sonuç (B1, BH2) için ayrı, p = 15: dört karar hücresi (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) GEÇER -> "
                        "'CEMAL SIKIŞMASI BÜYÜK HAREKET HABERCİSİ'; en az biri GEÇER -> EMARE; hiçbiri geçmez ve dördü TUTMADI / TERS -> 'HABERCİ DEĞİL' "
                        "(dördü TERS ise '(TERS)'); aksi ÖLÇÜLEMEDİ. p = 20, k = 2, B0, BIST ve 2016-22 bilgi."},
    "C": "SY.sy_olc_C aynen (10 gün bandı %1 taşma kapanışı -> ertesi açılış, stop öteki kenar, 20 bar; eş aynı t momentum beşliği x likidite üçlüsü, "
         "S4 dışı; FI_OLCUT dört şart); yalnız olay = S4 olayı (p 15), eş = S4 koşulu yanlış. BİLGİ.",
    "OC": "ORTAK_CETVEL.oc_olc: S4 (p 15) olayları [sembol, tarih, pazar] (tarih = t; giriş, tekilleştirme, eşler, olasılık tablosu cetvelin); BİLGİ "
          "(yön tahmini yok).",
    "gelecek_denetimi_n": 40, "tohum": 1515,
    "liste": {"bas": "2025-01-01", "son": "2026-08-31", "rastgele_hisse": 7, "ardisik": 3, "en_iyi": 10, "tohum": 27, "pazar": "BIST",
              "fiyat": "ekran fiyatı = Yahoo kapanış x sonraki bölünme çarpanı (TAVAN_SERISI.ts_fiyatlar); tespit Yahoo bölünme düzeltmeli oranlarla"},
    "fener": {"sembol": "FENER", "asil": ["2025-10-14", "2025-11-07"], "yanlis": ["2025-12-03", "2025-12-16"],
              "tanim": "MEKANİK DOĞRULAMA: S4 (p 15) FENER'de karar günü 14.10-07.11.2025 içinde EN AZ BİR S4 günü (s4c) üretmeli; 03-16.12.2025 "
                       "içinde S4 günü üretmemeli. Ekran fiyatıyla (Yahoo) ve V_BIST ile. Tutmazsa eşik OYNANMAZ, düşen koşul raporlanır."},
}

SC_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş 1 = aynı gün/pazar σ250 ondalığı x likidite üçlüsü (SY hucA), S4 dışı; eş 2 = aynı gün (pencere ort TR/C / ATR250) 20'liği x likidite "
                   "üçlüsü, S4 dışı: sıkışmanın ATR250'yi düşürmesinden gelen mekanik üstünlüğü dengeler; aynı B tanımı eşlere; B0 tanımsal (bilgi); "
                   "60 gün getiri ve plasebo yalnız OC.oc_olc; işlem eşleri SY.sy_olc_C (aynı kural)"),
    "K2": ("EVET", "sc_gecmis yalnız t'ye kadar (mum dağılımı pencereden önce, BBW dağılımı t-1'e kadar, likidite t-1'e kadar); bölünme şüphesi yalnız "
                   "[t-260, t]; kos'ta sc_gelecek_denetimi 40 olay/pazar seriyi t'de kesip aynı tespiti mekanik denetler; test kesme + gelecek bozma testi"),
    "K3": ("EVET", "SY.sy_veri_hazirla: H>L ve V>0 olmayan bar atılır (bayat fiyat sayılmaz); 'önceki C' önceki GEÇERLİ bar; günlük veri, kesik 31.08.2026"),
    "K4": ("EVET", "aynı hissede S4 olayı en az 20 bar arayla; n = olay sayısı; OC kendi 60 gün tekilleştirmesi; ay kümeli bootstrap; zaman medyan + %25-75"),
    "K5": ("EVET", "KAT olasılık ölçüsü (t kapanışı karar anı); 60 gün getiri OC: giriş t sonrası ilk geçerli açılış; işlem SY (C): kırılım kapanışı sonrası açılış"),
    "K6": ("EVET", "ölçüm tek kip: fi_k1_veri düzeltilmiş fiyat (V_*); liste ekran fiyatı ayrı (tespit Yahoo bölünme düzeltmeli oranla); mum ve ATR yüzde; "
                   "AVR likidite EUR (Kur); bölünme şüphesi SY.sy_bolunme_supheli"),
    "K7": ("EVET", "evren bugünün listesi (V_*.pkl; OC'de ABD + k34): batanlar yok; raporda yazılı; büyük hareket olasılığı olay ve eşte birlikte etkilenir"),
    "K8": ("EVET", "3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ, 30-999 güç sınırlı ÖLÇÜLEMEDİ (HABERCİ DEĞİL yalnız n >= 1000); iki doğrulama dönemi ayrı; "
                   "ana sonuç 2 (B1, BH2) x 2 eş; k2 / B0 / p20 / BIST bilgi"),
    "K9": ("EVET", "SC_ESIK sha mühür + SIKISMA_CEMAL.py sha + SIKISMA_YENIDEN.py sha + OC üç satır ön kayıtta; olay sayımı getirisiz; commit + push sonra kos; "
                   "kos OC.oc_kapi + kendi git / sha kapısı; FENER tanı kontrolü ön kayıtta yazılı, eşik oynanmadı"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV. Ham veriden 3 bölge (FENER Ekim-Kasım dahil) elle doğrulanır"),
    "K11": ("EVET", "2 hücre KAT /tmp/sikisma_cemal satır CSV'sinden bağımsız kodla yeniden üretilir; 3 bölge ham veriden elle"),
    "K12": ("EVET", "'HABERCİ / EMARE' yalnız karar kuralı geçince; büyük hareket olasılığı, 60 gün getiri ve işlem getirisi ayrı tablolarda; komisyon yok yazılır"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_sc; yasak dosyalara dokunulmaz (git diff denetimi); e-posta taraması ön kayıt + testte; ücretli veri yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; yalnız ölçüm (yön tahmini yok, öneri yok)"),
}


class SCHata(RuntimeError):
    """Durdurucu hata (ön kayıt yok / mühür ya da kod sha tutmuyor / git'e işlenmemiş / veri yok / geleceğe bakma denetimi tutmadı)."""


_SC_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _sc_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def sc_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or SC_ESIK, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")).hexdigest()


def _sc_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or SC_YOL["cikti"], SC_DOSYA.get(ad, ad))


def _sc_donem(t: pd.Series, E: Dict[str, Any]) -> np.ndarray:
    out = np.array([""] * len(t), dtype=object)
    for ad, a, b in E["donem"]:
        out[(t >= pd.Timestamp(a)) & (t <= pd.Timestamp(b))] = ad
    return out


def _sc_json(yol: str, J: Any) -> None:
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1, default=lambda x: None if (isinstance(x, float) and not math.isfinite(x)) else str(x))


def _sc_temiz(x: Any) -> Any:
    if isinstance(x, dict):
        return {str(k): _sc_temiz(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_sc_temiz(v) for v in x]
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return float(x) if math.isfinite(float(x)) else None
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (pd.Timestamp, np.datetime64)):
        return str(pd.Timestamp(x).date())
    return x


# ---------------------------------------------------------------- 1) S4 TESPİTİ (yalnız t'ye kadar)
def sc_s4(d: pd.DataFrame, pazar: str, p: int, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """d = SY.sy_veri_hazirla çıktısı (geçerli barlar). Her bar t için S4(p) koşulları ve tanı sütunları; yalnız t'ye kadarki barlar."""
    E = E or SC_ESIK; S = E["S4"]
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    n = len(C); Cp = np.r_[np.nan, C[:-1]]
    mum = pd.Series((H - L) / C)
    m = mum.rolling(p, min_periods=p).mean()
    qm = m.rolling(S["dagilim"], min_periods=S["dagilim"]).quantile(S["mum_yuzdelik"]).shift(p)
    Cs = pd.Series(C)
    bbw = 2 * S["bb_k"] * Cs.rolling(S["bb_gun"], min_periods=S["bb_gun"]).std(ddof=S["bb_ddof"]) / Cs.rolling(S["bb_gun"], min_periods=S["bb_gun"]).mean()
    qb = bbw.rolling(S["dagilim"], min_periods=S["dagilim"]).quantile(S["bb_yuzdelik"]).shift(1)
    bbr = bbw.rolling(S["dagilim"], min_periods=S["dagilim"]).rank(pct=True)          # tanı / liste: t dahil 250 gün yüzdelik sırası
    net = np.r_[np.full(p - 1, np.nan), C[p - 1:] / C[:n - p + 1] - 1] if n >= p else np.full(n, np.nan)
    mx = Cs.rolling(p, min_periods=p).max(); mn = Cs.rolling(p, min_periods=p).min()
    bant = ((mx - mn) / mn).to_numpy()
    asg = pd.Series((O < Cp).astype(float)); asg[0] = np.nan
    asagi = asg.rolling(p, min_periods=p).mean().to_numpy()
    tr = np.fmax(H, Cp) - np.fmin(L, Cp); tr[0] = H[0] - L[0]
    trp = pd.Series(tr / Cp).rolling(p, min_periods=p).mean().to_numpy()
    with np.errstate(invalid="ignore"):
        ci = (m <= qm).to_numpy(); cii = (bbw <= qb).to_numpy()
        ciii = (np.abs(net) <= S["net"]) & (bant <= S["bant"][pazar]) & (asagi <= S["asagi_acilis_pay"])
    run = SY._sy_kosu(ci & cii)
    gm = E["gecmis_min"]; ok_g = np.arange(n) >= gm
    s4c = ci & cii & ciii & (run >= S["uzunluk"]) & ok_g
    return pd.DataFrame({"m": m.to_numpy(), "qm": qm.to_numpy(), "bbw": bbw.to_numpy(), "qb": qb.to_numpy(), "bbr": bbr.to_numpy(), "net": net,
                         "bant4": bant, "asagi": asagi, "trp": trp, "ci": ci, "cii": cii, "ciii": ciii, "run4": run, "s4c": s4c,
                         "ev4": SY._sy_olay(s4c, S["ara"], gm)}, index=d.index)


def sc_gecmis(d: pd.DataFrame, pazar: str, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """SY geçmiş özellikleri (S1, ATR250, σ250, likidite, momentum, 10 gün bandı) + S4 (p 15 ana; p 20 '_20' ekli)."""
    E = E or SC_ESIK
    G = SY.sy_gecmis(d, pazar, SY.SY_ESIK)
    pa = E["S4"]["ana_pencere"]
    for p in E["S4"]["pencere"]:
        X = sc_s4(d, pazar, p, E)
        ek = "" if p == pa else f"_{p}"
        kol = list(X.columns) if p == pa else ["trp", "s4c", "ev4", "run4"]
        for c in kol:
            G[c + ek] = X[c].to_numpy()
        with np.errstate(invalid="ignore", divide="ignore"):
            G["oran" + ek] = X.trp.to_numpy() / G.atr.to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        G["oran_S1"] = G.m10.to_numpy() / G.atr.to_numpy()
    return G


# ---------------------------------------------------------------- 2) SONUÇLAR (t'den sonrası; yalnız kos)
def sc_sonuc(d: pd.DataFrame, G: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """SY.sy_sonuc (B1, B2 = BH2, B0 SY, k1, (C) işlem sütunları) + k=2 varyantları, göreli B0 (S4 penceresi), yön ve zaman."""
    E = E or SC_ESIK; SB = SY.SY_ESIK["B"]; h = SB["ufuk"]
    S = SY.sy_sonuc(d, G, SY.SY_ESIK)
    C = d.Close.to_numpy(float); n = len(C)
    trc = G.trc.to_numpy(); atr = G.atr.to_numpy(); sig = G.sig.to_numpy()
    Tf = SY._sy_ileri(trc, h)
    gel = S.gel.to_numpy()
    lc = np.log(C); Lf = SY._sy_ileri(lc, h) - lc[:, None]
    rf = SY._sy_ileri(np.r_[np.nan, np.diff(lc)], h)      # t+k günü kapanıştan kapanışa ln getiri
    sk = sig * math.sqrt(h)
    out = {}
    with np.errstate(invalid="ignore"):
        out["B1k2"] = (Tf >= 2.0 * atr[:, None]).any(axis=1) & gel
        thr3 = np.fmax(SB["b2_min"], SB["b2_kat"] * sk); thr2 = np.fmax(SB["b2_min"], 2.0 * sk)
        bh = np.abs(Lf) >= thr3[:, None]
        out["BH2k2"] = (np.abs(Lf) >= thr2[:, None]).any(axis=1) & gel
        for p in E["S4"]["pencere"]:
            ek = "" if p == E["S4"]["ana_pencere"] else f"_{p}"
            out["B0" + ek] = (Tf >= SB["b0_kat"] * G["trp" + ek].to_numpy()[:, None]).any(axis=1) & gel
        buyuk = Tf >= SB["b1_kat"] * atr[:, None]
    b1 = S.B1.to_numpy(); k1 = S.k1.to_numpy().astype(int)
    ii = np.arange(n)
    r_k1 = np.where(b1, rf[ii, np.clip(k1 - 1, 0, h - 1)], np.nan)
    out["B1_up"] = b1 & (r_k1 > 0)
    bh2 = S.B2.to_numpy()
    kh = np.where(bh2, bh.argmax(axis=1) + 1, 0)
    l_kh = np.where(bh2, Lf[ii, np.clip(kh - 1, 0, h - 1)], np.nan)
    out["BH2"] = bh2; out["kh"] = kh; out["BH2_up"] = bh2 & (l_kh > 0)
    for wi, (a, b) in enumerate(SY.SY_ESIK["zaman"]["pencere"], 1):
        out[f"f{wi}"] = b1 & (k1 >= a) & (k1 <= b)
        out[f"h{wi}"] = bh2 & (kh >= a) & (kh <= b)
    X = pd.DataFrame(out, index=d.index)
    return pd.concat([S.drop(columns=["B2", "B3", "B0", "B1_5"]), X], axis=1)


# ---------------------------------------------------------------- 3) PANEL
_SC_GECMIS_KOL = ["atr", "sig", "m10", "band", "s1c", "ev1", "run", "liq", "mom", "vk", "m", "qm", "bbw", "qb", "bbr", "net", "bant4", "asagi",
                  "trp", "ci", "cii", "ciii", "run4", "s4c", "ev4", "trp_20", "s4c_20", "ev4_20", "run4_20", "oran", "oran_20", "oran_S1"]
_SC_SONUC_KOL = ["B1", "k1", "BH2", "kh", "B1k2", "BH2k2", "B0", "B0_20", "B1_up", "BH2_up", "f1", "f2", "f3", "f4", "h1", "h2", "h3", "h4",
                 "c_yon", "c_r", "c_giris", "c_cikis", "c_ilk20", "c_ilk10"]
_SC_BOOL = ["s1c", "ev1", "ci", "cii", "ciii", "s4c", "ev4", "s4c_20", "ev4_20", "sup", "sup_sy", "gel", "c_ok"]


def sc_panel(V: Dict[str, pd.DataFrame], pazar: str, E: Optional[Dict[str, Any]] = None, sonuc: bool = True) -> pd.DataFrame:
    """Bütün hisse-günler: geçmiş özellikler, (sonuc=True) sonuçlar, uygunluk, dönem, eş hücreleri (hucA, hucE2, hucE2_20, hucE2_S1, hucC)."""
    E = E or SC_ESIK; SE = SY.SY_ESIK
    parca = []
    for s, d in V.items():
        try:
            G = sc_gecmis(d, pazar, E)
            C = d.Close.to_numpy(float)
            sup = SY.sy_bolunme_supheli(C, SE)
            X = G[_SC_GECMIS_KOL].copy()
            X["sup"] = SY._sy_pencere_var(sup, *E["bolunme_gecmis"]); X["sup_sy"] = SY._sy_pencere_var(sup, *E["sy_bolunme_bilgi"])
            X["gel"] = np.arange(len(d)) + SE["B"]["ufuk"] <= len(d) - 1
            X["c_ok"] = np.arange(len(d)) + SE["C"]["gelecek_bar"] <= len(d) - 1
            if sonuc:
                R = sc_sonuc(d, G, E)
                for c in _SC_SONUC_KOL:
                    X[c] = R[c].to_numpy()
            X["sembol"] = s; X["tarih"] = d.index
            X = X[np.arange(len(d)) >= E["gecmis_min"]]
            parca.append(X)
        except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer (log'da)
            sclog.warning("%s %s panel dışı: %s", pazar, s, ex)
    P = pd.concat(parca, ignore_index=True)
    for c in _SC_BOOL:
        if c in P:
            P[c] = P[c].fillna(False).astype(bool)
    P["pazar"] = pazar
    P["donem"] = _sc_donem(P.tarih, E)
    P["liq_pct"] = P.groupby("tarih").liq.rank(pct=True)
    temel = (P.donem != "") & np.isfinite(P.atr) & np.isfinite(P.sig) & np.isfinite(P.liq) & (P.liq_pct > SE["likidite"]["alt_kesik"]) \
        & (P.sig > 0) & (P.atr > 0)
    P["uygun"] = temel & P.gel & ~P.sup
    P["uygun_sy"] = temel & P.gel & ~P.sup_sy            # bilgi: SY'nin bölünme penceresi
    P["uygun_c"] = P.uygun & P.c_ok & np.isfinite(P.mom)
    u = P.uygun
    g = P[u].groupby("tarih")
    for c in ("oyn", "lq3", "e2", "e2_20", "e2_S1", "mom5"):
        P[c] = -1
    P.loc[u, "oyn"] = (np.ceil(g.sig.rank(pct=True, method="first") * SE["eslesme"]["oyn_kova"]) - 1).astype(int)
    P.loc[u, "lq3"] = (np.ceil(g.liq.rank(pct=True, method="first") * SE["likidite"]["kova"]) - 1).astype(int)
    for kol, oran in (("e2", "oran"), ("e2_20", "oran_20"), ("e2_S1", "oran_S1")):
        uu = u & np.isfinite(P[oran])
        P.loc[uu, kol] = (np.ceil(P[uu].groupby("tarih")[oran].rank(pct=True, method="first") * E["es"]["oran_kova"]) - 1).astype(int)
    uc = P.uygun_c
    P.loc[uc, "mom5"] = (np.ceil(P[uc].groupby("tarih").mom.rank(pct=True, method="first") * SE["eslesme"]["mom_kova"]) - 1).astype(int)
    P["hucA"] = P.oyn * 10 + P.lq3
    P["hucE2"] = np.where(P.e2 >= 0, P.e2 * 10 + P.lq3, -1)
    P["hucE2_20"] = np.where(P.e2_20 >= 0, P.e2_20 * 10 + P.lq3, -1)
    P["hucE2_S1"] = np.where(P.e2_S1 >= 0, P.e2_S1 * 10 + P.lq3, -1)
    P["hucC"] = P.mom5 * 10 + P.lq3
    return P


def sc_sayim(P: pd.DataFrame) -> Dict[str, Any]:
    """Olay SAYIMI ve S1 ile çakışma (sonuç / getiri kullanmaz)."""
    D = [d[0] for d in SC_ESIK["donem"]]
    out: Dict[str, Any] = {}
    for ad, ev in (("S4", "ev4"), ("S4_p20", "ev4_20"), ("S1", "ev1")):
        x = P[P.uygun & P[ev]]
        out[ad] = {d: int((x.donem == d).sum()) for d in D}
    for ad, (ev, kos) in {"S4_olay_S1_gunu": ("ev4", "s1c"), "S1_olay_S4_gunu": ("ev1", "s4c")}.items():
        x = P[P.uygun & P[ev]]
        out[ad] = {d: (float(x[x.donem == d][kos].mean()) if (x.donem == d).any() else None) for d in D}
    x = P[P.uygun & P.ev4]
    out["S4_olay_S1_ayni_gun_olay"] = {d: (float(x[x.donem == d].ev1.mean()) if (x.donem == d).any() else None) for d in D}
    out["S4_gun_pay"] = {d: (float(P[P.uygun & (P.donem == d)].s4c.mean()) if (P.uygun & (P.donem == d)).any() else None) for d in D}
    out["S1_gun_pay"] = {d: (float(P[P.uygun & (P.donem == d)].s1c.mean()) if (P.uygun & (P.donem == d)).any() else None) for d in D}
    out["hisse"] = int(P.sembol.nunique()); out["uygun_gun"] = int(P.uygun.sum())
    out["kosul_pay"] = {k: float(P.loc[P.uygun, k].mean()) for k in ("ci", "cii", "ciii")}
    return out


# ---------------------------------------------------------------- 4) (A) KAT, (B) ZAMAN, (C) İŞLEM
def _sc_hucre_karar(n: int, a1: float, a2: float, u1: float, u2: float, E: Dict[str, Any]) -> str:
    K = E["karar"]
    if n < K["n_min"] or not (np.isfinite(a1) and np.isfinite(a2)):
        return "ÖLÇÜLEMEDİ"
    if a1 > 1 and a2 > 1:
        return "GEÇER"
    if n >= K["n_guc"]:
        return "TERS" if (u1 < 1 or u2 < 1) else "TUTMADI"
    return "ÖLÇÜLEMEDİ (güç)"


def sc_olc_A(P: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """KAT tablosu: tanım (S4 p15, S4 p20, S4 p15 SY bölünme penceresi, S1) x eş (es1, es2) x sonuç x dönem. İkinci dönüş: satır tabloları."""
    E = E or SC_ESIK; pazar = P.pazar.iat[0]; sat = []; satir = {}
    Bs = ["B1", "BH2", "B1k2", "BH2k2"]
    tanim = [("S4", "ev4", "s4c", "uygun", "hucE2", Bs + ["B0"]), ("S4_p20", "ev4_20", "s4c_20", "uygun", "hucE2_20", Bs + ["B0_20"]),
             ("S4_supSY", "ev4", "s4c", "uygun_sy", "hucE2", ["B1", "BH2"]), ("S1", "ev1", "s1c", "uygun", "hucE2_S1", ["B1", "BH2"])]
    donem = [d[0] for d in E["donem"]] + list(E["birlesik"])
    for ad, ev, kos, um, h2, deg in tanim:
        u = P[um]
        olay = u & P[ev]
        ekstra = ["B1_up", "BH2_up", "f1", "f2", "f3", "f4", "h1", "h2", "h3", "h4"] if ad == "S4" else []
        for es, huc in (("es1", "hucA"), ("es2", h2)):
            es_m = u & ~P[kos] & (P[huc] >= 0)
            X = SY.sy_es_ortalama(P, olay & (P[huc] >= 0), es_m, huc, deg + ekstra)
            X = X[X.es_n >= E["es"]["min_es"]]
            if ad in ("S4", "S1"):
                satir[f"{ad}_{es}"] = X
            for dn in donem:
                Y = X[X.donem.isin(E["birlesik"][dn])] if dn in E["birlesik"] else X[X.donem == dn]
                ay = Y.tarih.dt.to_period("M").astype(str).to_numpy()
                for b in deg:
                    kat, a95, u95 = SY.sy_oran_boot(Y[b].astype(float).to_numpy(), Y["es_" + b].to_numpy(), ay, SY.SY_ESIK,
                                                    zlib.crc32(f"{ad}|{es}|{dn}|{b}".encode()) % 1000)
                    sat.append({"pazar": pazar, "donem": dn, "sikisma": ad, "es": es, "olcu": "B0" if b.startswith("B0") else b, "n": int(len(Y)),
                                "p_olay": float(Y[b].mean()) if len(Y) else np.nan, "p_es": float(Y["es_" + b].mean()) if len(Y) else np.nan,
                                "kat": kat, "alt95": a95, "ust95": u95, "es_n_medyan": float(Y.es_n.median()) if len(Y) else np.nan})
    for dn in [d[0] for d in E["donem"]]:
        U = P[P.uygun & (P.donem == dn)]
        sat.append({"pazar": pazar, "donem": dn, "sikisma": "TABAN_tum_gunler", "es": "-", "olcu": "B1", "n": int(len(U)),
                    "p_olay": float(U.B1.mean()) if len(U) else np.nan})
        sat.append({"pazar": pazar, "donem": dn, "sikisma": "TABAN_tum_gunler", "es": "-", "olcu": "BH2", "n": int(len(U)),
                    "p_olay": float(U.BH2.mean()) if len(U) else np.nan})
    return pd.DataFrame(sat), satir


def sc_olc_B(X1: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """S4 (p15) olaylarında ilk büyük hareketin zamanı ve yönü (eş 1 satırları; eş değerleri aynı gün aynı hücre ortalaması)."""
    E = E or SC_ESIK; pazar = X1.pazar.iat[0] if len(X1) else "?"; out = []
    donem = [d[0] for d in E["donem"]] + list(E["birlesik"])
    for dn in donem:
        Y = X1[X1.donem.isin(E["birlesik"][dn])] if dn in E["birlesik"] else X1[X1.donem == dn]
        for b, k, up, fw in (("B1", "k1", "B1_up", "f"), ("BH2", "kh", "BH2_up", "h")):
            Z = Y[Y[b].astype(bool)]
            r = {"pazar": pazar, "donem": dn, "olcu": b, "n": int(len(Y)), "n_olay": int(len(Z))}
            if len(Z):
                q = np.quantile(Z[k].astype(float), [0.25, 0.5, 0.75])
                r.update({"k_q25": float(q[0]), "k_medyan": float(q[1]), "k_q75": float(q[2]), "yukari_pay": float(Z[up].astype(bool).mean())})
            es_b = float(Y["es_" + b].sum()); es_u = float(Y["es_" + up].sum())
            r["es_yukari_pay"] = es_u / es_b if es_b > 0 else np.nan
            for wi in range(1, 5):
                r[f"p_{fw}{wi}"] = float(Y[f"{fw}{wi}"].astype(float).mean()) if len(Y) else np.nan
                r[f"es_p_{fw}{wi}"] = float(Y[f"es_{fw}{wi}"].mean()) if len(Y) else np.nan
            out.append(r)
    return out


def sc_olc_C(P: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """SY.sy_olc_C aynen: olay = S4 (p15) olayı, eş = S4 koşulu yanlış (SY kodu ev1 / s1c sütunlarını okur; bu çağrı için yeniden adlandırılır)."""
    Q = P[["pazar", "tarih", "donem", "sembol", "uygun_c", "ev4", "s4c", "hucC", "c_yon", "c_r", "c_giris", "c_cikis", "c_ilk20", "c_ilk10"]] \
        .rename(columns={"ev4": "ev1", "s4c": "s1c"})
    return SY.sy_olc_C(Q, SY.SY_ESIK)


# ---------------------------------------------------------------- 5) GELECEĞE BAKMA DENETİMİ (mekanik)
def sc_gelecek_denetimi(V: Dict[str, pd.DataFrame], X: pd.DataFrame, pazar: str, E: Optional[Dict[str, Any]] = None, n: Optional[int] = None) -> int:
    E = E or SC_ESIK; n = n or E["gelecek_denetimi_n"]
    rng = np.random.default_rng(E["tohum"])
    sec = X.iloc[rng.choice(len(X), min(n, len(X)), replace=False)] if len(X) else X
    kol = ["m", "qm", "bbw", "qb", "net", "bant4", "asagi", "trp", "run4", "s4c", "ev4", "s4c_20", "ev4_20", "oran", "atr", "sig", "liq", "s1c", "ev1"]
    for r in sec.itertuples():
        d = V[r.sembol]
        G1 = sc_gecmis(d, pazar, E).loc[r.tarih, kol]
        G2 = sc_gecmis(d[d.index <= r.tarih], pazar, E).iloc[-1][kol]
        a = pd.to_numeric(G1, errors="coerce").astype(float).to_numpy(); b = pd.to_numeric(G2, errors="coerce").astype(float).to_numpy()
        if not np.allclose(a, b, equal_nan=True, rtol=1e-9, atol=1e-12):
            raise SCHata(f"geleceğe bakma denetimi tutmadı: {pazar} {r.sembol} {pd.Timestamp(r.tarih).date()}")
    return len(sec)


# ---------------------------------------------------------------- 6) FENER MEKANİK DOĞRULAMA (tanı; sonuç ölçmez)
def _sc_yahoo_sy(d: pd.DataFrame) -> pd.DataFrame:
    """TAVAN_SERISI.ts_yahoo_oku çıktısı (o, h, l, c, v, carpan) -> SY biçimi (Open..Volume, Kur=1) + 'ekran' (c x carpan)."""
    x = pd.DataFrame({"Open": d.o, "High": d.h, "Low": d.l, "Close": d.c, "Volume": d.v}, index=d.index)
    y = SY.sy_veri_hazirla(x, SY.SY_ESIK)
    y["ekran"] = (d.c * d["carpan"]).reindex(y.index).to_numpy() if "carpan" in d else y.Close.to_numpy()
    y["carpan"] = d["carpan"].reindex(y.index).to_numpy() if "carpan" in d else 1.0
    return y


def sc_fener(E: Optional[Dict[str, Any]] = None, veri: Optional[str] = None, yahoo: Optional[str] = None) -> Dict[str, Any]:
    """FENER'de S4 (p15) iki bölgede: asıl (14.10-07.11.2025) en az bir s4c günü; yanlış (03-16.12.2025) hiç. Ekran (Yahoo) ve V_BIST.
    Düşen koşulları gün gün yazar (eşik oynamak için DEĞİL; tanı)."""
    E = E or SC_ESIK; F = E["fener"]; out: Dict[str, Any] = {}
    kaynak: Dict[str, pd.DataFrame] = {}
    try:
        import TAVAN_SERISI as TS
        S, _m = TS.ts_fiyatlar(yahoo or SC_YOL["yahoo"], semboller=[F["sembol"]])
        kaynak["ekran (Yahoo)"] = _sc_yahoo_sy(S[F["sembol"]])
    except Exception as ex:
        out["ekran_hata"] = str(ex)
    try:
        yol = os.path.join(veri or SC_YOL["veri"], "V_BIST.pkl")
        Vb = pd.read_pickle(yol); Vb = Vb.get("veri", Vb) if isinstance(Vb, dict) else Vb
        kaynak["V_BIST (düzeltilmiş)"] = SY.sy_veri_hazirla(Vb[F["sembol"]], SY.SY_ESIK)
    except Exception as ex:
        out["vbist_hata"] = str(ex)
    for ad, d in kaynak.items():
        X = sc_s4(d, "BIST", E["S4"]["ana_pencere"], E)
        G = SY.sy_gecmis(d, "BIST", SY.SY_ESIK)
        r: Dict[str, Any] = {}
        for bolge, (a, b) in (("asil", F["asil"]), ("yanlis", F["yanlis"])):
            Z = X.loc[a:b]; Gz = G.loc[a:b]
            r[bolge] = {"s4_gun": [str(t.date()) for t in Z.index[Z.s4c]], "s1_gun": [str(t.date()) for t in Gz.index[Gz.s1c.astype(bool)]],
                        "gunluk": [{"tarih": str(t.date()), "i": bool(z.ci), "ii": bool(z.cii), "iii": bool(z.ciii), "run": int(z.run4),
                                    "mum": _sc_temiz(z.m), "mum_q20": _sc_temiz(z.qm), "bbw": _sc_temiz(z.bbw), "bbw_q20": _sc_temiz(z.qb),
                                    "bb_yuzdelik": _sc_temiz(z.bbr), "net": _sc_temiz(z.net), "bant": _sc_temiz(z.bant4), "asagi": _sc_temiz(z.asagi)}
                                   for t, z in Z.iterrows()]}
        r["asil_tutar"] = len(r["asil"]["s4_gun"]) > 0
        r["yanlis_tutar"] = len(r["yanlis"]["s4_gun"]) == 0
        r["ev4_2025_26"] = [str(t.date()) for t in X.index[X.ev4 & (X.index >= "2025-01-01")]]
        out[ad] = r
    out["tutar"] = all(v["asil_tutar"] and v["yanlis_tutar"] for k, v in out.items() if isinstance(v, dict) and "asil_tutar" in v) and \
        any(isinstance(v, dict) and "asil_tutar" in v for v in out.values())
    return out


def _sc_fener_md(F: Dict[str, Any]) -> List[str]:
    s = ["| Kaynak | asıl bölge (14.10-07.11.2025) S4 günleri | yanlış bölge (03-16.12.2025) S4 günleri | S1 günleri (asıl / yanlış) | sonuç |", "|---|---|---|---|---|"]
    for ad, r in F.items():
        if not isinstance(r, dict) or "asil" not in r:
            continue
        s.append(f"| {ad} | {', '.join(r['asil']['s4_gun']) or 'YOK'} | {', '.join(r['yanlis']['s4_gun']) or 'YOK'} | "
                 f"{len(r['asil']['s1_gun'])} / {len(r['yanlis']['s1_gun'])} | {'TUTTU' if r['asil_tutar'] and r['yanlis_tutar'] else 'TUTMADI'} |")
    for ad, r in F.items():
        if not isinstance(r, dict) or "asil" not in r:
            continue
        if s[-1] != "":
            s.append("")
        for bolge, ad_b in (("asil", "asıl (14.10-07.11.2025)"), ("yanlis", "yanlış (03-16.12.2025)")):
            gl = r[bolge]["gunluk"]
            ucu = sum(1 for g in gl if g["i"] and g["ii"] and g["iii"]); rm = max((g["run"] for g in gl), default=0)
            dus = [k for k, ad_k in (("i", "(i) küçük mum"), ("ii", "(ii) dar BB"), ("iii", "(iii) yatay")) if not any(g[k] for g in gl)]
            s.append(f"- {ad}, {ad_b}: (i)+(ii)+(iii) aynı gün doğru {ucu} gün; (i)+(ii) en uzun ardışık {rm} gün "
                     f"({'(iv) uzunluk DÜŞTÜ: < 10' if rm < SC_ESIK['S4']['uzunluk'] else '(iv) sağlandı'}); hiç doğru olmayan koşul: {', '.join(dus) or 'yok'}.")
    for ad, r in F.items():
        if not isinstance(r, dict) or "asil" not in r:
            continue
        s += ["", f"Günlük koşullar — {ad} (i küçük mum, ii dar BB, iii yatay, run = (i)&(ii) ardışık gün):", "",
              "| bölge | tarih | i | ii | iii | run | mum / q20 | BBW / q20 | BB yüzdelik | net | bant | aşağı açılış payı |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for bolge in ("asil", "yanlis"):
            for g in r[bolge]["gunluk"]:
                f = lambda x, k=1: "-" if x is None else f"{x * 100:.{k}f}"   # noqa: E731
                s.append(f"| {bolge} | {g['tarih']} | {'E' if g['i'] else '-'} | {'E' if g['ii'] else '-'} | {'E' if g['iii'] else '-'} | {g['run']} | "
                         f"{f(g['mum'], 2)} / {f(g['mum_q20'], 2)} | {f(g['bbw'], 1)} / {f(g['bbw_q20'], 1)} | "
                         f"{'-' if g['bb_yuzdelik'] is None else round(g['bb_yuzdelik'], 2)} | {f(g['net'])} | {f(g['bant'])} | "
                         f"{'-' if g['asagi'] is None else round(g['asagi'], 2)} |")
    return s


# ---------------------------------------------------------------- 7) ÖN KAYIT
_SC_DESEN = {"muhur": r"MÜHÜR \(SC_ESIK sha256\): `([0-9a-f]{64})`", "kod": r"KOD \(SIKISMA_CEMAL\.py sha256\): `([0-9a-f]{64})`",
             "sy_kod": r"SY_KOD \(SIKISMA_YENIDEN\.py sha256\): `([0-9a-f]{64})`", "zaman": r"ZAMAN \(UTC\): `([^`]+)`"}


def sc_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = SC_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def _sc_yz(x: Any, k: int = 1) -> str:
    try:
        return "-" if x is None or not math.isfinite(float(x)) else f"%{float(x) * 100:.{k}f}"
    except (TypeError, ValueError):
        return "-"


def _sc_s(x: Any, k: int = 2) -> str:
    try:
        return "-" if x is None or not math.isfinite(float(x)) else f"{float(x):.{k}f}"
    except (TypeError, ValueError):
        return "-"


def sc_onkayit_metni(sayim: Dict[str, Dict[str, Any]], veri_sha: Dict[str, str], fener: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or SC_ESIK; T = E["S4"]["tanim"]
    s = ["# SIKISMA_CEMAL (S4) — ÖN KAYIT", "", SC_SURUM, "",
         f"- MÜHÜR (SC_ESIK sha256): `{sc_esik_sha(E)}`", f"- KOD (SIKISMA_CEMAL.py sha256): `{SY._sy_sha_dosya(SC_YOL['kod'])}`",
         f"- SY_KOD (SIKISMA_YENIDEN.py sha256): `{SY._sy_sha_dosya(SC_YOL['sy_kod'])}`", f"- ZAMAN (UTC): `{_sc_simdi()}`",
         "- Bu dosya ölçümden ÖNCE yazılır ve commit + push edilir; `kos` OC.oc_kapi (kontrol + cetvel sha + git) ve kendi kapısı (mühür, iki kod sha, "
         "git'e işlenmiş ve değişmemiş) geçmezse durur.", "",
         "## Cetvel mühür satırları (ORTAK_CETVEL; aynen)", "", OC.oc_kapi_satirlari(), "",
         "## Soru", "Cemal'in gözüyle tanımlanan sıkışma (küçük mum + yatay + dar Bollinger + en az 10 gün) bitince 20 günde hissenin olağan ölçüsüne göre "
         "büyük hareket (B1 tek gün, BH2 çok gün) eşlerden sık mı; ne zaman, hangi yöne. 60 gün getiri ve yönsüz işlem bilgi.", "",
         "## Tanım (SC_ESIK['S4'])", ""]
    s += [f"- (i) {T['i']}", f"- (ii) {T['ii']}", f"- (iii) {T['iii']}", f"- (iv) {T['iv']}", f"- {T['olay']}", f"- {T['p20']}",
          f"- Geçmiş: en az {E['gecmis_min']} geçerli bar. Uygunluk: {E['uygun']}.",
          f"- Bölünme şüphesi: SY.sy_bolunme_supheli ANA, pencere {E['bolunme_gecmis']} (yalnız geçmiş). SY'nin [{E['sy_bolunme_bilgi'][0]}, +{E['sy_bolunme_bilgi'][1]}] "
          "penceresiyle aynı ölçüm bilgi satırı (S4_supSY).", "", "## Sonuçlar (SIKISMA_YENIDEN içe alınır)", ""]
    s += [f"- **{k}**: {v}" for k, v in E["sonuc"]["tanim"].items()]
    s += [f"- Yön: B1 {E['sonuc']['yon']['B1']}; BH2 {E['sonuc']['yon']['BH2']}.", f"- Zaman: {E['sonuc']['zaman']}.",
          f"- Eş 1: {E['es']['es1']}.", f"- Eş 2: {E['es']['es2']}.", f"- {E['es']['olay_secimi']}; bootstrap {E['bootstrap']}.",
          f"- (C) 60 gün: {E['OC']}", f"- (C) işlem: {E['C']}", f"- Dönemler {E['donem']}; karar hücreleri ABD / AVR x 2023 / 2024-26; BIST ve 2016-22 bilgi.",
          f"- Hücre kararı: {E['karar']['hucre']}.", f"- Etiket: {E['karar']['etiket']}.", "",
          "## FENER MEKANİK DOĞRULAMA (tanı; sonuç / getiri ölçmez; eşikler bu kontrolden ÖNCE yazıldı ve oynanmadı)", "", E["fener"]["tanim"], "",
          f"**Sonuç: {'TUTTU' if fener.get('tutar') else 'TUTMADI'}**", ""] + _sc_fener_md(fener) + [""]
    if not fener.get("tutar"):
        s += ["**Tanı (ölçümden önce yazıldı):** yanlış bölge (03-16.12.2025) doğru biçimde DIŞARIDA ((ii) dar BB ve (iii) yatay hiç doğru değil). Asıl bölgede "
              "(14.10-07.11.2025) S4 günü YOK: düşen koşul (iv) uzunluk. (i) küçük mum (15 günlük ortalama) ve (ii) dar Bollinger (20 gün) pencereleri bölgeden "
              "önceki düşüşü içerdiği için ancak 31 Ekim'den sonra doğru oluyor; 18 barlık bölgede (i)+(ii) en çok 3-4 gün ardışık. İş tanımı gereği eşik "
              "OYNANMADI; ölçüm bu S4 tanımıyla sürer. Sınır: S4, Cemal'in iki bölgesinden yanlışı dışlıyor ama asılı yakalamıyor; kısa (< ~25 bar) "
              "sıkışmalar S4'e girmez. Uzunluk koşulunun yeniden tanımı (ör. (iv)'ü bölge içi ölçülerle saymak) Cemal kararıdır ve yeni ön kayıt ister.", ""]
    s += ["## Eşik sözlüğü (SC_ESIK, kararlı JSON)", "", "```json", json.dumps(E, sort_keys=True, ensure_ascii=False, indent=1, default=str), "```", "",
          "## Veri", ""] + [f"- V_{p}.pkl sha256: `{h}`" for p, h in veri_sha.items()]
    s += ["", "## Olay SAYIMI (sonuç / getiri hesaplanmadan; uygun hisse-gün)", "",
          "| Pazar | Tanım | 2016-22 | 2023 | 2024-26 |", "|---|---|---|---|---|"]
    for p, c in sayim.items():
        for k in ("S4", "S4_p20", "S1"):
            s.append(f"| {p} | {k} | {c[k]['2016-22']} | {c[k]['2023']} | {c[k]['2024-26']} |")
    s += ["", "| Pazar | S1/S4 olay oranı (2016-22 / 2023 / 2024-26) | S4 olaylarının S1 günü olan payı | S1 olaylarının S4 günü olan payı | "
          "S4 gün payı | S1 gün payı | (i) / (ii) / (iii) gün payı | hisse | uygun gün |", "|---|---|---|---|---|---|---|---|---|"]
    D = [d[0] for d in E["donem"]]
    for p, c in sayim.items():
        orn = " / ".join(_sc_s(c["S1"][d] / c["S4"][d], 1) if c["S4"][d] else "-" for d in D)
        s.append(f"| {p} | {orn} | {' / '.join(_sc_yz(c['S4_olay_S1_gunu'][d]) for d in D)} | {' / '.join(_sc_yz(c['S1_olay_S4_gunu'][d]) for d in D)} | "
                 f"{' / '.join(_sc_yz(c['S4_gun_pay'][d], 2) for d in D)} | {' / '.join(_sc_yz(c['S1_gun_pay'][d], 2) for d in D)} | "
                 f"{' / '.join(_sc_yz(c['kosul_pay'][k]) for k in ('ci', 'cii', 'ciii'))} | {c['hisse']} | {c['uygun_gun']} |")
    s += ["", "## Sınırlar (önceden)", "- Evren bugünün listesi: batan / kottan çıkan hisseler yok (hayatta kalma yanlılığı).",
          "- Bilanço takvimi yok: büyük günlerin bir kısmı bilanço günüdür.", "- Komisyon, kayma, açığa satış maliyeti yok.",
          "- BIST ölçümü düzeltilmiş fiyatla (V_BIST); liste ekran fiyatıyla (Yahoo). BIST ±%10 sınırı B1'i kısar (BH2 bu yüzden ikinci ana ölçü).",
          "- S4 S1'den çok daha seyrektir: güç sınırlı hücreler ÖLÇÜLEMEDİ yazılır, 'yok' denmez.", "", sc_kontrol_tablosu(), ""]
    return "\n".join(s)


def sc_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False) -> str:
    yol = _sc_yol("onkayit", cikti)
    if os.path.exists(yol):
        if not uzerine:
            raise SCHata(f"ön kayıt zaten var ({yol}); üzerine yazılmaz")
        try:
            SY._sy_git_islenmis(yol)
            raise SCHata(f"ön kayıt git'e işlenmiş ({yol}); üzerine yazılmaz")
        except SY.SYHata as ex:
            if "işlenmemiş" not in str(ex):
                raise SCHata(str(ex))
    sayim, vsha = {}, {}
    for p in SC_PAZAR:
        vsha[p] = SY._sy_sha_dosya(os.path.join(veri or SC_YOL["veri"], f"V_{p}.pkl"))
        V = SY.sy_veri_yukle(p, SY.SY_ESIK, veri or SC_YOL["veri"])
        P = sc_panel(V, p, SC_ESIK, sonuc=False)
        sayim[p] = sc_sayim(P)
        sclog.info("%s sayım: S4 %s S1 %s", p, sayim[p]["S4"], sayim[p]["S1"])
        del P, V
    fener = sc_fener(veri=veri)
    metin = sc_onkayit_metni(sayim, vsha, fener)
    if _SC_EPOSTA.search(metin):
        raise SCHata("ön kayıtta e-posta biçimli parça var")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    sclog.info("ön kayıt yazıldı: %s", yol)
    return yol


def sc_onkayit_dogrula(yol: Optional[str] = None, git: bool = True, kod_sha: bool = True) -> Dict[str, Any]:
    yol = yol or _sc_yol("onkayit")
    if not os.path.exists(yol):
        raise SCHata(f"ön kayıt yok ({yol}): önce `python SIKISMA_CEMAL.py onkayit`")
    metin = open(yol, encoding="utf-8").read(); oc = {}
    for ad, desen in _SC_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise SCHata(f"ön kayıt bozuk: '{ad}' yok")
        oc[ad] = m.group(1)
    if oc["muhur"] != sc_esik_sha():
        raise SCHata("ön kayıt mührü tutmuyor: eşikler ön kayıttan sonra değişmiş, koşu durdu")
    if kod_sha and oc["kod"] != SY._sy_sha_dosya(SC_YOL["kod"]):
        raise SCHata("SIKISMA_CEMAL.py sha256 ön kayıttakinden farklı (SAPMA): koşu durdu")
    if kod_sha and oc["sy_kod"] != SY._sy_sha_dosya(SC_YOL["sy_kod"]):
        raise SCHata("SIKISMA_YENIDEN.py sha256 ön kayıttakinden farklı: içe alınan sonuç tanımları değişmiş, koşu durdu")
    out = {"yol": yol, **oc}
    if git:
        try:
            out["git"] = SY._sy_git_islenmis(yol)
        except SY.SYHata as ex:
            raise SCHata(str(ex))
    return out


# ---------------------------------------------------------------- 8) KOŞU
def _sc_birlestir(parca: List[Dict[str, Any]]) -> Dict[str, Any]:
    T = pd.concat([p["hucre"] for p in parca if len(p["hucre"])], ignore_index=True) if parca else pd.DataFrame()
    return {"hucre": T, "olay": pd.concat([p["olay"] for p in parca], ignore_index=True) if parca else pd.DataFrame(),
            "olasilik": pd.concat([p["olasilik"] for p in parca], ignore_index=True) if parca else pd.DataFrame(),
            "sayim": {k: v for p in parca for k, v in p["sayim"].items()},
            "etiket": OC.oc_etiket(T) if len(T) else {"genel": "VERİ YOK", "olasilik": "ÖLÇÜLEMEDİ", "karar_hucre": {}},
            "cetvel_sha": parca[0]["cetvel_sha"] if parca else OC.oc_esik_sha(), "kod_sha": parca[0]["kod_sha"] if parca else "", "surum": OC.OC_SURUM}


def sc_karar(TA: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or SC_ESIK; out: Dict[str, Any] = {}
    for b in E["sonuc"]["ana"] + E["sonuc"]["bilgi"]:
        hucre = {}
        for p in E["karar_pazar"] + E["bilgi_pazar"]:
            for d in [x[0] for x in E["donem"]] + list(E["birlesik"]):
                x = {es: TA[(TA.sikisma == "S4") & (TA.es == es) & (TA.olcu == b) & (TA.pazar == p) & (TA.donem == d)] for es in ("es1", "es2")}
                if not all(len(v) for v in x.values()):
                    hucre[f"{p} {d}"] = "ÖLÇÜLEMEDİ"; continue
                r1, r2 = x["es1"].iloc[0], x["es2"].iloc[0]
                hucre[f"{p} {d}"] = _sc_hucre_karar(int(min(r1.n, r2.n)), r1.alt95, r2.alt95, r1.ust95, r2.ust95, E)
        kh = [hucre.get(f"{p} {d}", "ÖLÇÜLEMEDİ") for p in E["karar_pazar"] for d in E["karar_donem"]]
        if all(v == "GEÇER" for v in kh):
            g = "CEMAL SIKIŞMASI BÜYÜK HAREKET HABERCİSİ"
        elif any(v == "GEÇER" for v in kh):
            g = "EMARE (" + ", ".join(f"{p} {d}={hucre[f'{p} {d}']}" for p in E["karar_pazar"] for d in E["karar_donem"]) + ")"
        elif all(v in ("TUTMADI", "TERS") for v in kh):
            g = "HABERCİ DEĞİL" + (" (TERS: S4 sonrası büyük hareket eşlerden SEYREK)" if all(v == "TERS" for v in kh) else "")
        else:
            g = "ÖLÇÜLEMEDİ (" + ", ".join(f"{p} {d}={hucre[f'{p} {d}']}" for p in E["karar_pazar"] for d in E["karar_donem"]) + ")"
        out[b] = {"etiket": g if b in E["sonuc"]["ana"] else "BİLGİ: " + g, "hucre": hucre}
    return out


def sc_kos(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True, pazarlar: Tuple[str, ...] = SC_PAZAR,
           satir: Optional[str] = None, oc_veri: bool = True) -> Dict[str, Any]:
    E = SC_ESIK; t0 = time.time()
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    yol = _sc_yol("onkayit", cikti)
    kapi = OC.oc_kapi(yol, git=git, kontrol=kontrol)
    ok = sc_onkayit_dogrula(yol, git=git)
    kz = _sc_simdi()
    satir = satir or SC_YOL["satir"]; os.makedirs(satir, exist_ok=True)
    A_, B_, C_, den, oc_parca, say = [], [], [], {}, [], {}
    for p in pazarlar:
        V = SY.sy_veri_yukle(p, SY.SY_ESIK, veri or SC_YOL["veri"])
        P = sc_panel(V, p, E, sonuc=True)
        say[p] = sc_sayim(P)
        tA, satirlar = sc_olc_A(P, E)
        X1 = satirlar["S4_es1"]
        den[p] = {"gelecek_denetimi_olay": sc_gelecek_denetimi(V, X1, p, E)}
        B_ += sc_olc_B(X1, E)
        tC, XC = sc_olc_C(P)
        A_.append(tA); C_.append(tC)
        for ad, X in satirlar.items():
            kol = [c for c in ["pazar", "sembol", "tarih", "donem", "hucA", "hucE2", "hucE2_S1", "es_n", "B1", "BH2", "B1k2", "BH2k2", "B0", "k1", "kh",
                               "B1_up", "BH2_up", "es_B1", "es_BH2", "es_B1k2", "es_BH2k2", "es_B0", "es_B1_up", "es_BH2_up", "m", "bbr", "net", "bant4",
                               "run4", "s1c"] if c in X.columns]
            X[kol].to_csv(os.path.join(satir, f"olay_{ad}_{p}.csv.gz"), index=False)
        # eş havuzu (bağımsız yeniden üretim için): gün x hücre toplamları
        for es, huc in (("es1", "hucA"), ("es2", "hucE2")):
            m_ = P.uygun & ~P.s4c & (P[huc] >= 0)
            P.loc[m_, ["tarih", huc, "B1", "BH2"]].groupby(["tarih", huc]).agg(B1_t=("B1", "sum"), BH2_t=("BH2", "sum"), n=("B1", "size")) \
                .reset_index().to_csv(os.path.join(satir, f"es_{es}_{p}.csv.gz"), index=False)
        XC.to_csv(os.path.join(satir, f"olay_C_{p}.csv.gz"), index=False)
        olay = P.loc[P.ev4 & (P.donem != "") & ~P.sup, ["sembol", "tarih"]].copy(); olay["pazar"] = p
        olay.to_csv(os.path.join(satir, f"oc_girdi_{p}.csv.gz"), index=False)
        sclog.info("%s panel bitti: S4 olay %d (%.0f sn)", p, int((P.uygun & P.ev4).sum()), time.time() - t0)
        del P
        if oc_veri:
            Vd = OC.oc_veri(p, klasor=veri or SC_YOL["veri"], veri2=SC_YOL["veri2"])
            oc_parca.append(OC.oc_olc(olay.reset_index(drop=True), {p: Vd}))
            del Vd
            OC._OC_PANEL_ONBELLEK.clear()
        del V
        sclog.info("%s bitti (%.0f sn)", p, time.time() - t0)
    TA = pd.concat(A_, ignore_index=True); TC = pd.concat(C_, ignore_index=True)
    karar = sc_karar(TA, E)
    J: Dict[str, Any] = {"surum": SC_SURUM, "onkayit": ok, "oc_kapi": {k: v for k, v in kapi.items() if k != "kontrol"}, "kos_zaman_utc": kz,
                         "muhur": sc_esik_sha(), "sayim": say, "A": json.loads(TA.to_json(orient="records", force_ascii=False)),
                         "B": B_, "C": json.loads(TC.to_json(orient="records", force_ascii=False)), "karar": karar, "denetim": den, "pazarlar": list(pazarlar)}
    if oc_parca:
        S = _sc_birlestir(oc_parca)
        S["olay"].to_csv(os.path.join(satir, "oc_olay.csv.gz"), index=False)
        J["oc"] = {"hucre": json.loads(S["hucre"].to_json(orient="records", force_ascii=False)) if len(S["hucre"]) else [],
                   "olasilik": json.loads(S["olasilik"].to_json(orient="records", force_ascii=False)) if len(S["olasilik"]) else [],
                   "etiket": S["etiket"], "rapor": OC.oc_rapor(S, "S4 (Cemal sıkışması) olayları — 60 gün eşli (BİLGİ)")}
    J["sure_sn"] = round(time.time() - t0, 1)
    _sc_json(_sc_yol("sonuc", cikti), _sc_temiz(J))
    return {"sonuc": J, "rapor": sc_rapor(cikti)}


# ---------------------------------------------------------------- 9) RAPOR
def sc_rapor(cikti: Optional[str] = None) -> str:
    J = json.load(open(_sc_yol("sonuc", cikti), encoding="utf-8"))
    E = SC_ESIK; A = pd.DataFrame(J["A"]); C = pd.DataFrame(J["C"]); B = pd.DataFrame(J["B"])
    g = J["onkayit"].get("git", {}); D = [d[0] for d in E["donem"]]
    say = J["sayim"]

    def kat(p, d, b, es, sik="S4"):
        x = A[(A.pazar == p) & (A.donem == d) & (A.olcu == b) & (A.es == es) & (A.sikisma == sik)]
        return x.iloc[0] if len(x) else None

    def kt(r):
        return "-" if r is None or not r["n"] else f"{_sc_s(r['kat'])} [{_sc_s(r['alt95'])}, {_sc_s(r['ust95'])}]"

    s = ["# SIKISMA_CEMAL (S4) — RAPOR", "", f"{J['surum']}. Ön kayıt commit {str(g.get('commit', '-'))[:10]} ({g.get('commit_zamani', '-')}); "
         f"koşu {J['kos_zaman_utc']}; süre {J.get('sure_sn')} sn. Mühür `{J['muhur'][:16]}…`.", "", "## DÜZ DİL ÖZET", ""]
    for p in J["pazarlar"]:
        c = say[p]
        s.append(f"- **{p}**: S4 olayı {c['S4']['2016-22']} / {c['S4']['2023']} / {c['S4']['2024-26']} (2016-22 / 2023 / 2024-26); S1 olayı "
                 f"{c['S1']['2016-22']} / {c['S1']['2023']} / {c['S1']['2024-26']} -> S4, S1'den "
                 + " / ".join(_sc_s(c['S1'][d] / c['S4'][d], 1) + " kat" if c['S4'][d] else "-" for d in D) + " az. "
                 f"S4 olaylarının S1 günüyle çakışan payı {' / '.join(_sc_yz(c['S4_olay_S1_gunu'][d], 0) for d in D)}; S1 olaylarının S4 günü olan payı "
                 f"{' / '.join(_sc_yz(c['S1_olay_S4_gunu'][d], 0) for d in D)}.")
    for b in E["sonuc"]["ana"]:
        k = J["karar"][b]
        s.append(f"- **{b}** ({E['sonuc']['tanim'][b]}): **{k['etiket']}**.")
        for p in E["karar_pazar"] + E["bilgi_pazar"]:
            r1 = kat(p, "2023+", b, "es1")
            s.append(f"  - {p} 2023+: olay {_sc_yz(r1['p_olay'] if r1 is not None else None)} vs eş 1 {_sc_yz(r1['p_es'] if r1 is not None else None)}; "
                     f"KAT eş 1 {kt(r1)}, eş 2 {kt(kat(p, '2023+', b, 'es2'))}.")
    s += ["- Sayı ile yorum ayrı: KAT > 1 = S4'ten sonra 20 günde büyük hareket eşlerden SIK; < 1 = SEYREK. Eş 2 sıkışmanın kendi düşük oynaklığını "
          "dengeler (mekanik üstünlük kontrolü).", "- 60 gün getiri / olasılık tablosu ve yönsüz işlem BİLGİDİR (yön tahmini yok).",
          "- Hayatta kalma: evren bugünün listesi; batanlar yok.", "",
          "## KAT tablosu — ANA (S4 p15; B1 ve BH2; eş 1 / eş 2)", "",
          "| Pazar | Dönem | sonuç | n (eş1/eş2) | olay % | eş1 % | KAT eş 1 [%95] | eş2 % | KAT eş 2 [%95] | hücre |", "|---|---|---|---|---|---|---|---|---|---|"]
    for p in E["karar_pazar"] + E["bilgi_pazar"]:
        for d in D + list(E["birlesik"]):
            for b in E["sonuc"]["ana"] + E["sonuc"]["bilgi"]:
                r1, r2 = kat(p, d, b, "es1"), kat(p, d, b, "es2")
                if r1 is None:
                    continue
                s.append(f"| {p} | {d} | {b} | {int(r1['n'])}/{int(r2['n']) if r2 is not None else 0} | {_sc_yz(r1['p_olay'])} | {_sc_yz(r1['p_es'])} | {kt(r1)} | "
                         f"{_sc_yz(r2['p_es']) if r2 is not None else '-'} | {kt(r2)} | {J['karar'][b]['hucre'].get(f'{p} {d}', '-')} |")
    s += ["", "## Duyarlılık ve kıyas (bilgi): S4 p20, S4 SY bölünme penceresi, S1 (aynı panel, aynı eşler)", "",
          "| Pazar | Dönem | tanım | sonuç | n | KAT eş 1 [%95] | KAT eş 2 [%95] |", "|---|---|---|---|---|---|---|"]
    for p in E["karar_pazar"] + E["bilgi_pazar"]:
        for d in ("2023", "2024-26", "2023+"):
            for sik in ("S4_p20", "S4_supSY", "S1"):
                for b in ("B1", "BH2"):
                    r1, r2 = kat(p, d, b, "es1", sik), kat(p, d, b, "es2", sik)
                    if r1 is None:
                        continue
                    s.append(f"| {p} | {d} | {sik} | {b} | {int(r1['n'])} | {kt(r1)} | {kt(r2)} |")
    s += ["", "## (B) Zaman ve yön (S4 p15, eş 1 satırları)", "",
          "| Pazar | Dönem | sonuç | n | büyük hareketli | ilk gün medyan [%25-%75] | yukarı payı (eş) | 1-5 / 6-10 / 11-15 / 16-20 olay % (eş %) |", "|---|---|---|---|---|---|---|---|"]
    for r in B.to_dict("records"):
        fw = "f" if r["olcu"] == "B1" else "h"
        pen = " / ".join(f"{_sc_yz(r.get(f'p_{fw}{w}'))} ({_sc_yz(r.get(f'es_p_{fw}{w}'))})" for w in range(1, 5))
        s.append(f"| {r['pazar']} | {r['donem']} | {r['olcu']} | {r['n']} | {r['n_olay']} | {_sc_s(r.get('k_medyan'), 0)} [{_sc_s(r.get('k_q25'), 0)}-{_sc_s(r.get('k_q75'), 0)}] | "
                 f"{_sc_yz(r.get('yukari_pay'), 0)} ({_sc_yz(r.get('es_yukari_pay'), 0)}) | {pen} |")
    s += ["", "## (C) Yönsüz stoplu kırılım işlemi (SY (C) kuralı aynen; BİLGİ)", "",
          "| Pazar | Dönem | olay | işlem | işlem oranı | ort getiri | medyan | ort eş | ort fark [%95] | sıra | portföy / plasebo p90 | P(+%20 önce) / P(-%10 önce) (eş) | karar |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in C.to_dict("records"):
        s.append(f"| {r['pazar']} | {r['donem']} | {r['n_olay']} | {r['n']} | {_sc_yz(r.get('islem_orani'), 0)} | {_sc_yz(r.get('ort_r'))} | {_sc_yz(r.get('medyan_r'))} | "
                 f"{_sc_yz(r.get('ort_es_r'))} | {_sc_yz(r.get('ort_fark'))} [{_sc_yz(r.get('alt95'))}, {_sc_yz(r.get('ust95'))}] | {_sc_s(r.get('sira'))} | "
                 f"{_sc_yz(r.get('portfoy'), 0)} / {_sc_yz(r.get('port_es_p90'), 0)} | {_sc_yz(r.get('p_ilk20'), 0)} / {_sc_yz(r.get('p_ilk10'), 0)} "
                 f"({_sc_yz(r.get('es_p_ilk20'), 0)} / {_sc_yz(r.get('es_p_ilk10'), 0)}) | {r.get('karar')} |")
    if "oc" in J:
        s += ["", J["oc"]["rapor"]]
    s += ["", "## Geleceğe bakma denetimi (koşu içinde)", ""] + [f"- {p}: {v['gelecek_denetimi_olay']} olayda seri t'de kesildi, S4 / S1 / ATR / likidite aynı (TUTTU)"
                                                               for p, v in J["denetim"].items()]
    dy = _sc_yol("denetim", cikti)
    if os.path.exists(dy):
        Dn = json.load(open(dy, encoding="utf-8"))
        s += ["", "## Bağımsız denetim (koşudan sonra, ayrı kod)", ""] + [f"- {x}" for x in Dn.get("satirlar", [])]
    s += ["", "## Sınırlar", "", "- Evren bugünün listesi (V_*.pkl; OC'de ABD + k34): batan / kottan çıkan yok; büyük hareket olasılığı olay ve eşte birlikte etkilenir, "
          "işlem getirisi yukarı yanlı.", "- Bilanço takvimi yok. Komisyon / kayma / açığa satış maliyeti yok.",
          "- BIST ±%10 fiyat sınırı tek günlük büyük mumu kısar; BIST bilgi.", "- 31.08.2026 sonrası fiyat yok (fon krizi kesiği)."]
    metin = "\n".join(s)
    if _SC_EPOSTA.search(metin):
        raise SCHata("raporda e-posta biçimli parça var")
    with open(_sc_yol("rapor", cikti), "w", encoding="utf-8") as f:
        f.write(metin + "\n")
    return metin


# ---------------------------------------------------------------- 10) CEMAL'İN GÖZÜ İÇİN LİSTE (BIST, ekran fiyatı)
def _sc_bolge_satir(s: str, d: pd.DataFrame, X: pd.DataFrame, G: pd.DataFrame, i: int, p: int, supd: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """Liste satırı (gösterim; ölçüm değil). supd: bölünme / bedelsiz şüphesi günleri; sonraki 20 günde varsa g20 / uçlar gösterilmez (Yahoo bölünme kaydı eksik)."""
    C = d.Close.to_numpy(float); H = d.High.to_numpy(float); L = d.Low.to_numpy(float); ek = d.ekran.to_numpy(float)
    n = len(C); a = i - p + 1; b = min(n - 1, i + 20)
    Cp = np.r_[np.nan, C[:-1]]
    if i + 1 <= n - 1:
        rng_ = (H[i + 1:b + 1] - L[i + 1:b + 1]) / Cp[i + 1:b + 1]; j = int(np.argmax(rng_)); bm = float(rng_[j]); bt = d.index[i + 1 + j]
    else:
        bm, bt = float("nan"), None
    sik = float(np.mean((H[a:i + 1] - L[a:i + 1]) / C[a:i + 1]))
    return {"hisse": s, "bolge_bas": str(d.index[a].date()), "karar": str(d.index[i].date()), "bant_alt": float(np.min(ek[a:i + 1])),
            "bant_ust": float(np.max(ek[a:i + 1])), "bant": float(X.bant4.iat[i]), "sik_mum": sik, "bb_yuzdelik": float(X.bbr.iat[i]), "net": float(X.net.iat[i]),
            "en_buyuk_mum": bm, "en_buyuk_tarih": str(bt.date()) if bt is not None else "-", "kat_sik": bm / sik if sik > 0 else float("nan"),
            "kat_atr": bm / float(G.atr.iat[i]) if float(G.atr.iat[i]) > 0 else float("nan"),
            "g20": float(C[b] / C[i] - 1) if b > i else float("nan"), "gun_sonra": int(b - i),
            "en_yuksek": float(np.max(H[i + 1:b + 1]) / C[i] - 1) if b > i else float("nan"),
            "en_dusuk": float(np.min(L[i + 1:b + 1]) / C[i] - 1) if b > i else float("nan"),
            "bolunme_sonra": bool(supd is not None and b > i and supd[i + 1:b + 1].any())}


def _sc_bolge_md(R: List[Dict[str, Any]], tur: bool = False) -> List[str]:
    s = ["| hisse | " + ("tanım | " if tur else "") + "bolge_bas | karar | bant_alt | bant_ust | bant | sik_mum | BB yüzdelik | net kayma | en_buyuk_mum | kat_sik | kat_atr | g20 | en_yuksek | en_dusuk |",
         "|---|" + ("---|" if tur else "") + "---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        f = lambda x, k=1: "-" if x is None or not math.isfinite(x) else f"%{x * 100:+.{k}f}"   # noqa: E731
        u = lambda x, k=1: "-" if x is None or not math.isfinite(x) else f"%{x * 100:.{k}f}"    # noqa: E731
        g20 = f(r["g20"]) + ("" if r["gun_sonra"] >= 20 else f" ({r['gun_sonra']} gün)")
        if r.get("bolunme_sonra"):
            r = {**r, "en_yuksek": float("nan"), "en_dusuk": float("nan"), "en_buyuk_mum": float("nan"), "kat_sik": float("nan"), "kat_atr": float("nan")}
            g20 = "bedelsiz / bölünme şüphesi (Yahoo kaydı eksik; gösterilmez)"
        s.append(f"| {r['hisse']} | " + (f"{r.get('tur', '')} | " if tur else "") + f"{r['bolge_bas']} | {r['karar']} | {r['bant_alt']:.4g} | {r['bant_ust']:.4g} | {u(r['bant'])} | "
                 f"{u(r['sik_mum'])} | {r['bb_yuzdelik']:.2f} | {f(r['net'])} | {u(r['en_buyuk_mum'])} ({r['en_buyuk_tarih']}) | {_sc_s(r['kat_sik'], 1)} | "
                 f"{_sc_s(r['kat_atr'], 1)} | {g20} | {f(r['en_yuksek'])} | {f(r['en_dusuk'])} |")
    return s


def sc_liste(cikti: Optional[str] = None, yahoo: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """BIST 2025-01..2026-08 S4 (p15) bölgeleri, ekran fiyatı: rastgele 7 hisse x ardışık 3 bölge + 20 gün sonu en iyi / en kötü 10 + FENER S4 ve S1."""
    E = E or SC_ESIK; Ls = E["liste"]; p = E["S4"]["ana_pencere"]
    import TAVAN_SERISI as TS
    S, _m = TS.ts_fiyatlar(yahoo or SC_YOL["yahoo"])
    Dd, Xs, Gs, liq = {}, {}, {}, []
    for s_, d0 in S.items():
        try:
            d = _sc_yahoo_sy(d0)
            if len(d) < E["gecmis_min"] + 25:
                continue
            G = SY.sy_gecmis(d, "BIST", SY.SY_ESIK); X = sc_s4(d, "BIST", p, E)
            X["sup"] = SY._sy_pencere_var(SY.sy_bolunme_supheli(d.Close.to_numpy(float), SY.SY_ESIK), *E["bolunme_gecmis"])
            X["supd"] = SY.sy_bolunme_supheli(d.Close.to_numpy(float), SY.SY_ESIK, kati=True)   # gösterim: KATI (oran şartsız; Yahoo bedelli / bedelsiz kaydı eksik)
            Dd[s_], Xs[s_], Gs[s_] = d, X, G
            liq.append(pd.DataFrame({"sembol": s_, "tarih": d.index, "liq": G.liq.to_numpy()}))
        except Exception as ex:
            sclog.warning("liste %s atlandı: %s", s_, ex)
    Lq = pd.concat(liq, ignore_index=True); Lq["pct"] = Lq.groupby("tarih").liq.rank(pct=True)
    Lq = Lq.set_index(["sembol", "tarih"]).pct
    R: List[Dict[str, Any]] = []
    for s_, X in Xs.items():
        d = Dd[s_]
        for i in np.where(X.ev4.to_numpy())[0]:
            t = d.index[i]
            if not (pd.Timestamp(Ls["bas"]) <= t <= pd.Timestamp(Ls["son"])) or X.sup.iat[i]:
                continue
            lp = Lq.get((s_, t), np.nan)
            if not (np.isfinite(lp) and lp > SY.SY_ESIK["likidite"]["alt_kesik"]):
                continue
            R.append(_sc_bolge_satir(s_, d, X, Gs[s_], int(i), p, X.supd.to_numpy()))
    Rd = pd.DataFrame(R)
    rng = np.random.default_rng(Ls["tohum"])
    adaylar = sorted(Rd.groupby("hisse").size().loc[lambda x: x >= Ls["ardisik"]].index) if len(Rd) else []
    sec = list(rng.choice(adaylar, min(Ls["rastgele_hisse"], len(adaylar)), replace=False)) if adaylar else []
    A_ = [r for h in sec for r in sorted([r for r in R if r["hisse"] == h], key=lambda r: r["karar"])[:Ls["ardisik"]]]
    tam = [r for r in R if r["gun_sonra"] >= 20 and not r["bolunme_sonra"]]
    iyi = sorted(tam, key=lambda r: -r["g20"])[:Ls["en_iyi"]]; kotu = sorted(tam, key=lambda r: r["g20"])[:Ls["en_iyi"]]
    F_ = []
    fs = E["fener"]["sembol"]
    if fs in Dd:
        d, X, G = Dd[fs], Xs[fs], Gs[fs]
        for i in np.where(X.ev4.to_numpy())[0]:
            if d.index[i] >= pd.Timestamp("2025-01-01"):
                r = _sc_bolge_satir(fs, d, X, G, int(i), p, X.supd.to_numpy()); r["tur"] = "S4"; F_.append(r)
        ev1 = G.ev1.to_numpy().astype(bool)
        for i in np.where(ev1)[0]:
            if d.index[i] >= pd.Timestamp("2025-01-01"):
                r = _sc_bolge_satir(fs, d, X, G, int(i), 10, X.supd.to_numpy()); r["tur"] = "S1"
                a = int(i) - 9; r["bant"] = float((d.Close.iloc[a:i + 1].max() - d.Close.iloc[a:i + 1].min()) / d.Close.iloc[a:i + 1].min())
                r["net"] = float(d.Close.iat[i] / d.Close.iat[a] - 1); F_.append(r)
        F_.sort(key=lambda r: r["karar"])
    s = ["# Cemal tanımlı sıkışma (S4) bölgeleri (BIST, Ocak 2025 - Ağustos 2026) — Cemal'in kendi grafiğinde bakması için", "",
         "Tanım (S4, p = 15): karar gününe kadarki son 15 işlem günü (bölge = bolge_bas .. karar). (i) ortalama mum boyu (H-L)/C, önceki 250 günün 15 günlük "
         "ortalamalarının en küçük %20'sinde; (ii) Bollinger (20, 2σ) genişliği önceki 250 günün en dar %20'sinde; (iii) YATAY: ilk-son gün kapanış farkı "
         "<= %3, 15 günlük kapanış bandı <= %8, aşağı açılış günleri <= yarı; (iv) (i) ve (ii) en az 10 gündür sürüyor. Aynı hissede yeni bölge en az 20 gün "
         "sonra. Likidite alt %20 dışarıda. Fiyatlar ekran fiyatı.",
         "Sütunlar: bant_alt / bant_ust = 15 günün en düşük / en yüksek kapanışı; bant = (üst - alt) / alt; sik_mum = bölge günlerinin ortalama mum boyu "
         "(H-L)/C; BB yüzdelik = karar günü Bollinger genişliğinin son 250 gündeki sırası (0 = en dar); net kayma = karar / bolge_bas kapanışı - 1; "
         "en_buyuk_mum = sonraki 20 günün en büyük mumu (gün aralığı / önceki kapanış) ve tarihi; kat_sik = bu mumun sıkışma mumuna oranı; kat_atr = yıllık "
         "ortalama muma (ATR250) oranı; g20 = 20. gün kapanışı; en_yuksek / en_dusuk = 20 günde görülen uç (karar günü kapanışına göre).",
         f"Toplam bölge: {len(R)} ({len(set(r['hisse'] for r in R))} hisse); 20 günü tamamlanan ve sonraki 20 günde bedelsiz / bölünme şüphesi olmayan {len(tam)} "
         f"(şüpheli {sum(1 for r in R if r['bolunme_sonra'])}: Yahoo bölünme kaydı eksik olabilir, g20 gösterilmez).", "",
         f"## A. Rastgele {len(sec)} hisse (tohum {Ls['tohum']}; en az {Ls['ardisik']} bölgesi olanlardan), her birinde ARDIŞIK ilk {Ls['ardisik']} bölge ({len(A_)} satır)", ""]
    s += _sc_bolge_md(A_)
    s += ["", f"## B. 20 gün sonu getirisi EN İYİ {len(iyi)} (20 günü tamamlanan {len(tam)} bölge içinde)", ""] + _sc_bolge_md(iyi)
    s += ["", f"## C. 20 gün sonu getirisi EN KÖTÜ {len(kotu)}", ""] + _sc_bolge_md(kotu)
    s += ["", "## D. FENER karşılaştırma: bütün S4 ve S1 bölgeleri (2025-26)", "",
          "S1 satırlarında bölge 10 gün, bant / net 10 günden; S1 likidite / bölünme filtresi uygulanmadan, kodun eski seçimi olduğu gibi.", ""] + _sc_bolge_md(F_, tur=True)
    s += ["", "Not: liste ölçüm değildir; seçici değil, Cemal'in gözle kıyası içindir. Hayatta kalma: yalnız bugün işlem gören hisseler."]
    metin = "\n".join(s)
    if _SC_EPOSTA.search(metin):
        raise SCHata("listede e-posta biçimli parça var")
    yol = _sc_yol("liste", cikti)
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin + "\n")
    sclog.info("liste yazıldı: %s (%d bölge)", yol, len(R))
    return yol


# ---------------------------------------------------------------- 11) ÇAKIŞMA KAPISI
def _cakisma_kontrol_sc(_once=_CK_ONCE_SC, _dosya="SIKISMA_CEMAL.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_SC", "_CK_KAYIT", "_cakisma_kontrol_sc", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "subprocess", "zlib", "warnings", "_dt", "OC", "SY",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_sc()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=SC_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "liste", "fener"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true", help="onkayit: git'e İŞLENMEMİŞ ön kaydı yeniden yaz")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(sc_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            R_ = sc_kos(a.cikti, a.veri)
            print(json.dumps(_sc_temiz(R_["sonuc"]["karar"]), ensure_ascii=False, indent=1))
        elif a.komut == "liste":
            print(sc_liste(a.cikti))
        elif a.komut == "fener":
            print("\n".join(_sc_fener_md(sc_fener(veri=a.veri))))
        else:
            print(sc_rapor(a.cikti))
    except (SCHata, OC.OCHata) as ex:
        sclog.error("%s", ex); sys.exit(1)
