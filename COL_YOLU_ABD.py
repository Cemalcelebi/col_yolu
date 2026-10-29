# =====================================================================
# COL_YOLU_ABD.py — ABD hisselerinde Çöl Yolu formasyonu: üçlü bariyer, meta-etiketleme, görsel model (CNN), backtest aşırı uyumu
# Sürüm: CY v1.0 (2026-10-29, K51; Cemal'in araştırma görevi 29 Eki 2026)
#
# AMAÇ (Cemal): sert düşüş -> küçük gövdeli / gövdesiz mumlarla uzun sıkışma -> güçlü yükseliş ilişkisini ABD'de araştır. Yükseliş olduktan
#   sonra hisse bulmak değil, formasyon OLUŞURKEN gelecekteki performans ihtimalini ölç. Başarısız örnekler de karşılaştırılır.
# KAYNAKLAR: López de Prado 2018 (üçlü bariyer, meta-etiketleme, arındırma + ambargo), Gu-Kelly-Xiu 2020 (ağaç modeli, sayısal özellik),
#   Jiang-Kelly-Xiu 2023 (OHLC grafik resminden CNN), Bailey-Borwein-López de Prado-Zhu 2017 (PBO, CSCV), Bailey-López de Prado 2014
#   (deflated Sharpe), Shumway 1997 (borsadan çıkış getirisi ~ -%30).
#
# ÖN KAYIT (29 Eki 2026, sonuç görülmeden yazıldı; değişirse sürüm ve not düşülür):
#  VERİ (A): ABD = V_ABD (bugün işlem gören 1.411 hisse, 2015-06 -> 2026-10) + K34 Yahoo (nakdi biten 1.903 küçük / sıkıntılı şirket,
#   2020-10 ->) + K34 Tiingo (borsadan çıkmış / batmış 438 şirket örneklemi, 2020-10 ->, ağırlık 1,83 = evren / örnek). K34 şirketleri
#   evrene İLK SEC nakit pisti bildirimi tarihinden itibaren girer (o gün bilinen bilgi; geleceğe bakan evren seçimi yok). Fiyatlar
#   31.08.2026'da kesilir (fon krizi kuralı). Hayatta kalma yanlılığı: 2015-2020 arası yalnız bugün işlem görenler var (yanlı); 2021
#   sonrası batanların bir örneklemi var (kısmi). Etki ayrıca ölçülür (H9). Çoğaltma: Avrupa (V_AVR, 581) ve BIST (V_BIST, 581) ayrı.
#  LİKİDİTE (K): sinyal günü kapanış >= 1 $ (ABD), 20 gün medyan işlem değeri ABD >= 1 M$, AVR >= 1 M€ (Kur), BIST: o günkü BIST
#   hisselerinin 20. yüzdeliğinin üstü (TL enflasyonu); bütün pazarlarda ayrıca o günün pazar içi 20. yüzdeliğinin üstü.
#  MALİYET (K): tek yön komisyon ABD / AVR %0,05, BIST %0,10 + kayma = 0,25 x son 20 gün medyan gün aralığı (H-L / önceki kapanış),
#   en az %0,05, en çok %2; gidiş-dönüş iki kat. Borsadan çıkış: seri vadeden önce biterse son kapanışta çıkılır; son 60 gün getirisi
#   eksiyse ek -%30 (Shumway); bariyer değmediyse etiket 0.
#  BİRİNCİL MODEL (B): ÇÖL YOLU OLUŞURKEN (P1), d günü, pencere W = son L bar (yalnız d ve öncesi):
#   1 SERT DÜŞÜŞ: W'nin en düşüğü / W'den önceki 250-L barın en yükseği - 1 <= DÜŞÜŞ (ana -%35).
#   2 SIKIŞMA çekirdeği: DİPTE (W kapanış medyanı son 250 bar aralığının alt %35'inde), SAVUNMA (W'nin son %40'ında ilk %60'ın dibinin
#     yarım normal gün aralığından fazla altına inilmez), DAR BANT (W kapanışlarının %10-%90 bandı / medyan <= 6 x W öncesi normal gün aralığı).
#   3 İMZALAR (COL_v1 D12 ile aynı ruh): küçük mum (W gün aralığı medyanı / W öncesi 250 bar medyanı <= KÜÇÜK, ana 0,80), Bollinger
#     daralması (W'deki en dar BB genişliği son 250 günün en dar %15'inde), doji artışı (W doji payı >= W öncesi 250 bar doji payı, > 0;
#     doji = gövde / aralık < 0,10), hacim kuruması (W hacim medyanı <= W öncesi 60 bar medyanının %90'ı); İMZA >= İMZA_MIN (ana 3).
#   Ana yapı: L = 60, DÜŞÜŞ -0,35, KÜÇÜK 0,80, İMZA_MIN 3; hissede 40 işlem gününde tek. KIRILIM (P2): P1'den sonra 60 gün içinde W
#   gövde tavanının (%0,2 payla) üstünde ilk kapanış. EŞLER (H2): 1 + 2 tutan, imza <= 1 olan günler (aynı düşüş ve dip, sıkışma yok).
#  ETİKET (E): giriş d+1 açılışı; ÜÇLÜ BARİYER ana: +%20 hedef / -%10 zarar / 60 işlem günü (gün içi High / Low, boşlukta açılış, aynı
#   gün ikisi = zarar); y = 1 hedef önce. Bilgi: +%8 / -%8 / 20 gün.
#  TABAN: aynı gün, aynı pazar, aynı oynaklık (60 gün) ondalığındaki likit bütün hisse-günlerinin ortalaması (rastgele eş).
#  DÖNEMLER (I): eğitim sinyal 2016-01..2020-12, doğrulama 2021-01..2022-12, nihai test 2023 ve 2024-01..2026-06-05; eğitim etiketleri
#   bir sonraki dönem başından 10 gün önce biter (arındırma + ambargo). Meta model yıl yıl ileri yürür (her yıl yalnız önceki yıllarla).
#  META-ETİKETLEME (F): P1 adayları üzerinde LightGBM (300 ağaç, derinlik 4, yaprak 15, öğrenme 0,03, en az 20 örnek); seçim payı
#   s* {0,3 0,5 0,7} doğrulamada (2021-22) en yüksek ortalama net getiri; eşik p* = doğrulama olasılıklarının (1-s*) yüzdeliği; testte sabit.
#  GÖRSEL MODEL (G, H): Jiang-Kelly-Xiu tarzı 60 günlük siyah-beyaz OHLC + 20 gün ortalama + hacim resmi (64 x 180 piksel), küçük CNN
#   (16-32-64 kanal, 5x3 çekirdek, 2x2 havuz; CPU için JKX'ten küçük). Eğitim havuzu: 2016-20 likit ABD hisse-günlerinden rastgele 100 bin
#   + bütün eğitim P1 adayları; doğrulama 2021-22 (erken durma). AYNI havuzda AYNI etiketle sayısal LightGBM (genel) eğitilir; ikisi
#   aynı test adaylarında karşılaştırılır (AUC, seçilmiş adayların isabeti).
#  PARAMETRE ARAMA (J): ızgara DÜŞÜŞ {-0,25 -0,35 -0,50} x L {40 60 90} x KÜÇÜK {0,65 0,80} x İMZA_MIN {2 3} = 36 yapı; hepsi
#   cy_izgara.csv'ye yazılır; PBO = CSCV (16 blok, aylık net getiri, 2016-22), DSR (36 deneme). KARAR ana yapıyla verilir (seçilmiş
#   yapı bilgi; seçim yanlılığı PBO ile ölçülür).
#  PORTFÖY: 10 yuva, günde en çok 2 yeni giriş (meta / CNN olasılığı sırası; P1'de rastgele sıra yok, sinyal sırası), çıkış üçlü bariyer,
#   maliyetli; kıyas: eşit ağırlıklı likit piyasa ve aynı kurallı 20 rastgele portföyün ortancası.
#  HİPOTEZLER (karar eşikleri; hücre = ABD 2023 ve ABD 2024-26, ikisi de):
#   H1 P1 isabeti (y) - taban >= +5 puan, ay kümeli bootstrap %95 alt ucu > 0, net getiri - taban > 0, n >= 30.
#   H2 P1 - EŞLER (taban farkları arası) >= +5 puan, alt uç > 0.
#   H3 P2 (kırılım) - taban, H1 şartları.
#   H4 META: seçilen P1 - bütün P1 isabet >= +5 puan, alt uç > 0, net getiri farkı > 0.
#   H5 CNN: test AUC (P1 adayları) alt uç > 0,50 ve CNN seçimi - bütün P1 >= +5 puan, alt uç > 0.
#   H6 CNN ile sayısal model aynı adaylarda: AUC farkı ve aralığı (yön önceden yok).
#   H7 PORTFÖY: meta portföyü maliyet sonrası eşit ağırlıklı piyasayı, rastgele ortancasını VE SPY'yi geçer (endeks kıyası: ABD SPY ve IWM,
#      AVR ^STOXX (fiyat endeksi), BIST XU100; yfinance, veri klasöründe endeks.pkl).
#   H8 AŞIRI UYUM: PBO < 0,5 ve seçilmiş yapının DSR >= 0,95.
#   H9 HAYATTA KALMA: batanlar çıkarılınca H1 farkı ne kadar değişir (bilgi).
#   H10 ÇOĞALTMA: donmuş sistem (ABD'de eğitilmiş modeller) AVR'de H1 ve H4; BIST bilgi.
#  SONUÇ: ÇÖL YOLU ÖNGÖRÜ DEĞERİ = H1 (ya da H3) VE H2 ABD'de tutar VE AVR'de H1 / H3 tutar -> 'İZ'; yalnız ABD -> 'ABD-ADAY'; yoksa 'İZ DEĞİL'.
#
#  KURAL_MOTORU: Y1 veri + evren + likidite   Y2 günlük ölçüler + birincil model   Y3 üçlü bariyer + maliyet   Y4 taban / eş
#                Y5 özellikler   Y6 meta-etiketleme   Y7 görsel model (CNN)   Y8 ızgara + PBO + DSR   Y9 portföy   Y10 rapor
#  ÇALIŞTIRMA (Colab, tek hücre): drive bağla; exec(open('/content/drive/MyDrive/col_tarayici/COL_YOLU_ABD.py').read()); cy_calistir()
#   Veri klasörü CY_VERI (varsayılan .../COLAB_VERILER/OUTPUT/COL_YOLU_ABD/veri); yoksa Colab gizli anahtarı GH_TOKEN ile repo
#   'islenmis-veri' dalından açılır; batan şirket fiyatları Tiingo lisansı gereği pakette yok: TIINGO_TOKEN gizli anahtarı varsa
#   indirilir, yoksa batanlar olmadan koşar ve rapora yazılır. Çıktılar CY_CIKTI (varsayılan /content/drive/MyDrive/COLAB_VERILER/OUTPUT/COL_YOLU_ABD).
# =====================================================================
from __future__ import annotations

import io
import json
import logging
import lzma
import math
import os
import sys
import time
import zlib
from dataclasses import dataclass, field
from itertools import combinations
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_CK_ONCE_CY = {k: id(v) for k, v in dict(globals()).items()}   # çakışma kapısı: yüklenmeden önceki adlar

CY_SURUM = "CY v1.0 (2026-10-29, K51 ABD Çöl Yolu: üçlü bariyer, meta-etiketleme, CNN, PBO/DSR, batanlar dahil)"
cylog = logging.getLogger("col.cy")

CY: Dict[str, Any] = {
    "kriz": "2026-08-31", "alive_sinir": "2026-08-01", "ilk_gun": "2015-06-01",
    "egitim": ("2016-01-01", "2020-12-31"), "dogrulama": ("2021-01-01", "2022-12-31"),
    "test": (("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-06-05")),
    "embargo_gun": 10,
    "tb": {"ust": 0.20, "alt": -0.10, "ufuk": 60}, "tb_kisa": {"ust": 0.08, "alt": -0.08, "ufuk": 20},
    "komisyon": {"ABD": 0.0005, "AVR": 0.0005, "BIST": 0.0010}, "kayma_kat": 0.25, "kayma_min": 0.0005, "kayma_tavan": 0.02,
    "delist_kayip": -0.30,
    "likit": {"ABD": 1e6, "AVR": 1e6, "BIST": None}, "fiyat_min": {"ABD": 1.0, "AVR": 0.0, "BIST": 0.0}, "likit_yuzde": 0.20,
    "col": {"dusus": -0.35, "L": 60, "kucuk": 0.80, "imza_min": 3, "konum": 0.35, "bant_kat": 6.0, "son_pay": 0.40, "bb_yuzde": 0.15,
            "doji_esik": 0.10, "doji_kat": 1.0, "hacim_kat": 0.90, "ayri": 40, "kirilim_gun": 60, "kirilim_pay": 1.002, "es_imza_max": 1},
    "izgara": {"dusus": (-0.25, -0.35, -0.50), "L": (40, 60, 90), "kucuk": (0.65, 0.80), "imza_min": (2, 3)},
    "meta": {"pay": (0.3, 0.5, 0.7), "n_min_egitim": 100,
             "lgbm": {"n_estimators": 300, "learning_rate": 0.03, "num_leaves": 15, "max_depth": 4, "min_child_samples": 20,
                      "subsample": 0.8, "subsample_freq": 1, "colsample_bytree": 0.8, "reg_lambda": 1.0, "verbose": -1, "n_jobs": 4}},
    "genel_lgbm": {"n_estimators": 400, "learning_rate": 0.03, "num_leaves": 31, "max_depth": 6, "min_child_samples": 200,
                   "subsample": 0.8, "subsample_freq": 1, "colsample_bytree": 0.8, "reg_lambda": 1.0, "verbose": -1, "n_jobs": 4},
    "havuz": {"egitim": 100000, "dogrulama": 25000, "test": 25000},
    "cnn": {"gun": 60, "yuk": 64, "fiyat_px": 51, "kanal": (16, 32, 64), "epoch": 5, "sabir": 1, "batch": 256, "lr": 1e-3, "tohum": 51},
    "portfoy": {"slot": 10, "gunluk_azami": 2, "rastgele_n": 20},
    "karar": {"fark": 0.05, "n_min": 30, "boot": 2000, "tohum": 51},
    "pbo_blok": 16,
    "endeks": {"ABD": ("SPY", "IWM"), "AVR": ("^STOXX",), "BIST": ("XU100.IS",)},
}


