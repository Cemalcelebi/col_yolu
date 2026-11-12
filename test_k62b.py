"""K62-B testleri (ağ gerekmez; yalnız SENTETİK veri, gerçek veride getiri ölçmez). Çalıştırma: python test_k62b.py

1) çakışma kapısı  2) mühür (eşik / karar sırası değişince değişir; K64 ve K62 mührü girer) ve ön kayıt (karar sırası seçilmeden yazılmaz; seçim kuralıyla çelişirse
yazılmaz; üzerine yazmaz; bozuk / farklı mühür reddi; gerçek K62B_ON_KAYIT.md varsa bugünkü mühürle aynı)  3) 'ön kayıt git'e işlenmiş ve değişmemiş değilse kos
reddeder' (yok / işlenmemiş / sonradan değişmiş / mühür farklı; işlenmişse koşar)  4) BIST açıklama değerleri K62.k62_olay_tablosu (deger=True) ile birebir;
TMS 29 kirli çeyrekte SUETF yok  5) ABD: SUETF elle (NI farkı / (kapanış x bilinen pay)), defter değeri satırları ve PD elle, EAR elle (K62 portföyüyle), yedek
kural günlü çeyrek açıklama sayılmaz, takvim dışı açıklamada EAR / karar yok  6) son açıklama ve 90 gün kuralı (karar < t kesin; ann >= t - 90; değeri yoksa
daha eskiye gidilmez; aynı karar gününde geç dönem; hiç / yok90 / kirli bayrakları)  7) GELECEĞE BAKMA YOK: (a) karar günü >= t olan açıklamalar (değer, gün,
yeni satır) bozulunca t ve öncesi değerler / sıralar aynı; (b) ABD'de g gününden sonraki fiyat, pay ve net kâr bozulunca karar günü < g olan açıklamaların
SUETF / EAR'ı aynı  8) ÇÖL + SÜRPRİZ sınıfı = K62.k62_tertil_onsel (BIST SUETF'te kirli havuz hariç)  9) karar sırası seçim kuralı (toplanma eşikleri)
10) kapsam sayım modu: getiri / eşli fark sütunu yok, sayılar olay tablosuyla aynı  11) uçtan uca sentetik kos + rapor (K64 S1 / karar; bilgi grupları; çıktılardan
yeniden üretim)  12) e-posta / anahtar / SEC adresi yok.
"""
from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K62B as B  # noqa: E402

K62, K64, K60, FI = B.K62, B.K64, B.K60, B.FI


def _git(kl: str, *a: str) -> None:
    subprocess.run(["git", "-C", kl, "-c", "user.name=test", "-c", "user.email=test@invalid", "-c", "commit.gpgsign=false", *a], check=True, capture_output=True, timeout=60)


def E_test(sec: dict = None) -> dict:
    E = copy.deepcopy(B.K62B_ESIK); E["olay"]["d13"]["etkin"] = False
    E["sira"]["karar"] = sec or {"SUETF_C": "EVREN", "EAR_C": "IC"}
    return E


def sentetik_fiyat(S: list, bas: str = "2015-06-01", bit: str = "2026-08-31", tohum: int = 3) -> dict:
    """Oynak sentetik fiyatlar (K24 sinyali üretecek kadar)."""
    rng = np.random.default_rng(tohum); gun = pd.bdate_range(bas, bit); G = len(gun); V = {}
    for j, s in enumerate(S):
        r = rng.normal(0.0003, 0.032, G) + 0.5 * rng.normal(0, 0.012, G)
        for k in rng.choice(G - 60, 6, replace=False):
            r[k:k + 25] -= 0.022
        c = rng.uniform(5, 60) * np.exp(np.cumsum(r)); o = c * np.exp(rng.normal(0, 0.006, G))
        h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.006, G))); lo = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.006, G)))
        V[s] = pd.DataFrame({"Open": o, "High": h, "Low": lo, "Close": c, "Volume": rng.integers(2e5, 2e6, G).astype(float)}, index=gun)
    return V


def sentetik_duyuru(V: dict, tohum: int = 4, kirli: bool = False) -> pd.DataFrame:
    """Her hisse için her çeyrek bir açıklama: ann = çeyrek sonu + 30..60 gün; karar = ann'den sonraki ikinci iş günü; SUETF / EAR rastgele; birkaç değer eksik."""
    rng = np.random.default_rng(tohum); sat = []
    for s in sorted(V):
        for qs in pd.date_range("2014-03-31", "2026-06-30", freq="QE"):
            ann = (qs + pd.Timedelta(days=int(rng.integers(30, 61)))).normalize(); t = ann + pd.offsets.BDay(0); kr = t + pd.offsets.BDay(1)
            sat.append({"sembol": s, "yil": qs.year, "ceyrek": (qs.month - 1) // 3 + 1, "ann": ann, "t_gun": t, "karar": kr, "karar_i": 0,
                        "SUETF": rng.normal() if rng.random() > 0.05 else np.nan, "EAR": rng.normal(0, 0.05) if rng.random() > 0.05 else np.nan,
                        "kirli": bool(kirli and qs.year == 2024)})
    U = pd.DataFrame(sat); tak = pd.bdate_range("2014-01-01", "2026-12-31")
    U["karar_i"] = tak.searchsorted(U.karar)
    if kirli:
        U.loc[U.kirli, "SUETF"] = np.nan
    return U


