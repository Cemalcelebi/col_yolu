"""K56 sürücüleri: sentetik (M01), faz0 (raporlar), erisim (küçük örneklem). Her koşu: kimlik (commit, kilit sha, kod sha), kaynak kaydı, çıktı yolu denetimi."""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import time
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from .ortak import K56Ayar, KaynakKaydi, cikti_dogrula, gunluk_log, kosu_kimligi, log


def _json_yaz(yol: str, veri: Any) -> None:
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=1, default=str)


def _spek_isci(arg):
    spek, hucreler, A = arg
    from . import mekanizma as M
    kk = KaynakKaydi(); S, _ = M.secim_sentetik(A, kk, hucreler, spekler=(spek,)); return S


def sentetik_kos(A: K56Ayar, isci: int = 4, hucreler: Optional[List[str]] = None) -> Dict[str, Any]:
    from . import mekanizma as M
    gunluk_log(); A.cikti = cikti_dogrula(A.cikti); os.makedirs(A.cikti, exist_ok=True); t0 = time.time()
    kimlik = kosu_kimligi(A, "SENTETIK"); kk = KaynakKaydi()
    from K55.faz1 import hucreleri_kur
    hucreleri_kur(); T = M.k55_hucre_varyantlari(A, kk)
    if hucreler:
        T = T[T.hucre.isin(hucreler)].reset_index(drop=True)
    log.info("M01 sentetik: %d hücre × %d spek; kimlik %s", len(T), len(M.SENTETIK_SPEK), kimlik["kimlik"])
    args = [(s, list(T.hucre), A) for s in M.SENTETIK_SPEK]
    if isci > 1:
        with mp.get_context("fork").Pool(min(isci, len(args))) as hv:
            parca = hv.map(_spek_isci, args, chunksize=1)
    else:
        parca = [_spek_isci(a) for a in args]
    S = pd.concat(parca, ignore_index=True); Z = M.sentetik_ozet(S, T)
    S.to_csv(os.path.join(A.cikti, "K56_SECIM_SENTETIK.csv"), index=False); Z.to_csv(os.path.join(A.cikti, "K56_SECIM_SENTETIK_OZET.csv"), index=False)
    kk.tablo().to_csv(os.path.join(A.cikti, "K56_KAYNAK_KAYDI_SENTETIK.csv"), index=False)
    _json_yaz(os.path.join(A.cikti, "K56_KOSU_SENTETIK.json"), {**kimlik, "sure_dk": round((time.time() - t0) / 60, 1), "hucre": len(T), "spek": M.SENTETIK_SPEK,
                                                                 "karar": Z.karar.value_counts().to_dict() if len(Z) else {}})
    log.info("M01 sentetik bitti: %.1f dk; karar %s", (time.time() - t0) / 60, Z.karar.value_counts().to_dict() if len(Z) else {})
    return {"S": S, "Z": Z, "kimlik": kimlik}


def faz0_kos(A: K56Ayar) -> Dict[str, Any]:
    raise NotImplementedError("faz0 raporları henüz bağlanmadı")


def erisim_kos(A: K56Ayar) -> Dict[str, Any]:
    raise NotImplementedError("erişim testi henüz bağlanmadı")
