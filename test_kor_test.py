"""KOR_TEST testleri — YALNIZ SENTETİK veri (ağ yok; Tiingo'ya istek yok). Çalıştırma: python test_kor_test.py

1) pencere: karar gününden SONRA bar yok (son bar = t; gelecek bozulunca pencere ve PNG aynı); t sınır dışı -> dur  2) grafik: şekilde yalnız sayı (eksen
sayıları) var; başlık / eksen adı / lejant yok; x verisi <= 0; PNG'de yazılım / metin üst verisi yok; aynı girdi aynı sha256; sayı dışı metin eklenirse
yazmadan durur  3) seçim tohumla birebir (aynı tohum aynı; başka tohum başka), farklı hisse, haric tercihi, tekrar geçişi (>= 120 bar), uygun_mu reddi,
yetmezse uydurmaz  4) sağ boşluk kuralı elle  5) Wilson / Newcombe / Fisher / kappa elle (bilinen değerler)  6) karar kategorileri (BAŞARILI / ZAYIF / YOK /
VERİ YETERSİZ)  7) uçtan uca ölçü: EMİN DEĞİLİM paydadan çıkar; sağlamada HAYIR'a eklenir; duyarlılık / kesinlik elle  8) cevap dosyası biçimleri ve
eksik / geçersiz cevap reddi  9) uçtan uca sentetik set: VDYT2 fonksiyonlarıyla üretilen tablolar + sentetik Tiingo kayıtları -> 40 grafik, anahtar,
manifest (grup bilgisi yok), iki koşu birebir aynı (anahtar / manifest / PNG sha256)  10) anahtar mühür ve ret kapısı: ön kayıt git'te değil / sonradan
değişmiş / eşik / kod / anahtar / manifest / grafik sha256 tutmuyor -> RET; git'e işlenince geçer; ön kayıt ve set üzerine yazılmaz; gerçek depoda
KOR_TEST.py işlenmemişse `olc` reddeder  11) olc uçtan uca (git kapısı kapalı): sonuç JSON, rapor, anahtarın kopyalanması  12) çakışma kapısı
13) VDYT2.py / VDYT.py değişmedi; kodda e-posta / anahtar yok; VDYT*.py değiştirilmiyor  14) v1.1 (SAPMA 1): 250 bar pencere (kopuk / veri başı -> kesintisiz
en uzun, < 120 dur, gelecek yok); log ortak ölçek (%4 / %1 oynaklıkta mum piksel oranı ~ 3,94; piksel / ln birimi her grafikte aynı); %10 cetveli gerçek
ln(1,10) boyunda (küçültülen grafikte de); 350 / 1600 piksel sınırları; metin kapısı (sayı + '%10'); deterministik PNG; v1.0 sözlüğüyle kurulan set aynı;
ciz11 iki koşu aynı, anahtar değişmez, manifest_v11'de grup yok, karar günü tutmazsa durur; sapma11 (sonuç varsa / iki kez / manifest yoksa reddeder) ve
kapı (v1.0 mührü yeniden kurulur, v1.1 grafik / manifest bozulunca RET); gerçek anahtar sha256 73da87f12549 değişmedi.
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
sys.path.insert(0, KOK)
import VDYT as V1  # noqa: E402
import VDYT2 as V2  # noqa: E402
import KOR_TEST as K  # noqa: E402
import test_vdyt2 as T2  # noqa: E402  (sentetik pazar üretici; yalnız okunur)

E0 = K.KOR_ESIK
ANAHTAR_SHA = "73da87f12549b013e89b7dd24f11fdbc51c474ea1559410ad528e5ea049b6319"   # mühürlü kör set anahtarı (v1.0 ön kayıt; v1.1'de DEĞİŞMEZ)


def durmali(fn, mesaj: str, hata: list, icerik: str = "") -> None:
    try:
        fn()
    except (K.KorHata, V2.Vdyt2Hata, V1.VdytHata, RuntimeError) as ex:
        if icerik and icerik not in str(ex):
            hata.append(f"{mesaj} (yanlış neden: {ex})")
        return
    hata.append(mesaj)


def git(kl: str, *a: str) -> str:
    return subprocess.run(["git", "-C", kl, "-c", "user.name=kor", "-c", "user.email=kor@test.invalid"] + list(a), capture_output=True, text=True,
                          check=True).stdout


def tiingo_kayit(d: pd.DataFrame, kod: str) -> dict:
    v = [{"date": f"{g.date()}T00:00:00.000Z", "open": float(r.o), "high": float(r.h), "low": float(r.l), "close": float(r.c), "volume": float(r.v),
          "adjOpen": float(r.o), "adjHigh": float(r.h), "adjLow": float(r.l), "adjClose": float(r.c), "adjVolume": float(r.v), "divCash": 0.0, "splitFactor": 1.0}
         for g, r in d.iterrows()]
    return {"durum": "ok", "http": 200, "kod": kod, "satir": len(v), "veri": v, "zaman": "sentetik"}


def sentetik_tablolar(F: dict, pazar: str, kl: str, tohum: int) -> None:
    """VDYT2 fonksiyonlarıyla sentetik satir / kontrol / bolge tabloları (VDYT2 kos ara çıktısı biçiminde, yalnız gerekli sütunlar)."""
    rng = np.random.default_rng(tohum); sat, kon, bol = [], [], []
    for s, d in F["S"].items():
        Ol, B = K.kor_g5_bolgeler(d)
        icinde = np.zeros(len(d), bool)
        for b0, t0, b1, tur in B.tolist():
            icinde[b0: b1 + 1] = True; bol.append((s, b0, t0, b1, tur))
            for a in (10, 15, 20, 30, 45):
                t = b0 + a - 1
                if t0 <= t < b1 and t >= 260:
                    sat.append((s, "GERCEK", b0, t, a, str(d.index[t].date()), 0.0))
        cand = np.flatnonzero(~icinde & (np.arange(len(d)) >= 260))
        for t in rng.choice(cand, size=min(len(cand), 40), replace=False).tolist() if len(cand) else []:
            kon.append((s, "DISARI", t - 9, t, 10, str(d.index[t].date()), 0.0))
        for t in (rng.choice(len(d) - 300, size=5, replace=False).tolist() if len(d) > 320 else []):
            kon.append((s, "RASTGELE", t + 251, t + 260, 10, str(d.index[t + 260].date()), 0.0))
    kol = ["sembol", "kaynak", "bas", "t", "yas", "tarih", "P1"]
    pd.DataFrame(sat, columns=kol).to_csv(os.path.join(kl, f"satir_{pazar}_G5.csv.gz"), index=False)
    pd.DataFrame(kon, columns=kol).to_csv(os.path.join(kl, f"kontrol_{pazar}_G5.csv.gz"), index=False)
    pd.DataFrame(bol, columns=["sembol", "bas", "tespit", "bit", "bit_tur"]).to_csv(os.path.join(kl, f"bolge_{pazar}_G5.csv.gz"), index=False)


def sentetik_set(td: str) -> dict:
    """Sentetik dünya: BIST ve ABD pazarı (14 hisse), 7 batan kodu için sentetik Tiingo kayıtları, VDYT2 biçiminde tablolar."""
    Fb, _ = T2.sentetik_pazar(nh=14, tohum=7, pazar="BIST"); Fa, _ = T2.sentetik_pazar(nh=14, tohum=8, pazar="ABD")
    Fa = {**Fa, "S": {f"A{s}": d for s, d in Fa["S"].items()}}
    for kl in ("tablo", "tiingo", "cikti", "set"):
        os.makedirs(os.path.join(td, kl), exist_ok=True)
    sentetik_tablolar(Fb, "BIST", os.path.join(td, "tablo"), 1); sentetik_tablolar(Fa, "ABD", os.path.join(td, "tablo"), 2)
    Fbt, _ = T2.sentetik_pazar(nh=7, tohum=9, pazar="ABD", bas="2011-01-03", bit="2023-12-29")
    for kod, s in zip(E0["set"]["batan"]["semboller"], [f"S{j:02d}" for j in range(7)]):
        with open(os.path.join(td, "tiingo", f"{kod}.json"), "w", encoding="utf-8") as f:
            json.dump(tiingo_kayit(Fbt["S"][s], kod), f)
    return {"BIST": Fb, "ABD": Fa}


def testler() -> list:
    hata: list = []
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image
    td0 = tempfile.mkdtemp(prefix="kor_test_")
    # ---------------------------------------------------------------- 1) pencere: gelecek bar yok
    d = T2.rastgele_bar(400, tohum=3)
    W = K.kor_pencere(d, 250, 120)
    if len(W) != 120 or W.index[-1] != d.index[250] or W.index[0] != d.index[131]:
        hata.append("1) pencere karar günü t'de bitmiyor ya da 120 bar değil")
    if abs(float(W.c.iloc[-1]) - 100.0) > 1e-9:
        hata.append("1) normalize: karar günü kapanışı 100 değil")
    d2 = d.copy(); d2.iloc[251:, :] = d2.iloc[251:, :] * 7.0   # gelecek bozuldu
    if not K.kor_pencere(d2, 250, 120).equals(W):
        hata.append("1) gelecek barlar değişince pencere değişti (geleceğe bakıyor)")
    p1 = os.path.join(td0, "a.png"); p2 = os.path.join(td0, "b.png")
    g1 = K.kor_grafik_yaz(W, p1); g2 = K.kor_grafik_yaz(K.kor_pencere(d2, 250, 120), p2)
    if g1["sha256"] != g2["sha256"]:
        hata.append("1) gelecek barlar değişince PNG değişti")
    durmali(lambda: K.kor_pencere(d, 50, 120), "1) t < 119 iken pencere kuruldu", hata)
    durmali(lambda: K.kor_pencere(d, 400, 120), "1) t veri dışındayken pencere kuruldu", hata)
    # ---------------------------------------------------------------- 2) grafik: yalnız sayı, üst veri yok, deterministik
    fig = K.kor_ciz_fig(W)
    mt = K.kor_metinler(fig)
    if not mt or any(not K._KOR_SAYI.match(m.strip()) for m in mt):
        hata.append(f"2) grafikte sayı dışı metin var: {[m for m in mt if not K._KOR_SAYI.match(m.strip())][:5]}")
    for ax in fig.axes:
        if ax.get_title() or ax.get_xlabel() or ax.get_ylabel() or ax.get_legend() is not None:
            hata.append("2) başlık / eksen adı / lejant var")
        if ax.lines:
            hata.append("2) grafikte çizgi (Line2D) var")
        for col in ax.collections:
            for p in (col.get_paths() if hasattr(col, "get_paths") else []):
                if len(p.vertices) and float(np.max(p.vertices[:, 0])) > 0.5:
                    hata.append("2) x > 0 (karar gününden sonra) çizim var"); break
        for r in ax.patches:
            if r.get_x() + r.get_width() > 0.5:
                hata.append("2) x > 0 hacim çubuğu var"); break
    if fig.axes[1].get_yticklabels() and any(t.get_text() for t in fig.axes[1].get_yticklabels()):
        hata.append("2) hacim ekseninde sayı var")
    plt.close(fig)
    with Image.open(p1) as im:
        bilgi = {k for k in im.info if k not in ("dpi",)}
        if bilgi:
            hata.append(f"2) PNG üst verisinde metin var: {bilgi}")
        if list(im.size) != list(E0["grafik_v10"]["piksel"]):
            hata.append(f"2) PNG boyutu {im.size} != {E0['grafik_v10']['piksel']}")
    if os.path.getsize(p1) > E0["grafik_v10"]["hedef_kb"] * 1024:
        hata.append("2) PNG 150 KB'tan büyük")
    if K.kor_grafik_yaz(W, os.path.join(td0, "c.png"))["sha256"] != g1["sha256"]:
        hata.append("2) aynı girdi farklı PNG (deterministik değil)")
    eski = K.kor_ciz_fig

    def basliklı(W_, E_=None):
        f = eski(W_, E_); f.axes[0].set_title("ABC 2020"); return f
    K.kor_ciz_fig = basliklı
    try:
        durmali(lambda: K.kor_grafik_yaz(W, os.path.join(td0, "d.png")), "2) başlıklı grafik yazıldı (metin kapısı çalışmadı)", hata, "sayı dışı")
        if os.path.exists(os.path.join(td0, "d.png")):
            hata.append("2) metin kapısı dosyayı yine de yazdı")
    finally:
        K.kor_ciz_fig = eski
    # ---------------------------------------------------------------- 3) seçim
    T = pd.DataFrame({"sembol": [f"H{i % 25:02d}" for i in range(200)], "t": [300 + 7 * i for i in range(200)]}).sort_values(["sembol", "t"]).reset_index(drop=True)
    a = K.kor_sec(T, 8, [1, 0]); b = K.kor_sec(T, 8, [1, 0]); c = K.kor_sec(T, 8, [2, 0])
    if [(r["sembol"], r["t"]) for r in a] != [(r["sembol"], r["t"]) for r in b]:
        hata.append("3) aynı tohum farklı seçim")
    if [(r["sembol"], r["t"]) for r in a] == [(r["sembol"], r["t"]) for r in c]:
        hata.append("3) başka tohum aynı seçim")
    if len({r["sembol"] for r in a}) != 8:
        hata.append("3) seçimde aynı hisse iki kez")
    sira = np.random.default_rng([1, 0]).permutation(len(T)); ilk = []
    for i in sira:
        if T.sembol[i] not in [x[0] for x in ilk]:
            ilk.append((T.sembol[i], int(T.t[i])))
        if len(ilk) == 8:
            break
    if ilk != [(r["sembol"], int(r["t"])) for r in a]:
        hata.append("3) seçim permütasyon kuralına uymuyor (elle)")
    har = {f"H{i:02d}" for i in range(20)}
    h1 = K.kor_sec(T, 5, [3, 0], har)
    if any(r["sembol"] in har for r in h1):
        hata.append("3) haric tercihi uygulanmadı (yeterli aday varken haric hisse seçildi)")
    h2 = K.kor_sec(T, 8, [3, 0], har)
    if len(h2) != 8 or sum(r["sembol"] not in har for r in h2) != 5:
        hata.append("3) haric dışı tükenince ikinci geçiş haric hisselere geçmedi")
    T3 = pd.DataFrame({"sembol": ["X"] * 10 + ["Y"] * 10, "t": list(range(300, 3000, 270)) + list(range(300, 3000, 270))})
    s3 = K.kor_sec(T3, 4, [4, 0], tekrar=True, ara=120)
    if len(s3) != 4 or any(abs(p["t"] - q["t"]) < 120 for p in s3 for q in s3 if p is not q and p["sembol"] == q["sembol"]):
        hata.append("3) tekrar geçişi: 4 seçilmedi ya da aynı hissede < 120 bar")
    if len(K.kor_sec(T3, 4, [4, 0], tekrar=False)) != 2:
        hata.append("3) tekrar kapalıyken 2 hisseden fazla seçildi (uydurma)")
    s5 = K.kor_sec(T, 8, [5, 0], uygun_mu=lambda r: r["t"] % 2 == 0)
    if any(r["t"] % 2 for r in s5):
        hata.append("3) uygun_mu reddi uygulanmadı")
    if K.kor_aday_sha(pd.DataFrame({"sembol": ["A"], "tarih": ["2020-01-01"], "t": [5], "yas": [10]})) == \
            K.kor_aday_sha(pd.DataFrame({"sembol": ["A"], "tarih": ["2020-01-01"], "t": [6], "yas": [10]})):
        hata.append("3) aday sha256 içerik değişince değişmedi")
    # ---------------------------------------------------------------- 4) sağ boşluk
    Tb = pd.DataFrame({"sembol": ["A"] * 5 + ["B"], "t": [100, 129, 130, 160, 200, 120]})
    Zb = pd.DataFrame({"sembol": ["A", "A"], "bas": [80, 199], "bit": [100, 250]})
    ok = K._kor_sag_bos(Tb, Zb, 30).tolist()
    if ok != [False, False, True, True, False, True]:   # t=129: [100,129] ∩ [80,100] -> kesişir; t=130: [101,130] boş; t=200: bölge içinde
        hata.append(f"4) sağ boşluk yanlış: {ok}")
    # ---------------------------------------------------------------- 5) istatistik elle
    p, lo, hi = K.kor_wilson(7, 10)
    if abs(lo - 0.3968) > 5e-4 or abs(hi - 0.8922) > 5e-4:
        hata.append(f"5) Wilson 7/10 yanlış: {lo:.4f}-{hi:.4f}")
    fz = K.kor_fisher(3, 1, 1, 3)
    if abs(fz["iki_yonlu"] - 0.4857) > 5e-4 or abs(fz["tek_yonlu_buyuk"] - 0.2429) > 5e-4:
        hata.append(f"5) Fisher (çay tadımı) yanlış: {fz}")
    fz2 = K.kor_fisher(12, 4, 3, 13)
    from math import comb
    P = {x: comb(16, x) * comb(16, 15 - x) / comb(32, 15) for x in range(0, 16)}
    elle = sum(v for v in P.values() if v <= P[12] * (1 + 1e-7))
    if abs(fz2["iki_yonlu"] - elle) > 1e-12 or abs(fz2["tek_yonlu_buyuk"] - sum(v for x, v in P.items() if x >= 12)) > 1e-12:
        hata.append("5) Fisher 12/4-3/13 elle hesapla tutmuyor")
    d_, l_, u_ = K.kor_newcombe(56, 70, 48, 80)
    if abs(d_ - (0.8 - 0.6)) > 1e-12 or abs(l_ - 0.0524) > 6e-4 or abs(u_ - 0.3339) > 6e-4:
        hata.append(f"5) Newcombe 56/70-48/80 yanlış: {d_:.4f} {l_:.4f} {u_:.4f}")
    x = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0]; y = [1, 1, 1, 0, 0, 0, 0, 1, 1, 0]
    po = 0.8; pe = 0.5 * 0.5 + 0.5 * 0.5
    if abs(K.kor_kappa(x, y) - (po - pe) / (1 - pe)) > 1e-12:
        hata.append("5) kappa elle tutmuyor")
    # ---------------------------------------------------------------- 6) karar kategorileri
    def Kd(pa, pb, kp, pf, payda=(16, 16), fark=None):
        return {"gruplar": ["G5", "KONTROL"], "G5": {"oran": pa}, "KONTROL": {"oran": pb}, "kappa": kp, "fisher_iki_yonlu": pf, "payda": list(payda),
                "fark": pa - pb if fark is None else fark}
    for args, bek in [((0.75, 0.30, 0.45, 0.01), "BAŞARILI"), ((0.70, 0.35, 0.40, 0.049), "BAŞARILI"), ((0.69, 0.10, 0.6, 0.001), "ZAYIF İŞARET"),
                      ((0.80, 0.40, 0.4, 0.01), "ZAYIF İŞARET"), ((0.80, 0.30, 0.39, 0.01), "ZAYIF İŞARET"), ((0.80, 0.30, 0.5, 0.05), "ZAYIF İŞARET"),
                      ((0.59, 0.10, 0.5, 0.01), "İŞARET YOK"), ((0.60, 0.60, 0.0, 1.0), "İŞARET YOK"), ((0.65, 0.70, -0.1, 1.0), "İŞARET YOK")]:
        if K.kor_karar(Kd(*args)) != bek:
            hata.append(f"6) karar {args} -> {K.kor_karar(Kd(*args))} (beklenen {bek})")
    if K.kor_karar(Kd(0.9, 0.1, 0.8, 0.001, payda=(7, 16))) != "VERİ YETERSİZ":
        hata.append("6) payda < 8 iken VERİ YETERSİZ değil")
    if "HARCANMAZ" not in K.kor_kota("VERİ YETERSİZ") or "YALNIZ" not in K.kor_kota("ZAYIF İŞARET"):
        hata.append("6) kota kuralı yanlış")
    # ---------------------------------------------------------------- 7) uçtan uca ölçü (elle)
    A = {}; C = {}; no = 1
    plan = [("G5", "BIST", "EVET")] * 9 + [("G5", "ABD", "HAYIR")] * 3 + [("G5", "ABD", "EMIN")] * 4 + \
           [("KONTROL", "BIST", "EVET")] * 2 + [("KONTROL", "ABD", "HAYIR")] * 12 + [("KONTROL", "ABD", "EMIN")] * 2 + \
           [("BATAN_G5", "ABD (Tiingo, batan)", "EVET")] * 4 + [("BATAN_KONTROL", "ABD (Tiingo, batan)", "HAYIR")] * 4
    for g, pz, cv in plan:
        A[str(no)] = {"grup": g, "pazar": pz, "sembol": f"S{no}", "bilesen": {"G4": no % 2 == 0}}
        C[no] = {"bolge": cv, "destek": "EVET" if no % 3 == 0 else "HAYIR"}; no += 1
    S = K.kor_olcu(A, C)
    a_ = S["ana"]
    if (a_["G5"]["evet"], a_["G5"]["hayir"], a_["G5"]["emin"], a_["KONTROL"]["evet"], a_["KONTROL"]["hayir"], a_["KONTROL"]["emin"]) != (9, 3, 4, 2, 12, 2):
        hata.append("7) sayımlar yanlış")
    if abs(a_["G5"]["oran"] - 9 / 12) > 1e-12 or abs(a_["KONTROL"]["oran"] - 2 / 14) > 1e-12:
        hata.append("7) EMİN DEĞİLİM paydadan çıkmadı")
    s_ = S["saglama_emin_hayir"]
    if abs(s_["G5"]["oran"] - 9 / 16) > 1e-12 or abs(s_["KONTROL"]["oran"] - 2 / 16) > 1e-12:
        hata.append("7) sağlamada EMİN DEĞİLİM HAYIR'a eklenmedi")
    if abs(a_["duyarlilik"] - 9 / 11) > 1e-12 or abs(a_["kesinlik"] - 9 / 12) > 1e-12 or abs(a_["ozgulluk"] - 12 / 15) > 1e-12:
        hata.append("7) duyarlılık / kesinlik / özgüllük elle tutmuyor")
    kp = K.kor_kappa([1] * 12 + [0] * 14, [1] * 9 + [0] * 3 + [1] * 2 + [0] * 12)
    if abs(a_["kappa"] - kp) > 1e-12:
        hata.append("7) kappa uçtan uca tutmuyor")
    if abs(a_["fisher_iki_yonlu"] - K.kor_fisher(9, 3, 2, 12)["iki_yonlu"]) > 1e-12:
        hata.append("7) Fisher uçtan uca tutmuyor")
    if S["karar"] != K.kor_karar(a_) or S["batan"]["BATAN_G5"]["oran"] != 1.0 or S["batan"]["BATAN_KONTROL"]["oran"] != 0.0:
        hata.append("7) karar / batan alt grubu yanlış")
    if not (a_["fark_bootstrap"][0] <= a_["fark"] <= a_["fark_bootstrap"][1]):
        hata.append("7) bootstrap aralığı farkı içermiyor")
    if S["destek"]["n"] != 40 or abs(S["destek"]["uyum"] - np.mean([((i % 3 == 0) == (i % 2 == 0)) for i in range(1, 41)])) > 1e-12:
        hata.append("7) destek uyumu elle tutmuyor")
    if S["pazar"]["BIST"]["G5"]["evet"] != 9 or S["pazar"]["ABD"]["KONTROL"]["hayir"] != 12:
        hata.append("7) pazar kırılımı yanlış")
    # ---------------------------------------------------------------- 8) cevap dosyası
    def yaz(ad, metin):
        y = os.path.join(td0, ad)
        with open(y, "w", encoding="utf-8") as f:
            f.write(metin)
        return y
    j = {str(i): {"bolge": ["EVET", "HAYIR", "EMİN DEĞİLİM"][i % 3], "destek": "EVET" if i % 2 else ""} for i in range(1, 41)}
    c1 = K.kor_cevap_oku(yaz("c1.json", json.dumps(j, ensure_ascii=False)))
    if c1[3]["bolge"] != "EVET" or c1[1]["bolge"] != "HAYIR" or c1[2]["bolge"] != "EMIN" or c1[2]["destek"] is not None or c1[1]["destek"] != "EVET":
        hata.append("8) JSON iç içe biçim yanlış okundu")
    txt = "\n".join(f"{i} {['evet', 'Hayır', 'emin değilim'][i % 3]}" + (" evet" if i == 5 else "") for i in range(1, 41))
    c2 = K.kor_cevap_oku(yaz("c2.txt", "# Cemal\n" + txt))
    if c2[2]["bolge"] != "EMIN" or c2[4]["bolge"] != "HAYIR" or c2[5]["destek"] != "EVET" or c2[6]["bolge"] != "EVET":
        hata.append("8) metin biçimi yanlış okundu")
    c3 = K.kor_cevap_oku(yaz("c3.json", json.dumps({str(i): ["EVET", "HAYIR"] for i in range(1, 41)})))
    if c3[7]["destek"] != "HAYIR":
        hata.append("8) liste biçimi yanlış okundu")
    eks = dict(j); eks.pop("40")
    durmali(lambda: K.kor_cevap_oku(yaz("c4.json", json.dumps(eks))), "8) eksik cevap kabul edildi", hata, "eksik")
    bos = dict(j); bos["7"] = {"bolge": "", "destek": ""}
    durmali(lambda: K.kor_cevap_oku(yaz("c5.json", json.dumps(bos))), "8) boş (şablon) cevap kabul edildi", hata, "eksik")
    ger = dict(j); ger["8"] = "BELKI"
    durmali(lambda: K.kor_cevap_oku(yaz("c6.json", json.dumps(ger))), "8) geçersiz cevap kabul edildi", hata, "tanınmayan")
    faz = dict(j); faz["41"] = "EVET"
    durmali(lambda: K.kor_cevap_oku(yaz("c7.json", json.dumps(faz))), "8) fazla numara kabul edildi", hata, "fazla")
    # ---------------------------------------------------------------- 9) uçtan uca sentetik set (iki koşu birebir)
    td = os.path.join(td0, "dunya"); F = sentetik_set(td)
    oz = {}
    for kosu in ("k1", "k2"):
        sk = os.path.join(td, f"set_{kosu}"); ck = os.path.join(td, f"cikti_{kosu}"); os.makedirs(ck, exist_ok=True)
        oz[kosu] = K.kor_set(cikti=ck, set_kl=sk, tablo_kl=os.path.join(td, "tablo"), tiingo_kl=os.path.join(td, "tiingo"), F_ver=copy.copy(F),
                             kod_denetim=False)
    z1, z2 = oz["k1"], oz["k2"]
    if z1["anahtar_sha256"] != z2["anahtar_sha256"] or z1["manifest_sha256"] != z2["manifest_sha256"]:
        hata.append("9) iki koşu farklı anahtar / manifest (seçim tohumla birebir değil)")
    if z1["bulunan"] != {"G5": 16, "KONTROL": 16, "BATAN_G5": 4, "BATAN_KONTROL": 4}:
        hata.append(f"9) sentetik sette grup sayıları beklenenden farklı: {z1['bulunan']} (eksik {z1['eksik']})")
    sk = os.path.join(td, "set_k1")
    A9 = json.load(open(os.path.join(sk, "anahtar.json"), encoding="utf-8"))["numara"]; M9 = json.load(open(os.path.join(sk, "manifest.json"), encoding="utf-8"))
    if sorted(int(k) for k in A9) != list(range(1, len(A9) + 1)) or len(M9["grafik"]) != len(A9):
        hata.append("9) numaralar 1..n değil ya da manifest eksik")
    mtxt = json.dumps(M9["grafik"], ensure_ascii=False)
    if re.search(r"G5|KONTROL|BATAN|BIST|ABD|sembol|tarih|grup|pazar", mtxt) or any(set(m) != {"numara", "dosya", "sha256", "bayt", "piksel"} for m in M9["grafik"]):
        hata.append("9) manifestte grup / pazar / sembol / tarih bilgisi var")
    for k_, a9 in A9.items():
        pz = a9["pazar"]
        dd = (K.kor_tiingo_temiz(K.kor_tiingo_kayit(a9["sembol"], os.path.join(td, "tiingo")))[0] if pz.startswith("ABD (Tiingo")
              else F[pz]["S"][a9["sembol"]])
        if str(dd.index[a9["t"]].date()) != a9["tarih"] or a9["pencere"][1] != a9["tarih"]:
            hata.append(f"9) grafik {k_}: pencere sonu karar günü değil"); break
        Ol, B = K.kor_g5_bolgeler(dd); t = a9["t"]
        icinde = bool(((B[:, 1] <= t) & (B[:, 2] > t)).any())
        sag = bool(((B[:, 0] <= t) & (B[:, 2] >= t - 29)).any())
        if a9["grup"].endswith("G5") and not icinde:
            hata.append(f"9) G5 grafiği {k_} açık bölgede değil"); break
        if not a9["grup"].endswith("G5") and sag:
            hata.append(f"9) kontrol grafiği {k_} son 30 mumda bölge içeriyor"); break
        mm = [m for m in M9["grafik"] if m["numara"] == int(k_)][0]
        if K.kor_sha_dosya(os.path.join(sk, "grafik", mm["dosya"])) != mm["sha256"] or a9["grafik_sha256"] != mm["sha256"]:
            hata.append(f"9) grafik {k_} sha256 manifest / anahtarla tutmuyor"); break
    g5h = {a["sembol"] for a in A9.values() if a["grup"] == "G5"}
    if len(g5h) != 16 or len({a["sembol"] for a in A9.values() if a["grup"] == "KONTROL"}) != 16:
        hata.append("9) G5 / KONTROL grubunda farklı hisse kuralı tutmadı")
    for m in M9["grafik"]:
        if K.kor_sha_dosya(os.path.join(sk, "grafik", m["dosya"])) != K.kor_sha_dosya(os.path.join(td, "set_k2", "grafik", m["dosya"])):
            hata.append("9) iki koşuda PNG farklı"); break
    # ---------------------------------------------------------------- 10) ön kayıt, mühür ve ret kapısı
    ck = os.path.join(td, "cikti_k1")
    y_ok = K.kor_onkayit(cikti=ck, set_kl=sk)
    durmali(lambda: K.kor_onkayit(cikti=ck, set_kl=sk), "10) ön kayıt üzerine yazıldı", hata, "zaten var")
    durmali(lambda: K.kor_set(cikti=ck, set_kl=sk, tablo_kl=os.path.join(td, "tablo"), tiingo_kl=os.path.join(td, "tiingo"), F_ver=copy.copy(F),
                              kod_denetim=False), "10) ön kayıttan sonra set yeniden üretildi", hata, "mühürlü")
    O = K.kor_onkayit_oku(y_ok)
    if O["ANAHTAR_SHA256"] != z1["anahtar_sha256"] or O["ESIK_SHA256"] != K.kor_esik_sha() or O["KOD_SHA256"] != K.kor_kod_sha():
        hata.append("10) ön kayıt satırları yanlış")
    durmali(lambda: K.kor_kapi(ck, sk, git=True), "10) git'e işlenmemiş ön kayıtla ölçüm açıldı", hata, "git")
    K.kor_kapi(ck, sk, git=False)   # mühürler tutuyor -> geçer
    E2 = copy.deepcopy(E0); E2["olcum"]["basari"]["g5_evet_min"] = 0.6
    durmali(lambda: K.kor_kapi(ck, sk, E2, git=False), "10) eşik değişince ölçüm açıldı", hata, "eşik mührü")
    ak = os.path.join(sk, "anahtar.json"); yedek = open(ak, encoding="utf-8").read()
    with open(ak, "w", encoding="utf-8") as f:
        f.write(yedek.replace('"G5"', '"KONTROL"', 1))
    durmali(lambda: K.kor_kapi(ck, sk, git=False), "10) anahtar değişince ölçüm açıldı", hata, "anahtar")
    with open(ak, "w", encoding="utf-8") as f:
        f.write(yedek)
    pg = os.path.join(sk, "grafik", "grafik_01.png"); pb = open(pg, "rb").read()
    with open(pg, "ab") as f:
        f.write(b"x")
    durmali(lambda: K.kor_kapi(ck, sk, git=False), "10) grafik değişince ölçüm açıldı", hata, "manifest")
    with open(pg, "wb") as f:
        f.write(pb)
    mk = os.path.join(sk, "manifest.json"); mb = open(mk, encoding="utf-8").read()
    with open(mk, "w", encoding="utf-8") as f:
        f.write(mb + " ")
    durmali(lambda: K.kor_kapi(ck, sk, git=False), "10) manifest değişince ölçüm açıldı", hata, "manifest")
    with open(mk, "w", encoding="utf-8") as f:
        f.write(mb)
    ob = open(y_ok, encoding="utf-8").read()
    with open(y_ok, "w", encoding="utf-8") as f:
        f.write(re.sub(r"^KOD_SHA256: .+$", "KOD_SHA256: " + "0" * 64, ob, flags=re.M))
    durmali(lambda: K.kor_kapi(ck, sk, git=False), "10) kod sha256 tutmazken ölçüm açıldı", hata, "KOR_TEST.py")
    with open(y_ok, "w", encoding="utf-8") as f:
        f.write(ob)
    git(ck, "init", "-q"); git(ck, "add", K.KOR_DOSYA["onkayit"]); git(ck, "commit", "-q", "-m", "on kayit")
    try:
        K.kor_kapi(ck, sk, git=True, kod_git=False)
    except K.KorHata as ex:
        hata.append(f"10) git'e işlenmiş ön kayıt reddedildi: {ex}")
    with open(y_ok, "a", encoding="utf-8") as f:
        f.write("\nek\n")
    durmali(lambda: K.kor_kapi(ck, sk, git=True, kod_git=False), "10) işlendikten sonra değişen ön kayıt kabul edildi", hata, "farklı")
    with open(y_ok, "w", encoding="utf-8") as f:
        f.write(ob)
    r_ = subprocess.run(["git", "-C", KOK, "ls-files", "--error-unmatch", "KOR_TEST.py"], capture_output=True)
    if r_.returncode != 0:
        durmali(lambda: K.kor_git_durum(os.path.join(KOK, "KOR_TEST.py")), "10) işlenmemiş KOR_TEST.py git kapısından geçti", hata, "işlenmemiş")
    # ---------------------------------------------------------------- 11) olc uçtan uca (git kapısı kapalı)
    cv = {k_: {"bolge": "EVET" if a["grup"].endswith("G5") else "HAYIR", "destek": "EVET" if a["bilesen"]["G4"] else "HAYIR"} for k_, a in A9.items()}
    cy = yaz("cevap.json", json.dumps(cv))
    R11 = K.kor_olc(cy, cikti=ck, set_kl=sk, git=False)
    if R11["karar"] != "BAŞARILI" or abs(R11["ana"]["kappa"] - 1.0) > 1e-12 or R11["destek"]["uyum"] != 1.0:
        hata.append(f"11) mükemmel uyumda karar / kappa yanlış: {R11['karar']} {R11['ana']['kappa']}")
    for ad in ("sonuc", "rapor", "anahtar_repo"):
        if not os.path.exists(K._kor_yol(ad, ck)):
            hata.append(f"11) {ad} yazılmadı")
    if K.kor_sha_dosya(K._kor_yol("anahtar_repo", ck)) != z1["anahtar_sha256"]:
        hata.append("11) repoya kopyalanan anahtar mühürlü anahtarla aynı değil")
    cv2 = {k_: {"bolge": "EVET", "destek": ""} for k_ in A9}
    if K.kor_olc(yaz("cevap2.json", json.dumps(cv2)), cikti=ck, set_kl=sk, git=False)["karar"] == "BAŞARILI":
        hata.append("11) her şeye EVET diyen değerlendirici BAŞARILI çıktı")
    os.remove(K._kor_yol("rapor", ck)); K.kor_rapor(ck)
    if "SONUÇ" not in open(K._kor_yol("rapor", ck), encoding="utf-8").read():
        hata.append("11) rapor JSON'dan yeniden yazılamadı")
    # ---------------------------------------------------------------- 12) çakışma kapısı
    g12 = {"__name__": "x", "_CK_KAYIT": {"kor_sec": "BASKA.py"}, "kor_sec": 1}
    cwd = os.getcwd()
    try:
        os.chdir(KOK)
        exec(compile(open(os.path.join(KOK, "KOR_TEST.py"), encoding="utf-8").read(), "KOR_TEST.py", "exec"), g12)
        hata.append("12) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"12) çakışma kapısı yanlış neden: {ex}")
    finally:
        os.chdir(cwd)
    g12b: dict = {"__name__": "x"}
    try:
        os.chdir(KOK)
        exec(compile(open(os.path.join(KOK, "KOR_TEST.py"), encoding="utf-8").read(), "KOR_TEST.py", "exec"), g12b)
        exec(compile(open(os.path.join(KOK, "KOR_TEST.py"), encoding="utf-8").read(), "KOR_TEST.py", "exec"), g12b)
    except RuntimeError as ex:
        hata.append(f"12) aynı dosyanın ikinci yüklemesi durdu: {ex}")
    finally:
        os.chdir(cwd)
    # ---------------------------------------------------------------- 13) bağımlı kod değişmedi; sızıntı yok
    try:
        K.kor_bagimli_kod()
    except K.KorHata as ex:
        hata.append(f"13) {ex}")
    kaynak = open(os.path.join(KOK, "KOR_TEST.py"), encoding="utf-8").read()
    if K._KOR_EPOSTA.search(kaynak) or re.search(r"Token [0-9a-f]{20,}", kaynak) or "api.tiingo.com" in kaynak or "requests" in kaynak:
        hata.append("13) kodda e-posta / anahtar / ağ isteği izi var")
    if re.search(r"open\([^)]*VDYT2?B?\.py[^)]*['\"]w", kaynak):
        hata.append("13) KOR_TEST VDYT*.py'ye yazıyor")
    # ---------------------------------------------------------------- 14) v1.1 gösterim (SAPMA 1): pencere, log ortak ölçek, %10 cetveli, metin, mühür
    G1 = E0["grafik"]; olc0 = G1["olcek_px_ln110"] / np.log(1.10)
    on_gercek = os.path.join(KOK, "arastirma_cikti", "vdyt", "v2_20261112", "KOR_TEST_ON_KAYIT.md")
    if os.path.exists(on_gercek):
        Og = K.kor_onkayit_oku(on_gercek)
        if K.kor_esik_sha(K.kor_esik_v10(E0)) != Og.get("ESIK_SHA256_V10", Og["ESIK_SHA256"]):
            hata.append("14) v1.0 eşik mührü kor_esik_v10 ile yeniden kurulamadı (grafik dışında eşik değişmiş)")
        if Og["ANAHTAR_SHA256"] != ANAHTAR_SHA:
            hata.append("14) ön kayıttaki anahtar sha256 değişmiş")
    if set(E0) - {"grafik_v10"} != set(K.kor_esik_v10(E0)) or "grafik_v10" in K.kor_esik_v10(E0) or K.kor_esik_v10(E0)["grafik"] != E0["grafik_v10"]:
        hata.append("14) kor_esik_v10 yanlış kuruluyor")
    if K.kor_grafik_v10(E0)["bar"] != 120 or G1["bar"] != 250:
        hata.append("14) v1.0 seçim penceresi 120 / v1.1 çizim penceresi 250 değil")
    gercek_ak = os.path.join(K.KOR_YOL["set"], "anahtar.json")
    if os.path.exists(gercek_ak) and K.kor_sha_dosya(gercek_ak) != ANAHTAR_SHA:
        hata.append("14) gerçek anahtar.json sha256'sı değişmiş (73da87f12549 olmalı)")
    # pencere11
    d14 = T2.rastgele_bar(600, tohum=21)
    d14.index = pd.bdate_range("2015-01-02", periods=len(d14))
    W14, b14 = K.kor_pencere11(d14, 400)
    if len(W14) != 250 or W14.index[-1] != d14.index[400] or W14.index[0] != d14.index[151] or b14["kisa"] or abs(float(W14.c.iloc[-1]) - 100) > 1e-9:
        hata.append("14) pencere11 250 bar / karar günü sağda değil")
    d14b = d14.copy(); d14b.iloc[401:, :] = d14b.iloc[401:, :] * 5.0
    if not K.kor_pencere11(d14b, 400)[0].equals(W14):
        hata.append("14) pencere11 geleceğe bakıyor")
    ix = d14.index.to_list(); ix = ix[:251] + [g + pd.Timedelta(days=30) for g in ix[251:]]
    d14k = d14.copy(); d14k.index = pd.DatetimeIndex(ix)
    Wk, bk = K.kor_pencere11(d14k, 400)
    if len(Wk) != 150 or not bk["kisa"] or bk["neden"] != "kopuk" or Wk.index[0] != d14k.index[251]:
        hata.append(f"14) kopuklu pencere kesintisiz en uzun değil: {len(Wk)} {bk}")
    Wb, bb = K.kor_pencere11(d14, 180)
    if len(Wb) != 181 or bb["neden"] != "veri_basi":
        hata.append("14) veri başında pencere yanlış")
    durmali(lambda: K.kor_pencere11(d14, 100), "14) 120 bardan kısa pencere kabul edildi", hata, "<")
    durmali(lambda: K.kor_pencere11(d14k, 300), "14) kopuktan sonra 120 bardan kısa pencere kabul edildi", hata, "<")

    def duz(oran: float, tohum: int) -> pd.DataFrame:
        r = np.random.default_rng(tohum); n = 300; c = 100 * np.exp(np.cumsum(r.normal(0, 0.002, n)))
        return pd.DataFrame({"o": c, "h": c * np.exp(oran / 2), "l": c * np.exp(-oran / 2), "c": c, "v": r.uniform(1e5, 2e5, n)},
                            index=pd.bdate_range("2020-01-02", periods=n))

    def fitil_px(fig) -> np.ndarray:
        ax = fig.axes[0]; lc = ax.collections[0]; out = []
        for p in lc.get_paths():
            v = ax.transData.transform(p.vertices); out.append(abs(v[1, 1] - v[0, 1]))
        return np.asarray(out)

    def px_ln(fig, i=0) -> float:
        ax = fig.axes[i]; return float(ax.transData.transform((0, 1.0))[1] - ax.transData.transform((0, 0.0))[1])

    def cetvel_px(fig) -> float:
        axc = fig.axes[2]; v = axc.transData.transform(axc.collections[0].get_paths()[0].vertices); return float(abs(v[1, 1] - v[0, 1]))
    Wa, _ = K.kor_pencere11(duz(np.log(1.01), 1), 299); Wd, _ = K.kor_pencere11(duz(np.log(1.04), 2), 299)
    fa, fd = K.kor_ciz_fig11(Wa), K.kor_ciz_fig11(Wd)
    ha, hd = fitil_px(fa), fitil_px(fd); oran = float(np.median(hd) / np.median(ha)); bek = np.log(1.04) / np.log(1.01)
    if abs(oran / bek - 1) > 0.05:
        hata.append(f"14) ortak ölçek: %4 / %1 mum piksel oranı {oran:.2f} (beklenen {bek:.2f})")
    if abs(np.median(ha) - np.log(1.01) * olc0) > 0.5:
        hata.append(f"14) %1 mumun piksel boyu {np.median(ha):.2f} != {np.log(1.01) * olc0:.2f}")
    for f_ in (fa, fd):
        if abs(px_ln(f_) - olc0) > 1e-6 * olc0 or abs(px_ln(f_, 2) - olc0) > 1e-6 * olc0:
            hata.append("14) piksel / ln birimi ortak ölçekte değil"); break
        if abs(cetvel_px(f_) - G1["olcek_px_ln110"]) > 0.5:
            hata.append(f"14) %10 cetveli {cetvel_px(f_):.2f} piksel (beklenen {G1['olcek_px_ln110']})"); break
        if abs(f_.axes[0].get_window_extent().height - max(G1["fiyat_min_px"], 0)) > 0.5 and f_ is fa:
            hata.append("14) dar aralıklı grafikte fiyat paneli en az 350 piksel değil")
        if abs(f_.axes[1].get_window_extent().height - G1["hacim_px"]) > 0.5 or f_.axes[1].get_yticklabels() and any(t.get_text() for t in f_.axes[1].get_yticklabels()):
            hata.append("14) hacim paneli 180 piksel değil ya da sayılı"); break
        if round(f_.get_figwidth() * f_.dpi) != G1["genislik"]:
            hata.append("14) genişlik sabit değil"); break
        mt14 = K.kor_metinler(f_)
        if K.kor_metin_yabanci(mt14) or "%10" not in mt14 or not any(m == "100" for m in mt14):
            hata.append(f"14) v1.1 metinleri: {mt14}"); break
        if f_.axes[0].get_title() or f_.axes[0].get_ylabel() or f_.axes[1].get_xlabel() or f_.axes[0].get_legend() is not None:
            hata.append("14) v1.1'de başlık / eksen adı / lejant var"); break
        for col in f_.axes[0].collections:
            if any(len(p.vertices) and float(np.max(p.vertices[:, 0])) > 0.5 for p in col.get_paths()):
                hata.append("14) v1.1'de x > 0 çizim var"); break
    # büyük aralık: fiyat paneli 1600'ü aşar -> ölçek küçülür, cetvel yine gerçek ln(1,10) boyunda, oran korunur
    dbig = duz(np.log(1.04), 3); dbig[["o", "h", "l", "c"]] = dbig[["o", "h", "l", "c"]].mul(np.exp(np.linspace(np.log(40), 0, len(dbig))), axis=0)
    Wg, _ = K.kor_pencere11(dbig, 299); Yg = K.kor_geometri11(Wg); fg = K.kor_ciz_fig11(Wg)
    if not Yg["kucuk"] or Yg["fiyat_px"] != G1["fiyat_max_px"] or abs(fg.axes[0].get_window_extent().height - G1["fiyat_max_px"]) > 0.5:
        hata.append("14) 1600 pikseli aşan grafikte ölçek küçültülmedi")
    if abs(cetvel_px(fg) - np.log(1.10) * Yg["olcek"]) > 0.5 or abs(px_ln(fg) - Yg["olcek"]) > 1e-6 * Yg["olcek"]:
        hata.append("14) küçültülen grafikte %10 cetveli gerçek boyda değil")
    if abs(np.median(fitil_px(fg)) - np.log(1.04) * Yg["olcek"]) > 0.5:
        hata.append("14) küçültülen grafikte mum boyu ölçekle tutmuyor")
    for f_ in (fa, fd, fg):
        plt.close(f_)
    if K.kor_metin_yabanci(["100", "-50", "%10", "12.5"]) or K.kor_metin_yabanci(["%20"]) != ["%20"] or K.kor_metin_yabanci(["ABC"]) != ["ABC"]:
        hata.append("14) metin kapısı izinli listesi yanlış")
    p14 = os.path.join(td0, "v11a.png")
    g14 = K.kor_grafik_yaz(W14, p14, ciz=K.kor_ciz_fig11)
    if K.kor_grafik_yaz(W14, os.path.join(td0, "v11b.png"), ciz=K.kor_ciz_fig11)["sha256"] != g14["sha256"]:
        hata.append("14) v1.1 PNG deterministik değil")
    Y14 = K.kor_geometri11(W14)
    with Image.open(p14) as im:
        if list(im.size) != [Y14["genislik"], Y14["yukseklik"]] or {k for k in im.info if k != "dpi"}:
            hata.append(f"14) v1.1 PNG boyutu / üst verisi yanlış: {im.size} {im.info}")

    def basliklı11(W_, E_=None):
        f = K.kor_ciz_fig11(W_, E_); f.axes[0].set_title("ABC 2020"); return f
    durmali(lambda: K.kor_grafik_yaz(W14, os.path.join(td0, "v11c.png"), ciz=basliklı11), "14) v1.1 başlıklı grafik yazıldı", hata, "sayı dışı")
    if os.path.exists(os.path.join(td0, "v11c.png")):
        hata.append("14) v1.1 metin kapısı dosyayı yine de yazdı")
    # uçtan uca: v1.0 mührüyle kurulan set -> ön kayıt -> ciz11 (iki koşu) -> sapma11 -> kapı
    E10 = K.kor_esik_v10(E0); sk3 = os.path.join(td, "set_v10"); ck3 = os.path.join(td, "cikti_v10"); os.makedirs(ck3, exist_ok=True)
    z3 = K.kor_set(cikti=ck3, set_kl=sk3, E=E10, tablo_kl=os.path.join(td, "tablo"), tiingo_kl=os.path.join(td, "tiingo"), F_ver=copy.copy(F), kod_denetim=False)
    if json.load(open(z3["anahtar"], encoding="utf-8"))["numara"] != json.load(open(z1["anahtar"], encoding="utf-8"))["numara"] or \
            z3["aday_sha256"] != z1["aday_sha256"]:
        hata.append("14) v1.0 sözlüğüyle kurulan set v1.1 sözlüğüyle kurulandan farklı (seçim / v1.0 çizimi değişmiş)")
    y3 = K.kor_onkayit(cikti=ck3, set_kl=sk3, E=E10)
    ak3 = os.path.join(sk3, "anahtar.json"); sha_ak3 = K.kor_sha_dosya(ak3)
    durmali(lambda: K.kor_sapma11(cikti=ck3, set_kl=sk3), "14) manifest_v11 yokken SAPMA yazıldı", hata, "ciz11")
    kop = os.path.join(td, "kopya")
    c1 = K.kor_ciz11(set_kl=sk3, F_ver=copy.copy(F), tiingo_kl=os.path.join(td, "tiingo"), kopya_kl=kop)
    v11_1 = {m: K.kor_sha_dosya(os.path.join(sk3, "grafik_v11", m)) for m in sorted(os.listdir(os.path.join(sk3, "grafik_v11")))}
    c2 = K.kor_ciz11(set_kl=sk3, F_ver=copy.copy(F), tiingo_kl=os.path.join(td, "tiingo"))
    v11_2 = {m: K.kor_sha_dosya(os.path.join(sk3, "grafik_v11", m)) for m in sorted(os.listdir(os.path.join(sk3, "grafik_v11")))}
    if c1["manifest_v11_sha256"] != c2["manifest_v11_sha256"] or v11_1 != v11_2 or len(v11_1) != 40:
        hata.append("14) ciz11 iki koşuda farklı (deterministik değil) ya da 40 PNG değil")
    if c1["v10_yeniden_cizim_tuttu"] != 40:
        hata.append("14) v1.0 yeniden çizim anahtarla tutmadı")
    if K.kor_sha_dosya(ak3) != sha_ak3 or c1["anahtar_sha256"] != sha_ak3:
        hata.append("14) ciz11 anahtarı değiştirdi")
    if any(K.kor_sha_dosya(os.path.join(kop, m)) != s for m, s in v11_1.items()):
        hata.append("14) kopya klasörü PNG'leri farklı")
    M11 = json.load(open(os.path.join(sk3, "manifest_v11.json"), encoding="utf-8"))
    if re.search(r"G5|KONTROL|BATAN|BIST|ABD|sembol|tarih|grup|pazar", json.dumps(M11["grafik"], ensure_ascii=False)) or \
            any(set(m) != {"numara", "dosya", "sha256", "bayt", "piksel"} for m in M11["grafik"]) or \
            re.search(r"G5|KONTROL|BATAN|grup", json.dumps(M11["ozet"], ensure_ascii=False)):
        hata.append("14) manifest_v11'de grup / pazar / sembol / tarih bilgisi var")
    A3 = json.load(open(ak3, encoding="utf-8"))["numara"]; M3 = json.load(open(os.path.join(sk3, "manifest.json"), encoding="utf-8"))
    if any(A3[str(m["numara"])]["grafik_sha256"] != m["sha256"] for m in M3["grafik"]):
        hata.append("14) v1.0 grafikleri ciz11'den sonra değişti")
    # yanlış eşleşme: anahtardaki bir karar günü kayarsa ciz11 durur
    A3b = json.load(open(ak3, encoding="utf-8")); A3b["numara"]["1"]["tarih"] = "1999-01-01"; sk3b = os.path.join(td, "set_v10_bozuk"); os.makedirs(sk3b)
    with open(os.path.join(sk3b, "anahtar.json"), "w", encoding="utf-8") as f:
        json.dump(A3b, f)
    durmali(lambda: K.kor_ciz11(set_kl=sk3b, F_ver=copy.copy(F), tiingo_kl=os.path.join(td, "tiingo")), "14) karar günü tutmayan anahtarla çizildi", hata,
            "tutmuyor")
    sonuc3 = K._kor_yol("sonuc", ck3)
    with open(sonuc3, "w", encoding="utf-8") as f:
        f.write("{}")
    durmali(lambda: K.kor_sapma11(cikti=ck3, set_kl=sk3), "14) ölçüm sonucu varken SAPMA yazıldı", hata, "sonuc")
    os.remove(sonuc3)
    durmali(lambda: K.kor_sapma11(cikti=ck3, set_kl=sk3, E=E2), "14) başka eşikle SAPMA yazıldı", hata, "")
    K.kor_sapma11(cikti=ck3, set_kl=sk3)
    durmali(lambda: K.kor_sapma11(cikti=ck3, set_kl=sk3), "14) SAPMA iki kez yazıldı", hata, "zaten")
    O3 = K.kor_onkayit_oku(y3)
    if O3["ESIK_SHA256"] != K.kor_esik_sha() or O3["ESIK_SHA256_V10"] != K.kor_esik_sha(E10) or O3["MANIFEST_V11_SHA256"] != c1["manifest_v11_sha256"] \
            or O3["KOD_SHA256"] != K.kor_kod_sha() or O3["ANAHTAR_SHA256"] != sha_ak3:
        hata.append("14) SAPMA 1 satırları yanlış okunuyor")
    m3 = open(y3, encoding="utf-8").read()
    if "SAPMA 1 (v1.1" not in m3 or "%10" not in m3 or re.search(r"\b(BBBYQ|WEWKQ)\b", m3.split("## SAPMA 1")[1]):
        hata.append("14) SAPMA 1 metni eksik ya da sembol içeriyor")
    try:
        K.kor_kapi(ck3, sk3, git=False)
    except K.KorHata as ex:
        hata.append(f"14) SAPMA 1'li ön kayıt kapıdan geçmedi: {ex}")
    durmali(lambda: K.kor_kapi(ck3, sk3, E10, git=False), "14) v1.1 ön kaydı v1.0 eşikleriyle açıldı", hata, "eşik mührü")
    pg3 = os.path.join(sk3, "grafik_v11", "grafik_05.png"); pb3 = open(pg3, "rb").read()
    with open(pg3, "ab") as f:
        f.write(b"x")
    durmali(lambda: K.kor_kapi(ck3, sk3, git=False), "14) v1.1 grafiği değişince ölçüm açıldı", hata, "v1.1 grafikleri")
    with open(pg3, "wb") as f:
        f.write(pb3)
    mk3 = os.path.join(sk3, "manifest_v11.json"); mb3 = open(mk3, encoding="utf-8").read()
    with open(mk3, "w", encoding="utf-8") as f:
        f.write(mb3 + " ")
    durmali(lambda: K.kor_kapi(ck3, sk3, git=False), "14) manifest_v11 değişince ölçüm açıldı", hata, "manifest_v11")
    with open(mk3, "w", encoding="utf-8") as f:
        f.write(mb3)
    cv3 = {k_: {"bolge": "EVET" if a["grup"].endswith("G5") else "HAYIR", "destek": ""} for k_, a in A3.items()}
    R3 = K.kor_olc(yaz("cevap3.json", json.dumps(cv3)), cikti=ck3, set_kl=sk3, git=False)
    if R3["karar"] != "BAŞARILI" or "v11" not in R3["kapi"]:
        hata.append("14) v1.1 kapısıyla olc uçtan uca çalışmadı")
    # gerçek depo: SAPMA 1 yazıldıysa gerçek kapı (git hariç) geçmeli
    if os.path.exists(on_gercek) and "ESIK_SHA256_V11" in K.kor_onkayit_oku(on_gercek) and os.path.exists(gercek_ak) \
            and os.path.exists(os.path.join(K.KOR_YOL["set"], "manifest_v11.json")):
        try:
            K.kor_kapi(git=False)
        except K.KorHata as ex:
            hata.append(f"14) gerçek ön kayıt (SAPMA 1) kapıdan geçmedi: {ex}")
    shutil.rmtree(td0, ignore_errors=True)
    return hata


if __name__ == "__main__":
    h = testler()
    if h:
        print("BAŞARISIZ:", len(h)); print("\n".join(" - " + x for x in h)); sys.exit(1)
    print("test_kor_test: hepsi geçti")
