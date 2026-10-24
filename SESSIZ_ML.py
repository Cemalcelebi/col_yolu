# =====================================================================
#  SESSIZ_ML — sessiz yuvarlanma (Z0) bolgelerinde ALIS ve SATIS icin makine ogrenmesi   (2026-10-23, v1.2)
#
#  CEMAL (23 Eki): "Isaretledigin bolgede alis ve satis, makine ogrenmesi icin ne gerekiyorsa her seyi yap."
#  BOLGE: FON_IZI v1.1 Z0 = son 20 bar +%5..+%30, medyan mum hissenin kendi 250 bar normalinin <= 0,85'i, verim >= 0,3,
#    taban gunu yok, geri cekilme >= -%10 (fon hisselerinin sessiz birikim bolgesi). Olay = Z0 gunu (ayni hissede 20 bar icinde bir kez).
#  OZELLIKLER (hepsi o gune kadarki veriyle, ileriye bakis yok; K2): Z0 ve hacim esligi olculeri (FON_IZI.fi_hacim_olc), 5/60/120/250
#    bar getiri, 250 bar aralikta konum, oynaklik (20/60 ve orani), mum boyu, SMA20/50/200 uzakligi ve SMA50 egimi, RSI14, 60 barin en
#    buyuk gunluk yukselis/dusus, tavan/taban gunu sayisi, 120 bar dogrusallik (R2), TL hacim duzeyi ve 60/250 hacim orani, kapanis
#    konumu, doji ve alt fitil orani, bosluklu acilis sikligi, fiyat duzeyi; pazar baglami (evren medyan 20/60 getiri, SMA50 ustu oran),
#    hissenin evrendeki likidite ve 60 bar getiri sirasi, sektor ruzgari (sektor medyan 60 bar getiri - evren medyani), pazar bayragi.
#  ALIS ETIKETLERI (K3): y_k20 = 60 bar icinde once +%20 mi -%10 mu (High/Low); y_x2 = 250 bar icinde once 2 kat mi -%30 mu.
#  ALIS MODELI (K4): LightGBM, YIL YIL ILERI YURUYEN egitim: test yili Y icin yalniz etiket ufku Y'den once biten olaylarla egitilir
#    (k20: t + 90 takvim gunu < Y basi; x2: t + 365 gun < Y basi). BIST + ABD birlikte, pazar bayragi ozellik. Degerlendirme: AUC;
#    her test yilinda puana gore ust %20 vs geri kalan isabet orani (kat); dilimler BIST/ABD x 2019-21/2022-26; iz = 4 dilimde kat >= 1,3.
#  PORTFOY (K5): 30 slot, sinyalin ertesi gun acilisinda giris, uretim cikisi (T10: +%8 gorulunce stop maliyete; +%20 gorulunce SMA20
#    trail; 120 bar ufuk) + ilk stop Z0 20 bar dibinin -%2'si (T6 benzeri), %0,4 maliyet. Karsilastirma: tum Z0 / model ust %20 /
#    ayni sayida rastgele Z0 (20 tohum medyani).
#  SATIS MODELI (K6): tum Z0 islemlerinin tutuldugu her gun bir satir: gunluk ozellikler + pozisyon ozellikleri (gun, kar, en yuksek
#    kar, zirveden geri cekilme). Etiket y_sat = sonraki 20 barda once -%10 gelirse 1 (sat); once +%10 ya da hicbiri 0 (v1.1 duzeltme: 'hicbiri' eskiden 1 sayiliyordu). Ayni ileri yuruyen egitim
#    (t + 40 gun < Y basi). Kural: gun sonu P(sat) >= egitim donemi puanlarinin %90'lik esigi ise kapanista sat. Karsilastirma: ayni
#    girislerde uretim cikisi vs uretim + model cikisi. Ayrica 2026 fon hisselerinde model cikisinin cokusten once gelip gelmedigi.
#  STANDART (CLAUDE.md): BIST + ABD, iki donem, sabit esikler, trail, slot simulasyonu, taban 1,3x. ML bir 'kapali konu' degil ama
#    COL_OZET §3: KNN (5 olcu) kar eklemedi, IZ_DEFTERI C: makine birlesimi AUC 0,56. Ayni olcutle olculur.
#  OGRETMEN (K8, Cemal 23 Eki: "ogretmen ol; fon hisselerinden ogrendigin izi diger hisselerde gor: alim var, fiyat yukselecek ya da
#    satis var, dusecek; tuttu mu?"): etiketler SONUCTAN degil fonun davranisindan gelir. ALIM ogretmeni: fon hisselerinin dip -> tepe-40
#    bar gunleri (fonun topladigi donem) = 1, fon disi BIST hisselerinin 2024-26 gunleri = 0. SATIS ogretmeni: fon hisselerinin tepe
#    oncesi son 40 bar (dagitim / cokus oncesi; fonun ne zaman sattigi bilinmiyor, varsayim) = 1, ayni negatifler = 0. Tarih bilgisi
#    tasiyan pazar ozellikleri (piy20, piy60, genislik) ve pazar bayragi kullanilmaz. Fon disi BIST hisseleri ikiye bolunur (sembol
#    karmasi): yarisi egitim negatifi, yarisi hic gorulmeden degerlendirme. Hisse gruplu 5 katli capraz dogrulama AUC'si raporlanir.
#    Degerlendirme: gorulmemis BIST yarisi + tum ABD, 2016-26, her gun puanlanir; puan >= egitim negatiflerinin %95'lik esigi = 'iz var'
#    (ayni hissede 20 bar icinde bir kez). Alim izi sonucu: 60 barda once +%20 / -%10, 250 barda 2 kat / -%30, 60 bar getiri. Satis izi
#    sonucu: 20 barda once -%10 / +%10 (dusus once), 20 bar getiri. Taban: ayni hisselerin her 20. gunu. Iz = 4 dilimde kat >= 1,3.
#  v1.1 (23 Eki) DORT KONTROL (Cemal: "gercekten ogrenip ogrenmedigini nasil anlayacagiz?"):
#    (1) EGITIM KANITI: her egitimde LightGBM logloss egrisi (egitim ve test, ilk ve son agac) ve sabit tahmin (taban) kaybi tabloya
#        yazilir; her model dosyasi arastirma_cikti/sessiz_ml/modeller/ altina kaydedilir.
#    (2) GORMEDIGI VERI: alis/satis modelleri yil yil kronolojik (gecmisle egit, sonraki yili sina, etiket ufku kadar embargo);
#        ogretmen icin ayrica tarih kesimli test: 2025-07-01 oncesi verisiyle egitilir, sonrasinda gorulmemis hisselerde sinanir.
#    (3) ALIS/SATIS BASARISI: pozitif tahminlerden acilan islemlerde hedefe (+%20) ulasan, zararla kapanan, agir zarar (<= -%15)
#        oranlari; komisyon %0,2 (gidis-donus) + kayma her yonde %0,3 = islem basina %0,8 dusulur. Satis: model satisindan 20 bar
#        sonra fiyat satis fiyatinin altinda mi (dogru satis orani).
#    (4) SIZINTI: (a) etiketler karistirilinca AUC ~0,5'e inmeli; (b) bilerek eklenen gelecek bilgisi (60 bar sonraki getiri) AUC'yi
#        sicratmali (degerlendirme sizintiyi yakaliyor mu); (c) test_sessiz_ml.py: gelecek degisince gecmis ozellik ayni, embargo.
#  KURAL_MOTORU: K1 veri  K2 ozellik  K3 alis olaylari  K4 alis modeli  K5 portfoy  K6 satis modeli  K7 rapor
#  Calistirma: FI_VERI_BIST=... FI_VERI_ABD=... python SESSIZ_ML.py   Cikti: arastirma_cikti/sessiz_ml/
# =====================================================================
from __future__ import annotations

import logging
import os
import sys
import time
from dataclasses import dataclass, field, replace
from typing import Any, Dict, List, Optional, Tuple