@dataclass
class CYAyar:
    veri: str = field(default_factory=lambda: os.environ.get("CY_VERI", "/content/drive/MyDrive/COLAB_VERILER/OUTPUT/COL_YOLU_ABD/veri"))
    cikti: str = field(default_factory=lambda: os.environ.get("CY_CIKTI", "/content/drive/MyDrive/COLAB_VERILER/OUTPUT/COL_YOLU_ABD"))
    tiingo: str = field(default_factory=lambda: os.environ.get("CY_TIINGO", ""))
    is_parcacigi: int = field(default_factory=lambda: int(os.environ.get("CY_ISCI", "4")))
    cnn: bool = field(default_factory=lambda: os.environ.get("CY_CNN", "1") == "1")
    pazarlar: Tuple[str, ...] = ("ABD", "AVR", "BIST")


# ---------------------------------------------------------------- Y1 VERİ + EVREN
def _cy_lzma_ac(paket: str, hedef: str) -> List[str]:
    """islenmis-veri dalı paketini (manifest.json + <ad>.xz.NNN parçaları) sha256 doğrulamalı açar (FON_IZI fi_veri_paket_ac eşi)."""
    import hashlib
    with open(os.path.join(paket, "manifest.json"), encoding="utf-8") as f:
        man = json.load(f)
    for ad, b in man["dosyalar"].items():
        h = hashlib.sha256()
        with open(os.path.join(paket, ad), "rb") as f:
            for blok in iter(lambda: f.read(1 << 20), b""):
                h.update(blok)
        if h.hexdigest() != b["sha256"]:
            raise RuntimeError(f"veri paketi bozuk: {ad}")
    os.makedirs(hedef, exist_ok=True); cikan = []
    for ad, b in man["veri"].items():
        ham = b"".join(open(os.path.join(paket, f"{ad}.xz.{no:03d}"), "rb").read() for no in range(b["parca"]))
        with open(os.path.join(hedef, ad), "wb") as g:
            g.write(lzma.decompress(ham))
        if os.path.getsize(os.path.join(hedef, ad)) != b["kaynak_boy"]:
            raise RuntimeError(f"veri paketi boyu tutmuyor: {ad}")
        cikan.append(ad)
    return cikan


