"""KART_TUR1 testleri (yalnız SENTETİK veri; gerçek veri okunmaz). Çalıştırma: python test_kart_tur1.py

1) çakışma kapısı  2) KASA durumu -> açılmış bloklar / bakış no / hücreler; kesintili blok ve kesik tutarsızlığı durur
3) KASA kapısı: veri en geç tarihi > açık kesik ise durur, <= ise geçer; KASA dışı klasör (durum dosyası yok) durur
4) çeyrek etiketi  5) KT08 F15 / r5 = arastirma_cikti/canli/kazananlar.kz_ozellik (sentetik seride birebir; prefix aynı)
6) karar kuralı: TUTAR, KATKI−, BH düşer, ÖLÇÜLEMEDİ (n / güç, plasebo kapısı), İZ DEĞİL, KT00 GÖRMEDİ etkisi, KT10 ABD-ADAY, bakış dışı BİLGİ,
   açık veri işareti ve öteki ufuk işareti şartları  7) Bonferroni / BH sabitleri, m = 20, ufuklar (R45 bilgi)
8) ön kayıt kapısı (geçici git deposunda): işlenmiş + sha'lar aynı -> geçer; bağımlı sha farkı / KT_ESIK farkı / işlenmemiş değişiklik /
   hipotez farkı -> durur  9) 6 anlamlı basamak yuvarlaması  10) sızıntı taraması (e-posta / anahtar)  11) kontrol tablosu IZ_KARNE kapısından geçer
12) gerçek ön kayıt (varsa ve git'e işlenmişse) KASA 'ac' ön kayıt kapısından (KASA.ks_onkayit_kapi) ve kt_onkayit_kapisi'ndan geçer
"""
from __future__ import annotations

import json
import os
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
import KART_TUR1 as KT  # noqa: E402
import KASA as KS  # noqa: E402


def _durum(kl: str, kesik: str, acilan) -> None:
    os.makedirs(kl, exist_ok=True)
    json.dump({"acik_kesik": kesik, "acilan": list(acilan), "muhur_id": "test"}, open(os.path.join(kl, KS.KS_DURUM_AD), "w"))


def _seri(rng, idx):
    C = 20 * np.exp(np.cumsum(rng.normal(-0.001, 0.02, len(idx))))
    O = C * (1 + rng.normal(0, 0.003, len(idx))); H = np.maximum(O, C) * 1.01; L = np.minimum(O, C) * 0.99
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(1000, 10 ** 6, len(idx)).astype(float)},
                        index=pd.DatetimeIndex(idx))


# ------------------------------------------------------------------ 1
def test_cakisma_kapisi():
    kaynak = open(os.path.join(KOK, "KART_TUR1.py"), encoding="utf-8").read()
    ns = {"__name__": "kt_test"}
    exec(compile(kaynak, "KART_TUR1.py", "exec"), ns)
    exec(compile(kaynak, "KART_TUR1.py", "exec"), ns)            # aynı dosya yeniden: geçer
    ns2 = {"__name__": "kt_test", "kt_olc": 1}
    exec(compile(kaynak, "KART_TUR1.py", "exec"), ns2)           # kt_ önekli ad: geçer
    ns3 = {"__name__": "kt_test", "KOK": "başka modülün adı", "_CK_KAYIT": {}}
    try:
        exec(compile(kaynak.replace("KOK_KT = os.path", "KOK = 'ezen'\nKOK_KT = os.path", 1), "KART_TUR1.py", "exec"), ns3)
    except RuntimeError as ex:
        assert "EZDİ" in str(ex)
    else:
        raise AssertionError("çakışma kapısı önek dışı adı ezmeye izin verdi")


