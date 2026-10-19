# test_ruzgar_defteri.py — sahte col_tarayici + gerçek tema_col.py; ağsız (sahte indirici).
# (1) indirici: kapanış+hacim, kesilip sürme, günlük yenileme  (2) işaret 1 = tema_sepet.ts_erken ile birebir
# (3) işaret 2 yayılım ve işaret 3 hacim elle kurulmuş dünyada tam eşik  (4) kartlar: pencere, dipten işarete gün, geleceğe bakmıyor,
# süzgeç yok (1/3 de listede)  (5) karar: doğrulama, yalnız ekleme, ilk karar kalır, kart yoksa hata
# (6) karne: 20/40/60 gün olgunlaşma, sepet−SPY ve hisse−diğerleri elle hesapla aynı, EVET/HAYIR ve 1/3–3/3 kırılımı
# (7) uçtan uca günlük akış: dosyalar, kartlar.csv tekrar yazmıyor, çöl kuranlar  (8) çakışma kapısı
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
    c = x["Close"].to_numpy(float)[-30:]
    if len(c) < 30: return None
    return {"uzunluk": 30, "yukseklik_atr": float((c.max() - c.min()) / max(c.mean() * 0.01, 1e-9)), "tavan": float(c.max())}
'''
OLCUM, DESEN = _fx["OLCUM"], _fx["DESEN"]

def modul_yukle(yol, ad):
    m = types.ModuleType(ad); m.__file__ = yol; sys.modules[ad] = m
    with redirect_stdout(io.StringIO()):
        exec(compile(open(yol, encoding="utf-8").read(), yol, "exec"), m.__dict__)
    return m

RD = modul_yukle(os.path.join(D0, "ruzgar_defteri.py"), "rd_test").__dict__
TSm = modul_yukle(os.path.join(D0, "tema_sepet.py"), "ts_for_rd")
T = RD["RD_TANIM"]

def klasor(td):
    os.makedirs(os.path.join(td, "arsiv/desen"), exist_ok=True)
    open(os.path.join(td, "COL_v1.py"), "w").write(COL_V1); open(os.path.join(td, "OLCUM.py"), "w").write(OLCUM)
    open(os.path.join(td, "arsiv/desen/DESEN_TAM.py"), "w").write(DESEN)
    shutil.copy(os.path.join(D0, "tema_col.py"), os.path.join(td, "tema_col.py"))

print("T1 indirici (kapanış+hacim, kesilip sürme, günlük yenileme)")
with tempfile.TemporaryDirectory() as td:
    gx = pd.bdate_range("2024-01-01", periods=120)
    TAM = pd.DataFrame({f"H{i:03d}": 10 + np.arange(120) * 0.01 * (i + 1) for i in range(250)}, index=gx)
    HAC = pd.DataFrame({c: 1000.0 + i for i, c in enumerate(TAM.columns)}, index=gx)
    cagri = []
    def kopan(l, b):
        cagri.append(len(l))
        if len(cagri) >= 2: raise ConnectionError("koptu")
        return TAM[[x for x in l if x != "H007"]], HAC[[x for x in l if x != "H007"]]
    try:
        with redirect_stderr(io.StringIO()):
            RD["rd_fiyat_hacim"](td, list(TAM.columns), bas="2024-01-01", parti=100, indir=kopan)
        chk("kopma durdurur", False)
    except RuntimeError as e:
        chk("kopma: 2 deneme sonra 'kaldığı yerden sürer'", len(cagri) == 3 and "kaldığı yerden" in str(e))
    say = []
    def tam(l, b):
        say.append(len(l)); return TAM[[x for x in l if x != "H007"]], HAC[[x for x in l if x != "H007"]]
    with redirect_stderr(io.StringIO()):
        C1, V1, b1 = RD["rd_fiyat_hacim"](td, list(TAM.columns), bas="2024-01-01", parti=100, indir=tam)
    chk("sürme: yalnız kalan 150 indi; 249 hisse; hacim hizalı", sum(say) == 150 and C1.shape[1] == 249 and V1.shape == C1.shape
        and np.allclose(C1.values, TAM.drop(columns="H007").values) and float(V1["H001"].iloc[3]) == 1001.0 and b1["basarisiz"] == 1)
    say.clear()
    with redirect_stderr(io.StringIO()):
        RD["rd_fiyat_hacim"](td, list(TAM.columns), bas="2024-01-01", parti=100, indir=tam)
    chk("aynı gün: tekrar indirmez", sum(say) == 0)
    y = os.path.join(td, "ruzgar", "fiyat_hacim.pkl"); D = pickle.load(open(y, "rb")); D["oturum"] = str(pd.Timestamp.now() - pd.Timedelta(days=2)); pickle.dump(D, open(y, "wb"))
    with redirect_stderr(io.StringIO()):
        RD["rd_fiyat_hacim"](td, list(TAM.columns), bas="2024-01-01", parti=100, indir=tam)
    chk("2 gün eski: baştan iner (günlük veri)", sum(say) == 250)

print("T2 işaret 1 = tema_sepet.ts_erken birebir")
gx = pd.bdate_range("2018-01-01", periods=700); r = np.random.default_rng(3)
I = pd.Series(100 * np.exp(np.cumsum(r.normal(0.0005, 0.012, 700))), index=gx); spy = pd.Series(100 * np.exp(np.cumsum(r.normal(0.0003, 0.008, 700))), index=gx)
ok = pd.Series(True, index=gx)
a1, b1 = RD["rd_isaret1"](I, spy, ok, T); a2, b2 = TSm.ts_erken(I, spy, ok, TSm.TS_TANIM)
chk("işaret ve başlangıç serileri aynı", a1.equals(a2) and b1.equals(b2) and b1.sum() > 0, f"başlangıç {int(b1.sum())}")

print("T3 işaret 2 yayılım ve işaret 3 hacim (elle eşik)")
gx = pd.bdate_range("2024-01-01", periods=100); spy = pd.Series(100.0, index=gx)
def dunya2(n_iyi, n_kotu):
    C = {}
    for i in range(n_iyi): C[f"A{i}"] = pd.Series(np.r_[np.full(80, 10.0), np.linspace(10, 11, 20)], index=gx)
    for i in range(n_kotu): C[f"B{i}"] = pd.Series(np.r_[np.full(80, 10.0), np.linspace(10, 9.5, 20)], index=gx)
    return pd.DataFrame(C)
C = dunya2(6, 4); uy = list(C.columns)
y, pay, g20 = RD["rd_isaret2"](C, spy, uy, gx[-1], T)
chk("6/10 = %60 -> yayılım YANDI, tam eşik", y and abs(pay - 0.6) < 1e-9 and list(g20.index[:6]) == [f"A{i}" for i in range(6)])
C = dunya2(5, 5); y, pay, _ = RD["rd_isaret2"](C, spy, list(C.columns), gx[-1], T)
chk("5/10 = %50 -> yayılım YANMADI", not y and abs(pay - 0.5) < 1e-9)
V = pd.DataFrame({c: 100.0 for c in uy}, index=gx); V.iloc[-20:] = 130.0
y3, kat = RD["rd_isaret3"](V, uy, gx[-1], T)
chk("son 20g hacim = 1.30 × önceki 60g -> hacim YANDI, kat 1.30", y3 and abs(kat - 1.3) < 1e-9, str(kat))
V.iloc[-20:] = 129.0; y3, kat = RD["rd_isaret3"](V, uy, gx[-1], T)
chk("1.29 kat -> YANMADI", not y3 and abs(kat - 1.29) < 1e-9)
V2 = pd.DataFrame({c: 100.0 for c in uy}, index=gx); V2.iloc[-30:-10] = 130.0; V2.iloc[-10:] = 400.0   # son 10 gün aşırı hacim
y_kes = RD["rd_isaret3"](V2.iloc[:-10], uy, gx[-11], T)[1]; y_tam = RD["rd_isaret3"](V2, uy, gx[-11], T)[1]
chk("hacim geleceğe bakmıyor: gx[-11] için sonraki 10 gün eklenince sonuç değişmez", abs(y_kes - y_tam) < 1e-12 and abs(y_tam - 1.3) < 1e-9, f"{y_kes} {y_tam}")
chk("veri yetersiz (80 gün < 20+60) -> hacim yanmaz, NaN", RD["rd_isaret3"](V.iloc[:79], uy, gx[78], T) == (False, np.nan) or not RD["rd_isaret3"](V.iloc[:79], uy, gx[78], T)[0])

# ------------------------------------------------------------------ sentetik evren: 3 sepet; 'G0' 250. günden rüzgâr (3/3), 'G1' fiyat+yayılım ama hacim yok, 'G2' sakin
IX = pd.bdate_range("2023-01-02", periods=360)
def evren(tohum=5):
    r = np.random.default_rng(tohum); n = len(IX)
    spy = 100 * np.exp(np.cumsum(r.normal(0.0002, 0.006, n)))
    C, V, H = {}, {}, []
    for g in range(3):
        for j in range(8):
            f = np.cumsum(r.normal(0, 0.003, n))
            rz = np.r_[np.linspace(0, 0.14, 25), np.full(n - 250 - 25, 0.14)]
            if g == 0: f[250:] += rz
            if g == 1 and j < 6: f[250:] += rz
            c = spy * np.exp(f); s = f"G{g}S{j}"
            C[s] = c; v = np.full(n, 1e5) * (1 + 0.05 * r.random(n))
            if g == 0: v[250:] *= 1.6
            V[s] = v; H.append({"sembol": s + ".AM", "sektor": "X", "endustri": f"Ind{g}"})
    C["SPY"] = spy; V["SPY"] = np.full(n, 1e6)
    return pd.DataFrame(C, index=IX), pd.DataFrame(V, index=IX), pd.DataFrame(H)

def kur(td, tohum=5):
    klasor(td); C, V, H = evren(tohum); H.to_csv(os.path.join(td, "sektor_ABD.csv"), index=False)
    tcm = modul_yukle(os.path.join(td, "tema_col.py"), f"tc_rd{tohum}")
    VERI = {}
    for s in C.columns:
        if s == "SPY": continue
        c = C[s]; VERI[s + ".AM"] = pd.DataFrame({"Open": c, "High": c * 1.005, "Low": c * 0.995, "Close": c, "Volume": V[s]})
    d7 = VERI["G0S7.AM"]; c7 = float(d7["Close"].iloc[-41]); ix7 = d7.index[-40:]
    d7.loc[ix7, "Close"] = c7; d7.loc[ix7, "High"] = c7 * 1.001; d7.loc[ix7, "Low"] = c7 * 0.999   # G0S7 çölünü kurmuş, kırılmamış
    return C, V, H, tcm, VERI

def gun_calistir(td, C, V, tcm, VERI, gun, T_=T):
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return RD["ruzgar_gunu"](K=td, T=T_, C=C.copy(), V=V.copy(), VERI=VERI, gun=str(gun.date()), tc=tcm, yfinance_ile=False)

print("T4 kartlar")
with tempfile.TemporaryDirectory() as td:
    C, V, H, tcm, VERI = kur(td)
    Hm = H.assign(sembol=H.sembol.str[:-3]).set_index("sembol"); uy = RD["rd_sepetler"](C.drop(columns="SPY"), Hm, T)
    spy = C["SPY"]; Cx = C.drop(columns="SPY"); Vx = V.drop(columns="SPY")
    R = Cx.pct_change(fill_method=None)
    I0, ok0 = RD["rd_sepet_endeks"](R, uy["Ind0"], T); _, b0 = RD["rd_isaret1"](I0, spy, ok0, T)
    bas0 = b0[b0 & (b0.index >= IX[250])].index.min(); ib = IX.get_loc(bas0)
    K1 = RD["rd_kartlar"](Cx, Vx, spy, uy, IX[ib + 20], T)
    K2 = RD["rd_kartlar"](Cx, Vx, spy, uy, IX[ib + 21], T)
    chk("başlangıç+20. gün kartta, +21. gün değil", "Ind0" in set(K1.endustri) and "Ind0" not in set(K2.endustri), f"bas {bas0.date()}")
    k0 = K1[K1.endustri == "Ind0"].iloc[0]
    chk("Ind0: 3/3 yandı (fiyat+yayılım+hacim)", k0["yanan"] == 3 and k0["i1_fiyat"] and k0["i2_yayilim"] and k0["i3_hacim"], str(dict(k0[["i1_fiyat", "i2_yayilim", "i3_hacim"]])))
    k1 = K1[K1.endustri == "Ind1"]
    chk("Ind1: hacim yok -> 2/3 ama YİNE LİSTEDE (süzgeç yok)", len(k1) == 1 and k1.iloc[0]["yanan"] == 2 and not k1.iloc[0]["i3_hacim"])
    chk("Ind2 (sakin) kartta yok", "Ind2" not in set(K1.endustri))
    a = max(0, ib - T.dip_gun); dip_el = a + int(np.argmin(I0.iloc[a:ib + 1].to_numpy()))
    chk("dipten işarete gün elle aynı", int(k0["dipten_isarete_gun"]) == ib - dip_el and k0["dip"] == IX[dip_el].date())
    Kk = RD["rd_kartlar"](Cx.iloc[:ib + 1], Vx.iloc[:ib + 1], spy, uy, IX[ib], T)
    chk("geleceğe bakmıyor: seri başlangıç gününde kesilince de kart o gün var (kac_gun_once 0)", "Ind0" in set(Kk.endustri) and int(Kk[Kk.endustri == "Ind0"].iloc[0]["kac_gun_once"]) == 0)
    chk("önde gidenler ve kart_id", k0["onde"].startswith("G0S") and k0["kart_id"] == f"Ind0|{bas0.date()}")
    I1, ok1 = RD["rd_sepet_endeks"](R, uy["Ind1"], T); _, b1_ = RD["rd_isaret1"](I1, spy, ok1, T)
    ib1 = IX.get_loc(b1_[b1_ & (b1_.index >= IX[250])].index.min())
    ORTAK = max(ib, ib1) + 3                                      # iki sepetin de kartta olduğu gün

print("T5 karar (yalnız ekleme, ilk karar kalır)")
with tempfile.TemporaryDirectory() as td:
    C, V, H, tcm, VERI = kur(td)
    R5 = gun_calistir(td, C, V, tcm, VERI, IX[ORTAK])
    try:
        RD["rd_karar_ver"](td, "Ind0", "belki", neden="x" * 10); chk("geçersiz karar reddedilir", False)
    except ValueError: chk("geçersiz karar reddedilir", True)
    try:
        RD["rd_karar_ver"](td, "Ind0", "EVET", neden=""); chk("neden zorunlu", False)
    except ValueError: chk("neden zorunlu", True)
    try:
        RD["rd_karar_ver"](td, "YokSepet", "EVET", neden="deneme neden"); chk("kartı olmayan sepet reddedilir", False)
    except ValueError: chk("kartı olmayan sepet reddedilir", True)
    with redirect_stdout(io.StringIO()):
        s1 = RD["rd_karar_ver"](td, "Ind0", "evet", hisse="g0s3.am", neden="HBM talebi, 3/3 yandı")
    chk("karar kaydedildi: normalize (EVET, G0S3), damga, yanan 3", s1["karar"] == "EVET" and s1["hisse"] == "G0S3" and s1["yanan"] == "3" and len(s1["karar_zamani"]) >= 19)
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        s2 = RD["rd_karar_ver"](td, "Ind0", "HAYIR", neden="fikir değiştirdim")
    D = pd.read_csv(os.path.join(td, "ruzgar", "kararlar.csv"), dtype=str)
    chk("aynı kart için ikinci karar KABUL EDİLMEZ: ilk kalır, tek satır", s2["karar"] == "EVET" and len(D) == 1 and D.iloc[0]["karar"] == "EVET")
    with redirect_stdout(io.StringIO()):
        RD["rd_karar_ver"](td, "Ind1", "HAYIR", neden="hacim gelmedi, tek hisse sürüklüyor")
    D = pd.read_csv(os.path.join(td, "ruzgar", "kararlar.csv"), dtype=str)
    chk("ikinci sepet eklendi, ilk silinmedi", len(D) == 2 and set(D.endustri) == {"Ind0", "Ind1"})

print("T6 karne (olgunlaşma + elle hesap)")
with tempfile.TemporaryDirectory() as td:
    C, V, H, tcm, VERI = kur(td)
    g0 = IX[ORTAK]; gun_calistir(td, C, V, tcm, VERI, g0)
    with redirect_stdout(io.StringIO()):
        RD["rd_karar_ver"](td, "Ind0", "EVET", hisse="G0S3", neden="üç işaret birden")
        RD["rd_karar_ver"](td, "Ind1", "HAYIR", neden="hacim yok")
    Cx = C.drop(columns="SPY"); spy = C["SPY"]; Hm = H.assign(sembol=H.sembol.str[:-3]).set_index("sembol"); uy = RD["rd_sepetler"](Cx, Hm, T)
    KR19, txt19 = RD["rd_karne"](td, Cx.iloc[:ORTAK + 19 + 1], spy, uy, T)
    chk("19 gün sonra: hiçbir sütun olgun değil", KR19["sepet20"].isna().all() and "henüz" in txt19)
    KR40, txt40 = RD["rd_karne"](td, Cx.iloc[:ORTAK + 40 + 1], spy, uy, T)
    chk("40 gün sonra: sepet20/40 dolu, 60 boş", KR40["sepet40"].notna().all() and KR40["sepet60"].isna().all())
    i0 = ORTAK; j = i0 + 40; Rr = Cx.pct_change(fill_method=None)
    I0 = RD["rd_sepet_endeks"](Rr, uy["Ind0"], T)[0]
    el = ((I0.iloc[j] / I0.iloc[i0] - 1) - (spy.iloc[j] / spy.iloc[i0] - 1)) * 100
    dig = [u for u in uy["Ind0"] if u != "G0S3"]
    el_h = (Cx["G0S3"].iloc[j] / Cx["G0S3"].iloc[i0] - 1) * 100 - ((Cx[dig].iloc[j] / Cx[dig].iloc[i0] - 1) * 100).mean()
    r0 = KR40[KR40.endustri == "Ind0"].iloc[0]
    chk("sepet40 ve hisse40 elle hesapla aynı", abs(r0["sepet40"] - el) < 0.06 and abs(r0["hisse40"] - el_h) < 0.06, f"{r0['sepet40']} vs {el:.1f} · {r0['hisse40']} vs {el_h:.1f}")
    chk("Ind0 rüzgâr sürdü (≥ +5), Ind1 de sürdü (fiyat kurgusu) — karne EVET/HAYIR ve 3/3–2/3 satırları", bool(r0["surdu40"]) and "Cemal EVET" in txt40 and "Cemal HAYIR" in txt40 and "3/3 yanan" in txt40 and "2/3 yanan" in txt40, txt40)
    chk("hisse seçimi satırı", "HİSSE SEÇİMİ" in txt40)

print("T7 uçtan uca günlük akış")
with tempfile.TemporaryDirectory() as td:
    C, V, H, tcm, VERI = kur(td)
    R7 = gun_calistir(td, C, V, tcm, VERI, IX[ORTAK])
    oz = R7["ozet"]
    chk("rapor: kartlar + karne + komut ipucu", "KANIT KARTLARI" in oz and "[3/3] Ind0" in oz and "[2/3] Ind1" in oz and "KARNE" in oz and "karar_ver(" in oz)
    chk("Ind0 kartında çölünü kurmuş G0S7 görünüyor", "G0S7" in str(R7["kart"][R7["kart"].endustri == "Ind0"].iloc[0]["col_kuranlar"]))
    chk("dosyalar", all(os.path.exists(os.path.join(td, "ruzgar", f)) for f in ("kartlar.csv", "bugun.txt")))
    n1 = len(pd.read_csv(os.path.join(td, "ruzgar", "kartlar.csv")))
    gun_calistir(td, C, V, tcm, VERI, IX[ORTAK]); n2 = len(pd.read_csv(os.path.join(td, "ruzgar", "kartlar.csv")))
    gun_calistir(td, C, V, tcm, VERI, IX[ORTAK + 1]); n3 = len(pd.read_csv(os.path.join(td, "ruzgar", "kartlar.csv")))
    chk("aynı gün tekrar: kart eklenmez; ertesi gün: eklenir (tarihçe silinmez)", n2 == n1 and n3 == n1 + 2, f"{n1} {n2} {n3}")
    with redirect_stdout(io.StringIO()) as b:
        RD["karar_ver"]("Ind0", "KISMEN", neden="fiyat ve yayılım var, hikâye zayıf", K=td)
    chk("kısayol karar_ver çalışır", "kaydedildi" in b.getvalue())

print("T8 çakışma kapısı")
g = {"__name__": "__main__"}
try:
    with redirect_stdout(io.StringIO()):
        for f in ("tema_col.py", "tema_sepet.py", "ruzgar_defteri.py", "ruzgar_defteri.py"):
            exec(open(os.path.join(D0, f), encoding="utf-8").read(), g)
    chk("üçü birlikte + tekrar yükleme", True)
except RuntimeError as e:
    chk("üçü birlikte + tekrar yükleme", False, str(e))
print(f"\n{'=' * 60}\n  SONUÇ: {len(HATA)} hata" + (f" -> {HATA}" if HATA else "  — hepsi geçti"))
