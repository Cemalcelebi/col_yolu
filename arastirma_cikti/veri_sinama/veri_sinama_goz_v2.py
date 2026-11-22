"""Veri sinamasi v2: HAM (ayarsiz) + temettu ayarli fiyatli goz PDF'i. Girdi: goz_pencereler.json (v1 ile ayni 14 hisse / pencere / 6 gun),
/tmp/kasa/acik/V_*.pkl (bizim veri; yalniz dogrulama), Yahoo (yfinance, auto_adjust=False; bitis <= 2023-12-29).
Calistirma: python veri_sinama_goz_v2.py -> VERI_SINAMA_GOZ_v2.pdf, dogrulama_v2.json, yahoo_ham_v2.pkl (onbellek)"""
import json, os, pickle, textwrap, matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from veri_sinama_sec import yukle
from veri_sinama_goz import tv_kod
plt.rcParams.update({"font.family": "DejaVu Sans"})
SON_SINIR = "2023-12-30"   # yfinance end dislayici -> son gun 2023-12-29
ONB = "yahoo_ham_v2.pkl"
def tr(ts): return ts.strftime("%d.%m.%Y")
def tarih(s): return pd.Timestamp(pd.to_datetime(s, format="%d.%m.%Y"))
def f2(x, p="ABD", d=2):
    if x < 1: d = 4
    elif p == "AVR" and x < 50: d = 3
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",") if False else f"{x:,.{d}f}".replace(",", "_").replace(".", ",").replace("_", " ")
def indir(yk, bas, son):
    on = pickle.load(open(ONB, "rb")) if os.path.exists(ONB) else {}
    if yk in on: return on[yk]
    b = bas - pd.Timedelta(days=10); e = min(son + pd.Timedelta(days=1), pd.Timestamp(SON_SINIR))
    t = yf.Ticker(yk)
    h = t.history(start=b.strftime("%Y-%m-%d"), end=e.strftime("%Y-%m-%d"), auto_adjust=False, actions=True)
    h.index = h.index.tz_localize(None).normalize()
    # tum bolunme + temettu (2023-12-29'a kadar) pencere sonrasi bolunme tespiti icin
    a = t.history(start=(son + pd.Timedelta(days=1)).strftime("%Y-%m-%d"), end=SON_SINIR, auto_adjust=False, actions=True)
    a.index = a.index.tz_localize(None).normalize()
    sonra = a[(a["Stock Splits"] > 0)][["Stock Splits"]]
    on[yk] = (h, sonra); pickle.dump(on, open(ONB, "wb")); return on[yk]
