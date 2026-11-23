"""DS6 — DİP SAVUNMASI v6: DS5 kuralının Cemal'in DS5_ONAY işaretlerine göre düzeltilmiş hali (23 Kasım 2026). GETİRİ ÖLÇMEZ.

Cemal'in DS5_ONAY geri bildirimi (cemal_ds5_onay.json; tanım geri bildirimi, kör set etiketi DEĞİL): mavi gövde çizgisine ve dibe itiraz yok;
bütün itirazlar KIRMIZI DÜŞEN ÇİZGİDE: (1) s13: H1 tek sivri tepeden seçilmiş, çizgi çok dik; asıl trend soldan dibe inen ALÇALAN TEPELERİ
birleştiren uzun, yatık çizgi; (2) s18 / s2 / s3 / s4: daha önce kapanışla delinmiş (kirli) çizginin yeni kırılımı güvenilmez; (3) s23: hafif
aşağı eğik mavi çizgi yatay sayılmalı. Cemal (23 Kas, aynen): "dip savunması en derinden yukarı veya yatay bir çizgiyi takip eden mumları
takip ederek var / yok demeli; bu mum öbekleri aynı zamanda düşen trend çizgisini de kırmalı, yoksa sürekli aşağı giden trend içinde bir
tepkidir." ve "trend çizgisi belli noktalarda üstüne çıkıp tekrar trend çizgisini takip ediyor; kırıldı dediği bu çizgi de diğerleri gibi
sahte çıkarsa?"

DS6 = DS5 aynen (dip, P1, mavi gövde altı çizgisi, P3 takip, P4 dip korunur, kırılım şartı) + üç değişiklik:
  D1 düşen çizgi = ALÇALAN TEPELER ÇİZGİSİ (pivot tepe çiftleri; kapanışla kesilmemiş; en çok tepe dokunuşu; eşitlikte uzun, sonra yatık)
  D2 çizginin temizliği (d'den önce sahte kırılım yok; geçerli çizgi yoksa KİRLİ)
  D3 yatay toleransı (mavi çizginin dipten t'ye toplam düşüşü <= 0,5 ATR)
Sinyal sonrası fiyat hiçbir adımda okunmaz: pencere = kör sayfa penceresi (tanim2.tz_pencere; veri sinyal günü t'de KESİLİR, son 121 bar).
Komutlar (repo kökünden):
  python arastirma_cikti/goz_uyum/ds6.py test                  çakışma kapısı + sentetik seriler S1-S16 + prefix değişmezliği
  python arastirma_cikti/goz_uyum/ds6.py anahtar               iki setin 80 sayfası: ara değerler + V1 / V2 / V3 -> ds6_anahtar.json
  python arastirma_cikti/goz_uyum/ds6.py onay [--havuz_onbellek X.pkl]
                                                               DS5_ONAY'ın 24 sayfası + 12 yeni sayfa -> DS6_ONAY.pdf + ds6_onay_anahtar.json
  python arastirma_cikti/goz_uyum/ds6.py muhur                 sha'lar + kural + sentetik tablo + hüküm + kontrol tablosu -> DS6_ON_KAYIT.md
  python arastirma_cikti/goz_uyum/ds6.py olc                   mühür denetimi + etiketleri AÇAR -> DS6_SONUC.md, ds6_sonuc.json
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

_CK_ONCE_DS6 = {k: id(v) for k, v in globals().items()}

import numpy as np
import pandas as pd

DS6_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(os.getcwd(), "arastirma_cikti", "goz_uyum")
if DS6_DIR not in sys.path:
    sys.path.insert(0, DS6_DIR)
import goz_uyum as GU  # noqa: E402  (yalnız okunur)
import tanim2 as TZ  # noqa: E402  (yalnız okunur)
import ds5 as D5  # noqa: E402  (yalnız okunur: ds5_parca_dizi (V3 ve ortak parçalar), ds5_pencere, ds5_setler, ds5_havuz, ds5_sentetik, _insa)

d6log = logging.getLogger("ds6")
if not d6log.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

KOK6 = GU.KOK
DS6_YOL = {"is_tanimi": os.path.join(DS6_DIR, "DS6_IS_TANIMI.md"), "anahtar": os.path.join(DS6_DIR, "ds6_anahtar.json"),
           "onkayit": os.path.join(DS6_DIR, "DS6_ON_KAYIT.md"), "sonuc": os.path.join(DS6_DIR, "DS6_SONUC.md"),
           "sonuc_json": os.path.join(DS6_DIR, "ds6_sonuc.json"), "pdf": os.path.join(DS6_DIR, "DS6_ONAY.pdf"),
           "onay_anahtar": os.path.join(DS6_DIR, "ds6_onay_anahtar.json"),
           "set1_anahtar": GU.GU_YOL["anahtar"], "set2_anahtar": TZ.TZ_YOL["anahtar"],
           "set1_cemal": os.path.join(DS6_DIR, "cemal_isaret.json"), "set2_cemal": os.path.join(DS6_DIR, "cemal_isaret2.json"),
           "govde_anahtar": os.path.join(DS6_DIR, "govde_anahtar.json"), "ds5_anahtar": os.path.join(DS6_DIR, "ds5_anahtar.json"),
           "ds4_onay_anahtar": os.path.join(DS6_DIR, "ds4_onay_anahtar.json"), "ds5_onay_anahtar": os.path.join(DS6_DIR, "ds5_onay_anahtar.json"),
           "cemal_ds5_onay": os.path.join(DS6_DIR, "cemal_ds5_onay.json"), "ds5_kod": os.path.join(DS6_DIR, "ds5.py"),
           "kod": os.path.abspath(__file__) if "__file__" in globals() else os.path.join(DS6_DIR, "ds6.py")}

# ---------------------------------------------------------------- KURAL (iş tanımından aynen; kör set etiketleri okunmadan; ADIM 1 commit'i)
# Ortak parçalar DS5 ile aynı (ds5.ds5_parca_dizi'den alınır): d, m, P1, ATR14(d), mavi gövde altı çizgisi (çapa (d, B_d), s*), P3 dokunuş
# (0,35 ATR; >= 3; iki yarı), P4 (0,25 ATR).
# D3  P2' = mavi çizginin dipten t'ye toplam düşüşü (-s* x m, s* < 0 ise) <= 0,5 x ATR (yukarı eğim serbest).
# D1  düşen çizgi = alçalan tepeler çizgisi: pivot tepeler (5/5, j+5 <= d; DS5 ile aynı tanım); aday = her çift (Ha, Hb), a < b,
#     High(Hb) < High(Ha); GEÇERLİ = a <= i <= d için Close_i <= çizgi_i + 0,25 ATR VE Ha'dan önceki 5 mumda Ha'dan yüksek High yok;
#     dokunuş = a <= j pivot tepeler, |High_j - çizgi_j| < 0,5 ATR; seçim: dokunuş çok > a küçük (uzun) > eğim büyük (yatık) > b küçük.
#     Geçerli çizgi yoksa en çok dokunuşlu aday (kapanış şartı yok, aynı sıralama) çizilir ve KİRLİ sayılır.
# D2  sahte kırılım = seçilen çizgi için a < i < d aralığında Close_i > çizgi_i + 0,25 ATR olan ardışık mum öbeği, ardından j <= d'de
#     Close_j < çizgi_j (altına dönüş). TEMİZ = geçerli çizgi seçildi VE sahte kırılım sayısı 0.
#     P5 (kırılım; DS5 şartı yeni çizgiye göre) = dipten sonra Close > çizgi en az 3 mum VE Close_t > çizgi_t VE en az bir P3 dokunuşu ilk
#     kırılım gününden SONRA.  P5' = TEMİZ ∧ P5.
# V1 (ANA) = P1 ∧ P2' ∧ P3 ∧ P4 ∧ P5'.  V2 = P1 ∧ P2' ∧ P3 ∧ P4 ∧ P5 (D2 temizlik şartı yok).  V3 = DS5 V1 (karşılaştırma).
DS6_ESIK: Dict[str, Any] = {
    "ds5_ortak": "d, m, P1 (0,20), ATR14(d), mavi çizgi (çapa (d, B_d), s*), P3 (0,35 ATR, >= 3, iki yarı), P4 (0,25 ATR), pivot tepe (5/5) DS5_ESIK "
                 "ile aynı (ds5.ds5_parca_dizi; ds5.py değiştirilmedi, sha ön kayıtta)",
    "yatay_dusus_atr": 0.5, "kesme_atr": 0.25, "tepe_dokunus_atr": 0.5, "tepe_sol": 5, "tepe_sag": 5, "kirilim_kapanis_min": 3,
    "belirsizlik": {
        "p2_yatay": "P2' = max(0, -s* x m) / ATR14(d) <= 0,5 (eşitlik geçer); m = t - d; s* DS5'teki mavi çizgi eğimi (gövde altlarının alt destek "
                    "çizgisi); yukarı eğim serbest",
        "aday": "pivot tepe kümesi DS5 ile aynı (H_j > max H_{j-5..j-1}, H_j >= max H_{j+1..j+5}, j-5 >= t-119, j+5 <= d); aday çizgi = her (a, b) "
                "pivot çifti, a < b, High_b < High_a (KESİN); çizgi_i = High_a + eğim (i - a), eğim = (High_b - High_a) / (b - a) < 0",
        "gecerli": "a <= i <= d için Close_i <= çizgi_i + 0,25 x ATR14(d) (eşitlik geçer) VE max High [a-5 .. a-1] < High_a (pivot tanımı gereği "
                   "zaten doğru; ayrıca denetlenir)",
        "tepe_dokunus": "a <= j olan pivot tepeler (Ha ve Hb dahil) için |High_j - çizgi_j| < 0,5 x ATR14(d) (kesin küçük); Ha'dan önceki pivotlar "
                        "sayılmaz",
        "secim": "geçerli adaylar arasında sıralama: (1) tepe dokunuşu ÇOK, (2) a KÜÇÜK (çizgi daha uzun, Ha daha solda), (3) eğim BÜYÜK (daha "
                 "yatık; eğim < 0), (4) b KÜÇÜK; ilk sıradaki seçilir. Geçerli aday yoksa bütün adaylar aynı sıralamayla, ilk sıradaki çizilir ve "
                 "KİRLİ sayılır. Aday hiç yoksa (alçalan pivot çifti yok) düşen çizgi yok: TEMİZ YANLIŞ ve P5 YANLIŞ",
        "sahte": "seçilen çizgi için a < i < d aralığında Close_i > çizgi_i + 0,25 ATR olan maksimal ardışık mum öbekleri; bir öbek, sonunda (öbekten "
                 "sonra) j <= d olan bir Close_j < çizgi_j varsa SAHTE KIRILIM sayılır; turuncu ∧ öbeğin çizgiyi en çok aşan mumunda. TANIM GEREĞİ: "
                 "geçerli çizginin sahte kırılımı 0'dır (geçerlilik aynı 0,25 ATR şartı); D2 yalnız geçerli çizgi hiç yokken bağlar",
        "temiz": "TEMİZ = geçerli çizgi seçildi VE sahte kırılım sayısı 0",
        "p5": "çizgi_i (seçilen) için d < i <= t: Close_i > çizgi_i (kesin) olan mum sayısı >= 3 VE Close_t > çizgi_t VE kırılım günü kb = ilk "
              "Close_i > çizgi_i (d < i) olmak üzere en az bir P3 dokunuşu j > kb (DS5 P5 şartı aynen, yeni çizgiye)",
        "dusen_parca": "V1'i düşüren parçalar listesi: P1, P2 (= P2'), P3, P4, D2 (TEMİZ değil), P5 (kırılım yok); V1 = altısı doğru; V2 = D2 hariç beşi",
        "v3": "V3 = ds5.ds5_parca_dizi(...)['V1'] (DS5 V1, aynı pencere; ds5_anahtar.json mühürlü V1 ile eşitliği anahtar adımında denetlenir)",
    },
    "varyant": {"V1": "P1 ∧ P2' ∧ P3 ∧ P4 ∧ P5' (ANA; P5' = TEMİZ ∧ kırılım, alçalan tepeler çizgisi)",
                "V2": "P1 ∧ P2' ∧ P3 ∧ P4 ∧ P5 (V1 ama D2 temizlik şartı yok)", "V3": "DS5 V1 (karşılaştırma)"},
    "kappa": {"B": 5000, "tohum": 20261127, "guven": 0.95, "bonferroni_k": 3, "gecerli": 0.60, "gecerli_alt": 0.40, "kismen": 0.40,
              "karar_min": 30},
    "hukum": "V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu "
             ">= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (düzeltme Cemal'in DS5_ONAY işaretlerinden; set 1 / set 2 "
             "sayfaları önceki DS3-DS5 işlerinde kullanıldı; kesin hüküm yalnız Cemal'in görsel onayı (DS6_ONAY.pdf) + üçüncü bağımsız kör "
             "setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. "
             "Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33)",
    "onay": {"eski_sayfa": 24, "eski_kaynak": "ds5_onay_anahtar.json sayfa 1..24 (pazar, sembol, sinyal günü), aynı sırada, yeni çizimle",
             "tohum": 20261127, "VAR": 8, "VAR_pazar": {"ABD": 6, "AVR": 1, "BIST": 1}, "YOK_rastgele": 2, "YOK_D2": 2,
             "secim": "12 yeni sayfa. Havuz = goz_uyum.gu_havuz (DS4 / DS5 görsel onayıyla aynı havuz; sha denetlenir); iki kör setteki, DS4 görsel "
                      "onay setindeki VE DS5 görsel onay setindeki (pazar, sembol) çiftleri hariç; olaylar tohumla (20261127) karıştırılmış sırada "
                      "gezilir, her (pazar, sembol) en çok 1 sayfa. V1 VAR 8: karışık sıradaki İLK V1 VAR olaylar, pazar hedefi ABD 6 / AVR 1 / "
                      "BIST 1 (seçme / ayıklama yok); bir pazarda yetmezse aynı karışık sırada öteki pazarların sıradaki V1 VAR olaylarıyla "
                      "doldurulur ve yazılır. V1 YOK 4: karışık sırada ilk 2 V1 YOK -> 'rastgele'; sonra V2 VAR ∧ V1 YOK (yalnız D2 düştü: kirli "
                      "çizginin kırılımı) -> 'D2' (2); havuzda D2 örneği 2'den azsa eksik karışık sıradaki sonraki V1 YOK ile 'rastgele' doldurulur "
                      "ve yazılır. Sayfa sırası: 1-24 eski sayfalar (DS5_ONAY ile aynı numara), 25-32 yeni VAR (geliş sırası), 33-36 yeni YOK "
                      "(tohumla karıştırılmış); PDF kör değil, onay amaçlı"},
    "eski24_bilgi": "ADIM 3 bilgi tablosu (hüküm dışı): DS5_ONAY 24 sayfasında DS5 V1 -> DS6 V1 / V2; Cemal'in işareti (cemal_ds5_onay.json: DOĞRU / "
                    "YANLIŞ / İŞARETSİZ) ve çizim betimi; mekanik etiket: Cemal YANLIŞ ve V1 değişti -> 'itiraz yanıtı değişti'; Cemal YANLIŞ ve V1 "
                    "aynı -> 'yanıt aynı (çizgi değişti / aynı)'; Cemal DOĞRU ve V1 değişti -> 'DİKKAT: Cemal'in DOĞRU dediği yanıt değişti'; "
                    "Cemal DOĞRU ve aynı -> 'korundu'; işaretsiz -> 'bilgi'. Çizgi değişimi = DS6 (Ha, Hb) ile DS5 (H1, H2) aynı değil",
    "not": "parametreler (0,5 ATR yatay düşüş; 0,25 ATR kapanış kesmesi; 0,5 ATR tepe dokunuşu; 5/5 pivot; 3 kapanış) iş tanımından aynen; "
           "kör set etiketlerine bakılmadan sabitlendi; GETİRİ YOK",
}


class DS6Hata(RuntimeError):
    """Durdurucu hata: veri / mühür / tanım tutmadı."""


def _sha_esik6() -> str:
    return hashlib.sha256(json.dumps(DS6_ESIK, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _f6(x: Any, d: int = 3) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"{float(x):.{d}f}"
    except (TypeError, ValueError):
        return str(x)


def _isr6(x: bool) -> str:
    return "✓" if x else "✗"


# ================================================================ 1) KURAL (yalnız pencere; t sonrası yok)
def _ds6_pivot(H: np.ndarray, s0: int, d: int) -> List[int]:
    """Pivot tepeler (DS5 ile aynı tanım): H_j > max H_{j-5..j-1}, H_j >= max H_{j+1..j+5}; j-5 >= s0, j+5 <= d."""
    ts, tg = int(DS6_ESIK["tepe_sol"]), int(DS6_ESIK["tepe_sag"])
    return [j for j in range(s0 + ts, d - tg + 1) if H[j] > H[j - ts:j].max() and H[j] >= H[j + 1:j + tg + 1].max()]


def _ds6_dusen(H: np.ndarray, C: np.ndarray, s0: int, d: int, atr: float) -> Dict[str, Any]:
    """D1 + D2: alçalan tepeler çizgisi seçimi ve sahte kırılımlar. Yalnız [s0 .. d] okunur."""
    E = DS6_ESIK; ke = float(E["kesme_atr"]) * atr; te = float(E["tepe_dokunus_atr"]) * atr; ts = int(E["tepe_sol"])
    tepe = _ds6_pivot(H, s0, d)
    adaylar = []
    for ia, a in enumerate(tepe):
        for b in tepe[ia + 1:]:
            if not H[b] < H[a]:
                continue
            eg = (float(H[b]) - float(H[a])) / float(b - a)
            ii = np.arange(a, d + 1); cz = float(H[a]) + eg * (ii - a)
            sol_ok = bool(H[max(s0, a - ts):a].max() < H[a]) if a > s0 else False
            gecerli = bool(sol_ok and np.all(C[ii] <= cz + ke))
            dok = [j for j in tepe if j >= a and abs(float(H[j]) - (float(H[a]) + eg * (j - a))) < te]
            adaylar.append({"a": int(a), "b": int(b), "egim": float(eg), "gecerli": gecerli, "dokunus": dok})
    sira = sorted(adaylar, key=lambda x: (-len(x["dokunus"]), x["a"], -x["egim"], x["b"]))
    gec = [x for x in sira if x["gecerli"]]
    out: Dict[str, Any] = {"pivot_tepeler": [int(j) for j in tepe], "aday_n": len(adaylar), "gecerli_n": len(gec), "cizgi_var": False,
                           "gecerli_secildi": False, "ha_idx": -1, "hb_idx": -1, "ha": float("nan"), "hb": float("nan"),
                           "egim_dusen": float("nan"), "tepe_dokunus": [], "tepe_dokunus_n": 0, "sahte": [], "sahte_n": 0, "temiz": False}
    if not sira:
        return out
    s = gec[0] if gec else sira[0]
    a, eg = s["a"], s["egim"]
    ii = np.arange(a + 1, d); cz = float(H[a]) + eg * (ii - a); ust = C[ii] > cz + ke
    sahte: List[int] = []; k = 0
    while k < len(ii):
        if ust[k]:
            e = k
            while e + 1 < len(ii) and ust[e + 1]:
                e += 1
            sonra = np.arange(int(ii[e]) + 1, d + 1)
            if len(sonra) and np.any(C[sonra] < float(H[a]) + eg * (sonra - a)):
                blok = ii[k:e + 1]; sahte.append(int(blok[int(np.argmax(C[blok] - (float(H[a]) + eg * (blok - a))))]))
            k = e + 1
        else:
            k += 1
    out.update({"cizgi_var": True, "gecerli_secildi": bool(s["gecerli"]), "ha_idx": int(a), "hb_idx": int(s["b"]), "ha": float(H[a]),
                "hb": float(H[s["b"]]), "egim_dusen": float(eg), "tepe_dokunus": [int(j) for j in s["dokunus"]],
                "tepe_dokunus_n": int(len(s["dokunus"])), "sahte": sahte, "sahte_n": int(len(sahte)),
                "temiz": bool(s["gecerli"] and len(sahte) == 0)})
    return out


def ds6_parca_dizi(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray) -> Dict[str, Any]:
    """Diziler kör sayfa penceresi (son eleman = t, 121 bar). DS5 ortak parçaları + D1 / D2 / D3 + V1 / V2 / V3. Dizinler 121 barlık pencerede."""
    E = DS6_ESIK
    O, H, L, C = (np.asarray(a, float) for a in (O, H, L, C))
    try:
        r5 = D5.ds5_parca_dizi(O, H, L, C)                                   # pencere / geçersiz bar denetimi + ortak parçalar
    except D5.DS5Hata as ex:
        raise DS6Hata(str(ex)) from ex
    t, s0, d, m, atr = int(r5["t_idx"]), int(r5["s0_idx"]), int(r5["d_idx"]), int(r5["m"]), float(r5["atr_d"])
    # D3: yatay toleransı
    mavi_dusus = float(max(0.0, -float(r5["s"]) * m) / atr)
    p2 = bool(mavi_dusus <= float(E["yatay_dusus_atr"]))
    # D1 + D2: alçalan tepeler çizgisi
    Dz = _ds6_dusen(H, C, s0, d, atr)
    post = np.arange(d + 1, t + 1)
    ust: List[int] = []; kb = -1; son_ust = False; dok_sonra = 0; p5_neden = ""
    if not Dz["cizgi_var"]:
        p5_neden = "alçalan pivot tepe çifti yok (düşen çizgi yok)"
    else:
        dc = Dz["ha"] + Dz["egim_dusen"] * (post - Dz["ha_idx"])
        ust = [int(i) for i in post[C[post] > dc]]; son_ust = bool(C[t] > dc[-1]); kb = ust[0] if ust else -1
        dok_sonra = int(sum(1 for j in r5["dokunus"] if kb >= 0 and j > kb))
        if len(ust) < int(E["kirilim_kapanis_min"]):
            p5_neden = f"düşen çizginin üstünde {len(ust)} kapanış (< 3)"
        elif not son_ust:
            p5_neden = "son mumun kapanışı düşen çizginin altında"
        elif dok_sonra < 1:
            p5_neden = "kırılımdan sonra mavi çizgiye dokunuş yok"
    p5 = bool(Dz["cizgi_var"] and len(ust) >= int(E["kirilim_kapanis_min"]) and son_ust and dok_sonra >= 1)
    d2 = bool(Dz["temiz"])
    if not Dz["cizgi_var"]:
        d2_neden = "düşen çizgi yok"
    elif not Dz["gecerli_secildi"]:
        d2_neden = f"kapanışla kesilmemiş çizgi yok: kirli çizgi (sahte kırılım {Dz['sahte_n']})"
    elif Dz["sahte_n"]:
        d2_neden = f"sahte kırılım {Dz['sahte_n']}"
    else:
        d2_neden = ""
    ortak = bool(r5["P1"] and p2 and r5["P3"] and r5["P4"])
    v2 = bool(ortak and p5); v1 = bool(v2 and d2)
    out = {k: r5[k] for k in ("t_idx", "s0_idx", "d_idx", "m", "low_d", "B_d", "d_glob_idx", "dip_yeni", "tepe_idx", "tepe", "dusus", "P1",
                              "atr_d", "s", "s_atr20", "cizgi_son", "dokunus", "dokunus_n", "dokunus_ilk", "dokunus_ikinci", "P3",
                              "min_post_low_atr", "P4")}
    out.update({"mavi_dusus_atr": mavi_dusus, "P2": p2, "P2_ds5": bool(r5["P2"]), **Dz, "kirilim_idx": int(kb), "ust_kapanis": ust,
                "ust_kapanis_n": int(len(ust)), "son_ust": son_ust, "dokunus_kirilim_sonra": int(dok_sonra), "P5": p5, "P5_neden": p5_neden,
                "D2": d2, "D2_neden": d2_neden, "P5p": bool(d2 and p5),
                "ds5_h1_idx": int(r5["h1_idx"]), "ds5_h2_idx": int(r5["h2_idx"]), "ds5_P5": bool(r5["P5"]),
                "V1": v1, "V2": v2, "V3": bool(r5["V1"])})
    return out


def ds6_parca(W: pd.DataFrame) -> Dict[str, Any]:
    O, H, L, C = (W[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    r = ds6_parca_dizi(O, H, L, C)
    ix = W.index

    def tar(i: int) -> Optional[str]:
        return ix[i].strftime("%Y-%m-%d") if i >= 0 else None
    r["d_tarih"] = tar(r["d_idx"]); r["ha_tarih"] = tar(r["ha_idx"]); r["hb_tarih"] = tar(r["hb_idx"]); r["kirilim_tarih"] = tar(r["kirilim_idx"])
    r["sahte_tarih"] = [tar(j) for j in r["sahte"]]
    return r


def _kural_sha6() -> str:
    """Kural kaynağının (_ds6_pivot + _ds6_dusen + ds6_parca_dizi + ds6_parca) + DS5 kural sha'sı."""
    src = "".join(inspect.getsource(f) for f in (_ds6_pivot, _ds6_dusen, ds6_parca_dizi, ds6_parca)) + D5._kural_sha5()
    return hashlib.sha256(src.encode("utf-8")).hexdigest()


