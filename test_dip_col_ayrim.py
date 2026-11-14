"""DIP_COL_AYRIM testleri (yalnız SENTETİK veri; gerçek veride getiri ölçmez). Çalıştırma: python test_dip_col_ayrim.py

1) çakışma kapısı  2) sinyal tespiti: sentetik evrende dip16 / dip17 / col çıkar ve FON_IZI tarayıcılarıyla birebir (geçmiş asgari süzgeci
dışında)  3) geçmiş asgari süzgeci (i >= 399 / 199)  4) GELECEĞE BAKMA: seri t'de kesilince aynı sinyal t'de çıkar
  5) kümeleme A / B / C elle kurulmuş sinyallerle  6) D örneklemi
(o gün bar var, pencerede sinyal yok)  7) cetvel çağrısı: oc_olc uçtan uca, ayrım kat noktası oc_kat ile aynı  8) ayrım kuralı (VAR /
ÖLÇÜLEMEDİ / YOK)  9) kapı (sha satırı eksik / tasarım değişti -> durur)  10) mühür kararlılığı  11) e-posta / anahtar yok.
"""
from __future__ import annotations

import copy
import os
import re
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
warnings.filterwarnings("ignore")
import DIP_COL_AYRIM as D  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402


def seri(seed, T=900, bas="2019-01-01"):
    """Kriz + sakin taban + toparlanma döngüleri olan sentetik hisse (bütün barlar geçerli)."""
    rng = np.random.default_rng(seed); idx = pd.bdate_range(bas, periods=T)
    r = rng.normal(0.0005, 0.02, T)
    for k in range(3):
        a = 420 + k * 150
        if a + 140 > T:
            break
        r[a:a + 40] = rng.normal(-0.02, 0.01, 40); r[a + 40:a + 120] = rng.normal(0.0, 0.006, 80); r[a + 120:a + 140] = rng.normal(0.01, 0.01, 20)
    C = 20 * np.exp(np.cumsum(r)); O = np.r_[C[0], C[:-1]]
    H = np.fmax(O, C) * (1 + np.abs(rng.normal(0.004, 0.002, T))); L = np.fmin(O, C) * (1 - np.abs(rng.normal(0.004, 0.002, T)))
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(1e5, 1e6, T).astype(float) * (1 + seed % 5),
                         "Kur": 1.0}, index=idx)


