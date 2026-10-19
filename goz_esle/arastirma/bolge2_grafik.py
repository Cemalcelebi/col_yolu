import sys, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.insert(0, '.')
from bolge2 import *

PRM = dict(bant_kat=6, uzak_kat=1.5, sol_kat=1.5)
t = pd.read_csv('doji_tum.csv')
# once Cemal'in isaretledigi iki ornek (ARZUM, BINBN 2026), sonra digerleri
c = t[t.tur == 'COL'].copy()
c['on'] = c.sembol.isin(['ARZUM', 'BINBN']).astype(int)
c = c.sort_values(['on', 'iou'], ascending=[False, True])


def sayfa(sec, ad, baslik):
    ys = []
    for p0 in range(0, len(sec), 6):
        parca = sec.iloc[p0:p0 + 6]
        fig, axs = plt.subplots(len(parca), 1, figsize=(9, 3.0 * len(parca)), squeeze=False)
        for ax, (_, r) in zip(axs[:, 0], parca.iterrows()):
            df = veri[r.sembol]; ix = df.index; D = DZ[r.sembol]
            s, en = int(r.s), int(r.e)
            a0 = max(0, s - 100); a1 = min(len(df) - 1, en + 50)
            x = np.arange(a0, a1 + 1)
            O, H, L, C = (D[k][a0:a1 + 1] for k in ('O', 'H', 'L', 'C'))
            ax.vlines(x, L, H, color='#888', lw=0.7)
            ax.vlines(x, np.minimum(O, C), np.maximum(O, C), color=np.where(C >= O, '#2a9d8f', '#c0392b'), lw=2.2)
            ax.plot(x, df.Close.rolling(50).mean().to_numpy()[a0:a1 + 1], color='#e9a23b', lw=1, label='SMA50')
            dj = D['go'][a0:a1 + 1] < 0.1
            ax.scatter(x[dj], L[dj] * 0.985, s=7, color='#222', zorder=5, label='doji')
            for q in e[e.sembol == r.sembol].itertuples():
                if q.si0 >= a0 and q.bi0 <= a1:
                    ax.axvspan(q.bi0 - .5, q.si0 + .5, color='#2ecc71' if q.sinif == 'COL' else '#95a5a6', alpha=.2,
                               label='senin isaretin' if q.sinif == 'COL' else 'senin "degil"in')
            lo_, hi_ = D['L'][s:en + 1].min(), D['H'][s:en + 1].max()
            ax.add_patch(Rectangle((s - .5, lo_), en - s + 1, hi_ - lo_, fill=False, ec='#8e44ad', lw=2, label='yeni bolge'))
            ax.set_title(f"{r.sembol}  {ix[s]:%d.%m.%Y}-{ix[en]:%d.%m.%Y} ({en - s + 1} bar)   ortusme %{100 * r.get('iou', 0):.0f}   "
                         f"doji {100 * r['doji_0.1']:.0f}% (hissenin normalinin {r['doji_goreli_0.1']:.1f} kati)   dip {r['dip_konum']:.2f}", fontsize=8)
            tk = np.linspace(a0, a1, 6).astype(int)
            ax.set_xticks(tk); ax.set_xticklabels([f"{ix[i]:%m.%y}" for i in tk], fontsize=7)
            ax.tick_params(axis='y', labelsize=7); ax.legend(fontsize=6, loc='upper left', ncol=4)
        fig.suptitle(baslik, fontsize=10, y=1.0); fig.tight_layout()
        y = f'bolge2_{ad}_{p0 // 6 + 1:02d}.png'; fig.savefig(y, dpi=105, bbox_inches='tight'); plt.close(fig); ys.append(y)
    return ys


print(sayfa(c, 'senin', 'Yeni bolge: inis mumlari kirpildi, az ayrilma kabul / cok ayrilma dur. Siyah nokta = doji'))
