"""K56-EVREN2: batan şirketlerle yeni evren sürümü (ONKAYIT_K56 v1.2-C). K51-K55 evren ve sonuçları DEĞİŞMEZ; her şey ayrı klasörde ve ayrı kimlikle.

Adımlar: (1) aday listesi (Ö1 = K34 geçerli batan listesinden Tiingo örnekleminde olmayanlar, K34 eşleme kuralı FON_IZI.fi_k34_* aynen; Ö2 = KEŞİF dönemi
25-NSE başvuruları, SEC tam metin araması + Tiingo bitiş eşleşmesi, tohum 56 rastgele); (2) SEC başvuru geçmişi (data.sec.gov submissions; e-posta yalnız
SEC_EPOSTA); (3) sınıflandırma (COL_YOLU_ABD.cy_v15_sinifla aynen + K56 iflas / tasfiye ayrımı); (4) Tiingo fiyatları (yalnız 1 Kasım 2026 ve sonrası,
saatte en çok 45 istek, kaldığı yerden, kota / 429'da durur); (5) evren v2 kurulumu ve etki ölçümü (evren_v2_* fonksiyonları, sürücüde).
Getiri kuralı (asıl): seri bitince pencere TANIMSIZ; son fiyat tasfiye ödemesi sayılmaz; eksik delist getirisi uydurulmaz.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from .ortak import Istemci, K56Ayar, KaynakKaydi, log

TIINGO_BASLAMA = dt.date(2026, 11, 1)          # Kasım kotası: bu günden önce fiyat isteği YOK (ONKAYIT v1.2-C)
TIINGO_SAATLIK = 45
KOTA_UST = 490
O2_DONEM = ("2016-01-01", "2021-12-31")
BORSALAR = ("NYSE", "NASDAQ", "NYSE MKT", "AMEX")
EFTS = "https://efts.sec.gov/LATEST/search-index?forms=25-NSE&dateRange=custom&startdt={a}&enddt={b}&from={f}"
SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
TASFIYE_AD = r"LIQUIDAT|WIND[\s-]?DOWN|DISSOLUTION|DISSOLV"
SINIF_K56 = {"iflas": "İFLAS", "tasfiye": "TASFİYE", 3: "BİRLEŞME", 4: "SEMBOL DEĞİŞİKLİĞİ", 5: "VERİ SAĞLAYICISI KAYBOLMASI", 6: "DOĞRULANAMAYAN", 1: "HALEN İŞLEM GÖREN"}


def tiingo_listesi(A: K56Ayar) -> pd.DataFrame:
    y = "/tmp/k55/supported_tickers.csv"
    if not os.path.exists(y):
        from K55 import veri_paket
        veri_paket.ac(os.path.join(A.iv, "k55"), "/tmp/k55")
    T = pd.read_csv(y); T["ticker"] = T.ticker.astype(str).str.upper()
    for c in ("startDate", "endDate"):
        T[c] = pd.to_datetime(T[c], errors="coerce")
    return T


def aday_o1(A: K56Ayar, kk: KaynakKaydi, EV: pd.DataFrame, T: pd.DataFrame) -> pd.DataFrame:
    """Ö1: K34 eski kod listesi + K34 eşleme kuralı (FON_IZI.fi_k34_olaylar / fi_k34_tiingo_eslem, değiştirilmeden); K34 Tiingo örneklemi ve K55 evreni dışı."""
    import FON_IZI as F
    eski = pd.read_csv(kk.oku(os.path.join(A.iv, "k34", "k34_eski_kod.csv"), "veri", "K34 batan şirketlerin SEC kapak sayfası eski kodu"))
    orn = pd.read_csv(kk.oku(os.path.join(A.iv, "k34", "k34_orneklem.csv"), "veri", "K34 Tiingo örneklemi (450, zaten evrende)"))
    B = pd.read_pickle(kk.oku(os.path.join(A.veri, "k34_bildirim.pkl"), "veri", "K34 SEC bildirim özeti (olay günleri)"))
    E = F.fi_k34_tiingo_eslem(eski, T.assign(startDate=T.startDate.dt.strftime("%Y-%m-%d"), endDate=T.endDate.dt.strftime("%Y-%m-%d")), F.fi_k34_olaylar(B))
    E = E[E.tiingo.notna() & ~E.cik.isin(orn.cik) & ~E.cik.isin(EV.cik.dropna().astype(int))].copy()
    Ti = T.drop_duplicates("ticker").set_index("ticker"); E["bitis"] = E.tiingo.map(Ti.endDate); E["baslangic"] = E.tiingo.map(Ti.startDate); E["borsa"] = E.tiingo.map(Ti.exchange)
    E = E[E.bitis < pd.Timestamp("2026-08-01")]                     # bugün işlem gören değil
    E["kaynak"] = "Ö1 (K34 kalan)"; E["sembol"] = E.tiingo
    return E[["cik", "sembol", "kaynak", "baslangic", "bitis", "borsa"]].drop_duplicates("cik").reset_index(drop=True)


def efts_25nse(ist: Istemci, bas: str = O2_DONEM[0], son: str = O2_DONEM[1]) -> pd.DataFrame:
    """SEC tam metin aramasında 25-NSE başvuruları (ay ay, sayfalı): cik, görünen ad, sembol (adda varsa), başvuru tarihi."""
    rows = []
    for a in pd.date_range(bas, son, freq="MS"):
        b = a + pd.offsets.MonthEnd(0); f = 0
        while True:
            d, v, _ = ist.al(EFTS.format(a=a.date(), b=b.date(), f=f), ad=f"efts_25nse_{a:%Y%m}_{f}.json", sinir=5_000_000)
            if d != 200:
                log.warning("EFTS %s HTTP %s", a.date(), d); break
            J = json.loads(v.decode()); H = J.get("hits", {}).get("hits", [])
            for h in H:
                s = h.get("_source", {})
                for i, ad in enumerate(s.get("display_names", [])):
                    m = re.search(r"\(([A-Z0-9.\-]{1,6})\)\s*\(CIK (\d{10})\)", ad)
                    if m and "EXCHANGE" not in ad.upper() and "NASDAQ STOCK MARKET" not in ad.upper():
                        rows.append({"cik": int(m.group(2)), "ad": ad.split("(")[0].strip(), "sembol": m.group(1).replace(".", "-"), "nse_tarih": s.get("file_date")})
            f += len(H)
            if not H or f >= int(J.get("hits", {}).get("total", {}).get("value", 0)) or f >= 1000:
                break
    X = pd.DataFrame(rows)
    if len(X):
        X["nse_tarih"] = pd.to_datetime(X.nse_tarih)
    return X.drop_duplicates(["cik", "sembol", "nse_tarih"]).reset_index(drop=True) if len(X) else X


def aday_o2(A: K56Ayar, ist: Istemci, EV: pd.DataFrame, T: pd.DataFrame, n: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Ö2: 25-NSE (KEŞİF dönemi) + Tiingo: aynı sembolün bitişi 25-NSE ±45 gün, Stock, borsa listesi, seri >= 320 işlem günü (~465 takvim günü), K55 evreni
    dışı; tohum 56 rastgele n. Dönüş: (seçilen, bütün uygun havuz)."""
    X = efts_25nse(ist)
    Ts = T[(T.assetType == "Stock") & T.exchange.isin(BORSALAR)].drop_duplicates("ticker").set_index("ticker")
    X = X[X.sembol.isin(Ts.index)].copy(); X["bitis"] = X.sembol.map(Ts.endDate); X["baslangic"] = X.sembol.map(Ts.startDate); X["borsa"] = X.sembol.map(Ts.exchange)
    X = X[((X.bitis - X.nse_tarih).dt.days.abs() <= 45) & ((X.bitis - X.baslangic).dt.days >= 465)]
    X = X[~X.sembol.isin(set(EV.sembol)) & ~X.cik.isin(EV.cik.dropna().astype(int))].drop_duplicates("cik")
    havuz = X.reset_index(drop=True); rng = np.random.default_rng(56)
    sec = havuz.iloc[rng.permutation(len(havuz))[: max(0, n)]].copy() if len(havuz) else havuz
    sec["kaynak"] = "Ö2 (KEŞİF 25-NSE)"
    return sec[["cik", "sembol", "kaynak", "baslangic", "bitis", "borsa", "nse_tarih", "ad"]].reset_index(drop=True), havuz