import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", message=".*eval_set.*")   # lightgbm 4.7 uyarisi; Colab'daki eski surumde eval_set gecerli

_CK_ONCE_SM = {k: id(v) for k, v in globals().items()}

SM_SURUM = "SESSIZ_ML v1.3 (2026-10-24, denetim: bar ufuklu embargo, islem basina satis puani, slot hisse basina tek)"
smlog = logging.getLogger("col.sessiz_ml")
if not smlog.handlers:
    _sm_h = logging.StreamHandler(sys.stderr)
    _sm_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sessiz_ml: %(message)s", "%H:%M:%S"))
    smlog.addHandler(_sm_h)
    smlog.setLevel(logging.INFO)
    smlog.propagate = False


@dataclass
class SMAyar:
    test_yillari: Tuple[int, ...] = (2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026)
    donem_siniri: str = "2022-01-01"
    olay_bas: str = "2016-01-01"
    tekrar: int = 20
    ust_oran: float = 0.20            # model ust dilimi (egitim puanlarinin %80'lik esigi)
    sat_esik_q: float = 0.90          # satis modeli esigi (egitim puanlarinin %90'lik esigi)
    slot: int = 30
    komisyon: float = 0.002           # gidis-donus toplam
    kayma: float = 0.003              # her yonde (alis ve satis)
    maliyet: float = 0.008            # = komisyon + 2 x kayma (__post_init__ yeniden hesaplar)
    kesim: str = "2025-07-01"         # ogretmen tarih kesimli testi
    hedef: float = 0.20
    maliyete: float = 0.08
    ufuk: int = 120
    stop_pay: float = 0.02
    rastgele_tohum: int = 20
    gbm: Dict[str, Any] = field(default_factory=lambda: dict(n_estimators=300, learning_rate=0.03, num_leaves=15,
                                                             min_child_samples=100, subsample=0.8, subsample_freq=1,
                                                             colsample_bytree=0.8, reg_lambda=1.0, verbose=-1))
    sektor: Dict[str, str] = field(default_factory=lambda: {"BIST": "sektor_BIST.csv", "ABD": "sektor_ABD.csv"})
    cikti: str = "arastirma_cikti/sessiz_ml"

    def __post_init__(self):
        self.maliyet = self.komisyon + 2 * self.kayma


# ---------------------------------------------------------------- K2 ozellik
def _rsi(c: pd.Series, n: int = 14) -> pd.Series:
    d = c.diff(); up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean(); dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def sm_ozellik(d: pd.DataFrame, FA) -> pd.DataFrame:
    """Gunluk ozellikler (yalniz o gune kadarki veri). FA = FON_IZI.FIAyar (Z0 tanimi)."""
    import FON_IZI as F
    o = F.fi_hacim_olc(d, FA)
    c = d.Close; o_, h, l = d.Open, d.High, d.Low; pc = c.shift(); r = c / pc - 1
    hl = (h - l).replace(0, np.nan); v = d.Volume.replace(0, np.nan); tl = c * d.Volume
    for n in (5, 60, 120, 250):
        o[f"g{n}"] = c / c.shift(n) - 1
    mx = c.rolling(250, min_periods=120).max(); mn = c.rolling(250, min_periods=120).min()
    o["yuk250"] = c / mx - 1; o["dip250"] = c / mn - 1; o["konum250"] = (c - mn) / (mx - mn)
    o["vol20"] = r.rolling(20).std(); o["vol60"] = r.rolling(60).std(); o["vol_oran"] = o.vol20 / o.vol60
    o["mum14"] = ((h - l) / pc).rolling(14).median()
    for n in (20, 50, 200):
        o[f"sma{n}_uz"] = c / c.rolling(n, min_periods=int(n * 0.8)).mean() - 1
    s50 = c.rolling(50).mean(); o["sma50_egim"] = s50 / s50.shift(10) - 1
    o["rsi14"] = _rsi(c)
    o["maxup60"] = r.rolling(60).max(); o["maxdn60"] = r.rolling(60).min()
    o["tavan60"] = (r >= FA.sinir_gun).astype(float).rolling(60).sum(); o["taban60"] = (r <= -FA.sinir_gun).astype(float).rolling(60).sum()
    o["r2_120"] = F._fi_r2(np.log(c), 120)
    o["tl_log"] = np.log10(tl.rolling(20).median() + 1)
    o["hk60"] = v.rolling(60).median() / v.rolling(250, min_periods=120).median()
    o["clv20"] = ((c - l) / hl).rolling(20).mean()
    o["doji20"] = (((c - o_).abs() / hl) < 0.15).astype(float).rolling(20).mean()
    o["altfitil20"] = ((np.minimum(o_, c) - l) / hl).rolling(20).mean()
    o["gapup20"] = ((o_ / pc - 1) > 0.01).astype(float).rolling(20).mean()
    o["logp"] = np.log10(c)
    o["sma20"] = c.rolling(20).mean()          # satis/cikis icin (ozellik degil)
    o["dip20"] = l.rolling(20).min()           # ilk stop icin (ozellik degil)
    return o


OZ_KOL = ["g", "mk", "verim", "dd", "udvr", "hk", "emilim", "vcv", "dh", "emilim_gun", "g5", "g60", "g120", "g250", "yuk250", "dip250",
          "konum250", "vol20", "vol60", "vol_oran", "mum14", "sma20_uz", "sma50_uz", "sma200_uz", "sma50_egim", "rsi14", "maxup60",
          "maxdn60", "tavan60", "taban60", "r2_120", "tl_log", "hk60", "clv20", "doji20", "altfitil20", "gapup20", "logp",
          "piy20", "piy60", "genislik", "tl_yzd", "g60_yzd", "sektor_ruzgar", "pazar_bist"]


def sm_k2_panel(V: Dict[str, pd.DataFrame], pazar: str, FA, A: SMAyar) -> Dict[str, pd.DataFrame]:
    """Her hisse icin gunluk ozellikler + kesitsel (pazar, sektor, sira) ozellikler."""
    t0 = time.time(); Z: Dict[str, pd.DataFrame] = {}
    for no, (s, d) in enumerate(V.items(), 1):
        try:
            if len(d) >= 400:
                Z[s] = sm_ozellik(d, FA).astype("float32")
        except Exception as ex:
            smlog.warning("ozellik %s atlandi: %s", s, ex)
        if no % 300 == 0:
            smlog.info("%s ozellik %d/%d, %.0f sn", pazar, no, len(V), time.time() - t0)
    g20 = pd.concat({s: z.g for s, z in Z.items()}, axis=1, sort=True)
    g60 = pd.concat({s: z.g60 for s, z in Z.items()}, axis=1, sort=True)
    ust50 = pd.concat({s: (z.sma50_uz > 0).astype(float).where(z.sma50_uz.notna()) for s, z in Z.items()}, axis=1, sort=True)
    tl = pd.concat({s: z.tl_log for s, z in Z.items()}, axis=1, sort=True)
    piy20 = g20.median(axis=1); piy60 = g60.median(axis=1); gen = ust50.mean(axis=1)
    tl_yzd = tl.rank(axis=1, pct=True); g60_yzd = g60.rank(axis=1, pct=True)
    ruz = pd.DataFrame(np.nan, index=g60.index, columns=g60.columns)
    yol = A.sektor.get(pazar)
    if yol and os.path.exists(yol):
        sk = pd.read_csv(yol); sk["sembol"] = sk.sembol.astype(str).str.replace(r"\.\w+$", "", regex=True)
        harita = dict(zip(sk.sembol, sk.sektor))
        for sek in set(harita.values()):
            uye = [s for s in g60.columns if harita.get(s) == sek]
            if len(uye) >= 4:
                fark = (g60[uye].median(axis=1) - piy60).to_numpy()
                ruz.loc[:, uye] = np.repeat(fark[:, None], len(uye), axis=1)
    else:
        smlog.warning("%s sektor dosyasi yok (%s); sektor_ruzgar bos", pazar, yol)
    for s, z in Z.items():
        ix = z.index
        z["piy20"] = piy20.reindex(ix).values; z["piy60"] = piy60.reindex(ix).values; z["genislik"] = gen.reindex(ix).values
        z["tl_yzd"] = tl_yzd[s].reindex(ix).values; z["g60_yzd"] = g60_yzd[s].reindex(ix).values
        z["sektor_ruzgar"] = ruz[s].reindex(ix).values; z["pazar_bist"] = 1.0 if pazar == "BIST" else 0.0
    smlog.info("%s panel hazir: %d hisse, %.0f sn", pazar, len(Z), time.time() - t0)
    return Z


