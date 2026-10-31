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
O2_BAG = ("2015-11-01", "2022-02-28")                            # CIK bağlama için 25-NSE penceresi (bitiş ±45 gün)
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
    B = B.assign(cik=pd.to_numeric(B.cik, errors="coerce")).dropna(subset=["cik"]); B["cik"] = B.cik.astype(int)       # bildirim özetinde CIK metin; eski kod listesinde sayı
    olay = F.fi_k34_olaylar(B); eski = eski[eski.cik.isin(set(olay.cik))]          # K34 adayı olmayan (olayı olmayan) CIK eşlemeye girmez (K34'te de girmedi)
    E = F.fi_k34_tiingo_eslem(eski, T.assign(startDate=T.startDate.dt.strftime("%Y-%m-%d"), endDate=T.endDate.dt.strftime("%Y-%m-%d")), olay)
    E = E[E.tiingo.notna() & ~E.cik.isin(orn.cik) & ~E.cik.isin(EV.cik.dropna().astype(int))].copy()
    Ti = T.drop_duplicates("ticker").set_index("ticker"); E["bitis"] = E.tiingo.map(Ti.endDate); E["baslangic"] = E.tiingo.map(Ti.startDate); E["borsa"] = E.tiingo.map(Ti.exchange)
    E = E[E.bitis < pd.Timestamp("2026-08-01")]                     # bugün işlem gören değil
    E["kaynak"] = "Ö1 (K34 kalan)"; E["sembol"] = E.tiingo
    E = E[["cik", "sembol", "kaynak", "baslangic", "bitis", "borsa"]].drop_duplicates("cik").reset_index(drop=True)
    # v1.2-b (fiyat görülmeden): adi hisse olmayan menkul kıymet (SPAC birimi / varant / hak) ve sembolü K55 evreninde başka şirkete ait olanlar indirilmez
    # v1.3 (fiyat görülmeden): indirme öncesi sembol kuralları (sonek, paylaşılan sembol, beklenen gün < 320); işaretler (F / Y) ayrı sütunda
    ev_sem = set(EV.sembol.astype(str).str.upper()); dis, isaret, bit = [], [], []
    for r in E.itertuples():
        if r.sembol in ev_sem:
            dis.append("sembol K55 evreninde (başka CIK; yeniden kullanım)"); isaret.append(""); bit.append(r.bitis); continue
        k, n = indirme_oncesi_suzgec(T, r.sembol, r.borsa, r.baslangic, r.bitis); d = devam_satiri(T, r.sembol, r.baslangic, r.bitis)
        dis.append(n if k == "DIŞI" else ""); isaret.append(n if k == "İŞARET" else ""); bit.append(d.endDate if (d is not None and k != "DIŞI") else r.bitis)
    E["dislama"] = dis; E["isaret_on"] = isaret; E["bitis"] = bit                # OTC devamında seri sonu = devam satırının bitişi
    return E[E.dislama == ""].drop(columns="dislama").reset_index(drop=True), E[E.dislama != ""].reset_index(drop=True)


def sonek_sinifi(sembol: str, borsa: str) -> Tuple[str, str]:
    """v1.3 C-2 (indirme öncesi, yalnız sembol + borsa): ('DIŞI' | 'İŞARET' | '', neden). NASDAQ / OTC 5 harf ve 5. harf G H I L M N O P R T U W X Z -> DIŞI
    (imtiyazlı, borç senedi, birim, varant, hak ...); NYSE / NYSE MKT / AMEX 5 harf ve son harf Q değil -> DIŞI; -U / -WS / -R biçimleri -> DIŞI;
    5. harf F / Y -> İŞARET (yabancı / ADR)."""
    s = str(sembol).upper(); b = str(borsa).upper()
    if adi_hisse_degil(s) and ("-" in s):
        return "DIŞI", "sembol biçimi (birim / varant / hak)"
    if len(s) == 5 and s.isalpha():
        if b in ("NYSE", "NYSE MKT", "AMEX", "NYSE ARCA") and s[-1] != "Q":
            return "DIŞI", "NYSE grubunda 5 harf (adi hisse değil)"
        if s[-1] in "GHILMNOPRTUWXZ":
            return "DIŞI", f"5. harf {s[-1]} (adi hisse değil)"
        if s[-1] in "FY":
            return "İŞARET", f"5. harf {s[-1]} (yabancı / ADR)"
    return "", ""


