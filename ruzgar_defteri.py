#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 RÜZGÂR DEFTERİ  v1.0  — ileriye dönük kâğıt testi: makine erken görür, Cemal neden↔sonucu bağlar, karne sayar
===============================================================================
NEDEN (27 Eyl 2026): Tema Sepeti × Çöl v2 GEÇMEDİ — makinenin erken işareti (dipten medyan 20 gün, haberden ~1 ay
  önce) gerçek rüzgârı sahtesinden AYIRAMIYOR; ama gerçek rüzgârın ilk 40 gününde kırılan çöl 2 kat kazandırıyor.
  Geçmiş veride "hangi rüzgâr gerçekti" bilindiği için insan kararı test edilemez → İLERİYE DÖNÜK, sonuç bilinmeden.
  Cemal'in gücü: birbirini destekleyen neden↔sonuç gözlemlerini bağlamak. Makine gözlemleri ERKEN toplar, kanıt kartı
  olarak önüne koyar; Cemal tek soruya cevap verir: "nedenler sonuçları açıklıyor / destekliyor mu?"
KİLİTLİ TANIMLAR (2 ay değişmez; sonuca bakılıp eşik oynanmaz):
  SEPET      : yfinance endüstrisi (sektor_ABD.csv), ≥ 5 üye, eşit ağırlık, |günlük| > %50 = bozuk veri.
  İŞARET 1 FİYAT   : sepet 20 günde SPY'yi ≥ 5 puan geçti · sepet > SMA200 · önceki 20 günde bu işaret yok (= başlangıç)
  İŞARET 2 YAYILIM : üyelerin ≥ %60'ı son 20 günde SPY'den iyi
  İŞARET 3 HACİM   : üyelerin son 20 günlük toplam hacmi ≥ önceki 60 günlük ortalama hacmin 1.3 katı
  KART       : işaret 1 başlangıcından sonraki 0–20 işlem günü içindeki her sepet; kaç işaret yandığı (1/3, 2/3, 3/3),
               SÜZGEÇ YOK — hepsi gösterilir. Önde giden 5 üye, çölünü kurmuş (kırılmamış) üyeler, son haber başlıkları.
  KARAR      : Cemal, sonuç bilinmeden: destek = EVET / HAYIR / KISMEN · hisse (isteğe bağlı) · tek satır neden.
               Tarih damgalı; aynı kart için ikinci karar kabul edilmez (ilk kalır).
  KARNE      : karar gününden 20/40/60 işlem günü sonra otomatik: sepet SPY'den ayrışmayı sürdürdü mü (40g ≥ +5 puan),
               seçilen hisse sepetin diğer üyelerinden iyi mi; EVET/HAYIR/KISMEN ve 1/3–2/3–3/3 kırılımlarıyla.
  ÖLÇÜ       : "makine erken mi" = işaretin dipten kaç gün sonra yandığı (dip = son 60 günün en düşük sepet kapanışı);
               "makine doğru mu" = 40 gün sonra hâlâ önde olan işaretlerin payı, 1/3–2/3–3/3 ayrı.
KAĞIT: gerçek para yok. Bu bir ölçüm aracıdır, yatırım tavsiyesi değildir.
DOSYALAR ({K}/ruzgar/): fiyat_hacim.pkl (parti parti, kaldığı yerden sürer) · kartlar.csv (her gün eklenir, silinmez)
  · kararlar.csv (yalnız EKLENİR) · karne.txt/.csv · bugun.txt
KULLANIM (Colab):
  exec(open('/content/drive/MyDrive/col_tarayici/ruzgar_defteri.py').read())
  RD = ruzgar_gunu()                                  # bugünün kartları + karne
  karar_ver('Semiconductors', 'EVET', hisse='AMD', neden='HBM talebi + INTC teşvik; 3/3 yandı')
  haber('Semiconductors')                             # önde giden üyelerin son başlıkları (yfinance)
