# -*- coding: utf-8 -*-
"""
ÇÖL ÖĞREN v1.3 — Cemal'in öğrenme kuralı: şekil aday yapar, piyasa etiketler, etiketten kural çıkar
v1.3 (9 Eki 2026, akşam): önbellek VERİ İMZASI taşır. v1.2'ye kadar durum dosyası yalnız ayarlara bakıyordu; veri değişince (bedelsiz
onarımı ezildi / Yahoo seriyi düzeltti) eski veriyle bulunmuş adaylar sorgusuz kullanılıyordu. Şimdi: her hissenin taranan son tarihe
(kesim) kadarki kapanış toplamı + bar sayısı saklanır; geçmişi değişen hisse(ler)in adayları silinip yalnız onlar bütün tarihlerde
yeniden taranır, değişmeyenlere dokunulmaz. İmzasız eski durum dosyası (v1.2 ve öncesi) hangi veriyle tarandığı bilinmediği için sıfırlanır.
v1.2 (9 Eki 2026): Cemal'in ASIL kuralı doğrudan ölçülür — "U'nun sıkışık taban bölgesinde 5–8 doji". Bu kural katı diye gevşetilip
'küçük mum' olmuştu; eski testler yanlış olduğundan o gevşetme de kuşkulu. Burada taban bölgesi = dibin %taban_yakin'ı içindeki
kapanışlar (en az 8 bar: dipten itibaren 8 bar); doji = |C−O|/(H−L) < eşik, iki eşikle (0,15 ve 0,25). Ölçüler: doji_taban_15,
doji_taban_25, taban_bar, doji_taban_oran; rapor: doji sayısı kovalarına (0–2 / 3–4 / 5–8 / 9+) göre EVET oranı, iki etikette.
v1.1 (9 Eki 2026, ilk koşu sonrası): tavan/taban etiketi geometrik olarak asimetrik — sağ kolu uzun adayda taban uzakta kalır, HAYIR zorlaşır,
EVET kolaylaşır; sag_kol/egim/bant'ın yüksek AUC'si kısmen bu geometriden gelebilir. Kontrol: SİMETRİK etiket (T kapanışından ilk ±sim_pay
kapanış: yukarı EVET_S, aşağı HAYIR_S). Bir ölçü ancak iki etikette ve iki dönemde aynı yönde ayırıyorsa İZ. Etiketler tarama sonrası
fiyat verisinden yeniden kurulur (co_yeniden_etiketle); tarama tekrarlanmaz.
===================================================================================================
"Çöl mumları oluştu U şeklinde, Bollinger sıkıştı → aday. Sonra üst tavan GÖVDEYLE (kapanışla) kırıldıysa formasyon var (EVET);
tavan kırılmadan dibin altına kapanış geldiyse o çöl olmuyor (HAYIR). Bunlar olmadan öğrenme olmaz."

Nedensellik: ölçüler yalnız aday gününe (T) kadar olan barlardan; etiket T'den SONRAKİ ufuk bardan. Kod sızıntısı testi (co_sizinti)
tam seri+tarih ile kesik serinin aynı ölçüleri verdiğini sayıyla doğrular.

Aday eleği (gevşek, bilerek): K1 küçük mum + dip pencerenin ilk yarısında (U oturmuş, sağ taraf en az başlamış) + Bollinger sıkışması
(bb_rank_min ≤ bb_esik). Eğim, sağ kol yüksekliği, en dip, sol bacak, doji, hacim… ELENMEZ: hepsi ölçü olarak kaydedilir, EVET/HAYIR'ı
neyin ayırdığı sonradan bakılır.

Etiket (T+1 … T+ufuk, ilk gelen):
  EVET : kapanış ≥ tavan × (1 + onay_pay)  (tavan = penceredeki en yüksek GÖVDE ucu, fitil değil; kapanış = gövdeyle; onay_pay %10:
         sürünen çölde tavan her gün biraz aşılır, o "kırılım" değil sürünmenin kendisidir; çöl ancak tavanın belirgin üstüne
         çıkınca gerçekleşmiş sayılır. Tavan×(1+al_pay) ilk aşıldığı bar ayrıca 'kirilim_bar' olarak kaydedilir.)
  HAYIR: kapanış < taban                   (taban = penceredeki en düşük düşük)
  YOK  : ikisi de gelmedi (öğrenmeye girmez)

Çıktı: {K}/col_ogren_adaylar.csv (her aday: ölçüler + etiket + 60 bar getiri), {K}/col_ogren_rapor.txt (ölçü başına ayırma gücü,
dönem tutarlılığı), {K}/col_ogren_durum.pkl (kaldığı yerden sürer).

    exec(open(K + "/col_tanim2.py", encoding="utf-8").read())     # ct_olc, ColKural
    exec(open(K + "/col_ogren.py", encoding="utf-8").read())
    A = col_ogren(K, VERI, ct_olc, ColKural)                       # uzun iş; aynı çağrı kaldığı yerden sürer
"""
from __future__ import annotations