# ---------------------------------------------------------------- K3 alis olaylari ve etiketler
def sm_once(h: np.ndarray, l: np.ndarray, c0: float, i: int, ufuk: int, yukari: float, asagi: float) -> float:
    """i'den sonraki ufuk bar icinde once c0*(1+yukari) mi (1) c0*(1-asagi) mi (0); ayni gun ikisi = 0; ufuk dolmamissa NaN."""
    n = len(h)
    if i + ufuk >= n:
        return np.nan
    for j in range(i + 1, i + ufuk + 1):
        if l[j] <= c0 * (1 - asagi):
            return 0.0
        if h[j] >= c0 * (1 + yukari):
            return 1.0
    return 0.0


def sm_once_vek(h: np.ndarray, l: np.ndarray, c: np.ndarray, idx: np.ndarray, ufuk: int, yukari: float, asagi: float) -> np.ndarray:
    """sm_once'un vektorel hali (ayni kurallar): her i icin sonraki ufuk barda once yukari (1) / asagi (0); ufuk dolmamissa NaN."""
    idx = np.asarray(idx, dtype=int); n = len(h); out = np.full(len(idx), np.nan)
    if n <= ufuk + 1 or len(idx) == 0:
        return out
    ok = idx + ufuk < n; ii = idx[ok]
    if len(ii) == 0:
        return out
    from numpy.lib.stride_tricks import sliding_window_view as swv
    H = swv(h[1:], ufuk)[ii]; L = swv(l[1:], ufuk)[ii]; c0 = c[ii][:, None]
    up = H >= c0 * (1 + yukari); dn = L <= c0 * (1 - asagi)
    iu = np.where(up.any(1), up.argmax(1), ufuk + 1); idn = np.where(dn.any(1), dn.argmax(1), ufuk + 1)
    out[ok] = (iu < idn).astype(float)        # ayni gun ikisi (iu == idn) = 0
    return out


def sm_ilk_vek(h: np.ndarray, l: np.ndarray, c: np.ndarray, idx: np.ndarray, ufuk: int, yukari: float, asagi: float) -> np.ndarray:
    """Ufuk icinde hangisi once: +1 yukari, -1 asagi (ayni gun ikisi = -1), 0 hicbiri; ufuk dolmamissa NaN."""
    idx = np.asarray(idx, dtype=int); n = len(h); out = np.full(len(idx), np.nan)
    ok = idx + ufuk < n; ii = idx[ok]
    if len(ii) == 0 or n <= ufuk + 1:
        return out
    from numpy.lib.stride_tricks import sliding_window_view as swv
    H = swv(h[1:], ufuk)[ii]; L = swv(l[1:], ufuk)[ii]; c0 = c[ii][:, None]
    up = H >= c0 * (1 + yukari); dn = L <= c0 * (1 - asagi)
    iu = np.where(up.any(1), up.argmax(1), ufuk + 1); idn = np.where(dn.any(1), dn.argmax(1), ufuk + 1)
    out[ok] = np.where(idn <= iu, np.where(idn <= ufuk, -1.0, 0.0), 1.0)
    return out


def sm_k3_olaylar(V: Dict[str, pd.DataFrame], Z: Dict[str, pd.DataFrame], pazar: str, A: SMAyar) -> pd.DataFrame:
    rows = []
    for s, z in Z.items():
        d = V[s]; h = d.High.to_numpy(); l = d.Low.to_numpy(); c = d.Close.to_numpy()
        zf = z.Z0.to_numpy() > 0; son = -10 ** 9; X = z[OZ_KOL].to_numpy(); sec = []
        for i in np.flatnonzero(zf):
            if i - son < A.tekrar or d.index[i] < pd.Timestamp(A.olay_bas) or i + 1 >= len(d):
                continue
            son = i; sec.append(i)
        if not sec:
            continue
        sec = np.array(sec); yk = sm_once_vek(h, l, c, sec, 60, 0.20, 0.10); yx = sm_once_vek(h, l, c, sec, 250, 1.0, 0.30)
        for j, i in enumerate(sec):
            rows.append({"pazar": pazar, "sembol": s, "tarih": d.index[i], "i": int(i), "y_k20": yk[j], "y_x2": yx[j],
                         # denetim 24 Eki: etiket ufku bar; embargo takvim gunuydu (BIST'te 60 bar 84-97 gun) -> etiket bitis tarihi
                         "bitis_y_k20": d.index[min(i + 60, len(d) - 1)], "bitis_y_x2": d.index[min(i + 250, len(d) - 1)],
                         "gelecek_r60": c[i + 60] / c[i] - 1 if i + 60 < len(c) else np.nan,   # yalniz sizinti kanaryasi; ozellik degil
                         **dict(zip(OZ_KOL, X[i]))})
    O = pd.DataFrame(rows)
    smlog.info("%s Z0 olayi: %d", pazar, len(O))
    return O


# ---------------------------------------------------------------- K4 alis modeli (ileri yuruyen)
def _logloss(y: np.ndarray, p: np.ndarray) -> float:
    p = np.clip(p, 1e-7, 1 - 1e-7)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def sm_ileri_egit(O: pd.DataFrame, etiket: str, embargo_gun: int, A: SMAyar, kol: List[str] = OZ_KOL,
                  ad: Optional[str] = None) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[int, float], pd.DataFrame]:
    """Her test yili icin yalniz etiketi o yildan once kesinlesen olaylarla egitir.
    Donus: (tahminli olaylar, onem, yil esikleri, egitim kaniti). ad verilirse modeller cikti/modeller/ad_YIL.txt olarak kaydedilir."""
    import lightgbm as lgb
    O = O.copy(); O["p"] = np.nan; onem = []; esik: Dict[int, float] = {}; kanit = []
    t = pd.to_datetime(O.tarih)
    for Y in A.test_yillari:
        bas = pd.Timestamp(f"{Y}-01-01"); bit = pd.Timestamp(f"{Y + 1}-01-01")
        bk = f"bitis_{etiket}"           # denetim 24 Eki: etiketin bittigi gun test yilindan once (bar ufku); yoksa eski gun embargosu
        tr = O[((pd.to_datetime(O[bk]) < bas) if bk in O else (t + pd.Timedelta(days=embargo_gun) < bas)) & O[etiket].notna()]
        te = (t >= bas) & (t < bit)
        if len(tr) < 500 or tr[etiket].nunique() < 2 or not te.any():
            smlog.warning("%s %d: egitim kucuk (%d) ya da test yok, atlandi", etiket, Y, len(tr)); continue
        m = lgb.LGBMClassifier(**A.gbm, random_state=Y)
        tey = O.loc[te & O[etiket].notna()]
        evs = [(tr[kol], tr[etiket])] + ([(tey[kol], tey[etiket])] if len(tey) and tey[etiket].nunique() > 1 else [])
        m.fit(tr[kol], tr[etiket], eval_set=evs, eval_metric="binary_logloss")
        er = m.evals_result_; k_tr = er["training"]["binary_logloss"] if "training" in er else er["valid_0"]["binary_logloss"]
        k_te = er.get("valid_1", {}).get("binary_logloss", [np.nan])
        sabit_tr = _logloss(tr[etiket].to_numpy(), np.full(len(tr), tr[etiket].mean()))
        sabit_te = _logloss(tey[etiket].to_numpy(), np.full(len(tey), tr[etiket].mean())) if len(tey) else np.nan
        dosya = ""
        if ad:
            os.makedirs(os.path.join(A.cikti, "modeller"), exist_ok=True)
            dosya = os.path.join(A.cikti, "modeller", f"{ad}_{Y}.txt"); m.booster_.save_model(dosya)
        kanit.append({"model": ad or etiket, "test_yili": Y, "n_egitim": len(tr), "n_test": len(tey), "agac": len(k_tr),
                      "egitim_kayip_ilk": k_tr[0], "egitim_kayip_son": k_tr[-1], "egitim_sabit_tahmin": sabit_tr,
                      "test_kayip_ilk": k_te[0], "test_kayip_son": k_te[-1], "test_kayip_en_dusuk": float(np.nanmin(k_te)),
                      "test_sabit_tahmin": sabit_te, "dosya": dosya})
        O.loc[te, "p"] = m.predict_proba(O.loc[te, kol])[:, 1]
        p_tr = m.predict_proba(tr[kol])[:, 1]
        esik[Y] = float(np.quantile(p_tr, 1 - A.ust_oran))
        if "pazar" in O.columns:                       # v1.2: pazar bazinda egitim esigi (havuz esigi BIST'te %58-74 seciyordu)
            if "esik_pz" not in O.columns:
                O["esik_pz"] = np.nan
            for pz in O.loc[te, "pazar"].dropna().unique():
                mk = (tr.pazar == pz).to_numpy()
                O.loc[te & (O.pazar == pz), "esik_pz"] = float(np.quantile(p_tr[mk], 1 - A.ust_oran)) if mk.sum() >= 100 else esik[Y]
        onem.append(pd.Series(m.booster_.feature_importance("gain"), index=kol, name=Y))
    imp = pd.concat(onem, axis=1) if onem else pd.DataFrame()
    if not imp.empty:
        imp = (imp / imp.sum()).mean(axis=1).sort_values(ascending=False).rename("pay").reset_index().rename(columns={"index": "ozellik"})
    return O, imp, esik, pd.DataFrame(kanit)


