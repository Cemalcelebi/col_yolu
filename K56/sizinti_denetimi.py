"""K56 İÇ → BAĞIMSIZ dolaylı erişim denetimi (ONKAYIT_K56 v1.3-SIZ; Cemal, 31 Eki: 'İç doğrulama sırasında bağımsız döneme dolaylı erişim olmadığı
doğrulanacak').

T0 (yeniden üretim): K55 evreni, panel ve olay tablosu K55 koduyla baştan kurulur; kilitli panel / olay tablosuyla birebir aynı olmalı (yoksa T1 farkı
sızıntı sanılır).
T1 (aynı evren, kesik fiyat): her fiyat serisi ve endeks kesim gününde (İÇ: 2023-12-31) kesilir; panel / olay / D10 bileşenleri yeniden kurulur; İÇ motoru
(faz1_yerel.calistir, B3 dahil) kesik SEC başvuru özetiyle koşar (T1b). S, H, B3 ve olay oranı geçerli İÇ koşusuyla (SON.json) TAM EŞİT olmalı (tolerans 0;
NaN = NaN; yalnız süre sütunu hariç). Bileşim ayrıca tam başvuru özetiyle (T1a) hesaplanır: T1a bileşimi birebir, T1b bileşimi yalnız sec_var (başvuru
geçmişi var mı) yüzünden farklı olabilir — farkın büyüklüğü kaydedilir.
T2 (evren de kesik): evren üyeliği kesik veriden yeniden kurulur (K55 evren_insa; >= 320 gün; ALIVE_SINIR kesimden bir ay öncesine çekilir); T2a yalnız bu,
T2b ayrıca evrene kesimden sonra giren K34 sembollerini atar. K54 sınıfı (SEC dış bilgisi) aynen. T1b'ye karşı karşılaştırılır; fark, K55 evren tasarımının
(üyelik tam seriden) İÇ sonuçlarına etkisidir; ihlal değil, ölçülür ve raporlanır. Görünmeyen sınırlamalar: hayatta kalma (evren 2026'da işlem görenler +
K34), 2026 sürümü bölünme / temettü düzeltmesi, güncel sektör ve CIK etiketleri (raporda beyan).
"""
from __future__ import annotations

import os
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd

from .ortak import K56Ayar, log

KESIM = {"IC_DOGRULAMA": "2023-12-31", "KESIF": "2021-12-31"}
TOL_AYR = 1e-12   # v1.3-c: T1 ayrışma (İÇ) karşılaştırmasında sayısal tolerans (kayan nokta toplama sırası; karar eşiklerinin çok altında); metin / sınıf birebir


def _kes(d: pd.DataFrame, kesim: pd.Timestamp) -> pd.DataFrame:
    return d[d.index <= kesim]


def sec_kes(J: Dict[str, Any], kesim: pd.Timestamp) -> Dict[str, Any]:
    """SEC başvuru özetinden kesim sonrası başvuruları atar (tarih / form / madde hizalı)."""
    from .kurumsal_olaylar import _liste
    k = str(kesim.date()); out = {}
    for c, v in J.items():
        t = _liste(v.get("date", "[]")); f = _liste(v.get("form", "[]")); it = _liste(v.get("items", "[]")) or [""] * len(f)
        keep = [i for i, x in enumerate(t) if str(x) <= k]
        out[c] = {**v, "date": [t[i] for i in keep], "form": [f[i] for i in keep], "items": [it[i] for i in keep]}
    return out


def _panel_olay(V, EV, A55, endeks) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    from K55.faz1 import D10_BILESEN, DALLAR, ek_kur, hucreleri_kur
    from K55.hucre import degisken_hesapla
    from K55.hucreler import HUCRELER
    from K55.olay_tanimlari import olaylar
    from K55.panel import panel_kur
    P, likit_map, bilgi = panel_kur(V, EV, A55, endeks); O, _ = olaylar(V, likit_map)
    ek_kur(V, EV, endeks); hucreleri_kur(DALLAR)
    for kb, p in D10_BILESEN:
        if kb in HUCRELER and kb not in P:
            P[kb], _ = degisken_hesapla(P, V, HUCRELER[kb], p, kb)
    return P, O, bilgi


