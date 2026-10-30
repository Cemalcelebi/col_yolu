"""D04 — Zaman ve süre davranışı (K55_PLAN D04-S01 … S10). Takvim değil, olaylar arası süre. D04-S07 takvim yalnız A (bilgi); D04-S10 bilgi (değişken yok).
D04-S02 yaklaşımı: 250 günde kapanışın 250 gün tepesinin %80 altında geçirdiği gün (toparlanma yavaşlığı). Hepsi geriye bakar."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .dal_ortak import C_, aralik, getiri, gun_once, hacim, mp, rs, run_uzunlugu
from .hucreler import kaydet
from .istatistik import cusum


def s01_dusus_dip_suresi(d: pd.DataFrame) -> pd.Series:
    C = C_(d); n = len(C); v = C.to_numpy(float); out = np.full(n, np.nan)
    for i in range(250, n):
        w = v[i - 250: i + 1]; it = int(np.argmax(w)); idip = int(np.argmin(w))
        if idip > it:
            out[i] = (idip - it) / max(1, 250 - idip)                      # düşüş süresi / dipten bugüne süre
    return pd.Series(out, index=d.index)


def s02_toparlanma_yavasligi(d: pd.DataFrame) -> pd.Series:
    C = C_(d); tepe = rs(250, C).max(); alt = (C < 0.8 * tepe).astype(float); alt[tepe.isna()] = np.nan; return rs(250, alt).sum()


def _dip_testleri(d: pd.DataFrame, w: int = 120, bant: float = 0.02) -> pd.Series:
    L = d.Low.astype(float); dip = rs(w, L.shift(1)).min(); return ((L <= dip * (1 + bant)) & (L >= dip * (1 - bant))).where(dip.notna())


def s03_dip_testi_sikligi(d: pd.DataFrame) -> pd.Series:
    t = _dip_testleri(d).fillna(False).to_numpy(bool); n = len(t); out = np.full(n, np.nan); son = []
    for i in range(n):
        if t[i]:
            son.append(i)
        son = [j for j in son if i - j <= 250]
        if len(son) >= 3:
            ara = np.diff(son); out[i] = ara[-1] / np.mean(ara[:-1]) if np.mean(ara[:-1]) > 0 else np.nan     # son aralık / önceki aralıkların ortalaması (< 1 sıklaşıyor)
    return pd.Series(out, index=d.index)


def s04_buyuk_hareket_bosluk(d: pd.DataFrame) -> pd.Series:
    r = getiri(d); sd = rs(60, r.shift(1)).std(ddof=0); buyuk = (r.abs() > 2 * sd).where(sd.notna()); g = gun_once(buyuk)
    ort = rs(250, buyuk.astype(float)).mean(); return g * ort                                             # son büyük hareketten bu yana süre × büyük hareket sıklığı (≈ süre / ortalama aralık)


def s05_once_hacim_mi_fiyat_mi(d: pd.DataFrame, w: int = 60) -> pd.Series:
    V = hacim(d); med = rs(20, V.shift(1)).median(); ho = (V > 2 * med).fillna(False).to_numpy(bool)
    r = getiri(d); sd = rs(60, r.shift(1)).std(ddof=0); fo = (r.abs() > 2 * sd).fillna(False).to_numpy(bool); n = len(d); out = np.full(n, np.nan)
    for i in range(w, n):
        hs = np.flatnonzero(ho[i - w + 1: i + 1]); fs = np.flatnonzero(fo[i - w + 1: i + 1])
        if len(hs) and len(fs):
            out[i] = float(fs[0] - hs[0])                                     # > 0: hacim olayı fiyattan önce
    return pd.Series(out, index=d.index)


def s06_kanalda_bekleme(d: pd.DataFrame) -> pd.Series:
    C = C_(d); H = rs(20, C.shift(1)).max(); L = rs(20, C.shift(1)).min(); kirilim = ((C > H) | (C < L)).where(H.notna()); return gun_once(kirilim)


def s07_haftanin_gunu(d: pd.DataFrame) -> pd.Series:
    return pd.Series(pd.DatetimeIndex(d.index).dayofweek.astype(float), index=d.index)


def s08_uzun_hareketsizlik(d: pd.DataFrame) -> pd.Series:
    C = C_(d); r20 = (C / C.shift(20) - 1).abs(); ar20 = rs(20, aralik(d)).median(); med = rs(250, ar20).median()
    return run_uzunlugu(((r20 < 0.05) & (ar20 < med)).where(med.notna()))


def s09_degisim_sirasi(d: pd.DataFrame, w: int = 60) -> pd.Series:
    """Hacim, aralık ve fiyat serilerinde CUSUM değişim tarihleri; son w günde hacim -> aralık -> fiyat sırası tamamlandıysa tamamlanmadan bu yana geçen gün
    (negatif: yakın = yüksek); yoksa NaN. (D10-S06 aynı değişken.)"""
    V = hacim(d).to_numpy(float); A = aralik(d).to_numpy(float); C = np.log(C_(d).to_numpy(float)); n = len(C)
    ch = {k: np.zeros(n, dtype=bool) for k in ("h", "a", "f")}
    for k, x in (("h", np.log1p(V)), ("a", A), ("f", C)):
        for i, _ in cusum(x, 4.0, 250):
            ch[k][i] = True
    out = np.full(n, np.nan); tamam = -1
    for i in range(n):
        if ch["f"][i]:
            a_idx = np.flatnonzero(ch["a"][max(0, i - w): i]); h_idx = np.flatnonzero(ch["h"][max(0, i - w): i])
            if len(a_idx) and len(h_idx) and h_idx[0] < a_idx[-1]:
                tamam = i
        if i >= 250:
            out[i] = -min(i - tamam, w) if tamam >= 0 else -float(w)          # tamamlanma yoksa taban (−w); yakın tamamlanma = yüksek
    return pd.Series(out, index=d.index)


def kaydet_hucreler() -> None:
    kaydet("D04-S01", "D04", "Düşüş süresi / dipten bugüne süre (250 gün)", +1, fonk=s01_dusus_dip_suresi)
    kaydet("D04-S02", "D04", "Toparlanma yavaşlığı (250 günde tepenin %80 altında geçirilen gün; yaklaşım)", +1, fonk=s02_toparlanma_yavasligi, not_="plan tanımının yaklaşımı")
    kaydet("D04-S03", "D04", "Dip testleri sıklaşıyor mu? (son aralık / önceki aralıklar; < 1 sıklaşma)", -1, fonk=s03_dip_testi_sikligi)
    kaydet("D04-S04", "D04", "Büyük hareketler arası boşluk (son büyük hareketten bu yana süre × sıklık)", +1, fonk=s04_buyuk_hareket_bosluk)
    kaydet("D04-S05", "D04", "Önce hacim mi fiyat mı? (60 günde ilk hacim olayı − ilk fiyat olayı, gün)", +1, fonk=s05_once_hacim_mi_fiyat_mi, yontemler=("A", "B"))
    kaydet("D04-S06", "D04", "Kanalda bekleme süresi (son 20 gün kanal kırılımından bu yana gün)", +1, fonk=s06_kanalda_bekleme)
    kaydet("D04-S07", "D04", "Haftanın günü (bilgi; tek başına iz değil)", +1, fonk=s07_haftanin_gunu, yontemler=("A",), not_="düşük öncelik")
    kaydet("D04-S08", "D04", "Uzun hareketsizlik süresi (|r20| < %5 ve dar aralık ardışık gün)", +1, fonk=s08_uzun_hareketsizlik)
    kaydet("D04-S09", "D04", "Değişimlerin sırası (hacim -> aralık -> fiyat CUSUM; tamamlanmadan bu yana gün, negatif)", +1, fonk=s09_degisim_sirasi, yontemler=("A", "B"), not_="D10-S06 aynı değişken")
