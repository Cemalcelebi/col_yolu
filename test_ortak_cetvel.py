"""ORTAK_CETVEL testleri (yalnız SENTETİK veri; gerçek veride sinyal ölçmez). Çalıştırma: python test_ortak_cetvel.py

1) çakışma kapısı  2) tekilleştirme (60 işlem günü)  3) giriş = t'den sonraki ilk geçerli bar açılışı; geçersiz sinyal barı düşer
4) FON_IZI FI_OLCUT ile birebir: hücre etiketleri (H), r60, havuz; olay r60 / eşli / sıra; hücre istatistikleri (bootstrap + plasebo dahil);
   'gecmis' havuz kipi gelecek tam olan günlerde FI ile aynı  5) bootstrap deterministik  6) plasebo (δ=0 düşük, büyük δ yüksek güç; σ=%25 yedek)
7) olasılık tablosu (+%100 / -%50 dokunma, önce +%20, aynı gün iki eşik = aşağı; KAT elle)  8) etiket kuralları (İZ / İZ + BIST / EMARE /
   İZ DEĞİL / ÖLÇÜLEMEDİ / ABD-ADAY; SEÇİCİ / PİYANGO / YOK)  9) kapı (sha farkı / kod farkı / güç farkı / satır eksik / git'e işlenmemiş /
   boş kontrol tablosu -> durur; doğru ön kayıt geçer)  10) GELECEĞE BAKMA: seri d'de kesilince hücre etiketleri ve olay girişi aynı
   (fi kipi aynı değil)  11) bölünme şüphesi = SIKISMA_YENIDEN ANA  12) uçtan uca oc_olc + oc_rapor; olay satırlarından hücre yeniden üretimi
13) mühür kararlılığı  14) e-posta / anahtar yok.
"""
from __future__ import annotations

import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
warnings.filterwarnings("ignore", category=RuntimeWarning)
import ORTAK_CETVEL as OC  # noqa: E402

E = OC.OC_ESIK


def _evren(N=45, T=420, bas="2022-06-01", tohum=3):
    """Sentetik pazar: N hisse, T iş günü, farklı hacim düzeyleri ve oynaklıklar; bütün barlar geçerli."""
    rng = np.random.default_rng(tohum); idx = pd.bdate_range(bas, periods=T); V = {}
    for i in range(N):
        sig = 0.01 + 0.03 * rng.random()
        C = 20 * np.exp(np.cumsum(rng.normal(0.0003, sig, T)))
        O = np.r_[C[0], C[:-1]] * (1 + rng.normal(0, sig / 3, T))
        H = np.fmax(O, C) * (1 + np.abs(rng.normal(0.005, 0.003, T))); L = np.fmin(O, C) * (1 - np.abs(rng.normal(0.005, 0.003, T)))
        Vol = rng.integers(1e4, 1e5, T).astype(float) * (1 + 20 * (i % 5))
        V[f"S{i:02d}"] = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": Vol}, index=idx)
    return V


def _E_fi():
    Ef = copy.deepcopy(E); Ef["likidite"]["alt_kesik"] = 0.0; Ef["bolunme"]["aktif"] = False
    return Ef


