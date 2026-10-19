# -*- coding: utf-8 -*-
"""
VERİ KORU v1.0 — veri yenilendikten sonra bölünme/bedelsiz onarımını VERI'ye yeniden uygular
=============================================================================================
Sorun (9 Eki 2026 teşhisi): BASLAT.veri_yenile, son 15 günde eski/yeni kapanış %0,5'ten fazla ayrışınca hisseyi Yahoo'dan BAŞTAN ve
HAM indirir (B2). Ham Yahoo serisinde BIST bedelsizleri düzeltilmemiştir → bolunme_onar'ın yaptığı onarım silinir (teşhis: 31 olayda
sahte −%50 sıçrama geri geldi, 323 hisse baştan indi). Onarım tek seferlik yazılmıştı, yenilemeye bağlanmamıştı.

Çözüm (en basit tek yol): her BASLAT'ta veri_yenile'den hemen sonra bütün VERI'de bo_bul → bo_onar (bolunme_onar.py v1.2 kuralları,
kapanış doğrulaması dahil). Onarım veriye bakarak çalışır, bu yüzden:
  - zaten onarılmış seri: sıçrama yok → dokunulmaz (iki kez onarılmaz),
  - Yahoo'nun kendisi düzelttiği seri: sıçrama yok → dokunulmaz,
  - ham inmiş seri: sıçrama var → onarılır, pkl yazılır.
Ek teşhis: B2'nin hangi tarihteki farkla tetiklendiği BASLAT yamasıyla B2_NEDEN'e yazılır; burada özetlenir (neden 323 hisse indi
sorusunun cevabı bir sonraki koşuda sayıyla görünür; şimdilik "doğrulanamadı").

    exec(open(K + "/veri_koru.py", encoding="utf-8").read())
    VK = veri_koru(K, VERI, B2_NEDEN)        # BASLAT yaması bunu veri_yenile()'den hemen sonra çağırır
    yeni_metin, degisti = baslat_yama(open(K + "/BASLAT.py").read())
"""
from __future__ import annotations

import logging
import os
import pickle
import sys
import time
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

VK_SURUM = "1.0"
VK_ISARET = "# VK_YAMA v1.0"
VK_SICRAMA_ALT = 0.62   # kapanıştan kapanışa bu oranın altı / VK_SICRAMA_UST üstü: BIST ±%10 limitiyle olamaz → kalan sıçrama (öz-denetim)
VK_SICRAMA_UST = 1.60
_vk_log = logging.getLogger("veri_koru")
if not _vk_log.handlers:
    _h = logging.StreamHandler(sys.stdout)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s veri_koru: %(message)s", "%H:%M:%S"))
    _vk_log.addHandler(_h)
_vk_log.setLevel(logging.INFO)
_vk_log.propagate = False

# ---------------------------------------------------------------- BASLAT.py yaması (eski kod korunur, yalnız 4 yere ekleme)
VK_CAPALAR: List[Tuple[str, str, str]] = [
    ("B2_NEDEN tanımı",
     "def veri_yenile(gun=15, zorla=False, sapma=0.005):\n",
     "B2_NEDEN = {}   " + VK_ISARET + " (veri_koru: yenileme sonrası bölünme onarımı + B2 nedeni)\n"
     "def veri_yenile(gun=15, zorla=False, sapma=0.005):\n"),
    ("B2_NEDEN sıfırlama",
     "    semboller=[s+'.IS' for s in VERI]; guncel=0; hata=0; bastan=[]; t0=time.time()\n",
     "    semboller=[s+'.IS' for s in VERI]; guncel=0; hata=0; bastan=[]; t0=time.time(); B2_NEDEN.clear()\n"),
    ("B2 farkının tarihi",
     "                        bastan.append(k); continue\n",
     "                        _i=int(np.nanargmax(np.abs(y_c[m]/e_c[m]-1))); B2_NEDEN[k]=(str(ort[m][_i].date()), float(y_c[m][_i]/e_c[m][_i]), str(eski.index[-1].date()))\n"
     "                        bastan.append(k); continue\n"),
    ("veri_koru çağrısı",
     "veri_yenile()\nexec(open(f'{K}/COL_v1.py').read())\n",
     "veri_yenile()\nexec(open(f'{K}/veri_koru.py', encoding='utf-8').read()); VK = veri_koru(K, VERI, B2_NEDEN)\n"
     "exec(open(f'{K}/COL_v1.py').read())\n"),
]


def baslat_yama(metin: str) -> Tuple[str, bool]:
    """BASLAT metnine 4 ekleme yapar. Zaten yamalıysa dokunmaz (False). Her çapa TAM BİR kez bulunmalı, yoksa ValueError (sessiz yama yok)."""
    if VK_ISARET in metin:
        return metin, False
    yeni = metin
    for ad, capa, yerine in VK_CAPALAR:
        n = yeni.count(capa)
        if n != 1:
            raise ValueError(f"BASLAT yaması: '{ad}' çapası {n} kez bulundu (1 olmalı) — BASLAT.py beklenen sürüm değil, yama yapılmadı")
        yeni = yeni.replace(capa, yerine)
    compile(yeni, "BASLAT.py", "exec")
    return yeni, True


