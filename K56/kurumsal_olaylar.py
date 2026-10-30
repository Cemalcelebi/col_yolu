"""K56 D (+ F, G) — kurumsal olaylar, kasıt kanıtı kaynakları ve veri hatası denetimi.

D: SEC başvuru geçmişi (islenmis-veri k55/sec_ozet.json: 3.262 CIK, bütün başvurular 1990'lar -> 2026-10-30, form + tarih + 8-K madde kodları).
   Olaylar: hisse ihracı / izahname (S-1, S-3, S-3ASR, 424B1 / 4 / 5; 424B2 çoğunlukla banka yapılandırılmış borç notu, ayrı sayılır; form türü
   hisse mi borç mu ayırmaz -> hisse sayısıyla doğrulanır), kayıtsız satış (8-K 3.02), önemli sözleşme / borç (1.01 / 2.03), iflas
   (1.03), birleşme tamamlanması (2.01), borsa kotu (3.01; 25-NSE), kayıt sonu (15-12B / 15-12G), %5 üstü sahiplik (SC 13D / 13G ve
   değişiklikleri; konu şirketin başvuru listesinde), birleşme oy belgesi (DEFM14A), ihale teklifi (SC TO-T / TO-I), geç bildirim (NT 10-K / Q),
   bölünme / ters bölünme için 8-K 5.03 (esas sözleşme; tek başına bölünme kanıtı değil). Bölünmeler ayrıca Yahoo (yfinance splits).
F: SEC işlem askıya alma listesi (sayfalı tablo: tarih, şirket adı, 34- bülten no; SEMBOL YOK -> ad eşlemesi), SEC dava bültenleri (sayfa).
   Kasıt yalnız bu tür resmî kayıtla gösterilir (ONKAYIT_K56 3); kayıt yalnız yakalananları kapsar ve yıllar sonra gelir.
G: veri hatası: V_ABD gece açılış sıçramalarının Yahoo bölünme tarihleriyle çakışması (düzeltme hatası), XBRL hisse sayısının bölünmeye göre
   düzeltilmemiş olması (sulandırma ölçüsünü bozar).
"""
from __future__ import annotations

import json
import os
import pickle
import re
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from .ortak import Istemci, K56Ayar, erisim_satiri

MODUL = "kurumsal_olaylar"
SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
ASKIYA_ALMA = "https://www.sec.gov/enforcement-litigation/trading-suspensions"
DAVA = "https://www.sec.gov/enforcement-litigation/litigation-releases"
OLAY_FORMLARI = {"ihrac_izahname": r"^(S-1|S-3|S-3ASR|424B1|424B4|424B5)$", "borc_notu_424B2": r"^424B2$", "sahiplik_13D": r"^SC 13D(/A)?$", "sahiplik_13G": r"^SC 13G(/A)?$", "ihale": r"^SC TO-(T|I)(/A)?$",
                 "birlesme_oy": r"^DEFM14A$", "kot_cikis": r"^(25-NSE|15-12B|15-12G)$", "gec_bildirim": r"^NT 10-(K|Q)$"}
OLAY_MADDELERI = {"8K_kayitsiz_satis": "3.02", "8K_iflas": "1.03", "8K_birlesme": "2.01", "8K_kot": "3.01", "8K_esas_sozlesme": "5.03", "8K_borc": "2.03", "8K_sozlesme": "1.01"}


def _liste(x: Any) -> List[str]:
    if isinstance(x, list):
        return [str(v) for v in x]
    try:
        import ast
        return [str(v) for v in ast.literal_eval(x)]
    except Exception:
        return []


def sec_ozet_yukle(A: K56Ayar) -> Dict[str, Any]:
    """islenmis-veri k55 paketinden açılmış sec_ozet.json (önce /tmp/k55, sonra paketten K55/veri_paket.ac ile). Yeniden indirme yok."""
    y = "/tmp/k55/sec_ozet.json"
    if not os.path.exists(y):
        from K55 import veri_paket
        veri_paket.ac(os.path.join(A.iv, "k55"), "/tmp/k55")
    return json.load(open(y, encoding="utf-8"))


