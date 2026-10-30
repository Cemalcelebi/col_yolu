"""D06 — Göreli güç ve piyasa içindeki konum (SPY, IWM, sektör sepetleri; dal_ortak.EK ile verilir). Bir hissenin yükselmesi değil, diğerlerinden önce
farklılaşmaya başlaması aranır. D06-S01 momentum (Ç121) kıyasına tabidir. Hepsi geriye bakar."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .dal_ortak import C_, EK, PENCERE_KISA, PENCERE_ORTA, getiri, gun_once, hizala, mp, rs, sektor_adi
from .hucreler import kaydet
from .istatistik import cusum


def _endeks_getiri(d: pd.DataFrame, ad: str = "SPY") -> pd.Series:
    e = hizala(EK.get(ad), d.index); return e.pct_change(fill_method=None)


def _sektor_getiri(d: pd.DataFrame) -> pd.Series:
    sg = EK.get("sektor_getiri", {}); s = sektor_adi(d); return hizala(sg.get(s), d.index) if (s and s in sg) else pd.Series(np.nan, index=d.index)


def _kum(r: pd.Series, w: int) -> pd.Series:
    return rs(w, np.log1p(r)).sum()


def s01_rs_ivmesi(p: int):
    def f(d):
        r = getiri(d); m = _endeks_getiri(d); rsp = _kum(r, p) - _kum(m, p); rs60 = _kum(r, 60) - _kum(m, 60); return rsp - rs60 * (p / 60)
    return f


def s02_dusus_direnci(p: int):
    def f(d):
        r = getiri(d); m = _endeks_getiri(d); return r.where(m < -0.01).rolling(p, min_periods=3).mean()
    return f


def s03_sektor_ayrismasi(p: int):
    def f(d):
        return _kum(getiri(d), p) - _kum(_sektor_getiri(d), p)
    return f


def s04_sektor_ici_sira_degisimi(p: int):
    """Kesitsel: r60'ın sektör içi yüzdeliğinin p gün değişimi (panel fonksiyonu)."""
    def f(P: pd.DataFrame) -> pd.Series:
        L = P.likit; q = P.loc[L].groupby(["tarih", "sektor"]).r60.rank(pct=True).reindex(P.index); return q - q.groupby(P.sembol).shift(p)
    return f


def s05_endeksten_once_dip(d: pd.DataFrame, w: int = 60) -> pd.Series:
    C = C_(d).to_numpy(float); S = hizala(EK.get("SPY"), d.index).to_numpy(float); n = len(C); out = np.full(n, np.nan)
    for i in range(w, n):
        c = C[i - w + 1: i + 1]; s = S[i - w + 1: i + 1]
        if np.isfinite(c).all() and np.isfinite(s).sum() >= w // 2:
            out[i] = float(np.nanargmin(s) - np.argmin(c))                  # > 0: hisse dibini endeksten önce yapmış
    return pd.Series(out, index=d.index)


def s06_rs_degisim_noktasi(d: pd.DataFrame) -> pd.Series:
    r = getiri(d); m = _endeks_getiri(d); x = (np.log1p(r) - np.log1p(m)).cumsum().to_numpy(float); cp = cusum(x, 4.0, 250)
    bay = pd.Series(False, index=d.index); yuk = [i for i, y in cp if y == 1]
    if yuk:
        bay.iloc[yuk] = True
    return -gun_once(bay)                                                   # son yukarı değişimden bu yana gün (negatif: yakın = yüksek)


def _beta(d: pd.DataFrame, w: int, kosul):
    r = getiri(d); m = _endeks_getiri(d); mm = m.where(kosul(m)); rr = r.where(kosul(m)); q = max(5, w // 4)
    return rr.rolling(w, min_periods=q).cov(mm) / mm.rolling(w, min_periods=q).var(ddof=0).replace(0, np.nan)


def s07_asagi_beta(d: pd.DataFrame) -> pd.Series:
    return _beta(d, 120, lambda m: m < 0)


def s08_beta_asimetrisi(d: pd.DataFrame) -> pd.Series:
    return _beta(d, 120, lambda m: m > 0) - _beta(d, 120, lambda m: m < 0)


def s09_iwm_goreli(p: int):
    def f(d):
        return _kum(getiri(d), p) - _kum(_endeks_getiri(d, "IWM"), p)
    return f


def s10_korelasyon_kopusu(d: pd.DataFrame) -> pd.Series:
    r = getiri(d); m = _endeks_getiri(d); return rs(60, r).corr(m) - rs(250, r).corr(m)


def kaydet_hucreler() -> None:
    kaydet("D06-S01", "D06", "Göreli güç ivmesi (p gün RS − 60 gün RS'nin p payı)", +1, fabrika=s01_rs_ivmesi, pencereler=(5, 10, 20, 40), not_="momentum (Ç121) kıyası zorunlu")
    kaydet("D06-S02", "D06", "Piyasa düşerken direnç (SPY < −%1 günlerinde hisse ortalama getirisi, p gün)", +1, fabrika=s02_dusus_direnci, pencereler=(60, 120))
    kaydet("D06-S03", "D06", "Sektörden ayrışma (hisse − sektör sepeti, p gün)", +1, fabrika=s03_sektor_ayrismasi, pencereler=PENCERE_KISA, not_="Ç117 sektör düzeyi; hisse ayrışması yeni")
    kaydet("D06-S04", "D06", "Sektör içi sıra değişimi (r60 sektör yüzdeliğinin p gün değişimi; kesitsel)", +1, panel_fonk=s04_sektor_ici_sira_degisimi(20), fabrika=s04_sektor_ici_sira_degisimi, pencereler=PENCERE_ORTA, yontemler=("A", "B"))
    kaydet("D06-S05", "D06", "Endeksten önce dip (60 gün: SPY dip günü − hisse dip günü)", +1, fonk=s05_endeksten_once_dip)
    kaydet("D06-S06", "D06", "Göreli güç değişim noktası (CUSUM; son yukarı değişimden bu yana gün, negatif)", +1, fonk=s06_rs_degisim_noktasi, yontemler=("A", "B"))
    kaydet("D06-S07", "D06", "Düşüşte sınırlı kayıp (aşağı beta, 120 gün; düşük = dirençli)", -1, fonk=s07_asagi_beta)
    kaydet("D06-S08", "D06", "Yükselişte güçlenen tepki (yukarı beta − aşağı beta, 120 gün)", +1, fonk=s08_beta_asimetrisi)
    kaydet("D06-S09", "D06", "Küçüklere göre konum (IWM'ye göre p gün)", +1, fabrika=s09_iwm_goreli, pencereler=(20, 60))
    kaydet("D06-S10", "D06", "Korelasyon kopuşu (hisse–SPY 60 gün − 250 gün korelasyon)", -1, fonk=s10_korelasyon_kopusu)
