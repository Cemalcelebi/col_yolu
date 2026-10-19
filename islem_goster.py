# -*- coding: utf-8 -*-
"""
İŞLEM GÖSTER v1.0 — DENETIM'in saydığı her işlemi bar bar, resimle ve tabloyla gösterir
======================================================================================
Soru: "Çöl segmenti nereyi saymış, nerede kırıldı, kâr/zarar nereden nereye hesaplandı?"
Hiçbir şeyi yeniden hesaplamaz: DENETIM.islemler() ne saydıysa onu alır (kırılım barı, giriş, hedef, trail çıkışı) ve
önbellekteki (OB) ham barların üzerine çizer. Çizilenle sayılan arasında fark olamaz; ikisi aynı sayılardır.

Her işlem için:
  • PNG   : {K}/teshis/{ad}_{sıra:04d}_{sembol}_{giriş}.png — mumlar (segment öncesi 40 bar bağlam + segment + ileri),
            segment gölgeli, taban/tavan/kırılım çizgisi, sinyal günü, kırılım barı, giriş (ertesi açılış), hedef (+%20),
            SMA20, hedef vuruş barı, çıkış barı; başlıkta sayılar.
  • CSV   : {K}/teshis/{ad}_{sıra:04d}_{sembol}_{giriş}_barlar.csv — bar bar tarih, O/H/L/C, SMA20, rol (segment/sinyal/kırılım/giriş/hedef/çıkış)
  • Özet  : {K}/teshis/{ad}_ozet.csv — seçilen işlemlerin sayıları tek tabloda (ekrana da basılır)

    exec(open(K + "/islem_goster.py", encoding="utf-8").read())
    q, _ = islemler(OB, 'acilis')                                 # DENETIM'in işlem tablosu (aynı sıra)
    islem_goster(K, OB, [48, 57, 69, 102, 125, 200, 400], 'v2_2024_26', islemler, VERI)
    islem_goster(K, OB, 'rastgele:8', 'v2_2024_26', islemler, VERI)            # rastgele 8 işlem
    islem_goster(K, OB, [('ERSU', '2025-03-13')], 'v2_2024_26', islemler, VERI) # sembol + giriş günü
"""
from __future__ import annotations

import logging
import os
import sys
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd

IG_SURUM = "1.0"
IG_BAGLAM = 40            # segment öncesi gösterilen bar
IG_SONRA = 10             # çıkıştan sonra gösterilen bar
IG_HEDEF = 20             # DENETIM.DN_HEDEF ile aynı (yalnız çizim; sayılar DENETIM'den gelir)
IG_MALIYET = 0.4

_ig_log = logging.getLogger("islem_goster")
if not _ig_log.handlers:
    _h = logging.StreamHandler(sys.stdout); _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s ig: %(message)s", "%H:%M:%S"))
    _ig_log.addHandler(_h); _ig_log.setLevel(logging.INFO)


