"""K55 ortak araştırma paneli (Faz 0 madde 3): sembol × gün satırları; K51 taban ölçüleri (vol60, log_dv20, dd250, r60, ar20, trend), likit bayrağı,
maliyet (komisyon + kayma), ileri getiri r60 (seri sonu işlemiyle) ve tanımlı bayrağı, oynaklık ondalığı / likidite üçlüsü / rejim / sektör / dönem.
Her modül aynı paneli kullanır; panel bir kez kurulur ve pickle olarak saklanır (sürüm = evren sürümü + kod sürümü).
"""
from __future__ import annotations

import multiprocessing as mp
import os
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from .olay_tanimlari import ileri_getiri
from .ortak import ALIVE_SINIR, DONEM, K55Ayar, MIN_GUN, OLAY, cy, donem_etiketi, donem_etiketi_ufuk, log

PANEL_KOL = ["tarih", "i", "likit", "open", "close", "dv20", "vol60", "log_dv20", "dd250", "r60", "ar20", "trend", "kayma", "mal", "r60_ileri", "r60_tanimli"]


def _isci(arg: Tuple[Any, ...]) -> Optional[Dict[str, Any]]:
    s, d, evren_bas, esik, seri_erken, seri_sonu = arg
    try:
        C = cy(); K = C.CY; M = C.cy_olculer(d, K, (K["col"]["L"],)); F = M["F"]; n = len(d); idx = d.index
        dv20 = np.asarray(M["dv20"], float); e = esik.reindex(idx).ffill().to_numpy(float)
        likit = (dv20 >= e) & (dv20 >= float(K["likit"]["ABD"])) & (d.Close.to_numpy(float) >= float(K["fiyat_min"]["ABD"])) & (np.arange(n) >= MIN_GUN)
        likit &= np.asarray(idx >= pd.Timestamp(evren_bas)) & np.asarray(idx >= pd.Timestamp(DONEM["KESIF"][0]))
        O = d.Open.to_numpy(float); Cl = d.Close.to_numpy(float); r60, tam = ileri_getiri(O, Cl, 60, seri_erken, seri_sonu)
        kayma = np.asarray(M["kayma"], float); mal = 2 * (K["komisyon"]["ABD"] + kayma)
        P = pd.DataFrame({"tarih": idx, "i": np.arange(n, dtype=np.int32), "likit": likit, "open": O.astype(np.float32), "close": Cl.astype(np.float32),
                          "dv20": dv20.astype(np.float32), "vol60": F.vol60.to_numpy(np.float32), "log_dv20": F.log_dv20.to_numpy(np.float32),
                          "dd250": F.dd250.to_numpy(np.float32), "r60": F.r60.to_numpy(np.float32), "ar20": F.ar20.to_numpy(np.float32),
                          "trend": (F.c_sma200.to_numpy(float) > 0).astype(np.int8), "kayma": kayma.astype(np.float32), "mal": mal.astype(np.float32),
                          "r60_ileri": r60.astype(np.float32), "r60_tanimli": tam | (seri_erken & np.isfinite(r60))})
        for ad, (h, _) in OLAY.items():                                  # etiket penceresinin son günü (purge için); seri dışına taşarsa NaT
            bt = np.full(n, np.datetime64("NaT"), dtype="datetime64[ns]"); ok = np.arange(n) + h < n; bt[ok] = idx.to_numpy()[np.arange(n)[ok] + h]
            P[f"bitis{h}"] = bt
        P = P[np.arange(n) >= MIN_GUN]                                   # ölçüler ilk MIN_GUN günde tanımsız (özellik gereksinimi; evren dışı değil)
        return {"sembol": s, "panel": P, "likit": likit, "ozelliksiz": int(min(n, MIN_GUN))}
    except Exception as ex:
        log.warning("panel %s atlandı: %s", s, ex); return None


