"""K60 testleri (ağ gerekmez; yalnız SENTETİK veri, gerçek veride getiri / olasılık ölçmez). Çalıştırma: python test_k60.py

1) çakışma kapısı (_CK_ONCE_K60)  2) ön kayıt mührü (UTC zaman, üzerine yazmama, bozuk / farklı mühür reddi, eşik ya da kütüphane tanımı
değişince mühür değişir; gerçek K60_ON_KAYIT.md varsa bugünkü eşiklerle aynı)  3) ön kayıtsız / git'e işlenmemiş ön kayıtla koşu durur;
DÖNEM SIRASI: dogrulama kesif'ten önce, secili.json işlenmeden; kasa dogrulama'dan önce, dogrulama_gecen.json işlenmeden, ikinci kez
açılmaz; işlenmiş ön kayıt değişirse koşu durur  4) GELECEĞE BAKMA YOK: t'den sonraki fiyat, hacim, temel veri (bilgi tarihi > t), pay
kaydı, başvuru, temettü bozulunca t ve öncesi evren + 77 sinyal + bileşikler aynı; her aileden örnek ayrıca sayılır; gelecekteki bölünme
(Yahoo biçimi) geçmiş sinyalleri değiştirmez  5) bilgi tarihi kuralı (mali yıl sonu -> 10-K, öteki -> 10-Q, sonraki ilk başvuru, yedek),
4. çeyrek türetme, 'bilgi tarihi < t' ve bayatlık, açıklama günü vekili  6) sinyal tanımları elle (her aileden)  7) panel K59 ile aynı
(uygunluk, 1 ay getirisi), R1 = K59 k59_sinyal_olc ile birebir, ileri getiri penceresi (yalnız m+1 .. m+h; kesiği aşan oluşum ayı düşer;
dönem = oluşum ayı)  8) uçlar, bayrak, eşitlik bozma, ölçüm ayları  9) lift elle, blok bootstrap tohumla birebir, aralık ve p  10) BH elle
örnek + kaba kuvvet  11) plasebo tohumla birebir, 'en büyük' eşiği  12) seçim ve geçiş kuralları, etiketler  13) lojistik (bilinen
katsayı), kalibrasyon  14) Yahoo okuyucu K60_veri ile aynı, French günlük, EDGAR dizini  15) kapsam modu getiri hesaplamaz
16) uçtan uca sentetik kesif -> dogrulama -> kasa (git'li) + rapor + olasılık tablosu; çıktılardan yeniden üretim  17) e-posta / anahtar yok.
"""
from __future__ import annotations

import copy
import gzip
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K60 as K  # noqa: E402

K57, K58, K59, KV = K.K57, K.K58, K.K59, K.KV
BOL_GERI = pd.Timestamp("2019-06-03")     # hisse 5: 1:10 ters bölünme
BOL_ILERI = pd.Timestamp("2018-09-04")    # hisse 6: 4:1 bölünme
Q_BAS, NQ, Y_BAS, NY = 2009 * 4, 70, 2009, 17
ETIKET_Q = ["Revenues", "NetIncomeLoss", "GrossProfit", "CostOfRevenue", "OperatingIncomeLoss", "ResearchAndDevelopmentExpense", "IncomeTaxExpenseBenefit"]
ETIKET_I = ["StockholdersEquity", "Liabilities", "Assets", "AssetsCurrent", "LiabilitiesCurrent", "CashAndCashEquivalentsAtCarryingValue", "LongTermDebt"]
ETIKET_Y = ETIKET_Q + ["DepreciationDepletionAndAmortization", "NetCashProvidedByUsedInOperatingActivities", "PaymentsToAcquirePropertyPlantAndEquipment",
                       "PaymentsForRepurchaseOfCommonStock", "ProceedsFromIssuanceOfCommonStock", "PaymentsOfDividends"]


def test_esik(**ek) -> dict:
    """Sentetik koşular için küçültülmüş eşikler (mühür yine K60_ESIK'ten hesaplanır)."""
    E = copy.deepcopy(K.K60_ESIK)
    E["uygunluk"]["min_evren"] = 30; E["portfoy"].update({"min_sinyal": 20, "min_bayrak": 3})
    E["r2"].update({"cekilis": 120, "min_hisse_ay": 40}); E["coklu"].update({"plasebo_n": 30, "maks_tekrar": 300})
    for k, v in ek.items():
        E[k].update(v)
    return E


