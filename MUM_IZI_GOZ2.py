"""MUM_IZI_GOZ2 — MUM_IZI EK 13: göz ölçümünün İKİNCİ BAKIŞI (26 Kasım 2026).

Ana modelin görevi: MUM_IZI11 göz ölçümü AYNI ön kayıtlı tanımlarla (MUM_IZI_GOZ.py GZ_ESIK; hiçbir tanım / eşik değişmez) set 5 (MUM_IZI12_ONAY: hakem v3'ün
seçtiği 24 bölge; Cemal EVET 11 / KISMEN 8 / HAYIR 5) eklenerek yeniden koşulur. Üç rapor ailesi: (i) İLK BAKIŞ = set 1-4 (MUM_IZI11 sonucu, değişmez; json'dan),
(ii) İKİNCİ BAKIŞ = yalnız set 5, (iii) BİRLEŞİK = set 1-5. Ek ölçü (ön kayıtta): EVET - eş = EVET'lerin eşli farkının sıfırdan farkı, işaret çevirme
permütasyonu (iki yönlü, 10.000). MUM_IZI_GOZ.py ve MUM_IZI11 çıktıları değişmez (içe alınır / okunur). GETİRİ bilgi; n < 30 'örneklem yetersiz'; 'iz / tuttu' yok;
kasa açılmaz. Veri <= 2022-12-31.

Komut:  python MUM_IZI_GOZ2.py ornek | onkayit | kos | pdf
EK 15 (kopma ayrımı; yeni getiri yok, mum_izi13_olay.csv gruplama):  python MUM_IZI_GOZ2.py kopma_sayim | kopma_onkayit | kopma
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
    ap.add_argument("komut", choices=["ornek", "onkayit", "kos", "pdf", "kopma_sayim", "kopma_onkayit", "kopma"])
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
    except (G2Hata, GZ.GZHata) as ex:
        g2log.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_g2_ana())
