"""MUM_IZI_V3 — MUM_IZI EK 5: BANT KOORDİNATINDA MUM DİZİSİ BENZERLİĞİ (v3), SENTETİK, CEMAL'İN İŞARETLERİYLE SINAMA, EN BENZER 24 BÖLGE (25 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI5_IS_TANIMI.md (commit 36a4686; ana model). Cemal: "asıl benzemesinin sebeplerinde en çoğu: mumların SMA ile
üst / alt / orta banda konumları, İLK NEREDE SONRA NEREDE KALIYOR; bir de birbirlerine göre açılış kapanışları ve fitil."

MÜHÜR: v3 tanımı (MV3_ESIK, aile fonksiyonları) yalnız Cemal'in sözünden ve iş tanımındaki sabit tanımdan kuruldu; Cemal'in işaret dosyası
(cemal_mum_izi4_onay.json) ön kayıt (MUM_IZI5_ON_KAYIT.md) commit edilene kadar OKUNMADI. Sınamadan (C) sonra tanım değişmez; değişiklik fikri
raporda 'ÖNERİ'. GETİRİ / SONRASI HESAPLANMAZ. v1 / v2 dosyaları değişmez (içe alınır). Veri <= 2022-12-31; KASA açılmaz.

Komut:  python MUM_IZI_V3.py dagilim     günlük / haftalık rastgele 20.000 pencere -> tau ve %20 eşikleri (mum_izi5_dagilim.json)
        python MUM_IZI_V3.py sentetik    B: pozitif + n1-n5 + rastgele (mum_izi5_sentetik.json)
        python MUM_IZI_V3.py onkayit     MUM_IZI5_ON_KAYIT.md
        python MUM_IZI_V3.py sinama [--kaydirma K]   C: kapı -> işaretler -> AUC / permütasyon / bootstrap (mum_izi5_sinama.csv, mum_izi5_sonuc.json)
        python MUM_IZI_V3.py tarama      D (yalnız C hükmü UYUMLU / KISMEN): evren taraması + aday sayımı
        python MUM_IZI_V3.py onay        D: MUM_IZI5_ONAY.pdf + mum_izi5_onay_anahtar.json
        python MUM_IZI_V3.py rapor       MUM_IZI5_RAPOR.md
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_V3 = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from numpy.lib.stride_tricks import sliding_window_view as _swv5  # noqa: E402

KOK_V3 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_V3 not in sys.path:
    sys.path.insert(0, KOK_V3)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAFTALIK as MH  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ)

v3log = logging.getLogger("col.mum_izi_v3")
if not v3log.handlers:
    _v3_h = logging.StreamHandler(sys.stderr)
    _v3_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_v3: %(message)s", "%H:%M:%S"))
    v3log.addHandler(_v3_h)
    v3log.setLevel(logging.INFO)
    v3log.propagate = False


class V3Hata(RuntimeError):
    """Durdurucu hata: veri / kapı / mühür / kesik."""


V3_SURUM = "MUM_IZI_V3 v1.0 (2026-11-25): bant koordinatında mum dizisi (F1 konum, F2 açılış / kapanış ilişkisi, F3 fitil), telafi yasağı, D3"
V3_YOL = {"cikti": MI.MI_YOL["cikti"], "kod": os.path.join(KOK_V3, "MUM_IZI_V3.py"), "gecici": "/tmp/mum_izi/v3",
          "isaret": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi4_onay.json"), "anahtar4": os.path.join(MI.MI_YOL["cikti"], "mum_izi4_onay_anahtar.json")}
V3_DOSYA = {"onkayit": "MUM_IZI5_ON_KAYIT.md", "rapor": "MUM_IZI5_RAPOR.md", "sonuc": "mum_izi5_sonuc.json", "sinama": "mum_izi5_sinama.csv",
            "onay": "MUM_IZI5_ONAY.pdf", "anahtar": "mum_izi5_onay_anahtar.json", "dagilim": "mum_izi5_dagilim.json", "sentetik": "mum_izi5_sentetik.json",
            "tarama": "mum_izi5_tarama.json"}

MV3_ESIK: Dict[str, Any] = {
    "surum": "MV3-1.0",
    "koordinat": "b = (fiyat - SMA20) / (üst bant - SMA20): SMA 0, üst bant +1, alt bant -1; her mum kendi günündeki Bollinger (20, 2; std ddof 0) ile, "
                 "yalnız o güne kadarki barlar (MI.mi_bant); üst bant = SMA ise pencere geçersiz. Şablonda bantlar görüntüden (mum_izi_mumlar BU / BO)",
    "uzunluklar": [16, 18, 20, 22, 24], "konum": 20,
    "eslem": "mum başına ölçüler hissenin kendi m mumunda hesaplanır, sonra konum oranıyla 20 konuma doğrusal yeniden örneklenir (ardışık ilişkiler 19 "
             "konuma); ikili bayraklar (uzun üst fitil) en yakın konumla",
    "F1": "konum dizisi: 20 konumda bC, bO, bH, bL ile şablon arasındaki mutlak farkların ortalaması (dizi farkı) VE evre farkı: mumlar konum oranıyla "
          "üçe ayrılır (ilk < 1/3, orta, son >= 2/3), her üçte birde ortalama bC ve gövde ortası SMA üstünde payı ((bO + bC) / 2 > 0); 6 değerin şablonla "
          "mutlak farkının ortalaması. F1 = (dizi farkı + evre farkı) / 2",
    "F2": "mumların birbirine göre açılış / kapanışı: konum başına açılışın önceki kapanışa göre yeri (bO_i - bC_i-1), kapanış değişimi (bC_i - bC_i-1), "
          "gövde (bC_i - bO_i), açılış önceki gövdenin içinde mi (0 / 1); dört dizinin şablonla mutlak farkı ortalaması A2; işaret uyumu U2 = (kapanış "
          "değişimi işareti aynı payı + gövde işareti aynı payı) / 2. F2 = (A2 + (1 - U2)) / 2",
    "F3": "fitil: konum başına üst fitil ve alt fitil b biriminde ve mum boyuna oranla (4 dizi), şablonla mutlak fark ortalaması A3; uzun üst fitil "
          "(üst fitil >= boyun yarısı) bayrağı aynı konumlarda payı U3. F3 = (A3 + (1 - U3)) / 2",
    "dagilim": {"n": 20000, "L": "her uzunluk (16 / 18 / 20 / 22 / 24) için 4.000 pencere, birleşik", "gunluk": {"uclar": ["2016-01-01", "2022-12-31"], "tohum": 25112051},
                "haftalik": {"uclar": ["2001-01-01", "2022-12-31"], "tohum": 25112052},
                "yontem": "MUM_IZI2 / v2 yöntemi: geçerli (hisse, pencere sonu) çiftleri ABD + AVR + BIST birleşik havuz, pencere başı >= 19, haftalıkta eksik "
                          "haftalı pencere atılır; yerine koymadan düzgün; tau_k = F_k medyanı; aday eşiği q_k = F_k'nın 0,20 yüzdeliği"},
    "aday": "TELAFİ YASAĞI: pencere aday <=> F1 <= q1 VE F2 <= q2 VE F3 <= q3 (aynı zaman dilimi dağılımında en iyi %20)",
    "D3": {"agirlik": [0.5, 0.25, 0.25], "tanim": "D3 = 0,5 F1 / tau1 + 0,25 F2 / tau2 + 0,25 F3 / tau3 (küçük = benzer); t'de uzunluklar içinde en küçük"},
    "tekil": "aynı hissede aday pencere sonları birbirine < 15 mum olan zincir = bir küme; olay = kümenin en küçük D3'lü hizası",
    "sentetik": {"kok": 25112053, "tohum": 200, "gurultu": [0.0, 0.1, 0.2], "baglam": ["dip", "yatay", "tepe"], "uretec": ["blok", "ry"], "tol": 3,
                 "negatif": {"n1": "fitilsiz büyük gövde (MV.mv_karsi_ornek n1)", "n2": "fitiller ters (n2)", "n3": "mumlar 2 kat (n3)",
                             "n4": "AYNI şablon mumları, gömmeden hemen önce sert düşüş (10 bar, bar başına -%3; doğal eğim silinir): bant geniş ve çöküyor",
                             "n5": "aynı mum biçimleri, yatay kapanış yolu (MV.mv_karsi_ornek p1)"},
                 "n4": {"bar": 10, "egim": -0.03}, "yanlis": {"seri": 200, "n": 1000},
                 "kabul_olcutu": "%10 gürültüde pozitif aday payı (gerçek sonun +-3 barında aday) >= %70 (üç bağlam x iki üretici birleşik); n1-n5 her "
                                 "birinde aday payı <= %5 (bütün gürültüler birleşik); rastgele seride tekil aday <= 0,5 / 1.000 bar (iki üretici ayrı). "
                                 "Geçmezse yazılır; tanım gevşetilmez / sıkılaştırılmaz",
                 "dagilim": "sentetikte tau ve q günlük gerçek dağılımdan"},
    "sinama": {"etiket": "cemal_mum_izi4_onay.json 'isaret' alanı (ön kayıt commit'inden SONRA açılır; 24 sayfa) + mum_izi4_onay_anahtar.json (sayfa -> hisse / tarih / m / zaman)",
               "pencere": "sayfadaki bölgenin kendisi (aynı uzunluk m, aynı son); D3 ve aileler o pencerede", "auc": "P(D3 benziyor < D3 benzemiyor) + 0,5 eşit",
               "p": "tam permütasyon (C(n, n_benziyor) bütün etiket atamaları), tek yönlü", "boot": {"B": 5000, "tohum": 25112054, "tanim": "grup içi yeniden örnekleme"},
               "hukum": {"UYUMLU": 0.80, "KISMEN": 0.65}, "bilgi": "aynı AUC v1 S (büyük = benzer) için; v2 bütün sayfaları kabul ettiği için ayırt edemez",
               "isaretsiz": "işaretsiz sayfa dışarıda"},
    "tarama": {"gunluk": ["2016-01-01", "2022-12-31"], "haftalik": ["2001-01-01", "2022-12-31"],
               "evren": "ABD / AVR: TEZGAH2 P2 (giriş günü; MH.mh_p2); BIST: geçerli bar ve pencere sonu günü işlem değeri (C x V) o günkü BIST medyanının üstünde",
               "sayim": "aday (tekil) sayısı pazar x zaman dilimi; Cemal'in BENZİYOR sayfalarının medyan D3'ünden küçük D3'lü aday sayısı"},
    "onay": {"tohum": 25112055, "gunluk": 12, "haftalik": 12, "bist_max": 3, "once": 15,
             "secim": "evren içi tekil adaylar, en küçük D3'ten, hisse başına bir (iki zaman dilimi birlikte), zaman dilimi başına 12, BIST dilim başına en çok 3; "
                      "sayfa sırası tohumla karışık; hisse / tarih / sonrası yok",
             "esik": "24'ün >= 19'u ✓ -> tespit GEÇERLİ; değilse v3 de geçersiz (karar Cemal'in)"},
}

V3_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "negatif kontroller sentetikte SAYIYLA (n1-n5 + rastgele seri), kabul ölçütü önceden; işaretlerle sınamada permütasyon p ve bootstrap aralığı; "
                   "getiri / eş bu işte yok"),
    "K2": ("EVET", "b koordinatı her mumun kendi gününe kadarki SMA / bant ile; pencere ölçüleri t'ye kadar; v3_prefix 30 olayda veri t'de kesilince D3 aynı; "
                   "veri <= 2022-12-31 + KASA kapısı; işaretler ön kayıttan sonra açılır (git sırası raporda)"),
    "K3": ("EVET", "MI.mi_veri geçerli bar; haftalıkta eksik haftalı pencere atılır (MV.mv_haftalik_panel); BIST'te işlem değeri günlük medyan üstü"),
    "K4": ("EVET", "aynı hissede < 15 mum zincir = bir olay (kümenin en küçük D3'ü)"),
    "K5": ("UYGULANMAZ", "giriş / getiri hesaplanmaz"),
    "K6": ("EVET", "b birimi bant genişliğine oranlı, ölçek bağımsız; TEZGAH2 bölünme düzeltmeli fiyat"),
    "K7": ("EVET", "evren bugün yaşayan hisseler; sayım ve görsel onay (getiri yok)"),
    "K8": ("EVET", "24 etiketle (ana model 25 Kas: işaretsiz sayfa için sözlü yanıt; 'isaret' alanı) AUC: aralık geniş, raporda yazılır; sentetik 200 tohum / koşul; hüküm eşikleri önceden"),
    "K9": ("EVET", "MUM_IZI5_ON_KAYIT.md: KOD5_SHA, ESIK5_SHA, DAGILIM5_SHA, SENTETIK5_SHA + MI / MH / MV sha; işaretler ön kayıt commit'inden sonra; "
                   "v3_kapi kontrol + sha + git"),
    "K10": ("EVET", "işaretli sayfaların penceresi v2 anahtarındaki (sayfa -> hisse / tarih / m) pencereyle birebir; şablon v3 uzaklığı 0 (test)"),
    "K11": ("EVET", "v3_duz: 5 pencerede F1 / F2 / F3 düz döngüyle yeniden; AUC iki yoldan (çift sayım ve sıra toplamı) aynı"),
    "K12": ("EVET", "hüküm yalnız önceden yazılı AUC eşikleriyle; 'iz' sözü yok; getiri yok"),
    "K13": ("EVET", "çakışma kapısı; v1 / v2 / defterler / UC_IZ2 değişmez; işaret dosyası mühürlü sırayla"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


# ================================================================ 0) YARDIMCI
def _v3_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or V3_YOL["cikti"], V3_DOSYA[ad])


def v3_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or MV3_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _lin(x: np.ndarray, K: int) -> np.ndarray:
    """(N, m) -> (N, K) doğrusal yeniden örnekleme (konum oranı)."""
    N, m = x.shape
    if m == K:
        return x
    q = np.linspace(0.0, m - 1.0, K); i0 = np.minimum(np.floor(q).astype(int), m - 2); w = q - i0
    return x[:, i0] * (1 - w)[None, :] + x[:, i0 + 1] * w[None, :]


def _yakin(x: np.ndarray, K: int) -> np.ndarray:
    N, m = x.shape
    return x[:, np.rint(np.linspace(0, m - 1, K)).astype(int)]


# ================================================================ 1) v3 ÖLÇÜLERİ
def v3_ozet(O, H, L, C, BU, BO) -> Dict[str, np.ndarray]:
    """Pencereler (N, m) -> bant koordinatında 20 konumlu diziler. Geçersiz (üst bant = SMA) pencere: 'gecerli' False."""
    O, H, L, C, BU, BO = [np.atleast_2d(np.asarray(v, float)) for v in (O, H, L, C, BU, BO)]
    N, m = C.shape; K = int(MV3_ESIK["konum"])
    d = BU - BO; ok = (d > 0).all(1) & np.isfinite(d).all(1)
    dd = np.where(d > 0, d, 1.0)
    bO, bH, bL, bC = ((X - BO) / dd for X in (O, H, L, C))
    seq = np.stack([_lin(x, K) for x in (bC, bO, bH, bL)], -1)                     # (N, 20, 4)
    r = np.arange(m) / (m - 1); uc = [r < 1 / 3, (r >= 1 / 3) & (r < 2 / 3), r >= 2 / 3]
    orta = (bO + bC) / 2
    evre = np.stack([np.stack([bC[:, u].mean(1), (orta[:, u] > 0).mean(1)], -1) for u in uc], 1)   # (N, 3, 2)
    ust_g = np.maximum(bO, bC); alt_g = np.minimum(bO, bC)
    gap = bO[:, 1:] - bC[:, :-1]; dC = bC[:, 1:] - bC[:, :-1]; body = bC - bO
    icinde = ((bO[:, 1:] >= alt_g[:, :-1]) & (bO[:, 1:] <= ust_g[:, :-1])).astype(float)
    uw = bH - ust_g; lw = alt_g - bL; rg = np.maximum(bH - bL, 1e-12)
    uwr = uw / rg; lwr = lw / rg; uzun = (uwr >= 0.5).astype(float)
    return {"seq": seq, "evre": evre, "gap": _lin(gap, K - 1), "dC": _lin(dC, K - 1), "body": _lin(body, K), "icinde": _lin(icinde, K - 1),
            "uw": _lin(uw, K), "lw": _lin(lw, K), "uwr": _lin(uwr, K), "lwr": _lin(lwr, K), "uzun": _yakin(uzun, K), "gecerli": ok}


def v3_aileler(Z: Dict[str, np.ndarray], S: Dict[str, np.ndarray]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Z: pencere özetleri; S: şablon özeti (N = 1). Döner F1, F2, F3 (N,)."""
    dizi = np.abs(Z["seq"] - S["seq"]).mean((1, 2)); evre = np.abs(Z["evre"] - S["evre"]).mean((1, 2))
    F1 = (dizi + evre) / 2
    A2 = np.mean([np.abs(Z[k] - S[k]).mean(1) for k in ("gap", "dC", "body", "icinde")], axis=0)
    U2 = (np.mean(np.sign(Z["dC"]) == np.sign(S["dC"]), axis=1) + np.mean(np.sign(Z["body"]) == np.sign(S["body"]), axis=1)) / 2
    F2 = (A2 + (1 - U2)) / 2
    A3 = np.mean([np.abs(Z[k] - S[k]).mean(1) for k in ("uw", "lw", "uwr", "lwr")], axis=0)
    U3 = np.mean(Z["uzun"] == S["uzun"], axis=1)
    F3 = (A3 + (1 - U3)) / 2
    bad = ~Z["gecerli"]
    return tuple(np.where(bad, np.nan, F) for F in (F1, F2, F3))