def cakisan_satir(T: pd.DataFrame, sembol: str, bas: pd.Timestamp, bitis: pd.Timestamp, gun: int = 14) -> int:
    """v1.3: aynı sembolün adayın kendi satırı dışında, aday bitişinden gun günden fazla sonra biten başka Tiingo satırı sayısı (API yeni varlığı döndürür).
    Devam satırı (aday bitişinden en çok 10 iş günü sonra başlayan; aynı şirketin OTC devamı) sayılmaz: devam_satiri ile ayrı işaretlenir."""
    g = T[T.ticker == str(sembol).upper()]
    g = g[~((g.startDate == pd.Timestamp(bas)) & (g.endDate == pd.Timestamp(bitis)))]
    g = g[g.endDate > pd.Timestamp(bitis) + pd.Timedelta(days=gun)]
    devam = np.array([pd.notna(x) and pd.Timestamp(bitis) <= x and len(pd.bdate_range(pd.Timestamp(bitis), x)) - 1 <= 10 for x in g.startDate], dtype=bool)
    return int((~devam).sum())


def devam_satiri(T: pd.DataFrame, sembol: str, bas: Any, bitis: Any) -> Optional[pd.Series]:
    """Aday bitişinden en çok 10 iş günü sonra başlayan ve daha geç biten Tiingo satırı (OTC devamı); varsa satır."""
    g = T[(T.ticker == str(sembol).upper()) & (T.endDate > pd.Timestamp(bitis) + pd.Timedelta(days=14))]
    g = g[np.array([pd.notna(x) and pd.Timestamp(bitis) <= x and len(pd.bdate_range(pd.Timestamp(bitis), x)) - 1 <= 10 for x in g.startDate], dtype=bool)]
    return g.sort_values("endDate").iloc[-1] if len(g) else None


def beklenen_gun(bas: Any, bitis: Any, indirme_bas: str = "2015-01-01") -> int:
    return int(len(pd.bdate_range(max(pd.Timestamp(bas), pd.Timestamp(indirme_bas)), pd.Timestamp(bitis))))


def indirme_oncesi_suzgec(T: pd.DataFrame, sembol: str, borsa: str, bas: Any, bitis: Any) -> Tuple[str, str]:
    """v1.3 (fiyat görülmeden): sonek kuralı, paylaşılan sembol, beklenen gün < 320. Dönüş: (DIŞI | İŞARET | '', neden)."""
    k, n = sonek_sinifi(sembol, borsa)
    if k == "DIŞI":
        return k, n
    if cakisan_satir(T, sembol, bas, bitis):
        return "DIŞI", "paylaşılan sembol (adaydan sonra biten başka Tiingo satırı)"
    d = devam_satiri(T, sembol, bas, bitis)
    if d is not None:                                                    # aynı şirketin OTC devamı: yalnız OTC satırı ve bugün işlem görmüyorsa; seri sonu devam satırının bitişi
        if str(d.exchange).upper() not in ("PINK", "EXPM", "OTCMKTS", "OTCQX", "OTCQB", "OTCCE", "OTCGREY", "GREY", "OTC") or d.endDate >= pd.Timestamp("2026-08-01"):
            return "DIŞI", f"devam satırı OTC değil ya da bugün işlem görüyor (Tiingo {d.exchange} {d.startDate.date()}..{d.endDate.date()})"
        bitis = d.endDate; k, n = "İŞARET", "; ".join(x for x in (n, f"OTC devamı (Tiingo {d.exchange} {d.startDate.date()}..{d.endDate.date()})") if x)
    if beklenen_gun(bas, bitis) < 320:
        return "DIŞI", "beklenen işlem günü < 320 (2015 başlangıçlı indirme)"
    return k, n


def adi_hisse_degil(sembol: str) -> bool:
    """Tiingo sembol biçimi: NYSE birim -U / -UN, varant -WS / -WT, hak -R / -RT; NASDAQ 5. harf U (birim), W (varant), R (hak)."""
    s = str(sembol).upper()
    return bool(re.search(r"-(U|UN|WS|WT|W|R|RT)$", s) or (len(s) == 5 and s.isalpha() and s[-1] in "UWR"))


