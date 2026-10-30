"""K55 Faz 1 sürücüsü: D01-D06 + D10 OHLCV hücreleri, yalnız KEŞİF (2016-21), A / B / C, pencere varyantları, hücre içi Holm + aile (dal × yöntem) BH-FDR,
durum etiketleri (ONKAYIT 2.8). Faz 0 panelini ve olay tablosunu kullanır (aynı evren sürümü şart). Dal dal koşar; her dal sonunda rapor yazar.
Kesinlikle: İÇ DOĞRULAMA ve BAĞIMSIZ dönemler açılmaz; sonuç görüldükten sonra tanım / eşik değişmez (yeni tanım = yeni kimlik).
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from . import dal01_fiyat, dal02_hacim, dal03_volatilite, dal04_zaman, dal05_mikroyapi, dal06_goreli_guc, dal10_birlesik
from .dal_ortak import EK
from .evren import evren_kur
from .hucre import degisken_hesapla, hucre_kos, hucre_rng
from .hucreler import HUCRELER, temizle
from .istatistik import coklu_test_ozeti
from .ortak import DONEM, FDR_Q, K55Ayar, OLAY, cikti_dogrula, cy, gunluk_log, kosu_kimligi, log, veri_sha
from .raporlama import faz1_yaz

DALLAR = ("D01", "D02", "D03", "D04", "D05", "D06", "D10")
MODUL = {"D01": dal01_fiyat, "D02": dal02_hacim, "D03": dal03_volatilite, "D04": dal04_zaman, "D05": dal05_mikroyapi, "D06": dal06_goreli_guc, "D10": dal10_birlesik}
D10_BILESEN = (("D02-S02", 20), ("D03-S01", 20), ("D06-S01", 20), ("D01-S06", None), ("D06-S02", 60), ("D04-S08", None), ("D02-S05", 20))
_CTX: Dict[str, Any] = {}


def ek_kur(V: Dict[str, pd.DataFrame], EV: pd.DataFrame, endeks: pd.DataFrame) -> Dict[str, Any]:
    """D06 / D10 ek verileri: SPY, IWM kapanış; sektör eşit ağırlık günlük getiri; sektör liderleri (önceki yıl işlem değeri üst üçte bir) getirisi;
    her hisse tablosuna 'sektor' attr'ı."""
    ek: Dict[str, Any] = {"SPY": endeks["SPY"].dropna() if "SPY" in endeks else None, "IWM": endeks["IWM"].dropna() if "IWM" in endeks else None}
    sek = EV.set_index("sembol").sektor.to_dict(); R = {}; DV = {}
    for s, d in V.items():
        d.attrs["sektor"] = sek.get(s, "bilinmiyor"); R[s] = d.Close.astype(float).pct_change(fill_method=None); DV[s] = (d.Close * d.Volume).astype(float)
    Rt = pd.DataFrame(R); DVt = pd.DataFrame(DV); sg = {}; lg = {}
    for sk, grp in pd.Series(sek).groupby(pd.Series(sek)):
        uye = [s for s in grp.index if s in Rt]
        if len(uye) < 3 or sk == "bilinmiyor":
            continue
        sg[sk] = Rt[uye].mean(axis=1, skipna=True)
        yil = Rt.index.year; lider = pd.Series(np.nan, index=Rt.index)
        for y in np.unique(yil):
            onceki = DVt.loc[yil == y - 1, uye].median() if (yil == y - 1).any() else None
            if onceki is None or onceki.notna().sum() < 3:
                continue
            ust = onceki[onceki >= onceki.quantile(2 / 3)].index.tolist(); lider[yil == y] = Rt.loc[yil == y, ust].mean(axis=1, skipna=True)
        lg[sk] = lider
    ek["sektor_getiri"] = sg; ek["lider_getiri"] = lg; ek["sektor_of"] = sek
    EK.clear(); EK.update(ek); return ek


def hucreleri_kur(dallar: Tuple[str, ...] = DALLAR) -> None:
    temizle()
    for dal in dallar:
        MODUL[dal].kaydet_hucreler()


def _hucre_isci(kimlik: str) -> List[Dict[str, Any]]:
    P = _CTX["P"].copy(deep=False); V = _CTX["V"]; O = _CTX["O"]; t0 = time.time()
    try:
        rows = hucre_kos(kimlik, HUCRELER[kimlik], P, V, O, hucre_rng(kimlik, _CTX["tohum"]), donemler=("KESIF",), ufuklar=tuple(OLAY))
    except Exception as ex:
        rows = [{"hucre": kimlik, "dal": kimlik.split("-")[0], "varyant": "", "yontem": "-", "donem": "KESIF", "karar": f"HATA: {ex}"}]
        log.warning("hücre %s hata: %s", kimlik, ex)
    for r in rows:
        r["sure_sn"] = round(time.time() - t0, 1)
    return rows


