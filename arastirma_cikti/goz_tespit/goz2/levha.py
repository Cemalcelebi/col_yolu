# Ana modelin göz denetimi için levha çizici (denetim aracı; üretim kodu değil). Yalnız bölge sonuna kadar çizer.
import sys, json, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/col_yolu')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def mum(ax, d, kutu=None):
    O, H, L, C = (d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close')); x = np.arange(len(C))
    yuk = C >= O; renk = np.where(yuk, '#1a9850', '#d73027')
    ax.vlines(x, L, H, color=renk, linewidth=0.6)
    ax.bar(x, np.maximum(np.abs(C - O), (H.max() - L.min()) * 0.002), bottom=np.minimum(O, C), color=renk, width=0.7, linewidth=0)
    if kutu:
        a, b = kutu; lo = L[a:b + 1].min(); hi = H[a:b + 1].max()
        ax.add_patch(Rectangle((a - 0.5, lo), b - a + 1, hi - lo, facecolor='#ffb347', alpha=0.25, edgecolor='#ff7f00', linewidth=1.0))
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(-1, len(C))
    lo_, hi_ = np.percentile(L, 1), np.percentile(H, 99); pad = 0.06 * (hi_ - lo_ + 1e-12); ax.set_ylim(lo_ - pad, hi_ + pad)

def levha(hucreler, yol, sutun=4, baslik=None):
    """hucreler: [(etiket, df_kesik, s, t)]; df_kesik bölge sonunda biter (assert)."""
    n = len(hucreler); satir = (n + sutun - 1) // sutun
    fig = plt.figure(figsize=(sutun * 4.5, satir * 5.0), dpi=100)
    for i, (et, d, s, t) in enumerate(hucreler):
        assert len(d) == t + 1, 'geleceğe bakma'
        r, c = divmod(i, sutun); x0 = c / sutun + 0.004; w = 1 / sutun - 0.008; y1 = 1 - (r + 1) / satir
        h = 1 / satir
        axu = fig.add_axes([x0, y1 + h * 0.47, w, h * 0.45]); iu = max(0, s - 120); mum(axu, d.iloc[iu:t + 1], (s - iu, t - iu))
        axu.set_title(f"{et}  (bölge {t - s + 1} mum)", fontsize=11, loc='left', pad=2)
        axy = fig.add_axes([x0, y1 + h * 0.03, w, h * 0.41]); iy = max(0, s - 10); mum(axy, d.iloc[iy:t + 1], (s - iy, t - iy))
    if baslik: fig.suptitle(baslik, fontsize=10, y=0.999)
    fig.savefig(yol); plt.close(fig)
