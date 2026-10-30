"""K55 gelecek bilgisi sızıntısı testleri (ONKAYIT_K55 bölüm 10; Faz 0 madde 5).
(a) kesme testi: değişken fonksiyonu seri t'de kesilince aynı değeri verir (her hücre için zorunlu).
(b) olumlu kontrol: geleceğe bakan yapay değişken (t+60 getirisi) pipeline'da çok büyük etki vermeli (dedektör çalışıyor).
(c) olumsuz kontrol: rastgele değişken etki vermemeli.
(d) olay etiketi: olay getirisi yalnız t0+1 … t0+ufuk verisinden; seri t0'dan sonra değiştirilirse (ufuk dışı) etiket değişmez, pencere içi değişirse değişir.
(e) eşleşmiş kontrol: kontrol satırlarının tarihi sinyal tarihinden en çok gun_tol gün uzak; kullanılan sütunlar geriye bakan ölçüler.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Sequence

import numpy as np
import pandas as pd

from .eslestirme import UZAK
from .olay_tanimlari import ileri_getiri, sembol_olaylari
from .ortak import GUN_TOL, OLAY


def kesme_testi(fonk: Callable[[pd.DataFrame], pd.Series], d: pd.DataFrame, noktalar: Sequence[int], tol: float = 1e-9) -> Dict[str, Any]:
    """Her t için fonk(d)[t] == fonk(d[:t+1])[t] (NaN == NaN). Dönüş: gecti, hata listesi."""
    tam = np.asarray(fonk(d), float); hatalar = []
    for t in noktalar:
        if t < 0 or t >= len(d):
            continue
        kes = np.asarray(fonk(d.iloc[: t + 1]), float)
        a, b = tam[t], kes[-1]
        if not ((np.isnan(a) and np.isnan(b)) or (np.isfinite(a) and np.isfinite(b) and abs(a - b) <= tol * max(1.0, abs(a)))):
            hatalar.append({"t": int(t), "tam": float(a), "kesik": float(b)})
    return {"gecti": not hatalar, "nokta": len(noktalar), "hata": hatalar[:10], "hata_sayi": len(hatalar)}


def gelecek_degisken(d: pd.DataFrame, h: int = 60) -> pd.Series:
    """Olumlu kontrol: t+h kapanışı / t+1 açılışı (GELECEĞE BAKAR; yalnız dedektör testi için)."""
    O = d.Open.to_numpy(float); C = d.Close.to_numpy(float); r, _ = ileri_getiri(O, C, h, False, "k51"); return pd.Series(r, index=d.index)


def rastgele_degisken_uret(tohum: int) -> Callable[[pd.DataFrame], pd.Series]:
    """Olumsuz kontrol: sembol başına tohumlu rastgele gürültü (geçmişe bile bakmaz)."""
    import hashlib

    def f(d: pd.DataFrame) -> pd.Series:
        kim = int(hashlib.sha256(f"{d.index[0]}|{len(d)}|{float(d.Close.iloc[0]):.6f}".encode()).hexdigest()[:8], 16)   # süreçten bağımsız, tekrar üretilebilir
        rng = np.random.default_rng(tohum + kim); return pd.Series(rng.standard_normal(len(d)), index=d.index)
    return f


def olay_etiketi_testi(d: pd.DataFrame, likit: np.ndarray, t0: int, ufuk: str = "Y60") -> Dict[str, Any]:
    """t0 olayının etiketi: pencere DIŞI (t0+h+1 …) fiyatlar değiştirilince aynı kalmalı, pencere İÇİ (t0+h) değiştirilince değişmeli."""
    h, esik = OLAY[ufuk]
    def olay_var(dd):
        rows, _ = sembol_olaylari("X", dd, likit); return any(r["i"] == t0 and r["ufuk"] == ufuk for r in rows)
    temel = olay_var(d)
    d1 = d.copy(); d1.iloc[t0 + h + 1 :, d1.columns.get_loc("Close")] = d1.Close.iloc[t0 + h + 1 :] * 5.0   # pencere dışı
    d2 = d.copy(); d2.iloc[t0 + h, d2.columns.get_loc("Close")] = d2.Open.iloc[t0 + 1] * (1 + esik + 0.5) if not temel else d2.Open.iloc[t0 + 1] * 0.5
    disi_ayni = olay_var(d1) == temel; ici_degisti = olay_var(d2) != temel
    return {"gecti": bool(disi_ayni and ici_degisti), "temel": temel, "pencere_disi_ayni": bool(disi_ayni), "pencere_ici_degisti": bool(ici_degisti)}


def eslesme_testi(X: pd.DataFrame, havuz: pd.DataFrame, gun_tol: int = GUN_TOL) -> Dict[str, Any]:
    """Eşleşmiş kontrol satırlarının (kontrol_kimlik 'sembol@index') tarihi sinyal tarihinden en çok gun_tol işlem günü uzak ve sembol farklı."""
    gunler = np.array(sorted(havuz.tarih.unique())); gix = {g: i for i, g in enumerate(gunler)}; hata = 0; n = 0
    for r in X.itertuples():
        if not isinstance(r.kontrol_kimlik, str) or not r.kontrol_kimlik:
            continue
        for kim in r.kontrol_kimlik.split(";"):
            s, ix = kim.split("@"); ix = int(ix); n += 1
            if ix not in havuz.index:
                hata += 1; continue
            kt = havuz.loc[ix, "tarih"]; ks = havuz.loc[ix, "sembol"]
            if ks == r.sembol or abs(gix.get(kt, -10 ** 6) - gix.get(r.tarih, 10 ** 6)) > gun_tol:
                hata += 1
    return {"gecti": hata == 0, "kontrol": n, "hata": hata, "kullanilan_sutunlar": list(UZAK) + ["vd", "lt", "trend", "rejim", "sektor"]}
