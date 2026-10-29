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
# ÖN KAYIT v1.1 (29 Eki 2026, Cemal'in birleştirilmiş araştırma planı; v1.0'ın TEST sonucu görülmeden yazıldı). v1.0 kararları aynen kalır
#  (v1.0 özellik listesi CY['oz_v10'] ile dondurulur). Ekler (cy_analiz_b):
#  B1 ETİKET: oynaklığa bağlı üçlü bariyer (σ = 60 gün günlük getiri std, s = σ x √60; üst = s, [%5, %100]; alt = -0,5 s, [-%3, -%50];
#     60 gün) sabit +%20 / -%10 ile aynı örneklerde karşılaştırılır. Aynı gün hem hedef hem stop (boşluksuz) = BELİRSİZ: ana etikette
#     muhafazakâr (stop) sayılır, ayrıca belirsizler çıkarılarak duyarlılık yazılır; sayısı raporlanır.
#  B2 ÖNCEKİ ADAY 'ABD HACİMLİ TABAN' (K38 / Ç112, eşli +%14,9 2024-26): hacim >= 20 x önceki 20 gün medyanı ve gün getirisi <= -%9,5;
#     aynı üçlü bariyer, taban, H1 kuralı ve portföyle yeniden ölçülür (HT).
#  B3 SAFHA ÖLÇÜLERİ: düşüş süresi (250 gün tepesinden dibe bar), düşüş / ATR, kırılım günü göreli hacmi, kapanışın mum içindeki yeri,
#     kutu tavanına uzaklık, para akışı (CMF20, OBV eğimi, A/D eğimi, MFI14; olumlu sinyal VARSAYILMAZ, açıklayıcı özellik), MACD histogramı.
#  B4 MODEL MERDİVENİ (ABD; P1 sessizlik ve P2 kırılım AYRI; aynı örnekler, yıl yıl ileri yürüyen, arındırma + ambargo): M0 birincil kural
#     (model yok) -> LR (medyan doldurma + ölçekleme + L2 lojistik, C = 1) -> GBM (LightGBM, v1.1 özellikleri) -> CNN (grafik resmi) ->
#     LSTM (60 günlük mum dizisi: getiri, aralık, gövde, fitiller, göreli hacim; 32 gizli). CNN / LSTM havuzda (2016-20) bir kez eğitilir.
#     KATKI kuralları (iki test hücresinde de): LR kabul = LR seçimi bütün adaylardan isabet >= +5 puan, alt uç > 0, net fark > 0;
#     GBM kabul = AUC(GBM) - AUC(LR) alt uç > 0 VE seçilmiş net getiri >= LR'ninki; CNN katkısı = doğrulamada (2021-22) kurulan yığma
#     lojistik [GBM, CNN] - [GBM] test AUC farkı alt uç > 0; LSTM katkısı = [GBM, LSTM] - [GBM] aynı kural (bilgi: [GBM, CNN, LSTM] - [GBM, CNN]).
#     Karmaşık model kuralı geçmezse 'katkı yok' yazılır, sisteme alınmaz.
#  B5 ÖZELLİK GRUPLARI (mum, oynaklık, hacim-akış, trend, momentum-düşüş, likidite-piyasa, çöl ölçüleri): GBM tam - grubu çıkarılmış AUC
#     farkı (ay kümeli aralık); 'ek bilgi var' = iki test hücresinde alt uç > 0. Yalnız-grup AUC'si bilgi.
#  B6 ÖLÇÜTLER: precision, recall, PR-AUC, ROC-AUC, Brier, kalibrasyon ondalıkları; portföyde Sharpe (günlük, √252), Calmar (yıllık / |MDD|).
#     Kırılımlar: yıl yıl, piyasa rejimi (SPY 200 gün ortalamasının üstü / altı), likidite üçte biri (yıl içi), sektör yoğunlaşması (HHI).
#  B7 KONTROLLER: negatif (aday etiketleri ay içinde karıştırılır -> GBM AUC ~0,5), plasebo (her P1 için aynı gün aynı oynaklık ondalığından
#     rastgele hisse -> H1 farkı ~0), pozitif (geleceği gören 5 gün getirisi özellik olarak eklenir -> AUC belirgin yükselmeli; hat sinyali görür).
#  B8 ÇOKLU TEST: ana farkların tek yönlü bootstrap p değerleri, Holm düzeltmesi.
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

