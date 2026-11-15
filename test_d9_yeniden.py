"""test_d9_yeniden — D9_YENIDEN.py sentetik testleri (veri gerekmez).

1) D9_PARAM == COL_v1 sabitleri (ast)            2) d9_uzun_ref == COL_v1.uzun_col_olc (birebir kopya)
3) d9_uzun_seri (vektörlü) == d9_uzun_ref her bar  4) d9_ruzgar_ref == COL_v1.sektor_ruzgar; d9_ruzgar_panel == d9_ruzgar_ref her gün
5) geleceğe bakma: seri t'de kesilince D9 ve rüzgâr aynı   6) sinyal satırları (a / b / c) ve sektörsüz pazar
7) cetvel çağrısı: OC.oc_olc sentetik olaylarla çalışır, birleştirme oc_etiket ile   8) kapı: ön kayıt yok / bozuk -> durur
9) e-posta / anahtar taraması
Çalıştır: python test_d9_yeniden.py
"""
import io
import os
import re
import sys
import tempfile
import contextlib
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
warnings.filterwarnings("ignore")

import D9_YENIDEN as D9  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    import COL_v1 as CV  # noqa: E402

GECTI, KALDI = [], []


def kontrol(ad, kosul, ek=""):
    (GECTI if kosul else KALDI).append(ad)
    print(("  OK   " if kosul else "  HATA ") + ad + (f"  ({ek})" if ek else ""))


def sentetik_hisse(n, tohum, col=None, trend=0.0, bas="2015-01-01", bosluk=None):
    """col=(a, b): a..b barları dar bant + küçük mum (dipte çöl); önce düşüş."""
    rng = np.random.default_rng(tohum)
    r = rng.normal(trend, 0.025, n)
    if col:
        a, b = col
        r[max(0, a - 150):a] = rng.normal(-0.006, 0.02, a - max(0, a - 150))
        r[a:b] = rng.normal(0, 0.006, b - a)
        r[b:] = rng.normal(0.003, 0.02, n - b)
    C = 100 * np.exp(np.cumsum(r))
    O = C * (1 + rng.normal(0, 0.003, n))
    rngd = np.abs(rng.normal(0, 0.01 if col is None else 0.008, n)) + 0.002
    if col:
        rngd[col[0]:col[1]] = np.abs(rng.normal(0, 0.004, col[1] - col[0])) + 0.001
    H = np.maximum(O, C) * (1 + rngd); L = np.minimum(O, C) * (1 - rngd)
    V = rng.integers(1000, 50000, n).astype(float)
    ix = pd.bdate_range(bas, periods=n)
    df = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=ix)
    if bosluk is not None:
        df = df.drop(df.index[bosluk])
    return df