===============================================================================
"""
from __future__ import annotations
import hashlib, io, json, logging, os, pickle, sys, time, types
from contextlib import redirect_stdout
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

_CK_ONCE = {k: id(v) for k, v in globals().items()}

RD_SURUM = "2026-09-27 v1.0"
RD_K = "/content/drive/MyDrive/col_tarayici"
_rd_log = logging.getLogger("ruzgar_defteri")
if not _rd_log.handlers:
    _rd_h = logging.StreamHandler(sys.stderr)
    _rd_h.setFormatter(logging.Formatter("%(asctime)s │ %(levelname)-7s │ %(message)s", "%H:%M:%S"))
    _rd_log.addHandler(_rd_h); _rd_log.setLevel(logging.INFO)


@dataclass(frozen=True)
class DefterTanim:
    surum: str = "v1"
    min_uye: int = 5
    getiri_sinir: float = 0.5
    erken_gun: int = 20
    erken_fark: float = 5.0
    sma: int = 200
    sessiz: int = 20
    pencere: int = 20                 # kart: başlangıçtan sonraki 0..20 gün
    yayilim_esik: float = 0.60        # işaret 2
    hacim_kat: float = 1.3            # işaret 3
    hacim_ref_gun: int = 60
    dip_gun: int = 60                 # "erken mi": dip = son 60 günün en düşüğü
    karne_gunler: Tuple[int, ...] = (20, 40, 60)
    karne_esik: float = 5.0           # 40 gün sonra sepet SPY'den ≥ 5 puan önde = rüzgâr sürdü
    onde_n: int = 5
    fiyat_bas: str = "2024-01-01"     # SMA200 + hacim referansı için yeter


RD_TANIM = DefterTanim()
RD_KARAR = ("EVET", "HAYIR", "KISMEN")


# ----------------------------------------------------------------------------- yardımcı
def _rd_norm(s: Any) -> str:
    s = str(s)
    return s[:-3] if s.upper().endswith(".AM") else s


def _rd_f(x, fmt="+.1f"):
    try:
        return format(float(x), fmt) if np.isfinite(float(x)) else "—"
    except Exception:
        return "—"


def rd_klasor(K: str) -> str:
    y = os.path.join(K, "ruzgar"); os.makedirs(y, exist_ok=True); return y


def rd_tc_yukle(K: str) -> types.ModuleType:
    """tema_col.py ayrı modül (harita + COL_v1.col_segment için). Oturumu ezmez."""
    yol = os.path.join(K, "tema_col.py")
    if not os.path.exists(yol):
        raise FileNotFoundError(f"{yol} yok")
    m = types.ModuleType("tema_col_rd"); m.__file__ = yol; sys.modules["tema_col_rd"] = m
    with redirect_stdout(io.StringIO()):
        exec(compile(open(yol, encoding="utf-8").read(), yol, "exec"), m.__dict__)
    return m


# ----------------------------------------------------------------------------- fiyat + hacim (parti parti, sürer)
def _rd_yf_indir(liste: List[str], bas: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """-> (kapanış, hacim) gün × sembol. Düzeltilmiş kapanış; BRK.B → BRK-B çevirisi."""
    import yfinance as yf
    yfad = {x.replace(".", "-"): x for x in liste}
    d = yf.download(list(yfad), start=bas, interval="1d", auto_adjust=True, progress=False, group_by="column", threads=True)
    if d is None or not len(d):
        return pd.DataFrame(), pd.DataFrame()
    out = []
    for kol in ("Close", "Volume"):
        X = d[kol] if isinstance(d.columns, pd.MultiIndex) else d[[kol]].rename(columns={kol: list(yfad)[0]})
        if isinstance(X, pd.Series):
            X = X.to_frame(list(yfad)[0])
        X = X.rename(columns=lambda c: yfad.get(str(c), str(c)))
        ix = pd.to_datetime(X.index)
        X.index = (ix.tz_localize(None) if getattr(ix, "tz", None) is not None else ix).normalize()
        out.append(X.dropna(how="all"))
    return out[0], out[1]


def rd_fiyat_hacim(K: str, semboller: List[str], bas: str, parti: int = 100, indir: Any = None, bayat_gun: int = 1
                   ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """{K}/ruzgar/fiyat_hacim.pkl — günlük yenilenir (bayat_gun), kesilirse kaldığı yerden sürer."""
    indir = indir or _rd_yf_indir
    yol = os.path.join(rd_klasor(K), "fiyat_hacim.pkl"); D: Dict[str, Any] = {}
    if os.path.exists(yol):
        try:
            D = pickle.load(open(yol, "rb"))
            yas = (pd.Timestamp.now() - pd.Timestamp(D.get("oturum", "1900-01-01"))).days
            if D.get("bas") != bas or yas > bayat_gun:
                D = {}
        except Exception as e:
            _rd_log.warning("fiyat önbelleği okunamadı (%s)", e); D = {}
    if not D:
        D = {"bas": bas, "oturum": str(pd.Timestamp.now()), "bitti": [], "basarisiz": [], "C": pd.DataFrame(), "V": pd.DataFrame()}
    bitti = set(D["bitti"]); kalan = [x for x in dict.fromkeys(semboller) if x not in bitti]
    if kalan:
        _rd_log.info("fiyat+hacim indiriliyor: %d sembol (%d hazır)", len(kalan), len(bitti))
    t0 = time.monotonic()
    for i in range(0, len(kalan), parti):
        grup = kalan[i:i + parti]; Cp = Vp = None
        for deneme in range(2):
            try:
                Cp, Vp = indir(grup, bas); break
            except Exception as e:
                _rd_log.warning("parti %d indirilemedi (%d): %s", i // parti + 1, deneme + 1, e); time.sleep(2 * (deneme + 1))
        if Cp is None:
            raise RuntimeError(f"indirme durdu (parti {i // parti + 1}) — hücreyi yeniden çalıştır, kaldığı yerden sürer")
        gel = [c for c in Cp.columns if c in grup and Cp[c].notna().sum() > 0]
        D["C"] = pd.concat([D["C"], Cp[gel]], axis=1) if len(D["C"]) else Cp[gel]
        D["V"] = pd.concat([D["V"], Vp.reindex(columns=gel)], axis=1) if len(D["V"]) else Vp.reindex(columns=gel)
        D["bitti"] = list(bitti | set(grup)); bitti = set(D["bitti"])
        D["basarisiz"] = sorted(set(D["basarisiz"]) | (set(grup) - set(gel)))
        tmp = yol + ".tmp"; pickle.dump(D, open(tmp, "wb")); os.replace(tmp, yol)
        _rd_log.info("  parti %d/%d · %d hisse · %.0f sn", i // parti + 1, -(-len(kalan) // parti), D["C"].shape[1], time.monotonic() - t0)
    C = D["C"].sort_index(); C = C.loc[:, ~C.columns.duplicated()]
    V = D["V"].sort_index(); V = V.loc[:, ~V.columns.duplicated()]
    sira = [c for c in dict.fromkeys(semboller) if c in C.columns]
    return C[sira].where(C[sira] > 0), V.reindex(columns=sira).reindex(C.index), {"hisse": len(sira), "basarisiz": len(D["basarisiz"]), "son": str(C.index.max().date()) if len(C) else None}


# ----------------------------------------------------------------------------- sepet + üç işaret
def rd_sepetler(C: pd.DataFrame, H: pd.DataFrame, T: DefterTanim = RD_TANIM) -> Dict[str, List[str]]:
    e = H["endustri"].astype(str); uy: Dict[str, List[str]] = {}
    for g, grup in e.groupby(e):
        if g in ("BILINMIYOR", "nan", "None", ""):
            continue
        m = [s for s in grup.index if s in C.columns]
        if len(m) >= T.min_uye:
            uy[g] = m
    return uy


def rd_sepet_endeks(R: pd.DataFrame, uyeler: List[str], T: DefterTanim = RD_TANIM) -> Tuple[pd.Series, pd.Series]:
    """Eşit ağırlıklı sepet endeksi ve geçerli gün maskesi (üye ≥ min_uye)."""
    Ru = R[uyeler]; n = Ru.notna().sum(axis=1); ok = n >= T.min_uye
    b = (Ru.sum(axis=1, min_count=1) / n.where(ok)).where(ok)
    return (1.0 + b.fillna(0.0)).cumprod(), ok


def rd_isaret1(I: pd.Series, spy: pd.Series, ok: pd.Series, T: DefterTanim = RD_TANIM) -> Tuple[pd.Series, pd.Series]:
    """(işaret, başlangıç) — tema_sepet.ts_erken ile aynı tanım."""
    spy = spy.reindex(I.index).ffill()
    fark = ((I / I.shift(T.erken_gun) - 1) - (spy / spy.shift(T.erken_gun) - 1)) * 100
    sma = I.rolling(T.sma, min_periods=T.sma).mean()
    g = ok.reindex(I.index).fillna(False).astype(bool)
    isaret = ((fark >= T.erken_fark) & (I > sma) & g & g.shift(T.erken_gun, fill_value=False)).fillna(False).astype(bool)
    onceki = isaret.astype(int).shift(1, fill_value=0).rolling(T.sessiz, min_periods=1).max()
    return isaret, (isaret & (onceki == 0))


def rd_isaret2(C: pd.DataFrame, spy: pd.Series, uyeler: List[str], gun: pd.Timestamp, T: DefterTanim = RD_TANIM) -> Tuple[bool, float, pd.Series]:
    """YAYILIM: üyelerin ≥ %60'ı son 20 günde SPY'den iyi. -> (yandı, pay, üye 20g getirileri)."""
    Cu = C[uyeler]; i = Cu.index.get_loc(gun)
    if i < T.erken_gun:
        return False, np.nan, pd.Series(dtype=float)
    g = (Cu.iloc[i] / Cu.iloc[i - T.erken_gun] - 1) * 100
    s = (spy.iloc[i] / spy.iloc[i - T.erken_gun] - 1) * 100
    g = g.dropna()
    if len(g) < T.min_uye:
        return False, np.nan, g
    pay = float((g > s).mean())
    return pay >= T.yayilim_esik, pay, g.sort_values(ascending=False)


def rd_isaret3(V: pd.DataFrame, uyeler: List[str], gun: pd.Timestamp, T: DefterTanim = RD_TANIM) -> Tuple[bool, float]:
    """HACİM: üyelerin son 20 gün toplam hacmi ≥ önceki 60 gün ortalama hacminin 1.3 katı (günlük ortalama bazında)."""
    Vu = V[uyeler]; i = Vu.index.get_loc(gun)
    if i < T.erken_gun + T.hacim_ref_gun:
        return False, np.nan
    son = Vu.iloc[i - T.erken_gun + 1:i + 1].sum(axis=1).mean()
    ref = Vu.iloc[i - T.erken_gun - T.hacim_ref_gun + 1:i - T.erken_gun + 1].sum(axis=1).mean()
    if not (np.isfinite(son) and np.isfinite(ref)) or ref <= 0:
        return False, np.nan
    kat = float(son / ref)
    return kat >= T.hacim_kat, kat


def rd_col_durum(df: Optional[pd.DataFrame], ns: Dict[str, Any]) -> Optional[bool]:
    """Çölünü kurmuş ve HENÜZ KIRILMAMIŞ mı (COL_v1.col_segment, gerçek OHLCV)."""
    cs = ns.get("col_segment")
    if cs is None or df is None or len(df) < 60:
        return None
    x = df.rename(columns=str.title)[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
    seg = cs(x)
    if not seg or seg.get("uzunluk", 0) < ns.get("MIN_UZ", 20) or seg.get("yukseklik_atr", 99) > ns.get("MAX_YUK", 6):
        return False
    return bool(float(x["Close"].iloc[-1]) <= float(seg["tavan"]) * float(ns.get("AL_PAY", 1.002)))


# ----------------------------------------------------------------------------- kartlar
def rd_kartlar(C: pd.DataFrame, V: pd.DataFrame, spy: pd.Series, uyeler: Dict[str, List[str]], gun: pd.Timestamp,
               T: DefterTanim = RD_TANIM, VERI: Any = None, ns: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """'gun' itibarıyla (o güne kadarki veriyle) kart olan sepetler: işaret 1 başlangıcı son 0..pencere günde."""
    Cg = C[C.index <= gun]; Vg = V[V.index <= gun]; spyg = spy.reindex(Cg.index).ffill()
    R = Cg.pct_change(fill_method=None); R = R.where(R.abs() <= T.getiri_sinir)
    anahtar = {_rd_norm(k): k for k in VERI} if isinstance(VERI, dict) else {}
    Rw: List[Dict[str, Any]] = []
    for g, uy in uyeler.items():
        I, ok = rd_sepet_endeks(R, uy, T)
        isr, bas = rd_isaret1(I, spyg, ok, T)
        son = bas.iloc[-(T.pencere + 1):]
        if not son.any():
            continue
        ib = int(np.where(son.values)[0][-1]); bas_gun = son.index[ib]; kac_gun = int(len(son) - 1 - ib)
        i_b = I.index.get_loc(bas_gun); a = max(0, i_b - T.dip_gun)
        dip_i = a + int(np.argmin(I.iloc[a:i_b + 1].to_numpy())); dip_gun = I.index[dip_i]
        sp = spyg
        fark = float(((I.iloc[-1] / I.iloc[-1 - T.erken_gun] - 1) - (sp.iloc[-1] / sp.iloc[-1 - T.erken_gun] - 1)) * 100)
        y2, pay, g20 = rd_isaret2(Cg, spyg, uy, gun, T)
        y3, kat = rd_isaret3(Vg, uy, gun, T)
        col_l: List[str] = []
        for s in uy:
            try:
                d = rd_col_durum(VERI[anahtar[s]] if s in anahtar else None, ns or {})
                if d:
                    col_l.append(s)
            except Exception as e:
                _rd_log.debug("çöl %s: %s", s, e)
        Rw.append({"gun": gun.date(), "endustri": g, "uye": len(uy), "isaret_bas": bas_gun.date(), "kac_gun_once": kac_gun,
                   "dip": dip_gun.date(), "dipten_isarete_gun": int(i_b - dip_i),
                   "i1_fiyat": bool(isr.iloc[-1]), "sepet_spy_20g": round(fark, 1),
                   "i2_yayilim": bool(y2), "yayilim_pay": round(pay, 2) if np.isfinite(pay) else np.nan,
                   "i3_hacim": bool(y3), "hacim_kat": round(kat, 2) if np.isfinite(kat) else np.nan,
                   "yanan": int(bool(isr.iloc[-1])) + int(y2) + int(y3),
                   "onde": ", ".join(f"{s} {v:+.0f}%" for s, v in g20.head(T.onde_n).items()),
                   "col_kuranlar": ", ".join(col_l[:12]),
                   "kart_id": f"{g}|{bas_gun.date()}"})
    K_ = pd.DataFrame(Rw)
    return K_.sort_values(["yanan", "kac_gun_once"], ascending=[False, True]).reset_index(drop=True) if len(K_) else K_


def rd_kart_kaydet(K: str, kartlar: pd.DataFrame) -> int:
    """kartlar.csv'ye ekler (aynı gün+kart tekrar yazılmaz). Döner: eklenen satır."""
    yol = os.path.join(rd_klasor(K), "kartlar.csv")
    if not len(kartlar):
        return 0
    eski = pd.read_csv(yol, dtype=str) if os.path.exists(yol) else pd.DataFrame()
    yeni = kartlar.astype(str)
    if len(eski):
        var = set(zip(eski["gun"], eski["kart_id"])); yeni = yeni[[ (a, b) not in var for a, b in zip(yeni["gun"], yeni["kart_id"])]]
    if len(yeni):
        pd.concat([eski, yeni]).to_csv(yol, index=False)
    return int(len(yeni))


