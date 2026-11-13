"""TAVAN_SERISI testleri — YALNIZ SENTETİK veri (ağ yok; gerçek fiyat ölçümü yok). Çalıştırma: python test_tavan_serisi.py

1) tavan sayımı: %10 rejiminde +%9,5 eşiği, 1-2 TL'de fiyat adımı (1,38 -> 1,51 = +%9,42 tavan), +%9,0 değil, +%12 değil (marj dışı), |r| > %25 kırık;
   %20 rejiminde (12.03.2020'ye kadar) +%9,6 tavan DEĞİL, +%19,6 tavan; bedelsiz çarpanıyla ekran fiyatı
2) ardışık sayaç ve seriler: uzunluk, ref derinlik (seri öncesi gün), kırıktan sonra 250 bar tepesi yeniden başlar
3) kilitli / tam kilitli gün; giriş günü = k. tavandan sonraki ilk bar açılışı; giriş günü tam kilitli tavansa dolum belirsiz
4) olay tablosu: k = 1, 2, 3 satırları, ertesi gün tavan, r5 elle, 60 gün penceresi kesiği aşınca NaN, kontrol (aynı kova, seri boyunca tavansız)
   ortalaması elle; seri içinde tavan yapan hisse kontrole girmez; ÇÖKMÜŞ / ÇÖKMEMİŞ sınıfı
5) özet + karar kategorileri (örneklem yetersiz / KONTROLDEN İYİ / KUMAR); bootstrap tohumla birebir; duyarlılık eşiği kopyası ana eşiği bozmaz
6) mühür kapısı: ön kayıt yok -> RET; git'te değil -> RET; commit sonrası geçer; eşik değişince RET; manifest farkı RET; kod farkı sapmasız RET
7) canlı tablo: kriz düşüşü, dipten kat, ardışık tavan (gün içi / kesin), veri kırığı evrene girmez; rapor metinleri yazılır
8) çakışma kapısı; kodda e-posta yok; yasak defter dosyalarına yazan kod yok
"""
from __future__ import annotations

import copy
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import TAVAN_SERISI as T  # noqa: E402

HATA: list = []


def kontrol(kosul: bool, mesaj: str) -> None:
    if not kosul:
        HATA.append(mesaj)


def durmali(fn, mesaj: str, icerik: str = "") -> None:
    try:
        fn()
    except (T.TsHata, RuntimeError) as ex:
        if icerik and icerik not in str(ex):
            HATA.append(f"{mesaj} (yanlış neden: {ex})")
        return
    HATA.append(mesaj)


def df(c, idx, o=None, h=None, l=None, v=None, carpan=None) -> pd.DataFrame:
    c = np.asarray(c, float); o = c.copy() if o is None else np.asarray(o, float)
    h = np.maximum(o, c) if h is None else np.asarray(h, float); l = np.minimum(o, c) if l is None else np.asarray(l, float)
    v = np.full(len(c), 1e6) if v is None else np.asarray(v, float)
    return pd.DataFrame({"o": o, "h": h, "l": l, "c": c, "v": v, "carpan": np.ones(len(c)) if carpan is None else carpan}, index=idx)


