"""DS5 — DİP SAVUNMASI v5: Cemal'in DS4 görselini görünce verdiği tarif (23 Kasım 2026). GETİRİ ÖLÇMEZ.

Cemal (23.11.2026, aynen): "Of ya, bu sefer de tamam düşeni kırmış ama düşeni kıran tek bir mum: dip savunması vardır denilmez ki. Bu
düşeni kıran, alt gövdesi küçük, eğimi yukarı bir çizim olan şeye ben dip savunması vardır [derim]. Yani dip savunması en derinden yukarı
veya yatay bir çizgi takip eden mumları takip ederek var / yok demeli."
Ana model yorumu: DİP SAVUNMASI = en derin noktadan başlayıp YATAY ya da YUKARI eğimli bir çizgiyi TAKİP EDEN bir mum DİZİSİ; çizgi
mumların GÖVDE ALTLARINDAN (min(Open, Close)) geçer; tek mum yetmez; mumlar çizgiye tekrar tekrar yaklaşır, gövdeler çizginin altına inmez.
EK (Cemal, 23 Kas): "... bu yukarıdan sayılan mumların bir düşeni kırıyor olması gerekir; yani basit bir tepki içindeki dizilmiş mumlara dip
savunması var demesin kod." -> P5 (dizi DS4 düşen çizgisini kırıyor ve kırılımdan sonra da çizgiyi takip ediyor).
DS3 / DS4 dersi: önce sentetik sınama (test) -> 80 sayfa yanıtı + görsel onay PDF'i mühür (etiketler AÇILMADAN) -> ölçüm (olc).

Sinyal sonrası fiyat hiçbir adımda okunmaz: pencere = kör sayfa penceresi (tanim2.tz_pencere = goz_uyum._gu_pencere; veri sinyal günü t'de
KESİLİR, son 121 geçerli bar; kural penceresi son 120 mum [t-119 .. t]).
Komutlar (repo kökünden):
  python arastirma_cikti/goz_uyum/ds5.py test                  çakışma kapısı + sentetik seriler S1-S12 + prefix değişmezliği
  python arastirma_cikti/goz_uyum/ds5.py anahtar               iki setin 80 sayfası: ara değerler + V1 / V2 / V3 -> ds5_anahtar.json
  python arastirma_cikti/goz_uyum/ds5.py onay [--havuz_onbellek X.pkl]
                                                               iki set + DS4 onay seti dışından 24 yeni sayfa -> DS5_ONAY.pdf + ds5_onay_anahtar.json
  python arastirma_cikti/goz_uyum/ds5.py muhur                 sha'lar + kural + sentetik tablo + hüküm + kontrol tablosu -> DS5_ON_KAYIT.md
  python arastirma_cikti/goz_uyum/ds5.py olc                   mühür denetimi + etiketleri AÇAR -> DS5_SONUC.md, ds5_sonuc.json
  (deneme: olc --deneme --cemal1 X.json --cemal2 Y.json --cikti DIZIN -> mühür denetimi yok, uydurma etiketle kod yolu sınaması)
Veri: /tmp/kasa2/acik (V_ABD.pkl, V_AVR.pkl), /tmp/kasa/acik/V_BIST.pkl (goz_uyum.GU_VERI).  Kod değiştiyse çalışma zamanını yeniden başlat.
"""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import logging
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

_CK_ONCE_DS5 = {k: id(v) for k, v in globals().items()}

import numpy as np
import pandas as pd

DS5_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(os.getcwd(), "arastirma_cikti", "goz_uyum")
if DS5_DIR not in sys.path:
    sys.path.insert(0, DS5_DIR)
import goz_uyum as GU  # noqa: E402  (yalnız okunur: gu_veri, gu_havuz, _sha, _jyaz, _yaz, _simdi, _gu_git, gu_kappa, gu_norm)
import tanim2 as TZ  # noqa: E402  (yalnız okunur: tz_pencere, TZ_YOL)

d5log = logging.getLogger("ds5")
if not d5log.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

KOK5 = GU.KOK
DS5_YOL = {"is_tanimi": os.path.join(DS5_DIR, "DS5_IS_TANIMI.md"), "anahtar": os.path.join(DS5_DIR, "ds5_anahtar.json"),
           "onkayit": os.path.join(DS5_DIR, "DS5_ON_KAYIT.md"), "sonuc": os.path.join(DS5_DIR, "DS5_SONUC.md"),
           "sonuc_json": os.path.join(DS5_DIR, "ds5_sonuc.json"), "pdf": os.path.join(DS5_DIR, "DS5_ONAY.pdf"),
           "onay_anahtar": os.path.join(DS5_DIR, "ds5_onay_anahtar.json"),
           "set1_anahtar": GU.GU_YOL["anahtar"], "set2_anahtar": TZ.TZ_YOL["anahtar"],
           "set1_cemal": os.path.join(DS5_DIR, "cemal_isaret.json"), "set2_cemal": os.path.join(DS5_DIR, "cemal_isaret2.json"),
           "govde_anahtar": os.path.join(DS5_DIR, "govde_anahtar.json"), "ds3_anahtar": os.path.join(DS5_DIR, "ds3_anahtar.json"),
           "ds4_anahtar": os.path.join(DS5_DIR, "ds4_anahtar.json"), "ds4_onay_anahtar": os.path.join(DS5_DIR, "ds4_onay_anahtar.json"),
           "kod": os.path.abspath(__file__) if "__file__" in globals() else os.path.join(DS5_DIR, "ds5.py")}

# ---------------------------------------------------------------- KURAL (Cemal'in tarifinden; etiketler okunmadan yazıldı; ADIM 1 commit'i)
# W = kör sayfa penceresi (121 geçerli bar, dizin 0..120, t = 120); kural penceresi = son 120 mum, dizin s0 = 1 .. t (t-119 .. t).
# B_i = min(O_i, C_i) (gövde altı). ATR = ATR14(d).
# DİP: d = [s0 .. t-8] aralığında en düşük Low'un günü (eşitlikte EN SON); m = t - d (>= 8).
# P1 DÜŞÜŞTEN DİP: max High [s0 .. d-1] / Low(d) - 1 >= 0,20.
# ÇİZGİ: çapa (d, B_d); s* = min_{i = d+1..t} (B_i - B_d) / (i - d); L(i) = B_d + s* (i - d) (gövde altlarının alt destek çizgisi).
# P2 YATAY / YUKARI: s* >= -0,05 x ATR / 20.
# P3 TAKİP: dokunuş = d < i <= t ve B_i - L(i) < 0,35 x ATR; en az 3 dokunuş VE ilk yarıda (i - d <= m / 2) >= 1 VE ikinci yarıda (> m / 2) >= 1.
# P4 DİP KORUNUR: d < i <= t için hiçbir Low_i < Low(d) - 0,25 x ATR.
# P5 DİZİ DÜŞEN ÇİZGİYİ KIRIYOR (EK, 23 Kas): düşen çizgi DS4 tanımı (pivot tepe 5/5, j+5 <= d; H1 = en yüksek; H2 = H1'den sonra H1'den
#    alçak SON pivot tepe, yoksa H1'den sonraki en yüksek; eğim < 0 şart); d < i <= t kapanışı çizginin üstünde en az 3 mum VE C_t > çizgi_t
#    VE en az bir P3 dokunuşu ilk kırılım gününden (ilk C_i > çizgi_i) SONRA.
# V1 (ANA) = P1 ∧ P2 ∧ P3 ∧ P4 ∧ P5.  V2 = V1 ∧ (ortalama alt fitil (B_i - Low_i) dip sonrası < dipten önceki 20 mum).
# V3 = P1 ∧ P2 ∧ P3 ∧ P4 (V1 ama P5 yok: basit tepki dahil).
DS5_ESIK: Dict[str, Any] = {
    "pencere_bar": 121, "kural_bar": 120, "dip_sonrasi_min": 8, "dusus_min": 0.20, "atr_n": 14,
    "egim_atr": 0.05, "egim_bar": 20, "dokunus_atr": 0.35, "dokunus_min": 3, "delinme_atr": 0.25, "fitil_once_bar": 20,
    "tepe_sol": 5, "tepe_sag": 5, "kirilim_kapanis_min": 3,
    "belirsizlik": {
        "dip": "d = [t-119 .. t-8] aralığında en düşük Low'un günü; eşit en düşük Low birden çok günde ise EN SON gün (float ==). En düşük Low "
               "son 7 mumdaysa (t-7..t) d oraya gidemez; o mum dibi 0,25 ATR'den fazla deliyorsa P4 YANLIŞ olur. Bu tanım gereği d+1 .. t-8 "
               "arasında Low(d)'den düşük Low yoktur; P4 yalnız son 7 mumda bağlayıcıdır",
        "p1": "tepe = max High [t-119 .. d-1] (d hariç; d = t-119 ise tepe yok -> P1 YANLIŞ); oran = tepe / Low(d) - 1 >= 0,20",
        "govde": "B_i = min(Open_i, Close_i) (gövde altı; doji'de Open = Close)",
        "cizgi": "çapa (d, B_d); s* = min (B_i - B_d) / (i - d), i = d+1 .. t (tanım gereği bütün dip sonrası gövde altları çizginin üstünde ya "
                 "da üzerinde; en az bir mum çizginin ÜZERİNDE = mesafe 0); L(i) = B_d + s* (i - d), sağa t'ye kadar",
        "atr": "TR_j = max(H_j - L_j, |H_j - C_{j-1}|, |L_j - C_{j-1}|); ATR14(d) = ortalama TR, j = max(1, d-13) .. d (121 barlık pencerenin "
               "dizini; dizin 0 yalnız önceki kapanış olarak kullanılabilir) (DS4 ile aynı)",
        "p2": "s* >= -0,05 x ATR14(d) / 20 (eşitlik geçer)",
        "dokunus": "d < i <= t ve B_i - L(i) < 0,35 x ATR14(d) (kesin küçük); k = i - d; ilk yarı k <= m / 2, ikinci yarı k > m / 2 (m tek ise "
                   "orta mum ikinci yarıdadır, ör. m = 9: ilk yarı k 1..4, ikinci yarı k 5..9)",
        "p3": "dokunuş sayısı >= 3 VE ilk yarıda >= 1 VE ikinci yarıda >= 1",
        "p4": "d < i <= t için Low_i >= Low(d) - 0,25 x ATR14(d) (eşitlik geçer)",
        "v2": "alt fitil_i = B_i - Low_i; ortalama (i = d+1 .. t) < ortalama (i = max(t-119, d-20) .. d-1) (kesin küçük; dip mumu ikisine de "
              "girmez; dipten önce mum yoksa V2 YANLIŞ); V2 = V1 ∧ bu şart",
        "pivot_tepe": "H_j > max(H_{j-5..j-1}) (sol kesin) ve H_j >= max(H_{j+1..j+5}) (sağ eşit olabilir); j-5 >= t-119 ve j+5 <= d (DS4 ile aynı)",
        "h1_h2": "H1 = en yüksek pivot tepe (eşitte EN ERKEN); H2 = H1'den sonra, H1'den KESİN alçak pivot tepelerin EN SONU; yoksa H1'den sonraki "
                 "en yüksek pivot tepe (eşit -> eğim 0 -> P5 YOK); H1'den sonra pivot tepe yoksa ya da pivot tepe yoksa P5 YOK (DS4 ile aynı)",
        "p5": "düşen çizgi_i = H1 + eğim (i - j1), eğim < 0 şart; d < i <= t kapanışları: Close_i > çizgi_i olan mum sayısı >= 3 VE Close_t > "
              "çizgi_t VE kırılım günü kb = ilk Close_i > çizgi_i (d < i) olmak üzere en az bir P3 dokunuşu j > kb (kesin sonra)",
        "v3": "V3 = P1 ∧ P2 ∧ P3 ∧ P4 (V1'den P5 çıkarılmış; basit tepki dahil) (EK, 23 Kas: DS3 tipi Low çizgisi yerine)",
    },
    "varyant": {"V1": "P1 ∧ P2 ∧ P3 ∧ P4 ∧ P5 (ANA; gövde altı çizgisi + düşen çizgi kırılımı)",
                "V2": "V1 ∧ dip sonrası alt fitil dipten önceki 20 mumdan küçük", "V3": "P1 ∧ P2 ∧ P3 ∧ P4 (V1 ama P5 yok; basit tepki dahil)"},
    "kappa": {"B": 5000, "tohum": 20261126, "guven": 0.95, "bonferroni_k": 3, "gecerli": 0.60, "gecerli_alt": 0.40, "kismen": 0.40,
              "karar_min": 30},
    "hukum": "V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu "
             ">= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (Cemal tarifini DS4 görselini görerek verdi; set 1 / set 2 "
             "sayfaları daha önce DS3 / DS4 çalışmalarında kullanıldı; kesin hüküm yalnız Cemal'in görsel onayı + üçüncü bağımsız kör setle); "
             "kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve "
             "set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33)",
    "onay": {"tohum": 20261126, "VAR": 16, "VAR_pazar": {"ABD": 12, "AVR": 2, "BIST": 2}, "YOK_P3": 2, "YOK_P2": 2, "YOK_P5": 2, "YOK_rastgele": 2,
             "secim": "24 sayfa. Havuz = goz_uyum.gu_havuz (Y1 ∧ Ş1, likidite) ABD + AVR + BIST (DS4 görsel onayıyla aynı havuz; sha denetlenir); "
                      "iki kör setteki VE DS4 görsel onay setindeki (pazar, sembol) çiftleri hariç; olaylar tohumla (20261126) karıştırılmış "
                      "sırada gezilir, her (pazar, sembol) en çok 1 sayfa. V1 VAR 16: karışık sıradaki İLK V1 VAR olaylar, pazar hedefi ABD 12 / "
                      "AVR 2 / BIST 2 (seçme / ayıklama yok); bir pazarda yetmezse eksik, aynı karışık sırada öteki pazarların sıradaki V1 VAR "
                      "olaylarıyla doldurulur ve yazılır. V1 YOK 8: karışık sırada ilk 2 V1 YOK -> 'rastgele' (nedeni ne olursa); sonra "
                      "P1 ∧ P2 ∧ P4 ∧ P5 ∧ ¬P3 -> 'P3 düştü: tek mum / takip yok' (2); P1 ∧ P3 ∧ P4 ∧ P5 ∧ ¬P2 -> 'P2 düştü: çizgi alçalan' (2); "
                      "P1 ∧ P2 ∧ P3 ∧ P4 ∧ ¬P5 -> 'P5 düştü: basit tepki' (2) (EK, 23 Kas: iş tanımındaki 4 rastgeleden 2'si P5'e verildi). Sayfa "
                      "sırası: önce 16 VAR (karışık sıradaki geliş sırası), sonra 8 YOK (tohumla karıştırılmış); PDF kör değil, onay amaçlı"},
    "not": "parametreler (0,20; d <= t-8; 0,05 ATR / 20 mum; 0,35 ATR; 3 dokunuş + iki yarı; 0,25 ATR; P5: 5/5 pivot tepe, 3 kapanış) iş tanımından ve EK'ten aynen; etiketlere "
           "bakılmadan sabitlendi; GETİRİ YOK",
}