# ----------------------------------------------------------------------------- karar (yalnız eklenir)
def rd_karar_ver(K: str, endustri: str, karar: str, hisse: str = "", neden: str = "", gun: Optional[str] = None) -> Dict[str, Any]:
    """Kararı tarih damgasıyla kararlar.csv'ye EKLER. Aynı kart (endüstri + işaret başlangıcı) için ilk karar kalır."""
    karar = str(karar).strip().upper()
    if karar not in RD_KARAR:
        raise ValueError(f"karar {RD_KARAR} olmalı, gelen: {karar!r}")
    if not neden or len(neden.strip()) < 5:
        raise ValueError("tek satır 'neden' zorunlu (sonradan senin öğrenmen için)")
    ky = os.path.join(rd_klasor(K), "kartlar.csv")
    if not os.path.exists(ky):
        raise RuntimeError("önce ruzgar_gunu() çalıştır — kart yok")
    kart = pd.read_csv(ky, dtype=str)
    kart = kart[kart["endustri"] == endustri]
    if gun:
        kart = kart[kart["gun"] == str(gun)]
    if not len(kart):
        raise ValueError(f"'{endustri}' için kart yok (bugün ruzgar_gunu() çalıştı mı? ad birebir mi?)")
    k = kart.sort_values("gun").iloc[-1]
    yol = os.path.join(rd_klasor(K), "kararlar.csv")
    eski = pd.read_csv(yol, dtype=str) if os.path.exists(yol) else pd.DataFrame()
    if len(eski) and (eski["kart_id"] == k["kart_id"]).any():
        o = eski[eski["kart_id"] == k["kart_id"]].iloc[0]
        _rd_log.warning("bu kart için karar zaten var (%s %s) — ilk karar kalır, değiştirilmez", o["karar"], o["karar_zamani"])
        return o.to_dict()
    hisse = _rd_norm(hisse).upper() if hisse else ""
    satir = {"kart_id": k["kart_id"], "endustri": endustri, "kart_gunu": k["gun"], "karar_zamani": str(pd.Timestamp.now().floor("s")),
             "karar": karar, "hisse": hisse, "neden": neden.strip().replace("\n", " "), "yanan": k["yanan"],
             "i1": k["i1_fiyat"], "i2": k["i2_yayilim"], "i3": k["i3_hacim"], "sepet_spy_20g": k["sepet_spy_20g"],
             "dipten_isarete_gun": k["dipten_isarete_gun"]}
    pd.concat([eski, pd.DataFrame([satir])]).to_csv(yol, index=False)
    print(f"  kaydedildi: {endustri} → {karar}" + (f" · {hisse}" if hisse else "") + f" · {satir['karar_zamani']}")
    return satir