def _a55(A: K56Ayar, isci: int):
    from K55.ortak import K55Ayar
    A55 = K55Ayar(veri=A.veri, cikti=os.path.join(A.onbellek, "sizinti"), k54=A.abd, isci=isci); os.makedirs(A55.cikti, exist_ok=True); return A55


def t0_yeniden_uretim(A: K56Ayar, panel_yol: str, olay_yol: str, isci: int = 3) -> Dict[str, Any]:
    """K55 evren / panel / olay baştan; kilitli panel (pickle) ve olay tablosuyla karşılaştırma (DataFrame eşitliği, NaN = NaN)."""
    from K55 import evren as KE
    from K55.olay_tanimlari import olaylar
    from K55.ortak import cy, veri_sha
    from K55.panel import panel_kur
    A55 = _a55(A, isci); C = cy(); E = KE.evren_kur(A55, veri_sha(A55), network=False)
    endeks = C.cy_endeks(C.CYAyar(veri=A55.veri, cikti=A55.cikti, pazarlar=("ABD",)), C.CY)
    P, likit_map, _ = panel_kur(E["V"], E["EV"], A55, endeks); O, _ = olaylar(E["V"], likit_map)
    Pk = pd.read_pickle(panel_yol); Ok = pd.read_csv(olay_yol, parse_dates=["tarih", "bitis"])
    ortak_kol = [c for c in Pk.columns if c in P.columns]; eksik = sorted(set(Pk.columns) ^ set(P.columns))
    p_esit = len(P) == len(Pk) and all(_esit_seri(P[c], Pk[c]) for c in ortak_kol)
    Ok2 = O.copy(); Ok2["tarih"] = pd.to_datetime(Ok2.tarih); Ok2["bitis"] = pd.to_datetime(Ok2.bitis)
    o_esit = len(O) == len(Ok) and all(_esit_seri(Ok2[c].reset_index(drop=True), Ok[c].reset_index(drop=True), tol=1e-9) for c in Ok.columns if c in Ok2.columns)
    out = {"evren_surum": E["surum"], "panel_satir": len(P), "panel_satir_kilitli": len(Pk), "panel_esit": bool(p_esit), "panel_sutun_farki": eksik,
           "olay": len(O), "olay_kilitli": len(Ok), "olay_esit": bool(o_esit)}
    log.info("T0: %s", out); return out


def _esit_seri(a: pd.Series, b: pd.Series, tol: float = 0.0) -> bool:
    """NaN / NaT farkında eşitlik: tarih sütunları ns'ye çevrilip karşılaştırılır (birim ns / us farkı eşitsizlik değildir); sayısal sütunlar tol içinde
    (panel pickle'ı için 0; CSV'den okunan olay tablosu için 1e-9: CSV ondalık hassasiyeti, v1.3-b); öteki sütunlar metin olarak."""
    a = a.reset_index(drop=True); b = b.reset_index(drop=True)
    if len(a) != len(b):
        return False
    if pd.api.types.is_datetime64_any_dtype(a) or pd.api.types.is_datetime64_any_dtype(b):
        x = pd.to_datetime(a).to_numpy("datetime64[ns]"); y = pd.to_datetime(b).to_numpy("datetime64[ns]")
        return bool(((x == y) | (pd.isna(x) & pd.isna(y))).all())
    if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):
        x, y = a.to_numpy(float), b.to_numpy(float)
        return bool(((np.abs(x - y) <= tol) | (x == y) | (np.isnan(x) & np.isnan(y))).all())
    return bool((a.astype(str).to_numpy() == b.astype(str).to_numpy()).all())


