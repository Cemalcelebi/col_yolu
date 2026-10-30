"""K56 A — kurumsal sahiplik: SEC Form 13F veri setleri (yönetici çeyrek sonu uzun pozisyonları), CUSIP -> sembol eşlemesi (OpenFIGI), Form N-PORT
(fon portföyleri), Schedule 13D / 13G (%5 üstü sahiplik olayları; kurumsal_olaylar SEC başvuru özetinden). Faz 0: yalnız erişim / kapsam / boyut.

Bilinen sınırlar (K31 / Ç103'te 13F CUSIP eşlemesinde tıkandı): 13F yalnız 100 milyon $ üstü yöneticiler, yalnız uzun pozisyon, çeyrek sonu
anlık görüntü, bildirim 45 güne kadar gecikmeli (point-in-time için bildirim tarihi kullanılmalı), açığa satış ve gün içi akış yok.
"""
from __future__ import annotations

import io
import re
from typing import Any, Dict, List

import pandas as pd

from .ortak import Istemci, K56Ayar, erisim_satiri, log, zip_icerik_listesi, zip_uye_bas

MODUL = "kurumsal_sahiplik"
SEC_13F_SAYFA = "https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets"
SEC_NPORT_SAYFA = "https://www.sec.gov/data-research/sec-markets-data/form-n-port-data-sets"
OPENFIGI = "https://api.openfigi.com/v3/mapping"


def _zipler(ist: Istemci, sayfa: str) -> List[str]:
    d, h, _ = ist.al(sayfa, sinir=2_000_000)
    if d != 200:
        return []
    return sorted(set("https://www.sec.gov" + u for u in re.findall(r'href="(/files/[^"]+\.zip)"', h.decode("utf-8", "replace"))))


def _ceyrek(u: str) -> str:
    m = re.search(r"/(\d{4}q\d)_", u)
    if m:
        return m.group(1)
    m = re.search(r"/(\d{2}[a-z]{3}\d{4})-(\d{2}[a-z]{3}\d{4})_", u)
    return f"{m.group(1)}..{m.group(2)}" if m else u.rsplit("/", 1)[-1]


def openfigi_esle(ist: Istemci, cusipler: List[str]) -> pd.DataFrame:
    """CUSIP -> (securityType Common Stock / REIT / ADR / MLP ve exchCode 'US' olan) güncel ABD sembolü. Anahtarsız: istek başına en çok 10 kimlik, 25 istek / dk."""
    import json
    rows = []
    for i in range(0, len(cusipler), 10):
        parca = cusipler[i:i + 10]
        d, j, _ = ist.al(OPENFIGI, yontem="POST", govde=json.dumps([{"idType": "ID_CUSIP", "idValue": c} for c in parca]).encode(),
                         ek_baslik={"Content-Type": "application/json"}, sinir=2_000_000)
        J = json.loads(j.decode()) if d == 200 else [{}] * len(parca)
        for c, x in zip(parca, J):
            us = [y for y in (x.get("data") or []) if y.get("exchCode") == "US" and str(y.get("securityType", "")) in ("Common Stock", "REIT", "ADR", "MLP")] if isinstance(x, dict) else []
            rows.append({"cusip": c, "ticker_us": us[0].get("ticker") if us else None, "listeleme": len(x.get("data") or []) if isinstance(x, dict) else 0, "http": d})
    return pd.DataFrame(rows)


def _yil_sirasi(c: str) -> str:
    m = re.match(r"(\d{4})q(\d)", c)
    if m:
        return f"{m.group(1)}{m.group(2)}"
    m = re.match(r"\d{2}([a-z]{3})(\d{4})", c)
    ay = {"jan": 1, "feb": 1, "mar": 1, "apr": 2, "may": 2, "jun": 2, "jul": 3, "aug": 3, "sep": 3, "oct": 4, "nov": 4, "dec": 4}
    return f"{m.group(2)}{ay.get(m.group(1), 9)}" if m else c


