"""TEZGAH2_VERI: Tezgah 2 veri ajani (indirme + bicim + kalite denetimi; OLCUM YOK).

Ne yapar: bugun islem goren ABD adi hisseleri (nasdaqtrader symbol dizini; olmazsa SEC company_tickers.json) ve mevcut Avrupa evrenini
Yahoo'dan (yfinance) 2000-01-03'ten bugune gunluk OHLCV indirir; V_ABD / V_AVR ile AYNI yapida V_ABD2.pkl / V_AVR2.pkl uretir ve
kalite denetimi yapar. Getiri / olay / sinyal olcumu YOKTUR (yalniz veri tutarliligi).
Fiyat kipi (V_ABD / V_AVR ile ayni): yfinance auto_adjust=True (bolunme + temettu duzeltmeli), sutunlar Open High Low Close Volume (float),
indeks 'Date' datetime64[s]; AVR'de ek 'Kur' sutunu = yerel para -> EUR (1 / EURxxx=X kapanis; Londra peni icin /100; EUR ulkelerinde 1),
Londra peni / sterlin 100x temizligi fi_avr_evren ile ayni mantik.
Komutlar (Colab ya da terminal; nohup ile arka planda):
    python TEZGAH2_VERI.py evren              # evren2_ABD.csv
    python TEZGAH2_VERI.py indir ABD|AVR      # parca parca indirir, kaldigi yerden surer
    python TEZGAH2_VERI.py birlestir ABD|AVR  # V_ABD2.pkl / V_AVR2.pkl
    python TEZGAH2_VERI.py kalite             # kalite sayimlari + supheli.csv + rapor json
Veri yolu: /root/.kasa/ham/veri3 (repo DISI). Kod degistiyse Colab'da calisma zamanini yeniden baslat.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_TZ = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

TZ_SURUM = "TEZGAH2_VERI v1.0 (22 Kasim 2026)"
tzlog = logging.getLogger("tezgah2_veri")
if not tzlog.handlers:
    _h = logging.StreamHandler(sys.stdout)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    tzlog.addHandler(_h)
    tzlog.setLevel(logging.INFO)

TZ_AYAR: Dict[str, Any] = {
    "kok": "/root/.kasa/ham/veri3",
    "eski": "/root/.kasa/ham/veri",
    "baslangic": "2000-01-03",
    "parca": 60,            # parca basina sembol
    "bekle": 1.5,           # parcalar arasi sn
    "deneme": 3,
    "hiz_bekle": 90,        # hiz siniri hatasinda sn
    "min_bar": 150,         # fi_k1_veri ile ayni
    "url_nasdaq": "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt",
    "url_diger": "https://www.nasdaqtrader.com/dynamic/symdir/otherlisted.txt",
    # AVR para birimi eslemesi: fi_avr_evren ile birebir
    "para": {"United Kingdom": "GBp", "Bermuda": "GBp", "Israel": "GBp", "Switzerland": "CHF", "Sweden": "SEK",
             "Denmark": "DKK", "Norway": "NOK", "Poland": "PLN"},
    "fx": {"GBp": "EURGBP=X", "GBP": "EURGBP=X", "CHF": "EURCHF=X", "SEK": "EURSEK=X", "DKK": "EURDKK=X",
           "NOK": "EURNOK=X", "PLN": "EURPLN=X"},
}
# Elenen adlar (warrant / unit / right / preferred / tahvil / fon): ad deseni
TZ_ELE_AD = re.compile(
    r"\bwarrants?\b|\brights?\b|\bpreferred\b|\bpreference\b|\bnotes?\b|\bdebentures?\b|\bsubordinated\b|"
    r"\betf\b|\betn\b|\bexchange[- ]traded\b|\bportfolio\b|\bindex\b|\bdepositary shares?,? each representing (a )?(1/|one[- ](one[- ])?(hundredth|thousandth|fortieth|twentieth)|a fractional)|"
    r"\bcumulative\b|\bconvertible (senior|subordinated)|\btrust preferred\b|% series|\bbond\b|\bproshares\b|\bishares\b|\bspdr\b|\bvaneck\b|"
    r"\bwisdomtree\b|\binvesco (qqq|s&p)|\bleveraged\b|\binverse\b|\bproceeds\b|\bliquidating trust\b|\bliquidating\b",
    re.I)
TZ_UNIT = re.compile(r"\bunits?\b", re.I)
TZ_UNIT_OK = re.compile(r"common units?|limited partner|ordinary units?|limited liability company interests?", re.I)
TZ_FUND = re.compile(r"\bfunds?\b", re.I)
TZ_BDC = re.compile(r"\b(capital|lending|bdc|finance|financial)\b", re.I)
TZ_ADR = re.compile(r"american depositary|\bADS\b|\bADR\b|depositary shares", re.I)
TZ_SPAC = re.compile(r"acquisition (corp|co\b|company|holdings|limited|ltd)|blank check|\bspac\b|merger corp|capital corp\.? [ivx]+\b", re.I)
TZ_BORSA = {"N": "NYSE", "A": "NYSE American", "Q": "Nasdaq", "G": "Nasdaq", "S": "Nasdaq"}


def tz_ad_ele(ad: str) -> bool:
    """True = ad warrant / unit / right / preferred / tahvil / fon gibi adi hisse DEGIL. Istisna: 'Common Units / Limited Partner' (MLP),
    kapali uclu fon etiketli BDC'ler (Capital / Lending / BDC / Finance)."""
    if TZ_ELE_AD.search(ad):
        return True
    if TZ_UNIT.search(ad) and not TZ_UNIT_OK.search(ad):
        return True
    if TZ_FUND.search(ad) and not ((re.search(r"closed end fund|lending fund", ad, re.I)) and TZ_BDC.search(ad)):
        return True
    return False


