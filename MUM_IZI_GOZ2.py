"""MUM_IZI_GOZ2 — MUM_IZI EK 13: göz ölçümünün İKİNCİ BAKIŞI (26 Kasım 2026).

Ana modelin görevi: MUM_IZI11 göz ölçümü AYNI ön kayıtlı tanımlarla (MUM_IZI_GOZ.py GZ_ESIK; hiçbir tanım / eşik değişmez) set 5 (MUM_IZI12_ONAY: hakem v3'ün
seçtiği 24 bölge; Cemal EVET 11 / KISMEN 8 / HAYIR 5) eklenerek yeniden koşulur. Üç rapor ailesi: (i) İLK BAKIŞ = set 1-4 (MUM_IZI11 sonucu, değişmez; json'dan),
(ii) İKİNCİ BAKIŞ = yalnız set 5, (iii) BİRLEŞİK = set 1-5. Ek ölçü (ön kayıtta): EVET - eş = EVET'lerin eşli farkının sıfırdan farkı, işaret çevirme
permütasyonu (iki yönlü, 10.000). MUM_IZI_GOZ.py ve MUM_IZI11 çıktıları değişmez (içe alınır / okunur). GETİRİ bilgi; n < 30 'örneklem yetersiz'; 'iz / tuttu' yok;
kasa açılmaz. Veri <= 2022-12-31.

Komut:  python MUM_IZI_GOZ2.py ornek | onkayit | kos | pdf
EK 15 (kopma ayrımı; yeni getiri yok, mum_izi13_olay.csv gruplama):  python MUM_IZI_GOZ2.py kopma_sayim | kopma_onkayit | kopma
EK 16 (ölçek: sayfadaki / gerçek mum boyu; yeni getiri yok):            python MUM_IZI_GOZ2.py olcek_olcu | olcek_onkayit | olcek
EK 17 (üçüncü bakış: set 6 = MUM_IZI14 ölçekli onay 17 bölge; birleşik 145): python MUM_IZI_GOZ2.py set6_sayim | set6_onkayit | set6_kos | set6_pdf
EK 19 (dördüncü bakış: set 7 = MUM_IZI18 mum boyu kapılı onay 12 bölge; set 6+7; birleşik 157): python MUM_IZI_GOZ2.py set7_sayim | set7_onkayit | set7_kos | set7_pdf
EK 21 (beşinci bakış: set 8 = MUM_IZI20 katmanlı onay 24 bölge; kapıdan geçenler 36; set 6+7+8; birleşik 181): python MUM_IZI_GOZ2.py set8_sayim | set8_onkayit | set8_kos | set8_pdf
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_G2 = {k: id(v) for k, v in globals().items()}

import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_G2 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_G2 not in sys.path:
    sys.path.insert(0, KOK_G2)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_GOZ as GZ  # noqa: E402  (DEĞİŞTİRİLMEZ: tanımlar ve ölçü fonksiyonları)
import MUM_IZI_HAFTALIK as MH  # noqa: E402
import MUM_IZI_V2 as MV  # noqa: E402

g2log = logging.getLogger("col.mum_izi_goz2")
if not g2log.handlers:
    _g2_h = logging.StreamHandler(sys.stderr)
    _g2_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_goz2: %(message)s", "%H:%M:%S"))
    g2log.addHandler(_g2_h)
    g2log.setLevel(logging.INFO)
    g2log.propagate = False


class G2Hata(RuntimeError):
    """Durdurucu hata: kapı / şema / veri."""


G2_SURUM = "MUM_IZI_GOZ2 v1.0 (2026-11-26): göz ölçümü ikinci bakış (set 5) + birleşik; tanımlar MUM_IZI_GOZ GZ_ESIK aynen"
_C = MI.MI_YOL["cikti"]
G2_YOL = {"cikti": _C, "kod": os.path.join(KOK_G2, "MUM_IZI_GOZ2.py"), "set5": (os.path.join(_C, "cemal_mum_izi12_onay.json"), os.path.join(_C, "MUM_IZI12_onay_anahtar.json"),
          "MUM_IZI12_ONAY"), "sonuc11": os.path.join(_C, "mum_izi11_sonuc.json"), "olay11": os.path.join(_C, "mum_izi11_olay.csv")}
G2_DOSYA = {"onkayit": "MUM_IZI13_ON_KAYIT.md", "rapor": "MUM_IZI13_RAPOR.md", "sonuc": "mum_izi13_sonuc.json", "olay": "mum_izi13_olay.csv", "pdf": "MUM_IZI13_SONRASI.pdf"}
G2_EK: Dict[str, Any] = {
    "surum": "G2-1.0", "tanim": "MUM_IZI_GOZ GZ_ESIK aynen (ESIK11_SHA ön kayıtta)",
    "set5": "MUM_IZI12_ONAY (s2-25; anahtar: yeni_sayfa, bolge_bas (ilk barın tarihi), bolge_son, pencere); işaret EVET / KISMEN / HAYIR",
    "aileler": {"ilk_bakis": "set 1-4: MUM_IZI11 sonucu (mum_izi11_sonuc.json), değişmez", "ikinci_bakis": "yalnız set 5 (yeni, bağımsız örnek)",
                "birlesik": "set 1-5 (eş dışlama kümesi 128 olayla; set 1-4 olayları MUM_IZI11 ile karşılaştırılır, fark yazılır)"},
    "evet_es": {"tanim": "EVET (ve EVET + KISMEN) eşli farkının ortalaması; %95 olay bootstrap (GZ ile aynı); p = işaret çevirme permütasyonu (eşli farkların "
                         "işaretleri rastgele çevrilir), iki yönlü, 10.000, tohum 25112131", "perm": 10000, "tohum": 25112131},
    "yon": "ilk bakışla aynı yön mü: her dilimde EVET - HAYIR eşli fark farkının ve EVET eşli farkının İŞARETİ ilk bakışla aynı mı (büyüklük / p değil)",
}


def _g2_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or G2_YOL["cikti"], G2_DOSYA[ad])


def g2_ek_sha() -> str:
    return hashlib.sha256(json.dumps(G2_EK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


# ================================================================ 1) ÖRNEKLEM
def g2_set5() -> pd.DataFrame:
    iy, ay, ad = G2_YOL["set5"]; E = GZ.gz_isaret_oku(iy); A = json.load(open(ay, encoding="utf-8"))["sayfalar"]; rows = []
    for r in A:
        pg = int(r["yeni_sayfa"]); lab = E.get(pg, "eksik")
        rows.append({"set": "set5", "set_ad": ad, "sayfa": pg, "isaret": lab, "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "tarih": r["bolge_son"],
                     "m": int(r["pencere"]), "bolge_bas_anahtar": r["bolge_bas"]})
    X = pd.DataFrame(rows); X["sinif"] = np.where(X.isaret.isin(GZ.SINIF), X.isaret, None); X["sinif_son"] = X["sinif"]
    return X[X.sinif.notna()].reset_index(drop=True)


def g2_ornek() -> pd.DataFrame:
    X = pd.concat([GZ.gz_ornek(), g2_set5()], ignore_index=True)
    if X.duplicated(["zaman", "sembol", "tarih"]).any():
        raise G2Hata("K4: aynı bölge iki kez")
    return X


# ================================================================ 2) EK İSTATİSTİK
def g2_isaret_perm(x: np.ndarray, n: int, tohum: int) -> Optional[float]:
    """Ortalama 0'dan farklı mı: işaret çevirme permütasyonu (iki yönlü)."""
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 2:
        return None
    obs = abs(x.mean()); rng = np.random.default_rng(tohum); s = rng.choice([-1.0, 1.0], size=(n, len(x)))
    return float((1 + int((np.abs((s * x).mean(1)) >= obs - 1e-15).sum())) / (1 + n))


def g2_evet_es(Y: pd.DataFrame) -> Dict[str, Any]:
    E = G2_EK["evet_es"]; out = {}
    o = Y[Y.olculdu.astype(bool)]
    for zi, z in enumerate(("gunluk", "haftalik", "birlesik")):
        for si, (ad, sl) in enumerate((("EVET", ["EVET"]), ("EVET+KISMEN", ["EVET", "KISMEN"]), ("HAYIR", ["HAYIR"]))):
            g = o[o.sinif.isin(sl)] if z == "birlesik" else o[(o.zaman == z) & o.sinif.isin(sl)]
            f = g.fark.astype(float).to_numpy(); f = f[np.isfinite(f)]
            out[f"{ad}-es|{z}"] = {"n_es": int(len(f)), "esli_fark_ort": float(f.mean()) if len(f) else None,
                                   "boot95": GZ.gz_boot(f, GZ.GZ_ESIK["tablo"]["B"], 25112141 + 10 * zi + si)["ort95"], "p": g2_isaret_perm(f, E["perm"], E["tohum"] + 10 * zi + si)}
    return out


# ================================================================ 3) KAPI, ÖN KAYIT, KOŞU
def g2_sha_simdi() -> Dict[str, str]:
    iy, ay, _ = G2_YOL["set5"]
    return {"KOD13_SHA": MI._mi_sha(G2_YOL["kod"]), "EK13_SHA": g2_ek_sha(), "GZ_KOD_SHA": MI._mi_sha(GZ.GZ_YOL["kod"]), "ESIK11_SHA": GZ.gz_esik_sha(),
            "ISARET_SET5_SHA": MI._mi_sha(iy), "ANAHTAR_SET5_SHA": MI._mi_sha(ay), "SONUC11_SHA": MI._mi_sha(G2_YOL["sonuc11"]), "OLAY11_SHA": MI._mi_sha(G2_YOL["olay11"])}


