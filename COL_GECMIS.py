# =====================================================================
#  COL_GECMIS — "Bugun X tarihi olsaydi kod hangi colleri bulurdu?"   (2026-10-20, v1.0)
#
#  SORU (Cemal 20 Eki): gecmis bir gunde (or. 16 Mart 2024) tarayici calissaydi hangi colleri bulurdu,
#    sonra ne oldu? Ya da genis bir tarih araliginda kodun buldugu butun coller.
#
#  YONTEM (geri sarma, ileriye bakis yok)
#    Tespit: COL_v1._col_dip_e (D12 dip colu, uretimdeki kod) + col_olc'nin kosullari (uzunluk >= MIN_UZ,
#            yukseklik <= MAX_YUK ATR). Her gun yalniz o gune kadarki veri kullanilir.
#    Sonuc (sonradan): COL_DIP_TEST ile ayni kural — KIRILIM_EN_GEC bar icinde kapanis > tavan*AL_PAY = atilim,
#            ertesi gun acilis alim, %20 hedef sonra SMA20 trail / 120 bar; atilimdan once taban kirilirsa 'bozuldu'.
#            Ayrica tespit gununden sonraki 120 barda en yuksek / en dusuk (%).
#    ANLIK : verilen gunler (varsayilan 2024-03-15 = 16 Mart 2024 Cumartesi'den onceki son seans) — butun coller
#            + grafik icin fiyat pencereleri (kutu oncesi 150, tespit sonrasi 130 bar).
#    ARALIK: ARALIK_BAS'tan bugune her cuma; ayni col (ayni hisse, kutu basi +-10 bar) bir kez, ilk goruldugu gun.
#
#  KURAL_MOTORU: K1 veri (COL_DIP_TEST.cd_k1_bist + onarim)  K2 COL_v1  K3 anlik  K4 aralik  K5 rapor
#  Calistirma: GitHub Actions 'Arastirma' is akisi (betik: COL_GECMIS.py) ya da Colab:
#    exec(open('/content/drive/MyDrive/col_tarayici/COL_GECMIS.py').read()); R = col_gecmis()
#  Cikti: arastirma_cikti/col_gecmis/ (col_gecmis_anlik.csv, col_gecmis_aralik.csv, col_gecmis_pencere.csv.gz, rapor)
#  Grafikler hisse adsiz cizilir (Cemal'in kurali: test resimlerinde hisse adi yok); ad anahtari anlik.csv'de.
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

_CK_ONCE_GC = {k: id(v) for k, v in globals().items()}

GC_SURUM = "COL_GECMIS v1.0 (2026-10-20)"
gclog = logging.getLogger("col.gecmis")
if not gclog.handlers:
    _gc_h = logging.StreamHandler(sys.stderr)
    _gc_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s gecmis: %(message)s", "%H:%M:%S"))
    gclog.addHandler(_gc_h)
    gclog.setLevel(logging.INFO)
    gclog.propagate = False


@dataclass
class GCAyar:
    kok: str = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/content/drive/MyDrive/col_tarayici"
    cikti: Optional[str] = None
    anlik: Tuple[str, ...] = ("2024-03-15",)
    aralik_bas: str = "2024-01-01"
    aralik_frekans: str = "W-FRI"
    pencere_once: int = 150
    pencere_sonra: int = 130
    ayni_kutu_bar: int = 10
    ufuk_bak: int = 120


def _gc_cd():
    """COL_DIP_TEST tek kaynak: veri yukleme, onarim, COL_v1 yukleme ve islem kurali."""
    import importlib
    kok = GCAyar().kok
    if kok not in sys.path:
        sys.path.insert(0, kok)
    return importlib.import_module("COL_DIP_TEST")


def _gc_tespit(CD, cay, ns, df: pd.DataFrame, D, bbw, e: int) -> Optional[Dict[str, Any]]:
    out, t = ns["_col_dip_e"](df, D, bbw, e, alanlar=False)
    if not out or out["uzunluk"] < int(ns["MIN_UZ"]) or out["yukseklik_atr"] > float(ns["MAX_YUK"]):
        return None
    return out


