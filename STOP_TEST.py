# =============================================================================
#  STOP_TEST.py — Col Yolu: SAF HEDEF / STOP testi (+%10/-%10 ve +%20/-%10)   (2026-09-22)
#
#  Cemal'in kurali (tek ve saf):
#    Giris : kirilim ertesi gun ACILIS (DENETIM ile ayni: e = kirilim+1)
#    CIKIS : once hangisi olursa
#              - fiyat +%10'a degerse  -> HEDEF, kar al (giris x 1.10)   [SAF_10_10]
#                (+%20 / giris x 1.20 ayrica SAF_20_10 olarak da kosar)
#              - fiyat -%10'a degerse   -> STOP, zarar kes (giris x 0.90)
#            Baska hicbir cikis yok (trail yok, taban yok, doji yok).
#            Ikisi de 120 barda olmazsa -> SURE cikisi (kapanistan).
#
#  Gerceklik ayarlari:
#    - Bosluk (gap): acilis stopun altindaysa stop ACILISTAN dolar (daha kotu),
#                    acilis hedefin ustundeyse hedef ACILISTAN dolar (daha iyi).
#    - Ayni mumda hem +%20 hem -%10 goruldu -> once STOP varsayilir (temkinli),
#      sayisi 'belirsiz' olarak raporlanir.
#    - BIST taban kilidi: mum H==L ve dususte ise o gun satis dolmaz, ertesi
#      gun acilisa kayar.
#    - Maliyet: gidis-donus %0.4 (DENETIM ile ayni).
#
#  Karsilastirma: ayni islem listesi, ayni portfoy motoru ile MEVCUT kural
#  (%20 -> SMA20 trail, hedefsiz 120 bar). Boylece fark sadece cikis kuralidir.
#
#  PORTFOY MOTORU (duzeltilmis): gun sirasi = ACILIS girisleri (onceki gunun
#  nakdiyle) -> gun ici cikislar -> kapanis degerlemesi. Acik pozisyon her gun
#  PIYASA fiyatiyla degerlenir, giris tutariyla degil. Her gun degismezler
#  kontrol edilir (nakit>=0, ozsermaye>0, gunluk sicrama < %60); bozulursa
#  hata loglanir ve sonuc 'SUPHELI' isaretlenir.
#
#  Kullanim (BASLAT sonrasi, OB24/OB23/OBUS/xu yukluyse onlari kullanir):
#    exec(open(f'{K}/STOP_TEST.py').read())
#    S = stop_test()                 # 3 set, ~1-3 dk
#  Cikti: {K}/stop_test_sonuc.csv  ve  {K}/stop_test_islemler.csv
# =============================================================================
import os, time, pickle, logging
import numpy as np
import pandas as pd

log = logging.getLogger('col.stop_test')
if not log.handlers:
    _h = logging.StreamHandler(); _h.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    log.addHandler(_h)
log.setLevel(logging.INFO)

K = globals().get('K', '/content/drive/MyDrive/col_tarayici')

# ----------------------------------------------------------------------------- AYARLAR
AYAR = {
    'MALIYET': 0.4,        # gidis-donus %
    'UFUK': 120,           # hedef/stop olmazsa bu kadar bar sonra cik
    'KIRILIM_EN_GEC': 60,  # segment sonrasi kirilim bu bar icinde olmali
    'HL_MAX': 0.20,        # segmentte H==L / V==0 bar orani ust siniri
    'LIK_TL': 1_000_000,   # BIST segment medyan gunluk TL hacim alt siniri
    'MAX_POZ': 12.0,       # tek pozisyon max %
    'SLOT': 30,            # esit agirlik = 100/30
    'MIN_TUTAR': 0.005,    # ozsermayenin binde 5'inden kucuk giris atlanir
    'SICRAMA_MAX': 0.60,   # gunluk ozsermaye degisimi bundan buyukse SUPHELI
}

