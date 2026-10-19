# =====================================================================
#  GOZ_ESLE — "Kodun colu = Cemal'in gozundeki col" olcumu   (2026-10-19, v1.0)
#
#  SORU
#    1) Bugunku kod (COL_v1: col_segment / col_olc / uzun_col_olc) Cemal'in
#       gozle isaretledigi colleri nerede buluyor? Pencere ortusmesi (IoU).
#    2) Cemal'in col penceresini diger pencerelerden (ve onun 'col degil'
#       dediklerinden) hangi olculer ayiriyor? Makine ~50 olcuyu tarar.
#       Bir olcu ancak hisselerin cogunda AYNI YONDE ayiriyorsa iz sayilir.
#    3) Bu olculerle ogrenilen tespit, bir hisse disarida birakildiginda
#       o hissenin colunu geri buluyor mu, olumsuzlarda alarm veriyor mu?
#
#  GIRDI  (col_tarayici klasoru; Colab, yerel ya da GitHub Actions)
#    kalibre_etiketler.csv  sembol,bas,son,sinif(COL|OLUMSUZ)  — Cemal'in gozu
#    kalibre_veri.csv       tarih,sembol,Open,High,Low,Close,Volume
#    COL_v1.py              mevcut kod (ayri ad alaninda yuklenir; cakisma yok)
#
#  CIKTI  (cikti klasoru, varsayilan <K>/goz_esle/)
#    goz_kod_kiyas.csv      etiket basina kodun penceresi + IoU
#    goz_metrik_tarama.csv  olcu basina AUC, yon tutarliligi, olumsuz ayrimi
#    goz_model_loso.csv     etiket basina model tespiti (hisse disarida)
#    goz_model_tespitler.csv modelin tum tespitleri (Cemal'in bakacagi liste)
#    grafik_XX.png          her etiket: Cemal yesil, kod kirmizi, model mavi
#    GOZ_ESLE_rapor.md      ozet
#
#  KURAL_MOTORU
#    K1 veri+etiket denetimi  K2 kod pencereleri  K3 aday pencere + olcu
#    K4 olcu taramasi  K5 LOSO model  K6 grafik  K7 rapor
#    Her adim kendi hatasini loglar; kritik adim duserse program durur.
#
#  KULLANIM
#    Colab : exec(open('/content/drive/MyDrive/col_tarayici/GOZ_ESLE.py').read()); R=goz_esle()
#    Komut : python GOZ_ESLE.py --kok <klasor> [--cikti <klasor>]
# =====================================================================
from __future__ import annotations

import argparse
import bisect
import logging
import math
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

SURUM = "GOZ_ESLE v1.3 (2026-10-19: bolge ince ayar + doji)"
glog = logging.getLogger("col.goz")
if not glog.handlers:
    _h = logging.StreamHandler(sys.stderr)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s goz: %(message)s", "%H:%M:%S"))
    glog.addHandler(_h)
    glog.setLevel(logging.INFO)
    glog.propagate = False


@dataclass
class GozAyar:
    kok: str = "/content/drive/MyDrive/col_tarayici"
    cikti: Optional[str] = None
    veri_csv: str = "kalibre_veri.csv"
    etiket_csv: str = "kalibre_etiketler.csv"
    kod_dosya: str = "COL_v1.py"
    # aday pencere izgarasi
    uzunluklar: Tuple[int, ...] = (12, 16, 20, 25, 30, 35, 40, 50, 60, 70, 80, 100, 120)
    adim: int = 2                      # pencere sonu her 'adim' barda bir
    min_once: int = 60                 # pencere oncesi en az bar (ATR, baglam)
    # etiketleme
    iou_poz: float = 0.5               # >= bu IoU: Cemal'in colu
    iou_neg: float = 0.1               # < bu IoU (her COL etiketiyle): col degil
    # tarama esikleri (iz sayilma)
    iz_auc: float = 0.70
    iz_tutarlilik: float = 0.80
    # v1.1 BUYUK MUM KAPISI (Cemal 19 Eki: "%10 dev mum cole dahil olamaz")
    #   bir barda (H-L)/onceki kapanis >= buyuk_aralik (%) ya da |kapanis degisimi| >= buyuk_degisim (%)
    #   -> buyuk mum. Icinde buyuk mum olan pencere col DEGILDIR (puanlanmaz).
    #   Cemal'in Eylul etiketleri buyuk mumsuz en uzun parcaya kirpilir; kirpik < min_kirpik bar ise etiket duser.
    #   v1.2 (23:05): tek buyuk mum colu bozmaz (Cemal: bolgeye geri donuyorsa col); varsayilan KAPALI,
    #   yerine BOLGE KURALI (asagida). Esik tarama icin --buyuk-aralik/--buyuk-degisim ile acilir.
    buyuk_aralik: Optional[float] = None
    buyuk_degisim: Optional[float] = None
    min_kirpik: int = 10
    # v1.2 BOLGE KURALI (Cemal 19 Eki 23:03): col = fiyat bolgeden ayrilmiyor + zamanla pespese kucuk mumlar;
    #   pespese buyuk mumla fiyat bolgeden ayriliyorsa col orada biter. Olcu hisseye ozel (23:04):
    #   ref = son 250 barin medyan gun araligi (H-L / onceki kapanis, %).
    #   buyuk mum: aralik >= bolge_buyuk_kat x ref ya da |kapanis degisimi| >= 0.9 x bolge_buyuk_kat x ref
    #   bant: kapanislarin (max-min)/medyan <= bolge_bant_kat x ref  (fitiller bolgeyi bozmaz)
    bolge_bant_kat: float = 6.0          # v1.3: cekirdek (%10-%90 kapanis) bandi
    bolge_uzak_kat: float = 1.5          # v1.3: cekirdekten bu kadar ref otesi kapanis = COK ayrilma
    bolge_sol_kat: float = 1.5           # v1.3: bastaki bu kadar ref'ten buyuk mumlar kirpilir (inis mumlari)
    bolge_buyuk_kat: float = 2.0
    bolge_ardisik: int = 3
    bolge_min_bar: int = 15
    bolge_en_cok: int = 250
    # model
    nms_iou: float = 0.3
    esik_olasilik: float = 0.5
    rastgele: int = 42


# ------------------------------------------------------------------ yardimcilar
def iou(a0: int, a1: int, b0: int, b1: int) -> float:
    """Kapali bar araliklari [a0,a1] ve [b0,b1] icin ortusme / birlesim."""
    k = min(a1, b1) - max(a0, b0) + 1
    if k <= 0:
        return 0.0
    return k / float((a1 - a0 + 1) + (b1 - b0 + 1) - k)


def _tr(H: np.ndarray, L: np.ndarray, C: np.ndarray) -> np.ndarray:
    pc = np.roll(C, 1)
    pc[0] = C[0]
    return np.maximum(H - L, np.maximum(np.abs(H - pc), np.abs(L - pc)))


