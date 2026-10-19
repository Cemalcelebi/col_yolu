#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 TEMA × ÇÖL  v1.0  — Çöl Yolu'nun ABD kırılımları, "ilk dalgasını yapmış tema" içinde daha mı iyi?
===============================================================================
YOL HARİTASI (Cemal ile 27 Eyl 2026'da KİLİTLENDİ — tanımlar sonuca bakılıp değiştirilmez):
  ADIM 0  TEMEL   : Çöl'ün resmi ölçüm fonksiyonu islemler_olc (arsiv/desen/DESEN_TAM.py içinde; kapalı dosyanın
                    YALNIZ bu fonksiyonu + 5 yardımcısı birebir okunur) iki ABD setinde resmi sayıları üretmeli:
                    ABD 2024-26 %62 / +8.3 · ABD 2022-23 %62 / +4.7  (tekil, ertesi açılış, 120 bar, %0.4).
                    Tutmazsa DUR — üstüne hiçbir şey kurulmaz.
  ADIM 1  TEMA    : endüstri → sektör fonu (sabit tablo). İLK DALGA GÜNÜ (fonun o güne kadarki kapanışlarıyla):
                    60 günde ≥ +%15 · SPY'den ≥ 10 puan önde · kapanış > SMA200.
                    Çıktı: dalga tablosu (her dalga sonrası fonun 60/120 gün SPY'ye göre getirisi — bilgi) + grafik.
  ADIM 2  KARAR   : kırılım günü "TEMA DALGASI SONRASI" = son 120 işlem gününde ≥ 1 ilk dalga günü VE fon > SMA200.
                    Eşlenemeyen hisse DIŞARIDA (tema yok sayılmaz).
                    GEÇME ŞARTI (ikisi birden, iki ABD setinde birden):
                      1) işlem başı beklenti farkı (tema − gerisi) Çöl'ün kendi ölçümüyle (OLCUM.kiyas: gün bloklu
                         bootstrap, %90 bant) iki sette de POZİTİF ve GERÇEK (bant sıfırın üstünde)
                      2) büyük kazanan (getiri ≥ %30) oranı tema grubunda gerisinin ≥ 1.3 katı
                    Geçmezse: bir kez, gerekçesi yazılarak tanım gözden geçirilir (TC_TANIM sürümü artar);
                    ikinci başarısızlıkta proje kapanır, Çöl mevcut haliyle devam eder.
ÖNCEKİ SEKTÖR TESTİNDEN FARKI (SEKTOR.py v1.4, kapandı): o test 11 geniş sektörün kırılım günü "şu an sıcak"
  (60 gün, üst %20) olup olmadığına bakıyordu. Bu test (a) endüstri düzeyinde tema fonu, (b) "ilk dalgasını yapmış,
  dinlenen tema" zamanlaması kullanır — çöl kırıldığı gün dinlenen temayı eski test "soğuk" sayıyordu.
