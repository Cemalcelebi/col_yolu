"""Veri sinamasi IS 1: goz PDF'i (Cemal TradingView ile karsilastirir). Girdi: secim.json (veri_sinama_sec.py) ve /tmp/kasa/acik/V_*.pkl.
Calistirma: python veri_sinama_goz.py   -> VERI_SINAMA_GOZ.pdf, goz_pencereler.json"""
import json, matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from veri_sinama_sec import yukle, W
plt.rcParams.update({"font.family": "DejaVu Sans"})
BORSA = {".L": ("LSE", "Londra, fiyat pens (GBX)"), ".ST": ("OMXSTO", "Stokholm"), ".PA": ("EURONEXT", "Paris"), ".AS": ("EURONEXT", "Amsterdam"),
         ".DE": ("XETR", "Frankfurt"), ".SW": ("SIX", "Zurih"), ".MI": ("MIL", "Milano"), ".MC": ("BME", "Madrid"), ".CO": ("OMXCOP", "Kopenhag"),
         ".HE": ("OMXHEX", "Helsinki"), ".OL": ("OSL", "Oslo"), ".BR": ("EURONEXT", "Bruksel"), ".LS": ("EURONEXT", "Lizbon"), ".VI": ("VIE", "Viyana")}
def tv_kod(p, kod):
    if p == "BIST": return f"BIST:{kod}", f"{kod}.IS", "Borsa Istanbul, TL"
    if p == "ABD": return kod, kod, "ABD borsasi, USD"
    suf = "." + kod.split(".")[-1]; b, ad = BORSA.get(suf, ("?", "?"))
    return f"{b}:{kod[:-len(suf)].replace('-', '_')}", kod, ad
def tr(ts): return ts.strftime("%d.%m.%Y")
def sayi(x, p): return f"{x:,.2f}".replace(",", " ") if p != "AVR" or x > 50 else f"{x:.3f}"
def isaret_gunleri(pen, r):
    """6 gun: en yuksek, en dusuk, en buyuk artis, en buyuk dusus, ilk, son (tekrar eden -> siradaki aday)."""
    n = len(pen); secili = []; ad = []
    def al(sira, etiket):
        for i in sira:
            if i not in secili: secili.append(int(i)); ad.append(etiket); return
    rr = r.reindex(pen.index).fillna(0).values
    al(np.argsort(-pen.High.values), "pencere en yuksek"); al(np.argsort(pen.Low.values), "pencere en dusuk")
    al(np.argsort(-rr), "en buyuk artis"); al(np.argsort(rr), "en buyuk dusus"); al([0, 1, 2], "ilk gun"); al([n - 1, n - 2, n - 3], "son gun")
    return secili, ad
ETK = {"pencere en yuksek": "Pencere en yüksek", "pencere en dusuk": "Pencere en düşük", "en buyuk artis": "En büyük artış günü",
       "en buyuk dusus": "En büyük düşüş günü", "ilk gun": "İlk gün", "son gun": "Son gün"}
