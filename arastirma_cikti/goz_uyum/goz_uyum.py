"""GOZ_UYUM — GÖZ UYUM KÖR SETİ: kodun 'dip savunması' (Ş3) bayrağı Cemal'in gözüyle örtüşüyor mu?  (23 Kasım 2026)

Bu dosya ÖLÇÜM YAPMAZ (getiri yok): örneklem + grafik + mühür ve Cemal işaretledikten sonra uyum (kappa) ölçümü.
Komutlar (repo kökünden):
  python arastirma_cikti/goz_uyum/goz_uyum.py sec  [--islem 4]   Y1 ∧ Ş1 havuzu -> 40 sayfa seçimi (tohum 20261123) -> goz_uyum_anahtar.json
  python arastirma_cikti/goz_uyum/goz_uyum.py pdf                anahtar -> GOZ_UYUM_KOR.pdf (kapak + 40 kör sayfa)
  python arastirma_cikti/goz_uyum/goz_uyum.py muhur              anahtar + PDF sha256 -> GOZ_UYUM_ON_KAYIT.md (kontrol tablosu + kapı)
  python arastirma_cikti/goz_uyum/goz_uyum.py olc --cemal J.json mühür denetimi -> GOZ_UYUM_SONUC.md (J.json: {"1": "VAR", "2": "YOK", "3": "?", ...})
Veri: /tmp/kasa2/acik (V_ABD.pkl, V_AVR.pkl), /tmp/kasa/acik/V_BIST.pkl.  Kod değiştiyse çalışma zamanını yeniden başlat.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import logging
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

_CK_ONCE_GU = {k: id(v) for k, v in globals().items()}

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) if "__file__" in globals() else os.getcwd()
if KOK not in sys.path:
    sys.path.insert(0, KOK)
import GOZ_ETIKET as GE  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

gulog = logging.getLogger("goz_uyum")
if not gulog.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

GU_DIR = os.path.join(KOK, "arastirma_cikti", "goz_uyum")
GU_YOL = {"anahtar": os.path.join(GU_DIR, "goz_uyum_anahtar.json"), "pdf": os.path.join(GU_DIR, "GOZ_UYUM_KOR.pdf"),
          "onkayit": os.path.join(GU_DIR, "GOZ_UYUM_ON_KAYIT.md"), "sonuc": os.path.join(GU_DIR, "GOZ_UYUM_SONUC.md"),
          "kod": os.path.abspath(__file__) if "__file__" in globals() else "goz_uyum.py"}
GU_VERI = {"ABD": "/tmp/kasa2/acik/V_ABD.pkl", "AVR": "/tmp/kasa2/acik/V_AVR.pkl", "BIST": "/tmp/kasa/acik/V_BIST.pkl"}

GU_ESIK: Dict[str, Any] = {
    "tohum": 20261123,
    "pencere": {"ABD": [["2001-01-01", "2023-06-30"]], "AVR": [["2001-01-01", "2023-06-30"]],
                "BIST": [["2016-01-01", "2017-12-31"], ["2021-03-01", "2023-06-30"]]},
    "evren_disi_ABD": ["DBA", "DBB", "DBO", "UNG", "UNL", "UUP", "BTCW"],
    "likidite": {"ABD": {"fiyat": 2.0, "medyan_deger": 1e6}, "AVR": {"fiyat": 1.0, "medyan_deger": 1e6}, "BIST": {"fiyat": 0.0, "medyan_deger": 5e6},
                 "gun": 20, "not": "ABD $ / AVR EUR (Close x Kur) / BIST TL; medyan(Close x Volume [x Kur], son 20 bar, t dahil)"},
    "tekil_bar": 60,
    "sayfa": {"ABD": 30, "AVR": 5, "BIST": 5, "hucre": 10, "hucre_pazar": [[8, 1, 1], [8, 1, 1], [7, 1, 2], [7, 2, 1]],
              "min_gun_arasi": 30, "hisse_azami": 1},
    "gorsel": {"bar": 120, "sayfa_in": [7.5, 10.5], "dpi": 100},
    "kappa": {"B": 5000, "tohum": 20261124, "gecerli": 0.60, "kismen": 0.40},
    "model": {"ANA": "Ş3 (F2 >= -0,01)", "IKINCIL-1": "Ş5 (F4 <= 0,25)", "IKINCIL-2": "Ş3 ∧ Ş5"},
}
GU_ESIK["ikinci_adim"] = ("(bu işte YAPILMAZ) kappa < 0,60 ise: Cemal'in işaretleri hedef, anahtardaki özellikler aday; her aday için tek eşikli kural "
                          "(eşik = 40 sayfada VAR / YOK ayrımını en iyi yapan) ve ikinci bağımsız 40 sayfalık kör sette sınama; kappa >= 0,60 olmadan "
                          "getiri ölçümü yok")
GU_OZ_KOL = ["F%d" % k for k in range(1, 24)] + ["F22a"]
GU_EK_KOL = ["fitil20", "fitil40", "dip_bolge_n", "dip_bolge_fitil", "dibe_dokunus", "dokunus_egim", "hacim_dus_yuk", "low20_onceki20"]


class GUHata(RuntimeError):
    """Durdurucu hata: veri / örneklem kotası / mühür tutmadı."""


# ================================================================ ortak
def _sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _sha_esik() -> str:
    return hashlib.sha256(json.dumps(GU_ESIK, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _jyaz(yol: str, J: Any) -> None:
    def kon(o: Any) -> Any:
        if isinstance(o, (np.floating, float)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, pd.Timestamp):
            return o.strftime("%Y-%m-%d")
        raise TypeError(str(type(o)))
    metin = json.dumps(J, ensure_ascii=False, indent=1, default=kon)
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", metin):
        raise GUHata("e-posta benzeri metin yazılmaz: " + yol)
    with open(yol + ".tmp", "w", encoding="utf-8") as f:
        f.write(metin)
    os.replace(yol + ".tmp", yol)


def _yaz(yol: str, metin: str) -> None:
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", metin):
        raise GUHata("e-posta benzeri metin yazılmaz: " + yol)
    with open(yol + ".tmp", "w", encoding="utf-8") as f:
        f.write(metin)
    os.replace(yol + ".tmp", yol)


# ================================================================ 1) HAVUZ
_GU_IS: Dict[str, Any] = {}


def _gu_ek_ozellik(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, V: np.ndarray, i: int) -> Dict[str, float]:
    """Nedensel ek özellikler; yalnız [0..i] (dilimler i + 1 ile sınırlı). ÖLÇÜ DEĞİL: ileride tanım kurmak için aday."""
    O, H, L, C, V = O[:i + 1], H[:i + 1], L[:i + 1], C[:i + 1], V[:i + 1]
    out = {k: np.nan for k in GU_EK_KOL}
    af = (np.minimum(O, C) - L) / (H - L)
    if i >= 19:
        out["fitil20"] = float(np.mean(af[i - 19:i + 1]))
    if i >= 39:
        out["fitil40"] = float(np.mean(af[i - 39:i + 1]))
        l40, h40 = L[i - 39:i + 1], H[i - 39:i + 1]
        lo, hi = float(l40.min()), float(h40.max())
        band = lo + 0.20 * (hi - lo)
        m = l40 <= band
        out["dip_bolge_n"] = float(m.sum())
        out["dip_bolge_fitil"] = float(np.mean(af[i - 39:i + 1][m])) if m.any() else np.nan
        dok = np.flatnonzero(l40 <= lo * 1.015)
        out["dibe_dokunus"] = float(len(dok))
        out["dokunus_egim"] = float(l40[dok[-1]] / l40[dok[0]] - 1) if len(dok) >= 2 else np.nan
        k0 = i - 19
        dc = np.diff(C[i - 20:i + 1])
        vv = V[k0:i + 1]
        vd, vy = float(vv[dc < 0].sum()), float(vv[dc > 0].sum())
        out["hacim_dus_yuk"] = vd / vy if vy > 0 else np.nan
        out["low20_onceki20"] = float(L[i - 19:i + 1].min() / L[i - 39:i - 19].min())
    return out


def _gu_isci(semboller: List[str]) -> Dict[str, Any]:
    """Hisse başına: S6 sinyalleri (veri pencere sonunda KESİK) -> pencere + likidite + 60 bar tekil -> F1-F23 + ek özellik -> Ş1."""
    pazar = _GU_IS["pazar"]; V = _GU_IS["V"]; Eg = GU_ESIK; sat, hata = [], []
    pen = [(pd.Timestamp(a), pd.Timestamp(b)) for a, b in Eg["pencere"][pazar]]
    son = max(b for _, b in pen); lq = Eg["likidite"][pazar]; gun = int(Eg["likidite"]["gun"])
    ESG = YH.YH_ESIK["denemeler"]["Y10"]["esik"]
    for s in semboller:
        try:
            df = V[s]
            df = df[df.index <= son]                                     # sinyal çağı sonrası veri fonksiyona hiç girmez
            if len(df) < 260:
                continue
            X, _ = YH.yh_s6_hisse(df)
            if not len(X):
                continue
            d = GE.ge_hazir(df)
            kur = df["Kur"].reindex(d.index).to_numpy(float) if "Kur" in df.columns else np.ones(len(d))
            C = d["Close"].to_numpy(float); Vo = d["Volume"].to_numpy(float)
            deger = pd.Series(C * Vo * kur).rolling(gun, min_periods=gun).median().to_numpy()
            fiyat = C * kur if pazar == "AVR" else C
            tl = pd.to_datetime(X.tarih)
            pos = d.index.get_indexer(pd.DatetimeIndex(tl))
            ok = np.zeros(len(X), bool)
            for k, (t, p) in enumerate(zip(tl, pos)):
                if p < 0 or p < 130:
                    continue
                if not any(a <= t <= b for a, b in pen):
                    continue
                if not (np.isfinite(deger[p]) and deger[p] >= lq["medyan_deger"] and fiyat[p] >= lq["fiyat"]):
                    continue
                ok[k] = True
            if not ok.any():
                continue
            Xk = X[ok]; pk = pos[ok]; tk = list(pd.to_datetime(Xk.tarih))
            keep, son_p = [], -10 ** 9                                   # 60 bar tekil (aynı hissede)
            for k, p in enumerate(pk):
                if p - son_p >= int(Eg["tekil_bar"]):
                    keep.append(k); son_p = p
            Xk = Xk.iloc[keep]; pk = pk[keep]; tk = [tk[k] for k in keep]
            Fs, Bs = GE.ge_ozellik_hisse(d, tk, hazir=True)
            S7 = YH.yh_s7_ozellik(d, tk, hazir=True)
            PR = GE.ge_parmak_hisse(d, tk, hazir=True)
            O_, H_, L_ = d["Open"].to_numpy(float), d["High"].to_numpy(float), d["Low"].to_numpy(float)
            for k, (t, f, b, p) in enumerate(zip(tk, Fs, Bs, pk)):
                if abs(b["hat"] / float(Xk.hat.iloc[k]) - 1) > 1e-9:
                    hata.append(f"{s} {t.date()} hat sinyalle aynı değil")
                    continue
                F15, F17, F2, F4 = f["F15"], f["F17"], f["F2"], f["F4"]
                s1 = bool(np.isfinite(F15) and np.isfinite(F17) and F15 <= ESG["F15_ust"] and F17 <= ESG["F17_ust"])
                if not s1:
                    continue
                s3 = bool(np.isfinite(F2) and F2 >= ESG["F2_min"]); s5 = bool(np.isfinite(F4) and F4 <= ESG["F4_ust"])
                r = {"pazar": pazar, "sembol": s, "tarih": t, "pos": int(p), "S1": s1, "S3": s3, "S5": s5, **f,
                     **{c: float(S7.iloc[k][c]) for c in S7.columns}, "F19": float(PR[k]["F19"]),
                     **_gu_ek_ozellik(O_, H_, L_, C, Vo, int(p)),
                     "deger_medyan": float(deger[p]), "fiyat": float(fiyat[p])}
                sat.append(r)
        except Exception as ex:                                         # tek hisse bozuksa sayılır, sonda DURUR
            hata.append(f"{s}: {type(ex).__name__}: {str(ex)[:160]}")
    return {"sat": sat, "hata": hata}


def gu_veri(pazar: str) -> Dict[str, pd.DataFrame]:
    yol = GU_VERI[pazar]
    if not os.path.exists(yol):
        raise GUHata(f"veri yok: {yol}")
    V = pd.read_pickle(yol)
    if pazar == "ABD":
        V = {k: v for k, v in V.items() if k not in set(GU_ESIK["evren_disi_ABD"])}
    return {k: v for k, v in V.items() if isinstance(v, pd.DataFrame) and "Close" in v.columns}


def gu_havuz(pazar: str, islem: int = 4) -> pd.DataFrame:
    t0 = time.time(); V = gu_veri(pazar); S = sorted(V); k = max(1, islem * 6)
    dilim = [S[j::k] for j in range(k) if S[j::k]]
    _GU_IS.clear(); _GU_IS.update({"V": V, "pazar": pazar})
    try:
        if islem > 1:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(islem) as hv:
                R = hv.map(_gu_isci, dilim)
        else:
            R = [_gu_isci(x) for x in dilim]
    finally:
        _GU_IS.clear()
    hata = [h for r in R for h in r["hata"]]
    if hata:
        raise GUHata(f"{pazar}: {len(hata)} hisse / olayda hata (ör. {hata[:3]}) -> DURDU")
    P = pd.DataFrame([x for r in R for x in r["sat"]])
    gulog.info("%s: %d hisse, %d Y1 ∧ Ş1 olay (%.0f sn)", pazar, len(V), len(P), time.time() - t0)
    return P.sort_values(["sembol", "tarih"], kind="mergesort").reset_index(drop=True)


# ================================================================ 2) SEÇİM
def gu_sec_df(H: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, List[str]]:
    """Havuz -> 40 sayfa. Tabaka Ş3 x Ş5; hücre başına 10; hücre-pazar kotası GU_ESIK['sayfa']['hucre_pazar'] (hücre sırası tohumla karışır).
    Kısıt: aynı (pazar, sembol) en çok 1 sayfa, sinyal günleri arasında >= 30 gün (bütün sayfalar). Kota dolmazsa ABD'den tamamlanır ve yazılır."""
    Eg = GU_ESIK; rng = np.random.default_rng(int(Eg["tohum"])); notlar: List[str] = []
    hucreler = [(True, True), (True, False), (False, True), (False, False)]
    kota = [list(x) for x in Eg["sayfa"]["hucre_pazar"]]
    sira = rng.permutation(4)
    plan = {hucreler[j]: kota[int(sira[j])] for j in range(4)}           # (S3, S5) -> [ABD, AVR, BIST]
    secili: List[Dict[str, Any]] = []; kullanilan: set = set(); gunler: List[pd.Timestamp] = []
    mingun = int(Eg["sayfa"]["min_gun_arasi"])

    def al(pazar: str, h: Tuple[bool, bool], n: int) -> int:
        P = H[pazar]; m = (P.S3.to_numpy(bool) == h[0]) & (P.S5.to_numpy(bool) == h[1])
        idx = np.flatnonzero(m); idx = idx[rng.permutation(len(idx))]
        say = 0
        for j in idx:
            if say >= n:
                break
            r = P.iloc[int(j)]; key = (pazar, r.sembol)
            if key in kullanilan or any(abs((r.tarih - g).days) < mingun for g in gunler):
                continue
            kullanilan.add(key); gunler.append(r.tarih); secili.append({**r.to_dict(), "hucre_S3": h[0], "hucre_S5": h[1]}); say += 1
        return say
    for h in hucreler:
        for pi, pazar in enumerate(["ABD", "AVR", "BIST"]):
            n = plan[h][pi]; g = al(pazar, h, n)
            if g < n:
                notlar.append(f"hücre Ş3={h[0]} Ş5={h[1]} {pazar}: kota {n}, bulunan {g}")
    for h in hucreler:                                                   # eksikleri ABD'den tamamla
        eks = int(Eg["sayfa"]["hucre"]) - sum(1 for x in secili if (x["hucre_S3"], x["hucre_S5"]) == h)
        if eks > 0:
            g = al("ABD", h, eks); notlar.append(f"hücre Ş3={h[0]} Ş5={h[1]}: {eks} eksik ABD'den tamamlandı ({g})")
            if g < eks:
                raise GUHata(f"hücre {h}: 10 sayfa dolmadı")
    S = pd.DataFrame(secili)
    for pz in ("ABD", "AVR", "BIST"):
        if int((S.pazar == pz).sum()) != Eg["sayfa"][pz]:
            notlar.append(f"pazar {pz}: {int((S.pazar == pz).sum())} sayfa (hedef {Eg['sayfa'][pz]})")
    S = S.iloc[rng.permutation(len(S))].reset_index(drop=True)           # sayfa sırası rastgele (tabakaya göre değil)
    S.insert(0, "sayfa", np.arange(1, len(S) + 1))
    return S, notlar


