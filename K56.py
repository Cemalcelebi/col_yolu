"""K56 — K51-K55 ETKİ VE MEKANİZMA ARAŞTIRMASI, tek giriş dosyası (Cemal, 30 Ekim 2026). Ön kayıt: K56/ONKAYIT_K56.md.

Komut:  python K56.py sentetik            (M01 olay başlangıcı seçim etkisi, sentetik sıfır sınaması; ağ yok)
        python K56.py faz0                (etki envanteri + açıklanmamış bulgular + hipotezler + veri kaynakları + yöntemler + riskler + sıra)
        SEC_EPOSTA=... python K56.py erisim   (küçük örneklem veri erişim testi; ağ açık, büyük indirme yok)
        python K56.py drive               (Colab: repodaki çıktıları Drive OUTPUT/K56_MEKANIZMA'ya sha doğrulamalı kopyala)
Colab:  exec(open('K56.py').read()); k56_faz0()
K51-K55 dosyaları yalnız okunur; çıktılar Drive COLAB_VERILER/OUTPUT/K56_MEKANIZMA (repoda arastirma_cikti/k56_mekanizma).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K56 = {k: id(v) for k, v in globals().items()}
KOK_K56 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K56 not in sys.path:
    sys.path.insert(0, KOK_K56)

from K56.ortak import K56Ayar, K56_SURUM  # noqa: E402


def k56_sentetik(cikti=None, isci=4, hucreler=None):
    """M01 sentetik sıfır sınaması (ONKAYIT_K56 6): dört yapay evren × K55 hücreleri; K56_SECIM_SENTETIK*.csv."""
    from K56.surucu import sentetik_kos
    A = K56Ayar(**({"cikti": cikti} if cikti else {}))
    return sentetik_kos(A, isci=int(isci), hucreler=hucreler)


def k56_sentetik_kesif(cikti=None, isci=4):
    """ONKAYIT_K56 v1.1-3: KEŞİF'i sağlayan bütün (varyant, ufuk) satırlarında sentetik sınama; K56_SECIM_SENTETIK_KESIF.csv."""
    from K56.surucu import sentetik_kesif_kos
    A = K56Ayar(**({"cikti": cikti} if cikti else {}))
    return sentetik_kesif_kos(A, isci=int(isci))


def k56_faz0(cikti=None):
    """Faz 0 raporları (ağ yok): envanter, açıklanmamışlar, hipotezler, veri kaynakları, yöntemler, riskler, sıra."""
    from K56.surucu import faz0_kos
    A = K56Ayar(**({"cikti": cikti} if cikti else {}))
    return faz0_kos(A)


def k56_erisim(cikti=None, ornek=12):
    """Küçük örneklem veri erişim testi (ağ açık; SEC_EPOSTA gerekli; büyük indirme yok)."""
    from K56.surucu import erisim_kos
    A = K56Ayar(**({"cikti": cikti} if cikti else {})); A.ag = True; A.ornek = int(ornek)
    return erisim_kos(A)


def k56_drive(kaynak=None, hedef=None):
    """Colab: repodaki K56 çıktılarını Drive COLAB_VERILER/OUTPUT/K56_MEKANIZMA'ya sha256 doğrulamalı kopyalar."""
    from K56.surucu import drive_kopyala
    return drive_kopyala(kaynak, hedef)


def _cakisma_kontrol_k56(_once=_CK_ONCE_K56, _dosya="K56.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka modülün) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K56", "_CK_KAYIT", "_cakisma_kontrol_k56", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit", "os", "sys", "annotations")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla and not (k.startswith("_i") and k[2:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k56()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=K56_SURUM); ap.add_argument("komut", choices=["sentetik", "sentetik_kesif", "faz0", "erisim", "drive"])
    ap.add_argument("--cikti", default=None); ap.add_argument("--isci", type=int, default=4); ap.add_argument("--hucreler", default=None); ap.add_argument("--ornek", type=int, default=12)
    a = ap.parse_args()
    if a.komut == "sentetik":
        k56_sentetik(a.cikti, a.isci, a.hucreler.split(",") if a.hucreler else None)
    elif a.komut == "sentetik_kesif":
        k56_sentetik_kesif(a.cikti, a.isci)
    elif a.komut == "faz0":
        k56_faz0(a.cikti)
    elif a.komut == "erisim":
        k56_erisim(a.cikti, a.ornek)
    else:
        k56_drive()
