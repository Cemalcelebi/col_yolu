"""K56 E — işlem davranışı: SEC MIDAS 'Metrics by Individual Security and Exchange' (çeyreklik; gün × hisse; işlem büyüklüğü, tek lot altı, gizli
emir, iptal / işlem; 2012q1+; borsa kırılımsız dosya çeyrek ~15-22 MB), FINRA Reg SHO günlük açığa satış hacmi (konsolide CNMS 2018-08+, tesis
dosyaları FNYX / FNSQ 2009-08+), FINRA konsolide açığa satış
pozisyonu (API; ayda iki kez; erişilebilir en eski ~2017-12), FINRA OTC / ATS haftalık hacim (karanlık havuz; API), SEC başarısız teslim (FTD;
yarım aylık, 2004+), günlük OHLC'den spread tahmini (Corwin-Schultz 2012, Abdi-Ranaldo 2017; VEKİL). Gün içi işlem / emir defteri verisi
(TAQ, ITCH) ücretli ve projede YOK: dağıtım ile emilimi işlem sırası düzeyinde ayırmak bu veriyle mümkün değil (yalnız toplam / çeyreklik izler).
"""
from __future__ import annotations

import io
import json
import os
import pickle
import re
import zipfile
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from .ortak import Istemci, K56Ayar, erisim_satiri, zip_icerik_listesi

MODUL = "islem_davranisi"
MIDAS_SAYFA = "https://www.sec.gov/data-research/sec-markets-data/market-structure-data-security-exchange"
MIDAS_HISSE = "https://www.sec.gov/files/opa/data/market-structure/metrics-individual-security/individual_security_{y}_q{q}.zip"     # borsa kırılımsız, çeyrek ~15-22 MB
REGSHO_TESIS = "https://cdn.finra.org/equity/regsho/daily/{t}shvol{g}.txt"     # FNSQ / FNYX tesis dosyaları 2009-08'den (CNMS 2018-08'den)
REGSHO = "https://cdn.finra.org/equity/regsho/daily/CNMSshvol{g}.txt"
FINRA_SI = "https://api.finra.org/data/group/otcMarket/name/consolidatedShortInterest"
FINRA_ATS = "https://api.finra.org/data/group/otcMarket/name/weeklySummary"
FTD_SAYFA = "https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data"


def corwin_schultz(d: pd.DataFrame) -> pd.Series:
    """Corwin-Schultz (2012) yüksek-düşük spread tahmini (iki günlük; negatifler 0). VEKİL: gerçek kote spread'i değil."""
    H = np.log(d.High.astype(float)); L = np.log(d.Low.astype(float)); b = (H - L) ** 2 + (H.shift(1) - L.shift(1)) ** 2
    g = (np.maximum(H, H.shift(1)) - np.minimum(L, L.shift(1))) ** 2; k = 3 - 2 * np.sqrt(2)
    a = (np.sqrt(2 * b) - np.sqrt(b)) / k - np.sqrt(g / k); s = 2 * (np.exp(a) - 1) / (1 + np.exp(a))
    return s.clip(lower=0)


def abdi_ranaldo(d: pd.DataFrame) -> pd.Series:
    """Abdi-Ranaldo (2017) kapanış-orta nokta spread tahmini (iki günlük). VEKİL."""
    c = np.log(d.Close.astype(float)); eta = (np.log(d.High.astype(float)) + np.log(d.Low.astype(float))) / 2
    v = 4 * (c.shift(1) - eta.shift(1)) * (c.shift(1) - eta)          # t−1 ve t çifti: yalnız t'ye kadar bilinen veri (geleceğe bakmaz)
    return np.sqrt(v.clip(lower=0))


def _midas_ceyrek(ist: Istemci, y: int, q: int) -> pd.DataFrame:
    u = MIDAS_HISSE.format(y=y, q=q); d, veri, _ = ist.al(u, ad=f"midas_hisse_{y}q{q}.zip")
    if d != 200:
        return pd.DataFrame()
    zf = zipfile.ZipFile(io.BytesIO(veri))
    return pd.concat([pd.read_csv(zf.open(n), dtype=str, usecols=lambda c: c in ("Date", "Ticker", "Security")) for n in zf.namelist() if n.lower().endswith(".csv")], ignore_index=True)


