# test_tema_sepet.py — tema_sepet v2 testleri. Sahte col_tarayici (test_tema_col.py'nin sahte COL/OLCUM/DESEN'i) + GERÇEK tema_col.py.
# Sınananlar: (1) veri okuma (2) sepet toplamı + küçük sepet dışarıda (3) erken işaret günü bağımsız hesapla aynı, geleceğe
# bakmıyor, 20 gün sessizlik kuralı (4) LİDER etiketi: 0..20 gün penceresi, kendi sıçraması rüzgâr sayılmıyor, sepetsiz = dışarıda
# (5) fon kontrolü (6) gecikme/eğri: dip ve dalga günü tam doğru, dilim doğru (7) çöl durumu (8) uçtan uca: ekilmiş rüzgâr etkisi
# GEÇTİ · plasebo 3 dünyada GEÇMEDİ · Adım 0 / kısa veri DURUR · BUGÜN listesi · dosyalar/damga (9) çakışma kapısı
import os, io, sys, types, pickle, tempfile, json, shutil
from contextlib import redirect_stdout, redirect_stderr
import numpy as np, pandas as pd
D0 = os.path.dirname(os.path.abspath(__file__))
HATA = []
def chk(ad, k, ek=""):
    print(f"  [{'OK' if k else 'HATA'}] {ad} {ek}"); (not k) and HATA.append(ad)

_fx = {"__file__": os.path.join(D0, "test_tema_col.py"), "__name__": "fx"}
exec(open(os.path.join(D0, "test_tema_col.py"), encoding="utf-8").read().split("TCm = modul_yukle")[0], _fx)
COL_V1 = _fx["COL_V1"] + '''
MIN_UZ = 20
MAX_YUK = 6
def col_segment(x):
    """test ikamesi: son 30 bar dar bantta ise çöl."""
    c = x["Close"].to_numpy(float)[-30:]
    if len(c) < 30: return None
    return {"uzunluk": 30, "yukseklik_atr": float((c.max() - c.min()) / max(c.mean() * 0.01, 1e-9)), "tavan": float(c.max())}
'''
OLCUM, DESEN, ob_kayit = _fx["OLCUM"], _fx["DESEN"], _fx["ob_kayit"]
FONLAR = _fx["FONLAR"]

def modul_yukle(yol, ad):
    m = types.ModuleType(ad); m.__file__ = yol; sys.modules[ad] = m
    with redirect_stdout(io.StringIO()):
        exec(compile(open(yol, encoding="utf-8").read(), yol, "exec"), m.__dict__)
    return m

TSm = modul_yukle(os.path.join(D0, "tema_sepet.py"), "tema_sepet_test"); TS = TSm.__dict__
T = TS["TS_TANIM"]

print("T1 veri okuma")
ix = pd.date_range("2020-01-01", periods=10, freq="B", tz="UTC")
df = pd.DataFrame({"open": 1.0, "high": 1.0, "low": 1.0, "close": [10, 11, 0, 12, 12, 21.6, 22, 22, 22, 22.0], "volume": 1}, index=ix)
df = pd.concat([df, df.iloc[[-1]]])
C = TS["ts_kapanis"]({"AAA.AM": df, "BBB.AM": None, "CCC.AM": pd.DataFrame({"x": [1]})})
chk("sembol .AM'siz, tz'siz, tekrar gün yok", list(C.columns) == ["AAA"] and C.index.tz is None and C.index.is_unique and len(C) == 10)
chk("sıfır fiyat NaN", np.isnan(C["AAA"].iloc[2]))
sar = {"kayit": "2026-09-17", "veri": {"AAA.AM": df}}
C2 = TS["ts_kapanis"](TS["ts_veri_ac"](sar))
chk("col_atilim_TEK önbellek biçimi {kayit, veri:{...}} açılır, sonuç düz sözlükle aynı", C2.equals(C))
try:
    TS["ts_kapanis"](sar); chk("sarılı biçim açılmadan verilirse yapıyı söyleyen hata", False)
except RuntimeError as e:
    chk("sarılı biçim açılmadan verilirse yapıyı söyleyen hata", "kayit" in str(e) and "veri" in str(e), str(e)[:90])
