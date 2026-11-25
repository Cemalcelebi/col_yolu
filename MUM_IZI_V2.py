"""MUM_IZI_V2 — MUM_IZI EK 4: CEMAL'İN İTİRAZI. FARK ÖLÇÜMÜ + HATA DÖKÜMÜ + v2 DEDEKTÖR (zorunlu mum yapısı kapıları) + GÖRSEL ONAY (25 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI4_IS_TANIMI.md (commit d0a88e1; ana model). Cemal (25 Kas 13:53, ORNEK3_CEMAL_ITIRAZ_25Kas.jpg): "Aynı mı?
Bu mudur senin parmak izi dediğin şey? Eğer buysa bak gör farkı nedir, nerede ne denli hataların var; bu hataları bir daha yapmanı yasaklıyorum."

BU İŞTE GETİRİ / SONRASI HESAPLANMAZ. v2 kapıları yalnız şablondan (ve gerçek açık verinin getirisiz ölçü dağılımından) türetilir. v1 kodu / şablonu /
ön kaydı / sonuçları DEĞİŞMEZ (MUM_IZI.py, MUM_IZI_HAFTALIK.py yalnız içe alınır). Veri <= 2022-12-31; KASA açılmaz.

Komut:  python MUM_IZI_V2.py fark        A1-A4 (itiraz edilen bölge, v1 eşleşmelerinin ölçü sapması, mum / bant büyüklüğü, karşı örnekler) + dağılımlar
        python MUM_IZI_V2.py sentetik    C2: v2 sentetik pozitif / negatif / rastgele testi
        python MUM_IZI_V2.py onkayit     MUM_IZI4_ON_KAYIT.md
        python MUM_IZI_V2.py say         C3: kapı -> gerçek veride v2 BÖLGE SAYISI (günlük 2016-22, haftalık 2001-22) -> onay seti seçimi
        python MUM_IZI_V2.py onay        C4: MUM_IZI4_ONAY.pdf + mum_izi4_onay_anahtar.json
        python MUM_IZI_V2.py rapor       MUM_IZI4_RAPOR.md
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_MV = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from numpy.lib.stride_tricks import sliding_window_view as _swv4  # noqa: E402

KOK_MV = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_MV not in sys.path:
    sys.path.insert(0, KOK_MV)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAFTALIK as MH  # noqa: E402  (DEĞİŞTİRİLMEZ)

mvlog = logging.getLogger("col.mum_izi_v2")
if not mvlog.handlers:
    _mv_h = logging.StreamHandler(sys.stderr)
    _mv_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_v2: %(message)s", "%H:%M:%S"))
    mvlog.addHandler(_mv_h)
    mvlog.setLevel(logging.INFO)
    mvlog.propagate = False


class MVHata(RuntimeError):
    """Durdurucu hata: veri / kapı / kesik / doğrulama."""


MV_SURUM = "MUM_IZI_V2 v1.0 (2026-11-25): Cemal'in itirazı -> fark ölçümü, hata dökümü, v2 = v1 S + 7 zorunlu mum yapısı kapısı (getirisiz), görsel onay"
MV_YOL = {"cikti": MI.MI_YOL["cikti"], "kod": os.path.join(KOK_MV, "MUM_IZI_V2.py"), "gunluk": MI.MI_YOL["acik"], "haftalik": MH.MH_YOL["tam"],
          "gecici": "/tmp/mum_izi/v2", "itiraz": os.path.join(MI.MI_YOL["cikti"], "ORNEK3_CEMAL_ITIRAZ_25Kas.jpg"),
          "sentetik_satir": "/tmp/mum_izi/sentetik_satir.pkl"}
MV_DOSYA = {"onkayit": "MUM_IZI4_ON_KAYIT.md", "rapor": "MUM_IZI4_RAPOR.md", "fark": "mum_izi4_fark.csv", "sonuc": "mum_izi4_sonuc.json",
            "onay": "MUM_IZI4_ONAY.pdf", "anahtar": "mum_izi4_onay_anahtar.json", "fark_json": "mum_izi4_fark.json", "sentetik": "mum_izi4_sentetik.json",
            "esikler": "mum_izi4_kapi_esik.json"}

MV_ESIK: Dict[str, Any] = {
    "surum": "MV-1.0",
    "ek_olcu": {"mum_bant": "ortalama (H - L) / (üst - alt bant), mum başına oranların ortalaması",
                "govde_bant": "ortalama |C - O| / (üst - alt bant)", "max_mum_bant": "en büyük (H - L) / (üst - alt bant)",
                "max_govde_bant": "en büyük |C - O| / (üst - alt bant)",
                "not": "A3'ün 3 ölçüsü + k4'ün 'en büyük gövde / bant' ölçüsü; bant = o mumdaki Bollinger (20, 2) genişliği; şablonda görüntüden"},
    "dagilim": {"n": 20000, "L": [14, 15, 16, 17, 18, 19, 20, 22, 24],
                "gunluk": {"veri": "MUM_IZI açık kopya (/tmp/mum_izi/acik; ABD + AVR + BIST; <= 2022-12-30)", "uclar": ["2016-01-01", "2022-12-31"],
                           "tohum": 25112041},
                "haftalik": {"veri": "MUM_IZI_HAFTALIK tam kopya haftalık bar (ABD + AVR + BIST; 2000-2022)", "uclar": ["2001-01-01", "2022-12-31"],
                             "tohum": 25112042, "eksik_hafta": "pencerede eksik hafta (ardışık ISO haftaları arasında boşluk) varsa pencere atılır"},
                "yontem": "MUM_IZI2 yöntemi: geçerli (hisse, pencere sonu) çiftleri üç pazar birleşik havuz, pencere başı >= 19 (bant tanımlı), "
                          "yerine koymadan düzgün 20.000; tohum = taban + L; yüzdelik p = (#< + 0,5 #=) / N"},
    "kapilar": {
        "k1": {"ad": "uzun üst fitil", "olcu": [["ust_fitil", "Y"], ["uzun_ust_pay", "Y"]]},
        "k2": {"ad": "kısa alt fitil", "olcu": [["alt_fitil", "D"]]},
        "k3": {"ad": "küçük gövde / doji", "olcu": [["govde_oran", "D"], ["doji_pay", "Y"]]},
        "k4": {"ad": "küçük mumlar (banda göre de)", "olcu": [["kucuk_mum_pay", "Y"]], "ek": [["mum_bant", 1.25], ["max_govde_bant", 1.25]]},
        "k5": {"ad": "yükselen dipler", "olcu": [["yuk_dip_pay", "Y"]]},
        "k6": {"ad": "alt banttan üst banda", "ham": [["pB_bas", "<=", 0.25], ["pB_son", ">=", 0.75]]},
        "k7": {"ad": "mumlar birbirine biniyor", "olcu": [["ortusme", "Y"]]},
        "esik": "Y (yüksek uç): ölçü >= min(q_L(0,75), şablon değeri); D (düşük uç): ölçü <= max(q_L(0,25), şablon değeri); q_L = aynı zaman dilimi ve "
                "aynı pencere uzunluğu L dağılımı (tam şablonda bütün kapı değerleri uç dilimde olduğu için eşik = q_L; tepesizde govde_oran (p 0,30) "
                "ve yuk_dip_pay (p 0,62) uç dilimde değil -> eşik şablon değeri: şablon kendi kapısından geçer, daha sıradan pencere geçmez); "
                "k4 ek: mum_bant <= şablon x 1,25, max_govde_bant <= şablon x 1,25; k6 ham değer",
        "kabul": "v2 kabul = v1 S >= eşik (tam 0,59 / tepesiz 0,56, AYNEN) VE aynı penceredeki 7 kapının hepsi; t'de L uzunluklarından biri kabul "
                 "edilirse olay, m = en büyük S'li kabul edilen L; aynı hissede 15 bar tekil (ilk)"},
    "karsi_ornek": {"n1": "aynı kapanış yolu, gövde = şablon ortalama mum boyu (yeşil / kırmızı kapanış yönüne göre), fitil yok",
                    "n2": "aynı O / C, üst ve alt fitil yer değiştirmiş", "n3": "aynı kapanış, O / H / L kapanış etrafında 2 kat (mum boyu 2 x)",
                    "p1": "şablonun mum biçimleri (O / H / L kapanışa göre), kapanış yolu yatay (ilk kapanışta sabit)",
                    "p1b": "aynı mum biçimleri, kapanış yolu düşen (şablon kapanış değişimlerinin tersi)",
                    "A4": "şablonun görüntüdeki bantlarıyla S ve üç bileşen"},
    "sentetik": {"kok": 25112043, "tohum": 200, "gurultu": [0.0, 0.1, 0.2], "uretec": ["blok", "ry"], "baglam": ["dip", "yatay", "tepe"],
                 "negatif": ["n1", "n2", "n3"], "yanlis_seri": 200, "yanlis_n": 1000,
                 "kabul_olcutu": "n1 / n2 / n3 gömülü serilerde v2 kabul payı (gerçek sonun +-3 barında) <= %5 HER BİRİNDE; rastgele seride v2 tekil "
                                 "kabul (1.000 bar başına) <= v1'in 1 / 5'i (iki üretici ayrı). Yakalama düşerse yazılır; kapılar gevşetilmez"},
    "say": {"gunluk": {"donem": {"d1619": ["2016-01-01", "2019-12-31"], "d2022": ["2020-01-01", "2022-12-31"]}},
            "haftalik": {"donem": {"h0107": ["2001-01-01", "2007-12-31"], "h0815": ["2008-01-01", "2015-12-31"], "h1622": ["2016-01-01", "2022-12-31"]}},
            "evren": "ABD / AVR: TEZGAH2 P2 (giriş günü; KART_TUR2) ; BIST: hepsi; sayılar evren içi ve bütün (v1 ile aynı tanım); v1 oranı = v2 / v1 aynı hücre",
            "getiri": "HESAPLANMAZ"},
    "onay": {"tohum": 25112044, "haftalik": 12, "gunluk": 12, "once": 15,
             "secim": "v2 kabul edilen TAM şablon bölgeleri (evren içi) -> zaman dilimi başına hisse başına ilk olay -> tohumla RASTGELE (S'ye göre değil) "
                      "12 haftalık + 12 günlük; günlük listede haftalıkta seçilen hisseler dışarıda; sayfa sırası tohumla karıştırılır; 24'ten azsa hepsi",
             "sayfa": "solda Cemal'in kalıbı (şablon mumları + bant), sağda bölge (öncesi 15 mum, bölge kutulu, bölge sonunda kesik), Bollinger 20 + "
                      "SMA20, hisse / tarih yok, altta ✓ benziyor / ✗ benzemiyor kutusu",
             "esik": "Cemal 24'ün >= 19'una ✓ derse (%80) tespit GEÇERLİ; değilse ✗ sayfalarındaki ortak neden bir sonraki kapı (bu işte ölçülmez)"},
}

MV_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "v2 sentetik testinde negatif kontroller (n1 / n2 / n3 aynı gidiş farklı mum yapısı) ve rastgele seri tabanı SAYIYLA; v1 ile yan yana; "
                   "getiri / eş bu işte yok (bölge sayımı)"),
    "K2": ("EVET", "kapı ölçüleri ve S pencere içi, t'ye kadarki barlar (MI.mi_bant / mi_ozellik); mv_prefix 30 olayda veri t'de kesilince kabul ve S "
                   "aynı (assert); veri <= 2022-12-31 + KASA kapısı"),
    "K3": ("EVET", "MI.mi_veri geçerli bar süzgeci; haftalıkta eksik hafta içeren pencere atılır (bağımsız denetçi bulgusu, v2'de kural)"),
    "K4": ("EVET", "aynı hissede 15 bar (günlük) / 15 hafta tekil (ilk kabul)"),
    "K5": ("UYGULANMAZ", "giriş / getiri hesaplanmaz (bölge sayımı ve görsel onay)"),
    "K6": ("EVET", "ölçüler ölçek bağımsız; EK ölçüler mum / bant oranı; TEZGAH2 bölünme düzeltmeli fiyat"),
    "K7": ("EVET", "evren bugün yaşayan hisseler; sayım bilgi; onay seti görsel (getiri yok)"),
    "K8": ("EVET", "sentetik 200 tohum / koşul; kabul ölçütü önceden; gerçek veride yalnız sayım (pazar x dönem)"),
    "K9": ("EVET", "MUM_IZI4_ON_KAYIT.md: KOD4_SHA, ESIK4_SHA, kapı eşik tablosu sha, sentetik sonuç sha, onay seçim tohumu; gerçek veri sayımından ÖNCE commit; "
                   "mv_kapi kontrol + sha + git"),
    "K10": ("EVET", "itiraz edilen bölge mum renk dizisiyle bulundu (15 / 15); onay PDF'i Cemal'in gözü (✓ / ✗) = görsel doğrulama"),
    "K11": ("EVET", "mv_tara_seri S'si kapısız durumda MI.mi_tara_seri ile birebir (test); 2 hücre sayımı olay dosyasından düz pandas"),
    "K12": ("EVET", "v1 sonuçları 'v1 dedektörünün bölgeleri için' diye yazılır; kalıp için hüküm yok (ÖLÇÜLEMEDİ); 'iz' sözü yok"),
    "K13": ("EVET", "çakışma kapısı; v1 dosyaları / defterler / UC_IZ2 değişmez; yalnız kendi yolları git add"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


# ================================================================ 0) YARDIMCI
def _mv_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or MV_YOL["cikti"], MV_DOSYA[ad])


def mv_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or MV_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def mv_ek_olcu(O, H, L, C, BU, BA) -> Dict[str, np.ndarray]:
    O, H, L, C, BU, BA = [np.atleast_2d(np.asarray(v, float)) for v in (O, H, L, C, BU, BA)]
    gen = np.maximum(BU - BA, 1e-12)
    r = (H - L) / gen; g = np.abs(C - O) / gen
    return {"mum_bant": r.mean(1), "govde_bant": g.mean(1), "max_mum_bant": r.max(1), "max_govde_bant": g.max(1)}


def mv_pct(dagilim: np.ndarray, v) -> np.ndarray:
    x = np.sort(np.asarray(dagilim, float)); v = np.asarray(v, float)
    lo = np.searchsorted(x, v, "left"); hi = np.searchsorted(x, v, "right")
    return (lo + 0.5 * (hi - lo)) / len(x)


def mv_sablon() -> Dict[str, Dict[str, Any]]:
    """MUM_IZI şablonları (kalibre) + EK ölçüler (görüntü bantlarıyla)."""
    sab = MI.mi_sablon_yukle()
    for ad, s in sab.items():
        a = s["ohlc"]
        s["EK"] = {k: float(v[0]) for k, v in mv_ek_olcu(a["O"], a["H"], a["L"], a["C"], a["BU"], a["BA"]).items()}
    return sab


# ================================================================ 1) VERİ ve DAĞILIM
def mv_haftalik_panel(V: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """MH.mh_haftalik + eksik hafta bayrağı ('bosluk' = önceki haftayla arada boş ISO haftası var)."""
    out = {}
    for s, d in V.items():
        W = MH.mh_haftalik(d, MH.MH_KESIK)
        if len(W) < 40:
            continue
        pz = pd.DatetimeIndex(W.bas)
        hno = ((pz - pd.to_timedelta(pz.dayofweek, unit="D")).normalize().values.astype("datetime64[D]").astype(np.int64)) // 7
        W = W.copy(); W["bosluk"] = np.r_[False, np.diff(hno) > 1]
        out[s] = W
    return out


def mv_veri(zaman: str, pazar: str) -> Dict[str, pd.DataFrame]:
    if zaman == "gunluk":
        V = MI.mi_veri(pazar, MV_YOL["gunluk"])["V"]
        return {s: d for s, d in V.items() if len(d) >= 40}
    V = MI.mi_veri(pazar, MV_YOL["haftalik"])["V"]
    return mv_haftalik_panel(V)


def _mv_pencere(d: pd.DataFrame, e: np.ndarray, L: int) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray], np.ndarray]:
    O, H, Lw, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    BU, BO, BA = MI.mi_bant(C)
    idx = (e - L + 1)[:, None] + np.arange(L)[None, :]
    F = MI.mi_ozellik(O[idx], H[idx], Lw[idx], C[idx], BU[idx], BO[idx], BA[idx])
    EK = mv_ek_olcu(O[idx], H[idx], Lw[idx], C[idx], BU[idx], BA[idx])
    return F, EK, idx


def mv_gecerli_uclar(d: pd.DataFrame, L: int, uclar: List[str]) -> np.ndarray:
    ix = d.index; e = np.flatnonzero((ix >= pd.Timestamp(uclar[0])) & (ix <= pd.Timestamp(uclar[1]))); e = e[e - L + 1 >= 19]
    if "bosluk" in d.columns and len(e):
        b = np.r_[0, np.cumsum(d.bosluk.to_numpy(bool))]
        e = e[(b[e + 1] - b[e - L + 2]) == 0]          # pencerenin 2..L. barında boşluk yok
    return e


def mv_dagilim(zaman: str, V: Dict[str, Dict[str, pd.DataFrame]]) -> Dict[int, pd.DataFrame]:
    G = MV_ESIK["dagilim"]; Z = G[zaman]; out = {}
    for L in G["L"]:
        anah, say, uc = [], [], []
        for p in ("ABD", "AVR", "BIST"):
            for s in sorted(V[p]):
                e = mv_gecerli_uclar(V[p][s], L, Z["uclar"]); anah.append((p, s)); say.append(len(e)); uc.append(e)
        say = np.array(say); top = int(say.sum()); rng = np.random.default_rng(int(Z["tohum"]) + L)
        g = np.sort(rng.choice(top, size=min(G["n"], top), replace=False)); sinir = np.r_[0, np.cumsum(say)]
        h = np.searchsorted(sinir, g, side="right") - 1; parca = []
        for hh in np.unique(h):
            p, s = anah[hh]; e = uc[hh][g[h == hh] - sinir[hh]]
            F, EK, _ = _mv_pencere(V[p][s], e, L)
            parca.append(pd.DataFrame({**F, **EK, "pazar": p}))
        out[L] = pd.concat(parca, ignore_index=True); out[L].attrs["havuz"] = top
        mvlog.info("dağılım %s L %d: havuz %d", zaman, L, top)
    return out


def mv_kapi_esik(D: Dict[str, Dict[int, pd.DataFrame]], sab: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Kapı eşik tablosu: zaman x şablon x L x ölçü (MV_ESIK['kapilar']['esik'])."""
    K = MV_ESIK["kapilar"]; out: Dict[str, Any] = {}
    for zaman, DL in D.items():
        out[zaman] = {}
        for ad, s in sab.items():
            out[zaman][ad] = {}
            for L in s["uzunluklar"]:
                q = {}
                for kk in ("k1", "k2", "k3", "k4", "k5", "k7"):
                    for olc, yon in K[kk]["olcu"]:
                        x = DL[L][olc].to_numpy()
                        q[olc] = float(min(np.quantile(x, 0.75), s["F"][olc])) if yon == "Y" else float(max(np.quantile(x, 0.25), s["F"][olc]))
                for olc, kat in K["k4"]["ek"]:
                    q[olc] = float(s["EK"][olc] * kat)
                out[zaman][ad][str(L)] = q
    return out