def sec_gecmis(ist: Istemci, ciks: List[int], hedef: str) -> Dict[str, Any]:
    """data.sec.gov submissions (+ eski dosyalar) -> sec_ozet biçimi (name, tickers, exchanges, sic, formerNames, form, date, items). Var olanı atlar."""
    out = json.load(open(hedef, encoding="utf-8")) if os.path.exists(hedef) else {}
    for n, c in enumerate(ciks, 1):
        if str(c) in out:
            continue
        try:
            d, v, _ = ist.al(SUBMISSIONS.format(cik=int(c)), ad=f"subm_{int(c)}.json", sinir=40_000_000)
            if d != 200:
                out[str(c)] = {"hata": f"HTTP {d}"}; continue
            J = json.loads(v.decode()); f = J["filings"]["recent"]; form, date, items = list(f["form"]), list(f["filingDate"]), list(f.get("items", [""] * len(f["form"])))
            for fx in J["filings"].get("files", []):
                d2, v2, _ = ist.al("https://data.sec.gov/submissions/" + fx["name"], ad=f"subm_{fx['name']}", sinir=40_000_000)
                if d2 == 200:
                    g = json.loads(v2.decode()); form += g["form"]; date += g["filingDate"]; items += g.get("items", [""] * len(g["form"]))
            out[str(c)] = {"name": J.get("name"), "tickers": J.get("tickers", []), "exchanges": J.get("exchanges", []), "sic": J.get("sic"),
                           "formerNames": J.get("formerNames", []), "form": form, "date": date, "items": items}
        except Exception as ex:
            out[str(c)] = {"hata": f"{type(ex).__name__}: {str(ex)[:120]}"}
        if n % 50 == 0:
            json.dump(out, open(hedef, "w", encoding="utf-8")); log.info("SEC geçmişi %d/%d", n, len(ciks))
    json.dump(out, open(hedef, "w", encoding="utf-8"))
    return out


