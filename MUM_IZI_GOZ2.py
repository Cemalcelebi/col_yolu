"""MUM_IZI_GOZ2 — MUM_IZI EK 13: göz ölçümünün İKİNCİ BAKIŞI (26 Kasım 2026).

Ana modelin görevi: MUM_IZI11 göz ölçümü AYNI ön kayıtlı tanımlarla (MUM_IZI_GOZ.py GZ_ESIK; hiçbir tanım / eşik değişmez) set 5 (MUM_IZI12_ONAY: hakem v3'ün
seçtiği 24 bölge; Cemal EVET 11 / KISMEN 8 / HAYIR 5) eklenerek yeniden koşulur. Üç rapor ailesi: (i) İLK BAKIŞ = set 1-4 (MUM_IZI11 sonucu, değişmez; json'dan),
(ii) İKİNCİ BAKIŞ = yalnız set 5, (iii) BİRLEŞİK = set 1-5. Ek ölçü (ön kayıtta): EVET - eş = EVET'lerin eşli farkının sıfırdan farkı, işaret çevirme
permütasyonu (iki yönlü, 10.000). MUM_IZI_GOZ.py ve MUM_IZI11 çıktıları değişmez (içe alınır / okunur). GETİRİ bilgi; n < 30 'örneklem yetersiz'; 'iz / tuttu' yok;
kasa açılmaz. Veri <= 2022-12-31.

Komut:  python MUM_IZI_GOZ2.py ornek | onkayit | kos | pdf
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
    ap.add_argument("komut", choices=["ornek", "onkayit", "kos", "pdf"])
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
    except (G2Hata, GZ.GZHata) as ex:
        g2log.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_g2_ana())