class TZHata(RuntimeError):
    """Durdurucu hata: girdi / yol / liste bozuk."""


def tz_yol(*p: str) -> str:
    d = os.path.join(TZ_AYAR["kok"], *p)
    os.makedirs(os.path.dirname(d) if os.path.splitext(d)[1] else d, exist_ok=True)
    return d


def tz_ham_dir() -> str:
    d = os.path.join(TZ_AYAR["kok"], "ham"); os.makedirs(d, exist_ok=True)
    return d


def tz_yahoo_kod(s: str) -> str:
    """nasdaqtrader ACT sembolu -> Yahoo kodu (BRK.B -> BRK-B)."""
    return s.strip().upper().replace(".", "-")


# ================================================================ 1) EVREN
def tz_evren_ayristir(nasdaq_txt: str, diger_txt: str, eski: Optional[List[str]] = None) -> pd.DataFrame:
    """nasdaqlisted + otherlisted metinlerinden adi hisse evreni. Elenen: test, ETF, fon / tahvil / warrant / unit / right / preferred,
    NYSE Arca / Cboe / IEX tek kayitlari (ETF agirlikli; NYSE, NYSE American, Nasdaq istenir). 'eski' listesindeki sembol listede yoksa
    borsa='eski_liste' ile eklenir (V_ABD 1.411 kapsamasi)."""
    def oku(txt: str) -> pd.DataFrame:
        satir = [x for x in txt.splitlines() if x and not x.startswith("File Creation")]
        bas = satir[0].split("|")
        return pd.DataFrame([x.split("|") for x in satir[1:]], columns=bas)
    n = oku(nasdaq_txt); o = oku(diger_txt)
    A = pd.DataFrame({"sembol": n["Symbol"], "ad": n["Security Name"], "borsa": n["Market Category"].map(TZ_BORSA).fillna("Nasdaq"),
                      "test": n["Test Issue"], "etf": n["ETF"], "durum": n["Financial Status"]})
    B = pd.DataFrame({"sembol": o["ACT Symbol"], "ad": o["Security Name"], "borsa": o["Exchange"].map(TZ_BORSA),
                      "test": o["Test Issue"], "etf": o["ETF"], "durum": ""})
    E = pd.concat([A, B], ignore_index=True)
    E["ad"] = E["ad"].astype(str).str.strip(); E["sembol"] = E["sembol"].astype(str).str.strip()
    E["sec"] = (E.test != "Y") & (E.etf != "Y") & E.borsa.notna() & ~E.sembol.str.contains(r"\$|\^|=|/| ", regex=True) & ~E.ad.map(tz_ad_ele)
    elenen = E[~E.sec]
    E = E[E.sec].drop(columns=["sec", "test", "etf"]).drop_duplicates("sembol").copy()
    E["yahoo"] = E.sembol.map(tz_yahoo_kod)
    E["adr"] = E.ad.str.contains(TZ_ADR.pattern, case=False, regex=True).astype(int); E["spac"] = E.ad.str.contains(TZ_SPAC.pattern, case=False, regex=True).astype(int)
    if eski:
        var = set(E.yahoo)
        ek = [s for s in eski if s not in var]
        if ek:
            E = pd.concat([E, pd.DataFrame({"sembol": ek, "ad": "", "borsa": "eski_liste", "durum": "", "yahoo": ek, "adr": 0, "spac": 0})], ignore_index=True)
    E = E.drop_duplicates("yahoo").sort_values("yahoo").reset_index(drop=True)
    E.attrs["elenen"] = len(elenen)
    return E


