"""K60-B testleri (ağ gerekmez; yalnız SENTETİK veri). Çalıştırma: python test_k60b.py

1) çakışma kapısı (_CK_ONCE_K60B)  2) ön kayıt: koddaki sabitler K60B_ON_KAYIT.md ile aynı; dosya sha256'sı değişmişse / git'e işlenmemişse /
işlendikten sonra değişmişse ret  3) havuz kuralı (uygun evrenin oynaklığı en yüksek %20'si, elle; küçük havuzlu ay atlanır)  4) GELECEĞE
BAKMA YOK (t'den sonrası bozulunca t ve öncesi havuz, havuz içi sinyaller, bileşikler ve uçlar aynı)  5) havuz içi sıralar (bileşik ve
MOM_FIP havuz içinde yeniden), uçlar (ÜST / ALT %20, bayrak, ay ay atlama)  6) kat / ASIM / aralık elle (düz döngü + aylık sayımlardan)
7) aylık portföy (kıyas = havuz)  8) plasebo tohumu  9) seçim, geçiş, etiket, YAKIN kuralları (elle tablolar)  10) uçtan uca sentetik koşu +
rapor + çıktılardan yeniden üretim  11) e-posta / anahtar yok.
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

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K60B as KB  # noqa: E402
import test_k60 as TK  # noqa: E402

K60, K58, K59 = KB.K60, KB.K58, KB.K59


def test_b(**ek) -> dict:
    """Sentetik koşular için küçültülmüş K60-B eşikleri."""
    B = copy.deepcopy(KB.K60B_ESIK)
    B["havuz"]["min_hisse"] = 30; B["uc"].update({"min_sinyal": 20, "min_bayrak": 2}); B["olcu"]["min_hisse_ay"] = 30
    B["plasebo"].update({"n": 30, "maks_tekrar": 300})
    for k, v in ek.items():
        B[k].update(v)
    return B


def durmali(f, ad: str, hata: list) -> None:
    try:
        f(); hata.append(ad)
    except KB.K60BHata:
        pass


def testler() -> list:
    hata = []; B0 = KB.K60B_ESIK; nan = np.nan
    # 1) çakışma kapısı
    src = open(os.path.join(KOK, "K60B.py"), encoding="utf-8").read().replace("from __future__ import annotations\n", "")
    g = {"__name__": "kapi_test", "k60b_kos": object(), "_CK_KAYIT": {"k60b_kos": "BASKA.py"}}
    try:
        exec(compile(src, "K60B.py", "exec"), g); hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "kapi_test2"}
    try:
        exec(compile(src, "K60B.py", "exec"), g2); exec(compile(src, "K60B.py", "exec"), g2)
    except Exception as ex:
        hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
    if "_CK_ONCE_K60B = " not in src or "_cakisma_kontrol_k60b()" not in src:
        hata.append("1) çakışma kapısı adı _CK_ONCE_K60B değil")
    # 2) ön kayıt sabitleri ve doğrulama
    if not (B0["havuz"] == {"sinyal": "VOL_60D", "pay": 0.20, "min_hisse": 150} and B0["uc"] == {"pay": 0.20, "min_sinyal": 100, "min_bayrak": 10} and B0["olcu"]["ana_ufuk"] == 12
            and B0["olcu"]["bilgi_ufuk"] == [6] and B0["olcu"]["min_ay"] == 12 and B0["olcu"]["min_hisse_ay"] == 200 and B0["olcu"]["p100"] == 1.0 and B0["olcu"]["m50"] == -0.5
            and B0["portfoy"] == {"maliyet": 0.001, "nw_lag": 6, "min_ay": 12} and B0["plasebo"]["n"] == 200 and B0["plasebo"]["tohum"] == 60200 and B0["plasebo"]["maks_tekrar"] == 2000
            and B0["plasebo"]["maks_tohum"] == 60203 and B0["plasebo"]["maks_yuzde"] == 95.0 and B0["plasebo"]["donem_yuzde"] == 95.0 and B0["plasebo"]["yp_esik"] == 0.05
            and B0["secim"] == {"kat_p100_min": 0.90, "bh_q": 0.10} and len(B0["baslik"]) == 25 and K60.K60_ESIK["r2"]["blok"] == 12 and K60.K60_ESIK["r2"]["cekilis"] == 500
            and K60.K60_ESIK["r2"]["tohum"] == 60002 and K60.K60_ESIK["donem"]["kesif"] == ["2012-01", "2021-12"]):
        hata.append("2) K60B_ESIK sabitleri ön kayıttaki gibi değil")
    gercek = KB.K60B_YOL["onkayit"]
    if not os.path.exists(gercek) or K60._k60_sha(gercek) != KB.K60B_ONKAYIT_SHA:
        hata.append("2) K60B_ON_KAYIT.md yok ya da sha256'sı koddaki sabitle aynı değil")
    else:
        metin = open(gercek, encoding="utf-8").read()
        for parca in ("en yüksek %20", "Havuz < 150", "ÜST ve ALT\n%20", "< 100 olan ay", "ayda en az 10", "en az 12 oluşum ayı", "200 hisse-ay", "60200", "60203", "2000 tekrar", ">= 0,90",
                      "tek yön 10 bp", "NW(6)", "K60B-KOŞULLU FIRSAT", "K60B-KOŞULLU KORUMA"):
            if parca not in metin:
                hata.append(f"2) ön kayıtta beklenen ifade yok (kod sabiti dayanaksız kalır): {parca!r}")
        try:
            d = KB.k60b_onkayit_dogrula()
            if d["dosya_sha256"] != KB.K60B_ONKAYIT_SHA or not d["git"]["commit"]:
                hata.append("2) gerçek ön kayıt doğrulaması sha256 / git commit döndürmedi")
        except KB.K60BHata as ex:
            hata.append(f"2) gerçek ön kayıt doğrulanamadı: {ex}")
        with tempfile.TemporaryDirectory() as td:
            y = os.path.join(td, "K60B_ON_KAYIT.md"); shutil.copy(gercek, y)
            durmali(lambda: KB.k60b_onkayit_dogrula(y), "2) git'e işlenmemiş ön kayıt kabul edildi", hata)
            if KB.k60b_onkayit_dogrula(y, git=False)["dosya_sha256"] != KB.K60B_ONKAYIT_SHA:
                hata.append("2) git'siz doğrulama sha256 döndürmedi")
            TK.git(td, "init", "-q"); TK.git(td, "add", "K60B_ON_KAYIT.md"); TK.git(td, "commit", "-q", "-m", "x")
            try:
                KB.k60b_onkayit_dogrula(y)
            except KB.K60BHata as ex:
                hata.append(f"2) git'e işlenmiş, değişmemiş ön kayıt reddedildi: {ex}")
            open(y, "a", encoding="utf-8").write("\n")
            durmali(lambda: KB.k60b_onkayit_dogrula(y), "2) içeriği değişmiş ön kayıt kabul edildi", hata)
            durmali(lambda: KB.k60b_onkayit_dogrula(y, beklenen=K60._k60_sha(y)), "2) git'e işlendikten sonra değişmiş ön kayıt kabul edildi", hata)
            durmali(lambda: KB.k60b_onkayit_dogrula(os.path.join(td, "yok.md")), "2) olmayan ön kayıt kabul edildi", hata)
            durmali(lambda: KB.k60b_kos(td, demet={}, onkayit_yol=y), "2) değişmiş ön kayıtla koşu durmadı", hata)
    # ortak sentetik veri
    D = TK.sentetik_demet(N=300, etki=0.0008); Et = TK.test_esik(); Bt = test_b(); X = KB.k60b_hazirla(D, Et, Bt); P, H, Sh, Sd, bag = X["P"], X["H"], X["Sh"], X["Sd"], X["bag"]
    U = P["U"]; me = P["ay_sonu"]; M, N = U.shape; tn = K60.k60_tanim(); k = int(np.flatnonzero(np.asarray(me == pd.Timestamp("2018-06-29")))[0])
    # 3) havuz kuralı
    vol = Sd["VOL_60D"]; uy = np.flatnonzero(U[k] & np.isfinite(vol[k])); mm = max(1, int(round(0.2 * len(uy)))); bek = set(uy[np.argsort(vol[k][uy])][-mm:])
    if set(np.flatnonzero(H[k])) != bek or (H & ~U).any() or H[k].sum() != mm or np.nanmin(vol[k][H[k]]) < np.nanmax(vol[k][U[k] & ~H[k]]):
        hata.append("3) havuz = uygun evrenin oynaklığı en yüksek %20'si değil")
    Hb = KB.k60b_havuz(P, vol, bag, test_b(havuz={"min_hisse": 10 ** 6}))
    if Hb.any() or not H.any() or (H.sum(axis=1)[H.any(axis=1)] < Bt["havuz"]["min_hisse"]).any():
        hata.append("3) havuzu alt sınırdan küçük ay atlanmadı")
    # 4) geleceğe bakma yok
    Db = TK.boz(D, me[k]); Xb = KB.k60b_hazirla(Db, Et, Bt)
    if not np.array_equal(H[:k + 1], Xb["H"][:k + 1]) or np.array_equal(H[k + 2:], Xb["H"][k + 2:]):
        hata.append("4) GELECEĞE BAKMA: havuz t ve öncesinde değişti / bozma havuzu hiç değiştirmedi")
    for kod in Sh:
        if not TK.esit(Sh[kod][:k + 1], Xb["Sh"][kod][:k + 1]):
            hata.append(f"4) GELECEĞE BAKMA: havuz içi {kod} t ve öncesinde değişti")
        if np.isfinite(Sh[kod][~H]).any():
            hata.append(f"4) {kod}: havuz dışında değer var")
    for kod in ("BM", "AILE_PRF", "E_S3", "MOM_FIP"):
        u1 = KB.k60b_uclar(Sh[kod], "+", tn.get(kod, {"tur": "surekli"})["tur"], H, bag, Bt); u2 = KB.k60b_uclar(Xb["Sh"][kod], "+", tn.get(kod, {"tur": "surekli"})["tur"], Xb["H"], Xb["bag"], Bt)
        if any(not np.array_equal(u1[t]["sec"][:k + 1], u2[t]["sec"][:k + 1]) for t in u1):
            hata.append(f"4) GELECEĞE BAKMA: {kod} uçları t ve öncesinde değişti")
    # 5) havuz içi sıralar ve uçlar
    sira = lambda x: (pd.Series(np.where(H[k] & np.isfinite(x), x, nan)).rank() - 0.5) / (H[k] & np.isfinite(x)).sum()  # noqa: E731
    j = int(np.flatnonzero(H[k] & np.isfinite(Sh["AILE_VAL"][k]))[0]); uye = K60.K60_ESIK["bilesik"]["AILE_VAL"]["uye"]
    sr = np.array([sira((-1.0 if tn[u]["yon"] == "-" else 1.0) * Sd[u][k])[j] for u in uye])
    if abs(Sh["AILE_VAL"][k, j] - np.nanmean(sr)) > 1e-12 or abs(Sh["AILE_VAL"][k, j] - Sd["AILE_VAL"][k, j]) < 1e-9:
        hata.append("5) bileşik havuz içi yüzdelik sıralarla yeniden hesaplanmadı")
    sur = K60._k60_sinyal_fiyat(D, P, Et)[1]["sureklilik"]; jf = int(np.flatnonzero(H[k] & np.isfinite(Sh["MOM_FIP"][k]))[0])
    if abs(Sh["MOM_FIP"][k, jf] - (sira(Sd["MOM_12_1"][k])[jf] + sira(sur[k])[jf]) / 2) > 1e-12:
        hata.append("5) MOM_FIP havuz içi sıralarla yeniden hesaplanmadı")
    if not TK.esit(Sh["ROE_TTM"], np.where(H, Sd["ROE_TTM"], nan)) or "REV_YOY" not in Sh or not np.isfinite(Sh["REV_YOY"]).any():
        hata.append("5) ham sinyal havuzda K60 değeriyle aynı değil / REV_YOY ek satırı yok")
    uc = KB.k60b_uclar(Sh["BM"], "+", "surekli", H, bag, Bt); hs = np.flatnonzero(H[k] & np.isfinite(Sh["BM"][k])); mu = max(1, int(round(0.2 * len(hs)))); so = hs[np.argsort(Sh["BM"][k][hs])]
    if set(np.flatnonzero(uc["UST"]["sec"][k])) != set(so[-mu:]) or set(np.flatnonzero(uc["ALT"]["sec"][k])) != set(so[:mu]) or uc["UST"]["say"][k] != len(hs) or uc["UST"]["min"] != 20:
        hata.append("5) havuz içi ÜST / ALT %20 yanlış")
    ue = KB.k60b_uclar(Sh["VOL_60D"], "-", "surekli", H, bag, Bt); hv = np.flatnonzero(H[k])
    if set(np.flatnonzero(ue["UST"]["sec"][k])) != set(hv[np.argsort(vol[k][hv])][:max(1, int(round(0.2 * len(hv))))]):
        hata.append("5) eksi yönlü sinyalde ÜST uç havuzun en DÜŞÜK değerleri olmalıydı")
    ub = KB.k60b_uclar(Sh["E_S3"], "-", "bayrak", H, bag, Bt)
    if list(ub) != ["ALT"] or not np.array_equal(ub["ALT"]["sec"], H & (np.nan_to_num(Sh["E_S3"]) > 0.5)) or ub["ALT"]["min"] != 2:
        hata.append("5) bayrak ucu = bayraklı havuz hisseleri olmalıydı")
    if [s["kod"] for s in KB.k60b_satirlar() if not s["hipotez"]] != ["REV_YOY"] or sum(s["hipotez"] for s in KB.k60b_satirlar()) != 89:
        hata.append("5) satır listesi 77 sinyal + 12 bileşik (hipotez) + REV_YOY (aile dışı) değil")
    # 6) kat / ASIM elle
    Od = KB.k60b_donem_olc(P, Sh, H, "kesif", bag, Et, test_b(plasebo={"n": 6})); T = Od["tablo"]; A = Od["aylik"]
    r = T[(T.sinyal == "ROE_TTM") & (T.taraf == "UST") & (T.ufuk == 12)].iloc[0]; u = KB.k60b_uclar(Sh["ROE_TTM"], "+", "surekli", H, bag, Bt)["UST"]
    pm = K60.k60_donem_aylari(P, "kesif", 1, Et) & H.any(axis=1); F = P["F"][12]; nd = nb = kd = kb = kdm = kbm = 0; fd = []; fb = []; ays = 0
    for m_ in np.flatnonzero(pm & (u["say"] >= 20)):
        if m_ + 12 > M - 1:
            continue
        ays += 1
        for x in np.flatnonzero(H[m_]):
            if np.isfinite(F[m_, x]):
                nb += 1; kb += F[m_, x] >= 1.0; kbm += F[m_, x] <= -0.5; fb.append(F[m_, x])
                if u["sec"][m_, x]:
                    nd += 1; kd += F[m_, x] >= 1.0; kdm += F[m_, x] <= -0.5; fd.append(F[m_, x])
    if not (r.ay == ays and r.n == nd and r.n_havuz == nb and abs(r.P_p100 - kd / nd) < 1e-15 and abs(r.havuz_p100 - kb / nb) < 1e-15 and abs(r.kat_p100 - (kd / nd) / (kb / nb)) < 1e-12
            and abs(r.kat_m50 - (kdm / nd) / (kbm / nb)) < 1e-12 and abs(r.asim - r.kat_p100 / r.kat_m50) < 1e-12 and abs(r.ort - np.mean(fd)) < 1e-12 and abs(r.medyan - np.median(fd)) < 1e-12
            and abs(r.havuz_ort - np.mean(fb)) < 1e-12 and abs(r.havuz_medyan - np.median(fb)) < 1e-12 and bool(r.olculdu)):
        hata.append("6) kat / ASIM / ortalama / medyan düz döngüyle aynı değil")
    a = A[(A.sinyal == "ROE_TTM") & (A.taraf == "UST")]; ix = K60.k60_blok_dizini(len(a)); g_ = lambda c: a[c].to_numpy(float)  # noqa: E731
    Lp = (g_("k_p100")[ix].sum(1) / g_("n")[ix].sum(1)) / (g_("k_havuz_p100")[ix].sum(1) / g_("n_havuz")[ix].sum(1)); Lm = (g_("k_m50")[ix].sum(1) / g_("n")[ix].sum(1)) / (g_("k_havuz_m50")[ix].sum(1) / g_("n_havuz")[ix].sum(1))
    with np.errstate(divide="ignore", invalid="ignore"):
        As = (Lp / Lm)[np.isfinite(Lp / Lm) & (Lm > 0)]
    if abs(r.alt_p100 - np.percentile(Lp, 2.5)) > 1e-12 or abs(r.ust_m50 - np.percentile(Lm, 97.5)) > 1e-12 or r.asim_gecerli != len(As) \
            or (len(As) >= 400 and (abs(r.asim_alt - np.percentile(As, 2.5)) > 1e-12 or abs(r.p_asim - K60._k60_norm_p(np.log(r.asim) / np.log(As).std(ddof=1))) > 1e-12)):
        hata.append("6) aralıklar / p değeri aylık sayımlardan (K60 çekilişleriyle) yeniden üretilemiyor")
    z = KB.k60b_kat([0, 0, 0], [5, 5, 5], [1, 2, 3], [50, 50, 50], [0, 0, 0], [2, 2, 2]); z2 = KB.k60b_kat([1, 1, 1], [5, 5, 5], [0, 0, 0], [50, 50, 50], [1, 0, 1], [2, 2, 2])
    if z["kat_p100"] != 0 or not np.isnan(z["asim"]) or not np.isnan(z["asim_alt"]) or np.isfinite(z2["kat_p100"]) or KB.k60b_sartlar({**z, "olculdu": True, "ort": 1, "havuz_ort": 0, "medyan": 1, "havuz_medyan": 0})["firsat"]:
        hata.append("6) olaysız uç / olaysız havuzda kat ve ASIM tanımsız kalmalı, şart sağlanmamalıydı")
    if set(T.ufuk.unique()) != {12, 6} or T[(T.sinyal == "REV_YOY")].hipotez.any() or not T[T.sinyal == "BM"].hipotez.all():
        hata.append("6) tablo ufukları (12 ana, 6 bilgi) / hipotez işareti yanlış")
    # 7) aylık portföy
    ol = pm & (u["say"] >= 20); pf, Ap = KB.k60b_portfoy(P, u["sec"], ol, H, Bt); Xp = K58.k58_portfoy(P["R"], u["sec"], H, ol, 0.001); kk = np.flatnonzero(ol)
    elle_k = np.array([np.nanmean(P["R"][i][H[i]]) for i in kk]); reg = K59.k59_ols_nw(Xp["net"], Xp["kiyas"], 6)
    if not np.allclose(Xp["kiyas"], elle_k) or abs(pf["pf_fazla"] - 12 * (Xp["net"] - elle_k).mean()) > 1e-12 or abs(pf["pf_t_alfa"] - reg["t"][0]) > 1e-12 or abs(r.pf_fazla - pf["pf_fazla"]) > 1e-12 \
            or len(Ap) != len(kk) or np.isfinite(KB.k60b_portfoy(P, u["sec"], np.zeros(M, bool), H, Bt)[0]["pf_fazla"]):
        hata.append("7) aylık portföy (kıyas = havuz eşit ağırlık, net fazla, NW t(alfa)) yanlış")
    # 8) plasebo tohumu
    Pl = Od["plasebo"]; Pl2 = KB.k60b_donem_olc(P, Sh, H, "kesif", bag, Et, test_b(plasebo={"n": 6}))["plasebo"]; Pl3 = KB.k60b_donem_olc(P, Sh, H, "kesif", bag, Et, test_b(plasebo={"n": 6, "tohum": 7}))["plasebo"]
    S3 = np.random.default_rng(60200 + 3).random(U.shape); S3[~H] = nan; s3 = K58.k58_ust_dilim(S3, H, 0.2)
    r3 = KB.k60b_olc(P, s3, pm, {h: KB._k60b_taban(P, H, h, Bt) for h in (12, 6)}, Bt)[0][0]
    if len(Pl) != 6 or not Pl.equals(Pl2) or Pl.asim.equals(Pl3.asim) or abs(Pl.asim[3] - r3["asim"]) > 1e-15 or (s3 & ~H).any() or abs(s3[k].sum() - max(1, round(0.2 * H[k].sum()))) > 0:
        hata.append("8) plasebo default_rng(60200 + i) havuz içi rastgele sıranın ÜST %20'si değil / tekrar üretilemiyor")
    # 9) seçim, geçiş, etiket (elle tablolar)
    Bs = test_b(plasebo={"n": 40}); npl = 40
    Plx = pd.DataFrame({"asim": np.linspace(0.8, 1.25, npl), "kat_m50": np.linspace(0.75, 1.3, npl), "olculdu": True, "alt_p100": 0.8, "asim_alt": 0.7, "ust_m50": 1.2, "kat_p100": 1.0,
                        "ort": 0.1, "havuz_ort": 0.1, "medyan": 0.0, "havuz_medyan": 0.0})
    s_ = lambda s, t, d="kesif", **kw: {"sinyal": s, "taraf": t, "donem": d, "ufuk": 12, "hipotez": True, "olculdu": True, "kat_p100": 1.0, "alt_p100": 0.9, "ust_p100": 1.1, "kat_m50": 1.0,  # noqa: E731
                                        "alt_m50": 0.9, "ust_m50": 1.1, "asim": 1.0, "asim_alt": 0.9, "asim_ust": 1.1, "ort": 0.10, "havuz_ort": 0.10, "medyan": 0.0, "havuz_medyan": 0.0,
                                        "p_asim": 0.5, "p_koruma": 0.5, **kw}
    iyi = dict(kat_p100=1.6, alt_p100=1.3, asim=1.5, asim_alt=1.2, ort=0.2, p_asim=1e-5); kor = dict(kat_m50=0.6, ust_m50=0.8, kat_p100=0.95, medyan=0.05, p_koruma=1e-5)
    Tx = pd.DataFrame([s_("A", "UST", **iyi), s_("B", "UST", **{**iyi, "asim": 1.2, "asim_alt": 1.05}), s_("C", "UST", **{**iyi, "ort": 0.05}), s_("D", "UST", **{**iyi, "olculdu": False}),
                       s_("E", "UST", **{**iyi, "hipotez": False}), s_("G", "ALT", **kor), s_("H", "ALT", **{**kor, "kat_p100": 0.85}), s_("I", "ALT", **{**kor, "medyan": -0.01}),
                       s_("J", "ALT", **{**kor, "kat_m50": 0.78, "ust_m50": 0.95}), {**s_("A", "UST", **iyi), "ufuk": 6}] + [s_(f"Z{i}", "UST") for i in range(10)]
                      + [s_("A", "UST", "dogrulama", **iyi), s_("A", "UST", "kasa", **{**iyi, "asim_alt": 0.97}), s_("G", "ALT", "dogrulama", **kor), s_("G", "ALT", "kasa", **kor),
                         s_("K", "UST", "dogrulama", **iyi)])
    Sc = KB.k60b_secim(Tx, Plx, Bs); es = Sc["esik"]
    if not (es["hipotez"] == 17 and 1.2 < es["asim_maks"] <= 1.25 and 0.75 <= es["kat_m50_min"] < 0.8 and Sc["aday"] == [{"sinyal": "A", "taraf": "UST", "yol": "FIRSAT"}, {"sinyal": "G", "taraf": "ALT", "yol": "KORUMA"}]
            and Tx.bh_asim.sum() >= 1 and not Tx[Tx.donem != "kesif"].aday_firsat.any()):
        hata.append(f"9) KEŞİF seçimi kuralları yanlış: {es} {Sc['aday']}")
    Gd = KB.k60b_gecis(Tx, Plx, Sc["aday"], "dogrulama", Bs); Gk = KB.k60b_gecis(Tx, Plx, Sc["aday"], "kasa", Bs); et = KB.k60b_etiketler(Sc["aday"], Gd["sonuc"], Gk["sonuc"], Bs)
    if not (abs(Gd["plasebo"]["asim95"] - np.percentile(Plx.asim, 95)) < 1e-12 and abs(Gd["plasebo"]["kat_m50_05"] - np.percentile(Plx.kat_m50, 5)) < 1e-12 and Gd["plasebo"]["plasebo_firsat_oran"] == 0
            and [x["gecer"] for x in Gd["sonuc"]] == [True, True] and [x["gecer"] for x in Gk["sonuc"]] == [False, True] and Gk["sonuc"][0]["nokta"]
            and et[0]["etiket"].startswith("YAKIN (K60B-KOŞULLU FIRSAT") and "KASA" in et[0]["etiket"] and et[1]["etiket"] == "K60B-KOŞULLU KORUMA" and et[1]["dogrulama"] and et[1]["kasa"]):
        hata.append(f"9) geçiş / etiket / YAKIN kuralları yanlış: {Gd['sonuc']} {Gk['sonuc']} {et}")
    Plk = Plx.assign(alt_p100=1.2, asim_alt=1.1, ort=0.2)
    if not KB.k60b_gecis(Tx, Plk, Sc["aday"], "kasa", Bs)["plasebo"]["aralik_dar"] or Gd["plasebo"]["aralik_dar"]:
        hata.append("9) plasebo şart sağlama oranı > %5 iken 'aralık dar' notu düşmedi")
    if KB.k60b_etiketler([{"sinyal": "Q", "taraf": "UST", "yol": "FIRSAT"}], [], [], Bs)[0]["etiket"] != "":
        hata.append("9) sonraki dönemlerde ölçülmeyen aday etiket aldı")
    # 10) uçtan uca sentetik koşu + rapor + yeniden üretim
    with tempfile.TemporaryDirectory() as td:
        try:
            R = KB.k60b_kos(td, demet=D, E=Et, B=Bt); m = json.load(open(os.path.join(td, "k60b_meta.json"), encoding="utf-8"))
            for a_ in ("k60b_tablo.csv", "k60b_aylik.csv", "k60b_portfoy_aylik.csv", "k60b_plasebo.csv", "k60b_meta.json", "K60B_RAPOR.md"):
                if not os.path.exists(os.path.join(td, a_)):
                    hata.append(f"10) çıktı yok: {a_}")
            Tt = pd.read_csv(os.path.join(td, "k60b_tablo.csv")); At = pd.read_csv(os.path.join(td, "k60b_aylik.csv")); Pt = pd.read_csv(os.path.join(td, "k60b_plasebo.csv"))
            if m["onkayit"]["dosya_sha256"] != KB.K60B_ONKAYIT_SHA or set(Tt.donem) != set(K60.K60_DONEM) or len(Pt) != 3 * Bt["plasebo"]["n"] or m["esik"]["hipotez"] != int(((Tt.donem == "kesif") & (Tt.ufuk == 12) & Tt.hipotez & Tt.olculdu).sum()):
                hata.append("10) meta / tablo / plasebo tutarsız")
            for d_ in K60.K60_DONEM:
                rr = Tt[(Tt.sinyal == "BM") & (Tt.taraf == "UST") & (Tt.donem == d_) & (Tt.ufuk == 12)].iloc[0]; aa = At[(At.sinyal == "BM") & (At.taraf == "UST") & (At.donem == d_)]
                kz = KB.k60b_kat(aa.k_p100, aa.n, aa.k_havuz_p100, aa.n_havuz, aa.k_m50, aa.k_havuz_m50, Bt)
                if any(abs(rr[c] - kz[c]) > 1e-12 for c in ("kat_p100", "alt_p100", "kat_m50", "ust_m50", "asim") if np.isfinite(rr[c])) or len(aa) != rr.ay:
                    hata.append(f"10) {d_}: tablo satırı k60b_aylik.csv'den yeniden üretilemiyor")
            ad_t = {(r_.sinyal, r_.taraf) for r_ in Tt[Tt.aday_firsat | Tt.aday_koruma].itertuples()}
            if ad_t != {(x["sinyal"], x["taraf"]) for x in m["aday"]} or len(m["etiket"]) != len(m["aday"]) or any(x["etiket"] and not x["etiket"].startswith(("K60B-", "YAKIN")) for x in m["etiket"]):
                hata.append("10) adaylar / etiketler tablo ile meta arasında tutarsız")
            if not m["aday"]:
                hata.append("10) ekilmiş etki (kalite -> getiri) havuz içinde hiç aday üretmedi (test kurgusu zayıf)")
            rp = open(os.path.join(td, "K60B_RAPOR.md"), encoding="utf-8").read()
            for parca in ("## Bulgular (düz dille)", "## Havuz ve taban oranlar", "## KEŞİF seçimi", "## Plasebo", "## Önceden adı konan başlık satırları", "## Üç dönemde de kat_m50 < 1",
                          "## BOŞLUK", "| DOSYA_Y (ÜST) | KEŞİF |", "| E_RSPLIT (ALT) |", "| REV_YOY (ÜST) |", "İZ değildir"):
                if parca not in rp:
                    hata.append(f"10) raporda '{parca}' yok")
            os.remove(os.path.join(td, "K60B_RAPOR.md")); KB.k60b_rapor(td, Bt)
            if open(os.path.join(td, "K60B_RAPOR.md"), encoding="utf-8").read() != rp:
                hata.append("10) rapor çıktılardan yeniden üretilince değişti")
            for f_ in os.listdir(td):
                if K60._K60_EPOSTA.search(open(os.path.join(td, f_), encoding="utf-8").read()):
                    hata.append(f"10) sentetik çıktıda e-posta var: {f_}")
            del R
        except Exception as ex:
            import traceback
            hata.append(f"10) uçtan uca sentetik koşu çöktü: {type(ex).__name__} {ex} | {traceback.format_exc()[-700:]}")
    durmali(lambda: KB.k60b_rapor(os.path.join(tempfile.gettempdir(), "k60b_yok_klasor")), "10) çıktı yokken rapor durmadı", hata)
    # 11) e-posta / anahtar yok; K60B ağ kullanmaz
    anahtar = re.compile(r"(api[_-]?key\s*[:=]\s*['\"]\w{8,}|bearer\s+[A-Za-z0-9_\-]{16,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,})", re.I)
    for y in (os.path.join(KOK, "K60B.py"), os.path.join(KOK, "test_k60b.py")):
        mt = open(y, encoding="utf-8").read()
        if K60._K60_EPOSTA.search(mt) or anahtar.search(mt):
            hata.append(f"11) e-posta / anahtar biçimli parça var: {os.path.basename(y)}")
    if "urlopen" in src or "requests." in src or "K60_SEC_UA" in src:
        hata.append("11) K60B.py ağ isteği atabilecek kod içeriyor")
    _ = subprocess
    return hata


if __name__ == "__main__":
    Hh = testler()
    if Hh:
        print("K60-B TEST: HATA", len(Hh)); print("\n".join(Hh)); sys.exit(1)
    print("K60-B TEST: GEÇTİ")