def _auc(y: np.ndarray, p: np.ndarray) -> float:
    m = ~(np.isnan(y) | np.isnan(p))
    y, p = y[m], p[m]
    if len(np.unique(y)) < 2:
        return np.nan
    r = pd.Series(p).rank().to_numpy(); n1 = y.sum(); n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def sm_degerlendir(O: pd.DataFrame, etiket: str, A: SMAyar) -> pd.DataFrame:
    """Dilim basina AUC ve ust %20 (test yili icinde puana gore) isabet orani / geri kalan."""
    P = O[O.p.notna() & O[etiket].notna()].copy()
    P["yil"] = pd.to_datetime(P.tarih).dt.year
    P["ust"] = P.groupby(["pazar", "yil"]).p.transform(lambda x: x >= x.quantile(1 - A.ust_oran))
    P["donem"] = np.where(pd.to_datetime(P.tarih) < pd.Timestamp(A.donem_siniri), "2019-21", "2022-26")
    rows = []
    for (pz, dn), g in P.groupby(["pazar", "donem"]):
        u = g[g.ust]; k = g[~g.ust]
        rows.append({"etiket": etiket, "pazar": pz, "donem": dn, "n": len(g), "auc": _auc(g[etiket].to_numpy(), g.p.to_numpy()),
                     "ust_isabet": u[etiket].mean() * 100, "kalan_isabet": k[etiket].mean() * 100, "tum_isabet": g[etiket].mean() * 100,
                     "kat": u[etiket].mean() / k[etiket].mean() if k[etiket].mean() > 0 else np.nan, "n_ust": len(u)})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- K5 portfoy
def sm_cikis(o: np.ndarray, h: np.ndarray, l: np.ndarray, c: np.ndarray, sma20: np.ndarray, e: int, stop0: float, A: SMAyar,
             psat: Optional[np.ndarray] = None, sat_esik: float = np.inf) -> Tuple[int, float, str, bool]:
    """Uretim cikisi (+ istege bagli model cikisi). Giris e gunu acilisi. Donus (cikis gunu, cikis fiyati, neden, hedef goruldu mu)."""
    n = len(c); giris = o[e]; stop = stop0; tepe = -np.inf; hedef_goruldu = False
    for j in range(e, n):
        if l[j] <= stop:
            fiyat = min(o[j], stop) if j > e else min(giris, stop)
            return j, fiyat, ("maliyet" if stop >= giris else "stop"), hedef_goruldu
        tepe = max(tepe, h[j])
        if tepe >= giris * (1 + A.maliyete):
            stop = max(stop, giris)
        if tepe >= giris * (1 + A.hedef):
            hedef_goruldu = True
        if hedef_goruldu and np.isfinite(sma20[j]) and c[j] < sma20[j]:
            return j, c[j], "trail", True
        if psat is not None and j > e and np.isfinite(psat[j]) and psat[j] >= sat_esik:
            return j, c[j], "model", hedef_goruldu
        if not hedef_goruldu and j - e >= A.ufuk:
            return j, c[j], "ufuk", False
    return n - 1, c[n - 1], "acik", hedef_goruldu


def sm_islemler(sinyal: pd.DataFrame, V: Dict[str, pd.DataFrame], Z: Dict[str, pd.DataFrame], A: SMAyar,
                PS: Optional[Dict[str, np.ndarray]] = None, sat_esik: Optional[Dict[int, float]] = None) -> pd.DataFrame:
    """Her sinyal icin (ertesi gun acilis girisi) cikis; PS verilirse model cikisi da (yil esigi giris yilina gore)."""
    rows = []
    for x in sinyal.itertuples():
        d = V[x.sembol]; z = Z[x.sembol]; e = int(x.i) + 1
        if e >= len(d):
            continue
        o, h, l, c = (d[k].to_numpy() for k in ("Open", "High", "Low", "Close"))
        stop0 = float(z.dip20.iat[int(x.i)]) * (1 - A.stop_pay)
        ps = PS.get((x.sembol, pd.Timestamp(d.index[e]))) if PS is not None else None
        es = sat_esik.get(pd.Timestamp(x.tarih).year, np.inf) if sat_esik else np.inf
        j, fiyat, neden, hg = sm_cikis(o, h, l, c, z.sma20.to_numpy(), e, stop0, A, ps, es)
        rows.append({"pazar": x.pazar, "sembol": x.sembol, "sinyal": x.tarih, "giris_t": d.index[e], "cikis_t": d.index[j],
                     "getiri": fiyat / o[e] - 1 - A.maliyet, "brut": fiyat / o[e] - 1, "bar": j - e, "neden": neden, "hedef_gordu": hg,
                     "sonra20": c[j + 20] / fiyat - 1 if j + 20 < len(c) else np.nan})
    return pd.DataFrame(rows)


def sm_portfoy(I: pd.DataFrame, A: SMAyar) -> Dict[str, float]:
    """30 slot: sirayla giris, bos slot yoksa atla; esit pay (giristeki ozkaynak / slot), cikista ozkaynak guncellenir."""
    if I.empty:
        return {"islem": 0, "portfoy": 0.0, "kazanan": np.nan, "islem_basi": np.nan, "agir": np.nan}
    I = I.sort_values("giris_t"); oz = 1.0; acik: List[Tuple[pd.Timestamp, float, float, str]] = []; alinan = []
    for x in I.itertuples():
        # denetim 24 Eki: cikis gunu kapanista biten islemin parasi o gunun acilisinda kullanilamaz (<); ayni hisseye ikinci slot yok
        for a in [a for a in acik if a[0] < x.giris_t]:
            oz += a[1] * a[2]; acik.remove(a)
        sem = getattr(x, "sembol", None)
        if len(acik) >= A.slot or (sem is not None and any(a[3] == sem for a in acik)):
            continue
        pay = oz / A.slot; acik.append((x.cikis_t, pay, x.getiri, sem)); alinan.append(x.getiri)
    for a in acik:
        oz += a[1] * a[2]
    g = np.array(alinan)
    return {"islem": len(g), "portfoy": (oz - 1) * 100, "kazanan": (g > 0).mean() * 100, "islem_basi": g.mean() * 100,
            "agir": (g <= -0.15).mean() * 100}