def _gc_sonuc(CD, cay, ns, O, H, L, C, S20, e: int, tavan: float, taban: float, ufuk: int) -> Dict[str, Any]:
    r = CD._cd_islem(cay, float(ns["AL_PAY"]), O, H, L, C, S20, e, tavan, taban)
    n = len(C)
    il = slice(e + 1, min(n, e + 1 + ufuk))
    s: Dict[str, Any] = {"en_yuksek_%": round(float(H[il].max() / C[e] - 1) * 100, 1) if e + 1 < n else np.nan,
                         "en_dusuk_%": round(float(L[il].min() / C[e] - 1) * 100, 1) if e + 1 < n else np.nan}
    if r and "getiri" in r:
        s.update(sonuc="atilim", atilim_i=r["b"], giris_i=r["g"], cikis_i=r["c"], islem_getiri=round(r["getiri"], 1),
                 hedef=r["hedef"], acik=r["acik"])
    elif r and r.get("bozuldu"):
        s.update(sonuc="bozuldu")
    elif r and r.get("atilim_yok"):
        s.update(sonuc="atilim yok")
    else:
        s.update(sonuc="veri sonu")
    return s


def col_gecmis(ay: Optional[GCAyar] = None) -> Dict[str, Any]:
    ay = ay or GCAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "col_gecmis")
    os.makedirs(cikti, exist_ok=True)
    t0 = time.monotonic()
    CD = _gc_cd()
    cay = CD.CDAyar(kok=ay.kok)
    ns = CD.cd_k3_col(cay)
    veri = CD.cd_k1_bist(cay)
    CD.cd_k2_onarim(cay, veri)
    anlik = [pd.Timestamp(d) for d in ay.anlik]
    son_gun = max(df.index[-1] for df in veri.values())
    cuma = list(pd.date_range(pd.Timestamp(ay.aralik_bas), son_gun, freq=ay.aralik_frekans))
    A: List[Dict[str, Any]] = []
    R: List[Dict[str, Any]] = []
    P: List[pd.DataFrame] = []
    cid = 0
    for k, (sem, df) in enumerate(veri.items()):
        df = df[np.isfinite(df.Close)]
        if len(df) < 300:
            continue
        ix = df.index
        O, H, L, C = (df[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
        S20 = df.Close.rolling(cay.ma, min_periods=cay.ma).mean().to_numpy(float)
        try:
            D, bbw = ns["_bolge_dizi"](df), ns["_bb_genislik"](df)
        except Exception as ex:
            gclog.debug("%s dizi: %s", sem, ex)
            continue

        def _kayit(gun, e, out):
            s0 = int(ix.searchsorted(pd.Timestamp(out["bas_tarih"])))
            so = _gc_sonuc(CD, cay, ns, O, H, L, C, S20, e, out["tavan"], out["taban"], ay.ufuk_bak)
            rec = {"gun": gun.date(), "sembol": sem, "tespit": ix[e].date(), "kutu_bas": out["bas_tarih"], "kutu_son": out["son_tarih"],
                   "uzunluk": out["uzunluk"], "tavan": out["tavan"], "taban": out["taban"], "imza": out["imza"],
                   "imza_ok": out["imza_ok"], "konum": out["konum"], "kapanis": round(float(C[e]), 2), **so}
            for a in ("atilim_i", "giris_i", "cikis_i"):
                if a in rec:
                    rec[a.replace("_i", "")] = ix[int(rec.pop(a))].date()
            return rec, s0

        for g in anlik:
            e = int(ix.searchsorted(g, side="right")) - 1
            if e < 260 or ix[e] < g - pd.Timedelta(days=7):
                continue
            out = _gc_tespit(CD, cay, ns, df, D, bbw, e)
            if out:
                rec, s0 = _kayit(g, e, out)
                cid += 1
                rec["cid"] = cid
                A.append(rec)
                w = df.iloc[max(0, s0 - ay.pencere_once):min(len(df), e + 1 + ay.pencere_sonra)].copy()
                w.insert(0, "cid", cid)
                P.append(w.reset_index().rename(columns={w.index.name or "index": "tarih"}))
        son_bas = -999
        for g in cuma:
            e = int(ix.searchsorted(g, side="right")) - 1
            if e < 260 or ix[e] < g - pd.Timedelta(days=7):
                continue
            out = _gc_tespit(CD, cay, ns, df, D, bbw, e)
            if not out:
                continue
            s0 = int(ix.searchsorted(pd.Timestamp(out["bas_tarih"])))
            if abs(s0 - son_bas) <= ay.ayni_kutu_bar:
                continue
            son_bas = s0
            rec, _ = _kayit(g, e, out)
            R.append(rec)
        if (k + 1) % 100 == 0:
            gclog.info("K3/K4: %d/%d hisse | anlik %d col | aralik %d col (%.0f sn)", k + 1, len(veri), len(A), len(R), time.monotonic() - t0)
    ta, tr = pd.DataFrame(A), pd.DataFrame(R)
    ta.to_csv(os.path.join(cikti, "col_gecmis_anlik.csv"), index=False)
    tr.to_csv(os.path.join(cikti, "col_gecmis_aralik.csv"), index=False)
    if P:
        pd.concat(P, ignore_index=True).to_csv(os.path.join(cikti, "col_gecmis_pencere.csv.gz"), index=False)
    # K5 rapor
    sat = [f"# COL GECMIS TARAMA — {pd.Timestamp.now():%Y-%m-%d %H:%M} ({GC_SURUM})", "",
           "Tespit: D12 dip colu (uretim kodu), her gun yalniz o gune kadarki veri. Sonuc: atilim (kapanis > tavan*1.002, 60 bar icinde) "
           "-> ertesi gun acilis alim -> %20 sonra SMA20 trail / 120 bar; atilimdan once taban kirilirsa 'bozuldu'.", ""]
    for g in anlik:
        x = ta[ta.gun == g.date()] if len(ta) else ta
        sat.append(f"## {g.date()} itibariyla: {len(x)} col")
        if len(x):
            sat.append("sonuc dagilimi: " + ", ".join(f"{a} {b}" for a, b in x.sonuc.value_counts().items()))
            z = x[x.sonuc == "atilim"]
            if len(z):
                sat.append(f"atilim olanlarda islem getirisi: ort {z['islem_getiri'].mean():+.1f}% medyan {z['islem_getiri'].median():+.1f}% "
                           f"kazanan %{100*(z['islem_getiri'] > 0).mean():.0f} (n={len(z)})")
        sat.append("")
    if len(tr):
        tr["yil"] = pd.to_datetime(tr.tespit).dt.year
        sat.append(f"## Aralik {ay.aralik_bas} -> {son_gun.date()} (her cuma, ayni col bir kez): {len(tr)} col")
        for y, x in tr.groupby("yil"):
            z = x[x.sonuc == "atilim"]
            sat.append(f"- {y}: {len(x)} col | " + ", ".join(f"{a} {b}" for a, b in x.sonuc.value_counts().items())
                       + (f" | atilimda ort {z['islem_getiri'].mean():+.1f}% medyan {z['islem_getiri'].median():+.1f}% "
                          f"kazanan %{100*(z['islem_getiri'] > 0).mean():.0f}" if len(z) else ""))
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "COL_GECMIS_rapor.md"), "w", encoding="utf-8").write(metin)
    gclog.info("BITTI %.0f sn -> %s", time.monotonic() - t0, cikti)
    return {"anlik": ta, "aralik": tr, "rapor": metin, "cikti": cikti}


def _cakisma_kontrol_gc(_once=_CK_ONCE_GC, _dosya='COL_GECMIS.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_GC', '_CK_KAYIT', '_cakisma_kontrol_gc', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'time', 'logging', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_gc()

if __name__ == "__main__":
    R = col_gecmis()
    print(R["rapor"])