def tz_evren_sec_yedek(js: Dict[str, Any], eski: Optional[List[str]] = None) -> pd.DataFrame:
    """Yedek: SEC company_tickers.json ({'0': {'cik_str','ticker','title'}}). Borsa bilgisi yok ('SEC')."""
    satir = [(v["ticker"], v["title"]) for v in js.values()]
    E = pd.DataFrame(satir, columns=["sembol", "ad"]); E["borsa"] = "SEC"; E["durum"] = ""
    E = E[~E.ad.map(tz_ad_ele) & ~E.sembol.str.contains(r"\$|\^|=|/| ", regex=True)].copy()
    E["yahoo"] = E.sembol.map(tz_yahoo_kod); E["adr"] = E.ad.str.contains(TZ_ADR.pattern, case=False, regex=True).astype(int); E["spac"] = E.ad.str.contains(TZ_SPAC.pattern, case=False, regex=True).astype(int)
    if eski:
        ek = [s for s in eski if s not in set(E.yahoo)]
        if ek:
            E = pd.concat([E, pd.DataFrame({"sembol": ek, "ad": "", "borsa": "eski_liste", "durum": "", "yahoo": ek, "adr": 0, "spac": 0})], ignore_index=True)
    return E.drop_duplicates("yahoo").sort_values("yahoo").reset_index(drop=True)


def tz_evren_abd() -> pd.DataFrame:
    """evren2_ABD.csv uretir (indirme oncesi; ilk / son bar sutunlari birlestir adiminda dolar)."""
    import urllib.request
    eski = sorted(str(s) for s in pickle.load(open(os.path.join(TZ_AYAR["eski"], "V_ABD.pkl"), "rb")))
    try:
        ua = {"User-Agent": "Mozilla/5.0"}
        n = urllib.request.urlopen(urllib.request.Request(TZ_AYAR["url_nasdaq"], headers=ua), timeout=60).read().decode("utf-8", "replace")
        o = urllib.request.urlopen(urllib.request.Request(TZ_AYAR["url_diger"], headers=ua), timeout=60).read().decode("utf-8", "replace")
        E = tz_evren_ayristir(n, o, eski); kaynak = "nasdaqtrader"
        open(tz_yol("nasdaqlisted.txt"), "w").write(n); open(tz_yol("otherlisted.txt"), "w").write(o)
    except Exception as ex:
        tzlog.warning("nasdaqtrader erisilemedi (%s); SEC yedegi", ex)
        yol = "/tmp/iv_veri/secfs/company_tickers.json"
        if not os.path.exists(yol):
            raise TZHata("ne nasdaqtrader ne yerel company_tickers.json var")
        E = tz_evren_sec_yedek(json.load(open(yol)), eski); kaynak = "sec_company_tickers"
    E.attrs["kaynak"] = kaynak
    tzlog.info("ABD evreni: %d (kaynak %s, elenen %s, eski listeden eklenen %d)", len(E), kaynak, E.attrs.get("elenen"), int((E.borsa == "eski_liste").sum()))
    E.to_csv(tz_yol("evren2_ABD_ham.csv"), index=False)
    return E


def tz_evren_avr() -> pd.DataFrame:
    V = pickle.load(open(os.path.join(TZ_AYAR["eski"], "V_AVR.pkl"), "rb"))
    kodlar = sorted(str(s) for s in V)
    ul = {}
    p = "/tmp/iv_veri/avr/evren_avr_ham.csv"
    if os.path.exists(p):
        ul = pd.read_csv(p).set_index("kod").ulke.to_dict()
    return pd.DataFrame({"yahoo": kodlar, "ulke": [ul.get(k, "") for k in kodlar]})


# ================================================================ 2) INDIRME
def tz_parcala(kodlar: List[str], n: int) -> List[List[str]]:
    kodlar = sorted(set(kodlar))
    return [kodlar[i:i + n] for i in range(0, len(kodlar), n)]


def tz_cikar(ham: pd.DataFrame, kodlar: List[str]) -> Tuple[Dict[str, pd.DataFrame], List[str]]:
    """yf.download(group_by='ticker', actions=True) sonucundan {kod: OHLCV + 'Stock Splits'} ve bos kodlar."""
    out: Dict[str, pd.DataFrame] = {}; yok: List[str] = []
    for k in kodlar:
        try:
            d = ham[k] if isinstance(ham.columns, pd.MultiIndex) else ham
            d = d.dropna(subset=["Open", "High", "Low", "Close"], how="all")
            if len(d) == 0:
                yok.append(k); continue
            kol = [c for c in ("Open", "High", "Low", "Close", "Volume", "Stock Splits") if c in d.columns]
            out[k] = d[kol].copy()
        except Exception:
            yok.append(k)
    return out, yok


