"""test_mum_izi13 — MUM_IZI_GOZ2 testleri: set 5 ve birleşik örneklem sayıları, işaret çevirme permütasyonu, yön karşılaştırması, ek tanım mührü, çakışma kapısı.
Çalıştır: python test_mum_izi13.py"""
import json
import os
import subprocess
import sys

import numpy as np

import MUM_IZI_GOZ2 as G2


def test_ornek():
    if not os.path.exists(G2.G2_YOL["set5"][0]):
        print("  (set 5 işaretleri yok: atlandı)"); return
    X = G2.g2_ornek(); s5 = X[X.set == "set5"]
    assert len(s5) == 24 and s5.sinif.value_counts().to_dict() == {"EVET": 11, "KISMEN": 8, "HAYIR": 5} and len(X) == 128
    assert not X.duplicated(["zaman", "sembol", "tarih"]).any()


def test_isaret_perm():
    assert G2.g2_isaret_perm(np.full(20, 0.05) + np.linspace(-0.001, 0.001, 20), 2000, 1) < 0.01
    rng = np.random.default_rng(3); assert G2.g2_isaret_perm(rng.normal(0, 1, 40), 2000, 1) > 0.05
    assert G2.g2_isaret_perm(np.array([0.1]), 100, 1) is None


def test_yon():
    def T(k):
        return {"karsilastirma": {f"EVET-HAYIR|{z}": {"esli_fark_fark": k[z]} for z in ("gunluk", "haftalik")}}
    J = {"ilk_bakis": {"tablo": T({"gunluk": 0.05, "haftalik": -0.15})}, "ikinci_bakis": {"tablo": T({"gunluk": -0.02, "haftalik": -0.03}),
         "evet_es": {"EVET-es|gunluk": {"esli_fark_ort": 0.01}, "EVET-es|haftalik": {"esli_fark_ort": 0.02}}},
         "ilk_bakis_evet_es": {"EVET-es|gunluk": {"esli_fark_ort": 0.03}, "EVET-es|haftalik": {"esli_fark_ort": -0.16}}}
    Y = G2.g2_yon(J)
    assert Y["gunluk"]["EVET-HAYIR_esli"]["ayni_yon"] is False and Y["haftalik"]["EVET-HAYIR_esli"]["ayni_yon"] is True
    assert Y["gunluk"]["EVET-es"]["ayni_yon"] is True and Y["haftalik"]["EVET-es"]["ayni_yon"] is False


def test_ek_sabit():
    assert G2.g2_ek_sha() == G2.g2_ek_sha() and G2.G2_EK["evet_es"]["perm"] == 10000 and "GZ_ESIK aynen" in G2.G2_EK["tanim"]


def test_cakisma_kapisi():
    kod = ("import MUM_IZI_GOZ2 as M\nns = dict(vars(M))\nns['g2_yon'] = 1\nns['_CK_ONCE_G2'] = {'g2_yon': id(M.g2_yon)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_g2()')[0] + '_cakisma_kontrol_g2()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(G2.__file__)))
    assert "KAPALI" in r.stdout, (r.stdout, r.stderr[-500:])


if __name__ == "__main__":
    adlar = [k for k in list(globals()) if k.startswith("test_")]
    hata = 0
    for k in adlar:
        try:
            globals()[k](); print("GEÇTİ", k)
        except Exception as ex:   # her test ayrı raporlanır
            hata += 1; print("KALDI", k, type(ex).__name__, ex)
    print(f"{len(adlar) - hata} / {len(adlar)} geçti")
    sys.exit(1 if hata else 0)