def durum_etiketi(H: pd.DataFrame) -> pd.DataFrame:
    """Hücre başına durum (ONKAYIT 2.8 / v1.2): KEŞİF = A (FDR ret + ETKİ + yıl tekrarı ≥ 5/6 + rejim tutarlı) VEYA B (FDR ret + TUTAR + yıl tekrarı);
    VERİ YETERSİZ = bütün varyantlar yetersiz; REDDEDİLDİ = ötekiler. C yalnız destek (lift) olarak yazılır."""
    rows = []
    for kimlik, g in H.groupby("hucre"):
        a = g[g.yontem == "A"]; b = g[g.yontem == "B"]; c = g[g.yontem == "C"]
        a_ok = a[(a.karar == "ETKİ") & a.ret.fillna(False).astype(bool) & (a.yil_tekrar.fillna(0) >= np.minimum(5, a.yil_n.fillna(0))) & (a.yil_n.fillna(0) >= 5) & a.rejim_tutarli.fillna(False).astype(bool)] if len(a) else a
        b_ok = b[(b.karar == "TUTAR") & b.ret.fillna(False).astype(bool) & (b.yil_tekrar.fillna(0) >= np.minimum(5, b.yil_n.fillna(0))) & (b.yil_n.fillna(0) >= 5)] if len(b) else b
        hepsi_yetersiz = bool((g.karar.astype(str) == "VERİ YETERSİZ").all()) if len(g) else True
        hata = g.karar.astype(str).str.startswith("HATA").any()
        durum = "HATA" if hata and hepsi_yetersiz else ("VERİ YETERSİZ" if hepsi_yetersiz else ("KEŞİF" if (len(a_ok) or len(b_ok)) else "REDDEDİLDİ"))
        en_iyi_a = a.loc[a.p.idxmin()] if len(a) and a.p.notna().any() else None; en_iyi_b = b.loc[b.p.idxmin()] if len(b) and b.p.notna().any() else None
        rows.append({"hucre": kimlik, "dal": kimlik.split("-")[0], "soru": g.soru.iloc[0], "durum": durum, "A_etki_varyant": int(len(a_ok)), "B_tutar_varyant": int(len(b_ok)), "C_etki_varyant": int((c.karar == "ETKİ").sum()),
                     "varyant": int(g.varyant.nunique()), "A_en_iyi": en_iyi_a.varyant if en_iyi_a is not None else "", "A_d": en_iyi_a.d if en_iyi_a is not None else np.nan, "A_auc": en_iyi_a.auc if en_iyi_a is not None else np.nan,
                     "A_p_holm": en_iyi_a.p_holm if en_iyi_a is not None else np.nan, "A_q": en_iyi_a.q_bh if en_iyi_a is not None else np.nan,
                     "B_en_iyi": en_iyi_b.varyant if en_iyi_b is not None else "", "B_fark": en_iyi_b.fark if en_iyi_b is not None else np.nan, "B_fark_alt": en_iyi_b.fark_alt if en_iyi_b is not None else np.nan,
                     "B_p_holm": en_iyi_b.p_holm if en_iyi_b is not None else np.nan, "B_q": en_iyi_b.q_bh if en_iyi_b is not None else np.nan, "C_lift_max": c.lift.max() if len(c) and c.lift.notna().any() else np.nan,
                     "eksik_pay_max": g.eksik_pay.max() if "eksik_pay" in g else np.nan, "not": g["not"].iloc[0] if "not" in g else ""})
    return pd.DataFrame(rows)