def tz_indir_parca(kodlar: List[str]) -> Tuple[Dict[str, pd.DataFrame], List[str]]:
    import yfinance as yf
    son = None
    for dnm in range(1, TZ_AYAR["deneme"] + 1):
        try:
            ham = yf.download(kodlar, start=TZ_AYAR["baslangic"], auto_adjust=True, actions=True, group_by="ticker",
                              progress=False, threads=True, timeout=40)
            if ham is None or len(ham) == 0:
                raise RuntimeError("bos yanit")
            return tz_cikar(ham, kodlar)
        except Exception as ex:
            son = ex
            hiz = "ratelimit" in type(ex).__name__.lower() or "too many" in str(ex).lower() or "429" in str(ex)
            bekle = TZ_AYAR["hiz_bekle"] * dnm if hiz else 10 * dnm
            tzlog.warning("parca hatasi (deneme %d): %s -> %ds bekle", dnm, ex, bekle); time.sleep(bekle)
    raise TZHata(f"parca indirilemedi: {son}")


def tz_tek(kod: str) -> Optional[pd.DataFrame]:
    import yfinance as yf
    for dnm in range(1, TZ_AYAR["deneme"] + 1):
        try:
            d = yf.Ticker(kod).history(start=TZ_AYAR["baslangic"], auto_adjust=True, actions=True)
            if d is not None and len(d):
                if getattr(d.index, "tz", None) is not None:
                    d.index = d.index.tz_localize(None)
                d.index = d.index.normalize()
                kol = [c for c in ("Open", "High", "Low", "Close", "Volume", "Stock Splits") if c in d.columns]
                return d[kol].dropna(subset=["Open", "High", "Low", "Close"], how="all")
            return None
        except Exception as ex:
            tzlog.warning("%s tek indirme hatasi (%d): %s", kod, dnm, ex); time.sleep(5 * dnm)
    return None


def tz_indir(pazar: str, kodlar: List[str]) -> Dict[str, Any]:
    """Parca parca indirir; parca dosyasi varsa atlar (kaldigi yerden). Sonra bos kalanlari tek tek dener."""
    ham_d = tz_ham_dir()
    parcalar = tz_parcala(kodlar, TZ_AYAR["parca"]); yok_hepsi: List[str] = []
    for i, p in enumerate(parcalar):
        f = os.path.join(ham_d, f"{pazar}_p{i:04d}.pkl")
        if os.path.exists(f):
            continue
        t0 = time.time()
        veri, yok = tz_indir_parca(p)
        tmp = f + ".tmp"
        pickle.dump({"kodlar": p, "veri": veri, "yok": yok}, open(tmp, "wb")); os.replace(tmp, f)
        tzlog.info("%s parca %d/%d: %d veri, %d bos (%.0fs)", pazar, i + 1, len(parcalar), len(veri), len(yok), time.time() - t0)
        time.sleep(TZ_AYAR["bekle"])
    # bos kalanlari tek tek yeniden dene (bir kez)
    tek_f = os.path.join(ham_d, f"{pazar}_tek.pkl")
    tek = pickle.load(open(tek_f, "rb")) if os.path.exists(tek_f) else {"veri": {}, "denendi": []}
    for fn in sorted(os.listdir(ham_d)):
        if fn.startswith(pazar + "_p") and fn.endswith(".pkl"):
            yok_hepsi += pickle.load(open(os.path.join(ham_d, fn), "rb"))["yok"]
    bekleyen = [k for k in yok_hepsi if k not in tek["denendi"]]
    tzlog.info("%s: %d bos sembol tek tek denenecek", pazar, len(bekleyen))
    for j, k in enumerate(bekleyen):
        d = tz_tek(k)
        if d is not None:
            tek["veri"][k] = d
        tek["denendi"].append(k)
        if (j + 1) % 25 == 0 or j + 1 == len(bekleyen):
            pickle.dump(tek, open(tek_f + ".tmp", "wb")); os.replace(tek_f + ".tmp", tek_f)
        time.sleep(0.3)
    return {"parca": len(parcalar), "bos": len(yok_hepsi), "tek_kurtarilan": len(tek["veri"])}


def tz_ham_topla(pazar: str) -> Tuple[Dict[str, pd.DataFrame], List[str]]:
    d = tz_ham_dir()
    veri: Dict[str, pd.DataFrame] = {}; yok: List[str] = []
    for fn in sorted(os.listdir(d)):
        if fn.startswith(pazar + "_p") and fn.endswith(".pkl"):
            z = pickle.load(open(os.path.join(d, fn), "rb")); veri.update(z["veri"]); yok += z["yok"]
    tf = os.path.join(d, f"{pazar}_tek.pkl")
    if os.path.exists(tf):
        veri.update(pickle.load(open(tf, "rb"))["veri"])
    yok = sorted(set(k for k in yok if k not in veri))
    return veri, yok