# ------------------------------------------------------------------ 2
def test_durum_bloklar():
    with tempfile.TemporaryDirectory() as td:
        kl = os.path.join(td, "acik")
        _durum(kl, "2022-12-31", [])
        D = KT.kt_durum(kl); assert D["blok_sayi"] == 0 and D["bakis_no"] == 0 and list(KT.kt_hucreler(D)) == ["acik"]
        _durum(kl, "2023-12-31", ["2023Q1", "2023Q2", "2023Q3", "2023Q4"])
        D = KT.kt_durum(kl); assert D["bakis_no"] == 1 and KT.kt_hucreler(D)["birikimli"] == ["2023-01-01", "2023-12-31"]
        _durum(kl, "2024-12-31", KT.kt_bloklar_beklenen(8)); assert KT.kt_durum(kl)["bakis_no"] == 2
        _durum(kl, "2023-06-30", ["2023Q1", "2023Q2"]); D = KT.kt_durum(kl); assert D["bakis_no"] == 0 and D["blok_sayi"] == 2
        _durum(kl, "2026-10-27", KT.kt_bloklar_beklenen(16)); assert KT.kt_durum(kl)["blok_sayi"] == 16
        for kes, ac in (("2023-06-30", ["2023Q2"]), ("2023-09-30", ["2023Q1", "2023Q2"]), ("2023-03-31", []), ("2022-12-31", ["2023Q1"])):
            _durum(kl, kes, ac)
            try:
                KT.kt_durum(kl)
            except KT.KTHata:
                pass
            else:
                raise AssertionError(f"tutarsız durum geçti: {kes} {ac}")
        try:
            KT.kt_durum(td)                      # KASA_DURUM.json yok
        except KT.KTHata:
            pass
        else:
            raise AssertionError("durum dosyasız klasör geçti")


# ------------------------------------------------------------------ 3
def test_kasa_kapisi_kesik():
    rng = np.random.default_rng(3)
    with tempfile.TemporaryDirectory() as td:
        kl = os.path.join(td, "acik"); _durum(kl, "2022-12-31", [])
        for ad in ("V_ABD.pkl", "V_AVR.pkl", "V_BIST.pkl", "k34_yahoo.pkl"):
            pd.to_pickle({"A": _seri(rng, pd.bdate_range("2022-01-03", "2022-12-30"))}, os.path.join(kl, ad))
        D = KT.kt_durum(kl); assert KT.kt_kasa(kl, D)["kesik"] == "2022-12-31"
        pd.to_pickle({"A": _seri(rng, pd.bdate_range("2022-01-03", "2023-01-05"))}, os.path.join(kl, "V_AVR.pkl"))
        try:
            KT.kt_kasa(kl, D)
        except KT.KTHata as ex:
            assert "KESİK AŞIMI" in str(ex)
        else:
            raise AssertionError("kesik aşımı geçti")
        os.remove(os.path.join(kl, "k34_yahoo.pkl"))
        try:
            KT.kt_veri_dosyalari(kl)
        except KT.KTHata:
            pass
        else:
            raise AssertionError("eksik veri dosyası geçti")


# ------------------------------------------------------------------ 4
def test_ceyrek():
    assert [KT.kt_ceyrek(x) for x in ("2023-01-02", "2023-03-31", "2023-04-01", "2024-12-31")] == ["2023Q1", "2023Q1", "2023Q2", "2024Q4"]
    assert KT.kt_bloklar_beklenen(6) == ["2023Q1", "2023Q2", "2023Q3", "2023Q4", "2024Q1", "2024Q2"]


# ------------------------------------------------------------------ 5
def test_f15_r5_kazananlar():
    sys.path.insert(0, os.path.join(KOK, "arastirma_cikti", "canli"))
    import kazananlar as KZ
    rng = np.random.default_rng(5); df = _seri(rng, pd.bdate_range("2019-01-01", "2021-06-30"))
    d = KT.YH._yh_hazir(df); T = list(d.index[[130, 200, 333, 500, len(d) - 1]])
    f, r = KT.kt_f15_r5(d, T)
    for t, a, b in zip(T, f, r):
        F = KZ.kz_ozellik(df, t)
        assert np.isclose(a, F["F15"], rtol=1e-12, atol=0) and np.isclose(b, F["r5"], rtol=1e-12, atol=0)
        fk, rk = KT.kt_f15_r5(KT.YH._yh_hazir(df[df.index <= t]), [t])             # prefix
        assert fk[0] == a and rk[0] == b
    f2, r2 = KT.kt_f15_r5(d, [d.index[50], d.index[3]])
    assert np.isnan(f2[0]) and np.isfinite(r2[0]) and np.isnan(r2[1])            # 120 kapanış yok / 5 bar yok


