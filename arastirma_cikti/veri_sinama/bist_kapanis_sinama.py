"""BIST kapanis sapmasi: Yahoo (yfinance ham, V_BIST) vs Is Yatirim acik uc (resmi, ham fiyat).
Girdi: /tmp/kasa/acik/V_BIST.pkl (<=2023-12-29), goz_pencereler.json. Dis istek: Is Yatirim HisseTekil + Yahoo; bitis <= 2023-12-29;
istekler arasi >= 1 sn; genel istemci. Cikti: bist_kapanis_sinama.json (fiyat serisi yok). Onbellek: ONB (repoya girmez).
Calistirma: python bist_kapanis_sinama.py"""
import json, os, pickle, random, subprocess, sys, time
import numpy as np, pandas as pd
import yfinance as yf
V_YOL = "/tmp/kasa/acik/V_BIST.pkl"
ONB = os.environ.get("SINAMA_ONB", "/tmp/claude-0/sc/onb_bist_kapanis.pkl")
SEED = 20261122
BAS, SON = "04-01-2016", "29-12-2023"
BOL = os.path.dirname(os.path.abspath(__file__))
PDF5 = ["BURCE", "LIDFA", "AVHOL", "TRMET", "ENJSA"]
IY = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse=%s&startdate=%s&enddate=%s"
def log(*a): print(*a, flush=True)
def resmi(kod, bas=BAS, son=SON):
    u = IY % (kod, bas, son)
    for _ in range(3):
        try:
            r = subprocess.check_output(["curl", "-s", "-m", "90", u]); j = json.loads(r)
            if j.get("ok"): v = j["value"]; break
        except Exception as e: log("  istek hata", kod, e)
        time.sleep(2)
    else: return None
    if not v: return None
    d = pd.DataFrame(v)
    d["Date"] = pd.to_datetime(d["HGDG_TARIH"], format="%d-%m-%Y")
    d = d.set_index("Date").sort_index()
    return d[["HG_KAPANIS", "HG_MIN", "HG_MAX", "HG_AOF", "HG_HACIM", "HGDG_KAPANIS"]].astype(float)
def yahoo(kod):
    t = yf.Ticker(kod + ".IS")
    h = t.history(start="2015-12-15", end="2023-12-30", auto_adjust=False, actions=True)
    if h is None or len(h) == 0: return None
    h.index = h.index.tz_localize(None).normalize()
    return h[["Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits"]].astype(float)
def indir(kodlar):
    on = pickle.load(open(ONB, "rb")) if os.path.exists(ONB) else {}
    for k in kodlar:
        if k in on: continue
        o = resmi(k); time.sleep(1.1)
        y = yahoo(k) if o is not None else None; time.sleep(1.1)
        on[k] = (o, y); pickle.dump(on, open(ONB, "wb")); log("indirildi", k, None if o is None else len(o), None if y is None else len(y))
    return on
def ozet_oran(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) == 0: return {}
    q = np.quantile(x, [.01, .05, .25, .5, .75, .95, .99])
    return {"n": int(len(x)), "q01": q[0], "q05": q[1], "q25": q[2], "med": q[3], "q75": q[4], "q95": q[5], "q99": q[6], "ort": float(x.mean())}