import logging
import os
import pickle
import sys
import time
from dataclasses import dataclass, asdict
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

CO_SURUM = "1.3"
_co_log = logging.getLogger("col_ogren")
if not _co_log.handlers:
    _h = logging.StreamHandler(sys.stdout); _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s co: %(message)s", "%H:%M:%S"))
    _co_log.addHandler(_h); _co_log.setLevel(logging.INFO)

CO_OLCULER = ["doji_taban_15", "doji_taban_25", "doji_taban_oran", "taban_bar", "uzunluk", "govde_pct", "aralik_pct", "doji", "clv", "egim_pct_gun", "bant_pct", "dip_konum", "sol_kol_pct", "sag_kol_pct",
              "taban_genislik", "egrilik", "u_r2", "ilk_egim_pct_gun", "son_egim_pct_gun", "sikisma", "sol_bacak_pct", "atr_once_ici",
              "hacim_orani", "dip_gercek_pct", "bb_rank_son", "bb_rank_min", "hafta_egim_pct", "hafta_govde_pct"]


@dataclass
class OgrenAyar:
    adim: int = 5                 # her 5 barda bir aday günü
    uz_adim: int = 3              # pencere uzunluğu 3'er bar adımla denenir (120, 117, … 15)
    min_bar: int = 15             # aday penceresi 15..120 bar
    max_bar: int = 120
    dip_konum_max: float = 0.50   # dip pencerenin ilk yarısında (U oturmuş)
    bb_esik: float = 0.35         # Bollinger: pencere içindeki en dar genişlik son 100 barın alt %35'inde
    ufuk: int = 60                # etiket penceresi (bar)
    al_pay: float = 0.002         # tavan × (1+al_pay) üstü kapanış = kırılım anı (kaydedilir)
    onay_pay: float = 0.10        # tavan × (1+onay_pay) üstü kapanış = çöl GERÇEKLEŞTİ (EVET); sürünme tavanı zaten az az aşar
    sim_pay: float = 0.10         # kontrol etiketi: T kapanışından ±%10 ilk hangisi (geometriden bağımsız)
    min_gecmis: int = 250         # aday gününden önce en az 250 bar
    min_hacim_tl: float = 1_000_000.0   # pencere medyan TL hacmi
    bas: str = "2023-01-01"       # tarama başlangıcı


# ---------------------------------------------------------------- yardımcılar
def _co_veri(V: Any) -> Dict[str, pd.DataFrame]:
    V = V["veri"] if isinstance(V, dict) and isinstance(V.get("veri"), dict) else V
    return {str(s): df for s, df in V.items() if isinstance(df, pd.DataFrame) and "Close" in df.columns}