# ------------------------------------------------------------------ 6
def _hc(degis=None, n=500, guc=0.9):
    """Bütün kartlar x {15, 30} x pazar x {acik, birikimli}: varsayılan 'beklenen yönde TUTAR'."""
    sat = []
    for k, v in KT.KT_KART.items():
        s = 1 if v["yon"] == "+" else -1
        for H in (15, 30, 45):
            for P in ("ABD", "AVR", "BIST"):
                for hc in ("acik", "birikimli"):
                    r = {"kod": k, "yon": v["yon"], "pazar": P, "ufuk": H, "hucre": hc, "n": n, "guc": guc, "fark": 0.01 * s,
                         "sira": 0.5 + 0.05 * s, "l3o": 0.005 * s, "l3o_neg": 0.005 * s, "p": 0.001, "p_ters": 0.99, "plasebo_gecti": True,
                         "plasebo_fark": 0.0, "plasebo_tutar_pay": 0.02, "boot_alt_k": 0.003 if s > 0 else -0.02,
                         "boot_ust_k": 0.02 if s > 0 else -0.003, "Tp": s > 0, "Tn": s < 0}
                    if degis:
                        r = degis(r) or r
                    sat.append(r)
    return pd.DataFrame(sat)


def _et(Hc, nb=4):
    D = {"blok_sayi": nb, "bakis_no": 1 if nb == 4 else 2 if nb == 8 else 0}
    return dict(zip(*KT.kt_karar(Hc, D)[["kod", "etiket"]].to_numpy().T))


def test_karar_kurali():
    E = _et(_hc())
    assert E["KT00"] == "KONTROL GÖRDÜ" and E["KT01"] == "TUTAR" and E["KT08"] == "TUTAR" and E["KT10"] == "ABD-ADAY", E
    assert _et(_hc(), nb=5)["KT01"] == "BİLGİ (TUTAR)"
    assert _et(_hc(), nb=0)["KT01"].startswith("BİLGİ (blok yok")

    def ters(r):           # her şey ters yönde
        if r["kod"] != "KT00":
            s = -1 if r["yon"] == "+" else 1
            r.update({"fark": 0.01 * s, "sira": 0.5 + 0.05 * s, "l3o": 0.005 * s, "l3o_neg": 0.005 * s, "p": 0.99, "p_ters": 0.001,
                      "Tp": s > 0, "Tn": s < 0})
    E = _et(_hc(ters)); assert E["KT01"] == "KATKI−" and E["KT08"] == "KATKI−" and E["KT10"] == "ABD-ADAY (−)", E

    def bh(r):
        r["p"] = 0.2
    E = _et(_hc(bh)); assert E["KT01"].startswith("İZ DEĞİL"), E

    def kucuk(r):
        if r["kod"] == "KT03" and r["pazar"] == "AVR" and r["ufuk"] == 30 and r["hucre"] == "birikimli":
            r.update({"n": 20, "Tp": False})
    E = _et(_hc(kucuk)); assert E["KT03"] == "TUTAR", E          # R15 iki pazarda tutar, R30 işaret aynı -> yine TUTAR

    def kucuk2(r):
        if r["kod"] == "KT03" and r["pazar"] == "AVR" and r["hucre"] == "birikimli" and r["ufuk"] in (15, 30):
            r.update({"guc": 0.5, "Tp": False})
    E = _et(_hc(kucuk2)); assert E["KT03"] == "ÖLÇÜLEMEDİ", E

    def kapi(r):
        if r["kod"] == "KT04" and r["pazar"] == "ABD" and r["hucre"] == "birikimli" and r["ufuk"] in (15, 30):
            r.update({"plasebo_gecti": False, "Tp": False})
    E = _et(_hc(kapi)); assert E["KT04"] == "ÖLÇÜLEMEDİ", E

    def acik_ters(r):
        if r["kod"] == "KT05" and r["hucre"] == "acik" and r["pazar"] == "AVR":
            r["fark"] = -0.001
    E = _et(_hc(acik_ters)); assert E["KT05"].startswith("İZ DEĞİL"), E

    def h2_ters(r):        # R15 tutar ama R30 ABD işareti ters; R30 tutmuyor -> TUTAR değil
        if r["kod"] == "KT06" and r["hucre"] == "birikimli" and r["ufuk"] == 30 and r["pazar"] == "ABD":
            r.update({"fark": -0.001, "Tp": False})
    E = _et(_hc(h2_ters)); assert E["KT06"].startswith("İZ DEĞİL"), E

    def kt00_yok(r):       # KT00 görmez + kartlar tutmaz -> İZ DEĞİL yerine ÖLÇÜLEMEDİ (KT00)
        if r["kod"] == "KT00":
            r.update({"fark": -0.001, "Tp": False})
        else:
            r.update({"p": 0.5, "Tp": False, "Tn": False})
    E = _et(_hc(kt00_yok)); assert E["KT00"] == "KONTROL GÖRMEDİ" and E["KT01"].startswith("ÖLÇÜLEMEDİ (KT00"), E

    def kt00_kismen(r):
        if r["kod"] == "KT00":
            r["Tp"] = False
    assert _et(_hc(kt00_kismen))["KT00"] == "KONTROL KISMEN"

    def avr_yok_kt10(r):   # KT10 yalnız ABD'ye bakar: AVR satırları bozuk olsa da etkilemez
        if r["kod"] == "KT10" and r["pazar"] == "AVR":
            r.update({"fark": -1.0, "Tp": False, "n": 0})
    assert _et(_hc(avr_yok_kt10))["KT10"] == "ABD-ADAY"