R = TS["ts_getiri"](C)
chk("|günlük| > %50 bozuk veri NaN (+%80 sıçrama)", np.isnan(R["AAA"].iloc[5]) and abs(R["AAA"].iloc[1] - 0.1) < 1e-12)

print("T1b uzun fiyat indirici (parti, kesilip sürme, bayat önbellek)")
with tempfile.TemporaryDirectory() as td:
    gx = pd.bdate_range("2019-01-01", periods=300)
    TAM = pd.DataFrame({f"H{i:03d}": 10 + np.arange(300) * 0.01 * (i + 1) for i in range(250)}, index=gx)
    cagri = []
    def kopan(liste, bas_):                                         # 1. parti gelir; sonrası (yeniden deneme dahil) kopar
        cagri.append(list(liste))
        if len(cagri) >= 2:
            raise ConnectionError("ağ koptu")
        return TAM[[x for x in liste if x != "H007"]]              # H007 hiç gelmiyor (borsadan çıkmış)
    sem = list(TAM.columns) + ["H000"]                              # tekrar eden sembol
    try:
        with redirect_stderr(io.StringIO()):
            TS["ts_uzun_fiyat"](td, sem, bas="2019-01-01", parti=100, indir=kopan)
        chk("kopma RuntimeError ile durur", False)
    except RuntimeError as e:
        chk("kopma: yeniden denedi (2 kez) sonra 'kaldığı yerden sürer' diyerek durdu", len(cagri) == 3 and "kaldığı yerden" in str(e), str(len(cagri)))
    D1 = pickle.load(open(os.path.join(td, "tema_sepet_fiyat.pkl"), "rb"))
    chk("kopma: ilk parti diske yazılmış, ikinci yazılmamış", len(D1["bitti"]) == 100 and D1["C"].shape[1] == 99, f"bitti {len(D1['bitti'])} · C {D1['C'].shape}")
    cagri.clear(); sayac = []
    with redirect_stderr(io.StringIO()):
        C1, b1 = TS["ts_uzun_fiyat"](td, sem, bas="2019-01-01", parti=100, indir=lambda l, b: (sayac.append(len(l)), TAM[[x for x in l if x != "H007"]])[1])
    chk("sürme: yalnız kalan 150 sembol indirildi", sum(sayac) == 150, str(sayac))
    chk("sonuç: 249 hisse, sırası istenen sırada, değerler birebir, gelmeyen 1", C1.shape[1] == 249 and list(C1.columns) == [c for c in TAM.columns if c != "H007"]
        and np.allclose(C1.values, TAM.drop(columns="H007").values) and b1["basarisiz"] == 1)
    sayac.clear()
    with redirect_stderr(io.StringIO()):
        TS["ts_uzun_fiyat"](td, sem, bas="2019-01-01", parti=100, indir=lambda l, b: (sayac.append(len(l)), TAM[l[:0]])[1])
    chk("taze önbellek: hiç indirme yok", sum(sayac) == 0)
    D = pickle.load(open(os.path.join(td, "tema_sepet_fiyat.pkl"), "rb")); D["oturum"] = str(pd.Timestamp.now() - pd.Timedelta(days=9))
    pickle.dump(D, open(os.path.join(td, "tema_sepet_fiyat.pkl"), "wb"))
    with redirect_stderr(io.StringIO()):
        TS["ts_uzun_fiyat"](td, sem, bas="2019-01-01", parti=100, indir=lambda l, b: (sayac.append(len(l)), TAM[[x for x in l if x != "H007"]])[1])
    chk("9 günlük bayat önbellek: baştan indirildi (250)", sum(sayac) == 250, str(sum(sayac)))

print("T1c yfinance ad çevirisi (ağsız, sahte yf modülü)")
_yf = types.ModuleType("yfinance"); _istek = []
def _dl(l, **k):
    _istek.append(list(l)); ix_ = pd.bdate_range("2020-01-01", periods=3)
    return pd.concat({"Close": pd.DataFrame({x: [1.0, 2, 3] for x in l}, index=ix_.tz_localize("America/New_York"))}, axis=1)
