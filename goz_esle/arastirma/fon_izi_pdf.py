# FON_IZI vaka grafikleri: tasfiye fonu hisselerinin dip -> tepe -> cokus seyri, fazlar ve TL hacim (Cemal hisse adiyla istedi).
# Calistir: FI_VERI_BIST=... python3 goz_esle/arastirma/fon_izi_pdf.py CIKTI.pdf   (repo kokunde)
import sys, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
sys.path.insert(0, ".")
import FON_IZI as F
A = F.FIAyar(); V = F.fi_k1_veri(A.veri["BIST"], "BIST", A)
kos = pd.read_csv(f"{A.cikti}/fon_kosular.csv", parse_dates=["dip", "x2", "tepe"]).sort_values("kat", ascending=False)
tet = pd.read_csv(f"{A.cikti}/fon_iz_tetik.csv", parse_dates=["ilk_iz"]).set_index("sembol")
faz = pd.read_csv(f"{A.cikti}/fon_fazlar.csv")
RENK = {"ONCE": "#bbbbbb", "ERKEN": "#7fc97f", "KOSU": "#fdc086", "COKUS": "#f0027f"}
def ciz(ax, axv, x):
    d = V[x.sembol]; a = max(0, d.index.get_loc(x.dip) - 150); d = d.iloc[a:]
    ax.semilogy(d.index, d.Close, color="#222", lw=0.9)
    sinir = [("ONCE", d.index[0], x.dip), ("ERKEN", x.dip, x.x2), ("KOSU", x.x2, x.tepe), ("COKUS", x.tepe, d.index[-1])]
    for f, b, e in sinir:
        if pd.notna(b) and pd.notna(e): ax.axvspan(b, e, color=RENK[f], alpha=0.25, lw=0)
    t = tet.loc[x.sembol, "ilk_iz"] if x.sembol in tet.index else pd.NaT
    if pd.notna(t): ax.axvline(t, color="#1f4e9c", ls="--", lw=1)
    f = faz[faz.sembol == x.sembol].set_index("faz")
    e = f.loc["ERKEN"] if "ERKEN" in f.index else None
    alt = (f"ERKEN fazı: {int(e.bar)} gün, taban günü {e.taban100:.1f}/100, en derin geri çekilme %{e.maks_dd:.0f}, "
           f"mum boyu evrenin %{e.mum_evren_yzd:.0f}'inde" if e is not None else "")
    ax.set_title(f"{x.sembol}: dipten tepeye {x.kat:.0f} kat · tepeden bugüne %{(d.Close.iloc[-1]/d.Close.loc[x.tepe]-1)*100:.0f}\n{alt}", fontsize=8.5, loc="left")
    tl = (d.Close * d.Volume) / 1e6
    axv.bar(d.index, tl, width=1.0, color="#4a6fa5"); axv.set_ylabel("TL hacim (mn)", fontsize=7)
    for a_ in (ax, axv): a_.tick_params(labelsize=7)
with PdfPages(sys.argv[1]) as pdf:
    fig = plt.figure(figsize=(8.5, 11))
    fm = faz.groupby("faz").median(numeric_only=True).reindex(["ONCE", "ERKEN", "KOSU", "COKUS"])
    txt = ["FONLARIN TOPLADIĞI HİSSELER — YÜKSELİŞİN İZİ", "",
           "23 hisse (tasfiye fonlarının fiili dolaşımda büyük pay sahibi olduğu). Fiyat bölünme/bedelsiz düzeltilmiş.",
           "Renkler: gri = dipten önceki 120 gün · yeşil = ERKEN (dipten ilk 2 kata) · turuncu = KOŞU (2 kattan tepeye)",
           "· pembe = ÇÖKÜŞ. Mavi kesik = izin (aşağıda B) bugünkü bilgiyle ilk tetiklendiği gün.", "",
           "23 hissenin medyanı:",
           f"  ERKEN: {fm.loc['ERKEN','bar']:.0f} gün, günlük +%{fm.loc['ERKEN','gunluk_get']:.2f}, taban günü {fm.loc['ERKEN','taban100']:.1f}/100,",
           f"         en derin geri çekilme %{fm.loc['ERKEN','maks_dd']:.0f}, mum boyu evrenin %{fm.loc['ERKEN','mum_evren_yzd']:.0f}'inde (küçük DEĞİL)",
           f"  KOŞU:  {fm.loc['KOSU','bar']:.0f} gün, tavan {fm.loc['KOSU','tavan100']:.1f}/100, taban {fm.loc['KOSU','taban100']:.1f}/100, TL hacim sırası %{fm.loc['ONCE','tl_evren_yzd']:.0f} → %{fm.loc['KOSU','tl_evren_yzd']:.0f}",
           f"  ÇÖKÜŞ: {fm.loc['COKUS','bar']:.0f} gün, taban {fm.loc['COKUS','taban100']:.0f}/100, tepeden %{fm.loc['COKUS','maks_dd']:.0f}", "",
           "İz B = son 60 günde +%30..100 yükseliş + hiç taban günü yok + geri çekilme ≤ %20",
           "        + mumlar hissenin kendi geçmişinden küçük + istikrarlı yükseliş (verim ≥ 0,25)."]
    fig.text(0.06, 0.95, "\n".join(txt), fontsize=9, va="top", family="DejaVu Sans")
    pdf.savefig(fig); plt.close(fig)
    xs = list(kos.itertuples())
    for i in range(0, len(xs), 2):
        fig = plt.figure(figsize=(8.5, 11)); gs = fig.add_gridspec(6, 1, hspace=0.6)
        for j, x in enumerate(xs[i:i + 2]):
            ax = fig.add_subplot(gs[j * 3:j * 3 + 2]); axv = fig.add_subplot(gs[j * 3 + 2], sharex=ax); ciz(ax, axv, x)
        pdf.savefig(fig, dpi=80); plt.close(fig)
print("ok", len(xs))