DAVRANIŞ: ana sisteme hiçbir şey YAZMAZ; COL_v1/OLCUM/DESEN_TAM kendi ÖZEL ad alanında yüklenir (oturumu ezmez).
ÇIKTI ({K}/): tema_col.txt · tema_col_islemler.csv · tema_dalga.csv · tema_dalga.png · tema_col.json (damga)
KULLANIM (Colab):  exec(open('/content/drive/MyDrive/col_tarayici/tema_col.py').read()); TC = tema_col()
Bu bir ölçüm aracıdır, yatırım tavsiyesi değildir.
===============================================================================
"""
from __future__ import annotations
import ast, hashlib, io, json, logging, os, pickle, sys, time, types
from contextlib import redirect_stdout
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

_CK_ONCE = {k: id(v) for k, v in globals().items()}

TC_SURUM = "2026-09-27 v1.0a"
TC_K = "/content/drive/MyDrive/col_tarayici"
_tc_log = logging.getLogger("tema_col")
if not _tc_log.handlers:
    _tc_h = logging.StreamHandler(sys.stderr)
    _tc_h.setFormatter(logging.Formatter("%(asctime)s │ %(levelname)-7s │ %(message)s", "%H:%M:%S"))
    _tc_log.addHandler(_tc_h); _tc_log.setLevel(logging.INFO)


@dataclass(frozen=True)
class TemaTanim:
    """KİLİTLİ tanımlar. Tek revizyon hakkı: sürüm 'v1' → 'v2', gerekçe 'revizyon_gerekce'ye yazılır."""
    surum: str = "v1"
    revizyon_gerekce: str = ""
    dalga_gun: int = 60              # ilk dalga: fonun bu kadar günlük getirisi
    dalga_min: float = 15.0          # ≥ %15
    dalga_spy_fark: float = 10.0     # SPY'den ≥ 10 puan önde
    sma: int = 200                   # kapanış > SMA200
    sonrasi_gun: int = 120           # kırılım günü: son 120 işlem gününde ≥ 1 dalga günü
    buyuk_kazanan: float = 30.0      # getiri ≥ %30
    buyuk_oran_min: float = 1.3      # tema / gerisi ≥ 1.3
    ufuk: int = 120                  # Çöl ölçümü (değişmez)
    maliyet: float = 0.4
    giris: str = "acilis"


TC_TANIM = TemaTanim()
# ADIM 0 — resmi sayılar (COL_OZET.md bölüm 8 / KISA BLOK, 25 Eyl 2026)
TC_TABAN = {"ABD 2024-26": {"dosya": "onbellek_ABD.pkl", "kazanan": 62.0, "bek": 8.3},
            "ABD 2022-23": {"dosya": "onbellek_ABD_2022_23.pkl", "kazanan": 62.0, "bek": 4.7}}
TC_TOL_KAZANAN, TC_TOL_BEK = 1.0, 0.15          # yuvarlama payı (resmi sayılar tam sayı / 1 ondalık)
TC_OLC_ADLAR = ("_HATA_OLC", "dlog", "kirilim_bul_olc", "pnl_olc", "_olcu_olc", "_endeks_getiri_olc", "islemler_olc")

# endüstri → tema fonu (yfinance endüstri adları) · kalanlar sektör fonuna
TC_ENDUSTRI_FON: Dict[str, str] = {
    "Semiconductors": "SMH", "Semiconductor Equipment & Materials": "SMH",
    "Software - Application": "IGV", "Software - Infrastructure": "IGV", "Information Technology Services": "IGV",
    "Oil & Gas E&P": "XOP", "Oil & Gas Drilling": "XOP", "Oil & Gas Equipment & Services": "XOP",
    "Oil & Gas Integrated": "XLE", "Oil & Gas Midstream": "XLE", "Oil & Gas Refining & Marketing": "XLE",
    "Aerospace & Defense": "ITA", "Biotechnology": "XBI",
    "Medical Devices": "IHI", "Medical Instruments & Supplies": "IHI",
    "Banks - Regional": "KRE",
    "Residential Construction": "XHB", "Building Products & Equipment": "XHB",
    "Steel": "XME", "Other Industrial Metals & Mining": "XME", "Copper": "XME", "Aluminum": "XME",
    "Gold": "GDX", "Silver": "GDX", "Other Precious Metals & Mining": "GDX",
    "Solar": "TAN", "Uranium": "URA",
}
TC_SEKTOR_FON: Dict[str, str] = {
    "Technology": "XLK", "Financial Services": "XLF", "Healthcare": "XLV", "Industrials": "XLI",
    "Consumer Cyclical": "XLY", "Consumer Defensive": "XLP", "Utilities": "XLU", "Basic Materials": "XLB",
    "Real Estate": "XLRE", "Communication Services": "XLC", "Energy": "XLE",
}
TC_FON_AD = {"SMH": "yarı iletken", "IGV": "yazılım", "XOP": "petrol arama", "XLE": "enerji", "ITA": "savunma",
             "XBI": "biyoteknoloji", "IHI": "tıbbi cihaz", "KRE": "bölgesel banka", "XHB": "konut", "XME": "metal",
             "GDX": "altın/gümüş", "TAN": "güneş", "URA": "uranyum", "XLK": "teknoloji", "XLF": "finans",
             "XLV": "sağlık", "XLI": "sanayi", "XLY": "tüketim (döngüsel)", "XLP": "tüketim (temel)",
             "XLU": "kamu hizmeti", "XLB": "hammadde", "XLRE": "gayrimenkul", "XLC": "iletişim"}
TC_BUYUK_MIN_N = 5                 # şart 2 için temada en az bu kadar büyük kazanan (1-2 şanslı işlem geçirmesin)
TC_PIYASA = "SPY"


# ----------------------------------------------------------------------------- yükleme (özel ad alanı)
def _tc_dosya(K: str, *adaylar: str) -> str:
    for a in adaylar:
        y = os.path.join(K, a)
        if os.path.exists(y):
            return y
    raise FileNotFoundError(f"bulunamadı: {', '.join(os.path.join(K, a) for a in adaylar)}")


def tc_olc_cek(desen_yolu: str) -> Dict[str, str]:
    """DESEN_TAM.py'den YALNIZ islemler_olc ve yardımcılarının kaynağını BİREBİR çıkarır (ast)."""
    src = open(desen_yolu, encoding="utf-8").read()
    agac = ast.parse(src)
    out: Dict[str, str] = {}
    for dugum in agac.body:
        ad = None
        if isinstance(dugum, ast.FunctionDef):
            ad = dugum.name
        elif isinstance(dugum, ast.Assign) and len(dugum.targets) == 1 and isinstance(dugum.targets[0], ast.Name):
            ad = dugum.targets[0].id
        if ad in TC_OLC_ADLAR and ad not in out:          # ilk tanım (gömülü çekirdek dosyanın başında)
            out[ad] = ast.get_source_segment(src, dugum)
    eksik = [a for a in TC_OLC_ADLAR if a not in out]
    if eksik:
        raise RuntimeError(f"DESEN_TAM.py'de bulunamadı: {eksik} — resmi ölçüm fonksiyonu değişmiş olabilir")
    return out