# ---------------------------------------------------------------- B2 nedeni özeti
def vk_b2_ozet(b2: Optional[Dict[str, Tuple[str, float, str]]]) -> Dict[str, Any]:
    """B2_NEDEN {sembol: (fark_tarihi, yeni/eski oran, eski_son_bar)} → kaç hisse, farkın en sık tarihleri, kaçında fark eski serinin SON barında."""
    b2 = b2 or {}
    if not b2:
        return {"n": 0, "tarihler": [], "son_barda": 0, "oran_ornek": {}}
    tar = Counter(v[0] for v in b2.values())
    son_barda = sum(1 for v in b2.values() if v[0] == v[2])
    return {"n": len(b2), "tarihler": tar.most_common(5), "son_barda": int(son_barda),
            "oran_ornek": {s: round(v[1], 4) for s, v in list(b2.items())[:8]}}


# ---------------------------------------------------------------- kalan kapanış sıçraması (öz-denetim)
def vk_kalan_sicrama(VERI: Dict[str, pd.DataFrame]) -> List[Tuple[str, str, float]]:
    out: List[Tuple[str, str, float]] = []
    for s, df in VERI.items():
        try:
            C = pd.to_numeric(df["Close"], errors="coerce").to_numpy(float)
            if len(C) < 2:
                continue
            with np.errstate(divide="ignore", invalid="ignore"):
                r = C[1:] / C[:-1]
            for i in np.flatnonzero(np.isfinite(r) & ((r <= VK_SICRAMA_ALT) | (r >= VK_SICRAMA_UST))):
                out.append((s, str(pd.Timestamp(df.index[i + 1]).date()), float(r[i])))
        except Exception as e:
            _vk_log.warning("%s kalan sıçrama: %s", s, e)
    return out


# ---------------------------------------------------------------- ana iş
def veri_koru(K: str, VERI: Dict[str, pd.DataFrame], b2_neden: Optional[Dict[str, Any]] = None, kaydet: bool = True,
              veri_ad: str = "veri_1d_turkey.pkl") -> Dict[str, Any]:
    g = globals()
    if "bo_bul" not in g or "bo_onar" not in g:
        yol_bo = os.path.join(K, "bolunme_onar.py")
        if not os.path.exists(yol_bo):
            raise FileNotFoundError(f"{yol_bo} yok — veri_koru onarım yapamaz")
        exec(open(yol_bo, encoding="utf-8").read(), g)
    t0 = time.monotonic(); satir: List[Dict[str, Any]] = []; degisen = 0; dokunulmayan = 0
    for s in list(VERI.keys()):
        df = VERI[s]
        try:
            ol = g["bo_bul"](df)
            if not ol:
                continue
            yeni, kayit = g["bo_onar"](df, ol)
            on = [r for r in kayit if r["onarildi"]]
            dokunulmayan += len(kayit) - len(on)
            if on:
                VERI[s] = yeni; degisen += 1
                for r in on:
                    satir.append({"zaman": str(pd.Timestamp.now()), "sembol": s, "tarih": str(pd.Timestamp(r["tarih"]).date()), "oran": float(r["oran"])})
        except Exception as e:
            _vk_log.warning("%s: %s", s, e)
    yazildi = False
    if degisen and kaydet:
        yol = os.path.join(K, veri_ad); tmp = yol + ".vk.tmp"
        with open(tmp, "wb") as f:
            pickle.dump(VERI, f)
        os.replace(tmp, yol); yazildi = True
        gunluk = os.path.join(K, "veri_koru_gunluk.csv")
        pd.DataFrame(satir).to_csv(gunluk, mode="a", header=not os.path.exists(gunluk), index=False)
    kalan = vk_kalan_sicrama(VERI)
    b2 = vk_b2_ozet(b2_neden)
    print(f"VERİ KORU v{VK_SURUM}: {len(VERI)} hisse | {degisen} hissede {len(satir)} bölünme/bedelsiz onarıldı (ham inen seri) | "
          f"{dokunulmayan} açılış hatası/şüpheli dokunulmadı | {'pkl yazıldı' if yazildi else 'pkl değişmedi'} | {time.monotonic() - t0:.0f}s")
    if satir:
        print("  onarılan: " + "; ".join(f"{r['sembol']} {r['tarih']} ×{r['oran']:.3f}" for r in satir[:20]) + (" ..." if len(satir) > 20 else ""))
    print(f"  kalan kapanış sıçraması (≤{VK_SICRAMA_ALT} / ≥{VK_SICRAMA_UST}): {len(kalan)}"
          + (" → " + "; ".join(f"{s} {t} {r:.3f}" for s, t, r in kalan[:12]) if kalan else ""))
    if b2["n"]:
        print(f"  B2 nedeni: {b2['n']} hisse baştan indi | fark tarihleri: {b2['tarihler']} | farkı eski serinin SON barında olan: {b2['son_barda']}"
              f" | yeni/eski oran örnek: {b2['oran_ornek']}")
    return {"degisen_hisse": degisen, "onarilan": satir, "dokunulmayan": dokunulmayan, "kalan": kalan, "b2": b2, "yazildi": yazildi}
