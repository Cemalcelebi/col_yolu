# test_col_dip2.py — D13 col_dip2 (COL_v1) mekanik sinama (2026-10-21)
# Calistir: python3 test_col_dip2.py   (repo kokunde; COL_v1.py exec edilir, veri indirilmez)
# 1) D13 sentetik: dusus -> dip -> savunma + parabolik yuvarlanma + kucuk mum obekleri -> COL; kutu dipten baslar (kural 1).
# 2) Trend yukari seri -> None ('inis yok' / 'dipte degil'); dipten sonra tekrar yeni dip -> kutu yeni dibe kayar (eski raf girmez).
# 3) Cikti alanlari col_dip (D12) ile ayni cekirdek alanlari tasir (takip / carpanlar_hesapla icin).
# 4) col_olc SEGMENT_MOD='dip2' ile col_dip2'yi kullanir.
import io, contextlib, numpy as np, pandas as pd, os, sys

K = os.path.dirname(os.path.abspath(__file__))
ns = {'__name__': 'COL_v1_test'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(os.path.join(K, 'COL_v1.py'), encoding='utf-8').read(), 'COL_v1.py', 'exec'), ns)
col_dip, col_dip2, col_olc = ns['col_dip'], ns['col_dip2'], ns['col_olc']


def seri(n=420, tohum=1, dusus=True, dip_sonra=40, ikinci_dip=False):
    """Sentetik OHLCV: 300 bar normal (gunluk aralik ~%3) -> 30 bar dusus (-%25) -> dip -> dip_sonra bar sakin yuvarlanma
    (kucuk mumlar, diplerin parabolik yukari donusu) ."""
    rng = np.random.default_rng(tohum)
    idx = pd.bdate_range('2024-01-01', periods=n)
    c = np.empty(n); c[0] = 100.0
    for i in range(1, n):
        c[i] = c[i - 1] * (1 + rng.normal(0.0003, 0.015))
    d0 = n - dip_sonra - 1
    if dusus:
        for i in range(d0 - 30, d0 + 1):
            c[i] = c[i - 1] * (1 - 0.0095 + rng.normal(0, 0.004))
        dip = c[d0]
        for j, i in enumerate(range(d0 + 1, n)):
            u = j / max(1, dip_sonra - 1)
            c[i] = dip * (1 + 0.002 + 0.06 * u * u) * (1 + rng.normal(0, 0.003))     # parabolik yukari yuvarlanma, kucuk mumlar
        if ikinci_dip:
            k = d0 + dip_sonra // 2
            c[k] = dip * 0.93; c[k + 1] = dip * 0.95
    o = c * (1 + rng.normal(0, 0.002, n))
    ar = np.where(np.arange(n) > d0, 0.006, 0.03) if dusus else np.full(n, 0.03)
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, ar / 2)))
    l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, ar / 2)))
    v = rng.lognormal(12, 0.4, n)
    return pd.DataFrame({'Open': o, 'High': h, 'Low': l, 'Close': c, 'Volume': v}, index=idx)


def sina():
    hata = []
    # 1) dip -> savunma -> yuvarlanma -> obek: COL ve kutu dipten baslar
    ns['D13_YUV'] = 'parabol'; ns['D13_OBEK'] = 1; ns['D13_KONUM'] = 0.5; ns['D13_INIS'] = 5.0; ns['D13_KUCUK'] = 99.0
    df = seri(dip_sonra=40)
    out, t = col_dip2(df, tani=True)
    if not out: hata.append(f"1) sentetik col bulunmadi: {t.get('red')} {t}")
    else:
        dip_i = int(np.argmin(df.Low.to_numpy()[-160:])) + len(df) - 160
        if t['dip_i'] != dip_i: hata.append(f"1) kutu dipten baslamiyor: dip_i {t['dip_i']} beklenen {dip_i}")
        if out['uzunluk'] != len(df) - dip_i: hata.append(f"1) uzunluk {out['uzunluk']} != {len(df) - dip_i} (dipten bugune)")
        if out['taban'] > df.Low.to_numpy()[dip_i] * 1.0001: hata.append("1) taban kutu dibi degil")
    # 2a) trend yukari -> None
    out2, t2 = col_dip2(seri(dusus=False), tani=True)
    if out2: hata.append("2a) yukari trendde col bulundu")
    # 2b) ikinci (yeni) dip -> kutu yeni dibe kayar, eski raf girmez
    df3 = seri(dip_sonra=60, ikinci_dip=True)
    out3, t3 = col_dip2(df3, tani=True)
    k = len(df3) - 61 + 30
    if t3.get('dip_i') != k: hata.append(f"2b) kutu yeni dipten baslamiyor: dip_i {t3.get('dip_i')} beklenen {k}")
    # 3) cikti alanlari: col_dip cekirdek alanlari
    if out:
        gerekli = {'bas_tarih', 'son_tarih', 'uzunluk', 'hafta_bar', 'cekirdek_bar', 'atr_ref', 'taban', 'tavan', 'yukseklik_atr',
                   'govde_ort', 'doji', 'alt_fitil', 'dar', 'gecerli_oran', 'egim', 'bb_rank', 'hacim_orani', 'mod'}
        eksik = gerekli - set(out)
        if eksik: hata.append(f"3) eksik alan: {eksik}")
        if out['mod'] != 'dip2': hata.append("3) mod dip2 degil")
    # 4) col_olc dip2 modunu kullanir
    eski_mod = ns['SEGMENT_MOD']; ns['SEGMENT_MOD'] = 'dip2'
    try:
        r = col_olc(df)
        if r is not None and r.get('mod') != 'dip2': hata.append("4) col_olc dip2 kullanmadi")
    finally:
        ns['SEGMENT_MOD'] = eski_mod
    # 5) D12 hala calisiyor (ortak yardimci kirmadi)
    try:
        col_dip(df)
    except Exception as ex:
        hata.append(f"5) col_dip hata: {ex}")
    return hata


if __name__ == '__main__':
    h = sina()
    if h:
        print('HATA:'); [print(' -', x) for x in h]; sys.exit(1)
    print('test_col_dip2: 5/5 OK')