def sm_basari(I: pd.DataFrame) -> Dict[str, float]:
    """Islem basarisi (maliyet dusulmus): hedefe ulasan, zararla kapanan, agir zarar, ortalama/medyan net getiri."""
    if I.empty:
        return {"n": 0}
    return {"n": len(I), "hedefe_ulasan_%": I.hedef_gordu.mean() * 100, "zararla_kapanan_%": (I.getiri < 0).mean() * 100,
            "agir_zarar_%": (I.getiri <= -0.15).mean() * 100, "ort_net_%": I.getiri.mean() * 100, "medyan_net_%": I.getiri.median() * 100,
            "ort_brut_%": I.brut.mean() * 100, "ort_bar": I.bar.mean()}


# ---------------------------------------------------------------- K6 satis modeli
POZ_KOL = ["gun", "kar", "kar_maks", "zirveden"]


def sm_k6_satis_satirlari(I: pd.DataFrame, V: Dict[str, pd.DataFrame], Z: Dict[str, pd.DataFrame], A: SMAyar) -> pd.DataFrame:
    """Uretim cikisli islemlerin tutuldugu her gun: ozellik + pozisyon durumu + y_sat (20 bar icinde once -%10 = 1)."""
    parca = []
    for x in I.itertuples():
        d = V[x.sembol]; z = Z[x.sembol]
        e = d.index.get_loc(x.giris_t); j = d.index.get_loc(x.cikis_t)
        if j <= e:
            continue
        h = d.High.to_numpy(); l = d.Low.to_numpy(); c = d.Close.to_numpy(); o = d.Open.to_numpy()
        ix = np.arange(e + 1, j + 1); giris = o[e]
        tepe = np.maximum.accumulate(h[e:j + 1])[1:]
        ilk = sm_ilk_vek(h, l, c, ix, 20, 0.10, 0.10)
        df = z.iloc[ix][OZ_KOL].copy()
        df["gun"] = ix - e; df["kar"] = c[ix] / giris - 1; df["kar_maks"] = tepe / giris - 1; df["zirveden"] = c[ix] / tepe - 1
        df["y_sat"] = np.where(np.isnan(ilk), np.nan, (ilk == -1).astype(float))   # once -%10 -> 1 (sat); once +%10 ya da hicbiri -> 0
        df["pazar"] = x.pazar; df["sembol"] = x.sembol; df["tarih"] = d.index[ix]; df["k"] = ix
        df["giris_t"] = x.giris_t                                   # denetim 24 Eki: ayni hissede ust uste binen islemler ayrilsin
        df["bitis_y_sat"] = d.index[np.minimum(ix + 20, len(d) - 1)]
        parca.append(df)
    S = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame()
    smlog.info("satis satiri: %d", len(S))
    return S


def sm_satis_puan(S: pd.DataFrame, A: SMAyar):
    kol = OZ_KOL + POZ_KOL
    return sm_ileri_egit(S, "y_sat", 40, replace(A, ust_oran=1 - A.sat_esik_q), kol, ad="satis")


# ---------------------------------------------------------------- sizinti kontrolu
def sm_sizinti(O: pd.DataFrame, A: SMAyar) -> pd.DataFrame:
    """(a) karistirilmis etiket -> AUC ~0,5 olmali; (b) gelecek bilgisi kanaryasi -> AUC sicramali; (c) normal model (karsilastirma)."""
    hizli = replace(A, gbm={**A.gbm, "n_estimators": 150})
    rng = np.random.default_rng(11); rows = []
    Ok = O.copy(); Ok["y_kar"] = rng.permutation(Ok.y_k20.to_numpy())
    Ok["y_kar"] = np.where(O.y_k20.isna(), np.nan, Ok.y_kar)
    for ad, et, kol in (("normal", "y_k20", OZ_KOL), ("karistirilmis_etiket", "y_kar", OZ_KOL),
                        ("gelecek_kanaryasi", "y_k20", OZ_KOL + ["gelecek_r60"])):
        P, _, _, _ = sm_ileri_egit(Ok, et, 90, hizli, kol)
        dg = sm_degerlendir(P, et, hizli)
        for r in dg.itertuples():
            rows.append({"deneme": ad, "pazar": r.pazar, "donem": r.donem, "auc": r.auc, "kat_ust20": r.kat})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- K8 ogretmen
OGR_KOL = [k for k in OZ_KOL if k not in ("piy20", "piy60", "genislik", "pazar_bist")]


def _sm_yarim(s: str) -> int:
    """Sembolu kararli bicimde ikiye boler (0 = egitim negatifi, 1 = gorulmemis degerlendirme)."""
    return sum(ord(ch) for ch in s) % 2


def _sm_sonuclar_vek(h: np.ndarray, l: np.ndarray, c: np.ndarray, idx: np.ndarray) -> pd.DataFrame:
    idx = np.asarray(idx, dtype=int); n = len(c)
    ilk20 = sm_ilk_vek(h, l, c, idx, 20, 0.10, 0.10)
    return pd.DataFrame({"y_k20": sm_once_vek(h, l, c, idx, 60, 0.20, 0.10), "y_x2": sm_once_vek(h, l, c, idx, 250, 1.0, 0.30),
                         "y_dus20": np.where(np.isnan(ilk20), np.nan, (ilk20 == -1).astype(float)),
                         "r20": np.where(idx + 20 < n, c[np.minimum(idx + 20, n - 1)] / c[idx] - 1, np.nan),
                         "r60": np.where(idx + 60 < n, c[np.minimum(idx + 60, n - 1)] / c[idx] - 1, np.nan)})


def _ogr_egit(Pz: pd.DataFrame, N: pd.DataFrame, ad: str, A: SMAyar, esik_q: float):
    """Ogretmen modeli: hisse gruplu 5 kat CV AUC + tum veriyle egitim (logloss kaniti: egitim ve ayrilmis hisse grubu) + kayit."""
    import lightgbm as lgb
    X = pd.concat([Pz, N]); y = np.r_[np.ones(len(Pz)), np.zeros(len(N))]; grp = X.sembol.to_numpy()
    hisseler = np.unique(grp); rs = np.random.default_rng(3); kat_no = dict(zip(hisseler, rs.integers(0, 5, len(hisseler))))
    kk = np.array([kat_no[g] for g in grp]); pcv = np.full(len(X), np.nan); spw = len(N) / max(len(Pz), 1)
    for f in range(5):
        tr = kk != f; te = kk == f
        if len(np.unique(y[tr])) < 2 or len(np.unique(y[te])) < 2:
            continue
        m = lgb.LGBMClassifier(**A.gbm, random_state=f, scale_pos_weight=spw)
        m.fit(X.loc[tr, OGR_KOL], y[tr]); pcv[te] = m.predict_proba(X.loc[te, OGR_KOL])[:, 1]
    tr = kk != 0; te = kk == 0
    m = lgb.LGBMClassifier(**A.gbm, random_state=0, scale_pos_weight=spw)
    m.fit(X.loc[tr, OGR_KOL], y[tr], eval_set=[(X.loc[tr, OGR_KOL], y[tr]), (X.loc[te, OGR_KOL], y[te])], eval_metric="binary_logloss")
    er = m.evals_result_; k_tr = (er.get("training") or er["valid_0"])["binary_logloss"]; k_te = er["valid_1"]["binary_logloss"]
    mt = lgb.LGBMClassifier(**A.gbm, random_state=0, scale_pos_weight=spw); mt.fit(X[OGR_KOL], y)
    os.makedirs(os.path.join(A.cikti, "modeller"), exist_ok=True)
    dosya = os.path.join(A.cikti, "modeller", f"ogretmen_{ad}.txt"); mt.booster_.save_model(dosya)
    esik = float(np.quantile(mt.predict_proba(N[OGR_KOL])[:, 1], esik_q))
    imp = pd.Series(mt.booster_.feature_importance("gain"), index=OGR_KOL); imp = (imp / imp.sum()).sort_values(ascending=False)
    kanit = {"model": f"ogretmen_{ad}", "pozitif": len(Pz), "negatif": len(N), "cv_auc_hisse_gruplu": _auc(y, pcv), "agac": len(k_tr),
             "egitim_kayip_ilk": k_tr[0], "egitim_kayip_son": k_tr[-1], "ayrik_hisse_kayip_ilk": k_te[0],
             "ayrik_hisse_kayip_son": k_te[-1], "esik": esik, "dosya": dosya}
    return mt, esik, kanit, imp