# ----------------------------------------------------------------------------- KURAL_MOTORU
class CikisKurali:
    """Her kural: cik(o, e, gp) -> (cikis_bar, cikis_fiyat, neden)."""
    ad = 'taban'
    def cik(self, o, e, gp):
        raise NotImplementedError


class HedefStop(CikisKurali):
    """Saf kural: +hedef% veya -stop%, hangisi once. Yoksa UFUK bar sonra kapanis."""
    def __init__(self, hedef=20.0, stop=10.0, ufuk=None, bist=True):
        self.hedef, self.stop = hedef, stop
        self.ufuk = ufuk or AYAR['UFUK']; self.bist = bist
        self.ad = f'SAF +%{hedef:g} / -%{stop:g}'

    def cik(self, o, e, gp):
        O, H, L, C = o['iO'], o['iH'], o['iL'], o['iC']
        th, ts = gp * (1 + self.hedef / 100), gp * (1 - self.stop / 100)
        son = min(e + self.ufuk, len(C) - 1)
        bekleyen_stop = False
        for j in range(e, son + 1):
            o_, h_, l_, c_ = O[j], H[j], L[j], C[j]
            if not (np.isfinite(h_) and np.isfinite(l_)):
                continue
            kilit = self.bist and h_ == l_ and j > 0 and c_ < C[j - 1]
            if bekleyen_stop and not kilit:            # dunku taban kilidinden satis
                return j, float(o_ if np.isfinite(o_) else c_), 'stop_kilit'
            if j > e and np.isfinite(o_):              # bosluklar
                if o_ <= ts and not kilit:
                    return j, float(o_), 'stop_gap'
                if o_ >= th:
                    return j, float(o_), 'hedef_gap'
            vs, vh = l_ <= ts, h_ >= th
            if vs and kilit:                           # taban kilidi: satilamaz
                bekleyen_stop = True
                continue
            if vs and vh:
                return j, float(ts), 'belirsiz_stop'
            if vs:
                return j, float(ts), 'stop'
            if vh:
                return j, float(th), 'hedef'
        return son, float(C[son]), 'sure'


class MevcutTrail(CikisKurali):
    """COL_v1 / DENETIM kurali: +%20 degince SMA20 trail, hedefsiz UFUK bar."""
    ad = 'MEVCUT (%20 -> SMA20 trail)'
    def __init__(self, hedef=20.0, ufuk=None):
        self.hedef = hedef; self.ufuk = ufuk or AYAR['UFUK']

    def cik(self, o, e, gp):
        C, H, s20 = o['iC'], o['iH'], o['s20']
        son = min(e + self.ufuk, len(C) - 1)
        m = H[e + 1:son + 1] >= gp * (1 + self.hedef / 100)
        if m.any():
            jh = int(np.argmax(m)) + e + 1
            alt = np.where(C[jh + 1:] < s20[jh + 1:])[0]
            if len(alt):
                j = int(alt[0]) + jh + 1
                return j, float(C[j]), 'trail'
            return len(C) - 1, float(C[-1]), 'veri_sonu'
        return son, float(C[son]), 'sure'


KURAL_MOTORU = {
    'SAF_10_10': lambda bist: HedefStop(10, 10, bist=bist),   # Cemal: +%10 kar al / -%10 zarar kes
    'SAF_20_10': lambda bist: HedefStop(20, 10, bist=bist),
    'MEVCUT':    lambda bist: MevcutTrail(20),
}

# ----------------------------------------------------------------------------- ISLEM LISTESI
def _kirilim(o):
    tv = np.maximum(o['sO'], o['sC']).max() * 1.002; C = o['iC']
    for j in range(min(AYAR['KIRILIM_EN_GEC'], len(C))):
        if C[j] > tv:
            return j
    return None


def _temiz_olcu(o):
    O, H, L, C, V = o['sO'], o['sH'], o['sL'], o['sC'], o['sV']
    ok = (H > L) & (V > 0); hl = 1 - ok.mean(); lik = float(np.median(C * V))
    if ok.sum() < 5:
        return hl, lik, np.nan, np.nan
    a = (o.get('seg') or {}).get('atr_ref') or np.nan
    rng = (H - L)[ok]
    doji = float((np.abs(C - O)[ok] / rng < 0.15).mean())
    fitil = float(((np.minimum(O, C) - L)[ok] / a).mean()) if (np.isfinite(a) and a > 0) else np.nan
    return hl, lik, doji, fitil


