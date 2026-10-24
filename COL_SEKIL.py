# =====================================================================
#  COL_SEKIL — Cemal'in col tarifini olcuye cevirme   (2026-10-21, v1.0)
#
#  CEMAL (21 Eki, 21 kutuluk etiketleme): hicbiri col degil; #19'da mumlar kucuk ama "kucuk mum tek basina yetmez:
#    dip olusmali, dip savunulmali, parabolik cizgiyle yukari yuvarlanma ve kucuk mum obekleri sirasi birlikte olmali".
#    Diger 20 kutuda onun gozunde kucuk mum yok — kodun 'kucuk' imzasi (250 gun medyanina gore) ise cogunda gecmisti.
#
#  SORU: Cemal'in 29 colu ile "degil" dedigi 29 kutuyu (8 eski OLUMSUZ + 21 bugun) hangi olcu ayiriyor?
#  OLCULER (pencere = etiketin kendisi; ileriye bakis yok, yalniz pencere ve oncesi):
#    kucuk mum  : aralik_pct (gun araligi medyani, % fiyat), aralik_kutu (aralik / kutu yuksekligi), aralik_ref60, aralik_ref250
#    dip        : dip_pos (dibin kutudaki yeri 0-1), dip_sonrasi_bar, retest (dibe 1 normal gun yaklasan bar sayisi)
#    yuvarlanma : dipten sonraki diplere parabol: egri_a (>0 ic bukey), son_egim (>0 yukari donmus), ilk_egim; sma10_donus
#    obek       : dipten sonra kucuk mum obegi (>=3 ardisik kucuk bar) sayisi, obek_yukselen (ardisik obek orta fiyati artiyor mu)
#    bollinger  : bb_son (kutu sonu BB genisliginin son 250 gundeki sirasi, 0 = en dar)
#  KURAL_MOTORU: K1 veri (COL_DIP_TEST.cd_k1_bist; yoksa kalibre_veri.csv)  K2 etiketler  K3 olcu  K4 kiyas + rapor
#  Calistirma: GitHub Actions 'Arastirma' (betik: COL_SEKIL.py). Cikti: arastirma_cikti/col_sekil/
#  n kucuk (29 / 29), donemler farkli (2024-25 / 2026 cokus): bulgu degil, olcum. Kural yazmaz, aday olcu gosterir.
# =====================================================================
from __future__ import annotations

import logging
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_CK_ONCE_CS = {k: id(v) for k, v in globals().items()}

CS_SURUM = "COL_SEKIL v1.1 (2026-10-24, denetim: karsilastirilabilir negatif = eski OLUMSUZ)"
cslog = logging.getLogger("col.sekil")
if not cslog.handlers:
    _cs_h = logging.StreamHandler(sys.stderr)
    _cs_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sekil: %(message)s", "%H:%M:%S"))
    cslog.addHandler(_cs_h)
    cslog.setLevel(logging.INFO)
    cslog.propagate = False


@dataclass
class CSAyar:
    kok: str = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/content/drive/MyDrive/col_tarayici"
    cikti: Optional[str] = None
    etiket_eski: str = "kalibre_etiketler.csv"
    etiket_bugun: str = os.path.join("goz_esle", "etiket_2026-10-20.csv")
    kalibre_veri: str = "kalibre_veri.csv"
    min_pencere: int = 15


# ------------------------------------------------------------------ K1 veri
def cs_k1_veri(ay: CSAyar) -> Dict[str, pd.DataFrame]:
    """Actions/Drive onbellegi varsa COL_DIP_TEST.cd_k1_bist (583 hisse); yoksa yerel kalibre_veri.csv (32 hisse, prova)."""
    if os.path.exists(os.path.join(ay.kok, "veri_1d_turkey.pkl")):
        import importlib
        if ay.kok not in sys.path:
            sys.path.insert(0, ay.kok)
        CD = importlib.import_module("COL_DIP_TEST")
        cay = CD.CDAyar(kok=ay.kok)
        veri = CD.cd_k1_bist(cay)
        CD.cd_k2_onarim(cay, veri)
        return veri
    y = os.path.join(ay.kok, ay.kalibre_veri)
    v = pd.read_csv(y, parse_dates=["tarih"])
    veri = {s: g.set_index("tarih").sort_index()[["Open", "High", "Low", "Close", "Volume"]].astype(float) for s, g in v.groupby("sembol")}
    cslog.warning("K1: onbellek yok, yerel %s (%d hisse) — prova", ay.kalibre_veri, len(veri))
    return veri


