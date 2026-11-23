"""TANIM2 — TANIM ADIMI 2: Cemal'in 'dip savunması VAR' gözünü ölçülebilir tanıma çevirme + ikinci bağımsız kör set  (23 Kasım 2026)

GETİRİ ÖLÇMEZ. Sinyal sonrası fiyat hiçbir adımda okunmaz: bütün özellikler kör sayfada görülen pencereden (sinyal günü t dahil, son 121
geçerli bar; veri t'de KESİLİR) ya da goz_uyum anahtarındaki nedensel F / ek özelliklerden.
Komutlar (repo kökünden):
  python arastirma_cikti/goz_uyum/tanim2.py aday               ADIM A (keşif): ilk 40 sayfa + Cemal'in işaretleri -> TANIM2_KESIF.md, tanim2_kesif.json
  python arastirma_cikti/goz_uyum/tanim2.py sec  [--islem 4]   ADIM B: Y1 ∧ Ş1 havuzu (ilk set (pazar, sembol) hariç) -> 40 sayfa (tohum 20261124) -> tanim2_anahtar.json
  python arastirma_cikti/goz_uyum/tanim2.py pdf                anahtar -> TANIM2_KOR.pdf (kapak + 40 kör sayfa; goz_uyum ile aynı sayfa tasarımı)
  python arastirma_cikti/goz_uyum/tanim2.py muhur              sha'lar + seçim kuralı + hüküm + kontrol tablosu -> TANIM2_ON_KAYIT.md (kontrol kapısı)
  python arastirma_cikti/goz_uyum/tanim2.py olc --cemal J.json mühür denetimi -> TANIM2_SONUC.md (J.json: {"1": "VAR", "2": "YOK", "3": "?", ...})
  python arastirma_cikti/goz_uyum/tanim2.py test               çakışma kapısı + kappa + yeni özellik prefix değişmezliği + kural seçimi sağlaması
Veri: /tmp/kasa2/acik (V_ABD.pkl, V_AVR.pkl), /tmp/kasa/acik/V_BIST.pkl (goz_uyum.GU_VERI).  Kod değiştiyse çalışma zamanını yeniden başlat.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import logging
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

_CK_ONCE_TZ = {k: id(v) for k, v in globals().items()}

import numpy as np
import pandas as pd

TZ_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(os.getcwd(), "arastirma_cikti", "goz_uyum")
if TZ_DIR not in sys.path:
    sys.path.insert(0, TZ_DIR)
import goz_uyum as GU  # noqa: E402  (KOK'u sys.path'e koyar; GOZ_ETIKET / YAPI_HEDEF'i içe alır)

tzlog = logging.getLogger("tanim2")
if not tzlog.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

KOK = GU.KOK
TZ_YOL = {"is_tanimi": os.path.join(TZ_DIR, "TANIM2_IS_TANIMI.md"), "kesif_md": os.path.join(TZ_DIR, "TANIM2_KESIF.md"),
          "kesif": os.path.join(TZ_DIR, "tanim2_kesif.json"), "anahtar": os.path.join(TZ_DIR, "tanim2_anahtar.json"),
          "pdf": os.path.join(TZ_DIR, "TANIM2_KOR.pdf"), "onkayit": os.path.join(TZ_DIR, "TANIM2_ON_KAYIT.md"),
          "sonuc": os.path.join(TZ_DIR, "TANIM2_SONUC.md"), "sonuc_json": os.path.join(TZ_DIR, "tanim2_sonuc.json"),
          "ilk_anahtar": GU.GU_YOL["anahtar"], "ilk_cemal": os.path.join(TZ_DIR, "cemal_isaret.json"),
          "kod": os.path.abspath(__file__) if "__file__" in globals() else os.path.join(TZ_DIR, "tanim2.py")}

# Seçim kuralı: iş tanımından AYNEN (sonuç görülmeden; ön kayda aynen girer)
TZ_SECIM_KURALI = ("ADAY_1 = LOOCV kappa'sı en yüksek TEK özellikli kural; ADAY_2 = LOOCV kappa'sı en yüksek iki özellikli kural (ADAY_1'den "
                   "LOOCV kappa'da en az 0,10 yüksek değilse ADAY_2 = yok, basit olan kalır); her ikisinin eşiği 40 sayfanın TAMAMIYLA yeniden "
                   "seçilir ve SAYI olarak mühürlenir. Ayrıca KONTROL = eski Ş3 (değişmez).")

# YENİ ÖZELLİKLER (Cemal'in çizimlerinden; en çok 8; tanım ve pencere sonuç görülmeden yazıldı).
# Pencere W = kör sayfada görülen 121 geçerli bar [t-120, t] (t = sinyal günü dahil; veri t'de kesik). Dizinler 0..120, i = 120.
# lo = min L(W), jd = lo'nun İLK görüldüğü bar, hi = max H(W). NaN olan değer kuralda YOK sayılır (TZ_ESIK['nan']).
TZ_YENI: Dict[str, str] = {
    "Y1_dip_tepki_konum": "dipten sonraki en yüksek tepkiye göre son fiyatın konumu: (C_t - lo) / (max H[jd..t] - lo); 1 = dip sonrası tepede, "
                          "0 = dipte (payda 0 ise NaN). Çizim: 5 (orta bölgede V dönüş, VAR)",
    "Y2_dip_alt_yari": "dip bölgesinde kapanışların alt yarıda kalma payı: dip bölgesi = W'de L <= lo + 0,20 x (hi - lo) olan barlar; "
                       "pay((C - L) / (H - L) < 0,5). Sözlü kural: 'alt fitili az mumlar' (kapanış dip bölgesinde aşağıda = savunma yok)",
    "Y3_dokunus2_hacim": "dibe ikinci dokunuşta hacmin birincisine oranı: dokunuş barı = L <= lo x 1,03; ardışık dokunuş barları arasında 5 bardan "
                         "fazla boşluk yeni dokunuş epizodu başlatır; ort V(2. epizot) / ort V(1. epizot); 2 epizot yoksa NaN",
    "Y4_yukselen_dip_n": "dip sonrası yükselen dip sayısı (higher lows): pivot dip = j (jd < j <= t-3, j >= 3) ve L_j = min L[j-3..j+3]; "
                         "sırayla her pivotun L'si bir öncekinden (ilki için lo) büyükse +1. Çizim: 12 (yıldız, VAR)",
    "Y5_direnc_uzaklik": "tabanın üstündeki yatay direnç çizgisine uzaklık: R = max H[jd..t-1] (dip sonrası tavan, t hariç); C_t / R - 1 "
                         "(< 0: fiyat direncin altında); jd = t ise NaN. Çizim: 2 (tabanın üstüne yatay direnç, YOK)",
    "Y6_tepe_egim20": "son 20 mumun tepeleri düşüyor mu (dağıtım): H[t-19..t] doğrusal regresyon eğimi x 19 / ort H[t-19..t] "
                      "(20 barlık göreli değişim; < 0 düşen tepeler). Çizim: 35 (tepe bölgesi, dağıtım, YOK)",
    "Y7_v_hiz": "V dönüş hızı: dipten sonra ilk C_j >= 1,10 x lo olan bara kadar bar sayısı (j - jd); t'ye kadar olmadıysa 121 "
                "(küçük = hızlı V). Çizim: 5 (V dönüş, VAR)",
    "Y8_dip_sonrasi_boy": "dip sonrası mumların ortalama boyunun düşüş mumlarına oranı: ort((H - L) / C, [jd+1..t]) / ort((H - L) / C, "
                          "W içinde [0..jd] düşüş mumları C < O); dip sonrası 3 bardan ya da düşüş mumu 3'ten azsa NaN. Sözlü kural: "
                          "'dip savunması' (dip sonrası küçük mum)",
}
TZ_YENI_KOL = list(TZ_YENI)

TZ_ESIK: Dict[str, Any] = {
    "tohum": 20261124,
    "kaynak_havuz": "goz_uyum.gu_havuz (Y1 ∧ Ş1, P2 benzeri likidite, aynı hissede 60 bar tekil; pencereler ve likidite GU_ESIK ile aynı)",
    "sayfa": {"ABD": 30, "AVR": 5, "BIST": 5, "hucre": 10, "hucre_pazar": [[8, 1, 1], [8, 1, 1], [7, 1, 2], [7, 2, 1]],
              "min_gun_arasi": 30, "hisse_azami": 1, "ilk_set_haric": "ilk 40 sayfanın (pazar, sembol) çiftleri havuzdan çıkarılır"},
    "tabaka": "ADAY_1 VAR / YOK x KONTROL (Ş3) VAR / YOK dört hücre, 10'ar sayfa; hücre-pazar kotası tohumla karışır; eksik ABD'den, "
              "yine eksikse aynı ADAY_1 değerli öteki hücreden, yine eksikse herhangi hücreden tamamlanır ve yazılır",
    "kural": {"yon": [">=", "<="], "esik_aday": "eğitim değerlerinin ardışık benzersiz sonlu değerleri arasındaki orta noktalar",
              "amac": "dengeli doğruluk = (VAR duyarlılığı + YOK duyarlılığı) / 2 (hedef = Cemal VAR)",
              "esitlik": "dengeli doğruluk büyük > ham doğruluk büyük > yön '>=' önce (çiftte (A, B) yön sırası '>=' önce) > eşit eşik listesinin "
                         "ortadaki (alt-orta) elemanı",
              "nan": "NaN değer kuralda YOK", "cift_aday_n": 6, "cift_op": ["VE", "VEYA"],
              "cift_sira": "ilk 6 = tek özellik LOOCV kappa büyük > 40 sayfa kappa büyük > ad sırası",
              "aday2_fark": 0.10, "loocv": "her dışarıda bırakılan sayfa için eşik aday kümesi ve eşik(ler) kalan 39 sayfadan yeniden seçilir"},
    "kappa": {"B": 5000, "tohum": 20261124, "gecerli": 0.60, "gecerli_alt": 0.40, "kismen": 0.40, "karar_min": 30},
    "hukum": "ikinci sette ADAY_1 (ve varsa ADAY_2) kappa >= 0,60 ve bootstrap %95 alt ucu >= 0,40 -> TANIM GEÇERLİ (getiri ölçümüne geçilir, kasa açılır); "
             "kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN (üçüncü tur: ilk iki setin 80 sayfası birleşik keşif, üçüncü bağımsız set); "
             "< 0,40 GEÇERSİZ (Cemal'le görüşme: neye baktığını çizimle anlatması); karar sayısı < 30 ise ÖLÇÜLEMEDİ. KONTROL (eski Ş3) kappa'sı karşılaştırma için yazılır",
    "pencere_bar": 120,
    "yeni_ozellik_sha": hashlib.sha256(json.dumps(TZ_YENI, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest(),
    "secim_kurali": TZ_SECIM_KURALI,
}


class TZHata(RuntimeError):
    """Durdurucu hata: veri / seçim / mühür tutmadı."""


def _sha_esik() -> str:
    return hashlib.sha256(json.dumps(TZ_ESIK, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


# ================================================================ 1) YENİ ÖZELLİKLER (yalnız kör sayfa penceresi)
def tz_yeni_ozellik_dizi(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, V: np.ndarray) -> Dict[str, float]:
    """Diziler = pencere W (son eleman = t). Yalnız W okunur; t sonrası fonksiyona girmez."""
    out = {k: np.nan for k in TZ_YENI_KOL}
    n = len(C)
    if n < 25:
        return out
    i = n - 1
    lo = float(L.min()); jd = int(np.argmin(L)); hi = float(H.max())
    hp = float(H[jd:].max())
    if hp > lo:
        out["Y1_dip_tepki_konum"] = float((C[i] - lo) / (hp - lo))
    m = L <= lo + 0.20 * (hi - lo)
    pos = (C - L) / (H - L)
    out["Y2_dip_alt_yari"] = float(np.mean(pos[m] < 0.5)) if m.any() else np.nan
    dok = np.flatnonzero(L <= lo * 1.03)
    if len(dok):
        ep: List[List[int]] = [[int(dok[0])]]
        for j in dok[1:]:
            if int(j) - ep[-1][-1] > 5:
                ep.append([int(j)])
            else:
                ep[-1].append(int(j))
        if len(ep) >= 2:
            v1 = float(np.mean(V[ep[0]])); v2 = float(np.mean(V[ep[1]]))
            out["Y3_dokunus2_hacim"] = v2 / v1 if v1 > 0 else np.nan
    piv = [j for j in range(max(jd + 1, 3), i - 2) if L[j] == L[j - 3:j + 4].min()]
    ref = lo; say = 0
    for j in piv:
        if L[j] > ref:
            say += 1
        ref = float(L[j])
    out["Y4_yukselen_dip_n"] = float(say)
    if jd < i:
        R = float(H[jd:i].max())
        out["Y5_direnc_uzaklik"] = float(C[i] / R - 1)
    h20 = H[i - 19:i + 1]; xx = np.arange(20, dtype=float)
    egim = float(np.polyfit(xx, h20, 1)[0])
    out["Y6_tepe_egim20"] = egim * 19.0 / float(np.mean(h20))
    hit = np.flatnonzero(C[jd + 1:] >= 1.10 * lo)
    out["Y7_v_hiz"] = float(hit[0] + 1) if len(hit) else 121.0
    r = (H - L) / C
    post = r[jd + 1:]; pre_m = (C[:jd + 1] < O[:jd + 1]); pre = r[:jd + 1][pre_m]
    if len(post) >= 3 and len(pre) >= 3:
        out["Y8_dip_sonrasi_boy"] = float(np.mean(post) / np.mean(pre))
    return out


def tz_yeni_ozellik(W: pd.DataFrame) -> Dict[str, float]:
    O, H, L, C, V = (W[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    return tz_yeni_ozellik_dizi(O, H, L, C, V)


def tz_pencere(pazar: str, sembol: str, t: pd.Timestamp, V: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """goz_uyum._gu_pencere (veri t'de kesik, son 121 geçerli bar) + K2 mekanik denetimi."""
    W = GU._gu_pencere(pazar, sembol, t, V)
    if W.index.max() > t or W.index[-1] != t or len(W) != TZ_ESIK["pencere_bar"] + 1:
        raise TZHata(f"{pazar} {sembol} {t.date()}: pencere t'de kesik değil / 121 bar değil")
    return W


# ================================================================ 2) KURAL SEÇİMİ (tek / çift; LOOCV)
def tz_kural(x: np.ndarray, yon: str, e: float) -> np.ndarray:
    x = np.asarray(x, float); f = np.isfinite(x)
    out = np.zeros(len(x), bool)
    out[f] = (x[f] >= e) if yon == ">=" else (x[f] <= e)
    return out


def _esik_aday(x: np.ndarray) -> np.ndarray:
    u = np.unique(x[np.isfinite(x)])
    return (u[:-1] + u[1:]) / 2.0 if len(u) >= 2 else np.array([], float)


def _metrik(P: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """P: (..., n) bool kural çıktıları; y: (n,) bool. -> (dengeli doğruluk, ham doğruluk)."""
    nv = max(int(y.sum()), 1); ny = max(int((~y).sum()), 1)
    tp = (P & y).sum(-1); tn = (~P & ~y).sum(-1)
    return (tp / nv + tn / ny) / 2.0, (tp + tn) / len(y)


def _en_iyi(bal: np.ndarray, acc: np.ndarray) -> np.ndarray:
    """Eşitlik kuralı: bal büyük > acc büyük; kalan indeksler (düz sıra) döner."""
    b = bal.max(); m = np.isclose(bal, b, atol=1e-12)
    a = np.where(m, acc, -1.0).max(); return np.flatnonzero((m & np.isclose(acc, a, atol=1e-12)).ravel())


def tz_tek_sec(x: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    ea = _esik_aday(x)
    if not len(ea):
        return {"yon": ">=", "esik": float("nan"), "bal": 0.5}
    P = np.stack([tz_kural(x, yon, e) for yon in (">=", "<=") for e in ea])           # (2E, n): önce '>=' sonra '<='
    bal, acc = _metrik(P, y)
    idx = _en_iyi(bal, acc)
    E = len(ea); yon_i = idx // E
    yon0 = int(yon_i.min()); kalan = idx[yon_i == yon0] % E                           # '>=' önce
    k = int(kalan[(len(kalan) - 1) // 2])                                             # alt-orta eleman
    return {"yon": (">=", "<=")[yon0], "esik": float(ea[k]), "bal": float(bal[yon0 * E + k])}


def tz_cift_sec(xa: np.ndarray, xb: np.ndarray, y: np.ndarray, op: str) -> Dict[str, Any]:
    ea, eb = _esik_aday(xa), _esik_aday(xb)
    if not len(ea) or not len(eb):
        return {"yonA": ">=", "esikA": float("nan"), "yonB": ">=", "esikB": float("nan"), "bal": 0.5}
    RA = np.stack([tz_kural(xa, yon, e) for yon in (">=", "<=") for e in ea])          # (2Ea, n)
    RB = np.stack([tz_kural(xb, yon, e) for yon in (">=", "<=") for e in eb])          # (2Eb, n)
    P = (RA[:, None, :] & RB[None, :, :]) if op == "VE" else (RA[:, None, :] | RB[None, :, :])
    bal, acc = _metrik(P, y)
    idx = _en_iyi(bal, acc)
    Ea, Eb = len(ea), len(eb); nb = 2 * Eb
    ia, ib = idx // nb, idx % nb
    ya, yb = ia // Ea, ib // Eb
    key = ya * 2 + yb; k0 = int(key.min()); sel = idx[key == k0]                      # yön çifti sırası: (>=,>=), (>=,<=), (<=,>=), (<=,<=)
    k = int(sel[(len(sel) - 1) // 2])
    a, b = k // nb, k % nb
    return {"yonA": (">=", "<=")[a // Ea], "esikA": float(ea[a % Ea]), "yonB": (">=", "<=")[b // Eb], "esikB": float(eb[b % Eb]),
            "bal": float(bal.ravel()[k])}


def tz_cift_kural(xa: np.ndarray, xb: np.ndarray, r: Dict[str, Any], op: str) -> np.ndarray:
    a = tz_kural(xa, r["yonA"], r["esikA"]); b = tz_kural(xb, r["yonB"], r["esikB"])
    return (a & b) if op == "VE" else (a | b)


def tz_loocv_tek(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    n = len(y); pr = np.zeros(n, bool)
    for k in range(n):
        m = np.arange(n) != k
        r = tz_tek_sec(x[m], y[m])
        pr[k] = bool(tz_kural(x[k:k + 1], r["yon"], r["esik"])[0]) if np.isfinite(r["esik"]) else False
    return pr


def tz_loocv_cift(xa: np.ndarray, xb: np.ndarray, y: np.ndarray, op: str) -> np.ndarray:
    n = len(y); pr = np.zeros(n, bool)
    for k in range(n):
        m = np.arange(n) != k
        r = tz_cift_sec(xa[m], xb[m], y[m], op)
        pr[k] = bool(tz_cift_kural(xa[k:k + 1], xb[k:k + 1], r, op)[0]) if np.isfinite(r["esikA"]) and np.isfinite(r["esikB"]) else False
    return pr


# ================================================================ 3) ADIM A (keşif)
def _ilk_set() -> Tuple[pd.DataFrame, np.ndarray]:
    J = json.load(open(TZ_YOL["ilk_anahtar"], encoding="utf-8")); S = pd.DataFrame(J["sayfalar"]).sort_values("sayfa").reset_index(drop=True)
    C = json.load(open(TZ_YOL["ilk_cemal"], encoding="utf-8"))
    cem = {int(k): GU.gu_norm(v) for k, v in C.items()}
    if sorted(cem) != list(S.sayfa):
        raise TZHata("cemal_isaret.json sayfaları ilk anahtarla uyuşmuyor")
    S["cemal"] = S.sayfa.map(cem)
    if (S.cemal == "?").any():
        raise TZHata("ilk sette '?' var: keşif tasarımı yalnız VAR / YOK için yazıldı")
    Vc: Dict[str, Dict[str, pd.DataFrame]] = {}
    yeni = []
    for r in S.itertuples(index=False):
        if r.pazar not in Vc:
            Vc[r.pazar] = GU.gu_veri(r.pazar)
        yeni.append(tz_yeni_ozellik(tz_pencere(r.pazar, r.sembol, pd.Timestamp(r.sinyal_gunu), Vc[r.pazar])))
    S = pd.concat([S, pd.DataFrame(yeni)], axis=1)
    return S, (S.cemal == "VAR").to_numpy(bool)


def tz_aday_kolonlar() -> List[str]:
    return GU.GU_OZ_KOL + GU.GU_EK_KOL + TZ_YENI_KOL


def tz_aday() -> Dict[str, Any]:
    t0 = time.time()
    S, y = _ilk_set()
    kol = tz_aday_kolonlar()
    tek = []
    for c in kol:
        x = S[c].to_numpy(float)
        r = tz_tek_sec(x, y)
        tam = tz_kural(x, r["yon"], r["esik"]) if np.isfinite(r["esik"]) else np.zeros(len(y), bool)
        lo = tz_loocv_tek(x, y)
        g = {}
        for ad, m in (("VAR", y), ("YOK", ~y)):
            v = x[m]; f = v[np.isfinite(v)]
            g[ad] = {"n": int(len(v)), "nan": int((~np.isfinite(v)).sum()), "medyan": float(np.median(f)) if len(f) else np.nan,
                     "q25": float(np.percentile(f, 25)) if len(f) else np.nan, "q75": float(np.percentile(f, 75)) if len(f) else np.nan}
        tek.append({"ozellik": c, "yeni": c in TZ_YENI, "yon": r["yon"], "esik": r["esik"], "bal": r["bal"], "kappa": GU.gu_kappa(y, tam),
                    "loocv_kappa": GU.gu_kappa(y, lo), "loocv_uyum": float(np.mean(lo == y)), "dagilim": g,
                    "tam_VAR": int(tam.sum())})
    T = pd.DataFrame(tek)
    T["_k"] = T.loocv_kappa.fillna(-9); T["_t"] = T.kappa.fillna(-9)
    T = T.sort_values(["_k", "_t", "ozellik"], ascending=[False, False, True], kind="mergesort").reset_index(drop=True)
    ilk6 = list(T.ozellik[:int(TZ_ESIK["kural"]["cift_aday_n"])])
    cift = []
    for a, b in itertools.combinations(ilk6, 2):
        xa, xb = S[a].to_numpy(float), S[b].to_numpy(float)
        for op in TZ_ESIK["kural"]["cift_op"]:
            r = tz_cift_sec(xa, xb, y, op)
            tam = tz_cift_kural(xa, xb, r, op)
            lo = tz_loocv_cift(xa, xb, y, op)
            cift.append({"A": a, "B": b, "op": op, **r, "kappa": GU.gu_kappa(y, tam), "loocv_kappa": GU.gu_kappa(y, lo),
                         "loocv_uyum": float(np.mean(lo == y)), "tam_VAR": int(tam.sum())})
    Cf = pd.DataFrame(cift)
    Cf["_k"] = Cf.loocv_kappa.fillna(-9); Cf["_t"] = Cf.kappa.fillna(-9)
    Cf = Cf.sort_values(["_k", "_t", "A", "B", "op"], ascending=[False, False, True, True, True], kind="mergesort").reset_index(drop=True)
    # SEÇİM (TZ_SECIM_KURALI)
    a1 = T.iloc[0]
    x1 = S[a1.ozellik].to_numpy(float); r1 = tz_tek_sec(x1, y)
    ADAY_1 = {"tur": "tek", "ozellik": a1.ozellik, "yon": r1["yon"], "esik": r1["esik"], "kappa_40": GU.gu_kappa(y, tz_kural(x1, r1["yon"], r1["esik"])),
              "loocv_kappa_40": float(a1.loocv_kappa), "tanim": _tanim_metni(a1.ozellik)}
    c1 = Cf.iloc[0]
    if float(c1.loocv_kappa) >= float(a1.loocv_kappa) + float(TZ_ESIK["kural"]["aday2_fark"]) - 1e-12:
        xa, xb = S[c1.A].to_numpy(float), S[c1.B].to_numpy(float); r2 = tz_cift_sec(xa, xb, y, c1.op)
        ADAY_2: Optional[Dict[str, Any]] = {"tur": "cift", "A": c1.A, "B": c1.B, "op": c1.op, **r2,
                                            "kappa_40": GU.gu_kappa(y, tz_cift_kural(xa, xb, r2, c1.op)), "loocv_kappa_40": float(c1.loocv_kappa),
                                            "tanim": f"{_tanim_metni(c1.A)} {c1.op} {_tanim_metni(c1.B)}"}
    else:
        ADAY_2 = None
    s3 = S.S3.to_numpy(bool)
    KONTROL = {"tur": "Ş3", "tanim": "eski Ş3: F2 (hat eğimi) >= -0,01", "kappa_40": GU.gu_kappa(y, s3)}
    # Cemal'in çizim sayfaları (bilgi)
    cizim = {int(p): {c: float(S.loc[S.sayfa == p, c].iloc[0]) for c in TZ_YENI_KOL} | {"cemal": S.loc[S.sayfa == p, "cemal"].iloc[0]}
             for p in (2, 5, 12, 35)}
    K = {"zaman_utc": GU._simdi(), "etiket": "KEŞİF (40 sayfa; seçilen kural ikinci bağımsız sette sınanır)", "n": int(len(y)),
         "cemal_VAR": int(y.sum()), "cemal_YOK": int((~y).sum()), "esik_sha": _sha_esik(), "secim_kurali": TZ_SECIM_KURALI,
         "ADAY_1": ADAY_1, "ADAY_2": ADAY_2, "KONTROL": KONTROL, "ilk6": ilk6,
         "tek": T.drop(columns=["_k", "_t"]).to_dict("records"), "cift": Cf.drop(columns=["_k", "_t"]).to_dict("records"),
         "yeni_40": S[["sayfa", "pazar", "cemal"] + TZ_YENI_KOL].to_dict("records"), "cizim_sayfalari": cizim,
         "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(TZ_YOL["kesif"], K)
    _kesif_md(K, T, Cf)
    tzlog.info("ADAY_1 %s %s %.4g (kappa %.3f, LOOCV %.3f); ADAY_2 %s", ADAY_1["ozellik"], ADAY_1["yon"], ADAY_1["esik"],
               ADAY_1["kappa_40"], ADAY_1["loocv_kappa_40"], "yok" if ADAY_2 is None else ADAY_2["tanim"])
    return K


_F_ACIK = {
    "F1": "hat dokunuş sayısı", "F2": "hat eğimi (son / ilk dokunuş Low - 1)", "F3": "bölge mum boyu medyanı / ATR250", "F4": "bölge alt fitil payı medyanı",
    "F5": "açılış-dip yakınlığı medyanı", "F6": "bölge üst fitil payı medyanı", "F7": "bölge yeşil mum payı", "F8": "bölge boyu (bar)",
    "F9": "bant (tavan / hat - 1)", "F10": "bölge net değişimi", "F11": "kırılım mumu C_t / tavan - 1", "F12": "kırılım gövdesi / bölge medyan mumu",
    "F13": "kırılım hacmi / bölge medyan hacmi", "F14": "büyük desen (250 bar) dip eğimi", "F15": "120 gün kapanış konumu",
    "F16": "son 250 barda KIRILDI bölge sayısı", "F17": "bölge öncesi 60 gün düşüş", "F18": "stop uzaklığı C_t / hat - 1",
    "F19": "parmak izi (0/1)", "F20": "kazan sağ kenarı: min L[t-5..t-1] / min L[t-15..t-6] - 1", "F21": "max H[t-15..t-1] (fiyat düzeyi)",
    "F22": "C_t / F21 - 1", "F22a": "O_t / F21 - 1", "F23": "kırılım gövdesi / mum boyu",
    "fitil20": "son 20 bar alt fitil payı ortalaması", "fitil40": "son 40 bar alt fitil payı ortalaması",
    "dip_bolge_n": "son 40 barda dip bölgesi (alt %20) bar sayısı", "dip_bolge_fitil": "son 40 bar dip bölgesi alt fitil payı ortalaması",
    "dibe_dokunus": "son 40 barda dibe (lo x 1,015) dokunan bar sayısı", "dokunus_egim": "son 40 bar dokunuş eğimi (son / ilk - 1)",
    "hacim_dus_yuk": "son 20 bar düşüş günü hacmi / yükseliş günü hacmi", "low20_onceki20": "min L son 20 / min L önceki 20",
}


def _tanim_metni(c: str) -> str:
    return f"{c}: {TZ_YENI[c]}" if c in TZ_YENI else f"{c}: {_F_ACIK.get(c, c)}"


def _f(x: Any, d: int = 3) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "—"
    return "—" if not np.isfinite(x) else f"{x:.{d}f}"


def _fe(x: Any) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "—"
    return "—" if not np.isfinite(x) else f"{x:.6g}"


def _kesif_md(K: Dict[str, Any], T: pd.DataFrame, Cf: pd.DataFrame) -> None:
    A1, A2, KO = K["ADAY_1"], K["ADAY_2"], K["KONTROL"]
    L = ["# TANIM ADIMI 2 — ADIM A: ADAY ÖZELLİKLER (KEŞİF)", "",
         f"Üretim: {K['zaman_utc']} (UTC). Etiket: **KEŞİF** (Cemal'in 40 işareti hedef: VAR {K['cemal_VAR']}, YOK {K['cemal_YOK']}). GETİRİ YOK; "
         "bütün özellikler sinyal günü t dahil, t'de kesik veriden (kör sayfanın 121 barı ya da goz_uyum anahtarındaki nedensel özellikler).", "",
         "**ÇOKLU KARŞILAŞTIRMA UYARISI:** " + f"{len(T)} tek özellik x 2 yön x ~39 eşik ve {len(Cf)} çift kural (ilk 6 adayın 15 çifti x VE / VEYA) aynı 40 "
         "sayfada denendi. 40 sayfada en iyi kuralın kappa'sı şans eseri yüksek çıkar (seçim yanlılığı); LOOCV bunu kısmen düzeltir ama sıralamada "
         "en yüksek LOOCV kappa'yı seçmek de yukarı yanlıdır. Bu yüzden buradaki sayılar bulgu değildir; seçilen kural YALNIZ ikinci bağımsız kör "
         "sette sınanır (TANIM2_ON_KAYIT.md).", "",
         "## Seçim kuralı (önceden yazılı, aynen)", "", TZ_SECIM_KURALI, "",
         "## Seçilen kurallar", "",
         f"- **ADAY_1**: {A1['tanim']}. Kural: VAR ⇔ {A1['ozellik']} {A1['yon']} {_fe(A1['esik'])} (NaN = YOK). 40 sayfada kappa {_f(A1['kappa_40'])}, "
         f"LOOCV kappa {_f(A1['loocv_kappa_40'])}.",
         ("- **ADAY_2**: yok (en iyi çift kuralın LOOCV kappa'sı ADAY_1'den en az 0,10 yüksek değil; basit olan kalır). En iyi çift: "
          f"{Cf.iloc[0].A} {Cf.iloc[0].op} {Cf.iloc[0].B}, LOOCV kappa {_f(Cf.iloc[0].loocv_kappa)}.") if A2 is None else
         (f"- **ADAY_2**: VAR ⇔ ({A2['A']} {A2['yonA']} {_fe(A2['esikA'])}) {A2['op']} ({A2['B']} {A2['yonB']} {_fe(A2['esikB'])}). "
          f"40 sayfada kappa {_f(A2['kappa_40'])}, LOOCV kappa {_f(A2['loocv_kappa_40'])}. Tanım: {A2['tanim']}."),
         f"- **KONTROL**: {KO['tanim']}; 40 sayfada kappa {_f(KO['kappa_40'])} (ilk setin hükmü).", "",
         "## Yeni özellikler (Cemal'in çizimlerinden; tanım ve pencere ölçümden önce yazıldı: tanim2.py TZ_YENI, ilk commit)", ""]
    for k, v in TZ_YENI.items():
        L.append(f"- **{k}**: {v}")
    L += ["", "## Tek özellik tablosu (LOOCV kappa sırasıyla)", "",
          "Kural: VAR ⇔ özellik (yön) eşik; eşik 40 sayfada dengeli doğruluğu en yüksek yapan. VAR / YOK sütunları: medyan [q25, q75] (NaN sayısı).", "",
          "| sıra | özellik | yön | eşik | dengeli doğr. | kappa (40) | LOOCV kappa | LOOCV uyum | kural VAR | Cemal VAR: medyan [q25, q75] (NaN) | Cemal YOK: medyan [q25, q75] (NaN) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for j, r in T.iterrows():
        gv, gy = r.dagilim["VAR"], r.dagilim["YOK"]
        L.append(f"| {j + 1} | {r.ozellik}{' (yeni)' if r.yeni else ''} | {r.yon} | {_fe(r.esik)} | {_f(r.bal)} | {_f(r.kappa)} | {_f(r.loocv_kappa)} | "
                 f"{_f(r.loocv_uyum)} | {r.tam_VAR} | {_f(gv['medyan'])} [{_f(gv['q25'])}, {_f(gv['q75'])}] ({gv['nan']}) | "
                 f"{_f(gy['medyan'])} [{_f(gy['q25'])}, {_f(gy['q75'])}] ({gy['nan']}) |")
    L += ["", f"## Çift kurallar (ilk 6: {', '.join(K['ilk6'])}; LOOCV kappa sırasıyla)", "",
          "| sıra | A | yön A | eşik A | op | B | yön B | eşik B | dengeli doğr. | kappa (40) | LOOCV kappa | LOOCV uyum | kural VAR |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for j, r in Cf.iterrows():
        L.append(f"| {j + 1} | {r.A} | {r.yonA} | {_fe(r.esikA)} | {r.op} | {r.B} | {r.yonB} | {_fe(r.esikB)} | {_f(r.bal)} | {_f(r.kappa)} | "
                 f"{_f(r.loocv_kappa)} | {_f(r.loocv_uyum)} | {r.tam_VAR} |")
    L += ["", "## Cemal'in çizim sayfalarında yeni özellikler (bilgi)", "", "| sayfa | Cemal | " + " | ".join(TZ_YENI_KOL) + " |",
          "|---|---|" + "---|" * len(TZ_YENI_KOL)]
    for p, v in K["cizim_sayfalari"].items():
        L.append(f"| {p} | {v['cemal']} | " + " | ".join(_f(v[c]) for c in TZ_YENI_KOL) + " |")
    L += ["", "Çizimler: 2 = tabanın üstünde yatay direnç (YOK), 35 = tepe bölgesi / dağıtım (YOK), 5 = orta bölgede V dönüş (VAR), 12 = yıldız (VAR).", ""]
    GU._yaz(TZ_YOL["kesif_md"], "\n".join(L))


# ================================================================ 4) ADIM B: İKİNCİ KÖR SET
def tz_yanit(r: Dict[str, Any], K: Dict[str, Any]) -> Dict[str, str]:
    """Bir sayfanın ADAY_1 / ADAY_2 / KONTROL yanıtı (mühürlü kurallarla)."""
    A1 = K["ADAY_1"]
    y1 = bool(tz_kural(np.array([r[A1["ozellik"]]], float), A1["yon"], A1["esik"])[0])
    out = {"ADAY_1": "VAR" if y1 else "YOK", "KONTROL": "VAR" if bool(r["S3"]) else "YOK", "ADAY_2": "—"}
    A2 = K.get("ADAY_2")
    if A2:
        y2 = bool(tz_cift_kural(np.array([r[A2["A"]]], float), np.array([r[A2["B"]]], float), A2, A2["op"])[0])
        out["ADAY_2"] = "VAR" if y2 else "YOK"
    return out


def tz_sec_df(H: Dict[str, pd.DataFrame], haric: set) -> Tuple[pd.DataFrame, List[str]]:
    """goz_uyum.gu_sec_df mantığı; tabaka = (ADAY_1, Ş3). Kısıt: ilk set (pazar, sembol) hariç; aynı (pazar, sembol) en çok 1; sinyal günleri >= 30 gün."""
    Eg = TZ_ESIK; rng = np.random.default_rng(int(Eg["tohum"])); notlar: List[str] = []
    hucreler = [(True, True), (True, False), (False, True), (False, False)]
    kota = [list(x) for x in Eg["sayfa"]["hucre_pazar"]]
    sira = rng.permutation(4)
    plan = {hucreler[j]: kota[int(sira[j])] for j in range(4)}
    secili: List[Dict[str, Any]] = []; kullanilan: set = set(haric); gunler: List[pd.Timestamp] = []
    mingun = int(Eg["sayfa"]["min_gun_arasi"])

    def al(pazar: str, h: Tuple[bool, bool], n: int, etiket: Tuple[bool, bool]) -> int:
        P = H[pazar]; m = (P.A1.to_numpy(bool) == h[0]) & (P.S3.to_numpy(bool) == h[1])
        idx = np.flatnonzero(m); idx = idx[rng.permutation(len(idx))]
        say = 0
        for j in idx:
            if say >= n:
                break
            r = P.iloc[int(j)]; key = (pazar, r.sembol)
            if key in kullanilan or any(abs((r.tarih - g).days) < mingun for g in gunler):
                continue
            kullanilan.add(key); gunler.append(r.tarih)
            secili.append({**r.to_dict(), "hucre_A1": etiket[0], "hucre_S3": etiket[1], "hucre_gercek": f"A1={h[0]} S3={h[1]}"}); say += 1
        return say
    for h in hucreler:
        for pi, pazar in enumerate(["ABD", "AVR", "BIST"]):
            n = plan[h][pi]; g = al(pazar, h, n, h)
            if g < n:
                notlar.append(f"hücre A1={h[0]} S3={h[1]} {pazar}: kota {n}, bulunan {g}")
    hedef = int(Eg["sayfa"]["hucre"])
    for h in hucreler:
        eks = hedef - sum(1 for x in secili if (x["hucre_A1"], x["hucre_S3"]) == h)
        if eks > 0:
            g = al("ABD", h, eks, h); notlar.append(f"hücre A1={h[0]} S3={h[1]}: {eks} eksik ABD'den tamamlandı ({g})")
            eks -= g
        if eks > 0:                                                       # en yakın: aynı ADAY_1 değerli öteki hücre, sonra herhangi
            for h2 in [(h[0], not h[1])] + [z for z in hucreler if z[0] != h[0]]:
                for pazar in ("ABD", "AVR", "BIST"):
                    if eks <= 0:
                        break
                    g = al(pazar, h2, eks, h); eks -= g
                    if g:
                        notlar.append(f"hücre A1={h[0]} S3={h[1]}: {g} sayfa en yakın hücreden (A1={h2[0]} S3={h2[1]}, {pazar}) alındı")
            if eks > 0:
                raise TZHata(f"hücre {h}: 10 sayfa dolmadı")
    S = pd.DataFrame(secili)
    for pz in ("ABD", "AVR", "BIST"):
        if int((S.pazar == pz).sum()) != Eg["sayfa"][pz]:
            notlar.append(f"pazar {pz}: {int((S.pazar == pz).sum())} sayfa (hedef {Eg['sayfa'][pz]})")
    S = S.iloc[rng.permutation(len(S))].reset_index(drop=True)
    S.insert(0, "sayfa", np.arange(1, len(S) + 1))
    return S, notlar


def tz_sec(islem: int = 4) -> Dict[str, Any]:
    if not os.path.exists(TZ_YOL["kesif"]):
        raise TZHata("önce 'aday' (tanim2_kesif.json yok)")
    K = json.load(open(TZ_YOL["kesif"], encoding="utf-8"))
    if K.get("esik_sha") != _sha_esik():
        raise TZHata("TZ_ESIK keşiften sonra değişmiş -> DURDU")
    ilk = json.load(open(TZ_YOL["ilk_anahtar"], encoding="utf-8"))["sayfalar"]
    haric = {(s["pazar"], s["sembol"]) for s in ilk}
    H: Dict[str, pd.DataFrame] = {}
    havuz_ozet: Dict[str, Any] = {}
    for p in ("ABD", "AVR", "BIST"):
        P = GU.gu_havuz(p, islem)
        n0 = len(P)
        P = P[[(p, s) not in haric for s in P.sembol]].reset_index(drop=True)
        V = GU.gu_veri(p); yeni = []
        for r in P.itertuples(index=False):
            W = tz_pencere(p, r.sembol, pd.Timestamp(r.tarih), V)
            yeni.append(tz_yeni_ozellik(W))
        del V
        P = pd.concat([P, pd.DataFrame(yeni, index=P.index)], axis=1)
        P["A1"] = [tz_yanit(r, K)["ADAY_1"] == "VAR" for r in P.to_dict("records")]
        H[p] = P
        havuz_ozet[p] = {"n_havuz": int(n0), "n_ilk_set_haric": int(len(P)),
                         "hucre": {f"A1={a}_S3={b}": int(((P.A1 == a) & (P.S3 == b)).sum()) for a in (True, False) for b in (True, False)}}
        tzlog.info("%s havuz: %d olay (ilk set hariç %d); hücreler %s", p, n0, len(P), havuz_ozet[p]["hucre"])
    S, notlar = tz_sec_df(H, haric)
    sayfalar = []
    for d in S.to_dict("records"):
        sat = {"sayfa": int(d["sayfa"]), "pazar": d["pazar"], "sembol": d["sembol"], "sinyal_gunu": pd.Timestamp(d["tarih"]).strftime("%Y-%m-%d"),
               "hucre": f"A1={d['hucre_A1']} S3={d['hucre_S3']}", "hucre_gercek": d["hucre_gercek"],
               "S1": bool(d["S1"]), "S3": bool(d["S3"]), "S5": bool(d["S5"]), "yanit": tz_yanit(d, K),
               "deger_medyan": d["deger_medyan"], "fiyat": d["fiyat"]}
        for c in tz_aday_kolonlar():
            if c in d:
                sat[c] = d[c]
        sayfalar.append(sat)
    if any(s["hucre"] != s["hucre_gercek"] for s in sayfalar):
        notlar.append("bazı sayfalar hücresine en yakın hücreden alındı (hucre_gercek sütunu)")
    for s in sayfalar:
        if (s["pazar"], s["sembol"]) in haric:
            raise TZHata("ilk set (pazar, sembol) ikinci sete girdi")
        if (s["yanit"]["ADAY_1"] == "VAR") != s["hucre_gercek"].startswith("A1=True"):
            raise TZHata("ADAY_1 yanıtı hücreyle tutarsız")
    J = {"surum": "TANIM2 v1.0 (23.11.2026)", "uyari": "GİZLİ ANAHTAR: Cemal işaretlemeden önce açılmaz; mühür TANIM2_ON_KAYIT.md'de.",
         "esik": TZ_ESIK, "esik_sha": _sha_esik(), "kesif_sha": GU._sha(TZ_YOL["kesif"]),
         "kurallar": {"ADAY_1": K["ADAY_1"], "ADAY_2": K["ADAY_2"], "KONTROL": K["KONTROL"]},
         "havuz": havuz_ozet, "notlar": notlar, "sayfalar": sayfalar}
    GU._jyaz(TZ_YOL["anahtar"], J)
    tzlog.info("anahtar yazıldı: %d sayfa; notlar: %s", len(sayfalar), notlar)
    return J


# ================================================================ 5) PDF (goz_uyum ile aynı sayfa tasarımı)
def tz_pdf() -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    J = json.load(open(TZ_YOL["anahtar"], encoding="utf-8")); sayfalar = J["sayfalar"]
    Vc: Dict[str, Dict[str, pd.DataFrame]] = {}
    gw, gh = GU.GU_ESIK["gorsel"]["sayfa_in"]
    meta = {"Title": "TANIM2 KOR SET", "Author": "", "Creator": "", "Producer": "", "CreationDate": None, "ModDate": None}
    with PdfPages(TZ_YOL["pdf"] + ".tmp", metadata=meta) as pp:
        fig = plt.figure(figsize=(gw, gh))
        fig.text(0.5, 0.80, "İkinci set.", fontsize=30, ha="center", fontweight="bold")
        fig.text(0.5, 0.72, "Soru aynı: DİP SAVUNMASI var mı?", fontsize=24, ha="center")
        fig.text(0.5, 0.64, "VAR / YOK / ?", fontsize=26, ha="center", fontweight="bold")
        fig.text(0.5, 0.52, "Her sayfaya VAR ya da YOK yaz\n(emin değilsen ?).", fontsize=22, ha="center", linespacing=1.5)
        fig.text(0.5, 0.38, "Sonrası yok, hisse adı yok.", fontsize=20, ha="center")
        fig.text(0.5, 0.30, f"{len(sayfalar)} sayfa.", fontsize=20, ha="center")
        pp.savefig(fig); plt.close(fig)
        for s in sorted(sayfalar, key=lambda z: z["sayfa"]):
            p = s["pazar"]
            if p not in Vc:
                Vc[p] = GU.gu_veri(p)
            W = tz_pencere(p, s["sembol"], pd.Timestamp(s["sinyal_gunu"]), Vc[p])
            fig = GU.gu_sayfa_ciz(W, s["sayfa"], len(sayfalar)); pp.savefig(fig); plt.close(fig)
    os.replace(TZ_YOL["pdf"] + ".tmp", TZ_YOL["pdf"])
    mb = os.path.getsize(TZ_YOL["pdf"]) / 2 ** 20
    if mb >= 6:
        raise TZHata(f"PDF {mb:.1f} MB >= 6 MB")
    return {"pdf": TZ_YOL["pdf"], "boyut_mb": round(mb, 2), "sayfa": len(sayfalar) + 1}


# ================================================================ 6) MÜHÜR
TZ_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralların uyumu, kappa)"),
    "K2": ("EVET", "yeni özellikler yalnız kör sayfa penceresinden: tz_pencere = goz_uyum._gu_pencere (veri t'de KESİK, son 121 bar) + mekanik denetim "
                   "(W.index.max() <= t, W.index[-1] == t); havuz goz_uyum.gu_havuz (veri sinyal çağı sonunda kesik, F1-F23 nedensel); "
                   "test: tanim2.py test prefix değişmezliği (t sonrası değişince yeni özellikler aynı); getiri / sinyal sonrası fiyat hiç okunmaz"),
    "K3": ("EVET", "GE.ge_hazir (H>L, V>0, O/H/L/C>0) geçerli bar; havuz ve pencere goz_uyum ile aynı"),
    "K4": ("EVET", "havuzda aynı hissede 60 bar tekil (goz_uyum._gu_isci); ikinci sette aynı (pazar, sembol) en çok 1, ilk setin 40 (pazar, sembol) çifti hariç, "
                   "sinyal günleri arası >= 30 gün (tz_sec_df); n = 40 bağımsız sayfa"),
    "K5": ("UYGULANMAZ", "giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik"),
    "K6": ("EVET", "tek kip V_*.pkl (goz_uyum ile aynı); yeni özellikler birimsiz oran / bar sayısı; AVR likidite EUR (Close x Kur)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok; raporda yazılı"),
    "K8": ("EVET", "keşif 40 sayfa küçük örneklem: TANIM2_KESIF 'keşif' etiketli + çoklu karşılaştırma uyarısı (tek ~32 özellik, 30 çift kural); seçilen kural "
                   "YALNIZ ikinci bağımsız 40 sayfada sınanır; karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); pazar dağılımı ABD 30 / AVR 5 / BIST 5"),
    "K9": ("EVET", "yeni özellik tanımları + seçim kuralı keşiften önce commit (TZ_YENI, TZ_SECIM_KURALI; ilk commit); ADAY eşikleri SAYI olarak bu dosyada; "
                   "anahtar + PDF + kesif + tanim2.py + TZ_ESIK sha'ları burada; bu dosya Cemal işaretlemeden ÖNCE commit; hüküm eşikleri sabit"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırma yok; yalnız OHLCV"),
    "K11": ("EVET", "tohum 20261124 ile anahtar aynı komutla yeniden üretilir; olc komutu anahtardan tabloyu yeniden kurar; keşif tabloları tanim2_kesif.json'dan"),
    "K12": ("EVET", "iddia yok; yalnız 'uyum' ve 'kappa' sayısı; keşif sayıları 'bulgu' denmez; hüküm sözü yalnız ön kayıttaki eşikle"),
    "K13": ("EVET", "çakışma kapısı _CK_ONCE_TZ + test; yasak dosyalar (defter, mevcut .py, goz_uyum.py / anahtar / GOZ_UYUM_*, kart / kart2 / kasa) "
                    "değiştirilmedi (git status); e-posta taraması GU._yaz / _jyaz; kod değiştiyse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


def tz_muhur() -> str:
    for y in (TZ_YOL["anahtar"], TZ_YOL["pdf"], TZ_YOL["kesif"], TZ_YOL["kesif_md"], TZ_YOL["is_tanimi"]):
        if not os.path.exists(y):
            raise TZHata(f"mühür için dosya yok: {y}")
    J = json.load(open(TZ_YOL["anahtar"], encoding="utf-8")); S = pd.DataFrame(J["sayfalar"]); Kr = J["kurallar"]
    if J["esik_sha"] != _sha_esik():
        raise TZHata("TZ_ESIK anahtardan sonra değişmiş")
    ad = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
          "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
          "K13": "süreç", "K14": "boyut (gerçek para)"}
    tab = "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |\n|---|---|---|---|\n"
    for k, (y, kn) in TZ_KONTROL.items():
        tab += f"| {k} | {ad[k]} | {y} | {kn} |\n"
    A1, A2 = Kr["ADAY_1"], Kr["ADAY_2"]
    a2 = ("yok (seçim kuralı: en iyi çift kuralın LOOCV kappa'sı ADAY_1'den en az 0,10 yüksek değil)" if not A2 else
          f"VAR ⇔ ({A2['A']} {A2['yonA']} {A2['esikA']!r}) {A2['op']} ({A2['B']} {A2['yonB']} {A2['esikB']!r}) (NaN = YOK); 40 sayfada kappa "
          f"{_f(A2['kappa_40'])}, LOOCV {_f(A2['loocv_kappa_40'])}")
    hucre = S.groupby(["hucre", "pazar"]).size().to_dict()
    yan = pd.DataFrame(list(S.yanit))
    m = f"""# TANIM ADIMI 2 — İKİNCİ KÖR SET — ÖN KAYIT (Cemal işaretlemeden ÖNCE mühürlenir)

Üretim: {GU._simdi()} (UTC). Soru: Cemal'in 'dip savunması VAR' gözü, ilk 40 sayfadan seçilen ölçülebilir kuralla (ADAY_1 / ADAY_2) BAĞIMSIZ ikinci sette örtüşüyor mu? GETİRİ ÖLÇÜLMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/tanim2_anahtar.json` sha256: `{GU._sha(TZ_YOL['anahtar'])}`
- PDF: `arastirma_cikti/goz_uyum/TANIM2_KOR.pdf` sha256: `{GU._sha(TZ_YOL['pdf'])}`
- keşif: `arastirma_cikti/goz_uyum/tanim2_kesif.json` sha256: `{GU._sha(TZ_YOL['kesif'])}`
- keşif raporu: `arastirma_cikti/goz_uyum/TANIM2_KESIF.md` sha256: `{GU._sha(TZ_YOL['kesif_md'])}`
- kod: `arastirma_cikti/goz_uyum/tanim2.py` sha256: `{GU._sha(TZ_YOL['kod'])}`
- eşik sözlüğü (TZ_ESIK) sha256: `{_sha_esik()}`
- iş tanımı: `arastirma_cikti/goz_uyum/TANIM2_IS_TANIMI.md` sha256: `{GU._sha(TZ_YOL['is_tanimi'])}`
- bağımlı kod: goz_uyum.py `{GU._sha(GU.GU_YOL['kod'])[:16]}`, GOZ_ETIKET.py `{GU._sha(os.path.join(KOK, 'GOZ_ETIKET.py'))[:16]}`, YAPI_HEDEF.py `{GU._sha(os.path.join(KOK, 'YAPI_HEDEF.py'))[:16]}`

## 2. Seçim kuralı (iş tanımından aynen; keşiften önce yazıldı)
{TZ_SECIM_KURALI}

## 3. Mühürlü kurallar (SAYI; 40 sayfanın tamamıyla seçildi; NaN = YOK)
- **ADAY_1**: VAR ⇔ {A1['ozellik']} {A1['yon']} {A1['esik']!r}. Tanım: {A1['tanim']}. 40 sayfada kappa {_f(A1['kappa_40'])}, LOOCV kappa {_f(A1['loocv_kappa_40'])} (keşif).
- **ADAY_2**: {a2}.
- **KONTROL**: eski Ş3, VAR ⇔ F2 >= -0,01 (değişmez); ilk sette kappa {_f(Kr['KONTROL']['kappa_40'])}.

## 4. Örneklem (tohum {TZ_ESIK['tohum']})
Havuz: {TZ_ESIK['kaynak_havuz']}; ilk setin 40 (pazar, sembol) çifti hariç. Dönem: ABD / AVR 2001-01-01..2023-06-30; BIST 2016-01-01..2017-12-31 ve 2021-03-01..2023-06-30.
40 sayfa: ABD 30, AVR 5, BIST 5; tabaka ADAY_1 x KONTROL (Ş3), hücre başına 10; aynı hisseden en çok 1; sinyal günleri arası >= 30 gün; sayfa sırası rastgele.
Havuz hücreleri: {json.dumps(J['havuz'], ensure_ascii=False)}
Tabaka dağılımı (hücre, pazar -> sayfa): {json.dumps({f'{a} {b}': v for (a, b), v in hucre.items()}, ensure_ascii=False)}
Yanıt sayıları: ADAY_1 VAR {int((yan.ADAY_1 == 'VAR').sum())}, KONTROL VAR {int((yan.KONTROL == 'VAR').sum())}, ADAY_2 VAR {int((yan.ADAY_2 == 'VAR').sum())}.
Notlar: {json.dumps(J['notlar'], ensure_ascii=False)}

## 5. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in ikinci setteki VAR / YOK işaretleri ile ADAY_1, (varsa) ADAY_2 ve KONTROL arasında uyum ve Cohen kappa; '?' karar dışı, sayısı ayrıca yazılır; kappa bootstrap %95 aralığı (B {TZ_ESIK['kappa']['B']}, tohum {TZ_ESIK['kappa']['tohum']}, sayfa yeniden örneklemesi).
- HÜKÜM: {TZ_ESIK['hukum']}.
- Eşik ve kural sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 6. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
{tab}
## 7. Git kaydı (bu dosyanın yazıldığı an)
- tanim2.py: {GU._gu_git('arastirma_cikti/goz_uyum/tanim2.py')}
"""
    GU._yaz(TZ_YOL["onkayit"], m)
    import IZ_KARNE as IK
    r = IK.ik_kontrol_kapisi(TZ_YOL["onkayit"])
    tzlog.info("kontrol kapısı: %s", "GEÇTİ" if r["gecti"] else r)
    return TZ_YOL["onkayit"]


# ================================================================ 7) ÖLÇÜM (olc)
def _tz_muhur_oku() -> Dict[str, str]:
    if not os.path.exists(TZ_YOL["onkayit"]):
        raise TZHata("ön kayıt yok")
    t = open(TZ_YOL["onkayit"], encoding="utf-8").read(); out = {}
    for ad, anahtar in (("anahtar", "tanim2_anahtar.json"), ("pdf", "TANIM2_KOR.pdf"), ("kesif", "tanim2_kesif.json")):
        m = re.search(re.escape(anahtar) + r"` sha256: `([0-9a-f]{64})`", t)
        if not m:
            raise TZHata(f"ön kayıtta {ad} sha'sı yok")
        out[ad] = m.group(1)
    m = re.search(r"eşik sözlüğü \(TZ_ESIK\) sha256: `([0-9a-f]{64})`", t)
    if not m:
        raise TZHata("ön kayıtta TZ_ESIK sha'sı yok")
    out["esik"] = m.group(1)
    return out


def tz_hukum(k: float, alt: float, n: int) -> str:
    E = TZ_ESIK["kappa"]
    if n < int(E["karar_min"]) or not np.isfinite(k):
        return "ÖLÇÜLEMEDİ (karar sayısı < 30 ya da kappa tanımsız)"
    if k >= E["gecerli"] and np.isfinite(alt) and alt >= E["gecerli_alt"]:
        return "TANIM GEÇERLİ"
    return "KISMEN" if k >= E["kismen"] else "GEÇERSİZ"


def tz_olc(cemal_yol: str) -> Dict[str, Any]:
    M = _tz_muhur_oku()
    for ad, y in (("anahtar", TZ_YOL["anahtar"]), ("pdf", TZ_YOL["pdf"]), ("kesif", TZ_YOL["kesif"])):
        if GU._sha(y) != M[ad]:
            raise TZHata(f"MÜHÜR BOZUK: {ad} sha'sı ön kayıttakiyle aynı değil -> DURDU")
    if _sha_esik() != M["esik"]:
        raise TZHata("MÜHÜR BOZUK: TZ_ESIK sha'sı ön kayıttakiyle aynı değil -> DURDU")
    J = json.load(open(TZ_YOL["anahtar"], encoding="utf-8")); S = pd.DataFrame(J["sayfalar"])
    C = json.load(open(cemal_yol, encoding="utf-8"))
    cem = {int(k): GU.gu_norm(v) for k, v in C.items()}
    eksik = sorted(set(S.sayfa) - set(cem)); fazla = sorted(set(cem) - set(S.sayfa))
    if eksik or fazla:
        raise TZHata(f"yanıt sayfaları anahtarla uyuşmuyor: eksik {eksik}, fazla {fazla}")
    S["cemal"] = S.sayfa.map(cem)
    soru = int((S.cemal == "?").sum()); K = S[S.cemal != "?"].copy(); n = len(K)
    E = TZ_ESIK["kappa"]; cb = (K.cemal == "VAR").to_numpy(bool)
    sonuc: Dict[str, Any] = {"n_sayfa": int(len(S)), "soru_isareti": soru, "karar_n": n, "cemal_VAR": int(cb.sum()), "modeller": {}}
    adlar = ["ADAY_1"] + (["ADAY_2"] if J["kurallar"].get("ADAY_2") else []) + ["KONTROL"]
    for ad in adlar:
        mod = (K.yanit.map(lambda z: z[ad]) == "VAR").to_numpy(bool)
        k = GU.gu_kappa(cb, mod)
        ar = GU.gu_boot(cb, mod, int(E["B"]), int(E["tohum"])) if n else {"alt": np.nan, "ust": np.nan, "gecersiz": 0}
        tp, tn = int((cb & mod).sum()), int((~cb & ~mod).sum()); fp, fn = int((~cb & mod).sum()), int((cb & ~mod).sum())
        sonuc["modeller"][ad] = {"uyum": float(np.mean(cb == mod)) if n else np.nan, "kappa": k, "aralik": ar,
                                 "hukum": tz_hukum(k, ar["alt"], n) if ad != "KONTROL" else "karşılaştırma (hüküm yok)",
                                 "tablo": {"Cemal VAR + kod VAR": tp, "Cemal YOK + kod YOK": tn, "Cemal YOK + kod VAR": fp, "Cemal VAR + kod YOK": fn},
                                 "uyusmayan": [int(s) for s in K.sayfa[cb != mod]]}
    a1 = (K.yanit.map(lambda z: z["ADAY_1"]) == "VAR").to_numpy(bool); K["_ok"] = cb == a1
    sonuc["bilgi_pazar"] = {p: {"n": int(len(g)), "uyum": float(g._ok.mean())} for p, g in K.groupby("pazar")}
    sonuc["bilgi_hucre"] = {h: {"n": int(len(g)), "uyum": float(g._ok.mean()), "Cemal_VAR": int((g.cemal == "VAR").sum())} for h, g in K.groupby("hucre")}
    Kr = J["kurallar"]
    L = ["# TANIM ADIMI 2 — İKİNCİ KÖR SET — SONUÇ", "", f"Üretim: {GU._simdi()} (UTC). Mühür denetimi: anahtar, PDF, keşif ve TZ_ESIK sha'ları ön kayıtla aynı.", "",
         f"Sayfa {len(S)}; karar (VAR / YOK) {n} (Cemal VAR {int(cb.sum())}); '?' (karar dışı) {soru}.", "",
         f"- ADAY_1: VAR ⇔ {Kr['ADAY_1']['ozellik']} {Kr['ADAY_1']['yon']} {Kr['ADAY_1']['esik']!r}",
         f"- ADAY_2: {'yok' if not Kr.get('ADAY_2') else Kr['ADAY_2']['tanim']}", "- KONTROL: eski Ş3 (F2 >= -0,01)", "",
         "| model | uyum | kappa | %95 aralık (B 5000) | hüküm |", "|---|---|---|---|---|"]
    for ad, r in sonuc["modeller"].items():
        L.append(f"| {ad} | {_f(r['uyum'])} | {_f(r['kappa'])} | [{_f(r['aralik']['alt'])}, {_f(r['aralik']['ust'])}] | {r['hukum']} |")
    L += ["", f"HÜKÜM kuralı (ön kayıt): {TZ_ESIK['hukum']}.", ""]
    for ad, r in sonuc["modeller"].items():
        L += [f"### {ad}: 2x2", "", "| | sayı |", "|---|---|"] + [f"| {k} | {v} |" for k, v in r["tablo"].items()]
        L += ["", f"Uyuşmayan sayfalar ({len(r['uyusmayan'])}): {r['uyusmayan']}", ""]
    L += ["## Bilgi: ADAY_1 uyumu pazar ve hücre bazında (küçük n; hüküm değil)", "", "| grup | n | uyum |", "|---|---|---|"]
    for k, v in sonuc["bilgi_pazar"].items():
        L.append(f"| {k} | {v['n']} | {_f(v['uyum'])} |")
    for k, v in sonuc["bilgi_hucre"].items():
        L.append(f"| {k} (Cemal VAR {v['Cemal_VAR']}) | {v['n']} | {_f(v['uyum'])} |")
    GU._yaz(TZ_YOL["sonuc"], "\n".join(L) + "\n")
    GU._jyaz(TZ_YOL["sonuc_json"], sonuc)
    return sonuc


# ================================================================ 8) TEST
def tz_cakisma_kontrol() -> None:
    ez = [k for k, v in _CK_ONCE_TZ.items() if k in globals() and id(globals()[k]) != v and not k.startswith("_")]
    if ez:
        raise TZHata(f"çakışma kapısı: bellekteki mevcut ad(lar) ezildi: {ez[:5]}")


def tz_test() -> Dict[str, Any]:
    tz_cakisma_kontrol()
    GU.gu_test()
    # yeni özellik prefix değişmezliği: t sonrası pencereye hiç girmez (pencere = son 121 bar); burada pencere sonrası dizi değişince aynı
    rng = np.random.default_rng(3); n = 200
    C = 100 + np.cumsum(rng.normal(0, 1, n)); O = C + rng.normal(0, .3, n); H = np.maximum(O, C) + abs(rng.normal(0, .5, n)) + .1
    L = np.minimum(O, C) - abs(rng.normal(0, .5, n)) - .1; V = rng.uniform(1e3, 2e3, n)
    i = 150; s = slice(i - 120, i + 1)
    x1 = tz_yeni_ozellik_dizi(O[s], H[s], L[s], C[s], V[s])
    O2, H2, L2, C2, V2 = O.copy(), H.copy(), L.copy(), C.copy(), V.copy()
    O2[i + 1:] = 1; H2[i + 1:] = 2; L2[i + 1:] = 0.5; C2[i + 1:] = 1.5; V2[i + 1:] = 7
    x2 = tz_yeni_ozellik_dizi(O2[s], H2[s], L2[s], C2[s], V2[s])
    assert all((np.isnan(x1[k]) and np.isnan(x2[k])) or x1[k] == x2[k] for k in TZ_YENI_KOL), "yeni özellik t sonrasına bağlı"
    assert sum(np.isfinite(x1[k]) for k in TZ_YENI_KOL) >= 6, "yeni özellikler çoğunlukla NaN"
    # kural seçimi sağlaması: ayrılabilir veri -> dengeli doğruluk 1, doğru yön
    y = np.array([0, 0, 0, 1, 1, 1], bool); x = np.array([1., 2, 3, 4, 5, 6])
    r = tz_tek_sec(x, y); assert r["yon"] == ">=" and r["esik"] == 3.5 and abs(r["bal"] - 1) < 1e-12, r
    r = tz_tek_sec(-x, y); assert r["yon"] == "<=" and r["esik"] == -3.5, r
    assert tz_kural(np.array([np.nan, 5.0]), ">=", 3.5).tolist() == [False, True]
    rc = tz_cift_sec(x, x[::-1].copy(), y, "VE"); assert abs(rc["bal"] - 1) < 1e-12, rc
    assert (tz_loocv_tek(np.array([1., 2, 3, 10, 11, 12]), y) == y).all()
    return {"tamam": True}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", choices=["aday", "sec", "pdf", "muhur", "olc", "test"])
    ap.add_argument("--islem", type=int, default=4)
    ap.add_argument("--cemal", default=None)
    a = ap.parse_args()
    if a.komut == "aday":
        K = tz_aday(); print(json.dumps({"ADAY_1": K["ADAY_1"], "ADAY_2": K["ADAY_2"]}, ensure_ascii=False, default=str))
    elif a.komut == "sec":
        J = tz_sec(a.islem); print(json.dumps({"sayfa": len(J["sayfalar"]), "notlar": J["notlar"]}, ensure_ascii=False))
    elif a.komut == "pdf":
        print(tz_pdf())
    elif a.komut == "muhur":
        print(tz_muhur())
    elif a.komut == "olc":
        if not a.cemal:
            raise SystemExit("olc için --cemal J.json gerekli")
        r = tz_olc(a.cemal); print(json.dumps({k: r[k] for k in ("n_sayfa", "soru_isareti", "karar_n")}, ensure_ascii=False))
    else:
        print(tz_test())