def co_aday(df: pd.DataFrame, T: Any, ct_olc: Callable, K: Any, A: OgrenAyar) -> Optional[Dict[str, Any]]:
    """T'de biten, gevşek eleği geçen EN UZUN pencere; başlangıç en düşük kapanışa kırpılır. Geleceğe bakmaz."""
    x = df[df.index <= pd.Timestamp(T)]
    n = len(x)
    if n < A.min_gecmis:
        return None
    geri = max(getattr(K, "dip_bakis", 120), getattr(K, "sol_bacak_bar", 60), 120)
    O = x["Open"].to_numpy(float); H = x["High"].to_numpy(float); L = x["Low"].to_numpy(float); C = x["Close"].to_numpy(float)
    govde = np.abs(C - O) / C; aralik = (H - L) / C
    if np.median(govde[-A.min_bar:]) > K.govde_pct or np.median(aralik[-A.min_bar:]) > K.aralik_pct:      # son barlar küçük değilse hiç bakma
        return None
    for uz in range(min(A.max_bar, n - 1), A.min_bar - 1, -A.uz_adim):
        g = govde[n - uz:]; a = aralik[n - uz:]; c = C[n - uz:]                                            # ucuz ön eleme (ct_olc ile aynı tanımlar)
        if np.median(g) > K.govde_pct or np.median(a) > K.aralik_pct or int(np.argmin(c)) / max(uz - 1, 1) > A.dip_konum_max:
            continue
        seg = x.iloc[n - uz:]; onc = x.iloc[max(0, n - uz - geri): n - uz]
        o = ct_olc(seg, onc, K)
        if o.get("uzunluk", 0) < 3:
            continue
        kucuk = o["govde_pct"] <= K.govde_pct * 100 and o["aralik_pct"] <= K.aralik_pct * 100
        if not (kucuk and o["dip_konum"] <= A.dip_konum_max and np.isfinite(o.get("bb_rank_min", np.nan)) and o["bb_rank_min"] <= A.bb_esik):
            continue
        C = seg["Close"].to_numpy(float); i_min = int(np.argmin(C))
        if uz - i_min < A.min_bar:                                                                    # dipten sonra en az min_bar bar yok: çöl henüz genç
            return None
        if i_min > 0:                                                                                 # çöl dipten başlar: pencereyi en düşük kapanışa kırp
            seg = seg.iloc[i_min:]; onc = x.iloc[max(0, n - uz + i_min - geri): n - uz + i_min]
            o = ct_olc(seg, onc, K)
        v = seg["Volume"].to_numpy(float) if "Volume" in seg.columns else np.full(len(seg), np.nan)
        hacim_tl = float(np.nanmedian(seg["Close"].to_numpy(float) * v)) if np.isfinite(v).any() else np.nan
        if np.isfinite(hacim_tl) and hacim_tl < A.min_hacim_tl:
            return None
        o["taban"] = float(seg["Low"].min()); o["tavan"] = float(np.maximum(seg["Open"], seg["Close"]).max()); o["hacim_tl"] = hacim_tl
        o["bas"] = str(seg.index[0].date()); o["son"] = str(seg.index[-1].date())
        return o
    return None


def co_etiket(df: pd.DataFrame, T: Any, taban: float, tavan: float, A: OgrenAyar) -> Tuple[str, Optional[int], float, Optional[int]]:
    """T'den sonraki ufuk barda ilk gelen: kapanış ≥ tavan×(1+onay_pay) → EVET; kapanış < taban → HAYIR; yoksa YOK.
    Döner: (etiket, kaçıncı bar, ufuk getirisi %, kirilim_bar = tavan×(1+al_pay) ilk aşıldığı bar ya da None)"""
    il = df[df.index > pd.Timestamp(T)].head(A.ufuk)
    if len(il) < 20:
        return "KISA", None, np.nan, None
    C = il["Close"].to_numpy(float); p0 = float(df[df.index <= pd.Timestamp(T)]["Close"].iloc[-1]); g = (float(C[-1]) / p0 - 1) * 100
    kir = next((j + 1 for j, c in enumerate(C) if c > tavan * (1 + A.al_pay)), None)
    for j, c in enumerate(C):
        if c >= tavan * (1 + A.onay_pay):
            return "EVET", j + 1, g, kir
        if c < taban:
            return "HAYIR", j + 1, g, kir
    return "YOK", None, g, kir


# ---------------------------------------------------------------- tarama (kaldığı yerden)
def _co_bos() -> Dict[str, Any]:
    return {"surum": CO_SURUM, "bitti": [], "satirlar": [], "ayar": None, "kesim": None, "veri_imza": None}


def co_veri_imza(veri: Dict[str, pd.DataFrame], kesim: Any) -> Dict[str, Tuple[int, float]]:
    """Her hisse için kesim tarihine kadarki (bar sayısı, kapanış toplamı). Kesimden sonra eklenen yeni barlar imzayı değiştirmez."""
    k = pd.Timestamp(kesim); out: Dict[str, Tuple[int, float]] = {}
    for s, df in veri.items():
        c = pd.to_numeric(df["Close"][df.index <= k], errors="coerce").to_numpy(float)
        out[s] = (int(len(c)), float(np.nansum(c)))
    return out


