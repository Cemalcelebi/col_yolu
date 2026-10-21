# =====================================================================
#  COL_BUGUN — "D12 BUGUN hangi colleri buluyor?"   (2026-10-21, v1.0)
#
#  SORU (Cemal 21 Eki): D12 nerede, bugun hangi colu buluyor; goster, test edelim.
#
#  YONTEM
#    Tespit: COL_v1.col_olc (uretimdeki kod: SEGMENT_MOD='dip' -> col_dip = bolge + dipte + yeni dip yok + imza >= 3/4,
#            uzunluk >= MIN_UZ, yukseklik <= MAX_YUK ATR, bant). Yalniz bugune kadarki veri. D11 verisi durmus hisse
#            aday sayilmaz, D8 fon suzgeci etiket olarak yazilir (elenmez, gorulsun diye).
#    Cikti : her col icin satir (kutu tarihleri, bar, konum, imza, taban, tavan, fiyat, tavana %, GECER, ruzgar, fon)
#            + grafikli PDF (son 220 bar, kutu dikdortgeni, taban/tavan cizgisi, SMA20/SMA50, hacim). Hisse adi GORUNUR:
#            bu kor test degil, Cemal'in "hangi colu buluyor" sorusuna cevap.
#    Ek    : kutusu olup imza/dip kapisina takilan hisseler ayri CSV'de (RED nedeniyle) — "neden bulmadi" icin.
#
#  KURAL_MOTORU: K1 veri (COL_DIP_TEST.cd_k1_bist + onarim)  K2 COL_v1  K3 tarama  K4 grafik  K5 rapor
#  Calistirma: GitHub Actions 'Arastirma' is akisi (betik: COL_BUGUN.py) ya da Colab:
#    exec(open('/content/drive/MyDrive/col_tarayici/COL_BUGUN.py').read()); R = col_bugun()
#  Cikti: arastirma_cikti/col_bugun/ (COL_BUGUN_YYYY-MM-DD.csv, COL_BUGUN_YYYY-MM-DD.pdf, COL_BUGUN_red_YYYY-MM-DD.csv, rapor)
# =====================================================================
from __future__ import annotations

import contextlib
import io
import logging
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

_CK_ONCE_CB = {k: id(v) for k, v in globals().items()}

CB_SURUM = "COL_BUGUN v1.1 (2026-10-21, etiketleme seti)"
cblog = logging.getLogger("col.bugun")
if not cblog.handlers:
    _cb_h = logging.StreamHandler(sys.stderr)
    _cb_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s bugun: %(message)s", "%H:%M:%S"))
    cblog.addHandler(_cb_h)
    cblog.setLevel(logging.INFO)
    cblog.propagate = False


@dataclass
class CBAyar:
    kok: str = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/content/drive/MyDrive/col_tarayici"
    cikti: Optional[str] = None
    tarih: Optional[str] = None          # None = verinin son gunu
    grafik_bar: int = 220                # grafikte gosterilen son bar sayisi
    sayfa_basi: int = 4                  # PDF sayfasinda grafik sayisi
    min_bar: int = 260                   # taramaya girmek icin en az bar
    etiket_n: int = 20                   # etiketleme PDF'i: red listesinden secilen kutu sayisi (bulunanlar ayrica hepsi)
    etiket_min_bar: int = 25             # etiketlemeye girecek red kutusunun en az bar sayisi
    tohum: int = 42


def _cb_cd():
    """COL_DIP_TEST tek kaynak: veri yukleme, onarim ve COL_v1'i ayri ad alaninda yukleme."""
    import importlib
    kok = CBAyar().kok
    if kok not in sys.path:
        sys.path.insert(0, kok)
    return importlib.import_module("COL_DIP_TEST")