def tc_yukle(K: str = TC_K) -> Dict[str, Any]:
    """COL_v1 + OLCUM + islemler_olc (DESEN_TAM'dan birebir) ÖZEL ad alanında. Oturumun adlarını ezmez."""
    m = types.ModuleType("tema_col_ozel")          # gerçek modül: OLCUM'daki dataclass sys.modules'ta ad alanını arar
    m.__file__ = os.path.join(K, "OLCUM.py"); sys.modules["tema_col_ozel"] = m
    ns: Dict[str, Any] = m.__dict__; ns["K"] = K
    with redirect_stdout(io.StringIO()):
        exec(compile(open(_tc_dosya(K, "COL_v1.py"), encoding="utf-8").read(), "COL_v1.py", "exec"), ns)
    # OLCUM kendi çakışma kapısıyla gelir. COL_v1'in ÖZEL adları (ör. günlükçü '_h', yalnız taze oturumda tanımlanır)
    # OLCUM'un özel adlarıyla çakışır → OLCUM, COL_v1'in yalnız GENEL adlarını gören AYRI bir modülde yüklenir;
    # sonra OLCUM'un genel adları (+ çakışmayan özel adları) ortak ad alanına alınır. OLCUM fonksiyonları kendi modülünde yaşar.
    mo = types.ModuleType("tema_col_ozel_olcum"); mo.__file__ = os.path.join(K, "OLCUM.py"); sys.modules["tema_col_ozel_olcum"] = mo
    mo.__dict__.update({k: v for k, v in ns.items() if not k.startswith("_")})
    with redirect_stdout(io.StringIO()):
        exec(compile(open(_tc_dosya(K, "OLCUM.py"), encoding="utf-8").read(), "OLCUM.py", "exec"), mo.__dict__)
    for k, v in mo.__dict__.items():
        if not k.startswith("__") and k not in ("_CK_ONCE", "_CK_KAYIT") and (not k.startswith("_") or k not in ns):
            ns[k] = v
    dy = _tc_dosya(K, "arsiv/desen/DESEN_TAM.py", "arsiv/DESEN_TAM.py", "DESEN_TAM.py")
    parcalar = tc_olc_cek(dy)
    ns["logging"] = logging
    for ad in TC_OLC_ADLAR:                                      # bağımlılık sırası korunur
        exec(compile(parcalar[ad], f"DESEN_TAM.py:{ad}", "exec"), ns)
    gerek = ["AL_PAY", "DOJI_ESIK", "gecerli_bar_maskesi", "carpanlar_hesapla", "bek", "kiyas", "olculer", "islemler_olc"]
    eksik = [g for g in gerek if g not in ns]
    if eksik:
        raise RuntimeError(f"yüklenemedi: {eksik}")
    ns["_tc_kaynak"] = {"desen": dy, "desen_md5": hashlib.md5(open(dy, "rb").read()).hexdigest(),
                        "olc_md5": hashlib.md5("".join(parcalar[a] for a in TC_OLC_ADLAR).encode()).hexdigest()}
    return ns


# ----------------------------------------------------------------------------- ADIM 0
def tc_islemler(ns: Dict[str, Any], OB: List[Dict[str, Any]], T: TemaTanim = TC_TANIM) -> pd.DataFrame:
    with redirect_stdout(io.StringIO()):
        return ns["islemler_olc"](OB, T.giris, tekil=True, ufuk=T.ufuk, maliyet=T.maliyet, xu=None)


def tc_adim0(ns: Dict[str, Any], setler: Dict[str, List[Dict[str, Any]]], beklenen: Optional[Dict[str, Dict[str, float]]] = None,
             T: TemaTanim = TC_TANIM) -> Dict[str, Any]:
    """Resmi sayıları yeniden üret. Döner: {'gecti': bool, 'setler': {ad: {...}}, 'islemler': {ad: t}}."""
    beklenen = beklenen or {k: {"kazanan": v["kazanan"], "bek": v["bek"]} for k, v in TC_TABAN.items()}
    R: Dict[str, Any] = {"gecti": True, "setler": {}, "islemler": {}}
    for ad, OB in setler.items():
        t = tc_islemler(ns, OB, T)
        kaz = 100 * float((t["getiri"] > 0).mean()) if len(t) else np.nan
        bk = float(ns["bek"](t["getiri"])) if len(t) else np.nan
        b = beklenen.get(ad, {})
        ok = bool(len(t) and abs(kaz - b.get("kazanan", np.nan)) <= TC_TOL_KAZANAN and abs(bk - b.get("bek", np.nan)) <= TC_TOL_BEK)
        R["setler"][ad] = {"n": int(len(t)), "kazanan": kaz, "bek": bk, "beklenen_kazanan": b.get("kazanan"),
                           "beklenen_bek": b.get("bek"), "tuttu": ok}
        R["islemler"][ad] = t
        R["gecti"] = R["gecti"] and ok
    return R


