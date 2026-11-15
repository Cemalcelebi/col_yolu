"""K67 testleri (ağ gerekmez; yalnız SENTETİK veri, gerçek veride getiri ölçmez). Çalıştırma: python test_k67.py

1) çakışma kapısı (_CK_ONCE_K67)  2) ön kayıt mührü (üzerine yazmama, farklı mühür reddi, eşik / değişken değişince mühür değişir; gerçek K67_ON_KAYIT.md varsa
bugünkü eşiklerle aynı)  3) ayrıştırıcılar (not günlüğü JSON: hedef 0 -> yok, ET zamanı, tarih-yalnız kayıt gün sonu; takvim HTML: tarih, saat, AM / PM)
4) olay kuralı elle (r0: açılış öncesi / kapanış sonrası / hafta sonu / saat yok; d = r0 + 4; giriş d + 1; pencere sınırları)  5) 60 işlem günü tekilleştirme
6) EAR = FON_IZI.fi_k28_olaylar 'ear'  7) değişkenler ELLE (kurum yönü kuralı, AYKIRI oran, BASLA, NET / BUYUKLUK / AYRISMA, en az kayıt eşikleri)
8) pencere ve GELECEĞE BAKMA YOK (d kapanışından sonraki kayıt bozulunca / eklenince değişkenler aynı; açıklama anından önceki kayıt girmez; tarih-yalnız kayıt
d günü girmez; t0 sonrası her şey bozulunca t0'a kadar olayların değişkenleri ve sıraları aynı)  9) YON_UYUM kategori kuralı  10) olay içi sıra elle +
geleceğe bakmaz  11) katmanlı ÜST - ALT (elle nokta, tek katman = ham fark, katman_min, tohumla birebir)  12) karar kuralı (ADAY / İZ DEĞİL / ÖLÇÜLEMEZ /
işaret / BH)  13) S2 eşleme kuralı (d <= t, son 60 işlem günü, en son olay)  14) kapsam modu getiri hesaplamaz  15) uçtan uca sentetik koşu (git'li): ön kayıt
yokken / işlenmemişken / değişmişken `kos` reddeder; çıktılar ve rapor yeniden üretilir  16) indirici (sahte; 429'da geri çekilir, yavaşlar, kaldığı yerden
sürer)  17) e-posta / anahtar yok.
"""
from __future__ import annotations

import copy
import gzip
import json
import os
import re
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K67 as K  # noqa: E402
import test_k60 as TK  # noqa: E402
import test_k64 as T64  # noqa: E402

FI, K60, K64 = K.FI, K.K60, K.K64
E0 = K.K67_ESIK
ET = "America/New_York"


def durmali(f, ad: str, hata: list, tur=None) -> None:
    try:
        f(); hata.append(ad)
    except (tur or K.K67Hata):
        pass


def epoch_et(s: str) -> int:
    """ET yerel zaman metni -> epoch saniye."""
    return int(pd.Timestamp(s).tz_localize(ET).tz_convert("UTC").timestamp())


def not_satir(sembol: str, et: str, kurum: str, eylem: str = "main", hedef_eylem: str = "", hedef: float = np.nan, eski: float = np.nan,
              yalniz_tarih: bool = False) -> dict:
    ep = int(pd.Timestamp(et[:10]).tz_localize("UTC").timestamp()) if yalniz_tarih else epoch_et(et)
    return {"sembol": sembol, "zaman_utc": ep, "kurum": kurum, "eylem": eylem, "yeni_tav": "", "eski_tav": "", "hedef_eylem": hedef_eylem, "hedef": hedef,
            "eski_hedef": eski}


def notlar(sat: list) -> pd.DataFrame:
    return K.k67_not_et(pd.DataFrame(sat, columns=["sembol", "zaman_utc", "kurum", "eylem", "yeni_tav", "eski_tav", "hedef_eylem", "hedef", "eski_hedef"]))


def sentetik_takvim(V: dict, tohum: int = 11) -> pd.DataFrame:
    """Her hisse için çeyreklik açıklama günleri (2016-07 -> 2026-08), saat (açılış öncesi / kapanış sonrası / yok) ve sürpriz."""
    rng = np.random.default_rng(tohum); sat = []
    for j, s in enumerate(sorted(V)):
        g = pd.Timestamp("2016-07-18") + pd.Timedelta(days=int(rng.integers(0, 20)))
        while g <= pd.Timestamp("2026-08-20"):
            sa = int(rng.choice([7, 16, -1]))
            sat.append({"sembol": s, "tarih": g.normalize(), "saat": sa, "an": g.normalize() + pd.Timedelta(hours=max(sa, 0)), "eps_tahmin": 1.0, "eps_gercek": 1.0,
                        "surpriz": float(np.round(rng.normal(2, 8), 2)) if rng.random() > 0.05 else np.nan})
            g = g + pd.Timedelta(days=int(rng.integers(84, 98)))
    return pd.DataFrame(sat)


def sentetik_not(T: pd.DataFrame, tohum: int = 12) -> pd.DataFrame:
    """Açıklamalardan sonraki günlere kurum kayıtları (bir kısmı pencere dışı: açıklamadan önce ve 2 hafta sonra)."""
    rng = np.random.default_rng(tohum); kurumlar = [f"Kurum{i}" for i in range(12)]; sat = []
    for r in T.itertuples():
        if rng.random() < 0.15:
            continue
        for kk in rng.choice(kurumlar, int(rng.integers(1, 9)), replace=False):
            gun = r.tarih + pd.Timedelta(days=int(rng.integers(-1, 10)), hours=int(rng.integers(5, 19)), minutes=int(rng.integers(0, 60)))
            eski = float(rng.uniform(10, 100)); deg = float(rng.normal(0.01, 0.08)); ey = str(rng.choice(["main", "main", "up", "down", "init", "reit"]))
            sat.append(not_satir(r.sembol, str(gun), str(kk), ey, "Raises" if deg > 0 else "Lowers", round(eski * (1 + deg), 2), round(eski, 2) if ey != "init" else np.nan))
    return notlar(sat)


