"""DS4 — DİP SAVUNMASI v4: Cemal'in DS3 görselini görünce verdiği tarif (23 Kasım 2026). GETİRİ ÖLÇMEZ.

Cemal (23.11.2026, aynen): "Burada kodun yanlışını buldum: en dip noktasında çizgi çekip bir düşeni kırmış mı, ve artık düşmüyor, yukarı
daha yukarıdan dönüyorsa VAR."
Ana model yorumu (üç parça): (P1) en dip noktası ve oradan yatay dip çizgisi (düşüşten gelen dip); (P2) dibe inerken tepelerden çizilen DÜŞEN
TREND ÇİZGİSİ fiyat tarafından yukarı kırılmış; (P3) dipten sonra dip delinmiyor ve geri çekilmeler dip çizgisinin ÜSTÜNDEN dönüyor (yükselen dip).
DS3 dersi (Ç212): formül sentetik örnekte sınanmadan kör sete gitti. Bu yüzden sıra: sentetik sınama (test) -> 80 sayfa yanıtı + görsel onay
PDF'i mühür (etiketler AÇILMADAN) -> ölçüm (olc).

Sinyal sonrası fiyat hiçbir adımda okunmaz: pencere = kör sayfa penceresi (tanim2.tz_pencere = goz_uyum._gu_pencere; veri sinyal günü t'de
KESİLİR, son 121 geçerli bar; kural penceresi son 120 mum [t-119 .. t]).
Komutlar (repo kökünden):
  python arastirma_cikti/goz_uyum/ds4.py test                  çakışma kapısı + sentetik seriler S1-S8 + prefix değişmezliği
  python arastirma_cikti/goz_uyum/ds4.py anahtar               iki setin 80 sayfası: P1 / P2 / P3 ara değerleri + V1 / V2 / V3 -> ds4_anahtar.json
  python arastirma_cikti/goz_uyum/ds4.py onay [--havuz_onbellek X.pkl]
                                                               iki set dışından 24 yeni sayfa -> DS4_ONAY.pdf + ds4_onay_anahtar.json
  python arastirma_cikti/goz_uyum/ds4.py muhur                 sha'lar + kural + sentetik tablo + hüküm + kontrol tablosu -> DS4_ON_KAYIT.md
  python arastirma_cikti/goz_uyum/ds4.py olc                   mühür denetimi + etiketleri AÇAR -> DS4_SONUC.md, ds4_sonuc.json
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

_CK_ONCE_DS4 = {k: id(v) for k, v in globals().items()}

import numpy as np
import pandas as pd

DS4_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(os.getcwd(), "arastirma_cikti", "goz_uyum")
if DS4_DIR not in sys.path:
    sys.path.insert(0, DS4_DIR)
import goz_uyum as GU  # noqa: E402  (yalnız okunur: gu_veri, gu_havuz, _gu_pencere, _sha, _jyaz, _yaz, _simdi, _gu_git, gu_kappa, gu_norm)
import tanim2 as TZ  # noqa: E402  (yalnız okunur: tz_pencere, TZ_YOL)

d4log = logging.getLogger("ds4")
if not d4log.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

KOK4 = GU.KOK
DS4_YOL = {"is_tanimi": os.path.join(DS4_DIR, "DS4_IS_TANIMI.md"), "anahtar": os.path.join(DS4_DIR, "ds4_anahtar.json"),
           "onkayit": os.path.join(DS4_DIR, "DS4_ON_KAYIT.md"), "sonuc": os.path.join(DS4_DIR, "DS4_SONUC.md"),
           "sonuc_json": os.path.join(DS4_DIR, "ds4_sonuc.json"), "pdf": os.path.join(DS4_DIR, "DS4_ONAY.pdf"),
           "onay_anahtar": os.path.join(DS4_DIR, "ds4_onay_anahtar.json"),
           "set1_anahtar": GU.GU_YOL["anahtar"], "set2_anahtar": TZ.TZ_YOL["anahtar"],
           "set1_cemal": os.path.join(DS4_DIR, "cemal_isaret.json"), "set2_cemal": os.path.join(DS4_DIR, "cemal_isaret2.json"),
           "govde_anahtar": os.path.join(DS4_DIR, "govde_anahtar.json"), "ds3_anahtar": os.path.join(DS4_DIR, "ds3_anahtar.json"),
           "kod": os.path.abspath(__file__) if "__file__" in globals() else os.path.join(DS4_DIR, "ds4.py")}

# ---------------------------------------------------------------- KURAL (Cemal'in tarifinden; etiketler okunmadan yazıldı; ADIM 1 commit'i)
# W = kör sayfa penceresi (121 geçerli bar, dizin 0..120, t = 120); kural penceresi = son 120 mum, dizin s0 = 1 .. t (t-119 .. t).
# DİP: d = [s0 .. t-5] aralığında en düşük Low'un günü (eşitlikte EN SON gün); dip çizgisi = Low(d).
# P1 DÜŞÜŞTEN DİP: max High [s0 .. d-1] / Low(d) - 1 >= 0,20.
# P2 DÜŞEN TREND KIRILIMI: pivot tepe j: H_j > max H[j-5..j-1] ve H_j >= max H[j+1..j+5], s0 <= j-5, j+5 <= d. H1 = en yüksek pivot tepe;
#    H2 = H1'den sonra gelen, H1'den alçak SON pivot tepe (yoksa H1'den sonraki en yüksek pivot tepe; o da yoksa P2 YOK). Düşen çizgi = H1-H2
#    doğrusu; eğim < 0 değilse P2 YOK. Kırılım = d < i <= t için en az bir Close_i > çizgi_i.
# P3 ARTIK DÜŞMÜYOR, DAHA YUKARIDAN DÖNÜYOR: (i) d < i <= t hiçbir Low_i < Low(d); (ii) pivot dip j: L_j < min L[j-3..j-1] ve
#    L_j <= min L[j+1..j+3], d < j, j+3 <= t, j-3 >= s0; en az bir pivot dip VE hepsi L_j > Low(d) + 0,5 x ATR14(d); (iii) pivot dip >= 2 ise
#    son pivot dip L >= ilk pivot dip L.
# V1 (ANA) = P1 ∧ P2 ∧ P3;  V2 = P1 ∧ P3;  V3 = P1 ∧ P2 ∧ P3(i).
DS4_ESIK: Dict[str, Any] = {
    "pencere_bar": 121, "kural_bar": 120, "dip_sonrasi_min": 5, "dusus_min": 0.20, "tepe_sol": 5, "tepe_sag": 5, "dip_sol": 3, "dip_sag": 3,
    "atr_n": 14, "bant_atr": 0.5,
    "belirsizlik": {
        "dip": "d = [t-119 .. t-5] aralığında en düşük Low'un günü; eşit en düşük Low birden çok günde ise EN SON gün (float ==). En düşük Low "
               "son 4 mumdaysa (t-4..t) d oraya gidemez; o mum dibi deldiği için P3(i) YANLIŞ olur ('dip çok yeni' = delinme)",
        "p1": "tepe = max High [t-119 .. d-1] (d hariç; d = t-119 ise tepe yok -> P1 YANLIŞ); oran = tepe / Low(d) - 1 >= 0,20",
        "pivot_tepe": "H_j > max(H_{j-5..j-1}) (sol kesin) ve H_j >= max(H_{j+1..j+5}) (sağ eşit olabilir); j-5 >= t-119 ve j+5 <= d "
                      "(pivot yalnız d'ye kadar onaylı tepeler)",
        "h1": "en yüksek pivot tepe; eşit yükseklikte EN ERKEN olan",
        "h2": "H1'den sonra (j > j1), H1'den KESİN alçak pivot tepelerin EN SONU; yoksa H1'den sonraki en yüksek pivot tepe (bu durumda eşit "
              "yükseklik -> eğim 0 -> P2 YOK); H1'den sonra pivot tepe yoksa P2 YOK",
        "cizgi": "çizgi_i = H1 + eğim x (i - j1), eğim = (H2 - H1) / (j2 - j1); eğim < 0 şart; sağa t'ye kadar uzatılır",
        "kirilim": "d < i <= t için Close_i > çizgi_i olan İLK gün = kırılım mumu; yoksa P2 YANLIŞ",
        "delinme": "P3(i): Low_i >= Low(d) bütün d < i <= t (eşitlik delinme sayılmaz)",
        "pivot_dip": "L_j < min(L_{j-3..j-1}) (sol kesin) ve L_j <= min(L_{j+1..j+3}); d < j, j+3 <= t (t'ye kadar onaylı), j-3 >= t-119",
        "atr": "TR_j = max(H_j - L_j, |H_j - C_{j-1}|, |L_j - C_{j-1}|); ATR14(d) = ortalama TR, j = max(1, d-13) .. d (121 barlık pencerenin "
               "dizini; dizin 0 yalnız önceki kapanış olarak kullanılabilir)",
        "bant": "P3(ii): her pivot dip L_j > Low(d) + 0,5 x ATR14(d) (kesin büyük); pivot dip yoksa P3(ii) YANLIŞ",
        "yukselen": "P3(iii): pivot dip sayısı >= 2 ise L(son) >= L(ilk); 0-1 pivot dipte DOĞRU (P3(ii) zaten pivot dip ister)",
    },
    "varyant": {"V1": "P1 ∧ P2 ∧ P3 (ANA)", "V2": "P1 ∧ P3 (trend kırılımı şartı yok)", "V3": "P1 ∧ P2 ∧ P3(i) (yükselen dip şartı yok)"},
    "kappa": {"B": 5000, "tohum": 20261125, "guven": 0.95, "bonferroni_k": 3, "gecerli": 0.60, "gecerli_alt": 0.40, "kismen": 0.40,
              "karar_min": 30},
    "hukum": "V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu "
             ">= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (Cemal tarifini DS3 görselindeki 6 set-1 sayfasını görerek "
             "verdi; kesin hüküm yalnız Cemal'in görsel onayı + üçüncü bağımsız kör setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) "
             "KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise "
             "'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33)",
    "onay": {"tohum": 20261125, "VAR": 16, "VAR_pazar": {"ABD": 12, "AVR": 2, "BIST": 2}, "YOK_P2": 2, "YOK_P3": 2, "YOK_rastgele": 4,
             "secim": "EK (ana model, 23 Kas): 24 sayfa. Havuz = goz_uyum.gu_havuz (Y1 ∧ Ş1, likidite) ABD + AVR + BIST; iki setteki (pazar, "
                      "sembol) çiftleri hariç; olaylar tohumla (20261125) karıştırılmış sırada gezilir, her (pazar, sembol) en çok 1 sayfa. "
                      "V1 VAR 16: karışık sıradaki İLK V1 VAR olaylar, pazar hedefi ABD 12 / AVR 2 / BIST 2 (seçme / ayıklama yok); bir pazarda "
                      "yetmezse eksik, aynı karışık sırada öteki pazarların sıradaki V1 VAR olaylarıyla doldurulur ve yazılır. V1 YOK 8: karışık "
                      "sırada ilk 4 V1 YOK -> 'rastgele' (nedeni ne olursa); sonra P1 ∧ P3 ∧ ¬P2 -> 'P2 düştü' (2); P1 ∧ P2 ∧ ¬P3 -> 'P3 düştü' "
                      "(2). Sayfa sırası: önce 16 VAR (karışık sıradaki geliş sırası), sonra 8 YOK (tohumla karıştırılmış); PDF kör değil, onay amaçlı"},
    "not": "parametreler (0,20; 5/5 tepe; 3/3 dip; 0,5 ATR14; d <= t-5) iş tanımından aynen; etiketlere bakılmadan sabitlendi; GETİRİ YOK",
}


class DS4Hata(RuntimeError):
    """Durdurucu hata: veri / mühür / tanım tutmadı."""


def _sha_esik4() -> str:
    return hashlib.sha256(json.dumps(DS4_ESIK, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _f4(x: Any, d: int = 3) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"{float(x):.{d}f}"
    except (TypeError, ValueError):
        return str(x)


# ================================================================ 1) KURAL (yalnız pencere; t sonrası yok)
def ds4_parca_dizi(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray) -> Dict[str, Any]:
    """Diziler kör sayfa penceresi (son eleman = t, 121 bar). P1 / P2 / P3 + ara değerler + V1 / V2 / V3. Dizinler 121 barlık pencerede."""
    E = DS4_ESIK
    O, H, L, C = (np.asarray(a, float) for a in (O, H, L, C))
    n = len(C)
    if n != int(E["pencere_bar"]):
        raise DS4Hata(f"pencere {n} bar (beklenen {E['pencere_bar']})")
    if not (np.all(np.isfinite(np.c_[O, H, L, C])) and np.all(H > L) and np.all(L > 0)):
        raise DS4Hata("geçersiz bar (NaN / H <= L / L <= 0) pencerede")
    t = n - 1; s0 = t - (int(E["kural_bar"]) - 1); B = int(E["dip_sonrasi_min"])
    ts, tg, ds_, dg, A = int(E["tepe_sol"]), int(E["tepe_sag"]), int(E["dip_sol"]), int(E["dip_sag"]), int(E["atr_n"])
    # DİP
    seg = L[s0:t - B + 1]; mn = float(seg.min())
    d = s0 + int(np.flatnonzero(seg == mn)[-1])
    Ld = float(L[d])
    gmn = float(L[s0:].min()); d_glob = s0 + int(np.flatnonzero(L[s0:] == gmn)[-1])
    # P1
    if d > s0:
        tepe_i = s0 + int(np.argmax(H[s0:d])); tepe = float(H[tepe_i]); dusus = tepe / Ld - 1.0
    else:
        tepe_i, tepe, dusus = -1, float("nan"), float("nan")
    p1 = bool(np.isfinite(dusus) and dusus >= float(E["dusus_min"]))
    # P2
    tepeler = [j for j in range(s0 + ts, d - tg + 1) if H[j] > H[j - ts:j].max() and H[j] >= H[j + 1:j + tg + 1].max()]
    j1 = j2 = kir = -1; egim = float("nan"); p2_neden = ""
    if not tepeler:
        p2_neden = "d'den önce onaylı pivot tepe yok"
    else:
        hv = np.array([H[j] for j in tepeler]); j1 = tepeler[int(np.flatnonzero(hv == hv.max())[0])]
        sonra = [j for j in tepeler if j > j1]
        alcak = [j for j in sonra if H[j] < H[j1]]
        if alcak:
            j2 = alcak[-1]
        elif sonra:
            hs = np.array([H[j] for j in sonra]); j2 = sonra[int(np.argmax(hs))]
        if j2 < 0:
            p2_neden = "H1'den sonra pivot tepe yok"
        else:
            egim = (float(H[j2]) - float(H[j1])) / float(j2 - j1)
            if not egim < 0:
                p2_neden = "H1-H2 çizgisi düşen değil (eğim >= 0)"
            else:
                post = np.arange(d + 1, t + 1)
                cizgi = float(H[j1]) + egim * (post - j1)
                ust = np.flatnonzero(C[post] > cizgi)
                if len(ust):
                    kir = int(post[ust[0]])
                else:
                    p2_neden = "d'den sonra hiçbir kapanış düşen çizginin üstünde değil"
    p2 = kir >= 0
    # P3
    post = np.arange(d + 1, t + 1)
    p3i = bool(np.all(L[post] >= Ld))
    min_post = float(L[post].min())
    jj = np.arange(max(1, d - A + 1), d + 1)
    tr = np.maximum(H[jj] - L[jj], np.maximum(np.abs(H[jj] - C[jj - 1]), np.abs(L[jj] - C[jj - 1])))
    atr = float(np.mean(tr))
    if not atr > 0:
        raise DS4Hata("ATR14(d) <= 0")
    bant = Ld + float(E["bant_atr"]) * atr
    dipler = [j for j in range(d + 1, t - dg + 1) if j - ds_ >= s0 and L[j] < L[j - ds_:j].min() and L[j] <= L[j + 1:j + dg + 1].min()]
    p3ii = bool(len(dipler) >= 1 and all(L[j] > bant for j in dipler))
    p3iii = bool(len(dipler) < 2 or L[dipler[-1]] >= L[dipler[0]])
    p3 = p3i and p3ii and p3iii
    return {"t_idx": int(t), "s0_idx": int(s0), "d_idx": int(d), "m": int(t - d), "low_d": Ld, "d_glob_idx": int(d_glob),
            "dip_yeni": bool(d_glob > t - B), "tepe_idx": int(tepe_i), "tepe": tepe, "dusus": float(dusus), "P1": p1,
            "pivot_tepeler": [int(j) for j in tepeler], "h1_idx": int(j1), "h1": float(H[j1]) if j1 >= 0 else float("nan"),
            "h2_idx": int(j2), "h2": float(H[j2]) if j2 >= 0 else float("nan"), "egim": float(egim),
            "egim_atr": float(egim / atr) if np.isfinite(egim) else float("nan"), "kirilim_idx": int(kir), "P2": bool(p2), "P2_neden": p2_neden,
            "min_post_low_oran": float(min_post / Ld - 1.0), "P3i": p3i, "atr_d": atr, "bant": float(bant),
            "pivot_dipler": [int(j) for j in dipler], "pivot_dip_low": [float(L[j]) for j in dipler],
            "pivot_dip_atr": [float((L[j] - Ld) / atr) for j in dipler], "P3ii": p3ii, "P3iii": p3iii, "P3": bool(p3),
            "V1": bool(p1 and p2 and p3), "V2": bool(p1 and p3), "V3": bool(p1 and p2 and p3i)}


def ds4_parca(W: pd.DataFrame) -> Dict[str, Any]:
    O, H, L, C = (W[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    r = ds4_parca_dizi(O, H, L, C)
    ix = W.index

    def tar(i: int) -> Optional[str]:
        return ix[i].strftime("%Y-%m-%d") if i >= 0 else None
    r["d_tarih"] = tar(r["d_idx"]); r["h1_tarih"] = tar(r["h1_idx"]); r["h2_tarih"] = tar(r["h2_idx"])
    r["kirilim_tarih"] = tar(r["kirilim_idx"]); r["pivot_dip_tarih"] = [tar(j) for j in r["pivot_dipler"]]
    return r


def _kural_sha4() -> str:
    """Kural kaynağının (ds4_parca_dizi + ds4_parca) sha'sı: olc'de kuralın değişmediği ayrıca denetlenir."""
    src = inspect.getsource(ds4_parca_dizi) + inspect.getsource(ds4_parca)
    return hashlib.sha256(src.encode("utf-8")).hexdigest()


def ds4_dusen(r: Dict[str, Any]) -> List[str]:
    """V1'i düşüren parçalar (P1 / P2 / P3(i) / P3(ii) / P3(iii))."""
    out = []
    if not r["P1"]:
        out.append("P1")
    if not r["P2"]:
        out.append("P2")
    if not r["P3i"]:
        out.append("P3(i)")
    if not r["P3ii"]:
        out.append("P3(ii)")
    if not r["P3iii"]:
        out.append("P3(iii)")
    return out


