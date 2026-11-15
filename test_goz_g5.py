"""GOZ_G5 testleri — YALNIZ SENTETİK veri + etiket dosyalarının okunması (ağ yok; gerçek fiyat / G5 ölçümü yok). Çalıştırma: python test_goz_g5.py

1) G5 bilinen sıkışma penceresini yakalar (pay >= 0,50), oynak bölgede yakalamaz; goz_satir yakaladi / bir_gun alanları doğru
2) rastgele pencere: aynı uzunluk, hiçbir yasak aralıkla kesişmez, ilk_bar / bas_tarih şartı, tohumla birebir, başka tohum başka, yer yoksa boş
3) ölçüler: geleceğe bakmaz (e sonrasındaki barlar bozulunca değer aynı); elle bilinen değerler (uzunluk, kapanış bandı, dip savunma); geçmiş yetmezse NaN
4) AUC elle (tam ayrım 1, ters 0, eşit 0,5, bağ yarım); LOSO AUC ve kural LOSO sentetik ayrımda yüksek; karar kategorileri (UYUYOR / ZAYIF / UYMUYOR)
5) etiketler: kalibre 30 COL + 8 OLUMSUZ, C 21 DEĞİL + 3 OBEK + 1 DEĞİL; tanımsız sınıf reddi; yasak listesi bütün etiketleri içerir
6) mühür kapısı: ön kayıt yok -> RET; git'te değil -> RET; commit sonrası geçer; eşik değişince RET; ön kayıt sonradan değişince RET; kod sha farkı sapmasız RET
7) uçtan uca sentetik koşu (git kapısı kapalı): A / B / C sonuç ve rapor yazılır; grafik repo içine yazmayı reddeder
8) çakışma kapısı; VDYT2.py / VDYT.py ön kayıttaki dedektörle aynı; kodda e-posta yok
"""
from __future__ import annotations

import copy
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
import GOZ_G5 as G  # noqa: E402

HATA: list = []


def kontrol(kosul: bool, mesaj: str) -> None:
    if not kosul:
        HATA.append(mesaj)


def durmali(fn, mesaj: str, icerik: str = "") -> None:
    try:
        fn()
    except (G.GozHata, RuntimeError) as ex:
        if icerik and icerik not in str(ex):
            HATA.append(f"{mesaj} (yanlış neden: {ex})")
        return
    HATA.append(mesaj)


def sentetik(n: int = 700, sik: tuple = (600, 660), tohum: int = 3, bas: str = "2021-01-01") -> pd.DataFrame:
    """Oynak rastgele yürüyüş + [sik) aralığında düz destekli, tepesi hafif inen küçük mumlu sıkışma."""
    rng = np.random.default_rng(tohum); idx = pd.bdate_range(bas, periods=n)
    r = rng.normal(0, 0.03, n); c = 100 * np.exp(np.cumsum(r)); o = np.r_[c[0], c[:-1]]
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.01, n))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.01, n)))
    a, b = sik; m = b - a; p = c[a - 1]; k = np.arange(m)
    cc = p * (1 + 0.002 * np.sin(k * 1.3)); oo = np.r_[p, cc[:-1]]
    hh = np.maximum(np.maximum(oo, cc) * 1.002 - 0.00002 * p * k, np.maximum(oo, cc)); ll = np.full(m, p * 0.996)
    c[a:b] = cc; o[a:b] = oo; h[a:b] = hh; l[a:b] = ll
    v = rng.uniform(5e5, 1.5e6, n)
    return pd.DataFrame(dict(o=o, h=h, l=l, c=c, v=v), index=idx)


def t1_g5_yakalama() -> None:
    d = sentetik(); Gd = G.goz_g5(d); tr = G._goz_tr(d)
    r = G.goz_satir("COL", "S_1", "S", d, 600, 659, Gd, tr, G.GOZ_ESIK)
    kontrol(r["g5_pay"] >= 0.5 and r["yakaladi"] == 1 and r["bir_gun"] == 1, f"1: sıkışma yakalanmadı (pay {r['g5_pay']:.2f})")
    q = G.goz_satir("RASTGELE", "S_R", "S", d, 400, 459, Gd, tr, G.GOZ_ESIK)
    kontrol(q["yakaladi"] == 0, f"1: oynak bölge yakalandı (pay {q['g5_pay']:.2f})")
    kontrol(q["tanimli_pay"] == 1.0 and r["tanimli_pay"] == 1.0, "1: tanımlılık yanlış")
    e = G.goz_satir("RASTGELE", "S_E", "S", d, 5, 30, Gd, tr, G.GOZ_ESIK)
    kontrol(e["tanimli_pay"] == 0.0 and e["yakaladi"] == 0, "1: geçmişi yetmeyen bölge tanımlı / yakalandı sayıldı")


