"""K24_YENIDEN testleri (yalnız SENTETİK veri; gerçek veride getiri ölçmez). Çalıştırma: python test_k24_yeniden.py

1) çakışma kapısı  2) sinyal tespiti: ky_tara = FON_IZI.fi_k24_tara kural satırları (SAPMA-1 sonrası) birebir
3) GELECEĞE BAKMA: seri t'de kesilince aynı tespit (aynı dusus / L1); SAPMA-1 gerekçesi: t < 199 sinyali tam seride var, kesik seride yok
4) L1 (1. evre süresi) bağımsız kaba kuvvet hesabıyla aynı  5) tercil / derinlik kovaları  6) cetvel çağrısı: OC.oc_olc uçtan uca + rapor
7) kapı: doğru ön kayıt geçer, sha farkı / satır eksik durur  8) eski kayıt alıntıları IZ_KARNE metninde  9) olay sha sıradan bağımsız
10) e-posta / anahtar yok.
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
warnings.filterwarnings("ignore", category=RuntimeWarning)
import FON_IZI as F  # noqa: E402
import K24_YENIDEN as KY  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402


def _seri(tohum: int, T: int = 900, bas: str = "2018-01-01") -> pd.DataFrame:
    """Sentetik hisse: 150 barlık düşüş / yükseliş rejimleri, 60 barlık oynak / sakin dönemler (K24 sinyali üretir)."""
    rng = np.random.default_rng(tohum); idx = pd.bdate_range(bas, periods=T); a = np.arange(T)
    sig = np.where((a // 60) % 2 == 0, 0.035, 0.008); dr = np.where((a // 150) % 2 == 0, -0.004, 0.002)
    C = 50 * np.exp(np.cumsum(rng.normal(dr, sig)))
    O = np.r_[C[0], C[:-1]]; H = np.fmax(O, C) * 1.005; L = np.fmin(O, C) * 0.995
    Vol = rng.integers(5e4, 5e5, T).astype(float)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": Vol}, index=idx)


def _L1_kaba(c: np.ndarray, t: int) -> int:
    """L1'in bağımsız hesabı: SMA20'yi ayrı döngüyle; a = t-4'ten geriye, >= 3 ardışık SMA20 üstü kapanışlık son dizinin sonu."""
    n = len(c); sma = np.full(n, np.nan)
    for i in range(19, n):
        sma[i] = c[i - 19:i + 1].mean()
    ust = [bool(np.isfinite(sma[i]) and c[i] > sma[i]) for i in range(n)]
    a = t - 4
    for j in range(a - 1, -1, -1):
        if ust[j]:
            k = j; run = 0
            while k >= 0 and ust[k]:
                run += 1; k -= 1
            if run >= 3:
                return a - 1 - j
    return a - 1 - 19


