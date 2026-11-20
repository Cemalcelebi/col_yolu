# -*- coding: utf-8 -*-
"""ESLER — bir CANLI_TARAMA listesindeki adayların EŞ KÜMESİ (aynı giriş günü, aynı OC momentum x likidite kovası) ve sonuçları.

Tanım CANLI_TARAMA.ct_olc_olaylar / YAPI_HEDEF.yh_olay_olc ile AYNI (aynı veri kırpması, aynı panel, aynı yh_sim, aynı d / stop geometrisi):
  havuz = ok[d] (giriş günü d), eş = havuzda, 15 barı ölçülebilir, olay hissesi hariç, H[d, k] == H[d, j].
Her eş için: giriş açılışı (Op[d]), h5 / h10 / st5 (yh_sim, stop = giriş x (1 - dd), dd = olayın stop uzaklığı), 15 geçerli barda en yüksek
kapanış / giriş - 1, sinyal günü t'de S6 AL (YH.yh_s6_hisse, tam veri, kriz kesiği bellekte açık) ve Ş1 / Ş7 / Ş9 / Ş10 (S6 AL olanlarda;
CANLI_TARAMA.ct_ozellik_hisse ile, sinyal yoksa '-'). Kapı: n_es ve es_h5 yh_olay_olc çıktısıyla birebir; değilse DURUR.

Kullanım: python arastirma_cikti/canli/esler_pdf.py 2026-10-22 [veri_klasoru]
Yazı yeri: arastirma_cikti/canli/ESLER_<etiket>.md ve .pdf. Defter dosyalarına dokunmaz. Kod değişirse Colab'da çalışma zamanını yeniden başlat.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import textwrap
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if KOK not in sys.path:
    sys.path.insert(0, KOK)

import CANLI_TARAMA as CT  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

eslog = logging.getLogger("col.esler")
if not eslog.handlers:
    _h = logging.StreamHandler(sys.stderr); _h.setFormatter(logging.Formatter("%(asctime)s ESLER %(levelname)s %(message)s"))
    eslog.addHandler(_h); eslog.setLevel(logging.INFO); eslog.propagate = False

CIKTI = os.path.join(KOK, "arastirma_cikti", "canli")
ES_KAPI = {"n_es": {"RARE": 103, "ALKT": 71, "FNF": 71, "NOVO-B.CO": 39},
           "es_h5": {"RARE": 0.56, "ALKT": 0.68, "FNF": 0.83, "NOVO-B.CO": 0.74}}   # CANLI_SONUC.md (2 basamak yuvarlak)
PDF_EN_IYI = 10
GRAF_ONCE, GRAF_SONRA = 120, 30


class ESHata(RuntimeError):
    pass


def es_kume(etiket: str, veri: Optional[str] = None) -> Dict[str, Any]:
    """Adaylar -> {aday satırları (yh_olay_olc), eş tablosu, tam veri}. ct_olc ile aynı Ad kurulumu ve pazar gruplaması."""
    J = json.load(open(os.path.join(CIKTI, f"CANLI_TARAMA_{etiket}.json"), encoding="utf-8"))
    A = pd.DataFrame(J["adaylar"]).assign(kapsam="liste"); Hv = pd.DataFrame(J["havuz_tumu"])
    if len(Hv):
        Hv = Hv.assign(kapsam="havuz")
        Hv = Hv[~Hv.set_index(["pazar", "sembol", "tarih"]).index.isin(A.set_index(["pazar", "sembol", "tarih"]).index)]
    Ad = pd.concat([x[["pazar", "sembol", "tarih", "hat", "kapsam"] + [c for c in ("sira", "kapanis") if c in x.columns]] for x in (A, Hv) if len(x)],
                   ignore_index=True)
    E = CT.CT_ESIK; Y = YH.YH_ESIK; R = int(Y["olcu"]["pencere_azami"]); u = int(Y["olcu"]["ufuk"])
    Zs, Es, Vt = [], [], {}
    for p, g in Ad.groupby("pazar"):
        with CT.ct_kriz_ac():
            Vfull = OC.oc_veri(p, klasor=CT.ct_kaynak(p, veri))
            Vt[p] = Vfull["V"]
            bas = pd.to_datetime(g.tarih).min() - pd.Timedelta(days=200)
            Vd = {**Vfull, "V": {s: d[d.index >= bas] for s, d in Vfull["V"].items() if len(d[d.index >= bas]) >= 30}}
            P = OC.oc_panel(Vd); Cl = YH.yh_kapanis(P, Vd)
            sig = g.assign(tarih=pd.to_datetime(g.tarih), yon=1)
            sig["stop0"] = sig.hat.astype(float) * float(E["olcu"]["stop_carp"])
            X, say = OC.oc_olay_hazirla(sig[["sembol", "tarih", "pazar"]], P)
            if not len(X):
                raise ESHata(f"{p}: olay hazırlığında hepsi düştü {say}")
            X = X.merge(sig[["sembol", "tarih", "stop0", "yon", "hat", "kapsam"]], on=["sembol", "tarih"], how="left")
            Z = YH.yh_olay_olc(P, Cl, Vd, X, YH._yh_deneme_no("Y1"), OC.OC_ESIK["pazar"].index(p) + 1)
            Z.insert(0, "pazar", p); Zs.append(Z)
            Op, Hi, Lo, Hc, ok = P["Op"], P["Hi"], P["Lo"], P["H"], P["ok"]
            for r in X.itertuples(index=False):
                d, j = int(r.d), int(r.j); E0 = float(Op[d, j]); st0 = float(r.stop0); dd = 1 - st0 / E0
                havuz = np.flatnonzero(ok[d])
                if not ok[d, j]:
                    havuz = np.r_[havuz, j]
                Ek = Op[d, havuz]; stk = Ek * (1 - dd); stk[havuz == j] = st0
                Cw = YH._yh_pencere(Cl, d, R, havuz)
                Sm = YH.yh_sim(Cw, YH._yh_pencere(Hi, d, R, havuz), YH._yh_pencere(Lo, d, R, havuz), Ek, stk, 1, Y)
                pj = int(np.flatnonzero(havuz == j)[0])
                diger = Sm["olc"].copy(); diger[pj] = False
                es = diger & (Hc[d, havuz] == Hc[d, j])
                for q in np.flatnonzero(es):
                    cv = Cw[:, q]; cv = cv[np.isfinite(cv)][:u]
                    Es.append({"pazar": p, "aday": r.sembol, "sinyal": pd.Timestamp(r.tarih), "giris": P["tarih"][d], "kova": int(Hc[d, j]),
                               "sembol": P["sembol"][havuz[q]], "E0": float(Ek[q]), "stop": float(stk[q]), "h5": float(Sm["h5"][q]),
                               "h10": float(Sm["h10"][q]), "st5": float(Sm["st5"][q]), "k5": int(Sm["k5"][q]), "kst": int(Sm["kst"][q]),
                               "max15": float(np.max(cv) / Ek[q] - 1)})
    Z = pd.concat(Zs, ignore_index=True); Es = pd.DataFrame(Es)
    return {"J": J, "Z": Z, "E": Es, "V": Vt}


def es_kapi(Z: pd.DataFrame, Es: pd.DataFrame) -> List[str]:
    """n_es / es_h5: kendi eş kümem = yh_olay_olc (birebir, göreli 1e-9) = CANLI_SONUC (n birebir, h5 2 basamak). Tutmazsa DURUR."""
    sat = []
    for r in Z.itertuples(index=False):
        g = Es[(Es.pazar == r.pazar) & (Es.aday == r.sembol)]
        n, h = len(g), float(g.h5.mean())
        if n != int(r.n_es) or abs(h - float(r.es_h5)) > 1e-9 * max(1.0, abs(h)):
            raise ESHata(f"{r.sembol}: eş kümesi yh_olay_olc ile tutmuyor (n {n} / {r.n_es}, h5 {h} / {r.es_h5})")
        if r.sembol in ES_KAPI["n_es"]:
            if n != ES_KAPI["n_es"][r.sembol] or round(h, 2) != ES_KAPI["es_h5"][r.sembol]:
                raise ESHata(f"{r.sembol}: CANLI_SONUC ile tutmuyor (n {n} / {ES_KAPI['n_es'][r.sembol]}, h5 {h:.4f} / {ES_KAPI['es_h5'][r.sembol]})")
        sat.append(f"{r.sembol}: n_es {n} = yh_olay_olc {int(r.n_es)} = CANLI_SONUC; es_h5 {h:.6f} = yh_olay_olc {float(r.es_h5):.6f} (CANLI_SONUC "
                   f"{ES_KAPI['es_h5'].get(r.sembol)})")
    return sat


def es_sinyal(Es: pd.DataFrame, Vt: Dict[str, Dict[str, pd.DataFrame]]) -> pd.DataFrame:
    """Her eş için sinyal günü t'de S6 AL (son 5 gün de bilgi) ve S6 AL olanlarda Ş1 / Ş7 / Ş9 / Ş10."""
    Es = Es.copy()
    for c in ("S6", "S6_5g", "S1", "S7", "S9", "S10", "S9h"):
        Es[c] = None
    Es["hat_es"] = np.nan; Es["oz_hata"] = ""
    s6_onb: Dict[Any, pd.DataFrame] = {}
    with CT.ct_kriz_ac():
        for i, r in Es.iterrows():
            df = Vt[r.pazar][r.sembol]; key = (r.pazar, r.sembol)
            if key not in s6_onb:
                try:
                    s6_onb[key] = YH.yh_s6_hisse(df)[0]
                except Exception as ex:  # tek hisse bozuksa öteki eşler sürer
                    eslog.warning("S6 %s atlandı: %s", r.sembol, ex); s6_onb[key] = None
            X1 = s6_onb[key]
            if X1 is None:
                Es.at[i, "oz_hata"] = "S6 çalışmadı"; continue
            t = pd.Timestamp(r.sinyal)
            gun = X1[pd.to_datetime(X1.tarih) == t]
            d_ = YH._yh_hazir(df); k = d_.index.searchsorted(t, side="right")
            son5 = d_.index[max(0, k - 5):k]
            try:                         # Ş9 U dip S6'dan bağımsız: bütün eşlerde BİLGİ (yh_s9_ozellik + yh_s9_sartlar)
                Es.at[i, "S9h"] = bool(YH.yh_s9_sartlar(YH.yh_s9_ozellik(d_, [t], hazir=True))["S9"][0])
            except Exception as ex:  # t geçerli bar değilse '-'
                eslog.warning("Ş9 %s %s: %s", r.sembol, t.date(), ex)
            Es.at[i, "S6"] = bool(len(gun)); Es.at[i, "S6_5g"] = bool(pd.to_datetime(X1.tarih).isin(son5).any())
            if len(gun):
                Es.at[i, "hat_es"] = float(gun.hat.iloc[0])
                try:
                    F = CT.ct_ozellik_hisse(df, [t]); F.insert(0, "pazar", r.pazar)
                    S = YH.yh_s7_sartlar(F)
                    Es.at[i, "S1"] = bool(S["S1"][0]); Es.at[i, "S7"] = bool(S["S7"][0])
                    Es.at[i, "S9"] = bool(YH.yh_s9_sartlar(F)["S9"][0])
                    Es.at[i, "S10"] = bool(float(F["S10"].iloc[0]) == 1.0) if pd.notna(F["S10"].iloc[0]) else False
                except Exception as ex:  # özellik düşerse satır kalır, neden yazılır
                    Es.at[i, "oz_hata"] = str(ex)[:120]
    return Es


