"""K64 + K65 testleri (ağ gerekmez; yalnız SENTETİK veri, gerçek veride getiri ölçmez). Çalıştırma: python test_k64.py

1) çakışma kapısı (_CK_ONCE_K64)  2) ön kayıt mührü (üzerine yazmama, bozuk / farklı mühür reddi, eşik ya da değişken tanımı değişince mühür değişir; gerçek
K64_K65_ON_KAYIT.md varsa bugünkü eşiklerle aynı)  3) 60 gün tekilleştirme (elle) ve K24 olaylarının FI_K24 'tekrar' = 60 çıktısıyla birebirliği
4) K64 değişkenleri elle (Z52, D52, HIZ, DD252, DUSUS)  5) K65 değişkenleri: K60 sinyalleriyle ay sonunda birebir (GP_A, OP_BE, REV_YOY) + elle (FCF, BORC,
KAR_B, PAY_D)  6) BİLGİ TARİHİ kuralı ve BIST temel tablosu (kümülatif farkı, yatırım işareti, satış 0 kuralı, KAP ilk yayın günü, yedek kural, 'bilgi < t')
7) İş Yatırım önbelleği (sahte indirici; ağ yok)  8) GELECEĞE BAKMA YOK: t0'dan sonraki fiyat / temel veri / başvuru / pay bozulunca t0 ve öncesi olaylar,
değişkenler, sıralar aynı (K24 ve D13)  9) üçte bir kuralı (evren içi sıra elle, eşikler, çöl içi sıra elle + geleceğe bakmaz)  10) 'ek katkı' kuralı ve
ÜST - ALT bootstrap (elle nokta, tohumla birebir, ekilmiş fark)  11) eşli fark matrisi = fi_olcut_olay  12) karar kuralı (ADAY / İZ DEĞİL / ÖLÇÜLEMEZ / işaret /
BH)  13) kapsam modu getiri hesaplamaz  14) uçtan uca sentetik koşu (git'li): ön kayıt yokken / işlenmemişken / değişmişken `kos` reddeder; çıktılar ve rapor
15) e-posta / anahtar yok.
"""
from __future__ import annotations

import copy
import json
import os
import re
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K64 as K  # noqa: E402
import test_k60 as TK  # noqa: E402

FI, K60 = K.FI, K.K60
E0 = K.K64_ESIK


def sentetik_fiyat(S: list, bas: str = "2015-06-01", bit: str = "2026-08-31", tohum: int = 3) -> dict:
    """Oynak sentetik fiyatlar (K24 sinyali üretecek kadar): {sembol: OHLCV}. Hisse 2 geç başlar, hisse 4'te boş günler var."""
    rng = np.random.default_rng(tohum); gun = pd.bdate_range(bas, bit); G = len(gun); V = {}
    for j, s in enumerate(S):
        r = rng.normal(0.0003, 0.032, G) + 0.5 * rng.normal(0, 0.012, G)
        for k in rng.choice(G - 60, 6, replace=False):
            r[k:k + 25] -= 0.022
        c = rng.uniform(5, 60) * np.exp(np.cumsum(r)); o = c * np.exp(rng.normal(0, 0.006, G))
        h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.006, G))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.006, G)))
        d = pd.DataFrame({"Open": o, "High": h, "Low": l, "Close": c, "Volume": rng.integers(2e5, 2e6, G).astype(float)}, index=gun)
        if j == 2:
            d = d.iloc[400:]
        if j == 4:
            d = d.drop(d.index[rng.choice(len(d), 30, replace=False)])
        V[s] = d
    return V


def fiyat_boz(V: dict, t0: pd.Timestamp, tohum: int = 5) -> dict:
    """t0'dan SONRAKİ barları bozar (fiyat yolu ve hacim); t0 ve öncesi aynen."""
    rng = np.random.default_rng(tohum); out = {}
    for s, d in V.items():
        d = d.copy(); m = np.asarray(d.index > t0); n = int(m.sum())
        if n:
            yol = np.exp(np.cumsum(rng.normal(0, 0.06, n))) * rng.uniform(0.4, 2.5)
            for c in ("Open", "High", "Low", "Close"):
                d.loc[m, c] = d.loc[m, c].to_numpy() * yol
            d.loc[m, "Volume"] = d.loc[m, "Volume"].to_numpy() * rng.uniform(0.05, 6.0, n)
        out[s] = d
    return out


def esit(a, b, rtol: float = 0.0) -> bool:
    return TK.esit(np.asarray(a, float), np.asarray(b, float), rtol)


def durmali(f, ad: str, hata: list, tur=None) -> None:
    try:
        f(); hata.append(ad)
    except (tur or K.K64Hata):
        pass


