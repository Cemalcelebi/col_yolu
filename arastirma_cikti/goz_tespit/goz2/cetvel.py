# Göz cetveli: gözün uzak görünümde gördüğü geometri (yalnız bölge sonuna kadar). Denetim aracı.
import numpy as np
def goz_olcu(O, H, L, C, s, t, uzak=120):
    """O,H,L,C: tam seri (t dahil kesik de olabilir); bölge [s, t]; uzak görünüm = önceki `uzak` bar + bölge."""
    iu = max(0, s - uzak); Hb, Lb, Cb, Ob = H[s:t + 1], L[s:t + 1], C[s:t + 1], O[s:t + 1]; Ho, Lo = H[iu:s], L[iu:s]
    if len(Ho) < 40: return None
    ust = float(Hb.max()); alt = float(Lb.min()); kutu = ust - alt
    gust = float(max(Ho.max(), ust)); galt = float(min(Lo.min(), alt)); ga = gust - galt
    boyb = np.median(Hb - Lb); boyo = np.median((H[iu:s] - L[iu:s]))
    govb = np.median(np.abs(Cb - Ob)); govo = np.median(np.abs(C[iu:s] - O[iu:s]))
    n = len(Cb); x = np.arange(n); egim = np.polyfit(x, Cb, 1)[0] * (n - 1) / kutu if kutu > 0 and n > 2 else np.nan
    ipk = int(np.argmax(Ho)); dip_once = float(Lo[ipk:].min()) if ipk < len(Lo) else alt
    return dict(
        KUTU_ORAN=kutu / ga if ga > 0 else np.nan,                 # kutu yüksekliği / uzak görünüm yüksekliği
        KUTU_YER=((ust + alt) / 2 - galt) / ga if ga > 0 else np.nan,  # kutunun uzak görünümdeki yeri (0 = dip, 1 = tepe)
        TEPE_KAT=float(Ho.max()) / ust,                              # önceki tepe / kutu tavanı
        DUSUS=alt / float(Ho.max()) - 1,                             # önceki tepeden kutu dibine
        TEPE_UZAK=len(Ho) - ipk,                                     # tepe bölge başından kaç bar önce
        ONCE_DIP=dip_once / alt - 1,                                 # tepe ile bölge arasındaki en düşük, kutu dibine göre (eksi = bölgeden önce daha dip görülmüş)
        EGIM=float(egim),                                            # bölge içi kapanış eğimi, kutu yüksekliği biriminde
        SON_YER=(Cb[-1] - alt) / kutu if kutu > 0 else np.nan,       # son kapanışın kutudaki yeri
        BOY_ORAN=boyb / boyo if boyo > 0 else np.nan,                # mum boyu (fiyat) / önceki mum boyu
        GOV_ORAN=govb / govo if govo > 0 else np.nan,
        EN_BUYUK=float((Hb - Lb).max() / kutu) if kutu > 0 else np.nan,  # bölgedeki en büyük mum / kutu
        KUTU_YUZDE=kutu / alt)                                       # kutu yüksekliği, yüzde