def kesik_veri(A: K56Ayar, donem: str = "IC_DOGRULAMA", evren_kesik: str = "", isci: int = 3) -> Dict[str, Any]:
    """T1 (evren_kesik='') / T2a ('a') / T2b ('b') için P / V / O / EV / endeks / J (kesik) + J_tam (faz1_yerel.calistir veri sözlüğü)."""
    from K55 import evren as KE
    from K55.ortak import cy, veri_sha
    from .kurumsal_olaylar import sec_ozet_yukle
    kes = pd.Timestamp(KESIM[donem]); A55 = _a55(A, isci); C = cy()
    if not evren_kesik:
        E = KE.evren_kur(A55, veri_sha(A55), network=False); V = {s: _kes(d, kes) for s, d in E["V"].items()}; V = {s: d for s, d in V.items() if len(d)}
        EV = E["EV"][E["EV"].sembol.isin(V)].copy(); surum = "T1:" + E["surum"]
    else:
        SD, ES, _ = KE._k54_oku(A55); fon_disi = set(pd.read_csv(os.path.join(KE.KOK, "evren_disi_ABD.csv")).sembol.map(KE.sembol_normalize))
        Ac = C.CYAyar(veri=A55.veri, cikti=A55.cikti, pazarlar=("ABD",), is_parcacigi=1); eski = C.cy_tiingo_indir
        try:
            C.cy_tiingo_indir = lambda *a, **k: 0
            with KE.ag_kapali():
                Vs, EV_ham = C.cy_veri_yukle(Ac, C.CY)
        finally:
            C.cy_tiingo_indir = eski
        V_ham = {s: _kes(d, kes) for s, d in Vs["ABD"].items()}; V_ham = {s: d for s, d in V_ham.items() if len(d) >= KE.YUKLEYICI_MIN_GUN}     # yükleyici eşiği kesik seride
        EV_ham = EV_ham[(EV_ham.pazar == "ABD") & EV_ham.sembol.isin(V_ham)].copy()
        if evren_kesik == "b":
            EV_ham = EV_ham[pd.to_datetime(EV_ham.evren_bas) <= kes]
        V_ham = {s: d for s, d in V_ham.items() if s in set(EV_ham.sembol)}
        kisa, eksik = KE._ham_kisa_ve_eksik(A55, {KE.sembol_normalize(s): 1 for s in V_ham}, fon_disi)
        eski_alive = KE.ALIVE_SINIR
        try:
            KE.ALIVE_SINIR = str((kes - pd.DateOffset(months=1)).date())                 # kesik seride 'erken bitti' anlamı korunur
            R = KE.evren_insa(V_ham, EV_ham, SD, ES, fon_disi, kisa, eksik)
        finally:
            KE.ALIVE_SINIR = eski_alive
        sek = C.cy_sektor(Ac, R["EV"]); R["EV"]["sektor"] = R["EV"].sembol.map(sek).fillna("bilinmiyor")
        V, EV, surum = R["V"], R["EV"], f"T2{evren_kesik}:kesik-evren"
    endeks = C.cy_endeks(C.CYAyar(veri=A55.veri, cikti=A55.cikti, pazarlar=("ABD",)), C.CY); endeks = endeks[endeks.index <= kes]
    P, O, bilgi = _panel_olay(V, EV, A55, endeks); J_tam = sec_ozet_yukle(A); J = sec_kes(J_tam, kes)
    log.info("%s kesik veri (%s): %d sembol, panel %d satır, olay %s", surum.split(":")[0], kes.date(), len(V), len(P), O.groupby("donem").size().to_dict())
    return {"P": P, "V": V, "O": O, "EV": EV, "endeks": endeks, "evren_surum": surum, "J": J, "J_tam": J_tam, "panel_bilgi": bilgi}