def efts_25nse(ist: Istemci, bas: str = O2_BAG[0], son: str = O2_BAG[1]) -> pd.DataFrame:
    """SEC tam metin aramasında 25-NSE başvuruları (ay ay, sayfalı): ihraççı cik, görünen ad, sembol (SEC'in GÜNCEL sembolü; borsadan çıkanlarda
    çoğunlukla boş), başvuru tarihi. Borsa başvurucuları (NYSE, NASDAQ ...) atılır."""
    rows = []
    for a in pd.date_range(bas, son, freq="MS"):
        b = a + pd.offsets.MonthEnd(0); f = 0
        while True:
            d, v, _ = ist.al(EFTS.format(a=a.date(), b=b.date(), f=f), ad=f"efts_25nse_{a:%Y%m}_{f}.json", sinir=5_000_000)
            if d != 200:
                log.warning("EFTS %s HTTP %s", a.date(), d); break
            J = json.loads(v.decode()); H = J.get("hits", {}).get("hits", [])
            for h in H:
                src = h.get("_source", {})
                for ad in src.get("display_names", []):
                    m = re.search(r"^(.*?)\s*(?:\(([A-Z0-9.,\- ]{1,40})\))?\s*\(CIK (\d{10})\)\s*$", ad.strip())
                    if m and "EXCHANGE" not in ad.upper() and "NASDAQ STOCK MARKET" not in ad.upper():
                        sem = (m.group(2) or "").split(",")[0].strip().replace(".", "-") or None
                        rows.append({"cik": int(m.group(3)), "ad": m.group(1).strip(), "sembol": sem, "nse_tarih": src.get("file_date")})
            f += len(H)
            if not H or f >= int(J.get("hits", {}).get("total", {}).get("value", 0)) or f >= 1000:
                break
    X = pd.DataFrame(rows, columns=["cik", "ad", "sembol", "nse_tarih"])
    X["nse_tarih"] = pd.to_datetime(X.nse_tarih)
    return X.drop_duplicates(["cik", "sembol", "nse_tarih"]).reset_index(drop=True)


def o2_havuz(T: pd.DataFrame, haric: set, bas: str = O2_DONEM[0], son: str = O2_DONEM[1]) -> pd.DataFrame:
    """ONKAYIT v1.2-a Ö2 havuzu: Tiingo Stock, borsa listesi, sembol 1-5 harf, bitiş [bas, son], seri >= 465 takvim günü, sembol bitişten sonra yeniden
    kullanılmamış (sonraki_kullanim=True satırlar havuz tablosunda kalır, seçilmez), `haric` (K55 evreni + Ö1 sembolleri) dışı."""
    Ts = T[(T.assetType == "Stock") & T.exchange.isin(BORSALAR) & T.ticker.str.fullmatch(r"[A-Z]{1,5}") & ~T.ticker.map(adi_hisse_degil)].copy()
    Ts = Ts[(Ts.endDate >= pd.Timestamp(bas)) & (Ts.endDate <= pd.Timestamp(son)) & ((Ts.endDate - Ts.startDate).dt.days >= 465)]
    son_bas = T.groupby("ticker").startDate.max()
    Ts["sonraki_kullanim"] = Ts.ticker.map(son_bas).gt(Ts.endDate).to_numpy()
    Ts["haric"] = Ts.ticker.isin(haric)
    Ts = Ts.rename(columns={"ticker": "sembol", "startDate": "baslangic", "endDate": "bitis", "exchange": "borsa"})
    return Ts[["sembol", "baslangic", "bitis", "borsa", "sonraki_kullanim", "haric"]].sort_values(["sembol", "bitis"]).drop_duplicates("sembol", keep="last").reset_index(drop=True)


