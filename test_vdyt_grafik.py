"""VDYT_GRAFIK testleri — YALNIZ SENTETİK veri (gerçek veriye, VDYT ara tablolarına ve ağa dokunmaz). Çalıştırma: python test_vdyt_grafik.py

1) paket şeması + doğrulama geçer; float'lar bit bit geri okunur; 'NA' / 'TRUE' gibi semboller metin kalır  2) SİNYAL GÜNÜ grafiğinde karar gününden sonraki
hiçbir bar / çizgi / alan / yazı yok (gelecek barları zehirli: eksen sınırına da etki etmez); genişleme, yön, sonuç, grup adı yok; TAM grafikte var
3) üzerine yazmama (ciz ikinci kez: zaman damgalı alt klasör, ilk dosyalar aynı; paket farklı içerikle durur)  4) manifest doğrulaması (bozuk bayt, eksik /
fazla üye, şema dışı, BAŞARILI tanımı tutmuyor -> durur, HİÇBİR ŞEY çizilmez)  5) BAŞARILI ve BAŞARISIZ ikisi de çizilir (PNG + temas + dizin)
6) yakalayıcı: VDYT çizim fonksiyonu hata olsa da geri konur, dosya yazılmaz  7) ad çözme (BIST_K62, alt çizgili sembol)  8) özgün kip başlığı
9) bağımsızlık: ciz, VDYT.py olmayan klasörde `python -I` ile çalışır; VDYT içe alınmaz  10) çakışma kapısı  11) e-posta / anahtar yok.
"""
from __future__ import annotations

import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import types

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import VDYT_GRAFIK as G  # noqa: E402

CZ = {"dpi": 60, "on_bar": 40, "son_bar": 30, "boyut": [12, 6.5], "oran": [3.2, 1]}


def durmali(fn, mesaj: str, hata: list, icerik: str = "") -> None:
    try:
        fn()
    except (G.VgHata, RuntimeError) as ex:
        if icerik and icerik not in str(ex):
            hata.append(f"{mesaj} (yanlış neden: {ex})")
        return
    hata.append(mesaj)