def t1_tavan_sayimi() -> None:
    idx = pd.bdate_range("2026-11-02", periods=8)
    c = [1.15, 1.26, 1.38, 1.51, 1.66, 1.809, 2.03, 2.60]   # +9,57 / +9,52 / +9,42 (adım) / +9,93 / +8,98 (değil) / +12,2 (marj dışı) / +28 kırık
    X = T.ts_tavan(df(c, idx))
    kontrol(X.tavan.tolist() == [False, True, True, True, True, False, False, False], f"1: tavan dizisi yanlış {X.tavan.tolist()}")
    kontrol(X.kirik.tolist() == [False] * 7 + [True], "1: kırık yanlış")
    kontrol(X.sayac.tolist() == [0, 1, 2, 3, 4, 0, 0, 0], f"1: sayaç yanlış {X.sayac.tolist()}")
    kontrol(abs(X.esik.iloc[3] - (1.51 / 1.38 - 1)) < 1e-6, "1: adım eşiği 1,38 -> 1,51 olmalı")
    kontrol(abs(X.esik.iloc[2] - 0.095) < 1e-9, "1: 1,26'da eşik %9,5 olmalı (adım kaybı küçük)")
    # %20 rejimi
    idx2 = pd.bdate_range("2019-06-03", periods=4)
    X2 = T.ts_tavan(df([10.0, 10.96, 13.11, 13.20], idx2))   # +%9,6 (değil) / +%19,6 (tavan) / +%0,7
    kontrol(X2.tavan.tolist() == [False, False, True, False], f"1: %20 rejimi yanlış {X2.tavan.tolist()}")
    kontrol(T.ts_marj(pd.DatetimeIndex(["2020-03-12", "2020-03-13"])).tolist() == [0.20, 0.10], "1: rejim sınırı 12/13 Mart 2020")
    # bedelsiz: Yahoo düzeltilmiş 0,69 x çarpan 2 = ekran 1,38 -> ekran tavanı 1,51 => düzeltilmiş 0,755 (+%9,42) tavan
    X3 = T.ts_tavan(df([0.69, 0.755], pd.bdate_range("2026-01-05", periods=2), carpan=np.array([2.0, 2.0])))
    kontrol(bool(X3.tavan.iloc[1]), "1: bölünme çarpanıyla ekran fiyatı adımı kullanılmalı")
    X4 = T.ts_tavan(df([0.69, 0.755], pd.bdate_range("2026-01-05", periods=2), carpan=np.array([20.0, 20.0])))
    kontrol(not bool(X4.tavan.iloc[1]), "1: ekran 13,8'de adım 0,01 -> %9,42 tavan değil")
    kontrol(list(T.ts_adim(np.array([1.0, 19.99, 20.0, 60.0, 120.0, 300.0, 600.0, 1500.0, 3000.0]))) ==
            [0.01, 0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.00, 2.50], "1: fiyat adımı tablosu")


def t2_seri_ve_derinlik() -> None:
    n = 300; idx = pd.bdate_range("2023-01-02", periods=n)
    c = np.r_[np.full(10, 100.0), 100 * 0.99 ** np.arange(1, 271), np.zeros(20)]
    c[280:] = c[279]
    c[285] = c[284] * 1.10; c[286] = round(c[285] * 1.10, 6); c[287:] = c[286]
    X = T.ts_tavan(df(c, idx)); R = T.ts_seriler(df(c, idx), X)
    kontrol(len(R) == 1 and int(R.L.iloc[0]) == 2 and int(R.bas_i.iloc[0]) == 285, f"2: seri yanlış {R.to_dict('records')}")
    beklenen = c[284] / c[35:285].max() - 1
    kontrol(abs(R.ref_derinlik.iloc[0] - beklenen) < 1e-9, f"2: ref derinlik {R.ref_derinlik.iloc[0]} != {beklenen}")
    kontrol(np.isnan(X.derinlik.iloc[248]) and np.isfinite(X.derinlik.iloc[249]), "2: 250 bar dolmadan derinlik tanımsız olmalı")
    c2 = c.copy(); c2[100:] = c2[100:] * 0.5   # kırık (-%50)
    X2 = T.ts_tavan(df(c2, idx))
    kontrol(bool(X2.kirik.iloc[100]) and np.isnan(X2.derinlik.iloc[299]), "2: kırıktan sonra 250 bar dolmadan derinlik tanımsız olmalı")