def sentetik_abd(N: int = 40, tohum: int = 9) -> dict:
    """K60 benzeri ABD alt demeti: gun, kod, C, A, T (Q NetIncomeLoss, I StockholdersEquity, bit, bilgi, bilgi_kaynak, Ybit, Ybilgi, Yq, pay), bolunme."""
    rng = np.random.default_rng(tohum); gun = pd.bdate_range("2013-01-01", "2019-12-31"); G = len(gun); S = [f"A{j:02d}" for j in range(N)]
    C = rng.uniform(10, 80, N)[None, :] * np.exp(np.cumsum(rng.normal(0.0002, 0.02, (G, N)), axis=0)); Adj = C * 0.97
    qe = pd.date_range("2012-03-31", "2019-12-31", freq="QE"); nq = len(qe); q_bas = qe[0].year * 4
    NI = rng.normal(1e6, 5e5, (nq, N)); EQ = rng.uniform(1e7, 1e8, (nq, N)); EQ[:, 3] = -1e6
    bit = np.tile(qe.to_numpy("datetime64[D]")[:, None], (1, N)); bil = bit + np.timedelta64(35, "D"); kay = np.ones((nq, N), np.int8)
    kay[10, 5] = 2; bil[10, 5] = bit[10, 5] + np.timedelta64(90, "D")
    ys = sorted(set(qe.year)); ny = len(ys); Ybit = np.full((ny, N), np.datetime64("NaT", "D")); Ybilgi = Ybit.copy(); Yq = np.full((ny, N), -1)
    for yi, y in enumerate(ys):
        q = int(np.flatnonzero((qe.year == y) & (qe.month == 12))[0]); Ybit[yi] = bit[q]; Ybilgi[yi] = bil[q] + np.timedelta64(30, "D"); Yq[yi] = q
    pay = []
    for j in range(N):
        d = qe.to_numpy("datetime64[D]"); n_ = np.full(nq, 1e7 * (1 + j % 3)); b = d + np.timedelta64(35, "D"); pay.append((d, n_, b))
    T = {"q_bas": q_bas, "y_bas": ys[0], "Q": {"NetIncomeLoss": NI}, "I": {"StockholdersEquity": EQ}, "Y": {}, "bit": bit, "bilgi": bil, "bilgi_kaynak": kay,
         "Ybit": Ybit, "Ybas": Ybit.copy(), "Ybilgi": Ybilgi, "Yq": Yq, "pay": pay}
    return {"gun": gun, "kod": S, "C": C, "A": Adj, "T": T, "bolunme": {}, "var": np.ones(N, bool)}


