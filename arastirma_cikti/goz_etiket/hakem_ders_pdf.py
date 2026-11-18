"""hakem_ders_pdf — HAKEM DERS PDF'i (18 Kas 2026; iş tanımı HAKEM_DERS_PDF_IS_TANIMI.md).

Cemal'in el yazısıyla işaretlediği hakem PDF'inin her sayfası (pdftoppm 110 dpi) sol yarıya, AYNI olayın SONRASI AÇIK grafiği
sağ yarıya konur; başlıkta karar / sonuç / puan, altta Cemal'in notu, vekilin kararı + neden kodları ve DERS (HAKEM_DERSLER.md).
Kapak: puan tablosu + aynı hatayı yapmama listesi + göz aşinalığı notu. Son sayfa: 40 satırlık özet tablo.

YENİ ÖLÇÜ YOK: sonuç sayıları olay_Y1.csv.gz satırından (h5, h10, st5, k5, kst, getiri, cikis_bar, cikis_tur, es_h5) okunur.
Grafikteki '+%10 günü' işareti yalnız h10 = 1 olan olayda, giriş sonrası ilk 15 geçerli barda kapanışın giriş x 1,10'u ilk geçtiği bar
olarak ÇİZİM için bulunur (h10 bilgisi olay dosyasından gelir; ölçü değil).
Kimlik zinciri: hakem_anahtar.json sayfa -> no -> anahtar.json olay (pazar, sembol, tarih) -> olay_Y1 satırı. HİSSE ADI / TARİH PDF'E GİRMEZ.
Bölge (hat / tavan / S6 alanı) GOZ_ETIKET.ge_gorsel_veri ile t'de KESİLMİŞ veriden üretilir ve olay dosyasıyla aynı olmak zorundadır.

Kullanım:  OC_VERI=/tmp/veri python arastirma_cikti/goz_etiket/hakem_ders_pdf.py --cemal-pdf YOL [--cikti PDF] [--is KLASOR]
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_HD = {k: id(v) for k, v in globals().items()}

import argparse  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HD_KLASOR = os.path.dirname(os.path.abspath(__file__))
HD_KOK = os.path.abspath(os.path.join(HD_KLASOR, "..", ".."))
if HD_KOK not in sys.path:
    sys.path.insert(0, HD_KOK)

import GOZ_ETIKET as GE  # noqa: E402  (yalnız okunur: ge_hazir, ge_gorsel_veri, OC.oc_veri)

hdlog = logging.getLogger("col.hakem_ders")
if not hdlog.handlers:
    _h = logging.StreamHandler(sys.stderr)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s hakem_ders: %(message)s", "%H:%M:%S"))
    hdlog.addHandler(_h)
    hdlog.setLevel(logging.INFO)
    hdlog.propagate = False


class HDHata(RuntimeError):
    """hakem_ders_pdf hatası: durur, yarım PDF yazılmaz."""


HD_YOL = {
    "cevap": os.path.join(HD_KLASOR, "hakem_cevap_cemal.json"),
    "hakem_anahtar": os.path.join(HD_KLASOR, "hakem_anahtar.json"),
    "anahtar": os.path.join(HD_KLASOR, "anahtar.json"),
    "dersler": os.path.join(HD_KLASOR, "HAKEM_DERSLER.md"),
    "olay": os.path.join(HD_KOK, "arastirma_cikti", "yapi_hedef", "olay_Y1.csv.gz"),
    "cikti": os.path.join(HD_KLASOR, "HAKEM_DERS_2026-11-18.pdf"),
    "veri": os.environ.get("OC_VERI", "/tmp/veri"),
}
HD_AYAR = {"once": 60, "sonra": 20, "ufuk": 15, "hedef": (0.05, 0.10), "dpi_sayfa": 110, "dpi_grafik": 150,
           "e0_tol": GE.GE_ESIK["denetim"]["hat_tol"], "hat_tol": GE.GE_ESIK["denetim"]["hat_tol"], "azami_mb": 15.0}

# HAKEM_DERSLER.md §1-§3'ten (sayfa eşlemesi orada). Metinler kısaltılmıştır; kod md'de bulunmazsa betik durur.
HD_DERS_METIN = {
    "CD1": "Fitil teorisi yön vermez: üst / alt fitil okuması iki sayfada iki yönde yanılttı (s1, s5). Fitil, bağlam (dipte mi tepede mi) olmadan okunmaz.",
    "CD2": "'Tepede dikkat' uyarısını kendi kararına uygula: tepede raf = OLMAZ ya da BELİRSİZ, OLUR değil (s6).",
    "CD3": "Kazan çizmek yetmez; sağ kenarın döndüğü (yükseldiği) görülmeli; kendi D4 kuralın (s14).",
    "CD4": "Yükselen trendde kısa raf (yol almış) bazen koşar; 'dip savunması yok' tek başına eleme nedeni değil (s11; n 1).",
    "CD5": "En güzel görünen tabanlar (uzun, düzgün, gövdeli kırılım, parmak izi) stop oldu (s25, s28): şekil güzelliği sonuç garantisi değil.",
    "CD6": "'Kapanış tavana ancak değiyor' elemesine katıldın, hedef geldi (s35): bu eleme bir kez yanılttı.",
    "CD7": "'İki gün kapanış teyidi' doğru refleks: teyitsiz girilseydi 15 gün sönük kalırdı (s24).",
    "VD1": "Kuralların toplamı Cemal'in gözü değil: 'bütün kurallar tutuyor' diye vekilin OLUR dediği sayfaların hiçbiri +%5 görmedi.",
    "VD2": "Stop uzaklığı (%10) ve kırılım payı süzgeçleri hedefe gidenleri eledi; Cemal stop 'çok büyük' derken ~%25'i kastediyor, kırılımda iki gün teyit istiyor.",
    "VD3": "Vekilin BELİRSİZ grubu en iyi grup: lehte-aleyhte kural sayımı gerçek yapıları 'kararsız'a atıyor. Karar = bağlam (dipte / tepede) + yapı + dönüş.",
}
# sayfa -> (Cemal dersi, vekil dersi). HAKEM_DERSLER.md tabloları; 5 ve 6 vekil satırları md'de yoktu (bkz. rapor HATA), burada eklendi.
HD_DERS_SAYFA: Dict[int, Tuple[Optional[str], Optional[str]]] = {
    1: ("CD1", None), 5: ("CD1", "VD2"), 6: ("CD2", "VD1"), 14: ("CD3", None), 11: ("CD4", "VD3"), 25: ("CD5", "VD1"), 28: ("CD5", "VD1"),
    35: ("CD6", "VD2"), 24: ("CD7", None), 9: (None, "VD1"), 15: (None, "VD1"), 23: (None, "VD1"), 2: (None, "VD2"), 4: (None, "VD2"),
    26: (None, "VD2"), 30: (None, "VD2"), 33: (None, "VD2"), 10: (None, "VD3"), 16: (None, "VD3"), 19: (None, "VD3"), 21: (None, "VD3"),
}
HD_TERS = {"OLMAZ": "OLUR", "OLUR": "OLMAZ", "BELİRSİZ": "OLMAZ"}


# ================================================================ VERİ
def _hd_json(yol: str) -> Dict[str, Any]:
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as ex:
        raise HDHata(f"okunamadı: {yol}: {ex}") from ex


def hd_puan(karar: str, h5: float) -> int:
    """CLAUDE.md Hakem turları: OLUR & +%5 = +1, OLUR & yok = -1, OLMAZ & yok = +1, OLMAZ & geldi = -1, öteki = 0."""
    if karar == "OLUR":
        return 1 if h5 == 1 else -1
    if karar == "OLMAZ":
        return 1 if h5 == 0 else -1
    return 0


def hd_tablo() -> pd.DataFrame:
    """40 sayfa: kimlik zinciri + Cemal ham / etkin karar + vekil + olay_Y1 sonuç sütunları + puanlar + ders kodları."""
    C = _hd_json(HD_YOL["cevap"]); HA = _hd_json(HD_YOL["hakem_anahtar"])["sayfa"]; A = _hd_json(HD_YOL["anahtar"])["olay"]
    Y = pd.read_csv(HD_YOL["olay"], dtype={"tarih": str})
    Y = Y.set_index(["pazar", "sembol", "tarih"])
    if not Y.index.is_unique:
        raise HDHata("olay_Y1 (pazar, sembol, tarih) tekil değil")
    md = open(HD_YOL["dersler"], encoding="utf-8").read()
    for k in HD_DERS_METIN:
        if k not in md:
            raise HDHata(f"ders kodu {k} HAKEM_DERSLER.md'de yok")
    sat = []
    for s in range(1, len(HA) + 1):
        h = HA[str(s)]; o = A[str(h["no"])]
        kor = h["yari"] == "KÖR"
        cv = (C["kor"] if kor else C["acik"]).get(str(s))
        if cv is None:
            raise HDHata(f"sayfa {s}: Cemal yanıtı kaydı yok")
        key = (o["pazar"], o["sembol"], o["tarih"])
        if key not in Y.index:
            raise HDHata(f"sayfa {s}: olay_Y1 satırı yok")
        r = Y.loc[key]
        if not bool(r["olc"]):
            raise HDHata(f"sayfa {s}: olay 15 barda ölçülebilir değil")
        ham = cv["cevap"]
        if kor:
            etkin = ham if ham in ("OLUR", "OLMAZ", "BELİRSİZ") else "-"
        else:
            etkin = h["karar"] if ham == "DOĞRU" else (HD_TERS[h["karar"]] if ham == "YANLIŞ" else "-")
        h5 = float(r["h5"])
        cd, vd = HD_DERS_SAYFA.get(s, (None, None))
        sat.append({"sayfa": s, "yari": h["yari"], "no": int(h["no"]), "pazar": o["pazar"], "sembol": o["sembol"], "tarih": o["tarih"],
                    "giris": o["giris"], "cemal_ham": ham, "cemal_tur": cv.get("tur", ""), "cemal_not": cv.get("not", ""), "cemal": etkin,
                    "vekil": h["karar"], "nedenler": list(h["nedenler"]), "h5": h5, "h10": float(r["h10"]), "st5": float(r["st5"]),
                    "k5": int(r["k5"]), "kst": int(r["kst"]), "getiri": float(r["getiri"]), "cikis_bar": int(r["cikis_bar"]),
                    "cikis_tur": str(r["cikis_tur"]), "es_h5": float(r["es_h5"]), "hat": float(r["hat"]), "tavan": float(r["tavan"]),
                    "stop0": float(r["stop0"]), "E0": float(r["E0"]), "puan_c": hd_puan(etkin, h5), "puan_v": hd_puan(h["karar"], h5),
                    "cd": cd or "", "vd": vd or ""})
    T = pd.DataFrame(sat)
    if len(T) != 40:
        raise HDHata(f"40 sayfa bekleniyordu, {len(T)}")
    return T


def hd_puan_ozet(T: pd.DataFrame) -> List[Dict[str, Any]]:
    """Kör / açık / toplam x Cemal / vekil: karar, +1, -1, başarı, karar dışı, taban (eş payına göre beklenen başarı)."""
    out = []
    for ad, m in (("Kör yarı (1-20)", T.yari == "KÖR"), ("Açık yarı (21-40)", T.yari == "AÇIK"), ("Toplam (40)", T.yari.notna())):
        for kim, kk, pk in (("Cemal", "cemal", "puan_c"), ("Vekil", "vekil", "puan_v")):
            D = T[m]; k = D[D[kk].isin(["OLUR", "OLMAZ"])]
            art, eks = int((k[pk] == 1).sum()), int((k[pk] == -1).sum())
            beklenen = np.where(k[kk] == "OLUR", k.es_h5, 1 - k.es_h5)
            olur = k[k[kk] == "OLUR"]
            out.append({"bolum": ad, "kim": kim, "karar": len(k), "arti": art, "eksi": eks, "basari": art / len(k) if len(k) else np.nan,
                        "taban": float(np.mean(beklenen)) if len(k) else np.nan, "disi": int(len(D) - len(k)),
                        "olur_n": len(olur), "olur_isabet": float((olur.h5 == 1).mean()) if len(olur) else np.nan})
    return out


# ================================================================ GÖRSEL
def hd_sayfa_png(cemal_pdf: str, klasor: str, dpi: int) -> List[str]:
    """Cemal'in PDF'i -> sayfa PNG'leri (pdftoppm). 40 sayfa değilse durur."""
    if not os.path.exists(cemal_pdf):
        raise HDHata(f"Cemal'in PDF'i yok: {cemal_pdf}")
    os.makedirs(klasor, exist_ok=True)
    try:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", cemal_pdf, os.path.join(klasor, "s")], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError) as ex:
        raise HDHata(f"pdftoppm başarısız: {ex}") from ex
    ps = sorted(p for p in os.listdir(klasor) if re.fullmatch(r"s-\d+\.png", p))
    if len(ps) != 40:
        raise HDHata(f"Cemal'in PDF'inden 40 sayfa bekleniyordu, {len(ps)}")
    return [os.path.join(klasor, p) for p in ps]


