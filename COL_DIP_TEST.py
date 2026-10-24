# =====================================================================
#  COL_DIP_TEST — D12 "dip colu" tespiti para kazandiriyor mu?   (2026-10-20, v1.0)
#
#  SORU
#    Cemal'in tarifiyle kurulan yeni col tespiti (COL_v1.col_dip: bolge + dipte + yeni dip yok + imza)
#    ayni alim/cikis kurallariyla (1) tabandan (her 20 gun zirvesi kirilimi) ve (2) eski tespitten
#    (col_segment, D7) daha iyi mi? Iki donem + ABD, trail, slot simulasyonu (CLAUDE.md test standardi).
#
#  KURAL (test = canli, takip.py ile ayni)
#    Aday: e gununde col bulunur (yalniz e'ye kadarki veri; tavan/taban o gun bilinir), uzunluk >= MIN_UZ,
#          yukseklik <= MAX_YUK ATR (col_olc ile ayni). Aday KIRILIM_EN_GEC bar bekler.
#    Atilim: kapanis > tavan * AL_PAY. Alim ERTESI GUN ACILIS (Cemal: "ilk atilim mumu gorulur, ikinci gun alinir").
#    Col bozuldu: atilimdan once kapanis < taban * (1 - TABAN_TOL) -> islem yok.
#    Cikis: %HEDEF'e (High) degince TRAIL (kapanis < SMA20 -> o kapanis), hedefsizde UFUK. bar kapanisi; maliyet %.
#    Tekil: ayni hissede ayni atilim gunu bir kez sayilir.
#    Taban: her taze 20 gun zirvesi kirilimi (kapanis > onceki 20 kapanisin en yuksegi; dun degil), ayni cikis.
#  DONEMLER (giris tarihine gore): BIST 2016-19, 2020-22, 2023, 2024-26 | ABD 2022-23, 2024-26
#
#  KURAL_MOTORU: K1 veri (BIST onbellek / yfinance, ABD yfinance)  K2 bedelsiz onarimi  K3 COL_v1 yukle
#                K4 tarama + islemler  K5 ozet + slot  K6 rapor. Her adim kendi hatasini loglar.
#  Calistirma: GitHub Actions 'Arastirma' is akisi (betik: COL_DIP_TEST.py) ya da Colab:
#    exec(open('/content/drive/MyDrive/col_tarayici/COL_DIP_TEST.py').read()); R = col_dip_test()
#  Cikti: arastirma_cikti/col_dip/ (COL_DIP_rapor.md, col_dip_ozet.csv, col_dip_islemler.csv.gz)
# =====================================================================
from __future__ import annotations

import contextlib
import io
import logging
import os
import pickle
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_CK_ONCE_CD = {k: id(v) for k, v in globals().items()}

CD_SURUM = "COL_DIP_TEST v1.1 (2026-10-24, denetim: trail ufuksuz, slot hisse basina tek + rastgele sira bandi)"
cdlog = logging.getLogger("col.diptest")
if not cdlog.handlers:
    _cd_h = logging.StreamHandler(sys.stderr)
    _cd_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s diptest: %(message)s", "%H:%M:%S"))
    cdlog.addHandler(_cd_h)
    cdlog.setLevel(logging.INFO)
    cdlog.propagate = False


