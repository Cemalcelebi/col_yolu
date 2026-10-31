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
    Y["tiingo_ad"] = [meta_adi(klasor, s) for s in Y.sembol]; Y["baglama"] = np.where(Y.cik.notna(), "K34 eşleme (Ö1)", "")
    for k in Y.index[Y.cik.isna()]:
        c, how = BE.cik_bagla(Y.at[k, "sembol"], Y.at[k, "tiingo_ad"], Y.at[k, "bitis"], N25); Y.at[k, "cik"] = c if c is not None else np.nan; Y.at[k, "baglama"] = how
    yeni = sorted(int(c) for c in Y.cik.dropna().unique())
    sec = BE.sec_gecmis(ist, yeni, sec_yol) if ist is not None else (json.load(open(sec_yol, encoding="utf-8")) if os.path.exists(sec_yol) else {})
    ct = json.load(open("/tmp/k55/company_tickers.json", encoding="utf-8")); bugun = {v["ticker"].upper().replace(".", "-"): int(v["cik_str"]) for v in ct.values()}
    son = {s: (t if t is not None else b) for s, t, b in zip(Y.sembol, Y.seri_son, Y.bitis)}
    S = BE.siniflandir(Y.drop(columns=["seri_son"]), sec, T, bugun, son)
    S["seri_son"] = S.sembol.map(dict(zip(Y.sembol, Y.seri_son)))
    return S


def evren2_kur(A: K56Ayar, Y: pd.DataFrame, klasor: str) -> Dict[str, Any]:
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
    for r in Y.itertuples():
        s = KE.sembol_normalize(r.sembol); kay = "K56_" + ("O1" if str(r.kaynak).startswith("Ö1") else "O2")
        if r.seri_durum != "TAMAM":
            rap.append({"sembol": s, "kaynak": kay, "durum": r.seri_durum}); continue
        if s in V_ham or s in fon_disi:
            rap.append({"sembol": s, "kaynak": kay, "durum": "K55 evreninde / fon (eklenmedi)"}); continue
        try:
            d = yeni_seri_oku(os.path.join(klasor, f"{r.sembol}.csv"), kriz)
        except Exception as ex:
            rap.append({"sembol": s, "kaynak": kay, "durum": f"okunamadı: {type(ex).__name__}"}); continue
        if d is None or len(d) < KE.YUKLEYICI_MIN_GUN:
            rap.append({"sembol": s, "kaynak": kay, "durum": f"kısa seri ({0 if d is None else len(d)} < {KE.YUKLEYICI_MIN_GUN})"})
            kisa = pd.concat([kisa, pd.DataFrame([{"sembol": s, "kaynak": kay, "n_gun": 0 if d is None else len(d)}])], ignore_index=True); continue
        V_ham[s] = d
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
    R["surum"] = KE.evren_surum(R["EV"], {**dosya_sha, "K56_EVREN2_TIINGO": ysha, "K56_EVREN2_SINIF": hashlib.sha256(pd.DataFrame(sd).to_csv(index=False).encode()).hexdigest()}, veri_sha(A55))
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
    yeni = set(EV2.sembol[EV2.kaynak.str.startswith("K56_")])
    a = O1.groupby(["donem", "ufuk"]).size().rename("k55"); b = O2.groupby(["donem", "ufuk"]).size().rename("v2")
    c = O2[O2.sembol.isin(yeni)].groupby(["donem", "ufuk"]).size().rename("v2_yeni_sirket")
    T = pd.concat([a, b, c], axis=1).fillna(0).astype(int).reset_index(); T["fark"] = T.v2 - T.k55
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
                      "gun_ic": int(((ix >= "2022-01-01") & (ix <= "2023-12-31")).sum()), "gun_bagimsiz": int((ix >= "2024-01-01").sum())})
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
        Q = P[P.sembol.isin(yeni) & P.likit][["sembol", c]]; Q = Q.assign(sinif=Q.sembol.map(sn), tanimsiz=Q[c].isna())
        for k, g in Q.groupby("sinif"):
            rows.append({"ufuk_gun": h, "sinif_k56": k, "likit_satir": len(g), "pencere_tanimsiz": int(g.tanimsiz.sum()),
                         "duyarlilik": "−%100" if k == "İFLAS" else ("son kapanış" if k == "BİRLEŞME" else "TANIMSIZ kalır")})
    return pd.DataFrame(rows)
