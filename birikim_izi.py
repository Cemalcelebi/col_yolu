# -*- coding: utf-8 -*-
"""
BIRIKIM_IZI v1.1  —  AKD'siz "para giriyor mu?" tarayıcısı (BIST, günlük)
=========================================================================
Ne yapar:
  col_tarayici/veri_1d_turkey.pkl önbelleğini okur (indirme yok), isterse son
  eksik günleri yfinance ile YALNIZ BELLEKTE tamamlar (pkl'e dokunmaz), sonra
  KURAL_MOTORU ile her hisseye "birikim izi" puanı verir.

Ne YAPMAZ (dürüst sınır):
  Kimin aldığını göstermez — bu AKD/takas verisidir, OHLCV'de yoktur.
  Buradaki kurallar fiyat+hacimden türetilen VEKİL izlerdir.

Kullanım (Colab):
  from google.colab import drive; drive.mount('/content/drive')
  exec(open('/content/drive/MyDrive/col_tarayici/birikim_izi.py').read())
  sonuc = bi_calistir()                 # tüm evren + ODAK raporu
  sonuc = bi_calistir(odak=['ATATR'])   # istediğin hisseler

Çıktılar (CIKTI klasörü):
  birikim_<tarih>.csv       tüm evren, puana göre sıralı
  birikim_odak_<tarih>.txt  odak hisselerin kural-kural dökümü + son 15 bar
  birikim_izi.log           log
"""

# ──────────────────────────────────────────────────────────────────────────
# 0) ÇAKIŞMA KAPISI — bellekte aynı isimde başka bir şey varsa DUR
# ──────────────────────────────────────────────────────────────────────────
_BI_SURUM = '1.1'
_bi_mevcut = [n for n in list(globals()) if n.startswith('bi_') or n.startswith('BI_')]
if _bi_mevcut and globals().get('_BI_SAHIP') != 'birikim_izi':
    raise RuntimeError(
        f"[ÇAKIŞMA KAPISI] Bellekte 'bi_/BI_' önekli ve bu dosyaya ait olmayan isimler var: "
        f"{_bi_mevcut[:8]} — runtime'ı yeniden başlat ya da o isimleri sil.")
_BI_SAHIP = 'birikim_izi'

import os, sys, time, pickle, logging, datetime as _dt
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional
import numpy as np
import pandas as pd

# ──────────────────────────────────────────────────────────────────────────
# 1) AYARLAR
# ──────────────────────────────────────────────────────────────────────────
BI_AYAR = dict(
    KOK        = '/content/drive/MyDrive/col_tarayici',
    VERI_ADI   = 'veri_1d_turkey.pkl',
    CIKTI_ALT  = 'birikim',
    ODAK       = ['ATATR'],
    TAZELE     = True,     # pkl'in son gününden bugüne yfinance ile BELLEKTE tamamla
    TAZELE_PAKET = 100,    # yfinance toplu indirme paket boyu
    ILK_ATLA   = 10,       # her hissenin ilk 10 barı hiçbir hesaba girmez (halka arz etkisi)
    MIN_BAR    = 40,       # ilk 10 bar atıldıktan sonra en az bu kadar bar
    PIYASA_ESIK = -0.01,   # "zayıf piyasa günü": evren medyan getirisi bunun altı
    TAVAN_ESIK = 0.095,    # BIST tavan ~%10
    DIP_KAPISI = False,    # True: yalnız Fiyat < SMA50 ve < SMA200 olanları listele
    EKRAN_ILK  = 30,
)

# ──────────────────────────────────────────────────────────────────────────
# 2) LOG
# ──────────────────────────────────────────────────────────────────────────
bi_log = logging.getLogger('birikim_izi')

def bi_log_kur(cikti_dizin: str) -> None:
    bi_log.handlers.clear()
    bi_log.setLevel(logging.INFO)
    bi_log.propagate = False
    fmt = logging.Formatter('%(asctime)s | %(levelname)-7s | %(message)s', '%H:%M:%S')
    h1 = logging.StreamHandler(sys.stdout); h1.setFormatter(fmt); bi_log.addHandler(h1)
    try:
        os.makedirs(cikti_dizin, exist_ok=True)
        h2 = logging.FileHandler(os.path.join(cikti_dizin, 'birikim_izi.log'), encoding='utf-8')
        h2.setFormatter(fmt); bi_log.addHandler(h2)
    except OSError as e:
        bi_log.warning(f'Log dosyası açılamadı ({e}); yalnız ekrana yazılıyor.')