def testler() -> list:
    hata: list = []; nan = np.nan
    # 1) çakışma kapısı
    src = open(os.path.join(KOK, "K67.py"), encoding="utf-8").read().replace("from __future__ import annotations\n", "")
    g = {"__name__": "kapi_test", "k67_kos": object(), "_CK_KAYIT": {"k67_kos": "BASKA.py"}}
    try:
        exec(compile(src, "K67.py", "exec"), g); hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "kapi_test2"}
    try:
        exec(compile(src, "K67.py", "exec"), g2); exec(compile(src, "K67.py", "exec"), g2)
    except Exception as ex:
        hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
    if "_CK_ONCE_K67 = " not in src or "_cakisma_kontrol_k67()" not in src:
        hata.append("1) çakışma kapısı adı _CK_ONCE_K67 değil")
    # 2) ön kayıt mührü ve sabitler
    if K.k67_kodlar() != ["N_UP", "N_DOWN", "NET", "BUYUKLUK", "AYRISMA", "YON_UYUM"] or K.k67_kodlar(tur="S") != ["N_UP", "N_DOWN", "NET", "BUYUKLUK", "AYRISMA"]:
        hata.append("2) değişken listesi iş tanımındaki gibi değil")
    if not (E0["kriz"] == "2026-08-31" and [d[0] for d in E0["donem"]] == ["2017-2021", "2022-2026", "2023-2026"] and E0["bagimsiz"] == ["2017-2021", "2022-2026"]
            and E0["olay"]["tekil_gun"] == 60 and E0["olay"]["karar_gun"] == 5 and E0["maliyet"] == {"ABD": 0.0020} and E0["coklu"]["bh_q"] == 0.10
            and E0["rev"]["min_net"] == 2 and E0["rev"]["min_ayrisma"] == 3 and E0["s1"]["n_esik"] == 30 and E0["s2"]["pencere"] == 60
            and abs(E0["sira"]["ust"] - 2 / 3) < 1e-12 and abs(E0["sira"]["alt"] - 1 / 3) < 1e-12 and E0["ek_ufuk"] == 20
            and E0["aile"] == ["N_UP", "N_DOWN", "NET", "BUYUKLUK", "AYRISMA", "YU_POZ", "YU_NEG", "COL_NET"]):
        hata.append("2) K67_ESIK sabitleri iş tanımındaki gibi değil")
    if FI.FI_OLCUT["ufuk"] != 60 or FI.FI_OLCUT["n_esik"] != 30 or FI.FI_K24["tekrar"] != 60:
        hata.append("2) FI_OLCUT / FI_K24 beklenen değerlerde değil")
    for yol_, deg_ in ((("rev", "min_net"), 3), (("olay", "karar_gun"), 4), (("s1", "katman_min"), 5), (("coklu", "bh_q"), 0.05)):
        E2 = copy.deepcopy(E0); E2[yol_[0]][yol_[1]] = deg_
        if K.k67_esik_sha(E2) == K.k67_esik_sha():
            hata.append(f"2) {yol_} değişince mühür değişmiyor")
    E3 = copy.deepcopy(E0); E3["degisken"][2]["tanim"] += " (değişti)"
    if K.k67_esik_sha(E3) == K.k67_esik_sha():
        hata.append("2) değişken tanımı değişince mühür değişmiyor")
    vs = {"V_ABD.pkl": ("a" * 64, 1), "liste_abd.csv.gz": ("b" * 64, 1), "k67_yahoo": ("c" * 64, 2822)}
    with tempfile.TemporaryDirectory() as td:
        y = K.k67_onkayit(td, veri_sha=vs); oc = K._k67_onkayit_oku(y)
        if oc["sha"] != K.k67_esik_sha() or oc["veri"] != vs or not oc["zaman_utc"]:
            hata.append("2) ön kayıt mührü / veri özetleri / zaman okunamadı")
        metin = open(y, encoding="utf-8").read()
        for parca in ("## 1. Veri kaynakları", "VERİ YOK", "BIST VERİSİ YOK", "## 6. S1", "## 7. S2", "## 9. Karar", "## 10. Çoklu test", "## 11. Güç", "## 12. Geleceğe bakma",
                      "## 13. Yanlılık", "## 14. SAPMA / BOŞLUK", "## 15. Kapsam", "Alpha Vantage", "49,99"):
            if parca not in metin:
                hata.append(f"2) ön kayıtta '{parca}' yok")
        open(y, "a", encoding="utf-8").write("\n")
        if K.k67_onkayit(td, veri_sha=vs) != y:
            hata.append("2) mühür aynıyken ön kayıt yolu dönmedi")
        open(y, "w", encoding="utf-8").write(metin.replace(oc["sha"], "0" * 64))
        durmali(lambda: K.k67_onkayit(td, veri_sha=vs), "2) farklı mühürlü ön kaydın üzerine yazıldı", hata)
        durmali(lambda: K.k67_onkayit_dogrula(td), "2) farklı mühürlü ön kayıt doğrulandı", hata)
    gercek = K._k67_yol("onkayit")
    if os.path.exists(gercek) and K._k67_onkayit_oku(gercek)["sha"] != K.k67_esik_sha():
        hata.append("2) gerçek K67_ON_KAYIT.md mührü bugünkü eşiklerle aynı değil")
    # 3) ayrıştırıcılar
    js = json.dumps({"quoteSummary": {"result": [{"upgradeDowngradeHistory": {"history": [
        {"epochGradeDate": epoch_et("2024-05-02 07:30"), "firm": "A", "toGrade": "Buy", "fromGrade": "Hold", "action": "up", "priceTargetAction": "Raises",
         "currentPriceTarget": 110.0, "priorPriceTarget": 0.0},
        {"epochGradeDate": int(pd.Timestamp("2024-05-03").tz_localize("UTC").timestamp()), "firm": "B", "action": "main", "currentPriceTarget": 0, "priorPriceTarget": 50}]}}]}}).encode()
    Na = K.k67_not_et(K.k67_not_ayristir(js, "XYZ"))
    if not (len(Na) == 2 and Na.hedef.iloc[0] == 110 and np.isnan(Na.eski_hedef.iloc[0]) and np.isnan(Na.hedef.iloc[1]) and Na.eski_hedef.iloc[1] == 50
            and Na.et.iloc[0] == pd.Timestamp("2024-05-02 07:30") and not Na.tarih_yalniz.iloc[0] and Na.tarih_yalniz.iloc[1]
            and Na.et.iloc[1] == pd.Timestamp("2024-05-03 23:59:59")):
        hata.append("3) not günlüğü ayrıştırma / ET zamanı / tarih-yalnız kuralı yanlış")
    if len(K.k67_not_ayristir(b'{"quoteSummary": {"result": [{}]}}', "Q")) != 0:
        hata.append("3) boş not günlüğü boş tablo vermedi")
    durmali(lambda: K.k67_not_ayristir(b"bozuk", "Q"), "3) bozuk JSON durdurmadı", hata)
    html = ("<table><thead><tr><th>Symbol</th><th>Company</th><th>Earnings Date</th><th>EPS Estimate</th><th>Reported EPS</th><th>Surprise (%)</th></tr></thead><tbody>"
            "<tr><td>X</td><td>X Inc</td><td>November 2, 2026 at 4 PM EST</td><td>1.98</td><td>2.10</td><td>5.80</td></tr>"
            "<tr><td>X</td><td>X Inc</td><td>July 30, 2026 at 7 AM EDT</td><td>-</td><td>-</td><td>-</td></tr>"
            "<tr><td>X</td><td>X Inc</td><td>April 1, 2026 at 12 AM EDT</td><td>1</td><td>1</td><td>-3.5</td></tr>"
            "<tr><td>X</td><td>X Inc</td><td>March 3, 2026 at 12 PM EST</td><td>1</td><td>1</td><td>0</td></tr></tbody></table>").encode()
    Ta = K.k67_takvim_ayristir(html, "X")
    if not (list(Ta.saat) == [16, 7, 0, 12] and list(Ta.tarih.dt.strftime("%Y-%m-%d")) == ["2026-11-02", "2026-07-30", "2026-04-01", "2026-03-03"]
            and Ta.surpriz.iloc[0] == 5.8 and np.isnan(Ta.surpriz.iloc[1]) and Ta.an.iloc[0] == pd.Timestamp("2026-11-02 16:00") and Ta.surpriz.iloc[2] == -3.5):
        hata.append(f"3) takvim ayrıştırma yanlış: {Ta.to_dict('records')}")
    # 4) olay kuralı elle
    gun = pd.bdate_range("2024-01-01", "2024-12-31"); V1 = {"X": pd.DataFrame({"Open": 10.0, "High": 10.5, "Low": 9.5, "Close": np.linspace(10, 12, len(gun)), "Volume": 1e6}, index=gun),
                                                         "Y": pd.DataFrame({"Open": 20.0, "High": 21, "Low": 19, "Close": np.linspace(20, 18, len(gun)), "Volume": 1e6}, index=gun)}
    T1 = pd.DataFrame([{"sembol": "X", "tarih": pd.Timestamp("2024-05-02"), "saat": 7, "surpriz": 3.0},     # Perşembe açılış öncesi -> r0 = 2 Mayıs
                       {"sembol": "X", "tarih": pd.Timestamp("2024-08-01"), "saat": 16, "surpriz": -2.0},   # Perşembe kapanış sonrası -> r0 = 2 Ağustos
                       {"sembol": "X", "tarih": pd.Timestamp("2024-11-02"), "saat": -1, "surpriz": nan},    # Cumartesi, saat yok -> r0 = 4 Kasım
                       {"sembol": "Y", "tarih": pd.Timestamp("2024-05-03"), "saat": 0, "surpriz": 1.0}])    # 12 AM (saat yok) -> r0 = 3 Mayıs
    T1["an"] = T1.tarih + pd.to_timedelta(T1.saat.clip(lower=0), unit="h"); T1["eps_tahmin"] = 1.0; T1["eps_gercek"] = 1.0
    Q1 = pd.DataFrame([{"sembol": "X", "tarih": pd.Timestamp("2024-11-03"), "surpriz": 4.0}])
    X1 = K.k67_olaylar(T1, V1, Q1).set_index(["sembol", "tarih"])
    bek = {("X", "2024-05-02"): ("2024-05-02", "2024-05-08", "2024-05-09", "2024-05-02 07:00"), ("X", "2024-08-01"): ("2024-08-02", "2024-08-08", "2024-08-09", "2024-08-01 16:00"),
           ("X", "2024-11-02"): ("2024-11-04", "2024-11-08", "2024-11-11", "2024-11-02 00:00"), ("Y", "2024-05-03"): ("2024-05-03", "2024-05-09", "2024-05-10", "2024-05-03 00:00")}
    for (s, t), (r0, d, gi, bas) in bek.items():
        r = X1.loc[(s, pd.Timestamp(t))]
        if not (r.r0 == pd.Timestamp(r0) and r.d == pd.Timestamp(d) and r.giris == pd.Timestamp(gi) and r.pencere_bas == pd.Timestamp(bas) and r.pencere_son == pd.Timestamp(d) + pd.Timedelta(hours=16)):
            hata.append(f"4) olay kuralı yanlış: {s} {t} -> {r.r0} {r.d} {r.giris} {r.pencere_bas} {r.pencere_son}")
    r = X1.loc[("X", pd.Timestamp("2024-11-02"))]
    if not (r.surpriz_kaynak == "NASDAQ" and r.surpriz == 4.0 and X1.loc[("X", pd.Timestamp("2024-05-02"))].surpriz_kaynak == "YAHOO"):
        hata.append("4) sürpriz kaynağı kuralı (Yahoo -> Nasdaq ±1 gün -> EAR) yanlış")
    T1b = pd.concat([T1, pd.DataFrame([{"sembol": "X", "tarih": pd.Timestamp("2024-12-26"), "saat": 7, "surpriz": 1.0, "an": pd.Timestamp("2024-12-26 07:00"), "eps_tahmin": 1, "eps_gercek": 1}])])
    if len(K.k67_olaylar(T1b, V1)) != 4:
        hata.append("4) karar günü verinin sonunu aşan olay atılmadı")
    # 5) 60 işlem günü tekilleştirme
    T5 = pd.DataFrame([{"sembol": "X", "tarih": gun[p], "saat": 7, "surpriz": 1.0} for p in (10, 40, 75, 140, 150)]); T5["an"] = T5.tarih + pd.Timedelta(hours=7)
    T5["eps_tahmin"] = 1.0; T5["eps_gercek"] = 1.0
    if list(K.k67_olaylar(T5, V1).tekil) != [True, False, True, True, False]:
        hata.append("5) 60 işlem günü tekilleştirme kuralı yanlış")
    # 6) EAR = fi_k28_olaylar
    V6 = T64.sentetik_fiyat([f"S{i}" for i in range(8)], "2019-01-01", "2020-12-31"); T6 = sentetik_takvim(V6)
    T6 = T6[(T6.tarih >= "2019-03-01") & (T6.tarih <= "2020-11-30")].reset_index(drop=True)
    X6 = K.k67_olaylar(T6, V6, None, {**E0, "olay": {**E0["olay"], "ilk_tarih": "2019-01-01"}})
    A6 = FI.fi_k28_olaylar(T6.rename(columns={"tarih": "D"})[["sembol", "D", "surpriz"]], V6, "ABD").set_index(["sembol", "D"]).ear
    m6 = X6.set_index(["sembol", "tarih"]).ear.reindex(A6.index)
    if not (len(A6) > 20 and np.allclose(m6.to_numpy(float), A6.to_numpy(float), equal_nan=True)):
        hata.append("6) EAR fi_k28_olaylar ile birebir değil")
    # 7) değişkenler elle
    W = notlar([not_satir("X", "2024-05-03 08:00", "A", "main", "Raises", 110, 100),
                not_satir("X", "2024-05-03 09:00", "B", "main", "Lowers", 45, 50),
                not_satir("X", "2024-05-03 10:00", "C", "reit", "Maintains", 80, 80),
                not_satir("X", "2024-05-03 11:00", "D", "up", "", nan, nan),
                not_satir("X", "2024-05-03 12:00", "E", "init", "Announces", 70, nan),
                not_satir("X", "2024-05-03 13:00", "F", "main", "Raises", 105, 100), not_satir("X", "2024-05-06 13:00", "F", "main", "Raises", 120, 105),
                not_satir("X", "2024-05-03 14:00", "G", "main", "Lowers", 20, 100),
                not_satir("X", "2024-05-03 15:00", "H", "up", "Lowers", 90, 100),
                not_satir("X", "2024-05-03 15:30", "", "down", "Lowers", 1, 100)])
    v = K.k67_pencere_degiskenleri(W)
    oran = [0.1, -0.1, 0.0, 0.2, -0.1]   # A, B, C, F (105 -> 120 değil: ilk önceki 100 -> son 120), H
    if not (v["N_UP"] == 3 and v["N_DOWN"] == 3 and v["N_AYNI"] == 1 and v["N_BASLA"] == 1 and v["n_kurum"] == 8 and v["n_aykiri"] == 1 and v["n_oran"] == 5
            and np.isclose(v["NET"], 0 / 7) and np.isclose(v["BUYUKLUK"], np.median(oran)) and np.isclose(v["AYRISMA"], np.std(oran, ddof=1)) and v["n_kayit"] == 10):
        hata.append(f"7) değişkenler elle hesapla tutmuyor: {v}")
    yn = K.k67_kurum_yon(W[W.kurum == "H"]); yg = K.k67_kurum_yon(W[W.kurum == "G"]); yd = K.k67_kurum_yon(W[W.kurum == "D"]); ye = K.k67_kurum_yon(W[W.kurum == "E"])
    if not (yn[0] == "DOWN" and np.isclose(yn[1], -0.1) and yg == ("DOWN", yg[1], True) and np.isnan(yg[1]) and yd[0] == "UP" and ye[0] == "BASLA"):
        hata.append("7) kurum yönü kuralı (hedef önce, aykırı, tavsiye, init) yanlış")
    v2 = K.k67_pencere_degiskenleri(W[W.kurum.isin(["A", "E"])])
    if not (v2["N_UP"] == 1 and v2["N_DOWN"] == 0 and np.isnan(v2["NET"]) and np.isnan(v2["BUYUKLUK"]) and np.isnan(v2["AYRISMA"])):
        hata.append("7) en az kayıt eşikleri (NET payda >= 2, BUYUKLUK >= 2, AYRISMA >= 3) yanlış")
    v3 = K.k67_pencere_degiskenleri(W.iloc[:0])
    if not (v3["n_kurum"] == 0 and np.isnan(v3["N_UP"]) and np.isnan(v3["NET"])):
        hata.append("7) kaydı olmayan olayda değişkenler NaN değil")
    # 8) pencere ve geleceğe bakma
    Xo = K.k67_olaylar(T1, V1)
    Nw = notlar([not_satir("X", "2024-05-02 06:59", "P", "main", "Raises", 200, 100),       # açıklamadan (07:00) önce: girmez
                 not_satir("X", "2024-05-02 07:00", "A", "main", "Raises", 110, 100),       # açıklama anı: girer
                 not_satir("X", "2024-05-08 16:00", "B", "main", "Lowers", 90, 100),        # d kapanışı: girer
                 not_satir("X", "2024-05-08 16:01", "C", "main", "Lowers", 50, 100),        # d kapanışından sonra: girmez
                 not_satir("X", "2024-05-08", "D", "down", "", nan, nan, yalniz_tarih=True),   # d günü, saat yok: girmez
                 not_satir("X", "2024-05-07", "E", "up", "", nan, nan, yalniz_tarih=True)])    # d-1, saat yok: girer
    Xv = K.k67_degiskenler(Xo, Nw).set_index(["sembol", "tarih"]).loc[("X", pd.Timestamp("2024-05-02"))]
    if not (Xv.n_kayit == 3 and Xv.N_UP == 2 and Xv.N_DOWN == 1 and np.isclose(Xv.NET, 1 / 3) and np.isclose(Xv.BUYUKLUK, 0.0)):
        hata.append(f"8) pencere sınırları yanlış: {Xv[['n_kayit', 'N_UP', 'N_DOWN', 'NET', 'BUYUKLUK']].to_dict()}")
    Nw2 = notlar([*Nw[["sembol", "zaman_utc", "kurum", "eylem", "yeni_tav", "eski_tav", "hedef_eylem", "hedef", "eski_hedef"]].to_dict("records"),
                  not_satir("X", "2024-05-08 18:00", "Z", "down", "Lowers", 1, 100), not_satir("X", "2024-05-09 09:00", "Y", "down", "Lowers", 1, 100)])
    Nw2.loc[Nw2.et > pd.Timestamp("2024-05-08 16:00"), "hedef"] = 999.0
    Xv2 = K.k67_degiskenler(Xo, Nw2).set_index(["sembol", "tarih"]).loc[("X", pd.Timestamp("2024-05-02"))]
    if not all((Xv[c] == Xv2[c]) or (pd.isna(Xv[c]) and pd.isna(Xv2[c])) for c in ("n_kayit", "N_UP", "N_DOWN", "NET", "BUYUKLUK", "AYRISMA")):
        hata.append("8) d kapanışından sonraki kayıtlar değişkenleri değiştirdi (geleceğe bakma)")
    V8 = T64.sentetik_fiyat([f"S{i:02d}" for i in range(60)], "2015-06-01", "2024-12-31"); T8 = sentetik_takvim(V8); T8 = T8[T8.tarih <= "2024-11-15"].reset_index(drop=True)
    N8 = sentetik_not(T8); t0 = pd.Timestamp("2019-06-28")
    Xa = K.k67_siralar(K.k67_degiskenler(K.k67_olaylar(T8, V8), N8))
    T8b = T8.copy(); mb = T8b.tarih > t0; T8b.loc[mb, "surpriz"] = -T8b.loc[mb, "surpriz"] * 3; T8b.loc[mb, "saat"] = 16
    N8b = N8.copy(); nb = N8b.et > t0 + pd.Timedelta(hours=16); N8b.loc[nb, "hedef"] = N8b.loc[nb, "hedef"] * 3.7; N8b.loc[nb, "eylem"] = "down"
    N8b = pd.concat([N8b, notlar([not_satir(s, "2019-07-01 08:00", f"Yeni{i}", "down", "Lowers", 1, 50) for i, s in enumerate(sorted(V8))])], ignore_index=True)
    V8b = T64.fiyat_boz(V8, t0)
    Xb = K.k67_siralar(K.k67_degiskenler(K.k67_olaylar(T8b, V8b), N8b))
    ka = Xa[Xa.d <= t0].set_index(["sembol", "tarih"]); kb = Xb[Xb.d <= t0].set_index(["sembol", "tarih"]).reindex(ka.index)
    kol8 = ["ear", "surpriz", "n_kayit", "N_UP", "N_DOWN", "NET", "BUYUKLUK", "AYRISMA", "NET_ic", "N_UP_ic", "AYRISMA_ic", "ear_ic"]
    if not (len(ka) > 150 and all(T64.esit(ka[c].to_numpy(float), kb[c].to_numpy(float), 1e-12) for c in kol8) and (ka.YON_UYUM == kb.YON_UYUM).all()
            and (ka.tekil == kb.tekil).all() and (ka.d == kb.d).all()):
        hata.append("8) t0 sonrası fiyat / takvim / not bozulunca t0'a kadar olayların değişkenleri / sıraları değişti (geleceğe bakma)")
    if not (np.isfinite(Xa.NET_ic).sum() > 100 and (Xa.NET_grup == "UST").sum() > 20 and (Xa.NET_grup == "ALT").sum() > 20):
        hata.append("8) sentetik veride sıra / grup oluşmadı")
    # 9) YON_UYUM
    if [K.k67_yon_uyum(*a) for a in ((0.5, 2), (-0.5, 2), (0.5, -2), (-0.5, -2), (0, 3), (0.5, 0), (nan, 1), (1, nan))] != ["AO", "TO", "TU", "AU", "NOTR", "NOTR", "YOK", "YOK"]:
        hata.append("9) YON_UYUM kategori kuralı yanlış")
    # 10) olay içi sıra elle
    gx = np.array(["2020-01-01", "2020-01-01", "2020-03-01", "2020-06-01", "2021-03-01"], "datetime64[D]"); xx = np.array([1.0, 2.0, 2.0, nan, 0.5])
    s10 = K64.k64_ic_sira(gx, xx, 365, 2)
    if not T64.esit(s10, np.array([0.25, 0.75, (1 + 0.5 * 2) / 3, nan, (0 + 0.5) / 2])):
        hata.append(f"10) olay içi sıra elle tutmuyor: {s10}")
    # 11) katmanlı ÜST - ALT
    rng = np.random.default_rng(5); n = 400; fu = rng.normal(0.02, 0.1, n); fa = rng.normal(0, 0.1, n); ay = np.array([f"2020-{1 + i % 12:02d}" for i in range(n)])
    ku = rng.choice(["UST", "ORTA", "ALT"], n); ka_ = rng.choice(["UST", "ORTA", "ALT"], n); ka_[:5] = "TEK"   # 'TEK' katmanı katman_min altında
    kf = K.k67_katmanli_fark(fu, ay, ku, fa, ay, ka_, 300, 9, [2.5, 97.5], 0.9, 10)
    w = []; dd = []
    for k in ("ALT", "ORTA", "UST"):
        a_, b_ = fu[ku == k], fa[ka_ == k]; w.append(len(a_) * len(b_) / (len(a_) + len(b_))); dd.append(a_.mean() - b_.mean())
    if not (np.isclose(kf["nokta"], np.dot(w, dd) / sum(w)) and kf["katman"] == 3 and kf["n_alt"] == n - 5 and kf["n_ust"] == n and kf["alt"] < kf["nokta"] < kf["ust"]
            and kf == K.k67_katmanli_fark(fu, ay, ku, fa, ay, ka_, 300, 9, [2.5, 97.5], 0.9, 10)):
        hata.append(f"11) katmanlı fark elle / tohum tutmuyor: {kf}")
    tek = K.k67_katmanli_fark(fu, ay, np.full(n, "A"), fa, ay, np.full(n, "A"), 300, 9, [2.5, 97.5], 0.9, 10)
    ham = K64.k64_grup_farki(fu, ay, fa, ay, 300, 9, [2.5, 97.5], 0.9)
    if not (np.isclose(tek["nokta"], ham["nokta"]) and np.isclose(tek["alt"], ham["alt"]) and np.isclose(tek["ust"], ham["ust"])):
        hata.append("11) tek katmanda katmanlı fark ham farka (K64.k64_grup_farki) eşit değil")
    if K.k67_katmanli_fark(fu[:5], ay[:5], ku[:5], fa[:5], ay[:5], ka_[:5], 100, 1, [2.5, 97.5])["katman"] != 0:
        hata.append("11) katman_min altındaki katmanlar dışarıda kalmadı")
    # 12) karar kuralı
    def satir(k, d, olc, eu, ea, p_u, p_a, nk):
        return {"degisken": k, "donem": d, "olculebilir": olc, "ek_UST": eu, "ek_ALT": ea, "k_p_ust": p_u, "k_p_alt": p_a, "k_nokta": nk, "tutar_UST": False,
                "tutar_ALT": False, "tutar_net_UST": False, "tutar_net_ALT": False}
    Fk = pd.DataFrame([satir("NET", "2017-2021", True, True, False, 1e-6, 1, 0.05), satir("NET", "2022-2026", True, True, False, 1e-6, 1, 0.04),
                       satir("NET", "2023-2026", True, False, False, 0.2, 0.8, 0.01),
                       satir("N_UP", "2017-2021", True, True, False, 1e-6, 1, 0.05), satir("N_UP", "2022-2026", True, True, False, 1e-6, 1, 0.04),
                       satir("N_UP", "2023-2026", True, False, False, 0.7, 0.3, -0.01),
                       satir("AYRISMA", "2017-2021", False, False, False, nan, nan, nan), satir("AYRISMA", "2022-2026", True, False, True, 1, 1e-6, -0.05),
                       satir("BUYUKLUK", "2017-2021", True, True, False, 1e-6, 1, 0.05), satir("BUYUKLUK", "2022-2026", True, False, False, 0.4, 0.6, 0.01)])
    Kr = K.k67_karar(Fk).set_index(["degisken", "yon"])
    if not (Kr.loc[("NET", "UST"), "karar"].startswith("ABD-ADAY") and Kr.loc[("N_UP", "UST"), "karar"] == "İZ DEĞİL" and Kr.loc[("N_UP", "UST"), "abd"] == "ADAY"
            and Kr.loc[("AYRISMA", "ALT"), "karar"].startswith("ÖLÇÜLEMEZ") and Kr.loc[("BUYUKLUK", "UST"), "karar"] == "İZ DEĞİL"
            and Kr.loc[("NET", "ALT"), "karar"] == "İZ DEĞİL" and int(Kr.aile_m.iloc[0]) == 14):
        hata.append(f"12) karar kuralı yanlış: {Kr[['karar', 'abd']].to_dict()}")
    Fk2 = Fk.copy(); Fk2.loc[Fk2.degisken == "NET", ["k_p_ust"]] = [0.2, 1e-6, 0.2]
    if K.k67_karar(Fk2).set_index(["degisken", "yon"]).loc[("NET", "UST"), "karar"] != "İZ DEĞİL":
        hata.append("12) BH'den geçmeyen dönem varken ADAY verildi")
    # 13) S2 eşleme kuralı
    V13 = {"X": V1["X"]}; ix = V13["X"].index
    B13 = pd.DataFrame({"sembol": "X", "tarih": [ix[10], ix[100], ix[150]], "d": [ix[14], ix[104], ix[154]], "tekil": True, "NET": [0.5, -0.5, 1.0], "N_UP": 1.0, "N_DOWN": 0.0,
                        "BUYUKLUK": 0.1, "AYRISMA": nan, "n_kurum": 2.0, "ear": 0.0, "surpriz": 1.0, "YON_UYUM": "AO"})
    C13 = pd.DataFrame({"sembol": "X", "sinyal": [ix[60], ix[104], ix[153], ix[230]], "giris": [ix[61], ix[105], ix[154], ix[231]], "tekil": True})
    Y13 = K.k67_col_olaylar(V13, B13, None, C13)
    if not (list(Y13.bilanco) == [True, True, True, False] and list(Y13.b_NET.iloc[:3]) == [0.5, -0.5, -0.5] and pd.isna(Y13.b_NET.iloc[3])):
        hata.append(f"13) S2 eşleme kuralı yanlış: {Y13[['sinyal', 'bilanco', 'b_NET']].to_dict('records')}")
    # 14) kapsam modu getiri hesaplamaz
    girdi = {"V": V8, "T": T8, "N": N8, "Q": pd.DataFrame(columns=["sembol", "tarih", "surpriz"])}
    with tempfile.TemporaryDirectory() as td:
        asil = (FI.fi_olcut_panel, FI.fi_olcut_olay, FI.fi_olcut_hucre, K64.k64_olc)

        def yasak(*a, **k):
            raise AssertionError("kapsam modunda getiri / FI_OLCUT çağrıldı")
        try:
            FI.fi_olcut_panel = FI.fi_olcut_olay = FI.fi_olcut_hucre = K64.k64_olc = yasak
            Kp = K.k67_kapsam(td, girdi)
        except AssertionError as ex:
            hata.append(f"14) {ex}"); Kp = pd.DataFrame()
        finally:
            FI.fi_olcut_panel, FI.fi_olcut_olay, FI.fi_olcut_hucre, K64.k64_olc = asil
        if len(Kp):
            if any(c in Kp.columns for c in ("r60", "fark", "ort_fark", "r20")) or not {"n_ham", "n_tekil", "n_pencere", "n_deger", "n_ust", "n_alt", "n_kapsama"} <= set(Kp.columns):
                hata.append("14) kapsam tablosunda getiri sütunu var ya da sayım sütunu eksik")
            o = Kp[(Kp.degisken == "(olay)") & (Kp.donem == "2017-2021")].iloc[0]; z = Kp[(Kp.degisken == "NET") & (Kp.donem == "2017-2021")].iloc[0]
            gm = (Xa.giris >= "2017-01-01") & (Xa.giris <= "2021-12-31")
            if not (o.n_ham == gm.sum() and o.n_tekil == (gm & Xa.tekil).sum() and o.n_pencere <= o.n_tekil and z.n_ust + z.n_orta + z.n_alt <= z.n_deger <= o.n_pencere
                    and o.n_kapsama <= o.n_pencere):
                hata.append("14) kapsam sayıları olay tablosuyla tutmuyor")
            if "Kapsam sayımı" not in K.k67_kapsam_notu(td) or "| NET |" not in K.k67_kapsam_notu(td) or (Kp.kume == "S2").sum() != 3:
                hata.append("14) kapsam notu / S2 sayımı yazılamadı")
    # 15) uçtan uca sentetik koşu (git'li)
    with tempfile.TemporaryDirectory() as td:
        durmali(lambda: K.k67_kos(td, True, girdi), "15) ön kayıt yokken koşu durmadı", hata)
        TK.git(td, "init", "-q"); y = K.k67_onkayit(td, veri_sha=vs)
        durmali(lambda: K.k67_kos(td, True, girdi), "15) git'e işlenmemiş ön kayıtla koşu durmadı", hata)
        TK.git(td, "add", K.K67_DOSYA["onkayit"]); TK.git(td, "commit", "-q", "-m", "on kayit")
        R = K.k67_kos(td, True, girdi)
        for ad in ("olay", "s1", "fark", "s2", "karar", "meta", "rapor"):
            if not os.path.exists(K._k67_yol(ad, td)):
                hata.append(f"15) çıktı yok: {ad}")
        S1, Fk3, Kr3 = R["s1"], R["fark"], R["karar"]
        Xe = pd.read_csv(K._k67_yol("olay", td), parse_dates=["giris", "d"], keep_default_na=True); Xe["NET_grup"] = Xe.NET_grup.fillna("")
        m1 = (Xe.giris >= "2017-01-01") & (Xe.giris <= "2021-12-31") & Xe.fark.notna()
        tm = S1[(S1.grup == "TEMEL") & (S1.donem == "2017-2021")].iloc[0]
        if not (tm.n == m1.sum() and np.isclose(tm.ort_fark, Xe.fark[m1].mean()) and np.isclose(tm.ort_r60, Xe.r60[m1].mean())):
            hata.append("15) temel hücre olay dosyasından yeniden üretilemedi")
        fz = Fk3[(Fk3.degisken == "NET") & (Fk3.donem == "2017-2021")].iloc[0]; mu, ma = m1 & (Xe.NET_grup == "UST"), m1 & (Xe.NET_grup == "ALT")
        if not (fz.n_ust == mu.sum() and fz.n_alt == ma.sum() and np.isclose(fz.nokta, Xe.fark[mu].mean() - Xe.fark[ma].mean())
                and bool(fz.ek_UST) == bool(fz.olculebilir and fz.k_alt > 0 and fz.nokta > 0)):
            hata.append("15) NET ÜST - ALT satırı olay dosyasından yeniden üretilemedi / ek katkı kuralı tutmuyor")
        ke = Xe.ear_grup.fillna("").to_numpy(str); mu2, ma2 = mu.to_numpy() & (ke != ""), ma.to_numpy() & (ke != "")
        kfz = K.k67_katmanli_fark(Xe.fark[mu2].to_numpy(), K._k67_ay(Xe[mu2]), ke[mu2], Xe.fark[ma2].to_numpy(), K._k67_ay(Xe[ma2]), ke[ma2], E0["s1"]["bootstrap"],
                                  E0["s1"]["tohum"], E0["s1"]["guven"], E0["s1"]["gecerli_pay"], E0["s1"]["katman_min"])
        if not (np.isclose(kfz["nokta"], fz.k_nokta, equal_nan=True) and np.isclose(kfz["alt"], fz.k_alt, equal_nan=True)):
            hata.append("15) katmanlı fark olay dosyasından yeniden üretilemedi")
        if len(Fk3) != 3 * 8 or len(Kr3) != 16 or not set(Kr3.karar.str.slice(0, 8)) <= {"ABD-ADAY", "İZ DEĞİL", "ÖLÇÜLEME"}:
            hata.append(f"15) karşıtlık / karar tablosu boyutu ya da etiketleri beklenen gibi değil ({len(Fk3)}, {len(Kr3)})")
        rap = open(R["rapor"], encoding="utf-8").read()
        for parca in ("## Karar tablosu", "## Hücreler", "## ÜST - ALT", "VERİ YOK", "## Sınırlar"):
            if parca not in rap:
                hata.append(f"15) raporda '{parca}' yok")
        if open(K.k67_rapor(td), encoding="utf-8").read() != rap:
            hata.append("15) rapor çıktılardan yeniden üretilince değişti")
        open(y, "a", encoding="utf-8").write("\nsonradan eklenen satır\n")
        durmali(lambda: K.k67_kos(td, True, girdi), "15) git'e işlendikten sonra değişen ön kayıtla koşu durmadı", hata)
    # 16) indirici (sahte; ağ yok)
    with tempfile.TemporaryDirectory() as td:
        say = {"n": 0}; uyku = []

        def gn(_o, s):
            say["n"] += 1
            if say["n"] in (2, 3):
                raise K._K67Sinir("HTTP 429")
            return "tamam", json.dumps({"quoteSummary": {"result": [{"upgradeDowngradeHistory": {"history": []}}]}}).encode()

        def gt(_o, s):
            return ("yok", b"") if s == "B" else ("tamam", b"<table></table>")
        R16 = K.k67_indir(["A", "B"], td, gn, gt, oturum=object(), uyu=uyku.append)
        D16 = pd.read_csv(os.path.join(td, "durum.csv"))
        if not (R16["sinir_hatasi"] == 2 and len(D16) == 4 and os.path.exists(os.path.join(td, "not", "A.json.gz")) and not os.path.exists(os.path.join(td, "takvim", "B.html.gz"))
                and 60 in uyku and 120 in uyku and R16["son_bekleme_sn"] > K.K67_INDIR["bekle"]):
            hata.append(f"16) indirici geri çekilme / yavaşlama / durum kaydı yanlış: {R16} {uyku}")
        R16b = K.k67_indir(["A", "B", "C"], td, gn, gt, oturum=object(), uyu=uyku.append)
        if sum(R16b["yeni"].values()) != 2:
            hata.append("16) indirici kaldığı yerden sürmedi")
        with gzip.open(os.path.join(td, "not", "A.json.gz")) as f:
            json.loads(f.read())
        h1 = K.k67_klasor_sha(td); K._k67_yaz_gz(os.path.join(td, "not", "A.json.gz"), json.dumps({"quoteSummary": {"result": [{"upgradeDowngradeHistory": {"history": []}}]}}).encode())
        if K.k67_klasor_sha(td) != h1:
            hata.append("16) aynı içerik yeniden yazılınca önbellek sha256'sı değişti (gzip başlığı sabit değil)")
        say["n"] = 100

        def hep429(_o, s):
            raise K._K67Sinir("HTTP 429")
        durmali(lambda: K.k67_indir(["Z"], td, hep429, gt, oturum=object(), uyu=lambda x: None), "16) üst üste 429'da indirici durmadı", hata)
    # 17) e-posta / anahtar yok
    for ad in ("K67.py", "test_k67.py"):
        metin = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if K._K67_EPOSTA.search(metin) or re.search(r"(api[_-]?key|token|password|sifre)\s*=\s*['\"][A-Za-z0-9]{8,}", metin, re.I):
            hata.append(f"17) {ad} içinde e-posta / anahtar biçimli parça var")
    if os.path.exists(gercek) and K._K67_EPOSTA.search(open(gercek, encoding="utf-8").read()):
        hata.append("17) ön kayıtta e-posta biçimli parça var")
    return hata


if __name__ == "__main__":
    h = testler()
    for x in h:
        print("HATA:", x)
    print("test_k67:", "TAMAM (17/17)" if not h else f"{len(h)} HATA")
    sys.exit(1 if h else 0)