CY_SURUM = "CY v1.1 (2026-10-29, K51 ABD Çöl Yolu: üçlü bariyer (sabit + oynaklık), meta-etiketleme, model merdiveni LR/GBM/CNN/LSTM, PBO/DSR, batanlar dahil)"
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
    # ---- v1.1 (cy_analiz_b) ----
    "b_etkin": True,
    "tb_vol": {"kat_ust": 1.0, "kat_alt": 0.5, "ufuk": 60, "ust_sinir": (0.05, 1.0), "alt_sinir": (0.03, 0.50)},
    "ht": {"kat": 20.0, "esik": -0.095, "pencere": 20, "ayri": 40},
    "oz_v10": ("ar1", "ar5", "ar20", "ar60", "go20", "go60", "uw20", "lw20", "doji20", "doji60", "bbw", "bbw_yuzde250", "bbw_deg20", "atr14",
               "atr_oran", "v10_50", "v20_120", "ema20_egim5", "ema20_egim20", "ema50_egim20", "c_ema20", "c_ema50", "c_sma200", "r5", "r20",
               "r60", "r120", "r250", "dd250", "konum250", "dip_bar250", "log_dv20", "vol60", "rsi14", "col_dusus", "col_konum", "col_savunma",
               "col_bant", "col_kucuk", "col_bb_ok", "col_doji_ok", "col_hacim_ok", "col_imza", "piy_r20", "piy_r60"),
    "gruplar": {"mum": ("ar1", "ar5", "ar20", "ar60", "go20", "go60", "uw20", "lw20", "doji20", "doji60", "kapanis_yer"),
                "oynaklik": ("bbw", "bbw_yuzde250", "bbw_deg20", "atr14", "atr_oran", "vol60"),
                "hacim_akis": ("v10_50", "v20_120", "kir_hacim", "cmf20", "obv_egim20", "ad_egim20", "mfi14"),
                "trend": ("ema20_egim5", "ema20_egim20", "ema50_egim20", "c_ema20", "c_ema50", "c_sma200", "rsi14", "macd_hist"),
                "momentum_dusus": ("r5", "r20", "r60", "r120", "r250", "dd250", "konum250", "dip_bar250", "tepe_bar250", "dus_sure", "dus_atr"),
                "likidite_piyasa": ("log_dv20", "piy_r20", "piy_r60"),
                "col": ("col_dusus", "col_konum", "col_savunma", "col_bant", "col_kucuk", "col_bb_ok", "col_doji_ok", "col_hacim_ok", "col_imza", "kir_pay")},
    "lr_C": 1.0,
    "lstm": {"gizli": 32, "epoch": 5, "sabir": 1, "batch": 512, "lr": 1e-3, "tohum": 52},
    "boot_auc": 300,
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
    # v1.1 safha ve akış ölçüleri (hepsi yalnız o gün ve öncesi)
    tepe_bar = pd.Series(_cy_kayan_argmin(-H.to_numpy(float), 251), index=d.index)
    mfm = (((C - L_) - (H - C)) / rng.where(rng > 0)).fillna(0.0); Vs20 = V.rolling(20).sum() + eps
    obv = (np.sign(C.diff()).fillna(0) * V).cumsum(); adl = (mfm * V).cumsum(); tp = (H + L_ + C) / 3; para = tp * V
    pozp = para.where(tp > tp.shift(1), 0.0).rolling(14).sum(); negp = para.where(tp < tp.shift(1), 0.0).rolling(14).sum()
    e12 = C.ewm(span=12, adjust=False).mean(); e26 = C.ewm(span=26, adjust=False).mean(); macd = e12 - e26
    F = F.assign(kapanis_yer=((C - L_) / rng.where(rng > 0)).fillna(0.5),
                 kir_hacim=V / (V.shift(1).rolling(20, min_periods=16).median() + eps),
                 tepe_bar250=tepe_bar, dus_sure=tepe_bar - F.dip_bar250, dus_atr=(maxH250 - minL250) / (atr14 + eps),
                 cmf20=(mfm * V).rolling(20).sum() / Vs20, obv_egim20=(obv - obv.shift(20)) / Vs20, ad_egim20=(adl - adl.shift(20)) / Vs20,
                 mfi14=100 - 100 / (1 + pozp / (negp + eps)), macd_hist=(macd - macd.ewm(span=9, adjust=False).mean()) / C)
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
    y = np.full(n, np.nan); br = np.full(n, np.nan); ck = np.full(n, -1, dtype=np.int64); bl = np.zeros(n, np.int8)
    ii = np.arange(n - 1); o = O[ii + 1]; ok = o > 0; ii = ii[ok]; o = o[ok]
    ust = np.broadcast_to(np.asarray(ust, float), (n,))[ii]; alt = np.broadcast_to(np.asarray(alt, float), (n,))[ii]   # v1.1: gün başına bariyer
    yy = np.zeros(len(ii)); bb = np.full(len(ii), np.nan); cc = np.full(len(ii), -1, dtype=np.int64); bit = np.zeros(len(ii), bool)
    bel = np.zeros(len(ii), bool)                                    # v1.1: aynı gün (boşluksuz) hem hedef hem stop = belirsiz sıra
    for t in range(ufuk):
        k = ii + 1 + t; var = k < n; kk = np.where(var, k, n - 1)
        Ok = O[kk]; gd = var & (t > 0) & (Ok <= o * (1 + alt)); gu = var & (t > 0) & (Ok >= o * (1 + ust))
        lh = var & (L[kk] <= o * (1 + alt)); hh = var & (H[kk] >= o * (1 + ust))
        bel |= lh & hh & ~gd & ~gu & ~bit
        for kos, deger, kaz in ((gd, Ok / o - 1, 0.0), (gu, Ok / o - 1, 1.0), (lh, alt.copy(), 0.0), (hh, ust.copy(), 1.0)):
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
    y[ii[tam]] = yy[tam]; br[ii[tam]] = bb[tam]; ck[ii[tam]] = cc[tam]; bl[ii[tam]] = bel[tam]
    gun = np.where(ck >= 0, ck - np.arange(n), -1)
    return pd.DataFrame({"y": y, "brut": br, "cikis": ck, "gun": gun, "belirsiz": bl}, index=d.index)


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
        # v1.1: hacimli taban (K38 / Ç112 tanımı) ve oynaklığa bağlı bariyer
        Kh = K["ht"]; Vv = d.Volume.astype(float); medv = Vv.shift(1).rolling(Kh["pencere"], min_periods=int(0.8 * Kh["pencere"])).median()
        r1 = d.Close / d.Close.shift(1) - 1
        S["HT"] = _cy_aralik(np.flatnonzero(((Vv >= Kh["kat"] * medv) & (medv > 0) & (r1 <= Kh["esik"])).to_numpy() & uygun), Kh["ayri"])
        Kv = K["tb_vol"]; sg = M["vol60"].to_numpy() * np.sqrt(Kv["ufuk"])
        u_v = np.clip(Kv["kat_ust"] * sg, *Kv["ust_sinir"]); a_v = -np.clip(Kv["kat_alt"] * sg, *Kv["alt_sinir"])
        Tv = cy_uclu_bariyer(d, np.nan_to_num(u_v, nan=0.2), np.nan_to_num(a_v, nan=-0.1), Kv["ufuk"], cikti_mi, K)
        yv = np.where(np.isfinite(sg), Tv.y.to_numpy(), np.nan); netv = Tv.brut.to_numpy() - mal
        pm = uygun & np.isfinite(T.y.to_numpy())
        pan = pd.DataFrame({"tarih": idx[pm], "i": np.flatnonzero(pm).astype(np.int32), "y": T.y.to_numpy()[pm].astype(np.float32),
                            "net": net[pm].astype(np.float32), "brut": T.brut.to_numpy()[pm].astype(np.float32),
                            "cikis": T.cikis.to_numpy()[pm].astype(np.int32), "yk": Tk.y.to_numpy()[pm].astype(np.float32),
                            "netk": netk[pm].astype(np.float32), "vol60": M["vol60"].to_numpy()[pm].astype(np.float32),
                            "r20": M["F"].r20.to_numpy()[pm].astype(np.float32), "r60": M["F"].r60.to_numpy()[pm].astype(np.float32),
                            "yv": yv[pm].astype(np.float32), "netv": netv[pm].astype(np.float32), "belirsiz": T.belirsiz.to_numpy()[pm].astype(np.int8),
                            "log_dv20": M["F"].log_dv20.to_numpy()[pm].astype(np.float32)})
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
        satir = pd.concat([O[O.tip.isin(["P1", "P2", "ES", "HT"])], H_], ignore_index=True)
        ii = np.unique(satir.i.to_numpy().astype(int)) if len(satir) else np.array([], dtype=int)
        Kc = K["col"]; c = M["col"][Kc["L"]]
        Fi = M["F"].iloc[ii].copy()
        for k2 in ("dusus", "konum", "savunma", "bant", "kucuk", "bb_ok", "doji_ok", "hacim_ok"):
            Fi["col_" + k2] = c[k2].to_numpy()[ii]
        Fi["col_imza"] = cy_imza(c, Kc["kucuk"]).to_numpy()[ii]
        Fi["kir_pay"] = (d.Close / c.tavan.shift(1) - 1).to_numpy()[ii]          # v1.1: dünkü kutu tavanına uzaklık
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
        Q = None
        if resim_ok and len(ii):                                     # v1.1: LSTM için 60 günlük mum dizisi (yalnız i ve öncesi)
            Oa, Ha, La, Ca, Va = (d[k].to_numpy(float) for k in ("Open", "High", "Low", "Close", "Volume")); Cp = np.r_[np.nan, Ca[:-1]]
            ham = np.column_stack([np.log(Ca / Cp), (Ha - La) / Cp, (Ca - Oa) / Cp, (Ha - np.maximum(Oa, Ca)) / Cp, (np.minimum(Oa, Ca) - La) / Cp,
                                   np.log((Va + 1) / (pd.Series(Va).rolling(60, min_periods=20).median().to_numpy() + 1))])
            ham = np.nan_to_num(np.clip(ham, -5, 5)); G = K["cnn"]["gun"]; Q = np.zeros((len(ii), G, ham.shape[1]), np.float16)
            for j, i in enumerate(ii):
                if i + 1 >= G:
                    Q[j] = ham[i - G + 1:i + 1]
        return {"pazar": pz, "sembol": s, "cikti_mi": cikti_mi, "panel": pan, "olay": O, "satir": satir, "F": Fi, "R": R, "Q": Q,
                "tarih": idx.to_numpy(), "kapanis": d.Close.to_numpy(np.float32), "acilis": d.Open.to_numpy(np.float32),
                "kayma": M["kayma"].to_numpy(np.float32), "T": T[["brut", "cikis"]].to_numpy(np.float64)}
    except Exception as ex:
        cylog.warning("CY %s %s atlandı: %s", pz, s, ex)
        return None