def sm_k8_ogretmen(V: Dict[str, Dict[str, pd.DataFrame]], Z: Dict[str, Dict[str, pd.DataFrame]], A: SMAyar, FA,
                   kos: pd.DataFrame, neg_bas: str = "2024-01-01", neg_bit: str = "2026-09-14", dagitim_bar: int = 40,
                   neg_ornek: int = 150000, esik_q: float = 0.95, taban_ornek: int = 20000) -> Dict[str, pd.DataFrame]:
    import FON_IZI as F
    ZB = Z["BIST"]; fon = [s for s in F.FON_HISSE if s in ZB]; kosd = kos.set_index("sembol"); kesim = pd.Timestamp(A.kesim)
    pos = {"alim": [], "satis": []}
    for s in fon:
        if s not in kosd.index:
            continue
        k = kosd.loc[s]; z = ZB[s]; ix = z.index
        it = ix.get_indexer([pd.Timestamp(k.tepe)])[0]; idp = ix.get_indexer([pd.Timestamp(k.dip)])[0]
        if it < 0 or idp < 0:
            continue
        pos["alim"].append(z.iloc[idp:max(idp, it - dagitim_bar)][OGR_KOL].assign(sembol=s))
        pos["satis"].append(z.iloc[max(idp, it - dagitim_bar):it + 1][OGR_KOL].assign(sembol=s))
    pos = {a: pd.concat(v) for a, v in pos.items()}
    N = pd.concat([z.loc[neg_bas:neg_bit, OGR_KOL].assign(sembol=s) for s, z in ZB.items() if s not in fon and _sm_yarim(s) == 0])
    N = N.sample(min(neg_ornek, len(N)), random_state=1)
    smlog.info("ogretmen: alim pozitif %d, satis pozitif %d, negatif %d (%d fon hissesi)", len(pos["alim"]), len(pos["satis"]), len(N), len(fon))
    out: Dict[str, pd.DataFrame] = {}; kan = []; prof = []; imps = []
    M: Dict[str, Any] = {}
    for ad in ("alim", "satis"):
        Pz = pos[ad]
        mt, es, kt, imp = _ogr_egit(Pz, N, ad, A, esik_q); kan.append(kt); M[ad] = (mt, es)
        imps.append(imp.rename(f"onem_{ad}"))
        prof.append(pd.DataFrame({f"fon_{ad}_medyan": Pz[OGR_KOL].median()}))
        # tarih kesimli ogretmen: yalniz kesim oncesi veriyle
        Pk = Pz[Pz.index < kesim]; Nk = N[N.index < kesim]
        if len(Pk) > 200:
            mk, ek, kk_, _ = _ogr_egit(Pk, Nk, ad + "_kesim", A, esik_q); kan.append(kk_); M[ad + "_kesim"] = (mk, ek)
    prof.append(pd.DataFrame({"diger_medyan": N[OGR_KOL].median()}))
    out["ogr_kanit"] = pd.DataFrame(kan)
    out["ogr_profil"] = pd.concat(prof, axis=1).reset_index().rename(columns={"index": "ozellik"})
    out["ogr_onem"] = pd.concat(imps, axis=1).reset_index().rename(columns={"index": "ozellik"})
    # (a) kesim sonrasi tespit: fon hisselerinin kesim sonrasi alim/satis gunlerinin isaretlenme orani vs gorulmemis hisseler
    tes = []
    for ad in ("alim", "satis"):
        if ad + "_kesim" not in M:
            continue
        mk, ek = M[ad + "_kesim"]
        Pk = pos[ad][pos[ad].index >= kesim]
        Hk = pd.concat([z.loc[kesim:neg_bit, OGR_KOL] for s, z in ZB.items() if s not in fon and _sm_yarim(s) == 1])
        pf = (mk.predict_proba(Pk[OGR_KOL])[:, 1] >= ek).mean() if len(Pk) else np.nan
        ph = (mk.predict_proba(Hk[OGR_KOL])[:, 1] >= ek).mean()
        tes.append({"ogretmen": ad, "egitim": f"< {A.kesim}", "fon_gun_kesim_sonrasi": len(Pk), "fon_isaretlenme_%": pf * 100,
                    "gorulmemis_hisse_gun": len(Hk), "gorulmemis_isaretlenme_%": ph * 100, "ayirt_kat": pf / ph if ph > 0 else np.nan})
    out["ogr_kesim_tespit"] = pd.DataFrame(tes)
    # (b) tuttu mu: gorulmemis BIST yarisi + ABD; tam ogretmen 2016-26 ve kesim ogretmeni yalniz kesim sonrasi
    olay = []; taban = []; rng = np.random.default_rng(5)
    for pazar in ("BIST", "ABD"):
        for s, z in Z.get(pazar, {}).items():
            if pazar == "BIST" and (s in fon or _sm_yarim(s) == 0):
                continue
            d = V[pazar][s]; h = d.High.to_numpy(); l = d.Low.to_numpy(); c = d.Close.to_numpy(); n = len(c)
            bas_i = np.flatnonzero(z.index >= pd.Timestamp(A.olay_bas))
            if len(bas_i) == 0:
                continue
            Xs = z[OGR_KOL]
            for ad, (mm, es) in M.items():
                p = mm.predict_proba(Xs)[:, 1]
                uygun = (p >= es) & (z.index >= (kesim if ad.endswith("_kesim") else pd.Timestamp(A.olay_bas)))
                sec = []; son = -10 ** 9
                for i in np.flatnonzero(uygun):
                    if i - son >= A.tekrar and i + 20 < n:
                        sec.append(i); son = i
                if sec:
                    sec = np.array(sec); R = _sm_sonuclar_vek(h, l, c, sec)
                    olay.append(R.assign(ogretmen=ad, pazar=pazar, sembol=s, tarih=z.index[sec], i=sec, p=p[sec]))
            ti = np.arange(int(bas_i[0]), n - 20, A.tekrar)
            if len(ti):
                taban.append(_sm_sonuclar_vek(h, l, c, ti).assign(pazar=pazar, sembol=s, tarih=z.index[ti], i=ti))
    E = pd.concat(olay, ignore_index=True); T = pd.concat(taban, ignore_index=True)
    for t in (E, T):
        t["donem"] = np.where(pd.to_datetime(t.tarih) < pd.Timestamp(A.donem_siniri), "2016-21", "2022-26")
    T["kesim_sonrasi"] = pd.to_datetime(T.tarih) >= kesim
    olc = []
    for ad, sut, ret in (("alim", "y_k20", "r60"), ("alim", "y_x2", "r60"), ("satis", "y_dus20", "r20"),
                         ("alim_kesim", "y_k20", "r60"), ("satis_kesim", "y_dus20", "r20")):
        Ea = E[E.ogretmen == ad]
        gruplar = Ea.groupby(["pazar", "donem"]) if not ad.endswith("_kesim") else Ea.groupby(["pazar"])
        for key, g in gruplar:
            pz = key[0] if isinstance(key, tuple) else key
            dn = key[1] if isinstance(key, tuple) and len(key) > 1 else f">= {A.kesim}"
            t = T[(T.pazar == pz) & ((T.donem == dn) if not ad.endswith("_kesim") else T.kesim_sonrasi)]
            gg = g[g[sut].notna()]; tt = t[t[sut].notna()]
            olc.append({"ogretmen": ad, "sonuc": sut, "pazar": pz, "donem": dn, "n": len(gg), "isabet_%": gg[sut].mean() * 100,
                        "taban_isabet_%": tt[sut].mean() * 100, "kat": gg[sut].mean() / tt[sut].mean() if tt[sut].mean() > 0 else np.nan,
                        f"{ret}_medyan_%": gg[ret].median() * 100, f"taban_{ret}_medyan_%": tt[ret].median() * 100})
    out["ogr_tuttu_mu"] = pd.DataFrame(olc)
    # (c) alim izinden acilan islemler (uretim cikisi + maliyet) vs ayni hisselerin rastgele gunleri
    Vd = {**V.get("BIST", {}), **{("ABD:" + s): d for s, d in V.get("ABD", {}).items()}}
    Zd = {**Z.get("BIST", {}), **{("ABD:" + s): z for s, z in Z.get("ABD", {}).items()}}
    def _pref(df):
        df = df.copy(); df["sembol"] = np.where(df.pazar == "ABD", "ABD:" + df.sembol, df.sembol); return df
    isl = []
    Ea = _pref(E[E.ogretmen == "alim"]); Tb = _pref(T.sample(min(taban_ornek, len(T)), random_state=2))
    for ad, src in (("alim_izi", Ea), ("rastgele_gun", Tb)):
        I = sm_islemler(src, Vd, Zd, A)
        I["donem"] = np.where(pd.to_datetime(I.sinyal) < pd.Timestamp(A.donem_siniri), "2016-21", "2022-26")
        for (pz, dn), g in I.groupby(["pazar", "donem"]):
            isl.append({"secim": ad, "pazar": pz, "donem": dn, **sm_basari(g), "portfoy_%": sm_portfoy(g, A)["portfoy"]})
    out["ogr_islemler"] = pd.DataFrame(isl)
    out["ogr_olaylar"] = E
    return out