# ================================================================ 3) BICIM
def tz_temizle(d: pd.DataFrame, bugun: Optional[str] = None) -> pd.DataFrame:
    """fi_k1_veri ile ayni suzgec (H>=L, Close>0, bos OHLC atilir) + bugunku (yarim olabilir) bar atilir (K3).
    Indeks 'Date' datetime64[s]; sutunlar Open High Low Close Volume float; 'Price' sutun adi (V_*.pkl gibi)."""
    d = d.copy()
    if getattr(d.index, "tz", None) is not None:
        d.index = d.index.tz_localize(None)
    d.index = pd.DatetimeIndex(d.index).normalize()
    d = d[~d.index.duplicated(keep="last")]
    d = d.dropna(subset=["Open", "High", "Low", "Close"])
    d = d[(d.High >= d.Low) & (d.Close > 0)].sort_index()
    if bugun is None:
        bugun = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")
    d = d[d.index < pd.Timestamp(bugun)]
    if "Volume" not in d.columns:
        d["Volume"] = np.nan
    d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float)
    d.index = d.index.astype("datetime64[s]"); d.index.name = "Date"; d.columns.name = "Price"
    return d


def tz_avr_duzelt(d: pd.DataFrame, para: str, fx: Dict[str, pd.Series]) -> Tuple[Optional[pd.DataFrame], str]:
    """fi_avr_evren ile ayni mantik: 80-125x sicrama -> 100'e bol / carp; baska >=20x sicrama -> (None, 'sicrama'); Kur ekler."""
    d = d.copy()
    r = (d.Close / d.Close.shift(1)).to_numpy(float); carpan = np.ones(len(d)); kot = False
    for i in np.flatnonzero((r >= 20) | (r <= 0.05)):
        if 80 <= r[i] <= 125:
            carpan[i:] /= 100.0
        elif 1 / 125 <= r[i] <= 1 / 80:
            carpan[i:] *= 100.0
        else:
            kot = True
    if kot:
        return None, "aciklanamayan fiyat sicramasi"
    if (carpan != 1).any():
        for kol in ("Open", "High", "Low", "Close"):
            d[kol] = d[kol] * carpan
        if para == "GBp" and carpan[-1] < 1:
            para = "GBP"
    if para == "EUR":
        d["Kur"] = 1.0
    else:
        f = fx.get("GBp" if para == "GBP" else para)
        if f is None:
            return None, "kur yok"
        k = f.reindex(d.index).ffill().bfill().astype(float)
        d["Kur"] = (k / 100.0) if para == "GBp" else k
    return d, ""


def tz_fx_indir() -> Dict[str, pd.Series]:
    """Kur serileri: 1 / EURxxx=X kapanis (yerel para birimi basina EUR). Onbellek: ham/fx.pkl."""
    f = os.path.join(tz_ham_dir(), "fx.pkl")
    if os.path.exists(f):
        return pickle.load(open(f, "rb"))
    import yfinance as yf
    out = {}
    for ad, kod in TZ_AYAR["fx"].items():
        if ad == "GBP":
            continue
        for dnm in range(TZ_AYAR["deneme"]):
            try:
                x = yf.download(kod, start=TZ_AYAR["baslangic"], auto_adjust=True, progress=False)["Close"].squeeze()
                x.index = pd.DatetimeIndex(x.index).tz_localize(None) if getattr(x.index, "tz", None) else x.index
                out[ad] = (1.0 / x).dropna().astype(float); break
            except Exception as ex:
                tzlog.warning("%s kuru hatasi: %s", kod, ex); time.sleep(10)
    pickle.dump(out, open(f, "wb"))
    return out


