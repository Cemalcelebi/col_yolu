"""K56 B — içeriden işlemler: SEC 'Insider Transactions Data Sets' (Form 3 / 4 / 5 yapılandırılmış, 2006q1+), işlem kodları (P açık piyasa
alımı, S satış, A ödül, M opsiyon kullanımı, F vergi için tutulan, G hediye, D şirkete satış, C dönüşüm, X opsiyon kullanımı), 10b5-1
otomatik plan bilgisi (Nisan 2023 sonrası işaret; öncesi yalnız dipnot metni), bildirim gecikmesi. Projede K30'da yalnız açık piyasa alımları
özeti var (k30_alim); satış / opsiyon / vergi işlemleri ve 10b5-1 ayrımı yok. Faz 0: yalnız erişim / kapsam / eşleşme.

Sınırlar: yabancı özel ihraççılar (20-F / 40-F) Form 4 vermez; bildirim 2 iş günü içinde (2002 sonrası) ama geç bildirim olur; F / A / M
kodları bilgi taşımaz (zorunlu / ücret), yalnız P ve plansız S davranış sayılır.
"""
from __future__ import annotations

import io
import os
import re
import zipfile
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from .ortak import Istemci, K56Ayar, erisim_satiri, zip_icerik_listesi, zip_uye_bas

MODUL = "iceriden_islemler"
SEC_IC_SAYFA = "https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets"
KOD_ANLAM = {"P": "açık piyasa alımı", "S": "açık piyasa / özel satış", "A": "ödül / hibe", "M": "türev kullanımı", "F": "vergi / bedel için tutulan", "G": "hediye",
             "D": "şirkete satış", "C": "dönüşüm", "X": "opsiyon kullanımı (para içi)", "J": "diğer"}


def _zipler(ist: Istemci) -> List[str]:
    d, h, _ = ist.al(SEC_IC_SAYFA, sinir=2_000_000)
    return sorted(set("https://www.sec.gov" + u for u in re.findall(r'href="(/files/[^"]+_form345\.zip)"', h.decode("utf-8", "replace")))) if d == 200 else []