# ---------------------------------------------------------------- Y4 TABAN / EŞ + İSTATİSTİK
def cy_panel_taban(P: pd.DataFrame) -> pd.DataFrame:
    """Aynı gün, aynı oynaklık ondalığı ortalamaları: e_y, e_net, e_yk, e_netk."""
    P = P.copy(); P["vd"] = np.minimum((P.groupby("tarih").vol60.rank(pct=True) * 10).fillna(5).astype(int), 9).astype(np.int8)
    for c in [k for k in ("y", "net", "yk", "netk", "yv", "netv") if k in P]:
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
    gr = D.pct_change().dropna(); yl = float(D.iloc[-1] ** (1 / yil) - 1) if len(D) and yil else np.nan
    return {"toplam": float(D.iloc[-1] - 1) if len(D) else np.nan, "yillik": yl,
            "sharpe": float(gr.mean() / gr.std() * np.sqrt(252)) if len(gr) > 20 and gr.std() > 0 else np.nan,
            "calmar": float(yl / abs(mdd)) if mdd and np.isfinite(mdd) and mdd < 0 else np.nan,
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
    if K.get("b_etkin"):
        try:
            R["B"] = cy_analiz_b(SON, R, A, K, rng); pd.DataFrame(R["secim"]).to_csv(os.path.join(A.cikti, "cy_secim.csv"), index=False)
        except Exception as ex:
            cylog.exception("v1.1 analizi tamamlanamadı: %s", ex); R["notlar"].append(f"v1.1 analizi tamamlanamadı: {ex}")
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
    ek = [c for c in ("yv", "netv", "e_yv", "e_netv", "belirsiz", "log_dv20") if c in P]          # v1.1
    E = E.merge(P[["sembol", "i", "tarih", "y", "net", "brut", "cikis", "yk", "netk", "vol60", "vd", "e_y", "e_net", "e_yk", "e_netk"] + ek], on=["sembol", "i"], how="inner")
    E["gun"] = E.cikis - E.i
    E["cikis_tarih"] = [pd.Timestamp(H[s]["tarih"][min(int(c), len(H[s]["tarih"]) - 1)]) for s, c in zip(E.sembol, E.cikis)]
    E["batan"] = E.sembol.map(ev.batan).fillna(False).astype(bool); E["agirlik"] = E.sembol.map(ev.agirlik).fillna(1.0)
    F = pd.concat([r["F"].assign(sembol=r["sembol"]) for r in sonuc if len(r["F"])], ignore_index=True)
    F["i"] = F.i.astype(int)
    Rm, Rk, Qm = [], [], []
    for r in sonuc:
        if r["R"] is not None and len(r["F"]):
            Rm.append(r["R"]); Rk.append(pd.DataFrame({"sembol": r["sembol"], "i": r["F"].i.astype(int).to_numpy()}))
            if r.get("Q") is not None:
                Qm.append(r["Q"])
    resim = np.concatenate(Rm) if Rm else None; rk = pd.concat(Rk, ignore_index=True) if Rk else None
    dizi = np.concatenate(Qm) if (Qm and len(Qm) == len(Rm)) else None                     # v1.1 LSTM dizileri (resimle aynı sıra)
    if rk is not None:
        rk["r_ix"] = np.arange(len(rk))
        F = F.merge(rk, on=["sembol", "i"], how="left")
    S = pd.concat([r["satir"].assign(sembol=r["sembol"]) for r in sonuc if len(r["satir"])], ignore_index=True)
    S["i"] = S.i.astype(int)
    X = S.merge(F, on=["sembol", "i"], how="inner").merge(
        P[["sembol", "i", "tarih", "y", "net", "brut", "cikis", "yk", "netk", "vd", "e_y", "e_net", "e_yk", "e_netk"] + [c for c in ek if c != "log_dv20"]],
        on=["sembol", "i"], how="inner")
    X = X.merge(piy, left_on="tarih", right_index=True, how="left")
    X["cikis_tarih"] = [pd.Timestamp(H[s]["tarih"][min(int(c), len(H[s]["tarih"]) - 1)]) for s, c in zip(X.sembol, X.cikis)]
    X["gun"] = X.cikis - X.i; X["batan"] = X.sembol.map(ev.batan).fillna(False).astype(bool)
    return {"H": H, "P": P, "E": E, "X": X, "resim": resim, "dizi": dizi, "pazar": pz}


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
    X = SON["ABD"]["X"]; ozl = [c for c in K["oz_v10"] if c in X.columns]          # v1.0 özellik listesi dondurulmuş (v1.1 ekleri cy_analiz_b'de)
    P1 = X[X.tip == "P1"].copy()
    P1m, sec, izg = cy_meta(P1, ozl, K, rng); R["secim"] += izg; R["meta_secim"] = {k: v for k, v in sec.items() if k != "modeller"}
    pd.DataFrame(sec["yillik"]).to_csv(os.path.join(A.cikti, "cy_meta_yillik.csv"), index=False)
    # genel sayısal model ve CNN: aynı havuz (eğitim HAVUZ + eğitim P1), doğrulama HAVUZ + doğrulama P1
    tr = X[((X.tip == "HAVUZ_egitim") | ((X.tip == "P1") & (X.tarih <= K["egitim"][1]))) & (X.cikis_tarih < pd.Timestamp(K["dogrulama"][0]) - pd.Timedelta(days=K["embargo_gun"]))]
    tr = tr.drop_duplicates(["sembol", "i"]); dg = X[(X.tip.isin(["HAVUZ_dogrulama", "P1"])) & (X.tarih >= K["dogrulama"][0]) & (X.tarih <= K["dogrulama"][1])
                                                   & (X.cikis_tarih < pd.Timestamp(K["test"][0][1]) - pd.Timedelta(days=K["embargo_gun"]))].drop_duplicates(["sembol", "i"])
    import lightgbm as lgb
    R["_havuz"] = (tr.index, dg.index)                                # v1.1 LSTM aynı havuzu kullanır
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


# ---------------------------------------------------------------- v1.1 ANALİZ (cy_analiz_b): model merdiveni, katkı, kontroller, kırılımlar
def cy_lstm_egit(Xtr: np.ndarray, ytr: np.ndarray, Xdg: np.ndarray, ydg: np.ndarray, K: Dict[str, Any]) -> Tuple[Any, List[Dict[str, Any]]]:
    """60 günlük mum dizisinden LSTM (32 gizli). Özellikler eğitim ortalaması / std ile ölçeklenir; erken durma doğrulama kaybıyla."""
    import torch
    import torch.nn as nn
    Kl = K["lstm"]; torch.manual_seed(Kl["tohum"]); np.random.seed(Kl["tohum"]); cihaz = "cuda" if torch.cuda.is_available() else "cpu"
    mu = Xtr.astype(np.float32).reshape(-1, Xtr.shape[2]).mean(0); sd = Xtr.astype(np.float32).reshape(-1, Xtr.shape[2]).std(0) + 1e-6

    class Ag(nn.Module):
        def __init__(self):
            super().__init__(); self.l = nn.LSTM(Xtr.shape[2], Kl["gizli"], batch_first=True); self.o = nn.Linear(Kl["gizli"], 1)

        def forward(self, x):
            h, _ = self.l(x); return self.o(h[:, -1, :]).squeeze(1)
    net = Ag().to(cihaz); opt = torch.optim.Adam(net.parameters(), lr=Kl["lr"]); kf = nn.BCEWithLogitsLoss(); kayit = []; en_iyi = (np.inf, None); sabir = 0
    hz = lambda X: torch.from_numpy(((X.astype(np.float32) - mu) / sd)).to(cihaz)

    def tahmin(X):
        net.eval(); out = []
        with torch.no_grad():
            for a in range(0, len(X), 4096):
                out.append(net(hz(X[a:a + 4096])).cpu())
        return torch.cat(out)
    for ep in range(Kl["epoch"]):
        net.train(); sira = np.random.permutation(len(Xtr)); t0 = time.time(); top = 0.0
        for a in range(0, len(sira), Kl["batch"]):
            b = sira[a:a + Kl["batch"]]; yb = torch.from_numpy(ytr[b]).float().to(cihaz)
            opt.zero_grad(); ls = kf(net(hz(Xtr[b])), yb); ls.backward(); opt.step(); top += float(ls.detach()) * len(b)
        dk = float(kf(tahmin(Xdg), torch.from_numpy(ydg).float()))
        kayit.append({"epoch": ep + 1, "egitim_kayip": top / len(sira), "dogrulama_kayip": dk, "sure_sn": round(time.time() - t0)})
        cylog.info("LSTM epoch %d: eğitim %.4f doğrulama %.4f (%ds)", ep + 1, top / len(sira), dk, time.time() - t0)
        if dk < en_iyi[0] - 1e-4:
            en_iyi = (dk, {k: v.detach().clone() for k, v in net.state_dict().items()}); sabir = 0
        else:
            sabir += 1
            if sabir > Kl["sabir"]:
                break
    if en_iyi[1] is not None:
        net.load_state_dict(en_iyi[1])
    net._cy_tahmin = lambda X: torch.sigmoid(tahmin(X)).numpy()     # type: ignore[attr-defined]
    return net, kayit


def cy_ileri(E: pd.DataFrame, ozl: List[str], kur: Any, K: Dict[str, Any], ycol: str = "y") -> pd.Series:
    """Yıl yıl ileri yürüyen OOS olasılık (2021..2026): her yıl yalnız çıkışı o yıldan (ambargo payıyla) önce biten satırlarla eğitilir."""
    p = pd.Series(np.nan, index=E.index); X = E[ozl].replace([np.inf, -np.inf], np.nan)
    for Y in range(int(K["dogrulama"][0][:4]), 2027):
        sinir = pd.Timestamp(f"{Y}-01-01") - pd.Timedelta(days=K["embargo_gun"])
        tr = (E.cikis_tarih < sinir) & E[ycol].notna(); te = (E.tarih.dt.year == Y) & E[ycol].notna()
        if tr.sum() < K["meta"]["n_min_egitim"] or E.loc[tr, ycol].nunique() < 2 or not te.any():
            continue
        m = kur(); m.fit(X[tr], E.loc[tr, ycol].astype(int)); p[te] = m.predict_proba(X[te])[:, 1]
    return p


def cy_auc_fark(y: np.ndarray, p1: np.ndarray, p2: np.ndarray, tarih: pd.Series, B: int, rng: np.random.Generator) -> Dict[str, float]:
    """AUC(p1) - AUC(p2), aynı örnekler, ay kümeli bootstrap; tek yönlü p = farkın <= 0 olma payı."""
    from sklearn.metrics import roc_auc_score
    ok = np.isfinite(y) & np.isfinite(p1) & np.isfinite(p2); y, p1, p2 = y[ok], p1[ok], p2[ok]; ay = (tarih.dt.year * 12 + tarih.dt.month).to_numpy()[ok]
    if len(y) < 30 or len(np.unique(y)) < 2:
        return {"n": int(len(y)), "fark": np.nan, "alt": np.nan, "ust": np.nan, "p": np.nan}
    d0 = roc_auc_score(y, p1) - roc_auc_score(y, p2); ua = np.unique(ay); gr = {u: np.flatnonzero(ay == u) for u in ua}; bs = []
    for _ in range(B):
        ix = np.concatenate([gr[u] for u in rng.choice(ua, len(ua))])
        if len(np.unique(y[ix])) == 2:
            bs.append(roc_auc_score(y[ix], p1[ix]) - roc_auc_score(y[ix], p2[ix]))
    bs = np.array(bs)
    return {"n": int(len(y)), "fark": float(d0), "alt": float(np.quantile(bs, 0.025)), "ust": float(np.quantile(bs, 0.975)), "p": float(np.mean(bs <= 0))}


def cy_boot_p(D: pd.DataFrame, kol: str, B: int, rng: np.random.Generator) -> float:
    """Tek yönlü bootstrap p: ay kümeli ortalamanın <= 0 olma payı."""
    v = D[kol].to_numpy(float); ok = np.isfinite(v); v = v[ok]
    if len(v) < 10:
        return np.nan
    ay = (D.tarih.dt.year * 12 + D.tarih.dt.month).to_numpy()[ok]; ua, inv = np.unique(ay, return_inverse=True)
    sv = np.bincount(inv, v); sn = np.bincount(inv).astype(float); ix = rng.integers(0, len(ua), (B, len(ua)))
    return float(np.mean(sv[ix].sum(1) / sn[ix].sum(1) <= 0))


def cy_secim_olc(D: pd.DataFrame, kol: str, p_esik: float, K: Dict[str, Any], rng: np.random.Generator, ycol: str = "y", ncol: str = "net") -> Dict[str, Any]:
    """Bir hücrede model seçimi: precision, recall, ROC-AUC (+aralık), PR-AUC, Brier, seçilen - bütün isabet ve net farkı (aralık, p)."""
    from sklearn.metrics import average_precision_score
    D = D[D[kol].notna() & D[ycol].notna()]
    if not len(D) or not np.isfinite(p_esik):
        return {"n_hepsi": int(len(D))}
    S = D[D[kol] >= p_esik]; y = D[ycol].to_numpy(float); p = D[kol].to_numpy(float)
    auc = cy_auc_boot(y, p, D.tarih, K["boot_auc"], rng)
    fi = cy_boot_iki(S.assign(_f=S[ycol]), D.assign(_f=D[ycol]), "_f", K["karar"]["boot"], rng)
    fn = cy_boot_iki(S.assign(_f=S[ncol]), D.assign(_f=D[ncol]), "_f", K["karar"]["boot"], rng)
    r = S[ncol].to_numpy(float)
    return {"n_hepsi": int(len(D)), "n_secilen": int(len(S)), "taban_isabet": float(y.mean()), "precision": float(S[ycol].mean()) if len(S) else np.nan,
            "recall": float(S[ycol].sum() / max(D[ycol].sum(), 1)), "roc_auc": auc[0], "roc_auc_alt": auc[1], "roc_auc_ust": auc[2],
            "pr_auc": float(average_precision_score(y, p)) if len(np.unique(y)) == 2 else np.nan, "brier": float(np.mean((p - y) ** 2)),
            "net_secilen": float(np.nanmean(r)) if len(r) else np.nan, "net_hepsi": float(D[ncol].mean()), "isabet_fark": fi[0], "isabet_fark_alt": fi[1],
            "net_fark": fn[0], "net_fark_alt": fn[1], "kazanma": float(np.mean(r > 0)) if len(r) else np.nan,
            "ort_kayip": float(np.mean(r[r <= 0])) if (r <= 0).any() else np.nan}


def cy_sektor(A: CYAyar, EV: pd.DataFrame) -> pd.Series:
    """Sembol -> sektör: sektor_ABD.csv (Yahoo sektörü; repo kökü ya da veri klasörü), K34 şirketleri SIC bölümü (k35_sic.csv varsa)."""
    out = {}
    for yol in (os.path.join(A.veri, "sektor_ABD.csv"), os.path.join(os.path.dirname(os.path.abspath(globals().get("__file__", "."))), "sektor_ABD.csv")):
        if os.path.exists(yol):
            s = pd.read_csv(yol); out.update({str(k).split(".")[0]: v for k, v in zip(s.sembol, s.sektor)}); break
    sic = next((p for p in (os.path.join(A.veri, "k35_sic.csv"),) if os.path.exists(p)), None)
    ev = os.path.join(A.veri, "k34_evren.csv")
    if sic and os.path.exists(ev):
        bol = [(100, "Tarım"), (1000, "Madencilik"), (1500, "İnşaat"), (4000, "İmalat"), (5000, "Ulaştırma-Kamu"), (5200, "Toptan"),
               (6000, "Perakende"), (6800, "Finans"), (9100, "Hizmet"), (10000, "Kamu")]
        sc = pd.read_csv(sic).set_index("cik").sic; e = pd.read_csv(ev)
        for c, s_ in zip(e.cik, e.sembol):
            if s_ not in out and c in sc.index and np.isfinite(sc.loc[c]):
                out[s_] = next((ad for sin, ad in bol if sc.loc[c] < sin), "Diğer")
    return pd.Series(out)


def cy_analiz_b(SON: Dict[str, Dict[str, Any]], R: Dict[str, Any], A: CYAyar, K: Dict[str, Any], rng: np.random.Generator) -> Dict[str, Any]:
    """v1.1 ön kaydı (B1-B8). Çıktılar cy_b_*.csv; karar satırları R['H_b']."""
    import lightgbm as lgb
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    tests = list(K["test"]); dg_ = ("dogrulama", *K["dogrulama"]); B = {"hucre": [], "model": [], "katki": [], "grup": [], "kontrol": [], "kirilim": [],
                                                                       "portfoy": [], "kalibrasyon": [], "coklu": [], "notlar": []}
    S = SON["ABD"]; X = S["X"]; E = S["E"]; P = S["P"]
    ozl10 = [c for c in K["oz_v10"] if c in X]; ozl = list(dict.fromkeys(ozl10 + [c for g in K["gruplar"].values() for c in g if c in X]))
    LR = lambda: make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(C=K["lr_C"], max_iter=3000))
    GB = lambda: lgb.LGBMClassifier(**K["meta"]["lgbm"], random_state=K["karar"]["tohum"])
    donemler = [("egitim", *K["egitim"]), dg_] + tests
    # B1 / B2: etiket türleri, belirsiz, hacimli taban
    for tip in ("P1", "P2", "ES", "HT"):
        for dn, a, b in donemler:
            D = _cy_donem(E[E.tip == tip], a, b)
            for et, kol in (("sabit_20_10_60", ("y", "net", "e_y", "e_net")), ("oynak_s_0.5s_60", ("yv", "netv", "e_yv", "e_netv"))):
                if kol[0] not in D:
                    continue
                Dk = D.rename(columns={kol[0]: "_y", kol[1]: "_n", kol[2]: "_ey", kol[3]: "_en"})[["tarih", "_y", "_n", "_ey", "_en", "gun"]].rename(
                    columns={"_y": "y", "_n": "net", "_ey": "e_y", "_en": "e_net"}).dropna(subset=["y"])
                o = cy_ozet(Dk, K, rng); o["p"] = cy_boot_p(Dk.assign(_f=Dk.y - Dk.e_y), "_f", K["karar"]["boot"], rng) if len(Dk) else np.nan
                B["hucre"].append({"kume": tip, "donem": dn, "etiket": et, **o})
            if "belirsiz" in D and len(D):
                Db = D[D.belirsiz == 0]
                B["hucre"].append({"kume": tip + "_belirsizsiz", "donem": dn, "etiket": "sabit_20_10_60", "belirsiz_pay": float(D.belirsiz.mean()), **cy_ozet(Db, K, rng)})
    Hb = pd.DataFrame(B["hucre"])
    # B7 plasebo: her P1 olayına aynı gün aynı oynaklık ondalığından rastgele panel satırı
    p1 = E[E.tip == "P1"]; gr = P.groupby(["tarih", "vd"]).indices; sec = []
    for t, v in zip(p1.tarih, p1.vd):
        ix = gr.get((t, v))
        if ix is not None and len(ix):
            sec.append(ix[rng.integers(0, len(ix))])
    Pl = P.iloc[sec]
    for dn, a, b in donemler:
        o = cy_ozet(_cy_donem(Pl.assign(gun=Pl.cikis - Pl.i), a, b), K, rng); B["kontrol"].append({"kontrol": "plasebo_P1_esli_rastgele", "donem": dn, **o})
    # B4 / B5 / B7: model merdiveni ve gruplar (P1 ve P2 ayrı)
    H = S["H"]; tr_ix, dg_ix = R.get("_havuz", (None, None))
    lstm = None
    if S.get("dizi") is not None and tr_ix is not None and A.cnn:
        try:
            Q = S["dizi"]; trr = X.loc[tr_ix]; trr = trr[trr.r_ix.notna()]; dgr = X.loc[dg_ix]; dgr = dgr[dgr.r_ix.notna()]
            lstm, lk = cy_lstm_egit(Q[trr.r_ix.astype(int).to_numpy()], trr.y.to_numpy(np.float32), Q[dgr.r_ix.astype(int).to_numpy()], dgr.y.to_numpy(np.float32), K)
            B["notlar"].append(f"LSTM epoch kaydı: {lk}")
            ok = X.r_ix.notna(); X["lstm_p"] = np.nan; X.loc[ok, "lstm_p"] = lstm._cy_tahmin(Q[X.loc[ok, "r_ix"].astype(int).to_numpy()])
        except Exception as ex:
            cylog.error("LSTM eğitilemedi: %s", ex); B["notlar"].append(f"LSTM eğitilemedi: {ex}")
    if "lstm_p" not in X:
        X["lstm_p"] = np.nan
    if "cnn_p" not in X:
        X["cnn_p"] = np.nan
    gel = []                                                         # pozitif kontrol: geleceği gören 5 gün getirisi
    for s_, i_ in zip(X.sembol, X.i):
        h = H[s_]; gel.append(float(h["kapanis"][i_ + 5] / h["acilis"][i_ + 1] - 1) if i_ + 5 < len(h["kapanis"]) else np.nan)
    X["_gelecek5"] = gel
    for faz in ("P1", "P2"):
        Ef = X[X.tip == faz].copy()
        if len(Ef) < 200:
            B["notlar"].append(f"{faz}: aday az ({len(Ef)}), model merdiveni atlandı"); continue
        Ef["p_LR"] = cy_ileri(Ef, ozl, LR, K); Ef["p_GBM10"] = cy_ileri(Ef, ozl10, GB, K); Ef["p_GBM"] = cy_ileri(Ef, ozl, GB, K)
        Ef["p_GBM_oynak"] = cy_ileri(Ef, ozl, GB, K, ycol="yv") if "yv" in Ef else np.nan
        Ek = Ef.copy(); Ek["y"] = Ek.groupby(Ek.tarih.dt.to_period("M")).y.transform(lambda v: v.sample(frac=1.0, random_state=int(rng.integers(1 << 30))).to_numpy())
        Ef["p_KARISIK"] = cy_ileri(Ek, ozl, GB, K); Ef["y_karisik"] = Ek.y
        Ef["p_SIZINTI"] = cy_ileri(Ef, ozl + ["_gelecek5"], GB, K)
        for g, kols in K["gruplar"].items():
            Ef[f"p_cikar_{g}"] = cy_ileri(Ef, [c for c in ozl if c not in kols], GB, K)
            Ef[f"p_yalniz_{g}"] = cy_ileri(Ef, [c for c in kols if c in Ef], GB, K)
        # yığma: doğrulamada (2021-22) kurulur, testte uygulanır
        dgm = _cy_donem(Ef, *K["dogrulama"])
        for ad, kols in (("Y_G", ["p_GBM"]), ("Y_GC", ["p_GBM", "cnn_p"]), ("Y_GL", ["p_GBM", "lstm_p"]), ("Y_GCL", ["p_GBM", "cnn_p", "lstm_p"])):
            Ef[ad] = np.nan; d0 = dgm.dropna(subset=kols + ["y"])
            if len(d0) >= 100 and d0.y.nunique() == 2:
                lg = lambda Z: np.log(np.clip(Z, 1e-4, 1 - 1e-4) / (1 - np.clip(Z, 1e-4, 1 - 1e-4)))
                m = LogisticRegression(max_iter=2000).fit(lg(d0[kols].to_numpy()), d0.y.astype(int)); w = Ef[kols].notna().all(axis=1)
                Ef.loc[w, ad] = m.predict_proba(lg(Ef.loc[w, kols].to_numpy()))[:, 1]
        # eşik seçimi (doğrulama) ve test hücreleri
        dgm = _cy_donem(Ef, *K["dogrulama"]); esik = {}
        modeller = ["p_LR", "p_GBM10", "p_GBM", "cnn_p", "lstm_p", "Y_GC", "Y_GL", "Y_GCL", "p_KARISIK", "p_SIZINTI"]
        for mk in modeller:
            ycol = "y_karisik" if mk == "p_KARISIK" else "y"
            sc, izg = cy_esik_sec(dgm[dgm[mk].notna()].assign(y=dgm[ycol]), mk, K, f"{faz}_{mk}"); esik[mk] = sc; R["secim"] += izg
            for dn, a, b in [dg_] + tests:
                D = _cy_donem(Ef, a, b)
                o = cy_secim_olc(D.assign(y=D[ycol]), mk, sc.get("p", np.nan), K, rng)
                B["model"].append({"faz": faz, "model": mk, "donem": dn, "secim_pay": sc.get("pay"), **o})
        if "yv" in Ef:
            sc, _ = cy_esik_sec(dgm[dgm.p_GBM_oynak.notna()].assign(y=dgm.yv, net=dgm.netv), "p_GBM_oynak", K, f"{faz}_GBM_oynak")
            for dn, a, b in [dg_] + tests:
                D = _cy_donem(Ef, a, b); o = cy_secim_olc(D, "p_GBM_oynak", sc.get("p", np.nan), K, rng, ycol="yv", ncol="netv")
                B["model"].append({"faz": faz, "model": "p_GBM_oynak_etiket", "donem": dn, "secim_pay": sc.get("pay"), **o})
        # katkı farkları (aynı örnekler)
        for dn, a, b in tests:
            D = _cy_donem(Ef, a, b)
            for ad, p1, p2 in (("GBM-LR", "p_GBM", "p_LR"), ("GBM-GBM10 (v1.1 ölçüleri)", "p_GBM", "p_GBM10"), ("CNN katkısı [G,C]-[G]", "Y_GC", "Y_G"),
                               ("LSTM katkısı [G,L]-[G]", "Y_GL", "Y_G"), ("LSTM üstüne [G,C,L]-[G,C]", "Y_GCL", "Y_GC"), ("CNN tek - GBM", "cnn_p", "p_GBM"),
                               ("LSTM tek - GBM", "lstm_p", "p_GBM"), ("LR - rastgele(0,5)", "p_LR", "_sabit")):
                q2 = np.full(len(D), 0.5) if p2 == "_sabit" else D[p2].to_numpy(float)
                if p2 == "_sabit":
                    from sklearn.metrics import roc_auc_score
                    a0 = cy_auc_boot(D.y.to_numpy(float), D[p1].to_numpy(float), D.tarih, K["boot_auc"], rng)
                    B["katki"].append({"faz": faz, "kiyas": ad, "donem": dn, "fark": a0[0] - 0.5 if np.isfinite(a0[0]) else np.nan, "alt": a0[1] - 0.5 if np.isfinite(a0[1]) else np.nan,
                                       "ust": a0[2] - 0.5 if np.isfinite(a0[2]) else np.nan, "p": np.nan, "n": int(D[p1].notna().sum())})
                    continue
                B["katki"].append({"faz": faz, "kiyas": ad, "donem": dn, **cy_auc_fark(D.y.to_numpy(float), D[p1].to_numpy(float), q2, D.tarih, K["boot_auc"], rng)})
            for g in K["gruplar"]:
                f = cy_auc_fark(D.y.to_numpy(float), D.p_GBM.to_numpy(float), D[f"p_cikar_{g}"].to_numpy(float), D.tarih, K["boot_auc"], rng)
                yal = cy_auc_boot(D.y.to_numpy(float), D[f"p_yalniz_{g}"].to_numpy(float), D.tarih, 100, rng)
                B["grup"].append({"faz": faz, "grup": g, "donem": dn, "tam_eksi_cikarilmis": f["fark"], "alt": f["alt"], "ust": f["ust"], "p": f["p"],
                                  "yalniz_auc": yal[0], "yalniz_auc_alt": yal[1], "n": f["n"]})
            # kontroller
            for kk, mk, ycol in (("negatif_karisik_etiket", "p_KARISIK", "y_karisik"), ("pozitif_gelecek5_sizinti", "p_SIZINTI", "y")):
                au = cy_auc_boot(D[ycol].to_numpy(float), D[mk].to_numpy(float), D.tarih, 100, rng)
                B["kontrol"].append({"kontrol": f"{faz}_{kk}", "donem": dn, "auc": au[0], "auc_alt": au[1], "auc_ust": au[2], "n": int(D[mk].notna().sum())})
        # kalibrasyon (test, GBM ve LR)
        Dt = _cy_donem(Ef, tests[0][1], tests[-1][2])
        for mk in ("p_LR", "p_GBM", "Y_GC"):
            q = Dt[[mk, "y"]].dropna()
            if len(q) >= 50:
                q["dil"] = pd.qcut(q[mk].rank(method="first"), 10, labels=False)
                for k_, g in q.groupby("dil"):
                    B["kalibrasyon"].append({"faz": faz, "model": mk, "ondalik": int(k_), "tahmin": float(g[mk].mean()), "gercek": float(g.y.mean()), "n": len(g)})
        # kırılımlar: yıl, rejim, likidite (bütün adaylar ve GBM seçimi)
        spy = K.get("_endeks", pd.DataFrame()).get("SPY") if isinstance(K.get("_endeks"), pd.DataFrame) else None
        if spy is not None and len(spy.dropna()):
            sp = spy.dropna(); boga = (sp > sp.rolling(200).mean()).reindex(Ef.tarih.values, method="ffill").to_numpy()
            Ef["rejim"] = np.where(boga, "boga (SPY > SMA200)", "ayi (SPY < SMA200)")
        else:
            Ef["rejim"] = "bilinmiyor"
        Ef["likit_ucte"] = Ef.groupby(Ef.tarih.dt.year).log_dv20.transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=["dusuk", "orta", "yuksek"]))
        pg = esik.get("p_GBM", {}).get("p", np.nan)
        for kir, kol in (("yil", Ef.tarih.dt.year.astype(str)), ("rejim", Ef.rejim), ("likidite", Ef.likit_ucte.astype(str))):
            for v, g in Ef.groupby(kol):
                o = cy_ozet(g, K, rng); gt = g[(g.tarih >= tests[0][1]) & (g.p_GBM >= pg)] if np.isfinite(pg) else g.iloc[0:0]
                B["kirilim"].append({"faz": faz, "kirilim": kir, "deger": v, **o, "gbm_secilen_test_n": len(gt),
                                     "gbm_secilen_test_isabet": float(gt.y.mean()) if len(gt) else np.nan, "gbm_secilen_test_net": float(gt.net.mean()) if len(gt) else np.nan})
        # portföy: model seçimleri (test)
        takvim = pd.DatetimeIndex(sorted(P.tarih.unique()))
        for dn, a, b in tests:
            b2 = K["kriz"] if dn == "2024-26" else b
            for mk in ("p_LR", "p_GBM", "Y_GC", "Y_GL"):
                sc = esik.get(mk, {})
                if not np.isfinite(sc.get("p", np.nan)):
                    continue
                D = _cy_donem(Ef, a, b); D = D[D[mk] >= sc["p"]].sort_values(["tarih", mk], ascending=[True, False])
                po = cy_portfoy(H, [(t, s_, int(i_)) for t, s_, i_ in zip(D.tarih, D.sembol, D.i)], a, b2, "ABD", K, None, takvim)
                B["portfoy"].append({"pazar": "ABD", "donem": dn, "strateji": f"{faz}_{mk}", "sinyal_n": len(D), **{k: v for k, v in po.items() if k != "deger"}})
        Ef.drop(columns=[c for c in Ef if c.startswith("p_cikar_") or c.startswith("p_yalniz_")]).to_csv(os.path.join(A.cikti, f"cy_b_aday_{faz}.csv.gz"), index=False)
    # hacimli taban portföyü ve sektör yoğunlaşması
    takvim = pd.DatetimeIndex(sorted(P.tarih.unique()))
    for dn, a, b in tests:
        b2 = K["kriz"] if dn == "2024-26" else b; D = _cy_donem(E[E.tip == "HT"], a, b).sort_values(["tarih", "sembol"])
        po = cy_portfoy(H, [(t, s_, int(i_)) for t, s_, i_ in zip(D.tarih, D.sembol, D.i)], a, b2, "ABD", K, None, takvim)
        B["portfoy"].append({"pazar": "ABD", "donem": dn, "strateji": "HT_hepsi", "sinyal_n": len(D), **{k: v for k, v in po.items() if k != "deger"}})
    sek = cy_sektor(A, pd.DataFrame()); sk = []
    for tip in ("P1", "P2", "HT"):
        D = E[E.tip == tip].assign(sektor=lambda x: x.sembol.map(sek).fillna("bilinmiyor"))
        for Y, g in D.groupby(D.tarih.dt.year):
            pay = g.sektor.value_counts(normalize=True)
            sk.append({"kume": tip, "yil": int(Y), "n": len(g), "en_buyuk_sektor": pay.index[0], "en_buyuk_pay": float(pay.iloc[0]), "hhi": float((pay ** 2).sum()),
                       "bilinmiyor_pay": float(pay.get("bilinmiyor", 0.0))})
    # B8 çoklu test: test hücrelerindeki ana farklar
    for r in Hb[(Hb.donem.isin([t[0] for t in tests])) & Hb.kume.isin(["P1", "P2", "HT"]) & Hb.p.notna()].itertuples():
        B["coklu"].append({"test": f"{r.kume} {r.etiket} {r.donem} fark>0", "p": r.p})
    for r in B["katki"]:
        if np.isfinite(r.get("p", np.nan)):
            B["coklu"].append({"test": f"{r['faz']} {r['kiyas']} {r['donem']}", "p": r["p"]})
    for r in B["grup"]:
        if np.isfinite(r.get("p", np.nan)):
            B["coklu"].append({"test": f"{r['faz']} grup {r['grup']} {r['donem']}", "p": r["p"]})
    Cm = pd.DataFrame(B["coklu"])
    if len(Cm):
        Cm = Cm.sort_values("p").reset_index(drop=True); m = len(Cm)
        Cm["holm_p"] = np.minimum(1.0, np.maximum.accumulate([(m - k) * p for k, p in enumerate(Cm.p)]))
    # yazım
    T = {"hucre": Hb, "model": pd.DataFrame(B["model"]), "katki": pd.DataFrame(B["katki"]), "grup": pd.DataFrame(B["grup"]), "kontrol": pd.DataFrame(B["kontrol"]),
         "kirilim": pd.DataFrame(B["kirilim"]), "portfoy": pd.DataFrame(B["portfoy"]), "kalibrasyon": pd.DataFrame(B["kalibrasyon"]), "sektor": pd.DataFrame(sk), "coklu": Cm}
    for k, v in T.items():
        v.to_csv(os.path.join(A.cikti, f"cy_b_{k}.csv"), index=False)
    B["T"] = T; B["H_b"] = cy_hipotez_b(T, K)
    pd.DataFrame(B["H_b"]).to_csv(os.path.join(A.cikti, "cy_b_hipotez.csv"), index=False)
    return B