def t3_kilit_ve_giris() -> None:
    idx = pd.bdate_range("2026-03-02", periods=4)
    c = [1.00, 1.10, 1.21, 1.25]
    o = [1.00, 1.10, 1.21, 1.30]; h = [1.00, 1.10, 1.21, 1.31]; l = [1.00, 1.05, 1.21, 1.20]
    X = T.ts_tavan(df(c, idx, o=o, h=h, l=l))
    kontrol(X.kilitli.tolist() == [False, True, True, False], f"3: kilitli yanlış {X.kilitli.tolist()}")
    kontrol(X.tam_kilitli.tolist() == [False, False, True, False], f"3: tam kilitli yanlış {X.tam_kilitli.tolist()}")


def panel_kur():
    """A: çökmüş (-%88), 3 tavan (satır 300-302); B: aynı kova, tavansız (kontrol); C: aynı kova ama 301'de tavan (kontrol DIŞI);
    D: çökmüş değil, 2 tavan (300-301); E: derin kova (-%95), tavansız (başka kova -> kontrol dışı)."""
    n = 420; idx = pd.bdate_range("2021-01-04", periods=n)
    base = lambda son: np.r_[np.full(50, 100.0), 100 * (son / 100) ** (np.arange(1, 251) / 250), np.full(n - 300, son)]  # noqa: E731
    A = base(12.0); B = base(12.5); C = base(11.8); D = np.full(n, 50.0); Ee = base(5.0)
    for i in (300, 301, 302):
        A[i:] = A[i - 1] * 1.10
    A[303:] = A[302] * np.linspace(1.0, 1.5, n - 303)
    C[301:] = C[300] * 1.10
    for i in (300, 301):
        D[i:] = D[i - 1] * 1.10
    B[301:] = B[300] * np.linspace(1.0, 0.8, n - 301)
    S = {"A": df(A, idx), "B": df(B, idx), "C": df(C, idx), "D": df(D, idx), "E": df(Ee, idx)}
    # takvim için en az 10 hisse eşiği: dolgu hisseleri (sabit fiyat, çökmemiş)
    for i in range(6):
        S[f"Z{i}"] = df(np.full(n, 30.0 + i), idx)
    return S, idx


def t4_olaylar() -> None:
    S, idx = panel_kur(); kes = str(idx[400].date())
    P = T.ts_panel(S, kes=kes); U = T.ts_ufuk_panelleri(P)
    Ev = T.ts_olaylar(P, U, "2016-01-01", kes, True)
    a = Ev[Ev.sembol == "A"].set_index("k")
    kontrol(sorted(a.index.tolist()) == [1, 2, 3], f"4: A'da k = 1, 2, 3 olmalı {a.index.tolist()}")
    kontrol(a.loc[1, "ertesi_tavan"] and a.loc[2, "ertesi_tavan"] and not a.loc[3, "ertesi_tavan"], "4: ertesi gün tavan yanlış")
    kontrol((a.sinif == "COKMUS").all() and int(a.loc[1, "kova"]) == 1, f"4: A sınıf / kova yanlış {a[['sinif', 'kova']].to_dict()}")
    cA = S["A"].c.to_numpy(); oA = S["A"].o.to_numpy()
    e = 303
    kontrol(abs(a.loc[3, "r5"] - (cA[e + 4] / oA[e] - 1)) < 1e-9, "4: r5 elle tutmuyor")
    kontrol(a.loc[1, "e"] == idx[301] and abs(a.loc[1, "giris"] - oA[301]) < 1e-12, "4: giriş günü / fiyatı yanlış")
    kontrol(np.isnan(a.loc[3, "r120"]), "4: 120 gün penceresi kesiği aşıyor -> NaN olmalı")
    kontrol(np.isfinite(a.loc[3, "r60"]), "4: 60 gün penceresi kesik içinde -> ölçülmeli")
    # kontrol: k=3 için yalnız B (C seride tavan yaptı, E başka kova, D çökmemiş, Z'ler çökmemiş)
    cB = S["B"].c.to_numpy(); oB = S["B"].o.to_numpy()
    kontrol(int(a.loc[3, "n_kontrol"]) == 1, f"4: k=3 kontrol sayısı 1 olmalı (yalnız B), {a.loc[3, 'n_kontrol']}")
    kontrol(abs(a.loc[3, "k_r60"] - (cB[e + 59] / oB[e] - 1)) < 1e-9, "4: kontrol r60 elle tutmuyor")
    d = Ev[Ev.sembol == "D"]
    kontrol(len(d) == 2 and (d.sinif == "COKMEMIS").all(), "4: D çökmemiş 2 olay olmalı")
    c_ = Ev[Ev.sembol == "C"]
    kontrol(len(c_) == 1 and c_.sinif.iloc[0] == "COKMUS", "4: C'nin kendi 1 olayı olmalı")
    # dolum belirsiz: A'nın k=1 ve k=2 girişleri tam kilitli tavan günü (o = h = l = c)
    kontrol(bool(a.loc[1, "dolum_belirsiz"]) and bool(a.loc[2, "dolum_belirsiz"]) and not bool(a.loc[3, "dolum_belirsiz"]), "4: dolum belirsiz yanlış")


