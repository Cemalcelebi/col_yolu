"""K55 veri kalitesi denetimi (Cemal'in 8 maddelik talimatı, 30 Ekim 2026). YALNIZ denetim ve raporlama: veri silinmez, düzeltilmez; denetim için
normalize edilmiş KOPYA kullanılır, orijinal seri değişmez. Her kalite sorunu ayrı sütundur; "eksiksiz" tek bayrağı yoktur. Üç sınıf ayrılır:
VERİ HATASI (OHLCV ihlali, yinelenen işlem günü, sırasız, NaN / inf / sıfır / negatif fiyat, negatif hacim, takvim dışı satır),
VERİ YETERSİZLİĞİ (fiyat yok, boş seri, kısa seri, ciddi boşluk, eksik hacim, özellik / sonuç penceresi yetersiz),
OLAĞAN PİYASA DAVRANIŞI (%100 üstü getiri, sert haber hareketi; bilgi). Bölünme benzeri hareket: kesin (sağlayıcı kurumsal işlem verisiyle),
muhtemel (oran bölünme oranına yakın, hacim ters), açıklanamayan sıçrama, sert haber hareketi; kurumsal işlem verisi yoksa KESİN denmez.

Girdi: V (sembol -> OHLCV; bölünme + temettü düzeltmeli seriler: V_ABD / K34 Yahoo auto_adjust, Tiingo adj), EV (evren: sembol, kaynak, sinif,
alt, seri_sonu, kesim, cik, sec_ad, sektor, seri_erken, ...), isteğe bağlı O (olay tablosu) ve kurumsal (sembol -> bölünme tarih / oran tablosu).
Çıktı: sembol başına tablo (K55_VERI_KALITESI.csv) + özet sözlüğü (K55_VERI_KAPSAMI.md için). ABD işlem takvimi: NYSE kuralları (tatiller
eksik gün sayılmaz; takvim dışı satır ayrı sayılır).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from pandas.tseries.holiday import AbstractHolidayCalendar, GoodFriday, Holiday, USLaborDay, USMartinLutherKingJr, USMemorialDay, USPresidentsDay, USThanksgivingDay, nearest_workday

from .ortak import DONEM, MIN_GUN, OLAY, donem_etiketi
from .evren import bool_cevir, sembol_normalize

ESIK = {"ciddi_bosluk_gun": 5, "getiri_anormal": 1.0, "sicrama_log": np.log(1.8), "bolunme_oran_tol": 0.03, "hacim_sicrama_kat": 3.0, "sifir_hacim_pay": 0.20, "ozellik_gun": MIN_GUN}
BOLUNME_ORANLARI = [k for k in (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 40, 50)] + [1.5, 2.5] + [1 / k for k in (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 40, 50)] + [1 / 1.5, 1 / 2.5]
OHLCV = ("Open", "High", "Low", "Close", "Volume")
HATA_SUTUN = ("sirasiz", "yinelenen_islem_gunu", "takvim_disi_satir", "nan_fiyat", "inf_fiyat", "sifir_negatif_fiyat", "negatif_hacim", "ohlc_high_dusuk", "ohlc_low_yuksek", "ohlc_high_low", "sutun_eksik", "tur_hatasi")
YETERSIZ_SUTUN = ("fiyat_yok", "bos_seri", "kisa_seri_320", "ciddi_bosluk_sayi", "eksik_hacim_pay_yuksek", "ozellik_yetersiz", "sonuc_Y60_yetersiz")


# ---------------------------------------------------------------- ABD işlem takvimi (NYSE kuralları; dış kütüphane yok)
def _nyse_yilbasi(dt):
    """NYSE: 1 Ocak cumartesiye gelirse o yıl yılbaşı tatili yoktur (cuma ve pazartesi açık, ör. 2021-12-31 ve 2022-01-03); pazara gelirse pazartesi tatil."""
    if dt.weekday() == 5:
        return dt                              # cumartesi kalır; hafta sonu olduğu için takvimden zaten düşer (tatil etkisi yok)
    if dt.weekday() == 6:
        return dt + pd.Timedelta(days=1)
    return dt


class _NYSE(AbstractHolidayCalendar):
    rules = [Holiday("Yılbaşı", month=1, day=1, observance=_nyse_yilbasi), USMartinLutherKingJr, USPresidentsDay, GoodFriday, USMemorialDay,
             Holiday("Juneteenth", month=6, day=19, start_date="2022-06-19", observance=nearest_workday), Holiday("Bağımsızlık", month=7, day=4, observance=nearest_workday),
             USLaborDay, USThanksgivingDay, Holiday("Noel", month=12, day=25, observance=nearest_workday)]


OZEL_KAPANIS = pd.to_datetime(["2012-10-29", "2012-10-30", "2018-12-05", "2025-01-09"])     # Sandy, Bush, Carter cenazeleri


def abd_islem_gunleri(bas: Any, son: Any) -> pd.DatetimeIndex:
    """NYSE işlem günleri (iş günleri − tatiller − özel kapanışlar). 2012-2026 kuralları; 1 Ocak cumartesi istisnası uygulanır."""
    bas = pd.Timestamp(bas).normalize(); son = pd.Timestamp(son).normalize(); bd = pd.bdate_range(bas, son)
    tat = _NYSE().holidays(bas - pd.Timedelta(days=7), son + pd.Timedelta(days=7))
    tat = pd.DatetimeIndex([t for t in tat if t.weekday() < 5])        # yılbaşı cumartesi kaydırması hafta içine düşmez
    return bd.difference(tat).difference(OZEL_KAPANIS)


# ---------------------------------------------------------------- tek seri denetimi (saf; orijinal değişmez)
def _normalize_kopya(d: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Denetim kopyası: zaman damgası işlem gününe indirgenir (saat dilimi -> yerel gün), sıralama kontrolü ve sıralı kopya. Orijinal d değişmez."""
    k = d.copy(); idx = pd.DatetimeIndex(k.index); tzli = idx.tz is not None
    if tzli:
        idx = idx.tz_convert("America/New_York").tz_localize(None)
    idx = idx.normalize(); k.index = idx
    bilgi = {"saat_dilimli": bool(tzli), "sirasiz": int(not idx.is_monotonic_increasing), "yinelenen_islem_gunu": int(idx.duplicated().sum())}
    k = k.sort_index(kind="stable")
    return k, bilgi