def testler() -> list:
    hata: list = []; E = E_test()
    # 1) çakışma kapısı
    src = open(os.path.join(KOK, "K62B.py"), encoding="utf-8").read()
    try:
        exec(compile(src, "K62B.py", "exec"), {"__name__": "kapi", "k62b_kos": lambda: None}); hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "kapi2"}
    try:
        exec(compile(src, "K62B.py", "exec"), g2); exec(compile(src, "K62B.py", "exec"), g2)
    except Exception as ex:
        hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
    if "_CK_ONCE_K62B" not in src or "_cakisma_kontrol_k62b()" not in src:
        hata.append("1) çakışma kapısı adı _CK_ONCE_K62B değil")

    # 2) mühür ve ön kayıt
    E2 = copy.deepcopy(E); E2["surpriz"]["pencere_gun"] = 91; E3 = E_test({"SUETF_C": "IC", "EAR_C": "IC"})
    if len({B.k62b_esik_sha(E), B.k62b_esik_sha(E2), B.k62b_esik_sha(E3)}) != 3 or B.k62b_esik_sha(E) != B.k62b_esik_sha(copy.deepcopy(E)):
        hata.append("2) eşik / karar sırası değişince mühür değişmedi ya da mühür kararlı değil")
    import inspect
    if "K64_muhur" not in inspect.getsource(B.k62b_esik_sha) or "K62_muhur" not in inspect.getsource(B.k62b_esik_sha):
        hata.append("2) K64 / K62 mührü K62-B mührüne girmiyor")
    vs = {"V_BIST.pkl": ("a" * 64, 1), "k62_veri": ("b" * 64, 9)}
    with tempfile.TemporaryDirectory() as td:
        try:
            B.k62b_onkayit(td, vs, {**E, "sira": {**E["sira"], "karar": {"SUETF_C": None, "EAR_C": None}}})
            hata.append("2) karar sırası seçilmeden ön kayıt yazıldı")
        except B.K62BHata:
            pass
        y = B.k62b_onkayit(td, vs, E); ilk = open(y, encoding="utf-8").read(); oc = K64._k64_onkayit_oku(y)
        if oc["sha"] != B.k62b_esik_sha(E) or oc["veri"] != vs:
            hata.append(f"2) ön kayıttan mühür / veri okunamadı: {oc}")
        for parca in ("## 0. Soru", "## 2. Açıklama, değer ve BİLGİ TARİHİ", "KURAL", "90 takvim günü", "KİRLİ", "SAPMA 1", "BOŞLUK 1", "Kapsam sayımı görüldü, getiri görülmedi",
                      "SUETF_C = **EVREN", "EAR_C = **İÇ", "ABD-ADAY", "Benjamini-Hochberg", "python -I K62B.py kos", "OKUNMADI", "10-Q / 10-K başvuru günü"):
            if parca not in ilk:
                hata.append(f"2) ön kayıtta '{parca}' yok")
        if B.k62b_onkayit(td, vs, E) != y or open(y, encoding="utf-8").read() != ilk:
            hata.append("2) ön kayıt üzerine yazıldı")
        try:
            B.k62b_onkayit(td, vs, E3); hata.append("2) mühür farklıyken var olan ön kayıt kabul edildi")
        except B.K62BHata:
            pass
        try:
            B.k62b_onkayit_dogrula(td, E=E3); hata.append("2) eşiği farklı doğrulama geçti")
        except B.K62BHata:
            pass
    with tempfile.TemporaryDirectory() as td:          # seçim kuralıyla çelişen karar sırası: ön kayıt yazılmaz
        K = pd.DataFrame([{"tanim": "K24", "pazar": p, "donem": d, "degisken": k, "n_ust": 100, "n_alt": 100} for p in ("BIST", "ABD") for d in E["bagimsiz"] for k in ("SUETF_C", "EAR_C")])
        K.to_csv(B._k62b_yol("kapsam", td), index=False)
        try:
            B.k62b_onkayit(td, vs, E); hata.append("2) seçim kuralı (ikisi de EVREN) ile çelişen karar sırasıyla ön kayıt yazıldı")
        except B.K62BHata:
            pass
    gercek = B._k62b_yol("onkayit")
    if os.path.exists(gercek):
        if K64._k64_onkayit_oku(gercek)["sha"] != B.k62b_esik_sha():
            hata.append("2) gerçek K62B_ON_KAYIT.md mührü bugünkü K62B_ESIK ile aynı değil")
        if B._K62B_EPOSTA.search(open(gercek, encoding="utf-8").read()):
            hata.append("12) gerçek ön kayıtta e-posta var")

    # 4) BIST açıklama değerleri = K62 (deger=True)
    import test_k62 as T62
    S62 = T62.sentetik(n=60, bas="2015-06-01", bit="2026-08-31", tohum=17); D = S62["D"]; E62 = K62.K62_ESIK
    H62 = K62.k62_hazirla(D, E62, True); Ev = K62.k62_olay_tablosu(D, E62, True, H62); Ub = B.k62b_bist_duyuru(D, E62, H62)
    a = Ev.set_index(["kod", "yil", "ceyrek"]); b = Ub.set_index(["sembol", "yil", "ceyrek"]); b.index.names = a.index.names; b = b.reindex(a.index)
    kir = b.kirli.to_numpy(bool)
    if not np.allclose(a.SUETF.to_numpy(float)[~kir], b.SUETF.to_numpy(float)[~kir], equal_nan=True, rtol=0, atol=1e-12) or not np.allclose(a.EAR.to_numpy(float), b.EAR.to_numpy(float), equal_nan=True, rtol=0, atol=1e-12):
        hata.append("4) BIST SUETF / EAR K62.k62_olay_tablosu ile birebir değil")
    if not kir.any() or np.isfinite(b.SUETF.to_numpy(float)[kir]).any() or not np.isfinite(b.EAR.to_numpy(float)[kir]).any():
        hata.append("4) TMS 29 kirli çeyrekte SUETF var ya da EAR yok")
    tk = D["takvim"]
    if not (pd.to_datetime(Ub.karar.dropna()) > pd.to_datetime(Ub.t_gun[Ub.karar.notna()])).all() or (Ub.ann > Ub.t_gun).any():
        hata.append("4) BIST karar günü t'den sonra değil ya da ann > t")
    r0 = Ub.dropna(subset=["karar"]).iloc[50]
    if pd.Timestamp(r0.karar) != tk[int(tk.searchsorted(r0.ann)) + 1]:
        hata.append("4) BIST karar günü = yayın gününe eşit / sonraki ilk işlem günü + 1 değil")

    # 5) ABD açıklamaları elle
    Dz = sentetik_abd(); gD = Dz["gun"].to_numpy("datetime64[D]"); T = Dz["T"]; S = Dz["kod"]
    Ua, oz = B.k62b_abd_duyuru(Dz, E); I = B.k62b_abd_portfoy_girdi(Dz, E)
    if oz["yedek_gun"] != 1 or len(Ua[(Ua.sembol == "A05") & (Ua.yil == 2014) & (Ua.ceyrek == 3)]):
        hata.append(f"5) yedek kural günlü çeyrek açıklama sayıldı: {oz}")
    j = 7; q = 20; r = Ua[(Ua.sembol == S[j]) & (Ua.yil == pd.Timestamp(T["bit"][q, j]).year) & (Ua.ceyrek == (pd.Timestamp(T["bit"][q, j]).month - 1) // 3 + 1)].iloc[0]
    p = int(np.searchsorted(gD, T["bit"][q, j], side="right")) - 1; d = T["pay"][j][0]; bb = T["pay"][j][2]; i_ = int(np.searchsorted(bb, gD[p], side="left")) - 1
    sh = T["pay"][j][1][i_]; elle = (T["Q"]["NetIncomeLoss"][q, j] - T["Q"]["NetIncomeLoss"][q - 4, j]) / (Dz["C"][p, j] * sh)
    if abs(r.SUETF - elle) > 1e-12 * max(1, abs(elle)) or pd.Timestamp(r.ann) != pd.Timestamp(T["bilgi"][q, j]):
        hata.append(f"5) ABD SUETF elle hesapla aynı değil: {r.SUETF} != {elle}")
    M = I["Dk"]["mali"]; m1 = M[(M.kod == S[2]) & (M.yil == 2014)]
    if len(m1) != 1 or m1.ozkaynak.iloc[0] != T["I"]["StockholdersEquity"][int(T["Yq"][2, 2]), 2] or len(M[M.kod == S[3]]) == 0:
        hata.append("5) ABD defter değeri satırları (yıl sonu özkaynağı; bilgi tarihi Haziran'dan önce) yanlış")
    pj = int(np.searchsorted(gD, np.datetime64("2016-06-30"), side="right")) - 1
    if abs(I["Dk"]["PD"][pj, 9] - Dz["C"][pj, 9] * 1e7 * (1 + 9 % 3)) > 1e-3 or np.isfinite(I["Dk"]["PD"][pj + 1]).any():
        hata.append("5) ABD Haziran PD = kapanış x pay değil ya da Haziran / Aralık dışı gün dolu")
    H = K62.k62_hazirla(I["Dk"], E62, True); Pid = H["Pid"]
    r = Ua[(Ua.sembol == S[11]) & (Ua.yil == 2017) & (Ua.ceyrek == 2)].iloc[0]; t = int(np.searchsorted(gD, np.datetime64(pd.Timestamp(r.ann).date()), side="left")); j = 11
    pid = int(Pid[t, j]); uy = lambda k: [u for u in np.flatnonzero(Pid[t] == pid) if np.isfinite(Dz["A"][k, u])]  # noqa: E731
    rp = np.array([np.mean([Dz["A"][k, u] / Dz["A"][k - 1, u] - 1 for u in uy(k)]) for k in range(t - 1, t + 2)]); ri = Dz["A"][t - 1:t + 2, j] / Dz["A"][t - 2:t + 1, j] - 1
    if pid < 0 or abs(r.EAR - (np.prod(1 + ri) - np.prod(1 + rp))) > 1e-12 or pd.Timestamp(r.karar) != Dz["gun"][t + 1]:
        hata.append(f"5) ABD EAR elle (2x3 portföye göre [t-1, t+1]) aynı değil: {r.EAR}")
    if (Pid[:, 3] >= 0).any():
        hata.append("5) özkaynağı negatif ABD hissesi portföye girdi")
    Dz2 = copy.deepcopy(Dz); Dz2["gun"] = Dz["gun"][Dz["gun"] >= pd.Timestamp("2015-01-01")]; k0 = len(Dz["gun"]) - len(Dz2["gun"])
    for kk in ("C", "A"):
        Dz2[kk] = Dz[kk][k0:]
    U2, oz2 = B.k62b_abd_duyuru(Dz2, E)
    eski = U2[pd.to_datetime(U2.ann) < pd.Timestamp("2014-12-20")]
    if not len(eski) or eski.karar.notna().any() or eski.EAR.notna().any() or oz2["takvim_disi"] < len(eski):
        hata.append("5) fiyat takviminden önceki açıklamaya karar günü / EAR verildi")

    # 6) son açıklama ve 90 gün kuralı (elle kurulmuş tablo)
    tak = pd.bdate_range("2020-01-01", "2020-12-31")
    U = pd.DataFrame([{"sembol": "X", "yil": 2019, "ceyrek": 4, "ann": pd.Timestamp("2020-02-10"), "karar": pd.Timestamp("2020-02-12"), "SUETF": 1.0, "EAR": 0.1, "kirli": False},
                      {"sembol": "X", "yil": 2020, "ceyrek": 1, "ann": pd.Timestamp("2020-05-04"), "karar": pd.Timestamp("2020-05-06"), "SUETF": np.nan, "EAR": 0.2, "kirli": True},
                      {"sembol": "X", "yil": 2020, "ceyrek": 2, "ann": pd.Timestamp("2020-08-03"), "karar": pd.Timestamp("2020-08-05"), "SUETF": 3.0, "EAR": 0.3, "kirli": False},
                      {"sembol": "X", "yil": 2020, "ceyrek": 1, "ann": pd.Timestamp("2020-08-03"), "karar": pd.Timestamp("2020-08-05"), "SUETF": 9.0, "EAR": 0.9, "kirli": False},
                      {"sembol": "Y", "yil": 2019, "ceyrek": 4, "ann": pd.Timestamp("2020-03-02"), "karar": pd.NaT, "SUETF": 5.0, "EAR": 0.5, "kirli": False}])
    U["cs"] = False; U["cs_var"] = False; L = B.k62b_son_indeks(U, tak, ["X", "Y"]); Z = B.k62b_degiskenler(U, L, tak, E)
    gi = lambda s: int(tak.get_loc(pd.Timestamp(s)))  # noqa: E731
    beklenen = [("2020-02-12", np.nan, np.nan), ("2020-02-13", 1.0, 0.1), ("2020-05-06", 1.0, 0.1), ("2020-05-07", np.nan, 0.2), ("2020-05-08", np.nan, 0.2),
                ("2020-07-31", np.nan, 0.2), ("2020-08-03", np.nan, np.nan), ("2020-08-05", np.nan, np.nan), ("2020-08-06", 3.0, 0.3), ("2020-10-30", 3.0, 0.3),
                ("2020-11-02", np.nan, np.nan)]   # kirli son açıklamada eskiye gidilmez; 05-04 + 90 gün = 08-02 sınırı; aynı karar gününde geç dönem (Q2)
    for g_, su, ea in beklenen:
        v1, v2 = Z["SUETF_C"][gi(g_), 0], Z["EAR_C"][gi(g_), 0]
        if not (np.isnan(su) and np.isnan(v1) or abs(v1 - su) < 1e-6) or not (np.isnan(ea) and np.isnan(v2) or abs(v2 - ea) < 1e-6):
            hata.append(f"6) {g_}: SUETF_C / EAR_C = {v1} / {v2}, beklenen {su} / {ea}")
    if not Z["TAZE"][gi("2020-05-11"), 0] or not Z["KIRLI"][gi("2020-05-07"), 0] or Z["KIRLI"][gi("2020-05-06"), 0] or Z["TAZE"][gi("2020-11-03"), 0]:
        hata.append("6) taze / kirli bayrakları yanlış")
    if (L[:, 1] >= 0).any():
        hata.append("6) karar günü olmayan açıklama kullanıldı")
    if Z["YAS"][gi("2020-11-02"), 0] != (pd.Timestamp("2020-11-02") - pd.Timestamp("2020-08-03")).days:
        hata.append("6) YAS (takvim günü) yanlış")
    V = sentetik_fiyat([f"S{i:02d}" for i in range(36)]); Us = sentetik_duyuru(V)
    H = B.k62b_pazar_hazirla({"V": V, "duyuru": Us}, E)
    X0 = pd.DataFrame({"sembol": ["S01", "S02", "S03"], "sinyal": [H["takvim"][700], H["takvim"][1500], H["takvim"][20]], "bas": pd.NaT, "giris": H["takvim"][[701, 1501, 21]], "tekil": True})
    Xo = B._k62b_olay_tablosu(X0, H, "K24", E)
    for i, rr in Xo.iterrows():
        t_ = pd.Timestamp(rr.sinyal); u = Us[(Us.sembol == rr.sembol) & (pd.to_datetime(Us.karar) < t_)].sort_values(["karar", "yil", "ceyrek"])
        if not len(u):
            if not (rr.hic and rr.yok90 and np.isnan(rr.SUETF_C)):
                hata.append("6) açıklaması olmayan olayda hic / yok90 / değer yanlış")
            continue
        son = u.iloc[-1]; taze = (t_ - pd.Timestamp(son.ann)).days <= 90
        v = son.SUETF if taze else np.nan
        if rr.yok90 == taze or not ((np.isnan(v) and np.isnan(rr.SUETF_C)) or abs(rr.SUETF_C - np.float32(v)) < 1e-6) or rr.son_donem != f"{int(son.yil)}Q{int(son.ceyrek)}":
            hata.append(f"6) olayın son açıklaması / değeri elle hesapla aynı değil ({rr.sembol})")

    # 7) geleceğe bakma
    g = 1500; tg = H["takvim"][g]; Uf = Us.copy(); gel = pd.to_datetime(Uf.karar) >= tg; rng = np.random.default_rng(1)
    Uf.loc[gel, "SUETF"] = rng.normal(size=int(gel.sum())) * 50; Uf.loc[gel, "EAR"] = 7.0; Uf.loc[gel, "ann"] = pd.to_datetime(Uf.loc[gel, "ann"]) - pd.Timedelta(days=5)
    ek = Uf[gel].head(30).copy(); ek["karar"] = tg; ek["ann"] = tg - pd.Timedelta(days=1); Uf = pd.concat([Uf, ek], ignore_index=True)
    Hf = B.k62b_pazar_hazirla({"V": V, "duyuru": Uf}, E)
    for k in ("SUETF_C", "EAR_C"):
        if not np.allclose(H["X"][k][:g + 1], Hf["X"][k][:g + 1], equal_nan=True) or not np.allclose(H["sira"][k][:g + 1], Hf["sira"][k][:g + 1], equal_nan=True):
            hata.append(f"7) karar günü >= t olan açıklamalar bozulunca {k} / evren sırası t ve öncesinde değişti")
    if np.allclose(H["X"]["EAR_C"][g + 3:], Hf["X"]["EAR_C"][g + 3:], equal_nan=True):
        hata.append("7) sağlama: bozma t'den sonrasını değiştirmedi")
    gg = 900; tg2 = Dz["gun"][gg]; Dzf = copy.deepcopy(Dz); rng = np.random.default_rng(2)
    for kk in ("C", "A"):
        Dzf[kk][gg + 1:] *= rng.uniform(0.5, 2.0, Dzf[kk][gg + 1:].shape)
    Tf = Dzf["T"]; gelq = Tf["bilgi"] >= tg2.to_datetime64().astype("datetime64[D]"); Tf["Q"]["NetIncomeLoss"][gelq] *= -7; Tf["I"]["StockholdersEquity"][gelq] *= 3
    Tf["pay"] = [(d_, np.where(b_ >= tg2.to_datetime64().astype("datetime64[D]"), n_ * 5, n_), b_) for d_, n_, b_ in Tf["pay"]]
    Uf2, _ = B.k62b_abd_duyuru(Dzf, E)
    a = Ua[pd.to_datetime(Ua.karar) < tg2].set_index(["sembol", "yil", "ceyrek"]); b = Uf2.set_index(["sembol", "yil", "ceyrek"]).reindex(a.index)
    if not len(a) or not np.allclose(a.SUETF.to_numpy(float), b.SUETF.to_numpy(float), equal_nan=True, rtol=0, atol=1e-15) or not np.allclose(a.EAR.to_numpy(float), b.EAR.to_numpy(float), equal_nan=True, rtol=0, atol=1e-15):
        hata.append("7) ABD: g'den sonraki fiyat / pay / net kâr bozulunca karar günü < g olan açıklamaların SUETF / EAR'ı değişti")
    c = Ua[pd.to_datetime(Ua.karar) > tg2 + pd.Timedelta(days=200)].set_index(["sembol", "yil", "ceyrek"]); d = Uf2.set_index(["sembol", "yil", "ceyrek"]).reindex(c.index)
    if np.allclose(c.SUETF.to_numpy(float), d.SUETF.to_numpy(float), equal_nan=True):
        hata.append("7) sağlama: ABD bozması sonraki açıklamaları değiştirmedi")

    # 8) ÇÖL + SÜRPRİZ sınıfı
    Ub2 = Us.copy(); Ub2.loc[Ub2.yil == 2024, "kirli"] = True; Ub2.loc[Ub2.kirli, "SUETF"] = np.nan
    Cs = B.k62b_surpriz_sinif(Ub2, "BIST")
    X_ = Ub2[Ub2.karar.notna()].reset_index(drop=True)
    s1 = K62.k62_tertil_onsel(X_, "SUETF", E62, E62["bolum_b"]["tms29_haric"]); s2 = K62.k62_tertil_onsel(X_, "EAR", E62, None)
    if not (Cs.s_SUETF.to_numpy() == s1).all() or not (Cs.s_EAR.to_numpy() == s2).all() or not (Cs.cs == ((s1 == 2) & (s2 == 2))).all() or not Cs.cs.any():
        hata.append("8) ÇÖL + SÜRPRİZ sınıfı K62.k62_tertil_onsel ile aynı değil")
    if (Cs[Cs.yil == 2024].s_SUETF >= 0).any():
        hata.append("8) kirli çeyrekte SUETF sınıfı atandı")

    # 9) karar sırası seçim kuralı
    def Kk(u_s, a_s, u_e, a_e):
        return pd.DataFrame([{"tanim": "K24", "pazar": p, "donem": dn, "degisken": k, "n_ust": u, "n_alt": a_} for p in ("BIST", "ABD") for dn in E["bagimsiz"]
                             for k, u, a_ in (("SUETF_C", u_s, a_s), ("EAR_C", u_e, a_e))] + [{"tanim": "K24", "pazar": "ABD", "donem": "2023-2026", "degisken": "SUETF_C", "n_ust": 1, "n_alt": 500}])
    if B.k62b_sira_sec(Kk(100, 150, 100, 210), E)[0] != {"SUETF_C": "EVREN", "EAR_C": "IC"} or B.k62b_sira_sec(Kk(29, 40, 300, 300), E)[0] != {"SUETF_C": "IC", "EAR_C": "EVREN"}:
        hata.append("9) karar sırası seçim kuralı (oran < 0,5 ya da küçük grup < 30 -> İÇ; 2023-2026 hücresi kurala girmez) yanlış")

    # 10) kapsam sayım modu ve 11) uçtan uca koşu
    with tempfile.TemporaryDirectory() as td:
        try:
            Va = sentetik_fiyat([f"S{i:02d}" for i in range(36)], tohum=5); Vb = sentetik_fiyat([f"B{i:02d}" for i in range(36)], tohum=6)
            girdi = {"ABD": {"V": Va, "duyuru": B.k62b_surpriz_sinif(sentetik_duyuru(Va, 7), "ABD")}, "BIST": {"V": Vb, "duyuru": B.k62b_surpriz_sinif(sentetik_duyuru(Vb, 8, True), "BIST")}}
            cik = os.path.join(td, "c"); os.makedirs(cik)
            Kp = B.k62b_kapsam(cik, girdi, E)
            yasak = [c_ for c_ in Kp.columns if any(x in c_ for x in ("fark", "r60", "r20", "car", "getiri", "esli"))]
            if yasak or not len(Kp):
                hata.append(f"10) kapsam çıktısında getiri sütunu var / boş: {yasak}")
            Ho = B.k62b_pazar_hazirla(girdi["ABD"], E); O = K64.k64_olay_k24(Va, E); Xk = B._k62b_olay_tablosu(O, Ho, "K24", E)
            gi_ = Ho["takvim"].get_indexer(pd.DatetimeIndex(Xk.giris)); Xk["pencere"] = (gi_ >= 0) & (gi_ + 59 <= len(Ho["takvim"]) - 1)
            m_ = Xk.tekil & Xk.pencere & (Xk.giris >= "2022-01-01") & (Xk.giris <= "2026-12-31")
            r1 = Kp[(Kp.pazar == "ABD") & (Kp.donem == "2022-2026") & (Kp.degisken == "(olay)") & (Kp.tanim == "K24")].iloc[0]
            r2 = Kp[(Kp.pazar == "ABD") & (Kp.donem == "2022-2026") & (Kp.degisken == "EAR_C") & (Kp.tanim == "K24")].iloc[0]
            if int(r1.n_pencere) != int(m_.sum()) or int(r1.n_yok90) != int((m_ & Xk.yok90).sum()) or int(r2.n_ust_ic) != int((m_ & (Xk.EAR_C_ic >= 2 / 3)).sum()):
                hata.append("10) kapsam sayıları olay tablosuyla aynı değil")
            if int(Kp[(Kp.pazar == "BIST") & (Kp.degisken == "(olay)") & (Kp.donem == "2022-2026")].n_kirli.iloc[0]) == 0:
                hata.append("10) BIST kirli sayımı çalışmıyor")
            Ok = K60._k60_json_oku(B._k62b_yol("kapsam_ozet", cik))
            if (Ok.get("sira_secim") or {}).get("secim") is None:
                hata.append("10) kapsam özetinde karar sırası seçimi yok")
            sec = Ok["sira_secim"]["secim"]; Et = E_test(sec)
            _git(td, "init", "-q")
            try:
                B.k62b_kos(cik, girdi=girdi, E=Et); hata.append("3) ön kayıt yokken koşu durmadı")
            except B.K62BHata:
                pass
            y = B.k62b_onkayit(cik, {"V_ABD.pkl": ("c" * 64, 1)}, Et)
            try:
                B.k62b_kos(cik, girdi=girdi, E=Et); hata.append("3) git'e işlenmemiş ön kayıtla koşu durmadı")
            except B.K62BHata as ex:
                if "işlenmemiş" not in str(ex):
                    hata.append(f"3) beklenmeyen ret nedeni: {ex}")
            _git(td, "add", "-f", y); _git(td, "commit", "-q", "-m", "on kayit")
            Et2 = copy.deepcopy(Et); Et2["s1"]["tohum"] = 1
            try:
                B.k62b_kos(cik, girdi=girdi, E=Et2); hata.append("3) mührü farklı koşu durmadı")
            except B.K62BHata:
                pass
            R = B.k62b_kos(cik, girdi=girdi, E=Et)
            for ad in ("olay", "s1", "fark", "s2", "karar", "bilgi", "meta", "rapor"):
                if not os.path.exists(B._k62b_yol(ad, cik)):
                    hata.append(f"11) çıktı yok: {ad}")
            Kr = R["karar"]
            if len(Kr) != 4 or any(not (v.startswith("İZ DEĞİL") or v.startswith("ÖLÇÜLEMEZ") or "ADAY" in v) for v in Kr.karar) or any(v == "İZ" for v in Kr.karar):
                hata.append(f"11) karar tablosu beklenen biçimde değil: {Kr[['degisken', 'yon', 'karar']].to_dict('records') if len(Kr) else None}")
            Fk = R["fark"]; X = pd.read_csv(B._k62b_yol("olay", cik), parse_dates=["giris"])
            f0 = Fk[(Fk.tanim == "K24") & (Fk.pazar == "ABD") & (Fk.donem == "2022-2026") & (Fk.degisken == "EAR_C") & (Fk.sira_turu == "IC")].iloc[0]
            Xa = X[(X.pazar == "ABD") & (X.tanim == "K24") & (X.giris >= "2022-01-01") & X.fark.notna()]
            u_, a_ = Xa[Xa.EAR_C_ic >= 2 / 3].fark, Xa[Xa.EAR_C_ic <= 1 / 3].fark
            if int(f0.n_ust) != len(u_) or (len(u_) and len(a_) and abs(f0.nokta - (u_.mean() - a_.mean())) > 1e-9):
                hata.append("11) ÜST - ALT farkı olay dosyasından yeniden üretilemedi")
            Bi = R["bilgi"]; b0 = Bi[(Bi.pazar == "ABD") & (Bi.donem == "2022-2026") & (Bi.grup == "YOK90")].iloc[0]
            if int(b0.n) != int((Xa.yok90.astype(str).str.lower() == "true").sum()):
                hata.append("11) YOK90 bilgi grubunun n'i olay dosyasıyla aynı değil")
            once = open(B._k62b_yol("rapor", cik), "rb").read(); B.k62b_rapor(cik, Et)
            if open(B._k62b_yol("rapor", cik), "rb").read() != once:
                hata.append("11) `rapor` aynı raporu yeniden üretmedi")
            rap = once.decode("utf-8")
            for parca in ("## Karar tablosu", "## Temel model", "## SUETF_C", "## EAR_C", "Bilgi grupları"):
                if parca not in rap:
                    hata.append(f"11) raporda '{parca}' yok")
            open(y, "a", encoding="utf-8").write("\nsonradan eklenen kural\n")
            try:
                B.k62b_kos(cik, girdi=girdi, E=Et); hata.append("3) işlendikten sonra değişmiş ön kayıtla koşu durmadı")
            except B.K62BHata as ex:
                if "değişmiş" not in str(ex):
                    hata.append(f"3) beklenmeyen ret nedeni: {ex}")
            for f in os.listdir(cik):
                if f.endswith((".md", ".csv", ".json")) and B._K62B_EPOSTA.search(open(os.path.join(cik, f), encoding="utf-8").read()):
                    hata.append(f"12) sentetik çıktıda e-posta var: {f}")
        except (subprocess.SubprocessError, OSError) as ex:
            hata.append(f"3) git / dosya testi kurulamadı: {ex}")
        except Exception as ex:
            import traceback
            hata.append(f"11) uçtan uca sentetik koşu çöktü: {type(ex).__name__} {ex}\n{traceback.format_exc()[-2000:]}")

    # 12) e-posta / anahtar / SEC adresi yok
    for ad in ("K62B.py", "test_k62b.py"):
        s_ = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if [x for x in re.findall(r"[\w.+-]+@[\w-]+\.[A-Za-z]{2,}", s_) if not x.endswith("@invalid")] or ("sec" + ".gov") in s_.lower() \
                or re.search(r"(api[_-]?key|token|secret|password)\s*=\s*['\"][A-Za-z0-9]{12,}", s_, re.I):
            hata.append(f"12) {ad} içinde e-posta / anahtar / SEC adresi var")
    return hata


if __name__ == "__main__":
    Hh = testler()
    if Hh:
        print("K62-B TEST: HATA", len(Hh)); print("\n".join(Hh)); sys.exit(1)
    print("K62-B TEST: 12/12 bölüm GEÇTİ")