def _b(x: Any) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else ("✓" if bool(x) else "·")


def _v(x: float, n: int = 2, isaret: bool = False) -> str:
    return "-" if not np.isfinite(x) else (f"{x:+.{n}f}" if isaret else f"{x:.{n}f}").replace(".", ",")


def _p(x: float) -> str:
    return "-" if not np.isfinite(x) else f"%{x * 100:.0f}".replace(".", ",")


def es_md(etiket: str, J: Dict[str, Any], Z: pd.DataFrame, Es: pd.DataFrame, kapi: List[str]) -> str:
    L = [f"# Ekim adaylarının eşleri — liste {etiket} (aynı giriş günü, aynı momentum x likidite kovası)", "",
         "**" + CT.CT_DURUSTLUK + "**", "",
         "Eş tanımı CANLI_TARAMA / YAPI_HEDEF ölçümüyle AYNI: aynı giriş günü, aynı OC momentum beşliği x likidite üçlüsü kovası, havuzda, 15 barı "
         "ölçülebilir, aday hariç. Cetvel: giriş = sinyalden sonraki ilk açılış; h5 / h10 = 15 geçerli barda kapanışla +%5 / +%10, stop'tan önce; "
         "stop = giriş x (1 - adayın stop uzaklığı); st5 = stop +%5'ten önce. 'en yük. 15g' = 15 geçerli barda en yüksek kapanış / giriş - 1. "
         "S6 = eşin kendisinde de sinyal günü S6 AL; S6 5g = son 5 işlem gününde S6 AL (canlı liste penceresi, bilgi). Ş1 / Ş7 / Ş9 / Ş10 yalnız "
         "S6 AL olan eşte ölçülür (CANLI_TARAMA.ct_ozellik_hisse); sinyal yoksa '-'. Ş9h = Ş9 U dip şartı (S6'dan bağımsız; "
         "YH.yh_s9_ozellik + yh_s9_sartlar) BÜTÜN eşlerde, sinyal günü t'de (bilgi).",
         f"Veri: {', '.join(sorted(set(CT.ct_kaynak(p) for p in Es.pazar.unique())))} (son tarih 19 Kas 2026). Hayatta kalma: evren bugün işlem "
         "gören hisseler (yukarı yanlı). Örneklem küçük (her aday tek gün, tek kova): bulgu denmez, olaylar tek tek okunur.", "",
         "Kapı (eş kümesi = CANLI_SONUC):", ""] + [f"- {k}" for k in kapi] + ["", "## Özet", "",
         "| aday | pazar | sinyal | giriş | aday h5 | eş n | eş +%5 payı | eş +%10 payı | eş stop önce | S6 AL eş n | S6'lı eş +%5 | S6'sız eş +%5 | "
         "S6 5g eş n | S6 5g +%5 | Ş9 (S6'lı) eş | Ş1+Ş7 eş | Ş9h eş n | Ş9h eş +%5 | Ş9h'siz +%5 | Ş9h eşler |", "|" + "---|" * 20]
    for r in Z.itertuples(index=False):
        g = Es[(Es.pazar == r.pazar) & (Es.aday == r.sembol)]
        s6 = g.S6.astype(bool); s5 = g.S6_5g.astype(bool); s9 = g.S9.fillna(False).astype(bool)
        s17 = g.S1.fillna(False).astype(bool) & g.S7.fillna(False).astype(bool); s9h = g.S9h.fillna(False).astype(bool)
        L.append(f"| {r.sembol} | {r.pazar} | {pd.Timestamp(r.tarih).date()} | {pd.Timestamp(r.giris).date()} | {int(r.h5)} | {len(g)} | "
                 f"{_p(g.h5.mean())} | {_p(g.h10.mean())} | {_p(g.st5.mean())} | {int(s6.sum())} | {_p(g.h5[s6].mean()) if s6.any() else '-'} | "
                 f"{_p(g.h5[~s6].mean())} | {int(s5.sum())} | {_p(g.h5[s5].mean()) if s5.any() else '-'} | "
                 f"{', '.join(g.sembol[s9]) or '-'} | {', '.join(g.sembol[s17]) or '-'} | {int(s9h.sum())} | "
                 f"{_p(g.h5[s9h].mean()) if s9h.any() else '-'} | {_p(g.h5[~s9h].mean())} | {', '.join(g.sembol[s9h]) or '-'} |")
    L += ["", "Okuma: payların farkı küçük örneklemdir (S6 AL eş sayısı birkaç); 'desen eşlerde de vardı / yoktu' sözü sayıdan ayrı okunur.", ""]
    for r in Z.itertuples(index=False):
        g = Es[(Es.pazar == r.pazar) & (Es.aday == r.sembol)].sort_values(["h5", "max15", "sembol"], ascending=[False, False, True])
        L += [f"## {r.sembol} ({r.pazar}) — sinyal {pd.Timestamp(r.tarih).date()}, giriş {pd.Timestamp(r.giris).date()}, kova {int(r.hucre)}, "
              f"{len(g)} eş", "",
              f"Aday: giriş açılış {_v(r.E0)}, h5 {int(r.h5)}, h10 {int(r.h10)}, st5 {int(r.st5)}; stop uzaklığı %{_v(r.dd * 100, 1)}.", "",
              "| # | sembol | giriş açılış | h5 | h10 | st5 | +%5 bar | en yük. 15g | S6 | S6 5g | Ş1 | Ş7 | Ş9 | Ş10 | Ş9h |", "|" + "---|" * 15]
        for k, e in enumerate(g.itertuples(index=False), 1):
            L.append(f"| {k} | {e.sembol} | {_v(e.E0)} | {int(e.h5)} | {int(e.h10)} | {int(e.st5)} | {e.k5 + 1 if e.k5 >= 0 else '-'} | "
                     f"%{_v(e.max15 * 100, 1, True)} | {_b(e.S6)} | {_b(e.S6_5g)} | {_b(e.S1)} | {_b(e.S7)} | {_b(e.S9)} | {_b(e.S10)} | {_b(e.S9h)} |")
        L.append("")
    L.append("✓ = var, · = yok, - = ölçülmedi (S6 AL yok). '+%5 bar' = girişten sonra kaçıncı geçerli bar (1 = giriş günü).")
    return "\n".join(L) + "\n"