def hd_kirp(yol: str, cikis: str) -> str:
    """Sayfa görüntüsünü beyaz kenarlardan kırpar (içerik değişmez)."""
    from PIL import Image, ImageChops
    im = Image.open(yol).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bb = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
    if bb:
        pad = 8
        im = im.crop((max(0, bb[0] - pad), max(0, bb[1] - pad), min(im.width, bb[2] + pad), min(im.height, bb[3] + pad)))
    im.save(cikis, optimize=True)
    return cikis


def hd_grafik(r: pd.Series, d: pd.DataFrame, yol: str) -> Dict[str, Any]:
    """Sonrası açık grafik: t-60 .. t+1+20 bar; S6 bölgesi (t'de kesik veriden), giriş, +%5 / +%10, stop0, 15 bar penceresi, olaylar."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    t = pd.Timestamp(r.tarih)
    G = GE.ge_gorsel_veri(d, t, hazir=True)
    if abs(G["hat"] / r.hat - 1) > HD_AYAR["hat_tol"] or abs(G["tavan"] / r.tavan - 1) > HD_AYAR["hat_tol"]:
        raise HDHata(f"sayfa {r.sayfa}: kesik veride hat / tavan olay dosyasıyla tutmadı")
    i = int(d.index.get_loc(t)); gi = i + 1
    if gi >= len(d) or d.index[gi] != pd.Timestamp(r.giris):
        raise HDHata(f"sayfa {r.sayfa}: giriş barı anahtar.json ile tutmadı")
    O_, H_, L_, C_, V_ = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    E0 = O_[gi]
    if abs(E0 / r.E0 - 1) > HD_AYAR["e0_tol"]:
        raise HDHata(f"sayfa {r.sayfa}: giriş açılışı olay dosyasıyla tutmadı")
    a = max(0, i - HD_AYAR["once"]); b = min(len(d), gi + HD_AYAR["sonra"] + 1)
    x = np.arange(a, b) - i; sl = slice(a, b)
    o, h, l, c, v = O_[sl], H_[sl], L_[sl], C_[sl], V_[sl]
    T5, T10 = E0 * (1 + HD_AYAR["hedef"][0]), E0 * (1 + HD_AYAR["hedef"][1])
    k10 = -1
    if r.h10 == 1:
        for k in range(HD_AYAR["ufuk"]):
            if gi + k < len(C_) and C_[gi + k] >= T10:
                k10 = k; break
    fig = plt.figure(figsize=(7.2, 5.2), dpi=HD_AYAR["dpi_grafik"])
    try:
        gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1], hspace=0.05)
        ax = fig.add_subplot(gs[0]); av = fig.add_subplot(gs[1], sharex=ax)
        renk = np.where(c >= o, "#1a9850", "#d73027")
        ax.axvspan(0.5, 0.5 + HD_AYAR["ufuk"], color="#fee08b", alpha=0.25, zorder=0, label="15 bar penceresi")
        ax.vlines(x, l, h, colors=renk, linewidth=0.9, zorder=3)
        govde = np.maximum(np.abs(c - o), (h - l) * 0.01)
        ax.bar(x, govde, bottom=np.minimum(o, c), width=0.7, color=renk, edgecolor=renk, linewidth=0.5, zorder=4)
        # S6 bölgesi: ge_ciz ile aynı geometri (sol..t-1), t'de kesik veriden
        sol = int(G["sol"]) - int(G["son"]) + 0  # t'ye göre bar sırası
        x0 = max(sol, -HD_AYAR["once"]) - 0.5; x1 = -1 + 0.5
        ust = G["ust"] if np.isfinite(G["ust"]) else G["tavan"]
        ax.add_patch(Rectangle((x0, G["hat"]), x1 - x0, max(ust - G["hat"], 0.0), facecolor="#4575b4", alpha=0.13, edgecolor="#4575b4",
                               linewidth=0.8, zorder=1, label="S6 bölgesi"))
        ax.hlines(G["tavan"], x0, 0.5, colors="#f46d43", linestyles="--", linewidth=1.1, zorder=5, label="tavan")
        ax.hlines(G["hat"], x0, 0.5, colors="#313695", linestyles="-", linewidth=1.1, zorder=5, label="hat")
        xe = x[-1] + 0.5
        ax.hlines(T5, 0.5, xe, colors="#1a9850", linestyles="--", linewidth=1.0, zorder=5, label="+%5")
        ax.hlines(T10, 0.5, xe, colors="#006837", linestyles=":", linewidth=1.3, zorder=5, label="+%10")
        ax.hlines(r.stop0, 0.5, xe, colors="#a50026", linestyles="-.", linewidth=1.0, zorder=5, label="stop0")
        ax.axvline(0, color="#555555", linewidth=0.7, linestyle=":", zorder=2)
        ax.plot([1], [E0], marker="o", ms=7, color="#2166ac", zorder=7, label="giriş (t+1 açılış)")
        if r.k5 >= 0:
            ax.plot([1 + r.k5], [C_[gi + r.k5]], marker="*", ms=13, color="#1a9850", markeredgecolor="k", zorder=8, label=f"+%5 (gün +{r.k5})")
        if k10 >= 0:
            ax.plot([1 + k10], [C_[gi + k10]], marker="*", ms=15, color="#006837", markeredgecolor="k", zorder=8, label=f"+%10 (gün +{k10})")
        if r.st5 == 1 and r.kst >= 0:
            ax.plot([1 + r.kst], [C_[gi + r.kst]], marker="X", ms=11, color="#a50026", markeredgecolor="k", zorder=8, label=f"STOP (gün +{r.kst})")
        cb = int(r.cikis_bar); xc = 1 + cb
        if cb >= 0 and gi + cb < len(d) and cb <= HD_AYAR["sonra"]:
            yc = E0 * (1 + r.getiri)
            ax.plot([xc], [yc], marker="v", ms=10, color="#762a83", markeredgecolor="k", zorder=8,
                    label=f"takip çıkışı ({r.cikis_tur}, {r.getiri * 100:+.1f}%)")
        ax.set_title(f"{r.pazar} · sonrası açık (bar 0 = sinyal günü t, giriş = bar 1)", fontsize=10)
        fig.legend(*ax.get_legend_handles_labels(), loc="lower center", fontsize=7, frameon=False, ncol=4, bbox_to_anchor=(0.5, -0.12))
        ax.grid(alpha=0.25, zorder=0); ax.set_ylabel("fiyat")
        plt.setp(ax.get_xticklabels(), visible=False)
        av.bar(x, v, width=0.7, color=renk, alpha=0.7)
        av.axvspan(0.5, x[-1] + 0.5, color="#fee08b", alpha=0.15)
        av.set_ylabel("hacim"); av.set_xlabel("bar")
        av.ticklabel_format(axis="y", style="sci", scilimits=(0, 0)); av.grid(alpha=0.25)
        ax.set_xlim(x[0] - 1, x[-1] + 1)
        ylo = min(np.nanmin(l), r.stop0, G["hat"]); yhi = max(np.nanmax(h), T10)
        ax.set_ylim(ylo - (yhi - ylo) * 0.04, yhi + (yhi - ylo) * 0.06)
        fig.savefig(yol, dpi=HD_AYAR["dpi_grafik"], bbox_inches="tight", metadata={"Software": None})
    finally:
        plt.close(fig)
    return {"k10": k10, "cikis_grafikte": bool(0 <= cb <= HD_AYAR["sonra"])}


# ================================================================ METİN
def hd_sonuc_metni(r: pd.Series, k10: int) -> str:
    if r.h5 == 1:
        s = f"+%5 gün +{r.k5}" + (f" / +%10 gün +{k10}" if r.h10 == 1 and k10 >= 0 else (" / +%10" if r.h10 == 1 else ""))
    elif r.st5 == 1:
        s = f"STOP gün +{r.kst}"
    else:
        s = "sönük (15 günde ne +%5 ne stop)"
    return s


def hd_takip_metni(r: pd.Series) -> str:
    return f"takip stoplu çıkış: {r.cikis_tur}, gün +{r.cikis_bar}, {r.getiri * 100:+.1f}%" + ("" if r.cikis_bar <= HD_AYAR["sonra"] else " (grafik dışında)")


def _pz(p: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}[int(p)]


def hd_cemal_baslik(r: pd.Series) -> str:
    if r.yari == "KÖR":
        return f"Cemal (kör): {r.cemal if r.cemal != '-' else 'yanıtsız'}"
    if r.cemal_ham == "-":
        return f"Cemal (açık): yanıtsız (vekil kararı: {r.vekil})"
    return f"Cemal (açık): {r.cemal_ham} (vekil kararı: {r.vekil}) -> etkin {r.cemal}"


def hd_dogru_cumle(r: pd.Series) -> str:
    """Ders kodu olmayan sayfa için 'doğru karar: ...' tek cümle (hangi kural / gözlem tuttu)."""
    notu = re.sub(r"^B (OLUR|OLMAZ|BELİRSİZ) dedi; ", "", str(r.cemal_not).strip()).strip("'")
    if r.puan_c == 1 and r.cemal == "OLUR":
        return f"doğru karar: OLUR; gözün tuttu ({notu[:110]}), +%5 gün +{r.k5} geldi."
    if r.puan_c == 1 and r.cemal == "OLMAZ":
        return f"doğru karar: OLMAZ; eleme tuttu ({notu[:110]}), 15 günde +%5 gelmedi."
    if r.cemal in ("BELİRSİZ", "-"):
        ne = "+%5 geldi" if r.h5 == 1 else "+%5 gelmedi"
        return f"karar yok (puan 0): sonuç {ne}; bu şekil bir sonraki turda karar verilecek şekil olarak not edilir."
    return "—"


# ================================================================ PDF
def hd_pdf(cemal_pdf: str, cikti: Optional[str] = None, is_klasor: Optional[str] = None) -> Dict[str, Any]:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.utils import simpleSplit
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or HD_YOL["cikti"]
    if os.path.abspath(is_klasor or "/").startswith(HD_KOK + os.sep):
        raise HDHata("ara klasör repo içinde olamaz")
    is_klasor = is_klasor or tempfile.mkdtemp(prefix="hakem_ders_")
    T = hd_tablo(); P = hd_puan_ozet(T)
    sayfa_png = hd_sayfa_png(cemal_pdf, os.path.join(is_klasor, "sayfa"), HD_AYAR["dpi_sayfa"])
    os.makedirs(os.path.join(is_klasor, "graf"), exist_ok=True)
    ek: Dict[int, Dict[str, Any]] = {}
    for p in sorted(T.pazar.unique()):
        Vd = GE.OC.oc_veri(p, klasor=HD_YOL["veri"])
        for _, r in T[T.pazar == p].iterrows():
            if r.sembol not in Vd["V"]:
                raise HDHata(f"sayfa {r.sayfa}: sembol veride yok")
            d = GE.ge_hazir(Vd["V"][r.sembol])
            g = hd_grafik(r, d, os.path.join(is_klasor, "graf", f"g{r.sayfa:02d}.png"))
            g["sol_png"] = hd_kirp(sayfa_png[r.sayfa - 1], os.path.join(is_klasor, "graf", f"c{r.sayfa:02d}.png"))
            ek[int(r.sayfa)] = g
        hdlog.info("grafik %s: %d", p, int((T.pazar == p).sum()))
        del Vd
    T["k10"] = [ek[s]["k10"] for s in T.sayfa]

    for ad, y in (("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), ("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
        if not os.path.exists(y):
            raise HDHata(f"yazı tipi yok: {y}")
        pdfmetrics.registerFont(TTFont(ad, y))
    W, Hh = landscape(A4)
    tmp = cikti + ".tmp"
    cv = canvas.Canvas(tmp, pagesize=(W, Hh), invariant=1)
    cv.setTitle("HAKEM DERS 2026-11-18"); cv.setAuthor(""); cv.setCreator(""); cv.setProducer("")

    def yaz(x, y, s, f="DV", n=9, renk=(0, 0, 0)):
        cv.setFillColorRGB(*renk); cv.setFont(f, n); cv.drawString(x, y, s); cv.setFillColorRGB(0, 0, 0)

    def paragraf(x, y, s, gen, f="DV", n=8, ara=None, renk=(0, 0, 0)):
        ara = ara or n + 2
        for ln in simpleSplit(s, f, n, gen):
            yaz(x, y, ln, f, n, renk); y -= ara
        return y

    # ---------------- KAPAK
    yaz(30, Hh - 36, "HAKEM DERSİ — 18 Kasım 2026: senin çizimlerin + sonrası + puan + ders", "DVB", 15)
    yaz(30, Hh - 52, "40 sayfa: solda senin işaretlediğin hakem sayfası (aynen), sağda aynı olayın 15 gün sonrası. Hisse adı ve tarih yok; yalnız pazar.", n=9)
    yaz(30, Hh - 64, "Puan: OLUR ve 15 günde +%5 stop'tan önce geldi = +1, gelmedi = -1; OLMAZ ve gelmedi = +1, geldi = -1; BELİRSİZ / yanıtsız = 0 (karar dışı).", n=8)
    yaz(30, Hh - 75, "Açık yarıda etkin kararın: DOĞRU = vekilin kararı; YANLIŞ = tersi (OLMAZ -> OLUR; OLUR / BELİRSİZ -> OLMAZ). Taban = eş payına göre beklenen başarı (aynı gün aynı kova).", n=8)
    kol = [("Bölüm", 30), ("Kim", 150), ("Karar", 205), ("+1", 250), ("-1", 285), ("Başarı", 320), ("Taban", 375), ("OLUR isabeti", 430), ("Karar dışı", 515)]
    y = Hh - 98
    for k, x in kol:
        yaz(x, y, k, "DVB", 9)
    cv.line(30, y - 4, 575, y - 4); y -= 16
    for p in P:
        renk = (0.0, 0.35, 0.0) if p["kim"] == "Cemal" else (0.15, 0.15, 0.45)
        f = "DVB" if p["bolum"].startswith("Toplam") else "DV"
        vals = [p["bolum"], p["kim"], str(p["karar"]), str(p["arti"]), str(p["eksi"]), f"%{p['basari'] * 100:.0f}", f"%{p['taban'] * 100:.0f}",
                f"{int(round(p['olur_isabet'] * p['olur_n'])) if p['olur_n'] else 0} / {p['olur_n']}", str(p["disi"])]
        for (k, x), s in zip(kol, vals):
            yaz(x, y, s, f, 9, renk)
        y -= 13
        if p["kim"] == "Vekil":
            y -= 3
    y -= 4
    tc = next(p for p in P if p["bolum"].startswith("Toplam") and p["kim"] == "Cemal")
    tv = next(p for p in P if p["bolum"].startswith("Toplam") and p["kim"] == "Vekil")
    y = paragraf(30, y, f"Sonuç: sen {tc['karar']} kararda %{tc['basari'] * 100:.0f} (taban %{tc['taban'] * 100:.0f}); vekil {tv['karar']} kararda "
                 f"%{tv['basari'] * 100:.0f} (taban %{tv['taban'] * 100:.0f}). 40 sayfanın +%5 payı %{T.h5.mean() * 100:.0f}. n küçük; "
                 "dersler SINANMADI, kural değil (hedef %80-90; birikimli sayım TUR_DEFTERI'nde).", 545, "DVB", 8.5)
    # sağ sütun: aynı hatayı yapmama listesi
    xr = 600; yr = Hh - 98
    yaz(xr, yr, "AYNI HATAYI YAPMAMA LİSTESİ", "DVB", 10, (0.6, 0.0, 0.0)); yr -= 14
    for k in ("CD1", "CD2", "CD3", "CD4", "CD5", "CD6", "CD7"):
        yr = paragraf(xr, yr, f"{k} {HD_DERS_METIN[k]}", W - xr - 25, n=7.5, ara=9.2) - 3
    yr -= 4
    yaz(xr, yr, "VEKİLE (ana modelin kuralları)", "DVB", 9, (0.15, 0.15, 0.45)); yr -= 12
    for k in ("VD1", "VD2", "VD3"):
        yr = paragraf(xr, yr, f"{k} {HD_DERS_METIN[k]}", W - xr - 25, n=7.5, ara=9.2) - 3
    # göz aşinalığı
    y -= 10
    yaz(30, y, "GÖZ AŞİNALIĞI (bu 40 sayfada)", "DVB", 10, (0.0, 0.35, 0.0)); y -= 14
    git = T[(T.h5 == 1)]; gitmedi = T[(T.h5 == 0)]
    kazan_git = sorted(int(s) for s in T[(T.h5 == 1) & T.cemal_not.str.contains("kazan")].sayfa)
    kazan_gitmedi = sorted(int(s) for s in T[(T.h5 == 0) & T.cemal_not.str.contains("kazan")].sayfa)
    for s in (f"Hedefe gidenler ({len(git)} sayfa): kazan + sağ kenarı dönmüş dip. Kazan çizdiğin ve +%5 gelen sayfalar: {', '.join(map(str, kazan_git))}. "
              "Vekilin 'stop uzak / kapanış tavana ancak değiyor' diye elediği yapıların bir kısmı da gitti (2, 4, 5, 26, 30, 33, 35).",
              f"Gitmeyenler ({len(gitmedi)} sayfa): tepede raf (1, 6: 120 günün tepesinde / şemsiye sonrası) ve en güzel görünen taban "
              f"(25, 28: uzun, düzgün, gövdeli kırılım, parmak izi -> stop). Kazan çizip +%5 görmeyen: {', '.join(map(str, kazan_gitmedi)) or 'yok'} "
              "(14: sağ kenar dönmeden).",
              "Bakış sırası: 1) bağlam: dipte mi tepede mi (120 bar); 2) dip savunulmuş mu, kazanın sağ kenarı yükseliyor mu; 3) fitil ancak bağlamla okunur; "
              "4) güzel şekil tek başına yetmez; 5) kırılımda gün sonu kapanış + ertesi gün kalıcılık."):
        y = paragraf(30, y, "• " + s, 545, n=8, ara=10) - 3
    yaz(30, 22, "Kaynak: hakem_cevap_cemal.json, hakem_anahtar.json, anahtar.json, olay_Y1.csv.gz (15 gün: +%5 / +%10 stop'tan önce; takip stoplu çıkış bilgi), "
        "HAKEM_DERSLER.md. 'gün +k' = girişten sonraki k. geçerli bar (gün +0 = giriş günü).", n=6.5, renk=(0.35, 0.35, 0.35))
    cv.showPage()

    # ---------------- DERS SAYFALARI
    from PIL import Image
    for _, r in T.iterrows():
        g = ek[int(r.sayfa)]
        sonuc = hd_sonuc_metni(r, g["k10"])
        baslik = f"Sayfa {r.sayfa} · {hd_cemal_baslik(r)} · SONUÇ: {sonuc} · PUAN Cemal {_pz(r.puan_c)} / vekil {_pz(r.puan_v)}"
        renk = (0.0, 0.45, 0.0) if r.puan_c == 1 else ((0.7, 0.0, 0.0) if r.puan_c == -1 else (0.3, 0.3, 0.3))
        yy = Hh - 24
        for ln in simpleSplit(baslik, "DVB", 11, W - 50):
            yaz(25, yy, ln, "DVB", 11, renk); yy -= 13
        yaz(25, yy, f"{r.yari} yarı · {r.pazar} · {hd_takip_metni(r)} · eş payı (+%5) %{r.es_h5 * 100:.0f}", n=8, renk=(0.3, 0.3, 0.3))
        top = yy - 6; kutu_h = top - 150; kw = ((W - 60) * 0.56, (W - 60) * 0.44); hmax = 0.0
        for k, (p, x0) in enumerate(((g["sol_png"], 25), (os.path.join(is_klasor, "graf", f"g{r.sayfa:02d}.png"), 35 + kw[0]))):
            iw, ih = Image.open(p).size; kutu_w = kw[k]
            sc = min(kutu_w / iw, kutu_h / ih); w_, h_ = iw * sc, ih * sc; hmax = max(hmax, h_)
            cv.drawImage(p, x0 + (kutu_w - w_) / 2, top - h_, width=w_, height=h_)
        alt = top - hmax
        yaz(25, alt - 9, "Sol: senin işaretlediğin sayfa (aynen)", n=7, renk=(0.4, 0.4, 0.4))
        yaz(35 + kw[0], alt - 9, "Sağ: aynı olay, sonrası açık (sarı = 15 bar penceresi)", n=7, renk=(0.4, 0.4, 0.4))
        y = alt - 26
        y = paragraf(25, y, f"(1) Cemal'in notu: {r.cemal_not}", W - 50, n=9.5, ara=12) - 4
        ned = ", ".join(GE.ge_neden_acilim(k).replace(": UYUYOR (lehte)", " +").replace(": UYMUYOR (aleyhte)", " -") for k in r.nedenler)
        y = paragraf(25, y, f"(2) Vekil: {r.vekil} (puan {_pz(r.puan_v)}) · nedenler: {ned}", W - 50, n=8.5, ara=10.5) - 8
        ders = []
        if r.cd:
            ders.append(f"{r.cd}: {HD_DERS_METIN[r.cd]}")
        if r.vd:
            ders.append(f"{r.vd} (vekile): {HD_DERS_METIN[r.vd]}")
        if not r.cd:
            ders.insert(0, hd_dogru_cumle(r))
        metin = "(3) DERS: " + "  ·  ".join(ders)
        sat = simpleSplit(metin, "DVB", 9.5, W - 66)
        bh = 12.5 * len(sat) + 8
        kr = (0.8, 0.0, 0.0) if r.puan_c == -1 else ((0.0, 0.55, 0.0) if r.puan_c == 1 else (0.55, 0.55, 0.55))
        cv.setStrokeColorRGB(*kr); cv.setLineWidth(1.8); cv.rect(25, y - bh + 9, W - 50, bh, stroke=1, fill=0); cv.setStrokeColorRGB(0, 0, 0)
        cv.setLineWidth(1)
        yb = y
        for ln in sat:
            yaz(33, yb, ln, "DVB", 9.5); yb -= 12.5
        if yb < 8:
            raise HDHata(f"sayfa {r.sayfa}: metin sayfaya sığmadı")
        cv.showPage()

    # ---------------- ÖZET
    yaz(30, Hh - 32, "ÖZET — 40 sayfa", "DVB", 13)
    kol = [("Sayfa", 30), ("Yarı", 70), ("Pazar", 108), ("Cemal (ham)", 150), ("Cemal etkin", 235), ("Vekil", 310), ("Sonuç (15 gün)", 375),
           ("Puan C", 560), ("Puan V", 610), ("Ders", 665)]
    y = Hh - 54
    for k, x in kol:
        yaz(x, y, k, "DVB", 8)
    cv.line(30, y - 3, W - 30, y - 3); y -= 12.5
    for _, r in T.iterrows():
        rc = (0.0, 0.45, 0.0) if r.puan_c == 1 else ((0.7, 0.0, 0.0) if r.puan_c == -1 else (0.3, 0.3, 0.3))
        vals = [str(r.sayfa), r.yari, r.pazar, r.cemal_ham if r.cemal_ham != "-" else "yanıtsız", r.cemal, r.vekil, hd_sonuc_metni(r, r.k10),
                _pz(r.puan_c), _pz(r.puan_v), " ".join(x for x in (r.cd, r.vd) if x) or "—"]
        for (k, x), s in zip(kol, vals):
            yaz(x, y, s, "DV", 7.6, rc if k in ("Cemal etkin", "Puan C") else (0, 0, 0))
        y -= 12.5
    y -= 4
    for p in P:
        if p["bolum"].startswith("Toplam"):
            yaz(30, y, f"{p['kim']}: {p['karar']} karar, +1 {p['arti']}, -1 {p['eksi']}, başarı %{p['basari'] * 100:.0f}, taban %{p['taban'] * 100:.0f}, "
                f"karar dışı {p['disi']}", "DVB", 8.5); y -= 12
    cv.showPage(); cv.save()
    mb = os.path.getsize(tmp) / 2 ** 20
    if mb > HD_AYAR["azami_mb"]:
        os.remove(tmp)
        raise HDHata(f"PDF {mb:.1f} MB > {HD_AYAR['azami_mb']} MB")
    os.replace(tmp, cikti)
    return {"pdf": cikti, "mb": round(mb, 2), "sayfa": 2 + len(T), "puan": P, "is_klasor": is_klasor}


# ================================================================ ÇAKIŞMA KAPISI ve KOMUT
def _cakisma_kontrol_hd(_once=_CK_ONCE_HD):
    """Bellekte (Colab exec) önceden var olan bir ad bu dosyayla ezildiyse durur."""
    g = globals()
    atla = {"_CK_ONCE_HD", "_cakisma_kontrol_hd", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit", "__builtins__",
            "__name__", "__doc__", "__file__", "__loader__", "__spec__", "__package__", "__cached__", "__annotations__"}
    ezilen = [k for k, i in _once.items() if k not in atla and k in g and id(g[k]) != i and not k.startswith("__")]
    if ezilen:
        raise HDHata(f"çakışma kapısı: bellekteki adlar ezildi: {ezilen[:10]}")


_cakisma_kontrol_hd()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="HAKEM DERS PDF'i")
    ap.add_argument("--cemal-pdf", required=True)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--is", dest="is_klasor", default=None)
    a = ap.parse_args()
    try:
        R = hd_pdf(a.cemal_pdf, a.cikti, a.is_klasor)
        print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
    except (HDHata, GE.GEHata) as ex:
        hdlog.error("%s", ex); sys.exit(1)
