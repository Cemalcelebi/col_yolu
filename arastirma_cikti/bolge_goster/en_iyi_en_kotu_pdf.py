"""en_iyi_en_kotu_pdf: DS (dusus_sonrasi) ve S6 (olay_Y1) ABD 2023-26 olaylarinin STOP'SUZ R15'e gore en iyi / en kotu 20 bolgesi.
R15 = 15. gecerli barin kapanisi / giris (t+1 acilis) - 1. Siralama sonradan bakmadir, iz degildir. Hisse adi ve tarih yazilir (kor degil).
Kullanim: OC_VERI=/tmp/veri python arastirma_cikti/bolge_goster/en_iyi_en_kotu_pdf.py"""
import os, sys, logging
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle

KL = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.abspath(os.path.join(KL, "..", ".."))
sys.path.insert(0, KOK)
import ORTAK_CETVEL as OC
log = logging.getLogger("col.en_iyi_en_kotu"); logging.basicConfig(level=logging.INFO)
ONCE, SONRA, UFUK, N = 120, 30, 15, 20


def olaylar_ds():
    d = pd.read_csv(os.path.join(KOK, "arastirma_cikti/dusus_sonrasi/ds_olay.csv.gz"))
    d = d[(d.pazar == "ABD") & (d.donem == "sinama") & (d.olc == 1)].copy()
    return d[["sembol", "tarih", "giris", "hat"]]


def olaylar_s6():
    d = pd.read_csv(os.path.join(KOK, "arastirma_cikti/yapi_hedef/olay_Y1.csv.gz"))
    d = d[(d.pazar == "ABD") & d.donem.isin(["2023", "2024-26"]) & (d.olc == True)].copy()  # noqa: E712
    return d[["sembol", "tarih", "giris", "hat"]]


def olc(ev, V):
    """Her olay icin R15, h5/h10/st (15 barda, stop'suz R15 ayri), bar penceresi."""
    out = []; atl = 0
    for r in ev.itertuples():
        d = V.get(r.sembol)
        if d is None: atl += 1; continue
        t = pd.Timestamp(r.tarih)
        if t not in d.index: atl += 1; continue
        i = d.index.get_loc(t); gi = i + 1
        if gi + UFUK >= len(d) or d.index[gi] != pd.Timestamp(r.giris): atl += 1; continue
        E0 = float(d.Open.iloc[gi]); stop = r.hat * 0.98
        w = d.iloc[gi:gi + UFUK]
        out.append(dict(sembol=r.sembol, tarih=t, giris=pd.Timestamp(r.giris), hat=float(r.hat), E0=E0, stop=stop,
                        r15=float(d.Close.iloc[gi + UFUK - 1] / E0 - 1),
                        h5=int(w.High.max() >= E0 * 1.05), h10=int(w.High.max() >= E0 * 1.10), st5=int(w.Low.min() <= stop), i=i))
    if atl: log.warning("atlanan olay: %d", atl)
    return pd.DataFrame(out)


def sayfa(pdf, d, r, baslik, sira, kume):
    i = r.i; a = max(0, i - ONCE); b = min(len(d), i + 1 + 1 + SONRA)
    w = d.iloc[a:b]; x = np.arange(len(w)); xi = i - a
    fig, (ax, av) = plt.subplots(2, 1, figsize=(11, 6.6), gridspec_kw={"height_ratios": [4, 1]}, sharex=True)
    up = (w.Close >= w.Open).to_numpy(); col = np.where(up, "#1a7f37", "#c62828")
    ax.add_collection(LineCollection([[(k, lo), (k, hi)] for k, lo, hi in zip(x, w.Low, w.High)], colors=col, linewidths=0.7))
    ax.add_collection(LineCollection([[(k, o), (k, c)] for k, o, c in zip(x, w.Open, w.Close)], colors=col, linewidths=2.6))
    ax.axvline(xi, color="#555", lw=1, ls="--"); ax.axvline(xi + 1, color="#1565c0", lw=0.8, ls=":")
    ax.add_patch(Rectangle((xi + 1 - .5, w.Low.min()), UFUK, w.High.max() - w.Low.min(), color="#ffeb3b", alpha=.15, lw=0))
    for y, c, l in ((r.E0, "#1565c0", "giriş %.2f" % r.E0), (r.hat, "#0277bd", "hat %.2f" % r.hat), (r.stop, "#c62828", "stop %.2f" % r.stop),
                    (r.E0 * 1.05, "#2e7d32", "+%5"), (r.E0 * 1.10, "#1b5e20", "+%10")):
        ax.axhline(y, color=c, lw=0.9, ls="-" if "giriş" in l else "--"); ax.text(len(w) - 0.5, y, l, color=c, fontsize=7, va="bottom", ha="right")
    ax.set_xlim(-1, len(w)); ax.set_ylim(min(w.Low.min(), r.stop) * 0.98, max(w.High.max(), r.E0 * 1.10) * 1.02)
    av.bar(x, w.Volume, color=col, width=.8)
    ax.set_title("%s %d/%d   %s ABD   sinyal %s   R15 %+.1f%%\n+%%5 15 barda görüldü: %s   stop'a değdi: %s   (sıralama sonradan bakmadır, iz değildir)" % (
        kume, sira, N, r.sembol, r.tarih.date(), r.r15 * 100, "EVET" if r.h5 else "HAYIR", "EVET" if r.st5 else "HAYIR"), fontsize=10, loc="left")
    tk = list(range(0, len(w), 20)); av.set_xticks(tk); av.set_xticklabels([str(w.index[k].date()) for k in tk], rotation=30, fontsize=7)
    fig.tight_layout(); pdf.savefig(fig, dpi=150); plt.close(fig)