def t4b_kontrol_k1() -> None:
    """k=1: seri aralığı yalnız satır 300; C 300'de tavansız -> kontrol (B ve C); k=2 aralığı 300-301: C 301'de tavan -> dışarıda."""
    S, idx = panel_kur(); kes = str(idx[400].date())
    P = T.ts_panel(S, kes=kes); U = T.ts_ufuk_panelleri(P)
    Ev = T.ts_olaylar(P, U, "2016-01-01", kes, True); a = Ev[Ev.sembol == "A"].set_index("k")
    kontrol(int(a.loc[1, "n_kontrol"]) == 2 and int(a.loc[2, "n_kontrol"]) == 1, f"4b: kontrol sayıları {a.n_kontrol.tolist()}")


def t5_ozet_karar() -> None:
    rng = np.random.default_rng(1); n = 60
    Ek = pd.DataFrame({"sembol": [f"S{i % 20}" for i in range(n)], "k": 3, "L": rng.integers(3, 9, n), "durum": "tamam", "ertesi_tavan": rng.random(n) < 0.6,
                       "seri_acik": False, "dolum_belirsiz": False, "r5": 0.1, "r20": 0.1, "r60": 0.3 + rng.normal(0, 0.05, n), "r120": 0.2,
                       "up100_60": 0.0, "dn50_60": 0.0, "dn50_120": 0.0, "k_r60": 0.0, "k_up100_60": 0.0, "k_dn50_60": 0.1, "k_dn50_120": 0.1,
                       "n_kontrol": 3, "donem": ["2016-19", "2020-22", "2023-26.08"] * 20})
    o = T.ts_ozet_k(Ek); k = T.ts_karar(o)
    kontrol(k["karar"] == "KONTROLDEN İYİ", f"5: açık iyi örnek KONTROLDEN İYİ olmalı {k}")
    o2 = T.ts_ozet_k(Ek); kontrol(o2["fark_med_ci"] == o["fark_med_ci"], "5: bootstrap tohumla birebir olmalı")
    Ek2 = Ek.assign(r60=-0.2 + rng.normal(0, 0.05, n)); kontrol(T.ts_karar(T.ts_ozet_k(Ek2))["karar"].startswith("KUMAR"), "5: kötü örnek KUMAR olmalı")
    Ek3 = Ek.assign(dn50_60=1.0); kontrol(T.ts_karar(T.ts_ozet_k(Ek3))["karar"].startswith("KUMAR"), "5: P(-%50) yüksek -> KUMAR olmalı")
    kontrol(T.ts_karar(T.ts_ozet_k(Ek.iloc[:20]))["karar"] == "örneklem yetersiz", "5: n < 30 örneklem yetersiz")
    E6 = T.ts_esik_gevsek(-0.60)
    kontrol(E6["kontrol"]["kova"] == [-0.60, -0.60 + (-0.40) / 3, -0.60 + 2 * (-0.40) / 3] and T.TS_ESIK["olay"]["cokmus"]["esik"] == -0.80
            and T.ts_kova(-0.65, E6) == 0 and T.ts_kova(-0.90, E6) == 2, "5: duyarlılık kopyası / kovası yanlış (ana eşik değişmemeli)")
    kontrol(T.ts_kova(-0.82) == 0 and T.ts_kova(-0.87) == 1 and T.ts_kova(-0.95) == 2 and T.ts_kova(-0.5) == -1 and T.ts_kova(np.nan) == -1, "5: kova")