def t2_rastgele() -> None:
    d = sentetik(n=900); ix = d.index
    yasak = [(ix[600], ix[659]), (ix[300], ix[320])]
    P, uy = G.goz_rastgele(d, 60, yasak, "x|S|1")
    kontrol(len(P) == 20 and uy > 20, f"2: pencere sayısı {len(P)}")
    for b, e in P:
        kontrol(e - b + 1 == 60, "2: uzunluk farklı")
        kontrol(b >= 260 and ix[b] >= pd.Timestamp("2022-01-01"), "2: ilk_bar / bas_tarih ihlali")
        for yb, ye in yasak:
            kontrol(not (ix[b] <= ye and ix[e] >= yb), "2: yasak aralıkla kesişme")
        kontrol(e < len(d), "2: seri dışı")
    P2, _ = G.goz_rastgele(d, 60, yasak, "x|S|1"); P3, _ = G.goz_rastgele(d, 60, yasak, "x|S|2")
    kontrol(P == P2, "2: aynı tohum farklı sonuç"); kontrol(P != P3, "2: farklı tohum aynı sonuç")
    P4, uy4 = G.goz_rastgele(d.iloc[:300], 60, [], "x")
    kontrol(P4 == [] and uy4 == 0, "2: yer yokken pencere üretildi")
    E = copy.deepcopy(G.GOZ_ESIK); E["A"]["rastgele"]["n"] = 10 ** 6
    P5, uy5 = G.goz_rastgele(d, 60, yasak, "x", E)
    kontrol(len(P5) == uy5 and len(set(P5)) == len(P5), "2: uygun < n iken hepsi tekrarsız alınmadı")


def t3_olculer() -> None:
    d = sentetik(); m0 = G.goz_olculer(d, 600, 659)
    d2 = d.copy(); d2.iloc[660:, :4] = d2.iloc[660:, :4] * 3.0; d2.iloc[660:, 4] = 1e9
    m1 = G.goz_olculer(d2, 600, 659)
    kontrol(all((np.isnan(m0[k]) and np.isnan(m1[k])) or m0[k] == m1[k] for k in m0), "3: ölçü geleceğe bakıyor")
    kontrol(m0["uzunluk"] == 60.0, "3: uzunluk")
    c = d.c.to_numpy()[600:660]
    kontrol(abs(m0["kapanis_bant"] - (c.max() - c.min()) / np.median(c)) < 1e-12, "3: kapanış bandı")
    kontrol(m0["dip_savunma"] == 0.0, "3: düz destekte dip savunma 0 değil")
    kontrol(len(m0) == 10 and set(m0) == set(G.GOZ_ESIK["B"]["olculer"]), "3: ölçü listesi ön kayıttakiyle aynı değil")
    sp, sec = G.goz_dip_savunma(np.array([5.0, 1.0, 1.1, 9, 9, 9, 9, 2.0, 9, 9, 9, 9, 9, 3.0]), 3, 5)
    kontrol(sec == [1, 7, 13] and abs(sp - 2.0) < 1e-12, f"3: dip seçimi {sec} {sp}")
    sp2, _ = G.goz_dip_savunma(np.array([1.0, 2.0, 3.0]), 3, 5)
    kontrol(np.isnan(sp2), "3: 3 dip yokken NaN değil")
    m2 = G.goz_olculer(d, 20, 40)
    kontrol(np.isnan(m2["aralik_atr"]) and np.isnan(m2["dusus120"]) and np.isnan(m2["hacim_oran"]), "3: geçmiş yetmezken NaN değil")
    durmali(lambda: G.goz_olculer(d, 650, 640), "3: ters pencere kabul edildi", "sınır dışı")