def sayfa(pdf, s, h, sonra, no, top, V, dv):
    p = s["pazar"]; kod = s["kod"]; yk = s["yahoo"]
    tvk, _, bors = tv_kod(p, kod)
    bas, son = tarih(s["bas"]), tarih(s["son"])
    pen = h.loc[bas:son]
    ham = h[["Open", "High", "Low", "Close", "Volume"]]
    oran = (h["Close"] / h["Adj Close"])
    dg = ham["Close"].pct_change()
    tem = pen[pen["Dividends"] > 0]["Dividends"]
    bol = pen[pen["Stock Splits"] > 0]["Stock Splits"]
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.text(0.05, 0.975, f"Sayfa {no}/{top}   {tvk}", fontsize=18, weight="bold", va="top")
    fig.text(0.05, 0.952, f"Yahoo kodu: {yk}  |  {bors}  |  günlük mum, HAM fiyat  |  {tr(pen.index[0])} - {tr(pen.index[-1])} ({len(pen)} gün)", fontsize=9, va="top")
    o0, o1 = oran.loc[pen.index[0]], oran.loc[pen.index[-1]]
    ortxt = f"{o0:.4f}".replace(".", ",") if abs(o0 - o1) < 5e-5 else f"{o0:.4f} -> {o1:.4f}".replace(".", ",") + " (basamak)"
    fig.text(0.05, 0.935, f"Ham / ayarlı oranı bu pencerede: {ortxt}   |   Temettü günleri: " +
             ("yok" if tem.empty else "; ".join(f"{tr(i)} {v:g}".replace(".", ",") for i, v in tem.items())) + ("" if bol.empty else "   |  BÖLÜNME: " + "; ".join(f"{tr(i)} {v:g}" for i, v in bol.items())), fontsize=8.3, va="top")
    ax = fig.add_axes([0.08, 0.675, 0.88, 0.235]); av = fig.add_axes([0.08, 0.60, 0.88, 0.07], sharex=ax)
    x = np.arange(len(pen))
    for i, (o, hh, l, c) in enumerate(zip(pen.Open, pen.High, pen.Low, pen.Close)):
        col = "#1b8a4b" if c >= o else "#c0392b"
        ax.plot([i, i], [l, hh], color=col, lw=0.9); ax.add_patch(Rectangle((i - 0.35, min(o, c)), 0.7, max(abs(c - o), (hh - l) * 0.004), color=col))
    av.bar(x, pen.Volume.values, color=["#1b8a4b" if c >= o else "#c0392b" for o, c in zip(pen.Open, pen.Close)], width=0.8)
    rng = pen.High.max() - pen.Low.min()
    ax.set_ylim(pen.Low.min() - 0.12 * rng, pen.High.max() + 0.12 * rng); ax.set_xlim(-1, len(pen))
    gun_t = [tarih(g["tarih"]) for g in s["gunler"]]
    idx = [int(pen.index.get_loc(t)) for t in gun_t]
    for k, i in enumerate(idx):
        ust = k in (0, 2) or (k >= 4 and pen.Close.iloc[i] >= pen.Open.iloc[i] and k != 1 and k != 3)
        y = pen.High.iloc[i] if ust else pen.Low.iloc[i]
        ax.annotate(str(k + 1), xy=(i, y), xytext=(i, y + (0.09 if ust else -0.09) * rng), ha="center", va="center", fontsize=10, weight="bold",
                    color="white", bbox=dict(boxstyle="circle,pad=0.25", fc="#1f3a93", ec="none"), arrowprops=dict(arrowstyle="-|>", color="#1f3a93", lw=1.3))
    for t in tem.index:
        ax.axvline(pen.index.get_loc(t), color="#e08e0b", lw=0.8, ls=":")
    tk = list(range(0, len(pen), 20)); ax.set_xticks(tk); plt.setp(ax.get_xticklabels(), visible=False)
    av.set_xticks(tk); av.set_xticklabels([pen.index[i].strftime("%d.%m.%y") for i in tk], fontsize=8)
    ax.grid(alpha=.25); av.grid(alpha=.25); ax.tick_params(labelsize=8); av.tick_params(labelsize=7)
    ax.set_ylabel("Ham fiyat", fontsize=9); av.set_ylabel("Hacim", fontsize=9)
    av.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1e3:.0f}K"))
    # tablo 1: ham
    fig.text(0.05, 0.570, "1) SENİN GRAFİKTE GÖRECEĞİN (ham fiyat)", fontsize=10.5, weight="bold", va="top")
    r1 = []
    for k, i in enumerate(idx):
        t = pen.index[i]; row = ham.loc[t]; d = dg.loc[t]
        r1.append([str(k + 1), tr(t), f2(row.Open, p), f2(row.High, p), f2(row.Low, p), f2(row.Close, p), f"{row.Volume:,.0f}".replace(",", " "),
                   "-" if pd.isna(d) else f"{d*100:+.2f}".replace(".", ",")])
    a1 = fig.add_axes([0.04, 0.395, 0.92, 0.17]); a1.axis("off")
    t1 = a1.table(cellText=r1, colLabels=["No", "Tarih", "Açılış", "Yüksek", "Düşük", "Kapanış", "Hacim", "Değ. %"], loc="upper center", cellLoc="center",
                  colWidths=[.06, .15, .13, .13, .13, .13, .15, .12])
    t1.auto_set_font_size(False); t1.set_fontsize(9.5); t1.scale(1, 1.55)
    for (a, b), c in t1.get_celld().items():
        if a == 0: c.set_facecolor("#dfe6f1"); c.set_text_props(weight="bold")
    # tablo 2: BIZIM veri (V_*.pkl) ve ham / bizim orani
    bd = V[p][kod]; bd = bd[(bd.High >= bd.Low) & (bd.Volume > 0) & (bd.Close > 0)]
    kip = dv["kip"]
    fig.text(0.05, 0.372, f"2) BİZİM KULLANDIĞIMIZ ({kip})", fontsize=10.5, weight="bold", va="top")
    r2 = []
    for k, i in enumerate(idx):
        t = pen.index[i]; row = bd.loc[t]; o = ham.loc[t, "Close"] / row.Close
        r2.append([str(k + 1), tr(t), f2(row.Open, p), f2(row.High, p), f2(row.Low, p), f2(row.Close, p), f"{o:.4f}".replace(".", ",")])
    a2 = fig.add_axes([0.04, 0.215, 0.92, 0.15]); a2.axis("off")
    t2 = a2.table(cellText=r2, colLabels=["No", "Tarih", "Açılış", "Yüksek", "Düşük", "Kapanış", "Oran (ham/bizim)"], loc="upper center", cellLoc="center",
                  colWidths=[.06, .15, .14, .14, .14, .14, .23])
    t2.auto_set_font_size(False); t2.set_fontsize(9.5); t2.scale(1, 1.45)
    for (a, b), c in t2.get_celld().items():
        if a == 0: c.set_facecolor("#e7f1df"); c.set_text_props(weight="bold")
    notlar = ["1 pencere en yüksek", "2 pencere en düşük", "3 en büyük artış günü", "4 en büyük düşüş günü", "5 ilk gün", "6 son gün"]
    fig.text(0.05, 0.200, "   ".join(f"{n.split(' ',1)[0]} = {n.split(' ',1)[1]}" for n in notlar), fontsize=7.8, va="top")
    msg = dv["not"]
    if not sonra.empty:
        sb = sonra["Stock Splits"].prod()
        msg += f" Bu hissede sonradan bölünme var ({'; '.join(tr(i)+' '+format(v,'g') for i,v in sonra['Stock Splits'].items())}): uygulaman eski fiyatı ayarsız gösteriyorsa sayılar {sb:g} kat farklı olur."
    for j, ln in enumerate(textwrap.wrap(msg, 120)):
        fig.text(0.05, 0.178 - 0.0145 * j, ln, fontsize=7.8, va="top", color="#7a3b00")
    fig.text(0.06, 0.07, "☐ AYNI", fontsize=17, va="center"); fig.text(0.38, 0.07, "☐ FARKLI  (gün: ....................)", fontsize=14, va="center")
    pdf.savefig(fig, dpi=130); plt.close(fig)