def ds6_dusen(r: Dict[str, Any]) -> List[str]:
    """V1'i düşüren parçalar (P1 / P2 / P3 / P4 / D2 / P5)."""
    return [p for p in ("P1", "P2", "P3", "P4", "D2", "P5") if not r[p]]


def ds6_neden_metni(r: Dict[str, Any]) -> List[str]:
    out = []
    if not r["P1"]:
        out.append("P1 düşüş yok (%s < %%20)" % ("-" if not np.isfinite(r["dusus"]) else f"%{r['dusus']*100:.0f}"))
    if not r["P2"]:
        out.append(f"P2 mavi çizgi {r['mavi_dusus_atr']:.2f} ATR aşağı (> 0,5)")
    if not r["P3"]:
        out.append(f"P3 takip yok (dokunuş {r['dokunus_n']}: ilk yarı {r['dokunus_ilk']}, ikinci yarı {r['dokunus_ikinci']})")
    if not r["P4"]:
        out.append(f"P4 dip delinmiş (dip sonrası en düşük Low {r['min_post_low_atr']:+.2f} ATR)")
    if not r["D2"]:
        out.append(f"D2 {r['D2_neden']}")
    if not r["P5"]:
        out.append(f"P5 {r['P5_neden']}")
    return out


# ================================================================ 2) SETLER ve ANAHTAR
def _temiz6(r: Dict[str, Any]) -> Dict[str, Any]:
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