# ----------------------------------------------------------------------------- karne
def rd_karne(K: str, C: pd.DataFrame, spy: pd.Series, uyeler: Dict[str, List[str]], T: DefterTanim = RD_TANIM) -> Tuple[pd.DataFrame, str]:
    """Her karar için 20/40/60 işlem günü sonrası: sepet−SPY farkı, hisse − sepetin diğer üyeleri. Olgunlaşmamışlar '—'."""
    yol = os.path.join(rd_klasor(K), "kararlar.csv")
    if not os.path.exists(yol):
        return pd.DataFrame(), "   karar yok"
    D = pd.read_csv(yol, dtype=str)
    R = C.pct_change(fill_method=None); R = R.where(R.abs() <= T.getiri_sinir)
    Rw: List[Dict[str, Any]] = []
    for _, d in D.iterrows():
        g = d["endustri"]; uy = uyeler.get(g, [])
        k0 = pd.Timestamp(d["kart_gunu"]); i0 = C.index.searchsorted(k0, side="right") - 1
        satir: Dict[str, Any] = {"endustri": g, "kart_gunu": d["kart_gunu"], "karar": d["karar"], "hisse": d["hisse"], "yanan": int(d["yanan"]),
                                 "neden": d["neden"]}
        I = rd_sepet_endeks(R, uy, T)[0] if uy else None
        for n in T.karne_gunler:
            j = i0 + n
            if I is None or j >= len(C):
                satir[f"sepet{n}"] = np.nan; satir[f"hisse{n}"] = np.nan; continue
            sf = float(((I.iloc[j] / I.iloc[i0] - 1) - (spy.iloc[j] / spy.iloc[i0] - 1)) * 100)
            satir[f"sepet{n}"] = round(sf, 1)
            h = d["hisse"] if isinstance(d["hisse"], str) else ""
            if h and h in C.columns and len(uy) > 1:
                hg = float((C[h].iloc[j] / C[h].iloc[i0] - 1) * 100)
                dig = [u for u in uy if u != h]
                og = float(((C[dig].iloc[j] / C[dig].iloc[i0] - 1) * 100).mean())
                satir[f"hisse{n}"] = round(hg - og, 1)
            else:
                satir[f"hisse{n}"] = np.nan
        satir["surdu40"] = (satir.get("sepet40", np.nan) >= T.karne_esik) if np.isfinite(satir.get("sepet40", np.nan)) else None
        Rw.append(satir)
    KR = pd.DataFrame(Rw); L: List[str] = []
    if not len(KR):
        return KR, "   karar yok"
    olgun = KR[KR["surdu40"].notna()]
    L.append(f"   {len(KR)} karar · 40 günü dolan {len(olgun)}")
    if len(olgun):
        L.append("   RÜZGÂR SÜRDÜ MÜ (40 gün sonra sepet SPY'den ≥ +5 puan)?")
        for ad, grp in olgun.groupby("karar"):
            L.append(f"     Cemal {ad:6s}: {int(grp['surdu40'].sum())}/{len(grp)} sürdü · sepet 40g ort {_rd_f(grp['sepet40'].mean())}")
        for y, grp in olgun.groupby("yanan"):
            L.append(f"     makine {y}/3 yanan: {int(grp['surdu40'].sum())}/{len(grp)} sürdü · sepet 40g ort {_rd_f(grp['sepet40'].mean())}")
        hs = olgun[olgun["hisse40"].notna()]
        if len(hs):
            L.append(f"   HİSSE SEÇİMİ (seçilen − sepetin diğer üyeleri, 40g): ort {_rd_f(hs['hisse40'].mean())} · "
                     f"{int((hs['hisse40'] > 0).sum())}/{len(hs)} sepetten iyi")
    else:
        L.append("   henüz 40 günü dolan karar yok — karne olgunlaşınca dolar")
    return KR, "\n".join(L)