# ----------------------------------------------------------------------------- ADIM 1
def tc_fonlar(K: str = TC_K, yenile: bool = False, bas: str = "2005-01-01") -> pd.DataFrame:
    """Tema fonları + SPY günlük kapanış (düzeltilmiş). Önbellek {K}/tema_fon.pkl (5 günden eskiyse yenilenir)."""
    yol = os.path.join(K, "tema_fon.pkl")
    fonlar = sorted(set(TC_ENDUSTRI_FON.values()) | set(TC_SEKTOR_FON.values()) | {TC_PIYASA})
    if os.path.exists(yol) and not yenile:
        try:
            P = pickle.load(open(yol, "rb"))
            if set(fonlar) <= set(P.columns) and (pd.Timestamp.today() - P.index.max()).days <= 5:
                return P
        except Exception as e:
            _tc_log.warning("tema_fon.pkl okunamadı (%s) — yeniden indirilir", e)
    import yfinance as yf
    d = yf.download(fonlar, start=bas, interval="1d", auto_adjust=True, progress=False, group_by="column", threads=True)
    P = d["Close"] if isinstance(d.columns, pd.MultiIndex) else d[["Close"]]
    P = P.dropna(how="all")
    P.index = pd.to_datetime(P.index).tz_localize(None).normalize() if getattr(P.index, "tz", None) else pd.to_datetime(P.index).normalize()
    eksik = [f for f in fonlar if f not in P.columns or P[f].notna().sum() < 300]
    if eksik:
        _tc_log.warning("fon verisi eksik/kısa: %s", eksik)
    tmp = yol + ".tmp"; pickle.dump(P, open(tmp, "wb")); os.replace(tmp, yol)
    return P


def tc_dalga(P: pd.DataFrame, T: TemaTanim = TC_TANIM) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """-> (DALGA: gün×fon bool, SONRASI: gün×fon bool, UST200: gün×fon bool). Hepsi o güne kadarki kapanışlarla."""
    spy = P[TC_PIYASA]
    ret = P / P.shift(T.dalga_gun) - 1
    spy_ret = spy / spy.shift(T.dalga_gun) - 1
    sma = P.rolling(T.sma, min_periods=T.sma).mean()
    ust = (P > sma) & sma.notna()
    dalga = (ret * 100 >= T.dalga_min) & ((ret.sub(spy_ret, axis=0)) * 100 >= T.dalga_spy_fark) & ust
    dalga = dalga.fillna(False).astype(bool)
    # son 'sonrasi_gun' İŞLEM GÜNÜNDE (bugün dahil) ≥1 dalga günü VE bugün SMA üstü
    son_dalga = dalga.astype(int).rolling(T.sonrasi_gun, min_periods=1).max().astype(bool)
    sonrasi = son_dalga & ust
    return dalga.drop(columns=[TC_PIYASA], errors="ignore"), sonrasi.drop(columns=[TC_PIYASA], errors="ignore"), ust


def tc_dalga_tablosu(P: pd.DataFrame, DALGA: pd.DataFrame, bosluk: int = 20) -> pd.DataFrame:
    """Dalga dönemleri (≤ bosluk gün arayla gelen dalga günleri tek dönem) + başlangıçtan sonra fonun SPY'ye göre 60/120 gün getirisi."""
    S: List[Dict[str, Any]] = []; spy = P[TC_PIYASA]
    for f in DALGA.columns:
        g = DALGA[f].to_numpy(); ix = DALGA.index; i = 0; n = len(g)
        while i < n:
            if not g[i]:
                i += 1; continue
            bas = i; son = i; j = i + 1
            while j < n and (g[j] or (j - son) <= bosluk):
                if g[j]: son = j
                j += 1
            r: Dict[str, Any] = {"fon": f, "tema": TC_FON_AD.get(f, f), "bas": ix[bas].date(), "son": ix[son].date(), "gun": son - bas + 1}
            for k in (60, 120):
                if son + k < n:
                    a, b = ix[son], ix[son + k]
                    r[f"sonra{k}_goreli"] = 100 * ((P.at[b, f] / P.at[a, f] - 1) - (spy.at[b] / spy.at[a] - 1))
                else:
                    r[f"sonra{k}_goreli"] = np.nan
            S.append(r); i = j
    return pd.DataFrame(S)