def ds6_hesap(S: pd.DataFrame) -> pd.DataFrame:
    out = []
    for r in S.itertuples(index=False):
        W = D5.ds5_pencere(r.pazar, r.sembol, r.sinyal_gunu)                # K2: veri t'de kesik + mekanik denetim (121 bar, son = t)
        out.append(ds6_parca(W))
    return pd.concat([S.reset_index(drop=True), pd.DataFrame(out)], axis=1)


def _ozet6(R: pd.DataFrame) -> Dict[str, Any]:
    return {"n": int(len(R)), **{f"{v}_VAR": int(R[v].sum()) for v in ("V1", "V2", "V3")},
            **{f"{p}_DOGRU": int(R[p].sum()) for p in ("P1", "P2", "P2_ds5", "P3", "P4", "D2", "P5", "gecerli_secildi")}}


def ds6_anahtar() -> Dict[str, Any]:
    t0 = time.time()
    S = D5.ds5_setler()
    R = ds6_hesap(S)
    J5 = json.load(open(DS6_YOL["ds5_anahtar"], encoding="utf-8"))
    v5 = {(int(s["set"]), int(s["sayfa"])): bool(s["V1"]) for s in J5["sayfalar"]}; del J5
    fark = [(int(s), int(p)) for s, p, v in zip(R.set, R.sayfa, R.V3) if v5[(int(s), int(p))] != bool(v)]
    if fark:
        raise DS6Hata(f"V3 (DS5 V1 yeniden hesap) ds5_anahtar.json mühürlü V1 ile aynı değil: {fark}")
    sayfalar = []
    for r in R.to_dict("records"):
        r = _temiz6(r)
        r["yanit"] = {v: ("VAR" if r[v] else "YOK") for v in ("V1", "V2", "V3")}
        r["V1_dusen"] = ds6_dusen(r)
        sayfalar.append(r)
    ozet = {str(st): _ozet6(R if st == "birlesik" else R[R.set == st]) for st in (1, 2, "birlesik")}
    J = {"surum": "ds6 v1", "uretim_utc": GU._simdi(),
         "uyari": "GETİRİ YOK; Cemal'in kör set işaretleri bu dosya yazılırken AÇILMADI (etiketler yalnız mühürden sonra olc ile açılır); "
                  "dizinler 121 barlık pencerede (t = 120); V3 = DS5 V1 (ds5_anahtar.json ile eşit, denetlendi)",
         "esik": DS6_ESIK, "esik_sha": _sha_esik6(), "kural_sha": _kural_sha6(),
         "girdi_sha": {"goz_uyum_anahtar.json": GU._sha(DS6_YOL["set1_anahtar"]), "tanim2_anahtar.json": GU._sha(DS6_YOL["set2_anahtar"]),
                       "ds5_anahtar.json": GU._sha(DS6_YOL["ds5_anahtar"]), "ds5.py": GU._sha(DS6_YOL["ds5_kod"])},
         "ozet": ozet, "sayfalar": sayfalar, "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(DS6_YOL["anahtar"], J)
    d6log.info("anahtar: %s", json.dumps(ozet, ensure_ascii=False))
    return J


# ================================================================ 3) GÖRSEL ONAY (DS5_ONAY'ın 24 sayfası + 12 yeni sayfa)
def ds6_onay_sec(P: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    Eo = DS6_ESIK["onay"]; rng = np.random.default_rng(int(Eo["tohum"]))
    S = D5.ds5_setler(); haric = {(a, b) for a, b in zip(S.pazar, S.sembol)}
    for y in (DS6_YOL["ds4_onay_anahtar"], DS6_YOL["ds5_onay_anahtar"]):
        Jx = json.load(open(y, encoding="utf-8")); haric |= {(str(s["pazar"]), str(s["sembol"])) for s in Jx["sayfalar"]}; del Jx
    sira = rng.permutation(len(P))
    K: List[Dict[str, Any]] = []
    for j in sira:                                                         # tam havuzda kural (havuz sayımı için; seçim hariç kümeden)
        q = P.iloc[int(j)]
        W = D5.ds5_pencere(q.pazar, q.sembol, q.tarih.strftime("%Y-%m-%d"))
        K.append({"pazar": q.pazar, "sembol": q.sembol, "sinyal_gunu": q.tarih.strftime("%Y-%m-%d"),
                  "haric": (q.pazar, q.sembol) in haric, **_temiz6(ds6_parca(W))})
    KD = pd.DataFrame(K)
    kota = {"VAR": int(Eo["VAR"]), "YOK_rastgele": int(Eo["YOK_rastgele"]), "YOK_D2": int(Eo["YOK_D2"])}
    vpk = {p: int(x) for p, x in Eo["VAR_pazar"].items()}
    if sum(vpk.values()) != kota["VAR"]:
        raise DS6Hata("VAR pazar hedefleri toplamı VAR kotasına eşit değil")
    al: Dict[str, List[Dict[str, Any]]] = {k: [] for k in kota}; kullanilan: set = set(); notlar: List[str] = []
    var_say = {p: 0 for p in vpk}
    Kh = [r for r in K if not r["haric"]]
    for r in Kh:
        key = (r["pazar"], r["sembol"])
        if key in kullanilan:
            continue
        grup = None
        if r["V1"]:
            if var_say.get(r["pazar"], 0) < vpk.get(r["pazar"], 0):
                grup = "VAR"; var_say[r["pazar"]] += 1
        elif len(al["YOK_rastgele"]) < kota["YOK_rastgele"]:
            grup = "YOK_rastgele"
        elif r["V2"] and len(al["YOK_D2"]) < kota["YOK_D2"]:
            grup = "YOK_D2"
        if grup:
            kullanilan.add(key); al[grup].append({**r, "grup": grup})
    for p in vpk:
        if var_say[p] < vpk[p]:
            notlar.append(f"V1 VAR {p}: hedef {vpk[p]}, havuzda bulunan {var_say[p]}")
    if len(al["VAR"]) < kota["VAR"]:
        for r in Kh:
            if len(al["VAR"]) >= kota["VAR"]:
                break
            key = (r["pazar"], r["sembol"])
            if r["V1"] and key not in kullanilan:
                kullanilan.add(key); al["VAR"].append({**r, "grup": "VAR"}); notlar.append(f"V1 VAR eksiği {r['pazar']} ile dolduruldu")
    if len(al["YOK_D2"]) < kota["YOK_D2"]:
        notlar.append(f"D2 örneği (V2 VAR ∧ V1 YOK) havuzda {len(al['YOK_D2'])}; eksik rastgele V1 YOK ile dolduruldu")
        for r in Kh:
            if len(al["YOK_D2"]) + len(al["YOK_rastgele"]) >= kota["YOK_D2"] + kota["YOK_rastgele"]:
                break
            key = (r["pazar"], r["sembol"])
            if not r["V1"] and key not in kullanilan:
                kullanilan.add(key); al["YOK_rastgele"].append({**r, "grup": "YOK_rastgele"})
    if len(al["VAR"]) < kota["VAR"] or len(al["YOK_D2"]) + len(al["YOK_rastgele"]) < kota["YOK_D2"] + kota["YOK_rastgele"]:
        raise DS6Hata("görsel onay kotası dolmadı")
    Y = pd.DataFrame([x for k in ("YOK_D2", "YOK_rastgele") for x in al[k]])
    Y = Y.iloc[rng.permutation(len(Y))]
    T = pd.concat([pd.DataFrame(al["VAR"]), Y]).reset_index(drop=True)
    T.insert(0, "sayfa", np.arange(int(Eo["eski_sayfa"]) + 1, int(Eo["eski_sayfa"]) + 1 + len(T)))
    KH = KD[~KD.haric]
    bilgi = {"havuz_n": int(len(P)), "haric_disi_n": int(len(KH)),
             "havuz_pazar": {p: int((KD.pazar == p).sum()) for p in ("ABD", "AVR", "BIST")},
             "havuz_V1_VAR": {p: int(KD[KD.pazar == p].V1.sum()) for p in ("ABD", "AVR", "BIST")},
             "havuz_parca": {k: int(KD[k].sum()) for k in ("P1", "P2", "P2_ds5", "P3", "P4", "D2", "P5", "gecerli_secildi", "V1", "V2", "V3")},
             "havuz_kirli_n": int((~KD.gecerli_secildi.astype(bool) & KD.cizgi_var.astype(bool)).sum()),
             "havuz_cizgi_yok_n": int((~KD.cizgi_var.astype(bool)).sum()),
             "haric_disi_V1_VAR": {p: int(KH[KH.pazar == p].V1.sum()) for p in ("ABD", "AVR", "BIST")},
             "haric_disi_parca": {k: int(KH[k].sum()) for k in ("P1", "P2", "P3", "P4", "D2", "P5", "V1", "V2", "V3")},
             "VAR_pazar_sayfa": {p: int(sum(1 for x in al["VAR"] if x["pazar"] == p)) for p in ("ABD", "AVR", "BIST")}, "notlar": notlar}
    return T, bilgi


def ds6_sayfa_ciz(W: pd.DataFrame, r: Dict[str, Any], no: int, toplam: int, eski_v1: Optional[bool] = None):
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
    xs = np.array([d, t]); ys = r["B_d"] + r["s"] * (xs - d)
    ax.plot(xs - t, ys, color="#1f4e9c", linewidth=3.0, zorder=6, solid_capstyle="round")
    ax.annotate("DİP", xy=(xd, L[d]), xytext=(xd, L[d] - pad * 1.8), ha="center", va="top", fontsize=10, color="#1f4e9c", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#1f4e9c", lw=1.5), zorder=8)
    if r["cizgi_var"]:
        a = int(r["ha_idx"]); xs2 = np.array([a, t]); ys2 = r["ha"] + r["egim_dusen"] * (xs2 - a)
        ax.plot(xs2 - t, ys2, color="#e31a1c", linewidth=1.8, zorder=7, linestyle="-" if r["gecerli_secildi"] else "--")
        tj = np.array(r["tepe_dokunus"], int)
        if len(tj):
            ax.plot(tj - t, H[tj], linestyle="none", marker="o", markersize=8, markerfacecolor="none", markeredgecolor="#e31a1c",
                    markeredgewidth=1.6, zorder=8)
        for j in r["sahte"]:
            ax.plot([j - t], [H[j] + pad * 0.45], marker="^", markersize=11, color="#ff7f00", markeredgecolor="#b35806", linestyle="none", zorder=9)
    for j in r["ust_kapanis"]:
        ax.plot([j - t - 0.45, j - t + 0.45], [C[j], C[j]], color="#ff7f00", linewidth=2.2, zorder=9, solid_capstyle="butt")
    B = np.minimum(O, C)
    for j in r["dokunus"]:
        ax.plot([j - t], [B[j] - pad * 0.35], marker="o", markersize=6, markerfacecolor="none", markeredgecolor="#6a3d9a",
                markeredgewidth=1.6, linestyle="none", zorder=9)
    ax.axvline(0.5, color="#555555", linewidth=0.8, zorder=2); ax.axvline(-0.5, color="#555555", linewidth=0.8, zorder=2)
    ust_y = max(Hs.max(), r["ha"] if np.isfinite(r["ha"]) else Hs.max())
    ax.set_ylim(Ls.min() - pad * 2.4, ust_y + pad * 1.6); ax.set_xlim(x[0] - 1, 2)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.6); sp.set_color("#888888")
    fig.text(0.04, 0.945, f"{int(no)}", fontsize=44, fontweight="bold", va="center", ha="left")
    fig.text(0.96, 0.945, f"/ {toplam}", fontsize=16, va="center", ha="right", color="#666666")
    if eski_v1 is not None:
        fig.text(0.50, 0.945, f"geçen sefer (v5) kodun cevabı: {'VAR' if eski_v1 else 'YOK'}", fontsize=10, va="center", ha="center",
                 color="#444444")
    fig.text(0.50, 0.895, "kalın mavi = dipten başlayan gövde altı çizgisi · mor daire = mavi çizgiye değen mum · sarı zemin = dipten sonrası",
             fontsize=7.2, ha="center", color="#555555")
    fig.text(0.50, 0.878, "kırmızı = alçalan tepeler çizgisi · kırmızı daire = çizginin değdiği tepe · turuncu ∧ = sahte kırılım (kapanış çizgiyi "
             "deldi, geri döndü)", fontsize=7.2, ha="center", color="#555555")
    fig.text(0.50, 0.861, "kesik kırmızı = kapanışla kesilmemiş çizgi yok (kirli) · turuncu kısa çizgi = dipten sonra kırmızı çizginin üstünde "
             "kapanış", fontsize=7.2, ha="center", color="#555555")
    s1 = f"Düşüşten dip {_isr6(r['P1'])}   —   Mavi çizgi yatay/yukarı {_isr6(r['P2'])}"
    s2 = f"Mumlar mavi çizgiyi takip ediyor (dokunuş {int(r['dokunus_n'])}) {_isr6(r['P3'])}   —   Dip korunuyor {_isr6(r['P4'])}"
    s3 = f"Çizgi temiz mi (sahte kırılım {int(r['sahte_n'])}) {_isr6(r['D2'])}   —   Dizi kırmızı çizgiyi kırdı {_isr6(r['P5'])}"
    fig.text(0.50, 0.245, s1, fontsize=11.5, ha="center", va="center")
    fig.text(0.50, 0.215, s2, fontsize=11.5, ha="center", va="center")
    fig.text(0.50, 0.185, s3, fontsize=11.5, ha="center", va="center")
    fig.text(0.50, 0.135, f"SONUÇ: {'VAR' if r['V1'] else 'YOK'}", fontsize=20, fontweight="bold", ha="center", va="center")
    fig.text(0.50, 0.070, "☐ DOĞRU        ☐ YANLIŞ", fontsize=15, ha="center", va="center")
    return fig


def ds6_onay(onbellek: Optional[str] = None) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    t0 = time.time()
    P = D5.ds5_havuz(onbellek)                                              # DS4 / DS5 görsel onay havuzu (sha denetimi ds5_havuz içinde)
    hsha = D5._havuz_sha5(P)
    J5o = json.load(open(DS6_YOL["ds5_onay_anahtar"], encoding="utf-8"))
    if J5o["havuz_sha"] != hsha:
        raise DS6Hata("havuz DS5 görsel onay havuzuyla aynı değil (sha)")
    eski = []
    for s in sorted(J5o["sayfalar"], key=lambda z: int(z["sayfa"])):
        W = D5.ds5_pencere(s["pazar"], s["sembol"], s["sinyal_gunu"])
        r = _temiz6(ds6_parca(W))
        if bool(r["V3"]) != bool(s["V1"]):
            raise DS6Hata(f"eski sayfa {s['sayfa']}: V3 (DS5 V1) mühürlü DS5 onay yanıtıyla aynı değil")
        eski.append({"sayfa": int(s["sayfa"]), "pazar": s["pazar"], "sembol": s["sembol"], "sinyal_gunu": s["sinyal_gunu"],
                     "grup": "ESKİ (DS5_ONAY " + str(s["grup"]) + ")", "ds5_V1": bool(s["V1"]), "ds5_h1_onay": int(s["h1_idx"]),
                     "ds5_h2_onay": int(s["h2_idx"]), **r})
    if [e["sayfa"] for e in eski] != list(range(1, int(DS6_ESIK["onay"]["eski_sayfa"]) + 1)):
        raise DS6Hata("DS5 onay sayfaları 1..24 değil")
    T, bilgi = ds6_onay_sec(P)
    tum = eski + [dict(x) for x in T.to_dict("records")]
    toplam = len(tum)
    yol = DS6_YOL["pdf"]
    with PdfPages(yol, metadata={"Title": "DIP SAVUNMASI v6 - gorsel onay", "Author": "ds6", "Creator": "ds6", "Producer": "ds6",
                                 "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(7.5, 10.5))
        fig.text(0.5, 0.90, "DİP SAVUNMASI — kodun gözü (v6)", fontsize=22, fontweight="bold", ha="center")
        kapak = ("Düzeltmeler:\n"
                 "(1) kırmızı çizgi artık alçalan tepeleri birleştiriyor,\n"
                 "     tek sivri tepeden değil;\n"
                 "(2) daha önce delinmiş (kirli) çizginin kırılımı\n"
                 "     sayılmıyor;\n"
                 "(3) hafif aşağı eğik mavi çizgi yatay sayılıyor.\n\n"
                 "İlk 24 sayfa geçen seferkiyle aynı hisseler;\n"
                 "sonra 12 yeni sayfa.")
        fig.text(0.10, 0.84, kapak, fontsize=14, ha="left", va="top", linespacing=1.4)
        aciklama = ("Çizimler:\n"
                    "  DİP oku = penceredeki en derin nokta (en düşük fitil)\n"
                    "  kalın mavi çizgi = dip mumunun gövde altından başlayıp sonraki bütün gövde altlarının\n"
                    "      altında kalan en dik çizgi (sağa son güne kadar); mor daire = mavi çizgiye değen mum\n"
                    "  kırmızı çizgi = dibe inerken alçalan tepeleri birleştiren çizgi (en çok tepeye değen;\n"
                    "      eşitse en uzun); kırmızı daire = çizginin değdiği tepeler\n"
                    "  kırmızı kesik çizgi = kapanışla delinmemiş çizgi yok, çizilen çizgi kirli\n"
                    "  turuncu ∧ = sahte kırılım (kapanış çizginin üstüne çıkıp geri döndü)\n"
                    "  turuncu kısa çizgi = dipten sonra kırmızı çizginin üstünde kapanış\n"
                    "  sarı zemin = dipten sonraki bölge\n\n"
                    "Mavi çizgi: dipten sona toplam yarım ortalama mum boyundan az inen çizgi yatay sayılır.\n"
                    "Takip: en az 3 dokunuş, dipten sonraki sürenin hem ilk hem ikinci yarısında.\n"
                    "Kırılım: en az 3 kapanış ve son gün kırmızı çizginin üstünde; kırılımdan sonra da\n"
                    "      mavi çizgiye en az bir dokunuş; ve çizgi daha önce kapanışla delinmemiş olmalı.\n"
                    "İlk 24 sayfanın üstünde geçen seferki (v5) cevap yazılı; karşılaştırabilirsin.\n"
                    f"{toplam} sayfa (bu PDF kör değil, onay için). Hisse adı yok; son günden sonrası gösterilmez.\n"
                    "Kutulardan birini işaretlemen yeter.")
        fig.text(0.06, 0.47, aciklama, fontsize=9.0, ha="left", va="top", linespacing=1.35)
        pdf.savefig(fig); plt.close(fig)
        for rr in tum:
            W = D5.ds5_pencere(rr["pazar"], rr["sembol"], rr["sinyal_gunu"])
            r = ds6_parca(W)
            if r["V1"] != bool(rr["V1"]):
                raise DS6Hata("onay: V1 yeniden hesapta seçimden farklı")
            fig = ds6_sayfa_ciz(W, r, int(rr["sayfa"]), toplam, rr.get("ds5_V1") if int(rr["sayfa"]) <= 24 else None)
            pdf.savefig(fig); plt.close(fig)
    boy = os.path.getsize(yol)
    if boy >= 6 * 1024 * 1024:
        raise DS6Hata(f"PDF 6 MB'tan büyük: {boy}")
    sayfalar = []
    for rr in tum:
        rr = _temiz6(rr); rr.pop("haric", None); rr["V1_dusen"] = ds6_dusen(rr); rr["neden"] = ds6_neden_metni(rr)
        rr["yanit"] = {v: ("VAR" if rr[v] else "YOK") for v in ("V1", "V2", "V3")}
        sayfalar.append(rr)
    J = {"surum": "ds6 onay v1", "uretim_utc": GU._simdi(),
         "uyari": "GİZLİ ANAHTAR (hisse adları): Cemal DS6_ONAY.pdf'i işaretlemeden önce gösterilmez. GETİRİ YOK.",
         "esik_sha": _sha_esik6(), "kural_sha": _kural_sha6(), "havuz_sha": hsha, "havuz": bilgi,
         "pdf_sha": GU._sha(yol), "pdf_bayt": boy, "sayfalar": sayfalar, "sure_sn": round(time.time() - t0, 1)}
    GU._jyaz(DS6_YOL["onay_anahtar"], J)
    d6log.info("onay PDF %s (%.2f MB): %s", yol, boy / 1e6, [(s["sayfa"], s["grup"], s["yanit"]["V1"]) for s in sayfalar])
    return J


# ================================================================ 4) TEST (sentetik seriler; gerçek veriden ÖNCE)
def ds6_cakisma_kontrol() -> None:
    ez = [k for k, v in _CK_ONCE_DS6.items() if k in globals() and id(globals()[k]) != v and not k.startswith("_")]
    if ez:
        raise DS6Hata(f"çakışma kapısı: bellekteki mevcut ad(lar) ezildi: {ez[:5]}")


def _insa6(knot_x: List[int], knot_y: List[float], m: int, dip: Tuple[float, float, float, float],
           post: List[Tuple[float, float, float, float]], tut: Optional[Dict[int, float]] = None
           ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """DS5 _insa gibi ama dipten önceki fiyat yolu düğümlerle (knot_x = pencere dizini, knot_y = fiyat) verilir; tut = {dizin: kapanış}
    ile seçili mumların kapanışı elle konur (sahte kırılım kurmak için). H = max(O, C) + 0,3; L = min(O, C) - 0,3; O = önceki kapanış.
    dip / post DS5 _insa ile aynı birimlerde."""
    t = 120; d = t - m
    if not (8 <= m <= 100) or len(post) != m or knot_x[-1] != d - 1:
        raise DS6Hata("sentetik: m / post uzunluğu / düğüm")
    k = np.arange(d)
    p = np.interp(k, np.array(knot_x, float), np.array(knot_y, float))
    for j, v in (tut or {}).items():
        p[j] = v
    O = np.r_[p[0], p[:-1]].astype(float); C = p.astype(float)
    H = np.maximum(O, C) + 0.3; L = np.minimum(O, C) - 0.3
    a0 = D5._atr5(np.r_[O, O[-1]], np.r_[H, H[-1]], np.r_[L, L[-1]], np.r_[C, C[-1]], d - 1)
    gb_, yon_, u_, a_ = dip
    base = float(L[:d].min()) - 1.0
    Bd = base + a_ * a0
    Od, Cd = (Bd, Bd + gb_ * a0) if yon_ >= 0 else (Bd + gb_ * a0, Bd)
    Hd = max(Od, Cd) + u_ * a0; Ld = Bd - a_ * a0
    O = np.r_[O, Od]; C = np.r_[C, Cd]; H = np.r_[H, Hd]; L = np.r_[L, Ld]
    atr = D5._atr5(O, H, L, C, d)
    for (off, gb, uf, af) in post:
        b = Bd + off * atr; g = abs(gb) * atr
        o, c = (b, b + g) if gb >= 0 else (b + g, b)
        O = np.r_[O, o]; C = np.r_[C, c]; H = np.r_[H, max(o, c) + uf * atr]; L = np.r_[L, b - af * atr]
    if len(C) != 121:
        raise DS6Hata("sentetik uzunluk")
    return O, H, L, C


# S13 / S13b ön kısmı: d = 108 (m = 12); sivri tek zirve (dizin 13, 160) + alçalan tepeler 140 / 131,2 / 122,4 / 113,6 (dizin 28 / 50 / 72 / 94;
# eğim -0,4 / mum, aynı doğru üstünde) + dibe iniş.
_S13_X = [0, 9, 13, 17, 22, 28, 39, 50, 61, 72, 83, 94, 107]
_S13_Y = [118.0, 119.0, 160.0, 121.0, 124.0, 140.0, 125.0, 131.2, 116.0, 122.4, 107.0, 113.6, 102.0]
# S14 ön kısmı: d = 108; alçalan tepeler 150 / 140 / 130 / 120 (dizin 12 / 32 / 52 / 72; eğim -0,5) + T3'ten (dizin 52) sonra üç mum kapanışı
# tepe hizasında kalıyor (çizgi 0,5 / mum düşerken): kapanış çizgiyi ~1 puan deliyor, sonra iniş (sahte kırılım; delen mumlar pivot değil).
_S14_X = [0, 12, 22, 32, 42, 52, 62, 72, 107]
_S14_Y = [146.0, 150.0, 133.0, 140.0, 123.0, 130.0, 113.0, 120.0, 102.0]
_S14_TUT = {53: 130.0, 54: 129.8, 55: 129.6}


def ds6_sentetik() -> Dict[str, Dict[str, Any]]:
    """DS5'in 12 serisi (ds5.ds5_sentetik, aynen) yeni tanımla yeniden beklenen + S13-S16. dusen = V1'i düşürmesi beklenen parçalar (TAM küme)."""
    S5 = D5.ds5_sentetik()
    S: Dict[str, Dict[str, Any]] = {}
    gerekce = {
        "S1": ("VAR", [], {"V2": True, "V3": True}, "değişmez: ön kısmın dört tepesi aynı doğru üstünde (alçalan tepeler çizgisi = DS5 H1-H2 "
                                                    "çizgisi), çizgi temiz, tırmanış kırıyor"),
        "S2": ("VAR", [], {"V2": True, "V3": True}, "değişmez: yatay taban, temiz alçalan tepeler çizgisi kırılıyor"),
        "S3": ("YOK", ["P3", "P5"], {"V2": False, "V3": False}, "değişmez: tek mum sıçrama; takip yok, kırılımdan sonra dokunuş yok"),
        "S4": ("YOK", ["P2"], {"V2": False, "V3": False}, "değişmez: mavi çizgi 12 mumda ~1,4 ATR aşağı (> 0,5 ATR; D3 toleransını aşar)"),
        "S5": ("YOK", ["P4"], {"V2": False, "V3": False}, "değişmez: dip fitille ~0,55 ATR delinmiş"),
        "S6": ("YOK", ["P1"], {"V2": False, "V3": False}, "değişmez: düşüş yok (< %20)"),
        "S7": ("YOK", ["P3", "P5"], {"V2": False, "V3": False}, "değişmez: dokunuşlar yalnız ilk 3 mumda (ve kırılımdan önce)"),
        "S8": ("YOK", ["P5"], {"V2": False, "V3": False}, "değişmez: basit tepki, kapanışlar alçalan tepeler çizgisinin altında; V2 de YOK "
                                                         "(kırılım yok); V3 (DS5 V1) YOK çünkü DS5 P5 de düşer — DS5'te V3 'P5 yok' "
                                                         "varyantıydı, burada V3 = DS5 V1"),
        "S9": ("YOK", ["P5"], {"V2": False, "V3": False}, "değişmez: tek mum kırılım, sonra çizgi altına dönüş"),
        "S10": ("YOK", ["P4"], {"V2": False, "V3": False}, "değişmez: dip t-3'te ~2 ATR delinmiş"),
        "S11": ("VAR", [], {"V2": True, "V3": True}, "değişmez (DS6'da V2 = D2'siz V1; fitil şartı yok -> V2 VAR)"),
        "S12": ("YOK", ["P3"], {"V2": False, "V3": False}, "değişmez: ilk yarıda dokunuş yok"),
    }
    for ad, s in S5.items():
        bv, du, ek, gr = gerekce[ad]
        S[ad] = {"tarif": s["tarif"], "seri": s["seri"], "beklenen": {"V1": bv == "VAR", **ek}, "dusen": du, "gerekce": gr}
    dip = (0.6, -1, 0.2, 0.3)
    # S13: sivri tek zirve + uzun alçalan tepeler; dizi sivri zirve çizgisini (DS5 H1-H2) kırıyor ama alçalan tepeler çizgisinin altında kalıyor
    s13 = [((0.03 if k in (2, 5, 8, 11) else 0.45 + 0.08 * (k % 3)), 0.3 if k % 2 else -0.3, 0.1, 0.05) for k in range(1, 13)]
    S["S13"] = {"tarif": "sivri tek zirve (t-107) + sonra uzun alçalan tepeler (4 tepe, aynı doğru); dipten sonra yatay gövde tabanı; kapanışlar "
                         "sivri zirve çizgisinin (DS5 H1-H2) üstüne çıkıyor ama alçalan tepeler çizgisinin altında",
                "seri": _insa6(_S13_X, _S13_Y, 12, dip, s13), "beklenen": {"V1": False, "V2": False, "V3": True}, "dusen": ["P5"],
                "gerekce": "kırmızı çizgi alçalan tepelerden (Ha = t-92, 4 dokunuş), sivri zirveden değil; dizi bu çizgiyi kırmıyor -> V1 YOK (P5); "
                           "DS5 sivri zirveden dik çizgi çiziyordu -> V3 VAR (Cemal'in s13 itirazı)", "ha_t": -92, "ds5_h1_t": -107}
    # S13b: aynı ön kısım; dizi yükselen gövde tabanıyla alçalan tepeler çizgisini de kırıyor
    s13b = [(0.2 * k + (0.03 if k in (2, 5, 8, 11) else 0.7), 0.6 if k % 2 else -0.5, 0.15, 0.05) for k in range(1, 13)]
    S["S13b"] = {"tarif": "S13 ön kısmı; dipten sonra gövde altları yükselen çizgiyle 4 dokunuş ve kapanışlar alçalan tepeler çizgisini kırıyor",
                 "seri": _insa6(_S13_X, _S13_Y, 12, dip, s13b), "beklenen": {"V1": True, "V2": True, "V3": True}, "dusen": [],
                 "gerekce": "alçalan tepeler çizgisi temiz ve kırılıyor -> V1 VAR", "ha_t": -92, "ds5_h1_t": -107}
    # S14: alçalan tepeler çizgisi d'den önce bir kez kapanışla delinmiş (sahte kırılım), sonra öbek kırıyor
    s14 = [((0.03 if k in (2, 5, 8, 11) else 0.8 + 0.3 * (k % 3)), 0.5 if k % 2 else -0.6, 0.2, 0.08) for k in range(1, 13)]
    S["S14"] = {"tarif": "alçalan tepeler çizgisi (4 tepe) T3'ten sonra üç mum kapanışla delinmiş, geri dönmüş; dipten sonra yatay taban "
                         "öbeği çizgiyi kırıyor",
                "seri": _insa6(_S14_X, _S14_Y, 12, dip, s14, tut=_S14_TUT), "beklenen": {"V1": False, "V2": True, "V3": True}, "dusen": ["D2"],
                "gerekce": "kapanışla kesilmemiş aday çizgi yok (bütün tepeler aynı doğruda; delinme son iki tepe arasında, delen mumlar pivot değil; daha önce delinme olsaydı delinmeden sonra başlayan geçerli çizgi seçilirdi) -> kirli, sahte kırılım 1 "
                           "-> V1 YOK (D2); V2 (temizlik yok) VAR; DS5 aynı çizgiyi temizliğe bakmadan kullanır -> V3 VAR", "ha_t": -108}
    # S15: mavi çizgi 0,3 ATR aşağı eğik (12 mumda) yatay taban + temiz kırılım
    s15 = [(-0.025 * k + (0.0 if k in (3, 6, 9, 12) else 0.8 + 0.3 * (k % 3)), 0.5 if k % 2 else -0.6, 0.2, 0.08) for k in range(1, 13)]
    S["S15"] = {"tarif": "mavi çizgi dipten sona 0,3 ATR aşağı eğik yatay taban (4 dokunuş) + temiz alçalan tepeler çizgisi kırılımı",
                "seri": D5._insa(12, (0.6, -1, 0.2, 0.8), s15), "beklenen": {"V1": True, "V2": True, "V3": False}, "dusen": [],
                "gerekce": "toplam düşüş 0,3 ATR <= 0,5 -> P2' DOĞRU -> V1 VAR; DS5 P2 (20 mumda en çok 0,05 ATR) düşer -> V3 YOK (Cemal'in s23 "
                           "itirazı)"}
    # S16: mavi çizgi 1 ATR aşağı eğik
    s16 = [(-1.0 / 12 * k + (0.0 if k in (3, 6, 9, 12) else 0.8 + 0.3 * (k % 3)), 0.5 if k % 2 else -0.6, 0.2, 0.08) for k in range(1, 13)]
    S["S16"] = {"tarif": "mavi çizgi dipten sona 1 ATR aşağı eğik (4 dokunuş), dip korunuyor, temiz kırılım",
                "seri": D5._insa(12, (0.6, -1, 0.2, 1.3), s16), "beklenen": {"V1": False, "V2": False, "V3": False}, "dusen": ["P2"],
                "gerekce": "toplam düşüş ~1 ATR > 0,5 -> P2' YANLIŞ"}
    return S


def ds6_test() -> Dict[str, Any]:
    ds6_cakisma_kontrol()
    tablo = []
    SS = ds6_sentetik()
    for ad, s in SS.items():
        r = ds6_parca_dizi(*s["seri"])
        cik = {v: bool(r[v]) for v in ("V1", "V2", "V3")}
        esit = all(cik[v] == x for v, x in s["beklenen"].items()) and ds6_dusen(r) == s["dusen"]
        t = r["t_idx"]
        tablo.append({"seri": ad, "tarif": s["tarif"], "gerekce": s["gerekce"], "beklenen_V1": "VAR" if s["beklenen"]["V1"] else "YOK",
                      "beklenen_dusen": s["dusen"], "beklenen_ek": {v: ("VAR" if x else "YOK") for v, x in s["beklenen"].items() if v != "V1"},
                      "cikan": {v: ("VAR" if x else "YOK") for v, x in cik.items()}, "dusen": ds6_dusen(r),
                      **{p: r[p] for p in ("P1", "P2", "P3", "P4", "D2", "P5")}, "d": r["d_idx"] - t, "m": r["m"],
                      "mavi_dusus_atr": round(r["mavi_dusus_atr"], 3), "dokunus_n": r["dokunus_n"], "ilk": r["dokunus_ilk"],
                      "ikinci": r["dokunus_ikinci"], "min_post_low_atr": round(r["min_post_low_atr"], 3),
                      "ha": r["ha_idx"] - t if r["ha_idx"] >= 0 else None, "hb": r["hb_idx"] - t if r["hb_idx"] >= 0 else None,
                      "tepe_dokunus_n": r["tepe_dokunus_n"], "gecerli": r["gecerli_secildi"], "sahte_n": r["sahte_n"],
                      "ds5_h1": r["ds5_h1_idx"] - t if r["ds5_h1_idx"] >= 0 else None,
                      "kirilim": r["kirilim_idx"] - t if r["kirilim_idx"] >= 0 else None, "ust_n": r["ust_kapanis_n"], "son_ust": r["son_ust"],
                      "esit": esit})
    bozuk = [x["seri"] for x in tablo if not x["esit"]]
    if bozuk:
        raise AssertionError(f"sentetik seriler beklenenden farklı: {bozuk}: " + json.dumps([x for x in tablo if not x["esit"]], ensure_ascii=False))
    T = {x["seri"]: x for x in tablo}
    # S13: çizgi alçalan tepelerden (sivri zirveden değil); DS5 H1 sivri zirve
    for ad in ("S13", "S13b"):
        assert T[ad]["ha"] == SS[ad]["ha_t"] and T[ad]["ds5_h1"] == SS[ad]["ds5_h1_t"] and T[ad]["tepe_dokunus_n"] >= 4 and T[ad]["gecerli"], T[ad]
    assert T["S14"]["sahte_n"] == 1 and not T["S14"]["gecerli"] and T["S14"]["tepe_dokunus_n"] == 4 and T["S14"]["ha"] == SS["S14"]["ha_t"], T["S14"]
    assert 0.25 <= T["S15"]["mavi_dusus_atr"] <= 0.35 and 0.9 <= T["S16"]["mavi_dusus_atr"] <= 1.1, (T["S15"], T["S16"])
    for ad in ("S1", "S2", "S11", "S15"):
        assert T[ad]["gecerli"] and T[ad]["sahte_n"] == 0 and T[ad]["tepe_dokunus_n"] >= 3, T[ad]
    # tanım değişmezleri: geçerli seçilmiş çizgide [a, d] kapanışları <= çizgi + 0,25 ATR ve sahte 0; tepe dokunuşları Ha ve Hb'yi içerir
    for ad, s in SS.items():
        O, H, L, C = s["seri"]; r = ds6_parca_dizi(O, H, L, C)
        if r["cizgi_var"]:
            a, d = r["ha_idx"], r["d_idx"]; ii = np.arange(a, d + 1)
            assert r["ha_idx"] in r["tepe_dokunus"] and r["hb_idx"] in r["tepe_dokunus"], ad
            if r["gecerli_secildi"]:
                assert np.all(C[ii] <= r["ha"] + r["egim_dusen"] * (ii - a) + 0.25 * r["atr_d"] + 1e-9) and r["sahte_n"] == 0, ad
    # prefix değişmezliği: t sonrası veri değişince sonuç aynı (dizi ve DataFrame)
    rng = np.random.default_rng(11); n = 260
    Cx = 100 + np.cumsum(rng.normal(0, 1, n)); Ox = Cx + rng.normal(0, .3, n)
    Hx = np.maximum(Ox, Cx) + abs(rng.normal(0, .5, n)) + .1; Lx = np.minimum(Ox, Cx) - abs(rng.normal(0, .5, n)) - .1
    Cx, Ox, Hx, Lx = (a - min(Lx.min(), 0) + 5 for a in (Cx, Ox, Hx, Lx))
    for i in (150, 200, 230):
        s = slice(i - 120, i + 1)
        x1 = ds6_parca_dizi(Ox[s], Hx[s], Lx[s], Cx[s])
        O2, H2, L2, C2 = Ox.copy(), Hx.copy(), Lx.copy(), Cx.copy()
        O2[i + 1:] = 1; H2[i + 1:] = 2; L2[i + 1:] = 0.5; C2[i + 1:] = 1.5
        x2 = ds6_parca_dizi(O2[s], H2[s], L2[s], C2[s])
        assert json.dumps(x1, sort_keys=True) == json.dumps(x2, sort_keys=True), "DS6 t sonrasına bağlı"
    idx = pd.bdate_range("2020-01-01", periods=n)
    D1 = pd.DataFrame({"Open": Ox, "High": Hx, "Low": Lx, "Close": Cx}, index=idx)
    D2 = D1.copy(); D2.iloc[201:] = [1.0, 2.0, 0.5, 1.5]
    t = idx[200]
    y1 = ds6_parca(D1[D1.index <= t].iloc[-121:]); y2 = ds6_parca(D2[D2.index <= t].iloc[-121:])
    assert json.dumps(y1, sort_keys=True) == json.dumps(y2, sort_keys=True), "prefix (DataFrame) değişmezliği bozuk"
    # pencere boyu ve geçersiz bar denetimi
    for bozuk_ in ((Ox[:100], Hx[:100], Lx[:100], Cx[:100]), (Ox[:121], Lx[:121], Hx[:121], Cx[:121])):
        try:
            ds6_parca_dizi(*bozuk_); raise AssertionError("bozuk pencere kabul edildi")
        except DS6Hata:
            pass
    assert ds6_hukum(0.7, 0.45, 79) == "YARI BAĞIMSIZ GEÇERLİ" and ds6_hukum(0.7, 0.3, 79) == "KISMEN"
    assert ds6_hukum(0.5, 0.2, 79) == "KISMEN" and ds6_hukum(0.3, 0.1, 79) == "GEÇERSİZ" and ds6_hukum(0.9, 0.8, 20).startswith("ÖLÇÜLEMEDİ")
    return {"tamam": True, "kural_sha": _kural_sha6(), "esik_sha": _sha_esik6(), "tablo": tablo}


# ================================================================ 5) MÜHÜR
DS6_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralın uyumu, kappa)"),
    "K2": ("EVET", "bütün parçalar yalnız kör sayfa penceresinden: tanim2.tz_pencere (veri t'de KESİK, 121 bar) + ds5_pencere mekanik denetimi "
                   "(W.index.max() <= t, W.index[-1] == t, 121 bar); alçalan tepeler çizgisi ve sahte kırılım yalnız [t-119 .. d], pivot j+5 <= d; "
                   "kırılım ve mavi çizgi d+1 .. t; ds6.py test prefix değişmezliği (3 kesik + DataFrame); getiri / sinyal sonrası fiyat okunmaz; "
                   "kör set işaretleri ve önceki sonuç dosyaları mühürden önce açılmadı (olc açılış zamanı DS6_SONUC'ta); cemal_ds5_onay.json "
                   "(tanım geri bildirimi, kör set etiketi değil) iş tanımı izniyle okundu"),
    "K3": ("EVET", "GE.ge_hazir geçerli bar (goz_uyum ile aynı); ds6_parca_dizi -> ds5_parca_dizi NaN / H <= L / L <= 0 görürse durur (testte sınandı)"),
    "K4": ("EVET", "80 sayfa set 1 + set 2 ile aynı (aynı hissede en çok 1 sayfa); görsel onay 12 yeni sayfası iki set, DS4 ve DS5 görsel onay "
                   "setlerinin (pazar, sembol) çiftleri hariç, her çift en çok 1 sayfa; ilk 24 sayfa bilerek DS5_ONAY ile aynı"),
    "K5": ("UYGULANMAZ", "giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik"),
    "K6": ("EVET", "tek kip V_*.pkl (goz_uyum ile aynı); düşüş oranı birimsiz, eğim / dokunuş / kesme / tepe dokunuşu ATR14(d) biriminde"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok"),
    "K8": ("EVET", "79-80 karar (iki set); karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); 3 varyant: Bonferroni 3 (%98,33) V2 / V3 için; "
                   "hüküm yalnız V1 ve 'YARI BAĞIMSIZ' (düzeltme Cemal'in DS5_ONAY işaretlerinden; iki set önceki DS3-DS5 işlerinde kullanıldı); "
                   "set 1 ve set 2 ayrı; kural kör set etiketlerinden SEÇİLMEDİ; kesin hüküm üçüncü bağımsız kör setle; 24 eski onay sayfası "
                   "tablosu yalnız bilgi"),
    "K9": ("EVET", "kural + DS6_ESIK + sentetik test ADIM 1'de kör set etiketleri açılmadan commit; 80 yanıt ds6_anahtar.json + görsel onay "
                   "(DS6_ONAY.pdf, ds6_onay_anahtar.json) etiket açılmadan mühürlü; ds6.py + ds5.py + ds6_anahtar.json + DS6_ESIK + kural "
                   "kaynağı + PDF + onay anahtarı sha'ları bu dosyada; olc sha'ları denetler ve 80 yanıtı veriden yeniden hesaplayıp mühürle "
                   "karşılaştırır; hüküm eşikleri sabit"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırma yok; yalnız OHLCV"),
    "K11": ("EVET", "ds6.py anahtar / onay aynı komutla deterministik yeniden üretilir (tohum 20261127; havuz sha DS4 / DS5 havuzuyla eşit şartı); "
                    "V3 ds5_anahtar.json mühürlü DS5 V1 ile ve eski 24 sayfada ds5_onay_anahtar.json V1 ile eşit şartı; olc 80 sayfanın yanıtını "
                    "veriden yeniden hesaplar, mühürle eşitliğini şart koşar; sentetik seriler beklenen yanıt ve düşen parçayla birebir"),
    "K12": ("EVET", "iddia yok; yalnız 'uyum' ve 'kappa' sayısı; hüküm sözü yalnız ön kayıttaki eşikle ve yalnız V1 için; 'YARI BAĞIMSIZ' sınırı yazılı"),
    "K13": ("EVET", "çakışma kapısı _CK_ONCE_DS6 + test; yasak dosyalar (defter, mevcut .py dahil ds5.py, anahtar / ön kayıt / sonuç dosyaları) "
                    "değişmedi (git diff boş); e-posta / anahtar yok (_yaz / _jyaz e-posta taraması); git add -A yok; PDF Cemal'e gönderilmedi"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


def _sentetik_tablo6(T: Dict[str, Any]) -> List[str]:
    st = ["| seri | tarif | beklenen V1 (düşen); V2 / V3 | gerekçe | çıkan V1 / V2 / V3 | P1 | P2' | P3 | P4 | D2 | P5 | mavi düşüş (ATR) | "
          "dokunuş (ilk / ikinci) | kırmızı Ha / Hb (tepe dokunuşu; geçerli; sahte) | DS5 H1 | kırılım / üst kapanış | eşit |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in T["tablo"]:
        b = x["beklenen_V1"] + (f" ({', '.join(x['beklenen_dusen'])})" if x["beklenen_dusen"] else "") + \
            ("; " + ", ".join(f"{k} {v}" for k, v in x["beklenen_ek"].items()) if x["beklenen_ek"] else "")
        c = " / ".join(x["cikan"][v] for v in ("V1", "V2", "V3"))
        hh = (f"t{x['ha']:+d} / t{x['hb']:+d} ({x['tepe_dokunus_n']}; {'evet' if x['gecerli'] else 'HAYIR'}; {x['sahte_n']})"
              if x["ha"] is not None else "-")
        st.append(f"| {x['seri']} | {x['tarif']} | {b} | {x['gerekce']} | {c} | {_isr6(x['P1'])} | {_isr6(x['P2'])} | {_isr6(x['P3'])} | "
                  f"{_isr6(x['P4'])} | {_isr6(x['D2'])} | {_isr6(x['P5'])} | {x['mavi_dusus_atr']:.2f} | {x['dokunus_n']} ({x['ilk']} / {x['ikinci']}) | "
                  f"{hh} | {('t%+d' % x['ds5_h1']) if x['ds5_h1'] is not None else '-'} | "
                  f"{('t%+d' % x['kirilim']) if x['kirilim'] is not None else '-'} / {x['ust_n']} | {'EVET' if x['esit'] else 'HAYIR'} |")
    return st


def ds6_muhur() -> str:
    for y in (DS6_YOL["anahtar"], DS6_YOL["is_tanimi"], DS6_YOL["pdf"], DS6_YOL["onay_anahtar"]):
        if not os.path.exists(y):
            raise DS6Hata(f"mühür için dosya yok: {y}")
    J = json.load(open(DS6_YOL["anahtar"], encoding="utf-8")); JO = json.load(open(DS6_YOL["onay_anahtar"], encoding="utf-8"))
    for ad, X in (("anahtar", J), ("onay", JO)):
        if X["esik_sha"] != _sha_esik6():
            raise DS6Hata(f"DS6_ESIK {ad} dosyasından sonra değişmiş")
        if X["kural_sha"] != _kural_sha6():
            raise DS6Hata(f"kural kaynağı {ad} dosyasından sonra değişmiş")
    if JO["pdf_sha"] != GU._sha(DS6_YOL["pdf"]):
        raise DS6Hata("DS6_ONAY.pdf onay anahtarından sonra değişmiş")
    T = ds6_test()
    ad = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
          "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
          "K13": "süreç", "K14": "boyut (gerçek para)"}
    tab = "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |\n|---|---|---|---|\n"
    for k, (yy, kn) in DS6_KONTROL.items():
        tab += f"| {k} | {ad[k]} | {yy} | {kn} |\n"
    st = _sentetik_tablo6(T)
    oz = J["ozet"]
    ot = ["| küme | n | P1 | P2' | (DS5 P2) | P3 | P4 | D2 temiz | P5 kırılım | geçerli çizgi | V1 VAR | V2 VAR | V3 (DS5 V1) VAR |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k_, o in oz.items():
        ot.append(f"| {k_} | {o['n']} | {o['P1_DOGRU']} | {o['P2_DOGRU']} | {o['P2_ds5_DOGRU']} | {o['P3_DOGRU']} | {o['P4_DOGRU']} | "
                  f"{o['D2_DOGRU']} | {o['P5_DOGRU']} | {o['gecerli_secildi_DOGRU']} | {o['V1_VAR']} | {o['V2_VAR']} | {o['V3_VAR']} |")
    on = ["| sayfa | pazar | grup | v5 V1 | v6 V1 | V2 | P1 | P2' (mavi düşüş ATR) | P3 (dokunuş) | P4 | D2 (sahte; geçerli) | P5 (üst kapanış) | "
          "Ha / Hb (t'ye göre; tepe dok.) | DS5 H1 / H2 | düşen parça |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in JO["sayfalar"]:
        t = int(s["t_idx"])
        hh = f"t{s['ha_idx'] - t:+d} / t{s['hb_idx'] - t:+d} ({s['tepe_dokunus_n']})" if s["ha_idx"] >= 0 else "-"
        h5 = (f"t{s['ds5_h1_idx'] - t:+d} / t{s['ds5_h2_idx'] - t:+d}" if s["ds5_h1_idx"] >= 0 and s["ds5_h2_idx"] >= 0 else "-")
        on.append(f"| {s['sayfa']} | {s['pazar']} | {s['grup']} | {s['yanit']['V3']} | {s['yanit']['V1']} | {s['yanit']['V2']} | "
                  f"{_isr6(s['P1'])} | {_isr6(s['P2'])} ({s['mavi_dusus_atr']:.2f}) | {_isr6(s['P3'])} ({s['dokunus_n']}) | {_isr6(s['P4'])} | "
                  f"{_isr6(s['D2'])} ({s['sahte_n']}; {'evet' if s['gecerli_secildi'] else 'hayır'}) | {_isr6(s['P5'])} ({s['ust_kapanis_n']}) | "
                  f"{hh} | {h5} | {', '.join(s['V1_dusen']) or '-'} |")
    bel = "\n".join(f"- {k}: {v}" for k, v in DS6_ESIK["belirsizlik"].items())
    m = f"""# DİP SAVUNMASI v6 (DS6) — ÖN KAYIT (Cemal'in kör set işaretleri AÇILMADAN mühürlenir)

Üretim: {GU._simdi()} (UTC). Soru: DS5 kuralı Cemal'in DS5_ONAY işaretlerine göre üç noktada düzeltilince (D1 alçalan tepeler çizgisi, D2 kirli çizginin kırılımı sayılmaz, D3 hafif aşağı eğik mavi çizgi yatay), iki kör sette (GOZ_UYUM_KOR.pdf = set 1, TANIM2_KOR.pdf = set 2; 80 sayfa) Cemal'in VAR / YOK işaretleriyle örtüşüyor mu? Ayrıca DS5_ONAY'ın aynı 24 sayfası + 12 yeni sayfalık GÖRSEL ONAY PDF'i (Cemal'e gönderilmedi). GETİRİ ÖLÇÜLMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/ds6_anahtar.json` sha256: `{GU._sha(DS6_YOL['anahtar'])}`
- kod: `arastirma_cikti/goz_uyum/ds6.py` sha256: `{GU._sha(DS6_YOL['kod'])}`
- içe alınan kural kodu: `arastirma_cikti/goz_uyum/ds5.py` sha256: `{GU._sha(DS6_YOL['ds5_kod'])}` (değiştirilmedi)
- eşik sözlüğü (DS6_ESIK) sha256: `{_sha_esik6()}`
- kural kaynağı (_ds6_pivot + _ds6_dusen + ds6_parca_dizi + ds6_parca + DS5 kural sha) sha256: `{_kural_sha6()}`
- görsel onay PDF: `arastirma_cikti/goz_uyum/DS6_ONAY.pdf` sha256: `{GU._sha(DS6_YOL['pdf'])}`
- görsel onay anahtarı: `arastirma_cikti/goz_uyum/ds6_onay_anahtar.json` sha256: `{GU._sha(DS6_YOL['onay_anahtar'])}`
- iş tanımı: `arastirma_cikti/goz_uyum/DS6_IS_TANIMI.md` sha256: `{GU._sha(DS6_YOL['is_tanimi'])}`
- girdi (yalnız sayfa -> pazar, sembol, sinyal günü okundu): goz_uyum_anahtar.json `{J['girdi_sha']['goz_uyum_anahtar.json']}`, tanim2_anahtar.json `{J['girdi_sha']['tanim2_anahtar.json']}`; V3 denetimi ds5_anahtar.json `{J['girdi_sha']['ds5_anahtar.json']}`; onay: ds5_onay_anahtar.json `{GU._sha(DS6_YOL['ds5_onay_anahtar'])}`, ds4_onay_anahtar.json `{GU._sha(DS6_YOL['ds4_onay_anahtar'])}`; tanım geri bildirimi cemal_ds5_onay.json `{GU._sha(DS6_YOL['cemal_ds5_onay'])}`
- olay havuzu (pazar, sembol, tarih) sha256: `{JO['havuz_sha']}` (DS4 / DS5 görsel onay havuzuyla aynı)
- havuz bilgisi: {json.dumps(JO['havuz'], ensure_ascii=False)}
- bağımlı kod: goz_uyum.py `{GU._sha(GU.GU_YOL['kod'])[:16]}`, tanim2.py `{GU._sha(TZ.TZ_YOL['kod'])[:16]}`

## 2. Kural (ADIM 1'de, kör set etiketleri açılmadan commit; parametreler iş tanımından aynen)
DS5 aynen (pencere 121 bar, t'de kesik; kural penceresi son 120 mum; B_i = min(Open_i, Close_i); ATR = ATR14(d)): DİP d (en düşük Low, d <= t-8), P1 düşüşten dip (>= %20), MAVİ çizgi (çapa (d, B_d), s* = min (B_i - B_d) / (i - d)), P3 takip (0,35 ATR, >= 3 dokunuş, iki yarıda), P4 dip korunur (0,25 ATR). Üç değişiklik:
- **D3 / P2' YATAY TOLERANSI**: mavi çizginin dipten t'ye toplam düşüşü (-s* x m) <= 0,5 ATR; yukarı eğim serbest (DS5: 20 mumda en çok 0,05 ATR).
- **D1 DÜŞEN ÇİZGİ = ALÇALAN TEPELER ÇİZGİSİ**: d'den önceki pivot tepeler (5/5, pivot + 5 <= d); aday = her pivot çifti (Ha, Hb), a < b, High(Hb) < High(Ha); geçerli = Ha ile d arasında hiçbir kapanış çizginin 0,25 ATR üstüne çıkmaz ve Ha'dan önceki 5 mumda Ha'dan yüksek High yok; seçim = en çok pivot tepenin çizgiye 0,5 ATR'den yakın olduğu çizgi, eşitlikte daha uzun (Ha solda), sonra daha yatık. Geçerli çizgi yoksa en çok dokunuşlu aday çizilir ve KİRLİ sayılır. (DS5: H1 = en yüksek pivot tepe, H2 = H1'den sonraki son alçak pivot.)
- **D2 ÇİZGİNİN TEMİZLİĞİ**: seçilen çizgi için d'den önce kapanışın çizginin 0,25 ATR üstüne çıkıp sonra yeniden altına döndüğü sahte kırılım sayısı. P5' = (sahte kırılım 0 ve geçerli çizgi) ∧ DS5 kırılım şartı (dipten sonra >= 3 kapanış çizgi üstünde, son kapanış üstte, kırılımdan sonra mavi çizgiye dokunuş) bu yeni çizgiye göre.
- **V1 (ANA)** = P1 ∧ P2' ∧ P3 ∧ P4 ∧ P5'. **V2** = V1 ama D2 temizlik şartı yok. **V3** = DS5 V1 (karşılaştırma). Bonferroni 3.

Tanım belirsizliklerinin çözümü (kör set etiketlerinden önce yazıldı):
{bel}

DS6_ESIK (tam): `{json.dumps(DS6_ESIK, ensure_ascii=False, sort_keys=True)}`

## 3. Sentetik sınama (`python arastirma_cikti/goz_uyum/ds6.py test`; gerçek veriden ÖNCE; dizinler t'ye göre)
{chr(10).join(st)}

Ek testler: S13 / S13b'de kırmızı çizginin başı (Ha) alçalan tepelerin ilki, DS5 H1 sivri zirve; S14 kirli (geçerli aday yok, sahte 1, 4 tepe dokunuşu); S15 mavi düşüş 0,25-0,35 ATR, S16 0,9-1,1 ATR; tanım değişmezleri (geçerli çizgide [Ha, d] kapanışları <= çizgi + 0,25 ATR ve sahte 0; tepe dokunuşları Ha ve Hb'yi içerir); prefix değişmezliği (3 kesik, dizi + DataFrame); kısa pencere ve H <= L penceresi reddedilir; hüküm fonksiyonu. Sonuç: {sum(x['esit'] for x in T['tablo'])} / {len(T['tablo'])} seri beklenene (V1 / V2 / V3 ve düşen parça kümesi) eşit.

## 4. Mühürlü yanıtlar (ds6_anahtar.json 'sayfalar'; Cemal'in işaretleri AÇILMADAN yazıldı)
{chr(10).join(ot)}

## 5. Görsel onay PDF'i (DS6_ONAY.pdf; 1-24 DS5_ONAY ile aynı hisse / gün, 25-36 yeni; anahtar ds6_onay_anahtar.json)
Seçim: {DS6_ESIK['onay']['secim']}.

{chr(10).join(on)}

## 6. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in set 1 (cemal_isaret.json) ve set 2 (cemal_isaret2.json) VAR / YOK işaretleri ile V1 / V2 / V3 arasında uyum ve Cohen kappa; set 1, set 2 ve birleşik; işaretsiz / '?' sayfa karar dışı, sayısı ayrıca yazılır.
- Aralık: kappa bootstrap (B {DS6_ESIK['kappa']['B']}, tohum {DS6_ESIK['kappa']['tohum']}, sayfa yeniden örneklemesi, yüzdelik): V1 için %95; V2 / V3 için Bonferroni 3 ile %98,33 (ayrıca %95 bilgi).
- HÜKÜM: {DS6_ESIK['hukum']}.
- Ek bilgi (hüküm dışı): uyuşmayan sayfalar ve düşen parça (P1 / P2 / P3 / P4 / D2 / P5); Cemal VAR / kod YOK sayfalarda düşen parça sayımı; DS5 V1 (= V3) ve GOVDE_1 ile aynı sayfalarda karşılaştırma; DS5_ONAY 24 sayfasında cevap değişimi tablosu ({DS6_ESIK['eski24_bilgi']}).
- Kural ve eşik sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 7. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
{tab}
## 8. Git kaydı (bu dosyanın yazıldığı an)
- ds6.py: {GU._gu_git('arastirma_cikti/goz_uyum/ds6.py')}
- DS6_IS_TANIMI.md: {GU._gu_git('arastirma_cikti/goz_uyum/DS6_IS_TANIMI.md')}
"""
    GU._yaz(DS6_YOL["onkayit"], m)
    import IZ_KARNE as IK
    r = IK.ik_kontrol_kapisi(DS6_YOL["onkayit"])
    d6log.info("kontrol kapısı: %s", "GEÇTİ" if r["gecti"] else r)
    return DS6_YOL["onkayit"]


def _ds6_muhur_oku() -> Dict[str, str]:
    if not os.path.exists(DS6_YOL["onkayit"]):
        raise DS6Hata("ön kayıt yok")
    t = open(DS6_YOL["onkayit"], encoding="utf-8").read(); out = {}
    for ad, desen in (("anahtar", r"ds6_anahtar\.json` sha256: `([0-9a-f]{64})`"), ("kod", r"ds6\.py` sha256: `([0-9a-f]{64})`"),
                      ("ds5kod", r"ds5\.py` sha256: `([0-9a-f]{64})`"),
                      ("esik", r"eşik sözlüğü \(DS6_ESIK\) sha256: `([0-9a-f]{64})`"), ("kural", r"kural kaynağı \([^)]*\) sha256: `([0-9a-f]{64})`"),
                      ("pdf", r"DS6_ONAY\.pdf` sha256: `([0-9a-f]{64})`"), ("onay", r"ds6_onay_anahtar\.json` sha256: `([0-9a-f]{64})`")):
        mm = re.search(desen, t)
        if not mm:
            raise DS6Hata(f"ön kayıtta {ad} sha'sı yok")
        out[ad] = mm.group(1)
    return out


# ================================================================ 6) ÖLÇÜM
def ds6_hukum(k: float, alt: float, n: int) -> str:
    E = DS6_ESIK["kappa"]
    if n < int(E["karar_min"]) or not np.isfinite(k):
        return "ÖLÇÜLEMEDİ (karar sayısı < 30 ya da kappa tanımsız)"
    if k >= E["gecerli"] and np.isfinite(alt) and alt >= E["gecerli_alt"]:
        return "YARI BAĞIMSIZ GEÇERLİ"
    return "KISMEN" if k >= E["kismen"] else "GEÇERSİZ"


def _eski24_tablo(JO: Dict[str, Any]) -> List[Dict[str, Any]]:
    """DS5_ONAY 24 sayfası: DS5 V1 -> DS6 V1 / V2; Cemal'in DS5_ONAY işareti (tanım geri bildirimi) ve mekanik etiket (ön kayıttaki eşleme)."""
    CJ = json.load(open(DS6_YOL["cemal_ds5_onay"], encoding="utf-8"))
    out = []
    for s in JO["sayfalar"]:
        if int(s["sayfa"]) > int(DS6_ESIK["onay"]["eski_sayfa"]):
            continue
        c = CJ.get(str(s["sayfa"]), {}); ci = str(c.get("cemal", "?"))
        v5, v6 = bool(s["ds5_V1"]), bool(s["V1"]); deg = v5 != v6
        cizgi_deg = not (int(s["ha_idx"]) == int(s["ds5_h1_idx"]) and int(s["hb_idx"]) == int(s["ds5_h2_idx"]))
        if ci == "YANLIŞ":
            et = "itiraz yanıtı değişti" if deg else f"yanıt aynı (çizgi {'değişti' if cizgi_deg else 'aynı'})"
        elif ci == "DOĞRU":
            et = "DİKKAT: Cemal'in DOĞRU dediği yanıt değişti" if deg else "korundu"
        else:
            et = "bilgi" + (" (yanıt değişti)" if deg else "")
        out.append({"sayfa": int(s["sayfa"]), "pazar": s["pazar"], "cemal": ci, "cizim": c.get("cizim", ""), "ds5_V1": "VAR" if v5 else "YOK",
                    "ds6_V1": "VAR" if v6 else "YOK", "ds6_V2": "VAR" if s["V2"] else "YOK", "degisti": deg, "cizgi_degisti": cizgi_deg,
                    "sahte_n": int(s["sahte_n"]), "gecerli": bool(s["gecerli_secildi"]), "mavi_dusus_atr": float(s["mavi_dusus_atr"]),
                    "dusen": s["V1_dusen"], "etiket": et})
    return out


def ds6_olc(deneme: bool = False, cemal1: Optional[str] = None, cemal2: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    if not deneme:
        M = _ds6_muhur_oku()
        for ad, gercek in (("anahtar", GU._sha(DS6_YOL["anahtar"])), ("kod", GU._sha(DS6_YOL["kod"])), ("ds5kod", GU._sha(DS6_YOL["ds5_kod"])),
                           ("esik", _sha_esik6()), ("kural", _kural_sha6()), ("pdf", GU._sha(DS6_YOL["pdf"])),
                           ("onay", GU._sha(DS6_YOL["onay_anahtar"]))):
            if gercek != M[ad]:
                raise DS6Hata(f"MÜHÜR BOZUK: {ad} sha'sı ön kayıttakiyle aynı değil -> DURDU")
    J = json.load(open(DS6_YOL["anahtar"], encoding="utf-8"))
    Sm = pd.DataFrame(J["sayfalar"])
    R = ds6_hesap(Sm[["set", "sayfa", "pazar", "sembol", "sinyal_gunu"]])     # K11: yanıtlar veriden yeniden hesaplanır
    for v in ("V1", "V2", "V3", "P1", "P2", "P3", "P4", "D2", "P5"):
        if (R[v].to_numpy(bool) != Sm[v].to_numpy(bool)).any():
            raise DS6Hata(f"{v} yanıtları veriden yeniden hesaplanınca mühürle aynı değil -> DURDU")
    acilis = GU._simdi()
    c1 = cemal1 or DS6_YOL["set1_cemal"]; c2 = cemal2 or DS6_YOL["set2_cemal"]
    et = {1: D5._etiket_oku5(c1), 2: D5._etiket_oku5(c2)}
    d6log.info("etiket dosyaları açıldı: %s (UTC)", acilis)
    for st in (1, 2):
        fazla = sorted(set(et[st]) - set(range(1, 41)))
        if fazla:
            raise DS6Hata(f"set {st} etiketinde anahtarda olmayan sayfa: {fazla}")
    Sm["cemal"] = [et[int(s)].get(int(p), "?") for s, p in zip(Sm.set, Sm.sayfa)]
    E = DS6_ESIK["kappa"]; bon = 1 - (1 - E["guven"]) / E["bonferroni_k"]
    if deneme:
        g1k = {"ozellik": "G1_govde_dokunus_n", "yon": ">=", "esik": 3.0, "not": "DENEME: uydurma kural"}
    else:
        GJ = json.load(open(DS6_YOL["govde_anahtar"], encoding="utf-8")); g1k = dict(GJ["kurallar"]["GOVDE_1"]); del GJ
    Sm["GOVDE_1"] = D5._govde1_cevap5(Sm, g1k)
    kumeler = {"set 1": Sm.set == 1, "set 2": Sm.set == 2, "birleşik": Sm.set > 0}
    sonuc: Dict[str, Any] = {"etiket_acilis_utc": acilis, "deneme": deneme, "n_sayfa": int(len(Sm)), "kume": {}, "govde_kural": g1k}
    modeller = ("V1", "V2", "V3", "GOVDE_1")
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
            huk = (ds6_hukum(k, a95[0], n) if v == "V1" else
                   ("BİLGİ (Bonferroni alt uç ile: " + ds6_hukum(k, abn[0], n) + ")" if v in ("V2", "V3") else "BİLGİ (önceki kural)"))
            kd["model"][v] = {"kod_VAR": int(mod.sum()), "uyum": float(np.mean(cb == mod)) if n else np.nan, "kappa": k, "ar95": a95,
                              "ar_bon": abn, "hukum": huk,
                              "tablo": {"Cemal VAR + kod VAR": tp, "Cemal YOK + kod YOK": tn, "Cemal YOK + kod VAR": fp, "Cemal VAR + kod YOK": fn},
                              "uyusmayan": [f"set {s} / {p}" for s, p in zip(K.set[cb != mod], K.sayfa[cb != mod])]}
        sonuc["kume"][kad] = kd
    pl = ["P1", "P2", "P3", "P4", "D2", "P5"]
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
                   "tepe_dokunus_n": int(r.tepe_dokunus_n), "gecerli": bool(r.gecerli_secildi), "sahte_n": int(r.sahte_n),
                   "ust_kapanis_n": int(r.ust_kapanis_n), "kirilim_m": (int(r.kirilim_idx) - int(r.t_idx)) if int(r.kirilim_idx) >= 0 else None,
                   "dusen": ds6_dusen(rd), "neden": ds6_neden_metni(rd)})
    sonuc["V1_uyusmayan"] = uy
    K = Sm[Sm.cemal != "?"]; cv = (K.cemal == "VAR")
    sonuc["karsilastirma"] = {f"V1_{o}": {"iki_kod_ayni_yanit": int((K.V1.astype(bool) == K[o].astype(bool)).sum()), "karar_n": int(len(K)),
                                          "kod_kappa": GU.gu_kappa(K.V1.to_numpy(bool), K[o].to_numpy(bool)),
                                          "V1_dogru_oteki_yanlis": int(((K.V1.astype(bool) == cv) & (K[o].astype(bool) != cv)).sum()),
                                          "oteki_dogru_V1_yanlis": int(((K.V1.astype(bool) != cv) & (K[o].astype(bool) == cv)).sum())}
                              for o in ("V3", "GOVDE_1")}
    sonuc["V1_V3_degisen"] = [{"sayfa": f"set {r.set} / {r.sayfa}", "cemal": r.cemal, "V3_DS5": "VAR" if r.V3 else "YOK",
                               "V1_DS6": "VAR" if r.V1 else "YOK", "dusen": ds6_dusen(r.to_dict())}
                              for _, r in Sm.iterrows() if bool(r.V1) != bool(r.V3)]
    sonuc["sayfa_cemal"] = {f"{s}/{p}": c for s, p, c in zip(Sm.set, Sm.sayfa, Sm.cemal)}
    JO = json.load(open(DS6_YOL["onay_anahtar"], encoding="utf-8"))
    sonuc["eski24"] = _eski24_tablo(JO)
    md = _sonuc_md6(sonuc)
    hedef = cikti or DS6_DIR
    os.makedirs(hedef, exist_ok=True)
    GU._yaz(os.path.join(hedef, "DS6_SONUC.md"), md)
    GU._jyaz(os.path.join(hedef, "ds6_sonuc.json"), sonuc)
    return sonuc


def _sonuc_md6(S: Dict[str, Any]) -> str:
    B = S["kume"]["birleşik"]; v1 = B["model"]["V1"]
    L = [("# [DENEME — UYDURMA ETİKET] " if S["deneme"] else "# ") + "DİP SAVUNMASI v6 (DS6) — SONUÇ (iki kör set, 80 sayfa)", "",
         (f"Üretim: {GU._simdi()} (UTC). DENEME: uydurma etiket dosyaları; mühür denetimi YAPILMADI; 80 yanıt veriden yeniden hesaplandı, "
          "anahtarla aynı. GETİRİ YOK." if S["deneme"] else
          f"Üretim: {GU._simdi()} (UTC). Etiket dosyaları (cemal_isaret.json, cemal_isaret2.json) bu komutla açıldı: {S['etiket_acilis_utc']} (UTC). "
          "Mühür denetimi: ds6_anahtar.json, ds6.py, ds5.py, DS6_ESIK, kural kaynağı, DS6_ONAY.pdf ve ds6_onay_anahtar.json sha'ları DS6_ON_KAYIT "
          "ile aynı; 80 sayfanın P1-P5, D2 ve V1 / V2 / V3 yanıtı veriden yeniden hesaplandı, mühürle aynı. GETİRİ YOK."), "",
         f"Karar: birleşik {B['karar_n']} (Cemal VAR {B['cemal_VAR']}); işaretsiz / '?' (karar dışı): {B['isaretsiz']} {B['isaretsiz_sayfa']}.", "",
         f"## HÜKÜM (V1, ön kayıttaki eşikle): **{v1['hukum']}** — birleşik kappa {_f6(v1['kappa'])}, %95 [{_f6(v1['ar95'][0])}, {_f6(v1['ar95'][1])}]",
         "", "Sınır: düzeltme Cemal'in DS5_ONAY işaretlerinden yapıldı ve iki set önceki DS3-DS5 işlerinde kullanıldı; sonuç YARI BAĞIMSIZDIR. "
         "Kesin hüküm yalnız Cemal'in görsel onayı (DS6_ONAY.pdf) + üçüncü bağımsız kör setle.", ""]
    s1 = S["kume"]["set 1"]["model"]["V1"]["kappa"]; s2 = S["kume"]["set 2"]["model"]["V1"]["kappa"]
    dus1 = bool(np.isfinite(s1) and s1 < 0.40); dus2 = bool(np.isfinite(s2) and s2 < 0.40)
    if dus1 and dus2:
        L += [f"NOT: V1 kappa set 1 {_f6(s1)}, set 2 {_f6(s2)}: İKİ SETTE DE < 0,40.", ""]
    elif dus1 or dus2:
        L += [f"NOT: **tutarsız** — V1 kappa set 1 {_f6(s1)}, set 2 {_f6(s2)}; biri < 0,40.", ""]
    L += ["## Kappa tablosu", "", "| model | küme | karar | kod VAR | uyum | kappa | %95 aralık | %98,33 (Bonferroni 3) | hüküm |",
          "|---|---|---|---|---|---|---|---|---|"]
    for v in ("V1", "V2", "V3", "GOVDE_1"):
        for kad in ("set 1", "set 2", "birleşik"):
            r = S["kume"][kad]["model"][v]; kd = S["kume"][kad]
            huk = r["hukum"] if kad == "birleşik" else ("ayrı rapor" if v == "V1" else "bilgi")
            L.append(f"| {v} | {kad} | {kd['karar_n']} | {r['kod_VAR']} | {_f6(r['uyum'])} | {_f6(r['kappa'])} | [{_f6(r['ar95'][0])}, "
                     f"{_f6(r['ar95'][1])}] | [{_f6(r['ar_bon'][0])}, {_f6(r['ar_bon'][1])}] | {huk} |")
    L += ["", f"V1 = P1 ∧ P2' ∧ P3 ∧ P4 ∧ P5' (ANA; P5' = D2 temiz ∧ P5 kırılım); V2 = V1 ama D2 yok; V3 = DS5 V1. GOVDE_1 = "
          f"{S['govde_kural'].get('ozellik')} {S['govde_kural'].get('yon')} {S['govde_kural'].get('esik')!r} (eşiği set 1 etiketleriyle seçildi -> "
          "set 1'de iç-örneklem).", "", f"HÜKÜM kuralı (ön kayıt): {DS6_ESIK['hukum']}.", "", "## 2x2", ""]
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
          "| sayfa | Cemal | V1 | V2 | V3 (DS5) | GOVDE_1 | dip yaşı | düşüş | mavi düşüş (ATR) | dokunuş (ilk / ikinci) | dip sonrası en düşük Low "
          "(ATR) | kırmızı: tepe dok. / geçerli / sahte | kırılım / üst kapanış | düşen parça | kodun gördüğü |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in S["V1_uyusmayan"]:
        ne = "; ".join(r["neden"]) if r["neden"] else "altı parça da DOĞRU (kod VAR)"
        L.append(f"| {r['sayfa']} | {r['cemal']} | {r['V1']} | {r['V2']} | {r['V3']} | {r['GOVDE_1']} | {r['m']} | %{r['dusus']*100:.0f} | "
                 f"{r['mavi_dusus_atr']:.2f} | {r['dokunus_n']} ({r['dokunus_ilk']} / {r['dokunus_ikinci']}) | {r['min_post_low_atr']:+.2f} | "
                 f"{r['tepe_dokunus_n']} / {'evet' if r['gecerli'] else 'hayır'} / {r['sahte_n']} | "
                 f"{('t%+d' % r['kirilim_m']) if r['kirilim_m'] is not None else '-'} / {r['ust_kapanis_n']} | {', '.join(r['dusen']) or '-'} | {ne} |")
    L += ["", "## Karşılaştırma: aynı sayfalarda DS5 V1 (= V3) ve GOVDE_1", ""]
    for o, G in S["karsilastirma"].items():
        L.append(f"- {o}: karar {G['karar_n']} sayfada iki kod {G['iki_kod_ayni_yanit']} sayfada aynı yanıt (kodlar arası kappa {_f6(G['kod_kappa'])}); "
                 f"V1 doğru / öteki yanlış {G['V1_dogru_oteki_yanlis']}; öteki doğru / V1 yanlış {G['oteki_dogru_V1_yanlis']}.")
    L += ["", "DS6 V1 ile DS5 V1'in ayrıldığı sayfalar: " + (", ".join(f"{z['sayfa']} (Cemal {z['cemal']}; DS5 {z['V3_DS5']} -> DS6 {z['V1_DS6']}; "
                                                                      f"düşen {','.join(z['dusen']) or '-'})" for z in S["V1_V3_degisen"]) or "yok"), "",
          "## DS5_ONAY'ın 24 sayfasında cevap değişimi (BİLGİ; Cemal'in DS5_ONAY işaretleri tanım geri bildirimi)", "",
          "| sayfa | pazar | Cemal (DS5_ONAY) | v5 V1 | v6 V1 | v6 V2 | V değişti | kırmızı çizgi değişti | sahte / geçerli | mavi düşüş (ATR) | v6 düşen "
          "parça | etiket | Cemal'in çizimi (betim) |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for z in S["eski24"]:
        L.append(f"| {z['sayfa']} | {z['pazar']} | {z['cemal']} | {z['ds5_V1']} | {z['ds6_V1']} | {z['ds6_V2']} | {'EVET' if z['degisti'] else '-'} | "
                 f"{'evet' if z['cizgi_degisti'] else 'hayır'} | {z['sahte_n']} / {'evet' if z['gecerli'] else 'hayır'} | {z['mavi_dusus_atr']:.2f} | "
                 f"{', '.join(z['dusen']) or '-'} | {z['etiket']} | {z['cizim'].replace('|', '/')} |")
    L += ["", "Not: uyum Cemal'in gözüyle uyumdur; getiri ölçülmedi. Kural düzeltmeleri iş tanımından, kör set etiketlerine bakmadan sabitlendi ve "
          "önce sentetik serilerde sınandı."]
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
    if a.deneme and ({os.path.realpath(a.cemal1), os.path.realpath(a.cemal2)} & {os.path.realpath(DS6_YOL["set1_cemal"]),
                                                                                os.path.realpath(DS6_YOL["set2_cemal"])}
                     or os.path.realpath(a.cikti) == os.path.realpath(DS6_DIR)):
        raise SystemExit("--deneme gerçek etiket dosyasını açamaz / gerçek çıktı dizinine yazamaz")
    if not a.deneme and (a.cemal1 or a.cemal2 or a.cikti):
        raise SystemExit("gerçek kipte --cemal1 / --cemal2 / --cikti verilmez (mühürlü yollar kullanılır)")
    if a.komut == "anahtar":
        J = ds6_anahtar(); print(json.dumps(J["ozet"], ensure_ascii=False))
    elif a.komut == "onay":
        J = ds6_onay(a.havuz_onbellek)
        print(json.dumps([(s["sayfa"], s["pazar"], s["grup"], s["yanit"]["V3"], s["yanit"]["V1"], s["V1_dusen"], s["sahte_n"])
                          for s in J["sayfalar"]], ensure_ascii=False))
        print(json.dumps(J["havuz"], ensure_ascii=False))
    elif a.komut == "muhur":
        print(ds6_muhur())
    elif a.komut == "olc":
        r = ds6_olc(a.deneme, a.cemal1, a.cemal2, a.cikti)
        print(json.dumps({k: {"karar_n": v["karar_n"], **{m: _f6(x["kappa"]) for m, x in v["model"].items()}} for k, v in r["kume"].items()},
                         ensure_ascii=False))
    else:
        T = ds6_test()
        print(json.dumps({"tamam": T["tamam"], "kural_sha": T["kural_sha"], "esik_sha": T["esik_sha"]}, ensure_ascii=False))
        for x in T["tablo"]:
            print(x["seri"], "bekl", x["beklenen_V1"], x["beklenen_dusen"], x["beklenen_ek"], "çıkan", x["cikan"], "düşen", x["dusen"],
                  "mavi", x["mavi_dusus_atr"], "dok", x["dokunus_n"], "Ha/Hb", x["ha"], x["hb"], "tdok", x["tepe_dokunus_n"], "geç", x["gecerli"],
                  "sahte", x["sahte_n"], "H1", x["ds5_h1"], "kır", x["kirilim"], x["ust_n"])
