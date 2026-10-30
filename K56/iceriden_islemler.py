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


def _ceyrek_islem(A: K56Ayar, ist: Istemci, url: str, ceyrek: str, plan: bool = False) -> pd.DataFrame:
    """Bir çeyreğin işlem tablosu (NONDERIV_TRANS + SUBMISSION). Yerel kopya (K56_FORM345 klasörü, K30 / K31 indirmesi) varsa ondan, yoksa SEC'ten."""
    yerel = os.path.join(os.environ.get("K56_FORM345", ""), f"{ceyrek}_form345.zip")
    veri = open(yerel, "rb").read() if (os.environ.get("K56_FORM345") and os.path.exists(yerel)) else ist.al(url, ad=f"insider_{ceyrek}.zip")[1]
    zf = zipfile.ZipFile(io.BytesIO(veri)); ad = {n.rsplit("/", 1)[-1]: n for n in zf.namelist()}
    kol = ["ACCESSION_NUMBER", "ISSUERCIK", "DOCUMENT_TYPE", "FILING_DATE"] + (["AFF10B5ONE"] if plan else [])
    Su = pd.read_csv(zf.open(ad["SUBMISSION.tsv"]), sep="\t", dtype=str, on_bad_lines="skip"); Su = Su[[c for c in kol if c in Su]]
    Nd = pd.read_csv(zf.open(ad["NONDERIV_TRANS.tsv"]), sep="\t", dtype=str, on_bad_lines="skip", usecols=lambda c: c in ("ACCESSION_NUMBER", "TRANS_CODE", "TRANS_DATE"))
    M = Nd.merge(Su, on="ACCESSION_NUMBER", how="left"); M["cik"] = pd.to_numeric(M.ISSUERCIK, errors="coerce")
    return M


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
                rows = []; bulunan = 0
                for r in Ornek.itertuples():
                    t = pd.Timestamp(r.tarih); c = f"{t.year}q{(t.month - 1) // 3 + 1}"
                    uc = next((x for x in z if f"/{c}_form345.zip" in x), None)
                    if uc is None:
                        rows.append(f"{r.sembol}({r.grup}) {c}: dosya yok"); continue
                    Mq = _ceyrek_islem(A, ist, uc, c)
                    g = Mq[Mq.cik == r.cik]; bulunan += int(len(g) > 0)
                    rows.append(f"{r.sembol}({r.grup}) {c}: {len(g)} işlem {g.TRANS_CODE.value_counts().head(3).to_dict()}")
                pay = bulunan / len(Ornek)
                out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "örneklem: olay çeyreğinde işlem", "GECTI" if pay >= 0.6 else "KISMI", "işlemi olan sembol", f"{bulunan}/{len(Ornek)}",
                                         "; ".join(rows) + "; yabancı özel ihraççı (BNS) Form 4 vermez; çeyrekte işlem olmaması veri eksikliği değildir"))
        # 2023 sonrası plan işareti (AFF10B5ONE): son tam çeyrek, '1' ve 'true' sayılır, payda S içeren Form 4
        son = next((x for x in reversed(z) if re.search(r"/202[4-6]q\d_", x)), None)
        if son:
            c = re.search(r"/(\d{4}q\d)_", son).group(1); Mq = _ceyrek_islem(A, ist, son, c, plan=True)
            s4 = Mq[(Mq.DOCUMENT_TYPE == "4") & (Mq.TRANS_CODE == "S")].drop_duplicates("ACCESSION_NUMBER")
            if "AFF10B5ONE" in s4:
                isaret = s4.AFF10B5ONE.astype(str).str.strip().str.lower().isin(["1", "true"])
                out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", f"10b5-1 işareti ({c}, S içeren Form 4)", "GECTI", "işaretli pay", round(float(isaret.mean()), 3),
                                         f"{len(s4)} satışlı Form 4; değerler {s4.AFF10B5ONE.astype(str).str.strip().str.lower().value_counts().head(5).to_dict()}; işaret fiilen 2023q2+ (2023q1 çoğu boş)", son))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "SEC_INSIDER_DS", "erişim", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}", url=SEC_IC_SAYFA))
    # projede var olan özet (K30): yalnız açık piyasa alımları
    m = os.path.join(A.iv, "veri2", "manifest.json")
    if os.path.exists(m):
        import json
        j = json.load(open(m, encoding="utf-8")); k = {a: v for a, v in j.get("veri", j).items() if "k30" in a} if isinstance(j, dict) else {}
        kap = "kapsam ölçülemedi (açılmış dosya yok)"
        for y in ("/tmp/veri2/k30_alim.pkl", os.path.join(A.veri, "k30_alim.pkl")):
            if os.path.exists(y):
                try:
                    X = pd.read_pickle(y); tk = next((c for c in ("D", "tarih", "TRANS_DATE", "FILING_DATE") if c in getattr(X, "columns", [])), None)
                    if tk:
                        t = pd.to_datetime(X[tk], errors="coerce"); kap = f"{t.min().date()} .. {t.max().date()}, {len(X)} satır; KEŞİF 2016-21: {int(((t >= '2016-01-01') & (t <= '2021-12-31')).sum())} satır"
                except Exception as ex:
                    kap = f"okunamadı: {type(ex).__name__}"
                break
        out.append(erisim_satiri(MODUL, "K30_ALIM", "projede mevcut özet", "KISMI", "kapsam", kap, "yalnız P (açık piyasa alımı) özeti; satış / M / F / 10b5-1 yok; KEŞİF için Insider DS P kodları"))
    return out