def erisim_testi(A: K56Ayar, ist: Istemci, Ornek: pd.DataFrame, EV: pd.DataFrame) -> List[Dict[str, Any]]:
    """EV: K55 evreni (cik, ilk_islem, son_islem); eşleşme payı 2016q1'de işlemde olanlar içinde ölçülür."""
    out: List[Dict[str, Any]] = []
    try:
        z = _zipler(ist); cey = sorted(re.search(r"/(\d{4}q\d)_", u).group(1) for u in z if re.search(r"/(\d{4}q\d)_", u))
        out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "liste", "GECTI" if z else "BASARISIZ", "zip sayısı", len(z), f"çeyrek {cey[0] if cey else '-'} .. {cey[-1] if cey else '-'}", SEC_IC_SAYFA))
        kesif = [u for u in z if re.search(r"/(2016|2017|2018|2019|2020|2021)q\d_", u)]; boy = 0
        for u in kesif:
            _, bh = ist.bas(u); boy += int(bh.get("Content-Length", "0") or 0)
        out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "KEŞİF 2016-21 boy", "GECTI" if kesif else "BASARISIZ", "toplam MB", round(boy / 2 ** 20, 1), f"{len(kesif)} çeyrek", SEC_IC_SAYFA))
        u = next((x for x in kesif if "2016q1" in x), None)
        if u:
            d, veri, _ = ist.al(u, ad="insider_2016q1.zip")
            if d != 200:
                raise RuntimeError(f"2016q1 indirilemedi: HTTP {d}")
            zf = zipfile.ZipFile(io.BytesIO(veri)); ad = {n.rsplit("/", 1)[-1]: n for n in zf.namelist()}
            Su = pd.read_csv(zf.open(ad["SUBMISSION.tsv"]), sep="\t", dtype=str, on_bad_lines="skip"); Nd = pd.read_csv(zf.open(ad["NONDERIV_TRANS.tsv"]), sep="\t", dtype=str, on_bad_lines="skip")
            Fo = pd.read_csv(zf.open(ad["FOOTNOTES.tsv"]), sep="\t", dtype=str, on_bad_lines="skip") if "FOOTNOTES.tsv" in ad else pd.DataFrame(columns=["ACCESSION_NUMBER", "FOOTNOTE_TXT"])
            out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "2016q1 indirme + ayrıştırma", "GECTI", "başvuru / işlem", f"{len(Su)} / {len(Nd)}",
                                     f"{round(len(veri) / 2 ** 20, 1)} MB; tablolar {sorted(ad)}; SUBMISSION sütunları {list(Su.columns)[:12]}", u))
            Su["cik"] = pd.to_numeric(Su.ISSUERCIK, errors="coerce")
            akt = EV[EV.cik.notna() & (pd.to_datetime(EV.ilk_islem) <= "2016-01-04") & (pd.to_datetime(EV.son_islem) >= "2016-03-31")]
            ev = set(int(c) for c in akt.cik)
            kaps = len(ev & set(Su.cik.dropna().astype(int))) / max(1, len(ev))
            out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "evren eşleşmesi (CIK, 2016q1)", "GECTI" if kaps >= 0.6 else "KISMI", "K55 evreni CIK payı", round(kaps, 3),
                                     f"2016q1'de işlemde olan {len(ev)} CIK; eşleşmeyenler: o çeyrekte bildirim yok, yeni CIK (yeniden yapılanma sonrası güncel CIK), yabancı özel ihraççı (Form 4 yok)"))
            M = Nd.merge(Su[["ACCESSION_NUMBER", "cik", "ISSUERTRADINGSYMBOL", "FILING_DATE", "DOCUMENT_TYPE"]], on="ACCESSION_NUMBER", how="left")
            kod = M.TRANS_CODE.value_counts(normalize=True).head(8).round(3).to_dict()
            gec = (pd.to_datetime(M.FILING_DATE, errors="coerce", format="mixed") - pd.to_datetime(M.TRANS_DATE, errors="coerce", format="mixed")).dt.days
            out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "işlem kodları + gecikme (2016q1, bütün)", "GECTI", "medyan bildirim gecikmesi (gün)", float(np.nanmedian(gec)),
                                     f"kod payları {kod}; gecikme %90 {float(np.nanpercentile(gec.dropna(), 90)) if gec.notna().any() else 'yok'} gün; P = açık piyasa alımı payı {kod.get('P', 0)}"))
            sat = set(M.loc[M.TRANS_CODE == "S", "ACCESSION_NUMBER"]); dip = Fo[Fo.ACCESSION_NUMBER.isin(sat)]
            plan_acc = set(dip.loc[dip.FOOTNOTE_TXT.fillna("").str.contains(r"10b5\s*-?\s*1", case=False, regex=True), "ACCESSION_NUMBER"])
            if "REMARKS" in Su:
                plan_acc |= set(Su.loc[Su.ACCESSION_NUMBER.isin(sat) & Su.REMARKS.fillna("").str.contains(r"10b5\s*-?\s*1", case=False, regex=True), "ACCESSION_NUMBER"])
            out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "10b5-1 dipnot vekili (2016q1, S içeren Form 4)", "KISMI", "plan geçen pay", round(len(plan_acc) / max(1, len(sat)), 3),
                                     f"{len(sat)} satışlı bildirim; 2023 öncesi işaret sütunu yok, plan yalnız dipnot / açıklama metninden (olumsuz cümleleri de yakalar)"))
            if Ornek is not None and len(Ornek):
                rows = []
                for r in Ornek.itertuples():
                    g = M[M.cik == r.cik]; rows.append(f"{r.sembol}({r.grup}): {len(g)} işlem {g.TRANS_CODE.value_counts().head(4).to_dict()}")
                bulunan = sum(1 for r in Ornek.itertuples() if (M.cik == r.cik).any())
                out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "örneklem (2016q1)", "GECTI" if bulunan else "KISMI", "işlemi olan sembol", f"{bulunan}/{len(Ornek)}", "; ".join(rows)))
        # 2023 sonrası plan işareti: son çeyreğin SUBMISSION başı (kısmi okuma)
        son = next((x for x in reversed(z) if re.search(r"/202[4-6]q\d_", x)), None)
        if son:
            L = zip_icerik_listesi(ist, son, "insider_son")
            if "dosya" in L:
                bas = zip_uye_bas(ist, son, L, "SUBMISSION.tsv", 200_000, "insider_son_sub"); S2 = pd.read_csv(io.BytesIO(bas[: bas.rfind(b"\n")]), sep="\t", dtype=str)
                kol = [c for c in S2.columns if "10B5" in c.upper()]
                out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "10b5-1 işareti (son çeyrek)", "GECTI" if kol else "KISMI", "sütun", ", ".join(kol) or "yok",
                                         f"{son.rsplit('/', 1)[-1]}; işaretli pay {round(float((S2[kol[0]].astype(str).str.strip() == '1').mean()), 3) if kol else '-'}", son))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "erişim", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}", url=SEC_IC_SAYFA))
    # projede var olan özet (K30): yalnız açık piyasa alımları
    m = os.path.join(A.iv, "veri2", "manifest.json")
    if os.path.exists(m):
        import json
        j = json.load(open(m, encoding="utf-8")); k = {a: v for a, v in j.get("veri", j).items() if "k30" in a} if isinstance(j, dict) else {}
        out.append(erisim_satiri(MODUL, "K30_ALIM", "projede mevcut", "KISMI", "dosya", ", ".join(k) or "manifestte yok", "yalnız P (açık piyasa alımı) özeti; satış / M / F / 10b5-1 yok"))
    return out