_yf.download = _dl; _eski = sys.modules.get("yfinance"); sys.modules["yfinance"] = _yf
try:
    Cy = TS["_ts_yf_indir"](["BRK.B", "AAPL"], "2020-01-01")
    chk("BRK.B yfinance'e BRK-B diye sorulur, geri BRK.B adıyla döner; tz'siz", _istek[0] == ["BRK-B", "AAPL"] and list(Cy.columns) == ["BRK.B", "AAPL"] and Cy.index.tz is None)
finally:
    if _eski is not None: sys.modules["yfinance"] = _eski
    else: sys.modules.pop("yfinance", None)

print("T2 sepet")
r = np.random.default_rng(1); gix = pd.bdate_range("2020-01-01", periods=50)
R = pd.DataFrame(r.normal(0, 0.01, (50, 9)), index=gix, columns=[f"X{i}" for i in range(6)] + ["Y0", "Y1", "Y2"])
R.iloc[3, 0] = np.nan
H = pd.DataFrame({"endustri": ["IndX"] * 6 + ["IndY"] * 3 + ["BILINMIYOR"]}, index=[f"X{i}" for i in range(6)] + ["Y0", "Y1", "Y2", "Z"])
S, N, uy = TS["ts_sepet"](R, H, T)
chk("küçük sepet (3 üye) ve bilinmeyen yok", list(S.columns) == ["IndX"] and list(uy) == ["IndX"])
chk("toplam ve sayı elle aynı", np.allclose(S["IndX"], R.iloc[:, :6].sum(axis=1)) and N["IndX"].iloc[3] == 5 and N["IndX"].iloc[4] == 6)

print("T3 erken işaret")
gix = pd.bdate_range("2018-01-01", periods=700)
I = pd.Series(100.0, index=gix); I.iloc[400:] = 100 * (1.004 ** np.arange(300))
spy = pd.Series(100.0, index=gix); ok = pd.Series(True, index=gix)
isr, bas = TS["ts_erken"](I, spy, ok, T)
beklenen = next(gix[i] for i in range(220, 700) if (I.iloc[i] / I.iloc[i - 20] - 1) * 100 >= 5 and I.iloc[i] > I.iloc[i - 199:i + 1].mean())
chk("başlangıç günü bağımsız hesapla aynı", bas[bas].index.min() == beklenen and bas.sum() == 1, f"{bas[bas].index.min().date()} vs {beklenen.date()}")
ik = gix.get_loc(beklenen)
_, bk = TS["ts_erken"](I.iloc[:ik + 1], spy.iloc[:ik + 1], ok.iloc[:ik + 1], T)
chk("geleceğe bakmıyor: o günde kesilince son gün başlangıç", bool(bk.iloc[-1]) and bk.sum() == 1)
spy2 = spy.copy(); spy2.iloc[400:] = I.iloc[400:]
chk("SPY de aynı yükselirse işaret yok", not TS["ts_erken"](I, spy2, ok, T)[1].any())
chk("SMA200 kurulamadan (ilk 200 gün) işaret yok", not TS["ts_erken"](I.iloc[:150] * np.linspace(1, 2, 150), spy.iloc[:150], ok.iloc[:150], T)[0].any())
def iki_ruzgar(bosluk):
    J = pd.Series(100.0, index=gix); a = 400
    J.iloc[a:a + 25] = 100 * 1.004 ** np.arange(25); J.iloc[a + 25:] = J.iloc[a + 24]
    b = a + 25 + bosluk; J.iloc[b:b + 25] = J.iloc[a + 24] * 1.004 ** np.arange(25); J.iloc[b + 25:] = J.iloc[b + 24]
    return TS["ts_erken"](J, spy, ok, T)
i1, b1 = iki_ruzgar(10); i2, b2 = iki_ruzgar(60)
chk("20 günden kısa aradaki ikinci yükseliş YENİ başlangıç değil", b1.sum() == 1, str(b1.sum()))
chk("uzun aradan sonra yeni başlangıç", b2.sum() == 2, str(b2.sum()))
chk("geçersiz gün (üye < 5) işaret yok", not TS["ts_erken"](I, spy, pd.Series(False, index=gix), T)[0].any())

