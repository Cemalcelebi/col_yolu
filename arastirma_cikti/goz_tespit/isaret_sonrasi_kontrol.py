# İşaret sonrası KONTROL PDF'i (yeni ölçüm DEĞİL): cemal_isaret_sonrasi.json'daki 140 satırı (GT1, GT3, GT4, GT5, GT9, GT10 işaretli sayfalar)
# ham fiyattan AYNEN yeniden üretir, satır satır eşitliği assert eder, sonra her bölge için gerçek tarih / gerçek fiyatlı grafik sayfası çizer
# (Cemal TradingView ile karşılaştırsın diye). GT11 ve GT2 kullanılmaz / açılmaz. Veri <= 2022-12-31.
# Çalıştır: python arastirma_cikti/goz_tespit/isaret_sonrasi_kontrol.py
# Çıktı: ISARET_SONRASI_KONTROL.pdf, isaret_sonrasi_kontrol.json (aynı klasör). Kod değişirse Colab'da çalışma zamanını yeniden başlat.
from __future__ import annotations

import json
import logging
import os
import sys
import time
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if KOK not in sys.path:
    sys.path.insert(0, KOK)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("isaret_kontrol")

G = os.path.join(KOK, "arastirma_cikti", "goz_tespit") + os.sep
SETLER = (("GT1", "GT_onay_anahtar.json", "cemal_gt_onay.json"), ("GT3", "GT3_onay_anahtar.json", "cemal_gt3_onay.json"),
          ("GT4", "GT4_onay_anahtar.json", "cemal_gt4_onay.json"), ("GT5", "GT5_onay_anahtar.json", "cemal_gt5_onay.json"),
          ("GT9", "GT9_onay_anahtar.json", "cemal_gt9_onay.json"), ("GT10", "GT10_onay_anahtar.json", "cemal_gt10_onay.json"))
YASAK = ("GT11_onay_anahtar.json", "gt11_secim.json", "GT2_onay_anahtar.json")
KESIK = pd.Timestamp("2022-12-31")
CIKTI = {"pdf": G + "ISARET_SONRASI_KONTROL.pdf", "json": G + "isaret_sonrasi_kontrol.json", "eski": G + "cemal_isaret_sonrasi.json"}
BOY = (597.6 / 72.0, 1044.0 / 72.0)          # kör set sayfalarıyla aynı (pt -> inç)
UZAK, YAKIN, UFUK = 120, 10, 15
SIRA_ISARET = ("EVET", "ERKEN", "HAYIR", "KISMEN")
ISARET_YAZI = {"EVET": "✓ çöl", "KISMEN": "K kısmen", "ERKEN": "E erken", "HAYIR": "× değil"}
ISARET_KISA = {"EVET": "✓", "KISMEN": "K", "ERKEN": "E", "HAYIR": "×"}
BEKLENEN = {"EVET": (49, 24, 22), "ERKEN": (30, 8, 20), "HAYIR": (20, 10, 8), "KISMEN": (15, None, None), "RASTGELE": (26, None, None)}


class KontrolHata(RuntimeError):
    """Durdurucu hata: eşitlik / sayım / kesik / yasak dosya."""


# ---------------------------------------------------------------- biçim
def tr_sayi(x: float, ond: int = 2) -> str:
    s = f"{abs(x):,.{ond}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if x < 0 else "") + s


def tr_fiyat(x: float) -> str:
    return tr_sayi(x, 2 if x >= 10 else (3 if x >= 1 else 4))


def tr_yuzde(x: float, ond: int = 1) -> str:
    v = round(x * 100, ond)
    return ("+" if v > 0 else ("−" if v < 0 else "")) + "%" + tr_sayi(abs(v), ond)


def tr_tarih(t: pd.Timestamp, kisa: bool = False) -> str:
    return t.strftime("%d.%m.%y" if kisa else "%d.%m.%Y")