# ---------------------------------------------------------------- bir işlemin bar tablosu
def ig_barlar(r: Any, veri: Optional[Dict[str, pd.DataFrame]] = None, baglam: int = IG_BAGLAM, sonra: int = IG_SONRA) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """islemler() satırından (r.o önbellek kaydı, r.e giriş, r.jt çıkış) tek bir bar tablosu kurar.
    rol: baglam | segment | sinyal (segmentin son barı) | kirilim | giris | hedef | cikis | ileri"""
    o = r.o if hasattr(r, "o") else r["o"]
    e = int(r.e if hasattr(r, "e") else r["e"]); jt = int(r.jt if hasattr(r, "jt") else r["jt"])
    gp = float(r.gp if hasattr(r, "gp") else r["gp"]); cp = float(r.cp if hasattr(r, "cp") else r["cp"])
    seg = pd.DataFrame({"T": pd.to_datetime(o["sT"]), "O": o["sO"], "H": o["sH"], "L": o["sL"], "C": o["sC"]})
    seg["rol"] = "segment"; seg.loc[seg.index[-1], "rol"] = "sinyal"; seg["s20"] = np.nan
    ns = min(len(o["iT"]), jt + 1 + sonra)
    il = pd.DataFrame({"T": pd.to_datetime(o["iT"][:ns]), "O": o["iO"][:ns], "H": o["iH"][:ns], "L": o["iL"][:ns], "C": o["iC"][:ns], "s20": o["s20"][:ns]})
    il["rol"] = "ileri"
    tavan = float(np.maximum(o["sO"], o["sC"]).max()); kir = tavan * 1.002
    # kırılım barı: DENETIM._kirilim ile aynı tanım — ileri içinde ilk kapanış > tavan×1.002 (60 bar içinde)
    kb = next((j for j in range(min(60, len(o["iC"]))) if o["iC"][j] > kir), None)
    if kb is None:
        raise ValueError(f"{o['sembol']}: kırılım barı bulunamadı; islemler() bu kaydı nasıl saydı?")
    def _ekle(j, rol):
        il.loc[j, "rol"] = rol if il.loc[j, "rol"] == "ileri" else il.loc[j, "rol"] + "+" + rol
    _ekle(kb, "kirilim"); _ekle(e, "giris")
    hedef = gp * (1 + IG_HEDEF / 100); jh = None
    m = o["iH"][e + 1: jt + 1] >= hedef
    if m.any():
        jh = int(np.argmax(m)) + e + 1; _ekle(jh, "hedef")
    _ekle(jt, "cikis")
    onc = pd.DataFrame(columns=seg.columns)
    if veri is not None and o["sembol"] in veri and baglam > 0:
        df = veri[o["sembol"]]; x = df[df.index < seg["T"].iloc[0]].tail(baglam)
        onc = pd.DataFrame({"T": x.index, "O": x["Open"].to_numpy(float), "H": x["High"].to_numpy(float), "L": x["Low"].to_numpy(float), "C": x["Close"].to_numpy(float)})
        onc["rol"] = "baglam"; onc["s20"] = np.nan
    B = pd.concat([onc, seg, il], ignore_index=True)
    if jh is None:
        cikis_neden = "hedef vurulmadı, ufuk doldu (120 bar)" if jt == e + 120 else "hedef vurulmadı, veri sonu"
    elif np.isfinite(o["s20"][jt]) and o["iC"][jt] < o["s20"][jt]:
        cikis_neden = "hedef sonrası SMA20 altına kapanış (trail)"
    else:
        cikis_neden = "hedef vuruldu, trail tetiklenmedi, veri sonu"
    bilgi = {"sembol": o["sembol"], "sinyal_gunu": seg["T"].iloc[-1].date(), "segment_bas": seg["T"].iloc[0].date(), "segment_bar": len(seg),
             "taban": float(np.min(o["sL"])), "tavan": tavan, "kirilim_esigi": kir,
             "kirilim_gunu": il["T"].iloc[kb].date(), "kirilim_kapanis": float(o["iC"][kb]), "kirilim_kacinci_bar": kb + 1,
             "giris_gunu": il["T"].iloc[e].date(), "giris_fiyat": gp, "hedef_fiyat": hedef,
             "hedef_gunu": il["T"].iloc[jh].date() if jh is not None else None, "hedef_vuruldu": jh is not None,
             "cikis_gunu": il["T"].iloc[jt].date(), "cikis_fiyat": cp, "cikis_sma20": float(o["s20"][jt]) if np.isfinite(o["s20"][jt]) else np.nan,
             "cikis_neden": cikis_neden, "tutus_bar": jt - e,
             "getiri_ham": (cp / gp - 1) * 100, "getiri_net": (cp / gp - 1) * 100 - IG_MALIYET,
             "en_yuksek_tutusta": float(np.max(o["iH"][e: jt + 1])), "en_dusuk_tutusta": float(np.min(o["iL"][e: jt + 1]))}
    return B, bilgi


