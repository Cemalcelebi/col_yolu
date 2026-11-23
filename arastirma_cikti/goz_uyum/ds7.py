"""DS7 — DİP SAVUNMASI v7: dip / mavi çizgi (DS5 + DS6 D3, DONDURULMUŞ) + DAYANIKLI ANA TREND kırılımı (23 Kasım 2026). GETİRİ ÖLÇMEZ.

Cemal'in DS6_ONAY hükümleri (cemal_ds6_onay.json; tanım geri bildirimi, kör set etiketi DEĞİL; 23 Kas, aynen): (1) mavi dip çizgisine itiraz
YOK ('DİP var'); kodun VAR dediği 3 sayfanın 3'ü doğru; yanlışların hepsi kırmızı trend ve kırılımda. (2) s8: 'asıl trend 1 (soldaki büyük
tepeden inen); 2 ve 3 ara trend'. (3) s1: 'DİP var, kırdı': fiyat son mumlarda çizgiyi kırmış, kod '>= 3 kapanış' şartıyla saymamış.
(4) 'Ana trend esas alınmalı; en sonunda fiyat ara trendleri bırakıp ana trend çizgisine gelmişse ara trendleri esas almayacaktır.'

EK (Cemal, 23 Kas, aynen): "Bazen şöyle olabilir: bir trend çok uzun zaman tam harfiyen uyuyor, ama arada bir olay / bir haberle trend
delinmiş gibi; bu sayılıyor olmalı. Yani aslında daha çok ne ağır basıyor onu anlamalı, akıllı olmalı."

DS7 = dip / mavi parçaları (P1 düşüşten dip, P2' D3 yatay toleransı, P3 takip, P4 dip korunur; ds6.ds6_parca_dizi'den AYNEN) +
  i0 = d'den önceki pencerede en yüksek High (eşitte en erken).
  V1 (ANA) DAYANIKLI ANA TREND: aday = i0'dan ve i0'dan sonraki her pivot tepeden (5/5) geçen doğru (eğim < 0); DOKUNUŞ = çizgiye 0,5 ATR'den
     yakın pivot tepe; KISA DELME (<= 3 mum, sonra kapanış çizgi altına döner; affedilir) / UZUN DELME (affedilmez); geçerli = uzun delme yok
     ∧ kısa delme <= 2; seçim en çok dokunuş > az kısa delme > j sağda; geçerli aday yoksa saf zarfa düşer ('dayanıklı çizgi yok').
  V2 SAF ZARF: s = max_{i0 < j <= d} (High_j - High_i0) / (j - i0); T(i) = High_i0 + s (i - i0).
  Kırılım her ikisinde C_t > çizgi(t); V1 = dip / mavi ∧ eğim < 0 ∧ kırılım (dayanıklı); V2 aynı (saf zarf); V3 = yalnız dip / mavi.
Sinyal sonrası fiyat hiçbir adımda okunmaz: pencere = kör sayfa penceresi (tanim2.tz_pencere; veri sinyal günü t'de KESİLİR, son 121 bar).
Komutlar (repo kökünden):
  python arastirma_cikti/goz_uyum/ds7.py test                  çakışma kapısı + sentetik seriler S1-S6 + prefix değişmezliği
  python arastirma_cikti/goz_uyum/ds7.py anahtar               iki setin 80 sayfası: ara değerler + V1 / V2 / V3 -> ds7_anahtar.json
  python arastirma_cikti/goz_uyum/ds7.py onay [--havuz_onbellek X.pkl]
                                                               DS6_ONAY'ın aynı 36 sayfası yeni çizimle -> DS7_ONAY.pdf + ds7_onay_anahtar.json
  python arastirma_cikti/goz_uyum/ds7.py muhur                 sha'lar + kural + sentetik tablo + hüküm + kontrol tablosu -> DS7_ON_KAYIT.md
  python arastirma_cikti/goz_uyum/ds7.py olc                   mühür denetimi + etiketleri AÇAR -> DS7_SONUC.md, ds7_sonuc.json
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

_CK_ONCE_DS7 = {k: id(v) for k, v in globals().items()}

import numpy as np
import pandas as pd

DS7_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(os.getcwd(), "arastirma_cikti", "goz_uyum")
if DS7_DIR not in sys.path:
    sys.path.insert(0, DS7_DIR)
import goz_uyum as GU  # noqa: E402  (yalnız okunur)
import tanim2 as TZ  # noqa: E402  (yalnız okunur)
import ds5 as D5  # noqa: E402  (yalnız okunur: ds5_pencere, ds5_setler, ds5_havuz, _havuz_sha5, _insa, _boot5, _etiket_oku5, _govde1_cevap5)
import ds6 as D6  # noqa: E402  (yalnız okunur: ds6_parca_dizi (dip / mavi parçaları, DONDURULMUŞ), _insa6)

d7log = logging.getLogger("ds7")
if not d7log.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

KOK7 = GU.KOK
DS7_YOL = {"is_tanimi": os.path.join(DS7_DIR, "DS7_IS_TANIMI.md"), "anahtar": os.path.join(DS7_DIR, "ds7_anahtar.json"),
           "onkayit": os.path.join(DS7_DIR, "DS7_ON_KAYIT.md"), "sonuc": os.path.join(DS7_DIR, "DS7_SONUC.md"),
           "sonuc_json": os.path.join(DS7_DIR, "ds7_sonuc.json"), "pdf": os.path.join(DS7_DIR, "DS7_ONAY.pdf"),
           "onay_anahtar": os.path.join(DS7_DIR, "ds7_onay_anahtar.json"),
           "set1_anahtar": GU.GU_YOL["anahtar"], "set2_anahtar": TZ.TZ_YOL["anahtar"],
           "set1_cemal": os.path.join(DS7_DIR, "cemal_isaret.json"), "set2_cemal": os.path.join(DS7_DIR, "cemal_isaret2.json"),
           "govde_anahtar": os.path.join(DS7_DIR, "govde_anahtar.json"), "ds5_anahtar": os.path.join(DS7_DIR, "ds5_anahtar.json"),
           "ds6_anahtar": os.path.join(DS7_DIR, "ds6_anahtar.json"), "ds6_onay_anahtar": os.path.join(DS7_DIR, "ds6_onay_anahtar.json"),
           "cemal_ds6_onay": os.path.join(DS7_DIR, "cemal_ds6_onay.json"), "cemal_ds5_onay": os.path.join(DS7_DIR, "cemal_ds5_onay.json"),
           "ds5_kod": os.path.join(DS7_DIR, "ds5.py"), "ds6_kod": os.path.join(DS7_DIR, "ds6.py"),
           "kod": os.path.abspath(__file__) if "__file__" in globals() else os.path.join(DS7_DIR, "ds7.py")}

# ---------------------------------------------------------------- KURAL (iş tanımından aynen; kör set etiketleri okunmadan; ADIM 1 commit'i)
DS7_ESIK: Dict[str, Any] = {
    "dip_mavi": "ds6.ds6_parca_dizi'den AYNEN (DONDURULMUŞ; ds5.py ve ds6.py değiştirilmedi, sha ön kayıtta): pencere 121 bar (t = 120), kural "
                "penceresi son 120 mum [t-119 .. t]; d = [t-119 .. t-8] en düşük Low (eşitte en son); P1 max High [t-119 .. d-1] / Low(d) - 1 >= 0,20; "
                "mavi çizgi = çapa (d, B_d), B = min(Open, Close), s* = min (B_i - B_d) / (i - d); P2' (DS6 D3) mavi çizginin dipten t'ye "
                "toplam düşüşü max(0, -s* x m) <= 0,5 ATR14(d); P3 dokunuş B_i - L(i) < 0,35 ATR, >= 3, ilk ve ikinci yarıda >= 1; P4 dip "
                "sonrası Low >= Low(d) - 0,25 ATR",
    "dokunus_atr": 0.5, "delme_atr": 0.25, "kisa_delme_max_mum": 3, "kisa_delme_max_n": 2, "tepe_sol": 5, "tepe_sag": 5,
    "ana_trend": {
        "i0": "i0 = s0 + argmax High [s0 .. d-1] (s0 = t-119; d'den önceki pencere kısmında en yüksek High; eşitlikte EN ERKEN; np.argmax); "
              "d = s0 ise i0 yok -> TREND YANLIŞ (V1 ve V2)",
        "zarf_egim": "V2 SAF ZARF: s_z = max_{i0 < j <= d} (High_j - High_i0) / (j - i0) (j = d dahil); i0'dan geçen ve [i0 .. d] aralığındaki "
                     "BÜTÜN High'ların üstünde ya da üzerinde kalan en dış doğru; j* = argmax (eşitlikte EN ERKEN); T_z(i) = High_i0 + s_z (i - i0)",
        "pivot": "pivot tepe = ds6._ds6_pivot (DS5 / DS6 ile aynı: H_j > max H_{j-5..j-1}, H_j >= max H_{j+1..j+5}, j-5 >= s0, j+5 <= d)",
        "aday": "V1 DAYANIKLI: aday = her pivot tepe j, i0 < j, High_j < High_i0 (eğim < 0, kesin); çizgi_j(i) = High_i0 + e_j (i - i0), "
                "e_j = (High_j - High_i0) / (j - i0)",
        "dokunus": "DOKUNUŞ = i0 < p olan pivot tepeler (aday j dahil; i0'ın kendisi sayılmaz) için |High_p - çizgi(p)| < 0,5 x ATR14(d) (kesin "
                   "küçük; altında ya da üstünde)",
        "delme": "DELME BÖLÜMÜ = i0 < i <= d aralığında Close_i > çizgi(i) + 0,25 x ATR14(d) (kesin) olan maksimal ardışık mum öbeği. KISA DELME = "
                 "öbek boyu <= 3 mum VE öbekten sonra (öbek sonu < j <= d) en az bir Close_j < çizgi(j) (kesin; altına dönüş). Öteki her öbek "
                 "UZUN DELME (3 mumdan uzun ya da d'ye kadar altına dönmeyen). Turuncu iğne = kısa delme öbeğinde Close - çizgi en büyük mum",
        "gecerli": "geçerli aday = UZUN DELME yok VE kısa delme sayısı <= 2",
        "secim": "geçerli adaylar arasında sıralama: (1) DOKUNUŞ ÇOK, (2) kısa delme AZ, (3) j BÜYÜK (daha sağda, daha uzun); ilk sıradaki seçilir. "
                 "Geçerli aday yoksa (ya da pivot tepe yoksa) V1 çizgisi = saf zarf (V2 çizgisi) ve 'dayanıklı çizgi yok' notu (dy_yok = True)",
        "trend": "TREND (V1) = seçilen çizginin eğimi < 0; TREND_Z (V2) = s_z < 0 (kesin); i0 yoksa ikisi de YANLIŞ",
        "kirilim": "KIRILIM (V1) = C_t > çizgi_V1(t); KIRILIM_Z (V2) = C_t > T_z(t) (kesin); çizgi t'ye uzatılır (çizgi(t) <= 0 olabilir; o "
                   "zaman kırılım kendiliğinden doğrudur, bilgi sütununda yazılır)",
        "bilgi": "karar dışı: V1 çizgisi için kırılım günü kb = ilk i (d < i <= t) Close_i > çizgi(i); kırılımdan beri mum = t - kb; "
                 "C_t / çizgi(t) - 1; dip sonrası çizgi üstünde kapanış sayısı; aday / geçerli aday sayısı",
    },
    "varyant": {"V1": "P1 ∧ P2' ∧ P3 ∧ P4 ∧ TREND ∧ KIRILIM (ANA; dayanıklı ana trend)", "V2": "P1 ∧ P2' ∧ P3 ∧ P4 ∧ TREND_Z ∧ KIRILIM_Z (saf zarf)",
                "V3": "P1 ∧ P2' ∧ P3 ∧ P4 (yalnız dip / mavi; trend şartı yok)"},
    "dusen_parca": "V1'i düşüren parçalar: P1, P2 (= P2'), P3, P4, TREND (eğim >= 0 ya da i0 yok), KIRILIM (C_t <= çizgi_V1(t)); V1 = altısı doğru",
    "kappa": {"B": 5000, "tohum": 20261128, "guven": 0.95, "bonferroni_k": 3, "gecerli": 0.60, "gecerli_alt": 0.40, "kismen": 0.40,
              "karar_min": 30},
    "hukum": "V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu "
             ">= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (kural Cemal'in DS5_ONAY / DS6_ONAY işaretlerinden kuruldu; set 1 / "
             "set 2 sayfaları önceki DS3-DS6 işlerinde kullanıldı; kesin hüküm yalnız Cemal'in görsel onayı (DS7_ONAY.pdf) + bağımsız üçüncü kör "
             "setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. "
             "Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33)",
    "onay": {"kaynak": "ds6_onay_anahtar.json sayfa 1..36 (pazar, sembol, sinyal günü), AYNI sırada ve numarada, yeni çizimle; yeni sayfa yok",
             "havuz": "bilgi: DS4 / DS5 / DS6 görsel onay havuzu (ds5.ds5_havuz; sha ds6_onay_anahtar.json ile eşit şartı) üzerinde V1 / V2 / V3 "
                      "sayımı (seçim yok)"},
    "onay17": {"YANLIS": [1, 4, 8, 12, 16, 17, 21, 22], "DOGRU": [3, 5, 7, 9, 10, 13, 20, 23, 24],
               "eslem": "Cemal'in DS6_ONAY genel işareti (cemal_ds6_onay.json 'genel'): YANLIŞ -> Cemal'in beklediği yanıt = v6 yanıtının tersi; "
                        "DOĞRU -> v6 yanıtı. v7 V1 bu beklenen yanıta eşitse 'uyumlu'. Etiket: YANLIŞ ve v7 değişti -> 'itiraz giderildi'; "
                        "YANLIŞ ve aynı -> 'itiraz sürüyor'; DOĞRU ve aynı -> 'korundu'; DOĞRU ve değişti -> 'DİKKAT: bozuldu'. BİLGİ (hüküm dışı); "
                        "işaretsiz 19 sayfa yalnız değişim olarak listelenir"},
    "not": "dayanıklı çizgi parametreleri (0,5 ATR dokunuş; 0,25 ATR delme; kısa delme <= 3 mum, <= 2 adet; 5/5 pivot) iş tanımı EK'inden "
           "aynen; saf zarf parametresiz; dip / mavi parçaları DS5 / DS6'dan dondurulmuş; kör set etiketlerine bakılmadan sabitlendi; GETİRİ YOK",
}


class DS7Hata(RuntimeError):
    """Durdurucu hata: veri / mühür / tanım tutmadı."""


def _sha_esik7() -> str:
    return hashlib.sha256(json.dumps(DS7_ESIK, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _f7(x: Any, d: int = 3) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"{float(x):.{d}f}"
    except (TypeError, ValueError):
        return str(x)


def _isr7(x: bool) -> str:
    return "✓" if x else "✗"


# ================================================================ 1) KURAL (yalnız pencere; t sonrası yok)
def _ds7_zarf(H: np.ndarray, C: np.ndarray, s0: int, d: int, t: int) -> Dict[str, Any]:
    """V2 saf zarf ve kırılımı. Zarf yalnız [s0 .. d] High'larından; kırılım yalnız C_t."""
    out: Dict[str, Any] = {"i0_idx": -1, "i0_high": float("nan"), "jstar_idx": -1, "jstar_high": float("nan"), "egim_z": float("nan"),
                           "T_z_t": float("nan"), "TREND_Z": False, "KIRILIM_Z": False, "son_kapanis": float(C[t])}
    if d <= s0:
        return out
    i0 = s0 + int(np.argmax(H[s0:d]))
    jj = np.arange(i0 + 1, d + 1)
    eg = (H[jj] - H[i0]) / (jj - i0)
    k = int(np.argmax(eg)); s = float(eg[k]); js = int(jj[k])
    Tt = float(H[i0] + s * (t - i0))
    out.update({"i0_idx": int(i0), "i0_high": float(H[i0]), "jstar_idx": js, "jstar_high": float(H[js]), "egim_z": s, "T_z_t": Tt,
                "TREND_Z": bool(s < 0), "KIRILIM_Z": bool(C[t] > Tt)})
    return out