# ──────────────────────────────────────────────────────────────────────────
# 3) VERİ OKUMA + NORMALİZE
# ──────────────────────────────────────────────────────────────────────────
_BI_KOLON = {'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume',
             'adj close': 'Adj Close'}

def bi_sembol(s) -> str:
    return str(s).upper().replace('.IS', '').strip()

def bi_df_normalize(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Tek hissenin OHLCV tablosunu standart hale getirir; bozuksa None."""
    if not isinstance(df, pd.DataFrame) or df.empty:
        return None
    d = df.copy()
    if isinstance(d.columns, pd.MultiIndex):          # yfinance group_by artığı
        for lvl in range(d.columns.nlevels):
            if 'Close' in d.columns.get_level_values(lvl) or 'close' in d.columns.get_level_values(lvl):
                d.columns = d.columns.get_level_values(lvl); break
    d.columns = [_BI_KOLON.get(str(c).lower(), c) for c in d.columns]
    gerek = ['Open', 'High', 'Low', 'Close', 'Volume']
    if any(c not in d.columns for c in gerek):
        return None
    d = d[gerek].apply(pd.to_numeric, errors='coerce')
    idx = pd.to_datetime(d.index, errors='coerce')
    if getattr(idx, 'tz', None) is not None:
        idx = idx.tz_localize(None)
    d.index = idx.normalize()
    d = d[~d.index.isna()]
    d = d[~d.index.duplicated(keep='last')].sort_index()
    d = d.dropna(subset=['Close'])
    d = d[(d['Close'] > 0) & (d['High'] >= d['Low'])]
    return d if len(d) else None

_BI_ALAN = {'open', 'high', 'low', 'close', 'volume', 'adj close'}

def _bi_yapi(o, ad='pkl', derinlik=0, L=None) -> List[str]:
    """Teşhis: pkl'in iskeletini (tip, anahtar, boyut) döker."""
    L = [] if L is None else L
    girinti = '  ' * derinlik
    if isinstance(o, dict):
        L.append(f'{girinti}{ad}: dict ({len(o)} anahtar) ör: {list(o)[:5]}')
        if derinlik < 3:
            for k in list(o)[:4]:
                _bi_yapi(o[k], repr(k), derinlik + 1, L)
    elif isinstance(o, pd.DataFrame):
        kol = list(o.columns[:6])
        L.append(f'{girinti}{ad}: DataFrame {o.shape} index={type(o.index).__name__} kolon ör: {kol}')
    elif isinstance(o, (list, tuple)):
        L.append(f'{girinti}{ad}: {type(o).__name__} ({len(o)})')
        if o and derinlik < 3:
            _bi_yapi(o[0], '[0]', derinlik + 1, L)
    else:
        L.append(f'{girinti}{ad}: {type(o).__name__} = {str(o)[:60]}')
    return L

def _bi_genis_df(df: pd.DataFrame) -> Optional[dict]:
    """MultiIndex kolonlu geniş tablo → {sembol: OHLCV}. Alan seviyesi 0 ya da 1 olabilir."""
    if not isinstance(df.columns, pd.MultiIndex) or df.columns.nlevels != 2:
        return None
    for alan_lvl in (0, 1):
        alanlar = {str(x).lower() for x in df.columns.get_level_values(alan_lvl).unique()}
        if {'close', 'volume'} <= alanlar:
            sem_lvl = 1 - alan_lvl
            return {s: df.xs(s, axis=1, level=sem_lvl) for s in df.columns.get_level_values(sem_lvl).unique()}
    return None

def _bi_coz(o, derinlik=0) -> Optional[dict]:
    """pkl içinden {sembol: OHLCV DataFrame} sözlüğünü bulur (iç içe yapılar dahil)."""
    if isinstance(o, pd.DataFrame):
        for k in ('symbol', 'sembol', 'ticker', 'hisse'):
            if k in o.columns:
                return {s: g.drop(columns=[k]).set_index(g.index) for s, g in o.groupby(k)}
        return _bi_genis_df(o)
    if not isinstance(o, dict) or not o:
        return None
    # (a) doğrudan {sembol: DataFrame}
    df_say = sum(isinstance(v, pd.DataFrame) for v in o.values())
    anahtar_alan = {str(k).lower() for k in o} & _BI_ALAN
    if df_say >= max(3, len(o) // 2) and len(anahtar_alan) < 2:
        return o
    # (b) {alan: geniş tablo}  örn. {'Close': df(tarih × sembol), 'Volume': ...}
    if {'close', 'volume'} <= {str(k).lower() for k in o}:
        alanlar = {_BI_KOLON.get(str(k).lower(), k): v for k, v in o.items()
                   if str(k).lower() in _BI_ALAN and isinstance(v, pd.DataFrame)}
        if 'Close' in alanlar:
            semboller = alanlar['Close'].columns
            return {s: pd.DataFrame({a: t[s] for a, t in alanlar.items() if s in t.columns}) for s in semboller}
    # (c) iç katmanlarda ara; en çok hisse içeren adayı seç
    if derinlik >= 3:
        return None
    en_iyi = None
    for v in o.values():
        aday = _bi_coz(v, derinlik + 1)
        if aday and (en_iyi is None or len(aday) > len(en_iyi)):
            en_iyi = aday
    return en_iyi

def bi_veri_oku(yol: str) -> Dict[str, pd.DataFrame]:
    if not os.path.exists(yol):
        raise FileNotFoundError(f'Önbellek yok: {yol} — Drive bağlı mı? (drive.mount)')
    t0 = time.time()
    with open(yol, 'rb') as f:
        ham = pickle.load(f)
    cozulen = _bi_coz(ham)
    if not cozulen:
        yapi = '\n'.join(_bi_yapi(ham))
        bi_log.error('pkl içinde hisse tablosu bulunamadı. Yapı:\n' + yapi)
        raise ValueError('pkl yapısı tanınmadı — yukarıdaki yapı dökümünü gönder.')
    veri, bozuk = {}, 0
    for s, df in cozulen.items():
        n = bi_df_normalize(df)
        if n is None:
            bozuk += 1; continue
        veri[bi_sembol(s)] = n
    if not veri:
        bi_log.error('Tablolar bulundu ama hiçbiri OHLCV değil. Yapı:\n' + '\n'.join(_bi_yapi(ham)))
    son = max(d.index[-1] for d in veri.values()) if veri else None
    bi_log.info(f'Önbellek: {len(veri)} hisse okundu, {bozuk} bozuk atlandı, '
                f'son tarih {son.date() if son is not None else "-"} ({time.time()-t0:.1f}s)')
    return veri

def bi_tazele(veri: Dict[str, pd.DataFrame], paket: int) -> int:
    """pkl'in son gününden sonrasını yfinance ile BELLEKTE ekler. pkl'e yazmaz."""
    try:
        import yfinance as yf
    except ImportError:
        bi_log.warning('yfinance yok (pip install yfinance) — tazeleme atlandı.'); return 0
    son = max(d.index[-1] for d in veri.values())
    bugun = pd.Timestamp(_dt.date.today())
    if son >= bugun:
        bi_log.info('Önbellek zaten güncel.'); return 0
    semboller = sorted(veri)
    eklenen = 0
    for i in range(0, len(semboller), paket):
        grup = semboller[i:i+paket]
        try:
            ind = yf.download([f'{s}.IS' for s in grup], start=(son + pd.Timedelta(days=1)).date(),
                              interval='1d', group_by='ticker', auto_adjust=False,
                              progress=False, threads=True)
        except Exception as e:
            bi_log.warning(f'Tazeleme paketi {i//paket+1} hata: {e}'); continue
        if ind is None or ind.empty:
            continue
        for s in grup:
            try:
                parca = ind[f'{s}.IS'] if isinstance(ind.columns, pd.MultiIndex) else ind
                parca = bi_df_normalize(parca)
                if parca is None: continue
                yeni = parca[parca.index > veri[s].index[-1]]
                if len(yeni):
                    veri[s] = pd.concat([veri[s], yeni]); eklenen += 1
            except KeyError:
                continue
            except Exception as e:
                bi_log.debug(f'{s} tazeleme: {e}')
    yeni_son = max(d.index[-1] for d in veri.values())
    bi_log.info(f'Tazeleme: {eklenen} hisseye yeni bar eklendi → son tarih {yeni_son.date()} (yalnız bellekte)')
    return eklenen

# ──────────────────────────────────────────────────────────────────────────
# 4) GÖSTERGE HAZIRLIĞI
# ──────────────────────────────────────────────────────────────────────────
def bi_hazirla(df: pd.DataFrame, piyasa: pd.Series) -> pd.DataFrame:
    d = df.copy()
    rng = (d['High'] - d['Low']).replace(0, np.nan)
    d['CLV'] = (((d['Close'] - d['Low']) - (d['High'] - d['Close'])) / rng).fillna(0.0)
    d['RET'] = d['Close'].pct_change()
    d['VMED20'] = d['Volume'].rolling(20, min_periods=10).median().shift(1)
    d['VORAN'] = d['Volume'] / d['VMED20']
    # Çok günlük kurallarda tek bir dev hacim günü sonucu taşımasın: hacim 3x medyanda kırpılır
    d['VCAP'] = np.minimum(d['Volume'], (3 * d['VMED20']).fillna(d['Volume']))
    d['AD'] = (d['CLV'] * d['VCAP']).cumsum()
    d['OBV'] = (np.sign(d['RET'].fillna(0)) * d['Volume']).cumsum()
    d['SMA50'] = d['Close'].rolling(50, min_periods=30).mean()
    d['SMA200'] = d['Close'].rolling(200, min_periods=120).mean()
    d['PIY'] = piyasa.reindex(d.index)
    return d

def bi_piyasa_serisi(veri: Dict[str, pd.DataFrame]) -> pd.Series:
    """Evren medyan günlük getirisi (endeks yerine; tek hissenin ağırlığı yok)."""
    getiriler = pd.DataFrame({s: d['Close'].pct_change() for s, d in veri.items()})
    say = getiriler.notna().sum(axis=1)
    med = getiriler.median(axis=1)
    med[say < 50] = np.nan                             # az hisseli gün güvenilmez
    return med

# ──────────────────────────────────────────────────────────────────────────
# 5) KURAL_MOTORU
# ──────────────────────────────────────────────────────────────────────────
@dataclass
class BI_Kural:
    ad: str
    agirlik: float
    aciklama: str
    fn: Callable[[pd.DataFrame], dict]   # → {'gecti': bool, 'deger': float, 'not': str}

def _k_goreceli_guc(d):
    if len(d) < 6 or d['PIY'].iloc[-5:].isna().any():
        return dict(gecti=False, deger=np.nan, not_='piyasa verisi eksik')
    h = d['Close'].iloc[-1] / d['Close'].iloc[-6] - 1
    p = (1 + d['PIY'].iloc[-5:]).prod() - 1
    fark = h - p
    return dict(gecti=fark > 0.05, deger=fark, not_=f'5g hisse {h:+.1%} / piyasa {p:+.1%}')

def _k_zayif_gunde_guc(d, esik=None):
    esik = BI_AYAR['PIYASA_ESIK'] if esik is None else esik
    s = d.iloc[-10:]
    zayif = s[s['PIY'] < esik]
    if len(zayif) == 0:
        return dict(gecti=False, deger=np.nan, not_='son 10 günde zayıf piyasa günü yok')
    fark = (zayif['RET'] - zayif['PIY']).mean()
    return dict(gecti=fark > 0.02, deger=fark,
                not_=f'{len(zayif)} zayıf günde ort. fark {fark:+.1%}')

def _k_hacim_patlamasi(d):
    v = d['VORAN'].iloc[-1]
    return dict(gecti=bool(v >= 2.5), deger=v, not_=f'son gün hacim medyanın {v:.1f} katı')

def _k_kapanis_gucu_son(d):
    c = d['CLV'].iloc[-1]
    return dict(gecti=c >= 0.6, deger=c, not_=f'son gün kapanış konumu {c:+.2f} (−1 dip, +1 tepe)')

def _k_kapanis_gucu_10(d):
    s = d.iloc[-10:]
    w = (s['CLV'] * s['VCAP']).sum() / max(s['VCAP'].sum(), 1)
    ust = int((s['CLV'] > 0).sum())
    return dict(gecti=(w >= 0.2) and (ust >= 6), deger=w,
                not_=f'10g hacim ağırlıklı kapanış konumu {w:+.2f}, üst yarıda kapanan gün {ust}/10')

def _k_ad_uyumsuzluk(d):
    if len(d) < 21:
        return dict(gecti=False, deger=np.nan, not_='veri kısa')
    ad = (d['AD'].iloc[-1] - d['AD'].iloc[-21]) / max(d['VCAP'].iloc[-20:].sum(), 1)
    fiy = d['Close'].iloc[-1] / d['Close'].iloc[-21] - 1
    return dict(gecti=(ad > 0.15) and (fiy < 0.02), deger=ad,
                not_=f'20g A/D oranı {ad:+.2f}, fiyat {fiy:+.1%}')

def _k_obv_uyumsuzluk(d):
    if len(d) < 20:
        return dict(gecti=False, deger=np.nan, not_='veri kısa')
    x = np.arange(20)
    obv = d['OBV'].iloc[-20:].to_numpy(float); c = d['Close'].iloc[-20:].to_numpy(float)
    eg_obv = np.polyfit(x, obv, 1)[0] / max(d['Volume'].iloc[-20:].mean(), 1)
    eg_c = np.polyfit(x, c, 1)[0] / c.mean()
    return dict(gecti=(eg_obv > 0.05) and (eg_c < 0), deger=eg_obv,
                not_=f'OBV eğimi {eg_obv:+.2f}, fiyat eğimi {eg_c:+.2%}/gün')

def _k_emilim(d):
    s = d.iloc[-20:]
    m = s[(s['VORAN'] >= 2.0) & (s['RET'].abs() < 0.02) & (s['CLV'] > 0)]
    return dict(gecti=len(m) >= 2, deger=float(len(m)),
                not_=f'20g içinde yüksek hacimli-sabit-güçlü kapanışlı gün: {len(m)}')

def _k_dipten_donus(d):
    if len(d) < 60:
        return dict(gecti=False, deger=np.nan, not_='veri kısa')
    for k in range(1, 4):
        i = len(d) - k
        once = d['Low'].iloc[max(0, i-250):i]
        if len(once) == 0: continue
        r = d.iloc[i]
        if r['Low'] <= once.min() and r['CLV'] >= 0.5 and r['VORAN'] >= 2.0:
            return dict(gecti=True, deger=float(k),
                        not_=f'{d.index[i].date()}: 52h dip kırıldı, üstte kapandı, hacim {r["VORAN"]:.1f}x')
    return dict(gecti=False, deger=0.0, not_='son 3 günde dipten hacimli dönüş yok')

BI_KURALLAR: List[BI_Kural] = [
    BI_Kural('GORECELI_GUC_5',   2, 'Son 5 günde piyasayı %5+ geçti', _k_goreceli_guc),
    BI_Kural('ZAYIF_GUNDE_GUC',  2, 'Piyasanın düştüğü günlerde ort. %2+ iyi', _k_zayif_gunde_guc),
    BI_Kural('HACIM_PATLAMASI',  1, 'Son gün hacim 20g medyanın 2.5x+', _k_hacim_patlamasi),
    BI_Kural('KAPANIS_GUCU_SON', 1, 'Son gün mumun üst %20\'sinde kapanış', _k_kapanis_gucu_son),
    BI_Kural('KAPANIS_GUCU_10',  2, '10 günde hacim ağırlıklı kapanışlar üst yarıda', _k_kapanis_gucu_10),
    BI_Kural('AD_UYUMSUZLUK',    3, 'A/D yükseliyor, fiyat yerinde/aşağıda', _k_ad_uyumsuzluk),
    BI_Kural('OBV_UYUMSUZLUK',   1, 'OBV yükseliyor, fiyat düşüyor', _k_obv_uyumsuzluk),
    BI_Kural('EMILIM',           2, 'Yüksek hacim geliyor ama fiyat düşmüyor (satış emiliyor)', _k_emilim),
    BI_Kural('DIPTEN_DONUS',     3, '52h dip kırılıp hacimle üstte kapanış (son 3 gün)', _k_dipten_donus),
]
BI_MAKS = sum(k.agirlik for k in BI_KURALLAR)

def bi_kural_motoru(d: pd.DataFrame) -> dict:
    sonuc, puan = {}, 0.0
    for k in BI_KURALLAR:
        try:
            r = k.fn(d)
        except Exception as e:
            bi_log.debug(f'{k.ad} hata: {e}')
            r = dict(gecti=False, deger=np.nan, not_=f'HATA: {e}')
        gecti = bool(r.get('gecti', False))
        sonuc[k.ad] = dict(gecti=gecti, deger=r.get('deger', np.nan), not_=r.get('not_', ''))
        if gecti: puan += k.agirlik
    return dict(puan=puan, kurallar=sonuc)

# ──────────────────────────────────────────────────────────────────────────
# 6) TARAMA
# ──────────────────────────────────────────────────────────────────────────
def bi_tara(veri: Dict[str, pd.DataFrame]) -> (pd.DataFrame, Dict[str, pd.DataFrame], Dict[str, dict]):
    A = BI_AYAR
    piyasa = bi_piyasa_serisi(veri)
    son_tarih = max(d.index[-1] for d in veri.values())
    satirlar, hazir, detay, atla = [], {}, {}, dict(kisa=0, eski=0, hata=0)
    for s, df in veri.items():
        try:
            df = df.iloc[A['ILK_ATLA']:]
            if len(df) < A['MIN_BAR']:
                atla['kisa'] += 1; continue
            if (son_tarih - df.index[-1]).days > 5:
                atla['eski'] += 1; continue          # işlem görmeyen / kotasyondan çıkan
            d = bi_hazirla(df, piyasa)
            km = bi_kural_motoru(d)
            son = d.iloc[-1]
            dip_bolge = bool(pd.notna(son['SMA50']) and pd.notna(son['SMA200'])
                             and son['Close'] < son['SMA50'] and son['Close'] < son['SMA200'])
            satir = dict(sembol=s, tarih=d.index[-1].date(), kapanis=round(son['Close'], 2),
                         gun_getiri=round(son['RET'] * 100, 2) if pd.notna(son['RET']) else np.nan,
                         tavan=bool(pd.notna(son['RET']) and son['RET'] >= A['TAVAN_ESIK']),
                         hacim_kat=round(son['VORAN'], 2) if pd.notna(son['VORAN']) else np.nan,
                         dip_bolgesi=dip_bolge, puan=km['puan'],
                         tutan=','.join(k for k, v in km['kurallar'].items() if v['gecti']))
            satirlar.append(satir); hazir[s] = d; detay[s] = km
        except Exception as e:
            atla['hata'] += 1
            bi_log.debug(f'{s}: {e}')
    tablo = pd.DataFrame(satirlar)
    if len(tablo):
        tablo = tablo.sort_values(['puan', 'hacim_kat'], ascending=[False, False]).reset_index(drop=True)
    bi_log.info(f'Tarandı: {len(tablo)} hisse | atlanan: kısa {atla["kisa"]}, '
                f'güncel değil {atla["eski"]}, hata {atla["hata"]}')
    return tablo, hazir, detay

# ──────────────────────────────────────────────────────────────────────────
# 7) ODAK RAPORU
# ──────────────────────────────────────────────────────────────────────────
def bi_odak_rapor(s: str, d: pd.DataFrame, km: dict) -> str:
    L = [f'═══ {s} — birikim izi {km["puan"]:.0f}/{BI_MAKS:.0f}  (son bar {d.index[-1].date()}) ═══',
         '  NOT: Bu, fiyat+hacim vekilidir; kimin aldığını (AKD) göstermez.', '']
    for k in BI_KURALLAR:
        r = km['kurallar'][k.ad]
        L.append(f'  [{"✓" if r["gecti"] else "·"}] {k.ad:<17} (+{k.agirlik:.0f})  {r["not_"]}')
    son = d.iloc[-1]
    def _o(x): return f'{x:.2f}' if pd.notna(x) else 'veri yetersiz'
    konum = []
    if pd.notna(son['SMA50']):  konum.append('SMA50 ' + ('altında' if son['Close'] < son['SMA50'] else 'üstünde'))
    if pd.notna(son['SMA200']): konum.append('SMA200 ' + ('altında' if son['Close'] < son['SMA200'] else 'üstünde'))
    L += ['', f'  Kapanış {son["Close"]:.2f} | SMA50 {_o(son["SMA50"])} | SMA200 {_o(son["SMA200"])}'
              f'  → {", ".join(konum) or "-"}',
          f'  52h aralık: {d["Low"].iloc[-250:].min():.2f} – {d["High"].iloc[-250:].max():.2f}', '',
          '  Son 15 bar:',
          '  tarih        kapanış   getiri  piyasa   CLV   hacim_kat']
    for t, r in d.iloc[-15:].iterrows():
        L.append(f'  {t.date()}  {r["Close"]:8.2f}  {r["RET"]*100:+6.1f}%  '
                 f'{(r["PIY"]*100 if pd.notna(r["PIY"]) else float("nan")):+6.1f}%  '
                 f'{r["CLV"]:+.2f}   {r["VORAN"]:5.1f}x')
    return '\n'.join(L)

# ──────────────────────────────────────────────────────────────────────────
# 8) ANA
# ──────────────────────────────────────────────────────────────────────────
def bi_calistir(odak: Optional[List[str]] = None, tazele: Optional[bool] = None,
                veri: Optional[Dict[str, pd.DataFrame]] = None):
    A = BI_AYAR
    cikti = os.path.join(A['KOK'], A['CIKTI_ALT'])
    bi_log_kur(cikti)
    bi_log.info(f'BIRIKIM_IZI v{_BI_SURUM} başladı')
    odak = [bi_sembol(x) for x in (odak if odak is not None else A['ODAK'])]
    tazele = A['TAZELE'] if tazele is None else tazele

    if veri is None:
        veri = bi_veri_oku(os.path.join(A['KOK'], A['VERI_ADI']))
    if not veri:
        raise RuntimeError('Okunabilir hisse yok.')
    if tazele:
        bi_tazele(veri, A['TAZELE_PAKET'])
    son = max(d.index[-1] for d in veri.values())
    if son.date() < _dt.date.today():
        bi_log.warning(f'Veri {son.date()} tarihinde bitiyor — bugünün barı YOK. '
                       f'(TAZELE=True ile çalıştır ya da seans sonrası önbelleği güncelle)')

    tablo, hazir, detay = bi_tara(veri)
    if tablo.empty:
        bi_log.error('Sonuç boş.'); return tablo
    goster = tablo[tablo['dip_bolgesi']] if A['DIP_KAPISI'] else tablo

    etiket = son.strftime('%Y%m%d')
    try:
        yol = os.path.join(cikti, f'birikim_{etiket}.csv')
        tmp = yol + '.tmp'; goster.to_csv(tmp, index=False, encoding='utf-8-sig'); os.replace(tmp, yol)
        bi_log.info(f'CSV → {yol}')
    except OSError as e:
        bi_log.error(f'CSV yazılamadı: {e}')

    pd.set_option('display.width', 200)
    print(f'\n── En yüksek birikim izi (ilk {A["EKRAN_ILK"]}, maks puan {BI_MAKS:.0f}) ──')
    print(goster.head(A['EKRAN_ILK']).to_string(index=False))

    raporlar = []
    for s in odak:
        if s not in hazir:
            msg = (f'{s}: taramada yok — önbellekte bulunmuyor, '
                   f'{A["ILK_ATLA"]}+{A["MIN_BAR"]} bar şartını sağlamıyor ya da güncel değil.')
            bi_log.warning(msg); raporlar.append(msg); continue
        sira = int(tablo.index[tablo['sembol'] == s][0]) + 1
        r = bi_odak_rapor(s, hazir[s], detay[s]) + f'\n  Evrendeki sıra: {sira}/{len(tablo)}'
        raporlar.append(r); print('\n' + r)
    if raporlar:
        try:
            yol = os.path.join(cikti, f'birikim_odak_{etiket}.txt')
            with open(yol, 'w', encoding='utf-8') as f: f.write('\n\n'.join(raporlar))
            bi_log.info(f'Odak raporu → {yol}')
        except OSError as e:
            bi_log.error(f'Odak raporu yazılamadı: {e}')
    return tablo

print(f'[ok] birikim_izi.py v{_BI_SURUM} yüklendi → bi_calistir()  |  bi_calistir(odak=["ATATR","..."])')
