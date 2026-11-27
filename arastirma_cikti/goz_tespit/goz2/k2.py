# ÇÖL-K2 (Cemal, 27 Kas 2026: 'parabolik dip zamanı verir; yalnız başına filtre değil; küçük mum, dip savunması, daha derin diplerin bittiğinin teyidi birlikte olunca önemli').
# Beş şart: Y yer (K1), M küçük mum, S dip savunması, B derin dip bitti, Z zaman (dip parabolü). Denetim aracı; yalnız bölge sonuna kadar.
import sys, os, json, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/col_yolu'); import logging; logging.disable(logging.INFO)
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(D); sys.path.insert(0, D)
from cetvel import goz_olcu
from parabol import dip_parabol, dip_parabol_var
K2 = dict(Y=dict(KUTU_ORAN=0.22, KUTU_YER=0.35, TEPE_KAT=2.0), M=dict(BOY_ORAN=0.80, GOV_ORAN=0.80), S=dict(taban_pay=0.25, ayri_bar=3, dokunus=3, yayilim=0.25), B=dict(dipten_bar=5, once=20),
          Z=json.load(open(os.path.join(D, 'dip_parabol_kural.json'))))
def k2(O, H, L, C, s, t):
    o = goz_olcu(O, H, L, C, s, t)
    if not o: return None
    Hb, Lb = H[s:t + 1], L[s:t + 1]; n = len(Lb); dip = float(Lb.min()); kutu = float(Hb.max() - dip)
    y = o['KUTU_ORAN'] <= K2['Y']['KUTU_ORAN'] and o['KUTU_YER'] <= K2['Y']['KUTU_YER'] and o['TEPE_KAT'] >= K2['Y']['TEPE_KAT']
    m = o['BOY_ORAN'] <= K2['M']['BOY_ORAN'] and o['GOV_ORAN'] <= K2['M']['GOV_ORAN']
    idx = np.where(Lb <= dip + K2['S']['taban_pay'] * kutu)[0]; ay = []                      # taban bölgesine dokunan barlar; ayrı dokunuş = aralarında >= 3 bar
    for i in idx:
        if not ay or i - ay[-1] >= K2['S']['ayri_bar']: ay.append(int(i))
    sv = len(ay) >= K2['S']['dokunus'] and (ay[-1] - ay[0]) >= K2['S']['yayilim'] * n
    i0 = max(0, s - K2['B']['once']); b = (t - (i0 + int(np.argmin(L[i0:t + 1])))) >= K2['B']['dipten_bar']   # bölge + önceki 20 barın en derin dibi en az 5 bar geride
    z = dip_parabol_var(dip_parabol(H, L, s, t, K2['Z']), K2['Z'])
    return dict(Y=int(y), M=int(m), S=int(sv), B=int(b), Z=int(z), dokunus=len(ay), K2=int(y and m and sv and b and z), YMSB=int(y and m and sv and b))