print("T4 lider etiketi")
gix = pd.bdate_range("2018-01-01", periods=700); n_ = 7
base = np.ones(700); base[400:] = 1.004 ** np.arange(300)
Cm = pd.DataFrame({f"S{i}": 50 * base * np.exp(np.random.default_rng(i).normal(0, 0.0005, 700)) for i in range(n_)}, index=gix)
Cm["LONE"] = 50.0; Cm.iloc[410:, Cm.columns.get_loc("LONE")] = 70.0          # tek başına +%40 sıçrayan hisse
for i in range(5):
    Cm[f"Q{i}"] = 20 * np.exp(np.random.default_rng(99 + i).normal(0, 0.0005, 700))
Rm = TS["ts_getiri"](Cm)
Hm = pd.DataFrame({"endustri": ["IndS"] * n_ + ["IndQ"] * 6, "fon": [None] * (n_ + 6)}, index=[f"S{i}" for i in range(n_)] + ["LONE"] + [f"Q{i}" for i in range(5)])
Sm, Nm, _ = TS["ts_sepet"](Rm, Hm, T)
spym = pd.Series(100.0, index=gix)
okS = Nm["IndS"] >= T.min_uye
_, bS = TS["ts_erken"](TS["ts_endeks"](Sm["IndS"] / Nm["IndS"]), spym, okS, T)
d0 = bS[bS].index.min(); i0 = gix.get_loc(d0)
tt = pd.DataFrame({"sembol": ["S0.AM", "S0.AM", "S1.AM", "YOK.AM", "LONE.AM", "Q0.AM"],
                   "kirilim": [gix[i0], gix[i0 + 20], gix[i0 + 21], gix[i0 + 5], gix[412], gix[412]], "getiri": [1.0] * 6})
Et = TS["ts_etiketle"](tt, Hm, Rm, Sm, Nm, spym, T)
chk("başlangıç günü kırılım -> lider", Et["lider"].iloc[0] is True)
chk("20. gün lider, 21. gün değil", Et["lider"].iloc[1] is True and Et["lider"].iloc[2] is False)
chk("sepeti olmayan -> dışarıda (None)", Et["lider"].iloc[3] is None)
_, bQ = TS["ts_erken"](TS["ts_endeks"](Sm["IndQ"] / Nm["IndQ"]), spym, Nm["IndQ"] >= T.min_uye, T)
chk("kendi sıçraması: tam sepette işaret yanıyor AMA kendisi çıkarılınca lider DEĞİL", bool(bQ.iloc[:413].any()) and Et["lider"].iloc[4] is False,
    f"tam sepet {bool(bQ.iloc[:413].any())} · LONE {Et['lider'].iloc[4]}")
chk("aynı günde aynı sepetteki diğer hisse için de (LONE hâlâ içinde) işaret görülür", Et["lider"].iloc[5] is True)
chk("sütunlar: tema = lider, buyuk", Et["tema"].tolist() == Et["lider"].tolist() and "buyuk" in Et)

print("T5 fon kontrolü")
P5 = pd.DataFrame({"SPY": 100.0, "SMH": pd.Series(base * 100, index=gix)}, index=gix)
H5 = pd.DataFrame({"fon": ["SMH", None]}, index=["S0", "Q0"])
lf = TS["ts_etiketle_fon"](pd.DataFrame({"sembol": ["S0.AM", "Q0.AM", "S0.AM"], "kirilim": [gix[i0 + 3], gix[i0 + 3], gix[i0 + 40]]}), H5, P5, T)
chk("fon işareti: pencerede True, fonsuz None, geç False", lf.tolist() == [True, None, False], str(lf.tolist()))