def _ds7_delme(C: np.ndarray, i0: int, d: int, h0: float, e: float, atr: float) -> Tuple[List[int], List[int], int]:
    """i0 < i <= d delme öbekleri: (kısa öbek iğneleri, uzun öbek başları, kısa sayısı). Yalnız [i0 .. d] kapanışları okunur."""
    E = DS7_ESIK; ke = float(E["delme_atr"]) * atr; kmax = int(E["kisa_delme_max_mum"])
    ii = np.arange(i0 + 1, d + 1); cz = h0 + e * (ii - i0); ust = C[ii] > cz + ke
    kisa: List[int] = []; uzun: List[int] = []; k = 0
    while k < len(ii):
        if not ust[k]:
            k += 1; continue
        b = k
        while b + 1 < len(ii) and ust[b + 1]:
            b += 1
        sonra = np.arange(int(ii[b]) + 1, d + 1)
        don = bool(len(sonra) and np.any(C[sonra] < h0 + e * (sonra - i0)))
        if (b - k + 1) <= kmax and don:
            blok = ii[k:b + 1]; kisa.append(int(blok[int(np.argmax(C[blok] - (h0 + e * (blok - i0))))]))
        else:
            uzun.append(int(ii[k]))
        k = b + 1
    return kisa, uzun, len(kisa)


def _ds7_dayanikli(H: np.ndarray, C: np.ndarray, s0: int, d: int, t: int, atr: float, Z: Dict[str, Any]) -> Dict[str, Any]:
    """V1 dayanıklı ana trend: i0'dan ve i0'dan sonraki pivot tepelerden geçen adaylar; dokunuş / kısa-uzun delme; seçim. Yalnız [s0 .. d]."""
    E = DS7_ESIK; te = float(E["dokunus_atr"]) * atr; kn = int(E["kisa_delme_max_n"])
    out: Dict[str, Any] = {"dy_j_idx": -1, "egim_ana": float("nan"), "T_t": float("nan"), "dy_dokunus": [], "dy_dokunus_n": 0, "dy_kisa": [],
                           "dy_kisa_n": 0, "dy_aday_n": 0, "dy_gecerli_n": 0, "dy_yok": True, "dy_pivot": []}
    i0 = int(Z["i0_idx"])
    if i0 < 0:
        return out
    h0 = float(H[i0])
    piv = [int(j) for j in D6._ds6_pivot(H, s0, d) if j > i0]
    aday = []
    for j in piv:
        if not H[j] < h0:
            continue
        e = (float(H[j]) - h0) / float(j - i0)
        dok = [p for p in piv if abs(float(H[p]) - (h0 + e * (p - i0))) < te]
        kisa, uzun, nk = _ds7_delme(C, i0, d, h0, e, atr)
        aday.append({"j": j, "e": e, "dok": dok, "kisa": kisa, "uzun": uzun, "gecerli": bool(not uzun and nk <= kn)})
    gec = sorted([a for a in aday if a["gecerli"]], key=lambda a: (-len(a["dok"]), len(a["kisa"]), -a["j"]))
    out.update({"dy_aday_n": len(aday), "dy_gecerli_n": len(gec), "dy_pivot": piv})
    if gec:
        a = gec[0]
        out.update({"dy_j_idx": int(a["j"]), "egim_ana": float(a["e"]), "T_t": float(h0 + a["e"] * (t - i0)), "dy_dokunus": a["dok"],
                    "dy_dokunus_n": len(a["dok"]), "dy_kisa": a["kisa"], "dy_kisa_n": len(a["kisa"]), "dy_yok": False})
    else:                                                                    # geçerli aday yok -> saf zarf ('dayanıklı çizgi yok')
        e = float(Z["egim_z"])
        dok = [p for p in piv if abs(float(H[p]) - (h0 + e * (p - i0))) < te]
        out.update({"egim_ana": e, "T_t": float(Z["T_z_t"]), "dy_dokunus": dok, "dy_dokunus_n": len(dok), "dy_yok": True})
    return out


def _ds7_ana_trend(H: np.ndarray, C: np.ndarray, s0: int, d: int, t: int, atr: float) -> Dict[str, Any]:
    """V2 saf zarf + V1 dayanıklı ana trend + kırılım ve bilgi sütunları (V1 çizgisi için)."""
    Z = _ds7_zarf(H, C, s0, d, t)
    Dy = _ds7_dayanikli(H, C, s0, d, t, atr, Z)
    out = {**Z, **Dy, "TREND": False, "KIRILIM": False, "kapanis_T_oran": float("nan"), "kirilim_idx": -1, "kirilim_mum": -1,
           "ust_kapanis_n": 0, "T_t_pozitif": False, "kapanis_Tz_oran": float("nan"), "ayni_cizgi": False}
    if Z["i0_idx"] < 0:
        return out
    i0 = int(Z["i0_idx"]); e = float(Dy["egim_ana"]); Tt = float(Dy["T_t"])
    post = np.arange(d + 1, t + 1); ust = post[C[post] > H[i0] + e * (post - i0)]
    out.update({"TREND": bool(e < 0), "KIRILIM": bool(C[t] > Tt), "kapanis_T_oran": float(C[t] / Tt - 1.0) if Tt > 0 else float("nan"),
                "kirilim_idx": int(ust[0]) if len(ust) else -1, "kirilim_mum": int(t - ust[0]) if len(ust) else -1,
                "ust_kapanis_n": int(len(ust)), "T_t_pozitif": bool(Tt > 0),
                "kapanis_Tz_oran": float(C[t] / Z["T_z_t"] - 1.0) if Z["T_z_t"] > 0 else float("nan"),
                "ayni_cizgi": bool(abs(e - float(Z["egim_z"])) < 1e-12)})
    return out


def ds7_parca_dizi(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray) -> Dict[str, Any]:
    """Diziler kör sayfa penceresi (son eleman = t, 121 bar). Dip / mavi parçaları ds6'dan AYNEN + ana trend (dayanıklı + saf zarf) + V1 / V2 / V3."""
    O, H, L, C = (np.asarray(a, float) for a in (O, H, L, C))
    try:
        r6 = D6.ds6_parca_dizi(O, H, L, C)                                   # pencere / geçersiz bar denetimi + dip / mavi parçaları (DONDURULMUŞ)
    except D6.DS6Hata as ex:
        raise DS7Hata(str(ex)) from ex
    t, s0, d = int(r6["t_idx"]), int(r6["s0_idx"]), int(r6["d_idx"])
    A = _ds7_ana_trend(H, C, s0, d, t, float(r6["atr_d"]))
    dipmavi = bool(r6["P1"] and r6["P2"] and r6["P3"] and r6["P4"])
    v1 = bool(dipmavi and A["TREND"] and A["KIRILIM"])
    v2 = bool(dipmavi and A["TREND_Z"] and A["KIRILIM_Z"])
    out = {k: r6[k] for k in ("t_idx", "s0_idx", "d_idx", "m", "low_d", "B_d", "tepe_idx", "tepe", "dusus", "P1", "atr_d", "s", "cizgi_son",
                              "dokunus", "dokunus_n", "dokunus_ilk", "dokunus_ikinci", "mavi_dusus_atr", "P2", "P3", "min_post_low_atr", "P4")}
    out.update(A)
    out.update({"DIPMAVI": dipmavi, "V1": v1, "V2": v2, "V3": dipmavi,
                "v6_V1": bool(r6["V1"]), "v6_cizgi_var": bool(r6["cizgi_var"]), "v6_ha_idx": int(r6["ha_idx"]), "v6_hb_idx": int(r6["hb_idx"]),
                "v6_ha": float(r6["ha"]), "v6_egim": float(r6["egim_dusen"]), "v6_gecerli": bool(r6["gecerli_secildi"]),
                "ds5_V1": bool(r6["V3"])})
    return out