def v3_sablon() -> Dict[str, Any]:
    """Cemal'in kalıbı (MUM_IZI tam şablonu; bantlar görüntüden)."""
    a = MI.mi_sablon_yukle(kalibre=False)["tam"]["ohlc"]
    Z = v3_ozet(a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"])
    return {"ohlc": a, "Z": Z}


def v3_D3(F1, F2, F3, D: Dict[str, Any]) -> np.ndarray:
    w = MV3_ESIK["D3"]["agirlik"]
    return w[0] * F1 / D["tau"][0] + w[1] * F2 / D["tau"][1] + w[2] * F3 / D["tau"][2]


def v3_aday(F1, F2, F3, D: Dict[str, Any]) -> np.ndarray:
    """TELAFİ YASAĞI: üç aile de kendi en iyi %20 eşiğinde (NaN = geçersiz pencere, aday değil)."""
    q = D["q20"]
    return (np.nan_to_num(F1, nan=9e9) <= q[0]) & (np.nan_to_num(F2, nan=9e9) <= q[1]) & (np.nan_to_num(F3, nan=9e9) <= q[2])


# ================================================================ 2) TARAMA (seri)
def v3_tara_seri(O, H, L, C, S: Dict[str, Any], D: Optional[Dict[str, Any]], bosluk: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """Her pencere sonu e: en küçük D3 (bütün uzunluklar), aday mı, aday pencerelerde en küçük D3 ve m, o penceredeki F1-F3. D None ise yalnız F'ler."""
    O, H, L, C = (np.asarray(v, float) for v in (O, H, L, C)); T = len(C)
    BU, BO, BA = MI.mi_bant(C); s0 = 19
    bc = np.r_[0, np.cumsum(bosluk.astype(np.int64))] if bosluk is not None else None
    out = {k: np.full(T, np.nan) for k in ("D3", "D3a", "F1", "F2", "F3")}; out["ma"] = np.zeros(T, np.int64); out["aday"] = np.zeros(T, bool)
    for m in MV3_ESIK["uzunluklar"]:
        if T - s0 < m:
            continue
        W = [_swv5(x[s0:], m) for x in (O, H, L, C, BU, BO)]
        F1, F2, F3 = v3_aileler(v3_ozet(*W), S["Z"])
        e = np.arange(s0 + m - 1, T)
        if bc is not None:
            okb = (bc[e + 1] - bc[e - m + 2]) == 0
            F1 = np.where(okb, F1, np.nan); F2 = np.where(okb, F2, np.nan); F3 = np.where(okb, F3, np.nan)
        if D is None:
            continue
        d3 = v3_D3(F1, F2, F3, D); ad = v3_aday(F1, F2, F3, D) & np.isfinite(d3)
        iy = ~(d3 >= out["D3"][e]) & np.isfinite(d3); out["D3"][e[iy]] = d3[iy]
        d3a = np.where(ad, d3, np.nan); iy = ~(d3a >= out["D3a"][e]) & np.isfinite(d3a)
        out["D3a"][e[iy]] = d3a[iy]; out["ma"][e[iy]] = m; out["F1"][e[iy]] = F1[iy]; out["F2"][e[iy]] = F2[iy]; out["F3"][e[iy]] = F3[iy]
    out["aday"] = np.isfinite(out["D3a"])
    return out


def v3_tekil(e: np.ndarray, d3: np.ndarray, aralik: int = 15) -> np.ndarray:
    """Sıralı aday sonları: ardışık fark < aralik olan zincir bir küme; kümenin en küçük D3'lü sonu."""
    if not len(e):
        return e
    e = np.sort(e); kir = np.flatnonzero(np.diff(e) >= aralik) + 1; out = []
    for g in np.split(e, kir):
        out.append(int(g[np.argmin(d3[g])]))
    return np.array(out, np.int64)


# ================================================================ 3) DAĞILIM (tau, q20)
def v3_dagilim(cikti: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or V3_YOL["cikti"]; S = v3_sablon(); G = MV3_ESIK["dagilim"]; out: Dict[str, Any] = {"surum": V3_SURUM}
    for z in ("gunluk", "haftalik"):
        V = {p: MV.mv_veri(z, p) for p in ("ABD", "AVR", "BIST")}; rows = []
        for m in MV3_ESIK["uzunluklar"]:
            anah, say, uc = [], [], []
            for p in ("ABD", "AVR", "BIST"):
                for s in sorted(V[p]):
                    e = MV.mv_gecerli_uclar(V[p][s], m, G[z]["uclar"]); anah.append((p, s)); say.append(len(e)); uc.append(e)
            say = np.array(say); top = int(say.sum()); rng = np.random.default_rng(int(G[z]["tohum"]) + m)
            g = np.sort(rng.choice(top, size=min(G["n"] // len(MV3_ESIK["uzunluklar"]), top), replace=False)); sinir = np.r_[0, np.cumsum(say)]
            h = np.searchsorted(sinir, g, side="right") - 1
            for hh in np.unique(h):
                p, s = anah[hh]; e = uc[hh][g[h == hh] - sinir[hh]]; d = V[p][s]
                Oo, Hh, Ll, Cc = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")); BU, BO, BA = MI.mi_bant(Cc)
                idx = (e - m + 1)[:, None] + np.arange(m)[None, :]
                F1, F2, F3 = v3_aileler(v3_ozet(Oo[idx], Hh[idx], Ll[idx], Cc[idx], BU[idx], BO[idx]), S["Z"])
                rows.append(pd.DataFrame({"F1": F1, "F2": F2, "F3": F3, "m": m, "pazar": p}))
        R = pd.concat(rows, ignore_index=True); R = R.dropna()
        os.makedirs(V3_YOL["gecici"], exist_ok=True); R.to_pickle(os.path.join(V3_YOL["gecici"], f"dagilim_{z}.pkl"))
        out[z] = {"n": int(len(R)), "tau": [float(R[k].median()) for k in ("F1", "F2", "F3")], "q20": [float(R[k].quantile(0.20)) for k in ("F1", "F2", "F3")],
                  "pazar": R.pazar.value_counts().to_dict()}
        Dz = {"tau": out[z]["tau"], "q20": out[z]["q20"]}
        d3 = v3_D3(R.F1.to_numpy(), R.F2.to_numpy(), R.F3.to_numpy(), Dz); ad = v3_aday(R.F1.to_numpy(), R.F2.to_numpy(), R.F3.to_numpy(), Dz)
        out[z]["aday_pay_rastgele"] = float(ad.mean()); out[z]["D3_ceyrek"] = np.quantile(d3, [0.05, 0.25, 0.5, 0.75, 0.95]).tolist()
        out[z]["kor"] = {"F1_F2": float(np.corrcoef(R.F1, R.F2)[0, 1]), "F1_F3": float(np.corrcoef(R.F1, R.F3)[0, 1]), "F2_F3": float(np.corrcoef(R.F2, R.F3)[0, 1])}
        del V; gc.collect()
        v3log.info("dağılım %s: n %d, tau %s, q20 %s, aday payı %.4f", z, len(R), out[z]["tau"], out[z]["q20"], out[z]["aday_pay_rastgele"])
    out["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_v3_yol("dagilim", cikti), out, "dağılım 5")
    return out


def v3_D(zaman: str, cikti: Optional[str] = None) -> Dict[str, Any]:
    J = json.load(open(_v3_yol("dagilim", cikti), encoding="utf-8"))[zaman]
    return {"tau": J["tau"], "q20": J["q20"]}


# ================================================================ 4) SENTETİK (B)
def v3_sert_baglam(lO, lH, lL, lC, p: int) -> None:
    Sn = MV3_ESIK["sentetik"]["n4"]; nb = int(Sn["bar"]); a = p - nb
    dogal = (lC[p - 1] - lC[a - 1]) / nb; mu = float(Sn["egim"]) - dogal
    kay = np.zeros(len(lC)); kay[a:p] = mu * np.arange(1, nb + 1); kay[p:] = mu * nb
    for x in (lO, lH, lL, lC):
        x += kay


def v3_seri(rng, havuz, ohlc: Dict[str, np.ndarray], uretec: str, baglam: str, gurultu: float) -> Dict[str, Any]:
    Sn = MI.MI_ESIK["sentetik"]; p = int(Sn["seri_on"])
    esn = float(rng.uniform(*Sn["esneme"])); olc = float(math.exp(rng.uniform(math.log(Sn["olcek"][0]), math.log(Sn["olcek"][1]))))
    n = p + int(round(20 * Sn["esneme"][1])) + 1 + int(Sn["seri_son"])
    lO, lH, lL, lC = MI.mi_uret(rng, n, havuz, uretec)
    if baglam == "sert":
        v3_sert_baglam(lO, lH, lL, lC, p)
    else:
        MI.mi_baglam_uygula(lO, lH, lL, lC, p, baglam)
    Le = MI.mi_gom(rng, lO, lH, lL, lC, p, {"ohlc": ohlc}, gurultu, olc, esn)
    return {"O": np.exp(lO), "H": np.exp(lH), "L": np.exp(lL), "C": np.exp(lC), "e": p + Le - 1}


def v3_sentetik(cikti: Optional[str] = None, tohum: Optional[int] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or V3_YOL["cikti"]; Sn = MV3_ESIK["sentetik"]; T = int(tohum or Sn["tohum"]); tol = int(Sn["tol"])
    S = v3_sablon(); D = v3_D("gunluk", cikti); havuz = pd.read_pickle(os.path.join(MI.MI_YOL["gecici"], MI.MI_DOSYA["havuz"]))
    sab = MI.mi_sablon_yukle()["tam"]; kar = MV.mv_karsi_ornek(sab)
    turler = {"poz": (S["ohlc"], Sn["baglam"]), "n1": (kar["n1"], Sn["baglam"]), "n2": (kar["n2"], Sn["baglam"]), "n3": (kar["n3"], Sn["baglam"]),
              "n4": (S["ohlc"], ["sert"]), "n5": (kar["p1"], Sn["baglam"])}
    out: Dict[str, Any] = {"surum": V3_SURUM, "tohum": T, "D": D}
    for ti, (tur, (ohlc, bags)) in enumerate(turler.items()):
        sat = []
        for ui, ur in enumerate(Sn["uretec"]):
            for bi, bg in enumerate(bags):
                for gr in Sn["gurultu"]:
                    for t in range(T):
                        rng = np.random.default_rng([int(Sn["kok"]), ti, ui, bi, int(round(gr * 100)), t])
                        X = v3_seri(rng, havuz, ohlc, ur, bg, float(gr))
                        R = v3_tara_seri(X["O"], X["H"], X["L"], X["C"], S, D)
                        a, b = max(0, X["e"] - tol), X["e"] + tol + 1
                        sat.append({"uretec": ur, "baglam": bg, "gurultu": gr, "aday": bool(R["aday"][a:b].any()),
                                    "D3_min": float(np.nanmin(R["D3"][a:b])) if np.isfinite(R["D3"][a:b]).any() else np.nan})
        Dd = pd.DataFrame(sat)
        out[tur] = {"aday": float(Dd.aday.mean()), "n": int(len(Dd)), "D3_med": float(Dd.D3_min.median()),
                    "gurultu": {f"{g:.1f}": float(x.aday.mean()) for g, x in Dd.groupby("gurultu")},
                    "baglam": {b_: float(x.aday.mean()) for b_, x in Dd.groupby("baglam")}}
        v3log.info("sentetik %s: aday %.3f (%s)", tur, out[tur]["aday"], out[tur]["gurultu"])
    ry = {}
    for ui, ur in enumerate(Sn["uretec"]):
        n = 0; k = 0
        for t in range(int(Sn["yanlis"]["seri"])):
            rng = np.random.default_rng([int(Sn["kok"]), 99, ui, t])
            lO, lH, lL, lC = MI.mi_uret(rng, int(Sn["yanlis"]["n"]) + 60, havuz, ur)
            R = v3_tara_seri(np.exp(lO), np.exp(lH), np.exp(lL), np.exp(lC), S, D)
            n += int(np.isfinite(R["D3"]).sum()); e = np.flatnonzero(R["aday"]); k += len(v3_tekil(e, R["D3a"]))
        ry[ur] = {"aday_1000": 1000.0 * k / max(n, 1), "n_bar": n}
    out["rastgele"] = ry
    out["olcut"] = {"poz_g10_ge_70": bool(out["poz"]["gurultu"]["0.1"] >= 0.70), "neg_le_5": {k: bool(out[k]["aday"] <= 0.05) for k in ("n1", "n2", "n3", "n4", "n5")},
                    "rastgele_le_05": {k: bool(v["aday_1000"] <= 0.5) for k, v in ry.items()}}
    out["olcut"]["gecti"] = out["olcut"]["poz_g10_ge_70"] and all(out["olcut"]["neg_le_5"].values()) and all(out["olcut"]["rastgele_le_05"].values())
    out["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_v3_yol("sentetik", cikti), out, "sentetik 5")
    return out


# ================================================================ 5) KAPI ve ÖN KAYIT
def v3_sha_simdi(cikti: Optional[str] = None) -> Dict[str, str]:
    return {"KOD5_SHA": MI._mi_sha(V3_YOL["kod"]), "ESIK5_SHA": v3_esik_sha(), "DAGILIM5_SHA": MI._mi_sha(_v3_yol("dagilim", cikti)),
            "SENTETIK5_SHA": MI._mi_sha(_v3_yol("sentetik", cikti)), "MI_KOD_SHA": MI._mi_sha(MI.MI_YOL["kod"]), "MH_KOD_SHA": MI._mi_sha(MH.MH_YOL["kod"]),
            "MV_KOD_SHA": MI._mi_sha(MV.MV_YOL["kod"])}


def v3_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or V3_YOL["cikti"]; yol = _v3_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise V3Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = v3_sha_simdi(cikti)
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise V3Hata(f"ön kayıt kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_V3)
    c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise V3Hata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_V3.py", "MUM_IZI.py", "MUM_IZI_HAFTALIK.py", "MUM_IZI_V2.py",
                   os.path.relpath(_v3_yol("dagilim", cikti), KOK_V3), os.path.relpath(_v3_yol("sentetik", cikti), KOK_V3)]):
        raise V3Hata("ön kayıt / kod / dağılım / sentetik çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def v3_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or V3_YOL["cikti"]; y = _v3_yol("onkayit", cikti)
    if os.path.exists(y):
        raise V3Hata("ön kayıt zaten var")
    sh = v3_sha_simdi(cikti); DJ = json.load(open(_v3_yol("dagilim", cikti), encoding="utf-8")); SJ = json.load(open(_v3_yol("sentetik", cikti), encoding="utf-8"))
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in V3_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_V3.py"])
    s = [f"# MUM_IZI5 ÖN KAYIT ({MI._mi_simdi()})", "",
         "v3 tanımı Cemal'in sözünden ve iş tanımındaki sabit tanımdan kuruldu. Cemal'in işaret dosyası (cemal_mum_izi4_onay.json) ve işaretli PDF bu "
         "dosya commit edilene kadar AÇILMADI; iş tanımındaki sayfa numaraları tanımda kullanılmadı. Sınama (C) bu commit'ten sonra; sonra tanım değişmez.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_V3.py commit'i: {kc or 'yok'}", "",
         "## v3 tanımı (MV3_ESIK; sha yukarıda)", "", "```", json.dumps(MV3_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## Dağılım (tau, en iyi %20 eşikleri)", ""]
    for z in ("gunluk", "haftalik"):
        d = DJ[z]
        s.append(f"- {z}: n {d['n']}, tau {[round(x, 4) for x in d['tau']]}, q20 {[round(x, 4) for x in d['q20']]}, rastgele pencerede aday payı "
                 f"{100 * d['aday_pay_rastgele']:.2f} %, aile korelasyonları {d['kor']}")
    o = SJ["olcut"]
    s += ["", "## Sentetik (B; işaretlerden bağımsız)", "",
          f"- pozitif aday payı: {SJ['poz']['gurultu']} (bağlam {SJ['poz']['baglam']})",
          *[f"- {k}: aday {100 * SJ[k]['aday']:.1f} %" for k in ("n1", "n2", "n3", "n4", "n5")],
          f"- rastgele: {SJ['rastgele']}", f"- KABUL ÖLÇÜTÜ: {'GEÇTİ' if o['gecti'] else 'GEÇMEDİ'} {o}", "",
          "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 5")


# ================================================================ 6) İŞARETLERLE SINAMA (C)
def v3_etiket_oku(yol: Optional[str] = None) -> Dict[int, Optional[int]]:
    """İşaret dosyasından {sayfa: 1 (benziyor) / 0 (benzemiyor) / None (işaretsiz)}; biçime toleranslı."""
    J = json.load(open(yol or V3_YOL["isaret"], encoding="utf-8"))

    def lab(v: Any) -> Optional[int]:
        if v is None:
            return None
        t = str(v).strip().replace("İ", "i").lower().replace("i\u0307", "i")
        if any(x in t for x in ("benzemiyor", "✗", "×", "hayir", "hayır", "olmaz")) or t in ("x", "0", "false", "no"):
            return 0
        if any(x in t for x in ("benziyor", "✓", "evet", "olur")) or t in ("1", "true", "yes", "v"):
            return 1
        return None
    out: Dict[int, Optional[int]] = {}

    def gez(o: Any) -> None:
        if isinstance(o, dict):
            sk = next((k for k in o if str(k).lower() in ("sayfa", "page", "s", "sayfa_no", "no")), None)
            lk = "isaret" if "isaret" in o else next((k for k in o if any(w in str(k).lower() for w in ("isaret", "işaret", "etiket", "karar", "cemal",
                                                                                                         "label", "secim", "seçim"))), None)
            if sk is not None and lk is not None and isinstance(o[sk], (int, float, str)) and str(o[sk]).strip().isdigit():
                out[int(o[sk])] = lab(o[lk])
            for k, v in o.items():
                if str(k).strip().isdigit() and not isinstance(v, (dict, list)):
                    out[int(k)] = lab(v)
                elif isinstance(v, list) and v and all(str(x).strip().isdigit() for x in v) and (lab(k) is not None or "isaretsiz" in str(k).lower()
                                                                                                    or "işaretsiz" in str(k).lower()):
                    for x in v:                       # {"benziyor": [3, 5], "benzemiyor": [...], "isaretsiz": [...]}
                        out[int(x)] = lab(k)
                else:
                    gez(v)
        elif isinstance(o, list):
            for v in o:
                gez(v)
    gez(J)
    if not out:
        raise V3Hata("işaret dosyası çözülemedi")
    return out


def v3_auc(x_benz: np.ndarray, x_degil: np.ndarray) -> float:
    """P(benziyor < benzemiyor) + 0,5 eşit (küçük = benzer)."""
    a = np.asarray(x_benz, float)[:, None]; b = np.asarray(x_degil, float)[None, :]
    return float(((a < b).sum() + 0.5 * (a == b).sum()) / (a.size * b.size))


def v3_perm_p(x: np.ndarray, y: np.ndarray) -> float:
    """Tam permütasyon: bütün C(n, n1) atamalarında AUC >= gözlenen payı (tek yönlü)."""
    x = np.asarray(x, float); y = np.asarray(y, int); n1 = int(y.sum()); obs = v3_auc(x[y == 1], x[y == 0])
    r = pd.Series(x).rank(method="average").to_numpy(); n0 = len(x) - n1
    # AUC (küçük = benzer) = 1 - U1 / (n1 n0); U1 = R1 - n1 (n1 + 1) / 2 (R1 = benziyor sıra toplamı, büyük sıra = büyük D3)
    say = 0; top = 0
    for c in itertools.combinations(range(len(x)), n1):
        R1 = r[list(c)].sum(); auc = 1 - (R1 - n1 * (n1 + 1) / 2) / (n1 * n0)
        say += int(auc >= obs - 1e-12); top += 1
    return say / top


def v3_boot(x: np.ndarray, y: np.ndarray, B: int, tohum: int) -> Tuple[float, float]:
    rng = np.random.default_rng(tohum); a = x[y == 1]; b = x[y == 0]; v = []
    for _ in range(B):
        v.append(v3_auc(rng.choice(a, len(a)), rng.choice(b, len(b))))
    return float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))


def v3_pencere(zaman: str, pazar: str, sembol: str, tarih: str, m: int, Vc: Dict[Any, Any]) -> Dict[str, np.ndarray]:
    k = (zaman, pazar)
    if k not in Vc:
        Vc[k] = MV.mv_veri(zaman, pazar)
    d = Vc[k][sembol]; t = d.index.get_loc(pd.Timestamp(tarih)); BU, BO, BA = MI.mi_bant(d.Close.to_numpy(float)); sl = slice(t - m + 1, t + 1)
    return {"O": d.Open.to_numpy(float)[sl], "H": d.High.to_numpy(float)[sl], "L": d.Low.to_numpy(float)[sl], "C": d.Close.to_numpy(float)[sl], "BU": BU[sl], "BO": BO[sl], "BA": BA[sl],
            "d": d, "t": t}


def v3_sinama(cikti: Optional[str] = None, kaydirma: Optional[int] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or V3_YOL["cikti"]
    G0 = v3_kapi(cikti)
    git_isaret = MI._mi_git(["log", "-1", "--format=%H %cI", "--", os.path.relpath(V3_YOL["isaret"], KOK_V3)])
    E = v3_etiket_oku(); A = json.load(open(V3_YOL["anahtar4"], encoding="utf-8"))["sayfalar"]
    nums = sorted(E)
    if kaydirma is None:
        if max(nums) > 24:
            kaydirma = 0
        elif min(nums) < 3:
            kaydirma = 2
        else:
            raise V3Hata(f"sayfa numaralandırması belirsiz ({min(nums)}..{max(nums)}): --kaydirma ver")
    S = v3_sablon(); Dz = {z: v3_D(z, cikti) for z in ("gunluk", "haftalik")}
    Dd = {z: pd.read_pickle(os.path.join(V3_YOL["gecici"], f"dagilim_{z}.pkl")) for z in Dz}
    sab1 = MI.mi_sablon_yukle()["tam"]; Vc: Dict[Any, Any] = {}; rows = []
    for r in A:
        pdf_s = int(r["sayfa"]); isaret = E.get(pdf_s - kaydirma)
        W = v3_pencere(r["zaman"], r["pazar"], r["sembol"], r["tarih"], int(r["m"]), Vc)
        Z = v3_ozet(W["O"], W["H"], W["L"], W["C"], W["BU"], W["BO"]); F1, F2, F3 = (float(f[0]) for f in v3_aileler(Z, S["Z"]))
        D = Dz[r["zaman"]]; d3 = float(v3_D3(F1, F2, F3, D)); ad = bool(v3_aday(np.array([F1]), np.array([F2]), np.array([F3]), D)[0])
        pc = {k: float(MV.mv_pct(Dd[r["zaman"]][k].to_numpy(), v)) for k, v in (("F1", F1), ("F2", F2), ("F3", F3))}
        S1 = MV.mv_S_bilesen(sab1, {k: W[k] for k in ("O", "H", "L", "C", "BU", "BO", "BA")})
        rows.append({"sayfa": pdf_s, "bolge_no": pdf_s - 2, "zaman": r["zaman"], "cemal": isaret, "D3": d3, "F1": F1, "F2": F2, "F3": F3, "F1_pct": pc["F1"],
                     "F2_pct": pc["F2"], "F3_pct": pc["F3"], "aday": ad, "v1_S": S1["S"], "v1_dizi": S1["dizi"], "v1_bant": S1["bant"], "v1_oz": S1["oz"]})
    T = pd.DataFrame(rows).sort_values("sayfa").reset_index(drop=True)
    X = T[T.cemal.notna()].copy(); X["cemal"] = X.cemal.astype(int); X["D3_sira"] = X.D3.rank(method="min").astype(int)
    T = T.merge(X[["sayfa", "D3_sira"]], on="sayfa", how="left")
    Sm = MV3_ESIK["sinama"]; res: Dict[str, Any] = {}
    y = X.cemal.to_numpy()
    for ad_, col, kucuk in (("D3", "D3", True), ("F1", "F1", True), ("F2", "F2", True), ("F3", "F3", True), ("v1_S", "v1_S", False),
                            ("v1_dizi", "v1_dizi", True), ("v1_bant", "v1_bant", True), ("v1_oz", "v1_oz", True)):
        x = X[col].to_numpy(float) * (1 if kucuk else -1)
        auc = v3_auc(x[y == 1], x[y == 0]); p = v3_perm_p(x, y); lo, hi = v3_boot(x, y, int(Sm["boot"]["B"]), int(Sm["boot"]["tohum"]))
        # K11: AUC ikinci yoldan (sıra toplamı)
        r_ = pd.Series(x).rank(method="average").to_numpy(); n1 = int(y.sum()); n0 = len(y) - n1
        auc2 = 1 - (r_[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
        res[ad_] = {"auc": auc, "auc_sira_toplami": float(auc2), "p": p, "boot95": [lo, hi]}
    a = res["D3"]["auc"]; H = Sm["hukum"]
    hk = "UYUMLU" if a >= H["UYUMLU"] else ("KISMEN" if a >= H["KISMEN"] else "UYUMSUZ")
    benz = X[X.cemal == 1]; yari = X.D3.median()
    J = {"surum": V3_SURUM, "kapi": G0, "isaret_dosyasi_commit": git_isaret, "kaydirma": kaydirma, "n_isaretli": int(len(X)), "n_benziyor": int(y.sum()),
         "n_isaretsiz": int(T.cemal.isna().sum()), "auc": res, "hukum": hk,
         "benziyor_en_benzer_yarida": int((benz.D3 <= yari).sum()), "benziyor_medyan_D3": float(benz.D3.median()) if len(benz) else None,
         "aday_benziyor": int(benz.aday.sum()), "aday_benzemiyor": int(X[X.cemal == 0].aday.sum()), "sure_sn": round(time.time() - t0),
         "v2_not": "v2 bütün sayfaları kabul etmişti (kapılar hepsinde geçti): v2'nin sıralama puanı v1 S; kabul / ret olarak ayırt edemez"}
    T.to_csv(_v3_yol("sinama", cikti), index=False, float_format="%.5f")
    MI._mi_jyaz(_v3_yol("sonuc", cikti), {"sinama": J}, "sonuç 5")
    v3log.info("sınama: AUC D3 %.3f (%s) p %.4f", a, hk, res["D3"]["p"])
    return J


# ================================================================ 7) EVREN TARAMASI (D) ve ONAY
_V3_ISCI: Dict[str, Any] = {}


def _v3_isci(s: str) -> Tuple[str, List[Dict[str, Any]]]:
    d = _V3_ISCI["V"][s]; ix = d.index; uc = _V3_ISCI["uclar"]
    R = v3_tara_seri(*(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), _V3_ISCI["S"], _V3_ISCI["D"],
                     d.bosluk.to_numpy(bool) if "bosluk" in d.columns else None)
    ara = (ix >= pd.Timestamp(uc[0])) & (ix <= pd.Timestamp(uc[1]))
    e = np.flatnonzero(R["aday"] & ara); e = v3_tekil(e, R["D3a"])
    return s, [{"sembol": s, "tarih": ix[t], "D3": float(R["D3a"][t]), "m": int(R["ma"][t]), "F1": float(R["F1"][t]), "F2": float(R["F2"][t]), "F3": float(R["F3"][t]),
                "deger": float(d.Close.iloc[t] * d.Volume.iloc[t] * (d.Kur.iloc[t] if "Kur" in d.columns else 1.0))} for t in e]


def v3_tarama(cikti: Optional[str] = None) -> Dict[str, Any]:
    import multiprocessing as mp
    import KASA as KS
    t0 = time.time(); cikti = cikti or V3_YOL["cikti"]
    J0 = json.load(open(_v3_yol("sonuc", cikti), encoding="utf-8"))
    if J0["sinama"]["hukum"] not in ("UYUMLU", "KISMEN"):
        raise V3Hata(f"C hükmü {J0['sinama']['hukum']}: D yapılmaz")
    G0 = v3_kapi(cikti)
    kasa = KS.kasa_kapisi([os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] +
                          [os.path.join(MV.MV_YOL["haftalik"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")], "2022-12-31")
    S = v3_sablon(); parca = []; bar = {}
    for z in ("gunluk", "haftalik"):
        D = v3_D(z, cikti); uc = MV3_ESIK["tarama"][z]
        for p in ("ABD", "AVR", "BIST"):
            V = MV.mv_veri(z, p)
            _V3_ISCI.clear(); _V3_ISCI.update({"V": V, "S": S, "D": D, "uclar": uc})
            try:
                with mp.get_context("fork").Pool(3) as pool:
                    R = list(pool.imap(_v3_isci, sorted(V), chunksize=16))
            finally:
                _V3_ISCI.clear()
            X = pd.DataFrame([r for _, o in R for r in o])
            bar[f"{z}|{p}"] = int(sum(int(((d.index >= pd.Timestamp(uc[0])) & (d.index <= pd.Timestamp(uc[1]))).sum()) for d in V.values()))
            if len(X):
                X["zaman"] = z; X["pazar"] = p; X["evren_ici"] = True
                if p in ("ABD", "AVR"):
                    if z == "gunluk":
                        X["evren_ici"] = MH.mh_p2(X, p, MV.MV_YOL["gunluk"])
                    else:
                        ev = np.ones(len(X), bool); i1 = (pd.to_datetime(X.tarih) <= pd.Timestamp("2015-12-31")).to_numpy()
                        if i1.any():
                            ev[i1] = MH.mh_p2(X[i1], p, MH.MH_YOL["p1"])
                        if (~i1).any():
                            ev[~i1] = MH.mh_p2(X[~i1], p, MH.MH_YOL["p2"])
                        X["evren_ici"] = ev
                else:
                    med = {}
                    for s, d in V.items():
                        dv = (d.Close * d.Volume)
                        for tt, v in dv.items():
                            med.setdefault(tt, []).append(v)
                    medy = {tt: float(np.median(v)) for tt, v in med.items()}
                    X["evren_ici"] = [float(r.deger) > medy.get(pd.Timestamp(r.tarih), np.inf) for r in X.itertuples()]
                parca.append(X)
            del V; gc.collect()
            v3log.info("%s %s: aday %d (%.0f sn)", z, p, len(X), time.time() - t0)
    O = pd.concat(parca, ignore_index=True)
    if pd.to_datetime(O.tarih).max() > MI.MI_KESIK:
        raise V3Hata("KESİK AŞIMI")
    med_b = J0["sinama"]["benziyor_medyan_D3"]
    say = {}
    for (z, p), g in O.groupby(["zaman", "pazar"]):
        e = g[g.evren_ici.astype(bool)]
        say[f"{z}|{p}"] = {"aday": int(len(g)), "aday_evren": int(len(e)), "benziyor_medyanindan_benzer": int((e.D3 < med_b).sum()) if med_b is not None else None,
                           "bar": bar.get(f"{z}|{p}"), "aday_1000_bar": 1000.0 * len(g) / max(bar.get(f"{z}|{p}", 1), 1)}
    O2 = O.copy(); O2["tarih"] = pd.to_datetime(O2.tarih).dt.strftime("%Y-%m-%d")
    O2.to_csv(os.path.join(V3_YOL["gecici"], "v3_aday.csv.gz"), index=False)
    J = {"kapi": G0, "kasa": kasa, "sayim": say, "aday_sha": MI._mi_sha(os.path.join(V3_YOL["gecici"], "v3_aday.csv.gz")), "sure_sn": round(time.time() - t0),
         "prefix": v3_prefix(O)}
    J["onay_secim"] = v3_onay_secim(O)
    MI._mi_jyaz(_v3_yol("tarama", cikti), J, "tarama 5")
    return J


def v3_prefix(O: pd.DataFrame, n: int = 30) -> Dict[str, Any]:
    S = v3_sablon(); rng = np.random.default_rng(2531); sec = O.iloc[rng.choice(len(O), size=min(n, len(O)), replace=False)]; mx = 0.0; Vc: Dict[Any, Any] = {}
    for r in sec.itertuples():
        k = (r.zaman, r.pazar)
        if k not in Vc:
            Vc[k] = MV.mv_veri(r.zaman, r.pazar)
        d = Vc[k][r.sembol]; dk = d[d.index <= r.tarih]
        R = v3_tara_seri(*(dk[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), S, v3_D(r.zaman), dk.bosluk.to_numpy(bool) if "bosluk" in dk.columns else None)
        if not R["aday"][-1]:
            raise V3Hata("PREFIX: aday kayboldu")
        mx = max(mx, abs(float(R["D3a"][-1]) - float(r.D3)))
    if not mx < 1e-12:
        raise V3Hata(f"PREFIX TUTMADI {mx}")
    return {"n": int(len(sec)), "en_buyuk_fark": mx, "tuttu": True}


def v3_onay_secim(O: pd.DataFrame) -> List[Dict[str, Any]]:
    G = MV3_ESIK["onay"]; x = O[O.evren_ici.astype(bool)].sort_values("D3"); sec = []; gor = set(); say = {"gunluk": 0, "haftalik": 0}; bist = {"gunluk": 0, "haftalik": 0}
    for r in x.itertuples():
        if r.sembol in gor or say[r.zaman] >= G[r.zaman]:
            continue
        if r.pazar == "BIST" and bist[r.zaman] >= G["bist_max"]:
            continue
        sec.append({"zaman": r.zaman, "pazar": r.pazar, "sembol": r.sembol, "tarih": str(pd.Timestamp(r.tarih).date()), "m": int(r.m), "D3": float(r.D3),
                    "F1": float(r.F1), "F2": float(r.F2), "F3": float(r.F3)})
        gor.add(r.sembol); say[r.zaman] += 1; bist[r.zaman] += int(r.pazar == "BIST")
        if all(say[z] >= G[z] for z in say):
            break
    for i, r in enumerate(sec):
        r["D3_sira"] = i + 1
    p = np.random.default_rng(G["tohum"]).permutation(len(sec))
    return [dict(sec[i], sayfa=j + 2) for j, i in enumerate(p)]


def _v3_b_panel(ax, W: Dict[str, np.ndarray], S: Dict[str, Any]) -> None:
    """Bant koordinatında üst üste: şablon gri, bölge renkli, 20 konum."""
    K = MV3_ESIK["konum"]; a = S["ohlc"]
    for y_, ls in ((1, "-"), (0, "--"), (-1, "-")):
        ax.axhline(y_, color="#9e8fd6", linestyle=ls, linewidth=1.2)

    def bdiz(O, H, L, C, BU, BO):
        d = BU - BO
        return [_lin(((X - BO) / d)[None, :], K)[0] for X in (O, H, L, C)]
    sO, sH, sL, sC = bdiz(a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"]); x = np.arange(K)
    ax.vlines(x - 0.18, sL, sH, color="#9a9a9a", linewidth=1); ax.bar(x - 0.18, np.maximum(np.abs(sC - sO), 0.01), bottom=np.minimum(sO, sC), width=0.3, color="#bdbdbd")
    rO, rH, rL, rC = bdiz(W["O"], W["H"], W["L"], W["C"], W["BU"], W["BO"])
    rk = np.where(rC >= rO, "#1a9850", "#d73027")
    ax.vlines(x + 0.18, rL, rH, color="#555555", linewidth=1); ax.bar(x + 0.18, np.maximum(np.abs(rC - rO), 0.01), bottom=np.minimum(rO, rC), width=0.3, color=rk)
    ax.set_xticks([]); ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(["alt bant", "SMA", "üst bant"], fontsize=9)
    ax.set_title("Aynı ölçekte üst üste: gri = senin kalıbın, renkli = bölge (konum konum)", fontsize=10)


def v3_onay(cikti: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import Rectangle
    cikti = cikti or V3_YOL["cikti"]
    JT = json.load(open(_v3_yol("tarama", cikti), encoding="utf-8")); JS = json.load(open(_v3_yol("sonuc", cikti), encoding="utf-8"))["sinama"]
    S = v3_sablon(); a = S["ohlc"]; y = _v3_yol("onay", cikti); Vc: Dict[Any, Any] = {}
    top_aday = sum(v["aday_evren"] for v in JT["sayim"].values()); top_b = sum((v["benziyor_medyanindan_benzer"] or 0) for v in JT["sayim"].values())
    with PdfPages(y, metadata={"Title": "MUM_IZI5 onay", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.06, 0.95, "YENİ ÖLÇÜ: bant içindeki yer + açılış / kapanış + fitil", fontsize=14, weight="bold")
        fig.text(0.06, 0.9,
                 f"Senin işaretlerinle uyum: benziyor dediğin {JS['n_benziyor']} sayfanın {JS['benziyor_en_benzer_yarida']}'i yeni ölçüde en benzer yarıda "
                 f"({JS['n_isaretli']} sayfada AUC {JS['auc']['D3']['auc']:.2f}).\n\n"
                 f"Veride kaç aday var: {top_aday} (iki zaman dilimi, evren içi); senin 'benziyor' örneklerinden daha benzer olan {top_b}.\n\n"
                 "Birebir aynısı yok: en benzerleri bunlar. Sonraki 24 sayfa en benzer adaylar (sıra karışık).\n"
                 "Her sayfada üstte fiyat grafiği, altta aynı ölçekte üst üste (gri = senin kalıbın).\n"
                 "Hisse adı, tarih ve sonrası yok. ✓ benziyor ya da × benzemiyor işaretle; 24'ün 19'u ✓ ise tespit geçerli.", fontsize=11, va="top", wrap=True)
        pdf.savefig(fig); plt.close(fig)
        for r in sorted(JT["onay_secim"], key=lambda r: r["sayfa"]):
            W = v3_pencere(r["zaman"], r["pazar"], r["sembol"], r["tarih"], int(r["m"]), Vc); d = W["d"]; t = W["t"]; m = int(r["m"])
            i0 = max(0, t - m + 1 - MV3_ESIK["onay"]["once"]); BU, BO, BA = MI.mi_bant(d.Close.to_numpy(float)); sl = slice(i0, t + 1)
            fig = plt.figure(figsize=(8.3, 11.7))
            MV._mv_ciz(fig.add_axes([0.04, 0.62, 0.3, 0.27]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
            MV._mv_ciz(fig.add_axes([0.38, 0.56, 0.58, 0.36]), *(d[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close")), BU[sl], BO[sl], BA[sl],
                       (t - m + 1 - i0, t - i0), f"Sayfa {r['sayfa']}: bölge ({'haftalık' if r['zaman'] == 'haftalik' else 'günlük'} mum)")
            _v3_b_panel(fig.add_axes([0.12, 0.25, 0.84, 0.25]), W, S)
            ax = fig.add_axes([0.1, 0.04, 0.8, 0.15]); ax.axis("off")
            for xx, txt in ((0.0, "✓  benziyor"), (0.55, "×  benzemiyor")):
                ax.add_patch(Rectangle((xx, 0.1), 0.42, 0.8, fill=False, linewidth=3, transform=ax.transAxes))
                ax.text(xx + 0.21, 0.5, txt, ha="center", va="center", fontsize=20, transform=ax.transAxes)
            pdf.savefig(fig); plt.close(fig)
    MI._mi_jyaz(_v3_yol("anahtar", cikti), {"not": "sayfa -> hisse / tarih / D3 / D3 sırası; PDF'e girmez", "sayfalar": JT["onay_secim"]}, "anahtar 5")
    return y


def v3_duz(W: Dict[str, np.ndarray], S: Dict[str, Any]) -> Tuple[float, float, float]:
    """K11: tek pencerede F1 / F2 / F3 düz döngüyle (vektörsüz; yeniden örnekleme dahil)."""
    m = len(W["C"]); K = 20

    def b(X, i):
        return (X[i] - W["BO"][i]) / (W["BU"][i] - W["BO"][i])

    def yo(seq, K_):
        n = len(seq)
        if n == K_:
            return list(seq)
        o = []
        for k in range(K_):
            q = k * (n - 1) / (K_ - 1); i0 = min(int(math.floor(q)), n - 2); w = q - i0; o.append(seq[i0] * (1 - w) + seq[i0 + 1] * w)
        return o
    bO = [b(W["O"], i) for i in range(m)]; bH = [b(W["H"], i) for i in range(m)]; bL = [b(W["L"], i) for i in range(m)]; bC = [b(W["C"], i) for i in range(m)]
    Z = S["Z"]
    seq = [yo(bC, K), yo(bO, K), yo(bH, K), yo(bL, K)]
    dizi = sum(abs(seq[f][k] - Z["seq"][0][k][f]) for f in range(4) for k in range(K)) / (4 * K)
    ev = []
    for j, (lo, hi) in enumerate(((0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1.01))):
        ii = [i for i in range(m) if lo <= i / (m - 1) < hi] if j < 2 else [i for i in range(m) if i / (m - 1) >= 2 / 3]
        mc = sum(bC[i] for i in ii) / len(ii); py = sum(1 for i in ii if (bO[i] + bC[i]) / 2 > 0) / len(ii)
        ev += [abs(mc - Z["evre"][0][j][0]), abs(py - Z["evre"][0][j][1])]
    F1 = (dizi + sum(ev) / 6) / 2
    gap = yo([bO[i] - bC[i - 1] for i in range(1, m)], K - 1); dC = yo([bC[i] - bC[i - 1] for i in range(1, m)], K - 1); body = yo([bC[i] - bO[i] for i in range(m)], K)
    ic = yo([1.0 if min(bO[i - 1], bC[i - 1]) <= bO[i] <= max(bO[i - 1], bC[i - 1]) else 0.0 for i in range(1, m)], K - 1)
    A2 = (sum(abs(gap[k] - Z["gap"][0][k]) for k in range(K - 1)) / (K - 1) + sum(abs(dC[k] - Z["dC"][0][k]) for k in range(K - 1)) / (K - 1) +
          sum(abs(body[k] - Z["body"][0][k]) for k in range(K)) / K + sum(abs(ic[k] - Z["icinde"][0][k]) for k in range(K - 1)) / (K - 1)) / 4
    U2 = (sum(1 for k in range(K - 1) if np.sign(dC[k]) == np.sign(Z["dC"][0][k])) / (K - 1) + sum(1 for k in range(K) if np.sign(body[k]) == np.sign(Z["body"][0][k])) / K) / 2
    F2 = (A2 + 1 - U2) / 2
    uw = [bH[i] - max(bO[i], bC[i]) for i in range(m)]; lw = [min(bO[i], bC[i]) - bL[i] for i in range(m)]; rg = [max(bH[i] - bL[i], 1e-12) for i in range(m)]
    uwr = [uw[i] / rg[i] for i in range(m)]; lwr = [lw[i] / rg[i] for i in range(m)]
    A3 = sum(sum(abs(a_ - b_) for a_, b_ in zip(yo(s_, K), Z[k][0])) / K for s_, k in ((uw, "uw"), (lw, "lw"), (uwr, "uwr"), (lwr, "lwr"))) / 4
    uz = [1.0 if uwr[int(round(k * (m - 1) / (K - 1)))] >= 0.5 else 0.0 for k in range(K)]
    U3 = sum(1 for k in range(K) if uz[k] == Z["uzun"][0][k]) / K
    return F1, F2, (A3 + 1 - U3) / 2


def v3_rapor(cikti: Optional[str] = None) -> str:
    cikti = cikti or V3_YOL["cikti"]
    DJ = json.load(open(_v3_yol("dagilim", cikti), encoding="utf-8")); SJ = json.load(open(_v3_yol("sentetik", cikti), encoding="utf-8"))
    J = json.load(open(_v3_yol("sonuc", cikti), encoding="utf-8"))["sinama"]; T = pd.read_csv(_v3_yol("sinama", cikti))
    L = [f"# MUM_IZI5 RAPOR ({MI._mi_simdi()})", "", f"Sürüm: {V3_SURUM}", "", "## İŞARETLERLE SINAMA", "",
         f"Hüküm: {J['hukum']} (D3 AUC {J['auc']['D3']['auc']:.3f}, %95 {J['auc']['D3']['boot95'][0]:.2f}..{J['auc']['D3']['boot95'][1]:.2f}, p {J['auc']['D3']['p']:.4f}); "
         f"işaretli {J['n_isaretli']} (benziyor {J['n_benziyor']}), işaretsiz {J['n_isaretsiz']}; kaydırma {J['kaydirma']}", "",
         "| ölçü | AUC | %95 | p |", "|---|---|---|---|"]
    for k, v in J["auc"].items():
        L.append(f"| {k} | {v['auc']:.3f} | {v['boot95'][0]:.2f}..{v['boot95'][1]:.2f} | {v['p']:.4f} |")
    L += ["", "| sayfa | Cemal | D3 | D3 sırası | F1 / F2 / F3 yüzdelik | aday | v1 S |", "|---|---|---|---|---|---|---|"]
    for r in T.itertuples():
        c = "-" if pd.isna(r.cemal) else ("BENZİYOR" if int(r.cemal) == 1 else "benzemiyor")
        L.append(f"| {r.sayfa} | {c} | {r.D3:.3f} | {'' if pd.isna(r.D3_sira) else int(r.D3_sira)} | {r.F1_pct:.2f} / {r.F2_pct:.2f} / {r.F3_pct:.2f} | {'evet' if r.aday else '-'} | {r.v1_S:.2f} |")
    L += ["", "## SENTETİK", "", json.dumps(SJ, ensure_ascii=False)[:3000], "", "## DAĞILIM", "", json.dumps(DJ, ensure_ascii=False)[:2000], ""]
    if os.path.exists(_v3_yol("tarama", cikti)):
        JT = json.load(open(_v3_yol("tarama", cikti), encoding="utf-8"))
        L += ["## SAYIM", "", json.dumps(JT["sayim"], ensure_ascii=False), ""]
    return MI._mi_yaz(_v3_yol("rapor", cikti), "\n".join(L), "rapor 5")


# ================================================================ 8) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_v3(_once=_CK_ONCE_V3, _dosya="MUM_IZI_V3.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_V3",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_v3()


def _v3_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_V3")
    ap.add_argument("komut", choices=["dagilim", "sentetik", "onkayit", "sinama", "tarama", "onay", "rapor"])
    ap.add_argument("--kaydirma", type=int, default=None); ap.add_argument("--tohum", type=int, default=None)
    a = ap.parse_args(argv)
    try:
        if a.komut == "dagilim":
            J = v3_dagilim(); print(json.dumps(MI._mi_json(J), ensure_ascii=False)[:3000])
        elif a.komut == "sentetik":
            J = v3_sentetik(tohum=a.tohum); print(json.dumps(MI._mi_json(J), ensure_ascii=False)[:3000])
        elif a.komut == "onkayit":
            print(v3_onkayit_yaz())
        elif a.komut == "sinama":
            J = v3_sinama(kaydirma=a.kaydirma); print(json.dumps(MI._mi_json(J), ensure_ascii=False)[:4000])
        elif a.komut == "tarama":
            J = v3_tarama(); print(json.dumps(MI._mi_json({k: J[k] for k in ("sayim", "prefix")}), ensure_ascii=False)[:3000])
        elif a.komut == "onay":
            print(v3_onay())
        elif a.komut == "rapor":
            print(v3_rapor())
    except V3Hata as ex:
        v3log.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_v3_ana())