def islem_listesi(OB, kural, bist=True):
    """DENETIM.islemler ile ayni filtreler; cikis secilen kuraldan."""
    R = []; gor = set(); say = dict(ham=0, tekrar=0, hl=0, lik=0, hata=0)
    for o in OB:
        try:
            kb = _kirilim(o)
            if kb is None or kb + 2 > len(o['iC']) - 25:
                continue
            say['ham'] += 1
            key = (o['sembol'], pd.Timestamp(o['iT'][kb]).normalize())
            if key in gor:
                say['tekrar'] += 1; continue
            gor.add(key)
            hl, lik, doji, fitil = _temiz_olcu(o)
            if hl > AYAR['HL_MAX']:
                say['hl'] += 1; continue
            if bist and lik < AYAR['LIK_TL']:
                say['lik'] += 1; continue
            e = kb + 1; gp = float(o['iO'][e])
            if not np.isfinite(gp) or gp <= 0:
                continue
            jt, cp, neden = kural.cik(o, e, gp)
            if jt < e:
                raise ValueError(f'cikis girisden once ({jt}<{e})')
            a = (o.get('seg') or {}).get('atr_ref') or np.nan
            R.append({
                'sembol': o['sembol'],
                'giris_t': pd.Timestamp(o['iT'][e]).normalize(),
                'cikis_t': pd.Timestamp(o['iT'][jt]).normalize(),
                'e': e, 'jt': jt, 'bar': jt - e, 'gp': gp, 'cp': cp, 'neden': neden,
                'g': (cp / gp - 1) * 100 - AYAR['MALIYET'],
                'doji': doji, 'fitil': fitil, 'kural': bool(o.get('GECER', True)),
                'atr_pct': a / gp * 100 if np.isfinite(a) else np.nan, 'o': o,
            })
        except Exception as ex:
            say['hata'] += 1
            log.debug('%s: %s', o.get('sembol'), ex)
    if say['hata']:
        log.warning('islem_listesi: %d kayit hatali atlandi', say['hata'])
    return pd.DataFrame(R), say

# ----------------------------------------------------------------------------- PORTFOY
def _agirlik(r, mod):
    if mod == 'esit':
        return 100.0 / AYAR['SLOT']
    if mod == 'carpan':
        dc = 1.5 if (np.isfinite(r.doji) and r.doji >= 0.23) else (0.7 if (np.isfinite(r.doji) and r.doji < 0.13) else 1.0)
        fc = 2.5 if (np.isfinite(r.fitil) and r.fitil < 0.12) else 1.0
        kc = 1.0 if r.kural else 0.7
        return min(4.0 * dc * fc * kc, AYAR['MAX_POZ'])
    raise ValueError(mod)