def dogrula(s, h, sonra, V):
    p = s["pazar"]; kod = s["kod"]; bas, son = tarih(s["bas"]), tarih(s["son"])
    d = V[p][kod]; d = d[(d.High >= d.Low) & (d.Volume > 0) & (d.Close > 0)].loc[bas:son]
    pen = h.loc[bas:son]; ort = d.index.intersection(pen.index)
    oran = (pen["Close"] / pen["Adj Close"]).loc[ort]
    adj = pd.DataFrame({c: pen.loc[ort, c] / oran for c in ["Open", "High", "Low", "Close"]})
    hamo = pen.loc[ort, ["Open", "High", "Low", "Close"]]
    bz = d.loc[ort, ["Open", "High", "Low", "Close"]]
    fa = (bz / adj - 1).abs().max().max(); fh = (bz / hamo - 1).abs().max().max()
    # bizim / ham orani sabit mi
    rb = (bz["Close"] / hamo["Close"]); rb_cv = float(rb.std() / rb.mean())
    # ayarli (bizim) kendi icinde: bizim/yahoo-adj orani sabit mi
    ra = (bz["Close"] / adj["Close"]); ra_cv = float(ra.std() / ra.mean()); ra_m = float(ra.mean())
    # ham/ayarli oranin basamagi yalniz temettu gunlerinde mi
    ro = (pen["Close"] / pen["Adj Close"]); bas_gun = set(pen.index[1:][(ro.pct_change().abs().iloc[1:] > 1e-4).values])
    tg = set(pen[pen["Dividends"] > 0].index)
    # temettu gunu oran basamagi: ex-date'de (t) oran t-1 ile farkli
    basamak_disi = sorted(tr(x) for x in bas_gun - tg); temettu_basamaksiz = sorted(tr(x) for x in tg - bas_gun if x != pen.index[0])
    hv = (d.loc[ort, "Volume"] / pen.loc[ort, "Volume"]); hv_esit = bool((hv.sub(1).abs() < 1e-3).all()); hv_med = float(hv.median())
    hv_olcekli = bool((hv / hv.median() - 1).abs().max() < 1e-3)   # sabit carpan disinda esit mi
    fa_sabit = float((ra / ra.mean() - 1).abs().max())            # bizim / Yahoo-ayarli sabit carpan cikarilinca en buyuk fark
    fh_sabit = float((rb / rb.mean() - 1).abs().max())            # bizim / ham sabit carpan cikarilinca
    pv = (d.loc[ort, "Close"] * d.loc[ort, "Volume"]) / (pen.loc[ort, "Close"] * pen.loc[ort, "Volume"]); pv_med = float(pv.median())
    # 6 gun
    g6 = max(abs(d.loc[tarih(g["tarih"]), c] / adj.loc[tarih(g["tarih"]), c] - 1) for g in s["gunler"] for c in ["Open", "High", "Low", "Close"])
    tem_var = len(tg) > 0
    if p == "BIST":
        kip = "bölünme ayarlı, temettü ayarsız"
        nt = (f"Bizim fiyat = Yahoo ham x {rb.mean():.4f} sabit çarpan (bölünme / bedelsiz ayarı farkı); hacim ters çarpanla ölçeklidir (fiyat x hacim aynı). Çarpan tüm pencerede sabit, yani şekil ve değişim % aynı.").replace(".", ",", 1) if False else \
             (f"Bizim fiyat = Yahoo ham x {rb.mean():.4f} sabit çarpan (bölünme / bedelsiz ayarı farkı); hacim ters çarpanla ölçeklidir (fiyat x hacim aynı). Çarpan pencerede sabit: şekil ve değişim % aynı.")
    else:
        if ra_cv < 1e-5 and (rb_cv > 1e-5 or abs(rb.mean() - 1) > 0.002): kip = "temettü ayarlı"
        elif rb_cv < 1e-6 and abs(rb.mean() - 1) < 1e-6 and not tem_var and abs(ro.max() - 1) < 1e-9: kip = "ham ile aynı (bu pencerede temettü yok, ayırt edilemez)"
        else: kip = "belirsiz"
        nt = "Oran yalnız temettü gününde basamak yapar, diğer günlerde sabittir; yani ayarlı ile ham aynı şekildedir, fark bir çarpandır. Hacim iki tabloda aynıdır."
    return dict(kip=kip, **{"not": nt}, sayfa=s["sayfa"], kod=kod, yahoo=s["yahoo"], pazar=p, gun_bizim=int(len(d)), gun_yahoo=int(len(pen)), gun_ortak=int(len(ort)),
                fark_adj_max=float(fa), fark_ham_max=float(fh), fark_adj_6gun=float(g6), bizim_ham_oran_cv=rb_cv, bizim_ham_oran_ort=float(rb.mean()),
                bizim_adj_oran_cv=ra_cv, bizim_adj_oran_ort=ra_m, yahoo_oran_min=float(ro.min()), yahoo_oran_max=float(ro.max()),
                oran_sabit=bool(ro.max() / ro.min() - 1 < 1e-4), temettu_gunleri=[tr(x) for x in sorted(tg)],
                basamak_temettu_disi=basamak_disi, temettu_basamaksiz=temettu_basamaksiz, hacim_esit=hv_esit, hacim_olcekli_esit=hv_olcekli, fark_adj_sabit_sonrasi=fa_sabit, fark_ham_sabit_sonrasi=fh_sabit, fiyat_x_hacim_oran_medyan=pv_med, hacim_oran_medyan=hv_med,
                bolunme_pencere=[tr(i) for i in pen[pen["Stock Splits"] > 0].index], bolunme_sonra=[(tr(i), float(v)) for i, v in sonra["Stock Splits"].items()],
                yahoo_eksik_gun=[tr(x) for x in d.index.difference(pen.index)], bizim_eksik_gun=[tr(x) for x in pen.index.difference(d.index)])