if __name__ == '__main__':
    import MUM_IZI as MI, GOZ_TESPIT as GT
    VV = {}
    def veri(p, kaynak):
        if (p, kaynak) not in VV: VV[(p, kaynak)] = MI.mi_veri(p, GT.GT_YOL['tam_bist'] if kaynak == 'tam' else GT.GT_YOL['acik'])['V']
        return VV[(p, kaynak)]
    def hes(r, bit=None):
        d = veri(r['pazar'], r.get('kaynak', 'acik'))[r['sembol']]
        if bit: d = d[d.index <= pd.Timestamp(bit)]
        return k2(*(d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close')), int(r['s']), int(r['t']))
    pd.set_option('display.width', 220)
    # ilk set (Cemal'in işaretleri)
    C1 = json.load(open(os.path.join(C, 'cemal_gt_onay.json'), encoding='utf-8')); KT = {r['no']: r for r in json.load(open('/root/.kasa/ham/goz_tespit/kitaplik_olcu.json', encoding='utf-8')) if r['durum'] == 'tamam'}
    T1 = pd.DataFrame([dict(sayfa=r['sayfa'], kol=r['kol'], cemal=C1['sinif4'][str(r['sayfa'])], **hes(r, KT[r['kitaplik_no']]['bit'] if r['kaynak'] == 'tam' else None)) for r in json.load(open(os.path.join(C, 'GT_onay_anahtar.json'), encoding='utf-8'))['sayfalar']])
    Dd = T1[T1.kol != 'RASTGELE']; print('İLK SET (Cemal; rastgele hariç 24): şart başına sağlayan sayfa sayısı'); print(Dd.groupby('cemal')[['Y', 'M', 'S', 'B', 'Z', 'YMSB', 'K2']].sum().assign(n=Dd.groupby('cemal').size()).to_string())
    print('rastgele 6:', T1[T1.kol == 'RASTGELE'][['Y', 'M', 'S', 'B', 'Z']].sum().to_dict())
    # GT4 (ana modelin yargısı) ve GT3
    A4 = json.load(open(os.path.join(D, 'dip_anahtar.json'), encoding='utf-8')); Y4 = {n: k for k, v in json.load(open(os.path.join(D, 'dip_goz_yargi.json'), encoding='utf-8'))['etiket'].items() for n in v}
    T4 = pd.DataFrame([dict(sayfa=r['no'], kol=r['kol'], goz=Y4[r['no']], **hes(r)) for r in A4]); G = T4[T4.kol == 'K1+DIP']
    print('\nGT4 (16 sayfa; ana modelin yargısı): şart başına'); print(G.groupby('goz')[['Y', 'M', 'S', 'B', 'Z', 'K2']].sum().assign(n=G.groupby('goz').size()).to_string()); print('GT4: beş şartın beşi:', int(G.K2.sum()), '/ 16 | sayfalar:', G[G.K2 == 1].sayfa.tolist())
    J3 = json.load(open(os.path.join(D, 'gt3_secim.json'), encoding='utf-8')); Y3 = {n: k for k, v in json.load(open(os.path.join(D, 'gt3_goz_yargi.json'), encoding='utf-8'))['etiket'].items() for n in v}
    T3 = pd.DataFrame([dict(sayfa=r['sayfa'], kol=r['kol'], goz=Y3[r['sayfa']], **hes(r, J3['kit_bit'][str(r['kitaplik_no'])] if r['kaynak'] == 'tam' else None)) for r in J3['sayfalar']]); G3 = T3[T3.kol == 'D1']
    print('\nGT3 D1 (24 sayfa; ana modelin ön etiketi): şart başına'); print(G3.groupby('goz')[['Y', 'M', 'S', 'B', 'Z', 'YMSB', 'K2']].sum().assign(n=G3.groupby('goz').size()).to_string())
    json.dump(dict(kural=K2, not_="ÖN KAYIT (Cemal'in GT3 / GT4 işaretlerinden önce): sayfa başına beş şart", GT4=T4.to_dict('records'), GT3=T3.to_dict('records')), open(os.path.join(D, 'k2_onkayit.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # havuz sıklığı
    for p in ('BIST', 'ABD'):
        V = veri(p, 'acik'); P = pickle.load(open(f'/root/.kasa/ham/goz_tespit/pencere_{p}.pkl', 'rb')); P['tarih'] = pd.to_datetime(P['tarih'])
        Hv = P[(P.tarih >= '2016-01-01') & (P.tarih <= '2022-12-31') & (P.s >= 120) & (P.KIL <= 0.20) & (P.govdesiz_pay <= 0.30)][['sembol', 's', 't', 'ZIRVE_DUSUS']]; F = Hv[Hv.ZIRVE_DUSUS <= -0.5]; S_ = np.zeros(7, int); his = set()
        for sem, g in F.groupby('sembol'):
            d = V[sem]; O, H, L, Cc = (d[c].to_numpy(float) for c in ('Open', 'High', 'Low', 'Close'))
            for s, t in zip(g.s.values, g.t.values):
                o = k2(O, H, L, Cc, int(s), int(t))
                if o and o['Y']:
                    S_ += np.array([1, o['M'], o['M'] and o['S'], o['M'] and o['S'] and o['B'], o['K2'], o['Z'], o['M'] and o['B'] and o['Z']], int)
                    if o['K2']: his.add(sem)
        print(f"{p}: havuz {len(Hv)} | Y {S_[0]} | Y+M {S_[1]} | Y+M+S {S_[2]} | Y+M+S+B {S_[3]} | beşi (K2) {S_[4]} (havuzun %{100 * S_[4] / len(Hv):.3f}; {len(his)} hisse) | Y+Z {S_[5]} | Y+M+B+Z (savunmasız) {S_[6]}")