def testler():
    hata = []
    import FON_IZI as F

    # 1) çakışma kapısı
    kod = open(os.path.join(KOK, "DIP_COL_AYRIM.py"), encoding="utf-8").read()
    g = {"__name__": "colab_benzeri", "dca_kume": "baska_dosyanin_adi"}
    try:
        exec(compile(kod, "DIP_COL_AYRIM.py", "exec"), g)
        hata.append("1 çakışma kapısı ad ezmeyi yakalamadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1 beklenmeyen hata: {ex}")

    # 2) sinyal tespiti + FON_IZI ile birebir
    V = {f"S{s:02d}": seri(s) for s in range(40)}
    S = []
    for s, d in V.items():
        S += [(s, t, tur, i) for s_, t, tur, i in D.dca_tara_hisse(s, d)]
    S = pd.DataFrame(S, columns=["sembol", "tarih", "tur", "i"]); S.insert(0, "pazar", "ABD")
    for tur in ("dip16", "dip17", "col"):
        if not (S.tur == tur).any():
            hata.append(f"2 sentetik evrende {tur} sinyali yok")
    for s in ("S00", "S01", "S02", "S03"):
        d = V[s]; pos = {t: i for i, t in enumerate(d.index)}
        a = F.fi_k13_tara({s: d}, F.FI_K16_GEVSEK); b = F.fi_k17_tara({s: d}, F.FI_K17_ESIK); c = F.fi_k24_tara(d, F.FI_K24)
        bek = set()
        if len(a):
            bek |= {(pd.Timestamp(t), "dip16") for t in a.bilgi if pos[pd.Timestamp(t)] >= 399}
        if len(b):
            bek |= {(pd.Timestamp(t), "dip17") for t in b.bilgi if pos[pd.Timestamp(t)] >= 399}
        if len(c):
            bek |= {(pd.Timestamp(t), "col") for t in c[c.kural].tarih if pos[pd.Timestamp(t)] >= 199}
        bul = {(pd.Timestamp(t), tur) for t, tur in zip(S[S.sembol == s].tarih, S[S.sembol == s].tur)}
        if bek != bul:
            hata.append(f"2 {s} FON_IZI ile birebir değil: {len(bek ^ bul)} fark")

    # 3) geçmiş asgari süzgeci
    if len(S) and ((S[S.tur != "col"].i < 399).any() or (S[S.tur == "col"].i < 199).any()):
        hata.append("3 geçmiş asgari süzgeci çalışmıyor")

    # 4) geleceğe bakma: seri t'de kesilince aynı sinyal
    fark = 0; say = 0
    for r in S.itertuples():
        d = V[r.sembol]; y = D.dca_tara_hisse(r.sembol, d[d.index <= r.tarih]); say += 1
        if not any(t == r.tarih and tt == r.tur for _s, t, tt, _i in y):
            fark += 1
    if fark or not say:
        hata.append(f"4 geleceğe bakma: {fark}/{say} sinyal seri t'de kesilince kayboldu")
    # 5) kümeleme
    St = pd.DataFrame([("ABD", "X", pd.Timestamp("2023-01-02"), "dip16", 500), ("ABD", "X", pd.Timestamp("2023-02-01"), "col", 520),
                       ("ABD", "X", pd.Timestamp("2023-09-01"), "col", 700), ("ABD", "Y", pd.Timestamp("2023-03-01"), "col", 400),
                       ("ABD", "Y", pd.Timestamp("2023-05-01"), "dip17", 461), ("ABD", "Z", pd.Timestamp("2023-03-01"), "col", 400),
                       ("ABD", "Z", pd.Timestamp("2023-05-01"), "dip17", 460), ("ABD", "W", pd.Timestamp("2023-03-01"), "col", 400),
                       ("ABD", "W", pd.Timestamp("2023-03-01"), "dip16", 400)],
                      columns=["pazar", "sembol", "tarih", "tur", "i"])
    K = D.dca_kume(St)
    a_ = set(zip(K["A"].sembol, K["A"].tarih)); b_ = set(zip(K["B"].sembol, K["B"].tarih)); c_ = set(zip(K["C"].sembol, K["C"].tarih))
    if a_ != {("X", pd.Timestamp("2023-01-02")), ("Y", pd.Timestamp("2023-05-01"))}:
        hata.append(f"5 A yanlış: {a_}")
    if b_ != {("X", pd.Timestamp("2023-09-01")), ("Y", pd.Timestamp("2023-03-01")), ("Z", pd.Timestamp("2023-03-01"))}:
        hata.append(f"5 B yanlış: {b_}")
    if c_ != {("X", pd.Timestamp("2023-02-01")), ("Z", pd.Timestamp("2023-05-01")), ("W", pd.Timestamp("2023-03-01"))}:
        hata.append(f"5 C yanlış: {c_}")
    cz = K["C"][K["C"].sembol == "Z"]
    if len(cz) != 1 or int(cz.uzaklik.iloc[0]) != 60:
        hata.append("5 C uzaklık yanlış")

    # 6) D örneklemi
    Vd = {"pazar": "ABD", "V": {s: OC.oc_veri_hazirla(d)[0] for s, d in V.items()}, "evren_bas": {}}
    Kx = D.dca_kume(S)
    Dd = D.dca_D(S, Vd, Kx, 0)
    if not len(Dd):
        hata.append("6 D boş")
    for r in Dd.head(200).itertuples():
        ix = Vd["V"][r.sembol].index; k = ix.searchsorted(r.tarih)
        if ix[k] != r.tarih:
            hata.append("6 D o gün bar yok"); break
        si = S[(S.sembol == r.sembol)].i.to_numpy()
        if ((si <= k) & (si >= k - 60)).any():
            hata.append("6 D pencerede sinyal var"); break

    # 7) cetvel çağrısı uçtan uca
    P = OC.oc_panel(Vd)
    Ol = {}
    for k in ("A", "B", "C"):
        X = Kx[k]
        r = OC.oc_olc(X[["sembol", "tarih", "pazar"]], {"ABD": P})
        for kol in ("hucre", "olay", "olasilik", "etiket", "sayim"):
            if kol not in r:
                hata.append(f"7 oc_olc çıktısında {kol} yok")
        Ol[k] = r["olay"]
    AT, AE = D.dca_ayrim(Ol)
    if "genel" not in AE or not len(AT):
        hata.append("7 ayrım tablosu boş")
    x = Ol["C"][Ol["C"].donem == "2016-22"]
    if len(x):
        ay = pd.to_datetime(x.giris).dt.to_period("M").astype(str).to_numpy()
        k1 = OC.oc_kat(x.up100.to_numpy(float), x.es_up100.to_numpy(float), ay)["kat"]
        k2 = D.dca_kat_fark(x, Ol["A"][Ol["A"].donem == "2016-22"], "up100")["kat_C"]
        if np.isfinite(k1) and abs(k1 - k2) > 1e-12:
            hata.append(f"7 kat noktası oc_kat ile aynı değil {k1} {k2}")

    # 8) ayrım kuralı
    rng = np.random.default_rng(1)

    def yap(n, p_olay, p_es, pz="ABD", dn="2023"):
        g = pd.date_range("2023-01-02", periods=n, freq="D")
        return pd.DataFrame({"pazar": pz, "donem": dn, "giris": g, "fark": rng.normal(0, 0.1, n),
                             "up100": (rng.random(n) < p_olay).astype(float), "es_up100": np.full(n, p_es),
                             "dn50": (rng.random(n) < 0.1).astype(float), "es_dn50": np.full(n, 0.1)})
    karar = [(p, d) for p in ("ABD", "AVR") for d in ("2023", "2024-26")]
    Ol8 = {"C": pd.concat([yap(1500, 0.40, 0.10, p, d) for p, d in karar]), "A": pd.concat([yap(1500, 0.10, 0.10, p, d) for p, d in karar]),
           "B": pd.concat([yap(1500, 0.10, 0.10, p, d) for p, d in karar])}
    if D.dca_ayrim(Ol8)[1]["genel"] != "AYRIM VAR":
        hata.append("8 AYRIM VAR bekleniyordu")
    Ol8b = {"C": pd.concat([yap(1500, 0.10, 0.10, p, d) for p, d in karar]), "A": Ol8["A"], "B": Ol8["B"]}
    if D.dca_ayrim(Ol8b)[1]["genel"] != "AYRIM YOK":
        hata.append(f"8 AYRIM YOK bekleniyordu: {D.dca_ayrim(Ol8b)[1]['genel']}")
    Ol8c = {"C": pd.concat([yap(20, 0.9, 0.10, p, d) for p, d in karar]), "A": Ol8["A"], "B": Ol8["B"]}
    if D.dca_ayrim(Ol8c)[1]["genel"] != "ÖLÇÜLEMEDİ":
        hata.append("8 ÖLÇÜLEMEDİ bekleniyordu (n < 30)")
    Ol8d = {"C": pd.concat([yap(300, 0.10, 0.10, p, d) for p, d in karar]), "A": Ol8["A"], "B": Ol8["B"]}
    if D.dca_ayrim(Ol8d)[1]["genel"] != "ÖLÇÜLEMEDİ":
        hata.append("8 ÖLÇÜLEMEDİ bekleniyordu (C n < 1.000, VAR değil)")
    Ol8e = copy.deepcopy(Ol8); Ol8e["C"]["dn50"] = (rng.random(len(Ol8e["C"])) < 0.5).astype(float)
    if D.dca_ayrim(Ol8e)[1]["genel"] == "AYRIM VAR":
        hata.append("8 -%50 katı büyükken AYRIM VAR çıktı")

    # 9) kapı
    with tempfile.TemporaryDirectory() as td:
        y = os.path.join(td, "on.md")
        open(y, "w", encoding="utf-8").write("boş ön kayıt\n")
        try:
            D.dca_kapi(y, git=False); hata.append("9 kapı boş ön kaydı geçirdi")
        except (D.DCAHata, OC.OCHata):
            pass
        metin = OC.oc_kontrol_tablosu() + "\n" + OC.oc_kapi_satirlari() + "\n" + \
            f"DCA_PARAM_SHA: `{D.dca_param_sha()}`\nDCA_TASARIM_SHA: `{'0' * 64}`\nDCA_KOD_SHA: `{D.dca_kod_sha()}`\nSINYAL_SHA: `{'0' * 64}`\n"
        open(y, "w", encoding="utf-8").write(metin)
        try:
            D.dca_kapi(y, git=False); hata.append("9 kapı tasarım sha farkını geçirdi")
        except D.DCAHata as ex:
            if "tasarim" not in str(ex):
                hata.append(f"9 beklenmeyen kapı hatası: {ex}")
        metin = metin.replace("0" * 64, D.dca_tasarim_sha(), 1)
        open(y, "w", encoding="utf-8").write(metin)
        try:
            D.dca_kapi(y, git=False)
        except Exception as ex:
            hata.append(f"9 doğru ön kayıt kapıdan geçmedi: {ex}")
        try:
            D.dca_kapi(y, git=False, S=S); hata.append("9 kapı sinyal sha farkını geçirdi")
        except D.DCAHata:
            pass

    # 10) mühür kararlılığı
    if D.dca_param_sha() != D.dca_param_sha() or D.dca_tasarim_sha() != D.dca_tasarim_sha():
        hata.append("10 sha kararsız")

    # 11) e-posta / anahtar
    for ad in ("DIP_COL_AYRIM.py", "test_dip_col_ayrim.py"):
        m = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.(com|org|net|io)\b", m) or re.search(r"(api[_-]?key|token|secret)\s*=\s*['\"][A-Za-z0-9]{12,}", m, re.I):
            hata.append(f"11 {ad} e-posta / anahtar içeriyor")
    return hata


if __name__ == "__main__":
    h = testler()
    if h:
        print("TEST BAŞARISIZ:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_dip_col_ayrim: 11 test GEÇTİ")