def t4_istatistik() -> None:
    kontrol(G.goz_auc(np.array([3, 4.0]), np.array([1, 2.0])) == 1.0, "4: AUC tam")
    kontrol(G.goz_auc(np.array([1, 2.0]), np.array([3, 4.0])) == 0.0, "4: AUC ters")
    kontrol(G.goz_auc(np.array([1.0, 1.0]), np.array([1.0])) == 0.5, "4: AUC eşit")
    kontrol(abs(G.goz_auc(np.array([2.0, 3.0]), np.array([2.0, 1.0])) - 0.875) < 1e-12, "4: AUC bağ")
    kontrol(np.isnan(G.goz_auc(np.array([np.nan]), np.array([1.0]))), "4: boş AUC NaN değil")
    rng = np.random.default_rng(0); rows = []
    for s in range(8):
        rows.append({"grup": "COL", "sembol": f"S{s}", "x": rng.normal(-2, 0.3), "y": rng.normal()})
        for j in range(10):
            rows.append({"grup": "RASTGELE", "sembol": f"S{s}", "x": rng.normal(0, 0.3), "y": rng.normal()})
    R = pd.DataFrame(rows)
    L = G.goz_loso_auc(R, "x"); kontrol(L["auc"] > 0.95 and L["n_col"] == 8 and L["n_rastgele"] == 80, f"4: LOSO {L}")
    K = G.goz_kural_loso(R, ["x"]); kontrol(K["J"] > 0.6, f"4: kural LOSO J {K['J']}")
    k = G.goz_kural_kur(R, ["x"]); kontrol(k[0]["yon"] == -1, "4: yön")
    kontrol(G.goz_karar_A(0.8, 0.3, 0.5) == "G5 GÖZE UYUYOR", "4: karar UYUYOR")
    kontrol(G.goz_karar_A(0.8, 0.45, 0.5) == "ZAYIF", "4: karar ZAYIF (2 kat yok)")
    kontrol(G.goz_karar_A(0.8, 0.3, 0.9) == "ZAYIF", "4: karar ZAYIF (olumsuz üstte)")
    kontrol(G.goz_karar_A(0.45, 0.0, 0.0) == "UYMUYOR", "4: karar UYMUYOR")
    kontrol(G.goz_karar_A(0.6, 0.45, 0.0) == "UYMUYOR", "4: karar UYMUYOR (1,5 kat yok)")
    R["yakaladi"] = (R.x < -1).astype(int)
    Bt = G.goz_bootstrap_A(R.assign(grup=R.grup))
    kontrol(Bt["COL"][0] is not None and Bt["COL"][0] <= Bt["COL"][1], "4: bootstrap aralığı")


def t5_etiket() -> None:
    A = G.goz_etiket_ana(); vc = A.sinif.value_counts().to_dict()
    kontrol(vc == {"COL": 30, "OLUMSUZ": 8}, f"5: ana sayım {vc}")
    C, cik = G.goz_etiket_c(ana=A); vc = C.sinif.value_counts().to_dict()
    kontrol(vc == {"DEGIL": 22, "OBEK": 3} and cik == [], f"5: C sayım {vc} {cik}")
    Y = G.goz_yasak(A, C); kontrol(sum(len(v) for v in Y.values()) == len(A) + len(C), "5: yasak listesi eksik")
    tmp = tempfile.mkdtemp()
    try:
        y = os.path.join(tmp, "k.csv"); pd.DataFrame({"sembol": ["X"], "bas": ["2025-01-01"], "son": ["2025-02-01"], "sinif": ["BELKI"]}).to_csv(y, index=False)
        durmali(lambda: G.goz_etiket_ana(y), "5: bilinmeyen sınıf kabul edildi", "bilinmeyen")
        A2 = pd.DataFrame({"id": ["ARZUM_x"], "sembol": ["ARZUM"], "bas": [pd.Timestamp("2025-10-01")], "son": [pd.Timestamp("2025-10-20")],
                           "sinif": ["COL"], "kaynak": ["t"]})
        _C2, cik2 = G.goz_etiket_c(ana=A2); kontrol(cik2 == ["COB_1_ARZUM"], f"5: örtüşen C kutusu çıkarılmadı {cik2}")
    finally:
        shutil.rmtree(tmp)


def git(kl: str, *a: str) -> str:
    return subprocess.run(["git", "-C", kl, "-c", "user.name=goz", "-c", "user.email=goz@test.invalid"] + list(a), capture_output=True, text=True,
                          check=True).stdout