def tc_grafik(P: pd.DataFrame, DALGA: pd.DataFrame, SONRASI: pd.DataFrame, yol: str, bas: str = "2021-01-01") -> bool:
    """Küçük çoklu: her fon ayrı panel — kapanış (mavi), SMA200 (gri), ilk dalga günleri (turuncu şerit),
    'dalga sonrası' dönemi (açık turuncu zemin). Tek seri/panel: lejant yerine başlık ve alt yazı."""
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        _tc_log.warning("matplotlib yok (%s)", e); return False
    fonlar = [f for f in DALGA.columns if f in P.columns]
    n = len(fonlar); kol = 4; sat = int(np.ceil(n / kol))
    fig, axs = plt.subplots(sat, kol, figsize=(16, 2.6 * sat), dpi=110, sharex=True)
    axs = np.atleast_1d(axs).ravel()
    yazi, ikincil, izgara = "#3d3d3a", "#73726c", "#e5e4de"
    for ax, f in zip(axs, fonlar):
        p = P[f][P.index >= bas].dropna(); sma = P[f].rolling(200).mean().reindex(p.index)
        d = DALGA[f].reindex(p.index).fillna(False).astype(bool); s = SONRASI[f].reindex(p.index).fillna(False).astype(bool)
        ax.fill_between(p.index, 0, 1, where=s.values, transform=ax.get_xaxis_transform(), color="#eb6834", alpha=0.10, lw=0)
        ax.fill_between(p.index, 0, 0.06, where=d.values, transform=ax.get_xaxis_transform(), color="#eb6834", alpha=0.9, lw=0)
        ax.plot(p.index, p.values, color="#2a78d6", lw=1.6)
        ax.plot(sma.index, sma.values, color="#8f8e88", lw=1.0)
        ax.set_title(f"{f} — {TC_FON_AD.get(f, f)}", fontsize=9, color=yazi, loc="left")
        ax.grid(axis="y", color=izgara, lw=0.6); ax.tick_params(colors=ikincil, labelsize=7)
        for k in ("top", "right"):
            ax.spines[k].set_visible(False)
        for k in ("left", "bottom"):
            ax.spines[k].set_color(izgara)
    for ax in axs[n:]:
        ax.axis("off")
    fig.suptitle("Tema fonları — mavi: kapanış · gri: SMA200 · koyu turuncu şerit: İLK DALGA günü · açık turuncu zemin: 'dalga sonrası' (son 120 günde dalga + SMA200 üstü)",
                 fontsize=10, color=yazi, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.97)); fig.savefig(yol, facecolor="#ffffff"); plt.close(fig)
    return True


# ----------------------------------------------------------------------------- eşleme
def tc_harita(K: str, semboller: List[str], yfinance_ile: bool = True) -> pd.DataFrame:
    """sembol -> (sektor, endustri, fon, kaynak). sektor_ABD.csv önbelleği; eksikler yfinance .info ile eklenir (önbelleğe yazılır)."""
    yol = os.path.join(K, "sektor_ABD.csv")
    H = pd.read_csv(yol, dtype=str) if os.path.exists(yol) else pd.DataFrame(columns=["sembol", "sektor", "endustri"])
    norm = lambda s: str(s)[:-3] if str(s).upper().endswith(".AM") else str(s)
    H["_n"] = H["sembol"].map(norm); bilinen = set(H["_n"])
    eksik = sorted({norm(s) for s in semboller} - bilinen)
    if eksik and yfinance_ile:
        _tc_log.info("sektör: %d sembol yfinance'ten (önbellek %d)", len(eksik), len(bilinen))
        import yfinance as yf
        yeni = []
        for k, s in enumerate(eksik, 1):
            sek = end = "BILINMIYOR"
            try:
                inf = yf.Ticker(s).info or {}
                if inf.get("sector"):
                    sek, end = str(inf["sector"]), str(inf.get("industry") or "BILINMIYOR")
            except Exception as e:
                _tc_log.debug("%s: %s", s, e)
            yeni.append({"sembol": f"{s}.AM", "sektor": sek, "endustri": end})
            if k % 100 == 0 or k == len(eksik):
                pd.concat([H.drop(columns=["_n"]), pd.DataFrame(yeni)]).drop_duplicates("sembol").to_csv(yol, index=False)
        H = pd.read_csv(yol, dtype=str); H["_n"] = H["sembol"].map(norm)
    H = H.drop_duplicates("_n").set_index("_n")
    if not len(H):
        return H.assign(fon=pd.Series(dtype=object), kaynak=pd.Series(dtype=object))
    def fon(r):
        f = TC_ENDUSTRI_FON.get(str(r["endustri"]))
        if f:
            return f, "endüstri"
        f = TC_SEKTOR_FON.get(str(r["sektor"]))
        return (f, "sektör") if f else (None, "yok")
    fk = [fon(r) for _, r in H.iterrows()]                      # None korunur (NaN'a dönmez)
    H["fon"] = pd.Series([a for a, _ in fk], index=H.index, dtype=object)
    H["kaynak"] = pd.Series([b for _, b in fk], index=H.index, dtype=object)
    return H