def tz_birlestir(pazar: str) -> Dict[str, Any]:
    veri, yok = tz_ham_topla(pazar)
    V: Dict[str, pd.DataFrame] = {}; atilan: List[Tuple[str, str]] = []; splits: Dict[str, pd.Series] = {}
    fx = tz_fx_indir() if pazar == "AVR" else {}
    ul: Dict[str, str] = {}
    if pazar == "AVR":
        e = tz_evren_avr(); ul = e.set_index("yahoo").ulke.to_dict()
    for k, d0 in sorted(veri.items()):
        try:
            if "Stock Splits" in d0.columns:
                sp = d0["Stock Splits"].dropna(); sp = sp[sp != 0]
                if len(sp):
                    sp.index = pd.DatetimeIndex(sp.index).tz_localize(None).normalize() if getattr(sp.index, "tz", None) is not None else pd.DatetimeIndex(sp.index).normalize()
                    splits[k] = sp
            d = tz_temizle(d0)
            if len(d) < TZ_AYAR["min_bar"]:
                atilan.append((k, f"bar<{TZ_AYAR['min_bar']} ({len(d)})")); continue
            if pazar == "AVR":
                d, neden = tz_avr_duzelt(d, TZ_AYAR["para"].get(ul.get(k, ""), "EUR"), fx)
                if d is None:
                    atilan.append((k, neden)); continue
                d.index = d.index.astype("datetime64[s]"); d.index.name = "Date"; d.columns.name = "Price"
            V[k] = d
        except Exception as ex:
            atilan.append((k, f"hata {ex}"))
    cikti = tz_yol(f"V_{pazar}2.pkl")
    pickle.dump(V, open(cikti + ".tmp", "wb"), protocol=4); os.replace(cikti + ".tmp", cikti)
    pickle.dump(splits, open(os.path.join(tz_ham_dir(), f"splits_{pazar}.pkl"), "wb"))
    pd.DataFrame(atilan, columns=["sembol", "neden"]).to_csv(tz_yol(f"atilan_{pazar}.csv"), index=False)
    pd.DataFrame({"sembol": yok}).to_csv(tz_yol(f"indirilemeyen_{pazar}.csv"), index=False)
    tzlog.info("%s: V_%s2 %d sembol, atilan %d, indirilemeyen %d", pazar, pazar, len(V), len(atilan), len(yok))
    return {"yazilan": len(V), "atilan": len(atilan), "indirilemeyen": len(yok)}


# ================================================================ 4) KALITE
def tz_gecerlilik(d: pd.DataFrame) -> pd.DataFrame:
    """Yil yil bar gecerliligi sayimlari (tek hisse; toplamak icin yil bazinda satir)."""
    e = 1e-9
    h_l = d.High < d.Low
    aralik_disi = (d.Open > d.High * (1 + 1e-6)) | (d.Open < d.Low * (1 - 1e-6)) | (d.Close > d.High * (1 + 1e-6)) | (d.Close < d.Low * (1 - 1e-6))
    v0 = d.Volume.fillna(0) <= 0
    hl = (d.High - d.Low).abs() <= e * d.Close.abs()
    G = pd.DataFrame({"bar": 1, "h_lt_l": h_l.astype(int), "aralik_disi": aralik_disi.astype(int), "hacim0": v0.astype(int), "h_eq_l": hl.astype(int)})
    return G.groupby(d.index.year).sum()


def tz_sicrama(d: pd.DataFrame, bolunme: Optional[pd.Series] = None) -> Dict[str, Any]:
    """|gunluk getiri|>%50 gun sayisi (ve bolunme gunu +-1 is gunu ile eslesme), sicra-geri don (>%40, ertesi gun geri), ters bolunme gunu sureklilik."""
    c = d.Close; r = c.pct_change().dropna()
    buyuk = r[r.abs() > 0.5]
    esles = 0
    bol_gunleri = set()
    if bolunme is not None and len(bolunme):
        for t in bolunme.index:
            i = d.index.searchsorted(t)
            for j in (i - 1, i, i + 1):
                if 0 <= j < len(d):
                    bol_gunleri.add(d.index[j])
        esles = int(sum(1 for t in buyuk.index if t in bol_gunleri))
    r1 = r.shift(-1)
    net2 = (1 + r) * (1 + r1) - 1
    geri = int(((r.abs() > 0.4) & (r * r1 < 0) & (net2.abs() < 0.1)).sum())
    ters_sureksiz = 0; ters_n = 0
    if bolunme is not None:
        for t, oran in bolunme.items():
            if oran < 1:     # ters bolunme: yfinance 'Stock Splits' 1/10 gibi 0.1 verir
                ters_n += 1
                if t in r.index and abs(r.loc[t]) > 0.4:
                    ters_sureksiz += 1
    return {"buyuk50": int(len(buyuk)), "buyuk50_bolunme_esli": esles, "sicra_geri": geri, "ters_bolunme": ters_n, "ters_sureksiz": ters_sureksiz}


def tz_oran_tutarlilik(yeni: pd.DataFrame, eski: pd.DataFrame) -> Dict[str, float]:
    """Ortak gunlerde yeni/eski oranin hisse ici degisim katsayisi (std / ortalama); OHLC ve hacim."""
    ort = yeni.index.intersection(eski.index)
    out: Dict[str, float] = {"ortak_gun": float(len(ort))}
    if len(ort) < 30:
        return out
    for k in ("Open", "High", "Low", "Close", "Volume"):
        o = (yeni.loc[ort, k] / eski.loc[ort, k].replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).dropna()
        out["cv_" + k] = float(o.std() / o.mean()) if len(o) > 5 and o.mean() != 0 else float("nan")
        if k == "Close":
            out["oran_ort"] = float(o.mean()); out["oran_min"] = float(o.min()); out["oran_max"] = float(o.max())
            out["oran_son"] = float(o.iloc[-1]) if len(o) else float("nan")
    return out