def t6_muhur() -> None:
    tmp = tempfile.mkdtemp()
    try:
        durmali(lambda: G.goz_kapi(tmp, git=False), "6: ön kayıt yokken geçti", "ön kayıt yok")
        y = os.path.join(tmp, G.GOZ_DOSYA["onkayit"])
        G._goz_yaz(y, G.goz_onkayit_metin("2026-11-13 00:00:00 UTC", {"test": 1}))
        git(tmp, "init", "-q")
        durmali(lambda: G.goz_kapi(tmp), "6: git'te olmayan ön kayıt geçti", "işlenmemiş")
        git(tmp, "add", "."); git(tmp, "commit", "-q", "-m", "on kayit")
        K = G.goz_kapi(tmp); kontrol(K["kod_ayni"] and len(K["onkayit_git"]["commit"]) == 40, "6: işlenmiş ön kayıt geçmedi")
        E = copy.deepcopy(G.GOZ_ESIK); E["A"]["yakalama_pay"] = 0.4
        durmali(lambda: G.goz_kapi(tmp, E=E), "6: eşik değişince geçti", "eşik mührü")
        with open(y, "a", encoding="utf-8") as f:
            f.write("\nsonradan\n")
        durmali(lambda: G.goz_kapi(tmp), "6: sonradan değişen ön kayıt geçti", "farklı")
        git(tmp, "checkout", "-q", "--", G.GOZ_DOSYA["onkayit"])
        t = open(y, encoding="utf-8").read(); t = re.sub(r"^KOD_SHA256: [0-9a-f]{64}$", "KOD_SHA256: " + "0" * 64, t, flags=re.M)
        G._goz_yaz(y, t); git(tmp, "commit", "-q", "-am", "kod farki")
        durmali(lambda: G.goz_kapi(tmp), "6: kod sha farkı sapmasız geçti", "sapma")
        K2 = G.goz_kapi(tmp, sapma="test gerekçesi"); kontrol(K2["sapma"] == "test gerekçesi" and not K2["kod_ayni"], "6: sapma kaydı")
        durmali(lambda: G.goz_onkayit(tmp, {}, {}), "6: ön kayıt üzerine yazıldı", "zaten var")
    finally:
        shutil.rmtree(tmp)


def t7_uctan_uca() -> None:
    tmp = tempfile.mkdtemp()
    try:
        S = {}; rows = []
        for i in range(6):
            d = sentetik(n=900, sik=(700, 760), tohum=10 + i); S[f"S{i}"] = d
            rows.append({"sembol": f"S{i}", "bas": d.index[700], "son": d.index[759], "sinif": "COL"})
        d = sentetik(n=900, sik=(700, 760), tohum=99); S["O1"] = d
        rows.append({"sembol": "O1", "bas": d.index[400], "son": d.index[440], "sinif": "OLUMSUZ"})
        A = pd.DataFrame(rows); A["id"] = A.sembol + "_" + A.bas.dt.strftime("%Y%m%d"); A["kaynak"] = "t"
        C = pd.DataFrame([{"id": "C1", "sembol": "O1", "bas": d.index[700], "son": d.index[759], "sinif": "OBEK", "kaynak": "t"},
                          {"id": "C2", "sembol": "O1", "bas": d.index[500], "son": d.index[540], "sinif": "DEGIL", "kaynak": "t"}])
        H = G.goz_hazirla(S, S, ana=A, C=C, c_cik=[]); R = H["R"]
        kontrol(H["kapsam"]["sayim"] == {"COL": 6, "OLUMSUZ": 1, "RASTGELE": 120, "C_DEGIL": 1, "C_OBEK": 1}, f"7: sayım {H['kapsam']['sayim']}")
        TA = G.goz_test_A(R); kontrol(TA["COL"]["yakalama"] == 1.0 and TA["RASTGELE"]["yakalama"] < 0.1, f"7: A {TA['COL']} {TA['RASTGELE']}")
        kontrol(TA["karar"] == "G5 GÖZE UYUYOR", f"7: A karar {TA['karar']}")
        TB = G.goz_test_B(R); kontrol("aralik_atr" in TB["aday"] and TB["kural"] is not None, f"7: B aday {TB['aday']}")
        TC = G.goz_test_C(R, TB); kontrol(TC["karar"] in ("C TUTTU", "C TUTMADI") and TC["n_obek"] == 1, f"7: C {TC}")
        TC0 = G.goz_test_C(R, {"kural": None}); kontrol(TC0["karar"].startswith("C YAPILMADI"), "7: aday yokken C")
        G._goz_yaz(os.path.join(tmp, G.GOZ_DOSYA["onkayit"]), G.goz_onkayit_metin("t", {}))
        orj_a, orj_c = G.goz_etiket_ana, G.goz_etiket_c
        try:
            G.goz_etiket_ana = lambda yol=None: A  # type: ignore
            G.goz_etiket_c = lambda kutu=None, obek=None, ana=None: (C, [])  # type: ignore
            Sn = G.goz_kos(tmp, git=False, S_test=S, S_canli=S)
        finally:
            G.goz_etiket_ana, G.goz_etiket_c = orj_a, orj_c
        kontrol(os.path.exists(os.path.join(tmp, G.GOZ_DOSYA["sonuc"])) and os.path.exists(os.path.join(tmp, G.GOZ_DOSYA["rapor"])), "7: çıktı yok")
        md = open(os.path.join(tmp, G.GOZ_DOSYA["rapor"]), encoding="utf-8").read()
        kontrol("Test A" in md and Sn["A"]["karar"] in md, "7: rapor eksik")
        kontrol(G.goz_rapor(tmp).endswith(G.GOZ_DOSYA["rapor"]), "7: rapor yeniden yazılamadı")
        durmali(lambda: G.goz_grafik(tmp, os.path.join(KOK, "arastirma_cikti", "goz_g5_png"), S_test=S), "7: repo içine grafik yazıldı", "repoya")
        png = G.goz_grafik(tmp, os.path.join(tmp, "png"), S_test=S)
        kontrol(len(png) == 6 and all(os.path.getsize(p) > 1000 for p in png), f"7: grafik {len(png)}")
        sec = G.goz_grafik_sec(G._goz_json_oku(os.path.join(tmp, G.GOZ_DOSYA["sonuc"])))
        kontrol([r["id"] for r in sec] == [r["id"] for r in G.goz_grafik_sec(G._goz_json_oku(os.path.join(tmp, G.GOZ_DOSYA["sonuc"])))], "7: seçim tohumsuz")
        kontrol(sum(r["grup"] == "COL" for r in sec) == 3 and sum(r["grup"] == "RASTGELE" for r in sec) == 3, "7: grafik grupları")
    finally:
        shutil.rmtree(tmp)