print("T6 gecikme + eğri")
gix = pd.bdate_range("2018-01-01", periods=700)
J = np.full(700, 100.0); J[350:380] = np.linspace(100, 95, 30); J[380:] = 95 * 1.004 ** np.arange(320)
dip = gix[379]
S6 = pd.DataFrame({"IndJ": pd.Series(J, index=gix).pct_change().fillna(0) * 6}, index=gix); N6 = pd.DataFrame({"IndJ": 6}, index=gix)
B = TS["ts_bolumler"](S6, N6, pd.Series(100.0, index=gix), T)
Ij = pd.Series(J, index=gix)
dg = next(gix[i] for i in range(260, 700) if (J[i] / J[i - 60] - 1) * 100 >= 15 and J[i] > J[i - 199:i + 1].mean())
chk("tek dalga; dip ve dalga günü bağımsız hesapla aynı", len(B) == 1 and B["dip"].iloc[0] == dip.date() and B["dalga_gunu"].iloc[0] == dg.date(),
    f"{B[['dip', 'dalga_gunu']].to_dict('records')} · beklenen {dip.date()} / {dg.date()}")
chk("dipten dalgaya gün sayısı doğru; erken işaret dalgadan önce", B["gun_dip_dalga"].iloc[0] == gix.get_loc(dg) - 379 and 0 < B["gun_dip_erken"].iloc[0] < B["gun_dip_dalga"].iloc[0])
te = pd.DataFrame({"endustri": ["IndJ", "IndJ", "IndJ", None, "IndJ"], "kirilim": [gix[379 + 15], gix[379], gix[379 + 130], gix[400], gix[300]]})
eg = TS["ts_egri_etiket"](te, B, gix).tolist()
chk("dilimler: 15g→10–20, 0g→0–10, 130g→120–250, sepetsiz/önce→yok", eg == ["10–20", "0–10", "120–250", TS["TS_YOK"], TS["TS_YOK"]], str(eg))

print("T7 çöl durumu")
ns7 = {"col_segment": _fx.get("_yok") or (lambda x: {"uzunluk": 30, "yukseklik_atr": 2.0, "tavan": 10.0}), "AL_PAY": 1.002}
d7 = pd.DataFrame({"Open": 10.0, "High": 10.0, "Low": 9.9, "Close": 9.95, "Volume": 1.0}, index=pd.bdate_range("2024-01-01", periods=80))
chk("bantta, kırılmamış -> True", TS["ts_col_durum"](d7, ns7) is True)
d7b = d7.copy(); d7b.iloc[-1, 3] = 10.5
chk("tavan×1.002 üstünde (kırılmış) -> False", TS["ts_col_durum"](d7b, ns7) is False)
chk("col_segment yok -> None", TS["ts_col_durum"](d7, {}) is None)