def hisse_cerceve(o, y, v):
    """Yahoo ham + resmi + V_BIST ortak cerceve; K3: iki kaynakta V>0 ve resmi hacim>0."""
    o = o[(o.HG_HACIM > 0) & (o.HG_KAPANIS > 0)].copy()
    y = y[(y.Volume > 0) & (y.Close > 0)].copy()
    vv = v[(v.Volume > 0) & (v.Close > 0)].copy()
    # her kaynakta kendi onceki gunu; degisim yalniz ayni onceki gunle
    for d in (o, y, vv): d["onc"] = d.index.to_series().shift(1)
    o["o_chg"] = o.HGDG_KAPANIS.pct_change() * 100
    y["y_chg"] = y.Close.pct_change() * 100
    vv["v_chg"] = vv.Close.pct_change() * 100
    m = o.join(y, how="inner", lsuffix="_o", rsuffix="_y").join(vv[["v_chg", "onc", "Close", "Volume"]].rename(
        columns={"onc": "onc_v", "Close": "vClose", "Volume": "vVol"}), how="left")
    m = m.rename(columns={"onc_o": "onc_o", "onc_y": "onc_y"})
    m["ayni_onc"] = (m["onc_o"] == m["onc_y"])
    m["ayni_onc_v"] = m["ayni_onc"] & (m["onc_v"] == m["onc_o"])
    m["r"] = m.Close / m.HG_KAPANIS
    m["s"] = m["r"].rolling(21, center=True, min_periods=5).median()
    m["f"] = m.HG_KAPANIS / m.HGDG_KAPANIS
    fadim = (m["f"] / m["f"].shift(1) - 1).abs() > 0.005
    spl = (m["Stock Splits"] > 0)
    yak = lambda s: s | s.shift(1, fill_value=False) | s.shift(-1, fill_value=False) | s.shift(2, fill_value=False) | s.shift(-2, fill_value=False)
    m["olay2"] = yak(fadim.fillna(False)) | yak(spl)
    ra = m["r"]; ort_on = ra.rolling(6, min_periods=3).median().shift(1); ort_son = ra[::-1].rolling(6, min_periods=3).median()[::-1]
    adim = (ort_son / ort_on - 1).abs() > 0.03
    m["fark"] = m["y_chg"] - m["o_chg"]
    m["ayar"] = (m["olay2"] | adim.fillna(False)) & (m["fark"].abs() > 2)
    m["ayar_pen"] = m["olay2"] | adim.fillna(False)
    m["ayar_pen"] = m["ayar_pen"] | m["ayar_pen"].shift(1, fill_value=False) | m["ayar_pen"].shift(-1, fill_value=False) | \
        m["ayar_pen"].shift(2, fill_value=False) | m["ayar_pen"].shift(-2, fill_value=False) | m["ayar_pen"].shift(3, fill_value=False) | m["ayar_pen"].shift(-3, fill_value=False)
    return m
def payl(f):
    return {"n": int(len(f)), "gt05": float((f > .5).mean()), "gt1": float((f > 1).mean()), "gt2": float((f > 2).mean())} if len(f) else {"n": 0}