# ------------------------------------------------------------------ K2 etiketler
def cs_k2_etiket(ay: CSAyar) -> pd.DataFrame:
    """sembol, bas, son, sinif (COL | DEGIL), set (eski | bugun), not."""
    e1 = pd.read_csv(os.path.join(ay.kok, ay.etiket_eski), parse_dates=["bas", "son"])
    e1 = e1.rename(columns={"sinif": "sinif"})
    e1["sinif"] = e1.sinif.map({"COL": "COL", "OLUMSUZ": "DEGIL"}).fillna(e1.sinif)
    e1["set"] = "eski"; e1["not"] = ""
    y2 = os.path.join(ay.kok, ay.etiket_bugun)
    if os.path.exists(y2):
        e2 = pd.read_csv(y2, parse_dates=["kutu_bas", "kutu_son"])
        e2 = pd.DataFrame({"sembol": e2.sembol, "bas": e2.kutu_bas, "son": e2.kutu_son,
                           "sinif": np.where(e2.cemal.astype(str).str.upper().str.startswith("COL"), "COL", "DEGIL"),
                           "set": "bugun", "not": e2.cemal.astype(str)})
        e = pd.concat([e1[["sembol", "bas", "son", "sinif", "set", "not"]], e2], ignore_index=True)
    else:
        e = e1[["sembol", "bas", "son", "sinif", "set", "not"]]
    e["etiket"] = e.sembol + "_" + e.bas.dt.strftime("%Y%m%d")
    return e


# ------------------------------------------------------------------ K3 olcu
def _parabol(y: np.ndarray) -> Tuple[float, float, float]:
    """y (%) dizisine x in [0,1] parabol: (a, ilk_egim, son_egim). a>0 ic bukey (yuvarlanma), son_egim>0 yukari donmus."""
    n = len(y)
    if n < 8 or not np.all(np.isfinite(y)):
        return np.nan, np.nan, np.nan
    x = np.linspace(0, 1, n)
    a, b, _ = np.polyfit(x, y, 2)
    return float(a), float(b), float(2 * a + b)


