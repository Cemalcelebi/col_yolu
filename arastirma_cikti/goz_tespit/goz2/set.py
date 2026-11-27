# GT2 kör onay seti: ana modelin göz kapısından geçen sayfalar + kısmen + rastgele + kitaplık (denetim aracı; sayfa çizimi GOZ_TESPIT.gt_pdf).
import sys, os, json, hashlib, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/col_yolu'); import logging; logging.disable(logging.INFO)
import MUM_IZI as MI, GOZ_TESPIT as GT
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(D)
A = {r['no']: r for r in json.load(open(os.path.join(D, 'levha_anahtar.json')))}
Y = json.load(open(os.path.join(D, 'goz_yargi.json'), encoding='utf-8'))
KT = {r['no']: r for r in json.load(open('/root/.kasa/ham/goz_tespit/kitaplik_olcu.json', encoding='utf-8')) if r['durum'] == 'tamam'}
rng = np.random.default_rng(2717)
E = list(Y['EVET']); K = [27, 54, 47]
R = sorted(rng.choice([n for n, r in A.items() if r['kol'] == 'RASTGELE'], 5, replace=False).tolist())
KIT = [(1, 'NET'), (5, 'NET'), (3, 'KARISIK'), (19, 'KARISIK')]
S = [dict(kol='GOZ_EVET', hucre=n, **{k: A[n][k] for k in ('pazar', 'sembol', 's', 't', 'L', 'son')}, kaynak='acik') for n in E]
S += [dict(kol='GOZ_KISMEN', hucre=n, neden=Y['KISMEN'][str(n)], **{k: A[n][k] for k in ('pazar', 'sembol', 's', 't', 'L', 'son')}, kaynak='acik') for n in K]
S += [dict(kol='RASTGELE', hucre=n, **{k: A[n][k] for k in ('pazar', 'sembol', 's', 't', 'L', 'son')}, kaynak='acik') for n in R]
S += [dict(kol='KITAPLIK_' + tip, kitaplik_no=no, pazar='BIST', sembol=KT[no]['sembol'], s=int(KT[no]['s']), t=int(KT[no]['t']), L=int(KT[no]['bar']), son=KT[no]['son'], kaynak='tam') for no, tip in KIT]
for i, j in enumerate(rng.permutation(len(S))): S[j]['sayfa'] = i + 1
S.sort(key=lambda r: r['sayfa']); Vc = {}; sira = list(S)
def seri(p, sem, kaynak):
    r = sira.pop(0); assert (r['pazar'], r['sembol'], r['kaynak']) == (p, sem, kaynak)
    if (p, kaynak) not in Vc: Vc[(p, kaynak)] = MI.mi_veri(p, GT.GT_YOL['tam_bist'] if kaynak == 'tam' else GT.GT_YOL['acik'])['V']
    d = Vc[(p, kaynak)][sem]
    if kaynak == 'tam': d = d[d.index <= pd.Timestamp(KT[r['kitaplik_no']]['bit'])]
    else: assert d.index[int(r['t'])] <= pd.Timestamp('2022-12-31')
    assert str(d.index[int(r['t'])].date()) == r['son'], (r['sayfa'], 'tarih')
    return d
kapak = (f"Bu sette {len(S)} bölge var.\n\nKod aday buldu; ben her adaya tek tek kendi gözümle baktım. Bu sette: benim 'çöl' dediklerim, birkaç 'kısmen' dediğim, "
         "birkaç gelişigüzel seçilmiş bölge ve senin kendi çöllerinden birkaçı karışık duruyor. Hangisi olduğu yazmıyor.\n\n"
         "Soru tek: bu bölge senin çöl dediğin şey mi?\n\n✓ çöl      K kısmen      × değil\n\nSonrası gösterilmiyor. Hisse adı ve tarih yok.")
y = os.path.join(C, 'GT2_ONAY.pdf'); assert not os.path.exists(y)
P = GT.gt_pdf(y, S, seri, kapak=kapak); GT.gt_pdf_denetim(y, [r['sembol'] for r in S])
J = dict(not_='MÜHÜRLÜ: sayfa -> kol / hisse / bölge; işaretler gelmeden açılmaz', tohum=2717, pdf='GT2_ONAY.pdf', pdf_sha=P['sha'], goz_yargi_sha=hashlib.sha256(open(os.path.join(D, 'goz_yargi.json'), 'rb').read()).hexdigest(),
         say={k: sum(r['kol'] == k for r in S) for k in sorted({r['kol'] for r in S})}, sayfalar=S)
json.dump(J, open(os.path.join(C, 'GT2_onay_anahtar.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=int)
print(J['say'], len(S), P['sha'][:12], 'pazar', {p: sum(r['pazar'] == p for r in S) for p in ('BIST', 'ABD')})