def erisim_testi(A: K56Ayar, ist: Istemci, Ornek: pd.DataFrame, EV: Optional[pd.DataFrame] = None) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []; semb = list(Ornek.sembol)
    # 1) MIDAS hisse bazlı ölçüler
    try:
        d, h, _ = ist.al(MIDAS_SAYFA, sinir=2_000_000); z = sorted(set("https://www.sec.gov" + u for u in re.findall(r'href="(/files/[^"]+individual_security_exchange_[^"]+\.zip)"', h.decode("utf-8", "replace"))))
        cey = sorted(re.search(r"_(\d{4})_q(\d)", u).group(1) + "q" + re.search(r"_(\d{4})_q(\d)", u).group(2) for u in z if re.search(r"_(\d{4})_q(\d)", u))
        out.append(erisim_satiri(MODUL, "SEC_MIDAS", "liste", "GECTI" if z else "BASARISIZ", "zip sayısı", len(z), f"çeyrek {cey[0] if cey else '-'} .. {cey[-1] if cey else '-'}", MIDAS_SAYFA))
        T = _midas_ceyrek(ist, 2016, 1)
        if len(T) and EV is not None:
            akt = EV[(pd.to_datetime(EV.ilk_islem) <= "2016-01-04") & (pd.to_datetime(EV.son_islem) >= "2016-03-31")]
            bul = akt.sembol.isin(set(T.Ticker.str.upper())); sek = akt.assign(b=bul).groupby("sektor").b.mean().sort_values().head(4).round(2).to_dict()
            out.append(erisim_satiri(MODUL, "SEC_MIDAS", "hisse dosyası 2016q1: K55 evreni kapsamı", "KISMI", "2016q1'de işlemde olan K55 hissesi payı", round(float(bul.mean()), 3),
                                     f"{len(akt)} hisse; en düşük sektör kapsamı {sek}; MIDAS evreni CRSP adi hisse (SHRCD 10/11) + ETP: REIT, yabancı, BDC / MLP yok", MIDAS_HISSE.format(y=2016, q=1)))
        rows = []; bulunan = 0; uygun = 0
        for r in Ornek[Ornek.grup.isin(["G1", "G2"])].itertuples():
            t = pd.Timestamp(r.tarih); Tq = _midas_ceyrek(ist, t.year, (t.month - 1) // 3 + 1)
            var = bool(len(Tq) and (Tq.Ticker.str.upper() == r.sembol).any()); bulunan += int(var); uygun += 1
            rows.append(f"{r.sembol}({r.grup}) {t.year}q{(t.month - 1) // 3 + 1}: {'var' if var else 'yok'}")
        out.append(erisim_satiri(MODUL, "SEC_MIDAS", "örneklem G1 / G2: olay çeyreğinde", "GECTI" if uygun and bulunan >= 0.6 * uygun else "KISMI", "bulunan / uygun", f"{bulunan}/{uygun}",
                                 "; ".join(rows) + "; G3 / G6 (batan, birleşen) olay çeyrekleri 2022-23 (İÇ dönem) olduğu için indirilmedi", MIDAS_HISSE.format(y=2017, q=1)))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "SEC_MIDAS", "erişim", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}", url=MIDAS_SAYFA))
    # 2) FINRA Reg SHO günlük açığa satış hacmi: konsolide (CNMS, 2018-08+) ve tesis dosyaları (FNYX / FNSQ, 2009-08+)
    try:
        durum = {}; bul = []
        for t, g in (("CNMS", "20160104"), ("CNMS", "20180801"), ("FNYX", "20160104"), ("FNSQ", "20160104")):
            dd, veri, _ = ist.al(REGSHO_TESIS.format(t=t, g=g), ad=f"regsho_{t}_{g}.txt", sinir=2_000_000); durum[f"{t} {g}"] = dd
            if dd == 200 and t != "CNMS":
                T = pd.read_csv(io.StringIO(veri.decode()), sep="|"); bul = sorted(set(bul) | (set(T.Symbol.astype(str)) & set(semb)))
        ok = sum(1 for v in durum.values() if v == 200)
        out.append(erisim_satiri(MODUL, "FINRA_REGSHO", "günlük açığa satış hacmi (konsolide + tesis)", "GECTI" if durum.get("FNYX 20160104") == 200 else "KISMI", "HTTP", json.dumps(durum),
                                 f"KEŞİF tesis dosyalarıyla (FNYX + FNSQ [+ FORF], 2009-08+) kapsanır, konsolide CNMS 2018-08'den; 2016-01-04 tesis dosyalarında örneklemden {len(bul)} sembol; "
                                 "yalnız borsa dışı (TRF / ADF / ORF) hacim, pozisyon değil; FINRA koşulu: kişisel / ticari olmayan kullanım, ham veri dağıtılmaz", REGSHO_TESIS.format(t="FNYX", g="20160104")))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "FINRA_REGSHO", "erişim", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}"))
    # 3) FINRA açığa satış pozisyonu API: geçmiş derinliği
    try:
        sonuc = {}
        for a in ("2017-06", "2018-01", "2019-06", "2021-06"):
            gov = json.dumps({"limit": 50, "fields": ["symbolCode", "settlementDate", "currentShortPositionQuantity", "daysToCoverQuantity"],
                              "dateRangeFilters": [{"fieldName": "settlementDate", "startDate": f"{a}-01", "endDate": f"{a}-28"}],
                              "domainFilters": [{"fieldName": "symbolCode", "values": semb}]}).encode()
            dd, veri, _ = ist.al(FINRA_SI, yontem="POST", govde=gov, ek_baslik={"Content-Type": "application/json", "Accept": "application/json"}, sinir=2_000_000)
            J = json.loads(veri.decode()) if (dd == 200 and veri.strip()) else []; sonuc[a] = len({x["symbolCode"] for x in J})
        out.append(erisim_satiri(MODUL, "FINRA_SI", "API geçmiş derinliği (örneklem sembolleri)", "KISMI", "dönem -> sembol", json.dumps(sonuc),
                                 "2017 boş: API ~2017-12'den başlıyor -> KEŞİF'in 2016-01..2017-11'i eksik; öncesi için borsa (NYSE / Nasdaq) ücretli dosyaları", FINRA_SI))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "FINRA_SI", "erişim", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}"))
    # 4) FINRA ATS / OTC haftalık hacim (karanlık havuz): genel API'nin geçmiş derinliği
    try:
        sonuc = {}
        for a in ("2016-06", "2019-06", "2021-06", "2023-06"):
            gov = json.dumps({"limit": 50, "fields": ["issueSymbolIdentifier", "weekStartDate", "totalWeeklyShareQuantity", "summaryTypeCode"],
                              "domainFilters": [{"fieldName": "issueSymbolIdentifier", "values": semb[:4]}],
                              "dateRangeFilters": [{"fieldName": "weekStartDate", "startDate": f"{a}-01", "endDate": f"{a}-28"}]}).encode()
            dd, veri, _ = ist.al(FINRA_ATS, yontem="POST", govde=gov, ek_baslik={"Content-Type": "application/json", "Accept": "application/json"}, sinir=2_000_000)
            J = json.loads(veri.decode()) if (dd == 200 and veri.strip()) else []; sonuc[a] = len(J)
        out.append(erisim_satiri(MODUL, "FINRA_ATS", "haftalık ATS / OTC hacmi (genel API, 4 sembol)", "KISMI", "dönem -> kayıt", json.dumps(sonuc),
                                 "genel API yalnız yakın geçmişi veriyor (KEŞİF boş); 2014 / 2016 sonrası tarihsel dosyalar otctransparency.finra.org'dan elle / kullanım koşuluyla",
                                 FINRA_ATS))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "FINRA_ATS", "erişim", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}"))
    # 5) SEC başarısız teslim (FTD)
    try:
        d, h, _ = ist.al(FTD_SAYFA, sinir=3_000_000); z = sorted(set("https://www.sec.gov" + u for u in re.findall(r'href="(/files/[^"]+\.zip)"', h.decode("utf-8", "replace"))))
        rows = []; bulunan = 0
        for r in Ornek.itertuples():
            t = pd.Timestamp(r.tarih); kod = f"cnsfails{t.year}{t.month:02d}{'a' if t.day <= 15 else 'b'}"
            u = next((x for x in z if f"/{kod}.zip" in x), None)
            if u is None:
                rows.append(f"{r.sembol}: {kod} yok"); continue
            dd, veri, _ = ist.al(u, ad=f"ftd_{kod}.zip", sinir=20_000_000); zf = zipfile.ZipFile(io.BytesIO(veri))
            T = pd.read_csv(zf.open(zf.namelist()[0]), sep="|", dtype=str, encoding="latin-1", on_bad_lines="skip")
            var = bool((T.get("SYMBOL", pd.Series(dtype=str)) == r.sembol).any()); bulunan += int(var); rows.append(f"{r.sembol}({r.grup}) {kod}: {'var' if var else 'yok'}")
        out.append(erisim_satiri(MODUL, "SEC_FTD", "örneklem: olay yarım ayında başarısız teslim kaydı", "GECTI", "kaydı olan / örneklem", f"{bulunan}/{len(Ornek)}",
                                 f"{len(z)} dosya listede; " + "; ".join(rows) + "; yalnız eşik üstü bakiye yayımlanır: kayıt yokluğu veri eksikliği değildir", FTD_SAYFA))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "SEC_FTD", "erişim", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}", url=FTD_SAYFA))
    # 6) OHLC spread tahmini (yerel V_ABD; vekil)
    try:
        yv = os.path.join(A.veri, "V_ABD.pkl"); V = pickle.load(open(yv, "rb")) if os.path.exists(yv) else {}
        rows = []
        for s in semb:
            d = V.get(s)
            if d is None:
                continue
            k = d[(d.index >= "2016-01-01") & (d.index <= "2021-12-31")]
            cs = corwin_schultz(k).rolling(20, min_periods=10).mean(); ar = abdi_ranaldo(k).rolling(20, min_periods=10).mean()
            rows.append(f"{s}: CS medyan {cs.median() * 1e4:.0f} bp, AR medyan {ar.median() * 1e4:.0f} bp, dolu {cs.notna().mean():.2f}")
        out.append(erisim_satiri(MODUL, "OHLC_SPREAD_VEKIL", "Corwin-Schultz / Abdi-Ranaldo (yerel)", "GECTI" if rows else "ATLANDI", "sembol", len(rows),
                                 "; ".join(rows) or "V_ABD yok (CY_VERI)"))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "OHLC_SPREAD_VEKIL", "hesap", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}"))
    out.append(erisim_satiri(MODUL, "TAQ_ITCH_UCRETLI", "gün içi işlem / emir defteri", "ATLANDI", "istek", 0, "ücretli (NYSE TAQ / WRDS, Nasdaq ITCH, Polygon, Databento); Faz 0'da istek yok, fiyatı rapor"))
    return out