def aday_o2(A: K56Ayar, ist: Istemci, EV: pd.DataFrame, T: pd.DataFrame, n: int, haric_ek: Optional[set] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Ö2 (v1.2-a): Tiingo listesinden KEŞİF döneminde bitenler, tohum 56 ile rastgele n. CIK indirmeden sonra cik_bagla ile (25-NSE adı / tarihi).
    Dönüş: (seçilen, havuz, 25-NSE tablosu)."""
    N25 = efts_25nse(ist)
    havuz = o2_havuz(T, set(EV.sembol.astype(str).str.upper()) | set(haric_ek or ()))
    uygun = havuz[~havuz.sonraki_kullanim & ~havuz.haric].reset_index(drop=True)
    rng = np.random.default_rng(56); sira = rng.permutation(len(uygun)); al, atla = [], []
    for k in sira:                                                       # v1.3: aynı tohum-56 sırasının devamı; indirme öncesi kurala takılan atlanır
        r = uygun.iloc[k]; kk, nn = indirme_oncesi_suzgec(T, r.sembol, r.borsa, r.baslangic, r.bitis)
        if kk == "DIŞI":
            atla.append({**r.to_dict(), "dislama": nn}); continue
        d = devam_satiri(T, r.sembol, r.baslangic, r.bitis)
        al.append({**r.to_dict(), "isaret_on": nn if kk == "İŞARET" else "", **({"bitis": d.endDate} if d is not None else {})})
        if len(al) >= max(0, n):
            break
    sec = pd.DataFrame(al); sec["kaynak"] = "Ö2 (Tiingo KEŞİF bitişi)"; sec["cik"] = np.nan
    havuz = havuz.merge(pd.DataFrame(atla)[["sembol", "dislama"]] if atla else pd.DataFrame(columns=["sembol", "dislama"]), on="sembol", how="left")
    return sec[["cik", "sembol", "kaynak", "baslangic", "bitis", "borsa", "isaret_on"]].reset_index(drop=True), havuz, N25


AD_EK = {"INC", "INCORPORATED", "CORP", "CORPORATION", "CO", "COMPANY", "LTD", "LIMITED", "PLC", "HOLDING", "HOLDINGS", "GROUP", "LP", "LLC", "NV", "SA", "AG",
         "DE", "NEW", "THE"}
AD_GURULTU = r"(TRADING SYMBOL|STATE OF INCORPORATION|COMMISSION FILE).*$"


def ad_norm(ad: Any) -> str:
    """v1.3: büyük harf; sondaki eyalet etiketi (/FL/, /DE) ve K34 kapak gürültüsü silinir; noktalama boşluk; L P / N V / S A birleşir; ek sözcükler
    (INC, CORP, CO ...) atılır, ama ilk sözcükse kalır (Co-Diagnostics -> CO DIAGNOSTICS); THE her yerde atılır."""
    x = str(ad or "").upper().replace("&", " AND ")
    x = re.sub(AD_GURULTU, "", x); x = re.sub(r"\s*[/\\][A-Z]{2,4}[/\\]?\s*$", "", x.strip())
    x = re.sub(r"[^A-Z0-9 ]", " ", x); x = re.sub(r"\b([LNS]) ([PVA])\b", r"\1\2", x)
    t = [w for i, w in enumerate(x.split()) if w != "THE" and (w not in AD_EK or i == 0 or (i == 1 and x.split()[0] == "THE"))]
    t = [w for i, w in enumerate(t) if not (w in AD_EK and i > 0)]
    return " ".join(t).strip()


def ad_benzerlik(a: Any, b: Any) -> Tuple[float, float]:
    """(kelime Jaccard, SequenceMatcher oranı) normalize adlarda."""
    from difflib import SequenceMatcher
    x, y = ad_norm(a), ad_norm(b)
    if not x or not y:
        return 0.0, 0.0
    sx, sy = set(x.split()), set(y.split())
    return len(sx & sy) / len(sx | sy), SequenceMatcher(None, x, y).ratio()


def cik_bagla(sembol: str, ad: Optional[str], bitis: pd.Timestamp, N25: pd.DataFrame, gun: int = 45) -> Tuple[Optional[int], str]:
    """v1.2-a sabit kural: 25-NSE tarihi bitiş ±gun içinde; (1) normalize ad birebir tek CIK, (2) EFTS sembolü = Tiingo sembolü tek CIK, yoksa bağlanamadı."""
    if N25 is None or not len(N25):
        return None, "BAĞLANAMADI (25-NSE yok)"
    W = N25[(N25.nse_tarih - pd.Timestamp(bitis)).dt.days.abs() <= gun]
    if ad:
        c = W[W.ad.map(ad_norm) == ad_norm(ad)].cik.unique()
        if len(c) == 1:
            return int(c[0]), "ad + tarih"
        if len(c) > 1:
            return None, "BAĞLANAMADI (ad birden çok CIK)"
    c = W[W.sembol == sembol].cik.unique()
    if len(c) == 1:
        return int(c[0]), "sembol + tarih"
    if ad and len(W):                                                   # v1.3 ikinci kademe: tek CIK Jaccard >= 0,80 ve ikinci en iyi < 0,50
        J = W.assign(j=W.ad.map(lambda x: ad_benzerlik(ad, x)[0])).groupby("cik").j.max().sort_values(ascending=False)
        if len(J) and J.iloc[0] >= 0.80 and (len(J) == 1 or J.iloc[1] < 0.50):
            return int(J.index[0]), "benzer ad + tarih"
    return None, "BAĞLANAMADI"


def seri_denetimi(yol: str, bitis: pd.Timestamp, is_gunu: int = 10) -> Tuple[str, Optional[pd.Timestamp], int]:
    """v1.2-a: indirilen serinin son günü Tiingo bitişinden en çok is_gunu iş günü sapabilir; aksi hâlde TIINGO SERİSİ UYUŞMADI."""
    if not os.path.exists(yol):
        return "İNMEDİ", None, 0
    d = pd.read_csv(yol, usecols=["date"])
    if not len(d):
        return "BOŞ", None, 0
    son = pd.to_datetime(d.date.iloc[-1]).tz_localize(None).normalize(); fark = abs(len(pd.bdate_range(min(son, bitis), max(son, bitis))) - 1)
    return ("TAMAM" if fark <= is_gunu else "TIINGO SERİSİ UYUŞMADI"), son, int(len(d))


def sec_gecmis(ist: Istemci, ciks: List[int], hedef: str) -> Dict[str, Any]:
    """data.sec.gov submissions (+ eski dosyalar) -> sec_ozet biçimi (name, tickers, exchanges, sic, formerNames, form, date, items). Var olanı atlar."""
    out = json.load(open(hedef, encoding="utf-8")) if os.path.exists(hedef) else {}
    for n, c in enumerate(ciks, 1):
        if str(c) in out and "hata" not in out[str(c)]:                 # hatalı kayıt yeniden denenir
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
    C = cy(); G = {k: g for k, g in T.groupby("ticker")}; rows = []
    for r in aday.itertuples():
        cik = int(r.cik) if pd.notna(r.cik) else None
        s = sec.get(str(cik)) if cik is not None else None; s = s if (s and "hata" not in s) else None
        g = G.get(r.sembol)                                              # yeniden kullanılan sembol: adayın bitişine en yakın Tiingo satırı
        tg = g.loc[(g.endDate - pd.Timestamp(r.bitis)).abs().idxmin()].to_dict() if g is not None and len(g) else None
        if tg is not None:
            tg = {k: (v.strftime("%Y-%m-%d") if isinstance(v, pd.Timestamp) else v) for k, v in tg.items()}
        son = (son_gun or {}).get(r.sembol, r.bitis)
        k = C.cy_v15_sinifla(r.sembol, son, cik, s, tg, bugun.get(r.sembol))
        ad = " ".join([str((s or {}).get("name", ""))] + [str(x.get("name", "")) for x in ((s or {}).get("formerNames") or [])]).upper()
        if k["sinif"] == 2:
            k56 = "iflas"
        elif k["sinif"] == 5 and (re.search(TASFIYE_AD, ad) or (k.get("b201_tarih") and not k.get("birlesme_belge_tarih") and k.get("kayit_dis_tarih"))):
            k56 = "tasfiye"
        else:
            k56 = k["sinif"]
        rows.append({**{c: getattr(r, c) for c in aday.columns}, "k54_sinif": k["sinif"], "k54_alt": k.get("alt", ""), "k54_kural": k["kural"], "sinif_k56": SINIF_K56.get(k56, str(k56)),
                     "b103_tarih": k.get("b103_tarih", ""), "b201_tarih": k.get("b201_tarih", ""), "nse25_tarih": k.get("nse25_tarih", ""), "kayit_dis_tarih": k.get("kayit_dis_tarih", ""),
                     "sec_ad": (s or {}).get("name", ""), "sic": (s or {}).get("sic", ""), "sec_var": s is not None,
                     "cikis_islemi": k.get("cikis_islemi", ""), "kesim_tarihi": k.get("kesim_tarihi", ""), "erken_bitti": k.get("erken_bitti"), "k54_son_islem": k.get("son_islem", "")})
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


def tiingo_indir(kodlar: List[str], klasor: str, bugun: Optional[dt.date] = None, saatlik: int = TIINGO_SAATLIK, durum_yolu: Optional[str] = None,
                 meta: Optional[set] = None, fiyat: bool = True) -> pd.DataFrame:
    """Tiingo günlük fiyat (2015-01-01 ->), kod başına csv; `meta` içindeki kodlar için önce meta (ad; aynı sembol) meta/<kod>.json. 1 Kasım 2026'dan
    önce İSTEK YOK (ValueError). Var olan dosya atlanır; saatte en çok `saatlik` istek; 429 ya da kota iletisinde KotaDoldu. Anahtar başlıkta,
    loglanmaz. Durum tablosu her istekten sonra yazılır (kaldığı yerden sürer)."""
    bugun = bugun or dt.date.today()
    if bugun < TIINGO_BASLAMA:
        raise ValueError(f"Tiingo Kasım kotası {TIINGO_BASLAMA}'den önce kullanılmaz (bugün {bugun}); ONKAYIT_K56 v1.2-C")
    tok = tiingo_token()
    if not tok:
        raise RuntimeError("TIINGO_TOKEN yok (.env ya da Colab gizli anahtarı)")
    import requests
    os.makedirs(os.path.join(klasor, "meta"), exist_ok=True); s = requests.Session(); s.headers.update({"Content-Type": "application/json", "Authorization": f"Token {tok}"})
    durum = pd.read_csv(durum_yolu).to_dict("records") if (durum_yolu and os.path.exists(durum_yolu)) else []
    zaman: List[float] = sorted(pd.to_datetime([d["zaman"] for d in durum if isinstance(d.get("zaman"), str)], errors="coerce").dropna().map(lambda t: t.timestamp()).tolist())
    zaman = [t for t in zaman if time.time() - t < 3600]                 # yeniden başlatmada son saatin istekleri hız sınırına sayılır
    kalici = ("indi", "bos", "HTTP 404")                                 # 404 kalıcı (yeniden istenmez); öteki hatalar sürdürmede yeniden denenir
    bitti = {(d["sembol"], d["tur"] if isinstance(d.get("tur"), str) else "fiyat") for d in durum if d.get("durum") in kalici}

    def yaz():
        if durum_yolu:
            pd.DataFrame(durum).to_csv(durum_yolu, index=False)

    def istek(k: str, tur: str, url: str, params: Dict[str, str], yol: str, tamam, deneme: int = 3) -> None:
        while len(zaman) >= saatlik and time.time() - zaman[-saatlik] < 3600:
            time.sleep(20)
        try:
            x = None
            for d_ in range(deneme):                                         # geçici ağ hatası / 5xx: koşu içinde en çok 3 deneme, üstel bekleme
                try:
                    x = s.get(url, params=params, timeout=60); zaman.append(time.time())
                    if x.status_code < 500:
                        break
                except Exception:
                    zaman.append(time.time())
                    if d_ == deneme - 1:
                        raise
                time.sleep(5 * 2 ** d_)
            metin = x.text[:300]
            if x.status_code == 200 and tamam(x.text):
                open(yol, "w").write(x.text); dd = "indi" if (tur == "meta" or x.text.count("\n") > 1) else "bos"
            elif x.status_code == 429 or re.search(r"run over|limit|exceed", metin, re.I):
                durum.append({"sembol": k, "tur": tur, "durum": "kota", "http": x.status_code, "ileti": metin[:120], "zaman": dt.datetime.now().isoformat()}); yaz()
                raise KotaDoldu(f"Tiingo kota / hız sınırı: HTTP {x.status_code} {metin[:120]}")
            else:
                dd = f"HTTP {x.status_code}"
        except KotaDoldu:
            raise
        except Exception as ex:
            zaman.append(time.time()); dd = f"hata {type(ex).__name__}"
        durum.append({"sembol": k, "tur": tur, "durum": dd, "zaman": dt.datetime.now().isoformat()}); yaz()
        log.info("Tiingo %s %s: %s (%d istek)", tur, k, dd, len(durum))

    for k in kodlar:
        ym = os.path.join(klasor, "meta", f"{k}.json")
        if meta and k in meta and not os.path.exists(ym) and (k, "meta") not in bitti:
            istek(k, "meta", f"https://api.tiingo.com/tiingo/daily/{k}", {}, ym, lambda t: t.lstrip().startswith("{"))
        yol = os.path.join(klasor, f"{k}.csv")
        if not fiyat or os.path.exists(yol) or (k, "fiyat") in bitti:
            continue
        istek(k, "fiyat", f"https://api.tiingo.com/tiingo/daily/{k}/prices", {"startDate": "2015-01-01", "format": "csv",
              "columns": "date,open,high,low,close,volume,adjOpen,adjHigh,adjLow,adjClose,adjVolume,divCash,splitFactor"}, yol, lambda t: t.startswith("date"))
    return pd.DataFrame(durum)