# ------------------------------------------------------------------ 7
def test_sabitler():
    E = KT.KT_ESIK
    assert E["ufuk"]["karar"] == [15, 30] and E["ufuk"]["bilgi"] == [45] and E["ufuk"]["plasebo"] == [15, 30]
    assert E["bonferroni"]["boot_alt"] == 0.0125 and E["bonferroni"]["boot_ust"] == 0.9875 and E["bonferroni"]["bh_q"] == 0.05
    kar = [k for k, v in KT.KT_KART.items() if v["karar"]]
    assert E["bh"]["m"] == len(kar) * len(E["ufuk"]["karar"]) == 20 and "KT00" not in kar
    assert set(KT.KT_ESIK["bakis"]) >= {"4", "8"}
    assert KT.C2.C2_ESIK22["ufuklar"] == [15, 30, 45]


# ------------------------------------------------------------------ 8
def _git(args, kl):
    subprocess.run(["git"] + args, cwd=kl, check=True, capture_output=True)


def test_onkayit_kapisi():
    with tempfile.TemporaryDirectory() as td:
        _git(["init", "-q"], td); _git(["config", "user.email", "t@t"], td); _git(["config", "user.name", "t"], td)
        kod = os.path.join(td, "kod.py"); open(kod, "w").write("x = 1\n")
        b = KT.kt_bagimli_sha()
        metin = ["# ön kayıt", f"KASA_HIPOTEZ: {KT.KT_HIPOTEZ}", f"KASA_KOD: kod.py {KT._kt_sha(kod)}", f"KT_ESIK_SHA: {KT.kt_esik_sha()}", ""]
        metin += [f"BAGIMLI_SHA: {k} {v}" for k, v in b.items()] + ["", KT.kt_kontrol_tablosu(), ""]
        ok = os.path.join(td, "ok.md"); open(ok, "w", encoding="utf-8").write("\n".join(metin))
        _git(["add", "."], td); _git(["commit", "-qm", "on kayit".replace(" ", "_")], td)
        assert KT.kt_onkayit_kapisi(ok)["bagimli"] == len(b)
        for ad, eski, yeni in (("bagimli", f"BAGIMLI_SHA: CETVEL2.py {b['CETVEL2.py']}", "BAGIMLI_SHA: CETVEL2.py " + "0" * 64),
                               ("esik", f"KT_ESIK_SHA: {KT.kt_esik_sha()}", "KT_ESIK_SHA: " + "1" * 64),
                               ("hipotez", f"KASA_HIPOTEZ: {KT.KT_HIPOTEZ}", "KASA_HIPOTEZ: BASKA")):
            y = os.path.join(td, f"{ad}.md"); open(y, "w", encoding="utf-8").write("\n".join(metin).replace(eski, yeni))
            _git(["add", "."], td); _git(["commit", "-qm", ad], td)
            try:
                KT.kt_onkayit_kapisi(y)
            except KT.KTHata:
                pass
            else:
                raise AssertionError(f"ön kayıt kapısı {ad} farkında geçti")
        open(ok, "a", encoding="utf-8").write("sonradan\n")           # işlenmemiş değişiklik
        try:
            KT.kt_onkayit_kapisi(ok)
        except KT.KTHata:
            pass
        else:
            raise AssertionError("işlenmemiş ön kayıt geçti")
        _git(["checkout", "--", "ok.md"], td)
        open(kod, "w").write("x = 2\n"); _git(["add", "."], td); _git(["commit", "-qm", "kod"], td)
        try:
            KT.kt_onkayit_kapisi(ok)
        except KT.KTHata:
            pass
        else:
            raise AssertionError("kod sha farkı geçti")