def panel_kur(V: Dict[str, pd.DataFrame], EV: pd.DataFrame, A: K55Ayar, endeks: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, Dict[str, np.ndarray], Dict[str, Any]]:
    """Ortak panel. Dönüş: P (satır = sembol-gün, MIN_GUN sonrası), likit_map (sembol -> tam uzunlukta likit bayrağı), bilgi (süre, sayılar)."""
    C = cy(); t0 = time.time(); esik = C.cy_likit_esik(V, "ABD", C.CY); ev = EV.set_index("sembol")
    sk = "seri_sonu_getiri" if "seri_sonu_getiri" in ev else "seri_sonu"
    args = [(s, d, ev.loc[s, "evren_bas"], esik, bool(ev.loc[s, "seri_erken"]), str(ev.loc[s, sk])) for s, d in V.items() if s in ev.index]
    if A.isci > 1 and len(args) > 8:
        with mp.get_context("fork").Pool(A.isci) as hv:
            son = [x for x in hv.imap_unordered(_isci, args, chunksize=8) if x is not None]
    else:
        son = [x for x in map(_isci, args) if x is not None]
    son.sort(key=lambda r: r["sembol"])
    P = pd.concat([r["panel"].assign(sembol=r["sembol"]) for r in son if len(r["panel"])], ignore_index=True)
    P["tarih"] = pd.to_datetime(P.tarih).astype("datetime64[ns]"); P["sembol"] = P.sembol.astype(str)
    P["kaynak"] = P.sembol.map(ev.kaynak); P["sinif"] = P.sembol.map(ev.sinif).astype(np.int8); P["sektor"] = P.sembol.map(ev.sektor).fillna("bilinmiyor")
    P["agirlik"] = P.sembol.map(ev.agirlik).fillna(1.0).astype(np.float32)
    # gün içi sıralamalar yalnız likit satırlarda (eşleştirme hücreleri): oynaklık ondalığı, likidite üçlüsü
    L = P[P.likit]
    P["vd"] = np.int8(-1); P["lt"] = np.int8(-1)
    P.loc[L.index, "vd"] = np.minimum((L.groupby("tarih").vol60.rank(pct=True) * 10).fillna(5).astype(int), 9).astype(np.int8)
    P.loc[L.index, "lt"] = np.minimum((L.groupby("tarih").log_dv20.rank(pct=True) * 3).fillna(1).astype(int), 2).astype(np.int8)
    if isinstance(endeks, pd.DataFrame) and "SPY" in endeks:
        sp = endeks["SPY"].dropna(); boga = (sp > sp.rolling(200).mean()).reindex(P.tarih.values, method="ffill").fillna(False).to_numpy()
        P["rejim"] = np.where(boga, "BOGA", "AYI")
    else:
        P["rejim"] = "bilinmiyor"
    P["donem"] = donem_etiketi(P.tarih).to_numpy()                       # t0 dönemi (bilgi); ölçümde ufuk bazlı purge / embargo etiketleri kullanılır
    for ad, (h, _) in OLAY.items():
        P[f"donem{h}"] = donem_etiketi_ufuk(P.tarih, P[f"bitis{h}"]).to_numpy()
    P["ay"] = P.tarih.dt.to_period("M").astype(str); P["ceyrek"] = P.tarih.dt.to_period("Q").astype(str)
    gunler = np.array(sorted(P.tarih.unique())); gix = pd.Series(np.arange(len(gunler)) // 60, index=gunler); P["blok60"] = P.tarih.map(gix).astype(np.int32)
    P = P.sort_values(["sembol", "tarih"], kind="stable").reset_index(drop=True)
    likit_map = {r["sembol"]: r["likit"] for r in son}
    bilgi = {"sure_sn": round(time.time() - t0, 1), "sembol": int(P.sembol.nunique()), "satir": int(len(P)), "likit_satir": int(P.likit.sum()),
             "r60_tanimli_likit": int((P.likit & P.r60_tanimli).sum()), "donem_t0": P[P.likit].donem.value_counts().to_dict(),
             "donem60_purge_embargo": P[P.likit].donem60.value_counts().to_dict(), "donem250_purge_embargo": P[P.likit].donem250.value_counts().to_dict(),
             "ozelliksiz_satir_toplam": int(sum(r["ozelliksiz"] for r in son)), "atlanan": int(len(args) - len(son))}
    log.info("panel: %s", bilgi)
    return P, likit_map, bilgi


def panel_kaydet(P: pd.DataFrame, yol: str) -> str:
    P.to_pickle(yol); return yol
