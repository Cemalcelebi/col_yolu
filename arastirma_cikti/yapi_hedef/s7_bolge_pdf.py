"""s7_bolge_pdf — S7 (Y10) BÖLGE PDF'i, sonrası AÇIK (18 Kas 2026; Cemal: 'kodun yeni seçtiği bölgeleri görmek istiyorum').

Olaylar: olay_Y10.csv.gz içinden YALNIZ donem == '2016-22' (2023 ve 2024-26 olayları TUR 4 kör havuzudur, PDF'e GİRMEZ; betik durur):
ABD ve AVR'nin hepsi, BIST'ten --tohum (104) ile rastgele 10. Sıra ABD, AVR, BIST; pazar içinde tarih sırası.

Sayfa: sinyal öncesi 120 bar + giriş (t+1 açılış) + 30 bar sonrası; S6 hat (mavi) + S7 yakın tavan F21 = max High[t-15..t-1] (kırmızı kesik,
ozellik_Y1_s7.csv.gz) + kodun eski (S6) tavanı (gri ince, karşılaştırma) + +%5 / +%10 / stop0 çizgileri; sarı 15 bar penceresi; hacim.
Çizim hakem_ders_pdf.hd_grafik'in geometrisini ve denetimlerini aynen izler (hat / tavan / giriş / E0 olay dosyasıyla tutmalı); hd_grafik
120 bar öncesi ve F21 çizgisi çizmediği için burada genişletilmiş kopyası kullanılır (hd_grafik / HD_AYAR DEĞİŞTİRİLMEZ).

YENİ ÖLÇÜ YOK: h5 / h10 / st5 / k5 / kst / es_h5 / es_st5 olay dosyasından okunur; betik içi kapı olarak aynı olay YAPI_HEDEF.yh_sim ile
hissenin kendi geçerli barlarında yeniden simüle edilir ve h5 / st5 / k5 / kst satırla aynı olmak zorundadır (değilse DURUR).
'30 g en yüksek kapanış' = giriş günü dahil ilk 30 geçerli barın en yüksek kapanışı / giriş açılışı - 1 (bilgi; çizimden).
HİSSE ADI VE TARİH PDF'E GİRMEZ (yalnız pazar); pdftotext ile sızıntı kapısı betik içinde koşar.

--s9 (19 Kas 2026): aynı 50 olay, aynı sayfa + Ş9 çanağı: son 40 geçerli barın ([t-40, t-1]) Low serisine ikinci derece eğri (mor kalın
kesik), uyum dibi x* (mor nokta; pencere dışındaysa sınırda içi boş nokta), pencere sınırı (ince mor dikey). F24-F29 ozellik_Y1_s9.csv.gz'den
OKUNUR; eğri katsayıları Low'dan np.polyfit(derece 2) ile yeniden kurulur ve F24 = a / ATR250 (GOZ_ETIKET F3 tanımı) göreli 1e-3 ile tutmalı.
Başlık ikinci satırı 'Ş9: U DOĞRU' / 'Ş9: U DEĞİL — neden'; karar ve neden S7_S9_LISTE.md ile 50 / 50 BİREBİR aynı olmalı (değilse DURUR).
Çıktı S7_BOLGE_2016-22_S9.pdf; --s9'suz çıktı değişmez.

Kullanım:  OC_VERI=/tmp/veri python arastirma_cikti/yapi_hedef/s7_bolge_pdf.py [--cikti PDF] [--tohum 104] [--s9]
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_S7B = {k: id(v) for k, v in globals().items()}

import argparse  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

S7B_KLASOR = os.path.dirname(os.path.abspath(__file__))
S7B_KOK = os.path.abspath(os.path.join(S7B_KLASOR, "..", ".."))
for _p in (S7B_KOK, os.path.join(S7B_KOK, "arastirma_cikti", "goz_etiket")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import GOZ_ETIKET as GE  # noqa: E402  (yalnız okunur: ge_hazir, ge_gorsel_veri, OC.oc_veri)
import YAPI_HEDEF as YH  # noqa: E402  (yalnız okunur: yh_ozellik4_oku, yh_s7_sartlar, yh_sim, YH_ESIK)
import hakem_ders_pdf as HD  # noqa: E402  (yalnız okunur: HD_AYAR toleransları)

s7blog = logging.getLogger("col.s7_bolge_pdf")
if not s7blog.handlers:
    _h = logging.StreamHandler(sys.stderr)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s s7_bolge_pdf: %(message)s", "%H:%M:%S"))
    s7blog.addHandler(_h)
    s7blog.setLevel(logging.INFO)
    s7blog.propagate = False


class S7BHata(RuntimeError):
    """s7_bolge_pdf hatası: durur, yarım PDF yazılmaz."""


S7B_YOL = {
    "olay": os.path.join(S7B_KLASOR, "olay_Y10.csv.gz"),
    "cikti": os.path.join(S7B_KLASOR, "S7_BOLGE_2016-22.pdf"),
    "cikti_s9": os.path.join(S7B_KLASOR, "S7_BOLGE_2016-22_S9.pdf"),
    "s9_oz": os.path.join(S7B_KLASOR, "ozellik_Y1_s9.csv.gz"),
    "s9_liste": os.path.join(S7B_KLASOR, "S7_S9_LISTE.md"),
    "veri": os.environ.get("OC_VERI", "/tmp/veri"),
}
S7B_AYAR = {"donem": "2016-22", "kor_donem": ("2023", "2024-26"), "pazar_sira": ("ABD", "AVR", "BIST"), "bist_n": 10, "tohum": 104,
            "once": 120, "sonra": 30, "bilgi_bar": 30, "ufuk": 15, "hedef": (0.05, 0.10), "dpi_sayfa": 110, "azami_mb": 12.0,
            "tol": HD.HD_AYAR["hat_tol"]}
S7B_SART_AD = {"S1": "dipte", "S2": "hat net", "S3": "dip savunulmuş", "S4": "mumlar küçük", "S5": "alt fitil kısa",
               "S6": "kazan sağ kenarı dönmüş", "S7": "yakın tavan gövdeli kırılım", "S8": "yol almamış"}


# ================================================================ VERİ
def s7b_olaylar(tohum: int) -> pd.DataFrame:
    """olay_Y10 -> 2016-22 olayları (ABD, AVR hepsi; BIST rastgele bist_n) + Ş1-Ş8 / F14 bayrakları ve F21 (özellik dosyalarından)."""
    try:
        D = pd.read_csv(S7B_YOL["olay"], dtype={"sembol": str})
    except Exception as ex:
        raise S7BHata(f"olay dosyası okunamadı: {ex}") from ex
    D["tarih"] = pd.to_datetime(D.tarih); D["giris"] = pd.to_datetime(D.giris)
    if (D.deneme != "Y10").any():
        raise S7BHata("olay_Y10'da Y10 dışı deneme satırı")
    A = D[D.donem == S7B_AYAR["donem"]].copy()
    if A.empty or (A.tarih >= pd.Timestamp("2023-01-01")).any():
        raise S7BHata("2016-22 süzgeci: boş ya da 2023 sonrası tarih")
    parca = []
    for p in S7B_AYAR["pazar_sira"]:
        X = A[A.pazar == p].sort_values(["sembol", "tarih"]).reset_index(drop=True)
        if p == "BIST":
            if len(X) < S7B_AYAR["bist_n"]:
                raise S7BHata(f"BIST 2016-22 olayı {len(X)} < {S7B_AYAR['bist_n']}")
            X = X.sample(n=S7B_AYAR["bist_n"], random_state=int(tohum))
        parca.append(X.sort_values("tarih"))
    S = pd.concat(parca, ignore_index=True)
    # kör havuz kapısı (2023 / 2024-26 olayı yok)
    assert not S.donem.isin(S7B_AYAR["kor_donem"]).any() and (S.donem == S7B_AYAR["donem"]).all(), "kör havuz olayı PDF'e girdi"
    assert (S.tarih < pd.Timestamp("2023-01-01")).all(), "2023 sonrası tarih"
    if S.duplicated(["pazar", "sembol", "tarih"]).any():
        raise S7BHata("aynı olay iki kez")
    if not S.olc.astype(bool).all() or S[["h5", "st5", "es_h5", "es_st5"]].isna().any().any():
        raise S7BHata("ölçülemeyen olay var")
    # özellik dosyaları -> Ş1-Ş8, F14, F21
    F = YH.yh_ozellik4_oku()
    F = F.copy(); F["sembol"] = F.sembol.astype(str)
    M = S.merge(F, on=["pazar", "sembol", "tarih"], how="left", suffixes=("", "_oz"), validate="one_to_one", indicator=True)
    if (M._merge != "both").any():
        raise S7BHata(f"özellik satırı bulunamayan olay: {int((M._merge != 'both').sum())}")
    M = M.drop(columns="_merge")
    for k in YH._Y10_OZ:
        a, b = M[k].to_numpy(float), M[k + "_oz"].to_numpy(float)
        if not np.allclose(a, b, rtol=1e-4, atol=1e-9, equal_nan=True):
            raise S7BHata(f"{k}: olay dosyası ile özellik dosyası farklı")
    Fz = M[[k + "_oz" for k in YH._Y10_OZ]].copy(); Fz.columns = YH._Y10_OZ
    B = YH.yh_s7_sartlar(Fz)
    for k in list(S7B_SART_AD) + ["F14"]:
        M["b_" + k] = B[k]
    if not M[["b_" + k for k in S7B_SART_AD]].all().all():
        raise S7BHata("Y10 olayında Ş1-Ş8'den biri tutmuyor (olay kümesi ile özellik dosyası çelişiyor)")
    M["F21_ciz"] = M["F21_oz"]
    return M.reset_index(drop=True)


def s7b_ozet(D: pd.DataFrame, S: pd.DataFrame) -> List[Dict[str, Any]]:
    """Kapak tablosu (olay dosyasından): pazar 2016-22 tümü + PDF'teki BIST örneği + PDF toplamı."""
    A = D[D.donem == S7B_AYAR["donem"]]

    def sat(ad, X):
        return {"ad": ad, "n": int(len(X)), "h5": float(X.h5.mean()), "h10": float(X.h10.mean()), "es_h5": float(X.es_h5.mean()),
                "st5": float(X.st5.mean()), "es_st5": float(X.es_st5.mean())}
    out = [sat(f"{p} (2016-22 tümü)", A[A.pazar == p]) for p in S7B_AYAR["pazar_sira"]]
    out.append(sat(f"BIST (PDF'teki {S7B_AYAR['bist_n']}; tohum)", S[S.pazar == "BIST"]))
    out.append(sat(f"PDF toplamı ({len(S)} sayfa)", S))
    return out


