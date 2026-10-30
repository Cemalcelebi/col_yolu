"""K56 C — şirket finansalları ve sermaye yapısı: SEC XBRL companyfacts (data.sec.gov; her kavram için dönem sonu 'end' ve bildirim tarihi
'filed' -> point-in-time), SEC Financial Statement Data Sets (2009q1+; projede yalnız 2021q1-2026q3 özütü). Ölçüler: satış büyümesi, faaliyet
kârı, net kâr, faaliyet nakit akışı, serbest nakit akışı (FNA − yatırım harcaması), borç, nakit, hisse ihracı geliri, hisse sayısı (dei kapak
sayfası + ağırlıklı ortalama) -> sulandırma (G5: 12 ayda > %20). Faz 0: yalnız erişim / kapsam / point-in-time alanı.

Sınırlar: XBRL 2009-11 arası aşamalı (küçük şirketler 2011+); yabancı özel ihraççılar (20-F / 40-F) us-gaap yerine ifrs-full kullanır ya da
XBRL vermez; şirket yeniden yapılanınca CIK değişir (eski dönem eski CIK'te); 'filed' tarihi gecikmeli bilgidir (10-Q ~40-45 gün).
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from .ortak import Istemci, K56Ayar, erisim_satiri

MODUL = "finansal_mekanizma"
COMPANYFACTS = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
FS_DS = "https://www.sec.gov/files/dera/data/financial-statement-data-sets/{c}.zip"
KAVRAMLAR: Dict[str, List[str]] = {
    "hisse_sayisi_kapak": ["dei:EntityCommonStockSharesOutstanding"],
    "hisse_agirlikli": ["us-gaap:WeightedAverageNumberOfSharesOutstandingBasic"],
    "satis": ["us-gaap:Revenues", "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax", "us-gaap:SalesRevenueNet"],
    "faaliyet_kari": ["us-gaap:OperatingIncomeLoss"],
    "net_kar": ["us-gaap:NetIncomeLoss"],
    "faaliyet_nakit": ["us-gaap:NetCashProvidedByUsedInOperatingActivities"],
    "yatirim_harcamasi": ["us-gaap:PaymentsToAcquirePropertyPlantAndEquipment"],
    "hisse_ihraci": ["us-gaap:ProceedsFromIssuanceOfCommonStock"],
    "nakit": ["us-gaap:CashAndCashEquivalentsAtCarryingValue"],
    "uzun_borc": ["us-gaap:LongTermDebt", "us-gaap:LongTermDebtNoncurrent"],
}


def kavram_serisi(J: Dict[str, Any], adlar: List[str]) -> pd.DataFrame:
    """companyfacts JSON -> (end, filed, val, form, fp) satırları; ilk bulunan kavram. filed = point-in-time bilgi tarihi."""
    for ad in adlar:
        ns, k = ad.split(":"); f = J.get("facts", {}).get(ns, {}).get(k)
        if not f:
            continue
        rows = [{"kavram": ad, "birim": b, **x} for b, xs in f.get("units", {}).items() for x in xs]
        T = pd.DataFrame(rows)
        if len(T):
            for c in ("end", "filed"):
                T[c] = pd.to_datetime(T[c], errors="coerce")
            return T
    return pd.DataFrame()


def sulandirma(T: pd.DataFrame, bas: Optional[str] = None, son: Optional[str] = None) -> float:
    """Hisse sayısı (kapak) 12 ayda en büyük artış oranı (bildirim tarihine göre sıralı; isteğe bağlı bildirim penceresi). HAM: bölünme / ters
    bölünme ve birleşme artışı ayrılmaz (Faz 1'de bölünme katsayısı ve 8-K 2.01 / DEFM14A ile ayrılmalı)."""
    if not len(T):
        return np.nan
    T = T.dropna(subset=["filed"])
    if bas:
        T = T[T.filed >= pd.Timestamp(bas)]
    if son:
        T = T[T.filed <= pd.Timestamp(son)]
    s = T.sort_values("filed").drop_duplicates("filed", keep="last").set_index("filed").val.astype(float)
    if len(s) < 2:
        return np.nan
    oran = [s.iloc[j] / s[(s.index <= t - pd.Timedelta(days=330)) & (s.index >= t - pd.Timedelta(days=400))].iloc[-1] - 1
            for j, t in enumerate(s.index) if ((s.index <= t - pd.Timedelta(days=330)) & (s.index >= t - pd.Timedelta(days=400))).any()]
    return float(np.nanmax(oran)) if oran else np.nan


def erisim_testi(A: K56Ayar, ist: Istemci, Ornek: pd.DataFrame) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []; ozet = []
    for r in Ornek.itertuples():
        u = COMPANYFACTS.format(cik=int(r.cik))
        try:
            d, veri, _ = ist.al(u, ad=f"companyfacts_{int(r.cik)}.json", sinir=40_000_000)
            if d != 200:
                ozet.append({"sembol": r.sembol, "grup": r.grup, "durum": f"HTTP {d}"}); continue
            J = json.loads(veri.decode()); sat = {"sembol": r.sembol, "grup": r.grup, "durum": "ok", "mb": round(len(veri) / 2 ** 20, 2), "ifrs": "ifrs-full" in J.get("facts", {})}
            for ad, kav in KAVRAMLAR.items():
                T = kavram_serisi(J, kav)
                kesif = T[(T.end >= "2016-01-01") & (T.end <= "2021-12-31")] if len(T) else T
                sat[ad] = int(kesif.end.nunique()) if len(T) else 0
                if ad == "hisse_sayisi_kapak":
                    sat["ilk_filed"] = str(T.filed.min().date()) if len(T) else ""; sat["sulandirma_12ay_max_kesif_ham"] = round(sulandirma(T, "2016-01-01", "2021-12-31"), 3) if len(T) else np.nan
                    sat["filed_gecikme_medyan_gun"] = float((T.filed - T.end).dt.days.median()) if len(T) else np.nan
            sat["bolunme_orani_kavrami"] = bool(len(kavram_serisi(J, ["us-gaap:StockholdersEquityNoteStockSplitConversionRatio1"])))
            ozet.append(sat)
        except Exception as ex:
            ozet.append({"sembol": r.sembol, "grup": r.grup, "durum": f"{type(ex).__name__}: {str(ex)[:120]}"})
    Z = pd.DataFrame(ozet); ok = Z[Z.durum == "ok"] if len(Z) else Z
    out.append(erisim_satiri(MODUL, "SEC_COMPANYFACTS", "örneklem indirme", "GECTI" if len(ok) == len(Ornek) else ("KISMI" if len(ok) else "BASARISIZ"), "başarılı", f"{len(ok)}/{len(Ornek)}",
                             "; ".join(f"{x.sembol}:{x.durum}" for x in Z.itertuples() if x.durum != "ok") or "hepsi indi", COMPANYFACTS))
    if len(ok):
        kols = list(KAVRAMLAR)
        dolu = {k: int((ok[k] >= 8).sum()) for k in kols}                  # KEŞİF'te >= 8 farklı dönem sonu
        out.append(erisim_satiri(MODUL, "SEC_COMPANYFACTS", "kavram kapsamı KEŞİF 2016-21 (>= 8 dönem)", "GECTI" if min(dolu.values()) >= len(ok) // 2 else "KISMI", "kavram -> şirket sayısı",
                                 json.dumps(dolu, ensure_ascii=False), "; ".join(f"{x.sembol}({x.grup}) ilk_filed {x.ilk_filed} ifrs {x.ifrs}" for x in ok.itertuples())))
        out.append(erisim_satiri(MODUL, "SEC_COMPANYFACTS", "point-in-time: filed − end (kapak hisse sayısı)", "GECTI", "medyan gün", float(ok.filed_gecikme_medyan_gun.median()),
                                 "her değer bildirim tarihinden sonra kullanılabilir (bilgi gecikmesi)"))
        s = ok[["sembol", "grup", "sulandirma_12ay_max_kesif_ham", "bolunme_orani_kavrami"]].dropna(subset=["sulandirma_12ay_max_kesif_ham"])
        out.append(erisim_satiri(MODUL, "SEC_COMPANYFACTS", "sulandırma ölçüsü HAM (KEŞİF bildirimleri; G5 adayı > %20)", "KISMI", "G5 adayı (ham)", int((s.sulandirma_12ay_max_kesif_ham > 0.20).sum()),
                                 "; ".join(f"{x.sembol}({x.grup}) {x.sulandirma_12ay_max_kesif_ham:+.2f}" for x in s.itertuples())
                                 + f"; bölünme oranı kavramı olan şirket {int(s.bolunme_orani_kavrami.sum())}/{len(s)}; HAM: bölünme / birleşme ayrılmadı (TRMB 2013 bölünmesi, EXR 2023 birleşmesi pencere dışı)"))
        out[-1]["tablo"] = Z.to_dict("records")
    # Financial Statement Data Sets: projede 2021q1+; KEŞİF çeyrekleri boyu (eksik 2016-20)
    try:
        yerel = sorted(f for f in os.listdir(os.path.join(A.iv, "secfs")) if f.startswith("fs_")) if os.path.isdir(os.path.join(A.iv, "secfs")) else []
        boy = 0; hata = 0
        for y in range(2016, 2021):
            for q in range(1, 5):
                dd, bh = ist.bas(FS_DS.format(c=f"{y}q{q}")); boy += int(bh.get("Content-Length", "0") or 0); hata += int(dd != 200)
        out.append(erisim_satiri(MODUL, "SEC_FS_DS", "projede 2021q1+; eksik 2016-20 boyu", "GECTI" if not hata else "KISMI", "eksik 20 çeyrek MB", round(boy / 2 ** 20, 1),
                                 f"yerel özüt {yerel[0] if yerel else '-'} .. {yerel[-1] if yerel else '-'} ({len(yerel)} dosya); HEAD hatası {hata}", FS_DS.format(c="2016q1")))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "SEC_FS_DS", "boy", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}"))
    return out