def _sutun_tur(d: pd.DataFrame) -> Dict[str, Any]:
    eksik = [c for c in OHLCV if c not in d.columns]; tur = []
    for c in OHLCV:
        if c in d.columns and not pd.api.types.is_numeric_dtype(d[c]):
            tur.append(c)
    return {"sutun_eksik": len(eksik), "sutun_eksik_liste": ";".join(eksik), "tur_hatasi": len(tur), "tur_hatasi_liste": ";".join(tur)}


def _ohlcv_denetim(k: pd.DataFrame) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    F = k[["Open", "High", "Low", "Close"]].apply(pd.to_numeric, errors="coerce"); V = pd.to_numeric(k["Volume"], errors="coerce")
    out["nan_fiyat"] = int(F.isna().any(axis=1).sum()); out["inf_fiyat"] = int(np.isinf(F.to_numpy(float)).any(axis=1).sum())
    Ff = F.replace([np.inf, -np.inf], np.nan); out["sifir_negatif_fiyat"] = int((Ff <= 0).any(axis=1).sum())
    out["negatif_hacim"] = int((V < 0).sum()); out["eksik_hacim_sayi"] = int(V.isna().sum()); out["eksik_hacim_pay"] = float(V.isna().mean()) if len(V) else np.nan
    out["sifir_hacim_sayi"] = int((V == 0).sum()); out["sifir_hacim_pay"] = float((V == 0).sum() / V.notna().sum()) if V.notna().sum() else np.nan
    ok = Ff.notna().all(axis=1) & (Ff > 0).all(axis=1)
    H, L, O, C = Ff.High[ok], Ff.Low[ok], Ff.Open[ok], Ff.Close[ok]; tol = 1e-6
    out["ohlc_high_dusuk"] = int(((H < O * (1 - tol)) | (H < C * (1 - tol))).sum()); out["ohlc_low_yuksek"] = int(((L > O * (1 + tol)) | (L > C * (1 + tol))).sum()); out["ohlc_high_low"] = int((H < L * (1 - tol)).sum())
    return out


