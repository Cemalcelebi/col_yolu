import sys, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.insert(0, '/home/claude/col_yolu')
import GOZ_ESLE as G

ay = G.GozAyar(kok='etiket')
veri, e = G.k1_veri(ay)
t = pd.read_csv('karne_tum.csv')
ESIK = {'dip_konum': ('<=', 0.339, 'dip'), 'bb_min_sira': ('<=', 0.139, 'BB sikisma'), 'uz': ('>=', 29.6, 'uzun'),
        'clv': ('>=', -0.168, 'kapanis yukarda'), 'hacim_yon': ('>=', 0.915, 'alim hacmi')}


def gecti(r, m):
    op, v, _ = ESIK[m]
    x = r[m]
    return bool(np.isfinite(x) and (x <= v if op == '<=' else x >= v))


t['gecen'] = [sum(gecti(r, m) for m in ESIK) for _, r in t.iterrows()]
t['hepsi'] = t.gecen == len(ESIK)
# ayni bolgenin tekrarlarini ele: ayni hissede %30'dan fazla ortusenlerden en uzunu kalir
_kal = []
for _, r in t.sort_values('uz', ascending=False).iterrows():
    if r.tur == 'DIGER' and any(q.sembol == r.sembol and q.tur == 'DIGER' and G.iou(int(r.s), int(r.e), int(q.s), int(q.e)) > 0.3 for q in _kal):
        continue
    _kal.append(r)
t = pd.DataFrame(_kal).sort_index()


def sayfa(sec, ad, baslik):
    yollar = []
    for p0 in range(0, len(sec), 6):
        parca = sec.iloc[p0:p0 + 6]
        fig, axs = plt.subplots(len(parca), 1, figsize=(9, 3.0 * len(parca)), squeeze=False)
        for ax, (_, r) in zip(axs[:, 0], parca.iterrows()):
            df = veri[r.sembol]; ix = df.index
            s, en = int(r.s), int(r.e)
            a0 = max(0, s - 120); a1 = min(len(df) - 1, en + 60)
            x = np.arange(a0, a1 + 1)
            O, H, L, C, V = (df[c].to_numpy()[a0:a1 + 1] for c in ('Open', 'High', 'Low', 'Close', 'Volume'))
            ax.vlines(x, L, H, color='#888', lw=0.7)
            ax.vlines(x, np.minimum(O, C), np.maximum(O, C), color=np.where(C >= O, '#2a9d8f', '#c0392b'), lw=2.2)
            ax.plot(x, df.Close.rolling(50).mean().to_numpy()[a0:a1 + 1], color='#e9a23b', lw=1, label='SMA50')
            ax.plot(x, df.Close.rolling(200).mean().to_numpy()[a0:a1 + 1], color='#6c5ce7', lw=1, label='SMA200')
            for q in e[e.sembol == r.sembol].itertuples():
                if q.si0 >= a0 and q.bi0 <= a1:
                    ax.axvspan(q.bi0 - .5, q.si0 + .5, color='#2ecc71' if q.sinif == 'COL' else '#95a5a6', alpha=.2,
                               label='senin isaretin' if q.sinif == 'COL' else 'senin "degil"in')
            lo_, hi_ = df.Low.iloc[s:en + 1].min(), df.High.iloc[s:en + 1].max()
            ax.add_patch(Rectangle((s - .5, lo_), en - s + 1, hi_ - lo_, fill=False, ec='#8e44ad', lw=2, label='bolge'))
            ax2 = ax.twinx(); ax2.bar(x, V, color='#bbb', alpha=.35, width=1); ax2.set_ylim(0, np.nanmax(V) * 4); ax2.axis('off')
            cip = '  '.join(f"{'+' if gecti(r, m) else '-'}{ESIK[m][2]}" for m in ESIK)
            ax.set_title(f"{r.sembol}  {ix[s]:%d.%m.%Y}-{ix[en]:%d.%m.%Y} ({en - s + 1} bar)   [{cip}]", fontsize=8.5)
            tk = np.linspace(a0, a1, 6).astype(int)
            ax.set_xticks(tk); ax.set_xticklabels([f"{ix[i]:%m.%y}" for i in tk], fontsize=7)
            ax.tick_params(axis='y', labelsize=7); ax.legend(fontsize=6, loc='upper left', ncol=4)
        fig.suptitle(baslik, fontsize=10, y=1.0)
        fig.tight_layout()
        y = f"karne_{ad}_{p0 // 6 + 1:02d}.png"; fig.savefig(y, dpi=105, bbox_inches='tight'); plt.close(fig); yollar.append(y)
    return yollar


ys = []
ys += sayfa(t[(t.tur == 'DIGER') & t.hepsi].sort_values(['sembol', 's']), 'yeni', 'Makinenin buldugu, senin isaretlemedigin: 5 izin hepsi var')
ys += sayfa(t[t.tur == 'COL'].sort_values(['gecen', 'sembol'], ascending=[False, True]), 'senin', 'Senin colun: hangi iz var (+) hangisi yok (-)')
ys += sayfa(t[t.tur == 'OLUMSUZ'].sort_values('sembol'), 'degil', 'Senin "col degil" dediklerin')
print('\n'.join(ys))
t.to_csv('karne_tum.csv', index=False)