def cy_hipotez_b(T: Dict[str, pd.DataFrame], K: Dict[str, Any]) -> List[Dict[str, Any]]:
    """v1.1 önceden yazılı kabul kuralları."""
    tests = [t[0] for t in K["test"]]; out = []; fe = K["karar"]["fark"]; M = T["model"]; Kt = T["katki"]; G = T["grup"]; Hb = T["hucre"]

    def ekle(kod, ad, ok, ay):
        out.append({"kod": kod, "hipotez": ad, "karar": "ÖLÇÜLEMEDİ" if ok is None else ("DESTEKLENİYOR" if ok else "DESTEKLENMİYOR"), "ayrinti": ay})
    cs = [Hb[(Hb.kume == "HT") & (Hb.donem == dn) & (Hb.etiket == "sabit_20_10_60")] for dn in tests]
    ok = all(len(c) and cy_tutar(c.iloc[0].to_dict(), K) for c in cs) if all(len(c) for c in cs) else None
    ekle("B2", "Önceki aday 'ABD hacimli taban' üçlü bariyerde rastgeleden iyi", ok,
         "; ".join(f"{dn}: n {c.iloc[0].n}, isabet {c.iloc[0].isabet:.3f}, taban {c.iloc[0].taban:.3f}, fark {c.iloc[0].fark:+.3f} [{c.iloc[0].fark_alt:+.3f}], net {c.iloc[0].net:+.4f}"
                   for dn, c in zip(tests, cs) if len(c) and c.iloc[0].n))
    for et in ("oynak_s_0.5s_60",):
        cs = [Hb[(Hb.kume == "P1") & (Hb.donem == dn) & (Hb.etiket == et)] for dn in tests]
        ok = all(len(c) and cy_tutar(c.iloc[0].to_dict(), K) for c in cs) if all(len(c) for c in cs) else None
        ekle("B1", "P1 oynaklığa bağlı bariyerle rastgeleden iyi", ok, "; ".join(f"{dn}: n {c.iloc[0].n}, fark {c.iloc[0].fark:+.3f} [{c.iloc[0].fark_alt:+.3f}]" for dn, c in zip(tests, cs) if len(c) and c.iloc[0].n))
    for faz in ("P1", "P2"):
        q = M[(M.faz == faz) & (M.model == "p_LR") & M.donem.isin(tests)]
        ok = (len(q) == len(tests) and all((r.n_secilen or 0) >= K["karar"]["n_min"] and (r.isabet_fark or -1) >= fe and (r.isabet_fark_alt or -1) > 0 and (r.net_fark or -1) > 0
                                            for r in q.itertuples())) if len(q) else None
        ekle(f"B4-{faz}-LR", f"{faz}: lojistik referans modeli adayları iyileştiriyor", ok,
             "; ".join(f"{r.donem}: seçilen {r.n_secilen}/{r.n_hepsi}, precision {r.precision:.3f} (taban {r.taban_isabet:.3f}), AUC {r.roc_auc:.3f}, net fark {r.net_fark:+.4f}" for r in q.itertuples()))
        k = Kt[(Kt.faz == faz) & (Kt.kiyas == "GBM-LR")]; q2 = M[(M.faz == faz) & M.donem.isin(tests)]
        ok = (len(k) == len(tests) and all((r.alt or -1) > 0 for r in k.itertuples()) and all(
            (q2[(q2.model == "p_GBM") & (q2.donem == dn)].net_secilen.iloc[0] >= q2[(q2.model == "p_LR") & (q2.donem == dn)].net_secilen.iloc[0]) for dn in tests)) if len(k) == len(tests) else None
        ekle(f"B4-{faz}-GBM", f"{faz}: ağaç modeli lojistik modeli geçiyor", ok, "; ".join(f"{r.donem}: AUC farkı {r.fark:+.3f} [{r.alt:+.3f}, {r.ust:+.3f}]" for r in k.itertuples()))
        for kod, ad in (("CNN", "CNN katkısı [G,C]-[G]"), ("LSTM", "LSTM katkısı [G,L]-[G]")):
            k = Kt[(Kt.faz == faz) & (Kt.kiyas == ad)]
            ok = (all((r.alt or -1) > 0 for r in k.itertuples())) if len(k) == len(tests) and k.fark.notna().all() else None
            ekle(f"B4-{faz}-{kod}", f"{faz}: {kod} sayısal modelin üstüne bilgi ekliyor", ok, "; ".join(f"{r.donem}: {r.fark:+.3f} [{r.alt:+.3f}, {r.ust:+.3f}]" for r in k.itertuples()))
        for g in K["gruplar"]:
            k = G[(G.faz == faz) & (G.grup == g)]
            ok = all((r.alt or -1) > 0 for r in k.itertuples()) if len(k) == len(tests) and k.tam_eksi_cikarilmis.notna().all() else None
            ekle(f"B5-{faz}-{g}", f"{faz}: '{g}' özellik grubu ek bilgi taşıyor", ok,
                 "; ".join(f"{r.donem}: tam - çıkarılmış AUC {r.tam_eksi_cikarilmis:+.3f} [{r.alt:+.3f}], yalnız grup AUC {r.yalniz_auc:.3f}" for r in k.itertuples()))
    C = T["kontrol"]
    for kk, beklenen in (("negatif_karisik_etiket", "AUC ~0,5"), ("pozitif_gelecek5_sizinti", "AUC belirgin yüksek")):
        q = C[C.kontrol.str.endswith(kk)]
        ok = (all(abs(r.auc - 0.5) < 0.06 for r in q.itertuples()) if kk.startswith("negatif") else all(r.auc > 0.65 for r in q.itertuples())) if len(q) else None
        ekle(f"B7-{kk}", f"Kontrol: {kk} ({beklenen})", ok, "; ".join(f"{r.kontrol} {r.donem}: AUC {r.auc:.3f} [{r.auc_alt:.3f}, {r.auc_ust:.3f}]" for r in q.itertuples()))
    q = C[C.kontrol == "plasebo_P1_esli_rastgele"]
    ok = all(abs(r.fark) < fe for r in q[q.donem.isin(tests)].itertuples()) if len(q) else None
    ekle("B7-plasebo", "Kontrol: plasebo (aynı gün aynı oynaklık rastgele) farkı ~0", ok, "; ".join(f"{r.donem}: fark {r.fark:+.3f} [{r.fark_alt:+.3f}, {r.fark_ust:+.3f}] n {r.n}" for r in q.itertuples()))
    Cm = T["coklu"]
    if len(Cm):
        ekle("B8", "Çoklu test (Holm): düzeltme sonrası anlamlı (p < 0,05) testler", None,
             f"{int((Cm.holm_p < 0.05).sum())} / {len(Cm)} test; " + "; ".join(f"{r.test} (p {r.p:.3f}, Holm {r.holm_p:.3f})" for r in Cm[Cm.holm_p < 0.05].head(12).itertuples()))
    return out


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
    if R.get("B"):
        L += cy_rapor_b(R["B"], K)
    metin = "\n".join(L) + "\n"
    with open(os.path.join(A.cikti, "cy_rapor.md"), "w", encoding="utf-8") as fh:
        fh.write(metin)
    return metin