def _takvim_denetim(k: pd.DataFrame) -> Dict[str, Any]:
    idx = pd.DatetimeIndex(k.index.unique()); out: Dict[str, Any] = {}
    if not len(idx):
        return {"eksik_islem_gunu": 0, "bosluk_sayi": 0, "en_uzun_bosluk": 0, "ciddi_bosluk_sayi": 0, "bosluk_tarihleri": "", "takvim_disi_satir": 0}
    tak = abd_islem_gunleri(idx[0], idx[-1]); eksik = tak.difference(idx); disi = idx.difference(tak)
    out["eksik_islem_gunu"] = int(len(eksik)); out["takvim_disi_satir"] = int(len(disi)); out["takvim_disi_tarihleri"] = ";".join(str(t.date()) for t in disi[:5])
    bos = []
    if len(eksik):
        pos = tak.get_indexer(eksik); kir = np.flatnonzero(np.diff(pos) != 1); bloklar = np.split(pos, kir + 1)
        bos = [(tak[b[0]], tak[b[-1]], len(b)) for b in bloklar]
    out["bosluk_sayi"] = len(bos); out["en_uzun_bosluk"] = max((b[2] for b in bos), default=0)
    ciddi = [b for b in bos if b[2] > ESIK["ciddi_bosluk_gun"]]; out["ciddi_bosluk_sayi"] = len(ciddi)
    out["bosluk_tarihleri"] = ";".join(f"{a.date()}..{b.date()}({n})" for a, b, n in bos[:10]); out["ciddi_bosluk_tarihleri"] = ";".join(f"{a.date()}..{b.date()}({n})" for a, b, n in ciddi[:10])
    return out


def _sicrama_sinifla(k: pd.DataFrame, kurumsal: Optional[pd.DataFrame]) -> Dict[str, Any]:
    """|log getiri| > ln 1,8 günleri: kesin bölünme (sağlayıcı kurumsal işlem verisinde o gün bölünme), muhtemel bölünme (oran bölünme oranına
    ±%3 yakın VE hacim ters yönde ≥ oran/2 kat), sert haber hareketi (hacim 20 gün medyanının ≥ 3 katı), açıklanamayan sıçrama (geri kalan).
    Seriler düzeltmeli olduğundan bölünme BEKLENMEZ; muhtemel bölünme bayrağı 'düzeltme eksik olabilir' uyarısıdır. Kurumsal veri yoksa kesin denmez."""
    C = pd.to_numeric(k.Close, errors="coerce"); V = pd.to_numeric(k.Volume, errors="coerce"); r = C / C.shift(1); lr = np.log(r); vr = V / V.shift(1).replace(0, np.nan)
    med20 = V.shift(1).rolling(20, min_periods=10).median(); out = {"getiri_100_ustu_sayi": int(((r - 1) > ESIK["getiri_anormal"]).sum()), "kesin_bolunme": 0, "muhtemel_bolunme": 0, "aciklanamayan_sicrama": 0, "sert_haber_hareketi": 0, "sicrama_tarihleri": ""}
    gunler = k.index[(lr.abs() > ESIK["sicrama_log"]).fillna(False).to_numpy()]; kay = []
    kur_gunler = set(pd.to_datetime(kurumsal.tarih).dt.normalize()) if (kurumsal is not None and len(kurumsal) and "tarih" in kurumsal) else None
    for t in gunler:
        oran = float(r.loc[t]) if np.isfinite(r.loc[t]) else np.nan; vo = float(vr.loc[t]) if np.isfinite(vr.loc[t]) else np.nan
        bol_yakin = np.isfinite(oran) and any(abs(oran / b - 1) <= ESIK["bolunme_oran_tol"] for b in BOLUNME_ORANLARI)
        hacim_ters = np.isfinite(vo) and ((oran < 1 and vo >= (1 / oran) / 2) or (oran > 1 and vo <= oran / 2 and vo < 1))
        if kur_gunler is not None and t in kur_gunler:
            etiket = "kesin_bolunme"
        elif bol_yakin and hacim_ters:
            etiket = "muhtemel_bolunme"
        elif np.isfinite(med20.loc[t]) and med20.loc[t] > 0 and V.loc[t] >= ESIK["hacim_sicrama_kat"] * med20.loc[t]:
            etiket = "sert_haber_hareketi"
        else:
            etiket = "aciklanamayan_sicrama"
        out[etiket] += 1; kay.append(f"{t.date()}:{etiket}:{oran:.3f}")
    out["sicrama_tarihleri"] = ";".join(kay[:10]); out["kurumsal_veri_var"] = kur_gunler is not None
    return out


