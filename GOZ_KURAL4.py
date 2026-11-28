"""GOZ_KURAL4 — KURAL-4: beş işaretli kör setten (GT1, GT3, GT4, GT5, GT9) SETE GÖRE DIŞARIDA sınanmış tespit (kabul) kuralı var mı (28 Kasım 2026).

İş tanımı: arastirma_cikti/goz_tespit/GT10_IS_TANIMI.md (ana model). Bu iş YALNIZ TESPİT içindir: hiçbir sayfanın / bölgenin sonrası, getirisi
hesaplanmaz, okunmaz. Etiket = Cemal'in dört kutusu (sinif4: EVET / KISMEN / ERKEN / HAYIR).
  tablo   : beş setin işaretli sayfaları + sayfa başına ölçüler (goz2/uc_set.olc AYNEN, import; + 4 yeni ölçü) + KURAL-3 bayrağı (D1 + YER + ZAMAN)
            -> arastirma_cikti/goz_tespit/gt10_tablo.json (etiket - ölçü ilişkisi HESAPLANMAZ; yalnız sayım)
  onkayit : GT10_ON_KAYIT.md taslağının sayım bölümü (set x sınıf, set x kol, ölçü eksikleri, kod / eşik sha) -> stdout
  kos     : (kapı: GT10_ON_KAYIT.md commit + push + IZ_KARNE.ik_kontrol_kapisi; BİR KEZ) set dışı sınama (A tek ölçü, B <= 3 şartlı VE, C L2 lojistik
            <= 4 ölçü; bazlar KURAL-3 ve hepsini kabul) + set içi etiket karıştırma + sayfa bootstrap + H2 (✓ - erken tek ölçü AUC) -> gt10_ozet.json
  olay    : seçilen kural (geçen yoksa EN İYİ ADAY) beş setle yeniden kurulur -> gt10_kural4.json; KURAL-3'ün D1 havuzuna (ABD + BIST; 2016-22)
            uygulanır -> /root/.kasa/ham/goz_tespit/k4/k4_olay.pkl (getirisiz) + sayım gt10_ozet.json'a
  rapor   : GT10_RAPOR.md (gt10_ozet.json'dan)
Mevcut modüller DEĞİŞTİRİLMEZ; içe alınır: goz2/uc_set (olc, veri, auc), GOZ_TESPIT (pencere paneli, D1 sırası, olay evreni, tekilleştirme), MUM_IZI.
Veri: açık kopya <= 2022-12-31 (assert); kitaplık sayfaları (kaynak 'tam') bölge bitişinde kesilir (uc_set.tablo ile aynı).
Colab:  exec(open('GOZ_KURAL4.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_GK4 = {k: id(v) for k, v in globals().items()}

import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_GK4 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
_GK4_GOZ2 = os.path.join(KOK_GK4, "arastirma_cikti", "goz_tespit", "goz2")
for _p in (KOK_GK4, _GK4_GOZ2):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import uc_set as U  # noqa: E402  (DEĞİŞTİRİLMEZ; olc / veri / auc; k1.py import EDİLMEZ)
logging.disable(logging.NOTSET)   # uc_set içe alınırken INFO'yu genel kapatır; bu modülün günlüğü için geri açılır
import GOZ_TESPIT as GT  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)

gk4log = logging.getLogger("col.goz_kural4")
if not gk4log.handlers:
    _gk4_h = logging.StreamHandler(sys.stderr)
    _gk4_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s goz_kural4: %(message)s", "%H:%M:%S"))
    gk4log.addHandler(_gk4_h)
    gk4log.setLevel(logging.INFO)
    gk4log.propagate = False


class GK4Hata(RuntimeError):
    """Durdurucu hata: kapı / kesik / sayım / şema / ikinci koşu."""


GK4_SURUM = "GOZ_KURAL4 v1.0 (2026-11-28): beş işaretli setten sete göre dışarıda sınanmış kabul kuralı (yalnız tespit; getiri yok)"
GK4_YOL = {"cikti": os.path.join(KOK_GK4, "arastirma_cikti", "goz_tespit"), "kod": os.path.join(KOK_GK4, "GOZ_KURAL4.py"),
           "ham": os.path.join(GT.GT_YOL["ham"], "k4")}
GK4_DOSYA = {"tablo": "gt10_tablo.json", "onkayit": "GT10_ON_KAYIT.md", "ozet": "gt10_ozet.json", "kural": "gt10_kural4.json", "rapor": "GT10_RAPOR.md",
             "olay_pkl": "k4_olay.pkl", "kilit": "kos_kilit.json"}

GK4: Dict[str, Any] = {
    "surum": "K4-1.0 (2026-11-28)",
    "setler": [["GT1", "GT_onay_anahtar.json", "cemal_gt_onay.json"], ["GT3", "GT3_onay_anahtar.json", "cemal_gt3_onay.json"],
               ["GT4", "GT4_onay_anahtar.json", "cemal_gt4_onay.json"], ["GT5", "GT5_onay_anahtar.json", "cemal_gt5_onay.json"],
               ["GT9", "GT9_onay_anahtar.json", "cemal_gt9_onay.json"]],
    # İş tanımı 30 + 28 + 20 + 21 + 23 = 122 bekliyordu; GT3 anahtarı ve işaret dosyası 32 sayfa (D1 24 + RASTGELE 4 + KİTAPLIK 4; Ç268 '32 sayfa'):
    # gerçek toplam 126. Ön kayıtta SAPMA olarak yazıldı (ölçümden önce).
    "beklenen": {"GT1": 30, "GT3": 32, "GT4": 20, "GT5": 21, "GT9": 23}, "toplam": 126,
    "sinif": ["EVET", "KISMEN", "ERKEN", "HAYIR"], "rastgele_kol": "RASTGELE", "kitaplik_kol_bas": "KITAPLIK",
    "yeni_olcu": ["YENI_DIP_SON", "ALT_FITIL_SON10", "EGIM_FARK", "SON_BOY_ORAN"],
    "A": {"yuzdelik": [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90], "en_az_kabul_egitim": 20, "z": 1.96},
    "B": {"en_cok_sart": 3},
    "C": {"en_cok_olcu": 4, "lam": 1.0, "rho_ust": 0.80, "hedef_pay": 0.70, "en_az_kabul_egitim": 20, "newton_tur": 100},
    "karistirma": {"B": 1000, "tohum": 1028}, "boot": {"B": 2000, "tohum": 10},
    "karar": {"kabul_en_az": 25, "set_en_az": 4, "evet_pay": 0.70, "erken_pay": 0.20, "rastgele_en_cok": 1, "k3_fark": 0.10, "karistirma_q": 0.95},
    "H2": {"auc": 0.70, "set_en_az": 4, "karistirma_B": 1000},
    "K3": {"D1": 0.90, "dipten_bar": 0.5},
    "olay": {"pazar": ["ABD", "BIST"], "tekil": 40, "bas": "2016-01-01", "son": "2022-12-31", "donem": {"d1619": ["2016-01-01", "2019-12-31"],
                                                                                                         "d2022": ["2020-01-01", "2022-12-31"]}},
    "tanim": {
        "olcu": "goz2/uc_set.olc(d, s, t) çıktısının bütün sayısal alanları (35) + 4 yeni ölçü; d açık kopyada tam seri (olc yalnız <= t okur: testle), "
                "kitaplıkta bölge bitişinde kesik",
        "YENI_DIP_SON": "bölgenin son üçte birindeki (en az 3 bar) barlardan Low'u bölgede o bara kadarki bütün Low'lardan küçük olanların payı "
                        "('daha derin dip yok' => küçük)",
        "ALT_FITIL_SON10": "son 10 barın (H > L olanlar) (min(O, C) - L) / (H - L) ortalaması ('dip savunması'); geçerli bar yoksa boş",
        "EGIM_FARK": "son üçte bir kapanış eğimi - ilk üçte bir kapanış eğimi (bar başına, kutu yüksekliği x üçte bir uzunluk biriminde) "
                     "('düşüş bitmeli / yuvarlanma' => büyük)",
        "SON_BOY_ORAN": "son 10 barın medyan (H - L)'si / bölgenin medyan (H - L)'si ('küçük mum' sonda); bölge medyanı 0 ise boş",
        "K3": "KURAL-3 = D1 (PUAN_ESIT pazar + L içi evren sırası >= 0,90; GOZ_TESPIT.gt_k3_d1_sira, pencere panelinden (sembol, s, t, L) ile) VE Y = 1 "
              "VE DIPTEN_BAR >= 0,5; panelde olmayan sayfa (kitaplık, panel dışı pencere) D1 değil",
        "A": "tek ölçü + yön (>= / <=) + eşik; aday eşikler = eğitim sayfalarının sonlu değerlerinin %10, 15, ..., 90 yüzdelikleri; amaç = kabul içinde "
             "✓ payının Wilson %95 alt ucu, eğitimde kabul >= 20 sayfa; eşitlikte çok kabul, sonra ölçü sırası; boş değer şartı sağlamaz",
        "B": "ileri seçim: ilk şart = A'nın seçtiği; her adımda (en çok 3 şart) A'nın aday şartlarından (aynı ölçü ikinci kez yok) VE ile eklenince "
             "amaç (Wilson alt ucu, eğitim kabulü >= 20) en çok artanı; artış yoksa durur",
        "C": "L2 lojistik (ceza lam = 1 standart katsayılarda; sabit cezasız; Newton); ölçü seçimi eğitimde: EVET - öteki AUC'sinin |AUC - 0,5|'ine göre "
             "sıralı, Spearman |rho| > 0,80 olan atlanır, ilk 4; boşlar eğitim medyanıyla doldurulur, eğitim ort / sd ile standart; kabul eşiği = eğitim "
             "skorlarında kabul >= 20 ve ✓ payı >= %70 veren EN DÜŞÜK skor; yoksa kural hiçbir sayfayı kabul etmez",
        "set_disi": "5 kat: her set bir kez sınama, kalan dört set eğitim; bütün seçimler (ölçü, yön, eşik, şart sayısı, C ölçüleri ve eşiği) yalnız eğitimde",
        "karistirma": "etiketler (sinif4) SET İÇİNDE karıştırılır (1.000 kez), bütün hat (A, B, C + en iyiyi seçme) yeniden koşar; istatistik T = set dışı "
                      "kabulü >= 25 olan ailelerin en büyük havuzlanmış set dışı ✓ payı (yoksa havuz ✓ payı); bir ailenin ✓ payı karıştırma T'sinin "
                      "%95'inin üstünde olmalı",
        "boot": "sayfa düzeyi bootstrap (2.000; 126 sayfa yerine koyarak; set dışı kabul kararı sabit): kabul içinde ✓ payının %2,5 / %97,5'i",
        "H2": "yalnız kodun seçtiği sayfalar (kol RASTGELE ve KITAPLIK* değil) ve sinif4 EVET / ERKEN; her ölçü için her katta yön eğitim AUC'sinden "
              "(>= 0,5 ise olduğu gibi, değilse ters), sınama setinin yönlü değerleri havuzlanır, havuz AUC (EVET > ERKEN); set set yön = o setin ham "
              "AUC'si bütün veri yönüyle aynı tarafta mı (0,5 eşit sayılmaz); ADAY <=> havuz AUC >= 0,70 ve >= 4 sette aynı yön; karıştırma (set "
              "içi EVET / ERKEN, 1.000): en büyük havuz AUC'nin %95'i BİLGİ",
        "en_iyi_aday": "karar geçen aile varsa EN BASİTİ (A < B < C); yoksa set dışı kabul >= 25 ailelerden en yüksek ✓ payı; o da yoksa en yüksek set "
                       "dışı Wilson alt ucu (kabul >= 1); açıkça 'EN İYİ ADAY (karar geçmedi)' adıyla",
        "olay": "seçilen aile beş setin tamamıyla aynı yöntemle yeniden kurulur; havuz = GOZ_TESPIT.gt_k2_evren (pencere sonu 2016-2022, s >= 120, KIL "
                "<= 0,20, gövdesiz pay <= 0,30) ∩ D1 (gt_k3_d1_sira >= 0,90), ABD + BIST; her pencerede gk4_olc; kabul edilenler hisse başına "
                "gt_k2_tekil(bar = 40); KURAL-3 bayrağı = k3/k3_aday.pkl'da ANA = 1; gosterildi = beş setteki aynı pazar + sembol açık veri sayfası "
                "ile [s, t] kesişiyor; dönem pencere sonu tarihine göre"},
}
_GK4_DURUM = {"kapi": False}
GK4_AILE = ["A", "B", "C"]


# ================================================================ 0) YARDIMCI
def _gk4_yol(ad: str, cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    if ad.endswith("_pkl") or ad == "kilit":
        return os.path.join(ham or GK4_YOL["ham"], GK4_DOSYA[ad])
    return os.path.join(cikti or GK4_YOL["cikti"], GK4_DOSYA[ad])


def gk4_esik_sha() -> str:
    return hashlib.sha256(json.dumps(GK4, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def gk4_kod_sha() -> str:
    return MI._mi_sha(GK4_YOL["kod"])


def _gk4_git(args: List[str]) -> str:
    try:
        return subprocess.run(["git"] + args, cwd=KOK_GK4, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as ex:   # git yoksa kapı düşer (fail-closed)
        gk4log.warning("git çalışmadı: %s", ex)
        return ""


def gk4_kapi_commit(yol: str, ad: str) -> str:
    """yol commit edilmiş, çalışma kopyası HEAD ile aynı ve uzak dalda (push) olmalı."""
    rel = os.path.relpath(yol, KOK_GK4)
    if not os.path.exists(yol):
        raise GK4Hata(f"kapı: {ad} yok ({rel})")
    c = _gk4_git(["log", "-1", "--format=%H", "--", rel])
    if not c:
        raise GK4Hata(f"kapı: {ad} commit edilmemiş")
    if _gk4_git(["status", "--porcelain", "--", rel]):
        raise GK4Hata(f"kapı: {ad} commit'ten sonra değişmiş")
    if not _gk4_git(["branch", "-r", "--contains", c]):
        raise GK4Hata(f"kapı: {ad} commit'i ({c[:10]}) push edilmemiş")
    return c


def _gk4_kesik(V: Dict[str, pd.DataFrame], ad: str) -> None:
    mx = max((d.index.max() for d in V.values() if len(d)), default=pd.Timestamp("1900-01-01"))
    if mx > pd.Timestamp(GK4["olay"]["son"]):
        raise GK4Hata(f"KESİK: {ad} verisi {mx.date()} > {GK4['olay']['son']}")


# ================================================================ 1) ÖLÇÜLER (<= t)
def gk4_yeni_olcu(d: pd.DataFrame, s: int, t: int) -> Dict[str, float]:
    """4 yeni ölçü; yalnız s..t barları okunur."""
    O, H, L, C = (d[c].to_numpy(float)[s:t + 1] for c in ("Open", "High", "Low", "Close"))
    n = len(C); kutu = float(H.max() - L.min()); u = max(3, n // 3); o: Dict[str, float] = {}
    onceki_min = np.minimum.accumulate(np.r_[np.inf, L[:-1]])        # her bar için bölgede o bara kadarki en düşük Low (kendisi hariç)
    yeni = L < onceki_min; yeni[0] = False
    o["YENI_DIP_SON"] = float(yeni[-u:].mean())
    h10, l10, o10, c10 = H[-10:], L[-10:], O[-10:], C[-10:]; g = h10 > l10
    o["ALT_FITIL_SON10"] = float(((np.minimum(o10, c10) - l10)[g] / (h10 - l10)[g]).mean()) if g.any() else np.nan
    if kutu > 0 and n >= 6:
        e1 = np.polyfit(np.arange(u), C[:u], 1)[0]; e2 = np.polyfit(np.arange(u), C[-u:], 1)[0]
        o["EGIM_FARK"] = float((e2 - e1) * u / kutu)
    else:
        o["EGIM_FARK"] = np.nan
    mb = float(np.median(H - L))
    o["SON_BOY_ORAN"] = float(np.median(h10 - l10) / mb) if mb > 0 else np.nan
    return o


def gk4_olc(d: pd.DataFrame, s: int, t: int) -> Dict[str, float]:
    """uc_set.olc AYNEN (import) + 4 yeni ölçü."""
    o = dict(U.olc(d, int(s), int(t)))
    o.update(gk4_yeni_olcu(d, int(s), int(t)))
    return o


def gk4_olcu_ad(T: pd.DataFrame) -> List[str]:
    """Tablodaki ölçü sütunları (sayfa / etiket / kimlik sütunları hariç)."""
    dis = {"set", "sayfa", "kol", "pazar", "kaynak", "sembol", "s", "t", "L", "cemal", "D1_sira", "K3", "kitaplik_no", "son"}
    return [c for c in T.columns if c not in dis and pd.api.types.is_numeric_dtype(T[c])]


# ================================================================ 2) SAYFALAR ve TABLO
def gk4_sayfalar(cikti: Optional[str] = None) -> pd.DataFrame:
    """Beş setin işaretli sayfaları (ölçüsüz). Sayım beklenenden farklıysa DURUR."""
    C = cikti or GK4_YOL["cikti"]; R = []
    for ad, anahtar, isaret in GK4["setler"]:
        A = json.load(open(os.path.join(C, anahtar), encoding="utf-8"))["sayfalar"]
        S4 = json.load(open(os.path.join(C, isaret), encoding="utf-8"))["sinif4"]
        bilinmeyen = set(S4.values()) - set(GK4["sinif"])
        if bilinmeyen:
            raise GK4Hata(f"K10: {ad} bilinmeyen sınıf {bilinmeyen}")
        sayfa_no = {str(r["sayfa"]) for r in A}
        if set(S4) - sayfa_no:
            raise GK4Hata(f"K10: {ad} işarette anahtarda olmayan sayfa {sorted(set(S4) - sayfa_no)}")
        for r in A:
            k = str(r["sayfa"])
            if k not in S4:
                continue                                                   # işaretsiz (GT9 s. 1): dışarıda
            R.append({"set": ad, "sayfa": int(r["sayfa"]), "kol": r["kol"], "pazar": r["pazar"], "kaynak": r.get("kaynak", "acik"), "sembol": r["sembol"],
                      "s": int(r["s"]), "t": int(r["t"]), "L": int(r["L"]), "kitaplik_no": r.get("kitaplik_no"), "cemal": S4[k]})
    P = pd.DataFrame(R)
    say = P.groupby("set").size().to_dict()
    if say != GK4["beklenen"] or len(P) != int(GK4["toplam"]):
        raise GK4Hata(f"SAYIM: {say} (toplam {len(P)}) beklenen {GK4['beklenen']} ({GK4['toplam']})")
    return P


def gk4_d1_sayfa(P: pd.DataFrame, ham: Optional[str] = None) -> np.ndarray:
    """Sayfaların D1 sırası (GOZ_TESPIT.gt_k3_d1_sira; pencere paneli, anahtar (sembol, s, t, L)); panelde yoksa NaN. Getirisiz."""
    out = np.full(len(P), np.nan)
    for p in sorted(P.pazar.unique()):
        X = GT.gt_yukle(p, ham); X["D1_sira"] = GT.gt_k3_d1_sira(X)
        key = X.drop_duplicates(["sembol", "s", "t", "L"]).set_index(["sembol", "s", "t", "L"]).D1_sira
        for i in np.flatnonzero((P.pazar == p).to_numpy() & (P.kaynak == "acik").to_numpy()):
            r = P.iloc[i]; k = (r.sembol, int(r.s), int(r.t), int(r.L))
            if k in key.index:
                out[i] = float(key.loc[k])
        del X, key
    return out


def gk4_k3_bayrak(T: pd.DataFrame) -> np.ndarray:
    d1 = np.asarray(T.D1_sira, float)
    with np.errstate(invalid="ignore"):
        return (np.isfinite(d1) & (d1 >= float(GK4["K3"]["D1"])) & (T.Y.to_numpy(float) == 1)
                & (T.DIPTEN_BAR.to_numpy(float) >= float(GK4["K3"]["dipten_bar"])))


def gk4_tablo(cikti: Optional[str] = None, ham: Optional[str] = None) -> pd.DataFrame:
    """126 sayfa x ölçü + D1_sira + K3 -> gt10_tablo.json. Etiket - ölçü ilişkisi hesaplanmaz."""
    t0 = time.time(); P = gk4_sayfalar(cikti)
    KT = {r["no"]: r for r in json.load(open(os.path.join(GT.GT_YOL["ham"], "kitaplik_olcu.json"), encoding="utf-8")) if r["durum"] == "tamam"}
    O = []
    for r in P.itertuples():
        V = U.veri(r.pazar, r.kaynak)
        if r.kaynak == "acik":
            _gk4_kesik(V, f"{r.pazar} açık")
        d = V[r.sembol]
        if r.kaynak == "tam":
            d = d[d.index <= pd.Timestamp(KT[r.kitaplik_no]["bit"])]
        if r.t >= len(d):
            raise GK4Hata(f"K10: {r.set} s.{r.sayfa} t={r.t} seride yok")
        O.append(gk4_olc(d.iloc[:r.t + 1], r.s, r.t))                    # t sonrası verilmez
    T = pd.concat([P.reset_index(drop=True), pd.DataFrame(O)], axis=1)
    T["D1_sira"] = gk4_d1_sayfa(T, ham); T["K3"] = gk4_k3_bayrak(T).astype(int)
    MI._mi_jyaz(_gk4_yol("tablo", cikti), {"surum": GK4_SURUM, "kod_sha": gk4_kod_sha(), "esik_sha": gk4_esik_sha(),
                                           "not": "GETİRİSİZ; etiket - ölçü ilişkisi bu dosyada hesaplanmadı", "satir": T.to_dict("records")}, "gt10 tablo")
    gk4log.info("tablo: %d sayfa, %d ölçü (%.0f sn)", len(T), len(gk4_olcu_ad(T)), time.time() - t0)
    return T


def gk4_tablo_oku(cikti: Optional[str] = None) -> pd.DataFrame:
    J = json.load(open(_gk4_yol("tablo", cikti), encoding="utf-8"))
    T = pd.DataFrame(J["satir"])
    for c in gk4_olcu_ad(T) + ["D1_sira"]:
        T[c] = pd.to_numeric(T[c], errors="coerce").astype(float)
    if len(T) != int(GK4["toplam"]):
        raise GK4Hata(f"SAYIM: tablo {len(T)} satır")
    return T


# ================================================================ 3) KURAL AİLELERİ
def gk4_wilson(k: np.ndarray, n: np.ndarray, z: float = 1.96) -> np.ndarray:
    k = np.asarray(k, float); n = np.asarray(n, float); out = np.full(np.broadcast(k, n).shape, -np.inf)
    m = n > 0
    p = np.where(m, k / np.where(m, n, 1), 0.0); nn = np.where(m, n, 1)
    lb = (p + z * z / (2 * nn) - z * np.sqrt(p * (1 - p) / nn + z * z / (4 * nn * nn))) / (1 + z * z / nn)
    out[m] = lb[m]
    return out


def gk4_aday_sart(X: np.ndarray) -> List[Tuple[int, str, float]]:
    """A / B aday şartları: her ölçü için eğitim yüzdelikleri x iki yön."""
    S = []
    for j in range(X.shape[1]):
        x = X[:, j]; f = np.isfinite(x)
        if f.sum() < 5:
            continue
        for q in np.unique(np.percentile(x[f], GK4["A"]["yuzdelik"])):
            S.append((j, ">=", float(q))); S.append((j, "<=", float(q)))
    return S


def gk4_sart_mat(X: np.ndarray, S: List[Tuple[int, str, float]]) -> np.ndarray:
    if not S:
        return np.zeros((len(X), 0), bool)
    j = np.array([s[0] for s in S]); q = np.array([s[2] for s in S]); b = np.array([s[1] == ">=" for s in S])
    V = X[:, j]
    with np.errstate(invalid="ignore"):
        M = np.where(b[None, :], V >= q[None, :], V <= q[None, :])
    return M & np.isfinite(V)


def _gk4_en_iyi(M: np.ndarray, y: np.ndarray, maske: Optional[np.ndarray] = None) -> Tuple[int, float]:
    """Amaç: kabul içinde y payının Wilson alt ucu (kabul >= en az). Eşitlikte çok kabul, sonra sıra. -1: yok."""
    if maske is not None:
        M = M & maske[:, None]
    n = M.sum(0); k = (M & y[:, None]).sum(0); lb = gk4_wilson(k, n, GK4["A"]["z"])
    lb[n < int(GK4["A"]["en_az_kabul_egitim"])] = -np.inf
    if not len(lb) or not np.isfinite(lb).any():
        return -1, -np.inf
    en = lb.max(); aday = np.flatnonzero(lb == en); i = aday[np.argmax(n[aday])]          # argmax ilk görüleni verir
    return int(i), float(en)


def gk4_kur_A(X: np.ndarray, y: np.ndarray, ad: List[str]) -> Dict[str, Any]:
    S = gk4_aday_sart(X); M = gk4_sart_mat(X, S); i, lb = _gk4_en_iyi(M, y)
    if i < 0:
        return {"aile": "A", "sart": [], "bos": True}
    j, yon, q = S[i]
    return {"aile": "A", "sart": [{"olcu": ad[j], "yon": yon, "esik": q}], "egitim_lb": lb, "bos": False}


def gk4_kur_B(X: np.ndarray, y: np.ndarray, ad: List[str]) -> Dict[str, Any]:
    S = gk4_aday_sart(X); M = gk4_sart_mat(X, S); i, lb = _gk4_en_iyi(M, y)
    if i < 0:
        return {"aile": "B", "sart": [], "bos": True}
    sec = [i]; cur = M[:, i].copy(); kul = {S[i][0]}
    while len(sec) < int(GK4["B"]["en_cok_sart"]):
        uy = np.array([S[c][0] not in kul for c in range(len(S))])
        M2 = M & uy[None, :]
        i2, lb2 = _gk4_en_iyi(M2, y, cur)
        if i2 < 0 or not lb2 > lb:
            break
        sec.append(i2); cur &= M[:, i2]; kul.add(S[i2][0]); lb = lb2
    return {"aile": "B", "sart": [{"olcu": ad[S[c][0]], "yon": S[c][1], "esik": S[c][2]} for c in sec], "egitim_lb": lb, "bos": False}


def gk4_lojistik(Z: np.ndarray, y: np.ndarray, lam: float, tur: int) -> np.ndarray:
    """L2 lojistik (Newton); sabit cezasız. w[0] sabit."""
    n, k = Z.shape; A = np.c_[np.ones(n), Z]; w = np.zeros(k + 1); Pn = lam * np.eye(k + 1); Pn[0, 0] = 0.0
    for _ in range(int(tur)):
        p = 1.0 / (1.0 + np.exp(-np.clip(A @ w, -30, 30))); g = A.T @ (p - y) + Pn @ w
        Hs = A.T @ (A * (p * (1 - p))[:, None]) + Pn + 1e-9 * np.eye(k + 1)
        d = np.linalg.solve(Hs, g); w -= d
        if np.max(np.abs(d)) < 1e-9:
            break
    return w


def _gk4_spearman(a: np.ndarray, b: np.ndarray) -> float:
    f = np.isfinite(a) & np.isfinite(b)
    if f.sum() < 5:
        return 0.0
    ra = pd.Series(a[f]).rank().to_numpy(); rb = pd.Series(b[f]).rank().to_numpy()
    if ra.std() == 0 or rb.std() == 0:
        return 0.0
    return float(np.corrcoef(ra, rb)[0, 1])


def gk4_kur_C(X: np.ndarray, y: np.ndarray, ad: List[str]) -> Dict[str, Any]:
    E = GK4["C"]; sira = []
    for j in range(X.shape[1]):
        x = X[:, j]; f = np.isfinite(x)
        if f.sum() < 10 or np.nanstd(x) == 0:
            continue
        a = U.auc(x[f & (y == 1)], x[f & (y == 0)])
        if np.isfinite(a):
            sira.append((abs(a - 0.5), -j, j))
    sira.sort(reverse=True); sec: List[int] = []
    for _, _, j in sira:
        if all(abs(_gk4_spearman(X[:, j], X[:, k])) <= float(E["rho_ust"]) for k in sec):
            sec.append(j)
        if len(sec) >= int(E["en_cok_olcu"]):
            break
    if not sec:
        return {"aile": "C", "bos": True, "olcu": []}
    Xs = X[:, sec]; med = np.nanmedian(Xs, 0); Xi = np.where(np.isfinite(Xs), Xs, med[None, :]); ort = Xi.mean(0); sd = Xi.std(0); sd[sd == 0] = 1.0
    Z = (Xi - ort) / sd; w = gk4_lojistik(Z, y.astype(float), float(E["lam"]), int(E["newton_tur"]))
    sk = 1.0 / (1.0 + np.exp(-np.clip(np.c_[np.ones(len(Z)), Z] @ w, -30, 30)))
    o = np.argsort(-sk, kind="mergesort"); sks = sk[o]; ys = y[o]; cn = np.arange(1, len(sk) + 1); ck = np.cumsum(ys)
    # eşik = sks[i]; kabul = sk >= sks[i] (eşitler dahil): eşit skorların son konumunda değerlendirilir
    son = np.r_[sks[1:] != sks[:-1], True]
    uy = son & (cn >= int(E["en_az_kabul_egitim"])) & (ck / cn >= float(E["hedef_pay"]))
    esik = float(sks[np.flatnonzero(uy)].min()) if uy.any() else np.inf
    return {"aile": "C", "bos": not np.isfinite(esik), "olcu": [ad[j] for j in sec], "medyan": med.tolist(), "ort": ort.tolist(), "sd": sd.tolist(),
            "w": w.tolist(), "esik": esik}


def gk4_uygula(K: Dict[str, Any], T: pd.DataFrame) -> np.ndarray:
    """Kuralı bir tabloya uygula (boş değer şartı sağlamaz; C'de eğitim medyanıyla doldurulur)."""
    n = len(T)
    if K.get("bos"):
        return np.zeros(n, bool)
    if K["aile"] in ("A", "B"):
        m = np.ones(n, bool)
        for s in K["sart"]:
            x = T[s["olcu"]].to_numpy(float)
            with np.errstate(invalid="ignore"):
                m &= np.isfinite(x) & ((x >= s["esik"]) if s["yon"] == ">=" else (x <= s["esik"]))
        return m
    Xs = T[K["olcu"]].to_numpy(float); med = np.asarray(K["medyan"]); Xi = np.where(np.isfinite(Xs), Xs, med[None, :])
    Z = (Xi - np.asarray(K["ort"])) / np.asarray(K["sd"]); sk = 1.0 / (1.0 + np.exp(-np.clip(np.c_[np.ones(n), Z] @ np.asarray(K["w"]), -30, 30)))
    return sk >= float(K["esik"])


_GK4_KUR = {"A": gk4_kur_A, "B": gk4_kur_B, "C": gk4_kur_C}


def gk4_kur(aile: str, T: pd.DataFrame, y: np.ndarray, ad: List[str]) -> Dict[str, Any]:
    return _GK4_KUR[aile](T[ad].to_numpy(float), np.asarray(y, int), ad)


# ================================================================ 4) SET DIŞI HAT
def gk4_hat(T: pd.DataFrame, y: np.ndarray, ad: List[str], kural_yaz: bool = False) -> Dict[str, Any]:
    """5 kat set dışı: her aile için set dışı kabul vektörü (126) + (istenirse) kat kuralları."""
    st = T["set"].to_numpy(); y = np.asarray(y, int); out: Dict[str, Any] = {a: np.zeros(len(T), bool) for a in GK4_AILE}
    if kural_yaz:
        out["kural"] = {a: {} for a in GK4_AILE}
    for g in pd.unique(st):
        te = st == g; tr = ~te; Ttr = T[tr]; Tte = T[te]
        for a in GK4_AILE:
            K = gk4_kur(a, Ttr, y[tr], ad); out[a][te] = gk4_uygula(K, Tte)
            if kural_yaz:
                out["kural"][a][g] = K
    return out


def gk4_istatistik(acc: Dict[str, np.ndarray], y: np.ndarray) -> float:
    """T = set dışı kabulü >= 25 ailelerin en büyük ✓ payı; yoksa havuz ✓ payı."""
    y = np.asarray(y, bool); v = [y[acc[a]].mean() for a in GK4_AILE if acc[a].sum() >= int(GK4["karar"]["kabul_en_az"])]
    return float(max(v)) if v else float(y.mean())


def gk4_karistir(T: pd.DataFrame, c4: np.ndarray, B: int, tohum: int, ad: List[str]) -> Dict[str, Any]:
    """Set içi etiket karıştırma; bütün hat yeniden; T dağılımı + aile ✓ payları."""
    rng = np.random.default_rng(int(tohum)); st = T["set"].to_numpy(); c4 = np.asarray(c4); Ts = []; Fa = {a: [] for a in GK4_AILE}; t0 = time.time()
    gruplar = [np.flatnonzero(st == g) for g in pd.unique(st)]
    for b in range(int(B)):
        c = c4.copy()
        for ii in gruplar:
            c[ii] = c4[ii][rng.permutation(len(ii))]
        y = (c == "EVET").astype(int); acc = gk4_hat(T, y, ad); Ts.append(gk4_istatistik(acc, y))
        for a in GK4_AILE:
            Fa[a].append(float(y[acc[a]].mean()) if acc[a].any() else np.nan)
        if (b + 1) % 100 == 0:
            gk4log.info("karıştırma %d / %d (%.0f sn)", b + 1, B, time.time() - t0)
    Ts = np.array(Ts)
    return {"B": int(B), "tohum": int(tohum), "T": Ts.tolist(), "q95": float(np.quantile(Ts, float(GK4["karar"]["karistirma_q"]))),
            "aile_pay": Fa, "sure_sn": time.time() - t0}


def gk4_boot(acc: np.ndarray, evet: np.ndarray, B: int, tohum: int) -> List[Optional[float]]:
    rng = np.random.default_rng(int(tohum)); n = len(acc); v = []
    for _ in range(int(B)):
        i = rng.integers(0, n, n); a = acc[i]
        if a.any():
            v.append(float(evet[i][a].mean()))
    if not v:
        return [None, None]
    return [float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))]