# ------------------------------------------------------------------ K3 tarama
def cb_k3_tara(ay: CBAyar, ns: Dict[str, Any], veri: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Uretim col_olc ile bugunku coller + kutusu olup kapiya takilanlar (red). Donus: {'col': df, 'red': df, 'bayat': {...}}."""
    t0 = time.monotonic()
    tarih = pd.Timestamp(ay.tarih) if ay.tarih else None
    try:
        bayat, _, toplu = ns["veri_bayat"](veri, tarih=tarih)
        if toplu:
            bayat = {}
    except Exception as ex:                                                  # D11 yoksa surdur
        cblog.warning("K3 veri_bayat: %s", ex)
        bayat = {}
    try:
        RZ = ns["sektor_ruzgar"](veri, tarih=tarih)
    except Exception as ex:
        cblog.warning("K3 sektor_ruzgar: %s", ex)
        RZ = pd.DataFrame()
    col: List[Dict[str, Any]] = []
    red: List[Dict[str, Any]] = []
    for k, (sem, df) in enumerate(veri.items()):
        x = df[df.index <= tarih] if tarih is not None else df
        x = x[np.isfinite(x.Close)]
        if len(x) < ay.min_bar or sem in bayat:
            continue
        try:
            o = ns["col_olc"](x)
        except Exception as ex:
            cblog.debug("%s col_olc: %s", sem, ex)
            o = None
        fiyat = float(x.Close.iloc[-1])
        if o:
            try:
                fe = ns["fon_etiket"](sem)
            except Exception:
                fe = None
            rz = float(RZ.ruz.get(sem, np.nan)) if (not RZ.empty and sem in RZ.index) else np.nan
            rv = bool(RZ.ruzgar.get(sem, False)) if (not RZ.empty and sem in RZ.index and "ruzgar" in RZ.columns) else False
            col.append({"sembol": sem, "kutu_bas": o["bas_tarih"], "kutu_son": o["son_tarih"], "bar": o["uzunluk"],
                        "konum": o.get("konum"), "imza": o.get("imza"), "imza_ok": o.get("imza_ok", ""),
                        "kucuk_oran": o.get("kucuk_oran"), "bb_min": o.get("bb_min"), "doji_kat": o.get("doji_kat"),
                        "hacim_kat": o.get("hacim_kat"), "taban": o["taban"], "tavan": o["tavan"], "fiyat": round(fiyat, 2),
                        "tavana_%": round((o["tavan"] / fiyat - 1) * 100, 1), "yuk_atr": o["yukseklik_atr"],
                        "doji": o.get("doji"), "fitil": o.get("alt_fitil"), "dar": o.get("dar"), "clv": o.get("clv"),
                        "GECER": bool(o["GECER"]), "ruz_%": round(100 * rz) if np.isfinite(rz) else np.nan,
                        "ruzgar": "RUZGAR" if rv else "", "fon": f"{fe[1]:.0f}%" if fe else ""})
        else:
            # neden yok? col_dip tanisi: kutu var ama kapiya mi takildi
            try:
                _, t = ns["col_dip"](x, tani=True)
            except Exception:
                t = {}
            if t.get("red") and t.get("red") not in ("bolge yok", "veri kisa", "gecmis kisa"):
                red.append({"sembol": sem, "red": t["red"], "kutu_bas": t.get("bas_tarih"), "kutu_son": t.get("son_tarih"),
                            "bar": t.get("uz"), "konum": t.get("konum"), "yeni_dip_yok": t.get("yeni_dip_yok"),
                            "imza": t.get("imza"), "imza_ok": t.get("imza_ok", ""), "kucuk_oran": t.get("kucuk_oran"),
                            "bb_min": t.get("bb_min"), "doji_kat": t.get("doji_kat"), "hacim_kat": t.get("hacim_kat"),
                            "fiyat": round(fiyat, 2)})
        if (k + 1) % 100 == 0:
            cblog.info("K3: %d/%d hisse | col %d | red %d (%.0f sn)", k + 1, len(veri), len(col), len(red), time.monotonic() - t0)
    tc = pd.DataFrame(col)
    if len(tc):
        tc = tc.sort_values(["GECER", "imza", "tavana_%"], ascending=[False, False, True]).reset_index(drop=True)
    tr = pd.DataFrame(red)
    if len(tr):
        tr = tr.sort_values(["red", "sembol"]).reset_index(drop=True)
    cblog.info("K3 bitti: %d col, %d red, %d bayat (%.0f sn)", len(tc), len(tr), len(bayat), time.monotonic() - t0)
    return {"col": tc, "red": tr, "bayat": bayat}


# ------------------------------------------------------------------ K4 grafik
def cb_k4_grafik(ay: CBAyar, veri: Dict[str, pd.DataFrame], tc: pd.DataFrame, yol: str, baslik: str, anonim: bool = False) -> Optional[str]:
    """Her col icin mum grafigi: kutu dikdortgeni, taban/tavan, SMA20/50, hacim. Tek PDF.
    anonim=True: etiketleme icin — hisse adi yok, numara var, taban/tavan cizgisi yok (Cemal'in kurali: test resminde ad yok)."""
    if tc.empty:
        return None
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        from matplotlib.patches import Rectangle
    except Exception as ex:
        cblog.warning("K4 matplotlib yok, grafik atlandi: %s", ex)
        return None
    tarih = pd.Timestamp(ay.tarih) if ay.tarih else None
    with PdfPages(yol) as pdf:
        for p0 in range(0, len(tc), ay.sayfa_basi):
            parca = tc.iloc[p0:p0 + ay.sayfa_basi]
            fig, axs = plt.subplots(len(parca), 1, figsize=(8.27, 2.9 * len(parca)), squeeze=False)
            for ax, (_, r) in zip(axs[:, 0], parca.iterrows()):
                df = veri[r.sembol]
                x_ = df[df.index <= tarih] if tarih is not None else df
                x_ = x_[np.isfinite(x_.Close)]
                ix = x_.index
                en = len(x_) - 1
                a0 = max(0, en - ay.grafik_bar + 1)
                s = int(ix.searchsorted(pd.Timestamp(r.kutu_bas)))
                xs = np.arange(a0, en + 1)
                O, H, L, C, V = (x_[c].to_numpy(float)[a0:en + 1] for c in ("Open", "High", "Low", "Close", "Volume"))
                ax.vlines(xs, L, H, color="#888", lw=0.6)
                ax.vlines(xs, np.minimum(O, C), np.maximum(O, C), color=np.where(C >= O, "#2a9d8f", "#c0392b"), lw=1.8)
                ax.plot(xs, x_.Close.rolling(20).mean().to_numpy()[a0:en + 1], color="#e9a23b", lw=0.9, label="SMA20")
                ax.plot(xs, x_.Close.rolling(50).mean().to_numpy()[a0:en + 1], color="#6c5ce7", lw=0.9, label="SMA50")
                lo_, hi_ = float(x_.Low.iloc[s:en + 1].min()), float(x_.High.iloc[s:en + 1].max())
                ax.add_patch(Rectangle((s - .5, lo_), en - s + 1, hi_ - lo_, fill=False, ec="#8e44ad", lw=1.8, label="kutu (D12)"))
                if not anonim:
                    ax.axhline(r.tavan, color="#27ae60", lw=0.9, ls="--", label=f"tavan {r.tavan}")
                    ax.axhline(r.taban, color="#c0392b", lw=0.9, ls="--", label=f"taban {r.taban}")
                ax2 = ax.twinx(); ax2.bar(xs, V, color="#bbb", alpha=.35, width=1); ax2.set_ylim(0, np.nanmax(V) * 4); ax2.axis("off")
                if anonim:
                    ax.set_title(f"#{int(r.no)}   kutu {pd.Timestamp(r.kutu_bas):%d.%m.%Y}-{pd.Timestamp(r.kutu_son):%d.%m.%Y} ({r.bar} bar)   "
                                 f"konum {r.konum}  imza {r.imza}/4 [{r.imza_ok}]        COL / DEGIL / HENUZ DEGIL : ______", fontsize=8)
                else:
                    etiket = "  ".join(e for e in (("GECER" if r.GECER else "kural gecmez"), r.ruzgar, (f"fon {r.fon}" if r.fon else "")) if e)
                    ax.set_title(f"{r.sembol}  kutu {pd.Timestamp(r.kutu_bas):%d.%m.%Y}-{pd.Timestamp(r.kutu_son):%d.%m.%Y} ({r.bar} bar)  "
                                 f"konum {r.konum}  imza {r.imza}/4 [{r.imza_ok}]  fiyat {r.fiyat}  tavana %{r['tavana_%']:+.1f}  {etiket}",
                                 fontsize=7.5)
                tk = np.linspace(a0, en, 6).astype(int)
                ax.set_xticks(tk); ax.set_xticklabels([f"{ix[i]:%d.%m.%y}" for i in tk], fontsize=6.5)
                ax.tick_params(axis="y", labelsize=6.5); ax.legend(fontsize=5.5, loc="upper left", ncol=5)
            fig.suptitle(baslik, fontsize=9, y=1.0)
            fig.tight_layout()
            pdf.savefig(fig, bbox_inches="tight"); plt.close(fig)
    cblog.info("K4: PDF -> %s (%d grafik)", yol, len(tc))
    return yol


# ------------------------------------------------------------------ K6 etiketleme
def cb_k6_etiket(ay: CBAyar, veri: Dict[str, pd.DataFrame], tc: pd.DataFrame, tr: pd.DataFrame, cikti: str, gun: str) -> Optional[str]:
    """Cemal'in gozu icin set: bulunan collerin hepsi + red listesinden red nedenine gore dengeli etiket_n kutu
    (bar >= etiket_min_bar, imza yuksek olan once, sabit tohumla). Karisik sirada numaralanir; ad anahtari CSV'de."""
    rng = np.random.default_rng(ay.tohum)
    parcalar: List[pd.DataFrame] = []
    if len(tc):
        a = tc[["sembol", "kutu_bas", "kutu_son", "bar", "konum", "imza", "imza_ok", "fiyat"]].copy(); a["kaynak"] = "col"; a["red"] = "COL"
        parcalar.append(a)
    if len(tr):
        t = tr[tr.bar.fillna(0) >= ay.etiket_min_bar].copy()
        nedenler = [n for n in ("yeni dip", "dipte degil", "imza az") if (t.red == n).any()]
        pay = int(np.ceil(ay.etiket_n / max(1, len(nedenler))))
        for n in nedenler:
            g = t[t.red == n].copy()
            g["_r"] = rng.random(len(g))
            g = g.sort_values(["imza", "_r"], ascending=[False, True]).head(pay)
            b = g[["sembol", "kutu_bas", "kutu_son", "bar", "konum", "imza", "imza_ok", "fiyat", "red"]].copy(); b["kaynak"] = "red"
            parcalar.append(b)
    if not parcalar:
        return None
    E = pd.concat(parcalar, ignore_index=True)
    E = E.iloc[rng.permutation(len(E))].reset_index(drop=True)
    E.insert(0, "no", np.arange(1, len(E) + 1))
    E["cemal"] = ""
    E.to_csv(os.path.join(cikti, f"COL_BUGUN_etiket_{gun}.csv"), index=False)
    yol = cb_k4_grafik(ay, veri, E, os.path.join(cikti, f"COL_BUGUN_etiket_{gun}.pdf"),
                       f"Etiketleme — {gun}: {len(E)} kutu (hisse adsiz). Her kutuya: COL / DEGIL / HENUZ DEGIL", anonim=True)
    cblog.info("K6: etiket seti %d kutu (col %d, red %d)", len(E), int((E.kaynak == 'col').sum()), int((E.kaynak == 'red').sum()))
    return yol


# ------------------------------------------------------------------ ANA
def col_bugun(ay: Optional[CBAyar] = None, veri: Optional[Dict[str, pd.DataFrame]] = None) -> Dict[str, Any]:
    ay = ay or CBAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "col_bugun")
    os.makedirs(cikti, exist_ok=True)
    t0 = time.monotonic()
    CD = _cb_cd()
    cay = CD.CDAyar(kok=ay.kok)
    ns = CD.cd_k3_col(cay)                                                   # K2 COL_v1 (uretim)
    if veri is None:                                                         # K1 veri
        veri = CD.cd_k1_bist(cay)
        CD.cd_k2_onarim(cay, veri)
    son_gun = pd.Timestamp(ay.tarih) if ay.tarih else max(df.index[-1] for df in veri.values())
    R = cb_k3_tara(ay, ns, veri)                                             # K3
    tc, tr = R["col"], R["red"]
    gun = f"{son_gun:%Y-%m-%d}"
    tc.to_csv(os.path.join(cikti, f"COL_BUGUN_{gun}.csv"), index=False)
    tr.to_csv(os.path.join(cikti, f"COL_BUGUN_red_{gun}.csv"), index=False)
    pdf = cb_k4_grafik(ay, veri, tc, os.path.join(cikti, f"COL_BUGUN_{gun}.pdf"),
                       f"D12 dip colu — {gun} itibariyla bulunan {len(tc)} col ({ns.get('SEGMENT_MOD')}, imza>={ns.get('IMZA_MIN')}/4, "
                       f"DIP_KONUM {ns.get('DIP_KONUM')})")                   # K4
    etiket_pdf = cb_k6_etiket(ay, veri, tc, tr, cikti, gun)                      # K6
    # K5 rapor
    sat = [f"# COL BUGUN — {gun} ({CB_SURUM})", "",
           f"Tespit: uretim COL_v1.col_olc, SEGMENT_MOD={ns.get('SEGMENT_MOD')} (D12 col_dip: bolge + dipte DIP_KONUM<={ns.get('DIP_KONUM')} "
           f"+ yeni dip yok + imza>={ns.get('IMZA_MIN')}/4), uzunluk>={ns.get('MIN_UZ')} bar, yukseklik<={ns.get('MAX_YUK')} ATR. "
           f"{len(veri)} hisse, {len(R['bayat'])} verisi durmus (D11) disarida.", "",
           f"## Bulunan col: {len(tc)}  (kurali gecen {int(tc.GECER.sum()) if len(tc) else 0}, ruzgarli {int((tc.ruzgar == 'RUZGAR').sum()) if len(tc) else 0})", ""]
    if len(tc):
        g = tc[["sembol", "kutu_bas", "bar", "konum", "imza", "imza_ok", "taban", "tavan", "fiyat", "tavana_%", "GECER", "ruzgar", "fon"]]
        sat.append(g.to_string(index=False)); sat.append("")
        sat.append("imza dagilimi: " + ", ".join(f"{a}/4: {b}" for a, b in tc.imza.value_counts().sort_index(ascending=False).items()))
        sat.append("kutu uzunlugu (bar): medyan %.0f, en kisa %d, en uzun %d" % (tc.bar.median(), tc.bar.min(), tc.bar.max()))
        sat.append("")
    sat.append(f"## Kutusu olup kapiya takilan: {len(tr)}")
    if len(tr):
        sat.append("neden: " + ", ".join(f"{a} {b}" for a, b in tr.red.value_counts().items()))
        sat.append(tr[["sembol", "red", "kutu_bas", "bar", "konum", "imza", "imza_ok", "fiyat"]].head(60).to_string(index=False))
        if len(tr) > 60:
            sat.append(f"... (+{len(tr) - 60}; tamami CSV'de)")
    sat.append("")
    sat.append(f"Dosyalar: COL_BUGUN_{gun}.csv, COL_BUGUN_red_{gun}.csv" + (f", COL_BUGUN_{gun}.pdf" if pdf else " (PDF yok)")
               + (f", etiketleme: COL_BUGUN_etiket_{gun}.pdf + .csv" if etiket_pdf else ""))
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "COL_BUGUN_rapor.md"), "w", encoding="utf-8").write(metin)
    cblog.info("BITTI %.0f sn -> %s", time.monotonic() - t0, cikti)
    return {"col": tc, "red": tr, "rapor": metin, "pdf": pdf, "etiket_pdf": etiket_pdf, "cikti": cikti}


def _cakisma_kontrol_cb(_once=_CK_ONCE_CB, _dosya='COL_BUGUN.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_CB', '_CK_KAYIT', '_cakisma_kontrol_cb', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'io', 'time', 'logging', 'contextlib', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'dataclass')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_cb()

if __name__ == "__main__":
    R = col_bugun()
    print(R["rapor"])