def siniflandir(aday: pd.DataFrame, sec: Dict[str, Any], T: pd.DataFrame, bugun: Dict[str, int], son_gun: Optional[Dict[str, pd.Timestamp]] = None) -> pd.DataFrame:
    """K54 kuralı (COL_YOLU_ABD.cy_v15_sinifla, değiştirilmeden) + K56 ayrımı. T = fiyat serisinin son günü (indirme öncesi Tiingo bitişi; sonra gerçek son gün)."""
    from K55.ortak import cy
    C = cy(); Ti = T.drop_duplicates("ticker").set_index("ticker"); rows = []
    for r in aday.itertuples():
        s = sec.get(str(int(r.cik))); s = s if (s and "hata" not in s) else None
        tg = Ti.loc[r.sembol].to_dict() if r.sembol in Ti.index else None
        if tg is not None:
            tg = {k: (v.strftime("%Y-%m-%d") if isinstance(v, pd.Timestamp) else v) for k, v in tg.items()}
        son = (son_gun or {}).get(r.sembol, r.bitis)
        k = C.cy_v15_sinifla(r.sembol, son, int(r.cik), s, tg, bugun.get(r.sembol))
        ad = " ".join([str((s or {}).get("name", ""))] + [str(x.get("name", "")) for x in ((s or {}).get("formerNames") or [])]).upper()
        if k["sinif"] == 2:
            k56 = "iflas"
        elif k["sinif"] == 5 and (re.search(TASFIYE_AD, ad) or (k.get("b201_tarih") and not k.get("birlesme_belge_tarih") and k.get("kayit_dis_tarih"))):
            k56 = "tasfiye"
        else:
            k56 = k["sinif"]
        rows.append({**{c: getattr(r, c) for c in aday.columns}, "k54_sinif": k["sinif"], "k54_alt": k.get("alt", ""), "k54_kural": k["kural"], "sinif_k56": SINIF_K56.get(k56, str(k56)),
                     "b103_tarih": k.get("b103_tarih", ""), "b201_tarih": k.get("b201_tarih", ""), "nse25_tarih": k.get("nse25_tarih", ""), "kayit_dis_tarih": k.get("kayit_dis_tarih", ""),
                     "sec_ad": (s or {}).get("name", ""), "sic": (s or {}).get("sic", ""), "sec_var": s is not None})
    return pd.DataFrame(rows)