def sayfa(pdf, p, kod, pen, r, tip, no, top):
    tvk, yk, bors = tv_kod(p, kod)
    idx, ad = isaret_gunleri(pen, r)
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.text(0.05, 0.965, f"Sayfa {no}/{top}   {tvk}", fontsize=19, weight="bold", va="top")
    fig.text(0.05, 0.935, f"Yahoo kodu: {yk}  |  {bors}  |  günlük mum", fontsize=11, va="top")
    fig.text(0.05, 0.915, f"Tarih aralığı: {tr(pen.index[0])} - {tr(pen.index[-1])}  ({len(pen)} işlem günü)", fontsize=11, va="top")
    ax = fig.add_axes([0.08, 0.60, 0.88, 0.29]); av = fig.add_axes([0.08, 0.50, 0.88, 0.09], sharex=ax)
    x = np.arange(len(pen))
    for i, (o, h, l, c) in enumerate(zip(pen.Open, pen.High, pen.Low, pen.Close)):
        col = "#1b8a4b" if c >= o else "#c0392b"
        ax.plot([i, i], [l, h], color=col, lw=0.9); ax.add_patch(Rectangle((i - 0.35, min(o, c)), 0.7, max(abs(c - o), (h - l) * 0.004), color=col))
    av.bar(x, pen.Volume.values, color=["#1b8a4b" if c >= o else "#c0392b" for o, c in zip(pen.Open, pen.Close)], width=0.8)
    rng = pen.High.max() - pen.Low.min()
    ax.set_ylim(pen.Low.min() - 0.12 * rng, pen.High.max() + 0.12 * rng); ax.set_xlim(-1, len(pen))
    for k, i in enumerate(idx):
        ust = k in (0, 2) or (k >= 4 and pen.Close.iloc[i] >= pen.Open.iloc[i] and k != 1 and k != 3)
        y = pen.High.iloc[i] if ust else pen.Low.iloc[i]
        ax.annotate(str(k + 1), xy=(i, y), xytext=(i, y + (0.09 if ust else -0.09) * rng), ha="center", va="center", fontsize=11, weight="bold",
                    color="white", bbox=dict(boxstyle="circle,pad=0.25", fc="#1f3a93", ec="none"), arrowprops=dict(arrowstyle="-|>", color="#1f3a93", lw=1.4))
    tk = list(range(0, len(pen), 20)); ax.set_xticks(tk); plt.setp(ax.get_xticklabels(), visible=False)
    av.set_xticks(tk); av.set_xticklabels([pen.index[i].strftime("%d.%m.%y") for i in tk], fontsize=8)
    ax.grid(alpha=.25); av.grid(alpha=.25); ax.tick_params(labelsize=9); av.tick_params(labelsize=8)
    ax.set_ylabel("Fiyat", fontsize=9); av.set_ylabel("Hacim", fontsize=9)
    av.yaxis.get_major_formatter().set_scientific(False)
    av.ticklabel_format(axis="y", style="plain"); av.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1e3:.0f}K"))
    # tablo
    bas = ["No", "Tarih", "Açılış", "Yüksek", "Düşük", "Kapanış", "Hacim", "Değ. %"]
    satir = []
    for k, i in enumerate(idx):
        row = pen.iloc[i]; dg = r.loc[pen.index[i]]
        satir.append([str(k + 1), tr(pen.index[i]), sayi(row.Open, p), sayi(row.High, p), sayi(row.Low, p), sayi(row.Close, p),
                      f"{row.Volume:,.0f}".replace(",", " "), "-" if pd.isna(dg) else f"{dg*100:+.2f}".replace(".", ",")])
    at = fig.add_axes([0.04, 0.215, 0.92, 0.26]); at.axis("off")
    t = at.table(cellText=satir, colLabels=bas, loc="upper center", cellLoc="center", colWidths=[.06, .15, .13, .13, .13, .13, .15, .12])
    t.auto_set_font_size(False); t.set_fontsize(10.5); t.scale(1, 2.0)
    for (a, b), c in t.get_celld().items():
        if a == 0: c.set_facecolor("#dfe6f1"); c.set_text_props(weight="bold")
    notlar = [f"{k+1} = {ETK[ad[k]]}" for k in range(6)]
    fig.text(0.05, 0.205, "   ".join(notlar[:3]), fontsize=8.5, va="top"); fig.text(0.05, 0.188, "   ".join(notlar[3:]), fontsize=8.5, va="top")
    if tip == "atlama":
        jd = r.reindex(pen.index).abs().idxmax(); jr = r.loc[jd]
        fig.text(0.05, 0.168, f"Bu pencerede büyük hareket günü: {tr(jd)} ({jr*100:+.1f}% kapanış/önceki kapanış). Şekle özellikle bak.".replace(".", ",", 0), fontsize=9, va="top", color="#7a3b00")
    fig.text(0.06, 0.09, "☐ AYNI", fontsize=18, va="center"); fig.text(0.40, 0.09, "☐ FARKLI  (not: ........................)", fontsize=15, va="center")
    pdf.savefig(fig, dpi=150); plt.close(fig)
    return dict(sayfa=no, kod=kod, tv=tvk, yahoo=yk, pazar=p, tip=tip, bas=tr(pen.index[0]), son=tr(pen.index[-1]), n=len(pen),
                gunler=[dict(no=k + 1, etiket=ETK[ad[k]], tarih=tr(pen.index[i]), O=float(pen.Open.iloc[i]), H=float(pen.High.iloc[i]), L=float(pen.Low.iloc[i]),
                             C=float(pen.Close.iloc[i]), V=float(pen.Volume.iloc[i])) for k, i in enumerate(idx)])