# ------------------------------------------------------------------------------------------ uçtan uca sentetik dünya
IXW = pd.bdate_range("2016-01-04", "2026-09-25")
def dunya(td, etki, tohum, n_islem=600, veri_bas=None):
    r = np.random.default_rng(tohum); n = len(IXW)
    spy = 100 * np.exp(np.cumsum(r.normal(0.0003, 0.008, n)))
    VERI, H, ruzgar = {}, [], {}
    for g in range(10):
        f = np.cumsum(r.normal(0.0002, 0.003, n))
        basla = sorted(r.choice(np.arange(300, n - 60), 10, replace=False)); ruzgar[g] = [IXW[b] for b in basla]
        for b in basla:
            f[b:] += np.r_[np.linspace(0, 0.17, 25), np.full(n - b - 25, 0.17)][: n - b]
        if g == 0:                                              # bugün taze rüzgâr
            b = n - 12; f[b:] += np.linspace(0, 0.08, n - b); ruzgar[g].append(IXW[b])
        endu = "Semiconductors" if g == 0 else f"Ind{g}"
        for j in range(8):
            c = spy * np.exp(f + np.cumsum(r.normal(0, 0.004, n)))
            if g == 0 and j == 7:
                c[-40:] = c[-41] * (1 + r.normal(0, 0.0005, 40))    # çölünü kurmuş, kırılmamış üye
            d = pd.DataFrame({"Open": c, "High": c * 1.005, "Low": c * 0.995, "Close": c, "Volume": 1e5}, index=IXW)
            if veri_bas is not None:
                d = d[d.index >= veri_bas]
            VERI[f"G{g}S{j}.AM"] = d
            H.append({"sembol": f"G{g}S{j}.AM", "sektor": "Technology", "endustri": endu})
    for j in range(3):                                           # endüstrisi bilinmeyen
        c = spy * np.exp(np.cumsum(r.normal(0, 0.004, n)))
        VERI[f"U{j}.AM"] = pd.DataFrame({"Open": c, "High": c, "Low": c, "Close": c, "Volume": 1e5}, index=IXW)
        H.append({"sembol": f"U{j}.AM", "sektor": "BILINMIYOR", "endustri": "BILINMIYOR"})
    P = pd.DataFrame({f_: spy * np.exp(np.cumsum(r.normal(0, 0.002, n))) for f_ in FONLAR if f_ != "SPY"}, index=IXW); P["SPY"] = spy
    os.makedirs(os.path.join(td, "arsiv/desen"), exist_ok=True)
    open(os.path.join(td, "COL_v1.py"), "w").write(COL_V1); open(os.path.join(td, "OLCUM.py"), "w").write(OLCUM)
    open(os.path.join(td, "arsiv/desen/DESEN_TAM.py"), "w").write(DESEN)
    shutil.copy(os.path.join(D0, "tema_col.py"), os.path.join(td, "tema_col.py"))
    pd.DataFrame(H).to_csv(os.path.join(td, "sektor_ABD.csv"), index=False)
    # etiket için sepetleri modülün kendi fonksiyonlarıyla (işlem getirisi etikete göre ekilir)
    Cw = TS["ts_kapanis"]({k: v for k, v in VERI.items()}); Rw = TS["ts_getiri"](Cw)
    Hw = pd.DataFrame(H).assign(sembol=lambda x: x.sembol.str[:-3]).set_index("sembol")
    Sw, Nw, _ = TS["ts_sepet"](Rw, Hw, T); spyw = pd.Series(spy, index=IXW)
    setler, liderler = {}, {}
    tcm = modul_yukle(os.path.join(td, "tema_col.py"), f"tc_w{tohum}")
    for ad, (b0, b1) in (("ABD 2024-26", ("2024-01-02", "2026-03-01")), ("ABD 2022-23", ("2022-01-03", "2023-10-01"))):
        gun = pd.bdate_range(b0, b1); sem = [f"G{r.integers(0, 10)}S{r.integers(0, 8)}.AM" if r.random() > 0.03 else f"U{r.integers(0, 3)}.AM" for _ in range(n_islem)]
        kir = [gun[r.integers(0, len(gun))] for _ in range(n_islem)]
        et = TS["ts_etiketle"](pd.DataFrame({"sembol": sem, "kirilim": kir, "getiri": 0.0}), Hw, Rw, Sw, Nw, spyw, T)
        OB = []
        for s, k, l in zip(sem, kir, et["lider"]):
            gt = float(r.normal(6, 12) + (etki if l is True else 0.0))
            OB.append(ob_kayit(s, k - pd.offsets.BDay(1), gt, r))
        setler[ad] = OB; liderler[ad] = (et, ruzgar)
        pickle.dump(OB, open(os.path.join(td, tcm.TC_TABAN[ad]["dosya"]), "wb"))
    return VERI, P, setler, liderler, tcm

def indirici(VERI, sayac=None):
    """yfinance ikamesi: sentetik dünyanın kapanışlarını parti parti verir (sayac: çağrılan sembol sayısı)."""
    Cf = {k[:-3] if k.endswith(".AM") else k: v["Close"] for k, v in VERI.items()}
    def f(liste, bas):
        if sayac is not None: sayac.append(len(liste))
        return pd.DataFrame({x: Cf[x][Cf[x].index >= pd.Timestamp(bas)] for x in liste if x in Cf})
    return f

