"""K55 — DALLANMALI İZ ARAMA, tek giriş dosyası (Cemal, 30 Ekim 2026: K55/ klasöründe bağımsız modüller + bu giriş).

Colab:  exec(open('K55.py').read()); R = k55_faz0(ornek=50)        (CY_VERI ortam değişkeni ya da K55Ayar(veri=...) ile veri klasörü)
Komut:  python K55.py faz0 --ornek 50 --veri /tmp/veri --cikti arastirma_cikti/k55_dallanma
Ön kayıt ve kilit: K55/ONKAYIT_K55.md. Eski K51-K54 dosyaları değiştirilmez (COL_YOLU_ABD yalnız içe aktarılır).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K55 = {k: id(v) for k, v in globals().items()}
KOK_K55 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K55 not in sys.path:
    sys.path.insert(0, KOK_K55)

from K55.ortak import K55Ayar, K55_SURUM  # noqa: E402
from K55.faz0 import faz0  # noqa: E402


def k55_faz0(ornek=None, veri=None, cikti=None, isci=None, tohum=55, paketler=None):
    """Faz 0: evren + veri kalitesi + ortak panel + olaylar + sızıntı testleri + hücre iskelesi + rapor. ornek=50 deneme, None tam evren."""
    kw = {"ornek": ornek, "tohum": tohum}
    if veri:
        kw["veri"] = veri
    if cikti:
        kw["cikti"] = cikti
    if isci:
        kw["isci"] = int(isci)
    return faz0(K55Ayar(**kw), paketler)


def _cakisma_kontrol_k55(_once=_CK_ONCE_K55, _dosya="K55.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka modülün) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K55", "_CK_KAYIT", "_cakisma_kontrol_k55", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit", "os", "sys", "annotations")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla and not (k.startswith("_i") and k[2:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k55()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=K55_SURUM); ap.add_argument("komut", choices=["faz0"]); ap.add_argument("--ornek", type=int, default=None)
    ap.add_argument("--veri", default=None); ap.add_argument("--cikti", default=None); ap.add_argument("--isci", type=int, default=None); ap.add_argument("--tohum", type=int, default=55)
    a = ap.parse_args()
    if a.komut == "faz0":
        k55_faz0(ornek=a.ornek, veri=a.veri, cikti=a.cikti, isci=a.isci, tohum=a.tohum)