def olay_tablosu(J: Dict[str, Any], cik: int, bas: str = "2016-01-01", son: str = "2026-08-31") -> pd.DataFrame:
    v = J.get(str(int(cik)))
    if not v:
        return pd.DataFrame()
    T = pd.DataFrame({"form": _liste(v["form"]), "tarih": pd.to_datetime(_liste(v["date"]), errors="coerce"), "madde": _liste(v.get("items", "[]"))})
    return T[(T.tarih >= bas) & (T.tarih <= son)]


def olay_sayilari(T: pd.DataFrame) -> Dict[str, int]:
    out = {k: int(T.form.str.match(p).sum()) for k, p in OLAY_FORMLARI.items()} if len(T) else {k: 0 for k in OLAY_FORMLARI}
    k8 = T[T.form.isin(["8-K", "8-K/A"])] if len(T) else T
    out.update({k: int(k8.madde.str.contains(re.escape(m)).sum()) if len(k8) else 0 for k, m in OLAY_MADDELERI.items()})
    return out


def _ad_norm(s: str) -> str:
    s = re.sub(r"[^A-Z0-9 ]", " ", str(s).upper()); s = re.sub(r"\b(INC|CORP|CORPORATION|CO|LTD|LIMITED|PLC|HOLDINGS|HOLDING|GROUP|THE|LLC|LP|SA|NV|AG)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def erisim_testi(A: K56Ayar, ist: Istemci, Ornek: pd.DataFrame, EV: pd.DataFrame) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    # D1) yerel SEC başvuru özeti: kapsam ve örneklem olayları (ağ yok)
    try:
        J = sec_ozet_yukle(A); ilk = pd.to_datetime(pd.Series([min(_liste(v["date"])) for v in J.values() if _liste(v["date"])]))
        n8 = sum(1 for v in J.values() for f in _liste(v["form"]) if f == "8-K"); n8i = sum(1 for v in J.values() for f, i in zip(_liste(v["form"]), _liste(v.get("items", "[]"))) if f == "8-K" and i)
        eslesen = EV.cik.dropna().astype(int).astype(str).isin(set(J)).mean()
        out.append(erisim_satiri(MODUL, "SEC_SUBMISSIONS_OZET", "yerel kapsam (islenmis-veri k55)", "GECTI", "K55 evreni CIK eşleşmesi", round(float(eslesen), 3),
                                 f"{len(J)} CIK; ilk başvuru medyanı {ilk.median().date()}; 8-K {n8}, madde kodu dolu pay {round(n8i / max(1, n8), 3)}; yeniden indirme gerekmez"))
        rows = []
        for r in Ornek.itertuples():
            T = olay_tablosu(J, r.cik); s = olay_sayilari(T); rows.append({"sembol": r.sembol, "grup": r.grup, "basvuru": len(T), **s})
        Z = pd.DataFrame(rows)
        out.append(erisim_satiri(MODUL, "SEC_SUBMISSIONS_OZET", "örneklem olayları 2016-26", "GECTI", "olaylı sembol", int((Z.drop(columns=["sembol", "grup", "basvuru"]).sum(axis=1) > 0).sum()),
                                 "; ".join(f"{x['sembol']}({x['grup']}) ihraç {x['ihrac_izahname']} 13D {x['sahiplik_13D']} 13G {x['sahiplik_13G']} 3.02 {x['8K_kayitsiz_satis']} 1.03 {x['8K_iflas']} "
                                           f"2.01 {x['8K_birlesme']} 25/15 {x['kot_cikis']}" for x in Z.to_dict("records"))))
        out[-1]["tablo"] = Z.to_dict("records")
        # canlı karşılaştırma (tazelik): iki CIK için submissions JSON'daki son başvuru tarihi
        for r in Ornek.head(2).itertuples():
            d, veri, _ = ist.al(SUBMISSIONS.format(cik=int(r.cik)), ad=f"submissions_{int(r.cik)}.json", sinir=20_000_000)
            if d == 200:
                S = json.loads(veri.decode()); son_canli = max(S["filings"]["recent"]["filingDate"]); son_yerel = max(_liste(J[str(int(r.cik))]["date"])) if str(int(r.cik)) in J else "-"
                out.append(erisim_satiri(MODUL, "SEC_SUBMISSIONS", f"canlı tazelik ({r.sembol})", "GECTI", "son başvuru canlı / yerel", f"{son_canli} / {son_yerel}",
                                         f"recent {len(S['filings']['recent']['form'])} kayıt + eski dosya {len(S['filings'].get('files', []))}", SUBMISSIONS.format(cik=int(r.cik))))
            else:
                out.append(erisim_satiri(MODUL, "SEC_SUBMISSIONS", f"canlı tazelik ({r.sembol})", "BASARISIZ", ayrinti=f"HTTP {d}"))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "SEC_SUBMISSIONS_OZET", "kapsam", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}"))
    # G) bölünme: Yahoo splits + V_ABD gece sıçraması çakışması (düzeltme hatası denetimi)
    try:
        import yfinance as yf
        yv = os.path.join(A.veri, "V_ABD.pkl"); V = pickle.load(open(yv, "rb")) if os.path.exists(yv) else {}
        bilinen = [("AAPL", "2020-08-31"), ("TSLA", "2020-08-31"), ("NVDA", "2021-07-20")]
        semb = list(dict.fromkeys([s for s, _ in bilinen] + list(Ornek.sembol)))
        rows = []
        for s in semb:
            try:
                sp = yf.Ticker(s).splits
            except Exception as ex:
                rows.append({"sembol": s, "durum": f"hata {type(ex).__name__}"}); continue
            if sp is None or not hasattr(sp, "index"):
                rows.append({"sembol": s, "durum": "yanıt yok (Yahoo erişim engeli / 401 / 429)"}); continue
            sp = sp[sp.index >= pd.Timestamp("2016-01-01", tz=sp.index.tz)] if len(sp) else sp
            d = V.get(s); sicra = []
            if d is not None and len(sp):
                for t, oran in sp.items():
                    t0 = pd.Timestamp(t.date()); i = d.index.searchsorted(t0)
                    if 0 < i < len(d):
                        g = float(d.Open.iloc[i] / d.Close.iloc[i - 1]); sicra.append(round(g, 3))
            rows.append({"sembol": s, "durum": "ok", "bolunme_2016": len(sp), "oranlar": [round(float(x), 3) for x in sp.values][:4], "V_ABD_gece_orani": sicra[:4], "V_ABD_var": d is not None})
        Z = pd.DataFrame(rows); ok = Z[Z.durum == "ok"] if len(Z) else Z
        if not len(ok):
            out.append(erisim_satiri(MODUL, "YAHOO_SPLITS", "bölünme listesi", "BASARISIZ", "yanıt", f"0/{len(Z)}", "Yahoo bu ortamdan engelli (crumb 401 / 429); Colab'da yeniden denenmeli; "
                                     "seçenekler: Tiingo splitFactor (kota), XBRL StockholdersEquityNoteStockSplitConversionRatio1, Nasdaq / NYSE bildirimleri", "https://query1.finance.yahoo.com"))
            raise StopIteration
        bozuk = [r.sembol for r in ok.itertuples() if isinstance(r.V_ABD_gece_orani, list) and any(abs(x - 1) > 0.25 for x in r.V_ABD_gece_orani)]
        out.append(erisim_satiri(MODUL, "YAHOO_SPLITS", "bölünme listesi + V_ABD düzeltme denetimi", "GECTI" if len(ok) else "BASARISIZ", "düzeltilmemiş sıçrama", len(bozuk),
                                 "; ".join(f"{r.sembol}: {r.bolunme_2016} bölünme {r.oranlar} V_ABD gece oranı {r.V_ABD_gece_orani}" for r in ok.itertuples() if r.bolunme_2016)[:580]
                                 + f"; V_ABD {'yüklü' if V else 'YOK (CY_VERI ayarlı değil)'}", "https://query1.finance.yahoo.com (yfinance)"))
    except StopIteration:
        pass
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "YAHOO_SPLITS", "bölünme", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}"))
    # F) SEC işlem askıya alma listesi (bütün sayfalar, ad eşlemesi) + dava bültenleri sayfası
    try:
        rows = []
        for sayfa in range(0, 40):
            d, h, _ = ist.al(f"{ASKIYA_ALMA}?page={sayfa}", ad=f"askiya_{sayfa}.html", sinir=3_000_000)
            if d != 200:
                break
            tr = re.findall(r"<tr[^>]*>(.*?)</tr>", h.decode("utf-8", "replace"), flags=re.S); yeni = 0
            for t in tr:
                m = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})', t); no = re.search(r"(34-\d+)", t); res = re.search(r"release-view__respondents'?\"?>(.*?)</div>", t, flags=re.S)
                if m and no and res:
                    for ad in re.findall(r"<a[^>]*>(.*?)</a>", res.group(1), flags=re.S) or [re.sub(r"<[^>]+>", " ", res.group(1))]:
                        ad = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", ad)).strip()
                        if ad:
                            rows.append({"tarih": pd.to_datetime(m.group(1)), "ad": ad, "no": no.group(1)}); yeni += 1
            if not yeni:
                break
        S = pd.DataFrame(rows).drop_duplicates(["no", "ad"]) if rows else pd.DataFrame(columns=["tarih", "ad", "no"])
        adlar = {}
        for cik, v in sec_ozet_yukle(A).items():
            for a in [v.get("name", "")] + [x.get("name", "") for x in (v.get("formerNames") if isinstance(v.get("formerNames"), list) else [])]:
                if a and _ad_norm(a):
                    adlar[_ad_norm(a)] = cik
        S["eslesen_cik"] = S.ad.map(lambda a: adlar.get(_ad_norm(a)) if _ad_norm(a) else None)
        es = S[S.eslesen_cik.notna()]
        out.append(erisim_satiri(MODUL, "SEC_ASKIYA_ALMA", "liste (bütün sayfalar) + evren ad eşlemesi", "GECTI" if len(S) else "BASARISIZ", "askıya alma / evrenle eşleşen",
                                 f"{len(S)} / {len(es)}", f"{S.no.nunique()} bülten; tarih {S.tarih.min().date() if len(S) else '-'} .. {S.tarih.max().date() if len(S) else '-'}; sembol YOK, ad eşlemesi; eşleşenler: "
                                 + "; ".join(f"{r.ad} {r.tarih.date()}" for r in es.head(8).itertuples()), ASKIYA_ALMA))
        d, h, _ = ist.al(DAVA, ad="dava_0.html", sinir=3_000_000); tr = re.findall(r"LR-\d+", h.decode("utf-8", "replace")) if d == 200 else []
        out.append(erisim_satiri(MODUL, "SEC_DAVA", "ilk sayfa", "GECTI" if tr else "BASARISIZ", "bülten no (ilk sayfa)", len(set(tr)), "başlıklarda kişi / şirket adı; sembol yok; ayrıntı metinde", DAVA))
    except Exception as ex:
        out.append(erisim_satiri(MODUL, "SEC_ASKIYA_ALMA", "liste", "BASARISIZ", ayrinti=f"{type(ex).__name__}: {ex}", url=ASKIYA_ALMA))
    return out