def main():
    V = pickle.load(open(V_YOL, "rb"))
    rng = random.Random(SEED)
    uygun = sorted(k for k, d in V.items() if k not in PDF5 and (d.index >= "2016-01-04").sum() >= 1500 and d.index[-1] >= pd.Timestamp("2023-12-20"))
    aday = rng.sample(uygun, len(uygun))
    kodlar = list(PDF5); atlanan = []
    on = indir(PDF5)
    idx = 0; secilen25 = []
    while len(secilen25) < 25 and idx < len(aday):
        k = aday[idx]; idx += 1
        on = indir([k]); o, y = on[k]
        if o is None or y is None or len(o) < 1000: atlanan.append(k); continue
        secilen25.append(k)
    kodlar += secilen25
    log("sec:", kodlar, "atlanan:", atlanan)
    # 19.07.2019 BURCE ve cevresi
    ornek = None
    cer = {}
    for k in kodlar:
        o, y = on[k]
        if o is None or y is None: cer[k] = None; continue
        cer[k] = hisse_cerceve(o, y, V[k])
    b = cer["BURCE"].loc["2019-07-15":"2019-07-24"]
    ornek = []
    for t, r in b.iterrows():
        ornek.append({"tarih": t.strftime("%d.%m.%Y"), "resmi_kapanis_ham": r.HG_KAPANIS, "resmi_min_ham": r.HG_MIN, "resmi_max_ham": r.HG_MAX,
                      "resmi_ort_fiyat_ham": r.HG_AOF, "resmi_hacim_TL": r.HG_HACIM, "resmi_degisim_pct": None if pd.isna(r.o_chg) else round(r.o_chg, 2),
                      "yahoo_ham_acilis": r.Open, "yahoo_ham_yuksek": r.High, "yahoo_ham_dusuk": r.Low, "yahoo_ham_kapanis": r.Close,
                      "yahoo_hacim": r.Volume, "yahoo_degisim_pct": None if pd.isna(r.y_chg) else round(r.y_chg, 2),
                      "olcek_s": r.s, "resmi_hacim_hisse_yahoo_birim": r.HG_HACIM / r.HG_AOF / r.s, "V_BIST_kapanis": r.vClose, "V_BIST_degisim_pct": None if pd.isna(r.v_chg) else round(r.v_chg, 2)})
    # ---- olcek analizleri
    S = {}; tum = []
    for k in kodlar:
        m = cer[k]
        if m is None: continue
        m = m.copy(); m["kod"] = k; m["yil"] = m.index.year
        tum.append(m)
    T = pd.concat(tum)
    gecerli_chg = T[T.ayni_onc & T.fark.notna()]
    ayar_say = int((gecerli_chg.ayar).sum())
    G = gecerli_chg[~gecerli_chg.ayar]           # Yahoo ham vs resmi
    Gv = T[T.ayni_onc_v & T.v_chg.notna() & T.o_chg.notna()].copy()
    Gv["fark_v"] = Gv.v_chg - Gv.o_chg
    Gv["v_y_uyumsuz"] = (Gv.v_chg - Gv.y_chg).abs() > 0.2
    Gv = Gv[~Gv.ayar]
    Gv_ok = Gv[~Gv.v_y_uyumsuz]
    S["chg_gun_karsilastirilan"] = int(len(gecerli_chg)); S["ayar_gunu_hariç"] = ayar_say
    S["yahoo_ham_vs_resmi"] = payl(G.fark.abs())
    S["V_BIST_vs_resmi_hepsi"] = payl(Gv.fark_v.abs())
    S["V_BIST_vs_resmi_temettu_hariç"] = payl(Gv_ok.fark_v.abs()); S["V_BIST_vs_Yahoo_ham_uyumsuz_gun_payi"] = float(Gv.v_y_uyumsuz.mean()); S["V_BIST_uyumsuz_gun_n"] = int(Gv.v_y_uyumsuz.sum())
    S["yil_yahoo_ham_vs_resmi"] = {int(y): payl(g.fark.abs()) for y, g in G.groupby("yil")}
    S["yil_V_BIST_temettu_hariç"] = {int(y): payl(g.fark_v.abs()) for y, g in Gv_ok.groupby("yil")}
    S["hisse"] = {k: payl(g.fark.abs()) for k, g in G.groupby("kod")}
    S["fark_isaretli_yahoo_ham_eksi_resmi_pct_puan"] = ozet_oran(G.fark)
    S["fark_isaretli_V_BIST_eksi_resmi"] = ozet_oran(Gv_ok.fark_v)
    # (b) kapanis seviyesi: Yahoo kapanis / s / resmi kapanis
    L = T[~T.ayar_pen & T.s.notna()].copy()
    L["dev"] = (L.r / L.s - 1) * 100
    L["tik_esit"] = L.dev.abs() < 0.2
    S["kapanis_seviye_fark_pct"] = ozet_oran(L.dev)
    S["kapanis_seviye_esit_payi_abs<0.2"] = float(L.tik_esit.mean()); S["kapanis_seviye_yahoo_buyuk"] = float((L.dev > 0.2).mean()); S["kapanis_seviye_yahoo_kucuk"] = float((L.dev < -0.2).mean())
    S["kapanis_seviye_n"] = int(len(L))
    S["kapanis_seviye_yil"] = {int(y): {"n": int(len(g)), "esit": float((g.dev.abs() < .2).mean()), "yahoo_buyuk": float((g.dev > .2).mean()), "yahoo_kucuk": float((g.dev < -.2).mean()), "mutlak_med": float(g.dev.abs().median())} for y, g in L.groupby("yil")}
    # resmi kapanis aralik iliskisi
    L["oc_eq_low"] = (L.HG_KAPANIS <= L.HG_MIN * 1.0005); L["oc_eq_high"] = (L.HG_KAPANIS >= L.HG_MAX * 0.9995)
    L["yH"] = L.High / L.s; L["yL"] = L.Low / L.s; L["yC"] = L.Close / L.s
    tol = 0.003
    L["oc_ytas"] = (L.HG_KAPANIS > L.yH * (1 + tol)) | (L.HG_KAPANIS < L.yL * (1 - tol))
    L["yh_esit"] = (L.yH / L.HG_MAX - 1).abs() < 0.005; L["yl_esit"] = (L.yL / L.HG_MIN - 1).abs() < 0.005
    L["yc_esit"] = (L.yC / L.HG_KAPANIS - 1).abs() < 0.005
    L["yc_aralik_icinde"] = (L.yC >= L.HG_MIN * (1 - tol)) & (L.yC <= L.HG_MAX * (1 + tol))
    Lf = L.join(T[["fark", "ayni_onc"]].rename(columns={"fark": "fark2", "ayni_onc": "ayni2"})[~T.index.duplicated(keep=False)], how="left") if False else L
    Lf = Lf.copy()
    buyuk = Lf[Lf.ayni_onc & (Lf.fark.abs() > 1)]; kucuk = Lf[Lf.ayni_onc & (Lf.fark.abs() <= 0.5)]
    def aralik(g):
        return {"n": int(len(g)), "resmi_kapanis_eq_resmi_dusuk": float(g.oc_eq_low.mean()), "resmi_kapanis_eq_resmi_yuksek": float(g.oc_eq_high.mean()),
                "resmi_kapanis_yahoo_aralik_disi": float(g.oc_ytas.mean()), "yahoo_yuksek_esit_resmi_max": float(g.yh_esit.mean()), "yahoo_dusuk_esit_resmi_min": float(g.yl_esit.mean()),
                "yahoo_kapanis_esit_resmi": float(g.yc_esit.mean()), "yahoo_kapanis_resmi_aralikta": float(g.yc_aralik_icinde.mean())}
    S["aralik_tum"] = aralik(Lf); S["aralik_fark_gt1"] = aralik(buyuk); S["aralik_fark_le0.5"] = aralik(kucuk)
    S["aralik_yil"] = {int(y): aralik(g) for y, g in Lf.groupby("yil")}
    # yon: fark>1 gunlerde resmi kapanis Yahoo kapanisindan asagi mi
    S["fark_gt1_yon"] = {"resmi_alt (yahoo_chg>resmi_chg)": float((buyuk.fark > 0).mean()), "n": int(len(buyuk))}
    # (c) hacim orani
    Lh = L[(L.HG_AOF > 0)].copy()
    Lh["vr"] = (Lh.HG_HACIM / Lh.HG_AOF / Lh.s) / Lh.Volume
    S["hacim_orani_resmi_bizim"] = ozet_oran(Lh.vr)
    S["hacim_orani_pay_resmi_buyuk>1.02"] = float((Lh.vr > 1.02).mean()); S["hacim_orani_pay_resmi_kucuk<0.98"] = float((Lh.vr < 0.98).mean())
    S["hacim_orani_yil"] = {int(y): {"med": float(g.vr.median()), "q25": float(g.vr.quantile(.25)), "q75": float(g.vr.quantile(.75))} for y, g in Lh.groupby("yil")}
    # V_BIST hacmi Yahoo hamdan farkli (bolunme / temettu ayarli): oran
    Lv = L[L.vVol.notna()].copy(); Lv["vv"] = Lv.vVol / Lv.Volume; Lv["vp"] = Lv.vClose / Lv.Close
    S["V_BIST_hacim_ham_oranina_karsi_fiyat_oranina_gore_sapma"] = ozet_oran(np.log(Lv.vv * Lv.vp))
    # rejim (betimleyici: gunluk fark payi 2018-02-27'de basliyor, 2021-01-26'da bitiyor; veriden okunmus, ONKAYITLI DEGIL)
    R0, R1 = pd.Timestamp("2018-02-27"), pd.Timestamp("2021-01-26")
    ic = (G.index >= R0) & (G.index <= R1)
    S["rejim_tarihleri"] = [str(R0.date()), str(R1.date())]
    S["rejim_ici_yahoo_ham_vs_resmi"] = payl(G[ic].fark.abs()); S["rejim_disi_yahoo_ham_vs_resmi"] = payl(G[~ic].fark.abs())
    icL = (Lf.index >= R0) & (Lf.index <= R1)
    S["aralik_rejim_ici"] = aralik(Lf[icL]); S["aralik_rejim_disi"] = aralik(Lf[~icL])
    S["aralik_rejim_ici_fark_gt1"] = aralik(Lf[icL & Lf.ayni_onc & (Lf.fark.abs() > 1)])
    icH = (Lh.index >= R0) & (Lh.index <= R1)
    S["hacim_orani_rejim_ici"] = ozet_oran(Lh[icH].vr); S["hacim_orani_rejim_disi"] = ozet_oran(Lh[~icH].vr)
    S["kapanis_seviye_rejim_ici"] = {"n": int(icL.sum()), "esit": float((Lf[icL].dev.abs() < .2).mean()), "yahoo_buyuk": float((Lf[icL].dev > .2).mean()), "yahoo_kucuk": float((Lf[icL].dev < -.2).mean()), "mutlak_med": float(Lf[icL].dev.abs().median()), "mutlak_q90": float(Lf[icL].dev.abs().quantile(.9))}
    # (5) 15 gunluk getiri farki
    fark15, fark15v, f15r = [], [], []
    for k in kodlar:
        m = cer[k]
        if m is None: continue
        mm = m[m.ayni_onc | True].copy()
        mm = mm.copy(); n = len(mm)
        ayar = (mm.ayar_pen | mm.ayar).values; yc = mm.Close.values; oc = mm.HGDG_KAPANIS.values; vc = mm.vClose.values
        ayarcs = np.concatenate([[0], np.cumsum(ayar)])
        # kesintisiz mi: ardisik ortak satirlar arasi bosluk <= 6 takvim gunu
        tg = mm.index.values.astype("datetime64[D]").astype(int)
        for i in range(0, n - 15, 5):
            j = i + 15
            if (tg[j] - tg[i]) > 30 or np.max(np.diff(tg[i:j + 1])) > 7: continue
            if ayarcs[j + 1] - ayarcs[i] > 0: continue
            ry = yc[j] / yc[i] - 1; ro = oc[j] / oc[i] - 1
            fark15.append((ry - ro) * 100)
            f15r.append(R0 <= mm.index[i] and mm.index[j] <= R1)
            if np.isfinite(vc[i]) and np.isfinite(vc[j]): fark15v.append(((vc[j] / vc[i] - 1) - ro) * 100)
    f15 = np.array(fark15); S["getiri15_yahoo_ham_eksi_resmi"] = {"n": int(len(f15)), "sd_pct_puan": float(f15.std()), "ort": float(f15.mean()), "mutlak_med": float(np.median(np.abs(f15))), "mutlak_q90": float(np.quantile(np.abs(f15), .9)), "mutlak_q99": float(np.quantile(np.abs(f15), .99))}
    f15v = np.array(fark15v); S["getiri15_V_BIST_eksi_resmi_temettu_dahil"] = {"n": int(len(f15v)), "sd_pct_puan": float(f15v.std()), "mutlak_med": float(np.median(np.abs(f15v))), "mutlak_q90": float(np.quantile(np.abs(f15v), .9))}
    ir = np.array(f15r, bool)
    for ad, msk in (("rejim_ici", ir), ("rejim_disi", ~ir)):
        x = f15[msk]; S["getiri15_yahoo_ham_eksi_resmi_" + ad] = {"n": int(len(x)), "sd_pct_puan": float(x.std()), "mutlak_med": float(np.median(np.abs(x))), "mutlak_q90": float(np.quantile(np.abs(x), .9)), "mutlak_q99": float(np.quantile(np.abs(x), .99))}
    # robust SD (MAD)
    S["getiri15_yahoo_ham_eksi_resmi"]["sd_robust_mad"] = float(1.4826 * np.median(np.abs(f15 - np.median(f15))))
    # getiri15 bolu-10 yil
    cikti = {"secilen_hisseler": kodlar, "tohum": SEED, "atlanan_adaylar": atlanan, "pdf5": PDF5, "ornek_BURCE_2019_07": ornek, "sonuc": S,
             "ilk_tarih_son_tarih": [str(T.index.min().date()), str(T.index.max().date())], "n_satir_toplam": int(len(T))}
    def temiz(x):
        if isinstance(x, dict): return {str(k): temiz(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)): return [temiz(v) for v in x]
        if isinstance(x, (np.floating, float)): return None if not np.isfinite(x) else float(x)
        if isinstance(x, (np.integer,)): return int(x)
        if isinstance(x, (np.bool_,)): return bool(x)
        return x
    json.dump(temiz(cikti), open(os.path.join(BOL, "bist_kapanis_sinama.json"), "w"), ensure_ascii=False, indent=1)
    log('tamam')
if __name__ == "__main__": main()
