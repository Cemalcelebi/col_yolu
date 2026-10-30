"""K55 veri kalitesi denetimi (Faz 0 madde 1): sembol başına kapsam, boşluk, sıfır hacim, aşırı getiri, bölünme benzeri sıçrama, OHLC tutarlılığı,
yinelenen tarih, şirket eşleştirmesi; evren düzeyinde özet. Çıktı K55_VERI_KALITESI.csv + K55_VERI_KAPSAMI.md (raporlama.py).
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

ESIK = {"bosluk_gun": 5, "asiri_getiri": 1.0, "sert_hareket_log": np.log(1.8), "sifir_hacim_pay": 0.20, "min_gun": 260, "ozellik_gun": 260 + 60}


def sembol_kalite(s: str, d: pd.DataFrame) -> Dict[str, Any]:
    """Tek sembol: OHLCV serisinin kalite ölçüleri (yalnız seri; evren bilgisi evren_kalite'de eklenir)."""
    idx = pd.DatetimeIndex(d.index); n = len(d); out: Dict[str, Any] = {"sembol": s, "n_gun": n, "ilk": idx[0] if n else pd.NaT, "son": idx[-1] if n else pd.NaT}
    if n < 2:
        out.update({"yinelenen_tarih": 0, "bosluk_sayi": 0, "bosluk_max_gun": 0, "sifir_hacim_pay": np.nan, "asiri_getiri_sayi": 0, "sert_hareket_sayi": 0, "ohlc_hata": 0, "sirali": True, "eksiksiz": False, "ozellik_yeterli": False})
        return out
    out["yinelenen_tarih"] = int(idx.duplicated().sum()); out["sirali"] = bool(idx.is_monotonic_increasing)
    bd = pd.bdate_range(idx[0], idx[-1]); eksik = bd.difference(idx)
    # ardışık eksik iş günü blokları (tatiller ~9 gün/yıl tek tek; > ESIK ardışık = boşluk)
    bos_sayi = 0; bos_max = 0
    if len(eksik):
        pos = bd.get_indexer(eksik); kir = np.flatnonzero(np.diff(pos) != 1); bloklar = np.split(pos, kir + 1)
        uzun = [len(b) for b in bloklar if len(b) > ESIK["bosluk_gun"]]; bos_sayi = len(uzun); bos_max = max(uzun) if uzun else 0
    out["bosluk_sayi"] = bos_sayi; out["bosluk_max_gun"] = int(bos_max)
    V = d.Volume.astype(float); out["sifir_hacim_pay"] = float((V <= 0).mean())
    C = d.Close.astype(float); r = C.pct_change(fill_method=None)
    out["asiri_getiri_sayi"] = int((r.abs() > ESIK["asiri_getiri"]).sum())
    lr = np.log(C / C.shift(1)); vr = V / V.shift(1).replace(0, np.nan)
    # sert hareket (bilgi; v1.2): |günlük hareket| > %80 ve ters yönlü hacim. Seriler bölünme + temettü düzeltmeli; tam evren örneklemesinde bunlar
    # bölünme değil haber günü hareketleri çıktı (ABEO, AGEN, ALNY ...). Eksiksizlik tanımına girmez.
    sic = (lr.abs() > ESIK["sert_hareket_log"]) & (((lr < 0) & (vr > 1.8)) | ((lr > 0) & (vr < 0.55)))
    out["sert_hareket_sayi"] = int(sic.fillna(False).sum())
    out["ohlc_hata"] = int(((d.High < d.Low) | (d.Close > d.High * 1.0001) | (d.Close < d.Low * 0.9999) | (d.Open > d.High * 1.0001) | (d.Open < d.Low * 0.9999) | (C <= 0)).sum())
    out["ozellik_yeterli"] = bool(n >= ESIK["ozellik_gun"])                 # MIN_GUN özellik + en az bir 60 günlük sonuç penceresi
    out["eksiksiz"] = bool(n >= ESIK["min_gun"] and out["yinelenen_tarih"] == 0 and out["sirali"] and out["ohlc_hata"] == 0 and out["sifir_hacim_pay"] <= ESIK["sifir_hacim_pay"] and bos_max == 0)
    return out


def evren_kalite(V: Dict[str, pd.DataFrame], EV: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Bütün evren: sembol tablosu + özet (kaç hisse eksiksiz, kaçında tarihsel veri eksik, kaç sembol şirketle eşleşti, delist sınıfları)."""
    rows = [sembol_kalite(s, V[s]) for s in EV.sembol if s in V]
    Q = pd.DataFrame(rows).merge(EV[["sembol", "kaynak", "sinif", "seri_sonu", "seri_erken", "cik", "sec_ad", "sektor", "evren_bas"]], on="sembol", how="left")
    Q["cik_var"] = Q.cik.notna(); Q["sektor_var"] = Q.sektor.ne("bilinmiyor")
    Q["tarihsel_eksik"] = (Q.bosluk_sayi > 0) | (Q.n_gun < ESIK["min_gun"]) | (Q.sifir_hacim_pay > ESIK["sifir_hacim_pay"])
    ozet = {"sembol": int(len(Q)), "eksiksiz": int(Q.eksiksiz.sum()), "tarihsel_eksik": int(Q.tarihsel_eksik.sum()), "bosluklu": int((Q.bosluk_sayi > 0).sum()),
            "kisa_seri": int((Q.n_gun < ESIK["min_gun"]).sum()), "sifir_hacim_yuksek": int((Q.sifir_hacim_pay > ESIK["sifir_hacim_pay"]).sum()),
            "sert_hareketli_bilgi": int((Q.sert_hareket_sayi > 0).sum()), "ozellik_yeterli": int(Q.ozellik_yeterli.sum()), "asiri_getirili": int((Q.asiri_getiri_sayi > 0).sum()), "ohlc_hatali": int((Q.ohlc_hata > 0).sum()),
            "yinelenen_tarihli": int((Q.yinelenen_tarih > 0).sum()), "cik_eslesen": int(Q.cik_var.sum()), "sektor_bilinen": int(Q.sektor_var.sum()),
            "seri_erken_biten": int(Q.seri_erken.sum()), "sinif": Q.sinif.value_counts().sort_index().to_dict(), "seri_sonu": Q.seri_sonu.value_counts().to_dict(),
            "kaynak": Q.kaynak.value_counts().to_dict(), "ilk_gun_medyan": str(Q.ilk.median().date()) if len(Q) else "", "son_gun_max": str(Q.son.max().date()) if len(Q) else ""}
    return Q, ozet