# ================================================================ Ş9 (--s9): F24-F29 dosyadan, karar / neden S7_S9_LISTE.md ile birebir
S9_OZ = ["F24", "F25", "F26", "F27", "F28", "F29"]
S9_RENK = "#7b3294"


def s9_karar(r: pd.Series, T: Dict[str, float]) -> Dict[str, Any]:
    """F24-F29 -> ('U DOĞRU' | 'U DEĞİL', neden). Alt şart sırası a, b, c, d, e, f; a <= 0 ise yalnız 'çanak değil'. NaN tutmaz."""
    f = {k: float(r[k]) for k in S9_OZ}
    if not (np.isfinite(f["F24"]) and f["F24"] > T["F24_alt_acik"]):
        return {"karar": "U DEĞİL", "neden": "çanak değil (a<=0)"}
    n = []
    if not (f["F25"] >= T["F25_alt"] and f["F25"] <= T["F25_ust"]):
        n.append(f"dip kenarda (x* {f['F25']:.2f})")
    if not f["F26"] >= T["F26_min"]:
        n.append(f"uyum zayıf (R² {f['F26']:.2f})")
    if not f["F27"] >= T["F27_min"]:
        n.append(f"sol derinlik az ({f['F27']:.1f} ATR)")
    if not f["F28"] >= T["F28_min"]:
        n.append(f"sağ kalkmamış ({f['F28']:.1f} ATR)")
    if not abs(f["F29"]) <= T["F29_mutlak_ust"]:
        n.append(f"gerçek dip uyum dibinden uzak ({f['F29']:+.0f} bar)")
    return {"karar": "U DEĞİL" if n else "U DOĞRU", "neden": "; ".join(n)}


