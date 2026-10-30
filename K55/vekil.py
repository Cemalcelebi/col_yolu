"""K55 vekil / bilinen etki kıyası (K55_PLAN bölüm 2.7; ONKAYIT ek v1.4). Faz 1'den sonra, ayrı adım (python K55.py vekil).

Her seçilen hücrenin en iyi varyantı (A_en_iyi, yoksa B_en_iyi) KEŞİF döneminde likit panel satırlarında bilinen ölçülerle Spearman
korelasyonuna girer: r20 (1 ay tersine dönüş), r60, mom12_1 (250 gün getirisi, son 20 gün hariç; Ç121 momentum kıyası), dd250 (düşüş),
vol60, log_dv20 (büyüklük / likidite), ar20 (K51 imza aralığı), hacim_orani (20 / 120 gün hacim; K51 hacim kuruması vekili).
|ρ| > 0,8 -> 'vekil': bağımsız bilgi iddiası düşer (hücre durumu değiştirilmez, yalnız işaretlenir).
Ek teşhis (eşik değil): A yöntemi dd250 katmanlı — gün × oynaklık ondalığı × dd250 üçlüsü içinde z; olay öncesi farkın derin düşüşten
gelip gelmediğini gösterir (Y60, KEŞİF).
Seçim (varsayılan): durumu KEŞİF olan hücreler + tanım notunda 'vekil' / 'kıyas' geçen hücreler. Modül yalnız okur ve raporlar.
"""
from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from .hucre import _donem_sec, degisken_hesapla
from .hucreler import HUCRELER
from .istatistik import auc, d_boot_ay
from .ortak import BOOT, K55Ayar, cikti_dogrula, cy, gunluk_log, kosu_kimligi, log, veri_sha

BILINEN = ("r20", "r60", "mom12_1", "dd250", "vol60", "log_dv20", "ar20", "hacim_orani")
VEKIL_ESIK = 0.8
ORNEK_SATIR = 200_000
SECIM_NOT = ("vekil", "kıyas", "kiyas")