def gu_sec(islem: int = 4) -> Dict[str, Any]:
    H = {p: gu_havuz(p, islem) for p in ("ABD", "AVR", "BIST")}
    S, notlar = gu_sec_df(H)
    havuz_ozet = {p: {"n": int(len(H[p])), "S3": int(H[p].S3.sum()), "S5": int(H[p].S5.sum()),
                      "hucre": {f"S3={a}_S5={b}": int(((H[p].S3 == a) & (H[p].S5 == b)).sum()) for a in (True, False) for b in (True, False)}}
                  for p in H}
    sayfalar = []
    for r in S.itertuples(index=False):
        d = r._asdict()
        ana = "VAR" if d["S3"] else "YOK"; ik1 = "VAR" if d["S5"] else "YOK"; ik2 = "VAR" if (d["S3"] and d["S5"]) else "YOK"
        sat = {"sayfa": int(d["sayfa"]), "pazar": d["pazar"], "sembol": d["sembol"], "sinyal_gunu": pd.Timestamp(d["tarih"]).strftime("%Y-%m-%d"),
               "S1": bool(d["S1"]), "S3": bool(d["S3"]), "S5": bool(d["S5"]), "F2": d["F2"], "F4": d["F4"],
               "model_etiketi": {"ANA": ana, "IKINCIL-1": ik1, "IKINCIL-2": ik2}, "deger_medyan": d["deger_medyan"], "fiyat": d["fiyat"]}
        for c in GU_OZ_KOL + GU_EK_KOL:
            if c in d:
                sat[c] = d[c]
        sayfalar.append(sat)
    J = {"surum": "GOZ_UYUM v1.0 (23.11.2026)", "uyari": "GİZLİ ANAHTAR: Cemal işaretlemeden önce açılmaz; mühür ON_KAYIT.md'de.",
         "esik": GU_ESIK, "esik_sha": _sha_esik(), "havuz": havuz_ozet, "notlar": notlar, "sayfalar": sayfalar}
    _jyaz(GU_YOL["anahtar"], J)
    gulog.info("anahtar yazıldı: %d sayfa; notlar: %s", len(sayfalar), notlar)
    return J