def calistir(td, VERI, P, setler, tcm, beklenen=None, dosyadan=False, sayac=None):
    ns = tcm.tc_yukle(td)
    if beklenen is None:
        beklenen = {ad: {"kazanan": 100 * float((tcm.tc_islemler(ns, OB)["getiri"] > 0).mean()),
                         "bek": float(ns["bek"](tcm.tc_islemler(ns, OB)["getiri"]))} for ad, OB in setler.items()}
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        if dosyadan:                                         # Drive'daki gerçek biçim: {"kayit": ..., "veri": {...}}
            pickle.dump({"kayit": "2026-09-17", "veri": VERI}, open(os.path.join(td, "veri_1d_america.pkl"), "wb"))
            return TS["tema_sepet"](K=td, P=P, setler=setler, beklenen=beklenen, yfinance_ile=False, n_boot=200, tc=tcm,
                                    indir=indirici(VERI, sayac), fiyat_bas="2016-01-01")
        return TS["tema_sepet"](K=td, VERI=VERI, P=P, setler=setler, beklenen=beklenen, yfinance_ile=False, n_boot=200, tc=tcm,
                                indir=indirici(VERI, sayac), fiyat_bas="2016-01-01")

print("T8 uçtan uca")
with tempfile.TemporaryDirectory() as td:
    VERI, P, setler, lid, tcm = dunya(td, 25, 11)
    et, ruz = lid["ABD 2024-26"]
    li = et[et["lider"] == True]
    yakin = [any(0 <= (k - w).days <= 70 for w in ruz[int(s[1])]) for s, k in zip(li["sembol"], pd.to_datetime(li["kirilim"]))]
    chk("etiket bağımsız doğrulama: lider kırılımların ≥ %80'i ekilmiş rüzgâr başlangıcından sonraki 70 gün içinde",
        np.mean(yakin) >= 0.8 and len(li) >= 25, f"n lider {len(li)} · yakın %{100 * np.mean(yakin):.0f}")
    # kuralın BAĞIMSIZ yeniden hesabı (düz döngü, pandas rolling yok): 40 işlem
    Cw = pd.DataFrame({k[:-3]: v["Close"] for k, v in VERI.items()}); Rw = Cw.pct_change()
    spyv = P["SPY"].reindex(Cw.index).ffill().to_numpy(); esit = 0; say = 0
    for s_, k_, l_ in list(zip(et["sembol"], pd.to_datetime(et["kirilim"]), et["lider"]))[:40]:
        if l_ is None: continue
        n0 = s_[:-3]; uy = [c for c in Cw.columns if c.startswith(n0[:2] + "S") and c != n0]
        ik = Cw.index.get_loc(k_); b = Rw[uy].mean(axis=1).fillna(0).to_numpy(); I_ = np.cumprod(1 + b)
        def isr(i): return i >= 219 and ((I_[i] / I_[i - 20] - 1) - (spyv[i] / spyv[i - 20] - 1)) * 100 >= 5 and I_[i] > I_[i - 199:i + 1].mean()
        bas_ = [i for i in range(ik - 20, ik + 1) if isr(i) and not any(isr(j) for j in range(i - 20, i))]
        esit += (len(bas_) > 0) == l_; say += 1
    chk("lider etiketi, kuralın düz döngüyle bağımsız hesabıyla birebir (40 işlem)", esit == say and say >= 30, f"{esit}/{say}")
    R8 = calistir(td, VERI, P, setler, tcm, dosyadan=True)
    J = json.load(open(os.path.join(td, "tema_sepet.json")))
    chk("ekilmiş +25 rüzgâr etkisi -> GEÇTİ", J["karar"] == "GEÇTİ", str(J.get("neden")))
    chk("dosyalar", all(os.path.exists(os.path.join(td, f)) for f in ("tema_sepet.txt", "tema_sepet.json", "tema_sepet_islemler.csv",
                                                                     "tema_sepet_gecikme.csv", "tema_sepet_bugun.csv", "tema_sepet_egri.png", "tema_sepet_sepet.pkl")))
    oz = R8["ozet"]
    chk("rapor bölümleri", all(x in oz for x in ("ADIM 0 GEÇTİ", "SEPETLER", "BİLGİ 1", "KARAR — LİDER", "KONTROL", "BİLGİ 2", "BUGÜN")))
    Ti = pd.read_csv(os.path.join(td, "tema_sepet_islemler.csv"))
    chk("endüstrisi bilinmeyen U* dışarıda", Ti[Ti.sembol.str.startswith("U")]["lider"].isna().all() and (Ti.sembol.str.startswith("U")).any())
    chk("damga: tanım v2 + gerekçe + tema_col md5", J["tanim"]["surum"] == "v2" and len(J["tanim"]["revizyon_gerekce"]) > 20 and len(J["tema_col_md5"]) == 32)
    bg = pd.read_csv(os.path.join(td, "tema_sepet_bugun.csv"))
    chk("BUGÜN: taze rüzgârlı sepet listede ve çölünü kurmuş üye (G0S7) gösteriliyor",
        "Semiconductors" in set(bg.endustri) and "G0S7" in str(bg.set_index("endustri").loc["Semiconductors", "col_kuranlar"]), bg.to_string()[:300])
    chk("gecikme tablosu dolu, erken işaret çoğunlukla dalgadan önce", len(R8["gecikme"]) > 20 and R8["gecikme"]["gun_dip_erken"].notna().mean() > 0.5)
    # önbellek: ikinci çalıştırma aynı sonucu verir
    say2 = []
    R8b = calistir(td, VERI, P, setler, tcm, sayac=say2)
    chk("ikinci çalıştırmada fiyat yeniden İNDİRİLMEDİ (önbellek)", sum(say2) == 0, str(say2))
    chk("sepet önbelleğiyle ikinci çalıştırma aynı karar ve aynı etiketler",
        json.load(open(os.path.join(td, "tema_sepet.json")))["karar"] == J["karar"] and
        all(R8b["islemler"][a]["lider"].tolist() == R8["islemler"][a]["lider"].tolist() for a in R8["islemler"]))
    kotu = {a: {"kazanan": 99.0, "bek": 0.0} for a in setler}
    R8c = calistir(td, VERI, P, setler, tcm, beklenen=kotu)
    chk("Adım 0 tutmazsa DURUR", "DURULDU" in R8c["ozet"] and "KARAR — LİDER" not in R8c["ozet"])
