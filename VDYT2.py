"""VDYT2 — VOLATİLİTE DENGE VE YÖN TAHMİNİ, SÜRÜM 2 (v2_20261112). Tek dosya, ayrı araştırma motoru (12 Kasım 2026; Cemal'in TEK ve DEĞİŞMEZ hedefi).

Hedef (Cemal): 'Sert düşüş veya önceki hareket -> küçük mumların oluşturduğu uzun sessiz bölge -> büyük mumlarla başlayan volatilite genişlemesi.' Sessiz bölgeyi
BÜYÜK HAREKET BAŞLAMADAN ÖNCE tespit et; büyük hareketin ne zaman başlayabileceğini, yönünü ve hangi özelliklerin doğru tahmin ihtimalini artırdığını belirle.
ÜÇ BAŞARI AYRI AYRI kanıtlanır: (1) bölgeyi önceden bulmak, (2) genişlemeyi önceden tahmin etmek, (3) yönü önceden tahmin etmek; basit piyasa kontrollerinden
daha iyi. Biri başarısızsa başarılı gibi sunulmaz; sonuç olumsuz olabilir.

VDYT sürüm 1'den dersler (zorunlu): D1 karar günü ancak büyük hareket henüz başlamamışsa geçerli; etiket yalnız t'den SONRA başlayan büyük hareketi sayar; aynı
model sıkışma DIŞI günlerde ve rastgele bölgelerde de koşulur. D2 'olgunlaşma' varsayılmaz, sınanır. D3 yön temeli B1 (piyasa 60 gün yönü; KARAR) + B2 (bölge içi
konum; mekanik, BİLGİ) + konum-dışı model. D4 olay bulgusu ancak WF + KASA + plasebo eşiğini geçerse sayılır. D5 grafik: küçük girdi paketi + yalnız paketten
çizen Colab komutu (VDYT_GRAFIK.py ve v1 paketine dokunulmaz).

SINIR: VDYT2, Çöl Yolu'nu, IZ_KARNE kararlarını, VDYT.py'yi ve v1 kayıt / çıktılarını DEĞİŞTİRMEZ; VDYT.py'nin veri yükleyicilerini, ölçü, olay ve model
fonksiyonlarını İÇE AKTARIR. Sonuç doğrulanmış sinyal değildir; yüksek olasılık alım sinyali değildir; ilişki nedensellik değildir.

Komut:  python -I VDYT2.py kapsam              YALNIZ SAYIM (bölge, geçerli karar günü, kontrol satırı, büyük hareket SAYISI); oran / yön / getiri / model YOK
        python VDYT2.py onkayit                ön kaydı yazar (eşik mührü + kod sha256 + VDYT.py sha256 + veri sha256 + kapsam; varsa üzerine yazmaz)
        python -I VDYT2.py kos --asama wf      ön kayıt + VDYT2.py + VDYT.py git'e işlenmiş, değişmemiş, mühür / kod / veri tutuyorsa ölçüm; yoksa REDDEDER
        python -I VDYT2.py kos --asama kasa    KASA (2024-01 -> 2026-08-31) BİR KEZ açılır (vdyt2_kasa_acildi.json; varsa ret)
        python -I VDYT2.py canli               her hisse için güncel durum (CANLI, test dışı); yalnız KASA'dan sonra; yön sınıfı KASA sonucuna bağlı
        python VDYT2.py paket --asama kasa     grafik girdi paketi (önceden tanımlı grup x tohumlu 5 örnek; dosya < 3 MB)
        python VDYT2.py ciz --paket KLASOR --cikti KLASOR   YALNIZ paketten çizer (Colab'da bağımsız; var olan PNG'nin üstüne yazmaz)
        python VDYT2.py rapor --asama wf|kasa  raporu sonuç JSON'undan yeniden yazar
Colab:  exec(open('VDYT2.py').read()); v2_ciz('<paket klasörü>', '<çıktı klasörü>')
Veri:   yalnız yerel, daha önce inmiş veri (VDYT_VERI_ENVANTERI.md + /tmp/k67_yahoo takvimi). Ağ yok. SEC'e istek yok; e-posta / anahtar yok.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_VDYT2 = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import glob  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_VDYT2 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_VDYT2 not in sys.path:
    sys.path.insert(0, KOK_VDYT2)
import VDYT as V1  # noqa: E402  (VDYT sürüm 1: veri yükleyicileri, ölçüler, olaylar, lojistik, bootstrap; DEĞİŞTİRİLMEZ)

vdyt2log = logging.getLogger("col.vdyt2")
if not vdyt2log.handlers:
    _v2_h = logging.StreamHandler(sys.stderr)
    _v2_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s vdyt2: %(message)s", "%H:%M:%S"))
    vdyt2log.addHandler(_v2_h)
    vdyt2log.setLevel(logging.INFO)
    vdyt2log.propagate = False

VDYT2_ETIKET = "v2_20261112"
VDYT2_SURUM = "VDYT2 v2.0 (v2_20261112): Faz 1 (ön kayıt, kod + sentetik test, yalnız sayım); ölçüm Faz 2'de, ön kayıt git'e işlendikten sonra"

VDYT2_YOL: Dict[str, str] = {
    "cikti": os.environ.get("VDYT2_CIKTI", os.path.join(KOK_VDYT2, "arastirma_cikti", "vdyt", VDYT2_ETIKET)),
    "ara": os.environ.get("VDYT2_ARA", "/tmp/vdyt2"),
    "k67_takvim": os.environ.get("VDYT2_K67", "/tmp/k67_yahoo/takvim"),
    "drive": "MyDrive/COLAB_VERILER/OUTPUT/VDYT/" + VDYT2_ETIKET,
}
VDYT2_DOSYA: Dict[str, str] = {
    "onkayit": "VDYT2_ON_KAYIT.md", "kapsam": "vdyt2_kapsam.json", "kapsam_md": "VDYT2_KAPSAM.md", "kasa": "vdyt2_kasa_acildi.json",
    "parametre": "vdyt2_parametre_kaydi.json", "meta": "vdyt2_meta.json",
}
_V2_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256 mührü ön kayıtta; sonuç görüldükten sonra değişmez)
VDYT2_ESIK: Dict[str, Any] = {
    "surum_etiket": VDYT2_ETIKET,
    "kesik": "2026-08-31",                         # fon krizi kesiği: test fiyatları burada kesilir (canlı çıktı hariç; 'CANLI, test dışı')
    "karar_pazari": ["BIST", "ABD"],
    "kontrol_pazari": ["BIST_K62"],                 # yalnız yanlılık kontrolü (kapanış verisi; kotasyondan çıkanlar dahil)
    "maliyet": {"BIST": 0.0030, "ABD": 0.0010, "BIST_K62": 0.0030},   # tek yön
    "atr_ref": {"n": 250, "min": 200},             # ATRref(t) = ort TR[t-L-249 .. t-L] (sessiz pencereden ÖNCEKİ 250 bar)
    "sessiz": {
        "L": 10,                                    # sessiz pencere (işlem günü)
        "G1": {"aralik_atr": [0.60, 0.50, 0.70], "govde_atr": 0.30, "maks_aralik_atr": 1.50, "doji": 0.10},
        "G2": {"bant_oran": [0.50, 0.40, 0.60], "gecmis_n": 250, "gecmis_min": 200},
        "G3": {"tepe_egim_ust": 0.0, "dip_egim_alt": 0.0},
        "G4": {"pencere": 20, "tabanlar": ["govde", "fitil", "kapanis"], "ana_taban": "govde", "kirilma_yok": True},
        "G5": "G1 VE G2 VE (G3 YA DA G4)",
        "olusuyor_en_az": 2,                        # canlı 'Sıkışma oluşuyor': {G1, G2, G3∨G4} üçünden en az 2'si
    },
    "tanim": {                                      # rol: ANA (tam analiz), AILE (G5 tabanı değişik: başarı 1 + 2 + 3 bilgi), ALT (yalnız başarı 1 + sayım)
        "G5": {"rol": "ANA", "durum": "G5", "devam": "G12", "min_kosu": 1}, "G5f": {"rol": "AILE", "durum": "G5f", "devam": "G12", "min_kosu": 1},
        "G5k": {"rol": "AILE", "durum": "G5k", "devam": "G12", "min_kosu": 1},
        "G1": {"rol": "ALT", "durum": "G1", "min_kosu": 1}, "G2": {"rol": "ALT", "durum": "G2", "min_kosu": 1},
        "G3": {"rol": "ALT", "durum": "G3", "min_kosu": 1}, "G4": {"rol": "ALT", "durum": "G4", "min_kosu": 1},
        "G1_e0.5": {"rol": "ALT", "durum": "G1_e1", "min_kosu": 1}, "G1_e0.7": {"rol": "ALT", "durum": "G1_e2", "min_kosu": 1},
        "G5_g0.4": {"rol": "ALT", "durum": "G5_b1", "devam": "G12_b1", "min_kosu": 1}, "G5_g0.6": {"rol": "ALT", "durum": "G5_b2", "devam": "G12_b2", "min_kosu": 1},
        "T1": {"rol": "ALT", "durum": "V1:T1", "min_kosu": 10}, "T2": {"rol": "ALT", "durum": "V1:T2", "min_kosu": 10},
        "T3": {"rol": "ALT", "durum": "V1:T3", "min_kosu": 10}, "T4": {"rol": "ALT", "durum": "V1:T4", "min_kosu": 10},
        "T5": {"rol": "ALT", "durum": "V1:T5", "min_kosu": 10},
    },
    "tanim_k62": {"G2K": {"rol": "K62", "durum": "G2", "min_kosu": 1}},   # BIST_K62: yalnız kapanış bandı (açılış / yüksek / düşük yok)
    "ana_tanim": "G5",
    "bolge": {"sonme_gun": 5},                      # açık bölge: durum 5 gün üst üste yanlış -> SÖNME
    "buyuk": {"k_b": 2.5, "m": 3.0, "ref_max": 60, "ref_min": 8, "onay_gun": 10, "tr_taban": 0.001, "govde_taban": 0.10},
    "gecerli": {"k_sessiz": 2.0, "gun": 3, "ref_max": 60},
    "onkosul": {"pencere": 120, "P1": -0.30, "P2": 0.30, "ana": "P1", "alt_kumeler": ["P0", "P1", "P2"]},
    "karar_yas": [10, 15, 20, 30, 45, 60, 90],
    "yas_kova": [[10, 14], [15, 19], [20, 29], [30, 44], [45, 59], [60, 89], [90, 100000]],
    "ufuk": [5, 10, 20], "ana_ufuk": 10, "basari1_ufuk": 20, "getiri_ufuk": [5, 10, 20], "mfe_ufuk": 20,
    "bhu": {"ref_n": 60, "ref_min": 40, "bant_n": 20, "tekil": 20},
    "kontrol": {"disari_kat": {"ANA": 5, "AILE": 2, "ALT": 2, "K62": 2}, "rastgele_kat": 2, "tohum": 20261115, "ilk_bar": 260,
                "hafif_bas": "2019-01-01"},          # ALT / K62 satırları ve AILE kontrolleri yalnız başarı 1'de: ilk WF test yılından önce etiketlenmez
    "wf": {"kesif_yillar": [2019, 2020, 2021, 2022, 2023], "kasa_yillar": [2024, 2025, 2026], "kasa": ["2024-01-01", "2026-08-31"],
           "wf_son": "2023-12-31",
           "kural": "her test yılı Y için eğitim = etiketi Y başından ÖNCE tamamlanmış satırlar (t + h + 9. bar < 1 Ocak Y); genişleyen pencere, yıllık yeniden eğitim"},
    "model": {"ridge": 1.0, "tur": 25, "tol": 1e-8, "winsor": [0.01, 0.99], "min_egitim": 200},
    "temel": {"G_T0": ["ay"], "G_T1": ["yas_kova", "ay"], "kucuk_hucre": 20, "Y_B0": 0.5, "Y_B1": ["pazar_yon"]},
    "basari": {"bootstrap": 2000, "tohum": 20261112, "guven": [2.5, 97.5], "kume": "hisse"},
    "coklu": {"bh_q": 0.10, "plasebo_olay_tekrar": 50, "plasebo_ust": 3000, "plasebo_esik_pct": 95.0, "tohum": 20261113},
    "olay": copy.deepcopy(V1.VDYT_ESIK["olay"]),
    "haber": {"haberli": [-5, 1], "habersiz": [-10, 1], "makro": [-1, 0]},
    "sinif": {"q_yuksek": 0.80, "yukari": 0.60, "asagi": 0.40, "basladi_gun": 3, "eski_veri_gun": 10,
              "guven_genisleme": {"ece_max": 0.03, "skill_min": 0.05}, "guven_yon": {"ece_max": 0.05, "ba_min": 0.05},
              "siniflar": ["Sıkışma yok", "Sıkışma oluşuyor", "Sıkışma devam ediyor", "Genişlemeye yaklaşan sıkışma", "Yukarı kırılma adayı",
                           "Aşağı kırılma adayı", "Yön belirsiz", "Genişleme başladı"]},
    "grafik": {"gruplar": ["BASARILI", "BASARISIZ", "KACIRILAN", "YON_DOGRU", "YON_YANLIS", "HABERSIZ"], "grup_n": 5, "tohum": 20261116,
               "on_bar": 60, "son_bar": 30, "dpi": 150, "paket_mb": 3.0, "boyut": [14, 8]},
    "savunma": copy.deepcopy(V1.VDYT_ESIK["savunma"]),
    "hisse_gecmis": {"min_bolge": 3},
    "donem_kapsam": [["2010-2015", "2010-01-01", "2015-12-31"], ["2016-2018", "2016-01-01", "2018-12-31"],
                     ["2019-2023 (WF test)", "2019-01-01", "2023-12-31"], ["2024-2026 (KASA)", "2024-01-01", "2026-08-31"]],
}

# Özellik grupları (tek model; ablasyon = grubu çıkar, tek grup = yalnız o grup). Hepsi yalnız t ve öncesi.
VDYT2_OZELLIK: Dict[str, List[str]] = {
    "SURE": ["yas_log", "yk_15", "yk_20", "yk_30", "yk_45", "yk_60", "yk_90"],
    "HISSE": ["hs_oran", "hs_yetersiz", "hs_bh_pay"],
    "REJIM": ["rj_pazar", "rj_sektor"],
    "ONCEKI": ["on_dusus120", "on_yukselis120", "on_p1", "on_p2"],
    "MUM": ["m_aralik_atr", "m_govde_atr", "m_govde_aralik", "m_fitil_ust_atr", "m_fitil_alt_atr", "m_doji_pay", "m_maks_aralik"],
    "BANT": ["b_kapanis_bant", "b_govde_bant", "b_bolge_bant_atr", "b_egim_tepe", "b_egim_dip"],
    "VOL": ["v_natr_oran", "v_rv_yuzde", "v_bbw_yuzde", "v_rv5_rv20", "v_tr_son3"],
    "HACIM": ["h_hacim_oran", "h_hacim_son5", "h_yukselen_hacim", "h_bolge_hacim"],
    "HAT": ["sv_hat_var", "sv_temas", "sv_korunma", "sv_kirilma", "sv_fitil_ihlal", "sv_son_test", "sv_hacim_test", "sv_yukselen_dip",
            "sv_alcalan_tepe", "sv_kapanis_ustu", "svf_hat_var", "svf_kirilma", "svk_hat_var", "svk_kirilma"],
    "KONUM": ["k_bolge_konum", "k_ust_mesafe_atr", "k_alt_mesafe_atr", "sv_mesafe"],
    "EMA": ["e_ema20", "e_ema50", "e_ema200", "e_sma50", "e_sma200", "e_sma50_egim", "e_ema20_50"],
    "FIYAT": ["f_ret20", "f_ret60", "f_likidite"],
    "OLAY": ["o_bilanco_gun", "o_bilanco_yok", "o_bilanco_son", "o_bilanco_bolgede", "o_makro_10", "o_olay_son5", "o_olay_son20", "o_olay_tepki"],
    "PAZAR": ["p_pazar_ret60", "p_pazar_ret20", "p_sektor_ret20"],
}
VDYT2_MODEL: Dict[str, Any] = {
    "genisleme": {"M_TAM": list(VDYT2_OZELLIK), "A_ORTAK": ["SURE"], "B_HISSE": ["SURE", "HISSE"], "C_REJIM": ["SURE", "REJIM"],
                  "D_ADAPTIF": ["SURE", "HISSE", "REJIM"]},
    "yon": {"M_TAM": list(VDYT2_OZELLIK), "M_KONUMSUZ": [g for g in VDYT2_OZELLIK if g != "KONUM"], "B2_KONUM": ["KONUM"]},
    "ablasyon": True, "tek_grup": True,
}

BIT_BUYUK, BIT_SONME, BIT_SANSUR = 1, 2, 3
BIT_AD = {BIT_BUYUK: "BUYUK_MUM", BIT_SONME: "SONME", BIT_SANSUR: "SANSUR"}


def _v2_sessiz(fn: Callable) -> Callable:
    """Uzun koşularda numpy / pandas uyarı gürültüsünü (boş dilim, parçalı çerçeve) bastırır; hatalar etkilenmez."""
    import functools
    import warnings

    @functools.wraps(fn)
    def sar(*a: Any, **k: Any) -> Any:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            warnings.simplefilter("ignore", getattr(pd.errors, "PerformanceWarning", RuntimeWarning))
            return fn(*a, **k)
    return sar


class Vdyt2Hata(RuntimeError):
    """VDYT2'ye özgü durdurucu hata (ön kayıt yok / değişmiş / git'e işlenmemiş, kod / veri sha256 farklı, KASA açılmış / açılmamış, veri eksik)."""


# ---------------------------------------------------------------- 0) YARDIMCILAR
def _v2_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _v2_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or VDYT2_YOL["cikti"], VDYT2_DOSYA.get(ad, ad))


def _v2_ara(*parca: str) -> str:
    y = os.path.join(VDYT2_YOL["ara"], *parca)
    os.makedirs(os.path.dirname(y) if os.path.splitext(y)[1] else y, exist_ok=True)
    return y


def _v2_yaz(yol: str, metin: str) -> str:
    if _V2_EPOSTA.search(metin):
        raise Vdyt2Hata(f"{os.path.basename(yol)}: metinde e-posta biçimli parça var; yazılmadı")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _v2_json(yol: str, obj: Any) -> str:
    return _v2_yaz(yol, json.dumps(_v2_kayit(obj), ensure_ascii=False, indent=1, default=str, sort_keys=True))


def _v2_json_oku(yol: str) -> Any:
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def _v2_kayit(x: Any) -> Any:
    if isinstance(x, pd.DataFrame):
        return json.loads(x.to_json(orient="records", date_format="iso", default_handler=str))
    if isinstance(x, dict):
        return {str(k): _v2_kayit(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_v2_kayit(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        return x.item()
    if isinstance(x, float) and not np.isfinite(x):
        return None
    return x


def _v2_tohum(*parca: Any) -> int:
    return int(hashlib.sha256("|".join(map(str, parca)).encode("utf-8")).hexdigest()[:8], 16)


def v2_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: VDYT2_ESIK + özellik grupları + model listesi + (içe aktarılan) v1 olay türleri ve EDGAR formları; sıralı JSON."""
    s = json.dumps({"ESIK": E or VDYT2_ESIK, "OZELLIK": VDYT2_OZELLIK, "MODEL": VDYT2_MODEL, "V1_OLAY": V1.VDYT_OLAY_TUR, "V1_EDGAR": V1.VDYT_EDGAR_FORM},
                   sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def v2_kod_sha(yol: Optional[str] = None) -> str:
    return V1.vdyt_sha_dosya(yol or os.path.join(KOK_VDYT2, "VDYT2.py"))


def v2_v1_kod_sha() -> str:
    return V1.vdyt_sha_dosya(os.path.join(KOK_VDYT2, "VDYT.py"))


def _v2_e1(canli: bool = False) -> Dict[str, Any]:
    """VDYT.py fonksiyonlarına verilen v1 biçimli eşik sözlüğü (v1 değerleri; kesik VDYT2'den; canlıda kesik kaldırılır)."""
    E = copy.deepcopy(V1.VDYT_ESIK); E["kesik"] = "2099-12-31" if canli else VDYT2_ESIK["kesik"]
    E["basari"] = copy.deepcopy(VDYT2_ESIK["basari"]); E["coklu"] = {**E["coklu"], **{k: VDYT2_ESIK["coklu"][k] for k in ("bh_q", "tohum")}}
    E["model"] = copy.deepcopy(VDYT2_ESIK["model"]); E["temel"] = {**E["temel"], "kucuk_hucre": VDYT2_ESIK["temel"]["kucuk_hucre"]}
    return E


def _v2_tanimlar(pazar: str, E: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
    E = E or VDYT2_ESIK
    return dict(E["tanim_k62"]) if pazar == "BIST_K62" else dict(E["tanim"])


# ---------------------------------------------------------------- 1) VERİ (VDYT.py yükleyicileri + ABD bilanço günü için Yahoo takvimi birincil)
def v2_fiyat(pazar: str, canli: bool = False, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Temizlenmiş fiyatlar (V1.vdyt_fiyat_yukle). Test: kesik 31.08.2026. Canlı: kesik yok (veri sonu). ABD önbelleği VDYT2 ara klasöründe (v1 önbelleği
    yalnız kaynak özeti tutuyorsa OKUNUR, üzerine yazılmaz)."""
    E1 = _v2_e1(canli)
    if pazar != "ABD":
        return V1.vdyt_fiyat_yukle(pazar, E1, onbellek=False)
    ozet = V1.vdyt_sha_klasor(V1.VDYT_YOL["k60_fiyat"], "*.json")[0]
    ob = _v2_ara(f"fiyat_ABD_{'canli' if canli else 'test'}.pkl")
    for y in ([ob] + ([] if canli else [os.path.join(V1.VDYT_YOL["ara"], "fiyat_ABD.pkl")])):
        if os.path.exists(y):
            try:
                with open(y, "rb") as f:
                    X = pickle.load(f)
                if X.get("kaynak_sha") == ozet and (y == ob or E1["kesik"] == V1.VDYT_ESIK["kesik"]):
                    return X
            except (OSError, pickle.UnpicklingError, EOFError, AttributeError) as ex:
                vdyt2log.warning("ABD önbelleği okunamadı (%s): %s", y, ex)
    X = V1.vdyt_fiyat_yukle("ABD", E1, onbellek=False); X["kaynak_sha"] = ozet
    with open(ob, "wb") as f:
        pickle.dump(X, f, protocol=pickle.HIGHEST_PROTOCOL)
    return X


_V2_YAHOO_TARIH = re.compile(r"\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})(?:\s+at\s+(\d{1,2})\s*([AP]M))?")


def v2_yahoo_takvim_ayristir(html: bytes, sembol: str) -> pd.DataFrame:
    """Yahoo bilanço takvimi tablosu (ham HTML, K67 önbelleği) -> sembol, tarih, saat (ET; 'at 12 AM' = saat yok = 0). K67.py ayrıştırıcısıyla aynı kural
    (K67 içe aktarılmaz: FON_IZI / K60 / K64 bağımlılığı)."""
    bos = pd.DataFrame(columns=["sembol", "tarih", "saat"])
    if not html:
        return bos
    try:
        import io
        T = pd.read_html(io.StringIO(html.decode("utf-8", "replace")), na_values=["-"])[0]
    except (ValueError, IndexError, ImportError) as ex:
        vdyt2log.warning("%s Yahoo takvim tablosu okunamadı: %s", sembol, ex)
        return bos
    kol = {c: re.sub(r"\s+", "", str(c)).lower() for c in T.columns}; T = T.rename(columns=kol)
    if "earningsdate" not in T:
        return bos
    sat = []
    for v in T["earningsdate"].astype(str):
        m = _V2_YAHOO_TARIH.match(v)
        if not m:
            continue
        g = None
        for bc in ("%B %d, %Y", "%b %d, %Y"):
            try:
                g = pd.Timestamp(_dt.datetime.strptime(re.sub(r"\s+", " ", m.group(1)), bc)); break
            except ValueError:
                continue
        if g is None:
            continue
        sa = int(m.group(2)) % 12 + (12 if m.group(3) == "PM" else 0) if m.group(2) else 0
        sat.append((sembol, g, sa))
    return pd.DataFrame(sat, columns=bos.columns).drop_duplicates(["sembol", "tarih"]) if sat else bos


def v2_yahoo_takvim(klasor: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Bütün Yahoo bilanço takvimleri (önbellek /tmp/vdyt2/yahoo_takvim_<özet>.pkl). Döner (tablo, not)."""
    kl = klasor or VDYT2_YOL["k67_takvim"]
    if not os.path.isdir(kl):
        return pd.DataFrame(columns=["sembol", "tarih", "saat"]), {"durum": f"EKSİK ({kl} yok)"}
    oz, n = V1.vdyt_sha_klasor(kl, "*.html.gz"); ob = _v2_ara(f"yahoo_takvim_{oz[:16]}.pkl")
    if os.path.exists(ob):
        with open(ob, "rb") as f:
            return pickle.load(f)
    sat = []
    for y in sorted(glob.glob(os.path.join(kl, "*.html.gz"))):
        s = os.path.basename(y)[: -len(".html.gz")].upper().replace(".", "-")
        try:
            with gzip.open(y, "rb") as f:
                sat.append(v2_yahoo_takvim_ayristir(f.read(), s))
        except OSError as ex:
            vdyt2log.warning("Yahoo takvim dosyası okunamadı %s: %s", y, ex)
    T = pd.concat([x for x in sat if len(x)], ignore_index=True) if any(len(x) for x in sat) else pd.DataFrame(columns=["sembol", "tarih", "saat"])
    out = (T, {"dosya": n, "hisse": int(T.sembol.nunique()) if len(T) else 0, "satir": int(len(T)), "ilk": str(T.tarih.min()) if len(T) else None,
               "son": str(T.tarih.max()) if len(T) else None, "ozet": oz})
    with open(ob, "wb") as f:
        pickle.dump(out, f, protocol=pickle.HIGHEST_PROTOCOL)
    return out


def v2_olaylar(pazar: str, F: Dict[str, Any], canli: bool = False, yahoo: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Pazarın olayları: V1.vdyt_olaylar (KAP / EDGAR / Nasdaq / makro / emtia) + ABD'de bilanço günü için Yahoo takvimi BİRİNCİL (takvimi olan hissede
    v1 bilanço satırları Yahoo ile değiştirilir; saat >= 16 ET -> sonraki işlem günü; diğerleri o gün); ABD rakip bilançosu yeni bilanço kümesinden yeniden
    kurulur. Gelecekteki (bugünden sonraki) takvim satırları atılır. BIST_K62: olay yok (yanlılık kontrolü yalnız başarı 1)."""
    if pazar == "BIST_K62":
        return pd.DataFrame(columns=V1.OLAY_SUTUN), {"durum": "BIST_K62: olay kullanılmaz"}
    Ev, not_ = V1.vdyt_olaylar(pazar, F, _v2_e1(canli))
    if pazar != "ABD":
        return Ev, not_
    Y, yn = (yahoo, {"kaynak": "verilen"}) if yahoo is not None else v2_yahoo_takvim()
    not_["YAHOO_TAKVIM"] = yn
    if not len(Y):
        return Ev, not_
    son = pd.Timestamp(_v2_e1(canli)["kesik"]) if not canli else pd.Timestamp(_dt.date.today())
    Y = Y[(Y.tarih <= son) & Y.sembol.isin(set(F["S"]))].copy()
    g0 = []
    for r in Y.itertuples():
        g = r.tarih + pd.Timedelta(days=1) if r.saat >= 16 else r.tarih
        g0.append(g)
    Y["g0"] = pd.to_datetime(g0)
    yh = set(Y.sembol)
    Ev = Ev[~((Ev.tur == "ABD_BILANCO") & Ev.sembol.isin(yh)) & (Ev.tur != "ABD_RAKIP")]
    Yb = pd.DataFrame({"pazar": "ABD", "sembol": Y.sembol.values, "tur": "ABD_BILANCO", "kat": "A", "onceden": True, "g0_tarih": Y.g0.values,
                       "bilgi_tarih": Y.g0.values, "kaynak": "Yahoo takvimi", "ek": Y.saat.astype(str).values})
    Ev = pd.concat([Ev, Yb], ignore_index=True)
    sek = V1.vdyt_sektor("ABD"); Bl = Ev[Ev.tur == "ABD_BILANCO"].assign(sektor=lambda x: x.sembol.map(sek)).dropna(subset=["sektor"])
    Bl = Bl.assign(ceyrek=pd.to_datetime(Bl.g0_tarih).dt.to_period("Q").astype(str)); ilk = Bl.sort_values("g0_tarih").drop_duplicates(["sektor", "ceyrek"])
    uye: Dict[str, List[str]] = {}
    for s_, g_ in sek.items():
        if s_ in F["S"]:
            uye.setdefault(g_, []).append(s_)
    rk = [(u, r.g0_tarih, r.bilgi_tarih, r.sembol) for r in ilk.itertuples() for u in uye.get(r.sektor, []) if u != r.sembol]
    R_ = pd.DataFrame(rk, columns=["sembol", "g0", "bi", "kim"])
    Ev = pd.concat([Ev, pd.DataFrame({"pazar": "ABD", "sembol": R_.sembol.values, "tur": "ABD_RAKIP", "kat": "C", "onceden": True, "g0_tarih": R_.g0.values,
                                      "bilgi_tarih": R_.bi.values, "kaynak": "bilanço (Yahoo birincil) + SIC", "ek": R_.kim.values})], ignore_index=True)
    Ev["g0_tarih"] = pd.to_datetime(Ev.g0_tarih); Ev["bilgi_tarih"] = pd.to_datetime(Ev.bilgi_tarih)
    not_["ABD_BILANCO_v2"] = {"yahoo_hisse": len(yh), "yahoo_satir": int(len(Yb)), "toplam_bilanco": int((Ev.tur == "ABD_BILANCO").sum())}
    not_["ABD_RAKIP_v2"] = {"olay": int(len(R_))}
    return Ev[V1.OLAY_SUTUN].reset_index(drop=True), not_


def v2_veri_sha() -> Dict[str, Tuple[str, int]]:
    """Koşunun okuduğu veri kaynaklarının sha256'sı: VDYT.py kaynakları (V1.vdyt_veri_sha) + Yahoo bilanço takvimi klasörü."""
    out = dict(V1.vdyt_veri_sha())
    out["k67_takvim"] = V1.vdyt_sha_klasor(VDYT2_YOL["k67_takvim"], "*.html.gz")
    return out


# ---------------------------------------------------------------- 2) GÜNLÜK ÖLÇÜLER VE SESSİZ BÖLGE DURUMLARI (her değer yalnız o gün ve öncesi)
def _v2_egim(y: np.ndarray, L: int) -> np.ndarray:
    """Son L değerin doğrusal eğimi (bar başına; en küçük kareler). İlk L-1 gün NaN."""
    y = np.asarray(y, float); n = len(y); out = np.full(n, np.nan)
    if n < L:
        return out
    x = np.arange(L, dtype=float); w = (x - x.mean()) / np.sum((x - x.mean()) ** 2)
    out[L - 1:] = np.lib.stride_tricks.sliding_window_view(y, L) @ w
    return out


def v2_hat_pencere(o: np.ndarray, h: np.ndarray, l: np.ndarray, c: np.ndarray, tr: np.ndarray, W: int, taban: str,
                   S: Optional[Dict[str, Any]] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """V1.vdyt_savunma'nın kayan pencere [t-W+1, t] sürümü (vektörel; G4 günlük durumu için): taban b (govde = min(O,C), fitil = L, kapanis = C);
    tol = tolerans_tr x medyan TR; adaylar bölge aralığının alt dilimindeki b; p* = en çok temaslı (eşitlikte en düşük); hat VAR <=> temas >= min_temas ve
    ilk-son temas arası >= min_aralik; kırılma = ilk temastan sonra kapanış < p* - tol. Döner (hat_var, kirilma, seviye)."""
    S = S or VDYT2_ESIK["savunma"]; n = len(c); hv = np.zeros(n, bool); kr = np.zeros(n, bool); sv = np.full(n, np.nan)
    if n < W:
        return hv, kr, sv
    b = {"govde": np.minimum(o, c), "fitil": l, "kapanis": c}[taban]
    V = np.lib.stride_tricks.sliding_window_view
    Bw, Hw, Lw, Cw, Tw = V(b, W), V(h, W), V(l, W), V(c, W), V(tr, W)
    tol = float(S["tolerans_tr"]) * np.nanmedian(Tw, axis=1); lo = Lw.min(1); hi = Hw.max(1); sinir = lo + (hi - lo) * float(S["alt_dilim"])
    aday = Bw <= sinir[:, None]
    temas = (np.abs(Bw[:, :, None] - Bw[:, None, :]) <= tol[:, None, None]).sum(2)
    temas = np.where(aday, temas, -1); en = temas.max(1)
    p = np.where((temas == en[:, None]) & aday, Bw, np.inf).min(1)
    ok = (en > 0) & np.isfinite(p) & (tol > 0)
    tj = np.abs(Bw - p[:, None]) <= tol[:, None]
    say = tj.sum(1); ilk = np.argmax(tj, axis=1); son = W - 1 - np.argmax(tj[:, ::-1], axis=1)
    hat = ok & (say >= int(S["min_temas"])) & ((son - ilk) >= int(S["min_aralik"]))
    sonra = np.arange(W)[None, :] > ilk[:, None]
    kir = ok & np.any(sonra & (Cw < (p - tol)[:, None]), axis=1)
    hv[W - 1:] = hat; kr[W - 1:] = kir; sv[W - 1:] = np.where(ok, p, np.nan)
    return hv, kr, sv


def v2_olculer(d: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """V1.vdyt_olculer + VDYT2 sessiz bölge ölçüleri ve günlük durumlar (G1-G5, G5f, G5k, alternatif eşikler, v1 T1-T5). Hepsi geriye bakar."""
    E = E or VDYT2_ESIK; Ss = E["sessiz"]; L = int(Ss["L"]); E1 = _v2_e1()
    Ol = V1.vdyt_olculer(d, E1)
    o, h, l, c = (d[k].to_numpy(float) for k in ("o", "h", "l", "c")); tr = Ol["tr"]
    S = lambda a: pd.Series(a)   # noqa: E731
    with np.errstate(invalid="ignore", divide="ignore"):
        rng = h - l; govde = np.abs(c - o); ust = h - np.maximum(o, c); alt = np.minimum(o, c) - l
        A = E["atr_ref"]
        atr_ref = S(tr).rolling(int(A["n"]), min_periods=int(A["min"])).mean().shift(L).to_numpy()
        R = lambda a, f: getattr(S(a).rolling(L, min_periods=L), f)().to_numpy()   # noqa: E731
        m_aralik = R(rng, "median") / atr_ref; m_govde = R(govde, "median") / atr_ref; m_maks = R(rng, "max") / atr_ref
        m_ust = R(ust, "median") / atr_ref; m_alt = R(alt, "median") / atr_ref
        m_govde_aralik = R(np.where(rng > 0, govde / np.where(rng > 0, rng, 1.0), np.nan), "median")
        m_doji = R((govde <= float(Ss["G1"]["doji"]) * rng).astype(float), "mean")
        G2 = Ss["G2"]
        kb = (R(c, "max") - R(c, "min")) / R(c, "mean")
        gb = (R(np.maximum(o, c), "max") - R(np.minimum(o, c), "min")) / R(c, "mean")
        kb_ref = S(kb).rolling(int(G2["gecmis_n"]), min_periods=int(G2["gecmis_min"])).median().shift(L).to_numpy()
        gb_ref = S(gb).rolling(int(G2["gecmis_n"]), min_periods=int(G2["gecmis_min"])).median().shift(L).to_numpy()
        b_kb = kb / kb_ref; b_gb = gb / gb_ref
        e_tepe = _v2_egim(h, L) / atr_ref; e_dip = _v2_egim(l, L) / atr_ref
        ema = {k: S(c).ewm(span=k, adjust=False, min_periods=k).mean().to_numpy() for k in (20, 50, 200)}
    G4 = Ss["G4"]; W4 = int(G4["pencere"]); g4 = {}; seviye4 = {}
    for tb in G4["tabanlar"]:
        hv, kr, sv = v2_hat_pencere(o, h, l, c, tr, W4, tb, E["savunma"])
        g4[tb] = hv & ~kr if G4["kirilma_yok"] else hv; seviye4[tb] = sv
    kop = V1.vdyt_kopuk(d.index, E1)
    pk = S(kop.astype(float)).rolling(max(L, W4) - 1, min_periods=1).max().to_numpy() > 0   # pencere içinde kopukluk
    fin = lambda x: np.nan_to_num(x, nan=np.inf)   # noqa: E731
    fin_neg = lambda x: np.nan_to_num(x, nan=-np.inf)   # noqa: E731
    G1 = Ss["G1"]

    def g1(e: float) -> np.ndarray:
        return (fin(m_aralik) <= e) & (fin(m_govde) <= float(G1["govde_atr"])) & (fin(m_maks) <= float(G1["maks_aralik_atr"]))

    def g2(e: float) -> np.ndarray:
        return (fin(b_kb) <= e) & (fin(b_gb) <= e)
    g3 = (fin(e_tepe) <= float(Ss["G3"]["tepe_egim_ust"])) & (fin_neg(e_dip) >= float(Ss["G3"]["dip_egim_alt"]))
    G1a, G2a = g1(float(G1["aralik_atr"][0])), g2(float(G2["bant_oran"][0]))
    dur = {"G1": G1a, "G2": G2a, "G3": g3, "G4": g4["govde"], "G5": G1a & G2a & (g3 | g4["govde"]),
           "G5f": G1a & G2a & (g3 | g4["fitil"]), "G5k": G1a & G2a & (g3 | g4["kapanis"]),
           "G1_e1": g1(float(G1["aralik_atr"][1])), "G1_e2": g1(float(G1["aralik_atr"][2])),
           "G5_b1": G1a & g2(float(G2["bant_oran"][1])) & (g3 | g4["govde"]), "G5_b2": G1a & g2(float(G2["bant_oran"][2])) & (g3 | g4["govde"]),
           "G12": G1a & G2a, "G12_b1": G1a & g2(float(G2["bant_oran"][1])), "G12_b2": G1a & g2(float(G2["bant_oran"][2]))}
    dur = {k: x & ~pk for k, x in dur.items()}
    for t_ in ("T1", "T2", "T3", "T4", "T5"):
        dur["V1:" + t_] = V1.vdyt_durum(Ol, t_, 0, E1)
    Ol.update({"govde": govde, "aralik": rng, "atr_ref": atr_ref, "m_aralik_atr": m_aralik, "m_govde_atr": m_govde, "m_maks_aralik": m_maks,
               "m_fitil_ust_atr": m_ust, "m_fitil_alt_atr": m_alt, "m_govde_aralik": m_govde_aralik, "m_doji_pay": m_doji, "b_kapanis_bant": b_kb,
               "b_govde_bant": b_gb, "b_egim_tepe": e_tepe, "b_egim_dip": e_dip, "ema20": ema[20], "ema50": ema[50], "ema200": ema[200],
               "g4_seviye": seviye4["govde"], "kopuk": kop, "durum": dur, "g_bilesen": G1a.astype(int) + G2a.astype(int) + (g3 | g4["govde"]).astype(int)})
    return Ol


# ---------------------------------------------------------------- 3) BÜYÜK MUM, BÖLGE MOTORU, GEÇERLİLİK, ETİKET
def _v2_ref(i: int, ref_bas: int, tr: np.ndarray, govde: np.ndarray, c: np.ndarray, E: Dict[str, Any], kapanis: bool) -> Tuple[float, float, int]:
    """[max(ref_bas, i - ref_max), i - 1] referansı: medyan TR (taban tr_taban x C[i-1]) ve medyan gövde (taban govde_taban x TR referansı), başlangıç."""
    B = E["buyuk"]; a = max(int(ref_bas), i - int(B["ref_max"]))
    if i - a < int(B["ref_min"]) or a < 0:
        return np.nan, np.nan, a
    rt = max(float(np.median(tr[a:i])), float(B["tr_taban"]) * float(c[i - 1]))
    rb = np.nan if kapanis else max(float(np.median(govde[a:i])), float(B["govde_taban"]) * rt)
    return rt, rb, a


def v2_buyuk_mum(i: int, ref_bas: int, tr: np.ndarray, govde: np.ndarray, c: np.ndarray, E: Optional[Dict[str, Any]] = None, kapanis: bool = False) -> bool:
    """i. gün 'büyük mum' mu (yalnız i ve öncesi): TR_i >= k_b x medyan TR[ref] VE |gövde_i| >= m x medyan |gövde|[ref]; ref = [max(ref_bas, i-60), i-1],
    en az ref_min gün. Kapanış kipinde (BIST_K62; açılış yok) gövde şartı yok."""
    E = E or VDYT2_ESIK; rt, rb, _a = _v2_ref(i, ref_bas, tr, govde, c, E, kapanis)
    if not np.isfinite(rt) or not np.isfinite(tr[i]):
        return False
    if tr[i] < float(E["buyuk"]["k_b"]) * rt:
        return False
    return True if kapanis else bool(govde[i] >= float(E["buyuk"]["m"]) * rb)


def _v2_nanmedyan(W: np.ndarray) -> np.ndarray:
    """Satır başına NaN'sız medyan (np.nanmedian ile aynı değer; küçük pencerelerde maskeli dizi yavaşlığı olmadan). Boş satır -> NaN."""
    S = np.sort(W, axis=1); k = (~np.isnan(W)).sum(1); i = np.arange(len(W))
    a = S[i, np.maximum((k - 1) // 2, 0)]; b = S[i, np.maximum(k // 2, 0)]
    return np.where(k > 0, 0.5 * (a + b), np.nan)


def v2_ref_blok(bas: int, g0: int, g1: int, tr: np.ndarray, govde: np.ndarray, c: np.ndarray, E: Optional[Dict[str, Any]] = None,
                kapanis: bool = False) -> Dict[str, Any]:
    """v2_buyuk_mum / v2_onay'ın vektörel sürümü, g ∈ [g0, g1] için (aynı ref başlangıcı bas): ref = [max(bas, g-ref_max), g-1] -> büyük mum (bool), Lo, Hi.
    Değerler skaler fonksiyonlarla birebir aynıdır (test_vdyt2 bölüm 3)."""
    E = E or VDYT2_ESIK; B = E["buyuk"]; R = int(B["ref_max"]); n = len(tr); g1 = min(int(g1), n - 1); g0 = max(int(g0), 1)
    if g1 < g0:
        z = np.zeros(0)
        return {"g0": g0, "g1": g1, "buyuk": z.astype(bool), "lo": z, "hi": z}
    idx = np.arange(g0 - R, g1); ok = (idx >= max(int(bas), 0)) & (idx < n); al = np.clip(idx, 0, n - 1)
    V_ = np.lib.stride_tricks.sliding_window_view
    Wt = V_(np.where(ok, tr[al], np.nan), R); Wc = V_(np.where(ok, c[al], np.nan), R); say = (~np.isnan(Wt)).sum(1); gg = np.arange(g0, g1 + 1)
    yeter = say >= int(B["ref_min"])
    with np.errstate(invalid="ignore"), __import__("warnings").catch_warnings():
        __import__("warnings").simplefilter("ignore", RuntimeWarning)
        rt = np.maximum(_v2_nanmedyan(Wt), float(B["tr_taban"]) * c[gg - 1])
        lo = np.nanmin(Wc, axis=1); hi = np.nanmax(Wc, axis=1)
        bm = yeter & np.isfinite(tr[gg]) & (tr[gg] >= float(B["k_b"]) * rt)
        if not kapanis:
            rb = np.maximum(_v2_nanmedyan(V_(np.where(ok, govde[al], np.nan), R)), float(B["govde_taban"]) * rt)
            bm &= govde[gg] >= float(B["m"]) * rb
    return {"g0": g0, "g1": g1, "buyuk": bm, "lo": lo, "hi": hi}


def _v2_cikis(g: int, lo: float, hi: float, c: np.ndarray, kop: np.ndarray, og: int) -> Tuple[int, int]:
    n = len(c)
    for e in range(g, g + og):
        if e > n - 1 or (e > g and kop[e]):
            return -9, -1
        if c[e] > hi:
            return 1, e
        if c[e] < lo:
            return -1, e
    return 0, -1


def v2_onay(g: int, ref_bas: int, c: np.ndarray, kop: np.ndarray, E: Optional[Dict[str, Any]] = None) -> Tuple[int, int]:
    """Büyük mumun onayı: [g, g + onay_gun - 1] içinde ilk kapanış > Hi -> +1, < Lo -> -1 (Lo / Hi = [max(ref_bas, g-60), g-1] kapanış aralığı).
    Döner (yön, çıkış günü e): onaysız (pencere tamam, çıkış yok) -> (0, -1); belirsiz (veri / kopukluk) -> (-9, -1)."""
    E = E or VDYT2_ESIK; B = E["buyuk"]; n = len(c); a = max(int(ref_bas), g - int(B["ref_max"]))
    if a >= g:
        return -9, -1
    lo, hi = float(np.min(c[a:g])), float(np.max(c[a:g]))
    for e in range(g, g + int(B["onay_gun"])):
        if e > n - 1 or (e > g and kop[e]):
            return -9, -1
        if c[e] > hi:
            return 1, e
        if c[e] < lo:
            return -1, e
    return 0, -1


def v2_bolgeler(durum: np.ndarray, kop: np.ndarray, tr: np.ndarray, govde: np.ndarray, c: np.ndarray, min_kosu: int,
                E: Optional[Dict[str, Any]] = None, kapanis: bool = False, devam: Optional[np.ndarray] = None) -> np.ndarray:
    """Sessiz bölgeler (ön kayıtlı kural). Açılış: durum min_kosu gün kesintisiz doğru (G tanımlarında 1; durum zaten son L günün ölçüsü; v1 T tanımlarında 10)
    ve önceki bölgenin bitişinden en az L gün sonra -> tespit = o gün, bas = tespit - L + 1 (yaş = t - bas + 1; tespitte 10). Bitiş (tespitten SONRA, ilk
    gerçekleşen): BÜYÜK MUM (v2_buyuk_mum, ref başlangıcı bas) | SÖNME (DEVAM durumu sonme_gun gün üst üste yanlış; devam verilmezse açılış durumu; G5
    ailesinde devam = çekirdek G1 VE G2: tepe-dip / destek şartı açılış onayıdır) | SANSÜR (veri sonu / kopukluk).
    Döner (m, 4) int: bas, tespit, bit, bit_tur. Bitiş günü gerçek zamanda bilinir (bit kapanışında)."""
    E = E or VDYT2_ESIK; L = int(E["sessiz"]["L"]); sg = int(E["bolge"]["sonme_gun"]); n = len(durum)
    dv = durum if devam is None else devam
    kosu = V1.vdyt_kosu(durum, kop); aday = np.flatnonzero(kosu >= int(min_kosu)); out = []; j = -10 ** 9
    while True:
        p = int(np.searchsorted(aday, max(j + L, L - 1)))
        if p >= len(aday):
            break
        tes = int(aday[p]); bas = tes - L + 1; yanlis = 0; kapandi = False; i = tes + 1; bl = None
        while i < n:
            if kop[i]:
                out.append((bas, tes, i - 1, BIT_SANSUR)); j = i - 1; kapandi = True; break
            if bl is None or i > bl["g1"]:
                bl = v2_ref_blok(bas, i, i + 127, tr, govde, c, E, kapanis)
            if bl["buyuk"][i - bl["g0"]]:
                out.append((bas, tes, i, BIT_BUYUK)); j = i; kapandi = True; break
            if not dv[i]:
                yanlis += 1
                if yanlis >= sg:
                    out.append((bas, tes, i, BIT_SONME)); j = i; kapandi = True; break
            else:
                yanlis = 0
            i += 1
        if not kapandi:
            out.append((bas, tes, n - 1, BIT_SANSUR)); break
    return np.array(out, dtype=np.int64).reshape(-1, 4)


def v2_gecerli(t: int, bas: int, tr: np.ndarray, c: np.ndarray, E: Optional[Dict[str, Any]] = None) -> bool:
    """D1a: karar günü t geçerli <=> t ve önceki gun-1 günün HER BİRİNİN gerçek aralığı <= k_sessiz x medyan TR[max(bas, t-59), t] (taban tr_taban x C)."""
    E = E or VDYT2_ESIK; G = E["gecerli"]; k = int(G["gun"])
    if t - k + 1 < max(0, bas) or t < 1:
        return False
    a = max(int(bas), t - int(G["ref_max"]) + 1)
    ref = max(float(np.median(tr[a: t + 1])), float(E["buyuk"]["tr_taban"]) * float(c[t]))
    x = tr[t - k + 1: t + 1]
    return bool(np.all(np.isfinite(x)) and np.all(x <= float(G["k_sessiz"]) * ref))


def v2_onkosul(c: np.ndarray, bas: int, E: Optional[Dict[str, Any]] = None) -> Tuple[float, float, float, float]:
    """Ön koşul (bas günündeki bilgi): düşüş = C[bas] / max(C[bas-120 .. bas-1]) - 1; yükseliş = C[bas] / min(...) - 1. P1 = düşüş <= -0,30;
    P2 = P1 ya da yükseliş >= +0,30 (|değişim| >= %30). Geçmiş < 120 bar -> NaN. Döner (düşüş, yükseliş, P1, P2)."""
    E = E or VDYT2_ESIK; O = E["onkosul"]; W = int(O["pencere"])
    if bas < W:
        return np.nan, np.nan, np.nan, np.nan
    w = c[bas - W: bas]; d = float(c[bas] / np.max(w) - 1.0); u = float(c[bas] / np.min(w) - 1.0)
    p1 = float(d <= float(O["P1"])); p2 = float(p1 == 1.0 or u >= float(O["P2"]))
    return d, u, p1, p2


def v2_etiket(t: int, bas: int, c: np.ndarray, tr: np.ndarray, govde: np.ndarray, kop: np.ndarray, E: Optional[Dict[str, Any]] = None,
              kapanis: bool = False, blok: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Büyük hareket etiketi (BH1), YALNIZ t'den SONRA başlayan: g = ilk ONAYLI büyük mum günü, g ∈ (t, t + max ufuk] (ref başlangıcı bas; bölge g-1'e kadar
    sürmüş sayılır). y_h = 1 <=> g <= t + h; 0 <=> (t, t+h] içinde onaylı büyük mum yok; NaN <=> t + h + onay_gun - 1 > veri sonu ya da (t, t+h+9] içinde
    kopukluk. Yön = çıkılan kenar; e = çıkış günü."""
    E = E or VDYT2_ESIK; U = [int(x) for x in E["ufuk"]]; H = max(U); og = int(E["buyuk"]["onay_gun"]); n = len(c)
    out: Dict[str, Any] = {f"y{h}": np.nan for h in U}; out.update({"g": -1, "e": -1, "yon": np.nan})
    son = min(n - 1, t + H + og - 1); kj = np.flatnonzero(kop[t + 1: son + 1]); ilk_kop = t + 1 + int(kj[0]) if len(kj) else n
    g_on = -1
    if blok is None or blok["g0"] > t + 1 or blok["g1"] < min(n - 1, t + H):
        blok = v2_ref_blok(bas, t + 1, t + H, tr, govde, c, E, kapanis)
    for g in range(t + 1, min(n, t + H + 1)):
        if g >= ilk_kop:
            break
        k = g - blok["g0"]
        if blok["buyuk"][k]:
            yon, e = _v2_cikis(g, float(blok["lo"][k]), float(blok["hi"][k]), c, kop, og)
            if yon in (1, -1):
                g_on = g; out.update({"g": g, "e": e, "yon": float(yon)}); break
    for h in U:
        gerek = t + h + og - 1
        if gerek > n - 1 or ilk_kop <= gerek:
            continue
        out[f"y{h}"] = 1.0 if (g_on > 0 and g_on <= t + h) else 0.0
    return out


def v2_bhu(c: np.ndarray, tr: np.ndarray, govde: np.ndarray, kop: np.ndarray, E: Optional[Dict[str, Any]] = None, kapanis: bool = False
           ) -> pd.DataFrame:
    """Bölgeden bağımsız BÜYÜK HAREKET başlangıçları (duyarlılık / kaçırılan için): g'de TR >= k_b x medyan TR[g-60, g-1] VE |gövde| >= m x medyan |gövde|
    (aynı tabanlarla) VE [g, g+9] içinde [g-20, g-1] kapanış aralığından çıkış; başlangıç = önceki 20 barda tutulan başka BHU yok. Döner g, e, yon."""
    E = E or VDYT2_ESIK; B = E["bhu"]; K = E["buyuk"]; n = len(c); S = lambda a: pd.Series(a)   # noqa: E731
    with np.errstate(invalid="ignore", divide="ignore"):
        cp = np.r_[np.nan, c[:-1]]
        rt = np.maximum(S(tr).rolling(int(B["ref_n"]), min_periods=int(B["ref_min"])).median().shift(1).to_numpy(), float(K["tr_taban"]) * cp)
        rb = np.maximum(S(govde).rolling(int(B["ref_n"]), min_periods=int(B["ref_min"])).median().shift(1).to_numpy(), float(K["govde_taban"]) * rt)
        bm = (np.nan_to_num(tr) >= float(K["k_b"]) * np.nan_to_num(rt, nan=np.inf))
        if not kapanis:
            bm &= np.nan_to_num(govde) >= float(K["m"]) * np.nan_to_num(rb, nan=np.inf)
        hi = S(c).rolling(int(B["bant_n"]), min_periods=int(B["bant_n"])).max().shift(1).to_numpy()
        lo = S(c).rolling(int(B["bant_n"]), min_periods=int(B["bant_n"])).min().shift(1).to_numpy()
    sat = []; son_g = -10 ** 9
    for g in np.flatnonzero(bm):
        g = int(g)
        if g - son_g <= int(B["tekil"]) or not np.isfinite(hi[g]) or kop[g]:
            continue
        yon, e = 0, -1
        for j in range(g, g + int(K["onay_gun"])):
            if j > n - 1 or (j > g and kop[j]):
                yon = -9; break
            if c[j] > hi[g]:
                yon, e = 1, j; break
            if c[j] < lo[g]:
                yon, e = -1, j; break
        if yon in (1, -1):
            sat.append((g, e, yon)); son_g = g
    return pd.DataFrame(sat, columns=["g", "e", "yon"])


# ---------------------------------------------------------------- 4) KARAR SATIRI ÖZELLİKLERİ (bilgi tarihi <= t)
def v2_ozellik(t: int, bas: int, A: Dict[str, Any], ctx: Dict[str, Any], once: np.ndarray, E: Optional[Dict[str, Any]] = None,
               tabanlar: bool = True) -> Dict[str, float]:
    """Karar günü t, bölge başlangıcı bas için VDYT2_OZELLIK (hepsi t ve öncesi). once: t'den önce bitip onayı bilinen bölgeler (bas, tespit, bit, tur, onay)."""
    E = E or VDYT2_ESIK; Ol = A["Ol"]; o, h, l, c, v, tr, atr = A["o"], A["h"], A["l"], A["c"], A["v"], Ol["tr"], Ol["atr"]; a = t - bas + 1
    r: Dict[str, float] = {"yas_log": float(np.log(a))}
    for k in (15, 20, 30, 45, 60, 90):
        r[f"yk_{k}"] = float(a >= k)
    if len(once) >= int(E["hisse_gecmis"]["min_bolge"]):
        su = once[:, 2] - once[:, 0] + 1
        r.update({"hs_oran": a / float(np.median(su)), "hs_yetersiz": 0.0, "hs_bh_pay": float(np.mean((once[:, 3] == BIT_BUYUK) & (once[:, 4] == 1)))})
    else:
        r.update({"hs_oran": 0.0, "hs_yetersiz": 1.0, "hs_bh_pay": 0.0})
    r.update({"rj_pazar": ctx["rj_pazar"][t], "rj_sektor": ctx["rj_sektor"][t], "p_pazar_ret60": ctx["p_pazar_ret60"][t],
              "p_pazar_ret20": ctx["p_pazar_ret20"][t], "p_sektor_ret20": ctx["p_sektor_ret20"][t]})
    d_, u_, p1, p2 = v2_onkosul(c, bas, E)
    r.update({"on_dusus120": d_, "on_yukselis120": u_, "on_p1": p1, "on_p2": p2})
    for k in ("m_aralik_atr", "m_govde_atr", "m_govde_aralik", "m_fitil_ust_atr", "m_fitil_alt_atr", "m_doji_pay", "m_maks_aralik", "b_kapanis_bant",
              "b_govde_bant", "b_egim_tepe", "b_egim_dip"):
        r[k] = float(Ol[k][t])
    at = float(atr[t]) if np.isfinite(atr[t]) and atr[t] > 0 else np.nan
    cl = c[bas: t + 1]; lo, hi = float(np.min(cl)), float(np.max(cl))
    r["b_bolge_bant_atr"] = (hi - lo) / at if np.isfinite(at) else np.nan
    ra = max(bas, t - int(E["gecerli"]["ref_max"]) + 1); rm = float(np.median(tr[ra: t + 1]))
    r.update({"v_natr_oran": Ol["natr_oran"][t], "v_rv_yuzde": Ol["rv_yuzde"][t], "v_bbw_yuzde": Ol["bbw_yuzde"][t], "v_rv5_rv20": Ol["rv5_rv20"][t],
              "v_tr_son3": float(np.mean(tr[t - 2: t + 1]) / rm) if rm > 0 else np.nan})
    mv = float(np.median(v[bas: t + 1])); vo = v[max(0, bas - 250): bas]
    r.update({"h_hacim_oran": Ol["hacim_oran"][t], "h_hacim_son5": float(np.mean(v[t - 4: t + 1]) / mv) if mv > 0 else np.nan,
              "h_yukselen_hacim": Ol["yuk_hacim"][t], "h_bolge_hacim": float(mv / np.median(vo)) if len(vo) >= 100 and np.median(vo) > 0 else np.nan})
    E1 = A["E1"]; sv = V1.vdyt_savunma(o, h, l, c, v, tr, atr, int(bas), int(t), "govde", E1)
    for k in ("hat_var", "temas", "korunma", "kirilma", "fitil_ihlal", "son_test", "hacim_test", "yukselen_dip", "alcalan_tepe", "mesafe"):
        r[f"sv_{k}"] = float(sv[k])
    r["sv_seviye"] = sv["seviye"]
    r["sv_kapanis_ustu"] = float(np.mean(cl >= sv["seviye"])) if np.isfinite(sv["seviye"]) else np.nan
    for tb, on in (("fitil", "svf"), ("kapanis", "svk")):
        if tabanlar:
            s2 = V1.vdyt_savunma(o, h, l, c, v, tr, atr, int(bas), int(t), tb, E1)
            r[f"{on}_hat_var"] = float(s2["hat_var"]); r[f"{on}_kirilma"] = float(s2["kirilma"]); r[f"{on}_seviye"] = s2["seviye"]
        else:
            r[f"{on}_hat_var"] = np.nan; r[f"{on}_kirilma"] = np.nan; r[f"{on}_seviye"] = np.nan
    r["k_bolge_konum"] = (c[t] - lo) / (hi - lo) if hi > lo else 0.5
    r["k_ust_mesafe_atr"] = (hi - c[t]) / at if np.isfinite(at) else np.nan; r["k_alt_mesafe_atr"] = (c[t] - lo) / at if np.isfinite(at) else np.nan
    with np.errstate(invalid="ignore", divide="ignore"):
        r.update({"e_ema20": float(np.log(c[t] / Ol["ema20"][t])), "e_ema50": float(np.log(c[t] / Ol["ema50"][t])),
                  "e_ema200": float(np.log(c[t] / Ol["ema200"][t])), "e_sma50": Ol["sma50"][t], "e_sma200": Ol["sma200"][t],
                  "e_sma50_egim": Ol["sma50_egim"][t], "e_ema20_50": float(np.log(Ol["ema20"][t] / Ol["ema50"][t]))})
    r.update({"f_ret20": Ol["ret20"][t], "f_ret60": Ol["ret60"][t], "f_likidite": Ol["likidite"][t]})
    bb = ctx["bilanco_bilgi_i"]; bil = ctx["bilanco_tarih"][(bb >= 0) & (bb <= t)]
    bg, bs = V1.vdyt_beklenen_bilanco(bil, ctx["gun"][t])
    r["o_bilanco_gun"] = float(np.clip(bg, 0, 90)) if np.isfinite(bg) else 90.0; r["o_bilanco_yok"] = float(not np.isfinite(bg))
    r["o_bilanco_son"] = float(np.clip(bs, 0, 120)) if np.isfinite(bs) else 120.0
    r["o_bilanco_bolgede"] = float(np.sum((bb >= bas) & (bb <= t)))
    mg = ctx["makro_g0_i"]; r["o_makro_10"] = float(np.any((mg > t) & (mg <= t + 10)))
    bi, b0 = ctx["B_bilgi_i"], ctx["B_g0_i"]; ok = (bi >= 0) & (bi <= t)
    r["o_olay_son5"] = float(np.sum(ok & (bi > t - 5))); r["o_olay_son20"] = float(np.sum(ok & (bi > t - 20)))
    sn = np.flatnonzero(ok & (b0 > t - 20) & (b0 >= 1) & (b0 <= t))
    if len(sn):
        g0 = int(b0[sn[np.argmax(b0[sn])]]); pl = ctx["p_lr"][g0]
        r["o_olay_tepki"] = float(Ol["lr"][g0] - (pl if np.isfinite(pl) else 0.0))
    else:
        r["o_olay_tepki"] = 0.0
    return r


def v2_satir(s: str, t: int, bas: int, A: Dict[str, Any], ctx: Dict[str, Any], kaynak: str, bolge: int, once: Optional[np.ndarray],
             E: Optional[Dict[str, Any]] = None, ozellik: bool = True, tabanlar: bool = True, kapanis: bool = False) -> Dict[str, Any]:
    """Bir karar satırı: kimlik, eşleme anahtarları, etiketler (v2_etiket), çözülme tarihleri, bilgi amaçlı getiriler (t+1 açılış ve kırılım sonrası;
    maliyet sonrası) + (ozellik ise) v2_ozellik."""
    E = E or VDYT2_ESIK; gun = A["gun"]; n = A["n"]; c, o, h, l = A["c"], A["o"], A["h"], A["l"]; og = int(E["buyuk"]["onay_gun"]); a = t - bas + 1
    r: Dict[str, Any] = {"sembol": s, "kaynak": kaynak, "bolge": int(bolge), "bas": int(bas), "t": int(t), "yas": int(a), "tarih": gun[t],
                         "natr_d": ctx["natr_d"][t], "mom_t": ctx["mom_t"][t], "liq_t": ctx["liq_t"][t],
                         "pazar_yon": float(np.nan_to_num(ctx["p_pazar_ret60"][t], nan=0.0) >= 0)}
    d_, u_, p1, p2 = v2_onkosul(c, bas, E); r.update({"P1": p1, "P2": p2})
    for hh in E["ufuk"]:
        r[f"son{hh}"] = gun[min(t + int(hh) + og - 1, n - 1)]
    if kaynak == "GERCEK":   # aynı bölgenin satırları aynı bas'ı paylaşır: blok bir kez
        bc = A.setdefault("blok", {}); blok = bc.get(bas)
        if blok is None:
            blok = bc[bas] = v2_ref_blok(bas, bas + 1, bas + max(E["karar_yas"]) + max(E["ufuk"]), A["Ol"]["tr"], A["Ol"]["govde"], c, E, kapanis)
    else:
        blok = v2_ref_blok(bas, t + 1, t + max(E["ufuk"]), A["Ol"]["tr"], A["Ol"]["govde"], c, E, kapanis)
    Y = v2_etiket(t, bas, c, A["Ol"]["tr"], A["Ol"]["govde"], A["Ol"]["kopuk"], E, kapanis, blok); r.update(Y)
    g, e = int(Y["g"]), int(Y["e"]); mal = float(E["maliyet"].get(A["pazar"], 0.001))
    r["g_tarih"] = gun[g] if g >= 0 else pd.NaT
    r["buyukluk10"] = float(np.log(c[g + og - 1] / c[g - 1])) if g > 0 and g + og - 1 <= n - 1 else np.nan
    r["buyukluk20"] = float(np.log(c[g + 19] / c[g - 1])) if g > 0 and g + 19 <= n - 1 else np.nan
    at = A["Ol"]["atr"][g - 1] if g > 0 else np.nan
    r["hareket_atr"] = float((c[g + og - 1] - c[g - 1]) / at) if g > 0 and g + og - 1 <= n - 1 and np.isfinite(at) and at > 0 else np.nan
    if t + 1 <= n - 1:
        gir = o[t + 1]
        for hh in E["getiri_ufuk"]:
            r[f"r{hh}"] = (c[t + hh] / gir - 1.0 - 2.0 * mal) if t + hh <= n - 1 else np.nan
        mu = int(E["mfe_ufuk"])
        if t + mu <= n - 1:
            r["mfe"] = float(np.max(h[t + 1: t + mu + 1]) / gir - 1.0); r["mae"] = float(np.min(l[t + 1: t + mu + 1]) / gir - 1.0)
    if e >= 0 and e + 1 <= n - 1:
        gk = o[e + 1]
        for hh in E["getiri_ufuk"]:
            r[f"rk{hh}"] = (c[e + hh] / gk - 1.0 - 2.0 * mal) if e + hh <= n - 1 else np.nan
    if ozellik:
        r.update(v2_ozellik(t, bas, A, ctx, once if once is not None else np.zeros((0, 5), np.int64), E, tabanlar))
    return r


# ---------------------------------------------------------------- 5) HİSSE BAŞINA İŞLEM (bölgeler, satırlar, kontroller, BHU, olay havuzu)
_V2_IS: Dict[str, Any] = {}


def _v2_bolge_tablo(s: str, B: np.ndarray, A: Dict[str, Any], uy: np.ndarray, E: Dict[str, Any], kapanis: bool) -> pd.DataFrame:
    """Bölge tablosu + onay (BÜYÜK MUM bitişinin [g, g+9] bant çıkışı: 1 onaylı, 0 sahte, -1 belirsiz / uygulanmaz) + ön koşul."""
    gun = A["gun"]; c = A["c"]; kop = A["Ol"]["kopuk"]; sat = []
    for bas, tes, bit, tur in B:
        on, yb, eb = -1, np.nan, -1
        if tur == BIT_BUYUK:
            y_, e_ = v2_onay(int(bit), int(bas), c, kop, E); on = 1 if y_ in (1, -1) else (0 if y_ == 0 else -1)
            yb = float(y_) if y_ in (1, -1) else np.nan; eb = e_
        d_, u_, p1, p2 = v2_onkosul(c, int(bas), E)
        sat.append((s, int(bas), int(tes), int(bit), int(tur), on, yb, eb, int(bit - bas + 1), gun[bas], gun[tes], gun[bit], bool(uy[tes]), d_, u_, p1, p2))
    T = pd.DataFrame(sat, columns=["sembol", "bas", "tespit", "bit", "bit_tur", "onay", "yon_bit", "e_bit", "sure", "bas_tarih", "tespit_tarih", "bit_tarih",
                                   "uygun_tespit", "on_dusus", "on_yukselis", "P1", "P2"])
    return T.astype({"bas": np.int64, "tespit": np.int64, "bit": np.int64, "bit_tur": np.int64, "onay": np.int64, "e_bit": np.int64, "sure": np.int64,
                     "uygun_tespit": bool, "yon_bit": float, "on_dusus": float, "on_yukselis": float, "P1": float, "P2": float})


def _v2_once(T: Any, t: int, E: Dict[str, Any]) -> np.ndarray:
    """t gününde onayı bilinen, t'den önce bitmiş bölgeler: bit + onay_gun <= t (bas, tespit, bit, tur, onay). T: bölge tablosu ya da onun dizisi."""
    if not len(T):
        return np.zeros((0, 5), np.int64)
    X = T[["bas", "tespit", "bit", "bit_tur", "onay"]].to_numpy(np.int64) if isinstance(T, pd.DataFrame) else T
    return X[X[:, 2] + int(E["buyuk"]["onay_gun"]) <= t]


def _v2_rastgele_bolge(n: int, sureler: np.ndarray, sayi: int, rng: np.random.Generator, E: Dict[str, Any]) -> List[Tuple[int, int]]:
    """Rastgele bölgeler (kontrol b): gerçek süre dağılımından çekilen süre, tekdüze başlangıç [ilk_bar, n-1-süre-30]; sıkışma şartı yok."""
    out = []; ilk = int(E["kontrol"]["ilk_bar"])
    if not len(sureler):
        return out
    for L_ in rng.choice(sureler, size=int(sayi), replace=True):
        ust = n - 1 - int(L_) - 30
        if ust <= ilk:
            continue
        b = int(rng.integers(ilk, ust)); out.append((b, b + int(L_) - 1))
    return out


def v2_onkosul_dizi(c: np.ndarray, E: Optional[Dict[str, Any]] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """v2_onkosul'un her bas için vektörel sürümü (aynı değerler): düşüş, yükseliş, P1, P2 dizileri (geçmiş < pencere -> NaN)."""
    E = E or VDYT2_ESIK; O = E["onkosul"]; W = int(O["pencere"]); S = pd.Series(np.asarray(c, float))
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (S / S.rolling(W, min_periods=W).max().shift(1) - 1.0).to_numpy(); u = (S / S.rolling(W, min_periods=W).min().shift(1) - 1.0).to_numpy()
    p1 = np.where(np.isfinite(d), (d <= float(O["P1"])).astype(float), np.nan)
    p2 = np.where(np.isfinite(d), ((p1 == 1.0) | (u >= float(O["P2"]))).astype(float), np.nan)
    return d, u, p1, p2


def v2_etiket_toplu(ts: np.ndarray, bs: np.ndarray, c: np.ndarray, tr: np.ndarray, govde: np.ndarray, kop: np.ndarray, E: Optional[Dict[str, Any]] = None,
                    kapanis: bool = False, parca: int = 1500) -> Dict[str, np.ndarray]:
    """v2_etiket'in çok satırlı vektörel sürümü (aynı sonuç; test_vdyt2 bölüm 3): her satır (t, bas) için g ∈ (t, t+H] referans pencereleri tek matriste."""
    E = E or VDYT2_ESIK; B = E["buyuk"]; R = int(B["ref_max"]); U = [int(h) for h in E["ufuk"]]; H = max(U); og = int(B["onay_gun"]); n = len(c)
    ts = np.asarray(ts, np.int64); bs = np.asarray(bs, np.int64); m = len(ts)
    out = {f"y{h}": np.full(m, np.nan) for h in U}; out.update({"g": np.full(m, -1, np.int64), "e": np.full(m, -1, np.int64), "yon": np.full(m, np.nan)})
    if not m:
        return out
    for p0 in range(0, m, parca):
        t_ = ts[p0: p0 + parca]; b_ = bs[p0: p0 + parca]; G = t_[:, None] + 1 + np.arange(H)[None, :]; Gc = np.minimum(G, n - 1)
        W = G[:, :, None] - R + np.arange(R)[None, None, :]; ok = (W >= np.maximum(b_, 0)[:, None, None]) & (W >= 0) & (W < n); Wc = np.clip(W, 0, n - 1)
        with np.errstate(invalid="ignore"), __import__("warnings").catch_warnings():
            __import__("warnings").simplefilter("ignore", RuntimeWarning)
            Tw = np.where(ok, tr[Wc], np.nan); say = ok.sum(2)
            rt = np.maximum(_v2_nanmedyan(Tw.reshape(-1, R)).reshape(Tw.shape[:2]), float(B["tr_taban"]) * c[np.maximum(Gc - 1, 0)])
            bm = (say >= int(B["ref_min"])) & (G <= n - 1) & np.isfinite(tr[Gc]) & (tr[Gc] >= float(B["k_b"]) * rt)
            if not kapanis:
                rb = np.maximum(_v2_nanmedyan(np.where(ok, govde[Wc], np.nan).reshape(-1, R)).reshape(Tw.shape[:2]), float(B["govde_taban"]) * rt)
                bm &= govde[Gc] >= float(B["m"]) * rb
            Cw = np.where(ok, c[Wc], np.nan); lo = np.nanmin(Cw, 2); hi = np.nanmax(Cw, 2)
        for i in range(len(t_)):
            t = int(t_[i]); son = min(n - 1, t + H + og - 1)
            kj = np.flatnonzero(kop[t + 1: son + 1]); ilk_kop = t + 1 + int(kj[0]) if len(kj) else n; g_on = -1
            for j in np.flatnonzero(bm[i]).tolist():
                g = t + 1 + j
                if g >= ilk_kop:
                    break
                yon, e = _v2_cikis(g, float(lo[i, j]), float(hi[i, j]), c, kop, og)
                if yon in (1, -1):
                    g_on = g; out["g"][p0 + i] = g; out["e"][p0 + i] = e; out["yon"][p0 + i] = float(yon); break
            for h in U:
                gerek = t + h + og - 1
                if gerek > n - 1 or ilk_kop <= gerek:
                    continue
                out[f"y{h}"][p0 + i] = 1.0 if (g_on > 0 and g_on <= t + h) else 0.0
    return out


def _v2_hafif(s: str, A: Dict[str, Any], natr_d: np.ndarray, onk: Tuple[np.ndarray, ...], ts: List[int], bs: List[int], bolge: List[int], kaynak: str,
              E: Dict[str, Any], kapanis: bool, etiket: bool) -> pd.DataFrame:
    """Hafif satırlar (ALT / K62 tanımları ve AILE kontrolleri; yalnız başarı 1): kimlik, tabaka anahtarları, ön koşul, (etiket ise) y5 / y10 / y20, g, yön,
    çözülme tarihleri (v2_etiket_toplu)."""
    ts_ = np.asarray(ts, np.int64); bs_ = np.asarray(bs, np.int64); n = A["n"]; gun = A["gun"]; og = int(E["buyuk"]["onay_gun"]); U = [int(h) for h in E["ufuk"]]
    K: Dict[str, Any] = {"sembol": np.full(len(ts_), s, object), "kaynak": np.full(len(ts_), kaynak, object), "bolge": np.asarray(bolge, np.int64), "bas": bs_,
                         "t": ts_, "yas": (ts_ - bs_ + 1).astype(np.int64)}
    if len(ts_):
        K.update({"tarih": gun[ts_], "natr_d": natr_d[ts_], "P1": onk[2][bs_], "P2": onk[3][bs_]})
        if etiket:
            for h in U:
                K[f"son{h}"] = gun[np.minimum(ts_ + h + og - 1, n - 1)]
            Y = v2_etiket_toplu(ts_, bs_, A["c"], A["Ol"]["tr"], A["Ol"]["govde"], A["Ol"]["kopuk"], E, kapanis)
            K.update({k: Y[k] for k in [f"y{h}" for h in U] + ["g", "yon"]})
    return pd.DataFrame(K)


def _v2_hisse_is(s: str) -> Dict[str, Any]:
    """Tek hisse: kip 'kapsam' -> yalnız sayım girdileri (etiket / getiri YOK); kip 'kos' -> bölgeler, karar satırları, kontrol satırları (DIŞARI: aynı hisse
    / yıl / NATR ondalığı, sıkışma dışı; RASTGELE: aynı süre dağılımı), BHU olayları ve bölge kapsaması, olay havuzu (ANA). Tam satır (etiket + özellik +
    getiri): ANA (gerçek ve kontrol) ve AILE (gerçek). Hafif satır (etiket + tabaka; yalnız başarı 1): ALT / K62 ve AILE kontrolleri, YALNIZ hafif_bas'tan
    (ilk WF test yılı) sonraki karar günleri (önceki yıllar başarı 1'de kullanılmaz)."""
    X = _V2_IS; E = X["E"]; pazar = X["pazar"]; kip = X["kip"]; d = X["F"]["S"][s]; kapanis = pazar == "BIST_K62"
    try:
        Ol = v2_olculer(d, E); n = len(d); E1 = _v2_e1(X.get("canli", False))
        Ev_s = X["Ev_s"].get(s, X["bos_olay"]); ctx = V1.vdyt_hisse_baglam(s, d, X["Pn"], Ev_s, X["Ev_m"])
        ctx["p_pazar_ret20"] = X["Pn"]["p_pazar_ret20"].reindex(d.index).to_numpy(float)
        uy = V1.vdyt_hisse_uygun(s, d, X["Pn"])
        A = {"Ol": Ol, "o": d.o.to_numpy(float), "h": d.h.to_numpy(float), "l": d.l.to_numpy(float), "c": d.c.to_numpy(float), "v": d.v.to_numpy(float),
             "gun": d.index, "n": n, "pazar": pazar, "E1": E1}
        tr, gv, c, kop = Ol["tr"], Ol["govde"], A["c"], Ol["kopuk"]; onk = v2_onkosul_dizi(c, E)
        out: Dict[str, Any] = {"sembol": s, "n": n, "hata": None, "bolge": {}, "satir": {}, "kontrol": {}, "bhu": None, "kapsama": {}, "havuz": {}}
        bhu = v2_bhu(c, tr, gv, kop, E, kapanis); bhu = bhu[(bhu.g >= int(E["kontrol"]["ilk_bar"])) & uy[np.maximum(bhu.g.to_numpy() - 1, 0)]] if len(bhu) else bhu
        bhu = bhu.assign(sembol=s, tarih=d.index[bhu.g.to_numpy()] if len(bhu) else pd.DatetimeIndex([]),
                         e_tarih=d.index[bhu.e.to_numpy()] if len(bhu) else pd.DatetimeIndex([]))
        yil = d.index.year.to_numpy(); natr_d = ctx["natr_d"]; ilk = int(E["kontrol"]["ilk_bar"]); tam = (kip == "kos")
        hb = int(np.searchsorted(d.index, pd.Timestamp(E["kontrol"]["hafif_bas"])))
        for ad, Tn in X["tanimlar"].items():
            rol = Tn["rol"]; dur = Ol["durum"][Tn["durum"]]; dv = Ol["durum"][Tn.get("devam", Tn["durum"])]
            B = v2_bolgeler(dur, kop, tr, gv, c, int(Tn["min_kosu"]), E, kapanis, dv)
            T = _v2_bolge_tablo(s, B, A, uy, E, kapanis); out["bolge"][ad] = T; Tx = T[["bas", "tespit", "bit", "bit_tur", "onay"]].to_numpy(np.int64)
            acik = np.full(n, -1, np.int64); icinde = np.zeros(n, bool)
            for i_, (b0, t0_, b1) in enumerate(Tx[:, :3].tolist()):
                acik[t0_: b1] = i_; icinde[b0: b1 + 1] = True
            if len(bhu):   # BHU tespiti: g-1 gününde açık bölge (tespit <= g-1 < bit) -> uyarı süresi g - tespit
                ai = acik[np.maximum(bhu.g.to_numpy() - 1, 0)]
                bhu[f"tespit_{ad}"] = ai >= 0
                bhu[f"uyari_{ad}"] = np.where(ai >= 0, bhu.g.to_numpy() - T.tespit.to_numpy()[np.maximum(ai, 0)], -1) if len(T) else -1
                bhu[f"p1_{ad}"] = np.where(ai >= 0, T.P1.to_numpy(float)[np.maximum(ai, 0)], np.nan) if len(T) else np.nan
            uy_gun = uy & (np.arange(n) >= ilk)
            out["kapsama"][ad] = pd.DataFrame({"yil": yil[uy_gun], "acik": (acik[uy_gun] >= 0)}).groupby("yil").agg(gun=("acik", "size"), acik=("acik", "sum"))
            tam_g = tam and rol in ("ANA", "AILE"); tam_k = tam and rol == "ANA"; alt_sinir = 0 if (tam_g or not tam) else hb
            # gerçek karar satırları (D1a geçerli, uygun)
            ts, bs, bo = [], [], []
            for i_, (b0, t0_, b1) in enumerate(Tx[:, :3].tolist()):
                for a in E["karar_yas"]:
                    t = b0 + int(a) - 1
                    if t < t0_ or t >= b1 or not uy[t] or not v2_gecerli(t, b0, tr, c, E):
                        continue
                    ts.append(t); bs.append(b0); bo.append(i_)
            if tam_g:
                S_ = pd.DataFrame([v2_satir(s, t, b, A, ctx, "GERCEK", i_, _v2_once(Tx, t, E), E, ozellik=True, tabanlar=(rol == "ANA"), kapanis=kapanis)
                                   for t, b, i_ in zip(ts, bs, bo)])
            else:
                S0 = _v2_hafif(s, A, natr_d, onk, ts, bs, bo, "GERCEK", E, kapanis, etiket=False)   # tabaka için bütün yıllar
                S_ = _v2_hafif(s, A, natr_d, onk, [t for t in ts if t >= alt_sinir], [b for t, b in zip(ts, bs) if t >= alt_sinir],
                               [i_ for t, i_ in zip(ts, bo) if t >= alt_sinir], "GERCEK", E, kapanis, etiket=tam) if tam else S0
            out["satir"][ad] = S_; Sk = S_ if tam_g or not tam else S0
            # kontrol a (DIŞARI): sıkışma dışı (bu tanımın hiçbir bölgesinin [bas, bit] aralığında değil) uygun günler, aynı (yıl, NATR ondalığı) hücresinden
            kat = int(E["kontrol"]["disari_kat"][rol]); rng = np.random.default_rng(_v2_tohum(s, ad, "DISARI", E["kontrol"]["tohum"])); kd = []
            if len(Sk):
                cand = np.flatnonzero(~icinde & uy & (np.arange(n) >= ilk) & np.isfinite(natr_d))
                ck: Dict[Tuple[int, float], List[int]] = {}
                for q in cand.tolist():
                    ck.setdefault((int(yil[q]), float(natr_d[q])), []).append(q)
                tt = Sk.t.to_numpy(np.int64); yaslar = Sk.yas.to_numpy(); hk = pd.Series(np.arange(len(tt))).groupby([yil[tt], natr_d[tt]]).size()
                for (yy, nd), m_ in hk.items():
                    havuz = ck.get((int(yy), float(nd)))
                    if not havuz:
                        continue
                    for t in np.sort(rng.choice(np.asarray(havuz), size=min(len(havuz), kat * int(m_)), replace=False)).tolist():
                        a = int(rng.choice(yaslar)); b_ = t - a + 1
                        if b_ >= 1 and v2_gecerli(t, b_, tr, c, E):
                            kd.append((t, b_))
            # kontrol b (RASTGELE): aynı süre dağılımı, rastgele başlangıç, sıkışma şartı yok; aynı karar yaşları, geçerlilik ve etiket
            Tu = T[T.uygun_tespit]; rr = np.random.default_rng(_v2_tohum(s, ad, "RASTGELE", E["kontrol"]["tohum"])); kr = []
            for b_, bit_ in _v2_rastgele_bolge(n, Tu.sure.to_numpy(), int(E["kontrol"]["rastgele_kat"]) * len(Tu), rr, E):
                for a in E["karar_yas"]:
                    t = b_ + int(a) - 1
                    if t < bit_ and t <= n - 1 and uy[t] and v2_gecerli(t, b_, tr, c, E):
                        kr.append((t, b_))
            ks = []
            for kn, L_ in (("DISARI", kd), ("RASTGELE", kr)):
                if tam_k:
                    ks.append(pd.DataFrame([v2_satir(s, t, b, A, ctx, kn, -1, _v2_once(Tx, t, E), E, ozellik=True, tabanlar=False, kapanis=kapanis) for t, b in L_]))
                else:
                    L2 = [(t, b) for t, b in L_ if t >= (hb if tam else 0)]
                    ks.append(_v2_hafif(s, A, natr_d, onk, [t for t, _b in L2], [b for _t, b in L2], [-1] * len(L2), kn, E, kapanis, etiket=tam))
            out["kontrol"][ad] = pd.concat([k_ for k_ in ks if len(k_)], ignore_index=True) if any(len(k_) for k_ in ks) else pd.DataFrame()
            if rol == "ANA" and tam:
                tur_v1 = np.where((T.bit_tur == BIT_BUYUK) & (T.onay == 1), V1.BITIS_GEN, np.where(T.bit_tur == BIT_SANSUR, V1.BITIS_SANSUR,
                                                                                                   np.where(T.onay == -1, V1.BITIS_SANSUR, V1.BITIS_SONME)))
                acik_u = acik.copy()
                for i_, (b0, t0_, b1) in enumerate(Tx[:, :3].tolist()):
                    if not bool(T.uygun_tespit.iat[i_]):
                        acik_u[t0_: b1] = -1
                out["havuz"][ad] = {"acik": acik_u, "B": np.column_stack([Tx[:, :3], tur_v1]).astype(np.int64) if len(T) else np.zeros((0, 4), np.int64)}
                if not kapanis and len(T):   # olay-bölge zaman eşlemesi (olayın bölge başına göre yaşı, onaylı BH gününe göre gün farkı); V1 kuralı
                    T2 = T.assign(uygun=T.uygun_tespit.astype(bool), bit_tur=tur_v1, gen_bas=T.bit, Y1=T.yon_bit)
                    out["olay_es"] = V1._vdyt_olay_bolge_satir(s, d, Ol, T2, V1._vdyt_tur_indeks(d.index, Ev_s, X["Ev_m"]), E1)
        out["bhu"] = bhu
        if kip == "kos":
            out["havuz"]["_ortak"] = {"ym": (d.index.year * 100 + d.index.month).to_numpy(np.int32), "yil": yil.astype(np.int32),
                                      "mom": np.nan_to_num(ctx["mom_t"], nan=-1).astype(np.int8), "liq": np.nan_to_num(ctx["liq_t"], nan=-1).astype(np.int8),
                                      "ti": V1._vdyt_tur_indeks(d.index, Ev_s, X["Ev_m"]), "gun": d.index}
        return out
    except Exception as ex:   # tek hissenin hatası koşuyu durdurmaz; sayısı ve nedeni hata raporuna yazılır
        return {"sembol": s, "hata": f"{type(ex).__name__}: {str(ex)[:200]}", "bolge": {}, "satir": {}, "kontrol": {}, "kapsama": {}, "havuz": {}}


def v2_pazar_isle(pazar: str, kip: str, isci: int = 3, F: Optional[Dict[str, Any]] = None, Ev: Optional[pd.DataFrame] = None,
                  E: Optional[Dict[str, Any]] = None, canli: bool = False) -> Dict[str, Any]:
    """Pazarın bütün hisseleri: panel (V1.vdyt_panel; uygunluk, tertiller, NATR ondalığı, rejim) + hisse başına _v2_hisse_is. F / Ev verilirse yükleme atlanır."""
    E = E or VDYT2_ESIK; t0 = time.time(); E1 = _v2_e1(canli)
    F = F or v2_fiyat(pazar, canli)
    if Ev is None:
        Ev, ev_not = v2_olaylar(pazar, F, canli)
    else:
        ev_not = {"kaynak": "verilen"}
    Pn = V1.vdyt_panel(pazar, F, E1, isci)
    Pn["p_pazar_ret20"] = Pn["p_pazar_lr"].rolling(20, min_periods=20).sum()
    Ev_m = Ev[Ev.sembol == "*"]; Ev_s = {s: g for s, g in Ev[Ev.sembol != "*"].groupby("sembol")}
    _V2_IS.clear()
    _V2_IS.update({"E": E, "F": F, "pazar": pazar, "kip": kip, "Pn": Pn, "Ev_s": Ev_s, "Ev_m": Ev_m, "bos_olay": Ev.iloc[:0], "tanimlar": _v2_tanimlar(pazar, E),
                   "canli": canli})
    R = V1._vdyt_harita(_v2_hisse_is, sorted(F["S"]), isci)
    hata = {r["sembol"]: r["hata"] for r in R if r.get("hata")}
    if hata:
        vdyt2log.warning("%s: %d hissede hata (ilk: %s)", pazar, len(hata), list(hata.items())[:2])
    vdyt2log.info("%s %s: %d hisse, %.0f sn", pazar, kip, len(R), time.time() - t0)
    return {"pazar": pazar, "R": [r for r in R if not r.get("hata")], "hata": hata, "Pn": Pn, "Ev": Ev, "ev_not": ev_not, "F": F, "sure_sn": round(time.time() - t0, 1)}


# ---------------------------------------------------------------- 6) KAPSAM (YALNIZ SAYIM: etiket / oran / yön / getiri / model YOK)
@_v2_sessiz
def v2_kapsam(pazarlar: Optional[List[str]] = None, cikti: Optional[str] = None, isci: int = 3, girdi: Optional[Dict[str, Tuple[Dict[str, Any], pd.DataFrame]]] = None,
              E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Gerçek veride YALNIZ SAYIM: tanım x ön koşul x dönem bölge sayısı, geçerli karar günü (yaş x dönem), kontrol satırı sayısı (DIŞARI / RASTGELE; etiketsiz),
    bölgeden bağımsız büyük hareket (BHU) TOPLAM SAYISI (dönem başına; bölgelere göre oran YOK), olay sayıları. Süre / bitiş türü / genişleme oranı YAZILMAZ."""
    E = E or VDYT2_ESIK; pazarlar = pazarlar or (list(E["karar_pazari"]) + list(E["kontrol_pazari"]))
    out: Dict[str, Any] = {"zaman": _v2_simdi(), "surum": VDYT2_SURUM, "kod_sha256": v2_kod_sha(), "pazar": {}}
    for pz in pazarlar:
        try:
            F_, Ev_ = (girdi or {}).get(pz, (None, None))
            Z = v2_pazar_isle(pz, "kapsam", isci, F_, Ev_, E)
        except (Vdyt2Hata, V1.VdytHata) as ex:
            out["pazar"][pz] = {"durum": f"EKSİK: {ex}"}; continue
        R = Z["R"]; Pn = Z["Pn"]; o: Dict[str, Any] = {"hisse": len(Z["F"]["S"]), "hisse_hata": len(Z["hata"]), "sure_sn": Z["sure_sn"],
                                                     "takvim": [str(Pn["takvim"].min().date()), str(Pn["takvim"].max().date())] if len(Pn["takvim"]) else None,
                                                     "endeks_kaynak": Pn["endeks_kaynak"]}
        U = Pn["uygun"]; o["uygun_hisse_yil_sonu"] = {int(y): int(v) for y, v in U.sum(axis=1).groupby(U.index.year).last().items()}
        o["olay_turu"] = {t: {"olay": int(len(g)), "hisse": int(g.sembol.nunique()), "ilk": str(g.g0_tarih.min().date()), "son": str(g.g0_tarih.max().date())}
                          for t, g in Z["Ev"].groupby("tur")} if len(Z["Ev"]) else {}
        o["olay_notu"] = Z["ev_not"]
        BH = pd.concat([h["bhu"] for h in R if h.get("bhu") is not None and len(h["bhu"])], ignore_index=True) if any(
            h.get("bhu") is not None and len(h["bhu"]) for h in R) else pd.DataFrame(columns=["tarih"])
        o["buyuk_hareket_BHU_toplam"] = {dn: int(((BH.tarih >= pd.Timestamp(a)) & (BH.tarih <= pd.Timestamp(b))).sum()) for dn, a, b in E["donem_kapsam"]}
        o["buyuk_hareket_BHU_toplam"]["hepsi"] = int(len(BH))
        bol, kar, kon = {}, {}, {}
        for ad, Tn in Z.get("tanimlar", _v2_tanimlar(pz, E)).items():
            T = pd.concat([h["bolge"][ad] for h in R if ad in h["bolge"]], ignore_index=True) if R else pd.DataFrame()
            Tu = T[T.uygun_tespit] if len(T) else T
            bol[ad] = {"rol": Tn["rol"], "bolge_hepsi": int(len(T)), "bolge_uygun": int(len(Tu)), "hisse": int(Tu.sembol.nunique()) if len(Tu) else 0,
                       "P": {p: int(len(Tu)) if p == "P0" else int((Tu[p] == 1).sum()) if len(Tu) else 0 for p in E["onkosul"]["alt_kumeler"]},
                       "donem": {dn: int(((Tu.bas_tarih >= pd.Timestamp(a)) & (Tu.bas_tarih <= pd.Timestamp(b))).sum()) if len(Tu) else 0
                                 for dn, a, b in E["donem_kapsam"]}}
            KD = pd.concat([h["satir"][ad] for h in R if ad in h["satir"] and len(h["satir"][ad])], ignore_index=True) if any(
                ad in h["satir"] and len(h["satir"][ad]) for h in R) else pd.DataFrame(columns=["yas", "tarih", "P1", "P2"])
            KD = KD.assign(yil=pd.to_datetime(KD.tarih).dt.year)
            kar[ad] = {"toplam": int(len(KD)), "P": {p: int(len(KD)) if p == "P0" else int((KD[p] == 1).sum()) for p in E["onkosul"]["alt_kumeler"]},
                       "yas": {int(a): int(v) for a, v in KD.yas.value_counts().sort_index().items()},
                       "donem": {dn: int(((KD.yil >= pd.Timestamp(a).year) & (KD.yil <= pd.Timestamp(b).year)).sum()) for dn, a, b in E["donem_kapsam"]},
                       "donem_P1": {dn: int(((KD.yil >= pd.Timestamp(a).year) & (KD.yil <= pd.Timestamp(b).year) & (KD.P1 == 1)).sum()) for dn, a, b in E["donem_kapsam"]}}
            KK = pd.concat([h["kontrol"][ad] for h in R if ad in h["kontrol"] and len(h["kontrol"][ad])], ignore_index=True) if any(
                ad in h["kontrol"] and len(h["kontrol"][ad]) for h in R) else pd.DataFrame(columns=["kaynak", "P1"])
            kon[ad] = {k: {"toplam": int((KK.kaynak == k).sum()), "P1": int(((KK.kaynak == k) & (KK.P1 == 1)).sum())} for k in ("DISARI", "RASTGELE")}
        o["bolge"] = bol; o["karar"] = kar; o["kontrol"] = kon; out["pazar"][pz] = o
        del Z, R
    if cikti is not False:
        _v2_json(_v2_yol("kapsam", cikti), out); _v2_yaz(_v2_yol("kapsam_md", cikti), v2_kapsam_md(out))
    return out


def v2_kapsam_md(K: Dict[str, Any]) -> str:
    E = VDYT2_ESIK; dn = [d[0] for d in E["donem_kapsam"]]
    L = [f"# VDYT2 kapsam sayımı (YALNIZ SAYI) — {VDYT2_ETIKET}\n\nÜretim: {K['zaman']} ({K['surum']}; VDYT2.py sha256 {K.get('kod_sha256', '')[:12]}). "
         "`python -I VDYT2.py kapsam`. Büyük hareket ORANI, yön, getiri, süre / bitiş türü dağılımı, model başarısı HESAPLANMADI. Büyük hareket satırı yalnız "
         "bölgeden bağımsız BHU TOPLAM SAYISIDIR (etiketin kendisi; tespit edilen bölgelere göre oran DEĞİL).\n"]
    for pz, o in K["pazar"].items():
        if "bolge" not in o:
            L.append(f"\n## {pz}\n\n{o.get('durum')}\n"); continue
        L.append(f"\n## {pz}\n\nHisse {V1._t(o['hisse'])} (hata {o['hisse_hata']}), takvim {o['takvim']}, endeks {o['endeks_kaynak']}, süre {o['sure_sn']} sn.\n\n"
                 "Yıl sonu uygun hisse: " + ", ".join(f"{y}: {V1._t(v)}" for y, v in o["uygun_hisse_yil_sonu"].items()) + "\n\n"
                 "Bölgeden bağımsız büyük hareket başlangıcı (BHU, uygun; YALNIZ TOPLAM): " + ", ".join(f"{k}: {V1._t(v)}" for k, v in o["buyuk_hareket_BHU_toplam"].items()) + "\n")
        L.append("\n### Sessiz bölgeler (uygun; başlangıç dönemine göre) ve ön koşul\n\n| tanım | rol | bölge (uygun / hepsi) | hisse | P1 | P2 | " + " | ".join(dn)
                 + " |\n|" + "---|" * (6 + len(dn)) + "\n")
        for ad, b in o["bolge"].items():
            L.append(f"| {ad} | {b['rol']} | {V1._t(b['bolge_uygun'])} / {V1._t(b['bolge_hepsi'])} | {V1._t(b['hisse'])} | {V1._t(b['P']['P1'])} | "
                     f"{V1._t(b['P']['P2'])} | " + " | ".join(V1._t(b["donem"].get(x)) for x in dn) + " |\n")
        L.append("\n### Geçerli karar günleri (D1a; bölge açık, uygun) ve kontrol satırları (etiketsiz sayım)\n\n| tanım | toplam | P1 | P2 | "
                 + " | ".join(f"yaş {a}" for a in E["karar_yas"]) + " | " + " | ".join(dn) + " | P1: " + " | P1: ".join(dn)
                 + " | DIŞARI (P1) | RASTGELE (P1) |\n|" + "---|" * (6 + len(E["karar_yas"]) + 2 * len(dn)) + "\n")
        for ad, k in o["karar"].items():
            kk = o["kontrol"].get(ad, {})
            L.append(f"| {ad} | {V1._t(k['toplam'])} | {V1._t(k['P']['P1'])} | {V1._t(k['P']['P2'])} | " + " | ".join(V1._t(k["yas"].get(a, 0)) for a in E["karar_yas"])
                     + " | " + " | ".join(V1._t(k["donem"].get(x, 0)) for x in dn) + " | " + " | ".join(V1._t(k["donem_P1"].get(x, 0)) for x in dn)
                     + f" | {V1._t(kk.get('DISARI', {}).get('toplam'))} ({V1._t(kk.get('DISARI', {}).get('P1'))}) | "
                       f"{V1._t(kk.get('RASTGELE', {}).get('toplam'))} ({V1._t(kk.get('RASTGELE', {}).get('P1'))}) |\n")
        if o.get("olay_turu"):
            L.append("\n### Olaylar\n\n| tür | olay | hisse | ilk | son |\n|---|---|---|---|---|\n")
            for t, v in sorted(o["olay_turu"].items()):
                L.append(f"| {t} | {V1._t(v['olay'])} | {V1._t(v['hisse'])} | {v['ilk']} | {v['son']} |\n")
        L.append("\nOlay kaynak notları: `" + json.dumps(o.get("olay_notu"), ensure_ascii=False, default=str)[:2500] + "`\n")
    return "".join(L)


# ---------------------------------------------------------------- 7) MODEL, WALK-FORWARD, DEĞERLENDİRME
def v2_kolon(gruplar: List[str]) -> List[str]:
    return [c for g in gruplar for c in VDYT2_OZELLIK[g]]


def v2_wf(D: pd.DataFrame, y: str, son: str, modeller: Dict[str, List[str]], temeller: Dict[str, Any], yillar: List[int], kesik: str,
          E: Optional[Dict[str, Any]] = None, Dtest: Optional[pd.DataFrame] = None, katsayi: bool = False) -> Tuple[pd.DataFrame, List[Dict[str, Any]], Dict[str, Any]]:
    """Zaman sıralı walk-forward: test yılı Y için eğitim = etiketi Y başından ÖNCE tamamlanmış satırlar (son < Y-01-01; etiketli), test = Dtest (varsayılan D)
    satırlarından karar günü Y içinde ve son <= kesik olanlar. Standartlaştırma ve eşikler (q_yüksek = eğitim tahminlerinin %80'i, %90'ı) yalnız eğitimden.
    Döner (tahmin tablosu: satir, yil, p_<model>, q80_<model>, q90_<model>, p_<temel>; yıl kaydı; son yılın katsayıları)."""
    E = E or VDYT2_ESIK; M = E["model"]; tah, kayit, kat = [], [], {}
    Dtr = D[D[y].notna()]; T_ = (Dtest if Dtest is not None else D)
    T_ = T_[T_[y].notna()] if Dtest is None else T_
    for Y in yillar:
        b = pd.Timestamp(f"{Y}-01-01"); tr = Dtr[Dtr[son] < b]; te = T_[(T_.tarih.dt.year == Y) & (T_[son] <= pd.Timestamp(kesik))]
        k_ = {"yil": Y, "egitim": int(len(tr)), "test": int(len(te)), "egitim_son_max": str(tr[son].max()) if len(tr) else None}
        if len(tr) < int(M["min_egitim"]) or not len(te) or tr[y].nunique() < 2:
            k_["durum"] = "atlandı (eğitim yetersiz ya da test boş)"; kayit.append(k_); continue
        P = pd.DataFrame({"satir": te.index.to_numpy(), "yil": Y}, index=te.index.to_numpy())
        for ad, kol in modeller.items():
            Xa, Xb = V1.vdyt_standart(tr[kol].to_numpy(float), te[kol].to_numpy(float), tuple(M["winsor"]))
            bta = V1.vdyt_lojistik(Xa, tr[y].to_numpy(float), float(M["ridge"]), int(M["tur"]), float(M["tol"]))
            P[f"p_{ad}"] = np.clip(V1.vdyt_sigmoid(np.column_stack([np.ones(len(Xb)), Xb]) @ bta), 1e-4, 1 - 1e-4)
            fit = V1.vdyt_sigmoid(np.column_stack([np.ones(len(Xa)), Xa]) @ bta)
            P[f"q80_{ad}"] = float(np.quantile(fit, float(E["sinif"]["q_yuksek"]))); P[f"q90_{ad}"] = float(np.quantile(fit, 0.9))
            P[f"esik90_{ad}"] = P[f"q90_{ad}"]
            if katsayi:
                kat[ad] = {"yil": Y, "kolon": kol, "b": bta.tolist()}
        for ad, an in temeller.items():
            P[f"p_{ad}"] = float(an) if isinstance(an, (int, float)) else V1.vdyt_temel_tablo(tr, te, list(an), y, int(E["temel"]["kucuk_hucre"]))
        k_["durum"] = "tamam"; kayit.append(k_); tah.append(P)
    return (pd.concat(tah) if tah else pd.DataFrame()), kayit, kat


def v2_degerlendir(P: pd.DataFrame, D: pd.DataFrame, y: str, m: str, t0: str, E: Optional[Dict[str, Any]] = None, yon: bool = False,
                   maske: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """V1._vdyt_degerlendir (Brier / log loss skill, dengeli doğruluk farkı, hisse kümeli bootstrap, ECE, kesinlik / duyarlılık) + kalibrasyon tablosu."""
    E = E or VDYT2_ESIK; r = V1._vdyt_degerlendir(P, D, y, m, t0, _v2_e1(), yon, maske)
    if r.get("n", 0) >= 30 and f"p_{m}" in P:
        Q = P if maske is None else P[maske]; yy = D.loc[Q.satir, y].to_numpy(float); ok = np.isfinite(yy)
        cal, _e = V1.vdyt_kalibrasyon(yy[ok], Q[f"p_{m}"].to_numpy(float)[ok]); r["kalibrasyon"] = _v2_kayit(cal)
    return r


def v2_skill_fark(Pa: pd.DataFrame, Da: pd.DataFrame, Pb: pd.DataFrame, Db: pd.DataFrame, y: str, m: str, t0: str, E: Optional[Dict[str, Any]] = None,
                  ma: Optional[np.ndarray] = None, mb: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """D1b: Brier skill(a) - Brier skill(b) (a = gerçek bölge satırları, b = kontrol satırları), ortak hisse kümeleriyle bootstrap (aynı çekiliş ikisine)."""
    E = E or VDYT2_ESIK; B = E["basari"]

    def hz(P: pd.DataFrame, D: pd.DataFrame, mk: Optional[np.ndarray]) -> Optional[pd.DataFrame]:
        if not len(P) or f"p_{m}" not in P or f"p_{t0}" not in P:
            return None
        Q = P if mk is None else P[mk]; yy = D.loc[Q.satir, y].to_numpy(float); ok = np.isfinite(yy)
        return pd.DataFrame({"k": D.loc[Q.satir, "sembol"].to_numpy()[ok], "bm": (Q[f"p_{m}"].to_numpy(float)[ok] - yy[ok]) ** 2,
                             "b0": (Q[f"p_{t0}"].to_numpy(float)[ok] - yy[ok]) ** 2})
    A_, B_ = hz(Pa, Da, ma), hz(Pb, Db, mb)
    if A_ is None or B_ is None or len(A_) < 30 or len(B_) < 30:
        return {"n_a": 0 if A_ is None else len(A_), "n_b": 0 if B_ is None else len(B_), "fark": np.nan, "alt": np.nan, "ust": np.nan, "p": np.nan}
    kod, uq = pd.factorize(pd.concat([A_.k, B_.k], ignore_index=True)); nk = len(uq); ka, kb = kod[: len(A_)], kod[len(A_):]
    bc = lambda k, w: np.bincount(k, weights=w, minlength=nk)   # noqa: E731
    Sa, S0a, Sb, S0b = bc(ka, A_.bm.to_numpy()), bc(ka, A_.b0.to_numpy()), bc(kb, B_.bm.to_numpy()), bc(kb, B_.b0.to_numpy())
    W = V1._vdyt_bootstrap_agirlik(nk, int(B["bootstrap"]), int(B["tohum"]))
    with np.errstate(invalid="ignore", divide="ignore"):
        bs = (1 - (W @ Sa) / (W @ S0a)) - (1 - (W @ Sb) / (W @ S0b))
    bs = bs[np.isfinite(bs)]; f = float((1 - Sa.sum() / S0a.sum()) - (1 - Sb.sum() / S0b.sum()))
    return {"n_a": int(len(A_)), "n_b": int(len(B_)), "skill_a": float(1 - Sa.sum() / S0a.sum()), "skill_b": float(1 - Sb.sum() / S0b.sum()), "fark": f,
            "alt": float(np.percentile(bs, B["guven"][0])), "ust": float(np.percentile(bs, B["guven"][1])), "p": V1.vdyt_p_normal(f, bs)}


def v2_oran_karsilastir(Dg: pd.DataFrame, Dk: pd.DataFrame, y: str, tabaka: List[str], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Başarı (1): gerçek bölge satırlarının y oranı - kontrol satırlarının (tabaka içinde gerçeğin dağılımına yeniden ağırlıklı) oranı; hisse kümeli bootstrap.
    Tabakasında kontrolü olmayan gerçek satırlar düşer (sayısı yazılır). Oran = ort1 / ort0."""
    E = E or VDYT2_ESIK; B = E["basari"]
    kol = ["sembol", y] + [c for c in tabaka if c not in ("sembol", y)]
    U = pd.concat([Dg[kol].assign(g=1.0), Dk[kol].assign(g=0.0)], ignore_index=True)
    U = U[U[y].notna()]
    if not len(U) or U.g.nunique() < 2:
        return {"n1": int((U.g == 1).sum()) if len(U) else 0, "n0": int((U.g == 0).sum()) if len(U) else 0, "fark": np.nan, "alt": np.nan, "ust": np.nan, "p": np.nan}
    w = V1.vdyt_tabakali_agirlik(U.g.to_numpy(), U[tabaka].fillna(-1))
    r = V1.vdyt_bootstrap_fark(U.sembol.to_numpy(), U[y].to_numpy(float), np.where(w > 0, U.g, np.nan), int(B["bootstrap"]), int(B["tohum"]),
                               tuple(B["guven"]), agirlik=w)
    r["n1_ham"] = int((U.g == 1).sum()); r["n0_ham"] = int((U.g == 0).sum()); r["n1_dusen"] = int(((U.g == 1) & (w <= 0)).sum())
    r["oran"] = float(r["ort1"] / r["ort0"]) if r.get("ort0") and np.isfinite(r.get("ort0", np.nan)) and r["ort0"] > 0 else np.nan
    return r


def _v2_donem(asama: str, E: Dict[str, Any]) -> Tuple[str, str, List[int]]:
    if asama == "wf":
        return f"{E['wf']['kesif_yillar'][0]}-01-01", E["wf"]["wf_son"], list(E["wf"]["kesif_yillar"])
    if asama == "kasa":
        return E["wf"]["kasa"][0], E["wf"]["kasa"][1], list(E["wf"]["kasa_yillar"])
    raise Vdyt2Hata(f"bilinmeyen aşama: {asama}")


def _v2_alt(D: pd.DataFrame, p: str) -> np.ndarray:
    return np.ones(len(D), bool) if p == "P0" else (D[p].to_numpy(float) == 1)


# ---------------------------------------------------------------- 8) PAZAR ANALİZİ (Faz 2; yalnız `kos` çağırır)
def _v2_birlestir(R: List[Dict[str, Any]], alan: str, ad: str) -> pd.DataFrame:
    L = [h[alan][ad] for h in R if ad in h.get(alan, {}) and isinstance(h[alan][ad], pd.DataFrame) and len(h[alan][ad])]
    return pd.concat(L, ignore_index=True) if L else pd.DataFrame()


def _v2_hazirla(D: pd.DataFrame, E: Dict[str, Any]) -> pd.DataFrame:
    if not len(D):
        return D
    D = D.reset_index(drop=True).rename_axis("satir")
    D["tarih"] = pd.to_datetime(D.tarih); D["yil"] = D.tarih.dt.year; D["ay"] = D.tarih.dt.month; D["yas_kova"] = V1.vdyt_yas_kova(D.yas, {"yas_kova": E["yas_kova"]})
    D["yukari"] = np.where(D.yon == 1, 1.0, np.where(D.yon == -1, 0.0, np.nan))
    return D


def v2_analiz(Z: Dict[str, Any], asama: str, E: Optional[Dict[str, Any]] = None, ara: Optional[str] = None, p1_tekrar: Optional[int] = None) -> Dict[str, Any]:
    """Bir pazarın Faz 2 analizi: başarı (1) tanım x ön koşul x kontrol; duyarlılık / kaçırılan / uyarı süresi / yanlış bölge (bilgi); başarı (2) genişleme
    (ufuk x model x temel; ablasyon; tek grup; süre yaklaşımları; D1b kontrolleri); başarı (3) yön (B1 KARAR, B2 ve konum-dışı BİLGİ; işlem sonucu); süre
    (KM / CIF / hazard, olgunlaşma testi); olaylar (E1 / E2, haberli / habersiz, plasebo eşiği); sınıf değerlendirmesi (bilgi); BH aileleri."""
    E = E or VDYT2_ESIK; pazar = Z["pazar"]; R = Z["R"]; tan = _v2_tanimlar(pazar, E); bas, son, yillar = _v2_donem(asama, E)
    tb, ts = pd.Timestamp(bas), pd.Timestamp(son); Bb = E["basari"]; ara = ara or _v2_ara(asama); os.makedirs(ara, exist_ok=True)
    if not R:
        raise Vdyt2Hata(f"{pazar}: bütün hisseler hatalı; analiz yapılmadı (ilk hatalar: {list(Z.get('hata', {}).items())[:3]})")
    an = E["ana_tanim"] if E["ana_tanim"] in tan else list(tan)[0]; y1u = f"y{int(E['basari1_ufuk'])}"; s1u = f"son{int(E['basari1_ufuk'])}"
    hu = int(E["ana_ufuk"]); out: Dict[str, Any] = {"pazar": pazar, "asama": asama, "donem": [bas, son], "ana_tanim": an}; hip: List[Dict[str, Any]] = []
    E1 = _v2_e1()

    def donemde(D: pd.DataFrame, sn: str) -> pd.DataFrame:
        return D[(D.tarih >= tb) & (D.tarih <= ts) & (D[sn] <= ts)] if len(D) else D

    def ekle(aile: str, id_: str, r: Dict[str, Any], nk: str = "fark", ana: bool = False, beklenen: str = "+") -> None:
        hip.append({"aile": aile, "id": id_, "nokta": r.get(nk), "alt": r.get(nk + "_alt", r.get("alt")) if nk != "fark" else r.get("alt"),
                    "ust": r.get(nk + "_ust", r.get("ust")) if nk != "fark" else r.get("ust"), "p": r.get(nk + "_p", r.get("p")) if nk != "fark" else r.get("p"),
                    "ana": bool(ana), "beklenen_isaret": beklenen, "n": r.get("n", r.get("n1"))})
    # ---- tablolar
    BOL = {ad: _v2_birlestir(R, "bolge", ad) for ad in tan}
    SAT = {ad: _v2_hazirla(_v2_birlestir(R, "satir", ad), E) for ad in tan}
    KON = {ad: _v2_hazirla(_v2_birlestir(R, "kontrol", ad), E) for ad in tan}
    BHU = pd.concat([h["bhu"] for h in R if h.get("bhu") is not None and len(h["bhu"])], ignore_index=True) if any(
        h.get("bhu") is not None and len(h["bhu"]) for h in R) else pd.DataFrame()
    for ad in tan:
        if len(BOL[ad]):
            BOL[ad].assign(tanim=ad).to_csv(os.path.join(ara, f"bolge_{pazar}_{ad}.csv.gz"), index=False)
    ince = ["sembol", "kaynak", "bolge", "bas", "t", "yas", "tarih", "P1", "P2", "natr_d", "y5", "y10", "y20", "son5", "son10", "son20", "g", "e", "yon",
            "g_tarih", "buyukluk10", "r5", "r10", "r20", "rk5", "rk10", "rk20", "mfe", "mae", "sv_seviye", "pazar_yon"]
    for ad in tan:
        for nm, D in (("satir", SAT[ad]), ("kontrol", KON[ad])):
            if len(D):
                D[[c for c in ince if c in D]].reset_index().to_csv(os.path.join(ara, f"{nm}_{pazar}_{ad}.csv.gz"), index=False)
    if len(SAT.get(an, [])):
        SAT[an].to_pickle(os.path.join(ara, f"satir_tam_{pazar}_{an}.pkl"))
    # ---- BAŞARI (1): bölgeyi önceden bulmak (KARAR: ANA tanım, P1; iki kontrolün İKİSİ)
    b1 = []
    for ad, Tn in tan.items():
        Dg = donemde(SAT[ad], s1u); Dk = donemde(KON[ad], s1u)
        for p in E["onkosul"]["alt_kumeler"]:
            g_ = Dg[_v2_alt(Dg, p)] if len(Dg) else Dg; k_ = Dk[_v2_alt(Dk, p)] if len(Dk) else Dk
            for kn, tab in (("DISARI", ["sembol", "yil", "natr_d"]), ("RASTGELE", ["yil", "yas"])):
                kk = k_[k_.kaynak == kn] if len(k_) else k_
                r = v2_oran_karsilastir(g_, kk, y1u, tab, E) if len(g_) and len(kk) else {"fark": np.nan, "n1": len(g_), "n0": len(kk)}
                r.update({"tanim": ad, "rol": Tn["rol"], "onkosul": p, "kontrol": kn, "ana": bool(ad == an and p == E["onkosul"]["ana"])}); b1.append(r)
                ekle("F1_BOLGE", f"B1-{pazar}-{ad}-{p}-{kn}", r, ana=r["ana"])
            if pazar == "BIST_K62" and len(g_):   # yanlılık kontrolü: kotasyondan çıkanlar (son barı kesikten 30+ gün önce) / yaşayanlar
                cik = {s for s, m in Z["F"]["meta"].items() if m.get("son") is not None and pd.Timestamp(m["son"]) < pd.Timestamp(E["kesik"]) - pd.Timedelta(days=30)}
                for grp, ms in (("cikmis", g_.sembol.isin(cik)), ("yasayan", ~g_.sembol.isin(cik))):
                    kk = k_[(k_.kaynak == "RASTGELE") & (k_.sembol.isin(cik) == (grp == "cikmis"))] if len(k_) else k_
                    r = v2_oran_karsilastir(g_[ms], kk, y1u, ["yil", "yas"], E) if ms.any() and len(kk) else {"fark": np.nan}
                    r.update({"tanim": ad, "onkosul": p, "kontrol": f"RASTGELE_{grp}", "ana": False}); b1.append(r)
    out["basari1"] = pd.DataFrame(b1)
    # duyarlılık / kaçırılan / uyarı süresi / kapsama / yanlış bölge (BİLGİ)
    duy = []
    if len(BHU):
        Bp = BHU[(BHU.tarih >= tb) & (BHU.e_tarih <= ts)]
        for ad in tan:
            if f"tespit_{ad}" not in Bp:
                continue
            kap = pd.concat([h["kapsama"][ad] for h in R if ad in h.get("kapsama", {})]).groupby(level=0).sum() if any(ad in h.get("kapsama", {}) for h in R) else pd.DataFrame()
            kap = kap[(kap.index >= tb.year) & (kap.index <= ts.year)] if len(kap) else kap
            kps = float(kap.acik.sum() / kap.gun.sum()) if len(kap) and kap.gun.sum() > 0 else np.nan
            for p in ("P0", "P1"):
                tes = Bp[f"tespit_{ad}"].to_numpy(bool) & ((Bp[f"p1_{ad}"].to_numpy(float) == 1) if p == "P1" else True)
                uy_ = Bp[f"uyari_{ad}"].to_numpy(float)[tes]
                Dg = donemde(SAT[ad], s1u); Dg = Dg[_v2_alt(Dg, p)] if len(Dg) else Dg
                ilk = Dg.sort_values("yas").groupby(["sembol", "bolge"]).head(1) if len(Dg) else Dg
                duy.append({"tanim": ad, "onkosul": p, "bhu": int(len(Bp)), "onceden_tespit": int(tes.sum()), "kacirilan": int(len(Bp) - tes.sum()),
                            "duyarlilik": float(tes.mean()) if len(Bp) else np.nan, "kapsama_P0": kps,
                            "kaldirac_P0": float(tes.mean() / kps) if (p == "P0" and len(Bp) and kps and np.isfinite(kps)) else np.nan,
                            "uyari_q25": float(np.percentile(uy_, 25)) if len(uy_) else np.nan, "uyari_medyan": float(np.median(uy_)) if len(uy_) else np.nan,
                            "uyari_q75": float(np.percentile(uy_, 75)) if len(uy_) else np.nan,
                            "yanlis_bolge_payi": float((ilk[y1u] == 0).sum() / ilk[y1u].notna().sum()) if len(ilk) and ilk[y1u].notna().sum() else np.nan,
                            "bolge_ilk_satir": int(ilk[y1u].notna().sum()) if len(ilk) else 0})
        Bp.to_csv(os.path.join(ara, f"bhu_{pazar}.csv.gz"), index=False)
    out["duyarlilik"] = pd.DataFrame(duy)
    # ---- BAŞARI (2) genişleme ve (3) yön: ANA ve AILE tanımları
    m2, m3, kal, olg, kpk, tahm1 = [], [], {}, [], {}, {}
    temel_g = {"T0": E["temel"]["G_T0"], "T1": E["temel"]["G_T1"]}
    for ad, Tn in tan.items():
        if Tn["rol"] not in ("ANA", "AILE"):
            continue
        D = SAT[ad]
        if not len(D) or not set(v2_kolon(list(VDYT2_OZELLIK))) <= set(D.columns):
            continue
        ana_mi = Tn["rol"] == "ANA"
        for hh in E["ufuk"]:
            y, sn = f"y{hh}", f"son{hh}"
            mod = {"M_TAM": v2_kolon(list(VDYT2_OZELLIK))}
            if ana_mi:
                mod.update({k: v2_kolon(g) for k, g in VDYT2_MODEL["genisleme"].items() if k != "M_TAM"})
                if hh == hu:
                    mod.update({f"M_EKSI_{g}": v2_kolon([x for x in VDYT2_OZELLIK if x != g]) for g in VDYT2_OZELLIK})
                    mod.update({f"M_TEK_{g}": v2_kolon([g]) for g in VDYT2_OZELLIK})
            P, kay, kat = v2_wf(D, y, sn, mod, {}, yillar, son, E, katsayi=(ana_mi and hh == hu))
            if not len(P):
                continue
            for p in E["onkosul"]["alt_kumeler"]:
                Ds = D[_v2_alt(D, p)]
                Pt, _k, _ = v2_wf(Ds, y, sn, {}, temel_g, yillar, son, E)
                if not len(Pt):
                    continue
                Pp = P.join(Pt.set_index("satir")[[c for c in Pt if c.startswith("p_")]], on="satir", how="inner")
                for m in [k for k in mod]:
                    for t0 in (("T1", "T0") if (m in VDYT2_MODEL["genisleme"] or m.startswith("M_TEK")) else ("T1",)):
                        if m.startswith("M_EKSI"):
                            continue
                        r = v2_degerlendir(Pp, D, y, m, t0, E); r.update({"tanim": ad, "onkosul": p, "ufuk": hh, "yillar": kay if m == "M_TAM" else None})
                        ana = bool(ana_mi and p == E["onkosul"]["ana"] and hh == hu and m == "M_TAM" and t0 == "T1")
                        r["ana"] = ana; m2.append(r)
                        aile = "F2_GENISLEME" if m == "M_TAM" else ("F5_SURE" if m in VDYT2_MODEL["genisleme"] else "F6_TEK_GRUP")
                        ekle(aile, f"M1-{pazar}-{ad}-{p}-y{hh}-{m}-vs-{t0}", r, "brier_skill", ana)
                    if m.startswith("M_EKSI"):
                        r = v2_degerlendir(Pp, D, y, "M_TAM", m, E); r.update({"tanim": ad, "onkosul": p, "ufuk": hh, "katki": m[7:], "ana": False}); m2.append(r)
                        ekle("F6_KATKI", f"M1-{pazar}-{ad}-{p}-katki-{m[7:]}", r, "brier_skill")
                if ana_mi and hh == hu:
                    kal[f"{ad}-{p}"] = v2_degerlendir(Pp, D, y, "M_TAM", "T1", E).get("kalibrasyon")
                    # D1b: aynı model kontrol satırlarında (DIŞARI, RASTGELE): kendi WF'si, kendi T1 temeli; skill farkı ortak bootstrap
                    for kn in ("DISARI", "RASTGELE"):
                        K_ = KON[ad][KON[ad].kaynak == kn] if len(KON[ad]) else KON[ad]
                        if not len(K_) or not set(mod["M_TAM"]) <= set(K_.columns):
                            continue
                        if (kn, hh) not in kpk:   # kontrol modeli alt kümeden bağımsız (P0 satırlarıyla), bir kez
                            kpk[(kn, hh)] = v2_wf(K_, y, sn, {"M_TAM": mod["M_TAM"]}, {}, yillar, son, E)[0]
                        Pk = kpk[(kn, hh)]
                        Ks = K_[_v2_alt(K_, p)]; Pkt, _k2, _ = v2_wf(Ks, y, sn, {}, temel_g, yillar, son, E)
                        if not len(Pk) or not len(Pkt):
                            continue
                        Pkp = Pk.join(Pkt.set_index("satir")[[c for c in Pkt if c.startswith("p_")]], on="satir", how="inner")
                        rk = v2_degerlendir(Pkp, K_, y, "M_TAM", "T1", E); rk.update({"tanim": ad, "onkosul": p, "ufuk": hh, "kontrol": kn, "ana": False}); m2.append(rk)
                        f_ = v2_skill_fark(Pp, D, Pkp, K_, y, "M_TAM", "T1", E); f_.update({"tanim": ad, "onkosul": p, "kontrol": kn,
                                                                                           "ana": bool(p == E["onkosul"]["ana"])})
                        out.setdefault("d1b", []).append(f_)
                        ekle("F2_D1B", f"D1b-{pazar}-{ad}-{p}-{kn}", f_, ana=f_["ana"])
                    # sınıf değerlendirmesi (bilgi; eşikler yalnız o yılın eğitiminden)
                    if p == "P0":
                        out["katsayi"] = kat
                if ana_mi and p == "P0":
                    tahm1[(ad, hh)] = Pp
                    if hh == hu:
                        Pp.assign(sembol=D.loc[Pp.satir, "sembol"].values, tarih=D.loc[Pp.satir, "tarih"].values, y=D.loc[Pp.satir, y].values,
                                  P1=D.loc[Pp.satir, "P1"].values).to_csv(os.path.join(ara, f"tahmin_m1_{pazar}_{ad}_y{hh}.csv.gz"), index=False)
            if ana_mi and hh == hu:
                # olgunlaşma (D2): yaş >= 30 karar noktalarının y10 oranı - yaş 10-15 noktalarının; hisse kümeli
                Dd = donemde(D, sn)
                for p in E["onkosul"]["alt_kumeler"]:
                    Ds = Dd[_v2_alt(Dd, p)]
                    g = np.where(Ds.yas >= 30, 1.0, np.where(Ds.yas <= 15, 0.0, np.nan))
                    r = V1.vdyt_bootstrap_fark(Ds.sembol.to_numpy(), Ds[y].to_numpy(float), g, int(Bb["bootstrap"]), int(Bb["tohum"]), tuple(Bb["guven"]))
                    r.update({"tanim": ad, "onkosul": p}); olg.append(r); ekle("F5_SURE", f"OLG-{pazar}-{ad}-{p}", r)
        # ---- (3) YÖN: büyük harekete dönüşen (y20 = 1, yön ±1) geçerli karar günleri
        D2 = D[(D.y20 == 1) & D.yukari.notna()]
        if len(D2):
            mod2 = {k: v2_kolon(g) for k, g in VDYT2_MODEL["yon"].items()}
            if ana_mi:
                mod2.update({f"M_EKSI_{g}": v2_kolon([x for x in VDYT2_OZELLIK if x != g]) for g in VDYT2_OZELLIK})
            P2, kay2, _ = v2_wf(D2, "yukari", "son20", mod2, {}, yillar, son, E)
            if len(P2):
                for p in E["onkosul"]["alt_kumeler"]:
                    Ds = D2[_v2_alt(D2, p)]
                    Pt, _k, _ = v2_wf(Ds, "yukari", "son20", {}, {"B0": E["temel"]["Y_B0"], "B1": E["temel"]["Y_B1"]}, yillar, son, E)
                    if not len(Pt):
                        continue
                    Pp = P2.join(Pt.set_index("satir")[["p_B0", "p_B1"]], on="satir", how="inner")
                    for m, t0, aile in (("M_TAM", "B1", "F3_YON"), ("M_TAM", "B0", "F3_YON"), ("M_TAM", "B2_KONUM", "F3_YON"), ("M_KONUMSUZ", "B1", "F3_YON"),
                                        ("B2_KONUM", "B1", "F3_YON")):
                        r = v2_degerlendir(Pp, D2, "yukari", m, t0, E, yon=True); ana = bool(ana_mi and p == E["onkosul"]["ana"] and m == "M_TAM" and t0 == "B1")
                        r.update({"tanim": ad, "onkosul": p, "ana": ana, "yillar": kay2 if (m == "M_TAM" and t0 == "B1") else None}); m3.append(r)
                        ekle(aile, f"M2-{pazar}-{ad}-{p}-{m}-vs-{t0}", r, "brier_skill", ana)
                        if m == "M_TAM" and t0 == "B1":
                            ekle(aile, f"M2BA-{pazar}-{ad}-{p}-{m}-vs-{t0}", r, "ba_fark", ana)
                    if ana_mi:
                        for g in VDYT2_OZELLIK:
                            r = v2_degerlendir(Pp, D2, "yukari", "M_TAM", f"M_EKSI_{g}", E, yon=True); r.update({"tanim": ad, "onkosul": p, "katki": g, "ana": False})
                            m3.append(r); ekle("F6_KATKI", f"M2-{pazar}-{ad}-{p}-katki-{g}", r, "brier_skill")
                        # işlem sonucu (bilgi): tahmin edilen yöne göre işaretli getiri, maliyet sonrası; M_TAM - B1
                        Q = Pp.assign(**{k: D2.loc[Pp.satir, k].values for k in ("sembol", "r5", "r10", "r20", "rk5", "rk10", "rk20", "mfe", "mae", "yukari")})
                        msk = _v2_alt(D2.loc[Pp.satir], p)
                        isl = {"onkosul": p, "tanim": ad, "n": int(msk.sum())}
                        for k in ("r5", "r10", "r20", "rk5", "rk10", "rk20"):
                            sm = np.where(Q.p_M_TAM >= 0.5, 1.0, -1.0) * Q[k]; s0 = np.where(Q.p_B1 >= 0.5, 1.0, -1.0) * Q[k]
                            ok = msk & np.isfinite(Q[k].to_numpy(float))
                            isl[f"{k}_M_TAM"] = float(np.mean(sm[ok])) if ok.any() else np.nan; isl[f"{k}_B1"] = float(np.mean(s0[ok])) if ok.any() else np.nan
                            if ok.sum() >= 30:
                                rr = V1.vdyt_bootstrap_fark(np.r_[Q.sembol[ok], Q.sembol[ok]], np.r_[sm[ok], s0[ok]], np.r_[np.ones(ok.sum()), np.zeros(ok.sum())],
                                                            int(Bb["bootstrap"]), int(Bb["tohum"]), tuple(Bb["guven"]))
                                isl[f"{k}_fark_alt"] = rr.get("alt"); isl[f"{k}_fark_ust"] = rr.get("ust")
                        isl["mfe_ort"] = float(np.nanmean(Q.mfe[msk])) if msk.any() else np.nan; isl["mae_ort"] = float(np.nanmean(Q.mae[msk])) if msk.any() else np.nan
                        out.setdefault("islem", []).append(isl)
                        if p == "P0":
                            Pp.assign(sembol=D2.loc[Pp.satir, "sembol"].values, tarih=D2.loc[Pp.satir, "tarih"].values, y=D2.loc[Pp.satir, "yukari"].values,
                                      P1=D2.loc[Pp.satir, "P1"].values).to_csv(os.path.join(ara, f"tahmin_m2_{pazar}_{ad}.csv.gz"), index=False)
            # birleşik üç sınıf (BİLGİ): 20 gün içinde {yukarı BH, aşağı BH, yok}; M = p20 x p_yukarı vs T1 x B1 (P0 temelleri), çok sınıflı Brier skill
            if ana_mi and (ad, 20) in tahm1:
                Dall = D[D.y20.notna() & ((D.y20 == 0) | D.yukari.notna())]
                P3, _k3, _ = v2_wf(D2, "yukari", "son20", {"M_TAM": v2_kolon(list(VDYT2_OZELLIK))}, {"B1": E["temel"]["Y_B1"]}, yillar, son, E, Dtest=Dall)
                if len(P3):
                    P3 = P3.set_index("satir")[["p_M_TAM", "p_B1"]].join(tahm1[(ad, 20)].set_index("satir")[["p_M_TAM", "p_T1"]].rename(
                        columns={"p_M_TAM": "g_m", "p_T1": "g_0"}), how="inner")
                    yy = Dall.loc[P3.index]; yu = ((yy.y20 == 1) & (yy.yukari == 1)).astype(float).to_numpy()
                    ya_ = ((yy.y20 == 1) & (yy.yukari == 0)).astype(float).to_numpy(); yd = 1 - yu - ya_

                    def br(g: np.ndarray, u: np.ndarray) -> np.ndarray:
                        return (g * u - yu) ** 2 + (g * (1 - u) - ya_) ** 2 + ((1 - g) - yd) ** 2
                    lm, l0 = br(P3.g_m.to_numpy(), P3.p_M_TAM.to_numpy()), br(P3.g_0.to_numpy(), P3.p_B1.to_numpy()); bl_ = []
                    for p in ("P0", "P1"):
                        mk = _v2_alt(yy, p)
                        if mk.sum() >= 30:
                            bl_.append({"tanim": ad, "onkosul": p, "n": int(mk.sum()), **V1._vdyt_bs_oran(yy.sembol.to_numpy()[mk], lm[mk], l0[mk], int(Bb["bootstrap"]),
                                                                                                        int(Bb["tohum"]), tuple(Bb["guven"]))})
                    out["birlesik"] = bl_
    out["basari2"] = pd.DataFrame(m2); out["basari3"] = pd.DataFrame(m3); out["kalibrasyon"] = kal; out["olgunlasma"] = pd.DataFrame(olg)
    out["d1b"] = pd.DataFrame(out.get("d1b", [])); out["islem"] = pd.DataFrame(out.get("islem", []))
    # ---- SÜRE (bölge başına): KM / CIF / yaş hazard'ı (ANA, P0 ve P1); WF'de 2023 sonu sansür
    sure = []
    if len(BOL.get(an, [])):
        T = BOL[an]; T = T[T.uygun_tespit & (T.tespit_tarih >= (pd.Timestamp("1900-01-01") if asama == "wf" else tb)) & (T.tespit_tarih <= ts)].copy()
        tur = np.where((T.bit_tur == BIT_BUYUK) & (T.onay == 1), V1.BITIS_GEN, np.where((T.bit_tur == BIT_SANSUR) | (T.onay == -1), V1.BITIS_SANSUR, V1.BITIS_SONME))
        gecti = (T.bit_tarih + pd.Timedelta(days=14) > ts).to_numpy()
        kes_su = np.busday_count(T.bas_tarih.to_numpy("datetime64[D]"), np.datetime64(ts.date()) + 1)
        tur = np.where(gecti, V1.BITIS_SANSUR, tur); su = np.where(gecti, np.minimum(T.sure.to_numpy(), kes_su), T.sure.to_numpy())
        for p in ("P0", "P1"):
            m_ = _v2_alt(T, p); Sk = V1.vdyt_sureklilik(su[m_], tur[m_], int(E["sessiz"]["L"]))
            Sk.to_csv(os.path.join(ara, f"sure_{pazar}_{an}_{p}.csv"), index=False)
            row = {"tanim": an, "onkosul": p, "bolge": int(m_.sum())}
            for a in (15, 20, 30, 45, 60, 90):
                row[f"cif_bh_{a}"] = float(Sk.cif_gen[Sk.yas <= a].iloc[-1]) if (Sk.yas <= a).any() else np.nan
            kv = V1.vdyt_yas_kova(Sk.yas, {"yas_kova": E["yas_kova"]})
            for i, (a, b) in enumerate(E["yas_kova"]):
                mm = kv == i; row[f"hazard_{a}_{b}"] = float(Sk.gen[mm].sum() / Sk.risk[mm].sum()) if Sk.risk[mm].sum() > 0 else np.nan
            sure.append(row)
    out["sure"] = pd.DataFrame(sure)
    # ---- OLAYLAR (ANA): E1 / E2 (haber bitirdi mi, zaten bitecek miydi: eşlenmiş olaysız kontroller), haberli / habersiz, plasebo eşiği
    ol = []
    if pazar != "BIST_K62":
        turler = sorted({t for h in R for t in h["havuz"].get("_ortak", {}).get("ti", {})})
        E1o = {**E1, "olay": E["olay"]}
        for tur_ in turler:
            for kip in ("e1", "e2"):
                r = V1.vdyt_olay_analizi(R, an, tur_, kip, E1o, donem=(bas, son))
                for x in r.get("tablo", []):
                    ol.append({"tur": tur_, "kip": kip, "olay_toplam": r["olay_toplam"], "olay_kullanilan": r["olay_kullanilan"], "kontrolsuz": r["kontrolsuz"], **x})
                    if x["pencere"] != "yok":
                        hip.append({"aile": "F4_OLAY", "id": f"{kip.upper()}-{pazar}-{an}-{tur_}-{x['pencere']}", "nokta": x["fark"], "alt": x["alt"], "ust": x["ust"],
                                    "p": x["p"], "ana": False})
        out["olay"] = pd.DataFrame(ol)
        out["plasebo"] = v2_plasebo_olay(R, an, [t for t in turler if not t.startswith("MAKRO")], E, (bas, son), p1_tekrar)
        # haberli / habersiz (BH'ye dönüşen ANA satırları; g'ye göre): yön payı, büyüklük; yön motoru dengeli doğruluğu ayrı ayrı (bilgi)
        D = donemde(SAT[an], "son20"); hb = []
        if len(D):
            ti = {h["sembol"]: h["havuz"].get("_ortak", {}).get("ti", {}) for h in R}
            sp = [k for k in V1.VDYT_OLAY_TUR if not k.startswith("MAKRO") and V1.VDYT_OLAY_TUR[k]["kat"] in ("A", "B")]
            Dh = D[(D.y20 == 1) & D.yukari.notna()]
            H_ = E["haber"]; fl = []
            for r_ in Dh.itertuples():
                T_ = ti.get(r_.sembol, {}); g = int(r_.g)
                var = lambda ks, a, b: any(np.any((T_.get(k, np.zeros(0)) >= g + a) & (T_.get(k, np.zeros(0)) <= g + b)) for k in ks)   # noqa: E731
                fl.append((float(var(sp, *H_["haberli"])), float((not var(sp, *H_["habersiz"])) and not var(["MAKRO_FOMC", "MAKRO_PPK", "MAKRO_EMTIA"], *H_["makro"]))))
            if fl:
                Dh = Dh.assign(haberli=[a for a, _b in fl], habersiz=[b for _a, b in fl])
                ym2 = os.path.join(ara, f"tahmin_m2_{pazar}_{an}.csv.gz")
                if os.path.exists(ym2):   # yön motorunun haberli / habersiz satırlardaki dengeli doğruluğu (BİLGİ)
                    Q2 = pd.read_csv(ym2).set_index("satir").join(Dh[["haberli", "habersiz"]], how="inner")
                    for grp in ("haberli", "habersiz"):
                        q = Q2[Q2[grp] == 1]
                        if len(q) >= 30:
                            hb.append({"olcu": f"yon_BA_{grp}", "n1": int(len(q)), "ba_M_TAM": V1.vdyt_dengeli_dogruluk(q.y.to_numpy(float), q.p_M_TAM.to_numpy(float)),
                                       "ba_B1": V1.vdyt_dengeli_dogruluk(q.y.to_numpy(float), q.p_B1.to_numpy(float))})
                Dg = Dh.sort_values("yas").groupby(["sembol", "bolge"]).tail(1)
                Dg[["sembol", "bolge", "t", "g", "g_tarih", "yon", "buyukluk10", "haberli", "habersiz", "P1"]].to_csv(os.path.join(ara, f"haber_{pazar}_{an}.csv.gz"), index=False)
                g = np.where(Dg.haberli == 1, 1.0, np.where(Dg.habersiz == 1, 0.0, np.nan))
                w = V1.vdyt_tabakali_agirlik(g, Dg[["yil", "mom_t", "liq_t"]].fillna(-1))
                for olc in ("yukari", "buyukluk"):
                    a = Dg.yukari.to_numpy(float) if olc == "yukari" else np.abs(Dg.buyukluk10.to_numpy(float))
                    r = V1.vdyt_bootstrap_fark(Dg.sembol.to_numpy(), a, np.where(w > 0, g, np.nan), int(Bb["bootstrap"]), int(Bb["tohum"]), tuple(Bb["guven"]), agirlik=w)
                    r.update({"olcu": olc}); hb.append(r); ekle("F4_OLAY", f"K1-{pazar}-{an}-{olc}", r)
        out["haber"] = pd.DataFrame(hb)
        OE = pd.concat([h["olay_es"] for h in R if isinstance(h.get("olay_es"), pd.DataFrame) and len(h["olay_es"])], ignore_index=True) if any(
            isinstance(h.get("olay_es"), pd.DataFrame) and len(h["olay_es"]) for h in R) else pd.DataFrame()
        if len(OE):
            OE = OE[(OE.olay_tarih >= (tb if asama == "kasa" else pd.Timestamp("1900-01-01"))) & (OE.olay_tarih <= ts)]
            OE.to_csv(os.path.join(ara, f"olay_eslesme_{pazar}_{an}.csv.gz"), index=False)
            out["olay_eslesme"] = OE.groupby("tur").agg(cift=("bolge", "size"), yas_medyan=("yas_olayda", "median"),
                                                         bh_gun_medyan=("olay_gen_gun", "median"), bh_olan=("olay_gen_gun", "count")).reset_index()
    # ---- SINIF DEĞERLENDİRMESİ (bilgi; yön kapısı uygulanmadan, eşikler o yılın eğitiminden)
    y_m1 = os.path.join(ara, f"tahmin_m1_{pazar}_{an}_y{hu}.csv.gz"); y_m2 = os.path.join(ara, f"tahmin_m2_{pazar}_{an}.csv.gz")
    if os.path.exists(y_m1) and len(SAT.get(an, [])):
        P1_ = pd.read_csv(y_m1); P2_ = pd.read_csv(y_m2) if os.path.exists(y_m2) else pd.DataFrame(columns=["satir", "p_M_TAM"])
        Dn = SAT[an].loc[P1_.satir]
        Pb = P1_.merge(P2_[["satir", "p_M_TAM"]].rename(columns={"p_M_TAM": "p_yukari"}), on="satir", how="left")
        S_ = E["sinif"]; ya = Pb.p_M_TAM >= Pb.q80_M_TAM
        sinif = np.where(~ya, "Sıkışma devam ediyor", np.where(Pb.p_yukari >= S_["yukari"], "Yukarı kırılma adayı",
                                                               np.where(Pb.p_yukari <= S_["asagi"], "Aşağı kırılma adayı", "Genişlemeye yaklaşan sıkışma")))
        Ct = pd.DataFrame({"sinif": sinif, "y10": Dn.y10.values, "y20": Dn.y20.values, "yukari": Dn.yukari.values, "P1": Dn.P1.values})
        out["sinif"] = Ct.groupby("sinif").agg(n=("y10", "size"), y10_oran=("y10", "mean"), y20_oran=("y20", "mean"), yukari_payi=("yukari", "mean")).reset_index()
    # ---- çoklu test
    H = pd.DataFrame(hip)
    if len(H):
        H["bh_ret"] = False
        for a, g in H.groupby("aile"):
            H.loc[g.index, "bh_ret"] = V1.vdyt_bh(g.p.to_numpy(float), float(E["coklu"]["bh_q"]))
    out["hipotez"] = H
    return out


def v2_plasebo_olay(R: List[Dict[str, Any]], ad: str, turler: List[str], E: Dict[str, Any], donem: Tuple[str, str], tekrar: Optional[int] = None) -> Dict[str, Any]:
    """D4 plasebo P1: her hissede gerçek olay sayısı kadar tekdüze rastgele 'olay' günü (260 .. n-22), E1 ve E2 aynı yöntemle (V1.vdyt_olay_analizi). Döner:
    tekrar başına BH keşif sayısı (yanlış pozitif) ve tür x kip x pencere başına |fark|'ın plasebo_esik_pct yüzdeliği (bir olay bulgusu ancak WF |fark|'ı bu
    eşiği aşarsa sayılır)."""
    tekrar = int(tekrar if tekrar is not None else E["coklu"]["plasebo_olay_tekrar"]); E1o = {**_v2_e1(), "olay": E["olay"]}; sat = []; fk: Dict[str, List[float]] = {}
    for rep in range(tekrar):
        ps = []
        for tur in turler:
            ol = {}
            for si, h in enumerate(R):
                ii = h["havuz"].get("_ortak", {}).get("ti", {}).get(tur)
                if ii is None or not len(ii) or ad not in h["havuz"]:
                    continue
                n = len(h["havuz"][ad]["acik"])
                if n - 22 <= 260:
                    continue
                rg = np.random.default_rng(_v2_tohum(h["sembol"], tur, rep, E["coklu"]["tohum"]))
                ol[si] = np.unique(rg.integers(260, n - 22, size=len(ii)))
            for kip in ("e1", "e2"):
                r = V1.vdyt_olay_analizi(R, ad, tur, kip, E1o, olaylar=ol, ust=int(E["coklu"]["plasebo_ust"]), tohum=_v2_tohum(tur, kip, rep, "P1"), donem=donem)
                for x in r.get("tablo", []):
                    if x["pencere"] != "yok":
                        ps.append(x["p"]); fk.setdefault(f"{kip.upper()}|{tur}|{x['pencere']}", []).append(abs(float(x["fark"])))
        p_ = np.array(ps, float); ret = V1.vdyt_bh(p_, float(E["coklu"]["bh_q"]))
        sat.append({"tekrar": rep, "test": int(np.isfinite(p_).sum()), "kesif": int(ret.sum()), "ham_p_lt_005": int(np.sum(p_ < 0.05))})
    T = pd.DataFrame(sat)
    return {"tekrar": T, "yanlis_pozitif_orani": float((T.kesif > 0).mean()) if len(T) else np.nan,
            "esik": {k: float(np.percentile(v, float(E["coklu"]["plasebo_esik_pct"]))) for k, v in fk.items() if len(v)}}


# ---------------------------------------------------------------- 9) ÖN KAYIT, MÜHÜR, GİT KAPISI, KOŞU, KARAR TABLOSU
def _v2_onkayit_oku(yol: str) -> Dict[str, Any]:
    with open(yol, encoding="utf-8") as f:
        m = f.read()
    a = re.search(r"^ESIK_SHA256: ([0-9a-f]{64})$", m, re.M); k = re.search(r"^KOD_SHA256: ([0-9a-f]{64})$", m, re.M)
    k1 = re.search(r"^VDYT_KOD_SHA256: ([0-9a-f]{64})$", m, re.M); z = re.search(r"^Yazım zamanı: (.+)$", m, re.M)
    veri = {x: (h, int(n)) for x, h, n in re.findall(r"^- ([\w.\-]+): sha256 ([0-9a-f]{64}|YOK) \((\d+) dosya\)$", m, re.M)}
    return {"esik": a.group(1) if a else None, "kod": k.group(1) if k else None, "kod_v1": k1.group(1) if k1 else None, "zaman": z.group(1) if z else "", "veri": veri}


def v2_onkayit(cikti: Optional[str] = None, kapsam: Optional[Dict[str, Any]] = None, veri_sha: Optional[Dict[str, Tuple[str, int]]] = None) -> str:
    """Ön kaydı yazar. Dosya varsa ÜZERİNE YAZMAZ (mühür ve kodlar aynıysa yolu döndürür, değilse durur). kapsam None ise vdyt2_kapsam.json okunur."""
    yol = _v2_yol("onkayit", cikti)
    if os.path.exists(yol):
        oc = _v2_onkayit_oku(yol)
        if oc["esik"] != v2_esik_sha() or oc["kod"] != v2_kod_sha() or oc["kod_v1"] != v2_v1_kod_sha():
            raise Vdyt2Hata(f"ön kayıt zaten var ve mühür / kod farklı (esik {oc['esik']} / {v2_esik_sha()}, kod {oc['kod']} / {v2_kod_sha()}); üzerine yazılmadı")
        vdyt2log.info("ön kayıt zaten var (mühür ve kodlar aynı): %s", yol); return yol
    if kapsam is None and os.path.exists(_v2_yol("kapsam", cikti)):
        kapsam = _v2_json_oku(_v2_yol("kapsam", cikti))
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    _v2_yaz(yol, v2_onkayit_metin(zaman, v2_veri_sha() if veri_sha is None else veri_sha, kapsam))
    vdyt2log.info("ön kayıt yazıldı: %s (mühür %s, kod %s)", yol, v2_esik_sha()[:12], v2_kod_sha()[:12])
    return yol


def v2_git_islenmis(yol: str, ne: str) -> Dict[str, str]:
    try:
        return V1.vdyt_git_islenmis(yol, ne)
    except V1.VdytHata as ex:
        raise Vdyt2Hata(str(ex)) from None


def v2_onkayit_dogrula(cikti: Optional[str] = None, veri: bool = True, git: bool = True) -> Dict[str, Any]:
    """`kos` / `canli` kapısı: ön kayıt var; eşik mührü, VDYT2.py ve VDYT.py sha256'ları ön kayıttakiyle aynı; (veri) veri sha256'ları aynı; (git) ön kayıt,
    VDYT2.py ve VDYT.py git'e işlenmiş ve sonra değişmemiş. Biri tutmazsa Vdyt2Hata (REDDEDİLİR)."""
    yol = _v2_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise Vdyt2Hata(f"ön kayıt yok ({yol}): önce `python VDYT2.py onkayit`; koşu REDDEDİLDİ")
    oc = _v2_onkayit_oku(yol)
    if oc["esik"] != v2_esik_sha():
        raise Vdyt2Hata(f"eşik mührü tutmuyor ({oc['esik']} != {v2_esik_sha()}): eşikler ön kayıttan sonra değişmiş; koşu REDDEDİLDİ")
    if oc["kod"] != v2_kod_sha():
        raise Vdyt2Hata(f"VDYT2.py sha256 ön kayıttakiyle aynı değil ({oc['kod']} != {v2_kod_sha()}): kod değişmiş; SAPMA yazılıp ön kayıt yeniden işlenmeli; REDDEDİLDİ")
    if oc["kod_v1"] != v2_v1_kod_sha():
        raise Vdyt2Hata(f"VDYT.py sha256 ön kayıttakiyle aynı değil ({oc['kod_v1']} != {v2_v1_kod_sha()}): içe aktarılan v1 kodu değişmiş; REDDEDİLDİ")
    out = {"yol": yol, "esik": oc["esik"], "kod": oc["kod"], "kod_v1": oc["kod_v1"], "zaman": oc["zaman"], "dosya_sha256": V1.vdyt_sha_dosya(yol)}
    if veri:
        simdi = v2_veri_sha(); fark = sorted(k for k in set(simdi) | set(oc["veri"]) if tuple(simdi.get(k, ("", -1))) != tuple(oc["veri"].get(k, ("", -1))))
        if fark:
            raise Vdyt2Hata(f"veri ön kayıttakiyle aynı değil (sha256 / dosya sayısı): {fark}; koşu REDDEDİLDİ")
    if git:
        out["git_onkayit"] = v2_git_islenmis(yol, "VDYT2 ön kaydı"); out["git_kod"] = v2_git_islenmis(os.path.join(KOK_VDYT2, "VDYT2.py"), "VDYT2.py")
        out["git_kod_v1"] = v2_git_islenmis(os.path.join(KOK_VDYT2, "VDYT.py"), "VDYT.py")
    return out


def _v2_gecti(r: Optional[Dict[str, Any]], anahtarlar: List[str]) -> Optional[bool]:
    if not r or any(r.get(k) is None or (isinstance(r.get(k), float) and not np.isfinite(r.get(k))) for k in anahtarlar):
        return None
    return bool(all((r.get(k) or -1) > 0 for k in anahtarlar))


def v2_karar_tablosu(wf: Dict[str, Any], kasa: Optional[Dict[str, Any]], E: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """ÜÇ BAŞARI AYRI AYRI, pazar x ön koşul alt kümesi (ANA = P1; P0 / P2 bilgi ama canlı kapısında kullanılır). BAŞARILI ancak WF test yılları toplamında VE
    KASA'da şart tutarsa. (1) DIŞARI ve RASTGELE kontrollerinin İKİSİNDE oran farkı > 0 ve %95 alt > 0. (2) = (2a) M_TAM vs T1 Brier skill > 0 ve alt > 0
    VE (2b, D1b) skill farkı (gerçek - DIŞARI) ve (gerçek - RASTGELE) > 0 ve alt > 0. (3) M_TAM vs B1 Brier skill ve dengeli doğruluk farkı > 0 ve alt > 0."""
    E = E or VDYT2_ESIK; an = E["ana_tanim"]; hu = int(E["ana_ufuk"]); sat = []

    def bul(S: Optional[Dict[str, Any]], pz: str, alan: str, kos: Callable[[Dict[str, Any]], bool]) -> Optional[Dict[str, Any]]:
        if not S or pz not in S.get("pazar", {}):
            return None
        for r in S["pazar"][pz].get(alan) or []:
            if kos(r):
                return r
        return None
    for pz in E["karar_pazari"]:
        for p in E["onkosul"]["alt_kumeler"]:
            d: Dict[str, Any] = {"pazar": pz, "onkosul": p, "ana": p == E["onkosul"]["ana"]}
            for asm, S in (("wf", wf), ("kasa", kasa)):
                b1 = {kn: bul(S, pz, "basari1", lambda r, kn=kn: r.get("tanim") == an and r.get("onkosul") == p and r.get("kontrol") == kn)
                      for kn in ("DISARI", "RASTGELE")}
                g1 = [_v2_gecti({"f": (b or {}).get("fark"), "a": (b or {}).get("alt")}, ["f", "a"]) for b in b1.values()]
                d[f"b1_{asm}"] = None if any(x is None for x in g1) else all(g1)
                d[f"b1_{asm}_detay"] = {kn: {k: (b or {}).get(k) for k in ("ort1", "ort0", "fark", "alt", "ust", "oran", "n1", "n0")} for kn, b in b1.items()}
                r2 = bul(S, pz, "basari2", lambda r: r.get("tanim") == an and r.get("onkosul") == p and r.get("ufuk") == hu and r.get("model") == "M_TAM"
                         and r.get("temel") == "T1" and not r.get("katki") and not r.get("kontrol"))
                g2a = _v2_gecti(r2, ["brier_skill", "brier_skill_alt"])
                db = {kn: bul(S, pz, "d1b", lambda r, kn=kn: r.get("tanim") == an and r.get("onkosul") == p and r.get("kontrol") == kn) for kn in ("DISARI", "RASTGELE")}
                g2b = [_v2_gecti({"f": (b or {}).get("fark"), "a": (b or {}).get("alt")}, ["f", "a"]) for b in db.values()]
                d[f"b2a_{asm}"] = g2a; d[f"b2b_{asm}"] = None if any(x is None for x in g2b) else all(g2b)
                d[f"b2_{asm}_detay"] = {**{k: (r2 or {}).get(k) for k in ("n", "brier_skill", "brier_skill_alt", "brier_skill_ust", "ece")},
                                        "d1b": {kn: {k: (b or {}).get(k) for k in ("skill_a", "skill_b", "fark", "alt")} for kn, b in db.items()}}
                r3 = bul(S, pz, "basari3", lambda r: r.get("tanim") == an and r.get("onkosul") == p and r.get("model") == "M_TAM" and r.get("temel") == "B1"
                         and not r.get("katki"))
                d[f"b3_{asm}"] = _v2_gecti(r3, ["brier_skill", "brier_skill_alt", "ba_fark", "ba_fark_alt"])
                d[f"b3_{asm}_detay"] = {k: (r3 or {}).get(k) for k in ("n", "brier_skill", "brier_skill_alt", "ba_m", "ba_0", "ba_fark", "ba_fark_alt", "ece")}
            for b in ("b1", "b2a", "b2b", "b3"):
                w_, k_ = d.get(f"{b}_wf"), d.get(f"{b}_kasa")
                d[b] = "KASA AÇILMADI" if kasa is None else ("BAŞARILI" if (w_ and k_) else ("VERİ YOK" if (w_ is None or k_ is None) else "BAŞARISIZ"))
            d["b2"] = "KASA AÇILMADI" if kasa is None else ("BAŞARILI" if d["b2a"] == "BAŞARILI" and d["b2b"] == "BAŞARILI" else
                                                            ("VERİ YOK" if "VERİ YOK" in (d["b2a"], d["b2b"]) else "BAŞARISIZ"))
            sat.append(d)
    return sat


def v2_teyit(wf: Dict[str, Any], kasa: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """WF'de BH ile reddedilen her hipotez KASA'da aynı işaretle ve %95 aralığı 0'ı dışlayarak tekrar ederse TUTTU. F4_OLAY ailesinde ayrıca WF |fark| plasebo
    eşiğini (aynı tür x kip x pencere; P1 plasebosunun %95 yüzdeliği) aşmalı (D4); aşmazsa 'PLASEBO EŞİĞİ ALTINDA'."""
    E = E or VDYT2_ESIK; sat = []
    for pz, P in (wf.get("pazar") or {}).items():
        K = {h["id"]: h for h in ((kasa.get("pazar") or {}).get(pz, {}).get("hipotez") or [])}
        es = ((P.get("plasebo") or {}).get("esik") or {})
        for h in P.get("hipotez") or []:
            if not h.get("bh_ret"):
                continue
            k = K.get(h["id"]); n0 = h.get("nokta") or 0.0
            ok = bool(k and k.get("nokta") is not None and np.sign(k["nokta"]) == np.sign(n0) and (
                (n0 > 0 and (k.get("alt") if k.get("alt") is not None else -1) > 0) or (n0 < 0 and (k.get("ust") if k.get("ust") is not None else 1) < 0)))
            sonuc = "TUTTU" if ok else "TUTMADI"
            if ok and h.get("aile") == "F4_OLAY" and re.match(r"^E[12]-", h["id"]):
                kip, _pz, _an, tur, pen = h["id"].split("-", 4)[0], *h["id"].split("-", 4)[1:]
                esk = es.get(f"{kip}|{tur}|{pen}")
                if esk is None or abs(n0) <= esk:
                    sonuc = "PLASEBO EŞİĞİ ALTINDA"
            sat.append({"pazar": pz, "id": h["id"], "aile": h.get("aile"), "wf_nokta": n0, "wf_p": h.get("p"), "kasa_nokta": (k or {}).get("nokta"),
                        "kasa_alt": (k or {}).get("alt"), "kasa_ust": (k or {}).get("ust"), "sonuc": sonuc})
    return sat


def _v2_meta(oc: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    k, h, _e = V1._vdyt_git(["rev-parse", "HEAD"], KOK_VDYT2)
    return {"surum": VDYT2_SURUM, "etiket": VDYT2_ETIKET, "kod_sha256": v2_kod_sha(), "vdyt_kod_sha256": v2_v1_kod_sha(), "esik_sha256": v2_esik_sha(),
            "git_head": h if k == 0 else None, "onkayit_commit": ((oc or {}).get("git_onkayit") or {}).get("commit"), "zaman": _v2_simdi()}


@_v2_sessiz
def v2_kos(asama: str = "wf", cikti: Optional[str] = None, isci: int = 3, git_sart: bool = True, veri_sart: bool = True, pazarlar: Optional[List[str]] = None,
           girdi: Optional[Dict[str, Tuple[Dict[str, Any], pd.DataFrame]]] = None, p1_tekrar: Optional[int] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Faz 2 ölçümü. Önce v2_onkayit_dogrula (ret kapısı). 'kasa' yalnız 'wf' sonucu varken ve KASA daha önce açılmamışsa (işaret dosyası; TEK AÇILIŞ)."""
    E = E or VDYT2_ESIK; t0 = time.time(); bas = _v2_simdi()
    if asama not in ("wf", "kasa"):
        raise Vdyt2Hata(f"aşama 'wf' ya da 'kasa' olmalı: {asama}")
    oc = v2_onkayit_dogrula(cikti, veri=veri_sart, git=git_sart)
    wf_yol = _v2_yol("vdyt2_sonuc_wf.json", cikti); ky = _v2_yol("kasa", cikti)
    if asama == "kasa":
        if not os.path.exists(wf_yol):
            raise Vdyt2Hata("KASA açılamaz: önce `kos --asama wf` bitmeli")
        if os.path.exists(ky):
            raise Vdyt2Hata(f"KASA zaten açılmış ({ky}); ikinci kez açılmaz")
        _v2_json(ky, {"acilis": bas, "onkayit": oc, **_v2_meta(oc)})
    pazarlar = pazarlar or (list(E["karar_pazari"]) + list(E["kontrol_pazari"]))
    sonuc: Dict[str, Any] = {"asama": asama, "baslangic": bas, "onkayit": oc, "meta": _v2_meta(oc), "pazar": {}}; hata: Dict[str, Any] = {}
    ara = _v2_ara(asama) if girdi is None else os.path.join(cikti or VDYT2_YOL["cikti"], "_ara", asama)
    for pz in pazarlar:
        try:
            F, Ev = (girdi or {}).get(pz, (None, None))
            Z = v2_pazar_isle(pz, "kos", isci, F, Ev, E)
            A = v2_analiz(Z, asama, E, ara, p1_tekrar if pz in E["karar_pazari"] else 0)
            sonuc["pazar"][pz] = _v2_kayit(A); hata[pz] = {"hisse_hata": Z["hata"], "olay_notu": Z["ev_not"], "sure_sn": Z["sure_sn"]}
            del Z, A
        except (Vdyt2Hata, V1.VdytHata) as ex:
            sonuc["pazar"][pz] = {"durum": f"EKSİK: {ex}"}; hata[pz] = {"durum": str(ex)}
        except Exception as ex:   # bir pazarın beklenmeyen hatası öteki pazarları silmez; kayda geçer
            vdyt2log.exception("%s: beklenmeyen hata", pz)
            sonuc["pazar"][pz] = {"durum": f"HATA: {type(ex).__name__}: {str(ex)[:300]}"}; hata[pz] = {"durum": f"HATA: {type(ex).__name__}: {ex}"}
    wf = _v2_json_oku(wf_yol) if asama == "kasa" else _v2_kayit(sonuc)
    sonuc["karar"] = v2_karar_tablosu(wf, _v2_kayit(sonuc) if asama == "kasa" else None, E)
    if asama == "kasa":
        sonuc["teyit"] = v2_teyit(wf, _v2_kayit(sonuc), E)
    sonuc["bitis"] = _v2_simdi(); sonuc["sure_sn"] = round(time.time() - t0, 1)
    _v2_json(_v2_yol(f"vdyt2_sonuc_{asama}.json", cikti), sonuc)
    _v2_json(_v2_yol("meta", cikti), {"asama": asama, "baslangic": bas, "bitis": sonuc["bitis"], "sure_sn": sonuc["sure_sn"], "hata": hata, **_v2_meta(oc)})
    v2_parametre_kaydi(cikti, {"komut": f"kos {asama}"}, oc)
    v2_hata_raporu(hata, sonuc, cikti); sonuc["rapor"] = v2_rapor(asama, cikti)
    return sonuc


def v2_parametre_kaydi(cikti: Optional[str] = None, ek: Optional[Dict[str, Any]] = None, oc: Optional[Dict[str, Any]] = None) -> str:
    kayit = {**_v2_meta(oc), "veri_sha256": {a: list(v) for a, v in v2_veri_sha().items()}, "kesik": VDYT2_ESIK["kesik"], "python": sys.version.split()[0],
             "numpy": np.__version__, "pandas": pd.__version__, "esik": VDYT2_ESIK, "ozellik": VDYT2_OZELLIK, "model": VDYT2_MODEL, **(ek or {})}
    return _v2_json(_v2_yol("parametre", cikti), kayit)


def v2_hata_raporu(H: Dict[str, Any], S: Dict[str, Any], cikti: Optional[str] = None) -> str:
    m = S.get("meta") or {}
    L = [f"# VDYT2 hata ve veri eksikliği raporu ({S.get('asama')}) — {VDYT2_ETIKET}\n\nÜretim: {_v2_simdi()}; kod {str(m.get('kod_sha256'))[:12]}; ön kayıt commit "
         f"{m.get('onkayit_commit')}.\n"]
    for pz, h in H.items():
        L.append(f"\n## {pz}\n")
        if "durum" in h:
            L.append(f"\n{h['durum']}\n"); continue
        L.append(f"\nHisse hatası: {len(h.get('hisse_hata') or {})}; süre {h.get('sure_sn')} sn.\n")
        for s, e in list((h.get("hisse_hata") or {}).items())[:30]:
            L.append(f"- {s}: {e}\n")
        L.append("\nOlay notu: `" + json.dumps(h.get("olay_notu"), ensure_ascii=False, default=str)[:2500] + "`\n")
    return _v2_yaz(_v2_yol(f"VDYT2_HATA_{S.get('asama')}.md", cikti), "".join(L))


# ---------------------------------------------------------------- 10) RAPOR
def _v2_md(rows: List[Dict[str, Any]], kol: List[str], n: int = 4) -> str:
    if not rows:
        return "\n(veri yok)\n"
    L = ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
    for r in rows:
        L.append("| " + " | ".join(V1._t(r.get(k), 0 if (isinstance(r.get(k), (int, np.integer)) or (isinstance(r.get(k), float) and np.isfinite(r.get(k))
                                                                 and float(r.get(k)).is_integer() and abs(r.get(k)) >= 1)) else n)
                                   if isinstance(r.get(k), (int, float, np.floating, np.integer)) and not isinstance(r.get(k), bool) else str(r.get(k, "-"))
                                   for k in kol) + " |")
    return "\n" + "\n".join(L) + "\n"


def v2_rapor(asama: str = "wf", cikti: Optional[str] = None) -> str:
    """VDYT2_RAPOR_<aşama>.md: önce ÜÇ BAŞARI karar tablosu (ayrı ayrı), sonra ayrıntı. Başarısız satırlar silinmez."""
    yol = _v2_yol(f"vdyt2_sonuc_{asama}.json", cikti)
    if not os.path.exists(yol):
        raise Vdyt2Hata(f"sonuç yok: {yol} (önce kos --asama {asama})")
    S = _v2_json_oku(yol); m = S.get("meta") or {}
    L = [f"# VDYT2 raporu — aşama {asama} — {VDYT2_ETIKET}\n\nKoşu {S.get('baslangic')} → {S.get('bitis')} ({S.get('sure_sn')} sn). Kod {str(m.get('kod_sha256'))[:12]}, "
         f"VDYT.py {str(m.get('vdyt_kod_sha256'))[:12]}, mühür {str(m.get('esik_sha256'))[:12]}, ön kayıt commit {m.get('onkayit_commit')}.\n"
         "Sonuç doğrulanmış sinyal değildir; ilişki nedensellik değildir; yüksek olasılık alım sinyali değildir. Üç başarı AYRI ayrı; biri başarısızsa başarılı "
         "sunulmaz.\n\n## 1. Üç başarı (ANA = G5, ön koşul P1; P0 / P2 bilgi)\n"]
    L.append(_v2_md(S.get("karar") or [], ["pazar", "onkosul", "b1", "b2a", "b2b", "b2", "b3", "b1_wf", "b1_kasa", "b2a_wf", "b2a_kasa", "b2b_wf", "b2b_kasa",
                                           "b3_wf", "b3_kasa"]))
    if S.get("teyit"):
        L.append("\n## 2. WF'de BH ile reddedilen hipotezlerin KASA teyidi (olaylarda ayrıca plasebo eşiği)\n")
        L.append(_v2_md(S["teyit"], ["pazar", "id", "aile", "wf_nokta", "wf_p", "kasa_nokta", "kasa_alt", "kasa_ust", "sonuc"]))
    for pz, P in (S.get("pazar") or {}).items():
        L.append(f"\n## {pz}\n")
        if "durum" in P:
            L.append(f"\n{P['durum']}\n"); continue
        L.append("\n### Başarı (1): bölgeyi önceden bulmak (20 gün içinde büyük hareket oranı, kontrollere karşı)\n")
        L.append(_v2_md(P.get("basari1") or [], ["tanim", "rol", "onkosul", "kontrol", "n1", "n0", "n1_dusen", "ort1", "ort0", "fark", "alt", "ust", "oran", "p", "ana"]))
        L.append("\n### Duyarlılık, kaçırılan büyük hareket, uyarı süresi, yanlış bölge payı (BİLGİ)\n")
        L.append(_v2_md(P.get("duyarlilik") or [], ["tanim", "onkosul", "bhu", "onceden_tespit", "kacirilan", "duyarlilik", "kapsama_P0", "kaldirac_P0", "uyari_q25",
                                                    "uyari_medyan", "uyari_q75", "yanlis_bolge_payi"]))
        b2 = [r for r in (P.get("basari2") or []) if not r.get("katki")]
        L.append("\n### Başarı (2): genişlemeyi önceden tahmin (Brier skill; ANA hücre y10, M_TAM vs T1)\n")
        L.append(_v2_md(b2, ["tanim", "onkosul", "ufuk", "model", "temel", "kontrol", "n", "y_ort", "brier_skill", "brier_skill_alt", "brier_skill_ust", "ece",
                             "kesinlik_ust10", "duyarlilik_ust10", "ana"]))
        L.append("\n### D1b: bölgeye özgü bilgi (gerçek - kontrol skill farkı)\n")
        L.append(_v2_md(P.get("d1b") or [], ["tanim", "onkosul", "kontrol", "n_a", "n_b", "skill_a", "skill_b", "fark", "alt", "ust", "p"]))
        L.append("\n### Katkı (ablasyon: M_TAM - M_EKSI_grup; başarısız gruplar da burada)\n")
        L.append(_v2_md([r for r in (P.get("basari2") or []) if r.get("katki")], ["onkosul", "ufuk", "katki", "n", "brier_skill", "brier_skill_alt", "brier_skill_ust"]))
        L.append("\n### Başarı (3): yön (M_TAM vs B1 KARAR; B2 konum ve konum-dışı BİLGİ)\n")
        L.append(_v2_md([r for r in (P.get("basari3") or []) if not r.get("katki")], ["tanim", "onkosul", "model", "temel", "n", "y_ort", "brier_skill", "brier_skill_alt",
                                                                                     "ba_m", "ba_0", "ba_fark", "ba_fark_alt", "ece", "ana"]))
        L.append("\n### Yön katkısı (ablasyon)\n")
        L.append(_v2_md([r for r in (P.get("basari3") or []) if r.get("katki")], ["onkosul", "katki", "n", "brier_skill", "brier_skill_alt", "ba_fark"]))
        L.append("\n### İşlem sonucu (tahmin edilen yöne işaretli, maliyet sonrası; BİLGİ)\n")
        L.append(_v2_md(P.get("islem") or [], ["onkosul", "n", "r10_M_TAM", "r10_B1", "r10_fark_alt", "rk10_M_TAM", "rk10_B1", "rk10_fark_alt", "r20_M_TAM", "r20_B1",
                                                "mfe_ort", "mae_ort"]))
        L.append("\n### Süre (KM / CIF / yaş hazard'ı) ve olgunlaşma testi (D2)\n")
        L.append(_v2_md(P.get("sure") or [], ["tanim", "onkosul", "bolge"] + [f"hazard_{a}_{b}" for a, b in VDYT2_ESIK["yas_kova"]]))
        L.append(_v2_md(P.get("olgunlasma") or [], ["tanim", "onkosul", "n1", "n0", "ort1", "ort0", "fark", "alt", "ust", "p"]))
        if P.get("olay"):
            L.append("\n### Olaylar E1 / E2 (gözlenen - eşlenmiş beklenen; plasebo eşiği teyitte)\n")
            L.append(_v2_md([r for r in P["olay"] if r.get("pencere") != "yok"], ["tur", "kip", "pencere", "olay_kullanilan", "gozlenen", "beklenen", "fark", "alt", "ust", "p"]))
            L.append("\n### Haberli / habersiz büyük hareketler (yön payı, büyüklük)\n")
            L.append(_v2_md(P.get("haber") or [], ["olcu", "n1", "n0", "ort1", "ort0", "fark", "alt", "ust", "p", "ba_M_TAM", "ba_B1"]))
            pl = P.get("plasebo") or {}
            L.append(f"\nPlasebo P1 yanlış pozitif oranı (tekrarların >= 1 BH keşfi payı): {pl.get('yanlis_pozitif_orani')}\n")
        if P.get("birlesik"):
            L.append("\n### Birleşik üç sınıf (yukarı BH / aşağı BH / yok; BİLGİ)\n")
            L.append(_v2_md(P["birlesik"], ["tanim", "onkosul", "n", "skill", "alt", "ust", "p"]))
        if P.get("olay_eslesme"):
            L.append("\n### Olay-bölge zaman eşlemesi (BİLGİ; yaş = olay günündeki bölge yaşı, bh_gun = onaylı BH günü - olay günü)\n")
            L.append(_v2_md(P["olay_eslesme"], ["tur", "cift", "yas_medyan", "bh_olan", "bh_gun_medyan"]))
        L.append("\n### Sınıf değerlendirmesi (BİLGİ; yön kapısı uygulanmadan)\n")
        L.append(_v2_md(P.get("sinif") or [], ["sinif", "n", "y10_oran", "y20_oran", "yukari_payi"]))
    return _v2_yaz(_v2_yol(f"VDYT2_RAPOR_{asama}.md", cikti), "".join(L))


# ---------------------------------------------------------------- 11) CANLI ÇIKTI (her hisse için güncel durum; KASA'dan sonra; test dışı)
def v2_sinif(acik: bool, basladi: bool, bilesen: int, gecerli: bool, p10: float, q80: float, p_up: float, gen_gecti: bool, yon_gecti: bool,
             E: Optional[Dict[str, Any]] = None) -> str:
    """Sınıf kuralı (ön kayıt; eşikler eğitimden / sabit). Öncelik: Genişleme başladı > (açık bölge yok: oluşuyor / yok) > devam > yaklaşan / adaylar / yön belirsiz."""
    E = E or VDYT2_ESIK; S = E["sinif"]
    if basladi:
        return "Genişleme başladı"
    if not acik:
        return "Sıkışma oluşuyor" if bilesen >= int(E["sessiz"]["olusuyor_en_az"]) else "Sıkışma yok"
    if not gecerli or not gen_gecti or not np.isfinite(p10) or not np.isfinite(q80) or p10 < q80:
        return "Sıkışma devam ediyor"
    if not yon_gecti or not np.isfinite(p_up):
        return "Yön belirsiz"
    if p_up >= float(S["yukari"]):
        return "Yukarı kırılma adayı"
    if p_up <= float(S["asagi"]):
        return "Aşağı kırılma adayı"
    return "Genişlemeye yaklaşan sıkışma"


def v2_guven(gecti: Optional[bool], ece: Optional[float], olcu: Optional[float], ece_max: float, olcu_min: float) -> str:
    if not gecti:
        return "DÜŞÜK"
    return "YÜKSEK" if (ece is not None and olcu is not None and ece <= ece_max and olcu >= olcu_min) else "ORTA"


_V2_AD = {"m_aralik_atr": "mum aralığı / ATR250", "b_kapanis_bant": "kapanış bandı / kendi geçmişi", "sv_hat_var": "savunma hattı var", "sv_temas": "hat teması",
          "k_bolge_konum": "bölge içi konum", "yas_log": "bölge yaşı", "o_bilanco_gun": "beklenen bilançoya gün", "p_pazar_ret60": "piyasa 60 gün getirisi",
          "h_hacim_oran": "hacim daralması", "v_natr_oran": "ATR oranı", "on_dusus120": "önceki düşüş (120 gün)"}


def v2_dayanak(kolon: List[str], b: List[float], x_z: np.ndarray, k: int = 3) -> str:
    """En önemli dayanaklar: lojistik katkı = katsayı x z-değer; mutlak en büyük k tanesi (işaretli)."""
    kat = np.asarray(b[1:], float) * np.asarray(x_z, float); sira = np.argsort(-np.abs(kat))[:k]
    return "; ".join(f"{_V2_AD.get(kolon[i], kolon[i])} ({'+' if kat[i] >= 0 else '-'}{abs(kat[i]):.2f})" for i in sira)


@_v2_sessiz
def v2_canli(cikti: Optional[str] = None, isci: int = 3, git_sart: bool = True, veri_sart: bool = True, pazarlar: Optional[List[str]] = None,
             girdi: Optional[Dict[str, Tuple[Dict[str, Any], pd.DataFrame]]] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """Her hisse için güncel durum (son veri günü; 'CANLI, test dışı'). YALNIZ KASA sonucu varken. Modeller: kesik (31.08.2026) içinde etiketi tamamlanan bütün
    ANA satırlarla eğitilir; q_yüksek = bu eğitim tahminlerinin %80'i. Genişleme sınıfları yalnız (2) o alt kümede BAŞARILI ise; yön sınıfları yalnız (3) o alt
    kümede BAŞARILI ise (alt küme: P1 bayrağı varsa P1, yoksa P2, yoksa P0)."""
    E = E or VDYT2_ESIK; oc = v2_onkayit_dogrula(cikti, veri=veri_sart, git=git_sart)
    ky = _v2_yol("vdyt2_sonuc_kasa.json", cikti)
    if not os.path.exists(ky):
        raise Vdyt2Hata("canlı çıktı yalnız KASA'dan sonra: önce `kos --asama kasa`")
    S = _v2_json_oku(ky); K = {(r["pazar"], r["onkosul"]): r for r in S.get("karar") or []}; an = E["ana_tanim"]; tum = []
    for pz in pazarlar or list(E["karar_pazari"]):
        F, Ev = (girdi or {}).get(pz, (None, None))
        Z = v2_pazar_isle(pz, "kapsam", isci, F, Ev, E, canli=True)
        ara = os.path.join(cikti or VDYT2_YOL["cikti"], "_ara", "kasa") if girdi is not None else _v2_ara("kasa")
        yt = os.path.join(ara, f"satir_tam_{pz}_{an}.pkl")
        if not os.path.exists(yt):
            raise Vdyt2Hata(f"{pz}: KASA satır tablosu yok ({yt}); kos --asama kasa yeniden üretilmeli")
        D = pd.read_pickle(yt); kol = v2_kolon(list(VDYT2_OZELLIK)); kes = pd.Timestamp(E["kesik"]); M = E["model"]; mdl = {}
        for hh in E["ufuk"]:
            tr = D[D[f"y{hh}"].notna() & (D[f"son{hh}"] <= kes)]
            Xa, _ = V1.vdyt_standart(tr[kol].to_numpy(float), tr[kol].to_numpy(float)[:1], tuple(M["winsor"]))
            b = V1.vdyt_lojistik(Xa, tr[f"y{hh}"].to_numpy(float), float(M["ridge"]), int(M["tur"]), float(M["tol"]))
            fit = V1.vdyt_sigmoid(np.column_stack([np.ones(len(Xa)), Xa]) @ b); mdl[hh] = (tr[kol].to_numpy(float), b, float(np.quantile(fit, float(E["sinif"]["q_yuksek"]))))
        D2 = D[(D.y20 == 1) & D.yukari.notna() & (D.son20 <= kes)]
        Xy, _ = V1.vdyt_standart(D2[kol].to_numpy(float), D2[kol].to_numpy(float)[:1], tuple(M["winsor"]))
        by = V1.vdyt_lojistik(Xy, D2.yukari.to_numpy(float), float(M["ridge"]), int(M["tur"]), float(M["tol"]))
        ctxP = Z["Pn"]; Ev_m = Z["Ev"][Z["Ev"].sembol == "*"]; Ev_g = {s_: g_ for s_, g_ in Z["Ev"][Z["Ev"].sembol != "*"].groupby("sembol")}
        for h in Z["R"]:
            s = h["sembol"]; d = Z["F"]["S"][s]; n = len(d); T = h["bolge"].get(an, pd.DataFrame())
            Ol = v2_olculer(d, E); c = d.c.to_numpy(float); t = n - 1
            sat: Dict[str, Any] = {"pazar": pz, "sembol": s, "son_gun": d.index[-1].date(), "etiket": "CANLI, test dışı"}
            eski = (Z["Pn"]["takvim"].max() - d.index[-1]).days > int(E["sinif"]["eski_veri_gun"])
            uy = V1.vdyt_hisse_uygun(s, d, ctxP)[t]
            son = T.iloc[-1] if len(T) else None
            acik = bool(son is not None and son.bit_tur == BIT_SANSUR and son.bit == t and son.tespit <= t)
            basladi = bool(son is not None and son.bit_tur == BIT_BUYUK and son.bit >= t - int(E["sinif"]["basladi_gun"]) + 1)
            sat.update({"bolge_var": acik, "savunma_hatti": np.nan, "onkosul": None, "baslangic": d.index[int(son.bas)].date() if acik else None, "sure_gun": int(t - son.bas + 1) if acik else 0,
                        "sikisma_gucu": float(np.clip(1.0 - Ol["m_aralik_atr"][t], 0, 1) * 100) if np.isfinite(Ol["m_aralik_atr"][t]) else np.nan,
                        "bilesen": int(Ol["g_bilesen"][t]), "uygun": bool(uy), "veri_eski": bool(eski)})
            p = {hh: np.nan for hh in E["ufuk"]}; p_up = np.nan; q80 = np.nan; gec = False; day = ""; alt_k = "P0"
            if acik:
                bas = int(son.bas); gec = v2_gecerli(t, bas, Ol["tr"], c, E)
                ctx = V1.vdyt_hisse_baglam(s, d, ctxP, Ev_g.get(s, Z["Ev"].iloc[:0]), Ev_m)
                ctx["p_pazar_ret20"] = ctxP["p_pazar_ret20"].reindex(d.index).to_numpy(float)
                A = {"Ol": Ol, "o": d.o.to_numpy(float), "h": d.h.to_numpy(float), "l": d.l.to_numpy(float), "c": c, "v": d.v.to_numpy(float), "gun": d.index,
                     "n": n, "pazar": pz, "E1": _v2_e1(True)}
                x = v2_ozellik(t, bas, A, ctx, _v2_once(T, t, E), E, True); xv = np.array([[x.get(k, np.nan) for k in kol]], float)
                alt_k = "P1" if x["on_p1"] == 1 else ("P2" if x["on_p2"] == 1 else "P0")
                sat["savunma_hatti"] = x.get("sv_seviye"); sat["onkosul"] = alt_k
                if gec:
                    for hh, (Xtr, b, q) in mdl.items():
                        _a, xz = V1.vdyt_standart(Xtr, xv, tuple(M["winsor"])); p[hh] = float(V1.vdyt_sigmoid(np.r_[1.0, xz[0]] @ b))
                        if hh == int(E["ana_ufuk"]):
                            q80 = q; day = v2_dayanak(kol, list(b), xz[0])
                    _a, xz = V1.vdyt_standart(D2[kol].to_numpy(float), xv, tuple(M["winsor"])); p_up = float(V1.vdyt_sigmoid(np.r_[1.0, xz[0]] @ by))
            k_ = K.get((pz, alt_k), {}); gen_g = k_.get("b2") == "BAŞARILI"; yon_g = k_.get("b3") == "BAŞARILI"
            sat["sinif"] = v2_sinif(acik, basladi, int(Ol["g_bilesen"][t]), gec, p[int(E["ana_ufuk"])], q80, p_up, gen_g, yon_g, E)
            zam = next((f"<= {hh} işlem günü" for hh in E["ufuk"] if np.isfinite(p[hh]) and p[hh] >= 0.5), "> 20 işlem günü" if np.isfinite(p[20]) else None)
            d2 = (k_.get("b2_kasa_detay") or {}); d3 = (k_.get("b3_kasa_detay") or {}); G = E["sinif"]
            gv = v2_guven(gen_g, d2.get("ece"), d2.get("brier_skill"), G["guven_genisleme"]["ece_max"], G["guven_genisleme"]["skill_min"])
            if sat["sinif"] in ("Yukarı kırılma adayı", "Aşağı kırılma adayı"):
                gy = v2_guven(yon_g, d3.get("ece"), d3.get("ba_fark"), G["guven_yon"]["ece_max"], G["guven_yon"]["ba_min"])
                gv = min((gv, gy), key=["DÜŞÜK", "ORTA", "YÜKSEK"].index)
            sat.update({"p5": p[5], "p10": p[10], "p20": p[20], "q_yuksek": q80, "zaman_araligi": zam, "p_yukari_kosullu": p_up,
                        "p_asagi_kosullu": 1 - p_up if np.isfinite(p_up) else np.nan, "p_yukari_20": p[20] * p_up if np.isfinite(p_up) else np.nan,
                        "p_asagi_20": p[20] * (1 - p_up) if np.isfinite(p_up) else np.nan, "gecerli_gun": gec, "guvenilirlik": gv, "dayanaklar": day,
                        "genisleme_motoru": k_.get("b2"), "yon_motoru": k_.get("b3"), "bolge_motoru": k_.get("b1")})
            tum.append(sat)
    T_ = pd.DataFrame(tum); meta = _v2_meta(oc)
    for k in ("surum", "kod_sha256", "onkayit_commit"):
        T_[k] = meta.get(k)
    y = _v2_yol(f"vdyt2_canli_{_dt.date.today().isoformat()}.csv", cikti)
    if os.path.exists(y):
        raise Vdyt2Hata(f"canlı tablo zaten var: {y} (üzerine yazılmaz)")
    T_.to_csv(y, index=False)
    return y


# ---------------------------------------------------------------- 12) GRAFİK: girdi paketi (kos çıktısından) + YALNIZ paketten çizim (Colab)
@_v2_sessiz
def v2_paket(asama: str = "kasa", cikti: Optional[str] = None, pazarlar: Optional[List[str]] = None, F_ver: Optional[Dict[str, Dict[str, Any]]] = None,
             ara: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> List[str]:
    """Önceden tanımlı gruplar (BAŞARILI: p10 >= q80 ve y10 = 1; BAŞARISIZ: p10 >= q80 ve y10 = 0; KAÇIRILAN: BHU, g-1'de açık ANA bölge yok; YÖN DOĞRU / YANLIŞ:
    yön tahmini (p >= 0,5) çıkılan kenarla aynı / değil; HABERSİZ: büyük harekete dönüşen satır, g çevresinde olay yok) x tohumlu grup_n örnek. Paket: örnek
    başına [bas - on_bar, son olay + son_bar] OHLCV + meta (bölge, tespit, karar günü, savunma hattı, büyük hareket başlangıcı, yön). Dosya < paket_mb."""
    E = E or VDYT2_ESIK; G = E["grafik"]; an = E["ana_tanim"]; hu = int(E["ana_ufuk"]); ara = ara or _v2_ara(asama); yazilan = []
    kl = os.path.join(cikti or VDYT2_YOL["cikti"], "grafik_paket", asama); os.makedirs(kl, exist_ok=True)
    for pz in pazarlar or list(E["karar_pazari"]):
        yk, y1, y2, yb = (os.path.join(ara, f) for f in (f"satir_{pz}_{an}.csv.gz", f"tahmin_m1_{pz}_{an}_y{hu}.csv.gz", f"tahmin_m2_{pz}_{an}.csv.gz",
                                                          f"bolge_{pz}_{an}.csv.gz"))
        if not all(os.path.exists(x) for x in (yk, y1, yb)):
            vdyt2log.warning("%s: paket girdisi yok (önce kos)", pz); continue
        Kd = pd.read_csv(yk, parse_dates=["tarih", "g_tarih"]).set_index("satir"); P1 = pd.read_csv(y1); P2 = pd.read_csv(y2) if os.path.exists(y2) else pd.DataFrame()
        Bd = pd.read_csv(yb); yh = os.path.join(ara, f"haber_{pz}_{an}.csv.gz"); Hd = pd.read_csv(yh) if os.path.exists(yh) else pd.DataFrame()
        ybh = os.path.join(ara, f"bhu_{pz}.csv.gz"); BHd = pd.read_csv(ybh) if os.path.exists(ybh) else pd.DataFrame()
        F = (F_ver or {}).get(pz) or v2_fiyat(pz)
        P1 = P1.join(Kd[["t", "bas", "bolge", "g", "e", "yon", "sv_seviye"]], on="satir")
        gr: Dict[str, pd.DataFrame] = {"BASARILI": P1[(P1.p_M_TAM >= P1.q80_M_TAM) & (P1.y == 1)], "BASARISIZ": P1[(P1.p_M_TAM >= P1.q80_M_TAM) & (P1.y == 0)]}
        if len(P2):
            P2 = P2.join(Kd[["t", "bas", "bolge", "g", "e", "yon", "sv_seviye"]], on="satir")
            dog = (P2.p_M_TAM >= 0.5) == (P2.y == 1); gr["YON_DOGRU"] = P2[dog]; gr["YON_YANLIS"] = P2[~dog]
        if len(Hd):
            Hs = Hd[Hd.habersiz == 1][["sembol", "t", "g", "yon"]].merge(Kd.reset_index()[["satir", "sembol", "t"]], on=["sembol", "t"], how="inner")
            if len(Hs):
                Hs = Hs.join(Kd[["bas", "bolge", "e", "sv_seviye", "y20"]].rename(columns={"y20": "y"}), on="satir")
                Hs = Hs.merge(P1[["satir", "p_M_TAM"]].drop_duplicates("satir"), on="satir", how="left")
            gr["HABERSIZ"] = Hs
        if len(BHd) and f"tespit_{an}" in BHd:
            Kc = BHd[~BHd[f"tespit_{an}"].astype(bool)].copy(); Kc["t"] = Kc.g - 1; Kc["bas"] = Kc.t; Kc["bolge"] = -1; Kc["sv_seviye"] = np.nan
            gr["KACIRILAN"] = Kc
        meta, bars = [], []
        for g in G["gruplar"]:
            A = gr.get(g)
            if A is None or not len(A):
                continue
            A = A.sort_values(["sembol", "t"]).reset_index(drop=True)
            rng = np.random.default_rng(_v2_tohum(G["tohum"], pz, g)); sec = np.sort(rng.choice(len(A), size=min(int(G["grup_n"]), len(A)), replace=False))
            for j, i in enumerate(sec):
                r = A.iloc[i]; s = r.sembol; d = F["S"].get(s)
                if d is None:
                    continue
                t = int(r.t); bas_ = int(r.bas) if np.isfinite(r.get("bas", np.nan)) else t; gg = int(r.g) if np.isfinite(r.get("g", np.nan)) else -1
                ee = int(r.e) if np.isfinite(r.get("e", np.nan)) else -1
                bo = Bd[(Bd.sembol == s) & (Bd.bas == bas_)]; tes = int(bo.tespit.iloc[0]) if len(bo) else t
                a0 = max(0, bas_ - int(G["on_bar"])); a1 = min(len(d) - 1, max(t, gg, ee) + int(G["son_bar"]))
                oid = f"{pz}_{g}_{j + 1}"
                X = d.iloc[a0: a1 + 1][["o", "h", "l", "c", "v"]].reset_index().rename(columns={d.index.name or "index": "tarih"})
                X.columns = ["tarih", "o", "h", "l", "c", "v"]; X.insert(0, "i", np.arange(a0, a1 + 1)); X.insert(0, "ornek", oid); bars.append(X)
                meta.append({"ornek": oid, "pazar": pz, "grup": g, "sembol": s, "bas": bas_, "tespit": tes, "t": t, "g": gg, "e": ee,
                             "yon": float(r.get("yon", np.nan)) if r.get("yon") is not None else np.nan,
                             "hat": float(r.sv_seviye) if np.isfinite(r.get("sv_seviye", np.nan)) else np.nan, "p": float(r.get("p_M_TAM", np.nan)),
                             "y": float(r.get("y", np.nan)) if r.get("y") is not None else np.nan})
        if not meta:
            continue
        yb_ = os.path.join(kl, f"grafik_bar_{pz}.csv.gz"); ym_ = os.path.join(kl, f"grafik_ornek_{pz}.json")
        pd.concat(bars, ignore_index=True).to_csv(yb_, index=False)
        _v2_json(ym_, {"meta": _v2_meta(), "asama": asama, "ornek": meta})
        for y_ in (yb_, ym_):
            if os.path.getsize(y_) > float(G["paket_mb"]) * 1e6:
                raise Vdyt2Hata(f"paket dosyası {G['paket_mb']} MB sınırını aşıyor: {y_}")
        yazilan += [yb_, ym_]
    return yazilan


def v2_grafik_ogeler(m: Dict[str, Any], X: pd.DataFrame, sadece_gecmis: bool) -> Dict[str, Any]:
    """Çizilecek öğeler (test edilebilir): mumlar (gövde + fitil), hacim, bölge alanı, savunma hattı, tespit / karar günü, büyük hareket başlangıcı, yön, başlık.
    sadece_gecmis = True (TESPİT GÜNÜ grafiği): YALNIZ karar günü t'ye kadarki barlar; büyük hareket, yön, sonuç ve grup adı YOK."""
    t = int(m["t"]); X = X[X.i <= t] if sadece_gecmis else X
    og: Dict[str, Any] = {"bar": X, "bolge": (int(m["bas"]), t if sadece_gecmis else max(t, int(m["g"]) - 1 if int(m["g"]) >= 0 else t)),
                          "vcizgi": [("tespit", int(m["tespit"])), ("karar günü", t)], "hat": None, "metin": []}
    if m.get("hat") is not None and np.isfinite(m.get("hat", np.nan)):
        og["hat"] = (int(m["bas"]), t, float(m["hat"]))
    if sadece_gecmis:
        og["baslik"] = f"{m['pazar']} {m['sembol']} — TESPİT GÜNÜ {X.tarih.iloc[-1] if len(X) else ''}: YALNIZ bu güne kadarki mumlar"
    else:
        if int(m["g"]) >= 0:
            og["vcizgi"].append(("büyük hareket başlangıcı", int(m["g"])))
            y_ = {1.0: "YUKARI", -1.0: "AŞAĞI"}.get(m.get("yon"), "?"); og["metin"].append((int(m["g"]), y_))
        og["baslik"] = f"{m['pazar']} {m['grup']} {m['sembol']} — karar günü {X.tarih[X.i == t].iloc[0] if (X.i == t).any() else ''}; p={m.get('p')}; sonuç y={m.get('y')}"
    return og


def v2_ciz(paket: str, cikti: str, dpi: Optional[int] = None) -> List[str]:
    """YALNIZ paketten çizim (Colab'da bağımsız; veri / model gerekmez). Var olan PNG'nin ÜSTÜNE YAZMAZ. Her örnek: tam grafik + tespit günü grafiği.
    Büyük ve net gövde / fitil, ayrı hacim paneli, bölge, savunma hattı, tespit tarihi, büyük hareket başlangıcı, yön."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    G = VDYT2_ESIK["grafik"]; dpi = int(dpi or G["dpi"]); os.makedirs(cikti, exist_ok=True); yaz = []
    for ym in sorted(glob.glob(os.path.join(paket, "grafik_ornek_*.json"))):
        J = _v2_json_oku(ym); pz = os.path.basename(ym)[len("grafik_ornek_"): -5]
        B = pd.read_csv(os.path.join(paket, f"grafik_bar_{pz}.csv.gz"), parse_dates=["tarih"])
        for m in J["ornek"]:
            Xo = B[B.ornek == m["ornek"]].sort_values("i")
            for gecmis in (False, True):
                y = os.path.join(cikti, f"{m['ornek']}_{m['sembol']}_{'tespit' if gecmis else 'tam'}.png")
                if os.path.exists(y):
                    vdyt2log.info("var, üzerine yazılmadı: %s", y); continue
                og = v2_grafik_ogeler(m, Xo, gecmis); X = og["bar"]
                fig, (ax, av) = plt.subplots(2, 1, figsize=tuple(G["boyut"]), sharex=True, gridspec_kw={"height_ratios": [3.4, 1]})
                for r in X.itertuples():
                    renk = "#1a9850" if r.c >= r.o else "#d73027"
                    ax.vlines(r.i, r.l, r.h, color=renk, linewidth=1.3)
                    ax.add_patch(Rectangle((r.i - 0.36, min(r.o, r.c)), 0.72, max(abs(r.c - r.o), 1e-9), facecolor=renk, edgecolor="black", linewidth=0.4))
                a, b = og["bolge"]; ax.axvspan(a - 0.5, b + 0.5, color="#4575b4", alpha=0.10, label="küçük mum bölgesi")
                if og["hat"]:
                    ax.hlines(og["hat"][2], og["hat"][0], og["hat"][1], color="#542788", linestyle="--", linewidth=1.6, label="savunma hattı (gövde; t'ye kadar)")
                renkler = {"tespit": "#4575b4", "karar günü": "black", "büyük hareket başlangıcı": "#d73027"}
                for ad, x in og["vcizgi"]:
                    ax.axvline(x, color=renkler.get(ad, "grey"), linewidth=1.4, linestyle=":" if ad == "tespit" else "-", label=ad)
                for x, mt in og["metin"]:
                    ax.annotate(mt, (x, float(X.h.max())), fontsize=12, fontweight="bold")
                av.bar(X.i, X.v, color=["#1a9850" if c_ >= o_ else "#d73027" for c_, o_ in zip(X.c, X.o)], width=0.72)
                ax.set_title(og["baslik"], fontsize=11); ax.legend(loc="upper left", fontsize=8); av.set_ylabel("hacim", fontsize=9)
                tick = np.linspace(X.i.min(), X.i.max(), min(10, len(X))).astype(int)
                av.set_xticks(tick); av.set_xticklabels([str(X.tarih[X.i == k].iloc[0].date()) if (X.i == k).any() else "" for k in tick], fontsize=8, rotation=25)
                fig.tight_layout(); fig.savefig(y, dpi=dpi); plt.close(fig); yaz.append(y)
    return yaz


# ---------------------------------------------------------------- 13) ÖN KAYIT METNİ
def v2_onkayit_metin(zaman: str, veri_sha: Dict[str, Tuple[str, int]], kapsam: Optional[Dict[str, Any]], E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt metni: bütün tanımlar ve sayılar VDYT2_ESIK / VDYT2_OZELLIK / VDYT2_MODEL'den (mühürle aynı kaynak)."""
    E = E or VDYT2_ESIK; Ss = E["sessiz"]; G1, G2, G4 = Ss["G1"], Ss["G2"], Ss["G4"]; Bk = E["buyuk"]; Gc = E["gecerli"]; O = E["onkosul"]; K = E["kontrol"]
    W = E["wf"]; S_ = E["sinif"]; Gr = E["grafik"]; Sv = E["savunma"]; L = int(Ss["L"]); og = int(Bk["onay_gun"])
    tl = "\n".join(f"| {ad} | {T['rol']} | {T['durum']} | {T.get('devam', T['durum'])} | {T['min_kosu']} |" for ad, T in E["tanim"].items())
    oz = "\n".join(f"| {g} | {', '.join(v)} |" for g, v in VDYT2_OZELLIK.items())
    md = "\n".join(f"| {k} | {' + '.join(v)} |" for k, v in VDYT2_MODEL["genisleme"].items())
    my = "\n".join(f"| {k} | {' + '.join(v)} |" for k, v in VDYT2_MODEL["yon"].items())
    vs = "\n".join(f"- {k}: sha256 {h} ({n} dosya)" for k, (h, n) in sorted(veri_sha.items()))
    ks = ["| pazar | tanım | rol | bölge (uygun) | bölge P1 | geçerli karar günü | P1 | WF test 2019-2023 (P1) | KASA 2024-2026 (P1) | DIŞARI kontrol (P1) | "
          "RASTGELE kontrol (P1) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    bh = []
    for pz, o in ((kapsam or {}).get("pazar") or {}).items():
        if "bolge" not in o:
            ks.append(f"| {pz} | {o.get('durum')} | | | | | | | | | |"); continue
        bh.append(f"- {pz}: hisse {V1._t(o['hisse'])}, takvim {o['takvim']}; bölgeden bağımsız büyük hareket başlangıcı (BHU) TOPLAM: "
                  + ", ".join(f"{k} {V1._t(v)}" for k, v in o["buyuk_hareket_BHU_toplam"].items()))
        for ad, b in o["bolge"].items():
            k = o["karar"].get(ad, {}); kk = o["kontrol"].get(ad, {}); dp = k.get("donem_P1", {})
            ks.append(f"| {pz} | {ad} | {b['rol']} | {V1._t(b['bolge_uygun'])} | {V1._t(b['P']['P1'])} | {V1._t(k.get('toplam'))} | {V1._t(k.get('P', {}).get('P1'))} | "
                      f"{V1._t(dp.get('2019-2023 (WF test)'))} | {V1._t(dp.get('2024-2026 (KASA)'))} | {V1._t(kk.get('DISARI', {}).get('toplam'))} "
                      f"({V1._t(kk.get('DISARI', {}).get('P1'))}) | {V1._t(kk.get('RASTGELE', {}).get('toplam'))} ({V1._t(kk.get('RASTGELE', {}).get('P1'))}) |")
    kz = (kapsam or {}).get("zaman", "-")
    return f"""# VDYT2 ÖN KAYIT — Volatilite Denge ve Yön Tahmini, SÜRÜM 2 ({VDYT2_ETIKET}) — ölçümden ÖNCE

Yazım zamanı: {zaman}
ESIK_SHA256: {v2_esik_sha(E)}
KOD_SHA256: {v2_kod_sha()}
VDYT_KOD_SHA256: {v2_v1_kod_sha()}
Sürüm: {VDYT2_SURUM}

Bu dosya, VDYT2.py ve VDYT.py git'e işlenmeden; eşik mührü, iki kod sha256'sı ve veri sha256'ları tutmadan `kos` ve `canli` ÇALIŞMAZ (Vdyt2Hata, çıkış 1).
Sonuç görüldükten sonra tanım, eşik, pencere, ufuk, kontrol, model, temel ya da karar kuralı değişmez; değişirse bu dosyada tarihli SAPMA yazılır, mühür / kod
satırı yeniden işlenir. VDYT sürüm 1 kayıtları, kodu (VDYT.py), ön kaydı, çıktıları ve VDYT_GRAFIK.py DEĞİŞMEZ; v2 ayrı dosya ve ayrı klasördür.

## 0. Hedef (Cemal, aynen) ve sınır
'Sert düşüş veya önceki hareket -> küçük mumların oluşturduğu uzun sessiz bölge -> büyük mumlarla başlayan volatilite genişlemesi.' Bu sessiz bölgeyi BÜYÜK
HAREKET BAŞLAMADAN ÖNCE tespit et; büyük hareketin ne zaman başlayabileceğini, yönünü ve hangi özelliklerin doğru tahmin ihtimalini artırdığını belirle. Amaç
geçmiş grafikte güzel görünen bölgeleri bulmak değil, gerçek zamanda henüz büyük hareket olmamışken yakalamak.
- ÜÇ BAŞARI AYRI AYRI kanıtlanır (bölüm 7): (1) bölgeyi önceden bulmak, (2) genişlemeyi önceden tahmin etmek, (3) yönü önceden tahmin etmek; basit piyasa
  kontrollerinden daha iyi. Biri başarısızsa başarılı gibi sunulmaz. Sonuç olumsuz olabilir; başarısız değişken / test rapordan silinmez.
- Çöl Yolu kuralları, IZ_KARNE kararları, geçmiş kayıtlar (VDYT v1 ve Ç161 dahil) DEĞİŞMEZ. Hacim / mum şekli değişkenleri (Çöl Yolu'nda kapalı konu) yalnız bu
  motorda ölçülür; sonuç Çöl Yolu'na 'yaz' kararı olmadan taşınmaz. VDYT2 sonucu doğrulanmış sinyal değildir; yüksek olasılık alım sinyali değildir.
- Ücretli veri / abonelik (Alpha Vantage, Tiingo, IBorrowDesk) YOK; SEC'e istek yok; yeni büyük indirme yok.

## 1. VDYT v1 dersleri ve v2'deki zorunlu karşılığı
- D1 (genişleme motoru mekanikti): (a) GEÇERLİ KARAR GÜNÜ (bölüm 5.2): t ve önceki {int(Gc['gun']) - 1} günün HER BİRİNİN gerçek aralığı <= {Gc['k_sessiz']} x bölge
  referansı ve bölge t kapanışında hâlâ açık; etiket YALNIZ t'den SONRA başlayan büyük hareketi sayar (g > t). (b) Aynı model sıkışma DIŞI ve aynı mutlak
  oynaklık ondalığındaki günlerde (DIŞARI) ve rastgele bölgelerde (RASTGELE, aynı süre dağılımı) koşulur; 'bölgenin kendine özgü bilgisi' ancak bu iki
  kontrolden iyiyse vardır (başarı 2b).
- D2 (v1'de hazard yaşla AZALDI): 'olgunlaşma' VARSAYILMAZ; OLG testi (bölüm 9) ve yaş hazard'ı raporlanır; SÜRE grubu modelde serbest işaretli.
- D3 (v1 yön başarısı büyük ölçüde konumdan): yön KARAR temeli B1 (piyasanın son 60 gün yönü); B2 = yalnız KONUM grubu (mekanik temel; BİLGİ); konum-dışı
  model (M_KONUMSUZ) BİLGİ; yön ayrıca işlem sonucuyla (maliyet sonrası getiri) raporlanır.
- D4 (bilanço dışı olay bulgularında plasebo yanlış pozitifi yüksekti): olay bulgusu ancak WF'de BH ile reddedilir, KASA'da aynı işaretle %95 aralığı 0'ı
  dışlar VE WF |fark| aynı tür x pencerenin plasebo |fark| dağılımının %{E['coklu']['plasebo_esik_pct']:.0f} yüzdeliğini aşarsa SAYILIR (bölüm 11).
- D5: VDYT_GRAFIK.py ve arastirma_cikti/vdyt/paket'e dokunulmaz; v2 grafikleri kendi paketi + yalnız paketten çizen `ciz` ile (bölüm 14).

## 2. Veri ve dönem (VDYT v1 ile aynı kaynaklar; VDYT.py yükleyicileri içe aktarılır, değiştirilmez)
- BIST = V_BIST (OHLCV, 2015-06+; yaşayan 581). ABD = k60_fiyat (Yahoo OHLCV 2010+; 4.678 hisse; yaşayan). BIST_K62 = K62 kapanış 2008+ (kotasyondan
  çıkanlar dahil; açılış / yüksek / düşük YOK) YALNIZ yanlılık kontrolü: tanım G2K (yalnız kapanış bandı), büyük mumda gövde şartı yok, yalnız başarı (1)
  ve çıkmış / yaşayan ayrımı (BİLGİ).
- Bar temizliği, uygunluk (BIST: >= 252 bar, 20 gün medyan işlem değeri kesitte %20 üstü; ABD: EQUITY, >= 252 bar, ekrandaki fiyat >= 2 $, 20 gün medyan işlem
  değeri >= 1 milyon $), kopukluk (> 15 takvim günü), endeks (XU100 / SPY), sektör, NATR ondalığı, momentum / likidite tertilleri: VDYT v1 ile aynı
  (V1.vdyt_panel). Karar satırı yalnız uygun günde (t).
- Olaylar: KAP Finansal Rapor 2009+ (BIST bilanço; yayın saati kuralı), KAP içeriden işlem 2022-07+, KAP fon girişleri 2023+, K62 hak kullanım / sermaye,
  EDGAR form grupları (8-K, sermaye, 13D, birleşme, gecikme, vekâlet), FOMC / PPK (planlı), emtia şokları, rakip bilançosu. ABD bilanço günü: Yahoo takvimi
  (/tmp/k67_yahoo/takvim; 1.410 hisse, 1998+; K67'de Nasdaq ile %97 uyumlu) BİRİNCİL: takvimi olan hissede v1 bilanço satırları Yahoo ile değişir (saat
  >= 16 ET -> sonraki işlem günü; diğerleri ve 'saat yok' -> o gün); takvimi olmayanda v1 (Nasdaq 2022-12+, öncesi 10-Q / 10-K vekili). Gelecek tarihli
  takvim satırları atılır; özellikte beklenen bilanço günü YALNIZ t'ye kadar bilinen bilançolardan (v1 kuralı) türetilir.
- Fon krizi kesiği {E['kesik']}: test fiyatları burada kesilir; etiketi kesiği aşan satır ölçülmez. Canlı çıktı (bölüm 13) son veri gününde, 'CANLI, test dışı'.
- Maliyet (tek yön; yalnız getiri bilgisinde): BIST {E['maliyet']['BIST'] * 1e4:.0f} bp, ABD {E['maliyet']['ABD'] * 1e4:.0f} bp.

## 3. Ön koşul (önceki hareket) alternatifleri — bölge başlangıcı bas'taki bilgiyle
- düşüş120 = C[bas] / max(C[bas-{O['pencere']} .. bas-1]) - 1; yükseliş120 = C[bas] / min(aynı pencere) - 1; geçmiş < {O['pencere']} bar ise tanımsız (P1 = P2 = yok).
- P0 = koşul yok; P1 (ANA; 'sert düşüş') = düşüş120 <= {O['P1']:+.2f}; P2 ('önceki büyük hareket') = P1 YA DA yükseliş120 >= {O['P2']:+.2f} (|değişim| >= %30).
- Bütün ön koşullar raporlanır. Modeller P0 satırlarıyla eğitilir (ön koşul ölçüleri ONCEKI grubu olarak modelde); değerlendirme ve TEMELLER her alt
  kümede o alt kümenin kendi eğitim satırlarıyla kurulur (temel alt küme bilgisinden yoksun kalmaz). Kontrol satırlarında da aynı ön koşul (sözde bas'a göre).

## 4. Sessiz bölge ('insan gözü') tanımları — günlük DURUM, yalnız [t-L+1, t] (L = {L}) ve öncesi
- ATRref(t) = ortalama TR[t-L-{int(E['atr_ref']['n']) - 1} .. t-L] (sessiz pencereden ÖNCEKİ {E['atr_ref']['n']} bar; en az {E['atr_ref']['min']}); TR = max(H-L, |H-C[-1]|, |L-C[-1]|).
- G1 küçük mum bileşiği: medyan(H-L) / ATRref <= {G1['aralik_atr'][0]} (alternatifler {G1['aralik_atr'][1]}, {G1['aralik_atr'][2]}) VE medyan |C-O| / ATRref <= {G1['govde_atr']} VE
  maks(H-L) / ATRref <= {G1['maks_aralik_atr']} (pencerede büyük mum yok). Ölçü olarak (şart değil): medyan |gövde| / (H-L), üst / alt fitil / ATRref, doji payı
  (|C-O| <= {G1['doji']} x (H-L)).
- G2 dar bant: kapanış bandı KB = (maks C - min C) / ort C (son L) ve gövde bandı GB = (maks max(O,C) - min min(O,C)) / ort C; her biri kendi geçmişinin
  medyanına bölünür (aynı ölçünün [t-L-{int(G2['gecmis_n']) - 1}, t-L] değerleri; en az {G2['gecmis_min']}); İKİSİ de <= {G2['bant_oran'][0]} (alternatifler {G2['bant_oran'][1]}, {G2['bant_oran'][2]}).
- G3 yaklaşan tepe-dip (kanal daralması): son L günün tepelerinin (H) en küçük kareler eğimi / ATRref <= {Ss['G3']['tepe_egim_ust']} VE diplerinin (L) eğimi / ATRref >= {Ss['G3']['dip_egim_alt']}.
- G4 savunulan destek: VDYT v1 savunma hattı (V1.vdyt_savunma ile aynı kural, kayan pencere [t-{int(G4['pencere']) - 1}, t]; tol = {Sv['tolerans_tr']} x medyan TR; adaylar aralığın alt
  {Sv['alt_dilim']:.3f}'ü; hat VAR <=> temas >= {Sv['min_temas']} ve ilk-son temas arası >= {Sv['min_aralik']} bar) VE ilk temastan sonra kapanışla kırılma YOK ('savunulan').
  Taban: gövde dibi min(O,C) (ANA), fitil dibi (L), kapanış (C) AYRI.
- G5 (ANA) = G1 VE G2 VE (G3 YA DA G4[gövde]): 'küçük mumlar + dar bant + tekrar test edilen dipler / ortak destek'. Aile: G5f (G4 fitil), G5k (G4 kapanış).
  Alternatif eşikler: G1_e0.5, G1_e0.7 (G1 tek başına), G5_g0.4, G5_g0.6 (G2 eşiği). Karşılaştırma: VDYT v1 T1-T5 durumları (v1 eşikleriyle). Pencerede
  kopukluk varsa durum yanlış.
- BÖLGE KURALI: G tanımlarında durum 1 gün doğru (durum zaten son L günün ölçüsü), v1 T tanımlarında 10 gün kesintisiz doğru VE önceki bölgenin bitişinden en az
  L gün sonra -> tespit = o gün, bas = tespit - L + 1 (yaş = t - bas + 1; tespitte {L}). Bitiş (tespitten SONRA, gerçek zamanda bilinen ilk olay): BÜYÜK MUM
  (bölüm 5.1, ref başlangıcı bas) | SÖNME: DEVAM durumu {E['bolge']['sonme_gun']} gün üst üste yanlış | SANSÜR: veri sonu / kopukluk. DEVAM durumu G5 ailesinde
  çekirdek G1 VE G2'dir (küçük mum + dar bant sürdükçe bölge açık; tepe-dip / destek şartı G3 ∨ G4 AÇILIŞ onayıdır, her gün aranmaz); diğer tanımlarda açılış
  durumunun kendisi. Büyük mumla biten bölgenin ONAYI (bölüm 5.1) süre analizinde olay / rakip olay ayrımıdır.

| tanım | rol | açılış durumu | devam durumu | açılış için kesintisiz gün |
|---|---|---|---|---|
{tl}
| G2K (BIST_K62) | K62 | G2 (kapanış) | G2 (kapanış) | 1 |
Roller: ANA = bütün analizler; AILE = başarı (1), (2) ve (3) M_TAM (BİLGİ); ALT = başarı (1) + duyarlılık + sayım (BİLGİ); K62 = yanlılık kontrolü.

## 5. Büyük hareket, geçerli karar günü, etiket
### 5.1 Büyük mum ve BH1 (etiket)
- Büyük mum (gün i; yalnız i ve öncesi): TR_i >= k_b x medyan TR[ref] VE |C_i - O_i| >= m x medyan |C - O|[ref]; ref = [max(bas, i-{Bk['ref_max']}), i-1], en az
  {Bk['ref_min']} gün; k_b = {Bk['k_b']}, m = {Bk['m']}; TR referansı en az {Bk['tr_taban']} x C[i-1], gövde referansı en az {Bk['govde_taban']} x TR referansı (işlemsiz /
  düz bar tabanı). Kapanış kipinde (K62) gövde şartı yok.
- ONAY: [i, i+{og - 1}] içinde ilk kapanış > Hi -> YUKARI, < Lo -> AŞAĞI (Lo / Hi = ref penceresinin kapanış aralığı); çıkış yoksa SAHTE (onaysız), veri / kopukluk
  yetmezse BELİRSİZ.
- BH1 (ANA etiket) başlangıcı g = t'den SONRAKİ ilk ONAYLI büyük mum (g > t; ref başlangıcı bölgenin bas'ı; bölge g-1'e kadar sürmüş sayılır; onaysız büyük
  mumlar atlanır, sonraki onaylı mum aranır). y_h = 1 <=> g <= t + h; y_h = 0 <=> (t, t+h] içinde onaylı büyük mum yok; ölçülmez (NaN) <=> t + h + {og - 1} veri
  dışında ya da (t, t+h+{og - 1}] içinde kopukluk. Ufuklar {E['ufuk']} (ANA {E['ana_ufuk']}; başarı (1) için {E['basari1_ufuk']}). Etiket tamamlanma günü son_h = t + h + {og - 1}.
  bar (WF eğitim kuralı bunu kullanır). Yön = çıkılan kenar; büyüklük = ln(C[g+{og - 1}] / C[g-1]), ln(C[g+19] / C[g-1]), ATR cinsinden (C[g+{og - 1}] - C[g-1]) / ATR14[g-1].
- BH2 (v1 genişleme tanımı) v2'de koşulmaz: v1 sonuçları zaten kayıtlı; karşılaştırma v1 T1-T5 durumlarının v2 etiketiyle koşulmasıyla yapılır (SAPMA 1).
### 5.2 Geçerli karar günü (D1a) ve karar yaşları
- Karar yaşları {E['karar_yas']} (t = bas + yaş - 1); satır ancak: t >= tespit, bölge t kapanışında açık (t < bitiş), t uygun VE GEÇERLİ: TR[t-{int(Gc['gun']) - 1}..t]'nin her
  biri <= {Gc['k_sessiz']} x medyan TR[max(bas, t-{int(Gc['ref_max']) - 1}), t] (taban {Bk['tr_taban']} x C_t). Geçersiz yaş atlanır (kaydırılmaz). Bölge başına çok satır ->
  bütün belirsizlikler HİSSE kümeli bootstrap.
### 5.3 Bölgeden bağımsız büyük hareket (BHU; duyarlılık / kaçırılan için)
- g'de TR >= {Bk['k_b']} x medyan TR[g-{E['bhu']['ref_n']}, g-1] (en az {E['bhu']['ref_min']}) VE |gövde| >= {Bk['m']} x medyan |gövde| (aynı tabanlar) VE [g, g+{og - 1}] içinde
  [g-{E['bhu']['bant_n']}, g-1] kapanış aralığından çıkış; BAŞLANGIÇ = önceki {E['bhu']['tekil']} barda tutulmuş BHU yok; g-1 uygun.

## 6. Kontroller (D1b; 'basit piyasa kontrolleri')
- DIŞARI (kontrol a): aynı hisse, aynı yıl, aynı mutlak oynaklık ondalığı (NATR14'ün o günkü uygun kesitteki ondalığı); gün t tanımın HİÇBİR bölgesinin
  [bas, bitiş] aralığında değil, uygun, bar >= {K['ilk_bar']}. Gerçek satırların her (yıl, ondalık) hücresinden hücredeki gerçek satır sayısının
  ANA {K['disari_kat']['ANA']} / AILE {K['disari_kat']['AILE']} / ALT {K['disari_kat']['ALT']} / K62 {K['disari_kat']['K62']} katı gün (yerine koymadan, tohum sha256(sembol, tanım, 'DISARI', {K['tohum']})); sözde yaş = o hissenin gerçek yaşlarından çekilir, sözde bas = t - yaş + 1;
  AYNI geçerlilik (D1a), etiket, ön koşul ve özellikler. Karşılaştırmada tabaka = (hisse, yıl, NATR ondalığı); kontrol, gerçeğin tabaka dağılımına yeniden
  ağırlıklanır; kontrolsüz tabakadaki gerçek satır düşer (sayısı raporda).
- RASTGELE (kontrol b): hisse başına uygun gerçek bölge sayısının {K['rastgele_kat']} katı bölge; süre = o hissenin gerçek bölge sürelerinden (yerine koyarak), başlangıç
  tekdüze [{K['ilk_bar']}, n-1-süre-30]; sıkışma şartı YOK; aynı karar yaşları, geçerlilik, etiket, ön koşul ve özellikler. Tabaka = (yıl, yaş).
- Aynı model (bölüm 8) kontrol satırlarında kendi WF'siyle koşulur (ANA; D1b). Tam satır (etiket + özellik + getiri): ANA gerçek ve kontrol satırları, AILE
  gerçek satırları (bütün yıllar; model eğitimi için). Hafif satır (etiket + tabaka; yalnız başarı 1): ALT / K62 satırları ve AILE / ALT / K62 kontrolleri, YALNIZ
  {K['hafif_bas']}'den sonraki karar günleri (başarı 1 yalnız WF test yılları ve KASA'da ölçülür; önceki yıllar kullanılmaz). Tabaka ve örnekleme bütün yıllardan.

## 7. ÜÇ BAŞARI — KARAR KURALI (önceden; WF test yılları {W['kesif_yillar'][0]}-{W['kesif_yillar'][-1]} toplamında VE KASA'da; BIST ve ABD AYRI; hisse kümeli bootstrap B = {E['basari']['bootstrap']}, tohum {E['basari']['tohum']}, %95)
ANA hücre: tanım {E['ana_tanim']}, ön koşul {O['ana']}. P0 ve P2 alt kümeleri aynı kuralla BİLGİ olarak hesaplanır (canlı sınıf kapısında kullanılır, bölüm 13).
- (1) BÖLGEYİ ÖNCEDEN BULMAK = BAŞARILI <=> geçerli karar günlerinin {E['basari1_ufuk']} gün içinde BH1'e dönüşme oranı, DIŞARI'nın (tabakalı) oranından VE RASTGELE'nin
  (tabakalı) oranından yüksek: İKİSİNDE oran farkı > 0 ve %95 alt sınır > 0 (oran > 1 bunu izler), WF'de VE KASA'da. Ayrıca (BİLGİ): duyarlılık = dönemdeki
  BHU'ların g-1 gününde (en az 1 işlem günü önce) açık bölgesi olanların payı; kaçırılan büyük hareket sayısı; uyarı süresi (g - tespit, işlem günü; q25 /
  medyan / q75); kapsama (uygun hisse-günlerinin açık bölgedeki payı) ve kaldıraç = duyarlılık / kapsama; yanlış bölge payı (bölgenin ilk geçerli satırında
  y20 = 0 olanların payı).
- (2) GENİŞLEMEYİ ÖNCEDEN TAHMİN = BAŞARILI <=> (2a) M_TAM vs T1 (ufuk {E['ana_ufuk']}) Brier skill = 1 - Brier / Brier_T1 > 0 ve %95 alt > 0 VE (2b, D1b) bölgeye özgü:
  skill(gerçek) - skill(DIŞARI) > 0 ve alt > 0 VE skill(gerçek) - skill(RASTGELE) > 0 ve alt > 0 (ortak hisse kümeli bootstrap); WF'de VE KASA'da. 5 / 20 ufuk,
  T0, süre modelleri, tek grup modelleri, ablasyon BİLGİ.
- (3) YÖNÜ ÖNCEDEN TAHMİN = BAŞARILI <=> büyük harekete dönüşen (y20 = 1, yön ±1) geçerli karar günlerinde P(YUKARI) için M_TAM vs B1: Brier skill > 0 ve alt > 0
  VE dengeli doğruluk farkı (eşik 0,5) > 0 ve alt > 0; WF'de VE KASA'da. B0, B2 (yalnız KONUM; mekanik), M_KONUMSUZ vs B1, işlem sonucu, birleşik üç sınıf
  BİLGİ.
- Karar etiketleri: BAŞARILI / BAŞARISIZ / VERİ YOK (n < 30 ya da tek sınıf) / KASA AÇILMADI. (2) yalnız (2a) VE (2b) ile BAŞARILI; (2a) tutup (2b) tutmazsa
  'genişleme tahmini sıkışmaya özgü değil' diye yazılır.

## 8. Model, özellikler, temeller, walk-forward
- Tek model ailesi: sırt cezalı lojistik (V1.vdyt_lojistik; IRLS, ceza {E['model']['ridge']}, en çok {E['model']['tur']} tur); özellikler yalnız eğitimden uç kırpma
  {E['model']['winsor']} + z-ölçek, NaN -> 0; eğitim < {E['model']['min_egitim']} satır ise yıl atlanır. Karmaşık model yok.
- Özellik grupları (hepsi t ve öncesi; olaylarda bilgi günü <= t):

| grup | özellikler |
|---|---|
{oz}

- Genişleme modelleri (M_TAM bütün gruplar; ablasyon M_EKSI_<grup>; tek grup M_TEK_<grup>; süre yaklaşımları):

| model | gruplar |
|---|---|
{md}

- Yön modelleri:

| model | gruplar |
|---|---|
{my}

- Temeller: genişleme T0 = eğitim sıklığı {E['temel']['G_T0']}, T1 (KARAR) = {E['temel']['G_T1']} (pazar ayrı; yaş kovası x takvim ayı; hücre n < {E['temel']['kucuk_hucre']} ise sondan bir
  anahtar düşer); yön B0 = {E['temel']['Y_B0']}, B1 (KARAR) = eğitimde P(yukarı | piyasanın son 60 gün getirisi >= 0 / < 0), B2 = M yalnız KONUM (BİLGİ).
  Yaş kovaları {E['yas_kova']}.
- WALK-FORWARD: {W['kural']}. WF test yılları {W['kesif_yillar']} (aşama 'wf'; etiketi {W['wf_son']}'i aşan satır ölçülmez). KASA = {W['kasa'][0]} -> {W['kasa'][1]},
  test yılları {W['kasa_yillar']}, aynı eğitim kuralı; YALNIZ `kos --asama kasa` ile ve BİR KEZ açılır (vdyt2_kasa_acildi.json; varsa ret). Bütün ölçüler geriye
  bakar; tam veride hesaplanıp tarihe göre süzülür (geleceğe bakma testi test_vdyt2.py).

## 9. Süre (bölge başına)
- KM (BH1-onaylı büyük mum nedenine özgü; SÖNME ve SAHTE rakip; SANSÜR / BELİRSİZ sansür), Aalen-Johansen CIF, yaş kovası hazard'ı (V1.vdyt_sureklilik); ANA, P0
  ve P1. WF'de {W['wf_son']}'ten sonra biten / onayı taşan bölge SANSÜR.
- Dört yaklaşım ileriye dönük Brier (bölüm 8 modelleri, T0 ve T1'e karşı): A ORTAK (yalnız SÜRE), B HİSSEYE ÖZGÜ (SÜRE + HİSSE: yalnız t'de onayı bilinen, t'den
  önce biten bölgeler; en az {E['hisse_gecmis']['min_bolge']} yoksa 'yetersiz' bayrağı), C REJİM (SÜRE + REJİM), D ADAPTİF (SÜRE + HİSSE + REJİM). Bitiş olasılık olarak (p5 / p10 / p20).
- OLG (D2): y10 oranı (yaş >= 30) - (yaş <= 15), hisse kümeli bootstrap; beklenen işaret yazılmaz (iki yanlı), sonuç ne çıkarsa.

## 10. Olaylar (AYNI sisteme girdi; ayrı proje değil)
- Modelde OLAY grubu (bilgi kuralıyla) + ablasyon. E1 (koşul günü c = g0 - 21; pencereler {E['olay']['pencere_e1']}) ve E2 (c = g0 - 1; {E['olay']['pencere_e2']}):
  gözlenen (ilk onaylı BH penceresi) - beklenen (aynı c ayı / momentum / likidite tertili, yaşı ±{E['olay']['esleme']['yas_tol']}, ölçülen aralıkta aynı türden olayı
  olmayan en çok {E['olay']['esleme']['kontrol_n']} kontrol; V1.vdyt_olay_analizi) = 'haber mi bitirdi, zaten bitecek miydi'.
- Haberli / habersiz (BH'ye dönüşen bölgenin son geçerli satırı; g'ye göre): haberli = A / B olayı [g{E['haber']['haberli'][0]}, g+{E['haber']['haberli'][1]}];
  habersiz = A / B yok [g{E['haber']['habersiz'][0]}, g+{E['haber']['habersiz'][1]}] ve makro yok [g{E['haber']['makro'][0]}, g]; yukarı payı ve |büyüklük| farkı (yıl x momentum x
  likidite tabakalı). Habersiz bölgeler hiçbir analizden ÇIKARILMAZ.
- Olay-bölge zaman ilişkisi: olay eşleme tablosu (V1._vdyt_olay_bolge_satir: bölgenin [bas, bitiş + 20] aralığındaki her olay; olay günündeki bölge yaşı,
  onaylı BH günü - olay günü, BH'den önce oynaklık artışı başlamış mı); tür başına özet. Haberli / habersiz satırlarda yön motorunun dengeli doğruluğu ayrı (BİLGİ).

## 11. Çoklu test ve plasebo
- BH q = {E['coklu']['bh_q']} aile içinde: F1_BOLGE, F2_GENISLEME, F2_D1B, F3_YON, F4_OLAY, F5_SURE, F6_KATKI, F6_TEK_GRUP. Bir aile bulgusu 'TUTTU' ancak WF'de
  BH ile reddedilir VE KASA'da aynı işaretle %95 aralığı 0'ı dışlarsa.
- P1 plasebo (D4): her hissede gerçek olay sayısı kadar rastgele olay günü (bar 260 .. n-22), E1 ve E2, {E['coklu']['plasebo_olay_tekrar']} tekrar, tür başına en çok {E['coklu']['plasebo_ust']} olay;
  tekrar başına BH keşif sayısı (yanlış pozitif oranı) ve tür x kip x pencere |fark| eşiği (%{E['coklu']['plasebo_esik_pct']:.0f}). E1 / E2 bulgusu ancak bu eşiği de aşarsa sayılır.
- P2 plasebo = RASTGELE kontrolün kendisi (bölüm 6).

## 12. Değerlendirme (bilgi satırları; hepsi raporlanır)
5 / 10 / 20 gün genişleme Brier / log loss skill, kalibrasyon (10 kutu, ECE), kesinlik / duyarlılık (eğitimin %90 eşiği), genişlemeye kadar süre (KM / CIF),
uyarı süresi, yanlış bölge sayısı, kaçırılan büyük hareket sayısı, yön dengeli doğruluk + Brier, işlem sonucu: tahmin edilen yöne işaretli r5 / r10 / r20 (t+1
açılışından) ve rk5 / rk10 / rk20 (kırılım sonrası: çıkış gününün ertesi açılışından), maliyet sonrası, M_TAM - B1 farkı; MFE / MAE (20 gün); birleşik üç sınıf
(20 gün içinde yukarı BH / aşağı BH / yok): M = p20 x p_yukarı vs T1 x B1 (P0 temelleri), çok sınıflı Brier skill, P0 ve P1; sınıf değerlendirmesi (WF / KASA
test satırlarında sınıf başına gerçekleşen y10 / y20 oranı ve yukarı payı; yön kapısı uygulanmadan).

## 13. Sınıflandırma (canlı çıktı; eşikler eğitimden ya da sabit, test sonucuna göre değişmez)
- Canlı model: kesik ({E['kesik']}) içinde etiketi tamamlanan bütün ANA satırlarıyla eğitilir; q_yüksek = bu eğitim tahminlerinin %{S_['q_yuksek'] * 100:.0f} yüzdeliği (p10).
  WF / KASA sınıf değerlendirmesinde q_yüksek o test yılının eğitiminden.
- Kurallar (öncelik sırası): 'Genişleme başladı' = ANA bölge son {S_['basladi_gun']} işlem gününde büyük mumla bitti. 'Sıkışma yok' / 'Sıkışma oluşuyor' = açık bölge yok
  ve {{G1, G2, G3 ∨ G4}} üçünden en az {Ss['olusuyor_en_az']}'si doğru ise 'oluşuyor', değilse 'yok'. Açık bölge: karar günü geçersiz (D1a) ya da (2) o alt kümede
  BAŞARILI değil ya da p10 < q_yüksek -> 'Sıkışma devam ediyor'; p10 >= q_yüksek ve (3) o alt kümede BAŞARILI değil -> 'Yön belirsiz' (yön güvenilir değil); (3)
  BAŞARILI ise p_yukarı >= {S_['yukari']} -> 'Yukarı kırılma adayı', <= {S_['asagi']} -> 'Aşağı kırılma adayı', arada -> 'Genişlemeye yaklaşan sıkışma'. Alt küme: P1 bayrağı varsa P1,
  yoksa P2, yoksa P0.
- Güvenilirlik: genişleme YÜKSEK <=> (2) BAŞARILI ve KASA ECE <= {S_['guven_genisleme']['ece_max']} ve KASA skill >= {S_['guven_genisleme']['skill_min']}; ORTA <=> (2) BAŞARILI; DÜŞÜK değilse. Yön sınıflarında
  min(genişleme, yön); yön YÜKSEK <=> (3) BAŞARILI ve KASA ECE <= {S_['guven_yon']['ece_max']} ve KASA dengeli doğruluk farkı >= {S_['guven_yon']['ba_min']}.
- Tek nihai çıktı (hisse başına): (1) bölge var mı, (2) başlangıç tarihi, (3) kaç gündür (yaş), (4) sıkışma gücü = 100 x (1 - medyan(H-L) / ATRref) (0-100),
  (5) savunma hattı seviyesi (gövde tabanı), (6) p5 / p10 / p20, (7) zaman aralığı = p_h >= 0,5 olan ilk h ('<= h işlem günü'; yoksa '> 20'), (8) / (9) yukarı /
  aşağı olasılığı (büyük hareket olursa koşullu; ayrıca p20 x p_yukarı, p20 x p_aşağı), (10) güvenilirlik, (11) en önemli dayanaklar = lojistik katkı (katsayı x
  z-değer) mutlak en büyük 3; sınıf; ön koşul; geçerli gün; motor durumları; 'CANLI, test dışı'; veri eskiyse (> {S_['eski_veri_gun']} gün) bayrak.

## 14. Grafik (seçim kuralı sonuç görülmeden)
Gruplar {Gr['gruplar']}: BAŞARILI = ANA test satırı p10 >= q80 ve y10 = 1; BAŞARISIZ = p10 >= q80 ve y10 = 0 (yanlış alarm); KAÇIRILAN = BHU, g-1'de açık ANA bölge
yok; YÖN DOĞRU / YANLIŞ = yön testi satırında (p >= 0,5) çıkılan kenarla aynı / değil; HABERSİZ = BH'ye dönüşen, g çevresinde olay yok. Pazar x grup başına {Gr['grup_n']}
örnek, numpy default_rng(sha256 tohum: {Gr['tohum']}, pazar, grup), aday listesi (sembol, t) sıralı. Paket (`paket`): örnek başına [bas-{Gr['on_bar']}, son olay+{Gr['son_bar']}] OHLCV + meta;
dosya başına < {Gr['paket_mb']} MB. `ciz` YALNIZ paketten (Colab'da bağımsız; var olan PNG'nin üstüne yazmaz): {Gr['boyut']} inç, {Gr['dpi']} dpi, büyük ve net gövde + fitil, ayrı
hacim paneli, küçük mum bölgesi, savunma hattı (t'ye kadar), tespit tarihi, karar günü, büyük hareket başlangıcı, yön; her örnek iki PNG: TAM ve TESPİT GÜNÜ
(yalnız t'ye kadarki mumlar; büyük hareket / yön / sonuç / grup adı YOK). Grafikler Drive'a parçalı yüklenmez; paketten Colab'da yeniden üretilir.

## 15. Sürüm ve çıktılar
Sürüm etiketi {VDYT2_ETIKET}; repo arastirma_cikti/vdyt/{VDYT2_ETIKET}/ (ön kayıt, kapsam, sonuç JSON, rapor, hata raporu, parametre kaydı, canlı tablo,
grafik paketi); büyük ara tablolar /tmp/vdyt2/<aşama>/ (bölge, satır, kontrol, tahmin, BHU, haber); Drive hedefi {VDYT2_YOL['drive']}/ (yüklemeyi ana oturum yapar;
dosya < 3 MB). Her çıktıda sürüm, VDYT2.py ve VDYT.py sha256'sı, eşik mührü ve ön kayıt commit'i. Mevcut dosyalar silinmez / ezilmez (ön kayıt, KASA işareti, canlı
tablo ve PNG'ler üzerine yazmaz).

## 16. Yanlılık beyanı
- Yaşayan evren (V_BIST, k60): batan / kotasyondan çıkanlar yok; aşağı yönlü büyük hareketler ve sessizlikten sonra batanlar eksik -> yön sonuçları YUKARI
  lehine yanlı olabilir; BIST_K62 (çıkmış 92 hisse dahil, yalnız kapanış) başarı (1) için çıkmış / yaşayan ayrımıyla BİLGİ. ABD delist: veri yok.
- Yahoo takvimi yalnız bugün Yahoo'da olan 1.410 hisse; kalanında 2022-11 öncesi bilanço günü 10-Q / 10-K vekili (bilanço -> 10-Q medyan 8 gün). KAP saati
  18:00 varsayımı. Makro: yalnız TARİH (CPI / istihdam / TÜİK EKSİK). BIST KAP özel durum açıklamaları EKSİK -> BIST 'habersiz' = kayıtlı veri setlerinde olay yok.
- Etiket ve özellikler tam veride hesaplanıp tarihe göre süzülür; her ölçü geriye bakar (sentetik testte t sonrası barlar bozulunca özellikler ve geçerlilik
  aynı). Panel kesitleri (tertil, ondalık) yalnız aynı günün değerleri.

## 17. SAPMA / BOŞLUK (iş tanımına göre; ölçümden önce)
1. BH2 (v1 genişleme etiketi) ayrıca koşulmaz; v1 sonuçları kayıtlı (Ç162). v1 karşılaştırması v1 T1-T5 DURUMLARININ v2 bölge kuralı + BH1 etiketiyle koşulmasıdır.
2. BH1 başlangıcı 'ilk ONAYLI büyük mum': iş tanımındaki 'ilk büyük mum günü' + '10 günde bant çıkışı' şartının gerçek zamanlı biçimi; onaysız (sahte) büyük
   mumlar etiket olayı değildir, süre analizinde rakip olaydır. Referans pencere bölge başı bas'tan g-1'e (en çok 60 gün).
3. G3 (yaklaşan tepe-dip) eğim ölçüsü L = 10 günlük en küçük kareler eğimi; G4 penceresi 20 gün (tekrar test için 10 gün kısa; v1 savunma kuralı en az 3 temas ve
   5 bar aralık ister). G4 'savunulan' = hat VAR ve kapanışla kırılma YOK.
4. Modeller P0 satırlarıyla eğitilir, değerlendirme ve temeller alt kümede (bölüm 3). AILE tanımlarında yalnız M_TAM; ALT tanımlarında model yok (yalnız başarı 1).
5. Sınıf 'Yön belirsiz' iş tanımındaki gibi yön motoru geçmediğinde verilir; yön motoru geçtiğinde kararsız aralık (0,40-0,60) 'Genişlemeye yaklaşan sıkışma'dır.
   Genişleme motoru (2) geçmediyse 'Genişlemeye yaklaşan' ve aday sınıfları verilmez ('Sıkışma devam ediyor').
6. Plasebo P1 tekrar {E['coklu']['plasebo_olay_tekrar']} (v1: 100, yalnız E2); v2'de E1 ve E2 birlikte (aynı toplam hesap) ve bulgu başına eşik.
7. ABD 8-K'ların 'bilanço günü ±3 iş günü' süzgeci v1 bilanço kümesiyle (Nasdaq / EDGAR) yapılır (v1 kodu; Yahoo değişikliğinden önce).
8. BOŞLUK: BIST 2015 öncesi OHLC yok (WF eğitimi 2016+); ABD delist yok; CPI / istihdam / TÜİK takvimi yok; BIST özel durum açıklamaları yok; ABD Yahoo takvimi
   1.410 hisse.
9. Kapsam (bölüm 19) yalnız sayım: bölge, geçerli karar günü, kontrol satırı, BHU TOPLAM sayısı; oran, yön, getiri, süre / bitiş türü dağılımı YOK.
10. Veri sha256'ları bu konteynerdeki /tmp dosyalarına bağlıdır; Faz 2 aynı veriyle koşmalı (değişirse SAPMA + yeni satırlar + kapsam yeniden).
11. Hesap sınırı: ALT / K62 satırları ve AILE / ALT / K62 kontrolleri yalnız {K['hafif_bas']} sonrası etiketlenir (bölüm 6); ALT tanımlarında model yok. ANA'da
    kontrol katsayısı 5, diğerlerinde 2 (ANA'da tabaka kapsaması öncelikli).
12. G5 ailesinde bölgenin devamı çekirdek G1 VE G2 ile (bölüm 4); iş tanımındaki 'G5 = G1 ve G2 ve (G3 ya da G4)' AÇILIŞ şartıdır. Gerekçe: tepe-dip / destek
    şartı her gün yeniden aranırsa uzun sessiz bölge gün aşırı bölünür (sentetik sınamada görülen tasarım sorunu; gerçek veride hiçbir sonuç görülmeden).
13. Birleşik üç sınıf ve sınıf değerlendirmesi P0 temelleriyle (BİLGİ); karar hücreleri bölüm 7.
14. Kapsam sayımı (bölüm 19) ön kayıttan hemen önce AYNI kodla yapıldı (vdyt2_kapsam.json 'kod_sha256' = KOD_SHA256; değilse ret sebebi sayılır, ana oturum denetler).

## 18. Veri sha256 (ön kayıt anı; `kos` / `canli` yeniden hesaplar, farklıysa ret)
{vs}

## 19. Kapsam (YALNIZ SAYI; `python -I VDYT2.py kapsam`, {kz})
{chr(10).join(bh)}

{chr(10).join(ks)}

Ayrıntı: arastirma_cikti/vdyt/{VDYT2_ETIKET}/VDYT2_KAPSAM.md.

## 20. Faz 2 komutları
1. (ana oturum) bu dosyayı, VDYT2.py'yi ve test_vdyt2.py'yi denetler, git'e işler (VDYT.py zaten işlenmiş).
2. `python -I VDYT2.py kos --asama wf` -> WF ölçümü + VDYT2_RAPOR_wf.md (mühür, iki kod, veri sha256 ve git doğrulanır; yoksa ret).
3. `python -I VDYT2.py kos --asama kasa` -> KASA bir kez; karar tablosu (üç başarı ayrı) + teyit.
4. `python -I VDYT2.py canli` -> vdyt2_canli_<tarih>.csv (CANLI, test dışı). 5. `python VDYT2.py paket --asama kasa` -> grafik paketi; Colab: `v2_ciz(paket, çıktı)`.
Tahmini süre (bu konteyner, 4 çekirdek, 3 işçi; BIST 40 hisselik ölçümden ölçeklenmiş): kapsam BIST ~3 dk, ABD ~30 dk, BIST_K62 ~2 dk; `kos wf` BIST ~10 dk +
ABD ~60-80 dk + K62 ~5 dk; `kos kasa` aynı (~75-95 dk); canlı ~40 dk (ABD fiyatı kesiksiz yeniden okunur); paket < 5 dk. Bellek: ABD tam satır tabloları birkaç GB.

## 21. Değişmezlik
VDYT2_ESIK, VDYT2_OZELLIK, VDYT2_MODEL (ve içe aktarılan v1 olay / EDGAR tanımları) değişirse ESIK_SHA256; VDYT2.py ya da VDYT.py değişirse KOD satırları; veri
değişirse veri sha256 tutmaz -> `kos` / `canli` durur.
"""


def _cakisma_kontrol_vdyt2(_once=_CK_ONCE_VDYT2, _dosya="VDYT2.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_VDYT2", "_CK_KAYIT", "_cakisma_kontrol_vdyt2", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "pickle", "hashlib", "glob", "gzip", "copy", "_dt", "annotations",
           "Any", "Callable", "Dict", "List", "Optional", "Tuple", "V1")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_vdyt2()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=VDYT2_SURUM)
    ap.add_argument("komut", choices=["kapsam", "onkayit", "kos", "canli", "paket", "ciz", "rapor"])
    ap.add_argument("--asama", default="wf", choices=["wf", "kasa"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--isci", type=int, default=3)
    ap.add_argument("--pazar", action="append", default=None)
    ap.add_argument("--paket", default=None, help="ciz: paket klasörü")
    a_ = ap.parse_args()
    try:
        if a_.komut == "kapsam":
            v2_kapsam(a_.pazar, a_.cikti, a_.isci); print(_v2_yol("kapsam_md", a_.cikti))
        elif a_.komut == "onkayit":
            y_ = v2_onkayit(a_.cikti); print(y_, "mühür", v2_esik_sha(), "kod", v2_kod_sha(), "VDYT.py", v2_v1_kod_sha(), "dosya sha256", V1.vdyt_sha_dosya(y_))
        elif a_.komut == "kos":
            R_ = v2_kos(a_.asama, a_.cikti, a_.isci, pazarlar=a_.pazar)
            print(json.dumps(_v2_kayit(R_["karar"]), ensure_ascii=False, default=str, indent=1)); print(R_["rapor"])
        elif a_.komut == "canli":
            print(v2_canli(a_.cikti, a_.isci, pazarlar=a_.pazar))
        elif a_.komut == "paket":
            print("\n".join(v2_paket(a_.asama, a_.cikti, a_.pazar)))
        elif a_.komut == "ciz":
            if not a_.paket or not a_.cikti:
                raise Vdyt2Hata("ciz: --paket ve --cikti gerekli")
            print("\n".join(v2_ciz(a_.paket, a_.cikti)))
        else:
            print(v2_rapor(a_.asama, a_.cikti))
    except (Vdyt2Hata, V1.VdytHata, FileNotFoundError) as ex:
        vdyt2log.error("%s", ex); sys.exit(1)
