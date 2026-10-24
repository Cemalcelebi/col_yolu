# -*- coding: utf-8 -*-
"""
ZİNCİR DENETİMİ v1.1 — Çöl Yolu veri→sinyal→çıkış→muhasebe zincirinin her halkasını tartar
==========================================================================================
Soru: ölçülen sayı, kod doğruyken bile hangi yoldan yanlış olabilir? Her madde kendi hükmünü yazar.
  1. BÜTÜNLÜK   : fiziksel olarak imkânsız barlar (açılış/kapanış aralık dışında, H<L, fiyat≤0, çift tarih) — bozuk açılış buradan.
  2. TAKVİM     : piyasanın açık olduğu günde (hisselerin ≥%80'inde bar var) bu hissede bar yok → eksik gün.
  3. DOLUM      : sinyal ertesi açılış tavandan (≥ +%9,5) → alınamaz; tabandan (≤ −%9,5) → kötü dolum. Payı.
  4. TEMETTÜ    : önbellek temettü-düzeltisiz; tutuş penceresine (ufuk bar) temettü denk gelen sinyal payı ve ortalama verim.
  5. KESİK PENCERE: veri sonuna ufuk bardan yakın sinyaller (yarım ölçülen) payı.
  6. NEDENSELLİK: (a) col_olc(tam seri, T) == col_olc(T'de kesik seri)? (kod sızıntısı)  (b) d'deki saklı sütunlar
                  (clv, bant_son, ortaust, uzunluk, doji, alt_fitil, dar, gecerli_oran, GECER) sinyal gününde kesilmiş veriden
                  yeniden üretilebiliyor mu? VERI_ESKI (ham yedek) verilirse d'nin üretildiği veriyle karşılaştırır.
  7. MALİYET    : basit P&L kopyası (ertesi açılış giriş, +%20 sonrası SMA20 trail, ufuk çıkış) %0,4 / %1,0 / %1,5 maliyetle.
  8. HAYATTA KALMA: evrende son barı eski hisse sayısı + temel_duz'da olup evrende olmayanlar.
Rapor: {K}/zincir_denetimi_rapor.txt. Hiçbir şeyi değiştirmez (yalnız okur); temettü önbelleği {K}/temettu.pkl (kaldığı yerden sürer).

    exec(open(K + "/zincir_denetimi.py", encoding="utf-8").read())
    ZD = zincir_denetimi(K, VERI, d[d.GECER], col_olc=col_olc, VERI_ESKI=VERI_ESKI)     # BASLAT'tan sonra
"""
from __future__ import annotations

import logging
import os
import pickle
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

ZD_SURUM = "1.1"
_zd_log = logging.getLogger("zincir_denetimi")
if not _zd_log.handlers:
    _h = logging.StreamHandler(sys.stdout)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s zincir: %(message)s", "%H:%M:%S"))
    _zd_log.addHandler(_h)
_zd_log.setLevel(logging.INFO)
_zd_log.propagate = False

if any(k in globals() for k in ("zd_butunluk", "zd_takvim", "zd_dolum", "zincir_denetimi")) and globals().get("_ZD_IMZA") != "zincir_denetimi":
    raise RuntimeError("çakışma kapısı: bellekte başka bir zd_* ismi var — yeni oturumda çalıştır")
_ZD_IMZA = "zincir_denetimi"


