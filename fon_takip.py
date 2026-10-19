# =====================================================================
#  FON TAKIP — fonoloji.com API (2026-09-13)
#  BULGU: fonun ILK KEZ girdigi hisse, sonraki 3 ayda medyan +%11.9,
#         %69 kazanan. Diger tum hisse-ay kayitlari: -%1.3.  (n=90, 9 ay)
#  Agirlik artisi/azalisi ANLAMSIZ (0 civari). Sadece ILK GIRIS onemli.
#  UYARI: veri aylik ve ~1.5 ay gecikmeli. Tek donem (2025-10..2026-08).
#         2 donemde dogrulanmadi — CDS/borc gibi kural degil, IZLEME LISTESI.
#  Kullanim: ayda bir  F,yeni = fon_guncelle()   -> yeni girenler listesi
# =====================================================================
import requests, pandas as pd, numpy as np, time, os
_K='/content/drive/MyDrive/col_tarayici'
FONLAR=['THF','TLY','PHE','AFT','IPJ','TTE','IYB','AK3','TI2','MAC','TCD','NNF','BGP','AFA',
        'GTZ','YAY','ODV','HVT','TGE','IJH','AES','YZG','DLY','HPT','GA1','DBB','OJT','IST','TMG','FYD']

def _sess():
    s=requests.Session()
    s.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36',
                      'Accept':'application/json','Accept-Language':'tr-TR,tr;q=0.9'})
    return s

def fon_cek(kod, s=None):
    s=s or _sess()
    try:
        s.headers['Referer']=f'https://fonoloji.com/fon/{kod}'
        s.get(f"https://fonoloji.com/fon/{kod}",timeout=20)
        r=s.get(f"https://fonoloji.com/api/funds/{kod}/holdings",timeout=30)
        if r.status_code!=200: return []
        j=r.json()
        return [{'fon':kod,'donem':it.get('report_date'),'sembol':it['asset_code'],
                 'agirlik':it.get('weight'),'mv':it.get('market_value')}
                for it in j.get('holdings',[])
                if it.get('asset_type')=='stock' and it.get('asset_code')]
    except Exception: return []

def fon_guncelle(fonlar=None, kaydet=True, sessiz=False):
    s=_sess(); R=[]
    for f in (fonlar or FONLAR):
        h=fon_cek(f,s); R+=h
        if h and not sessiz: print(f"  {f}: {len(h)}")
        time.sleep(0.5)
    H=pd.DataFrame(R)
    H=H[H.donem.notna() & (H.donem.str.len()==7)].copy()
    if kaydet:
        y=f'{_K}/fon_holdings.csv'
        if os.path.exists(y):
            eski=pd.read_csv(y); H=pd.concat([eski,H]).drop_duplicates(['fon','donem','sembol'],keep='last')
        H.to_csv(y,index=False)
    H['ay']=pd.PeriodIndex(H.donem,freq='M')
    G=H.groupby(['sembol','ay']).agg(fon_say=('fon','nunique'),top_ag=('agirlik','sum')).reset_index().sort_values(['sembol','ay'])
    G['onceki']=G.groupby('sembol').fon_say.shift()
    ilk_ay=G.ay.min()
    G['yeni']=(G.onceki.isna())&(G.ay>ilk_ay+1)          # veri basi yanlisligi temizlendi
    son=G.ay.max()
    yeni=G[(G.ay==son)&G.yeni].merge(H[H.ay==son].groupby('sembol').fon.apply(lambda v:','.join(v)).rename('fonlar'),on='sembol',how='left')
    print(f"\n  {len(H)} kayit | {H.sembol.nunique()} hisse | {H.fon.nunique()} fon | donem {H.ay.min()} -> {son}")
    print(f"\n  === {son} DONEMINDE FONUN ILK KEZ GIRDIGI HISSELER ===")
    print("  (gecmiste bu grup 3 ayda medyan +%11.9, %69 kazanan)\n")
    if len(yeni): print(yeni[['sembol','fon_say','top_ag','fonlar']].sort_values('top_ag',ascending=False).to_string(index=False))
    else: print("  yok")
    return H, yeni

def fon_col_kesisim(yeni, veri=None):
    """yeni giren fon hisseleri ile bugunun col adaylarini kesistir"""
    veri=veri if veri is not None else VERI
    import os
    A=pd.read_csv(f'{_K}/takip_adaylar.csv') if os.path.exists(f'{_K}/takip_adaylar.csv') else pd.DataFrame(columns=['sembol'])
    P=pd.read_csv(f'{_K}/takip_pozisyonlar.csv') if os.path.exists(f'{_K}/takip_pozisyonlar.csv') else pd.DataFrame(columns=['sembol'])
    col=set(A.sembol)|set(P.sembol)
    k=[s for s in yeni.sembol if s in col]
    print(f"\n  COL LISTESI x YENI FON GIRISI: {', '.join(k) if k else 'kesisim yok'}")
    return k

print("[ok] fon_takip yuklendi  (AYDA BIR calistir)")
print("  H,yeni = fon_guncelle()")
print("  fon_col_kesisim(yeni)")