def _co_imza_esit(a: Any, b: Any) -> bool:
    if a is None or b is None:
        return False
    return int(a[0]) == int(b[0]) and bool(np.isclose(float(a[1]), float(b[1]), rtol=1e-9, atol=1e-9))


def _co_satir(s: str, df: pd.DataFrame, T: Any, ct_olc: Callable, K: Any, A: OgrenAyar) -> Optional[Dict[str, Any]]:
    if df.index[-1] < T or df.index[0] > T or T not in df.index:
        return None
    try:
        o = co_aday(df, T, ct_olc, K, A)
    except Exception as e:
        _co_log.debug("%s@%s aday: %s", s, T, e); o = None
    if not o:
        return None
    et, kac, g, kir = co_etiket(df, T, o["taban"], o["tavan"], A)
    return {"sembol": s, "tarih": pd.Timestamp(T), "etiket": et, "kacinci_bar": kac, "kirilim_bar": kir, "getiri_ufuk": g,
            "kapanis": float(df.loc[T, "Close"]),
            **{k: o.get(k, np.nan) for k in CO_OLCULER}, "taban": o["taban"], "tavan": o["tavan"], "hacim_tl": o["hacim_tl"],
            "bas": o["bas"]}


def _co_kaydet(D: Dict[str, Any], yol: str, veri: Dict[str, pd.DataFrame]) -> None:
    if D["bitti"]:
        D["kesim"] = max(D["bitti"]); D["veri_imza"] = co_veri_imza(veri, D["kesim"])
    gecici = yol + ".tmp"
    with open(gecici, "wb") as f:
        pickle.dump(D, f, protocol=4)
    os.replace(gecici, yol)


def co_tara(K_yol: str, veri: Dict[str, pd.DataFrame], ct_olc: Callable, K: Any, A: OgrenAyar, ad: str = "col_ogren") -> pd.DataFrame:
    yol = os.path.join(K_yol, f"{ad}_durum.pkl")
    D = _co_bos()
    if os.path.exists(yol):
        try:
            with open(yol, "rb") as f:
                D0 = pickle.load(f)
            tarama_anahtar = ("adim", "uz_adim", "min_bar", "max_bar", "dip_konum_max", "bb_esik", "min_gecmis", "min_hacim_tl", "bas")
            ayni = isinstance(D0, dict) and isinstance(D0.get("ayar"), dict) and all(D0["ayar"].get(k) == getattr(A, k) for k in tarama_anahtar)
            if ayni and D0.get("bitti") and not (isinstance(D0.get("veri_imza"), dict) and D0.get("kesim")):
                _co_log.warning("durum dosyasında veri imzası yok (v1.2 ve öncesi) → hangi veriyle tarandığı bilinmiyor, sıfırdan")
            elif ayni:
                D = D0                                       # etiket ayarları (ufuk, onay_pay, sim_pay) taramayı değiştirmez: yeniden etiketlenir
            else:
                _co_log.warning("durum dosyası farklı tarama ayarı → sıfırdan")
        except Exception as e:
            _co_log.warning("durum okunamadı (%s) → sıfırdan", e)
    D["ayar"] = asdict(A)
    if D["bitti"]:                                          # veri imzası: geçmişi değişen hisseler yalnız kendileri yeniden taranır
        yeni_imza = co_veri_imza(veri, D["kesim"]); eski_imza = D["veri_imza"]
        degisen = sorted(s for s in set(yeni_imza) | set(eski_imza) if not _co_imza_esit(eski_imza.get(s), yeni_imza.get(s)))
        if degisen:
            dset = set(degisen); t2 = time.monotonic()
            print(f"  [veri imzası] {len(degisen)} hissenin geçmişi değişmiş ({', '.join(degisen[:12])}{' ...' if len(degisen) > 12 else ''}) "
                  f"→ eski adayları silinip {len(D['bitti'])} tarihte yeniden taranıyor", flush=True)
            D["satirlar"] = [r for r in D["satirlar"] if r["sembol"] not in dset]
            for t_ in D["bitti"]:
                T = pd.Timestamp(t_)
                for s in degisen:
                    if s in veri:
                        r = _co_satir(s, veri[s], T, ct_olc, K, A)
                        if r:
                            D["satirlar"].append(r)
            _co_kaydet(D, yol, veri)
            print(f"  [veri imzası] yeniden tarama bitti | {time.monotonic() - t2:.0f}s", flush=True)
    takvim = sorted(set(t for df in veri.values() for t in df.index[df.index >= pd.Timestamp(A.bas)]))
    tarihler = takvim[::A.adim]
    kalan = [t for t in tarihler if str(pd.Timestamp(t).date()) not in D["bitti"]]
    _co_log.info("%d tarih, %d bitmiş, %d kalan | hisse %d", len(tarihler), len(D["bitti"]), len(kalan), len(veri))
    t0 = time.monotonic(); yapilan = 0
    for T in kalan:
        t1 = time.monotonic(); n_aday = 0
        for s, df in veri.items():
            r = _co_satir(s, df, T, ct_olc, K, A)
            if r:
                D["satirlar"].append(r); n_aday += 1
        D["bitti"].append(str(pd.Timestamp(T).date())); yapilan += 1
        _co_kaydet(D, yol, veri)
        gec = time.monotonic() - t0
        print(f"  {len(D['bitti'])}/{len(tarihler)} {pd.Timestamp(T).date()} -> {n_aday} aday | {time.monotonic() - t1:.0f}s | kalan ~{gec / yapilan * (len(kalan) - yapilan) / 60:.0f} dk", flush=True)
    S = pd.DataFrame(D["satirlar"])
    if len(S):
        S = S.sort_values(["sembol", "bas", "tarih"]).drop_duplicates(subset=["sembol", "bas"], keep="first").reset_index(drop=True)   # aynı çöl bir kez (ilk görüldüğü gün)
    return S