def testler():
    hata = []
    import FON_IZI as F

    # 1) çakışma kapısı
    kod = open(os.path.join(KOK, "ORTAK_CETVEL.py"), encoding="utf-8").read()
    g = {"__name__": "colab_benzeri", "oc_panel": "baska_dosyanin_adi"}
    try:
        exec(compile(kod, "ORTAK_CETVEL.py", "exec"), g)
        hata.append("1) çakışma kapısı bellekteki adı ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) çakışma kapısı yanlış hata: {ex}")
    g2 = {"__name__": "colab_benzeri"}
    try:
        exec(compile(kod, "ORTAK_CETVEL.py", "exec"), g2); exec(compile(kod, "ORTAK_CETVEL.py", "exec"), g2)   # aynı dosya iki kez: serbest
    except RuntimeError as ex:
        hata.append(f"1) aynı dosyanın yeniden yüklenmesi durdu: {ex}")

    V = _evren(); Vd = OC._oc_veri_sar(V, "ABD"); P = OC.oc_panel(Vd, E)
    idx = P["tarih"]

    # 2) tekilleştirme
    s0 = "S07"; t = [idx[100], idx[110], idx[160], idx[171]]
    X, say = OC.oc_olay_hazirla(pd.DataFrame({"sembol": s0, "tarih": t, "pazar": "ABD"}), P, E)
    beklenen = [idx[101], idx[161]]   # 101 tutulur; 111 (< 60) düşer; 161 - 101 = 60 -> tutulur; 172 (< 60) düşer
    if list(X.giris) != beklenen or say["tekil"] != 2:
        hata.append(f"2) tekilleştirme: {list(X.giris)} tekil {say['tekil']} (beklenen {beklenen}, 2)")

    # 3) giriş ertesi açılış; eksik gün -> sonraki geçerli bar; geçersiz sinyal barı düşer
    V3 = copy.deepcopy(V); s = "S03"
    V3[s] = V3[s].drop(index=idx[121])                               # 121. gün bar yok -> giriş 122
    V3[s].loc[idx[130], "Volume"] = 0.0                              # sinyal günü geçersiz
    P3 = OC.oc_panel(OC._oc_veri_sar(V3, "ABD"), E)
    X3, say3 = OC.oc_olay_hazirla(pd.DataFrame({"sembol": [s, s, s], "tarih": [idx[100], idx[120], idx[130]], "pazar": "ABD"}), P3, E)
    X3 = OC.oc_esli(P3, X3, E)
    r = X3[X3.tarih == idx[100]]
    if not len(r) or r.giris.iat[0] != idx[101] or abs(r.giris_fiyat.iat[0] - V[s].Open.iat[101]) > 1e-12:
        hata.append("3) giriş t'den sonraki ilk açılış değil")
    # 120'deki olay 100'ün 60 gün içinde: önce ayrı denetle
    X3b, _ = OC.oc_olay_hazirla(pd.DataFrame({"sembol": [s], "tarih": [idx[120]], "pazar": "ABD"}), P3, E)
    if not len(X3b) or X3b.giris.iat[0] != idx[122]:
        hata.append(f"3) eksik günde giriş sonraki geçerli bar değil: {list(X3b.giris)}")
    if say3["sinyal_bar_gecersiz"] != 1:
        hata.append(f"3) geçersiz sinyal barı düşmedi: {say3}")
    r60_el = V[s].Close.iat[101 + 59] / V[s].Open.iat[101] - 1
    if not len(r) or abs(r.r60.iat[0] - r60_el) > 1e-12:
        hata.append("3) r60 = 60. gün kapanışı / giriş açılışı - 1 değil")

    # 4) FON_IZI FI_OLCUT ile birebir
    Ef = _E_fi()
    Pfi = F.fi_olcut_panel(V); Poc = OC.oc_panel(OC._oc_veri_sar(V, "ABD"), Ef, kip="fi")
    if not (np.array_equal(Pfi["H"], Poc["H"]) and np.array_equal(Pfi["ok"], Poc["ok"]) and np.allclose(Pfi["R"], Poc["R"], equal_nan=True)):
        hata.append(f"4) fi kipi hücre etiketleri FON_IZI ile aynı değil (fark {int((Pfi['H'] != Poc['H']).sum())})")
    Pg = OC.oc_panel(OC._oc_veri_sar(V, "ABD"), Ef, kip="gecmis")
    tam = np.where(np.isfinite(Pfi["R"]).all(1))[0]
    if not len(tam) or not np.array_equal(Pfi["H"][tam], Pg["H"][tam]):
        hata.append("4) 'gecmis' havuz kipi gelecek tam olan günlerde FON_IZI ile aynı değil")
    rng = np.random.default_rng(5); ss = sorted(V); ol = []
    for k in range(70):
        ol.append((ss[rng.integers(len(ss))], idx[rng.integers(70, 330)]))
    olay = pd.DataFrame(ol, columns=["sembol", "giris"])
    Xfi = F.fi_olcut_olay(Pfi, olay)
    Xoc = OC.oc_esli(Poc, pd.DataFrame({"sembol": olay.sembol, "giris": olay.giris, "d": [Poc["tarih"].get_loc(x) for x in olay.giris],
                                        "j": [Poc["kol"][x] for x in olay.sembol]}), Ef)
    for c in ("r60", "esli_r60", "sira", "fark"):
        if not np.allclose(Xfi[c].to_numpy(float), Xoc[c].to_numpy(float), equal_nan=True, rtol=0, atol=1e-14):
            hata.append(f"4) olay {c} FON_IZI ile aynı değil")
    hf = F.fi_olcut_hucre(Xfi); ho = OC.oc_hucre(Xoc, Ef)
    for k, v in hf.items():
        if not (abs(v - ho[k]) <= 1e-12 or (v != v and ho[k] != ho[k])):
            hata.append(f"4) hücre '{k}' FON_IZI ile aynı değil ({v} / {ho[k]})")
    if F.FI_OLCUT["ufuk"] != E["olcu"]["ufuk"] or F.FI_OLCUT["bootstrap"] != E["olcu"]["bootstrap"] or F.FI_OLCUT["tohum"] != E["olcu"]["tohum"] \
            or F.FI_OLCUT["port_n"] != E["olcu"]["port_n"] or F.FI_OLCUT["slot"] != E["olcu"]["slot"] or F.FI_OLCUT["n_esik"] != E["hucre_karar"]["n_esik"] \
            or F.FI_OLCUT["mom_kova"] != E["esli"]["mom_kova"] or F.FI_OLCUT["likit_kova"] != E["esli"]["likit_kova"] or F.FI_OLCUT["kriz"] != E["kriz"]:
        hata.append("4) OC_ESIK sayıları FI_OLCUT ile aynı değil")

    # 5) bootstrap deterministik
    h1 = OC.oc_hucre(Xoc, Ef); h2 = OC.oc_hucre(Xoc, Ef)
    if any(h1[k] != h2[k] for k in h1 if not k.startswith("_") and h1[k] == h1[k]):
        hata.append("5) oc_hucre deterministik değil")
    k1 = OC.oc_kat(np.array([1., 0, 1, 0, 1]), np.full(5, 0.5), np.array(list("aabbc")), E)
    k2 = OC.oc_kat(np.array([1., 0, 1, 0, 1]), np.full(5, 0.5), np.array(list("aabbc")), E)
    if k1 != k2 or abs(k1["kat"] - 3 / 2.5) > 1e-12:
        hata.append(f"5) oc_kat deterministik / elle değil: {k1}")

    # 6) plasebo / güç
    Eg = copy.deepcopy(E); Eg["guc"]["bas"] = "2022-09-01"; Eg["guc"]["son"] = "2023-12-31"
    Pb = OC.oc_panel(OC._oc_veri_sar(_evren(N=60, T=520, tohum=11), "ABD"), Eg)
    G = OC.oc_guc(60, [0.0, 0.40], Pb, None, Eg, tekrar=30)
    g0 = G[G.delta == 0].tutar.mean(); g1 = G[G.delta == 0.40].tutar.mean()
    if not (g0 <= 0.2 and g1 >= 0.8):
        hata.append(f"6) plasebo / güç beklenen gibi değil: δ0 {g0:.2f}, δ40 {g1:.2f}")
    Gs = OC.oc_guc(300, [0.0, 0.10], None, None, E, tekrar=20)
    if not (Gs[Gs.delta == 0].tutar.mean() <= 0.2 and (Gs.kaynak == "sigma25").all()):
        hata.append("6) σ=%25 yedek güç δ0 yüksek ya da kaynak etiketi yanlış")
    Z = OC.oc_guc_ozet(pd.concat([G, Gs]))
    if not {"guc", "guc4", "yari_genislik"} <= set(Z.columns):
        hata.append("6) güç özeti sütunları eksik")

    # 7) olasılık tablosu (elle kurulmuş hisseler)
    T7 = 600; V7 = _evren(N=40, T=T7, tohum=21); i7 = V7["S00"].index
    def yol(kat_son, ad, gun=150, sert=None):
        d = V7[ad].copy(); C = d.Close.to_numpy().copy(); O = d.Open.to_numpy().copy()
        x = np.linspace(0, np.log(kat_son), 200)
        C[gun + 1:gun + 201] = O[gun + 1] * np.exp(x); C[gun + 201:] = C[gun + 200]
        O[gun + 2:] = C[gun + 1:-1]
        Hh = np.fmax(O, C) * 1.001; Ll = np.fmin(O, C) * 0.999
        d["Open"], d["High"], d["Low"], d["Close"] = O, Hh, Ll, C
        if sert is not None:
            j, hi, lo = sert; e0 = O[gun + 1]
            d.iloc[j, d.columns.get_loc("High")] = e0 * hi; d.iloc[j, d.columns.get_loc("Low")] = e0 * lo
        V7[ad] = d
    yol(2.5, "S01"); yol(0.3, "S02"); yol(1.0, "S04", sert=(155, 1.25, 0.85))
    P7 = OC.oc_panel(OC._oc_veri_sar(V7, "ABD"), E)
    X7, _ = OC.oc_olay_hazirla(pd.DataFrame({"sembol": ["S01", "S02", "S04"], "tarih": [i7[150]] * 3, "pazar": "ABD"}), P7, E)
    X7 = OC.oc_olasilik_olay(P7, OC.oc_esli(P7, X7, E), E).set_index("sembol")
    if len(X7) != 3:
        hata.append(f"7) olasılık olayları havuza girmedi: {list(X7.index)}")
    else:
        if X7.at["S01", "up100"] != 1 or X7.at["S01", "dn50"] != 0 or X7.at["S02", "dn50"] != 1 or X7.at["S02", "up100"] != 0:
            hata.append("7) +%100 / -%50 dokunma yanlış")
        if X7.at["S01", "once20"] != 1 or X7.at["S02", "once20"] != 0:
            hata.append("7) 60 gün önce +%20 yanlış")
        if not (X7.at["S04", "u20"] == 0 and X7.at["S04", "d20"] == 1):
            hata.append("7) aynı gün iki eşik aşağı önce sayılmadı")
        d = int(X7.at["S01", "d"]); j = int(X7.at["S01", "j"])
        FH = OC._oc_ileri_maks(P7["Hi"], 250, "max"); m = OC._oc_olculebilir(P7, d, 250)
        es = OC._oc_es_maske(P7, d, j, m); el = float((FH[d, es] >= 2 * P7["Op"][d, es]).mean())
        if abs(el - X7.at["S01", "es_up100"]) > 1e-12:
            hata.append("7) eş +%100 oranı elle hesapla aynı değil")
    Xs = OC.oc_olasilik_olay(P7, OC.oc_esli(P7, OC.oc_olay_hazirla(pd.DataFrame({"sembol": ["S05"], "tarih": [i7[T7 - 100]], "pazar": "ABD"}), P7, E)[0], E), E)
    if len(Xs) and np.isfinite(Xs.up100.iat[0]):
        hata.append("7) 250 gün penceresi verinin sonunu aşan olay ölçüldü")

    # 8) etiket kuralları
    def T(d):
        return pd.DataFrame([{"pazar": p, "donem": dn, "durum": v, "olas": o} for (p, dn), (v, o) in d.items()])
    K = [("ABD", "2023"), ("ABD", "2024-26"), ("AVR", "2023"), ("AVR", "2024-26")]
    tt = {k: ("TUTAR", "SEÇİCİ") for k in K}
    if OC.oc_etiket(T(tt))["genel"] != "İZ" or OC.oc_etiket(T(tt))["olasilik"] != "SEÇİCİ":
        hata.append("8) dört TUTAR İZ / dört SEÇİCİ değil")
    tb = {**tt, ("BIST", "2023"): ("TUTAR", "YOK"), ("BIST", "2024-26"): ("TUTAR", "YOK")}
    if OC.oc_etiket(T(tb))["genel"] != "İZ + BIST":
        hata.append("8) İZ + BIST değil")
    te = {k: ("TUTMADI", "PİYANGO") for k in K}; te[("ABD", "2023")] = ("TUTAR", "PİYANGO")
    if not OC.oc_etiket(T(te))["genel"].startswith("EMARE") or OC.oc_etiket(T(te))["olasilik"] != "PİYANGO":
        hata.append("8) tek hücre EMARE / dört PİYANGO değil")
    td = {k: ("TUTMADI", "YOK") for k in K}
    if OC.oc_etiket(T(td))["genel"] != "İZ DEĞİL" or OC.oc_etiket(T(td))["olasilik"] != "YOK":
        hata.append("8) dört TUTMADI İZ DEĞİL değil")
    to = {**td, ("AVR", "2023"): ("ÖLÇÜLEMEDİ", "ÖLÇÜLEMEDİ")}
    if OC.oc_etiket(T(to))["genel"] != "ÖLÇÜLEMEDİ" or OC.oc_etiket(T(to))["olasilik"] != "ÖLÇÜLEMEDİ":
        hata.append("8) güçsüz hücreli ÖLÇÜLEMEDİ değil")
    ta = {("ABD", "2023"): ("TUTAR", "YOK"), ("ABD", "2024-26"): ("TUTAR", "YOK")}
    if "ABD-ADAY" not in OC.oc_etiket(T(ta))["genel"]:
        hata.append(f"8) AVR verisi yokken ABD-ADAY değil: {OC.oc_etiket(T(ta))['genel']}")
    tab = {"30": {"0.05": 0.1}, "300": {"0.05": 0.5}, "1000": {"0.05": 0.95}}
    if OC.oc_hucre_durum({"n": 20, "tutar": True}, E, tab)[0] != "ÖLÇÜLEMEDİ" or OC.oc_hucre_durum({"n": 1500, "tutar": False}, E, tab)[0] != "TUTMADI" \
            or OC.oc_hucre_durum({"n": 400, "tutar": False}, E, tab)[0] != "ÖLÇÜLEMEDİ" or OC.oc_hucre_durum({"n": 400, "tutar": True}, E, tab)[0] != "TUTAR" \
            or OC.oc_hucre_durum({"n": 400, "tutar": False}, E, {"300": {"0.05": 0.85}})[0] != "TUTMADI" \
            or abs(OC.oc_guc_bak(999, None, tab, E) - 0.5) > 1e-12:
        hata.append("8) hücre durum / güç bakma kuralı yanlış")
    def ol(n, ua, da, du):
        return OC.oc_olasilik_etiket({"n250": n, "up100_es_alt": ua, "dn50_es_alt": da, "dn50_es_ust": du}, E)
    if ol(100, 1.2, 0.5, 0.9) != "SEÇİCİ" or ol(100, 1.2, 1.1, 1.5) != "PİYANGO" or ol(100, 0.9, 0.5, 0.9) != "YOK" or ol(10, 2, 0.1, 0.2) != "ÖLÇÜLEMEDİ":
        hata.append("8) olasılık etiketi yanlış")

    # 9) kapı
    tmp = tempfile.mkdtemp(prefix="oc_kapi_")
    try:
        gj = os.path.join(tmp, "guc_tablosu.json"); json.dump({"tablo_guc5": tab}, open(gj, "w"))
        ok_ = os.path.join(tmp, "ON.md")
        def yaz(cetvel=None, kod_=None, guc=None, tablo=True, eksik=False):
            sat = [f"CETVEL_SHA: `{cetvel or OC.oc_esik_sha()}`", f"CETVEL_KOD_SHA: `{kod_ or OC.oc_kod_sha()}`"]
            if not eksik:
                sat.append(f"GUC_SHA: `{guc or OC._oc_sha_dosya(gj)}`")
            sat.append(OC.oc_kontrol_tablosu() if tablo else "| K1 | x | | |")
            open(ok_, "w", encoding="utf-8").write("\n".join(sat) + "\n")
        git = lambda *a: subprocess.run(["git", "-C", tmp, *a], capture_output=True, text=True)  # noqa: E731
        git("init", "-q"); git("config", "user.email", "t@t.invalid"); git("config", "user.name", "t")
        yaz(); git("add", "."); git("commit", "-qm", "on kayit")
        try:
            OC.oc_kapi(ok_, guc_yol=gj, kod_git=False)
        except OC.OCHata as ex:
            hata.append(f"9) doğru ön kayıt kapıdan geçmedi: {ex}")
        E2 = copy.deepcopy(E); E2["hucre_karar"]["n_esik"] = 20
        for ad, fn in (("cetvel farkı", lambda: OC.oc_kapi(ok_, guc_yol=gj, kod_git=False, E=E2)),):
            try:
                fn(); hata.append(f"9) {ad}: kapı durmadı")
            except OC.OCHata:
                pass
        for ad, kw in (("kod sha farkı", {"kod_": "0" * 64}), ("güç sha farkı", {"guc": "1" * 64}), ("GUC_SHA satırı eksik", {"eksik": True}),
                       ("boş kontrol tablosu", {"tablo": False})):
            yaz(**kw); git("add", "."); git("commit", "-qm", ad)
            try:
                OC.oc_kapi(ok_, guc_yol=gj, kod_git=False); hata.append(f"9) {ad}: kapı durmadı")
            except OC.OCHata:
                pass
        yaz(); git("add", "."); git("commit", "-qm", "dogru")
        open(ok_, "a", encoding="utf-8").write("\nsonradan eklendi\n")
        try:
            OC.oc_kapi(ok_, guc_yol=gj, kod_git=False); hata.append("9) git'e işlenmemiş değişiklik: kapı durmadı")
        except OC.OCHata:
            pass
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 10) geleceğe bakma: seri d'de kesilince aynı hücre etiketi ve aynı giriş
    for d in (90, 150, 260, 380):
        Vk = {s_: x[x.index <= idx[d]] for s_, x in V.items()}
        Pk = OC.oc_panel(OC._oc_veri_sar(Vk, "ABD"), E)
        if not np.array_equal(Pk["H"][d], P["H"][d]) or not np.array_equal(Pk["ok"][d], P["ok"][d]):
            hata.append(f"10) gecmis kipte gün {d}: kesilmiş seriyle hücre etiketleri farklı (geleceğe bakma)")
        Xk, _ = OC.oc_olay_hazirla(pd.DataFrame({"sembol": ["S10"], "tarih": [idx[d - 1]], "pazar": "ABD"}), Pk, E)
        Xt, _ = OC.oc_olay_hazirla(pd.DataFrame({"sembol": ["S10"], "tarih": [idx[d - 1]], "pazar": "ABD"}), P, E)
        if list(Xk.giris) != list(Xt.giris) or list(Xk.hucre) != list(Xt.hucre):
            hata.append(f"10) gün {d}: kesilmiş seriyle olay girişi / hücresi farklı")
    Vk = {s_: x[x.index <= idx[200]] for s_, x in V.items()}
    Pkf = OC.oc_panel(OC._oc_veri_sar(Vk, "ABD"), Ef, kip="fi"); Pff = OC.oc_panel(OC._oc_veri_sar(V, "ABD"), Ef, kip="fi")
    if np.array_equal(Pkf["H"][200], Pff["H"][200]):
        hata.append("10) fi kipi kesilince değişmedi (beklenen: FON_IZI havuzu ileri r60'a bağlı)")

    # 11) bölünme şüphesi = SIKISMA_YENIDEN ANA
    import SIKISMA_YENIDEN as SY
    rng = np.random.default_rng(8)
    for k in range(6):
        C = 50 * np.exp(np.cumsum(rng.normal(0, 0.02, 300)))
        if k % 2 == 0:
            C[150:] /= 2.0
        if k == 3:
            C[100] *= 1.4   # geri dönen sıçrama
        a = OC.oc_bolunme_supheli(C, E); b = SY.sy_bolunme_supheli(C, SY.SY_ESIK)
        if not np.array_equal(a, b):
            hata.append(f"11) bölünme şüphesi SIKISMA_YENIDEN ile farklı (seri {k})")
        if k % 2 == 0 and not a[150]:
            hata.append("11) 2:1 bölünme yakalanmadı")
    V11 = copy.deepcopy(V); x = V11["S24"]; x.loc[x.index >= idx[200], ["Open", "High", "Low", "Close"]] /= 3.0
    c199 = x.Close.iat[199]; x.iloc[200, x.columns.get_indexer(["Open", "Close"])] = c199 / 3.0       # tam 1:3 (oran toleransı içinde)
    x.iloc[200, x.columns.get_loc("High")] = c199 / 3.0 * 1.002; x.iloc[200, x.columns.get_loc("Low")] = c199 / 3.0 * 0.998
    P11 = OC.oc_panel(OC._oc_veri_sar(V11, "ABD"), E); j = P11["kol"]["S24"]
    if P11["ok"][230, j] or not P11["ok"][170, j] or not P11["okR"][170, j] or not P11["sup"][200, j]:
        hata.append("11) bölünme şüphesi geçmiş pencerede havuzdan çıkarılmadı ya da ileri pencerede dışlandı")
    X11, s11 = OC.oc_olay_hazirla(pd.DataFrame({"sembol": ["S24"], "tarih": [idx[229]], "pazar": "ABD"}), P11, E)
    if len(X11) or s11["bolunme_gecmis"] != 1:
        hata.append(f"11) geçmiş bölünme olayı sayımda ayrı düşmedi: {s11}")

    # 12) uçtan uca
    VA = _evren(N=50, T=700, bas="2022-01-03", tohum=31); VB = _evren(N=50, T=700, bas="2022-01-03", tohum=32)
    rng = np.random.default_rng(12); ol = []
    for pz, VV in (("ABD", VA), ("AVR", VB)):
        ix = VV["S00"].index; ss = sorted(VV)
        for k in range(160):
            ol.append((ss[rng.integers(len(ss))], ix[rng.integers(80, 640)], pz))
    Sx = OC.oc_olc(pd.DataFrame(ol, columns=["sembol", "tarih", "pazar"]), {"ABD": OC._oc_veri_sar(VA, "ABD"), "AVR": OC._oc_veri_sar(VB, "AVR")}, E, tablo=tab)
    md = OC.oc_rapor(Sx, "sentetik")
    if "GENEL ETİKET" not in md or "Olasılık tablosu" not in md or not len(Sx["hucre"]) or "_esler" in Sx["olay"].columns:
        hata.append("12) oc_olc / oc_rapor çıktısı eksik")
    h = Sx["hucre"]; h = h[(h.pazar == "ABD") & (h.donem == "2023")]
    o = Sx["olay"]; o = o[(o.pazar == "ABD") & (o.donem == "2023")].dropna(subset=["fark"])
    if not len(h) or int(h.n.iat[0]) != len(o) or abs(float(h.ort_fark.iat[0]) - (o.r60 - o.esli_r60).mean()) > 1e-12:
        hata.append("12) hücre ortalama eşli fark olay satırlarından yeniden üretilemedi")
    ob = Sx["olasilik"]; ob = ob[(ob.pazar == "ABD") & (ob.donem == "2023")]
    oo = o.dropna(subset=["up100", "es_up100"])
    if len(oo) and oo.es_up100.sum() > 0 and abs(float(ob.up100_es_kat.iat[0]) - oo.up100.sum() / oo.es_up100.sum()) > 1e-12:
        hata.append("12) +%100 eş katı olay satırlarından yeniden üretilemedi")
    if Sx["etiket"]["genel"].startswith("İZ ") or Sx["etiket"]["genel"] == "İZ":
        hata.append(f"12) rastgele olayda İZ çıktı: {Sx['etiket']}")

    # 13) mühür kararlılığı
    if OC.oc_esik_sha() != OC.oc_esik_sha(copy.deepcopy(E)) or OC.oc_esik_sha(E2) == OC.oc_esik_sha():
        hata.append("13) mühür kararsız ya da eşik değişikliğini görmüyor")

    # 14) e-posta / anahtar yok
    for ad in ("ORTAK_CETVEL.py", "test_ortak_cetvel.py"):
        s_ = open(os.path.join(KOK, ad), encoding="utf-8").read()
        s_ = s_.replace("t@t.invalid", "")
        if OC._OC_EPOSTA.findall(s_) or re.search(r"(api[_-]?key|token|secret|password)\s*=\s*['\"][A-Za-z0-9]{12,}", s_, re.I):
            hata.append(f"14) {ad} içinde e-posta / anahtar var")
    return hata


if __name__ == "__main__":
    Hh = testler()
    if Hh:
        print("ORTAK_CETVEL TEST: HATA", len(Hh)); print("\n".join(Hh)); sys.exit(1)
    print("ORTAK_CETVEL TEST: 14/14 bölüm GEÇTİ")