def t8_kapilar() -> None:
    ns = {"goz_auc": "baska", "__file__": os.path.join(KOK, "GOZ_G5.py"), "__name__": "goz_test_ns"}
    try:
        exec(compile(open(os.path.join(KOK, "GOZ_G5.py"), encoding="utf-8").read(), "GOZ_G5.py", "exec"), ns)
        HATA.append("8: çakışma kapısı ad ezmeyi yakalamadı")
    except RuntimeError as ex:
        kontrol("goz_auc" in str(ex), f"8: çakışma nedeni {ex}")
    ns2 = {"__file__": os.path.join(KOK, "GOZ_G5.py"), "__name__": "goz_test_ns2"}
    exec(compile(open(os.path.join(KOK, "GOZ_G5.py"), encoding="utf-8").read(), "GOZ_G5.py", "exec"), ns2)
    exec(compile(open(os.path.join(KOK, "GOZ_G5.py"), encoding="utf-8").read(), "GOZ_G5.py", "exec"), ns2)   # aynı dosya ikinci kez: geçer
    try:
        G.goz_vdyt2_denetim()
    except G.GozHata as ex:
        HATA.append(f"8: {ex}")
    for f in ("GOZ_G5.py", "test_goz_g5.py"):
        t = open(os.path.join(KOK, f), encoding="utf-8").read()
        kontrol(not re.search(r"[\w.+-]+@(?!test\.invalid)[\w-]+\.(com|net|org|edu|gov|io|tr)\b", t), f"8: {f} içinde e-posta")
        kontrol(not re.search(r"(api[_-]?key|token)\s*=\s*['\"][A-Za-z0-9]{16,}", t, re.I), f"8: {f} içinde anahtar")


if __name__ == "__main__":
    for fn in (t1_g5_yakalama, t2_rastgele, t3_olculer, t4_istatistik, t5_etiket, t6_muhur, t7_uctan_uca, t8_kapilar):
        n0 = len(HATA)
        try:
            fn()
        except Exception as ex:  # noqa: BLE001
            HATA.append(f"{fn.__name__}: beklenmeyen {type(ex).__name__}: {ex}")
        print(f"{fn.__name__}: {'TAMAM' if len(HATA) == n0 else 'HATA'}")
    if HATA:
        print("\n".join(HATA)); sys.exit(1)
    print("test_goz_g5: 8/8 TAMAM")
