"""INTEM_ILERI testleri (yalnız SENTETİK veri; gerçek veride getiri ölçmez). Çalıştırma: python test_intem_ileri.py

1) çakışma kapısı  2) eşleşme: sabit cetvelle ii_esle = FON_IZI fi_k44_eslesme (aynı havuzda, SAPMA-1 sonrası) birebir
3) GELECEĞE BAKMA: seri t'de kesilince aynı pencere ölçüleri ve aynı eşleşme; SAPMA-1 gerekçesi (kesik seride erken pencere yok)
4) ii_k45 (tam=None) = FON_IZI fon_izi_k45 satırı birebir  5) tam pencere süzgeci (SAPMA-4) son barları atar, rastgeleye de uygulanır
6) cetvel çağrısı: OC.oc_olc uçtan uca + rapor  7) kapı: doğru ön kayıt geçer; sha farkı / satır eksik / kontrol eksik durur
8) eski kayıt alıntıları IZ_KARNE metninde  9) olay sha sıradan bağımsız; ileri test cümlesi eşlemesi  10) e-posta / anahtar yok.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
warnings.filterwarnings("ignore", category=RuntimeWarning); warnings.filterwarnings("ignore", message="All-NaN")
import FON_IZI as F  # noqa: E402
import INTEM_ILERI as II  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402


def _seri(tohum: int, T: int = 700, bas: str = "2019-01-01") -> pd.DataFrame:
    """Sentetik hisse: rejimli oynaklık ve eğilim (düşüş sonrası duraklama pencereleri üretir)."""
    rng = np.random.default_rng(tohum); idx = pd.bdate_range(bas, periods=T); a = np.arange(T)
    sig = np.where((a // 50) % 2 == 0, 0.035, 0.012) * (1 + 0.3 * (tohum % 3)); dr = np.where((a // 120) % 2 == 0, -0.004, 0.003)
    C = 40 * np.exp(np.cumsum(rng.normal(dr, sig)))
    O = C * np.exp(rng.normal(0, 0.006, T)); H = np.fmax(O, C) * (1 + rng.uniform(0.002, 0.02, T)); L = np.fmin(O, C) * (1 - rng.uniform(0.002, 0.02, T))
    Vol = rng.integers(5e4, 5e5, T).astype(float) * np.where((a // 30) % 3 == 0, 0.5, 1.0)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": Vol}, index=idx)


def json_kayit(T: pd.DataFrame):
    return json.loads(T.to_json(orient="records", force_ascii=False))


def testler():
    hata = []; bilgi = {}

    # 1) çakışma kapısı
    kod = open(os.path.join(KOK, "INTEM_ILERI.py"), encoding="utf-8").read()
    g = {"__name__": "colab_benzeri", "ii_tara": "baska_dosyanin_adi", "__file__": os.path.join(KOK, "INTEM_ILERI.py")}
    try:
        exec(compile(kod, "INTEM_ILERI.py", "exec"), g); hata.append("1 çakışma kapısı durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1 beklenmeyen hata: {ex}")
    g2 = {"__name__": "colab_benzeri", "__file__": os.path.join(KOK, "INTEM_ILERI.py")}
    try:
        exec(compile(kod, "INTEM_ILERI.py", "exec"), g2); exec(compile(kod, "INTEM_ILERI.py", "exec"), g2)
    except RuntimeError as ex:
        hata.append(f"1 aynı dosyanın yeniden yüklenmesi durdu: {ex}")

    # 2) eşleşme: sabit cetvel = fi_k44_eslesme (cetvel = sentetik havuz; hedef = havuzdaki bir pencerenin ölçüleri)
    L = 20; K = F.FI_K44
    V = {f"S{s:02d}": _seri(s) for s in range(30)}
    Hh = F.fi_k44_havuz(V, L, K)
    hedef = Hh.iloc[len(Hh) // 3][list(K["olcu"])].astype(float)
    hy = F.fi_k44_yuzdelik(Hh, hedef.to_frame().T, K).iloc[0]
    band = 0.30   # sentetik havuz küçük: geniş bant yalnız testte (kural bandı ii'de değişmez)
    c = {"H": Hh, "hy": hy, "band": band}
    E0 = F.fi_k44_eslesme(Hh, hy, band, K)
    ref = set(zip(E0.sembol, pd.to_datetime(E0.tarih)))
    yeni = set(); erken = 0
    for s, d in V.items():
        X = II.ii_pencereler(d, L); m = II.ii_esle(X, c)
        yeni |= set((s, t) for t in pd.to_datetime(X.tarih[m]))
        P = F.fi_k23_parmak(d, L); erken_t = set(P.index[P["i"] < L + 199])
        erken += len([1 for (s_, t) in ref if s_ == s and t in erken_t])
    ref_s1 = {(s, t) for (s, t) in ref if t not in set(F.fi_k23_parmak(V[s], L).pipe(lambda P: P.index[P["i"] < L + 199]))}
    if yeni != ref_s1:
        hata.append(f"2 eşleşme FON_IZI ile aynı değil: yeni {len(yeni)}, ref {len(ref_s1)}, ortak {len(yeni & ref_s1)}")
    if len(yeni) < 20:
        hata.append(f"2 sentetik eşleşme az ({len(yeni)})")
    bilgi.update({"eslesme": len(yeni), "sapma1_erken": erken})

    # 3) geleceğe bakma: kesik seride aynı ölçüler ve aynı eşleşme; SAPMA-1 gerekçesi
    bozuk = 0; say = 0
    for (s, t) in sorted(yeni)[:40]:
        say += 1
        Xt = II.ii_pencereler(V[s].loc[:t], L); Xt = Xt[Xt.tarih == t]
        Xf = II.ii_pencereler(V[s], L); Xf = Xf[Xf.tarih == t]
        if len(Xt) != 1 or not np.allclose(Xt[list(K["olcu"])].to_numpy(float), Xf[list(K["olcu"])].to_numpy(float)) or not II.ii_esle(Xt, c)[0]:
            bozuk += 1
    if bozuk or not say:
        hata.append(f"3 geleceğe bakma: {bozuk} / {say} sinyal kesik seride farklı")
    s0 = "S00"; P0 = F.fi_k23_parmak(V[s0], L); t_erken = P0.index[P0["i"] == L + 100][0]
    if len(F.fi_k23_parmak(V[s0].loc[:t_erken], L)):
        hata.append("3 SAPMA-1 gerekçesi: kesik seride erken pencere ölçülüyor (beklenmedi)")
    if (II.ii_pencereler(V[s0], L).tarih == t_erken).any():
        hata.append("3 ii_pencereler SAPMA-1 penceresini almış")

    # 4) ii_k45 (tam=None) = fon_izi_k45 birebir
    Ek = pd.DataFrame(sorted(yeni)[:35], columns=["sembol", "gun"])
    gun = pd.DatetimeIndex(sorted(set().union(*[d.index for d in V.values()]))); j = gun.searchsorted(pd.DatetimeIndex(Ek.gun), side="right")
    ok = j < len(gun); Ek = Ek[ok].assign(giris=gun[j[ok]]); Ek = Ek[[g_ in V[s].index for s, g_ in zip(Ek.sembol, Ek.giris)]]
    with tempfile.TemporaryDirectory() as td:
        A = F.FIAyar(); A.cikti = td
        Z = F.fon_izi_k45({"ABD": V}, Ek.assign(pazar="ABD", pencere=L), A)["ozet"].iloc[0].to_dict()
    r = II.ii_k45(V, Ek, None); r.pop("_olay", None); r.pop("n_rast", None)
    farkli = [k for k, v in r.items() if k in Z and not (pd.isna(v) and pd.isna(Z[k])) and not np.isclose(float(v), float(Z[k]))]
    if farkli or r["n"] != Z["n"]:
        hata.append(f"4 ii_k45 fon_izi_k45 ile farklı: {farkli[:6]}")
    bilgi["k45_n"] = int(r["n"])

    # 5) tam pencere süzgeci
    son = pd.DataFrame({"sembol": ["S01", "S01", "S01"], "giris": [V["S01"].index[100], V["S01"].index[-41], V["S01"].index[-40]]})
    kal = II.ii_tam(V, son, 41)
    if list(kal.giris) != [V["S01"].index[100], V["S01"].index[-41]]:
        hata.append(f"5 tam pencere süzgeci yanlış: {list(kal.giris)}")
    Vk = {s: d.iloc[:-30] for s, d in V.items()}   # kesik veri: son 30 gündeki olaylar ölçülmemeli
    Ek2 = Ek[[g_ in Vk[s].index for s, g_ in zip(Ek.sembol, Ek.giris)]]
    r2 = II.ii_k45(Vk, Ek2, 41)
    if r2.get("n", 0) and len(II.ii_tam(Vk, r2["_olay"][["sembol", "giris"]], 41)) != r2["n"]:
        hata.append("5 tam süzgeçli ii_k45 kesik pencereli olay ölçmüş")

    # 6) cetvel çağrısı uçtan uca (OC.oc_olc + rapor)
    Vp = {f"P{s:02d}": _seri(s, T=900, bas="2021-01-01") for s in range(45)}
    Vd = OC._oc_veri_sar(Vp, "ABD")
    Hp = F.fi_k44_havuz(Vd["V"], L, K); hyp = F.fi_k44_yuzdelik(Hp, Hp.iloc[len(Hp) // 2][list(K["olcu"])].astype(float).to_frame().T, K).iloc[0]
    cp = {"H": Hp, "hy": hyp, "band": 0.30}
    S, say6 = II.ii_tara(Vd | {"kaynak": {s: "k34_yahoo" for s in Vd["V"]}}, sorted(Vd["V"]), {L: cp})
    R = OC.oc_olc(S[["sembol", "tarih", "pazar"]], {"ABD": Vd})
    if not {"ort_fark", "alt95", "durum", "olas"} <= set(R["hucre"].columns) or len(R["hucre"]) != 3:
        hata.append("6 oc_olc hücre tablosu eksik")
    if R["sayim"]["ABD"]["girdi"] != len(S):
        hata.append("6 oc_olc sayımı girdi ile tutmuyor")
    if R["cetvel_sha"] != OC.oc_esik_sha():
        hata.append("6 cetvel sha farklı")
    J = {"surum": II.II_SURUM, "kos_bas_utc": "x", "kos_son_utc": "y", "sure_sn": 0, "kapi": {}, "dogrula": {"20": {"c124_n": 1, "yeniden": 1, "ortak": 1}},
         "gorulmemis_hisse": 45, "sayim_tarama": say6, "gelecek_denetim": {"ornek": 1, "bozuk": []}, "etiket": R["etiket"],
         "ileri_cumle": II.ii_ileri_cumle(R["etiket"]), "hucre": {"20": json_kayit(R["hucre"])}, "olasilik": {"20": json_kayit(R["olasilik"])},
         "k45": [{"pencere": 20, "grup": "2016-26 (hepsi)", **{k: v for k, v in r.items()}, "kural": II.ii_k45_kural(r)}],
         "eski": II.ii_eski_dogrula(), "oc_rapor": OC.oc_rapor(R, "test"), "oc_rapor_L10": OC.oc_rapor(R, "test L10")}
    md = II.ii_rapor_md(J)
    if "DÜZ DİL ÖZET" not in md or "Olasılık tablosu" not in md or "kendi ölçüsü" not in md:
        hata.append("6 rapor bölümleri eksik")
    bilgi["oc_olay"] = int(R["sayim"]["ABD"]["girdi"])

    # 7) kapı (git=False; sentetik ön kayıt)
    with tempfile.TemporaryDirectory() as td:
        yol = os.path.join(td, "on.md")
        metin = "\n".join([OC.oc_kapi_satirlari(), f"II_ESIK_SHA: `{II.ii_esik_sha()}`", f"FI_PARAM_SHA: `{II.ii_fi_param_sha()}`",
                           f"FI_KOD_SHA: `{II.ii_fi_kod_sha()}`", f"II_KOD_SHA: `{II.ii_kod_sha()}`", f"HEDEF_CETVEL_SHA: `{'0' * 64}`",
                           f"OLAY_SHA: `{'0' * 64}`", "", II.ii_kontrol_tablosu()])
        open(yol, "w", encoding="utf-8").write(metin)
        try:
            II.ii_kapi(yol, git=False)
        except II.IIHata as ex:
            hata.append(f"7 doğru ön kayıt geçmedi: {ex}")
        for eski, yeni_ in ((II.ii_esik_sha(), "1" * 64), (II.ii_fi_kod_sha(), "2" * 64), ("OLAY_SHA:", "OLAY_SH_:"), (OC.oc_esik_sha(), "3" * 64)):
            open(yol, "w", encoding="utf-8").write(metin.replace(eski, yeni_, 1))
            try:
                II.ii_kapi(yol, git=False); hata.append(f"7 bozuk ön kayıt geçti ({yeni_[:6]})")
            except II.IIHata:
                pass
        open(yol, "w", encoding="utf-8").write(metin.replace("| K3 |", "| K3x |"))
        try:
            II.ii_kapi(yol, git=False); hata.append("7 eksik kontrol satırıyla geçti")
        except II.IIHata:
            pass

    # 8) eski kayıt alıntıları
    if not all(e["metinde"] for e in II.ii_eski_dogrula()):
        hata.append(f"8 eski alıntı IZ_KARNE metninde yok: {[e['alinti'][:30] for e in II.ii_eski_dogrula() if not e['metinde']]}")

    # 9) olay sha sıradan bağımsız; ileri test cümlesi
    if II.ii_olay_sha(S) != II.ii_olay_sha(S.sample(frac=1, random_state=1)):
        hata.append("9 olay sha sıraya bağlı")
    for kh, bek in (({"ABD 2023": "TUTAR", "ABD 2024-26": "TUTAR"}, "TUTTU"), ({"ABD 2023": "TUTAR", "ABD 2024-26": "ÖLÇÜLEMEDİ"}, "KISMEN"),
                    ({"ABD 2023": "TUTMADI", "ABD 2024-26": "TUTMADI"}, "TUTMADI"), ({"ABD 2023": "ÖLÇÜLEMEDİ", "ABD 2024-26": "TUTMADI"}, "ÖLÇÜLEMEDİ")):
        if bek not in II.ii_ileri_cumle({"karar_hucre": kh}):
            hata.append(f"9 ileri cümle {kh} -> {II.ii_ileri_cumle({'karar_hucre': kh})}")

    # 10) e-posta / anahtar
    for ad in ("INTEM_ILERI.py", "test_intem_ileri.py"):
        m = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.(com|org|net|io|tr)\b", m) or re.search(r"(api[_-]?key|token|sifre)\s*=\s*['\"][^'\"]{6,}", m, re.I):
            hata.append(f"10 {ad}: e-posta / anahtar deseni")
    return hata, bilgi


if __name__ == "__main__":
    h, bilgi = testler()
    print(bilgi)
    if h:
        print("BAŞARISIZ:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_intem_ileri: 10/10 GEÇTİ")
