# -*- coding: utf-8 -*-
"""
EVREN GENİŞLET v1.0 — hayatta kalan yanlılığına karşı: fiyat verisinde olmayan hisseleri ekler
==============================================================================================
Kaynak liste: {K}/temel_duz.csv (İş Yatırım finansalları 2022-2026; borsadan çıkmış / işlemi durmuş şirketler de dahil)
  + isteğe bağlı {K}/evren_ek_liste.txt (satır başına sembol; elle eklenenler).
Fiyat verisinde (veri_1d_turkey.pkl) olmayan her sembol yfinance'den 10 yıl indirilir (auto_adjust=False — BASLAT B1 ile aynı),
≥60 bar gelenler pkl'ye eklenir. Kaldığı yerden sürer ({K}/evren_ek_durum.json). Pkl yazmadan önce yedek alır.
Çıktı: eklenen / veri yok / hata sayıları ve listeleri; son barı eski olanlar (= borsadan çıkmış adaylar) ayrıca sayılır.

    exec(open(K + "/evren_genislet.py", encoding="utf-8").read())
    EG = evren_genislet(K)
"""
from __future__ import annotations

import json
import logging
import os
import pickle
import shutil
import sys
import time
from typing import Any, Dict, List, Optional

import pandas as pd

EG_SURUM = "1.0"
_eg_log = logging.getLogger("evren_genislet")
if not _eg_log.handlers:
    _h = logging.StreamHandler(sys.stdout)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s evren: %(message)s", "%H:%M:%S"))
    _eg_log.addHandler(_h)
_eg_log.setLevel(logging.INFO)
_eg_log.propagate = False

if any(k in globals() for k in ("eg_aday", "eg_indir", "evren_genislet")) and globals().get("_EG_IMZA") != "evren_genislet":
    raise RuntimeError("çakışma kapısı: bellekte başka bir eg_* ismi var — yeni oturumda çalıştır")
_EG_IMZA = "evren_genislet"


def _eg_norm(s: str) -> str:
    s = str(s).upper().strip()
    return s[:-3] if s.endswith(".IS") else s