# ---------------------------------------------------------------- etiketleri fiyattan yeniden kur (tarama tekrarı yok)
def co_etiket_sim(df: pd.DataFrame, T: Any, A: OgrenAyar) -> str:
    """T kapanışından ufuk içinde ilk gelen: kapanış ≥ ×(1+sim_pay) → EVET_S; kapanış ≤ ×(1−sim_pay) → HAYIR_S; yoksa YOK_S."""
    x = df[df.index <= pd.Timestamp(T)]; il = df[df.index > pd.Timestamp(T)].head(A.ufuk)
    if len(x) == 0 or len(il) < 20:
        return "KISA"
    p0 = float(x["Close"].iloc[-1])
    for c in il["Close"].to_numpy(float):
        if c >= p0 * (1 + A.sim_pay):
            return "EVET_S"
        if c <= p0 * (1 - A.sim_pay):
            return "HAYIR_S"
    return "YOK_S"


def co_yeniden_etiketle(S: pd.DataFrame, veri: Dict[str, pd.DataFrame], A: OgrenAyar) -> pd.DataFrame:
    """Kayıtlı adaylara (sembol, tarih, taban, tavan) fiyattan etiket + simetrik etiket + kapanış yazar. Ayar değişince tarama gerekmez."""
    S = S.copy(); et = []; kac = []; kir = []; g = []; sim = []; kap = []
    for r in S.itertuples():
        df = veri.get(r.sembol)
        if df is None or pd.Timestamp(r.tarih) not in df.index:
            et.append("VERİ YOK"); kac.append(None); kir.append(None); g.append(np.nan); sim.append("VERİ YOK"); kap.append(np.nan); continue
        e, k, gg, kk = co_etiket(df, r.tarih, float(r.taban), float(r.tavan), A)
        et.append(e); kac.append(k); kir.append(kk); g.append(gg); sim.append(co_etiket_sim(df, r.tarih, A)); kap.append(float(df.loc[pd.Timestamp(r.tarih), "Close"]))
    S["etiket"] = et; S["kacinci_bar"] = kac; S["kirilim_bar"] = kir; S["getiri_ufuk"] = g; S["etiket_sim"] = sim; S["kapanis"] = kap
    return S


