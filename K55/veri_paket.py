"""K55 veri paketi: islenmis-veri dalına sürümlü veri koyma / açma (Cemal, 30 Ekim 2026: kaynak, indirme tarihi, veri dönemi, sürüm, sha256,
işleme kodu sürümü her dosyayla birlikte; her oturumda yeniden indirme yok; bütünlük doğrulanmadan kullanılmaz; ham ve işlenmiş ayrı).

Düzen: <klasör>/manifest.json + <ad>.xz.NNN parçaları (45 MB; GitHub sınırı). manifest: paket sürümü, oluşturma, dosya başına meta
(kaynak, indirme_tarihi, donem, surum, sha256 (orijinal), boy, isleme_kodu, tur: ham | islenmis) ve parça sha256'ları.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from typing import Any, Dict, List

from .ortak import K55_SURUM, sha256_dosya


def paketle(kaynak: Dict[str, Dict[str, Any]], hedef: str, parca_mb: int = 45) -> Dict[str, Any]:
    """kaynak: paket adı -> {yol, kaynak, indirme_tarihi, donem, surum, isleme_kodu, tur}. Var olan paket yeniden yazılır."""
    os.makedirs(hedef, exist_ok=True)
    for eski in [f for f in os.listdir(hedef) if ".xz." in f or f == "manifest.json"]:
        os.unlink(os.path.join(hedef, eski))
    man: Dict[str, Any] = {"paket_surum": K55_SURUM, "olusturma": time.strftime("%Y-%m-%d %H:%M:%S"), "veri": {}, "parcalar": {}}; boy = parca_mb * 1024 * 1024
    for ad, meta in kaynak.items():
        yol = meta["yol"]
        if not os.path.exists(yol):
            raise FileNotFoundError(f"paket kaynağı yok: {ad} -> {yol}")
        xz = subprocess.Popen(["xz", "-T0", "-6", "-c", yol], stdout=subprocess.PIPE); no = 0
        while True:
            blok = xz.stdout.read(boy)
            if not blok:
                break
            with open(os.path.join(hedef, f"{ad}.xz.{no:03d}"), "wb") as f:
                f.write(blok)
            no += 1
        if xz.wait() != 0:
            raise RuntimeError(f"xz hatası: {ad}")
        man["veri"][ad] = {"boy": os.path.getsize(yol), "sha256": sha256_dosya(yol), "parca": no, **{k: v for k, v in meta.items() if k != "yol"}}
    for ad in sorted(os.listdir(hedef)):
        if ".xz." in ad:
            man["parcalar"][ad] = {"boy": os.path.getsize(os.path.join(hedef, ad)), "sha256": sha256_dosya(os.path.join(hedef, ad))}
    with open(os.path.join(hedef, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    return man


def ac(kaynak: str, hedef: str, beklenen_sha: Dict[str, str] = None) -> Dict[str, Dict[str, Any]]:
    """Paketi açar: her parça sha256 ile doğrulanır, açılan dosyanın sha256'sı manifestteki orijinal sha256 ile karşılaştırılır (tutmazsa durur).
    beklenen_sha verilirse (ad -> sha256) manifest de ona karşı doğrulanır (sürüm kilidi). Dönüş: ad -> {yol, meta}."""
    with open(os.path.join(kaynak, "manifest.json"), encoding="utf-8") as f:
        man = json.load(f)
    for ad, b in man["parcalar"].items():
        yol = os.path.join(kaynak, ad)
        if not os.path.exists(yol):
            raise FileNotFoundError(f"paket parçası eksik: {ad}")
        if sha256_dosya(yol) != b["sha256"]:
            raise RuntimeError(f"paket parçası bozuk: {ad}")
    os.makedirs(hedef, exist_ok=True); out = {}
    for ad, meta in man["veri"].items():
        if beklenen_sha and ad in beklenen_sha and beklenen_sha[ad] != meta["sha256"]:
            raise RuntimeError(f"veri sürümü beklenenden farklı: {ad} (manifest {meta['sha256'][:12]}, beklenen {beklenen_sha[ad][:12]})")
        yol = os.path.join(hedef, ad)
        if os.path.exists(yol) and sha256_dosya(yol) == meta["sha256"]:
            out[ad] = {"yol": yol, "meta": meta}; continue                 # zaten açık ve doğru
        with open(yol, "wb") as g:
            xz = subprocess.Popen(["xz", "-d", "-c"], stdin=subprocess.PIPE, stdout=g)
            for no in range(meta["parca"]):
                with open(os.path.join(kaynak, f"{ad}.xz.{no:03d}"), "rb") as f:
                    xz.stdin.write(f.read())
            xz.stdin.close()
            if xz.wait() != 0:
                raise RuntimeError(f"xz açma hatası: {ad}")
        if sha256_dosya(yol) != meta["sha256"]:
            raise RuntimeError(f"açılan dosya sha256 tutmuyor: {ad}")
        out[ad] = {"yol": yol, "meta": meta}
    return out


def manifest_ozet(kaynak: str) -> List[Dict[str, Any]]:
    with open(os.path.join(kaynak, "manifest.json"), encoding="utf-8") as f:
        man = json.load(f)
    return [{"ad": ad, **{k: v for k, v in m.items() if k != "parca"}} for ad, m in man["veri"].items()]