def cy_rapor_b(Bb: Dict[str, Any], K: Dict[str, Any]) -> List[str]:
    """v1.1 rapor bölümü (markdown satırları)."""
    T = Bb["T"]; f = lambda x, p=3: ("" if x is None or (isinstance(x, float) and not np.isfinite(x)) else (f"{x:+.{p}f}" if isinstance(x, float) else str(x)))
    L = ["", "## v1.1 — birleştirilmiş plan (model merdiveni, katkı, kontroller)", "", "| Kod | Hipotez | Karar | Ayrıntı |", "|---|---|---|---|"]
    L += [f"| {h['kod']} | {h['hipotez']} | **{h['karar']}** | {h['ayrinti']} |" for h in Bb["H_b"]]
    Hb = T["hucre"]; L += ["", "### Etiket türleri, belirsiz mumlar, hacimli taban", "", "| Küme | Dönem | Etiket | n | İsabet | Taban | Fark [alt] | Net | Belirsiz payı |", "|---|---|---|---|---|---|---|---|---|"]
    for r in Hb.itertuples():
        L.append(f"| {r.kume} | {r.donem} | {r.etiket} | {r.n} | {f(getattr(r, 'isabet', np.nan))} | {f(getattr(r, 'taban', np.nan))} | {f(getattr(r, 'fark', np.nan))} [{f(getattr(r, 'fark_alt', np.nan))}] | "
                 f"{f(getattr(r, 'net', np.nan), 4)} | {f(getattr(r, 'belirsiz_pay', np.nan), 3)} |")
    M = T["model"]; L += ["", "### Model merdiveni (seçim eşiği doğrulamada, 2021-22)", "",
                          "| Faz | Model | Dönem | Seçilen / hepsi | Precision | Taban | Recall | ROC-AUC [alt] | PR-AUC | Brier | Net seçilen | Net fark [alt] |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in M.itertuples():
        L.append(f"| {r.faz} | {r.model} | {r.donem} | {getattr(r, 'n_secilen', '')} / {r.n_hepsi} | {f(getattr(r, 'precision', np.nan))} | {f(getattr(r, 'taban_isabet', np.nan))} | "
                 f"{f(getattr(r, 'recall', np.nan))} | {f(getattr(r, 'roc_auc', np.nan))} [{f(getattr(r, 'roc_auc_alt', np.nan))}] | {f(getattr(r, 'pr_auc', np.nan))} | {f(getattr(r, 'brier', np.nan))} | "
                 f"{f(getattr(r, 'net_secilen', np.nan), 4)} | {f(getattr(r, 'net_fark', np.nan), 4)} [{f(getattr(r, 'net_fark_alt', np.nan), 4)}] |")
    for ad, kol in (("katki", ("faz", "kiyas", "donem", "n", "fark", "alt", "ust", "p")), ("grup", ("faz", "grup", "donem", "n", "tam_eksi_cikarilmis", "alt", "ust", "yalniz_auc")),
                    ("kontrol", None), ("portfoy", ("donem", "strateji", "sinyal_n", "toplam", "yillik", "mdd", "sharpe", "calmar", "islem_n", "kazanma", "ort_islem", "ort_kayip")),
                    ("sektor", None), ("kirilim", ("faz", "kirilim", "deger", "n", "isabet", "taban", "fark", "fark_alt", "net", "gbm_secilen_test_n", "gbm_secilen_test_isabet"))):
        Dt = T[ad]
        if not len(Dt):
            continue
        kol = [c for c in (kol or Dt.columns) if c in Dt.columns]
        L += ["", f"### {ad}", "", "| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
        for r in Dt[kol].itertuples(index=False):
            L.append("| " + " | ".join(f(v) if isinstance(v, float) else str(v) for v in r) + " |")
    L += ["", "### Notlar v1.1", ""] + [f"- {n}" for n in Bb.get("notlar", [])]
    return L


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