# ---------------------------------------------------------------- K7 rapor + ana akis
def _sm_veri(A: SMAyar):
    import FON_IZI as F
    FA = F.FIAyar(); V: Dict[str, Dict[str, pd.DataFrame]] = {}; Z: Dict[str, Dict[str, pd.DataFrame]] = {}
    for pazar, yol in FA.veri.items():
        try:
            V[pazar] = F.fi_k1_veri(yol, pazar, FA); Z[pazar] = sm_k2_panel(V[pazar], pazar, FA, A)
        except Exception as ex:
            smlog.error("%s verisi okunamadi (%s); atlandi", pazar, ex)
    return FA, V, Z


def _sm_kos(V, FA) -> pd.DataFrame:
    import FON_IZI as F
    yol = os.path.join(FA.cikti, "fon_kosular.csv")
    if os.path.exists(yol):
        return pd.read_csv(yol, parse_dates=["dip", "x2", "tepe"])
    return pd.DataFrame([{"sembol": s, **F.fi_kosu(V["BIST"][s], FA)} for s in F.FON_HISSE if s in V["BIST"]])


def _sm_md(baslik: str, t: pd.DataFrame, n: Optional[int] = None) -> List[str]:
    t = t.head(n) if n else t
    return [f"## {baslik}", "", t.round(3).to_markdown(index=False) if len(t) else "(bos)", ""]


