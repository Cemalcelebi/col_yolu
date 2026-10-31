"""K56-EVREN2 (ONKAYIT_K56 v1.2-C + v1.2-a): Tiingo Kasım kotasıyla indirilen batan şirketlerle yeni evren sürümü ve etkisi.

Sıra: indirme (batan_evren.tiingo_indir) -> indirme_sonrasi (seri denetimi, Ö2 CIK bağlama, SEC geçmişi, sınıflandırma) -> evren2_kur (K55 evren_insa
AYNEN, girdiye yeni seriler eklenerek) -> panel_olay (K55 panel_kur / olaylar AYNEN) -> etki (faz1_yerel motoru, yalnız A1: 125 KEŞİF satırının d(i) / d(ii)
KEŞİF ve İÇ'te; BAĞIMSIZ kapalı). K51-K55 evreni, panelleri ve sonuçları değişmez; v2 çıktıları ayrı klasöre ve ayrı sürüm kimliğiyle yazılır.
Getiri (asıl): yeni şirketlerde seri_erken = False -> pencere seri sonunu aşarsa TANIMSIZ; son işlem fiyatı tasfiye ödemesi sayılmaz; eksik delist
getirisi uydurulmaz.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import re
import os
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from . import batan_evren as BE
from .ortak import K56Ayar, KaynakKaydi, log

SIC_BOLUM = [(100, "Tarım"), (1000, "Madencilik"), (1500, "İnşaat"), (4000, "İmalat"), (5000, "Ulaştırma-Kamu"), (5200, "Toptan"),
             (6000, "Perakende"), (6800, "Finans"), (9100, "Hizmet"), (10000, "Kamu")]          # COL_YOLU_ABD.cy_sektor (K34) ile aynı tablo


def sic_bolum(sic: Any) -> str:
    try:
        x = float(sic)
    except (TypeError, ValueError):
        return "bilinmiyor"
    if not np.isfinite(x):
        return "bilinmiyor"
    return next((ad for s, ad in SIC_BOLUM if x < s), "Diğer")


def yeni_seri_oku(yol: str, kriz: pd.Timestamp) -> Optional[pd.DataFrame]:
    """COL_YOLU_ABD.cy_veri_yukle'nin K34 Tiingo okuma biçimi (düzeltilmiş OHLCV) + _cy_temizle."""
    from K55.ortak import cy
    t = pd.read_csv(yol)
    if not len(t) or "adjClose" not in t:
        return None
    t.index = pd.to_datetime(t.date.str[:10]); d = t[["adjOpen", "adjHigh", "adjLow", "adjClose", "adjVolume"]].astype(float)
    d.columns = ["Open", "High", "Low", "Close", "Volume"]
    return cy()._cy_temizle(d, kriz)


def meta_adi(klasor: str, sembol: str) -> Optional[str]:
    y = os.path.join(klasor, "meta", f"{sembol}.json")
    if not os.path.exists(y):
        return None
    try:
        return (json.load(open(y, encoding="utf-8")) or {}).get("name")
    except Exception:
        return None


def indirme_sonrasi(A: K56Ayar, ist: Any, ADAY: pd.DataFrame, klasor: str, N25: pd.DataFrame, T: pd.DataFrame, sec_yol: str) -> pd.DataFrame:
    """Aday başına: seri denetimi (v1.2-a), Ö2 için Tiingo meta adı + 25-NSE ile CIK (cik_bagla), SEC geçmişi (yalnız yeni CIK'ler; e-posta SEC_EPOSTA),
    sınıflandırma (K54 kuralı, T = indirilen serinin son günü)."""
    Y = ADAY.copy(); Y["bitis"] = pd.to_datetime(Y.bitis); dur = [BE.seri_denetimi(os.path.join(klasor, f"{s}.csv"), b) for s, b in zip(Y.sembol, Y.bitis)]
    Y["seri_durum"] = [d[0] for d in dur]; Y["seri_son"] = [d[1] for d in dur]; Y["seri_n"] = [d[2] for d in dur]
    Y["tiingo_ad"] = [meta_adi(klasor, s) for s in Y.sembol]
    onceki = Y["baglama"] if "baglama" in Y else pd.Series("", index=Y.index)          # meta aşamasının bağlama yöntemi korunur
    Y["baglama"] = np.where(onceki.fillna("").astype(str) != "", onceki.fillna("").astype(str), np.where(Y.cik.notna(), "K34 eşleme (Ö1)", ""))
    for k in Y.index[Y.cik.isna()]:
        c, how = BE.cik_bagla(Y.at[k, "sembol"], Y.at[k, "tiingo_ad"], Y.at[k, "bitis"], N25); Y.at[k, "cik"] = c if c is not None else np.nan; Y.at[k, "baglama"] = how
    yeni = sorted(int(c) for c in Y.cik.dropna().unique())
    sec = BE.sec_gecmis(ist, yeni, sec_yol) if ist is not None else (json.load(open(sec_yol, encoding="utf-8")) if os.path.exists(sec_yol) else {})
    ct = json.load(open("/tmp/k55/company_tickers.json", encoding="utf-8")); bugun = {v["ticker"].upper().replace(".", "-"): int(v["cik_str"]) for v in ct.values()}
    son = {s: (t if pd.notna(t) else b) for s, t, b in zip(Y.sembol, Y.seri_son, Y.bitis)}       # inmeyen seride None -> NaT; Tiingo bitişi kullanılır
    S = BE.siniflandir(Y.drop(columns=["seri_son"]), sec, T, bugun, son)
    S["seri_son"] = S.sembol.map(dict(zip(Y.sembol, Y.seri_son)))
    return S