def ds7_parca(W: pd.DataFrame) -> Dict[str, Any]:
    O, H, L, C = (W[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    r = ds7_parca_dizi(O, H, L, C)
    ix = W.index

    def tar(i: int) -> Optional[str]:
        return ix[i].strftime("%Y-%m-%d") if i >= 0 else None
    r["d_tarih"] = tar(r["d_idx"]); r["i0_tarih"] = tar(r["i0_idx"]); r["jstar_tarih"] = tar(r["jstar_idx"])
    r["dy_j_tarih"] = tar(r["dy_j_idx"]); r["kirilim_tarih"] = tar(r["kirilim_idx"]); r["dy_kisa_tarih"] = [tar(j) for j in r["dy_kisa"]]
    return r


def _kural_sha7() -> str:
    """Kural kaynağının (_ds7_zarf + _ds7_delme + _ds7_dayanikli + _ds7_ana_trend + ds7_parca_dizi + ds7_parca) + DS6 kural sha'sı (DS5 dahil)."""
    src = "".join(inspect.getsource(f) for f in (_ds7_zarf, _ds7_delme, _ds7_dayanikli, _ds7_ana_trend, ds7_parca_dizi, ds7_parca)) + \
        D6._kural_sha6()
    return hashlib.sha256(src.encode("utf-8")).hexdigest()


def ds7_dusen(r: Dict[str, Any]) -> List[str]:
    """V1'i düşüren parçalar (P1 / P2 / P3 / P4 / TREND / KIRILIM)."""
    return [p for p in ("P1", "P2", "P3", "P4", "TREND", "KIRILIM") if not r[p]]


def ds7_neden_metni(r: Dict[str, Any]) -> List[str]:
    out = []
    if not r["P1"]:
        out.append("P1 düşüş yok (%s < %%20)" % ("-" if not np.isfinite(r["dusus"]) else f"%{r['dusus']*100:.0f}"))
    if not r["P2"]:
        out.append(f"P2 mavi çizgi {r['mavi_dusus_atr']:.2f} ATR aşağı (> 0,5)")
    if not r["P3"]:
        out.append(f"P3 takip yok (dokunuş {r['dokunus_n']}: ilk yarı {r['dokunus_ilk']}, ikinci yarı {r['dokunus_ikinci']})")
    if not r["P4"]:
        out.append(f"P4 dip delinmiş (dip sonrası en düşük Low {r['min_post_low_atr']:+.2f} ATR)")
    if not r["TREND"]:
        out.append("TREND ana çizgi düşmüyor" + ("" if r["i0_idx"] >= 0 else " (d'den önce mum yok)"))
    if r.get("dy_yok") and r["i0_idx"] >= 0:
        out.append("not: dayanıklı çizgi yok (saf zarf kullanıldı)")
    if not r["KIRILIM"]:
        oran = r["kapanis_T_oran"]
        out.append("KIRILIM son kapanış ana çizginin altında" + (f" (%{oran*100:+.1f})" if oran is not None and np.isfinite(oran) else ""))
    return out


# ================================================================ 2) SETLER ve ANAHTAR
def _temiz7(r: Dict[str, Any]) -> Dict[str, Any]:
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


def ds7_hesap(S: pd.DataFrame) -> pd.DataFrame:
    out = []
    for r in S.itertuples(index=False):
        W = D5.ds5_pencere(r.pazar, r.sembol, r.sinyal_gunu)                # K2: veri t'de kesik + mekanik denetim (121 bar, son = t)
        out.append(ds7_parca(W))
    return pd.concat([S.reset_index(drop=True), pd.DataFrame(out)], axis=1)


def _ozet7(R: pd.DataFrame) -> Dict[str, Any]:
    return {"n": int(len(R)), **{f"{v}_VAR": int(R[v].sum()) for v in ("V1", "V2", "V3", "v6_V1", "ds5_V1")},
            **{f"{p}_DOGRU": int(R[p].sum()) for p in ("P1", "P2", "P3", "P4", "DIPMAVI", "TREND", "KIRILIM", "TREND_Z", "KIRILIM_Z", "dy_yok",
                                                         "ayni_cizgi")},
            "T_t_pozitif_degil": int((~R["T_t_pozitif"].astype(bool) & R["TREND"].astype(bool)).sum())}


def ds7_anahtar() -> Dict[str, Any]:
    t0 = time.time()
    S = D5.ds5_setler()
    R = ds7_hesap(S)
    J6 = json.load(open(DS7_YOL["ds6_anahtar"], encoding="utf-8"))
    m6 = {(int(s["set"]), int(s["sayfa"])): s for s in J6["sayfalar"]}; del J6
    fark = []
    for r in R.itertuples(index=False):
        s6 = m6[(int(r.set), int(r.sayfa))]
        for k in ("P1", "P2", "P3", "P4"):
            if bool(getattr(r, k)) != bool(s6[k]):
                fark.append((int(r.set), int(r.sayfa), k))
        if bool(r.v6_V1) != bool(s6["V1"]) or bool(r.ds5_V1) != bool(s6["V3"]):
            fark.append((int(r.set), int(r.sayfa), "v6_V1 / ds5_V1"))
    if fark:
        raise DS7Hata(f"dip / mavi parçaları ya da v6 / DS5 yanıtı ds6_anahtar.json mühürlü değerlerle aynı değil: {fark}")
    sayfalar = []
    for r in R.to_dict("records"):
        r = _temiz7(r)
        r["yanit"] = {v: ("VAR" if r[v] else "YOK") for v in ("V1", "V2", "V3")}
        r["V1_dusen"] = ds7_dusen(r)
        sayfalar.append(r)
    ozet = {str(st): _ozet7(R if st == "birlesik" else R[R.set == st]) for st in (1, 2, "birlesik")}
    J = {"surum": "ds7 v1", "uretim_utc": GU._simdi(),
         "uyari": "GETİRİ YOK; Cemal'in kör set işaretleri bu dosya yazılırken AÇILMADI (etiketler yalnız mühürden sonra olc ile açılır); "
                  "dizinler 121 barlık pencerede (t = 120); P1-P4, v6 V1 ve DS5 V1 ds6_anahtar.json ile eşit (denetlendi)",
         "esik": DS7_ESIK, "esik_sha": _sha_esik7(), "kural_sha": _kural_sha7(),
         "girdi_sha": {"goz_uyum_anahtar.json": GU._sha(DS7_YOL["set1_anahtar"]), "tanim2_anahtar.json": GU._sha(DS7_YOL["set2_anahtar"]),
                       "ds6_anahtar.json": GU._sha(DS7_YOL["ds6_anahtar"]), "ds5.py": GU._sha(DS7_YOL["ds5_kod"]),
                       "ds6.py": GU._sha(DS7_YOL["ds6_kod"])},
         "ozet": ozet, "sayfalar": sayfalar, "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(DS7_YOL["anahtar"], J)
    d7log.info("anahtar: %s", json.dumps(ozet, ensure_ascii=False))
    return J


# ================================================================ 3) GÖRSEL ONAY (DS6_ONAY'ın aynı 36 sayfası, yeni çizim)
def ds7_sayfa_ciz(W: pd.DataFrame, r: Dict[str, Any], no: int, toplam: int, v6_V1: bool):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure(figsize=(7.5, 10.5))
    ax = fig.add_axes([0.04, 0.29, 0.92, 0.56])
    O, H, L, C = (W[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    t = int(r["t_idx"]); s0 = int(r["s0_idx"]); d = int(r["d_idx"])
    idx = np.arange(s0, t + 1); x = idx - t
    Hs, Ls = H[idx], L[idx]; aralik = float(Hs.max() - Ls.min()); pad = aralik * 0.05
    xd = d - t
    ax.axvspan(xd + 0.5, 0.5, color="#fff4cc", alpha=0.8, zorder=0, linewidth=0)
    renk = np.where(C[idx] >= O[idx], "#1a9850", "#d73027")
    ax.vlines(x, Ls, Hs, colors=renk, linewidth=1.1, zorder=3)
    for xi, o, c, col in zip(x, O[idx], C[idx], renk):
        ax.add_patch(Rectangle((xi - 0.35, min(o, c)), 0.7, max(abs(c - o), aralik * 0.0008), facecolor=col, edgecolor=col, linewidth=0.4,
                               zorder=4))
    # mavi dip çizgisi + dokunuşlar (DS6 gibi)
    xs = np.array([d, t]); ys = r["B_d"] + r["s"] * (xs - d)
    ax.plot(xs - t, ys, color="#1f4e9c", linewidth=3.0, zorder=6, solid_capstyle="round")
    ax.annotate("DİP", xy=(xd, L[d]), xytext=(xd, L[d] - pad * 1.8), ha="center", va="top", fontsize=10, color="#1f4e9c", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#1f4e9c", lw=1.5), zorder=8)
    B = np.minimum(O, C)
    for j in r["dokunus"]:
        ax.plot([j - t], [B[j] - pad * 0.35], marker="o", markersize=6, markerfacecolor="none", markeredgecolor="#6a3d9a",
                markeredgewidth=1.6, linestyle="none", zorder=9)
    alt_y = Ls.min() - pad * 2.4; ust_y = Hs.max() + pad * 1.6
    # ince gri: DS6'nın seçtiği eski çizgi
    if r["v6_cizgi_var"]:
        a = int(r["v6_ha_idx"]); xg = np.array([a, t]); yg = r["v6_ha"] + r["v6_egim"] * (xg - a)
        ax.plot(xg - t, yg, color="#8c8c8c", linewidth=1.0, zorder=5, linestyle="-" if r["v6_gecerli"] else "--")
    # KALIN kırmızı: V1 dayanıklı ana trend (i0 -> t); kırmızı daire = i0 + dokunuş tepeleri; turuncu iğne = affedilen kısa delme;
    # kesik kırmızı = V2 saf zarf (farklıysa)
    if r["i0_idx"] >= 0:
        i0 = int(r["i0_idx"]); xr = np.array([i0, t])
        if not r["ayni_cizgi"]:
            ax.plot(xr - t, r["i0_high"] + r["egim_z"] * (xr - i0), color="#e31a1c", linewidth=1.3, zorder=6, linestyle=(0, (5, 4)))
        yr = r["i0_high"] + r["egim_ana"] * (xr - i0)
        ax.plot(xr - t, yr, color="#e31a1c", linewidth=3.2, zorder=7, solid_capstyle="round")
        for j in [i0] + [int(p) for p in r["dy_dokunus"]]:
            ax.plot([j - t], [H[j]], linestyle="none", marker="o", markersize=12, markerfacecolor="none", markeredgecolor="#e31a1c",
                    markeredgewidth=2.0, zorder=8)
        for j in r["dy_kisa"]:
            ax.plot([j - t], [H[j] + pad * 0.45], marker="^", markersize=11, color="#ff7f00", markeredgecolor="#b35806", linestyle="none",
                    zorder=9)
        Tt = float(r["T_t"])
        if alt_y <= Tt <= ust_y:
            ax.plot([0.55, 1.6], [Tt, Tt], color="#e31a1c", linewidth=2.4, zorder=9)
    # son kapanış noktası
    ax.plot([0], [C[t]], marker="o", markersize=7, color="#000000", linestyle="none", zorder=10)
    ax.plot([0.55, 1.6], [C[t], C[t]], color="#000000", linewidth=1.6, zorder=9)
    ax.axvline(0.5, color="#555555", linewidth=0.8, zorder=2); ax.axvline(-0.5, color="#555555", linewidth=0.8, zorder=2)
    ax.set_ylim(alt_y, ust_y); ax.set_xlim(x[0] - 1, 2)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.6); sp.set_color("#888888")
    fig.text(0.04, 0.945, f"{int(no)}", fontsize=44, fontweight="bold", va="center", ha="left")
    fig.text(0.96, 0.945, f"/ {toplam}", fontsize=16, va="center", ha="right", color="#666666")
    fig.text(0.53, 0.945, f"geçen sefer (v6): {'VAR' if v6_V1 else 'YOK'}  —  şimdi (v7): {'VAR' if r['V1'] else 'YOK'}", fontsize=11.5,
             va="center", ha="center", color="#222222", fontweight="bold")
    fig.text(0.50, 0.895, "kalın mavi = dipten başlayan gövde altı çizgisi · mor daire = mavi çizgiye değen mum · sarı zemin = dipten sonrası",
             fontsize=7.2, ha="center", color="#555555")
    fig.text(0.50, 0.878, "KALIN kırmızı = ana trend (en yüksek tepeden, en çok tepeye değen) · kırmızı daire = başladığı ve değdiği tepeler · "
             "turuncu ∧ = affedilen kısa iğne", fontsize=7.0, ha="center", color="#555555")
    fig.text(0.50, 0.861, "kesik kırmızı = saf zarf (farklıysa) · ince gri = geçen seferki (v6) çizgi · siyah nokta = son kapanış · sağdaki kısa "
             "çizgiler = son gündeki yerleri", fontsize=7.0, ha="center", color="#555555")
    if r["DIPMAVI"]:
        s1 = "Dip / mavi ✓ (onaylı)"
    else:
        s1 = "Dip / mavi ✗ (onaylı tanım)"
    s2 = f"Ana trend düşüyor {_isr7(r['TREND'])}"
    s3 = f"Son kapanış ana çizginin üstünde {_isr7(r['KIRILIM'])}"
    fig.text(0.50, 0.255, f"{s1}   —   {s2}", fontsize=12, ha="center", va="center")
    fig.text(0.50, 0.226, s3, fontsize=12, ha="center", va="center")
    s4 = (f"Ana trend: {int(r['dy_dokunus_n'])} dokunuş, affedilen delme {int(r['dy_kisa_n'])}"
          + ("  (dayanıklı çizgi yok: saf zarf)" if r["dy_yok"] and r["i0_idx"] >= 0 else ""))
    fig.text(0.50, 0.200, s4, fontsize=10.5, ha="center", va="center")
    ek = []
    if not r["DIPMAVI"]:
        ek += [n for n in ds7_neden_metni(r) if n[:2] in ("P1", "P2", "P3", "P4")]
    if r["TREND"] and r["T_t_pozitif"] and r["kapanis_T_oran"] is not None and np.isfinite(r["kapanis_T_oran"]):
        ek.append(f"son kapanış ana çizginin %{r['kapanis_T_oran']*100:+.1f} {'üstünde' if r['KIRILIM'] else 'altında'}"
                  + (f"; ilk kapanış üstte: son günden {r['kirilim_mum']} mum önce" if r["kirilim_idx"] >= 0 else ""))
    if ek:
        fig.text(0.50, 0.176, " · ".join(ek), fontsize=8.0, ha="center", va="center", color="#444444")
    fig.text(0.50, 0.135, f"SONUÇ: {'VAR' if r['V1'] else 'YOK'}", fontsize=20, fontweight="bold", ha="center", va="center")
    fig.text(0.50, 0.070, "☐ DOĞRU        ☐ YANLIŞ", fontsize=15, ha="center", va="center")
    return fig


def ds7_havuz_say(onbellek: Optional[str] = None) -> Dict[str, Any]:
    """Bilgi: görsel onay havuzunda (DS4 / DS5 / DS6 ile aynı; sha denetlenir) V1 / V2 / V3 sayımı. Seçim yok."""
    P = D5.ds5_havuz(onbellek)
    hsha = D5._havuz_sha5(P)
    J6o = json.load(open(DS7_YOL["ds6_onay_anahtar"], encoding="utf-8"))
    if J6o["havuz_sha"] != hsha:
        raise DS7Hata("havuz DS6 görsel onay havuzuyla aynı değil (sha)")
    K = []
    for q in P.itertuples(index=False):
        W = D5.ds5_pencere(q.pazar, q.sembol, q.tarih.strftime("%Y-%m-%d"))
        r = ds7_parca(W)
        K.append({"pazar": q.pazar, **{k: bool(r[k]) for k in ("V1", "V2", "V3", "v6_V1", "TREND", "KIRILIM", "DIPMAVI", "T_t_pozitif", "dy_yok",
                                                               "ayni_cizgi")}})
    KD = pd.DataFrame(K)
    return {"havuz_sha": hsha, "havuz_n": int(len(KD)),
            "havuz_pazar": {p: int((KD.pazar == p).sum()) for p in ("ABD", "AVR", "BIST")},
            "V1_VAR": {p: int(KD[KD.pazar == p].V1.sum()) for p in ("ABD", "AVR", "BIST")},
            "V2_VAR": {p: int(KD[KD.pazar == p].V2.sum()) for p in ("ABD", "AVR", "BIST")},
            "V3_VAR": {p: int(KD[KD.pazar == p].V3.sum()) for p in ("ABD", "AVR", "BIST")},
            "v6_V1_VAR": {p: int(KD[KD.pazar == p].v6_V1.sum()) for p in ("ABD", "AVR", "BIST")},
            "toplam": {k: int(KD[k].sum()) for k in ("V1", "V2", "V3", "v6_V1", "DIPMAVI", "TREND", "KIRILIM", "dy_yok", "ayni_cizgi")},
            "V1_T_t_pozitif_degil": int((KD.V1 & ~KD.T_t_pozitif).sum())}


def ds7_onay(onbellek: Optional[str] = None) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    t0 = time.time()
    J6o = json.load(open(DS7_YOL["ds6_onay_anahtar"], encoding="utf-8"))
    tum = []
    for s in sorted(J6o["sayfalar"], key=lambda z: int(z["sayfa"])):
        W = D5.ds5_pencere(s["pazar"], s["sembol"], s["sinyal_gunu"])
        r = _temiz7(ds7_parca(W))
        if bool(r["v6_V1"]) != bool(s["V1"]):
            raise DS7Hata(f"onay sayfa {s['sayfa']}: v6 V1 yeniden hesabı ds6_onay_anahtar.json ile aynı değil")
        tum.append({"sayfa": int(s["sayfa"]), "pazar": s["pazar"], "sembol": s["sembol"], "sinyal_gunu": s["sinyal_gunu"],
                    "grup_v6": s["grup"], **r})
    if [e["sayfa"] for e in tum] != list(range(1, 37)):
        raise DS7Hata("DS6 onay sayfaları 1..36 değil")
    havuz = ds7_havuz_say(onbellek)
    toplam = len(tum)
    yol = DS7_YOL["pdf"]
    with PdfPages(yol, metadata={"Title": "DIP SAVUNMASI v7 - gorsel onay", "Author": "ds7", "Creator": "ds7", "Producer": "ds7",
                                 "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(7.5, 10.5))
        fig.text(0.5, 0.90, "DİP SAVUNMASI — kodun gözü (v7)", fontsize=22, fontweight="bold", ha="center")
        kapak = ("Ana trend esas: kalın kırmızı çizgi dibe inişten\n"
                 "önceki en yüksek tepeden başlıyor ve bütün tepelerin\n"
                 "üstünden geçiyor (ara trendler altında kalır).\n"
                 "Kırılım = son kapanış bu çizginin üstünde.\n"
                 "Mavi dip çizgisi senin onayladığın haliyle aynı.\n"
                 "İnce gri = geçen seferki çizgi.\n"
                 "Kısa haber iğneleri (en çok 3 mum) affedilir;\n"
                 "çizgiyi en çok tepeye değen, ağır basan trend belirler.")
        fig.text(0.08, 0.85, kapak, fontsize=13.0, ha="left", va="top", linespacing=1.4)
        aciklama = ("Çizimler:\n"
                    "  DİP oku = penceredeki en derin nokta (en düşük fitil)\n"
                    "  kalın mavi çizgi = dip mumunun gövde altından başlayıp sonraki bütün gövde altlarının\n"
                    "      altında kalan çizgi (sağa son güne kadar); mor daire = mavi çizgiye değen mum\n"
                    "  KALIN kırmızı çizgi = ana trend: dibe inişten önceki en yüksek tepeden başlar, sonraki tepelerden\n"
                    "      en çoğuna değen çizgi; kapanışın çizgiyi en çok 3 mum delip geri döndüğü iğneler affedilir (en çok 2);\n"
                    "      daha uzun delinme çizgiyi bozar. Kırmızı daireler = başladığı ve değdiği tepeler; turuncu ∧ = affedilen iğne\n"
                    "  kesik kırmızı = bütün tepelerin üstünden geçen en dış çizgi (saf zarf), kalın çizgiden farklıysa\n"
                    "  ince gri çizgi = geçen seferki (v6) kırmızı çizgi (kesik = o zaman kirli sayılmıştı)\n"
                    "  siyah nokta = son kapanış; sağ kenardaki kısa kırmızı çizgi = ana çizginin son gündeki yeri\n"
                    "  sarı zemin = dipten sonraki bölge\n\n"
                    "Dip / mavi: düşüşten dip (en az %20), mavi çizgi yatay ya da yukarı (yarım mum boyundan az\n"
                    "      inen çizgi yatay), mumlar mavi çizgiyi takip ediyor (en az 3 dokunuş, iki yarıda), dip korunuyor.\n"
                    "Ana trend düşüyor: kalın kırmızı çizgi aşağı eğik.\n"
                    "Kırılım: son günün kapanışı kalın kırmızı çizginin üstünde (tek kapanış yeter).\n"
                    "Uygun çizgi yoksa kalın çizgi saf zarf olur (sayfada 'dayanıklı çizgi yok' yazar).\n"
                    "Her sayfanın üstünde geçen seferki (v6) ve şimdiki (v7) cevap yazılı.\n"
                    f"{toplam} sayfa, geçen seferkiyle aynı hisseler ve aynı sıra (bu PDF kör değil, onay için).\n"
                    "Hisse adı yok; son günden sonrası gösterilmez. Kutulardan birini işaretlemen yeter.")
        fig.text(0.05, 0.53, aciklama, fontsize=8.3, ha="left", va="top", linespacing=1.32)
        pdf.savefig(fig); plt.close(fig)
        for rr in tum:
            W = D5.ds5_pencere(rr["pazar"], rr["sembol"], rr["sinyal_gunu"])
            r = ds7_parca(W)
            if r["V1"] != bool(rr["V1"]):
                raise DS7Hata("onay: V1 yeniden hesapta farklı")
            fig = ds7_sayfa_ciz(W, r, int(rr["sayfa"]), toplam, bool(rr["v6_V1"]))
            pdf.savefig(fig); plt.close(fig)
    boy = os.path.getsize(yol)
    if boy >= 6 * 1024 * 1024:
        raise DS7Hata(f"PDF 6 MB'tan büyük: {boy}")
    sayfalar = []
    for rr in tum:
        rr = _temiz7(rr); rr["V1_dusen"] = ds7_dusen(rr); rr["neden"] = ds7_neden_metni(rr)
        rr["yanit"] = {v: ("VAR" if rr[v] else "YOK") for v in ("V1", "V2", "V3")}
        rr["yanit_v6"] = "VAR" if rr["v6_V1"] else "YOK"
        sayfalar.append(rr)
    J = {"surum": "ds7 onay v1", "uretim_utc": GU._simdi(),
         "uyari": "GİZLİ ANAHTAR (hisse adları): Cemal DS7_ONAY.pdf'i işaretlemeden önce gösterilmez. GETİRİ YOK.",
         "esik_sha": _sha_esik7(), "kural_sha": _kural_sha7(), "ds6_onay_anahtar_sha": GU._sha(DS7_YOL["ds6_onay_anahtar"]),
         "havuz": havuz, "pdf_sha": GU._sha(yol), "pdf_bayt": boy, "sayfalar": sayfalar, "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(DS7_YOL["onay_anahtar"], J)
    d7log.info("onay PDF %s (%.2f MB): %s", yol, boy / 1e6, [(s["sayfa"], s["yanit_v6"], s["yanit"]["V1"]) for s in sayfalar])
    return J


# ================================================================ 4) TEST (sentetik seriler; gerçek veriden ÖNCE)
def ds7_cakisma_kontrol() -> None:
    ez = [k for k, v in _CK_ONCE_DS7.items() if k in globals() and id(globals()[k]) != v and not k.startswith("_")]
    if ez:
        raise DS7Hata(f"çakışma kapısı: bellekteki mevcut ad(lar) ezildi: {ez[:5]}")


# Ön kısım (d = 100, m = 20): büyük tepe (dizin 5, 170) -> ana zarf tepesi (dizin 30, 158,4) -> üçgen (ara trend 1: alçalan tepeler 140 / 134 / 128,
# dizin 45 / 60 / 75; ara trend 2: yükselen dipler 124 / 126, dizin 50 / 65) -> kırılım aşağı -> dip. Üçgen tepeleri ana zarfın çok altında.
_S7_X = [0, 5, 18, 30, 38, 45, 50, 60, 65, 75, 80, 99]
_S7_Y = [150.0, 170.0, 145.0, 158.4, 135.0, 140.0, 124.0, 134.0, 126.0, 128.0, 127.0, 101.0]
_S7_DUZ_X = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99]
_S7_DUZ_Y = [112.0, 113.0, 109.0, 111.0, 107.0, 109.0, 105.0, 107.0, 103.0, 104.5, 101.0]
# S6 / S7 ön kısmı: uzun düşen trend, tepeler aynı doğruda (dizin 5 / 25 / 45 / 65 / 85: 160 / 150 / 140 / 130 / 120; eğim -0,5 / mum),
# dipler 135 / 125 / 115 / 105 (dizin 15 / 35 / 55 / 75), dibe iniş 92 (dizin 99). Haber iğnesi dizin 57'den başlar (S6: 2 mum, S7: 5 mum).
_S7_UZ_X = [0, 5, 15, 25, 35, 45, 55, 65, 75, 85, 99]
_S7_UZ_Y = [150.0, 160.0, 135.0, 150.0, 125.0, 140.0, 115.0, 130.0, 105.0, 120.0, 92.0]
_S7_IGNE2 = {57: 143.0, 58: 142.5}
_S7_IGNE5 = {57: 143.0, 58: 142.6, 59: 142.2, 60: 141.8, 61: 141.4}


def _s7_taban(k: int, egim: float) -> Tuple[float, float, float, float]:
    """Yükselen mavi taban: gövde altı egim x k ATR; k = 3, 8, 13, 18 dokunuş; arada 0,8-1,2 ATR yukarıda."""
    off = egim * k + (0.02 if k in (3, 8, 13, 18) else 0.8 + 0.2 * (k % 3))
    return (off, 0.6 if k % 2 else -0.5, 0.15, 0.08)


def _s7_insa(knot_x: List[int], knot_y: List[float], post: List[Tuple[float, float, float, float]], son_fark: Optional[float] = None,
             cizgi: str = "ust", son_ust_fitil: float = 0.15, delin: Optional[Dict[int, float]] = None,
             tut: Optional[Dict[int, float]] = None, geo_j: Optional[int] = None) -> Tuple[np.ndarray, ...]:
    """ds6._insa6 ile 121 bar (m = 20). Son mumun kapanışı bir çizginin t'deki değerine göre (son_fark ATR; + üstünde, - altında) konur
    (gövde altı aynı kalır: mavi çizgi bozulmaz). cizgi: 'ust' = V1 ve V2 çizgilerinin üstteki, 'alt' = alttaki, 'geo' = i0'dan geo_j
    dizinindeki High'tan geçen doğru (kural seçiminden bağımsız). delin = {k: x}: dip sonrası k. mumun Low'u Low(d) - x ATR."""
    m = 20
    O, H, L, C = (a.copy() for a in D6._insa6(knot_x, knot_y, m, (0.6, -1, 0.2, 0.3), post, tut=tut))
    t = 120; d = t - m; s0 = 1
    # dipten önceki mumlar açılışı önceki kapanışla bu kapanışın ortasından yapar (tepeden sonraki mumun High'ı tepeye eşit 'ikiz' olmasın)
    O[1:d] = (C[0:d - 1] + C[1:d]) / 2.0; H[1:d] = np.maximum(O[1:d], C[1:d]) + 0.3; L[1:d] = np.minimum(O[1:d], C[1:d]) - 0.3
    atr = D5._atr5(O, H, L, C, d)
    if son_fark is not None:
        A = _ds7_ana_trend(H, C, s0, d, t, atr)
        if cizgi == "geo":
            i0 = int(A["i0_idx"]); ref = float(H[i0] + (H[geo_j] - H[i0]) / (geo_j - i0) * (t - i0))
        else:
            ref = (max if cizgi == "ust" else min)(float(A["T_t"]), float(A["T_z_t"]))
        b = min(O[t], C[t]); c = ref + son_fark * atr
        if c < b - 1e-9:
            raise DS7Hata("sentetik: son mum kapanışı gövde altının altına iniyor (mavi çizgi bozulur)")
        O[t] = b; C[t] = c
        H[t] = max(O[t], C[t]) + son_ust_fitil * atr; L[t] = min(O[t], C[t]) - 0.08 * atr
    for k, x in (delin or {}).items():
        L[d + k] = float(L[d]) - x * atr
    return O, H, L, C


def ds7_sentetik() -> Dict[str, Dict[str, Any]]:
    """S1-S7. dusen = V1'i düşürmesi beklenen parçalar (TAM küme)."""
    S: Dict[str, Dict[str, Any]] = {}
    taban = [_s7_taban(k, 0.25) for k in range(1, 21)]
    S["S1"] = {"tarif": "büyük tepe (t-115) -> ana zarf tepesi (t-90) -> üçgen (iki ara çizgi: alçalan tepeler t-75 / t-60 / t-45 ve yükselen "
                        "dipler) -> aşağı kırılım -> dip (t-20) -> yükselen mavi taban (4 dokunuş) -> son mum kapanışı ana çizginin 0,5 ATR üstünde",
               "seri": _s7_insa(_S7_X, _S7_Y, taban, son_fark=0.5), "beklenen": {"V1": True, "V2": True, "V3": True}, "dusen": [],
               "gerekce": "dip / mavi dört parça doğru; ana çizgi büyük tepeden (i0 = t-115) ana zarf tepesine (t-90): üçgenin ara tepelerinden "
                          "geçen adaylar ana tepe bölgesinde uzun delmeyle geçersiz; son kapanış çizginin üstünde -> V1 VAR (V2 aynı çizgi)",
               "i0_t": -115, "j_t": -90}
    S["S2"] = {"tarif": "S1 aynı ama son mum kapanışı ana çizginin 1 ATR altında (yalnız ara trendi, üçgenin alçalan tepeler çizgisini kırmış)",
               "seri": _s7_insa(_S7_X, _S7_Y, taban, son_fark=-1.0, cizgi="alt", son_ust_fitil=0.1),
               "beklenen": {"V1": False, "V2": False, "V3": True}, "dusen": ["KIRILIM"],
               "gerekce": "ara trend çizgisi esas alınmaz: ana çizgi kırılmadı -> V1 / V2 YOK; dip / mavi doğru -> V3 VAR", "i0_t": -115, "j_t": -90}
    s3 = [(0.02, 9.0, 0.2, 0.05)] + [(8.5 + 0.5 * ((k * 5) % 3), 0.5 if k % 2 else -0.5, 0.2, 0.1) for k in range(2, 21)]
    S["S3"] = {"tarif": "dipten sonra TEK büyük mumla sıçrama (9 ATR), sonra dokunuşsuz yukarıda gezinme; son kapanış ana çizginin üstünde",
               "seri": _s7_insa(_S7_X, _S7_Y, s3, son_fark=1.0), "beklenen": {"V1": False, "V2": False, "V3": False}, "dusen": ["P3"],
               "gerekce": "mavi çizgi yok (takip yok: tek dokunuş) -> P3 düşer -> V1 / V2 / V3 YOK"}
    S["S4"] = {"tarif": "düşüş yok (112 -> 101 dalgalı hafif düşüş, < %20), dip sonrası S1 tabanı (gövde altları iki çizginin de üstüne çıkıyor)",
               "seri": _s7_insa(_S7_DUZ_X, _S7_DUZ_Y, taban), "beklenen": {"V1": False, "V2": False, "V3": False},
               "dusen": ["P1"], "gerekce": "düşüşten dip yok (P1) -> YOK"}
    S["S5"] = {"tarif": "S1 aynı (son kapanış ana çizginin üstünde) ama dip sonrası 17. mumun (t-3) fitili dibi 0,8 ATR deliyor",
               "seri": _s7_insa(_S7_X, _S7_Y, taban, son_fark=0.5, delin={17: 0.8}), "beklenen": {"V1": False, "V2": False, "V3": False},
               "dusen": ["P4"], "gerekce": "dip delinmiş (P4) -> YOK (ana çizgi kırılmış olsa da)"}
    taban2 = [_s7_taban(k, 0.1) for k in range(1, 21)]
    S["S6"] = {"tarif": "uzun düşen trend: tepeler (t-115 / t-95 / t-75 / t-55 / t-35) aynı doğruda; ortada 2 mumluk haber iğnesi (t-63, t-62) "
                        "kapanışla çizgiyi ~8 puan delip geri dönüyor; dip (t-20), yatay-yükselen mavi taban, son kapanış dayanıklı çizginin "
                        "0,5 ATR üstünde ama iğne tepesinden geçen saf zarfın altında",
               "seri": _s7_insa(_S7_UZ_X, _S7_UZ_Y, taban2, son_fark=0.5, cizgi="geo", geo_j=85, tut=_S7_IGNE2),
               "beklenen": {"V1": True, "V2": False, "V3": True}, "dusen": [],
               "gerekce": "dayanıklı çizgi 4 tepeye değiyor, iğne kısa delme (2 mum, affedilir) -> seçilir, son kapanış üstünde -> V1 VAR; saf zarf "
                          "iğne tepesinden (t-63 / t-62) geçen daha yatık çizgi, son kapanış altında -> V2 YOK", "i0_t": -115, "dy_j_t": -35,
               "zarf_j_t": "iğne (t-63 / t-62)", "dokunus_n": 4, "kisa_n": 1}
    S["S7"] = {"tarif": "S6 aynı ama delme 5 mum sürüyor (t-63 .. t-59; uzun delme); son kapanış eski dayanıklı çizginin 0,5 ATR üstünde",
               "seri": _s7_insa(_S7_UZ_X, _S7_UZ_Y, taban2, son_fark=0.5, cizgi="geo", geo_j=85, tut=_S7_IGNE5),
               "beklenen": {"V1": False, "V2": False, "V3": True}, "dusen": ["KIRILIM"],
               "gerekce": "uzun delme affedilmez: tepelerden geçen çizgi geçersiz; geçerli tek aday iğne tepesinden geçen çizgi (saf zarfla neredeyse "
                          "aynı; zarf iğne mumlarından birine değer), son kapanış ikisinin de altında -> V1 / V2 YOK; dip / mavi doğru -> V3 VAR", "i0_t": -115, "zarf_j_t": "iğne (t-63 .. t-59)"}
    return S


def ds7_test() -> Dict[str, Any]:
    ds7_cakisma_kontrol()
    tablo = []
    SS = ds7_sentetik()
    for ad, s in SS.items():
        r = ds7_parca_dizi(*s["seri"])
        cik = {v: bool(r[v]) for v in ("V1", "V2", "V3")}
        esit = all(cik[v] == x for v, x in s["beklenen"].items()) and ds7_dusen(r) == s["dusen"]
        t = r["t_idx"]
        tablo.append({"seri": ad, "tarif": s["tarif"], "gerekce": s["gerekce"], "beklenen_V1": "VAR" if s["beklenen"]["V1"] else "YOK",
                      "beklenen_dusen": s["dusen"], "beklenen_ek": {v: ("VAR" if x else "YOK") for v, x in s["beklenen"].items() if v != "V1"},
                      "cikan": {v: ("VAR" if x else "YOK") for v, x in cik.items()}, "dusen": ds7_dusen(r),
                      **{p: r[p] for p in ("P1", "P2", "P3", "P4", "TREND", "KIRILIM", "TREND_Z", "KIRILIM_Z")}, "d": r["d_idx"] - t, "m": r["m"],
                      "dusus": round(r["dusus"], 3), "mavi_dusus_atr": round(r["mavi_dusus_atr"], 3), "dokunus_n": r["dokunus_n"],
                      "ilk": r["dokunus_ilk"], "ikinci": r["dokunus_ikinci"], "min_post_low_atr": round(r["min_post_low_atr"], 3),
                      "i0": r["i0_idx"] - t if r["i0_idx"] >= 0 else None, "jstar": r["jstar_idx"] - t if r["jstar_idx"] >= 0 else None,
                      "dy_j": r["dy_j_idx"] - t if r["dy_j_idx"] >= 0 else None, "dy_yok": r["dy_yok"], "dy_dokunus_n": r["dy_dokunus_n"],
                      "dy_kisa_n": r["dy_kisa_n"], "dy_aday_n": r["dy_aday_n"], "dy_gecerli_n": r["dy_gecerli_n"],
                      "egim_ana": round(r["egim_ana"], 4), "egim_z": round(r["egim_z"], 4), "T_t": round(r["T_t"], 3), "T_z_t": round(r["T_z_t"], 3),
                      "C_t": round(r["son_kapanis"], 3), "v6": "VAR" if r["v6_V1"] else "YOK", "esit": esit})
    bozuk = [x["seri"] for x in tablo if not x["esit"]]
    if bozuk:
        raise AssertionError(f"sentetik seriler beklenenden farklı: {bozuk}: " + json.dumps([x for x in tablo if not x["esit"]], ensure_ascii=False))
    T = {x["seri"]: x for x in tablo}
    # S1 / S2 / S5: ana çizgi büyük tepeden ana zarf tepesine; üçgenin ara tepeleri seçilmedi (V1 = V2 çizgisi)
    for ad in ("S1", "S2", "S5"):
        assert T[ad]["i0"] == -115 and T[ad]["jstar"] == -90 and T[ad]["dy_j"] == -90 and not T[ad]["dy_yok"], T[ad]
    # S2: ara trend (üçgenin alçalan tepeler çizgisi, 140 / 134 / 128 -> t'de) son kapanışın altında = ara trend kırıldı, ana çizgi kırılmadı
    O, H, L, C = SS["S2"]["seri"]; t = 120
    ara = [45, 60, 75]; ah = H[ara]; eg = (ah[-1] - ah[0]) / (ara[-1] - ara[0]); ara_t = ah[0] + eg * (t - ara[0])
    assert C[t] > ara_t and not T["S2"]["KIRILIM"], (C[t], ara_t, T["S2"])
    # S6: dayanıklı çizgi (4 tepe, 1 affedilen iğne) seçildi; saf zarf iğne tepesinden geçiyor
    x = T["S6"]
    assert x["i0"] == -115 and x["dy_j"] == -35 and x["dy_dokunus_n"] == 4 and x["dy_kisa_n"] == 1 and x["jstar"] in (-63, -62) and not x["dy_yok"], x
    # S7: uzun delme -> tepelerden geçen çizgi geçersiz; V1 çizgisi iğne tepesinden (saf zarfla aynı)
    x = T["S7"]
    assert x["i0"] == -115 and -63 <= x["jstar"] <= -59 and x["dy_j"] == -63 and x["dy_gecerli_n"] == 1 and not x["KIRILIM_Z"], x
    O, H, L, C = SS["S7"]["seri"]; r7 = ds7_parca_dizi(O, H, L, C)
    e_eski = (H[85] - H[5]) / 80.0
    k_, u_, _n = _ds7_delme(C, 5, r7["d_idx"], float(H[5]), float(e_eski), float(r7["atr_d"]))
    assert len(u_) == 1 and not k_ and C[120] > H[5] + e_eski * 115, (k_, u_)
    # tanım değişmezleri: [i0 .. d] aralığında hiçbir High saf zarfın üstünde değil; j*'de eşit; seçilen dayanıklı çizgi geçerli
    for ad, s in SS.items():
        O, H, L, C = s["seri"]; r = ds7_parca_dizi(O, H, L, C)
        if r["i0_idx"] >= 0:
            ii = np.arange(r["i0_idx"], r["d_idx"] + 1); Tz = r["i0_high"] + r["egim_z"] * (ii - r["i0_idx"])
            assert np.all(H[ii] <= Tz + 1e-9), ad
            assert abs(H[r["jstar_idx"]] - (r["i0_high"] + r["egim_z"] * (r["jstar_idx"] - r["i0_idx"]))) < 1e-9, ad
            assert r["i0_high"] == H[r["s0_idx"]:r["d_idx"]].max(), ad
            if not r["dy_yok"]:
                k_, u_, n_ = _ds7_delme(C, r["i0_idx"], r["d_idx"], r["i0_high"], r["egim_ana"], r["atr_d"])
                assert not u_ and n_ <= 2 and r["dy_j_idx"] in r["dy_dokunus"], ad
    # prefix değişmezliği: t sonrası veri değişince sonuç aynı (dizi ve DataFrame)
    rng = np.random.default_rng(11); n = 260
    Cx = 100 + np.cumsum(rng.normal(0, 1, n)); Ox = Cx + rng.normal(0, .3, n)
    Hx = np.maximum(Ox, Cx) + abs(rng.normal(0, .5, n)) + .1; Lx = np.minimum(Ox, Cx) - abs(rng.normal(0, .5, n)) - .1
    Cx, Ox, Hx, Lx = (a - min(Lx.min(), 0) + 5 for a in (Cx, Ox, Hx, Lx))
    for i in (150, 200, 230):
        s = slice(i - 120, i + 1)
        x1 = ds7_parca_dizi(Ox[s], Hx[s], Lx[s], Cx[s])
        O2, H2, L2, C2 = Ox.copy(), Hx.copy(), Lx.copy(), Cx.copy()
        O2[i + 1:] = 1; H2[i + 1:] = 2; L2[i + 1:] = 0.5; C2[i + 1:] = 1.5
        x2 = ds7_parca_dizi(O2[s], H2[s], L2[s], C2[s])
        assert json.dumps(x1, sort_keys=True) == json.dumps(x2, sort_keys=True), "DS7 t sonrasına bağlı"
    idx = pd.bdate_range("2020-01-01", periods=n)
    D1 = pd.DataFrame({"Open": Ox, "High": Hx, "Low": Lx, "Close": Cx}, index=idx)
    D2 = D1.copy(); D2.iloc[201:] = [1.0, 2.0, 0.5, 1.5]
    t_ = idx[200]
    y1 = ds7_parca(D1[D1.index <= t_].iloc[-121:]); y2 = ds7_parca(D2[D2.index <= t_].iloc[-121:])
    assert json.dumps(y1, sort_keys=True) == json.dumps(y2, sort_keys=True), "prefix (DataFrame) değişmezliği bozuk"
    # dip / mavi parçaları ds6 ile birebir (dondurulmuş)
    for ad, s in SS.items():
        r6 = D6.ds6_parca_dizi(*s["seri"]); r7 = ds7_parca_dizi(*s["seri"])
        assert all(bool(r6[k]) == bool(r7[k]) for k in ("P1", "P2", "P3", "P4")) and r7["V3"] == bool(r6["P1"] and r6["P2"] and r6["P3"] and r6["P4"]), ad
    # pencere boyu ve geçersiz bar denetimi
    for bozuk_ in ((Ox[:100], Hx[:100], Lx[:100], Cx[:100]), (Ox[:121], Lx[:121], Hx[:121], Cx[:121])):
        try:
            ds7_parca_dizi(*bozuk_); raise AssertionError("bozuk pencere kabul edildi")
        except DS7Hata:
            pass
    assert ds7_hukum(0.7, 0.45, 79) == "YARI BAĞIMSIZ GEÇERLİ" and ds7_hukum(0.7, 0.3, 79) == "KISMEN"
    assert ds7_hukum(0.5, 0.2, 79) == "KISMEN" and ds7_hukum(0.3, 0.1, 79) == "GEÇERSİZ" and ds7_hukum(0.9, 0.8, 20).startswith("ÖLÇÜLEMEDİ")
    return {"tamam": True, "kural_sha": _kural_sha7(), "esik_sha": _sha_esik7(), "tablo": tablo}


# ================================================================ 5) MÜHÜR
DS7_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralın uyumu, kappa)"),
    "K2": ("EVET", "bütün parçalar yalnız kör sayfa penceresinden: tanim2.tz_pencere (veri t'de KESİK, 121 bar) + ds5_pencere mekanik denetimi "
                   "(W.index.max() <= t, W.index[-1] == t, 121 bar); ana trend çizgileri (dayanıklı + saf zarf), pivot tepeler (j+5 <= d) ve delme "
                   "öbekleri yalnız [t-119 .. d] High / Close'larından, kırılım yalnız C_t; ds7.py test prefix değişmezliği (3 kesik + DataFrame); getiri / sinyal sonrası fiyat okunmaz; kör set işaretleri ve "
                   "*SONUC* dosyaları mühürden önce açılmadı (olc açılış zamanı DS7_SONUC'ta); cemal_ds6_onay.json / cemal_ds5_onay.json (tanım "
                   "geri bildirimi, kör set etiketi değil) iş tanımı izniyle okundu"),
    "K3": ("EVET", "GE.ge_hazir geçerli bar (goz_uyum ile aynı); ds7_parca_dizi -> ds6 -> ds5_parca_dizi NaN / H <= L / L <= 0 görürse durur "
                   "(testte sınandı)"),
    "K4": ("EVET", "80 sayfa set 1 + set 2 ile aynı (aynı hissede en çok 1 sayfa); görsel onay 36 sayfası bilerek DS6_ONAY ile aynı hisse / gün "
                   "(onay amaçlı, kör değil)"),
    "K5": ("UYGULANMAZ", "giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik"),
    "K6": ("EVET", "tek kip V_*.pkl (goz_uyum ile aynı); düşüş oranı birimsiz, mavi çizgi / dokunuş / delinme ATR14(d) biriminde; zarf fiyat "
                   "biriminde ama karar yalnız işaret (s < 0, C_t > T(t)); birim bağımsız"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok"),
    "K8": ("EVET", "79-80 karar (iki set); karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); 3 varyant: Bonferroni 3 (%98,33) V2 / V3 için; "
                   "hüküm yalnız V1 ve 'YARI BAĞIMSIZ' (kural Cemal'in DS5 / DS6 onay işaretlerinden; iki set önceki DS3-DS6 işlerinde kullanıldı); "
                   "set 1 ve set 2 ayrı; kural kör set etiketlerinden SEÇİLMEDİ; kesin hüküm bağımsız üçüncü kör setle; DS6 onay 17 sayfa "
                   "tablosu yalnız bilgi"),
    "K9": ("EVET", "kural + DS7_ESIK + sentetik test ADIM 1'de kör set etiketleri açılmadan commit; 80 yanıt ds7_anahtar.json + görsel onay "
                   "(DS7_ONAY.pdf, ds7_onay_anahtar.json) etiket açılmadan mühürlü; ds7.py + ds6.py + ds5.py + ds7_anahtar.json + DS7_ESIK + kural "
                   "kaynağı + PDF + onay anahtarı sha'ları bu dosyada; olc sha'ları denetler ve 80 yanıtı veriden yeniden hesaplayıp mühürle "
                   "karşılaştırır; hüküm eşikleri sabit"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırma yok; yalnız OHLCV"),
    "K11": ("EVET", "ds7.py anahtar / onay aynı komutla deterministik yeniden üretilir (seçim yok; 36 sayfa ds6_onay_anahtar.json'dan; havuz sha "
                    "DS6 havuzuyla eşit şartı); P1-P4 ve v6 / DS5 V1 ds6_anahtar.json mühürlü değerlerle ve onay sayfalarında v6 V1 "
                    "ds6_onay_anahtar.json ile eşit şartı; olc 80 sayfanın yanıtını veriden yeniden hesaplar, mühürle eşitliğini şart koşar; "
                    "sentetik seriler beklenen yanıt ve düşen parçayla birebir"),
    "K12": ("EVET", "iddia yok; yalnız 'uyum' ve 'kappa' sayısı; hüküm sözü yalnız ön kayıttaki eşikle ve yalnız V1 için; 'YARI BAĞIMSIZ' sınırı yazılı"),
    "K13": ("EVET", "çakışma kapısı _CK_ONCE_DS7 + test; yasak dosyalar (defter, mevcut .py dahil ds5.py / ds6.py, anahtar / ön kayıt / sonuç "
                    "dosyaları) değişmedi (git diff boş); e-posta / anahtar yok (_yaz / _jyaz e-posta taraması); git add -A yok; PDF Cemal'e "
                    "gönderilmedi"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


def _sentetik_tablo7(T: Dict[str, Any]) -> List[str]:
    st = ["| seri | tarif | beklenen V1 (düşen); V2 / V3 | gerekçe | çıkan V1 / V2 / V3 | P1 (düşüş) | P2' (mavi düşüş ATR) | P3 (dokunuş ilk / "
          "ikinci) | P4 | TREND | KIRILIM | TREND_Z | KIRILIM_Z | i0 / dayanıklı j (dokunuş; kısa delme; aday / geçerli) / zarf j* | "
          "T(t) / T_z(t) / C_t | v6 V1 | eşit |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in T["tablo"]:
        b = x["beklenen_V1"] + (f" ({', '.join(x['beklenen_dusen'])})" if x["beklenen_dusen"] else "") + \
            ("; " + ", ".join(f"{k} {v}" for k, v in x["beklenen_ek"].items()) if x["beklenen_ek"] else "")
        c = " / ".join(x["cikan"][v] for v in ("V1", "V2", "V3"))
        zz = (f"t{x['i0']:+d} / " + (f"t{x['dy_j']:+d}" if x["dy_j"] is not None else "yok") +
              f" ({x['dy_dokunus_n']}; {x['dy_kisa_n']}; {x['dy_aday_n']} / {x['dy_gecerli_n']}) / t{x['jstar']:+d}") if x["i0"] is not None else "-"
        st.append(f"| {x['seri']} | {x['tarif']} | {b} | {x['gerekce']} | {c} | {_isr7(x['P1'])} (%{x['dusus']*100:.0f}) | "
                  f"{_isr7(x['P2'])} ({x['mavi_dusus_atr']:.2f}) | {_isr7(x['P3'])} ({x['dokunus_n']}: {x['ilk']} / {x['ikinci']}) | {_isr7(x['P4'])} | "
                  f"{_isr7(x['TREND'])} | {_isr7(x['KIRILIM'])} | {_isr7(x['TREND_Z'])} | {_isr7(x['KIRILIM_Z'])} | {zz} | "
                  f"{x['T_t']:.2f} / {x['T_z_t']:.2f} / {x['C_t']:.2f} | {x['v6']} | "
                  f"{'EVET' if x['esit'] else 'HAYIR'} |")
    return st


def ds7_muhur() -> str:
    for y in (DS7_YOL["anahtar"], DS7_YOL["is_tanimi"], DS7_YOL["pdf"], DS7_YOL["onay_anahtar"]):
        if not os.path.exists(y):
            raise DS7Hata(f"mühür için dosya yok: {y}")
    J = json.load(open(DS7_YOL["anahtar"], encoding="utf-8")); JO = json.load(open(DS7_YOL["onay_anahtar"], encoding="utf-8"))
    for ad, X in (("anahtar", J), ("onay", JO)):
        if X["esik_sha"] != _sha_esik7():
            raise DS7Hata(f"DS7_ESIK {ad} dosyasından sonra değişmiş")
        if X["kural_sha"] != _kural_sha7():
            raise DS7Hata(f"kural kaynağı {ad} dosyasından sonra değişmiş")
    if JO["pdf_sha"] != GU._sha(DS7_YOL["pdf"]):
        raise DS7Hata("DS7_ONAY.pdf onay anahtarından sonra değişmiş")
    T = ds7_test()
    ad = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
          "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
          "K13": "süreç", "K14": "boyut (gerçek para)"}
    tab = "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |\n|---|---|---|---|\n"
    for k, (yy, kn) in DS7_KONTROL.items():
        tab += f"| {k} | {ad[k]} | {yy} | {kn} |\n"
    st = _sentetik_tablo7(T)
    oz = J["ozet"]
    ot = ["| küme | n | P1 | P2' | P3 | P4 | dip / mavi (V3) | TREND | KIRILIM | TREND_Z | KIRILIM_Z | dayanıklı yok | V1 çizgisi = zarf | "
          "V1 VAR | V2 VAR | v6 V1 VAR | DS5 V1 VAR | TREND ama T(t) <= 0 |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k_, o in oz.items():
        ot.append(f"| {k_} | {o['n']} | {o['P1_DOGRU']} | {o['P2_DOGRU']} | {o['P3_DOGRU']} | {o['P4_DOGRU']} | {o['DIPMAVI_DOGRU']} | "
                  f"{o['TREND_DOGRU']} | {o['KIRILIM_DOGRU']} | {o['TREND_Z_DOGRU']} | {o['KIRILIM_Z_DOGRU']} | {o['dy_yok_DOGRU']} | "
                  f"{o['ayni_cizgi_DOGRU']} | {o['V1_VAR']} | {o['V2_VAR']} | {o['v6_V1_VAR']} | "
                  f"{o['ds5_V1_VAR']} | {o['T_t_pozitif_degil']} |")
    on = ["| sayfa | pazar | v6 grup | v6 V1 | v7 V1 | V2 (zarf) | V3 (dip / mavi) | TREND | KIRILIM (C_t / T(t) - 1) | i0 / dayanıklı j "
          "(dokunuş; affedilen) / zarf j* (t'ye göre) | kırılım (t'ye göre; üst kapanış) | v6 Ha (t'ye göre) | düşen parça |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in JO["sayfalar"]:
        t = int(s["t_idx"])
        zz = (f"t{s['i0_idx'] - t:+d} / " + (f"t{s['dy_j_idx'] - t:+d}" if not s["dy_yok"] else "yok (zarf)") +
              f" ({s['dy_dokunus_n']}; {s['dy_kisa_n']}) / t{s['jstar_idx'] - t:+d}") if s["i0_idx"] >= 0 else "-"
        kb = f"t{s['kirilim_idx'] - t:+d} ({s['ust_kapanis_n']})" if s["kirilim_idx"] >= 0 else f"- ({s['ust_kapanis_n']})"
        oran = s["kapanis_T_oran"]
        on.append(f"| {s['sayfa']} | {s['pazar']} | {s['grup_v6']} | {s['yanit_v6']} | {s['yanit']['V1']} | {s['yanit']['V2']} | "
                  f"{s['yanit']['V3']} | {_isr7(s['TREND'])} | {_isr7(s['KIRILIM'])} ({'-' if oran is None else f'%{oran*100:+.1f}'}) | {zz} | "
                  f"{kb} | {('t%+d' % (s['v6_ha_idx'] - t)) if s['v6_ha_idx'] >= 0 else '-'} | {', '.join(s['V1_dusen']) or '-'} |")
    hv = JO["havuz"]
    bel = "\n".join(f"- {k}: {v}" for k, v in DS7_ESIK["ana_trend"].items())
    m = f"""# DİP SAVUNMASI v7 (DS7) — ÖN KAYIT (Cemal'in kör set işaretleri AÇILMADAN mühürlenir)

Üretim: {GU._simdi()} (UTC). Soru: dip / mavi parçaları (DS5 + DS6 D3; Cemal'in onayladığı hali, DONDURULMUŞ) + DAYANIKLI ANA TREND kırılımı (dibe inişten önceki en yüksek tepeden başlayan, en çok tepeye değen, kısa haber iğnelerini affeden çizgi; son kapanış üstünde), iki kör sette (GOZ_UYUM_KOR.pdf = set 1, TANIM2_KOR.pdf = set 2; 80 sayfa) Cemal'in VAR / YOK işaretleriyle örtüşüyor mu? Ayrıca DS6_ONAY'ın aynı 36 sayfalık GÖRSEL ONAY PDF'i (Cemal'e gönderilmedi). GETİRİ ÖLÇÜLMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/ds7_anahtar.json` sha256: `{GU._sha(DS7_YOL['anahtar'])}`
- kod: `arastirma_cikti/goz_uyum/ds7.py` sha256: `{GU._sha(DS7_YOL['kod'])}`
- içe alınan kural kodu: `arastirma_cikti/goz_uyum/ds6.py` sha256: `{GU._sha(DS7_YOL['ds6_kod'])}` (değiştirilmedi)
- içe alınan kural kodu: `arastirma_cikti/goz_uyum/ds5.py` sha256: `{GU._sha(DS7_YOL['ds5_kod'])}` (değiştirilmedi)
- eşik sözlüğü (DS7_ESIK) sha256: `{_sha_esik7()}`
- kural kaynağı (_ds7_ana_trend + ds7_parca_dizi + ds7_parca + DS6 kural sha) sha256: `{_kural_sha7()}`
- görsel onay PDF: `arastirma_cikti/goz_uyum/DS7_ONAY.pdf` sha256: `{GU._sha(DS7_YOL['pdf'])}`
- görsel onay anahtarı: `arastirma_cikti/goz_uyum/ds7_onay_anahtar.json` sha256: `{GU._sha(DS7_YOL['onay_anahtar'])}`
- iş tanımı: `arastirma_cikti/goz_uyum/DS7_IS_TANIMI.md` sha256: `{GU._sha(DS7_YOL['is_tanimi'])}`
- girdi (yalnız sayfa -> pazar, sembol, sinyal günü okundu): goz_uyum_anahtar.json `{J['girdi_sha']['goz_uyum_anahtar.json']}`, tanim2_anahtar.json `{J['girdi_sha']['tanim2_anahtar.json']}`; P1-P4 / v6 denetimi ds6_anahtar.json `{J['girdi_sha']['ds6_anahtar.json']}`; onay: ds6_onay_anahtar.json `{JO['ds6_onay_anahtar_sha']}`; tanım geri bildirimi cemal_ds6_onay.json `{GU._sha(DS7_YOL['cemal_ds6_onay'])}`, cemal_ds5_onay.json `{GU._sha(DS7_YOL['cemal_ds5_onay'])}`
- olay havuzu (pazar, sembol, tarih) sha256: `{hv['havuz_sha']}` (DS4 / DS5 / DS6 görsel onay havuzuyla aynı)
- bağımlı kod: goz_uyum.py `{GU._sha(GU.GU_YOL['kod'])[:16]}`, tanim2.py `{GU._sha(TZ.TZ_YOL['kod'])[:16]}`

## 2. Kural (ADIM 1'de, kör set etiketleri açılmadan commit; iş tanımından aynen)
- **DİP / MAVİ (DONDURULMUŞ)**: {DS7_ESIK['dip_mavi']}.
- **i0**: d'den önceki pencere kısmında en yüksek High (eşitte en erken).
- **V1 DAYANIKLI ANA TREND (iş tanımı EK'i, Cemal 23 Kas)**: aday = i0'dan ve i0'dan sonraki her pivot tepeden (5/5) geçen doğru (eğim < 0); DOKUNUŞ = çizgiye 0,5 ATR'den yakın pivot tepe sayısı; DELME = kapanışın çizginin 0,25 ATR üstüne çıktığı ardışık öbek; KISA DELME (<= 3 mum ve sonra kapanış çizgi altına döner; haber iğnesi, affedilir) / UZUN DELME (affedilmez); geçerli = uzun delme yok ∧ kısa delme <= 2; seçim en çok dokunuş > az kısa delme > j sağda; geçerli aday yoksa saf zarf ('dayanıklı çizgi yok').
- **V2 SAF ZARF (parametresiz)**: s = max_(i0 < j <= d) (High_j - High_i0) / (j - i0); j* = argmax; T_z(i) = High_i0 + s (i - i0), t'ye uzatılır.
- **KIRILIM**: her ikisinde C_t > çizgi(t) (tek kapanış yeter; DS6'daki '>= 3 kapanış' ve 'kırılımdan sonra dokunuş' şartları YOK).
- **V1 (ANA)** = P1 ∧ P2' ∧ P3 ∧ P4 ∧ TREND (dayanıklı eğim < 0) ∧ KIRILIM. **V2** = P1 ∧ P2' ∧ P3 ∧ P4 ∧ TREND_Z ∧ KIRILIM_Z (saf zarf). **V3** = yalnız dip / mavi (P1 ∧ P2' ∧ P3 ∧ P4). Bonferroni 3.

Tanım belirsizliklerinin çözümü (kör set etiketlerinden önce yazıldı):
{bel}

DS7_ESIK (tam): `{json.dumps(DS7_ESIK, ensure_ascii=False, sort_keys=True)}`

## 3. Sentetik sınama (`python arastirma_cikti/goz_uyum/ds7.py test`; gerçek veriden ÖNCE; dizinler t'ye göre)
{chr(10).join(st)}

Ek testler: S1 / S2 / S5'te i0 = t-115 (büyük tepe), dayanıklı j = zarf j* = t-90 (ana tepe; üçgenin ara tepeleri değil); S2'de son kapanış üçgenin alçalan tepeler çizgisinin (ara trend) t'deki uzantısının ÜSTÜNDE ama ana çizginin altında; S6'da dayanıklı çizgi 4 tepe dokunuşu + 1 affedilen iğne ile seçildi, zarf iğneden geçiyor; S7'de tepelerden geçen çizgide tek UZUN delme (geçersiz), V1 çizgisi iğne pivotundan (tek geçerli aday); tanım değişmezleri ([i0 .. d] High'ları zarfın üstüne çıkmaz, j*'de eşit, High_i0 = pencerenin d öncesi en yüksek High'ı, seçilen dayanıklı çizgide uzun delme yok ve kısa delme <= 2); dip / mavi parçaları ds6 ile birebir; prefix değişmezliği (3 kesik, dizi + DataFrame); kısa pencere ve H <= L penceresi reddedilir; hüküm fonksiyonu. Sonuç: {sum(x['esit'] for x in T['tablo'])} / {len(T['tablo'])} seri beklenene (V1 / V2 / V3 ve düşen parça kümesi) eşit.

## 4. Mühürlü yanıtlar (ds7_anahtar.json 'sayfalar'; Cemal'in işaretleri AÇILMADAN yazıldı)
{chr(10).join(ot)}

## 5. Görsel onay PDF'i (DS7_ONAY.pdf; DS6_ONAY ile aynı 36 sayfa, aynı sıra; anahtar ds7_onay_anahtar.json)
{chr(10).join(on)}

Havuz (bilgi; DS4-DS6 görsel onay havuzu, {hv['havuz_n']} olay {json.dumps(hv['havuz_pazar'], ensure_ascii=False)}): V1 VAR {json.dumps(hv['V1_VAR'], ensure_ascii=False)} (toplam {hv['toplam']['V1']}); V2 VAR toplam {hv['toplam']['V2']}; V3 (dip / mavi) VAR toplam {hv['toplam']['V3']}; v6 V1 VAR toplam {hv['toplam']['v6_V1']}; V1 VAR ama T(t) <= 0: {hv['V1_T_t_pozitif_degil']}.

## 6. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in set 1 (cemal_isaret.json) ve set 2 (cemal_isaret2.json) VAR / YOK işaretleri ile V1 / V2 / V3 arasında uyum ve Cohen kappa; set 1, set 2 ve birleşik; işaretsiz / '?' sayfa karar dışı, sayısı ayrıca yazılır.
- Aralık: kappa bootstrap (B {DS7_ESIK['kappa']['B']}, tohum {DS7_ESIK['kappa']['tohum']}, sayfa yeniden örneklemesi, yüzdelik): V1 için %95; V2 / V3 için Bonferroni 3 ile %98,33 (ayrıca %95 bilgi).
- HÜKÜM: {DS7_ESIK['hukum']}.
- Ek bilgi (hüküm dışı): uyuşmayan sayfalar ve düşen parça (P1 / P2 / P3 / P4 / TREND / KIRILIM); Cemal VAR / kod YOK sayfalarda düşen parça sayımı; DS6 V1, DS5 V1 ve GOVDE_1 ile aynı sayfalarda karşılaştırma; DS6_ONAY 17 işaretli sayfada v7 cevabı ({DS7_ESIK['onay17']['eslem']}).
- Kural ve eşik sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 7. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
{tab}
## 8. Git kaydı (bu dosyanın yazıldığı an)
- ds7.py: {GU._gu_git('arastirma_cikti/goz_uyum/ds7.py')}
- DS7_IS_TANIMI.md: {GU._gu_git('arastirma_cikti/goz_uyum/DS7_IS_TANIMI.md')}
"""
    GU._yaz(DS7_YOL["onkayit"], m)
    import IZ_KARNE as IK
    r = IK.ik_kontrol_kapisi(DS7_YOL["onkayit"])
    d7log.info("kontrol kapısı: %s", "GEÇTİ" if r["gecti"] else r)
    return DS7_YOL["onkayit"]


def _ds7_muhur_oku() -> Dict[str, str]:
    if not os.path.exists(DS7_YOL["onkayit"]):
        raise DS7Hata("ön kayıt yok")
    t = open(DS7_YOL["onkayit"], encoding="utf-8").read(); out = {}
    for ad, desen in (("anahtar", r"ds7_anahtar\.json` sha256: `([0-9a-f]{64})`"), ("kod", r"ds7\.py` sha256: `([0-9a-f]{64})`"),
                      ("ds6kod", r"ds6\.py` sha256: `([0-9a-f]{64})`"), ("ds5kod", r"ds5\.py` sha256: `([0-9a-f]{64})`"),
                      ("esik", r"eşik sözlüğü \(DS7_ESIK\) sha256: `([0-9a-f]{64})`"), ("kural", r"kural kaynağı \([^)]*\) sha256: `([0-9a-f]{64})`"),
                      ("pdf", r"DS7_ONAY\.pdf` sha256: `([0-9a-f]{64})`"), ("onay", r"ds7_onay_anahtar\.json` sha256: `([0-9a-f]{64})`")):
        mm = re.search(desen, t)
        if not mm:
            raise DS7Hata(f"ön kayıtta {ad} sha'sı yok")
        out[ad] = mm.group(1)
    return out


# ================================================================ 6) ÖLÇÜM
def ds7_hukum(k: float, alt: float, n: int) -> str:
    E = DS7_ESIK["kappa"]
    if n < int(E["karar_min"]) or not np.isfinite(k):
        return "ÖLÇÜLEMEDİ (karar sayısı < 30 ya da kappa tanımsız)"
    if k >= E["gecerli"] and np.isfinite(alt) and alt >= E["gecerli_alt"]:
        return "YARI BAĞIMSIZ GEÇERLİ"
    return "KISMEN" if k >= E["kismen"] else "GEÇERSİZ"


def _onay17_tablo(JO: Dict[str, Any]) -> Dict[str, Any]:
    """DS6_ONAY sayfaları: Cemal'in genel işareti (cemal_ds6_onay.json) ile v6 -> v7 V1 (ön kayıttaki eşleme; BİLGİ)."""
    CJ = json.load(open(DS7_YOL["cemal_ds6_onay"], encoding="utf-8"))
    E = DS7_ESIK["onay17"]; out = []
    for s in JO["sayfalar"]:
        no = int(s["sayfa"]); c = CJ.get(str(no), {}); ci = str(c.get("genel", "?"))
        v6, v7 = bool(s["v6_V1"]), bool(s["V1"]); deg = v6 != v7
        if no in E["YANLIS"]:
            if ci != "YANLIŞ":
                raise DS7Hata(f"onay sayfa {no}: iş tanımında YANLIŞ, cemal_ds6_onay.json'da {ci}")
            bek = not v6; et = "itiraz giderildi" if deg else "itiraz sürüyor"
        elif no in E["DOGRU"]:
            if ci != "DOĞRU":
                raise DS7Hata(f"onay sayfa {no}: iş tanımında DOĞRU, cemal_ds6_onay.json'da {ci}")
            bek = v6; et = "korundu" if not deg else "DİKKAT: bozuldu"
        else:
            bek = None; et = "işaretsiz" + (" (yanıt değişti)" if deg else "")
        t = int(s["t_idx"])
        out.append({"sayfa": no, "pazar": s["pazar"], "cemal": ci, "yazi": c.get("yazi", ""), "v6_V1": "VAR" if v6 else "YOK",
                    "v7_V1": "VAR" if v7 else "YOK", "v7_V2": "VAR" if s["V2"] else "YOK", "v7_V3": "VAR" if s["V3"] else "YOK",
                    "degisti": deg, "cemal_bekledigi": (None if bek is None else ("VAR" if bek else "YOK")),
                    "uyumlu": (None if bek is None else bool(v7 == bek)), "etiket": et, "dusen": s["V1_dusen"],
                    "oran": s["kapanis_T_oran"], "kirilim_t": (int(s["kirilim_idx"]) - t) if int(s["kirilim_idx"]) >= 0 else None,
                    "i0_t": (int(s["i0_idx"]) - t) if int(s["i0_idx"]) >= 0 else None,
                    "jstar_t": (int(s["jstar_idx"]) - t) if int(s["jstar_idx"]) >= 0 else None,
                    "dy_j_t": (int(s["dy_j_idx"]) - t) if int(s["dy_j_idx"]) >= 0 else None, "dy_yok": bool(s["dy_yok"]),
                    "dy_dokunus_n": int(s["dy_dokunus_n"]), "dy_kisa_n": int(s["dy_kisa_n"])})
    isl = [z for z in out if z["uyumlu"] is not None]
    return {"satir": out, "isaretli_n": len(isl), "uyumlu_n": int(sum(z["uyumlu"] for z in isl)),
            "YANLIS_uyumlu": int(sum(z["uyumlu"] for z in isl if z["cemal"] == "YANLIŞ")), "YANLIS_n": len(E["YANLIS"]),
            "DOGRU_uyumlu": int(sum(z["uyumlu"] for z in isl if z["cemal"] == "DOĞRU")), "DOGRU_n": len(E["DOGRU"]),
            "v6_uyumlu_n": int(sum(1 for z in isl if z["cemal"] == "DOĞRU"))}


def ds7_olc(deneme: bool = False, cemal1: Optional[str] = None, cemal2: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    if not deneme:
        M = _ds7_muhur_oku()
        for ad, gercek in (("anahtar", GU._sha(DS7_YOL["anahtar"])), ("kod", GU._sha(DS7_YOL["kod"])), ("ds6kod", GU._sha(DS7_YOL["ds6_kod"])),
                           ("ds5kod", GU._sha(DS7_YOL["ds5_kod"])), ("esik", _sha_esik7()), ("kural", _kural_sha7()),
                           ("pdf", GU._sha(DS7_YOL["pdf"])), ("onay", GU._sha(DS7_YOL["onay_anahtar"]))):
            if gercek != M[ad]:
                raise DS7Hata(f"MÜHÜR BOZUK: {ad} sha'sı ön kayıttakiyle aynı değil -> DURDU")
    J = json.load(open(DS7_YOL["anahtar"], encoding="utf-8"))
    Sm = pd.DataFrame(J["sayfalar"])
    R = ds7_hesap(Sm[["set", "sayfa", "pazar", "sembol", "sinyal_gunu"]])     # K11: yanıtlar veriden yeniden hesaplanır
    for v in ("V1", "V2", "V3", "P1", "P2", "P3", "P4", "TREND", "KIRILIM", "TREND_Z", "KIRILIM_Z", "dy_yok", "v6_V1", "ds5_V1"):
        if (R[v].to_numpy(bool) != Sm[v].to_numpy(bool)).any():
            raise DS7Hata(f"{v} yanıtları veriden yeniden hesaplanınca mühürle aynı değil -> DURDU")
    acilis = GU._simdi()
    c1 = cemal1 or DS7_YOL["set1_cemal"]; c2 = cemal2 or DS7_YOL["set2_cemal"]
    et = {1: D5._etiket_oku5(c1), 2: D5._etiket_oku5(c2)}
    d7log.info("etiket dosyaları açıldı: %s (UTC)", acilis)
    for st in (1, 2):
        fazla = sorted(set(et[st]) - set(range(1, 41)))
        if fazla:
            raise DS7Hata(f"set {st} etiketinde anahtarda olmayan sayfa: {fazla}")
    Sm["cemal"] = [et[int(s)].get(int(p), "?") for s, p in zip(Sm.set, Sm.sayfa)]
    Sm["DS6_V1"] = Sm["v6_V1"].astype(bool); Sm["DS5_V1"] = Sm["ds5_V1"].astype(bool)
    E = DS7_ESIK["kappa"]; bon = 1 - (1 - E["guven"]) / E["bonferroni_k"]
    if deneme:
        g1k = {"ozellik": "G1_govde_dokunus_n", "yon": ">=", "esik": 3.0, "not": "DENEME: uydurma kural"}
    else:
        GJ = json.load(open(DS7_YOL["govde_anahtar"], encoding="utf-8")); g1k = dict(GJ["kurallar"]["GOVDE_1"]); del GJ
    Sm["GOVDE_1"] = D5._govde1_cevap5(Sm, g1k)
    kumeler = {"set 1": Sm.set == 1, "set 2": Sm.set == 2, "birleşik": Sm.set > 0}
    sonuc: Dict[str, Any] = {"etiket_acilis_utc": acilis, "deneme": deneme, "n_sayfa": int(len(Sm)), "kume": {}, "govde_kural": g1k}
    modeller = ("V1", "V2", "V3", "DS6_V1", "DS5_V1", "GOVDE_1")
    for kad, km in kumeler.items():
        K = Sm[km & (Sm.cemal != "?")]; cb = (K.cemal == "VAR").to_numpy(bool); n = len(K)
        kd: Dict[str, Any] = {"karar_n": int(n), "isaretsiz": int((km & (Sm.cemal == "?")).sum()),
                              "isaretsiz_sayfa": [f"set {s} / {p}" for s, p in zip(Sm[km & (Sm.cemal == '?')].set, Sm[km & (Sm.cemal == '?')].sayfa)],
                              "cemal_VAR": int(cb.sum()), "model": {}}
        for v in modeller:
            mod = K[v].to_numpy(bool)
            k = GU.gu_kappa(cb, mod)
            ar = D5._boot5(cb, mod, int(E["B"]), int(E["tohum"]), (E["guven"], bon)) if n else {}
            tp, tn = int((cb & mod).sum()), int((~cb & ~mod).sum()); fp, fn = int((~cb & mod).sum()), int((cb & ~mod).sum())
            a95 = ar.get(f"{E['guven']:.4f}", [np.nan, np.nan]); abn = ar.get(f"{bon:.4f}", [np.nan, np.nan])
            huk = (ds7_hukum(k, a95[0], n) if v == "V1" else
                   ("BİLGİ (Bonferroni alt uç ile: " + ds7_hukum(k, abn[0], n) + ")" if v in ("V2", "V3") else "BİLGİ (önceki kural)"))
            kd["model"][v] = {"kod_VAR": int(mod.sum()), "uyum": float(np.mean(cb == mod)) if n else np.nan, "kappa": k, "ar95": a95,
                              "ar_bon": abn, "hukum": huk,
                              "tablo": {"Cemal VAR + kod VAR": tp, "Cemal YOK + kod YOK": tn, "Cemal YOK + kod VAR": fp, "Cemal VAR + kod YOK": fn},
                              "uyusmayan": [f"set {s} / {p}" for s, p in zip(K.set[cb != mod], K.sayfa[cb != mod])]}
        sonuc["kume"][kad] = kd
    pl = ["P1", "P2", "P3", "P4", "TREND", "KIRILIM"]
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
                   "m": int(r.m), "dusus": float(r.dusus), "mavi_dusus_atr": float(r.mavi_dusus_atr), "dokunus_n": int(r.dokunus_n),
                   "dokunus_ilk": int(r.dokunus_ilk), "dokunus_ikinci": int(r.dokunus_ikinci), "min_post_low_atr": float(r.min_post_low_atr),
                   "i0_t": (int(r.i0_idx) - int(r.t_idx)) if int(r.i0_idx) >= 0 else None,
                   "jstar_t": (int(r.jstar_idx) - int(r.t_idx)) if int(r.jstar_idx) >= 0 else None,
                   "dy_j_t": (int(r.dy_j_idx) - int(r.t_idx)) if int(r.dy_j_idx) >= 0 else None, "dy_dokunus_n": int(r.dy_dokunus_n),
                   "dy_kisa_n": int(r.dy_kisa_n), "dy_yok": bool(r.dy_yok),
                   "oran": (float(r.kapanis_T_oran) if r.kapanis_T_oran is not None and np.isfinite(float(r.kapanis_T_oran)) else None),
                   "kirilim_t": (int(r.kirilim_idx) - int(r.t_idx)) if int(r.kirilim_idx) >= 0 else None, "ust_kapanis_n": int(r.ust_kapanis_n),
                   "dusen": ds7_dusen(rd), "neden": ds7_neden_metni(rd)})
    sonuc["V1_uyusmayan"] = uy
    K = Sm[Sm.cemal != "?"]; cv = (K.cemal == "VAR")
    sonuc["karsilastirma"] = {f"V1_{o}": {"iki_kod_ayni_yanit": int((K.V1.astype(bool) == K[o].astype(bool)).sum()), "karar_n": int(len(K)),
                                          "kod_kappa": GU.gu_kappa(K.V1.to_numpy(bool), K[o].to_numpy(bool)),
                                          "V1_dogru_oteki_yanlis": int(((K.V1.astype(bool) == cv) & (K[o].astype(bool) != cv)).sum()),
                                          "oteki_dogru_V1_yanlis": int(((K.V1.astype(bool) != cv) & (K[o].astype(bool) == cv)).sum())}
                              for o in ("DS6_V1", "DS5_V1", "GOVDE_1")}
    sonuc["V1_DS6_degisen"] = [{"sayfa": f"set {r.set} / {r.sayfa}", "cemal": r.cemal, "DS6": "VAR" if r.DS6_V1 else "YOK",
                                "DS7": "VAR" if r.V1 else "YOK", "dusen": ds7_dusen(r.to_dict())}
                               for _, r in Sm.iterrows() if bool(r.V1) != bool(r.DS6_V1)]
    sonuc["sayfa_cemal"] = {f"{s}/{p}": c for s, p, c in zip(Sm.set, Sm.sayfa, Sm.cemal)}
    JO = json.load(open(DS7_YOL["onay_anahtar"], encoding="utf-8"))
    sonuc["onay17"] = _onay17_tablo(JO)
    sonuc["havuz"] = JO["havuz"]
    md = _sonuc_md7(sonuc)
    hedef = cikti or DS7_DIR
    os.makedirs(hedef, exist_ok=True)
    GU._yaz(os.path.join(hedef, "DS7_SONUC.md"), md)
    GU._jyaz(os.path.join(hedef, "ds7_sonuc.json"), sonuc)
    return sonuc


def _sonuc_md7(S: Dict[str, Any]) -> str:
    B = S["kume"]["birleşik"]; v1 = B["model"]["V1"]
    L = [("# [DENEME — UYDURMA ETİKET] " if S["deneme"] else "# ") + "DİP SAVUNMASI v7 (DS7) — SONUÇ (iki kör set, 80 sayfa)", "",
         (f"Üretim: {GU._simdi()} (UTC). DENEME: uydurma etiket dosyaları; mühür denetimi YAPILMADI; 80 yanıt veriden yeniden hesaplandı, "
          "anahtarla aynı. GETİRİ YOK." if S["deneme"] else
          f"Üretim: {GU._simdi()} (UTC). Etiket dosyaları (cemal_isaret.json, cemal_isaret2.json) bu komutla açıldı: {S['etiket_acilis_utc']} (UTC). "
          "Mühür denetimi: ds7_anahtar.json, ds7.py, ds6.py, ds5.py, DS7_ESIK, kural kaynağı, DS7_ONAY.pdf ve ds7_onay_anahtar.json sha'ları "
          "DS7_ON_KAYIT ile aynı; 80 sayfanın P1-P4, TREND, KIRILIM, TREND_Z, KIRILIM_Z ve V1 / V2 / V3 yanıtı veriden yeniden hesaplandı, mühürle aynı. "
          "GETİRİ YOK."), "",
         f"Karar: birleşik {B['karar_n']} (Cemal VAR {B['cemal_VAR']}); işaretsiz / '?' (karar dışı): {B['isaretsiz']} {B['isaretsiz_sayfa']}.", "",
         f"## HÜKÜM (V1, ön kayıttaki eşikle): **{v1['hukum']}** — birleşik kappa {_f7(v1['kappa'])}, %95 [{_f7(v1['ar95'][0])}, {_f7(v1['ar95'][1])}]",
         "", "Sınır: kural Cemal'in DS5_ONAY / DS6_ONAY işaretlerinden kuruldu ve iki set önceki DS3-DS6 işlerinde kullanıldı; sonuç YARI "
         "BAĞIMSIZDIR. Kesin hüküm yalnız Cemal'in görsel onayı (DS7_ONAY.pdf) + bağımsız üçüncü kör setle.", ""]
    s1 = S["kume"]["set 1"]["model"]["V1"]["kappa"]; s2 = S["kume"]["set 2"]["model"]["V1"]["kappa"]
    dus1 = bool(np.isfinite(s1) and s1 < 0.40); dus2 = bool(np.isfinite(s2) and s2 < 0.40)
    if dus1 and dus2:
        L += [f"NOT: V1 kappa set 1 {_f7(s1)}, set 2 {_f7(s2)}: İKİ SETTE DE < 0,40.", ""]
    elif dus1 or dus2:
        L += [f"NOT: **tutarsız** — V1 kappa set 1 {_f7(s1)}, set 2 {_f7(s2)}; biri < 0,40.", ""]
    L += ["## Kappa tablosu", "", "| model | küme | karar | kod VAR | uyum | kappa | %95 aralık | %98,33 (Bonferroni 3) | hüküm |",
          "|---|---|---|---|---|---|---|---|---|"]
    for v in ("V1", "V2", "V3", "DS6_V1", "DS5_V1", "GOVDE_1"):
        for kad in ("set 1", "set 2", "birleşik"):
            r = S["kume"][kad]["model"][v]; kd = S["kume"][kad]
            huk = r["hukum"] if kad == "birleşik" else ("ayrı rapor" if v == "V1" else "bilgi")
            L.append(f"| {v} | {kad} | {kd['karar_n']} | {r['kod_VAR']} | {_f7(r['uyum'])} | {_f7(r['kappa'])} | [{_f7(r['ar95'][0])}, "
                     f"{_f7(r['ar95'][1])}] | [{_f7(r['ar_bon'][0])}, {_f7(r['ar_bon'][1])}] | {huk} |")
    L += ["", "V1 = dip / mavi (P1 ∧ P2' ∧ P3 ∧ P4) ∧ TREND (dayanıklı ana trend düşüyor) ∧ KIRILIM (C_t > T(t)); V2 = aynı, saf zarfla; "
          f"V3 = yalnız dip / mavi. DS6_V1 / DS5_V1 = önceki kurallar (mühürlü). GOVDE_1 = {S['govde_kural'].get('ozellik')} "
          f"{S['govde_kural'].get('yon')} {S['govde_kural'].get('esik')!r} (eşiği set 1 etiketleriyle seçildi -> set 1'de iç-örneklem).", "",
          f"HÜKÜM kuralı (ön kayıt): {DS7_ESIK['hukum']}.", "", "## 2x2", ""]
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
          "| sayfa | Cemal | V1 | V2 | V3 | DS6 | DS5 | GOVDE_1 | dip yaşı | düşüş | mavi düşüş (ATR) | dokunuş (ilk / ikinci) | dip sonrası en düşük "
          "Low (ATR) | i0 / dayanıklı j (dokunuş; affedilen) / zarf j* | C_t / T(t) - 1 | ilk kırılım / üst kapanış | düşen parça | kodun gördüğü |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in S["V1_uyusmayan"]:
        ne = "; ".join(r["neden"]) if r["neden"] else "altı parça da DOĞRU (kod VAR)"
        zz = (f"t{r['i0_t']:+d} / " + (f"t{r['dy_j_t']:+d}" if not r["dy_yok"] else "yok") +
              f" ({r['dy_dokunus_n']}; {r['dy_kisa_n']}) / t{r['jstar_t']:+d}") if r["i0_t"] is not None else "-"
        L.append(f"| {r['sayfa']} | {r['cemal']} | {r['V1']} | {r['V2']} | {r['V3']} | {r['DS6_V1']} | {r['DS5_V1']} | {r['GOVDE_1']} | {r['m']} | "
                 f"%{r['dusus']*100:.0f} | {r['mavi_dusus_atr']:.2f} | {r['dokunus_n']} ({r['dokunus_ilk']} / {r['dokunus_ikinci']}) | "
                 f"{r['min_post_low_atr']:+.2f} | {zz} | {('%' + format(r['oran'] * 100, '+.1f')) if r['oran'] is not None else '-'} | "
                 f"{('t%+d' % r['kirilim_t']) if r['kirilim_t'] is not None else '-'} / {r['ust_kapanis_n']} | {', '.join(r['dusen']) or '-'} | {ne} |")
    L += ["", "## Karşılaştırma: aynı sayfalarda DS6 V1, DS5 V1 ve GOVDE_1", ""]
    for o, G in S["karsilastirma"].items():
        L.append(f"- {o}: karar {G['karar_n']} sayfada iki kod {G['iki_kod_ayni_yanit']} sayfada aynı yanıt (kodlar arası kappa {_f7(G['kod_kappa'])}); "
                 f"V1 doğru / öteki yanlış {G['V1_dogru_oteki_yanlis']}; öteki doğru / V1 yanlış {G['oteki_dogru_V1_yanlis']}.")
    L += ["", "DS7 V1 ile DS6 V1'in ayrıldığı sayfalar: " + (", ".join(f"{z['sayfa']} (Cemal {z['cemal']}; DS6 {z['DS6']} -> DS7 {z['DS7']}; "
                                                                       f"düşen {','.join(z['dusen']) or '-'})" for z in S["V1_DS6_degisen"]) or "yok"), ""]
    O = S["onay17"]
    L += ["## DS6_ONAY sayfalarında v7 cevabı (BİLGİ; Cemal'in DS6_ONAY işaretleri tanım geri bildirimi)", "",
          f"İşaretli {O['isaretli_n']} sayfada v7 V1 Cemal'in genel hükmüyle uyumlu: **{O['uyumlu_n']} / {O['isaretli_n']}** (YANLIŞ dediği "
          f"{O['YANLIS_n']} sayfada {O['YANLIS_uyumlu']} itiraz giderildi; DOĞRU dediği {O['DOGRU_n']} sayfada {O['DOGRU_uyumlu']} korundu). "
          f"Karşılaştırma: v6 aynı 17 sayfada {O['v6_uyumlu_n']} / {O['isaretli_n']} uyumluydu.", "",
          "| sayfa | pazar | Cemal (DS6_ONAY) | v6 V1 | v7 V1 | v7 V2 | v7 V3 | Cemal'in beklediği | uyumlu | etiket | i0 / dayanıklı j (dokunuş; affedilen) / zarf j* | "
          "C_t / T(t) - 1 | ilk kırılım | v7 düşen parça | Cemal'in yazısı |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for z in O["satir"]:
        zz = (f"t{z['i0_t']:+d} / " + (f"t{z['dy_j_t']:+d}" if not z["dy_yok"] else "yok") +
              f" ({z['dy_dokunus_n']}; {z['dy_kisa_n']}) / t{z['jstar_t']:+d}") if z["i0_t"] is not None else "-"
        L.append(f"| {z['sayfa']} | {z['pazar']} | {z['cemal']} | {z['v6_V1']} | {z['v7_V1']} | {z['v7_V2']} | {z['v7_V3']} | "
                 f"{z['cemal_bekledigi'] or '-'} | {'-' if z['uyumlu'] is None else ('EVET' if z['uyumlu'] else 'HAYIR')} | {z['etiket']} | {zz} | "
                 f"{('%' + format(z['oran'] * 100, '+.1f')) if z['oran'] is not None else '-'} | "
                 f"{('t%+d' % z['kirilim_t']) if z['kirilim_t'] is not None else '-'} | {', '.join(z['dusen']) or '-'} | {str(z['yazi']).replace('|', '/')} |")
    hv = S["havuz"]
    L += ["", f"Havuz (bilgi; {hv['havuz_n']} olay): V1 VAR {json.dumps(hv['V1_VAR'], ensure_ascii=False)} (toplam {hv['toplam']['V1']}); "
          f"V2 {hv['toplam']['V2']}; V3 {hv['toplam']['V3']}; v6 V1 {hv['toplam']['v6_V1']}.", "",
          "Not: uyum Cemal'in gözüyle uyumdur; getiri ölçülmedi. Kural iş tanımından, kör set etiketlerine bakmadan sabitlendi ve önce sentetik "
          "serilerde sınandı."]
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
    if a.deneme and ({os.path.realpath(a.cemal1), os.path.realpath(a.cemal2)} & {os.path.realpath(DS7_YOL["set1_cemal"]),
                                                                                os.path.realpath(DS7_YOL["set2_cemal"])}
                     or os.path.realpath(a.cikti) == os.path.realpath(DS7_DIR)):
        raise SystemExit("--deneme gerçek etiket dosyasını açamaz / gerçek çıktı dizinine yazamaz")
    if not a.deneme and (a.cemal1 or a.cemal2 or a.cikti):
        raise SystemExit("gerçek kipte --cemal1 / --cemal2 / --cikti verilmez (mühürlü yollar kullanılır)")
    if a.komut == "anahtar":
        J = ds7_anahtar(); print(json.dumps(J["ozet"], ensure_ascii=False))
    elif a.komut == "onay":
        J = ds7_onay(a.havuz_onbellek)
        print(json.dumps([(s["sayfa"], s["pazar"], s["yanit_v6"], s["yanit"]["V1"], s["yanit"]["V2"], s["yanit"]["V3"], s["V1_dusen"])
                          for s in J["sayfalar"]], ensure_ascii=False))
        print(json.dumps(J["havuz"], ensure_ascii=False))
    elif a.komut == "muhur":
        print(ds7_muhur())
    elif a.komut == "olc":
        r = ds7_olc(a.deneme, a.cemal1, a.cemal2, a.cikti)
        print(json.dumps({k: {"karar_n": v["karar_n"], **{m: _f7(x["kappa"]) for m, x in v["model"].items()}} for k, v in r["kume"].items()},
                         ensure_ascii=False))
    else:
        T = ds7_test()
        print(json.dumps({"tamam": T["tamam"], "kural_sha": T["kural_sha"], "esik_sha": T["esik_sha"]}, ensure_ascii=False))
        for x in T["tablo"]:
            print(x["seri"], "bekl", x["beklenen_V1"], x["beklenen_dusen"], x["beklenen_ek"], "çıkan", x["cikan"], "düşen", x["dusen"],
                  "düşüş", x["dusus"], "mavi", x["mavi_dusus_atr"], "dok", x["dokunus_n"], x["ilk"], x["ikinci"], "i0/j*/dyj", x["i0"], x["jstar"],
                  x["dy_j"], "dydok", x["dy_dokunus_n"], "kısa", x["dy_kisa_n"], "aday/geç", x["dy_aday_n"], x["dy_gecerli_n"], "yok", x["dy_yok"],
                  "T/Tz/C", x["T_t"], x["T_z_t"], x["C_t"], "v6", x["v6"])