def _pencere_denetim(k: pd.DataFrame, O: Optional[pd.DataFrame], sembol: str) -> Dict[str, Any]:
    """Özellik penceresi (MIN_GUN) ile ileri sonuç pencereleri (Y60 / Y120 / Y250) ayrı; olay tablosu verilirse her olayın ufku serinin içinde mi."""
    n = int(len(k)); out = {"n_gun": n, "ozellik_gun": MIN_GUN, "ozellik_yeterli": bool(n >= MIN_GUN), "ozellik_yetersiz": int(n < MIN_GUN)}
    for ad, (h, _) in OLAY.items():
        out[f"sonuc_{ad}_gun"] = int(max(0, n - MIN_GUN - h)); out[f"sonuc_{ad}_yeterli"] = bool(n - MIN_GUN - h >= 1)
    out["sonuc_Y60_yetersiz"] = int(not out["sonuc_Y60_yeterli"])
    if O is not None and len(O):
        Os = O[O.sembol == sembol]; eksik = 0
        for r in Os.itertuples():
            h = OLAY[r.ufuk][0]
            if int(r.i) + h >= n:
                eksik += 1
        out["olay_sayisi"] = int(len(Os)); out["olay_pencere_eksik"] = eksik
    else:
        out["olay_sayisi"] = 0; out["olay_pencere_eksik"] = 0
    de = donem_etiketi(pd.Series(k.index))
    for ad in DONEM:
        out[f"gun_{ad}"] = int((de == ad).sum())
    return out


