# -*- coding: utf-8 -*-
"""
ÇÖL TANIM 2 v1.4 — Cemal'in çölünü kurala çevirir ve kendi işaretlediği çöllerle sınar
v1.4 (9 Eki 2026, Cemal'in kuralı kendi sözüyle): "EN DİP oluştuktan sonra mumlar küçük ve yukarı sürünür; Bollinger sürünmede sıkışır;
küçük mum TEPEDE olursa dağıtım habercisidir; haftalık desteklemeli." → K6 EN DİP: pencerenin dibi, öncesindeki dip_bakis barın da
en düşük kapanışı olmalı (tepe sıkışması = dağıtım, çöl değil). Bilgi: bb_rank_son (Bollinger genişliği son 100 bara göre yüzdelik,
küçük = sıkışık), hafta_egim_pct (haftalık kapanış eğimi %/hafta), hafta_govde_pct (haftalık medyan gövde).
v1.3 (9 Eki 2026, ikinci sınav): Cemal'in 12 çölünün 9'unda işaretlediği başlangıç = EN DÜŞÜK KAPANIŞ (dip_konum 0,00–0,07).
Yani onun "çöl"ü çanağın DİBİNDEN başlayıp sağ kol boyunca yavaş yükselen kısım; sol kol = sol bacak (çölden önce).
K2 artık DİP BAŞTA: en düşük kapanış pencerenin ilk %15'inde, sağ kol dipten ≥ kol_min yukarıda (yükseliş var).
K3 artık SÜRÜNME: bütün pencerenin eğimi egim_min..egim_max (%/gün; 12 çölde +0,06…+0,57, SUNTK +0,57).
v1.1 (9 Eki 2026, ilk sınav sonrası): 12 EVET / 3 HAYIR tablosunda en iyi ayıran K2 çıktı (HAYIR'ın hepsi taban altına yeni dip yapıyor,
EVET'lerin 9'u tabanın ÜSTÜNDE dip yapıyor = yükselen taban). K3 sınırı Cemal'in çöllerine göre genişletildi (+0,2…+0,6 %/gün sürünme),
K1/K4 sınırları 12 örneğin en genişine çekildi (artık ayırıcı değil, sadece sağlama). 'yukselen_taban' bilgi sütunu eklendi.
=====================================================================================
Eski col_segment "küçük gövdeli barlar + yükseklik ≤ 6 ATR" buluyor; ATR'yi segment ÖNCESİ 30 bardan alıyor, yön bakmıyor,
taban koruması yok. Bu yüzden çöküş molası (AGHOL), geniş çarşı (EGSER), yavaş yükseliş (GOODY) çöl sayıldı.

Burada her kural Cemal'in sözünden geliyor ve AYRI ölçülüyor; bir pencere için her kuralın geçti/kaldı sonucu görünür:
  K1 KÜÇÜK MUM     : medyan gövde / kapanış ≤ govde_pct  ve  medyan aralık / kapanış ≤ aralik_pct   (fiyata göre, ATR'ye değil)
  K2 DİP BAŞTA     : en düşük kapanış pencerenin ilk %dip_max'ında (çöl çanağın dibinden başlar), son 3 bar dipten ≥ kol_min yukarıda;
                     sol kol / taban genişliği / eğrilik bilgi
  K3 SÜRÜNME       : bütün pencerenin eğimi egim_min..egim_max %/gün (yavaş yükseliş; düz ya da aşağı = çöl değil, fırlama = çölün sonu)
  K4 BANT          : (en yüksek − en düşük) / en düşük ≤ bant_max ; uzunluk min_bar..max_bar
  K5 SOL BACAK     : çölden önceki sol_bacak_bar barda en az sol_bacak_min düşüş (0 = kapalı)
  K6 EN DİP        : pencerenin en düşük kapanışı, önceki dip_bakis barın en düşük kapanışının en fazla %dip_gercek_tol üstünde
                     (en dip burada; küçük mumlar tepede/ortada ise dağıtım, çöl değil)
  Bilgi (kural değil): doji oranı, sıkışma (son 5 bar aralığı / segment medyanı), hacim oranı, ATR_önce/ATR_içi (eski kodun şişme payı)

ct_olc(x)          : bir pencerenin bütün ölçüleri
ct_karar(olc, K)   : (geçti, kalan kurallar)
ct_bul(df, T, K)   : T'de biten, kuralların hepsini geçen EN UZUN pencere; sonra başlangıç o pencerenin en düşük kapanışına kırpılır (çöl dipten başlar)
ct_ogret(...)      : Cemal'in EVET listesi (kalibrasyon.CEMAL) + HAYIR listesi üzerinde: her örnek için ölçüler, hangi kural ayırıyor,
                     ct_bul başlangıcı Cemal'in başlangıcına kaç bar uzak → {K}/col_tanim2_ogret.csv + rapor

    exec(open(K + "/col_tanim2.py", encoding="utf-8").read())
    T = ct_ogret(K, VERI, CEMAL, HAYIR)             # CEMAL kalibrasyon.py'den; HAYIR = [(sembol, bas, son, not), ...]
"""
from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