def g2_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or G2_YOL["cikti"]; yol = _g2_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise G2Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = g2_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise G2Hata(f"ön kayıt kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_G2); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise G2Hata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_GOZ2.py", "MUM_IZI_GOZ.py"]):
        raise G2Hata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def g2_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or G2_YOL["cikti"]; y = _g2_yol("onkayit", cikti)
    if os.path.exists(y):
        raise G2Hata("ön kayıt zaten var")
    X = g2_ornek(); S5 = GZ.gz_ornek_sayim(X[X.set == "set5"]); SB = GZ.gz_ornek_sayim(X); sh = g2_sha_simdi()
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in GZ.GZ_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_GOZ2.py"])
    s = [f"# MUM_IZI13 ÖN KAYIT ({MI._mi_simdi()})", "",
         "MUM_IZI11_ON_KAYIT tanımları AYNEN (MUM_IZI_GOZ.py GZ_ESIK; ESIK11_SHA aşağıda; giriş, ufuk 15 mum, stop, dokunma, R30, CETVEL2 konum eşi, tablolar, "
         "permütasyon). Ek: set 5 = MUM_IZI12_ONAY 24 bölge. Bu dosya set 5'in getirileri hesaplanmadan ÖNCE commit edilir.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_GOZ2.py commit'i: {kc or 'yok'}", "",
         "## Üç rapor satırı ailesi", "",
         "- (i) İLK BAKIŞ = set 1-4: MUM_IZI11 sonucu (mum_izi11_sonuc.json), DEĞİŞMEZ.",
         "- (ii) İKİNCİ BAKIŞ = yalnız set 5: ilk bakıştan bağımsız yeni örnek. Soru: ilk bakıştaki yön tekrar ediyor mu (haftalıkta EVET eşlerin ve HAYIR'ın gerisinde: "
         "EVET eşli fark -%16,2, EVET - HAYIR eşli -15,7 puan; günlükte belirgin fark yok: EVET - HAYIR eşli +5,7 puan, p 0,29). 'Aynı yön' = ilgili farkın İŞARETİ aynı.",
         "- (iii) BİRLEŞİK = set 1-5 (128 bölge). Eş dışlama kümesi 128 olayla kurulur; set 1-4 olaylarının değerleri MUM_IZI11 ile karşılaştırılır, fark varsa yazılır.",
         "- Ek ölçü: EVET - eş (EVET'lerin eşli farkı 0'dan farklı mı): olay bootstrap %95 + işaret çevirme permütasyonu (iki yönlü, 10.000, tohum 25112131); "
         "EVET + KISMEN ve HAYIR için de aynı (bilgi).", "",
         "## Sınıf sayıları (getirisiz)", "", f"- Set 5: {json.dumps(S5, ensure_ascii=False)}", f"- Birleşik (set 1-5): {json.dumps(SB, ensure_ascii=False)}", "",
         "## Ek tanımlar (G2_EK; sha yukarıda)", "", "```", json.dumps(G2_EK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ (MUM_IZI11 ile aynı; K8: set 5 hücreleri n < 30)", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 13")


def g2_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    t0 = time.time(); cikti = cikti or G2_YOL["cikti"]
    if os.path.exists(_g2_yol("sonuc", cikti)):
        raise G2Hata("sonuç zaten var")
    G0 = g2_kapi(cikti)
    kasa = KS.kasa_kapisi([os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] +
                          [os.path.join(MH.MH_YOL["tam"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")],
                          "2022-12-31")
    X = g2_ornek(); Y = GZ.gz_es(GZ.gz_olc(X)); Y = Y.sort_values(["set", "sayfa"]).reset_index(drop=True)
    kol = ["set", "set_ad", "sayfa", "isaret", "sinif", "sinif_son", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "m", "olculdu", "neden", "giris", "E0", "stop", "son15",
           "R15", "max15", "min15", "stop15", "d5", "d10", "d20", "R30", "panel", "kova", "n_es", "es_R15", "es_med", "fark", "sira", "es_max15", "es_min15", "es_d5", "es_d10",
           "es_d20", "es_stop15", "es_neden"]
    for c in kol:
        if c not in Y:
            Y[c] = np.nan
    O = Y[kol].copy()
    for c in ("bolge_bas", "bolge_son", "giris", "son15"):
        O[c] = pd.to_datetime(O[c]).dt.strftime("%Y-%m-%d")
    O.to_csv(_g2_yol("olay", cikti), index=False, float_format="%.6f")
    # set 1-4 değerleri MUM_IZI11 ile aynı mı (eş dışlama kümesi büyüdü)
    O11 = pd.read_csv(G2_YOL["olay11"]); O2 = pd.read_csv(_g2_yol("olay", cikti)); M = O11.merge(O2[O2.set != "set5"], on=["set", "sayfa"], suffixes=("_11", "_13"))
    fk = {}
    for c in ("R15", "es_R15", "fark", "n_es"):
        a = M[f"{c}_11"].to_numpy(float); b = M[f"{c}_13"].to_numpy(float); fk[c] = int((~(np.isclose(a, b, atol=1e-9) | (np.isnan(a) & np.isnan(b)))).sum())
    J11 = json.load(open(G2_YOL["sonuc11"], encoding="utf-8"))
    Y5 = Y[Y.set == "set5"]
    J = {"surum": G2_SURUM, "kapi": G0, "kasa": kasa, "ornek": {"set5": GZ.gz_ornek_sayim(X[X.set == "set5"]), "birlesik": GZ.gz_ornek_sayim(X)},
         "olculemedi": {"set5": Y5[~Y5.olculdu.astype(bool)].neden.value_counts().to_dict(), "birlesik": Y[~Y.olculdu.astype(bool)].neden.value_counts().to_dict()},
         "es_yok": {"set5": Y5[Y5.olculdu.astype(bool)].es_neden.fillna("").replace("", "var").value_counts().to_dict(),
                    "birlesik": Y[Y.olculdu.astype(bool)].es_neden.fillna("").replace("", "var").value_counts().to_dict()},
         "set1_4_mum_izi11_farki": {"satir": int(len(M)), "farkli": fk},
         "ilk_bakis": {"tablo": J11["tablo"]},
         "ikinci_bakis": {"tablo": GZ.gz_tablolar(Y5), "evet_es": g2_evet_es(Y5)},
         "birlesik": {"tablo": GZ.gz_tablolar(Y), "evet_es": g2_evet_es(Y), "duyarlilik_son_isaret": GZ.gz_tablolar(Y, "sinif_son")["karsilastirma"]},
         "ilk_bakis_evet_es": g2_evet_es(Y[Y.set != "set5"]),
         "olay_sha": MI._mi_sha(_g2_yol("olay", cikti)), "sure_sn": round(time.time() - t0)}
    J["yon"] = g2_yon(J)
    MI._mi_jyaz(_g2_yol("sonuc", cikti), J, "sonuç 13")
    return J


def g2_yon(J: Dict[str, Any]) -> Dict[str, Any]:
    """İkinci bakış ilk bakışla aynı yönde mi (işaret)."""
    out = {}
    for z in ("gunluk", "haftalik"):
        k1 = J["ilk_bakis"]["tablo"]["karsilastirma"][f"EVET-HAYIR|{z}"]["esli_fark_fark"]; k2 = J["ikinci_bakis"]["tablo"]["karsilastirma"][f"EVET-HAYIR|{z}"]["esli_fark_fark"]
        e1 = J["ilk_bakis_evet_es"][f"EVET-es|{z}"]["esli_fark_ort"]; e2 = J["ikinci_bakis"]["evet_es"][f"EVET-es|{z}"]["esli_fark_ort"]
        out[z] = {"EVET-HAYIR_esli": {"ilk": k1, "ikinci": k2, "ayni_yon": None if (k1 is None or k2 is None) else bool(np.sign(k1) == np.sign(k2))},
                  "EVET-es": {"ilk": e1, "ikinci": e2, "ayni_yon": None if (e1 is None or e2 is None) else bool(np.sign(e1) == np.sign(e2))}}
    return out


# ================================================================ 4) PDF
def g2_pdf(cikti: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    cikti = cikti or G2_YOL["cikti"]; y = _g2_yol("pdf", cikti)
    J = json.load(open(_g2_yol("sonuc", cikti), encoding="utf-8"))
    if MI._mi_sha(_g2_yol("olay", cikti)) != J["olay_sha"]:
        raise G2Hata("olay csv'si sonuç json'uyla uyuşmuyor")
    O = pd.read_csv(_g2_yol("olay", cikti)); H = J["birlesik"]["tablo"]["hucre"]; Vc: Dict[Any, Any] = {}; f = GZ._gz_y
    ad = {"EVET": "BENZİYOR", "KISMEN": "KISMEN", "HAYIR": "BENZEMİYOR"}

    def ozet(T: Dict[str, Any], E: Dict[str, Any]) -> str:
        p = []
        for z, zad in (("haftalik", "haftalık"), ("gunluk", "günlük")):
            e = T["hucre"][f"EVET|{z}"]; h = T["hucre"][f"HAYIR|{z}"]; ee = E[f"EVET-es|{z}"]
            p.append(f"{zad}: BENZİYOR {e.get('n', 0)} bölge ortalama {f(e.get('R15_ort'))}, eşlerinden {f(ee.get('esli_fark_ort'))}; BENZEMİYOR {h.get('n', 0)} bölge "
                     f"{f(h.get('R15_ort'))}")
        return "; ".join(p)
    with PdfPages(y, metadata={"Title": "MUM_IZI13 sonrası", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); n_e = int(sum(H[f"EVET|{z}"]["n"] for z in ("gunluk", "haftalik")))
        fig.text(0.05, 0.95, f"Senin BENZİYOR dediğin {n_e} bölge sonrasında ne yaptı (128 bölge, hepsi)", fontsize=14, weight="bold")
        fig.text(0.05, 0.915, "Giriş: bölgeden sonraki ilk mumun açılışı. 15 mum sonra kapanışla getiri. Eş: aynı gün, benzer oynaklık ve likiditedeki hisseler.", fontsize=9.5)
        ax = fig.add_axes([0.03, 0.47, 0.94, 0.42]); ax.axis("off"); sat = []
        for z, zad in (("haftalik", "haftalık (15 hafta)"), ("gunluk", "günlük (15 gün)")):
            for s in GZ.SINIF:
                c = H[f"{s}|{z}"]; n = c.get("n", 0)
                sat.append([ad[s], zad, str(n), f"{int(round(c.get('arti_pay', 0) * n))} / {n}" if n else "-", f(c.get("R15_ort")), f(c.get("R15_med")), f(c.get("es_ort")),
                            f"{int(round(c.get('dokunma_d10', 0) * n))} / {n}" if n else "-", f"{int(round(c.get('stop_pay', 0) * n))} / {n}" if n else "-"])
        tb = ax.table(cellText=sat, colLabels=["senin işaretin", "mum", "bölge", "artıda kapanan", "ortalama", "medyan", "eşlerin ort.", "+%10'a dokunan", "stop olan"],
                      loc="upper center", cellLoc="center", colWidths=[0.14, 0.15, 0.07, 0.12, 0.1, 0.1, 0.1, 0.12, 0.1])
        tb.auto_set_font_size(False); tb.set_fontsize(9); tb.scale(1, 2.0)
        fig.text(0.05, 0.43, "İlk 104 bölgede: " + ozet(J["ilk_bakis"]["tablo"], J["ilk_bakis_evet_es"]) + ".", fontsize=9.5, va="top", wrap=True)
        fig.text(0.05, 0.36, "Yeni 24 bölgede: " + ozet(J["ikinci_bakis"]["tablo"], J["ikinci_bakis"]["evet_es"]) + ".", fontsize=9.5, va="top", wrap=True)
        fig.text(0.05, 0.28, "Sayılar az (N < 30): bu bir sonuç değil, ilk bakış.", fontsize=13, weight="bold")
        fig.text(0.05, 0.24, "Sonraki sayfalar: YENİ 24 bölgeden BENZİYOR dediklerin (önce haftalık, sonra günlük), sonra KISMEN dediklerin.\n"
                 "Hisse ve tarih açık; turuncu kutu = bölge, yeşil çizgi = giriş, kırmızı = stop (bölge dibi x 0,98), gri dikey = 15. mum.", fontsize=9.5, va="top")
        pdf.savefig(fig); plt.close(fig)
        for s in ("EVET", "KISMEN"):
            X = O[(O.set == "set5") & (O.sinif == s)].copy(); X["zs"] = X.zaman.map({"haftalik": 0, "gunluk": 1}); X = X.sort_values(["zs", "bolge_son"])
            for r in X.itertuples():
                k = (r.zaman, r.pazar)
                if k not in Vc:
                    Vc[k] = MV.mv_veri(*k)
                d = Vc[k][r.sembol]; t = d.index.get_loc(pd.Timestamp(r.bolge_son)) if r.zaman == "gunluk" else int(np.flatnonzero(d.index >= pd.Timestamp(r.bolge_son))[0])
                m = int(r.m); i0 = max(0, t - m + 1 - 15); i1 = min(len(d) - 1, t + 30); eksik = (t + 30) - i1
                BU, BO, BA = MI.mi_bant(d.Close.to_numpy(float)); sl = slice(i0, i1 + 1)
                fig = plt.figure(figsize=(8.3, 11.7)); ax = fig.add_axes([0.07, 0.36, 0.9, 0.56])
                MV._mv_ciz(ax, *(d[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close")), BU[sl], BO[sl], BA[sl], (t - m + 1 - i0, t - i0),
                           f"{ad[s]} · {r.sembol} ({r.pazar}) · {'haftalık' if r.zaman == 'haftalik' else 'günlük'} · bölge {r.bolge_bas} .. {r.bolge_son}")
                xg = t + 1 - i0
                if np.isfinite(r.E0):
                    ax.axvline(xg - 0.5, color="#1a9850", linewidth=1.2, linestyle="--"); ax.hlines(r.E0, xg - 0.5, i1 - i0 + 0.5, color="#1a9850", linewidth=1)
                if np.isfinite(r.stop):
                    ax.hlines(r.stop, t - m + 1 - i0 - 0.5, i1 - i0 + 0.5, color="#d73027", linewidth=1)
                if t + 15 <= i1:
                    ax.axvline(t + 15 - i0 + 0.4, color="#777777", linewidth=1.2)
                ax.set_xticks([t - m + 1 - i0, xg] + ([t + 15 - i0] if t + 15 <= i1 else []))
                ax.set_xticklabels([str(d.index[t - m + 1].date()), "giriş"] + (["15. mum"] if t + 15 <= i1 else []), fontsize=8)
                if bool(r.olculdu):
                    alt = (f"15 mum getirisi: {f(r.R15)}   ·   eşlerin ortalaması: {f(r.es_R15) if np.isfinite(r.es_R15) else 'eş yok'}   ·   en yüksek: {f(r.max15)}   ·   "
                           f"en derin: {f(r.min15)}\n30 mum getirisi: {f(r.R30) if np.isfinite(r.R30) else '-'}   ·   stop: {'oldu' if r.stop15 == 1 else 'olmadı'}")
                else:
                    alt = f"ölçülmedi: {r.neden}"
                if eksik > 0:
                    alt += f"\nsonrası {30 - eksik} mum (veri 2022-12-30'da bitiyor)"
                fig.text(0.07, 0.3, alt, fontsize=11, va="top")
                pdf.savefig(fig); plt.close(fig)
    return y


# ================================================================ 4b) MUM_IZI EK 15: KOPMA AYRIMI (yeni getiri hesabı yok; yalnız mum_izi13_olay.csv gruplama)
K15_SURUM = "MUM_IZI_GOZ2 kopma v1.0 (2026-11-26): EK 15 kopma ayrımı; iki sonrasını-görmeyen hakem (K1, K2); mum_izi13_olay.csv satırları aynen"
K15_DOSYA = {"onkayit": "MUM_IZI15_ON_KAYIT.md", "rapor": "MUM_IZI15_RAPOR.md", "sonuc": "mum_izi15_sonuc.json", "olay": "mum_izi15_olay.csv"}
K15_YOL = {"K1": os.path.join(_C, "mum_izi15_kopma_K1.json"), "K2": os.path.join(_C, "mum_izi15_kopma_K2.json"), "olay13": os.path.join(_C, "mum_izi13_olay.csv"),
           "anahtar6": os.path.join(_C, "mum_izi6_anahtar.json")}
K15_K = ("KOPMUS", "BASKI", "BELIRSIZ")
K15_EK: Dict[str, Any] = {
    "surum": "K15-1.0", "kaynak": "mum_izi13_olay.csv (128 bölge; R15, es_R15, fark = R15 - es_R15, sinif, zaman AYNEN; yeni getiri hesabı yok)",
    "hakem": "mum_izi15_kopma_K1.json / _K2.json; anahtar (set, sayfa) = csv set ve sayfa; k KOPMUS / BASKI / BELIRSIZ, puan 0-10 (10 = net kopmuş)",
    "uzlasi": "iki hakem KOPMUS -> KOPMUS; ikisi BASKI -> BASKI; ötekiler KARISIK",
    "duyarlilik": {"tanim": "iki hakemin ortalama puanı >= 6 -> KOPMUS*, <= 4 -> BASKI*, arası ARA*", "ust": 6.0, "alt": 4.0},
    "aileler": {"ANA": ["EVET"], "IKINCI": ["EVET", "KISMEN"], "UCUNCU": ["EVET", "KISMEN", "HAYIR"]},
    "zaman": ["haftalik", "gunluk", "birlikte"],
    "hucre": "n (ölçülen), R15 ort / medyan, n_es, eşli fark ort / medyan, artıda payı (R15 > 0), eşinden iyi payı (fark > 0; eşi olanlarda)",
    "karsilastirma": {"tanim": "KOPMUS - BASKI (duyarlılıkta KOPMUS* - BASKI*) eşli fark ortalaması farkı; p = etiket permütasyonu (GZ.gz_perm), iki yönlü, 10.000, tohum 15 "
                               "(her karşılaştırmada aynı tohum); bir grup boş ya da n < 2 -> 'karşılaştırma yapılamaz'", "perm": 10000, "tohum": 15, "n_min": 2},
    "okuma": "AYRIM YÖNÜ CEMAL'İN DEDİĞİ GİBİ <=> ANA (EVET) içinde KOPMUS eşli fark ortalaması > 0 VE KOPMUS - BASKI > 0, haftalıkta ve günlükte aynı yönde; "
             "biri hesaplanamazsa 'OKUNAMADI (karşılaştırma yapılamaz)'; uzlaşı ve duyarlılık ayrı okunur",
    "etiket": "BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK",
    "bilgi_spearman": "EVET bölgelerinde iki hakemin ortalama puanı ile eşli fark arasında Spearman korelasyonu (haftalık, günlük, birlikte)",
    "kappa": "Cohen kappa, üç sınıf (KOPMUS / BASKI / BELIRSIZ): 128 csv bölgesi (ana) ve hakemlerin bütün sayfaları (bilgi)",
    "tekrar": "set2 katman T sayfaları (MUM_IZI6_ETIKET 7, 8, 9, 20, 26, 28, 34, 46) = set1 bölgeleri (mum_izi6_anahtar.json zaman + sembol + tarih = csv set1 bolge_son); "
              "her hakemin iki bakışta aynı k vermesi ve puan farkı",
    "es_siniri": "eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240)",
}
K15_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eşli fark mum_izi13_olay.csv'den aynen (aynı giriş günü aynı kova CETVEL2 konum eşi); yeni eş yok; sınır: eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240)"),
    "K2": ("EVET", "hakemler sonrasını görmedi (işaretsiz PDF bölge sonunda kesik; yasak liste hakem metninde); hakem json'ları hesaptan önce commit; SINIR: ölçüt Cemal "
                   "sonrasını gördükten sonra söylendi -> GERİYE DÖNÜK"),
    "K3": ("EVET", "geçerli bar kuralı MUM_IZI11 / 13 ölçümünde (MI.mi_veri H > L, V > 0); bu iş bar okumaz"),
    "K4": ("EVET", "128 tekil bölge (GZ.gz_ornek K4 denetimi); set2 T tekrar sayfaları ayrı bölge sayılmaz, yalnız hakem tutarlılığında kullanılır"),
    "K5": ("EVET", "giriş = bölgeden sonraki ilk geçerli barın açılışı (MUM_IZI11 tanımı, csv aynen)"),
    "K6": ("EVET", "getiriler oransal, csv aynen; pazarlar arası karşılaştırma eşli farkla"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz"),
    "K8": ("EVET", "bütün gruplar n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK'; n < 2 grup 'karşılaştırma yapılamaz'; tek dönem (<= 2022), BH yok (karar yok)"),
    "K9": ("EVET", "bu ön kayıt (KOD15 / EK15 / hakem / olay sha + getirisiz sayımlar) hesaptan önce commit; k15_kapi sha + commit + temiz ağaç denetler"),
    "K10": ("EVET", "hakem json şeması denetlenir (k ve puan aralığı; bilinmeyen değer DUR); (set, sayfa) eşleşmesi 128 / 128 değilse DUR; tekrar eşlemesi anahtardan"),
    "K11": ("EVET", "tablo sayılarından >= 2 hücre olay csv'sinden bağımsız pandas koduyla yeniden üretilir (rapor öncesi denetim)"),
    "K12": ("EVET", "'iz / tuttu / anlamlı' sözü yok; sayı ile yorum ayrı; okuma kuralı yalnız yön"),
    "K13": ("EVET", "çakışma kapısı korunur; çalışan komutlar değişmez (test); yasak defter dosyalarına dokunulmaz; yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez"),
}


def _k15_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or G2_YOL["cikti"], K15_DOSYA[ad])


def k15_ek_sha() -> str:
    return hashlib.sha256(json.dumps(K15_EK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def k15_hakem_oku(yol: str) -> Dict[Tuple[str, int], Dict[str, Any]]:
    """Hakem json'u -> {(set, sayfa): {k, puan, gerekce}}; şema dışı değer DUR."""
    try:
        J = json.load(open(yol, encoding="utf-8"))
    except (OSError, ValueError) as ex:
        raise G2Hata(f"hakem dosyası okunamadı: {yol}: {ex}") from ex
    if not isinstance(J, dict) or not isinstance(J.get("sayfalar"), dict):
        raise G2Hata(f"hakem şeması: 'sayfalar' yok: {os.path.basename(yol)}")
    out: Dict[Tuple[str, int], Dict[str, Any]] = {}
    for st, S in J["sayfalar"].items():
        for pg, v in S.items():
            k = v.get("k") if isinstance(v, dict) else None; p = v.get("puan") if isinstance(v, dict) else None
            if k not in K15_K or isinstance(p, bool) or not isinstance(p, (int, float)) or not (0 <= p <= 10):
                raise G2Hata(f"hakem şeması: {os.path.basename(yol)} {st} sayfa {pg}: k={k!r} puan={p!r}")
            out[(str(st), int(pg))] = {"k": k, "puan": float(p), "gerekce": str(v.get("gerekce", ""))}
    return out


def k15_uzlasi(k1: str, k2: str) -> str:
    return "KOPMUS" if k1 == k2 == "KOPMUS" else ("BASKI" if k1 == k2 == "BASKI" else "KARISIK")


def k15_duyar(p: float) -> str:
    D = K15_EK["duyarlilik"]
    return "KOPMUS*" if p >= D["ust"] else ("BASKI*" if p <= D["alt"] else "ARA*")


def k15_birlestir(O: pd.DataFrame, H1: Dict[Tuple[str, int], Dict[str, Any]], H2: Dict[Tuple[str, int], Dict[str, Any]]) -> pd.DataFrame:
    """csv satırlarına iki hakem etiketi + uzlaşı + duyarlılık; eksik sayfa DUR."""
    anah = list(zip(O["set"].astype(str), O["sayfa"].astype(int)))
    if len(set(anah)) != len(anah):
        raise G2Hata("olay csv: (set, sayfa) tekil değil")
    eksik = {ad: [a for a in anah if a not in H] for ad, H in (("K1", H1), ("K2", H2))}
    if any(eksik.values()):
        raise G2Hata(f"hakemde bulunmayan sayfa: {json.dumps({k: [f'{s}:{p}' for s, p in v] for k, v in eksik.items() if v}, ensure_ascii=False)} -> DURDU")
    D = O.copy()
    for ad, H in (("1", H1), ("2", H2)):
        D[f"k{ad}"] = [H[a]["k"] for a in anah]; D[f"puan{ad}"] = [H[a]["puan"] for a in anah]; D[f"gerekce{ad}"] = [H[a]["gerekce"] for a in anah]
    D["uzlasi"] = [k15_uzlasi(a, b) for a, b in zip(D.k1, D.k2)]; D["puan_ort"] = (D.puan1 + D.puan2) / 2.0
    D["duyarlilik"] = [k15_duyar(p) for p in D.puan_ort]
    return D


def k15_kappa(a: List[str], b: List[str], siniflar: Tuple[str, ...] = K15_K) -> Dict[str, Any]:
    a = list(a); b = list(b); n = len(a)
    if n == 0 or n != len(b):
        return {"n": n, "kappa": None, "uyum": None}
    po = sum(x == y for x, y in zip(a, b)) / n; pe = sum((a.count(c) / n) * (b.count(c) / n) for c in siniflar)
    return {"n": n, "uyum": float(po), "beklenen": float(pe), "kappa": None if pe >= 1 else float((po - pe) / (1 - pe)),
            "tablo": {f"{x}|{y}": int(sum(1 for i, j in zip(a, b) if i == x and j == y)) for x in siniflar for y in siniflar}}


def k15_tekrar(A6: List[Dict[str, Any]], O: pd.DataFrame, Hs: Dict[str, Dict[Tuple[str, int], Dict[str, Any]]]) -> Dict[str, Any]:
    """set2 T sayfası <-> set1 bölgesi (zaman + sembol + tarih = bolge_son); her hakemin iki bakışı."""
    s1 = O[O["set"] == "set1"]; ciftler = []
    for r in A6:
        if r.get("katman") != "T":
            continue
        m = s1[(s1.zaman == r["zaman"]) & (s1.sembol == r["sembol"]) & (s1.bolge_son.astype(str) == str(r["tarih"]))]
        if len(m) != 1:
            raise G2Hata(f"tekrar eşlemesi: set2 sayfa {r.get('sayfa')} için set1 bölgesi {len(m)} -> DURDU")
        p1 = int(m.sayfa.iloc[0])
        if "eski_sayfa" in r and int(r["eski_sayfa"]) != p1:
            raise G2Hata(f"tekrar eşlemesi: set2 sayfa {r['sayfa']} eski_sayfa {r['eski_sayfa']} != csv {p1}")
        ciftler.append((int(r["sayfa"]), p1))
    out: Dict[str, Any] = {"ciftler": [{"set2": a, "set1": b} for a, b in ciftler]}
    for ad, H in Hs.items():
        sat = []
        for a, b in ciftler:
            x = H.get(("set2", a)); y = H.get(("set1", b))
            if x is None or y is None:
                raise G2Hata(f"tekrar: {ad} hakeminde set2:{a} ya da set1:{b} yok")
            sat.append({"set2": a, "set1": b, "k_set2": x["k"], "k_set1": y["k"], "puan_set2": x["puan"], "puan_set1": y["puan"]})
        out[ad] = {"satir": sat, "ayni_k": int(sum(s["k_set2"] == s["k_set1"] for s in sat)), "n": len(sat),
                   "puan_fark_mutlak_ort": float(np.mean([abs(s["puan_set2"] - s["puan_set1"]) for s in sat])) if sat else None}
    return out


def k15_sayim(D: pd.DataFrame) -> Dict[str, Any]:
    """GETİRİSİZ sayım: yalnız sinif, zaman, hakem etiketleri, olculdu ve es_neden (eşi var mı) okunur."""
    D = D.copy(); D["_es"] = D.olculdu.astype(bool) & D.es_neden.isna()
    out: Dict[str, Any] = {"toplam": int(len(D)), "uzlasi": D.uzlasi.value_counts().to_dict(), "duyarlilik": D.duyarlilik.value_counts().to_dict(),
                           "k1": D.k1.value_counts().to_dict(), "k2": D.k2.value_counts().to_dict(), "olculdu": int(D.olculdu.astype(bool).sum()), "es_var": int(D._es.sum())}
    for kol in ("uzlasi", "duyarlilik"):
        out[f"sinif_zaman_{kol}"] = {f"{a}|{b}|{c}": int(v) for (a, b, c), v in D.groupby(["sinif", "zaman", kol]).size().items()}
    az: Dict[str, Any] = {}
    gr = {"uzlasi": ("KOPMUS", "BASKI", "KARISIK"), "duyarlilik": ("KOPMUS*", "BASKI*", "ARA*")}
    for aile, sl in K15_EK["aileler"].items():
        for kol, gl in gr.items():
            for z in K15_EK["zaman"]:
                g = D[D.sinif.isin(sl) & ((D.zaman == z) if z != "birlikte" else True)]
                for grp in gl:
                    h = g[g[kol] == grp]; n = int(h.olculdu.astype(bool).sum()); ne = int(h._es.sum())
                    az[f"{aile}|{kol}|{z}|{grp}"] = {"n": n, "n_es": ne, "n_lt2": ne < K15_EK["karsilastirma"]["n_min"]}
    out["grup_n"] = az
    out["karsilastirma_yapilamaz"] = sorted({k.rsplit("|", 1)[0] for k, v in az.items() if v["n_lt2"] and k.rsplit("|", 1)[1] in ("KOPMUS", "BASKI", "KOPMUS*", "BASKI*")})
    return out


def k15_hucre(g: pd.DataFrame) -> Dict[str, Any]:
    o = g[g.olculdu.astype(bool)]; R = o.R15.astype(float); R = R[np.isfinite(R)]; f = o.fark.astype(float); f = f[np.isfinite(f)]
    out: Dict[str, Any] = {"n_bolge": int(len(g)), "n": int(len(R)), "n_es": int(len(f))}
    out.update({"R15_ort": float(R.mean()) if len(R) else None, "R15_med": float(R.median()) if len(R) else None, "arti_pay": float((R > 0).mean()) if len(R) else None,
                "fark_ort": float(f.mean()) if len(f) else None, "fark_med": float(f.median()) if len(f) else None, "esinden_iyi_pay": float((f > 0).mean()) if len(f) else None})
    out["etiket"] = "boş" if not len(R) else K15_EK["etiket"]
    return out


def k15_karsilastir(a: pd.DataFrame, b: pd.DataFrame) -> Dict[str, Any]:
    C = K15_EK["karsilastirma"]; fa = a[a.olculdu.astype(bool)].fark.astype(float).to_numpy(); fb = b[b.olculdu.astype(bool)].fark.astype(float).to_numpy()
    fa = fa[np.isfinite(fa)]; fb = fb[np.isfinite(fb)]
    Ra = a[a.olculdu.astype(bool)].R15.astype(float).to_numpy(); Rb = b[b.olculdu.astype(bool)].R15.astype(float).to_numpy(); Ra = Ra[np.isfinite(Ra)]; Rb = Rb[np.isfinite(Rb)]
    out: Dict[str, Any] = {"n_es_a": int(len(fa)), "n_es_b": int(len(fb)), "n_a": int(len(Ra)), "n_b": int(len(Rb))}
    if len(fa) < C["n_min"] or len(fb) < C["n_min"]:
        out.update({"esli_fark_fark": None, "esli_p": None, "durum": "karşılaştırma yapılamaz"})
    else:
        out.update({"esli_fark_fark": float(fa.mean() - fb.mean()), "esli_p": GZ.gz_perm(fa, fb, C["perm"], C["tohum"]), "durum": "hesaplandı"})
    out["R15_fark_bilgi"] = float(Ra.mean() - Rb.mean()) if len(Ra) and len(Rb) else None
    return out


def k15_tablolar(D: pd.DataFrame) -> Dict[str, Any]:
    gr = {"uzlasi": (("KOPMUS", "BASKI", "KARISIK"), "KOPMUS", "BASKI"), "duyarlilik": (("KOPMUS*", "BASKI*", "ARA*"), "KOPMUS*", "BASKI*")}
    T: Dict[str, Any] = {}
    for aile, sl in K15_EK["aileler"].items():
        for kol, (gl, ka, kb) in gr.items():
            for z in K15_EK["zaman"]:
                g = D[D.sinif.isin(sl)]
                g = g[g.zaman == z] if z != "birlikte" else g
                T[f"{aile}|{kol}|{z}"] = {"hucre": {grp: k15_hucre(g[g[kol] == grp]) for grp in gl}, "fark": k15_karsilastir(g[g[kol] == ka], g[g[kol] == kb])}
    return T


def k15_okuma(T: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for kol, ka in (("uzlasi", "KOPMUS"), ("duyarlilik", "KOPMUS*")):
        ad = {}
        for z in ("haftalik", "gunluk"):
            c = T[f"ANA|{kol}|{z}"]; e = c["hucre"][ka]["fark_ort"]; d = c["fark"]["esli_fark_fark"]
            ad[z] = {"kopmus_esli_ort": e, "kopmus_eksi_baski": d, "saglandi": None if (e is None or d is None) else bool(e > 0 and d > 0)}
        v = [ad[z]["saglandi"] for z in ("haftalik", "gunluk")]
        karar = ("OKUNAMADI (karşılaştırma yapılamaz)" if any(x is None for x in v) else
                 ("AYRIM YÖNÜ CEMAL'İN DEDİĞİ GİBİ" if all(v) else "AYRIM YÖNÜ CEMAL'İN DEDİĞİ GİBİ DEĞİL"))
        out[kol] = {**ad, "karar": karar, "etiket": K15_EK["etiket"]}
    return out


def k15_spearman(D: pd.DataFrame) -> Dict[str, Any]:
    from scipy.stats import spearmanr
    out = {}
    e = D[(D.sinif == "EVET") & D.olculdu.astype(bool)]
    for z in K15_EK["zaman"]:
        g = e if z == "birlikte" else e[e.zaman == z]; g = g[np.isfinite(g.fark.astype(float))]
        if len(g) < 3 or g.puan_ort.nunique() < 2:
            out[z] = {"n": int(len(g)), "rho": None, "p": None}; continue
        r = spearmanr(g.puan_ort.astype(float), g.fark.astype(float))
        out[z] = {"n": int(len(g)), "rho": float(r.statistic), "p_bilgi": float(r.pvalue)}
    return out


def k15_sha_simdi() -> Dict[str, str]:
    return {"KOD15_SHA": MI._mi_sha(G2_YOL["kod"]), "EK15_SHA": k15_ek_sha(), "HAKEM_K1_SHA": MI._mi_sha(K15_YOL["K1"]), "HAKEM_K2_SHA": MI._mi_sha(K15_YOL["K2"]),
            "OLAY13_SHA": MI._mi_sha(K15_YOL["olay13"]), "ANAHTAR6_SHA": MI._mi_sha(K15_YOL["anahtar6"])}


def k15_veri() -> Tuple[pd.DataFrame, Dict[str, Any], Dict[str, Any]]:
    """Getirisiz hazırlık: birleştirme + sayım + kappa + tekrar tutarlılığı."""
    O = pd.read_csv(K15_YOL["olay13"])
    if len(O) != 128:
        raise G2Hata(f"olay csv {len(O)} satır (128 beklenir)")
    H1 = k15_hakem_oku(K15_YOL["K1"]); H2 = k15_hakem_oku(K15_YOL["K2"]); D = k15_birlestir(O, H1, H2)
    ort = sorted(set(H1) & set(H2))
    uyum = {"csv128": k15_kappa(D.k1.tolist(), D.k2.tolist()), "butun_sayfalar_bilgi": k15_kappa([H1[a]["k"] for a in ort], [H2[a]["k"] for a in ort]),
            "uzlasi_dagilim": D.uzlasi.value_counts().to_dict(), "puan_spearman_K1_K2": None}
    try:
        from scipy.stats import spearmanr
        uyum["puan_spearman_K1_K2"] = float(spearmanr(D.puan1, D.puan2).statistic)
    except Exception as ex:   # bilgi satırı; hesap kapısı değil
        g2log.warning("puan spearman hesaplanamadı: %s", ex)
    A6 = json.load(open(K15_YOL["anahtar6"], encoding="utf-8"))["sayfalar"]
    tek = k15_tekrar(A6, O, {"K1": H1, "K2": H2})
    return D, {"sayim": k15_sayim(D), "uyum": uyum, "tekrar": tek}, {"K1": H1, "K2": H2}


def k15_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    yol = _k15_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise G2Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = k15_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise G2Hata(f"ön kayıt 15 kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_G2); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise G2Hata("ön kayıt 15 commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_GOZ2.py", os.path.relpath(K15_YOL["K1"], KOK_G2), os.path.relpath(K15_YOL["K2"], KOK_G2),
                   os.path.relpath(K15_YOL["olay13"], KOK_G2)]):
        raise G2Hata("ön kayıt / kod / hakem / olay çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def k15_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    y = _k15_yol("onkayit", cikti)
    if os.path.exists(y):
        raise G2Hata("ön kayıt 15 zaten var")
    D, G, _ = k15_veri(); sh = k15_sha_simdi(); S = G["sayim"]
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in K15_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_GOZ2.py"])
    sat = ["| Cemal | zaman | KOPMUS | BASKI | KARISIK | KOPMUS* | BASKI* | ARA* |", "|---|---|---|---|---|---|---|---|"]
    for s in ("EVET", "KISMEN", "HAYIR"):
        for z in ("haftalik", "gunluk"):
            g = D[(D.sinif == s) & (D.zaman == z)]
            sat.append(f"| {s} | {z} | " + " | ".join(str(int((g.uzlasi == u).sum())) for u in ("KOPMUS", "BASKI", "KARISIK")) + " | " +
                       " | ".join(str(int((g.duyarlilik == u).sum())) for u in ("KOPMUS*", "BASKI*", "ARA*")) + " |")
    U = G["uyum"]; T = G["tekrar"]
    s = [f"# MUM_IZI15 ÖN KAYIT ({MI._mi_simdi()})", "",
         "MUM_IZI EK 15: kopma ayrımı. mum_izi13_olay.csv satırları AYNEN (R15, es_R15, fark, sinif, zaman); yeni getiri hesabı yok, yalnız gruplama. "
         "Bu dosya gruplama tabloları hesaplanmadan ÖNCE commit edilir; R15 / fark sütunlarına bu aşamada bakılmadı (sayım yalnız sinif, zaman, hakem etiketi, olculdu, es_neden).", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_GOZ2.py commit'i: {kc or 'yok'}", "",
         "## Tanımlar (iş tanımı 2. bölüm aynen; K15_EK, sha yukarıda)", "", "```", json.dumps(K15_EK, ensure_ascii=False, indent=1), "```", "",
         "## Getirisiz sayım: Cemal sınıfı x zaman x uzlaşı / duyarlılık (128 bölge)", "", *sat, "",
         f"- Uzlaşı toplam: {json.dumps(S['uzlasi'], ensure_ascii=False)}; duyarlılık: {json.dumps(S['duyarlilik'], ensure_ascii=False)}",
         f"- K1: {json.dumps(S['k1'], ensure_ascii=False)}; K2: {json.dumps(S['k2'], ensure_ascii=False)}",
         f"- Ölçülen {S['olculdu']} / 128; eşi olan {S['es_var']} (es_neden boş).", "",
         "## Hakem uyumu (getirisiz)", "",
         f"- 128 bölge, üç sınıf: uyum {U['csv128']['uyum']:.3f}, kappa {U['csv128']['kappa']:.3f}; çapraz tablo (K1|K2): {json.dumps(U['csv128']['tablo'], ensure_ascii=False)}",
         f"- Bütün ortak sayfalar (bilgi, n {U['butun_sayfalar_bilgi']['n']}): kappa {U['butun_sayfalar_bilgi']['kappa']:.3f}",
         f"- Puanların Spearman'ı (K1 - K2, 128): {U['puan_spearman_K1_K2']:.3f}" if U["puan_spearman_K1_K2"] is not None else "- Puan Spearman: hesaplanamadı", "",
         "## Hakemin kendi tutarlılığı (set2 tekrar sayfaları = set1 bölgeleri)", "",
         f"- Eşleme: {', '.join(f'set2 s{c['set2']} = set1 s{c['set1']}' for c in T['ciftler'])} (mum_izi6_anahtar.json katman T; eski_sayfa ve csv bolge_son ile denetlendi)",
         *[f"- {h}: aynı k {T[h]['ayni_k']} / {T[h]['n']}; ortalama mutlak puan farkı {T[h]['puan_fark_mutlak_ort']:.2f}" for h in ("K1", "K2")], "",
         "## n < 2 olan karşılaştırmalar ('karşılaştırma yapılamaz' çıkacak)", "",
         *([f"- {k}" for k in S["karsilastirma_yapilamaz"]] or ["- yok"]), "",
         "Grup n'leri (n = ölçülen, n_es = eşi olan):", "", "```", json.dumps(S["grup_n"], ensure_ascii=False, indent=0), "```", "",
         "## Ek BİLGİ satırı (önceden yazılı)", "", "- EVET bölgelerinde iki hakemin ortalama puanı ile eşli fark arasında Spearman korelasyonu (haftalık, günlük, birlikte); karar vermez.", "",
         "## Okuma kuralı (aynen)", "", f"- {K15_EK['okuma']}", f"- Etiket her durumda: {K15_EK['etiket']}. Eşik / gruplama sonuca göre değişmez; değişirse SAPMA.", "",
         "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 15")


def k15_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time()
    if os.path.exists(_k15_yol("sonuc", cikti)):
        raise G2Hata("sonuç 15 zaten var")
    G0 = k15_kapi(cikti); D, G, _ = k15_veri()
    es_kontrol = int((D.olculdu.astype(bool) & D.es_neden.isna()).sum()); es_gercek = int(np.isfinite(D.fark.astype(float)).sum())
    T = k15_tablolar(D)
    J = {"surum": K15_SURUM, "kapi": G0, **G, "es_sayim_denetimi": {"es_neden_bos": es_kontrol, "fark_sonlu": es_gercek, "esit": es_kontrol == es_gercek},
         "tablo": T, "okuma": k15_okuma(T), "bilgi_spearman_evet": k15_spearman(D), "etiket": K15_EK["etiket"], "es_siniri": K15_EK["es_siniri"]}
    kol = list(pd.read_csv(K15_YOL["olay13"], nrows=0).columns) + ["k1", "puan1", "gerekce1", "k2", "puan2", "gerekce2", "uzlasi", "puan_ort", "duyarlilik"]
    D[kol].to_csv(_k15_yol("olay", cikti), index=False, float_format="%.6f")
    J["olay_sha"] = MI._mi_sha(_k15_yol("olay", cikti)); J["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_k15_yol("sonuc", cikti), J, "sonuç 15")
    return J


# ================================================================ 4c) MUM_IZI EK 16: ÖLÇEK (sayfadaki mum boyu / gerçek mum boyu; yeni getiri hesabı yok)
K16_SURUM = "MUM_IZI_GOZ2 olcek v1.0 (2026-11-26): EK 16 ölçek; mum_izi13_olay.csv 128 bölge; ölçüler yalnız bölge ve öncesi barlardan; sonrası csv aynen"
K16_DOSYA = {"onkayit": "MUM_IZI16_ON_KAYIT.md", "rapor": "MUM_IZI16_RAPOR.md", "sonuc": "mum_izi16_sonuc.json", "olay": "mum_izi16_olay.csv"}
K16_YOL = {"olay13": os.path.join(_C, "mum_izi13_olay.csv"), "sonrasi13": os.path.join(_C, "MUM_IZI13_SONRASI.pdf"), "anahtar8": os.path.join(_C, "mum_izi8_onay_anahtar.json")}
K16_GETIRISIZ = ["set", "set_ad", "sayfa", "isaret", "sinif", "sinif_son", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "m", "olculdu", "neden", "es_neden"]
K16_OLCU = ["BOY_MUTLAK", "BOY_OZ", "SON_BOY_OZ", "BOY_BANT", "BOY_SAYFA", "SISME"]
K16_AILE_OLCU = ["BOY_OZ", "BOY_MUTLAK", "SON_BOY_OZ", "BOY_BANT", "BOY_SAYFA"]          # A2 ailesi: 5 ölçü (SISME yalnız A1 olgusu)
K16_ANA = "BOY_OZ"
K16_EK: Dict[str, Any] = {
    "surum": "K16-1.0", "kaynak": "mum_izi13_olay.csv (128 bölge); A1 ve grup sayımı yalnız getirisiz sütunlarla (usecols: K16_GETIRISIZ); R15 / es_R15 / fark ön kayıt "
                                  "commit'inden SONRA okunur (aynen; yeni getiri hesabı yok)",
    "veri": "bölge barları mumun kendi zaman diliminde: günlük MV.mv_veri('gunluk') (açık kopya), haftalık MV.mv_veri('haftalik') (MH tam -> ISO hafta); onay "
            "sayfalarının kullandığı yol; bölge = bolge_son barında biten m bar; bolge_bas csv ile denetlenir (uyuşmazsa DUR)",
    "olcu": {
        "r": "r = (H - L) / C (her bar)",
        "BOY_MUTLAK": "bölge barlarında r medyanı x 100 (%)",
        "BOY_OZ": "ANA ÖLÇÜ: bölge r medyanı / bölgeden hemen önceki en çok 120 barın r medyanı; önceki sonlu bar < 40 ise boş (NaN). < 1: hisse kendi olağanından sakin",
        "SON_BOY_OZ": "bölgenin son ceil(m / 3) barının r medyanı / aynı payda (BOY_OZ paydası)",
        "BOY_BANT": "bölge barlarında (H - L) / (BU - BA) medyanı; Bollinger 20, 2 sigma (MI.mi_bant: yalnız o güne kadarki kapanışlar); bant genişliği sonlu ve > 0 barlar",
        "BOY_SAYFA": "bölge barlarında (H - L) medyanı / onay sayfasındaki büyük grafiğin dikey açıklığı (y1 - y0). y sınırları sayfayı çizen fonksiyonla aynı yoldan "
                     "yeniden üretilir: pencere = bölgeden önceki 15 bar + bölge (bölge sonunda kesik), MV._mv_ciz (mumlar + Bollinger 20 + SMA20 + bölge kutusu; "
                     "matplotlib otomatik ölçek); set3 (MUM_IZI8_ONAY, V5.v5_onay) ayrıca V5._v5_okuma_ciz (y = [lo - 0,2 (hi - lo), hi + 0,05 (hi - lo)], "
                     "kutusuz); set1 MV.mv_onay, set2 ETIKET2, set4 / set5 HAKEM._hk_sayfa (kutulu) aynı MV._mv_ciz yolu",
        "SISME": "sayfanın dikey açıklığı / bölgenin (en yüksek H - en düşük L) açıklığı",
        "gelecek": "her bölgenin dizileri bolge_son barında KESİLİR (o bar dahil) ve ölçü yalnız bu kesik diziden hesaplanır; sonraki bar kullanılmaz (assert + test)"},
    "A1": {"spearman": "128 bölgede BOY_SAYFA ile BOY_MUTLAK ve BOY_OZ (iki değer sonlu olanlar); zaman dilimi ayrı satır bilgi",
           "terciller": "'sayfada küçük ama kendi geçmişine göre büyük' = BOY_SAYFA <= 128 bölgenin 1/3 dilimi (np.quantile, doğrusal) VE BOY_OZ >= 2/3 dilimi",
           "sinif": "EVET / KISMEN / HAYIR x günlük / haftalık (+ birlikte): n ve 6 ölçünün medyanı; EVET - HAYIR medyan farkı + Mann-Whitney U (iki yönlü, scipy varsayılan "
                    "yöntem)",
           "notlu": {"pdf": "MUM_IZI13_SONRASI.pdf", "fiziksel_sayfa": [4, 5, 7, 8, 9, 10, 11, 12, 13, 14],
                     "eslesme": "sayfa başlığı (sınıf · sembol (pazar) · zaman · bölge bas .. son) pypdf ile okunur; csv set5 satırına sembol + zaman + bölge başı + sonu ile "
                                "BİREBİR (tek satır) eşlenir; değilse DUR"}},
    "A2": {"gruplar": {"EVET": ["EVET"], "EVET+KISMEN": ["EVET", "KISMEN"], "HEPSI": ["EVET", "KISMEN", "HAYIR"]}, "zaman": ["gunluk", "haftalik"],
           "aile": "5 ölçü (BOY_OZ, BOY_MUTLAK, SON_BOY_OZ, BOY_BANT, BOY_SAYFA) x 2 zaman dilimi; SISME A2'ye girmez (sayfa özelliği, mum boyu değil)",
           "spearman": "ölçü ile eşli fark (fark sütunu) arasında Spearman (olculdu, fark ve ölçü sonlu; n < 3 -> boş)",
           "bolme": "grup x zaman dilimi içinde ölçünün (sonlu değerler) medyanı; KÜÇÜK = ölçü <= medyan, BÜYÜK = ölçü > medyan; ölçüsü boş bölge yarıya girmez",
           "hucre": "her yarı: n (ölçülen), n_es, R15 ort / medyan, artıda payı (R15 > 0), eşli fark ort / medyan, eşinden iyi payı (fark > 0) (k15_hucre aynen)",
           "fark": "KÜÇÜK - BÜYÜK eşli fark ortalaması farkı; p = etiket permütasyonu GZ.gz_perm, iki yönlü, 10.000, tohum 16 (her karşılaştırmada aynı); bir yarıda "
                   "n_es < 2 -> 'karşılaştırma yapılamaz'", "perm": 10000, "tohum": 16, "n_min": 2,
           "bh": "aile içi (5 ölçü x 2 zaman) Benjamini-Hochberg düzeltilmiş p, yalnız bilgi"},
    "okuma": "'YÖN CEMAL'İN DEDİĞİ GİBİ' <=> ANA ÖLÇÜDE (BOY_OZ) EVET bölgelerinde KÜÇÜK yarının eşli fark ortalaması > BÜYÜK yarının, günlükte VE haftalıkta; biri "
             "hesaplanamazsa 'OKUNAMADI'; öteki ölçüler bilgi (çoklu karşılaştırma)",
    "etiket": "BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK",
    "sinir": "Cemal sonrasını gördü ve gerçek grafiğe yalnız gitmeyenlerde baktı -> sonrası tablosu GERİYE DÖNÜK; eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240)",
}
K16_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eşli fark mum_izi13_olay.csv'den aynen (aynı giriş günü aynı kova CETVEL2 konum eşi); yeni eş yok; sınır: eşler bölgenin kendi koşusuyla eşlenmedi"),
    "K2": ("EVET", "ölçüler bolge_son barında kesilmiş diziden (k16_olcu_bir / k16_sayfa_ylim; assert + sentetik test: sonraki barlar değişince ölçü aynı); 120 bar öncesi "
                   "penceresi bölgeyi içermez; A1 / grup sayımı getirisiz sütunlarla (usecols); SINIR: ölçüt Cemal sonrasını gördükten sonra söylendi -> GERİYE DÖNÜK"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0); haftalık tamamlanmış ISO haftaları (MH); r = (H - L) / C sonlu barlar"),
    "K4": ("EVET", "128 tekil bölge (csv; (set, sayfa) ve (zaman, sembol, bolge_son) tekilliği denetlenir)"),
    "K5": ("EVET", "giriş = bölgeden sonraki ilk geçerli barın açılışı (MUM_IZI11 tanımı, csv aynen); bu iş giriş hesaplamaz"),
    "K6": ("EVET", "ölçüler birimsiz oran ((H - L) / C, bant ve sayfa oranları); bölünme düzeltmeli MI fiyatları; getiriler csv aynen"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz"),
    "K8": ("EVET", "bütün yarılar n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK'; tek dönem (<= 2022); aile içi BH bilgi; karar yok"),
    "K9": ("EVET", "bu ön kayıt (KOD16 / EK16 / olay13 / pdf / anahtar sha + A1 olgu tabloları + grup sayıları) sonrası okunmadan ÖNCE commit; k16_kapi sha + commit + temiz "
                   "ağaç denetler"),
    "K10": ("EVET", "notlu on sayfa pdf başlığından ayrıştırılır ve csv ile birebir eşlenir (DUR); bölge başı veriden yeniden hesaplanıp csv ile denetlenir; set3 'k' "
                    "anahtardan sayfa + sembol + tarih denetimiyle"),
    "K11": ("EVET", "rapor öncesi >= 2 hücre olay csv'sinden bağımsız pandas koduyla yeniden üretilir; BOY_MUTLAK / BOY_OZ iki bölgede düz döngüyle yeniden hesaplanır"),
    "K12": ("EVET", "'iz / tuttu / anlamlı' sözü yok; sayı ile yorum ayrı; okuma kuralı yalnız yön"),
    "K13": ("EVET", "çakışma kapısı korunur; çalışan komutlar değişmez (test); yasak defter dosyalarına ve MUM_IZI_HAKEM.py'ye dokunulmaz; yalnız kendi yolları commit; "
                    "sızıntı taraması MI._mi_yaz"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez"),
}


def _k16_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or G2_YOL["cikti"], K16_DOSYA[ad])


def k16_ek_sha() -> str:
    return hashlib.sha256(json.dumps(K16_EK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def k16_olcu_bir(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, m: int, ylim: Optional[Tuple[float, float]]) -> Dict[str, Any]:
    """Diziler bölgenin son barında BİTER (son eleman = bolge_son). Bölge = son m bar; öncesi = bölgeden hemen önceki en çok 120 bar."""
    O, H, L, C = (np.asarray(x, float) for x in (O, H, L, C)); T = len(C); m = int(m); s = T - m
    if not (len(O) == len(H) == len(L) == T) or m < 1 or s < 0:
        raise G2Hata(f"k16: dizi / pencere uyumsuz (T {T}, m {m})")
    with np.errstate(all="ignore"):
        r = (H - L) / C
    bol = r[s:]; bol = bol[np.isfinite(bol)]
    on = r[max(0, s - 120):s]; on = on[np.isfinite(on)]
    assert max(0, s - 120) + len(r[max(0, s - 120):s]) == s, "öncesi penceresi bölgeye taşıyor"
    bm = float(np.median(bol)) if len(bol) else np.nan
    pay = float(np.median(on)) if len(on) >= 40 else np.nan
    n3 = int(np.ceil(m / 3.0)); sn = r[T - n3:]; sn = sn[np.isfinite(sn)]
    BU, _, BA = MI.mi_bant(C); w = (BU - BA)[s:]; hb = (H - L)[s:]
    ok = np.isfinite(w) & (w > 0) & np.isfinite(hb)
    out: Dict[str, Any] = {"BOY_MUTLAK": 100.0 * bm, "BOY_OZ": bm / pay if np.isfinite(pay) and pay > 0 else np.nan,
                           "SON_BOY_OZ": (float(np.median(sn)) / pay) if len(sn) and np.isfinite(pay) and pay > 0 else np.nan,
                           "BOY_BANT": float(np.median(hb[ok] / w[ok])) if ok.any() else np.nan, "n_once": int(len(on)), "n_son": n3}
    if ylim is not None:
        sp = float(ylim[1]) - float(ylim[0]); ar = float(np.nanmax(H[s:]) - np.nanmin(L[s:]))
        out["BOY_SAYFA"] = float(np.nanmedian(hb)) / sp if sp > 0 else np.nan; out["SISME"] = sp / ar if ar > 0 else np.nan
        out["y0"], out["y1"] = float(ylim[0]), float(ylim[1])
    else:
        out["BOY_SAYFA"] = out["SISME"] = out["y0"] = out["y1"] = np.nan
    return out


def k16_sayfa_ylim(st: str, O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, m: int, k: Optional[int] = None) -> Tuple[float, float]:
    """Onay sayfasının büyük grafiğindeki y sınırları (diziler bölge sonunda biter). Çizim fonksiyonları aynen çağrılır (MV._mv_ciz; set3 ayrıca V5._v5_okuma_ciz)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    O, H, L, C = (np.asarray(x, float) for x in (O, H, L, C)); T = len(C); t = T - 1; m = int(m)
    once = int(MV.MV_ESIK["onay"]["once"]); i0 = max(0, t - m + 1 - once); BU, BO, BA = MI.mi_bant(C); sl = slice(i0, T)
    fig = plt.figure(figsize=(8.3, 11.7))
    try:
        if st == "set3":
            import MUM_IZI_V5 as V5
            if k is None:
                raise G2Hata("k16: set3 için 'k' gerekli")
            ax = fig.add_axes([0.34, 0.42, 0.63, 0.5])
            MV._mv_ciz(ax, O[sl], H[sl], L[sl], C[sl], BU[sl], BO[sl], BA[sl], None, "x")
            V5._v5_okuma_ciz(ax, t - m + 1 - i0, int(k), m, L[sl], H[sl])
        else:
            ax = fig.add_axes([0.38, 0.45, 0.58, 0.45])
            MV._mv_ciz(ax, O[sl], H[sl], L[sl], C[sl], BU[sl], BO[sl], BA[sl], (t - m + 1 - i0, t - i0), "x")
        y0, y1 = ax.get_ylim()
    finally:
        plt.close(fig)
    return float(y0), float(y1)


def k16_bolge_dizi(d: pd.DataFrame, r: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Bölge sonunda KESİLMİŞ OHLC; bolge_bas csv ile denetlenir."""
    try:
        t = d.index.get_loc(pd.Timestamp(r["bolge_son"]))
    except KeyError as ex:
        raise G2Hata(f"k16: {r['set']} s{r['sayfa']} bolge_son veride yok") from ex
    if not isinstance(t, (int, np.integer)):
        raise G2Hata(f"k16: {r['set']} s{r['sayfa']} bolge_son tekil değil")
    m = int(r["m"]); s = t - m + 1
    if s < 0:
        raise G2Hata(f"k16: {r['set']} s{r['sayfa']} pencere verinin başından taşıyor")
    bas = d.bas.iloc[s] if r["zaman"] == "haftalik" else d.index[s]
    if str(pd.Timestamp(bas).date()) != str(r["bolge_bas"]):
        raise G2Hata(f"k16: {r['set']} s{r['sayfa']} bölge başı csv ile uyuşmuyor ({pd.Timestamp(bas).date()} / {r['bolge_bas']})")
    x = d.iloc[:t + 1]
    assert pd.Timestamp(x.index[-1]) == pd.Timestamp(r["bolge_son"]), "dizi bölge sonunda bitmiyor"
    return tuple(x[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))  # type: ignore[return-value]


def k16_set3_k() -> Dict[int, Tuple[int, str, str]]:
    A = json.load(open(K16_YOL["anahtar8"], encoding="utf-8"))["sayfalar"]
    return {int(a["sayfa"]): (int(a["k"]), str(a["sembol"]), str(a["tarih"])) for a in A}


def k16_veri() -> pd.DataFrame:
    """GETİRİSİZ: csv'nin yalnız K16_GETIRISIZ sütunları + ölçüler (veri yükleyerek)."""
    import gc
    O = pd.read_csv(K16_YOL["olay13"], usecols=K16_GETIRISIZ)
    if len(O) != 128 or O.duplicated(["set", "sayfa"]).any() or O.duplicated(["zaman", "sembol", "bolge_son"]).any():
        raise G2Hata("k16: olay csv 128 tekil bölge değil")
    K8 = k16_set3_k(); rows: Dict[int, Dict[str, Any]] = {}
    for (z, pz), g in O.groupby(["zaman", "pazar"]):
        V = MV.mv_veri(z, pz)
        for i, r in g.iterrows():
            r = r.to_dict()
            if r["sembol"] not in V:
                raise G2Hata(f"k16: {r['sembol']} {z} {pz} veride yok")
            Od, Hd, Ld, Cd = k16_bolge_dizi(V[r["sembol"]], r); k = None
            if r["set"] == "set3":
                kk = K8.get(int(r["sayfa"]))
                if kk is None or kk[1] != r["sembol"] or kk[2] != str(r["bolge_son"]):
                    raise G2Hata(f"k16: set3 s{r['sayfa']} anahtar 8 ile eşleşmiyor")
                k = kk[0]
            rows[i] = k16_olcu_bir(Od, Hd, Ld, Cd, int(r["m"]), k16_sayfa_ylim(r["set"], Od, Hd, Ld, Cd, int(r["m"]), k))
        del V; gc.collect()
        g2log.info("ölçek: %s %s %d bölge", z, pz, len(g))
    M = pd.DataFrame.from_dict(rows, orient="index").sort_index()
    return pd.concat([O, M], axis=1)


def k16_notlu(D: pd.DataFrame) -> pd.DataFrame:
    """MUM_IZI13_SONRASI fiziksel sayfa 4, 5, 7-14 başlıkları -> csv set5 satırı (birebir)."""
    import re
    from pypdf import PdfReader
    P = PdfReader(K16_YOL["sonrasi13"]); sat = []
    for p in K16_EK["A1"]["notlu"]["fiziksel_sayfa"]:
        tx = P.pages[p - 1].extract_text() or ""
        mm = re.search(r"(BENZİYOR|KISMEN|BENZEMİYOR) · (\S+) \((\w+)\) · (haftalık|günlük) · bölge (\d{4}-\d\d-\d\d) \.\. (\d{4}-\d\d-\d\d)", tx)
        if not mm:
            raise G2Hata(f"k16: SONRASI sayfa {p} başlığı okunamadı")
        z = "haftalik" if mm.group(4) == "haftalık" else "gunluk"
        h = D[(D["set"] == "set5") & (D.sembol == mm.group(2)) & (D.zaman == z) & (D.bolge_bas.astype(str) == mm.group(5)) & (D.bolge_son.astype(str) == mm.group(6))]
        if len(h) != 1:
            raise G2Hata(f"k16: SONRASI sayfa {p} csv ile {len(h)} satır eşleşti")
        x = h.iloc[0].to_dict(); x["fiziksel_sayfa"] = p; x["pdf_sinif"] = mm.group(1); sat.append(x)
    return pd.DataFrame(sat)


def _k16_ms(x: pd.Series) -> Optional[float]:
    x = pd.to_numeric(x, errors="coerce"); x = x[np.isfinite(x)]
    return float(x.median()) if len(x) else None


def k16_a1(D: pd.DataFrame) -> Dict[str, Any]:
    from scipy.stats import mannwhitneyu, spearmanr
    out: Dict[str, Any] = {"spearman": {}, "sinif": {}, "evet_hayir": {}}
    for z in ("birlikte", "gunluk", "haftalik"):
        g = D if z == "birlikte" else D[D.zaman == z]
        for b in ("BOY_MUTLAK", "BOY_OZ"):
            h = g[np.isfinite(g.BOY_SAYFA) & np.isfinite(g[b])]
            rr = spearmanr(h.BOY_SAYFA, h[b]) if len(h) >= 3 else None
            out["spearman"][f"BOY_SAYFA~{b}|{z}"] = {"n": int(len(h)), "rho": float(rr.statistic) if rr else None, "p_bilgi": float(rr.pvalue) if rr else None}
    h = D[np.isfinite(D.BOY_SAYFA) & np.isfinite(D.BOY_OZ)]; qs = float(np.quantile(h.BOY_SAYFA, 1 / 3)); qo = float(np.quantile(h.BOY_OZ, 2 / 3))
    km = h[(h.BOY_SAYFA <= qs) & (h.BOY_OZ >= qo)]
    out["kucuk_ama_buyuk"] = {"n_iki_olcu": int(len(h)), "BOY_SAYFA_q1_3": qs, "BOY_OZ_q2_3": qo, "sayi": int(len(km)),
                              "sinif_zaman": {f"{a}|{b}": int(v) for (a, b), v in km.groupby(["sinif", "zaman"]).size().items()},
                              "bolgeler": [f"{r.set} s{r.sayfa}" for r in km.itertuples()]}
    for s in ("EVET", "KISMEN", "HAYIR"):
        for z in ("gunluk", "haftalik", "birlikte"):
            g = D[(D.sinif == s) & ((D.zaman == z) if z != "birlikte" else True)]
            out["sinif"][f"{s}|{z}"] = {"n": int(len(g)), **{o: _k16_ms(g[o]) for o in K16_OLCU}}
    for z in ("gunluk", "haftalik", "birlikte"):
        for o in K16_OLCU:
            a = D[(D.sinif == "EVET") & ((D.zaman == z) if z != "birlikte" else True)][o].astype(float); b = D[(D.sinif == "HAYIR") & ((D.zaman == z) if z != "birlikte" else True)][o].astype(float)
            a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
            p = float(mannwhitneyu(a, b, alternative="two-sided").pvalue) if len(a) and len(b) else None
            out["evet_hayir"][f"{o}|{z}"] = {"n_evet": int(len(a)), "n_hayir": int(len(b)), "med_evet": _k16_ms(a), "med_hayir": _k16_ms(b),
                                             "med_fark": (float(a.median() - b.median()) if len(a) and len(b) else None), "mw_p": p}
    out["bos"] = {o: int((~np.isfinite(D[o].astype(float))).sum()) for o in K16_OLCU}
    return out


def k16_yari(x: pd.Series) -> pd.Series:
    x = x.astype(float); f = x[np.isfinite(x)]
    if not len(f):
        return pd.Series([None] * len(x), index=x.index, dtype=object)
    med = float(f.median())
    return pd.Series(np.where(~np.isfinite(x), None, np.where(x <= med, "KUCUK", "BUYUK")), index=x.index, dtype=object)


def k16_grup_n(D: pd.DataFrame) -> Dict[str, Any]:
    """GETİRİSİZ: her grup x ölçü x zaman için medyan ve yarıların n'i (n_olculdu, n_es = olculdu ve es_neden boş)."""
    out: Dict[str, Any] = {}
    for ga, sl in K16_EK["A2"]["gruplar"].items():
        for o in K16_AILE_OLCU:
            for z in K16_EK["A2"]["zaman"]:
                g = D[D.sinif.isin(sl) & (D.zaman == z)]; lab = k16_yari(g[o]); x = g[o].astype(float); x = x[np.isfinite(x)]
                c: Dict[str, Any] = {"n_bolge": int(len(g)), "n_olcu": int(len(x)), "medyan": float(x.median()) if len(x) else None}
                for y in ("KUCUK", "BUYUK"):
                    h = g[lab == y]; c[y] = {"n": int(h.olculdu.astype(bool).sum()), "n_es": int((h.olculdu.astype(bool) & h.es_neden.isna()).sum())}
                out[f"{ga}|{o}|{z}"] = c
    return out


def _k16_bh(p: List[Optional[float]]) -> List[Optional[float]]:
    ix = [i for i, v in enumerate(p) if v is not None]; v = np.array([p[i] for i in ix], float); out: List[Optional[float]] = [None] * len(p)
    if not len(v):
        return out
    o = np.argsort(v); n = len(v); q = v[o] * n / (np.arange(n) + 1); q = np.minimum.accumulate(q[::-1])[::-1]; q = np.minimum(q, 1.0)
    for j, k in enumerate(o):
        out[ix[k]] = float(q[j])
    return out


def k16_a2(D: pd.DataFrame) -> Dict[str, Any]:
    from scipy.stats import spearmanr
    A = K16_EK["A2"]; T: Dict[str, Any] = {}
    for ga, sl in A["gruplar"].items():
        for o in K16_AILE_OLCU:
            for z in A["zaman"]:
                g = D[D.sinif.isin(sl) & (D.zaman == z)]; lab = k16_yari(g[o]); K = g[lab == "KUCUK"]; B = g[lab == "BUYUK"]
                fa = K[K.olculdu.astype(bool)].fark.astype(float).to_numpy(); fb = B[B.olculdu.astype(bool)].fark.astype(float).to_numpy()
                fa = fa[np.isfinite(fa)]; fb = fb[np.isfinite(fb)]
                c: Dict[str, Any] = {"KUCUK": k15_hucre(K), "BUYUK": k15_hucre(B), "medyan": _k16_ms(g[o])}
                if len(fa) < A["n_min"] or len(fb) < A["n_min"]:
                    c["fark"] = {"esli_fark_fark": None, "p": None, "durum": "karşılaştırma yapılamaz"}
                else:
                    c["fark"] = {"esli_fark_fark": float(fa.mean() - fb.mean()), "p": GZ.gz_perm(fa, fb, A["perm"], A["tohum"]), "durum": "hesaplandı"}
                h = g[g.olculdu.astype(bool) & np.isfinite(g.fark.astype(float)) & np.isfinite(g[o].astype(float))]
                if len(h) >= 3 and h[o].nunique() > 1:
                    rr = spearmanr(h[o].astype(float), h.fark.astype(float)); c["spearman"] = {"n": int(len(h)), "rho": float(rr.statistic), "p": float(rr.pvalue)}
                else:
                    c["spearman"] = {"n": int(len(h)), "rho": None, "p": None}
                T[f"{ga}|{o}|{z}"] = c
        ks = [f"{ga}|{o}|{z}" for o in K16_AILE_OLCU for z in A["zaman"]]
        for k, q in zip(ks, _k16_bh([T[k]["fark"]["p"] for k in ks])):
            T[k]["fark"]["p_bh_bilgi"] = q
    return T


def k16_okuma(T: Dict[str, Any]) -> Dict[str, Any]:
    ad: Dict[str, Any] = {}
    for z in ("gunluk", "haftalik"):
        c = T[f"EVET|{K16_ANA}|{z}"]; a = c["KUCUK"]["fark_ort"]; b = c["BUYUK"]["fark_ort"]
        ok = c["fark"]["durum"] == "hesaplandı" and a is not None and b is not None
        ad[z] = {"kucuk_esli_ort": a, "buyuk_esli_ort": b, "saglandi": bool(a > b) if ok else None}
    v = [ad[z]["saglandi"] for z in ("gunluk", "haftalik")]
    karar = "OKUNAMADI" if any(x is None for x in v) else ("YÖN CEMAL'İN DEDİĞİ GİBİ" if all(v) else "YÖN CEMAL'İN DEDİĞİ GİBİ DEĞİL")
    return {**ad, "karar": karar, "etiket": K16_EK["etiket"]}


def k16_sha_simdi() -> Dict[str, str]:
    import MUM_IZI_V5 as V5
    return {"KOD16_SHA": MI._mi_sha(G2_YOL["kod"]), "EK16_SHA": k16_ek_sha(), "OLAY13_SHA": MI._mi_sha(K16_YOL["olay13"]), "SONRASI13_PDF_SHA": MI._mi_sha(K16_YOL["sonrasi13"]),
            "ANAHTAR8_SHA": MI._mi_sha(K16_YOL["anahtar8"]), "MV_KOD_SHA": MI._mi_sha(MV.MV_YOL["kod"]), "MI_KOD_SHA": MI._mi_sha(MI.MI_YOL["kod"]),
            "V5_KOD_SHA": MI._mi_sha(V5.__file__)}


def k16_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    yol = _k16_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise G2Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = k16_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise G2Hata(f"ön kayıt 16 kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_G2); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise G2Hata("ön kayıt 16 commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_GOZ2.py", os.path.relpath(K16_YOL["olay13"], KOK_G2)]):
        raise G2Hata("ön kayıt / kod / olay çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def _k16_f(x: Any, n: int = 3) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{n}f}".replace(".", ",")


def k16_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    y = _k16_yol("onkayit", cikti)
    if os.path.exists(y):
        raise G2Hata("ön kayıt 16 zaten var")
    D = k16_veri(); A1 = k16_a1(D); GN = k16_grup_n(D); N = k16_notlu(D); sh = k16_sha_simdi()
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in K16_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_GOZ2.py"])
    sp = ["| ilişki | zaman | n | Spearman rho | p (bilgi) |", "|---|---|---|---|---|"] + [
        f"| {k.split('|')[0]} | {k.split('|')[1]} | {v['n']} | {_k16_f(v['rho'])} | {_k16_f(v['p_bilgi'], 4)} |" for k, v in A1["spearman"].items()]
    km = A1["kucuk_ama_buyuk"]
    sn = ["| sınıf | zaman | n | " + " | ".join(K16_OLCU) + " |", "|---|---|---|" + "---|" * len(K16_OLCU)] + [
        f"| {k.split('|')[0]} | {k.split('|')[1]} | {v['n']} | " + " | ".join(_k16_f(v[o]) for o in K16_OLCU) + " |" for k, v in A1["sinif"].items()]
    eh = ["| ölçü | zaman | n EVET | n HAYIR | medyan EVET | medyan HAYIR | fark | Mann-Whitney p |", "|---|---|---|---|---|---|---|---|"] + [
        f"| {k.split('|')[0]} | {k.split('|')[1]} | {v['n_evet']} | {v['n_hayir']} | {_k16_f(v['med_evet'])} | {_k16_f(v['med_hayir'])} | {_k16_f(v['med_fark'])} | "
        f"{_k16_f(v['mw_p'], 4)} |" for k, v in A1["evet_hayir"].items()]
    nt = ["| fiziksel sayfa | sınıf | sembol | zaman | bölge | BOY_MUTLAK % | BOY_OZ | SON_BOY_OZ | BOY_BANT | BOY_SAYFA | SISME |", "|---|---|---|---|---|---|---|---|---|---|---|"] + [
        f"| {r.fiziksel_sayfa} | {r.sinif} | {r.sembol} | {r.zaman} | {r.bolge_bas} .. {r.bolge_son} | {_k16_f(r.BOY_MUTLAK, 2)} | {_k16_f(r.BOY_OZ, 2)} | "
        f"{_k16_f(r.SON_BOY_OZ, 2)} | {_k16_f(r.BOY_BANT, 2)} | {_k16_f(r.BOY_SAYFA, 3)} | {_k16_f(r.SISME, 2)} |" for r in N.itertuples()]
    gn = ["| grup | ölçü | zaman | n bölge | medyan | KÜÇÜK n / n_es | BÜYÜK n / n_es |", "|---|---|---|---|---|---|---|"] + [
        f"| {k.split('|')[0]} | {k.split('|')[1]} | {k.split('|')[2]} | {v['n_bolge']} | {_k16_f(v['medyan'])} | {v['KUCUK']['n']} / {v['KUCUK']['n_es']} | "
        f"{v['BUYUK']['n']} / {v['BUYUK']['n_es']} |" for k, v in GN.items()]
    s = [f"# MUM_IZI16 ÖN KAYIT ({MI._mi_simdi()})", "",
         "MUM_IZI EK 16 İŞ A: ölçek. Ölçüler yalnız bölge ve öncesi barlarından; mum_izi13_olay.csv'nin getiri sütunlarına (R15, es_R15, fark, ...) bu aşamada BAKILMADI "
         "(csv yalnız getirisiz sütunlarla okundu: " + ", ".join(K16_GETIRISIZ) + "). Bu dosya sonrası tabloları hesaplanmadan ÖNCE commit edilir.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_GOZ2.py commit'i: {kc or 'yok'}", "",
         "## Tanımlar (iş tanımı 1. bölüm; K16_EK, sha yukarıda)", "", "```", json.dumps(K16_EK, ensure_ascii=False, indent=1), "```", "",
         "Yorum notu (ön kayıt anında): iş tanımı A2 ailesini '5 ölçü x 2 zaman dilimi' diye sayar; altı ölçüden SISME (sayfa açıklığı / bölge açıklığı: bir sayfa özelliği, "
         "mum boyu değil) A2 dışında tutuldu, A1'de olgu olarak raporlanır.", "",
         "## A1 OLGU (getirisiz)", "", "### Spearman (BOY_SAYFA ile gerçek boy)", "", *sp, "",
         f"### 'Sayfada küçük ama kendi geçmişine göre büyük'", "",
         f"- İki ölçüsü de dolu {km['n_iki_olcu']} bölge; BOY_SAYFA 1/3 dilimi {_k16_f(km['BOY_SAYFA_q1_3'], 4)}, BOY_OZ 2/3 dilimi {_k16_f(km['BOY_OZ_q2_3'], 3)}: "
         f"**{km['sayi']} bölge** ({json.dumps(km['sinif_zaman'], ensure_ascii=False)}).", "",
         "### Cemal sınıfına göre ölçü medyanları", "", *sn, "", "### EVET - HAYIR (Mann-Whitney U, iki yönlü)", "", *eh, "",
         f"- Boş ölçü sayısı (128'de): {json.dumps(A1['bos'], ensure_ascii=False)}", "",
         "### Cemal'in not yazdığı on bölge (MUM_IZI13_SONRASI fiziksel sayfa 4, 5, 7-14; getiri bu tabloda yok)", "", *nt, "",
         "## A2 grupları: getirisiz sayım (yarıların n'i; n = ölçülen, n_es = eşi olan)", "", *gn, "",
         "## Okuma kuralı (aynen)", "", f"- {K16_EK['okuma']}", f"- Etiket her durumda: {K16_EK['etiket']}. Grup / eşik / ana ölçü sonuca göre değişmez; değişirse SAPMA.", "",
         "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 16")


def k16_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    t0 = time.time()
    if os.path.exists(_k16_yol("sonuc", cikti)):
        raise G2Hata("sonuç 16 zaten var")
    G0 = k16_kapi(cikti)
    kasa = KS.kasa_kapisi([os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] +
                          [os.path.join(MV.MV_YOL["haftalik"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")], "2022-12-31")
    D = k16_veri(); A1 = k16_a1(D); GN = k16_grup_n(D); N = k16_notlu(D)
    G = pd.read_csv(K16_YOL["olay13"])                     # getiri sütunları: kapıdan SONRA
    ek = [c for c in G.columns if c not in K16_GETIRISIZ]; DD = D.merge(G[["set", "sayfa"] + ek], on=["set", "sayfa"], how="left", validate="one_to_one")
    if len(DD) != 128:
        raise G2Hata("k16: birleştirme 128 satır değil")
    T = k16_a2(DD); R = k16_okuma(T)
    kol = list(G.columns) + ["n_once", "n_son"] + K16_OLCU + ["y0", "y1"]
    DD[kol].to_csv(_k16_yol("olay", cikti), index=False, float_format="%.6f")
    Nr = N.merge(G[["set", "sayfa", "R15", "es_R15", "fark", "olculdu"]], on=["set", "sayfa"], how="left")
    J = {"surum": K16_SURUM, "kapi": G0, "kasa": kasa, "A1": A1, "grup_n": GN,
         "notlu": [{k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in r.items() if k in
                    ["fiziksel_sayfa", "pdf_sinif", "set", "sayfa", "sinif", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "m", "R15", "es_R15", "fark"] + K16_OLCU}
                   for r in Nr.to_dict("records")],
         "A2": T, "okuma": R, "etiket": K16_EK["etiket"], "sinir": K16_EK["sinir"], "olay_sha": MI._mi_sha(_k16_yol("olay", cikti)), "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_k16_yol("sonuc", cikti), J, "sonuç 16")
    return J


# ================================================================ 4d) MUM_IZI EK 17: ÜÇÜNCÜ BAKIŞ (set 6 = MUM_IZI14 ölçekli onay seti, 17 bölge) + BİRLEŞİK set 1-6
K17_SURUM = "MUM_IZI_GOZ2 set6 v1.0 (2026-11-26): EK 17 göz ölçümü üçüncü bakış (set 6) + birleşik 145; tanımlar MUM_IZI_GOZ GZ_ESIK ve G2_EK aynen"
K17_DOSYA = {"onkayit": "MUM_IZI17_ON_KAYIT.md", "rapor": "MUM_IZI17_RAPOR.md", "sonuc": "mum_izi17_sonuc.json", "olay": "mum_izi17_olay.csv", "pdf": "MUM_IZI17_SONRASI.pdf"}
K17_YOL = {"isaret6": os.path.join(_C, "cemal_mum_izi14_onay.json"), "anahtar6": os.path.join(_C, "MUM_IZI14_onay_anahtar.json"),
           "olcekli6": os.path.join(_C, "MUM_IZI14_onay_olcekli.json"), "olay13": os.path.join(_C, "mum_izi13_olay.csv"), "sonuc13": os.path.join(_C, "mum_izi13_sonuc.json")}
K17_SET6_AD = "MUM_IZI14_ONAY_OLCEKLI"
K17_EK: Dict[str, Any] = {
    "surum": "K17-1.0", "tanim": "MUM_IZI_GOZ GZ_ESIK aynen (ESIK11_SHA) + G2_EK aynen (EK13_SHA): giriş, ufuk 15 mum, stop = bölge dibi x 0,98, CETVEL2 konum eşi, "
                                "tablolar, permütasyonlar, işaret çevirme",
    "set6": "MUM_IZI14_ONAY_OLCEKLI (s2-18): sayfa -> bölge mühürlü MUM_IZI14_onay_anahtar.json 'yeni_sayfa' (zaman, pazar, sembol, bolge_bas = ilk barın tarihi, bolge_son, "
            "pencere); işaret cemal_mum_izi14_onay.json (EVET / KISMEN / HAYIR); üç dosyada sayfa kümesi ve zaman aynı olmalı (değilse DUR); mum boyu / olağan / oran "
            "MUM_IZI14_onay_olcekli.json'dan aynen (yeniden hesaplanmaz)",
    "birlesik": "set 1-6 (145 bölge); eş dışlama kümesi 145 olayla kurulur; set 1-5 değerleri mum_izi13_olay.csv ile karşılaştırılır (R15, es_R15, fark, n_es): değişen satır "
                "sayısı ve en büyük mutlak fark yazılır",
    "gecit": "getirisiz ölçülebilirlik: gz_olc_bir'in kapıları aynen (giris_yok, ufuk_kesik (15. mum > 2022-12-31), giris_stop_altinda); getiri hesaplamaz; hesapta gz_olc ile "
             "birebir aynı olmalı (değilse DUR)",
    "d5_tum": "BİLGİ ek ölçü: +%5 stop'tan önce (gz_olc_bir dokunma kuralı aynen: günlük sırayla High >= giriş x 1,05 olan ilk gün, Low <= stop olan ilk günden ÖNCE; aynı gün "
              "= stop önce); günlükte GZ d5 ile aynı; haftalıkta yeni (GZ haftalık hedefleri +%10 / +%20); aynı fonksiyonla hesaplanan haftalık +%10 GZ d10 ile aynı olmalı "
              "(değilse DUR); eşler için yok",
    "hucre": "n (ölçülen), n_es, R15 ort / medyan, eş ort, eşli fark ort / medyan, artıda payı (R15 > 0), eşinden iyi payı (fark > 0; eşi olanlarda), +%5 ve +%10 stop'tan "
             "önce payı (d5_tum, d10), stop payı",
    "tablolar": {"ucuncu_bakis": "yalnız set 6: Cemal sınıfı (EVET / KISMEN / HAYIR) x zaman (haftalık, günlük; birlikte bilgi) k17 hücresi + GZ tabloları (gz_tablolar) + "
                                 "g2_evet_es; BENZİYOR hücreleri n 3 / n 1: 'karşılaştırma yapılamaz / yalnız döküm'; 17 bölgenin tek tek dökümü",
                 "hakem": "BİLGİ: set 6'nın 17 bölgesi Cemal'in işaretinden bağımsız, zaman dilimine göre (haftalık, günlük, birlikte) k17 hücresi; karşılaştırma satırı set 5'in "
                          "24 bölgesi (hakem v3) aynı ölçülerle; ek bilgi: set 6 hakem sınıfı a (iki hakem EVET) / b",
                 "birlesik": "set 1-6 (145): GZ gz_tablolar (MUM_IZI13 birleşik tablosunun aynısı) + g2_evet_es + k17 hücresi (eşinden iyi payı, +%5); MUM_IZI13 birleşik "
                             "(mum_izi13_sonuc.json) ile fark: EVET - HAYIR eşli fark farkı ve p, EVET - eş, hücre n / R15 / eşli fark",
                 "yon": "üçüncü bakış iki bakışla aynı yönde mi: her dilimde EVET - HAYIR eşli fark farkının ve EVET - eş farkının İŞARETİ (MUM_IZI13 ilk / ikinci bakış ile); "
                        "hesaplanamazsa 'karşılaştırma yapılamaz'"},
    "etiket": "BİLGİ; ÖRNEKLEM YETERSİZ (bütün hücreler n < 30)",
    "es_siniri": "eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240): aynı gün aynı kova konum eşi",
    "pdf": "kapak: set 6 düz dil özet tablo (Cemal sınıfı x zaman) + hakem ve birleşik birer satır; sonra set 6'nın 17 bölgesinin HEPSİ: BENZİYOR, KISMEN, BENZEMİYOR "
           "(her sınıfta önce haftalık sonra günlük, bölge sonu sırası); her sayfada işaret, hisse, tarih, öncesi 15 mum + bölge + sonrası 30 mum, giriş / stop / 15. mum "
           "çizgileri, sağda girişe göre yüzde ekseni (MUM_IZI_HAKEM adım kuralı), R15, eş ortalaması, en yüksek / en derin, R30, stop, mum boyu satırı (olcekli json)",
}
K17_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü aynı kova (CETVEL2 v2.2 konum eşi) aynı takvim aralığı aynı stop geometrisi (GZ aynen); eş dışlama 145 olayla; sınır: eşler bölgenin "
                   "kendi koşusuyla eşlenmedi (Ç229 / Ç240)"),
    "K2": ("EVET", "Cemal set 6'yı sonrasını görmeden işaretledi (ölçekli sayfa bölge sonunda kesik; MUM_IZI_HAKEM yalnız t'ye kadar bar); işaret dosyası commit 0c6dfec, bu ön "
                   "kayıt set 6 getirilerinden önce; giriş bölgeden SONRAKİ barın açılışı; veri <= 2022-12-31 + KASA kapısı"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0); haftalık barlar tamamlanmış ISO haftaları (MH / MV aynen)"),
    "K4": ("EVET", "145 tekil bölge (zaman + sembol + bölge sonu; k17_ornek DUR); setler arası sembol tekrarı sayılıp yazılır"),
    "K5": ("EVET", "giriş = bölgeden sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk günü); giriş <= stop olay ölçülmez (sayısı yazılır)"),
    "K6": ("EVET", "MI bölünme düzeltmeli fiyatlar (GZ aynen); getiriler oransal; ABD USD, AVR yerel para; pazarlar arası karşılaştırma eşli farkla"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz"),
    "K8": ("EVET", "set 6 hücreleri n 1-4, birleşik hücreler n < 30 (HAYIR hariç): etiket 'BİLGİ; ÖRNEKLEM YETERSİZ'; n < 2 'karşılaştırma yapılamaz'; 17 bölge tek tek listeli; "
                   "tek dönem (<= 2022), BH yok (karar yok)"),
    "K9": ("EVET", "MUM_IZI17_ON_KAYIT.md: KOD17 / EK17 / ESIK11 / EK13 / işaret / anahtar / ölçekli / olay13 / sonuç13 sha + getirisiz sayımlar; set 6 getirilerinden önce commit; "
                   "k17_kapi sha + commit + temiz ağaç + IZ_KARNE.ik_kontrol_kapisi"),
    "K10": ("EVET", "işaret şeması GZ.gz_isaret_oku (bilinmeyen değer DUR); üç set 6 dosyasında sayfa kümesi ve zaman aynı (DUR); bölge başı veriden yeniden hesaplanıp anahtarla "
                    "denetlenir (GZ K10)"),
    "K11": ("EVET", "getirisiz geçit hesapta gz_olc ile birebir (DUR); haftalık +%10 k17 dokunma fonksiyonuyla GZ d10'a eşit (DUR); set 1-5 satırları mum_izi13_olay.csv ile "
                    "karşılaştırılır; tablo sayılarından >= 2 hücre olay csv'sinden bağımsız kodla yeniden üretilir (rapor öncesi)"),
    "K12": ("EVET", "'iz / tuttu / anlamlı' sözü yok; sayı ile yorum ayrı; n < 30 'örneklem yetersiz'"),
    "K13": ("EVET", "çakışma kapısı korunur; çalışan fonksiyonlar değişmez (test_mum_izi17 ast karşılaştırması); yasak defter / mühürlü dosyalara dokunulmaz; yalnız kendi yolları "
                    "commit; sızıntı taraması MI._mi_yaz"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez"),
}
K17_AD = {"EVET": "BENZİYOR", "KISMEN": "KISMEN", "HAYIR": "BENZEMİYOR"}
K17_ZAMAN = ("haftalik", "gunluk")


def _k17_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or G2_YOL["cikti"], K17_DOSYA[ad])


def k17_ek_sha() -> str:
    return hashlib.sha256(json.dumps(K17_EK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


# ---------------------------------------------------------------- örneklem
def k17_set6() -> pd.DataFrame:
    """Set 6: sayfa -> bölge (mühürlü anahtar), işaret (Cemal), mum boyu (ölçekli json). Üç dosyanın sayfa ve zaman tutarlılığı denetlenir."""
    E = GZ.gz_isaret_oku(K17_YOL["isaret6"]); EJ = json.load(open(K17_YOL["isaret6"], encoding="utf-8"))["sayfalar"]
    A = json.load(open(K17_YOL["anahtar6"], encoding="utf-8"))["sayfalar"]; B = {int(s["yeni_sayfa"]): s for s in json.load(open(K17_YOL["olcekli6"], encoding="utf-8"))["sayfalar"]}
    pa = {int(r["yeni_sayfa"]) for r in A}
    if pa != set(E) or pa != set(B) or len(pa) != len(A):
        raise G2Hata(f"K10: set 6 sayfa kümeleri uyuşmuyor (anahtar {sorted(pa)}, işaret {sorted(E)}, ölçekli {sorted(B)})")
    rows = []
    for r in A:
        pg = int(r["yeni_sayfa"]); b = B[pg]; ez = EJ[str(pg)].get("zaman")
        if b.get("zaman") != r["zaman"] or (ez is not None and ez != r["zaman"]):
            raise G2Hata(f"K10: set 6 sayfa {pg} zaman uyuşmuyor ({r['zaman']}, {b.get('zaman')}, {ez})")
        rows.append({"set": "set6", "set_ad": K17_SET6_AD, "sayfa": pg, "isaret": E[pg], "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "tarih": r["bolge_son"],
                     "m": int(r["pencere"]), "bolge_bas_anahtar": r["bolge_bas"], "hakem_sinif": r.get("sinif"), "hakem_karar": r.get("hakem_karar"),
                     "hakem2_karar": r.get("hakem2_karar"), "boy_mutlak": b.get("boy_mutlak"), "boy_onceki": b.get("onceki"), "boy_onceki_n": b.get("onceki_n"),
                     "boy_oran": b.get("oran")})
    X = pd.DataFrame(rows)
    for c in ("boy_mutlak", "boy_onceki", "boy_oran"):
        X[c] = pd.to_numeric(X[c], errors="coerce")
    X["sinif"] = np.where(X.isaret.isin(GZ.SINIF), X.isaret, None); X["sinif_son"] = X["sinif"]
    return X[X.sinif.notna()].reset_index(drop=True)


def k17_ornek() -> pd.DataFrame:
    X = pd.concat([g2_ornek(), k17_set6()], ignore_index=True)
    if X.duplicated(["zaman", "sembol", "tarih"]).any():
        raise G2Hata("K4: aynı bölge iki kez (set 1-6)")
    return X


def k17_sembol_tekrar(X: pd.DataFrame) -> Dict[str, Any]:
    s6 = X[X.set == "set6"]; once = X[X.set != "set6"]
    ort = sorted(set(s6.sembol) & set(once.sembol))
    return {"set6_onceki_setlerle_ortak_sembol": ort, "n": len(ort)}


# ---------------------------------------------------------------- getirisiz geçit
def _k17_veri(Vc: Dict[Any, Any], zaman: str, pazar: str) -> Tuple[Dict[str, pd.DataFrame], Optional[Dict[str, pd.DataFrame]]]:
    k = (zaman, pazar)
    if k not in Vc:
        if zaman == "gunluk":
            Vc[k] = (MI.mi_veri(pazar, MV.MV_YOL["gunluk"])["V"], None)
        else:
            Vd = MI.mi_veri(pazar, MH.MH_YOL["tam"])["V"]; Vc[k] = (Vd, MV.mv_haftalik_panel(Vd))
    return Vc[k]


def k17_gecit_bir(Dg: pd.DataFrame, W: Optional[pd.DataFrame], r: Dict[str, Any], kesik: pd.Timestamp) -> Dict[str, Any]:
    """gz_olc_bir'in kapıları aynen; getiri hesaplanmaz (yalnız giriş açılışı ve bölge dibi okunur)."""
    E = GZ.GZ_ESIK["olcu"]; U = int(E["ufuk"]); sc = float(E["stop_carpan"])
    B = W if r["zaman"] == "haftalik" else Dg
    t = B.index.get_loc(pd.Timestamp(r["tarih"])); m = int(r["m"]); s = t - m + 1
    rec: Dict[str, Any] = {"olculebilir": False, "neden": "", "bolge_bas_bar": B.index[s]}
    stop = float(B.Low.to_numpy(float)[s:t + 1].min()) * sc
    if t + 1 >= len(B):
        rec["neden"] = "giris_yok"; return rec
    g = W.bas.iloc[t + 1] if r["zaman"] == "haftalik" else Dg.index[t + 1]; E0 = float(Dg.Open.iloc[Dg.index.get_loc(g)])
    if t + U >= len(B) or B.index[t + U] > kesik:
        rec["neden"] = "ufuk_kesik"; return rec
    if E0 <= stop:
        rec["neden"] = "giris_stop_altinda"; return rec
    rec.update({"olculebilir": True, "son15_tarih": str(pd.Timestamp(B.index[t + U]).date())})
    return rec


def k17_gecit(X: pd.DataFrame) -> pd.DataFrame:
    Vc: Dict[Any, Any] = {}; out = []
    for r in X.to_dict("records"):
        Vd, Vw = _k17_veri(Vc, r["zaman"], r["pazar"])
        if r["sembol"] not in Vd:
            out.append({"olculebilir": False, "neden": "veri_yok"}); continue
        rec = k17_gecit_bir(Vd[r["sembol"]], Vw[r["sembol"]] if Vw is not None else None, r, MI.MI_KESIK)
        if isinstance(r.get("bolge_bas_anahtar"), str) and str(pd.Timestamp(rec["bolge_bas_bar"]).date()) != r["bolge_bas_anahtar"]:
            raise G2Hata(f"K10: {r['set']} s{r['sayfa']} bölge başı anahtarla uyuşmuyor")
        out.append(rec)
    return pd.concat([X.reset_index(drop=True), pd.DataFrame(out)[["olculebilir", "neden"] + (["son15_tarih"] if any("son15_tarih" in o for o in out) else [])]], axis=1)


def k17_sayim(G: pd.DataFrame) -> Dict[str, Any]:
    """GETİRİSİZ sayım: sınıf x zaman, ölçülebilen / ölçülemeyen ve nedeni (set 6 ve birleşik)."""
    def bir(g: pd.DataFrame) -> Dict[str, Any]:
        o = g[g.olculebilir.astype(bool)]
        return {"toplam": int(len(g)), "olculebilir": int(len(o)), "olculemedi": g[~g.olculebilir.astype(bool)].neden.value_counts().to_dict(),
                "sinif_zaman": {f"{s}|{z}": int(((g.sinif == s) & (g.zaman == z)).sum()) for s in GZ.SINIF for z in K17_ZAMAN},
                "sinif_zaman_olculebilir": {f"{s}|{z}": int(((o.sinif == s) & (o.zaman == z)).sum()) for s in GZ.SINIF for z in K17_ZAMAN},
                "pazar": g.pazar.value_counts().to_dict(), "en_gec_15_mum": (str(o.son15_tarih.max()) if "son15_tarih" in o and len(o) else None)}
    s6 = G[G.set == "set6"]
    return {"set6": bir(s6), "birlesik": bir(G), "set5": bir(G[G.set == "set5"]),
            "set6_hakem_sinif": s6.hakem_sinif.value_counts().to_dict() if "hakem_sinif" in s6 else {}}


# ---------------------------------------------------------------- ek ölçü (+%5 her iki dilimde) ve hücre
def k17_dokunma(Hs: np.ndarray, Ls: np.ndarray, E0: float, stop: float, x: float) -> float:
    """gz_olc_bir dokunma kuralı aynen: günlük sırayla High >= E0 x (1 + x) olan ilk gün, Low <= stop olan ilk günden ÖNCE (aynı gün = stop önce)."""
    Hs = np.asarray(Hs, float); Ls = np.asarray(Ls, float)
    sk = np.flatnonzero(Ls <= stop); ks = int(sk[0]) if len(sk) else 10 ** 9
    hk = np.flatnonzero(Hs >= E0 * (1 + x))
    return float(len(hk) > 0 and int(hk[0]) < ks)


def k17_d5(Y: pd.DataFrame) -> pd.DataFrame:
    """d5_tum: günlükte GZ d5 aynen; haftalıkta günlük veriyle aynı kural. Denetim: aynı fonksiyonla haftalık +%10 = GZ d10."""
    Y = Y.copy(); Y["d5_tum"] = np.nan; Vc: Dict[Any, Any] = {}
    g = Y.olculdu.astype(bool) & (Y.zaman == "gunluk"); Y.loc[g, "d5_tum"] = Y.loc[g, "d5"].astype(float)
    for i in Y.index[Y.olculdu.astype(bool) & (Y.zaman == "haftalik")]:
        r = Y.loc[i]; Vd, _ = _k17_veri(Vc, "haftalik", r.pazar); Dg = Vd[r.sembol]
        gi = Dg.index.get_loc(pd.Timestamp(r.giris)); ei = Dg.index.get_loc(pd.Timestamp(r.son15))
        Hs = Dg.High.to_numpy(float)[gi:ei + 1]; Ls = Dg.Low.to_numpy(float)[gi:ei + 1]
        if k17_dokunma(Hs, Ls, float(r.E0), float(r.stop), 0.10) != float(r.d10):
            raise G2Hata(f"K11: haftalık +%10 yeniden hesabı GZ d10 ile uyuşmuyor ({r.set} s{r.sayfa})")
        Y.loc[i, "d5_tum"] = k17_dokunma(Hs, Ls, float(r.E0), float(r.stop), 0.05)
    return Y


def k17_hucre(g: pd.DataFrame) -> Dict[str, Any]:
    out = k15_hucre(g); o = g[g.olculdu.astype(bool)]; f = o[np.isfinite(o.fark.astype(float))]
    out.update({"es_ort": float(f.es_R15.astype(float).mean()) if len(f) else None,
                "d5_pay": float(o.d5_tum.astype(float).mean()) if len(o) and "d5_tum" in o else None,
                "d10_pay": float(o.d10.astype(float).mean()) if len(o) else None, "stop_pay": float(o.stop15.astype(float).mean()) if len(o) else None})
    out["etiket"] = "boş" if not out["n"] else K17_EK["etiket"]
    return out


def k17_tablolar(Y: pd.DataFrame) -> Dict[str, Any]:
    Y6 = Y[Y.set == "set6"]; Y5 = Y[Y.set == "set5"]; zz = K17_ZAMAN + ("birlikte",)

    def zs(D: pd.DataFrame, z: str) -> pd.DataFrame:
        return D if z == "birlikte" else D[D.zaman == z]
    uc = {f"{s}|{z}": k17_hucre(zs(Y6[Y6.sinif == s], z)) for s in GZ.SINIF for z in zz}
    hk = {f"{st}|{z}": k17_hucre(zs(D, z)) for st, D in (("set6", Y6), ("set5", Y5)) for z in zz}
    hk.update({f"set6_hakem_{h}|{z}": k17_hucre(zs(Y6[Y6.hakem_sinif == h], z)) for h in ("a", "b") for z in zz})
    bk = {f"{s}|{z}": k17_hucre(zs(Y[Y.sinif.isin(sl)], z)) for s, sl in (("EVET", ["EVET"]), ("KISMEN", ["KISMEN"]), ("HAYIR", ["HAYIR"]), ("EVET+KISMEN", ["EVET", "KISMEN"]))
          for z in zz}
    return {"ucuncu_bakis": {"hucre": uc, "gz": GZ.gz_tablolar(Y6), "evet_es": g2_evet_es(Y6)}, "hakem": hk,
            "birlesik": {"tablo": GZ.gz_tablolar(Y), "evet_es": g2_evet_es(Y), "k17_hucre": bk, "duyarlilik_son_isaret": GZ.gz_tablolar(Y, "sinif_son")["karsilastirma"]}}


def k17_dokum(Y: pd.DataFrame) -> List[Dict[str, Any]]:
    Y6 = Y[Y.set == "set6"].copy(); Y6["_s"] = Y6.sinif.map({s: i for i, s in enumerate(GZ.SINIF)}); Y6["_z"] = Y6.zaman.map({"haftalik": 0, "gunluk": 1})
    kol = ["sayfa", "isaret", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "m", "olculdu", "neden", "R15", "es_R15", "n_es", "fark", "max15", "min15", "stop15", "d5_tum",
           "d10", "R30", "boy_mutlak", "boy_onceki", "boy_oran", "hakem_sinif", "hakem2_karar"]
    return [{k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in r.items()} for r in Y6.sort_values(["_s", "_z", "bolge_son"])[kol].to_dict("records")]


def k17_yon(T: Dict[str, Any], J13: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for z in K17_ZAMAN:
        k = T["ucuncu_bakis"]["gz"]["karsilastirma"][f"EVET-HAYIR|{z}"]["esli_fark_fark"]; e = T["ucuncu_bakis"]["evet_es"][f"EVET-es|{z}"]
        e3 = e["esli_fark_ort"] if e["n_es"] >= 2 else None
        r = {}
        for ad, v3, v1, v2 in (("EVET-HAYIR_esli", k, J13["ilk_bakis"]["tablo"]["karsilastirma"][f"EVET-HAYIR|{z}"]["esli_fark_fark"],
                                J13["ikinci_bakis"]["tablo"]["karsilastirma"][f"EVET-HAYIR|{z}"]["esli_fark_fark"]),
                               ("EVET-es", e3, J13["ilk_bakis_evet_es"][f"EVET-es|{z}"]["esli_fark_ort"], J13["ikinci_bakis"]["evet_es"][f"EVET-es|{z}"]["esli_fark_ort"])):
            r[ad] = {"ilk": v1, "ikinci": v2, "ucuncu": v3,
                     "ilkle_ayni_yon": None if (v3 is None or v1 is None) else bool(np.sign(v3) == np.sign(v1)),
                     "ikinciyle_ayni_yon": None if (v3 is None or v2 is None) else bool(np.sign(v3) == np.sign(v2)),
                     "durum": "karşılaştırma yapılamaz" if v3 is None else "hesaplandı"}
        out[z] = r
    return out


def k17_fark13(J13: Dict[str, Any], T: Dict[str, Any]) -> Dict[str, Any]:
    """MUM_IZI13 birleşik (128) -> MUM_IZI17 birleşik (145)."""
    a = J13["birlesik"]; b = T["birlesik"]; out: Dict[str, Any] = {"karsilastirma": {}, "evet_es": {}, "hucre": {}}
    for k, v in b["tablo"]["karsilastirma"].items():
        o = a["tablo"]["karsilastirma"].get(k, {})
        out["karsilastirma"][k] = {"esli_fark_fark_13": o.get("esli_fark_fark"), "esli_fark_fark_17": v.get("esli_fark_fark"), "esli_p_13": o.get("esli_p"), "esli_p_17": v.get("esli_p")}
    for k, v in b["evet_es"].items():
        o = a["evet_es"].get(k, {})
        out["evet_es"][k] = {"ort_13": o.get("esli_fark_ort"), "ort_17": v.get("esli_fark_ort"), "p_13": o.get("p"), "p_17": v.get("p"), "n_13": o.get("n_es"), "n_17": v.get("n_es")}
    for k, v in b["tablo"]["hucre"].items():
        if k.endswith("|BIST"):
            continue
        o = a["tablo"]["hucre"].get(k, {})
        out["hucre"][k] = {"n_13": o.get("n"), "n_17": v.get("n"), "R15_ort_13": o.get("R15_ort"), "R15_ort_17": v.get("R15_ort"), "fark_ort_13": o.get("fark_ort"),
                           "fark_ort_17": v.get("fark_ort")}
    return out


def k17_set15_farki(O13: pd.DataFrame, O17: pd.DataFrame) -> Dict[str, Any]:
    M = O13.merge(O17[O17.set != "set6"], on=["set", "sayfa"], suffixes=("_13", "_17")); fk = {}; en = {}
    for c in ("R15", "es_R15", "fark", "n_es"):
        a = M[f"{c}_13"].to_numpy(float); b = M[f"{c}_17"].to_numpy(float); ayni = np.isclose(a, b, atol=1e-9) | (np.isnan(a) & np.isnan(b))
        fk[c] = int((~ayni).sum()); d = np.abs(a - b); d = d[~ayni & np.isfinite(d)]; en[c] = float(d.max()) if len(d) else 0.0
    nan_deg = int(((M.es_neden_13.fillna("") != M.es_neden_17.fillna(""))).sum()) if "es_neden_13" in M else None
    degisen = M[~(np.isclose(M.fark_13.to_numpy(float), M.fark_17.to_numpy(float), atol=1e-9) | (M.fark_13.isna() & M.fark_17.isna()))][["set", "sayfa", "sembol_13", "fark_13", "fark_17"]]
    return {"satir": int(len(M)), "beklenen": int(len(O13)), "farkli": fk, "en_buyuk_mutlak_fark": en, "es_neden_degisen": nan_deg,
            "degisen_satirlar": degisen.to_dict("records")}


# ---------------------------------------------------------------- kapı, ön kayıt, koşu
def k17_sha_simdi() -> Dict[str, str]:
    return {"KOD17_SHA": MI._mi_sha(G2_YOL["kod"]), "EK17_SHA": k17_ek_sha(), "EK13_SHA": g2_ek_sha(), "GZ_KOD_SHA": MI._mi_sha(GZ.GZ_YOL["kod"]), "ESIK11_SHA": GZ.gz_esik_sha(),
            "ISARET_SET6_SHA": MI._mi_sha(K17_YOL["isaret6"]), "ANAHTAR_SET6_SHA": MI._mi_sha(K17_YOL["anahtar6"]), "OLCEKLI_SET6_SHA": MI._mi_sha(K17_YOL["olcekli6"]),
            "OLAY13_SHA": MI._mi_sha(K17_YOL["olay13"]), "SONUC13_SHA": MI._mi_sha(K17_YOL["sonuc13"])}


def k17_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    yol = _k17_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise G2Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = k17_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise G2Hata(f"ön kayıt 17 kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_G2); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise G2Hata("ön kayıt 17 commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_GOZ2.py", "MUM_IZI_GOZ.py"] + [os.path.relpath(v, KOK_G2) for v in K17_YOL.values()]):
        raise G2Hata("ön kayıt / kod / girdiler çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def k17_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    y = _k17_yol("onkayit", cikti)
    if os.path.exists(y):
        raise G2Hata("ön kayıt 17 zaten var")
    X = k17_ornek(); G = k17_gecit(X); S = k17_sayim(G); sh = k17_sha_simdi(); st = k17_sembol_tekrar(X)
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in K17_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_GOZ2.py"])

    def tablo(s: Dict[str, Any]) -> List[str]:
        t = ["| Cemal | haftalık (ölçülebilen) | günlük (ölçülebilen) |", "|---|---|---|"]
        for c in GZ.SINIF:
            t.append(f"| {K17_AD[c]} | {s['sinif_zaman'][f'{c}|haftalik']} ({s['sinif_zaman_olculebilir'][f'{c}|haftalik']}) | "
                     f"{s['sinif_zaman'][f'{c}|gunluk']} ({s['sinif_zaman_olculebilir'][f'{c}|gunluk']}) |")
        return t
    s6 = S["set6"]; sb = S["birlesik"]
    s = [f"# MUM_IZI17 ÖN KAYIT ({MI._mi_simdi()})", "",
         "MUM_IZI11_ON_KAYIT ve MUM_IZI13_ON_KAYIT tanımları AYNEN (MUM_IZI_GOZ.py GZ_ESIK: ESIK11_SHA; MUM_IZI_GOZ2 G2_EK: EK13_SHA): giriş = bölgeden sonraki ilk geçerli barın "
         "açılışı; ufuk 15 mum; stop = bölge dibi x 0,98; dokunma; R30; CETVEL2 konum eşi; tablolar; permütasyonlar. Ek: set 6 = MUM_IZI14_ONAY_OLCEKLI 17 bölge (Cemal'in "
         "sonrasını görmeden, yüzde eksenli sayfada işaretlediği ilk set). Bu dosya set 6'nın getirileri hesaplanmadan ÖNCE commit edilir; getirisiz sayımlar aşağıda.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_GOZ2.py commit'i: {kc or 'yok'}", "",
         "## GETİRİSİZ SAYIM (getiri hesaplanmadı; yalnız işaret, zaman, veri kapıları)", "",
         f"Set 6: {s6['toplam']} bölge, ölçülebilen {s6['olculebilir']}, ölçülemeyen {s6['toplam'] - s6['olculebilir']} {json.dumps(s6['olculemedi'], ensure_ascii=False)}; "
         f"pazar {json.dumps(s6['pazar'], ensure_ascii=False)}; en geç 15. mum {s6['en_gec_15_mum']}; hakem sınıfı {json.dumps(S['set6_hakem_sinif'], ensure_ascii=False)} "
         "(a = iki hakem EVET).", "", *tablo(s6), "",
         f"Birleşik set 1-6: {sb['toplam']} bölge, ölçülebilen {sb['olculebilir']}, ölçülemeyen {sb['toplam'] - sb['olculebilir']} "
         f"{json.dumps(sb['olculemedi'], ensure_ascii=False)}; pazar {json.dumps(sb['pazar'], ensure_ascii=False)}.", "", *tablo(sb), "",
         f"- Set 6'nın önceki setlerle ortak sembolü: {st['n']} {st['set6_onceki_setlerle_ortak_sembol']} (bölge tekrarı yok: zaman + sembol + bölge sonu tekil, denetlendi).",
         "- Eş sayısı (eşi < 5 / kovasız) hesapta belirlenir ve yazılır; eşsiz olay eşli tabloya girmez (GZ aynen).",
         "- Set 6 BENZİYOR: haftalık 3, günlük 1 -> günlük BENZİYOR hücresi 'yalnız döküm'; haftalık BENZİYOR - BENZEMİYOR karşılaştırması n 3 / 3 ile (bilgi).", "",
         "## Tablolar (önceden; sonuçtan sonra değişmez)", "",
         "- (i) ÜÇÜNCÜ BAKIŞ = yalnız set 6: Cemal sınıfı x zaman dilimi: n, R15 ort / medyan, eş ort, eşli fark ort / medyan, artıda payı, eşinden iyi payı, +%5 / +%10 "
         "stop'tan önce payı, stop payı. +%5 haftalıkta GZ'de yoktu (haftalık hedefler +%10 / +%20): aynı dokunma kuralıyla BİLGİ olarak eklenir (d5_tum); GZ tabloları "
         "(haftalık +%10 / +%20) aynen ayrıca yazılır. BENZİYOR hücreleri (n 3 ve n 1): 'karşılaştırma yapılamaz / yalnız döküm'. 17 bölge tek tek döküm (sayfa, işaret, "
         "zaman, sembol, R15, eş ort, mum boyu %, oran).",
         "- (ii) HAKEMİN SEÇTİKLERİ (BİLGİ): set 6'nın 17 bölgesi Cemal'in işaretinden bağımsız, zaman dilimine göre (haftalık, günlük, birlikte); karşılaştırma satırı set 5 "
         "(24, hakem v3, dokuzuncu ölçütsüz) aynı ölçülerle; ek bilgi satırı hakem sınıfı a / b.",
         "- (iii) BİRLEŞİK = set 1-6 (145): MUM_IZI13 birleşik tablosunun aynısı (EVET / KISMEN / HAYIR / EVET+KISMEN x zaman; EVET - HAYIR ve (EVET + KISMEN) - HAYIR eşli "
         "fark farkı + permütasyon p; EVET - eş işaret çevirme p) + MUM_IZI13 birleşiğine göre değişim. Soru: iki bakıştaki yön (haftalıkta BENZİYOR eşlerin gerisinde; günlükte "
         "fark yok) üçüncüyle değişti mi: 'aynı yön' = farkın İŞARETİ; hesaplanamazsa 'karşılaştırma yapılamaz'.",
         "- Set 1-5 satırları mum_izi13_olay.csv ile karşılaştırılır (R15, es_R15, fark, n_es): eş dışlama kümesi 145 olayla kurulduğu için eş değerleri değişebilir; değişen satır "
         "sayısı ve en büyük fark yazılır.",
         "- OKUMA: bütün hücreler n < 30 (birleşik HAYIR hariç): etiket 'BİLGİ; ÖRNEKLEM YETERSİZ'. Eş sınırı: eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240).", "",
         "## Ek tanımlar (K17_EK; sha yukarıda)", "", "```", json.dumps(K17_EK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ (`python IZ_KARNE.py kontrol`; K8: set 6 hücreleri n < 30)", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 17")


K17_KOL = ["set", "set_ad", "sayfa", "isaret", "sinif", "sinif_son", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "m", "olculdu", "neden", "giris", "E0", "stop", "son15",
           "R15", "max15", "min15", "stop15", "d5", "d10", "d20", "R30", "panel", "kova", "n_es", "es_R15", "es_med", "fark", "sira", "es_max15", "es_min15", "es_d5", "es_d10",
           "es_d20", "es_stop15", "es_neden", "d5_tum", "hakem_sinif", "hakem_karar", "hakem2_karar", "boy_mutlak", "boy_onceki", "boy_onceki_n", "boy_oran"]


def k17_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    t0 = time.time(); cikti = cikti or G2_YOL["cikti"]
    if os.path.exists(_k17_yol("sonuc", cikti)):
        raise G2Hata("sonuç 17 zaten var")
    G0 = k17_kapi(cikti)
    kasa = KS.kasa_kapisi([os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] +
                          [os.path.join(MH.MH_YOL["tam"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")],
                          "2022-12-31")
    X = k17_ornek(); Gt = k17_gecit(X)
    Y = GZ.gz_es(GZ.gz_olc(X))
    if not (Y.olculdu.astype(bool).to_numpy() == Gt.olculebilir.astype(bool).to_numpy()).all() or \
            not (Y.neden.fillna("").to_numpy() == Gt.neden.fillna("").to_numpy()).all():
        raise G2Hata("K11: getirisiz geçit ile gz_olc uyuşmuyor")
    Y = k17_d5(Y).sort_values(["set", "sayfa"]).reset_index(drop=True)
    for c in K17_KOL:
        if c not in Y:
            Y[c] = np.nan
    O = Y[K17_KOL].copy()
    for c in ("bolge_bas", "bolge_son", "giris", "son15"):
        O[c] = pd.to_datetime(O[c]).dt.strftime("%Y-%m-%d")
    O.to_csv(_k17_yol("olay", cikti), index=False, float_format="%.6f")
    O17 = pd.read_csv(_k17_yol("olay", cikti)); O13 = pd.read_csv(K17_YOL["olay13"])
    J13 = json.load(open(K17_YOL["sonuc13"], encoding="utf-8")); T = k17_tablolar(O)      # tablolar tam duyarlıkla (g2_kos gibi bellekteki satırlardan)
    Y6 = O[O.set == "set6"]
    J = {"surum": K17_SURUM, "kapi": G0, "kasa": kasa, "sayim": k17_sayim(Gt), "sembol_tekrar": k17_sembol_tekrar(X),
         "es_yok": {"set6": Y6[Y6.olculdu.astype(bool)].es_neden.fillna("").replace("", "var").value_counts().to_dict(),
                    "birlesik": O[O.olculdu.astype(bool)].es_neden.fillna("").replace("", "var").value_counts().to_dict()},
         "set1_5_mum_izi13_farki": k17_set15_farki(O13, O17), **T, "dokum_set6": k17_dokum(O), "yon": k17_yon(T, J13), "mum_izi13_birlesik_farki": k17_fark13(J13, T),
         "etiket": K17_EK["etiket"], "es_siniri": K17_EK["es_siniri"], "olay_sha": MI._mi_sha(_k17_yol("olay", cikti)), "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_k17_yol("sonuc", cikti), J, "sonuç 17")
    return J


# ---------------------------------------------------------------- PDF
def _k17_yuzde(p: Optional[float]) -> str:
    return "-" if p is None or not np.isfinite(p) else f"{'+' if p >= 0 else '-'}%{abs(p) * 100:.1f}".replace(".", ",")


def _k17_pay(p: Optional[float], n: int) -> str:
    return "-" if p is None or not n or not np.isfinite(p) else f"{int(round(p * n))} / {n}"


def k17_sayfa(fig, r: Any, d: pd.DataFrame) -> None:
    """Tek bölge sonrası sayfası (g2_pdf düzeni + sağda girişe göre yüzde ekseni + mum boyu satırı)."""
    import MUM_IZI_HAKEM as HK   # yalnız okunur: yüzde adımı ve mum boyu satırı aynı kuralla
    t = d.index.get_loc(pd.Timestamp(r.bolge_son)) if r.zaman == "gunluk" else int(np.flatnonzero(d.index >= pd.Timestamp(r.bolge_son))[0])
    m = int(r.m); i0 = max(0, t - m + 1 - 15); i1 = min(len(d) - 1, t + 30); eksik = (t + 30) - i1
    BU, BO, BA = MI.mi_bant(d.Close.to_numpy(float)); sl = slice(i0, i1 + 1); zad = "haftalık" if r.zaman == "haftalik" else "günlük"
    fig.text(0.07, 0.955, f"Senin işaretin: {K17_AD[r.sinif]}", fontsize=17, weight="bold", color={"EVET": "#1a9850", "KISMEN": "#e08214", "HAYIR": "#d73027"}[r.sinif])
    ax = fig.add_axes([0.07, 0.38, 0.8, 0.52])
    MV._mv_ciz(ax, *(d[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close")), BU[sl], BO[sl], BA[sl], (t - m + 1 - i0, t - i0),
               f"{r.sembol} ({r.pazar}) · {zad} · bölge {r.bolge_bas} .. {r.bolge_son}")
    xg = t + 1 - i0
    if np.isfinite(r.E0):
        ax.axvline(xg - 0.5, color="#1a9850", linewidth=1.2, linestyle="--"); ax.hlines(r.E0, xg - 0.5, i1 - i0 + 0.5, color="#1a9850", linewidth=1)
    if np.isfinite(r.stop):
        ax.hlines(r.stop, t - m + 1 - i0 - 0.5, i1 - i0 + 0.5, color="#d73027", linewidth=1)
    if t + 15 <= i1:
        ax.axvline(t + 15 - i0 + 0.4, color="#777777", linewidth=1.2)
    ax.set_xticks([t - m + 1 - i0, xg] + ([t + 15 - i0] if t + 15 <= i1 else []))
    ax.set_xticklabels([str(d.index[t - m + 1].date()), "giriş"] + (["15. mum"] if t + 15 <= i1 else []), fontsize=9)
    lo = float(np.nanmin(d.Low.to_numpy(float)[sl])); hi = float(np.nanmax(d.High.to_numpy(float)[sl])); pd_ = 0.05 * (hi - lo)
    lo, hi = lo - pd_, hi + pd_; ax.set_ylim(lo, hi)      # dikey ölçek mumlara göre (bant çerçevede kesilir); yüzde ekseni gerçek boyu gösterir
    ref = float(r.E0) if np.isfinite(r.E0) else float(d.Close.iloc[t])
    _, ps = HK.hk_yuzde_adim(lo, hi, ref); yv = [ref * (1 + p / 100) for p in ps]
    for v in yv:
        ax.axhline(v, color="#cccccc", linewidth=0.5, zorder=0)
    ax2 = ax.twinx(); ax2.set_ylim(lo, hi); ax2.set_yticks(yv); ax2.set_yticklabels([HK._hk_yuzde_yazi(p) for p in ps], fontsize=10)
    ax2.set_ylabel("girişe göre (0 = giriş fiyatı)", fontsize=9)
    if bool(r.olculdu):
        es = f"{_k17_yuzde(r.es_R15)} ({int(r.n_es)} hisse)" if np.isfinite(r.es_R15) else "eş yok"
        alt = [f"15 mum getirisi: {_k17_yuzde(r.R15)}      eşlerin ortalaması: {es}",
               f"eşinden fark: {_k17_yuzde(r.fark) if np.isfinite(r.fark) else '-'}      en yüksek: {_k17_yuzde(r.max15)}      en derin: {_k17_yuzde(r.min15)}",
               f"+%5'e stop'tan önce: {'evet' if r.d5_tum == 1 else 'hayır'}      +%10'a: {'evet' if r.d10 == 1 else 'hayır'}      stop: {'oldu' if r.stop15 == 1 else 'olmadı'}"
               f"      30 mum: {_k17_yuzde(r.R30) if np.isfinite(r.R30) else '-'}"]
    else:
        alt = [f"ölçülmedi: {r.neden}"]
    B = {"boy_mutlak": float(r.boy_mutlak), "onceki": float(r.boy_onceki) if np.isfinite(r.boy_onceki) else float("nan"),
         "onceki_n": int(r.boy_onceki_n) if np.isfinite(r.boy_onceki_n) else 0, "oran": float(r.boy_oran) if np.isfinite(r.boy_oran) else float("nan")}
    b1, b2 = HK.hk_boy_satiri(B)
    alt += ["", b1, b2]
    if eksik > 0:
        alt.append(f"sonrası {30 - eksik} mum (veri 2022-12-30'da bitiyor)")
    fig.text(0.07, 0.32, "\n".join(alt), fontsize=11.5, va="top", linespacing=1.6)
    fig.text(0.07, 0.06, "Turuncu kutu = bölge · yeşil kesik = giriş · kırmızı = stop (bölge dibi x 0,98) · gri dikey = 15. mum · mor = Bollinger 20 ve SMA20",
             fontsize=8.5, color="#555555")


def k17_pdf(cikti: Optional[str] = None, olay: Optional[pd.DataFrame] = None, sonuc: Optional[Dict[str, Any]] = None, yol: Optional[str] = None) -> str:
    """MUM_IZI17_SONRASI.pdf. olay / sonuc / yol verilirse (deneme basımı) dosyalar okunmaz."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    cikti = cikti or G2_YOL["cikti"]; y = yol or _k17_yol("pdf", cikti)
    if olay is None:
        J = json.load(open(_k17_yol("sonuc", cikti), encoding="utf-8"))
        if MI._mi_sha(_k17_yol("olay", cikti)) != J["olay_sha"]:
            raise G2Hata("olay csv'si sonuç 17 json'uyla uyuşmuyor")
        O = pd.read_csv(_k17_yol("olay", cikti))
    else:
        O, J = olay, sonuc
    st = "set6" if (O.set == "set6").any() else "set5"; U = J["ucuncu_bakis"]["hucre"]; HK_ = J["hakem"]; BK = J["birlesik"]["k17_hucre"]
    Vc: Dict[Any, Any] = {}
    with PdfPages(y, metadata={"Title": "MUM_IZI17 sonrası", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); n6 = int((O.set == st).sum())
        fig.text(0.05, 0.955, f"Son {n6} bölge (yüzde eksenli sayfa): işaretlerin sonrasında ne yaptı", fontsize=14, weight="bold")
        fig.text(0.05, 0.928, "Giriş: bölgeden sonraki ilk mumun açılışı. 15 mum sonraki kapanışla getiri. Eş: aynı gün, benzer oynaklık ve likiditedeki hisseler.",
                 fontsize=9)
        ax = fig.add_axes([0.02, 0.66, 0.96, 0.25]); ax.axis("off"); sat = []
        for z, zad in (("haftalik", "haftalık"), ("gunluk", "günlük")):
            for s in GZ.SINIF:
                c = U[f"{s}|{z}"]; n = c.get("n", 0); ne = c.get("n_es", 0)
                sat.append([K17_AD[s], zad, str(n), _k17_pay(c.get("arti_pay"), n), _k17_yuzde(c.get("R15_ort")), _k17_yuzde(c.get("R15_med")), _k17_yuzde(c.get("es_ort")),
                            _k17_pay(c.get("esinden_iyi_pay"), ne), _k17_pay(c.get("d5_pay"), n), _k17_pay(c.get("stop_pay"), n)])
        tb = ax.table(cellText=sat, colLabels=["senin\nişaretin", "mum", "bölge", "artıda\nkapanan", "ortalama", "medyan", "eşlerin\nort.", "eşinden\niyi", "+%5'e\nstop'tan önce",
                                               "stop\nolan"], loc="upper center", cellLoc="center",
                      colWidths=[0.13, 0.09, 0.06, 0.09, 0.1, 0.1, 0.09, 0.09, 0.13, 0.08])
        tb.auto_set_font_size(False); tb.set_fontsize(9.5); tb.scale(1, 2.3)

        def sat_yaz(c: Dict[str, Any]) -> str:
            return (f"{c.get('n', 0)} bölge, ortalama {_k17_yuzde(c.get('R15_ort'))}, eşlerinden {_k17_yuzde(c.get('fark_ort'))}, eşinden iyi "
                    f"{_k17_pay(c.get('esinden_iyi_pay'), c.get('n_es', 0))}")
        sat2 = [f"Hakemin seçtiği {n6} bölgenin hepsi: haftalık {sat_yaz(HK_[f'{st}|haftalik'])}; günlük {sat_yaz(HK_[f'{st}|gunluk'])}.",
                f"Bütün bölgeler ({int(len(O))}): haftalık BENZİYOR {sat_yaz(BK['EVET|haftalik'])}; BENZEMİYOR {sat_yaz(BK['HAYIR|haftalik'])}.",
                f"Günlük BENZİYOR {sat_yaz(BK['EVET|gunluk'])}; BENZEMİYOR {sat_yaz(BK['HAYIR|gunluk'])}."]
        import textwrap
        yy = 0.63
        for s_ in sat2:
            w = textwrap.fill(s_, 95); fig.text(0.05, yy, w, fontsize=9.5, va="top", linespacing=1.4); yy -= 0.019 * (w.count("\n") + 1) + 0.015
        fig.text(0.05, yy - 0.01, "Sayılar çok az (N < 30): bu bir sonuç değil, bilgi.", fontsize=13, weight="bold")
        fig.text(0.05, yy - 0.06, "Sonraki sayfalar: bu bölgelerin hepsi; önce BENZİYOR, sonra KISMEN, sonra BENZEMİYOR dediklerin\n(her birinde önce haftalık). "
                 "Hisse ve tarih açık. Sağdaki eksen girişe göre yüzde (0 = giriş fiyatı).\nAltta bölgedeki gerçek mum boyu "
                 "ve bu hissenin olağanına oranı (1'den küçük = bölgede mumlar olağandan küçük).", fontsize=9.5, va="top", linespacing=1.5)
        pdf.savefig(fig); plt.close(fig)
        X = O[O.set == st].copy(); X["_s"] = X.sinif.map({s: i for i, s in enumerate(GZ.SINIF)}); X["_z"] = X.zaman.map({"haftalik": 0, "gunluk": 1})
        for r in X.sort_values(["_s", "_z", "bolge_son"]).itertuples():
            k = (r.zaman, r.pazar)
            if k not in Vc:
                Vc[k] = MV.mv_veri(*k)
            fig = plt.figure(figsize=(8.3, 11.7)); k17_sayfa(fig, r, Vc[k][r.sembol]); pdf.savefig(fig); plt.close(fig)
    return y


# ================================================================ 4e) MUM_IZI EK 19: DÖRDÜNCÜ BAKIŞ (set 7 = MUM_IZI18 mum boyu kapılı onay seti, 12 bölge) + set 6+7 + BİRLEŞİK 1-7
K19_SURUM = "MUM_IZI_GOZ2 set7 v1.0 (2026-11-26): EK 19 göz ölçümü dördüncü bakış (set 7) + gerçek ölçekle işaretlenenler (set 6+7) + birleşik 157; tanımlar GZ_ESIK, G2_EK, K17_EK aynen"
K19_DOSYA = {"onkayit": "MUM_IZI19_ON_KAYIT.md", "rapor": "MUM_IZI19_RAPOR.md", "sonuc": "mum_izi19_sonuc.json", "olay": "mum_izi19_olay.csv", "pdf": "MUM_IZI19_SONRASI.pdf"}
K19_YOL = {"isaret7": os.path.join(_C, "cemal_mum_izi18_onay.json"), "anahtar7": os.path.join(_C, "MUM_IZI18_onay_anahtar.json"),
           "olcekli7": os.path.join(_C, "MUM_IZI18_onay_olcekli.json"), "olay17": os.path.join(_C, "mum_izi17_olay.csv"), "sonuc17": os.path.join(_C, "mum_izi17_sonuc.json"),
           "sonuc13": os.path.join(_C, "mum_izi13_sonuc.json")}
K19_SET7_AD = "MUM_IZI18_ONAY_OLCEKLI"
K19_ZZ = K17_ZAMAN + ("birlikte",)
K19_EK: Dict[str, Any] = {
    "surum": "K19-1.0", "tanim": "MUM_IZI_GOZ GZ_ESIK aynen (ESIK11_SHA) + G2_EK aynen (EK13_SHA) + K17_EK aynen (EK17_SHA): giriş, ufuk 15 mum, stop = bölge dibi x 0,98, "
                                "CETVEL2 konum eşi, dokunma, d5_tum, k17 hücresi, tablolar, permütasyonlar, işaret çevirme",
    "set7": "MUM_IZI18_ONAY_OLCEKLI (s2-13): sayfa -> bölge mühürlü MUM_IZI18_onay_anahtar.json 'yeni_sayfa' (zaman, pazar, sembol, bolge_bas = ilk barın tarihi, bolge_son, "
            "pencere, sinif, katman); işaret cemal_mum_izi18_onay.json (EVET / KISMEN / HAYIR; yildiz true / false); üç dosyada sayfa kümesi ve zaman aynı olmalı (değilse DUR); "
            "yildiz bool olmalı (değilse DUR); mum boyu / olağan / oran MUM_IZI18_onay_olcekli.json'dan aynen (yeniden hesaplanmaz)",
    "birlesik": "set 1-7 (157 bölge); eş dışlama kümesi 157 olayla kurulur; set 1-6 değerleri mum_izi17_olay.csv ile karşılaştırılır (R15, es_R15, fark, n_es, es_neden): "
                "değişen satır sayısı ve en büyük mutlak fark yazılır",
    "gecit": "k17_gecit aynen (gz_olc_bir kapıları; getiri hesaplamaz); hesapta gz_olc ile birebir aynı olmalı (değilse DUR)",
    "tablolar": {"dorduncu_bakis": "yalnız set 7: Cemal sınıfı (EVET / KISMEN / HAYIR) x zaman (haftalık, günlük, birlikte) k17 hücresi (n, n_es, R15 ort / medyan, eş ort, "
                                   "eşli fark ort / medyan, artıda payı, eşinden iyi payı, +%5 / +%10 stop'tan önce payı, stop payı) + gz_tablolar + g2_evet_es; 12 bölgenin "
                                   "dökümü (yıldızlılar işaretli)",
                 "kapi": "BİLGİ: set 7'nin 12 bölgesi Cemal'in işaretinden bağımsız (mum boyu kapısından geçen bölgeler): zaman (haftalık, günlük, birlikte) k17 hücresi; "
                         "ek satır: yıldızlı 2 bölge; karşılaştırma satırı set 6'nın 17 bölgesi aynı ölçülerle",
                 "olcekli": "set 6 + set 7 (29; Cemal sonrasını görmeden yüzde eksenli sayfada işaretledi): Cemal sınıfı (EVET, KISMEN, HAYIR, EVET+KISMEN) x zaman (haftalık, "
                            "günlük, birlikte) k17 hücresi; EVET - HAYIR ve (EVET+KISMEN) - HAYIR eşli fark farkı her zaman diliminde (birlikte dahil): iki örneklem "
                            "permütasyonu (iki yönlü, 10.000, tohum 19), her iki grupta eşli n >= 2 değilse 'karşılaştırma yapılamaz'; R15 farkı bilgi; + gz_tablolar + "
                            "g2_evet_es",
                 "birlesik": "set 1-7 (157): gz_tablolar (MUM_IZI13 / 17 birleşik tablosunun aynısı) + g2_evet_es + k17 hücresi + duyarlılık (son işaret); MUM_IZI17 birleşiği "
                             "(mum_izi17_sonuc.json) ile fark: karşılaştırma satırları, EVET - eş, hücre n / R15 / eşli fark",
                 "yon": "k19_yon: dördüncü bakış önceki üç bakışla aynı yönde mi (EVET - HAYIR eşli fark farkı ve EVET - eş İŞARETİ; dilim başına); DÜZELTME (EK 17 HATA): bir "
                        "değer ancak ilgili her grupta eşli n >= 2 ise kullanılır (EVET - HAYIR: n_es_a ve n_es_b >= 2; EVET - eş: n_es >= 2), değilse 'karşılaştırma yapılamaz'; "
                        "önceki bakışların değerleri de aynı korumayla okunur (üçüncü bakış günlük EVET n 1 -> yapılamaz); k17_yon ve mum_izi17_sonuc.json değişmez"},
    "karsilastirma": {"n_min": 2, "perm": 10000, "tohum": 19},
    "etiket": "BİLGİ; ÖRNEKLEM YETERSİZ (set 7 ve set 6+7 hücrelerinin hepsi n < 30)",
    "es_siniri": "eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240): aynı gün aynı kova konum eşi",
    "pdf": "MUM_IZI17_SONRASI düzeni (k17_sayfa aynen): kapakta düz dil özet tablo (set 7 Cemal sınıfı x zaman; set 6+7 Cemal sınıfı x zaman) + kapı / set 6+7 farkı / "
           "birleşik birer satır; sonra 12 bölgenin hepsi: BENZİYOR (yıldızlılar önce), KISMEN, BENZEMİYOR (her sınıfta önce haftalık, sonra bölge sonu sırası); yıldızlı "
           "sayfada 'yıldız koydun' satırı",
}
K19_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü aynı kova (CETVEL2 v2.2 konum eşi) aynı takvim aralığı aynı stop geometrisi (GZ aynen); eş dışlama 157 olayla; sınır: eşler bölgenin "
                   "kendi koşusuyla eşlenmedi (Ç229 / Ç240)"),
    "K2": ("EVET", "Cemal set 7'yi sonrasını görmeden işaretledi (ölçekli sayfa bölge sonunda kesik); işaret dosyası commit 5068fa8, bu ön kayıt set 7 getirilerinden önce; "
                   "giriş bölgeden SONRAKİ barın açılışı; veri <= 2022-12-31 + KASA kapısı"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0); haftalık barlar tamamlanmış ISO haftaları (MH / MV aynen)"),
    "K4": ("EVET", "157 tekil bölge (zaman + sembol + bölge sonu; k19_ornek DUR); set 7'nin önceki setlerle ortak sembolü sayılıp yazılır"),
    "K5": ("EVET", "giriş = bölgeden sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk günü); giriş <= stop olay ölçülmez (sayısı yazılır)"),
    "K6": ("EVET", "MI bölünme düzeltmeli fiyatlar (GZ aynen); getiriler oransal; ABD USD, AVR yerel para, BIST TL; pazarlar arası karşılaştırma eşli farkla"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz"),
    "K8": ("EVET", "set 7 hücreleri n 0-5, set 6+7 hücreleri n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ'; eşli n < 2 'karşılaştırma yapılamaz' (yön satırında da); 12 bölge "
                   "tek tek listeli; tek dönem (<= 2022), BH yok (karar yok)"),
    "K9": ("EVET", "MUM_IZI19_ON_KAYIT.md: KOD19 / EK19 / EK17 / EK13 / ESIK11 / işaret / anahtar / ölçekli / olay17 / sonuç17 sha + getirisiz sayımlar; set 7 getirilerinden "
                   "önce commit + push; k19_kapi sha + commit + temiz ağaç + IZ_KARNE.ik_kontrol_kapisi"),
    "K10": ("EVET", "işaret şeması GZ.gz_isaret_oku (bilinmeyen değer DUR) + yildiz bool (DUR); üç set 7 dosyasında sayfa kümesi ve zaman aynı (DUR); bölge başı veriden "
                    "yeniden hesaplanıp anahtarla denetlenir (k17_gecit)"),
    "K11": ("EVET", "getirisiz geçit hesapta gz_olc ile birebir (DUR); haftalık +%10 k17 dokunma fonksiyonuyla GZ d10'a eşit (DUR); set 1-6 satırları mum_izi17_olay.csv ile "
                    "karşılaştırılır; >= 2 hücre olay csv'sinden bağımsız kodla yeniden üretilir (rapor öncesi, test_mum_izi19)"),
    "K12": ("EVET", "'iz / tuttu / anlamlı' sözü yok; sayı ile yorum ayrı; n < 30 'örneklem yetersiz'"),
    "K13": ("EVET", "çakışma kapısı korunur; çalışan fonksiyonlar değişmez (test_mum_izi19 ast karşılaştırması, f218598'e göre); yasak defter / mühürlü dosyalara dokunulmaz; "
                    "yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez"),
}


def _k19_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or G2_YOL["cikti"], K19_DOSYA[ad])


def k19_ek_sha() -> str:
    return hashlib.sha256(json.dumps(K19_EK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


# ---------------------------------------------------------------- örneklem
def k19_set7() -> pd.DataFrame:
    """Set 7: sayfa -> bölge (mühürlü anahtar), işaret + yıldız (Cemal), mum boyu (ölçekli json). k17_set6 ile aynı denetimler + yıldız şeması."""
    E = GZ.gz_isaret_oku(K19_YOL["isaret7"]); EJ = json.load(open(K19_YOL["isaret7"], encoding="utf-8"))["sayfalar"]
    A = json.load(open(K19_YOL["anahtar7"], encoding="utf-8"))["sayfalar"]; B = {int(s["yeni_sayfa"]): s for s in json.load(open(K19_YOL["olcekli7"], encoding="utf-8"))["sayfalar"]}
    pa = {int(r["yeni_sayfa"]) for r in A}
    if pa != set(E) or pa != set(B) or len(pa) != len(A):
        raise G2Hata(f"K10: set 7 sayfa kümeleri uyuşmuyor (anahtar {sorted(pa)}, işaret {sorted(E)}, ölçekli {sorted(B)})")
    rows = []
    for r in A:
        pg = int(r["yeni_sayfa"]); b = B[pg]; ej = EJ[str(pg)]; ez = ej.get("zaman")
        if b.get("zaman") != r["zaman"] or (ez is not None and ez != r["zaman"]):
            raise G2Hata(f"K10: set 7 sayfa {pg} zaman uyuşmuyor ({r['zaman']}, {b.get('zaman')}, {ez})")
        if not isinstance(ej.get("yildiz"), bool):
            raise G2Hata(f"K10: set 7 sayfa {pg} yildiz bool değil ({ej.get('yildiz')!r})")
        rows.append({"set": "set7", "set_ad": K19_SET7_AD, "sayfa": pg, "isaret": E[pg], "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "tarih": r["bolge_son"],
                     "m": int(r["pencere"]), "bolge_bas_anahtar": r["bolge_bas"], "hakem_sinif": r.get("sinif"), "hakem_karar": r.get("hakem_karar"),
                     "hakem2_karar": r.get("hakem2_karar"), "boy_mutlak": b.get("boy_mutlak"), "boy_onceki": b.get("onceki"), "boy_onceki_n": b.get("onceki_n"),
                     "boy_oran": b.get("oran"), "yildiz": bool(ej["yildiz"]), "katman": r.get("katman")})
    X = pd.DataFrame(rows)
    for c in ("boy_mutlak", "boy_onceki", "boy_oran"):
        X[c] = pd.to_numeric(X[c], errors="coerce")
    X["sinif"] = np.where(X.isaret.isin(GZ.SINIF), X.isaret, None); X["sinif_son"] = X["sinif"]
    return X[X.sinif.notna()].reset_index(drop=True)


def k19_ornek() -> pd.DataFrame:
    X = pd.concat([k17_ornek(), k19_set7()], ignore_index=True)
    if X.duplicated(["zaman", "sembol", "tarih"]).any():
        raise G2Hata("K4: aynı bölge iki kez (set 1-7)")
    X["yildiz"] = X["yildiz"].fillna(False).astype(bool) if "yildiz" in X else False
    return X


def k19_sembol_tekrar(X: pd.DataFrame) -> Dict[str, Any]:
    s7 = X[X.set == "set7"]; once = X[X.set != "set7"]
    ort = sorted(set(s7.sembol) & set(once.sembol))
    return {"set7_onceki_setlerle_ortak_sembol": ort, "n": len(ort)}


def k19_sayim(G: pd.DataFrame) -> Dict[str, Any]:
    """GETİRİSİZ sayım (k17_sayim'in küme sayımı aynen): set 7, set 6+7, birleşik 1-7; yıldız ve hakem sınıfı (set 7)."""
    def bir(g: pd.DataFrame) -> Dict[str, Any]:
        return k17_sayim(g)["birlesik"]
    s7 = G[G.set == "set7"]
    return {"set7": bir(s7), "set6_7": bir(G[G.set.isin(["set6", "set7"])]), "birlesik": bir(G),
            "set7_yildiz": {f"{s}|{z}": int(((s7.sinif == s) & (s7.zaman == z) & s7.yildiz.astype(bool)).sum()) for s in GZ.SINIF for z in K17_ZAMAN},
            "set7_hakem_sinif": s7.hakem_sinif.value_counts().to_dict(), "set7_katman": s7.katman.value_counts().to_dict()}


# ---------------------------------------------------------------- tablolar
def k19_karsilastir(a: pd.DataFrame, b: pd.DataFrame) -> Dict[str, Any]:
    """İki grup eşli fark farkı; her iki grupta eşli n >= 2 değilse 'karşılaştırma yapılamaz'; permütasyon GZ.gz_perm (10.000, tohum 19)."""
    C = K19_EK["karsilastirma"]
    oa = a[a.olculdu.astype(bool)]; ob = b[b.olculdu.astype(bool)]
    fa = oa.fark.astype(float).to_numpy(); fb = ob.fark.astype(float).to_numpy(); fa = fa[np.isfinite(fa)]; fb = fb[np.isfinite(fb)]
    Ra = oa.R15.astype(float).to_numpy(); Rb = ob.R15.astype(float).to_numpy(); Ra = Ra[np.isfinite(Ra)]; Rb = Rb[np.isfinite(Rb)]
    out: Dict[str, Any] = {"n_a": int(len(Ra)), "n_b": int(len(Rb)), "n_es_a": int(len(fa)), "n_es_b": int(len(fb))}
    if len(fa) < C["n_min"] or len(fb) < C["n_min"]:
        out.update({"esli_fark_fark": None, "esli_p": None, "durum": "karşılaştırma yapılamaz"})
    else:
        out.update({"esli_fark_fark": float(fa.mean() - fb.mean()), "esli_p": GZ.gz_perm(fa, fb, C["perm"], C["tohum"]), "durum": "hesaplandı"})
    out["R15_fark_bilgi"] = float(Ra.mean() - Rb.mean()) if len(Ra) and len(Rb) else None
    return out


def _k19_zs(D: pd.DataFrame, z: str) -> pd.DataFrame:
    return D if z == "birlikte" else D[D.zaman == z]


def k19_tablolar(Y: pd.DataFrame) -> Dict[str, Any]:
    Y7 = Y[Y.set == "set7"]; Y6 = Y[Y.set == "set6"]; Y67 = Y[Y.set.isin(["set6", "set7"])]; zs = _k19_zs
    gr = (("EVET", ["EVET"]), ("KISMEN", ["KISMEN"]), ("HAYIR", ["HAYIR"]), ("EVET+KISMEN", ["EVET", "KISMEN"]))
    dr = {f"{s}|{z}": k17_hucre(zs(Y7[Y7.sinif == s], z)) for s in GZ.SINIF for z in K19_ZZ}
    kp = {f"set7|{z}": k17_hucre(zs(Y7, z)) for z in K19_ZZ}
    kp.update({f"set7_yildiz|{z}": k17_hucre(zs(Y7[Y7.yildiz.astype(bool)], z)) for z in K19_ZZ})
    kp.update({f"set6|{z}": k17_hucre(zs(Y6, z)) for z in K19_ZZ})
    oh = {f"{s}|{z}": k17_hucre(zs(Y67[Y67.sinif.isin(sl)], z)) for s, sl in gr for z in K19_ZZ}
    ok = {f"{ad}|{z}": k19_karsilastir(zs(Y67[Y67.sinif.isin(sl)], z), zs(Y67[Y67.sinif == "HAYIR"], z))
          for ad, sl in (("EVET-HAYIR", ["EVET"]), ("(EVET+KISMEN)-HAYIR", ["EVET", "KISMEN"])) for z in K19_ZZ}
    bk = {f"{s}|{z}": k17_hucre(zs(Y[Y.sinif.isin(sl)], z)) for s, sl in gr for z in K19_ZZ}
    return {"dorduncu_bakis": {"hucre": dr, "gz": GZ.gz_tablolar(Y7), "evet_es": g2_evet_es(Y7)}, "kapi": kp,
            "olcekli": {"hucre": oh, "karsilastirma": ok, "gz": GZ.gz_tablolar(Y67), "evet_es": g2_evet_es(Y67)},
            "birlesik": {"tablo": GZ.gz_tablolar(Y), "evet_es": g2_evet_es(Y), "k17_hucre": bk, "duyarlilik_son_isaret": GZ.gz_tablolar(Y, "sinif_son")["karsilastirma"]}}


def k19_dokum(Y: pd.DataFrame) -> List[Dict[str, Any]]:
    Y7 = Y[Y.set == "set7"].copy(); Y7["_s"] = Y7.sinif.map({s: i for i, s in enumerate(GZ.SINIF)}); Y7["_z"] = Y7.zaman.map({"haftalik": 0, "gunluk": 1})
    Y7["_y"] = (~Y7.yildiz.astype(bool)).astype(int)
    kol = ["sayfa", "isaret", "yildiz", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "m", "olculdu", "neden", "R15", "es_R15", "n_es", "fark", "max15", "min15",
           "stop15", "d5_tum", "d10", "R30", "boy_mutlak", "boy_onceki", "boy_oran", "hakem_sinif", "katman"]
    return [{k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in r.items()}
            for r in Y7.sort_values(["_s", "_y", "_z", "bolge_son"])[kol].to_dict("records")]


def _k19_kv(K: Dict[str, Any], key: str) -> Optional[float]:
    """EVET - HAYIR eşli fark farkı: yalnız iki grupta da eşli n >= 2 ise (EK 17 HATA düzeltmesi)."""
    c = K.get(key) or {}; n0 = K19_EK["karsilastirma"]["n_min"]
    return c.get("esli_fark_fark") if (c.get("n_es_a") or 0) >= n0 and (c.get("n_es_b") or 0) >= n0 else None


def _k19_ev(E: Dict[str, Any], key: str) -> Optional[float]:
    c = E.get(key) or {}
    return c.get("esli_fark_ort") if (c.get("n_es") or 0) >= K19_EK["karsilastirma"]["n_min"] else None


def k19_yon(T: Dict[str, Any], J13: Dict[str, Any], J17: Dict[str, Any]) -> Dict[str, Any]:
    """Dördüncü bakış önceki üç bakışla aynı yönde mi; her değer n >= 2 korumasıyla (k17_yon'un düzeltilmiş hali; k17_yon değişmez)."""
    out = {}
    for z in K17_ZAMAN:
        kk = f"EVET-HAYIR|{z}"; ke = f"EVET-es|{z}"
        sat = {"EVET-HAYIR_esli": {"ilk": _k19_kv(J13["ilk_bakis"]["tablo"]["karsilastirma"], kk), "ikinci": _k19_kv(J13["ikinci_bakis"]["tablo"]["karsilastirma"], kk),
                                   "ucuncu": _k19_kv(J17["ucuncu_bakis"]["gz"]["karsilastirma"], kk), "dorduncu": _k19_kv(T["dorduncu_bakis"]["gz"]["karsilastirma"], kk)},
               "EVET-es": {"ilk": _k19_ev(J13["ilk_bakis_evet_es"], ke), "ikinci": _k19_ev(J13["ikinci_bakis"]["evet_es"], ke),
                           "ucuncu": _k19_ev(J17["ucuncu_bakis"]["evet_es"], ke), "dorduncu": _k19_ev(T["dorduncu_bakis"]["evet_es"], ke)}}
        for ad, r in sat.items():
            v4 = r["dorduncu"]
            for o in ("ilk", "ikinci", "ucuncu"):
                r[f"{o}le_ayni_yon"] = None if (v4 is None or r[o] is None) else bool(np.sign(v4) == np.sign(r[o]))
            r["durum"] = "karşılaştırma yapılamaz" if v4 is None else "hesaplandı"
        out[z] = sat
    return out


def k19_fark17(J17: Dict[str, Any], T: Dict[str, Any]) -> Dict[str, Any]:
    """MUM_IZI17 birleşik (145) -> MUM_IZI19 birleşik (157)."""
    a = J17["birlesik"]; b = T["birlesik"]; out: Dict[str, Any] = {"karsilastirma": {}, "evet_es": {}, "hucre": {}}
    for k, v in b["tablo"]["karsilastirma"].items():
        o = a["tablo"]["karsilastirma"].get(k, {})
        out["karsilastirma"][k] = {"esli_fark_fark_17": o.get("esli_fark_fark"), "esli_fark_fark_19": v.get("esli_fark_fark"), "esli_p_17": o.get("esli_p"), "esli_p_19": v.get("esli_p")}
    for k, v in b["evet_es"].items():
        o = a["evet_es"].get(k, {})
        out["evet_es"][k] = {"ort_17": o.get("esli_fark_ort"), "ort_19": v.get("esli_fark_ort"), "p_17": o.get("p"), "p_19": v.get("p"), "n_17": o.get("n_es"), "n_19": v.get("n_es")}
    for k, v in b["tablo"]["hucre"].items():
        if k.endswith("|BIST"):
            continue
        o = a["tablo"]["hucre"].get(k, {})
        out["hucre"][k] = {"n_17": o.get("n"), "n_19": v.get("n"), "R15_ort_17": o.get("R15_ort"), "R15_ort_19": v.get("R15_ort"), "fark_ort_17": o.get("fark_ort"),
                           "fark_ort_19": v.get("fark_ort")}
    return out


def k19_onceki_farki(Oe: pd.DataFrame, Oy: pd.DataFrame, yeni_set: str = "set7") -> Dict[str, Any]:
    """Önceki koşunun satırları (Oe) yeni koşuda (Oy, yeni set hariç) aynı mı: R15, es_R15, fark, n_es (+ es_neden)."""
    M = Oe.merge(Oy[Oy.set != yeni_set], on=["set", "sayfa"], suffixes=("_e", "_y")); fk = {}; en = {}
    for c in ("R15", "es_R15", "fark", "n_es"):
        a = M[f"{c}_e"].to_numpy(float); b = M[f"{c}_y"].to_numpy(float); ayni = np.isclose(a, b, atol=1e-9) | (np.isnan(a) & np.isnan(b))
        fk[c] = int((~ayni).sum()); d = np.abs(a - b); d = d[~ayni & np.isfinite(d)]; en[c] = float(d.max()) if len(d) else 0.0
    nd = int((M.es_neden_e.fillna("") != M.es_neden_y.fillna("")).sum()) if "es_neden_e" in M else None
    deg = ~(np.isclose(M.fark_e.to_numpy(float), M.fark_y.to_numpy(float), atol=1e-9) | (M.fark_e.isna() & M.fark_y.isna())) | \
        ~(np.isclose(M.es_R15_e.to_numpy(float), M.es_R15_y.to_numpy(float), atol=1e-9) | (M.es_R15_e.isna() & M.es_R15_y.isna()))
    return {"satir": int(len(M)), "beklenen": int(len(Oe)), "farkli": fk, "en_buyuk_mutlak_fark": en, "es_neden_degisen": nd,
            "degisen_satirlar": M[deg][["set", "sayfa", "sembol_e", "n_es_e", "n_es_y", "es_R15_e", "es_R15_y", "fark_e", "fark_y"]].to_dict("records")}


# ---------------------------------------------------------------- kapı, ön kayıt, koşu
def k19_sha_simdi() -> Dict[str, str]:
    return {"KOD19_SHA": MI._mi_sha(G2_YOL["kod"]), "EK19_SHA": k19_ek_sha(), "EK17_SHA": k17_ek_sha(), "EK13_SHA": g2_ek_sha(), "GZ_KOD_SHA": MI._mi_sha(GZ.GZ_YOL["kod"]),
            "ESIK11_SHA": GZ.gz_esik_sha(), "ISARET_SET7_SHA": MI._mi_sha(K19_YOL["isaret7"]), "ANAHTAR_SET7_SHA": MI._mi_sha(K19_YOL["anahtar7"]),
            "OLCEKLI_SET7_SHA": MI._mi_sha(K19_YOL["olcekli7"]), "ISARET_SET6_SHA": MI._mi_sha(K17_YOL["isaret6"]), "ANAHTAR_SET6_SHA": MI._mi_sha(K17_YOL["anahtar6"]),
            "OLAY17_SHA": MI._mi_sha(K19_YOL["olay17"]), "SONUC17_SHA": MI._mi_sha(K19_YOL["sonuc17"]), "SONUC13_SHA": MI._mi_sha(K19_YOL["sonuc13"])}


def k19_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    yol = _k19_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise G2Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = k19_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise G2Hata(f"ön kayıt 19 kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_G2); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise G2Hata("ön kayıt 19 commit'li değil -> DURDU")
    gir = [os.path.relpath(v, KOK_G2) for v in list(K19_YOL.values()) + list(K17_YOL.values())]
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_GOZ2.py", "MUM_IZI_GOZ.py"] + gir):
        raise G2Hata("ön kayıt / kod / girdiler çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def _k19_tablo_md(s: Dict[str, Any]) -> List[str]:
    t = ["| Cemal | haftalık (ölçülebilen) | günlük (ölçülebilen) |", "|---|---|---|"]
    for c in GZ.SINIF:
        t.append(f"| {K17_AD[c]} | {s['sinif_zaman'][f'{c}|haftalik']} ({s['sinif_zaman_olculebilir'][f'{c}|haftalik']}) | "
                 f"{s['sinif_zaman'][f'{c}|gunluk']} ({s['sinif_zaman_olculebilir'][f'{c}|gunluk']}) |")
    return t


def k19_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    y = _k19_yol("onkayit", cikti)
    if os.path.exists(y):
        raise G2Hata("ön kayıt 19 zaten var")
    X = k19_ornek(); G = k17_gecit(X); S = k19_sayim(G); sh = k19_sha_simdi(); st = k19_sembol_tekrar(X)
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in K19_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_GOZ2.py"])

    def sat(ad_: str, s: Dict[str, Any]) -> str:
        return (f"{ad_}: {s['toplam']} bölge, ölçülebilen {s['olculebilir']}, ölçülemeyen {s['toplam'] - s['olculebilir']} {json.dumps(s['olculemedi'], ensure_ascii=False)}; "
                f"pazar {json.dumps(s['pazar'], ensure_ascii=False)}; en geç 15. mum {s['en_gec_15_mum']}.")
    s7 = S["set7"]
    s = [f"# MUM_IZI19 ÖN KAYIT ({MI._mi_simdi()})", "",
         "MUM_IZI11 / 13 / 17 ön kayıtlarının tanımları AYNEN (MUM_IZI_GOZ.py GZ_ESIK: ESIK11_SHA; G2_EK: EK13_SHA; K17_EK: EK17_SHA): giriş = bölgeden sonraki ilk geçerli barın "
         "açılışı; ufuk 15 mum; stop = bölge dibi x 0,98; dokunma; R30; CETVEL2 konum eşi; d5_tum; tablolar; permütasyonlar. Ek: set 7 = MUM_IZI18_ONAY_OLCEKLI 12 bölge (mum "
         "boyu kapısından geçen bölgeler; Cemal sonrasını görmeden, yüzde eksenli sayfada işaretledi; iki yıldız). Bu dosya set 7'nin getirileri hesaplanmadan ÖNCE commit "
         "edilir; getirisiz sayımlar aşağıda.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_GOZ2.py commit'i: {kc or 'yok'}", "",
         "## GETİRİSİZ SAYIM (getiri hesaplanmadı; yalnız işaret, zaman, veri kapıları)", "",
         sat("Set 7", s7) + f" Hakem sınıfı {json.dumps(S['set7_hakem_sinif'], ensure_ascii=False)}; katman {json.dumps(S['set7_katman'], ensure_ascii=False)}; yıldız "
         f"{json.dumps({k: v for k, v in S['set7_yildiz'].items() if v}, ensure_ascii=False)}.", "", *_k19_tablo_md(s7), "",
         sat("Set 6 + 7 (gerçek ölçekle işaretlenenler)", S["set6_7"]), "", *_k19_tablo_md(S["set6_7"]), "",
         sat("Birleşik set 1-7", S["birlesik"]), "", *_k19_tablo_md(S["birlesik"]), "",
         f"- Set 7'nin önceki setlerle ortak sembolü: {st['n']} {st['set7_onceki_setlerle_ortak_sembol']} (bölge tekrarı yok: zaman + sembol + bölge sonu tekil, denetlendi).",
         "- Eş sayısı (eşi < 5 / kovasız) hesapta belirlenir ve yazılır; eşsiz olay eşli tabloya girmez (GZ aynen).",
         "- Set 7 haftalık yalnız 1 bölge (BENZİYOR, yıldızlı): haftalık hücreler 'yalnız döküm'; haftalık karşılaştırma yapılamaz. Günlük BENZİYOR 5 / BENZEMİYOR 4 / KISMEN 2.", "",
         "## Tablolar (önceden; sonuçtan sonra değişmez)", "",
         "- (i) DÖRDÜNCÜ BAKIŞ = yalnız set 7: Cemal sınıfı x zaman (haftalık, günlük, birlikte): n, R15 ort / medyan, eş ort, eşli fark ort / medyan, artıda payı, eşinden iyi "
         "payı, +%5 / +%10 stop'tan önce payı, stop payı (k17 hücresi) + GZ tabloları + EVET - eş (işaret çevirme). 12 bölgenin dökümü (sayfa, işaret, yıldız, zaman, sembol, "
         "R15, eş ort, mum boyu %, oran); yıldızlı iki bölge işaretli.",
         "- (ii) KAPIDAN GEÇENLER (BİLGİ): set 7'nin 12 bölgesi Cemal'in işaretinden bağımsız ('mumları belirgin küçük bölgeler eşlerinden iyi gitti mi'): aynı ölçüler, "
         "zaman dilimine göre ve birlikte; ek satır yıldızlı 2; karşılaştırma satırı set 6'nın 17 bölgesi.",
         "- (iii) GERÇEK ÖLÇEKLE İŞARETLENENLER = set 6 + set 7 (29): Cemal sınıfı (ve BENZİYOR + KISMEN) x zaman (haftalık, günlük, birlikte); BENZİYOR - BENZEMİYOR ve "
         "(BENZİYOR + KISMEN) - BENZEMİYOR eşli fark farkı, iki örneklem permütasyonu (iki yönlü, 10.000, tohum 19); iki grupta eşli n >= 2 değilse 'karşılaştırma yapılamaz'.",
         "- (iv) BİRLEŞİK = set 1-7 (157): MUM_IZI17 birleşik tablosunun aynısı (GZ tabloları, EVET - eş, k17 hücresi, duyarlılık) + MUM_IZI17 birleşiğine göre değişim.",
         "- YÖN (k19_yon): dördüncü bakış önceki üç bakışla aynı yönde mi (EVET - HAYIR eşli ve EVET - eş İŞARETİ). DÜZELTME (EK 17 HATA): her değer ancak ilgili her grupta "
         "eşli n >= 2 ise kullanılır; değilse 'karşılaştırma yapılamaz'. k17_yon ve mum_izi17_sonuc.json değişmez.",
         "- Set 1-6 satırları mum_izi17_olay.csv ile karşılaştırılır (R15, es_R15, fark, n_es, es_neden): eş dışlama kümesi 157 olayla kurulduğu için eş değerleri değişebilir; "
         "değişen satır sayısı ve en büyük fark yazılır.",
         "- OKUMA: set 7 ve set 6 + 7 hücrelerinin hepsi n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ'. Eş sınırı: eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240).", "",
         "## Ek tanımlar (K19_EK; sha yukarıda)", "", "```", json.dumps(K19_EK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ (`python IZ_KARNE.py kontrol`; K8: set 7 ve set 6 + 7 hücreleri n < 30)", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 19")


K19_KOL = K17_KOL + ["yildiz", "katman"]


def k19_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    t0 = time.time(); cikti = cikti or G2_YOL["cikti"]
    if os.path.exists(_k19_yol("sonuc", cikti)):
        raise G2Hata("sonuç 19 zaten var")
    G0 = k19_kapi(cikti)
    kasa = KS.kasa_kapisi([os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] +
                          [os.path.join(MH.MH_YOL["tam"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")],
                          "2022-12-31")
    X = k19_ornek(); Gt = k17_gecit(X)
    Y = GZ.gz_es(GZ.gz_olc(X))
    if not (Y.olculdu.astype(bool).to_numpy() == Gt.olculebilir.astype(bool).to_numpy()).all() or \
            not (Y.neden.fillna("").to_numpy() == Gt.neden.fillna("").to_numpy()).all():
        raise G2Hata("K11: getirisiz geçit ile gz_olc uyuşmuyor")
    Y = k17_d5(Y).sort_values(["set", "sayfa"]).reset_index(drop=True)
    for c in K19_KOL:
        if c not in Y:
            Y[c] = np.nan
    O = Y[K19_KOL].copy()
    for c in ("bolge_bas", "bolge_son", "giris", "son15"):
        O[c] = pd.to_datetime(O[c]).dt.strftime("%Y-%m-%d")
    O.to_csv(_k19_yol("olay", cikti), index=False, float_format="%.6f")
    O19 = pd.read_csv(_k19_yol("olay", cikti)); O17 = pd.read_csv(K19_YOL["olay17"])
    J13 = json.load(open(K19_YOL["sonuc13"], encoding="utf-8")); J17 = json.load(open(K19_YOL["sonuc17"], encoding="utf-8")); T = k19_tablolar(O)
    Y7 = O[O.set == "set7"]; Y67 = O[O.set.isin(["set6", "set7"])]
    J = {"surum": K19_SURUM, "kapi": G0, "kasa": kasa, "sayim": k19_sayim(Gt), "sembol_tekrar": k19_sembol_tekrar(X),
         "es_yok": {k: D[D.olculdu.astype(bool)].es_neden.fillna("").replace("", "var").value_counts().to_dict() for k, D in (("set7", Y7), ("set6_7", Y67), ("birlesik", O))},
         "set1_6_mum_izi17_farki": k19_onceki_farki(O17, O19), **T, "dokum_set7": k19_dokum(O), "yon": k19_yon(T, J13, J17), "mum_izi17_birlesik_farki": k19_fark17(J17, T),
         "etiket": K19_EK["etiket"], "es_siniri": K19_EK["es_siniri"], "olay_sha": MI._mi_sha(_k19_yol("olay", cikti)), "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_k19_yol("sonuc", cikti), J, "sonuç 19")
    return J


# ---------------------------------------------------------------- PDF
def k19_pdf(cikti: Optional[str] = None, olay: Optional[pd.DataFrame] = None, sonuc: Optional[Dict[str, Any]] = None, yol: Optional[str] = None) -> str:
    """MUM_IZI19_SONRASI.pdf (k17_pdf düzeni; sayfalar k17_sayfa aynen + yıldız satırı). olay / sonuc / yol verilirse dosyalar okunmaz (deneme basımı)."""
    import textwrap
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    cikti = cikti or G2_YOL["cikti"]; y = yol or _k19_yol("pdf", cikti)
    if olay is None:
        J = json.load(open(_k19_yol("sonuc", cikti), encoding="utf-8"))
        if MI._mi_sha(_k19_yol("olay", cikti)) != J["olay_sha"]:
            raise G2Hata("olay csv'si sonuç 19 json'uyla uyuşmuyor")
        O = pd.read_csv(_k19_yol("olay", cikti))
    else:
        O, J = olay, sonuc
    D4 = J["dorduncu_bakis"]["hucre"]; KP = J["kapi"]; OH = J["olcekli"]["hucre"]; OK = J["olcekli"]["karsilastirma"]; BK = J["birlesik"]["k17_hucre"]
    BKK = J["birlesik"]["tablo"]["karsilastirma"]; Vc: Dict[Any, Any] = {}; zad = {"haftalik": "haftalık", "gunluk": "günlük", "birlikte": "ikisi"}

    def puan(v: Optional[float]) -> str:
        return "-" if v is None or not np.isfinite(v) else f"{v * 100:+.1f} puan".replace(".", ",")

    def p_yaz(p: Optional[float]) -> str:
        return "-" if p is None else f"{p:.2f}".replace(".", ",")

    def satirlar(H: Dict[str, Any], zl: Tuple[str, ...]) -> List[List[str]]:
        sat = []
        for z in zl:
            for s in GZ.SINIF:
                c = H[f"{s}|{z}"]; n = c.get("n", 0); ne = c.get("n_es", 0)
                if not n:
                    continue
                sat.append([K17_AD[s], zad[z], str(n), _k17_pay(c.get("arti_pay"), n), _k17_yuzde(c.get("R15_ort")), _k17_yuzde(c.get("R15_med")), _k17_yuzde(c.get("es_ort")),
                            _k17_pay(c.get("esinden_iyi_pay"), ne), _k17_pay(c.get("d5_pay"), n), _k17_pay(c.get("stop_pay"), n)])
        return sat

    def tablo(y0: float, baslik: str, sat: List[List[str]]) -> float:
        fig.text(0.05, y0, baslik, fontsize=11, weight="bold"); h = 0.03 * (len(sat) + 1)
        ax = fig.add_axes([0.02, y0 - 0.012 - h, 0.96, h]); ax.axis("off")
        tb = ax.table(cellText=sat, colLabels=["senin\nişaretin", "mum", "bölge", "artıda\nkapanan", "ortalama", "medyan", "eşlerin\nort.", "eşinden\niyi",
                                               "+%5'e\nstop'tan önce", "stop\nolan"], loc="upper center", cellLoc="center",
                      colWidths=[0.13, 0.09, 0.06, 0.09, 0.1, 0.1, 0.09, 0.09, 0.13, 0.08], bbox=[0, 0, 1, 1])
        tb.auto_set_font_size(False); tb.set_fontsize(9.5)
        return y0 - 0.012 - h - 0.03

    def sat_yaz(c: Dict[str, Any]) -> str:
        return (f"{c.get('n', 0)} bölge, ortalama {_k17_yuzde(c.get('R15_ort'))}, eşlerinden {puan(c.get('fark_ort'))}, eşinden iyi "
                f"{_k17_pay(c.get('esinden_iyi_pay'), c.get('n_es', 0))}")

    def fark_yaz(c: Dict[str, Any]) -> str:
        return "karşılaştırma yapılamaz" if c.get("esli_fark_fark") is None else f"{puan(c['esli_fark_fark'])} (p {p_yaz(c.get('esli_p'))})"
    n7 = int((O.set == "set7").sum())
    with PdfPages(y, metadata={"Title": "MUM_IZI19 sonrası", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7))
        fig.text(0.05, 0.96, f"Son {n7} bölge (mumları belirgin küçük): işaretlerin sonrasında ne yaptı", fontsize=14, weight="bold")
        fig.text(0.05, 0.937, "Giriş: bölgeden sonraki ilk mumun açılışı. 15 mum sonraki kapanışla getiri. Eş: aynı gün, benzer oynaklık ve likiditedeki hisseler.",
                 fontsize=9)
        yy = tablo(0.91, f"Bu {n7} bölge", satirlar(D4, K17_ZAMAN))
        yy = tablo(yy, f"Yüzde eksenli iki set birlikte (önceki 17 + bu {n7} = {int(O.set.isin(['set6', 'set7']).sum())} bölge)", satirlar(OH, K17_ZAMAN))
        sat2 = [f"Bu {n7} bölgenin hepsi (işaretinden bağımsız): {sat_yaz(KP['set7|birlikte'])}. Yıldız koyduğun 2: {sat_yaz(KP['set7_yildiz|birlikte'])}.",
                f"{int(O.set.isin(['set6', 'set7']).sum())} bölgede BENZİYOR - BENZEMİYOR (eşlerine göre): günlük {fark_yaz(OK['EVET-HAYIR|gunluk'])}; haftalık {fark_yaz(OK['EVET-HAYIR|haftalik'])}; "
                f"ikisi birlikte {fark_yaz(OK['EVET-HAYIR|birlikte'])}.",
                f"Bütün bölgeler ({int(len(O))}): haftalık BENZİYOR {sat_yaz(BK['EVET|haftalik'])}; BENZEMİYOR {sat_yaz(BK['HAYIR|haftalik'])}.",
                f"Günlük BENZİYOR {sat_yaz(BK['EVET|gunluk'])}; BENZEMİYOR {sat_yaz(BK['HAYIR|gunluk'])}; fark {fark_yaz(BKK['EVET-HAYIR|gunluk'])}."]
        for s_ in sat2:
            w = textwrap.fill(s_, 95); fig.text(0.05, yy, w, fontsize=9.5, va="top", linespacing=1.4); yy -= 0.019 * (w.count("\n") + 1) + 0.013
        fig.text(0.05, yy - 0.01, "Sayılar çok az (N < 30): bu bir sonuç değil, bilgi.", fontsize=13, weight="bold")
        fig.text(0.05, yy - 0.055, f"Sonraki sayfalar: {n7} bölgenin hepsi; önce BENZİYOR (yıldızlılar önce), sonra KISMEN, sonra BENZEMİYOR.\n"
                 "Hisse ve tarih açık. Sağdaki eksen girişe göre yüzde (0 = giriş fiyatı).\nAltta bölgedeki gerçek mum boyu ve bu hissenin olağanına oranı "
                 "(1'den küçük = mumlar olağandan küçük).", fontsize=9.5, va="top", linespacing=1.5)
        pdf.savefig(fig); plt.close(fig)
        X = O[O.set == "set7"].copy(); X["_s"] = X.sinif.map({s: i for i, s in enumerate(GZ.SINIF)}); X["_z"] = X.zaman.map({"haftalik": 0, "gunluk": 1})
        X["_y"] = (~X.yildiz.astype(bool)).astype(int)
        for r in X.sort_values(["_s", "_y", "_z", "bolge_son"]).itertuples():
            k = (r.zaman, r.pazar)
            if k not in Vc:
                Vc[k] = MV.mv_veri(*k)
            fig = plt.figure(figsize=(8.3, 11.7)); k17_sayfa(fig, r, Vc[k][r.sembol])
            if bool(r.yildiz):
                fig.text(0.62, 0.957, "★ yıldız koydun", fontsize=15, weight="bold", color="#b8860b")
            pdf.savefig(fig); plt.close(fig)
    return y


# ================================================================ 4f) MUM_IZI EK 21: BEŞİNCİ BAKIŞ (set 8 = MUM_IZI20 katmanlı onay seti, 24 bölge) + kapıdan geçenler (set 7+8)
#                                    + gerçek ölçekle işaretlenenler (set 6+7+8) + BİRLEŞİK 1-8
K21_SURUM = ("MUM_IZI_GOZ2 set8 v1.0 (2026-11-26): EK 21 göz ölçümü beşinci bakış (set 8) + kapıdan geçenler (set 7+8, 36) + gerçek ölçekle işaretlenenler (set 6+7+8) + "
             "birleşik 181; tanımlar GZ_ESIK, G2_EK, K17_EK, K19_EK aynen")
K21_DOSYA = {"onkayit": "MUM_IZI21_ON_KAYIT.md", "rapor": "MUM_IZI21_RAPOR.md", "sonuc": "mum_izi21_sonuc.json", "olay": "mum_izi21_olay.csv", "pdf": "MUM_IZI21_SONRASI.pdf"}
K21_YOL = {"isaret8": os.path.join(_C, "cemal_mum_izi20_onay.json"), "anahtar8": os.path.join(_C, "MUM_IZI20_onay_anahtar.json"),
           "olcekli8": os.path.join(_C, "MUM_IZI20_onay_olcekli.json"), "olay19": os.path.join(_C, "mum_izi19_olay.csv"), "sonuc19": os.path.join(_C, "mum_izi19_sonuc.json")}
K21_SET8_AD = "MUM_IZI20_ONAY_OLCEKLI"
K21_ISARET = ("EVET", "KISMEN", "HAYIR", "YOK")
K21_EK: Dict[str, Any] = {
    "surum": "K21-1.0", "tanim": "MUM_IZI_GOZ GZ_ESIK aynen (ESIK11_SHA) + G2_EK aynen (EK13_SHA) + K17_EK aynen (EK17_SHA) + K19_EK aynen (EK19_SHA): giriş, ufuk 15 mum, stop = "
                                "bölge dibi x 0,98, CETVEL2 konum eşi, dokunma, d5_tum, k17 hücresi, gz_tablolar, g2_evet_es, k19 karşılaştırma kuralı (eşli n >= 2)",
    "set8": "MUM_IZI20_ONAY_OLCEKLI (s2-25): sayfa -> bölge mühürlü MUM_IZI20_onay_anahtar.json 'yeni_sayfa' (zaman, pazar, sembol, bolge_bas = ilk barın tarihi, bolge_son, "
            "pencere, oran, hakem_karar, hakem_puan, katman); işaret cemal_mum_izi20_onay.json (EVET / KISMEN / HAYIR / YOK; başka değer DUR); üç dosyada sayfa kümesi ve zaman "
            "aynı olmalı (DUR); anahtar 'oran' = ölçekli 'oran' (DUR); her bölgede oran <= 0,70 (mum boyu kapısı; DUR); mum boyu / olağan / oran ölçekli json'dan aynen",
    "isaretsiz": "isaret 'YOK' (s15) olan bölge sınıf tablolarına girmez (sinif boş) ama ölçülür, eş dışlama kümesine girer ve 'kapıdan geçenler' tablosuna ve dökümüne girer",
    "duyarlilik": "kutu_disi 'iki kutu' içeren sayfa (s11; ana sınıf KISMEN): sinif_duy = EVET; işaret KISMEN değilse DUR; öteki bütün satırlarda sinif_duy = sinif",
    "birlesik": "set 1-8 (181 bölge, 180 sınıflı); eş dışlama kümesi 181 olayla kurulur; set 1-7 değerleri mum_izi19_olay.csv ile karşılaştırılır (R15, es_R15, fark, n_es, "
                "es_neden): değişen satır sayısı ve en büyük mutlak fark yazılır",
    "gecit": "k17_gecit aynen (getiri hesaplamaz); eş sayımı (getirisiz): bölge getirisi NaN verilip GZ.gz_es koşulur, yalnız es_neden / n_es okunur; hesapta gz_olc ve gz_es ile "
             "birebir aynı olmalı (DUR)",
    "tablolar": {"besinci_bakis": "yalnız set 8 (23 sınıflı): Cemal sınıfı (EVET / KISMEN / HAYIR) x zaman (haftalık, günlük, birlikte) k17 hücresi + gz_tablolar + g2_evet_es; "
                                  "bilgi satırı: işaretsiz 1; 24 bölgenin dökümü",
                 "kapidan_gecenler": "set 7 + set 8 (36; oran <= 0,70), Cemal'in işaretinden bağımsız: zaman (haftalık, günlük, birlikte) k17 hücresi + eşli fark ortalamasının "
                                     "basit (ay kümesiz) olay bootstrap %95 aralığı (B 5000, tohum 21) + işaret çevirme p (iki yönlü, 10.000, tohum 21); bilgi satırları: "
                                     "set 7 ve set 8 ayrı (birlikte)",
                 "olcekli": "set 6 + 7 + 8 (52 sınıflı): Cemal sınıfı (EVET, KISMEN, HAYIR, EVET+KISMEN) x zaman (haftalık, günlük, birlikte) k17 hücresi; EVET - HAYIR ve "
                            "(EVET+KISMEN) - HAYIR eşli fark farkı (iki örneklem permütasyonu, iki yönlü, 10.000, tohum 21; iki grupta eşli n >= 2 değilse 'karşılaştırma "
                            "yapılamaz'); HAYIR'ların eşlerine göre farkı (işaret çevirme, 10.000, tohum 21; + bootstrap B 5000 tohum 21); + gz_tablolar + g2_evet_es; "
                            "duyarlılık: aynı tablolar sinif_duy ile",
                 "birlesik": "set 1-8 (181): gz_tablolar (MUM_IZI13 / 17 / 19 birleşik tablosunun aynısı) + g2_evet_es + k17 hücresi + duyarlılık (son işaret); MUM_IZI19 "
                             "birleşiği (mum_izi19_sonuc.json) ile fark: karşılaştırma satırları, EVET - eş, hücre n / R15 / eşli fark"},
    "karsilastirma": {"n_min": 2, "perm": 10000, "boot": 5000, "tohum": 21},
    "okuma": {"kapidan_gecenler": "eşli fark ortalamasının %95 aralığı sıfırın üstündeyse 'eşlerinden iyi', altındaysa 'eşlerinden kötü', sıfırı içeriyorsa 'ayrışmıyor'; "
                                  "eşli n < 30 hücrede ayrıca 'ÖRNEKLEM YETERSİZ'; tek pazar ağırlıklı (ABD) ve tek aday kuralı havuzu: karar etiketi BİLGİ",
              "oteki": "BİLGİ; ÖRNEKLEM YETERSİZ (n < 30)"},
    "etiket": "BİLGİ (kapıdan geçenler dahil); öteki hücreler n < 30: ÖRNEKLEM YETERSİZ",
    "es_siniri": "eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240): aynı gün aynı kova konum eşi",
    "sonuc_anahtar": "sonuç json'unda ön kayıt kapısı kaydı 'onkayit_kapi', tablo (ii) 'kapidan_gecenler'; temel anahtarlar ile tablo anahtarları kesişirse DUR (EK 19 HATA)",
    "pdf": "MUM_IZI19_SONRASI düzeni (k17_sayfa aynen): kapakta düz dil özet tablolar (set 8 Cemal sınıfı x zaman; kapıdan geçenler 36; set 6+7+8 Cemal sınıfı x zaman) + "
           "karşılaştırma / birleşik satırları; sonra set 8'in 24 bölgesinin hepsi: BENZİYOR, KISMEN, BENZEMİYOR, işaretsiz (her sınıfta önce haftalık, sonra bölge sonu "
           "sırası); işaretsiz sayfada 'işaret koymadın', iki kutulu sayfada 'iki kutu işaretledin' satırı",
}
K21_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü aynı kova (CETVEL2 v2.2 konum eşi) aynı takvim aralığı aynı stop geometrisi (GZ aynen); eş dışlama 181 olayla; sınır: eşler bölgenin "
                   "kendi koşusuyla eşlenmedi (Ç229 / Ç240); kapıdan geçenlerde fark = bölge - eş ortalaması (mekanik üstünlük yok: eş aynı giriş / çıkış geometrisi)"),
    "K2": ("EVET", "Cemal set 8'i sonrasını görmeden işaretledi (ölçekli sayfa bölge sonunda kesik); işaret dosyası commit fa7de71, bu ön kayıt set 8 getirilerinden önce; "
                   "giriş bölgeden SONRAKİ barın açılışı; veri <= 2022-12-31 + KASA kapısı; mum boyu oranı yalnız bölge sonu t'ye kadarki barlardan (ölçekli json)"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0); haftalık barlar tamamlanmış ISO haftaları (MH / MV aynen)"),
    "K4": ("EVET", "181 tekil bölge (zaman + sembol + bölge sonu; k21_ornek DUR); set 8'in önceki setlerle ortak sembolü sayılıp yazılır"),
    "K5": ("EVET", "giriş = bölgeden sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk günü); giriş <= stop olay ölçülmez (sayısı yazılır)"),
    "K6": ("EVET", "MI bölünme düzeltmeli fiyatlar (GZ aynen); getiriler oransal; ABD USD, AVR yerel para, BIST TL; pazarlar arası karşılaştırma eşli farkla"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç 'yukarı yanlı' okunur, bilgi, kasa açılmaz"),
    "K8": ("EVET", "set 8 ve set 6+7+8 hücreleri n < 30: 'BİLGİ; ÖRNEKLEM YETERSİZ'; kapıdan geçenler 36 (tek n >= 30 tablo; eşli n ayrıca yazılır); eşli n < 2 'karşılaştırma "
                   "yapılamaz'; 24 bölge tek tek listeli; tek dönem (<= 2022), BH yok (karar yok)"),
    "K9": ("EVET", "MUM_IZI21_ON_KAYIT.md: KOD21 / EK21 / EK19 / EK17 / EK13 / ESIK11 / set 6-7-8 işaret / anahtar / ölçekli / olay19 / sonuç19 sha + getirisiz sayımlar; set 8 "
                   "getirilerinden önce commit + push; k21_kapi sha + commit + temiz ağaç + IZ_KARNE.ik_kontrol_kapisi"),
    "K10": ("EVET", "işaret şeması GZ.gz_isaret_oku + yalnız EVET / KISMEN / HAYIR / YOK (DUR); üç set 8 dosyasında sayfa kümesi ve zaman aynı, anahtar oranı = ölçekli oranı, "
                    "oran <= 0,70 (DUR); iki kutu kuralı (DUR); bölge başı veriden yeniden hesaplanıp anahtarla denetlenir (k17_gecit)"),
    "K11": ("EVET", "getirisiz geçit ve eş sayımı hesapta gz_olc / gz_es ile birebir (DUR); haftalık +%10 k17 dokunma fonksiyonuyla GZ d10'a eşit (DUR); set 1-7 satırları "
                    "mum_izi19_olay.csv ile karşılaştırılır; >= 2 hücre olay csv'sinden bağımsız kodla yeniden üretilir (rapor öncesi, test_mum_izi21)"),
    "K12": ("EVET", "'iz / tuttu / anlamlı' sözü yok; sayı ile yorum ayrı; n < 30 'örneklem yetersiz'; kapıdan geçenler okuma kuralı önceden yazılı"),
    "K13": ("EVET", "çakışma kapısı korunur; çalışan fonksiyonlar değişmez (test_mum_izi21 ast karşılaştırması, e0d9e35'e göre); yasak defter / mühürlü dosyalara dokunulmaz; "
                    "yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez"),
}
K21_KOL = K19_KOL + ["sinif_duy"]


def _k21_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or G2_YOL["cikti"], K21_DOSYA[ad])


def k21_ek_sha() -> str:
    return hashlib.sha256(json.dumps(K21_EK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


# ---------------------------------------------------------------- örneklem
def k21_set8() -> pd.DataFrame:
    """Set 8: sayfa -> bölge (mühürlü anahtar), işaret (Cemal; YOK satırı tutulur, sinif boş), mum boyu (ölçekli json). k19_set7 denetimleri + oran ve iki kutu denetimi."""
    E = GZ.gz_isaret_oku(K21_YOL["isaret8"]); EJ = json.load(open(K21_YOL["isaret8"], encoding="utf-8"))["sayfalar"]
    A = json.load(open(K21_YOL["anahtar8"], encoding="utf-8"))["sayfalar"]; B = {int(s["yeni_sayfa"]): s for s in json.load(open(K21_YOL["olcekli8"], encoding="utf-8"))["sayfalar"]}
    pa = {int(r["yeni_sayfa"]) for r in A}
    if pa != set(E) or pa != set(B) or len(pa) != len(A):
        raise G2Hata(f"K10: set 8 sayfa kümeleri uyuşmuyor (anahtar {sorted(pa)}, işaret {sorted(E)}, ölçekli {sorted(B)})")
    rows = []
    for r in A:
        pg = int(r["yeni_sayfa"]); b = B[pg]; ej = EJ[str(pg)]; ez = ej.get("zaman")
        if E[pg] not in K21_ISARET:
            raise G2Hata(f"K10: set 8 sayfa {pg} işaret {E[pg]!r} (yalnız {K21_ISARET})")
        if b.get("zaman") != r["zaman"] or (ez is not None and ez != r["zaman"]):
            raise G2Hata(f"K10: set 8 sayfa {pg} zaman uyuşmuyor ({r['zaman']}, {b.get('zaman')}, {ez})")
        if not isinstance(ej.get("yildiz"), bool):
            raise G2Hata(f"K10: set 8 sayfa {pg} yildiz bool değil ({ej.get('yildiz')!r})")
        ob = b.get("oran"); oa = r.get("oran")
        if ob is None or oa is None or abs(float(ob) - float(oa)) > 1e-9:
            raise G2Hata(f"K10: set 8 sayfa {pg} anahtar oranı ölçekli oranla uyuşmuyor ({oa}, {ob})")
        if float(ob) > 0.70 + 1e-12:
            raise G2Hata(f"K10: set 8 sayfa {pg} oran {ob} > 0,70 (mum boyu kapısı)")
        iki = "iki kutu" in str(ej.get("kutu_disi", ""))
        if iki and E[pg] != "KISMEN":
            raise G2Hata(f"K10: set 8 sayfa {pg} iki kutu işaretli ama ana sınıf KISMEN değil ({E[pg]})")
        rows.append({"set": "set8", "set_ad": K21_SET8_AD, "sayfa": pg, "isaret": E[pg], "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "tarih": r["bolge_son"],
                     "m": int(r["pencere"]), "bolge_bas_anahtar": r["bolge_bas"], "hakem_sinif": None, "hakem_karar": r.get("hakem_karar"), "hakem2_karar": None,
                     "boy_mutlak": b.get("boy_mutlak"), "boy_onceki": b.get("onceki"), "boy_onceki_n": b.get("onceki_n"), "boy_oran": b.get("oran"),
                     "yildiz": bool(ej["yildiz"]), "katman": r.get("katman"), "iki_kutu": iki})
    X = pd.DataFrame(rows)
    for c in ("boy_mutlak", "boy_onceki", "boy_oran"):
        X[c] = pd.to_numeric(X[c], errors="coerce")
    X["sinif"] = np.where(X.isaret.isin(GZ.SINIF), X.isaret, None); X["sinif_son"] = X["sinif"]
    X["sinif_duy"] = np.where(X.iki_kutu, "EVET", X.sinif)
    return X.drop(columns=["iki_kutu"]).reset_index(drop=True)


def k21_ornek() -> pd.DataFrame:
    X = pd.concat([k19_ornek(), k21_set8()], ignore_index=True)
    if X.duplicated(["zaman", "sembol", "tarih"]).any():
        raise G2Hata("K4: aynı bölge iki kez (set 1-8)")
    X["yildiz"] = X["yildiz"].fillna(False).astype(bool)
    X["sinif_duy"] = [d if s == "set8" else c for s, d, c in zip(X.set, X.sinif_duy, X.sinif)]
    return X


def k21_sembol_tekrar(X: pd.DataFrame) -> Dict[str, Any]:
    s8 = X[X.set == "set8"]; once = X[X.set != "set8"]
    ort = sorted(set(s8.sembol) & set(once.sembol))
    return {"set8_onceki_setlerle_ortak_sembol": ort, "n": len(ort)}


# ---------------------------------------------------------------- getirisiz eş sayımı
def k21_tarih_bir(Dg: pd.DataFrame, W: Optional[pd.DataFrame], r: Dict[str, Any]) -> Dict[str, Any]:
    """gz_olc_bir'in tarih satırları aynen (bolge_bas, bolge_son, giris, son15); fiyat / getiri okunmaz."""
    U = int(GZ.GZ_ESIK["olcu"]["ufuk"]); B = W if r["zaman"] == "haftalik" else Dg
    t = B.index.get_loc(pd.Timestamp(r["tarih"])); s = t - int(r["m"]) + 1
    rec = {"bolge_bas": (W.bas.iloc[s] if r["zaman"] == "haftalik" else Dg.index[s]), "bolge_son": Dg.index[Dg.index.get_loc(B.index[t])], "giris": pd.NaT, "son15": pd.NaT}
    if t + 1 < len(B):
        rec["giris"] = W.bas.iloc[t + 1] if r["zaman"] == "haftalik" else Dg.index[t + 1]
    if t + U < len(B):
        rec["son15"] = B.index[t + U]
    return rec


def k21_es_sayim(X: pd.DataFrame, G: pd.DataFrame) -> pd.DataFrame:
    """Eşi olan / olmayan (getirisiz): bölge getirisi NaN verilerek GZ.gz_es koşulur; yalnız es_neden ve n_es döner (eş getirileri döndürülmez)."""
    Vc: Dict[Any, Any] = {}; T = []
    for r in X.to_dict("records"):
        Vd, Vw = _k17_veri(Vc, r["zaman"], r["pazar"])
        T.append(k21_tarih_bir(Vd[r["sembol"]], Vw[r["sembol"]] if Vw is not None else None, r))
    Z = pd.concat([X.reset_index(drop=True), pd.DataFrame(T)], axis=1)
    Z["olculdu"] = G.olculebilir.astype(bool).to_numpy(); Z["R15"] = np.nan
    E = GZ.gz_es(Z)
    out = pd.DataFrame({"es_neden": E["es_neden"] if "es_neden" in E else np.nan, "n_es": E["n_es"] if "n_es" in E else np.nan}, index=Z.index)
    out.loc[~Z.olculdu, "es_neden"] = "olculemedi"
    out["es_var"] = out.es_neden.fillna("") == ""
    return out


def k21_sayim(G: pd.DataFrame, ES: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """GETİRİSİZ sayım (k17_sayim'in küme sayımı aynen + işaretsiz + eşi olan / olmayan): set 8, kapıdan geçenler (set 7+8), set 6+7+8, birleşik 1-8."""
    def bir(g: pd.DataFrame) -> Dict[str, Any]:
        o = k17_sayim(g)["birlesik"]; o["isaretsiz"] = int(g.sinif.isna().sum())
        o["zaman"] = g.zaman.value_counts().to_dict()
        if ES is not None:
            e = ES.loc[g.index]; o["esi_olan"] = int(e.es_var.sum()); o["esi_olmayan"] = e[~e.es_var].es_neden.fillna("").value_counts().to_dict()
            o["esi_olan_sinif_zaman"] = {f"{s}|{z}": int(((g.sinif == s) & (g.zaman == z) & e.es_var).sum()) for s in GZ.SINIF for z in K17_ZAMAN}
            o["esi_olan_zaman"] = {z: int(((g.zaman == z) & e.es_var).sum()) for z in K17_ZAMAN}
        return o
    s8 = G[G.set == "set8"]
    return {"set8": bir(s8), "kapidan_gecenler": bir(G[G.set.isin(["set7", "set8"])]), "set6_7_8": bir(G[G.set.isin(["set6", "set7", "set8"]) & G.sinif.notna()]),
            "birlesik": bir(G), "set8_isaret": s8.isaret.value_counts().to_dict(),
            "set8_hakem_karar_isaret": {f"{h}|{i}": int(v) for (h, i), v in s8.groupby(["hakem_karar", "isaret"]).size().items()},
            "set8_katman": s8.katman.value_counts().to_dict(), "set8_duyarlilik_degisen": s8[s8.sinif_duy.fillna("-") != s8.sinif.fillna("-")][["sayfa", "sinif", "sinif_duy"]].to_dict("records")}


# ---------------------------------------------------------------- tablolar
def k21_karsilastir(a: pd.DataFrame, b: pd.DataFrame) -> Dict[str, Any]:
    """k19_karsilastir kuralı aynen (eşli n >= 2), permütasyon tohumu 21 (K21_EK)."""
    C = K21_EK["karsilastirma"]
    oa = a[a.olculdu.astype(bool)]; ob = b[b.olculdu.astype(bool)]
    fa = oa.fark.astype(float).to_numpy(); fb = ob.fark.astype(float).to_numpy(); fa = fa[np.isfinite(fa)]; fb = fb[np.isfinite(fb)]
    Ra = oa.R15.astype(float).to_numpy(); Rb = ob.R15.astype(float).to_numpy(); Ra = Ra[np.isfinite(Ra)]; Rb = Rb[np.isfinite(Rb)]
    out: Dict[str, Any] = {"n_a": int(len(Ra)), "n_b": int(len(Rb)), "n_es_a": int(len(fa)), "n_es_b": int(len(fb))}
    if len(fa) < C["n_min"] or len(fb) < C["n_min"]:
        out.update({"esli_fark_fark": None, "esli_p": None, "durum": "karşılaştırma yapılamaz"})
    else:
        out.update({"esli_fark_fark": float(fa.mean() - fb.mean()), "esli_p": GZ.gz_perm(fa, fb, C["perm"], C["tohum"]), "durum": "hesaplandı"})
    out["R15_fark_bilgi"] = float(Ra.mean() - Rb.mean()) if len(Ra) and len(Rb) else None
    return out


def k21_es_farki(g: pd.DataFrame) -> Dict[str, Any]:
    """Eşli fark ortalaması sıfırdan farklı mı: basit olay bootstrap %95 (B 5000, tohum 21) + işaret çevirme p (10.000, tohum 21)."""
    C = K21_EK["karsilastirma"]; o = g[g.olculdu.astype(bool)]; f = o.fark.astype(float).to_numpy(); f = f[np.isfinite(f)]
    return {"n_es": int(len(f)), "esli_fark_ort": float(f.mean()) if len(f) else None, "boot95": GZ.gz_boot(f, C["boot"], C["tohum"])["ort95"],
            "p": g2_isaret_perm(f, C["perm"], C["tohum"])}


def k21_okuma(e: Dict[str, Any]) -> str:
    b = e.get("boot95")
    if b is None:
        o = "hesaplanamadı"
    else:
        o = "eşlerinden iyi" if b[0] > 0 else ("eşlerinden kötü" if b[1] < 0 else "ayrışmıyor")
    return o + ("; ÖRNEKLEM YETERSİZ" if e.get("n_es", 0) < 30 else "") + "; BİLGİ"


def k21_tablolar(Y: pd.DataFrame) -> Dict[str, Any]:
    zs = _k19_zs; Y8 = Y[Y.set == "set8"]; Y78 = Y[Y.set.isin(["set7", "set8"])]; Y678 = Y[Y.set.isin(["set6", "set7", "set8"]) & Y.sinif.notna()]
    gr = (("EVET", ["EVET"]), ("KISMEN", ["KISMEN"]), ("HAYIR", ["HAYIR"]), ("EVET+KISMEN", ["EVET", "KISMEN"]))
    b5 = {f"{s}|{z}": k17_hucre(zs(Y8[Y8.sinif == s], z)) for s in GZ.SINIF for z in K19_ZZ}
    b5.update({f"isaretsiz|{z}": k17_hucre(zs(Y8[Y8.sinif.isna()], z)) for z in K19_ZZ})
    kg = {}
    for z in K19_ZZ:
        c = k17_hucre(zs(Y78, z)); e = k21_es_farki(zs(Y78, z)); c.update({"fark_boot95": e["boot95"], "fark_p": e["p"], "okuma": k21_okuma(e)}); kg[f"set7+set8|{z}"] = c
    kg.update({f"{st}|birlikte": k17_hucre(Y[Y.set == st]) for st in ("set7", "set8")})

    def olcekli(D: pd.DataFrame, kol: str) -> Dict[str, Any]:
        D = D.copy(); D["sinif"] = D[kol]
        return {"hucre": {f"{s}|{z}": k17_hucre(zs(D[D.sinif.isin(sl)], z)) for s, sl in gr for z in K19_ZZ},
                "karsilastirma": {f"{ad}|{z}": k21_karsilastir(zs(D[D.sinif.isin(sl)], z), zs(D[D.sinif == "HAYIR"], z))
                                  for ad, sl in (("EVET-HAYIR", ["EVET"]), ("(EVET+KISMEN)-HAYIR", ["EVET", "KISMEN"])) for z in K19_ZZ},
                "hayir_es": {f"HAYIR-es|{z}": k21_es_farki(zs(D[D.sinif == "HAYIR"], z)) for z in K19_ZZ}}
    ol = olcekli(Y678, "sinif"); ol.update({"gz": GZ.gz_tablolar(Y678), "evet_es": g2_evet_es(Y678), "duyarlilik": olcekli(Y678, "sinif_duy")})
    bk = {f"{s}|{z}": k17_hucre(zs(Y[Y.sinif.isin(sl)], z)) for s, sl in gr for z in K19_ZZ}
    return {"besinci_bakis": {"hucre": b5, "gz": GZ.gz_tablolar(Y8), "evet_es": g2_evet_es(Y8)}, "kapidan_gecenler": kg, "olcekli": ol,
            "birlesik": {"tablo": GZ.gz_tablolar(Y), "evet_es": g2_evet_es(Y), "k17_hucre": bk, "duyarlilik_son_isaret": GZ.gz_tablolar(Y, "sinif_son")["karsilastirma"]}}


def k21_dokum(Y: pd.DataFrame) -> List[Dict[str, Any]]:
    Y8 = Y[Y.set == "set8"].copy(); Y8["_s"] = Y8.sinif.map({s: i for i, s in enumerate(GZ.SINIF)}).fillna(9); Y8["_z"] = Y8.zaman.map({"haftalik": 0, "gunluk": 1})
    kol = ["sayfa", "isaret", "sinif_duy", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "m", "olculdu", "neden", "R15", "es_R15", "n_es", "fark", "max15", "min15",
           "stop15", "d5_tum", "d10", "R30", "boy_mutlak", "boy_onceki", "boy_oran", "hakem_karar", "katman"]
    return [{k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in r.items()}
            for r in Y8.sort_values(["_s", "_z", "bolge_son"])[kol].to_dict("records")]


def k21_fark19(J19: Dict[str, Any], T: Dict[str, Any]) -> Dict[str, Any]:
    """MUM_IZI19 birleşik (157) -> MUM_IZI21 birleşik (181)."""
    a = J19["birlesik"]; b = T["birlesik"]; out: Dict[str, Any] = {"karsilastirma": {}, "evet_es": {}, "hucre": {}}
    for k, v in b["tablo"]["karsilastirma"].items():
        o = a["tablo"]["karsilastirma"].get(k, {})
        out["karsilastirma"][k] = {"esli_fark_fark_19": o.get("esli_fark_fark"), "esli_fark_fark_21": v.get("esli_fark_fark"), "esli_p_19": o.get("esli_p"), "esli_p_21": v.get("esli_p"),
                                   "n_es_a_19": o.get("n_es_a"), "n_es_a_21": v.get("n_es_a"), "n_es_b_19": o.get("n_es_b"), "n_es_b_21": v.get("n_es_b")}
    for k, v in b["evet_es"].items():
        o = a["evet_es"].get(k, {})
        out["evet_es"][k] = {"ort_19": o.get("esli_fark_ort"), "ort_21": v.get("esli_fark_ort"), "p_19": o.get("p"), "p_21": v.get("p"), "n_19": o.get("n_es"), "n_21": v.get("n_es")}
    for k, v in b["tablo"]["hucre"].items():
        if k.endswith("|BIST"):
            continue
        o = a["tablo"]["hucre"].get(k, {})
        out["hucre"][k] = {"n_19": o.get("n"), "n_21": v.get("n"), "R15_ort_19": o.get("R15_ort"), "R15_ort_21": v.get("R15_ort"), "fark_ort_19": o.get("fark_ort"),
                           "fark_ort_21": v.get("fark_ort")}
    return out


# ---------------------------------------------------------------- kapı, ön kayıt, koşu
def k21_sha_simdi() -> Dict[str, str]:
    return {"KOD21_SHA": MI._mi_sha(G2_YOL["kod"]), "EK21_SHA": k21_ek_sha(), "EK19_SHA": k19_ek_sha(), "EK17_SHA": k17_ek_sha(), "EK13_SHA": g2_ek_sha(),
            "GZ_KOD_SHA": MI._mi_sha(GZ.GZ_YOL["kod"]), "ESIK11_SHA": GZ.gz_esik_sha(), "ISARET_SET8_SHA": MI._mi_sha(K21_YOL["isaret8"]),
            "ANAHTAR_SET8_SHA": MI._mi_sha(K21_YOL["anahtar8"]), "OLCEKLI_SET8_SHA": MI._mi_sha(K21_YOL["olcekli8"]), "ISARET_SET7_SHA": MI._mi_sha(K19_YOL["isaret7"]),
            "ANAHTAR_SET7_SHA": MI._mi_sha(K19_YOL["anahtar7"]), "ISARET_SET6_SHA": MI._mi_sha(K17_YOL["isaret6"]), "ANAHTAR_SET6_SHA": MI._mi_sha(K17_YOL["anahtar6"]),
            "OLAY19_SHA": MI._mi_sha(K21_YOL["olay19"]), "SONUC19_SHA": MI._mi_sha(K21_YOL["sonuc19"])}


def k21_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    yol = _k21_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise G2Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = k21_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise G2Hata(f"ön kayıt 21 kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_G2); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise G2Hata("ön kayıt 21 commit'li değil -> DURDU")
    gir = [os.path.relpath(v, KOK_G2) for v in list(K21_YOL.values()) + list(K19_YOL.values()) + list(K17_YOL.values())]
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_GOZ2.py", "MUM_IZI_GOZ.py"] + gir):
        raise G2Hata("ön kayıt / kod / girdiler çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def _k21_tablo_md(s: Dict[str, Any], es: bool = True) -> List[str]:
    t = ["| Cemal | haftalık: bölge (ölçülebilen; eşi olan) | günlük: bölge (ölçülebilen; eşi olan) |", "|---|---|---|"]
    for c in GZ.SINIF:
        t.append(f"| {K17_AD[c]} | " + " | ".join(f"{s['sinif_zaman'][f'{c}|{z}']} ({s['sinif_zaman_olculebilir'][f'{c}|{z}']}; "
                                                    f"{s['esi_olan_sinif_zaman'][f'{c}|{z}'] if es else '-'})" for z in K17_ZAMAN) + " |")
    return t


def k21_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    y = _k21_yol("onkayit", cikti)
    if os.path.exists(y):
        raise G2Hata("ön kayıt 21 zaten var")
    X = k21_ornek(); G = k17_gecit(X); ES = k21_es_sayim(X, G); S = k21_sayim(G, ES); sh = k21_sha_simdi(); st = k21_sembol_tekrar(X)
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in K21_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_GOZ2.py"])

    def sat(ad_: str, s: Dict[str, Any]) -> str:
        return (f"{ad_}: {s['toplam']} bölge (işaretsiz {s['isaretsiz']}), ölçülebilen {s['olculebilir']}, ölçülemeyen {s['toplam'] - s['olculebilir']} "
                f"{json.dumps(s['olculemedi'], ensure_ascii=False)}; eşi olan {s['esi_olan']}, eşi olmayan {json.dumps(s['esi_olmayan'], ensure_ascii=False)}; zaman "
                f"{json.dumps(s['zaman'], ensure_ascii=False)} (eşi olan {json.dumps(s['esi_olan_zaman'], ensure_ascii=False)}); pazar {json.dumps(s['pazar'], ensure_ascii=False)}; "
                f"en geç 15. mum {s['en_gec_15_mum']}.")
    s = [f"# MUM_IZI21 ÖN KAYIT ({MI._mi_simdi()})", "",
         "MUM_IZI11 / 13 / 17 / 19 ön kayıtlarının tanımları AYNEN (MUM_IZI_GOZ.py GZ_ESIK: ESIK11_SHA; G2_EK: EK13_SHA; K17_EK: EK17_SHA; K19_EK: EK19_SHA): giriş = bölgeden "
         "sonraki ilk geçerli barın açılışı; ufuk 15 mum; stop = bölge dibi x 0,98; dokunma; R30; CETVEL2 konum eşi; d5_tum; k17 hücresi; tablolar; permütasyonlar. Ek: set 8 = "
         "MUM_IZI20_ONAY_OLCEKLI 24 bölge (hepsi mum boyu kapısından geçen, oran <= 0,70; katmanlı: hakem KISMEN / BENZEMİYOR x oran <= 0,65 / 0,65-0,70; Cemal sonrasını "
         "görmeden, yüzde eksenli sayfada, 'mumlar gerçekten küçük kabul ederek' işaretledi; 1 sayfa işaretsiz, 1 sayfa iki kutu). Bu dosya set 8'in getirileri hesaplanmadan "
         "ÖNCE commit edilir; getirisiz sayımlar aşağıda (eş sayımı bölge getirisi hesaplanmadan, yalnız eş uygunluğu).", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_GOZ2.py commit'i: {kc or 'yok'}", "",
         "## GETİRİSİZ SAYIM (getiri hesaplanmadı; yalnız işaret, zaman, veri kapıları, eş uygunluğu)", "",
         sat("Set 8", S["set8"]) + f" İşaret {json.dumps(S['set8_isaret'], ensure_ascii=False)}; hakem kararı x işaret {json.dumps(S['set8_hakem_karar_isaret'], ensure_ascii=False)}; "
         f"katman {json.dumps(S['set8_katman'], ensure_ascii=False)}; duyarlılıkta değişen {json.dumps(S['set8_duyarlilik_degisen'], ensure_ascii=False)}.", "",
         *_k21_tablo_md(S["set8"]), "",
         sat("Kapıdan geçenler (set 7 + set 8; işaretten bağımsız)", S["kapidan_gecenler"]), "",
         sat("Set 6 + 7 + 8 (gerçek ölçekle işaretlenenler; yalnız sınıflı)", S["set6_7_8"]), "", *_k21_tablo_md(S["set6_7_8"]), "",
         sat("Birleşik set 1-8", S["birlesik"]), "", *_k21_tablo_md(S["birlesik"]), "",
         f"- Set 8'in önceki setlerle ortak sembolü: {st['n']} {st['set8_onceki_setlerle_ortak_sembol']} (bölge tekrarı yok: zaman + sembol + bölge sonu tekil, denetlendi).",
         "- Eşsiz olay eşli tabloya girmez (GZ aynen); eş sayımı hesapta gz_es ile satır satır aynı olmalı (DUR).", "",
         "## Tablolar (önceden; sonuçtan sonra değişmez)", "",
         "- (i) BEŞİNCİ BAKIŞ = yalnız set 8 (23 sınıflı): Cemal sınıfı x zaman (haftalık, günlük, birlikte): n, R15 ort / medyan, eş ort, eşli fark ort / medyan, artıda payı, "
         "eşinden iyi payı, +%5 / +%10 stop'tan önce payı, stop payı (k17 hücresi) + GZ tabloları + EVET - eş; bilgi satırı işaretsiz 1. 24 bölgenin dökümü (sayfa, işaret, zaman, "
         "sembol, R15, eş ort, mum boyu %, oran, hakem kararı, katman).",
         "- (ii) KAPIDAN GEÇENLER = set 7 + set 8 (36; mumları olağanın 0,70 katı ya da altı), Cemal'in işaretinden bağımsız: aynı ölçüler zaman dilimine göre ve birlikte + eşli "
         "fark ortalamasının basit olay bootstrap %95 aralığı (ay kümesiz; B 5000, tohum 21) + işaret çevirme p (iki yönlü, 10.000, tohum 21). Soru: 'belirgin küçük mumlu "
         "bölgeler eşlerinden iyi gitti mi'. Bilgi satırları: set 7 ve set 8 ayrı (birlikte).",
         "- (iii) GERÇEK ÖLÇEKLE İŞARETLENENLER = set 6 + 7 + 8 (52 sınıflı): Cemal sınıfı (ve BENZİYOR + KISMEN) x zaman (haftalık, günlük, birlikte); BENZİYOR - BENZEMİYOR ve "
         "(BENZİYOR + KISMEN) - BENZEMİYOR eşli fark farkı (iki örneklem permütasyonu, iki yönlü, 10.000, tohum 21; iki grupta eşli n >= 2 değilse 'karşılaştırma yapılamaz'); "
         "BENZEMİYOR'ların eşlerine göre farkı (işaret çevirme, tohum 21; bootstrap %95). Duyarlılık: iki kutu işaretli sayfa (s11) EVET sayılırsa aynı tablolar.",
         "- (iv) BİRLEŞİK = set 1-8 (181; 180 sınıflı): MUM_IZI19 birleşik tablosunun aynısı (GZ tabloları, EVET - eş, k17 hücresi, duyarlılık son işaret) + MUM_IZI19 birleşiğine "
         "göre değişim (EVET - HAYIR eşli fark farkı ve p, EVET - eş, hücre n / R15 / eşli fark).",
         "- Set 1-7 satırları mum_izi19_olay.csv ile karşılaştırılır (R15, es_R15, fark, n_es, es_neden): eş dışlama kümesi 181 olayla kurulduğu için eş değerleri değişebilir; "
         "değişen satır sayısı ve en büyük fark yazılır.",
         "- OKUMA: (ii) dışındaki hücreler n < 30: 'BİLGİ; ÖRNEKLEM YETERSİZ'. (ii) için: eşli fark ortalamasının %95 aralığı sıfırın üstündeyse 'eşlerinden iyi', altındaysa "
         "'eşlerinden kötü', sıfırı içeriyorsa 'ayrışmıyor'; eşli n < 30 olan (ii) hücresine ayrıca 'ÖRNEKLEM YETERSİZ'; tek pazar ağırlıklı (ABD) ve tek aday kuralı havuzu "
         "olduğu için karar etiketi yine BİLGİ. Eş sınırı: eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240).", "",
         "## Ek tanımlar (K21_EK; sha yukarıda)", "", "```", json.dumps(K21_EK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ (`python IZ_KARNE.py kontrol`; K8: set 8 ve set 6 + 7 + 8 hücreleri n < 30)", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 21")


def k21_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    t0 = time.time(); cikti = cikti or G2_YOL["cikti"]
    if os.path.exists(_k21_yol("sonuc", cikti)):
        raise G2Hata("sonuç 21 zaten var")
    G0 = k21_kapi(cikti)
    kasa = KS.kasa_kapisi([os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] +
                          [os.path.join(MH.MH_YOL["tam"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")],
                          "2022-12-31")
    X = k21_ornek(); Gt = k17_gecit(X); ES = k21_es_sayim(X, Gt)
    Y = GZ.gz_es(GZ.gz_olc(X))
    if not (Y.olculdu.astype(bool).to_numpy() == Gt.olculebilir.astype(bool).to_numpy()).all() or \
            not (Y.neden.fillna("").to_numpy() == Gt.neden.fillna("").to_numpy()).all():
        raise G2Hata("K11: getirisiz geçit ile gz_olc uyuşmuyor")
    m = Y.olculdu.astype(bool).to_numpy()
    if not (Y.es_neden.fillna("").to_numpy()[m] == ES.es_neden.fillna("").to_numpy()[m]).all() or \
            not np.allclose(Y.n_es.to_numpy(float)[m], ES.n_es.to_numpy(float)[m], equal_nan=True):
        raise G2Hata("K11: getirisiz eş sayımı ile gz_es uyuşmuyor")
    Y = k17_d5(Y).sort_values(["set", "sayfa"]).reset_index(drop=True)
    for c in K21_KOL:
        if c not in Y:
            Y[c] = np.nan
    O = Y[K21_KOL].copy()
    for c in ("bolge_bas", "bolge_son", "giris", "son15"):
        O[c] = pd.to_datetime(O[c]).dt.strftime("%Y-%m-%d")
    O.to_csv(_k21_yol("olay", cikti), index=False, float_format="%.6f")
    O21 = pd.read_csv(_k21_yol("olay", cikti)); O19 = pd.read_csv(K21_YOL["olay19"])
    J19 = json.load(open(K21_YOL["sonuc19"], encoding="utf-8")); T = k21_tablolar(O)
    Y8 = O[O.set == "set8"]; Y78 = O[O.set.isin(["set7", "set8"])]; Y678 = O[O.set.isin(["set6", "set7", "set8"]) & O.sinif.notna()]
    J = {"surum": K21_SURUM, "onkayit_kapi": G0, "kasa": kasa, "sayim": k21_sayim(Gt, ES), "sembol_tekrar": k21_sembol_tekrar(X),
         "es_yok": {k: D[D.olculdu.astype(bool)].es_neden.fillna("").replace("", "var").value_counts().to_dict()
                    for k, D in (("set8", Y8), ("kapidan_gecenler", Y78), ("set6_7_8", Y678), ("birlesik", O))},
         "set1_7_mum_izi19_farki": k19_onceki_farki(O19, O21, "set8"), "dokum_set8": k21_dokum(O), "mum_izi19_birlesik_farki": k21_fark19(J19, T),
         "etiket": K21_EK["etiket"], "okuma": K21_EK["okuma"], "es_siniri": K21_EK["es_siniri"], "olay_sha": MI._mi_sha(_k21_yol("olay", cikti))}
    cak = set(J) & set(T)
    if cak:
        raise G2Hata(f"sonuç 21 anahtar çakışması {sorted(cak)} (EK 19 HATA) -> DURDU")
    J.update(T); J["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_k21_yol("sonuc", cikti), J, "sonuç 21")
    return J


# ---------------------------------------------------------------- PDF
def k21_pdf(cikti: Optional[str] = None, olay: Optional[pd.DataFrame] = None, sonuc: Optional[Dict[str, Any]] = None, yol: Optional[str] = None) -> str:
    """MUM_IZI21_SONRASI.pdf (k19_pdf düzeni; sayfalar k17_sayfa aynen + işaretsiz / iki kutu satırı). olay / sonuc / yol verilirse dosyalar okunmaz (deneme basımı)."""
    import textwrap
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    cikti = cikti or G2_YOL["cikti"]; y = yol or _k21_yol("pdf", cikti)
    if olay is None:
        J = json.load(open(_k21_yol("sonuc", cikti), encoding="utf-8"))
        if MI._mi_sha(_k21_yol("olay", cikti)) != J["olay_sha"]:
            raise G2Hata("olay csv'si sonuç 21 json'uyla uyuşmuyor")
        O = pd.read_csv(_k21_yol("olay", cikti))
    else:
        O, J = olay, sonuc
    D5 = J["besinci_bakis"]["hucre"]; KG = J["kapidan_gecenler"]; OL = J["olcekli"]; OH = OL["hucre"]; OK = OL["karsilastirma"]; BK = J["birlesik"]["k17_hucre"]
    BKK = J["birlesik"]["tablo"]["karsilastirma"]; Vc: Dict[Any, Any] = {}; zad = {"haftalik": "haftalık", "gunluk": "günlük", "birlikte": "ikisi"}
    kol = ["senin\nişaretin", "mum", "bölge", "artıda\nkapanan", "ortalama", "medyan", "eşlerin\nort.", "eşinden\niyi", "+%5'e\nstop'tan önce", "stop\nolan"]

    def puan(v: Optional[float]) -> str:
        return "-" if v is None or not np.isfinite(v) else f"{v * 100:+.1f} puan".replace(".", ",")

    def p_yaz(p: Optional[float]) -> str:
        return "-" if p is None else f"{p:.2f}".replace(".", ",")

    def hsat(ad_: str, z: str, c: Dict[str, Any]) -> List[str]:
        n = c.get("n", 0); ne = c.get("n_es", 0)
        return [ad_, zad[z], str(n), _k17_pay(c.get("arti_pay"), n), _k17_yuzde(c.get("R15_ort")), _k17_yuzde(c.get("R15_med")), _k17_yuzde(c.get("es_ort")),
                _k17_pay(c.get("esinden_iyi_pay"), ne), _k17_pay(c.get("d5_pay"), n), _k17_pay(c.get("stop_pay"), n)]

    def satirlar(H: Dict[str, Any], zl: Tuple[str, ...]) -> List[List[str]]:
        return [hsat(K17_AD[s], z, H[f"{s}|{z}"]) for z in zl for s in GZ.SINIF if H[f"{s}|{z}"].get("n", 0)]

    def tablo(fig, y0: float, baslik: str, sat: List[List[str]], ilk: str = "senin\nişaretin") -> float:
        fig.text(0.05, y0, baslik, fontsize=11, weight="bold"); h = 0.028 * (len(sat) + 1)
        ax = fig.add_axes([0.02, y0 - 0.012 - h, 0.96, h]); ax.axis("off")
        tb = ax.table(cellText=sat, colLabels=[ilk] + kol[1:], loc="upper center", cellLoc="center", colWidths=[0.13, 0.09, 0.06, 0.09, 0.1, 0.1, 0.09, 0.09, 0.13, 0.08],
                      bbox=[0, 0, 1, 1])
        tb.auto_set_font_size(False); tb.set_fontsize(9.5)
        return y0 - 0.012 - h - 0.028

    def fark_yaz(c: Dict[str, Any]) -> str:
        return "karşılaştırma yapılamaz" if c.get("esli_fark_fark") is None else f"{puan(c['esli_fark_fark'])} (p {p_yaz(c.get('esli_p'))})"

    def aralik(b: Optional[List[float]]) -> str:
        return "-" if not b else f"{puan(b[0])[:-5]} .. {puan(b[1])}"
    n8 = int((O.set == "set8").sum()); n78 = int(O.set.isin(["set7", "set8"]).sum()); n678 = int((O.set.isin(["set6", "set7", "set8"]) & O.sinif.notna()).sum())
    with PdfPages(y, metadata={"Title": "MUM_IZI21 sonrası", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7))
        fig.text(0.05, 0.965, f"Son {n8} bölge (hepsi küçük mumlu): işaretlerin sonrasında ne yaptı", fontsize=14, weight="bold")
        fig.text(0.05, 0.945, "Giriş: bölgeden sonraki ilk mumun açılışı. 15 mum sonraki kapanışla getiri. Eş: aynı gün, benzer oynaklık ve likiditedeki hisseler.",
                 fontsize=9)
        yy = tablo(fig, 0.92, f"Bu {n8} bölge (işaret koymadığın 1 bölge tabloda yok)", satirlar(D5, K17_ZAMAN))
        yy = tablo(fig, yy, f"Mumları belirgin küçük {n78} bölgenin hepsi (bu set + önceki 12; işaretinden bağımsız)",
                   [hsat("hepsi", z, KG[f"set7+set8|{z}"]) for z in K19_ZZ], ilk="küme")
        yy = tablo(fig, yy, f"Yüzde eksenli üç set birlikte ({n678} bölge)", satirlar(OH, ("birlikte",)))
        kb = KG["set7+set8|birlikte"]
        sat2 = [f"{n78} küçük mumlu bölge eşlerinden ortalama {puan(kb.get('fark_ort'))} ayrıldı (%95 aralık {aralik(kb.get('fark_boot95'))}; p {p_yaz(kb.get('fark_p'))}): "
                f"{kb.get('okuma', '').split(';')[0]}.",
                f"{n678} bölgede BENZİYOR - BENZEMİYOR (eşlerine göre): günlük {fark_yaz(OK['EVET-HAYIR|gunluk'])}; haftalık {fark_yaz(OK['EVET-HAYIR|haftalik'])}; "
                f"ikisi birlikte {fark_yaz(OK['EVET-HAYIR|birlikte'])}. BENZEMİYOR dediklerin eşlerinden {puan(OL['hayir_es']['HAYIR-es|birlikte'].get('esli_fark_ort'))} "
                f"(p {p_yaz(OL['hayir_es']['HAYIR-es|birlikte'].get('p'))}).",
                f"Bütün bölgeler ({int(O.sinif.notna().sum())}): BENZİYOR - BENZEMİYOR günlük {fark_yaz(BKK['EVET-HAYIR|gunluk'])}; haftalık {fark_yaz(BKK['EVET-HAYIR|haftalik'])}."]
        for s_ in sat2:
            w = textwrap.fill(s_, 98); fig.text(0.05, yy, w, fontsize=9.5, va="top", linespacing=1.4); yy -= 0.018 * (w.count("\n") + 1) + 0.012
        fig.text(0.05, yy - 0.008, "Sayılar az (çoğu N < 30): bu bir sonuç değil, bilgi.", fontsize=12.5, weight="bold")
        fig.text(0.05, yy - 0.045, f"Sonraki sayfalar: bu {n8} bölgenin hepsi; önce BENZİYOR, sonra KISMEN, sonra BENZEMİYOR, en sonda işaretsiz.\n"
                 "Hisse ve tarih açık. Sağdaki eksen girişe göre yüzde (0 = giriş fiyatı). Altta bölgedeki gerçek mum boyu\nve bu hissenin olağanına oranı "
                 "(1'den küçük = mumlar olağandan küçük).", fontsize=9.5, va="top", linespacing=1.5)
        pdf.savefig(fig); plt.close(fig)
        X = O[O.set == "set8"].copy(); X["_s"] = X.sinif.map({s: i for i, s in enumerate(GZ.SINIF)}).fillna(9); X["_z"] = X.zaman.map({"haftalik": 0, "gunluk": 1})
        for r in X.sort_values(["_s", "_z", "bolge_son"]).itertuples():
            k = (r.zaman, r.pazar)
            if k not in Vc:
                Vc[k] = MV.mv_veri(*k)
            yok = not isinstance(r.sinif, str)
            rr = r._replace(sinif="KISMEN") if yok else r
            fig = plt.figure(figsize=(8.3, 11.7)); k17_sayfa(fig, rr, Vc[k][r.sembol])
            if yok:
                for t in fig.texts:
                    if t.get_text().startswith("Senin işaretin:"):
                        t.set_text("İşaret koymadın (karar dışı)"); t.set_color("#555555")
            elif isinstance(r.sinif_duy, str) and r.sinif_duy != r.sinif:
                fig.text(0.55, 0.957, "iki kutu işaretledin (BENZİYOR + KISMEN)", fontsize=11, weight="bold", color="#555555")
            pdf.savefig(fig); plt.close(fig)
    return y


# ================================================================ 5) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_g2(_once=_CK_ONCE_G2, _dosya="MUM_IZI_GOZ2.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_G2",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_g2()


def _g2_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_GOZ2")
    ap.add_argument("komut", choices=["ornek", "onkayit", "kos", "pdf", "kopma_sayim", "kopma_onkayit", "kopma", "olcek_olcu", "olcek_onkayit", "olcek",
                                      "set6_sayim", "set6_onkayit", "set6_kos", "set6_pdf", "set7_sayim", "set7_onkayit", "set7_kos", "set7_pdf",
                                      "set8_sayim", "set8_onkayit", "set8_kos", "set8_pdf"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "ornek":
            X = g2_ornek(); print(json.dumps({"set5": GZ.gz_ornek_sayim(X[X.set == "set5"]), "birlesik": GZ.gz_ornek_sayim(X)}, ensure_ascii=False))
        elif a.komut == "onkayit":
            print(g2_onkayit_yaz())
        elif a.komut == "kos":
            J = g2_kos(); print(json.dumps(MI._mi_json({k: J[k] for k in ("olculemedi", "es_yok", "set1_4_mum_izi11_farki", "yon")}), ensure_ascii=False))
        elif a.komut == "pdf":
            print(g2_pdf())
        elif a.komut == "kopma_sayim":
            _, G, _ = k15_veri(); print(json.dumps(MI._mi_json({k: G[k] for k in ("sayim", "uyum")} | {"tekrar": {h: G["tekrar"][h] for h in ("K1", "K2")}}), ensure_ascii=False))
        elif a.komut == "kopma_onkayit":
            print(k15_onkayit_yaz())
        elif a.komut == "kopma":
            J = k15_kos(); print(json.dumps(MI._mi_json({k: J[k] for k in ("okuma", "bilgi_spearman_evet", "es_sayim_denetimi")}), ensure_ascii=False))
        elif a.komut == "olcek_olcu":
            D = k16_veri(); print(json.dumps(MI._mi_json({"A1": k16_a1(D), "grup_n": k16_grup_n(D)}), ensure_ascii=False))
        elif a.komut == "olcek_onkayit":
            print(k16_onkayit_yaz())
        elif a.komut == "olcek":
            J = k16_kos(); print(json.dumps(MI._mi_json({"okuma": J["okuma"], "sure_sn": J["sure_sn"]}), ensure_ascii=False))
        elif a.komut == "set6_sayim":
            print(json.dumps(MI._mi_json(k17_sayim(k17_gecit(k17_ornek()))), ensure_ascii=False))
        elif a.komut == "set6_onkayit":
            print(k17_onkayit_yaz())
        elif a.komut == "set6_kos":
            J = k17_kos(); print(json.dumps(MI._mi_json({k: J[k] for k in ("sayim", "es_yok", "set1_5_mum_izi13_farki", "yon", "sure_sn")}), ensure_ascii=False))
        elif a.komut == "set6_pdf":
            print(k17_pdf())
        elif a.komut == "set7_sayim":
            print(json.dumps(MI._mi_json(k19_sayim(k17_gecit(k19_ornek()))), ensure_ascii=False))
        elif a.komut == "set7_onkayit":
            print(k19_onkayit_yaz())
        elif a.komut == "set7_kos":
            J = k19_kos(); print(json.dumps(MI._mi_json({k: J[k] for k in ("sayim", "es_yok", "set1_6_mum_izi17_farki", "yon", "sure_sn")}), ensure_ascii=False))
        elif a.komut == "set7_pdf":
            print(k19_pdf())
        elif a.komut == "set8_sayim":
            X = k21_ornek(); G = k17_gecit(X); print(json.dumps(MI._mi_json(k21_sayim(G, k21_es_sayim(X, G))), ensure_ascii=False))
        elif a.komut == "set8_onkayit":
            print(k21_onkayit_yaz())
        elif a.komut == "set8_kos":
            J = k21_kos(); print(json.dumps(MI._mi_json({k: J[k] for k in ("sayim", "es_yok", "set1_7_mum_izi19_farki", "sure_sn")}), ensure_ascii=False))
        elif a.komut == "set8_pdf":
            print(k21_pdf())
    except (G2Hata, GZ.GZHata) as ex:
        g2log.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_g2_ana())