def tz_yinelenen(V: Dict[str, pd.DataFrame], ad: Optional[Dict[str, str]] = None) -> Dict[str, List[List[str]]]:
    """Ayni kapanis serisine sahip (son 250 gun, 4 hane) semboller = ayni sirketin iki kodu; ad esitligi (sinif A / B kaldirilmis) = sinif bayragi."""
    h: Dict[str, List[str]] = {}
    for k, d in V.items():
        if len(d) < 250:
            continue
        x = d.Close.iloc[-250:].round(4)
        h.setdefault(hashlib.md5(x.to_numpy().tobytes() + str(x.index[0]).encode()).hexdigest(), []).append(k)
    ayni = [sorted(v) for v in h.values() if len(v) > 1]
    sinif: List[List[str]] = []
    if ad:
        g: Dict[str, List[str]] = {}
        for k in V:
            a = ad.get(k, "")
            if not a:
                continue
            a = re.sub(r"\b(class|series)\s+[a-z0-9]\b|\bcommon stock\b|\bordinary shares?\b|\bshares?\b|\bcapital stock\b|[^a-z0-9 ]", " ", a.lower())
            a = re.sub(r"\s+", " ", a).strip()
            if a:
                g.setdefault(a, []).append(k)
        sinif = [sorted(v) for v in g.values() if len(v) > 1]
    return {"ayni_seri": ayni, "ad_esit": sinif}


def tz_aktif_yil(V: Dict[str, pd.DataFrame], yillar: Tuple[int, int] = (2000, 2026)) -> Dict[int, int]:
    out = {y: 0 for y in range(yillar[0], yillar[1] + 1)}
    for d in V.values():
        for y in np.unique(d.index.year):
            if int(y) in out:
                out[int(y)] += 1
    return out