def s9_liste_oku(yol: str) -> Dict[int, Dict[str, str]]:
    """S7_S9_LISTE.md tablosu: | No | pazar | Ş9 | neden |."""
    try:
        txt = open(yol, encoding="utf-8").read()
    except OSError as ex:
        raise S7BHata(f"S7_S9_LISTE.md okunamadı: {ex}") from ex
    out: Dict[int, Dict[str, str]] = {}
    for ln in txt.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*(ABD|AVR|BIST)\s*\|\s*(U DOĞRU|U DEĞİL)\s*\|(.*)\|\s*$", ln)
        if m:
            no = int(m.group(1))
            if no in out:
                raise S7BHata(f"S7_S9_LISTE.md: No {no} iki kez")
            out[no] = {"pazar": m.group(2), "karar": m.group(3), "neden": m.group(4).strip()}
    return out


def s9_ekle(S: pd.DataFrame) -> pd.DataFrame:
    """S (no'lu 50 olay) + F24-F29 (ozellik_Y1_s9.csv.gz) + karar / neden; liste dosyasıyla 50 / 50 eşit değilse DURUR."""
    try:
        F = pd.read_csv(S7B_YOL["s9_oz"], dtype={"sembol": str})
    except Exception as ex:
        raise S7BHata(f"ozellik_Y1_s9 okunamadı: {ex}") from ex
    F["tarih"] = pd.to_datetime(F.tarih)
    if F.duplicated(["pazar", "sembol", "tarih"]).any():
        raise S7BHata("ozellik_Y1_s9: tekrar eden anahtar")
    M = S.drop(columns=[k for k in S9_OZ if k in S.columns]).merge(F[["pazar", "sembol", "tarih"] + S9_OZ], on=["pazar", "sembol", "tarih"],
                                                                     how="left", validate="one_to_one", indicator=True)
    if (M._merge != "both").any() or len(M) != len(S):
        raise S7BHata(f"F24-F29 bulunamayan olay: {int((M._merge != 'both').sum())}")
    M = M.drop(columns="_merge")
    assert (M.no.to_numpy() == S.no.to_numpy()).all(), "Ş9 birleştirmesi sırayı bozdu"
    T = YH.YH_ESIK["denemeler"]["Y11"]["esik"]
    K = [s9_karar(r, T) for _, r in M.iterrows()]
    M["s9_karar"] = [k["karar"] for k in K]; M["s9_neden"] = [k["neden"] for k in K]
    # YAPI_HEDEF'in kendi alt şartlarıyla da aynı karar
    A = YH.yh_s9_alt(M[S9_OZ].reset_index(drop=True))
    yh = np.all(np.vstack([np.asarray(v, bool) for v in A.values()]), axis=0)
    if not (yh == (M.s9_karar == "U DOĞRU").to_numpy()).all():
        raise S7BHata("Ş9 kararı YAPI_HEDEF.yh_s9_alt ile tutmadı")
    Lst = s9_liste_oku(S7B_YOL["s9_liste"])
    if sorted(Lst) != list(M.no.astype(int)):
        raise S7BHata(f"S7_S9_LISTE.md No kümesi ({len(Lst)}) olaylarla aynı değil")
    fark = [int(r.no) for _, r in M.iterrows()
            if (Lst[int(r.no)]["pazar"], Lst[int(r.no)]["karar"], Lst[int(r.no)]["neden"]) != (r.pazar, r.s9_karar, r.s9_neden)]
    esit = len(M) - len(fark)
    s7blog.info("Ş9 liste karşılaştırması: %d / %d eşit", esit, len(M))
    if fark:
        raise S7BHata(f"Ş9 karar / neden S7_S9_LISTE.md ile {esit} / {len(M)} eşit; farklı No: {fark[:10]}")
    return M