# ---------------------------------------------------------------- çizim
def ig_ciz(B: pd.DataFrame, bilgi: Dict[str, Any], yol: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    n = len(B); x = np.arange(n)
    fig, ax = plt.subplots(figsize=(16, 7.5), dpi=110)
    yuk = B["C"].to_numpy(float) >= B["O"].to_numpy(float)
    ax.vlines(x, B["L"], B["H"], color=np.where(yuk, "#2e7d32", "#c62828"), linewidth=0.9)
    govde = (B["C"] - B["O"]).abs().to_numpy(float); govde = np.where(govde > 0, govde, (B["H"] - B["L"]).to_numpy(float) * 0.02)
    ax.bar(x, govde, bottom=np.minimum(B["O"], B["C"]), width=0.65,
           color=np.where(yuk, "#66bb6a", "#ef5350"), edgecolor=np.where(yuk, "#2e7d32", "#c62828"), linewidth=0.5)
    seg_i = np.where(B["rol"].isin(["segment", "sinyal"]))[0]
    if len(seg_i):
        ax.axvspan(seg_i[0] - 0.5, seg_i[-1] + 0.5, color="#ffe082", alpha=0.35, label=f"ÇÖL SEGMENTİ {bilgi['segment_bas']} → {bilgi['sinyal_gunu']} ({bilgi['segment_bar']} bar)")
        ax.hlines(bilgi["taban"], seg_i[0] - 0.5, n - 1, color="#6d4c41", linestyle="--", linewidth=1.2, label=f"taban {bilgi['taban']:.2f}")
        ax.hlines(bilgi["tavan"], seg_i[0] - 0.5, n - 1, color="#e65100", linestyle="--", linewidth=1.2, label=f"tavan (gövde) {bilgi['tavan']:.2f}")
        ax.hlines(bilgi["kirilim_esigi"], seg_i[0] - 0.5, n - 1, color="#e65100", linestyle=":", linewidth=1.0, label=f"kırılım eşiği tavan×1.002 = {bilgi['kirilim_esigi']:.2f}")
        ax.axvline(seg_i[-1], color="#9e9e9e", linestyle="-.", linewidth=1.0, label=f"sinyal günü {bilgi['sinyal_gunu']}")
    s20 = B["s20"].to_numpy(float); ok = np.isfinite(s20)
    if ok.any():
        ax.plot(x[ok], s20[ok], color="#1565c0", linewidth=1.3, label="SMA20 (trail)")
    def _isaret(rol_parca, renk, sekil, etiket, fiyat_kol="C"):
        i = np.where(B["rol"].str.contains(rol_parca))[0]
        if len(i):
            i = int(i[0]); ax.scatter([i], [float(B[fiyat_kol].iloc[i])], s=140, marker=sekil, color=renk, edgecolor="black", zorder=5, label=etiket)
            return i
        return None
    _isaret("kirilim", "#ff6f00", "^", f"KIRILIM {bilgi['kirilim_gunu']} kapanış {bilgi['kirilim_kapanis']:.2f} > {bilgi['kirilim_esigi']:.2f} ({bilgi['kirilim_kacinci_bar']}. bar)")
    gi = _isaret("giris", "#00c853", "o", f"GİRİŞ {bilgi['giris_gunu']} açılış {bilgi['giris_fiyat']:.2f}", "O")
    if gi is not None:
        ax.hlines(bilgi["giris_fiyat"], gi, n - 1, color="#00c853", linewidth=1.0, alpha=0.8)
        ax.hlines(bilgi["hedef_fiyat"], gi, n - 1, color="#7b1fa2", linestyle="--", linewidth=1.1, label=f"hedef +%20 = {bilgi['hedef_fiyat']:.2f}" + (f" (vuruldu {bilgi['hedef_gunu']})" if bilgi["hedef_vuruldu"] else " (vurulmadı)"))
    if bilgi["hedef_vuruldu"]:
        _isaret("hedef", "#7b1fa2", "*", "hedef vuruş barı", "H")
    _isaret("cikis", "#d50000", "v", f"ÇIKIŞ {bilgi['cikis_gunu']} kapanış {bilgi['cikis_fiyat']:.2f} — {bilgi['cikis_neden']}")
    adim = max(1, n // 14)
    ax.set_xticks(x[::adim]); ax.set_xticklabels([t.strftime("%Y-%m-%d") for t in B["T"].iloc[::adim]], rotation=45, ha="right", fontsize=8)
    ax.set_xlim(-1, n); ax.grid(alpha=0.25)
    net = bilgi["getiri_net"]
    ax.set_title(f"{bilgi['sembol']}  |  giriş {bilgi['giris_fiyat']:.2f} → çıkış {bilgi['cikis_fiyat']:.2f}  =  %{bilgi['getiri_ham']:+.1f} ham, %{net:+.1f} net (maliyet %{IG_MALIYET})  |  "
                 f"tutuş {bilgi['tutus_bar']} bar  |  tutuşta en yüksek {bilgi['en_yuksek_tutusta']:.2f} / en düşük {bilgi['en_dusuk_tutusta']:.2f}",
                 fontsize=10.5, color="#1b5e20" if net > 0 else "#b71c1c")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.92)
    fig.tight_layout(); fig.savefig(yol); plt.close(fig)


# ---------------------------------------------------------------- seçim
def ig_sec(q: pd.DataFrame, secim: Union[Sequence[Any], str], seed: int = 7) -> List[int]:
    """int → q satır numarası; (sembol, giriş günü) → eşleşen satır; 'rastgele:N' → N rastgele satır."""
    if isinstance(secim, str) and secim.startswith("rastgele:"):
        n = int(secim.split(":")[1]); rng = np.random.default_rng(seed)
        return sorted(int(i) for i in rng.choice(len(q), size=min(n, len(q)), replace=False))
    out: List[int] = []
    for s in secim:
        if isinstance(s, (int, np.integer)):
            if 0 <= int(s) < len(q):
                out.append(int(s))
            else:
                _ig_log.warning("satır %s yok (işlem sayısı %d)", s, len(q))
        else:
            sem, t = s; t = pd.Timestamp(t).normalize()
            m = q[(q["sembol"] == sem) & ((q["giris_t"] == t) | (q["cikis_t"] == t))]
            if m.empty:
                m = q[(q["sembol"] == sem) & (q["giris_t"] >= t)].head(1)
            if m.empty:
                _ig_log.warning("%s %s için işlem yok", sem, t.date())
            else:
                out.append(int(m.index[0]))
    return out


# ---------------------------------------------------------------- uçtan uca
def islem_goster(K: str, OB: List[Dict[str, Any]], secim: Union[Sequence[Any], str], ad: str, islemler: Callable,
                 veri: Any = None, giris: str = "acilis", ciz: bool = True) -> pd.DataFrame:
    """DENETIM.islemler(OB, giris) tablosundan seçilen işlemleri resim + bar tablosu olarak {K}/teshis/ altına yazar."""
    veri = veri["veri"] if isinstance(veri, dict) and isinstance(veri.get("veri"), dict) else veri
    q, bilgi_q = islemler(OB, giris)
    q = q.reset_index(drop=True)
    kl = os.path.join(K, "teshis"); os.makedirs(kl, exist_ok=True)
    idx = ig_sec(q, secim)
    _ig_log.info("%s: işlem tablosu %d satır (%s); seçilen %d", ad, len(q), bilgi_q, len(idx))
    S = []
    for i in idx:
        r = q.iloc[i]
        B, b = ig_barlar(r, veri)
        kok = f"{ad}_{i:04d}_{b['sembol']}_{b['giris_gunu']}"
        B.to_csv(os.path.join(kl, kok + "_barlar.csv"), index=False)
        if ciz:
            ig_ciz(B, b, os.path.join(kl, kok + ".png"))
        b = {"sira": i, **b, "denetim_getiri": float(r["g"]), "dosya": kok}; S.append(b)
        print(f"[{i}] {b['sembol']}: segment {b['segment_bas']}→{b['sinyal_gunu']} ({b['segment_bar']} bar) taban {b['taban']:.2f} tavan {b['tavan']:.2f} | "
              f"kırılım {b['kirilim_gunu']} kapanış {b['kirilim_kapanis']:.2f} > {b['kirilim_esigi']:.2f} | giriş {b['giris_gunu']} {b['giris_fiyat']:.2f} | "
              f"hedef {b['hedef_fiyat']:.2f} {'vuruldu ' + str(b['hedef_gunu']) if b['hedef_vuruldu'] else 'vurulmadı'} | "
              f"çıkış {b['cikis_gunu']} {b['cikis_fiyat']:.2f} ({b['cikis_neden']}) | {b['tutus_bar']} bar | %{b['getiri_net']:+.1f} (DENETIM: %{b['denetim_getiri']:+.1f})")
        if abs(b["getiri_net"] - float(r["g"])) > 0.05:
            _ig_log.warning("[%d] %s: gösterilen getiri ile DENETIM getirisi farklı (%.2f / %.2f) — bu bir çatlak, bildir", i, b["sembol"], b["getiri_net"], float(r["g"]))
    T = pd.DataFrame(S)
    if len(T):
        T.to_csv(os.path.join(kl, f"{ad}_ozet.csv"), index=False)
        print(f"\n→ {kl}/ : {len(T)} işlem için PNG + bar tablosu, özet {ad}_ozet.csv")
    return T
