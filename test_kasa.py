"""KASA testleri (yalnız SENTETİK veri; gerçek veri mühürlenmez). Çalıştırma: python test_kasa.py

1) çakışma kapısı  2) kur: gizli yol repo içinde reddedilir, 0600, üzerine yazılmaz, açık anahtar üzerine yazılmaz
3) mühürle: açık kısımda kesikten sonra satır yok, kesikten sonra doğan sembol açık kısımda yok, manifest fiyat içermez, kasa dosyası düz metin sızdırmaz
4) şifreli blok anahtarsız / yanlış anahtarla / değiştirilmiş dosyayla açılmaz  5) KASA_GIZLI yoksa aç durur
6) ön kayıt kapısı: işlenmemiş / sonradan değişmiş ön kayıt, kod sha farkı, kod değişmiş, hipotez farkı, boş kontrol tablosu -> durur
7) sıra atlama durur  8) tek kullanım: aynı (blok, hipotez) ikinci açma durur; açılıştan sonra yazılmış başka hipotez durur, önce yazılmış geçer
9) bütün bloklar açılınca birleşik veri özgünle değer / dizin / dtype eşit; açık kesik doğru  10) denetim: kesik aşımı (pkl / csv / iç içe),
   tarihsiz dosya fail-closed, CLI çıkış kodu  11) gizli yol hiçbir çıktıda (stdout / stderr / log / manifest / defter / durum) geçmez
12) openssl arka ucu: tur, çapraz uyum (cryptography anahtarı <-> openssl), parola  13) muhurle --ekle: yeni veri parça blok, sıra sürer
14) ay blokları ve kuru sayım  15) e-posta / anahtar yok.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
warnings.filterwarnings("ignore", category=RuntimeWarning)
import KASA as K  # noqa: E402

KESIK = "2025-12-31"
DOSYALAR = ["V_ABD.pkl", "V_AVR.pkl", "V_BIST.pkl"]


def _seri(rng, idx, kur=False):
    C = 20 * np.exp(np.cumsum(rng.normal(0.0003, 0.02, len(idx))))
    O = C * (1 + rng.normal(0, 0.003, len(idx))); H = np.maximum(O, C) * 1.01; L = np.minimum(O, C) * 0.99
    d = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(1000, 10**6, len(idx)).astype(float)},
                     index=pd.DatetimeIndex(idx).astype("datetime64[s]"))
    if kur:
        d["Kur"] = 1.1
    return d


def _evren(tohum=1, son="2026-08-14"):
    rng = np.random.default_rng(tohum); V = {}
    tam = pd.bdate_range("2024-07-01", son)
    for ad in DOSYALAR:
        X = {}
        for i in range(8):
            X[f"S{i:02d}"] = _seri(rng, tam, kur=(ad == "V_AVR.pkl"))
        X["YENI"] = _seri(rng, pd.bdate_range("2026-02-02", son), kur=(ad == "V_AVR.pkl"))       # kesikten sonra doğan
        X["BATAN"] = _seri(rng, pd.bdate_range("2024-07-01", "2025-10-31"), kur=(ad == "V_AVR.pkl"))  # kesikten önce biten
        s = _seri(rng, tam, kur=(ad == "V_AVR.pkl")); X["SIRASIZ"] = s.iloc[rng.permutation(len(s))]   # sırasız seri
        V[ad] = X
    return V


def _kaynak_yaz(kl, V):
    os.makedirs(kl, exist_ok=True)
    for ad, X in V.items():
        pd.to_pickle(X, os.path.join(kl, ad))


def _cli(args, env_ek=None, gizli=None):
    env = dict(os.environ); env.pop("KASA_GIZLI", None)
    if gizli:
        env["KASA_GIZLI"] = gizli
    env.update(env_ek or {})
    r = subprocess.run([sys.executable, os.path.join(KOK, "KASA.py")] + args, capture_output=True, text=True, env=env, timeout=600)
    return r.returncode, r.stdout + r.stderr


def _git(kl, *a, tarih=None):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t.invalid", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t.invalid")
    if tarih:
        env["GIT_COMMITTER_DATE"] = tarih; env["GIT_AUTHOR_DATE"] = tarih
    r = subprocess.run(["git", "-C", kl] + list(a), capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"git {a}: {r.stderr}")
    return r.stdout


def _kontrol_tablosu(dolu=True):
    import IZ_KARNE as IK
    s = ["## KONTROL LİSTESİ", "", "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        s.append(f"| {k['kod']} | {k.get('ad', '')} | {'EVET' if dolu else ''} | {'sentetik test kanıt satırı' if dolu else ''} |")
    return "\n".join(s)


def _onkayit(repo, ad, hipotez, kod_ad, tarih=None, dolu=True, commit=True):
    kod = os.path.join(repo, kod_ad)
    if not os.path.exists(kod):
        with open(kod, "w") as f:
            f.write(f"# hipotez kodu {kod_ad}\nprint('olc')\n")
        _git(repo, "add", kod_ad); _git(repo, "commit", "-m", f"kod {kod_ad}", tarih=tarih)
    sha = K._sha_dosya(kod)
    yol = os.path.join(repo, ad)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(f"# Ön kayıt {hipotez}\n\nKASA_HIPOTEZ: {hipotez}\nKASA_KOD: {kod_ad} {sha}\n\n{_kontrol_tablosu(dolu)}\n")
    if commit:
        _git(repo, "add", ad); _git(repo, "commit", "-m", f"onkayit {hipotez}", tarih=tarih)
    return yol


def _beklenen_hata(fn, parca, etiket, hata):
    try:
        fn()
        hata.append(f"{etiket}: durmadı")
    except K.KasaHata as ex:
        if parca and parca not in str(ex):
            hata.append(f"{etiket}: yanlış hata: {ex}")


def testler():
    hata = []
    # 1) çakışma kapısı
    kod = open(os.path.join(KOK, "KASA.py"), encoding="utf-8").read()
    try:
        exec(compile(kod, "KASA.py", "exec"), {"__name__": "colab_benzeri", "ks_bol": "baska_dosyanin_adi"})
        hata.append("1) çakışma kapısı bellekteki adı ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) çakışma kapısı yanlış hata: {ex}")
    g2 = {"__name__": "colab_benzeri"}
    try:
        exec(compile(kod, "KASA.py", "exec"), g2); exec(compile(kod, "KASA.py", "exec"), g2)
    except RuntimeError as ex:
        hata.append(f"1) aynı dosyanın yeniden yüklenmesi durdu: {ex}")

    kok = tempfile.mkdtemp(prefix="kasa_test_")
    gizli_kl = tempfile.mkdtemp(prefix="gz_ozel_")
    os.chmod(gizli_kl, 0o700)
    gizli = os.path.join(gizli_kl, "anahtar_gizli_bunu_ara.pem")
    ciktilar = []   # bütün CLI çıktıları (11)
    try:
        kaynak, kasa = os.path.join(kok, "veri"), os.path.join(kok, "kasa")
        ciz = os.path.join(kok, "cikti"); os.makedirs(ciz)
        aa, man, dft = os.path.join(ciz, "acik.pem"), os.path.join(ciz, "MANIFEST.json"), os.path.join(ciz, "DEFTER.md")
        V2 = _evren(son="2026-10-30")   # tam seri; ilk mühür 2026-08-14'te kesilmiş kopyayla yapılır (13: --ekle kalanı mühürler)
        V = {ad: {s: d[d.index <= pd.Timestamp("2026-08-14")] for s, d in X.items()} for ad, X in V2.items()}
        _kaynak_yaz(kaynak, V)

        # 2) kur
        rc, o = _cli(["kur", "--gizli", os.path.join(KOK, "gizli_deneme.pem"), "--acik-anahtar", aa]); ciktilar.append(o)
        if rc == 0 or os.path.exists(os.path.join(KOK, "gizli_deneme.pem")):
            hata.append("2) repo içine gizli anahtar yazıldı")
        rc, o = _cli(["kur", "--acik-anahtar", aa]); ciktilar.append(o)
        if rc == 0:
            hata.append("2) gizli yol yokken kur çalıştı")
        rc, o = _cli(["kur", "--acik-anahtar", aa], gizli=gizli); ciktilar.append(o)
        if rc != 0 or not os.path.exists(gizli) or not os.path.exists(aa):
            hata.append(f"2) kur başarısız: {o[-300:]}")
            return hata
        if stat.S_IMODE(os.stat(gizli).st_mode) != 0o600:
            hata.append("2) gizli anahtar 0600 değil")
        g_once = open(gizli, "rb").read()
        rc, o = _cli(["kur", "--acik-anahtar", aa, "--uzerine"], gizli=gizli); ciktilar.append(o)
        if rc == 0 or open(gizli, "rb").read() != g_once:
            hata.append("2) var olan gizli anahtarın üzerine yazıldı")
        rc, o = _cli(["kur", "--acik-anahtar", aa], gizli=os.path.join(gizli_kl, "baska.pem")); ciktilar.append(o)
        if rc == 0:
            hata.append("2) açık anahtar --uzerine olmadan değişti")

        # 3) mühürle
        rc, o = _cli(["muhurle", "--kesik", KESIK, "--cikti", kasa, "--kaynak", kaynak, "--acik-anahtar", aa, "--manifest", man]); ciktilar.append(o)
        if rc != 0:
            hata.append(f"3) mühürle başarısız: {o[-500:]}"); return hata
        M = json.load(open(man))
        bl = K._blok_listesi(M)
        if bl != ["2026Q1", "2026Q2", "2026Q3"]:
            hata.append(f"3) blok listesi {bl}")
        for ad in DOSYALAR:
            A = pd.read_pickle(os.path.join(kasa, "acik", ad))
            if any(len(d) and K._gun_ix(d).max() > pd.Timestamp(KESIK) for d in A.values()):
                hata.append(f"3) {ad} açık kısımda kesikten sonra satır var")
            if "YENI" in A:
                hata.append(f"3) {ad} kesikten sonra doğan sembol açık kısımda (evren sızıntısı)")
            if "BATAN" not in A or not A["BATAN"].equals(V[ad]["BATAN"]):
                hata.append(f"3) {ad} kesikten önce biten seri eksik / farklı")
            if set(A["S00"].columns) != set(V[ad]["S00"].columns) or A["S00"].index.dtype != V[ad]["S00"].index.dtype:
                hata.append(f"3) {ad} açık kısım biçimi değişti")
        mtxt = open(man).read()
        fiyat = f"{V['V_ABD.pkl']['S00']['Close'].iloc[-1]:.6f}"[:8]
        if fiyat in mtxt or re.search(r'"(Open|High|Low|Close|Volume|getiri|fiyat)"', mtxt):
            hata.append("3) manifest fiyat / getiri içeriyor")
        for x in M["bloklar"]:
            b = open(os.path.join(kasa, "muhurlu", x["kasa_dosya"]), "rb").read()
            if b"S00" in b or b"Close" in b or b"pandas" in b:
                hata.append(f"3) {x['kasa_dosya']} düz metin sızdırıyor")
        if M["acik_anahtar_sha256"] != K.ks_parmak_izi(open(aa, "rb").read()):
            hata.append("3) manifest parmak izi farklı")
        rc, o = _cli(["muhurle", "--kesik", KESIK, "--cikti", kasa, "--kaynak", kaynak, "--acik-anahtar", aa, "--manifest", man]); ciktilar.append(o)
        if rc == 0:
            hata.append("3) ikinci mühür --uzerine olmadan manifesti ezdi")

        # 4) anahtarsız / yanlış anahtar / değiştirilmiş dosya
        x0 = M["bloklar"][0]; kyol = os.path.join(kasa, "muhurlu", x0["kasa_dosya"]); blob = open(kyol, "rb").read()
        yanlis_kl = tempfile.mkdtemp(prefix="gz_yanlis_"); yanlis = os.path.join(yanlis_kl, "y.pem")
        try:
            K.ks_kur(yanlis, os.path.join(kok, "y_acik.pem"))
            _beklenen_hata(lambda: K.ks_coz(blob, yanlis), "çözülemedi", "4) yanlış anahtar", hata)
        finally:
            shutil.rmtree(yanlis_kl, ignore_errors=True)
        bozuk = bytearray(blob); bozuk[-40] ^= 1
        _beklenen_hata(lambda: K.ks_coz(bytes(bozuk), gizli), "çözülemedi", "4) değiştirilmiş gövde", hata)
        bas = bytearray(blob); i = bas.find(b'"blok"'); bas[i + 10] ^= 1
        _beklenen_hata(lambda: K.ks_coz(bytes(bas), gizli), "", "4) değiştirilmiş başlık", hata)
        try:
            _, duz = K.ks_coz(blob, gizli)
            if K._sha_bayt(duz) != x0["duz_sha256"]:
                hata.append("4) doğru anahtarla çözülen veri farklı")
        except K.KasaHata as ex:
            hata.append(f"4) doğru anahtar açamadı: {ex}")

        # 6) ön kayıt kapısı (git deposu)
        repo = os.path.join(kok, "repo"); os.makedirs(repo); _git(repo, "init", "-q")
        onA = _onkayit(repo, "ONK_A.md", "HIPA", "hip_a.py", tarih="2026-01-05T10:00:00Z")
        ortam = {"KASA_GIZLI": gizli}
        os.environ.pop("KASA_GIZLI", None)
        kw = dict(cikti=kasa, manifest=man, defter=dft)
        # 5) KASA_GIZLI yok
        _beklenen_hata(lambda: K.ks_ac("2026Q1", "HIPA", onA, **kw), "KASA_GIZLI", "5) KASA_GIZLI yokken aç", hata)
        os.environ.update(ortam)
        try:
            onX = _onkayit(repo, "ONK_X.md", "HIPX", "hip_x.py", commit=False)
            _beklenen_hata(lambda: K.ks_ac("2026Q1", "HIPX", onX, **kw), "işlenmemiş", "6) işlenmemiş ön kayıt", hata)
            _git(repo, "add", "ONK_X.md"); _git(repo, "commit", "-qm", "onk x")
            with open(onX, "a") as f:
                f.write("\nsonradan eklenen satır\n")
            _beklenen_hata(lambda: K.ks_ac("2026Q1", "HIPX", onX, **kw), "değişmiş", "6) değişmiş ön kayıt", hata)
            _git(repo, "checkout", "--", "ONK_X.md")
            with open(os.path.join(repo, "hip_x.py"), "a") as f:
                f.write("# değişti\n")
            _beklenen_hata(lambda: K.ks_ac("2026Q1", "HIPX", onX, **kw), "kod sha", "6) kod değişmiş", hata)
            _git(repo, "checkout", "--", "hip_x.py")
            _beklenen_hata(lambda: K.ks_ac("2026Q1", "BASKA", onX, **kw), "KASA_HIPOTEZ", "6) hipotez farkı", hata)
            onBos = _onkayit(repo, "ONK_BOS.md", "HIPBOS", "hip_bos.py", dolu=False)
            _beklenen_hata(lambda: K.ks_ac("2026Q1", "HIPBOS", onBos, **kw), "kontrol", "6) boş kontrol tablosu", hata)
            if os.path.exists(dft) and K._defter_oku(dft):
                hata.append("6) kapı geçmeden defter satırı yazıldı")

            # 7) sıra atlama
            _beklenen_hata(lambda: K.ks_ac("2026Q2", "HIPA", onA, **kw), "sıra atlama", "7) sıra atlama", hata)
            _beklenen_hata(lambda: K.ks_ac("2027Q1", "HIPA", onA, **kw), "mühürlü değil", "7) olmayan blok", hata)

            # 8) aç + tek kullanım (CLI ile; çıktı 11 için toplanır)
            onB_once = _onkayit(repo, "ONK_B.md", "HIPB", "hip_b.py", tarih="2026-01-06T10:00:00Z")
            rc, o = _cli(["ac", "--blok", "2026Q1", "--hipotez", "HIPA", "--onkayit", onA, "--cikti", kasa, "--manifest", man,
                          "--defter", dft], gizli=gizli); ciktilar.append(o)
            if rc != 0:
                hata.append(f"8) ilk açma başarısız: {o[-500:]}")
            rc, o = _cli(["ac", "--blok", "2026Q1", "--hipotez", "HIPA", "--onkayit", onA, "--cikti", kasa, "--manifest", man,
                          "--defter", dft], gizli=gizli); ciktilar.append(o)
            if rc == 0 or "tek kullanım" not in o:
                hata.append("8) ikinci açma durmadı")
            onC_sonra = _onkayit(repo, "ONK_C.md", "HIPC", "hip_c.py", tarih="2099-01-01T00:00:00Z")
            _beklenen_hata(lambda: K.ks_ac("2026Q1", "HIPC", onC_sonra, **kw), "kör değil", "8) açılıştan sonra yazılmış ön kayıt", hata)
            try:
                r = K.ks_ac("2026Q1", "HIPB", onB_once, **kw)
                if r["tur"] != "kayit":
                    hata.append("8) önceden yazılmış hipotez 'kayıt' olmadı")
            except K.KasaHata as ex:
                hata.append(f"8) önceden yazılmış hipotez durdu: {ex}")
            D = json.load(open(os.path.join(kasa, "acik", K.KS_DURUM_AD)))
            if D["acik_kesik"] != "2026-03-31" or D["acilan"] != ["2026Q1"]:
                hata.append(f"8) durum yanlış: {D}")
            satir = K._defter_oku(dft)
            if [(r["Blok"], r["Hipotez"]) for r in satir] != [("2026Q1", "HIPA"), ("2026Q1", "HIPB")]:
                hata.append(f"8) defter satırları yanlış: {satir}")
            # 10a) denetim: açık kısım geçer, kesik aşımı yakalanır
            try:
                K.kasa_kapisi([os.path.join(kasa, "acik", a) for a in DOSYALAR], cikti=kasa)
            except K.KasaHata as ex:
                hata.append(f"10) açık kısım denetimi durdu: {ex}")
            # 9) kalan blokları sırayla aç
            for b in ("2026Q2", "2026Q3"):
                try:
                    K.ks_ac(b, "HIPA", onA, **kw)
                except K.KasaHata as ex:
                    hata.append(f"9) {b} açılmadı: {ex}")
            for ad in DOSYALAR:
                A = pd.read_pickle(os.path.join(kasa, "acik", ad))
                for s, d0 in V[ad].items():
                    beklenen = d0.sort_index(kind="mergesort")
                    if s not in A or not A[s].equals(beklenen) or A[s].index.dtype != beklenen.index.dtype \
                            or list(A[s].dtypes) != list(beklenen.dtypes) or not A[s].index.equals(beklenen.index):
                        hata.append(f"9) {ad} {s} birleşik veri özgünle eşit değil"); break
            D = json.load(open(os.path.join(kasa, "acik", K.KS_DURUM_AD)))
            if D["acik_kesik"] != "2026-08-14":
                hata.append(f"9) son açık kesik {D['acik_kesik']} (beklenen 2026-08-14, yarım çeyrek veri sonu)")
            _beklenen_hata(lambda: K.ks_ac("2026Q3", "HIPA", onA, **kw), "tek kullanım", "8) son blokta ikinci açma", hata)
        finally:
            os.environ.pop("KASA_GIZLI", None)

        # 10) denetim kapısı
        dk = os.path.join(kok, "denetim"); os.makedirs(dk)
        pd.DataFrame({"tarih": ["2025-12-30", "2026-01-02"], "x": [1, 2]}).to_csv(os.path.join(dk, "a.csv"), index=False)
        pd.DataFrame({"sembol": ["A"], "giris_gunu": ["2025-11-03"]}).to_csv(os.path.join(dk, "b.csv"), index=False)
        pd.to_pickle({"A": V["V_ABD.pkl"]["S00"]}, os.path.join(dk, "c.pkl"))
        pd.to_pickle({"ic": [{"seri": V["V_ABD.pkl"]["S01"].loc[:"2025-06-30"]}]}, os.path.join(dk, "d.pkl"))
        pd.DataFrame({"x": [1, 2]}).to_csv(os.path.join(dk, "e.csv"), index=False)
        _beklenen_hata(lambda: K.kasa_kapisi(os.path.join(dk, "a.csv"), KESIK), "KESİK AŞIMI", "10) csv aşımı", hata)
        _beklenen_hata(lambda: K.kasa_kapisi(os.path.join(dk, "c.pkl"), KESIK), "KESİK AŞIMI", "10) pkl aşımı", hata)
        _beklenen_hata(lambda: K.kasa_kapisi(os.path.join(dk, "e.csv"), KESIK), "tarih bulunamadı", "10) tarihsiz dosya", hata)
        try:
            K.kasa_kapisi([os.path.join(dk, "b.csv"), os.path.join(dk, "d.pkl")], KESIK)
        except K.KasaHata as ex:
            hata.append(f"10) kesik içi dosyalar durdu: {ex}")
        rc, o = _cli(["denetim", os.path.join(dk, "a.csv"), "--kesik", KESIK]); ciktilar.append(o)
        if rc != 2 or "KESİK AŞIMI" not in o:
            hata.append("10) CLI denetim aşımda 2 ile çıkmadı")
        rc, o = _cli(["durum", "--cikti", kasa, "--manifest", man, "--defter", dft]); ciktilar.append(o)
        if rc != 0 or "2026Q3" not in o:
            hata.append("10) durum çıktısı eksik")

        # 13) --ekle: yeni veri parça blok olarak mühürlenir, sıra sürer
        kaynak2 = os.path.join(kok, "veri2"); _kaynak_yaz(kaynak2, V2)
        rc, o = _cli(["muhurle", "--ekle", "--cikti", kasa, "--kaynak", kaynak2, "--acik-anahtar", aa, "--manifest", man]); ciktilar.append(o)
        M2 = json.load(open(man))
        if rc != 0 or K._blok_listesi(M2) != ["2026Q1", "2026Q2", "2026Q3", "2026Q3-2", "2026Q4"]:
            hata.append(f"13) ekle blokları yanlış: {rc} {K._blok_listesi(M2)} {o[-300:]}")
        else:
            os.environ["KASA_GIZLI"] = gizli
            try:
                _beklenen_hata(lambda: K.ks_ac("2026Q4", "HIPA", onA, **kw), "sıra atlama", "13) parça atlama", hata)
                K.ks_ac("2026Q3-2", "HIPA", onA, **kw); K.ks_ac("2026Q4", "HIPA", onA, **kw)
                for ad in DOSYALAR:
                    A = pd.read_pickle(os.path.join(kasa, "acik", ad))
                    if any(not A[s_].equals(d_.sort_index(kind="mergesort")) for s_, d_ in V2[ad].items()):
                        hata.append(f"13) {ad} ekle sonrası birleşik veri özgünle eşit değil")
            except K.KasaHata as ex:
                hata.append(f"13) ekle blokları açılmadı: {ex}")
            finally:
                os.environ.pop("KASA_GIZLI", None)

        # 11) gizli yol hiçbir çıktıda geçmez
        dosyalar = [man, dft, os.path.join(kasa, "kasa.log"), os.path.join(kasa, "acik", K.KS_DURUM_AD)]
        metin = "\n".join(ciktilar) + "\n".join(open(y, encoding="utf-8", errors="replace").read() for y in dosyalar if os.path.exists(y))
        for parca in (gizli, os.path.basename(gizli), os.path.basename(gizli_kl)):
            if parca in metin:
                hata.append("11) gizli yol parçası çıktıda geçti"); break
        if not os.path.exists(os.path.join(kasa, "kasa.log")):
            hata.append("11) kasa.log yazılmadı")

        # 12) openssl arka ucu + çapraz uyum + parola
        if shutil.which("openssl"):
            ok = tempfile.mkdtemp(prefix="gz_ossl_")
            try:
                g1 = os.path.join(ok, "o.pem"); K.ks_kur(g1, os.path.join(kok, "o_acik.pem"), arka="openssl")
                ap = open(os.path.join(kok, "o_acik.pem"), "rb").read(); veri = os.urandom(5000)
                for sif, coz in (("openssl", "openssl"), ("openssl", "cryptography"), ("cryptography", "openssl")):
                    try:
                        b = K.ks_sifrele(veri, ap, {"blok": "T"}, arka=sif)
                        if K._paket_coz(b)[0]["alg"] == K.KS_ALG_GCM and coz == "openssl":
                            continue   # GCM yalnız cryptography ile çözülür (tasarım)
                        if K.ks_coz(b, g1, arka=coz)[1] != veri:
                            hata.append(f"12) {sif}->{coz} tur bozuk")
                    except K.KasaHata as ex:
                        hata.append(f"12) {sif}->{coz}: {ex}")
                b = bytearray(K.ks_sifrele(veri, ap, {"blok": "T"}, arka="openssl")); b[-5] ^= 1
                _beklenen_hata(lambda: K.ks_coz(bytes(b), g1, arka="openssl"), "HMAC", "12) openssl değiştirilmiş dosya", hata)
                os.environ["KASA_PAROLA"] = "deneme-parolasi"
                try:
                    for ar in ("cryptography", "openssl"):
                        gp = os.path.join(ok, f"p_{ar}.pem"); K.ks_kur(gp, os.path.join(kok, f"p_{ar}_acik.pem"), arka=ar)
                        if b"ENCRYPTED" not in open(gp, "rb").read():
                            hata.append(f"12) {ar} parolalı gizli anahtar şifresiz")
                        apb = open(os.path.join(kok, f"p_{ar}_acik.pem"), "rb").read()
                        for coz in ("cryptography", "openssl"):
                            bb = K.ks_sifrele(veri, apb, {"blok": "P"}, arka="openssl")
                            if K.ks_coz(bb, gp, arka=coz)[1] != veri:
                                hata.append(f"12) parolalı {ar} -> {coz} tur bozuk")
                finally:
                    os.environ.pop("KASA_PAROLA", None)
            except K.KasaHata as ex:
                hata.append(f"12) openssl arka ucu: {ex}")
            finally:
                shutil.rmtree(ok, ignore_errors=True)

        # 14) ay blokları + kuru sayım
        acik, bloklar, sy = K.ks_bol(V["V_BIST.pkl"], KESIK, "ay")
        if sorted(bloklar, key=K._blok_sira)[:2] != ["2026-01", "2026-02"] or len(bloklar) != 8 or sy["sirasiz"] != 1:
            hata.append(f"14) ay blokları yanlış: {sorted(bloklar)} {sy}")
        T = K.ks_say(KESIK, "ceyrek", kaynak)
        t_abd = T[T.dosya == "V_ABD.pkl"]
        top = int(t_abd.satir.sum()); oz = int(sum(len(d) for d in V["V_ABD.pkl"].values()))
        if top != oz:
            hata.append(f"14) kuru sayım toplamı {top} != özgün {oz}")
        _beklenen_hata(lambda: K.ks_say(KESIK, "ceyrek", kaynak, [os.path.join(kaynak, "V_ABD.pkl")]), "dosya adı", "14) --dosya yol", hata)
        if set(os.listdir(kaynak)) != set(DOSYALAR):
            hata.append("14) kuru sayım dosya yazdı")
    finally:
        shutil.rmtree(kok, ignore_errors=True); shutil.rmtree(gizli_kl, ignore_errors=True)
        if os.path.exists(os.path.join(KOK, "gizli_deneme.pem")):
            os.unlink(os.path.join(KOK, "gizli_deneme.pem"))

    # 15) e-posta / anahtar yok
    eposta = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    for ad in ("KASA.py", "test_kasa.py"):
        s_ = open(os.path.join(KOK, ad), encoding="utf-8").read().replace("t@t.invalid", "").replace("noreply@anthropic.com", "")
        if eposta.findall(s_) or re.search(r"(api[_-]?key|token|secret|password)\s*=\s*['\"][A-Za-z0-9]{12,}", s_, re.I) \
                or "BEGIN PRIVATE KEY-----\n" in s_:
            hata.append(f"15) {ad} içinde e-posta / anahtar var")
    return hata


if __name__ == "__main__":
    Hh = testler()
    if Hh:
        print("KASA TEST: HATA", len(Hh)); print("\n".join(Hh)); sys.exit(1)
    print("KASA TEST: 15/15 bölüm GEÇTİ")