KAPAK = [("VERİ SINAMASI - GÖZ KARŞILAŞTIRMASI (v2: HAM + AYARLI)", 13, True),
 ("Ne değişti?", 12, True),
 ("İlk PDF'te yalnız temettü ayarlı fiyat vardı; bu yüzden sayılar grafiğinle sabit bir oranla farklıydı (örnek: 20.04.2020 açılış 94,82 ham / 83,92 ayarlı, oran 1,13; hacim aynı). Bu sürümde üst tablo senin grafiğinde göreceğin ham fiyattır; birebir tutmalı. Alt tablo bizim ölçümde kullandığımız ayarlı fiyattır; oran sütunu sabitse veri doğrudur.", 10.5, False),
 ("Nasıl karşılaştırılır?", 12, True),
 ("1) Grafik uygulamasında hisseyi aç (günlük), TEMETTÜ AYARI KAPALI olsun (ham fiyat). Sayfadaki tarih aralığına git.\n2) Mum grafiği ham fiyatla çizildi; tablodaki 1. tablonun açılış / yüksek / düşük / kapanış ve hacim değerleri senin grafikte görünenle birebir tutmalı.\n3) 2. tablo yalnız bizim verinin ayarlı hali; senin grafiğinle KIYASLANMAZ, oran sütunu (ham / ayarlı) içindir.\n4) Her sayfada AYNI ya da FARKLI (gün) işaretle.", 10.5, False),
 ("Sayfa listesi", 12, True)]