def tiingo_token() -> str:
    tok = os.environ.get("TIINGO_TOKEN", "").strip()
    if not tok:
        for y in (".env", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")):
            if os.path.exists(y):
                for l in open(y, encoding="utf-8"):
                    if l.startswith("TIINGO_TOKEN="):
                        tok = l.split("=", 1)[1].strip()
    if not tok:
        try:
            from google.colab import userdata          # type: ignore
            tok = userdata.get("TIINGO_TOKEN") or ""
        except Exception:
            pass
    return tok


class KotaDoldu(RuntimeError):
    pass


def tiingo_indir(kodlar: List[str], klasor: str, bugun: Optional[dt.date] = None, saatlik: int = TIINGO_SAATLIK, durum_yolu: Optional[str] = None) -> pd.DataFrame:
    """Tiingo günlük fiyat (2015-01-01 ->), kod başına csv. 1 Kasım 2026'dan önce İSTEK YOK (ValueError). Var olan dosya atlanır; saatte en çok `saatlik`
    istek; 429 ya da kota iletisinde KotaDoldu. Anahtar başlıkta, loglanmaz. Durum tablosu her istekten sonra yazılır (kaldığı yerden sürer)."""
    bugun = bugun or dt.date.today()
    if bugun < TIINGO_BASLAMA:
        raise ValueError(f"Tiingo Kasım kotası {TIINGO_BASLAMA}'den önce kullanılmaz (bugün {bugun}); ONKAYIT_K56 v1.2-C")
    tok = tiingo_token()
    if not tok:
        raise RuntimeError("TIINGO_TOKEN yok (.env ya da Colab gizli anahtarı)")
    import requests
    os.makedirs(klasor, exist_ok=True); s = requests.Session(); s.headers.update({"Content-Type": "application/json", "Authorization": f"Token {tok}"})
    durum = pd.read_csv(durum_yolu).to_dict("records") if (durum_yolu and os.path.exists(durum_yolu)) else []; zaman: List[float] = []
    bitti = {d["sembol"] for d in durum if d.get("durum") in ("indi", "bos")}
    for k in kodlar:
        yol = os.path.join(klasor, f"{k}.csv")
        if os.path.exists(yol) or k in bitti:
            continue
        while len(zaman) >= saatlik and time.time() - zaman[-saatlik] < 3600:
            time.sleep(20)
        try:
            x = s.get(f"https://api.tiingo.com/tiingo/daily/{k}/prices", params={"startDate": "2015-01-01", "format": "csv",
                      "columns": "date,open,high,low,close,volume,adjOpen,adjHigh,adjLow,adjClose,adjVolume"}, timeout=60)
            zaman.append(time.time()); metin = x.text[:300]
            if x.status_code == 200 and x.text.startswith("date"):
                open(yol, "w").write(x.text); dd = "indi" if x.text.count("\n") > 1 else "bos"
            elif x.status_code == 429 or re.search(r"run over|limit|exceed", metin, re.I):
                durum.append({"sembol": k, "durum": "kota", "http": x.status_code, "ileti": metin[:120], "zaman": dt.datetime.now().isoformat()})
                if durum_yolu:
                    pd.DataFrame(durum).to_csv(durum_yolu, index=False)
                raise KotaDoldu(f"Tiingo kota / hız sınırı: HTTP {x.status_code} {metin[:120]}")
            else:
                dd = f"HTTP {x.status_code}"
        except KotaDoldu:
            raise
        except Exception as ex:
            zaman.append(time.time()); dd = f"hata {type(ex).__name__}"
        durum.append({"sembol": k, "durum": dd, "zaman": dt.datetime.now().isoformat()})
        if durum_yolu:
            pd.DataFrame(durum).to_csv(durum_yolu, index=False)
        log.info("Tiingo %s: %s (%d/%d)", k, dd, len(durum), len(kodlar))
    return pd.DataFrame(durum)
