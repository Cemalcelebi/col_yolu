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


def _yil_sirasi(c: str) -> str:
    m = re.match(r"(\d{4})q(\d)", c)
    if m:
        return f"{m.group(1)}{m.group(2)}"
    m = re.match(r"\d{2}([a-z]{3})(\d{4})", c)
    ay = {"jan": 1, "feb": 1, "mar": 1, "apr": 2, "may": 2, "jun": 2, "jul": 3, "aug": 3, "sep": 3, "oct": 4, "nov": 4, "dec": 4}
    return f"{m.group(2)}{ay.get(m.group(1), 9)}" if m else c


def erisim_testi(A: K56Ayar, ist: Istemci, Ornek: pd.DataFrame) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
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
                cus = [c for c in T.CUSIP.dropna().str.upper().unique() if len(c) == 9][:10] if "CUSIP" in T else []
                if cus:
                    d, j, _ = ist.al(OPENFIGI, yontem="POST", govde=pd.Series([{"idType": "ID_CUSIP", "idValue": c} for c in cus]).to_json(orient="values").encode(),
                                     ek_baslik={"Content-Type": "application/json"}, sinir=500_000)
                    import json
                    J = json.loads(j.decode()) if d == 200 else []; ok = [x for x in J if isinstance(x, dict) and x.get("data")]
                    ornek = "; ".join(f"{c}->{x['data'][0].get('ticker')}" for c, x in zip(cus, J) if isinstance(x, dict) and x.get("data"))[:400]
                    out.append(erisim_satiri(MODUL, "OPENFIGI", "CUSIP -> sembol (anahtarsız, 10 kimlik)", "GECTI" if len(ok) >= 7 else ("KISMI" if ok else "BASARISIZ"), "eşleşen / 10",
                                             len(ok), f"HTTP {d}; {ornek}; NOT: CUSIP fon / tahvil de olabilir, eşlemede securityType = Common Stock ve exchCode = US süzgeci gerekir", OPENFIGI))
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