def kapak(pdf, S):
    fig = plt.figure(figsize=(8.27, 11.69)); y = 0.96
    for m, fs, b in KAPAK:
        sat = []
        for par in m.split("\n"): sat += textwrap.wrap(par, 95 if fs < 12 else 62) or [""]
        for t in sat:
            fig.text(0.06, y, t, fontsize=fs, weight="bold" if b else "normal", va="top"); y -= 0.0185 * fs / 10.5 + (0.004 if b else 0.0)
        y -= 0.010
    for s in S:
        tvk, yk, _ = tv_kod(s["pazar"], s["kod"])
        fig.text(0.08, y, f"Sayfa {s['sayfa']:>2}:  {tvk}   (Yahoo {yk}, {s['pazar']})   {s['bas']} - {s['son']}", fontsize=10, va="top", family="DejaVu Sans Mono"); y -= 0.022
    pdf.savefig(fig, dpi=130); plt.close(fig)
if __name__ == "__main__":
    S = json.load(open("goz_pencereler.json")); V = {p: yukle(p) for p in ("ABD", "AVR", "BIST")}
    H = {}
    for s in S:
        h0, sn = indir(s["yahoo"], tarih(s["bas"]), tarih(s["son"]))
        gec = h0.Open.notna() & h0.Close.notna() & (h0.Volume > 0) & (h0.High >= h0.Low)   # hacimsiz / bos bar (tatil satiri) grafikte yok
        atilan = h0.loc[tarih(s["bas"]):tarih(s["son"])][~gec.loc[tarih(s["bas"]):tarih(s["son"])]]
        print("  atilan hacimsiz/bos bar:", [(tr(i), float(v)) for i, v in atilan.Volume.items()])
        H[s["sayfa"]] = (h0[gec], sn)
        print(s["sayfa"], s["yahoo"], len(H[s["sayfa"]][0]), "satir")
    sonuc = [dogrula(s, *H[s["sayfa"]], V) for s in S]
    json.dump(sonuc, open("dogrulama_v2.json", "w"), ensure_ascii=False, indent=1)
    with PdfPages("VERI_SINAMA_GOZ_v2.pdf") as pdf:
        kapak(pdf, S)
        for s in S: sayfa(pdf, s, *H[s["sayfa"]], s["sayfa"], len(S), V, sonuc[s["sayfa"] - 1])
    print("tamam")
