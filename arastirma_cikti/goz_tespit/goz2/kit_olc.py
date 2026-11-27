import sys, json, pandas as pd, numpy as np
sys.path.insert(0, '/home/user/col_yolu')
import logging; logging.disable(logging.INFO)
import MUM_IZI as MI, GOZ_TESPIT as GT
from cetvel import goz_olcu
KT = [r for r in json.load(open('/root/.kasa/ham/goz_tespit/kitaplik_olcu.json', encoding='utf-8')) if r['durum'] == 'tamam']
V = MI.mi_veri('BIST', GT.GT_YOL['tam_bist'])['V']; R = []
for k in KT:
    d = V[k['sembol']]; d = d[d.index <= pd.Timestamp(k['bit'])]
    o = goz_olcu(*(d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close')), k['s'], k['t'])
    R.append(dict(no=f"K{k['no']} {k['sembol']}", bar=k['bar'], **(o or {})))
T = pd.DataFrame(R).set_index('no'); pd.set_option('display.width', 250); print(T.round(2).to_string())