def portfoy(q, mod='esit'):
    """Gunluk ozsermaye egrisi. Sira: acilista giris -> gun ici cikis -> kapanis degerleme."""
    bos = dict(egri=pd.Series(dtype=float), alinan=0, atlanan=0, dolu_ort=np.nan, supheli=False)
    if q.empty:
        return bos
    maly = AYAR['MALIYET'] / 200
    takvim = set()
    for r in q.itertuples():
        takvim.update(pd.to_datetime(r.o['iT'][r.e:r.jt + 1]).normalize())
    takvim = sorted(takvim)
    giris_gun = {}
    for r in q.sort_values('giris_t').itertuples():
        giris_gun.setdefault(r.giris_t, []).append(r)

    nakit, ozs = 100.0, 100.0
    acik = []; egri = {}; alinan = atlanan = 0; dolu = []; supheli = False
    for t in takvim:
        ozs_dun = ozs
        # 1) ACILIS: girisler, sadece eldeki nakitle
        for r in giris_gun.get(t, []):
            if any(p['sembol'] == r.sembol for p in acik):
                atlanan += 1; continue
            tutar = min(ozs_dun * _agirlik(r, mod) / 100, nakit)
            if tutar < ozs_dun * AYAR['MIN_TUTAR']:
                atlanan += 1; continue
            nakit -= tutar; alinan += 1
            adet = tutar * (1 - maly) / r.gp
            yol = dict(zip(pd.to_datetime(r.o['iT'][r.e:r.jt + 1]).normalize(), r.o['iC'][r.e:r.jt + 1]))
            acik.append({'sembol': r.sembol, 'adet': adet, 'cp': r.cp, 'cikis_t': r.cikis_t,
                         'yol': yol, 'son': r.gp})
        # 2) GUN ICI: cikislar (cikis fiyatindan)
        kal = []
        for p in acik:
            if p['cikis_t'] <= t:
                nakit += p['adet'] * p['cp'] * (1 - maly)
            else:
                kal.append(p)
        acik = kal
        # 3) KAPANIS: piyasa degerlemesi
        deger = 0.0
        for p in acik:
            v = p['yol'].get(t)
            if v is not None and np.isfinite(v):
                p['son'] = float(v)
            deger += p['adet'] * p['son']
        ozs = nakit + deger; egri[t] = ozs
        dolu.append(len(acik))
        # degismezler
        if nakit < -1e-6 or ozs <= 0 or (ozs_dun > 0 and abs(ozs / ozs_dun - 1) > AYAR['SICRAMA_MAX']):
            if not supheli:
                log.error('portfoy degismez bozuldu %s: nakit=%.2f ozs=%.2f dun=%.2f', t.date(), nakit, ozs, ozs_dun)
            supheli = True
    return dict(egri=pd.Series(egri).sort_index(), alinan=alinan, atlanan=atlanan,
                dolu_ort=float(np.mean(dolu)) if dolu else np.nan, supheli=supheli)


def _egri_ozet(e):
    if len(e) < 2:
        return np.nan, np.nan, np.nan
    yil = max((e.index[-1] - e.index[0]).days / 365.25, 0.1)
    top = (e.iloc[-1] / e.iloc[0] - 1) * 100
    cagr = ((e.iloc[-1] / e.iloc[0]) ** (1 / yil) - 1) * 100
    dd = ((e / e.cummax()) - 1).min() * 100
    return top, cagr, dd

