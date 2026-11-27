# YUVARLANMA = PARABOL (Cemal, 27 Kas 2026: 'son bölümdeki mumların oluşturduğu çizgi yukarı doğru bir parabol olmalı'). Denetim aracı; yalnız bölge sonuna kadar.
import numpy as np
def parabol(H, L, C, s, t, bolum='yari'):
    """Bölgenin son bölümündeki mum ortalarına (H + L + C) / 3 ikinci derece eğri. x: -1 (bölüm başı) .. +1 (bölge sonu); y: bölüm aralığına bölünmüş.
    Dönüş: a (kavis; > 0 = yukarı açılan), tepe_x (eğrinin dibi: -1..+1 içinde ise dip bölümde), son_egim (bölge sonundaki eğim), yukselis (dipten sona eğri yükselişi, bölüm aralığı biriminde), r2."""
    n_b = t - s + 1; n = {'yari': max(10, n_b // 2), 'ucte': max(10, n_b // 3), 'son20': 20, 'tum': n_b}[bolum]; n = min(n, n_b)
    i0 = t - n + 1; y = (H[i0:t + 1] + L[i0:t + 1] + C[i0:t + 1]) / 3.0; ar = float(H[i0:t + 1].max() - L[i0:t + 1].min())
    if n < 8 or ar <= 0: return None
    x = np.linspace(-1.0, 1.0, n); yn = (y - y.mean()) / ar; a, b, c = np.polyfit(x, yn, 2); f = a * x * x + b * x + c
    ss = float(((yn - yn.mean()) ** 2).sum()); r2 = 1.0 - float(((yn - f) ** 2).sum()) / ss if ss > 0 else 0.0
    tx = -b / (2 * a) if abs(a) > 1e-12 else np.nan; dx = float(np.clip(tx, -1, 1)) if np.isfinite(tx) else 1.0
    yuk = float((a + b + c) - (a * dx * dx + b * dx + c)) if a > 0 else 0.0
    return dict(a=float(a), tepe_x=float(tx), son_egim=float(2 * a + b), yukselis=yuk, r2=r2, n=n)
PARABOL_KURAL = dict(bolum='yari', a=0.0, son_egim=0.0, tepe_x=(-1.0, 0.6), yukselis=0.10)
def parabol_var(p, K=PARABOL_KURAL):
    """Yukarı açılan parabol: kavis > 0, bölge sonunda eğim yukarı, eğrinin dibi son bölümün içinde (en sonda değil), dipten sona en az bölüm aralığının %10'u kadar yükseliş."""
    return bool(p and p['a'] > K['a'] and p['son_egim'] > K['son_egim'] and K['tepe_x'][0] <= p['tepe_x'] <= K['tepe_x'][1] and p['yukselis'] >= K['yukselis'])


# ---- v2 (Cemal, 27 Kas 2026, düzeltme): 'bu, mumların DİPLERİNİ birleştiren çizgi olmalı; daha derin dipler olmaması gerekir; üstte bir yukarı bir aşağı olabilir'.
DIP_PARABOL_KURAL = dict(bolum_pay=3, bolum_en_az=10, tepe_x=(-1.0, 0.5), son_bar=3, yuksek_dip=0.05, r2=0.40, yukselis=0.15)
def dip_parabol(H, L, s, t, K=DIP_PARABOL_KURAL):
    """Bölgenin son bölümündeki mum DİPLERİNE ikinci derece eğri. Yalnız Low kullanılır (High yalnız bölüm aralığı için)."""
    n_b = t - s + 1; n = min(n_b, max(int(K['bolum_en_az']), n_b // int(K['bolum_pay']))); i0 = t - n + 1
    Ls = L[i0:t + 1]; ar = float(H[i0:t + 1].max() - Ls.min())
    if n < 8 or ar <= 0: return None
    x = np.linspace(-1.0, 1.0, n); yn = (Ls - Ls.mean()) / ar; a, b, c = np.polyfit(x, yn, 2); f = a * x * x + b * x + c
    ss = float(((yn - yn.mean()) ** 2).sum()); r2 = 1.0 - float(((yn - f) ** 2).sum()) / ss if ss > 0 else 0.0
    tx = -b / (2 * a) if abs(a) > 1e-12 else np.nan; dx = float(np.clip(tx, -1, 1)) if np.isfinite(tx) else 1.0
    yuk = float((a + b + c) - (a * dx * dx + b * dx + c)) if a > 0 else 0.0; k3 = max(3, n // 3)
    return dict(a=float(a), tepe_x=float(tx), son_egim=float(2 * a + b), yukselis=yuk, r2=r2, n=n, dip_yer=int(np.argmin(Ls)),
                son_dip=float((Ls[-int(K['son_bar']):].min() - Ls.min()) / ar), son_ucte_dip=float((Ls[-k3:].min() - Ls.min()) / ar))
def dip_parabol_var(p, K=DIP_PARABOL_KURAL):
    """Dipler yukarı açılan parabol çiziyor: kavis > 0; sonda dip çizgisi yükseliyor; eğrinin dibi bölümün içinde (sonda değil); en derin dip son 3 mumda değil;
    bölümün son üçte birindeki en düşük dip, bölümün en derin dibinden yukarıda (daha derin dip yok, dipler yükseliyor); uyum ve yükseliş eşikleri."""
    return bool(p and p['a'] > 0 and p['son_egim'] > 0 and K['tepe_x'][0] <= p['tepe_x'] <= K['tepe_x'][1] and p['son_dip'] > 0 and p['son_ucte_dip'] >= K['yuksek_dip']
                and p['r2'] >= K['r2'] and p['yukselis'] >= K['yukselis'])