def evren2_kur(A: K56Ayar, Y: pd.DataFrame, klasor: str, ek_sha: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """K55/evren.evren_kur ile aynı yol (ağ kapalı yükleme, K54 tabloları, evren_insa) + yeni seriler. Dönüş: evren_insa sözlüğü + surum, yeni (rapor)."""
    from K55 import evren as KE
    from K55.ortak import K55Ayar, cy, sha256_dosya, veri_sha
    A55 = K55Ayar(veri=A.veri, cikti=os.path.join(A.onbellek, "evren_v2", "k55"), k54=A.abd, isci=1); os.makedirs(A55.cikti, exist_ok=True)
    C = cy(); KE.yukleyici_esigi_dogrula(); Ac = C.CYAyar(veri=A55.veri, cikti=A55.cikti, pazarlar=("ABD",), is_parcacigi=1)
    SD, ES, dosya_sha = KE._k54_oku(A55); fon_disi = set(pd.read_csv(os.path.join(KE.KOK, "evren_disi_ABD.csv")).sembol.map(KE.sembol_normalize))
    eski = C.cy_tiingo_indir
    try:
        C.cy_tiingo_indir = lambda *a, **k: 0
        with KE.ag_kapali():
            Vs, EV_ham = C.cy_veri_yukle(Ac, C.CY)
    finally:
        C.cy_tiingo_indir = eski
    V_ham = Vs["ABD"]; EV_ham = EV_ham[EV_ham.pazar == "ABD"].copy()
    kisa, eksik = KE._ham_kisa_ve_eksik(A55, {KE.sembol_normalize(s): 1 for s in V_ham}, fon_disi)
    kriz = pd.Timestamp(C.CY["kriz"]); ev, sd, es, rap = [], [], [], []
    es_v = ES[ES.sembol.map(KE.sembol_normalize).isin({KE.sembol_normalize(x) for x in V_ham})] if "cik" in ES else ES.iloc[:0]   # yalnız K55 yükleyicisinde serisi olanlar
    cik_var = set(pd.to_numeric(es_v.cik, errors="coerce").dropna().astype(int)) if "cik" in es_v else set(); cik_yeni: set = set()
    for r in Y.itertuples():
        s = KE.sembol_normalize(r.sembol); kay = "K56_" + ("O1" if str(r.kaynak).startswith("Ö1") else "O2")
        if r.seri_durum != "TAMAM":
            rap.append({"sembol": s, "kaynak": kay, "durum": r.seri_durum}); continue
        if s in V_ham or s in fon_disi:
            rap.append({"sembol": s, "kaynak": kay, "durum": "K55 evreninde / fon (eklenmedi)"}); continue
        c = int(r.cik) if pd.notna(r.cik) else None
        if c is not None and (c in cik_var or c in cik_yeni):
            rap.append({"sembol": s, "kaynak": kay, "durum": "CIK tekrarı (aynı şirket K55'te ya da başka yeni sembolde; eklenmedi)"}); continue
        try:
            d = yeni_seri_oku(os.path.join(klasor, f"{r.sembol}.csv"), kriz)
        except Exception as ex:
            rap.append({"sembol": s, "kaynak": kay, "durum": f"okunamadı: {type(ex).__name__}"}); continue
        if d is None or len(d) < KE.YUKLEYICI_MIN_GUN:
            rap.append({"sembol": s, "kaynak": kay, "durum": f"kısa seri ({0 if d is None else len(d)} < {KE.YUKLEYICI_MIN_GUN})"})
            kisa = pd.concat([kisa, pd.DataFrame([{"sembol": s, "kaynak": kay, "n_gun": 0 if d is None else len(d)}])], ignore_index=True); continue
        V_ham[s] = d; cik_yeni |= {c} if c is not None else set()
        ev.append({"pazar": "ABD", "sembol": s, "kaynak": kay, "evren_bas": d.index[0], "batan": True, "agirlik": 1.0})
        sd.append({"sembol": s, "kaynak": kay, "cik": r.cik, "sinif": r.k54_sinif, "alt": r.k54_alt or "", "kural": r.k54_kural, "cikis_islemi": r.cikis_islemi,
                   "kesim_tarihi": r.kesim_tarihi or "", "erken_bitti": r.erken_bitti})
        es.append({"sembol": s, "cik": r.cik, "sec_ad": r.sec_ad or (r.tiingo_ad or "")}); rap.append({"sembol": s, "kaynak": kay, "durum": "eklendi (evren_insa'ya)"})
    SD2 = pd.concat([SD, pd.DataFrame(sd)], ignore_index=True, sort=False); ES2 = pd.concat([ES, pd.DataFrame(es)], ignore_index=True, sort=False)
    EV2 = pd.concat([EV_ham, pd.DataFrame(ev)], ignore_index=True, sort=False)
    R = KE.evren_insa(V_ham, EV2, SD2, ES2, fon_disi, kisa, eksik)
    yk = R["EV"].kaynak.str.startswith("K56_")
    sek = C.cy_sektor(Ac, R["EV"]); R["EV"]["sektor"] = R["EV"].sembol.map(sek).fillna("bilinmiyor")
    sic = dict(zip(Y.sembol.map(KE.sembol_normalize), Y.sic))
    R["EV"].loc[yk, "sektor"] = R["EV"].loc[yk, "sembol"].map(lambda s: sic_bolum(sic.get(s)))
    R["EV"].loc[yk, "seri_erken"] = False                                     # asıl: yeni şirkette pencere seri sonunu aşarsa TANIMSIZ
    ysha = hashlib.sha256("\n".join(f"{s}:{sha256_dosya(os.path.join(klasor, f'{s}.csv'))}" for s in sorted(Y.sembol[Y.seri_durum == "TAMAM"])).encode()).hexdigest()
    R["surum"] = KE.evren_surum(R["EV"], {**dosya_sha, "K56_EVREN2_TIINGO": ysha, "K56_EVREN2_SINIF": hashlib.sha256(pd.DataFrame(sd).to_csv(index=False).encode()).hexdigest(),
                                          **(ek_sha or {})}, veri_sha(A55))
    D = R["disi"]; R["yeni"] = pd.DataFrame(rap).merge(D[D.sembol.isin([x["sembol"] for x in ev])].rename(columns={"kategori": "evren_disi", "ayrinti": "evren_disi_ayrinti"}), on="sembol", how="left")
    R["yeni"]["evrende"] = R["yeni"].sembol.isin(set(R["EV"].sembol)); R["A55"] = A55
    log.info("evren v2: %d sembol (yeni %d / aday %d); sürüm %s", len(R["EV"]), int(yk.sum()), len(Y), R["surum"][:12])
    return R


def panel_olay(R: Dict[str, Any], isci: int = 3) -> Dict[str, Any]:
    """K55 panel_kur + olaylar + D10 bileşenleri (faz1_yerel.k55_veri ile aynı ek veri)."""
    from K55.faz1 import D10_BILESEN, DALLAR, ek_kur, hucreleri_kur
    from K55.hucre import degisken_hesapla
    from K55.hucreler import HUCRELER
    from K55.olay_tanimlari import olaylar
    from K55.ortak import cy
    from K55.panel import panel_kur
    A55 = R["A55"]; A55.isci = isci; C = cy(); endeks = C.cy_endeks(C.CYAyar(veri=A55.veri, cikti=A55.cikti, pazarlar=("ABD",)), C.CY)
    P, likit_map, bilgi = panel_kur(R["V"], R["EV"], A55, endeks); O, say = olaylar(R["V"], likit_map)
    ek_kur(R["V"], R["EV"], endeks); hucreleri_kur(DALLAR)
    for kb, p in D10_BILESEN:
        if kb in HUCRELER and kb not in P:
            P[kb], _ = degisken_hesapla(P, R["V"], HUCRELER[kb], p, kb)
    return {"P": P, "V": R["V"], "EV": R["EV"], "O": O, "endeks": endeks, "evren_surum": R["surum"], "panel_bilgi": bilgi}


def olay_karsilastir(O1: pd.DataFrame, O2: pd.DataFrame, EV2: pd.DataFrame) -> pd.DataFrame:
    """Olay sayıları dönem × ufuk: K55 (eski) / v2 (yeni) / v2'de yeni şirketlerden gelen."""
    yeni = set(EV2.sembol[EV2.kaynak.str.startswith("K56_")]); izin = ("KESIF", "IC_DOGRULAMA")            # BAĞIMSIZ / PURGE / EMBARGO sayılmaz (kapı dışı hesap yok)
    O1 = O1[O1.donem.isin(izin)]; O2 = O2[O2.donem.isin(izin)]
    a = O1.groupby(["donem", "ufuk"]).size().rename("k55"); b = O2.groupby(["donem", "ufuk"]).size().rename("v2")
    c = O2[O2.sembol.isin(yeni)].groupby(["donem", "ufuk"]).size().rename("v2_yeni_sirket")
    k = O2[~O2.sembol.isin(yeni)].groupby(["donem", "ufuk"]).size().rename("v2_k55_sirket")      # likit eşiği / sıralar kesitsel: yeni seriler K55 şirketlerini de kaydırır
    T = pd.concat([a, b, c, k], axis=1).fillna(0).astype(int).reset_index(); T["fark"] = T.v2 - T.k55; T["fark_k55_sirket"] = T.v2_k55_sirket - T.k55
    return T


def kapsam_tablosu(Y: pd.DataFrame, R: Dict[str, Any], V: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Yeni şirket başına tarihsel kapsam: ilk / son gün, gün sayısı, KEŞİF / İÇ / BAĞIMSIZ dönemlerindeki gün sayısı."""
    from K55.evren import sembol_normalize
    rows = []
    for r in Y.itertuples():
        s = sembol_normalize(r.sembol); d = V.get(s)
        x = {"sembol": s, "kaynak": r.kaynak, "cik": r.cik, "baglama": r.baglama, "sinif_k56": r.sinif_k56, "seri_durum": r.seri_durum,
             "evrende": bool(s in set(R["EV"].sembol))}
        if d is not None:
            ix = d.index
            x.update({"ilk": ix[0].date(), "son": ix[-1].date(), "n_gun": len(ix), "gun_kesif": int(((ix >= "2016-01-01") & (ix <= "2021-12-31")).sum()),
                      "gun_ic": int(((ix >= "2022-01-01") & (ix <= "2023-12-31")).sum()), "gun_2024_sonrasi_var": bool((ix >= "2024-01-01").any())})
        rows.append(x)
    return pd.DataFrame(rows)


def getiri_duyarlilik(P: pd.DataFrame, EV: pd.DataFrame, Y: pd.DataFrame) -> pd.DataFrame:
    """Yeni şirketlerin likit satırlarında 60 / 120 / 250 günlük penceresi seri sonunu aşanlar (asıl: TANIMSIZ). Duyarlılıkta İFLAS -> −%100,
    BİRLEŞME -> son kapanış olurdu; A1 olay / nitelikli gün tanımı tam pencere istediği için A1 sonuçlarını etkilemez (yalnız sayılır)."""
    from K55.evren import sembol_normalize
    yeni = EV[EV.kaynak.str.startswith("K56_")].sembol; sn = dict(zip(Y.sembol.map(sembol_normalize), Y.sinif_k56)); rows = []
    for h in (60, 120, 250):
        c = f"bitis{h}"
        if c not in P:
            continue
        Q = P[P.sembol.isin(yeni) & P.likit & (P.tarih <= pd.Timestamp("2023-12-31"))][["sembol", c]]; Q = Q.assign(sinif=Q.sembol.map(sn), tanimsiz=Q[c].isna())
        for k, g in Q.groupby("sinif"):
            rows.append({"ufuk_gun": h, "sinif_k56": k, "likit_satir": len(g), "pencere_tanimsiz": int(g.tanimsiz.sum()),
                         "duyarlilik": "−%100" if k == "İFLAS" else ("son kapanış" if k == "BİRLEŞME" else "TANIMSIZ kalır")})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- v1.3 aday doğrulama (Cemal, 31 Eki madde 6): kimlik, adi hisse, fiyat kapsamı, son işlem, sınıf
AD_DISI = r"\b(WARRANTS?|RIGHTS?|PREFERRED|PFD|NOTES?|DEBENTURES?|BONDS?|SENIOR|SUBORDINATED|CUMULATIVE|PERPETUAL|CONTINGENT VALUE|CVR|ETF|ETN|EXCHANGE TRADED)\b|%"
AD_ISARET = r"\b(TRUST|FUND|BDC)\b"
ACIKLAMA_ISARET = r"exchange-traded|seeks to track|closed-end|blank check"
OTC_BORSA = ("PINK", "EXPM", "OTCMKTS", "OTCQX", "OTCQB", "OTCCE", "OTCGREY", "GREY", "OTC")
DONEMSEL = ("10-K", "10-Q", "10-K/A", "10-Q/A", "20-F", "40-F", "10-KT")
CIKIS = ("25-NSE", "15-12B", "15-12G", "15-15D")


def meta_oku(klasor: str, sembol: str) -> Optional[Dict[str, Any]]:
    y = os.path.join(klasor, "meta", f"{sembol}.json")
    if not os.path.exists(y):
        return None
    try:
        return json.load(open(y, encoding="utf-8")) or None
    except Exception:
        return {"_hata": "okunamadı"}


def _tarihler(sec: Optional[Dict[str, Any]], kosul) -> List[pd.Timestamp]:
    from .kurumsal_olaylar import _liste
    if not sec:
        return []
    t, f, it = _liste(sec.get("date", "[]")), _liste(sec.get("form", "[]")), _liste(sec.get("items", "[]"))
    it = it or [""] * len(f)
    return sorted(pd.Timestamp(a) for a, b, c in zip(t, f, it) if kosul(str(b), str(c)))


def adi_hisse_ad(ad: Optional[str], aciklama: Optional[str]) -> Tuple[str, str]:
    """C-2 ad / açıklama kuralı: ('DIŞI' | 'İŞARET' | '', neden)."""
    a = str(ad or "").upper()
    if re.search(AD_DISI, a):
        return "DIŞI", f"ad: {re.search(AD_DISI, a).group(0)}"
    if re.search(r"\bUNITS?\b", a):
        return ("İŞARET", "ad: COMMON UNITS / LP (MLP)") if (re.search(r"COMMON UNITS", a) or re.search(r"\bL\.?P\.?\b", a)) else ("DIŞI", "ad: UNIT")
    if re.search(r"\bL\.?P\.?$|\bLIMITED PARTNERSHIP\b", a):
        return "İŞARET", "ad: LP (ortaklık payı)"
    if "DEPOSITARY" in a:
        return ("İŞARET", "ad: AMERICAN DEPOSITARY (ADR)") if "AMERICAN DEPOSITARY" in a else ("DIŞI", "ad: DEPOSITARY")
    if re.search(AD_ISARET, a):
        return "İŞARET", f"ad: {re.search(AD_ISARET, a).group(0)}"
    if aciklama and re.search(ACIKLAMA_ISARET, str(aciklama), re.I):
        return "İŞARET", "açıklama: fon / boş çek"
    return "", ""


def kimlik_ad(tiingo_ad: Optional[str], sec: Optional[Dict[str, Any]]) -> Tuple[str, float, float, str]:
    """C-1: Tiingo adı ile SEC adı / eski adları. Dönüş: (UYUMLU | YAKIN | UYUMSUZ | META YOK | SEC YOK, Jaccard, oran, eşleşen SEC adı)."""
    if not tiingo_ad:
        return "META YOK", np.nan, np.nan, ""
    if not sec:
        return "SEC YOK", np.nan, np.nan, ""
    adlar = [sec.get("name")] + [x.get("name") for x in (sec.get("formerNames") or [])]
    en = ("UYUMSUZ", 0.0, 0.0, "")
    for a in [x for x in adlar if x]:
        if BE.ad_norm(a) == BE.ad_norm(tiingo_ad):
            return "UYUMLU", 1.0, 1.0, a
        j, o = BE.ad_benzerlik(tiingo_ad, a)
        if (j >= 0.50 or o >= 0.85) and (j, o) > en[1:3]:
            en = ("YAKIN", j, o, a)
        elif en[0] == "UYUMSUZ" and (j, o) > en[1:3]:
            en = ("UYUMSUZ", j, o, a)
    return en


def meta_dogrulama(A: K56Ayar, ist: Any, ADAY: pd.DataFrame, klasor: str, N25: pd.DataFrame, T: pd.DataFrame, sec_yol: str) -> pd.DataFrame:
    """v1.3 meta aşaması (fiyat görülmeden): meta varlık (±10 iş günü), adi hisse (ad / açıklama), Ö2 CIK bağlama (iki kademe), SEC geçmişi, kimlik
    (Tiingo adı ~ SEC adı), SEC kapsamı (son dönemsel rapor), ön ek (seri başı ilk SEC başvurusundan > 400 gün önce), SPAC / OTC işaretleri, ön sınıf.
    fiyat_iste = hiçbir DIŞI kuralına takılmayan aday."""
    rows = []
    for r in ADAY.itertuples():
        m = meta_oku(klasor, r.sembol); d = {"sembol": r.sembol, "kaynak": r.kaynak, "cik": r.cik, "aday_baslangic": r.baslangic, "aday_bitis": r.bitis, "aday_borsa": r.borsa,
                                             "isaret_on": getattr(r, "isaret_on", "") if isinstance(getattr(r, "isaret_on", ""), str) else ""}
        d["meta_durum"] = "YOK" if m is None else ("HATA" if "_hata" in m else "VAR"); m = m if d["meta_durum"] == "VAR" else {}
        d.update({"tiingo_ad": m.get("name"), "tiingo_borsa": m.get("exchangeCode"), "meta_baslangic": m.get("startDate"), "meta_bitis": m.get("endDate"),
                  "meta_aciklama_var": bool(m.get("description"))})
        dis, isr = [], ([d["isaret_on"]] if d["isaret_on"] else [])
        if d["meta_durum"] == "VAR":
            for ad_, a_, b_ in (("başlangıç", m.get("startDate"), r.baslangic), ("bitiş", m.get("endDate"), r.bitis)):
                if a_ and b_ and abs(len(pd.bdate_range(*sorted([pd.Timestamp(a_[:10]), pd.Timestamp(str(b_)[:10])]))) - 1) > 10:
                    dis.append(f"META VARLIK: {ad_} {a_[:10]} ≠ liste {str(b_)[:10]}")
            k, n = adi_hisse_ad(m.get("name"), m.get("description"))
            (dis if k == "DIŞI" else isr).append(n) if k else None
        elif str(r.kaynak).startswith("Ö1"):
            dis.append(f"META {d['meta_durum']}: kimlik doğrulanamadı (Cemal madde 6)")
        else:
            isr.append(f"meta {d['meta_durum']}")
        if pd.isna(r.cik):
            c, how = BE.cik_bagla(r.sembol, m.get("name"), pd.Timestamp(r.bitis), N25); d["cik"] = c if c is not None else np.nan; d["baglama"] = how
            if how == "benzer ad + tarih":
                isr.append("CIK benzer adla bağlandı")
        else:
            d["baglama"] = "K34 eşleme (Ö1)"
        rows.append((d, dis, isr))
    yeni = sorted({int(d["cik"]) for d, _, _ in rows if pd.notna(d["cik"])})
    sec = BE.sec_gecmis(ist, yeni, sec_yol) if ist is not None else (json.load(open(sec_yol, encoding="utf-8")) if os.path.exists(sec_yol) else {})
    ct = json.load(open("/tmp/k55/company_tickers.json", encoding="utf-8")); bugun = {v["ticker"].upper().replace(".", "-"): int(v["cik_str"]) for v in ct.values()}
    out = []
    for d, dis, isr in rows:
        s = sec.get(str(int(d["cik"]))) if pd.notna(d["cik"]) else None; s = s if (s and "hata" not in s) else None
        kim, j, o, eslesen = kimlik_ad(d["tiingo_ad"], s); d.update({"kimlik_ad": kim, "ad_jaccard": j, "ad_oran": o, "ad_eslesen_sec": eslesen, "sec_ad": (s or {}).get("name"),
                                                                    "sic": (s or {}).get("sic"), "sec_var": s is not None})
        if pd.isna(d["cik"]):
            dis.append("CIK bağlanamadı (sınıf 6)")
        elif s is None:
            dis.append("SEC geçmişi yok")
        if kim == "UYUMSUZ":                                              # v1.3-a: Ö1 ve Ö2'de (sembol + tarih bağlamasında ad uyumsuzsa başka şirket)
            dis.append(f"KİMLİK: Tiingo adı SEC adlarıyla uyumsuz (Jaccard {j:.2f})")
        elif kim == "YAKIN":
            isr.append("kimlik YAKIN")
        otc = str(d["aday_borsa"]).upper() in OTC_BORSA or str(d["sembol"]).upper().endswith("Q") or "OTC devamı" in str(d["isaret_on"])
        if otc:
            isr.append("OTC")
        if s is not None:
            bit = pd.Timestamp(str(d["aday_bitis"])[:10]); donemsel = [x for x in _tarihler(s, lambda f, it: f in DONEMSEL) if x <= bit + pd.Timedelta(days=30)]
            d["son_donemsel"] = donemsel[-1].date() if donemsel else None; ilk = _tarihler(s, lambda f, it: True); d["ilk_sec_basvuru"] = ilk[0].date() if ilk else None
            if donemsel and (bit - donemsel[-1]).days > 400:
                (isr if otc else dis).append(f"SEC KAPSAM: son dönemsel rapor {donemsel[-1].date()} (> 400 gün önce)")
            elif not donemsel:
                (isr if otc else dis).append("SEC KAPSAM: dönemsel rapor yok")
            seri_bas = max(pd.Timestamp(str(d["meta_baslangic"] or d["aday_baslangic"])[:10]), pd.Timestamp("2015-01-01"))
            if ilk and ilk[0] >= pd.Timestamp("2003-01-01") and (ilk[0] - seri_bas).days > 400:
                dis.append(f"ÖN EK: seri başı {seri_bas.date()} ilk SEC başvurusundan ({ilk[0].date()}) > 400 gün önce")
            if str(s.get("sic") or "") == "6770" or re.search(r"ACQUISITION (CORP|CO|LTD|INC)|BLANK CHECK", str(s.get("name") or "").upper()):
                isr.append("SPAC")
        d["evren_disi_on"] = "; ".join(dis); d["isaretler_on"] = "; ".join(x for x in isr if x); d["fiyat_iste"] = not dis
        out.append(d)
    M = pd.DataFrame(out)
    pre = BE.siniflandir(M.rename(columns={"aday_baslangic": "baslangic", "aday_bitis": "bitis", "aday_borsa": "borsa"})[["cik", "sembol", "kaynak", "baslangic", "bitis", "borsa"]].assign(
        bitis=lambda x: pd.to_datetime(x.bitis)), sec, T, bugun)
    M["sinif_on_k54"] = M.sembol.map(dict(zip(pre.sembol, pre.k54_sinif))); M["sinif_on_k56"] = M.sembol.map(dict(zip(pre.sembol, pre.sinif_k56)))
    return M


def fiyat_son_islem_denetimi(Y: pd.DataFrame, M: pd.DataFrame, klasor: str, sec: Dict[str, Any], kriz: pd.Timestamp) -> pd.DataFrame:
    """v1.3 fiyat aşaması: C-3 fiyat kapsamı (K55 veri_kalitesi.sembol_kalite işaretleri; düzeltilmiş / ham oran, bölünme / temettü sayısı; dönem gün
    sayıları), C-4 son işlem tarihi (listeli: çıkış belgesi ±10 / ±45 gün; OTC: belge T+10'dan önce ve T son 15-12 / dönemsel rapordan en çok 180 gün sonra),
    C-5 ön / son sınıf. Getiriye dayalı dışlama yok."""
    from K55.veri_kalitesi import sembol_kalite
    rows = []; Mi = M.set_index("sembol")
    for r in Y.itertuples():
        d = {"sembol": r.sembol, "seri_durum": r.seri_durum, "seri_son": r.seri_son, "seri_n": r.seri_n, "sinif_son_k54": r.k54_sinif, "sinif_son_k56": r.sinif_k56,
             "sinif_on_k54": Mi.sinif_on_k54.get(r.sembol), "sinif_on_k56": Mi.sinif_on_k56.get(r.sembol)}
        d["sinif_degisti"] = str(d["sinif_on_k56"]) != str(d["sinif_son_k56"]); isr, dis = [], []
        yol = os.path.join(klasor, f"{r.sembol}.csv")
        if r.seri_durum == "TAMAM" and os.path.exists(yol):
            ham = pd.read_csv(yol); s_ = yeni_seri_oku(yol, kriz); q = sembol_kalite(r.sembol, s_)
            d.update({"n_temiz": len(s_) if s_ is not None else 0, "veri_hatasi": q.get("veri_hatasi"), "veri_yetersiz": q.get("veri_yetersiz"), "supheli_sicrama": q.get("supheli_sicrama"),
                      "bolunme_n": int((pd.to_numeric(ham.get("splitFactor", pd.Series(1.0)), errors="coerce").fillna(1.0) != 1.0).sum()),
                      "temettu_n": int((pd.to_numeric(ham.get("divCash", pd.Series(0.0)), errors="coerce").fillna(0.0) > 0).sum()),
                      "adj_oran_son": float(ham.adjClose.iloc[-1] / ham.close.iloc[-1]) if len(ham) and ham.close.iloc[-1] else np.nan})
            ix = s_.index if s_ is not None else pd.DatetimeIndex([])
            d.update({"gun_kesif": int(((ix >= "2016-01-01") & (ix <= "2021-12-31")).sum()), "gun_ic": int(((ix >= "2022-01-01") & (ix <= "2023-12-31")).sum())})
            for k in ("veri_hatasi", "veri_yetersiz", "supheli_sicrama"):
                if d.get(k):
                    isr.append(f"{k}: {d[k]}")
            if np.isfinite(d["adj_oran_son"]) and abs(d["adj_oran_son"] - 1) > 0.01:
                isr.append(f"son gün düzeltilmiş / ham oranı {d['adj_oran_son']:.3f}")
            # C-4
            s = sec.get(str(int(r.cik))) if pd.notna(r.cik) else None; s = s if (s and "hata" not in s) else None
            T = pd.Timestamp(r.seri_son) if pd.notna(r.seri_son) else None; otc = str(Mi.aday_borsa.get(r.sembol, "")).upper() in OTC_BORSA or str(r.sembol).upper().endswith("Q") or "OTC devamı" in str(Mi.isaret_on.get(r.sembol, ""))
            if s is not None and T is not None:
                E = _tarihler(s, lambda f, it: f in CIKIS or (f.startswith("8-K") and ("2.01" in it or "3.01" in it)))
                fark = min((abs((e - T).days) for e in E), default=np.nan); d["cikis_belge_fark_gun"] = fark
                if not otc:
                    d["son_islem"] = "TUTARLI" if fark <= 10 else ("YAKIN" if fark <= 45 else "UYUMSUZ")
                else:
                    E2_ = [e for e in E + _tarihler(s, lambda f, it: f.startswith("8-K") and "1.03" in it) if e <= T + pd.Timedelta(days=10)]
                    dayanak = max([x for x in _tarihler(s, lambda f, it: f in ("15-12B", "15-12G") or f in DONEMSEL) if x <= T] or [pd.NaT])
                    d["son_islem"] = "TUTARLI" if (E2_ and pd.notna(dayanak) and (T - dayanak).days <= 180) else "OTC KUYRUĞU"
                if d["son_islem"] in ("UYUMSUZ", "OTC KUYRUĞU"):
                    isr.append(f"son işlem {d['son_islem']} (en yakın çıkış belgesi {fark} gün)")
            else:
                d["son_islem"] = "UYGULANAMAZ"
        if d["sinif_degisti"]:
            isr.append(f"sınıf ön {d['sinif_on_k56']} -> son {d['sinif_son_k56']}")
        d["isaretler_fiyat"] = "; ".join(isr); d["evren_disi_fiyat"] = "; ".join(dis); rows.append(d)
    return pd.DataFrame(rows)


ISARET_ALT_KUME = ("SPAC", "OTC", "ADR", "kimlik YAKIN", "OTC KUYRUĞU", "5. harf F", "5. harf Y", "CIK benzer adla", "LP", "meta ")


def dogrulama_tablosu(M: pd.DataFrame, F: pd.DataFrame, yeni: pd.DataFrame) -> pd.DataFrame:
    """Aday başına son doğrulama satırı: meta aşaması + fiyat aşaması + evren_insa sonucu; evren_disi_neden (ilk DIŞI), isaretler, duyarlılık alt kümesi."""
    from K55.evren import sembol_normalize
    D = M.merge(F.drop(columns=[c for c in ("sinif_on_k54", "sinif_on_k56") if c in F]), on="sembol", how="left"); y = yeni.copy(); y["sembol"] = y.sembol.astype(str); m = dict(zip(y.sembol, y.durum)); dd = dict(zip(y.sembol, y.get("evren_disi_ayrinti", pd.Series(dtype=object))))
    D["evren_insa"] = D.sembol.map(lambda s: m.get(sembol_normalize(s), "")); D["evren_insa_ayrinti"] = D.sembol.map(lambda s: dd.get(sembol_normalize(s), ""))
    ev_icinde = set(y.sembol[y.get("evrende", pd.Series(False, index=y.index)).fillna(False).astype(bool)])
    D["evrende"] = D.sembol.map(lambda s: sembol_normalize(s) in ev_icinde)
    def neden(r):
        for k in ("evren_disi_on", "evren_disi_fiyat"):
            if isinstance(r.get(k), str) and r[k]:
                return r[k].split("; ")[0]
        if r.get("seri_durum") not in (None, "TAMAM") and isinstance(r.get("seri_durum"), str):
            return f"seri: {r['seri_durum']}"
        if not r["evrende"]:
            a_ = r.get("evren_insa_ayrinti"); b_ = r.get("evren_insa")
            return a_ if isinstance(a_, str) and a_ else (b_ if isinstance(b_, str) and b_ else "evren dışı")
        return ""
    D["evren_disi_neden"] = D.apply(neden, axis=1)
    D["isaretler"] = (D.isaretler_on.fillna("") + "; " + D.isaretler_fiyat.fillna("")).str.strip("; ")
    D["duyarlilik_disi"] = D.isaretler.map(lambda x: any(k in str(x) for k in ISARET_ALT_KUME))
    return D