def eg_temizle(y: Any) -> Optional[pd.DataFrame]:
    """BASLAT._temizle ile aynı biçim: Open/High/Low/Close/Volume, tz'siz, normalize, Close'u olmayan satır yok."""
    if y is None or not len(y):
        return None
    y = y.dropna(how="all")
    if not len(y):
        return None
    if isinstance(y.columns, pd.MultiIndex):
        y.columns = y.columns.get_level_values(0)
    y = y.rename(columns=str.title)
    if getattr(y.index, "tz", None) is not None:
        y.index = y.index.tz_localize(None)
    y.index = pd.to_datetime(y.index).normalize()
    if not {"Open", "High", "Low", "Close", "Volume"}.issubset(y.columns):
        return None
    y = y[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
    y = y[~y.index.duplicated(keep="last")].sort_index()
    return y if len(y) else None


def eg_aday(K: str, mevcut: List[str]) -> List[str]:
    """temel_duz.csv + evren_ek_liste.txt sembolleri − fiyat verisindekiler."""
    aday: List[str] = []
    yol = os.path.join(K, "temel_duz.csv")
    if os.path.exists(yol):
        t = pd.read_csv(yol, usecols=["sembol"])
        aday += [_eg_norm(s) for s in t["sembol"].dropna().unique()]
    ek = os.path.join(K, "evren_ek_liste.txt")
    if os.path.exists(ek):
        aday += [_eg_norm(l) for l in open(ek, encoding="utf-8").read().splitlines() if l.strip() and not l.startswith("#")]
    m = set(_eg_norm(s) for s in mevcut)
    return sorted(set(a for a in aday if a and a not in m and a.isalnum()))


def _eg_yf(s: str, period: str = "10y") -> Optional[pd.DataFrame]:
    import yfinance as yf
    return eg_temizle(yf.download(s + ".IS", period=period, interval="1d", progress=False, auto_adjust=False))


def eg_indir(K: str, adaylar: List[str], indir: Any = None, min_bar: int = 60) -> Dict[str, Any]:
    """Adayları tek tek indirir; durumu evren_ek_durum.json'a yazar (kaldığı yerden sürer). Döner: {sembol: df} + durum."""
    indir = indir or _eg_yf
    dyol = os.path.join(K, "evren_ek_durum.json")
    durum: Dict[str, str] = json.load(open(dyol, encoding="utf-8")) if os.path.exists(dyol) else {}
    yeni: Dict[str, pd.DataFrame] = {}
    kalan = [a for a in adaylar if durum.get(a) not in ("yok", "kisa")]
    _eg_log.info("aday %d, denenecek %d (daha önce 'yok/kısa' denen atlanır)", len(adaylar), len(kalan))
    t0 = time.monotonic()
    for i, s in enumerate(kalan, 1):
        try:
            df = indir(s)
            if df is None:
                durum[s] = "yok"
            elif len(df) < min_bar:
                durum[s] = "kisa"
            else:
                yeni[s] = df; durum[s] = "eklendi"
        except Exception as e:
            durum[s] = f"hata:{str(e)[:50]}"
        if i % 20 == 0 or i == len(kalan):
            json.dump(durum, open(dyol, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
            _eg_log.info("%d/%d · eklendi %d · %.0fs", i, len(kalan), len(yeni), time.monotonic() - t0)
    return {"yeni": yeni, "durum": durum}


def evren_genislet(K: str, veri_ad: str = "veri_1d_turkey.pkl", indir: Any = None, bayat_gun: int = 30) -> Dict[str, Any]:
    yol = os.path.join(K, veri_ad)
    P = pickle.load(open(yol, "rb"))
    sarmal = isinstance(P, dict) and isinstance(P.get("veri"), dict)
    V: Dict[str, pd.DataFrame] = P["veri"] if sarmal else P
    adaylar = eg_aday(K, list(V))
    if not adaylar:
        _eg_log.info("eklenecek aday yok (temel_duz.csv / evren_ek_liste.txt bulunamadı ya da hepsi veride)")
        return {"eklendi": [], "durum": {}}
    R = eg_indir(K, adaylar, indir=indir)
    yeni = R["yeni"]
    if yeni:
        shutil.copy(yol, yol + time.strftime(".yedek_evren_%Y%m%d_%H%M"))
        for s, df in yeni.items():
            V[s] = df
        if sarmal:
            P["veri"] = V
            if isinstance(P.get("kayit"), dict):
                P["kayit"]["evren_genislet"] = {"surum": EG_SURUM, "tarih": str(pd.Timestamp.now()), "eklenen": sorted(yeni)}
        tmp = yol + ".tmp"
        pickle.dump(P, open(tmp, "wb")); os.replace(tmp, yol)
    son = max(df.index[-1] for df in V.values() if len(df))
    cikmis = sorted(s for s, df in yeni.items() if (son - df.index[-1]).days > bayat_gun)
    durum = R["durum"]
    ozet = {"eklendi": sorted(yeni), "cikmis_gorunen": cikmis, "veri_yok": sorted(k for k, v in durum.items() if v == "yok"),
            "kisa": sorted(k for k, v in durum.items() if v == "kisa"), "hata": sorted(k for k, v in durum.items() if str(v).startswith("hata")),
            "evren": len(V)}
    print(f"EVREN GENİŞLET v{EG_SURUM}: aday {len(adaylar)} | eklendi {len(ozet['eklendi'])} (son barı {bayat_gun}+ gün eski = borsadan çıkmış görünen: {len(cikmis)}) "
          f"| veri yok {len(ozet['veri_yok'])} | kısa {len(ozet['kisa'])} | hata {len(ozet['hata'])} | evren şimdi {len(V)} hisse")
    if cikmis:
        print("  çıkmış görünenler:", ", ".join(cikmis[:40]) + (" ..." if len(cikmis) > 40 else ""))
    if ozet["veri_yok"]:
        print("  yfinance'de verisi olmayanlar (hayatta kalan yanlılığı burada kalır):", ", ".join(ozet["veri_yok"][:40]) + (" ..." if len(ozet["veri_yok"]) > 40 else ""))
    return ozet
