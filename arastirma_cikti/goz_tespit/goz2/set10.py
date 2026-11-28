# GT10 kör onay seti: K3 (C adayına göre tabakalı 16) + yalnız C 4 + rastgele 4; dört kutu (denetim aracı; çizim GOZ_TESPIT.gt_pdf).
import sys, os, json, pandas as pd
sys.path.insert(0, '/home/user/col_yolu'); import logging; logging.disable(logging.INFO)
import MUM_IZI as MI, GOZ_TESPIT as GT
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.dirname(D)
J = json.load(open(os.path.join(D, 'gt10_secim.json'), encoding='utf-8')); S = sorted(J['sayfalar'], key=lambda r: r['sayfa']); Vc = {}; sira = list(S)
def veri(r):
    if r['pazar'] not in Vc: Vc[r['pazar']] = MI.mi_veri(r['pazar'], GT.GT_YOL['acik'])['V']
    d = Vc[r['pazar']][r['sembol']]; assert d.index[int(r['t'])] <= pd.Timestamp('2022-12-31'); return d
def seri(p, sem, kaynak):
    r = sira.pop(0); assert (r['pazar'], r['sembol']) == (p, sem); return veri(r)
KUTU = ['✓  çöl', 'K  kısmen', 'E  erken', '×  değil']
kapak = (f"Bu sette {len(S)} bölge var.\n\nÇoğu geçen setle aynı kuralla seçildi: senin eski kodun + yer şartı (düşüş sonrası grafiğin altında ince şerit) + zaman şartı "
         "(bölgenin en derin dibi ilk yarıda). Geçen sette bu kural senin gözünü yeterince tutmadı (15 sayfada 6 ✓). Bu yüzden bu sette, beş setteki işaretlerinden çıkan yeni bir aday ölçü de sınanıyor "
         "(dört şeye bakıyor: en büyük mumun boyu, kutunun inceliği, kapanışların kutunun alt yarısında kalması, en derin dibin eskide kalması): bölgelerin bir kısmı ondan da geçiyor, "
         "bir kısmı geçmiyor, birkaçı yalnız onunla seçildi. Birkaç gelişigüzel bölge de var. Hangisi olduğu yazmıyor.\n\nSoru tek: bu bölge senin çöl dediğin şey mi?\n\n"
         "✓ çöl\nK kısmen\nE erken: yer doğru ama henüz yuvarlanmadı\n× değil\n\nHer sayfada bir kutu işaretle (geçen sette 1. sayfa boş kalmıştı).\n\nSonrası gösterilmiyor. Hisse adı ve tarih yok.")
y = os.path.join(C, 'GT10_ONAY.pdf'); assert not os.path.exists(y)
P = GT.gt_pdf(y, S, seri, kapak=kapak, kutu=KUTU); GT.gt_pdf_denetim(y, [r['sembol'] for r in S])
for r in S: r['son'] = str(veri(r).index[int(r['t'])].date())
json.dump(dict(not_='MÜHÜRLÜ: sayfa -> kol / hisse / bölge; işaretler gelmeden açılmaz', pdf='GT10_ONAY.pdf', pdf_sha=P['sha'], kutu=KUTU, kural=J['kural'], say={k: sum(r['kol'] == k for r in S) for k in sorted({r['kol'] for r in S})}, sayfalar=S),
          open(os.path.join(C, 'GT10_onay_anahtar.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=int)
print('pdf', P['sha'][:12], len(S))