def bilinen_olculer(P: pd.DataFrame, V: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Panele bilinen ölçü sütunlarını ekler: r20, mom12_1, hacim_orani (r60, dd250, vol60, log_dv20, ar20 panelde var). Panel sembol içinde
    tarih sıralı ve ardışık işlem günlüdür (panel_kur); hacim oranı hisse tablosundan 'i' satır konumuyla alınır."""
    P = P.copy(); g = P.groupby("sembol", sort=False)
    P["r20"] = P.close / g.close.shift(20) - 1; P["mom12_1"] = g.close.shift(20) / g.close.shift(250) - 1
    hr = {}
    for s, d in V.items():
        v = d.Volume.astype(float); hr[s] = (v.rolling(20, min_periods=10).mean() / v.rolling(120, min_periods=60).mean().replace(0, np.nan)).to_numpy()
    out = np.full(len(P), np.nan); sem = P.sembol.to_numpy(); ii = P.i.to_numpy(); bas = 0; n = len(P)
    while bas < n:
        son = bas
        while son < n and sem[son] == sem[bas]:
            son += 1
        h = hr.get(sem[bas])
        if h is not None and len(h) >= ii[son - 1] + 1:
            out[bas:son] = h[ii[bas:son]]
        bas = son
    P["hacim_orani"] = out
    return P


def hucre_sec(D: pd.DataFrame, yalniz: Optional[List[str]] = None) -> List[str]:
    """Varsayılan seçim: KEŞİF + notunda vekil / kıyas geçen kayıtlı hücreler; yalniz verilirse yalnız o liste (kayıtlı olanlar)."""
    if yalniz:
        return [h for h in yalniz if h in HUCRELER]
    sec = set(D.loc[D.durum == "KEŞİF", "hucre"]) if len(D) else set()
    for k, t in HUCRELER.items():
        n_ = str(t.get("not") or t.get("not_") or "").lower()
        if any(a in n_ for a in SECIM_NOT):
            sec.add(k)
    return [h for h in D.hucre if h in sec] if len(D) else sorted(sec)


def _dd250_katmanli_A(D2: pd.DataFrame, var: str, O: pd.DataFrame, rng: np.random.Generator) -> Dict[str, Any]:
    """Gün × vd × dd250 üçlüsü içinde z; Y60 KEŞİF olayları için Cohen d (ay kümeli bootstrap) ve AUC."""
    bos = {"d": np.nan, "d_alt": np.nan, "d_ust": np.nan, "auc": np.nan, "n_olay": 0}
    if not len(D2):
        return bos
    D2 = D2.copy(); D2["ddt"] = D2.groupby("tarih").dd250.rank(pct=True).fillna(0.5).mul(3).clip(upper=2.999).astype(int)
    g = D2.groupby(["tarih", "vd", "ddt"])[var]; z = (D2[var] - g.transform("mean")) / g.transform("std").replace(0, np.nan); z[g.transform("size") < 5] = np.nan
    Ou = O[(O.ufuk == "Y60") & (O.donem == "KESIF")]; anahtar = set(zip(Ou.sembol, Ou.tarih))
    olay = np.fromiter(((s, t) in anahtar for s, t in zip(D2.sembol, D2.tarih)), bool, len(D2)); zv = z.to_numpy(float)
    if olay.sum() < 30 or np.isfinite(zv[olay]).sum() < 30:
        return {**bos, "n_olay": int(olay.sum())}
    d_, a_, b_, _ = d_boot_ay(zv, olay, D2.ay.to_numpy(), max(200, BOOT // 2), rng)
    return {"d": d_, "d_alt": a_, "d_ust": b_, "auc": auc(zv[olay], zv[~olay]), "n_olay": int(olay.sum())}


def vekil_kiyas(D: pd.DataFrame, P: pd.DataFrame, V: Dict[str, pd.DataFrame], O: pd.DataFrame, rng: np.random.Generator, yalniz: Optional[List[str]] = None) -> pd.DataFrame:
    """D: K55_HUCRE_SONUC (hucre, durum, A_en_iyi, B_en_iyi). Hücre başına: korelasyon tablosu, en yakın bilinen ölçü, vekil işareti, dd250 katmanlı A."""
    P = bilinen_olculer(P, V); L = (P.likit.astype(bool) & (P.donem60 == "KESIF")).to_numpy(); rows = []
    for h in hucre_sec(D, yalniz):
        r = D[D.hucre == h].iloc[0] if (len(D) and (D.hucre == h).any()) else None; tanim = HUCRELER[h]
        var = ""
        if r is not None:
            for k in ("A_en_iyi", "B_en_iyi"):
                if isinstance(r.get(k), str) and r.get(k):
                    var = r[k]; break
        if not var:
            var = f"{h}|{tanim['pencereler'][0] if tanim['pencereler'][0] is not None else 'tek'}"
        p_ = var.split("|")[1]; p_ = None if p_ == "tek" else int(p_); t0 = time.time()
        try:
            x, _ = degisken_hesapla(P, V, tanim, p_, var)
        except Exception as ex:
            log.warning("vekil %s hesaplanamadı: %s", var, ex); rows.append({"hucre": h, "varyant": var, "hata": str(ex)}); continue
        P[var] = x.to_numpy(np.float32) if hasattr(x, "to_numpy") else np.asarray(x, np.float32); m = L & np.isfinite(P[var].to_numpy(float)); n_m = int(m.sum())
        S = P.loc[m].sample(min(ORNEK_SATIR, n_m), random_state=7) if n_m else P.iloc[0:0]
        kor = {b: (float(S[[var, b]].corr(method="spearman").iloc[0, 1]) if (len(S) and b in S) else np.nan) for b in BILINEN}
        en = max(kor, key=lambda k_: abs(kor[k_]) if np.isfinite(kor[k_]) else -1.0)
        katman = _dd250_katmanli_A(_donem_sec(P.loc[m], "KESIF", "donem60"), var, O, rng)
        rows.append({"hucre": h, "durum": (r.durum if r is not None else ""), "varyant": var, "n_satir": n_m, **{f"rho_{b}": v for b, v in kor.items()}, "en_yakin_bilinen": en,
                     "en_yakin_rho": kor.get(en, np.nan), "vekil": bool(np.isfinite(kor.get(en, np.nan)) and abs(kor[en]) > VEKIL_ESIK), "A_dd250_katmanli_d": katman["d"],
                     "A_dd250_katmanli_d_alt": katman["d_alt"], "A_dd250_katmanli_d_ust": katman["d_ust"], "A_dd250_katmanli_auc": katman["auc"], "A_dd250_katmanli_n": katman["n_olay"],
                     "A_d_faz1": (r.get("A_d") if r is not None else np.nan), "sure_sn": round(time.time() - t0, 1)})
        P.drop(columns=[var], inplace=True); log.info("vekil %s: en yakın %s ρ=%.2f%s; dd250 katmanlı d=%.3f (%.0f sn)", var, en, kor.get(en, np.nan), " VEKİL" if rows[-1]["vekil"] else "", katman["d"] if np.isfinite(katman["d"]) else np.nan, time.time() - t0)
    return pd.DataFrame(rows)


def vekil_yaz(T: pd.DataFrame, kimlik: Dict[str, Any], cikti: str) -> str:
    from .raporlama import tablo
    L = [f"# K55 — VEKİL / BİLİNEN ETKİ KIYASI (bölüm 2.7; {kimlik['kimlik']}; KEŞİF 2016-21, likit satırlar)", "",
         f"- Bilinen ölçüler: {', '.join(BILINEN)}. Spearman ρ, en çok {ORNEK_SATIR:,} satırlık rastgele örneklem. |ρ| > {VEKIL_ESIK} -> VEKİL (bağımsız bilgi iddiası düşer; hücre durumu değişmez).",
         "- mom12_1 = Ç121 momentum kıyası (D06-S01 için zorunlu). hacim_orani = K51 hacim kuruması vekili; ar20 = K51 imza aralığı.",
         "- A dd250 katmanlı: gün × oynaklık ondalığı × dd250 üçlüsü içinde z, Y60 olayları; Faz 1 A_d ile kıyaslanır (büyük fark = etki düşüş derinliğinden geliyor).", ""]
    if len(T):
        L += ["## Özet", ""] + tablo(T, ["hucre", "durum", "varyant", "n_satir", "en_yakin_bilinen", "en_yakin_rho", "vekil", "A_d_faz1", "A_dd250_katmanli_d", "A_dd250_katmanli_d_alt", "A_dd250_katmanli_auc", "A_dd250_katmanli_n"])
        L += ["", "## Korelasyon tablosu", ""] + tablo(T, ["hucre", "varyant"] + [f"rho_{b}" for b in BILINEN])
        vk = T[T.get("vekil", pd.Series(False, index=T.index)).fillna(False).astype(bool)]
        L += ["", f"- VEKİL işaretli hücre: {len(vk)}" + (f" -> {', '.join(f'{r.hucre} ({r.en_yakin_bilinen} ρ={r.en_yakin_rho:+.2f})' for r in vk.itertuples())}" if len(vk) else "")]
    else:
        L += ["(seçilen hücre yok)"]
    yol = os.path.join(cikti, "K55_VEKIL.md"); open(yol, "w", encoding="utf-8").write("\n".join(L) + "\n"); return yol


def vekil(A: Optional[K55Ayar] = None, hucreler: Optional[List[str]] = None, panel_yol: Optional[str] = None, olay_yol: Optional[str] = None, paketler: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """Faz 1 sonrası vekil kıyası: Faz 0 paneli + olaylar + K55_HUCRE_SONUC.csv okunur; K55_VEKIL.csv / .md yazılır. Koşu kimliği kaydedilir."""
    from .faz1 import D10_BILESEN, DALLAR, ek_kur, hucreleri_kur
    from .evren import evren_kur
    A = A or K55Ayar(); gunluk_log(); A.cikti = cikti_dogrula(A.cikti); t_bas = time.time()
    vsha = veri_sha(A); E = evren_kur(A, vsha, network=False); V, EV, surum = E["V"], E["EV"], E["surum"]
    kimlik = kosu_kimligi(A, surum, paketler, vsha); kimlik["faz"] = "1-vekil"
    pyol = panel_yol or os.path.join(A.cikti, "panel", f"k55_panel_{A.ornek or 'tam'}.pkl"); oyol = olay_yol or os.path.join(A.cikti, "K55_OLAYLAR.csv.gz"); syol = os.path.join(A.cikti, "K55_HUCRE_SONUC.csv")
    for y in (pyol, oyol, syol):
        if not os.path.exists(y):
            raise FileNotFoundError(f"girdi yok: {y} (önce faz0 ve faz1)")
    P = pd.read_pickle(pyol); O = pd.read_csv(oyol); O["tarih"] = pd.to_datetime(O.tarih); D = pd.read_csv(syol)
    kj = os.path.join(A.cikti, "K55_KOSU.json")
    if os.path.exists(kj):
        k0 = json.load(open(kj, encoding="utf-8"))
        if k0.get("evren_surum") and k0["evren_surum"] != surum:
            raise RuntimeError(f"panel başka evren sürümüyle kurulmuş ({k0['evren_surum'][:12]} ≠ {surum[:12]})")
    if A.ornek:
        sec = set(P.sembol.unique()); V = {s: d for s, d in V.items() if s in sec}; EV = EV[EV.sembol.isin(sec)].reset_index(drop=True)
    C = cy(); endeks = C.cy_endeks(C.CYAyar(veri=A.veri, cikti=A.cikti, pazarlar=("ABD",)), C.CY); ek_kur(V, EV, endeks); hucreleri_kur(DALLAR)
    secim = hucre_sec(D, hucreler)
    if any(h.startswith("D10") for h in secim):
        for kb, p in D10_BILESEN:
            if kb in HUCRELER and kb not in P:
                P[kb], _ = degisken_hesapla(P, V, HUCRELER[kb], p, kb)
    log.info("vekil kıyası: %d hücre %s; panel %d satır; kimlik %s", len(secim), secim, len(P), kimlik["kimlik"])
    T = vekil_kiyas(D, P, V, O, np.random.default_rng(A.tohum + 27), secim)
    T.to_csv(os.path.join(A.cikti, "K55_VEKIL.csv"), index=False); vekil_yaz(T, kimlik, A.cikti)
    with open(os.path.join(A.cikti, "K55_KOSU_VEKIL.json"), "w", encoding="utf-8") as f:
        json.dump({**kimlik, "hucreler": secim, "sure_dk": round((time.time() - t_bas) / 60, 1)}, f, ensure_ascii=False, indent=1, default=str)
    log.info("vekil kıyası bitti: %d hücre, VEKİL %d, %.1f dk", len(T), int(T.get("vekil", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if len(T) else 0, (time.time() - t_bas) / 60)
    return T