CT_SURUM = "1.4"
_ct_log = logging.getLogger("col_tanim2")
if not _ct_log.handlers:
    _h = logging.StreamHandler(sys.stdout); _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s ct: %(message)s", "%H:%M:%S"))
    _ct_log.addHandler(_h); _ct_log.setLevel(logging.INFO)


@dataclass
class ColKural:
    min_bar: int = 10            # DAR çöl 10–25, BÜYÜK çöl 40–80 (Cemal); alt sınır 10
    max_bar: int = 120
    govde_pct: float = 0.020     # K1 medyan |C−O|/C ≤ %2   (v1.1: Cemal'in 12 çölünde en büyük 1,93)
    aralik_pct: float = 0.045    # K1 medyan (H−L)/C ≤ %4,5 (en büyük 4,50)
    dip_max: float = 0.15        # K2 DİP BAŞTA: en düşük kapanış pencerenin ilk %15'inde
    kol_min: float = 0.05        # K2 DİP BAŞTA: son 3 bar ortalaması dipten en az %5 yukarıda (12 çölde en az 8,5; AGHOL 4,1)
    taban_yakin: float = 0.03    # bilgi: dibin %3 yakınındaki kapanışlar "taban"
    egim_min: float = 0.05       # K3 SÜRÜNME: eğim ≥ +%0,05/gün (düz kutu çöl değil)
    egim_max: float = 1.00       # K3 SÜRÜNME: eğim ≤ +%1,0/gün
    bant_max: float = 0.65       # K4 (v1.1: SUNTK %62)
    dip_bakis: int = 120         # K6 EN DİP: önceki 120 bar (yaklaşık 6 ay) içinde daha düşük kapanış olmamalı
    dip_gercek_tol: float = 0.02 # K6 EN DİP: önceki en düşük kapanışın en fazla %2 üstünde
    sol_bacak_bar: int = 60      # K5 çöl öncesi pencere
    sol_bacak_min: float = 0.0   # K5 0 = kapalı (önce ölçelim)
    doji_esik: float = 0.15      # bilgi: |C−O|/(H−L) < 0.15 → doji


KURAL_ADI = {"K1": "küçük mum", "K2": "dip başta", "K3": "sürünme", "K4": "bant/uzunluk", "K5": "sol bacak", "K6": "en dip"}


# ---------------------------------------------------------------- ölçüler
def _ct_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    k = {c.lower(): c for c in df.columns}
    ad = {}
    for a, b in (("open", "O"), ("high", "H"), ("low", "L"), ("close", "C"), ("volume", "V")):
        if a in k:
            ad[k[a]] = b
        elif b in df.columns:
            ad[b] = b
    o = df.rename(columns=ad)
    if "V" not in o.columns:
        o = o.assign(V=np.nan)
    return o[["O", "H", "L", "C", "V"]].astype(float)