def t6_kapi() -> None:
    tmp = tempfile.mkdtemp(prefix="ts_kapi_")
    try:
        durmali(lambda: T.ts_kapi(tmp, git=False), "6: ön kayıt yokken kapı açılmamalı", "ön kayıt yok")
        y = os.path.join(tmp, T.TS_DOSYA["onkayit"]); man = "a" * 64
        with open(y, "w", encoding="utf-8") as f:
            f.write(f"x\nESIK_SHA256: {T.ts_esik_sha()}\nKOD_SHA256: {T.ts_kod_sha()}\nVERI_MANIFEST_SHA256: {man}\n")
        durmali(lambda: T.ts_kapi(tmp, git=True), "6: git'e işlenmemiş ön kayıtla kapı açılmamalı", "git")
        subprocess.run(["git", "-C", tmp, "init", "-q"], check=True)
        subprocess.run(["git", "-C", tmp, "add", T.TS_DOSYA["onkayit"]], check=True)
        subprocess.run(["git", "-C", tmp, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "on kayit"], check=True)
        K = T.ts_kapi(tmp, git=True, manifest=man)
        kontrol(K["kod_ayni"] and len(K["onkayit_git"]["commit"]) == 40, "6: commit sonrası kapı geçmeli")
        E2 = copy.deepcopy(T.TS_ESIK); E2["karar"]["n_min"] = 29
        durmali(lambda: T.ts_kapi(tmp, git=True, E=E2), "6: eşik değişince kapı açılmamalı", "eşik")
        durmali(lambda: T.ts_kapi(tmp, git=True, manifest="b" * 64), "6: manifest farkında kapı açılmamalı", "manifest")
        with open(y, "a", encoding="utf-8") as f:
            f.write("sonradan\n")
        durmali(lambda: T.ts_kapi(tmp, git=True), "6: ön kayıt commit sonrası değişince kapı açılmamalı", "farklı")
        with open(y, "w", encoding="utf-8") as f:
            f.write(f"x\nESIK_SHA256: {T.ts_esik_sha()}\nKOD_SHA256: {'0' * 64}\nVERI_MANIFEST_SHA256: {man}\n")
        durmali(lambda: T.ts_kapi(tmp, git=False), "6: kod farkında sapmasız kapı açılmamalı", "sapma")
        kontrol(T.ts_kapi(tmp, git=False, sapma="test")["sapma"] == "test", "6: sapma gerekçesiyle geçmeli")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def t7_canli_ve_rapor() -> None:
    idx = pd.bdate_range("2026-01-02", "2026-11-13")
    n = len(idx); c = np.full(n, 50.0); i9 = idx.get_loc(pd.Timestamp("2026-09-01"))
    c[i9:] = 50 * 0.9 ** np.arange(1, n - i9 + 1)   # taban serisi
    c = np.maximum(c, 1.0)
    j = n - 4
    for i in range(j, n):
        c[i] = c[i - 1] * 1.10
    S = {"X": df(c, idx)}
    c2 = np.full(n, 20.0); c2[i9 + 5:] = 2.0     # -%90 tek gün = kırık
    S["Y"] = df(c2, idx)
    simdi = dt.datetime(2026, 11, 13, 12, 0, tzinfo=dt.timezone.utc)
    Tt = T.ts_canli_tablo(S, simdi=simdi).set_index("sembol")
    kontrol(bool(Tt.loc["X", "cokmus"]) and Tt.loc["X", "ardisik_tavan_bugun_dahil"] == 4 and Tt.loc["X", "ardisik_tavan_kesin"] == 3,
            f"7: X canlı değerleri yanlış {Tt.loc['X'].to_dict()}")
    kontrol(bool(Tt.loc["X", "gun_ici"]), "7: 12:00 UTC gün içi sayılmalı")
    kontrol(not bool(Tt.loc["Y", "cokmus"]) and bool(Tt.loc["Y", "kirik_tepe_sonrasi"]), "7: kırıklı Y evrene girmemeli")
    simdi2 = dt.datetime(2026, 11, 13, 16, 0, tzinfo=dt.timezone.utc)
    kontrol(T.ts_canli_tablo(S, simdi=simdi2).set_index("sembol").loc["X", "ardisik_tavan_kesin"] == 4, "7: kapanış sonrası kesin = bugün dahil")
    md = T.ts_canli_md(Tt.reset_index(), {"son_tarih": "2026-11-13", "okunan": 2, "eksik": {}}, {"hisse": 0})
    kontrol("| X |" in md and "TEHOL" in md, "7: canlı md tablosu")
    # rapor: sentetik sonuç
    S2, idx2 = panel_kur(); kes = str(idx2[400].date())
    P = T.ts_panel(S2, kes=kes); U = T.ts_ufuk_panelleri(P); Ev = T.ts_olaylar(P, U, "2016-01-01", kes, True)
    son = {"kapi": {"esik_sha256": "0" * 64}, "cokmus": {}, "karar": {}, "cokmus_kilitsiz": {}, "cokmemis": {}, "bilgi": {"kes": kes, "k": {}}}
    for k in (1, 2, 3):
        Ck = Ev[(Ev.k == k) & (Ev.sinif == "COKMUS")]
        o = T.ts_ozet_k(Ck); son["cokmus"][k] = o; son["karar"][k] = T.ts_karar(o)
    md2 = T.ts_rapor_md(T._ts_kayit(son))
    kontrol("Olasılık tablosu" in md2 and "örneklem yetersiz" in md2, "7: rapor metni")