def sembol_kalite(s: str, d: Optional[pd.DataFrame], O: Optional[pd.DataFrame] = None, kurumsal: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Tek sembol. d None -> fiyat yok; boş -> boş seri. Orijinal d değişmez (normalize kopya). Dönüş: ayrı sütunlu ölçüler + hata sınıfı özetleri."""
    out: Dict[str, Any] = {"sembol": sembol_normalize(s), "fiyat_yok": int(d is None), "bos_seri": int(d is not None and len(d) == 0)}
    if d is None or len(d) == 0:
        out.update({"n_gun": 0, "ilk": pd.NaT, "son": pd.NaT}); return _siniflandir(out)
    out.update(_sutun_tur(d))
    if out["sutun_eksik"]:
        out.update({"n_gun": int(len(d)), "ilk": pd.NaT, "son": pd.NaT}); return _siniflandir(out)
    k, bilgi = _normalize_kopya(d); out.update(bilgi); out["ilk"] = k.index[0]; out["son"] = k.index[-1]
    out["kisa_seri_320"] = int(len(k) < 320)
    out.update(_ohlcv_denetim(k)); out.update(_takvim_denetim(k)); out.update(_sicrama_sinifla(k, kurumsal)); out.update(_pencere_denetim(k, O, out["sembol"]))
    out["eksik_hacim_pay_yuksek"] = int(np.isfinite(out["eksik_hacim_pay"]) and out["eksik_hacim_pay"] > ESIK["sifir_hacim_pay"])
    out["sifir_hacim_pay_yuksek"] = int(np.isfinite(out["sifir_hacim_pay"]) and out["sifir_hacim_pay"] > ESIK["sifir_hacim_pay"])
    return _siniflandir(out)


def _siniflandir(out: Dict[str, Any]) -> Dict[str, Any]:
    hata = [c for c in HATA_SUTUN if out.get(c, 0)]; yet = [c for c in YETERSIZ_SUTUN if out.get(c, 0)]
    if out.get("sifir_hacim_pay_yuksek"):
        yet.append("sifir_hacim_pay_yuksek")
    piy = [c for c in ("getiri_100_ustu_sayi", "sert_haber_hareketi") if out.get(c, 0)]; sup = [c for c in ("muhtemel_bolunme", "aciklanamayan_sicrama", "kesin_bolunme") if out.get(c, 0)]
    out["veri_hatasi"] = ";".join(hata); out["veri_yetersiz"] = ";".join(yet); out["piyasa_davranisi"] = ";".join(piy); out["supheli_sicrama"] = ";".join(sup)
    out["veri_hatasi_var"] = bool(hata); out["veri_yetersiz_var"] = bool(yet); out["kullanilabilir"] = bool(not hata and not yet)
    return out


# ---------------------------------------------------------------- evren düzeyi
def _cik_denetim(EV: pd.DataFrame) -> pd.DataFrame:
    E = EV.copy(); cik = pd.to_numeric(E.get("cik", pd.Series(np.nan, index=E.index)), errors="coerce")
    E["cik_bos"] = cik.isna().astype(int); E["cik_gecersiz"] = ((cik.notna()) & ((cik <= 0) | (cik > 9_999_999_999) | (cik != cik.round()))).astype(int)
    say = cik[cik.notna()].value_counts(); E["cik_coklu_sembol"] = cik.map(say).fillna(0).astype(int).gt(1).astype(int)
    E["cik_coklu_sembol_liste"] = cik.map(lambda c: ";".join(sorted(E.sembol[cik == c])) if pd.notna(c) and say.get(c, 0) > 1 else "")
    alt = E.get("alt", pd.Series("", index=E.index)).fillna("").astype(str)
    E["sinif_4a"] = alt.str.startswith("4a").astype(int); E["sinif_4b"] = alt.str.startswith("4b").astype(int); E["sembol_yeniden_kullanim"] = E["sinif_4b"]
    ad = E.get("sec_ad", pd.Series("", index=E.index)); E["sec_ad_bos"] = (ad.isna() | ad.astype(str).str.strip().str.lower().isin(["", "nan", "none"])).astype(int)
    sek = E.get("sektor", pd.Series(np.nan, index=E.index)); E["sektor_bos"] = (sek.isna() | sek.astype(str).str.strip().str.lower().isin(["", "nan", "none", "bilinmiyor"])).astype(int)
    E["seri_erken_bool"] = E.get("seri_erken", pd.Series(None, index=E.index)).map(bool_cevir); E["seri_erken_gecersiz"] = E.seri_erken_bool.isna().astype(int)
    E["kesilmis_k54"] = (E.get("seri_sonu", pd.Series("", index=E.index)).astype(str) == "kes").astype(int)
    return E


def evren_kalite(V: Dict[str, pd.DataFrame], EV: pd.DataFrame, O: Optional[pd.DataFrame] = None, kurumsal: Optional[Dict[str, pd.DataFrame]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Bütün EV evreni rapora girer (V'de olmayanlar fiyat_yok); V'de olup EV'de olmayanlar ayrı (v_fazla); EV yinelenen sembol denetlenir."""
    EV = EV.copy(); EV["sembol"] = EV.sembol.map(sembol_normalize); Vn = {sembol_normalize(s): d for s, d in V.items()}
    yin = EV.sembol[EV.sembol.duplicated(keep=False)].unique().tolist(); v_fazla = sorted(set(Vn) - set(EV.sembol))
    rows = [sembol_kalite(s, Vn.get(s), O, (kurumsal or {}).get(s)) for s in EV.sembol]
    Q = pd.DataFrame(rows); E = _cik_denetim(EV)
    kol = [c for c in ["sembol", "kaynak", "sinif", "alt", "seri_sonu", "kesim", "cik", "sec_ad", "sektor", "seri_erken", "evren_bas", "cik_bos", "cik_gecersiz", "cik_coklu_sembol", "cik_coklu_sembol_liste",
                       "sinif_4a", "sinif_4b", "sembol_yeniden_kullanim", "sec_ad_bos", "sektor_bos", "seri_erken_bool", "seri_erken_gecersiz", "kesilmis_k54"] if c in E.columns]
    Q = Q.merge(E[kol], on="sembol", how="left"); Q["ev_yinelenen"] = Q.sembol.isin(yin).astype(int)
    n = int(len(Q)); say = lambda c: int(Q[c].fillna(0).astype(float).gt(0).sum()) if c in Q else 0
    ozet: Dict[str, Any] = {
        "sembol_ev": n, "fiyat_var": int((Q.fiyat_yok == 0).sum()), "fiyat_yok": say("fiyat_yok"), "bos_seri": say("bos_seri"), "kisa_seri_320": say("kisa_seri_320"), "kesilmis_k54": say("kesilmis_k54"),
        "v_fazla": len(v_fazla), "v_fazla_liste": v_fazla[:20], "ev_yinelenen": len(yin), "ev_yinelenen_liste": yin[:20],
        "kaynak": Q.kaynak.value_counts().to_dict() if "kaynak" in Q else {}, "sinif": Q.sinif.value_counts().sort_index().to_dict() if "sinif" in Q else {},
        "sinif_4a": say("sinif_4a"), "sinif_4b": say("sinif_4b"),
        "cik_eslesen": int(((Q.cik_bos == 0) & (Q.cik_gecersiz == 0)).sum()) if "cik_bos" in Q else 0, "cik_bos": say("cik_bos"), "cik_gecersiz": say("cik_gecersiz"), "cik_coklu_sembol": say("cik_coklu_sembol"),
        "sembol_yeniden_kullanim": say("sembol_yeniden_kullanim"), "sec_ad_bos": say("sec_ad_bos"), "sektor_bilinen": int((Q.sektor_bos == 0).sum()) if "sektor_bos" in Q else 0, "sektor_bos": say("sektor_bos"),
        "seri_erken": int(Q.seri_erken_bool.eq(True).sum()) if "seri_erken_bool" in Q else 0, "seri_erken_gecersiz": say("seri_erken_gecersiz"),
        "takvim": "NYSE kuralları (pandas holiday; Juneteenth 2022+, özel kapanışlar 2018-12-05, 2025-01-09)",
        "saat_dilimli": say("saat_dilimli"), "sirasiz": say("sirasiz"), "yinelenen_islem_gunlu": say("yinelenen_islem_gunu"), "takvim_disi_satirli": say("takvim_disi_satir"),
        "eksik_islem_gunu_toplam": int(Q.eksik_islem_gunu.fillna(0).sum()) if "eksik_islem_gunu" in Q else 0, "bosluklu": say("bosluk_sayi"), "ciddi_bosluklu": say("ciddi_bosluk_sayi"),
        "en_uzun_bosluk_max": int(Q.en_uzun_bosluk.fillna(0).max()) if "en_uzun_bosluk" in Q else 0,
        "sutun_eksik": say("sutun_eksik"), "tur_hatali": say("tur_hatasi"), "nan_fiyatli": say("nan_fiyat"), "inf_fiyatli": say("inf_fiyat"), "sifir_negatif_fiyatli": say("sifir_negatif_fiyat"),
        "negatif_hacimli": say("negatif_hacim"), "eksik_hacimli": say("eksik_hacim_sayi"), "eksik_hacim_pay_yuksek": say("eksik_hacim_pay_yuksek"), "sifir_hacim_pay_yuksek": say("sifir_hacim_pay_yuksek"),
        "ohlc_high_dusuk": say("ohlc_high_dusuk"), "ohlc_low_yuksek": say("ohlc_low_yuksek"), "ohlc_high_low": say("ohlc_high_low"),
        "getiri_100_ustu": say("getiri_100_ustu_sayi"), "kesin_bolunme": say("kesin_bolunme"), "muhtemel_bolunme": say("muhtemel_bolunme"), "aciklanamayan_sicrama": say("aciklanamayan_sicrama"), "sert_haber_hareketi": say("sert_haber_hareketi"),
        "kurumsal_veri_var": bool(kurumsal), "ozellik_yeterli": int(Q.ozellik_yeterli.fillna(False).astype(bool).sum()) if "ozellik_yeterli" in Q else 0,
        **{f"sonuc_{ad}_yeterli": int(Q[f"sonuc_{ad}_yeterli"].fillna(False).astype(bool).sum()) if f"sonuc_{ad}_yeterli" in Q else 0 for ad in OLAY},
        "olay_pencere_eksik": int(Q.olay_pencere_eksik.fillna(0).sum()) if "olay_pencere_eksik" in Q else 0,
        "donem_kapsami": {ad: int((Q[f"gun_{ad}"].fillna(0) > 0).sum()) if f"gun_{ad}" in Q else 0 for ad in DONEM},
        "veri_hatali": int(Q.veri_hatasi_var.sum()), "veri_yetersiz": int(Q.veri_yetersiz_var.sum()), "piyasa_davranisli": int(Q.piyasa_davranisi.astype(str).ne("").sum()), "supheli_sicramali": int(Q.supheli_sicrama.astype(str).ne("").sum()),
        "kullanilabilir": int(Q.kullanilabilir.sum()), "fiyat_turu": "bölünme + temettü düzeltmeli (V_ABD / K34 Yahoo auto_adjust; Tiingo adj); ham Close yok",
        "ilk_gun_medyan": str(Q.ilk.dropna().median().date()) if Q.ilk.notna().any() else "", "son_gun_max": str(Q.son.dropna().max().date()) if Q.son.notna().any() else "",
    }
    return Q, ozet


def kapsam_md(Q: pd.DataFrame, ozet: Dict[str, Any], baslik: str = "") -> List[str]:
    """K55_VERI_KAPSAMI.md gövdesi (raporlama.py ile birleşir)."""
    L = [f"# K55 — VERİ KAPSAMI {baslik}", "", "## Evren toplamı ve kapsam (EV'deki BÜTÜN semboller; fiyatı olmayanlar dahil)", ""]
    for k in ("sembol_ev", "fiyat_var", "fiyat_yok", "bos_seri", "kisa_seri_320", "kesilmis_k54", "v_fazla", "v_fazla_liste", "ev_yinelenen", "kaynak", "sinif", "sinif_4a", "sinif_4b", "fiyat_turu"):
        L.append(f"- {k}: {ozet.get(k)}")
    L += ["", "## Şirket eşleştirmesi", ""] + [f"- {k}: {ozet.get(k)}" for k in ("cik_eslesen", "cik_bos", "cik_gecersiz", "cik_coklu_sembol", "sembol_yeniden_kullanim", "sec_ad_bos", "sektor_bilinen", "sektor_bos", "seri_erken", "seri_erken_gecersiz")]
    L += ["", "## Tarih ve takvim (ABD işlem takvimi; tatiller eksik gün değil)", ""] + [f"- {k}: {ozet.get(k)}" for k in ("takvim", "saat_dilimli", "sirasiz", "yinelenen_islem_gunlu", "takvim_disi_satirli", "eksik_islem_gunu_toplam", "bosluklu", "ciddi_bosluklu", "en_uzun_bosluk_max")]
    L += ["", "## OHLCV sorunları (veri hatası; sembol sayısı)", ""] + [f"- {k}: {ozet.get(k)}" for k in ("sutun_eksik", "tur_hatali", "nan_fiyatli", "inf_fiyatli", "sifir_negatif_fiyatli", "negatif_hacimli", "eksik_hacimli", "eksik_hacim_pay_yuksek", "sifir_hacim_pay_yuksek", "ohlc_high_dusuk", "ohlc_low_yuksek", "ohlc_high_low")]
    L += ["", "## Getiri ve bölünme benzeri hareket (kesin / muhtemel / açıklanamayan / sert haber; kurumsal veri yoksa kesin denmez)", ""] + [f"- {k}: {ozet.get(k)}" for k in ("getiri_100_ustu", "kesin_bolunme", "muhtemel_bolunme", "aciklanamayan_sicrama", "sert_haber_hareketi", "kurumsal_veri_var")]
    L += ["", "## Özellik ve sonuç pencereleri, dönem kapsamı", ""] + [f"- {k}: {ozet.get(k)}" for k in ("ozellik_yeterli", "sonuc_Y60_yeterli", "sonuc_Y120_yeterli", "sonuc_Y250_yeterli", "olay_pencere_eksik", "donem_kapsami")]
    L += ["", "## Sınıf özetleri (sembol sayısı)", ""] + [f"- {k}: {ozet.get(k)}" for k in ("veri_hatali", "veri_yetersiz", "piyasa_davranisli", "supheli_sicramali", "kullanilabilir")]
    return L