# ---------------------------------------------------------------- Cemal'in asıl kuralı: taban bölgesinde doji sayısı
def co_doji_taban(df: pd.DataFrame, bas: Any, T: Any, taban_yakin: float = 0.03, en_az_bar: int = 8) -> Dict[str, Any]:
    """Pencere (bas..T) içinde dibin %taban_yakin'ı içindeki kapanışlar = taban bölgesi (dipten başlayarak en az en_az_bar bar).
    Doji = |C−O| / (H−L) < eşik. İki eşik: 0,15 (katı) ve 0,25 (gevşek)."""
    w = df[(df.index >= pd.Timestamp(bas)) & (df.index <= pd.Timestamp(T))]
    if len(w) < 3:
        return {"doji_taban_15": np.nan, "doji_taban_25": np.nan, "doji_taban_oran": np.nan, "taban_bar": np.nan}
    O, H, L, C = (w[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    c_min = float(C.min()); i_min = int(np.argmin(C))
    m = C <= c_min * (1 + taban_yakin); m[i_min: i_min + en_az_bar] = True
    rng = np.maximum(H - L, 1e-12); g = np.abs(C - O) / rng
    d15 = int((g[m] < 0.15).sum()); d25 = int((g[m] < 0.25).sum()); nb = int(m.sum())
    return {"doji_taban_15": d15, "doji_taban_25": d25, "doji_taban_oran": d15 / nb if nb else np.nan, "taban_bar": nb}


def co_ek_olculer(S: pd.DataFrame, veri: Dict[str, pd.DataFrame], taban_yakin: float = 0.03) -> pd.DataFrame:
    S = S.copy(); R = []
    for r in S.itertuples():
        df = veri.get(r.sembol)
        R.append(co_doji_taban(df, r.bas, r.tarih, taban_yakin) if df is not None else {"doji_taban_15": np.nan, "doji_taban_25": np.nan, "doji_taban_oran": np.nan, "taban_bar": np.nan})
    for k in ("doji_taban_15", "doji_taban_25", "doji_taban_oran", "taban_bar"):
        S[k] = [x[k] for x in R]
    return S


def co_doji_rapor(S: pd.DataFrame) -> str:
    """Doji sayısı kovalarına göre EVET oranı — tavan/taban etiketi ve simetrik etiket, dönem ayrımıyla."""
    if "doji_taban_15" not in S.columns:
        return ""
    s = ["DOJİ ÇEKİRDEĞİ (Cemal'in asıl kuralı: U taban bölgesinde 5–8 doji) — kovalara göre EVET oranı"]
    kova = pd.cut(S["doji_taban_15"].astype(float), bins=[-1, 2, 4, 8, 999], labels=["0–2", "3–4", "5–8", "9+"])
    kova25 = pd.cut(S["doji_taban_25"].astype(float), bins=[-1, 2, 4, 8, 999], labels=["0–2", "3–4", "5–8", "9+"])
    for ad, kv in (("doji<0,15", kova), ("doji<0,25", kova25)):
        for etk, poz, neg in (("etiket", "EVET", "HAYIR"), ("etiket_sim", "EVET_S", "HAYIR_S")):
            if etk not in S.columns:
                continue
            E = S[S[etk].isin([poz, neg])]
            par = []
            for k in ["0–2", "3–4", "5–8", "9+"]:
                g = E[kv[E.index] == k]
                if len(g):
                    par.append(f"{k}: n={len(g)} EVET %{100 * (g[etk] == poz).mean():.0f}")
            s.append(f"  {ad} | {etk}: " + " | ".join(par))
    return "\n".join(s)


# ---------------------------------------------------------------- öğrenme raporu
def _auc(poz: np.ndarray, neg: np.ndarray) -> float:
    """Sıra tabanlı AUC: P(poz > neg). 0,5 = ayırmıyor; >0,5 büyük değer EVET'e yakın; <0,5 küçük değer EVET'e yakın."""
    poz = poz[np.isfinite(poz)]; neg = neg[np.isfinite(neg)]
    if len(poz) == 0 or len(neg) == 0:
        return np.nan
    hepsi = np.concatenate([poz, neg]); sira = pd.Series(hepsi).rank().to_numpy()
    return float((sira[: len(poz)].sum() - len(poz) * (len(poz) + 1) / 2) / (len(poz) * len(neg)))


def co_ogren(S: pd.DataFrame, donem_sinir: str = "2024-06-01", etiket_kol: str = "etiket", poz: str = "EVET", neg: str = "HAYIR") -> pd.DataFrame:
    """Her ölçü için: poz/neg medyanı, AUC (tüm), AUC dönem 1 (< sınır) ve dönem 2 (≥ sınır), aynı yönde mi."""
    if etiket_kol not in S.columns:
        return pd.DataFrame()
    E = S[S[etiket_kol].isin([poz, neg])].copy()
    if E.empty:
        return pd.DataFrame()
    E["donem"] = np.where(pd.to_datetime(E["tarih"]) < pd.Timestamp(donem_sinir), "D1", "D2"); L = E[etiket_kol]
    R = []
    for k in CO_OLCULER:
        if k not in E.columns:
            continue
        v = E[k].astype(float); p_ = v[L == poz].to_numpy(); n_ = v[L == neg].to_numpy()
        a = _auc(p_, n_)
        a1 = _auc(v[(L == poz) & (E.donem == "D1")].to_numpy(), v[(L == neg) & (E.donem == "D1")].to_numpy())
        a2 = _auc(v[(L == poz) & (E.donem == "D2")].to_numpy(), v[(L == neg) & (E.donem == "D2")].to_numpy())
        ayni = bool(np.isfinite(a1) and np.isfinite(a2) and ((a1 - 0.5) * (a2 - 0.5) > 0))
        R.append({"olcu": k, "n": int(np.isfinite(v).sum()), "evet_medyan": float(np.nanmedian(p_)) if len(p_) else np.nan,
                  "hayir_medyan": float(np.nanmedian(n_)) if len(n_) else np.nan, "auc": a, "auc_d1": a1, "auc_d2": a2,
                  "ayni_yon": ayni, "guc": abs(a - 0.5) if np.isfinite(a) else np.nan})
    T = pd.DataFrame(R).sort_values("guc", ascending=False).reset_index(drop=True)
    return T


def co_iz(T1: pd.DataFrame, T2: pd.DataFrame, esik: float = 0.08) -> pd.DataFrame:
    """İki etiket (tavan/taban ve simetrik) ve iki dönemde aynı yönde, |AUC−0,5| ≥ esik: gerçek iz. Yalnız birinde: geometri/dönem kuşkulu."""
    if T1.empty or T2.empty:
        return pd.DataFrame()
    m = T1.merge(T2, on="olcu", suffixes=("", "_sim"))
    m["iz"] = (m.ayni_yon & m.ayni_yon_sim & (m.guc >= esik) & (m.guc_sim >= esik) & ((m.auc - 0.5) * (m.auc_sim - 0.5) > 0))
    m["kusku"] = (m.guc >= esik) & ~m.iz
    return m[["olcu", "auc", "auc_d1", "auc_d2", "auc_sim", "auc_d1_sim", "auc_d2_sim", "iz", "kusku"]].sort_values("auc", key=lambda c: (c - 0.5).abs(), ascending=False)


def co_rapor(S: pd.DataFrame, T: pd.DataFrame, A: OgrenAyar, T_sim: Optional[pd.DataFrame] = None) -> str:
    s = [f"ÇÖL ÖĞREN v{CO_SURUM} — ayar {asdict(A)}"]
    if S.empty:
        return "\n".join(s + ["aday yok"])
    say = S.etiket.value_counts().to_dict(); n_e = say.get("EVET", 0); n_h = say.get("HAYIR", 0)
    s.append(f"aday {len(S)} (tekil çöl) | EVET {n_e} | HAYIR {n_h} | YOK {say.get('YOK', 0)} | KISA {say.get('KISA', 0)} | EVET oranı %{100 * n_e / max(n_e + n_h, 1):.0f}")
    E = S[S.etiket.isin(["EVET", "HAYIR"])]
    if len(E):
        for d, g in E.groupby(pd.to_datetime(E.tarih).dt.year):
            s.append(f"  {d}: EVET {int((g.etiket == 'EVET').sum())} / HAYIR {int((g.etiket == 'HAYIR').sum())} | EVET'lerin 60 bar getirisi medyan %{g[g.etiket == 'EVET'].getiri_ufuk.median():+.1f}, HAYIR %{g[g.etiket == 'HAYIR'].getiri_ufuk.median():+.1f}")
    if not T.empty:
        pd.set_option("display.width", 220); pd.set_option("display.max_columns", None)
        s.append("ölçü başına ayırma gücü (AUC: 0,5 ayırmıyor; >0,5 büyük değer EVET'e yakın, <0,5 küçük değer EVET'e yakın; ayni_yon: iki dönemde aynı yön)")
        s.append(T.round(3).to_string(index=False))
        iz = T[(T.ayni_yon) & (T.guc >= 0.08)]
        s.append("tavan/taban etiketinde (iki dönemde aynı yön, |AUC−0,5| ≥ 0,08): " + (", ".join(f"{r.olcu} ({'büyük' if r.auc > 0.5 else 'küçük'} iyi, AUC {r.auc:.2f})" for r in iz.itertuples()) if len(iz) else "yok"))
    if T_sim is not None and not T_sim.empty and "etiket_sim" in S.columns:
        sy = S.etiket_sim.value_counts().to_dict()
        s.append(f"SİMETRİK kontrol (T kapanışından ±%{A.sim_pay * 100:.0f} ilk hangisi): EVET_S {sy.get('EVET_S', 0)} | HAYIR_S {sy.get('HAYIR_S', 0)} | YOK_S {sy.get('YOK_S', 0)}")
        M = co_iz(T, T_sim)
        s.append(M.round(3).to_string(index=False))
        gercek = M[M.iz]; kusku = M[M.kusku]
        s.append("GERÇEK İZ (iki etiket + iki dönem aynı yön): " + (", ".join(f"{r.olcu} ({'büyük' if r.auc > 0.5 else 'küçük'} iyi, AUC {r.auc:.2f}/{r.auc_sim:.2f})" for r in gercek.itertuples()) if len(gercek) else "yok"))
        s.append("KUŞKULU (yalnız tavan/taban etiketinde ayırıyor → geometri payı var): " + (", ".join(f"{r.olcu} ({r.auc:.2f} / sim {r.auc_sim:.2f})" for r in kusku.itertuples()) if len(kusku) else "yok"))
    return "\n".join(s)


# ---------------------------------------------------------------- kod sızıntısı testi
def co_sizinti(veri: Dict[str, pd.DataFrame], S: pd.DataFrame, ct_olc: Callable, K: Any, A: OgrenAyar, ornek: int = 40, seed: int = 7) -> Dict[str, Any]:
    """Örnek adaylarda: tam seri + T ile T'de kesilmiş seri aynı ölçüleri veriyor mu?"""
    if S.empty:
        return {"n": 0, "fark": 0, "hukum": "aday yok"}
    rng = np.random.default_rng(seed); idx = rng.choice(len(S), size=min(ornek, len(S)), replace=False); fark = 0; n = 0; ornekler = []
    for j in idx:
        r = S.iloc[j]; df = veri.get(r["sembol"])
        if df is None:
            continue
        T = pd.Timestamp(r["tarih"]); kesik = df[df.index <= T]
        a = co_aday(df, T, ct_olc, K, A); b = co_aday(kesik, T, ct_olc, K, A); n += 1
        if (a is None) != (b is None) or (a and b and any(not (np.isclose(float(a.get(k, np.nan)), float(b.get(k, np.nan)), equal_nan=True)) for k in CO_OLCULER)):
            fark += 1; ornekler.append(f"{r['sembol']} {T.date()}")
    return {"n": n, "fark": fark, "ornek": ornekler[:5], "hukum": f"kod sızıntısı: {n - fark}/{n} aynı" + (" → NEDENSEL" if fark == 0 else " → FARK VAR, ölçüm geleceğe bakıyor")}


# ---------------------------------------------------------------- uçtan uca
def col_ogren(K_yol: str, VERI: Any, ct_olc: Callable, ColKural: Any, A: Optional[OgrenAyar] = None, K: Any = None, ad: str = "col_ogren") -> pd.DataFrame:
    A = A or OgrenAyar(); K = K or ColKural(); veri = _co_veri(VERI)
    S = co_tara(K_yol, veri, ct_olc, K, A, ad)
    S = co_yeniden_etiketle(S, veri, A)
    S = co_ek_olculer(S, veri, getattr(K, "taban_yakin", 0.03))
    S.to_csv(os.path.join(K_yol, f"{ad}_adaylar.csv"), index=False)
    T = co_ogren(S); T_sim = co_ogren(S, etiket_kol="etiket_sim", poz="EVET_S", neg="HAYIR_S")
    rapor = co_rapor(S, T, A, T_sim) + "\n" + co_doji_rapor(S)
    sz = co_sizinti(veri, S, ct_olc, K, A); rapor += "\n" + sz["hukum"] + ((" | " + "; ".join(sz.get("ornek", []))) if sz.get("fark") else "")
    with open(os.path.join(K_yol, f"{ad}_rapor.txt"), "w", encoding="utf-8") as f:
        f.write(rapor + "\n")
    print(rapor)
    return S
