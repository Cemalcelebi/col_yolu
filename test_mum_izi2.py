"""test_mum_izi2 — MUM_IZI2 testleri (gerçek fiyat verisi yok): ENSRI sayısallaştırması = elle sayım, TL kalibrasyonu, yüzdelik ve sınıf
kuralları, birleşik kural eşiği, kapı ve çakışma kapısı. Çalıştır: python test_mum_izi2.py"""
import os
import subprocess
import sys
import tempfile

import numpy as np

import MUM_IZI2 as M2

# ENSRI görüntüsünden ELLE sayım (soldan sağa): 1 Y, 2 K (ince gövde), 3 K, 4 Y, 5 K, 6 K (doji çizgisi), 7 K, 8 K, 9 Y, 10 Y (ince), 11 Y (ince),
# 12 Y (grafik sağ kenarında hafif kırpık). İlk iki mumda alt bant çizgisi fiyat panelinin altında (görünmüyor).
ELLE_RENK = "YKKYKKKKYYYY"


def _D():
    if not hasattr(_D, "c"):
        _D.c = M2.mi2_sayisallastir()
    return _D.c


def test_sayisallastirma_elle():
    D = _D(); T = D["tablo"]
    assert D["n"] == 12 and D["renk_dizisi"] == ELLE_RENK, (D["n"], D["renk_dizisi"])
    assert list(T[T.doji_cizgi.astype(bool)].i) == [6]
    assert D["alt_gorunmeyen"] == [1, 2]
    assert list(T[T.kenar != ""].i) == [12]
    assert 75 < D["izgara"]["b"] < 80
    # en uzun üst fitil 2. mumda; en düşük Low 8. mumda
    assert int(T.loc[(T.H - T[["O", "C"]].max(axis=1)).idxmax(), "i"]) == 2
    assert int(T.loc[T.L.idxmin(), "i"]) == 8


def test_kalibrasyon():
    K = _D()["kalibrasyon"]
    assert len(K["etiket_satir"]) == 13 and K["kesik_etiket"] == 1
    assert K["artik_tl_max"] < 0.01 and K["izgara_fark_px_max"] <= 2.0
    assert abs(K["px_tl"] - 124.8) < 1.0                    # 0,50 TL = 62,4 px


def test_yuzdelik_sinif():
    x = np.array([1, 2, 2, 3, 4], float)
    assert M2.mi2_yuzdelik(x, 2) == (1 + 0.5 * 2) / 5
    assert np.allclose(M2.mi2_yuzdelik_coklu(x, np.array([2.0, 0.0, 9.0])), [0.4, 0.0, 1.0])
    assert M2.mi2_sinif(0.95, 0.91) == "GÜÇLÜ ORTAK" and M2.mi2_sinif(0.05, 0.08) == "GÜÇLÜ ORTAK"
    assert M2.mi2_sinif(0.80, 0.95) == "ORTAK" and M2.mi2_sinif(0.2, 0.25) == "ORTAK"
    assert M2.mi2_sinif(0.80, 0.20) == "ZIT" and M2.mi2_sinif(0.6, 0.9) == "AYRI"


def test_kural_esik():
    k = {"q12": 1.0, "q20": 3.0}
    assert M2._mi2_kural_esik(k, 12) == 1.0 and M2._mi2_kural_esik(k, 20) == 3.0 and M2._mi2_kural_esik(k, 16) == 2.0


def test_ozellik_senaryo():
    T = _D()["tablo"]
    FE, FT = M2.mi2_ozellik(T, "E"), M2.mi2_ozellik(T, "T")
    assert len(FE) == 35 and all(np.isfinite(v) for v in FE.values())
    # alt bant yalnız 1-2. mumda farklı: bant içermeyen ölçüler iki senaryoda aynı
    for k in ("ust_fitil", "alt_fitil", "kapanis_egim", "yuk_dip_pay", "ust_bant_asim_pay", "pB_son"):
        assert FE[k] == FT[k], k


def test_kapi_kapali():
    with tempfile.TemporaryDirectory() as d:
        try:
            M2.mi2_kapi(d)
        except (M2.MI2Hata, FileNotFoundError):
            pass
        else:
            raise AssertionError("ön kayıtsız kapı açıldı")


def test_cakisma_kapisi():
    kod = ("import MUM_IZI2 as M\nns = dict(vars(M))\nns['mi2_sinif'] = 1\nns['_CK_ONCE_MI2'] = {'mi2_sinif': id(M.mi2_sinif)}\n"
           "src = open(M.__file__, encoding='utf-8').read()\n"
           "try:\n    exec(compile(src.split('_cakisma_kontrol_mi2()')[0] + '_cakisma_kontrol_mi2()', 'x', 'exec'), ns)\n"
           "    print('ACIK')\nexcept RuntimeError as e:\n    print('KAPALI' if 'çakışma kapısı' in str(e) else 'BASKA')\n")
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(M2.__file__)))
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
