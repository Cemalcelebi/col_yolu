import sys, json, pandas as pd
sys.path.insert(0, '/home/user/col_yolu')
import logging; logging.disable(logging.INFO)
import MUM_IZI as MI, GOZ_TESPIT as GT
from levha import levha
KT = [r for r in json.load(open('/root/.kasa/ham/goz_tespit/kitaplik_olcu.json', encoding='utf-8')) if r['durum'] == 'tamam']
V = MI.mi_veri('BIST', GT.GT_YOL['tam_bist'])['V']
H = []
for k in KT:
    d = V[k['sembol']]; d = d[d.index <= pd.Timestamp(k['bit'])]
    assert str(d.index[k['t']].date()) == k['son'] and str(d.index[k['s']].date()) == k['ilk'], k['sembol']
    H.append((f"K{k['no']} {k['sembol']}", d, k['s'], k['t']))
levha(H[:8], 'kit1.png'); levha(H[8:], 'kit2.png'); print(len(H))