# ================================================================ 3) PDF
def _gu_pencere(pazar: str, sembol: str, t: pd.Timestamp, V: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Veri t'de KESİLİR (t sonrası fonksiyona girmez); son 120 + t."""
    df = V[sembol]; df = df[df.index <= t]
    d = GE.ge_hazir(df)
    if not len(d) or d.index[-1] != t:
        raise GUHata(f"{pazar} {sembol} {t.date()}: sinyal günü geçerli bar değil")
    if len(d) < int(GU_ESIK["gorsel"]["bar"]) + 1:
        raise GUHata(f"{pazar} {sembol} {t.date()}: 121 bar yok")
    return d.iloc[-(int(GU_ESIK["gorsel"]["bar"]) + 1):]


def gu_sayfa_ciz(W: pd.DataFrame, no: int, toplam: int):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    gw, gh = GU_ESIK["gorsel"]["sayfa_in"]
    fig = plt.figure(figsize=(gw, gh))
    n = len(W); x = np.arange(n) - (n - 1)
    O, H, L, C, V = (W[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    ax = fig.add_axes([0.04, 0.27, 0.92, 0.58]); av = fig.add_axes([0.04, 0.12, 0.92, 0.13], sharex=ax)
    yes = C >= O; renk = np.where(yes, "#1a9850", "#d73027")
    ax.vlines(x, L, H, colors=renk, linewidth=1.1, zorder=3)
    for xi, o, c, col in zip(x, O, C, renk):
        ax.add_patch(Rectangle((xi - 0.35, min(o, c)), 0.7, max(abs(c - o), (H.max() - L.min()) * 0.0008), facecolor=col, edgecolor=col, linewidth=0.4, zorder=4))
    ax.axvline(x[-1] + 0.5, color="#555555", linewidth=0.8, zorder=2)             # sinyal günü: ince dikey çizgi (mumun sağında; mumu örtmez)
    ax.axvline(x[-1] - 0.5, color="#555555", linewidth=0.8, zorder=2)
    pad = (H.max() - L.min()) * 0.04; ax.set_ylim(L.min() - pad, H.max() + pad); ax.set_xlim(x[0] - 1, x[-1] + 2)
    av.bar(x, V, width=0.7, color=renk, alpha=0.7); av.set_xlim(x[0] - 1, x[-1] + 2)
    for a in (ax, av):
        a.set_xticks([]); a.set_yticks([])
        for sp in a.spines.values():
            sp.set_linewidth(0.6); sp.set_color("#888888")
    fig.text(0.04, 0.945, f"{int(no)}", fontsize=46, fontweight="bold", va="center", ha="left")
    fig.text(0.96, 0.945, f"/ {toplam}", fontsize=16, va="center", ha="right", color="#666666")
    fig.text(0.50, 0.905, "sağdaki iki ince çizgi arası = sinyal günü", fontsize=10, ha="center", color="#666666")
    fig.text(0.50, 0.045, "☐ VAR        ☐ YOK        ☐ ?", fontsize=28, ha="center", va="center")
    return fig


def gu_pdf() -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    J = json.load(open(GU_YOL["anahtar"], encoding="utf-8")); sayfalar = J["sayfalar"]
    Vc: Dict[str, Dict[str, pd.DataFrame]] = {}
    gw, gh = GU_ESIK["gorsel"]["sayfa_in"]
    meta = {"Title": "GOZ UYUM KOR SET", "Author": "", "Creator": "", "Producer": "", "CreationDate": None, "ModDate": None}
    with PdfPages(GU_YOL["pdf"] + ".tmp", metadata=meta) as pp:
        fig = plt.figure(figsize=(gw, gh))
        fig.text(0.5, 0.78, "Soru tek:", fontsize=30, ha="center", fontweight="bold")
        fig.text(0.5, 0.70, "bu grafikte DİP SAVUNMASI var mı?", fontsize=24, ha="center")
        fig.text(0.5, 0.58, "Her sayfaya VAR ya da YOK yaz\n(emin değilsen ?).", fontsize=22, ha="center", linespacing=1.5)
        fig.text(0.5, 0.42, "Sonrası yok, hisse adı yok.", fontsize=20, ha="center")
        fig.text(0.5, 0.34, f"{len(sayfalar)} sayfa.", fontsize=20, ha="center")
        pp.savefig(fig); plt.close(fig)
        for s in sorted(sayfalar, key=lambda z: z["sayfa"]):
            p = s["pazar"]
            if p not in Vc:
                Vc[p] = gu_veri(p)
            W = _gu_pencere(p, s["sembol"], pd.Timestamp(s["sinyal_gunu"]), Vc[p])
            fig = gu_sayfa_ciz(W, s["sayfa"], len(sayfalar)); pp.savefig(fig); plt.close(fig)
    os.replace(GU_YOL["pdf"] + ".tmp", GU_YOL["pdf"])
    mb = os.path.getsize(GU_YOL["pdf"]) / 2 ** 20
    if mb >= 6:
        raise GUHata(f"PDF {mb:.1f} MB >= 6 MB")
    return {"pdf": GU_YOL["pdf"], "boyut_mb": round(mb, 2), "sayfa": len(sayfalar) + 1}


# ================================================================ 4) MÜHÜR
GU_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kodun bayrağı arasında uyum ölçülür)"),
    "K2": ("EVET", "veri sinyal çağı sonunda KESİK (df.index <= pencere sonu) ve grafik her sayfada t'de kesilerek çizilir (_gu_pencere); S6 ve F1-F23 "
                   "nedensel; ek özellikler dilim i + 1 ile sınırlı; test: goz_uyum.py testler komutu prefix değişmezliği"),
    "K3": ("EVET", "GE.ge_hazir (YAPI_HEDEF._yh_hazir = H>L, V>0, O/H/L/C>0) geçerli bar; likidite hesabı geçerli bar dizisinde; sinyal günü p >= 130"),
    "K4": ("EVET", "aynı hissede 60 bar tekil (_gu_isci), seçimde aynı (pazar, sembol) en çok 1 sayfa ve sinyal günleri arası >= 30 gün (gu_sec_df)"),
    "K5": ("UYGULANMAZ", "giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik"),
    "K6": ("EVET", "tek kip V_*.pkl (düzeltilmiş fiyat; YAPI_HEDEF ile aynı); AVR likidite Close x Kur (EUR); oranlar birimsiz; ABD evren dışı 7 fon çıkarıldı"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (hayatta kalma yanlılığı); bu iş görsel uyum sınaması, getiri iddiası yok; raporda yazılı"),
    "K8": ("EVET", "n = 40 sayfa küçük örneklem: karar n >= 30 değilse kappa 'ÖLÇÜLEMEDİ' kuralı olc'ta uygulanır; '?' karar dışı sayılır; kappa bootstrap "
                   "aralığı (B 5000) ile; hüküm eşikleri ön kayıtta sabit; dönem: ABD / AVR 2001-2023, BIST 2016-17 + 2021-23 (sapma penceresi dışı)"),
    "K9": ("EVET", "GU_ESIK sha + goz_uyum.py sha + anahtar sha + PDF sha ve hüküm kuralı ön kayıtta; bu dosya Cemal işaretlemeden ÖNCE commit; eşik sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırma yok; yalnız OHLCV"),
    "K11": ("EVET", "tohum 20261123 ile anahtar aynı komutla yeniden üretilir; olc komutu anahtardan tabloyu yeniden kurar"),
    "K12": ("EVET", "iddia yok; yalnız 'uyum' ve 'kappa' sayısı; hüküm sözü yalnız ön kayıttaki eşikle (>= 0,60 / 0,40-0,60 / < 0,40)"),
    "K13": ("EVET", "çakışma kapısı _CK_ONCE_GU + test; yasak dosyalar (defter, mevcut .py, kart / kart2 / kasa) değiştirilmedi (git status); e-posta taraması _yaz / _jyaz; "
                    "kod değiştiyse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


def _gu_git(yol: str) -> str:
    import subprocess
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%H %cI", "--", yol], cwd=KOK, capture_output=True, text=True, timeout=30)
        return r.stdout.strip() or "(henüz commit yok)"
    except Exception as ex:  # noqa: BLE001
        return f"(git okunamadı: {ex})"


def gu_muhur() -> str:
    for y in (GU_YOL["anahtar"], GU_YOL["pdf"]):
        if not os.path.exists(y):
            raise GUHata(f"mühür için dosya yok: {y}")
    J = json.load(open(GU_YOL["anahtar"], encoding="utf-8")); S = J["sayfalar"]
    tab = "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |\n|---|---|---|---|\n"
    ad = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
          "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
          "K13": "süreç", "K14": "boyut (gerçek para)"}
    for k, (y, kn) in GU_KONTROL.items():
        tab += f"| {k} | {ad[k]} | {y} | {kn} |\n"
    cap = pd.DataFrame(S)
    hucre = cap.groupby([cap.S3, cap.S5, cap.pazar]).size().to_dict()
    m = f"""# GÖZ UYUM KÖR SETİ — ÖN KAYIT (Cemal işaretlemeden ÖNCE mühürlenir)

Üretim: {_simdi()} (UTC). Soru (Cemal, 23.11.2026): kodun 'dip savunması' bayrağı (Ş3) Cemal'in gözüyle örtüşüyor mu? Bu aşama getiri ÖLÇMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/goz_uyum_anahtar.json` sha256: `{_sha(GU_YOL['anahtar'])}`
- PDF: `arastirma_cikti/goz_uyum/GOZ_UYUM_KOR.pdf` sha256: `{_sha(GU_YOL['pdf'])}`
- kod: `arastirma_cikti/goz_uyum/goz_uyum.py` sha256: `{_sha(GU_YOL['kod'])}`
- eşik sözlüğü (GU_ESIK) sha256: `{_sha_esik()}`
- iş tanımı: `arastirma_cikti/goz_uyum/GOZ_UYUM_IS_TANIMI.md` sha256: `{_sha(os.path.join(GU_DIR, 'GOZ_UYUM_IS_TANIMI.md'))}`
- bağımlı kod: GOZ_ETIKET.py `{_sha(os.path.join(KOK, 'GOZ_ETIKET.py'))[:16]}`, YAPI_HEDEF.py `{_sha(os.path.join(KOK, 'YAPI_HEDEF.py'))[:16]}`

## 2. Örneklem (tohum {GU_ESIK['tohum']})
Olay = Y1 (S6 taban kırılımı, aynı hissede 60 bar tekil) ∧ Ş1 (F15 <= 0,25 ∧ F17 <= -0,20); P2 benzeri likidite (ABD fiyat >= 2 $, 20 gün medyan işlem değeri >= 1 mn $; AVR 1 EUR / 1 mn EUR; BIST >= 5 mn TL).
Dönem: ABD / AVR 2001-01-01..2023-06-30; BIST 2016-01-01..2017-12-31 ve 2021-03-01..2023-06-30 (Yahoo BIST kapanış sapma penceresi 27.02.2018-26.01.2021 dışı).
40 sayfa: ABD 30, AVR 5, BIST 5; tabaka Ş3 x Ş5, hücre başına 10; aynı hisseden en çok 1; sinyal günleri arası >= 30 gün; sayfa sırası rastgele.
Tabaka dağılımı (Ş3, Ş5, pazar -> sayfa): {json.dumps({f'S3={a} S5={b} {c}': v for (a, b, c), v in hucre.items()}, ensure_ascii=False)}
Notlar: {json.dumps(J['notlar'], ensure_ascii=False)}

## 3. ÖLÇÜ (önceden yazılı, değişmez)
- Model etiketi (kodun yanıtı): ANA = Ş3 (VAR = F2 >= -0,01), İKİNCİL-1 = Ş5 (VAR = F4 <= 0,25), İKİNCİL-2 = Ş3 ∧ Ş5.
- Cemal'in VAR / YOK işaretleri ile her model etiketi arasında: uyum yüzdesi ve Cohen kappa (2x2: VAR / YOK); '?' karar dışı, sayısı ayrıca yazılır; kappa'nın bootstrap %95 aralığı (B {GU_ESIK['kappa']['B']}, tohum {GU_ESIK['kappa']['tohum']}, sayfa yeniden örneklemesi).
- HÜKÜM (ANA için; ikincil ikisi bilgi): kappa >= 0,60 TANIM GEÇERLİ; 0,40-0,60 KISMEN; < 0,40 TANIM GEÇERSİZ. Karar sayısı < 30 ise hüküm 'ÖLÇÜLEMEDİ' yazılır (K8).
- İKİNCİ ADIM {GU_ESIK['ikinci_adim']}.
- Eşik sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 4. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
{tab}
## 5. Git kaydı (bu dosyanın yazıldığı an; commit sonrası `git log` ile doğrulanır)
- anahtar: {_gu_git('arastirma_cikti/goz_uyum/goz_uyum_anahtar.json')}
"""
    _yaz(GU_YOL["onkayit"], m)
    import IZ_KARNE as IK
    r = IK.ik_kontrol_kapisi(GU_YOL["onkayit"])
    gulog.info("kontrol kapısı: %s", "GEÇTİ" if r["gecti"] else r)
    return GU_YOL["onkayit"]


# ================================================================ 5) ÖLÇÜM (olc)
def _gu_muhur_oku() -> Dict[str, str]:
    if not os.path.exists(GU_YOL["onkayit"]):
        raise GUHata("ön kayıt yok")
    t = open(GU_YOL["onkayit"], encoding="utf-8").read()
    out = {}
    for ad, anahtar in (("anahtar", "goz_uyum_anahtar.json"), ("pdf", "GOZ_UYUM_KOR.pdf"), ("esik", "GU_ESIK")):
        m = re.search(re.escape(anahtar) + r"[^\n]*sha256:? `([0-9a-f]{64})`", t) if ad != "esik" else re.search(r"eşik sözlüğü \(GU_ESIK\) sha256: `([0-9a-f]{64})`", t)
        if not m:
            raise GUHata(f"ön kayıtta {ad} sha'sı yok")
        out[ad] = m.group(1)
    return out


def gu_norm(x: Any) -> Optional[str]:
    if x is None:
        return None
    k = str(x).strip().replace("İ", "I").replace("ı", "I").upper()
    if k in ("VAR", "V", "EVET"):
        return "VAR"
    if k in ("YOK", "Y", "HAYIR"):
        return "YOK"
    if k in ("?", "BELIRSIZ", "BELIRSİZ", ""):
        return "?"
    raise GUHata(f"tanınmayan yanıt: {x!r}")


def gu_kappa(a: np.ndarray, b: np.ndarray) -> float:
    """Cohen kappa; a, b bool dizileri (VAR = True)."""
    n = len(a)
    if n == 0:
        return float("nan")
    po = float(np.mean(a == b)); pa, pb = float(np.mean(a)), float(np.mean(b))
    pe = pa * pb + (1 - pa) * (1 - pb)
    return float((po - pe) / (1 - pe)) if pe < 1 else float("nan")


def gu_boot(a: np.ndarray, b: np.ndarray, B: int, tohum: int) -> Dict[str, Any]:
    rng = np.random.default_rng(tohum); n = len(a); ks = []
    for _ in range(B):
        j = rng.integers(0, n, n); ks.append(gu_kappa(a[j], b[j]))
    ks = np.array(ks); gec = ks[np.isfinite(ks)]
    return {"alt": float(np.percentile(gec, 2.5)) if len(gec) else float("nan"), "ust": float(np.percentile(gec, 97.5)) if len(gec) else float("nan"),
            "gecersiz": int(len(ks) - len(gec))}


def gu_hukum(k: float, n: int) -> str:
    if n < 30 or not np.isfinite(k):
        return "ÖLÇÜLEMEDİ (karar sayısı < 30 ya da kappa tanımsız)"
    E = GU_ESIK["kappa"]
    return "TANIM GEÇERLİ" if k >= E["gecerli"] else ("KISMEN" if k >= E["kismen"] else "TANIM GEÇERSİZ")


def gu_olc(cemal_yol: str) -> Dict[str, Any]:
    M = _gu_muhur_oku()
    for ad, y in (("anahtar", GU_YOL["anahtar"]), ("pdf", GU_YOL["pdf"])):
        if _sha(y) != M[ad]:
            raise GUHata(f"MÜHÜR BOZUK: {ad} sha'sı ön kayıttakiyle aynı değil -> DURDU")
    if _sha_esik() != M["esik"]:
        raise GUHata("MÜHÜR BOZUK: GU_ESIK sha'sı ön kayıttakiyle aynı değil -> DURDU")
    J = json.load(open(GU_YOL["anahtar"], encoding="utf-8")); S = pd.DataFrame(J["sayfalar"])
    C = json.load(open(cemal_yol, encoding="utf-8"))
    cem = {int(k): gu_norm(v) for k, v in C.items()}
    eksik = sorted(set(S.sayfa) - set(cem)); fazla = sorted(set(cem) - set(S.sayfa))
    if eksik or fazla:
        raise GUHata(f"yanıt sayfaları anahtarla uyuşmuyor: eksik {eksik}, fazla {fazla}")
    S["cemal"] = S.sayfa.map(cem)
    soru = int((S.cemal == "?").sum()); K = S[S.cemal != "?"].copy(); n = len(K)
    E = GU_ESIK["kappa"]; sonuc: Dict[str, Any] = {"n_sayfa": int(len(S)), "soru_isareti": soru, "karar_n": n, "modeller": {}}
    cem_b = (K.cemal == "VAR").to_numpy(bool)
    for ad in ("ANA", "IKINCIL-1", "IKINCIL-2"):
        mod = (K.model_etiketi.map(lambda z: z[ad]) == "VAR").to_numpy(bool)
        k = gu_kappa(cem_b, mod); ar = gu_boot(cem_b, mod, int(E["B"]), int(E["tohum"])) if n else {"alt": np.nan, "ust": np.nan, "gecersiz": 0}
        tp, tn = int((cem_b & mod).sum()), int((~cem_b & ~mod).sum()); fp, fn = int((~cem_b & mod).sum()), int((cem_b & ~mod).sum())
        sonuc["modeller"][ad] = {"uyum": float(np.mean(cem_b == mod)) if n else np.nan, "kappa": k, "aralik": ar, "hukum": gu_hukum(k, n),
                                 "tablo": {"Cemal VAR + kod VAR": tp, "Cemal YOK + kod YOK": tn, "Cemal YOK + kod VAR": fp, "Cemal VAR + kod YOK": fn},
                                 "uyusmayan": [int(s) for s in K.sayfa[cem_b != mod]]}
    # bilgi: pazar ve hücre bazında ANA uyumu
    ana = (K.model_etiketi.map(lambda z: z["ANA"]) == "VAR").to_numpy(bool)
    K["_ana_ok"] = (cem_b == ana)
    sonuc["bilgi_pazar"] = {p: {"n": int(len(g)), "uyum": float(g._ana_ok.mean())} for p, g in K.groupby("pazar")}
    sonuc["bilgi_hucre"] = {f"S3={a} S5={b}": {"n": int(len(g)), "uyum": float(g._ana_ok.mean()), "Cemal_VAR": int((g.cemal == 'VAR').sum())}
                            for (a, b), g in K.groupby(["S3", "S5"])}
    f = lambda x: "—" if x is None or not np.isfinite(x) else f"{x:.3f}"  # noqa: E731
    L = [f"# GÖZ UYUM KÖR SETİ — SONUÇ", "", f"Üretim: {_simdi()} (UTC). Mühür denetimi: anahtar, PDF ve GU_ESIK sha'ları ön kayıtla aynı.", "",
         f"Sayfa {len(S)}; karar (VAR / YOK) {n}; '?' (karar dışı) {soru}.", "",
         "## Uyum tablosu", "", "| model | uyum | kappa | %95 aralık (B 5000) | hüküm |", "|---|---|---|---|---|"]
    for ad, r in sonuc["modeller"].items():
        L.append(f"| {ad} ({GU_ESIK['model'][ad]}) | {f(r['uyum'])} | {f(r['kappa'])} | [{f(r['aralik']['alt'])}, {f(r['aralik']['ust'])}] | {r['hukum']} |")
    L += ["", "Hüküm yalnız ANA için bağlayıcıdır (ön kayıt); ikincil iki satır bilgidir. Kappa >= 0,60 TANIM GEÇERLİ; 0,40-0,60 KISMEN; < 0,40 TANIM GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ.", ""]
    for ad, r in sonuc["modeller"].items():
        L += [f"### {ad}: 2x2", "", "| | sayı |", "|---|---|"] + [f"| {k} | {v} |" for k, v in r["tablo"].items()]
        L += ["", f"Uyuşmayan sayfalar ({len(r['uyusmayan'])}): {r['uyusmayan']}", ""]
    L += ["## Bilgi: ANA uyumu pazar ve hücre bazında (küçük n; hüküm değil)", "", "| grup | n | uyum |", "|---|---|---|"]
    for k, v in sonuc["bilgi_pazar"].items():
        L.append(f"| {k} | {v['n']} | {f(v['uyum'])} |")
    for k, v in sonuc["bilgi_hucre"].items():
        L.append(f"| {k} (Cemal VAR {v['Cemal_VAR']}) | {v['n']} | {f(v['uyum'])} |")
    L += ["", "## Uyuşmayan sayfaların kodu gördüğü değerler (ANA)", "", "| sayfa | pazar | Cemal | kod (Ş3) | F2 | F4 | Ş5 |", "|---|---|---|---|---|---|---|"]
    for r in K[~K._ana_ok].sort_values("sayfa").itertuples():
        L.append(f"| {r.sayfa} | {r.pazar} | {r.cemal} | {'VAR' if r.S3 else 'YOK'} | {f(r.F2)} | {f(r.F4)} | {'VAR' if r.S5 else 'YOK'} |")
    L += ["", f"Sonraki adım (ön kayıt): {GU_ESIK['ikinci_adim']}.", ""]
    _yaz(GU_YOL["sonuc"], "\n".join(L))
    _jyaz(os.path.join(GU_DIR, "goz_uyum_sonuc.json"), sonuc)
    return sonuc


# ================================================================ 6) TEST (kısa; prefix değişmezliği + çakışma kapısı)
def gu_cakisma_kontrol() -> None:
    ez = [k for k, v in _CK_ONCE_GU.items() if k in globals() and id(globals()[k]) != v and not k.startswith("_")]
    if ez:
        raise GUHata(f"çakışma kapısı: bellekteki mevcut ad(lar) ezildi: {ez[:5]}")


def gu_test() -> Dict[str, Any]:
    gu_cakisma_kontrol()
    # kappa sağlaması
    a = np.array([1, 1, 0, 0, 1, 0], bool); b = np.array([1, 0, 0, 0, 1, 1], bool)
    assert abs(gu_kappa(a, a) - 1.0) < 1e-12 and abs(gu_kappa(a, ~a) + 1.0) < 1e-12 and abs(gu_kappa(a, b) - 0.3333333333333333) < 1e-9
    # ek özellik prefix değişmezliği: sonrası değişince aynı
    rng = np.random.default_rng(1); n = 200
    C = 100 + np.cumsum(rng.normal(0, 1, n)); O = C + rng.normal(0, .3, n); H = np.maximum(O, C) + abs(rng.normal(0, .5, n)) + .1
    L = np.minimum(O, C) - abs(rng.normal(0, .5, n)) - .1; V = rng.uniform(1e3, 2e3, n)
    i = 150; x1 = _gu_ek_ozellik(O, H, L, C, V, i)
    O2, H2, L2, C2, V2 = O.copy(), H.copy(), L.copy(), C.copy(), V.copy()
    O2[i + 1:] = 1; H2[i + 1:] = 2; L2[i + 1:] = 0.5; C2[i + 1:] = 1.5; V2[i + 1:] = 7
    x2 = _gu_ek_ozellik(O2, H2, L2, C2, V2, i)
    assert all((np.isnan(x1[k]) and np.isnan(x2[k])) or x1[k] == x2[k] for k in GU_EK_KOL), "ek özellik t sonrasına bağlı"
    return {"tamam": True}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", choices=["sec", "pdf", "muhur", "olc", "test"])
    ap.add_argument("--islem", type=int, default=4)
    ap.add_argument("--cemal", default=None)
    a = ap.parse_args()
    if a.komut == "sec":
        gu_sec(a.islem)
    elif a.komut == "pdf":
        print(gu_pdf())
    elif a.komut == "muhur":
        print(gu_muhur())
    elif a.komut == "olc":
        if not a.cemal:
            raise SystemExit("olc için --cemal J.json gerekli")
        r = gu_olc(a.cemal); print(json.dumps({k: r[k] for k in ("n_sayfa", "soru_isareti", "karar_n")}, ensure_ascii=False))
    else:
        print(gu_test())