def karsilastir(ref: Dict[str, pd.DataFrame], yeni: Dict[str, pd.DataFrame], tol: float = 0.0) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """S (anahtar hücre|varyant|ufuk), H (hücre), B3 (hücre|varyant), Bl (ufuk|ölçü): bütün sütunlar karşılaştırılır (süre hariç); sayısal fark > tol ya da
    metin farkı ya da eşleşmeyen satır = fark. Dönüş: fark tablosu (yalnız farklı hücreler) ve özet."""
    anahtar = {"S": ["hucre", "varyant", "ufuk"], "H": ["hucre"], "B3": ["hucre", "varyant"], "Bl": ["ufuk", "olcu"]}; atla = {"sure_sn"}; rows = []; ozet = {}
    for t, kk_ in anahtar.items():
        a, b = ref.get(t, pd.DataFrame()), yeni.get(t, pd.DataFrame())
        if not len(a) and not len(b):
            continue
        M = a.merge(b, on=kk_, how="outer", suffixes=("_ref", "_yeni"), indicator=True); n_fark = 0
        kol = sorted({c[:-4] for c in M.columns if c.endswith("_ref")} - atla)
        for c in sorted((set(a.columns) ^ set(b.columns)) - atla - set(kk_)):          # tek tarafta olan sütun = fark
            rows.append({"tablo": t, "anahtar": "(sütun)", "sutun": c, "ref": c in a.columns, "yeni": c in b.columns})
        for r in M.to_dict("records"):
            key = "|".join(str(r[c]) for c in kk_)
            if r["_merge"] != "both":
                rows.append({"tablo": t, "anahtar": key, "sutun": "(satır)", "ref": r["_merge"], "yeni": ""}); n_fark += 1; continue
            for c in kol:
                va, vb = r.get(f"{c}_ref"), r.get(f"{c}_yeni")
                if isinstance(va, (int, float, np.integer, np.floating)) and isinstance(vb, (int, float, np.integer, np.floating)) and not isinstance(va, bool):
                    if (pd.isna(va) and pd.isna(vb)) or (pd.notna(va) and pd.notna(vb) and abs(float(va) - float(vb)) <= tol):
                        continue
                elif str(va) == str(vb) or (pd.isna(va) if not isinstance(va, (list, dict)) else False) and (pd.isna(vb) if not isinstance(vb, (list, dict)) else False):
                    continue
                rows.append({"tablo": t, "anahtar": key, "sutun": c, "ref": va, "yeni": vb}); n_fark += 1
        ozet[t] = {"satir_ref": int(len(a)), "satir_yeni": int(len(b)), "fark_hucre": int(n_fark + len((set(a.columns) ^ set(b.columns)) - atla - set(kk_)))}
    F = pd.DataFrame(rows, columns=["tablo", "anahtar", "sutun", "ref", "yeni"])
    ozet["birebir"] = {t: v["fark_hucre"] == 0 for t, v in ozet.items() if isinstance(v, dict)}
    return F, ozet


def ayr_karsilastir(ref: pd.DataFrame, yeni: pd.DataFrame, kimlik_tol: float) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """v1.3-c: T1 ayrışma (İÇ) satırları AYR koşusuyla (aynı tohum etiketi). kimlik_fark (E1 − E2 + Cov(L, f) / ort L: cebirsel özdeşlik kalıntısı, ~1e-16)
    değer olarak değil özdeşlik olarak karşılaştırılır: iki tarafta da NaN ya da |.| <= kimlik_tol. Öteki sayısal sütunlar TOL_AYR içinde, metin / sınıf
    sütunları birebir, tek tarafta olan sütun ya da satır fark. Dönüş: fark tablosu, özet (birebir, kimlik özdeşliği, en büyük sayısal fark)."""
    at = ["etiket", "sure_sn", "kimlik_fark"]; kk_ = ["hucre", "varyant", "ufuk"]
    F, z = karsilastir({"S": ref.drop(columns=at, errors="ignore")}, {"S": yeni.drop(columns=at, errors="ignore")}, tol=TOL_AYR)
    M = ref.reindex(columns=kk_ + ["kimlik_fark"]).merge(yeni.reindex(columns=kk_ + ["kimlik_fark"]), on=kk_, how="outer", suffixes=("_ref", "_yeni"))
    a, b = M.kimlik_fark_ref.to_numpy(float), M.kimlik_fark_yeni.to_numpy(float); ab = np.r_[a, b]
    ok = (np.isnan(a) & np.isnan(b)) | ((np.abs(a) <= kimlik_tol) & (np.abs(b) <= kimlik_tol))
    z["kimlik_ozdeslik"] = {"tutar": bool(ok.all()), "bozulan": int((~ok).sum()), "en_buyuk_mutlak": float(np.nanmax(np.abs(ab))) if np.isfinite(ab).any() else 0.0}
    M2 = ref.drop(columns=at, errors="ignore").merge(yeni.drop(columns=at, errors="ignore"), on=kk_, how="inner", suffixes=("_ref", "_yeni")); en = 0.0
    for c in [c[:-4] for c in M2.columns if c.endswith("_ref")]:
        x, y = M2[f"{c}_ref"], M2[f"{c}_yeni"]
        if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y) and not pd.api.types.is_bool_dtype(x):
            d = np.abs(x.to_numpy(float) - y.to_numpy(float)); en = max(en, float(np.nanmax(d)) if np.isfinite(d).any() else 0.0)
    z["en_buyuk_sayisal_fark"] = en; z["birebir"]["S"] = bool(z["birebir"].get("S") and ok.all())
    return F, z
