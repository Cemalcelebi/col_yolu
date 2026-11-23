"""DS3 — DİP SAVUNMASI v3: Cemal'in cümlesinden doğrudan kural (23 Kasım 2026). GETİRİ ÖLÇMEZ.

Cemal (23.11.2026, aynen): "Çok kolay: eğer bir enstrüman düşüyor ve son bir dipten sonra mumlar bir hat boyunca daha yukarıda kalıp
aşağıda fitil boyu küçülüyor ise bu dip savunması."  Önceki sözleri: "dip delinmiş mi tamam, bu kolay, ama yeterli değil; mumların fitili
değil gövde ile tepki alması gerekir"; "dip oluşumu + alt fitili az mumlar + dip savunması = yön yukarı".
Önceki ders (Ç211): kuralı Cemal'in işaretlerinden SEÇMEK ezber üretti (40 sayfada 0,63 -> bağımsız sette 0,23). Bu yüzden kural ve BÜTÜN
parametreleri cümleden, ETİKETLERE BAKMADAN sabitlenir (DS3_ESIK); etiketler yalnız mühürden sonra `olc` ile açılır.

Sinyal sonrası fiyat hiçbir adımda okunmaz: pencere = kör sayfa penceresi (tanim2.tz_pencere = goz_uyum._gu_pencere; veri sinyal günü
t'de KESİLİR, son 121 geçerli bar).
Komutlar (repo kökünden):
  python arastirma_cikti/goz_uyum/ds3.py test                 çakışma kapısı + sentetik seriler + prefix değişmezliği
  python arastirma_cikti/goz_uyum/ds3.py anahtar              iki setin 80 sayfası: (a)-(d) ara değerleri + V1 / V2 / V3 -> ds3_anahtar.json
  python arastirma_cikti/goz_uyum/ds3.py muhur                sha'lar + kural + hüküm + kontrol tablosu -> DS3_ON_KAYIT.md (kontrol kapısı)
  python arastirma_cikti/goz_uyum/ds3.py olc                  mühür denetimi + etiketleri AÇAR -> DS3_SONUC.md, ds3_sonuc.json
  python arastirma_cikti/goz_uyum/ds3.py pdf                  görsel kontrol -> DS3_GORSEL.pdf (olc sonrası)
  (deneme: olc / pdf --deneme --cemal1 X.json --cemal2 Y.json --cikti DIZIN  -> mühür denetimi yok, uydurma etiketle kod yolu sınaması)
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

_CK_ONCE_DS = {k: id(v) for k, v in globals().items()}

import numpy as np
import pandas as pd

DS_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(os.getcwd(), "arastirma_cikti", "goz_uyum")
if DS_DIR not in sys.path:
    sys.path.insert(0, DS_DIR)
import goz_uyum as GU  # noqa: E402  (yalnız okunur: gu_veri, _gu_pencere, _sha, _jyaz, _yaz, _simdi, _gu_git, gu_kappa, gu_norm)
import tanim2 as TZ  # noqa: E402  (yalnız okunur: tz_pencere, TZ_YOL)

dslog = logging.getLogger("ds3")
if not dslog.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

KOK = GU.KOK
DS_YOL = {"is_tanimi": os.path.join(DS_DIR, "DS3_IS_TANIMI.md"), "anahtar": os.path.join(DS_DIR, "ds3_anahtar.json"),
          "onkayit": os.path.join(DS_DIR, "DS3_ON_KAYIT.md"), "sonuc": os.path.join(DS_DIR, "DS3_SONUC.md"),
          "sonuc_json": os.path.join(DS_DIR, "ds3_sonuc.json"), "pdf": os.path.join(DS_DIR, "DS3_GORSEL.pdf"),
          "set1_anahtar": GU.GU_YOL["anahtar"], "set2_anahtar": TZ.TZ_YOL["anahtar"],
          "set1_cemal": os.path.join(DS_DIR, "cemal_isaret.json"), "set2_cemal": os.path.join(DS_DIR, "cemal_isaret2.json"),
          "govde_anahtar": os.path.join(DS_DIR, "govde_anahtar.json"),
          "kod": os.path.abspath(__file__) if "__file__" in globals() else os.path.join(DS_DIR, "ds3.py")}

# ---------------------------------------------------------------- KURAL (Cemal'in cümlesinden; etiketler okunmadan yazıldı; ADIM 1 commit'i)
# Pencere W = kör sayfa penceresi (121 geçerli bar, dizin 0..120, t = 120). Karar penceresi = son 60 mum [t-59..t].
# (b) SON DİP: d = [t-59 .. t-5] aralığında en düşük Low'un günü; eşit en düşük Low birden çoksa EN SON gün; m = t - d (>= 5).
# (a) DÜŞÜŞ: max High [d-60 .. d-1] / Low(d) - 1 >= 0,20.
# (c) HAT BOYUNCA YUKARIDA: c1 dip delinmez (dip sonrası m mumun hepsinde Low >= Low(d)) VE c2 hat eğimi >= 0 (hat = dip sonrası
#     m Low'un zamana göre en küçük kareler doğrusu) VE c3 dip sonrası mumların en az %80'inde min(O,C) >= hattın o gündeki değeri.
# (d) ALT FİTİL KÜÇÜLÜYOR: w_i = (min(O_i,C_i) - L_i) / ATR14(d), i = d+1..t; w'nin zamana göre en küçük kareler eğimi < 0 VE
#     son üçte birin ortalama w'si < ilk üçte birin ortalama w'si.
# V1 (ANA) = a ∧ b ∧ c ∧ d;  V2 = a ∧ b ∧ c1 ∧ d (hat şartı yok);  V3 = a ∧ b ∧ c (fitil şartı yok).
DS3_ESIK: Dict[str, Any] = {
    "pencere_bar": 121, "karar_pencere": 60, "dip_sonrasi_min": 5, "dusus_bar": 60, "dusus_min": 0.20, "hat_ust_pay": 0.80,
    "hat_egim_min": 0.0, "atr_n": 14, "ucte_bir": 3,
    "belirsizlik": {
        "dip_esitlik": "eşit en düşük Low birden çok günde ise d = EN SON gün (tam eşitlik, float ==)",
        "dusus": "tepe = max High, d'den önceki 60 mum [d-60 .. d-1] (d hariç); oran = tepe / Low(d) - 1",
        "dip_delinmez": "Low_i >= Low(d) (eşitlik delinme sayılmaz), i = d+1..t",
        "hat": "x = 1..m (i - d), y = Low_i; numpy.polyfit derece 1; hat_i = kesişim + eğim x x_i",
        "egim_sifir": "c2: eğim >= -1e-12 x Low(d) (sayısal sıfır yatay sayılır); d: w eğimi < -1e-12 (sayısal sıfır küçülme sayılmaz)",
        "hat_ustu": "min(O_i,C_i) >= hat_i - 1e-9 x |hat_i| (bağıl sayısal tolerans)",
        "atr": "TR_j = max(H_j - L_j, |H_j - C_{j-1}|, |L_j - C_{j-1}|); ATR14(d) = ortalama TR, j = d-13..d",
        "ucte_bir": "k = floor(m / 3) (m >= 5 olduğu için k >= 1); ilk üçte bir = dip sonrası ilk k mum, son üçte bir = son k mum",
        "b": "pencere geçerli ve d bulunduysa b = DOĞRU (m >= 5 tanım gereği); bulunamazsa kural YOK",
    },
    "varyant": {"V1": "a ∧ b ∧ c ∧ d (ANA; Cemal'in tam cümlesi)", "V2": "a ∧ b ∧ c1 (dip delinmez) ∧ d (hat şartı yok)",
                "V3": "a ∧ b ∧ c (fitil şartı yok)"},
    "kappa": {"B": 5000, "tohum": 20261125, "guven": 0.95, "bonferroni_k": 3, "gecerli": 0.60, "gecerli_alt": 0.40, "kismen": 0.40,
              "karar_min": 30},
    "hukum": "V1 (ANA): iki set birleşik Cemal kararlarıyla (işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 "
             "(B 5000, sayfa yeniden örneklemesi) -> TANIM GEÇERLİ; kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; "
             "kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı ayrı da raporlanır; birinde V1 kappa < 0,40 ise "
             "'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33) verilir, hüküm sözü yalnız V1 için",
    "not": "parametreler (0,20; 60; 5; %80; üçte bir) iş tanımından aynen; etiketlere bakılmadan sabitlendi; GETİRİ YOK",
}


class DSHata(RuntimeError):
    """Durdurucu hata: veri / mühür / tanım tutmadı."""


def _sha_esik() -> str:
    return hashlib.sha256(json.dumps(DS3_ESIK, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _f(x: Any, d: int = 3) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"{float(x):.{d}f}"
    except (TypeError, ValueError):
        return str(x)


# ================================================================ 1) KURAL (yalnız pencere; t sonrası yok)
def ds3_parca_dizi(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray) -> Dict[str, Any]:
    """Diziler kör sayfa penceresi (son eleman = t, 121 bar). Dört parça + ara değerler + V1 / V2 / V3."""
    E = DS3_ESIK
    O, H, L, C = (np.asarray(a, float) for a in (O, H, L, C))
    n = len(C)
    if n != int(E["pencere_bar"]):
        raise DSHata(f"pencere {n} bar (beklenen {E['pencere_bar']})")
    if not (np.all(np.isfinite(np.c_[O, H, L, C])) and np.all(H > L) and np.all(L > 0)):
        raise DSHata("geçersiz bar (NaN / H <= L / L <= 0) pencerede")
    t = n - 1; P = int(E["karar_pencere"]); B = int(E["dip_sonrasi_min"]); D = int(E["dusus_bar"]); A = int(E["atr_n"])
    # (b) son dip
    i0, i1 = t - (P - 1), t - B
    seg = L[i0:i1 + 1]; mn = float(seg.min())
    d = i0 + int(np.flatnonzero(seg == mn)[-1])
    m = t - d
    if d - D < 0 or d - A < 0 or m < B:
        raise DSHata(f"dip dizini {d}: geri bakış için pencere kısa")
    Ld = float(L[d])
    # (a) düşüş
    tepe_i = d - D + int(np.argmax(H[d - D:d])); tepe = float(H[tepe_i])
    dusus = tepe / Ld - 1.0
    a = bool(dusus >= float(E["dusus_min"]))
    # (c) hat boyunca yukarıda
    post = np.arange(d + 1, t + 1); x = (post - d).astype(float)
    Lp = L[post]; bp = np.minimum(O[post], C[post])
    c1 = bool(np.all(Lp >= Ld))
    egim, kes = (float(v) for v in np.polyfit(x, Lp, 1))
    hat = kes + egim * x
    ust = bp >= hat - 1e-9 * np.abs(hat)
    ust_pay = float(np.mean(ust))
    c2 = bool(egim >= float(E["hat_egim_min"]) - 1e-12 * Ld)
    c3 = bool(ust_pay >= float(E["hat_ust_pay"]))
    c = c1 and c2 and c3
    # (d) alt fitil küçülüyor
    j = np.arange(d - A + 1, d + 1)
    tr = np.maximum(H[j] - L[j], np.maximum(np.abs(H[j] - C[j - 1]), np.abs(L[j] - C[j - 1])))
    atr = float(np.mean(tr))
    if not atr > 0:
        raise DSHata("ATR14(d) <= 0")
    w = (bp - Lp) / atr
    w_egim = float(np.polyfit(x, w, 1)[0])
    k = m // int(E["ucte_bir"])
    w_ilk = float(np.mean(w[:k])); w_son = float(np.mean(w[-k:]))
    d_egim = bool(w_egim < -1e-12); d_ucte = bool(w_son < w_ilk)
    dd = d_egim and d_ucte
    b = True
    return {"d_idx": int(d), "m": int(m), "low_d": Ld, "tepe_idx": int(tepe_i), "tepe": tepe, "dusus": float(dusus), "a": a, "b": b,
            "min_post_low_oran": float(Lp.min() / Ld - 1.0), "c1_delinmez": c1, "hat_egim": egim, "hat_kesisim": kes,
            "hat_egim_atr": float(egim / atr), "hat_ust_pay": ust_pay, "c2_egim": c2, "c3_ust": c3, "c": bool(c),
            "atr_d": atr, "w_egim": w_egim, "k_ucte": int(k), "w_ilk": w_ilk, "w_son": w_son, "d_egim": d_egim, "d_ucte": d_ucte,
            "d": bool(dd), "V1": bool(a and b and c and dd), "V2": bool(a and b and c1 and dd), "V3": bool(a and b and c)}


def ds3_parca(W: pd.DataFrame) -> Dict[str, Any]:
    O, H, L, C = (W[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    r = ds3_parca_dizi(O, H, L, C)
    r["d_tarih"] = W.index[r["d_idx"]].strftime("%Y-%m-%d")
    return r


def _kural_sha() -> str:
    """Kural kaynağının (ds3_parca_dizi + ds3_parca) sha'sı: olc'de kuralın değişmediği ayrıca denetlenir."""
    src = inspect.getsource(ds3_parca_dizi) + inspect.getsource(ds3_parca)
    return hashlib.sha256(src.encode("utf-8")).hexdigest()


# ================================================================ 2) SETLER (anahtar dosyalarından YALNIZ sayfa -> pazar, sembol, sinyal günü)
def ds3_setler() -> pd.DataFrame:
    rows = []
    for st, yol in ((1, DS_YOL["set1_anahtar"]), (2, DS_YOL["set2_anahtar"])):
        J = json.load(open(yol, encoding="utf-8"))
        for s in J["sayfalar"]:
            rows.append({"set": st, "sayfa": int(s["sayfa"]), "pazar": str(s["pazar"]), "sembol": str(s["sembol"]),
                         "sinyal_gunu": str(s["sinyal_gunu"])[:10]})
        del J
    S = pd.DataFrame(rows).sort_values(["set", "sayfa"]).reset_index(drop=True)
    for st in (1, 2):
        s = S[S.set == st].sayfa.tolist()
        if s != list(range(1, 41)):
            raise DSHata(f"set {st} sayfaları 1..40 değil: {s[:5]}..")
    return S


_VERI: Dict[str, Dict[str, pd.DataFrame]] = {}


def ds3_pencere(pazar: str, sembol: str, t: str) -> pd.DataFrame:
    if pazar not in _VERI:
        dslog.info("veri yükleniyor: %s", pazar)
        _VERI[pazar] = GU.gu_veri(pazar)
    tt = pd.Timestamp(t)
    W = TZ.tz_pencere(pazar, sembol, tt, _VERI[pazar])                 # K2: veri t'de kesik + mekanik denetim (121 bar, son = t)
    if W.index.max() > tt or W.index[-1] != tt:
        raise DSHata(f"{sembol} {t}: pencere t sonrasını içeriyor")
    return W


def ds3_hesap(S: pd.DataFrame) -> pd.DataFrame:
    out = []
    for r in S.itertuples(index=False):
        W = ds3_pencere(r.pazar, r.sembol, r.sinyal_gunu)
        out.append(ds3_parca(W))
    return pd.concat([S.reset_index(drop=True), pd.DataFrame(out)], axis=1)


def ds3_anahtar() -> Dict[str, Any]:
    t0 = time.time()
    S = ds3_setler()
    R = ds3_hesap(S)
    sayfalar = []
    for r in R.to_dict("records"):
        r = {k: (bool(v) if isinstance(v, (np.bool_,)) else v) for k, v in r.items()}
        r["yanit"] = {v: ("VAR" if r[v] else "YOK") for v in ("V1", "V2", "V3")}
        sayfalar.append(r)
    ozet = {}
    for st in (1, 2, "birlesik"):
        X = R if st == "birlesik" else R[R.set == st]
        ozet[str(st)] = {"n": int(len(X)), **{f"{v}_VAR": int(X[v].sum()) for v in ("V1", "V2", "V3")},
                         **{f"{p}_DOGRU": int(X[p].sum()) for p in ("a", "c1_delinmez", "c2_egim", "c3_ust", "c", "d")}}
    J = {"surum": "ds3 v1", "uretim_utc": GU._simdi(),
         "uyari": "GETİRİ YOK; Cemal'in işaretleri bu dosya yazılırken AÇILMADI (etiketler yalnız mühürden sonra olc ile açılır)",
         "esik": DS3_ESIK, "esik_sha": _sha_esik(), "kural_sha": _kural_sha(),
         "girdi_sha": {"goz_uyum_anahtar.json": GU._sha(DS_YOL["set1_anahtar"]), "tanim2_anahtar.json": GU._sha(DS_YOL["set2_anahtar"])},
         "ozet": ozet, "sayfalar": sayfalar, "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(DS_YOL["anahtar"], J)
    dslog.info("anahtar: %s", json.dumps(ozet, ensure_ascii=False))
    return J


# ================================================================ 3) MÜHÜR
DS_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralın uyumu, kappa)"),
    "K2": ("EVET", "(a)-(d) yalnız kör sayfa penceresinden: tanim2.tz_pencere = goz_uyum._gu_pencere (veri t'de KESİK, 121 bar) + ds3_pencere "
                   "mekanik denetimi (W.index.max() <= t, W.index[-1] == t); ds3.py test prefix değişmezliği (t sonrası değişince sonuç aynı); "
                   "getiri / sinyal sonrası fiyat okunmaz; Cemal'in işaretleri mühürden önce açılmadı (olc açılış zamanı DS3_SONUC'ta)"),
    "K3": ("EVET", "GE.ge_hazir (H>L, V>0, O/H/L/C>0) geçerli bar (goz_uyum ile aynı); ds3_parca_dizi NaN / H <= L / L <= 0 görürse durur"),
    "K4": ("EVET", "sayfalar set 1 (goz_uyum_anahtar) ve set 2 (tanim2_anahtar) ile aynı: aynı hissede en çok 1 sayfa, 60 bar tekil; n = 40 + 40"),
    "K5": ("UYGULANMAZ", "giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik"),
    "K6": ("EVET", "tek kip V_*.pkl (goz_uyum ile aynı); düşüş oranı ve hat payı birimsiz, fitil ATR14(d) birimi; fiyat birimi kuralı etkilemez"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok"),
    "K8": ("EVET", "79-80 karar (iki set); karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); 3 varyant: Bonferroni 3 (%98,33) V2 / V3 için; "
                   "hüküm yalnız V1; set 1 ve set 2 ayrı raporlanır (birinde < 0,40 'tutarsız'); kural etiketlerden SEÇİLMEDİ (Ç211 ezber dersi)"),
    "K9": ("EVET", "kural + DS3_ESIK + varyantlar etiketler açılmadan commit (ADIM 1); yanıtlar ds3_anahtar.json'da etiket açılmadan mühürlü; "
                   "ds3.py + ds3_anahtar.json + DS3_ESIK + kural kaynağı sha'ları bu dosyada; olc sha'ları denetler ve yanıtları veriden yeniden hesaplayıp "
                   "mühürle karşılaştırır; hüküm eşikleri sabit"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırma yok; yalnız OHLCV"),
    "K11": ("EVET", "ds3.py anahtar aynı komutla deterministik yeniden üretilir (rastgelelik yok); olc 80 sayfanın yanıtını veriden yeniden hesaplar "
                    "ve mühürlü yanıtla eşitliğini şart koşar; bootstrap tohumu sabit (20261125)"),
    "K12": ("EVET", "iddia yok; yalnız 'uyum' ve 'kappa' sayısı; hüküm sözü yalnız ön kayıttaki eşikle ve yalnız V1 için"),
    "K13": ("EVET", "çakışma kapısı _CK_ONCE_DS + test; yasak dosyalar (defter, mevcut .py, anahtar / ön kayıt / sonuç dosyaları) değişmedi "
                    "(git diff boş); e-posta / anahtar yok (_yaz / _jyaz e-posta taraması); git add -A yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


def ds3_muhur() -> str:
    for y in (DS_YOL["anahtar"], DS_YOL["is_tanimi"]):
        if not os.path.exists(y):
            raise DSHata(f"mühür için dosya yok: {y}")
    J = json.load(open(DS_YOL["anahtar"], encoding="utf-8"))
    if J["esik_sha"] != _sha_esik():
        raise DSHata("DS3_ESIK anahtardan sonra değişmiş")
    if J["kural_sha"] != _kural_sha():
        raise DSHata("kural kaynağı anahtardan sonra değişmiş")
    ad = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
          "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
          "K13": "süreç", "K14": "boyut (gerçek para)"}
    tab = "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |\n|---|---|---|---|\n"
    for k, (yy, kn) in DS_KONTROL.items():
        tab += f"| {k} | {ad[k]} | {yy} | {kn} |\n"
    oz = J["ozet"]
    ot = ["| küme | n | (a) düşüş DOĞRU | (c1) delinmez | (c2) eğim >= 0 | (c3) %80 üstte | (c) | (d) fitil küçülüyor | V1 VAR | V2 VAR | V3 VAR |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for st, o in oz.items():
        ot.append(f"| {st} | {o['n']} | {o['a_DOGRU']} | {o['c1_delinmez_DOGRU']} | {o['c2_egim_DOGRU']} | {o['c3_ust_DOGRU']} | {o['c_DOGRU']} | "
                  f"{o['d_DOGRU']} | {o['V1_VAR']} | {o['V2_VAR']} | {o['V3_VAR']} |")
    bel = "\n".join(f"- {k}: {v}" for k, v in DS3_ESIK["belirsizlik"].items())
    m = f"""# DİP SAVUNMASI v3 (DS3) — ÖN KAYIT (Cemal'in işaretleri AÇILMADAN mühürlenir)