def gk4_metrik(acc: np.ndarray, T: pd.DataFrame, boot: bool = True) -> Dict[str, Any]:
    """Kabul içinde sınıf payları, rastgele kabul, ✓ yakalama, set set, GT5 + GT9, bootstrap."""
    acc = np.asarray(acc, bool); c4 = T.cemal.to_numpy(); kol = T.kol.to_numpy(); st = T["set"].to_numpy(); evet = c4 == "EVET"; n = int(acc.sum())

    def pay(m: np.ndarray) -> Dict[str, Any]:
        k = int(m.sum()); d = {"kabul": k}
        for s in GK4["sinif"]:
            d[s] = int((m & (c4 == s)).sum()); d[f"{s}_pay"] = (d[s] / k) if k else None
        return d
    o = pay(acc)
    o["set_kabul_var"] = int(sum(acc[st == g].any() for g in pd.unique(st)))
    o["rastgele_kabul"] = int((acc & (kol == GK4["rastgele_kol"])).sum()); o["rastgele_n"] = int((kol == GK4["rastgele_kol"]).sum())
    o["evet_yakalama"] = float((acc & evet).sum() / evet.sum()) if evet.sum() else None
    o["wilson_alt"] = float(gk4_wilson(np.array([(acc & evet).sum()]), np.array([n]))[0]) if n else None
    o["set"] = {g: pay(acc & (st == g)) for g in pd.unique(st)}
    m59 = np.isin(st, ["GT5", "GT9"]); o["gt5_gt9"] = pay(acc & m59)
    if boot:
        o["evet_pay_ga95"] = gk4_boot(acc, evet, GK4["boot"]["B"], GK4["boot"]["tohum"])
    return o