def s9_egri(r: pd.Series, d: pd.DataFrame) -> Dict[str, Any]:
    """[t-40, t-1] Low'a polyfit(2); ATR250 (GOZ_ETIKET F3 tanımı, pencereden önce) ile F24 / F25 / F26 / F29 dosyayla tutmalı."""
    Pz = YH.YH_ESIK["denemeler"]["Y11"]["s9_prm"]; n = int(Pz["pencere"])
    i = int(d.index.get_loc(pd.Timestamp(r.tarih))); w0 = i - n
    cnt = min(int(Pz["atr_gun"]), w0 - 1)
    if w0 < 0 or cnt < int(Pz["atr_min"]):
        raise S7BHata(f"No {r.no}: Ş9 penceresi / ATR geçmişi yok")
    H_, L_, C_ = (d[c].to_numpy(float) for c in ("High", "Low", "Close"))
    Hh, Ll, Cp = H_[w0 - cnt:w0], L_[w0 - cnt:w0], C_[w0 - cnt - 1:w0 - 1]
    atr = float(np.mean((np.maximum(Hh, Cp) - np.minimum(Ll, Cp)) / Cp)) * float(np.mean(C_[w0:i]))
    Lw = L_[w0:i]; x = np.arange(n, dtype=float)
    a, b, c = (float(v) for v in np.polyfit(x, Lw, 2))
    f24 = a / atr
    assert abs(f24 / float(r.F24) - 1) <= 1e-3, f"No {r.no}: F24 yeniden {f24:.6g} != dosya {float(r.F24):.6g}"
    u = a * x * x + b * x + c
    r2 = 1.0 - float(np.sum((Lw - u) ** 2)) / float(np.sum((Lw - Lw.mean()) ** 2))
    assert abs(r2 - float(r.F26)) <= 1e-3, f"No {r.no}: F26 yeniden {r2:.6g} != dosya {float(r.F26):.6g}"
    xs = np.nan
    if a > 0:
        xs = -b / (2.0 * a)
        assert abs(xs / (n - 1) - float(r.F25)) <= 1e-3 * max(1.0, abs(float(r.F25))), f"No {r.no}: F25 yeniden tutmadı"
        assert abs((float(np.argmin(Lw)) - xs) - float(r.F29)) <= 1e-2 * max(1.0, abs(float(r.F29))), f"No {r.no}: F29 yeniden tutmadı"
    return {"xr": x - n, "u": u, "a": a, "b": b, "c": c, "xs": xs, "n": n}


# ================================================================ KAPI: yeniden simülasyon
def s7b_sim_kapi(r: pd.Series, d: pd.DataFrame) -> None:
    """Hissenin kendi geçerli barlarıyla YH.yh_sim; h5 / st5 / k5 / kst satırla aynı olmalı."""
    gi = int(d.index.get_loc(pd.Timestamp(r.giris)))
    u = int(YH.YH_ESIK["olcu"]["ufuk"])
    W = d.iloc[gi:gi + u + 5]
    Cr = W.Close.to_numpy(float)[:, None]; Hr = W.High.to_numpy(float)[:, None]; Lr = W.Low.to_numpy(float)[:, None]
    R = YH.yh_sim(Cr, Hr, Lr, np.array([float(r.E0)]), np.array([float(r.stop0)]), int(r.yon))
    bek = {"h5": float(r.h5), "st5": float(r.st5), "k5": int(r.k5), "kst": int(r.kst)}
    bul = {"h5": float(R["h5"][0]), "st5": float(R["st5"][0]), "k5": int(R["k5"][0]), "kst": int(R["kst"][0])}
    assert bek == bul, f"yeniden simülasyon satırla tutmadı: {bek} != {bul}"


