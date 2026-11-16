"""tarama_kosu.py — BIST canlı tarama (16 Kasım 2026; öneri modülü TARAMA kapısı). Tek dosya, hata yakalama, log.

İş tanımı: arastirma_cikti/oneri/BIST_TARAMA_IS_TANIMI_2026-11-16.md. Ön kayıt: BIST_TARAMA_2026-11-16.md 'A. ÖN KAYIT' + KONTROL LİSTESİ.
ÖLÇÜLMÜŞ SİNYAL YOK: bu bir ADAY sıralamasıdır, öneri değildir.

Komut:  python arastirma_cikti/oneri/tarama_kosu.py indir   [--canli DIZIN]     yfinance 3y günlük -> DIZIN/bist_3y.pkl (+ hata listesi)
        python arastirma_cikti/oneri/tarama_kosu.py kos     [--canli DIZIN] [--veri DIZIN]   ölçüler + şart + puan -> csv + rapor
Modüller yalnız import edilir (S6_TABAN, SIKISMA_OBEK, D9_YENIDEN, FON_IZI, IZ_KARNE); hiçbiri değiştirilmez.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import logging
import os
import re
import sys
import time
import traceback
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if KOK not in sys.path:
    sys.path.insert(0, KOK)
CIKTI = os.path.join(KOK, "arastirma_cikti", "oneri")
SCR = "/tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad"

log = logging.getLogger("col.bist_tarama")
if not log.handlers:
    _h = logging.StreamHandler(sys.stderr)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s bist_tarama: %(message)s", "%H:%M:%S"))
    log.addHandler(_h)
    log.setLevel(logging.INFO)
    log.propagate = False

# ---------------------------------------------------------------- ÖN KAYITLI SABİTLER (iş tanımı; sonuçtan sonra değişmez)
BT_ESIK: Dict[str, Any] = {
    "tarih": "2026-11-16", "karar_gunu_beklenen": "2026-11-13", "period": "3y",
    "son_n": 10,              # S6 AL / KIRILDI penceresi (geçerli bar)
    "s5_n": 20,               # S5 karar günü penceresi
    "likidite_gun": 20, "likidite_alt": 0.20,
    "tavan_aralik": [-0.05, 0.03], "zirve_dusus": -0.30, "hacim_gun_getiri": 0.05, "hacim_pencere": 20,
    "sicrama": 0.11, "sicrama_gun": 260,
    "bayat_isgunu": 5,        # K3 düzeltmesi (ilk koşudan sonra; SAPMA kaydı raporda): son geçerli bar karar gününden 5 iş gününden eskiyse ölçü yok
    "puan": {"s6_acik": 2, "s6_al10": 2, "s5_20": 1, "ruzgar": 1, "tavan_yakin": 1, "zirve_dusus": 1, "hacim_tepki": 1},
}
UZAK = ["TEHOL", "PEKGY", "ODINE", "ANELE", "MANAS", "IEYHO", "GUNDG", "DSTKF", "OZATD", "TRHOL", "SKYLP"]
MSCI = ["TEHOL", "PEKGY", "IEYHO", "LYDHO", "ALKLC", "ODINE"]
IZLEME = ["PNLSN", "FORTE", "GWIND", "EUPWR", "SEGMN", "TKNKA", "GIPTA", "SVGYO", "KARCL", "YEOTK", "HDFGS", "SKBNK"]
D13_IS_TANIMI = ["ONCSM", "METRO", "ALBRK", "HUNER", "EGEGY", "ULUFA"]
_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


class BTHata(RuntimeError):
    """Durdurucu hata."""


def _sha(yol: str) -> str:
    with open(yol, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ---------------------------------------------------------------- 1) İNDİRME
def bt_evren() -> List[str]:
    s = pd.read_csv(os.path.join(KOK, "sektor_BIST.csv"))
    ev = [str(x).strip().upper() for x in s.sembol.dropna()]
    for w in IZLEME:
        if w not in ev:
            ev.append(w)
    return ev


def bt_indir(canli: str, parca: int = 60) -> Dict[str, Any]:
    import yfinance as yf
    os.makedirs(canli, exist_ok=True)
    ev = bt_evren() + ["XU100"]
    V: Dict[str, pd.DataFrame] = {}
    hata: Dict[str, str] = {}

    def _al(df: pd.DataFrame, t: str) -> Optional[pd.DataFrame]:
        try:
            x = df[t] if isinstance(df.columns, pd.MultiIndex) else df
            x = x[["Open", "High", "Low", "Close", "Adj Close", "Volume"]].dropna(how="all")
            x = x.dropna(subset=["Close"])
            if x.empty:
                return None
            x.index = pd.DatetimeIndex(x.index).tz_localize(None).normalize()
            return x.astype(float)
        except Exception:
            return None

    for i in range(0, len(ev), parca):
        grup = ev[i:i + parca]
        tk = [g + ".IS" for g in grup]
        for deneme in range(3):
            try:
                df = yf.download(tk, period=BT_ESIK["period"], interval="1d", auto_adjust=False, group_by="ticker",
                                 threads=True, progress=False)
                break
            except Exception as ex:
                log.warning("parça %d deneme %d: %s", i, deneme, ex); time.sleep(3); df = None
        for g, t in zip(grup, tk):
            x = _al(df, t) if df is not None else None
            if x is not None:
                V[g] = x
        log.info("indirildi %d / %d", min(i + parca, len(ev)), len(ev))
    # eksikleri tek tek yeniden dene
    for g in [g for g in ev if g not in V]:
        try:
            df = yf.download(g + ".IS", period=BT_ESIK["period"], interval="1d", auto_adjust=False, progress=False)
            x = _al(df, g + ".IS")
            if x is not None:
                V[g] = x
            else:
                hata[g] = "boş veri (Yahoo'da yok / kottan çıkmış olabilir)"
        except Exception as ex:
            hata[g] = f"{type(ex).__name__}: {ex}"[:200]
    yol = os.path.join(canli, "bist_3y.pkl")
    pd.to_pickle({"veri": V, "hata": hata, "zaman": _dt.datetime.now(_dt.timezone.utc).isoformat(), "evren": ev}, yol)
    log.info("kaydedildi %s: %d sembol, %d hata", yol, len(V), len(hata))
    return {"n": len(V), "hata": hata, "yol": yol}


# ---------------------------------------------------------------- 2) ÖLÇÜLER
def gecerli(d: pd.DataFrame) -> pd.DataFrame:
    """SY.sy_veri_hazirla süzgeci (kriz kesiği yok: canlı tarama)."""
    d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float).copy()
    ok = (d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0) & np.isfinite(d[["Open", "High", "Low", "Close"]]).all(axis=1)
    d = d[ok].sort_index()
    d = d[~d.index.duplicated(keep="last")]
    d["Kur"] = 1.0
    return d


def kes(d: pd.DataFrame, karar: pd.Timestamp) -> pd.DataFrame:
    x = d[d.index <= karar]
    if len(x) and x.index.max() > karar:
        raise BTHata("geleceğe bakma: karar sonrası bar")
    return x


def bt_fon_leke(veri: str, karar: pd.Timestamp) -> pd.DataFrame:
    import FON_IZI as F
    G = pd.read_pickle(os.path.join(veri, "G.pkl"))
    if pd.Timestamp(G.bilinme.max()) > karar + pd.Timedelta(days=1):
        raise BTHata("fon tablosunda karar gününden sonra bilinen satır var")
    G = G.copy()
    G["tasf"] = G.sirket.astype(str).str.upper().str.match(F.FI_TASFIYE_RE)
    G["tasf_lot"] = np.where(G.tasf, G.nominal, 0.0)
    son = G.groupby("kod").ay.max().rename("son_ay")
    G = G.join(son, on="kod")
    S = G[G.ay == G.son_ay].groupby("kod").agg(son_ay=("ay", "max"), tasf_lot=("tasf_lot", "sum"), fon_lot=("nominal", "sum"),
                                                tasf_fon=("fon", lambda x: 0))
    S["tasf_fon"] = G[(G.ay == G.son_ay) & G.tasf].groupby("kod").fon.nunique().reindex(S.index).fillna(0).astype(int)
    try:
        dol = pd.read_pickle(os.path.join(veri, "dol.pkl")).set_index("kod")
        S["tasf_pay_sermaye"] = S.tasf_lot / dol.sermaye_lot.reindex(S.index)
    except Exception as ex:
        log.warning("dol.pkl okunamadı: %s", ex); S["tasf_pay_sermaye"] = np.nan
    S["son_ay"] = [f"{a // 12}-{a % 12 + 1:02d}" for a in S.son_ay]
    S["leke"] = S.tasf_lot > 0
    return S


def bt_d13(rapor: str) -> List[str]:
    try:
        m = open(rapor, encoding="utf-8").read()
        blok = m.split("BEKLE")[1].split("KAPANAN")[0]
        return re.findall(r"^\s{2}([A-Z0-9]{3,6})\s", blok, flags=re.M)
    except Exception as ex:
        log.warning("son_rapor okunamadı: %s", ex); return []


def bt_hisse(s: str, d: pd.DataFrame, karar: pd.Timestamp) -> Dict[str, Any]:
    import S6_TABAN as S6
    import SIKISMA_OBEK as SO
    E = BT_ESIK
    r: Dict[str, Any] = {"sembol": s}
    x = kes(d, karar)
    r["son_bar"] = str(x.index[-1].date()) if len(x) else ""
    r["n_bar"] = len(x)
    if len(x) < 30:
        r["not"] = "az bar"; return r
    if x.index[-1] < karar - pd.offsets.BDay(BT_ESIK["bayat_isgunu"]):     # K3: işlem görmeyen hissenin eski barları karar günü ölçüsü değildir
        r["not"] = f"HESAPLANAMADI: işlem görmüyor (son geçerli bar {r['son_bar']})"; return r
    C, H, L, V = x.Close.to_numpy(), x.High.to_numpy(), x.Low.to_numpy(), x.Volume.to_numpy()
    r["kapanis"] = C[-1]
    r["likidite_tl"] = float(np.mean(C[-E["likidite_gun"]:] * V[-E["likidite_gun"]:]))
    for g in (60, 120, 250):
        r[f"r{g}"] = C[-1] / C[-g - 1] - 1 if len(C) > g else np.nan
    if len(C) >= 120:
        mn, mx = C[-120:].min(), C[-120:].max(); r["konum120"] = (C[-1] - mn) / (mx - mn) if mx > mn else np.nan
    else:
        r["konum120"] = np.nan
    r["zirve250_dusus"] = C[-1] / C[-250:].max() - 1 if len(C) >= 250 else np.nan
    Cp = np.r_[np.nan, C[:-1]]
    tr = np.fmax(H, Cp) - np.fmin(L, Cp)
    r["atr250"] = float(np.nanmean((tr / Cp)[-250:])) if len(C) >= 251 else np.nan
    hp = E["hacim_pencere"]
    j = len(C) - hp + int(np.argmax(V[-hp:]))
    r["hacim_gun"] = str(x.index[j].date()); r["hacim_gun_getiri"] = C[j] / C[j - 1] - 1 if j >= 1 else np.nan
    r["hacim5_60"] = float(V[-5:].mean() / V[-60:].mean()) if len(V) >= 60 else np.nan
    sg = E["sicrama_gun"]
    rr = np.abs(C[1:] / C[:-1] - 1)[-sg:]
    r["sicrama"] = int((rr > E["sicrama"]).sum())
    # S6
    try:
        T = S6.s6_taban(x)
        son = T.iloc[-1]; k = E["son_n"]; Tk = T.iloc[-k:]
        acik = bool(son.bolge_id >= 0 and not son.al and not son.kirildi and son.durum in ("YENI", "SURER", "YENIDEN"))
        r["s6_olculur"] = bool(son.olculur)
        r["s6_acik"] = acik
        r["s6_al10"] = bool(Tk.al.any()); r["s6_kir10"] = bool(Tk.kirildi.any())
        r["s6_al_gun"] = str(Tk.index[Tk.al.to_numpy()][-1].date()) if r["s6_al10"] else ""
        r["s6_kir_gun"] = str(Tk.index[Tk.kirildi.to_numpy()][-1].date()) if r["s6_kir10"] else ""
        r["s6_durum"] = str(son.durum); r["s6_sinif"] = str(son.sinif)
        r["s6_n"] = float(son.n) if son.n == son.n else np.nan
        r["s6_bant"] = float(son.bant); r["s6_net"] = float(son.net)
        tavan = np.nan
        if acik:
            tavan = float(son.kutu_ust)
            g = T[T.bolge_id == son.bolge_id]
            r["s6_bolge_bas"] = str(T.index[int(son.kutu_sol_i)].date()); r["s6_bolge_gun"] = int(son.kutu_sag_i - son.kutu_sol_i + 1)
            r["s6_bolge_sinif"] = str(g.sinif.iloc[0])
        elif r["s6_al10"]:
            ia = np.where(T.al.to_numpy())[0][-1]
            tavan = float(T.tavan.iloc[ia - 1])
        r["s6_tavan"] = tavan
        r["tavana_uzaklik"] = C[-1] / tavan - 1 if tavan == tavan else np.nan
        if not r["s6_olculur"]:
            r["s6_not"] = "HESAPLANAMADI (250 geçerli bar yok)"
    except Exception as ex:
        r["s6_not"] = f"HESAPLANAMADI: {type(ex).__name__}: {ex}"[:150]
    # S5
    try:
        X = SO.so_s5(x, "BIST")
        if len(x) < SO.SO_ESIK["gecmis_min"] + 1:
            r["s5_not"] = "HESAPLANAMADI (290 geçerli bar yok)"
        Xk = X.iloc[-E["s5_n"]:]
        r["s5_20"] = bool(Xk.ev5.any())
        if r["s5_20"]:
            t = Xk.index[Xk.ev5.to_numpy()][-1]
            r["s5_gun"] = str(t.date()); r["s5_sinif"] = "DIP" if bool(Xk.loc[t, "ev5_dip"]) else "YOL"
        r["s5_bugun"] = bool(X.s5c.iloc[-1])
    except Exception as ex:
        r["s5_not"] = f"HESAPLANAMADI: {type(ex).__name__}: {ex}"[:150]
    return r


def bt_kos(canli: str, veri: str) -> pd.DataFrame:
    import IZ_KARNE as IK
    import D9_YENIDEN as D9
    onk = os.path.join(CIKTI, "BIST_TARAMA_2026-11-16.md")
    kapi = IK.ik_kontrol_kapisi(onk)            # eksik / HAYIR varsa durur
    log.info("kontrol kapısı açık (%d madde)", kapi["n"])
    P = pd.read_pickle(os.path.join(canli, "bist_3y.pkl"))
    Vham: Dict[str, pd.DataFrame] = P["veri"]; hata = P["hata"]
    bugun = pd.Timestamp(BT_ESIK["tarih"])
    tum_tarih = sorted({t for d in Vham.values() for t in d.index})
    karar = max(t for t in tum_tarih if t < bugun)          # bugünkü bar seans açıkken yarım: karar = önceki son tam bar
    if str(karar.date()) != BT_ESIK["karar_gunu_beklenen"]:
        log.warning("karar günü beklenenden farklı: %s", karar.date())
    log.info("karar günü %s", karar.date())
    Vg = {s: gecerli(d) for s, d in Vham.items()}
    Vg.pop("XU100", None)
    xu = Vham.get("XU100")                                   # endeks: hacim alanı 16 Kas'ta 0; geçerli bar = H > L, C > 0
    if xu is not None:
        xu = xu[(xu.High > xu.Low) & (xu.Close > 0)].sort_index()
    sek = pd.read_csv(os.path.join(KOK, "sektor_BIST.csv"))
    sek_d = dict(zip(sek.sembol.str.upper(), sek.alt_bist))
    # rüzgâr
    try:
        Vk = {s: kes(d, karar) for s, d in Vg.items()}
        R = D9.d9_ruzgar_ref(Vk, sek_d, tarih=karar)
    except Exception as ex:
        log.error("rüzgâr hesaplanamadı: %s", ex); R = pd.DataFrame()
    leke = bt_fon_leke(veri, karar)
    satir = []
    for i, (s, d) in enumerate(sorted(Vg.items())):
        try:
            r = bt_hisse(s, d, karar)
        except Exception as ex:
            r = {"sembol": s, "not": f"HATA: {type(ex).__name__}: {ex}"[:200]}
            log.warning("%s: %s", s, traceback.format_exc(limit=1))
        b = d[d.index > karar]
        if len(b):
            r["bilgi_16kas_kapanis"] = float(b.Close.iloc[-1]); r["bilgi_16kas_degisim"] = float(b.Close.iloc[-1] / d[d.index <= karar].Close.iloc[-1] - 1) if (d.index <= karar).any() else np.nan
        satir.append(r)
        if i % 100 == 0:
            log.info("ölçüldü %d / %d", i, len(Vg))
    T = pd.DataFrame(satir).set_index("sembol")
    T["alt_bist"] = [sek_d.get(s, "") for s in T.index]
    for c in ("ruz", "sepet", "ruzgar", "piy"):
        T[c] = R[c].reindex(T.index) if c in R.columns else np.nan
    T["ruzgar"] = T.ruzgar.fillna(False).astype(bool)
    T["leke"] = leke.leke.reindex(T.index).fillna(False).astype(bool)
    T["fon_son_ay"] = leke.son_ay.reindex(T.index)
    T["tasf_lot"] = leke.tasf_lot.reindex(T.index)
    T["tasf_pay_sermaye"] = leke.tasf_pay_sermaye.reindex(T.index)
    T["uzak"] = T.index.isin(UZAK); T["msci"] = T.index.isin(MSCI)
    d13 = bt_d13(os.path.join(KOK, "rapor", "son_rapor.txt"))
    T["d13"] = T.index.isin(d13)
    T["izleme"] = T.index.isin(IZLEME)
    # likidite alt %20
    liq = T.likidite_tl.dropna()
    esik = float(liq.quantile(BT_ESIK["likidite_alt"]))
    T["likidite_alt20"] = T.likidite_tl < esik
    # bayat: son bar karar gününden eski (işlem görmüyor / durdurulmuş)
    T["bayat"] = pd.to_datetime(T.son_bar, errors="coerce") < karar
    # ŞART
    for c in ("s6_kir10", "s6_acik", "s6_al10", "s5_20"):
        if c not in T.columns:
            T[c] = np.nan
    T["sart"] = (~T.leke) & (~T.uzak) & (~T.likidite_alt20.fillna(True)) & (T.s6_kir10 != True) & T.likidite_tl.notna()  # noqa: E712
    # PUAN (HESAPLANAMADI -> 0)
    p = BT_ESIK["puan"]; a, b_ = BT_ESIK["tavan_aralik"]
    T["p_s6_acik"] = np.where(T.s6_acik == True, p["s6_acik"], 0)  # noqa: E712
    T["p_s6_al10"] = np.where(T.s6_al10 == True, p["s6_al10"], 0)  # noqa: E712
    T["p_s5"] = np.where(T.s5_20 == True, p["s5_20"], 0)  # noqa: E712
    T["p_ruzgar"] = np.where(T.ruzgar, p["ruzgar"], 0)
    T["p_tavan"] = np.where(T.tavana_uzaklik.between(a, b_), p["tavan_yakin"], 0) if "tavana_uzaklik" in T else 0
    T["p_zirve"] = np.where(T.zirve250_dusus <= BT_ESIK["zirve_dusus"], p["zirve_dusus"], 0)
    T["p_hacim"] = np.where(T.hacim_gun_getiri >= BT_ESIK["hacim_gun_getiri"], p["hacim_tepki"], 0)
    T["puan"] = T[["p_s6_acik", "p_s6_al10", "p_s5", "p_ruzgar", "p_tavan", "p_zirve", "p_hacim"]].sum(axis=1)
    T = T.sort_values(["sart", "puan", "likidite_tl"], ascending=[False, False, False])
    T["sira"] = np.where(T.sart, np.arange(1, len(T) + 1), np.nan)
    meta = {"karar": str(karar.date()), "likidite_esik": esik, "hata": hata, "n_indirilen": len(Vham) - (1 if "XU100" in Vham else 0),
            "evren": P.get("evren", []), "zaman": P.get("zaman"), "d13_rapor": d13, "rapor_sha": _sha(os.path.join(KOK, "rapor", "son_rapor.txt")),
            "kod_sha": _sha(os.path.abspath(__file__)), "ruzgar_n": int(T.ruzgar.sum()),
            "piy_medyan": float(R.piy.iloc[0]) if len(R) and "piy" in R else np.nan}
    if xu is not None and len(xu):
        x = kes(xu, karar); C = x.Close.to_numpy()
        meta["xu100"] = {"son": str(x.index[-1].date()), "kapanis": float(C[-1]), "r60": float(C[-1] / C[-61] - 1), "r120": float(C[-1] / C[-121] - 1),
                         "r250": float(C[-1] / C[-251] - 1) if len(C) > 250 else np.nan,
                         "zirve250": float(C[-1] / C[-250:].max() - 1), "zirve_gun": str(x.index[-250:][int(np.argmax(C[-250:]))].date())}
        b = xu[xu.index > karar]
        meta["xu100"]["bilgi_16kas"] = float(b.Close.iloc[-1] / C[-1] - 1) if len(b) else None
    else:
        meta["xu100"] = None
    T.to_csv(os.path.join(CIKTI, "bist_tarama_2026-11-16.csv"), float_format="%.6g")
    with open(os.path.join(canli, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1, default=str)
    bt_rapor(T, meta)
    return T


# ---------------------------------------------------------------- 3) RAPOR
def _y(x: Any, n: int = 1) -> str:
    try:
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            return "HESAPLANAMADI"
        return f"{100 * float(x):+.{n}f}%".replace(".", ",")
    except Exception:
        return "HESAPLANAMADI"


def _s(x: Any, n: int = 2) -> str:
    try:
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            return "-"
        return f"{float(x):.{n}f}".replace(".", ",")
    except Exception:
        return "-"


def _e(x: Any) -> str:
    if x is True or x == True:  # noqa: E712
        return "E"
    if x is False or x == False:  # noqa: E712
        return "-"
    return "?"


def _tablo(T: pd.DataFrame) -> List[str]:
    b = ["| # | Hisse | Puan | Şart | S6 açık (gün, sınıf) | S6 AL10 | S5 20 | Rüzgâr (ruz) | Tavana | Zirve250 | Hacim günü getiri | r60 | r120 | r250 | Konum120 | ATR% | H5/60 | Likidite (mn TL) | Leke / Uzak / MSCI / D13 | Not |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s, r in T.iterrows():
        acik = f"E ({int(r.s6_bolge_gun)}g, {r.s6_bolge_sinif})" if r.get("s6_acik") == True else _e(r.get("s6_acik"))  # noqa: E712
        al = f"E {r.s6_al_gun}" if r.get("s6_al10") == True else _e(r.get("s6_al10"))  # noqa: E712
        s5 = f"E {r.s5_gun} {r.s5_sinif}" if r.get("s5_20") == True else _e(r.get("s5_20"))  # noqa: E712
        ruz = ("E " if r.ruzgar else "- ") + (_y(r.ruz, 0) if r.ruz == r.ruz else "HESAPLANAMADI")
        bay = "/".join(x for x, c in (("LEKE", r.leke), ("UZAK", r.uzak), ("MSCI", r.msci), ("D13", r.d13)) if c) or "-"
        notlar = []
        if r.get("s6_kir10") == True:  # noqa: E712
            notlar.append(f"KIRILDI {r.s6_kir_gun}")
        if r.get("likidite_alt20") == True:  # noqa: E712
            notlar.append("likidite alt %20")
        if r.get("sicrama", 0) and r.sicrama > 0:
            notlar.append(f"sıçrama {int(r.sicrama)}")
        for c in ("s6_not", "s5_not", "not"):
            v = r.get(c)
            if isinstance(v, str) and v:
                notlar.append(v)
        if r.get("bayat") == True:  # noqa: E712
            notlar.append(f"son bar {r.son_bar}")
        sira = "" if r.sira != r.sira else int(r.sira)
        b.append(f"| {sira} | {s} | {int(r.puan)} | {'E' if r.sart else 'H'} | {acik} | {al} | {s5} | {ruz} | {_y(r.get('tavana_uzaklik'))} | "
                 f"{_y(r.zirve250_dusus, 0)} | {_y(r.hacim_gun_getiri)} ({r.hacim_gun}) | {_y(r.r60, 0)} | {_y(r.r120, 0)} | {_y(r.r250, 0)} | "
                 f"{_s(r.konum120)} | {_y(r.atr250)} | {_s(r.hacim5_60)} | {_s(r.likidite_tl / 1e6, 1)} | {bay} | {'; '.join(notlar)} |")
    return b


def bt_rapor(T: pd.DataFrame, meta: Dict[str, Any]) -> str:
    yol = os.path.join(CIKTI, "BIST_TARAMA_2026-11-16.md")
    eski = open(yol, encoding="utf-8").read()
    isaret = "<!-- KOSU SONUCU BU SATIRDAN SONRA (tarama_kosu.py yazar) -->"
    if isaret not in eski:
        raise BTHata("ön kayıt işaret satırı yok")
    on = eski.split(isaret)[0]
    G = T[T.sart]
    ilk = G.head(15)
    xu = meta.get("xu100") or {}
    L: List[str] = [isaret, "", f"## B. ÖZET (karar günü {meta['karar']}; bulgu dili)", ""]
    L.append(f"- Taranan: {meta['n_indirilen']} hisse indirildi, {len(T)} ölçüldü; indirme hatası {len(meta['hata'])}. ŞARTI GEÇEN: {len(G)}.")
    pd_ = G.puan.value_counts().sort_index(ascending=False)
    L.append("- Şartı geçenlerde puan dağılımı: " + ", ".join(f"{int(k)} puan: {int(v)}" for k, v in pd_.items()) + ".")
    L.append("- İlk 5: " + "; ".join(f"{s} ({int(r.puan)} puan)" for s, r in G.head(5).iterrows()) + ".")
    if xu:
        L.append(f"- Piyasa (XU100, {xu['son']}): 60 gün {_y(xu['r60'])}, 120 gün {_y(xu['r120'])}, 250 gün {_y(xu['r250'])}; 250 gün zirvesinden {_y(xu['zirve250'])} "
                 f"(zirve {xu['zirve_gun']}). 16 Kas (yarım bar, bilgi): {_y(xu.get('bilgi_16kas'))}.")
    L.append(f"- Sektör rüzgârı: rüzgârlı hisse {meta['ruzgar_n']} (60 gün piyasa medyanı {_y(meta['piy_medyan'])}); üretim raporu 13 Kas: rüzgârlı sektör 0, piyasa medyanı 60 g -%33,3.")
    L.append("- BIST fon krizi: 31 Ağu 2026 sonrası olağanüstü dönem (tasfiye fonları, tedbirler); 250 gün ölçüleri bu dönemi içerir. Mart 2027 fon tasfiye sonu.")
    L.append(f"- Üretim D13 BEKLE (son_rapor.txt, sha {meta['rapor_sha'][:12]}): {', '.join(meta['d13_rapor'])}"
             f" — iş tanımı listesiyle {'AYNI' if sorted(meta['d13_rapor']) == sorted(D13_IS_TANIMI) else 'FARKLI'}.")
    L.append(f"- Likidite eşiği (alt %20, 20 gün ort işlem değeri): {_s(meta['likidite_esik'] / 1e6, 2)} mn TL; 5.900 TL'lik alım için şartı geçen hiçbir hissede fiili likidite sorunu yok (en düşük şartı geçen > {_s(meta['likidite_esik'] / 1e6, 1)} mn TL/gün).")
    L.append(f"- Koşu: kod sha256 `{meta['kod_sha']}`; indirme {meta.get('zaman')}.")
    L += ["", "## C. İLK 15 (şartı geçenler; puan, eşitlikte likidite)", "",
          "Sütunlar: S6 açık = karar gününde açık taban bölgesi (bölge gün sayısı, açılış sınıfı); AL10 = son 10 barda S6 AL; S5 20 = son 20 barda S5 karar günü (sınıf); "
          "Rüzgâr = D9 bayrağı (ruz = sepet - piyasa medyanı, 60 g); Tavana = C / tavan - 1; Zirve250 = C / 250 g en yüksek kapanış - 1; Hacim günü = son 20 barın en yüksek hacimli günü (bilanço tepkisi vekili); "
          "H5/60 = son 5 gün / 60 gün ort hacim; ATR% = 250 g ort TR / C_önceki.", ""]
    L += _tablo(ilk)
    W = T[T.izleme].copy()
    W = W.reindex([s for s in IZLEME if s in W.index])
    L += ["", "## D. İZLEME LİSTESİ (Cemal; aynı ölçüler, puanlı; '#' = genel sıra)", ""]
    L += _tablo(W)
    eks = [s for s in IZLEME if s not in T.index]
    if eks:
        L.append(f"\nVeri gelmeyen izleme hissesi: {', '.join(eks)}")
    if "YEOTK" in T.index:
        y = T.loc["YEOTK"]
        L += ["", f"YEOTK (Cemal'in pozisyonu / tezi): kapanış {_s(y.kapanis)} TL; r60 {_y(y.r60)}, r120 {_y(y.r120)}, r250 {_y(y.r250)}; 250 g zirveden {_y(y.zirve250_dusus)}; "
              f"konum120 {_s(y.konum120)}; S6 durum {y.get('s6_durum') or 'taban yok'} (açık {_e(y.get('s6_acik'))}, AL10 {_e(y.get('s6_al10'))}, KIRILDI10 {_e(y.get('s6_kir10'))}); "
              f"S5 20 {_e(y.get('s5_20'))}; rüzgâr {_e(y.ruzgar)}; hacim günü {y.hacim_gun} {_y(y.hacim_gun_getiri)}; puan {int(y.puan)}; şart {'E' if y.sart else 'H'}."]
    L += ["", "## E. HARİÇ TUTULANLAR", ""]
    L.append(f"- LEKE (fon tablosunda son raporlu ayda tasfiye fonu pozisyonu): {int(T.leke.sum())}")
    L.append(f"- Uzak listesi: {int(T.uzak.sum())} ({', '.join(T.index[T.uzak])})")
    L.append(f"- Likidite alt %20: {int(T.likidite_alt20.fillna(False).sum())}")
    L.append(f"- Son 10 barda S6 KIRILDI: {int((T.s6_kir10 == True).sum())}")  # noqa: E712
    L.append(f"- Birden çok neden çakışabilir; şartı geçmeyen toplam {int((~T.sart).sum())}. MSCI çıkarma bayrağı (şart değil): {', '.join(T.index[T.msci])}.")
    L.append(f"- Son barı karar gününden eski (işlem görmüyor / durdurulmuş olabilir): {int(T.bayat.sum())} ({', '.join(T.index[T.bayat][:20])})")
    isl = T["not"].astype(str).str.contains("işlem görmüyor") if "not" in T else pd.Series(False, index=T.index)
    L.append(f"- İşlem görmüyor (son geçerli bar karar gününden {BT_ESIK['bayat_isgunu']} iş gününden eski; ölçü HESAPLANAMADI, şart dışı): {int(isl.sum())} ({', '.join(T.index[isl])})")
    eskl = T[T.leke & (T.fon_son_ay < "2026-07")]
    L.append(f"- BİLGİ (şart değişmedi): LEKE'lilerin {len(eskl)}'i son raporlu ayı 2026-07'den eski olan hisseler (fonlar o aydan sonra tutmamış olabilir); "
             f"bunlardan leke dışında şartı geçip puanı >= 3 olan: {', '.join(f'{s_} ({int(r_.puan)})' for s_, r_ in eskl.iterrows() if r_.puan >= 3 and not r_.uzak and r_.likidite_alt20 != True and r_.s6_kir10 != True and r_.likidite_tl == r_.likidite_tl) or 'yok'}.")
    L += ["", "## F. VERİ NOTU", ""]
    L.append(f"- Kaynak yfinance (Yahoo), 3 yıl günlük, auto_adjust=False (ekran fiyatı; bölünme düzeltmeli, temettü düzeltmesiz). Karar günü {meta['karar']} (son TAM bar). "
             "16 Kas barı seans açıkken indirildi (YARIM): yalnız 'bilgi_16kas_*' sütunlarında, hiçbir ölçüye girmedi.")
    L.append(f"- İndirme hatası {len(meta['hata'])}: " + (", ".join(f"{k} ({v[:60]})" for k, v in sorted(meta['hata'].items())) or "yok"))
    L.append(f"- Son 260 barda tek günde |%11| üstü sıçrama olan hisse: {int((T.sicrama > 0).sum())} (bedelli / bölünme düzeltme eksiği olabilir; S6 / S5 ölçüsünü bozabilir; puana girmez, tabloda 'sıçrama' notu).")
    L.append("- Fon tablosu G.pkl: KAP aylık portföy raporları, en geç rapor ayı 2026-09 (bilinme <= 12 Eki); tasfiye fonları sonradan haftalık rapor verir, bu tabloda yok: LEKE alt sınırdır.")
    L.append("- Hayatta kalma: evren bugünün listesi; canlı tarama için doğal.")
    L += ["", "## G. ÖLÇÜLMÜŞ SİNYAL YOK — taban oranlar", "",
          "Bu sıralamanın hiçbir puanı getiri için ölçülmedi. S6 / S5 göz araçları; sektör rüzgârı ABD'de EMARE, BIST'te ölçülmedi; D13 İZ DEĞİL.",
          "Taban oranlar (ONERI_DEFTERI risk süzgeci): BIST'te 12 ayda ikiye katlanma %4-7, yarıya inme %6-7; oynak havuzda %9-16 / %17-21. 3 yılda 10x: ABD mikro-cap ~%1, BIST USD ~%1,85.",
          "Claude yatırım danışmanı değildir; alım-satım kararı Cemal'indir.", "",
          "## H. DOSYA KAPISI İÇİN İLK 5 (KAP'ta bakılacaklar)", ""]
    for s, r in G.head(5).iterrows():
        L.append(f"- {s} ({int(r.puan)} puan, {r.alt_bist}): 3Ç26 gelir / kâr ivmesi (hacim günü {r.hacim_gun} {_y(r.hacim_gun_getiri)}), isimli sözleşme / iş ilişkisi, nakit, borç, "
                 "seyrelme / bedelli (sıçrama " + str(int(r.sicrama)) + "), going concern, fon / tedbir / SPK lekesi.")
    metin = on + "\n".join(L) + "\n"
    if _EPOSTA.search(metin):
        raise BTHata("raporda e-posta deseni var")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    log.info("rapor yazıldı: %s", yol)
    return yol


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="BIST canlı tarama (16 Kas 2026)")
    ap.add_argument("is_", choices=["indir", "kos"])
    ap.add_argument("--canli", default=os.path.join(SCR, "canli"))
    ap.add_argument("--veri", default=os.path.join(SCR, "veri"))
    a = ap.parse_args(argv)
    try:
        if a.is_ == "indir":
            bt_indir(a.canli)
        else:
            bt_kos(a.canli, a.veri)
        return 0
    except Exception as ex:
        log.error("DURDU: %s\n%s", ex, traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