def mv_kapilar(F: Dict[str, np.ndarray], EK: Dict[str, np.ndarray], q: Dict[str, float]) -> Dict[str, np.ndarray]:
    K = MV_ESIK["kapilar"]; out = {}
    for kk in ("k1", "k2", "k3", "k4", "k5", "k6", "k7"):
        ok = None
        for olc, yon in K[kk].get("olcu", []):
            c = (F[olc] >= q[olc] - 1e-12) if yon == "Y" else (F[olc] <= q[olc] + 1e-12)
            ok = c if ok is None else ok & c
        for olc, kat in K[kk].get("ek", []):
            c = EK[olc] <= q[olc] + 1e-12; ok = c if ok is None else ok & c
        for olc, op, v in K[kk].get("ham", []):
            c = (F[olc] <= v) if op == "<=" else (F[olc] >= v); ok = c if ok is None else ok & c
        out[kk] = ok
    return out


# ================================================================ 2) TARAMA (v1 S + kapılar)
def mv_tara_seri(O, H, L, C, sab: Dict[str, Any], qL: Optional[Dict[str, Dict[str, float]]], bosluk: Optional[np.ndarray] = None
                 ) -> Dict[str, np.ndarray]:
    """Her pencere sonu e: v1 en iyi S (MI.mi_tara_seri ile aynı), v2 kabul (S >= eşik ve 7 kapı aynı pencerede), v2 kabul edilen en iyi S ve m.
    qL None ise yalnız v1."""
    O, H, L, C = (np.asarray(v, float) for v in (O, H, L, C)); T = len(C); nb = int(MI.MI_ESIK["benzerlik"]["bant"]["n"])
    BU, BO, BA = MI.mi_bant(C, nb, float(MI.MI_ESIK["benzerlik"]["bant"]["k"]))
    v1 = np.full(T, np.nan); v1m = np.zeros(T, np.int64); v2 = np.full(T, np.nan); v2m = np.zeros(T, np.int64); s0 = nb - 1
    bc = np.r_[0, np.cumsum(bosluk.astype(np.int64))] if bosluk is not None else None
    for m in sab["uzunluklar"]:
        if T - s0 < m:
            continue
        W = [_swv4(x[s0:], m) for x in (O, H, L, C, BU, BO, BA)]
        F = MI.mi_ozellik(*W); Z, pB = MI.mi_dizi(W[0], W[1], W[2], W[3], W[4], W[6], sab["L"])
        S = MI.mi_S_bilesen(*MI.mi_mesafe(Z, pB, F, sab), sab["tau"])
        e = np.arange(s0 + m - 1, T)
        if bc is not None:
            okb = (bc[e + 1] - bc[e - m + 2]) == 0
            S = np.where(okb, S, np.nan)
        iyi = ~(S <= v1[e]); v1[e[iyi]] = S[iyi]; v1m[e[iyi]] = m
        if qL is not None:
            EK = mv_ek_olcu(W[0], W[1], W[2], W[3], W[4], W[6])
            kp = mv_kapilar(F, EK, qL[str(m)])
            ok = np.nan_to_num(S, nan=-1) >= sab["esik"]
            for v in kp.values():
                ok &= v
            S2 = np.where(ok, S, np.nan); iy = ~(S2 <= v2[e]) & np.isfinite(S2)
            v2[e[iy]] = S2[iy]; v2m[e[iy]] = m
    return {"v1": v1, "v1m": v1m, "v2": v2, "v2m": v2m}