def testler():
    hata = []

    # 1) çakışma kapısı
    kod = open(os.path.join(KOK, "K24_YENIDEN.py"), encoding="utf-8").read()
    g = {"__name__": "colab_benzeri", "ky_tara": "baska_dosyanin_adi", "__file__": os.path.join(KOK, "K24_YENIDEN.py")}
    try:
        exec(compile(kod, "K24_YENIDEN.py", "exec"), g); hata.append("1 çakışma kapısı durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1 beklenmeyen hata: {ex}")
    g2 = {"__name__": "colab_benzeri", "__file__": os.path.join(KOK, "K24_YENIDEN.py")}
    try:
        exec(compile(kod, "K24_YENIDEN.py", "exec"), g2); exec(compile(kod, "K24_YENIDEN.py", "exec"), g2)
    except RuntimeError as ex:
        hata.append(f"1 aynı dosyanın yeniden yüklenmesi durdu: {ex}")

    # 2) sinyal tespiti FON_IZI ile birebir (SAPMA-1 sonrası)
    tohumlar = list(range(40)); V = {f"S{s:02d}": _seri(s) for s in tohumlar}
    tum = 0; s1 = 0; ornek_s1 = None
    for s, d in V.items():
        X0 = F.fi_k24_tara(d, F.FI_K24); X0 = X0[X0.kural] if len(X0) else X0
        X = KY.ky_tara(d)
        ti0 = d.index.get_indexer(pd.DatetimeIndex(X0.tarih)) if len(X0) else np.array([], int)
        bek = X0[ti0 >= 199] if len(X0) else X0
        tum += len(X); s1 += int((ti0 < 199).sum())
        if (ti0 < 199).any() and ornek_s1 is None:
            ornek_s1 = (s, pd.Timestamp(X0[ti0 < 199].tarih.iloc[0]))
        if len(bek) != len(X) or (len(X) and (not (pd.DatetimeIndex(bek.tarih) == pd.DatetimeIndex(X.tarih)).all()
                                              or not np.allclose(bek.dusus.to_numpy(float), X.dusus.to_numpy(float)))):
            hata.append(f"2 {s}: ky_tara FON_IZI kural satırlarıyla aynı değil")
        if len(X) and (X.dusus > F.FI_K24["dusus"]).any():
            hata.append(f"2 {s}: dusus eşiği aşılmış satır")
    if tum < 30:
        hata.append(f"2 sentetik sinyal az ({tum})")
    if s1 == 0 or ornek_s1 is None:
        hata.append("2 SAPMA-1 örneği yok (t < 199 sinyali beklenirdi)")

    # 3) geleceğe bakma
    bozuk = 0
    for s, d in V.items():
        X = KY.ky_tara(d)
        for r in X.itertuples():
            Y = KY.ky_tara(d.loc[:r.tarih]); Y = Y[Y.tarih == r.tarih]
            if len(Y) != 1 or not np.isclose(Y.dusus.iloc[0], r.dusus) or int(Y.L1.iloc[0]) != int(r.L1):
                bozuk += 1
            # kesik seriye ileri barlar eklense de (veri sonradan gelir) t'deki tespit değişmez: 3 bar ileri kesik
            k = d.index.get_loc(r.tarih)
            Y3 = KY.ky_tara(d.iloc[:k + 4]); Y3 = Y3[Y3.tarih == r.tarih]
            if len(Y3) != 1:
                bozuk += 1
    if bozuk:
        hata.append(f"3 geleceğe bakma: {bozuk} sinyal kesik seride farklı")
    s, t = ornek_s1
    tam = F.fi_k24_tara(V[s]); kesik = F.fi_k24_tara(V[s].loc[:t])
    if not ((tam.tarih == t) & tam.kural).any():
        hata.append("3 SAPMA-1 örneği tam seride yok")
    if len(kesik) and ((kesik.tarih == t) & kesik.kural).any():
        hata.append("3 SAPMA-1 örneği kesik seride de var (gerekçe çürük)")
    if (KY.ky_tara(V[s]).tarih == t).any():
        hata.append("3 ky_tara SAPMA-1 sinyalini almış")

    # 4) L1 kaba kuvvet
    farkli = 0; say = 0
    for s, d in list(V.items())[:15]:
        X = KY.ky_tara(d); c = d.Close.to_numpy(float)
        for r in X.itertuples():
            say += 1
            if _L1_kaba(c, int(r.t_i)) != int(r.L1):
                farkli += 1
    if farkli or not say:
        hata.append(f"4 L1 kaba kuvvetle farklı: {farkli} / {say}")

    # 5) kovalar
    S = pd.DataFrame({"pazar": "ABD", "sembol": list("abcdef"), "tarih": pd.Timestamp("2020-01-02"),
                      "dusus": [-0.30, -0.4999, -0.50, -0.70, -0.71, -0.95], "L1": [5, 10, 11, 20, 21, 99]})
    K = KY.ky_kova_ekle(S, (10.0, 20.0))
    if list(K.L1_kova) != ["kısa", "kısa", "orta", "orta", "uzun", "uzun"]:
        hata.append(f"5 L1 kova: {list(K.L1_kova)}")
    if list(K.derinlik_kova) != ["-%30..-%50", "-%30..-%50", "-%50..-%70", "<-%70", "<-%70", "<-%70"]:
        hata.append(f"5 derinlik kova: {list(K.derinlik_kova)}")

    # 6) cetvel çağrısı uçtan uca (sentetik pazar; 3 kat daha fazla hisse ile havuz >= 30)
    Vp = {f"P{s:02d}": _seri(s, T=900, bas="2021-01-01") for s in range(45)}
    Vd = OC._oc_veri_sar(Vp, "ABD")
    Sx = []
    for s, d in Vd["V"].items():
        X = KY.ky_tara(d)
        if len(X):
            Sx.append(X.assign(pazar="ABD", sembol=s))
    Sx = pd.concat(Sx, ignore_index=True)
    R = OC.oc_olc(Sx[["sembol", "tarih", "pazar"]], {"ABD": Vd})
    if not {"ort_fark", "alt95", "durum", "olas"} <= set(R["hucre"].columns) or len(R["hucre"]) != 3:
        hata.append("6 oc_olc hücre tablosu eksik")
    if R["sayim"]["ABD"]["girdi"] != len(Sx):
        hata.append("6 oc_olc sayımı girdi ile tutmuyor")
    if R["cetvel_sha"] != OC.oc_esik_sha():
        hata.append("6 cetvel sha farklı")
    Sk = KY.ky_kova_ekle(Sx, (Sx.L1.quantile(1 / 3), Sx.L1.quantile(2 / 3)))
    alt = KY._ky_alt_ozet(OC.oc_olc(Sk[Sk.L1_kova == "kısa"][["sembol", "tarih", "pazar"]], {"ABD": Vd}), "L1 tercil", "kısa")
    J = {"surum": KY.KY_SURUM, "kos_bas_utc": "x", "kos_son_utc": "y", "sure_sn": 0, "kapi": {}, "sayim_tarama": {"ABD": {"hisse": 45,
         "kural_tum": 1, "sapma1_dusen": 0, "sinyal": 1}}, "etiket": R["etiket"],
         "hucre": json_kayit(R["hucre"]), "olasilik": json_kayit(R["olasilik"]), "alt": alt, "gelecek_denetim": {"ABD": {"ornek": 1, "bozuk": []}},
         "tercil": [1.0, 2.0], "eski": KY.ky_eski_dogrula(), "oc_rapor": OC.oc_rapor(R, "test")}
    md = KY.ky_rapor_md(J)
    if "DÜZ DİL ÖZET" not in md or "Olasılık tablosu" not in md or "Ek bilgi tablosu: L1 tercil" not in md:
        hata.append("6 rapor bölümleri eksik")

    # 7) kapı (git=False; sentetik ön kayıt)
    with tempfile.TemporaryDirectory() as td:
        yol = os.path.join(td, "on.md")
        metin = "\n".join([OC.oc_kapi_satirlari(), f"KY_ESIK_SHA: `{KY.ky_esik_sha()}`", f"FI_K24_SHA: `{KY.ky_fi_k24_sha()}`",
                           f"FI_K24_KOD_SHA: `{KY.ky_fi_kod_sha()}`", f"KY_KOD_SHA: `{KY.ky_kod_sha()}`", f"OLAY_SHA: `{'0' * 64}`",
                           "TERCIL: `10.000000` `20.000000`", "", KY.ky_kontrol_tablosu()])
        open(yol, "w", encoding="utf-8").write(metin)
        try:
            k = KY.ky_kapi(yol, git=False)
            if k["TERCIL"] != (10.0, 20.0):
                hata.append("7 tercil okunamadı")
        except KY.KYHata as ex:
            hata.append(f"7 doğru ön kayıt geçmedi: {ex}")
        for eski, yeni in ((KY.ky_esik_sha(), "1" * 64), (KY.ky_fi_kod_sha(), "2" * 64), ("TERCIL:", "TERCI_:")):
            open(yol, "w", encoding="utf-8").write(metin.replace(eski, yeni, 1))
            try:
                KY.ky_kapi(yol, git=False); hata.append(f"7 bozuk ön kayıt geçti ({yeni[:6]})")
            except KY.KYHata:
                pass
        open(yol, "w", encoding="utf-8").write(metin.replace("| K3 |", "| K3x |"))
        try:
            KY.ky_kapi(yol, git=False); hata.append("7 eksik kontrol satırıyla geçti")
        except KY.KYHata:
            pass

    # 8) eski kayıt alıntıları
    if not all(e["metinde"] for e in KY.ky_eski_dogrula()):
        hata.append(f"8 eski alıntı IZ_KARNE metninde yok: {[e['kod'] for e in KY.ky_eski_dogrula() if not e['metinde']]}")

    # 9) olay sha sıradan bağımsız
    if KY.ky_olay_sha(Sx) != KY.ky_olay_sha(Sx.sample(frac=1, random_state=1)):
        hata.append("9 olay sha sıraya bağlı")

    # 10) e-posta / anahtar
    for ad in ("K24_YENIDEN.py", "test_k24_yeniden.py"):
        m = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.(com|org|net|io|tr)\b", m) or re.search(r"(api[_-]?key|token|sifre)\s*=\s*['\"][^'\"]{6,}", m, re.I):
            hata.append(f"10 {ad}: e-posta / anahtar deseni")
    return hata, {"sentetik_sinyal": tum, "sapma1": s1, "L1_kontrol": say}


def json_kayit(T: pd.DataFrame):
    import json
    return json.loads(T.to_json(orient="records", force_ascii=False))


if __name__ == "__main__":
    h, bilgi = testler()
    print(bilgi)
    if h:
        print("BAŞARISIZ:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_k24_yeniden: 10/10 GEÇTİ")