def cy_veri_hazirla(A: CYAyar) -> None:
    """Colab: veri klasöründe V_ABD.pkl yoksa repo 'islenmis-veri' dalını (GH_TOKEN gizli anahtarıyla) indirip açar. Token koda yazılmaz."""
    if os.path.exists(os.path.join(A.veri, "V_ABD.pkl")):
        return
    tok = os.environ.get("GH_TOKEN", "")
    if not tok:
        try:
            from google.colab import userdata          # type: ignore
            tok = userdata.get("GH_TOKEN") or ""
        except Exception:
            tok = ""
    if not tok:
        raise FileNotFoundError(f"{A.veri} içinde V_ABD.pkl yok ve GH_TOKEN gizli anahtarı yok: veri paketi açılamıyor")
    import subprocess
    gec = "/content/cy_iv"
    if not os.path.exists(gec):
        r = subprocess.run(["git", "clone", "--depth", "1", "--branch", "islenmis-veri",
                            f"https://x-access-token:{tok}@github.com/Cemalcelebi/col_yolu.git", gec], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("islenmis-veri dalı indirilemedi (token / erişim)")
    _cy_lzma_ac(os.path.join(gec, "veri"), A.veri); _cy_lzma_ac(os.path.join(gec, "veri2"), A.veri)
    for ad in ("k34_orneklem.csv",):
        src = os.path.join(gec, "k34", ad)
        if os.path.exists(src):
            open(os.path.join(A.veri, ad), "wb").write(open(src, "rb").read())
    import urllib.request                                            # K34 evren tablosu main dalında (küçük CSV)
    rq = urllib.request.Request("https://api.github.com/repos/Cemalcelebi/col_yolu/contents/arastirma_cikti/col_yolu_abd/k34_evren.csv?ref=main",
                                headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github.raw"})
    try:
        with urllib.request.urlopen(rq, timeout=60) as r:
            open(os.path.join(A.veri, "k34_evren.csv"), "wb").write(r.read())
    except Exception as ex:
        cylog.warning("k34_evren.csv indirilemedi (batanlar ve küçükler olmadan koşar): %s", ex)
    cylog.info("veri paketi açıldı -> %s", A.veri)


def cy_tiingo_indir(A: CYAyar, evren: pd.DataFrame, klasor: str) -> int:
    """Batan şirket örneklemi fiyatları (Tiingo; anahtar yalnız ortam / Colab gizli anahtarı TIINGO_TOKEN). Var olan dosyayı yeniden indirmez."""
    tok = os.environ.get("TIINGO_TOKEN", "")
    if not tok:
        try:
            from google.colab import userdata          # type: ignore
            tok = userdata.get("TIINGO_TOKEN") or ""
        except Exception:
            tok = ""
    if not tok:
        return 0
    import urllib.request
    os.makedirs(klasor, exist_ok=True); n = 0
    for s in evren.loc[evren.kaynak == "tiingo", "sembol"].unique():
        yol = os.path.join(klasor, f"{s}.csv")
        if os.path.exists(yol):
            continue
        url = f"https://api.tiingo.com/tiingo/daily/{s}/prices?startDate=2020-10-01&format=csv&token={tok}"
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                open(yol, "wb").write(r.read())
            n += 1; time.sleep(75)                          # ücretsiz hesap: saatte 50 istek
        except Exception as ex:
            cylog.warning("Tiingo %s indirilemedi: %s", s, ex)
    return n


def _cy_temizle(d: pd.DataFrame, kriz: pd.Timestamp) -> pd.DataFrame:
    d = d[~d.index.duplicated(keep="last")].sort_index(); ix = pd.DatetimeIndex(d.index)
    d.index = (ix.tz_convert(None) if ix.tz is not None else ix).astype("datetime64[ns]")
    d = d[d.index <= kriz]
    ok = (d.Open > 0) & (d.High > 0) & (d.Low > 0) & (d.Close > 0) & (d.High >= d.Low)
    return d[ok]


def cy_veri_yukle(A: CYAyar, K: Dict[str, Any] = CY) -> Tuple[Dict[str, Dict[str, pd.DataFrame]], pd.DataFrame]:
    """Pazar -> sembol -> OHLCV(+Kur) ve evren tablosu (pazar, sembol, kaynak, evren_bas, batan, agirlik)."""
    kriz = pd.Timestamp(K["kriz"]); Vs: Dict[str, Dict[str, pd.DataFrame]] = {}; ev = []
    for pz in A.pazarlar:
        yol = os.path.join(A.veri, f"V_{pz}.pkl")
        if not os.path.exists(yol):
            cylog.warning("%s verisi yok: %s", pz, yol); continue
        V = pd.read_pickle(yol); Vt = {}
        for s, d in V.items():
            try:
                d = _cy_temizle(d, kriz)
            except Exception as ex:
                cylog.warning("%s %s temizlenemedi: %s", pz, s, ex); continue
            if len(d) >= 320:
                Vt[s] = d; ev.append({"pazar": pz, "sembol": s, "kaynak": f"V_{pz}", "evren_bas": d.index[0], "batan": False, "agirlik": 1.0})
        Vs[pz] = Vt
    # K34: küçük / sıkıntılı ve batan ABD şirketleri (evrene ilk SEC nakit pisti bildiriminden itibaren)
    ev_yol = next((p for p in (os.path.join(A.veri, "k34_evren.csv"), os.path.join(os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else ".",
                                                                                   "arastirma_cikti", "col_yolu_abd", "k34_evren.csv")) if os.path.exists(p)), None)
    if "ABD" in Vs and ev_yol:
        E = pd.read_csv(ev_yol, parse_dates=["ilk_giris"]); Y = {}
        yy = os.path.join(A.veri, "k34_yahoo.pkl")
        if os.path.exists(yy):
            Y = pd.read_pickle(yy)
        tk = A.tiingo or os.path.join(A.veri, "tiingo")
        cy_tiingo_indir(A, E, tk); n_y = n_t = 0
        for r in E.itertuples():
            if r.sembol in Vs["ABD"]:
                continue
            d = None
            if r.kaynak == "yahoo" and r.sembol in Y:
                d = Y[r.sembol]
                if isinstance(d.columns, pd.MultiIndex):
                    d.columns = d.columns.get_level_values(0)
                d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float)
            elif r.kaynak == "tiingo" and os.path.exists(os.path.join(tk, f"{r.sembol}.csv")):
                t = pd.read_csv(os.path.join(tk, f"{r.sembol}.csv"))
                if len(t) and "adjClose" in t:
                    t.index = pd.to_datetime(t.date.str[:10]); d = t[["adjOpen", "adjHigh", "adjLow", "adjClose", "adjVolume"]].astype(float)
                    d.columns = ["Open", "High", "Low", "Close", "Volume"]
            if d is None:
                continue
            try:
                d = _cy_temizle(d, kriz)
            except Exception as ex:
                cylog.warning("K34 %s temizlenemedi: %s", r.sembol, ex); continue
            if len(d) < 320:
                continue
            Vs["ABD"][r.sembol] = d; n_y += r.kaynak == "yahoo"; n_t += r.kaynak == "tiingo"
            ev.append({"pazar": "ABD", "sembol": r.sembol, "kaynak": f"K34_{r.kaynak}", "evren_bas": max(pd.Timestamp(r.ilk_giris), d.index[0]),
                       "batan": bool(r.kaynak == "tiingo"), "agirlik": float(r.w) if r.kaynak == "tiingo" else 1.0})
        cylog.info("K34 eklendi: Yahoo %d, Tiingo (batan) %d", n_y, n_t)
    return Vs, pd.DataFrame(ev)


def cy_endeks(A: CYAyar, K: Dict[str, Any] = CY) -> pd.DataFrame:
    """Endeks kapanışları (veri klasöründe endeks.pkl; yoksa yfinance ile indirilir ve kaydedilir). Hata -> boş tablo (rapora not)."""
    yol = os.path.join(A.veri, "endeks.pkl")
    if os.path.exists(yol):
        return pd.read_pickle(yol)
    try:
        import yfinance as yf
        kod = sorted({k for v in K["endeks"].values() for k in v})
        d = yf.download(kod, start=K["ilk_gun"], end=K["kriz"], auto_adjust=True, progress=False, threads=False)["Close"]
        d.index = pd.DatetimeIndex(d.index).tz_localize(None); d = d[d.index <= pd.Timestamp(K["kriz"])]
        try:
            d.to_pickle(yol)
        except Exception:
            pass
        return d
    except Exception as ex:
        cylog.warning("endeks indirilemedi: %s", ex)
        return pd.DataFrame()


def cy_likit_esik(V: Dict[str, pd.DataFrame], pazar: str, K: Dict[str, Any] = CY) -> pd.Series:
    """Gün -> pazar içi 20 gün medyan işlem değeri yüzdelik eşiği (likit_yuzde)."""
    T = pd.DataFrame({s: (d.Close * d.Volume * (d["Kur"] if "Kur" in d else 1.0)).rolling(20, min_periods=15).median() for s, d in V.items()})
    return T.quantile(K["likit_yuzde"], axis=1)


# ---------------------------------------------------------------- Y2 GÜNLÜK ÖLÇÜLER + BİRİNCİL MODEL
def _cy_kayan_argmin(x: np.ndarray, w: int) -> np.ndarray:
    """Son w barda en düşüğün kaç bar önce olduğu (geriye bakar)."""
    n = len(x); out = np.full(n, np.nan)
    if n < w:
        return out
    from numpy.lib.stride_tricks import sliding_window_view
    sw = sliding_window_view(np.where(np.isfinite(x), x, np.inf), w)
    out[w - 1:] = (w - 1 - np.argmin(sw, axis=1)).astype(float)
    return out


def cy_olculer(d: pd.DataFrame, K: Dict[str, Any] = CY, Ls: Optional[Tuple[int, ...]] = None) -> Dict[str, Any]:
    """Bir hissenin günlük ölçüleri (yalnız o gün ve öncesi). Dönüş: 'F' özellik tablosu ve L başına çöl ölçüleri."""
    O = d.Open.astype(float); H = d.High.astype(float); L_ = d.Low.astype(float); C = d.Close.astype(float); V = d.Volume.astype(float).clip(lower=0)
    C1 = C.shift(1); eps = 1e-12; rng = (H - L_).clip(lower=0)
    ar = rng / C1                                                    # gün aralığı (fitil dahil; Cemal'in 'küçük mum'u)
    go = ((C - O).abs() / rng.where(rng > 0)).fillna(1.0)            # gövde / aralık (aralık 0 -> gövdesiz değil, ölçü dışı 1)
    uw = ((H - np.maximum(O, C)) / rng.where(rng > 0)).fillna(0.0); lw = ((np.minimum(O, C) - L_) / rng.where(rng > 0)).fillna(0.0)
    doji = (go < K["col"]["doji_esik"]).astype(float)
    ref250 = ar.rolling(250, min_periods=120).median()
    sm20 = C.rolling(20).mean(); sd20 = C.rolling(20).std(ddof=0); bbw = 4 * sd20 / sm20
    tr = pd.concat([H - L_, (H - C1).abs(), (L_ - C1).abs()], axis=1).max(axis=1); atr14 = tr.ewm(alpha=1 / 14, adjust=False).mean()
    e20 = C.ewm(span=20, adjust=False).mean(); e50 = C.ewm(span=50, adjust=False).mean(); s200 = C.rolling(200, min_periods=160).mean()
    g = C.pct_change(fill_method=None); dv = C * V * (d["Kur"] if "Kur" in d else 1.0); dv20 = dv.rolling(20, min_periods=15).median()
    fark = C.diff(); yu = fark.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean(); du = (-fark.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    maxH250 = H.rolling(251, min_periods=200).max(); minL250 = L_.rolling(251, min_periods=200).min()
    F = pd.DataFrame({
        "ar1": ar / ref250, "ar5": ar.rolling(5).mean() / ref250, "ar20": ar.rolling(20).median() / ref250, "ar60": ar.rolling(60).median() / ref250,
        "go20": go.rolling(20).mean(), "go60": go.rolling(60).mean(), "uw20": uw.rolling(20).mean(), "lw20": lw.rolling(20).mean(),
        "doji20": doji.rolling(20).mean(), "doji60": doji.rolling(60).mean(),
        "bbw": bbw, "bbw_yuzde250": bbw.rolling(250, min_periods=120).rank(pct=True), "bbw_deg20": bbw / bbw.shift(20) - 1,
        "atr14": atr14 / C, "atr_oran": atr14 / atr14.rolling(100, min_periods=60).mean(),
        "v10_50": V.rolling(10).mean() / (V.rolling(50).mean() + eps), "v20_120": V.rolling(20).mean() / (V.rolling(120, min_periods=80).mean() + eps),
        "ema20_egim5": e20 / e20.shift(5) - 1, "ema20_egim20": e20 / e20.shift(20) - 1, "ema50_egim20": e50 / e50.shift(20) - 1,
        "c_ema20": C / e20 - 1, "c_ema50": C / e50 - 1, "c_sma200": C / s200 - 1,
        "r5": C / C.shift(5) - 1, "r20": C / C.shift(20) - 1, "r60": C / C.shift(60) - 1, "r120": C / C.shift(120) - 1, "r250": C / C.shift(250) - 1,
        "dd250": C / maxH250 - 1, "konum250": (C - minL250) / (maxH250 - minL250 + eps),
        "dip_bar250": pd.Series(_cy_kayan_argmin(L_.to_numpy(float), 251), index=d.index),
        "log_dv20": np.log10(dv20.clip(lower=1.0)), "vol60": g.rolling(60, min_periods=40).std(), "rsi14": 100 - 100 / (1 + yu / (du + eps)),
    }, index=d.index)
    Ls = Ls or tuple(sorted(set(K["izgara"]["L"]) | {K["col"]["L"]}))
    Kc = K["col"]; cl: Dict[int, pd.DataFrame] = {}
    bbq = bbw.rolling(250, min_periods=120).quantile(Kc["bb_yuzde"]); dj_pre250 = doji.rolling(250, min_periods=120).mean()
    for Lw in Ls:
        mH_pre = H.rolling(251 - Lw, min_periods=int(0.8 * (251 - Lw))).max().shift(Lw)
        lowW = L_.rolling(Lw).min(); medW = C.rolling(Lw).median()
        k = int(round((1 - Kc["son_pay"]) * Lw)); ref_pre = ref250.shift(Lw)
        low_ilk = L_.rolling(k).min().shift(Lw - k); low_son = L_.rolling(Lw - k).min()
        band = (C.rolling(Lw).quantile(0.9) - C.rolling(Lw).quantile(0.1)) / medW
        djW = doji.rolling(Lw).mean(); djp = dj_pre250.shift(Lw)
        cl[Lw] = pd.DataFrame({
            "dusus": lowW / mH_pre - 1, "konum": (medW - minL250) / (maxH250 - minL250 + eps),
            "savunma": low_son / low_ilk - 1 + 0.5 * ref_pre, "bant": band / ref_pre, "kucuk": ar.rolling(Lw).median() / ref_pre,
            "bb_ok": (bbw.rolling(Lw).min() <= bbq).astype(float), "doji_ok": ((djW >= Kc["doji_kat"] * djp) & (djW > 0)).astype(float),
            "hacim_ok": (V.rolling(Lw).median() <= Kc["hacim_kat"] * V.rolling(60).median().shift(Lw)).astype(float),
            "tavan": np.maximum(O, C).rolling(Lw).max(),
        }, index=d.index)
    return {"F": F, "col": cl, "kayma": (K["kayma_kat"] * ar.rolling(20, min_periods=10).median()).clip(K["kayma_min"], K["kayma_tavan"]),
            "dv20": dv20, "vol60": F.vol60}


def cy_cekirdek(c: pd.DataFrame, Lw: int, K: Dict[str, Any] = CY) -> pd.Series:
    """Sıkışma çekirdeği: dipte + savunma + dar bant (+ yeterli geçmiş)."""
    Kc = K["col"]
    ok = (c.konum <= Kc["konum"]) & (c.savunma >= 0) & (c.bant <= Kc["bant_kat"]) & c.dusus.notna() & c.kucuk.notna()
    ok.iloc[:250 + Lw] = False
    return ok


def cy_imza(c: pd.DataFrame, kucuk: float) -> pd.Series:
    return (c.kucuk <= kucuk).astype(int) + c.bb_ok.astype(int) + c.doji_ok.astype(int) + c.hacim_ok.astype(int)


def _cy_aralik(idx: np.ndarray, ayri: int) -> np.ndarray:
    """Sinyal indisleri: hissede 'ayri' işlem gününde tek (ilk gelen)."""
    out = []; son = -10 ** 9
    for i in idx:
        if i - son >= ayri:
            out.append(i); son = i
    return np.array(out, dtype=int)


def cy_sinyaller(d: pd.DataFrame, M: Dict[str, Any], uygun: np.ndarray, K: Dict[str, Any] = CY) -> Dict[str, np.ndarray]:
    """Izgara P1 yapıları + ana yapının P2 (kırılım) ve EŞ günleri (indis dizileri). uygun: likidite + evren maskesi."""
    Kc = K["col"]; out = {}; C = d.Close.to_numpy(float)
    for Lw in K["izgara"]["L"]:
        c = M["col"][Lw]; cek = cy_cekirdek(c, Lw, K).to_numpy() & uygun
        for du in K["izgara"]["dusus"]:
            m0 = cek & (c.dusus.to_numpy() <= du)
            for ku in K["izgara"]["kucuk"]:
                im = cy_imza(c, ku).to_numpy()
                for imn in K["izgara"]["imza_min"]:
                    out[f"P1|{du}|{Lw}|{ku}|{imn}"] = _cy_aralik(np.flatnonzero(m0 & (im >= imn)), Kc["ayri"])
    ana = f"P1|{Kc['dusus']}|{Kc['L']}|{Kc['kucuk']}|{Kc['imza_min']}"; out["P1"] = out[ana]
    c = M["col"][Kc["L"]]; cek = cy_cekirdek(c, Kc["L"], K).to_numpy() & uygun & (c.dusus.to_numpy() <= Kc["dusus"])
    out["ES"] = _cy_aralik(np.flatnonzero(cek & (cy_imza(c, Kc["kucuk"]).to_numpy() <= Kc["es_imza_max"])), Kc["ayri"])
    tav = c.tavan.to_numpy(); p2 = []
    for i0 in out["P1"]:
        for j in range(i0 + 1, min(i0 + Kc["kirilim_gun"], len(C) - 1) + 1):
            if C[j] > tav[i0] * Kc["kirilim_pay"]:
                if uygun[j]:
                    p2.append(j)
                break
    out["P2"] = _cy_aralik(np.array(sorted(set(p2)), dtype=int), Kc["ayri"])
    return out


# ---------------------------------------------------------------- Y3 ÜÇLÜ BARİYER + MALİYET
def cy_uclu_bariyer(d: pd.DataFrame, ust: float, alt: float, ufuk: int, batan: bool, K: Dict[str, Any] = CY) -> pd.DataFrame:
    """Her gün i için: giriş i+1 açılışı; önce +ust (High) -> y = 1, önce alt (Low) ya da vade -> y = 0. Boşlukta açılış fiyatı; aynı gün
    ikisi = zarar. Seri vadeden önce biterse (borsadan çıkış, batan): son kapanış, son 60 gün eksi ise ek delist_kayip.
    Seri kriz kesiğine kadar sürüyor ve vade dolmuyorsa NaN (ölçülmez). Dönüş: y, brut, cikis (indis), gun."""
    O = d.Open.to_numpy(float); H = d.High.to_numpy(float); L = d.Low.to_numpy(float); C = d.Close.to_numpy(float); n = len(C)
    y = np.full(n, np.nan); br = np.full(n, np.nan); ck = np.full(n, -1, dtype=np.int64)
    ii = np.arange(n - 1); o = O[ii + 1]; ok = o > 0; ii = ii[ok]; o = o[ok]
    yy = np.zeros(len(ii)); bb = np.full(len(ii), np.nan); cc = np.full(len(ii), -1, dtype=np.int64); bit = np.zeros(len(ii), bool)
    for t in range(ufuk):
        k = ii + 1 + t; var = k < n; kk = np.where(var, k, n - 1)
        Ok = O[kk]; gd = var & (t > 0) & (Ok <= o * (1 + alt)); gu = var & (t > 0) & (Ok >= o * (1 + ust))
        lh = var & (L[kk] <= o * (1 + alt)); hh = var & (H[kk] >= o * (1 + ust))
        for kos, deger, kaz in ((gd, Ok / o - 1, 0.0), (gu, Ok / o - 1, 1.0), (lh, np.full(len(ii), alt), 0.0), (hh, np.full(len(ii), ust), 1.0)):
            w = kos & ~bit; bb[w] = deger[w]; yy[w] = kaz; cc[w] = kk[w]; bit |= w
    son = ii + ufuk; tam = son < n
    w = ~bit & tam; bb[w] = C[son[w]] / o[w] - 1; cc[w] = son[w]
    gecerli = tam | bit if batan else tam                            # borsadan çıkan: vadeden önce değen bariyer de geçerli
    if batan:                                                        # vade dolmadan seri bitti: borsadan çıkış
        w = ~bit & ~tam
        r60 = C[-1] / C[max(0, n - 61)] - 1
        bb[w] = C[-1] / o[w] - 1; cc[w] = n - 1
        if r60 < 0:
            bb[w] = (1 + bb[w]) * (1 + K["delist_kayip"]) - 1
        gecerli = np.ones(len(ii), bool)
    tam = gecerli
    y[ii[tam]] = yy[tam]; br[ii[tam]] = bb[tam]; ck[ii[tam]] = cc[tam]
    gun = np.where(ck >= 0, ck - np.arange(n), -1)
    return pd.DataFrame({"y": y, "brut": br, "cikis": ck, "gun": gun}, index=d.index)


# ---------------------------------------------------------------- Y7a GÖRSEL (OHLC RESMİ)
def cy_resim(d: pd.DataFrame, i: int, K: Dict[str, Any] = CY, ma: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
    """Jiang-Kelly-Xiu tarzı i günü dahil son 'gun' bar: 3 piksel / gün (açılış sol, aralık orta, kapanış sağ), 20 gün ortalama çizgisi,
    altta hacim. Yalnız i ve öncesi. uint8 (yuk x 3*gun)."""
    Kc = K["cnn"]; G = Kc["gun"]; Y = Kc["yuk"]; P = Kc["fiyat_px"]
    if i + 1 < G:
        return None
    s = slice(i - G + 1, i + 1)
    O = d.Open.to_numpy(float)[s]; H = d.High.to_numpy(float)[s]; L = d.Low.to_numpy(float)[s]; C = d.Close.to_numpy(float)[s]
    V = d.Volume.to_numpy(float)[s]
    m = (ma if ma is not None else d.Close.rolling(20, min_periods=1).mean().to_numpy(float))[s]
    lo = np.nanmin(np.r_[L, m]); hi = np.nanmax(np.r_[H, m])
    if not (np.isfinite(lo) and np.isfinite(hi) and hi > lo):
        return None
    im = np.zeros((Y, 3 * G), dtype=np.uint8)
    sat = lambda p: (P - 1 - np.clip(np.round((p - lo) / (hi - lo) * (P - 1)), 0, P - 1)).astype(int)
    rO, rH, rL, rC, rM = sat(O), sat(H), sat(L), sat(C), sat(m)
    vm = np.nanmax(V); hv = Y - P - 1
    for t in range(G):
        x = 3 * t
        im[rH[t]:rL[t] + 1, x + 1] = 255; im[rO[t], x] = 255; im[rC[t], x + 2] = 255
        if t > 0:
            a, b = sorted((rM[t - 1], rM[t]))
            im[a:b + 1, x] = 255
        im[rM[t], x + 1] = 255
        if vm > 0 and np.isfinite(V[t]):
            hpx = int(round(V[t] / vm * hv))
            if hpx > 0:
                im[Y - hpx:Y, x + 1] = 255
    return im


# ---------------------------------------------------------------- HİSSE İŞLEME (Y2 + Y3 + Y5 + Y7a birlikte; paralel)
def cy_hisse_isle(arg: Tuple[str, str, pd.DataFrame, Dict[str, Any], pd.Series, Dict[str, Any], bool, int]) -> Optional[Dict[str, Any]]:
    """Bir hisse: ölçüler, sinyaller, etiketler, panel satırları, özellik satırları, resimler (yalnız gereken satırlar)."""
    pz, s, d, ev, likesik, K, resim_ok, tohum = arg
    try:
        M = cy_olculer(d, K); n = len(d); idx = d.index
        min_dv = K["likit"].get(pz)
        uygun = (M["dv20"] >= likesik.reindex(idx).ffill().to_numpy()).to_numpy() & (d.Close.to_numpy() >= K["fiyat_min"].get(pz, 0.0))
        if min_dv:
            uygun &= (M["dv20"] >= min_dv).to_numpy()
        uygun &= (idx >= pd.Timestamp(ev["evren_bas"])) & (idx >= pd.Timestamp(K["egitim"][0]))
        uygun &= np.arange(n) >= 260
        S = cy_sinyaller(d, M, uygun, K)
        cikti_mi = bool(d.index[-1] < pd.Timestamp(K["alive_sinir"]))  # seri kriz kesiğinden önce bitiyor: borsadan çıkış (kaynak ne olursa)
        T = cy_uclu_bariyer(d, K["tb"]["ust"], K["tb"]["alt"], K["tb"]["ufuk"], cikti_mi, K)
        Tk = cy_uclu_bariyer(d, K["tb_kisa"]["ust"], K["tb_kisa"]["alt"], K["tb_kisa"]["ufuk"], cikti_mi, K)
        mal = 2 * (K["komisyon"][pz] + M["kayma"].to_numpy())
        net = T.brut.to_numpy() - mal; netk = Tk.brut.to_numpy() - mal
        pm = uygun & np.isfinite(T.y.to_numpy())
        pan = pd.DataFrame({"tarih": idx[pm], "i": np.flatnonzero(pm).astype(np.int32), "y": T.y.to_numpy()[pm].astype(np.float32),
                            "net": net[pm].astype(np.float32), "brut": T.brut.to_numpy()[pm].astype(np.float32),
                            "cikis": T.cikis.to_numpy()[pm].astype(np.int32), "yk": Tk.y.to_numpy()[pm].astype(np.float32),
                            "netk": netk[pm].astype(np.float32), "vol60": M["vol60"].to_numpy()[pm].astype(np.float32),
                            "r20": M["F"].r20.to_numpy()[pm].astype(np.float32), "r60": M["F"].r60.to_numpy()[pm].astype(np.float32)})
        olay = []
        for tip, ix in S.items():
            ix = ix[np.isfinite(T.y.to_numpy()[ix])] if len(ix) else ix
            if len(ix):
                olay.append(pd.DataFrame({"tip": tip, "i": ix.astype(np.int32)}))
        O = pd.concat(olay, ignore_index=True) if olay else pd.DataFrame(columns=["tip", "i"])
        # özellik / resim satırları: ana P1, P2, ES + havuz örneklemi (rastgele, tohum hisseye bağlı)
        rng = np.random.default_rng(tohum); hv = []
        for ad, (a, b) in (("egitim", K["egitim"]), ("dogrulama", K["dogrulama"]), ("test", (K["test"][0][1], K["test"][-1][2]))):
            m = pm & (idx >= pd.Timestamp(a)) & (idx <= pd.Timestamp(b))
            cand = np.flatnonzero(m); p = K["_havuz_p"][pz].get(ad, 0.0)
            if len(cand) and p > 0:
                sec = cand[rng.random(len(cand)) < p]
                hv.append(pd.DataFrame({"tip": f"HAVUZ_{ad}", "i": sec.astype(np.int32)}))
        H_ = pd.concat(hv, ignore_index=True) if hv else pd.DataFrame(columns=["tip", "i"])
        satir = pd.concat([O[O.tip.isin(["P1", "P2", "ES"])], H_], ignore_index=True)
        ii = np.unique(satir.i.to_numpy().astype(int)) if len(satir) else np.array([], dtype=int)
        Kc = K["col"]; c = M["col"][Kc["L"]]
        Fi = M["F"].iloc[ii].copy()
        for k2 in ("dusus", "konum", "savunma", "bant", "kucuk", "bb_ok", "doji_ok", "hacim_ok"):
            Fi["col_" + k2] = c[k2].to_numpy()[ii]
        Fi["col_imza"] = cy_imza(c, Kc["kucuk"]).to_numpy()[ii]
        Fi["i"] = ii; Fi = Fi.astype(np.float32); Fi["i"] = ii
        R = None
        if resim_ok and len(ii):
            ma = d.Close.rolling(20, min_periods=1).mean().to_numpy(float)
            R = np.zeros((len(ii), K["cnn"]["yuk"], 3 * K["cnn"]["gun"]), dtype=np.uint8); okr = np.zeros(len(ii), bool)
            for j, i in enumerate(ii):
                im = cy_resim(d, int(i), K, ma)
                if im is not None:
                    R[j] = im; okr[j] = True
            Fi["resim_ok"] = okr
        return {"pazar": pz, "sembol": s, "cikti_mi": cikti_mi, "panel": pan, "olay": O, "satir": satir, "F": Fi, "R": R,
                "tarih": idx.to_numpy(), "kapanis": d.Close.to_numpy(np.float32), "acilis": d.Open.to_numpy(np.float32),
                "kayma": M["kayma"].to_numpy(np.float32), "T": T[["brut", "cikis"]].to_numpy(np.float64)}
    except Exception as ex:
        cylog.warning("CY %s %s atlandı: %s", pz, s, ex)
        return None


# ---------------------------------------------------------------- Y4 TABAN / EŞ + İSTATİSTİK
def cy_panel_taban(P: pd.DataFrame) -> pd.DataFrame:
    """Aynı gün, aynı oynaklık ondalığı ortalamaları: e_y, e_net, e_yk, e_netk."""
    P = P.copy(); P["vd"] = np.minimum((P.groupby("tarih").vol60.rank(pct=True) * 10).fillna(5).astype(int), 9).astype(np.int8)
    for c in ("y", "net", "yk", "netk"):
        P["e_" + c] = P.groupby(["tarih", "vd"])[c].transform("mean").astype(np.float32)
    return P


def cy_boot_fark(D: pd.DataFrame, kol: str, B: int, rng: np.random.Generator) -> Tuple[float, float, float]:
    """Ortalama ve ay kümeli bootstrap %95 aralığı (D: 'tarih' ve kol)."""
    v = D[kol].to_numpy(float); ok = np.isfinite(v); v = v[ok]
    if not len(v):
        return np.nan, np.nan, np.nan
    ay = (D.tarih.dt.year * 12 + D.tarih.dt.month).to_numpy()[ok]; ua, inv = np.unique(ay, return_inverse=True)
    sv = np.bincount(inv, v); sn = np.bincount(inv).astype(float); Mn = len(ua)
    if Mn < 3:
        return float(v.mean()), np.nan, np.nan
    ix = rng.integers(0, Mn, (B, Mn)); bs = sv[ix].sum(1) / sn[ix].sum(1)
    return float(v.mean()), float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))


def cy_boot_iki(A_: pd.DataFrame, B_: pd.DataFrame, kol: str, B: int, rng: np.random.Generator) -> Tuple[float, float, float]:
    """İki grup ortalama farkı (A - B), ayları birlikte yeniden örnekleyerek %95 aralık."""
    def ayla(D):
        ay = (D.tarih.dt.year * 12 + D.tarih.dt.month).to_numpy(); v = D[kol].to_numpy(float); ok = np.isfinite(v)
        return pd.DataFrame({"ay": ay[ok], "v": v[ok]}).groupby("ay").v.agg(["sum", "count"])
    a = ayla(A_); b = ayla(B_)
    if not len(a) or not len(b):
        return np.nan, np.nan, np.nan
    ay = np.array(sorted(set(a.index) | set(b.index))); a = a.reindex(ay, fill_value=0); b = b.reindex(ay, fill_value=0)
    fark = a["sum"].sum() / max(a["count"].sum(), 1) - b["sum"].sum() / max(b["count"].sum(), 1)
    ix = rng.integers(0, len(ay), (B, len(ay)))
    fa = a["sum"].to_numpy()[ix].sum(1) / np.maximum(a["count"].to_numpy()[ix].sum(1), 1)
    fb = b["sum"].to_numpy()[ix].sum(1) / np.maximum(b["count"].to_numpy()[ix].sum(1), 1)
    return float(fark), float(np.quantile(fa - fb, 0.025)), float(np.quantile(fa - fb, 0.975))


def cy_auc_boot(y: np.ndarray, p: np.ndarray, tarih: pd.Series, B: int, rng: np.random.Generator) -> Tuple[float, float, float]:
    """AUC ve ay kümeli bootstrap aralığı."""
    from sklearn.metrics import roc_auc_score
    ok = np.isfinite(y) & np.isfinite(p); y = y[ok]; p = p[ok]; ay = (tarih.dt.year * 12 + tarih.dt.month).to_numpy()[ok]
    if len(np.unique(y)) < 2:
        return np.nan, np.nan, np.nan
    a0 = float(roc_auc_score(y, p)); ua = np.unique(ay); gr = {u: np.flatnonzero(ay == u) for u in ua}; bs = []
    for _ in range(min(B, 500)):
        ix = np.concatenate([gr[u] for u in rng.choice(ua, len(ua))])
        if len(np.unique(y[ix])) == 2:
            bs.append(roc_auc_score(y[ix], p[ix]))
    return a0, float(np.quantile(bs, 0.025)) if bs else np.nan, float(np.quantile(bs, 0.975)) if bs else np.nan


def cy_ozet(D: pd.DataFrame, K: Dict[str, Any], rng: np.random.Generator, kisa: bool = False) -> Dict[str, Any]:
    """Olay kümesi özeti: n, isabet, taban, fark (+aralık), net getiri, kazanma, ort kazanç / kayıp."""
    y, net, ey, en = ("yk", "netk", "e_yk", "e_netk") if kisa else ("y", "net", "e_y", "e_net")
    if not len(D):
        return {"n": 0}
    X = D.assign(_f=D[y] - D[ey], _fn=D[net] - D[en]); f, a, b = cy_boot_fark(X, "_f", K["karar"]["boot"], rng)
    fn, an, bn = cy_boot_fark(X, "_fn", K["karar"]["boot"], rng); r = D[net].to_numpy(float)
    return {"n": int(len(D)), "isabet": float(D[y].mean()), "taban": float(D[ey].mean()), "fark": f, "fark_alt": a, "fark_ust": b,
            "net": float(np.nanmean(r)), "net_taban": float(D[en].mean()), "net_fark": fn, "net_fark_alt": an,
            "kazanma": float(np.mean(r > 0)), "ort_kazanc": float(np.mean(r[r > 0])) if (r > 0).any() else np.nan,
            "ort_kayip": float(np.mean(r[r <= 0])) if (r <= 0).any() else np.nan, "en_kotu": float(np.nanmin(r)),
            "medyan_gun": float(D.gun.median()) if "gun" in D else np.nan}


def cy_tutar(o: Dict[str, Any], K: Dict[str, Any]) -> bool:
    return bool(o.get("n", 0) >= K["karar"]["n_min"] and (o.get("fark") or -1) >= K["karar"]["fark"] and (o.get("fark_alt") or -1) > 0
                and (o.get("net_fark") or -1) > 0)


# ---------------------------------------------------------------- Y6 META-ETİKETLEME
def cy_ozellik_adlari(F: pd.DataFrame) -> List[str]:
    return [c for c in F.columns if c not in ("i", "resim_ok", "pazar", "sembol", "tarih", "tip", "y", "net", "brut", "cikis", "gun", "yk",
                                                  "netk", "vd", "e_y", "e_net", "e_yk", "e_netk", "yil", "uid", "agirlik", "batan", "kaynak")]


def cy_meta(E: pd.DataFrame, ozl: List[str], K: Dict[str, Any], rng: np.random.Generator) -> Tuple[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]:
    """Yıl yıl ileri yürüyen meta model (P1 adayları, ABD). Doğrulamada s* ve p* seçilir; testte sabit. Dönüş: (E + 'meta_p'), seçim, kayıt."""
    import lightgbm as lgb
    E = E.copy(); E["meta_p"] = np.nan; kayit = []; modeller = {}
    yillar = sorted(set(E.tarih.dt.year) & set(range(int(K["dogrulama"][0][:4]), 2027)))
    for Y in yillar:
        sinir = pd.Timestamp(f"{Y}-01-01") - pd.Timedelta(days=K["embargo_gun"])
        tr = E[(E.cikis_tarih < sinir) & E.y.notna()]
        if len(tr) < K["meta"]["n_min_egitim"] or tr.y.nunique() < 2:
            continue
        m = lgb.LGBMClassifier(**K["meta"]["lgbm"], random_state=K["karar"]["tohum"]); m.fit(tr[ozl], tr.y.astype(int))
        te = E.tarih.dt.year == Y; E.loc[te, "meta_p"] = m.predict_proba(E.loc[te, ozl])[:, 1]; modeller[Y] = m
        kayit.append({"yil": Y, "egitim_n": len(tr), "egitim_isabet": float(tr.y.mean()), "test_n": int(te.sum())})
    dg = E[(E.tarih >= K["dogrulama"][0]) & (E.tarih <= K["dogrulama"][1]) & E.meta_p.notna()]
    sec = {"pay": np.nan, "p": np.nan}; izg = []
    for pay in K["meta"]["pay"]:
        p = float(dg.meta_p.quantile(1 - pay)) if len(dg) else np.nan; S = dg[dg.meta_p >= p]
        izg.append({"model": "meta", "pay": pay, "p": p, "dogrulama_n": len(S), "dogrulama_net": float(S.net.mean()) if len(S) else np.nan,
                    "dogrulama_isabet": float(S.y.mean()) if len(S) else np.nan})
    gec = [r for r in izg if r["dogrulama_n"] >= K["karar"]["n_min"] and np.isfinite(r["dogrulama_net"])]
    if gec:
        b = max(gec, key=lambda r: r["dogrulama_net"]); sec = {"pay": b["pay"], "p": b["p"]}
    return E, {**sec, "modeller": modeller, "yillik": kayit}, izg


def cy_esik_sec(dg: pd.DataFrame, kol: str, K: Dict[str, Any], ad: str) -> Tuple[Dict[str, float], List[Dict[str, Any]]]:
    """Genel model / CNN için s* ve p* (doğrulama P1 adayları, en yüksek ortalama net)."""
    izg = []
    for pay in K["meta"]["pay"]:
        p = float(dg[kol].quantile(1 - pay)) if len(dg) else np.nan; S = dg[dg[kol] >= p]
        izg.append({"model": ad, "pay": pay, "p": p, "dogrulama_n": len(S), "dogrulama_net": float(S.net.mean()) if len(S) else np.nan,
                    "dogrulama_isabet": float(S.y.mean()) if len(S) else np.nan})
    gec = [r for r in izg if r["dogrulama_n"] >= K["karar"]["n_min"] and np.isfinite(r["dogrulama_net"])]
    b = max(gec, key=lambda r: r["dogrulama_net"]) if gec else {"pay": np.nan, "p": np.nan}
    return {"pay": b["pay"], "p": b["p"]}, izg


# ---------------------------------------------------------------- Y7b CNN
def cy_cnn_egit(Xtr: np.ndarray, ytr: np.ndarray, Xdg: np.ndarray, ydg: np.ndarray, K: Dict[str, Any]) -> Tuple[Any, List[Dict[str, Any]]]:
    """Küçük JKX tarzı CNN; erken durma doğrulama kaybıyla. Dönüş (model, epoch kayıtları)."""
    import torch
    import torch.nn as nn
    Kc = K["cnn"]; torch.manual_seed(Kc["tohum"]); np.random.seed(Kc["tohum"])
    torch.set_num_threads(max(1, os.cpu_count() or 1)); cihaz = "cuda" if torch.cuda.is_available() else "cpu"
    k1, k2, k3 = Kc["kanal"]

    def blok(a, b):
        return nn.Sequential(nn.Conv2d(a, b, (5, 3), padding=(2, 1)), nn.BatchNorm2d(b), nn.LeakyReLU(0.01), nn.MaxPool2d((2, 2)))
    h, w = Kc["yuk"] // 8, (3 * Kc["gun"]) // 8
    net = nn.Sequential(blok(1, k1), blok(k1, k2), blok(k2, k3), nn.Flatten(), nn.Dropout(0.5), nn.Linear(k3 * h * w, 1)).to(cihaz)
    opt = torch.optim.Adam(net.parameters(), lr=Kc["lr"]); kf = nn.BCEWithLogitsLoss(); kayit = []; en_iyi = (np.inf, None); sabir = 0

    def tahmin_kayip(X, y):
        net.eval(); out = []
        with torch.no_grad():
            for a in range(0, len(X), 2048):
                xb = torch.from_numpy(X[a:a + 2048]).float().div_(255.0).unsqueeze(1).to(cihaz); out.append(net(xb).squeeze(1).cpu())
        lo = torch.cat(out); return float(kf(lo, torch.from_numpy(y).float())), torch.sigmoid(lo).numpy()
    for ep in range(Kc["epoch"]):
        net.train(); sira = np.random.permutation(len(Xtr)); t0 = time.time(); top = 0.0
        for a in range(0, len(sira), Kc["batch"]):
            b = sira[a:a + Kc["batch"]]
            xb = torch.from_numpy(Xtr[b]).float().div_(255.0).unsqueeze(1).to(cihaz); yb = torch.from_numpy(ytr[b]).float().to(cihaz)
            opt.zero_grad(); ls = kf(net(xb).squeeze(1), yb); ls.backward(); opt.step(); top += float(ls) * len(b)
        dk, _ = tahmin_kayip(Xdg, ydg); kayit.append({"epoch": ep + 1, "egitim_kayip": top / len(sira), "dogrulama_kayip": dk, "sure_sn": round(time.time() - t0)})
        cylog.info("CNN epoch %d: eğitim %.4f doğrulama %.4f (%ds)", ep + 1, top / len(sira), dk, time.time() - t0)
        if dk < en_iyi[0] - 1e-4:
            en_iyi = (dk, {k: v.detach().clone() for k, v in net.state_dict().items()}); sabir = 0
        else:
            sabir += 1
            if sabir > Kc["sabir"]:
                break
    if en_iyi[1] is not None:
        net.load_state_dict(en_iyi[1])
    net._cy_tahmin = lambda X: tahmin_kayip(X, np.zeros(len(X), np.float32))[1]   # type: ignore[attr-defined]
    return net, kayit


# ---------------------------------------------------------------- Y8 IZGARA + PBO + DSR
def cy_pbo(M: np.ndarray, S: int = 16) -> Dict[str, float]:
    """CSCV (Bailey ve ark.): M = T x N (dönem x yapı) getiri matrisi. IS'te en iyi Sharpe'lı yapının OOS göreli sırası; PBO = logit <= 0 payı."""
    T, N = M.shape
    if N < 2 or T < S:
        return {"pbo": np.nan, "kombinasyon": 0}
    bl = np.array_split(np.arange(T), S); lam = []
    for ic in combinations(range(S), S // 2):
        IS = np.concatenate([bl[k] for k in ic]); OS = np.concatenate([bl[k] for k in range(S) if k not in ic])
        sh = lambda X: X.mean(0) / (X.std(0, ddof=1) + 1e-12)
        si, so = sh(M[IS]), sh(M[OS]); n_ = int(np.argmax(si)); w = (np.sum(so < so[n_]) + 1) / (N + 1)
        lam.append(np.log(w / (1 - w)))
    lam = np.array(lam)
    return {"pbo": float(np.mean(lam <= 0)), "kombinasyon": len(lam), "logit_medyan": float(np.median(lam))}


def cy_dsr(r: np.ndarray, sr_denemeler: np.ndarray) -> Dict[str, float]:
    """Deflated Sharpe (Bailey-López de Prado 2014): seçilen serinin (r, dönem getirileri) SR'si, N denemenin SR varyansıyla düzeltilir."""
    from scipy.stats import norm, skew, kurtosis
    r = r[np.isfinite(r)]; T = len(r); N = int(np.isfinite(sr_denemeler).sum())
    if T < 10 or N < 2:
        return {"dsr": np.nan}
    sr = r.mean() / (r.std(ddof=1) + 1e-12); v = float(np.nanvar(sr_denemeler, ddof=1)); g = 0.5772156649
    sr0 = math.sqrt(max(v, 1e-12)) * ((1 - g) * norm.ppf(1 - 1 / N) + g * norm.ppf(1 - 1 / (N * math.e)))
    sk = float(skew(r)); ku = float(kurtosis(r, fisher=False))
    z = (sr - sr0) * math.sqrt(T - 1) / math.sqrt(max(1 - sk * sr + (ku - 1) / 4 * sr ** 2, 1e-12))
    return {"dsr": float(norm.cdf(z)), "sr": float(sr), "sr0": float(sr0), "T": T, "N": N}


# ---------------------------------------------------------------- Y9 PORTFÖY
def cy_portfoy(H: Dict[str, Dict[str, Any]], gir: List[Tuple[pd.Timestamp, str, int]], bas: str, bit: str, pz: str, K: Dict[str, Any],
               rastgele: Optional[Tuple[np.random.Generator, Dict[pd.Timestamp, List[Tuple[str, int]]]]] = None,
               takvim: Optional[pd.DatetimeIndex] = None) -> Dict[str, Any]:
    """10 yuva, günde en çok 2 yeni; giriş sinyal ertesi açılış, çıkış üçlü bariyer (cikis indisi; brüt getiri, batanda delist kaybı dahil),
    maliyet giriş ve çıkışta yarı yarıya. H: sembol -> {'tarih','kapanis','acilis','kayma','T'}. gir: (sinyal günü, sembol, i)."""
    Kp = K["portfoy"]; gun = takvim[(takvim >= pd.Timestamp(bas)) & (takvim <= pd.Timestamp(bit))]
    gs: Dict[pd.Timestamp, List[Tuple[str, int]]] = {}
    for t, s, i in gir:
        h = H[s]; j = i + 1
        if j < len(h["tarih"]):
            gs.setdefault(pd.Timestamp(h["tarih"][j]), []).append((s, i))
    deger = np.zeros(len(gun)); nakit = 1.0; acik: List[Dict[str, Any]] = []; islem = []; onceki = 1.0
    for g_i, t in enumerate(gun):
        if rastgele is not None:
            rng, hav = rastgele; c = hav.get(t, [])
            aday = [c[k] for k in rng.permutation(len(c))[:Kp["gunluk_azami"] * 3]] if c else []
        else:
            aday = gs.get(t, [])
        yeni = 0
        for s, i in aday:
            if len(acik) >= Kp["slot"] or yeni >= Kp["gunluk_azami"] or any(p["s"] == s for p in acik):
                continue
            h = H[s]; j = i + 1; br, ck = h["T"][i]
            if not np.isfinite(br) or ck < j:
                continue
            mal = K["komisyon"][pz] + float(h["kayma"][i]); tutar = min(onceki / Kp["slot"], nakit / (1 + mal))
            if tutar <= 0:
                continue
            nakit -= tutar * (1 + mal); o = float(h["acilis"][j])
            acik.append({"s": s, "tutar": tutar, "o": o, "ck_t": pd.Timestamp(h["tarih"][int(ck)]), "br": br, "mal": mal, "h": h}); yeni += 1
        top = nakit
        for p in list(acik):
            if t >= p["ck_t"]:
                v = p["tutar"] * (1 + p["br"]) * (1 - p["mal"]); nakit += v; top += v
                islem.append((1 + p["br"]) * (1 - p["mal"]) / (1 + p["mal"]) - 1); acik.remove(p)
            else:
                h = p["h"]; k = int(np.searchsorted(h["tarih"], np.datetime64(t), side="right")) - 1
                top += p["tutar"] * float(h["kapanis"][max(k, 0)]) / p["o"]
        deger[g_i] = top; onceki = top
    for p in acik:
        islem.append((1 + p["br"]) * (1 - p["mal"]) / (1 + p["mal"]) - 1)
    D = pd.Series(deger, index=gun); r = np.array(islem)
    yil = max((gun[-1] - gun[0]).days / 365.25, 1e-9) if len(gun) > 1 else np.nan
    mdd = float((D / D.cummax() - 1).min()) if len(D) else np.nan
    return {"toplam": float(D.iloc[-1] - 1) if len(D) else np.nan, "yillik": float(D.iloc[-1] ** (1 / yil) - 1) if len(D) and yil else np.nan,
            "mdd": mdd, "islem_n": int(len(r)), "kazanma": float(np.mean(r > 0)) if len(r) else np.nan,
            "ort_islem": float(r.mean()) if len(r) else np.nan, "ort_kazanc": float(r[r > 0].mean()) if (r > 0).any() else np.nan,
            "ort_kayip": float(r[r <= 0].mean()) if (r <= 0).any() else np.nan, "deger": D}


def cy_piyasa(H: Dict[str, Dict[str, Any]], P: pd.DataFrame, bas: str, bit: str) -> Dict[str, Any]:
    """Eşit ağırlıklı likit piyasa (her gün o gün likit hisselerin günlük getirisi ortalaması)."""
    parca = []
    for s, g in P[(P.tarih >= bas) & (P.tarih <= bit)].groupby("sembol"):
        h = H[s]; c = pd.Series(h["kapanis"].astype(float), index=pd.DatetimeIndex(h["tarih"])); r = c.pct_change()
        parca.append(r.reindex(pd.DatetimeIndex(g.tarih)).rename(s))
    if not parca:
        return {"toplam": np.nan, "mdd": np.nan}
    R = pd.concat(parca, axis=1).clip(-0.9, 3.0).mean(axis=1).fillna(0); D = (1 + R).cumprod()
    yil = max((D.index[-1] - D.index[0]).days / 365.25, 1e-9)
    return {"toplam": float(D.iloc[-1] - 1), "yillik": float(D.iloc[-1] ** (1 / yil) - 1), "mdd": float((D / D.cummax() - 1).min()), "deger": D}


# ---------------------------------------------------------------- SÜRÜCÜ
def cy_calistir(A: Optional[CYAyar] = None, K: Dict[str, Any] = CY) -> Dict[str, Any]:
    """Uçtan uca: veri -> hisse işleme -> taban -> hipotezler -> meta -> CNN -> ızgara/PBO -> portföy -> rapor."""
    A = A or CYAyar(); os.makedirs(A.cikti, exist_ok=True); t_bas = time.time()
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    cy_veri_hazirla(A); Vs, EV = cy_veri_yukle(A, K)
    if "ABD" not in Vs:
        raise RuntimeError("ABD verisi yok")
    EV.to_csv(os.path.join(A.cikti, "cy_evren.csv"), index=False)
    rng = np.random.default_rng(K["karar"]["tohum"])
    # havuz örnekleme olasılıkları (ABD; resim ve genel model için)
    K = {**K, "_havuz_p": {}}
    for pz, V in Vs.items():
        if pz != "ABD":
            K["_havuz_p"][pz] = {}; continue
        say = {}
        for ad, (a, b) in (("egitim", K["egitim"]), ("dogrulama", K["dogrulama"]), ("test", (K["test"][0][1], K["test"][-1][2]))):
            say[ad] = sum(int(((d.index >= a) & (d.index <= b)).sum()) for d in V.values())
        K["_havuz_p"][pz] = {ad: min(1.0, 2.0 * K["havuz"][ad] / max(say[ad], 1)) for ad in say}   # likidite süzgecinden önce: ~2 kat pay
    SON: Dict[str, Dict[str, Any]] = {}
    for pz, V in Vs.items():
        t0 = time.time(); le = cy_likit_esik(V, pz, K); evp = EV[EV.pazar == pz].set_index("sembol")
        args = [(pz, s, d, evp.loc[s].to_dict(), le, K, A.cnn and pz in ("ABD", "AVR", "BIST"), zlib.crc32(f"{pz}|{s}".encode())) for s, d in V.items() if s in evp.index]
        sonuc = []
        if A.is_parcacigi > 1:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(A.is_parcacigi) as havuz:
                for r in havuz.imap_unordered(cy_hisse_isle, args, chunksize=8):
                    if r is not None:
                        sonuc.append(r)
        else:
            sonuc = [r for r in map(cy_hisse_isle, args) if r is not None]
        cylog.info("%s: %d hisse işlendi (%ds)", pz, len(sonuc), time.time() - t0)
        SON[pz] = cy_birlestir(sonuc, EV[EV.pazar == pz], pz, K)
    K = {**K, "_endeks": cy_endeks(A, K)}
    R = cy_analiz(SON, A, K, rng)
    R["sure_dk"] = round((time.time() - t_bas) / 60, 1)
    cy_rapor(R, A, K)
    return R


def cy_birlestir(sonuc: List[Dict[str, Any]], EV: pd.DataFrame, pz: str, K: Dict[str, Any]) -> Dict[str, Any]:
    """Hisse çıktılarını pazar tablolarına çevirir: panel (+taban), olaylar, özellik satırları, resimler, fiyat sözlüğü."""
    H = {r["sembol"]: {"tarih": r["tarih"], "kapanis": r["kapanis"], "acilis": r["acilis"], "kayma": r["kayma"], "T": r["T"]} for r in sonuc}
    P = pd.concat([r["panel"].assign(sembol=r["sembol"]) for r in sonuc if len(r["panel"])], ignore_index=True)
    P["tarih"] = pd.to_datetime(P.tarih); P = cy_panel_taban(P)
    piy = P.groupby("tarih").agg(piy_r20=("r20", "median"), piy_r60=("r60", "median"))
    ev = EV.set_index("sembol")
    olay = []
    for r in sonuc:
        if len(r["olay"]):
            o = r["olay"].copy(); o["sembol"] = r["sembol"]; olay.append(o)
    E = pd.concat(olay, ignore_index=True) if olay else pd.DataFrame(columns=["tip", "i", "sembol"])
    E["i"] = E.i.astype(int)
    E = E.merge(P[["sembol", "i", "tarih", "y", "net", "brut", "cikis", "yk", "netk", "vol60", "vd", "e_y", "e_net", "e_yk", "e_netk"]], on=["sembol", "i"], how="inner")
    E["gun"] = E.cikis - E.i
    E["cikis_tarih"] = [pd.Timestamp(H[s]["tarih"][min(int(c), len(H[s]["tarih"]) - 1)]) for s, c in zip(E.sembol, E.cikis)]
    E["batan"] = E.sembol.map(ev.batan).fillna(False).astype(bool); E["agirlik"] = E.sembol.map(ev.agirlik).fillna(1.0)
    F = pd.concat([r["F"].assign(sembol=r["sembol"]) for r in sonuc if len(r["F"])], ignore_index=True)
    F["i"] = F.i.astype(int)
    Rm, Rk = [], []
    for r in sonuc:
        if r["R"] is not None and len(r["F"]):
            Rm.append(r["R"]); Rk.append(pd.DataFrame({"sembol": r["sembol"], "i": r["F"].i.astype(int).to_numpy()}))
    resim = np.concatenate(Rm) if Rm else None; rk = pd.concat(Rk, ignore_index=True) if Rk else None
    if rk is not None:
        rk["r_ix"] = np.arange(len(rk))
        F = F.merge(rk, on=["sembol", "i"], how="left")
    S = pd.concat([r["satir"].assign(sembol=r["sembol"]) for r in sonuc if len(r["satir"])], ignore_index=True)
    S["i"] = S.i.astype(int)
    X = S.merge(F, on=["sembol", "i"], how="inner").merge(
        P[["sembol", "i", "tarih", "y", "net", "brut", "cikis", "yk", "netk", "vd", "e_y", "e_net", "e_yk", "e_netk"]], on=["sembol", "i"], how="inner")
    X = X.merge(piy, left_on="tarih", right_index=True, how="left")
    X["cikis_tarih"] = [pd.Timestamp(H[s]["tarih"][min(int(c), len(H[s]["tarih"]) - 1)]) for s, c in zip(X.sembol, X.cikis)]
    X["gun"] = X.cikis - X.i; X["batan"] = X.sembol.map(ev.batan).fillna(False).astype(bool)
    return {"H": H, "P": P, "E": E, "X": X, "resim": resim, "pazar": pz}


def _cy_donem(D: pd.DataFrame, a: str, b: str) -> pd.DataFrame:
    return D[(D.tarih >= pd.Timestamp(a)) & (D.tarih <= pd.Timestamp(b))]


def cy_analiz(SON: Dict[str, Dict[str, Any]], A: CYAyar, K: Dict[str, Any], rng: np.random.Generator) -> Dict[str, Any]:
    """Hipotezler H1-H10, meta, CNN, ızgara, portföy. Bütün tablolar A.cikti'ye yazılır."""
    R: Dict[str, Any] = {"hucre": [], "izgara": [], "secim": [], "portfoy": [], "cnn_kayit": [], "notlar": [], "veri": {}}
    donemler = [("egitim", *K["egitim"]), ("dogrulama", *K["dogrulama"])] + [(a, b, c) for a, b, c in K["test"]]
    for pz, S in SON.items():
        E = S["E"]; P = S["P"]
        R["veri"][pz] = {"hisse": int(P.sembol.nunique()), "panel_satir": int(len(P)), "ilk": str(P.tarih.min().date()), "son": str(P.tarih.max().date()),
                         "batan_hisse": int(E[E.batan].sembol.nunique()) if len(E) else 0}
        for tip in ("P1", "P2", "ES"):
            for dn, a, b in donemler:
                D = _cy_donem(E[E.tip == tip], a, b)
                for kisa in (False, True):
                    R["hucre"].append({"pazar": pz, "kume": tip, "donem": dn, "etiket": "kisa_8_8_20" if kisa else "ana_20_10_60", **cy_ozet(D, K, rng, kisa)})
                if pz == "ABD":
                    Dg = D[~D.batan]
                    R["hucre"].append({"pazar": pz, "kume": tip + "_batansiz", "donem": dn, "etiket": "ana_20_10_60", **cy_ozet(Dg, K, rng)})
        # H2: P1 - ES
        for dn, a, b in donemler:
            p1 = _cy_donem(E[E.tip == "P1"], a, b).assign(_f=lambda x: x.y - x.e_y); es = _cy_donem(E[E.tip == "ES"], a, b).assign(_f=lambda x: x.y - x.e_y)
            f, lo, hi = cy_boot_iki(p1, es, "_f", K["karar"]["boot"], rng)
            R["hucre"].append({"pazar": pz, "kume": "P1-ES", "donem": dn, "etiket": "ana_20_10_60", "n": len(p1), "n_es": len(es), "fark": f, "fark_alt": lo, "fark_ust": hi})
    Hc = pd.DataFrame(R["hucre"])
    # Y8 ızgara (ABD) + PBO + DSR
    E = SON["ABD"]["E"]; aylar = pd.period_range(K["egitim"][0], K["dogrulama"][1], freq="M"); Mx = {}
    for tip, g in E[E.tip.str.startswith("P1|")].groupby("tip"):
        satir = {"yapi": tip}
        for dn, a, b in donemler:
            o = cy_ozet(_cy_donem(g, a, b), K, rng); satir.update({f"{dn}_{k}": o.get(k) for k in ("n", "isabet", "fark", "fark_alt", "net", "net_fark")})
        R["izgara"].append(satir)
        gg = _cy_donem(g, K["egitim"][0], K["dogrulama"][1]); m = gg.groupby(gg.tarih.dt.to_period("M")).net.mean()
        Mx[tip] = m.reindex(aylar).fillna(0.0).to_numpy()
    Iz = pd.DataFrame(R["izgara"]); Mm = np.column_stack([Mx[k] for k in Iz.yapi]) if len(Iz) else np.zeros((0, 0))
    pbo = cy_pbo(Mm, K["pbo_blok"]) if Mm.size else {"pbo": np.nan}
    gec = Iz[(Iz["dogrulama_n"].fillna(0) >= 50)]
    secilen = gec.sort_values("dogrulama_net", ascending=False).yapi.iloc[0] if len(gec) else None
    sr_all = Mm.mean(0) / (Mm.std(0, ddof=1) + 1e-12) if Mm.size else np.array([])
    dsr = cy_dsr(Mx[secilen], sr_all) if secilen else {"dsr": np.nan}
    R["pbo"] = {**pbo, **{f"dsr_{k}": v for k, v in dsr.items()}, "secilen_yapi": secilen,
                "ana_yapi": f"P1|{K['col']['dusus']}|{K['col']['L']}|{K['col']['kucuk']}|{K['col']['imza_min']}"}
    # Y6 meta (ABD), Y7 CNN + genel model (ABD), donmuş uygulama AVR / BIST
    X = SON["ABD"]["X"]; ozl = cy_ozellik_adlari(X); ozl = [c for c in ozl if c not in ("r_ix", "cikis_tarih", "tip")]
    P1 = X[X.tip == "P1"].copy()
    P1m, sec, izg = cy_meta(P1, ozl, K, rng); R["secim"] += izg; R["meta_secim"] = {k: v for k, v in sec.items() if k != "modeller"}
    pd.DataFrame(sec["yillik"]).to_csv(os.path.join(A.cikti, "cy_meta_yillik.csv"), index=False)
    # genel sayısal model ve CNN: aynı havuz (eğitim HAVUZ + eğitim P1), doğrulama HAVUZ + doğrulama P1
    tr = X[((X.tip == "HAVUZ_egitim") | ((X.tip == "P1") & (X.tarih <= K["egitim"][1]))) & (X.cikis_tarih < pd.Timestamp(K["dogrulama"][0]) - pd.Timedelta(days=K["embargo_gun"]))]
    tr = tr.drop_duplicates(["sembol", "i"]); dg = X[(X.tip.isin(["HAVUZ_dogrulama", "P1"])) & (X.tarih >= K["dogrulama"][0]) & (X.tarih <= K["dogrulama"][1])
                                                   & (X.cikis_tarih < pd.Timestamp(K["test"][0][1]) - pd.Timedelta(days=K["embargo_gun"]))].drop_duplicates(["sembol", "i"])
    import lightgbm as lgb
    gm = lgb.LGBMClassifier(**K["genel_lgbm"], random_state=K["karar"]["tohum"]); gm.fit(tr[ozl], tr.y.astype(int))
    R["veri"]["havuz"] = {"egitim": int(len(tr)), "dogrulama": int(len(dg)), "egitim_isabet": float(tr.y.mean())}
    cnn = None
    if A.cnn and SON["ABD"]["resim"] is not None:
        try:
            Ri = SON["ABD"]["resim"]; trr = tr[tr.r_ix.notna() & tr.resim_ok.astype(bool)]; dgr = dg[dg.r_ix.notna() & dg.resim_ok.astype(bool)]
            cnn, ck = cy_cnn_egit(Ri[trr.r_ix.astype(int).to_numpy()], trr.y.to_numpy(np.float32), Ri[dgr.r_ix.astype(int).to_numpy()], dgr.y.to_numpy(np.float32), K)
            R["cnn_kayit"] = ck
        except Exception as ex:
            cylog.error("CNN eğitilemedi: %s", ex); R["notlar"].append(f"CNN eğitilemedi: {ex}")
    # olasılıklar: bütün pazarların P1 / P2 satırları
    for pz, S in SON.items():
        Xp = S["X"]; Xp["genel_p"] = gm.predict_proba(Xp[ozl])[:, 1]
        if cnn is not None and S["resim"] is not None:
            ok = Xp.r_ix.notna() & Xp.resim_ok.astype(bool); Xp["cnn_p"] = np.nan
            Xp.loc[ok, "cnn_p"] = cnn._cy_tahmin(S["resim"][Xp.loc[ok, "r_ix"].astype(int).to_numpy()])
        else:
            Xp["cnn_p"] = np.nan
        if pz == "ABD":
            Xp["meta_p"] = np.nan; Xp.loc[P1m.index, "meta_p"] = P1m.meta_p
        else:                                                         # donmuş ABD yıllık meta modelleri
            Xp["meta_p"] = np.nan
            for Y, m in sec["modeller"].items():
                w = (Xp.tip == "P1") & (Xp.tarih.dt.year == Y); Xp.loc[w, "meta_p"] = m.predict_proba(Xp.loc[w, ozl])[:, 1] if w.any() else np.nan
        S["X"] = Xp
    dgP1 = _cy_donem(SON["ABD"]["X"][SON["ABD"]["X"].tip == "P1"], *K["dogrulama"])
    sec_g, izg_g = cy_esik_sec(dgP1, "genel_p", K, "genel"); R["secim"] += izg_g
    sec_c, izg_c = cy_esik_sec(dgP1[dgP1.cnn_p.notna()], "cnn_p", K, "cnn") if cnn is not None else ({"pay": np.nan, "p": np.nan}, [])
    R["secim"] += izg_c; R["genel_secim"] = sec_g; R["cnn_secim"] = sec_c
    # H4 / H5 / H6 test hücreleri (her pazar)
    for pz, S in SON.items():
        P1x = S["X"][S["X"].tip == "P1"]; P2x = S["X"][S["X"].tip == "P2"]
        for dn, a, b in [("dogrulama", *K["dogrulama"])] + list(K["test"]):
            D = _cy_donem(P1x, a, b)
            for ad, kol, s_ in (("META", "meta_p", R["meta_secim"]), ("GENEL", "genel_p", sec_g), ("CNN", "cnn_p", sec_c)):
                if not np.isfinite(s_.get("p", np.nan)) or D[kol].notna().sum() == 0:
                    continue
                Dk = D[D[kol].notna()]; Sx = Dk[Dk[kol] >= s_["p"]]
                o = cy_ozet(Sx, K, rng); ftam = cy_boot_iki(Sx.assign(_f=Sx.y), Dk.assign(_f=Dk.y), "_f", K["karar"]["boot"], rng)
                fnet = cy_boot_iki(Sx.assign(_f=Sx.net), Dk.assign(_f=Dk.net), "_f", K["karar"]["boot"], rng)
                auc = cy_auc_boot(Dk.y.to_numpy(float), Dk[kol].to_numpy(float), Dk.tarih, K["karar"]["boot"], rng)
                R["hucre"].append({"pazar": pz, "kume": f"P1_{ad}", "donem": dn, "etiket": "ana_20_10_60", **o, "secim_fark": ftam[0], "secim_fark_alt": ftam[1],
                                   "secim_net_fark": fnet[0], "secim_net_fark_alt": fnet[1], "auc": auc[0], "auc_alt": auc[1], "auc_ust": auc[2], "n_hepsi": len(Dk)})
            # H6: CNN - genel AUC farkı aynı adaylarda
            Dk = D[D.cnn_p.notna()]
            if len(Dk) >= 30 and Dk.y.nunique() == 2:
                from sklearn.metrics import roc_auc_score
                ay = (Dk.tarih.dt.year * 12 + Dk.tarih.dt.month).to_numpy(); ua = np.unique(ay); bs = []
                for _ in range(300):
                    ix = np.concatenate([np.flatnonzero(ay == u) for u in rng.choice(ua, len(ua))])
                    if Dk.y.iloc[ix].nunique() == 2:
                        bs.append(roc_auc_score(Dk.y.iloc[ix], Dk.cnn_p.iloc[ix]) - roc_auc_score(Dk.y.iloc[ix], Dk.genel_p.iloc[ix]))
                d0 = roc_auc_score(Dk.y, Dk.cnn_p) - roc_auc_score(Dk.y, Dk.genel_p)
                R["hucre"].append({"pazar": pz, "kume": "AUC_CNN-GENEL", "donem": dn, "etiket": "ana_20_10_60", "n": len(Dk), "fark": d0,
                                   "fark_alt": float(np.quantile(bs, 0.025)) if bs else np.nan, "fark_ust": float(np.quantile(bs, 0.975)) if bs else np.nan})
            # genel havuz AUC (yalnız ABD test havuzu): modeller genel olarak öğrenmiş mi
            if pz == "ABD":
                Hv = _cy_donem(S["X"][S["X"].tip.str.startswith("HAVUZ_")], a, b)
                for ad, kol in (("GENEL", "genel_p"), ("CNN", "cnn_p")):
                    Hk = Hv[Hv[kol].notna()]
                    if len(Hk) > 100:
                        auc = cy_auc_boot(Hk.y.to_numpy(float), Hk[kol].to_numpy(float), Hk.tarih, 200, rng)
                        R["hucre"].append({"pazar": pz, "kume": f"HAVUZ_AUC_{ad}", "donem": dn, "etiket": "ana_20_10_60", "n": len(Hk), "auc": auc[0], "auc_alt": auc[1], "auc_ust": auc[2]})
        # Y9 portföy (test dönemleri)
        takvim = pd.DatetimeIndex(sorted(S["P"].tarih.unique()))
        for dn, a, b in K["test"]:
            b2 = K["kriz"] if dn == "2024-26" else b
            hav: Dict[pd.Timestamp, List[Tuple[str, int]]] = {}
            Pd = _cy_donem(S["P"], a, b)
            for s_, i_, t_ in zip(Pd.sembol.to_numpy(), Pd.i.to_numpy(), Pd.tarih.to_numpy()):
                h = S["H"][s_]
                if i_ + 1 < len(h["tarih"]):
                    hav.setdefault(pd.Timestamp(h["tarih"][i_ + 1]), []).append((s_, int(i_)))
            piy = cy_piyasa(S["H"], S["P"], a, b2); ek = {}
            En = K.get("_endeks", pd.DataFrame())
            for kod in K["endeks"].get(pz, ()):
                if kod in En:
                    e = En[kod].dropna(); e = e[(e.index >= pd.Timestamp(a)) & (e.index <= pd.Timestamp(b2))]
                    if len(e) > 10:
                        ad = "endeks_" + kod.replace("^", "").replace(".", "_")      # tablo sütunu olarak geçerli ad
                        ek[ad] = float(e.iloc[-1] / e.iloc[0] - 1); ek[ad + "_mdd"] = float((e / e.cummax() - 1).min())
            rs = [cy_portfoy(S["H"], [], a, b2, pz, K, (np.random.default_rng(1000 + k), hav), takvim) for k in range(K["portfoy"]["rastgele_n"])]
            rs_m = pd.DataFrame([{k: v for k, v in r.items() if k != "deger"} for r in rs]).median().to_dict()
            for ad, kol, s_ in (("P1_hepsi", None, None), ("P1_META", "meta_p", R["meta_secim"]), ("P1_GENEL", "genel_p", sec_g), ("P1_CNN", "cnn_p", sec_c), ("P2_hepsi", None, None)):
                tip = "P2" if ad.startswith("P2") else "P1"; D = _cy_donem(S["X"][S["X"].tip == tip], a, b)
                if kol is not None:
                    if not np.isfinite((s_ or {}).get("p", np.nan)):
                        continue
                    D = D[D[kol] >= s_["p"]].sort_values(["tarih", kol], ascending=[True, False])
                else:
                    D = D.sort_values(["tarih", "sembol"])
                po = cy_portfoy(S["H"], [(t, s_, int(i_)) for t, s_, i_ in zip(D.tarih, D.sembol, D.i)], a, b2, pz, K, None, takvim)
                R["portfoy"].append({"pazar": pz, "donem": dn, "strateji": ad, "sinyal_n": len(D), **{k: v for k, v in po.items() if k != "deger"},
                                     "piyasa_toplam": piy["toplam"], "piyasa_mdd": piy["mdd"], "rastgele_toplam": rs_m.get("toplam"), "rastgele_mdd": rs_m.get("mdd"),
                                     "rastgele_kazanma": rs_m.get("kazanma"), "rastgele_ort_islem": rs_m.get("ort_islem"), **ek})
    # D: yükselen / yükselmeyen P1 adaylarının özellik farkı (eğitim + doğrulama, ABD) — betimleyici
    P1a = _cy_donem(SON["ABD"]["X"][SON["ABD"]["X"].tip == "P1"], K["egitim"][0], K["dogrulama"][1])
    if len(P1a) and P1a.y.nunique() == 2:
        k1 = P1a[P1a.y == 1][ozl].median(); k0 = P1a[P1a.y == 0][ozl].median(); sd = P1a[ozl].std() + 1e-12
        R["yukselen"] = pd.DataFrame({"yukselen_medyan": k1, "yukselmeyen_medyan": k0, "fark_sd": (k1 - k0) / sd}).sort_values("fark_sd", key=np.abs, ascending=False)
        R["yukselen"].to_csv(os.path.join(A.cikti, "cy_yukselen_yukselmeyen.csv"))
    try:
        imp = pd.Series(np.mean([m.feature_importances_ for m in sec["modeller"].values()], axis=0), index=ozl).sort_values(ascending=False)
        imp.to_csv(os.path.join(A.cikti, "cy_meta_onem.csv"))
        R["meta_onem"] = imp
    except Exception as ex:
        cylog.warning("önem yazılamadı: %s", ex)
    Hc = pd.DataFrame(R["hucre"]); Iz = pd.DataFrame(R["izgara"]); Sc = pd.DataFrame(R["secim"]); Pf = pd.DataFrame(R["portfoy"])
    Hc.to_csv(os.path.join(A.cikti, "cy_hucre.csv"), index=False); Iz.to_csv(os.path.join(A.cikti, "cy_izgara.csv"), index=False)
    Sc.to_csv(os.path.join(A.cikti, "cy_secim.csv"), index=False); Pf.to_csv(os.path.join(A.cikti, "cy_portfoy.csv"), index=False)
    pd.DataFrame(R["cnn_kayit"]).to_csv(os.path.join(A.cikti, "cy_cnn_kayit.csv"), index=False)
    for pz, S in SON.items():
        S["E"][S["E"].tip.isin(["P1", "P2", "ES"])].drop(columns=["vd"], errors="ignore").to_csv(os.path.join(A.cikti, f"cy_olay_{pz}.csv.gz"), index=False)
        cols = ["sembol", "tarih", "tip", "y", "net", "e_y", "meta_p", "genel_p", "cnn_p", "col_dusus", "col_kucuk", "col_imza", "batan"]
        S["X"][S["X"].tip.isin(["P1", "P2"])][[c for c in cols if c in S["X"]]].to_csv(os.path.join(A.cikti, f"cy_aday_{pz}.csv.gz"), index=False)
    R["H"] = cy_hipotez(Hc, Pf, R, K)
    pd.DataFrame(R["H"]).to_csv(os.path.join(A.cikti, "cy_hipotez.csv"), index=False)
    R["tablolar"] = {"hucre": Hc, "izgara": Iz, "secim": Sc, "portfoy": Pf}
    return R


def _cy_h(Hc: pd.DataFrame, pz: str, kume: str, dn: str, et: str = "ana_20_10_60") -> Dict[str, Any]:
    q = Hc[(Hc.pazar == pz) & (Hc.kume == kume) & (Hc.donem == dn) & (Hc.etiket == et)]
    return q.iloc[0].to_dict() if len(q) else {}


def cy_hipotez(Hc: pd.DataFrame, Pf: pd.DataFrame, R: Dict[str, Any], K: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Önceden yazılı karar kuralları -> her hipotez için 'DESTEKLENİYOR' / 'DESTEKLENMİYOR' / 'ÖLÇÜLEMEDİ'."""
    tests = [t[0] for t in K["test"]]; out = []
    fe = K["karar"]["fark"]

    def ekle(kod, ad, ok, ayrinti):
        out.append({"kod": kod, "hipotez": ad, "karar": ("ÖLÇÜLEMEDİ" if ok is None else ("DESTEKLENİYOR" if ok else "DESTEKLENMİYOR")), "ayrinti": ayrinti})

    def h_taban(pz, kume):
        cs = [_cy_h(Hc, pz, kume, dn) for dn in tests]
        return (all(cy_tutar(c, K) for c in cs) if all(c for c in cs) else None), "; ".join(
            f"{dn}: n {c.get('n')}, isabet {c.get('isabet', np.nan):.3f}, taban {c.get('taban', np.nan):.3f}, fark {c.get('fark', np.nan):+.3f} "
            f"[{c.get('fark_alt', np.nan):+.3f}], net {c.get('net', np.nan):+.4f} (taban farkı {c.get('net_fark', np.nan):+.4f})" for dn, c in zip(tests, cs) if c)
    for kod, kume, ad in (("H1", "P1", "Çöl Yolu oluşurken (P1) aynı gün aynı oynaklıktaki rastgeleden iyi"), ("H3", "P2", "Kırılım (P2) rastgeleden iyi")):
        ok, ay = h_taban("ABD", kume); ekle(kod, ad + " (ABD)", ok, ay)
    cs = [_cy_h(Hc, "ABD", "P1-ES", dn) for dn in tests]
    ok = all(c.get("n", 0) >= K["karar"]["n_min"] and (c.get("fark") or -1) >= fe and (c.get("fark_alt") or -1) > 0 for c in cs) if all(cs) else None
    ekle("H2", "Sıkışma imzası fark yaratıyor: P1, aynı düşüş ve dipteki imzasız eşlerden iyi (ABD)", ok,
         "; ".join(f"{dn}: fark {c.get('fark', np.nan):+.3f} [{c.get('fark_alt', np.nan):+.3f}, {c.get('fark_ust', np.nan):+.3f}], n {c.get('n')} / eş {c.get('n_es')}" for dn, c in zip(tests, cs) if c))
    for kod, ad_, kume in (("H4", "Meta-etiketleme P1 seçimini iyileştiriyor (ABD)", "P1_META"), ("H5", "CNN P1 seçimini iyileştiriyor (ABD)", "P1_CNN")):
        cs = [_cy_h(Hc, "ABD", kume, dn) for dn in tests]
        if not all(cs):
            ekle(kod, ad_, None, "model / eşik yok"); continue
        ok = all(c.get("n", 0) >= K["karar"]["n_min"] and (c.get("secim_fark") or -1) >= fe and (c.get("secim_fark_alt") or -1) > 0
                 and (c.get("secim_net_fark") or -1) > 0 for c in cs)
        if kod == "H5":
            ok = ok and all((c.get("auc_alt") or 0) > 0.5 for c in cs)
        ekle(kod, ad_, ok, "; ".join(f"{dn}: seçilen n {c.get('n')} / {c.get('n_hepsi')}, isabet farkı {c.get('secim_fark', np.nan):+.3f} [{c.get('secim_fark_alt', np.nan):+.3f}], "
                                      f"net farkı {c.get('secim_net_fark', np.nan):+.4f}, AUC {c.get('auc', np.nan):.3f} [{c.get('auc_alt', np.nan):.3f}]" for dn, c in zip(tests, cs)))
    cs = [_cy_h(Hc, "ABD", "AUC_CNN-GENEL", dn) for dn in tests]
    ekle("H6", "CNN ile sayısal model aynı adaylarda (AUC farkı; yön önceden yok)", None if not all(cs) else
         all((c.get("fark_alt") or -1) > 0 for c in cs), "; ".join(f"{dn}: CNN - sayısal {c.get('fark', np.nan):+.3f} [{c.get('fark_alt', np.nan):+.3f}, {c.get('fark_ust', np.nan):+.3f}]" for dn, c in zip(tests, cs) if c)
         + " (DESTEKLENİYOR = CNN daha iyi; DESTEKLENMİYOR = CNN üstün değil)")
    q = Pf[(Pf.pazar == "ABD") & (Pf.strateji == "P1_META")]
    spy = q["endeks_SPY"] if "endeks_SPY" in q else pd.Series(np.nan, index=q.index)
    ok = (bool(len(q) == len(tests) and ((q.toplam > q.piyasa_toplam) & (q.toplam > q.rastgele_toplam) & (q.toplam > spy.fillna(-9))).all()) if len(q) else None)
    ekle("H7", "Meta portföyü maliyet sonrası piyasayı, rastgeleyi ve SPY'yi geçiyor (ABD)", ok,
         "; ".join(f"{r.donem}: portföy {r.toplam:+.1%} (MDD {r.mdd:.1%}, işlem {r.islem_n}, kazanma {r.kazanma:.0%}), piyasa {r.piyasa_toplam:+.1%}, "
                   f"rastgele {r.rastgele_toplam:+.1%}, SPY {getattr(r, 'endeks_SPY', np.nan):+.1%}" for r in q.itertuples()))
    pb = R.get("pbo", {})
    ok = (pb.get("pbo", np.nan) < 0.5 and pb.get("dsr_dsr", 0) >= 0.95) if np.isfinite(pb.get("pbo", np.nan)) else None
    ekle("H8", "Aşırı uyum riski düşük: PBO < 0,5 ve seçilmiş yapının DSR >= 0,95", ok,
         f"PBO {pb.get('pbo', np.nan):.2f} ({pb.get('kombinasyon')} bölünme), DSR {pb.get('dsr_dsr', np.nan):.2f}, seçilen {pb.get('secilen_yapi')}, ana {pb.get('ana_yapi')}")
    cs = [(_cy_h(Hc, "ABD", "P1", dn), _cy_h(Hc, "ABD", "P1_batansiz", dn)) for dn in tests]
    ekle("H9", "Hayatta kalma yanlılığı (batanlar çıkarılınca P1 farkı; bilgi)", None,
         "; ".join(f"{dn}: batanlar dahil {a.get('fark', np.nan):+.3f} (n {a.get('n')}), batansız {b.get('fark', np.nan):+.3f} (n {b.get('n')})" for dn, (a, b) in zip(tests, cs) if a and b))
    for pz in ("AVR", "BIST"):
        if not len(Hc[Hc.pazar == pz]):
            continue
        ok1, ay1 = h_taban(pz, "P1"); ok3, ay3 = h_taban(pz, "P2")
        ekle("H10" if pz == "AVR" else "H10-BIST", f"Çoğaltma {pz}: P1 / P2 rastgeleden iyi (donmuş kurallar)", (ok1 or ok3) if (ok1 is not None and ok3 is not None) else None,
             f"P1 {ay1} | P2 {ay3}")
        cs = [_cy_h(Hc, pz, "P1_META", dn) for dn in tests]
        if all(cs):
            ok = all(c.get("n", 0) >= K["karar"]["n_min"] and (c.get("secim_fark") or -1) >= fe and (c.get("secim_fark_alt") or -1) > 0 and (c.get("secim_net_fark") or -1) > 0 for c in cs)
            ekle(("H10" if pz == "AVR" else "H10-BIST") + "-META", f"Çoğaltma {pz}: ABD'de eğitilmiş meta model seçimi iyileştiriyor", ok,
                 "; ".join(f"{dn}: isabet farkı {c.get('secim_fark', np.nan):+.3f} [{c.get('secim_fark_alt', np.nan):+.3f}], n {c.get('n')}" for dn, c in zip(tests, cs)))
    d = {h["kod"]: h["karar"] for h in out}
    abd = (d.get("H1") == "DESTEKLENİYOR" or d.get("H3") == "DESTEKLENİYOR") and d.get("H2") == "DESTEKLENİYOR"
    avr = d.get("H10") == "DESTEKLENİYOR"
    out.append({"kod": "SONUÇ", "hipotez": "Çöl Yolu öngörü değeri (önceden yazılı kural)", "karar": "İZ" if (abd and avr) else ("ABD-ADAY" if abd else "İZ DEĞİL"),
                "ayrinti": f"ABD (H1/H3 ve H2): {abd}; Avrupa çoğaltma (H10): {avr}"})
    return out


# ---------------------------------------------------------------- Y10 RAPOR
def cy_rapor(R: Dict[str, Any], A: CYAyar, K: Dict[str, Any]) -> str:
    """Markdown rapor (cy_rapor.md): veri, hipotez kararları, hücreler, portföy, ızgara / PBO, başarısız testler."""
    T = R["tablolar"]; Hc, Pf = T["hucre"], T["portfoy"]
    f = lambda x, p=3: ("" if x is None or (isinstance(x, float) and not np.isfinite(x)) else (f"{x:+.{p}f}" if isinstance(x, float) else str(x)))
    L = [f"# ÇÖL YOLU — ABD araştırması ({CY_SURUM})", "", f"Süre {R.get('sure_dk')} dk. Kurallar koşudan önce yazıldı (dosya başı, ÖN KAYIT).", "",
         "## Veri", ""]
    for pz, v in R["veri"].items():
        L.append(f"- {pz}: {v}")
    L += ["", "## Hipotez kararları", "", "| Kod | Hipotez | Karar | Ayrıntı |", "|---|---|---|---|"]
    for h in R["H"]:
        L.append(f"| {h['kod']} | {h['hipotez']} | **{h['karar']}** | {h['ayrinti']} |")
    L += ["", "## Olay hücreleri (ana etiket +%20 / -%10 / 60 gün)", "",
          "| Pazar | Küme | Dönem | n | İsabet | Taban | Fark [alt] | Net ort | Net-taban | Kazanma | Ort kazanç | Ort kayıp |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in Hc[(Hc.etiket == "ana_20_10_60") & Hc.kume.isin(["P1", "P2", "ES", "P1_batansiz", "P1_META", "P1_GENEL", "P1_CNN"])].itertuples():
        L.append(f"| {r.pazar} | {r.kume} | {r.donem} | {r.n} | {f(getattr(r, 'isabet', np.nan))} | {f(getattr(r, 'taban', np.nan))} | {f(getattr(r, 'fark', np.nan))} "
                 f"[{f(getattr(r, 'fark_alt', np.nan))}] | {f(getattr(r, 'net', np.nan), 4)} | {f(getattr(r, 'net_fark', np.nan), 4)} | {f(getattr(r, 'kazanma', np.nan), 2)} | "
                 f"{f(getattr(r, 'ort_kazanc', np.nan), 3)} | {f(getattr(r, 'ort_kayip', np.nan), 3)} |")
    L += ["", "## Portföy (10 yuva, günde en çok 2 giriş, üçlü bariyer çıkışı, maliyetli)", "",
          "| Pazar | Dönem | Strateji | Toplam | Yıllık | MDD | İşlem | Kazanma | Ort işlem | Ort kazanç | Ort kayıp | Piyasa (EA) | Piyasa MDD | Rastgele | Endeks |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in Pf.itertuples():
        en = ", ".join(f"{k[7:]} {f(v, 3)}" for k, v in r._asdict().items() if k.startswith("endeks_") and not k.endswith("_mdd") and isinstance(v, float) and np.isfinite(v))
        L.append(f"| {r.pazar} | {r.donem} | {r.strateji} | {f(r.toplam, 3)} | {f(r.yillik, 3)} | {f(r.mdd, 3)} | {r.islem_n} | {f(r.kazanma, 2)} | {f(r.ort_islem, 4)} | "
                 f"{f(r.ort_kazanc, 3)} | {f(r.ort_kayip, 3)} | {f(r.piyasa_toplam, 3)} | {f(r.piyasa_mdd, 3)} | {f(r.rastgele_toplam, 3)} | {en} |")
    L += ["", "## Parametre arama ve aşırı uyum", "", f"- {R.get('pbo')}", f"- Meta seçim: {R.get('meta_secim')}; genel: {R.get('genel_secim')}; CNN: {R.get('cnn_secim')}",
          f"- CNN epoch kaydı: {R.get('cnn_kayit')}", "", "## Notlar", ""] + [f"- {n}" for n in R.get("notlar", [])]
    metin = "\n".join(L) + "\n"
    with open(os.path.join(A.cikti, "cy_rapor.md"), "w", encoding="utf-8") as fh:
        fh.write(metin)
    return metin


def _cakisma_kontrol_cy(_once=_CK_ONCE_CY, _dosya="COL_YOLU_ABD.py"):
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_CY", "_CK_KAYIT", "_cakisma_kontrol_cy", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("np", "pd", "os", "sys", "time", "json", "io", "math", "lzma", "zlib", "logging", "annotations", "Any", "Dict", "List", "Optional", "Tuple",
           "dataclass", "field", "combinations")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_cy()

if __name__ == "__main__" and "get_ipython" not in globals():       # Colab exec(): yalnız yükler, cy_calistir() ayrıca çağrılır
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    cy_calistir()