def main():
    print("== test_d9_yeniden ==")
    # 1) parametre
    kontrol("D9_PARAM == COL_v1 sabitleri", D9.d9_col_v1_param() == D9.D9_PARAM, str(D9.d9_col_v1_param()))
    kontrol("COL_v1 bellek sabitleri de aynı", all(getattr(CV, k) == v for k, v in D9.D9_PARAM.items()))
    try:
        D9.D9_PARAM["UZUN_BANT"] = 1.6; D9.d9_param_denetle(); kontrol("param değişince durur", False)
    except D9.D9Hata:
        kontrol("param değişince durur", True)
    finally:
        D9.D9_PARAM["UZUN_BANT"] = 1.50

    # 2-3) D9 kopyası ve vektörlü
    hisseler = {f"S{i}": sentetik_hisse(900, i, col=(450, 780) if i % 2 == 0 else None) for i in range(6)}
    hisseler["G1"] = sentetik_hisse(900, 77, col=(400, 820), bosluk=list(range(300, 310)))
    fark_ref, fark_vek, d9_say = 0, 0, 0
    for s, df in hisseler.items():
        U = D9.d9_uzun_seri(df)
        for i in range(300, len(df), 3):
            t = df.index[i]
            a = CV.uzun_col_olc(df, t); b = D9.d9_uzun_ref(df, t)
            if a != b and not (a and b and all((a[k] == b[k]) or (pd.isna(a[k]) and pd.isna(b[k])) for k in a)):
                fark_ref += 1
            uz = (b or {}).get("uzun", "")
            if uz != U.uzun.iat[i]:
                fark_vek += 1
            d9_say += bool(uz)
    kontrol("d9_uzun_ref == COL_v1.uzun_col_olc", fark_ref == 0, f"fark {fark_ref}")
    kontrol("d9_uzun_seri == d9_uzun_ref (her 3. bar)", fark_vek == 0, f"fark {fark_vek}")
    kontrol("sentetik çöl D9 olarak tespit edildi", d9_say > 20, f"D9 gün {d9_say}")
    kontrol("çölsüz trendli hissede D9 yok", not D9.d9_uzun_seri(sentetik_hisse(900, 5, trend=0.004)).D9.any())

    # 4) rüzgâr
    veri = {}
    sek = {}
    for i in range(18):
        sektor = "XA" if i < 6 else ("XB" if i < 12 else "XC")
        tr = 0.004 if sektor == "XA" else (0.0 if sektor == "XB" else -0.002)
        bos = list(range(500, 503)) if i == 3 else None
        df = sentetik_hisse(700, 100 + i, trend=tr, bosluk=bos)
        if i == 7:
            df = df.iloc[:640]   # verisi durmuş hisse (bayat)
        veri[f"H{i}"] = df; sek[f"H{i}"] = sektor
    veri["Y1"] = sentetik_hisse(700, 999)   # sektörsüz
    CV._SEKTOR = dict(sek); CV.VERI = veri
    fark_cv, fark_pan, rz_say = 0, 0, 0
    Vd = OC._oc_veri_sar(veri, "BIST")
    RP = D9.d9_ruzgar_panel(Vd, sek)
    for t in list(Vd["V"]["H0"].index[80::7]):
        A = CV.sektor_ruzgar(veri, t); B = D9.d9_ruzgar_ref(veri, sek, t)
        if not A.drop(columns=[]).equals(B):
            ok = (A.index.equals(B.index) and np.allclose(A.ruz.astype(float), B.ruz.astype(float), equal_nan=True)
                  and (A.ruzgar == B.ruzgar).all())
            fark_cv += not ok
        Bt = D9.d9_ruzgar_ref(Vd["V"], sek, t)
        d = RP["tarih"].get_loc(t)
        for s in Bt.index:
            v1 = float(Bt.ruz[s]); v2 = RP["ruz"][d, RP["kol"][s]]
            if not ((np.isnan(v1) and np.isnan(v2)) or abs(v1 - v2) < 1e-9):
                fark_pan += 1
            if bool(Bt.ruzgar[s]) != bool(RP["ruzgar"][d, RP["kol"][s]]):
                fark_pan += 1
            rz_say += bool(Bt.ruzgar[s])
    kontrol("d9_ruzgar_ref == COL_v1.sektor_ruzgar", fark_cv == 0, f"fark {fark_cv}")
    kontrol("d9_ruzgar_panel == d9_ruzgar_ref (her 7. gün, her hisse)", fark_pan == 0, f"fark {fark_pan}")
    kontrol("yükselen sektörde rüzgâr bulundu", rz_say > 10, f"rüzgâr hisse-gün {rz_say}")

    # 5) geleceğe bakma: seri t'de kesilince aynı
    t = Vd["V"]["H0"].index[400]
    kes = {s: x[x.index <= t] for s, x in Vd["V"].items()}
    RPk = D9.d9_ruzgar_panel({"V": kes, "evren_bas": {}}, sek)
    dk = RPk["tarih"].get_loc(t); d = RP["tarih"].get_loc(t)
    ayni = all((np.isnan(RP["ruz"][d, RP["kol"][s]]) and np.isnan(RPk["ruz"][dk, RPk["kol"][s]])) or
               abs(RP["ruz"][d, RP["kol"][s]] - RPk["ruz"][dk, RPk["kol"][s]]) < 1e-12 for s in kes)
    kontrol("geleceğe bakma: rüzgâr t'de kesilince aynı", ayni)
    df = hisseler["S0"]; U = D9.d9_uzun_seri(df)
    ayni2 = all(D9.d9_uzun_seri(df.iloc[:i + 1]).D9.iat[-1] == U.D9.iat[i] for i in range(400, 900, 25))
    kontrol("geleceğe bakma: D9 t'de kesilince aynı", ayni2)

    # 6) satırlar
    Vd2 = OC._oc_veri_sar({**veri, **{k: v for k, v in hisseler.items()}}, "BIST")
    eski = D9.d9_sektor
    D9.d9_sektor = lambda p, E=D9.D9_ESIK: dict(sek) if p == "BIST" else {}
    try:
        Dd = D9.d9_durum(Vd2, "BIST")
        Da = D9.d9_durum(Vd2, "AVR")
    finally:
        D9.d9_sektor = eski
    a_, b_, c_ = D9.d9_satir(Dd, "a"), D9.d9_satir(Dd, "b"), D9.d9_satir(Dd, "c")
    kontrol("satır a = D9, b ⊂ a, c ∩ a = ∅", len(a_) == Dd.D9.sum() and set(map(tuple, b_[["sembol", "tarih"]].values)) <= set(map(tuple, a_[["sembol", "tarih"]].values))
            and not (set(map(tuple, c_[["sembol", "tarih"]].values)) & set(map(tuple, a_[["sembol", "tarih"]].values))))
    kontrol("sektörsüz pazar: b ve c boş", len(D9.d9_satir(Da, "b")) == 0 and len(D9.d9_satir(Da, "c")) == 0 and len(D9.d9_satir(Da, "a")) > 0)
    tr = D9.d9_tercil_sinir(Dd)
    kontrol("tercil sınırları sıralı", "BIST" in tr and tr["BIST"][0] <= tr["BIST"][1])

    # 7) cetvel çağrısı (40 hisseli sentetik pazar)
    pazar = {f"P{i}": sentetik_hisse(800, 500 + i, trend=0.0005 * (i % 5)) for i in range(40)}
    Vp = OC._oc_veri_sar(pazar, "ABD"); P = OC.oc_panel(Vp)
    olay = pd.DataFrame({"sembol": [f"P{i}" for i in range(0, 40, 2) for _ in range(2)],
                         "tarih": [Vp["V"]["P0"].index[k] for _ in range(20) for k in (300, 330)], "pazar": "ABD"})
    S = D9.d9_olc_satir(olay, {"ABD": P})
    kontrol("cetvel çağrısı: hücre tablosu + etiket", len(S["hucre"]) == 3 and S["etiket"]["genel"] in
            ("ÖLÇÜLEMEDİ", "İZ DEĞİL", "VERİ YOK", "İZ DEĞİL (AVR verisi yok)") or S["etiket"]["genel"].startswith(("EMARE", "İZ")))
    kontrol("cetvel tekilleştirmesi (aynı hissede 30 gün arayla ikinci olay düşer)",
            S["sayim"]["ABD"]["tekil"] > 0 and int(S["olay"].groupby("sembol").size().max()) == 1, str(S["sayim"]["ABD"]))
    rp = OC.oc_rapor(S, "test")
    kontrol("oc_rapor biçimi", "OLASILIK" in rp.upper() and "Hücre tablosu" in rp)

    # 8) kapı
    with tempfile.TemporaryDirectory() as tmp:
        try:
            D9.d9_onkayit_dogrula(os.path.join(tmp, "yok.md"), git=False); kontrol("kapı: ön kayıt yok -> durur", False)
        except D9.D9Hata:
            kontrol("kapı: ön kayıt yok -> durur", True)
        y = os.path.join(tmp, "b.md")
        open(y, "w").write(f"D9_ESIK_SHA: `{'0' * 64}`\nD9_PARAM_SHA: `{D9.d9_sha(D9.D9_PARAM)}`\nD9_KOD_SHA: `{'0' * 64}`\nCOL_V1_SHA: `{'0' * 64}`\n")
        try:
            D9.d9_onkayit_dogrula(y, git=False); kontrol("kapı: sha tutmuyor -> durur", False)
        except D9.D9Hata:
            kontrol("kapı: sha tutmuyor -> durur", True)
        y2 = os.path.join(tmp, "c.md")
        open(y2, "w").write(f"D9_ESIK_SHA: `{D9.d9_sha(D9.D9_ESIK)}`\nD9_PARAM_SHA: `{D9.d9_sha(D9.D9_PARAM)}`\n"
                            f"D9_KOD_SHA: `{D9._d9_sha_dosya(D9.D9_YOL['kod'])}`\nCOL_V1_SHA: `{D9._d9_sha_dosya(D9.D9_YOL['col_v1'])}`\n")
        kontrol("kapı: doğru sha ile açılır (git hariç)", D9.d9_onkayit_dogrula(y2, git=False)["esik"] == D9.d9_sha(D9.D9_ESIK))

    # 9) e-posta / anahtar
    ep = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    anahtar = re.compile(r"(api[_-]?key|token|secret|password)\s*=\s*['\"][A-Za-z0-9]{12,}", re.I)
    sorun = []
    for yol in [D9.D9_YOL["kod"], os.path.abspath(__file__)] + [os.path.join(D9.D9_YOL["cikti"], f) for f in os.listdir(D9.D9_YOL["cikti"])] \
            if os.path.isdir(D9.D9_YOL["cikti"]) else [D9.D9_YOL["kod"], os.path.abspath(__file__)]:
        if os.path.isfile(yol) and yol.endswith((".py", ".md", ".json")):
            m = open(yol, encoding="utf-8").read()
            if ep.search(m) or anahtar.search(m):
                sorun.append(yol)
    kontrol("e-posta / anahtar yok", not sorun, str(sorun))

    print(f"\n{len(GECTI)} geçti, {len(KALDI)} kaldı")
    if KALDI:
        print("KALAN:", KALDI)
        sys.exit(1)


if __name__ == "__main__":
    main()