class DS5Hata(RuntimeError):
    """Durdurucu hata: veri / mühür / tanım tutmadı."""


def _sha_esik5() -> str:
    return hashlib.sha256(json.dumps(DS5_ESIK, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _f5(x: Any, d: int = 3) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"{float(x):.{d}f}"
    except (TypeError, ValueError):
        return str(x)


# ================================================================ 1) KURAL (yalnız pencere; t sonrası yok)
def _ds5_cizgi(Y: np.ndarray, d: int, t: int, atr: float, E: Dict[str, Any]) -> Dict[str, Any]:
    """Çapa (d, Y_d); s* = min (Y_i - Y_d) / (i - d); dokunuşlar ve P2 / P3. Y = gövde altı (V1) ya da Low (V3)."""
    k = np.arange(1, t - d + 1); post = d + k; m = t - d
    s = float(np.min((Y[post] - Y[d]) / k))
    cizgi = Y[d] + s * k
    mesafe = Y[post] - cizgi
    dok = post[mesafe < float(E["dokunus_atr"]) * atr]
    kd = dok - d
    ilk = int(np.sum(kd <= m / 2.0)); ikinci = int(np.sum(kd > m / 2.0))
    p2 = bool(s >= -float(E["egim_atr"]) * atr / float(E["egim_bar"]))
    p3 = bool(len(dok) >= int(E["dokunus_min"]) and ilk >= 1 and ikinci >= 1)
    return {"s": s, "s_atr20": float(s * float(E["egim_bar"]) / atr), "son": float(cizgi[-1]), "dokunus": [int(j) for j in dok],
            "dokunus_n": int(len(dok)), "ilk_yari": ilk, "ikinci_yari": ikinci, "mesafe_atr_min_ikinci": float(
                np.min(mesafe[k > m / 2.0]) / atr) if np.any(k > m / 2.0) else float("nan"), "P2": p2, "P3": p3}


def ds5_parca_dizi(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray) -> Dict[str, Any]:
    """Diziler kör sayfa penceresi (son eleman = t, 121 bar). P1-P4 + ara değerler + V1 / V2 / V3. Dizinler 121 barlık pencerede."""
    E = DS5_ESIK
    O, H, L, C = (np.asarray(a, float) for a in (O, H, L, C))
    n = len(C)
    if n != int(E["pencere_bar"]):
        raise DS5Hata(f"pencere {n} bar (beklenen {E['pencere_bar']})")
    if not (np.all(np.isfinite(np.c_[O, H, L, C])) and np.all(H > L) and np.all(L > 0)):
        raise DS5Hata("geçersiz bar (NaN / H <= L / L <= 0) pencerede")
    t = n - 1; s0 = t - (int(E["kural_bar"]) - 1); Bm = int(E["dip_sonrasi_min"]); A = int(E["atr_n"])
    B = np.minimum(O, C)
    # DİP
    seg = L[s0:t - Bm + 1]; mn = float(seg.min())
    d = s0 + int(np.flatnonzero(seg == mn)[-1]); Ld = float(L[d]); m = t - d
    gmn = float(L[s0:].min()); d_glob = s0 + int(np.flatnonzero(L[s0:] == gmn)[-1])
    # P1
    if d > s0:
        tepe_i = s0 + int(np.argmax(H[s0:d])); tepe = float(H[tepe_i]); dusus = tepe / Ld - 1.0
    else:
        tepe_i, tepe, dusus = -1, float("nan"), float("nan")
    p1 = bool(np.isfinite(dusus) and dusus >= float(E["dusus_min"]))
    # ATR14(d)
    jj = np.arange(max(1, d - A + 1), d + 1)
    tr = np.maximum(H[jj] - L[jj], np.maximum(np.abs(H[jj] - C[jj - 1]), np.abs(L[jj] - C[jj - 1])))
    atr = float(np.mean(tr))
    if not atr > 0:
        raise DS5Hata("ATR14(d) <= 0")
    post = np.arange(d + 1, t + 1)
    # ÇİZGİ (gövde altı) ve P2 / P3
    G = _ds5_cizgi(B, d, t, atr, E)
    # P4
    min_post = float(L[post].min())
    p4 = bool(min_post >= Ld - float(E["delinme_atr"]) * atr)
    # V2: alt fitil
    once = np.arange(max(s0, d - int(E["fitil_once_bar"])), d)
    fit_post = float(np.mean(B[post] - L[post]) / atr)
    fit_once = float(np.mean(B[once] - L[once]) / atr) if len(once) else float("nan")
    fitil_kucuk = bool(len(once) > 0 and fit_post < fit_once)
    # P5: düşen çizgi (DS4 tanımı) ve dizinin kırılımı
    ts, tg = int(E["tepe_sol"]), int(E["tepe_sag"])
    tepeler = [j for j in range(s0 + ts, d - tg + 1) if H[j] > H[j - ts:j].max() and H[j] >= H[j + 1:j + tg + 1].max()]
    j1 = j2 = kb = -1; egim = float("nan"); p5_neden = ""; ust_n = 0; ust: List[int] = []; son_ust = False; dok_sonra = 0
    if not tepeler:
        p5_neden = "d'den önce onaylı pivot tepe yok"
    else:
        hv = np.array([H[j] for j in tepeler]); j1 = tepeler[int(np.flatnonzero(hv == hv.max())[0])]
        sonra = [j for j in tepeler if j > j1]
        alcak = [j for j in sonra if H[j] < H[j1]]
        if alcak:
            j2 = alcak[-1]
        elif sonra:
            hs = np.array([H[j] for j in sonra]); j2 = sonra[int(np.argmax(hs))]
        if j2 < 0:
            p5_neden = "H1'den sonra pivot tepe yok"
        else:
            egim = (float(H[j2]) - float(H[j1])) / float(j2 - j1)
            if not egim < 0:
                p5_neden = "H1-H2 çizgisi düşen değil (eğim >= 0)"
            else:
                dc = float(H[j1]) + egim * (post - j1)
                ust = [int(i) for i in post[C[post] > dc]]; ust_n = len(ust); son_ust = bool(C[t] > dc[-1])
                kb = ust[0] if ust else -1
                dok_sonra = int(sum(1 for j in G["dokunus"] if kb >= 0 and j > kb))
                if ust_n < int(E["kirilim_kapanis_min"]):
                    p5_neden = f"düşen çizginin üstünde {ust_n} kapanış (< 3)"
                elif not son_ust:
                    p5_neden = "son mumun kapanışı düşen çizginin altında"
                elif dok_sonra < 1:
                    p5_neden = "kırılımdan sonra çizgiye dokunuş yok"
    p5 = bool(j2 >= 0 and np.isfinite(egim) and egim < 0 and ust_n >= int(E["kirilim_kapanis_min"]) and son_ust and dok_sonra >= 1)
    v3 = bool(p1 and G["P2"] and G["P3"] and p4)
    v1 = bool(v3 and p5)
    return {"t_idx": int(t), "s0_idx": int(s0), "d_idx": int(d), "m": int(m), "low_d": Ld, "B_d": float(B[d]), "d_glob_idx": int(d_glob),
            "dip_yeni": bool(d_glob > t - Bm), "tepe_idx": int(tepe_i), "tepe": tepe, "dusus": float(dusus), "P1": p1, "atr_d": atr,
            "s": G["s"], "s_atr20": G["s_atr20"], "cizgi_son": G["son"], "dokunus": G["dokunus"], "dokunus_n": G["dokunus_n"],
            "dokunus_ilk": G["ilk_yari"], "dokunus_ikinci": G["ikinci_yari"], "P2": G["P2"], "P3": G["P3"],
            "min_post_low_atr": float((min_post - Ld) / atr), "P4": p4, "fitil_post_atr": fit_post, "fitil_once_atr": fit_once,
            "fitil_kucuk": fitil_kucuk, "pivot_tepeler": [int(j) for j in tepeler], "h1_idx": int(j1),
            "h1": float(H[j1]) if j1 >= 0 else float("nan"), "h2_idx": int(j2), "h2": float(H[j2]) if j2 >= 0 else float("nan"),
            "egim_dusen": float(egim), "kirilim_idx": int(kb), "ust_kapanis": ust, "ust_kapanis_n": int(ust_n), "son_ust": son_ust,
            "dokunus_kirilim_sonra": int(dok_sonra), "P5": p5, "P5_neden": p5_neden,
            "V1": v1, "V2": bool(v1 and fitil_kucuk), "V3": v3}


def ds5_parca(W: pd.DataFrame) -> Dict[str, Any]:
    O, H, L, C = (W[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    r = ds5_parca_dizi(O, H, L, C)
    ix = W.index

    def tar(i: int) -> Optional[str]:
        return ix[i].strftime("%Y-%m-%d") if i >= 0 else None
    r["d_tarih"] = tar(r["d_idx"]); r["dokunus_tarih"] = [tar(j) for j in r["dokunus"]]
    r["h1_tarih"] = tar(r["h1_idx"]); r["h2_tarih"] = tar(r["h2_idx"]); r["kirilim_tarih"] = tar(r["kirilim_idx"])
    return r


def _kural_sha5() -> str:
    """Kural kaynağının (_ds5_cizgi + ds5_parca_dizi + ds5_parca) sha'sı: olc'de kuralın değişmediği ayrıca denetlenir."""
    src = inspect.getsource(_ds5_cizgi) + inspect.getsource(ds5_parca_dizi) + inspect.getsource(ds5_parca)
    return hashlib.sha256(src.encode("utf-8")).hexdigest()


def ds5_dusen(r: Dict[str, Any]) -> List[str]:
    """V1'i düşüren parçalar (P1 / P2 / P3 / P4 / P5)."""
    return [p for p in ("P1", "P2", "P3", "P4", "P5") if not r[p]]


def ds5_neden_metni(r: Dict[str, Any]) -> List[str]:
    out = []
    if not r["P1"]:
        out.append("P1 düşüş yok (%s < %%20)" % ("-" if not np.isfinite(r["dusus"]) else f"%{r['dusus']*100:.0f}"))
    if not r["P2"]:
        out.append(f"P2 çizgi alçalan ({r['s_atr20']:+.2f} ATR / 20 mum)")
    if not r["P3"]:
        out.append(f"P3 takip yok (dokunuş {r['dokunus_n']}: ilk yarı {r['dokunus_ilk']}, ikinci yarı {r['dokunus_ikinci']})")
    if not r["P4"]:
        out.append(f"P4 dip delinmiş (dip sonrası en düşük Low {r['min_post_low_atr']:+.2f} ATR)")
    if not r["P5"]:
        out.append(f"P5 {r['P5_neden']}")
    return out


# ================================================================ 2) SETLER (anahtar dosyalarından YALNIZ sayfa -> pazar, sembol, sinyal günü)
def ds5_setler() -> pd.DataFrame:
    rows = []
    for st, yol in ((1, DS5_YOL["set1_anahtar"]), (2, DS5_YOL["set2_anahtar"])):
        J = json.load(open(yol, encoding="utf-8"))
        for s in J["sayfalar"]:
            rows.append({"set": st, "sayfa": int(s["sayfa"]), "pazar": str(s["pazar"]), "sembol": str(s["sembol"]),
                         "sinyal_gunu": str(s["sinyal_gunu"])[:10]})
        del J
    S = pd.DataFrame(rows).sort_values(["set", "sayfa"]).reset_index(drop=True)
    for st in (1, 2):
        s = S[S.set == st].sayfa.tolist()
        if s != list(range(1, 41)):
            raise DS5Hata(f"set {st} sayfaları 1..40 değil: {s[:5]}..")
    return S


_VERI5: Dict[str, Dict[str, pd.DataFrame]] = {}


def ds5_pencere(pazar: str, sembol: str, t: str) -> pd.DataFrame:
    if pazar not in _VERI5:
        d5log.info("veri yükleniyor: %s", pazar)
        _VERI5[pazar] = GU.gu_veri(pazar)
    tt = pd.Timestamp(t)
    W = TZ.tz_pencere(pazar, sembol, tt, _VERI5[pazar])                 # K2: veri t'de kesik + mekanik denetim (121 bar, son = t)
    if W.index.max() > tt or W.index[-1] != tt or len(W) != int(DS5_ESIK["pencere_bar"]):
        raise DS5Hata(f"{sembol} {t}: pencere t sonrasını içeriyor / 121 bar değil")
    return W


def _temiz5(r: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for k, v in r.items():
        if isinstance(v, np.bool_):
            v = bool(v)
        elif isinstance(v, np.integer):
            v = int(v)
        elif isinstance(v, np.floating):
            v = float(v)
        out[k] = v
    return out


def ds5_hesap(S: pd.DataFrame) -> pd.DataFrame:
    out = []
    for r in S.itertuples(index=False):
        W = ds5_pencere(r.pazar, r.sembol, r.sinyal_gunu)
        out.append(ds5_parca(W))
    return pd.concat([S.reset_index(drop=True), pd.DataFrame(out)], axis=1)


def _ozet5(R: pd.DataFrame) -> Dict[str, Any]:
    return {"n": int(len(R)), **{f"{v}_VAR": int(R[v].sum()) for v in ("V1", "V2", "V3")},
            **{f"{p}_DOGRU": int(R[p].sum()) for p in ("P1", "P2", "P3", "P4", "P5", "fitil_kucuk")}}


def ds5_anahtar() -> Dict[str, Any]:
    t0 = time.time()
    S = ds5_setler()
    R = ds5_hesap(S)
    sayfalar = []
    for r in R.to_dict("records"):
        r = _temiz5(r)
        r["yanit"] = {v: ("VAR" if r[v] else "YOK") for v in ("V1", "V2", "V3")}
        r["V1_dusen"] = ds5_dusen(r)
        sayfalar.append(r)
    ozet = {str(st): _ozet5(R if st == "birlesik" else R[R.set == st]) for st in (1, 2, "birlesik")}
    J = {"surum": "ds5 v1", "uretim_utc": GU._simdi(),
         "uyari": "GETİRİ YOK; Cemal'in işaretleri bu dosya yazılırken AÇILMADI (etiketler yalnız mühürden sonra olc ile açılır); "
                  "dizinler 121 barlık pencerede (t = 120)",
         "esik": DS5_ESIK, "esik_sha": _sha_esik5(), "kural_sha": _kural_sha5(),
         "girdi_sha": {"goz_uyum_anahtar.json": GU._sha(DS5_YOL["set1_anahtar"]), "tanim2_anahtar.json": GU._sha(DS5_YOL["set2_anahtar"])},
         "ozet": ozet, "sayfalar": sayfalar, "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(DS5_YOL["anahtar"], J)
    d5log.info("anahtar: %s", json.dumps(ozet, ensure_ascii=False))
    return J


# ================================================================ 3) GÖRSEL ONAY (iki set + DS4 onay seti dışından 24 yeni sayfa)
def _havuz_sha5(P: pd.DataFrame) -> str:
    return hashlib.sha256(P.assign(tarih=P.tarih.dt.strftime("%Y-%m-%d")).to_csv(index=False).encode("utf-8")).hexdigest()


def ds5_havuz(onbellek: Optional[str] = None) -> pd.DataFrame:
    """goz_uyum.gu_havuz (Y1 ∧ Ş1, likidite) üç pazar; yalnız (pazar, sembol, tarih). onbellek verilirse ve varsa oradan okunur; okunan havuzun
    sha'sı DS4 görsel onay anahtarındaki havuz sha'sına eşit olmalı (aynı havuz)."""
    if onbellek and os.path.exists(onbellek):
        P = pd.read_pickle(onbellek)
        d5log.info("havuz önbellekten: %s (%d olay)", onbellek, len(P))
    else:
        P = pd.concat([GU.gu_havuz(p, 4)[["pazar", "sembol", "tarih"]] for p in ("BIST", "AVR", "ABD")]).reset_index(drop=True)
        if onbellek:
            P.to_pickle(onbellek)
    P = P[["pazar", "sembol", "tarih"]].copy(); P["tarih"] = pd.to_datetime(P["tarih"])
    P = P.sort_values(["pazar", "sembol", "tarih"], kind="mergesort").reset_index(drop=True)
    J4 = json.load(open(DS5_YOL["ds4_onay_anahtar"], encoding="utf-8"))
    if _havuz_sha5(P) != J4["havuz_sha"]:
        raise DS5Hata("olay havuzu DS4 görsel onay havuzuyla aynı değil (sha) -> DURDU")
    return P


def ds5_onay_sec(P: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    Eo = DS5_ESIK["onay"]; rng = np.random.default_rng(int(Eo["tohum"]))
    S = ds5_setler(); haric = {(a, b) for a, b in zip(S.pazar, S.sembol)}
    J4 = json.load(open(DS5_YOL["ds4_onay_anahtar"], encoding="utf-8"))
    haric4 = {(str(s["pazar"]), str(s["sembol"])) for s in J4["sayfalar"]}; del J4
    Q = P[[(a, b) not in haric and (a, b) not in haric4 for a, b in zip(P.pazar, P.sembol)]].reset_index(drop=True)
    kota = {"VAR": int(Eo["VAR"]), "YOK_rastgele": int(Eo["YOK_rastgele"]), "YOK_P3": int(Eo["YOK_P3"]), "YOK_P2": int(Eo["YOK_P2"]),
            "YOK_P5": int(Eo["YOK_P5"])}
    vpk = {p: int(x) for p, x in Eo["VAR_pazar"].items()}
    if sum(vpk.values()) != kota["VAR"]:
        raise DS5Hata("VAR pazar hedefleri toplamı VAR kotasına eşit değil")
    sira = rng.permutation(len(Q))
    K: List[Dict[str, Any]] = []
    for j in sira:                                                         # tam havuzda kural (seçimden bağımsız; kayıt için sayılır)
        q = Q.iloc[int(j)]
        W = ds5_pencere(q.pazar, q.sembol, q.tarih.strftime("%Y-%m-%d"))
        K.append({"pazar": q.pazar, "sembol": q.sembol, "sinyal_gunu": q.tarih.strftime("%Y-%m-%d"), **_temiz5(ds5_parca(W))})
    al: Dict[str, List[Dict[str, Any]]] = {k: [] for k in kota}; kullanilan: set = set(); notlar: List[str] = []
    var_say = {p: 0 for p in vpk}
    for r in K:
        key = (r["pazar"], r["sembol"])
        if key in kullanilan:
            continue
        grup = None
        if r["V1"]:
            if var_say.get(r["pazar"], 0) < vpk.get(r["pazar"], 0):
                grup = "VAR"; var_say[r["pazar"]] += 1
        elif len(al["YOK_rastgele"]) < kota["YOK_rastgele"]:
            grup = "YOK_rastgele"
        elif r["P1"] and r["P2"] and r["P4"] and r["P5"] and not r["P3"] and len(al["YOK_P3"]) < kota["YOK_P3"]:
            grup = "YOK_P3"
        elif r["P1"] and r["P3"] and r["P4"] and r["P5"] and not r["P2"] and len(al["YOK_P2"]) < kota["YOK_P2"]:
            grup = "YOK_P2"
        elif r["P1"] and r["P2"] and r["P3"] and r["P4"] and not r["P5"] and len(al["YOK_P5"]) < kota["YOK_P5"]:
            grup = "YOK_P5"
        if grup:
            kullanilan.add(key); al[grup].append({**r, "grup": grup})
    for p in vpk:
        if var_say[p] < vpk[p]:
            notlar.append(f"V1 VAR {p}: hedef {vpk[p]}, havuzda bulunan {var_say[p]}")
    if len(al["VAR"]) < kota["VAR"]:
        for r in K:
            if len(al["VAR"]) >= kota["VAR"]:
                break
            key = (r["pazar"], r["sembol"])
            if r["V1"] and key not in kullanilan:
                kullanilan.add(key); al["VAR"].append({**r, "grup": "VAR"})
                notlar.append(f"V1 VAR eksiği {r['pazar']} ile dolduruldu")
    eksik = {k: kota[k] - len(al[k]) for k in kota if len(al[k]) < kota[k]}
    if eksik:
        raise DS5Hata(f"görsel onay kotası dolmadı: {eksik}")
    Y = pd.DataFrame([x for k in ("YOK_P3", "YOK_P2", "YOK_P5", "YOK_rastgele") for x in al[k]])
    Y = Y.iloc[rng.permutation(len(Y))]
    T = pd.concat([pd.DataFrame(al["VAR"]), Y]).reset_index(drop=True)
    T.insert(0, "sayfa", np.arange(1, len(T) + 1))
    KD = pd.DataFrame(K)
    bilgi = {"havuz_n": int(len(P)), "haric_n": int(len(Q)),
             "havuz_pazar": {p: int((P.pazar == p).sum()) for p in ("ABD", "AVR", "BIST")},
             "haric_pazar": {p: int((Q.pazar == p).sum()) for p in ("ABD", "AVR", "BIST")},
             "haric_V1_VAR": {p: int(KD[KD.pazar == p].V1.sum()) for p in ("ABD", "AVR", "BIST")},
             "haric_parca": {k: int(KD[k].sum()) for k in ("P1", "P2", "P3", "P4", "P5", "fitil_kucuk", "V1", "V2", "V3")},
             "VAR_pazar_sayfa": {p: int(sum(1 for x in al["VAR"] if x["pazar"] == p)) for p in ("ABD", "AVR", "BIST")}, "notlar": notlar}
    return T, bilgi


def _isr5(x: bool) -> str:
    return "✓" if x else "✗"


def ds5_sayfa_ciz(W: pd.DataFrame, r: Dict[str, Any], no: int, toplam: int):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure(figsize=(7.5, 10.5))
    ax = fig.add_axes([0.04, 0.27, 0.92, 0.58])
    O, H, L, C = (W[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    t = int(r["t_idx"]); s0 = int(r["s0_idx"]); d = int(r["d_idx"])
    idx = np.arange(s0, t + 1); x = idx - t                                     # 120 mum: -119 .. 0
    Hs, Ls = H[idx], L[idx]; aralik = float(Hs.max() - Ls.min()); pad = aralik * 0.05
    xd = d - t
    ax.axvspan(xd + 0.5, 0.5, color="#fff4cc", alpha=0.8, zorder=0, linewidth=0)          # dipten sonraki bölge
    renk = np.where(C[idx] >= O[idx], "#1a9850", "#d73027")
    ax.vlines(x, Ls, Hs, colors=renk, linewidth=1.1, zorder=3)
    for xi, o, c, col in zip(x, O[idx], C[idx], renk):
        ax.add_patch(Rectangle((xi - 0.35, min(o, c)), 0.7, max(abs(c - o), aralik * 0.0008), facecolor=col, edgecolor=col, linewidth=0.4,
                               zorder=4))
    # gövde altı çizgisi: çapa (d, B_d), eğim s*, t'ye kadar
    xs = np.array([d, t]); ys = r["B_d"] + r["s"] * (xs - d)
    ax.plot(xs - t, ys, color="#1f4e9c", linewidth=3.0, zorder=6, solid_capstyle="round")
    ax.annotate("DİP", xy=(xd, L[d]), xytext=(xd, L[d] - pad * 1.8), ha="center", va="top", fontsize=10, color="#1f4e9c", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#1f4e9c", lw=1.5), zorder=8)
    if r["h1_idx"] >= 0 and r["h2_idx"] >= 0 and np.isfinite(r["egim_dusen"]):
        j1, j2 = int(r["h1_idx"]), int(r["h2_idx"])
        xs2 = np.array([j1, t]); ys2 = r["h1"] + r["egim_dusen"] * (xs2 - j1)
        ax.plot(xs2 - t, ys2, color="#e31a1c" if r["egim_dusen"] < 0 else "#fb9a99", linewidth=1.8, zorder=7)
        ax.plot([j1 - t, j2 - t], [r["h1"], r["h2"]], linestyle="none", marker="o", markersize=6, markerfacecolor="none",
                markeredgecolor="#e31a1c", markeredgewidth=1.5, zorder=8)
        ax.text(j1 - t, r["h1"] + pad * 0.3, "H1", ha="center", va="bottom", fontsize=8, color="#e31a1c")
        ax.text(j2 - t, r["h2"] + pad * 0.3, "H2", ha="center", va="bottom", fontsize=8, color="#e31a1c")
    for j in r["ust_kapanis"]:                                                    # düşen çizginin üstünde kapanan dip sonrası mumlar
        ax.plot([j - t - 0.45, j - t + 0.45], [C[j], C[j]], color="#ff7f00", linewidth=2.2, zorder=9, solid_capstyle="butt")
    B = np.minimum(O, C)
    for j in r["dokunus"]:
        ax.plot([j - t], [B[j] - pad * 0.35], marker="o", markersize=6, markerfacecolor="none", markeredgecolor="#6a3d9a",
                markeredgewidth=1.6, linestyle="none", zorder=9)
    ax.axvline(0.5, color="#555555", linewidth=0.8, zorder=2); ax.axvline(-0.5, color="#555555", linewidth=0.8, zorder=2)
    ust_y = max(Hs.max(), r["h1"] if np.isfinite(r["h1"]) else Hs.max())
    ax.set_ylim(Ls.min() - pad * 2.4, ust_y + pad * 1.4); ax.set_xlim(x[0] - 1, 2)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.6); sp.set_color("#888888")
    fig.text(0.04, 0.945, f"{int(no)}", fontsize=44, fontweight="bold", va="center", ha="left")
    fig.text(0.96, 0.945, f"/ {toplam}", fontsize=16, va="center", ha="right", color="#666666")
    fig.text(0.50, 0.885, "kalın mavi = dipten başlayan gövde altı çizgisi · mor daire = çizgiye değen mum · sarı zemin = dipten sonrası",
             fontsize=7.4, ha="center", color="#555555")
    fig.text(0.50, 0.868, "kırmızı = düşen çizgi (H1-H2) · turuncu çizgi = düşen çizginin üstünde kapanış · sağdaki iki ince çizgi arası = son gün",
             fontsize=7.4, ha="center", color="#555555")
    s1 = f"Düşüşten dip {_isr5(r['P1'])}   —   Çizgi yatay/yukarı {_isr5(r['P2'])}"
    s2 = f"Mumlar çizgiyi takip ediyor (dokunuş {int(r['dokunus_n'])}) {_isr5(r['P3'])}   —   Dip korunuyor {_isr5(r['P4'])}"
    s3 = f"Dizi düşen çizgiyi kırdı {_isr5(r['P5'])}"
    fig.text(0.50, 0.235, s1, fontsize=12, ha="center", va="center")
    fig.text(0.50, 0.205, s2, fontsize=12, ha="center", va="center")
    fig.text(0.50, 0.175, s3, fontsize=12, ha="center", va="center")
    fig.text(0.50, 0.128, f"SONUÇ: {'VAR' if r['V1'] else 'YOK'}", fontsize=20, fontweight="bold", ha="center", va="center")
    fig.text(0.50, 0.065, "☐ DOĞRU ÇİZGİ        ☐ YANLIŞ (doğrusunu çiz)", fontsize=14, ha="center", va="center")
    return fig


def ds5_onay(onbellek: Optional[str] = None) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    t0 = time.time()
    P = ds5_havuz(onbellek)
    hsha = _havuz_sha5(P)
    T, bilgi = ds5_onay_sec(P)
    yol = DS5_YOL["pdf"]
    with PdfPages(yol, metadata={"Title": "DIP SAVUNMASI v5 - gorsel onay", "Author": "ds5", "Creator": "ds5", "Producer": "ds5",
                                 "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(7.5, 10.5))
        fig.text(0.5, 0.88, "DİP SAVUNMASI — kodun gözü (v5)", fontsize=22, fontweight="bold", ha="center")
        kapak = ("Senin tarifin: en dipten başlayıp yatay ya da\n"
                 "yukarı bir çizgiyi takip eden mumlar (gövde altları).\n\n"
                 "Kod çizgiyi mavi çizdi,\n"
                 "değdiği mumları daire ile gösterdi.\n\n"
                 "Mavi çizgiyi takip eden mumlar kırmızı düşen\n"
                 "çizgiyi de kırmış olmalı; düşüş içindeki basit\n"
                 "tepki sayılmaz.\n\n"
                 "İlk 16 sayfa kodun VAR dediği rastgele örnekler.\n"
                 "Çizgi senin çizeceğin gibi mi?")
        fig.text(0.5, 0.82, kapak, fontsize=14, ha="center", va="top", linespacing=1.4)
        aciklama = ("Çizimler:\n"
                    "  DİP oku = penceredeki en derin nokta (en düşük fitil)\n"
                    "  kalın mavi çizgi = dip mumunun gövde altından başlayıp sonraki bütün\n"
                    "      gövde altlarının altında kalan en dik çizgi (sağa son güne kadar)\n"
                    "  mor daire = gövde altı çizgiye çok yakın mum (dokunuş; ortalama mum\n"
                    "      boyunun üçte birinden yakın)\n"
                    "  sarı zemin = dipten sonraki bölge\n"
                    "  kırmızı çizgi = dibe inerken iki tepeden (H1, H2) çizilen düşen çizgi\n"
                    "  turuncu kısa çizgi = dipten sonra düşen çizginin üstünde kapanış\n\n"
                    "Takip: en az 3 dokunuş, dipten sonraki sürenin hem ilk hem ikinci yarısında.\n"
                    "Kırılım: en az 3 kapanış ve son gün düşen çizginin üstünde; kırılımdan\n"
                    "      sonra da mavi çizgiye en az bir dokunuş.\n"
                    "Sayfanın altında kodun cevabı: beş parça ✓ / ✗ ve SONUÇ.\n"
                    f"{len(T)} sayfa: önce {int((T.V1.astype(bool)).sum())} VAR, sonra {int((~T.V1.astype(bool)).sum())} YOK "
                    "(bu PDF kör değil, onay için).\n"
                    "Daha önce görmediğin yeni grafikler. Hisse adı yok; son günden sonrası gösterilmez.\n"
                    "Kutulardan birini işaretlemen yeter.")
        fig.text(0.06, 0.47, aciklama, fontsize=9.5, ha="left", va="top", linespacing=1.35)
        pdf.savefig(fig); plt.close(fig)
        for rr in T.to_dict("records"):
            W = ds5_pencere(rr["pazar"], rr["sembol"], rr["sinyal_gunu"])
            r = ds5_parca(W)
            if r["V1"] != bool(rr["V1"]):
                raise DS5Hata("onay: V1 yeniden hesapta seçimden farklı")
            fig = ds5_sayfa_ciz(W, r, int(rr["sayfa"]), len(T))
            pdf.savefig(fig); plt.close(fig)
    boy = os.path.getsize(yol)
    if boy >= 6 * 1024 * 1024:
        raise DS5Hata(f"PDF 6 MB'tan büyük: {boy}")
    sayfalar = []
    for rr in T.to_dict("records"):
        rr = _temiz5(rr); rr["V1_dusen"] = ds5_dusen(rr); rr["neden"] = ds5_neden_metni(rr)
        rr["yanit"] = {v: ("VAR" if rr[v] else "YOK") for v in ("V1", "V2", "V3")}
        sayfalar.append(rr)
    J = {"surum": "ds5 onay v1", "uretim_utc": GU._simdi(),
         "uyari": "GİZLİ ANAHTAR (hisse adları): Cemal DS5_ONAY.pdf'i işaretlemeden önce gösterilmez. GETİRİ YOK.",
         "esik_sha": _sha_esik5(), "kural_sha": _kural_sha5(), "havuz_sha": hsha, "havuz": bilgi,
         "pdf_sha": GU._sha(yol), "pdf_bayt": boy, "sayfalar": sayfalar, "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(DS5_YOL["onay_anahtar"], J)
    d5log.info("onay PDF %s (%.2f MB): %s", yol, boy / 1e6, [(s["sayfa"], s["grup"], s["yanit"]["V1"]) for s in sayfalar])
    return J


# ================================================================ 4) TEST (sentetik seriler; gerçek veriden ÖNCE)
def ds5_cakisma_kontrol() -> None:
    ez = [k for k, v in _CK_ONCE_DS5.items() if k in globals() and id(globals()[k]) != v and not k.startswith("_")]
    if ez:
        raise DS5Hata(f"çakışma kapısı: bellekteki mevcut ad(lar) ezildi: {ez[:5]}")


def _atr5(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, d: int) -> float:
    jj = np.arange(max(1, d - 13), d + 1)
    return float(np.mean(np.maximum(H[jj] - L[jj], np.maximum(np.abs(H[jj] - C[jj - 1]), np.abs(L[jj] - C[jj - 1])))))


def _insa(m: int, dip: Tuple[float, float, float, float], post: List[Tuple[float, float, float, float]],
          duz: bool = False, cokus: float = 0.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """121 bar sentetik seri; d = 120 - m. Dipten önce: 148'den dibe doğru zikzak düşüş (dört tepe: düşen çizgi H1-H2 kurulabilsin; duz=True
    ise 112'den 100'e %11'lik hafif eğimli dalgalı seri, düşüş < %20; cokus > 0 ise
    dipten önceki son 6 mumda ek 'cokus' puanlık sert düşüş: düşen çizgi dibin çok üstünde kalır).
    dip = (gövde boyu, yön (+1 yeşil / -1 kırmızı), üst fitil, alt fitil) ATR0 biriminde.
    post = her dip sonrası mum için (gövde altı - B_d, gövde boyu, üst fitil, alt fitil) ATR biriminde (ATR = ATR14(d), dip mumu dahil);
    gövde boyu > 0 yeşil (O = alt, C = üst), < 0 kırmızı (O = üst, C = alt)."""
    t = 120; d = t - m
    if not (8 <= m <= 100) or len(post) != m:
        raise DS5Hata("sentetik: m / post uzunluğu")
    k = np.arange(d)
    if duz:
        p = 112.0 - 12.0 * k / max(d - 1, 1) + 1.5 * np.sin(k / 3.0)
    else:
        fr = [0.0, 0.10, 0.25, 0.33, 0.50, 0.58, 0.75, 0.83, 1.0]; ys = [148.0, 152.0, 135.0, 140.0, 122.0, 127.0, 110.0, 114.0, 102.0]
        p = np.interp(k, np.array(fr) * max(d - 1, 1), ys)
    if cokus > 0:
        p = p - cokus * np.clip((k - (d - 7)) / 6.0, 0.0, 1.0)
    O = np.r_[p[0], p[:-1]].astype(float); C = p.astype(float)
    H = np.maximum(O, C) + 0.3; L = np.minimum(O, C) - 0.3
    a0 = _atr5(np.r_[O, O[-1]], np.r_[H, H[-1]], np.r_[L, L[-1]], np.r_[C, C[-1]], d - 1) if d >= 2 else 1.0
    gb_, yon_, u_, a_ = dip
    base = float(L[:d].min()) - 1.0
    Bd = base + a_ * a0
    Od, Cd = (Bd, Bd + gb_ * a0) if yon_ >= 0 else (Bd + gb_ * a0, Bd)
    Hd = max(Od, Cd) + u_ * a0; Ld = Bd - a_ * a0
    O = np.r_[O, Od]; C = np.r_[C, Cd]; H = np.r_[H, Hd]; L = np.r_[L, Ld]
    atr = _atr5(O, H, L, C, d)
    for (off, gb, uf, af) in post:
        b = Bd + off * atr; g = abs(gb) * atr
        o, c = (b, b + g) if gb >= 0 else (b + g, b)
        O = np.r_[O, o]; C = np.r_[C, c]; H = np.r_[H, max(o, c) + uf * atr]; L = np.r_[L, b - af * atr]
    if len(C) != 121:
        raise DS5Hata("sentetik uzunluk")
    return O, H, L, C


def ds5_sentetik() -> Dict[str, Dict[str, Any]]:
    """Sentetik seriler ve beklenen yanıtlar (iş tanımı S1-S7, EK S8-S9, ek S10-S12). dusen = V1'i düşürmesi beklenen parçalar (TAM küme);
    beklenen = V1 (ve gerekiyorsa V2 / V3)."""
    S: Dict[str, Dict[str, Any]] = {}
    dip = (0.6, -1, 0.2, 0.3)                                                # kırmızı dip mumu, kısa alt fitil
    # S1: 15 mumluk tırmanış, gövde altları 0,25 ATR / mum yükselen çizgiye k = 3, 6, 10, 14'te değiyor; arada 0,8-1,2 ATR yukarıda
    s1 = []
    for k in range(1, 16):
        off = 0.25 * k + (0.05 if k in (3, 6, 10, 14) else 0.8 + 0.4 * ((k * 7) % 3) / 2)
        s1.append((off, 0.6 if k % 2 else -0.5, 0.15, 0.08))
    S["S1"] = {"tarif": "düşüş -> dip -> gövde altları yükselen çizgiye 4 kez değen 15 mumluk tırmanış; düşen çizgiyi kırıyor",
               "seri": _insa(15, dip, s1), "beklenen": {"V1": True, "V2": True, "V3": True}, "dusen": []}
    # S2: 12 mumluk yatay gövde tabanı; k = 2, 5, 8, 11 dokunuş; yavaş düşen çizgi kırılıyor
    s2 = [((0.03 if k in (2, 5, 8, 11) else 0.8 + 0.3 * (k % 3)), 0.5 if k % 2 else -0.6, 0.2, 0.08) for k in range(1, 13)]
    S["S2"] = {"tarif": "düşüş -> dip -> yatay gövde tabanı, 4 dokunuş (12 mum); düşen çizgiyi kırıyor", "seri": _insa(12, dip, s2),
               "beklenen": {"V1": True, "V3": True}, "dusen": []}
    # S3: tek büyük yeşil mumla sıçrama (k = 1, gövde altı dibe yakın), sonra 4,5-5,5 ATR yukarıda dokunuşsuz gezinme
    s3 = [(0.05, 5.0, 0.2, 0.05)] + [(4.5 + 0.5 * ((k * 5) % 3), 0.5 if k % 2 else -0.5, 0.2, 0.1) for k in range(2, 13)]
    S["S3"] = {"tarif": "dipten sonra TEK büyük mumla sıçrama, sonra dokunuşsuz yukarıda gezinme (tek dokunuş kırılım mumunun kendisi -> "
                        "P5 de düşer: kırılımdan sonra dokunuş yok)", "seri": _insa(12, dip, s3),
               "beklenen": {"V1": False}, "dusen": ["P3", "P5"]}
    # S4: çekiç dip (uzun alt fitil 2 ATR), sonra gövde altları 0,12 ATR / mum alçalıyor (dibi delmeden)
    s4 = [(-0.12 * k, 0.4 if k % 2 else -0.4, 0.15, 0.1) for k in range(1, 13)]
    S["S4"] = {"tarif": "dipten sonra gövde altları alçalıyor (0,12 ATR / mum; dip delinmiyor)", "seri": _insa(12, (0.3, 1, 0.2, 2.0), s4),
               "beklenen": {"V1": False}, "dusen": ["P2"]}
    # S5: S2 gibi; son 7 mumda iki mumun fitili dibi 0,55 ATR deliyor (gövdeler aynı)
    s5 = [list(x) for x in s2]
    for k in (7, 10):                                                     # k = 7 -> t-5, k = 10 -> t-2
        s5[k - 1][3] = s5[k - 1][0] + 0.3 + 0.55                         # alt fitil = (gövde altı - B_d) + dip alt fitili + 0,55 (ATR0 ~ ATR)
    S["S5"] = {"tarif": "S2 gibi ama dip sonrası (t-5, t-2) iki mumun fitili dibi ~0,55 ATR deliyor", "seri": _insa(12, dip, [tuple(x) for x in s5]),
               "beklenen": {"V1": False}, "dusen": ["P4"]}
    # S6: düşüş yok: 100 çevresinde yatay dalgalı, dip sonrası S2 gibi
    s6 = [(0.5 * k + (0.05 if k in (3, 6, 10, 14) else 0.9), 0.6 if k % 2 else -0.5, 0.15, 0.08) for k in range(1, 16)]
    S["S6"] = {"tarif": "düşüş yok (112 -> 100 hafif eğimli dalgalı seri, < %20), dip sonrası 0,5 ATR / mum tırmanış, 4 dokunuş",
               "seri": _insa(15, dip, s6, duz=True),
               "beklenen": {"V1": False}, "dusen": ["P1"]}
    # S7: dokunuşlar yalnız dipten hemen sonraki 3 mumda; sonra çizgiden 1 ATR / mum uzaklaşıyor
    s7 = [(0.05, 0.4, 0.1, 0.05), (0.04, -0.4, 0.1, 0.05), (0.06, 0.4, 0.1, 0.05)] + \
         [(0.5 + 1.0 * (k - 3), 0.6, 0.2, 0.1) for k in range(4, 16)]
    S["S7"] = {"tarif": "dokunuşlar yalnız dipten hemen sonraki 3 mumda, sonra çizgiden uzaklaşma (15 mum; dokunuşlar kırılımdan önce -> "
                        "P5 de düşer)", "seri": _insa(15, dip, s7),
               "beklenen": {"V1": False}, "dusen": ["P3", "P5"]}
    # S8 (EK): basit tepki: dipten önce sert çöküş (düşen çizgi dibin çok üstünde); gövde altları yükselen çizgiye 4 dokunuş, kapanışlar çizgi altında
    s8 = [(0.12 * k + (0.04 if k in (2, 5, 8, 11) else 0.6), 0.4 if k % 2 else -0.4, 0.15, 0.08) for k in range(1, 13)]
    S["S8"] = {"tarif": "basit tepki: sert çöküş sonrası dip; gövde altları yükselen çizgiye 4 dokunuş ama bütün kapanışlar düşen çizginin altında",
               "seri": _insa(12, dip, s8, cokus=25.0), "beklenen": {"V1": False, "V3": True}, "dusen": ["P5"]}
    # S9 (EK): tek mum düşen çizgiyi kırıyor (k = 6 büyük yeşil mum), sonraki mumlar yatay tabana (çizgi altına) dönüyor
    s9 = [((0.03 if k in (2, 5, 8, 11) else 0.7 + 0.2 * (k % 3)), 0.5 if k % 2 else -0.5, 0.15, 0.08) for k in range(1, 13)]
    s9[5] = (0.03, 14.0, 0.3, 0.05)
    S["S9"] = {"tarif": "tek mum düşen çizgiyi kırıyor (t-6), sonraki mumlar yatay tabana, çizginin altına dönüyor",
               "seri": _insa(12, dip, s9, cokus=25.0), "beklenen": {"V1": False, "V3": True}, "dusen": ["P5"]}
    # S10 (ek): dip çok yeni: S2 gibi ama t-3'te dibi 2 ATR delen mum (d t-8'den sonraya gidemez)
    s10 = [list(x) for x in s2]; s10[8][3] = s10[8][0] + 0.3 + 2.0
    S["S10"] = {"tarif": "en düşük Low t-3'te (dibi ~2 ATR deliyor; d t-8'den sonraya gidemez)", "seri": _insa(12, dip, [tuple(x) for x in s10]),
                "beklenen": {"V1": False}, "dusen": ["P4"]}
    # S11 (ek): V2 ayrımı: S2 gibi ama dip sonrası mumların alt fitilleri uzun (1,2 ATR'ye kadar; dibi delmeden)
    s11 = [(o, g, u, min(1.2, o + 0.25)) for (o, g, u, _a) in s2]
    S["S11"] = {"tarif": "S2 gibi (V1 VAR) ama dip sonrası alt fitiller uzun (V2 YOK)", "seri": _insa(12, dip, s11),
                "beklenen": {"V1": True, "V2": False}, "dusen": []}
    # S12 (ek): gövde altları hep 1+ ATR yukarıda, son mum çizgiyi belirliyor (ilk yarıda dokunuş yok)
    s12 = [(1.2 + 0.3 * k, 0.5, 0.2, 0.1) for k in range(1, 12)] + [(0.3 * 12, 0.5, 0.2, 0.1)]
    S["S12"] = {"tarif": "gövde altları hep yukarıda, çizgiye yalnız son mumlar değiyor (ilk yarıda dokunuş yok)", "seri": _insa(12, dip, s12),
                "beklenen": {"V1": False}, "dusen": ["P3"]}
    return S


def ds5_test() -> Dict[str, Any]:
    ds5_cakisma_kontrol()
    tablo = []
    for ad, s in ds5_sentetik().items():
        r = ds5_parca_dizi(*s["seri"])
        cik = {v: bool(r[v]) for v in ("V1", "V2", "V3")}
        esit = all(cik[v] == x for v, x in s["beklenen"].items()) and ds5_dusen(r) == s["dusen"]
        tablo.append({"seri": ad, "tarif": s["tarif"], "beklenen_V1": "VAR" if s["beklenen"]["V1"] else "YOK",
                      "beklenen_dusen": s["dusen"], "beklenen_ek": {v: ("VAR" if x else "YOK") for v, x in s["beklenen"].items() if v != "V1"},
                      "cikan": {v: ("VAR" if x else "YOK") for v, x in cik.items()}, "dusen": ds5_dusen(r),
                      "P1": r["P1"], "P2": r["P2"], "P3": r["P3"], "P4": r["P4"], "P5": r["P5"], "d": r["d_idx"] - r["t_idx"], "m": r["m"],
                      "s_atr20": round(r["s_atr20"], 3), "dokunus": [j - r["t_idx"] for j in r["dokunus"]], "dokunus_n": r["dokunus_n"],
                      "ilk": r["dokunus_ilk"], "ikinci": r["dokunus_ikinci"], "min_post_low_atr": round(r["min_post_low_atr"], 3),
                      "fitil_post": round(r["fitil_post_atr"], 3), "fitil_once": round(r["fitil_once_atr"], 3),
                      "h1": r["h1_idx"] - r["t_idx"] if r["h1_idx"] >= 0 else None, "h2": r["h2_idx"] - r["t_idx"] if r["h2_idx"] >= 0 else None,
                      "kirilim": r["kirilim_idx"] - r["t_idx"] if r["kirilim_idx"] >= 0 else None, "ust_n": r["ust_kapanis_n"],
                      "son_ust": r["son_ust"], "dok_sonra": r["dokunus_kirilim_sonra"], "P5_neden": r["P5_neden"], "esit": esit})
    bozuk = [x["seri"] for x in tablo if not x["esit"]]
    if bozuk:
        raise AssertionError(f"sentetik seriler beklenenden farklı: {bozuk}: " + json.dumps([x for x in tablo if not x["esit"]], ensure_ascii=False))
    T = {x["seri"]: x for x in tablo}
    assert T["S1"]["d"] == -15 and T["S1"]["dokunus_n"] >= 4 and T["S1"]["s_atr20"] > 1 and T["S1"]["kirilim"] is not None, T["S1"]
    assert T["S2"]["dokunus_n"] == 4 and abs(T["S2"]["s_atr20"]) < 0.2 and T["S2"]["kirilim"] is not None, T["S2"]
    assert T["S3"]["dokunus_n"] == 1 and T["S3"]["P2"], T["S3"]
    assert T["S4"]["P3"] and T["S4"]["P4"] and T["S4"]["s_atr20"] < -2, T["S4"]
    assert T["S5"]["d"] == -12 and T["S5"]["min_post_low_atr"] < -0.25, T["S5"]
    assert T["S7"]["dokunus_n"] == 3 and T["S7"]["ikinci"] == 0, T["S7"]
    assert T["S8"]["ust_n"] == 0 and T["S8"]["dokunus_n"] == 4 and T["S8"]["s_atr20"] > 0, T["S8"]
    assert T["S9"]["ust_n"] == 1 and not T["S9"]["son_ust"] and T["S9"]["kirilim"] == -6, T["S9"]
    assert T["S10"]["d"] == -12, T["S10"]
    assert T["S12"]["ilk"] == 0 and T["S12"]["ikinci"] >= 1, T["S12"]
    # eşit en düşük Low: EN SON gün
    O, H, L, C = (a.copy() for a in ds5_sentetik()["S2"]["seri"]); L[100] = L[108]
    r = ds5_parca_dizi(O, H, L, C)
    assert r["d_idx"] == 108 and L[100] == L[108] == L[1:113].min(), r["d_idx"]
    # prefix değişmezliği: t sonrası veri değişince sonuç aynı (dizi ve DataFrame)
    rng = np.random.default_rng(11); n = 260
    Cx = 100 + np.cumsum(rng.normal(0, 1, n)); Ox = Cx + rng.normal(0, .3, n)
    Hx = np.maximum(Ox, Cx) + abs(rng.normal(0, .5, n)) + .1; Lx = np.minimum(Ox, Cx) - abs(rng.normal(0, .5, n)) - .1
    Cx, Ox, Hx, Lx = (a - min(Lx.min(), 0) + 5 for a in (Cx, Ox, Hx, Lx))
    for i in (150, 200, 230):
        s = slice(i - 120, i + 1)
        x1 = ds5_parca_dizi(Ox[s], Hx[s], Lx[s], Cx[s])
        O2, H2, L2, C2 = Ox.copy(), Hx.copy(), Lx.copy(), Cx.copy()
        O2[i + 1:] = 1; H2[i + 1:] = 2; L2[i + 1:] = 0.5; C2[i + 1:] = 1.5
        x2 = ds5_parca_dizi(O2[s], H2[s], L2[s], C2[s])
        assert json.dumps(x1, sort_keys=True) == json.dumps(x2, sort_keys=True), "DS5 t sonrasına bağlı"
    idx = pd.bdate_range("2020-01-01", periods=n)
    D1 = pd.DataFrame({"Open": Ox, "High": Hx, "Low": Lx, "Close": Cx}, index=idx)
    D2 = D1.copy(); D2.iloc[201:] = [1.0, 2.0, 0.5, 1.5]
    t = idx[200]
    y1 = ds5_parca(D1[D1.index <= t].iloc[-121:]); y2 = ds5_parca(D2[D2.index <= t].iloc[-121:])
    assert json.dumps(y1, sort_keys=True) == json.dumps(y2, sort_keys=True), "prefix (DataFrame) değişmezliği bozuk"
    # tanım değişmezleri: hiçbir dip sonrası gövde altı çizginin altında değil; en az bir mum çizgi üzerinde
    for ad, s in ds5_sentetik().items():
        O, H, L, C = s["seri"]; r = ds5_parca_dizi(O, H, L, C); d = r["d_idx"]; k = np.arange(1, 121 - d)
        mes = np.minimum(O, C)[d + k] - (r["B_d"] + r["s"] * k)
        assert mes.min() > -1e-9 and abs(mes.min()) < 1e-9, (ad, mes.min())
    # pencere boyu ve geçersiz bar denetimi
    for bozuk_ in ((Ox[:100], Hx[:100], Lx[:100], Cx[:100]), (Ox[:121], Lx[:121], Hx[:121], Cx[:121])):
        try:
            ds5_parca_dizi(*bozuk_); raise AssertionError("bozuk pencere kabul edildi")
        except DS5Hata:
            pass
    # hüküm
    assert ds5_hukum(0.7, 0.45, 79) == "YARI BAĞIMSIZ GEÇERLİ" and ds5_hukum(0.7, 0.3, 79) == "KISMEN"
    assert ds5_hukum(0.5, 0.2, 79) == "KISMEN" and ds5_hukum(0.3, 0.1, 79) == "GEÇERSİZ" and ds5_hukum(0.9, 0.8, 20).startswith("ÖLÇÜLEMEDİ")
    a = np.array([1, 1, 0, 0] * 10, bool)
    assert abs(GU.gu_kappa(a, a) - 1) < 1e-12
    return {"tamam": True, "kural_sha": _kural_sha5(), "esik_sha": _sha_esik5(), "tablo": tablo}


# ================================================================ 5) MÜHÜR
DS5_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralın uyumu, kappa)"),
    "K2": ("EVET", "P1-P5 yalnız kör sayfa penceresinden: tanim2.tz_pencere = goz_uyum._gu_pencere (veri t'de KESİK, 121 bar) + ds5_pencere "
                   "mekanik denetimi (W.index.max() <= t, W.index[-1] == t, 121 bar); çizgi ve dokunuşlar yalnız d+1 .. t; pivot tepe j+5 <= d; ds5.py test prefix "
                   "değişmezliği (3 kesik + DataFrame); getiri / sinyal sonrası fiyat okunmaz; Cemal'in işaretleri ve önceki sonuç dosyaları "
                   "mühürden önce açılmadı (olc açılış zamanı DS5_SONUC'ta)"),
    "K3": ("EVET", "GE.ge_hazir (H>L, V>0, O/H/L/C>0) geçerli bar (goz_uyum ile aynı); ds5_parca_dizi NaN / H <= L / L <= 0 görürse durur (testte sınandı)"),
    "K4": ("EVET", "80 sayfa set 1 (goz_uyum_anahtar) + set 2 (tanim2_anahtar) ile aynı: aynı hissede en çok 1 sayfa; görsel onay 24 sayfası iki "
                   "setin VE DS4 görsel onay setinin (pazar, sembol) çiftleri hariç, her çift en çok 1 sayfa"),
    "K5": ("UYGULANMAZ", "giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik"),
    "K6": ("EVET", "tek kip V_*.pkl (goz_uyum ile aynı); düşüş oranı birimsiz, eğim / dokunuş / delinme ATR14(d) biriminde; fiyat birimi kuralı etkilemez"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok"),
    "K8": ("EVET", "79-80 karar (iki set); karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); 3 varyant: Bonferroni 3 (%98,33) V2 / V3 için; "
                   "hüküm yalnız V1 ve 'YARI BAĞIMSIZ' (Cemal tarifi DS4 görselini görerek verdi; iki set önceki DS3 / DS4 işlerinde kullanıldı); "
                   "set 1 ve set 2 ayrı; kural etiketlerden SEÇİLMEDİ (Ç211 ezber dersi); kesin hüküm üçüncü bağımsız kör setle"),
    "K9": ("EVET", "kural + DS5_ESIK + sentetik test ADIM 1'de etiketler açılmadan commit; 80 yanıt ds5_anahtar.json + görsel onay (DS5_ONAY.pdf, "
                   "ds5_onay_anahtar.json) etiket açılmadan mühürlü; ds5.py + ds5_anahtar.json + DS5_ESIK + kural kaynağı + PDF + onay anahtarı "
                   "sha'ları bu dosyada; olc sha'ları denetler ve 80 yanıtı veriden yeniden hesaplayıp mühürle karşılaştırır; hüküm eşikleri sabit"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırma yok; yalnız OHLCV"),
    "K11": ("EVET", "ds5.py anahtar / onay aynı komutla deterministik yeniden üretilir (tohum 20261126; havuz sha DS4 havuzuyla eşit şartı); olc 80 "
                    "sayfanın yanıtını veriden yeniden hesaplar, mühürlü yanıtla eşitliğini şart koşar; sentetik seriler beklenen yanıt ve düşen "
                    "parçayla birebir"),
    "K12": ("EVET", "iddia yok; yalnız 'uyum' ve 'kappa' sayısı; hüküm sözü yalnız ön kayıttaki eşikle ve yalnız V1 için; 'YARI BAĞIMSIZ' sınırı yazılı"),
    "K13": ("EVET", "çakışma kapısı _CK_ONCE_DS5 + test; yasak dosyalar (defter, mevcut .py, anahtar / ön kayıt / sonuç dosyaları) değişmedi "
                    "(git diff boş); e-posta / anahtar yok (_yaz / _jyaz e-posta taraması); git add -A yok; PDF Cemal'e gönderilmedi"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


def _sentetik_tablo5(T: Dict[str, Any]) -> List[str]:
    st = ["| seri | tarif | beklenen V1 (düşen) | çıkan V1 / V2 / V3 | P1 | P2 | P3 | P4 | P5 | d | çizgi eğimi (ATR / 20 mum) | dokunuş (ilk / ikinci yarı) | "
          "dip sonrası en düşük Low (ATR) | H1 / H2 / kırılım | düşen çizgi üstü kapanış (son mum üstte) | eşit |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in T["tablo"]:
        b = x["beklenen_V1"] + (f" ({', '.join(x['beklenen_dusen'])})" if x["beklenen_dusen"] else "") + \
            ("; " + ", ".join(f"{k} {v}" for k, v in x["beklenen_ek"].items()) if x["beklenen_ek"] else "")
        c = " / ".join(x["cikan"][v] for v in ("V1", "V2", "V3"))
        tt = " / ".join(("t%+d" % x[k]) if x[k] is not None else "-" for k in ("h1", "h2", "kirilim"))
        st.append(f"| {x['seri']} | {x['tarif']} | {b} | {c} | {_isr5(x['P1'])} | {_isr5(x['P2'])} | {_isr5(x['P3'])} | {_isr5(x['P4'])} | "
                  f"{_isr5(x['P5'])} | t{x['d']:+d} | {x['s_atr20']:+.2f} | {x['dokunus_n']} ({x['ilk']} / {x['ikinci']}) | "
                  f"{x['min_post_low_atr']:+.2f} | {tt} | {x['ust_n']} ({'evet' if x['son_ust'] else 'hayır'}) | {'EVET' if x['esit'] else 'HAYIR'} |")
    return st


def ds5_muhur() -> str:
    for y in (DS5_YOL["anahtar"], DS5_YOL["is_tanimi"], DS5_YOL["pdf"], DS5_YOL["onay_anahtar"]):
        if not os.path.exists(y):
            raise DS5Hata(f"mühür için dosya yok: {y}")
    J = json.load(open(DS5_YOL["anahtar"], encoding="utf-8")); JO = json.load(open(DS5_YOL["onay_anahtar"], encoding="utf-8"))
    for ad, X in (("anahtar", J), ("onay", JO)):
        if X["esik_sha"] != _sha_esik5():
            raise DS5Hata(f"DS5_ESIK {ad} dosyasından sonra değişmiş")
        if X["kural_sha"] != _kural_sha5():
            raise DS5Hata(f"kural kaynağı {ad} dosyasından sonra değişmiş")
    if JO["pdf_sha"] != GU._sha(DS5_YOL["pdf"]):
        raise DS5Hata("DS5_ONAY.pdf onay anahtarından sonra değişmiş")
    T = ds5_test()
    ad = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
          "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
          "K13": "süreç", "K14": "boyut (gerçek para)"}
    tab = "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |\n|---|---|---|---|\n"
    for k, (yy, kn) in DS5_KONTROL.items():
        tab += f"| {k} | {ad[k]} | {yy} | {kn} |\n"
    st = _sentetik_tablo5(T)
    oz = J["ozet"]
    ot = ["| küme | n | P1 | P2 | P3 | P4 | P5 | fitil küçük | V1 VAR | V2 VAR | V3 VAR |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k_, o in oz.items():
        ot.append(f"| {k_} | {o['n']} | {o['P1_DOGRU']} | {o['P2_DOGRU']} | {o['P3_DOGRU']} | {o['P4_DOGRU']} | {o['P5_DOGRU']} | "
                  f"{o['fitil_kucuk_DOGRU']} | {o['V1_VAR']} | {o['V2_VAR']} | {o['V3_VAR']} |")
    on = ["| sayfa | pazar | grup (seçim) | V1 | P1 | P2 | P3 (dokunuş: ilk / ikinci) | P4 | P5 (üst kapanış) | düşen parça |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for s in JO["sayfalar"]:
        on.append(f"| {s['sayfa']} | {s['pazar']} | {s['grup']} | {s['yanit']['V1']} | {_isr5(s['P1'])} | {_isr5(s['P2'])} | "
                  f"{_isr5(s['P3'])} ({s['dokunus_n']}: {s['dokunus_ilk']} / {s['dokunus_ikinci']}) | {_isr5(s['P4'])} | "
                  f"{_isr5(s['P5'])} ({s['ust_kapanis_n']}) | {', '.join(s['V1_dusen']) or '-'} |")
    bel = "\n".join(f"- {k}: {v}" for k, v in DS5_ESIK["belirsizlik"].items())
    m = f"""# DİP SAVUNMASI v5 (DS5) — ÖN KAYIT (Cemal'in işaretleri AÇILMADAN mühürlenir)

Üretim: {GU._simdi()} (UTC). Soru: Cemal'in 23.11.2026 tarifi ("... dip savunması en derinden yukarı veya yatay bir çizgi takip eden mumları takip ederek var / yok demeli." + EK: "... bu yukarıdan sayılan mumların bir düşeni kırıyor olması gerekir; yani basit bir tepki içindeki dizilmiş mumlara dip savunması var demesin kod.") gövde altı destek çizgisi + düşen çizgi kırılımı kuralına çevrilince, iki kör sette (GOZ_UYUM_KOR.pdf = set 1, TANIM2_KOR.pdf = set 2; 80 sayfa) Cemal'in VAR / YOK işaretleriyle örtüşüyor mu? Ayrıca iki set ve DS4 onay seti dışından 24 sayfalık GÖRSEL ONAY PDF'i (Cemal'e henüz gönderilmedi). GETİRİ ÖLÇÜLMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/ds5_anahtar.json` sha256: `{GU._sha(DS5_YOL['anahtar'])}`
- kod: `arastirma_cikti/goz_uyum/ds5.py` sha256: `{GU._sha(DS5_YOL['kod'])}`
- eşik sözlüğü (DS5_ESIK) sha256: `{_sha_esik5()}`
- kural kaynağı (_ds5_cizgi + ds5_parca_dizi + ds5_parca) sha256: `{_kural_sha5()}`
- görsel onay PDF: `arastirma_cikti/goz_uyum/DS5_ONAY.pdf` sha256: `{GU._sha(DS5_YOL['pdf'])}`
- görsel onay anahtarı: `arastirma_cikti/goz_uyum/ds5_onay_anahtar.json` sha256: `{GU._sha(DS5_YOL['onay_anahtar'])}`
- iş tanımı: `arastirma_cikti/goz_uyum/DS5_IS_TANIMI.md` sha256: `{GU._sha(DS5_YOL['is_tanimi'])}`
- girdi (yalnız sayfa -> pazar, sembol, sinyal günü okundu): goz_uyum_anahtar.json `{J['girdi_sha']['goz_uyum_anahtar.json']}`, tanim2_anahtar.json `{J['girdi_sha']['tanim2_anahtar.json']}`; DS4 onay seti dışlaması için ds4_onay_anahtar.json `{GU._sha(DS5_YOL['ds4_onay_anahtar'])}`
- olay havuzu (görsel onay; pazar, sembol, tarih) sha256: `{JO['havuz_sha']}` (DS4 görsel onay havuzuyla aynı) ({json.dumps(JO['havuz'], ensure_ascii=False)})
- bağımlı kod: goz_uyum.py `{GU._sha(GU.GU_YOL['kod'])[:16]}`, tanim2.py `{GU._sha(TZ.TZ_YOL['kod'])[:16]}`, GOZ_ETIKET.py `{GU._sha(os.path.join(KOK5, 'GOZ_ETIKET.py'))[:16]}`

## 2. Kural (ADIM 1'de, etiketler açılmadan commit; parametreler iş tanımından aynen)
Pencere: kör sayfa penceresi (121 geçerli bar, veri sinyal günü t'de kesik); kural penceresi son 120 mum [t-119 .. t]. B_i = min(Open_i, Close_i) (gövde altı); ATR = ATR14(d).
- **DİP**: d = [t-119 .. t-8] aralığında en düşük Low'un günü (eşitlikte en son); m = t - d (>= 8, bilgi için kaydedilir).
- **P1 DÜŞÜŞTEN DİP**: d'den önceki pencere kısmında en yüksek High / Low(d) - 1 >= 0,20.
- **ÇİZGİ**: çapa (d, B_d); s* = min over i = d+1 .. t of (B_i - B_d) / (i - d) (çapadan geçen, sonraki bütün gövde altlarının altında kalan en dik doğru); L(i) = B_d + s* (i - d).
- **P2 YATAY YA DA YUKARI**: s* >= -0,05 x ATR / 20.
- **P3 TAKİP**: dokunuş = dipten sonraki mum, B_i - L(i) < 0,35 x ATR; en az 3 dokunuş VE dipten sonraki sürenin ilk yarısında en az 1 VE ikinci yarısında en az 1.
- **P4 DİP KORUNUR**: dipten sonra hiçbir Low < Low(d) - 0,25 x ATR.
- **P5 DİZİ DÜŞEN ÇİZGİYİ KIRIYOR** (EK, 23 Kas): düşen çizgi DS4 tanımıyla (d'den önceki pivot tepeler 5/5, pivot günü + 5 <= d; H1 = en yüksek pivot tepe; H2 = H1'den sonra, H1'den alçak SON pivot tepe; yoksa H1'den sonraki en yüksek; eğim < 0 değilse P5 YOK); dipten sonra KAPANIŞI düşen çizginin üstünde en az 3 mum VE son mumun (t) kapanışı çizginin üstünde VE P3 dokunuşlarından en az biri ilk kırılım gününden SONRA.
- **V1 (ANA)** = P1 ∧ P2 ∧ P3 ∧ P4 ∧ P5; **V2** = V1 ∧ (dip sonrası ortalama alt fitil (B_i - Low_i) dipten önceki 20 mumunkinden küçük); **V3** = P1 ∧ P2 ∧ P3 ∧ P4 (V1 ama P5 yok; basit tepki dahil). Bonferroni 3.

Tanım belirsizliklerinin çözümü (etiketlerden önce yazıldı):
{bel}

DS5_ESIK (tam): `{json.dumps(DS5_ESIK, ensure_ascii=False, sort_keys=True)}`

## 3. Sentetik sınama (`python arastirma_cikti/goz_uyum/ds5.py test`; gerçek veriden ÖNCE; dizinler t'ye göre)
{chr(10).join(st)}

Ek testler: eşit en düşük Low -> en son gün; prefix değişmezliği (3 kesik, dizi + DataFrame); tanım değişmezi (hiçbir dip sonrası gövde altı çizginin altında değil, en az biri üzerinde; bütün sentetik serilerde); kısa pencere ve H <= L penceresi reddedilir; hüküm fonksiyonu. Sonuç: {sum(x['esit'] for x in T['tablo'])} / {len(T['tablo'])} seri beklenene (V1 ve düşen parça kümesi) eşit.

## 4. Mühürlü yanıtlar (ds5_anahtar.json 'sayfalar'; Cemal'in işaretleri AÇILMADAN yazıldı)
{chr(10).join(ot)}

## 5. Görsel onay PDF'i (DS5_ONAY.pdf; iki set + DS4 onay seti dışından 24 yeni sayfa; anahtar ds5_onay_anahtar.json)
Seçim: {DS5_ESIK['onay']['secim']}.

{chr(10).join(on)}

## 6. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in set 1 (cemal_isaret.json) ve set 2 (cemal_isaret2.json) VAR / YOK işaretleri ile V1 / V2 / V3 arasında uyum ve Cohen kappa; set 1, set 2 ve birleşik; işaretsiz / '?' sayfa karar dışı, sayısı ayrıca yazılır.
- Aralık: kappa bootstrap (B {DS5_ESIK['kappa']['B']}, tohum {DS5_ESIK['kappa']['tohum']}, sayfa yeniden örneklemesi, yüzdelik): V1 için %95; V2 / V3 için Bonferroni 3 ile %98,33 (ayrıca %95 bilgi).
- HÜKÜM: {DS5_ESIK['hukum']}.
- Ek bilgi (hüküm dışı): uyuşmayan sayfalar ve düşen parça (P1 / P2 / P3 / P4 / P5); Cemal VAR / kod YOK sayfalarda düşen parça sayımı; GOVDE_1 (önceki birleşik kappa 0,35), DS4 V1 (0,13) ve DS3 V1 (-0,15) ile aynı sayfalarda karşılaştırma.
- Kural ve eşik sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 7. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
{tab}
## 8. Git kaydı (bu dosyanın yazıldığı an)
- ds5.py: {GU._gu_git('arastirma_cikti/goz_uyum/ds5.py')}
- DS5_IS_TANIMI.md: {GU._gu_git('arastirma_cikti/goz_uyum/DS5_IS_TANIMI.md')}
"""
    GU._yaz(DS5_YOL["onkayit"], m)
    import IZ_KARNE as IK
    r = IK.ik_kontrol_kapisi(DS5_YOL["onkayit"])
    d5log.info("kontrol kapısı: %s", "GEÇTİ" if r["gecti"] else r)
    return DS5_YOL["onkayit"]


def _ds5_muhur_oku() -> Dict[str, str]:
    if not os.path.exists(DS5_YOL["onkayit"]):
        raise DS5Hata("ön kayıt yok")
    t = open(DS5_YOL["onkayit"], encoding="utf-8").read(); out = {}
    for ad, desen in (("anahtar", r"ds5_anahtar\.json` sha256: `([0-9a-f]{64})`"), ("kod", r"ds5\.py` sha256: `([0-9a-f]{64})`"),
                      ("esik", r"eşik sözlüğü \(DS5_ESIK\) sha256: `([0-9a-f]{64})`"), ("kural", r"kural kaynağı \([^)]*\) sha256: `([0-9a-f]{64})`"),
                      ("pdf", r"DS5_ONAY\.pdf` sha256: `([0-9a-f]{64})`"), ("onay", r"ds5_onay_anahtar\.json` sha256: `([0-9a-f]{64})`")):
        mm = re.search(desen, t)
        if not mm:
            raise DS5Hata(f"ön kayıtta {ad} sha'sı yok")
        out[ad] = mm.group(1)
    return out


# ================================================================ 6) ÖLÇÜM
def _boot5(a: np.ndarray, b: np.ndarray, B: int, tohum: int, guven: Tuple[float, ...]) -> Dict[str, Any]:
    rng = np.random.default_rng(tohum); n = len(a); ks = np.empty(B)
    for i in range(B):
        j = rng.integers(0, n, n); ks[i] = GU.gu_kappa(a[j], b[j])
    g = ks[np.isfinite(ks)]; out: Dict[str, Any] = {"gecersiz": int(B - len(g))}
    for gv in guven:
        al = (1 - gv) / 2 * 100
        out[f"{gv:.4f}"] = [float(np.percentile(g, al)), float(np.percentile(g, 100 - al))] if len(g) else [np.nan, np.nan]
    return out


def ds5_hukum(k: float, alt: float, n: int) -> str:
    E = DS5_ESIK["kappa"]
    if n < int(E["karar_min"]) or not np.isfinite(k):
        return "ÖLÇÜLEMEDİ (karar sayısı < 30 ya da kappa tanımsız)"
    if k >= E["gecerli"] and np.isfinite(alt) and alt >= E["gecerli_alt"]:
        return "YARI BAĞIMSIZ GEÇERLİ"
    return "KISMEN" if k >= E["kismen"] else "GEÇERSİZ"


def _etiket_oku5(yol: str) -> Dict[int, str]:
    C = json.load(open(yol, encoding="utf-8"))
    atla = [k for k in C if not str(k).strip().isdigit()]
    if atla:
        d5log.warning("etiket dosyasında sayfa olmayan anahtar(lar) atlandı: %s", atla)
    return {int(k): (GU.gu_norm(v) or "?") for k, v in C.items() if str(k).strip().isdigit()}


def _govde1_cevap5(R: pd.DataFrame, kural: Dict[str, Any]) -> np.ndarray:
    import govde as GV                                                   # yalnız okunur (özellik + kural)
    out = []
    for r in R.itertuples(index=False):
        W = ds5_pencere(r.pazar, r.sembol, r.sinyal_gunu)
        x = GV.gv_ozellik(W)[kural["ozellik"]]
        out.append(bool(GV.gv_kural(np.array([x], float), kural["yon"], float(kural["esik"]))[0]))
    return np.array(out, bool)


def ds5_olc(deneme: bool = False, cemal1: Optional[str] = None, cemal2: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    if not deneme:
        M = _ds5_muhur_oku()
        for ad, gercek in (("anahtar", GU._sha(DS5_YOL["anahtar"])), ("kod", GU._sha(DS5_YOL["kod"])), ("esik", _sha_esik5()),
                           ("kural", _kural_sha5()), ("pdf", GU._sha(DS5_YOL["pdf"])), ("onay", GU._sha(DS5_YOL["onay_anahtar"]))):
            if gercek != M[ad]:
                raise DS5Hata(f"MÜHÜR BOZUK: {ad} sha'sı ön kayıttakiyle aynı değil -> DURDU")
    J = json.load(open(DS5_YOL["anahtar"], encoding="utf-8"))
    Sm = pd.DataFrame(J["sayfalar"])
    R = ds5_hesap(Sm[["set", "sayfa", "pazar", "sembol", "sinyal_gunu"]])     # K11: yanıtlar veriden yeniden hesaplanır
    for v in ("V1", "V2", "V3", "P1", "P2", "P3", "P4", "P5"):
        if (R[v].to_numpy(bool) != Sm[v].to_numpy(bool)).any():
            raise DS5Hata(f"{v} yanıtları veriden yeniden hesaplanınca mühürle aynı değil -> DURDU")
    acilis = GU._simdi()
    c1 = cemal1 or DS5_YOL["set1_cemal"]; c2 = cemal2 or DS5_YOL["set2_cemal"]
    et = {1: _etiket_oku5(c1), 2: _etiket_oku5(c2)}
    d5log.info("etiket dosyaları açıldı: %s (UTC)", acilis)
    for st in (1, 2):
        fazla = sorted(set(et[st]) - set(range(1, 41)))
        if fazla:
            raise DS5Hata(f"set {st} etiketinde anahtarda olmayan sayfa: {fazla}")
    Sm["cemal"] = [et[int(s)].get(int(p), "?") for s, p in zip(Sm.set, Sm.sayfa)]
    E = DS5_ESIK["kappa"]; bon = 1 - (1 - E["guven"]) / E["bonferroni_k"]
    if deneme:
        g1k = {"ozellik": "G1_govde_dokunus_n", "yon": ">=", "esik": 3.0, "not": "DENEME: uydurma kural"}
        ds3_v1 = {(int(s), int(p)): False for s, p in zip(Sm.set, Sm.sayfa)}; ds4_v1 = dict(ds3_v1)
    else:
        GJ = json.load(open(DS5_YOL["govde_anahtar"], encoding="utf-8")); g1k = dict(GJ["kurallar"]["GOVDE_1"]); del GJ
        D3 = json.load(open(DS5_YOL["ds3_anahtar"], encoding="utf-8"))
        ds3_v1 = {(int(s["set"]), int(s["sayfa"])): bool(s["V1"]) for s in D3["sayfalar"]}; del D3
        D4 = json.load(open(DS5_YOL["ds4_anahtar"], encoding="utf-8"))
        ds4_v1 = {(int(s["set"]), int(s["sayfa"])): bool(s["V1"]) for s in D4["sayfalar"]}; del D4
    Sm["GOVDE_1"] = _govde1_cevap5(Sm, g1k)
    Sm["DS4_V1"] = [ds4_v1[(int(s), int(p))] for s, p in zip(Sm.set, Sm.sayfa)]
    Sm["DS3_V1"] = [ds3_v1[(int(s), int(p))] for s, p in zip(Sm.set, Sm.sayfa)]
    kumeler = {"set 1": Sm.set == 1, "set 2": Sm.set == 2, "birleşik": Sm.set > 0}
    sonuc: Dict[str, Any] = {"etiket_acilis_utc": acilis, "deneme": deneme, "n_sayfa": int(len(Sm)), "kume": {}, "govde_kural": g1k}
    modeller = ("V1", "V2", "V3", "GOVDE_1", "DS4_V1", "DS3_V1")
    for kad, km in kumeler.items():
        K = Sm[km & (Sm.cemal != "?")]; cb = (K.cemal == "VAR").to_numpy(bool); n = len(K)
        kd: Dict[str, Any] = {"karar_n": int(n), "isaretsiz": int((km & (Sm.cemal == "?")).sum()),
                              "isaretsiz_sayfa": [f"set {s} / {p}" for s, p in zip(Sm[km & (Sm.cemal == '?')].set, Sm[km & (Sm.cemal == '?')].sayfa)],
                              "cemal_VAR": int(cb.sum()), "model": {}}
        for v in modeller:
            mod = K[v].to_numpy(bool)
            k = GU.gu_kappa(cb, mod)
            ar = _boot5(cb, mod, int(E["B"]), int(E["tohum"]), (E["guven"], bon)) if n else {}
            tp, tn = int((cb & mod).sum()), int((~cb & ~mod).sum()); fp, fn = int((~cb & mod).sum()), int((cb & ~mod).sum())
            a95 = ar.get(f"{E['guven']:.4f}", [np.nan, np.nan]); abn = ar.get(f"{bon:.4f}", [np.nan, np.nan])
            huk = (ds5_hukum(k, a95[0], n) if v == "V1" else
                   ("BİLGİ (Bonferroni alt uç ile: " + ds5_hukum(k, abn[0], n) + ")" if v in ("V2", "V3") else "BİLGİ (önceki kural)"))
            kd["model"][v] = {"kod_VAR": int(mod.sum()), "uyum": float(np.mean(cb == mod)) if n else np.nan, "kappa": k, "ar95": a95,
                              "ar_bon": abn, "hukum": huk,
                              "tablo": {"Cemal VAR + kod VAR": tp, "Cemal YOK + kod YOK": tn, "Cemal YOK + kod VAR": fp, "Cemal VAR + kod YOK": fn},
                              "uyusmayan": [f"set {s} / {p}" for s, p in zip(K.set[cb != mod], K.sayfa[cb != mod])]}
        sonuc["kume"][kad] = kd
    pl = ["P1", "P2", "P3", "P4", "P5"]
    X = Sm[(Sm.cemal == "VAR") & (~Sm.V1.astype(bool))]
    say: Dict[str, Any] = {"V1": {"n": int(len(X)), "dusen": {p: int((~X[p].astype(bool)).sum()) for p in pl},
                                  "yalniz_bu_dusen": {p: int(((~X[p].astype(bool)) & X[[q for q in pl if q != p]].astype(bool).all(axis=1)).sum())
                                                      for p in pl}}}
    Y = Sm[(Sm.cemal == "YOK") & (Sm.V1.astype(bool))]
    say["V1_cemal_YOK_kod_VAR"] = {"n": int(len(Y)), "sayfa": [f"set {s} / {p}" for s, p in zip(Y.set, Y.sayfa)]}
    sonuc["cemal_VAR_kod_YOK_parca"] = say
    uy = []
    for _, r in Sm.iterrows():
        if r.cemal == "?" or (r.cemal == "VAR") == bool(r.V1):
            continue
        rd = r.to_dict()
        uy.append({"sayfa": f"set {r.set} / {r.sayfa}", "cemal": r.cemal, **{v: ("VAR" if r[v] else "YOK") for v in modeller},
                   "m": int(r.m), "dusus": float(r.dusus), "s_atr20": float(r.s_atr20), "dokunus_n": int(r.dokunus_n),
                   "dokunus_ilk": int(r.dokunus_ilk), "dokunus_ikinci": int(r.dokunus_ikinci), "min_post_low_atr": float(r.min_post_low_atr),
                   "ust_kapanis_n": int(r.ust_kapanis_n), "son_ust": bool(r.son_ust),
                   "kirilim_m": (int(r.kirilim_idx) - int(r.t_idx)) if int(r.kirilim_idx) >= 0 else None,
                   "dusen": ds5_dusen(rd), "neden": ds5_neden_metni(rd)})
    sonuc["V1_uyusmayan"] = uy
    K = Sm[Sm.cemal != "?"]; cv = (K.cemal == "VAR")
    sonuc["karsilastirma"] = {f"V1_{o}": {"iki_kod_ayni_yanit": int((K.V1.astype(bool) == K[o].astype(bool)).sum()), "karar_n": int(len(K)),
                                          "kod_kappa": GU.gu_kappa(K.V1.to_numpy(bool), K[o].to_numpy(bool)),
                                          "V1_dogru_oteki_yanlis": int(((K.V1.astype(bool) == cv) & (K[o].astype(bool) != cv)).sum()),
                                          "oteki_dogru_V1_yanlis": int(((K.V1.astype(bool) != cv) & (K[o].astype(bool) == cv)).sum())}
                              for o in ("GOVDE_1", "DS4_V1", "DS3_V1")}
    sonuc["sayfa_cemal"] = {f"{s}/{p}": c for s, p, c in zip(Sm.set, Sm.sayfa, Sm.cemal)}
    md = _sonuc_md5(sonuc)
    hedef = cikti or DS5_DIR
    os.makedirs(hedef, exist_ok=True)
    GU._yaz(os.path.join(hedef, "DS5_SONUC.md"), md)
    GU._jyaz(os.path.join(hedef, "ds5_sonuc.json"), sonuc)
    return sonuc


def _sonuc_md5(S: Dict[str, Any]) -> str:
    B = S["kume"]["birleşik"]; v1 = B["model"]["V1"]
    L = [("# [DENEME — UYDURMA ETİKET] " if S["deneme"] else "# ") + "DİP SAVUNMASI v5 (DS5) — SONUÇ (iki kör set, 80 sayfa)", "",
         (f"Üretim: {GU._simdi()} (UTC). DENEME: uydurma etiket dosyaları; mühür denetimi YAPILMADI; 80 yanıt veriden yeniden hesaplandı, "
          "anahtarla aynı. GETİRİ YOK." if S["deneme"] else
          f"Üretim: {GU._simdi()} (UTC). Etiket dosyaları (cemal_isaret.json, cemal_isaret2.json) bu komutla açıldı: {S['etiket_acilis_utc']} (UTC). "
          "Mühür denetimi: ds5_anahtar.json, ds5.py, DS5_ESIK, kural kaynağı, DS5_ONAY.pdf ve ds5_onay_anahtar.json sha'ları DS5_ON_KAYIT ile aynı; "
          "80 sayfanın P1-P5 ve V1 / V2 / V3 yanıtı veriden yeniden hesaplandı, mühürle aynı. GETİRİ YOK."), "",
         f"Karar: birleşik {B['karar_n']} (Cemal VAR {B['cemal_VAR']}); işaretsiz / '?' (karar dışı): {B['isaretsiz']} {B['isaretsiz_sayfa']}.", "",
         f"## HÜKÜM (V1, ön kayıttaki eşikle): **{v1['hukum']}** — birleşik kappa {_f5(v1['kappa'])}, %95 [{_f5(v1['ar95'][0])}, {_f5(v1['ar95'][1])}]",
         "", "Sınır: Cemal tarifini DS4 görselini görerek verdi ve iki set önceki DS3 / DS4 işlerinde kullanıldı; bu yüzden sonuç YARI BAĞIMSIZDIR. "
         "Kesin hüküm yalnız Cemal'in görsel onayı (DS5_ONAY.pdf) + üçüncü bağımsız kör setle.", ""]
    s1 = S["kume"]["set 1"]["model"]["V1"]["kappa"]; s2 = S["kume"]["set 2"]["model"]["V1"]["kappa"]
    dus1 = bool(np.isfinite(s1) and s1 < 0.40); dus2 = bool(np.isfinite(s2) and s2 < 0.40)
    if dus1 and dus2:
        L += [f"NOT: V1 kappa set 1 {_f5(s1)}, set 2 {_f5(s2)}: İKİ SETTE DE < 0,40.", ""]
    elif dus1 or dus2:
        L += [f"NOT: **tutarsız** — V1 kappa set 1 {_f5(s1)}, set 2 {_f5(s2)}; biri < 0,40.", ""]
    L += ["## Kappa tablosu", "", "| model | küme | karar | kod VAR | uyum | kappa | %95 aralık | %98,33 (Bonferroni 3) | hüküm |",
          "|---|---|---|---|---|---|---|---|---|"]
    for v in ("V1", "V2", "V3", "GOVDE_1", "DS4_V1", "DS3_V1"):
        for kad in ("set 1", "set 2", "birleşik"):
            r = S["kume"][kad]["model"][v]; kd = S["kume"][kad]
            huk = r["hukum"] if kad == "birleşik" else ("ayrı rapor" if v == "V1" else "bilgi")
            L.append(f"| {v} | {kad} | {kd['karar_n']} | {r['kod_VAR']} | {_f5(r['uyum'])} | {_f5(r['kappa'])} | [{_f5(r['ar95'][0])}, "
                     f"{_f5(r['ar95'][1])}] | [{_f5(r['ar_bon'][0])}, {_f5(r['ar_bon'][1])}] | {huk} |")
    L += ["", f"V1 = P1 ∧ P2 ∧ P3 ∧ P4 ∧ P5 (ANA); V2 = V1 ∧ alt fitil küçük; V3 = P1 ∧ P2 ∧ P3 ∧ P4 (P5 yok, basit tepki dahil). GOVDE_1 = "
          f"{S['govde_kural'].get('ozellik')} {S['govde_kural'].get('yon')} {S['govde_kural'].get('esik')!r} (eşiği set 1 etiketleriyle seçildi -> "
          "set 1'de iç-örneklem); DS4_V1 = ds4_anahtar.json mühürlü V1; DS3_V1 = ds3_anahtar.json mühürlü V1.", "",
          f"HÜKÜM kuralı (ön kayıt): {DS5_ESIK['hukum']}.", "", "## 2x2", ""]
    for v in ("V1", "V2", "V3"):
        L += [f"**{v} birleşik**: " + "; ".join(f"{k} {x}" for k, x in B["model"][v]["tablo"].items()), ""]
    for kad in ("set 1", "set 2"):
        L += [f"**V1 {kad}**: " + "; ".join(f"{k} {x}" for k, x in S["kume"][kad]["model"]["V1"]["tablo"].items()), ""]
    P = S["cemal_VAR_kod_YOK_parca"]; x = P["V1"]
    L += ["## Cemal VAR dediği halde kodun (V1) YOK dediği sayfalarda düşen parça", "",
          f"Sayfa {x['n']}. Düşen parça sayımı (bir sayfada birden çok olabilir): " + "; ".join(f"{k} {c}" for k, c in x["dusen"].items()) +
          ". Yalnız bu parça düştü: " + "; ".join(f"{k} {c}" for k, c in x["yalniz_bu_dusen"].items()) + ".", "",
          f"Cemal YOK / kod V1 VAR: {P['V1_cemal_YOK_kod_VAR']['n']} sayfa {P['V1_cemal_YOK_kod_VAR']['sayfa']}.", "",
          "## V1 uyuşmayan sayfalar", "",
          "| sayfa | Cemal | V1 | V2 | V3 | GOVDE_1 | DS4_V1 | DS3_V1 | dip yaşı (mum) | düşüş | eğim (ATR / 20) | dokunuş (ilk / ikinci) | "
          "dip sonrası en düşük Low (ATR) | kırılım (t'ye göre) / üst kapanış | düşen parça | kodun gördüğü |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in S["V1_uyusmayan"]:
        ne = "; ".join(r["neden"]) if r["neden"] else "beş parça da DOĞRU (kod VAR)"
        L.append(f"| {r['sayfa']} | {r['cemal']} | {r['V1']} | {r['V2']} | {r['V3']} | {r['GOVDE_1']} | {r['DS4_V1']} | {r['DS3_V1']} | {r['m']} | "
                 f"%{r['dusus']*100:.0f} | {r['s_atr20']:+.2f} | {r['dokunus_n']} ({r['dokunus_ilk']} / {r['dokunus_ikinci']}) | "
                 f"{r['min_post_low_atr']:+.2f} | {('t%+d' % r['kirilim_m']) if r['kirilim_m'] is not None else '-'} / {r['ust_kapanis_n']} | "
                 f"{', '.join(r['dusen']) or '-'} | {ne} |")
    L += ["", "## Karşılaştırma: aynı sayfalarda önceki kurallar", ""]
    for o, G in S["karsilastirma"].items():
        L.append(f"- {o}: karar {G['karar_n']} sayfada iki kod {G['iki_kod_ayni_yanit']} sayfada aynı yanıt (kodlar arası kappa {_f5(G['kod_kappa'])}); "
                 f"V1 doğru / öteki yanlış {G['V1_dogru_oteki_yanlis']}; öteki doğru / V1 yanlış {G['oteki_dogru_V1_yanlis']}.")
    L += ["", "Not: uyum Cemal'in gözüyle uyumdur; getiri ölçülmedi. Kural Cemal'in tarifinden etiketlere bakmadan sabitlendi ve önce sentetik "
          "serilerde sınandı (DS3 / DS4 dersi)."]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", choices=["anahtar", "onay", "muhur", "olc", "test"])
    ap.add_argument("--deneme", action="store_true")
    ap.add_argument("--cemal1", default=None)
    ap.add_argument("--cemal2", default=None)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--havuz_onbellek", default=None)
    a = ap.parse_args()
    if a.deneme and not (a.cikti and a.cemal1 and a.cemal2):
        raise SystemExit("--deneme için --cikti, --cemal1, --cemal2 gerekli (gerçek etiket dosyaları açılmaz)")
    if a.deneme and ({os.path.realpath(a.cemal1), os.path.realpath(a.cemal2)} & {os.path.realpath(DS5_YOL["set1_cemal"]),
                                                                                os.path.realpath(DS5_YOL["set2_cemal"])}
                     or os.path.realpath(a.cikti) == os.path.realpath(DS5_DIR)):
        raise SystemExit("--deneme gerçek etiket dosyasını açamaz / gerçek çıktı dizinine yazamaz")
    if not a.deneme and (a.cemal1 or a.cemal2 or a.cikti):
        raise SystemExit("gerçek kipte --cemal1 / --cemal2 / --cikti verilmez (mühürlü yollar kullanılır)")
    if a.komut == "anahtar":
        J = ds5_anahtar(); print(json.dumps(J["ozet"], ensure_ascii=False))
    elif a.komut == "onay":
        J = ds5_onay(a.havuz_onbellek)
        print(json.dumps([(s["sayfa"], s["pazar"], s["grup"], s["yanit"]["V1"], s["V1_dusen"], s["dokunus_n"]) for s in J["sayfalar"]],
                         ensure_ascii=False))
    elif a.komut == "muhur":
        print(ds5_muhur())
    elif a.komut == "olc":
        r = ds5_olc(a.deneme, a.cemal1, a.cemal2, a.cikti)
        print(json.dumps({k: {"karar_n": v["karar_n"], **{m: _f5(x["kappa"]) for m, x in v["model"].items()}} for k, v in r["kume"].items()},
                         ensure_ascii=False))
    else:
        T = ds5_test()
        print(json.dumps({"tamam": T["tamam"], "kural_sha": T["kural_sha"], "esik_sha": T["esik_sha"]}, ensure_ascii=False))
        for x in T["tablo"]:
            print(x["seri"], "beklenen", x["beklenen_V1"], x["beklenen_dusen"], x["beklenen_ek"], "çıkan", x["cikan"], "düşen", x["dusen"],
                  "d", x["d"], "eğim", x["s_atr20"], "dok", x["dokunus"], x["ilk"], x["ikinci"], "minL", x["min_post_low_atr"],
                  "fitil", x["fitil_post"], x["fitil_once"])