def cs_olc(df: pd.DataFrame, bas: pd.Timestamp, son: pd.Timestamp) -> Optional[Dict[str, Any]]:
    x = df[np.isfinite(df.Close)]
    ix = x.index
    s, e = int(ix.searchsorted(bas)), int(ix.searchsorted(son, side="right")) - 1
    if e - s + 1 < 8 or s < 60:
        return None
    O, H, L, C, V = (x[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    pc = np.r_[O[0], C[:-1]]
    ar = 100 * (H - L) / pc
    uz = e - s + 1
    ref250 = float(np.nanmedian(ar[max(0, s - 250):s])) if s >= 120 else np.nan
    ref60 = float(np.nanmedian(ar[max(0, s - 60):s]))
    r = {"uz": uz, "aralik_pct": round(float(np.nanmedian(ar[s:e + 1])), 2),
         "aralik_kutu": round(float(np.nanmedian(H[s:e + 1] - L[s:e + 1]) / max(1e-9, H[s:e + 1].max() - L[s:e + 1].min())), 3),
         "aralik_ref60": round(float(np.nanmedian(ar[s:e + 1]) / ref60), 2) if ref60 > 0 else np.nan,
         "aralik_ref250": round(float(np.nanmedian(ar[s:e + 1]) / ref250), 2) if (np.isfinite(ref250) and ref250 > 0) else np.nan,
         "kucuk_oran250": round(float(np.mean(ar[s:e + 1] <= ref250)), 2) if np.isfinite(ref250) else np.nan}
    # dip
    d = s + int(np.nanargmin(L[s:e + 1]))
    dip = L[d]
    norm = ref60 if ref60 > 0 else float(np.nanmedian(ar[s:e + 1]))
    r.update(dip_pos=round((d - s) / uz, 2), dip_sonrasi_bar=int(e - d),
             retest=int(np.sum(L[d + 1:e + 1] <= dip * (1 + norm / 100))) if e > d else 0,
             dip_oncesi_dusus=round(float(C[s] / dip - 1) * 100, 1))
    # yuvarlanma: dipten sonraki diplerin parabolu (L / dip - 1, %)
    if e - d >= 8:
        a, b0, b1 = _parabol(100 * (L[d:e + 1] / dip - 1))
        r.update(egri_a=round(a, 1), ilk_egim=round(b0, 1), son_egim=round(b1, 1),
                 yuvarlak=bool(np.isfinite(a) and a > 0 and b1 > 0))
        sma = pd.Series(C[:e + 1]).rolling(10, min_periods=10).mean().to_numpy()
        seg = sma[d:e + 1]; k = max(3, len(seg) // 3)
        r["sma10_donus"] = bool(np.isfinite(seg[k - 1]) and (seg[k - 1] - seg[0]) <= 0 and (seg[-1] - seg[-k]) > 0)
    else:
        r.update(egri_a=np.nan, ilk_egim=np.nan, son_egim=np.nan, yuvarlak=False, sma10_donus=False)
    # obek: dipten sonra kucuk mum obekleri (>= 3 ardisik bar, aralik <= kutu medyani)
    med = float(np.nanmedian(ar[s:e + 1]))
    kucuk = ar[d:e + 1] <= med
    obek: List[Tuple[int, int]] = []
    i = 0
    while i < len(kucuk):
        if kucuk[i]:
            j = i
            while j + 1 < len(kucuk) and kucuk[j + 1]:
                j += 1
            if j - i + 1 >= 3:
                obek.append((d + i, d + j))
            i = j + 1
        else:
            i += 1
    orta = [float(np.median(C[a:b + 1])) for a, b in obek]
    r.update(obek=len(obek), obek_yukselen=round(float(np.mean(np.diff(orta) > 0)), 2) if len(orta) >= 2 else np.nan)
    # bollinger kutu sonu
    cs_ = pd.Series(C[:e + 1]); m = cs_.rolling(20, min_periods=20).mean(); sd = cs_.rolling(20, min_periods=20).std(ddof=0)
    bbw = (4 * sd / m.replace(0, np.nan)).to_numpy(float)
    pen = bbw[max(0, e - 249):e + 1]; pen = pen[np.isfinite(pen)]
    r["bb_son"] = round(float((pen <= bbw[e]).mean()), 2) if (len(pen) >= 60 and np.isfinite(bbw[e])) else np.nan
    r["hacim_kat60"] = round(float(np.nanmedian(V[s:e + 1]) / np.nanmedian(V[max(0, s - 60):s])), 2) if s > 0 and np.nanmedian(V[max(0, s - 60):s]) > 0 else np.nan
    return r


def cs_k3_olc(ay: CSAyar, veri: Dict[str, pd.DataFrame], e: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for r in e.itertuples():
        df = veri.get(r.sembol)
        if df is None:
            cslog.warning("K3: veri yok %s", r.sembol); continue
        o = cs_olc(df, r.bas, r.son)
        if not o:
            cslog.warning("K3: pencere kisa %s", r.etiket); continue
        rows.append({"etiket": r.etiket, "sembol": r.sembol, "sinif": r.sinif, "set": r.set, "bas": r.bas.date(), "son": r.son.date(), **o})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ K4 kiyas
def _auc(poz: np.ndarray, neg: np.ndarray) -> float:
    poz, neg = poz[np.isfinite(poz)], neg[np.isfinite(neg)]
    if len(poz) == 0 or len(neg) == 0:
        return np.nan
    return float((poz[:, None] > neg[None, :]).mean() + 0.5 * (poz[:, None] == neg[None, :]).mean())


OLCULER = ["aralik_pct", "aralik_kutu", "aralik_ref60", "aralik_ref250", "kucuk_oran250", "dip_pos", "dip_sonrasi_bar", "retest",
           "dip_oncesi_dusus", "egri_a", "ilk_egim", "son_egim", "obek", "obek_yukselen", "bb_son", "hacim_kat60", "uz"]


def cs_k4_rapor(ay: CSAyar, T: pd.DataFrame, cikti: str) -> str:
    c, d = T[T.sinif == "COL"], T[T.sinif == "DEGIL"]
    sat = [f"# COL SEKIL — Cemal'in tarifi olcuye   ({CS_SURUM}, {pd.Timestamp.now():%Y-%m-%d %H:%M})", "",
           f"Etiket: COL {len(c)} (Cemal'in colleri, 2024-26) | DEGIL {len(d)} (eski OLUMSUZ {int((d.set=='eski').sum())} + 21 Eki kutulari {int((d.set=='bugun').sum())}).",
           "Pencere = etiketin kendisi. n kucuk, donemler farkli: BULGU DEGIL, OLCUM. AUC 0.5 = ayirmiyor, 1.0/0.0 = tam ayiriyor.", "",
           "DENETIM 24 Eki: 'bugun' DEGIL kutulari cokus haftasinda biten ve COL_BUGUN'un kendi ret nedenine ('yeni dip', 'dipte degil')",
           "gore secilmis kutular; dip olculeri bu kutularda tanim geregi farkli. COL kutularinin sonu ise grafigin devami gorulerek cizildi",
           "(19/29'da kirilim 5 bar icinde). Karsilastirilabilir negatif yalniz ayni yoldan (gozle) cizilen eski OLUMSUZ: AUC_esk sutunu esastir.", "",
           "## Olcu basina medyan (COL | DEGIL) ve AUC (COL > DEGIL olasiligi)", "",
           "| olcu | COL medyan | DEGIL medyan | AUC (tum DEGIL) | AUC_esk (yalniz eski OLUMSUZ) | yorum |", "|---|---|---|---|---|---|"]
    yorum = {"aralik_pct": "gun araligi % (mutlak kucuk mum)", "aralik_kutu": "aralik / kutu yuksekligi", "aralik_ref60": "onceki 60 gune gore",
             "aralik_ref250": "onceki 250 gune gore (kodun olcusu)", "kucuk_oran250": "kodun 'kucuk' imzasi", "dip_pos": "dip kutunun neresinde (0 bas)",
             "dip_sonrasi_bar": "dipten sonra kac bar", "retest": "dibe yaklasan bar (savunma testi)", "dip_oncesi_dusus": "kutu basi -> dip %",
             "egri_a": "parabol ic bukeyligi (>0 yuvarlanma)", "ilk_egim": "dipten sonra ilk egim", "son_egim": "kutu sonu egim (>0 yukari)",
             "obek": "kucuk mum obegi sayisi", "obek_yukselen": "obekler yukseliyor mu", "bb_son": "kutu sonu Bollinger sirasi", "hacim_kat60": "hacim / onceki 60 gun", "uz": "bar"}
    for m in OLCULER:
        if m not in T.columns: continue
        a = _auc(c[m].to_numpy(float), d[m].to_numpy(float)); a_es = _auc(c[m].to_numpy(float), d[d.set == "eski"][m].to_numpy(float))
        sat.append(f"| {m} | {c[m].median():.2f} | {d[m].median():.2f} | {a:.2f} | {a_es:.2f} | {yorum.get(m,'')} |")
    for m in ("yuvarlak", "sma10_donus"):
        if m in T.columns:
            sat.append(f"| {m} | %{100*c[m].mean():.0f} evet | %{100*d[m].mean():.0f} evet | - | {('dipten sonra parabol yukari donmus' if m=='yuvarlak' else 'SMA10 once duz/asagi sonra yukari')} |")
    sat += ["", "## Bileşik: dip savunması + yuvarlanma (dip_pos <= 0.6 ve yuvarlak)", ""]
    for ad, g in (("COL", c), ("DEGIL", d), ("DEGIL yalniz eski OLUMSUZ", d[d.set == "eski"])):
        b = (g.dip_pos <= 0.6) & g.yuvarlak.astype(bool)
        sat.append(f"- {ad}: {int(b.sum())}/{len(g)} gecer")
    sat += ["", "## Etiket basina", ""]
    kol = ["etiket", "sinif", "set", "uz", "aralik_pct", "aralik_kutu", "aralik_ref250", "dip_pos", "dip_sonrasi_bar", "retest", "egri_a", "son_egim", "yuvarlak", "obek", "obek_yukselen", "bb_son"]
    sat.append(T[kol].sort_values(["sinif", "set", "etiket"]).to_string(index=False))
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "COL_SEKIL_rapor.md"), "w", encoding="utf-8").write(metin)
    return metin


def col_sekil(ay: Optional[CSAyar] = None, veri: Optional[Dict[str, pd.DataFrame]] = None) -> Dict[str, Any]:
    ay = ay or CSAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "col_sekil")
    os.makedirs(cikti, exist_ok=True)
    t0 = time.monotonic()
    veri = veri if veri is not None else cs_k1_veri(ay)
    e = cs_k2_etiket(ay)
    cslog.info("K2: %d etiket (COL %d, DEGIL %d)", len(e), int((e.sinif == 'COL').sum()), int((e.sinif == 'DEGIL').sum()))
    T = cs_k3_olc(ay, veri, e)
    T.to_csv(os.path.join(cikti, "col_sekil_olcu.csv"), index=False)
    metin = cs_k4_rapor(ay, T, cikti)
    cslog.info("BITTI %.0f sn -> %s", time.monotonic() - t0, cikti)
    return {"olcu": T, "rapor": metin, "cikti": cikti}


def _cakisma_kontrol_cs(_once=_CK_ONCE_CS, _dosya='COL_SEKIL.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_CS', '_CK_KAYIT', '_cakisma_kontrol_cs', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'time', 'logging', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_cs()

if __name__ == "__main__":
    R = col_sekil()
    print(R["rapor"])