def _egim_r2(y: np.ndarray) -> Tuple[float, float]:
    n = len(y)
    if n < 3 or not np.isfinite(y).all():
        return np.nan, np.nan
    x = np.arange(n, dtype=float)
    xm, ym = x.mean(), y.mean()
    sxx = ((x - xm) ** 2).sum()
    b = ((x - xm) * (y - ym)).sum() / sxx
    yh = ym + b * (x - xm)
    sst = ((y - ym) ** 2).sum()
    r2 = 1 - ((y - yh) ** 2).sum() / sst if sst > 0 else np.nan
    return float(b), float(r2)


def _artik_std(y: np.ndarray) -> float:
    n = len(y)
    if n < 3:
        return np.nan
    x = np.arange(n, dtype=float)
    b, a = np.polyfit(x, y, 1)
    return float(np.std(y - (a + b * x)))


def _auc(poz: np.ndarray, neg: np.ndarray) -> float:
    """Mann-Whitney AUC; NaN'lar atilir."""
    poz = poz[np.isfinite(poz)]
    neg = neg[np.isfinite(neg)]
    if len(poz) < 3 or len(neg) < 3:
        return np.nan
    from scipy.stats import rankdata
    r = rankdata(np.concatenate([poz, neg]))
    u = r[: len(poz)].sum() - len(poz) * (len(poz) + 1) / 2
    return float(u / (len(poz) * len(neg)))