# ----------------------------------------------------------------------------- TEST
def _set_testi(OB, ad, bist, xu=None):
    satir = []; islemler = []
    print(f"\n{'=' * 66}\n  {ad}\n{'=' * 66}")
    print(f"  {'kural':30s} {'n':>5s} {'kaz%':>5s} {'isl.basi':>8s} {'medyan':>7s} {'ort.bar':>7s}")
    qs = {}
    for anahtar, fab in KURAL_MOTORU.items():
        kural = fab(bist)
        q, say = islem_listesi(OB, kural, bist)
        qs[anahtar] = (kural, q)
        if q.empty:
            print(f"  {kural.ad:30s}  islem yok"); continue
        print(f"  {kural.ad:30s} {len(q):5d} {100 * (q.g > 0).mean():5.0f} {q.g.mean():+8.1f} "
              f"{q.g.median():+7.1f} {q.bar.mean():7.0f}")
        dag = q.neden.value_counts()
        print(f"      cikislar: " + ', '.join(f'{k} {v}' for k, v in dag.items()))
        x = q.drop(columns='o').copy(); x['set'] = ad; x['kural_ad'] = kural.ad; islemler.append(x)
    # portfoy
    bas = min(q.giris_t.min() for _, q in qs.values() if not q.empty)
    son = max(q.cikis_t.max() for _, q in qs.values() if not q.empty)
    xu_top = np.nan
    if xu is not None and len(xu):
        x = xu.Close[(xu.index >= bas) & (xu.index <= son)]
        if len(x) > 1:
            xu_top = (x.iloc[-1] / x.iloc[0] - 1) * 100
    print(f"\n  PORTFOY {bas.date()} -> {son.date()}   (acilista giris, gun ici cikis, maliyet %{AYAR['MALIYET']})")
    print(f"  {'kural':30s} {'boyut':7s} {'alinan':>6s} {'atlanan':>7s} {'dolu':>5s} {'TOPLAM':>8s} {'YILLIK':>7s} {'MAX DD':>7s}")
    for anahtar, (kural, q) in qs.items():
        if q.empty:
            continue
        for mod in ('esit', 'carpan'):
            p = portfoy(q, mod); top, cagr, dd = _egri_ozet(p['egri'])
            isaret = '  SUPHELI' if p['supheli'] else ''
            print(f"  {kural.ad:30s} {mod:7s} {p['alinan']:6d} {p['atlanan']:7d} {p['dolu_ort']:5.1f} "
                  f"{top:+7.0f}% {cagr:+6.0f}% {dd:+6.0f}%{isaret}")
            satir.append({'set': ad, 'kural': kural.ad, 'boyut': mod, 'n': len(q),
                          'kazanan%': 100 * (q.g > 0).mean(), 'islem_basi': q.g.mean(), 'medyan': q.g.median(),
                          'ort_bar': q.bar.mean(), 'alinan': p['alinan'], 'atlanan': p['atlanan'],
                          'ort_dolu_slot': p['dolu_ort'], 'toplam%': top, 'yillik%': cagr, 'maxdd%': dd,
                          'xu100%': xu_top, 'supheli': p['supheli'],
                          **{f'cikis_{k}': v for k, v in q.neden.value_counts().items()}})
    if np.isfinite(xu_top):
        print(f"  {'XU100 ayni donem':30s} {'':7s} {'':6s} {'':7s} {'':5s} {xu_top:+7.0f}%")
    return satir, islemler


def _yukle(ad_listesi):
    for ad in ad_listesi:
        y = f'{K}/{ad}'
        if os.path.exists(y):
            with open(y, 'rb') as f:
                OB = pickle.load(f)
            log.info('%s yuklendi: %d kayit', ad, len(OB)); return OB
    log.warning('bulunamadi: %s', ad_listesi); return None


def stop_test(OB24=None, OB23=None, OBUS=None, xu=None, kaydet=True):
    t0 = time.time(); g = globals()
    OB24 = OB24 if OB24 is not None else g.get('OB24') or _yukle(['onbellek_2024_26_v3.pkl', 'onbellek_2024_26.pkl'])
    OB23 = OB23 if OB23 is not None else g.get('OB23') or _yukle(['onbellek_2023_v3.pkl', 'onbellek_2023.pkl'])
    OBUS = OBUS if OBUS is not None else g.get('OBUS') or _yukle(['onbellek_ABD.pkl'])
    xu = xu if xu is not None else g.get('xu')
    setler = [(OB24, 'BIST 2024-26', True), (OB23, 'BIST 2023', True), (OBUS, 'ABD 2024-26', False)]
    tum_satir, tum_islem = [], []
    for OB, ad, bist in setler:
        if not OB:
            log.warning('%s atlandi (onbellek yok)', ad); continue
        try:
            s, i = _set_testi(OB, ad, bist, xu if bist else None)
            tum_satir += s; tum_islem += i
        except Exception:
            log.exception('%s testi coktu', ad)
    S = pd.DataFrame(tum_satir)
    if kaydet and not S.empty:
        try:
            S.to_csv(f'{K}/stop_test_sonuc.csv', index=False)
            pd.concat(tum_islem).to_csv(f'{K}/stop_test_islemler.csv', index=False)
            print(f"\n  -> {K}/stop_test_sonuc.csv, stop_test_islemler.csv")
        except Exception:
            log.exception('csv yazilamadi')
    print(f"  ({time.time() - t0:.0f}s)")
    return S


print("[ok] STOP_TEST yuklendi -> S = stop_test()")