def kapak(pdf, ad, tanim, n, q):
    fig = plt.figure(figsize=(11, 6.6)); fig.text(.05, .9, "EN İYİ 20 / EN KÖTÜ 20 — %s" % ad, fontsize=18, weight="bold")
    s = ["Olay kümesi: " + tanim, "Dönem: ABD 2023-26 (sınama), hisse adı ve tarih yazılı (kör değil)", "n = %d olay" % n,
         "Sıralama ölçüsü: STOP'SUZ R15 = 15. geçerli barın kapanışı / giriş (t+1 açılış) - 1",
         "R15 dağılımı: medyan %+.1f%%, %%10 %+.1f%%, %%90 %+.1f%%" % (q[1] * 100, q[0] * 100, q[2] * 100),
         "Sayfa: sinyalden 120 bar önce, 30 bar sonra; kesik dikey = sinyal günü; mavi = giriş; hat; stop = hat x 0,98; +%5 / +%10; sarı = 15 bar",
         "", "SIRALAMA SONRADAN BAKMADIR, İZ DEĞİLDİR. En iyi / en kötü uçlar seçilim yanlılığıyla doludur."]
    for k, t in enumerate(s): fig.text(.05, .78 - k * .08, t, fontsize=11)
    pdf.savefig(fig); plt.close(fig)


def uret(ad, kume_ad, tanim, ev, V, dosya):
    R = olc(ev, V).sort_values("r15", ascending=False).reset_index(drop=True)
    q = R.r15.quantile([.1, .5, .9]).to_numpy()
    iyi = R.head(N); kotu = R.tail(N).iloc[::-1]
    with PdfPages(dosya) as pdf:
        kapak(pdf, ad, tanim, len(R), q)
        for etk, S in (("EN İYİ", iyi), ("EN KÖTÜ", kotu)):
            for k, r in enumerate(S.itertuples(), 1):
                sayfa(pdf, V[r.sembol], r, ad, k, etk)
    md = dosya.replace(".pdf", "_liste.md")
    with open(md, "w") as f:
        f.write("# %s — ABD 2023-26, n=%d, R15 medyan %+.1f%% (p10 %+.1f%%, p90 %+.1f%%)\nSıralama sonradan bakmadır, iz değildir.\n\n" % (ad, len(R), q[1] * 100, q[0] * 100, q[2] * 100))
        for etk, S in (("EN İYİ 20", iyi), ("EN KÖTÜ 20", kotu)):
            f.write("## %s\n\n| # | sembol | sinyal | R15 %% | h5 | st5 |\n|---|---|---|---|---|---|\n" % etk)
            for k, r in enumerate(S.itertuples(), 1):
                f.write("| %d | %s | %s | %+.1f | %d | %d |\n" % (k, r.sembol, r.tarih.date(), r.r15 * 100, r.h5, r.st5))
            f.write("\n")
    log.info("%s: n=%d medyan %.3f MB=%.1f", ad, len(R), q[1], os.path.getsize(dosya) / 1e6)
    return R, q


if __name__ == "__main__":
    V = OC.oc_veri("ABD")["V"]
    uret("DS düşüş sonrası", "DS", "düşüş sonrası olay: tepeden >= %30 düşüş + 120 gün aralığının alt çeyreği", olaylar_ds(), V, os.path.join(KL, "EN_IYI_EN_KOTU_DS_ABD_2023-26.pdf"))
    uret("S6 taban kırılımı", "S6", "S6 taban kırılımı (olay_Y1, hat üstüne kırılım)", olaylar_s6(), V, os.path.join(KL, "EN_IYI_EN_KOTU_S6_ABD_2023-26.pdf"))