def buyuk_mum(df: pd.DataFrame, ay: "GozAyar") -> np.ndarray:
    """v1.1: bar basina buyuk mum bayragi. Olcu onceki kapanisa gore %:
    gun araligi (H-L) >= buyuk_aralik  VEYA  |kapanis degisimi| >= buyuk_degisim. Ilk bar: acilisa gore."""
    pc = df.Close.shift(1).fillna(df.Open).to_numpy(float)
    H, L, C = df.High.to_numpy(float), df.Low.to_numpy(float), df.Close.to_numpy(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        ar = 100 * (H - L) / pc
        dg = 100 * np.abs(C / pc - 1)
    b = np.zeros(len(df), bool)
    if ay.buyuk_aralik is not None:
        b |= np.nan_to_num(ar, nan=0.0) >= ay.buyuk_aralik
    if ay.buyuk_degisim is not None:
        b |= np.nan_to_num(dg, nan=0.0) >= ay.buyuk_degisim
    return b


def bolge_hazirla(df: pd.DataFrame) -> Dict[str, np.ndarray]:
    """BOLGE KURALI icin bar dizileri: kapanis, gun araligi %, kapanis degisimi %, hisseye ozel ref, govde orani."""
    O, H, L, C = (df[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    pc = np.r_[O[0], C[:-1]]
    with np.errstate(divide="ignore", invalid="ignore"):
        ar = 100 * (H - L) / pc
        dg = 100 * (C / pc - 1)
    ref = pd.Series(ar).rolling(250, min_periods=120).median().to_numpy()
    rng = H - L
    go = np.where(rng > 0, np.abs(C - O) / np.where(rng > 0, rng, 1), 1.0)
    return {"C": C, "H": H, "L": L, "ar": ar, "dg": dg, "ref": ref, "go": go}


def bolge_col(D: Dict[str, np.ndarray], e: int, ay: "GozAyar") -> Optional[Tuple[int, int]]:
    """v1.3 (Cemal 19 Eki 23:28 ince ayar). e gununde biten col penceresi (s, e) ya da None.
    Geriye dogru buyur; cekirdek = kapanislarin %10-%90 araligi (her adimda guncellenir). Durur:
      (a) cekirdek bandi > bolge_bant_kat x ref                      -> bolge genisledi
      (b) bir kapanis cekirdegin bolge_uzak_kat x ref otesinde       -> COK ayrilma (az ayrilma kabul)
      (c) bolge_ardisik kadar pespese ayni yonlu buyuk mum           -> buyuk mumla ayrilma
    SOL KIRPMA: bolgenin basindaki, gun araligi > bolge_sol_kat x ref olan ya da kapanisi
    cekirdek disinda kalan barlar atilir (bolgeye inis mumlari cole dahil edilmez)."""
    C, ar, dg, ref = D["C"], D["ar"], D["dg"], D["ref"]
    r = ref[e]
    if not np.isfinite(r) or r <= 0 or not np.isfinite(C[e]):
        return None
    buyuk = ay.bolge_buyuk_kat * r
    s, seri, yon = e, 0, 0
    srt = [float(C[e])]                     # siralı kapanislar (bisect) — np.percentile ile ayni sonuc, hizli

    def _yuzde(a: List[float], q: float) -> float:
        k = (len(a) - 1) * q
        f = int(k)
        return a[f] + (a[min(f + 1, len(a) - 1)] - a[f]) * (k - f)

    for j in range(e - 1, max(-1, e - ay.bolge_en_cok), -1):
        if not np.isfinite(C[j]):
            break
        if ar[j] >= buyuk or abs(dg[j]) >= 0.9 * buyuk:
            y = 1 if dg[j] > 0 else -1
            seri = seri + 1 if (seri and y == yon) else 1
            yon = y
            if seri >= ay.bolge_ardisik:
                s = max(s, j + ay.bolge_ardisik)
                break
        else:
            seri = 0
        bisect.insort(srt, float(C[j]))
        lo, hi, med = _yuzde(srt, 0.10), _yuzde(srt, 0.90), _yuzde(srt, 0.50)
        if (hi - lo) / med * 100 > ay.bolge_bant_kat * r:
            break
        tol = ay.bolge_uzak_kat * r / 100 * med
        if C[j] > hi + tol or C[j] < lo - tol:
            break
        s = j
    z = C[s:e + 1]
    lo, hi = np.percentile(z, 10), np.percentile(z, 90)
    while s < e and (ar[s] > ay.bolge_sol_kat * r or C[s] > hi or C[s] < lo):
        s += 1
    return (s, e) if e - s + 1 >= ay.bolge_min_bar else None


def bolge_doji(D: Dict[str, np.ndarray], s: int, e: int, esik: float = 0.10) -> Dict[str, float]:
    """Bolgedeki doji orani ve hissenin kendi normaline (bolge oncesi 250 bar) gore kati."""
    go = D["go"]
    d = go[s:e + 1] < esik
    d0 = go[max(0, s - 250):s] < esik
    return {"doji": float(d.mean()),
            "doji_kat": float(d.mean() / d0.mean()) if len(d0) >= 60 and d0.mean() > 0 else np.nan}


# ------------------------------------------------------------------ K1
def k1_veri(ay: GozAyar) -> Tuple[Dict[str, pd.DataFrame], pd.DataFrame]:
    yv = os.path.join(ay.kok, ay.veri_csv)
    ye = os.path.join(ay.kok, ay.etiket_csv)
    for y in (yv, ye):
        if not os.path.exists(y):
            raise FileNotFoundError(f"K1: {y} yok")
    v = pd.read_csv(yv, parse_dates=["tarih"])
    eksik = {"tarih", "sembol", "Open", "High", "Low", "Close", "Volume"} - set(v.columns)
    if eksik:
        raise ValueError(f"K1: veri sutunu eksik: {eksik}")
    veri: Dict[str, pd.DataFrame] = {}
    for s, g in v.groupby("sembol"):
        d = g.drop(columns="sembol").set_index("tarih").sort_index()
        d = d[~d.index.duplicated(keep="last")].dropna(subset=["Close"])
        d = d[(d.High >= d.Low)]
        if len(d) >= 120:
            veri[str(s)] = d.astype(float)
    e = pd.read_csv(ye, parse_dates=["bas", "son"])
    e["sinif"] = e.sinif.str.upper().str.strip()
    e = e[e.sinif.isin(["COL", "OLUMSUZ"])].reset_index(drop=True)
    e["veri_var"] = e.sembol.isin(veri.keys())
    for c in ("bi", "si"):
        e[c] = -1
    for i, r in e.iterrows():
        if not r.veri_var:
            continue
        ix = veri[r.sembol].index
        b = int(ix.searchsorted(r.bas))
        s = int(ix.searchsorted(r.son, side="right")) - 1
        e.loc[i, "bi"], e.loc[i, "si"] = b, s
    yok = e[~e.veri_var]
    if len(yok):
        glog.warning("K1: veride olmayan etiket: %s", ", ".join(yok.sembol))
    e = e[e.veri_var & (e.si > e.bi)].reset_index(drop=True)
    e["etiket_id"] = [f"{r.sembol}_{r.bas:%Y%m%d}" for r in e.itertuples()]
    # v1.1: buyuk mum kapisi -> Eylul etiketlerini buyuk mumsuz en uzun parcaya kirp
    e["bi0"], e["si0"] = e.bi, e.si
    e["buyuk_mum_sayi"] = 0
    e["kirpik_durum"] = "kapi yok"
    if ay.buyuk_aralik is not None or ay.buyuk_degisim is not None:
        dus = []
        for i, r in e.iterrows():
            b = buyuk_mum(veri[r.sembol], ay)
            ic = b[int(r.bi):int(r.si) + 1]
            e.loc[i, "buyuk_mum_sayi"] = int(ic.sum())
            if not ic.any():
                e.loc[i, "kirpik_durum"] = "temiz"
                continue
            en, en_b, k, kb = 0, 0, 0, 0
            for j, v in enumerate(ic):
                if v:
                    k = 0
                    continue
                if k == 0:
                    kb = j
                k += 1
                if k > en:
                    en, en_b = k, kb
            if en < ay.min_kirpik:
                e.loc[i, "kirpik_durum"] = f"dustu (buyuk mumsuz en uzun parca {en} bar)"
                dus.append(i)
                continue
            e.loc[i, "bi"] = int(r.bi) + en_b
            e.loc[i, "si"] = int(r.bi) + en_b + en - 1
            e.loc[i, "kirpik_durum"] = f"kirpildi {int(r.si0 - r.bi0 + 1)}->{en} bar"
        if dus:
            glog.warning("K1: buyuk mum kapisindan sonra %d etiket dustu: %s", len(dus),
                         ", ".join(e.loc[dus, "etiket_id"]))
        dusen_df = e.loc[dus].copy()
        e = e.drop(index=dus).reset_index(drop=True)
        e.attrs["dusen"] = dusen_df
        glog.info("K1: buyuk mum kapisi aralik>=%s%% / degisim>=%s%%: temiz %d, kirpildi %d, dustu %d",
                  ay.buyuk_aralik, ay.buyuk_degisim, int((e.kirpik_durum == "temiz").sum()),
                  int(e.kirpik_durum.str.startswith("kirpildi").sum()), len(dus))
    glog.info("K1: %d hisse, %d etiket (COL %d, OLUMSUZ %d)", len(veri), len(e),
              int((e.sinif == "COL").sum()), int((e.sinif == "OLUMSUZ").sum()))
    return veri, e


# ------------------------------------------------------------------ K2
def k2_kod_pencereleri(ay: GozAyar, veri: Dict[str, pd.DataFrame], e: pd.DataFrame) -> pd.DataFrame:
    """COL_v1'i ayri ad alaninda yukler; her etiketin son gununde kodun penceresi."""
    yol = os.path.join(ay.kok, ay.kod_dosya)
    ns: Dict[str, Any] = {"__name__": "col_v1_goz"}
    try:
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(open(yol, encoding="utf-8").read(), yol, "exec"), ns)
    except Exception as ex:
        raise RuntimeError(f"K2: {ay.kod_dosya} yuklenemedi: {ex}") from ex
    for ad in ("col_segment", "col_olc", "uzun_col_olc"):
        if ad not in ns:
            raise RuntimeError(f"K2: {ay.kod_dosya} icinde {ad} yok")
    satir = []
    for r in e.itertuples():
        df = veri[r.sembol]
        ix = df.index
        kayit: Dict[str, Any] = {"etiket_id": r.etiket_id, "sembol": r.sembol, "sinif": r.sinif,
                                 "cemal_bas": str(r.bas.date()), "cemal_son": str(r.son.date()),
                                 "cemal_uz": int(r.si - r.bi + 1)}
        try:
            seg = ns["col_segment"](df, tarih=ix[r.si])
        except Exception as ex:
            glog.debug("%s col_segment: %s", r.etiket_id, ex)
            seg = None
        try:
            olc = ns["col_olc"](df, tarih=ix[r.si])
        except Exception as ex:
            glog.debug("%s col_olc: %s", r.etiket_id, ex)
            olc = None
        try:
            uz = ns["uzun_col_olc"](df, tarih=ix[r.si])
        except Exception as ex:
            glog.debug("%s uzun_col_olc: %s", r.etiket_id, ex)
            uz = None
        if seg:
            kb = int(ix.searchsorted(pd.Timestamp(seg["bas_tarih"])))
            ks = int(ix.searchsorted(pd.Timestamp(seg["son_tarih"]), side="right")) - 1
            kayit.update(kod_bas=seg["bas_tarih"], kod_son=seg["son_tarih"], kod_uz=int(seg["uzunluk"]),
                         kod_taban=seg["taban"], kod_tavan=seg["tavan"], kod_yuk_atr=seg["yukseklik_atr"],
                         kod_iou=round(iou(kb, ks, int(r.bi), int(r.si)), 3),
                         bas_fark_bar=int(kb - r.bi))
        else:
            kayit.update(kod_bas=None, kod_son=None, kod_uz=0, kod_taban=np.nan, kod_tavan=np.nan,
                         kod_yuk_atr=np.nan, kod_iou=0.0, bas_fark_bar=np.nan)
        kayit["kod_aday"] = bool(olc) and bool(olc.get("aday", True)) if isinstance(olc, dict) else False
        kayit["uzun_col"] = (uz or {}).get("uzun", "") if isinstance(uz, dict) else ""
        # v1.2 BOLGE KURALI: Cemal'in (kirpilmamis) isaretinin son gununde
        try:
            bw = bolge_col(bolge_hazirla(df), int(r.si0), ay)
        except Exception as ex:
            glog.debug("%s bolge_col: %s", r.etiket_id, ex)
            bw = None
        kayit["bolge_bas_i"], kayit["bolge_son_i"] = (bw if bw else (-1, -1))
        kayit["bolge_uz"] = (bw[1] - bw[0] + 1) if bw else 0
        kayit["bolge_iou"] = round(iou(bw[0], bw[1], int(r.bi0), int(r.si0)), 3) if bw else 0.0
        if bw:                                                    # v1.3: doji (hissenin kendi normaline gore)
            kayit.update({f"bolge_{k_}": round(v_, 3) for k_, v_ in bolge_doji(bolge_hazirla(df), *bw).items()})
        if not seg:
            kayit["kod_durum"] = "segment yok"
        elif kayit["kod_iou"] >= 0.5:
            kayit["kod_durum"] = "eslesti"
        elif kayit["bas_fark_bar"] > 0:
            kayit["kod_durum"] = "kisa (gec basladi)"
        else:
            kayit["kod_durum"] = "uzun/kaymis"
        satir.append(kayit)
    t = pd.DataFrame(satir)
    c = t[t.sinif == "COL"]
    glog.info("K2: kod COL etiketlerinde: eslesti %d/%d | segment yok %d | aday %d",
              int((c.kod_iou >= 0.5).sum()), len(c), int((c.kod_durum == "segment yok").sum()),
              int(c.kod_aday.sum()))
    o = t[t.sinif == "OLUMSUZ"]
    glog.info("K2: BOLGE KURALI (bant %gx, buyuk %gx, pespese %d): COL eslesti %d/%d (ort ortusme %.2f) | "
              "OLUMSUZ'da bolge var %d/%d", ay.bolge_bant_kat, ay.bolge_buyuk_kat, ay.bolge_ardisik,
              int((c.bolge_iou >= 0.5).sum()), len(c), float(c.bolge_iou.mean()),
              int((o.bolge_uz > 0).sum()), len(o))
    return t


# ------------------------------------------------------------------ K3
@dataclass
class Dizi:
    ix: pd.DatetimeIndex
    O: np.ndarray
    H: np.ndarray
    L: np.ndarray
    C: np.ndarray
    V: np.ndarray
    TR: np.ndarray
    sma50: np.ndarray
    sma200: np.ndarray


def _dizi(df: pd.DataFrame) -> Dizi:
    O, H, L, C, V = (df[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    cs = df.Close
    return Dizi(df.index, O, H, L, C, V, _tr(H, L, C),
                cs.rolling(50, min_periods=50).mean().to_numpy(float),
                cs.rolling(200, min_periods=200).mean().to_numpy(float))


OLCU_ACIKLAMA: Dict[str, str] = {
    "uz": "pencere uzunlugu (bar)",
    "bant_pct": "bant: (en yuksek - en dusuk) / medyan fiyat",
    "bant_govde_pct": "govde bandi (fitilsiz) / medyan fiyat",
    "bant_kap_pct": "kapanislarin %5-%95 bandi / medyan fiyat",
    "aralik_ort_pct": "ortalama gun araligi H-L / fiyat",
    "aralik_med_pct": "medyan gun araligi H-L / fiyat",
    "kucuk_mum_once": "H-L <= 0.65 x onceki ATR30 olan bar orani (D7 tanimi)",
    "kucuk_mum_kendi": "H-L <= 0.65 x pencere oncesi 60 bar medyan araligi olan bar orani",
    "govde_ort_pct": "ortalama govde |C-O| / fiyat",
    "doji_oran": "|C-O|/(H-L) < 0.15 olan bar orani",
    "ust_fitil_atr": "ortalama ust fitil / pencere ATR",
    "alt_fitil_atr": "ortalama alt fitil / pencere ATR",
    "fitil_asimetri": "ust fitil - alt fitil (ATR)",
    "atr_daralma30": "pencere ATR / onceki 30 bar ATR",
    "atr_daralma120": "pencere ATR / onceki 120 bar ATR",
    "egim_pct_gun": "kapanis egimi, % / gun",
    "egim_abs": "egim mutlak degeri",
    "trend_r2": "kapanis dogrusal trend R2",
    "verim": "Kaufman verimi |net| / toplam yol",
    "chop": "choppiness endeksi (yuksek = yatay)",
    "ust_kenar_sapma": "tepelerin dogrudan sapmasi / ATR (dusuk = duzgun tavan)",
    "alt_kenar_sapma": "diplerin dogrudan sapmasi / ATR (dusuk = duzgun taban)",
    "kenar_budama": "min(ust,alt sapma)/max — bir kenar budanmis, digeri pruzlu",
    "ust_kenar_egim": "tepe cizgisi egimi, % / gun",
    "alt_kenar_egim": "dip cizgisi egimi, % / gun",
    "kenar_yakinsama": "ust egim - alt egim (negatif = daralan ucgen)",
    "tavan_dokunus": "en yuksege 0.3 ATR yakin bar orani",
    "taban_dokunus": "en dusuge 0.3 ATR yakin bar orani",
    "dip_yakin120": "pencere dibi / onceki 120 bar dibi - 1",
    "onceki_dusus120": "onceki 120 bar tepesinden pencere medyanina dusus",
    "onceki_getiri60": "pencere basina kadar 60 bar getiri",
    "konum_tum": "pencere medyani, onceki tum gecmisin (min..max) neresinde",
    "sma50_uzak": "son kapanis / SMA50 - 1",
    "sma50_egim": "SMA50 egimi (20 bar), %",
    "sma200_uzak": "son kapanis / SMA200 - 1",
    "sma200_yakin_oran": "kapanislarin SMA200 +-%10 icinde olma orani",
    "sma50_ustu_oran": "kapanislarin SMA50 ustunde olma orani",
    "hacim_daralma": "pencere hacmi / onceki 60 bar hacmi",
    "hacim_cv": "hacim degiskenlik katsayisi",
    "getiri_std": "gunluk getiri std (%)",
    "getiri_std_daralma": "getiri std / onceki 60 bar",
    "max_hareket_atr": "en buyuk gunluk kapanis degisimi / onceki ATR",
    "buyuk_mum_oran": "H-L > 1.5 x onceki ATR olan bar orani",
    "yeni_dip_sayi": "ilk 5 bardan sonra yeni pencere dibi yapan bar orani",
    "yeni_tepe_sayi": "ilk 5 bardan sonra yeni pencere tepesi yapan bar orani",
    "gap_oran": "acilis bosluklu (> 0.5 ATR) bar orani",
    "orta_kapanis_oran": "kapanislarin bandin orta %50'sinde olma orani",
    "clv_ort": "ortalama kapanis konumu (-1 dip, +1 tepe)",
    "yesil_oran": "yesil mum orani",
    "son_ardisik_kucuk": "sondaki ardisik kucuk mum sayisi",
    "son10_aralik_oran": "son 10 bar araligi / pencere araligi (sikisma sonu)",
    "yari_bant_oran": "ikinci yari bandi / ilk yari bandi",
    "yari_seviye": "ikinci yari medyani / ilk yari medyani - 1",
    "otokor1": "gunluk getirilerin 1 gecikmeli otokorelasyonu",
}
OLCULER: List[str] = list(OLCU_ACIKLAMA.keys())


def pencere_olc(d: Dizi, s: int, e: int) -> Dict[str, float]:
    """[s,e] penceresi icin olculer. Yalniz e'ye kadarki veri kullanilir (ileriye bakis yok)."""
    O, H, L, C, V, TR = d.O[s:e + 1], d.H[s:e + 1], d.L[s:e + 1], d.C[s:e + 1], d.V[s:e + 1], d.TR[s:e + 1]
    n = e - s + 1
    P = float(np.median(C))
    atr_w = float(TR.mean())
    atr30 = float(d.TR[max(0, s - 30):s].mean()) if s >= 10 else np.nan
    atr120 = float(d.TR[max(0, s - 120):s].mean()) if s >= 30 else np.nan
    rng = H - L
    govde = np.abs(C - O)
    gu, ga = np.maximum(O, C), np.minimum(O, C)
    r: Dict[str, float] = {"uz": float(n)}
    if P <= 0 or atr_w <= 0:
        return r
    hi, lo = float(H.max()), float(L.min())
    r["bant_pct"] = (hi - lo) / P
    r["bant_govde_pct"] = (float(gu.max()) - float(ga.min())) / P
    r["bant_kap_pct"] = (float(np.percentile(C, 95)) - float(np.percentile(C, 5))) / P
    r["aralik_ort_pct"] = float(rng.mean()) / P
    r["aralik_med_pct"] = float(np.median(rng)) / P
    r["kucuk_mum_once"] = float((rng <= 0.65 * atr30).mean()) if np.isfinite(atr30) and atr30 > 0 else np.nan
    med60 = float(np.median(d.H[max(0, s - 60):s] - d.L[max(0, s - 60):s])) if s >= 20 else np.nan
    r["kucuk_mum_kendi"] = float((rng <= med60).mean()) if np.isfinite(med60) and med60 > 0 else np.nan
    r["govde_ort_pct"] = float(govde.mean()) / P
    ok = rng > 0
    r["doji_oran"] = float((govde[ok] / rng[ok] < 0.15).mean()) if ok.sum() >= 5 else np.nan
    r["ust_fitil_atr"] = float((H - gu).mean()) / atr_w
    r["alt_fitil_atr"] = float((ga - L).mean()) / atr_w
    r["fitil_asimetri"] = r["ust_fitil_atr"] - r["alt_fitil_atr"]
    r["atr_daralma30"] = atr_w / atr30 if np.isfinite(atr30) and atr30 > 0 else np.nan
    r["atr_daralma120"] = atr_w / atr120 if np.isfinite(atr120) and atr120 > 0 else np.nan
    b, r2 = _egim_r2(C)
    r["egim_pct_gun"] = 100 * b / P if np.isfinite(b) else np.nan
    r["egim_abs"] = abs(r["egim_pct_gun"]) if np.isfinite(r["egim_pct_gun"]) else np.nan
    r["trend_r2"] = r2
    yol = float(np.abs(np.diff(C)).sum())
    r["verim"] = abs(float(C[-1] - C[0])) / yol if yol > 0 else np.nan
    r["chop"] = 100 * math.log10(float(TR.sum()) / (hi - lo)) / math.log10(n) if hi > lo and n > 1 else np.nan
    us, as_ = _artik_std(H), _artik_std(L)
    r["ust_kenar_sapma"] = us / atr_w
    r["alt_kenar_sapma"] = as_ / atr_w
    mx = max(us, as_)
    r["kenar_budama"] = min(us, as_) / mx if mx > 0 else np.nan
    bh, _ = _egim_r2(H)
    bl, _ = _egim_r2(L)
    r["ust_kenar_egim"] = 100 * bh / P
    r["alt_kenar_egim"] = 100 * bl / P
    r["kenar_yakinsama"] = r["ust_kenar_egim"] - r["alt_kenar_egim"]
    r["tavan_dokunus"] = float((H >= hi - 0.3 * atr_w).mean())
    r["taban_dokunus"] = float((L <= lo + 0.3 * atr_w).mean())
    if s >= 30:
        onl = d.L[max(0, s - 120):s]
        onh = d.H[max(0, s - 120):s]
        r["dip_yakin120"] = lo / float(onl.min()) - 1
        r["onceki_dusus120"] = P / float(onh.max()) - 1
    if s >= 60:
        r["onceki_getiri60"] = float(d.C[s - 1] / d.C[s - 60] - 1)
    if s >= 60:
        tl, th = float(d.L[:s].min()), float(d.H[:s].max())
        r["konum_tum"] = (P - tl) / (th - tl) if th > tl else np.nan
    s50, s200 = d.sma50[s:e + 1], d.sma200[s:e + 1]
    if np.isfinite(d.sma50[e]):
        r["sma50_uzak"] = float(C[-1] / d.sma50[e] - 1)
        if e >= 20 and np.isfinite(d.sma50[e - 20]):
            r["sma50_egim"] = float(d.sma50[e] / d.sma50[e - 20] - 1)
        m = np.isfinite(s50)
        r["sma50_ustu_oran"] = float((C[m] > s50[m]).mean()) if m.sum() >= 5 else np.nan
    if np.isfinite(d.sma200[e]):
        r["sma200_uzak"] = float(C[-1] / d.sma200[e] - 1)
        m = np.isfinite(s200)
        r["sma200_yakin_oran"] = float((np.abs(C[m] / s200[m] - 1) <= 0.10).mean()) if m.sum() >= 5 else np.nan
    if s >= 60:
        v0 = float(np.nanmean(d.V[s - 60:s]))
        r["hacim_daralma"] = float(np.nanmean(V)) / v0 if v0 > 0 else np.nan
    vm = float(np.nanmean(V))
    r["hacim_cv"] = float(np.nanstd(V)) / vm if vm > 0 else np.nan
    ret = np.diff(np.log(np.maximum(C, 1e-9)))
    r["getiri_std"] = 100 * float(ret.std()) if len(ret) > 2 else np.nan
    if s >= 61:
        r0 = np.diff(np.log(np.maximum(d.C[s - 61:s], 1e-9)))
        r["getiri_std_daralma"] = float(ret.std() / r0.std()) if r0.std() > 0 and len(ret) > 2 else np.nan
    if np.isfinite(atr30) and atr30 > 0:
        r["max_hareket_atr"] = float(np.abs(np.diff(C)).max()) / atr30 if n > 1 else np.nan
        r["buyuk_mum_oran"] = float((rng > 1.5 * atr30).mean())
        pc = d.C[s - 1:e] if s >= 1 else np.r_[C[0], C[:-1]]
        r["gap_oran"] = float((np.abs(O - pc) > 0.5 * atr30).mean())
    if n > 6:
        cl = np.minimum.accumulate(L)
        ch = np.maximum.accumulate(H)
        r["yeni_dip_sayi"] = float((L[5:] < cl[4:-1]).mean())
        r["yeni_tepe_sayi"] = float((H[5:] > ch[4:-1]).mean())
    q1, q3 = lo + 0.25 * (hi - lo), lo + 0.75 * (hi - lo)
    r["orta_kapanis_oran"] = float(((C >= q1) & (C <= q3)).mean())
    clv = np.where(rng > 0, ((C - L) - (H - C)) / np.where(rng > 0, rng, 1), 0.0)
    r["clv_ort"] = float(clv.mean())
    r["yesil_oran"] = float((C > O).mean())
    if np.isfinite(atr30) and atr30 > 0:
        kc = rng <= 0.65 * atr30
        k = 0
        for v_ in kc[::-1]:
            if not v_:
                break
            k += 1
        r["son_ardisik_kucuk"] = float(k)
    r["son10_aralik_oran"] = float(rng[-10:].mean() / rng.mean()) if n >= 15 and rng.mean() > 0 else np.nan
    h2 = n // 2
    if h2 >= 5:
        b1 = float(H[:h2].max() - L[:h2].min())
        b2 = float(H[h2:].max() - L[h2:].min())
        r["yari_bant_oran"] = b2 / b1 if b1 > 0 else np.nan
        r["yari_seviye"] = float(np.median(C[h2:]) / np.median(C[:h2]) - 1)
    if len(ret) > 5 and ret.std() > 0:
        r["otokor1"] = float(np.corrcoef(ret[:-1], ret[1:])[0, 1])
    return r


def k3_pencereler(ay: GozAyar, veri: Dict[str, pd.DataFrame], e: pd.DataFrame) -> pd.DataFrame:
    t0 = time.monotonic()
    col = e[e.sinif == "COL"]
    olm = e[e.sinif == "OLUMSUZ"]
    satir: List[Dict[str, Any]] = []
    atlanan = 0
    for s_ad, df in veri.items():
        d = _dizi(df)
        n = len(df)
        kapi = ay.buyuk_aralik is not None or ay.buyuk_degisim is not None
        bk = np.concatenate([[0], np.cumsum(buyuk_mum(df, ay))]) if kapi else None
        ecol = [(int(r.bi), int(r.si), r.etiket_id) for r in col[col.sembol == s_ad].itertuples()]
        eolm = [(int(r.bi), int(r.si), r.etiket_id) for r in olm[olm.sembol == s_ad].itertuples()]
        sonlar = set(range(ay.min_once + min(ay.uzunluklar), n, ay.adim))
        for b0, b1, _ in ecol + eolm:          # etiketin tam kendisi de aday olsun
            sonlar.add(b1)
        for en in sorted(sonlar):
            for uz in ay.uzunluklar:
                st = en - uz + 1
                if st < ay.min_once:
                    continue
                if bk is not None and bk[en + 1] - bk[st] > 0:
                    atlanan += 1
                    continue          # v1.1 kapi: icinde buyuk mum var -> col degil, puanlanmaz
                try:
                    o = pencere_olc(d, st, en)
                except Exception as ex:
                    glog.debug("%s %d-%d: %s", s_ad, st, en, ex)
                    continue
                ic = max([(iou(st, en, a, b), i) for a, b, i in ecol], default=(0.0, ""))
                io = max([(iou(st, en, a, b), i) for a, b, i in eolm], default=(0.0, ""))
                o.update(sembol=s_ad, bas_i=st, son_i=en, iou_col=ic[0], etiket_col=ic[1],
                         iou_olm=io[0], etiket_olm=io[1])
                satir.append(o)
        for b0, b1, i in ecol + eolm:          # etiketin tam penceresi (ayri bayrak)
            o = pencere_olc(d, b0, b1)
            o.update(sembol=s_ad, bas_i=b0, son_i=b1, iou_col=1.0 if i in [x[2] for x in ecol] else 0.0,
                     etiket_col=i if i in [x[2] for x in ecol] else "", iou_olm=1.0 if i in [x[2] for x in eolm] else 0.0,
                     etiket_olm=i if i in [x[2] for x in eolm] else "", tam_etiket=i)
            satir.append(o)
    w = pd.DataFrame(satir)
    w["tam_etiket"] = w.get("tam_etiket", pd.Series(index=w.index, dtype=object)).fillna("")
    w["poz"] = w.iou_col >= ay.iou_poz
    w["neg"] = (w.iou_col < ay.iou_neg)
    w["olm"] = w.iou_olm >= ay.iou_poz
    glog.info("K3: %d pencere (%d poz, %d neg, %d olumsuz) | buyuk mum kapisindan atlanan %d | %.0f sn",
              len(w), int(w.poz.sum()), int(w.neg.sum()), int(w.olm.sum()), atlanan, time.monotonic() - t0)
    return w


# ------------------------------------------------------------------ K4
def k4_tarama(ay: GozAyar, w: pd.DataFrame, e: pd.DataFrame) -> pd.DataFrame:
    """Her olcu: Cemal'in col (tam etiket penceresi) vs negatif pencereler vs olumsuz etiketler."""
    tam = w[w.tam_etiket != ""]
    tcol = tam[tam.etiket_col != ""]
    tolm = tam[tam.etiket_olm != ""]
    neg = w[w.neg & (w.tam_etiket == "") & (w.iou_olm < ay.iou_neg)]
    satir = []
    for m in OLCULER:
        if m not in w.columns:
            continue
        pv = tcol[m].to_numpy(float)
        nv = neg[m].to_numpy(float)
        ov = tolm[m].to_numpy(float)
        auc = _auc(pv, nv)
        yon = 1 if (np.isfinite(auc) and auc >= 0.5) else -1
        # hisse/etiket basina yon tutarliligi: etiket degeri, ayni hissenin negatif medyanina gore
        ayni = 0
        top = 0
        for r in tcol.itertuples():
            v = getattr(r, m)
            nn = neg.loc[neg.sembol == r.sembol, m].dropna()
            if not np.isfinite(v) or len(nn) < 10:
                continue
            top += 1
            fark = v - float(nn.median())
            if fark * yon > 0:
                ayni += 1
        tut = ayni / top if top else np.nan
        auc_o = _auc(pv, ov)
        satir.append({"olcu": m, "aciklama": OLCU_ACIKLAMA.get(m, ""),
                      "col_medyan": float(np.nanmedian(pv)) if np.isfinite(pv).any() else np.nan,
                      "diger_medyan": float(np.nanmedian(nv)) if np.isfinite(nv).any() else np.nan,
                      "olumsuz_medyan": float(np.nanmedian(ov)) if np.isfinite(ov).any() else np.nan,
                      "auc_diger": auc, "ayirma_gucu": abs(auc - 0.5) * 2 if np.isfinite(auc) else np.nan,
                      "yon": "col'de YUKSEK" if yon > 0 else "col'de DUSUK",
                      "tutarlilik": tut, "n_etiket": top,
                      "auc_olumsuz": auc_o,
                      "iz": bool(np.isfinite(auc) and abs(auc - 0.5) * 2 >= (ay.iz_auc - 0.5) * 2
                                 and np.isfinite(tut) and tut >= ay.iz_tutarlilik)})
    t = pd.DataFrame(satir).sort_values("ayirma_gucu", ascending=False).reset_index(drop=True)
    glog.info("K4: %d olcu tarandi, %d iz (AUC>=%.2f ve tutarlilik>=%.0f%%)", len(t), int(t.iz.sum()),
              ay.iz_auc, 100 * ay.iz_tutarlilik)
    return t


# ------------------------------------------------------------------ K5
def _nms(cand: pd.DataFrame, esik: float, nms_iou: float) -> pd.DataFrame:
    c = cand[cand.skor >= esik].sort_values("skor", ascending=False)
    sec: List[Tuple[int, int]] = []
    keep = []
    for i, r in c.iterrows():
        if all(iou(int(r.bas_i), int(r.son_i), a, b) < nms_iou for a, b in sec):
            sec.append((int(r.bas_i), int(r.son_i)))
            keep.append(i)
    return c.loc[keep]


def k5_model(ay: GozAyar, w: pd.DataFrame, e: pd.DataFrame, olculer: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.impute import SimpleImputer
    egit = w[(w.poz | w.neg) & (w.tam_etiket == "")].copy()
    egit["y"] = egit.poz.astype(int)
    semboller = sorted(w.sembol.unique())
    tum_tespit = []
    satir = []
    w = w.copy()
    w["skor"] = np.nan
    for s_ad in semboller:
        tr = egit[egit.sembol != s_ad]
        if tr.y.sum() < 10:
            continue
        mdl = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                            LogisticRegression(C=0.3, class_weight="balanced", max_iter=2000,
                                               random_state=ay.rastgele))
        mdl.fit(tr[olculer].to_numpy(float), tr.y.to_numpy(int))
        te = w[(w.sembol == s_ad) & (w.tam_etiket == "")]
        w.loc[te.index, "skor"] = mdl.predict_proba(te[olculer].to_numpy(float))[:, 1]
    for s_ad in semboller:
        te = w[(w.sembol == s_ad) & (w.tam_etiket == "") & w.skor.notna()]
        if not len(te):
            continue
        tes = _nms(te, ay.esik_olasilik, ay.nms_iou)
        tes = tes.assign(sembol=s_ad)
        tum_tespit.append(tes)
    T = pd.concat(tum_tespit, ignore_index=True) if tum_tespit else pd.DataFrame(columns=["sembol", "bas_i", "son_i", "skor"])
    # etiket basina degerlendirme
    for r in e.itertuples():
        ts = T[T.sembol == r.sembol]
        en = max([(iou(int(t.bas_i), int(t.son_i), int(r.bi), int(r.si)), t.Index) for t in ts.itertuples()],
                 default=(0.0, None))
        sat = {"etiket_id": r.etiket_id, "sembol": r.sembol, "sinif": r.sinif, "model_iou": round(en[0], 3)}
        if en[1] is not None:
            t = T.loc[en[1]]
            sat.update(model_bas_i=int(t.bas_i), model_son_i=int(t.son_i), model_skor=round(float(t.skor), 3),
                       bas_fark_bar=int(t.bas_i - r.bi), son_fark_bar=int(t.son_i - r.si))
        satir.append(sat)
    L = pd.DataFrame(satir)
    # tespitlerin siniflandirmasi
    def _sinif(t):
        best_c = max([iou(int(t.bas_i), int(t.son_i), int(r.bi), int(r.si)) for r in e[(e.sembol == t.sembol) & (e.sinif == "COL")].itertuples()], default=0)
        best_o = max([iou(int(t.bas_i), int(t.son_i), int(r.bi), int(r.si)) for r in e[(e.sembol == t.sembol) & (e.sinif == "OLUMSUZ")].itertuples()], default=0)
        if best_c >= 0.3:
            return "cemal_col"
        if best_o >= 0.3:
            return "cemal_olumsuz"
        return "isaretsiz"
    if len(T):
        T["durum"] = [_sinif(t) for t in T.itertuples()]
    c = L[L.sinif == "COL"]
    o = L[L.sinif == "OLUMSUZ"]
    glog.info("K5 (hisse disarida): COL yakalama IoU>=0.5 %d/%d, IoU>=0.3 %d/%d | OLUMSUZ'da alarm %d/%d | "
              "toplam tespit %d (isaretsiz %d)",
              int((c.model_iou >= 0.5).sum()), len(c), int((c.model_iou >= 0.3).sum()), len(c),
              int((o.model_iou >= 0.3).sum()), len(o), len(T), int((T.get("durum") == "isaretsiz").sum()) if len(T) else 0)
    # tum veriyle egitilmis model: katsayilar
    mdl = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                        LogisticRegression(C=0.3, class_weight="balanced", max_iter=2000, random_state=ay.rastgele))
    mdl.fit(egit[olculer].to_numpy(float), egit.y.to_numpy(int))
    kats = pd.DataFrame({"olcu": olculer, "katsayi": mdl[-1].coef_[0]}).sort_values("katsayi", key=np.abs, ascending=False)
    return L, T, kats


# ------------------------------------------------------------------ K6
def k6_grafik(ay: GozAyar, veri, e, kod: pd.DataFrame, loso: pd.DataFrame, cikti: str, sayfa_basi: int = 6,
              bolge_ciz: bool = True) -> List[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    yollar = []
    kd = kod.set_index("etiket_id")
    ld = loso.set_index("etiket_id")
    ee = e.sort_values(["sinif", "sembol", "bas"]).reset_index(drop=True)
    for p0 in range(0, len(ee), sayfa_basi):
        parca = ee.iloc[p0:p0 + sayfa_basi]
        fig, axs = plt.subplots(len(parca), 1, figsize=(9, 3.1 * len(parca)), squeeze=False)
        for ax, r in zip(axs[:, 0], parca.itertuples()):
            df = veri[r.sembol]
            ix = df.index
            a0 = max(0, int(r.bi) - 90)
            a1 = min(len(df) - 1, int(r.si) + 50)
            x = np.arange(a0, a1 + 1)
            H, L, C = df.High.to_numpy()[a0:a1 + 1], df.Low.to_numpy()[a0:a1 + 1], df.Close.to_numpy()[a0:a1 + 1]
            O = df.Open.to_numpy()[a0:a1 + 1]
            ax.vlines(x, L, H, color="#888", lw=0.7)
            renk = np.where(C >= O, "#2a9d8f", "#c0392b")
            ax.vlines(x, np.minimum(O, C), np.maximum(O, C), color=renk, lw=2.2)
            s50 = df.Close.rolling(50).mean().to_numpy()[a0:a1 + 1]
            s200 = df.Close.rolling(200).mean().to_numpy()[a0:a1 + 1]
            ax.plot(x, s50, color="#e9a23b", lw=1, label="SMA50")
            ax.plot(x, s200, color="#6c5ce7", lw=1, label="SMA200")
            lo_, hi_ = np.nanmin(L), np.nanmax(H)
            ax.axvspan(r.bi - 0.5, r.si + 0.5, color="#2ecc71" if r.sinif == "COL" else "#95a5a6", alpha=0.22,
                       label="Cemal: COL" if r.sinif == "COL" else "Cemal: COL DEGIL")
            if (int(r.bi0), int(r.si0)) != (int(r.bi), int(r.si)):       # v1.1: Eylul isaretinin kirpilmamis hali
                for xx in (r.bi0 - 0.5, r.si0 + 0.5):
                    ax.axvline(xx, color="#2ecc71", lw=1.2, ls=":")
            if ay.buyuk_aralik is not None or ay.buyuk_degisim is not None:   # v1.1: buyuk mumlar
                bm = buyuk_mum(df, ay)[a0:a1 + 1]
                if bm.any():
                    ax.scatter(x[bm], H[bm] * 1.012, marker="v", s=22, color="#e67e22", zorder=5,
                               label=f"kapi: >=%{ay.buyuk_aralik:g} aralik / %{ay.buyuk_degisim:g} kapanis")
                orta = GozAyar(buyuk_aralik=6.0, buyuk_degisim=5.0)      # gostergelik: kapidan kucuk ama iri mum
                om = buyuk_mum(df, orta)[a0:a1 + 1] & ~bm
                if om.any():
                    ax.scatter(x[om], H[om] * 1.012, marker="v", s=16, facecolors="none", edgecolors="#c39b00",
                               zorder=5, label="iri mum (>=%6 aralik / %5 kapanis)")
            k = kd.loc[r.etiket_id] if r.etiket_id in kd.index else None
            if k is not None and isinstance(k.kod_bas, str):
                kb = int(ix.searchsorted(pd.Timestamp(k.kod_bas)))
                ks = int(ix.searchsorted(pd.Timestamp(k.kod_son), side="right")) - 1
                ax.add_patch(Rectangle((kb - 0.5, k.kod_taban), ks - kb + 1, k.kod_tavan - k.kod_taban,
                                       fill=False, ec="#e74c3c", lw=1.8, label="kod (COL_v1)"))
            m = ld.loc[r.etiket_id] if r.etiket_id in ld.index else None
            if bolge_ciz and k is not None and int(k.get("bolge_uz", 0)) > 0:      # v1.2: BOLGE KURALI kutusu
                mb, ms = int(k.bolge_bas_i), int(k.bolge_son_i)
                ax.add_patch(Rectangle((mb - 0.5, float(df.Low.iloc[mb:ms + 1].min())), ms - mb + 1,
                                       float(df.High.iloc[mb:ms + 1].max() - df.Low.iloc[mb:ms + 1].min()),
                                       fill=False, ec="#8e44ad", lw=2.0, label="bolge kurali"))
            elif m is not None and np.isfinite(m.get("model_bas_i", np.nan)) and m.model_iou > 0:
                mb, ms = int(m.model_bas_i), int(m.model_son_i)
                ax.add_patch(Rectangle((mb - 0.5, float(df.Low.iloc[mb:ms + 1].min())), ms - mb + 1,
                                       float(df.High.iloc[mb:ms + 1].max() - df.Low.iloc[mb:ms + 1].min()),
                                       fill=False, ec="#2980b9", lw=1.6, ls="--", label="yeni model"))
            kod_iou = float(k.kod_iou) if k is not None else 0.0
            mdl_iou = float(k.bolge_iou) if (bolge_ciz and k is not None) else (float(m.model_iou) if m is not None else 0.0)
            kirp = f"  (kirpildi: {ix[int(r.bi)]:%d.%m}-{ix[int(r.si)]:%d.%m})" if (int(r.bi0), int(r.si0)) != (int(r.bi), int(r.si)) else ""
            ax.set_title(f"{r.sembol}  {r.bas:%d.%m.%Y}-{r.son:%d.%m.%Y}{kirp}  [{'COL' if r.sinif == 'COL' else 'COL DEGIL'}]"
                         f"   kod %{100 * kod_iou:.0f}   {'bolge' if bolge_ciz else 'model'} %{100 * mdl_iou:.0f}", fontsize=9)
            tk = np.linspace(a0, a1, 6).astype(int)
            ax.set_xticks(tk)
            ax.set_xticklabels([f"{ix[i]:%m.%y}" for i in tk], fontsize=7)
            ax.tick_params(axis="y", labelsize=7)
            ax.set_ylim(lo_ * 0.97, hi_ * 1.03)
            ax.legend(fontsize=6, loc="upper left", ncol=3)
        fig.tight_layout()
        y = os.path.join(cikti, f"grafik_{p0 // sayfa_basi + 1:02d}.png")
        fig.savefig(y, dpi=110)
        plt.close(fig)
        yollar.append(y)
    glog.info("K6: %d grafik sayfasi", len(yollar))
    return yollar


# ------------------------------------------------------------------ ANA
def goz_esle(ay: Optional[GozAyar] = None, grafik: bool = True) -> Dict[str, Any]:
    ay = ay or GozAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "goz_esle")
    os.makedirs(cikti, exist_ok=True)
    t0 = time.monotonic()
    veri, e = k1_veri(ay)
    kod = k2_kod_pencereleri(ay, veri, e)
    kod.to_csv(os.path.join(cikti, "goz_kod_kiyas.csv"), index=False)
    w = k3_pencereler(ay, veri, e)
    tar = k4_tarama(ay, w, e)
    tar.to_csv(os.path.join(cikti, "goz_metrik_tarama.csv"), index=False)
    olculer = [m for m in OLCULER if m in w.columns and w[m].notna().mean() > 0.5]
    loso, tespit, kats = k5_model(ay, w, e, olculer)
    loso.to_csv(os.path.join(cikti, "goz_model_loso.csv"), index=False)
    tespit.to_csv(os.path.join(cikti, "goz_model_tespitler.csv"), index=False)
    kats.to_csv(os.path.join(cikti, "goz_model_katsayi.csv"), index=False)
    grafikler = k6_grafik(ay, veri, e, kod, loso, cikti) if grafik else []
    sure = time.monotonic() - t0
    glog.info("BITTI %.0f sn -> %s", sure, cikti)
    return {"veri": veri, "etiket": e, "kod": kod, "pencere": w, "tarama": tar, "loso": loso,
            "tespit": tespit, "katsayi": kats, "grafik": grafikler, "cikti": cikti, "sure": sure}


def _arg() -> GozAyar:
    p = argparse.ArgumentParser(description=SURUM)
    p.add_argument("--kok", default=GozAyar.kok)
    p.add_argument("--cikti", default=None)
    p.add_argument("--kod-kok", default=None, help="COL_v1.py baska klasordeyse")
    p.add_argument("--buyuk-aralik", type=float, default=GozAyar.buyuk_aralik, help="%%; 0 = kapali")
    p.add_argument("--buyuk-degisim", type=float, default=GozAyar.buyuk_degisim, help="%%; 0 = kapali")
    p.add_argument("--grafiksiz", action="store_true")
    a = p.parse_args()
    ay = GozAyar(kok=a.kok, cikti=a.cikti,
                 buyuk_aralik=a.buyuk_aralik or None, buyuk_degisim=a.buyuk_degisim or None)
    ay.grafiksiz = a.grafiksiz  # type: ignore[attr-defined]
    if a.kod_kok:
        ay.kod_dosya = os.path.join(os.path.abspath(a.kod_kok), "COL_v1.py")
    return ay


if __name__ == "__main__":
    _ay = _arg()
    goz_esle(_ay, grafik=not getattr(_ay, "grafiksiz", False))
