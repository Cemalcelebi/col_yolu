"""Olcum (21 Eki, Cemal'in ARZUM cizimi): aranan desen kucuk olcekte de var — dip -> savunma -> yukari yuvarlanan kucuk mum obegi,
bir hissede arka arkaya birkac kez. 'Yuvarlanma obegi' tanimi (ilk deneme):
  pencere w = 10..25 bar; dip pencerenin ilk %40'inda; dipten sonra yeni dip yok (dibe en cok 1 normal gun yaklasir);
  diplerin parabolu ic bukey ve sonda yukari (a>0, son_egim>0) veya son ucte bir dip medyani > orta ucte bir > dip;
  mumlar kucuk: pencere aralik medyani <= 0.9 x onceki 60 gunun medyani; pencere yuksekligi <= 5 x pencere aralik medyani.
Ortusen pencerelerden en uzunu kalir. Grafik: senin ciziminle kiyas icin.
Calistirma: python3 obek_tani.py <repo_kok> <sembol> <bas> <son> <png>"""
import sys, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

K, SEM, BAS, SON, PNG = sys.argv[1:6]
v = pd.read_csv(f'{K}/kalibre_veri.csv', parse_dates=['tarih'])
df = v[v.sembol == SEM].set_index('tarih').sort_index()[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
O, H, L, C, V = (df[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close', 'Volume'))
pc = np.r_[O[0], C[:-1]]; ar = 100 * (H - L) / pc
n = len(df)


def obek(s, e):
    w = e - s + 1
    d = s + int(np.argmin(L[s:e + 1]))
    if (d - s) / w > 0.4 or e - d < 5: return None
    ref60 = np.nanmedian(ar[max(0, s - 60):s])
    med = np.nanmedian(ar[s:e + 1])
    if not (ref60 > 0 and med <= 0.9 * ref60): return None                       # kucuk mum (yakin gecmise gore)
    if (H[s:e + 1].max() - L[s:e + 1].min()) / C[e] * 100 > 5 * med: return None  # dar pencere
    dip = L[d]
    if L[d + 1:e + 1].min() < dip * (1 - 0.5 * ref60 / 100): return None          # yeni dip yok
    y = L[d:e + 1] / dip - 1
    x = np.linspace(0, 1, len(y)); a, b, _ = np.polyfit(x, y, 2); son = 2 * a + b
    k = max(2, len(y) // 3)
    yuv = (a > 0 and son > 0) or (np.median(y[-k:]) > np.median(y[k:2 * k]) > 0)
    if not yuv: return None
    return dict(s=s, e=e, d=d, w=w, med=round(med, 2), ref60=round(ref60, 2), a=round(a * 100, 2), son=round(son * 100, 2))


bul = []
for e in range(70, n):
    for w in range(10, 26):
        s = e - w + 1
        r = obek(s, e)
        if r: bul.append(r)
# ortusenlerden en uzun
bul.sort(key=lambda r: -r['w'])
kal = []
for r in bul:
    if all(r['e'] < q['s'] or r['s'] > q['e'] for q in kal): kal.append(r)
kal.sort(key=lambda r: r['s'])
ix = df.index
a0, a1 = int(ix.searchsorted(pd.Timestamp(BAS))), int(ix.searchsorted(pd.Timestamp(SON), side='right')) - 1
sec = [r for r in kal if r['e'] >= a0 and r['s'] <= a1]
print(f"{SEM}: toplam {len(kal)} obek, {BAS}-{SON} araliginda {len(sec)}")
for r in sec:
    print(f"  {ix[r['s']].date()} -> {ix[r['e']].date()} ({r['w']} bar) dip {ix[r['d']].date()} aralik {r['med']}% (ref60 {r['ref60']}%) parabol a {r['a']} son_egim {r['son']}")
fig, ax = plt.subplots(figsize=(11, 4.2))
xs = np.arange(a0, a1 + 1)
ax.vlines(xs, L[a0:a1 + 1], H[a0:a1 + 1], color='#888', lw=0.6)
ax.vlines(xs, np.minimum(O, C)[a0:a1 + 1], np.maximum(O, C)[a0:a1 + 1], color=np.where(C[a0:a1 + 1] >= O[a0:a1 + 1], '#2a9d8f', '#c0392b'), lw=1.8)
ax.plot(xs, df.Close.rolling(20).mean().to_numpy()[a0:a1 + 1], color='#e9a23b', lw=0.9, label='SMA20')
ax.plot(xs, df.Close.rolling(50).mean().to_numpy()[a0:a1 + 1], color='#6c5ce7', lw=0.9, label='SMA50')
for i, r in enumerate(sec):
    lo, hi = L[r['s']:r['e'] + 1].min(), H[r['s']:r['e'] + 1].max()
    ax.add_patch(Rectangle((r['s'] - .5, lo), r['w'], hi - lo, fill=True, fc='#2ecc71', alpha=.18, ec='#1e8449', lw=1.5, label='yuvarlanma obegi (kod)' if i == 0 else None))
    ax.plot([r['d']], [L[r['d']]], marker='v', color='#1e8449', ms=7)
ax2 = ax.twinx(); ax2.bar(xs, V[a0:a1 + 1], color='#bbb', alpha=.35, width=1); ax2.set_ylim(0, np.nanmax(V[a0:a1 + 1]) * 4); ax2.axis('off')
tk = np.linspace(a0, a1, 8).astype(int); ax.set_xticks(tk); ax.set_xticklabels([f"{ix[i]:%d.%m.%y}" for i in tk], fontsize=7)
ax.set_title(f"Yuvarlanma obegi denemesi — {BAS} / {SON} — kodun buldugu {len(sec)} obek (yesil), dip = ucgen", fontsize=9)
ax.legend(fontsize=7, loc='upper left'); fig.tight_layout(); fig.savefig(PNG, dpi=110); print('PNG', PNG)