def sentetik(tohum: int = 3) -> tuple:
    """İki pazar x iki grup (BASARILI, BASARISIZ) x 2 örnek; karar gününden sonraki barlar 'zehirli' (çok yüksek fitil), olaylar t'den önce ve sonra."""
    rng = np.random.default_rng(tohum); O, Ol, B = [], [], []
    for pz, sem in (("BIST", ["NA", "TRUE"]), ("ABD", ["AB_C", "XYZ"])):
        for g in ("BASARILI", "BASARISIZ"):
            for no, s in enumerate(sem, start=1):
                oid = f"wf|{pz}|{g}|{no}"; bas, t, bit, gb = 50, 70, 90, 88; a0, e = bas - 40, bit + 30
                ix = np.arange(a0, e + 1); n = len(ix); gun = pd.bdate_range("2021-01-04", periods=e + 1)[a0:]
                c = 10 * np.exp(np.cumsum(rng.normal(0, 0.01, n))) + rng.random() * 1e-7; o = c * np.exp(rng.normal(0, 0.003, n))
                h = np.maximum(o, c) * 1.004; l_ = np.minimum(o, c) * 0.996; h[ix > t] = 1e6        # gelecek zehirli
                B.append(pd.DataFrame({"oid": oid, "i": ix, "tarih": [str(z.date()) for z in gun], "o": o, "h": h, "l": l_, "c": c,
                                       "v": rng.lognormal(10, 0.3, n)}))
                Ol.append(pd.DataFrame({"oid": oid, "sira": [0, 1, 2], "i": [60, t, 100], "olay_tarih": [str(gun[60 - a0].date()), str(gun[t - a0].date()),
                                                                                                         str(gun[100 - a0].date())],
                                        "tur": ["BIST_BILANCO", "MAKRO_FOMC", "ABD_8K"], "kat": ["A", "C", "B"], "onceden": ["True", "True", "False"],
                                        "yas_olayda": [11, 21, 51]}))
                y = 1.0 if g == "BASARILI" else 0.0
                O.append({"oid": oid, "asama": "wf", "pazar": pz, "grup": g, "no": no, "sembol": s, "bolge": 0, "satir": 7 + no, "tanim": "T1",
                          "model": "M_TAM", "ufuk": 10, "t": t, "karar_tarih": str(gun[t - a0].date()), "yas": t - bas + 1, "bas": bas, "tespit": bas + 9,
                          "gen_bas": gb, "bit": bit, "bit_tur": 1, "bas_tarih": str(gun[bas - a0].date()), "tespit_tarih": str(gun[bas + 9 - a0].date()),
                          "gen_bas_tarih": str(gun[gb - a0].date()), "bit_tarih": str(gun[bit - a0].date()), "a0": a0, "son_tam": e,
                          "lo_t": float(c[bas - a0: t - a0 + 1].min()), "hi_t": float(c[bas - a0: t - a0 + 1].max()), "lo": float(c[bas - a0: bit - a0 + 1].min()),
                          "hi": float(c[bas - a0: bit - a0 + 1].max()), "sv_hat_var": 1.0, "sv_seviye": float(c[bas - a0: t - a0 + 1].min()),
                          "sv_taban": "govde", "sv_kirilma": 0.0, "Y1": 1.0 if no == 1 else -1.0, "Y2": 1.0, "haberli": 1.0, "habersiz": 0.0,
                          "p": 0.9, "esik": 0.8, "y": y, "y20": y, "sonuc": G.vg_sonuc_metni(y, 1.0), "baslik_tam_vdyt": f"{pz} {g} #{no} — özgün tam",
                          "baslik_sinyal_vdyt": f"{pz} {g} #{no} — özgün sinyal", "dosya_tam": f"{pz}_{g}_{no}_{s}_tam.png",
                          "dosya_sinyal": f"{pz}_{g}_{no}_{s}_sinyal.png"})
    meta = {"vdyt": {"kod_sha256": "0" * 64, "esik_sha256": "1" * 64, "onkayit_commit": "test", "on_kayit_bolum": "§13"}, "secim": {"tohum": 1},
            "cizim": CZ}
    return pd.DataFrame(O, columns=G.VG_SEMA["ornek.csv.gz"]), pd.concat(Ol, ignore_index=True), pd.concat(B, ignore_index=True), meta


def tar_degistir(yol: str, yeni: str, fn) -> str:
    with tarfile.open(yol) as tf:
        U = {m.name: tf.extractfile(m).read() for m in tf.getmembers()}
    fn(U)
    with open(yeni, "wb") as f:
        f.write(G._vg_tar_bayt(U))
    return yeni


def sekil_x(fig) -> tuple:
    """Şekildeki bütün veri öğelerinin en büyük x'i ve bütün metinler."""
    from matplotlib.collections import LineCollection
    xs, metin = [], []
    for ax in fig.axes:
        for c in ax.collections:
            if isinstance(c, LineCollection):
                for seg in c.get_segments():
                    xs += list(np.asarray(seg)[:, 0])
            else:
                for p in c.get_paths():
                    xs += list(p.vertices[:, 0])
        for p in ax.patches:
            bb = p.get_bbox() if hasattr(p, "get_bbox") else None
            if bb is not None and hasattr(p, "get_x"):
                xs += [p.get_x(), p.get_x() + p.get_width()]
            else:
                xs += list(p.get_path().transformed(p.get_patch_transform()).vertices[:, 0])
        for ln in ax.lines:
            xs += list(np.asarray(ln.get_xdata(), float))
        metin += [ax.get_title()] + [t.get_text() for t in ax.texts] + [t.get_text() for t in ax.get_xticklabels()]
        lg = ax.get_legend()
        if lg is not None:
            metin += [t.get_text() for t in lg.get_texts()]
        for t in ax.texts:
            xs.append(float(t.get_position()[0]))
    return max(xs), metin, fig.axes[0].get_ylim()


