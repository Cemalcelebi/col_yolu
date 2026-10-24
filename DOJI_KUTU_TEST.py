# =====================================================================
#  DOJI_KUTU_TEST — "Kutuda 3-5 doji varsa birikim/sikisma bolgesidir,
#                    ardindan sert fiyat hareketi gelir"   (2026-10-19, v1.0)
#
#  CEMAL'IN SAVI (19 Eki 23:31)
#    Bir kutu (bolge) icinde sadece 3-5 doji bile varsa orasi birikim / sikisma
#    bolgesidir; en cok aranan bolge budur, cunku ardindan genelde SERT hareket olur.
#    Col tespitinin amaci bu hareketi yakalamak.
#
#  OLCUM
#    Evren   : BIST 583 hisse (sektor_BIST.csv), gunluk, 10 yil
#    Kutu    : GOZ_ESLE.bolge_col v1.3 (hisseye ozel: cekirdek bant 6x, az ayrilma kabul,
#              cok ayrilma dur, inis mumlari kirpilir, pespese 3 buyuk mum = ayrilma)
#    Doji    : |C-O| / (H-L) < 0.10
#    Gruplar : A = kutu + doji >= DOJI_MIN    B = kutu + doji < DOJI_MIN    T = taban (tum gunler)
#              A_dip = A + kutu dipte (onceki 250 gun araliginin alt %35'i)
#    Sonuc   : kutunun son gununden sonraki UFUK bar (kapanistan):
#              sert_yukari  = en yuksek >= +SERT%      sert_asagi = en dusuk <= -SERT%
#              sert_herhangi = ikisinden biri          once_yukari = +SERT% once mi, -SERT/2% once mi
#              goreli: sert esigi hissenin kendi normal gununun SERT_KAT kati da ayrica olculur
#    Standart: donemler ayri (2016-19, 2020-22, 2023-26); bir iz ancak her donemde ayni yonde
#              ve tabandan belirgin (>=1.3x) ise iz sayilir. Ayni kutu bir kez sayilir.
#
#  KURAL_MOTORU: K1 veri  K2 onarim  K3 tarama  K4 ozet  K5 rapor
#  Calistirma: GitHub Actions 'Arastirma' is akisi (yfinance orada calisir) ya da Colab:
#    exec(open('/content/drive/MyDrive/col_tarayici/DOJI_KUTU_TEST.py').read()); R = doji_kutu_test()
# =====================================================================
from __future__ import annotations

import logging
import os
import pickle
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

SURUM = "DOJI_KUTU_TEST v1.1 (2026-10-19: kirilim olcumu + dusus riski)"
dlog = logging.getLogger("col.dojikutu")
if not dlog.handlers:
    _h = logging.StreamHandler(sys.stderr)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s dojikutu: %(message)s", "%H:%M:%S"))
    dlog.addHandler(_h)
    dlog.setLevel(logging.INFO)
    dlog.propagate = False


@dataclass
class DKAyar:
    kok: str = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/content/drive/MyDrive/col_tarayici"
    cikti: Optional[str] = None
    veri_pkl: str = "veri_1d_turkey.pkl"
    evren_csv: str = "sektor_BIST.csv"
    period: str = "10y"
    adim: int = 3                # kutu sonu her 'adim' barda bir denenir
    doji_esik: float = 0.10
    doji_min: int = 3            # Cemal: 3-5 doji yeter
    dip_esik: float = 0.35
    ufuk: int = 60
    sert: float = 20.0           # % — sert hareket
    sert_kat: float = 8.0        # goreli: hissenin normal gununun bu kati
    min_bar_gecmis: int = 260
    donemler: tuple = (("2016-19", "2016-01-01", "2019-12-31"), ("2020-22", "2020-01-01", "2022-12-31"),
                       ("2023-26", "2023-01-01", "2026-12-31"))