def es_pdf(etiket: str, Z: pd.DataFrame, Es: pd.DataFrame, Vt: Dict[str, Dict[str, pd.DataFrame]], yol: str) -> int:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    sayfa = 0
    with PdfPages(yol, metadata={"Title": f"ESLER {etiket}", "Creator": "esler_pdf", "Producer": None}) as pp:
        fig = plt.figure(figsize=(11.69, 8.27))
        try:
            fig.text(0.04, 0.94, f"Ekim adaylarının eşleri — liste {etiket}", fontsize=16, weight="bold")
            fig.text(0.04, 0.84, "\n".join(textwrap.wrap(CT.CT_DURUSTLUK, 150)), fontsize=8.5, color="#a50026", va="bottom")
            sat = ["Eş = aynı giriş günü, aynı momentum x likidite kovası (CANLI_TARAMA / YAPI_HEDEF ölçümüyle aynı). Her aday için 15 geçerli barda",
                   "en yüksek kapanışa göre en iyi 10 eş. Grafik: sinyal gününden önce 120 bar + sonra 30 bar (veri 19 Kas 2026'da biter).",
                   "Gri dikey = sinyal günü, siyah kesik = giriş açılışı, kırmızı = stop, yeşil = +%5 / +%10, lacivert = eşin kendi S6 hattı (S6 AL varsa).", ""]
            sat.append(f"{'aday':<10} {'pazar':<5} {'sinyal':<10} {'eş n':>5} {'+%5 payı':>9} {'S6 eş':>6} {'S6 +%5':>7} {'S6siz +%5':>9}")
            for r in Z.itertuples(index=False):
                g = Es[(Es.pazar == r.pazar) & (Es.aday == r.sembol)]; s6 = g.S6.astype(bool)
                sat.append(f"{r.sembol:<10} {r.pazar:<5} {str(pd.Timestamp(r.tarih).date()):<10} {len(g):>5} {_p(g.h5.mean()):>9} {int(s6.sum()):>6} "
                           f"{(_p(g.h5[s6].mean()) if s6.any() else '-'):>7} {_p(g.h5[~s6].mean()):>9}")
            fig.text(0.04, 0.76, "\n".join(sat), fontsize=9, family="DejaVu Sans Mono", va="top")
            pp.savefig(fig); sayfa += 1
        finally:
            plt.close(fig)
        for r in Z.itertuples(index=False):
            g = Es[(Es.pazar == r.pazar) & (Es.aday == r.sembol)].sort_values(["max15", "sembol"], ascending=[False, True]).head(PDF_EN_IYI)
            for k, e in enumerate(g.itertuples(index=False), 1):
                with CT.ct_kriz_ac():
                    d = YH._yh_hazir(Vt[e.pazar][e.sembol])
                t = pd.Timestamp(e.sinyal); i = int(d.index.searchsorted(t, side="right")) - 1
                a0 = max(0, i - GRAF_ONCE + 1); b0 = min(len(d), i + GRAF_SONRA + 1); W = d.iloc[a0:b0]
                x = np.arange(a0, b0) - i
                o, h, l, c, v = (W[q].to_numpy(float) for q in ("Open", "High", "Low", "Close", "Volume"))
                fig = plt.figure(figsize=(11.69, 8.27))
                try:
                    gs = fig.add_gridspec(2, 1, height_ratios=[3.4, 0.9], hspace=0.05)
                    ax = fig.add_subplot(gs[0]); av = fig.add_subplot(gs[1], sharex=ax)
                    renk = np.where(c >= o, "#1a9850", "#d73027")
                    ax.vlines(x, l, h, colors=renk, linewidth=0.8, zorder=3)
                    ax.bar(x, np.maximum(np.abs(c - o), (h - l) * 0.01), bottom=np.minimum(o, c), width=0.7, color=renk, edgecolor=renk, linewidth=0.4, zorder=4)
                    if np.isfinite(e.hat_es):
                        ax.hlines(e.hat_es, x[0], 0.5, colors="#313695", linewidth=1.3, zorder=5, label=f"eşin S6 hattı {e.hat_es:.2f}")
                    ax.hlines(e.E0, 0.5, x[-1] + 0.5, colors="#000000", linestyles="--", linewidth=0.9, zorder=5, label=f"giriş açılışı {e.E0:.2f}")
                    ax.hlines(e.stop, 0.5, x[-1] + 0.5, colors="#a50026", linestyles="-.", linewidth=1.0, zorder=5, label=f"stop {e.stop:.2f}")
                    ax.hlines(e.E0 * 1.05, 0.5, x[-1] + 0.5, colors="#1a9850", linestyles="--", linewidth=1.0, zorder=5, label="+%5")
                    ax.hlines(e.E0 * 1.10, 0.5, x[-1] + 0.5, colors="#006837", linestyles=":", linewidth=1.3, zorder=5, label="+%10")
                    for z in (ax, av):
                        z.axvline(0, color="#777777", linewidth=1.0, zorder=2)
                    ax.legend(loc="upper left", fontsize=7.5, ncol=2, frameon=False); ax.grid(alpha=0.25); ax.set_ylabel("fiyat")
                    av.bar(x, v, width=0.7, color=renk, alpha=0.7); av.set_ylabel("hacim"); av.grid(alpha=0.25)
                    av.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
                    av.set_xlabel(f"bar (0 = sinyal günü {t.date()}; son bar {W.index[-1].date()})")
                    plt.setp(ax.get_xticklabels(), visible=False)
                    ax.set_xlim(x[0] - 1, max(x[-1], GRAF_SONRA) + 1)
                    fig.suptitle(f"{r.sembol} eşi #{k}: {e.pazar} {e.sembol}  ·  sinyal {t.date()}  giriş {pd.Timestamp(e.giris).date()}  ·  "
                                 f"en yük. 15g {e.max15 * 100:+.1f}%  ·  h5 {int(e.h5)} h10 {int(e.h10)} st5 {int(e.st5)}", fontsize=11, weight="bold", y=0.97)
                    fig.text(0.5, 0.925, f"S6 AL (t) {_b(e.S6)}  ·  S6 son 5g {_b(e.S6_5g)}  ·  Ş1 {_b(e.S1)}  Ş7 {_b(e.S7)}  Ş9 {_b(e.S9)}  Ş10 {_b(e.S10)}  Ş9h {_b(e.S9h)}"
                             "   (✓ var, · yok, - ölçülmedi)  ·  izleme / ileri test, öneri değil", ha="center", fontsize=9, color="#a50026")
                    pp.savefig(fig); sayfa += 1
                finally:
                    plt.close(fig)
    return sayfa


def es_calistir(etiket: str, veri: Optional[str] = None) -> Dict[str, Any]:
    K = es_kume(etiket, veri)
    kapi = es_kapi(K["Z"], K["E"])
    for s in kapi:
        eslog.info("KAPI %s", s)
    Es = es_sinyal(K["E"], K["V"])
    md = es_md(etiket, K["J"], K["Z"], Es, kapi)
    ym = os.path.join(CIKTI, f"ESLER_{etiket}.md"); yp = os.path.join(CIKTI, f"ESLER_{etiket}.pdf")
    CT._ct_yaz(ym, md, "eşler md")        # e-posta / anahtar taraması dahil
    n = es_pdf(etiket, K["Z"], Es, K["V"], yp)
    eslog.info("yazıldı %s, %s (%d sayfa)", ym, yp, n)
    return {"Z": K["Z"], "E": Es, "md": ym, "pdf": yp, "sayfa": n}


if __name__ == "__main__":
    try:
        R_ = es_calistir(sys.argv[1] if len(sys.argv) > 1 else "2026-10-22", sys.argv[2] if len(sys.argv) > 2 else None)
    except ESHata as ex_:
        eslog.error("DURDU: %s", ex_); sys.exit(2)