def testler() -> list:
    hata: list = []
    plt = G._vg_plt()
    O, Ol, B, meta = sentetik()
    with tempfile.TemporaryDirectory() as td:
        pk = os.path.join(td, "pk")
        # ------------------------------------------------------------ 1) şema + doğrulama + round trip
        y = G.vg_paket_yaz("wf", O, Ol, B, meta, [pk])[0]
        try:
            D = G.vg_dogrula(y)
            if D["ornek"] != len(O) or D["bar"] != len(B) or D["olay"] != len(Ol) or D["asama"] != "wf":
                hata.append(f"1) doğrulama özeti yanlış: {D}")
        except G.VgHata as ex:
            hata.append(f"1) geçerli paket reddedildi: {ex}")
        man, O2, Ol2, B2 = G.vg_dogrula_bayt(G._vg_tar_oku(y))
        if list(O2.columns) != G.VG_SEMA["ornek.csv.gz"] or list(Ol2.columns) != G.VG_SEMA["olay.csv.gz"] or list(B2.columns) != G.VG_SEMA["bar.csv.gz"]:
            hata.append("1) paket sütunları şemayla aynı değil")
        if not all(np.array_equal(B2[c].to_numpy(float), B[c].to_numpy(float)) for c in ("o", "h", "l", "c", "v")):
            hata.append("1) bar float'ları bit bit geri okunmadı")
        if sorted(O2.sembol) != sorted(O.sembol) or O2.sembol.map(type).ne(str).any():
            hata.append(f"1) semboller metin kalmadı: {list(O2.sembol)}")
        if G._vg_tar_bayt({"a": b"1"}) != G._vg_tar_bayt({"a": b"1"}) or G._vg_csv_gz(O) != G._vg_csv_gz(O):
            hata.append("1) paket yazımı belirlenimci değil")
        for k in ("asama", "sayim", "dosyalar", "sema", "vdyt", "cizim"):
            if k not in man:
                hata.append(f"1) manifestte {k} yok")

        # ------------------------------------------------------------ 2) SİNYAL GÜNÜ: gelecek yok
        o = O2.iloc[0].to_dict(); t = int(o["t"])
        Bo, Oo = B2[B2.oid == o["oid"]], Ol2[Ol2.oid == o["oid"]]
        for ozgun in (False, True):
            fig = G.vg_sekil(o, Bo, Oo, CZ, sinyal=True, ozgun=ozgun); xm, metin, yl = sekil_x(fig); plt.close(fig)
            if xm > t + 0.5 + 1e-9:
                hata.append(f"2) sinyal grafiğinde karar gününden sonra öğe var (x maks {xm} > {t + 0.5}; ozgun={ozgun})")
            if yl[1] > 1e5:
                hata.append("2) sinyal grafiğinin eksen sınırı gelecek barlardan etkilendi")
            yasak = ["YUKARI", "AŞAĞI", "BELİRSİZ", "GENİŞ", "genişleme", "sonuç", "BASARI", "BASARISIZ"] if not ozgun else ["YUKARI", "AŞAĞI", "genişleme"]
            bul = [w for w in yasak for m in metin if w in m]
            if bul:
                hata.append(f"2) sinyal grafiğinde gelecek / sonuç metni: {sorted(set(bul))} (ozgun={ozgun})")
            tar = [m for m in metin if re.fullmatch(r"\d{4}-\d{2}-\d{2}", m)]
            if any(m > o["karar_tarih"] for m in tar):
                hata.append("2) sinyal grafiğinde karar gününden sonraki tarih etiketi var")
        fig = G.vg_sekil(o, Bo, Oo, CZ, sinyal=False); xm, metin, _yl = sekil_x(fig); plt.close(fig)
        if xm < int(o["bit"]) or not any("genişleme" in m for m in metin) or not any("YUKARI" in m for m in metin) or not any("GENİŞLEDİ" in m for m in metin):
            hata.append("2) tam grafikte genişleme / yön / sonuç yok (test kendini doğrulamıyor)")
        if not any("BILANCO" in m for m in metin):
            hata.append("2) tam grafikte olay türü etiketi yok")

        # ------------------------------------------------------------ 3) + 5) çizim, üzerine yazmama, BAŞARILI ve BAŞARISIZ
        ck = os.path.join(td, "cikti")
        R1 = G.vg_ciz("wf", pk, ck)["wf"]
        if R1["hata"] or len(R1["png"]) != 2 * len(O) or R1["klasor"] != os.path.join(ck, "wf"):
            hata.append(f"3) ilk çizim: {len(R1['png'])} PNG, hata {R1['hata']}, klasör {R1['klasor']}")
        dosyalar = sorted(os.listdir(R1["klasor"]))
        for g in ("BASARILI", "BASARISIZ"):
            if not [f for f in dosyalar if f"_{g}_" in f and f.endswith("_tam.png")] or not [f for f in dosyalar if f"_{g}_" in f and f.endswith("_sinyal.png")]:
                hata.append(f"5) {g} grafikleri üretilmedi")
            if not [f for f in dosyalar if f.startswith("temas_") and f.endswith(f"_{g}.png")]:
                hata.append(f"5) {g} temas sayfası yok")
        dz = open(R1["dizin"], encoding="utf-8").read()
        if "| BASARILI |" not in dz or "| BASARISIZ |" not in dz:
            hata.append("5) dizinde BAŞARILI / BAŞARISIZ satırı yok")
        once = {f: G.vg_sha_dosya(os.path.join(R1["klasor"], f)) for f in dosyalar}
        R2 = G.vg_ciz("wf", pk, ck)["wf"]
        if R2["klasor"] == R1["klasor"] or os.path.dirname(R2["klasor"]) != R1["klasor"] or len(R2["png"]) != 2 * len(O):
            hata.append(f"3) ikinci çizim yeni alt klasöre gitmedi: {R2['klasor']}")
        if {f: G.vg_sha_dosya(os.path.join(R1["klasor"], f)) for f in dosyalar} != once:
            hata.append("3) ilk çizimin dosyaları değişti")
        ilk = os.path.join(R1["klasor"], dosyalar[0])
        durmali(lambda: G._vg_png_yaz(plt.figure(), ilk, 50), "3) PNG üzerine yazdı", hata)
        G.vg_paket_yaz("wf", O, Ol, B, meta, [pk])                    # aynı içerik: dokunmaz
        O_f = O.copy(); O_f.loc[0, "p"] = 0.95
        durmali(lambda: G.vg_paket_yaz("wf", O_f, Ol, B, meta, [pk]), "3) farklı paket üzerine yazdı", hata, "üzerine yazılmadı")

        # ------------------------------------------------------------ 4) manifest / şema doğrulaması; bozuk paket çizilmez
        def boz_bayt(U):
            b = bytearray(U["bar.csv.gz"]); b[len(b) // 2] ^= 0xFF; U["bar.csv.gz"] = bytes(b)

        def eksik_uye(U):
            U.pop("olay.csv.gz")

        def fazla_uye(U):
            U["x.py"] = b"print(1)"

        def sema_disi(U):
            import gzip as _gz, json as _js
            X = pd.read_csv(io.BytesIO(_gz.decompress(U["bar.csv.gz"]))).drop(columns=["v"]); b = G._vg_csv_gz(X); U["bar.csv.gz"] = b
            m = _js.loads(U["manifest.json"]); m["dosyalar"]["bar.csv.gz"].update({"sha256": G._vg_sha_bayt(b), "boy": len(b)}); U["manifest.json"] = _js.dumps(m).encode()

        def basari_bozuk(U):
            import gzip as _gz, json as _js
            X = G._vg_csv_oku(U["ornek.csv.gz"]); X.loc[X.grup == "BASARILI", "y"] = 0.0; b = G._vg_csv_gz(X); U["ornek.csv.gz"] = b
            m = _js.loads(U["manifest.json"]); m["dosyalar"]["ornek.csv.gz"].update({"sha256": G._vg_sha_bayt(b), "boy": len(b)}); U["manifest.json"] = _js.dumps(m).encode()
        for ad, fn, ic in (("bozuk bayt", boz_bayt, "sha256"), ("eksik üye", eksik_uye, "üyeleri"), ("fazla üye", fazla_uye, "üyeleri"),
                           ("şema dışı", sema_disi, "şema"), ("BAŞARILI tanımı", basari_bozuk, "tanımı")):
            kd = os.path.join(td, "boz_" + re.sub(r"\W", "_", ad)); os.makedirs(kd)
            tar_degistir(y, os.path.join(kd, "vdyt_grafik_paket_wf.tar"), fn)
            durmali(lambda: G.vg_dogrula(os.path.join(kd, "vdyt_grafik_paket_wf.tar")), f"4) {ad}: doğrulama geçti", hata, ic)
            co = os.path.join(td, "cikti_" + re.sub(r"\W", "_", ad))
            durmali(lambda: G.vg_ciz("hepsi", kd, co), f"4) {ad}: bozuk paket çizildi", hata)
            if os.path.exists(co):
                hata.append(f"4) {ad}: bozuk pakette çıktı klasörü açıldı")
        durmali(lambda: G.vg_paket_bul(os.path.join(td, "yok")), "4) olmayan paket durmadı", hata, "bulunamadı")

        # ------------------------------------------------------------ 6) yakalayıcı: asıl fonksiyon geri konur, dosya yazılmaz
        V = types.SimpleNamespace()

        def asil(d, b, t, hat, olaylar, yol, sadece_gecmis, baslik, E=None):
            raise AssertionError("asıl çizim çağrılmamalı")

        def vdyt_grafik(asama, cikti, pazarlar, E, F_ver):
            V.vdyt_grafik_ciz(F_ver["BIST"]["S"]["X"], {"bas": 1}, 3, 1.0, [2], os.path.join(cikti, asama, "BIST_HATLI_1_X_tam.png"), False, "b")
            V.vdyt_grafik_ciz(F_ver["BIST"]["S"]["X"], {"bas": 1}, 3, 1.0, [2], os.path.join(cikti, asama, "BIST_HATLI_1_X_sinyal.png"), True, "b")
            if asama == "kasa":
                raise ValueError("deneme hatası")
            return []
        V.vdyt_grafik_ciz = asil; V.vdyt_grafik = vdyt_grafik
        K = G.vg_yakala(V, "wf", "BIST", {"S": {"X": pd.DataFrame()}})
        if len(K) != 2 or K[0]["t"] != 3 or K[1]["sadece_gecmis"] is not True or V.vdyt_grafik_ciz is not asil:
            hata.append(f"6) yakalama yanlış ({len(K)} kayıt)")
        try:
            G.vg_yakala(V, "kasa", "BIST", {"S": {"X": pd.DataFrame()}}); hata.append("6) VDYT hatası yutuldu")
        except ValueError:
            pass
        if V.vdyt_grafik_ciz is not asil:
            hata.append("6) hata sonrası asıl çizim fonksiyonu geri konmadı")

        # ------------------------------------------------------------ 7) ad çözme
        if G._vg_ad_coz("/x/BIST_K62_HATSIZ_3_AB_C_sinyal.png") != ("BIST_K62", "HATSIZ", 3, "AB_C", "sinyal") or \
                G._vg_ad_coz("BIST_BASARISIZ_12_SEKFK_tam.png") != ("BIST", "BASARISIZ", 12, "SEKFK", "tam"):
            hata.append("7) grafik adı çözülemedi")
        durmali(lambda: G._vg_ad_coz("ABD_BASKA_1_X_tam.png"), "7) bilinmeyen grup kabul edildi", hata)

        # ------------------------------------------------------------ 8) özgün kip başlığı
        if G.vg_baslik(o, True, True) != o["baslik_sinyal_vdyt"] or G.vg_baslik(o, False, True) != o["baslik_tam_vdyt"]:
            hata.append("8) özgün başlık kullanılmadı")
        if o["grup"] in G.vg_baslik(o, True, False) or o["sembol"] not in G.vg_baslik(o, True, False) or "p = 0.900" not in G.vg_baslik(o, False, False):
            hata.append("8) başlık içeriği yanlış (sinyalde grup olmamalı; sembol ve olasılık olmalı)")

        # ------------------------------------------------------------ 9) bağımsızlık: VDYT.py olmadan, python -I
        kl = os.path.join(td, "yalniz"); os.makedirs(kl); shutil.copy(os.path.join(KOK, "VDYT_GRAFIK.py"), kl)
        r = subprocess.run([sys.executable, "-I", os.path.join(kl, "VDYT_GRAFIK.py"), "ciz", "--asama", "wf", "--girdi", pk, "--cikti",
                            os.path.join(td, "bagimsiz"), "--temas_yok"], capture_output=True, text=True, timeout=600, cwd=kl)
        if r.returncode != 0 or len([f for f in os.listdir(os.path.join(td, "bagimsiz", "wf")) if f.endswith(".png")]) != 2 * len(O):
            hata.append(f"9) VDYT.py olmadan çizim çalışmadı: {r.returncode} {r.stderr[-400:]}")
        r = subprocess.run([sys.executable, "-I", os.path.join(kl, "VDYT_GRAFIK.py"), "dogrula", "--girdi", pk], capture_output=True, text=True, timeout=300)
        if r.returncode != 0 or '"ornek": 8' not in r.stdout:
            hata.append(f"9) komut satırı doğrulama: {r.returncode} {r.stdout[-200:]} {r.stderr[-200:]}")
    kaynak = open(os.path.join(KOK, "VDYT_GRAFIK.py"), encoding="utf-8").read()
    if re.search(r"^\s*(import|from)\s+(VDYT|FON_IZI|K5\d|K6\d|COL_\w+|IZ_KARNE|BASLAT|takip)\b", kaynak, re.M):
        hata.append("9) VDYT_GRAFIK modül düzeyinde VDYT / Çöl Yolu içe alıyor (ciz bağımsız olmalı)")

    # ------------------------------------------------------------ 10) çakışma kapısı
    ns = {"__name__": "vg_test", "vg_ciz": "başka dosyanın adı", "_CK_KAYIT": {"vg_ciz": "BASKA.py"}}
    try:
        exec(compile(kaynak, "VDYT_GRAFIK.py", "exec"), ns); hata.append("10) başka dosyanın adını ezen yükleme durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"10) çakışma kapısı yanlış nedenle durdu: {ex}")
    ns2 = {"__name__": "vg_test"}
    exec(compile(kaynak, "VDYT_GRAFIK.py", "exec"), ns2); exec(compile(kaynak, "VDYT_GRAFIK.py", "exec"), ns2)

    # ------------------------------------------------------------ 11) e-posta / anahtar yok
    for ad in ("VDYT_GRAFIK.py", "test_vdyt_grafik.py"):
        mt = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if G._VG_EPOSTA.search(mt) or re.search(r"(api[_-]?key|token|password|sifre)\s*=\s*['\"][A-Za-z0-9]{8,}", mt, re.I):
            hata.append(f"11) {ad} içinde e-posta / anahtar biçimli parça var")
    return hata


if __name__ == "__main__":
    h = testler()
    for x in h:
        print("HATA:", x)
    print("test_vdyt_grafik:", "TAMAM (11/11)" if not h else f"{len(h)} HATA")
    sys.exit(1 if h else 0)