def testler() -> list:
    hata = []; nan = np.nan
    # 1) çakışma kapısı
    src = open(os.path.join(KOK, "K64.py"), encoding="utf-8").read().replace("from __future__ import annotations\n", "")
    g = {"__name__": "kapi_test", "k64_kos": object(), "_CK_KAYIT": {"k64_kos": "BASKA.py"}}
    try:
        exec(compile(src, "K64.py", "exec"), g); hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "kapi_test2"}
    try:
        exec(compile(src, "K64.py", "exec"), g2); exec(compile(src, "K64.py", "exec"), g2)
    except Exception as ex:
        hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
    if "_CK_ONCE_K64 = " not in src or "_cakisma_kontrol_k64()" not in src:
        hata.append("1) çakışma kapısı adı _CK_ONCE_K64 değil")
    # 2) ön kayıt mührü
    if K.k64_kodlar() != ["Z52", "D52", "HIZ", "DUSUS", "GP", "OP", "FCF", "BORC", "SATIS_B", "KAR_B", "PAY_D"] or K.k64_kodlar(aile="K64") != ["Z52", "D52", "HIZ", "DUSUS"]:
        hata.append("2) değişken listesi iş tanımındaki gibi değil")
    if not (E0["kriz"] == "2026-08-31" and [d[0] for d in E0["donem"]] == ["2017-2021", "2022-2026", "2023-2026"] and E0["bagimsiz"] == ["2017-2021", "2022-2026"]
            and E0["olay"]["tekil_gun"] == 60 and E0["olay"]["ana"] == "K24" and E0["maliyet"] == {"BIST": 0.0060, "ABD": 0.0020} and E0["coklu"]["bh_q"] == 0.10
            and abs(E0["sira"]["ust"] - 2 / 3) < 1e-12 and abs(E0["sira"]["alt"] - 1 / 3) < 1e-12 and E0["s1"]["n_esik"] == 30 and E0["k64"]["pencere"] == 252
            and E0["k64"]["hiz_gun"] == 20 and E0["k65"]["pay"] == {"ABD": True, "BIST": False} and E0["sira"]["karar"] == {"K64": "IC", "K65": "EVREN"}):
        hata.append("2) K64_ESIK sabitleri iş tanımındaki gibi değil")
    if FI.FI_OLCUT["ufuk"] != 60 or FI.FI_OLCUT["n_esik"] != 30 or FI.FI_K24["tekrar"] != 60:
        hata.append("2) FI_OLCUT / FI_K24 beklenen değerlerde değil")
    if [K.k64_karar_sirasi(k) for k in K.k64_kodlar()] != ["IC"] * 4 + ["EVREN"] * 7:
        hata.append("2) karar sırası aile bazında değil (K64 ailesi İÇ, K65 ailesi EVREN olmalı)")
    durmali(lambda: K.k64_karar_sirasi("YOK"), "2) tanımsız değişkenin karar sırası verildi", hata)
    E5 = copy.deepcopy(E0); E5["sira"]["karar"]["K64"] = "EVREN"
    if K.k64_esik_sha(E5) == K.k64_esik_sha() or K.k64_karar_sirasi("Z52", E5) != "EVREN":
        hata.append("2) karar sırası değişince mühür değişmiyor")
    E2 = copy.deepcopy(E0); E2["coklu"]["bh_q"] = 0.2
    E3 = copy.deepcopy(E0); E3["degisken"][0]["tanim"] += " "
    E4 = copy.deepcopy(E0); E4["donem"][0][1] = "2016-01-01"
    if len({K.k64_esik_sha(), K.k64_esik_sha(E2), K.k64_esik_sha(E3), K.k64_esik_sha(E4)}) != 4 or K.k64_esik_sha() != K.k64_esik_sha(copy.deepcopy(E0)):
        hata.append("2) eşik / tanım / dönem değişince mühür değişmiyor ya da aynı eşikte mühür farklı")
    vs = {"V_BIST.pkl": ("a" * 64, 1), "V_ABD.pkl": ("b" * 64, 1)}
    with tempfile.TemporaryDirectory() as td:
        y = K.k64_onkayit(td, veri_sha=vs); ilk = open(y, encoding="utf-8").read()
        if f"ESIK_SHA256: {K.k64_esik_sha()}" not in ilk or not re.search(r"^Yazım zamanı: \d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC", ilk, re.M):
            hata.append("2) ön kayıtta mühür / UTC zaman yok")
        for parca in ("## Veri", "## 0. Soru", "## 1. Olay", "## 2. Evren", "## 3. Değişkenler", "## 4. S1", "## 5. S2", "## 6. Cetvel", "## 7. Hücreler", "## 8. Çoklu test",
                      "## 9. GÜÇ BEYANI", "## 10. Yanlılık beyanı", "## 11. SAPMA / BOŞLUK", "## 12. Kapsam", "## 13. Çıktılar", "## 14. Değişmezlik", "EK KATKI VAR", "ÖLÇÜLEMEZ",
                      "ABD-ADAY", "BIST VERİSİ YOK", "YAŞAYAN YANLILIĞI", "Benjamini-Hochberg", "python -I K64.py kos", "2017-2021", "2022-2026", "2023-2026", "fi_k24_tara",
                      "COL_v1.col_olc", "KARAR SIRASI (aile bazında", "kapsam sayımı görüldü, getiri görülmedi", "SAPMA 15.") + tuple(f"BOŞLUK {i}." for i in range(1, 15)) + tuple(f"| {k} | " for k in K.k64_kodlar()):
            if parca not in ilk:
                hata.append(f"2) ön kayıtta '{parca}' yok")
        if K._k64_onkayit_oku(y)["veri"] != vs:
            hata.append("2) ön kayıttan veri sha256'ları okunamadı")
        K.k64_onkayit(td)
        if open(y, encoding="utf-8").read() != ilk:
            hata.append("2) ön kayıt üzerine yazıldı")
        if K.k64_onkayit_dogrula(td)["sha"] != K.k64_esik_sha():
            hata.append("2) doğrulama mührü yanlış")
        durmali(lambda: K.k64_onkayit_dogrula(td, git=True), "2) git'e işlenmemiş ön kayıt kabul edildi", hata)
        open(y, "w", encoding="utf-8").write(ilk.replace(K.k64_esik_sha(), "0" * 64))
        durmali(lambda: K.k64_onkayit_dogrula(td), "2) bozuk mühür kabul edildi", hata)
        durmali(lambda: K.k64_onkayit(td), "2) mührü farklı ön kayıt sessizce kabul edildi", hata)
    gercek = K._k64_yol("onkayit")
    if os.path.exists(gercek):
        try:
            oc = K.k64_onkayit_dogrula()
            if not oc["zaman_utc"] or len(oc["veri"]) < 8:
                hata.append(f"2) gerçek ön kayıtta UTC zaman / veri sha256 eksik ({len(oc['veri'])} kaynak)")
        except K.K64Hata as ex:
            hata.append(f"2) gerçek ön kayıt bugünkü eşiklerle tutmuyor: {ex}")
    # 3) tekilleştirme + K24 olayları
    if K.k64_tekil(np.array([10, 40, 69, 70, 100, 129, 131, 300]), 60).tolist() != [True, False, False, True, False, False, True, True]:
        hata.append("3) 60 gün tekilleştirme elle hesapla aynı değil")
    D = TK.sentetik_demet(N=70, tohum=4); S = list(D["sembol"]); V = sentetik_fiyat(S)
    O = K.k64_olay_k24(V)
    if len(O) < 40 or O.attrs.get("sapma", 1) != 0:
        hata.append(f"3) sentetik K24 olayı az ({len(O)}) ya da tekil olaylar FI_K24 tekrar = 60 ile aynı değil (sapma {O.attrs.get('sapma')})")
    for s, gq in O.groupby("sembol"):
        d = V[s]; pos = d.index.get_indexer(pd.DatetimeIndex(gq.sinyal)); tk = gq.tekil.to_numpy(bool)
        if (np.diff(pos[tk]) < 60).any() or tk.tolist() != K.k64_tekil(pos, 60).tolist():
            hata.append(f"3) {s}: tekil olaylar arasında 60 işlem gününden az var"); break
        Y = FI.fi_k24_tara(d)
        if set(pd.DatetimeIndex(Y.loc[Y.kural, "tarih"])) != set(gq.sinyal[tk]):
            hata.append(f"3) {s}: tekil K24 olayları fi_k24_tara çıktısıyla aynı değil"); break
        if any(d.index[p - 14] != b for p, b in zip(pos, gq.bas)) or any((d.index[p + 1] != g) if p + 1 < len(d) else pd.notna(g) for p, g in zip(pos, gq.giris)):
            hata.append(f"3) {s}: çöl başlangıcı / giriş günü yanlış"); break
    if {"yon60", "yon20", "r120"} & set(O.columns):
        hata.append("3) olay tablosunda ileriye bakan sonuç sütunu var")
    # 4) K64 değişkenleri elle
    rng = np.random.default_rng(11); c = 20 * np.exp(np.cumsum(rng.normal(0, 0.03, 600))); X = K.k64_fiyat_olculeri(c)
    for t in (199, 251, 300, 599):
        a = max(0, t - 251); z = c[t] / c[a:t + 1].max(); dd = c[t] / c[a:t + 1].min()
        if not (np.isclose(X["Z52"][t], z) and np.isclose(X["D52"][t], dd)):
            hata.append(f"4) Z52 / D52 elle hesapla aynı değil (t = {t})")
        za = c[t - 20] / c[max(0, t - 20 - 251):t - 19].max() if t - 20 >= 199 else nan
        if not (np.isclose(X["HIZ"][t], z - za) if np.isfinite(za) else np.isnan(X["HIZ"][t])):
            hata.append(f"4) HIZ elle hesapla aynı değil (t = {t})")
        if t >= 252 + 14:
            b = t - 14; ds = c[b] / c[b - 252:b].max() - 1
            if not (np.isclose(X["DUSUS"][t], ds) and np.isclose(X["DD252"][b], ds)):
                hata.append(f"4) DUSUS / DD252 elle hesapla aynı değil (t = {t})")
    if np.isfinite(X["Z52"][:199]).any() or not np.isfinite(X["Z52"][199]):
        hata.append("4) en az 200 gözlem kuralı tutmuyor")
    M = K.k64_fiyat_matrisleri(V); tak = M["takvim"]; j2 = M["sembol"].index(S[2]); p2 = tak.get_indexer(V[S[2]].index)
    if not esit(M["Z52"][p2, j2], K.k64_fiyat_olculeri(V[S[2]].Close.to_numpy())["Z52"].astype(np.float32)) or M["var"][:p2[0], j2].any():
        hata.append("4) fiyat matrisi hissenin kendi işlem günlerine oturmuyor")
    # 5) K65: K60 ile ay sonunda birebir + elle
    Ek = TK.test_esik(); P = K60.k60_panel(D, Ek, False); Sd, ek = K60.k60_sinyaller(D, P, Ek); N = len(S); T = D["temel"]
    Kl = K.k64_kalite(T, P["mtD"], N, "ABD", {"bolunme": D["bolunme"], "sembol": S})
    for a, b in (("GP", Sd["GP_A"]), ("OP", Sd["OP_BE"]), ("SATIS_B", ek["bilesen"]["REV_YOY"])):
        m = np.isfinite(b)
        if m.sum() < 500 or not np.allclose(Kl[a][m], b[m], rtol=2e-5, atol=1e-7):
            hata.append(f"5) {a} ay sonunda K60 sinyaliyle aynı değil (dolu hücre {int(m.sum())})")
    t = np.datetime64("2019-05-20"); Kg = K.k64_kalite(T, np.array([t], "datetime64[D]"), N, "ABD", {"bolunme": D["bolunme"], "sembol": S})
    for j in (0, 2, 9, 20):
        q0 = TK.elle_q0(T, t, j); y0 = max([y for y in range(T["Ybilgi"].shape[0]) if T["Ybilgi"][y, j] < t], default=-1)
        if q0 < 4 or y0 < 0:
            continue
        at = T["I"]["Assets"][q0, j]; eq = T["I"]["StockholdersEquity"][q0, j]; ni = T["Q"]["NetIncomeLoss"]
        el = {"BORC": T["I"]["Liabilities"][q0, j] / at, "KAR_B": (ni[q0 - 3:q0 + 1, j].sum() - ni[q0 - 7:q0 - 3, j].sum()) / T["I"]["Assets"][q0 - 4, j],
              "FCF": (T["Y"]["NetCashProvidedByUsedInOperatingActivities"][y0, j] - T["Y"]["PaymentsToAcquirePropertyPlantAndEquipment"][y0, j]) / T["I"]["Assets"][T["Yq"][y0, j], j],
              "GP": T["Q"]["GrossProfit"][q0 - 3:q0 + 1, j].sum() / at, "OP": T["Q"]["OperatingIncomeLoss"][q0 - 3:q0 + 1, j].sum() / eq if eq > 0 else nan}
        for k, v in el.items():
            if not (np.isclose(Kg[k][0, j], v, rtol=2e-5) if np.isfinite(v) else np.isnan(Kg[k][0, j])):
                hata.append(f"5) {k} elle hesapla aynı değil (hisse {j}: {Kg[k][0, j]} != {v})")
    def elle_pay(j: int, gun: np.datetime64) -> float:
        kd, kn, kb = T["pay"][j]; m = kb < gun
        return float(kn[m][np.argmax(kd[m])])
    el = np.log(elle_pay(2, t) / elle_pay(2, t - np.timedelta64(365, "D")))
    if not (np.isclose(Kg["PAY_D"][0, 2], el, rtol=1e-5) and 0.05 < el < 0.11 and np.isclose(Kg["PAY_D"][0, 1], 0.0, atol=1e-6) and abs(Kg["PAY_D"][0, 6]) < 0.15):
        hata.append(f"5) PAY_D beklenen değerde değil ({Kg['PAY_D'][0, [1, 2, 6]]}, elle {el})")
    if np.isfinite(K.k64_kalite(T, np.array([t], "datetime64[D]"), N, "BIST", None)["PAY_D"]).any():
        hata.append("5) BIST'te PAY_D hesaplandı (VERİ YOK olmalıydı)")
    # 6) BIST temel tablosu + bilgi tarihi kuralı
    def donem(a, ozk, sat, brut, faal, net, ocf, cap):
        return {"Assets": a, "StockholdersEquity": ozk, "Revenues": sat, "GrossProfit": brut, "OperatingIncomeLoss": faal, "NetIncomeLoss": net,
                "NetCashProvidedByUsedInOperatingActivities": ocf, "PaymentsToAcquirePropertyPlantAndEquipment": cap}
    ham = {"AAA": {}, "BBB": {}}
    for y in (2018, 2019, 2020):
        for i, p in enumerate((3, 6, 9, 12), 1):
            k = (y - 2018) * 4 + i
            ham["AAA"][(y, p)] = donem(1000.0 + 10 * k, 400.0 + k, 100.0 * i + y - 2018, 30.0 * i, 12.0 * i, 8.0 * i + k, 20.0 * i, 5.0 * i)
    ham["BBB"][(2019, 12)] = donem(500.0, -20.0, nan, nan, 5.0, 3.0, nan, nan)
    kap = {("AAA", 2019, 4): np.datetime64("2020-03-05"), ("AAA", 2020, 1): np.datetime64("2020-05-08"), ("AAA", 2019, 3): np.datetime64("2019-10-01")}
    Tb = K.k64_bist_temel(["AAA", "BBB"], ham, kap); B = E0["bist"]; qb = lambda y, p: (y - B["yil_bas"]) * 4 + p // 3 - 1  # noqa: E731
    if not (Tb["Q"]["Revenues"][qb(2019, 6), 0] == 100.0 and Tb["Q"]["Revenues"][qb(2019, 3), 0] == 101.0 and Tb["Q"]["NetIncomeLoss"][qb(2019, 12), 0] == 8.0 + 1
            and Tb["Y"]["Revenues"][2019 - B["yil_bas"], 0] == 401.0 and Tb["I"]["Assets"][qb(2019, 12), 0] == 1080.0):
        hata.append("6) BIST kümülatif farkı / yıllık / anlık değerler yanlış")
    if not (Tb["bilgi"][qb(2019, 12), 0] == np.datetime64("2020-03-05") and Tb["bilgi_kaynak"][qb(2019, 12), 0] == 1
            and Tb["bilgi"][qb(2019, 6), 0] == np.datetime64("2019-06-30") + np.timedelta64(B["yedek_ara_gun"], "D") and Tb["bilgi_kaynak"][qb(2019, 6), 0] == 2
            and Tb["bilgi"][qb(2019, 9), 0] == np.datetime64("2019-09-30") + np.timedelta64(B["yedek_ara_gun"], "D")      # KAP günü dönem sonuna 5 günden yakın: yedek
            and Tb["bilgi"][qb(2018, 12), 0] == np.datetime64("2018-12-31") + np.timedelta64(B["yedek_yil_gun"], "D") and Tb["Ybilgi"][2019 - B["yil_bas"], 0] == np.datetime64("2020-03-05")):
        hata.append("6) BIST bilgi tarihi (KAP ilk yayın / yedek kural) yanlış")
    gun = np.array(["2020-03-05", "2020-03-06", "2020-05-08", "2020-05-11"], "datetime64[D]"); Kb = K.k64_kalite(Tb, gun, 2, "BIST", None)
    gp_q3 = (30.0 + 30 + 30 + 30) / 1070.0; gp_q4 = 120.0 / 1080.0; fcf_q4 = (80.0 - 20.0) / 1080.0
    if not (np.isclose(Kb["GP"][0, 0], gp_q3) and np.isclose(Kb["GP"][1, 0], gp_q4) and np.isclose(Kb["FCF"][1, 0], fcf_q4) and np.isclose(Kb["BORC"][1, 0], (1080.0 - 408.0) / 1080.0)
            and np.isclose(Kb["SATIS_B"][1, 0], 100.0 / 100.0 - 1) and np.isclose(Kb["KAR_B"][1, 0], 4.0 / 1040.0)
            and np.isclose(Kb["GP"][2, 0], gp_q4) and not np.isclose(Kb["GP"][3, 0], gp_q4)):
        hata.append(f"6) 'bilgi tarihi < t' kuralı / BIST K65 elle hesabı tutmuyor ({Kb['GP'][:, 0]}, {Kb['FCF'][:, 0]}, {Kb['KAR_B'][:, 0]})")
    if np.isfinite(Kb["GP"][:, 1]).any() or np.isfinite(Kb["OP"][:, 1]).any() or np.isfinite(Kb["FCF"][:, 1]).any():
        hata.append("6) satışı olmayan / özkaynağı eksi şirkette GP / OP / FCF hesaplandı")
    # 7) İş Yatırım önbelleği (sahte indirici)
    with tempfile.TemporaryDirectory() as td:
        cagri = []

        def sahte(s, y, grup):
            cagri.append((s, y)); deger = [] if s == "BNK" else [
                {"itemCode": "1BL", "value1": "1000", "value2": "900", "value3": None, "value4": "800"}, {"itemCode": "2N", "value1": "400", "value2": "390", "value3": None, "value4": "380"},
                {"itemCode": "3C", "value1": "0" if y == 2015 else "500", "value2": "300", "value3": None, "value4": "100"}, {"itemCode": "3D", "value1": "50", "value2": "30", "value3": None, "value4": "10"},
                {"itemCode": "4CAI", "value1": "-40", "value2": "-30", "value3": None, "value4": "-10"}]
            return json.dumps({"ok": True, "value": deger}).encode()
        Et = copy.deepcopy(E0); Et["bist"].update({"yil_bas": 2014, "yil_son": 2015, "bekle": 0.0, "isci": 2})
        r1 = K.k64_isy_indir(["XYZ", "BNK"], td, sahte, Et); r2 = K.k64_isy_indir(["XYZ", "BNK"], td, sahte, Et)
        if r1 != {"is": 4, "yeni": 4, "vardi": 0, "hata": 0} or r2["yeni"] != 0 or r2["vardi"] != 4 or len(cagri) != 4:
            hata.append(f"7) İş Yatırım önbelleği yeniden indirdi ya da sayım yanlış ({r1}, {r2})")
        hm, oz = K.k64_isy_oku(["XYZ", "BNK"], td, Et)
        if not (set(hm["XYZ"]) == {(2014, 12), (2014, 9), (2014, 3), (2015, 12), (2015, 9), (2015, 3)} and hm["XYZ"][(2014, 12)]["PaymentsToAcquirePropertyPlantAndEquipment"] == 40.0
                and np.isnan(hm["XYZ"][(2015, 12)]["Revenues"]) and np.isnan(hm["XYZ"][(2015, 12)]["GrossProfit"]) and hm["XYZ"][(2014, 12)]["GrossProfit"] == 50.0
                and hm["BNK"] == {} and oz["bos_hisse"] == ["BNK"] and oz["dosya"] == 4 and len(oz["icerik_sha256"]) == 64):
            hata.append("7) İş Yatırım okuyucu: dönemler / yatırım işareti / satış 0 kuralı / boş hisse yanlış")
        os.remove(os.path.join(td, "XYZ_2015.json"))
        durmali(lambda: K.k64_isy_oku(["XYZ", "BNK"], td, Et), "7) eksik İş Yatırım dosyasıyla okuma durmadı", hata)
    with tempfile.TemporaryDirectory() as td:
        yk = os.path.join(td, "l.csv.gz")
        pd.DataFrame({"yayin": ["05.03.2020 18:20:00", "01.03.2020 09:00:00", "x"], "kod": ["AAA, AAB", "AAA", "AAA"], "yil": [2019, 2019, 2019], "donem": [4, 4, 4]}).to_csv(yk, index=False)
        kp = K.k64_kap_bilgi([yk])
        if kp != {("AAA", 2019, 4): np.datetime64("2020-03-01"), ("AAB", 2019, 4): np.datetime64("2020-03-05")}:
            hata.append(f"7) KAP ilk yayın günü eşlemesi yanlış ({kp})")
    # 8) GELECEĞE BAKMA YOK
    t0 = pd.Timestamp("2021-06-30"); Vb = fiyat_boz(V, t0); Db = TK.boz(D, t0); pay = {"bolunme": D["bolunme"], "sembol": S}
    H1 = K.k64_pazar_hazirla("ABD", V, D["temel"], pay); H2 = K.k64_pazar_hazirla("ABD", Vb, Db["temel"], {"bolunme": Db["bolunme"], "sembol": S})
    son = int(np.searchsorted(H1["takvim"].to_numpy(), t0.to_datetime64(), side="right"))
    if not H1["takvim"][:son].equals(H2["takvim"][:son]):
        hata.append("8) takvim t0 öncesinde değişti")
    for k in list(K.k64_kodlar()) + ["DD252"]:
        if not esit(H1["X"][k][:son], H2["X"][k][:son]) or not esit(H1["sira"][k][:son], H2["sira"][k][:son]):
            hata.append(f"8) GELECEĞE BAKMA: {k} değeri / sırası t0 sonrası bozulunca t0 ve öncesinde değişti")
        if esit(H1["X"][k][son:], H2["X"][k][son:]) and np.isfinite(H1["X"][k][son:]).any():
            hata.append(f"8) bozma etkisiz: {k} t0 sonrasında da aynı (test bir şey sınamıyor)")
    if not esit(H1["rejim"][:son], H2["rejim"][:son]):
        hata.append("8) GELECEĞE BAKMA: piyasa koşulu t0 öncesinde değişti")
    Ob = K.k64_olay_k24(Vb); a = O[O.sinyal <= t0].reset_index(drop=True); b = Ob[Ob.sinyal <= t0].reset_index(drop=True)
    a2, b2 = a[a.sinyal < t0], b[b.sinyal < t0]
    if len(a) < 20 or not a[["sembol", "sinyal", "bas", "tekil"]].equals(b[["sembol", "sinyal", "bas", "tekil"]]) or not a2.giris.equals(b2.giris):
        hata.append("8) GELECEĞE BAKMA: K24 olayları t0 sonrası fiyat bozulunca değişti")
    Xa = K.k64_olay_degerleri(a, H1, "K24"); Xb = K.k64_olay_degerleri(b, H2, "K24")
    for k in K.k64_kodlar():
        if not (esit(Xa[k], Xb[k]) and esit(Xa[k + "_sira"], Xb[k + "_sira"]) and esit(Xa[k + "_ic"], Xb[k + "_ic"])):
            hata.append(f"8) GELECEĞE BAKMA: olay değeri / sırası değişti ({k})")
    if not (Xa.Z52_sira.notna().sum() > 20 and Xa.GP_sira.notna().sum() > 10 and Xa.Z52_ic.notna().sum() > 5):
        hata.append("8) olay değerleri boş (test bir şey sınamıyor)")
    Ed = copy.deepcopy(E0); Ed["olay"]["d13"].update({"isci": 1, "gecer": False}); Vk = {s: V[s] for s in S[:6]}; Vkb = {s: Vb[s] for s in S[:6]}
    d1 = K.k64_olay_d13(Vk, Ed); d2 = K.k64_olay_d13(Vkb, Ed); a = d1[d1.sinyal <= t0].reset_index(drop=True); b = d2[d2.sinyal <= t0].reset_index(drop=True)
    if not a[["sembol", "sinyal", "bas", "gecer", "tekil"]].equals(b[["sembol", "sinyal", "bas", "gecer", "tekil"]]):
        hata.append("8) GELECEĞE BAKMA: D13 olayları t0 sonrası fiyat bozulunca değişti")
    if len(d1):
        CV = K._k64_colv1(); r = d1.iloc[0]; d = Vk[r.sembol]; j = d.index.get_loc(r.sinyal)
        if not any((o := CV.col_olc(d.iloc[:e + 1])) and d.Close.iloc[j] > o["tavan"] * CV.AL_PAY for e in range(max(j - 60, 300), j)):
            hata.append("8) D13 olay gününde üretim AL kırılımı yok")
        for s, gq in d1[d1.tekil].groupby("sembol"):
            if (np.diff(Vk[s].index.get_indexer(pd.DatetimeIndex(gq.sinyal))) < 60).any():
                hata.append("8) D13 tekil olayları arasında 60 işlem gününden az var")
    # 9) üçte bir kuralı
    Xm = np.array([[1.0, 2.0, 2.0, 5.0, nan, 7.0], [3.0, nan, nan, nan, nan, 1.0]]); vr = np.ones((2, 6), bool); vr[0, 5] = False
    Sr = K.k64_sira(Xm, vr, 3)
    if not (esit(Sr[0], [0.125, 0.5, 0.5, 0.875, nan, nan]) and np.isnan(Sr[1]).all()):
        hata.append(f"9) evren içi sıra elle hesapla aynı değil ({Sr})")
    if K.k64_grup([2 / 3, 0.66, 1 / 3, 0.34, nan, 1.0, 0.0]).tolist() != ["UST", "ORTA", "ALT", "ORTA", "", "UST", "ALT"]:
        hata.append("9) üçte bir eşikleri (>= 2/3 ÜST, <= 1/3 ALT) tutmuyor")
    gg = np.array(["2020-01-10", "2020-01-10", "2020-03-01", "2020-06-01", "2021-03-05", "2021-03-06"], "datetime64[D]"); xx = np.array([1.0, 3.0, 2.0, nan, 0.5, 9.0])
    ic = K.k64_ic_sira(gg, xx, 365, 3); ic2 = K.k64_ic_sira(gg[:3], xx[:3], 365, 3)
    if not (np.isnan(ic[0]) and np.isnan(ic[1]) and np.isclose(ic[2], 0.5) and np.isnan(ic[3]) and np.isnan(ic[4]) and np.isnan(ic[5]) and esit(ic[:3], ic2)):
        hata.append(f"9) çöl içi sıra elle hesapla aynı değil / geleceğe bakıyor ({ic})")
    ic3 = K.k64_ic_sira(gg, xx, 420, 3)
    if not np.isclose(ic3[4], 0.5 / 4) or not np.isclose(ic3[5], 2.5 / 3):
        hata.append(f"9) çöl içi sıra pencere kuralı yanlış ({ic3})")
    # 10) ek katkı kuralı + ÜST - ALT
    ekk = K.k64_ek_katki
    if not (ekk(40, 35, 0.05, 0.01, 0.02, 0.005, 0.07, 30) == {"olculebilir": True, "UST": True, "ALT": False}
            and ekk(40, 35, 0.05, 0.01, 0.06, 0.005, 0.07, 30)["UST"] is False                       # ÜST temelden büyük değil
            and ekk(40, 35, 0.05, 0.01, 0.02, -0.001, 0.07, 30)["UST"] is False                      # alt sınır > 0 değil
            and ekk(40, 35, 0.01, 0.05, 0.02, -0.07, -0.005, 30) == {"olculebilir": True, "UST": False, "ALT": True}
            and ekk(29, 35, 0.05, 0.01, 0.02, 0.005, 0.07, 30) == {"olculebilir": False, "UST": False, "ALT": False}
            and ekk(40, 35, 0.05, 0.01, 0.02, nan, nan, 30)["olculebilir"] is False):
        hata.append("10) 'ek katkı' kuralı doğruluk tablosu tutmuyor")
    rng = np.random.default_rng(2); ayl = np.array([f"2019-{m:02d}" for m in range(1, 13)]); au = rng.choice(ayl, 300); aa = rng.choice(ayl, 280)
    fu = rng.normal(0.06, 0.2, 300); fa = rng.normal(0.0, 0.2, 280)
    f1 = K.k64_grup_farki(fu, au, fa, aa, 2000, 64001, [2.5, 97.5]); f2 = K.k64_grup_farki(fu, au, fa, aa, 2000, 64001, [2.5, 97.5]); f3 = K.k64_grup_farki(fa, aa, fu, au, 2000, 64001, [2.5, 97.5])
    if not (np.isclose(f1["nokta"], fu.mean() - fa.mean()) and f1 == f2 and f1["alt"] < f1["nokta"] < f1["ust"] and f1["alt"] > 0 and f1["p_ust"] < 0.01 and f1["p_alt"] > 0.99
            and np.isclose(f3["nokta"], -f1["nokta"]) and f3["ust"] < 0 and f1["gecerli"] == 2000):
        hata.append(f"10) ÜST - ALT bootstrap: nokta / tohum / ekilmiş fark tutmuyor ({f1})")
    f4 = K.k64_grup_farki(fu[:5], np.array(["2019-01"] * 5), fa[:5], np.array(["2019-02"] * 5), 500, 1, [2.5, 97.5])
    if np.isfinite(f4["alt"]) or f4["gecerli"] >= 450:
        hata.append("10) iki grubu da dolu çekiliş payı düşükken aralık verildi")
    if K.k64_grup_farki(np.array([]), np.array([]), fa, aa, 100, 1, [2.5, 97.5])["gecerli"] != 0:
        hata.append("10) boş grupla fark hesaplandı")
    # 11) eşli fark matrisi = fi_olcut_olay; hücre ölçüleri
    P = FI.fi_olcut_panel(V); P20 = FI.fi_olcut_panel(V, {**FI.FI_OLCUT, "ufuk": 20}); F = K.k64_fark_matris(P); rng = np.random.default_rng(3)
    dd = rng.integers(100, len(P["tarih"]) - 100, 300); jj = rng.integers(0, len(P["sembol"]), 300)
    Q = FI.fi_olcut_olay(P, pd.DataFrame({"sembol": [P["sembol"][j] for j in jj], "giris": P["tarih"][dd]}))
    if not esit(Q.fark.to_numpy(), F[dd, jj], rtol=1e-9) or Q.fark.notna().sum() < 200:
        hata.append("11) eşli fark matrisi fi_olcut_olay ile aynı değil")
    Xo = O[O.tekil & O.giris.notna()].reset_index(drop=True); Xo = K.k64_olc(P, P20, Xo)
    k = Xo[~Xo.sembol.isin([S[2], S[4]])].dropna(subset=["fark"]).iloc[0]; d = V[k.sembol]; i = d.index.get_loc(k.giris)
    if not (np.isclose(k.r60, d.Close.iloc[i + 59] / d.Open.iloc[i] - 1) and np.isclose(k.r20, d.Close.iloc[i + 19] / d.Open.iloc[i] - 1)):
        hata.append("11) r60 / r20 giriş açılışından 60. / 20. gün kapanışına değil")
    h = K.k64_hucre(Xo, 0.002); h0 = FI.fi_olcut_hucre(Xo)
    if not (h["n"] == h0["n"] and h["ort_fark"] == h0["ort_fark"] and h["alt95"] == h0["alt95"] and h["portfoy"] == h0["portfoy"] and np.isclose(h["ort_fark_net"], h["ort_fark"] - 0.002)
            and np.isclose(h["medyan_r60"], Xo.dropna(subset=["fark"]).r60.median()) and np.isclose(h["yari_genislik"], (h["ust95"] - h["alt95"]) / 2) and h["portfoy_net"] < h["portfoy"]
            and h["tutar"] == bool(h["n"] >= 30 and h["alt95"] > 0 and h["sira"] > 0.5 and h["portfoy"] > h["portfoy_esli_p90"])):
        hata.append("11) hücre ölçüleri FI_OLCUT ile aynı değil / maliyet düşülmemiş")
    # 12) karar kuralı
    def satir(dg, pz, dn, nokta, ek_u=False, ek_a=False, olc=True, p_u=0.5, tut=False, st="EVREN"):
        return {"tanim": "K24", "sira_turu": st, "degisken": dg, "pazar": pz, "donem": dn, "nokta": nokta, "olculebilir": olc, "ek_UST": ek_u, "ek_ALT": ek_a, "p_ust": p_u,
                "p_alt": 1 - p_u, "tutar_UST": tut, "tutar_ALT": False, "tutar_net_UST": tut, "tutar_net_ALT": False}
    dnm = ["2017-2021", "2022-2026", "2023-2026"]; sat = []
    sat += [satir("GP", "ABD", d, 0.05, True, p_u=1e-5, tut=True) for d in dnm] + [satir("GP", "BIST", d, 0.01) for d in dnm]                     # ABD aday, işaret tutarlı
    sat += [satir("OP", "ABD", d, 0.05, True, p_u=1e-5) for d in dnm] + [satir("OP", "BIST", d, -0.01) for d in dnm]                              # BIST'te işaret dönüyor
    sat += [satir("FCF", "ABD", dnm[0], 0.05, True, p_u=1e-5), satir("FCF", "ABD", dnm[1], 0.01, False), satir("FCF", "ABD", dnm[2], 0.01)]            # tek dönem
    sat += [satir("FCF", "BIST", d, 0.02, True, p_u=1e-5) for d in dnm]                                                                           # BIST aday
    sat += [satir("BORC", "ABD", dnm[0], 0.05, True, p_u=1e-5), satir("BORC", "ABD", dnm[1], nan, olc=False), satir("BORC", "ABD", dnm[2], nan, olc=False)]   # ölçülemez
    sat += [satir("SATIS_B", "ABD", d, 0.05, True, p_u=0.04) for d in dnm]                                                                            # BH'den geçmez
    # aile bazında karar sırası: Z52 (K64) İÇ satırlarıyla aday, EVREN satırları (ters işaretli, anlamlı) karara ve BH ailesine girmez; KAR_B (K65) tersi
    sat += [satir("Z52", "ABD", d, 0.05, True, p_u=1e-5, st="IC") for d in dnm] + [satir("Z52", "ABD", d, -0.05, False, True, p_u=1 - 1e-6) for d in dnm]
    sat += [satir("KAR_B", "ABD", d, 0.05, True, p_u=1e-5, st="IC") for d in dnm] + [satir("KAR_B", "ABD", d, 0.01) for d in dnm]
    Kr = K.k64_karar(pd.DataFrame(sat)).set_index(["degisken", "yon"])
    if not (str(Kr.loc[("Z52", "UST"), "karar"]).startswith("ABD-ADAY") and Kr.loc[("Z52", "ALT"), "karar"] == "İZ DEĞİL" and Kr.loc[("Z52", "UST"), "isaret_tutarli"]
            and Kr.loc[("KAR_B", "UST"), "karar"] == "İZ DEĞİL" and Kr.loc[("KAR_B", "UST"), "ABD_ek"] == "h/h/h" and int(Kr.aile_m.iloc[0]) == 38):
        hata.append(f"12) aile bazında karar sırası tutmuyor (Z52 {Kr.loc[('Z52', 'UST'), 'karar']}, KAR_B {Kr.loc[('KAR_B', 'UST'), 'karar']}, m {Kr.aile_m.iloc[0]})")
    bek = {("GP", "UST"): "ABD-ADAY", ("OP", "UST"): "İZ DEĞİL", ("FCF", "UST"): "BIST-ADAY", ("BORC", "UST"): "ÖLÇÜLEMEZ", ("SATIS_B", "UST"): "İZ DEĞİL", ("GP", "ALT"): "İZ DEĞİL"}
    for a, v in bek.items():
        if not str(Kr.loc[a, "karar"]).startswith(v):
            hata.append(f"12) karar kuralı: {a} -> {Kr.loc[a, 'karar']} (beklenen {v})")
    if not (Kr.loc[("GP", "UST"), "ABD_dort_sart"] and not Kr.loc[("OP", "UST"), "isaret_tutarli"] and Kr.loc[("SATIS_B", "UST"), "ABD_bh"] == "h/h" and Kr.loc[("GP", "UST"), "ABD_bh"] == "E/E"
            and Kr.loc[("GP", "UST"), "ABD_ek"] == "E/E/E" and Kr.loc[("BORC", "UST"), "ABD_karar"] == "ÖLÇÜLEMEZ"):
        hata.append("12) karar tablosu sütunları (dört şart / işaret / BH / ek katkı) beklenen gibi değil")
    # 13) kapsam modu getiri hesaplamaz
    girdi = {"ABD": {"V": V, "T": D["temel"], "pay": pay, "ozet": {"hisse": len(V)}}}
    Es = copy.deepcopy(E0); Es["pazar"] = ["ABD"]; Es["olay"]["d13"]["etkin"] = False
    asil = (FI.fi_olcut_panel, FI.fi_olcut_olay, FI.fi_olcut_hucre)

    def yasak(*a, **k):
        raise AssertionError("kapsam modunda FI_OLCUT çağrıldı")
    with tempfile.TemporaryDirectory() as td:
        try:
            FI.fi_olcut_panel = FI.fi_olcut_olay = FI.fi_olcut_hucre = yasak
            Kp = K.k64_kapsam(td, girdi, Es)
        except AssertionError as ex:
            hata.append(f"13) {ex}"); Kp = pd.DataFrame()
        finally:
            FI.fi_olcut_panel, FI.fi_olcut_olay, FI.fi_olcut_hucre = asil
        if len(Kp):
            if any(c in Kp.columns for c in ("r60", "fark", "ort_fark", "r20")) or not {"n_ham", "n_tekil", "n_pencere", "n_deger", "n_ust", "n_alt", "n_ust_ic"} <= set(Kp.columns):
                hata.append("13) kapsam tablosunda getiri sütunu var ya da sayım sütunu eksik")
            o = Kp[(Kp.degisken == "(olay)") & (Kp.donem == "2017-2021")].iloc[0]; z = Kp[(Kp.degisken == "Z52") & (Kp.donem == "2017-2021")].iloc[0]
            gm = (O.giris >= "2017-01-01") & (O.giris <= "2021-12-31")
            if not (o.n_ham == gm.sum() and o.n_tekil == (gm & O.tekil).sum() and o.n_pencere <= o.n_tekil and z.n_ust + z.n_orta + z.n_alt <= z.n_deger <= o.n_pencere):
                hata.append("13) kapsam sayıları olay tablosuyla tutmuyor")
            if "Kapsam sayımı" not in K.k64_kapsam_notu(td, Es) or "| Z52 | EVREN |" not in K.k64_kapsam_notu(td, Es):
                hata.append("13) kapsam notu yazılamadı")
    # 14) uçtan uca sentetik koşu (git'li)
    with tempfile.TemporaryDirectory() as td:
        durmali(lambda: K.k64_kos(td, True, girdi, Es), "14) ön kayıt yokken koşu durmadı", hata)
        TK.git(td, "init", "-q"); y = K.k64_onkayit(td, veri_sha=vs)
        durmali(lambda: K.k64_kos(td, True, girdi, Es), "14) git'e işlenmemiş ön kayıtla koşu durmadı", hata)
        TK.git(td, "add", "K64_K65_ON_KAYIT.md"); TK.git(td, "commit", "-q", "-m", "on kayit")
        R = K.k64_kos(td, True, girdi, Es)
        for ad in ("olay", "s1", "fark", "s2", "karar", "meta", "rapor"):
            if not os.path.exists(K._k64_yol(ad, td)):
                hata.append(f"14) çıktı yok: {ad}")
        S1, Fk, Kr2 = R["s1"], R["fark"], R["karar"]
        tm = S1[(S1.grup == "TEMEL") & (S1.rejim == "HEPSI") & (S1.donem == "2017-2021")].iloc[0]
        Xe = pd.read_csv(K._k64_yol("olay", td), parse_dates=["sinyal", "giris"]); m1 = (Xe.giris >= "2017-01-01") & (Xe.giris <= "2021-12-31") & Xe.fark.notna()
        if not (tm.n == m1.sum() and np.isclose(tm.ort_fark, Xe.fark[m1].mean()) and np.isclose(tm.medyan_r60, Xe.r60[m1].median())):
            hata.append("14) temel model hücresi olay dosyasından yeniden üretilemedi")
        fz = Fk[(Fk.degisken == "HIZ") & (Fk.sira_turu == "EVREN") & (Fk.donem == "2017-2021")].iloc[0]; gz = K.k64_grup(Xe.HIZ_sira.to_numpy(float))
        if not (fz.n_ust == (m1 & (gz == "UST")).sum() and fz.n_alt == (m1 & (gz == "ALT")).sum()
                and np.isclose(fz.nokta, Xe.fark[m1 & (gz == "UST")].mean() - Xe.fark[m1 & (gz == "ALT")].mean())
                and bool(fz.ek_UST) == bool(fz.olculebilir and fz.ort_ust > fz.ort_temel and fz.alt > 0)):
            hata.append("14) ÜST - ALT satırı olay dosyasından yeniden üretilemedi / ek katkı kuralı tutmuyor")
        if len(Fk) != 3 * 11 * 2 or len(Kr2) != 22 or set(S1[S1.rejim != "HEPSI"].groupby("degisken").sira_turu.first().drop("", errors="ignore").items()) != {(k, K.k64_karar_sirasi(k)) for k in K.k64_kodlar()} or not set(Kr2.karar.str.slice(0, 8)) <= {"ABD-ADAY", "İZ DEĞİL", "ÖLÇÜLEME", "BIST-ADA"}:
            hata.append(f"14) ÜST - ALT / karar tablosu boyutu ya da etiketleri beklenen gibi değil ({len(Fk)}, {len(Kr2)})")
        if len(R["s2"]) != 33 or not (R["s2"].n_ust.fillna(0) > 0).any():
            hata.append("14) S2 tablosu boş / eksik")
        rap = open(R["rapor"], encoding="utf-8").read()
        for parca in ("## Karar tablosu", "## Temel model", "## Z52 (K64)", "## PAY_D (K65)", "ÜST - ALT", "S2 (çöl dışı evren", "## Veri eksikleri"):
            if parca not in rap:
                hata.append(f"14) raporda '{parca}' yok")
        if open(K.k64_rapor(td, Es), encoding="utf-8").read() != rap:
            hata.append("14) rapor çıktılardan yeniden üretilince değişti")
        open(y, "a", encoding="utf-8").write("\nsonradan eklenen satır\n")
        durmali(lambda: K.k64_kos(td, True, girdi, Es), "14) git'e işlendikten sonra değişen ön kayıtla koşu durmadı", hata)
    # 15) e-posta / anahtar yok
    for ad in ("K64.py", "test_k64.py"):
        metin = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if K._K64_EPOSTA.search(metin) or re.search(r"(api[_-]?key|token|password|sifre)\s*=\s*['\"][A-Za-z0-9]{8,}", metin, re.I):
            hata.append(f"15) {ad} içinde e-posta / anahtar biçimli parça var")
    return hata


if __name__ == "__main__":
    h = testler()
    for x in h:
        print("HATA:", x)
    print("test_k64:", "TAMAM (15/15)" if not h else f"{len(h)} HATA")
    sys.exit(1 if h else 0)