# ----------------------------------------------------------------------------- haber (isteğe bağlı, yfinance)
def rd_haber(semboller: List[str], n: int = 5) -> List[str]:
    """Önde giden üyelerin son başlıkları — ham, doğrulanmamış; hikâyeyi okuyan insan."""
    try:
        import yfinance as yf
    except Exception:
        return ["yfinance yok"]
    out: List[str] = []
    for s in semboller:
        try:
            for h in (yf.Ticker(s.replace(".", "-")).news or [])[:n]:
                c = h.get("content", h); t = c.get("title") or h.get("title"); z = c.get("pubDate") or h.get("providerPublishTime")
                if t:
                    out.append(f"  {s}: {t}" + (f"  ({str(z)[:10]})" if z else ""))
        except Exception as e:
            out.append(f"  {s}: haber alınamadı ({e})")
    return out or ["  haber yok"]


# ----------------------------------------------------------------------------- günlük akış
def ruzgar_gunu(K: str = RD_K, T: DefterTanim = RD_TANIM, indir: Any = None, C: Optional[pd.DataFrame] = None,
                V: Optional[pd.DataFrame] = None, spy: Optional[pd.Series] = None, VERI: Any = None, gun: Optional[str] = None,
                tc: Any = None, yfinance_ile: bool = True) -> Dict[str, Any]:
    t0 = time.monotonic(); L: List[str] = []; A = L.append
    tc = tc or rd_tc_yukle(K)
    ns = tc.tc_yukle(K)
    hy = os.path.join(K, "sektor_ABD.csv")
    if not os.path.exists(hy):
        raise FileNotFoundError("sektor_ABD.csv yok — tema_sepet önce çalışmış olmalı")
    H = tc.tc_harita(K, sorted({_rd_norm(x) for x in pd.read_csv(hy, dtype=str)["sembol"]}), yfinance_ile=yfinance_ile)
    evren = sorted(x for x in H.index if str(H.at[x, "endustri"]) not in ("BILINMIYOR", "nan", "None", ""))
    if C is None or V is None:
        C, V, fb = rd_fiyat_hacim(K, evren + ["SPY"], bas=T.fiyat_bas, indir=indir)
    else:
        fb = {"hisse": C.shape[1], "basarisiz": 0, "son": str(C.index.max().date())}
    if spy is None:
        if "SPY" not in C.columns:
            raise RuntimeError("SPY fiyatı yok")
        spy = C["SPY"]
    C = C.drop(columns=["SPY"], errors="ignore"); V = V.drop(columns=["SPY"], errors="ignore")
    uyeler = rd_sepetler(C, H, T)
    g = pd.Timestamp(gun) if gun else C.index.max()
    if VERI is None:
        y = os.path.join(K, "veri_1d_america.pkl")
        try:
            VERI = pickle.load(open(y, "rb")) if os.path.exists(y) else None
            if isinstance(VERI, dict) and isinstance(VERI.get("veri"), dict):
                VERI = VERI["veri"]
        except Exception as e:
            _rd_log.warning("veri_1d_america.pkl okunamadı (%s)", e); VERI = None
    kart = rd_kartlar(C, V, spy, uyeler, g, T, VERI, ns)
    eklenen = rd_kart_kaydet(K, kart)
    A("=" * 100); A(f" RÜZGÂR DEFTERİ {RD_SURUM} · {g.date()} · {len(uyeler)} sepet · {fb['hisse']} hisse (veri {fb['son']})"); A("=" * 100)
    A(" KANIT KARTLARI — işaret 1 (fiyat) son 20 günde başlamış sepetler · süzgeç yok · Cemal: nedenler sonuçları destekliyor mu?")
    if not len(kart):
        A("   bugün kart yok")
    ky = os.path.join(rd_klasor(K), "kararlar.csv")
    kararli = set(pd.read_csv(ky, dtype=str)["kart_id"]) if os.path.exists(ky) else set()
    for _, r in kart.iterrows():
        durum = "KARAR VERİLDİ" if r["kart_id"] in kararli else "karar bekliyor"
        A(f"\n   [{r['yanan']}/3] {r['endustri']}  ({r['uye']} üye) · işaret {r['kac_gun_once']} gün önce · dipten işarete {r['dipten_isarete_gun']} gün · {durum}")
        yay = f"üyelerin %{100 * r['yayilim_pay']:.0f}'ı SPY'den iyi" if np.isfinite(r["yayilim_pay"]) else "—"
        A(f"      1 fiyat  {'✔' if r['i1_fiyat'] else '✖'}  sepet 20g SPY'den {r['sepet_spy_20g']:+.1f} puan")
        A(f"      2 yayılım {'✔' if r['i2_yayilim'] else '✖'}  {yay}")
        A(f"      3 hacim  {'✔' if r['i3_hacim'] else '✖'}  son 20g / önceki 60g = {_rd_f(r['hacim_kat'], '.2f')} kat")
        A(f"      önde: {r['onde']}")
        A(f"      çölünü kurmuş (kırılmamış): {r['col_kuranlar'] or '—'}")
    A(f"\n   kartlar.csv'ye {eklenen} yeni satır")
    KR, ktxt = rd_karne(K, C, spy, uyeler, T)
    A("\n KARNE"); A(ktxt)
    A(f"\n   karar_ver('<endüstri>', 'EVET|HAYIR|KISMEN', hisse='...', neden='...')   ·   haber('<endüstri>')")
    txt = "\n".join(L); print(txt)
    try:
        open(os.path.join(rd_klasor(K), "bugun.txt"), "w", encoding="utf-8").write(txt)
        if len(KR):
            KR.to_csv(os.path.join(rd_klasor(K), "karne.csv"), index=False)
            open(os.path.join(rd_klasor(K), "karne.txt"), "w", encoding="utf-8").write(ktxt)
    except OSError as e:
        _rd_log.error("yazılamadı: %s", e)
    _rd_log.info("%.0f sn", time.monotonic() - t0)
    g_ = globals(); g_["_RD_SON"] = {"K": K, "kart": kart, "uyeler": uyeler}
    return {"kart": kart, "karne": KR, "uyeler": uyeler, "ozet": txt}