def faz1(A: Optional[K55Ayar] = None, dallar: Tuple[str, ...] = DALLAR, panel_yol: Optional[str] = None, olay_yol: Optional[str] = None, paketler: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    A = A or K55Ayar(); gunluk_log(); A.cikti = cikti_dogrula(A.cikti); os.makedirs(A.cikti, exist_ok=True); t_bas = time.time()
    vsha = veri_sha(A); E = evren_kur(A, vsha, network=False); V, EV, surum = E["V"], E["EV"], E["surum"]
    kimlik = kosu_kimligi(A, surum, paketler, vsha); kimlik["faz"] = 1
    pyol = panel_yol or os.path.join(A.cikti, "panel", f"k55_panel_{A.ornek or 'tam'}.pkl"); oyol = olay_yol or os.path.join(A.cikti, "K55_OLAYLAR.csv.gz")
    for y in (pyol, oyol):
        if not os.path.exists(y):
            raise FileNotFoundError(f"Faz 0 çıktısı yok: {y} (önce faz0)")
    P = pd.read_pickle(pyol); O = pd.read_csv(oyol); O["tarih"] = pd.to_datetime(O.tarih)
    if "bitis" in O:
        O["bitis"] = pd.to_datetime(O.bitis)
    kj = os.path.join(A.cikti, "K55_KOSU.json")
    if os.path.exists(kj):
        k0 = json.load(open(kj, encoding="utf-8"))
        if k0.get("evren_surum") and k0["evren_surum"] != surum:
            raise RuntimeError(f"Faz 0 paneli başka evren sürümüyle kurulmuş ({k0['evren_surum'][:12]} ≠ {surum[:12]}); önce faz0 yeniden")
    if A.ornek:
        sec = set(P.sembol.unique()); V = {s: d for s, d in V.items() if s in sec}; EV = EV[EV.sembol.isin(sec)].reset_index(drop=True)
    C = cy(); endeks = C.cy_endeks(C.CYAyar(veri=A.veri, cikti=A.cikti, pazarlar=("ABD",)), C.CY); ek_kur(V, EV, endeks); hucreleri_kur(dallar)
    log.info("Faz 1: %d hücre, %d dal, panel %d satır, olay %d; kimlik %s", len(HUCRELER), len(dallar), len(P), len(O), kimlik["kimlik"])
    _CTX.update({"P": P, "V": V, "O": O, "tohum": A.tohum}); tum: List[Dict[str, Any]] = []; sure: Dict[str, float] = {}; R: Dict[str, Any] = {"kimlik": kimlik, "dal": {}}
    for dal in dallar:
        t0 = time.time(); kimlikler = [k for k, v in HUCRELER.items() if v["dal"] == dal]
        if dal == "D10":
            for kb, p in D10_BILESEN:                                       # kesitsel bileşikler için bileşen sütunları ana panelde
                if kb in HUCRELER and kb not in P:
                    P[kb], _ = degisken_hesapla(P, V, HUCRELER[kb], p, kb)
            _CTX["P"] = P
        if A.isci > 1 and len(kimlikler) > 1:
            with mp.get_context("fork").Pool(min(A.isci, len(kimlikler))) as hv:
                sonuc = hv.map(_hucre_isci, kimlikler, chunksize=1)
        else:
            sonuc = [_hucre_isci(k) for k in kimlikler]
        rows = [r for rs in sonuc for r in rs]; tum += rows; sure[dal] = round(time.time() - t0, 1)
        H = pd.DataFrame(tum); Hp = H[H.p.notna()] if "p" in H else H.iloc[0:0]
        Hc, yuk = coklu_test_ozeti(Hp, FDR_Q) if len(Hp) else (H.assign(p_holm=np.nan, q_bh=np.nan, ret=False), pd.DataFrame())
        if len(Hp):
            H = H.merge(Hc[["hucre", "varyant", "yontem", "ufuk", "donem", "p_holm", "q_bh", "ret"]].drop_duplicates(), on=["hucre", "varyant", "yontem", "ufuk", "donem"], how="left") if "ufuk" in H else H.merge(Hc[["hucre", "varyant", "yontem", "donem", "p_holm", "q_bh", "ret"]].drop_duplicates(), on=["hucre", "varyant", "yontem", "donem"], how="left")
        D = durum_etiketi(H); H.to_csv(os.path.join(A.cikti, "K55_VARYANTLAR.csv"), index=False); D.to_csv(os.path.join(A.cikti, "K55_HUCRE_SONUC.csv"), index=False); yuk.to_csv(os.path.join(A.cikti, "K55_COKLU_TEST.csv"), index=False)
        R.update({"H": H, "D": D, "yuk": yuk, "sure": sure, "tamamlanan": [d_ for d_ in dallar if d_ in sure]}); R["dal"][dal] = {"hucre": len(kimlikler), "satir": len(rows), "sure_sn": sure[dal]}
        faz1_yaz(R, A.cikti); log.info("Faz 1 %s bitti: %d hücre, %d satır, %.0f sn; durum %s", dal, len(kimlikler), len(rows), sure[dal], D[D.dal == dal].durum.value_counts().to_dict())
    R["toplam_sure_dk"] = round((time.time() - t_bas) / 60, 1); faz1_yaz(R, A.cikti)
    with open(os.path.join(A.cikti, "K55_KOSU_FAZ1.json"), "w", encoding="utf-8") as f:
        json.dump({**kimlik, "sure": sure, "toplam_dk": R["toplam_sure_dk"]}, f, ensure_ascii=False, indent=1, default=str)
    return R
