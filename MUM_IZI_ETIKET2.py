"""MUM_IZI_ETIKET2 — MUM_IZI EK 6: ETİKET SETİ 2 (25 Kasım 2026). Yeni ölçü KURULMAZ.

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI6_IS_TANIMI.md (commit 4338f6b; ana model). Donmuş MUM_IZI_V3 ölçüleri (F1 / F2 / F3 / D3; KOD5_SHA
70fc2fb9..., ESIK5_SHA 0a46827a...) ve v1 S aynen kullanılır. Bu modül Cemal'in işaretleyeceği 48 sayfalık seti (8 tekrar + 40 yeni; yeni sayfalar
donmuş F1 yüzdeliğine göre katmanlı) hazırlar ve Cemal işaretleyince koşulacak sınamaları (T1 tutarlılık, T2 F1 AUC ana sınama, T3 / T4 bilgi)
ön kayıtlı biçimde içerir. GETİRİ / SONRASI YOK. MÜHÜR: anahtar (sayfa -> hisse / tarih / katman / ölçüler) PDF'e girmez; commit mesajlarına ve
rapora sayfa -> katman / etiket eşlemesi yazılmaz (yalnız sayım). v1 / v2 / v3 dosyaları değişmez (içe alınır). Veri <= 2022-12-31; KASA açılmaz.

Komut:  python MUM_IZI_ETIKET2.py onkayit          MUM_IZI6_ON_KAYIT.md (tarama ve PDF'ten önce commit edilir)
        python MUM_IZI_ETIKET2.py tarama           kapı -> evren pencereleri (donmuş F1) -> katman sayımı -> seçim (mum_izi6_tarama.json)
        python MUM_IZI_ETIKET2.py pdf              MUM_IZI6_ETIKET.pdf (kapak + 48) + mum_izi6_anahtar.json
        python MUM_IZI_ETIKET2.py rapor            MUM_IZI6_RAPOR.md (yalnız sayımlar)
        python MUM_IZI_ETIKET2.py olc [--etiket YOL] [--cikti KLASÖR]   Cemal işaretleyince: T1-T4 (mum_izi6_olcum.json, MUM_IZI6_OLCUM.md)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_E6 = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_E6 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_E6 not in sys.path:
    sys.path.insert(0, KOK_E6)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAFTALIK as MH  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V3 as V3  # noqa: E402  (DEĞİŞTİRİLMEZ; ölçüler donmuş)

e6log = logging.getLogger("col.mum_izi_etiket2")
if not e6log.handlers:
    _e6_h = logging.StreamHandler(sys.stderr)
    _e6_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_etiket2: %(message)s", "%H:%M:%S"))
    e6log.addHandler(_e6_h)
    e6log.setLevel(logging.INFO)
    e6log.propagate = False


class E6Hata(RuntimeError):
    """Durdurucu hata: kapı / mühür / veri / şema."""


E6_SURUM = "MUM_IZI_ETIKET2 v1.0 (2026-11-25): etiket seti 2 (8 tekrar + 40 katmanlı yeni), T1-T4 ön kayıtlı"
E6_YOL = {"cikti": MI.MI_YOL["cikti"], "kod": os.path.join(KOK_E6, "MUM_IZI_ETIKET2.py"), "gecici": "/tmp/mum_izi/etiket2",
          "isaret4": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi4_onay.json"), "anahtar4": os.path.join(MI.MI_YOL["cikti"], "mum_izi4_onay_anahtar.json"),
          "dagilim": {z: os.path.join(V3.V3_YOL["gecici"], f"dagilim_{z}.pkl") for z in ("gunluk", "haftalik")}}
E6_DOSYA = {"onkayit": "MUM_IZI6_ON_KAYIT.md", "tarama": "mum_izi6_tarama.json", "pdf": "MUM_IZI6_ETIKET.pdf", "anahtar": "mum_izi6_anahtar.json",
            "rapor": "MUM_IZI6_RAPOR.md", "etiket": "cemal_mum_izi6_etiket.json", "olcum": "mum_izi6_olcum.json", "olcum_md": "MUM_IZI6_OLCUM.md"}

E6_KAPAK = ("Kodun üç denemesi de gözünle uyuşmadı. Bu set kodun değil senin gözünün ölçümü: 48 bölge; bir kısmı kalıbına yakın, bir kısmı uzak, "
            "bir kısmı rastgele; 8'i daha önce gördüklerin. Her sayfada benziyorsa ✓ kutusuna, benzemiyorsa × kutusuna X koy. İstersen benzeyen sayfada "
            "benzeten 2-3 mumu daire içine al.")

E6_ESIK: Dict[str, Any] = {
    "surum": "E6-1.0",
    "olcu": "donmuş MUM_IZI_V3: F1 / F2 / F3 (v3_ozet + v3_aileler), D3 (v3_D3, mum_izi5_dagilim.json tau), yüzdelik = MV.mv_pct(V3 rastgele pencere "
            "dağılımı, aynı zaman dilimi); v1 S = MV.mv_S_bilesen(MUM_IZI tam şablon, kalibre). Yeni ölçü yok",
    "pencere": {"birim": "(hisse, pencere sonu, uzunluk m); m = V3 uzunlukları 16 / 18 / 20 / 22 / 24", "gunluk": ["2016-01-01", "2022-12-31"],
                "haftalik": ["2001-01-01", "2022-12-31"], "bas_min": 19,
                "gecerli": "MI.mi_veri geçerli bar; pencere başı >= 19 (bant); haftalıkta pencerenin 2..m. barında boşluk (eksik hafta) yok; üst bant > SMA"},
    "evren": {"ABD_AVR": "giriş günü TEZGAH2 P2 üyeliği (MH.mh_p2 ile aynı kural, hisse başına vektörlü: sonraki geçerli bar <= 10 gün, P2 ve hücre >= 0, "
                         "sinyal barı geçersiz değil); günlük -> /tmp/mum_izi/acik, haftalık 2001-15 -> /tmp/mum_izi/haftalik/p1, 2016-22 -> /tmp/mum_izi/acik; "
                         "vektörlü maske MH.mh_p2 ile her (zaman dilimi, pazar, parça) için 2.000 rastgele (hisse, tarih) çiftinde birebir sınanır (fark -> DUR)",
              "BIST": "pencere sonu barının işlem değeri (Close x Volume) aynı gün (günlük) / aynı ISO haftası (haftalık) BIST kesit medyanının üstünde",
              "haric": "önceki 24 sayfanın (MUM_IZI4_ONAY) hisseleri"},
    "katman": {"K1": {"alt": None, "ust": 0.005, "n": 16}, "K2": {"alt": 0.005, "ust": 0.05, "n": 12}, "K3": {"alt": 0.05, "ust": 0.20, "n": 6},
               "K4": {"alt": "rastgele", "ust": "rastgele", "n": 6}, "kural": "F1 yüzdeliği alt < p <= ust (K1: p <= 0,005); K4 = evren içi bütün pencereler"},
    "secim": {"yari": "her katmanda n / 2 günlük + n / 2 haftalık", "bist_tavan": "katman x zaman dilimi başına en çok floor((n / 2) / 3) BIST (katman başına <= üçte bir)",
              "yontem": "katman içi RASTGELE: her hisse için evren içi katman pencerelerinden biri düzgün rastgele (hisse tohumu = md5(tohum|zaman|pazar|sembol|katman)); "
                        "sonra hisseler katmandaki pencere sayısıyla orantılı olasılıkla, yerine koymadan, tek tek çekilir (= katman pencereleri arasında düzgün "
                        "çekim, hisse başına bir); sıra K1, K2, K3, K4; her katmanda önce günlük sonra haftalık; bir hisse sette bir kez (günlük ve haftalık dahil); "
                        "BIST tavanı dolunca BIST hisseleri o katman x zaman diliminde çekilmez",
              "tekrar": "önceki 24 sayfadan Cemal'in EVET dediklerinden rastgele 4 + HAYIR dediklerinden rastgele 4 (cemal_mum_izi4_onay.json 'isaret'); aynı bölge, aynı çizim",
              "sira": "48 sayfa tohumla karışık; PDF sayfa 1 kapak, bölgeler PDF sayfa 2-49; sayfada yazan numara = PDF sayfa numarası"},
    "tohum": {"secim": 25112061, "tekrar": 25112062, "sira": 25112063, "boot": 25112064, "t4_cv": 25112065, "t4_null": 25112066, "p2_dogrulama": 25112067},
    "sayfa": "MUM_IZI4_ONAY ile birebir: solda 'Senin kalıbın' (şablon + bant), sağda 'Sayfa N: bulunan bölge (günlük / haftalık mum)' (öncesi 15 mum, turuncu "
             "kutu, bölge sonunda kesik), Bollinger 20 + SMA20 (kesik), hisse / tarih / sonrası yok, altta ✓ benziyor / ✗ benzemiyor kutuları",
    "kapak": E6_KAPAK,
    "etiket": {"dosya": "cemal_mum_izi6_etiket.json", "sema": {"sayfalar": {"<PDF sayfa no, metin>": {"isaret": "EVET | HAYIR | YOK | IKISI | BELIRSIZ",
                                                                                                         "kutu_disi": "metin", "guven": "metin"}}},
               "anlam": "EVET = benziyor (1), HAYIR = benzemiyor (0); YOK / IKISI / BELIRSIZ = karar değil (sınamalardan çıkar, sayılır); başka değer -> DUR",
               "numara": "PDF sayfa numarası (2-49); 1 kapak (yok sayılır); 1-49 dışı anahtar -> DUR"},
    "T1": {"tanim": "8 tekrar sayfasında yeni işaret = önceki işaret (EVET / HAYIR) sayısı; karar olmayan yeni işaret 'aynı değil' sayılır (ayrıca yazılır)",
           "hukum": {"tutarli": 7, "kismen": 5}, "metin": ">= 7 / 8 tutarlı; 5-6 kısmen; <= 4 tutarsız (tutarsızsa hiçbir formül tutturamaz)"},
    "T2": {"tanim": "40 yeni sayfada donmuş F1'in AUC'si = P(F1 benziyor < F1 benzemiyor) + 0,5 eşit; bootstrap %95 (grup içi, B 5000); tam permütasyon p "
                    "(sıra toplamının tam dağılımı, tek yönlü)", "en_az": 3, "B": 5000,
           "hukum": "en az 3 EVET ve 3 HAYIR yoksa ÖLÇÜLEMEDİ; AUC >= 0,80 VE alt uç >= 0,65 -> UYUMLU; değilse AUC >= 0,65 -> KISMEN; AUC < 0,65 -> UYUMSUZ",
           "esik": {"uyumlu": 0.80, "alt_uc": 0.65, "kismen": 0.65},
           "katman": "katman başına EVET payı (karar verilmiş sayfalar içinde); 'sıra tutuyor' = K1 >= K2 >= K3 >= K4 ve K1 > K4; 'tam sıra' = kesin büyük"},
    "T3": {"tanim": "bilgi: D3, F2, F3, F1 evre parçası, F1 dizi parçası, v1 S (büyük = benzer) için aynı AUC / %95 / p (40 yeni); F1 ve hepsi günlük / haftalık ayrı"},
    "T4": {"tanim": "bilgi, EZBER RİSKLİ: 64 etiket (önceki 24 sayfa ilk işaretleriyle + 40 yeni); girdi 12 v3 parçası (F1 dizi, F1 evre, F2: 4 fark + işaret "
                    "uyumu, F3: 4 fark + uzun üst fitil uyumu) + 39 ölçü (MI_OZELLIK 35 + MV EK 4; şablondan mutlak fark) = 51; kat içi standartlaştırma; "
                    "L2 lojistik (lambda 1, kesişim cezasız, IRLS); tabakalı 5 kat x 50 tekrar çapraz doğrulama, kat dışı tahminlerle AUC; yalnız CV AUC "
                    "(ortalama ve %2,5-%97,5) + etiket karıştırma tabanı (200 karıştırma x 5 tekrar) raporlanır",
           "lambda": 1.0, "kat": 5, "tekrar": 50, "null": 200, "null_tekrar": 5},
    "sonrasi": "T2 UYUMLU -> v4 (F1 eşiği + sentetik negatiflerden geçen zorunlu kapılar; yeni ön kayıt), sonra en benzer bölgelerle onay; KISMEN / UYUMSUZ -> karar Cemal'in",
}

E6_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban = katman K4 (evrenden düzgün rastgele pencere) ve önceki işaretlerle tekrar (T1); AUC permütasyon / bootstrap; T4 etiket karıştırma tabanı; "
                   "getiri / eş yok"),
    "K2": ("EVET", "F1 her mumun kendi gününe kadarki bantla (V3); seçilen 40 pencerede veri pencere sonunda kesilince F1 aynı (e6_prefix); veri <= 2022-12-31 + "
                   "KASA kapısı; etiketler set üretiminden SONRA gelir; ön kayıt tarama ve PDF'ten önce commit"),
    "K3": ("EVET", "MI.mi_veri geçerli bar; haftalıkta eksik haftalı pencere atılır (V3 kuralı); BIST işlem değeri kesit medyanı üstü; ABD / AVR P2"),
    "K4": ("EVET", "hisse başına bir sayfa (günlük ve haftalık birlikte); önceki 24 sayfanın hisseleri hariç"),
    "K5": ("UYGULANMAZ", "giriş / getiri yok"),
    "K6": ("EVET", "b birimi ölçek bağımsız; BIST işlem değeri aynı para biriminde kesit medyanıyla"),
    "K7": ("EVET", "evren bugün yaşayan hisseler; yalnız görsel etiket (getiri yok)"),
    "K8": ("EVET", "40 yeni + 8 tekrar; en az 3 EVET / 3 HAYIR yoksa ÖLÇÜLEMEDİ; aralık raporda; T4 EZBER RİSKLİ yalnız bilgi"),
    "K9": ("EVET", "MUM_IZI6_ON_KAYIT.md: KOD6_SHA, ESIK6_SHA, V3 / MI / MH / MV kod sha, ESIK5_SHA, dağılım pkl sha; e6_kapi (kontrol + sha + git) tarama ve "
                   "olc öncesi; anahtar sha tarama json'unda, olc onu denetler"),
    "K10": ("EVET", "etiket şeması önceden yazılı (sayfalar -> no -> isaret); bilinmeyen değer / numara DUR; P2 vektörlü maske MH.mh_p2 ile 2.000 çiftte birebir"),
    "K11": ("EVET", "seçilen sayfaların F1 / F2 / F3'ü V3.v3_duz ile düz döngüde yeniden; tekrar sayfalarında v1 S = MUM_IZI4 anahtarındaki S; AUC iki yoldan"),
    "K12": ("EVET", "hüküm yalnız önceden yazılı eşiklerle; rapor ve commit mesajında sayfa -> katman / etiket eşlemesi yok; 'iz' sözü yok"),
    "K13": ("EVET", "çakışma kapısı; v1 / v2 / v3 / defterler / kural_defteri / UC_IZ2 değişmez; yalnız kendi yolları commit"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


# ================================================================ 0) YARDIMCI
def _e6_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or E6_YOL["cikti"], E6_DOSYA[ad])


def e6_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or E6_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _e6_tohum(*parca: Any) -> int:
    return int(hashlib.md5("|".join(str(p) for p in parca).encode()).hexdigest()[:12], 16)


def e6_katman(pct: np.ndarray) -> np.ndarray:
    """F1 yüzdeliği -> 1 / 2 / 3 (K1-K3), 0 = hiçbiri (K4 ayrıca bütün pencereler)."""
    p = np.asarray(pct, float); k = np.zeros(len(p), np.int8)
    k[(p > 0.05) & (p <= 0.20)] = 3; k[(p > 0.005) & (p <= 0.05)] = 2; k[p <= 0.005] = 1
    return k


def e6_auc(x_benz: np.ndarray, x_degil: np.ndarray) -> float:
    return V3.v3_auc(x_benz, x_degil)


def e6_perm_p(x: np.ndarray, y: np.ndarray) -> float:
    """Tam permütasyon p (tek yönlü, AUC >= gözlenen): benziyor sıra toplamının bütün C(n, n1) atamalardaki tam dağılımı (eşitlerde ortalama sıra;
    sıralar 2 ile çarpılıp tamsayı). Küçük x = benzer."""
    x = np.asarray(x, float); y = np.asarray(y, int); n = len(x); n1 = int(y.sum())
    r2 = np.rint(2 * pd.Series(x).rank(method="average").to_numpy()).astype(np.int64); obs = int(r2[y == 1].sum())
    S = int(r2.sum()); dp = np.zeros((n1 + 1, S + 1)); dp[0, 0] = 1.0
    for v in r2:
        dp[1:, v:] = dp[1:, v:] + dp[:-1, :S + 1 - v]
    tam = dp[n1]
    return float(tam[:obs + 1].sum() / tam.sum())


def e6_boot(x: np.ndarray, y: np.ndarray, B: int, tohum: int) -> Tuple[float, float]:
    return V3.v3_boot(np.asarray(x, float), np.asarray(y, int), B, tohum)


def _e6_ozet(x: np.ndarray, y: np.ndarray, kucuk: bool, B: int, tohum: int) -> Dict[str, Any]:
    x = np.asarray(x, float) * (1 if kucuk else -1); y = np.asarray(y, int)
    if y.sum() < 1 or (1 - y).sum() < 1:
        return {"n": int(len(y)), "n_benz": int(y.sum()), "auc": None}
    a = e6_auc(x[y == 1], x[y == 0]); r = pd.Series(x).rank(method="average").to_numpy(); n1 = int(y.sum()); n0 = len(y) - n1
    a2 = 1 - (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    lo, hi = e6_boot(x, y, B, tohum) if min(n1, n0) >= 2 else (None, None)
    return {"n": int(len(y)), "n_benz": n1, "auc": float(a), "auc_sira": float(a2), "p": e6_perm_p(x, y), "boot95": [lo, hi]}


# ================================================================ 1) EVREN MASKELERİ
def e6_p2_hazirla(pazar: str, klasor: str) -> Dict[str, Any]:
    import KART_TUR2 as KT2
    import OLCU_SINAMA as OS
    Vd = OS.os_veri(pazar, klasor); Pk, P2 = KT2.k2_panel(Vd, pazar); P = KT2.k2_P(Pk, Vd, P2)
    del Vd, Pk; gc.collect()
    return P


def e6_p2_maske(P: Dict[str, Any], s: str, tarih: pd.DatetimeIndex, bosluk_azami: Optional[int] = None) -> np.ndarray:
    """OC.oc_olay_hazirla'nın havuz kuralının (tekil 1) hisse başına vektörlü hali: sinyal barı geçersiz değil, sonraki geçerli bar var ve
    <= giriş_azami_bosluk, giriş günü havuzda (ok ve H >= 0)."""
    import ORTAK_CETVEL as OC
    bz = int(bosluk_azami if bosluk_azami is not None else OC.OC_ESIK["olay"]["giris_azami_bosluk"])
    t = pd.DatetimeIndex(tarih).normalize(); out = np.zeros(len(t), bool); j = P["kol"].get(s)
    if j is None or not len(t):
        return out
    vi = P["Vidx"][s]; idx = P["tarih"]
    k = vi.searchsorted(t, side="right"); var = k < len(vi)
    g = vi[np.minimum(k, len(vi) - 1)]; d = idx.get_indexer(g); dt = idx.searchsorted(t, side="right")
    ok = var & (d >= 0) & (d - dt + 1 <= bz)
    dd = np.where(ok, d, 0)
    ok &= P["ok"][dd, j] & (P["H"][dd, j] >= 0)
    gec = P["gecersiz"].get(s)
    if gec is not None and len(gec):
        ok &= ~t.isin(gec)
    return ok


def e6_bist_medyan(V: Dict[str, pd.DataFrame], zaman: str) -> pd.Series:
    """Kesit medyanı: günlük -> tarih, haftalık -> ISO (yıl, hafta) anahtarı."""
    parca = []
    for s, d in V.items():
        dv = (d.Close * d.Volume).astype(float); dv.index = _e6_anahtar(d.index, zaman); parca.append(dv.rename(s))
    M = pd.concat(parca, axis=1)
    return M.median(axis=1, skipna=True)


def _e6_anahtar(ix: pd.DatetimeIndex, zaman: str) -> pd.Index:
    if zaman == "gunluk":
        return pd.DatetimeIndex(ix).normalize()
    c = pd.DatetimeIndex(ix).isocalendar()
    return pd.Index((c.year.to_numpy().astype(np.int64) * 100 + c.week.to_numpy().astype(np.int64)))


# ================================================================ 2) TARAMA (hisse başına)
_E6_ISCI: Dict[str, Any] = {}


def e6_hisse(d: pd.DataFrame, s: str, zaman: str, pazar: str, S: Dict[str, Any], dag: np.ndarray, uc: List[str], evren: np.ndarray,
             tohum: int) -> Dict[str, Any]:
    """Bir hissenin bütün geçerli pencereleri: F1, yüzdelik, katman; evren içi katman sayımları; katman başına bir düzgün rastgele pencere."""
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")); T = len(C); ix = d.index
    BU, BO, BA = MI.mi_bant(C); s0 = int(E6_ESIK["pencere"]["bas_min"])
    bc = np.r_[0, np.cumsum(d.bosluk.to_numpy(bool).astype(np.int64))] if "bosluk" in d.columns else None
    ara = (ix >= pd.Timestamp(uc[0])) & (ix <= pd.Timestamp(uc[1]))
    E_, M_, F_ = [], [], []
    for m in V3.MV3_ESIK["uzunluklar"]:
        if T - s0 < m:
            continue
        from numpy.lib.stride_tricks import sliding_window_view as swv
        W = [swv(x[s0:], m) for x in (O, H, L, C, BU, BO)]
        e = np.arange(s0 + m - 1, T)
        ok = ara[e]
        if bc is not None:
            ok &= (bc[e + 1] - bc[e - m + 2]) == 0
        if not ok.any():
            continue
        Wk = [w[ok] for w in W]
        F1, _, _ = V3.v3_aileler(V3.v3_ozet(*Wk), S["Z"])
        g = np.isfinite(F1); E_.append(e[ok][g]); M_.append(np.full(int(g.sum()), m)); F_.append(F1[g])
    out = {"sembol": s, "zaman": zaman, "pazar": pazar, "n_pencere": 0, "n_evren": 0, "say": {k: 0 for k in ("K1", "K2", "K3", "K4")}, "sec": {}}
    if not E_:
        return out
    e = np.concatenate(E_); m = np.concatenate(M_); F1 = np.concatenate(F_)
    pct = MV.mv_pct(dag, F1); kat = e6_katman(pct); ev = evren[e]
    out["n_pencere"] = int(len(e)); out["n_evren"] = int(ev.sum())
    for kk, maske in (("K1", kat == 1), ("K2", kat == 2), ("K3", kat == 3), ("K4", np.ones(len(e), bool))):
        w = np.flatnonzero(maske & ev); out["say"][kk] = int(len(w))
        if len(w):
            i = w[int(np.random.default_rng(_e6_tohum(tohum, zaman, pazar, s, kk)).integers(len(w)))]
            out["sec"][kk] = {"t": int(e[i]), "tarih": str(ix[e[i]].date()), "m": int(m[i]), "F1": float(F1[i]), "F1_pct": float(pct[i])}
    return out


def _e6_isci(s: str) -> Dict[str, Any]:
    G = _E6_ISCI; d = G["V"][s]; z = G["zaman"]; p = G["pazar"]
    if p in ("ABD", "AVR"):
        ev = np.zeros(len(d), bool)
        for (a, b), P in G["P"]:
            i = np.flatnonzero((d.index >= pd.Timestamp(a)) & (d.index <= pd.Timestamp(b)))
            if len(i):
                ev[i] = e6_p2_maske(P, s, d.index[i])
    else:
        dv = (d.Close * d.Volume).to_numpy(float); med = G["med"].reindex(_e6_anahtar(d.index, z)).to_numpy(float)
        ev = np.isfinite(med) & (dv > med)
    return e6_hisse(d, s, z, p, G["S"], G["dag"], G["uc"], ev, G["tohum"])


def e6_parcalar(zaman: str, pazar: str) -> List[Tuple[Tuple[str, str], str]]:
    """P2 maskesi için (tarih aralığı, günlük veri klasörü) parçaları: günlük -> açık kopya; haftalık 2001-15 p1, 2016-22 açık kopya (V2 / V3 kuralı)."""
    if zaman == "gunluk":
        return [(("1900-01-01", "2100-01-01"), MV.MV_YOL["gunluk"])]
    return [(("1900-01-01", "2015-12-31"), MH.MH_YOL["p1"]), (("2016-01-01", "2100-01-01"), MH.MH_YOL["p2"])]


def e6_p2_dogrula(P: Dict[str, Any], pazar: str, klasor: str, V: Dict[str, pd.DataFrame], ara: Tuple[str, str], n: int, tohum: int) -> Dict[str, Any]:
    """Vektörlü maske = MH.mh_p2 (n rastgele (hisse, tarih) çifti)."""
    rng = np.random.default_rng(tohum); syms = sorted(V); sat = []
    for _ in range(n * 3):
        s = syms[int(rng.integers(len(syms)))]; ix = V[s].index; ix = ix[(ix >= pd.Timestamp(ara[0])) & (ix <= pd.Timestamp(ara[1]))]
        if len(ix):
            sat.append((s, ix[int(rng.integers(len(ix)))]))
        if len(sat) >= n:
            break
    X = pd.DataFrame(sat, columns=["sembol", "tarih"]).drop_duplicates().reset_index(drop=True)
    a = MH.mh_p2(X, pazar, klasor)
    b = np.zeros(len(X), bool)
    for s, g in X.groupby("sembol"):
        b[g.index.to_numpy()] = e6_p2_maske(P, s, pd.DatetimeIndex(g.tarih))
    fark = int((a != b).sum())
    if fark:
        raise E6Hata(f"P2 vektörlü maske MH.mh_p2'den farklı: {fark} / {len(X)} ({pazar}, {klasor})")
    return {"n": int(len(X)), "fark": fark, "p2_pay": float(a.mean())}


def e6_tarama(cikti: Optional[str] = None, islem: int = 3) -> Dict[str, Any]:
    import multiprocessing as mp
    import KASA as KS
    t0 = time.time(); cikti = cikti or E6_YOL["cikti"]
    if os.path.exists(_e6_yol("tarama", cikti)):
        raise E6Hata("tarama zaten var")
    G0 = e6_kapi(cikti)
    yol = [os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + \
          [os.path.join(MV.MV_YOL["haftalik"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")]
    kasa = KS.kasa_kapisi(yol, "2022-12-31")
    S = V3.v3_sablon(); A4 = json.load(open(E6_YOL["anahtar4"], encoding="utf-8"))["sayfalar"]; haric = {r["sembol"] for r in A4}
    T = E6_ESIK["tohum"]; sonuc: List[Dict[str, Any]] = []; dog: Dict[str, Any] = {}; bar: Dict[str, Any] = {}
    for z in ("gunluk", "haftalik"):
        dag = np.sort(pd.read_pickle(E6_YOL["dagilim"][z]).F1.to_numpy(float)); uc = E6_ESIK["pencere"][z]
        for p in ("ABD", "AVR", "BIST"):
            V = MV.mv_veri(z, p); Ps: List[Any] = []; med = None
            if p in ("ABD", "AVR"):
                for ara, kl in e6_parcalar(z, p):
                    P = e6_p2_hazirla(p, kl)
                    a2 = (max(ara[0], uc[0]), min(ara[1], uc[1]))
                    dog[f"{z}|{p}|{os.path.basename(kl)}"] = e6_p2_dogrula(P, p, kl, V, a2, 2000, _e6_tohum(T["p2_dogrulama"], z, p, kl))
                    Ps.append((ara, P))
            else:
                med = e6_bist_medyan(V, z)
            _E6_ISCI.clear(); _E6_ISCI.update({"V": V, "zaman": z, "pazar": p, "P": Ps, "med": med, "S": S, "dag": dag, "uc": uc, "tohum": T["secim"]})
            try:
                with mp.get_context("fork").Pool(islem) as pool:
                    R = list(pool.imap(_e6_isci, sorted(V), chunksize=16))
            finally:
                _E6_ISCI.clear()
            sonuc += R; bar[f"{z}|{p}"] = {"hisse": len(R), "pencere": int(sum(r["n_pencere"] for r in R)), "evren": int(sum(r["n_evren"] for r in R)),
                                          **{k: int(sum(r["say"][k] for r in R)) for k in ("K1", "K2", "K3", "K4")}}
            del V, Ps, med; gc.collect()
            e6log.info("%s %s: %s (%.0f sn)", z, p, bar[f"{z}|{p}"], time.time() - t0)
    secim = e6_secim(sonuc, haric)
    tekrar = e6_tekrar_sec()
    J = {"surum": E6_SURUM, "kapi": G0, "kasa": kasa, "p2_dogrulama": dog, "evren_sayim": bar,
         "katman_evren": {k: {z: int(sum(v[k] for kk, v in bar.items() if kk.startswith(z))) for z in ("gunluk", "haftalik")} for k in ("K1", "K2", "K3", "K4")},
         "secim": secim, "tekrar": tekrar, "sure_sn": round(time.time() - t0)}
    if max(pd.Timestamp(r["tarih"]) for r in secim) > MI.MI_KESIK:
        raise E6Hata("KESİK AŞIMI")
    MI._mi_jyaz(os.path.join(E6_YOL["gecici"], "tarama_ham.json"), J, "tarama ham")
    J["secim"] = None; J["tekrar"] = None          # eşleme yalnız anahtarda (PDF adımında); tarama json'u sayım düzeyinde
    J["ham_sha"] = MI._mi_sha(os.path.join(E6_YOL["gecici"], "tarama_ham.json"))
    MI._mi_jyaz(_e6_yol("tarama", cikti), J, "tarama 6")
    return J


def e6_cek(aday: List[Dict[str, Any]], kat: str, n: int, tavan: int, gor: set, rng: np.random.Generator) -> List[Dict[str, Any]]:
    """Hisseler katman pencere sayısıyla orantılı, yerine koymadan; BIST tavanı; görülen hisse yok."""
    sec: List[Dict[str, Any]] = []; bist = 0
    for _ in range(n):
        h = [r for r in aday if r["say"][kat] > 0 and r["sembol"] not in gor and not (r["pazar"] == "BIST" and bist >= tavan)]
        if not h:
            raise E6Hata(f"{kat}: aday hisse kalmadı")
        w = np.array([r["say"][kat] for r in h], float); r = h[int(rng.choice(len(h), p=w / w.sum()))]
        sec.append(dict(r["sec"][kat], sembol=r["sembol"], zaman=r["zaman"], pazar=r["pazar"], katman=kat)); gor.add(r["sembol"]); bist += int(r["pazar"] == "BIST")
    return sec


def e6_secim(sonuc: List[Dict[str, Any]], haric: set) -> List[Dict[str, Any]]:
    rng = np.random.default_rng(E6_ESIK["tohum"]["secim"]); gor = set(haric); sec: List[Dict[str, Any]] = []
    for kat in ("K1", "K2", "K3", "K4"):
        n = int(E6_ESIK["katman"][kat]["n"]); nz = n // 2; tavan = nz // 3
        for z in ("gunluk", "haftalik"):
            sec += e6_cek([r for r in sonuc if r["zaman"] == z], kat, nz, tavan, gor, rng)
    return sec


def e6_tekrar_sec() -> List[Dict[str, Any]]:
    E = V3.v3_etiket_oku(E6_YOL["isaret4"]); A = json.load(open(E6_YOL["anahtar4"], encoding="utf-8"))["sayfalar"]
    rng = np.random.default_rng(E6_ESIK["tohum"]["tekrar"]); out = []
    for lab, k in ((1, 4), (0, 4)):
        h = sorted([r for r in A if E.get(int(r["sayfa"])) == lab], key=lambda r: int(r["sayfa"]))
        for i in np.sort(rng.choice(len(h), size=k, replace=False)):
            r = h[int(i)]; out.append({"zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "tarih": r["tarih"], "m": int(r["m"]), "katman": "T",
                                       "eski_sayfa": int(r["sayfa"]), "eski_isaret": int(lab), "eski_S": float(r["S"])})
    return out


# ================================================================ 3) ÖLÇÜLER (seçilen sayfalar; etiketten ÖNCE donar)
def e6_olcu(zaman: str, pazar: str, sembol: str, tarih: str, m: int, Vc: Dict[Any, Any], S: Dict[str, Any], sab1: Dict[str, Any],
            sabv: Dict[str, Any], dag: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    W = V3.v3_pencere(zaman, pazar, sembol, tarih, m, Vc)
    Z = V3.v3_ozet(W["O"], W["H"], W["L"], W["C"], W["BU"], W["BO"]); Sz = S["Z"]
    F1, F2, F3 = (float(f[0]) for f in V3.v3_aileler(Z, Sz)); Dz = V3.v3_D(zaman); d3 = float(V3.v3_D3(F1, F2, F3, Dz))
    duz = V3.v3_duz(W, S)
    if not np.allclose([F1, F2, F3], duz, atol=1e-10):
        raise E6Hata(f"K11: düz döngü farklı {sembol} {tarih}")
    par = {"F1_dizi": float(np.abs(Z["seq"] - Sz["seq"]).mean()), "F1_evre": float(np.abs(Z["evre"] - Sz["evre"]).mean())}
    for k in ("gap", "dC", "body", "icinde"):
        par[f"F2_{k}"] = float(np.abs(Z[k] - Sz[k]).mean())
    par["F2_uyum"] = float((np.mean(np.sign(Z["dC"]) == np.sign(Sz["dC"])) + np.mean(np.sign(Z["body"]) == np.sign(Sz["body"]))) / 2)
    for k in ("uw", "lw", "uwr", "lwr"):
        par[f"F3_{k}"] = float(np.abs(Z[k] - Sz[k]).mean())
    par["F3_uyum"] = float(np.mean(Z["uzun"] == Sz["uzun"]))
    Fo = MI.mi_ozellik(W["O"], W["H"], W["L"], W["C"], W["BU"], W["BO"], W["BA"]); Ek = MV.mv_ek_olcu(W["O"], W["H"], W["L"], W["C"], W["BU"], W["BA"])
    oz = {f"oz_{k}": float(abs(float(Fo[k][0]) - sabv["F"][k])) for k, _, _ in MI.MI_OZELLIK}
    oz.update({f"ek_{k}": float(abs(float(Ek[k][0]) - sabv["EK"][k])) for k in list(MV.MV_ESIK["ek_olcu"])[:4]})
    S1 = MV.mv_S_bilesen(sab1, {k: W[k] for k in ("O", "H", "L", "C", "BU", "BO", "BA")})
    pc = {f"{k}_pct": float(MV.mv_pct(dag[zaman][k].to_numpy(), v)) for k, v in (("F1", F1), ("F2", F2), ("F3", F3))}
    return {"F1": F1, "F2": F2, "F3": F3, "D3": d3, **pc, "parca": par, "oz39": oz, "v1_S": S1["S"], "v1_dizi": S1["dizi"], "v1_bant": S1["bant"], "v1_oz": S1["oz"]}


def e6_prefix(r: Dict[str, Any], Vc: Dict[Any, Any], S: Dict[str, Any]) -> float:
    """K2: veri pencere sonunda kesilince F1 aynı."""
    k = (r["zaman"], r["pazar"]); d = Vc[k][r["sembol"]]; dk = d[d.index <= pd.Timestamp(r["tarih"])]
    t = len(dk) - 1; m = int(r["m"]); BU, BO, BA = MI.mi_bant(dk.Close.to_numpy(float)); sl = slice(t - m + 1, t + 1)
    Z = V3.v3_ozet(*(dk[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close")), BU[sl], BO[sl])
    return abs(float(V3.v3_aileler(Z, S["Z"])[0][0]) - float(r["olcu"]["F1"]))


# ================================================================ 4) PDF ve ANAHTAR
def e6_pdf(cikti: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import Rectangle
    cikti = cikti or E6_YOL["cikti"]; y = _e6_yol("pdf", cikti); ya = _e6_yol("anahtar", cikti)
    if os.path.exists(y) or os.path.exists(ya):
        raise E6Hata("PDF / anahtar zaten var")
    JT = json.load(open(_e6_yol("tarama", cikti), encoding="utf-8")); hp = os.path.join(E6_YOL["gecici"], "tarama_ham.json")
    if MI._mi_sha(hp) != JT["ham_sha"]:
        raise E6Hata("tarama ham dosyası değişmiş")
    H = json.load(open(hp, encoding="utf-8")); sec = H["tekrar"] + H["secim"]
    S = V3.v3_sablon(); sab1 = MI.mi_sablon_yukle()["tam"]; sabv = MV.mv_sablon()["tam"]; a = sabv["ohlc"]
    dag = {z: pd.read_pickle(E6_YOL["dagilim"][z]) for z in ("gunluk", "haftalik")}; Vc: Dict[Any, Any] = {}
    for r in sec:
        r["olcu"] = e6_olcu(r["zaman"], r["pazar"], r["sembol"], r["tarih"], int(r["m"]), Vc, S, sab1, sabv, dag)
        if r["katman"] != "T" and abs(r["olcu"]["F1"] - r["F1"]) > 1e-10:
            raise E6Hata(f"tarama F1 ile sayfa F1 farklı: {r['sembol']}")
        if r["katman"] == "T" and abs(r["olcu"]["v1_S"] - r["eski_S"]) > 1e-4:
            raise E6Hata("K11: tekrar sayfasında v1 S MUM_IZI4 anahtarından farklı")
    pre = max(e6_prefix(r, Vc, S) for r in sec if r["katman"] != "T")
    if not pre < 1e-12:
        raise E6Hata(f"K2 prefix tutmadı {pre}")
    A4 = json.load(open(E6_YOL["anahtar4"], encoding="utf-8"))["sayfalar"]; E4 = V3.v3_etiket_oku(E6_YOL["isaret4"]); eski = []
    for r in A4:
        eski.append({"sayfa4": int(r["sayfa"]), "isaret4": E4.get(int(r["sayfa"])), "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "tarih": r["tarih"],
                     "m": int(r["m"]), "olcu": e6_olcu(r["zaman"], r["pazar"], r["sembol"], r["tarih"], int(r["m"]), Vc, S, sab1, sabv, dag)})
    p = np.random.default_rng(E6_ESIK["tohum"]["sira"]).permutation(len(sec))
    sayfa = [dict(sec[i], sayfa=j + 2) for j, i in enumerate(p)]
    once = int(MV.MV_ESIK["onay"]["once"])
    with PdfPages(y, metadata={"Title": "MUM_IZI6 etiket", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.06, 0.94, "ETİKET SETİ 2", fontsize=16, weight="bold")
        fig.text(0.06, 0.88, E6_KAPAK, fontsize=13, va="top", wrap=True)
        MV._mv_ciz(fig.add_axes([0.25, 0.2, 0.5, 0.35]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
        pdf.savefig(fig); plt.close(fig)
        for r in sayfa:
            d = Vc[(r["zaman"], r["pazar"])][r["sembol"]]; t = d.index.get_loc(pd.Timestamp(r["tarih"])); m = int(r["m"]); i0 = max(0, t - m + 1 - once)
            BU, BO, BA = MI.mi_bant(d.Close.to_numpy(float)); sl = slice(i0, t + 1)
            fig = plt.figure(figsize=(8.3, 11.7))
            MV._mv_ciz(fig.add_axes([0.04, 0.6, 0.3, 0.28]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
            MV._mv_ciz(fig.add_axes([0.38, 0.45, 0.58, 0.45]), *(d[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close")), BU[sl], BO[sl], BA[sl],
                       (t - m + 1 - i0, t - i0), f"Sayfa {r['sayfa']}: bulunan bölge ({'haftalık' if r['zaman'] == 'haftalik' else 'günlük'} mum)")
            ax = fig.add_axes([0.1, 0.12, 0.8, 0.22]); ax.axis("off")
            for xx, txt in ((0.0, "✓  benziyor"), (0.55, "✗  benzemiyor")):
                ax.add_patch(Rectangle((xx, 0.1), 0.42, 0.8, fill=False, linewidth=3, transform=ax.transAxes))
                ax.text(xx + 0.21, 0.5, txt, ha="center", va="center", fontsize=22, transform=ax.transAxes)
            fig.text(0.04, 0.4, "Turuncu kutu = bölge; sağ kenar = bölgenin sonu (sonrası gösterilmiyor).\nMor = Bollinger 20 ve SMA20 (kesik).", fontsize=9)
            pdf.savefig(fig); plt.close(fig)
    K = {"not": "MÜHÜRLÜ: sayfa -> hisse / tarih / katman / ölçüler; PDF'e, rapora ve commit mesajına girmez; yalnız olc okur",
         "surum": E6_SURUM, "pdf_sha": MI._mi_sha(y), "prefix_en_buyuk": pre, "sayfalar": sayfa, "eski24": eski}
    MI._mi_jyaz(ya, K, "anahtar 6")
    JT["anahtar_sha"] = MI._mi_sha(ya); JT["pdf_sha"] = K["pdf_sha"]; JT["sayim"] = e6_sayim(sayfa)
    MI._mi_jyaz(_e6_yol("tarama", cikti), JT, "tarama 6")
    return y


def e6_sayim(sayfa: List[Dict[str, Any]]) -> Dict[str, Any]:
    X = pd.DataFrame([{k: r[k] for k in ("katman", "zaman", "pazar")} for r in sayfa])
    return {"toplam": int(len(X)), "katman": X.katman.value_counts().sort_index().to_dict(),
            "katman_zaman": {f"{k}|{z}": int(v) for (k, z), v in X.groupby(["katman", "zaman"]).size().items()},
            "katman_pazar": {f"{k}|{p}": int(v) for (k, p), v in X.groupby(["katman", "pazar"]).size().items()},
            "zaman": X.zaman.value_counts().to_dict(), "pazar": X.pazar.value_counts().to_dict()}


# ================================================================ 5) KAPI ve ÖN KAYIT
def e6_sha_simdi() -> Dict[str, str]:
    return {"KOD6_SHA": MI._mi_sha(E6_YOL["kod"]), "ESIK6_SHA": e6_esik_sha(), "V3_KOD_SHA": MI._mi_sha(V3.V3_YOL["kod"]), "ESIK5_SHA": V3.v3_esik_sha(),
            "DAGILIM5_JSON_SHA": MI._mi_sha(os.path.join(V3.V3_YOL["cikti"], V3.V3_DOSYA["dagilim"])),
            "DAGILIM_GUNLUK_PKL_SHA": MI._mi_sha(E6_YOL["dagilim"]["gunluk"]), "DAGILIM_HAFTALIK_PKL_SHA": MI._mi_sha(E6_YOL["dagilim"]["haftalik"]),
            "MI_KOD_SHA": MI._mi_sha(MI.MI_YOL["kod"]), "MH_KOD_SHA": MI._mi_sha(MH.MH_YOL["kod"]), "MV_KOD_SHA": MI._mi_sha(MV.MV_YOL["kod"])}


def e6_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or E6_YOL["cikti"]; yol = _e6_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise E6Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = e6_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise E6Hata(f"ön kayıt kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_E6)
    c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise E6Hata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_ETIKET2.py", "MUM_IZI_V3.py", "MUM_IZI.py", "MUM_IZI_HAFTALIK.py", "MUM_IZI_V2.py"]):
        raise E6Hata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def e6_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or E6_YOL["cikti"]; y = _e6_yol("onkayit", cikti)
    if os.path.exists(y):
        raise E6Hata("ön kayıt zaten var")
    for z, p in E6_YOL["dagilim"].items():
        R = pd.read_pickle(p); J = json.load(open(os.path.join(V3.V3_YOL["cikti"], V3.V3_DOSYA["dagilim"]), encoding="utf-8"))[z]
        if not (len(R) == J["n"] and abs(float(R.F1.median()) - J["tau"][0]) < 1e-12):
            raise E6Hata(f"dağılım pkl mum_izi5_dagilim.json ile uyuşmuyor ({z})")
    sh = e6_sha_simdi(); ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in E6_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_ETIKET2.py"])
    s = [f"# MUM_IZI6 ÖN KAYIT ({MI._mi_simdi()})", "",
         "Etiket seti 2: yeni ölçü yok; donmuş MUM_IZI_V3 ölçüleri. Bu dosya evren taramasından, seçimden ve PDF'ten ÖNCE commit edilir. Sınamalar (T1-T4) "
         "Cemal'in işaret dosyası (cemal_mum_izi6_etiket.json) gelince `python MUM_IZI_ETIKET2.py olc` ile AYNEN koşulur; eşikler sonuca göre değişmez.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_ETIKET2.py commit'i: {kc or 'yok'}",
         "- Dağılım pkl dosyaları /tmp'de (repoda değil); MUM_IZI_V3.py v3_dagilim ile aynı tohumlarla yeniden üretilir; pkl ile mum_izi5_dagilim.json (n, tau1) uyumu denetlendi.", "",
         "## Seçim kuralı, tohumlar, sınamalar (E6_ESIK; sha yukarıda)", "", "```", json.dumps(E6_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## Uygulamada verilen kararlar (iş tanımında açık bırakılanlar)", "",
         "1. Pencere = (hisse, son, m), m = V3 uzunlukları (16 / 18 / 20 / 22 / 24); her pencerenin kendi F1 yüzdeliği (V3 dağılımı uzunlukları birleşik).",
         "2. Katman içi 'rastgele': katmandaki evren içi pencereler arasında düzgün; hisse başına bir (iki aşamalı: hisse ~ pencere sayısı, hisse içinde düzgün).",
         "3. BIST tavanı katman x zaman dilimi başına floor((n / 2) / 3): K1 2 + 2, K2 2 + 2, K3 1 + 1, K4 1 + 1 (katman başına üçte birin altında).",
         "4. Haftalık BIST likiditesi ISO haftası kesit medyanıyla (haftanın son günleri hisseden hisseye değişir).",
         "5. ABD / AVR P2: MH.mh_p2 kuralının vektörlü hali; tarama başında her parça için 2.000 çiftte MH.mh_p2 ile birebir denetlenir (fark -> DUR).",
         "6. T1'de karar olmayan yeni işaret 'aynı değil' sayılır. T2'de en az 3 EVET ve 3 HAYIR yoksa ÖLÇÜLEMEDİ. T2 hükmünde AUC >= 0,80 ama alt uç < 0,65 ise KISMEN.",
         "7. T4'te önceki 24 sayfa İLK işaretleriyle (MUM_IZI4); tekrar sayfalarının yeni işareti yalnız T1'de.",
         "8. Bütün sayfa ölçüleri (F1-F3, D3, parçalar, 39 ölçü, v1 S) PDF adımında anahtara yazılır: Cemal'in işaretinden ÖNCE donar.", "",
         "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 6")


# ================================================================ 6) ÖLÇÜM (Cemal işaretleyince)
_E6_DEGER = {"EVET": 1, "HAYIR": 0, "YOK": None, "IKISI": None, "BELIRSIZ": None}


def e6_etiket_oku(yol: str) -> Dict[int, Tuple[Optional[int], str]]:
    """Şemaya sıkı: {"sayfalar": {"<no>": {"isaret": ...}}}; no 1-49, değer EVET / HAYIR / YOK / IKISI / BELIRSIZ; başka -> DUR."""
    J = json.load(open(yol, encoding="utf-8"))
    if not isinstance(J, dict) or not isinstance(J.get("sayfalar"), dict):
        raise E6Hata("etiket şeması: 'sayfalar' sözlüğü yok")
    out: Dict[int, Tuple[Optional[int], str]] = {}
    for k, v in J["sayfalar"].items():
        if not str(k).strip().isdigit() or not (1 <= int(k) <= 49):
            raise E6Hata(f"etiket şeması: sayfa numarası {k!r}")
        if not isinstance(v, dict) or "isaret" not in v:
            raise E6Hata(f"etiket şeması: sayfa {k} 'isaret' yok")
        t = str(v["isaret"]).strip().replace("İ", "I").replace("ı", "I").upper()
        if t not in _E6_DEGER:
            raise E6Hata(f"etiket şeması: sayfa {k} bilinmeyen değer {v['isaret']!r}")
        out[int(k)] = (_E6_DEGER[t], t)
    return out


def _e6_lojistik(X: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    n, p = X.shape; Xa = np.c_[np.ones(n), X]; w = np.zeros(p + 1); R = lam * np.eye(p + 1); R[0, 0] = 0.0
    for _ in range(100):
        pr = 1 / (1 + np.exp(-np.clip(Xa @ w, -30, 30))); W = pr * (1 - pr)
        g = Xa.T @ (pr - y) + R @ w; Hs = Xa.T @ (Xa * W[:, None]) + R
        st = np.linalg.solve(Hs, g); w = w - st
        if np.max(np.abs(st)) < 1e-9:
            break
    return w


def e6_cv_auc(X: np.ndarray, y: np.ndarray, lam: float, kat: int, tekrar: int, tohum: int) -> np.ndarray:
    rng = np.random.default_rng(tohum); out = []
    for _ in range(tekrar):
        f = np.zeros(len(y), int)
        for c in (0, 1):
            i = np.flatnonzero(y == c); rng.shuffle(i); f[i] = np.arange(len(i)) % kat
        sk = np.zeros(len(y))
        for k in range(kat):
            tr = f != k; te = ~tr; mu = X[tr].mean(0); sd = X[tr].std(0); sd[sd < 1e-12] = 1.0
            w = _e6_lojistik((X[tr] - mu) / sd, y[tr].astype(float), lam); sk[te] = np.c_[np.ones(te.sum()), (X[te] - mu) / sd] @ w
        out.append(V3.v3_auc(-sk[y == 1], -sk[y == 0]))       # büyük skor = benziyor
    return np.array(out)


def e6_ozellik(o: Dict[str, Any]) -> List[float]:
    return [o["parca"][k] for k in sorted(o["parca"])] + [o["oz39"][k] for k in sorted(o["oz39"])]


def e6_olc(etiket: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time(); kaynak = E6_YOL["cikti"]; cikti = cikti or kaynak; etiket = etiket or _e6_yol("etiket", kaynak)
    if os.path.exists(_e6_yol("olcum", cikti)):
        raise E6Hata("ölçüm zaten var")
    G0 = e6_kapi(kaynak)
    JT = json.load(open(_e6_yol("tarama", kaynak), encoding="utf-8")); ya = _e6_yol("anahtar", kaynak)
    if MI._mi_sha(ya) != JT.get("anahtar_sha"):
        raise E6Hata("anahtar mühürü tutmadı")
    K = json.load(open(ya, encoding="utf-8")); E = e6_etiket_oku(etiket)
    karar = {"EVET": 0, "HAYIR": 0, "YOK": 0, "IKISI": 0, "BELIRSIZ": 0, "eksik": 0}
    rows = []
    for r in K["sayfalar"]:
        v, t = E.get(int(r["sayfa"]), (None, "eksik")); karar[t] += 1
        rows.append({**{k: r[k] for k in ("sayfa", "katman", "zaman", "pazar")}, "eski_isaret": r.get("eski_isaret"), "y": v, **{k: r["olcu"][k] for k in
                     ("F1", "F2", "F3", "D3", "v1_S")}, "F1_evre": r["olcu"]["parca"]["F1_evre"], "F1_dizi": r["olcu"]["parca"]["F1_dizi"], "oz": e6_ozellik(r["olcu"])})
    X = pd.DataFrame(rows); B = int(E6_ESIK["T2"]["B"]); tb = int(E6_ESIK["tohum"]["boot"]); out: Dict[str, Any] = {"surum": E6_SURUM, "kapi": G0, "etiket_sha": MI._mi_sha(etiket),
                                                                                                                  "karar_sayim": karar}
    # T1
    T = X[X.katman == "T"]; ayni = int(sum(1 for r in T.itertuples() if r.y is not None and not pd.isna(r.y) and int(r.y) == int(r.eski_isaret)))
    h = E6_ESIK["T1"]["hukum"]
    out["T1"] = {"n": int(len(T)), "karar_verilen": int(T.y.notna().sum()), "ayni": ayni,
                 "hukum": "TUTARLI" if ayni >= h["tutarli"] else ("KISMEN" if ayni >= h["kismen"] else "TUTARSIZ")}
    # T2
    Y = X[(X.katman != "T") & X.y.notna()].copy(); Y["y"] = Y.y.astype(int); y = Y.y.to_numpy(); en = int(E6_ESIK["T2"]["en_az"]); es = E6_ESIK["T2"]["esik"]
    if y.sum() < en or (1 - y).sum() < en:
        t2 = {"n": int(len(Y)), "n_benz": int(y.sum()), "hukum": "ÖLÇÜLEMEDİ"}
    else:
        t2 = _e6_ozet(Y.F1.to_numpy(), y, True, B, tb)
        a = t2["auc"]; lo = t2["boot95"][0]
        t2["hukum"] = "UYUMLU" if (a >= es["uyumlu"] and lo >= es["alt_uc"]) else ("KISMEN" if a >= es["kismen"] else "UYUMSUZ")
    pay = {k: (float(g.y.mean()) if len(g) else None) for k, g in ((k, Y[Y.katman == k]) for k in ("K1", "K2", "K3", "K4"))}
    pv = [pay[k] for k in ("K1", "K2", "K3", "K4")]
    t2["katman_benziyor_payi"] = pay; t2["katman_n"] = {k: int((Y.katman == k).sum()) for k in ("K1", "K2", "K3", "K4")}
    t2["sira_tutuyor"] = bool(all(v is not None for v in pv) and pv[0] >= pv[1] >= pv[2] >= pv[3] and pv[0] > pv[3])
    t2["tam_sira"] = bool(all(v is not None for v in pv) and pv[0] > pv[1] > pv[2] > pv[3])
    out["T2"] = t2
    # T3
    t3: Dict[str, Any] = {}
    for ad, kucuk in (("F1", True), ("D3", True), ("F2", True), ("F3", True), ("F1_evre", True), ("F1_dizi", True), ("v1_S", False)):
        t3[ad] = {"hepsi": _e6_ozet(Y[ad].to_numpy(), y, kucuk, B, tb) if len(Y) else None}
        for z in ("gunluk", "haftalik"):
            g = Y[Y.zaman == z]; t3[ad][z] = _e6_ozet(g[ad].to_numpy(), g.y.to_numpy(), kucuk, B, tb) if len(g) else None
    out["T3"] = t3
    # T4
    T4 = E6_ESIK["T4"]; Xs = [np.array(v) for v in Y.oz]; ys = list(y)
    for r in K["eski24"]:
        if r["isaret4"] is not None:
            Xs.append(np.array(e6_ozellik(r["olcu"]))); ys.append(int(r["isaret4"]))
    Xm = np.vstack(Xs); ym = np.array(ys, int)
    if not np.isfinite(Xm).all():
        raise E6Hata("T4 girdisinde sonlu olmayan değer")
    if ym.sum() >= T4["kat"] and (1 - ym).sum() >= T4["kat"]:
        cv = e6_cv_auc(Xm, ym, T4["lambda"], T4["kat"], T4["tekrar"], E6_ESIK["tohum"]["t4_cv"]); rng = np.random.default_rng(E6_ESIK["tohum"]["t4_null"]); nul = []
        for i in range(int(T4["null"])):
            nul.append(float(e6_cv_auc(Xm, rng.permutation(ym), T4["lambda"], T4["kat"], T4["null_tekrar"], int(rng.integers(2**31))).mean()))
        nul = np.array(nul)
        out["T4"] = {"n": int(len(ym)), "n_benz": int(ym.sum()), "girdi": int(Xm.shape[1]), "cv_auc": float(cv.mean()), "cv_aralik": np.quantile(cv, [0.025, 0.975]).tolist(),
                     "null_ort": float(nul.mean()), "null_95": float(np.quantile(nul, 0.95)), "p": float((1 + (nul >= cv.mean()).sum()) / (1 + len(nul))),
                     "not": "EZBER RİSKLİ; yalnız bilgi"}
    else:
        out["T4"] = {"n": int(len(ym)), "n_benz": int(ym.sum()), "hukum": "ÖLÇÜLEMEDİ (sınıf başına en az kat sayısı kadar etiket yok)"}
    out["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_e6_yol("olcum", cikti), out, "ölçüm 6")
    MI._mi_yaz(_e6_yol("olcum_md", cikti), e6_olcum_md(out), "ölçüm 6 md")
    return out


def _f(x: Any, n: int = 3) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{n}f}"


def e6_olcum_md(o: Dict[str, Any]) -> str:
    t1 = o["T1"]; t2 = o["T2"]
    L = [f"# MUM_IZI6 ÖLÇÜM ({MI._mi_simdi()})", "", f"Etiket sayımı: {o['karar_sayim']}", "",
         f"## T1 tutarlılık: {t1['hukum']} ({t1['ayni']} / {t1['n']} aynı; karar verilen {t1['karar_verilen']})",
         "" if t1["hukum"] != "TUTARSIZ" else "Göz kendi içinde tutarsız: hiçbir formül bu etiketleri tutturamaz.", "",
         f"## T2 konum (ana): {t2['hukum']}", "",
         f"AUC {_f(t2.get('auc'))}, %95 {_f((t2.get('boot95') or [None, None])[0], 2)}-{_f((t2.get('boot95') or [None, None])[1], 2)}, p {_f(t2.get('p'), 4)}, "
         f"n {t2.get('n')} (benziyor {t2.get('n_benz')})", "",
         f"Katmana göre benziyor payı: {t2['katman_benziyor_payi']} (n {t2['katman_n']}); sıra tutuyor: {t2['sira_tutuyor']}; tam sıra: {t2['tam_sira']}", "",
         "## T3 (bilgi)", "", "| ölçü | AUC hepsi | p | günlük | haftalık |", "|---|---|---|---|---|"]
    for k, v in o["T3"].items():
        h = v["hepsi"] or {}
        L.append(f"| {k} | {_f(h.get('auc'))} | {_f(h.get('p'), 4)} | {_f((v.get('gunluk') or {}).get('auc'))} | {_f((v.get('haftalik') or {}).get('auc'))} |")
    L += ["", f"## T4 (bilgi, EZBER RİSKLİ): {json.dumps(o['T4'], ensure_ascii=False)}", ""]
    return "\n".join(L)


# ================================================================ 7) RAPOR (yalnız sayım)
def e6_rapor(cikti: Optional[str] = None, ek: str = "") -> str:
    cikti = cikti or E6_YOL["cikti"]; J = json.load(open(_e6_yol("tarama", cikti), encoding="utf-8")); s = J["sayim"]
    L = [f"# MUM_IZI6 RAPOR ({MI._mi_simdi()})", "", f"Sürüm: {E6_SURUM}. Getiri / sonrası yok. Sayfa -> katman / etiket eşlemesi bu dosyada YOK (mühürlü anahtarda).", "",
         "## SET", "", f"- Toplam {s['toplam']} sayfa + kapak (MUM_IZI6_ETIKET.pdf, {s['toplam'] + 1} sayfa).",
         f"- Katman başına sayfa: {s['katman']}", f"- Katman x zaman dilimi: {s['katman_zaman']}", f"- Katman x pazar: {s['katman_pazar']}",
         f"- Zaman dilimi: {s['zaman']}; pazar: {s['pazar']}", "", "## EVREN (evren içi pencere sayısı; pencere = hisse x son x uzunluk)", "",
         "| zaman / pazar | hisse | pencere | evren içi | K1 | K2 | K3 | K4 |", "|---|---|---|---|---|---|---|---|"]
    for k, v in J["evren_sayim"].items():
        L.append(f"| {k} | {v['hisse']} | {v['pencere']} | {v['evren']} | {v['K1']} | {v['K2']} | {v['K3']} | {v['K4']} |")
    L += ["", f"- P2 vektörlü maske denetimi (MH.mh_p2 ile): {J['p2_dogrulama']}", f"- KASA: {J['kasa'].get('kesik')}; sha: tarama {J.get('ham_sha', '')[:12]}, "
          f"anahtar {J.get('anahtar_sha', '')[:12]}, PDF {J.get('pdf_sha', '')[:12]}", "", ek]
    return MI._mi_yaz(_e6_yol("rapor", cikti), "\n".join(L), "rapor 6")


# ================================================================ 8) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_e6(_once=_CK_ONCE_E6, _dosya="MUM_IZI_ETIKET2.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_E6",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_e6()


def _e6_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_ETIKET2")
    ap.add_argument("komut", choices=["onkayit", "tarama", "pdf", "rapor", "olc"])
    ap.add_argument("--etiket", default=None); ap.add_argument("--cikti", default=None)
    a = ap.parse_args(argv)
    try:
        if a.komut == "onkayit":
            print(e6_onkayit_yaz())
        elif a.komut == "tarama":
            J = e6_tarama(); print(json.dumps(MI._mi_json({k: J[k] for k in ("evren_sayim", "katman_evren", "p2_dogrulama")}), ensure_ascii=False)[:3000])
        elif a.komut == "pdf":
            print(e6_pdf())
        elif a.komut == "rapor":
            print(e6_rapor())
        elif a.komut == "olc":
            J = e6_olc(a.etiket, a.cikti); print(json.dumps(MI._mi_json({k: J[k] for k in ("karar_sayim", "T1", "T2")}), ensure_ascii=False)[:3000])
    except E6Hata as ex:
        e6log.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_e6_ana())