def sentetik_demet(N: int = 150, bas: str = "2010-01-04", bit: str = "2026-08-31", tohum: int = 1, etki: float = 0.0006) -> dict:
    """Sentetik K60 demeti: günlük O / H / L / C / A / V, bölünmeler, temettüler, temel tablo (bilgi tarihleriyle), pay kayıtları, başvurular,
    French faktörleri. 'kalite' kalıcı bir hisse özelliğidir: kârlılığı ve (etki > 0 ise) günlük getiri eğilimini birlikte belirler."""
    rng = np.random.default_rng(tohum); gun = pd.bdate_range(bas, bit); G = len(gun); S = [f"S{i:03d}" for i in range(N)]
    kalite = rng.normal(0, 1, N); beta = rng.uniform(0.5, 1.5, N); sig = 0.018 * np.exp(0.3 * rng.normal(0, 1, N))
    mk = rng.normal(0.0004, 0.009, G); r = 0.0002 + etki * kalite[None, :] + beta[None, :] * mk[:, None] + rng.normal(0, 1, (G, N)) * sig[None, :]
    C = rng.uniform(15, 80, N)[None, :] * np.exp(np.cumsum(np.log1p(np.clip(r, -0.5, 1.0)), axis=0))
    x = np.linspace(0, 40, G)
    C[:, 3] = 1.2 + 0.3 * np.sin(x)                     # hep 2 $ altı
    C[:, 5] = 12.0 + 3.0 * np.sin(x)                    # düzeltilmiş 9-15; ters bölünmeden önce o günkü fiyat 0,9-1,5
    O = C * np.exp(rng.normal(0, 0.004, (G, N))); H = np.maximum(O, C) * (1 + np.abs(rng.normal(0, 0.004, (G, N)))); L = np.minimum(O, C) * (1 - np.abs(rng.normal(0, 0.004, (G, N))))
    V = rng.integers(200_000, 1_000_000, (G, N)).astype(float); V[:, 4] = 100.0      # hisse 4 likit değil
    ilk = np.full(N, np.datetime64("2005-01-03", "D"))
    for j in range(N):
        if j % 9 == 0 and j:
            k = int(rng.integers(300, 2500)); C[:k, j] = O[:k, j] = H[:k, j] = L[:k, j] = V[:k, j] = np.nan; ilk[j] = gun[k].to_datetime64().astype("datetime64[D]")
        if j % 13 == 7:
            bos = rng.choice(G, 25, replace=False); C[bos, j] = O[bos, j] = H[bos, j] = L[bos, j] = V[bos, j] = np.nan
    tem = {}; A = C.copy()
    for j in range(N):
        if j % 4 == 1:                                  # temettü ödeyenler: çeyreklik hak düşüm günü; A geçmişe doğru küçülür
            gunler = gun[(gun.month % 3 == 2) & (gun.day <= 7)]; gunler = gunler[~pd.Series(gunler.to_period("M")).duplicated().to_numpy()]
            if j % 8 == 5:
                gunler = gunler[gunler < pd.Timestamp("2019-01-01")]        # 2019'da temettüyü kesenler
            if j % 16 == 9:
                gunler = gunler[gunler > pd.Timestamp("2016-06-01")]        # 2016'da başlatanlar
            tem[S[j]] = gunler.to_numpy("datetime64[D]")
            sonra = len(gunler) - np.searchsorted(gunler.to_numpy("datetime64[ns]"), gun.to_numpy("datetime64[ns]"), side="right")
            A[:, j] = C[:, j] * 0.995 ** sonra
    bol = {S[5]: (np.array([BOL_GERI.to_datetime64()], "datetime64[ns]"), np.array([0.1])), S[6]: (np.array([BOL_ILERI.to_datetime64()], "datetime64[ns]"), np.array([4.0]))}
    cik = [None if j == 10 else str(1000 + j) for j in range(N)]; sic = (rng.integers(10, 22, N) * 100 + rng.integers(0, 99, N)).astype(int); sic[11] = -1
    # temel tablo
    nat = np.datetime64("NaT", "D"); T = {"q_bas": Q_BAS, "y_bas": Y_BAS, "Q": {}, "I": {}, "Y": {}}
    qson = np.array([pd.Period(year=(Q_BAS + q) // 4, quarter=(Q_BAS + q) % 4 + 1, freq="Q").end_time.normalize().to_datetime64() for q in range(NQ)], "datetime64[D]")
    bit = np.repeat(qson[:, None], N, axis=1); gec = rng.integers(35, 50, (NQ, N)); mali = np.zeros((NQ, N), bool); mali[3::4] = True
    bilgi = bit + np.where(mali, gec + 25, gec).astype("timedelta64[D]")
    oz = rng.uniform(2e8, 9e8, N)[None, :] * np.exp(np.cumsum(rng.normal(0.01, 0.03, (NQ, N)), axis=0)); oz[:, 7] = -5e7
    varlik = oz * rng.uniform(1.5, 4.0, N)[None, :] * np.exp(np.cumsum(rng.normal(0.0, 0.02, (NQ, N)), axis=0)); varlik[:, 7] = 4e8
    gelir = varlik * rng.uniform(0.1, 0.4, N)[None, :] * np.exp(rng.normal(0, 0.08, (NQ, N)))
    kar = np.abs(oz) * (0.02 + 0.012 * kalite[None, :]) + rng.normal(0, 0.004, (NQ, N)) * np.abs(oz)
    T["Q"]["Revenues"] = gelir; T["Q"]["NetIncomeLoss"] = kar; T["Q"]["GrossProfit"] = gelir * rng.uniform(0.2, 0.6, N)[None, :]
    T["Q"]["CostOfRevenue"] = gelir - T["Q"]["GrossProfit"]; T["Q"]["OperatingIncomeLoss"] = kar * 1.3
    T["Q"]["ResearchAndDevelopmentExpense"] = np.where((np.arange(N) % 3 == 0)[None, :], gelir * 0.08, np.nan); T["Q"]["IncomeTaxExpenseBenefit"] = kar * 0.25 * np.exp(rng.normal(0, 0.2, (NQ, N)))
    T["Q"]["WeightedAverageNumberOfDilutedSharesOutstanding"] = np.full((NQ, N), 1.0e7)
    T["I"]["StockholdersEquity"] = oz; T["I"]["Assets"] = varlik.copy(); T["I"]["Liabilities"] = varlik - oz
    T["I"]["AssetsCurrent"] = varlik * rng.uniform(0.2, 0.5, (NQ, N)); T["I"]["LiabilitiesCurrent"] = varlik * rng.uniform(0.1, 0.3, (NQ, N))
    T["I"]["CashAndCashEquivalentsAtCarryingValue"] = varlik * rng.uniform(0.03, 0.2, (NQ, N)); T["I"]["LongTermDebt"] = np.where((np.arange(N) % 5 == 0)[None, :], np.nan, varlik * rng.uniform(0.05, 0.4, (NQ, N)))
    T["I"]["LongTermDebtNoncurrent"] = np.where((np.arange(N) % 5 == 0)[None, :], varlik * 0.2, np.nan); T["I"]["CommonStockSharesOutstanding"] = np.full((NQ, N), 1.0e7)
    T["I"]["Assets"][:, 12] = np.nan; T["I"]["LiabilitiesAndStockholdersEquity"] = varlik.copy()       # hisse 12: yalnız toplam pasif
    T["I"]["Liabilities"][:, 13] = np.nan                                                                 # hisse 13: yükümlülük = varlık - özkaynak
    for q in range(0, NQ, 5):
        T["Q"]["NetIncomeLoss"][q, 8] = np.nan                                                            # hisse 8: eksik çeyrek kârı
    Ybit = np.full((NY, N), nat); Ybas = np.full((NY, N), nat); Ybilgi = np.full((NY, N), nat); Yq = np.full((NY, N), -1)
    for y in range(NY):
        q4 = y * 4 + 3
        Ybit[y] = qson[q4]; Ybas[y] = np.datetime64(f"{Y_BAS + y}-01-01"); Ybilgi[y] = bilgi[q4]; Yq[y] = q4
        for e in ETIKET_Q:
            T["Y"].setdefault(e, np.full((NY, N), np.nan))[y] = T["Q"][e][y * 4:y * 4 + 4].sum(axis=0)
    ocf = T["Y"]["NetIncomeLoss"] * rng.uniform(0.6, 1.6, (NY, N)); ocf[:, 14] = -np.abs(ocf[:, 14])
    T["Y"]["NetCashProvidedByUsedInOperatingActivities"] = ocf; T["Y"]["DepreciationDepletionAndAmortization"] = T["Y"]["Revenues"] * 0.04
    T["Y"]["PaymentsToAcquirePropertyPlantAndEquipment"] = T["Y"]["Revenues"] * rng.uniform(0.02, 0.1, (NY, N))
    T["Y"]["PaymentsForRepurchaseOfCommonStock"] = np.where((np.arange(N) % 2 == 0)[None, :], T["Y"]["Revenues"] * rng.uniform(0.0, 0.05, (NY, N)), np.nan)
    T["Y"]["ProceedsFromIssuanceOfCommonStock"] = np.where((np.arange(N) % 4 == 2)[None, :], T["Y"]["Revenues"] * 0.03, np.nan)
    T["Y"]["PaymentsOfDividends"] = np.where((np.arange(N) % 4 == 1)[None, :], T["Y"]["Revenues"] * 0.02, np.nan)
    pay = []
    for j in range(N):
        if j == 15:
            pay.append(None); continue                                                                    # hisse 15: kapak sayısı yok -> yedek
        d = bit[:, j] + np.timedelta64(30, "D"); buyume = 1.02 if j % 4 == 2 else (0.995 if j % 2 == 0 else 1.0)
        n_ = 1.0e7 * buyume ** np.arange(NQ) * (4.0 if j == 6 else 1.0) ** (d >= BOL_ILERI.to_datetime64().astype("datetime64[D]")) \
            * (0.1 if j == 5 else 1.0) ** (d >= BOL_GERI.to_datetime64().astype("datetime64[D]"))
        pay.append((d, n_, bilgi[:, j].copy()))
    T.update({"bit": bit, "bilgi": bilgi, "mali": mali, "Ybit": Ybit, "Ybas": Ybas, "Ybilgi": Ybilgi, "Yq": Yq, "pay": pay})
    basv = {g: [None] * N for g in ("K", "Q", "8K", "NT", "S3", "424B5", "13D", "TOI")}
    for j in range(N):
        if cik[j] is None:
            continue
        basv["K"][j] = np.unique(bilgi[mali[:, j], j]); basv["Q"][j] = np.unique(bilgi[~mali[:, j], j])
        basv["8K"][j] = np.unique(np.r_[bilgi[::2, j] - np.timedelta64(7, "D"), bilgi[1::4, j] - np.timedelta64(45, "D")])
        for g, p, kosul in (("NT", 0.03, j % 7 == 3), ("S3", 0.06, j % 3 == 0), ("424B5", 0.08, j % 3 == 0), ("13D", 0.05, j % 5 == 1), ("TOI", 0.04, j % 6 == 2)):
            if kosul:
                sec = rng.random(G) < p
                basv[g][j] = gun[sec].to_numpy("datetime64[D]") if sec.any() else None
    ffg = pd.DataFrame({"MKT_RF": mk - 0.00005, "SMB": rng.normal(0, 0.004, G), "HML": rng.normal(0, 0.004, G), "RF": 0.00005}, index=gun)
    ay = gun.to_period("M"); ffa = (1 + ffg).groupby(ay).prod() - 1
    for k in ("RMW", "CMA", "UMD"):
        ffa[k] = rng.normal(0, 0.01, len(ffa))
    return {"gun": gun, "sembol": S, "O": O, "H": H, "L": L, "C": C, "A": A, "V": V, "bolunme": bol, "temettu": tem, "ilk_islem": ilk,
            "tur_ok": np.ones(N, bool), "cik": cik, "sic": sic, "temel": T, "basvuru": basv, "ff_gunluk": ffg, "ff_aylik": ffa[["MKT_RF", "SMB", "HML", "RMW", "CMA", "UMD", "RF"]],
            "kalite": kalite}


# ---------------------------------------------------------------- yardımcılar
def kopya(D: dict) -> dict:
    """Demetin derin kopyası (diziler ve temel tablo ayrı)."""
    out = dict(D)
    for k in ("O", "H", "L", "C", "A", "V"):
        out[k] = D[k].copy()
    T = D["temel"]; out["temel"] = {**T, "Q": {a: x.copy() for a, x in T["Q"].items()}, "I": {a: x.copy() for a, x in T["I"].items()},
                                    "Y": {a: x.copy() for a, x in T["Y"].items()}, "pay": [None if p is None else tuple(x.copy() for x in p) for p in T["pay"]]}
    out["basvuru"] = {g: [None if x is None else x.copy() for x in v] for g, v in D["basvuru"].items()}
    out["temettu"] = {s: x.copy() for s, x in D["temettu"].items()}; out["bolunme"] = dict(D["bolunme"])
    out["ff_gunluk"] = D["ff_gunluk"].copy(); out["ff_aylik"] = D["ff_aylik"].copy()
    return out


def boz(D: dict, t0: pd.Timestamp, tohum: int = 9) -> dict:
    """t0'dan SONRAKİ her şeyi bozar: fiyat / hacim (gün > t0), bilgi tarihi >= t0 olan çeyrek ve yıl değerleri, bilgi tarihi >= t0 olan pay
    kayıtları, günü >= t0 olan başvurular (silinir + rastgele yenileri eklenir), günü > t0 olan temettüler, French faktörleri (gün > t0)."""
    rng = np.random.default_rng(tohum); B = kopya(D); gun = pd.DatetimeIndex(D["gun"]); s = np.asarray(gun > t0); n = int(s.sum()); N = len(D["sembol"])
    t0d = t0.to_datetime64().astype("datetime64[D]")
    yol = np.exp(np.cumsum(rng.normal(0, 0.05, (n, N)), axis=0)) * rng.uniform(0.3, 3.0, N)[None, :]
    for k in ("O", "H", "L", "C", "A"):
        B[k][s] = B[k][s] * yol * (1.3 if k == "H" else 1.0)
    B["V"][s] = B["V"][s] * rng.uniform(0.01, 5.0, (n, N)); B["C"][s][rng.random((n, N)) < 0.01] = np.nan
    T, Tb = D["temel"], B["temel"]; gq = T["bilgi"] >= t0d; gy = T["Ybilgi"] >= t0d
    for a in Tb["Q"]:
        Tb["Q"][a][gq] = Tb["Q"][a][gq] * rng.uniform(-2, 3, int(gq.sum()))
    for a in Tb["I"]:
        Tb["I"][a][gq] = Tb["I"][a][gq] * rng.uniform(0.2, 3, int(gq.sum()))
    for a in Tb["Y"]:
        Tb["Y"][a][gy] = Tb["Y"][a][gy] * rng.uniform(-2, 3, int(gy.sum()))
    for j, p in enumerate(Tb["pay"]):
        if p is not None:
            m = p[2] >= t0d; p[1][m] = p[1][m] * rng.uniform(0.2, 5.0, int(m.sum()))
    gelecek = gun[s].to_numpy("datetime64[D]")
    for g, v in B["basvuru"].items():
        for j in range(N):
            if v[j] is not None or (D["cik"][j] is not None and rng.random() < 0.3):
                eski = v[j][v[j] < t0d] if v[j] is not None else np.array([], "datetime64[D]")
                v[j] = np.unique(np.r_[eski, rng.choice(np.r_[gelecek, t0d], size=min(6, len(gelecek) + 1), replace=False)])
    for sm in list(B["temettu"]):
        B["temettu"][sm] = np.unique(np.r_[B["temettu"][sm][B["temettu"][sm] <= t0d], rng.choice(gelecek, size=min(3, len(gelecek)), replace=False)])
    B["ff_gunluk"].loc[gun[s]] = rng.normal(0, 0.02, (n, 4))
    ay = B["ff_aylik"].index > t0.to_period("M"); B["ff_aylik"].loc[ay] = rng.normal(0, 0.05, (int(ay.sum()), B["ff_aylik"].shape[1]))
    return B


def esit(a: np.ndarray, b: np.ndarray, rtol: float = 0.0) -> bool:
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.shape != b.shape or not (np.isnan(a) == np.isnan(b)).all():
        return False
    m = ~np.isnan(a)
    return bool(np.array_equal(a[m], b[m]) if rtol == 0 else np.allclose(a[m], b[m], rtol=rtol, atol=1e-12))


def elle_q0(T: dict, t: np.datetime64, j: int, max_gun: int = 200) -> int:
    """Bilgi tarihi < t olan en son çeyrek (bayat değilse); yoksa -1. Düz döngü."""
    q0 = -1
    for q in range(T["bilgi"].shape[0]):
        if not np.isnat(T["bilgi"][q, j]) and T["bilgi"][q, j] < t:
            q0 = q
    return q0 if q0 >= 0 and (t - T["bit"][q0, j]) <= np.timedelta64(max_gun, "D") else -1


def git(kl: str, *arg: str) -> None:
    r = subprocess.run(["git", "-C", kl, "-c", "user.name=k60test", "-c", "user.email=k60test", "-c", "commit.gpgsign=false", *arg], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {arg}: {r.stderr[:300]}")


def durmali(f, ad: str, hata: list, tur=None) -> None:
    try:
        f(); hata.append(ad)
    except (tur or K.K60Hata):
        pass


def testler() -> list:
    hata = []; E0 = K.K60_ESIK; nan = np.nan
    # 1) çakışma kapısı
    src = open(os.path.join(KOK, "K60.py"), encoding="utf-8").read().replace("from __future__ import annotations\n", "")
    g = {"__name__": "kapi_test", "k60_kos": object(), "_CK_KAYIT": {"k60_kos": "BASKA.py"}}
    try:
        exec(compile(src, "K60.py", "exec"), g); hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "kapi_test2"}
    try:
        exec(compile(src, "K60.py", "exec"), g2); exec(compile(src, "K60.py", "exec"), g2)
    except Exception as ex:
        hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
    if "_CK_ONCE_K60 = " not in src or "_cakisma_kontrol_k60()" not in src:
        hata.append("1) çakışma kapısı adı _CK_ONCE_K60 değil")
    # 2) ön kayıt mührü + kütüphane
    tn = K.k60_tanim()
    if len(tn) != len(E0["kutuphane"]) or len(tn) < 60:
        hata.append(f"2) kütüphane kodları tekil değil ya da 60'tan az: {len(tn)}")
    aile = {r["aile"] for r in E0["kutuphane"]}
    if not {"MOM", "VAL", "PRF", "INV", "EAR", "RSK", "LIQ", "SEA", "DIS", "SEC"} <= aile:
        hata.append(f"2) istenen ailelerden biri kütüphanede yok: {sorted(aile)}")
    if any(r["yon"] not in ("+", "-", "?") or r["tur"] not in ("surekli", "bayrak") or not r["tanim"] or not r["kaynak"] for r in E0["kutuphane"]):
        hata.append("2) kütüphane satırında yön / tür / tanım / kaynak eksik")
    if {r["kod"] for r in E0["dalga2"]} & set(tn):
        hata.append("2) bir kod hem ölçülen hem ertelenen listede")
    for b, t in E0["bilesik"].items():
        if any(u not in tn and u not in E0["ek_bilesen"] for u in t["uye"]) or not (1 <= t["min"] <= len(t["uye"])):
            hata.append(f"2) bileşik {b} üyeleri / en az üye kuralı bozuk")
        if t["rol"] == "AİLE" and any(tn[u]["tur"] != "surekli" or tn[u]["yon"] == "?" for u in t["uye"]):
            hata.append(f"2) aile bileşiği {b} bayrak ya da '?' sinyal içeriyor")
    if E0["donem"] != {"kesif": ["2012-01", "2021-12"], "dogrulama": ["2022-01", "2023-12"], "kasa": ["2024-01", "2026-08"]} or E0["veri"]["kes"] != "2026-08-31":
        hata.append("2) dönemler / kesik iş tanımındaki gibi değil")
    if not (E0["portfoy"]["dilim"] == 0.10 and E0["r1"]["maliyet"] == 0.001 and E0["r2"]["blok"] == 12 and E0["r2"]["cekilis"] == 500 and E0["r2"]["ufuk"] == [12, 6, 3]
            and E0["r2"]["olay"] == {"p100": 1.0, "p50": 0.5, "m50": -0.5} and E0["coklu"]["bh_q"] == 0.10 and E0["coklu"]["plasebo_n"] == 200 and E0["coklu"]["t_dogrudan"] == 3.0
            and E0["dogrulama"]["t_tek_yon"] == 1.65 and E0["uygunluk"]["fiyat_min"] == 2.0 and E0["uygunluk"]["likit_min"] == 1.0e6 and E0["uygunluk"]["gecmis_gun"] == 252
            and E0["r1"]["cetvel"] == {k: K59.K59_ESIK["cetvel"][k] for k in ("nw_lag", "t_esik", "alt_donem_n", "alt_donem_min", "son_pay")}):
        hata.append("2) K60_ESIK sabitleri iş tanımındaki gibi değil")
    with tempfile.TemporaryDirectory() as td:
        vs = {"k60_fiyat": ("a" * 64, 4755), "k60_secframes": ("b" * 64, 1781)}
        y = K.k60_onkayit(td, veri_sha=vs); ilk = open(y, encoding="utf-8").read()
        if f"ESIK_SHA256: {K.k60_esik_sha()}" not in ilk or not re.search(r"^Yazım zamanı: \d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC", ilk, re.M):
            hata.append("2) ön kayıtta mühür / UTC zaman yok")
        for parca in ("## Veri", "## 0. Soru", "## 1. Kütüphane", "## 2. Dönemler", "## 3. Evren", "## 4. Cetvel R1", "## 5. Cetvel R2", "## 6. KEŞİF", "## 7. DOĞRULAMA",
                      "## 8. Birleşik olasılık modeli", "## 9. Yanlılık beyanı", "## 10. Çıktılar", "## 11. BOŞLUK listesi", "## 12. Kapsam", "## 13. Değişmezlik",
                      "K60-İZ ADAYI", "K60-OLASILIK İZİ", "K60-KAÇINMA İZİ", "İZ ilan EDİLEMEZ", "DALGA 2", "TEK AÇILIŞ", "Benjamini-Hochberg", "YALNIZ YAŞAYANLAR", "ALT SINIR",
                      "python -I K60.py kos --donem kesif", "python -I K60.py kos --donem dogrulama", "python -I K60.py kos --donem kasa", "secili.json", "dogrulama_gecen.json",
                      "2012-01", "2021-12", "2022-01", "2023-12", "2024-01", "EVREN_SECENEKLERI") + tuple(f"BOŞLUK {i}." for i in range(1, 26)) \
                + tuple(f"| {r['kod']} | {r['aile']} | {r['yon']} |" for r in E0["kutuphane"]) + tuple(f"- {r['kod']} (" for r in E0["dalga2"]) + tuple(f"- {b} (" for b in E0["bilesik"]):
            if parca not in ilk:
                hata.append(f"2) ön kayıtta '{parca}' yok")
        if K._k60_onkayit_oku(y)["veri"] != vs:
            hata.append("2) ön kayıttan veri sha256'ları okunamadı")
        K.k60_onkayit(td)
        if open(y, encoding="utf-8").read() != ilk:
            hata.append("2) ön kayıt üzerine yazıldı")
        if K.k60_onkayit_dogrula(td)["sha"] != K.k60_esik_sha():
            hata.append("2) doğrulama mührü yanlış")
        durmali(lambda: K.k60_onkayit_dogrula(td, git=True), "3) git'e işlenmemiş ön kayıt kabul edildi", hata)
        open(y, "w", encoding="utf-8").write(ilk.replace(K.k60_esik_sha(), "0" * 64))
        durmali(lambda: K.k60_onkayit_dogrula(td), "2) bozuk mühür kabul edildi", hata)
        durmali(lambda: K.k60_onkayit(td), "2) mührü farklı ön kayıt sessizce kabul edildi", hata)
    E2 = copy.deepcopy(E0); E2["coklu"]["bh_q"] = 0.2
    E3 = copy.deepcopy(E0); E3["kutuphane"][0]["tanim"] += " "
    E4 = copy.deepcopy(E0); E4["donem"]["kesif"][0] = "2016-01"
    if len({K.k60_esik_sha(), K.k60_esik_sha(E2), K.k60_esik_sha(E3), K.k60_esik_sha(E4)}) != 4 or K.k60_esik_sha() != K.k60_esik_sha(copy.deepcopy(E0)):
        hata.append("2) eşik / kütüphane tanımı / dönem değişince mühür değişmiyor ya da aynı eşikte mühür farklı")
    gercek = K._k60_yol("onkayit")
    if os.path.exists(gercek):
        try:
            oc = K.k60_onkayit_dogrula()
            if not oc["zaman_utc"] or len(oc["veri"]) < 6:
                hata.append(f"2) gerçek ön kayıtta UTC zaman / veri sha256 eksik ({len(oc['veri'])} kaynak)")
            for d in K.K60_DONEM:
                m = K._k60_meta_bitti(d, None)
                if m and (pd.Timestamp(oc["zaman_utc"]) > pd.Timestamp(m["kos_baslangic"].replace(" UTC", "")) or m["onkayit"]["sha"] != oc["sha"]):
                    hata.append(f"2) ön kayıt {d} koşusundan sonra yazılmış / koşu başka mühürle yapılmış")
        except K.K60Hata as ex:
            hata.append(f"2) gerçek ön kayıt bugünkü eşiklerle aynı değil: {ex}")
    # ortak sentetik veri
    D = sentetik_demet(); Et = test_esik(); P = K.k60_panel(D, Et, True); Sd, ek = K.k60_sinyaller(D, P, Et); U = P["U"]; me = P["ay_sonu"]; mp = P["me_pos"]; M, N = U.shape
    gun = pd.DatetimeIndex(D["gun"]); T = D["temel"]; S = D["sembol"]
    # 3) ön kayıtsız koşu durur (sentetik demetle bile); kapsam için ön kayıt gerekmez
    with tempfile.TemporaryDirectory() as td:
        durmali(lambda: K.k60_kos("kesif", td, git_sart=False, demet=D, E=Et), "3) ön kayıtsız koşu durmadı", hata)
        K.k60_onkayit(td, veri_sha={})
        durmali(lambda: K.k60_kos("kesif", td, git_sart=True, demet=D, E=Et), "3) git'e işlenmemiş ön kayıtla koşu durmadı", hata)
        durmali(lambda: K.k60_kos("dogrulama", td, git_sart=False, demet=D, E=Et), "3) KEŞİF çıktısı yokken DOĞRULAMA durmadı", hata)
        durmali(lambda: K.k60_kos("kasa", td, git_sart=False, demet=D, E=Et), "3) DOĞRULAMA çıktısı yokken KASA durmadı", hata)
        durmali(lambda: K.k60_kos("baska", td, git_sart=False, demet=D, E=Et), "3) bilinmeyen dönem kabul edildi", hata)
        if os.path.exists(K._k60_yol("kasa_isaret", td)):
            hata.append("3) reddedilen KASA koşusu açılış işareti bıraktı")
    # 4) GELECEĞE BAKMA YOK
    k0 = int(np.flatnonzero(np.asarray(me == pd.Timestamp("2019-03-29")))[0]); t0 = me[k0]
    Db = boz(D, t0); Pb = K.k60_panel(Db, Et, True); Sb, ekb = K.k60_sinyaller(Db, Pb, Et)
    if not np.array_equal(P["U"][:k0 + 1], Pb["U"][:k0 + 1]) or not esit(P["fiyat_o"][:k0 + 1], Pb["fiyat_o"][:k0 + 1]) or not esit(P["tl_me"][:k0 + 1], Pb["tl_me"][:k0 + 1]):
        hata.append("4) t'den sonraki veri bozulunca t ve öncesi evren / o günkü fiyat / likidite değişti")
    if np.array_equal(P["U"][k0 + 2:], Pb["U"][k0 + 2:]) and esit(Sd["MOM_12_1"][k0 + 2:], Sb["MOM_12_1"][k0 + 2:]):
        hata.append("4) bozma hiçbir şeyi değiştirmedi (test anlamsız)")
    for kod in Sd:
        if not esit(Sd[kod][:k0 + 1], Sb[kod][:k0 + 1]):
            fark = np.argwhere(~((Sd[kod][:k0 + 1] == Sb[kod][:k0 + 1]) | (np.isnan(Sd[kod][:k0 + 1]) & np.isnan(Sb[kod][:k0 + 1]))))
            hata.append(f"4) GELECEĞE BAKMA: {kod} t ve öncesinde değişti (ör. ay {me[fark[0][0]].date()}, hisse {S[fark[0][1]]}; {len(fark)} hücre)")
        if not np.isfinite(Sd[kod][max(k0 - 24, 0):k0 + 1]).any():
            hata.append(f"4) {kod}: sınanan aylarda hiç değer yok (geleceğe bakma testi boş)")
        if kod in tn and esit(Sd[kod][k0 + 3:], Sb[kod][k0 + 3:]) and kod not in ("E_IPO_3Y", "E_SPLIT", "E_RSPLIT"):
            hata.append(f"4) {kod}: bozulan gelecek veriye tepki vermedi (sinyal veriyi okumuyor olabilir)")
    for a in ("q0", "y0", "pay_kaynak"):
        if not np.array_equal(ek[a][:k0 + 1], ekb[a][:k0 + 1]):
            hata.append(f"4) {a} t ve öncesinde değişti")
    for a in aile:
        if not any(np.isfinite(Sd[r["kod"]][k0]).sum() >= 20 for r in E0["kutuphane"] if r["aile"] == a):
            hata.append(f"4) {a} ailesinden t ayında yeterli değeri olan sinyal yok")
    # gelecekteki bölünme (Yahoo biçimi: düzeltilmiş seri aynı kalır, bölünme kaydı eklenir, eski pay sayıları eski birimdedir)
    Dsp = kopya(D); js = 20; sg = np.datetime64("2021-03-01", "D")
    Dsp["bolunme"][S[js]] = (np.array([sg], "datetime64[ns]"), np.array([3.0])); pj = Dsp["temel"]["pay"][js]; pj[1][pj[0] < sg] /= 3.0
    Psp = K.k60_panel(Dsp, Et, True); Ssp, _e = K.k60_sinyaller(Dsp, Psp, Et); ks = int(np.searchsorted(P["mtD"], sg))
    for kod in ("SIZE_ME", "TURN_12M", "NSI_1Y", "NSI_5Y", "BM", "EP", "MOM_12_1", "AMIHUD", "HIGH52", "GAP_OVN", "EV_EBITDA", "IND_LEAD_BIG"):
        if not esit(Sd[kod][:, js], Ssp[kod][:, js], rtol=1e-9):
            hata.append(f"4) gelecekteki bölünme {kod} sinyalini değiştirdi (piyasa değeri / pay birimi tutarsız)")
    if not np.allclose(Psp["fiyat_o"][:ks, js], 3.0 * P["fiyat_o"][:ks, js], equal_nan=True) or not esit(Psp["fiyat_o"][ks:, js], P["fiyat_o"][ks:, js]):
        hata.append("4) o günkü fiyat bölünmeden önce 3 kat, sonra aynı olmalıydı")
    if np.nanmax(Ssp["E_SPLIT"][:ks, js]) != 0 or Ssp["E_SPLIT"][ks, js] != 1 or Ssp["E_SPLIT"][ks + 11, js] != 1 or Ssp["E_SPLIT"][ks + 13, js] != 0 or np.nanmax(Sd["E_SPLIT"][:, js]) != 0:
        hata.append("4) E_SPLIT bayrağı bölünmeden önce 0, bölünme ayında 1 olmalıydı")
    # 5) bilgi tarihi kuralı, 4. çeyrek türetme, 'bilgi tarihi < t', bayatlık, açıklama günü vekili
    g_ = lambda s: np.datetime64(s, "D"); nat = np.datetime64("NaT", "D")  # noqa: E731
    qe = np.array([pd.Period(year=2015 + q // 4, quarter=q % 4 + 1, freq="Q").end_time.normalize().to_datetime64() for q in range(8)], "datetime64[D]")
    Tr = {"q_bas": 2015 * 4, "y_bas": 2015, "Q": {"NetIncomeLoss": np.full((8, 3), nan)}, "I": {"Assets": np.full((8, 3), nan)}, "Y": {"NetIncomeLoss": np.full((2, 3), nan)},
          "bit": np.full((8, 3), nat), "Ybit": np.full((2, 3), nat), "Ybas": np.full((2, 3), nat),
          "pay_ham": [[(g_("2015-04-30"), 1.0e6), (g_("2015-07-31"), 1.1e6), (g_("2015-10-30"), 0.0)], [(g_("2015-04-30"), 5.0e5)], []]}
    for j in range(3):
        for q, v in ((0, 10.0), (1, 20.0), (2, 30.0), (4, 11.0), (5, 21.0), (6, 31.0)):
            Tr["Q"]["NetIncomeLoss"][q, j] = v; Tr["bit"][q, j] = qe[q]; Tr["I"]["Assets"][q, j] = 100.0 + q
    for j in (0, 1):
        Tr["Y"]["NetIncomeLoss"][0, j] = 100.0; Tr["Ybit"][0, j] = qe[3]; Tr["Ybas"][0, j] = g_("2015-01-01")
    Tr["Y"]["NetIncomeLoss"][1, 1] = 90.0; Tr["Ybit"][1, 1] = qe[7]; Tr["Ybas"][1, 1] = g_("2016-03-01")       # süre 306 gün: 4. çeyrek türetilmez
    Kg = [np.array(["2016-04-20"], "datetime64[D]"), None, np.array(["2016-02-20"], "datetime64[D]")]
    Qg = [np.array(["2015-05-10", "2015-08-09", "2015-11-08", "2016-05-12", "2016-08-10", "2016-11-09"], "datetime64[D]"), None, np.array(["2015-05-01", "2015-07-03", "2015-08-01"], "datetime64[D]")]
    Tt = K.k60_temel_tamamla(Tr, Kg, Qg, E0); bl = Tt["bilgi"]
    if Tt["turetilen_q4"] != 2 or Tt["Q"]["NetIncomeLoss"][3, 0] != 40.0 or Tt["Q"]["NetIncomeLoss"][3, 1] != 40.0 or np.isfinite(Tt["Q"]["NetIncomeLoss"][3, 2]) or np.isfinite(Tt["Q"]["NetIncomeLoss"][7, 1]):
        hata.append(f"5) 4. çeyrek türetme yanlış: {Tt['turetilen_q4']}, {Tt['Q']['NetIncomeLoss'][3]}")
    if not (bl[0, 0] == g_("2015-05-10") and bl[2, 0] == g_("2015-11-08") and bl[3, 0] == g_("2016-04-20") and bl[4, 0] == g_("2016-05-12") and Tt["Ybilgi"][0, 0] == g_("2016-04-20")):
        hata.append(f"5) bilgi tarihi: mali yıl sonu 10-K'ya, öteki çeyrek 10-Q'ya bağlanmalı (geç gelen 10-K sonraki çeyreğe yazılmamalı): {bl[:, 0]}")
    if not (Tt["mali"][3, 0] and not Tt["mali"][2, 0] and not Tt["mali"][4, 0] and Tt["bilgi_kaynak"][3, 0] == 1 and Tt["bilgi_kaynak"][0, 1] == 2):
        hata.append("5) mali yıl sonu bayrağı / bilgi kaynağı yanlış")
    if not (bl[0, 1] == qe[0] + np.timedelta64(E0["bilgi"]["yedek_ceyrek_gun"], "D") and bl[3, 1] == qe[3] + np.timedelta64(E0["bilgi"]["yedek_yil_gun"], "D")
            and Tt["Ybilgi"][0, 1] == qe[3] + np.timedelta64(E0["bilgi"]["yedek_yil_gun"], "D") and E0["bilgi"]["yedek_ceyrek_gun"] == 90 and E0["bilgi"]["yedek_yil_gun"] == 120):
        hata.append(f"5) yedek bilgi tarihi (çeyrek + 90, yıl + 120) yanlış: {bl[:, 1]}")
    if not (bl[0, 2] == g_("2015-05-01") and bl[1, 2] == g_("2015-08-01") and bl[2, 2] == g_("2016-02-20") and bl[4, 2] == qe[4] + np.timedelta64(90, "D") and E0["bilgi"]["en_az_gun"] == 15):
        hata.append(f"5) yıllık çerçevesi olmayan şirkette ilk dönemsel başvuru / yedek yanlış: {bl[:, 2]}")
    p0_, p1_ = Tt["pay"][0], Tt["pay"][1]
    if not (len(p0_[0]) == 2 and p0_[2][0] == g_("2015-05-10") and p0_[2][1] == g_("2015-08-09") and p1_[2][0] == g_("2015-04-30") + np.timedelta64(60, "D") and Tt["pay"][2] is None):
        hata.append("5) kapak pay sayısı bilgi tarihi (kapak gününden sonraki ilk başvuru; yoksa + 60 gün; sıfır pay atılır) yanlış")
    mt_ = np.array(["2015-05-10", "2015-05-11", "2016-04-20", "2016-04-21", "2016-05-13", "2017-07-31"], "datetime64[D]"); AO = K._K60Temel(Tt, mt_, 3, E0["bilgi"])
    if list(AO.q0[:, 0]) != [-1, 0, -1, 3, 4, -1] or list(AO.y0[:, 0]) != [-1, -1, -1, 0, 0, -1]:
        hata.append(f"5) ç0 / y0 yanlış (bilgi tarihi < t KESİN; bayat çeyrek yok sayılır): {list(AO.q0[:, 0])}, {list(AO.y0[:, 0])}")
    if not (AO.q("NetIncomeLoss")[3, 0] == 40 and AO.q("NetIncomeLoss", 1)[3, 0] == 30 and AO.ttm("NetIncomeLoss")[3, 0] == 100 and AO.ttm("NetIncomeLoss")[4, 0] == 101
            and np.isnan(AO.q("NetIncomeLoss")[2, 0]) and AO.y("NetIncomeLoss")[3, 0] == 100 and np.isnan(AO.y("NetIncomeLoss")[2, 0]) and np.isnan(AO.ya("Assets")[3, 0])
            and np.isnan(AO.q("Yok")[3, 0]) and AO.i("Assets")[4, 0] == 104):
        hata.append("5) 'o gün bilinen' değerler (q, ttm, y, ya, i) yanlış")
    dv = K.k60_duyuru_gunu(np.array(["2015-05-10", "2015-08-09"], "datetime64[D]"), np.array(["2015-04-01", "2015-05-03", "2015-05-08", "2015-08-20"], "datetime64[D]"), 30)
    if list(dv.astype(str)) != ["2015-05-08", "2015-08-09"] or len(K.k60_duyuru_gunu(None, None, 30)) != 0:
        hata.append(f"5) açıklama günü vekili yanlış: {dv}")
    # 6) sinyal tanımları elle
    k = int(np.flatnonzero(np.asarray(me == pd.Timestamp("2018-06-29")))[0]); j = 30; p = int(mp[k]); t = P["mtD"][k]; A5, C5 = P["A5"], P["C5"]; r_ = pd.DataFrame(A5).pct_change(fill_method=None)
    C, V, H, L, O = D["C"], D["V"], D["H"], D["L"], D["O"]; ay_g = slice(int(mp[k - 1]) + 1, p + 1); rj = r_[j].to_numpy()

    def yakin(kod: str, deger: float, jj: int = j, kk: int = k, tol: float = 1e-9) -> None:
        x = Sd[kod][kk, jj]
        if not (np.isfinite(x) and np.isfinite(deger) and abs(x - deger) <= tol * max(1.0, abs(deger))) and not (np.isnan(x) and np.isnan(deger)):
            hata.append(f"6) {kod} elle hesapla aynı değil: {x} != {deger} (hisse {S[jj]}, ay {me[kk].date()})")
    if not U[k, j] or not U[k, 12] or not U[k, 13] or not U[k, 15] or U[k, 3] or U[k, 4] or U[k, 5]:
        hata.append("6) sınanan hisselerin uygunluğu beklenen gibi değil (3: fiyat < 2, 4: likit değil, 5: ters bölünmeden önce < 2)")
    yakin("MOM_12_1", A5[mp[k - 1], j] / A5[mp[k - 12], j] - 1); yakin("MOM_6_1", A5[mp[k - 1], j] / A5[mp[k - 6], j] - 1); yakin("MOM_INT_12_7", A5[mp[k - 6], j] / A5[mp[k - 12], j] - 1)
    yakin("STREV_1M", A5[p, j] / A5[mp[k - 1], j] - 1); yakin("LTREV_60_13", A5[mp[k - 12], j] / A5[mp[k - 60], j] - 1); yakin("SEAS_1", A5[mp[k - 11], j] / A5[mp[k - 12], j] - 1)
    yakin("SEAS_2_5", np.mean([A5[mp[k - a], j] / A5[mp[k - a - 1], j] - 1 for a in (23, 35, 47, 59)]))
    yakin("VOL_60D", r_[j].rolling(60, min_periods=40).std().iloc[p]); yakin("HIGH52", C5[p, j] / pd.Series(H[:, j]).rolling(252, min_periods=200).max().iloc[p])
    ra = rj[ay_g]; yakin("MAX5", np.sort(ra)[-5:].mean()); yakin("SKEW_TOT", ((ra - ra.mean()) ** 3).mean() / ((ra - ra.mean()) ** 2).mean() ** 1.5)
    fg = D["ff_gunluk"].to_numpy(); Xg = np.column_stack([np.ones(len(ra)), fg[ay_g, :3]]); yg = ra - fg[ay_g, 3]; eg = yg - Xg @ np.linalg.lstsq(Xg, yg, rcond=None)[0]
    yakin("IVOL_FF3", np.sqrt((eg ** 2).mean()), tol=1e-7); yakin("ISKEW", (eg ** 3).mean() / (eg ** 2).mean() ** 1.5, tol=1e-6)
    son252 = slice(p - 251, p + 1); yakin("AMIHUD", 1e6 * np.nanmean(np.abs(rj[son252]) / (C[son252, j] * V[son252, j])))
    yakin("DOLVOL", np.log(np.nanmean((C * V)[int(mp[k - 2]) + 1:int(mp[k - 1]) + 1, j]))); yakin("VOL_SHOCK", V[p - 4:p + 1, j].mean() / V[p - 54:p - 4, j].mean())
    yakin("GAP_OVN", np.log(O[ay_g, j] / C[int(mp[k - 1]):p, j]).sum()); yakin("PRICE_LVL", np.log(C5[p, j]))
    kcs = 3 - 2 * np.sqrt(2); sp = []
    for d_ in range(int(mp[k - 1]) + 1, p):
        be = np.log(H[d_, j] / L[d_, j]) ** 2 + np.log(H[d_ + 1, j] / L[d_ + 1, j]) ** 2; ga = np.log(max(H[d_, j], H[d_ + 1, j]) / min(L[d_, j], L[d_ + 1, j])) ** 2
        al = (np.sqrt(2 * be) - np.sqrt(be)) / kcs - np.sqrt(ga / kcs); sp.append(max(2 * (np.exp(al) - 1) / (1 + np.exp(al)), 0.0))
    yakin("SPREAD_CS", np.mean(sp), tol=1e-7)
    mkt = (D["ff_gunluk"].MKT_RF + D["ff_gunluk"].RF).to_numpy(); u_ = slice(p - 1259, p + 1); b_ = slice(p - 251, p + 1)
    yakin("BETA_BAB", np.corrcoef(rj[u_], mkt[u_])[0, 1] * rj[b_].std() / mkt[b_].std(), tol=1e-7)
    a_, c_ = int(mp[k - 12]) + 1, int(mp[k - 1]) + 1
    with np.errstate(invalid="ignore"):
        surek = np.array([np.sign(A5[mp[k - 1], x] / A5[mp[k - 12], x] - 1) * ((r_[x].to_numpy()[a_:c_] > 0).mean() - (r_[x].to_numpy()[a_:c_] < 0).mean()) for x in range(N)])
        mom = A5[mp[k - 1]] / A5[mp[k - 12]] - 1
    sira = lambda x: (pd.Series(np.where(U[k] & np.isfinite(x), x, nan)).rank() - 0.5) / (U[k] & np.isfinite(x)).sum()  # noqa: E731
    yakin("MOM_FIP", (sira(mom)[j] + sira(surek)[j]) / 2)
    fa = D["ff_aylik"].reindex(me.to_period("M")); rm_ = A5[mp[1:]] / A5[mp[:-1]] - 1; rm_ = np.vstack([np.full((1, N), nan), rm_])
    Xm = np.column_stack([np.ones(36), fa[["MKT_RF", "SMB", "HML"]].to_numpy()[k - 35:k + 1]]); ym = rm_[k - 35:k + 1, j] - fa.RF.to_numpy()[k - 35:k + 1]
    em = ym - Xm @ np.linalg.lstsq(Xm, ym, rcond=None)[0]; yakin("MOM_RES_12_1", em[24:35].sum() / em[24:35].std(ddof=1), tol=1e-7)
    Lg = E0["param"]["trend_gun"]; xl = lambda kk: np.column_stack([np.array([C5[mp[kk] - L_ + 1:mp[kk] + 1, x].mean() for x in range(N)]) / C5[mp[kk]] for L_ in Lg])  # noqa: E731
    kat = []
    for kk in range(k - 11, k + 1):
        Xk = xl(kk - 1); ok = P["U"][kk - 1] & np.isfinite(Xk).all(axis=1) & np.isfinite(rm_[kk])
        kat.append(np.linalg.lstsq(np.column_stack([np.ones(ok.sum()), Xk[ok]]), rm_[kk, ok], rcond=None)[0])
    yakin("TREND_MA", float(xl(k)[j] @ np.mean(kat, axis=0)[1:]), tol=1e-6)
    # temel: ç0 / y0 düz döngüyle
    q0 = elle_q0(T, t, j); TQ, TI, TY = T["Q"], T["I"], T["Y"]
    y0 = max(y for y in range(NY) if T["Ybilgi"][y, j] < t)
    if q0 != ek["q0"][k, j] or y0 != ek["y0"][k, j] or q0 < 12:
        hata.append(f"6) ç0 / y0 düz döngüyle aynı değil: {q0} / {ek['q0'][k, j]}, {y0} / {ek['y0'][k, j]}")

    def pay_elle(jj: int, tt: np.datetime64) -> float:
        d_, n_, b_ = T["pay"][jj]; bil = b_ < tt
        if not bil.any():
            return nan
        i = int(np.argmax(np.where(bil, d_.astype(np.int64), -10 ** 9)))
        return float(n_[i] * K59.k59_bolunme_carpan(D["bolunme"].get(S[jj]), np.array([d_[i]], "datetime64[ns]"))[0])
    SH = pay_elle(j, t); PD = C5[p, j] * SH; ni4 = TQ["NetIncomeLoss"][q0 - 3:q0 + 1, j].sum(); rev4 = TQ["Revenues"][q0 - 3:q0 + 1, j].sum(); oz = TI["StockholdersEquity"][q0, j]
    at = lambda q: TI["Assets"][q, j]  # noqa: E731
    yakin("SIZE_ME", np.log(PD)); yakin("BM", oz / PD); yakin("EP", ni4 / PD); yakin("SP", rev4 / PD); yakin("AM", at(q0) / PD); yakin("LEV_MKT", TI["Liabilities"][q0, j] / PD)
    yakin("ROE_TTM", ni4 / oz); yakin("ROA_Q", TQ["NetIncomeLoss"][q0, j] / at(q0 - 1)); yakin("ASSET_G", at(q0) / at(q0 - 4) - 1); yakin("BE_G", oz / TI["StockholdersEquity"][q0 - 4, j] - 1)
    yakin("SALES_ACCEL", TQ["Revenues"][q0, j] / ((TQ["Revenues"][q0 - 1, j] + TQ["Revenues"][q0 - 2, j]) / 2)); yakin("GP_A", TQ["GrossProfit"][q0 - 3:q0 + 1, j].sum() / at(q0))
    yakin("OP_BE", TQ["OperatingIncomeLoss"][q0 - 3:q0 + 1, j].sum() / oz); yakin("OPLEV", (rev4 - TQ["OperatingIncomeLoss"][q0 - 3:q0 + 1, j].sum()) / at(q0))
    yakin("D_ASSET_TURN", rev4 / at(q0) - TQ["Revenues"][q0 - 7:q0 - 3, j].sum() / at(q0 - 4)); yakin("TAX_CHG", (TQ["IncomeTaxExpenseBenefit"][q0, j] - TQ["IncomeTaxExpenseBenefit"][q0 - 4, j]) / at(q0 - 4))
    yakin("RD_ME", TQ["ResearchAndDevelopmentExpense"][q0 - 3:q0 + 1, j].sum() / PD)
    ltd = lambda q: TI["LongTermDebt"][q, j] if np.isfinite(TI["LongTermDebt"][q, j]) else TI["LongTermDebtNoncurrent"][q, j]  # noqa: E731
    nakit = TI["CashAndCashEquivalentsAtCarryingValue"][q0, j]; yakin("NOA", (ltd(q0) + oz - nakit) / at(q0 - 4)); yakin("NDF_BS", (ltd(q0) - ltd(q0 - 4)) / ((at(q0) + at(q0 - 4)) / 2))
    fk = np.array([TQ["NetIncomeLoss"][q0 - a, j] - TQ["NetIncomeLoss"][q0 - a - 4, j] for a in range(8)]); yakin("SUE_SRW", fk[0] / fk.std(ddof=1))
    fr = np.array([TQ["Revenues"][q0 - a, j] - TQ["Revenues"][q0 - a - 4, j] for a in range(8)]); yakin("REV_SURP", fr[0] / fr.std(ddof=1))
    n_ = 1
    while n_ < 8 and np.sign(fk[n_]) == np.sign(fk[0]):
        n_ += 1
    yakin("EARN_STREAK", np.sign(fk[0]) * n_)
    ocf = TY["NetCashProvidedByUsedInOperatingActivities"]; qy = lambda y: T["Yq"][y, j]  # noqa: E731
    yakin("CFP", ocf[y0, j] / PD); yakin("ACCRUALS", (TY["NetIncomeLoss"][y0, j] - ocf[y0, j]) / ((at(qy(y0)) + at(qy(y0 - 1))) / 2)); yakin("CBOP_A", ocf[y0, j] / at(qy(y0)))
    yakin("EV_EBITDA", (PD + ltd(q0) - nakit) / (TQ["OperatingIncomeLoss"][q0 - 3:q0 + 1, j].sum() + TY["DepreciationDepletionAndAmortization"][y0, j]))
    s0 = lambda x: 0.0 if np.isnan(x) else float(x)  # noqa: E731
    tem_, geri_, ihr_ = (s0(TY[a][y0, j]) for a in ("PaymentsOfDividends", "PaymentsForRepurchaseOfCommonStock", "ProceedsFromIssuanceOfCommonStock"))
    yakin("NET_PAYOUT_YLD", (tem_ + geri_ - ihr_) / PD); yakin("BUYBACK_YLD", geri_ / PD); yakin("NEF", (ihr_ - geri_ - tem_) / ((at(qy(y0)) + at(qy(y0 - 1))) / 2))
    cx = TY["PaymentsToAcquirePropertyPlantAndEquipment"]; yakin("CAPEX_G", cx[y0, j] / ((cx[y0 - 1, j] + cx[y0 - 2, j]) / 2) - 1); yakin("RUNWAY", -ocf[y0, j] / nakit)
    yakin("NSI_1Y", np.log(SH / pay_elle(j, P["mtD"][k - 12]))); yakin("NSI_5Y", np.log(SH / pay_elle(j, P["mtD"][k - 60])))
    yakin("TURN_12M", np.nanmean(V[son252, j]) / SH)
    oh = E0["param"]["ohlson"]; TA = at(qy(y0)); TL = TI["Liabilities"][qy(y0), j]; CA, CL = TI["AssetsCurrent"][qy(y0), j], TI["LiabilitiesCurrent"][qy(y0), j]; n0, n1 = TY["NetIncomeLoss"][y0, j], TY["NetIncomeLoss"][y0 - 1, j]
    yakin("O_SCORE", oh["sabit"] + oh["lnTA"] * np.log(TA) + oh["TLTA"] * TL / TA + oh["WCTA"] * (CA - CL) / TA + oh["CLCA"] * CL / CA + oh["OENEG"] * float(TL > TA) + oh["NITA"] * n0 / TA
          + oh["FUTL"] * ocf[y0, j] / TL + oh["INTWO"] * float(n0 < 0 and n1 < 0) + oh["CHIN"] * (n0 - n1) / (abs(n0) + abs(n1)))
    fo = []
    for y in (y0, y0 - 1):
        a_y = at(qy(y)); fo.append({"roa": TY["NetIncomeLoss"][y, j] / a_y, "kal": s0(ltd(qy(y))) / a_y, "cari": TI["AssetsCurrent"][qy(y), j] / TI["LiabilitiesCurrent"][qy(y), j],
                                    "bm": TY["GrossProfit"][y, j] / TY["Revenues"][y, j], "dv": TY["Revenues"][y, j] / a_y})
    fsk = sum([fo[0]["roa"] > 0, ocf[y0, j] > 0, fo[0]["roa"] > fo[1]["roa"], ocf[y0, j] > TY["NetIncomeLoss"][y0, j], fo[0]["kal"] < fo[1]["kal"], fo[0]["cari"] > fo[1]["cari"],
               not ihr_ > 0, fo[0]["bm"] > fo[1]["bm"], fo[0]["dv"] > fo[1]["dv"]])
    yakin("F_SCORE", fsk + 0.001 * np.clip(fo[0]["roa"], -1, 1))
    # özel hisseler: 12 (yalnız toplam pasif), 13 (yükümlülük yok), 7 (eksi özkaynak), 15 (kapak sayısı yok), 8 (eksik çeyrek), 6 / 5 (bölünme)
    q12 = elle_q0(T, t, 12); yakin("AM", TI["LiabilitiesAndStockholdersEquity"][q12, 12] / (C5[p, 12] * pay_elle(12, t)), 12)
    q13 = elle_q0(T, t, 13); yakin("LEV_MKT", (TI["Assets"][q13, 13] - TI["StockholdersEquity"][q13, 13]) / (C5[p, 13] * pay_elle(13, t)), 13)
    if U[k, 7] and (np.isfinite(Sd["BM"][k, 7]) or np.isfinite(Sd["ROE_TTM"][k, 7]) or np.isfinite(Sd["OP_BE"][k, 7])):
        hata.append("6) eksi özkaynakta BM / ROE / OP_BE hesaplanmamalıydı")
    if ek["pay_kaynak"][k, 15] != 2 or ek["pay_kaynak"][k, j] != 1 or abs(Sd["SIZE_ME"][k, 15] - np.log(C5[p, 15] * 1.0e7)) > 1e-9:
        hata.append("6) kapak sayısı olmayan (bölünmesiz) hissede bilanço pay sayısı yedeği kullanılmadı")
    D15 = kopya(D); D15["bolunme"][S[15]] = (np.array([np.datetime64("2012-05-01")], "datetime64[ns]"), np.array([2.0]))
    if np.isfinite(K.k60_pay(D15, P, K._K60Temel(T, P["mtD"], N, E0["bilgi"]), E0)[0][:, 15]).any():
        hata.append("6) bölünmesi olan hissede yedek pay sayısı kullanıldı (kural: yalnız bölünmesizlerde)")
    k8 = [kk for kk in range(60, M - 1) if U[kk, 8] and np.isnan(Sd["ROE_TTM"][kk, 8])]
    if not k8 or not np.isfinite(Sd["ROE_TTM"][:, 8]).any():
        hata.append("6) eksik çeyrek kârı olan hissede 4 çeyrek toplamı bazı aylarda NaN olmalıydı")
    for jj, b in ((6, 1.02), (5, 1.0)):
        kk = [x for x in range(M - 1) if U[x, jj] and me[x] > pd.Timestamp("2019-09-30") and me[x] < pd.Timestamp("2020-03-31")]
        if not kk or abs(Sd["NSI_1Y"][kk[0], jj] - 4 * np.log(b)) > 1e-9:
            hata.append(f"6) bölünmeyi aşan NSI_1Y yalnız gerçek ihracı göstermeliydi (hisse {jj}): {Sd['NSI_1Y'][kk[0], jj] if kk else None}")
    kb = int(np.flatnonzero(np.asarray(me == pd.Timestamp("2018-12-31")))[0])
    if Sd["E_SPLIT"][kb, 6] != 1 or Sd["E_SPLIT"][kb - 6, 6] != 0 or Sd["E_RSPLIT"][int(np.flatnonzero(np.asarray(me == pd.Timestamp("2019-12-31")))[0]), 5] != 1 or np.nanmax(Sd["E_RSPLIT"][:, 6]) != 0:
        hata.append("6) E_SPLIT / E_RSPLIT bayrakları yanlış")
    # olaylar
    gD = P["gunD"]; don = np.union1d(D["basvuru"]["K"][j], D["basvuru"]["Q"][j]); f_ = don[don < t][-1]; mk_ = mkt

    def tepki_elle(gn: np.datetime64) -> float:
        p0 = int(np.searchsorted(gD, gn)); return A5[p0 + 1, j] / A5[p0 - 2, j] - 1 - ((1 + mk_[p0 - 1]) * (1 + mk_[p0]) * (1 + mk_[p0 + 1]) - 1)
    p0f = int(np.searchsorted(gD, f_)); yakin("EAR_FILE", tepki_elle(f_) if p0f + 1 > p - 63 else nan)
    s8 = D["basvuru"]["8K"][j]; ad8 = s8[(s8 <= f_) & (s8 >= f_ - np.timedelta64(30, "D"))]; dstar = ad8[-1] if len(ad8) else f_; p0d = int(np.searchsorted(gD, dstar))
    yakin("EAR_ANN", tepki_elle(dstar) if p0d + 1 > p - 63 else nan); yakin("EAR_VOL", V[p0d, j] / V[p0d - 50:p0d, j].mean() if p0d + 1 > p - 63 else nan)
    for kk in range(k - 3, k + 1):
        hedef = (me[kk].to_period("M") + 1 - 12); dvs = K.k60_duyuru_gunu(don, s8, 30)
        yakin("EA_MONTH", float(any(pd.Timestamp(x).to_period("M") == hedef for x in dvs)), j, kk)
        jt = 29; yakin("DIV_MONTH", float((me[kk].month + 1 - 1) % 12 + 1 in (2, 5, 8, 11)), jt, kk); yakin("DIV_MONTH", 0.0, j, kk)
    for kod, grp, jj in (("NT_LATE", "NT", 3 + 7 * 4), ("E_S3", "S3", 30), ("E_424B5", "424B5", 30), ("ACT_13D", "13D", 31), ("E_TENDER_SELF", "TOI", 32)):
        w = np.timedelta64(E0["param"]["bayrak_gun"][kod], "D"); x = D["basvuru"][grp][jj]
        for kk in range(k - 5, k + 1):
            tt = P["mtD"][kk]; yakin(kod, float(x is not None and ((x >= tt - w) & (x < tt)).any()), jj, kk)
    if not np.isnan(Sd["NT_LATE"][k, 10]) if U[k, 10] else False:
        hata.append("6) CIK'i olmayan hissede başvuru bayrağı NaN olmalıydı")
    ko = int(np.flatnonzero(np.asarray(me == pd.Timestamp("2020-06-30")))[0]); ki = int(np.flatnonzero(np.asarray(me == pd.Timestamp("2017-01-31")))[0])
    if not (Sd["E_DIV_OMIT"][ko, 13] == 1 and Sd["E_DIV_OMIT"][ki, 13] == 0 and Sd["E_DIV_INIT"][ki, 25] == 1 and Sd["E_DIV_INIT"][ko, 25] == 0 and Sd["E_DIV_INIT"][ki, 29] == 0 and Sd["E_DIV_OMIT"][ko, j] == 0):
        hata.append("6) E_DIV_INIT / E_DIV_OMIT bayrakları yanlış")
    j9 = 18; ipo = D["ilk_islem"][j9]; ki_ = [kk for kk in range(M - 1) if U[kk, j9]]
    if not ki_ or any(Sd["E_IPO_3Y"][kk, j9] != float((P["mtD"][kk] - ipo) <= np.timedelta64(1095, "D")) for kk in ki_) or np.nanmax(Sd["E_IPO_3Y"][:, j]) != 0:
        hata.append("6) E_IPO_3Y bayrağı yanlış")
    s2 = D["sic"] // 100; ayni = U[k] & (s2 == s2[j]) & (D["sic"] >= 0); g6 = A5[p] / A5[mp[k - 6]] - 1
    yakin("IND_MOM_6", g6[ayni & np.isfinite(g6)].mean() if (ayni & np.isfinite(g6)).sum() >= 5 else nan)
    PDo = ek["PD"][k - 1]; rmk = A5[p] / A5[mp[k - 1]] - 1; sinanan = 0
    for jj in range(N):
        grp = np.flatnonzero(U[k] & (s2 == s2[jj]) & (D["sic"] >= 0) & np.isfinite(PDo) & np.isfinite(rmk))
        if not U[k, jj] or D["sic"][jj] < 0:
            continue
        if len(grp) < 10 or jj not in grp:
            bek = nan
        else:
            buyuk = grp[np.argsort(-PDo[grp], kind="stable")][:max(1, int(round(0.3 * len(grp))))]; bek = nan if jj in buyuk else float(rmk[buyuk].mean()); sinanan += int(np.isfinite(bek))
        yakin("IND_LEAD_BIG", bek, jj)
    if sinanan < 10:
        hata.append(f"6) IND_LEAD_BIG elle sınaması boş kaldı ({sinanan} hisse)")
    # bileşik: üyelerin yönlü yüzdelik sıra ortalaması
    uy_ = E0["bilesik"]["AILE_VAL"]["uye"]; sr = np.array([sira((-1.0 if tn[u]["yon"] == "-" else 1.0) * Sd[u][k])[j] for u in uy_])
    yakin("AILE_VAL", float(np.nanmean(sr)) if np.isfinite(sr).sum() >= E0["bilesik"]["AILE_VAL"]["min"] else nan)
    c4 = np.array([sira((-1.0 if tn[u]["yon"] == "-" else 1.0) * Sd[u][k])[j] for u in E0["bilesik"]["COMP4"]["uye"]]); yakin("COMP4", float(np.nanmean(c4)) if np.isfinite(c4).sum() >= 3 else nan)
    if E0["bilesik"]["COMP4"] != {"ad": E0["bilesik"]["COMP4"]["ad"], "uye": ["MOM_12_1", "EAR_ANN", "ROE_TTM", "NSI_1Y"], "min": 3, "rol": "K59"} or E0["bilesik"]["DOSYA_Y"]["min"] != 4 \
            or E0["bilesik"]["DOSYA_Y"]["uye"] != ["SALES_ACCEL", "REV_YOY", "ROE_TTM", "NSI_1Y", "EAR_ANN"]:
        hata.append("6) COMP4 / DOSYA_Y üyeleri K59 eşlemesiyle aynı değil")
    ry = TQ["Revenues"][q0, j] / TQ["Revenues"][q0 - 4, j] - 1
    if abs(ek["bilesen"]["REV_YOY"][k, j] - ry) > 1e-9:
        hata.append("6) REV_YOY bileşeni elle hesapla aynı değil")
    if np.isfinite(Sd["BM"][~U]).any() or any(np.isfinite(Sd[x][~U]).any() for x in ("MOM_12_1", "AILE_MOM", "E_S3")):
        hata.append("6) uygun olmayan hisse-ayda sinyal değeri var")
    # 7) panel K59 ile aynı; R1 = K59 cetveli; ileri getiri penceresi; dönemler
    V59 = {}
    for jj, s in enumerate(S):
        v = np.isfinite(D["C"][:, jj])
        V59[s] = pd.DataFrame({"Open": D["O"][v, jj], "High": D["H"][v, jj], "Low": D["L"][v, jj], "Close": D["A"][v, jj], "Volume": D["V"][v, jj]}, index=gun[v])
    ev59 = {"ad": "sentetik", "kaynak": "K57B_YAHOO", "rol": "KARAR", "bas": "2010-01-01", "kes": "2026-08-31", "fiyat_min": 2.0, "likit_min": 1.0e6, "maliyet": 0.001, "min_evren": 30,
            "min_sinyal": 20, "boyut": "piyasa_degeri", "sinyal": [], "french": False}
    P59 = K59.k59_panel({"ad": "U2", "evren": ev59, "V": V59, "ham": pd.DataFrame(D["C"], index=gun, columns=S), "bolunme": D["bolunme"]}, K59.K59_ESIK)
    if not (list(P59["ay_sonu"]) == list(me) and np.array_equal(P59["U"], U) and np.allclose(P59["R"], P["R"], equal_nan=True, rtol=1e-12) and np.array_equal(P59["olusum"], P["olusum"])
            and np.allclose(P59["fiyat_o"], P["fiyat_o"], equal_nan=True)):
        hata.append("7) K60 paneli (ay sonları, uygun evren, 1 ay getirisi, o günkü fiyat) K59 k59_panel ile aynı değil")
    bag = K.k60_bag(U.shape, Et); pm = K.k60_donem_aylari(P, "kesif", 1, Et); E59 = copy.deepcopy(K59.K59_ESIK)
    Pm = {"evren": {"maliyet": 0.001, "min_sinyal": 20, "french": False}, "U": U, "R": P["R"], "olusum": pm, "ay_sonu": me}
    for kod, isaret in (("MOM_12_1", 1.0), ("VOL_60D", -1.0), ("ROE_TTM", 1.0), ("LTREV_60_13", -1.0)):
        r59, A59 = K59.k59_sinyal_olc(Pm, isaret * Sd[kod], None, E59)
        uc = K.k60_uclar(Sd[kod], tn[kod]["yon"], "surekli", P, bag, Et)["UST"]; ol = K.k60_olcum_aylari(pm, uc["say"], 20, "surekli"); r60, A60 = K.k60_r1(P, uc["sec"], ol, "kesif", None, Et)
        for a in ("ay", "yillik_fazla", "nw_t", "alfa_yillik", "beta", "t_alfa", "tutar_v2", "brut_yillik_fazla", "brut_t_alfa", "ort_devir", "alt1", "alt2", "alt3", "son30", "ilk_ay"):
            if r59[a] != r60[a] and not (isinstance(r59[a], float) and abs(r59[a] - r60[a]) < 1e-12):
                hata.append(f"7) R1 K59 k59_sinyal_olc ile aynı değil: {kod} {a} {r59[a]} != {r60[a]}")
        if not np.array_equal(A59.net.to_numpy(), A60.net.to_numpy()) or abs(r60["p_alfa"] - 2 * K._k60_norm_p(abs(r60["t_alfa"]))) > 1e-15:
            hata.append(f"7) R1 aylık serisi K59 ile aynı değil / p değeri yanlış: {kod}")
    if not (pm.sum() == 120 and str(me[pm][0].date()) == "2012-01-31" and str(me[pm][-1].date()) == "2021-12-31" and K.k60_donem_aylari(P, "dogrulama", 1, Et).sum() == 24
            and [int(K.k60_donem_aylari(P, "kasa", h, Et).sum()) for h in (1, 3, 6, 12)] == [31, 29, 26, 20] and str(me[K.k60_donem_aylari(P, "kasa", 12, Et)][-1].date()) == "2025-08-29"
            and str(me[K.k60_donem_aylari(P, "kasa", 1, Et)][-1].date()) == "2026-07-31" and K.k60_donem_aylari(P, "kesif", 12, Et).sum() == 120):
        hata.append("7) dönemin oluşum ayları yanlış (KEŞİF 120, DOĞRULAMA 24, KASA 1 / 3 / 6 / 12 ay = 31 / 29 / 26 / 20; penceresi kesiği aşan ay düşmeli)")
    if any((K.k60_donem_aylari(P, a, 1, Et) & K.k60_donem_aylari(P, b, 1, Et)).any() for a, b in (("kesif", "dogrulama"), ("dogrulama", "kasa"), ("kesif", "kasa"))):
        hata.append("7) dönemler örtüşüyor")
    F12 = P["F"][12]; kk = k; jj = j
    if abs(F12[kk, jj] - (P["A5"][mp[kk + 12], jj] / P["A5"][mp[kk], jj] - 1)) > 1e-12 or abs(P["F"][3][kk, jj] - (P["A5"][mp[kk + 3], jj] / P["A5"][mp[kk], jj] - 1)) > 1e-12 \
            or abs(P["R"][kk, jj] - (P["A5"][mp[kk + 1], jj] / P["A5"][mp[kk], jj] - 1)) > 1e-12 or np.isfinite(F12[M - 12:]).any() or np.isfinite(P["F"][6][M - 6:]).any() or np.isfinite(P["R"][M - 1]).any():
        hata.append("7) ileri getiri tanımı yanlış (F_h = A(m+h) / A(m) - 1; son h ayda tanımsız)")
    Dg1 = boz(D, me[kk + 12]); Pg1 = K.k60_panel(Dg1, Et, True); Dg2 = boz(D, me[kk + 11]); Pg2 = K.k60_panel(Dg2, Et, True)
    if not esit(Pg1["F"][12][:kk + 1], F12[:kk + 1]) or not esit(Pg1["R"][:kk + 12], P["R"][:kk + 12]) or esit(Pg2["F"][12][kk], F12[kk]) or not esit(Pg2["F"][12][:kk], F12[:kk]) \
            or esit(Pg1["F"][12][kk + 1], F12[kk + 1]):
        hata.append("7) 12 aylık ileri getiri yalnız m+1 .. m+12 aylarını kullanmalı (m+12'den sonrası bozulunca değişmemeli, m+12 bozulunca değişmeli)")
    Dn = kopya(D); Dn["A"][mp[kk + 12] - 6:mp[kk + 12] + 1, jj] = np.nan; Dn["C"][mp[kk + 12] - 6:mp[kk + 12] + 1, jj] = np.nan; Pn = K.k60_panel(Dn, Et, True)
    if np.isfinite(Pn["F"][12][kk, jj]) or not np.isfinite(Pn["F"][12][kk, jj + 1]):
        hata.append("7) m+12 ay sonunda taze fiyatı olmayan hisse-ayın ileri getirisi NaN olmalıydı")
    Dz = kopya(D); Dz["A"][100:110, jj] = 0.0; Pz = K.k60_panel(Dz, Et, True)
    if np.isfinite(Pz["A5"][105:110, jj]).any() or not np.isfinite(Pz["A5"][100:105, jj]).all() or np.isinf(K._k60_sinyal_fiyat(Dz, Pz, Et)[0]["MOM_12_1"]).any():
        hata.append("7) düzeltilmiş kapanışı <= 0 olan gün yok sayılmalıydı")
    Pk = K.k60_panel(D, Et, getiri=False)
    if Pk["R"] is not None or Pk["F"] or not np.array_equal(Pk["U"], U):
        hata.append("7) getiri=False panelde ileri getiri hesaplandı / evren değişti")
    # 8) uçlar, bayrak, eşitlik bozma, ölçüm ayları
    uc = K.k60_uclar(Sd["BM"], "+", "surekli", P, bag, Et); ue = U[k] & np.isfinite(Sd["BM"][k]); nn = int(ue.sum()); mm = max(1, int(round(0.1 * nn)))
    sirali = np.flatnonzero(ue)[np.argsort(Sd["BM"][k][ue])]
    if set(np.flatnonzero(uc["UST"]["sec"][k])) != set(sirali[-mm:]) or set(np.flatnonzero(uc["ALT"]["sec"][k])) != set(sirali[:mm]) or uc["UST"]["say"][k] != nn or uc["UST"]["min"] != 20:
        hata.append("8) sürekli sinyalin ÜST / ALT ucu en yüksek / en düşük %10 değil")
    ue_ = K.k60_uclar(Sd["VOL_60D"], "-", "surekli", P, bag, Et); uv = U[k] & np.isfinite(Sd["VOL_60D"][k]); sv = np.flatnonzero(uv)[np.argsort(Sd["VOL_60D"][k][uv])]
    if set(np.flatnonzero(ue_["UST"]["sec"][k])) != set(sv[:max(1, int(round(0.1 * uv.sum())))]):
        hata.append("8) eksi yönlü sinyalde ÜST uç en DÜŞÜK değerler olmalıydı")
    ub = K.k60_uclar(Sd["E_S3"], "-", "bayrak", P, bag, Et); ub2 = K.k60_uclar(Sd["DIV_MONTH"], "+", "bayrak", P, bag, Et)
    if list(ub) != ["ALT"] or list(ub2) != ["UST"] or not np.array_equal(ub["ALT"]["sec"], U & (np.nan_to_num(Sd["E_S3"]) > 0.5)) or ub["ALT"]["min"] != 3 or ub["ALT"]["tur"] != "bayrak":
        hata.append("8) bayrak sinyalinde uç = bayraklı uygun hisseler ('-' ALT, '+' ÜST) olmalıydı")
    Seq = np.where(U, 1.0, nan); u1 = K.k60_uclar(Seq, "+", "surekli", P, bag, Et); u2 = K.k60_uclar(Seq, "+", "surekli", P, K.k60_bag(U.shape, Et), Et)
    beklenen = np.flatnonzero(U[k])[np.argsort(bag[k][U[k]])]; nu = int(U[k].sum()); mu_ = max(1, int(round(0.1 * nu)))
    if not np.array_equal(u1["UST"]["sec"], u2["UST"]["sec"]) or set(np.flatnonzero(u1["UST"]["sec"][k])) != set(beklenen[-mu_:]) or (u1["UST"]["sec"][k] & u1["ALT"]["sec"][k]).any() \
            or set(np.flatnonzero(u1["UST"]["sec"][k])) == set(np.flatnonzero(U[k])[:mu_]):
        hata.append("8) eşitlik bozma sabit tohumlu rastgele sırayla yapılmıyor (kod sırası / tekrar üretilemez)")
    pm_ = np.zeros(10, bool); pm_[2:9] = True; sy = np.array([50, 50, 5, 5, 30, 4, 30, 30, 2, 50])
    if list(K.k60_olcum_aylari(pm_, sy, 20, "surekli")) != [False] * 4 + [True] * 5 + [False] or list(np.flatnonzero(K.k60_olcum_aylari(pm_, sy, 20, "bayrak"))) != [4, 6, 7] \
            or K.k60_olcum_aylari(pm_, sy * 0, 20, "surekli").any():
        hata.append("8) ölçüm ayları kuralı yanlış (sürekli: ilk yeterli aydan dönem sonuna; bayrak: yalnız yeterli aylar)")
    # 9) lift elle, blok bootstrap, R2 elle
    kd, nd, kb, nb = np.array([1, 0, 2, 1, 0, 3.0]), np.array([10, 10, 10, 10, 10, 10.0]), np.array([4, 2, 6, 5, 1, 9.0]), np.array([100, 100, 100, 100, 100, 100.0])
    Eb = test_esik(r2={"blok": 2, "cekilis": 400}); L1 = K.k60_lift(kd, nd, kb, nb, Eb); L2 = K.k60_lift(kd, nd, kb, nb, Eb)
    if abs(L1["P"] - 7 / 60) > 1e-15 or abs(L1["taban"] - 27 / 600) > 1e-15 or abs(L1["lift"] - (7 / 60) / (27 / 600)) > 1e-12 or L1 != L2:
        hata.append(f"9) lift elle hesapla aynı değil / tekrar üretilemiyor: {L1}")
    ix = K.k60_blok_dizini(6, Eb); Lb = (kd[ix].sum(1) / nd[ix].sum(1)) / (kb[ix].sum(1) / nb[ix].sum(1))
    if ix.shape != (400, 6) or ix.min() < 0 or ix.max() > 5 or not ((ix[:, 1] - ix[:, 0]) % 6 == 1).all() or not ((ix[:, 3] - ix[:, 2]) % 6 == 1).all() or len(np.unique(ix[:, 0])) != 6 \
            or not np.array_equal(ix, K.k60_blok_dizini(6, Eb)) or np.array_equal(ix, K.k60_blok_dizini(6, test_esik(r2={"blok": 2, "cekilis": 400, "tohum": 7}))):
        hata.append("9) blok bootstrap dizini (dairesel, ardışık bloklar, tohumla birebir) yanlış")
    if abs(L1["alt"] - np.percentile(Lb, 2.5)) > 1e-12 or abs(L1["ust"] - np.percentile(Lb, 97.5)) > 1e-12 or abs(L1["py"] - (1 + (Lb <= 1).sum()) / 401) > 1e-15 \
            or abs(L1["z"] - np.log(L1["lift"]) / np.log(Lb).std(ddof=1)) > 1e-12 or abs(L1["pz"] - K._k60_norm_p(L1["z"])) > 1e-15 or abs(K._k60_norm_p(1.6448536269514722) - 0.05) > 1e-9:
        hata.append("9) lift aralığı / yüzdelik p / z p'si elle hesapla aynı değil")
    if K.k60_blok_dizini(20, E0).shape != (500, 20) or not ((np.diff(K.k60_blok_dizini(20, E0)[:, :12], axis=1) % 20) == 1).all():
        hata.append("9) varsayılan bootstrap (blok 12 ay, 500 çekiliş) dizini yanlış")
    sfr = K.k60_lift(np.zeros(6), nd, kb, nb, Eb); bos_ = K.k60_lift(kd, nd, np.zeros(6), nb, Eb)
    if sfr["lift"] != 0 or sfr["pz"] != 1.0 or np.isfinite(bos_["lift"]):
        hata.append("9) olaysız uç (lift 0, p 1) / olaysız evren (lift tanımsız) yanlış")
    ucb = K.k60_uclar(Sd["BM"], "+", "surekli", P, bag, Et)["UST"]; olb = K.k60_olcum_aylari(pm, ucb["say"], 20, "surekli"); sat2, A2 = K.k60_r2(P, ucb["sec"], olb, Et)
    for h, row in zip((12, 6, 3), sat2):
        F = P["F"][h]; nde = nbe = kde = kbe = 0; fd = []; fb = []; ays = 0; kme = 0
        for m_ in np.flatnonzero(olb):
            if m_ + h > M - 1:
                continue
            ays += 1
            for x in range(N):
                if U[m_, x] and np.isfinite(F[m_, x]):
                    nbe += 1; kbe += F[m_, x] >= 1.0; fb.append(F[m_, x])
                    if ucb["sec"][m_, x]:
                        nde += 1; kde += F[m_, x] >= 1.0; kme += F[m_, x] <= -0.5; fd.append(F[m_, x])
        if not (row["ufuk"] == h and row["ay"] == ays and row["n"] == nde and row["n_evren"] == nbe and abs(row["P_p100"] - kde / nde) < 1e-15 and abs(row["taban_p100"] - kbe / nbe) < 1e-15
                and abs(row["lift_p100"] - (kde / nde) / (kbe / nbe)) < 1e-12 and abs(row["P_m50"] - kme / nde) < 1e-15 and abs(row["ort"] - np.mean(fd)) < 1e-12 and abs(row["medyan"] - np.median(fd)) < 1e-12
                and abs(row["taban_ort"] - np.mean(fb)) < 1e-12 and row["alt_p100"] <= row["lift_p100"] * 1.5 and row["olculdu"]):
            hata.append(f"9) R2 satırı düz döngüyle aynı değil (ufuk {h})")
    if list(A2.columns) != ["ay_sonu", "n", "n_evren", "k_p100", "k_evren_p100", "k_p50", "k_evren_p50", "k_m50", "k_evren_m50"] or len(A2) != sat2[0]["ay"] \
            or abs(A2.k_p100.sum() / A2.n.sum() - sat2[0]["P_p100"]) > 1e-15 or abs(K.k60_lift(A2.k_p100, A2.n, A2.k_evren_p100, A2.n_evren, Et)["alt"] - sat2[0]["alt_p100"]) > 1e-15:
        hata.append("9) R2 aylık sayım tablosundan satır yeniden üretilemiyor")
    # 10) BH: elle örnek + kaba kuvvet
    pv = np.array([0.001, 0.008, 0.039, 0.041, 0.042, 0.059, 0.074, 0.205, 0.212, 0.216])     # q = 0,05 -> 2; q = 0,10 -> 6 (p6 = 0,059 <= 0,06); q = 0,25 -> 10
    if list(K.k60_bh(pv, 0.05)) != [True, True] + [False] * 8 or list(K.k60_bh(pv[::-1], 0.10)) != [False] * 4 + [True] * 6 or K.k60_bh(pv, 0.25).sum() != 10 or K.k60_bh([nan, 0.04, nan], 0.05).tolist() != [False, True, False] \
            or K.k60_bh([0.03, 0.04], 0.05).tolist() != [True, True] or K.k60_bh([], 0.1).tolist() != [] or K.k60_bh([0.2, 0.9], 0.1).any():
        hata.append("10) Benjamini-Hochberg elle örnekle aynı değil")
    rg = np.random.default_rng(3)
    for _ in range(50):
        x = rg.random(17) ** 3; x[rg.random(17) < 0.1] = nan; q = 0.1; g_ix = np.flatnonzero(np.isfinite(x)); s_ = np.sort(x[g_ix]); kmax = 0
        for i_ in range(len(s_)):
            if s_[i_] <= (i_ + 1) / len(s_) * q:
                kmax = i_ + 1
        bek = np.zeros(17, bool); bek[g_ix] = x[g_ix] <= (s_[kmax - 1] if kmax else -1)
        if not np.array_equal(K.k60_bh(x, q), bek):
            hata.append("10) Benjamini-Hochberg kaba kuvvetle aynı değil"); break
    # 11) plasebo tohumla birebir; 'en büyük' eşiği
    Ep = test_esik(coklu={"plasebo_n": 6}); Pl1 = K.k60_plasebo(P, "dogrulama", Ep); Pl2 = K.k60_plasebo(P, "dogrulama", Ep); Pl3 = K.k60_plasebo(P, "dogrulama", test_esik(coklu={"plasebo_n": 6, "plasebo_tohum": 5}))
    if len(Pl1) != 6 or not Pl1.equals(Pl2) or Pl1.t_alfa.equals(Pl3.t_alfa) or not {"t_alfa", "brut_t_alfa", "tutar_v2", "brut_tutar_v2", "r2_lift_p100", "r2_alt_p100", "r2_lift_m50", "r2_alt_m50"} <= set(Pl1.columns):
        hata.append("11) plasebo tohumla tekrar üretilemiyor / tohum değişince değişmiyor / sütun eksik")
    rngp = np.random.default_rng(E0["coklu"]["plasebo_tohum"] + 2); Sp = rngp.random(U.shape); Sp[~U] = nan; secp = K58.k58_ust_dilim(Sp, U, 0.1)
    rp, _a = K.k60_r1(P, secp, K.k60_donem_aylari(P, "dogrulama", 1, Et), "dogrulama", None, Et)
    if abs(rp["t_alfa"] - Pl1.t_alfa[2]) > 1e-12:
        hata.append("11) plasebo i = default_rng(tohum + i) rastgele sırasının ÜST %10'u değil")
    xs = np.arange(200.0)
    if K.k60_plasebo_maks(xs, 5000, E0) != 199.0 or abs(K.k60_plasebo_maks(xs, 1, E0) - 189) > 12 or K.k60_plasebo_maks(xs, 90, E0) != K.k60_plasebo_maks(xs, 90, E0) or not np.isnan(K.k60_plasebo_maks([nan], 5, E0)) \
            or not (K.k60_plasebo_maks(xs, 1, E0) < K.k60_plasebo_maks(xs, 10, E0) <= K.k60_plasebo_maks(xs, 90, E0) <= 199):
        hata.append("11) plasebo en büyüğü eşiği yanlış")
    # 12) seçim, geçiş, etiket kuralları (elle kurulmuş tablolar)
    Es = test_esik(coklu={"plasebo_n": 40}); npl = 40
    Plx = pd.DataFrame({"t_alfa": np.linspace(-2.5, 1.5, npl), "brut_t_alfa": np.linspace(-2.0, 2.0, npl), "tutar_v2": False, "brut_tutar_v2": [True] + [False] * (npl - 1),
                        "r2_lift_p100": np.linspace(0.8, 1.2, npl), "r2_alt_p100": 0.7, "r2_lift_m50": np.linspace(0.7, 1.3, npl), "r2_alt_m50": 0.6})
    sat = lambda s, t, **kw: {"sinyal": s, "taraf": t, "aile_r1": True, "olculdu": True, "t_alfa": 0.0, "p_alfa": 1.0, "brut_t_alfa": 0.0, **kw}  # noqa: E731
    R1x = pd.DataFrame([sat("A", "UST", t_alfa=4.0, p_alfa=6e-5, brut_t_alfa=4.2), sat("B", "UST", t_alfa=2.6, p_alfa=0.0093, brut_t_alfa=2.8), sat("C", "UST", t_alfa=1.2, p_alfa=0.23, brut_t_alfa=1.4),
                        sat("D", "ALT", t_alfa=-3.4, p_alfa=7e-4, brut_t_alfa=-3.1), sat("E", "UST", t_alfa=-3.3, p_alfa=1e-3, brut_t_alfa=-1.0), sat("F", "UST", t_alfa=5.0, p_alfa=1e-6, olculdu=False),
                        sat("G", "ALT", t_alfa=6.0, p_alfa=1e-8, aile_r1=False), sat("H", "ALT", t_alfa=-2.6, p_alfa=0.0093, brut_t_alfa=-2.4)] + [sat(f"Z{i}", "UST") for i in range(12)])
    s2 = lambda s, t, **kw: {"sinyal": s, "taraf": t, "ufuk": 12, "aile_r2": True, "olculdu": True, "lift_p100": 1.0, "pz_p100": 0.5, "lift_m50": 1.0, "pz_m50": 0.5, **kw}  # noqa: E731
    R2x = pd.DataFrame([s2("A", "UST", lift_p100=1.6, pz_p100=1e-6), s2("B", "UST", lift_p100=1.15, pz_p100=1e-5), s2("C", "ALT", lift_m50=1.9, pz_m50=1e-7), s2("C", "UST", lift_p100=1.5, pz_p100=0.04),
                        s2("K", "UST", lift_p100=3.0, pz_p100=1e-9, olculdu=False), {**s2("A", "UST", lift_p100=9.0, pz_p100=1e-9), "ufuk": 6}] + [s2(f"Z{i}", "UST") for i in range(12)])
    Sc = K.k60_secim(R1x, R2x, Plx, Es); es = Sc["esik"]; sc = {(x["sinyal"], x["taraf"]): x for x in Sc["secili"]}
    if not (es["m_r1"] == 18 and es["m_r2"] == 16 and abs(es["yp_brut"] - 1 / npl) < 1e-12 and es["r1_acik"] and 1.8 < es["t_arti"] <= 2.0 and 1.8 < es["t_eksi_brut"] <= 2.0 and 1.15 < es["lift_p100"] <= 1.2):
        hata.append(f"12) seçim eşikleri yanlış: {es}")
    if sc.get(("A", "UST"), {}).get("yol") != ["R1", "R2"] or sc[("A", "UST")]["yon_r1"] != 1 or sc.get(("B", "UST"), {}).get("yol") != ["R1"] or ("C", "UST") in sc or sc.get(("C", "ALT"), {}).get("yol") != ["R2K"] \
            or sc.get(("D", "ALT"), {}).get("yon_r1") != -1 or ("E", "UST") in sc or ("F", "UST") in sc or ("G", "ALT") in sc or ("K", "UST") in sc or sc.get(("H", "ALT"), {}).get("yon_r1") != -1 or len(sc) != 5:
        hata.append(f"12) KEŞİF seçimi kuralları yanlış: {Sc['secili']}")
    Plk = Plx.assign(brut_tutar_v2=[True] * 3 + [False] * (npl - 3)); Sk = K.k60_secim(R1x.copy(), R2x.copy(), Plk, Es)
    if Sk["esik"]["r1_acik"] or any("R1" in x["yol"] for x in Sk["secili"]) or not any(x["yol"] == ["R2"] for x in Sk["secili"]):
        hata.append("12) plasebo yanlış pozitifi > %5 iken R1 yolu kapanmalı, R2 yolu açık kalmalıydı")
    R1b = R1x.copy(); R1b.loc[R1b.sinyal == "B", ["t_alfa", "p_alfa"]] = [1.95, 0.0093]      # BH'den geçer ama plasebo brüt t en büyüğünü (2,0) aşmaz
    if any(x["sinyal"] == "B" for x in K.k60_secim(R1b, R2x.copy(), Plx, Es)["secili"]):
        hata.append("12) BH'den geçmeyen / plasebo eşiğini aşmayan sinyal seçildi")
    d1 = lambda s, t, **kw: {"sinyal": s, "taraf": t, "olculdu": True, "yillik_fazla": 0.05, "alfa_yillik": 0.04, "t_alfa": 2.0, "brut_yillik_fazla": 0.06, "brut_alfa_yillik": 0.05, "brut_t_alfa": 2.1, **kw}  # noqa: E731
    d2 = lambda s, t, **kw: {"sinyal": s, "taraf": t, "ufuk": 12, "olculdu": True, "lift_p100": 1.5, "alt_p100": 1.1, "lift_m50": 0.8, "alt_m50": 0.5, **kw}  # noqa: E731
    G1 = pd.DataFrame([d1("A", "UST"), d1("B", "UST", t_alfa=1.6), d1("C", "ALT", t_alfa=1.7, yillik_fazla=-0.01), d1("D", "ALT", brut_yillik_fazla=-0.05, brut_alfa_yillik=-0.04, brut_t_alfa=-2.3, t_alfa=-2.8, yillik_fazla=-0.06, alfa_yillik=-0.05),
                       d1("E", "UST", olculdu=False), d1("H", "ALT", brut_yillik_fazla=-0.05, brut_alfa_yillik=-0.04, brut_t_alfa=-1.7)])
    G2 = pd.DataFrame([d2("A", "UST"), d2("B", "UST", alt_p100=0.99), d2("C", "ALT", lift_m50=1.6, alt_m50=1.2, lift_p100=0.9, alt_p100=0.6), d2("D", "ALT", lift_p100=1.1, alt_p100=1.01), d2("E", "UST", olculdu=False)])
    gir = [{"sinyal": "A", "taraf": "UST", "yol": ["R1", "R2"], "yon_r1": 1}, {"sinyal": "B", "taraf": "UST", "yol": ["R1"], "yon_r1": 1}, {"sinyal": "C", "taraf": "ALT", "yol": ["R2K"], "yon_r1": 0},
           {"sinyal": "D", "taraf": "ALT", "yol": ["R1"], "yon_r1": -1}, {"sinyal": "E", "taraf": "UST", "yol": ["R2"], "yon_r1": 0}, {"sinyal": "H", "taraf": "ALT", "yol": ["R1"], "yon_r1": -1},
           {"sinyal": "AILE_X", "taraf": "UST", "yol": [], "yon_r1": 0, "kesif_secili": False}]
    Gc = K.k60_gecis(G1, G2, Plx, gir, Es); gs = {(x["sinyal"], x["taraf"]): x for x in Gc["sonuc"]}; pl = Gc["plasebo"]
    if not (abs(pl["t95"] - np.percentile(Plx.brut_t_alfa, 95)) < 1e-12 and abs(pl["brut_t05"] - np.percentile(Plx.brut_t_alfa, 5)) < 1e-12 and abs(pl["lift_p100"] - np.percentile(Plx.r2_lift_p100, 95)) < 1e-12):
        hata.append("12) geçiş plasebo dilimleri yanlış")
    if not (gs[("A", "UST")]["r1"] and gs[("A", "UST")]["r2"] and gs[("A", "UST")]["gecer"] and not gs[("B", "UST")]["r1"] and not gs[("B", "UST")]["r2"] and not gs[("B", "UST")]["gecer"]
            and not gs[("C", "ALT")]["r1"] and gs[("C", "ALT")]["r2k"] and gs[("C", "ALT")]["alt_m50_ustu_1"] and gs[("D", "ALT")]["r1_ters"] and not gs[("D", "ALT")]["r1"]
            and not gs[("D", "ALT")]["r2"] and not gs[("E", "UST")]["gecer"] and not gs[("H", "ALT")]["r1_ters"] and not gs[("AILE_X", "UST")]["gecer"] and not gs[("AILE_X", "UST")]["kesif_secili"]):
        hata.append(f"12) DOĞRULAMA / KASA geçme kuralları yanlış: {Gc['sonuc']}")
    kasa_s = [dict(gs[("A", "UST")], r2=False), gs[("C", "ALT")], gs[("D", "ALT")]]
    et = K.k60_etiketler([{"sinyal": "A", "taraf": "UST", "yol": ["R1", "R2"], "yon_r1": 1}, {"sinyal": "C", "taraf": "ALT", "yol": ["R2K"], "yon_r1": 0}, {"sinyal": "D", "taraf": "ALT", "yol": ["R1"], "yon_r1": -1},
                          {"sinyal": "B", "taraf": "UST", "yol": ["R1"], "yon_r1": 1}], Gc["sonuc"], kasa_s, None, Es)
    if et != {("A", "UST"): ["K60-İZ ADAYI"], ("C", "ALT"): ["K60-KAÇINMA İZİ"], ("D", "ALT"): ["K60-R1 TERS (bilgi)"], ("B", "UST"): []}:
        hata.append(f"12) etiket kuralları yanlış: {et}")
    sec_c = [{"sinyal": "C", "taraf": "ALT", "yol": ["R2K"], "yon_r1": 0}]; kr2 = lambda v: pd.DataFrame([{"sinyal": "C", "taraf": "ALT", "ufuk": 12, "alt_m50": v}, {"sinyal": "C", "taraf": "ALT", "ufuk": 6, "alt_m50": 9.0}])  # noqa: E731
    if K.k60_etiketler(sec_c, Gc["sonuc"], kasa_s, kr2(0.97), Es) != {("C", "ALT"): []} or K.k60_etiketler(sec_c, Gc["sonuc"], kasa_s, kr2(1.2), Es) != {("C", "ALT"): ["K60-KAÇINMA İZİ"]}:
        hata.append("12) KAÇINMA etiketi KEŞİF'te de -%50 lift alt sınırı > 1 istemeliydi (ana ufuk)")
    # 13) lojistik ve kalibrasyon
    rl = np.random.default_rng(5); Xl = rl.random((120000, 3)); bl_ = np.array([-3.0, 1.5, -1.0, 0.0]); pl_ = 1 / (1 + np.exp(-(bl_[0] + Xl @ bl_[1:]))); yl = (rl.random(120000) < pl_).astype(float)
    kt = K.k60_lojistik(Xl, yl, 1e-6, 50)
    if np.abs(kt - bl_).max() > 0.12:
        hata.append(f"13) lojistik regresyon bilinen katsayıları bulamadı: {kt}")
    kl = K.k60_kalibrasyon(pl_, yl, 10)
    if len(kl) != 10 or kl.n.sum() != 120000 or not kl.tahmin.is_monotonic_increasing or np.abs(kl.tahmin - kl.gerceklesen).max() > 0.02 or len(K.k60_kalibrasyon(np.array([]), np.array([]), 10)):
        hata.append("13) kalibrasyon tablosu yanlış")
    Xg_ = K.k60_model_girdi(Sd, Et); sk = K.k60_model_skor(Sd, U, [-2.0] + [0.5] * 10, Et)
    if Xg_.shape != (M, N, 10) or np.isnan(Xg_).any() or not (Xg_[~np.isfinite(Sd["AILE_SEC"]), 9] == 0.5).all() or np.isfinite(sk[~U]).any() \
            or abs(sk[k, j] - 1 / (1 + np.exp(-(-2.0 + 0.5 * Xg_[k, j].sum())))) > 1e-12 or E0["model"]["girdi"] != ["AILE_" + a for a in ("MOM", "VAL", "PRF", "INV", "EAR", "RSK", "LIQ", "SEA", "DIS", "SEC")]:
        hata.append("13) model girdisi (eksik = 0,5) / skor yanlış")
    # 14) okuyucular: Yahoo (K60_veri ile aynı), French günlük, EDGAR dizini, frames
    with tempfile.TemporaryDirectory() as td:
        ts = [int(pd.Timestamp(x, tz="America/New_York").timestamp()) + 34200 for x in pd.bdate_range("2012-03-01", periods=40)] + [int(pd.Timestamp("2026-09-02", tz="America/New_York").timestamp()) + 34200]
        cl = [10.0 + 0.1 * i for i in range(41)]; op = [c - 0.05 for c in cl]; hi = [c + 0.2 for c in cl]; lo = [c - 0.2 for c in cl]; vo = [1000 + i for i in range(41)]
        cl[5] = None; hi[7] = lo[7] - 1.0; vo[9] = None; cl[11] = 0.0
        J = {"chart": {"result": [{"meta": {"instrumentType": "EQUITY", "exchangeTimezoneName": "America/New_York", "firstTradeDate": ts[0] - 86400 * 2},
                                   "timestamp": ts, "indicators": {"quote": [{"open": op, "high": hi, "low": lo, "close": cl, "volume": vo}], "adjclose": [{"adjclose": [None if c is None else c * 0.9 for c in cl]}]},
                                   "events": {"splits": {"1": {"date": ts[20], "numerator": 2.0, "denominator": 1.0}, "2": {"date": ts[30], "numerator": 1.0, "denominator": 1.0}},
                                              "dividends": {"1": {"date": ts[15], "amount": 0.1}, "2": {"date": ts[25], "amount": 0.0}}}}]}}
        yj = os.path.join(td, "X.json"); json.dump(J, open(yj, "w"))
        o1, d1_ = K.k60_fiyat_oku(yj, "2026-08-31"); o2, d2_ = KV.k60v_yahoo_oku(yj, "2026-08-31")
        if d1_ != d2_ or not np.array_equal(o1["gun"], o2["gun"].to_numpy("datetime64[D]")) or not np.array_equal(o1["c"], o2["kapanis"]) or not np.array_equal(o1["a"], o2["duzeltilmis"]) \
                or not np.array_equal(o1["v"], o2["hacim"]) or o1["kirpik"] != o2["kirpik"] or o1["tur"] != "EQUITY" or len(o1["gun"]) != 37 or len(o1["bolunme"][0]) != 1 or o1["bolunme"][1][0] != 2.0 \
                or len(o1["temettu"]) != 1 or str(o1["temettu"][0]) != str(pd.bdate_range("2012-03-01", periods=40)[15].date()) or not np.allclose(o1["h"] - o1["c"], 0.2) or not np.allclose(o1["c"] - o1["o"], 0.05):
            hata.append("14) K60 Yahoo okuyucusu K60_veri okuyucusuyla aynı değil / bölünme, temettü, OHL yanlış")
        json.dump({"yok": 404}, open(yj, "w"))
        if K.k60_fiyat_oku(yj)[0] is not None or K.k60_fiyat_oku(os.path.join(td, "yok.json"))[0] is not None:
            hata.append("14) '404 yok' işareti / olmayan dosya fiyat diye okundu")
        zf = os.path.join(td, "ff.zip")
        with zipfile.ZipFile(zf, "w") as z:
            z.writestr("F-F_Research_Data_Factors_daily.csv", "Baslik satiri\n\n,Mkt-RF,SMB,HML,RF\n20200102,    0.50,   -0.25,    0.10,    0.01\n20200103,   -1.00,    0.20,  -99.99,    0.01\n\nCopyright\n")
        Fg = K.k60_french_gunluk(zf)
        if Fg.shape != (2, 4) or abs(Fg.MKT_RF.iloc[0] - 0.005) > 1e-15 or abs(Fg.RF.iloc[1] - 0.0001) > 1e-15 or not np.isnan(Fg.HML.iloc[1]) or str(Fg.index[1].date()) != "2020-01-03":
            hata.append("14) French günlük faktör ayrıştırıcısı yanlış")
        durmali(lambda: K.k60_french_gunluk(os.path.join(td, "yok.zip")), "14) olmayan French dosyası hata vermedi", hata)
        dz = os.path.join(td, "edgar_master_2015Q2.gz")
        govde = ("Description:           Master Index of EDGAR Dissemination Feed\nLast Data Received:    June 30, 2015\n\n\nCIK|Company Name|Form Type|Date Filed|Filename\n" + "-" * 80 + "\n"
                 "1001|A CO|10-K|2015-04-10|edgar/data/1001/a.txt\n1001|A CO|10-K/A|2015-04-20|edgar/data/1001/b.txt\n1001|A CO|10-Q|2015-05-11|x\n1001|A CO|8-K|2015-05-04|x\n1001|A CO|8-K|2015-05-04|y\n"
                 "1001|A CO|NT 10-Q|2015-05-12|x\n1001|A CO|S-3ASR|2015-06-01|x\n1001|A CO|424B5|2015-06-02|x\n1001|A CO|SC 13D|2015-06-03|x\n1001|A CO|SC 13D/A|2015-06-04|x\n1001|A CO|SC TO-I|2015-06-05|x\n"
                 "1002|B CO|10-Q|2015-05-01|x\n9999|EVREN DISI|10-K|2015-04-01|x\n1002|B CO|4|2015-05-02|x\n1002|B CO|SCHEDULE 13D|2015-06-09|x\n")
        open(dz, "wb").write(gzip.compress(govde.encode("latin-1")))
        Bz = K.k60_dizin_oku({"1001", "1002"}, E0, [{"yol": dz, "tur": "dizin"}])
        if not (list(Bz["K"]) == ["1001"] and list(Bz["K"]["1001"].astype(str)) == ["2015-04-10"] and list(Bz["Q"]["1002"].astype(str)) == ["2015-05-01"] and len(Bz["8K"]["1001"]) == 1
                and list(Bz["NT"]["1001"].astype(str)) == ["2015-05-12"] and len(Bz["S3"]["1001"]) == 1 and len(Bz["424B5"]["1001"]) == 1 and list(Bz["13D"]["1001"].astype(str)) == ["2015-06-03"]
                and list(Bz["13D"]["1002"].astype(str)) == ["2015-06-09"] and len(Bz["TOI"]["1001"]) == 1 and "9999" not in Bz["K"]):
            hata.append(f"14) EDGAR dizin okuyucusu yanlış: { {g: {c: list(v.astype(str)) for c, v in x.items()} for g, x in Bz.items()} }")
        fr = lambda ad, veri: (json.dump({"data": veri}, open(os.path.join(td, ad), "w")), os.path.join(td, ad))[1]  # noqa: E731
        satirlar = [{"tur": "an", "etiket": "Assets", "donem": "CY2015Q2I", "yol": fr("a.json", [{"cik": 1001, "end": "2015-06-30", "val": 500}, {"cik": 7, "end": "2015-06-30", "val": 1}])},
                    {"tur": "sure", "etiket": "NetIncomeLoss", "donem": "CY2015Q2", "yol": fr("b.json", [{"cik": 1001, "start": "2015-04-01", "end": "2015-06-30", "val": 12}])},
                    {"tur": "sure", "etiket": "NetIncomeLoss", "donem": "CY2015", "yol": fr("c.json", [{"cik": 1002, "start": "2015-01-01", "end": "2015-12-31", "val": 99}])},
                    {"tur": "an", "etiket": "EntityCommonStockSharesOutstanding", "donem": "CY2015Q2I", "yol": fr("d.json", [{"cik": 1001, "end": "2015-07-28", "val": 1000000}])},
                    {"tur": "an", "etiket": "CommonStockSharesOutstanding", "donem": "CY2015Q2I", "yol": fr("e.json", [{"cik": 1002, "end": "2015-06-30", "val": 77}])},
                    {"tur": "sure", "etiket": "Revenues", "donem": "CY2015Q3", "yol": fr("f.json", {})}, {"tur": "dizin", "etiket": "master", "donem": "2015Q2", "yol": dz}]
        eski_fn = K.k60_frame_yollari; K.k60_frame_yollari = lambda: (satirlar, [])
        try:
            Th = K.k60_temel_yukle(["1001", None, "1002", "1001"], E0); q15 = 2015 * 4 + 1 - Th["q_bas"]
            if not (Th["I"]["Assets"][q15, 0] == 500 and Th["I"]["Assets"][q15, 3] == 500 and np.isnan(Th["I"]["Assets"][q15, 1]) and Th["Q"]["NetIncomeLoss"][q15, 0] == 12
                    and Th["Y"]["NetIncomeLoss"][2015 - Th["y_bas"], 2] == 99 and str(Th["Ybit"][2015 - Th["y_bas"], 2]) == "2015-12-31" and str(Th["Ybas"][2015 - Th["y_bas"], 2]) == "2015-01-01"
                    and str(Th["bit"][q15, 0]) == "2015-06-30" and np.isnat(Th["bit"][q15, 2]) and Th["pay_ham"][0] == [(np.datetime64("2015-07-28"), 1000000.0)] and Th["pay_ham"][2] == []
                    and Th["I"]["CommonStockSharesOutstanding"][q15, 2] == 77 and Th["bit"].shape == (70, 4) and Th["Ybit"].shape == (17, 4) and "Revenues" not in Th["Q"]):
                hata.append("14) SEC frames yükleyicisi (CIK -> sütun, çeyrek / yıl sırası, dönem sonları, kapak pay kayıtları) yanlış")
            K.k60_frame_yollari = lambda: (satirlar, ["Assets/CY2015Q3I"])
            durmali(lambda: K.k60_temel_yukle(["1001"], E0), "14) eksik SEC çerçevesiyle yükleme durmadı", hata)
        finally:
            K.k60_frame_yollari = eski_fn
    if K._k60_ceyrek_sira(np.array(["2015-05-31", "2015-12-31", "2016-01-02", "NaT"], "datetime64[D]")).tolist()[:3] != [2015 * 4 + 1, 2015 * 4 + 3, 2015 * 4 + 3] \
            or any(K._k60_ceyrek_sira(np.array([x], "datetime64[D]"))[0] != K57._k57_ceyrek_sira(pd.Timestamp(x)) for x in ("2015-05-31", "2016-01-02", "2019-09-28", "2020-02-29")):
        hata.append("14) çeyrek sırası K57 kuralıyla aynı değil")
    # 15) kapsam modu: ileri getiri, portföy, olasılık HESAPLANMAZ; ön kayıt gerekmez
    with tempfile.TemporaryDirectory() as td:
        asil = {a: getattr(K, a) for a in ("k60_r1", "k60_r2", "k60_plasebo", "k60_panel", "k60_lift")}; cagri = {"getiri": []}

        def yasak(*a, **kw):
            raise AssertionError("kapsam modunda getiri / olasılık hesabı çağrıldı")

        def panel_izle(D_, E_=None, getiri=True):
            cagri["getiri"].append(getiri); return asil["k60_panel"](D_, E_, getiri)
        for a in ("k60_r1", "k60_r2", "k60_plasebo", "k60_lift"):
            setattr(K, a, yasak)
        K.k60_panel = panel_izle
        try:
            Zk = K.k60_kapsam_kos(td, demet=D, E=Et)
        except AssertionError as ex:
            hata.append(f"15) {ex}"); Zk = None
        finally:
            for a, f in asil.items():
                setattr(K, a, f)
        if Zk is not None:
            oz = json.load(open(K._k60_yol("kapsam_ozet", td), encoding="utf-8")); z = Zk.set_index(["sinyal", "donem"])
            if cagri["getiri"] != [False] or sorted(os.listdir(td)) != ["kapsam.csv", "kapsam_ozet.json"] or len(Zk) != 3 * (len(tn) + len(E0["bilesik"])):
                hata.append(f"15) kapsam modu getirili panel kurdu / fazladan dosya yazdı / satır sayısı yanlış: {cagri}, {os.listdir(td)}, {len(Zk)}")
            say_ = (U & np.isfinite(Sd["MOM_12_1"])).sum(axis=1)
            if not (z.loc[("MOM_12_1", "kesif"), "olcum_ay"] == 120 and abs(z.loc[("MOM_12_1", "kesif"), "ort_n"] - say_[pm].mean()) < 1e-9 and z.loc[("LTREV_60_13", "kesif"), "ilk_ay"] == "2015-01-30"
                    and z.loc[("LTREV_60_13", "kesif"), "olcum_ay"] == 84 and z.loc[("MOM_12_1", "kasa"), "olcum_ay"] == 31 and z.loc[("E_S3", "kesif"), "tur"] == "bayrak"
                    and oz["evren"]["kesif"]["ay_r1"] == 120 and oz["evren"]["kasa"]["ay_r2_12"] == 20 and oz["evren"]["kasa"]["son_r2_12"] == "2025-08-29" and oz["hisse"] == N
                    and abs(oz["evren"]["kesif"]["pay_dei"] + oz["evren"]["kesif"]["pay_cso"] + oz["evren"]["kesif"]["pay_wads"] + oz["evren"]["kesif"]["pay_yok"] - 1) < 1e-5):
                hata.append("15) kapsam sayıları elle sayımla aynı değil")
            nt = K.k60_kapsam_notu(td)
            if "| MOM_12_1 | MOM | surekli | 120 / " not in nt or "KEŞİF: oluşum ayı R1 120" not in nt or nt.index("- KEŞİF:") > nt.index("- DOĞRULAMA:") or nt.index("- DOĞRULAMA:") > nt.index("- KASA:") or "getiri, olasılık, t hesaplanmadı" not in nt or "henüz koşulmadı" not in K.k60_kapsam_notu(td + "_yok"):
                hata.append("15) kapsam notu (ön kayıt §12) beklenen satırları içermiyor")
    # 16) uçtan uca: git'li kesif -> dogrulama -> kasa, dönem sırası, tek açılış, rapor, çıktılardan yeniden üretim
    import shutil
    Eu = test_esik(coklu={"plasebo_n": 100}); kos = lambda d, kl, dm=D: K.k60_kos(d, kl, git_sart=True, demet=dm, E=Eu)  # noqa: E731
    with tempfile.TemporaryDirectory() as ana:
        td = os.path.join(ana, "cikti"); os.makedirs(td); git(td, "init", "-q")
        try:
            yo = K.k60_onkayit(td, veri_sha={}); durmali(lambda: kos("kesif", td), "16) git'e işlenmemiş ön kayıtla KEŞİF durmadı", hata)
            git(td, "add", "K60_ON_KAYIT.md"); git(td, "commit", "-q", "-m", "on kayit")
            Rk = kos("kesif", td); sec = json.load(open(K._k60_yol("secili", td), encoding="utf-8")); mk = json.load(open(K._k60_meta_yol("kesif", td), encoding="utf-8"))
            for a in ("kesif_r1.csv", "kesif_r2.csv", "kesif_aylik.csv", "kesif_r2_aylik.csv", "placebo.csv", "secili.json", "kesif_meta.json", "model_kalibrasyon.csv", "olasilik_tablosu.md", "K60_RAPOR.md"):
                if not os.path.exists(os.path.join(td, a)):
                    hata.append(f"16) KEŞİF çıktısı yok: {a}")
            yollar = {(x["sinyal"], x["taraf"]): x for x in sec["secili"]}
            if not sec["secili"] or sec["muhur"] != K.k60_esik_sha() or mk["secili_sha256"] != K._k60_sha(K._k60_yol("secili", td)) or len(sec["model"]["katsayi"]) != 11 \
                    or sorted(sec["bilesik"]) != sorted(E0["bilesik"]) or not sec["esik"]["r1_acik"]:
                hata.append(f"16) secili.json beklenen alanları taşımıyor / R1 yolu kapalı: {sec['esik']}")
            if "R1" not in yollar.get(("ROE_TTM", "UST"), {}).get("yol", []) or yollar[("ROE_TTM", "UST")]["yon_r1"] != 1 or "R2" not in yollar.get(("ROE_TTM", "UST"), {}).get("yol", []):
                hata.append(f"16) ekilmiş etki (kalite -> getiri) KEŞİF'te ROE_TTM ÜST'ü R1 ve R2 yolundan seçtirmedi: {yollar.get(('ROE_TTM', 'UST'))}")
            R1k = pd.read_csv(os.path.join(td, "kesif_r1.csv")); R2k = pd.read_csv(os.path.join(td, "kesif_r2.csv")); Ak = pd.read_csv(os.path.join(td, "kesif_aylik.csv")); A2k = pd.read_csv(os.path.join(td, "kesif_r2_aylik.csv"))
            r_ = R1k[(R1k.sinyal == "ROE_TTM") & (R1k.taraf == "UST")].iloc[0]; a_ = Ak[(Ak.sinyal == "ROE_TTM") & (Ak.taraf == "UST")]
            if abs(r_.yillik_fazla - 12 * (a_.net - a_.kiyas).mean()) > 1e-9 or r_.ay != len(a_) or abs(r_.t_alfa - K59.k59_ols_nw(a_.net.to_numpy(), a_.kiyas.to_numpy(), 6)["t"][0]) > 1e-9:
                hata.append("16) R1 satırı kesif_aylik.csv'den yeniden üretilemiyor")
            r2_ = R2k[(R2k.sinyal == "ROE_TTM") & (R2k.taraf == "UST") & (R2k.ufuk == 12)].iloc[0]; b_ = A2k[(A2k.sinyal == "ROE_TTM") & (A2k.taraf == "UST")]
            Lr = K.k60_lift(b_.k_p100, b_.n, b_.k_evren_p100, b_.n_evren, Eu)
            if abs(r2_.P_p100 - b_.k_p100.sum() / b_.n.sum()) > 1e-12 or abs(r2_.taban_p100 - b_.k_evren_p100.sum() / b_.n_evren.sum()) > 1e-12 or abs(r2_.lift_p100 - Lr["lift"]) > 1e-12 \
                    or abs(r2_.alt_p100 - Lr["alt"]) > 1e-12 or abs(r2_.pz_p100 - Lr["pz"]) > 1e-12 or abs(r2_.lift_m50 - (b_.k_m50.sum() / b_.n.sum()) / (b_.k_evren_m50.sum() / b_.n_evren.sum())) > 1e-12:
                hata.append("16) R2 satırı kesif_r2_aylik.csv'den yeniden üretilemiyor")
            if set(R2k.ufuk.unique()) != {12, 6, 3} or len(pd.read_csv(os.path.join(td, "placebo.csv"))) != 100 or "ODDS_MODEL" not in set(R2k.sinyal) or R2k[R2k.sinyal == "ODDS_MODEL"].aile_r2.any() \
                    or R1k[R1k.sinyal == "GAP_OVN"].aile_r1.sum() != 2 or R1k[(R1k.sinyal == "MOM_12_1")].aile_r1.tolist() != [True, False] or R1k[R1k.sinyal == "E_S3"].taraf.tolist() != ["ALT"]:
                hata.append("16) KEŞİF tabloları: ufuklar / plasebo sayısı / hipotez aileleri (yönlü: ÜST; '?': iki uç; bayrak: bayraklı grup; model aile dışı) yanlış")
            durmali(lambda: kos("dogrulama", td), "16) secili.json git'e işlenmeden DOĞRULAMA durmadı", hata)
            durmali(lambda: kos("kasa", td), "16) DOĞRULAMA'dan önce KASA durmadı", hata)
            git(td, "add", "secili.json"); git(td, "commit", "-q", "-m", "secili")
            asil_metin = open(yo, encoding="utf-8").read(); open(yo, "a", encoding="utf-8").write("\n")
            durmali(lambda: kos("dogrulama", td), "16) git'e işlendikten sonra değişen ön kayıtla koşu durmadı", hata)
            open(yo, "w", encoding="utf-8").write(asil_metin)
            ys = K._k60_yol("secili", td); asil_sec = open(ys, encoding="utf-8").read(); open(ys, "w", encoding="utf-8").write(asil_sec.replace('"secili": [', '"secili": [\n  {"sinyal": "BM", "taraf": "UST", "yol": ["R1"], "yon_r1": 1},', 1))
            durmali(lambda: kos("dogrulama", td), "16) değiştirilmiş secili.json ile DOĞRULAMA durmadı", hata)
            durmali(lambda: kos("kesif", td), "16) KEŞİF yeniden koşusu farklı secili.json'ı sessizce kabul etti / üzerine yazdı", hata)
            open(ys, "w", encoding="utf-8").write(asil_sec)
            kos("kesif", td)
            if open(ys, encoding="utf-8").read() != asil_sec:
                hata.append("16) KEŞİF yeniden koşusu secili.json'ı bayt bayt aynı üretmedi")
            Rd = kos("dogrulama", td); gc = json.load(open(K._k60_yol("gecen", td), encoding="utf-8")); md = json.load(open(K._k60_meta_yol("dogrulama", td), encoding="utf-8"))
            R1d = pd.read_csv(os.path.join(td, "dogrulama_r1.csv")); izinli = {(x["sinyal"], x["taraf"]) for x in sec["secili"]} | {(b, t) for b in sec["bilesik"] for t in ("UST", "ALT")} | {("ODDS_MODEL", "UST")}
            if not set(zip(R1d.sinyal, R1d.taraf)) <= izinli or md["giren_n"] != len(izinli) - 1 or md["gecen_sha256"] != K._k60_sha(K._k60_yol("gecen", td)) or not gc["gecen"] \
                    or any(not x["gecer"] for x in gc["gecen"]) or len(gc["sonuc"]) != md["giren_n"] or R1d.ay.max() != 24:
                hata.append("16) DOĞRULAMA yalnız KEŞİF-SEÇİLİ çiftleri + bileşikleri ölçmeliydi / geçen listesi tutarsız")
            if abs(json.load(open(ys, encoding="utf-8"))["model"]["katsayi"][0] - sec["model"]["katsayi"][0]) > 0 or not len(pd.read_csv(os.path.join(td, "model_kalibrasyon.csv")).query("donem == 'dogrulama'")):
                hata.append("16) model katsayıları DOĞRULAMA'da dondurulmuş değil / kalibrasyon yazılmadı")
            durmali(lambda: kos("kasa", td), "16) dogrulama_gecen.json git'e işlenmeden KASA açıldı", hata)
            if os.path.exists(K._k60_yol("kasa_isaret", td)):
                hata.append("16) reddedilen KASA koşusu açılış işareti bıraktı")
            git(td, "add", "dogrulama_gecen.json"); git(td, "commit", "-q", "-m", "gecen")
            td2 = os.path.join(ana, "kopya"); shutil.copytree(td, td2)
            try:
                kos("kasa", td2, {"sembol": []}); hata.append("16) bozuk demetle KASA çökmedi (test kurgusu)")
            except K.K60Hata:
                hata.append("16) bozuk demetle KASA beklenmeyen biçimde durdu")
            except Exception:
                pass
            if not os.path.exists(K._k60_yol("kasa_isaret", td2)):
                hata.append("16) KASA açılış işareti ölçümden ÖNCE yazılmamış (çöken koşu iz bırakmadı)")
            durmali(lambda: kos("kasa", td2), "16) çöken ilk açılıştan sonra KASA ikinci kez açıldı", hata)
            Rs = kos("kasa", td); mks = json.load(open(K._k60_meta_yol("kasa", td), encoding="utf-8")); R1s = pd.read_csv(os.path.join(td, "kasa_r1.csv"))
            gecenler = {(x["sinyal"], x["taraf"]) for x in gc["gecen"]} | {("ODDS_MODEL", "UST")}
            if mks.get("kod_sha256") != K._k60_sha(os.path.join(KOK, "K60.py")) or mks["not"] or "numpy" not in mks["surumler"]:
                hata.append("16) koşu meta dosyasında kod sha256 / sürümler yok ya da gereksiz not var")
            if not set(zip(R1s.sinyal, R1s.taraf)) <= gecenler or mks["giren_n"] != len(gc["gecen"]) or json.load(open(K._k60_yol("kasa_isaret", td), encoding="utf-8"))["muhur"] != K.k60_esik_sha() or R1s.ay.max() != 31:
                hata.append("16) KASA yalnız DOĞRULAMA'dan geçenleri ölçmeliydi / açılış işareti yanlış")
            for d_ in K.K60_DONEM:
                durmali(lambda d_=d_: kos(d_, td), f"16) KASA açıldıktan sonra {d_} yeniden koşuldu (tek açılış / dönem sırası)", hata)
            etk = {(x["sinyal"], x["taraf"]): x["etiket"] for x in mks["etiket"]}; hepsi = [e for v in etk.values() for e in v]
            if set(etk) != set(yollar) or "K60-İZ ADAYI" not in hepsi or "K60-OLASILIK İZİ" not in hepsi or any(e not in E0["etiket"].values() for e in hepsi) \
                    or any("K60-İZ ADAYI" in v and "R1" not in yollar[a]["yol"] for a, v in etk.items()):
                hata.append(f"16) etiketler: ekilmiş etki İZ ADAYI ve OLASILIK İZİ üretmeliydi; etiket yalnız seçildiği yoldan verilir: { {a: v for a, v in etk.items() if v} }")
            rp = open(os.path.join(td, "K60_RAPOR.md"), encoding="utf-8").read(); tb = open(os.path.join(td, "olasilik_tablosu.md"), encoding="utf-8").read()
            for parca in ("## Bulgular (düz dille)", "## Olasılık tablosu (ana sonuç)", "## R1 — portföy cetveli v2", "## Kütüphanenin tamamı", "## Plasebo dağılımı", "## Birleşik olasılık modeli", "## Yanlılık ve sınırlar", "## En büyük üç katkı",
                          "İZ ilan edilemez", "ETİKETLER", "KEŞİF-SEÇİLİ", "taban oranı", "K60-İZ ADAYI", "tam kör OLMAYAN"):
                if parca not in rp:
                    hata.append(f"16) raporda '{parca}' yok")
            for parca in ("KASA açıldı", "| ROE_TTM (ÜST)", "| KEŞİF |", "| DOĞRULAMA |", "| KASA |", "taban P(+%100)", "kat (lift) [%95 aralık]", "taban P(-%50)", "ALT SINIRDIR", "## Aile bileşikleri", "ODDS_MODEL"):
                if parca not in tb:
                    hata.append(f"16) olasılık tablosunda '{parca}' yok")
            satir = [x for x in tb.splitlines() if x.startswith("| ROE_TTM (ÜST)") and "| KEŞİF |" in x][0].split("|")
            if satir[4].strip() != K._k60_yuzde(r2_.taban_p100) or satir[5].strip() != K._k60_yuzde(r2_.P_p100) or not satir[6].strip().startswith(K._sy(r2_.lift_p100) + " ["):
                hata.append(f"16) olasılık tablosu satırı kesif_r2.csv ile aynı değil: {satir}")
            os.remove(os.path.join(td, "K60_RAPOR.md")); K.k60_rapor(td, Eu)
            if open(os.path.join(td, "K60_RAPOR.md"), encoding="utf-8").read() != rp:
                hata.append("16) rapor çıktılardan yeniden üretilince değişti")
            for f in os.listdir(td):
                if f.endswith((".md", ".csv", ".json")) and K._K60_EPOSTA.search(open(os.path.join(td, f), encoding="utf-8").read()):
                    hata.append(f"16) sentetik çıktıda e-posta var: {f}")
            del Rk, Rd, Rs
        except Exception as ex:
            import traceback
            hata.append(f"16) uçtan uca sentetik koşu çöktü: {type(ex).__name__} {ex} | {traceback.format_exc()[-600:]}")
    # 17) e-posta / anahtar yok (kod, test, gerçek ön kayıt ve çıktılar)
    anahtar = re.compile(r"(api[_-]?key\s*[:=]\s*['\"]\w{8,}|bearer\s+[A-Za-z0-9_\-]{16,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|TIINGO_TOKEN\s*=\s*['\"]\w+)", re.I)
    dosyalar = [os.path.join(KOK, "K60.py"), os.path.join(KOK, "test_k60.py")]
    if os.path.isdir(K.K60_YOL["cikti"]):
        dosyalar += [os.path.join(K.K60_YOL["cikti"], f) for f in os.listdir(K.K60_YOL["cikti"]) if f.endswith((".md", ".csv", ".json"))]
    for y in dosyalar:
        m_ = open(y, encoding="utf-8").read()
        if K._K60_EPOSTA.search(m_) or anahtar.search(m_):
            hata.append(f"17) e-posta / anahtar biçimli parça var: {os.path.relpath(y, KOK)}")
    if "urlopen" in src or "requests." in src or "indir_sec" in src.replace("k60v", "") or "K60_SEC_UA" in src:
        hata.append("17) K60.py ağ isteği atabilecek / SEC kimliği okuyan kod içeriyor")
    return hata


if __name__ == "__main__":
    Hh = testler()
    if Hh:
        print("K60 TEST: HATA", len(Hh)); print("\n".join(Hh)); sys.exit(1)
    print("K60 TEST: GEÇTİ")
