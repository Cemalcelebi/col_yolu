"""test_d9_avr — D9_AVR.py testleri (sektör listesi için V_AVR / ham evren varsa gerçek dosya; akış testleri sentetik).

1) sektor_AVR.csv: V_AVR ile birebir (581), ust boş sayısı, her ham ad tek ust'a, eşleme md ile tutarlı, ham evrenden yeniden üretim aynı
2) sentetik AVR akışı: rüzgâr paneli AVR sektörüyle çalışır, b / c satırları boş değil, geleceğe bakma denetimi (AVR sözlüğüyle) tutar,
   fon hariç sayım çalışır
3) D9_YENIDEN davranışı değişmedi: D9_ESIK['sektor']['AVR'] import ve d9a_E sonrası hâlâ None, D9_ESIK sha D9_YENIDEN ön kaydıyla aynı,
   BIST / ABD sektör kaynağı aynı, d9_sektor('AVR') boş
4) kapı: KONTROL LİSTESİ eksik satırda kos durur; ön kayıt yok / sha tutmuyor -> durur; doğru sha ile açılır (git hariç)
5) önceden yazılı karar kuralı dört dal; bilinmeyen ham sektör adı durur
6) e-posta / anahtar taraması
Çalıştır: python test_d9_avr.py   (veri: OC_VERI ya da /tmp/veri içinde V_AVR.pkl; yoksa 1. bölümün V_AVR kısmı ATLANIR ve yazılır)
"""
import os
import re
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
warnings.filterwarnings("ignore")

import D9_YENIDEN as D9  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import D9_AVR as A  # noqa: E402

GECTI, KALDI, ATLANDI = [], [], []


def kontrol(ad, kosul, ek=""):
    (GECTI if kosul else KALDI).append(ad)
    print(("  OK   " if kosul else "  HATA ") + ad + (f"  ({ek})" if ek else ""))


def sentetik_hisse(n, tohum, col=None, trend=0.0, bas="2015-01-01"):
    """test_d9_yeniden.sentetik_hisse ile aynı üretici (col=(a, b): dipte dar bant + küçük mum)."""
    rng = np.random.default_rng(tohum)
    r = rng.normal(trend, 0.025, n)
    if col:
        a, b = col
        r[max(0, a - 150):a] = rng.normal(-0.006, 0.02, a - max(0, a - 150))
        r[a:b] = rng.normal(0, 0.006, b - a)
        r[b:] = rng.normal(0.003, 0.02, n - b)
    C = 100 * np.exp(np.cumsum(r))
    O = C * (1 + rng.normal(0, 0.003, n))
    rngd = np.abs(rng.normal(0, 0.01 if col is None else 0.008, n)) + 0.002
    if col:
        rngd[col[0]:col[1]] = np.abs(rng.normal(0, 0.004, col[1] - col[0])) + 0.001
    H = np.maximum(O, C) * (1 + rngd); L = np.minimum(O, C) * (1 - rngd)
    V = rng.integers(1000, 50000, n).astype(float)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": V}, index=pd.bdate_range(bas, periods=n))