def karar_ver(endustri: str, karar: str, hisse: str = "", neden: str = "", K: Optional[str] = None) -> Dict[str, Any]:
    K = K or (globals().get("_RD_SON") or {}).get("K") or RD_K
    return rd_karar_ver(K, endustri, karar, hisse, neden)


def haber(endustri: str, n: int = 5) -> None:
    S = globals().get("_RD_SON")
    if not S or not len(S["kart"]):
        print("önce ruzgar_gunu()"); return
    k = S["kart"][S["kart"]["endustri"] == endustri]
    if not len(k):
        print(f"'{endustri}' bugünkü kartlarda yok"); return
    semb = [x.split()[0] for x in str(k.iloc[0]["onde"]).split(", ") if x]
    print(f" {endustri} — önde gidenlerin son başlıkları (ham, doğrulanmamış):")
    for s in rd_haber(semb, n):
        print(s)


def _cakisma_kontrol_rd(_once=_CK_ONCE, _dosya='ruzgar_defteri.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE', '_CK_KAYIT', '_cakisma_kontrol', '_cakisma_kontrol_ts', '_cakisma_kontrol_rd', '_RD_SON',
            'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'io', 'time', 'json', 'hashlib', 'pickle', 'logging', 'types', 'redirect_stdout', 'annotations',
           'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass', 'asdict')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")
_cakisma_kontrol_rd()
print(f"[ok] ruzgar_defteri {RD_SURUM} — RD = ruzgar_gunu() · karar_ver(...) · haber(...)")