# ---------------------------------------------------------------- 1) yeniden üretim (iş tanımındaki kod AYNEN) + ayrıntı
def veri_yukle() -> Dict[str, Dict[str, Any]]:
    import MUM_IZI as MI
    import GOZ_TESPIT as GT
    out = {}
    for p in ("ABD", "BIST"):
        Vd = MI.mi_veri(p, GT.GT_YOL["acik"])
        en_gec = max(d.index.max() for d in Vd["V"].values())
        if en_gec > KESIK:
            raise KontrolHata(f"{p}: kesik aşımı {en_gec.date()}")
        out[p] = {"V": Vd["V"], "gecersiz": Vd.get("gecersiz", {})}
        log.info("%s: %d hisse, en geç %s", p, len(Vd["V"]), en_gec.date())
    return out


def satirlar_uret(VV: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    V = {p: VV[p]["V"] for p in VV}
    sat: List[Dict[str, Any]] = []
    for ad, an, isr in SETLER:
        if an in YASAK or isr in YASAK:
            raise KontrolHata(f"yasak dosya: {an} / {isr}")
        S4 = json.load(open(G + isr, encoding="utf-8"))["sinif4"]
        for r in json.load(open(G + an, encoding="utf-8"))["sayfalar"]:
            if r.get("kaynak") == "tam":
                continue
            if str(r["sayfa"]) not in S4:
                continue
            d = V[r["pazar"]][r["sembol"]]
            O, C, H, L = (d[c].to_numpy(float) for c in ("Open", "Close", "High", "Low"))
            t = int(r["t"])
            if t + 15 >= len(C) or d.index[t + 15] > pd.Timestamp("2022-12-31"):
                continue
            m = (d.index >= "2016-01-01") & (d.index <= "2022-12-31"); ii = np.where(m)[0]; ii = ii[ii + 15 < len(C)]
            t1 = float(np.mean(C[ii + 15] / O[ii + 1] - 1)); e = O[t + 1]
            up = np.where(H[t + 1:t + 16] >= 1.05 * e)[0]; dn = np.where(L[t + 1:t + 16] <= 0.95 * e)[0]
            iu = up[0] if len(up) else 99; idn = dn[0] if len(dn) else 99
            R15 = C[t + 15] / e - 1
            # --- ayrıntı (kontrol sayfası için; hesap yukarıdakiyle aynı değişkenlerden)
            if iu < idn:
                once, j = "YUKARI", int(iu)
            elif idn < iu:
                once, j = "ASAGI", int(idn)
            elif iu == idn and iu != 99:
                once, j = "AYNI_MUM", int(iu)
            else:
                once, j = "HICBIRI", None
            s = int(r["s"])
            sat.append({"set": ad, "sayfa": int(r["sayfa"]), "kol": r["kol"], "pazar": r["pazar"], "sembol": r["sembol"], "cemal": S4[str(r["sayfa"])],
                        "s": s, "t": t, "L": int(r["L"]), "bolge_bas": str(d.index[s].date()), "bolge_son": str(d.index[t].date()),
                        "bolge_mum": t - s + 1, "giris_tarih": str(d.index[t + 1].date()), "giris_fiyat": float(e),
                        "ust5": float(1.05 * e), "alt5": float(0.95 * e), "once": once,
                        "once_tarih": str(d.index[t + 1 + j].date()) if j is not None else None, "once_mum_no": (j + 1) if j is not None else None,
                        "mum15_tarih": str(d.index[t + 15].date()), "mum15_kapanis": float(C[t + 15]),
                        "R15": float(R15), "T1": t1, "yukari_once": float(iu < idn), "asagi_once": float(idn < iu), "TF15": float(R15 - t1)})
    return sat


def esitlik_denetle(sat: List[Dict[str, Any]]) -> Dict[str, Any]:
    eski = json.load(open(CIKTI["eski"], encoding="utf-8"))
    if len(eski) != len(sat):
        raise KontrolHata(f"satır sayısı farklı: eski {len(eski)}, yeni {len(sat)}")
    for k in ("set", "kol", "cemal"):
        if [a[k] for a in eski] != [b[k] for b in sat]:
            raise KontrolHata(f"'{k}' sırası farklı")
    for k in ("R15", "T1", "yukari_once", "asagi_once", "TF15"):
        a = np.array([x[k] for x in eski], float); b = np.array([x[k] for x in sat], float)
        if not np.allclose(a, b, rtol=1e-7, atol=1e-9):
            raise KontrolHata(f"'{k}' eşit değil (en büyük fark {np.nanmax(np.abs(a - b))})")
    log.info("eşitlik: %d satır, R15 / T1 / yukari_once / asagi_once / TF15 allclose TUTTU", len(sat))
    return {"satir": len(sat), "alanlar": ["set", "kol", "cemal", "R15", "T1", "yukari_once", "asagi_once", "TF15"], "tuttu": True}


def grup(r: Dict[str, Any]) -> str:
    return "RASTGELE" if r["kol"] == "RASTGELE" else r["cemal"]


def ozet_yap(sat: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    oz = {}
    for g in SIRA_ISARET + ("RASTGELE",):
        x = [r for r in sat if grup(r) == g]
        n = len(x); u = sum(r["once"] == "YUKARI" for r in x); a = sum(r["once"] == "ASAGI" for r in x)
        oz[g] = {"n": n, "yukari": u, "asagi": a, "ayni_mum": sum(r["once"] == "AYNI_MUM" for r in x), "hicbiri": sum(r["once"] == "HICBIRI" for r in x),
                 "TF15_ort": float(np.mean([r["TF15"] for r in x])) if n else float("nan"),
                 "R15_ort": float(np.mean([r["R15"] for r in x])) if n else float("nan")}
    for g, (n, u, a) in BEKLENEN.items():
        if oz[g]["n"] != n or (u is not None and oz[g]["yukari"] != u) or (a is not None and oz[g]["asagi"] != a):
            raise KontrolHata(f"özet tutmadı: {g} {oz[g]} beklenen n={n} yukarı={u} aşağı={a}")
    log.info("özet sayıları TUTTU: %s", {g: (v["n"], v["yukari"], v["asagi"]) for g, v in oz.items()})
    return oz


def sirala(sat: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    sno = {ad: i for i, (ad, _, _) in enumerate(SETLER)}
    gs = {g: i for i, g in enumerate(SIRA_ISARET + ("RASTGELE",))}
    x = sorted(sat, key=lambda r: (gs[grup(r)], sno[r["set"]], r["sayfa"]))
    for i, r in enumerate(x, 1):
        r["sira"] = i
    return x


def tuhaflik(d: pd.DataFrame, gec: pd.DatetimeIndex, a: int, b: int, sonra: Tuple[int, int] = None) -> List[str]:
    """Pencere [a, b] içinde: atılmış (geçersiz) gün, takvim boşluğu, büyük sıçrama, H == L, sıfır hacim."""
    w = d.iloc[a:b + 1]; out = []
    if gec is not None and len(gec):
        k = int(((gec >= w.index[0]) & (gec <= w.index[-1])).sum())
        if k:
            out.append(f"grafik aralığında veride atılmış {k} gün (hacim 0 / H=L / bozuk)")
        if sonra is not None:
            k2 = int(((gec > d.index[sonra[0]]) & (gec <= d.index[sonra[1]])).sum())
            if k2:
                out.append(f"giriş ile 15. mum arasında atılmış gün: {k2} (TradingView'da 15. mum daha erken bir güne düşer)")
    gap = np.diff(w.index.values).astype("timedelta64[D]").astype(int)
    if len(gap) and gap.max() > 7:
        i = int(np.argmax(gap)); out.append(f"{gap.max()} günlük boşluk ({tr_tarih(w.index[i], True)}–{tr_tarih(w.index[i + 1], True)})")
    r = (w.Close / w.Close.shift() - 1).abs()
    if (r > 0.5).any():
        out.append(f"{int((r > 0.5).sum())} günde > %50 kapanış sıçraması")
    if ((w.High - w.Low) <= 0).any():
        out.append("H = L mum var")
    if (w.Volume <= 0).any():
        out.append("sıfır hacimli mum var")
    return out


# ---------------------------------------------------------------- 2) çizim
def mumlar(ax, d: pd.DataFrame, a: int, b: int) -> np.ndarray:
    w = d.iloc[a:b + 1]; x = np.arange(a, b + 1)
    O, H, L, C = (w[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    yuk = C >= O; renk = np.where(yuk, "#1a9850", "#d73027")
    ax.vlines(x, L, H, color=renk, linewidth=0.8, zorder=2)
    gov = np.maximum(np.abs(C - O), (H.max() - L.min()) * 0.0015)
    ax.bar(x, gov, bottom=np.minimum(O, C), width=0.7, color=renk, edgecolor=renk, linewidth=0.3, zorder=3)
    return x


def tarih_ekseni(ax, d: pd.DataFrame, a: int, b: int, adim: int, kisa: bool) -> None:
    xs = list(range(a, b + 1, adim))
    ax.set_xticks(xs); ax.set_xticklabels([tr_tarih(d.index[i], kisa) for i in xs], rotation=55, ha="right", fontsize=9)
    ax.set_xlim(a - 1, b + 1)


def sayfa_ciz(fig, r: Dict[str, Any], d: pd.DataFrame, notlar: List[str]) -> None:
    s, t, e = r["s"], r["t"], r["giris_fiyat"]; son = t + UFUK
    rast = r["kol"] == "RASTGELE"
    bas = f"{r['sira']}.  {r['set']} s. {r['sayfa']}   {r['sembol']}  ({r['pazar']})"
    fig.text(0.05, 0.975, bas, fontsize=17, weight="bold", va="top")
    alt = f"işaretin: {ISARET_YAZI[r['cemal']]}" + ("     gelişigüzel seçilmiş bölge" if rast else f"     kol: {r['kol']}")
    fig.text(0.05, 0.948, alt, fontsize=13, va="top", color="#7b3294" if rast else "black")
    # ÜST (uzak)
    a = max(0, s - UZAK)
    ax = fig.add_axes([0.13, 0.645, 0.83, 0.265])
    ax.axvspan(t + 0.5, son + 0.5, color="#bbbbbb", alpha=0.35, zorder=0)
    mumlar(ax, d, a, son)
    w = d.iloc[a:son + 1]
    lo, hi = float(w.Low.min()), float(w.High.max())
    if hi / lo > 6:
        from matplotlib.ticker import FuncFormatter, LogLocator
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1, 2, 5)))
        ax.yaxis.set_minor_locator(LogLocator(base=10, subs=()))
    from matplotlib.ticker import FuncFormatter
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: tr_fiyat(v) if v > 0 else tr_sayi(v)))
    yl = ax.get_ylim()
    from matplotlib.patches import Rectangle
    bl, bh = float(d.Low.iloc[s:t + 1].min()), float(d.High.iloc[s:t + 1].max())
    ax.add_patch(Rectangle((s - 0.5, bl), t - s + 1, bh - bl, fill=False, edgecolor="#f28e2b", linewidth=2.0, zorder=4))
    ax.axvline(t + 1, color="#2b83ba", linewidth=1.0, linestyle="--", zorder=1)
    ax.set_ylim(yl)
    tarih_ekseni(ax, d, a, son, max(1, (son - a) // 11), True)
    ax.tick_params(axis="y", labelsize=9); ax.grid(alpha=0.25)
    ax.set_title("Uzak: önceki 120 mum + bölge (turuncu) + sonraki 15 mum (gri zemin); kesik mavi = giriş mumu", fontsize=10, loc="left")
    # ALT (yakın)
    a2 = max(0, s - YAKIN)
    ax2 = fig.add_axes([0.13, 0.255, 0.83, 0.305])
    ax2.axvspan(t + 0.5, son + 0.5, color="#bbbbbb", alpha=0.30, zorder=0)
    mumlar(ax2, d, a2, son)
    ax2.add_patch(Rectangle((s - 0.5, bl), t - s + 1, bh - bl, fill=False, edgecolor="#f28e2b", linewidth=2.0, zorder=4))
    ax2.hlines(r["ust5"], t + 0.6, son + 0.4, color="#1a9850", linewidth=1.6, zorder=5)
    ax2.hlines(r["alt5"], t + 0.6, son + 0.4, color="#d73027", linewidth=1.6, zorder=5)
    ax2.hlines(e, t + 0.6, son + 0.4, color="#2b83ba", linewidth=0.9, linestyle=":", zorder=5)
    ax2.text(son + 0.6, r["ust5"], f"+%5\n{tr_fiyat(r['ust5'])}", color="#1a9850", fontsize=8.5, va="bottom", ha="left")
    ax2.text(son + 0.6, r["alt5"], f"−%5\n{tr_fiyat(r['alt5'])}", color="#d73027", fontsize=8.5, va="top", ha="left")
    ax2.plot([t + 1], [e], marker=">", color="#2b83ba", markersize=11, zorder=7)
    ax2.annotate("giriş", (t + 1, e), xytext=(-34, 0), textcoords="offset points", fontsize=9, color="#2b83ba", va="center")
    if r["once"] in ("YUKARI", "AYNI_MUM"):
        xj = t + r["once_mum_no"]; ax2.plot([xj], [r["ust5"]], marker="*", color="#006d2c", markersize=17, zorder=8, markeredgecolor="black")
    if r["once"] in ("ASAGI", "AYNI_MUM"):
        xj = t + r["once_mum_no"]; ax2.plot([xj], [r["alt5"]], marker="*", color="#a50f15", markersize=17, zorder=8, markeredgecolor="black")
    ax2.plot([son], [r["mum15_kapanis"]], marker="D", color="black", markersize=8, zorder=8, markerfacecolor="yellow")
    ax2.annotate("15. mum kapanış", (son, r["mum15_kapanis"]), xytext=(-8, -16), textcoords="offset points", fontsize=8.5, ha="right")
    w2 = d.iloc[a2:son + 1]
    lo2 = min(float(w2.Low.min()), r["alt5"]); hi2 = max(float(w2.High.max()), r["ust5"]); pad = (hi2 - lo2) * 0.05
    ax2.set_ylim(lo2 - 1.8 * pad, hi2 + 1.8 * pad)
    tarih_ekseni(ax2, d, a2, son, max(1, int(np.ceil((son - a2) / 13))), False)
    ax2.set_xlim(a2 - 1, son + 3.5)
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: tr_fiyat(v)))
    ax2.tick_params(axis="y", labelsize=9); ax2.grid(alpha=0.25)
    ax2.set_title("Yakın: önceki 10 mum + bölge + sonraki 15 mum; ★ = ilk değen çizgi; sarı ◆ = 15. mum kapanışı", fontsize=10, loc="left")
    # yazı
    if r["once"] == "HICBIRI":
        once = "15 mumda ikisine de değmedi"
    else:
        ne = {"YUKARI": "+%5", "ASAGI": "−%5", "AYNI_MUM": "aynı mumda ikisi de"}[r["once"]]
        once = f"{ne} ({tr_tarih(pd.Timestamp(r['once_tarih']))}, {r['once_mum_no']}. mum)"
        if r["once"] == "AYNI_MUM":
            once += "; sayımda ne yukarı ne aşağı"
    fark = r["TF15"] * 100
    yazi = (f"Bölge: {tr_tarih(pd.Timestamp(r['bolge_bas']))} – {tr_tarih(pd.Timestamp(r['bolge_son']))} ({r['bolge_mum']} mum).\n"
            f"Giriş: {tr_tarih(pd.Timestamp(r['giris_tarih']))} açılış {tr_fiyat(e)}.   +%5 = {tr_fiyat(r['ust5'])};  −%5 = {tr_fiyat(r['alt5'])}.\n"
            f"Önce: {once}.\n"
            f"15. mum {tr_tarih(pd.Timestamp(r['mum15_tarih']))} kapanış {tr_fiyat(r['mum15_kapanis'])}: getiri {tr_yuzde(r['R15'])}.\n"
            f"Aynı hissenin sıradan günü: {tr_yuzde(r['T1'])}.   Fark: {('+' if fark > 0 else ('−' if fark < 0 else ''))}{tr_sayi(abs(fark), 1)} puan.")
    fig.text(0.05, 0.205, yazi, fontsize=12, va="top", linespacing=1.55,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#f7f7f7", edgecolor="#999999"))
    if notlar:
        import textwrap
        fig.text(0.05, 0.06, textwrap.fill("Veri notu: " + "; ".join(notlar) + ".", 95), fontsize=10, va="top", color="#b35806", linespacing=1.35)


def kapak(fig, oz: Dict[str, Dict[str, Any]], n: int) -> None:
    fig.text(0.06, 0.965, "İŞARET SONRASI — KONTROL DOSYASI", fontsize=18, weight="bold", va="top")
    metin = (
        f"Bu dosya ne: kör setlerde (GT1, GT3, GT4, GT5, GT9, GT10) işaretlediğin {n} bölgenin\n"
        "sonrasına dair sayıların grafikli dökümü. Her bölge bir sayfa: hisse adı, gerçek\n"
        "tarihler, verideki fiyatlar. Amaç: TradingView'da aynı tarihlere bakıp kodun\n"
        "verisini ve hesabını kendin denetlemen.\n\n"
        "Hesap (her sayfada aynı):\n"
        "• Bölgeyi bulan kod yalnız bölgenin son mumuna kadar görür.\n"
        "• Giriş = bölgeden sonraki ilk mumun AÇILIŞI. Sonraki 15 mumda (giriş mumu 1.)\n"
        "   önce +%5'e mi (yüksek fiyat) −%5'e mi (düşük fiyat) değdi; 15. mum kapanışı.\n"
        "• 'Sıradan gün' = aynı hissenin 2016-22 bütün günlerinde aynı hesabın ortalaması.\n"
        "   Fark = 15. mum getirisi − sıradan gün.\n\n"
        "Nasıl okunur: sayfa 2-6 liste; sonra grafikler. Sıra: ✓ dediklerin, erken, değil,\n"
        "kısmen (kodun seçtiği sayfalar), en sonda gelişigüzel seçilmiş bölgeler.")
    fig.text(0.06, 0.925, metin, fontsize=11.5, va="top", linespacing=1.5)
    # tablo
    y0 = 0.55; fig.text(0.06, y0 + 0.03, "Özet (kodun seçtiği sayfalar, işaretine göre)", fontsize=13, weight="bold")
    bas = ["işaretin", "sayfa", "önce +%5", "önce −%5", "ort. fark"]; xs = [0.06, 0.30, 0.43, 0.63, 0.83]
    for x, b in zip(xs, bas):
        fig.text(x, y0, b, fontsize=11.5, weight="bold")
    ad = {"EVET": "✓ çöl", "ERKEN": "E erken", "HAYIR": "× değil", "KISMEN": "K kısmen", "RASTGELE": "gelişigüzel (hepsi)"}
    for i, g in enumerate(SIRA_ISARET + ("RASTGELE",)):
        v = oz[g]; y = y0 - 0.03 * (i + 1) - (0.012 if g == "RASTGELE" else 0)
        hc = [ad[g], str(v["n"]), f"{v['yukari']}  ({tr_sayi(100 * v['yukari'] / v['n'], 0)}%)", f"{v['asagi']}  ({tr_sayi(100 * v['asagi'] / v['n'], 0)}%)",
              f"{('+' if v['TF15_ort'] > 0 else '−')}{tr_sayi(abs(v['TF15_ort']) * 100, 1)} puan"]
        for x, h in zip(xs, hc):
            fig.text(x, y, h, fontsize=11.5)
    fig.text(0.06, y0 - 0.205, "Kalan sayfalarda ya aynı mumda ikisine birden ya da hiçbirine değmedi (o sayfalarda yazılı).", fontsize=10)
    not_ = (
        "FİYAT NOTU (önemli):\n"
        "• ABD fiyatları bölünme VE temettü düzeltmeli (Yahoo 'auto_adjust'; örnek: XOM 02.01.2019\n"
        "   kapanış veride 49,04, ham fiyat ~69,7). TradingView varsayılan olarak temettü düzeltmesi\n"
        "   yapmaz: seviye farklı görünür; oranlar (+%5 / −%5) çok yakın kalır.\n"
        "• BIST fiyatları Yahoo'nun ham serisi (temettü düzeltmesi YOK); bölünme / bedelsiz için Yahoo'nun\n"
        "   kendi düzeltmesi + kodun sıçrama düzeltmesi (günlük sınırı aşan sıçrama bölünme sayılır).\n"
        "   Bu yüzden eski tarihlerde seviye TradingView'dan farklı olabilir.\n"
        "• Veriden hacmi 0 ya da yüksek = düşük olan günler ATILDI; o günler TradingView'da görünür,\n"
        "   burada yoktur (15 mum takvimde biraz uzayabilir). Varsa sayfanın altında yazılı.\n"
        "• Açılış o günün yüksek-düşük aralığı dışındaysa aralığa kırpıldı.\n"
        "Tarih ve mum şekli aynı olmalı. Fark görürsen grubu ve sayfa numarasını yaz\n"
        "(ör. 'GT10 s. 3, 12. sıra').")
    fig.text(0.06, 0.29, not_, fontsize=10.5, va="top", linespacing=1.45,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff7e6", edgecolor="#d98c00"))


def liste_sayfa(fig, x: List[Dict[str, Any]], no: int, top: int) -> None:
    fig.text(0.04, 0.975, f"LİSTE ({no}/{top})   — sıra grafik sayfalarıyla aynı", fontsize=14, weight="bold", va="top")
    fig.text(0.04, 0.952, "işaret: ✓ çöl, K kısmen, E erken, × değil; G = gelişigüzel seçilmiş bölge.  Tarihler GG.AA.YY.", fontsize=9.5, va="top")
    xs = [0.04, 0.10, 0.31, 0.62, 0.80]
    bas = ["no", "set / hisse", "bölge  /  giriş (açılış)", "önce ne / tarih", "15. mum"]
    y = 0.925
    for xx, b in zip(xs, bas):
        fig.text(xx, y, b, fontsize=10.5, weight="bold", va="top")
    for i, r in enumerate(x):
        y = 0.90 - i * 0.0293
        if i % 2 == 0:
            fig.patches.append(__import__("matplotlib").patches.Rectangle((0.03, y - 0.027), 0.94, 0.0293, transform=fig.transFigure,
                                                                           facecolor="#f0f0f0", edgecolor="none", zorder=0))
        g = "G " if r["kol"] == "RASTGELE" else ""
        once = {"YUKARI": "+%5", "ASAGI": "−%5", "AYNI_MUM": "ikisi aynı mum", "HICBIRI": "hiçbiri"}[r["once"]]
        ot = f"{tr_tarih(pd.Timestamp(r['once_tarih']), True)} ({r['once_mum_no']}.)" if r["once_tarih"] else "—"
        c1 = [str(r["sira"]), f"{r['set']} s.{r['sayfa']}  {g}{ISARET_KISA[r['cemal']]}",
              f"{tr_tarih(pd.Timestamp(r['bolge_bas']), True)} – {tr_tarih(pd.Timestamp(r['bolge_son']), True)}", once, tr_yuzde(r["R15"])]
        c2 = ["", f"{r['sembol']} ({r['pazar']})", f"{tr_tarih(pd.Timestamp(r['giris_tarih']), True)}  {tr_fiyat(r['giris_fiyat'])}", ot, ""]
        for xx, a, b in zip(xs, c1, c2):
            fig.text(xx, y, a, fontsize=10, va="top", weight="bold" if xx == xs[0] else "normal")
            if b:
                fig.text(xx, y - 0.0128, b, fontsize=9.3, va="top", color="#333333")


def pdf_yaz(sat: List[Dict[str, Any]], oz: Dict[str, Dict[str, Any]], VV: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    plt.rcParams["font.family"] = "DejaVu Sans"
    TUH: Dict[str, List[str]] = {}
    n_liste = int(np.ceil(len(sat) / 30))
    gecici = CIKTI["pdf"] + ".tmp"
    with PdfPages(gecici) as pp:
        f = plt.figure(figsize=BOY); kapak(f, oz, len(sat)); pp.savefig(f); plt.close(f)
        for k in range(n_liste):
            f = plt.figure(figsize=BOY); liste_sayfa(f, sat[30 * k:30 * (k + 1)], k + 1, n_liste); pp.savefig(f); plt.close(f)
        for r in sat:
            d = VV[r["pazar"]]["V"][r["sembol"]]
            gec = VV[r["pazar"]]["gecersiz"].get(r["sembol"])
            nt = tuhaflik(d, gec, max(0, r["s"] - UZAK), r["t"] + UFUK, (r["t"], r["t"] + UFUK))
            if nt:
                TUH[f"{r['sira']}. {r['set']} s.{r['sayfa']} {r['sembol']}"] = nt
            r["veri_notu"] = nt
            f = plt.figure(figsize=BOY)
            try:
                sayfa_ciz(f, r, d, nt)
                pp.savefig(f)
            except Exception:
                log.exception("sayfa çizilemedi: %s", r["sira"]); raise
            finally:
                plt.close(f)
    os.replace(gecici, CIKTI["pdf"])
    return {"sayfa": 1 + n_liste + len(sat), "boyut_mb": os.path.getsize(CIKTI["pdf"]) / 1e6, "tuhaflik": TUH}


def ana() -> Dict[str, Any]:
    t0 = time.time()
    VV = veri_yukle()
    sat = satirlar_uret(VV)
    esit = esitlik_denetle(sat)                      # tutmazsa KontrolHata: PDF yazılmaz
    oz = ozet_yap(sat)                               # tutmazsa KontrolHata
    sat = sirala(sat)
    P = pdf_yaz(sat, oz, VV)
    alan = ["sira", "set", "sayfa", "kol", "pazar", "sembol", "cemal", "bolge_bas", "bolge_son", "bolge_mum", "L", "giris_tarih", "giris_fiyat",
            "ust5", "alt5", "once", "once_tarih", "once_mum_no", "mum15_tarih", "mum15_kapanis", "R15", "T1", "TF15", "veri_notu"]
    J = {"aciklama": "İşaret sonrası kontrol: cemal_isaret_sonrasi.json'un satır satır yeniden üretimi + ayrıntı (yeni ölçüm değil). once: YUKARI / ASAGI / "
                     "AYNI_MUM / HICBIRI; once_mum_no: giriş mumu = 1. Fiyatlar verideki (ABD bölünme + temettü düzeltmeli; BIST ham + bölünme düzeltmesi).",
         "esitlik": esit, "ozet": oz, "pdf": {k: v for k, v in P.items() if k != "tuhaflik"}, "satirlar": [{k: r[k] for k in alan} for r in sat]}
    with open(CIKTI["json"], "w", encoding="utf-8") as fh:
        json.dump(J, fh, ensure_ascii=False, indent=1)
    log.info("bitti: %d sayfa, %.2f MB, %.0f sn; veri notu olan sayfa %d", P["sayfa"], P["boyut_mb"], time.time() - t0, len(P["tuhaflik"]))
    for k, v in P["tuhaflik"].items():
        log.info("  veri notu %s: %s", k, "; ".join(v))
    return J


if __name__ == "__main__":
    try:
        ana()
    except KontrolHata as ex:
        log.error("DURDU: %s", ex); sys.exit(2)
    except Exception:
        log.exception("beklenmeyen hata"); sys.exit(1)