def ds4_neden_metni(r: Dict[str, Any]) -> List[str]:
    out = []
    if not r["P1"]:
        out.append("P1 düşüş yok (%s < %%20)" % ("-" if not np.isfinite(r["dusus"]) else f"%{r['dusus']*100:.0f}"))
    if not r["P2"]:
        out.append(f"P2 {r['P2_neden']}")
    if not r["P3i"]:
        out.append(f"P3(i) dip delinmiş (dip sonrası en düşük Low {r['min_post_low_oran']*100:+.1f}%)")
    if not r["P3ii"]:
        if not r["pivot_dipler"]:
            out.append("P3(ii) dip sonrası onaylı pivot dip yok")
        else:
            out.append("P3(ii) pivot dip dibe yapışık (en yakın " + _f4(min(r["pivot_dip_atr"]), 2) + " ATR <= 0,5)")
    if not r["P3iii"]:
        out.append("P3(iii) son pivot dip ilkinden düşük")
    return out


# ================================================================ 2) SETLER (anahtar dosyalarından YALNIZ sayfa -> pazar, sembol, sinyal günü)
def ds4_setler() -> pd.DataFrame:
    rows = []
    for st, yol in ((1, DS4_YOL["set1_anahtar"]), (2, DS4_YOL["set2_anahtar"])):
        J = json.load(open(yol, encoding="utf-8"))
        for s in J["sayfalar"]:
            rows.append({"set": st, "sayfa": int(s["sayfa"]), "pazar": str(s["pazar"]), "sembol": str(s["sembol"]),
                         "sinyal_gunu": str(s["sinyal_gunu"])[:10]})
        del J
    S = pd.DataFrame(rows).sort_values(["set", "sayfa"]).reset_index(drop=True)
    for st in (1, 2):
        s = S[S.set == st].sayfa.tolist()
        if s != list(range(1, 41)):
            raise DS4Hata(f"set {st} sayfaları 1..40 değil: {s[:5]}..")
    return S


_VERI4: Dict[str, Dict[str, pd.DataFrame]] = {}


def ds4_pencere(pazar: str, sembol: str, t: str) -> pd.DataFrame:
    if pazar not in _VERI4:
        d4log.info("veri yükleniyor: %s", pazar)
        _VERI4[pazar] = GU.gu_veri(pazar)
    tt = pd.Timestamp(t)
    W = TZ.tz_pencere(pazar, sembol, tt, _VERI4[pazar])                 # K2: veri t'de kesik + mekanik denetim (121 bar, son = t)
    if W.index.max() > tt or W.index[-1] != tt or len(W) != int(DS4_ESIK["pencere_bar"]):
        raise DS4Hata(f"{sembol} {t}: pencere t sonrasını içeriyor / 121 bar değil")
    return W


def _temiz(r: Dict[str, Any]) -> Dict[str, Any]:
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