# ------------------------------------------------------------------ K1
def k1_veri(ay: DKAyar) -> Dict[str, pd.DataFrame]:
    yol = os.path.join(ay.kok, ay.veri_pkl)
    veri: Dict[str, pd.DataFrame] = {}
    if os.path.exists(yol):
        try:
            p = pickle.load(open(yol, "rb"))
            veri = p.get("veri", p) if isinstance(p, dict) else {}
            veri = {k: v for k, v in veri.items() if isinstance(v, pd.DataFrame)}
            dlog.info("K1: onbellek %d hisse (%s)", len(veri), yol)
        except Exception as ex:
            dlog.warning("K1: onbellek okunamadi: %s", ex)
            veri = {}
    evren = pd.read_csv(os.path.join(ay.kok, ay.evren_csv)).sembol.astype(str).str.upper().tolist()
    eksik = [s for s in evren if s not in veri or len(veri[s]) < 1500]
    if eksik:
        import yfinance as yf
        dlog.info("K1: %d hisse indirilecek (%s)", len(eksik), ay.period)
        t0 = time.monotonic()
        for i in range(0, len(eksik), 40):
            grup = eksik[i:i + 40]
            try:
                y = yf.download([s + ".IS" for s in grup], period=ay.period, interval="1d", group_by="ticker",
                                auto_adjust=False, progress=False, threads=True)
            except Exception as ex:
                dlog.warning("K1: grup indirilemedi (%s): %s", grup[0], ex)
                continue
            for s in grup:
                try:
                    d = y[s + ".IS"] if len(grup) > 1 else y
                    if isinstance(d.columns, pd.MultiIndex):
                        d.columns = d.columns.get_level_values(-1)
                    d = d.rename(columns=str.title)[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
                    if d.index.tz is not None:
                        d.index = d.index.tz_localize(None)
                    d.index = d.index.normalize()
                    d = d[~d.index.duplicated(keep="last")]
                    if len(d) >= 300:
                        veri[s] = d.astype(float)
                except Exception as ex:
                    dlog.debug("K1: %s: %s", s, ex)
            dlog.info("K1: %d/%d indirildi (%.0f sn)", min(i + 40, len(eksik)), len(eksik), time.monotonic() - t0)
        try:
            tmp = yol + ".dk.tmp"
            pickle.dump({"kayit": str(pd.Timestamp.now()), "veri": veri}, open(tmp, "wb"), protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, yol)
        except Exception as ex:
            dlog.warning("K1: onbellek yazilamadi: %s", ex)
    veri = {s: veri[s] for s in evren if s in veri}
    if len(veri) < 100:
        raise RuntimeError(f"K1: yalniz {len(veri)} hisse var — veri yetersiz")
    dlog.info("K1: %d hisse hazir", len(veri))
    return veri


# ------------------------------------------------------------------ K2
def k2_onarim(ay: DKAyar, veri: Dict[str, pd.DataFrame]) -> int:
    """bolunme_onar.py (bedelsiz/bolunme) — Yahoo BIST bedelsizlerini duzeltmez."""
    y = os.path.join(ay.kok, "bolunme_onar.py")
    if not os.path.exists(y):
        dlog.warning("K2: bolunme_onar.py yok — onarim atlandi")
        return 0
    g: Dict[str, Any] = {"__name__": "bolunme_onar_dk"}
    exec(compile(open(y, encoding="utf-8").read(), y, "exec"), g)
    n = 0
    for s in list(veri):
        try:
            ol = g["bo_bul"](veri[s])
            if ol:
                yeni, kayit = g["bo_onar"](veri[s], ol)
                if any(r["onarildi"] for r in kayit):
                    veri[s] = yeni
                    n += 1
        except Exception as ex:
            dlog.debug("K2: %s: %s", s, ex)
    dlog.info("K2: %d hissede bedelsiz/bolunme onarildi", n)
    return n


# ------------------------------------------------------------------ K3
def k3_tarama(ay: DKAyar, veri: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    sys.path.insert(0, ay.kok)
    import GOZ_ESLE as G                       # bolge_col v1.3 (tek kaynak)
    gay = G.GozAyar()
    t0 = time.monotonic()
    satir: List[Dict[str, Any]] = []
    for k, (s_ad, df) in enumerate(veri.items()):
        D = G.bolge_hazirla(df)
        H, L, C = D["H"], D["L"], D["C"]
        n = len(df)
        ix = df.index
        son_bolge_bas = -999; son_bolge_son = -999
        kutu_A = False
        for en in range(ay.min_bar_gecmis, n - 1, ay.adim):
            r = D["ref"][en]
            if not np.isfinite(r) or r <= 0:
                continue
            ileri = slice(en + 1, min(n, en + 1 + ay.ufuk))
            if en + 1 >= n:
                continue
            up = float(H[ileri].max() / C[en] - 1) * 100
            dn = float(L[ileri].min() / C[en] - 1) * 100
            # once hangisi: +sert mi, -sert/2 mi
            hu = np.where(H[ileri] >= C[en] * (1 + ay.sert / 100))[0]
            hd = np.where(L[ileri] <= C[en] * (1 - ay.sert / 200))[0]
            once = "yukari" if (len(hu) and (not len(hd) or hu[0] < hd[0])) else ("asagi" if len(hd) else "yok")
            g_sert = ay.sert_kat * r
            kayit = {"sembol": s_ad, "tarih": ix[en], "ref": r, "up": up, "dn": dn, "once": once,
                     "tam_ufuk": int(en + ay.ufuk < n), "sert_goreli_up": up >= g_sert, "sert_goreli_dn": dn <= -g_sert}
            # taban: her gun (adimla) — kutu sarti yok
            kayit["grup"] = "T"
            kayit["donchian"] = bool(en >= 21 and C[en] > C[en - 20:en].max())   # v1.1: taban kirilim (20 gun zirvesi)
            satir.append(dict(kayit))
            w = G.bolge_col(D, en, gay)
            if not w:
                continue
            s0, e0 = w
            dj = int((D["go"][s0:e0 + 1] < ay.doji_esik).sum())
            # denetim 24 Eki: eskiden 'ayni kutu' = baslangic +-5 bar; kutu basi kayinca (medyan ~14 gun) ayni kutu yeniden A
            # sayiliyordu (A olaylarinin %58'i onceki A kutusuyla ortusuyordu). Simdi: onceki kutuyla ortusen kutu ayni kutudur.
            ayni = s0 <= son_bolge_son
            son_bolge_son = max(son_bolge_son, e0)
            if not ayni:
                son_bolge_bas, kutu_A = s0, False
                grp = "A" if dj >= ay.doji_min else "B"   # kutu ilk goruldugunde
            elif dj >= ay.doji_min and not kutu_A:
                grp = "A"                                 # kutu sonradan 3. dojisini buldu: tarayicinin sinyal ani
            else:
                continue
            if grp == "A":
                kutu_A = True
            o = slice(max(0, s0 - 250), s0)
            if s0 - max(0, s0 - 250) >= 60:
                tl, th = L[o].min(), H[o].max()
                dip = float((np.median(C[s0:e0 + 1]) - tl) / (th - tl)) if th > tl else np.nan
            else:
                dip = np.nan
            # v1.1: KIRILIM — kutu tavani (en yuksek kapanis) ufuk icinde asilirsa, sonuc kirilim kapanisindan
            tavan = float(C[s0:e0 + 1].max())
            kb = np.where(C[en + 1:min(n, en + 1 + ay.ufuk)] > tavan * 1.002)[0]
            if len(kb) and en + 1 + kb[0] + ay.ufuk < n:
                b = en + 1 + int(kb[0]); ik = slice(b + 1, b + 1 + ay.ufuk)
                hu2 = np.where(H[ik] >= C[b] * (1 + ay.sert / 100))[0]
                hd2 = np.where(L[ik] <= C[b] * (1 - ay.sert / 200))[0]
                kayit.update(kirilim=True, k_up=float(H[ik].max() / C[b] - 1) * 100, k_dn=float(L[ik].min() / C[b] - 1) * 100,
                             k_once="yukari" if (len(hu2) and (not len(hd2) or hu2[0] < hd2[0])) else ("asagi" if len(hd2) else "yok"))
            else:
                kayit.update(kirilim=False)
            kayit.update(grup=grp, doji=dj, uz=e0 - s0 + 1, dip=dip,
                         doji_oran=dj / (e0 - s0 + 1))
            satir.append(kayit)
        if (k + 1) % 100 == 0:
            dlog.info("K3: %d/%d hisse (%.0f sn)", k + 1, len(veri), time.monotonic() - t0)
    t = pd.DataFrame(satir)
    t = t[t.tam_ufuk == 1].reset_index(drop=True)
    dlog.info("K3: %d kayit (T %d, A %d, B %d) %.0f sn", len(t), int((t.grup == "T").sum()),
              int((t.grup == "A").sum()), int((t.grup == "B").sum()), time.monotonic() - t0)
    return t


# ------------------------------------------------------------------ K4
def _ozet(g: pd.DataFrame, ay: DKAyar) -> Dict[str, Any]:
    if not len(g):
        return {"n": 0}
    return {"n": len(g),
            "sert_yukari_%": round(100 * (g.up >= ay.sert).mean(), 1),
            "sert_asagi_%": round(100 * (g.dn <= -ay.sert).mean(), 1),
            "agir_dusus_%": round(100 * (g.dn <= -ay.sert / 2).mean(), 1),
            "sert_herhangi_%": round(100 * ((g.up >= ay.sert) | (g.dn <= -ay.sert)).mean(), 1),
            "goreli_yukari_%": round(100 * g.sert_goreli_up.mean(), 1),
            "goreli_asagi_%": round(100 * (g.dn <= -ay.sert_kat * g.ref).mean(), 1),   # hissenin kendi normal gununun 8 kati
            "once_yukari_%": round(100 * (g.once == "yukari").mean(), 1),
            "medyan_en_yuksek_%": round(float(g.up.median()), 1),
            "medyan_en_dusuk_%": round(float(g.dn.median()), 1)}


def k4_ozet(ay: DKAyar, t: pd.DataFrame) -> pd.DataFrame:
    grup = {"T (taban: her gun)": t[t.grup == "T"],
            "B (kutu, doji < %d)" % ay.doji_min: t[t.grup == "B"],
            "A (kutu, doji >= %d)" % ay.doji_min: t[t.grup == "A"],
            "A_dip (A + dipte)": t[(t.grup == "A") & (t.dip <= ay.dip_esik)],
            "B_dip (B + dipte: A_dip'in esi, denetim 24 Eki)": t[(t.grup == "B") & (t.dip <= ay.dip_esik)],
            "A5_dip (doji >= 5 + dipte)": t[(t.grup == "A") & (t.doji >= 5) & (t.dip <= ay.dip_esik)]}
    def _kir(g):    # kirilim kapanisindan olculen sonuclar, _ozet ile ayni alanlar
        g = g[g.get("kirilim", pd.Series(False, index=g.index)).fillna(False).astype(bool)]
        return g.assign(up=g.k_up, dn=g.k_dn, once=g.k_once, sert_goreli_up=g.k_up >= ay.sert_kat * g.ref)
    T = t[t.grup == "T"]
    grup.update({"K_T (taban kirilim: 20 gun zirvesi)": T[T.donchian.fillna(False).astype(bool)],
                 "K_B (dojisiz kutu kirildi)": _kir(t[t.grup == "B"]),
                 "K_A (doji kutusu kirildi)": _kir(t[t.grup == "A"]),
                 "K_A_dip (dipteki doji kutusu kirildi)": _kir(t[(t.grup == "A") & (t.dip <= ay.dip_esik)])})
    satir = []
    for ad, bas, son in ay.donemler:
        m = (t.tarih >= bas) & (t.tarih <= son)
        for gad, g in grup.items():
            satir.append({"donem": ad, "grup": gad, **_ozet(g[m.loc[g.index]], ay)})
    for gad, g in grup.items():
        satir.append({"donem": "HEPSI", "grup": gad, **_ozet(g, ay)})
    oz = pd.DataFrame(satir)
    # iz denetimi: ayni donemin tabanina (T) gore kat
    taban = oz[oz.grup.str.startswith("T")].set_index("donem")
    for kol in ("sert_yukari_%", "sert_herhangi_%", "once_yukari_%", "sert_asagi_%", "agir_dusus_%", "goreli_asagi_%", "goreli_yukari_%"):
        kat = []
        for _, r in oz.iterrows():
            tb = taban[kol].get(r["donem"], np.nan) if kol in taban.columns else np.nan
            kat.append(round(r[kol] / tb, 2) if (np.isfinite(tb) and tb > 0 and np.isfinite(r.get(kol, np.nan))) else np.nan)
        oz[kol.replace("_%", "_kat")] = kat
    return oz


# ------------------------------------------------------------------ K5
def k5_rapor(ay: DKAyar, oz: pd.DataFrame, cikti: str) -> str:
    dlog.info("K5: rapor")
    kol = ["donem", "grup", "n", "sert_yukari_%", "sert_yukari_kat", "sert_asagi_%", "sert_asagi_kat",
           "agir_dusus_%", "agir_dusus_kat", "goreli_yukari_%", "goreli_yukari_kat", "goreli_asagi_%", "goreli_asagi_kat", "once_yukari_%", "once_yukari_kat", "medyan_en_yuksek_%", "medyan_en_dusuk_%"]
    sat = [f"# DOJI KUTU TESTI — {pd.Timestamp.now():%Y-%m-%d %H:%M}", "",
           f"Sav: kutuda >= {ay.doji_min} doji -> ardindan sert hareket (+-%{ay.sert:g}, {ay.ufuk} bar). "
           f"kat = ayni donemin tabanina (her gun) gore.", "",
           "| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
    for _, r in oz.iterrows():
        sat.append("| " + " | ".join("" if pd.isna(r.get(k)) else str(r.get(k)) for k in kol) + " |")
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "DOJI_KUTU_rapor.md"), "w", encoding="utf-8").write(metin)
    return metin


def doji_kutu_test(ay: Optional[DKAyar] = None) -> Dict[str, Any]:
    ay = ay or DKAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "doji_kutu")
    os.makedirs(cikti, exist_ok=True)
    t0 = time.monotonic()
    veri = k1_veri(ay)
    k2_onarim(ay, veri)
    t = k3_tarama(ay, veri)
    t[t.grup != "T"].to_csv(os.path.join(cikti, "doji_kutu_kutular.csv.gz"), index=False)
    oz = k4_ozet(ay, t)
    oz.to_csv(os.path.join(cikti, "doji_kutu_ozet.csv"), index=False)
    k5_rapor(ay, oz, cikti)
    dlog.info("BITTI %.0f sn -> %s", time.monotonic() - t0, cikti)
    return {"tablo": t, "ozet": oz, "cikti": cikti}


if __name__ == "__main__":
    R = doji_kutu_test()
    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print(R["ozet"].to_string(index=False))
