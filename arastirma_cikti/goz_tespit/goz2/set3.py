# GT3 kör onay seti: D1 (COL_SKOR6 PUAN_ESIT üst sıra) 24 yeni sayfa + rastgele 4 + kitaplık 4; dört kutu (denetim aracı; çizim GOZ_TESPIT.gt_pdf).
import sys, os, json, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/col_yolu'); import logging; logging.disable(logging.INFO)
import MUM_IZI as MI, GOZ_TESPIT as GT
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(D); sys.path.insert(0, D)
from levha import levha
asama = sys.argv[1]
KUTU = ['✓  çöl', 'K  kısmen', 'E  erken', '×  değil']
if asama == 'sec':
    A = pickle.load(open('/root/.kasa/ham/goz_tespit/dedektor_aday.pkl', 'rb'))
    KT = {r['no']: r for r in json.load(open('/root/.kasa/ham/goz_tespit/kitaplik_olcu.json', encoding='utf-8')) if r['durum'] == 'tamam'}
    kul = set()
    for f in ('GT_onay_anahtar.json', 'GT2_onay_anahtar.json'):
        kul |= {(r['pazar'], r['sembol']) for r in json.load(open(os.path.join(C, f), encoding='utf-8'))['sayfalar']}
    rng = np.random.default_rng(2718); S = []
    for p in ('BIST', 'ABD'):
        n = 0
        for r in A[p]['D1'].itertuples():
            if (p, r.sembol) in kul: continue
            kul.add((p, r.sembol)); S.append(dict(kol='D1', pazar=p, sembol=r.sembol, s=int(r.s), t=int(r.t), L=int(r.L), d1_sira=int(r.Index) + 1, kaynak='acik')); n += 1
            if n == 12: break
        H = A[p]['havuz']; n = 0
        for j in rng.permutation(len(H)):
            r = H.iloc[int(j)]
            if (p, r.sembol) in kul: continue
            kul.add((p, r.sembol)); S.append(dict(kol='RASTGELE', pazar=p, sembol=r.sembol, s=int(r.s), t=int(r.t), L=int(r.L), kaynak='acik')); n += 1
            if n == 2: break
    S += [dict(kol='KITAPLIK_' + tip, kitaplik_no=no, pazar='BIST', sembol=KT[no]['sembol'], s=int(KT[no]['s']), t=int(KT[no]['t']), L=int(KT[no]['bar']), kaynak='tam') for no, tip in [(1, 'NET'), (5, 'NET'), (3, 'KARISIK'), (19, 'KARISIK')]]
    for i, j in enumerate(rng.permutation(len(S))): S[j]['sayfa'] = i + 1
    S.sort(key=lambda r: r['sayfa']); json.dump(dict(tohum=2718, kit_bit={str(k): KT[k]['bit'] for k in (1, 5, 3, 19)}, sayfalar=S), open(os.path.join(D, 'gt3_secim.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=int)
    print({k: sum(r['kol'] == k for r in S) for k in sorted({r['kol'] for r in S})}, len(S))
J = json.load(open(os.path.join(D, 'gt3_secim.json'), encoding='utf-8')); S = J['sayfalar']; Vc = {}
def veri(r):
    k = (r['pazar'], r['kaynak'])
    if k not in Vc: Vc[k] = MI.mi_veri(r['pazar'], GT.GT_YOL['tam_bist'] if r['kaynak'] == 'tam' else GT.GT_YOL['acik'])['V']
    d = Vc[k][r['sembol']]
    if r['kaynak'] == 'tam': d = d[d.index <= pd.Timestamp(J['kit_bit'][str(r['kitaplik_no'])])]
    else: assert d.index[int(r['t'])] <= pd.Timestamp('2022-12-31')
    return d
if asama in ('sec', 'levha'):
    for b in range(0, len(S), 16):
        levha([(f"#{r['sayfa']}", veri(r).iloc[:int(r['t']) + 1], int(r['s']), int(r['t'])) for r in S[b:b + 16]], os.path.join(D, f'GT3_LEVHA_{b // 16 + 1}.png'))
if asama == 'pdf':
    sira = list(S)
    def seri(p, sem, kaynak):
        r = sira.pop(0); assert (r['pazar'], r['sembol'], r['kaynak']) == (p, sem, kaynak); return veri(r)
    kapak = (f"Bu sette {len(S)} bölge var.\n\nÇoğunu senin eski kodunun puanı seçti (ilk sette gözüne en çok uyan oydu); arada birkaç gelişigüzel bölge ve senin kendi "
             "çöllerinden birkaçı var. Hangisi olduğu yazmıyor.\n\nSoru tek: bu bölge senin çöl dediğin şey mi?\n\n✓ çöl\nK kısmen\nE erken: yer doğru ama henüz yuvarlanmadı\n× değil\n\n"
             "Yazı yazman gerekmez; çizim (U, ok, çizgi) yaparsan onu da okurum.\nSonrası gösterilmiyor. Hisse adı ve tarih yok.")
    y = os.path.join(C, 'GT3_ONAY.pdf'); assert not os.path.exists(y)
    P = GT.gt_pdf(y, S, seri, kapak=kapak, kutu=KUTU); GT.gt_pdf_denetim(y, [r['sembol'] for r in S])
    for r in S: r['son'] = str(veri(r).index[int(r['t'])].date())
    json.dump(dict(not_='MÜHÜRLÜ: sayfa -> kol / hisse / bölge; işaretler gelmeden açılmaz', tohum=J['tohum'], pdf='GT3_ONAY.pdf', pdf_sha=P['sha'], kutu=KUTU,
                   say={k: sum(r['kol'] == k for r in S) for k in sorted({r['kol'] for r in S})}, sayfalar=S), open(os.path.join(C, 'GT3_onay_anahtar.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=int)
    print('pdf', P['sha'][:12], len(S))