def ds4_hesap(S: pd.DataFrame) -> pd.DataFrame:
    out = []
    for r in S.itertuples(index=False):
        W = ds4_pencere(r.pazar, r.sembol, r.sinyal_gunu)
        out.append(ds4_parca(W))
    return pd.concat([S.reset_index(drop=True), pd.DataFrame(out)], axis=1)


def _ozet(R: pd.DataFrame) -> Dict[str, Any]:
    return {"n": int(len(R)), **{f"{v}_VAR": int(R[v].sum()) for v in ("V1", "V2", "V3")},
            **{f"{p}_DOGRU": int(R[p].sum()) for p in ("P1", "P2", "P3i", "P3ii", "P3iii", "P3")}}


def ds4_anahtar() -> Dict[str, Any]:
    t0 = time.time()
    S = ds4_setler()
    R = ds4_hesap(S)
    sayfalar = []
    for r in R.to_dict("records"):
        r = _temiz(r)
        r["yanit"] = {v: ("VAR" if r[v] else "YOK") for v in ("V1", "V2", "V3")}
        r["V1_dusen"] = ds4_dusen(r)
        sayfalar.append(r)
    ozet = {str(st): _ozet(R if st == "birlesik" else R[R.set == st]) for st in (1, 2, "birlesik")}
    J = {"surum": "ds4 v1", "uretim_utc": GU._simdi(),
         "uyari": "GETİRİ YOK; Cemal'in işaretleri bu dosya yazılırken AÇILMADI (etiketler yalnız mühürden sonra olc ile açılır); "
                  "dizinler 121 barlık pencerede (t = 120)",
         "esik": DS4_ESIK, "esik_sha": _sha_esik4(), "kural_sha": _kural_sha4(),
         "girdi_sha": {"goz_uyum_anahtar.json": GU._sha(DS4_YOL["set1_anahtar"]), "tanim2_anahtar.json": GU._sha(DS4_YOL["set2_anahtar"])},
         "ozet": ozet, "sayfalar": sayfalar, "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(DS4_YOL["anahtar"], J)
    d4log.info("anahtar: %s", json.dumps(ozet, ensure_ascii=False))
    return J


# ================================================================ 3) GÖRSEL ONAY (iki set dışından 24 yeni sayfa; EK 23 Kas)
def ds4_havuz(onbellek: Optional[str] = None) -> pd.DataFrame:
    """goz_uyum.gu_havuz (Y1 ∧ Ş1, likidite) üç pazar; yalnız (pazar, sembol, tarih). onbellek verilirse ve varsa oradan okunur (deterministik
    fonksiyonun hız kopyası; sha ds4_onay_anahtar.json'a yazılır)."""
    if onbellek and os.path.exists(onbellek):
        P = pd.read_pickle(onbellek)
        d4log.info("havuz önbellekten: %s (%d olay)", onbellek, len(P))
    else:
        P = pd.concat([GU.gu_havuz(p, 4)[["pazar", "sembol", "tarih"]] for p in ("BIST", "AVR", "ABD")]).reset_index(drop=True)
        if onbellek:
            P.to_pickle(onbellek)
    P = P[["pazar", "sembol", "tarih"]].copy(); P["tarih"] = pd.to_datetime(P["tarih"])
    return P.sort_values(["pazar", "sembol", "tarih"], kind="mergesort").reset_index(drop=True)


def ds4_onay_sec(P: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    Eo = DS4_ESIK["onay"]; rng = np.random.default_rng(int(Eo["tohum"]))
    S = ds4_setler(); haric = {(a, b) for a, b in zip(S.pazar, S.sembol)}
    Q = P[[(a, b) not in haric for a, b in zip(P.pazar, P.sembol)]].reset_index(drop=True)
    kota = {"VAR": int(Eo["VAR"]), "YOK_rastgele": int(Eo["YOK_rastgele"]), "YOK_P2": int(Eo["YOK_P2"]), "YOK_P3": int(Eo["YOK_P3"])}
    vpk = {p: int(x) for p, x in Eo["VAR_pazar"].items()}
    if sum(vpk.values()) != kota["VAR"]:
        raise DS4Hata("VAR pazar hedefleri toplamı VAR kotasına eşit değil")
    sira = rng.permutation(len(Q))
    # karışık sırada her olay için kural (tam havuz; seçimden bağımsız, kayıt için sayılır)
    K: List[Dict[str, Any]] = []
    for j in sira:
        q = Q.iloc[int(j)]
        W = ds4_pencere(q.pazar, q.sembol, q.tarih.strftime("%Y-%m-%d"))
        K.append({"pazar": q.pazar, "sembol": q.sembol, "sinyal_gunu": q.tarih.strftime("%Y-%m-%d"), **_temiz(ds4_parca(W))})
    al: Dict[str, List[Dict[str, Any]]] = {k: [] for k in kota}; kullanilan: set = set(); notlar: List[str] = []
    var_say = {p: 0 for p in vpk}
    for r in K:                                                           # 1. geçiş: VAR pazar hedefli; YOK grupları
        key = (r["pazar"], r["sembol"])
        if key in kullanilan:
            continue
        grup = None
        if r["V1"]:
            if var_say.get(r["pazar"], 0) < vpk.get(r["pazar"], 0):
                grup = "VAR"; var_say[r["pazar"]] += 1
        elif len(al["YOK_rastgele"]) < kota["YOK_rastgele"]:
            grup = "YOK_rastgele"
        elif r["P1"] and r["P3"] and not r["P2"] and len(al["YOK_P2"]) < kota["YOK_P2"]:
            grup = "YOK_P2"
        elif r["P1"] and r["P2"] and not r["P3"] and len(al["YOK_P3"]) < kota["YOK_P3"]:
            grup = "YOK_P3"
        if grup:
            kullanilan.add(key); al[grup].append({**r, "grup": grup})
    for p in vpk:
        if var_say[p] < vpk[p]:
            notlar.append(f"V1 VAR {p}: hedef {vpk[p]}, havuzda bulunan {var_say[p]}")
    if len(al["VAR"]) < kota["VAR"]:                                      # 2. geçiş: en yakın = aynı karışık sırada öteki pazarlar
        for r in K:
            if len(al["VAR"]) >= kota["VAR"]:
                break
            key = (r["pazar"], r["sembol"])
            if r["V1"] and key not in kullanilan:
                kullanilan.add(key); al["VAR"].append({**r, "grup": "VAR"})
                notlar.append(f"V1 VAR eksiği {r['pazar']} ile dolduruldu")
    eksik = {k: kota[k] - len(al[k]) for k in kota if len(al[k]) < kota[k]}
    if eksik:
        raise DS4Hata(f"görsel onay kotası dolmadı: {eksik}")
    Y = pd.DataFrame([x for k in ("YOK_P2", "YOK_P3", "YOK_rastgele") for x in al[k]])
    Y = Y.iloc[rng.permutation(len(Y))]
    T = pd.concat([pd.DataFrame(al["VAR"]), Y]).reset_index(drop=True)
    T.insert(0, "sayfa", np.arange(1, len(T) + 1))
    KD = pd.DataFrame(K)
    bilgi = {"havuz_n": int(len(P)), "iki_set_haric_n": int(len(Q)),
             "havuz_pazar": {p: int((P.pazar == p).sum()) for p in ("ABD", "AVR", "BIST")},
             "iki_set_haric_pazar": {p: int((Q.pazar == p).sum()) for p in ("ABD", "AVR", "BIST")},
             "havuz_V1_VAR": {p: int(KD[KD.pazar == p].V1.sum()) for p in ("ABD", "AVR", "BIST")},
             "havuz_parca": {k: int(KD[k].sum()) for k in ("P1", "P2", "P3i", "P3ii", "P3iii", "P3", "V1", "V2", "V3")},
             "VAR_pazar_sayfa": {p: int(sum(1 for x in al["VAR"] if x["pazar"] == p)) for p in ("ABD", "AVR", "BIST")}, "notlar": notlar}
    return T, bilgi


def _isr(x: bool) -> str:
    return "✓" if x else "✗"


def ds4_sayfa_ciz(W: pd.DataFrame, r: Dict[str, Any], no: int, toplam: int):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure(figsize=(7.5, 10.5))
    ax = fig.add_axes([0.04, 0.25, 0.92, 0.60])
    O, H, L, C = (W[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    t = int(r["t_idx"]); s0 = int(r["s0_idx"]); d = int(r["d_idx"])
    idx = np.arange(s0, t + 1); x = idx - t                                     # 120 mum: -119 .. 0
    Hs, Ls = H[idx], L[idx]; aralik = float(Hs.max() - Ls.min()); pad = aralik * 0.05
    renk = np.where(C[idx] >= O[idx], "#1a9850", "#d73027")
    ax.vlines(x, Ls, Hs, colors=renk, linewidth=1.1, zorder=3)
    for xi, o, c, col in zip(x, O[idx], C[idx], renk):
        ax.add_patch(Rectangle((xi - 0.35, min(o, c)), 0.7, max(abs(c - o), aralik * 0.0008), facecolor=col, edgecolor=col, linewidth=0.4,
                               zorder=4))
    xd = d - t
    # 0,5 ATR bandı (dip çizgisi .. dip + 0,5 ATR), dipten sinyal gününe
    ax.fill_between([xd - 0.5, 0.5], [r["low_d"]] * 2, [r["bant"]] * 2, color="#d9d9d9", alpha=0.7, zorder=1, linewidth=0)
    ax.hlines(r["low_d"], xd - 0.5, 0.5, colors="#1f4e9c", linestyles="--", linewidth=1.4, zorder=6)
    ax.annotate("DİP", xy=(xd, L[d]), xytext=(xd, L[d] - pad * 1.6), ha="center", va="top", fontsize=10, color="#1f4e9c", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#1f4e9c", lw=1.5), zorder=8)
    if r["h1_idx"] >= 0 and r["h2_idx"] >= 0 and np.isfinite(r["egim"]):
        j1, j2 = int(r["h1_idx"]), int(r["h2_idx"])
        xs = np.array([j1, t]); ys = r["h1"] + r["egim"] * (xs - j1)
        ax.plot(xs - t, ys, color="#e31a1c" if r["egim"] < 0 else "#fb9a99", linewidth=1.8, zorder=7)
        ax.plot([j1 - t, j2 - t], [r["h1"], r["h2"]], linestyle="none", marker="o", markersize=6, markerfacecolor="none",
                markeredgecolor="#e31a1c", markeredgewidth=1.5, zorder=8)
        ax.text(j1 - t, r["h1"] + pad * 0.3, "H1", ha="center", va="bottom", fontsize=8, color="#e31a1c")
        ax.text(j2 - t, r["h2"] + pad * 0.3, "H2", ha="center", va="bottom", fontsize=8, color="#e31a1c")
    if r["kirilim_idx"] >= 0:
        k = int(r["kirilim_idx"])
        ax.plot([k - t], [H[k] + pad * 0.6], marker="*", markersize=16, color="#ff7f00", markeredgecolor="#7f3f00", zorder=9)
    for j in r["pivot_dipler"]:
        ax.annotate("", xy=(j - t, L[j]), xytext=(j - t, L[j] - pad * 1.3),
                    arrowprops=dict(arrowstyle="-|>", color="#00a651", lw=1.8), zorder=8)
    ax.axvline(0.5, color="#555555", linewidth=0.8, zorder=2); ax.axvline(-0.5, color="#555555", linewidth=0.8, zorder=2)
    ust = max(Hs.max(), (r["h1"] if np.isfinite(r["h1"]) else Hs.max()))
    ax.set_ylim(Ls.min() - pad * 2.2, ust + pad * 1.4); ax.set_xlim(x[0] - 1, 2)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.6); sp.set_color("#888888")
    fig.text(0.04, 0.945, f"{int(no)}", fontsize=44, fontweight="bold", va="center", ha="left")
    fig.text(0.96, 0.945, f"/ {toplam}", fontsize=16, va="center", ha="right", color="#666666")
    fig.text(0.50, 0.885, "mavi kesik = dip çizgisi · gri bant = dip + yarım ATR · kırmızı = düşen çizgi (H1-H2) · yıldız = kırılım mumu · "
             "yeşil ok = dip sonrası dönüş dipleri", fontsize=7.2, ha="center", color="#555555")
    fig.text(0.50, 0.868, "sağdaki iki ince çizgi arası = son gün", fontsize=7.2, ha="center", color="#555555")
    s1 = (f"Düşüşten dip {_isr(r['P1'])}   —   Düşen çizgi kırıldı {_isr(r['P2'])}   —   Dip üstünden dönüyor {_isr(r['P3'])}")
    fig.text(0.50, 0.200, s1, fontsize=12, ha="center", va="center")
    fig.text(0.50, 0.155, f"SONUÇ: {'VAR' if r['V1'] else 'YOK'}", fontsize=20, fontweight="bold", ha="center", va="center")
    fig.text(0.50, 0.075, "☐ KOD DOĞRU GÖRÜYOR        ☐ YANLIŞ (neresi): ____________", fontsize=14, ha="center", va="center")
    return fig


def ds4_onay(onbellek: Optional[str] = None) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    t0 = time.time()
    P = ds4_havuz(onbellek)
    hsha = hashlib.sha256(P.assign(tarih=P.tarih.dt.strftime("%Y-%m-%d")).to_csv(index=False).encode("utf-8")).hexdigest()
    T, bilgi = ds4_onay_sec(P)
    yol = DS4_YOL["pdf"]
    with PdfPages(yol, metadata={"Title": "DIP SAVUNMASI - gorsel onay", "Author": "ds4", "Creator": "ds4", "Producer": "ds4",
                                 "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(7.5, 10.5))
        fig.text(0.5, 0.88, "DİP SAVUNMASI — kodun gözü (v4)", fontsize=22, fontweight="bold", ha="center")
        kapak = ("Senin tarifin: en dibe yatay çizgi; düşen çizgi kırıldı mı;\n"
                 "artık düşmüyor, daha yukarıdan dönüyor mu.\n\n"
                 "Kod bunları sayfalara çizdi.\n"
                 "Her sayfada kod senin gibi mi görüyor?\n"
                 "Yanlışsa doğru çizgiyi çiz.\n\n"
                 "İlk 16 sayfa kodun VAR dediği rastgele örnekler:\n"
                 "kod hepsini senin tarifinle mi seçiyor?")
        fig.text(0.5, 0.78, kapak, fontsize=15, ha="center", va="top", linespacing=1.5)
        aciklama = ("Çizimler:\n"
                    "  DİP oku + mavi kesik çizgi = en dip ve oradan yatay dip çizgisi\n"
                    "  kırmızı çizgi = dibe inerken iki tepeden (H1, H2) çizilen düşen çizgi, sağa uzatıldı\n"
                    "  turuncu yıldız = düşen çizginin üstünde kapanan ilk mum (kırılım)\n"
                    "  yeşil ok = dipten sonraki dönüş dipleri\n"
                    "  gri bant = dip çizgisinin yarım ATR (ortalama mum boyunun yarısı) üstü;\n"
                    "      dönüş dipleri bu bandın ÜSTÜNDE olmalı\n\n"
                    "Sayfanın altında kodun cevabı: üç parça ✓ / ✗ ve SONUÇ.\n"
                    f"{len(T)} sayfa: önce {int((T.V1.astype(bool)).sum())} VAR, sonra {int((~T.V1.astype(bool)).sum())} YOK "
                    "(bu PDF kör değil, onay için).\n"
                    "Daha önce görmediğin yeni grafikler. Hisse adı yok; son günden sonrası gösterilmez.\n"
                    "Kutulardan birini işaretlemen yeter.")
        fig.text(0.08, 0.40, aciklama, fontsize=10, ha="left", va="top", linespacing=1.4)
        pdf.savefig(fig); plt.close(fig)
        for rr in T.to_dict("records"):
            W = ds4_pencere(rr["pazar"], rr["sembol"], rr["sinyal_gunu"])
            r = ds4_parca(W)
            if r["V1"] != bool(rr["V1"]):
                raise DS4Hata("onay: V1 yeniden hesapta seçimden farklı")
            fig = ds4_sayfa_ciz(W, r, int(rr["sayfa"]), len(T))
            pdf.savefig(fig); plt.close(fig)
    boy = os.path.getsize(yol)
    if boy >= 6 * 1024 * 1024:
        raise DS4Hata(f"PDF 6 MB'tan büyük: {boy}")
    sayfalar = []
    for rr in T.to_dict("records"):
        rr = _temiz(rr); rr["V1_dusen"] = ds4_dusen(rr); rr["neden"] = ds4_neden_metni(rr)
        rr["yanit"] = {v: ("VAR" if rr[v] else "YOK") for v in ("V1", "V2", "V3")}
        sayfalar.append(rr)
    J = {"surum": "ds4 onay v1", "uretim_utc": GU._simdi(),
         "uyari": "GİZLİ ANAHTAR (hisse adları): Cemal DS4_ONAY.pdf'i işaretlemeden önce gösterilmez. GETİRİ YOK.",
         "esik_sha": _sha_esik4(), "kural_sha": _kural_sha4(), "havuz_sha": hsha, "havuz": bilgi,
         "pdf_sha": GU._sha(yol), "pdf_bayt": boy, "sayfalar": sayfalar, "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(DS4_YOL["onay_anahtar"], J)
    d4log.info("onay PDF %s (%.2f MB): %s", yol, boy / 1e6, [(s["sayfa"], s["grup"], s["yanit"]["V1"]) for s in sayfalar])
    return J


# ================================================================ 4) TEST (sentetik seriler; kör / gerçek veriden ÖNCE)
def ds4_cakisma_kontrol() -> None:
    ez = [k for k, v in _CK_ONCE_DS4.items() if k in globals() and id(globals()[k]) != v and not k.startswith("_")]
    if ez:
        raise DS4Hata(f"çakışma kapısı: bellekteki mevcut ad(lar) ezildi: {ez[:5]}")


def _seri(capalar: List[Tuple[int, float]], r: float = 0.3) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """121 bar: orta fiyat çapa noktaları arasında doğrusal; O_i = p_{i-1}, C_i = p_i, H = max(O,C) + r, L = min(O,C) - r."""
    xs = [a for a, _ in capalar]; ys = [b for _, b in capalar]
    if xs[0] != 0 or xs[-1] != 120:
        raise DS4Hata("sentetik çapalar 0 .. 120 olmalı")
    p = np.interp(np.arange(121), xs, ys)
    O = np.r_[p[0], p[:-1]]; C = p.copy()
    H = np.maximum(O, C) + r; L = np.minimum(O, C) - r
    return O, H, L, C


_DUSUS = [(0, 148.0), (8, 152.0), (20, 135.0), (28, 140.0), (40, 122.0), (48, 127.0), (60, 110.0), (66, 114.0), (80, 100.0)]


def ds4_sentetik() -> Dict[str, Dict[str, Any]]:
    """Sentetik seriler ve beklenen yanıtlar (iş tanımı S1-S6 + ek S7-S8)."""
    S: Dict[str, Dict[str, Any]] = {}
    O, H, L, C = _seri(_DUSUS + [(92, 112.0), (100, 106.0), (120, 118.0)]); L[80] -= 0.3
    S["S1"] = {"tarif": "düşüş -> dip -> düşen çizgiyi kıran yükseliş -> dibin üstünde dönen geri çekilme", "seri": (O, H, L, C),
               "beklenen": {"V1": True, "V2": True, "V3": True}}
    O, H, L, C = _seri(_DUSUS + [(92, 112.0), (100, 97.0), (120, 118.0)]); L[80] -= 0.3; L[100] -= 0.3
    S["S2"] = {"tarif": "S1 gibi ama geri çekilme dibi deliyor (97 < 100; yeni dip sonrası dönüş dibi yok)", "seri": (O, H, L, C),
               "beklenen": {"V1": False, "V2": False, "V3": True}}
    O, H, L, C = _seri([(0, 145.0), (10, 150.0), (25, 135.0), (40, 146.0), (55, 132.0), (70, 140.0), (80, 100.0), (92, 112.0), (100, 106.0),
                        (120, 115.0)]); L[80] -= 0.3
    S["S3"] = {"tarif": "dip ve yükselen dip var ama yavaş düşen çizgi (H1-H2) kırılmamış", "seri": (O, H, L, C),
               "beklenen": {"V1": False, "V2": True, "V3": False}}
    O, H, L, C = _seri(_DUSUS + [(86, 103.0), (92, 100.1), (98, 103.0), (120, 104.0)]); L[80] -= 0.3
    S["S4"] = {"tarif": "dip sonrası yatay, dönüş dibi dibe yapışık (< 0,5 ATR)", "seri": (O, H, L, C),
               "beklenen": {"V1": False, "V2": False, "V3": True}}
    k = np.arange(121); p = 100.0 + 1.5 * np.sin(k / 6.0)
    O, H, L, C = _seri([(int(i), float(v)) for i, v in zip(k, p)])
    S["S5"] = {"tarif": "düşüş yok, yatay dalgalı seri", "seri": (O, H, L, C), "beklenen": {"V1": False, "V2": False, "V3": False}}
    O, H, L, C = _seri(_DUSUS[:-1] + [(117, 95.0), (120, 97.0)])
    S["S6"] = {"tarif": "dip çok yeni: en düşük Low t-3'te (d t-5'ten sonraya gidemez, o mum dibi deler)", "seri": (O, H, L, C),
               "beklenen": {"V1": False, "V2": False, "V3": False}}
    O, H, L, C = _seri(_DUSUS + [(92, 112.0), (100, 106.0), (120, 118.0)]); L[80] -= 0.3; L[118] = L[80] - 0.5
    S["S7"] = {"tarif": "S1 gibi ama son 4 mumda (t-2) dip deliniyor", "seri": (O, H, L, C), "beklenen": {"V1": False, "V2": False, "V3": False}}
    O, H, L, C = _seri([(0, 150.0), (80, 100.0), (92, 112.0), (100, 106.0), (120, 118.0)]); L[80] -= 0.3
    S["S8"] = {"tarif": "tek düz düşüş (pivot tepe yok -> düşen çizgi kurulamaz), dip sonrası S1 gibi", "seri": (O, H, L, C),
               "beklenen": {"V1": False, "V2": True, "V3": False}}
    O, H, L, C = _seri(_DUSUS + [(86, 108.0), (92, 105.0), (98, 110.0), (104, 103.0), (120, 112.0)]); L[80] -= 0.3
    S["S9"] = {"tarif": "S1 gibi ama ikinci dönüş dibi ilkinden alçak (105 -> 103, ikisi de bandın üstünde)", "seri": (O, H, L, C),
               "beklenen": {"V1": False, "V2": False, "V3": True}}
    return S


def ds4_test() -> Dict[str, Any]:
    ds4_cakisma_kontrol()
    tablo = []
    for ad, s in ds4_sentetik().items():
        r = ds4_parca_dizi(*s["seri"])
        cik = {v: bool(r[v]) for v in ("V1", "V2", "V3")}
        tablo.append({"seri": ad, "tarif": s["tarif"], "beklenen": {v: ("VAR" if x else "YOK") for v, x in s["beklenen"].items()},
                      "cikan": {v: ("VAR" if x else "YOK") for v, x in cik.items()},
                      "P1": r["P1"], "P2": r["P2"], "P3i": r["P3i"], "P3ii": r["P3ii"], "P3iii": r["P3iii"], "d": r["d_idx"] - r["t_idx"],
                      "h1": r["h1_idx"] - r["t_idx"] if r["h1_idx"] >= 0 else None, "h2": r["h2_idx"] - r["t_idx"] if r["h2_idx"] >= 0 else None,
                      "kirilim": r["kirilim_idx"] - r["t_idx"] if r["kirilim_idx"] >= 0 else None,
                      "pivot_dip": [j - r["t_idx"] for j in r["pivot_dipler"]], "pivot_dip_atr": [round(x, 2) for x in r["pivot_dip_atr"]],
                      "esit": cik == s["beklenen"]})
    bozuk = [x["seri"] for x in tablo if not x["esit"]]
    if bozuk:
        raise AssertionError(f"sentetik seriler beklenenden farklı: {bozuk}: " + json.dumps([x for x in tablo if not x["esit"]], ensure_ascii=False))
    T = {x["seri"]: x for x in tablo}
    # parça düzeyi: S2'de yeni dip sonrası dönüş dibi yok (P3(ii)); S4'te P3(ii) yapışık; S6 / S7 P3(i); S8 P2; S9 P3(iii); S3 P2
    assert not T["S2"]["P3ii"] and T["S2"]["P3i"] and T["S2"]["d"] == -20
    assert not T["S3"]["P2"] and T["S3"]["P3i"] and T["S3"]["P3ii"] and T["S3"]["P3iii"]
    assert T["S4"]["P2"] and not T["S4"]["P3ii"] and T["S4"]["pivot_dip"], T["S4"]
    assert not T["S5"]["P1"]
    assert not T["S6"]["P3i"] and T["S6"]["d"] == -5
    assert not T["S7"]["P3i"] and T["S7"]["d"] == -40
    assert T["S8"]["h1"] is None and not T["S8"]["P2"]
    assert T["S9"]["P3ii"] and not T["S9"]["P3iii"]
    assert T["S1"]["d"] == -40 and T["S1"]["h1"] == 8 - 120 and T["S1"]["h2"] == 66 - 120 and T["S1"]["pivot_dip"] == [-20]
    # eşit en düşük Low: EN SON gün
    O, H, L, C = ds4_sentetik()["S1"]["seri"]; O, H, L, C = O.copy(), H.copy(), L.copy(), C.copy(); L[100] = L[80]
    r = ds4_parca_dizi(O, H, L, C); assert r["d_idx"] == 100, r["d_idx"]
    # prefix değişmezliği: t sonrası veri değişince sonuç aynı (dizi ve DataFrame)
    rng = np.random.default_rng(11); n = 260
    Cx = 100 + np.cumsum(rng.normal(0, 1, n)); Ox = Cx + rng.normal(0, .3, n)
    Hx = np.maximum(Ox, Cx) + abs(rng.normal(0, .5, n)) + .1; Lx = np.minimum(Ox, Cx) - abs(rng.normal(0, .5, n)) - .1
    Cx, Ox, Hx, Lx = (a - min(Lx.min(), 0) + 5 for a in (Cx, Ox, Hx, Lx))
    for i in (150, 200, 230):
        s = slice(i - 120, i + 1)
        x1 = ds4_parca_dizi(Ox[s], Hx[s], Lx[s], Cx[s])
        O2, H2, L2, C2 = Ox.copy(), Hx.copy(), Lx.copy(), Cx.copy()
        O2[i + 1:] = 1; H2[i + 1:] = 2; L2[i + 1:] = 0.5; C2[i + 1:] = 1.5
        x2 = ds4_parca_dizi(O2[s], H2[s], L2[s], C2[s])
        assert json.dumps(x1, sort_keys=True) == json.dumps(x2, sort_keys=True), "DS4 t sonrasına bağlı"
    idx = pd.bdate_range("2020-01-01", periods=n)
    D1 = pd.DataFrame({"Open": Ox, "High": Hx, "Low": Lx, "Close": Cx}, index=idx)
    D2 = D1.copy(); D2.iloc[201:] = [1.0, 2.0, 0.5, 1.5]
    t = idx[200]
    y1 = ds4_parca(D1[D1.index <= t].iloc[-121:]); y2 = ds4_parca(D2[D2.index <= t].iloc[-121:])
    assert json.dumps(y1, sort_keys=True) == json.dumps(y2, sort_keys=True), "prefix (DataFrame) değişmezliği bozuk"
    # pencere boyu ve geçersiz bar denetimi
    for bozuk_ in ((Ox[:100], Hx[:100], Lx[:100], Cx[:100]), (Ox[:121], Lx[:121], Hx[:121], Cx[:121])):
        try:
            ds4_parca_dizi(*bozuk_); raise AssertionError("bozuk pencere kabul edildi")
        except DS4Hata:
            pass
    # hüküm
    assert ds4_hukum(0.7, 0.45, 79) == "YARI BAĞIMSIZ GEÇERLİ" and ds4_hukum(0.7, 0.3, 79) == "KISMEN"
    assert ds4_hukum(0.5, 0.2, 79) == "KISMEN" and ds4_hukum(0.3, 0.1, 79) == "GEÇERSİZ" and ds4_hukum(0.9, 0.8, 20).startswith("ÖLÇÜLEMEDİ")
    a = np.array([1, 1, 0, 0] * 10, bool)
    assert abs(GU.gu_kappa(a, a) - 1) < 1e-12
    return {"tamam": True, "kural_sha": _kural_sha4(), "esik_sha": _sha_esik4(), "tablo": tablo}


# ================================================================ 5) MÜHÜR
DS4_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralın uyumu, kappa)"),
    "K2": ("EVET", "P1 / P2 / P3 yalnız kör sayfa penceresinden: tanim2.tz_pencere = goz_uyum._gu_pencere (veri t'de KESİK, 121 bar) + ds4_pencere "
                   "mekanik denetimi (W.index.max() <= t, W.index[-1] == t, 121 bar); pivot tepe j+5 <= d, pivot dip j+3 <= t (yalnız t'ye kadar "
                   "onaylı); ds4.py test prefix değişmezliği (3 kesik + DataFrame); getiri / sinyal sonrası fiyat okunmaz; Cemal'in işaretleri "
                   "mühürden önce açılmadı (olc açılış zamanı DS4_SONUC'ta)"),
    "K3": ("EVET", "GE.ge_hazir (H>L, V>0, O/H/L/C>0) geçerli bar (goz_uyum ile aynı); ds4_parca_dizi NaN / H <= L / L <= 0 görürse durur (testte sınandı)"),
    "K4": ("EVET", "80 sayfa set 1 (goz_uyum_anahtar) + set 2 (tanim2_anahtar) ile aynı: aynı hissede en çok 1 sayfa; görsel onay 24 sayfası iki "
                   "setin (pazar, sembol) çiftleri hariç, her çift en çok 1 sayfa"),
    "K5": ("UYGULANMAZ", "giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik"),
    "K6": ("EVET", "tek kip V_*.pkl (goz_uyum ile aynı); düşüş oranı birimsiz, bant ve dönüş dibi uzaklığı ATR14(d) birimi; fiyat birimi kuralı etkilemez"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok"),
    "K8": ("EVET", "79-80 karar (iki set); karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); 3 varyant: Bonferroni 3 (%98,33) V2 / V3 için; "
                   "hüküm yalnız V1 ve 'YARI BAĞIMSIZ' (Cemal tarifi DS3 görselindeki 6 set-1 sayfasını görerek verdi); set 1 ve set 2 ayrı; "
                   "kural etiketlerden SEÇİLMEDİ (Ç211 ezber dersi)"),
    "K9": ("EVET", "kural + DS4_ESIK + sentetik test ADIM 1'de etiketler açılmadan commit; 80 yanıt ds4_anahtar.json + görsel onay (DS4_ONAY.pdf, "
                   "ds4_onay_anahtar.json) etiket açılmadan mühürlü; ds4.py + ds4_anahtar.json + DS4_ESIK + kural kaynağı + PDF + onay anahtarı "
                   "sha'ları bu dosyada; olc sha'ları denetler ve 80 yanıtı veriden yeniden hesaplayıp mühürle karşılaştırır; hüküm eşikleri sabit"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırma yok; yalnız OHLCV"),
    "K11": ("EVET", "ds4.py anahtar / onay aynı komutla deterministik yeniden üretilir (tohum 20261125); olc 80 sayfanın yanıtını veriden yeniden "
                    "hesaplar, mühürlü yanıtla eşitliğini şart koşar; sentetik seriler beklenen yanıtla birebir (9 / 9)"),
    "K12": ("EVET", "iddia yok; yalnız 'uyum' ve 'kappa' sayısı; hüküm sözü yalnız ön kayıttaki eşikle ve yalnız V1 için; 'YARI BAĞIMSIZ' sınırı yazılı"),
    "K13": ("EVET", "çakışma kapısı _CK_ONCE_DS4 + test; yasak dosyalar (defter, mevcut .py, anahtar / ön kayıt / sonuç dosyaları) değişmedi "
                    "(git diff boş); e-posta / anahtar yok (_yaz / _jyaz e-posta taraması); git add -A yok; PDF Cemal'e gönderilmedi"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


def ds4_muhur() -> str:
    for y in (DS4_YOL["anahtar"], DS4_YOL["is_tanimi"], DS4_YOL["pdf"], DS4_YOL["onay_anahtar"]):
        if not os.path.exists(y):
            raise DS4Hata(f"mühür için dosya yok: {y}")
    J = json.load(open(DS4_YOL["anahtar"], encoding="utf-8")); JO = json.load(open(DS4_YOL["onay_anahtar"], encoding="utf-8"))
    for ad, X in (("anahtar", J), ("onay", JO)):
        if X["esik_sha"] != _sha_esik4():
            raise DS4Hata(f"DS4_ESIK {ad} dosyasından sonra değişmiş")
        if X["kural_sha"] != _kural_sha4():
            raise DS4Hata(f"kural kaynağı {ad} dosyasından sonra değişmiş")
    if JO["pdf_sha"] != GU._sha(DS4_YOL["pdf"]):
        raise DS4Hata("DS4_ONAY.pdf onay anahtarından sonra değişmiş")
    T = ds4_test()
    ad = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
          "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
          "K13": "süreç", "K14": "boyut (gerçek para)"}
    tab = "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |\n|---|---|---|---|\n"
    for k, (yy, kn) in DS4_KONTROL.items():
        tab += f"| {k} | {ad[k]} | {yy} | {kn} |\n"
    st = ["| seri | tarif | beklenen V1 / V2 / V3 | çıkan V1 / V2 / V3 | P1 | P2 | P3(i) | P3(ii) | P3(iii) | d | H1 | H2 | kırılım | dönüş dipleri (ATR) | eşit |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in T["tablo"]:
        b = " / ".join(x["beklenen"][v] for v in ("V1", "V2", "V3")); c = " / ".join(x["cikan"][v] for v in ("V1", "V2", "V3"))
        pdx = ", ".join(f"t{j:+d} ({a:.2f})" for j, a in zip(x["pivot_dip"], x["pivot_dip_atr"])) or "-"
        st.append(f"| {x['seri']} | {x['tarif']} | {b} | {c} | {_isr(x['P1'])} | {_isr(x['P2'])} | {_isr(x['P3i'])} | {_isr(x['P3ii'])} | "
                  f"{_isr(x['P3iii'])} | t{x['d']:+d} | {('t%+d' % x['h1']) if x['h1'] is not None else '-'} | "
                  f"{('t%+d' % x['h2']) if x['h2'] is not None else '-'} | {('t%+d' % x['kirilim']) if x['kirilim'] is not None else '-'} | "
                  f"{pdx} | {'EVET' if x['esit'] else 'HAYIR'} |")
    oz = J["ozet"]
    ot = ["| küme | n | P1 | P2 | P3(i) | P3(ii) | P3(iii) | P3 | V1 VAR | V2 VAR | V3 VAR |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k_, o in oz.items():
        ot.append(f"| {k_} | {o['n']} | {o['P1_DOGRU']} | {o['P2_DOGRU']} | {o['P3i_DOGRU']} | {o['P3ii_DOGRU']} | {o['P3iii_DOGRU']} | "
                  f"{o['P3_DOGRU']} | {o['V1_VAR']} | {o['V2_VAR']} | {o['V3_VAR']} |")
    on = ["| sayfa | grup (seçim) | V1 | P1 | P2 | P3 | düşen parça |", "|---|---|---|---|---|---|---|"]
    for s in JO["sayfalar"]:
        on.append(f"| {s['sayfa']} | {s['grup']} | {s['yanit']['V1']} | {_isr(s['P1'])} | {_isr(s['P2'])} | {_isr(s['P3'])} | "
                  f"{', '.join(s['V1_dusen']) or '-'} |")
    bel = "\n".join(f"- {k}: {v}" for k, v in DS4_ESIK["belirsizlik"].items())
    m = f"""# DİP SAVUNMASI v4 (DS4) — ÖN KAYIT (Cemal'in işaretleri AÇILMADAN mühürlenir)

Üretim: {GU._simdi()} (UTC). Soru: Cemal'in 23.11.2026 tarifi ("Burada kodun yanlışını buldum: en dip noktasında çizgi çekip bir düşeni kırmış mı, ve artık düşmüyor, yukarı daha yukarıdan dönüyorsa VAR.") üç parçalı kurala çevrilince, iki kör sette (GOZ_UYUM_KOR.pdf = set 1, TANIM2_KOR.pdf = set 2; 80 sayfa) Cemal'in VAR / YOK işaretleriyle örtüşüyor mu? Ayrıca iki set dışından 24 sayfalık GÖRSEL ONAY (EK, 23 Kas) PDF'i (Cemal'e henüz gönderilmedi). GETİRİ ÖLÇÜLMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/ds4_anahtar.json` sha256: `{GU._sha(DS4_YOL['anahtar'])}`
- kod: `arastirma_cikti/goz_uyum/ds4.py` sha256: `{GU._sha(DS4_YOL['kod'])}`
- eşik sözlüğü (DS4_ESIK) sha256: `{_sha_esik4()}`
- kural kaynağı (ds4_parca_dizi + ds4_parca) sha256: `{_kural_sha4()}`
- görsel onay PDF: `arastirma_cikti/goz_uyum/DS4_ONAY.pdf` sha256: `{GU._sha(DS4_YOL['pdf'])}`
- görsel onay anahtarı: `arastirma_cikti/goz_uyum/ds4_onay_anahtar.json` sha256: `{GU._sha(DS4_YOL['onay_anahtar'])}`
- iş tanımı: `arastirma_cikti/goz_uyum/DS4_IS_TANIMI.md` sha256: `{GU._sha(DS4_YOL['is_tanimi'])}`
- girdi (yalnız sayfa -> pazar, sembol, sinyal günü okundu): goz_uyum_anahtar.json `{J['girdi_sha']['goz_uyum_anahtar.json']}`, tanim2_anahtar.json `{J['girdi_sha']['tanim2_anahtar.json']}`
- olay havuzu (görsel onay; pazar, sembol, tarih) sha256: `{JO['havuz_sha']}` ({json.dumps(JO['havuz'], ensure_ascii=False)})
- bağımlı kod: goz_uyum.py `{GU._sha(GU.GU_YOL['kod'])[:16]}`, tanim2.py `{GU._sha(TZ.TZ_YOL['kod'])[:16]}`, GOZ_ETIKET.py `{GU._sha(os.path.join(KOK4, 'GOZ_ETIKET.py'))[:16]}`

## 2. Kural (ADIM 1'de, etiketler açılmadan commit; parametreler iş tanımından aynen)
Pencere: kör sayfa penceresi (121 geçerli bar, veri sinyal günü t'de kesik); kural penceresi son 120 mum [t-119 .. t].
- **DİP**: d = [t-119 .. t-5] aralığında en düşük Low'un günü (eşitlikte en son); dip çizgisi = Low(d).
- **P1 DÜŞÜŞTEN DİP**: d'den önceki pencere kısmında en yüksek High / Low(d) - 1 >= 0,20.
- **P2 DÜŞEN TREND KIRILIMI**: d'den önceki pivot tepeler (High, 5 sol / 5 sağ; pivot günü + 5 <= d). H1 = en yüksek pivot tepe; H2 = H1'den sonra, H1'den alçak SON pivot tepe (yoksa H1'den sonraki en yüksek pivot tepe; o da yoksa P2 YOK). Düşen çizgi = H1-H2 doğrusu (eğim < 0 şart). Kırılım = d'den sonra en az bir mumun KAPANIŞI çizginin o gündeki değerinin üstünde.
- **P3 ARTIK DÜŞMÜYOR, DAHA YUKARIDAN DÖNÜYOR**: (i) d'den sonra hiçbir Low < Low(d); (ii) d'den sonra en az bir pivot dip (Low, 3 sol / 3 sağ; pivot günü + 3 <= t) var ve HEPSİ Low(d) + 0,5 x ATR14(d) üstünde; (iii) birden çok pivot dip varsa son pivot dip ilkinden düşük değil.
- **V1 (ANA)** = P1 ∧ P2 ∧ P3; **V2** = P1 ∧ P3 (trend kırılımı yok); **V3** = P1 ∧ P2 ∧ P3(i) (yükselen dip yok). Bonferroni 3.

Tanım belirsizliklerinin çözümü (etiketlerden önce yazıldı):
{bel}

DS4_ESIK (tam): `{json.dumps(DS4_ESIK, ensure_ascii=False, sort_keys=True)}`

## 3. Sentetik sınama (`python arastirma_cikti/goz_uyum/ds4.py test`; kör / gerçek veriden ÖNCE; dizinler t'ye göre)
{chr(10).join(st)}

Ek testler: eşit en düşük Low -> en son gün; prefix değişmezliği (3 kesik, dizi + DataFrame); kısa pencere ve H <= L penceresi reddedilir; hüküm fonksiyonu. Sonuç: {sum(x['esit'] for x in T['tablo'])} / {len(T['tablo'])} seri beklenene eşit.

## 4. Mühürlü yanıtlar (ds4_anahtar.json 'sayfalar'; Cemal'in işaretleri AÇILMADAN yazıldı)
{chr(10).join(ot)}

## 5. Görsel onay PDF'i (DS4_ONAY.pdf; iki set dışından 24 yeni sayfa; anahtar ds4_onay_anahtar.json)
Seçim: {DS4_ESIK['onay']['secim']}.

{chr(10).join(on)}

## 6. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in set 1 (cemal_isaret.json) ve set 2 (cemal_isaret2.json) VAR / YOK işaretleri ile V1 / V2 / V3 arasında uyum ve Cohen kappa; set 1, set 2 ve birleşik; işaretsiz / '?' sayfa karar dışı, sayısı ayrıca yazılır.
- Aralık: kappa bootstrap (B {DS4_ESIK['kappa']['B']}, tohum {DS4_ESIK['kappa']['tohum']}, sayfa yeniden örneklemesi, yüzdelik): V1 için %95; V2 / V3 için Bonferroni 3 ile %98,33 (ayrıca %95 bilgi).
- HÜKÜM: {DS4_ESIK['hukum']}.
- Ek bilgi (hüküm dışı): uyuşmayan sayfalar ve düşen parça (P1 / P2 / P3(i) / P3(ii) / P3(iii)); Cemal VAR / kod YOK sayfalarda düşen parça sayımı; GOVDE_1 (önceki birleşik kappa 0,35) ve DS3 V1 (-0,15) ile aynı sayfalarda karşılaştırma.
- Kural ve eşik sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 7. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
{tab}
## 8. Git kaydı (bu dosyanın yazıldığı an)
- ds4.py: {GU._gu_git('arastirma_cikti/goz_uyum/ds4.py')}
- DS4_IS_TANIMI.md: {GU._gu_git('arastirma_cikti/goz_uyum/DS4_IS_TANIMI.md')}
"""
    GU._yaz(DS4_YOL["onkayit"], m)
    import IZ_KARNE as IK
    r = IK.ik_kontrol_kapisi(DS4_YOL["onkayit"])
    d4log.info("kontrol kapısı: %s", "GEÇTİ" if r["gecti"] else r)
    return DS4_YOL["onkayit"]


def _ds4_muhur_oku() -> Dict[str, str]:
    if not os.path.exists(DS4_YOL["onkayit"]):
        raise DS4Hata("ön kayıt yok")
    t = open(DS4_YOL["onkayit"], encoding="utf-8").read(); out = {}
    for ad, desen in (("anahtar", r"ds4_anahtar\.json` sha256: `([0-9a-f]{64})`"), ("kod", r"ds4\.py` sha256: `([0-9a-f]{64})`"),
                      ("esik", r"eşik sözlüğü \(DS4_ESIK\) sha256: `([0-9a-f]{64})`"), ("kural", r"kural kaynağı \([^)]*\) sha256: `([0-9a-f]{64})`"),
                      ("pdf", r"DS4_ONAY\.pdf` sha256: `([0-9a-f]{64})`"), ("onay", r"ds4_onay_anahtar\.json` sha256: `([0-9a-f]{64})`")):
        m = re.search(desen, t)
        if not m:
            raise DS4Hata(f"ön kayıtta {ad} sha'sı yok")
        out[ad] = m.group(1)
    return out


# ================================================================ 6) ÖLÇÜM
def _boot4(a: np.ndarray, b: np.ndarray, B: int, tohum: int, guven: Tuple[float, ...]) -> Dict[str, Any]:
    rng = np.random.default_rng(tohum); n = len(a); ks = np.empty(B)
    for i in range(B):
        j = rng.integers(0, n, n); ks[i] = GU.gu_kappa(a[j], b[j])
    g = ks[np.isfinite(ks)]; out: Dict[str, Any] = {"gecersiz": int(B - len(g))}
    for gv in guven:
        al = (1 - gv) / 2 * 100
        out[f"{gv:.4f}"] = [float(np.percentile(g, al)), float(np.percentile(g, 100 - al))] if len(g) else [np.nan, np.nan]
    return out


def ds4_hukum(k: float, alt: float, n: int) -> str:
    E = DS4_ESIK["kappa"]
    if n < int(E["karar_min"]) or not np.isfinite(k):
        return "ÖLÇÜLEMEDİ (karar sayısı < 30 ya da kappa tanımsız)"
    if k >= E["gecerli"] and np.isfinite(alt) and alt >= E["gecerli_alt"]:
        return "YARI BAĞIMSIZ GEÇERLİ"
    return "KISMEN" if k >= E["kismen"] else "GEÇERSİZ"


def _etiket_oku4(yol: str) -> Dict[int, str]:
    C = json.load(open(yol, encoding="utf-8"))
    atla = [k for k in C if not str(k).strip().isdigit()]
    if atla:
        d4log.warning("etiket dosyasında sayfa olmayan anahtar(lar) atlandı: %s", atla)
    return {int(k): (GU.gu_norm(v) or "?") for k, v in C.items() if str(k).strip().isdigit()}


def _govde1_cevap(R: pd.DataFrame, kural: Dict[str, Any]) -> np.ndarray:
    import govde as GV                                                   # yalnız okunur (özellik + kural)
    out = []
    for r in R.itertuples(index=False):
        W = ds4_pencere(r.pazar, r.sembol, r.sinyal_gunu)
        x = GV.gv_ozellik(W)[kural["ozellik"]]
        out.append(bool(GV.gv_kural(np.array([x], float), kural["yon"], float(kural["esik"]))[0]))
    return np.array(out, bool)


def ds4_olc(deneme: bool = False, cemal1: Optional[str] = None, cemal2: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    if not deneme:
        M = _ds4_muhur_oku()
        for ad, gercek in (("anahtar", GU._sha(DS4_YOL["anahtar"])), ("kod", GU._sha(DS4_YOL["kod"])), ("esik", _sha_esik4()),
                           ("kural", _kural_sha4()), ("pdf", GU._sha(DS4_YOL["pdf"])), ("onay", GU._sha(DS4_YOL["onay_anahtar"]))):
            if gercek != M[ad]:
                raise DS4Hata(f"MÜHÜR BOZUK: {ad} sha'sı ön kayıttakiyle aynı değil -> DURDU")
    J = json.load(open(DS4_YOL["anahtar"], encoding="utf-8"))
    Sm = pd.DataFrame(J["sayfalar"])
    # K11: yanıtlar veriden yeniden hesaplanır ve mühürle eşit olmalı
    R = ds4_hesap(Sm[["set", "sayfa", "pazar", "sembol", "sinyal_gunu"]])
    for v in ("V1", "V2", "V3", "P1", "P2", "P3i", "P3ii", "P3iii"):
        if (R[v].to_numpy(bool) != Sm[v].to_numpy(bool)).any():
            raise DS4Hata(f"{v} yanıtları veriden yeniden hesaplanınca mühürle aynı değil -> DURDU")
    acilis = GU._simdi()
    c1 = cemal1 or DS4_YOL["set1_cemal"]; c2 = cemal2 or DS4_YOL["set2_cemal"]
    et = {1: _etiket_oku4(c1), 2: _etiket_oku4(c2)}
    d4log.info("etiket dosyaları açıldı: %s (UTC)", acilis)
    for st in (1, 2):
        fazla = sorted(set(et[st]) - set(range(1, 41)))
        if fazla:
            raise DS4Hata(f"set {st} etiketinde anahtarda olmayan sayfa: {fazla}")
    Sm["cemal"] = [et[int(s)].get(int(p), "?") for s, p in zip(Sm.set, Sm.sayfa)]
    E = DS4_ESIK["kappa"]; bon = 1 - (1 - E["guven"]) / E["bonferroni_k"]
    # karşılaştırma: GOVDE_1 ve DS3 V1 (aynı sayfalar)
    if deneme:
        g1k = {"ozellik": "G1_govde_dokunus_n", "yon": ">=", "esik": 3.0, "not": "DENEME: uydurma kural"}
        ds3_v1 = {(int(s), int(p)): False for s, p in zip(Sm.set, Sm.sayfa)}
    else:
        GJ = json.load(open(DS4_YOL["govde_anahtar"], encoding="utf-8")); g1k = dict(GJ["kurallar"]["GOVDE_1"]); del GJ
        D3 = json.load(open(DS4_YOL["ds3_anahtar"], encoding="utf-8"))
        ds3_v1 = {(int(s["set"]), int(s["sayfa"])): bool(s["V1"]) for s in D3["sayfalar"]}; del D3
    Sm["GOVDE_1"] = _govde1_cevap(Sm, g1k)
    Sm["DS3_V1"] = [ds3_v1[(int(s), int(p))] for s, p in zip(Sm.set, Sm.sayfa)]
    kumeler = {"set 1": Sm.set == 1, "set 2": Sm.set == 2, "birleşik": Sm.set > 0}
    sonuc: Dict[str, Any] = {"etiket_acilis_utc": acilis, "deneme": deneme, "n_sayfa": int(len(Sm)), "kume": {}, "govde_kural": g1k}
    for kad, km in kumeler.items():
        K = Sm[km & (Sm.cemal != "?")]; cb = (K.cemal == "VAR").to_numpy(bool); n = len(K)
        kd: Dict[str, Any] = {"karar_n": int(n), "isaretsiz": int((km & (Sm.cemal == "?")).sum()),
                              "isaretsiz_sayfa": [f"set {s} / {p}" for s, p in zip(Sm[km & (Sm.cemal == '?')].set, Sm[km & (Sm.cemal == '?')].sayfa)],
                              "cemal_VAR": int(cb.sum()), "model": {}}
        for v in ("V1", "V2", "V3", "GOVDE_1", "DS3_V1"):
            mod = K[v].to_numpy(bool)
            k = GU.gu_kappa(cb, mod)
            ar = _boot4(cb, mod, int(E["B"]), int(E["tohum"]), (E["guven"], bon)) if n else {}
            tp, tn = int((cb & mod).sum()), int((~cb & ~mod).sum()); fp, fn = int((~cb & mod).sum()), int((cb & ~mod).sum())
            a95 = ar.get(f"{E['guven']:.4f}", [np.nan, np.nan]); abn = ar.get(f"{bon:.4f}", [np.nan, np.nan])
            huk = (ds4_hukum(k, a95[0], n) if v == "V1" else
                   ("BİLGİ (Bonferroni alt uç ile: " + ds4_hukum(k, abn[0], n) + ")" if v in ("V2", "V3") else "BİLGİ (önceki kural)"))
            kd["model"][v] = {"kod_VAR": int(mod.sum()), "uyum": float(np.mean(cb == mod)) if n else np.nan, "kappa": k, "ar95": a95,
                              "ar_bon": abn, "hukum": huk,
                              "tablo": {"Cemal VAR + kod VAR": tp, "Cemal YOK + kod YOK": tn, "Cemal YOK + kod VAR": fp, "Cemal VAR + kod YOK": fn},
                              "uyusmayan": [f"set {s} / {p}" for s, p in zip(K.set[cb != mod], K.sayfa[cb != mod])]}
        sonuc["kume"][kad] = kd
    # Cemal VAR / kod YOK: düşen parça sayımı
    parcalar = {"P1": "P1", "P2": "P2", "P3i": "P3(i)", "P3ii": "P3(ii)", "P3iii": "P3(iii)"}
    say: Dict[str, Any] = {}
    for v, pl in (("V1", ["P1", "P2", "P3i", "P3ii", "P3iii"]), ("V2", ["P1", "P3i", "P3ii", "P3iii"]), ("V3", ["P1", "P2", "P3i"])):
        X = Sm[(Sm.cemal == "VAR") & (~Sm[v].astype(bool))]
        dus = {parcalar[p]: int((~X[p].astype(bool)).sum()) for p in pl}
        tek = {parcalar[p]: int(((~X[p].astype(bool)) & (X[[q for q in pl if q != p]].astype(bool).all(axis=1))).sum()) for p in pl}
        say[v] = {"n": int(len(X)), "dusen": dus, "yalniz_bu_dusen": tek}
    X = Sm[(Sm.cemal == "YOK") & (Sm.V1.astype(bool))]
    say["V1_cemal_YOK_kod_VAR"] = {"n": int(len(X)), "sayfa": [f"set {s} / {p}" for s, p in zip(X.set, X.sayfa)]}
    sonuc["cemal_VAR_kod_YOK_parca"] = say
    uy = []
    for _, r in Sm.iterrows():
        if r.cemal == "?" or (r.cemal == "VAR") == bool(r.V1):
            continue
        rd = r.to_dict()
        uy.append({"sayfa": f"set {r.set} / {r.sayfa}", "cemal": r.cemal, "V1": "VAR" if r.V1 else "YOK", "V2": "VAR" if r.V2 else "YOK",
                   "V3": "VAR" if r.V3 else "YOK", "GOVDE_1": "VAR" if r.GOVDE_1 else "YOK", "DS3_V1": "VAR" if r.DS3_V1 else "YOK",
                   "m": int(r.m), "dusus": float(r.dusus), "P1": bool(r.P1), "P2": bool(r.P2), "P3i": bool(r.P3i), "P3ii": bool(r.P3ii),
                   "P3iii": bool(r.P3iii), "dusen": ds4_dusen(rd), "neden": ds4_neden_metni(rd), "kirilim_m": (int(r.kirilim_idx) - int(r.t_idx))
                   if int(r.kirilim_idx) >= 0 else None, "pivot_dip_atr": [round(float(x), 2) for x in r.pivot_dip_atr]})
    sonuc["V1_uyusmayan"] = uy
    K = Sm[Sm.cemal != "?"]; cv = (K.cemal == "VAR")
    sonuc["karsilastirma"] = {f"V1_{o}": {"iki_kod_ayni_yanit": int((K.V1.astype(bool) == K[o].astype(bool)).sum()), "karar_n": int(len(K)),
                                          "kod_kappa": GU.gu_kappa(K.V1.to_numpy(bool), K[o].to_numpy(bool)),
                                          "V1_dogru_oteki_yanlis": int(((K.V1.astype(bool) == cv) & (K[o].astype(bool) != cv)).sum()),
                                          "oteki_dogru_V1_yanlis": int(((K.V1.astype(bool) != cv) & (K[o].astype(bool) == cv)).sum())}
                              for o in ("GOVDE_1", "DS3_V1")}
    sonuc["sayfa_cemal"] = {f"{s}/{p}": c for s, p, c in zip(Sm.set, Sm.sayfa, Sm.cemal)}
    md = _sonuc_md4(sonuc)
    hedef = cikti or DS4_DIR
    os.makedirs(hedef, exist_ok=True)
    GU._yaz(os.path.join(hedef, "DS4_SONUC.md"), md)
    GU._jyaz(os.path.join(hedef, "ds4_sonuc.json"), sonuc)
    return sonuc


def _sonuc_md4(S: Dict[str, Any]) -> str:
    B = S["kume"]["birleşik"]; v1 = B["model"]["V1"]
    L = [("# [DENEME — UYDURMA ETİKET] " if S["deneme"] else "# ") + "DİP SAVUNMASI v4 (DS4) — SONUÇ (iki kör set, 80 sayfa)", "",
         (f"Üretim: {GU._simdi()} (UTC). DENEME: uydurma etiket dosyaları; mühür denetimi YAPILMADI; 80 yanıt veriden yeniden hesaplandı, "
          "anahtarla aynı. GETİRİ YOK." if S["deneme"] else
          f"Üretim: {GU._simdi()} (UTC). Etiket dosyaları (cemal_isaret.json, cemal_isaret2.json) bu komutla açıldı: {S['etiket_acilis_utc']} (UTC). "
          "Mühür denetimi: ds4_anahtar.json, ds4.py, DS4_ESIK, kural kaynağı, DS4_ONAY.pdf ve ds4_onay_anahtar.json sha'ları DS4_ON_KAYIT ile aynı; "
          "80 sayfanın P1 / P2 / P3 ve V1 / V2 / V3 yanıtı veriden yeniden hesaplandı, mühürle aynı. GETİRİ YOK."), "",
         f"Karar: birleşik {B['karar_n']} (Cemal VAR {B['cemal_VAR']}); işaretsiz / '?' (karar dışı): {B['isaretsiz']} {B['isaretsiz_sayfa']}.", "",
         f"## HÜKÜM (V1, ön kayıttaki eşikle): **{v1['hukum']}** — birleşik kappa {_f4(v1['kappa'])}, %95 [{_f4(v1['ar95'][0])}, {_f4(v1['ar95'][1])}]",
         "", "Sınır: Cemal tarifini DS3 görselindeki 6 set-1 sayfasını görerek verdi; bu yüzden sonuç YARI BAĞIMSIZDIR. Kesin hüküm yalnız Cemal'in "
         "görsel onayı (DS4_ONAY.pdf) + üçüncü bağımsız kör setle.", ""]
    s1 = S["kume"]["set 1"]["model"]["V1"]["kappa"]; s2 = S["kume"]["set 2"]["model"]["V1"]["kappa"]
    dus1 = bool(np.isfinite(s1) and s1 < 0.40); dus2 = bool(np.isfinite(s2) and s2 < 0.40)
    if dus1 and dus2:
        L += [f"NOT: V1 kappa set 1 {_f4(s1)}, set 2 {_f4(s2)}: İKİ SETTE DE < 0,40.", ""]
    elif dus1 or dus2:
        L += [f"NOT: **tutarsız** — V1 kappa set 1 {_f4(s1)}, set 2 {_f4(s2)}; biri < 0,40.", ""]
    L += ["## Kappa tablosu", "", "| model | küme | karar | kod VAR | uyum | kappa | %95 aralık | %98,33 (Bonferroni 3) | hüküm |",
          "|---|---|---|---|---|---|---|---|---|"]
    for v in ("V1", "V2", "V3", "GOVDE_1", "DS3_V1"):
        for kad in ("set 1", "set 2", "birleşik"):
            r = S["kume"][kad]["model"][v]; kd = S["kume"][kad]
            huk = r["hukum"] if kad == "birleşik" else ("ayrı rapor" if v == "V1" else "bilgi")
            L.append(f"| {v} | {kad} | {kd['karar_n']} | {r['kod_VAR']} | {_f4(r['uyum'])} | {_f4(r['kappa'])} | [{_f4(r['ar95'][0])}, "
                     f"{_f4(r['ar95'][1])}] | [{_f4(r['ar_bon'][0])}, {_f4(r['ar_bon'][1])}] | {huk} |")
    L += ["", f"V1 = P1 ∧ P2 ∧ P3 (ANA); V2 = P1 ∧ P3; V3 = P1 ∧ P2 ∧ P3(i). GOVDE_1 = {S['govde_kural'].get('ozellik')} {S['govde_kural'].get('yon')} "
          f"{S['govde_kural'].get('esik')!r} (eşiği set 1 etiketleriyle seçildi -> set 1'de iç-örneklem); DS3_V1 = ds3_anahtar.json mühürlü V1.", "",
          f"HÜKÜM kuralı (ön kayıt): {DS4_ESIK['hukum']}.", "", "## 2x2", ""]
    for v in ("V1", "V2", "V3"):
        L += [f"**{v} birleşik**: " + "; ".join(f"{k} {x}" for k, x in B["model"][v]["tablo"].items()), ""]
    for kad in ("set 1", "set 2"):
        L += [f"**V1 {kad}**: " + "; ".join(f"{k} {x}" for k, x in S["kume"][kad]["model"]["V1"]["tablo"].items()), ""]
    P = S["cemal_VAR_kod_YOK_parca"]
    L += ["## Cemal VAR dediği halde kodun YOK dediği sayfalarda düşen parça", "",
          "| varyant | sayfa | düşen parça sayımı (bir sayfada birden çok olabilir) | yalnız bu parça düştü |", "|---|---|---|---|"]
    for v in ("V1", "V2", "V3"):
        x = P[v]
        L.append(f"| {v} | {x['n']} | " + "; ".join(f"{k} {c}" for k, c in x["dusen"].items()) + " | " +
                 "; ".join(f"{k} {c}" for k, c in x["yalniz_bu_dusen"].items()) + " |")
    L += ["", f"Cemal YOK / kod V1 VAR: {P['V1_cemal_YOK_kod_VAR']['n']} sayfa {P['V1_cemal_YOK_kod_VAR']['sayfa']}.", "",
          "## V1 uyuşmayan sayfalar", "",
          "| sayfa | Cemal | V1 | V2 | V3 | GOVDE_1 | DS3_V1 | dip yaşı (mum) | düşüş | kırılım (t'ye göre) | dönüş dipleri (ATR) | düşen parça | kodun gördüğü |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in S["V1_uyusmayan"]:
        ne = "; ".join(r["neden"]) if r["neden"] else "üç parça da DOĞRU (kod VAR)"
        L.append(f"| {r['sayfa']} | {r['cemal']} | {r['V1']} | {r['V2']} | {r['V3']} | {r['GOVDE_1']} | {r['DS3_V1']} | {r['m']} | "
                 f"%{r['dusus']*100:.0f} | {('t%+d' % r['kirilim_m']) if r['kirilim_m'] is not None else '-'} | "
                 f"{', '.join(_f4(x, 2) for x in r['pivot_dip_atr']) or '-'} | {', '.join(r['dusen']) or '-'} | {ne} |")
    L += ["", "## Karşılaştırma: aynı sayfalarda önceki kurallar", ""]
    for o, G in S["karsilastirma"].items():
        L.append(f"- {o}: karar {G['karar_n']} sayfada iki kod {G['iki_kod_ayni_yanit']} sayfada aynı yanıt (kodlar arası kappa {_f4(G['kod_kappa'])}); "
                 f"V1 doğru / öteki yanlış {G['V1_dogru_oteki_yanlis']}; öteki doğru / V1 yanlış {G['oteki_dogru_V1_yanlis']}.")
    L += ["", "Not: uyum Cemal'in gözüyle uyumdur; getiri ölçülmedi. Kural Cemal'in tarifinden etiketlere bakmadan sabitlendi ve önce sentetik "
          "serilerde sınandı (DS3 dersi)."]
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
    if a.deneme and ({os.path.realpath(a.cemal1), os.path.realpath(a.cemal2)} & {os.path.realpath(DS4_YOL["set1_cemal"]),
                                                                                os.path.realpath(DS4_YOL["set2_cemal"])}
                     or os.path.realpath(a.cikti) == os.path.realpath(DS4_DIR)):
        raise SystemExit("--deneme gerçek etiket dosyasını açamaz / gerçek çıktı dizinine yazamaz")
    if not a.deneme and (a.cemal1 or a.cemal2 or a.cikti):
        raise SystemExit("gerçek kipte --cemal1 / --cemal2 / --cikti verilmez (mühürlü yollar kullanılır)")
    if a.komut == "anahtar":
        J = ds4_anahtar(); print(json.dumps(J["ozet"], ensure_ascii=False))
    elif a.komut == "onay":
        J = ds4_onay(a.havuz_onbellek)
        print(json.dumps([(s["sayfa"], s["grup"], s["yanit"]["V1"], s["V1_dusen"]) for s in J["sayfalar"]], ensure_ascii=False))
    elif a.komut == "muhur":
        print(ds4_muhur())
    elif a.komut == "olc":
        r = ds4_olc(a.deneme, a.cemal1, a.cemal2, a.cikti)
        print(json.dumps({k: {"karar_n": v["karar_n"], **{m: _f4(x["kappa"]) for m, x in v["model"].items()}} for k, v in r["kume"].items()},
                         ensure_ascii=False))
    else:
        T = ds4_test()
        print(json.dumps({"tamam": T["tamam"], "kural_sha": T["kural_sha"], "esik_sha": T["esik_sha"]}, ensure_ascii=False))
        for x in T["tablo"]:
            print(x["seri"], "beklenen", x["beklenen"], "çıkan", x["cikan"], "P1/P2/P3i/P3ii/P3iii", x["P1"], x["P2"], x["P3i"], x["P3ii"],
                  x["P3iii"], "d", x["d"], "H1", x["h1"], "H2", x["h2"], "kır", x["kirilim"], "dipler", x["pivot_dip"], x["pivot_dip_atr"])