def erisim_testi(A: K56Ayar, ist: Istemci, Ornek: pd.DataFrame) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    # 0) örneklem sembollerinin CUSIP'i (SEC başarısız teslim dosyası 2016-01: SYMBOL + CUSIP) -> OpenFIGI geri eşleme (sembol tutuyor mu)
    try:
        import io as _io
        import zipfile as _zf
        d, h, _ = ist.al("https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data", sinir=3_000_000)
        u = next(("https://www.sec.gov" + x for x in re.findall(r'href="(/files/[^"]+cnsfails201601a\.zip)"', h.decode("utf-8", "replace"))), None)
        if u:
            dd, veri, _ = ist.al(u, ad="ftd_201601a.zip", sinir=20_000_000); z = _zf.ZipFile(_io.BytesIO(veri))
            F = pd.read_csv(z.open(z.namelist()[0]), sep="|", dtype=str, encoding="latin-1", on_bad_lines="skip")
            m = F[F.SYMBOL.isin(set(Ornek.sembol))].drop_duplicates("SYMBOL")
            if len(m):
                R = openfigi_esle(ist, list(m.CUSIP.str.upper())); R["sembol"] = list(m.SYMBOL); dogru = R[R.ticker_us == R.sembol]
                out.append(erisim_satiri(MODUL, "OPENFIGI", "örneklem CUSIP'i (FTD 2016-01) -> sembol geri eşleme", "GECTI" if len(dogru) >= 0.6 * len(R) else "KISMI", "doğru / bulunan",
                                         f"{len(dogru)}/{len(R)}", "; ".join(f"{r.sembol}:{r.cusip}->{r.ticker_us}" for r in R.itertuples())[:400]
                                         + "; bulunamayanlar: yeniden yapılanma / satın almayla kapanmış eski CUSIP (APO 2016, AERI) — OpenFIGI tarihli eşleme vermez", OPENFIGI))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "OPENFIGI", "örneklem CUSIP geri eşleme", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}"))
    # 1) 13F veri seti listesi ve KEŞİF çeyrek boyları
    try:
        z = _zipler(ist, SEC_13F_SAYFA); cey = [_ceyrek(u) for u in z]
        out.append(erisim_satiri(MODUL, "SEC_13F_DS", "liste", "GECTI" if z else "BASARISIZ", "zip sayısı", len(z), f"en eski {min(cey, key=_yil_sirasi) if cey else '-'}; en yeni {max(cey, key=_yil_sirasi) if cey else '-'}", SEC_13F_SAYFA))
        kesif = [u for u in z if re.search(r"/(2016|2017|2018|2019|2020|2021)q\d_", u)]; boy = 0; eksik = 0
        for u in kesif:
            dd, bh = ist.bas(u); b = int(bh.get("Content-Length", "0") or 0); boy += b; eksik += int(dd != 200)
        out.append(erisim_satiri(MODUL, "SEC_13F_DS", "KEŞİF 2016-21 boy", "GECTI" if kesif and not eksik else "KISMI", "toplam MB", round(boy / 2 ** 20, 1),
                                 f"{len(kesif)} çeyrek, HEAD hatası {eksik}; çeyrek ort. {round(boy / max(1, len(kesif)) / 2 ** 20, 1)} MB", SEC_13F_SAYFA))
        # 2) bir çeyreğin içeriği (Range ile merkez dizin) ve INFOTABLE'ın ilk satırları (kısmi açma) -> CUSIP örneği
        u = next((x for x in kesif if "2016q1" in x), kesif[0] if kesif else None)
        if u:
            L = zip_icerik_listesi(ist, u, "13f_2016q1")
            if "dosya" in L:
                out.append(erisim_satiri(MODUL, "SEC_13F_DS", "zip içeriği (Range)", "GECTI", "dosya", len(L), "; ".join(f"{r.dosya} {round(r.acik / 2 ** 20, 1)} MB" for r in L.itertuples()), u))
                bas = zip_uye_bas(ist, u, L, "INFOTABLE.tsv", 400_000, "13f_2016q1_info"); T = pd.read_csv(io.BytesIO(bas[: bas.rfind(b"\n")]), sep="\t", dtype=str)
                out.append(erisim_satiri(MODUL, "SEC_13F_DS", "INFOTABLE kısmi okuma", "GECTI" if "CUSIP" in T else "BASARISIZ", "satır", len(T), f"sütunlar: {', '.join(T.columns[:14])}", u))
                com = T[T.TITLEOFCLASS.fillna("").str.upper().str.contains(r"\bCOM") & T.CUSIP.fillna("").str.len().eq(9)] if "TITLEOFCLASS" in T else T.iloc[0:0]
                cus = list(com.CUSIP.str.upper().unique()[:10])
                if cus:
                    R = openfigi_esle(ist, cus); ok = R[R.ticker_us.notna()]
                    out.append(erisim_satiri(MODUL, "OPENFIGI", "13F adi hisse CUSIP'i -> ABD sembolü (10 kimlik, anahtarsız)", "GECTI" if len(ok) >= 6 else ("KISMI" if len(ok) else "BASARISIZ"),
                                             "adi hisse / REIT + exchCode US eşleşen / 10", len(ok), "; ".join(f"{r.cusip}->{r.ticker_us}" for r in ok.itertuples())[:400]
                                             + "; NOT: OpenFIGI GÜNCEL sembolü döndürür (tarihli değil); tarihli ad için SEC 13(f) listesi", OPENFIGI))
            else:
                out.append(erisim_satiri(MODUL, "SEC_13F_DS", "zip içeriği (Range)", "BASARISIZ", ayrinti=str(L.to_dict()), url=u))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "SEC_13F_DS", "erişim", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}", url=SEC_13F_SAYFA))
    # 3) N-PORT veri setleri (2019q4+): liste ve bir çeyrek boyu
    try:
        z = _zipler(ist, SEC_NPORT_SAYFA); cey = [_ceyrek(u) for u in z]
        b = 0
        if z:
            dd, bh = ist.bas(z[-1]); b = int(bh.get("Content-Length", "0") or 0)
        out.append(erisim_satiri(MODUL, "SEC_NPORT_DS", "liste + boy", "GECTI" if z else "BASARISIZ", "zip sayısı", len(z), f"en eski {min(cey, key=_yil_sirasi) if cey else '-'}; bir çeyrek {round(b / 2 ** 20)} MB "
                                 "(KEŞİF'in yalnız 2019q4-2021q4'ünü kapsar)", SEC_NPORT_SAYFA))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "SEC_NPORT_DS", "erişim", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}", url=SEC_NPORT_SAYFA))
    return out
