"""K55 evren: fonsuz ABD evreni + K54 şirket sınıfları + seri sonu işlemi + 50'lik deneme örneklemi (ONKAYIT_K55 bölüm 1).

Girdi: COL_YOLU_ABD.cy_veri_yukle (V_ABD + K34 Yahoo + K34 Tiingo; evren_disi_ABD.csv uygulanmış), K54_SIRKET_DURUMU.csv, K54_EVREN_ESLESTIRME.csv.
Çıktı: V (sembol -> OHLCV, 4b kesimi uygulanmış), EV (sembol başına kaynak, evren_bas, agirlik, sinif, seri_sonu, kesim, cik, sec_ad, sektor), evren_surum.
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd

from .ortak import ALIVE_SINIR, K55Ayar, KOK, cy, log, sha256_dosya, sha256_metin

SERI_SONU = {"y_d100": "d100", "y_d0": "d0"}          # K54 cikis_islemi -> seri sonu işlemi; öteki -> k51


def _k54_oku(A: K55Ayar) -> Tuple[pd.DataFrame, pd.DataFrame]:
    sd_yol = os.path.join(A.k54, "K54_SIRKET_DURUMU.csv"); es_yol = os.path.join(A.k54, "K54_EVREN_ESLESTIRME.csv")
    for y in (sd_yol, es_yol):
        if not os.path.exists(y):
            raise FileNotFoundError(f"K54 dosyası yok: {y} (evren sınıfları olmadan K55 koşulmaz)")
    SD = pd.read_csv(sd_yol); ES = pd.read_csv(es_yol)
    SD["sembol"] = SD.sembol.astype(str); ES["sembol"] = ES.sembol.astype(str)
    return SD, ES


def evren_kur(A: K55Ayar) -> Tuple[Dict[str, pd.DataFrame], pd.DataFrame, str, pd.DataFrame]:
    """Evreni kurar. Sınıf 6 ve K54'te bulunmayan semboller dışarıda; 4b kesimi seriye uygulanır; evren sürümü hesaplanır.
    Dönüş: V, EV, evren_surum, kisa (yükleyici dışı kısa geçmişli semboller; v1.2 madde 6)."""
    C = cy(); Ac = C.CYAyar(veri=A.veri, cikti=A.cikti, pazarlar=("ABD",), is_parcacigi=A.isci)
    eski_indir = C.cy_tiingo_indir
    try:
        C.cy_tiingo_indir = lambda *a, **k: 0                               # ONKAYIT v1.2 madde 9: K55 evren kurulurken ağdan veri indirilmez
        Vs, EV = C.cy_veri_yukle(Ac, C.CY)
    finally:
        C.cy_tiingo_indir = eski_indir
    if "ABD" not in Vs:
        raise RuntimeError("ABD verisi yüklenemedi")
    V = Vs["ABD"]; EV = EV[EV.pazar == "ABD"].copy(); EV["sembol"] = EV.sembol.astype(str)
    SD, ES = _k54_oku(A)
    sd = SD.set_index("sembol"); es = ES.set_index("sembol")
    EV["sinif"] = EV.sembol.map(sd.sinif); EV["cikis_islemi"] = EV.sembol.map(sd.cikis_islemi).fillna("y")
    EV["kesim"] = pd.to_datetime(EV.sembol.map(sd.kesim_tarihi), errors="coerce"); EV["erken_bitti"] = EV.sembol.map(sd.erken_bitti).fillna(False).astype(bool)
    EV["cik"] = EV.sembol.map(es.cik); EV["sec_ad"] = EV.sembol.map(es.sec_ad).fillna("")
    bulunmayan = EV.sembol[EV.sinif.isna()].tolist()
    if bulunmayan:
        log.warning("K54 sınıfı olmayan %d sembol doğrulanamayan (6) sayıldı ve çıkarıldı: %s", len(bulunmayan), bulunmayan[:10])
    EV["sinif"] = EV.sinif.fillna(6).astype(int)
    disari = EV.sembol[EV.sinif == 6].tolist()
    EV = EV[EV.sinif != 6].copy()
    for s in disari:
        V.pop(s, None)
    V = {s: d for s, d in V.items() if s in set(EV.sembol)}
    # 4b kod yeniden kullanımı: seri kesim tarihinde biter (kesim sonrası günler başka şirketin)
    kesilen = 0
    for r in EV.itertuples():
        if r.cikis_islemi == "y_kes" and pd.notna(r.kesim) and r.sembol in V:
            d = V[r.sembol]; d2 = d[d.index <= r.kesim]
            if len(d2) < len(d):
                V[r.sembol] = d2; kesilen += 1
    EV["seri_sonu"] = EV.cikis_islemi.map(SERI_SONU).fillna("k51")
    EV["son_islem"] = EV.sembol.map(lambda s: V[s].index[-1] if s in V and len(V[s]) else pd.NaT)
    EV["ilk_islem"] = EV.sembol.map(lambda s: V[s].index[0] if s in V and len(V[s]) else pd.NaT)
    EV["n_gun"] = EV.sembol.map(lambda s: len(V[s]) if s in V else 0)
    EV["seri_erken"] = EV.son_islem < pd.Timestamp(ALIVE_SINIR)
    sek = C.cy_sektor(Ac, EV); EV["sektor"] = EV.sembol.map(sek).fillna("bilinmiyor")
    EV = EV[EV.n_gun > 0].sort_values("sembol").reset_index(drop=True)
    kisa = _kisa_seriler(A, V, SD)                                       # v1.2 madde 6: yükleyici dışı kısa geçmişli semboller silinmez, raporlanır
    evren_surum = _evren_surum(EV)
    log.info("evren: %d sembol (sınıf: %s); 4b kesilen %d; sınıf 6 / K54 dışı çıkarılan %d; sürüm %s", len(EV), EV.sinif.value_counts().sort_index().to_dict(),
             kesilen, len(disari), evren_surum[:12])
    return V, EV, evren_surum, kisa


def _kisa_seriler(A: K55Ayar, V: Dict[str, pd.DataFrame], SD: pd.DataFrame) -> pd.DataFrame:
    """K51 yükleyicisinin (< 320 gün) dışarıda bıraktığı ya da K55 evreninde bulunmayan semboller: VERİ YETERSİZ (kısa geçmiş) listesi."""
    rows = []
    try:
        import pickle
        with open(os.path.join(A.veri, "V_ABD.pkl"), "rb") as f:
            ham = pickle.load(f)
        ham = ham.get("veri", ham) if isinstance(ham, dict) and "veri" in ham else ham
        for s, d in ham.items():
            if str(s) not in V and hasattr(d, "__len__") and len(d) < 320:
                rows.append({"sembol": str(s), "kaynak": "V_ABD", "n_gun": int(len(d)), "neden": "VERİ YETERSİZ (kısa geçmiş < 320 gün; K51 yükleyicisi dışı)"})
    except Exception as ex:
        log.warning("kısa seri taraması (V_ABD) yapılamadı: %s", ex)
    ky = os.path.join(A.veri, "k34_evren.csv")
    if os.path.exists(ky):
        E = pd.read_csv(ky); disi = set(pd.read_csv(os.path.join(KOK, "evren_disi_ABD.csv")).sembol.astype(str).str.upper()) if os.path.exists(os.path.join(KOK, "evren_disi_ABD.csv")) else set()
        sdx = SD.set_index("sembol").sinif.to_dict() if len(SD) else {}
        for r in E.itertuples():
            s = str(r.sembol)
            if s not in V and s.upper() not in disi and sdx.get(s) != 6:
                rows.append({"sembol": s, "kaynak": f"K34_{r.kaynak}", "n_gun": np.nan, "neden": "VERİ YETERSİZ (K34 fiyat serisi yok ya da < 320 gün; yükleyici dışı)"})
    return pd.DataFrame(rows, columns=["sembol", "kaynak", "n_gun", "neden"])


def _evren_surum(EV: pd.DataFrame) -> str:
    """Evren tablosunun içeriğinden (sembol, kaynak, sınıf, seri sonu, kesim, ilk / son gün, n) ve evren_disi dosyasından sha256."""
    kol = ["sembol", "kaynak", "sinif", "seri_sonu", "n_gun"]
    metin = EV[kol].astype(str).agg("|".join, axis=1).str.cat(sep="\n") + "\n" + EV.ilk_islem.astype(str).str.cat(sep=",") + "\n" + EV.son_islem.astype(str).str.cat(sep=",")
    ed = os.path.join(KOK, "evren_disi_ABD.csv")
    return sha256_metin(metin + (sha256_dosya(ed) if os.path.exists(ed) else ""))


def ornek_sec(EV: pd.DataFrame, n: int, tohum: int) -> pd.DataFrame:
    """Deneme örneklemi: tabakalı (kaynak × sınıf), tohumlu, tekrar üretilebilir. 50 için: V_ABD 1 ×30, K34 Yahoo ×8, Tiingo sınıf 2 ×4, 3 ×4, 5 ×2, 4 ×2."""
    rng = np.random.default_rng(tohum); pay = {("V_ABD", 1): 30, ("K34_yahoo", 1): 8, ("K34_tiingo", 2): 4, ("K34_tiingo", 3): 4, ("K34_tiingo", 5): 2, ("K34_tiingo", 4): 2}
    olcek = n / sum(pay.values()); secilen = []
    for (kay, sn), k in pay.items():
        aday = EV[(EV.kaynak == kay) & (EV.sinif == sn)].sembol.to_numpy()
        if not len(aday):
            aday = EV[EV.sinif == sn].sembol.to_numpy()
        kk = min(len(aday), max(1, int(round(k * olcek))))
        secilen += list(rng.choice(np.sort(aday), size=kk, replace=False))
    kalan = n - len(secilen)
    if kalan > 0:
        havuz = np.sort(EV.sembol[~EV.sembol.isin(secilen)].to_numpy()); secilen += list(rng.choice(havuz, size=min(kalan, len(havuz)), replace=False))
    return EV[EV.sembol.isin(secilen)].reset_index(drop=True)


def evren_daralt(V: Dict[str, pd.DataFrame], EV: pd.DataFrame, EVo: pd.DataFrame) -> Tuple[Dict[str, pd.DataFrame], pd.DataFrame]:
    s = set(EVo.sembol); return {k: v for k, v in V.items() if k in s}, EV[EV.sembol.isin(s)].reset_index(drop=True)
