# Üç işaretli set (GT1, GT3, GT4): Cemal'in dört sınıflı işaretleri + sayfa başına ölçüler tek tabloda. Denetim / öğrenme aracı (getiri yok).
import sys, os, json, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/col_yolu'); import logging; logging.disable(logging.INFO)
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(D); sys.path.insert(0, D)
import MUM_IZI as MI, GOZ_TESPIT as GT
from cetvel import goz_olcu
from k2 import k2
from parabol import dip_parabol
VV = {}
def veri(p, kaynak):
    if (p, kaynak) not in VV: VV[(p, kaynak)] = MI.mi_veri(p, GT.GT_YOL['tam_bist'] if kaynak == 'tam' else GT.GT_YOL['acik'])['V']
    return VV[(p, kaynak)]
def olc(d, s, t):
    O, H, L, Cc = (d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close')); o = dict(goz_olcu(O, H, L, Cc, s, t)); o.update({k: v for k, v in k2(O, H, L, Cc, s, t).items()})
    Hb, Lb, Cb = H[s:t + 1], L[s:t + 1], Cc[s:t + 1]; n = len(Cb); kutu = Hb.max() - Lb.min(); y = n // 2; i0 = max(0, s - 120)
    o['DIP_KAYMA'] = (Lb[y:].min() - Lb[:y].min()) / kutu; o['DIPTEN_BAR'] = (n - 1 - int(np.argmin(Lb))) / n
    o['SON10_EGIM'] = float(np.polyfit(np.arange(10), Cb[-10:], 1)[0] * 9 / kutu); o['YARI_ORT'] = float(Cb[y:].mean() / Cb[:y].mean() - 1); o['IC'] = float(Cb[-1] / Cb[0] - 1)
    o['SON_DIP'] = float((Lb[-max(3, n // 5):].min() - Lb.min()) / kutu); o['TABAN_YASI'] = t - (i0 + int(np.argmin(L[i0:t + 1]))); o['DUSUS_SONU'] = t - (i0 + int(np.argmax(H[i0:t + 1])))
    o['ONCE_DUZ'] = float((H[max(i0, s - 30):s].max() - L[max(i0, s - 30):s].min()) / kutu) if s - i0 >= 30 else np.nan; o['BAR'] = n
    p = dip_parabol(H, L, s, t); o['P_A'] = p['a']; o['P_YUK'] = p['yukselis']; o['P_SONEGIM'] = p['son_egim']
    o['SON5_YER'] = float((Cb[-5:].mean() - Lb.min()) / kutu); o['UST_YARI'] = float((Cb > Lb.min() + 0.5 * kutu).mean())   # son 5 kapanışın kutudaki yeri; kapanışların üst yarıda geçen payı
    return o
def tablo():
    KT = {r['no']: r for r in json.load(open('/root/.kasa/ham/goz_tespit/kitaplik_olcu.json', encoding='utf-8')) if r['durum'] == 'tamam'}; R = []
    setler = [('GT1', 'GT_onay_anahtar.json', 'cemal_gt_onay.json'), ('GT3', 'GT3_onay_anahtar.json', 'cemal_gt3_onay.json'), ('GT4', 'GT4_onay_anahtar.json', 'cemal_gt4_onay.json')]
    for ad, anahtar, isaret in setler:
        A = json.load(open(os.path.join(C, anahtar), encoding='utf-8'))['sayfalar']; S4 = json.load(open(os.path.join(C, isaret), encoding='utf-8'))['sinif4']
        for r in A:
            d = veri(r['pazar'], r.get('kaynak', 'acik'))[r['sembol']]
            if r.get('kaynak') == 'tam': d = d[d.index <= pd.Timestamp(KT[r['kitaplik_no']]['bit'])]
            R.append(dict(set=ad, sayfa=r['sayfa'], kol=r['kol'], pazar=r['pazar'], cemal=S4[str(r['sayfa'])], **olc(d, int(r['s']), int(r['t']))))
    return pd.DataFrame(R)
def auc(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    return float(((a[:, None] > b[None, :]).sum() + 0.5 * (a[:, None] == b[None, :]).sum()) / (len(a) * len(b))) if len(a) and len(b) else np.nan