def sm_ogretmen_calistir(A: Optional[SMAyar] = None, V=None, Z=None, FA=None) -> Dict[str, pd.DataFrame]:
    """K8: ogretmen; ciktilar arastirma_cikti/sessiz_ml/ogr_*.csv ve SESSIZ_ML_ogretmen.md."""
    A = A or SMAyar(); os.makedirs(A.cikti, exist_ok=True)
    if V is None:
        FA, V, Z = _sm_veri(A)
    if "BIST" not in Z:
        raise RuntimeError("BIST verisi yok; ogretmen fon hisselerinden ogrenir")
    R = sm_k8_ogretmen(V, Z, A, FA, _sm_kos(V, FA))
    for k, t in R.items():
        t.to_csv(os.path.join(A.cikti, k + (".csv.gz" if k == "ogr_olaylar" else ".csv")), index=False)
    sat = [f"# SESSIZ_ML ogretmen — {SM_SURUM}", "", f"Maliyet: komisyon %{A.komisyon*100:.1f} + kayma her yonde %{A.kayma*100:.1f} = islem basina %{A.maliyet*100:.1f}", ""]
    sat += _sm_md("1) Egitim kaniti (logloss ilk/son agac, model dosyasi)", R["ogr_kanit"])
    sat += _sm_md("2) Gormedigi veri: tarih kesimli ogretmen (kesim oncesiyle egitildi, sonrasinda fon hisselerini tanidi mi)", R["ogr_kesim_tespit"])
    sat += _sm_md("3a) Tuttu mu: iz goren hisselerde sonuc vs ayni hisselerin rastgele gunleri", R["ogr_tuttu_mu"])
    sat += _sm_md("3b) Alim izinden acilan islemler (uretim cikisi, maliyet dusulmus)", R["ogr_islemler"])
    sat += _sm_md("Ogretmenin gordugu: fon gunleri vs diger hisseler (ozellik medyanlari)", R["ogr_profil"])
    sat += _sm_md("Ogretmen ozellik onemi", R["ogr_onem"], 20)
    with open(os.path.join(A.cikti, "SESSIZ_ML_ogretmen.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(sat))
    return R


def sessiz_ml(A: Optional[SMAyar] = None, ogretmen: bool = True) -> Dict[str, Any]:
    import FON_IZI as F
    A = A or SMAyar(); os.makedirs(A.cikti, exist_ok=True)
    FA, V, Z = _sm_veri(A)
    if not Z:
        raise RuntimeError("hic veri yok")
    O = pd.concat([sm_k3_olaylar(V[p], Z[p], p, A) for p in Z], ignore_index=True)
    # K4 alis modelleri (egitim kaniti + model dosyalari)
    Ok20, imp_k20, esik_k20, kan1 = sm_ileri_egit(O, "y_k20", 90, A, ad="alis_k20")
    Ox2, imp_x2, _, kan2 = sm_ileri_egit(O, "y_x2", 365, A, ad="alis_x2")
    deg = pd.concat([sm_degerlendir(Ok20, "y_k20", A), sm_degerlendir(Ox2, "y_x2", A)], ignore_index=True)
    # K5 islemler: tum Z0 (test yillari), model ust %20 (egitim esigi), model alt
    P = Ok20[Ok20.p.notna()].copy(); P["yil"] = pd.to_datetime(P.tarih).dt.year
    P["ust"] = P.p >= P.esik_pz                     # v1.2: pazar bazinda egitim esigi (gercek zamanli)
    Vd = {**V.get("BIST", {}), **{("ABD:" + s): d for s, d in V.get("ABD", {}).items()}}
    Zd = {**Z.get("BIST", {}), **{("ABD:" + s): z for s, z in Z.get("ABD", {}).items()}}
    P["sembol"] = np.where(P.pazar == "ABD", "ABD:" + P.sembol, P.sembol)
    I_tum = sm_islemler(P, Vd, Zd, A)
    ust_harita = dict(zip(zip(P.sembol, pd.to_datetime(P.tarih)), P.ust))
    I_tum["ust"] = [bool(ust_harita.get((s_, pd.Timestamp(t_)), False)) for s_, t_ in zip(I_tum.sembol, I_tum.sinyal)]
    I_tum["donem"] = np.where(pd.to_datetime(I_tum.sinyal) < pd.Timestamp(A.donem_siniri), "2019-21", "2022-26")
    rng = np.random.default_rng(7); prt = []; bas = []
    for (pz, dn), g in I_tum.groupby(["pazar", "donem"]):
        u = g[g.ust]; al = g[~g.ust]
        rast = [sm_portfoy(g.sample(len(u), random_state=int(rng.integers(1e9))), A)["portfoy"] for _ in range(A.rastgele_tohum)] if len(u) else [np.nan]
        prt.append({"pazar": pz, "donem": dn, "secim": "tum_Z0", **sm_portfoy(g, A)})
        prt.append({"pazar": pz, "donem": dn, "secim": "model_ust20", **sm_portfoy(u, A), "rastgele_ayni_sayi_medyan": float(np.nanmedian(rast)),
                    "secilen_oran_yzd": 100.0 * len(u) / max(len(g), 1)})
        for ad, t in (("tum_Z0", g), ("model_ust20 (alis tahmini)", u), ("model_alt80", al)):
            bas.append({"pazar": pz, "donem": dn, "secim": ad, **sm_basari(t)})
    prt = pd.DataFrame(prt); bas = pd.DataFrame(bas)
    # K6 satis modeli
    S = sm_k6_satis_satirlari(I_tum, Vd, Zd, A)
    Sp, imp_sat, esik_sat, kan3 = sm_satis_puan(S, A)
    deg_sat = sm_degerlendir(Sp, "y_sat", replace(A, ust_oran=1 - A.sat_esik_q))
    PS: Dict[Any, np.ndarray] = {}
    # denetim 24 Eki: satis puani pozisyona ozgu (gun, kar, zirveden); eskiden hisse basina tek dizi, ust uste binen iki islemde
    # sonuncunun puani obur isleme yaziliyordu -> anahtar (sembol, giris_t)
    for (s, gt), g in Sp[Sp.p.notna()].groupby(["sembol", "giris_t"]):
        arr = np.full(len(Vd[s]), np.nan); arr[g.k.to_numpy()] = g.p.to_numpy(); PS[(s, pd.Timestamp(gt))] = arr
    I_ml = sm_islemler(P, Vd, Zd, A, PS, esik_sat)
    I_ml["donem"] = I_tum.donem.values; I_ml["ust"] = I_tum.ust.values
    cik = []
    for (pz, dn), g in I_tum.groupby(["pazar", "donem"]):
        ok = pd.to_datetime(g.sinyal).dt.year.isin(list(esik_sat)).to_numpy()
        g2 = I_ml.loc[g.index][ok]; g1 = g[ok]; ms = g2[g2.neden == "model"]
        cik.append({"pazar": pz, "donem": dn, "cikis": "uretim", **sm_portfoy(g1, A), **{k: v for k, v in sm_basari(g1).items() if k != "n"}})
        cik.append({"pazar": pz, "donem": dn, "cikis": "uretim+model", **sm_portfoy(g2, A), **{k: v for k, v in sm_basari(g2).items() if k != "n"},
                    "model_satis_n": len(ms), "dogru_satis_%": (ms.sonra20 < 0).mean() * 100 if len(ms) else np.nan,
                    "satis_sonrasi_20bar_medyan_%": ms.sonra20.median() * 100 if len(ms) else np.nan})
    cik = pd.DataFrame(cik)
    # sizinti kontrolu
    siz = sm_sizinti(O, A)
    kanit = pd.concat([kan1, kan2, kan3], ignore_index=True)
    # fon hisseleri 2026: satis modelinin ilk sinyali
    fon = []
    for s in F.FON_HISSE:
        ks = [k for k in PS if k[0] == s]
        if ks:
            p = pd.concat([pd.Series(PS[k], index=Vd[s].index) for k in ks], axis=1).max(axis=1).loc["2026-06-01":"2026-09-30"]
            yuk = p[p >= esik_sat.get(2026, np.inf)]
            fon.append({"sembol": s, "satis_puani_gun": int(p.notna().sum()), "ilk_sat_sinyali": yuk.index.min() if len(yuk) else None})
    fon = pd.DataFrame(fon)
    O.to_csv(os.path.join(A.cikti, "sm_olaylar.csv.gz"), index=False)
    Ok20[["pazar", "sembol", "tarih", "y_k20", "p"]].to_csv(os.path.join(A.cikti, "sm_alis_tahmin_k20.csv.gz"), index=False)
    I_tum.to_csv(os.path.join(A.cikti, "sm_islemler_uretim.csv.gz"), index=False)
    I_ml.to_csv(os.path.join(A.cikti, "sm_islemler_model_cikis.csv.gz"), index=False)
    for ad, t in (("sm_degerlendirme", deg), ("sm_portfoy", prt), ("sm_basari", bas), ("sm_cikis", cik), ("sm_onem_k20", imp_k20),
                  ("sm_onem_x2", imp_x2), ("sm_onem_satis", imp_sat), ("sm_satis_degerlendirme", deg_sat), ("sm_fon_2026", fon),
                  ("sm_egitim_kaniti", kanit), ("sm_sizinti", siz)):
        t.to_csv(os.path.join(A.cikti, ad + ".csv"), index=False)
    sat = [f"# SESSIZ_ML — {SM_SURUM}", "",
           f"Z0 olaylari: {len(O)} (BIST {int((O.pazar == 'BIST').sum())}, ABD {int((O.pazar == 'ABD').sum())}). "
           f"Maliyet: komisyon %{A.komisyon*100:.1f} + kayma her yonde %{A.kayma*100:.1f} = islem basina %{A.maliyet*100:.1f}.", ""]
    sat += _sm_md("1) Egitim kaniti (logloss: ilk/son agac, sabit tahmin kaybi, model dosyasi)", kanit)
    sat += _sm_md("2) Gormedigi veri: yil yil ileri yuruyen alis modeli (AUC, ust %20 kat)", deg)
    sat += _sm_md("3a) Alis basarisi: pozitif tahminlerden acilan islemler (maliyet dusulmus)", bas)
    sat += _sm_md("3b) Alis portfoyu (30 slot)", prt)
    sat += _sm_md("3c) Satis modeli (y_sat: 20 barda once -%10) ileri yuruyen degerlendirme", deg_sat)
    sat += _sm_md("3d) Satis basarisi: ayni girislerde uretim cikisi vs uretim + model satisi", cik)
    sat += _sm_md("4) Sizinti kontrolu (karistirilmis etiket ~0,5 olmali; gelecek kanaryasi sicramali)", siz)
    sat += _sm_md("Ozellik onemi — alis y_k20", imp_k20, 15)
    sat += _sm_md("Ozellik onemi — satis", imp_sat, 15)
    sat += _sm_md("Fon hisseleri 2026: satis modelinin ilk sat sinyali (Haz-Eyl)", fon)
    with open(os.path.join(A.cikti, "SESSIZ_ML_rapor.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(sat))
    R = {"olaylar": O, "deg": deg, "portfoy": prt, "basari": bas, "cikis": cik, "deg_sat": deg_sat, "imp_k20": imp_k20,
         "imp_sat": imp_sat, "fon": fon, "kanit": kanit, "sizinti": siz}
    if ogretmen:
        try:
            R["ogretmen"] = sm_ogretmen_calistir(A, V, Z, FA)
        except Exception as ex:
            smlog.error("ogretmen calismadi: %s", ex)
    return R


def _cakisma_kontrol_sm(_once=_CK_ONCE_SM, _dosya='SESSIZ_ML.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_SM', '_CK_KAYIT', '_cakisma_kontrol_sm', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'time', 'logging', 'warnings', 'replace', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass', 'field')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_sm()

if __name__ == "__main__" and "ogretmen" in sys.argv[1:]:
    R = sm_ogretmen_calistir()
    for k in ("ogr_kanit", "ogr_kesim_tespit", "ogr_tuttu_mu", "ogr_islemler"):
        print(k); print(R[k].round(3).to_string(index=False))
elif __name__ == "__main__":
    R = sessiz_ml()
    for k in ("kanit", "deg", "basari", "portfoy", "cikis", "sizinti"):
        print(k); print(R[k].round(3).to_string(index=False))
