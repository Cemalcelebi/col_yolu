"""gt7_sagla — GT7 bağımsız yeniden üretim (K11): K2 ABD 2020-22 DİPTE hücresinin n'i ve SEÇİM / SEÇİM_O ortalaması, ham seriden düz döngüyle.

GOZ_TESPIT / MUM_IZI_HAVUZ ölçü fonksiyonları KULLANILMAZ; yalnız veri yükleyici (MUM_IZI.mi_veri), dondurulmuş olay dosyası, yeniden kurulmuş G40 serisi
(k2r_g40.pkl) ve gt5_olay.json beşlik sınırları okunur. Rejim, evren şartları, R15, ATRP20 ve beşlik burada yeniden yazıldı.
Çalıştır: python arastirma_cikti/goz_tespit/gt7_sagla.py
"""
import json
import os
import pickle
import sys

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, KOK)
import MUM_IZI as MI  # noqa: E402  (yalnız veri yükleyici)

KESIM = 0.276760218650567
KES = pd.Timestamp("2022-12-31")
A0, A1 = pd.Timestamp("2020-01-01"), pd.Timestamp("2022-12-31")


def pazartesi(x):
    x = pd.Timestamp(x)
    return (x - pd.Timedelta(days=x.dayofweek)).normalize()


def main():
    G = pickle.load(open("/root/.kasa/ham/goz_tespit/k2/k2r_g40.pkl", "rb"))
    g40 = {pd.Timestamp(p): v for p, v in zip(G.pazartesi, G.G40) if np.isfinite(v)}
    sinir = json.load(open(os.path.join(KOK, "arastirma_cikti/goz_tespit/gt5_olay.json"), encoding="utf-8"))["besli_sinir"]["ABD"]["d2022"]

    def dip(D):
        p = pazartesi(D)
        for geri in (1, 2, 3):                       # D'nin haftasından önceki son bilinen hafta
            q = p - pd.Timedelta(days=7 * geri)
            if q in g40:
                return g40[q] <= KESIM
        return None

    OL = pickle.load(open("/root/.kasa/ham/goz_tespit/k2/k2_olay.pkl", "rb"))
    OL = OL[(OL.pazar == "ABD") & (OL.kol == "K2") & (OL.hucre == "ABD|d2022")]
    R = MI.mi_veri("ABD", "/tmp/mum_izi/acik"); V = {s: d for s, d in R["V"].items() if len(d) >= 2}; GEC = R.get("gecersiz", {})
    on = {}
    for s, d in V.items():
        O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
        TR = np.empty(len(C)); TR[0] = H[0] - L[0]
        for i in range(1, len(C)):
            TR[i] = max(H[i], C[i - 1]) - min(L[i], C[i - 1])
        cs = np.r_[0.0, np.cumsum(TR)]; atr = np.full(len(C), np.nan)
        for i in range(19, len(C)):
            atr[i] = (cs[i + 1] - cs[i - 19]) / 20 / C[i]
        gec = pd.DatetimeIndex(GEC.get(s)) if GEC.get(s) is not None else pd.DatetimeIndex([])
        on[s] = (d.index, O, H, L, C, atr, gec.sort_values())

    def r15(s, k):
        ix, O, H, L, C, atr, gec = on[s]
        return C[k + 15] / O[k + 1] - 1

    def besli(a):
        return 1 + sum(1 for b in sinir if a > b)

    def evren_mi(s, k):
        ix, O, H, L, C, atr, gec = on[s]
        if k < 139 or k + 15 >= len(C) or ix[k + 15] > KES or not (A0 <= ix[k + 1] <= A1):
            return False
        if not (O[k + 1] > 0 and O[k + 1] > L[k - 19:k + 1].min() * 0.98):
            return False
        if np.mean(O[k - 19:k + 1] == C[k - 19:k + 1]) > 0.30 or not np.isfinite(atr[k]):
            return False
        g = ((gec >= ix[k - 19]) & (gec <= ix[k])).sum(); v = k + 1 - (k - 19)
        return g / (g + v) <= 0.20

    olay = []
    for _, e in OL.iterrows():
        D = pd.Timestamp(e.tarih)
        if dip(D) is not True:
            continue
        ix, O, H, L, C, atr, gec = on[e.sembol]; k = int(e.t)
        assert ix[k] == D
        if k + 15 >= len(C) or ix[k + 15] > KES or not (A0 <= ix[k + 1] <= A1):
            continue
        if not (O[k + 1] > L[k - int(e.L) + 1:k + 1].min() * 0.98):
            continue                                  # STOP_ALTI (GT5 kuralı)
        olay.append((e.sembol, k, D))
    gunler = sorted(set(D for _, _, D in olay)); zorla = {}
    for s, k, D in olay:
        zorla.setdefault(D, set()).add((s, k))
    # aynı gün forced: üç kolun olay günleri evrene zorla girer; bu hücre için yalnız K2 değil üç kol gerekir
    OL3 = pickle.load(open("/root/.kasa/ham/goz_tespit/k2/k2_olay.pkl", "rb")); OL3 = OL3[(OL3.pazar == "ABD") & OL3.hucre.isin(["ABD|d1619", "ABD|d2022"])]
    for _, e in OL3.iterrows():
        D = pd.Timestamp(e.tarih)
        if D in zorla:
            ix, O, H, L, C, atr, gec = on[e.sembol]; k = int(e.t)
            if k + 15 < len(C) and ix[k + 15] <= KES and O[k + 1] > L[k - int(e.L) + 1:k + 1].min() * 0.98 and A0 <= ix[k + 1] <= A1:
                zorla[D].add((e.sembol, k))
    gun_ev = {}
    for D in gunler:
        rows = []
        for s, (ix, *_r) in on.items():
            j = ix.searchsorted(D)
            if j < len(ix) and ix[j] == D and (evren_mi(s, j) or (s, j) in zorla[D]):
                rows.append((r15(s, j), besli(on[s][5][j])))
        gun_ev[D] = rows
    S, SO = [], []
    for s, k, D in olay:
        r = r15(s, k); b = besli(on[s][5][k]); rows = gun_ev[D]
        ev = [x for x, _ in rows]; eb = [x for x, q in rows if q == b]
        if len(eb) < 5:
            continue
        S.append(r - np.mean(ev) if len(ev) >= 30 else np.nan); SO.append(r - np.mean(eb))
    Z = json.load(open(os.path.join(KOK, "arastirma_cikti/goz_tespit/gt7_ozet.json"), encoding="utf-8"))["tablo"]["K2"]["ABD|d2022"]["DİPTE"]
    out = {"n_bagimsiz": len(SO), "n_rapor": Z["n"], "SECIM_O_bagimsiz": float(np.mean(SO)), "SECIM_O_rapor": Z["SECIM_O"]["ort"],
           "SECIM_bagimsiz": float(np.nanmean(S)), "SECIM_rapor": Z["SECIM"]["ort"], "SECIM_O_medyan_bagimsiz": float(np.median(SO)),
           "SECIM_O_medyan_rapor": Z["SECIM_O_medyan"], "gun": len(gunler)}
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