def t8_kapilar() -> None:
    kod = open(os.path.join(KOK, "TAVAN_SERISI.py"), encoding="utf-8").read()
    kontrol(not re.search(r"[\w.+-]+@[\w-]+\.(com|net|org|io|tr)\b", kod), "8: kodda e-posta biçimli metin var")
    for yasak in ("IZ_DEFTERI.md", "IZ_KARNE.py", "CLAUDE.md", "COL_OZET.md", "ONERI_DEFTERI.md"):
        kontrol(yasak not in kod.split('"""', 2)[2], f"8: kod {yasak} dosyasına atıf yapıyor (yalnız belge başında olabilir)")
    g = {"__name__": "ts_cakisma", "ts_kos": lambda: None}
    try:
        exec(compile(kod, "TAVAN_SERISI.py", "exec"), g)
        HATA.append("8: çakışma kapısı bellekteki ts_kos'u ezen yüklemeyi durdurmalı")
    except RuntimeError as ex:
        kontrol("EZDİ" in str(ex), f"8: çakışma kapısı yanlış neden {ex}")


if __name__ == "__main__":
    for t in (t1_tavan_sayimi, t2_seri_ve_derinlik, t3_kilit_ve_giris, t4_olaylar, t4b_kontrol_k1, t5_ozet_karar, t6_kapi, t7_canli_ve_rapor, t8_kapilar):
        try:
            t()
        except Exception as ex:  # noqa: BLE001  (test çerçevesi: beklenmeyen hata da hata sayılır)
            HATA.append(f"{t.__name__}: beklenmeyen {type(ex).__name__}: {ex}")
    if HATA:
        print("TEST HATALI:\n- " + "\n- ".join(HATA)); sys.exit(1)
    print("test_tavan_serisi: bütün testler geçti")