Üretim: {GU._simdi()} (UTC). Soru: Cemal'in 23.11.2026 cümlesi ("Çok kolay: eğer bir enstrüman düşüyor ve son bir dipten sonra mumlar bir hat boyunca daha yukarıda kalıp aşağıda fitil boyu küçülüyor ise bu dip savunması.") doğrudan, etiketlerden SEÇİLMEDEN kurala çevrilince, iki kör sette (GOZ_UYUM_KOR.pdf = set 1, TANIM2_KOR.pdf = set 2; 80 sayfa) Cemal'in VAR / YOK işaretleriyle örtüşüyor mu? GETİRİ ÖLÇÜLMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/ds3_anahtar.json` sha256: `{GU._sha(DS_YOL['anahtar'])}`
- kod: `arastirma_cikti/goz_uyum/ds3.py` sha256: `{GU._sha(DS_YOL['kod'])}`
- eşik sözlüğü (DS3_ESIK) sha256: `{_sha_esik()}`
- kural kaynağı (ds3_parca_dizi + ds3_parca) sha256: `{_kural_sha()}`
- iş tanımı: `arastirma_cikti/goz_uyum/DS3_IS_TANIMI.md` sha256: `{GU._sha(DS_YOL['is_tanimi'])}`
- girdi (yalnız sayfa -> pazar, sembol, sinyal günü okundu): goz_uyum_anahtar.json `{J['girdi_sha']['goz_uyum_anahtar.json']}`, tanim2_anahtar.json `{J['girdi_sha']['tanim2_anahtar.json']}`
- bağımlı kod: goz_uyum.py `{GU._sha(GU.GU_YOL['kod'])[:16]}`, tanim2.py `{GU._sha(TZ.TZ_YOL['kod'])[:16]}`, GOZ_ETIKET.py `{GU._sha(os.path.join(KOK, 'GOZ_ETIKET.py'))[:16]}`

## 2. Kural (ADIM 1'de, etiketler açılmadan commit; parametreler iş tanımından aynen)
Pencere: kör sayfa penceresi (121 geçerli bar, veri sinyal günü t'de kesik); karar penceresi son 60 mum [t-59..t].
- **(b) SON DİP**: d = [t-59 .. t-5] aralığında en düşük Low'un günü (dipten sonra en az 5 mum); m = t - d.
- **(a) DÜŞÜŞ**: d'den önceki 60 mumun en yüksek High'ı / Low(d) - 1 >= 0,20.
- **(c) HAT BOYUNCA YUKARIDA**: (c1) dip sonrası m mumun hiçbirinin Low'u Low(d)'nin altına inmez VE (c2) hat = dip sonrası Low'ların en küçük kareler doğrusu, eğimi >= 0 VE (c3) dip sonrası mumların en az %80'inde min(O,C) >= hattın o gündeki değeri.
- **(d) ALT FİTİL KÜÇÜLÜYOR**: w_i = (min(O_i,C_i) - L_i) / ATR14(d); dip sonrası w'nin zamana göre en küçük kareler eğimi < 0 VE son üçte birin ortalama w'si < ilk üçte birin ortalama w'si.
- **V1 (ANA)** = a ∧ b ∧ c ∧ d (Cemal'in tam cümlesi); **V2** = a ∧ b ∧ c1 ∧ d (hat şartı yok); **V3** = a ∧ b ∧ c (fitil şartı yok).

Tanım belirsizliklerinin çözümü (etiketlerden önce yazıldı):
{bel}

DS3_ESIK (tam): `{json.dumps(DS3_ESIK, ensure_ascii=False, sort_keys=True)}`

## 3. Mühürlü yanıtlar (ds3_anahtar.json 'sayfalar'; Cemal'in işaretleri AÇILMADAN yazıldı)
{chr(10).join(ot)}

## 4. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in set 1 (cemal_isaret.json) ve set 2 (cemal_isaret2.json) VAR / YOK işaretleri ile V1 / V2 / V3 arasında uyum ve Cohen kappa; set 1, set 2 ve birleşik; işaretsiz / '?' sayfa karar dışı, sayısı ayrıca yazılır.
- Aralık: kappa bootstrap (B {DS3_ESIK['kappa']['B']}, tohum {DS3_ESIK['kappa']['tohum']}, sayfa yeniden örneklemesi, yüzdelik): V1 için %95; V2 / V3 için Bonferroni 3 ile %98,33 (ayrıca %95 bilgi).
- HÜKÜM: {DS3_ESIK['hukum']}.
- Ek bilgi (hüküm dışı): uyuşmayan sayfaların (a)-(d) değerleri; Cemal VAR / kod YOK sayfalarda düşen parça sayımı; önceki en iyi GOVDE_1 ile aynı sayfalarda karşılaştırma (GOVDE_1 eşiği set 1 etiketleriyle seçildiği için set 1'de iç-örneklem).
- Kural ve eşik sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 5. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
{tab}
## 6. Git kaydı (bu dosyanın yazıldığı an)
- ds3.py: {GU._gu_git('arastirma_cikti/goz_uyum/ds3.py')}
- DS3_IS_TANIMI.md: {GU._gu_git('arastirma_cikti/goz_uyum/DS3_IS_TANIMI.md')}
"""
    GU._yaz(DS_YOL["onkayit"], m)
    import IZ_KARNE as IK
    r = IK.ik_kontrol_kapisi(DS_YOL["onkayit"])
    dslog.info("kontrol kapısı: %s", "GEÇTİ" if r["gecti"] else r)
    return DS_YOL["onkayit"]


def _ds3_muhur_oku() -> Dict[str, str]:
    if not os.path.exists(DS_YOL["onkayit"]):
        raise DSHata("ön kayıt yok")
    t = open(DS_YOL["onkayit"], encoding="utf-8").read(); out = {}
    for ad, desen in (("anahtar", r"ds3_anahtar\.json` sha256: `([0-9a-f]{64})`"), ("kod", r"ds3\.py` sha256: `([0-9a-f]{64})`"),
                      ("esik", r"eşik sözlüğü \(DS3_ESIK\) sha256: `([0-9a-f]{64})`"), ("kural", r"kural kaynağı \([^)]*\) sha256: `([0-9a-f]{64})`")):
        m = re.search(desen, t)
        if not m:
            raise DSHata(f"ön kayıtta {ad} sha'sı yok")
        out[ad] = m.group(1)
    return out


# ================================================================ 4) ÖLÇÜM
def _boot(a: np.ndarray, b: np.ndarray, B: int, tohum: int, guven: Tuple[float, ...]) -> Dict[str, Any]:
    rng = np.random.default_rng(tohum); n = len(a); ks = np.empty(B)
    for i in range(B):
        j = rng.integers(0, n, n); ks[i] = GU.gu_kappa(a[j], b[j])
    g = ks[np.isfinite(ks)]; out: Dict[str, Any] = {"gecersiz": int(B - len(g))}
    for gv in guven:
        al = (1 - gv) / 2 * 100
        out[f"{gv:.4f}"] = [float(np.percentile(g, al)), float(np.percentile(g, 100 - al))] if len(g) else [np.nan, np.nan]
    return out


def ds3_hukum(k: float, alt: float, n: int) -> str:
    E = DS3_ESIK["kappa"]
    if n < int(E["karar_min"]) or not np.isfinite(k):
        return "ÖLÇÜLEMEDİ (karar sayısı < 30 ya da kappa tanımsız)"
    if k >= E["gecerli"] and np.isfinite(alt) and alt >= E["gecerli_alt"]:
        return "TANIM GEÇERLİ"
    return "KISMEN" if k >= E["kismen"] else "GEÇERSİZ"


def _etiket_oku(yol: str) -> Dict[int, str]:
    C = json.load(open(yol, encoding="utf-8"))
    return {int(k): (GU.gu_norm(v) or "?") for k, v in C.items()}


def _neden(r: Dict[str, Any]) -> List[str]:
    out = []
    if not r["a"]:
        out.append(f"düşüş yok ({r['dusus']*100:.0f}% < 20%)")
    if not r["c1_delinmez"]:
        out.append(f"dip delinmiş (en düşük dip sonrası Low {r['min_post_low_oran']*100:+.1f}%)")
    if not r["c2_egim"]:
        out.append(f"hat iniyor (eğim {r['hat_egim_atr']:+.3f} ATR/mum)")
    if not r["c3_ust"]:
        out.append(f"gövdeler hattın üstünde değil (%{r['hat_ust_pay']*100:.0f} < %80)")
    if not r["d"]:
        out.append(f"fitil küçülmüyor (w eğim {r['w_egim']:+.4f}, ilk 1/3 {r['w_ilk']:.2f} -> son 1/3 {r['w_son']:.2f})")
    return out


def _govde_cevap(R: pd.DataFrame, kural: Dict[str, Any]) -> np.ndarray:
    import govde as GV                                                   # yalnız okunur (özellik + kural)
    out = []
    for r in R.itertuples(index=False):
        W = ds3_pencere(r.pazar, r.sembol, r.sinyal_gunu)
        x = GV.gv_ozellik(W)[kural["ozellik"]]
        out.append(bool(GV.gv_kural(np.array([x], float), kural["yon"], float(kural["esik"]))[0]))
    return np.array(out, bool)


def ds3_olc(deneme: bool = False, cemal1: Optional[str] = None, cemal2: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    if not deneme:
        M = _ds3_muhur_oku()
        for ad, gercek in (("anahtar", GU._sha(DS_YOL["anahtar"])), ("kod", GU._sha(DS_YOL["kod"])), ("esik", _sha_esik()), ("kural", _kural_sha())):
            if gercek != M[ad]:
                raise DSHata(f"MÜHÜR BOZUK: {ad} sha'sı ön kayıttakiyle aynı değil -> DURDU")
    J = json.load(open(DS_YOL["anahtar"], encoding="utf-8"))
    Sm = pd.DataFrame(J["sayfalar"])
    # K11: yanıtlar veriden yeniden hesaplanır ve mühürle eşit olmalı
    R = ds3_hesap(Sm[["set", "sayfa", "pazar", "sembol", "sinyal_gunu"]])
    for v in ("V1", "V2", "V3"):
        if (R[v].to_numpy(bool) != Sm[v].to_numpy(bool)).any():
            raise DSHata(f"{v} yanıtları veriden yeniden hesaplanınca mühürle aynı değil -> DURDU")
    acilis = GU._simdi()
    c1 = cemal1 or DS_YOL["set1_cemal"]; c2 = cemal2 or DS_YOL["set2_cemal"]
    et = {1: _etiket_oku(c1), 2: _etiket_oku(c2)}
    dslog.info("etiket dosyaları açıldı: %s (UTC)", acilis)
    for st in (1, 2):
        fazla = sorted(set(et[st]) - set(range(1, 41)))
        if fazla:
            raise DSHata(f"set {st} etiketinde anahtarda olmayan sayfa: {fazla}")
    Sm["cemal"] = [et[int(s)].get(int(p), "?") for s, p in zip(Sm.set, Sm.sayfa)]
    E = DS3_ESIK["kappa"]; bon = 1 - (1 - E["guven"]) / E["bonferroni_k"]
    # GOVDE_1 (önceki en iyi; ek bilgi)
    if deneme:
        g1k = {"ozellik": "G1_govde_dokunus_n", "yon": ">=", "esik": 3.0, "not": "DENEME: uydurma kural"}
        g2_muhur = None
    else:
        GJ = json.load(open(DS_YOL["govde_anahtar"], encoding="utf-8"))
        g1k = dict(GJ["kurallar"]["GOVDE_1"]); g2_muhur = {int(s["sayfa"]): s["yanit"]["GOVDE_1"] == "VAR" for s in GJ["sayfalar"]}
        del GJ
    Sm["GOVDE_1"] = _govde_cevap(Sm, g1k)
    if g2_muhur is not None:
        m2 = Sm.set == 2
        if any(bool(Sm.loc[i, "GOVDE_1"]) != g2_muhur[int(Sm.loc[i, "sayfa"])] for i in Sm.index[m2]):
            raise DSHata("GOVDE_1 set 2 yanıtları govde_anahtar mührüyle aynı değil")
    kumeler = {"set 1": Sm.set == 1, "set 2": Sm.set == 2, "birleşik": Sm.set > 0}
    sonuc: Dict[str, Any] = {"etiket_acilis_utc": acilis, "deneme": deneme, "n_sayfa": int(len(Sm)), "kume": {}, "govde_kural": g1k}
    for kad, km in kumeler.items():
        K = Sm[km & (Sm.cemal != "?")]; cb = (K.cemal == "VAR").to_numpy(bool); n = len(K)
        kd: Dict[str, Any] = {"karar_n": int(n), "isaretsiz": int((km & (Sm.cemal == "?")).sum()), "isaretsiz_sayfa":
                              [f"set {s} / {p}" for s, p in zip(Sm[km & (Sm.cemal == '?')].set, Sm[km & (Sm.cemal == '?')].sayfa)],
                              "cemal_VAR": int(cb.sum()), "model": {}}
        for v in ("V1", "V2", "V3", "GOVDE_1"):
            mod = K[v].to_numpy(bool)
            k = GU.gu_kappa(cb, mod)
            ar = _boot(cb, mod, int(E["B"]), int(E["tohum"]), (E["guven"], bon)) if n else {}
            tp, tn = int((cb & mod).sum()), int((~cb & ~mod).sum()); fp, fn = int((~cb & mod).sum()), int((cb & ~mod).sum())
            a95 = ar.get(f"{E['guven']:.4f}", [np.nan, np.nan]); abn = ar.get(f"{bon:.4f}", [np.nan, np.nan])
            huk = (ds3_hukum(k, a95[0], n) if v == "V1" else
                   ("BİLGİ (Bonferroni alt uç ile: " + ds3_hukum(k, abn[0], n) + ")" if v in ("V2", "V3") else "BİLGİ (önceki kural)"))
            kd["model"][v] = {"kod_VAR": int(mod.sum()), "uyum": float(np.mean(cb == mod)) if n else np.nan, "kappa": k, "ar95": a95, "ar_bon": abn,
                              "hukum": huk, "tablo": {"Cemal VAR + kod VAR": tp, "Cemal YOK + kod YOK": tn, "Cemal YOK + kod VAR": fp,
                                                      "Cemal VAR + kod YOK": fn},
                              "uyusmayan": [f"set {s} / {p}" for s, p in zip(K.set[cb != mod], K.sayfa[cb != mod])]}
        sonuc["kume"][kad] = kd
    # Cemal VAR / kod YOK: düşen parça sayımı (her varyant)
    parca_ad = {"a": "(a) düşüş yok", "c1_delinmez": "(c1) dip delinmiş", "c2_egim": "(c2) hat iniyor", "c3_ust": "(c3) gövdeler hattın altında",
                "d": "(d) fitil küçülmüyor"}
    say: Dict[str, Any] = {}
    for v, parcalar in (("V1", ["a", "c1_delinmez", "c2_egim", "c3_ust", "d"]), ("V2", ["a", "c1_delinmez", "d"]),
                        ("V3", ["a", "c1_delinmez", "c2_egim", "c3_ust"])):
        X = Sm[(Sm.cemal == "VAR") & (~Sm[v].astype(bool))]
        dus = {parca_ad[p]: int((~X[p].astype(bool)).sum()) for p in parcalar}
        tek = {parca_ad[p]: int(((~X[p].astype(bool)) & (X[[q for q in parcalar if q != p]].astype(bool).all(axis=1))).sum()) for p in parcalar}
        say[v] = {"n": int(len(X)), "dusen": dus, "yalniz_bu_dusen": tek}
    # Cemal YOK / kod VAR sayısı (V1) zaten tabloda
    sonuc["cemal_VAR_kod_YOK_parca"] = say
    nd = Sm.set.astype(str)
    uy_rows = []
    for _, r in Sm.iterrows():
        if r.cemal == "?" or (r.cemal == "VAR") == bool(r.V1):
            continue
        uy_rows.append({"sayfa": f"set {r.set} / {r.sayfa}", "cemal": r.cemal, "V1": "VAR" if r.V1 else "YOK", "V2": "VAR" if r.V2 else "YOK",
                        "V3": "VAR" if r.V3 else "YOK", "GOVDE_1": "VAR" if r.GOVDE_1 else "YOK", "m": int(r.m), "dusus": float(r.dusus),
                        "a": bool(r.a), "c1": bool(r.c1_delinmez), "c2": bool(r.c2_egim), "c3": bool(r.c3_ust), "hat_ust_pay": float(r.hat_ust_pay),
                        "hat_egim_atr": float(r.hat_egim_atr), "min_post_low_oran": float(r.min_post_low_oran), "d": bool(r.d),
                        "w_egim": float(r.w_egim), "w_ilk": float(r.w_ilk), "w_son": float(r.w_son), "neden": _neden(r.to_dict())})
    sonuc["V1_uyusmayan"] = uy_rows
    del nd
    # V1 ile GOVDE_1 aynı sayfalarda
    K = Sm[Sm.cemal != "?"]
    sonuc["V1_GOVDE_1"] = {"iki_kod_ayni_yanit": int((K.V1.astype(bool) == K.GOVDE_1.astype(bool)).sum()), "karar_n": int(len(K)),
                           "kod_kappa": GU.gu_kappa(K.V1.to_numpy(bool), K.GOVDE_1.to_numpy(bool)),
                           "V1_dogru_GOVDE_yanlis": int(((K.V1.astype(bool) == (K.cemal == "VAR")) & (K.GOVDE_1.astype(bool) != (K.cemal == "VAR"))).sum()),
                           "GOVDE_dogru_V1_yanlis": int(((K.V1.astype(bool) != (K.cemal == "VAR")) & (K.GOVDE_1.astype(bool) == (K.cemal == "VAR"))).sum())}
    sonuc["sayfa_cemal"] = {f"{s}/{p}": c for s, p, c in zip(Sm.set, Sm.sayfa, Sm.cemal)}
    md = _sonuc_md(sonuc, J)
    hedef = cikti or DS_DIR
    os.makedirs(hedef, exist_ok=True)
    GU._yaz(os.path.join(hedef, "DS3_SONUC.md"), md)
    GU._jyaz(os.path.join(hedef, "ds3_sonuc.json"), sonuc)
    return sonuc


def _sonuc_md(S: Dict[str, Any], J: Dict[str, Any]) -> str:
    E = DS3_ESIK["kappa"]
    B = S["kume"]["birleşik"]; v1 = B["model"]["V1"]
    L = [("# [DENEME — UYDURMA ETİKET] " if S["deneme"] else "# ") + "DİP SAVUNMASI v3 (DS3) — SONUÇ (iki kör set, 80 sayfa)", "",
         f"Üretim: {GU._simdi()} (UTC). Etiket dosyaları (cemal_isaret.json, cemal_isaret2.json) bu komutla açıldı: {S['etiket_acilis_utc']} (UTC). "
         "Mühür denetimi: ds3_anahtar.json, ds3.py, DS3_ESIK ve kural kaynağı sha'ları DS3_ON_KAYIT ile aynı; 80 sayfanın V1 / V2 / V3 yanıtı "
         "veriden yeniden hesaplandı, mühürle aynı. GETİRİ YOK.", "",
         f"Karar: birleşik {B['karar_n']} (Cemal VAR {B['cemal_VAR']}); işaretsiz / '?' (karar dışı): {B['isaretsiz']} {B['isaretsiz_sayfa']}.", "",
         f"## HÜKÜM (V1, ön kayıttaki eşikle): **{v1['hukum']}** — birleşik kappa {_f(v1['kappa'])}, %95 [{_f(v1['ar95'][0])}, {_f(v1['ar95'][1])}]", ""]
    s1 = S["kume"]["set 1"]["model"]["V1"]["kappa"]; s2 = S["kume"]["set 2"]["model"]["V1"]["kappa"]
    if (np.isfinite(s1) and s1 < 0.40) or (np.isfinite(s2) and s2 < 0.40):
        L += [f"NOT: **tutarsız** — V1 kappa set 1 {_f(s1)}, set 2 {_f(s2)}; en az biri < 0,40.", ""]
    L += ["## Kappa tablosu", "", "| model | küme | karar | kod VAR | uyum | kappa | %95 aralık | %98,33 (Bonferroni 3) | hüküm |",
          "|---|---|---|---|---|---|---|---|---|"]
    for v in ("V1", "V2", "V3", "GOVDE_1"):
        for kad in ("set 1", "set 2", "birleşik"):
            r = S["kume"][kad]["model"][v]; kd = S["kume"][kad]
            huk = r["hukum"] if kad == "birleşik" else ("ayrı rapor" if v == "V1" else "bilgi")
            L.append(f"| {v} | {kad} | {kd['karar_n']} | {r['kod_VAR']} | {_f(r['uyum'])} | {_f(r['kappa'])} | [{_f(r['ar95'][0])}, {_f(r['ar95'][1])}] | "
                     f"[{_f(r['ar_bon'][0])}, {_f(r['ar_bon'][1])}] | {huk} |")
    L += ["", f"V1 = a ∧ b ∧ c ∧ d (ANA); V2 = a ∧ b ∧ c1 ∧ d; V3 = a ∧ b ∧ c. GOVDE_1 = {S['govde_kural'].get('ozellik')} {S['govde_kural'].get('yon')} "
          f"{S['govde_kural'].get('esik')!r} (önceki en iyi; eşiği set 1 etiketleriyle seçildi -> set 1'de iç-örneklem, yalnız bilgi).", "",
          f"HÜKÜM kuralı (ön kayıt): {DS3_ESIK['hukum']}.", "", "## 2x2 (birleşik)", ""]
    for v in ("V1", "V2", "V3"):
        r = B["model"][v]
        L += [f"**{v}**: " + "; ".join(f"{k} {x}" for k, x in r["tablo"].items()), ""]
    for kad in ("set 1", "set 2"):
        L += [f"**V1 {kad}**: " + "; ".join(f"{k} {x}" for k, x in S["kume"][kad]["model"]["V1"]["tablo"].items()), ""]
    L += ["## Cemal VAR dediği halde kodun YOK dediği sayfalarda düşen parça", "",
          "| varyant | sayfa | düşen parça sayımı (bir sayfada birden çok olabilir) | yalnız bu parça düştü |", "|---|---|---|---|"]
    for v, x in S["cemal_VAR_kod_YOK_parca"].items():
        L.append(f"| {v} | {x['n']} | " + "; ".join(f"{k} {c}" for k, c in x["dusen"].items()) + " | " +
                 "; ".join(f"{k} {c}" for k, c in x["yalniz_bu_dusen"].items()) + " |")
    L += ["", "## V1 uyuşmayan sayfalar ve (a)-(d) değerleri", "",
          "| sayfa | Cemal | V1 | V2 | V3 | GOVDE_1 | m | düşüş | dip sonrası en düşük Low | hat eğimi (ATR/mum) | gövde hattın üstünde | w ilk 1/3 -> son 1/3 (eğim) | kod neden YOK / ne gördü |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in S["V1_uyusmayan"]:
        ne = "; ".join(r["neden"]) if r["neden"] else "dört parça da DOĞRU (kod VAR)"
        L.append(f"| {r['sayfa']} | {r['cemal']} | {r['V1']} | {r['V2']} | {r['V3']} | {r['GOVDE_1']} | {r['m']} | %{r['dusus']*100:.0f} | "
                 f"{r['min_post_low_oran']*100:+.1f}% | {r['hat_egim_atr']:+.3f} | %{r['hat_ust_pay']*100:.0f} | {r['w_ilk']:.2f} -> {r['w_son']:.2f} "
                 f"({r['w_egim']:+.4f}) | {ne} |")
    G = S["V1_GOVDE_1"]
    L += ["", "## Ek bilgi: V1 ile GOVDE_1 aynı sayfalarda", "",
          f"Karar {G['karar_n']} sayfada iki kod {G['iki_kod_ayni_yanit']} sayfada aynı yanıtı verdi (iki kod arası kappa {_f(G['kod_kappa'])}); "
          f"V1 doğru / GOVDE_1 yanlış {G['V1_dogru_GOVDE_yanlis']} sayfa; GOVDE_1 doğru / V1 yanlış {G['GOVDE_dogru_V1_yanlis']} sayfa.", "",
          "Not: uyum Cemal'in gözüyle uyumdur; getiri ölçülmedi. Kural Cemal'in cümlesinden etiketlere bakmadan sabitlendi (Ç211 dersi)."]
    return "\n".join(L) + "\n"


# ================================================================ 5) GÖRSEL KONTROL PDF'i
def _isaret(x: bool) -> str:
    return "✓" if x else "✗"


def ds3_sayfa_ciz(W: pd.DataFrame, r: Dict[str, Any], baslik: str, cemal: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure(figsize=(7.5, 10.5))
    n = len(W); x = np.arange(n) - (n - 1)
    O, H, L, C = (W[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    ax = fig.add_axes([0.05, 0.30, 0.91, 0.56])
    yes = C >= O; renk = np.where(yes, "#1a9850", "#d73027")
    d = int(r["d_idx"]); t = n - 1
    ax.axvspan(x[t - 59] - 0.5, x[t] + 0.5, color="#f2f2f2", zorder=0)                          # karar penceresi (son 60 mum)
    ax.vlines(x, L, H, colors=renk, linewidth=1.0, zorder=3)
    for xi, o, c, col in zip(x, O, C, renk):
        ax.add_patch(Rectangle((xi - 0.35, min(o, c)), 0.7, max(abs(c - o), (H.max() - L.min()) * 0.0008), facecolor=col, edgecolor=col,
                               linewidth=0.4, zorder=4))
    post = np.arange(d + 1, t + 1)
    bp = np.minimum(O[post], C[post])
    ax.vlines(x[post], L[post], bp, colors="#ff8c00", linewidth=3.2, zorder=5, alpha=0.85)        # dip sonrası alt fitiller
    ax.hlines(r["low_d"], x[d] - 0.5, x[t] + 0.5, colors="#1f4e9c", linestyles="--", linewidth=1.2, zorder=6)
    xx = (post - d).astype(float); hat = r["hat_kesisim"] + r["hat_egim"] * xx
    ax.plot(x[post], hat, color="#7b2cbf", linewidth=1.8, zorder=6)
    rngp = H.max() - L.min(); pad = rngp * 0.06
    ax.annotate("DİP", xy=(x[d], L[d]), xytext=(x[d], L[d] - pad * 0.8), ha="center", va="top", fontsize=9, color="#1f4e9c",
                fontweight="bold", arrowprops=dict(arrowstyle="->", color="#1f4e9c", lw=1.2), zorder=7)
    ti = int(r["tepe_idx"])
    ax.plot([x[ti]], [H[ti]], marker="v", color="#555555", markersize=7, zorder=7)
    ax.text(x[ti], H[ti] + pad * 0.25, "tepe", ha="center", va="bottom", fontsize=8, color="#555555")
    ax.axvline(x[-1] + 0.5, color="#555555", linewidth=0.8, zorder=2)
    ax.axvline(x[-1] - 0.5, color="#555555", linewidth=0.8, zorder=2)
    ax.set_ylim(L.min() - pad * 1.6, H.max() + pad); ax.set_xlim(x[0] - 1, x[-1] + 2)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.6); sp.set_color("#888888")
    fig.text(0.05, 0.94, baslik, fontsize=30, fontweight="bold", va="center", ha="left")
    fig.text(0.96, 0.94, f"KOD (V1): {'VAR' if r['V1'] else 'YOK'}\nCEMAL: {cemal}", fontsize=13, va="center", ha="right")
    fig.text(0.50, 0.885, "gri alan = son 60 mum · mavi kesik = dip seviyesi · mor = dip sonrası hat · turuncu = dip sonrası alt fitiller",
             fontsize=7.5, ha="center", color="#555555")
    satir = [
        f"{_isaret(r['a'])}  düşüş: tepeden dibe %{r['dusus']*100:.0f}  (şart >= %20)",
        f"{_isaret(r['c1_delinmez'])}  dip delinmedi: dip sonrası en düşük Low dibe göre {r['min_post_low_oran']*100:+.1f}%  ({r['m']} mum)",
        f"{_isaret(r['c2_egim'] and r['c3_ust'])}  hat üstünde: hat eğimi {'yatay/yükselen' if r['c2_egim'] else 'İNİYOR'} ; "
        f"gövde altı hattın üstünde %{r['hat_ust_pay']*100:.0f}  (şart >= %80)",
        f"{_isaret(r['d'])}  fitil küçülüyor: alt fitil ilk 1/3 {r['w_ilk']:.2f} -> son 1/3 {r['w_son']:.2f} ATR ; "
        f"eğim {'aşağı' if r['d_egim'] else 'aşağı DEĞİL'}",
    ]
    for i, s in enumerate(satir):
        fig.text(0.06, 0.235 - i * 0.042, s, fontsize=11.5, ha="left", va="center")
    fig.text(0.06, 0.055, "Yanlış gördüğü parça:   ☐ düşüş    ☐ dip    ☐ hat    ☐ fitil    ☐ hepsi doğru", fontsize=12, ha="left", va="center")
    return fig


def ds3_pdf(deneme: bool = False, cikti: Optional[str] = None) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    hedef = cikti or DS_DIR
    SJ = json.load(open(os.path.join(hedef, "ds3_sonuc.json"), encoding="utf-8"))
    if bool(SJ.get("deneme")) != bool(deneme):
        raise DSHata("ds3_sonuc.json deneme kipi ile PDF kipi uyuşmuyor")
    J = json.load(open(DS_YOL["anahtar"], encoding="utf-8")); Sm = pd.DataFrame(J["sayfalar"])
    Sm["cemal"] = [SJ["sayfa_cemal"].get(f"{s}/{p}", "?") for s, p in zip(Sm.set, Sm.sayfa)]
    Sm = Sm.sort_values(["set", "sayfa"]).reset_index(drop=True)
    v = Sm.V1.astype(bool)
    var_sec = pd.concat([Sm[v & (Sm.cemal == "YOK")], Sm[v & (Sm.cemal == "VAR")], Sm[v & (Sm.cemal == "?")]]).head(6)
    yok_sec = pd.concat([Sm[~v & (Sm.cemal == "VAR")], Sm[~v & (Sm.cemal == "YOK")], Sm[~v & (Sm.cemal == "?")]]).head(6)
    sec = pd.concat([var_sec, yok_sec])
    yol = os.path.join(hedef, "DS3_GORSEL.pdf")
    liste = []
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=(7.5, 10.5))
        fig.text(0.5, 0.90, "DİP SAVUNMASI — kodun gözü", fontsize=24, fontweight="bold", ha="center")
        fig.text(0.5, 0.83, "Kodun senin tanımını nasıl gördüğü.\nHer sayfada: yanlış gördüğü bir parça varsa işaretle.", fontsize=14,
                 ha="center", va="top")
        aciklama = ("Senin cümlen (23 Kas): \"Bir enstrüman düşüyor ve son bir dipten sonra mumlar bir hat boyunca\n"
                    "daha yukarıda kalıp aşağıda fitil boyu küçülüyor ise bu dip savunması.\"\n\n"
                    "Kod bunu dört parçaya böldü (son 60 mum):\n"
                    "1. DÜŞÜŞ: dipten önceki 60 mumun tepesi dipten en az %20 yukarıda.\n"
                    "2. DİP DELİNMEDİ: son dipten sonra hiçbir mum dibin altına inmedi (dipten sonra en az 5 mum).\n"
                    "3. HAT ÜSTÜNDE: dip sonrası Low'lardan çizilen hat yatay ya da yükselen ve\n"
                    "    mumların en az %80'inin gövde altı bu hattın üstünde.\n"
                    "4. FİTİL KÜÇÜLÜYOR: dip sonrası alt fitiller zamanla kısalıyor\n"
                    "    (son üçte bir, ilk üçte birden kısa).\n"
                    "Kod VAR der = dördü birden ✓.\n\n"
                    "Çizimde: gri alan = son 60 mum; DİP oku = son dip günü; mavi kesik = dip seviyesi;\n"
                    "mor çizgi = dip sonrası hat; turuncu = dip sonrası alt fitiller; 'tepe' = düşüşün başı.\n"
                    "Sayfa numarası, daha önce işaretlediğin kör setlerdeki numaradır (set 1 / set 2 + no).\n"
                    f"İlk {len(var_sec)} sayfa: kodun VAR dedikleri; sonraki {len(yok_sec)} sayfa: kodun YOK dedikleri\n"
                    "(önce senin VAR deyip kodun YOK dedikleri).\n\nGetiri yok; sinyal sonrası gösterilmez.")
        fig.text(0.07, 0.72, aciklama, fontsize=10, ha="left", va="top")
        pdf.savefig(fig); plt.close(fig)
        for _, r in sec.iterrows():
            W = ds3_pencere(r.pazar, r.sembol, r.sinyal_gunu)
            rr = ds3_parca(W)
            if rr["V1"] != bool(r.V1):
                raise DSHata("PDF: V1 yeniden hesapta mühürden farklı")
            bas = f"set {int(r.set)} / {int(r.sayfa)}"
            fig = ds3_sayfa_ciz(W, rr, bas, r.cemal)
            pdf.savefig(fig); plt.close(fig)
            liste.append({"sayfa": bas, "V1": "VAR" if rr["V1"] else "YOK", "cemal": r.cemal})
    boy = os.path.getsize(yol)
    if boy >= 6 * 1024 * 1024:
        raise DSHata(f"PDF 6 MB'tan büyük: {boy}")
    dslog.info("PDF %s (%.2f MB): %s", yol, boy / 1e6, liste)
    return {"yol": yol, "bayt": boy, "sayfalar": liste}


# ================================================================ 6) TEST
def ds3_cakisma_kontrol() -> None:
    ez = [k for k, v in _CK_ONCE_DS.items() if k in globals() and id(globals()[k]) != v and not k.startswith("_")]
    if ez:
        raise DSHata(f"çakışma kapısı: bellekteki mevcut ad(lar) ezildi: {ez[:5]}")


def _sentetik(tur: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """121 bar: 0..79 düşüş (140 -> 101), 80 = dip (Low 99), 81..120 yükselen hat + küçülen alt fitil."""
    n = 121; O = np.zeros(n); C = np.zeros(n); H = np.zeros(n); L = np.zeros(n)
    for i in range(80):
        p = 140.0 - (140.0 - 101.0) * i / 79.0
        O[i] = p + 0.3; C[i] = p - 0.3; H[i] = p + 0.6; L[i] = p - 0.6
    O[80] = 100.0; C[80] = 100.2; H[80] = 100.5; L[80] = 99.0
    for i in range(81, n):
        k = i - 81; p = 100.0 + 0.1 * (k + 1)
        w = 1.0 - 0.95 * k / 39.0 if tur != "fitil_buyur" else 0.05 + 0.95 * k / 39.0
        O[i] = p; C[i] = p + 0.3; H[i] = C[i] + 0.2; L[i] = p - w
    if tur == "delinen":
        L[118] = 98.0
    if tur == "dusus_yok":
        for i in range(80):
            O[i] = 101.3; C[i] = 100.7; H[i] = 101.6; L[i] = 100.4
    return O, H, L, C


def ds3_test() -> Dict[str, Any]:
    ds3_cakisma_kontrol()
    r = ds3_parca_dizi(*_sentetik("tam"))
    assert r["d_idx"] == 80 and r["m"] == 40 and r["a"] and r["c1_delinmez"] and r["c2_egim"] and r["c3_ust"] and r["d"], r
    assert r["V1"] and r["V2"] and r["V3"], "dip + yükselen hat + küçülen fitil serisinde V1 VAR olmalı"
    r = ds3_parca_dizi(*_sentetik("delinen"))
    assert r["d_idx"] == 80 and not r["c1_delinmez"] and not r["V1"] and not r["V2"] and not r["V3"], "dip delinen seride V1 YOK olmalı"
    r = ds3_parca_dizi(*_sentetik("fitil_buyur"))
    assert not r["d"] and not r["V1"] and r["V3"], "fitil büyüyen seride V1 YOK, V3 VAR olmalı"
    r = ds3_parca_dizi(*_sentetik("dusus_yok"))
    assert not r["a"] and not r["V1"], "düşüş olmayan seride V1 YOK olmalı"
    # eşit en düşük Low: EN SON gün
    O, H, L, C = _sentetik("tam"); L[100] = 99.0
    r = ds3_parca_dizi(O, H, L, C); assert r["d_idx"] == 100, r["d_idx"]
    # dip [t-4..t] içinde ise d ona gidemez (dipten sonra en az 5 mum) ve dip delinmiş sayılır
    O, H, L, C = _sentetik("tam"); L[117] = 98.5
    r = ds3_parca_dizi(O, H, L, C); assert r["d_idx"] == 80 and not r["c1_delinmez"] and r["m"] >= 5
    # hat iniyor: dip sonrası Low'lar düşen (ama dibin üstünde) -> c2 YANLIŞ
    O, H, L, C = _sentetik("tam")
    for i in range(81, 121):
        k = i - 81; p = 110.0 - 0.2 * k; O[i] = p; C[i] = p + 0.3; H[i] = C[i] + 0.2; L[i] = p - 0.5
    r = ds3_parca_dizi(O, H, L, C); assert not r["c2_egim"] and not r["V1"], r
    # prefix değişmezliği: t sonrası veri değişince sonuç aynı (dizi ve DataFrame)
    rng = np.random.default_rng(11); n = 260
    Cx = 100 + np.cumsum(rng.normal(0, 1, n)); Ox = Cx + rng.normal(0, .3, n)
    Hx = np.maximum(Ox, Cx) + abs(rng.normal(0, .5, n)) + .1; Lx = np.minimum(Ox, Cx) - abs(rng.normal(0, .5, n)) - .1
    Cx, Ox, Hx, Lx = (a - min(Lx.min(), 0) + 5 for a in (Cx, Ox, Hx, Lx))
    i = 200; s = slice(i - 120, i + 1)
    x1 = ds3_parca_dizi(Ox[s], Hx[s], Lx[s], Cx[s])
    O2, H2, L2, C2 = Ox.copy(), Hx.copy(), Lx.copy(), Cx.copy()
    O2[i + 1:] = 1; H2[i + 1:] = 2; L2[i + 1:] = 0.5; C2[i + 1:] = 1.5
    x2 = ds3_parca_dizi(O2[s], H2[s], L2[s], C2[s])
    assert x1 == x2, "DS3 t sonrasına bağlı"
    idx = pd.bdate_range("2020-01-01", periods=n)
    D1 = pd.DataFrame({"Open": Ox, "High": Hx, "Low": Lx, "Close": Cx}, index=idx)
    D2 = pd.DataFrame({"Open": O2, "High": H2, "Low": L2, "Close": C2}, index=idx)
    t = idx[i]
    y1 = ds3_parca(D1[D1.index <= t].iloc[-121:]); y2 = ds3_parca(D2[D2.index <= t].iloc[-121:])
    assert y1 == y2, "prefix (DataFrame) değişmezliği bozuk"
    # pencere boyu denetimi
    try:
        ds3_parca_dizi(Ox[:100], Hx[:100], Lx[:100], Cx[:100]); raise AssertionError("kısa pencere kabul edildi")
    except DSHata:
        pass
    # bootstrap / hüküm
    a = np.array([1, 1, 0, 0] * 10, bool)
    assert abs(GU.gu_kappa(a, a) - 1) < 1e-12
    assert ds3_hukum(0.7, 0.45, 79) == "TANIM GEÇERLİ" and ds3_hukum(0.7, 0.3, 79) == "KISMEN"
    assert ds3_hukum(0.5, 0.2, 79) == "KISMEN" and ds3_hukum(0.3, 0.1, 79).startswith("GEÇERSİZ") and ds3_hukum(0.9, 0.8, 20).startswith("ÖLÇÜLEMEDİ")
    return {"tamam": True, "kural_sha": _kural_sha(), "esik_sha": _sha_esik()}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", choices=["anahtar", "muhur", "olc", "pdf", "test"])
    ap.add_argument("--deneme", action="store_true")
    ap.add_argument("--cemal1", default=None)
    ap.add_argument("--cemal2", default=None)
    ap.add_argument("--cikti", default=None)
    a = ap.parse_args()
    if a.deneme and not (a.cikti and a.cemal1 and a.cemal2):
        raise SystemExit("--deneme için --cikti, --cemal1, --cemal2 gerekli (gerçek etiket dosyaları açılmaz)")
    if a.deneme and ({os.path.realpath(a.cemal1), os.path.realpath(a.cemal2)} & {os.path.realpath(DS_YOL["set1_cemal"]),
                                                                                os.path.realpath(DS_YOL["set2_cemal"])}
                     or os.path.realpath(a.cikti) == os.path.realpath(DS_DIR)):
        raise SystemExit("--deneme gerçek etiket dosyasını açamaz / gerçek çıktı dizinine yazamaz")
    if not a.deneme and (a.cemal1 or a.cemal2 or a.cikti):
        raise SystemExit("gerçek kipte --cemal1 / --cemal2 / --cikti verilmez (mühürlü yollar kullanılır)")
    if a.komut == "anahtar":
        J = ds3_anahtar(); print(json.dumps(J["ozet"], ensure_ascii=False))
    elif a.komut == "muhur":
        print(ds3_muhur())
    elif a.komut == "olc":
        r = ds3_olc(a.deneme, a.cemal1, a.cemal2, a.cikti)
        print(json.dumps({k: {"karar_n": v["karar_n"], **{m: _f(x["kappa"]) for m, x in v["model"].items()}} for k, v in r["kume"].items()},
                         ensure_ascii=False))
    elif a.komut == "pdf":
        print(json.dumps(ds3_pdf(a.deneme, a.cikti), ensure_ascii=False))
    else:
        print(ds3_test())