@dataclass
class CDAyar:
    kok: str = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/content/drive/MyDrive/col_tarayici"
    cikti: Optional[str] = None
    veri_pkl: str = "veri_1d_turkey.pkl"
    evren_bist: str = "sektor_BIST.csv"
    evren_abd: str = "sektor_ABD.csv"
    period_bist: str = "10y"
    period_abd: str = "5y"
    abd: bool = True                 # ABD testi (yfinance ~1400 hisse, ~5 dk indirme)
    adim: int = 2                    # aday tarama adimi (bar); canli tarayici her gun bakar, bir col gunlerce aday kalir
    min_gecmis: int = 260            # taramaya baslamadan once en az bar
    kirilim_en_gec: int = 60         # aday gunu + en cok bu kadar bar atilim beklenir (takip: 60 bar)
    taban_tol: float = 0.02          # takip T6: kapanis < taban*(1-tol) -> col bozuldu
    hedef: float = 20.0
    ma: int = 20
    ufuk: int = 120
    maliyet: float = 0.4
    agir: float = -20.0              # agir kayip esigi (%)
    slot: int = 30
    eski_hisse: int = 200            # eski col_segment kiyasi icin BIST orneklemi (col_segment ~70 ms/cagri)
    eski_adim: int = 10
    eski_bas: str = "2023-01-01"
    tohum: int = 42
    donemler_bist: Tuple = (("2016-19", "2016-01-01", "2019-12-31"), ("2020-22", "2020-01-01", "2022-12-31"),
                            ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31"))
    donemler_abd: Tuple = (("ABD 2022-23", "2022-01-01", "2023-12-31"), ("ABD 2024-26", "2024-01-01", "2026-12-31"))


# ------------------------------------------------------------------ K1
def _cd_yf(semboller: List[str], ek: str, period: str, etiket: str) -> Dict[str, pd.DataFrame]:
    """yfinance toplu indirme (40'arli), kolonlar Open/High/Low/Close/Volume, tz'siz gun indeksi."""
    import yfinance as yf
    veri: Dict[str, pd.DataFrame] = {}
    t0 = time.monotonic()
    for i in range(0, len(semboller), 40):
        grup = semboller[i:i + 40]
        try:
            y = yf.download([s + ek for s in grup], period=period, interval="1d", group_by="ticker",
                            auto_adjust=False, progress=False, threads=True)
        except Exception as ex:
            cdlog.warning("K1 %s: grup indirilemedi (%s): %s", etiket, grup[0], ex)
            continue
        for s in grup:
            try:
                d = y[s + ek] if len(grup) > 1 else y
                if isinstance(d.columns, pd.MultiIndex):
                    d.columns = d.columns.get_level_values(-1)
                d = d.rename(columns=str.title)[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
                if d.index.tz is not None:
                    d.index = d.index.tz_localize(None)
                d.index = d.index.normalize()
                d = d[~d.index.duplicated(keep="last")]
                if len(d) >= 300:
                    veri[s] = d.astype(float)
            except Exception as ex:
                cdlog.debug("K1 %s: %s: %s", etiket, s, ex)
        if (i // 40) % 5 == 0:
            cdlog.info("K1 %s: %d/%d indirildi (%.0f sn)", etiket, min(i + 40, len(semboller)), len(semboller), time.monotonic() - t0)
    return veri


def cd_k1_bist(ay: CDAyar) -> Dict[str, pd.DataFrame]:
    """BIST: Actions/Drive onbellegi (veri_1d_turkey.pkl, {'kayit','veri'}) — eksik/kisa hisseler yfinance'ten.
    Onbellege YAZILMAZ (gunluk taramanin onbellegi bozulmasin)."""
    yol = os.path.join(ay.kok, ay.veri_pkl)
    veri: Dict[str, pd.DataFrame] = {}
    if os.path.exists(yol):
        try:
            p = pickle.load(open(yol, "rb"))
            veri = p.get("veri", p) if isinstance(p, dict) else {}
            veri = {k: v for k, v in veri.items() if isinstance(v, pd.DataFrame)}
            cdlog.info("K1 BIST: onbellek %d hisse", len(veri))
        except Exception as ex:
            cdlog.warning("K1 BIST: onbellek okunamadi: %s", ex)
            veri = {}
    evren = pd.read_csv(os.path.join(ay.kok, ay.evren_bist)).sembol.astype(str).str.upper().tolist()
    eksik = [s for s in evren if s not in veri or len(veri[s]) < 1500]
    if eksik:
        cdlog.info("K1 BIST: %d hisse indirilecek (%s)", len(eksik), ay.period_bist)
        veri.update(_cd_yf(eksik, ".IS", ay.period_bist, "BIST"))
    veri = {s: veri[s][["Open", "High", "Low", "Close", "Volume"]].astype(float) for s in evren if s in veri}
    if len(veri) < 100:
        raise RuntimeError(f"K1 BIST: yalniz {len(veri)} hisse — veri yetersiz")
    cdlog.info("K1 BIST: %d hisse hazir", len(veri))
    return veri


def cd_k1_abd(ay: CDAyar) -> Dict[str, pd.DataFrame]:
    ev = pd.read_csv(os.path.join(ay.kok, ay.evren_abd)).sembol.astype(str)
    sem = sorted({s[:-3] if s.upper().endswith(".AM") else s for s in ev})
    veri = _cd_yf(sem, "", ay.period_abd, "ABD")
    cdlog.info("K1 ABD: %d hisse hazir", len(veri))
    return veri


# ------------------------------------------------------------------ K2
def cd_k2_onarim(ay: CDAyar, veri: Dict[str, pd.DataFrame]) -> int:
    """bolunme_onar.py (BIST bedelsiz/bolunme) — Yahoo BIST bedelsizlerini duzeltmez."""
    y = os.path.join(ay.kok, "bolunme_onar.py")
    if not os.path.exists(y):
        cdlog.warning("K2: bolunme_onar.py yok — onarim atlandi")
        return 0
    g: Dict[str, Any] = {"__name__": "bolunme_onar_cd"}
    exec(compile(open(y, encoding="utf-8").read(), y, "exec"), g)
    n = 0
    for s in list(veri):
        try:
            ol = g["bo_bul"](veri[s])
            if ol:
                yeni, kayit = g["bo_onar"](veri[s], ol)
                if any(r["onarildi"] for r in kayit):
                    veri[s] = yeni
                    n += 1
        except Exception as ex:
            cdlog.debug("K2: %s: %s", s, ex)
    cdlog.info("K2: %d hissede bedelsiz/bolunme onarildi", n)
    return n


# ------------------------------------------------------------------ K3
def cd_k3_col(ay: CDAyar) -> Dict[str, Any]:
    """COL_v1 ayri ad alaninda (uretimdeki col_dip / col_segment ve esikler birebir)."""
    yol = os.path.join(ay.kok, "COL_v1.py")
    ns: Dict[str, Any] = {"__name__": "col_v1_diptest", "VERI": {}}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(open(yol, encoding="utf-8").read(), yol, "exec"), ns)
    for ad in ("_bolge_dizi", "_bb_genislik", "_col_dip_e", "col_segment", "MIN_UZ", "MAX_YUK", "AL_PAY"):
        if ad not in ns:
            raise RuntimeError(f"K3: COL_v1.py icinde {ad} yok")
    cdlog.info("K3: COL_v1 yuklendi | MIN_UZ %s MAX_YUK %s AL_PAY %s | DIP_KONUM %s IMZA_MIN %s",
               ns["MIN_UZ"], ns["MAX_YUK"], ns["AL_PAY"], ns.get("DIP_KONUM"), ns.get("IMZA_MIN"))
    return ns


# ------------------------------------------------------------------ K4
def _cd_islem(ay: CDAyar, al_pay: float, O, H, L, C, S20, e: int, tavan: float, taban: float) -> Optional[Dict[str, Any]]:
    """Aday (e gunu) -> atilim -> ertesi gun acilis alim -> trail/ufuk cikis. Atilim yoksa ya da col bozulduysa None."""
    n = len(C)
    b = None
    for j in range(e + 1, min(n, e + 1 + ay.kirilim_en_gec)):
        if C[j] > tavan * al_pay:
            b = j
            break
        if C[j] < taban * (1 - ay.taban_tol):
            return {"bozuldu": True}
    if b is None:
        return {"atilim_yok": True}
    return _cd_cikis(ay, O, H, C, S20, b)


def _cd_cikis(ay: CDAyar, O, H, C, S20, b: int) -> Optional[Dict[str, Any]]:
    n = len(C)
    g = b + 1
    if g >= n or not np.isfinite(O[g]) or O[g] <= 0:
        return None
    p0 = float(O[g])
    hv = None
    for k in range(g, n):     # denetim 24 Eki: trail'e ufuk uygulanmaz (uretim); eskiden hedefli islem 120. barda kesilip son bara atliyordu
        if hv is None and H[k] >= p0 * (1 + ay.hedef / 100):
            hv = k
            continue
        if hv is not None and np.isfinite(S20[k]) and C[k] < S20[k]:
            return {"b": b, "g": g, "c": k, "getiri": (C[k] / p0 - 1) * 100 - ay.maliyet, "hedef": True, "acik": False}
        if hv is None and k == g + ay.ufuk - 1:
            return {"b": b, "g": g, "c": k, "getiri": (C[k] / p0 - 1) * 100 - ay.maliyet, "hedef": False, "acik": False}
    k = n - 1
    return {"b": b, "g": g, "c": k, "getiri": (C[k] / p0 - 1) * 100 - ay.maliyet, "hedef": hv is not None, "acik": True}


def cd_k4_tara(ay: CDAyar, ns: Dict[str, Any], veri: Dict[str, pd.DataFrame], pazar: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Her hisse: dip colu adaylari (adim barda bir) + taban (taze 20 gun zirvesi kirilimi). Eski col_segment
    yalniz BIST orneklemde (eski_hisse, eski_adim, eski_bas) ve ayni orneklemde dip (dip_ornek) — elma-elma kiyas."""
    al_pay, min_uz, max_yuk = float(ns["AL_PAY"]), int(ns["MIN_UZ"]), float(ns["MAX_YUK"])
    rng = np.random.default_rng(ay.tohum)
    ornek = set(rng.choice(sorted(veri), size=min(ay.eski_hisse, len(veri)), replace=False)) if pazar == "BIST" else set()
    eski_bas = pd.Timestamp(ay.eski_bas)
    isl: List[Dict[str, Any]] = []
    aday: List[Dict[str, Any]] = []
    t0 = time.monotonic()
    for k, (s, df) in enumerate(veri.items()):
        df = df[np.isfinite(df.Close)]
        n = len(df)
        if n < ay.min_gecmis + 30:
            continue
        ix = df.index
        O, H, L, C = (df[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
        S20 = df.Close.rolling(ay.ma, min_periods=ay.ma).mean().to_numpy(float)
        D, bbw = ns["_bolge_dizi"](df), ns["_bb_genislik"](df)
        gorulen = set()

        def _kaydet(grup: str, e: int, tavan: float, taban: float, ek: Optional[Dict[str, Any]] = None):
            r = _cd_islem(ay, al_pay, O, H, L, C, S20, e, tavan, taban)
            aday.append({"pazar": pazar, "grup": grup, "sembol": s, "tarih": ix[e],
                         "sonuc": "islem" if (r and "getiri" in r) else ("bozuldu" if (r and r.get("bozuldu")) else
                                                                        ("atilim_yok" if (r and r.get("atilim_yok")) else "veri_sonu"))})
            if not r or "getiri" not in r or (grup, r["b"]) in gorulen:
                return
            gorulen.add((grup, r["b"]))
            isl.append({"pazar": pazar, "grup": grup, "sembol": s, "aday": ix[e], "atilim": ix[r["b"]], "giris": ix[r["g"]],
                        "cikis": ix[r["c"]], "bar": r["c"] - r["g"] + 1, "getiri": round(r["getiri"], 2),
                        "hedef": r["hedef"], "acik": r["acik"], **(ek or {})})

        for e in range(ay.min_gecmis, n - 1, ay.adim):
            try:
                out, _ = ns["_col_dip_e"](df, D, bbw, e, alanlar=False)
            except Exception as ex:
                cdlog.debug("K4 %s %s: %s", s, e, ex)
                out = None
            if out and out["uzunluk"] >= min_uz and out["yukseklik_atr"] <= max_yuk:
                _kaydet("dip", e, out["tavan"], out["taban"], {"uz": out["uzunluk"], "imza": out["imza"], "konum": out["konum"]})
                if s in ornek and ix[e] >= eski_bas and (e - ay.min_gecmis) % ay.eski_adim == 0:
                    _kaydet("dip_ornek", e, out["tavan"], out["taban"])
            if s in ornek and ix[e] >= eski_bas and (e - ay.min_gecmis) % ay.eski_adim == 0:
                try:
                    seg = ns["col_segment"](df.iloc[:e + 1])
                except Exception as ex:
                    cdlog.debug("K4 eski %s %s: %s", s, e, ex)
                    seg = None
                if seg and seg["uzunluk"] >= min_uz and seg["yukseklik_atr"] <= max_yuk:
                    _kaydet("eski", e, seg["tavan"], seg["taban"])
        # taban: taze 20 gun zirvesi kirilimi
        mx = pd.Series(C).shift(1).rolling(20, min_periods=20).max().to_numpy(float)
        taze = (C > mx) & ~(np.r_[False, (C > mx)[:-1]])
        for b in np.where(taze)[0]:
            if b < ay.min_gecmis or (("taban", int(b)) in gorulen):
                continue
            r = _cd_cikis(ay, O, H, C, S20, int(b))
            if r:
                gorulen.add(("taban", int(b)))
                isl.append({"pazar": pazar, "grup": "taban", "sembol": s, "aday": ix[b], "atilim": ix[b], "giris": ix[r["g"]],
                            "cikis": ix[r["c"]], "bar": r["c"] - r["g"] + 1, "getiri": round(r["getiri"], 2),
                            "hedef": r["hedef"], "acik": r["acik"]})
        if (k + 1) % 50 == 0:
            cdlog.info("K4 %s: %d/%d hisse, %d islem (%.0f sn)", pazar, k + 1, len(veri), len(isl), time.monotonic() - t0)
    cdlog.info("K4 %s: bitti — %d islem, %d aday kaydi (%.0f sn)", pazar, len(isl), len(aday), time.monotonic() - t0)
    return pd.DataFrame(isl), pd.DataFrame(aday)


# ------------------------------------------------------------------ K5
def _cd_slot(t: pd.DataFrame, slot: int, tohum: Optional[int] = None) -> Tuple[float, int, int]:
    """Sabit sermaye, esit agirlik (1/slot), giris sirasina gore; slotlar doluysa islem atlanir. -> (portfoy %, alinan, atlanan).
    Denetim 24 Eki: (1) ayni hisseye ikinci slot acilmaz (uretimde hisse bir kez tutulur); (2) cikis gunu kapanista biten islemin
    slotu o gunun acilis girisine verilmez (c >= giris dolu); (3) ayni gun girisler `tohum` verilirse rastgele siralanir (eskiden
    alfabetik: sonuc 121..144 arasi oynuyordu) — bant icin _cd_slot_bant."""
    acik: List[Tuple[pd.Timestamp, Any]] = []
    top, al, atla = 0.0, 0, 0
    sira = np.random.default_rng(tohum).random(len(t)) if tohum is not None else np.zeros(len(t))
    for r in t.assign(_sira=sira).sort_values(["giris", "_sira", "sembol"]).itertuples():
        acik = [(c, s) for c, s in acik if c >= r.giris]
        if len(acik) >= slot or any(s == r.sembol for _, s in acik):
            atla += 1
            continue
        acik.append((r.cikis, r.sembol))
        top += r.getiri / slot
        al += 1
    return top, al, atla


def _cd_slot_bant(t: pd.DataFrame, slot: int, n: int = 20) -> Tuple[float, float, float, float]:
    """Ayni gun giris sirasi n kez rastgele: (portfoy ort, std, alinan ort, atlanan ort)."""
    R = np.array([_cd_slot(t, slot, tohum=k) for k in range(n)], float)
    return float(R[:, 0].mean()), float(R[:, 0].std()), float(R[:, 1].mean()), float(R[:, 2].mean())


def cd_k5_ozet(ay: CDAyar, isl: pd.DataFrame, aday: pd.DataFrame) -> pd.DataFrame:
    sat: List[Dict[str, Any]] = []
    if isl.empty:
        return pd.DataFrame()
    for pazar, donemler in (("BIST", ay.donemler_bist), ("ABD", ay.donemler_abd)):
        for ad, bas, son in donemler:
            m = (isl.pazar == pazar) & (isl.giris >= pd.Timestamp(bas)) & (isl.giris <= pd.Timestamp(son)) & ~isl.acik
            tb = isl[m & (isl.grup == "taban")]
            tb_kaz = float((tb.getiri > 0).mean() * 100) if len(tb) else np.nan
            tb_bek = float(tb.getiri.mean()) if len(tb) else np.nan
            for grup in ("dip", "taban", "eski", "dip_ornek"):
                g = isl[m & (isl.grup == grup)]
                if g.empty:
                    continue
                kaz = float((g.getiri > 0).mean() * 100)
                port, port_sd, al, atla = _cd_slot_bant(g, ay.slot)
                al, atla = int(round(al)), int(round(atla))
                am = (aday.pazar == pazar) & (aday.grup == grup) & (aday.tarih >= pd.Timestamp(bas)) & (aday.tarih <= pd.Timestamp(son)) \
                    if not aday.empty else None
                sat.append({"donem": ad, "grup": grup, "n": len(g), "kazanan_%": round(kaz, 1),
                            "beklenti_%": round(float(g.getiri.mean()), 2), "medyan_%": round(float(g.getiri.median()), 2),
                            "agir_kayip_%": round(float((g.getiri <= ay.agir).mean() * 100), 1),
                            "hedef_%": round(float(g.hedef.mean() * 100), 1), "ort_bar": round(float(g.bar.mean()), 1),
                            "kazanan_kat_taban": round(kaz / tb_kaz, 2) if tb_kaz and np.isfinite(tb_kaz) else np.nan,
                            "beklenti_fark_taban": round(float(g.getiri.mean()) - tb_bek, 2) if np.isfinite(tb_bek) else np.nan,
                            "slot_portfoy_%": round(port, 1), "slot_sd": round(port_sd, 1), "slot_alinan": al, "slot_atlanan": atla,
                            "bozuldu_%": round(float((aday[am].sonuc == "bozuldu").mean() * 100), 1) if am is not None and am.any() else np.nan})
    return pd.DataFrame(sat)


# ------------------------------------------------------------------ K6
def cd_k6_rapor(ay: CDAyar, oz: pd.DataFrame, cikti: str) -> str:
    kol = ["donem", "grup", "n", "kazanan_%", "beklenti_%", "medyan_%", "agir_kayip_%", "hedef_%", "ort_bar",
           "kazanan_kat_taban", "beklenti_fark_taban", "slot_portfoy_%", "slot_alinan", "slot_atlanan", "bozuldu_%"]
    sat = [f"# COL DIP TESTI — {pd.Timestamp.now():%Y-%m-%d %H:%M} ({CD_SURUM})", "",
           "Kural: col (aday) -> kapanis > tavan*1.002 atilim -> ERTESI GUN ACILIS alim -> %20 hedef sonra SMA20 trail, "
           f"hedefsiz {ay.ufuk} bar; maliyet %{ay.maliyet}; atilimdan once taban kirilirsa islem yok. Tekil (hisse, atilim gunu).",
           "Gruplar: dip = yeni tespit (D12 col_dip, tum evren) · taban = her taze 20 gun zirvesi kirilimi · "
           f"eski = col_segment D7 ({ay.eski_hisse} hisselik BIST orneklemi, {ay.eski_adim} barda bir, {ay.eski_bas} sonrasi) · "
           "dip_ornek = dip, ayni orneklem ve adimla (eski ile elma-elma).", "",
           "| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
    for _, r in oz.iterrows():
        sat.append("| " + " | ".join("" if pd.isna(r.get(k)) else str(r.get(k)) for k in kol) + " |")
    d = oz[oz.grup == "dip"]
    if len(d):
        iyi = d[(d.beklenti_fark_taban > 0)]
        sat += ["", f"Ozet: dip tespiti {len(d)} donemin {len(iyi)}'inde tabandan yuksek beklenti verdi; "
                    f"kazanan orani tabanin 1.3 katini gecen donem: {int((d.kazanan_kat_taban >= 1.3).sum())}."]
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "COL_DIP_rapor.md"), "w", encoding="utf-8").write(metin)
    return metin


def col_dip_test(ay: Optional[CDAyar] = None) -> Dict[str, Any]:
    ay = ay or CDAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "col_dip")
    os.makedirs(cikti, exist_ok=True)
    t0 = time.monotonic()
    ns = cd_k3_col(ay)
    veri = cd_k1_bist(ay)
    cd_k2_onarim(ay, veri)
    isl, aday = cd_k4_tara(ay, ns, veri, "BIST")
    if ay.abd:
        try:
            va = cd_k1_abd(ay)
            if len(va) >= 100:
                i2, a2 = cd_k4_tara(ay, ns, va, "ABD")
                isl, aday = pd.concat([isl, i2], ignore_index=True), pd.concat([aday, a2], ignore_index=True)
            else:
                cdlog.warning("K1 ABD: yalniz %d hisse — ABD atlandi", len(va))
        except Exception as ex:
            cdlog.error("ABD testi dustu: %s", ex)
    oz = cd_k5_ozet(ay, isl, aday)
    oz.to_csv(os.path.join(cikti, "col_dip_ozet.csv"), index=False)
    isl[isl.grup != "taban"].to_csv(os.path.join(cikti, "col_dip_islemler.csv.gz"), index=False)
    metin = cd_k6_rapor(ay, oz, cikti)
    cdlog.info("BITTI %.0f sn -> %s", time.monotonic() - t0, cikti)
    return {"islemler": isl, "aday": aday, "ozet": oz, "rapor": metin, "cikti": cikti}


def _cakisma_kontrol_cd(_once=_CK_ONCE_CD, _dosya='COL_DIP_TEST.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_CD', '_CK_KAYIT', '_cakisma_kontrol_cd', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'io', 'time', 'pickle', 'logging', 'contextlib', 'annotations',
           'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_cd()

if __name__ == "__main__":
    R = col_dip_test()
    print(R["rapor"])