# ================================================================ GÖRSEL
def s7b_grafik(r: pd.Series, d: pd.DataFrame, yol: str, s9: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """hd_grafik geometrisi (sonra=30, bilgi_bar=30) + 120 bar öncesi + F21 (kırmızı kesik) + eski S6 tavanı (gri ince)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    once, sonra, bb, uf = S7B_AYAR["once"], S7B_AYAR["sonra"], S7B_AYAR["bilgi_bar"], S7B_AYAR["ufuk"]
    t = pd.Timestamp(r.tarih)
    G = GE.ge_gorsel_veri(d, t, hazir=True)
    if abs(G["hat"] / r.hat - 1) > S7B_AYAR["tol"] or abs(G["tavan"] / r.tavan - 1) > S7B_AYAR["tol"]:
        raise S7BHata(f"No {r.no}: kesik veride hat / tavan olay dosyasıyla tutmadı")
    i = int(d.index.get_loc(t)); gi = i + 1
    if gi >= len(d) or d.index[gi] != pd.Timestamp(r.giris):
        raise S7BHata(f"No {r.no}: giriş barı olay dosyasıyla tutmadı")
    O_, H_, L_, C_, V_ = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    E0 = O_[gi]
    if abs(E0 / r.E0 - 1) > S7B_AYAR["tol"]:
        raise S7BHata(f"No {r.no}: giriş açılışı olay dosyasıyla tutmadı")
    # F21 bağımsız: t'den önceki 15 geçerli barın en yüksek High'ı (çizim kapısı: 'tavan 15 bar tepesine oturuyor')
    f21 = float(np.max(H_[i - 15:i]))
    if abs(f21 / r.F21_ciz - 1) > 1e-4:
        raise S7BHata(f"No {r.no}: F21 veriden {f21} ozellik dosyasında {r.F21_ciz}")
    a = max(0, i - once); b = min(len(d), gi + sonra + 1)
    x = np.arange(a, b) - i; sl = slice(a, b)
    o, h, l, c, v = O_[sl], H_[sl], L_[sl], C_[sl], V_[sl]
    T5, T10 = E0 * (1 + S7B_AYAR["hedef"][0]), E0 * (1 + S7B_AYAR["hedef"][1])
    k10 = -1
    if r.h10 == 1:
        for k in range(uf):
            if gi + k < len(C_) and C_[gi + k] >= T10:
                k10 = k; break
    son30 = C_[gi:gi + bb]
    max30 = float(np.max(son30) / E0 - 1) if len(son30) else np.nan
    fig = plt.figure(figsize=(10.4, 5.3), dpi=S7B_AYAR["dpi_sayfa"])
    try:
        gs = fig.add_gridspec(2, 1, height_ratios=[3.3, 1], hspace=0.05)
        ax = fig.add_subplot(gs[0]); av = fig.add_subplot(gs[1], sharex=ax)
        renk = np.where(c >= o, "#1a9850", "#d73027")
        ax.axvspan(0.5, 0.5 + uf, color="#fee08b", alpha=0.30, zorder=0, label="15 bar penceresi")
        ax.vlines(x, l, h, colors=renk, linewidth=0.8, zorder=3)
        govde = np.maximum(np.abs(c - o), (h - l) * 0.01)
        ax.bar(x, govde, bottom=np.minimum(o, c), width=0.7, color=renk, edgecolor=renk, linewidth=0.4, zorder=4)
        sol = int(G["sol"]) - int(G["son"])
        x0 = max(sol, -once) - 0.5; x1 = -1 + 0.5
        ust = G["ust"] if np.isfinite(G["ust"]) else G["tavan"]
        ax.add_patch(Rectangle((x0, G["hat"]), x1 - x0, max(ust - G["hat"], 0.0), facecolor="#4575b4", alpha=0.10, edgecolor="#4575b4",
                               linewidth=0.6, zorder=1, label="S6 bölgesi"))
        ax.hlines(G["hat"], x0, 0.5, colors="#313695", linestyles="-", linewidth=1.3, zorder=5, label="S6 hat")
        ax.hlines(G["tavan"], x0, 0.5, colors="#888888", linestyles="-", linewidth=0.7, zorder=5, label="eski tavan (S6, karşılaştırma)")
        ax.hlines(r.F21_ciz, -15 - 0.5, 0.5, colors="#d7191c", linestyles="--", linewidth=1.5, zorder=6, label="S7 yakın tavan F21 (15 bar tepe)")
        xe = x[-1] + 0.5
        if s9 is not None:
            ax.axvline(-s9["n"] - 0.5, color=S9_RENK, linewidth=0.7, linestyle="-", alpha=0.8, zorder=2, label="Ş9 penceresi (son 40 bar)")
            ax.plot(s9["xr"], s9["u"], color=S9_RENK, linewidth=2.4, linestyle="--", zorder=6, label="Ş9 çanak (2. derece uyum)")
            if np.isfinite(s9["xs"]):
                xs = float(s9["xs"]); ic = 0.0 <= xs <= s9["n"] - 1; xc = min(max(xs, 0.0), float(s9["n"] - 1))
                uc = s9["a"] * xc * xc + s9["b"] * xc + s9["c"]
                ax.plot([xc - s9["n"]], [uc], marker="o", ms=8, color=S9_RENK if ic else "white", markeredgecolor=S9_RENK, markeredgewidth=1.8,
                        zorder=9, label="uyum dibi x*" if ic else "uyum dibi x* pencere dışı (sınırda)")
        ax.hlines(T5, 0.5, xe, colors="#1a9850", linestyles="--", linewidth=1.0, zorder=5, label="+%5")
        ax.hlines(T10, 0.5, xe, colors="#006837", linestyles=":", linewidth=1.3, zorder=5, label="+%10")
        ax.hlines(r.stop0, 0.5, xe, colors="#a50026", linestyles="-.", linewidth=1.0, zorder=5, label="stop0")
        ax.axvline(0, color="#555555", linewidth=0.7, linestyle=":", zorder=2)
        ax.plot([1], [E0], marker="o", ms=7, color="#2166ac", zorder=7, label="giriş (t+1 açılış)")
        if r.k5 >= 0 and r.h5 == 1:
            ax.plot([1 + r.k5], [C_[gi + int(r.k5)]], marker="*", ms=13, color="#1a9850", markeredgecolor="k", zorder=8, label=f"+%5 (gün +{int(r.k5)})")
        if k10 >= 0:
            ax.plot([1 + k10], [C_[gi + k10]], marker="*", ms=15, color="#006837", markeredgecolor="k", zorder=8, label=f"+%10 (gün +{k10})")
        if r.st5 == 1 and r.kst >= 0:
            ax.plot([1 + r.kst], [C_[gi + int(r.kst)]], marker="X", ms=11, color="#a50026", markeredgecolor="k", zorder=8,
                    label=f"STOP (gün +{int(r.kst)})")
        cb = int(r.cikis_bar)
        if 0 <= cb <= sonra and gi + cb < len(d):
            ax.plot([1 + cb], [E0 * (1 + r.getiri)], marker="v", ms=9, color="#762a83", markeredgecolor="k", zorder=8,
                    label=f"takip çıkışı ({r.cikis_tur}, {r.getiri * 100:+.1f}%)")
        if bb <= sonra:
            ax.axvline(bb + 0.5, color="#999999", linewidth=0.6, linestyle="-", zorder=2, label=f"{bb} bar sonu (gün +{bb - 1}; bilgi)")
        fig.legend(*ax.get_legend_handles_labels(), loc="lower center", fontsize=7, frameon=False, ncol=5, bbox_to_anchor=(0.5, -0.10))
        ax.grid(alpha=0.25, zorder=0); ax.set_ylabel("fiyat")
        plt.setp(ax.get_xticklabels(), visible=False)
        av.bar(x, v, width=0.7, color=renk, alpha=0.7)
        av.axvspan(0.5, 0.5 + uf, color="#fee08b", alpha=0.25)
        av.set_ylabel("hacim"); av.set_xlabel("bar (0 = sinyal günü t, giriş = bar 1)")
        av.ticklabel_format(axis="y", style="sci", scilimits=(0, 0)); av.grid(alpha=0.25)
        ax.set_xlim(x[0] - 1, x[-1] + 1)
        ylo = min(np.nanmin(l), r.stop0, G["hat"]); yhi = max(np.nanmax(h), T10)
        if s9 is not None:
            ylo = min(ylo, float(np.min(s9["u"])))
        ax.set_ylim(ylo - (yhi - ylo) * 0.04, yhi + (yhi - ylo) * 0.06)
        fig.savefig(yol, dpi=S7B_AYAR["dpi_sayfa"], bbox_inches="tight", metadata={"Software": None})
    finally:
        plt.close(fig)
    return {"k10": k10, "max30": max30}


# ================================================================ METİN
def s7b_sonuc(r: pd.Series, k10: int) -> str:
    if r.h5 == 1:
        s = f"+%5 (gün +{int(r.k5)})"
        if r.h10 == 1:
            s += f" / +%10 (gün +{k10})" if k10 >= 0 else " / +%10"
        return s
    if r.st5 == 1:
        return f"STOP (gün +{int(r.kst)})"
    return "gelmedi (15 günde ne +%5 ne stop)"


def s7b_sonuc_kapi(s: str, r: pd.Series) -> None:
    """Başlıktaki SONUÇ ile satırın h5 / st5 / k5 / kst aynı mı (betik içi assert)."""
    h5 = s.startswith("+%5"); st = s.startswith("STOP"); yok = s.startswith("gelmedi")
    assert h5 == (r.h5 == 1) and st == (r.st5 == 1) and yok == (r.h5 == 0 and r.st5 == 0), f"SONUÇ başlığı satırla çelişiyor: {s}"
    if h5:
        assert re.match(r"\+%5 \(gün \+(\d+)\)", s).group(1) == str(int(r.k5)), "k5 başlıkta farklı"
    if st:
        assert re.match(r"STOP \(gün \+(\d+)\)", s).group(1) == str(int(r.kst)), "kst başlıkta farklı"


def s7b_sart_satiri(r: pd.Series) -> str:
    p = [f"Ş{k[1:]} {ad} {'✓' if r['b_' + k] else '✗'}" for k, ad in S7B_SART_AD.items()]
    return "Şartlar: " + " · ".join(p) + f";  F14 büyük resim {'✓' if r.b_F14 else '✗'}"


# ================================================================ SIZINTI KAPISI
def s7b_sizinti(pdf: str, S: pd.DataFrame) -> Dict[str, int]:
    try:
        txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], check=True, capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError) as ex:
        raise S7BHata(f"pdftotext başarısız: {ex}") from ex
    tok = set(re.findall(r"[A-Za-z0-9.\-]+", txt))
    adlar = set()
    for s in S.sembol.astype(str):
        adlar.add(s); adlar.add(s.split(".")[0])
    adlar = {a for a in adlar if len(a) >= 2}
    sembol = sorted(a for a in adlar if a in tok)
    tarih = []
    for t in pd.concat([S.tarih, S.giris]):
        t = pd.Timestamp(t)
        for f in (t.strftime("%Y-%m-%d"), t.strftime("%d.%m.%Y"), t.strftime("%d/%m/%Y"), t.strftime("%Y%m%d")):
            if f in txt:
                tarih.append(f)
    yil = re.findall(r"\b(?:19|20)\d\d-\d\d-\d\d\b|\b\d\d\.\d\d\.(?:19|20)\d\d\b", txt)
    return {"sembol": len(sembol), "tarih": len(tarih) + len(yil), "sembol_liste": sembol[:5]}


# ================================================================ PDF
def s7b_pdf(cikti: Optional[str] = None, tohum: int = S7B_AYAR["tohum"], s9: bool = False) -> Dict[str, Any]:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.utils import simpleSplit
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    from PIL import Image
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = os.path.abspath(cikti or S7B_YOL["cikti_s9" if s9 else "cikti"])
    D = pd.read_csv(S7B_YOL["olay"], dtype={"sembol": str})
    S = s7b_olaylar(tohum)
    S["no"] = np.arange(1, len(S) + 1)
    if s9:
        S = s9_ekle(S)
    Z = s7b_ozet(D, S)
    is_k = tempfile.mkdtemp(prefix="s7_bolge_")
    try:
        ek: Dict[int, Dict[str, Any]] = {}
        for p in S7B_AYAR["pazar_sira"]:
            Vd = GE.OC.oc_veri(p, klasor=S7B_YOL["veri"])
            for _, r in S[S.pazar == p].iterrows():
                if r.sembol not in Vd["V"]:
                    raise S7BHata(f"No {r.no}: sembol veride yok")
                d = GE.ge_hazir(Vd["V"][r.sembol])
                s7b_sim_kapi(r, d)
                g = s7b_grafik(r, d, os.path.join(is_k, f"g{int(r.no):02d}.png"), s9_egri(r, d) if s9 else None)
                ek[int(r.no)] = g
            s7blog.info("grafik %s: %d", p, int((S.pazar == p).sum()))
            del Vd
        for ad, y in (("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), ("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
            if not os.path.exists(y):
                raise S7BHata(f"yazı tipi yok: {y}")
            pdfmetrics.registerFont(TTFont(ad, y))
        W, Hh = landscape(A4)
        tmp = cikti + ".tmp"
        cv = canvas.Canvas(tmp, pagesize=(W, Hh), invariant=1)
        cv.setTitle("S7 BÖLGE 2016-22" + (" Ş9" if s9 else "")); cv.setAuthor(""); cv.setCreator(""); cv.setProducer("")

        def yaz(x, y, s, f="DV", n=9, renk=(0, 0, 0)):
            cv.setFillColorRGB(*renk); cv.setFont(f, n); cv.drawString(x, y, s); cv.setFillColorRGB(0, 0, 0)

        def paragraf(x, y, s, gen, f="DV", n=9, ara=None, renk=(0, 0, 0)):
            ara = ara or n + 2.5
            for ln in simpleSplit(s, f, n, gen):
                yaz(x, y, ln, f, n, renk); y -= ara
            return y

        # ---------------- KAPAK
        npz = {p: int((S.pazar == p).sum()) for p in S7B_AYAR["pazar_sira"]}
        yaz(30, Hh - 38, f"S7 BÖLGELERİ — kodun yeni seçtiği bölgeler, sonrası açık ({len(S)} sayfa)", "DVB", 16)
        y = Hh - 62
        for s in (
            "S7 nedir: S6 taban kırılımı (Y1 olayı) + senin 8 kuralın birlikte: Ş1 dipte, Ş2 hat net, Ş3 dip savunulmuş, Ş4 mumlar küçük, "
            "Ş5 alt fitil kısa, Ş6 kazan sağ kenarı dönmüş, Ş7 yakın tavan (son 15 barın tepesi) gövdeli kırılım, Ş8 yol almamış. "
            "Sekizi birden tutan olay = Y10. F14 (büyük resim, 250 bar dipler yükseliyor) yalnız bilgi olarak yazılır.",
            "Neden 2016-22: 2023 ve 2024-26 olayları TUR 4 kör havuzudur; sana kör gösterilecekleri için burada YOK. "
            f"Bu PDF'te 2016-22'nin ABD olaylarının hepsi ({npz['ABD']}), AVR olaylarının hepsi ({npz['AVR']}) ve BIST'ten rastgele "
            f"{npz['BIST']} (tohum {tohum}) var. Sıra ABD, AVR, BIST; her pazarda tarih sırası. Hisse adı ve tarih yok.",
            "Grafik: sinyal öncesi 120 bar, giriş (ertesi gün açılış), sonrası 30 bar. Mavi = S6 hat, kırmızı kesik = S7 yakın tavan "
            "(son 15 barın en yüksek fiyatı), gri ince = kodun eski (S6) tavanı, yeşil kesik = +%5, koyu yeşil nokta = +%10, kırmızı "
            "nokta-çizgi = stop0; sarı = 15 bar penceresi. Sonuç 15 günde, kapanışla, stop'tan önce sayılır (olay dosyası).",
        ):
            y = paragraf(30, y, s, W - 60, n=9.5, ara=12.5) - 5
        y -= 6
        kol = [("Grup", 30), ("n", 255), ("+%5 payı", 300), ("+%10 payı", 375), ("eş payı (+%5)", 455), ("stop payı", 560), ("eş stop payı", 640)]
        for k, x in kol:
            yaz(x, y, k, "DVB", 10)
        cv.line(30, y - 4, 730, y - 4); y -= 18
        for z in Z:
            f = "DVB" if z["ad"].startswith("PDF") else "DV"
            vals = [z["ad"], str(z["n"]), f"%{z['h5'] * 100:.0f}", f"%{z['h10'] * 100:.0f}", f"%{z['es_h5'] * 100:.0f}",
                    f"%{z['st5'] * 100:.0f}", f"%{z['es_st5'] * 100:.0f}"]
            for (k, x), s in zip(kol, vals):
                yaz(x, y, s, f, 10)
            y -= 15
        if s9:
            y -= 4
            nd = {p: int(((S.pazar == p) & (S.s9_karar == "U DOĞRU")).sum()) for p in S7B_AYAR["pazar_sira"]}
            yaz(30, y, f"Ş9 (U DİP, mor): U DOĞRU {int((S.s9_karar == 'U DOĞRU').sum())} / {len(S)}  (ABD {nd['ABD']}, AVR {nd['AVR']}, "
                f"BIST {nd['BIST']})", "DVB", 11, (0.48, 0.20, 0.58)); y -= 14
            y = paragraf(30, y, "Ş9 nedir: sinyalden önceki son 40 barın dip (Low) fiyatlarına bir çanak eğrisi oturtulur (mor kesik). U DOĞRU için "
                         "altısı birden tutmalı: (1) çanak yukarı açık; (2) çanağın dibi pencerenin içinde, soldan 0,20 ile 0,75 arasında; "
                         "(3) eğri dipleri iyi izliyor (R² en az 0,40); (4) sol kol derin: pencerenin başı dibin en az 1 ATR üstünde; "
                         "(5) sağ kol kalkmış: pencerenin sonu dibin en az 0,5 ATR üstünde; (6) gerçek en düşük dip, çanağın dibinin ±5 bar "
                         "içinde. Mor nokta = çanağın dibi (içi boşsa dip pencerenin dışında, sınırda gösterilir); ince mor dikey = pencere "
                         "başı. Başlığın ikinci satırı karar ve tutmayan şartlardır (S7_S9_LISTE.md ile aynı).", W - 60, n=9, ara=11.5,
                         renk=(0.30, 0.10, 0.40)) - 2
        y -= 6
        yaz(30, y, "Eş payı = aynı giriş günü, aynı momentum x likidite kovasındaki öteki hisselerin aynı ölçüdeki payı (olay dosyası).", n=8,
            renk=(0.35, 0.35, 0.35)); y -= 22
        y = paragraf(30, y, "UYARI: n küçük, ÖLÇÜLEMEDİ. Bu PDF göz için: bölgenin nasıl seçildiğini görmek içindir, sonuç kanıtı değildir. "
                     "Evren bugün işlem gören hisseler (batanlar yok); hedef payı yukarı yanlı okunur.", W - 60, "DVB", 10.5, 14, (0.7, 0.0, 0.0))
        yaz(30, 22, "Kaynak: olay_Y10.csv.gz (donem 2016-22), ozellik_Y1.csv.gz + ozellik_Y1_s7.csv.gz (Ş1-Ş8, F14, F21). 'gün +k' = girişten sonraki "
            "k. geçerli bar (gün +0 = giriş günü).", n=7, renk=(0.35, 0.35, 0.35))
        cv.showPage()

        # ---------------- OLAY SAYFALARI
        basliklar = []
        for _, r in S.iterrows():
            g = ek[int(r.no)]
            sonuc = s7b_sonuc(r, g["k10"])
            s7b_sonuc_kapi(sonuc, r)
            baslik = (f"S7 bölge No {int(r.no)} — {r.pazar} — dönem {S7B_AYAR['donem']} — SONUÇ: {sonuc} — "
                      f"30 g en yüksek kapanış {g['max30'] * 100:+.1f}%")
            basliklar.append(baslik)
            rk = (0.0, 0.45, 0.0) if r.h5 == 1 else ((0.7, 0.0, 0.0) if r.st5 == 1 else (0.3, 0.3, 0.3))
            yy = Hh - 26
            for ln in simpleSplit(baslik, "DVB", 12, W - 50):
                yaz(25, yy, ln, "DVB", 12, rk); yy -= 14
            if s9:
                s9s = "Ş9: U DOĞRU" if r.s9_karar == "U DOĞRU" else f"Ş9: U DEĞİL — {r.s9_neden}"
                assert (r.s9_karar == "U DOĞRU") == (s9s == "Ş9: U DOĞRU"), "Ş9 başlığı kararla çelişiyor"
                for ln in simpleSplit(s9s, "DVB", 10.5, W - 50):
                    yaz(25, yy, ln, "DVB", 10.5, (0.48, 0.20, 0.58)); yy -= 12.5
            yaz(25, yy, f"eş payı (+%5) %{r.es_h5 * 100:.0f} · eş stop payı %{r.es_st5 * 100:.0f} · takip stoplu çıkış: {r.cikis_tur}, gün +{int(r.cikis_bar)}, "
                f"{r.getiri * 100:+.1f}%" + ("" if r.cikis_bar <= S7B_AYAR["sonra"] else " (grafik dışında)"), n=8.5, renk=(0.3, 0.3, 0.3))
            top = yy - 8; kutu_h = top - 48; kutu_w = W - 50
            gp = os.path.join(is_k, f"g{int(r.no):02d}.png")
            iw, ih = Image.open(gp).size
            sc = min(kutu_w / iw, kutu_h / ih); w_, h_ = iw * sc, ih * sc
            cv.drawImage(gp, 25 + (kutu_w - w_) / 2, top - h_, width=w_, height=h_)
            yb = top - h_ - 14
            for ln in simpleSplit(s7b_sart_satiri(r), "DV", 9.5, W - 50):
                yaz(25, yb, ln, "DV", 9.5); yb -= 12
            if yb < 6:
                raise S7BHata(f"No {r.no}: metin sayfaya sığmadı")
            cv.showPage()
        cv.save()
        mb = os.path.getsize(tmp) / 2 ** 20
        if mb > S7B_AYAR["azami_mb"]:
            os.remove(tmp)
            raise S7BHata(f"PDF {mb:.1f} MB > {S7B_AYAR['azami_mb']} MB")
        # kapılar: sayfa sayısı, sızıntı
        try:
            info = subprocess.run(["pdfinfo", tmp], check=True, capture_output=True, text=True).stdout
            sayfa = int(re.search(r"Pages:\s+(\d+)", info).group(1))
        except (OSError, subprocess.CalledProcessError, AttributeError) as ex:
            os.remove(tmp)
            raise S7BHata(f"pdfinfo başarısız: {ex}") from ex
        if sayfa != len(S) + 1:
            os.remove(tmp)
            raise S7BHata(f"sayfa {sayfa} != olay {len(S)} + 1")
        sz = s7b_sizinti(tmp, S)
        if sz["sembol"] or sz["tarih"]:
            os.remove(tmp)
            raise S7BHata(f"sızıntı: {sz}")
        os.replace(tmp, cikti)
    finally:
        shutil.rmtree(is_k, ignore_errors=True)
    return {"pdf": cikti, "mb": round(mb, 2), "sayfa": sayfa, "olay": {p: npz[p] for p in npz}, "sizinti": sz, "kapak": Z,
            "h5_toplam": int(S.h5.sum()), "st5_toplam": int(S.st5.sum()), "basliklar": basliklar,
            **({"s9_u_dogru": {p: int(((S.pazar == p) & (S.s9_karar == "U DOĞRU")).sum()) for p in S7B_AYAR["pazar_sira"]}} if s9 else {})}


# ================================================================ ÇAKIŞMA KAPISI ve KOMUT
def _cakisma_kontrol_s7b(_once=_CK_ONCE_S7B):
    """Bellekte (Colab exec) önceden var olan bir ad bu dosyayla ezildiyse durur."""
    g = globals()
    atla = {"_CK_ONCE_S7B", "_cakisma_kontrol_s7b", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit", "__builtins__",
            "__name__", "__doc__", "__file__", "__loader__", "__spec__", "__package__", "__cached__", "__annotations__"}
    ezilen = [k for k, i in _once.items() if k not in atla and k in g and id(g[k]) != i and not k.startswith("__")]
    if ezilen:
        raise S7BHata(f"çakışma kapısı: bellekteki adlar ezildi: {ezilen[:10]}")


_cakisma_kontrol_s7b()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="S7 bölge PDF'i (2016-22, sonrası 30 mum)")
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--tohum", type=int, default=S7B_AYAR["tohum"])
    ap.add_argument("--s9", action="store_true", help="Ş9 çanağı (ozellik_Y1_s9) + S7_S9_LISTE.md kararı; çıktı S7_BOLGE_2016-22_S9.pdf")
    a = ap.parse_args()
    try:
        R = s7b_pdf(a.cikti, a.tohum, a.s9)
        print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
    except (S7BHata, GE.GEHata, YH.YHHata, AssertionError) as ex:
        s7blog.error("%s", ex); sys.exit(1)