def tz_kalite(pazar: str) -> Dict[str, Any]:
    V = pickle.load(open(tz_yol(f"V_{pazar}2.pkl"), "rb"))
    eski = pickle.load(open(os.path.join(TZ_AYAR["eski"], f"V_{pazar}.pkl"), "rb"))
    spl = pickle.load(open(os.path.join(tz_ham_dir(), f"splits_{pazar}.pkl"), "rb"))
    R: Dict[str, Any] = {"pazar": pazar, "sembol": len(V), "eski_sembol": len(eski), "eski_olup_yenide_yok": sorted(set(eski) - set(V))}
    R["veri_sonu"] = str(max(d.index.max() for d in V.values()).date()); R["veri_basi"] = str(min(d.index.min() for d in V.values()).date())
    R["aktif_yil"] = tz_aktif_yil(V)
    ilk = pd.Series({k: d.index.min().year for k, d in V.items()}); R["ilk_bar_yil"] = {int(k): int(v) for k, v in ilk.value_counts().sort_index().items()}
    # b) eski veriyle ortusme
    S = []
    for k in sorted(set(V) & set(eski)):
        try:
            S.append({"sembol": k, **tz_oran_tutarlilik(V[k], eski[k])})
        except Exception as ex:
            S.append({"sembol": k, "hata": str(ex)})
    S = pd.DataFrame(S)
    R["ortak_sembol"] = int(len(S))
    sup: List[Dict[str, Any]] = []
    if len(S) and "cv_Close" in S:
        S.to_csv(tz_yol(f"oran_{pazar}.csv"), index=False)
        for k in ("Open", "High", "Low", "Close", "Volume"):
            c = S["cv_" + k].dropna()
            R[f"cv_{k}"] = {"n": int(len(c)), "medyan": float(c.median()), "p95": float(c.quantile(0.95)), "max": float(c.max()), "1pct_ustu": int((c > 0.01).sum())}
        for _, x in S[S.cv_Close > 0.01].iterrows():
            sup.append({"sembol": x.sembol, "neden": f"eski/yeni kapanis orani CV {x.cv_Close:.4f} > %1"})
        R["oran_ort_dagilim"] = {"min": float(S.oran_ort.min()), "medyan": float(S.oran_ort.median()), "max": float(S.oran_ort.max()),
                                  "oran_1den_uzak_5pct": int(((S.oran_ort - 1).abs() > 0.05).sum())}
    # c) bar gecerliligi + d) sicrama
    G = []; J = []
    for k, d in V.items():
        g = tz_gecerlilik(d); g["sembol"] = k; G.append(g.reset_index().rename(columns={"index": "yil"}))
        j = tz_sicrama(d, spl.get(k)); j["sembol"] = k; J.append(j)
    G = pd.concat(G); Y = G.groupby("yil")[["bar", "h_lt_l", "aralik_disi", "hacim0", "h_eq_l"]].sum()
    R["bar_gecerlilik_yil"] = {int(y): {c: int(Y.loc[y, c]) for c in Y.columns} for y in Y.index}
    R["bar_toplam"] = {c: int(Y[c].sum()) for c in Y.columns}
    J = pd.DataFrame(J)
    R["sicrama"] = {c: int(J[c].sum()) for c in ("buyuk50", "buyuk50_bolunme_esli", "sicra_geri", "ters_bolunme", "ters_sureksiz")}
    R["sicrama"]["bolunme_olay_sayisi"] = int(sum(len(v) for v in spl.values()))
    for _, x in J[(J.sicra_geri > 0) | (J.ters_sureksiz > 0) | (J.buyuk50 - J.buyuk50_bolunme_esli >= 3)].iterrows():
        sup.append({"sembol": x.sembol, "neden": f"sicra_geri {x.sicra_geri}, bolunmesiz >50% gun {x.buyuk50 - x.buyuk50_bolunme_esli}, ters_sureksiz {x.ters_sureksiz}"})
    # e) yinelenen
    ad = None
    f = tz_yol("evren2_ABD_ham.csv") if pazar == "ABD" else None
    if f and os.path.exists(f):
        ad = pd.read_csv(f, keep_default_na=False, dtype=str).set_index("yahoo").ad.to_dict()
    Y2 = tz_yinelenen(V, ad)
    R["yinelenen"] = {"ayni_seri_grup": len(Y2["ayni_seri"]), "ayni_seri": Y2["ayni_seri"][:80], "ad_esit_grup": len(Y2["ad_esit"]), "ad_esit_ornek": Y2["ad_esit"][:40]}
    for g in Y2["ayni_seri"]:
        for k in g:
            sup.append({"sembol": k, "neden": "ayni kapanis serisi: " + "/".join(g)})
    # f) hayatta kalma notu
    a = R["aktif_yil"]
    R["hayatta_kalma"] = {"aktif_2000": a.get(2000), "aktif_2025": a.get(2025), "oran_2000_2025": round(a.get(2000, 0) / max(a.get(2025, 1), 1), 3),
                          "not": "evren yalniz bugun yasayanlar; 2000-2010'da gercek aktif hisse sayisi kaynak yok: bilinmiyor"}
    sup_df = pd.DataFrame(sup).drop_duplicates() if sup else pd.DataFrame(columns=["sembol", "neden"])
    sup_df.insert(0, "pazar", pazar)
    sup_df.to_csv(tz_yol(f"supheli_{pazar}.csv"), index=False)
    R["supheli_sayi"] = int(sup_df.sembol.nunique())
    return R


# ================================================================ KOMUT
def _cakisma_kontrol_tz(_once=_CK_ONCE_TZ, _dosya="TEZGAH2_VERI.py"):
    """Cakisma kapisi: bu dosya bellekteki mevcut bir adi (baska dosyanin) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_TZ", "_CK_KAYIT", "_cakisma_kontrol_tz", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "pickle", "warnings", "_dt", "annotations",
           "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki su adlari EZDI -> {ezilen}")


_cakisma_kontrol_tz()
warnings.filterwarnings("ignore", category=FutureWarning)

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=TZ_SURUM)
    ap.add_argument("komut", choices=["evren", "indir", "birlestir", "kalite"])
    ap.add_argument("pazar", nargs="?", default="ABD", choices=["ABD", "AVR"])
    a = ap.parse_args()
    try:
        if a.komut == "evren":
            tz_evren_abd()
        elif a.komut == "indir":
            if a.pazar == "ABD":
                f = tz_yol("evren2_ABD_ham.csv")
                kodlar = list(pd.read_csv(f, keep_default_na=False, dtype=str).yahoo) if os.path.exists(f) else list(tz_evren_abd().yahoo)
            else:
                kodlar = list(tz_evren_avr().yahoo)
            tzlog.info("%s: %d sembol indirilecek", a.pazar, len(kodlar))
            print(json.dumps(tz_indir(a.pazar, kodlar)))
        elif a.komut == "birlestir":
            print(json.dumps(tz_birlestir(a.pazar)))
        else:
            R = tz_kalite(a.pazar)
            json.dump(R, open(tz_yol(f"kalite_{a.pazar}.json"), "w"), indent=1, default=str)
            print("kalite yazildi", a.pazar)
    except TZHata as ex:
        tzlog.error("%s", ex); sys.exit(1)