# ---------------------------------------------------------------- yardımcı
def _zd_ohlcv(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    kol = {str(c).lower(): c for c in df.columns}
    ad = {k: kol.get(uzun, kol.get(k)) for k, uzun in (("o", "open"), ("h", "high"), ("l", "low"), ("c", "close"), ("v", "volume"))}
    if any(v is None for v in ad.values()) or not len(df):
        return None
    out = pd.DataFrame({k.upper(): pd.to_numeric(df[v], errors="coerce") for k, v in ad.items()})
    ix = pd.to_datetime(out.index)
    out.index = (ix.tz_localize(None) if getattr(ix, "tz", None) is not None else ix).normalize()
    return out


def _zd_evren(V: Any) -> Dict[str, pd.DataFrame]:
    V = V["veri"] if isinstance(V, dict) and isinstance(V.get("veri"), dict) else V
    E = {}
    for s, df in V.items():
        o = _zd_ohlcv(df)
        if o is not None and len(o):
            E[str(s).upper().replace(".IS", "")] = o
    return E


def _zd_sinyaller(d: pd.DataFrame) -> pd.DataFrame:
    s = d.copy()
    s["sembol"] = s["sembol"].astype(str).str.upper().str.replace(".IS", "", regex=False)
    s["tarih"] = pd.to_datetime(s["tarih"]).dt.normalize()
    return s[["sembol", "tarih"] + [c for c in s.columns if c not in ("sembol", "tarih")]].drop_duplicates(subset=["sembol", "tarih"])


# ---------------------------------------------------------------- 1. bütünlük
def zd_butunluk(E: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    say = {"bar": 0, "acilis_disi": 0, "kapanis_disi": 0, "h_kucuk_l": 0, "fiyat_sifir": 0, "cift_tarih": 0, "hacim_sifir_hareketli": 0}
    hisse: Dict[str, int] = {}
    for s, M in E.items():
        n = len(M); say["bar"] += n
        a = ((M["O"] > M["H"] * 1.0001) | (M["O"] < M["L"] * 0.9999)) & M["O"].notna()
        c = ((M["C"] > M["H"] * 1.0001) | (M["C"] < M["L"] * 0.9999)) & M["C"].notna()
        hl = (M["H"] < M["L"]) & M["H"].notna() & M["L"].notna()
        sf = (M[["O", "H", "L", "C"]] <= 0).any(axis=1)
        ct = M.index.duplicated()
        hs = (M["V"] == 0) & (M["C"] != M["C"].shift(1))
        say["acilis_disi"] += int(a.sum()); say["kapanis_disi"] += int(c.sum()); say["h_kucuk_l"] += int(hl.sum())
        say["fiyat_sifir"] += int(sf.sum()); say["cift_tarih"] += int(ct.sum()); say["hacim_sifir_hareketli"] += int(hs.sum())
        k = int(a.sum() + c.sum() + hl.sum() + sf.sum() + ct.sum())
        if k:
            hisse[s] = k
    top = sorted(hisse.items(), key=lambda x: -x[1])[:15]
    bozuk = say["acilis_disi"] + say["kapanis_disi"] + say["h_kucuk_l"] + say["fiyat_sifir"] + say["cift_tarih"]
    say["bozuk_pay"] = bozuk / max(1, say["bar"])
    say["en_cok"] = top
    say["hukum"] = (f"imkânsız bar {bozuk}/{say['bar']} (%{100 * say['bozuk_pay']:.2f}); açılış aralık dışı {say['acilis_disi']}, kapanış aralık dışı {say['kapanis_disi']}, H<L {say['h_kucuk_l']}, fiyat≤0 {say['fiyat_sifir']}, çift tarih {say['cift_tarih']} → "
                   + ("TEMİZ" if say["bozuk_pay"] < 0.001 else "DÜZELTİLMELİ: açılış aralık dışıysa giriş fiyatı yanlış; bu barlarda açılış = kapanış alınmalı"))
    return say


# ---------------------------------------------------------------- 2. takvim
def zd_takvim(E: Dict[str, pd.DataFrame], esik: float = 0.8) -> Dict[str, Any]:
    tum = pd.Index(sorted(set().union(*[set(M.index) for M in E.values()])))
    sayac = pd.Series(0, index=tum, dtype=int)
    for M in E.values():
        sayac.loc[M.index.unique()] += 1
    acik = sayac[sayac >= esik * len(E)].index
    eksik_toplam = 0; hisse: Dict[str, int] = {}
    for s, M in E.items():
        if len(M) < 2:
            continue
        bek = acik[(acik >= M.index[0]) & (acik <= M.index[-1])]
        e = int(len(bek.difference(M.index)))
        eksik_toplam += e
        if e:
            hisse[s] = e
    top = sorted(hisse.items(), key=lambda x: -x[1])[:15]
    return {"acik_gun": int(len(acik)), "eksik_bar": eksik_toplam, "eksik_hisse": len(hisse), "en_cok": top,
            "hukum": f"piyasa açık {len(acik)} gün; {len(hisse)} hissede toplam {eksik_toplam} eksik bar → " + ("TEMİZ" if eksik_toplam < 0.002 * len(acik) * len(E) else "boşluklu hisseler var (işlem durdurma ya da indirme hatası); ufuk sayımı bar bazlı olduğu için pencere uzar")}


# ---------------------------------------------------------------- 3. dolum
def zd_dolum(E: Dict[str, pd.DataFrame], S: pd.DataFrame, limit: float = 0.095) -> Dict[str, Any]:
    oran: List[float] = []; yok = 0
    for r in S.itertuples():
        M = E.get(r.sembol)
        if M is None:
            yok += 1; continue
        i = M.index.get_indexer([r.tarih])[0]
        if i < 0 or i + 1 >= len(M):
            yok += 1; continue
        o = float(M["O"].iloc[i + 1]); c = float(M["C"].iloc[i])
        if o > 0 and c > 0:
            oran.append(o / c - 1)
    a = np.array(oran)
    tavan = float((a >= limit).mean()) if len(a) else np.nan; taban = float((a <= -limit).mean()) if len(a) else np.nan
    return {"n": int(len(a)), "bulunamayan": yok, "tavan_pay": tavan, "taban_pay": taban, "bosluk_medyan": float(np.median(a)) if len(a) else np.nan,
            "bosluk_ort": float(a.mean()) if len(a) else np.nan,
            "hukum": f"n={len(a)}: ertesi açılış tavandan %{100 * tavan:.1f} (alınamaz), tabandan %{100 * taban:.1f}; boşluk medyan %{100 * (np.median(a) if len(a) else 0):+.1f} ort %{100 * (a.mean() if len(a) else 0):+.1f} → "
                     + ("tavan açılış payı küçük" if tavan < 0.03 else "tavan açılışlar ölçümden ÇIKARILMALI ya da bir sonraki gün girilmeli; bu kadar işlem gerçekte alınamıyor")}


# ---------------------------------------------------------------- 4. temettü
def _zd_yf_temettu(s: str) -> pd.Series:
    import yfinance as yf
    d = yf.Ticker(s + ".IS").dividends
    if d is None or not len(d):
        return pd.Series(dtype=float)
    d.index = pd.to_datetime(d.index).tz_localize(None).normalize()
    return d.astype(float)


def zd_temettu_oku(K: str, semboller: List[str], indir: Any = None) -> Dict[str, pd.Series]:
    yol = os.path.join(K, "temettu.pkl")
    D: Dict[str, Any] = pickle.load(open(yol, "rb")) if os.path.exists(yol) else {}
    indir = indir or _zd_yf_temettu
    kalan = [s for s in semboller if s not in D]
    if kalan:
        _zd_log.info("temettü indiriliyor: %d kaldı (%d hazır)", len(kalan), len(D))
    for i, s in enumerate(kalan, 1):
        try:
            D[s] = indir(s)
        except Exception as e:
            D[s] = pd.Series(dtype=float); _zd_log.debug("%s temettü: %s", s, e)
        if i % 25 == 0 or i == len(kalan):
            pickle.dump(D, open(yol, "wb"))
    return D


def zd_temettu(E: Dict[str, pd.DataFrame], S: pd.DataFrame, T: Dict[str, pd.Series], ufuk: int = 120) -> Dict[str, Any]:
    n = 0; etk = 0; verim: List[float] = []
    for r in S.itertuples():
        M = E.get(r.sembol); t = T.get(r.sembol)
        if M is None:
            continue
        i = M.index.get_indexer([r.tarih])[0]
        if i < 0:
            continue
        n += 1
        if t is None or not len(t):
            continue
        son = M.index[min(len(M) - 1, i + ufuk)]
        tt = t[(t.index > r.tarih) & (t.index <= son)]
        if len(tt):
            etk += 1
            for gun, tutar in tt.items():
                j = M.index.get_indexer([gun])[0]
                onc = float(M["C"].iloc[j - 1]) if j > 0 else np.nan
                if onc and onc > 0:
                    verim.append(float(tutar) / onc)
    pay = etk / max(1, n); v = float(np.mean(verim)) if verim else np.nan
    return {"n": n, "etkilenen": etk, "pay": pay, "verim_ort": v, "toplam_etki_puan": pay * v * 100 if verim else np.nan,
            "hukum": f"{etk}/{n} sinyalin penceresinde temettü (%{100 * pay:.1f}); ortalama verim %{100 * v:.1f} → getiri ortalaması ~{pay * v * 100:.2f} puan DÜŞÜK ölçülüyor; ayrıca temettü günü boşluğu SMA20 trail'i erken tetikleyebilir"
                     if verim else f"{etk}/{n} sinyalde temettü; verim hesaplanamadı"}


# ---------------------------------------------------------------- 5. kesik pencere
def zd_kesik(E: Dict[str, pd.DataFrame], S: pd.DataFrame, ufuk: int = 120, en_az: int = 40) -> Dict[str, Any]:
    tam = 0; kesik = 0; atilan = 0
    for r in S.itertuples():
        M = E.get(r.sembol)
        if M is None:
            continue
        i = M.index.get_indexer([r.tarih])[0]
        if i < 0:
            continue
        ileri = len(M) - 1 - i
        if ileri >= ufuk:
            tam += 1
        elif ileri >= en_az:
            kesik += 1
        else:
            atilan += 1
    n = tam + kesik + atilan
    return {"tam": tam, "kesik": kesik, "atilan": atilan, "kesik_pay": kesik / max(1, n),
            "hukum": f"tam pencere {tam}, kesik ({en_az}–{ufuk - 1} bar) {kesik} (%{100 * kesik / max(1, n):.1f}), atılan (<{en_az}) {atilan} → "
                     + ("kesik pay küçük" if kesik / max(1, n) < 0.05 else "kesik işlemler sonucu oynatır; rapor 'tam pencere' ve 'kesik dahil' diye ikiye ayrılmalı")}


# ---------------------------------------------------------------- 6. nedensellik
ZD_KARSILASTIR = ("clv", "bant_son", "ortaust", "uzunluk", "doji", "alt_fitil", "dar", "gecerli_oran", "GECER", "tavan")


def _zd_esit(a: Any, b: Any, kol: str) -> bool:
    """d'deki değer ile yeniden hesaplanan değer aynı mı. Sayısal: yuvarlama payı (d 3 ondalık yazar). NaN==NaN."""
    if kol == "GECER":
        return bool(a) == bool(b)
    try:
        fa, fb = float(a), float(b)
    except (TypeError, ValueError):
        return str(a) == str(b)
    if np.isnan(fa) and np.isnan(fb):
        return True
    if np.isnan(fa) or np.isnan(fb):
        return False
    if kol == "uzunluk":
        return int(round(fa)) == int(round(fb))
    return abs(fa - fb) <= 0.0015 + 0.002 * abs(fb)


def zd_nedensellik(E: Dict[str, pd.DataFrame], S: pd.DataFrame, col_segment: Optional[Callable] = None, ornek: int = 60, seed: int = 7,
                   col_olc: Optional[Callable] = None, E_eski: Optional[Dict[str, pd.DataFrame]] = None) -> Dict[str, Any]:
    """İki soru, iki ölçü:
    (a) KOD SIZINTISI: olc(tam seri, tarih=T) ile olc(T'de kesilmiş seri) aynı sonucu veriyor mu? Vermiyorsa ölçüm T'den sonrasına bakıyor.
    (b) LİSTE UYUMU : d'deki saklı sütunlar (clv, bant_son, ortaust, uzunluk, doji, alt_fitil, dar, gecerli_oran, GECER, tavan)
        sinyal gününde kesilmiş veriden yeniden hesaplananla aynı mı? E_eski verilirse (d'nin üretildiği ham veri) karşılaştırma onunla yapılır;
        yoksa onarılmış veriyle (bedelsiz onarımı geçen hisselerde fark normaldir, 'veri_farki' olarak sayılır).
    col_olc verilirse o (tüm sütunlar), yoksa col_segment (yalnız segment sütunları) kullanılır."""
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(S), size=min(ornek, len(S)), replace=False)
    olc = col_olc if col_olc is not None else col_segment
    if olc is None:
        return {"n": 0, "hukum": "col_olc/col_segment verilmedi; nedensellik ölçülemedi"}
    kol = [c for c in ZD_KARSILASTIR if c in S.columns]
    sizinti = 0; uyum = 0; uyumsuz = 0; hata = 0
    kol_uyumsuz: Dict[str, int] = {c: 0 for c in kol}; ornekler: List[str] = []; sizinti_ornek: List[str] = []
    EK = E_eski if E_eski is not None else E
    for j in idx:
        r = S.iloc[j]; sem = r["sembol"]; T = r["tarih"]
        M = E.get(sem); MK = EK.get(sem)
        if M is None or MK is None:
            hata += 1; continue
        i = M.index.get_indexer([T])[0]; ik = MK.index.get_indexer([T])[0]
        if i < 60 or ik < 60:
            hata += 1; continue
        ad = {"O": "Open", "H": "High", "L": "Low", "C": "Close", "V": "Volume"}
        tam = M.rename(columns=ad); kesik = M.iloc[: i + 1].rename(columns=ad)
        try:
            s_tam = olc(tam, T) if col_olc is not None else None
            s_kesik = olc(kesik) if col_olc is None else olc(kesik, None)
            s_d = olc(MK.iloc[: ik + 1].rename(columns=ad), None) if EK is not E else s_kesik
        except Exception as e:
            hata += 1; _zd_log.debug("olc %s: %s", sem, e); continue
        if s_tam is not None:                                                  # (a) kod sızıntısı
            fark = [c for c in kol if not _zd_esit((s_tam or {}).get(c, np.nan), (s_kesik or {}).get(c, np.nan), c)]
            if (s_tam is None) != (s_kesik is None) or fark:
                sizinti += 1; sizinti_ornek.append(f"{sem} {pd.Timestamp(T).date()} {','.join(fark) or 'None/dict'}")
        if s_d is None:                                                         # (b) liste uyumu
            uyumsuz += 1; ornekler.append(f"{sem} {pd.Timestamp(T).date()} kesik veride sinyal yok"); continue
        fark = [c for c in kol if not _zd_esit(r[c], s_d.get(c, np.nan), c)]
        if not fark:
            uyum += 1
        else:
            for c in fark:
                kol_uyumsuz[c] += 1
            uyumsuz += 1
            ornekler.append(f"{sem} {pd.Timestamp(T).date()} " + " ".join(f"{c}:d={r[c]}/yeni={s_d.get(c)}" for c in fark[:4]))
    n = len(idx) - hata
    kaynak = "ham (d'nin üretildiği) veri" if E_eski is not None else "onarılmış veri (bedelsiz onarımı geçen hisselerde fark NORMAL)"
    parca = []
    if col_olc is not None:
        parca.append(f"(a) kod sızıntısı: tam seri+tarih ile kesik seri {n - sizinti}/{n} aynı" + (" → ölçüm NEDENSEL" if sizinti == 0 else f" → {sizinti} örnekte FARKLI: ölçüm T'den sonrasına bakıyor"))
    parca.append(f"(b) liste uyumu [{kaynak}]: {len(kol)} sütun ({', '.join(kol)}) örnek {n}: uyum {uyum}, uyumsuz {uyumsuz}"
                 + (f"; sütun bazında uyumsuz: " + ", ".join(f"{c}:{v}" for c, v in kol_uyumsuz.items() if v) if uyumsuz else ""))
    if not kol:
        parca.append("→ d'de karşılaştırılacak saklı sütun yok; liste uyumu ölçülemedi")
    elif n and uyumsuz <= 0.1 * n and sizinti == 0:
        parca.append("→ sinyal listesi nedensel: saklı ölçüler sinyal günü verisinden yeniden üretildi")
    elif sizinti:
        parca.append("→ sinyal listesi GELECEĞE BAKMIŞ olabilir: ölçüm fonksiyonu kesik seriyle farklı sonuç veriyor")
    elif n:
        parca.append("→ liste ile yeniden hesap uyuşmuyor; sızıntı yoksa sebep veri/sürüm farkıdır (E_eski=ham veriyle tekrar çalıştır)")
    return {"n": n, "uyum": uyum, "uyumsuz": uyumsuz, "sizinti": sizinti, "hata": hata, "kolonlar": kol, "kol_uyumsuz": kol_uyumsuz,
            "ornek": ornekler[:8], "sizinti_ornek": sizinti_ornek[:8], "hukum": " | ".join(parca)}


# ---------------------------------------------------------------- 7. maliyet duyarlılığı
def zd_pnl(M: pd.DataFrame, i: int, tavan: float, ufuk: int = 120, hedef: float = 0.20, ma: int = 20, maliyet: float = 0.004) -> Optional[float]:
    """Basit kopya: i sinyal (kapanış > tavan), giriş i+1 açılış; H ≥ giriş×(1+hedef) sonrası ilk kapanış < SMA20 → çık; yoksa ufuk sonu kapanış."""
    if i + 1 >= len(M):
        return None
    g = float(M["O"].iloc[i + 1])
    if not g > 0:
        return None
    s20 = M["C"].rolling(ma).mean()
    son = min(len(M) - 1, i + 1 + ufuk)
    trail = False
    for j in range(i + 1, son + 1):
        if not trail and float(M["H"].iloc[j]) >= g * (1 + hedef):
            trail = True
        if trail and j > i + 1 and float(M["C"].iloc[j]) < float(s20.iloc[j]):
            return (float(M["C"].iloc[j]) / g - 1 - 2 * maliyet) * 100
    return (float(M["C"].iloc[son]) / g - 1 - 2 * maliyet) * 100


def zd_maliyet(E: Dict[str, pd.DataFrame], S: pd.DataFrame, maliyetler: Tuple[float, ...] = (0.004, 0.01, 0.015), ufuk: int = 120) -> Dict[str, Any]:
    sonuc: Dict[float, List[float]] = {m: [] for m in maliyetler}
    for r in S.itertuples():
        M = E.get(r.sembol)
        if M is None:
            continue
        i = M.index.get_indexer([r.tarih])[0]
        if i < 0 or len(M) - 1 - i < 40:
            continue
        # denetim 24 Eki: uretim kurali gibi giris tavan x 1,002 kirilimindan (60 bar); eskiden tarama gunu +1 aciliyordu ve
        # ASAGI satirlari da (uretimde islem acilmaz) dahildi
        if str(getattr(r, "yon", "YUKARI")).upper().startswith("ASAGI"):
            continue
        tv = float(getattr(r, "tavan", np.nan))
        if not np.isfinite(tv):
            continue
        kb = next((j for j in range(i + 1, min(len(M), i + 61)) if float(M["C"].iloc[j]) > tv * 1.002), None)
        if kb is None:
            continue
        for m in maliyetler:
            p = zd_pnl(M, kb, tv, ufuk=ufuk, maliyet=m)
            if p is not None:
                sonuc[m].append(p)
    ozet = {m: (len(v), float(np.mean(v)) if v else np.nan, float((np.array(v) > 0).mean()) if v else np.nan) for m, v in sonuc.items()}
    sat = "; ".join(f"%{100 * m:.1f} → n={n} bekl {b:+.1f} kazanan %{100 * k:.0f}" for m, (n, b, k) in ozet.items())
    b04 = ozet[maliyetler[0]][1]; b15 = ozet[maliyetler[-1]][1]
    return {"ozet": ozet, "hukum": f"basit kopya P&L: {sat} → " + ("%1,5 maliyette de pozitif: maliyete dayanıklı" if np.isfinite(b15) and b15 > 0 else "maliyet artınca beklenti sıfıra iniyor: küçük hisse yayılımı sonucu belirliyor")}


# ---------------------------------------------------------------- 8. hayatta kalma
def zd_hayatta(E: Dict[str, pd.DataFrame], K: str, bayat_gun: int = 30) -> Dict[str, Any]:
    son = max(M.index[-1] for M in E.values())
    eski = [s for s, M in E.items() if (son - M.index[-1]).days > bayat_gun]
    yol = os.path.join(K, "temel_duz.csv"); disarida: List[str] = []
    if os.path.exists(yol):
        t = pd.read_csv(yol, usecols=["sembol"])
        disarida = sorted(set(t["sembol"].astype(str).str.upper()) - set(E))
    return {"evren": len(E), "son_bari_eski": eski, "temelde_var_evrende_yok": disarida,
            "hukum": f"evren {len(E)}; son barı {bayat_gun}+ gün eski {len(eski)}; finansal listede olup evrende olmayan {len(disarida)} ({', '.join(disarida[:10])}{' ...' if len(disarida) > 10 else ''}) → "
                     + ("çıkanlar veride yok: Çöl getirisi olduğundan İYİ ölçülüyor (yön belli, büyüklük bilinmiyor)" if len(eski) < 0.02 * len(E) else "çıkanlar kısmen veride")}


# ---------------------------------------------------------------- rapor
def zd_rapor(R: Dict[str, Any]) -> str:
    s = [f"ZİNCİR DENETİMİ v{ZD_SURUM}"]
    for k, ad in (("butunluk", "1 BÜTÜNLÜK"), ("takvim", "2 TAKVİM"), ("dolum", "3 DOLUM"), ("temettu", "4 TEMETTÜ"), ("kesik", "5 KESİK PENCERE"),
                  ("nedensellik", "6 NEDENSELLİK"), ("maliyet", "7 MALİYET"), ("hayatta", "8 HAYATTA KALMA")):
        if k in R:
            s.append(f"{ad}: {R[k]['hukum']}")
            if k == "butunluk" and R[k].get("en_cok"):
                s.append("   en bozuk hisseler: " + ", ".join(f"{a}:{b}" for a, b in R[k]["en_cok"]))
            if k == "takvim" and R[k].get("en_cok"):
                s.append("   en boşluklu hisseler: " + ", ".join(f"{a}:{b}" for a, b in R[k]["en_cok"]))
            if k == "nedensellik" and R[k].get("ornek"):
                s.append("   uyumsuz örnekler: " + "; ".join(R[k]["ornek"]))
            if k == "nedensellik" and R[k].get("sizinti_ornek"):
                s.append("   sızıntı örnekleri: " + "; ".join(R[k]["sizinti_ornek"]))
    return "\n".join(s)


def zincir_denetimi(K: str, VERI: Any, d: pd.DataFrame, col_segment: Optional[Callable] = None, ufuk: int = 120,
                    temettu: bool = True, indir: Any = None, col_olc: Optional[Callable] = None, VERI_ESKI: Any = None,
                    ornek: int = 120) -> Dict[str, Any]:
    t0 = time.monotonic()
    E = _zd_evren(VERI); S = _zd_sinyaller(d)
    E_eski = _zd_evren(VERI_ESKI) if VERI_ESKI is not None else None
    _zd_log.info("evren %d hisse, sinyal %d", len(E), len(S))
    R: Dict[str, Any] = {"butunluk": zd_butunluk(E), "takvim": zd_takvim(E), "dolum": zd_dolum(E, S), "kesik": zd_kesik(E, S, ufuk)}
    if temettu:
        T = zd_temettu_oku(K, sorted(set(S["sembol"])), indir=indir)
        R["temettu"] = zd_temettu(E, S, T, ufuk)
    if col_segment is not None or col_olc is not None:
        R["nedensellik"] = zd_nedensellik(E, S, col_segment, ornek=ornek, col_olc=col_olc, E_eski=E_eski)
    R["maliyet"] = zd_maliyet(E, S, ufuk=ufuk)
    R["hayatta"] = zd_hayatta(E, K)
    rapor = zd_rapor(R)
    open(os.path.join(K, "zincir_denetimi_rapor.txt"), "w", encoding="utf-8").write(rapor)
    print(rapor); _zd_log.info("bitti %.0fs → zincir_denetimi_rapor.txt", time.monotonic() - t0)
    R["rapor"] = rapor
    return R