def _tc_asof(M: pd.DataFrame, gun: pd.Timestamp, kol: Optional[str]) -> Optional[bool]:
    if kol is None or kol not in M.columns:
        return None
    i = M.index.searchsorted(pd.Timestamp(gun), side="right") - 1
    return None if i < 0 else bool(M[kol].iloc[i])


# ----------------------------------------------------------------------------- ADIM 2
def tc_etiketle(t: pd.DataFrame, H: pd.DataFrame, SONRASI: pd.DataFrame) -> pd.DataFrame:
    """Kırılım günündeki (o güne kadarki veriyle) tema durumu. Eşlenemeyen: tema=NaN (dışarıda)."""
    t = t.copy(); norm = lambda s: str(s)[:-3] if str(s).upper().endswith(".AM") else str(s)
    t["fon"] = [H["fon"].get(norm(s)) if norm(s) in H.index else None for s in t["sembol"]]
    t["tema"] = [(_tc_asof(SONRASI, k, f) if isinstance(f, str) and f else None) for k, f in zip(t["kirilim"], t["fon"])]
    t["buyuk"] = t["getiri"] >= TC_TANIM.buyuk_kazanan
    return t


def tc_karar(ns: Dict[str, Any], T_setler: Dict[str, pd.DataFrame], T: TemaTanim = TC_TANIM, n_boot: Optional[int] = None) -> Dict[str, Any]:
    """Her set: OLCUM.kiyas(tema vs gerisi) + büyük kazanan oranı. Geçme şartı iki sette birden."""
    R: Dict[str, Any] = {"setler": {}, "gecti": True, "neden": []}
    for ad, t in T_setler.items():
        tt = t[t["tema"].notna()].copy(); m = tt["tema"].astype(bool).to_numpy()
        with redirect_stdout(io.StringIO()):
            k = ns["kiyas"](tt, m, "gerisi", "tema dalgası sonrası", n=n_boot, yaz=False)
        fb = (k.get("fark") or {}).get("bek")
        bt = float(tt.loc[m, "buyuk"].mean()) if m.any() else np.nan
        bg = float(tt.loc[~m, "buyuk"].mean()) if (~m).any() else np.nan
        oran = (bt / bg) if (np.isfinite(bt) and np.isfinite(bg) and bg > 0) else (np.inf if bt and bt > 0 else np.nan)
        s = {"n": int(len(t)), "n_olculen": int(len(tt)), "n_disari": int(len(t) - len(tt)), "n_tema": int(m.sum()), "n_gerisi": int((~m).sum()),
             "olcu_tema": k.get("olcu_b", {}), "olcu_gerisi": k.get("olcu_a", {}), "bek_fark": fb, "yetersiz": bool(k.get("yetersiz", False)),
             "buyuk_tema%": 100 * bt if np.isfinite(bt) else np.nan, "buyuk_gerisi%": 100 * bg if np.isfinite(bg) else np.nan, "buyuk_oran": oran}
        s["sart1"] = bool(fb is not None and not s["yetersiz"] and fb[1] > 0)
        s["n_buyuk_tema"] = int(tt.loc[m, "buyuk"].sum()) if m.any() else 0
        s["sart2"] = (bool(np.isfinite(oran) and oran >= T.buyuk_oran_min) or bool(oran == np.inf)) and s["n_buyuk_tema"] >= TC_BUYUK_MIN_N
        R["setler"][ad] = s
        if s["yetersiz"]:
            R["neden"].append(f"{ad}: dilim küçük (n tema {s['n_tema']}, gerisi {s['n_gerisi']}) — karar verilemez")
        if not s["sart1"]:
            R["neden"].append(f"{ad}: beklenti farkı " + ("yok (bant sıfırı kapsıyor)" if fb and fb[1] <= 0 <= fb[2] else
                                                        "TERS (tema daha kötü)" if fb and fb[2] < 0 else "ölçülemedi"))
        if not s["sart2"]:
            R["neden"].append(f"{ad}: büyük kazanan yok (iki grupta da %{T.buyuk_kazanan}+ işlem 0)" if not np.isfinite(oran) and oran != np.inf else
                              f"{ad}: temada büyük kazanan {s['n_buyuk_tema']} işlem < {TC_BUYUK_MIN_N} — tesadüf olabilir" if s["n_buyuk_tema"] < TC_BUYUK_MIN_N else
                              f"{ad}: büyük kazanan oranı {oran:.2f} kat < {T.buyuk_oran_min}")
        R["gecti"] = R["gecti"] and s["sart1"] and s["sart2"]
    if len(T_setler) < 2:
        R["gecti"] = False; R["neden"].append("iki ABD seti gerekli")
    return R