def ct_olc(x: pd.DataFrame, onceki: Optional[pd.DataFrame] = None, K: Optional[ColKural] = None) -> Dict[str, Any]:
    """Bir pencerenin ölçüleri. x = pencere barları (DatetimeIndex), onceki = pencere öncesi barlar (sol bacak, hacim, ATR_önce)."""
    K = K or ColKural(); s = _ct_ohlc(x); n = len(s)
    if n < 3:
        return {"uzunluk": n}
    O, H, L, C, V = (s[c].to_numpy(float) for c in "OHLCV")
    govde = np.abs(C - O) / C; aralik = (H - L) / C
    rng = np.maximum(H - L, 1e-12); doji = float((np.abs(C - O) / rng < K.doji_esik).mean())
    clv = float((((C - L) - (H - C)) / rng).mean())
    egim = float(np.polyfit(np.arange(n), C, 1)[0] / C.mean() * 100)                     # %/gün
    i_min = int(np.argmin(C)); c_min = float(C[i_min]); dip_konum = i_min / max(n - 1, 1)
    k3 = max(3, n // 3)
    sol_kol = (float(C[:3].mean()) / c_min - 1) * 100; sag_kol = (float(C[-3:].mean()) / c_min - 1) * 100
    taban_genislik = float((C <= c_min * (1 + K.taban_yakin)).mean())
    ilk_egim = float(np.polyfit(np.arange(k3), C[:k3], 1)[0] / C[:k3].mean() * 100)
    son_egim = float(np.polyfit(np.arange(k3), C[-k3:], 1)[0] / C[-k3:].mean() * 100)
    t = np.arange(n) / max(n - 1, 1); egri = np.polyfit(t, C / C.mean(), 2); egrilik = float(egri[0]) * 100       # + = U (çanak), − = ters U
    tahmin = np.polyval(egri, t); ss = float(((C / C.mean() - tahmin) ** 2).sum()); st = float(((C / C.mean() - (C / C.mean()).mean()) ** 2).sum())
    r2 = 1 - ss / st if st > 0 else 0.0
    en_dusuk = float(L.min()); en_yuksek = float(H.max())
    son5 = float(np.median(aralik[-5:])) if n >= 5 else np.nan; med_ar = float(np.median(aralik))
    o: Dict[str, Any] = {"uzunluk": n, "bas": str(s.index[0].date()), "son": str(s.index[-1].date()),
                         "govde_pct": float(np.median(govde)) * 100, "aralik_pct": med_ar * 100, "doji": doji, "clv": clv,
                         "egim_pct_gun": egim, "bant_pct": (en_yuksek / en_dusuk - 1) * 100, "taban": en_dusuk, "tavan": float(np.maximum(O, C).max()),
                         "dip_konum": dip_konum, "sol_kol_pct": sol_kol, "sag_kol_pct": sag_kol, "taban_genislik": taban_genislik,
                         "egrilik": egrilik, "u_r2": r2, "ilk_egim_pct_gun": ilk_egim, "son_egim_pct_gun": son_egim,
                         "sikisma": son5 / med_ar if med_ar > 0 else np.nan}
    if onceki is not None and len(onceki):
        p = _ct_ohlc(onceki)
        sb = p.tail(K.sol_bacak_bar)
        o["sol_bacak_pct"] = (float(sb["H"].max()) / float(C[0]) - 1) * 100 if len(sb) else np.nan         # öncesindeki zirveden çöl başına düşüş
        o["atr_once_ici"] = float(((p["H"] - p["L"]).tail(30).mean()) / max((H - L).mean(), 1e-12)) if len(p) >= 8 else np.nan
        pv = p["V"].tail(60).dropna(); vv = V[np.isfinite(V)]
        o["hacim_orani"] = float(vv.mean() / pv.median()) if len(pv) and len(vv) and pv.median() > 0 else np.nan
        pc = p["C"].tail(K.dip_bakis); o["dip_gercek_pct"] = (c_min / float(pc.min()) - 1) * 100 if len(pc) >= 20 else np.nan
        # Bollinger sıkışması: pencere sonundaki BB(20) genişliği, son 100 barın yüzdeliği (küçük = sıkışık)
        tum = pd.concat([p["C"], s["C"]]); m20 = tum.rolling(20).mean(); sd20 = tum.rolling(20).std(ddof=0); bbw = (4 * sd20 / m20.replace(0, np.nan))
        ref = bbw.tail(100).dropna(); o["bb_rank_son"] = float((ref <= bbw.iloc[-1]).mean()) if len(ref) > 20 and np.isfinite(bbw.iloc[-1]) else np.nan
        bw = bbw.tail(n).dropna(); o["bb_rank_min"] = float((ref <= bw.min()).mean()) if len(ref) > 20 and len(bw) else np.nan
        # haftalık destek: pencere haftalarının kapanış eğimi ve gövde büyüklüğü
        hf = s.resample("W-FRI").agg({"O": "first", "H": "max", "L": "min", "C": "last"}).dropna()
        if len(hf) >= 3:
            hc = hf["C"].to_numpy(float); o["hafta_egim_pct"] = float(np.polyfit(np.arange(len(hc)), hc, 1)[0] / hc.mean() * 100)
            o["hafta_govde_pct"] = float(np.median(np.abs(hf["C"] - hf["O"]) / hf["C"])) * 100
        else:
            o["hafta_egim_pct"] = np.nan; o["hafta_govde_pct"] = np.nan
    else:
        for k in ("sol_bacak_pct", "atr_once_ici", "hacim_orani", "dip_gercek_pct", "bb_rank_son", "bb_rank_min", "hafta_egim_pct", "hafta_govde_pct"):
            o[k] = np.nan
    return o


def ct_karar(o: Dict[str, Any], K: Optional[ColKural] = None) -> Tuple[bool, List[str]]:
    K = K or ColKural(); kalan = []
    if o.get("uzunluk", 0) < 3:
        return False, ["K4"]
    if not (o["govde_pct"] <= K.govde_pct * 100 and o["aralik_pct"] <= K.aralik_pct * 100):
        kalan.append("K1")
    if not (o["dip_konum"] <= K.dip_max and o["sag_kol_pct"] >= K.kol_min * 100):
        kalan.append("K2")
    if not (K.egim_min <= o["egim_pct_gun"] <= K.egim_max):
        kalan.append("K3")
    if not (K.min_bar <= o["uzunluk"] <= K.max_bar and o["bant_pct"] <= K.bant_max * 100):
        kalan.append("K4")
    if K.sol_bacak_min > 0 and not (np.isfinite(o.get("sol_bacak_pct", np.nan)) and o["sol_bacak_pct"] >= K.sol_bacak_min * 100):
        kalan.append("K5")
    dg = o.get("dip_gercek_pct", np.nan)
    if np.isfinite(dg) and dg > K.dip_gercek_tol * 100:
        kalan.append("K6")
    return (not kalan), kalan


# ---------------------------------------------------------------- bulucu
def ct_bul(df: pd.DataFrame, T: Any = None, K: Optional[ColKural] = None) -> Optional[Dict[str, Any]]:
    """T'de biten, bütün kuralları geçen EN UZUN pencere. Yoksa None. Geleceğe bakmaz (df T'de kesilir)."""
    K = K or ColKural()
    x = df[df.index <= pd.Timestamp(T)] if T is not None else df
    n = len(x)
    if n < K.min_bar + 8:
        return None
    for uz in range(min(K.max_bar, n - 1), K.min_bar - 1, -1):
        geri = max(K.sol_bacak_bar, K.dip_bakis, 120)
        seg = x.iloc[n - uz:]; onc = x.iloc[max(0, n - uz - geri): n - uz]
        o = ct_olc(seg, onc, K); ok, kalan = ct_karar(o, K)
        if ok:
            i_min = int(np.argmin(seg["Close"].to_numpy(float) if "Close" in seg.columns else _ct_ohlc(seg)["C"].to_numpy()))
            if i_min > 0:                                                    # çöl dipten başlar: pencereyi en düşük kapanışa kırp
                seg2 = seg.iloc[i_min:]; onc2 = x.iloc[max(0, n - uz + i_min - geri): n - uz + i_min]
                o2 = ct_olc(seg2, onc2, K); ok2, _ = ct_karar(o2, K)
                if ok2:
                    o = o2
            o["gecti"] = True; return o
    return None


# ---------------------------------------------------------------- öğretme tablosu
def _ct_pencere(veri: Dict[str, pd.DataFrame], sembol: str, bas: Any, son: Any) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    k = sembol if sembol in veri else next((z for z in veri if str(z).split(".")[0] == sembol), None)
    if k is None:
        return None
    df = veri[k]; b, s = pd.Timestamp(bas), pd.Timestamp(son)
    seg = df[(df.index >= b) & (df.index <= s)]
    if len(seg) < 3:
        return None
    return df, seg, df[df.index < b]


def ct_ogret(K_yol: str, VERI: Any, evet: Sequence[Tuple[str, str, str, str]], hayir: Sequence[Tuple[str, str, str, str]] = (),
             K: Optional[ColKural] = None, ad: str = "col_tanim2_ogret") -> pd.DataFrame:
    """EVET (Cemal'in çölleri) ve HAYIR (çöl olmayanlar) pencerelerinde ölçüler + kural kararı + ct_bul'un bulduğu başlangıç."""
    K = K or ColKural(); veri = VERI["veri"] if isinstance(VERI, dict) and isinstance(VERI.get("veri"), dict) else VERI
    R = []
    for etiket, liste in (("EVET", evet), ("HAYIR", hayir)):
        for s, bas, son, nt in liste:
            p = _ct_pencere(veri, s, bas, son)
            if p is None:
                R.append({"etiket": etiket, "sembol": s, "cemal_bas": bas, "cemal_son": son, "durum": "VERİDE YOK"}); continue
            df, seg, onc = p
            o = ct_olc(seg, onc, K); ok, kalan = ct_karar(o, K)
            b = ct_bul(df, son, K)
            fark = None
            if b is not None:
                fark = int(df.index.get_indexer([pd.Timestamp(b["bas"])], method="nearest")[0] - df.index.get_indexer([pd.Timestamp(bas)], method="nearest")[0])
            R.append({"etiket": etiket, "sembol": s, "cemal_bas": bas, "cemal_son": son, "not": nt, "durum": "ok",
                      **{k: (round(v, 3) if isinstance(v, float) else v) for k, v in o.items() if k not in ("bas", "son")},
                      "kural_gecti": ok, "kalan": "+".join(kalan), "bul_bas": b["bas"] if b else None, "bul_uzunluk": b["uzunluk"] if b else 0,
                      "bas_fark": fark})
    T = pd.DataFrame(R)
    yol = os.path.join(K_yol, f"{ad}.csv"); T.to_csv(yol, index=False)
    rapor = ct_rapor(T, K); print(rapor)
    with open(os.path.join(K_yol, f"{ad}.txt"), "w", encoding="utf-8") as f:
        f.write(rapor + "\n")
    return T


def ct_rapor(T: pd.DataFrame, K: ColKural) -> str:
    s = [f"ÇÖL TANIM 2 v{CT_SURUM} — kural: {asdict(K)}"]
    ok = T[T["durum"] == "ok"].copy() if "durum" in T.columns else T.copy()
    if ok.empty:
        return "\n".join(s + ["örnek yok"])
    ok["kural_gecti"] = ok["kural_gecti"].astype(bool); ok["kalan"] = ok["kalan"].fillna("").astype(str)
    kol = ["etiket", "sembol", "cemal_bas", "cemal_son", "uzunluk", "govde_pct", "aralik_pct", "doji", "egim_pct_gun", "bant_pct", "dip_konum", "sag_kol_pct", "dip_gercek_pct", "bb_rank_son", "bb_rank_min", "hafta_egim_pct", "hafta_govde_pct", "taban_genislik",
           "sol_bacak_pct", "atr_once_ici", "sikisma", "kural_gecti", "kalan", "bul_bas", "bas_fark"]
    kol = [c for c in kol if c in ok.columns]
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", None)
    s.append(ok[kol].to_string(index=False))
    for etiket in ("EVET", "HAYIR"):
        g = ok[ok.etiket == etiket]
        if len(g):
            s.append(f"{etiket}: {int(g.kural_gecti.sum())}/{len(g)} kuralı geçti" + (f" | kalan kurallar: {g[~g.kural_gecti].kalan.value_counts().to_dict()}" if (~g.kural_gecti).any() else ""))
    e = ok[(ok.etiket == "EVET") & ok.bas_fark.notna()]
    if len(e):
        s.append(f"ct_bul başlangıcı Cemal'e göre: medyan {e.bas_fark.median():+.0f} bar, |fark| ort {e.bas_fark.abs().mean():.1f}, ≤5 bar isabet {int((e.bas_fark.abs() <= 5).sum())}/{len(e)}  (+ = kod geç başladı, − = erken)")
    # hangi kural ayırıyor
    ayir = []
    for k in ("K1", "K2", "K3", "K4", "K5", "K6"):
        ev = ok[ok.etiket == "EVET"]; ha = ok[ok.etiket == "HAYIR"]
        if len(ev) and len(ha):
            ev_g = (~ev.kalan.str.contains(k)).mean(); ha_g = (~ha.kalan.str.contains(k)).mean()
            ayir.append(f"{k} {KURAL_ADI[k]}: EVET geçen %{100 * ev_g:.0f} | HAYIR geçen %{100 * ha_g:.0f}")
    if ayir:
        s.append("kural bazında ayırma gücü: " + " || ".join(ayir))
    return "\n".join(s)