KAPAK = [("VERİ SINAMASI - GÖZ KARŞILAŞTIRMASI", 18, True),
 ("Ne sınanıyor?", 12, True),
 ("Ölçümlerde kullandığımız günlük fiyat verisi gerçek grafikle aynı mı? 14 hisse, her biri için 120 günlük bir pencere (2018-2023) seçildi (tohum 20261122). Senin işin: TradingView'da aynı pencereye bakıp mumların şeklinin ve tablodaki 6 günün değerlerinin aynı olup olmadığına karar vermek.", 10.5, False),
 ("Nasıl karşılaştırılır?", 12, True),
 ("1) TradingView'da hisse kodunu aç (sayfa başlığındaki kod; ABD hissesi için düz kod, BIST için BIST:KOD). Günlük (1G) grafik seç.\n2) Sayfadaki tarih aralığına git (Tarihe git / Go to date). Mum şekli ve hacim çubukları sayfadaki grafikle benzer olmalı.\n3) Tablodaki numaralı günlerin mumunun üstüne bas / imleci götür: A (açılış), Y (yüksek), D (düşük), K (kapanış) değerlerini tabloyla karşılaştır.\n4) Son sütun 'günlük değişim %' ve mum şekilleri aynı olmalı. Fiyat seviyesi sabit bir oranla farklı olabilir (aşağıdaki not).\n5) Sayfa sonunda AYNI ya da FARKLI kutusunu işaretle. FARKLI görürsen yalnız hangi sayfa ve hangi gün olduğunu yazman yeter.", 10.5, False),
 ("Veri kipi (bizim fiyatlar nasıl?)", 12, True),
 ("ABD: fiyatlar bölünme VE temettü ayarlıdır (doğrulandı: AAPL 02.01.2018 kapanış 40,23; ham kapanış 172,26 ve 4:1 bölünme ayarlı 43,07 idi, aradaki fark temettü ayarı). TradingView'da grafik ayarlarında 'Temettü ayarı (ADJ)' açık değilse eski tarihlerde fiyat SABİT bir oranla (yaklaşık %5-15) farklı görünebilir; yüzde değişimler yine aynı olmalı. Birebir sayı için ADJ'yi aç.\nBIST: fiyatlar TL, Yahoo ham kapanışı (auto_adjust kapalı); bölünme / bedelsiz sıçramaları kodla geriye doğru düzeltilmiş, temettü ayarı YOK. TradingView'da bölünme ayarı (varsayılan açık) ile aynı olmalı; ADJ kapalıyken sayılar birebir tutmalı.\nAvrupa: yerel para (Londra'da pens). Temettü ayarı durumu bu veri için tespit edilemedi; sayılar sabit oranla farklıysa 'FARKLI' yerine notta 'sabit oran' yaz; mum şekilleri ve yüzde değişim aynıysa kutuyu AYNI işaretleyebilirsin.", 10.5, False),
 ("Sayfa türleri", 12, True),
 ("Bazı sayfalarda pencerenin ortasında büyük bir hareket günü (tek günde %15'ten büyük, ya da bölünme / bedelsiz ayarı olabilecek bir sıçrama) vardır; sayfada turuncu satırla yazılıdır. Amaç ayarın ve sıçramanın gerçek grafikte de aynı görünmesini sınamak. Diğer sayfalar rastgele pencerelerdir.", 10.5, False)]
def kapak(pdf, n):
    fig = plt.figure(figsize=(8.27, 11.69)); y = 0.96
    import textwrap
    for m, fs, b in KAPAK:
        satirlar = []
        for par in m.split("\n"): satirlar += textwrap.wrap(par, 92 if fs < 12 else 60) or [""]
        for s in satirlar:
            fig.text(0.06, y, s, fontsize=fs, weight="bold" if b else "normal", va="top"); y -= 0.0185 * fs / 10.5 + (0.004 if b else 0.0)
        y -= 0.012
    pdf.savefig(fig, dpi=150); plt.close(fig)
if __name__ == "__main__":
    S = json.load(open("secim.json")); V = {p: yukle(p) for p in S}
    liste = []; sayfalar = [(p, s) for p in ("ABD", "AVR", "BIST") for s in S[p]["secim"]]
    with PdfPages("VERI_SINAMA_GOZ.pdf") as pdf:
        kapak(pdf, len(sayfalar))
        for no, (p, s) in enumerate(sayfalar, 1):
            d = V[p][s["kod"]]; d = d[(d.High >= d.Low) & (d.Volume > 0) & (d.Close > 0)]
            r = d.Close.pct_change()
            pen = d.loc[s["bas"]:s["son"]]
            liste.append(sayfa(pdf, p, s["kod"], pen, r, s["tip"], no, len(sayfalar)))
    json.dump(liste, open("goz_pencereler.json", "w"), ensure_ascii=False, indent=1)
    print(len(liste), "sayfa")