with tempfile.TemporaryDirectory() as td:
    VERI, P, setler, lid, tcm = dunya(td, 25, 12, n_islem=200, veri_bas=pd.Timestamp("2021-06-01"))
    R8d = calistir(td, VERI, P, setler, tcm)
    chk("veri ilk kırılımlar için SMA200'e yetmiyorsa DURUR", "DURULDU" in R8d["ozet"] and "KARAR — LİDER" not in R8d["ozet"])

print("T8b plasebo (etki 0, 3 dünya)")
kararlar = []
for toh in (21, 22, 23):
    with tempfile.TemporaryDirectory() as td:
        VERI, P, setler, lid, tcm = dunya(td, 0, toh)
        calistir(td, VERI, P, setler, tcm)
        kararlar.append(json.load(open(os.path.join(td, "tema_sepet.json")))["karar"])
chk("plasebo: 3 dünyada da GEÇMEDİ", all(k == "GEÇMEDİ" for k in kararlar), str(kararlar))

print("T9 çakışma kapısı (Colab gibi tek ad alanı: önce tema_col, sonra tema_sepet, sonra tekrar)")
g = {"__name__": "__main__"}
try:
    with redirect_stdout(io.StringIO()):
        exec(open(os.path.join(D0, "tema_col.py"), encoding="utf-8").read(), g)
        exec(open(os.path.join(D0, "tema_sepet.py"), encoding="utf-8").read(), g)
        exec(open(os.path.join(D0, "tema_sepet.py"), encoding="utf-8").read(), g)
    chk("birlikte ve tekrar yükleme", True)
except RuntimeError as e:
    chk("birlikte ve tekrar yükleme", False, str(e))
g["_CK_KAYIT"]["ts_etiketle"] = "baska_dosya.py"          # başka bir dosya bu adı sahiplenmiş olsun
try:
    with redirect_stdout(io.StringIO()):
        exec(open(os.path.join(D0, "tema_sepet.py"), encoding="utf-8").read(), g)
    chk("başka dosyanın adını ezince yakalanır", False)
except RuntimeError as e:
    chk("başka dosyanın adını ezince yakalanır", "ts_etiketle" in str(e), str(e)[:80])
print(f"\n{'=' * 60}\n  SONUÇ: {len(HATA)} hata" + (f" -> {HATA}" if HATA else "  — hepsi geçti"))