# ------------------------------------------------------------------ 9-11
def test_yuvarlama_sizinti_kontrol():
    assert list(KT._r6(np.array([0.123456789, -0.0100000049, np.nan]))[:2]) == [0.123457, -0.01] and np.isnan(KT._r6([np.nan])[0])
    with tempfile.TemporaryDirectory() as td:
        for m in ("iletisim ali@ornek.com", "api_key = ABCDEFGHIJKLMNOPQRST"):
            try:
                KT._kt_yaz(os.path.join(td, "x.md"), m)
            except KT.KTHata:
                pass
            else:
                raise AssertionError("sızıntı taraması geçti")
        y = os.path.join(td, "k.md"); open(y, "w", encoding="utf-8").write("## KONTROL\n\n" + KT.kt_kontrol_tablosu() + "\n")
        import IZ_KARNE as IK
        assert IK.ik_kontrol_kapisi(y)["gecti"]
    src = open(os.path.join(KOK, "KART_TUR1.py"), encoding="utf-8").read()
    assert not [m for m in KT._KT_EPOSTA.findall(src) if m != "noreply@anthropic.com"]


# ------------------------------------------------------------------ 12
def test_gercek_onkayit_kapisi():
    y = KT.KT_YOL["onkayit"]
    if not os.path.exists(y):
        print("  (gerçek ön kayıt yok: atlandı)"); return
    r = subprocess.run(["git", "status", "--porcelain", "--", y], cwd=KOK, capture_output=True, text=True)
    if r.stdout.strip():
        print("  (gerçek ön kayıt git'e işlenmemiş: atlandı)"); return
    G = KS.ks_onkayit_kapi(y, KT.KT_HIPOTEZ, kontrol=True)
    assert {k["yol"] for k in G["kod"]} >= {"KART_TUR1.py", "CETVEL2.py"}
    assert KT.kt_onkayit_kapisi(y)["bagimli"] == len(KT.KT_BAGIMLI)


if __name__ == "__main__":
    testler = [(k, v) for k, v in list(globals().items()) if k.startswith("test_") and callable(v)]
    hata = 0
    for ad, f in testler:
        try:
            f(); print(f"GEÇTİ  {ad}")
        except Exception as ex:   # her test ayrı raporlanır
            hata += 1; print(f"KALDI  {ad}: {type(ex).__name__}: {ex}")
    print(f"{len(testler) - hata}/{len(testler)} test geçti")
    sys.exit(1 if hata else 0)