def gk4_karar(m: Dict[str, Any], k3: Dict[str, Any], q95: float) -> Dict[str, Any]:
    E = GK4["karar"]; e = m["EVET_pay"]; k3e = k3["gt5_gt9"]["EVET_pay"]; e59 = m["gt5_gt9"]["EVET_pay"]
    sart = {"kabul>=25": m["kabul"] >= E["kabul_en_az"], "set>=4": m["set_kabul_var"] >= E["set_en_az"],
            "evet_pay>=0,70": e is not None and e >= E["evet_pay"], "erken_pay<=0,20": m["ERKEN_pay"] is not None and m["ERKEN_pay"] <= E["erken_pay"],
            "rastgele<=1": m["rastgele_kabul"] <= E["rastgele_en_cok"],
            "gt5_gt9>=K3+10": e59 is not None and k3e is not None and e59 >= k3e + E["k3_fark"],
            "karistirma>q95": e is not None and e > q95}
    return {"sart": sart, "gecti": all(sart.values()), "kalan": [k for k, v in sart.items() if not v]}


def gk4_en_iyi_aday(M: Dict[str, Dict[str, Any]], K: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    gec = [a for a in GK4_AILE if K[a]["gecti"]]
    if gec:
        return {"aile": gec[0], "ad": f"KURAL-4 ({gec[0]}; karar geçti)", "gecti": True}
    b = [a for a in GK4_AILE if M[a]["kabul"] >= GK4["karar"]["kabul_en_az"]]
    if b:
        a = max(b, key=lambda a: (M[a]["EVET_pay"], -GK4_AILE.index(a)))
    else:
        c = [a for a in GK4_AILE if M[a]["kabul"] >= 1]
        if not c:
            return {"aile": None, "ad": "YOK (hiçbir aile set dışında sayfa kabul etmedi)", "gecti": False}
        a = max(c, key=lambda a: (M[a]["wilson_alt"], -GK4_AILE.index(a)))
    return {"aile": a, "ad": f"EN İYİ ADAY ({a}; karar geçmedi)", "gecti": False}


# ================================================================ 5) H2: ✓ - ERKEN tek ölçü
def gk4_h2_alt(T: pd.DataFrame) -> np.ndarray:
    kol = T.kol.astype(str); c4 = T.cemal
    return ((kol != GK4["rastgele_kol"]) & ~kol.str.startswith(GK4["kitaplik_kol_bas"]) & c4.isin(["EVET", "ERKEN"])).to_numpy()


def gk4_h2(T: pd.DataFrame, y: np.ndarray, ad: List[str]) -> Dict[str, Dict[str, Any]]:
    """T: H2 alt kümesi; y: 1 = EVET, 0 = ERKEN. Her ölçü: havuz set dışı AUC + set set ham AUC + yön tutarlılığı."""
    st = T["set"].to_numpy(); y = np.asarray(y, int); out = {}
    for c in ad:
        x = T[c].to_numpy(float); oy = np.full(len(x), np.nan); yon_kat = {}
        for g in pd.unique(st):
            te = st == g; tr = ~te; a = U.auc(x[tr & (y == 1)], x[tr & (y == 0)]); sg = 1.0 if (not np.isfinite(a) or a >= 0.5) else -1.0
            oy[te] = sg * x[te]; yon_kat[g] = int(sg)
        hav = U.auc(oy[y == 1], oy[y == 0]); tum = U.auc(x[y == 1], x[y == 0]); ys = {}
        for g in pd.unique(st):
            m = st == g; ys[g] = U.auc(x[m & (y == 1)], x[m & (y == 0)])
        ayni = int(sum(1 for v in ys.values() if np.isfinite(v) and v != 0.5 and (v > 0.5) == (tum >= 0.5)))
        out[c] = {"havuz_auc": hav, "tum_auc": tum, "set_auc": ys, "ayni_yon_set": ayni, "kat_yon": yon_kat,
                  "aday": bool(np.isfinite(hav) and hav >= GK4["H2"]["auc"] and ayni >= GK4["H2"]["set_en_az"])}
    return out


def gk4_h2_karistir(T: pd.DataFrame, y: np.ndarray, ad: List[str], B: int, tohum: int) -> Dict[str, Any]:
    rng = np.random.default_rng(int(tohum)); st = T["set"].to_numpy(); y = np.asarray(y, int); gr = [np.flatnonzero(st == g) for g in pd.unique(st)]; mx = []
    for _ in range(int(B)):
        z = y.copy()
        for ii in gr:
            z[ii] = y[ii][rng.permutation(len(ii))]
        H = gk4_h2(T, z, ad); mx.append(max(v["havuz_auc"] for v in H.values() if np.isfinite(v["havuz_auc"])))
    return {"B": int(B), "q95": float(np.quantile(mx, 0.95)), "en_buyuk_havuz_auc": mx}


# ================================================================ 6) KOŞU (bir kez)
def gk4_kapi(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    yol = _gk4_yol("onkayit", cikti); c = gk4_kapi_commit(yol, "GT10_ON_KAYIT.md"); k = IK.ik_kontrol_kapisi(yol)
    metin = open(yol, encoding="utf-8").read()
    if gk4_esik_sha() not in metin:
        raise GK4Hata("kapı: ön kayıttaki eşik sha bugünkü GK4 ile aynı değil")
    kc = _gk4_git(["log", "-1", "--format=%H", "--", "GOZ_KURAL4.py"])
    if not kc or _gk4_git(["status", "--porcelain", "--", "GOZ_KURAL4.py"]):
        raise GK4Hata("kapı: GOZ_KURAL4.py commit edilmemiş ya da değişmiş")
    if kc[:12] not in metin:
        raise GK4Hata(f"kapı: ön kayıt kod commit'ini ({kc[:12]}) içermiyor")
    _GK4_DURUM["kapi"] = True
    return {"onkayit_commit": c, "kod_commit": kc, "kontrol": k["gecti"]}


def gk4_kos(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    kil = _gk4_yol("kilit", ham=ham)
    if os.path.exists(kil) or os.path.exists(_gk4_yol("ozet", cikti)):
        raise GK4Hata(f"BİR KEZ: kos daha önce koştu ({kil})")
    kapi = gk4_kapi(cikti, ham)
    os.makedirs(os.path.dirname(kil), exist_ok=True)
    MI._mi_jyaz(kil, {"bas_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), **kapi}, "gt10 kilit")
    t0 = time.time(); T = gk4_tablo_oku(cikti); ad = gk4_olcu_ad(T); c4 = T.cemal.to_numpy(); y = (c4 == "EVET").astype(int)
    H = gk4_hat(T, y, ad, kural_yaz=True)
    M = {a: gk4_metrik(H[a], T) for a in GK4_AILE}
    M["K3"] = gk4_metrik(T.K3.to_numpy(bool), T); M["HEPSI"] = gk4_metrik(np.ones(len(T), bool), T)
    gk4log.info("hat bitti (%.1f sn); karıştırma başlıyor", time.time() - t0)
    KR = gk4_karistir(T, c4, GK4["karistirma"]["B"], GK4["karistirma"]["tohum"], ad)
    K = {a: gk4_karar(M[a], M["K3"], KR["q95"]) for a in GK4_AILE}
    Tobs = gk4_istatistik({a: H[a] for a in GK4_AILE}, y)
    sec = gk4_en_iyi_aday(M, K)
    h2m = gk4_h2_alt(T); T2 = T[h2m].reset_index(drop=True); y2 = (T2.cemal == "EVET").astype(int).to_numpy()
    H2 = gk4_h2(T2, y2, ad); H2K = gk4_h2_karistir(T2, y2, ad, GK4["H2"]["karistirma_B"], GK4["karistirma"]["tohum"] + 1)
    bes = sorted([c for c in H2 if np.isfinite(H2[c]["havuz_auc"])], key=lambda c: -H2[c]["havuz_auc"])[:5]
    # seçim yanlılığı (bilgi): set set ölçü aralıkları
    yan = {c: {g: {"min": float(np.nanmin(v)), "med": float(np.nanmedian(v)), "max": float(np.nanmax(v))}
               for g, v in T.groupby("set")[c].apply(lambda s: s.to_numpy(float)).items()} for c in ["D1_sira", "DIPTEN_BAR", "KUTU_ORAN", "KUTU_YER", "TEPE_KAT", "Y"]}
    J = {"surum": GK4_SURUM, "not": "GETİRİSİZ: hiçbir sayfanın sonrası hesaplanmadı", "kod_sha": gk4_kod_sha(), "esik_sha": gk4_esik_sha(), "kapi": kapi,
         "zaman_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "n": int(len(T)), "olcu": ad,
         "metrik": M, "karar": K, "karistirma": {k: v for k, v in KR.items() if k != "aile_pay"}, "karistirma_aile_q95": {
             a: float(np.nanquantile(KR["aile_pay"][a], 0.95)) if np.isfinite(KR["aile_pay"][a]).any() else None for a in GK4_AILE},
         "T_gozlenen": Tobs, "secim": sec, "kat_kural": H["kural"], "set_disi_kabul": {a: H[a].astype(int).tolist() for a in GK4_AILE},
         "sayfa_kimlik": T[["set", "sayfa"]].to_dict("records"),
         "H2": {"n": int(len(T2)), "evet": int(y2.sum()), "erken": int((1 - y2).sum()), "olcu": H2, "en_iyi_bes": bes, "karistirma_q95": H2K["q95"],
                "aday": [c for c in H2 if H2[c]["aday"]]},
         "secim_yanliligi": yan, "sure_sn": time.time() - t0}
    MI._mi_jyaz(_gk4_yol("ozet", cikti), J, "gt10 özet")
    gk4log.info("kos bitti (%.0f sn): seçim %s", time.time() - t0, sec["ad"])
    return J


# ================================================================ 7) OLAY LİSTESİ (getirisiz)
def gk4_olay(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    J = json.load(open(_gk4_yol("ozet", cikti), encoding="utf-8"))
    if "olay" in J:
        raise GK4Hata("olay daha önce koştu")
    a = J["secim"]["aile"]
    if a is None:
        raise GK4Hata("olay: seçilen kural yok")
    T = gk4_tablo_oku(cikti); ad = J["olcu"]; K = gk4_kur(a, T, (T.cemal == "EVET").astype(int).to_numpy(), ad)
    K_ = {"ad": J["secim"]["ad"], "aile": a, "kural": K, "egitim": "beş setin 126 sayfası (aynı yöntem)", "esik_sha": gk4_esik_sha(), "kod_sha": gk4_kod_sha(),
          "tum_veri_kabul": int(gk4_uygula(K, T).sum())}
    MI._mi_jyaz(_gk4_yol("kural", cikti), K_, "gt10 kural")
    goster = T[T.kaynak == "acik"][["pazar", "sembol", "s", "t"]]
    k3a = pickle.load(open(os.path.join(GT.GT_YOL["ham"], "k3", "k3_aday.pkl"), "rb"))
    k3_ana = set(zip(k3a.pazar[k3a.ANA == 1], k3a.sembol[k3a.ANA == 1], k3a.L[k3a.ANA == 1].astype(int), k3a.t[k3a.ANA == 1].astype(int)))
    R = []; say: Dict[str, Any] = {"pazar": {}}; t0 = time.time()
    for p in GK4["olay"]["pazar"]:
        Vd = MI.mi_veri(p, GT.GT_YOL["acik"]); V = {s: d for s, d in Vd["V"].items() if len(d) >= 2}; _gk4_kesik(V, f"olay {p}")
        X = GT.gt_yukle(p, ham); X["D1_sira"] = GT.gt_k3_d1_sira(X); E = GT.gt_k2_evren(X)
        d1 = GT.gt_k3_d1(X.loc[E.index, "D1_sira"].to_numpy(float)); P = E[d1].copy(); P["D1_sira"] = X.loc[P.index, "D1_sira"].to_numpy(float)
        del X
        O = []; hata = 0
        for r in P.itertuples():
            try:
                O.append(gk4_olc(V[r.sembol], int(r.s), int(r.t)))
            except Exception:                                               # ölçü kurulamadı (ör. dip parabolü yok): kabul edilmez, sayılır
                O.append({}); hata += 1
        Q = pd.concat([P.reset_index(drop=True), pd.DataFrame(O)], axis=1)
        for c in ad:
            if c not in Q:
                Q[c] = np.nan
        Q[ad] = Q[ad].apply(pd.to_numeric, errors="coerce")
        acc = gk4_uygula(K, Q); A_ = Q[acc].copy()
        k3_y = Q.Y.to_numpy(float) == 1; k3_z = Q.DIPTEN_BAR.to_numpy(float) >= GK4["K3"]["dipten_bar"]
        k3_havuz = np.array([(p, s_, int(l_), int(t_)) in k3_ana for s_, l_, t_ in zip(Q.sembol, Q.L, Q.t)])
        uyusmaz = int(((k3_y & k3_z) != k3_havuz).sum())
        A_["K3"] = [int((p, s_, int(l_), int(t_)) in k3_ana) for s_, l_, t_ in zip(A_.sembol, A_.L, A_.t)]
        Tk = GT.gt_k2_tekil(A_, bar=int(GK4["olay"]["tekil"])).assign(pazar=p, kural=K_["ad"])
        g = goster[goster.pazar == p]
        Tk["gosterildi"] = [int(((g.sembol == s_) & (g.s <= t_) & (g.t >= s_i)).any()) for s_, s_i, t_ in zip(Tk.sembol, Tk.s, Tk.t)]
        Tk["donem"] = ["d1619" if pd.Timestamp(x) <= pd.Timestamp(GK4["olay"]["donem"]["d1619"][1]) else "d2022" for x in Tk.tarih]
        R.append(Tk[["pazar", "sembol", "s", "t", "L", "tarih", "donem", "kural", "K3", "gosterildi", "D1_sira"] + ad])
        say["pazar"][p] = {"d1_havuz": int(len(Q)), "olcu_hata": hata, "kabul_ham": int(acc.sum()), "olay": int(len(Tk)), "hisse": int(Tk.sembol.nunique()),
                           "k3_bayrak_uyusmaz": uyusmaz, "k3_havuz_ana": int(k3_havuz.sum()),
                           "donem": {dn: {"olay": int((Tk.donem == dn).sum()), "K3": int(((Tk.donem == dn) & (Tk.K3 == 1)).sum()),
                                          "gosterildi": int(((Tk.donem == dn) & (Tk.gosterildi == 1)).sum())} for dn in GK4["olay"]["donem"]}}
        gk4log.info("olay %s: D1 havuz %d, kabul %d, olay %d (%.0f sn)", p, len(Q), int(acc.sum()), len(Tk), time.time() - t0)
        del Vd, V, P, Q
    OL = pd.concat(R, ignore_index=True)
    if pd.to_datetime(OL.tarih).max() > pd.Timestamp(GK4["olay"]["son"]):
        raise GK4Hata("KESİK: olay tarihi > 2022-12-31")
    os.makedirs(GK4_YOL["ham"] if ham is None else ham, exist_ok=True)
    with open(_gk4_yol("olay_pkl", ham=ham), "wb") as f:
        pickle.dump(OL, f, protocol=4)
    say["olay_sha"] = MI._mi_sha(_gk4_yol("olay_pkl", ham=ham)); say["olay_yol"] = _gk4_yol("olay_pkl", ham=ham); say["kural"] = K_
    say["sure_sn"] = time.time() - t0
    J["olay"] = say
    MI._mi_jyaz(_gk4_yol("ozet", cikti), J, "gt10 özet")
    return say


# ================================================================ 8) RAPOR
def _y(x: Any, yuzde: bool = True, n: int = 0) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    return f"%{100 * x:.{n}f}" if yuzde else f"{x:.{n}f}".replace(".", ",")


def gk4_kural_metin(K: Dict[str, Any]) -> str:
    if K.get("bos"):
        return "(boş: kabul yok)"
    if K["aile"] in ("A", "B"):
        return " VE ".join(f"{s['olcu']} {s['yon']} {s['esik']:.4g}" for s in K["sart"])
    return "lojistik(" + ", ".join(K["olcu"]) + f") >= {K['esik']:.3f}"


def gk4_rapor(cikti: Optional[str] = None) -> str:
    J = json.load(open(_gk4_yol("ozet", cikti), encoding="utf-8")); M = J["metrik"]; L_: List[str] = []
    sec = J["secim"]; gec = [a for a in GK4_AILE if J["karar"][a]["gecti"]]
    L_ += ["# GT10 RAPOR — KURAL-4: beş işaretli setten sete göre dışarıda sınanmış kabul kuralı (28 Kasım 2026)", "",
           "GETİRİSİZ: hiçbir sayfanın sonrası hesaplanmadı. Etiket: tespit işi ('iz' değil).", ""]
    L_ += ["## Tablo 1 — Set dışı (havuz, 126 sayfa)", "",
           "| Kural | kabul | set | ✓ | K | erken | değil | ✓ payı [%95] | rastgele kabul | ✓ yakalama | karıştırma %95 (T) | karar |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in GK4_AILE + ["K3", "HEPSI"]:
        m = M[a]; ga = m.get("evet_pay_ga95") or [None, None]
        kr = ("GEÇTİ" if J["karar"][a]["gecti"] else "kaldı: " + ", ".join(J["karar"][a]["kalan"])) if a in GK4_AILE else "baz"
        L_.append(f"| {a} | {m['kabul']} | {m['set_kabul_var']} | {_y(m['EVET_pay'])} | {_y(m['KISMEN_pay'])} | {_y(m['ERKEN_pay'])} | {_y(m['HAYIR_pay'])} | "
                  f"{_y(m['EVET_pay'])} [{_y(ga[0])}; {_y(ga[1])}] | {m['rastgele_kabul']} / {m['rastgele_n']} | {_y(m['evet_yakalama'])} | "
                  f"{_y(J['karistirma']['q95'])} | {kr} |")
    L_ += ["", f"Gözlenen T = {_y(J['T_gozlenen'], n=1)}; karıştırma ({J['karistirma']['B']} kez) T %95 = {_y(J['karistirma']['q95'], n=1)}. "
           f"Seçim: {sec['ad']}.", ""]
    L_ += ["## Tablo 2 — Set set (set dışı kabul: kabul / ✓ / K / erken / değil)", "", "| Kural | " + " | ".join(g for g, _, _ in GK4["setler"]) + " | GT5 + GT9 ✓ payı |",
           "|---" * (len(GK4["setler"]) + 2) + "|"]
    for a in GK4_AILE + ["K3", "HEPSI"]:
        m = M[a]
        L_.append(f"| {a} | " + " | ".join(f"{v['kabul']} / {v['EVET']} / {v['KISMEN']} / {v['ERKEN']} / {v['HAYIR']}" for v in (m["set"][g] for g, _, _ in GK4["setler"]))
                  + f" | {_y(m['gt5_gt9']['EVET_pay'])} ({m['gt5_gt9']['kabul']}) |")
    L_ += ["", "## Tablo 3 — Kat kuralları (eğitim dört set)", "", "| Aile | sınama seti | kural |", "|---|---|---|"]
    for a in GK4_AILE:
        for g, K in J["kat_kural"][a].items():
            L_.append(f"| {a} | {g} | {gk4_kural_metin(K)} |")
    H2 = J["H2"]
    L_ += ["", f"## Tablo 4 — H2: ✓ - erken (kodun seçtiği sayfalar; {H2['evet']} ✓, {H2['erken']} erken)", "",
           "| Ölçü | havuz set dışı AUC | bütün veri AUC | " + " | ".join(g for g, _, _ in GK4["setler"]) + " | aynı yön set | aday |", "|---" * (len(GK4["setler"]) + 5) + "|"]
    for c in H2["en_iyi_bes"]:
        v = H2["olcu"][c]
        L_.append(f"| {c} | {_y(v['havuz_auc'], False, 2)} | {_y(v['tum_auc'], False, 2)} | " + " | ".join(_y(v["set_auc"].get(g), False, 2) for g, _, _ in GK4["setler"])
                  + f" | {v['ayni_yon_set']} | {'EVET' if v['aday'] else 'hayır'} |")
    L_ += ["", f"Karıştırma (set içi ✓ / erken, {GK4['H2']['karistirma_B']} kez): en büyük havuz AUC'nin %95'i = {_y(H2['karistirma_q95'], False, 2)}. "
           f"H2 adayları: {', '.join(H2['aday']) or 'yok'}.", ""]
    L_ += ["## Tablo 5 — Seçim yanlılığı (set set ölçü aralığı: min / medyan / maks)", "", "| Ölçü | " + " | ".join(g for g, _, _ in GK4["setler"]) + " |",
           "|---" * (len(GK4["setler"]) + 1) + "|"]
    for c, v in J["secim_yanliligi"].items():
        L_.append(f"| {c} | " + " | ".join(f"{_y(v[g]['min'], False, 2)} / {_y(v[g]['med'], False, 2)} / {_y(v[g]['max'], False, 2)}" if g in v else "-"
                                           for g, _, _ in GK4["setler"]) + " |")
    if "olay" in J:
        O = J["olay"]
        L_ += ["", f"## Tablo 6 — Olay listesi ({O['kural']['ad']}: {gk4_kural_metin(O['kural']['kural'])}; getirisiz)", "",
               "| Pazar | D1 havuz | ölçü hatası | kabul (ham) | olay (tekil 40) | hisse | 2016-19 olay / K3 / gösterildi | 2020-22 olay / K3 / gösterildi |",
               "|---|---|---|---|---|---|---|---|"]
        for p, v in O["pazar"].items():
            dd = v["donem"]
            L_.append(f"| {p} | {v['d1_havuz']} | {v['olcu_hata']} | {v['kabul_ham']} | {v['olay']} | {v['hisse']} | {dd['d1619']['olay']} / {dd['d1619']['K3']} / "
                      f"{dd['d1619']['gosterildi']} | {dd['d2022']['olay']} / {dd['d2022']['K3']} / {dd['d2022']['gosterildi']} |")
        L_ += ["", f"Dosya: {O['olay_yol']} (sha {O['olay_sha'][:12]}); eşikler arastirma_cikti/goz_tespit/gt10_kural4.json.", ""]
    L_ += ["", f"Karar geçen aile: {', '.join(gec) or 'YOK'}.", ""]
    md = "\n".join(L_) + "\n"
    return md


def _cakisma_kontrol_gk4(_once=_CK_ONCE_GK4, _dosya="GOZ_KURAL4.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_GK4",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_gk4()


def _gk4_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="GOZ_KURAL4")
    ap.add_argument("komut", choices=["tablo", "onkayit", "kos", "olay", "rapor", "sha"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "tablo":
            T = gk4_tablo(); print(T.groupby(["set", "cemal"]).size().unstack(fill_value=0))
        elif a.komut == "onkayit":
            print(gk4_onkayit_sayim())
        elif a.komut == "kos":
            J = gk4_kos(); print(json.dumps(MI._mi_json({"karar": J["karar"], "secim": J["secim"], "T": J["T_gozlenen"], "q95": J["karistirma"]["q95"]}),
                                           ensure_ascii=False, indent=1))
        elif a.komut == "olay":
            print(json.dumps(MI._mi_json({k: v for k, v in gk4_olay().items() if k != "kural"}), ensure_ascii=False, indent=1))
        elif a.komut == "rapor":
            md = gk4_rapor(); MI._mi_yaz(_gk4_yol("rapor") + ".tablo.md", md, "gt10 rapor tablo"); print(md)
        elif a.komut == "sha":
            print(json.dumps({"kod_sha": gk4_kod_sha(), "esik_sha": gk4_esik_sha()}, indent=1))
    except GK4Hata as ex:
        gk4log.error("DURDU: %s", ex)
        return 2
    return 0


def _gk4_md(D: pd.DataFrame) -> str:
    """Küçük çapraz tabloyu markdown'a (tabulate yok)."""
    sat = ["| set | " + " | ".join(str(c) for c in D.columns) + " | toplam |", "|---" * (len(D.columns) + 2) + "|"]
    for i, r in D.iterrows():
        sat.append(f"| {i} | " + " | ".join(str(int(v)) for v in r.to_numpy()) + f" | {int(r.sum())} |")
    sat.append("| toplam | " + " | ".join(str(int(v)) for v in D.sum(0).to_numpy()) + f" | {int(D.to_numpy().sum())} |")
    return "\n".join(sat)


def gk4_onkayit_sayim(cikti: Optional[str] = None) -> str:
    """Ön kayıt sayım bölümü: set x sınıf, set x kol, ölçü eksikleri, K3 bayrağı sayımı (etiketle çaprazlanmaz). Etiket - ölçü ilişkisi YOK."""
    T = gk4_tablo_oku(cikti); ad = gk4_olcu_ad(T); L_ = ["### Set x sınıf", "", _gk4_md(T.groupby(["set", "cemal"]).size().unstack(fill_value=0)), "",
                                                          "### Set x kol", "", _gk4_md(T.groupby(["set", "kol"]).size().unstack(fill_value=0)), ""]
    eks = {c: int(T[c].isna().sum()) for c in ad if T[c].isna().any()}
    L_ += ["### Ölçü eksikleri (126 sayfada boş değer)", "", (", ".join(f"{k} {v}" for k, v in eks.items()) or "yok"), "",
           f"Ölçü sayısı: {len(ad)}: {', '.join(ad)}", "",
           f"D1 sırası bulunan sayfa: {int(np.isfinite(T.D1_sira).sum())} / {len(T)}; KURAL-3 bayraklı sayfa (set başına; etiketle çaprazlanmadı): "
           + ", ".join(f"{g} {int(v)}" for g, v in T.groupby("set").K3.sum().items()), "",
           f"Kod sha256: {gk4_kod_sha()}; eşik sha256: {gk4_esik_sha()}"]
    return "\n".join(L_)


if __name__ == "__main__":
    sys.exit(_gk4_ana())