def mv_olay(R: Dict[str, np.ndarray], esik: float, tekil: int = 15) -> Dict[str, np.ndarray]:
    e1 = np.flatnonzero(np.nan_to_num(R["v1"], nan=-1) >= esik); e2 = np.flatnonzero(np.isfinite(R["v2"]))
    return {"v1": MI._mi_tekil(e1, tekil) if len(e1) else e1, "v2": MI._mi_tekil(e2, tekil) if len(e2) else e2}


# ================================================================ 3) FARK (A1-A4)
def mv_sd20(sab: Dict[str, Dict[str, Any]], havuz: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    """Şablonun sentetik %20 gürültü sd'si: kök A, gürültü 0,2 gömülü gerçek pencereler (MI._mi_sentetik_seri ile AYNI tohumlar); 35 ölçü + EK."""
    Sn = MI.MI_ESIK["sentetik"]; kok = Sn["kok"]["A"]; nb = 20; out = {}
    for si, (ad, s) in enumerate(sab.items()):
        rows = []
        for ui, ur in enumerate(Sn["uretec"]):
            for bi, bg in enumerate(Sn["baglam"]):
                for t in range(int(Sn["tohum"])):
                    rng = np.random.default_rng([int(kok), si, ui, bi, 20, t])
                    X = MI._mi_sentetik_seri(rng, havuz, s, ur, bg, 0.2)
                    BU, BO, BA = MI.mi_bant(X["C"], nb); sl = slice(X["p"], X["e"] + 1)
                    F = MI.mi_ozellik(X["O"][sl], X["H"][sl], X["L"][sl], X["C"][sl], BU[sl], BO[sl], BA[sl])
                    EK = mv_ek_olcu(X["O"][sl], X["H"][sl], X["L"][sl], X["C"][sl], BU[sl], BA[sl])
                    rows.append({**{k: float(v[0]) for k, v in F.items()}, **{k: float(v[0]) for k, v in EK.items()}})
        R = pd.DataFrame(rows); out[ad] = {k: float(R[k].std()) for k in R.columns}
    return out


def mv_karsi_ornek(s: Dict[str, Any]) -> Dict[str, Dict[str, np.ndarray]]:
    a = s["ohlc"]; O, H, L, C, BU, BO, BA = (np.asarray(a[c], float) for c in ("O", "H", "L", "C", "BU", "BO", "BA"))
    u = float((H - L).mean()); Cp = np.r_[O[0], C[:-1]]
    yon = np.where(C >= Cp, 1.0, -1.0)
    out = {}
    O1 = C - yon * u; out["n1"] = {"O": O1, "H": np.maximum(O1, C), "L": np.minimum(O1, C), "C": C.copy()}
    ust = H - np.maximum(O, C); alt = np.minimum(O, C) - L
    out["n2"] = {"O": O.copy(), "H": np.maximum(O, C) + alt, "L": np.minimum(O, C) - ust, "C": C.copy()}
    out["n3"] = {"O": C + 2 * (O - C), "H": C + 2 * (H - C), "L": C + 2 * (L - C), "C": C.copy()}
    for ad, Cn in (("p1", np.full(len(C), C[0])), ("p1b", C[0] - (C - C[0]))):
        out[ad] = {"O": Cn + (O - C), "H": Cn + (H - C), "L": Cn + (L - C), "C": Cn}
    for v in out.values():
        v.update({"BU": BU, "BO": BO, "BA": BA})
    return out


def mv_S_bilesen(s: Dict[str, Any], X: Dict[str, np.ndarray]) -> Dict[str, float]:
    F = MI.mi_ozellik(X["O"], X["H"], X["L"], X["C"], X["BU"], X["BO"], X["BA"])
    Z, pB = MI.mi_dizi(X["O"], X["H"], X["L"], X["C"], X["BU"], X["BA"], s["L"])
    D1, D2, D3 = MI.mi_mesafe(Z, pB, F, s)
    t = s["tau"]
    return {"S": float(MI.mi_S_bilesen(D1, D2, D3, t)[0]), "dizi": float(D1[0] / t[0]), "bant": float(D2[0] / t[1]), "oz": float(D3[0] / t[2])}


def mv_fark(cikti: Optional[str] = None) -> Dict[str, Any]:
    """A1-A4 + dağılımlar + kapı eşikleri (getirisiz)."""
    t0 = time.time(); cikti = cikti or MV_YOL["cikti"]; os.makedirs(MV_YOL["gecici"], exist_ok=True)
    sab = mv_sablon(); havuz = pd.read_pickle(os.path.join(MI.MI_YOL["gecici"], MI.MI_DOSYA["havuz"]))
    sd = mv_sd20(sab, havuz)
    oz = [k for k, _, _ in MI.MI_OZELLIK]; ek = list(MV_ESIK["ek_olcu"])[:4]
    J: Dict[str, Any] = {"surum": MV_SURUM, "zaman": MI._mi_simdi(), "sd20": sd, "sablon_EK": {ad: s["EK"] for ad, s in sab.items()}}
    V = {z: {p: mv_veri(z, p) for p in ("ABD", "AVR", "BIST")} for z in ("gunluk", "haftalik")}
    D = {z: mv_dagilim(z, V[z]) for z in ("gunluk", "haftalik")}
    for z in D:
        for L, x in D[z].items():
            x.to_pickle(os.path.join(MV_YOL["gecici"], f"dagilim_{z}_L{L}.pkl"))
    Q = mv_kapi_esik(D, sab)
    MI._mi_jyaz(_mv_yol("esikler", cikti), Q, "kapı eşik")
    # şablonun kendi kapıları (her zaman dilimi, L = şablon L)
    J["sablon_kapi"] = {z: {ad: {k: bool(v[0]) for k, v in mv_kapilar({k: np.array([x]) for k, x in s["F"].items()},
                                                                       {k: np.array([x]) for k, x in s["EK"].items()}, Q[z][ad][str(s["L"])]).items()}
                            for ad, s in sab.items()} for z in Q}
    # p1 (şablon yüzdeliği, günlük L 20 ve haftalık L 20)
    pt = {z: {k: float(mv_pct(D[z][20][k].to_numpy(), sab["tam"]["F"][k] if k in sab["tam"]["F"] else sab["tam"]["EK"][k])[()]) for k in oz + ek} for z in D}
    J["sablon_yuzdelik"] = pt
    K2 = pd.read_csv(os.path.join(MV_YOL["cikti"], "mum_izi2_karsilastirma.csv"))      # MUM_IZI2 p1 (iz 1, günlük L 20 dağılımı)
    ayirt = {r.olcu: ("Y" if r.p1 >= 0.5 else "D") for r in K2.itertuples() if r.p1 >= 0.90 or r.p1 <= 0.10}
    J["ayirt_edici"] = ayirt
    # A1: itiraz edilen bölge (MUM_IZI3_HAFTALIK.pdf sayfa 3 = ABD NEE, bölge sonu 2007-11-02, 16 hafta; renk dizisiyle bulundu)
    A1 = mv_a1(V, sab, sd, pt)
    J["A1"] = A1["ozet"]
    # A2: bütün v1 eşleşmeleri (tam): günlük 2016-22 ve haftalık (eşik listesi)
    A2, A2t = mv_a2(V, sab, sd, D, ayirt)
    J["A2"] = A2
    # A4: karşı örnekler
    J["A4"] = {ad: {k: mv_S_bilesen(s, X) for k, X in mv_karsi_ornek(s).items()} for ad, s in sab.items()}
    J["A4"]["esik"] = {ad: s["esik"] for ad, s in sab.items()}
    # (5) ilk eşik haftası vs kümenin en iyi S'si (haftalık)
    J["kume_S"] = A2t.pop("kume_S", None)
    tab = A1["tablo"]
    tab.to_csv(_mv_yol("fark", cikti), index=False, float_format="%.5f")
    J["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_mv_yol("fark_json", cikti), J, "fark")
    mvlog.info("fark bitti (%.0f sn)", time.time() - t0)
    return J


def mv_a1(V, sab, sd, pt) -> Dict[str, Any]:
    s = sab["tam"]; W = V["haftalik"]["ABD"]["NEE"]; t = W.index.get_loc(pd.Timestamp("2007-11-02")); m = 16
    e = np.array([t]); F, EK, idx = _mv_pencere(W, e, m)
    renk = "".join("G" if c >= o else "R" for o, c in zip(W.Open.to_numpy()[idx[0]], W.Close.to_numpy()[idx[0]]))
    O, H, Lw, C = (W[c].to_numpy(float)[idx[0]] for c in ("Open", "High", "Low", "Close")); BU, BO, BA = (x[idx[0]] for x in MI.mi_bant(W.Close.to_numpy(float)))
    Sb = mv_S_bilesen(s, {"O": O, "H": H, "L": Lw, "C": C, "BU": BU, "BO": BO, "BA": BA})
    rows = []
    for k, acik, grup in MI.MI_OZELLIK:
        v = float(F[k][0]); f = (v - s["F"][k]) / max(sd["tam"][k], 1e-9)
        rows.append({"olcu": k, "aciklama": acik, "sablon": s["F"][k], "olay": v, "fark_sd": f, "uyum": "UYUYOR" if abs(f) <= 1 else "UYMUYOR"})
    for k in list(MV_ESIK["ek_olcu"])[:4]:
        v = float(EK[k][0]); f = (v - s["EK"][k]) / max(sd["tam"][k], 1e-9)
        rows.append({"olcu": k, "aciklama": MV_ESIK["ek_olcu"][k], "sablon": s["EK"][k], "olay": v, "fark_sd": f, "uyum": "UYUYOR" if abs(f) <= 1 else "UYMUYOR"})
    T = pd.DataFrame(rows)
    return {"tablo": T, "ozet": {"sayfa": "MUM_IZI3_HAFTALIK.pdf sayfa 3 (ayri_ABD, en yüksek S)", "pazar": "ABD", "sembol": "NEE", "bolge_bas": str(W.bas.iloc[idx[0][0]].date()),
                                 "bolge_son": "2007-11-02", "m": m, "renk": renk, "S_bilesen": Sb, "uyuyor": int((T.uyum == "UYUYOR").sum()), "olcu": int(len(T)),
                                 "uymayan": T[T.uyum == "UYMUYOR"].olcu.tolist()}}


def mv_a2(V, sab, sd, D, ayirt) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    s = sab["tam"]; out: Dict[str, Any] = {}; ek = list(MV_ESIK["ek_olcu"])[:4]; ekst: Dict[str, Any] = {}
    O1 = pd.read_csv(MI._mi_yol("olay")); O1 = O1[O1.sablon == "tam"]
    O3 = pd.read_csv(MH._mh_yol("olay")); O3 = O3[(O3.sablon == "tam") & (O3.seviye == "ESIK")]
    kume = []
    for z, X in (("gunluk", O1), ("haftalik", O3)):
        for p in ("ABD", "AVR", "BIST"):
            x = X[X.pazar == p]; rows = []
            for sem, g in x.groupby("sembol"):
                d = V[z][p].get(sem)
                if d is None:
                    continue
                if z == "haftalik":
                    Rr = MI.mi_tara_seri(*(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), s)[0]
                for m, gg in g.groupby("m"):
                    e = np.array([d.index.get_loc(pd.Timestamp(tt)) for tt in gg.tarih]); F, EK, _ = _mv_pencere(d, e, int(m))
                    for i in range(len(e)):
                        rows.append({**{k: float(F[k][i]) for k in F}, **{k: float(EK[k][i]) for k in EK}})
                        if z == "haftalik":
                            w = Rr[e[i]:e[i] + 15]; j = int(np.nanargmax(w))
                            kume.append({"S_ilk": float(Rr[e[i]]), "S_kume_max": float(np.nanmax(w)), "gecikme": j})
            R = pd.DataFrame(rows)
            if not len(R):
                continue
            Dd = D[z][20]; r: Dict[str, Any] = {"n": int(len(R))}
            olc = {}
            for k in list(s["F"]) + ek:
                ref = s["F"][k] if k in s["F"] else s["EK"][k]
                olc[k] = {"medyan": float(R[k].median()), "sablon": float(ref), "uyuyor_pay": float((np.abs(R[k] - ref) <= sd["tam"][k]).mean())}
            r["olcu"] = olc
            r["en_cok_kacan"] = sorted(olc, key=lambda k: olc[k]["uyuyor_pay"])[:10]
            cnt = np.zeros(len(R), int); pay = {}
            for k, yon in ayirt.items():
                pk = mv_pct(Dd[k].to_numpy(), R[k].to_numpy())
                ok = (pk >= 0.75) if yon == "Y" else (pk <= 0.25); cnt += ok; pay[k] = float(ok.mean())
            r["ayirt_pay"] = pay; r["ayirt_say_dagilim"] = np.bincount(cnt, minlength=len(ayirt) + 1).tolist()
            r["hepsini_tasiyan_pay"] = float((cnt == len(ayirt)).mean()); r["ayirt_say_medyan"] = float(np.median(cnt))
            for k in ek:
                r[f"{k}_sablondan_buyuk_pay"] = float((R[k] > s["EK"][k]).mean())
            out[f"{z}|{p}"] = r
    if kume:
        K = pd.DataFrame(kume)
        ekst["kume_S"] = {"n": int(len(K)), "kume_max_sonra_pay": float((K.gecikme > 0).mean()), "S_ilk_med": float(K.S_ilk.median()),
                          "S_kume_max_med": float(K.S_kume_max.median()), "kume_max_ge_069_ilk_lt_069": float(((K.S_kume_max >= 0.69) & (K.S_ilk < 0.69)).mean()),
                          "kume_max_ge_069": int((K.S_kume_max >= 0.69).sum())}
    return out, ekst


# ================================================================ 4) SENTETİK v2 (C2)
def _mv_sablon_var(s: Dict[str, Any], X: Dict[str, np.ndarray]) -> Dict[str, Any]:
    s2 = dict(s); s2["ohlc"] = {**s["ohlc"], **{k: X[k] for k in ("O", "H", "L", "C")}}
    return s2


def mv_sentetik(cikti: Optional[str] = None, tohum: Optional[int] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or MV_YOL["cikti"]; Sn = MV_ESIK["sentetik"]; T = int(tohum or Sn["tohum"])
    sab = mv_sablon(); Q = json.load(open(_mv_yol("esikler", cikti), encoding="utf-8"))["gunluk"]
    havuz = pd.read_pickle(os.path.join(MI.MI_YOL["gecici"], MI.MI_DOSYA["havuz"])); tol = 3
    out: Dict[str, Any] = {"surum": MV_SURUM, "tohum": T}
    for si, (ad, s) in enumerate(sab.items()):
        kar = mv_karsi_ornek(s); res = {}
        for tur in ["poz"] + Sn["negatif"]:
            sv = s if tur == "poz" else _mv_sablon_var(s, kar[tur]); sat = []
            for ui, ur in enumerate(Sn["uretec"]):
                for bi, bg in enumerate(Sn["baglam"]):
                    for gr in Sn["gurultu"]:
                        for t in range(T):
                            rng = np.random.default_rng([int(Sn["kok"]), si, ["poz", "n1", "n2", "n3"].index(tur), ui, bi, int(round(gr * 100)), t])
                            X = MI._mi_sentetik_seri(rng, havuz, sv, ur, bg, float(gr))
                            R = mv_tara_seri(X["O"], X["H"], X["L"], X["C"], s, Q[ad])
                            a, b = max(0, X["e"] - tol), X["e"] + tol + 1
                            v1 = bool((np.nan_to_num(R["v1"][a:b], nan=-1) >= s["esik"]).any()); v2 = bool(np.isfinite(R["v2"][a:b]).any())
                            sat.append({"uretec": ur, "baglam": bg, "gurultu": gr, "v1": v1, "v2": v2})
            Dd = pd.DataFrame(sat)
            res[tur] = {"v1": float(Dd.v1.mean()), "v2": float(Dd.v2.mean()), "n": int(len(Dd)),
                        "gurultu": {f"{g:.1f}": {"v1": float(x.v1.mean()), "v2": float(x.v2.mean())} for g, x in Dd.groupby("gurultu")},
                        "baglam": {b_: {"v1": float(x.v1.mean()), "v2": float(x.v2.mean())} for b_, x in Dd.groupby("baglam")}}
            mvlog.info("sentetik %s %s: v1 %.3f v2 %.3f", ad, tur, res[tur]["v1"], res[tur]["v2"])
        ry = {}
        for ui, ur in enumerate(Sn["uretec"]):
            n = 0; k1 = 0; k2 = 0
            for t in range(int(Sn["yanlis_seri"])):
                rng = np.random.default_rng([int(Sn["kok"]), 99, si, ui, t])
                lO, lH, lL, lC = MI.mi_uret(rng, int(Sn["yanlis_n"]) + 60, havuz, ur)
                R = mv_tara_seri(np.exp(lO), np.exp(lH), np.exp(lL), np.exp(lC), s, Q[ad])
                n += int(np.isfinite(R["v1"]).sum()); ol = mv_olay(R, s["esik"]); k1 += len(ol["v1"]); k2 += len(ol["v2"])
            ry[ur] = {"v1_1000": 1000.0 * k1 / n, "v2_1000": 1000.0 * k2 / n, "oran": (k2 / k1) if k1 else None}
        res["rastgele"] = ry
        res["olcut"] = {"negatif_le_5": {tur: bool(res[tur]["v2"] <= 0.05) for tur in Sn["negatif"]},
                        "rastgele_le_1_5": {ur: bool(ry[ur]["v2_1000"] <= ry[ur]["v1_1000"] / 5) for ur in ry}}
        res["olcut"]["gecti"] = all(res["olcut"]["negatif_le_5"].values()) and all(res["olcut"]["rastgele_le_1_5"].values())
        out[ad] = res
    out["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_mv_yol("sentetik", cikti), out, "sentetik v2")
    return out


# ================================================================ 5) KAPI ve ÖN KAYIT
def mv_sha_simdi(cikti: Optional[str] = None) -> Dict[str, str]:
    return {"KOD4_SHA": MI._mi_sha(MV_YOL["kod"]), "ESIK4_SHA": mv_esik_sha(), "KAPI_ESIK_SHA": MI._mi_sha(_mv_yol("esikler", cikti)),
            "SENTETIK4_SHA": MI._mi_sha(_mv_yol("sentetik", cikti)), "MI_KOD_SHA": MI._mi_sha(MI.MI_YOL["kod"]), "MH_KOD_SHA": MI._mi_sha(MH.MH_YOL["kod"])}


def mv_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or MV_YOL["cikti"]; yol = _mv_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise MVHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = mv_sha_simdi(cikti)
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise MVHata(f"ön kayıt kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_MV)
    c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise MVHata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_V2.py", "MUM_IZI.py", "MUM_IZI_HAFTALIK.py",
                   os.path.relpath(_mv_yol("esikler", cikti), KOK_MV), os.path.relpath(_mv_yol("sentetik", cikti), KOK_MV)]):
        raise MVHata("ön kayıt / kod / eşik / sentetik çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def mv_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or MV_YOL["cikti"]; y = _mv_yol("onkayit", cikti)
    if os.path.exists(y):
        raise MVHata("ön kayıt zaten var")
    sh = mv_sha_simdi(cikti); SJ = json.load(open(_mv_yol("sentetik", cikti), encoding="utf-8")); FJ = json.load(open(_mv_yol("fark_json", cikti), encoding="utf-8"))
    Q = json.load(open(_mv_yol("esikler", cikti), encoding="utf-8"))
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"] +
                   [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in MV_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_V2.py"])
    s = [f"# MUM_IZI4 ÖN KAYIT ({MI._mi_simdi()})", "",
         "v2 tanımı (kapılar, eşik tablosu, sentetik sonuç, onay seçim kuralı) gerçek veride v2 BÖLGE SAYIMINDAN ÖNCE commit edilir (`mv_kapi`). Bu işte "
         "getiri / sonrası hesaplanmaz. Kapılar şablondan ve getirisiz açık veri ölçü dağılımından türetildi; v1 eşleşmelerinin getirisine bakılmadı.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_V2.py commit'i: {kc or 'yok'}", "",
         "## Kapılar ve eşikler (MV_ESIK; sha yukarıda)", "", "```", json.dumps(MV_ESIK, ensure_ascii=False, indent=1), "```", "",
         f"Şablonun kendi kapıları: {FJ['sablon_kapi']}", "", "Kapı eşik tablosu (tam, günlük, L 20): " + json.dumps(Q["gunluk"]["tam"]["20"], ensure_ascii=False), "",
         "## Sentetik v2 testi (C2; gerçek veriden önce)", ""]
    for a_ in ("tam", "tepesiz"):
        r = SJ[a_]
        s.append(f"- {a_}: yakalama v1 {r['poz']['v1']:.3f} -> v2 {r['poz']['v2']:.3f}; n1 {r['n1']['v1']:.3f} -> {r['n1']['v2']:.3f}; n2 {r['n2']['v1']:.3f} -> "
                 f"{r['n2']['v2']:.3f}; n3 {r['n3']['v1']:.3f} -> {r['n3']['v2']:.3f}; rastgele 1.000 bar v1 / v2: blok {r['rastgele']['blok']['v1_1000']:.2f} / "
                 f"{r['rastgele']['blok']['v2_1000']:.3f}, ry {r['rastgele']['ry']['v1_1000']:.2f} / {r['rastgele']['ry']['v2_1000']:.3f}; KABUL ÖLÇÜTÜ "
                 f"{'GEÇTİ' if r['olcut']['gecti'] else 'GEÇMEDİ'} {r['olcut']}")
    s += ["", "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 4")


# ================================================================ 6) GERÇEK VERİDE SAYIM (C3)
_MV_ISCI: Dict[str, Any] = {}


def _mv_isci(s: str) -> Tuple[str, List[Dict[str, Any]], Dict[str, int]]:
    d = _MV_ISCI["V"][s]; sab = _MV_ISCI["sab"]; Q = _MV_ISCI["Q"]; uc = _MV_ISCI["uclar"]
    ix = d.index; ara = (ix >= pd.Timestamp(uc[0])) & (ix <= pd.Timestamp(uc[1])); ol = []; nb = {}
    for ad, s_ in sab.items():
        R = mv_tara_seri(*(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), s_, Q[ad], d.bosluk.to_numpy(bool) if "bosluk" in d.columns else None)
        for k in ("v1", "v2"):
            R[k] = np.where(ara, R[k], np.nan)
        o = mv_olay(R, s_["esik"])
        nb[ad] = int(np.isfinite(R["v1"]).sum())
        for k in ("v1", "v2"):
            for t in o[k]:
                mm = int(R[f"{k}m"][t])
                ol.append({"surum": k, "sablon": ad, "sembol": s, "tarih": ix[t], "S": float(R[k][t]), "m": mm, "bar_no": int(t)})
    return s, ol, nb


def mv_say_pazar(V: Dict[str, pd.DataFrame], sab, Q, uclar, islem: int = 3) -> Tuple[pd.DataFrame, Dict[str, int]]:
    import multiprocessing as mp
    _MV_ISCI.clear(); _MV_ISCI.update({"V": V, "sab": sab, "Q": Q, "uclar": uclar}); semb = sorted(V)
    try:
        with mp.get_context("fork").Pool(islem) as pool:
            R = list(pool.imap(_mv_isci, semb, chunksize=16))
    finally:
        _MV_ISCI.clear()
    X = pd.DataFrame([r for _, o, _ in R for r in o]); nb = {ad: int(sum(x[ad] for _, _, x in R)) for ad in sab}
    return X, nb


def mv_prefix(V: Dict[str, pd.DataFrame], X: pd.DataFrame, sab, Q, n: int = 30) -> Dict[str, Any]:
    x = X[X.surum == "v2"]
    if not len(x):
        return {"n": 0, "tuttu": True}
    rng = np.random.default_rng(2530); sec = x.iloc[rng.choice(len(x), size=min(n, len(x)), replace=False)]; mx = 0.0
    for r in sec.itertuples():
        d = V[r.sembol]; dk = d[d.index <= r.tarih]
        R = mv_tara_seri(*(dk[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), sab[r.sablon], Q[r.sablon],
                         dk.bosluk.to_numpy(bool) if "bosluk" in dk.columns else None)
        if not np.isfinite(R["v2"][-1]):
            raise MVHata("PREFIX: kabul kayboldu")
        mx = max(mx, abs(float(R["v2"][-1]) - float(r.S)))
    if not mx < 1e-12:
        raise MVHata(f"PREFIX TUTMADI {mx}")
    return {"n": int(len(sec)), "en_buyuk_fark": mx, "tuttu": True}


def mv_say(cikti: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    t0 = time.time(); cikti = cikti or MV_YOL["cikti"]
    if os.path.exists(_mv_yol("sonuc", cikti)):
        raise MVHata("sonuç zaten var")
    G0 = mv_kapi(cikti)
    kasa = KS.kasa_kapisi([os.path.join(MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] +
                          [os.path.join(MV_YOL["haftalik"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")], "2022-12-31")
    sab = mv_sablon(); Qa = json.load(open(_mv_yol("esikler", cikti), encoding="utf-8"))
    J: Dict[str, Any] = {"surum": MV_SURUM, "kapi": G0, "kasa": kasa, "sayim": {}, "prefix": {}, "bar": {}}
    parca = []
    for z in ("gunluk", "haftalik"):
        Dn = MV_ESIK["say"][z]["donem"]; uc = [min(v[0] for v in Dn.values()), max(v[1] for v in Dn.values())]
        for p in ("ABD", "AVR", "BIST"):
            V = mv_veri(z, p)
            X, nb = mv_say_pazar(V, sab, Qa[z], uc); J["bar"][f"{z}|{p}"] = nb
            if not len(X):
                continue
            J["prefix"][f"{z}|{p}"] = mv_prefix(V, X, sab, Qa[z])
            X["zaman"] = z; X["pazar"] = p
            X["donem"] = "dis"
            for h, (a, b) in Dn.items():
                X.loc[(X.tarih >= pd.Timestamp(a)) & (X.tarih <= pd.Timestamp(b)), "donem"] = h
            # P2 (ABD / AVR): giriş günü; günlük -> MUM_IZI açık kopya; haftalık -> dönem parçası (p1 2000-16, p2 2015-22)
            X["evren_ici"] = True
            if p in ("ABD", "AVR"):
                if z == "gunluk":
                    X["evren_ici"] = MH.mh_p2(X, p, MV_YOL["gunluk"])
                else:
                    ev = np.ones(len(X), bool); i1 = X.donem.isin(["h0107", "h0815"]).to_numpy()
                    if i1.any():
                        ev[i1] = MH.mh_p2(X[i1], p, MH.MH_YOL["p1"])
                    if (~i1).any():
                        ev[~i1] = MH.mh_p2(X[~i1], p, MH.MH_YOL["p2"])
                    X["evren_ici"] = ev
            parca.append(X); del V; gc.collect()
            mvlog.info("%s %s: v1 %d, v2 %d olay (%.0f sn)", z, p, int((X.surum == "v1").sum()), int((X.surum == "v2").sum()), time.time() - t0)
    O = pd.concat(parca, ignore_index=True)
    for (z, p, ad, h), g in O.groupby(["zaman", "pazar", "sablon", "donem"]):
        v1 = g[g.surum == "v1"]; v2 = g[g.surum == "v2"]
        J["sayim"][f"{z}|{p}|{ad}|{h}"] = {"v1": int(len(v1)), "v2": int(len(v2)), "v1_evren": int(v1.evren_ici.sum()), "v2_evren": int(v2.evren_ici.sum()),
                                            "oran": (len(v2) / len(v1)) if len(v1) else None,
                                            "oran_evren": (int(v2.evren_ici.sum()) / int(v1.evren_ici.sum())) if v1.evren_ici.sum() else None}
    O2 = O.copy(); O2["tarih"] = pd.to_datetime(O2.tarih).dt.strftime("%Y-%m-%d")
    O2.to_csv(os.path.join(MV_YOL["gecici"], "v2_olay.csv.gz"), index=False)
    J["olay_sha"] = MI._mi_sha(os.path.join(MV_YOL["gecici"], "v2_olay.csv.gz"))
    J["en_gec"] = str(pd.to_datetime(O.tarih).max().date())
    if pd.Timestamp(J["en_gec"]) > MI.MI_KESIK:
        raise MVHata("KESİK AŞIMI")
    J["onay_secim"] = mv_onay_secim(O)
    J["yeniden"] = {k: {"duz_v2": int(((O.zaman == k.split("|")[0]) & (O.pazar == k.split("|")[1]) & (O.sablon == k.split("|")[2]) &
                                       (O.donem == k.split("|")[3]) & (O.surum == "v2")).sum()), "json_v2": J["sayim"][k]["v2"]}
                    for k in list(J["sayim"])[:2]}
    J["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_mv_yol("sonuc", cikti), J, "sonuç 4")
    return J


def mv_onay_secim(O: pd.DataFrame) -> List[Dict[str, Any]]:
    G = MV_ESIK["onay"]; rng = np.random.default_rng(G["tohum"]); sec = []; gor = set()
    for z in ("haftalik", "gunluk"):
        x = O[(O.surum == "v2") & (O.sablon == "tam") & (O.zaman == z) & O.evren_ici.astype(bool)].sort_values(["sembol", "tarih"])
        x = x[~x.sembol.isin(gor)].drop_duplicates("sembol")
        k = min(G[z], len(x))
        if k:
            ii = rng.choice(len(x), size=k, replace=False)
            for r in x.iloc[np.sort(ii)].itertuples():
                sec.append({"zaman": z, "pazar": r.pazar, "sembol": r.sembol, "tarih": str(pd.Timestamp(r.tarih).date()), "m": int(r.m), "S": float(r.S)})
                gor.add(r.sembol)
    p = rng.permutation(len(sec))
    return [dict(sec[i], sayfa=j + 3) for j, i in enumerate(p)]


# ================================================================ 7) ONAY PDF (C4) ve RAPOR
def _mv_ciz(ax, O, H, L, C, BU, BO, BA, kutu: Optional[Tuple[int, int]] = None, baslik: str = "") -> None:
    MI._mi_mum_ciz(ax, O, H, L, C, genislik=0.7)
    x = np.arange(len(C))
    ax.plot(x, BU, color="#9e8fd6", linewidth=1.3); ax.plot(x, BA, color="#9e8fd6", linewidth=1.3); ax.plot(x, BO, color="#7b3294", linestyle="--", linewidth=1)
    if kutu is not None:
        from matplotlib.patches import Rectangle
        a, b = kutu; lo = np.nanmin(L[a:b + 1]); hi = np.nanmax(H[a:b + 1])
        ax.add_patch(Rectangle((a - 0.5, lo), b - a + 1, hi - lo, facecolor="#ffb347", alpha=0.22, edgecolor="#ff7f00", linewidth=1.5))
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title(baslik, fontsize=11)


def mv_onay(cikti: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import Rectangle
    cikti = cikti or MV_YOL["cikti"]
    J = json.load(open(_mv_yol("sonuc", cikti), encoding="utf-8")); FJ = json.load(open(_mv_yol("fark_json", cikti), encoding="utf-8"))
    A1 = pd.read_csv(_mv_yol("fark", cikti)); sab = mv_sablon(); s = sab["tam"]; a = s["ohlc"]
    y = _mv_yol("onay", cikti); anah = []
    Vc: Dict[str, Any] = {}

    def kalip(ax, bas="Cemal'in kalıbı"):
        _mv_ciz(ax, a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, bas)

    with PdfPages(y, metadata={"Title": "MUM_IZI4 onay", "CreationDate": None, "ModDate": None}) as pdf:
        # s1 FARK
        fig = plt.figure(figsize=(8.3, 11.7))
        kalip(fig.add_axes([0.05, 0.62, 0.42, 0.3]), "Senin kalıbın (20 mum)")
        Vc[("haftalik", "ABD")] = mv_veri("haftalik", "ABD")
        W = Vc[("haftalik", "ABD")]["NEE"]; t = W.index.get_loc(pd.Timestamp("2007-11-02")); m = 16; i0 = t - m + 1 - 15
        BU, BO, BA = MI.mi_bant(W.Close.to_numpy(float)); sl = slice(i0, t + 1)
        _mv_ciz(fig.add_axes([0.53, 0.62, 0.42, 0.3]), *(W[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close")), BU[sl], BO[sl], BA[sl], (15, 15 + m - 1),
                "İtiraz ettiğin bölge (kod buldu)")
        ax = fig.add_axes([0.05, 0.18, 0.9, 0.4]); ax.axis("off")
        sec = [("mum_bant", "mum boyu / bant genişliği"), ("max_govde_bant", "en büyük gövde / bant"), ("govde_oran", "gövde / mum boyu"),
               ("doji_pay", "doji payı"), ("ust_fitil", "üst fitil / mum boyu"), ("uzun_ust_pay", "uzun üst fitilli mum payı"), ("alt_fitil", "alt fitil / mum boyu"),
               ("kucuk_mum_pay", "küçük mum payı"), ("ortusme", "mumlar birbirine biniyor"), ("pB_son", "son mumlarda üst banda yakınlık")]
        sat = []
        for k, ad in sec:
            r = A1[A1.olcu == k].iloc[0]
            sat.append([ad, f"{r.sablon:.2f}", f"{r.olay:.2f}", "evet" if r.uyum == "UYUYOR" else "HAYIR"])
        tb = ax.table(cellText=sat, colLabels=["ölçü", "senin kalıbın", "o bölge", "uyuyor mu"], loc="upper center", cellLoc="center", colWidths=[0.46, 0.18, 0.18, 0.18])
        tb.auto_set_font_size(False); tb.set_fontsize(11); tb.scale(1, 2.1)
        fig.text(0.05, 0.96, "FARK: aynı gidiş, farklı mum yapısı", fontsize=15, weight="bold")
        Sb = FJ["A1"]["S_bilesen"]
        fig.text(0.05, 0.13, f"Kod bu bölgeye S {Sb['S']:.2f} verdi: gidiş uzaklığı {Sb['dizi']:.2f}, bant yolu {Sb['bant']:.2f}, mum ölçüleri {Sb['oz']:.2f}\n"
                 "(1 = tipik rastgele pencere). Mum yapısı uzaktı ama gidiş yakın olduğu için ortalamada eşiği geçti.", fontsize=10, va="top")
        pdf.savefig(fig); plt.close(fig)
        # s2 HATA
        fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.05, 0.95, "HATALAR ve v2'nin değiştirdiği", fontsize=15, weight="bold")
        maddeler = [
            "1. Eşik yalnız 'kendi kalıbını bulma' ile seçildi; aynı gidişli ama farklı mumlu örnekler hiç sınanmadı.",
            "2. Kodun puanı gidiş + bant + mum ölçülerinin ortalaması: gidiş yakınsa mum farkını örtüyor.",
            "3. Mum boyu banda göre ölçülmedi (birim = bölgenin kendi mum boyu): büyük mumlu bölge küçük mumlu gibi göründü.",
            "4. 'Rastgele seride de aynı sıklıkta çıkıyor' sonucu 'kod ayırt edemiyor' demekti; 'kalıp sık' diye yorumlandı.",
            "5. Kodun bulduğu bölgeler sana gösterilmeden getiri ölçüldü ve 'iz değil' yazıldı.",
            "6. PDF'teki bölgeler 'tam uyan' sanıldı; çoğu eşiğin hemen üstündeydi (S 0,58-0,67).",
            "7. Haftalıkta kümenin ilk haftası alındı; en iyi hizalanan hafta değil.",
            "8. Haftalıkta eksik hafta içeren pencere atılmıyordu.",
        ]
        fig.text(0.05, 0.9, "\n\n".join(maddeler), fontsize=11, va="top", wrap=True)
        fig.text(0.05, 0.42, "v2: kodun eski puanı AYNEN + 7 ZORUNLU KAPI (hepsi aynı anda):\n"
                 "k1 uzun üst fitil  k2 kısa alt fitil  k3 küçük gövde / doji\nk4 küçük mum (banda göre de; en büyük gövde sınırlı)\n"
                 "k5 yükselen dipler  k6 alt banttan üst banda  k7 mumlar birbirine biniyor\n\n"
                 "Sonraki sayfalar: v2'nin bulduğu RASTGELE bölgeler (hisse / tarih yok, sonrası yok).\n"
                 "Her sayfada ✓ (benziyor) ya da ✗ (benzemiyor) işaretle. 24'ün 19'u ✓ ise tespit geçerli sayılır.", fontsize=11, va="top")
        pdf.savefig(fig); plt.close(fig)
        for r in sorted(J["onay_secim"], key=lambda r: r["sayfa"]):
            k = (r["zaman"], r["pazar"])
            if k not in Vc:
                Vc[k] = mv_veri(r["zaman"], r["pazar"])
            d = Vc[k][r["sembol"]]; t = d.index.get_loc(pd.Timestamp(r["tarih"])); m = int(r["m"]); i0 = max(0, t - m + 1 - MV_ESIK["onay"]["once"])
            BU, BO, BA = MI.mi_bant(d.Close.to_numpy(float)); sl = slice(i0, t + 1)
            fig = plt.figure(figsize=(8.3, 11.7))
            kalip(fig.add_axes([0.04, 0.6, 0.3, 0.28]), "Senin kalıbın")
            _mv_ciz(fig.add_axes([0.38, 0.45, 0.58, 0.45]), *(d[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close")), BU[sl], BO[sl], BA[sl],
                    (t - m + 1 - i0, t - i0), f"Sayfa {r['sayfa']}: bulunan bölge ({'haftalık' if r['zaman'] == 'haftalik' else 'günlük'} mum)")
            ax = fig.add_axes([0.1, 0.12, 0.8, 0.22]); ax.axis("off")
            for xx, txt in ((0.0, "✓  benziyor"), (0.55, "✗  benzemiyor")):
                ax.add_patch(Rectangle((xx, 0.1), 0.42, 0.8, fill=False, linewidth=3, transform=ax.transAxes))
                ax.text(xx + 0.21, 0.5, txt, ha="center", va="center", fontsize=22, transform=ax.transAxes)
            fig.text(0.04, 0.4, "Turuncu kutu = bölge; sağ kenar = bölgenin sonu (sonrası gösterilmiyor).\nMor = Bollinger 20 ve SMA20 (kesik).", fontsize=9)
            pdf.savefig(fig); plt.close(fig)
            anah.append(r)
    MI._mi_jyaz(_mv_yol("anahtar", cikti), {"not": "sayfa -> hisse / tarih; PDF'e girmez", "sayfalar": anah}, "anahtar")
    return y


def mv_rapor(cikti: Optional[str] = None) -> str:
    cikti = cikti or MV_YOL["cikti"]
    FJ = json.load(open(_mv_yol("fark_json", cikti), encoding="utf-8")); SJ = json.load(open(_mv_yol("sentetik", cikti), encoding="utf-8"))
    J = json.load(open(_mv_yol("sonuc", cikti), encoding="utf-8")); A1 = pd.read_csv(_mv_yol("fark", cikti))
    L = [f"# MUM_IZI4 RAPOR ({MI._mi_simdi()})", "", f"Sürüm: {MV_SURUM}", "", "## FARK", "", "### A1 itiraz edilen bölge", "",
         f"{FJ['A1']}", "", "| ölçü | şablon | olay | fark (sd) | sonuç |", "|---|---|---|---|---|"]
    for r in A1.itertuples():
        L.append(f"| {r.olcu} | {r.sablon:.3f} | {r.olay:.3f} | {r.fark_sd:+.2f} | {r.uyum} |")
    L += ["", "### A2 v1 eşleşmeleri", "", f"Ayırt edici ölçüler: {FJ['ayirt_edici']}", ""]
    for k, r in FJ["A2"].items():
        L.append(f"- {k}: n {r['n']}, ayırt edici ölçü sayısı medyan {r['ayirt_say_medyan']:.0f} / {len(FJ['ayirt_edici'])}, hepsini taşıyan %{100 * r['hepsini_tasiyan_pay']:.2f}; "
                 f"en çok kaçan {r['en_cok_kacan']}; ayırt edici payları {{{', '.join(f'{a}: %{100 * b:.0f}' for a, b in r['ayirt_pay'].items())}}}")
    L += ["", "### A3 mum / bant", ""]
    for k, r in FJ["A2"].items():
        L.append(f"- {k}: " + ", ".join(f"{e} medyan {r['olcu'][e]['medyan']:.3f} (şablon {r['olcu'][e]['sablon']:.3f}, şablondan büyük %{100 * r[e + '_sablondan_buyuk_pay']:.0f})"
                                       for e in ("mum_bant", "govde_bant", "max_mum_bant", "max_govde_bant")))
    L += ["", "### A4 karşı örnekler (şablon bantlarıyla)", "", f"{FJ['A4']}", "", f"Küme S (haftalık): {FJ.get('kume_S')}", "",
          "## v2 SENTETİK", "", f"{SJ}", "", "## v2 SAYIM", "", "| zaman | pazar | şablon | dönem | v1 | v2 | v2 / v1 | v1 evren | v2 evren | oran evren |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k, c in J["sayim"].items():
        z, p, ad, h = k.split("|")
        L.append(f"| {z} | {p} | {ad} | {h} | {c['v1']} | {c['v2']} | {MI._s(c['oran'], 4)} | {c['v1_evren']} | {c['v2_evren']} | {MI._s(c['oran_evren'], 4)} |")
    L += ["", f"Onay seti: {len(J['onay_secim'])} sayfa; tohum {MV_ESIK['onay']['tohum']}", f"Prefix: {J['prefix']}", f"Kapı: {J['kapi']}", f"KASA: {J['kasa']}", ""]
    return MI._mi_yaz(_mv_yol("rapor", cikti), "\n".join(L), "rapor 4")


# ================================================================ 8) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_mv(_once=_CK_ONCE_MV, _dosya="MUM_IZI_V2.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_MV",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_mv()


def _mv_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_V2")
    ap.add_argument("komut", choices=["fark", "sentetik", "onkayit", "say", "onay", "rapor"])
    ap.add_argument("--tohum", type=int, default=None)
    a = ap.parse_args(argv)
    try:
        if a.komut == "fark":
            J = mv_fark(); print(json.dumps(MI._mi_json({k: J[k] for k in ("A1", "ayirt_edici", "sablon_kapi", "A4", "kume_S")}), ensure_ascii=False)[:5000])
        elif a.komut == "sentetik":
            J = mv_sentetik(tohum=a.tohum); print(json.dumps(MI._mi_json(J), ensure_ascii=False)[:5000])
        elif a.komut == "onkayit":
            print(mv_onkayit_yaz())
        elif a.komut == "say":
            J = mv_say(); print(json.dumps(MI._mi_json({k: J[k] for k in ("sayim", "prefix")}), ensure_ascii=False)[:5000])
        elif a.komut == "onay":
            print(mv_onay())
        elif a.komut == "rapor":
            print(mv_rapor())
    except MVHata as ex:
        mvlog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_mv_ana())