# ----------------------------------------------------------------------------- orkestra
def _tc_f(x, fmt="+.1f"):
    try:
        return format(float(x), fmt) if np.isfinite(float(x)) else "—"
    except Exception:
        return "—"


def tema_col(K: str = TC_K, T: TemaTanim = TC_TANIM, yenile_fon: bool = False, n_boot: Optional[int] = None,
             ns: Optional[Dict[str, Any]] = None, setler: Optional[Dict[str, List[Dict[str, Any]]]] = None,
             P: Optional[pd.DataFrame] = None, beklenen: Optional[Dict[str, Dict[str, float]]] = None,
             yfinance_ile: bool = True) -> Dict[str, Any]:
    t0 = time.monotonic(); L: List[str] = []; A = L.append
    A("=" * 100); A(f" TEMA × ÇÖL {TC_SURUM} · tanım {T.surum}" + (f" (revizyon: {T.revizyon_gerekce})" if T.revizyon_gerekce else "")); A("=" * 100)
    C: Dict[str, Any] = {"surum": TC_SURUM, "tanim": asdict(T)}
    ns = ns or tc_yukle(K)
    C["kaynak"] = ns.get("_tc_kaynak", {})
    if setler is None:
        setler = {}
        for ad, v in TC_TABAN.items():
            setler[ad] = pickle.load(open(_tc_dosya(K, v["dosya"]), "rb"))
    # ---- ADIM 0
    A("\n ADIM 0 — TEMEL: resmi Çöl sayıları yeniden üretiliyor (islemler_olc, DESEN_TAM'dan birebir)")
    A0 = tc_adim0(ns, setler, beklenen, T)
    for ad, s in A0["setler"].items():
        A(f"   {ad:12s} n={s['n']:5d} kazanan %{_tc_f(s['kazanan'], '.1f')} bek {_tc_f(s['bek'], '+.2f')}   "
          f"(resmi %{_tc_f(s['beklenen_kazanan'], '.1f')} / {_tc_f(s['beklenen_bek'], '+.2f')})  -> {'TUTTU' if s['tuttu'] else 'TUTMADI'}")
    C["adim0"] = {k: v for k, v in A0["setler"].items()}
    if not A0["gecti"]:
        A("\n ✖ ADIM 0 GEÇMEDİ — temel sağlam değil, DURULDU. Farkın nedeni bulunmadan Adım 1–2 çalıştırılmaz.")
        return _tc_bitir(K, L, C, t0, None, None)
    A("   ✔ ADIM 0 GEÇTİ — temel sağlam.")
    # ---- ADIM 1
    A("\n ADIM 1 — TEMA: ilk dalga günü = fon 60 günde ≥ +%15, SPY'den ≥ 10 puan önde, SMA200 üstü")
    P = P if P is not None else tc_fonlar(K, yenile=yenile_fon)
    DALGA, SONRASI, _ = tc_dalga(P, T)
    DT = tc_dalga_tablosu(P, DALGA)
    C["dalga_sayisi"] = int(len(DT))
    if len(DT):
        oz = DT.groupby("fon").agg(dalga=("fon", "size"), s60=("sonra60_goreli", "mean"), s120=("sonra120_goreli", "mean"))
        A(f"   {len(DT)} dalga dönemi ({P.index.min().date()} → {P.index.max().date()}). Dalga BİTTİKTEN sonra fonun SPY'ye göre getirisi (bilgi):")
        tum60, tum120 = DT["sonra60_goreli"].dropna(), DT["sonra120_goreli"].dropna()
        A(f"   tümü: +60 gün {_tc_f(tum60.mean())} (medyan {_tc_f(tum60.median())}, n={len(tum60)}) · +120 gün {_tc_f(tum120.mean())} (medyan {_tc_f(tum120.median())}, n={len(tum120)})")
        for f, r in oz.sort_values("dalga", ascending=False).iterrows():
            A(f"     {f:5s} {TC_FON_AD.get(f, f):20s} dalga {int(r['dalga']):3d} · +60g {_tc_f(r['s60']):>6s} · +120g {_tc_f(r['s120']):>6s}")
    png = tc_grafik(P, DALGA, SONRASI, os.path.join(K, "tema_dalga.png"))
    # ---- ADIM 2
    A("\n ADIM 2 — KARAR: kırılım günü 'tema dalgası sonrası' (son 120 günde dalga + SMA200 üstü) vs gerisi")
    semb = sorted({str(o.get("sembol")) for OB in setler.values() for o in OB})
    H = tc_harita(K, semb, yfinance_ile=yfinance_ile)
    TS = {ad: tc_etiketle(A0["islemler"][ad], H, SONRASI) for ad in setler}
    KR = tc_karar(ns, TS, T, n_boot)
    for ad, s in KR["setler"].items():
        ot, og = s["olcu_tema"], s["olcu_gerisi"]; fb = s["bek_fark"]
        A(f"\n   [{ad}] işlem {s['n']} · ölçülen {s['n_olculen']} · dışarıda (fon eşlenemedi) {s['n_disari']}")
        A(f"     tema dalgası sonrası  n={s['n_tema']:5d} kazanan %{_tc_f(ot.get('kazanan%'), '.0f')} bek {_tc_f(ot.get('bek'))} ağır %{_tc_f(ot.get('agir%'), '.0f')} · büyük (≥%30) %{_tc_f(s['buyuk_tema%'], '.1f')}")
        A(f"     gerisi                n={s['n_gerisi']:5d} kazanan %{_tc_f(og.get('kazanan%'), '.0f')} bek {_tc_f(og.get('bek'))} ağır %{_tc_f(og.get('agir%'), '.0f')} · büyük (≥%30) %{_tc_f(s['buyuk_gerisi%'], '.1f')}")
        A(f"     bek farkı (tema − gerisi) " + (f"{fb[0]:+.1f} [%90 bant {fb[1]:+.1f}, {fb[2]:+.1f}]" if fb else "—") +
          f"  -> şart 1 {'✔' if s['sart1'] else '✖'} · büyük kazanan oranı {_tc_f(s['buyuk_oran'], '.2f')} kat -> şart 2 {'✔' if s['sart2'] else '✖'}")
    A("\n" + "#" * 100)
    if KR["gecti"]:
        A(" KARAR: GEÇTİ — iki ABD setinde de tema dalgası sonrası kırılımlar hem beklentide gerçekten iyi hem büyük kazanan oranı ≥ 1.3 kat.")
        A("        Sonraki adım (yol haritası 3): lider/takipçi. Günlük taramaya 'tema' sütunu eklenir, kâğıt defterinde izlenir.")
    else:
        A(" KARAR: GEÇMEDİ")
        for n_ in KR["neden"]:
            A(f"   · {n_}")
        A(" Kural: bir kez, gerekçesi yazılarak tanım gözden geçirilebilir (TemaTanim(surum='v2', revizyon_gerekce='...')).")
        A("        İkinci başarısızlıkta proje kapanır; Çöl mevcut haliyle devam eder.")
    A("#" * 100)
    C["adim2"] = {ad: {k: (list(v) if isinstance(v, tuple) else v) for k, v in s.items() if k not in ("olcu_tema", "olcu_gerisi")} | {
        "olcu_tema": s["olcu_tema"], "olcu_gerisi": s["olcu_gerisi"]} for ad, s in KR["setler"].items()}
    C["karar"] = "GEÇTİ" if KR["gecti"] else "GEÇMEDİ"; C["neden"] = KR["neden"]
    try:
        pd.concat([t.assign(set=ad).drop(columns=[c for c in ("o",) if c in t.columns]) for ad, t in TS.items()]).to_csv(
            os.path.join(K, "tema_col_islemler.csv"), index=False)
        DT.to_csv(os.path.join(K, "tema_dalga.csv"), index=False)
    except OSError as e:
        _tc_log.error("CSV yazılamadı: %s", e)
    return _tc_bitir(K, L, C, t0, TS, DT, png)


def _tc_bitir(K, L, C, t0, TS, DT, png=False) -> Dict[str, Any]:
    L.append(f"\n  -> {K}/tema_col.txt · tema_col.json" + (" · tema_col_islemler.csv · tema_dalga.csv" if TS else "") +
             (" · tema_dalga.png" if png else "") + f"   ({time.monotonic() - t0:.0f} sn)")
    txt = "\n".join(L); print(txt)
    try:
        open(os.path.join(K, "tema_col.txt"), "w", encoding="utf-8").write(txt)
        json.dump(C, open(os.path.join(K, "tema_col.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    except OSError as e:
        _tc_log.error("çıktı yazılamadı: %s", e)
    return {"ozet": txt, "damga": C, "islemler": TS, "dalga": DT}


def _cakisma_kontrol(_once=_CK_ONCE, _dosya='tema_col.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE', '_CK_KAYIT', '_cakisma_kontrol', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'io', 'time', 'json', 'ast', 'hashlib', 'pickle', 'logging', 'redirect_stdout', 'annotations',
           'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass', 'asdict')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")
_cakisma_kontrol()
print(f"[ok] tema_col {TC_SURUM} (tanım {TC_TANIM.surum}) — TC = tema_col()")