def main():
    print("== test_d9_avr ==")
    esik_once = D9.d9_sha(D9.D9_ESIK)

    # 1) sektör listesi
    T = pd.read_csv(A.D9A_YOL["sektor"])
    kontrol("sektor_AVR.csv sütunları", list(T.columns) == ["sembol", "sektor", "ust", "ulke", "kaynak"], str(list(T.columns)))
    kontrol("sektor_AVR.csv 581 satır, sembol tekil", len(T) == 581 and not T.sembol.duplicated().any(), f"{len(T)}")
    kontrol("ust boş sayısı 0 (3 boş Wikipedia'dan tamamlandı)", int(T.ust.isna().sum()) == 0, f"boş {int(T.ust.isna().sum())}")
    kontrol("her ham ad tek ust'a", int(T.groupby("sektor").ust.nunique().max()) == 1)
    kontrol("her satır eşleme tablosuna uygun", all(A.D9A_ESLESME[r.sektor] == r.ust for r in T.itertuples()))
    kontrol("ust sınıfları ICB 20 + fon sınıfı", set(T.ust) <= set(A.D9A_ICB) | {A.D9A_FON} and A.D9A_FON in set(T.ust), str(T.ust.nunique()))
    kontrol("her sınıf RUZ_MIN_UYE + 1 üyeye ulaşıyor (bilgi)", int(T.ust.value_counts().min()) >= D9.D9_PARAM["RUZ_MIN_UYE"] + 1,
            str(T.ust.value_counts().min()))
    md = open(A.D9A_YOL["eslesme"], encoding="utf-8").read()
    md_es = {m.group(1).strip(): (m.group(2).strip(), int(m.group(3))) for m in
             re.finditer(r"^\| ([^|]+?) \| ([^|]+?) \| (\d+) \| (\d+) \|$", md, flags=re.M)}
    vs = T.sektor.value_counts()
    kontrol("eşleme md == D9A_ESLESME (ad, ust, V_AVR sayısı)",
            set(md_es) == set(A.D9A_ESLESME) and all(md_es[h][0] == A.D9A_ESLESME[h] and md_es[h][1] == int(vs.get(h, 0)) for h in md_es),
            f"md {len(md_es)}, tablo {len(A.D9A_ESLESME)}")
    kontrol("D9_YENIDEN.d9_sektor okuması 581 sembol verir", len(D9.d9_sektor("AVR", A.d9a_E())) == 581)
    veri_var = os.path.exists(os.path.join(A.D9A_YOL["veri"], "V_AVR.pkl"))
    if veri_var:
        try:
            A.d9a_sektor_denetle(); kontrol("d9a_sektor_denetle: V_AVR ile birebir", True)
        except A.D9AHata as ex:
            kontrol("d9a_sektor_denetle: V_AVR ile birebir", False, str(ex))
        try:
            ham = A.d9a_ham_oku()
            T2 = A.d9a_sektor_tablosu(ham, A.d9a_v_semboller())
            T1 = pd.read_csv(A.D9A_YOL["sektor"], keep_default_na=False)
            kontrol("ham evrenden yeniden üretim dosyayla aynı", T2.astype(str).reset_index(drop=True).equals(T1.astype(str)))
            kontrol("eşleme md yeniden üretimle aynı", A.d9a_eslesme_md(T2, ham) == md)
        except A.D9AHata as ex:
            ATLANDI.append(f"ham evren yok: {ex}"); print(f"  ATLA ham evren yok ({ex})")
    else:
        ATLANDI.append("V_AVR.pkl yok: V_AVR birebir ve yeniden üretim testleri atlandı")
        print("  ATLA V_AVR.pkl yok (OC_VERI)")
    bozuk = T.copy(); bozuk.loc[0, "ust"] = "Banks" if bozuk.loc[0, "ust"] != "Banks" else "Media"
    with tempfile.TemporaryDirectory() as tmp:
        eski = A.D9A_YOL["sektor"]; A.D9A_YOL["sektor"] = os.path.join(tmp, "s.csv"); bozuk.to_csv(A.D9A_YOL["sektor"], index=False)
        try:
            A.d9a_sektor_denetle(semboller=sorted(T.sembol)); kontrol("bozuk eşleme satırı durur", False)
        except A.D9AHata:
            kontrol("bozuk eşleme satırı durur", True)
        finally:
            A.D9A_YOL["sektor"] = eski

    # 2) sentetik AVR akışı
    veri, sek = {}, {}
    for i in range(18):
        sk = "XA" if i < 6 else ("XB" if i < 12 else "XC")
        veri[f"H{i}.L"] = sentetik_hisse(900, 100 + i, trend={"XA": 0.004, "XB": 0.0, "XC": -0.002}[sk]); sek[f"H{i}.L"] = sk
    for i in range(4):                       # XA sınıfında dipte çöl kuran hisseler (D9 + rüzgâr)
        veri[f"S{i}.PA"] = sentetik_hisse(900, 10 + 2 * i, col=(450, 820)); sek[f"S{i}.PA"] = "XA"
    for i in range(5):                       # fon sınıfı (5 üye: kendi rüzgârını üretebilir)
        veri[f"F{i}.L"] = sentetik_hisse(900, 900 + i, trend=0.004); sek[f"F{i}.L"] = A.D9A_FON
    for i in range(12):                      # havuz >= 30 hisse olsun diye nötr sınıf (cetvel havuz şartı)
        veri[f"N{i}.DE"] = sentetik_hisse(900, 300 + i); sek[f"N{i}.DE"] = "XD"
    with tempfile.TemporaryDirectory() as tmp:
        sy = os.path.join(tmp, "sektor_test.csv")
        pd.DataFrame({"sembol": list(sek), "sektor": list(sek.values()), "ust": list(sek.values()), "ulke": "x", "kaynak": "test"}).to_csv(sy, index=False)
        E = A.d9a_E(sektor_yol=sy)
        sozluk = D9.d9_sektor("AVR", E)
        kontrol("AVR sektör sözlüğü (mutlak yol) okunur", sozluk == {k.upper(): v for k, v in sek.items()})
        Vd = OC._oc_veri_sar(veri, "AVR")
        D = A.d9a_durum(Vd, "AVR", E)
        kontrol("d9a_durum == D9_YENIDEN.d9_durum (uzun hisseler, birebir)", D.equals(D9.d9_durum(Vd, "AVR", E)))
        kisa = dict(veri); kisa["K1.L"] = sentetik_hisse(210, 4242, trend=0.006); sek_k = {**sek, "K1.L": "XA"}
        sy2 = os.path.join(tmp, "sektor_kisa.csv")
        pd.DataFrame({"sembol": list(sek_k), "sektor": list(sek_k.values()), "ust": list(sek_k.values()), "ulke": "x", "kaynak": "t"}).to_csv(sy2, index=False)
        Ek = A.d9a_E(sektor_yol=sy2); Vk = OC._oc_veri_sar(kisa, "AVR")
        Dk = A.d9a_durum(Vk, "AVR", Ek)
        try:
            D9.d9_durum(Vk, "AVR", Ek); d9_dustu = False
        except AttributeError:
            d9_dustu = True
        kontrol("kısa hisse (210 bar, rüzgârlı): d9a_durum çalışır, bant NaN, D9 yok", bool((Dk.sembol == "K1.L").any())
                and Dk[Dk.sembol == "K1.L"].bant250.isna().all() and not Dk[Dk.sembol == "K1.L"].D9.astype(bool).any(),
                f"D9_YENIDEN.d9_durum düştü mü: {d9_dustu}")
        a_, b_, c_ = D9.d9_satir(D, "a"), D9.d9_satir(D, "b"), D9.d9_satir(D, "c")
        kontrol("AVR rüzgâr paneli çalıştı (sektor_var, rüzgâr günü > 0)", bool(D.sektor_var.all()) and int(D.ruzgar.astype(bool).sum()) > 0,
                f"rüzgâr {int(D.ruzgar.astype(bool).sum())}")
        kontrol("satır a, b, c boş değil", len(a_) > 0 and len(b_) > 0 and len(c_) > 0, f"a {len(a_)}, b {len(b_)}, c {len(c_)}")
        kontrol("b ⊂ a ve c ∩ a = ∅", set(map(tuple, b_[["sembol", "tarih"]].values)) <= set(map(tuple, a_[["sembol", "tarih"]].values))
                and not (set(map(tuple, c_[["sembol", "tarih"]].values)) & set(map(tuple, a_[["sembol", "tarih"]].values))))
        Dg = D9.d9_durum(Vd, "AVR")            # D9_YENIDEN'in kendi E'si: AVR sektörsüz
        kontrol("D9_YENIDEN varsayılan E ile AVR b / c boş, a aynı", len(D9.d9_satir(Dg, "b")) == 0 and len(D9.d9_satir(Dg, "c")) == 0
                and len(D9.d9_satir(Dg, "a")) == len(a_))
        X = D[D.D9.astype(bool) | D.ruzgar.astype(bool)]
        try:
            n = A.d9a_gelecek_denetimi(Vd, X, sozluk, 12, 314); kontrol("geleceğe bakma denetimi (AVR sözlüğüyle) tutar", n == 12, str(n))
        except A.D9AHata as ex:
            kontrol("geleceğe bakma denetimi (AVR sözlüğüyle) tutar", False, str(ex))
        Xb = X.copy(); i0 = int(np.where(np.isfinite(Xb.ruz.to_numpy(float)))[0][0]); Xb.iloc[i0, Xb.columns.get_loc("ruz")] += 0.05
        try:
            A.d9a_gelecek_denetimi(Vd, Xb.iloc[[i0]], sozluk, 1, 1); kontrol("bozuk ruz değeri denetimde durur", False)
        except A.D9AHata:
            kontrol("bozuk ruz değeri denetimde durur", True)
        PN = OC.oc_panel(Vd)
        tr = D9.d9_tercil_sinir(D)
        say = D9.d9_sayim(D, {"AVR": PN}, tr)
        kontrol("olay sayımı AVR b / c (not yok, cetvel sonrası olay > 0)", "not" not in say["b"]["AVR"] and "not" not in say["c"]["AVR"]
                and sum(say["c"]["AVR"].get("olay", {}).values()) > 0 and sum(say["b"]["AVR"].get("olay", {}).values()) > 0,
                f"b {say['b']['AVR'].get('olay')}, c {say['c']['AVR'].get('olay')}")
        fon = {s for s, v in sek.items() if v == A.D9A_FON}
        fh = A.d9a_sayim_fon_haric(D, PN, fon)
        kontrol("fon hariç + fon olayı == toplam (c)", all(fh["c"][d] + fh["c"]["fon_olay"][d] == say["c"]["AVR"]["olay"].get(d, 0)
                                                         for d in A.D9A_DONEM) and sum(fh["c"]["fon_olay"].values()) > 0, str(fh["c"]))
        kontrol("tercil sınırı AVR sıralı", "AVR" in tr and tr["AVR"][0] <= tr["AVR"][1], str(tr))
        sic = A.d9a_sicrama({"V": {"Z": pd.DataFrame({"Close": [10.0, 10.5, 1050.0, 1040.0]}, index=pd.bdate_range("2020-01-01", periods=4))}})
        kontrol("sıçrama denetimi 100x birim kaymasını yakalar", len(sic) == 1 and sic[0][2] == 100.0, str(sic))

    # 3) D9_YENIDEN davranışı değişmedi
    kontrol("D9_ESIK['sektor']['AVR'] hâlâ None", D9.D9_ESIK["sektor"]["AVR"] is None)
    kontrol("D9_ESIK sha d9a_E çağrılarından sonra aynı", D9.d9_sha(D9.D9_ESIK) == esik_once)
    on = open(A.D9A_YOL["d9_onkayit"], encoding="utf-8").read() if os.path.exists(A.D9A_YOL["d9_onkayit"]) else ""
    m = re.search(r"D9_ESIK_SHA:\s*`([0-9a-f]{64})`", on)
    kontrol("D9_ESIK sha == D9_YENIDEN ön kaydındaki", bool(m) and m.group(1) == esik_once, (m.group(1)[:12] if m else "yok") + " / " + esik_once[:12])
    E0 = A.d9a_E()
    kontrol("d9a_E: BIST / ABD sektör kaynağı aynı, yalnız AVR farklı", E0["sektor"]["BIST"] == D9.D9_ESIK["sektor"]["BIST"]
            and E0["sektor"]["ABD"] == D9.D9_ESIK["sektor"]["ABD"] and E0["sektor"]["AVR"] == ["sektor_AVR.csv", "ust"]
            and E0["param"] == D9.D9_PARAM)
    kontrol("D9.d9_sektor('AVR') varsayılan E ile boş", D9.d9_sektor("AVR") == {})
    kontrol("a tutarlılık referansı D9_YENIDEN ön kaydından okunur", A.d9a_d9_yeniden_a_sayim() is not None, str(A.d9a_d9_yeniden_a_sayim()))

    # 4) kapı
    with tempfile.TemporaryDirectory() as tmp:
        tablo = A.d9a_kontrol_tablosu()
        eksik = "\n".join(l for l in tablo.splitlines() if not l.startswith("| K7 "))
        open(os.path.join(tmp, A.D9A_DOSYA["onkayit"]), "w", encoding="utf-8").write("# test\n" + eksik + "\n" + OC.oc_kapi_satirlari() + "\n")
        try:
            A.d9a_kos(cikti=tmp, git=False); kontrol("kontrol kapısı: K7 satırı eksik -> kos durur", False)
        except A.D9AHata as ex:
            kontrol("kontrol kapısı: K7 satırı eksik -> kos durur", "kontrol kapısı" in str(ex), str(ex)[:80])
        hayir = tablo.replace("| K14 | boyut (gerçek para) | UYGULANMAZ", "| K14 | boyut (gerçek para) | HAYIR")
        open(os.path.join(tmp, A.D9A_DOSYA["onkayit"]), "w", encoding="utf-8").write("# test\n" + hayir + "\n" + OC.oc_kapi_satirlari() + "\n")
        try:
            A.d9a_kos(cikti=tmp, git=False); kontrol("kontrol kapısı: HAYIR satırı -> kos durur", False)
        except A.D9AHata:
            kontrol("kontrol kapısı: HAYIR satırı -> kos durur", True)
        open(os.path.join(tmp, A.D9A_DOSYA["onkayit"]), "w", encoding="utf-8").write("# test\n" + tablo + "\n")
        try:
            A.d9a_kos(cikti=tmp, git=False); kontrol("cetvel kapısı: CETVEL_SHA yok -> kos durur", False)
        except (A.D9AHata, OC.OCHata):
            kontrol("cetvel kapısı: CETVEL_SHA yok -> kos durur", True)
        try:
            A.d9a_onkayit_dogrula(os.path.join(tmp, "yok.md"), git=False); kontrol("ön kayıt yok -> durur", False)
        except A.D9AHata:
            kontrol("ön kayıt yok -> durur", True)
        if veri_var:
            sha = A._d9a_shalar()
            satir = {"esik": "D9A_ESIK_SHA", "param": "D9_PARAM_SHA", "kod": "D9A_KOD_SHA", "d9_kod": "D9_YENIDEN_SHA", "sektor": "SEKTOR_AVR_SHA",
                     "eslesme": "ESLESME_SHA", "veri": "V_AVR_SHA"}
            y = os.path.join(tmp, "dogru.md")
            open(y, "w").write("\n".join(f"- {v}: `{sha[k]}`" for k, v in satir.items()) + "\n")
            kontrol("ön kayıt doğru sha ile açılır (git hariç)", A.d9a_onkayit_dogrula(y, git=False)["sektor"] == sha["sektor"])
            open(y, "w").write("\n".join(f"- {v}: `{('0' * 64) if k == 'sektor' else sha[k]}`" for k, v in satir.items()) + "\n")
            try:
                A.d9a_onkayit_dogrula(y, git=False); kontrol("sektör sha tutmuyor -> durur", False)
            except A.D9AHata:
                kontrol("sektör sha tutmuyor -> durur", True)

    # 5) karar kuralı ve eşleme
    def J(d23, d24, t4=False):
        return {"hucre": [{"pazar": "AVR", "donem": "2023", "durum": d23, "tutar4": t4}, {"pazar": "AVR", "donem": "2024-26", "durum": d24, "tutar4": t4}]}
    kontrol("karar: ikisi TUTAR -> GÜÇLENDİ", A.d9a_karar(J("TUTAR", "TUTAR"))["karar"].startswith("Ç181c EMARE GÜÇLENDİ"))
    kontrol("karar: biri TUTAR -> değişmedi", A.d9a_karar(J("TUTMADI", "TUTAR"))["karar"].startswith("EMARE (değişmedi), tek pazar"))
    kontrol("karar: ikisi TUTMADI -> ZAYIFLADI", A.d9a_karar(J("TUTMADI", "TUTMADI"))["karar"].startswith("EMARE ZAYIFLADI"))
    kontrol("karar: TUTMADI + ÖLÇÜLEMEDİ -> ÖLÇÜLEMEDİ", A.d9a_karar(J("TUTMADI", "ÖLÇÜLEMEDİ"))["karar"].endswith("AVR ÖLÇÜLEMEDİ"))
    kontrol("b bilgi: n < 1.000 ÖLÇÜLEMEDİ", A.d9a_b_bilgi({"hucre": [{"pazar": "AVR", "donem": "2023", "n": 400, "durum": "TUTMADI"}]})["2023"]
            .startswith("ÖLÇÜLEMEDİ"))
    try:
        A.d9a_ust("Bilinmeyen Sektör"); kontrol("bilinmeyen ham sektör adı durur", False)
    except A.D9AHata:
        kontrol("bilinmeyen ham sektör adı durur", True)

    # 6) e-posta / anahtar
    ep = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    anahtar = re.compile(r"(api[_-]?key|token|secret|password)\s*=\s*['\"][A-Za-z0-9]{12,}", re.I)
    yollar = [A.D9A_YOL["kod"], os.path.abspath(__file__), A.D9A_YOL["sektor"], A.D9A_YOL["eslesme"]]
    if os.path.isdir(A.D9A_YOL["cikti"]):
        yollar += [os.path.join(A.D9A_YOL["cikti"], f) for f in os.listdir(A.D9A_YOL["cikti"])]
    sorun = [y for y in yollar if os.path.isfile(y) and y.endswith((".py", ".md", ".json", ".csv"))
             and (ep.search(open(y, encoding="utf-8").read()) or anahtar.search(open(y, encoding="utf-8").read()))]
    kontrol("e-posta / anahtar yok", not sorun, str(sorun))

    print(f"\n{len(GECTI)} geçti, {len(KALDI)} kaldı" + (f", {len(ATLANDI)} atlandı: {ATLANDI}" if ATLANDI else ""))
    if KALDI:
        print("KALAN:", KALDI)
        sys.exit(1)


if __name__ == "__main__":
    main()
