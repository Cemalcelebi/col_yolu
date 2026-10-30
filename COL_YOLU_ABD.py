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

CY_SURUM = "CY v1.5 (2026-10-30, K54 tarihsel evren sağlamlık denetimi; v1.4 K53 bilgi direnci / analist dağınıklığı / karar gecikmesi; v1.3 K52 grafik izi + analist revizyonları: Yahoo not günlüğü, dört grup, H0-H6; v1.2 K51 sonrası bağımsız denetim: veri bütünlüğü, kırılganlık, eşleşmiş kontrollerle H-A..H-E; v1.1 K51 ABD Çöl Yolu: üçlü bariyer (sabit + oynaklık), meta-etiketleme, model merdiveni LR/GBM/CNN/LSTM, PBO/DSR, batanlar dahil)"
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
                "hacim": ("v10_50", "v20_120", "kir_hacim", "dus_hacim"),
                "akis": ("cmf20", "obv_egim20", "ad_egim20", "mfi14"),
                "trend": ("ema20_egim5", "ema20_egim20", "ema50_egim20", "c_ema20", "c_ema50", "c_sma200", "rsi14", "macd_hist"),
                "momentum_dusus": ("r5", "r20", "r60", "r120", "r250", "dd250", "konum250", "dip_bar250", "tepe_bar250", "dus_sure", "dus_atr",
                                   "dus_atr_gercek", "onceki_trend"),
                "likidite_piyasa": ("log_dv20", "piy_r20", "piy_r60"),
                "col": ("col_dusus", "col_konum", "col_savunma", "col_bant", "col_kucuk", "col_bb_ok", "col_doji_ok", "col_hacim_ok", "col_imza", "kir_pay",
                        "sikisma_gun")},
    "kir_basarisiz_gun": 10,
    "lr_C": 1.0,
    "lstm": {"gizli": 32, "epoch": 5, "sabir": 1, "batch": 512, "lr": 1e-3, "tohum": 52},
    "boot_auc": 300,
    "olay_kumeleri": ("P1", "P2", "ES", "HT"),
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
        yv = np.where(np.isfinite(sg), Tv.y.to_numpy(), np.nan); netv = Tv.brut.to_numpy() - mal; belv = Tv.belirsiz.to_numpy()
        pm = uygun & np.isfinite(T.y.to_numpy())
        pan = pd.DataFrame({"tarih": idx[pm], "i": np.flatnonzero(pm).astype(np.int32), "y": T.y.to_numpy()[pm].astype(np.float32),
                            "net": net[pm].astype(np.float32), "brut": T.brut.to_numpy()[pm].astype(np.float32),
                            "cikis": T.cikis.to_numpy()[pm].astype(np.int32), "yk": Tk.y.to_numpy()[pm].astype(np.float32),
                            "netk": netk[pm].astype(np.float32), "vol60": M["vol60"].to_numpy()[pm].astype(np.float32),
                            "r20": M["F"].r20.to_numpy()[pm].astype(np.float32), "r60": M["F"].r60.to_numpy()[pm].astype(np.float32),
                            "yv": yv[pm].astype(np.float32), "netv": netv[pm].astype(np.float32), "belirsiz": T.belirsiz.to_numpy()[pm].astype(np.int8), "belirsiz_v": belv[pm].astype(np.int8),
                            "log_dv20": M["F"].log_dv20.to_numpy()[pm].astype(np.float32)})
        olay = []
        for tip, ix in S.items():
            ix = ix[np.isfinite(T.y.to_numpy()[ix])] if len(ix) else ix
            if len(ix):
                olay.append(pd.DataFrame({"tip": tip, "i": ix.astype(np.int32)}))
        O = pd.concat(olay, ignore_index=True) if olay else pd.DataFrame(columns=["tip", "i"])
        # v1.1 denetim eki: başarısız kırılım (BİLGİ, gelecek bilgisi; özellik değil): P2'den sonraki 10 günde kapanış dünkü kutu tavanının altına
        tav_d = M["col"][K["col"]["L"]].tavan.shift(1).to_numpy(); Cn = d.Close.to_numpy(float); kb = K["kir_basarisiz_gun"]
        O["kir_basarisiz"] = [float(np.any(Cn[i + 1:i + 1 + kb] < tav_d[i])) if (t == "P2" and i + kb < len(Cn)) else np.nan for t, i in zip(O.tip, O.i)] if len(O) else []
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
        # v1.1 denetim ekleri (yalnız i ve öncesi): sıkışma süresi, düşüşün tepe günü ATR'sine oranı, düşüş sırasında hacim, düşüş öncesi trend
        cek = (cy_cekirdek(c, Kc["L"], K) & (c.dusus <= Kc["dusus"])).to_numpy(); sg_ = np.zeros(n)
        for k_ in range(n):
            sg_[k_] = sg_[k_ - 1] + 1 if (cek[k_] and k_ > 0) else float(cek[k_])
        Ha, La, Ca, Va = (d[k2].to_numpy(float) for k2 in ("High", "Low", "Close", "Volume"))
        trn = np.maximum(Ha - La, np.maximum(np.abs(Ha - np.r_[np.nan, Ca[:-1]]), np.abs(La - np.r_[np.nan, Ca[:-1]])))
        atr_abs = pd.Series(trn).ewm(alpha=1 / 14, adjust=False).mean().to_numpy(); tb = M["F"].tepe_bar250.to_numpy(); db = M["F"].dip_bar250.to_numpy()
        da, dh, ot = np.full(len(ii), np.nan), np.full(len(ii), np.nan), np.full(len(ii), np.nan)
        for j, i in enumerate(ii):
            if not (np.isfinite(tb[i]) and np.isfinite(db[i])):
                continue
            t_ = int(i - tb[i]); d_ = int(i - db[i])
            if d_ > t_ and atr_abs[t_] > 0:
                da[j] = (Ha[t_] - La[d_]) / atr_abs[t_]
                v0 = Va[max(0, t_ - 60):t_]
                if len(v0) >= 20 and np.nanmedian(v0) > 0:
                    dh[j] = np.nanmedian(Va[t_:d_ + 1]) / np.nanmedian(v0)
            if t_ >= 120 and Ca[t_ - 120] > 0:
                ot[j] = Ca[t_] / Ca[t_ - 120] - 1
        Fi["sikisma_gun"] = sg_[ii]; Fi["dus_atr_gercek"] = da; Fi["dus_hacim"] = dh; Fi["onceki_trend"] = ot
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
                "kayma": M["kayma"].to_numpy(np.float32), "T": T[["brut", "cikis"]].to_numpy(np.float64), "uygun": uygun.astype(bool)}
    except Exception as ex:
        cylog.warning("CY %s %s atlandı: %s", pz, s, ex)
        return None


# ---------------------------------------------------------------- Y4 TABAN / EŞ + İSTATİSTİK
def cy_panel_taban(P: pd.DataFrame) -> pd.DataFrame:
    """Aynı gün, aynı oynaklık ondalığı ortalamaları: e_y, e_net, e_yk, e_netk."""
    P = P.copy(); P["vd"] = np.minimum((P.groupby("tarih").vol60.rank(pct=True) * 10).fillna(5).astype(int), 9).astype(np.int8)
    w = P["agirlik"].astype(float) if "agirlik" in P else pd.Series(1.0, index=P.index); kk = [P.tarih, P.vd]

    def wort(v: pd.Series, m: Optional[pd.Series] = None) -> pd.Series:   # ağırlıklı (batan örneklemi 1,83) grup ortalaması, maskeli
        ww = w.where(v.notna() & (m if m is not None else True))
        return ((v * ww).groupby(kk).transform("sum") / ww.groupby(kk).transform("sum")).astype(np.float32)
    for c in [k for k in ("y", "net", "yk", "netk", "yv", "netv") if k in P]:
        P["e_" + c] = wort(P[c])
    if "belirsiz" in P:                                               # denetim: belirsizsiz kıyas için taban da belirsizsiz
        P["e_y_bs"] = wort(P.y, P.belirsiz == 0); P["e_net_bs"] = wort(P.net, P.belirsiz == 0)
    if "cikti" in P:                                                  # denetim: batansız kıyas için taban da batansız
        P["e_y_bt"] = wort(P.y, ~P.cikti.astype(bool)); P["e_net_bt"] = wort(P.net, ~P.cikti.astype(bool))
    return P


def cy_boot_fark(D: pd.DataFrame, kol: str, B: int, rng: np.random.Generator) -> Tuple[float, float, float]:
    """Ortalama ve ay kümeli bootstrap %95 aralığı (D: 'tarih' ve kol)."""
    v = D[kol].to_numpy(float); ok = np.isfinite(v); v = v[ok]
    if not len(v):
        return np.nan, np.nan, np.nan
    w = D["agirlik"].to_numpy(float)[ok] if "agirlik" in D else np.ones(len(v))          # batan örneklemi ağırlığı
    ay = (D.tarih.dt.year * 12 + D.tarih.dt.month).to_numpy()[ok]; ua, inv = np.unique(ay, return_inverse=True)
    sv = np.bincount(inv, v * w); sn = np.bincount(inv, w); Mn = len(ua); m0 = float(np.sum(v * w) / np.sum(w))
    if Mn < 3:
        return m0, np.nan, np.nan
    ix = rng.integers(0, Mn, (B, Mn)); bs = sv[ix].sum(1) / sn[ix].sum(1)
    return m0, float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))


def cy_boot_iki(A_: pd.DataFrame, B_: pd.DataFrame, kol: str, B: int, rng: np.random.Generator) -> Tuple[float, float, float]:
    """İki grup ortalama farkı (A - B), ayları birlikte yeniden örnekleyerek %95 aralık."""
    def ayla(D):
        ay = (D.tarih.dt.year * 12 + D.tarih.dt.month).to_numpy(); v = D[kol].to_numpy(float); ok = np.isfinite(v)
        w = D["agirlik"].to_numpy(float) if "agirlik" in D else np.ones(len(v))
        return pd.DataFrame({"ay": ay[ok], "sum": (v * w)[ok], "count": w[ok]}).groupby("ay")[["sum", "count"]].sum()
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
    w = D["agirlik"].to_numpy(float) if "agirlik" in D else np.ones(len(D))
    wm = lambda c: float(np.nansum(D[c].to_numpy(float) * w) / np.sum(w[np.isfinite(D[c].to_numpy(float))])) if np.isfinite(D[c].to_numpy(float)).any() else np.nan
    return {"n": int(len(D)), "isabet": wm(y), "taban": wm(ey), "fark": f, "fark_alt": a, "fark_ust": b,
            "net": wm(net), "net_taban": wm(en), "net_fark": fn, "net_fark_alt": an,
            "kazanma": float(np.mean(r > 0)), "ort_kazanc": float(np.mean(r[r > 0])) if (r > 0).any() else np.nan,
            "ort_kayip": float(np.mean(r[r <= 0])) if (r <= 0).any() else np.nan, "en_kotu": float(np.nanmin(r)),
            "medyan_gun": float(D.gun.median()) if "gun" in D else np.nan}


def cy_tutar(o: Dict[str, Any], K: Dict[str, Any]) -> bool:
    return bool(o.get("n", 0) >= K["karar"]["n_min"] and (o.get("fark") or -1) >= K["karar"]["fark"] and (o.get("fark_alt") or -1) > 0
                and (o.get("net_fark") or -1) > 0)


# ---------------------------------------------------------------- Y6 META-ETİKETLEME
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


def cy_beta(D: pd.Series, K: Dict[str, Any], pz: str) -> Dict[str, float]:
    """Portföy günlük getirisinin pazar endeksine (ABD SPY, AVR ^STOXX, BIST XU100) regresyonu: beta, yıllık alfa, alfa t."""
    En = K.get("_endeks", pd.DataFrame()); kod = (K["endeks"].get(pz) or (None,))[0]
    if D is None or not len(D) or kod is None or kod not in En:
        return {}
    r = D.pct_change(); e = En[kod].reindex(D.index).ffill().pct_change(); q = pd.concat([r, e], axis=1).dropna()
    if len(q) < 60 or q.iloc[:, 1].std() == 0:
        return {}
    x = q.iloc[:, 1].to_numpy(); y = q.iloc[:, 0].to_numpy(); b = np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1); a = y.mean() - b * x.mean()
    res = y - a - b * x; se = res.std(ddof=2) * np.sqrt(1 / len(y) + x.mean() ** 2 / np.sum((x - x.mean()) ** 2))   # kesişimin OLS standart hatası
    return {"beta": float(b), "alfa_yillik": float(a * 252), "alfa_t": float(a / se) if se > 0 else np.nan}


def cy_takvim(H: Dict[str, Dict[str, Any]]) -> pd.DatetimeIndex:
    """Bütün fiyat günleri (panel etiket kuyruğundan bağımsız; denetim düzeltmesi)."""
    return pd.DatetimeIndex(np.unique(np.concatenate([h["tarih"] for h in H.values()])))


def cy_piyasa(H: Dict[str, Dict[str, Any]], P: pd.DataFrame, bas: str, bit: str) -> Dict[str, Any]:
    """Eşit ağırlıklı likit piyasa: her gün, bir önceki gün likit (uygun) olan hisselerin günlük getirisi ortalaması. Fiyat serilerinden
    hesaplanır (etiketli panelden değil; denetim: panel kuyruğunda yalnız batan seriler kalıyordu)."""
    parca = []; a_, b_ = pd.Timestamp(bas), pd.Timestamp(bit)
    for s, h in H.items():
        ix = pd.DatetimeIndex(h["tarih"]); m = (ix >= a_ - pd.Timedelta(days=7)) & (ix <= b_)
        if not m.any():
            continue
        c = pd.Series(h["kapanis"].astype(float), index=ix)[m]; u = pd.Series(h["uygun"], index=ix)[m] if "uygun" in h else pd.Series(True, index=c.index)
        r = c.pct_change().where(u.shift(1, fill_value=False)); parca.append(r[(r.index >= a_)].rename(s))
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
    H = {r["sembol"]: {"tarih": r["tarih"], "kapanis": r["kapanis"], "acilis": r["acilis"], "kayma": r["kayma"], "T": r["T"], "uygun": r.get("uygun")} for r in sonuc}
    cikti = {r["sembol"]: bool(r.get("cikti_mi", False)) for r in sonuc}; ev0 = EV.set_index("sembol")
    P = pd.concat([r["panel"].assign(sembol=r["sembol"]) for r in sonuc if len(r["panel"])], ignore_index=True)
    P["tarih"] = pd.to_datetime(P.tarih); P["agirlik"] = P.sembol.map(ev0.agirlik).fillna(1.0).astype(np.float32); P["cikti"] = P.sembol.map(cikti).fillna(False)
    P = cy_panel_taban(P)
    piy = P.groupby("tarih").agg(piy_r20=("r20", "median"), piy_r60=("r60", "median"))
    ev = EV.set_index("sembol")
    olay = []
    for r in sonuc:
        if len(r["olay"]):
            o = r["olay"].copy(); o["sembol"] = r["sembol"]; olay.append(o)
    E = pd.concat(olay, ignore_index=True) if olay else pd.DataFrame(columns=["tip", "i", "sembol"])
    E["i"] = E.i.astype(int)
    ek = [c for c in ("yv", "netv", "e_yv", "e_netv", "belirsiz", "belirsiz_v", "e_y_bs", "e_net_bs", "e_y_bt", "e_net_bt", "log_dv20") if c in P]          # v1.1
    E = E.merge(P[["sembol", "i", "tarih", "y", "net", "brut", "cikis", "yk", "netk", "vol60", "vd", "e_y", "e_net", "e_yk", "e_netk"] + ek], on=["sembol", "i"], how="inner")
    E["gun"] = E.cikis - E.i
    E["cikis_tarih"] = [pd.Timestamp(H[s]["tarih"][min(int(c), len(H[s]["tarih"]) - 1)]) for s, c in zip(E.sembol, E.cikis)]
    E["batan"] = E.sembol.map(cikti).fillna(False).astype(bool); E["agirlik"] = E.sembol.map(ev.agirlik).fillna(1.0)   # batan = seri erken bitti (denetim)
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
    X["gun"] = X.cikis - X.i; X["batan"] = X.sembol.map(cikti).fillna(False).astype(bool)
    return {"H": H, "P": P, "E": E, "X": X, "resim": resim, "dizi": dizi, "pazar": pz}


def cy_olay_yaz(E: pd.DataFrame, cikti: str, pz: str, K: Dict[str, Any] = CY) -> Dict[str, int]:
    """Olay CSV'si (cy_olay_<pazar>.csv.gz): K['olay_kumeleri'] (P1, P2, ES, HT) eksiksiz yazılır; yazılan dosya geri okunup küme sayıları
    bellektekiyle karşılaştırılır (Cemal 29 Eki: HT kayıtları CSV'ye girmiyordu)."""
    X = E[E.tip.isin(K["olay_kumeleri"])].drop(columns=["vd"], errors="ignore"); yol = os.path.join(cikti, f"cy_olay_{pz}.csv.gz"); X.to_csv(yol, index=False)
    beklenen = X.tip.value_counts().to_dict(); okunan = pd.read_csv(yol, usecols=["tip"]).tip.value_counts().to_dict()
    if beklenen != okunan:
        raise RuntimeError(f"cy_olay_{pz}: yazılan küme sayıları tutmuyor: {beklenen} / {okunan}")
    eksik = [t for t in K["olay_kumeleri"] if t not in okunan and (E.tip == t).any()]
    if eksik:
        raise RuntimeError(f"cy_olay_{pz}: bellekte olup CSV'ye yazılmayan küme: {eksik}")
    cylog.info("cy_olay_%s yazıldı: %s", pz, okunan)
    return okunan


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
                    Dg = D[~D.batan].assign(e_y=lambda x: x.e_y_bt, e_net=lambda x: x.e_net_bt) if "e_y_bt" in D else D[~D.batan]   # taban da batansız
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
        takvim = cy_takvim(S["H"])
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
            rs_m["p90"] = float(np.quantile([r["toplam"] for r in rs], 0.90)) if rs else np.nan
            for ad, kol, s_ in (("P1_hepsi", None, None), ("P1_META", "meta_p", R["meta_secim"]), ("P1_GENEL", "genel_p", sec_g), ("P1_CNN", "cnn_p", sec_c), ("P2_hepsi", None, None)):
                tip = "P2" if ad.startswith("P2") else "P1"; D = _cy_donem(S["X"][S["X"].tip == tip], a, b)
                if kol is not None:
                    if not np.isfinite((s_ or {}).get("p", np.nan)):
                        continue
                    D = D[D[kol] >= s_["p"]].sort_values(["tarih", kol], ascending=[True, False])
                else:
                    D = D.sample(frac=1.0, random_state=K["karar"]["tohum"]).sort_values("tarih", kind="stable")   # aynı gün: tohumlu rastgele sıra
                po = cy_portfoy(S["H"], [(t, s_, int(i_)) for t, s_, i_ in zip(D.tarih, D.sembol, D.i)], a, b2, pz, K, None, takvim)
                R["portfoy"].append({"pazar": pz, "donem": dn, "strateji": ad, "sinyal_n": len(D), **{k: v for k, v in po.items() if k != "deger"},
                                     "piyasa_toplam": piy["toplam"], "piyasa_mdd": piy["mdd"], "rastgele_toplam": rs_m.get("toplam"), "rastgele_mdd": rs_m.get("mdd"),
                                     "rastgele_kazanma": rs_m.get("kazanma"), "rastgele_ort_islem": rs_m.get("ort_islem"), "rastgele_p90": rs_m.get("p90"),
                                     **ek, **cy_beta(po["deger"], K, pz)})
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
        cy_olay_yaz(S["E"], A.cikti, pz, K)
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
    return {"n": int(len(y)), "fark": float(d0), "alt": float(np.quantile(bs, 0.025)), "ust": float(np.quantile(bs, 0.975)), "p": float((np.sum(bs <= 0) + 1) / (len(bs) + 1))}


def cy_boot_p(D: pd.DataFrame, kol: str, B: int, rng: np.random.Generator) -> float:
    """Tek yönlü bootstrap p: ay kümeli ortalamanın <= 0 olma payı."""
    v = D[kol].to_numpy(float); ok = np.isfinite(v); v = v[ok]
    if len(v) < 10:
        return np.nan
    ay = (D.tarih.dt.year * 12 + D.tarih.dt.month).to_numpy()[ok]; ua, inv = np.unique(ay, return_inverse=True)
    sv = np.bincount(inv, v); sn = np.bincount(inv).astype(float); ix = rng.integers(0, len(ua), (B, len(ua)))
    return float((np.sum(sv[ix].sum(1) / sn[ix].sum(1) <= 0) + 1) / (B + 1))


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


def cy_eslesik_portfoy(H: Dict[str, Dict[str, Any]], D: pd.DataFrame, P: pd.DataFrame, a: str, b2: str, pz: str, K: Dict[str, Any], takvim: pd.DatetimeIndex,
                       tohum: int, n: int = 20) -> Dict[str, float]:
    """Eşleşik rastgele portföy (denetim): her sinyal yerine AYNI gün AYNI oynaklık ondalığından rastgele likit hisse; aynı kurallar. Ortanca ve %90."""
    gr = P.groupby(["tarih", "vd"]).indices; rng = np.random.default_rng(tohum); top = []
    for _ in range(n):
        gir = []
        for t, v in zip(D.tarih, D.vd):
            ix = gr.get((t, v))
            if ix is not None and len(ix):
                r = P.iloc[ix[rng.integers(0, len(ix))]]; gir.append((t, r.sembol, int(r.i)))
        top.append(cy_portfoy(H, gir, a, b2, pz, K, None, takvim)["toplam"])
    return {"eslesik_rastgele": float(np.nanmedian(top)) if top else np.nan, "eslesik_rastgele_p90": float(np.nanquantile(top, 0.9)) if top else np.nan}


def cy_boot_kume(D: pd.DataFrame, kol: str, B: int, rng: np.random.Generator) -> Tuple[float, float]:
    """Duyarlılık (denetim): hisse x çeyrek kümeli bootstrap %95 aralığı (aynı hissenin çakışan etiketleri aynı kümede)."""
    v = D[kol].to_numpy(float); ok = np.isfinite(v)
    if ok.sum() < 10:
        return np.nan, np.nan
    kume = (D.sembol.astype(str) + "|" + D.tarih.dt.to_period("Q").astype(str)).to_numpy()[ok]; ua, inv = np.unique(kume, return_inverse=True)
    w = D["agirlik"].to_numpy(float)[ok] if "agirlik" in D else np.ones(ok.sum())
    sv = np.bincount(inv, v[ok] * w); sn = np.bincount(inv, w); ix = rng.integers(0, len(ua), (B, len(ua))); bs = sv[ix].sum(1) / sn[ix].sum(1)
    return float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))


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
    for pz_, tip in [("ABD", t) for t in ("P1", "P2", "ES", "HT")] + [(p_, "HT") for p_ in SON if p_ != "ABD"] + [(p_, "P1") for p_ in SON if p_ != "ABD"]:
        Ez = SON[pz_]["E"]
        for dn, a, b in donemler:
            D = _cy_donem(Ez[Ez.tip == tip], a, b)
            if pz_ == "ABD" and tip == "P1" and len(D) and "agirlik" in D:      # batan örneklemi ağırlıklı (1,83) fark
                w = D.agirlik.to_numpy(float); f_ = (D.y - D.e_y).to_numpy(float)
                B["hucre"].append({"pazar": pz_, "kume": "P1_agirlikli", "donem": dn, "etiket": "sabit_20_10_60", "n": len(D), "fark": float(np.average(f_, weights=w)),
                                   "net": float(np.average(D.net.to_numpy(float), weights=w)), "isabet": float(np.average(D.y.to_numpy(float), weights=w))})
            for et, kol in (("sabit_20_10_60", ("y", "net", "e_y", "e_net")), ("oynak_s_0.5s_60", ("yv", "netv", "e_yv", "e_netv"))):
                if kol[0] not in D:
                    continue
                Dk = D.rename(columns={kol[0]: "_y", kol[1]: "_n", kol[2]: "_ey", kol[3]: "_en"})[["tarih", "_y", "_n", "_ey", "_en", "gun", "agirlik"]].rename(
                    columns={"_y": "y", "_n": "net", "_ey": "e_y", "_en": "e_net"}).dropna(subset=["y"])
                o = cy_ozet(Dk, K, rng); o["p"] = cy_boot_p(Dk.assign(_f=Dk.y - Dk.e_y), "_f", K["karar"]["boot"], rng) if len(Dk) else np.nan
                if len(Dk) >= 10 and "sembol" in D:
                    o["fark_alt_hisse_ceyrek"], o["fark_ust_hisse_ceyrek"] = cy_boot_kume(Dk.assign(sembol=D.loc[Dk.index, "sembol"], _f=Dk.y - Dk.e_y), "_f", 1000, rng)
                B["hucre"].append({"pazar": pz_, "kume": tip, "donem": dn, "etiket": et, **o})
            if "belirsiz" in D and len(D):
                Db = D[D.belirsiz == 0].assign(e_y=lambda x: x.e_y_bs, e_net=lambda x: x.e_net_bs)     # taban da belirsizsiz (denetim)
                B["hucre"].append({"pazar": pz_, "kume": tip + "_belirsizsiz", "donem": dn, "etiket": "sabit_20_10_60", "belirsiz_pay": float(D.belirsiz.mean()), **cy_ozet(Db, K, rng)})
            if tip == "P2" and "kir_basarisiz" in D and D.kir_basarisiz.notna().any():
                for v_, g_ in D.groupby("kir_basarisiz"):
                    B["hucre"].append({"pazar": pz_, "kume": "P2_basarisiz_kirilim" if v_ == 1 else "P2_suren_kirilim", "donem": dn, "etiket": "sabit_20_10_60 (BİLGİ: gelecek)", **cy_ozet(g_, K, rng)})
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
    sek = cy_sektor(A, pd.DataFrame())
    if len(sek):
        Ps = P[["tarih", "sembol", "r60"]].assign(sektor=P.sembol.map(sek)); sm = Ps.dropna(subset=["sektor"]).groupby(["tarih", "sektor"]).r60.median()
        pm_ = Ps.groupby("tarih").r60.median(); X["_sektor"] = X.sembol.map(sek)
        ix_ = pd.MultiIndex.from_arrays([X.tarih, X._sektor.fillna("?")])
        X["ruzgar"] = np.where(X._sektor.isna(), "sektör bilinmiyor", np.where((sm.reindex(ix_).to_numpy() - pm_.reindex(X.tarih).to_numpy()) >= 0.10, "rüzgâr var", "rüzgâr yok"))
    else:
        X["ruzgar"] = "sektör bilinmiyor"
    pbo_m = {}
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
        aylar_v = pd.period_range(K["dogrulama"][0], K["dogrulama"][1], freq="M")
        for mk in ("p_LR", "p_GBM10", "p_GBM", "cnn_p", "lstm_p"):      # denetim: doğrulamada kurulan yığmalar PBO'ya girmez
            q = dgm[dgm[mk].notna()]
            for pay in K["meta"]["pay"]:
                if len(q):
                    Sx = q[q[mk] >= q[mk].quantile(1 - pay)]
                    pbo_m[f"{faz}|{mk}|{pay}"] = Sx.groupby(Sx.tarih.dt.to_period("M")).net.mean().reindex(aylar_v).fillna(0.0).to_numpy()
        esik_g = {g: cy_esik_sec(dgm[dgm[f"p_cikar_{g}"].notna()], f"p_cikar_{g}", K, f"{faz}_cikar_{g}")[0] for g in K["gruplar"]}
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
                oc = cy_secim_olc(D, f"p_cikar_{g}", esik_g[g].get("p", np.nan), K, rng); ot_ = cy_secim_olc(D, "p_GBM", esik.get("p_GBM", {}).get("p", np.nan), K, rng)
                B["grup"].append({"faz": faz, "grup": g, "donem": dn, "tam_eksi_cikarilmis": f["fark"], "alt": f["alt"], "ust": f["ust"], "p": f["p"],
                                  "yalniz_auc": yal[0], "yalniz_auc_alt": yal[1], "n": f["n"], "net_tam": ot_.get("net_secilen"), "net_cikarilmis": oc.get("net_secilen"),
                                  "precision_tam": ot_.get("precision"), "precision_cikarilmis": oc.get("precision")})
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
        for kir, kol in (("yil", Ef.tarih.dt.year.astype(str)), ("rejim", Ef.rejim), ("likidite", Ef.likit_ucte.astype(str)), ("sektor_ruzgari", Ef.ruzgar)):
            for v, g in Ef.groupby(kol):
                o = cy_ozet(g, K, rng); gt = g[(g.tarih >= tests[0][1]) & (g.p_GBM >= pg)] if np.isfinite(pg) else g.iloc[0:0]
                B["kirilim"].append({"faz": faz, "kirilim": kir, "deger": v, **o, "gbm_secilen_test_n": len(gt),
                                     "gbm_secilen_test_isabet": float(gt.y.mean()) if len(gt) else np.nan, "gbm_secilen_test_net": float(gt.net.mean()) if len(gt) else np.nan})
        # portföy: model seçimleri (test)
        takvim = cy_takvim(H)
        for dn, a, b in tests:
            b2 = K["kriz"] if dn == "2024-26" else b
            for mk in ("p_LR", "p_GBM", "Y_GC", "Y_GL"):
                sc = esik.get(mk, {})
                if not np.isfinite(sc.get("p", np.nan)):
                    continue
                D = _cy_donem(Ef, a, b); D = D[D[mk] >= sc["p"]].sort_values(["tarih", mk], ascending=[True, False])
                po = cy_portfoy(H, [(t, s_, int(i_)) for t, s_, i_ in zip(D.tarih, D.sembol, D.i)], a, b2, "ABD", K, None, takvim)
                B["portfoy"].append({"pazar": "ABD", "donem": dn, "strateji": f"{faz}_{mk}", "sinyal_n": len(D), **{k: v for k, v in po.items() if k != "deger"},
                                     **cy_beta(po["deger"], K, "ABD"), **cy_eslesik_portfoy(H, D, P, a, b2, "ABD", K, takvim, 7000 + len(B["portfoy"]))})
        Ef.drop(columns=[c for c in Ef if c.startswith("p_cikar_") or c.startswith("p_yalniz_")]).to_csv(os.path.join(A.cikti, f"cy_b_aday_{faz}.csv.gz"), index=False)
    # hacimli taban portföyü ve sektör yoğunlaşması
    takvim = cy_takvim(H)
    for dn, a, b in tests:
        b2 = K["kriz"] if dn == "2024-26" else b; D = _cy_donem(E[E.tip == "HT"], a, b).sort_values(["tarih", "sembol"])
        po = cy_portfoy(H, [(t, s_, int(i_)) for t, s_, i_ in zip(D.tarih, D.sembol, D.i)], a, b2, "ABD", K, None, takvim)
        B["portfoy"].append({"pazar": "ABD", "donem": dn, "strateji": "HT_hepsi", "sinyal_n": len(D), **{k: v for k, v in po.items() if k != "deger"},
                             **cy_beta(po["deger"], K, "ABD"), **cy_eslesik_portfoy(H, D, P, a, b2, "ABD", K, takvim, 8000 + len(B["portfoy"]))})
        for tip in ("P1", "P2"):                                     # birincil kuralın kendisi de eşleşik rastgeleyle
            D = _cy_donem(E[E.tip == tip], a, b).sample(frac=1.0, random_state=K["karar"]["tohum"]).sort_values("tarih", kind="stable")
            po = cy_portfoy(H, [(t, s_, int(i_)) for t, s_, i_ in zip(D.tarih, D.sembol, D.i)], a, b2, "ABD", K, None, takvim)
            B["portfoy"].append({"pazar": "ABD", "donem": dn, "strateji": f"{tip}_hepsi", "sinyal_n": len(D), **{k: v for k, v in po.items() if k != "deger"},
                                 **cy_beta(po["deger"], K, "ABD"), **cy_eslesik_portfoy(H, D, P, a, b2, "ABD", K, takvim, 9000 + len(B["portfoy"]))})
    sk = []
    Mpm = np.column_stack(list(pbo_m.values())) if pbo_m else np.zeros((0, 0))
    B["pbo_model"] = {**(cy_pbo(Mpm, 8) if Mpm.size else {"pbo": np.nan}), "aday_sayisi": len(pbo_m), "ay": int(Mpm.shape[0]) if Mpm.size else 0}
    for tip in ("P1", "P2", "HT"):
        D = E[E.tip == tip].assign(sektor=lambda x: x.sembol.map(sek).fillna("bilinmiyor"))
        for Y, g in D.groupby(D.tarih.dt.year):
            pay = g.sektor.value_counts(normalize=True)
            sk.append({"kume": tip, "yil": int(Y), "n": len(g), "en_buyuk_sektor": pay.index[0], "en_buyuk_pay": float(pay.iloc[0]), "hhi": float((pay ** 2).sum()),
                       "bilinmiyor_pay": float(pay.get("bilinmiyor", 0.0))})
    # B8 çoklu test: test hücrelerindeki ana farklar
    for r in Hb[(Hb.donem.isin([t[0] for t in tests])) & Hb.kume.isin(["P1", "P2", "HT"]) & Hb.p.notna()].itertuples():
        B["coklu"].append({"test": f"{r.pazar} {r.kume} {r.etiket} {r.donem} fark>0", "p": r.p})
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
         "kirilim": pd.DataFrame(B["kirilim"]), "portfoy": pd.DataFrame(B["portfoy"]), "kalibrasyon": pd.DataFrame(B["kalibrasyon"]), "sektor": pd.DataFrame(sk), "coklu": Cm,
         "pbo_model": pd.DataFrame([B["pbo_model"]])}
    for k, v in T.items():
        v.to_csv(os.path.join(A.cikti, f"cy_b_{k}.csv"), index=False)
    B["T"] = T; B["H_b"] = cy_hipotez_b({**T, "portfoy_v10": R["tablolar"]["portfoy"]}, K)
    pd.DataFrame(B["H_b"]).to_csv(os.path.join(A.cikti, "cy_b_hipotez.csv"), index=False)
    return B


def cy_hipotez_b(T: Dict[str, pd.DataFrame], K: Dict[str, Any]) -> List[Dict[str, Any]]:
    """v1.1 önceden yazılı kabul kuralları."""
    tests = [t[0] for t in K["test"]]; out = []; fe = K["karar"]["fark"]; M = T["model"]; Kt = T["katki"]; G = T["grup"]; Hb = T["hucre"]
    Hb = Hb[Hb.pazar == "ABD"] if "pazar" in Hb else Hb

    def ekle(kod, ad, ok, ay):
        out.append({"kod": kod, "hipotez": ad, "karar": "ÖLÇÜLEMEDİ" if ok is None else ("DESTEKLENİYOR" if ok else "DESTEKLENMİYOR"), "ayrinti": ay})
    cs = [Hb[(Hb.kume == "HT") & (Hb.donem == dn) & (Hb.etiket == "sabit_20_10_60")] for dn in tests]
    ok = all(len(c) and cy_tutar(c.iloc[0].to_dict(), K) for c in cs) if all(len(c) for c in cs) else None
    ekle("B2", "Önceki aday 'ABD hacimli taban' üçlü bariyerde rastgeleden iyi", ok,
         "; ".join(f"{dn}: n {c.iloc[0].n}, isabet {c.iloc[0].isabet:.3f}, taban {c.iloc[0].taban:.3f}, fark {c.iloc[0].fark:+.3f} [{c.iloc[0].fark_alt:+.3f}], net {c.iloc[0].net:+.4f}"
                   for dn, c in zip(tests, cs) if len(c) and c.iloc[0].n))
    for kod, kume, et, ad in (("B1", "P1", "oynak_s_0.5s_60", "P1 oynaklığa bağlı bariyerle rastgeleden iyi"),
                              ("B1-P2", "P2", "oynak_s_0.5s_60", "P2 oynaklığa bağlı bariyerle rastgeleden iyi"),
                              ("B1-belirsiz", "P1_belirsizsiz", "sabit_20_10_60", "P1 belirsiz mumlar çıkarılınca da rastgeleden iyi (sıra uydurulmadan)")):
        cs = [Hb[(Hb.kume == kume) & (Hb.donem == dn) & (Hb.etiket == et)] for dn in tests]
        ok = all(len(c) and cy_tutar(c.iloc[0].to_dict(), K) for c in cs) if all(len(c) for c in cs) else None
        ekle(kod, ad, ok, "; ".join(f"{dn}: n {c.iloc[0].n}, fark {c.iloc[0].fark:+.3f} [{c.iloc[0].fark_alt:+.3f}]" + (f", belirsiz payı {c.iloc[0].belirsiz_pay:.3f}" if "belirsiz_pay" in c and np.isfinite(c.iloc[0].get("belirsiz_pay", np.nan)) else "")
                                     for dn, c in zip(tests, cs) if len(c) and c.iloc[0].n))
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
        # merdiven zinciri: birincil -> LR -> GBM -> CNN -> LSTM; ilk tutmayan basamakta durulur
        d_ = {h["kod"]: h["karar"] for h in out}; zin = ["birincil kural"]
        for kod in (f"B4-{faz}-LR", f"B4-{faz}-GBM", f"B4-{faz}-CNN", f"B4-{faz}-LSTM"):
            if d_.get(kod) == "DESTEKLENİYOR":
                zin.append(kod.split("-")[-1])
            else:
                break
        ekle(f"B4-{faz}-ZİNCİR", f"{faz}: sisteme alınan en üst model basamağı (karmaşık model yalnız bir alttakini geçerse)", None, " -> ".join(zin))
    # sıkı portföy: GBM / yığma seçimi hem eşit ağırlıklı piyasayı, hem rastgele %90 dilimini, hem SPY'yi iki test döneminde geçer
    Pb = T["portfoy"]; P0 = T.get("portfoy_v10", pd.DataFrame())
    for st in ("P1_hepsi", "P2_hepsi", "P1_p_GBM", "P1_Y_GC", "P2_p_GBM", "HT_hepsi"):
        q = Pb[Pb.strateji == st] if len(Pb) else Pb
        if not len(q) or not len(P0):
            ekle(f"B9-{st}", f"Sıkı portföy {st}", None, "yok"); continue
        sat = []; ok = len(q) == len(tests)
        for r in q.itertuples():
            b0 = P0[(P0.pazar == "ABD") & (P0.donem == r.donem)].iloc[0]
            spy = b0.get("endeks_SPY", np.nan); rp = getattr(r, "eslesik_rastgele_p90", np.nan)     # sinyal günlerine eşleşik rastgele %90
            ok = ok and bool(r.toplam > b0.piyasa_toplam and r.toplam > (rp if np.isfinite(rp) else -9) and r.toplam > (spy if np.isfinite(spy) else -9))
            sat.append(f"{r.donem}: {r.toplam:+.1%} (MDD {r.mdd:.1%}, Sharpe {getattr(r, 'sharpe', np.nan):.2f}, beta {getattr(r, 'beta', np.nan):.2f}, alfa {getattr(r, 'alfa_yillik', np.nan):+.1%}) "
                       f"| piyasa {b0.piyasa_toplam:+.1%}, eşleşik rastgele p90 {rp:+.1%}, SPY {spy:+.1%}")
        ekle(f"B9-{st}", f"Sıkı portföy: {st} piyasa, eşleşik rastgele %90 ve SPY'yi geçiyor", ok, "; ".join(sat))
    pm_ = T.get("pbo_model", pd.DataFrame())
    if len(pm_):
        r = pm_.iloc[0]; ok = (r.pbo < 0.5) if np.isfinite(r.get("pbo", np.nan)) else None
        ekle("B8-PBO-model", "Model x seçim payı seçiminde aşırı uyum riski düşük (PBO < 0,5; doğrulama ayları, 8 blok)", ok,
             f"PBO {r.get('pbo', np.nan):.2f}, {int(r.get('aday_sayisi', 0))} aday, {int(r.get('ay', 0))} ay")
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


# ---------------------------------------------------------------- v1.2 K51 SONRASI BAĞIMSIZ DENETİM (Cemal 29 Eki; ön kayıt commit 8e99902:
# arastirma_cikti/col_yolu_abd/K51_v12_onkayit.md). K51 kararı değişmez; yeni model yok. Veri bütünlüğü (V1-V8), kırılganlık, eşleşmiş
# kontrollerle beş hipotez (H-A..H-E), tekrar üretim. Çıktılar: K51_VERI_DENETIMI.md, K51_KIRILGANLIK.md, K51_ESLESMIS_KONTROL.csv,
# K51_HIPOTEZ_KARARLARI.csv, K51_TEKRAR_URETIM.md.
CY_V12: Dict[str, Any] = {
    "tohum": 512, "boot": 2000, "k": 5, "k_es": 3, "dd_tol": 0.10, "gun_tol": 10, "fark_esik": 0.05, "n_min": 30,
    "uzak": ("dd250", "vol60", "log_dv20", "r60", "ar20"), "delist_senaryo": (-0.30, 0.0, -1.0), "eski_commit": "b3835d8", "kes_gun": 120,
    "donem": (("2016-22", "2016-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-06-05")),
    "yillar": ((2023, "2023-01-01", "2023-12-31"), (2024, "2024-01-01", "2024-12-31"), (2025, "2025-01-01", "2025-12-31"), (2026, "2026-01-01", "2026-06-05")),
    "batma_r60": -0.50, "batma_fiyat": 1.0, "ileri_dogrulama": "2026-09-01",
}
_CY_ESKI_NS: Dict[str, Any] = {}


def cy_v12_tekil(EV: pd.DataFrame) -> None:
    """Sembol tekilliği: aynı pazarda aynı sembol iki kez evrene giremez (kod yeniden kullanımı ayrı sütunda raporlanır)."""
    yin = EV[EV.duplicated(["pazar", "sembol"], keep=False)]
    if len(yin):
        raise RuntimeError(f"evrende yinelenen sembol: {sorted(set(yin.sembol))[:10]}")


def cy_v12_hisse(arg: Tuple[Any, ...]) -> Optional[Dict[str, Any]]:
    """Bir hisse (v1.2): likit günlerin paneli (özellikler, etiketler, olay bayrakları, delist / ham fiyat / kod kesme senaryoları)."""
    pz, s, d, ev, likesik, K, ham, kes = arg
    try:
        Kc = K["col"]; Lw = Kc["L"]; M = cy_olculer(d, K, (Lw,)); n = len(d); idx = d.index; F = M["F"]
        min_dv = K["likit"].get(pz)
        uygun = (M["dv20"] >= likesik.reindex(idx).ffill().to_numpy()).to_numpy() & (d.Close.to_numpy() >= K["fiyat_min"].get(pz, 0.0))
        if min_dv:
            uygun &= (M["dv20"] >= min_dv).to_numpy()
        uygun &= (idx >= pd.Timestamp(ev["evren_bas"])) & (idx >= pd.Timestamp(K["egitim"][0])) & (np.arange(n) >= 260)
        c = M["col"][Lw]; cek_ham = (cy_cekirdek(c, Lw, K).to_numpy() & (c.dusus.to_numpy() <= Kc["dusus"]) & uygun)
        im = cy_imza(c, Kc["kucuk"]).to_numpy(); C = d.Close.to_numpy(float)
        CEK = _cy_aralik(np.flatnonzero(cek_ham), Kc["ayri"]); P1 = _cy_aralik(np.flatnonzero(cek_ham & (im >= Kc["imza_min"])), Kc["ayri"])
        ES = _cy_aralik(np.flatnonzero(cek_ham & (im <= Kc["es_imza_max"])), Kc["ayri"]); tav = c.tavan.to_numpy(); p2 = []
        for i0 in P1:
            for j in range(i0 + 1, min(i0 + Kc["kirilim_gun"], n - 1) + 1):
                if C[j] > tav[i0] * Kc["kirilim_pay"]:
                    if uygun[j]:
                        p2.append(j)
                    break
        P2 = _cy_aralik(np.array(sorted(set(p2)), dtype=int), Kc["ayri"])
        Kh = K["ht"]; Vv = d.Volume.astype(float); medv = Vv.shift(1).rolling(Kh["pencere"], min_periods=int(0.8 * Kh["pencere"])).median()
        r1 = d.Close / d.Close.shift(1) - 1
        HT = _cy_aralik(np.flatnonzero(((Vv >= Kh["kat"] * medv) & (medv > 0) & (r1 <= Kh["esik"])).to_numpy() & uygun), Kh["ayri"])
        cikti_mi = bool(idx[-1] < pd.Timestamp(K["alive_sinir"])); tb = K["tb"]
        T = cy_uclu_bariyer(d, tb["ust"], tb["alt"], tb["ufuk"], cikti_mi, K)
        mal = 2 * (K["komisyon"][pz] + M["kayma"].to_numpy())
        pm = uygun & np.isfinite(T.y.to_numpy()); ii = np.flatnonzero(pm)
        bayrak = lambda ix: np.isin(ii, ix)
        P = pd.DataFrame({"tarih": idx[ii], "i": ii.astype(np.int32), "y": T.y.to_numpy()[ii].astype(np.float32), "brut": T.brut.to_numpy()[ii].astype(np.float32),
                          "net": (T.brut.to_numpy() - mal)[ii].astype(np.float32), "cikis": T.cikis.to_numpy()[ii].astype(np.int32),
                          "belirsiz": T.belirsiz.to_numpy()[ii].astype(np.int8), "mal": mal[ii].astype(np.float32),
                          "vol60": F.vol60.to_numpy()[ii].astype(np.float32), "log_dv20": F.log_dv20.to_numpy()[ii].astype(np.float32),
                          "dd250": F.dd250.to_numpy()[ii].astype(np.float32), "r60": F.r60.to_numpy()[ii].astype(np.float32),
                          "ar20": F.ar20.to_numpy()[ii].astype(np.float32), "trend": (F.c_sma200.to_numpy()[ii] > 0).astype(np.int8),
                          "hacim_ok": c.hacim_ok.to_numpy()[ii].astype(np.int8), "imza": im[ii].astype(np.int8), "cek_ham": cek_ham[ii],
                          "CEK": bayrak(CEK), "P1": bayrak(P1), "ES": bayrak(ES), "P2": bayrak(P2), "HT": bayrak(HT)})
        # V5 delist senaryoları (yalnız seri erken bitenlerde fark eder)
        for sn in K["_v12"]["delist_senaryo"]:
            ad = f"y_d{int(round(-sn * 100))}"
            if cikti_mi and sn != K["delist_kayip"]:
                Ts = cy_uclu_bariyer(d, tb["ust"], tb["alt"], tb["ufuk"], True, {**K, "delist_kayip": sn})
                P[ad] = Ts.y.to_numpy()[ii].astype(np.float32); P["net" + ad[1:]] = (Ts.brut.to_numpy() - mal)[ii].astype(np.float32)
            else:
                P[ad] = P.y; P["net" + ad[1:]] = P.net
        # V6 ham fiyat etiketi (Tiingo)
        P["y_ham"] = np.nan
        if ham is not None:
            h = ham.reindex(idx)
            if h.Close.notna().mean() > 0.95:
                h = h.ffill().bfill(); Th = cy_uclu_bariyer(h, tb["ust"], tb["alt"], tb["ufuk"], cikti_mi, K); P["y_ham"] = Th.y.to_numpy()[ii].astype(np.float32)
        # V8 kod yeniden kullanımı: seri son bildirim + 120 günde kesilir
        P["y_kes"] = P.y; P["net_kes"] = P.net; P["kes_gecerli"] = True; kes_uygulandi = False
        if kes is not None and idx[-1] > kes:
            dk = d[idx <= kes]
            if len(dk) >= 70:
                Tk = cy_uclu_bariyer(dk, tb["ust"], tb["alt"], tb["ufuk"], True, K).reindex(idx)
                P["y_kes"] = Tk.y.to_numpy()[ii].astype(np.float32); P["net_kes"] = (Tk.brut.to_numpy() - mal)[ii].astype(np.float32)
                P["kes_gecerli"] = (idx[ii] <= kes); kes_uygulandi = True
        return {"pazar": pz, "sembol": s, "panel": P, "cikti_mi": cikti_mi, "ilk": idx[0], "son": idx[-1], "son_kapanis": float(C[-1]),
                "r60_son": float(C[-1] / C[max(0, n - 61)] - 1), "n_gun": n, "kes_uygulandi": kes_uygulandi}
    except Exception as ex:
        cylog.warning("v1.2 %s %s atlandı: %s", pz, s, ex)
        return None


def _cy_v12_eski_isci(arg: Tuple[Any, ...]) -> Optional[Dict[str, Any]]:
    return _CY_ESKI_NS["cy_hisse_isle"](arg)


def cy_v12_eslestir(P: pd.DataFrame, olay: pd.DataFrame, havuz: pd.DataFrame, K: Dict[str, Any], k: int, gun_tol: int,
                    rng: np.random.Generator, es_imza: bool = False) -> pd.DataFrame:
    """Eşleşmiş kontrol (ön kayıt 4): aynı gün (±gun_tol işlem günü), aynı oynaklık ondalığı ve likidite üçte biri, |dd250 farkı| <= dd_tol,
    aynı trend işareti, sektör biliniyorsa aynı sektör, hisse farklı; en yakın k (standartlaştırılmış uzaklık). Yalnız sinyal günü bilinen bilgi."""
    V12 = K["_v12"]; uz = list(V12["uzak"]); sd = P[uz].astype(float).std().fillna(1.0).replace(0, 1.0).to_numpy(float)
    gunler = np.array(sorted(P.tarih.unique())); gix = {g: i for i, g in enumerate(gunler)}
    hv = havuz.sort_values("tarih"); hg = hv.tarih.map(gix).to_numpy(); hx = hv[uz].to_numpy(float); hvd = hv["vd"].to_numpy(); hlt = hv["lt"].to_numpy()
    htr = hv.trend.to_numpy(); hsk = hv.sektor.to_numpy(); hsm = hv.sembol.to_numpy(); hy = hv.y.to_numpy(float); hn = hv.net.to_numpy(float)
    him = hv.imza_h.to_numpy() if es_imza else None; hid = hv.index.to_numpy(); out = []
    for r in olay.itertuples():
        g = gix.get(r.tarih)
        if g is None:
            out.append((0, np.nan, np.nan, "")); continue
        a, b = np.searchsorted(hg, g - gun_tol), np.searchsorted(hg, g + gun_tol, side="right")
        m = (hvd[a:b] == r.vd) & (hlt[a:b] == r.lt) & (htr[a:b] == r.trend) & (np.abs(hx[a:b, 0] - r.dd250) <= V12["dd_tol"]) & (hsm[a:b] != r.sembol)
        if isinstance(r.sektor, str) and r.sektor != "bilinmiyor":
            m &= hsk[a:b] == r.sektor
        if es_imza:
            m &= him[a:b] == r.imza_h
        cand = np.flatnonzero(m)
        if not len(cand):
            out.append((0, np.nan, np.nan, "")); continue
        x = hx[a:b][cand]; e = np.array([getattr(r, u) for u in uz], float)
        dist = np.sqrt(np.nansum(((x - e) / sd) ** 2, axis=1)); sec = cand[np.argsort(dist, kind="stable")[:k]]
        out.append((len(sec), float(np.nanmean(hy[a:b][sec])), float(np.nanmean(hn[a:b][sec])), ";".join(f"{hsm[a:b][j]}@{int(hid[a:b][j])}" for j in sec)))
    return pd.DataFrame(out, columns=["kontrol_n", "kontrol_y", "kontrol_net", "kontrol_kimlik"], index=olay.index)


def cy_v12_hucre(D: pd.DataFrame, K: Dict[str, Any], rng: np.random.Generator, ycol: str = "y", ncol: str = "net", kycol: str = "kontrol_y",
                 kncol: str = "kontrol_net") -> Dict[str, Any]:
    """Olay - kontrol farkı: n, isabet, kontrol, fark, ay kümeli ve hisse x çeyrek kümeli %95 aralık, net fark (+ aralık), tek yönlü p."""
    D = D[D[kycol].notna() & D[ycol].notna()]
    if not len(D):
        return {"n": 0}
    X = D.assign(_f=D[ycol] - D[kycol], _fn=D[ncol] - D[kncol]); B = K["_v12"]["boot"]
    f, a, b = cy_boot_fark(X, "_f", B, rng); fn, an, bn = cy_boot_fark(X, "_fn", B, rng); ka, kb = cy_boot_kume(X, "_f", 1000, rng)
    w = X["agirlik"].to_numpy(float) if "agirlik" in X else np.ones(len(X)); wm = lambda c: float(np.average(X[c].to_numpy(float), weights=w))
    return {"n": int(len(D)), "hisse_n": int(D.sembol.nunique()), "isabet": wm(ycol), "kontrol": wm(kycol), "fark": f, "fark_alt": a, "fark_ust": b,
            "fark_alt_hisse_ceyrek": ka, "fark_ust_hisse_ceyrek": kb, "net": wm(ncol), "kontrol_net": wm(kncol), "net_fark": fn, "net_fark_alt": an,
            "net_fark_ust": bn, "p": cy_boot_p(X, "_f", B, rng), "medyan_net": float(X[ncol].median()), "brut": float(X.brut.mean()) if "brut" in X else np.nan}


def cy_v12_karar(h: Dict[str, Any], K: Dict[str, Any]) -> str:
    V12 = K["_v12"]
    if h.get("n", 0) < V12["n_min"]:
        return "YETERSİZ ÖRNEKLEM"
    if h["fark"] >= V12["fark_esik"] and h["fark_alt"] > 0 and h["net_fark"] > 0:
        return "TUTAR"
    if h["fark"] <= -V12["fark_esik"] and h["fark_ust"] < 0:
        return "TERS YÖN"
    return "TUTMAZ"


def cy_v12_eski_kod(Vs_abd: Dict[str, pd.DataFrame], EV: pd.DataFrame, A: CYAyar, K: Dict[str, Any], rng: np.random.Generator) -> Tuple[pd.DataFrame, str]:
    """V7: ön kayıt commit'indeki (b3835d8) kod aynı veride koşulur (CNN yok); olay sayıları ve P1 / P2 / ES / HT hücreleri. Dönüş (tablo, not)."""
    import subprocess
    kok = os.path.dirname(os.path.abspath(globals().get("__file__", "COL_YOLU_ABD.py"))) or "."
    r = subprocess.run(["git", "-C", kok, "show", f"{K['_v12']['eski_commit']}:COL_YOLU_ABD.py"], capture_output=True, text=True)
    if r.returncode != 0:
        return pd.DataFrame(), f"eski kod alınamadı (git show {K['_v12']['eski_commit']}): {r.stderr.strip()[:200]}"
    import types
    mod = types.ModuleType("cy_eski"); sys.modules["cy_eski"] = mod                 # dataclass, sınıfın modülünü sys.modules'ta arar
    ns: Dict[str, Any] = mod.__dict__; ns.update({"get_ipython": None, "__file__": os.path.join(kok, "COL_YOLU_ABD.py")})
    exec(compile(r.stdout, "COL_YOLU_ABD_eski.py", "exec"), ns); _CY_ESKI_NS.clear(); _CY_ESKI_NS.update(ns)
    Ke = {**ns["CY"], "_havuz_p": {"ABD": {}}}; le = ns["cy_likit_esik"](Vs_abd, "ABD", Ke); evp = EV[EV.pazar == "ABD"].set_index("sembol")
    args = [("ABD", s, d, evp.loc[s].to_dict(), le, Ke, False, zlib.crc32(f"ABD|{s}".encode())) for s, d in Vs_abd.items() if s in evp.index]
    import multiprocessing as mp
    with mp.get_context("fork").Pool(max(1, A.is_parcacigi)) as hv:
        son = [x for x in hv.imap_unordered(_cy_v12_eski_isci, args, chunksize=8) if x is not None]
    S = ns["cy_birlestir"](son, EV[EV.pazar == "ABD"], "ABD", Ke); E = S["E"]; rows = []
    for tip in ("P1", "P2", "ES", "HT"):
        for dn, a, b in K["_v12"]["donem"]:
            D = E[(E.tip == tip) & (E.tarih >= a) & (E.tarih <= b)]; o = ns["cy_ozet"](D, Ke, rng)
            rows.append({"kod": "eski_" + K["_v12"]["eski_commit"], "kume": tip, "donem": dn, "n": o.get("n"), "isabet": o.get("isabet"), "taban": o.get("taban"),
                         "fark": o.get("fark"), "fark_alt": o.get("fark_alt"), "net": o.get("net"), "net_fark": o.get("net_fark")})
    _CY_ESKI_NS.clear()
    return pd.DataFrame(rows), f"eski kod {K['_v12']['eski_commit']} aynı veride yeniden koşuldu ({len(son)} hisse); CNN / LSTM / meta koşulmadı (olay ve taban kıyası)"


def cy_v12_calistir(A: Optional[CYAyar] = None, K: Dict[str, Any] = CY) -> Dict[str, Any]:
    """v1.2 sürücü: panel -> veri denetimi -> kırılganlık -> eşleştirme + hipotezler -> çıktılar. Yalnız ABD (hipotezler); evren tablosu üç pazar."""
    import hashlib, subprocess
    A = A or CYAyar(); os.makedirs(A.cikti, exist_ok=True); K = {**K, "_v12": CY_V12}; V12 = CY_V12; t0 = time.time()
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    rng = np.random.default_rng(V12["tohum"]); cy_veri_hazirla(A); Vs, EV = cy_veri_yukle(A, K); cy_v12_tekil(EV); K["_endeks"] = cy_endeks(A, K)
    # K34 kimlikleri, son SEC bildirimi, Tiingo ham fiyat
    kev = pd.read_csv(os.path.join(A.veri, "k34_evren.csv")) if os.path.exists(os.path.join(A.veri, "k34_evren.csv")) else pd.DataFrame(columns=["cik", "sembol", "kaynak"])
    son_bild = {}
    yb = os.path.join(A.veri, "k34_bildirim.pkl")
    if os.path.exists(yb) and len(kev):
        Bd = pd.read_pickle(yb); Bd = Bd.assign(cik=pd.to_numeric(Bd.cik, errors="coerce")).dropna(subset=["cik"])      # CIK türü: metin -> sayı
        sb = Bd.groupby(Bd.cik.astype(np.int64)).filed.max(); kv1 = kev.drop_duplicates("sembol", keep="first")          # yüklenen şirket = ilk satır
        son_bild = {s_: sb.get(int(c)) for c, s_ in zip(kv1.cik, kv1.sembol) if int(c) in sb.index}
        cylog.info("v1.2 son SEC bildirimi eşleşen K34 şirketi: %d / %d", len(son_bild), len(kv1))
    tk = A.tiingo or os.path.join(A.veri, "tiingo"); V = Vs["ABD"]; le = cy_likit_esik(V, "ABD", K); evp = EV[EV.pazar == "ABD"].set_index("sembol")
    def ham_oku(s_):
        yol = os.path.join(tk, f"{s_}.csv")
        if not os.path.exists(yol):
            return None
        t = pd.read_csv(yol)
        if not len(t) or "close" not in t:
            return None
        t.index = pd.to_datetime(t.date.str[:10]).astype("datetime64[ns]"); h = t[["open", "high", "low", "close", "volume"]].astype(float); h.columns = ["Open", "High", "Low", "Close", "Volume"]
        return h[~h.index.duplicated(keep="last")]
    args = []
    for s_, d in V.items():
        if s_ not in evp.index:
            continue
        ev = evp.loc[s_].to_dict(); kes = None
        if ev["kaynak"].startswith("K34") and son_bild.get(s_) is not None and pd.notna(son_bild[s_]):
            kes = pd.Timestamp(son_bild[s_]) + pd.Timedelta(days=V12["kes_gun"])
        args.append(("ABD", s_, d, ev, le, K, ham_oku(s_) if ev["kaynak"] == "K34_tiingo" else None, kes))
    import multiprocessing as mp
    with mp.get_context("fork").Pool(max(1, A.is_parcacigi)) as hv:
        son = [x for x in hv.imap_unordered(cy_v12_hisse, args, chunksize=8) if x is not None]
    cylog.info("v1.2 panel: %d hisse (%ds)", len(son), time.time() - t0)
    P = pd.concat([r["panel"].assign(sembol=r["sembol"]) for r in son if len(r["panel"])], ignore_index=True)
    P["tarih"] = pd.to_datetime(P.tarih).astype("datetime64[ns]"); P["agirlik"] = P.sembol.map(evp.agirlik).fillna(1.0).astype(np.float32)
    P["kaynak"] = P.sembol.map(evp.kaynak); sek = cy_sektor(A, EV); P["sektor"] = P.sembol.map(sek).fillna("bilinmiyor")
    P["vd"] = np.minimum((P.groupby("tarih").vol60.rank(pct=True) * 10).fillna(5).astype(int), 9).astype(np.int8)
    P["lt"] = np.minimum((P.groupby("tarih").log_dv20.rank(pct=True) * 3).fillna(1).astype(int), 2).astype(np.int8)
    P["imza_h"] = (P.imza - P.hacim_ok).astype(np.int8)
    for c_ in ("y", "y_d30", "y_d0", "y_d100", "y_kes"):                      # K51 tabanı (aynı gün aynı ondalık, ağırlıklı) her senaryoda
        ww = P.agirlik.where(P[c_].notna()); P["e_" + c_] = ((P[c_] * ww).groupby([P.tarih, P.vd]).transform("sum") / ww.groupby([P.tarih, P.vd]).transform("sum")).astype(np.float32)
    En = K.get("_endeks", pd.DataFrame())
    if isinstance(En, pd.DataFrame) and "SPY" in En:
        sp = En["SPY"].dropna(); boga = (sp > sp.rolling(200).mean()).reindex(P.tarih.values, method="ffill").to_numpy()
        P["rejim"] = np.where(boga, "BOĞA", "AYI")
    else:
        P["rejim"] = "bilinmiyor"
    meta = {r["sembol"]: r for r in son}
    # ---------------- V1-V8 veri denetimi
    satir = []
    for s_, r in meta.items():
        ev = evp.loc[s_]; sb = son_bild.get(s_); cik = kev.loc[kev.sembol == s_, "cik"].tolist()
        tur = "işlem görüyor"
        if r["cikti_mi"]:
            tur = "batma benzeri" if (r["r60_son"] <= V12["batma_r60"] or r["son_kapanis"] < V12["batma_fiyat"]) else ("satın alma / birleşme benzeri" if r["r60_son"] >= 0 else "belirsiz çıkış")
        suphe = bool(ev.kaynak.startswith("K34") and sb is not None and pd.notna(sb) and r["son"] > pd.Timestamp(sb) + pd.Timedelta(days=V12["kes_gun"]) and not r["cikti_mi"])
        bild_suruyor = bool(sb is not None and pd.notna(sb) and pd.Timestamp(sb) >= pd.Timestamp(K["kriz"]) - pd.Timedelta(days=120))
        satir.append({"sembol": s_, "cik": ";".join(str(c) for c in cik) if cik else "", "cik_sayisi": len(cik), "kaynak": ev.kaynak, "evren_bas": ev.evren_bas, "sec_bildirimi_suruyor": bild_suruyor,
                      "dayanak": "seri başı" if ev.kaynak == "V_ABD" else "ilk SEC nakit pisti bildirimi", "ilk_fiyat": r["ilk"], "son_fiyat": r["son"], "n_gun": r["n_gun"],
                      "son_kapanis": r["son_kapanis"], "r60_son": r["r60_son"], "seri_erken_bitti": r["cikti_mi"], "cikis_turu_tahmin": tur, "son_sec_bildirimi": sb,
                      "kod_yeniden_kullanim_suphesi": suphe, "kes_uygulandi": r["kes_uygulandi"], "agirlik": float(ev.agirlik),
                      "likit_gun": int((P.sembol == s_).sum())})
    EVT = pd.DataFrame(satir); EVT.to_csv(os.path.join(A.cikti, "K51_EVREN_PIT.csv"), index=False)
    yin = kev[kev.sembol.duplicated(keep=False)].sort_values("sembol") if len(kev) else pd.DataFrame()
    # V5 / V6 / V8 hücreleri ve V7 eski kod
    def hucre_taban(D, ycol, ecol, ncol):
        if not len(D):
            return {"n": 0}
        X = D.assign(_f=D[ycol] - D[ecol]); f, a, b = cy_boot_fark(X, "_f", V12["boot"], rng); w = X.agirlik.to_numpy(float)
        return {"n": int(len(X)), "isabet": float(np.average(X[ycol], weights=w)), "taban": float(np.average(X[ecol], weights=w)), "fark": f, "fark_alt": a, "fark_ust": b,
                "net": float(np.average(X[ncol], weights=w))}
    sen = []
    for tip in ("P1", "P2", "HT"):
        Et = P[P[tip]]
        for dn, a, b in V12["donem"]:
            D = Et[(Et.tarih >= a) & (Et.tarih <= b)]
            for ad, yc, ec, nc in (("ana (-%30)", "y", "e_y", "net"), ("delist %0", "y_d0", "e_y_d0", "net_d0"), ("delist -%100", "y_d100", "e_y_d100", "net_d100"),
                                   ("V8 kod kesme", "y_kes", "e_y_kes", "net_kes")):
                Dd = D[D.kes_gecerli] if ad.startswith("V8") else D
                sen.append({"kume": tip, "donem": dn, "senaryo": ad, **hucre_taban(Dd, yc, ec, nc), "etkilenen_olay": int((Dd[nc] != Dd.net).sum()),
                            "seri_sonunda_cikan_olay": int(Dd.sembol.map(lambda z: meta[z]["cikti_mi"]).to_numpy().astype(bool).sum())})
    SEN = pd.DataFrame(sen)
    hm = P[P.y_ham.notna()]; ham_t = {"satir": int(len(hm)), "uyum": float((hm.y_ham == hm.y).mean()) if len(hm) else np.nan,
                                     "olay_satir": int(hm[hm.P1 | hm.P2 | hm.HT].shape[0]), "olay_uyum": float((hm[hm.P1 | hm.P2 | hm.HT].y_ham == hm[hm.P1 | hm.P2 | hm.HT].y).mean()) if (hm.P1 | hm.P2 | hm.HT).any() else np.nan,
                                     "hisse": int(hm.sembol.nunique())}
    try:
        ESK, esk_not = cy_v12_eski_kod(V, EV, A, K, rng)
    except Exception as ex:
        ESK, esk_not = pd.DataFrame(), f"eski kod koşulamadı: {ex}"
    yeni = []
    for tip in ("P1", "P2", "ES", "HT"):
        for dn, a, b in V12["donem"]:
            D = P[P[tip] & (P.tarih >= a) & (P.tarih <= b)]; o = hucre_taban(D, "y", "e_y", "net")
            yeni.append({"kod": "yeni_v1.2", "kume": tip, "donem": dn, **{k_: o.get(k_) for k_ in ("n", "isabet", "taban", "fark", "fark_alt", "net")}})
    ESKYENI = pd.concat([ESK, pd.DataFrame(yeni)], ignore_index=True)
    # ---------------- kırılganlık
    kir = []
    for tip in ("P1", "P2", "HT"):
        Et = P[P[tip]]
        for dn, a, b in V12["donem"]:
            D = Et[(Et.tarih >= a) & (Et.tarih <= b)]
            for ky, g in [("hepsi", D)] + list(D.groupby("kaynak")):
                kir.append({"kume": tip, "kirilim": "kaynak", "deger": ky, "donem": dn, **hucre_taban(g, "y", "e_y", "net")})
            if len(D) >= 30:
                kat = (D.y - D.e_y).groupby(D.sembol).sum().sort_values(ascending=False); top20 = set(kat.head(20).index)
                kir.append({"kume": tip, "kirilim": "en_iyi_20_hisse_cikarildi", "deger": ",".join(list(top20)[:20]), "donem": dn, **hucre_taban(D[~D.sembol.isin(top20)], "y", "e_y", "net")})
                hs = (D.y - D.e_y).groupby(D.sembol).mean()
                kir.append({"kume": tip, "kirilim": "hisse_basina_esit_agirlik", "deger": f"{len(hs)} hisse", "donem": dn, "n": int(len(D)), "fark": float(hs.mean()),
                            "fark_alt": float(hs.mean() - 1.96 * hs.std() / np.sqrt(len(hs))), "fark_ust": float(hs.mean() + 1.96 * hs.std() / np.sqrt(len(hs)))})
                top = kat[kat > 0]; tpl = float(kat.sum())
                kir.append({"kume": tip, "kirilim": "katki_payi", "deger": f"ilk10 {top.head(10).sum() / tpl if tpl else np.nan:.2f}, ilk20 {top.head(20).sum() / tpl if tpl else np.nan:.2f}, ilk50 {top.head(50).sum() / tpl if tpl else np.nan:.2f} (toplam fark / n = {tpl / len(D):+.3f})",
                            "donem": dn, "n": int(len(D))})
            for rj, g in D.groupby("rejim"):
                kir.append({"kume": tip, "kirilim": "rejim", "deger": rj, "donem": dn, **hucre_taban(g, "y", "e_y", "net")})
        for yl, a, b in V12["yillar"]:
            D = Et[(Et.tarih >= a) & (Et.tarih <= b)]
            kir.append({"kume": tip, "kirilim": "yil", "deger": f"{yl}{' (kısmi)' if yl == 2026 else ''}", "donem": str(yl), **hucre_taban(D, "y", "e_y", "net")})
        # örtüşme
        Es = Et.sort_values(["sembol", "tarih"]); ayni_h = Es.groupby("sembol").tarih.diff().dt.days.le(90).mean() if len(Es) else np.nan
        gun_say = Et.groupby("tarih").size()
        kir.append({"kume": tip, "kirilim": "ortusme", "deger": f"aynı hissede 90 takvim günü içinde tekrar payı {ayni_h:.3f}; aynı günde >1 sinyal olan gün payı {(gun_say > 1).mean():.3f}; gün başına ortalama {gun_say.mean():.2f}",
                    "donem": "hepsi", "n": int(len(Et))})
    KIR = pd.DataFrame(kir)
    # ---------------- H-A..H-E eşleşmiş kontroller
    P["cek_any"] = P.cek_ham; genel = P[~P.cek_any]; esd = P[P.ES]; hed = []
    def olaylar(mask):
        return P[mask].copy()
    HA = olaylar(P.CEK); HB = olaylar(P.P1); HC = olaylar(P.CEK & (P.hacim_ok == 1)); HD = olaylar(P.HT); HE = olaylar(P.P1)
    cylog.info("v1.2 eşleştirme: H-A %d, H-B %d, H-C %d, H-D %d", len(HA), len(HB), len(HC), len(HD))
    MA = cy_v12_eslestir(P, HA, genel, K, V12["k"], 0, rng); MB = cy_v12_eslestir(P, HB, esd, K, V12["k_es"], V12["gun_tol"], rng)
    MC = cy_v12_eslestir(P, HC, P[P.CEK & (P.hacim_ok == 0)], K, V12["k_es"], V12["gun_tol"], rng, es_imza=True)
    MD = cy_v12_eslestir(P, HD, genel, K, V12["k"], 0, rng); ME = cy_v12_eslestir(P, HE, genel, K, V12["k"], 0, rng)
    # H-D bağımsızlık: HT'den önceki 60 işlem gününde aynı hissede ÇEK var mı
    cek_g = P[P.CEK].groupby("sembol").i.apply(lambda v: np.sort(v.to_numpy())); bag = []
    for r in HD.itertuples():
        v = cek_g.get(r.sembol); bag.append(bool(v is not None and np.any((v < r.i) & (v >= r.i - 60))))
    HD["ht_oncesi_cek"] = bag
    ESL = []
    for kod, O, M_ in (("H-A", HA, MA), ("H-B", HB, MB), ("H-C", HC, MC), ("H-D", HD, MD), ("H-E", HE, ME)):
        X = pd.concat([O, M_], axis=1); X["hipotez"] = kod; X["donem"] = ""
        for dn, a, b in V12["donem"]:
            X.loc[(X.tarih >= a) & (X.tarih <= b), "donem"] = dn
        ESL.append(X)
    ESL = pd.concat(ESL, ignore_index=True)
    kol = ["hipotez", "sembol", "tarih", "i", "donem", "rejim", "kaynak", "sektor", "vd", "lt", "dd250", "vol60", "log_dv20", "r60", "ar20", "trend", "imza", "hacim_ok",
           "y", "net", "brut", "mal", "belirsiz", "e_y", "kontrol_n", "kontrol_y", "kontrol_net", "kontrol_kimlik", "agirlik"] + (["ht_oncesi_cek"] if "ht_oncesi_cek" in ESL else [])
    ESL[kol].to_csv(os.path.join(A.cikti, "K51_ESLESMIS_KONTROL.csv.gz"), index=False)
    # hipotez hücreleri ve kararlar
    HK = []; p23 = {}
    for kod, ad in (("H-A", "sert düşüş + yataylaşma (ÇEK) > eşleşmiş genel kontrol"), ("H-B", "P1 (küçük mum imzaları) > ÇEK içi imzasız eşler (ES)"),
                    ("H-C", "ÇEK + hacim kuruması > ÇEK hacim kurumasız (öteki imzalar eşit)"), ("H-D", "hacimli taban (HT) > eşleşmiş genel kontrol; bağımsızlık"), ("H-E", "P1 rejime göre (AYI / BOĞA) > eşleşmiş genel kontrol")):
        X = ESL[ESL.hipotez == kod]; eslesme = {"olay": int(len(X)), "eslesmeyen_pay": float((X.kontrol_n == 0).mean()), "eksik_eslesme_pay (1-4)": float(((X.kontrol_n > 0) & (X.kontrol_n < (V12["k"] if kod in ("H-A", "H-D", "H-E") else V12["k_es"]))).mean()),
                                             "kapsanan_pay": float((X.kontrol_n > 0).mean())}
        kim = X.kontrol_kimlik.str.split(";").explode(); kim = kim[kim.notna() & (kim != "")]
        eslesme["kontrol_tekrar_kullanim_pay"] = float(1 - kim.nunique() / len(kim)) if len(kim) else np.nan
        hucreler = [("tum", X)] if kod != "H-E" else [(rj, X[X.rejim == rj]) for rj in ("AYI", "BOĞA")]
        for alt, Xh in hucreler:
            kararlar = []
            for dn, a, b in V12["donem"]:
                h = cy_v12_hucre(Xh[(Xh.tarih >= a) & (Xh.tarih <= b)], K, rng); kr = cy_v12_karar(h, K) if h.get("n", 0) else "YETERSİZ ÖRNEKLEM"
                HK.append({"hipotez": kod, "tanim": ad, "hucre": alt, "donem": dn, "birincil_olcut": "isabet farkı (olay - eşleşmiş kontrol), ağırlıklı", "asgari_etki": V12["fark_esik"],
                           **h, "karar_hucre": kr, **eslesme, **({"ht_oncesi_cek_pay": float(Xh.ht_oncesi_cek.mean())} if kod == "H-D" and len(Xh) else {})})
                kararlar.append(kr)
            h23 = cy_v12_hucre(Xh[(Xh.tarih >= "2023-01-01")], K, rng); p23[(kod, alt)] = h23.get("p", np.nan)
            HK.append({"hipotez": kod, "tanim": ad, "hucre": alt, "donem": "2023-26 (Holm için)", **h23, "karar_hucre": cy_v12_karar(h23, K) if h23.get("n", 0) else "YETERSİZ ÖRNEKLEM", **eslesme})
            if "YETERSİZ ÖRNEKLEM" in kararlar:
                son_k = "YETERSİZ ÖRNEKLEM"
            elif all(k_ == "TUTAR" for k_ in kararlar):
                son_k = "DESTEKLENİYOR (KEŞİFSEL; 2023-26 bağımsız değil)"
            elif any(k_ == "TERS YÖN" for k_ in kararlar):
                son_k = "DESTEKLENMİYOR (TERS YÖN en az bir dönemde)"
            else:
                son_k = "DESTEKLENMİYOR"
            if kod == "H-D" and len(Xh) and float(Xh.ht_oncesi_cek.mean()) >= 0.5:
                son_k += "; HT bağımsız değil (ÇEK ile örtüşme >= %50)"
            HK.append({"hipotez": kod, "tanim": ad, "hucre": alt, "donem": "KARAR", "karar_hucre": son_k, "donem_kararlari": " | ".join(f"{d_[0]}: {k_}" for d_, k_ in zip(V12["donem"], kararlar))})
    # Holm (aile = 5 hipotez; H-E için iki rejimin küçüğü)
    pl = {}
    for (kod, alt), p in p23.items():
        pl[kod] = min(pl.get(kod, 1.0), p if np.isfinite(p) else 1.0)
    sr = sorted(pl.items(), key=lambda x: x[1]); m = len(sr); holm = {}; cum = 0.0
    for r_, (kod, p) in enumerate(sr):
        cum = max(cum, (m - r_) * p); holm[kod] = min(1.0, cum)
    HKd = pd.DataFrame(HK); HKd["holm_p_2023_26"] = HKd.hipotez.map(holm); HKd["holm_gecer"] = HKd.holm_p_2023_26 < 0.05
    HKd["hiyerarsi"] = HKd.hipotez.map({"H-A": "ana", "H-B": "H-A altında", "H-C": "H-A altında", "H-D": "bağımsız", "H-E": "bağımsız"})
    HKd.to_csv(os.path.join(A.cikti, "K51_HIPOTEZ_KARARLARI.csv"), index=False)
    # ---------------- yazım
    R = {"P_n": int(len(P)), "hisse": int(P.sembol.nunique()), "EVT": EVT, "yinelenen": yin, "SEN": SEN, "ham": ham_t, "ESKYENI": ESKYENI, "esk_not": esk_not, "KIR": KIR,
         "HK": HKd, "holm": holm, "ESL_n": int(len(ESL)), "sure_dk": round((time.time() - t0) / 60, 1), "EV": EV, "evp_n": {k_: int(v) for k_, v in EV[EV.pazar == "ABD"].kaynak.value_counts().items()}}
    cy_v12_yaz(R, A, K); return R


def cy_v12_yaz(R: Dict[str, Any], A: CYAyar, K: Dict[str, Any]) -> None:
    """K51_VERI_DENETIMI.md, K51_KIRILGANLIK.md, K51_TEKRAR_URETIM.md."""
    import hashlib, subprocess
    TAM = {"n", "n_a", "n_b", "hisse", "hisse_a", "hisse_b", "analist_kaydi_olan_hisse", "kayit", "deger"}
    def f(x, p=3, tam=False):
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            return ""
        if isinstance(x, (float, np.floating)):
            return str(int(round(x))) if tam else f"{x:+.{p}f}"
        return str(x)
    def tablo(D: pd.DataFrame, kol: List[str]) -> List[str]:
        kol = [c for c in kol if c in D.columns]; L = ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
        for r in D[kol].itertuples(index=False):
            L.append("| " + " | ".join(f(v, tam=(c in TAM)) for c, v in zip(kol, r)) + " |")
        return L
    EVT = R["EVT"]; V12 = K["_v12"]
    L = ["# K51 — VERİ BÜTÜNLÜĞÜ DENETİMİ (v1.2, ön kayıt 8e99902)", "", "K51 kararı değişmez. Bu belge veri evreninin sınırlarını belgeler.", "",
         "## V1 Sayı uzlaşması", "", "| Sayı | Değer | Açıklama |", "|---|---|---|",
         f"| İşlenen tekil sembol (ABD) | {len(EVT)} | V_ABD {R['evp_n'].get('V_ABD')} + K34 Yahoo {R['evp_n'].get('K34_yahoo')} + K34 Tiingo {R['evp_n'].get('K34_tiingo')}; örtüşme yok (aynı sembol iki kez yüklenmez) |",
         f"| Likidite süzgecinden en az bir gün geçen | {int((EVT.likit_gun > 0).sum())} | bu çalışmanın paneli; K51 raporundaki 2.752 bu sayıdır |",
         f"| Hiç likit günü olmayan | {int((EVT.likit_gun == 0).sum())} | işlem değeri < 1 M$ ya da pazar içi alt %20, fiyat < 1 $, evren girişi geç |",
         f"| Panel satırı (likit hisse-gün, etiketli) | {R['P_n']} | |",
         f"| Yinelenen K34 sembolü | {len(R['yinelenen']) // 2 if len(R['yinelenen']) else 0} | aynı kod, FARKLI CIK (kod sonradan başka şirkete geçmiş); yüklemede ikinci şirket atlandı |", ""]
    if len(R["yinelenen"]):
        L += tablo(R["yinelenen"], ["cik", "sembol", "kaynak", "ilk_giris", "batan", "w"])
    L += ["", "Şirket kimliği (CIK) ve sembol kimliği K51_EVREN_PIT.csv'de ayrı sütunlardadır. Fiyat verisi sembole bağlıdır; CIK yalnız K34 şirketlerinde bilinir.", "",
          "## V2 Point-in-time evren tablosu", "", f"K51_EVREN_PIT.csv ({len(EVT)} satır): sembol, CIK, kaynak, evren girişi ve dayanağı, ilk / son fiyat günü, son kapanış, son 60 gün getirisi, çıkış türü tahmini, son SEC bildirimi, kod yeniden kullanımı şüphesi.", "",
          "## V3 2016-20 eğitim evreni", "", f"- Evrene 2021 öncesi giren hisse: {int((EVT.evren_bas < '2021-01-01').sum())} (hepsi V_ABD = bugün işlem görenler). K34 girişleri {str(pd.to_datetime(EVT[EVT.kaynak != 'V_ABD'].evren_bas).min().date()) if (EVT.kaynak != 'V_ABD').any() else '-'} ve sonrası.",
          "- 2016-20 dönemi yalnız hayatta kalanlardan oluşur; doldurulmadı. Bu dönemin hücreleri bu yüzden iyimser olabilir; kaynak kırılımı K51_KIRILGANLIK.md'de.", "",
          "## V4 Çıkış sınıflaması (tahmin; gerçek delist nedeni değil)", ""]
    ct = EVT.groupby(["kaynak", "cikis_turu_tahmin", "sec_bildirimi_suruyor"]).size().reset_index(name="n"); L += tablo(ct, ["kaynak", "cikis_turu_tahmin", "sec_bildirimi_suruyor", "n"])
    L += ["", "- 'sec_bildirimi_suruyor' = şirketin (yüklenen CIK) son 10-K / 10-Q bildirimi 31.08.2026'dan en çok 120 gün önce ya da sonra: şirket yaşıyor. Tiingo serisi sürüp şirket bildirim vermiyorsa kod başka şirkete geçmiş olabilir (V8).",
          "- Yinelenen 4 sembolde (BG, RDUS, SBGI, ZYME) iki CIK aynı şirketin yeniden kaydı (yeniden yapılanma / yer değişimi) ya da kodun yeni şirkete geçişi olabilir; K34 evreninde 'batan' sayılıp 1,83 ağırlık almışlardır, seri bugün sürüyor."]
    L += ["", f"- Kural: seri 2026-08-01'den önce bitiyorsa çıkış; son 60 gün getirisi <= {V12['batma_r60']:.0%} ya da son kapanış < {V12['batma_fiyat']} $ -> 'batma benzeri'; son 60 gün >= 0 -> 'satın alma / birleşme benzeri'; arası 'belirsiz çıkış'.",
          "- Tiingo örneklemi tam batan evreni DEĞİLDİR: SEC nakit pisti olan ve kodu kapakta bulunan şirketlerden 450'lik rastgele örneklem (K34, ağırlık 1,83); K34 dışındaki (nakit sorunu olmayan) batanlar evrende yoktur.",
          f"- Kod yeniden kullanımı şüphesi (Tiingo / Yahoo serisi şirketin son SEC bildiriminden {V12['kes_gun']} günden fazla sürüyor ve seri bugün devam ediyor): {int(EVT.kod_yeniden_kullanim_suphesi.sum())} hisse. Bu serilerde eski şirketin fiyatları, kodu sonradan alan şirketin fiyatlarıyla birleşmiş olabilir (V8 senaryosu).", "",
          "## V5 / V6 / V8 Duyarlılık senaryoları (olay isabeti - K51 tabanı; ağırlıklı)", "",
          "Senaryolar varsayımsaldır: 'ana' = seri vadeden önce bitince son kapanış, son 60 gün eksiyse ek -%30; 'delist %0' = ek kayıp yok; 'delist -%100' = tam kayıp; 'V8 kod kesme' = K34 serisi son SEC bildirimi + 120 günde kesilir (kesilen seri borsadan çıkmış sayılır), yalnız kesmeden önceki olaylar. Baz fiyat = serinin son kapanışı; uygulama günü = serinin son günü.", ""]
    L += tablo(R["SEN"], ["kume", "donem", "senaryo", "n", "isabet", "taban", "fark", "fark_alt", "fark_ust", "net", "etkilenen_olay", "seri_sonunda_cikan_olay"])
    L += ["", "- 'etkilenen_olay' = senaryoda net getirisi değişen olay sayısı; 'seri_sonunda_cikan_olay' = serisi 01.08.2026'dan önce biten hissedeki olay sayısı (delist kuralının uygulanabildiği küme). Üst bariyer etiketi (y) delist cezasından etkilenmez; yalnız net getiri etkilenir."]
    h = R["ham"]; L += ["", "## V6 Ham ve düzeltilmiş fiyat (yalnız Tiingo altkümesi; Yahoo serileri yalnız düzeltilmiş)", "",
                        f"- Tiingo hisse {h['hisse']}, likit satır {h['satir']}: ham fiyatla etiket uyumu {f(h['uyum'])}; olay satırı {h['olay_satir']}: uyum {f(h['olay_uyum'])}.",
                        "- Sınır: düzeltilmiş fiyatla bariyer, temettü ve bölünme sonrası gerçek işlem fiyatından sapabilir; Yahoo altkümesinde ölçülemedi. Temettü, düşüş sonrası küçük hisselerde azdır.", "",
                        "## V7 Eski kod (29 Ekim düzeltmelerinden önce) ve yeni kod", "", f"- {R['esk_not']}", "- Olay tespiti iki sürümde aynıdır; farklar taban (ağırlık, belirsiz, batan bayrağı) ve piyasa kıyasındadır.", ""]
    L += tablo(R["ESKYENI"], ["kod", "kume", "donem", "n", "isabet", "taban", "fark", "fark_alt", "net"])
    open(os.path.join(A.cikti, "K51_VERI_DENETIMI.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    KIR = R["KIR"]; L = ["# K51 — KIRILGANLIK (v1.2, ön kayıt 8e99902)", "", "Olay isabeti - K51 tabanı (aynı gün aynı oynaklık ondalığı, ağırlıklı); %95 aralık ay kümeli. 'Bugün hayatta olma' bilgisi hiçbir süzgeçte kullanılmadı; yalnız raporda ayrılıyor. 2026 kısmidir (sinyal <= 05.06.2026).", ""]
    for kir in ("kaynak", "en_iyi_20_hisse_cikarildi", "hisse_basina_esit_agirlik", "katki_payi", "yil", "rejim", "ortusme"):
        L += [f"## {kir}", ""] + tablo(KIR[KIR.kirilim == kir], ["kume", "donem", "deger", "n", "isabet", "taban", "fark", "fark_alt", "fark_ust", "net"]) + [""]
    HK = R["HK"]; L += ["## Eşleşmiş kontrol hücreleri: iki kümeleme", "", "Aynı fark için ay kümeli ve hisse x çeyrek kümeli %95 aralık yan yana.", ""]
    L += tablo(HK[HK.donem.isin([d_[0] for d_ in V12["donem"]])], ["hipotez", "hucre", "donem", "n", "hisse_n", "fark", "fark_alt", "fark_ust", "fark_alt_hisse_ceyrek", "fark_ust_hisse_ceyrek"])
    open(os.path.join(A.cikti, "K51_KIRILGANLIK.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    # tekrar üretim
    kok = os.path.dirname(os.path.abspath(globals().get("__file__", "COL_YOLU_ABD.py"))) or "."
    try:
        commit = subprocess.run(["git", "-C", kok, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "?"
    def sha(yol):
        hh = hashlib.sha256()
        with open(yol, "rb") as fh:
            for b in iter(lambda: fh.read(1 << 20), b""):
                hh.update(b)
        return hh.hexdigest()[:16]
    dosyalar = ["K51_VERI_DENETIMI.md", "K51_KIRILGANLIK.md", "K51_ESLESMIS_KONTROL.csv.gz", "K51_HIPOTEZ_KARARLARI.csv", "K51_EVREN_PIT.csv"]
    veri_d = [(ad, sha(os.path.join(A.veri, ad))) for ad in ("V_ABD.pkl", "k34_yahoo.pkl", "k34_evren.csv", "endeks.pkl") if os.path.exists(os.path.join(A.veri, ad))]
    tk = A.tiingo or os.path.join(A.veri, "tiingo"); tn = len([x for x in os.listdir(tk) if x.endswith(".csv")]) if os.path.isdir(tk) else 0
    L = ["# K51 — TEKRAR ÜRETİM (v1.2)", "", f"- Kod: COL_YOLU_ABD.py {CY_SURUM}; git commit {commit}; ön kayıt commit 8e99902; eski kod kıyası {V12['eski_commit']}.",
         f"- Veri sürümü: islenmis-veri dalı (V_ABD.pkl, k34_yahoo.pkl), k34_evren.csv (main), Tiingo CSV {tn} dosya (lisans gereği repoda yok), endeks.pkl (yfinance SPY/IWM/^STOXX/XU100).",
         "- Veri sha256 (ilk 16): " + ", ".join(f"{a}={b}" for a, b in veri_d),
         f"- Parametreler: CY (K51 ile aynı) + CY_V12 = {json.dumps({k_: (list(v) if isinstance(v, tuple) else v) for k_, v in V12.items()}, ensure_ascii=False)}",
         f"- Rastgelelik: tohum {V12['tohum']} (eşleştirme sırası ve bootstrap), bootstrap {V12['boot']}; eşleştirme deterministik (stable argsort).",
         f"- Örneklem: panel {R['P_n']} likit hisse-gün, {R['hisse']} hisse; eşleşmiş kontrol satırı {R['ESL_n']}; süre {R['sure_dk']} dk.",
         "- Adımlar: (1) `exec(open('.../COL_YOLU_ABD.py').read()); R = cy_v12_calistir()` (veri klasörü CY_VERI; Tiingo CSV'leri CY_TIINGO ya da veri/tiingo); (2) çıktılar CY_CIKTI altına yazılır; (3) `python test_col_yolu_abd.py` 17/17.",
         "- Çıktı özetleri (sha256 ilk 16): " + ", ".join(f"{ad}={sha(os.path.join(A.cikti, ad))}" for ad in dosyalar if os.path.exists(os.path.join(A.cikti, ad))),
         f"- Holm (aile = 5 hipotez, 2023-26 tek yönlü bootstrap p): {json.dumps({k_: round(v, 4) for k_, v in R['holm'].items()})}", ""]
    open(os.path.join(A.cikti, "K51_TEKRAR_URETIM.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


# ---------------------------------------------------------------- v1.3 K52 GRAFİK İZİ + ANALİST REVİZYONLARI (ön kayıt commit c33a10e:
# arastirma_cikti/col_yolu_abd/K52_onkayit.md). K51 kuralları ve kararı değişmez. Kaynak: Yahoo analist not günlüğü (yfinance
# upgrades_downgrades; EPS revizyonu ve gerekçe YOK). Sızıntı: olay günü d için yalnız tarih <= d-1 kayıtları. Pencere 20 işlem günü.
CY_V13: Dict[str, Any] = {
    "pencere": 20, "tohum": 513, "boot": 2000, "fark_esik": 0.05, "n_min": 30, "kapsama_gun": 365, "dogruluk_min": 10, "dogruluk_gecikme_gun": 90,
    "h4_yukselis": 0.10, "gun_tol": 10, "k_es": 3,
    "alim": ("BUY", "STRONG BUY", "OUTPERFORM", "OVERWEIGHT", "POSITIVE", "ACCUMULATE", "MARKET OUTPERFORM", "SECTOR OUTPERFORM", "TOP PICK", "CONVICTION BUY"),
    "donem": (("2016-22", "2016-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-06-05")),
    "yillar": ((2023, "2023-01-01", "2023-12-31"), (2024, "2024-01-01", "2024-12-31"), (2025, "2025-01-01", "2025-12-31"), (2026, "2026-01-01", "2026-06-05")),
}


def cy_v13_kurum(ad: Any) -> str:
    """Kurum adı normalizasyonu (kopya ayıklama için): büyük harf, noktalama ve yaygın ekler atılır."""
    s = " " + " ".join(str(ad).upper().replace("&", " AND ").replace(".", " ").replace(",", " ").split()) + " "
    for ek in (" SECURITIES ", " CAPITAL MARKETS ", " CAPITAL ", " RESEARCH ", " PARTNERS ", " GROUP ", " AND COMPANY ", " AND CO ", " INC ", " LLC ", " LTD ", " CO "):
        while ek in s:
            s = s.replace(ek, " ")
    return "".join(ch for ch in s if ch.isalnum())


def cy_v13_gunluk_yukle(yol: str, K: Dict[str, Any] = CY_V13) -> pd.DataFrame:
    """Yahoo not günlüğü (sembol -> DataFrame) -> tek tablo: sembol, zaman, tarih, saat_var, kurum, eski, yeni, eylem, hedef_eylem, hedef, eski_hedef,
    olumlu, olumsuz (ön kayıt 2). Aynı kurum aynı tarih tek kayıt."""
    import pickle
    ham = pickle.load(open(yol, "rb")); parca = []
    for s, u in ham.items():
        if u is None or not isinstance(u, pd.DataFrame) or not len(u):
            continue
        d = u.reset_index(); d.columns = [str(c) for c in d.columns]
        d = d.rename(columns={"GradeDate": "zaman", "Firm": "kurum", "ToGrade": "yeni", "FromGrade": "eski", "Action": "eylem", "priceTargetAction": "hedef_eylem",
                              "currentPriceTarget": "hedef", "priorPriceTarget": "eski_hedef"})
        d["sembol"] = s; parca.append(d)
    if not parca:
        return pd.DataFrame()
    G = pd.concat(parca, ignore_index=True); G["zaman"] = pd.to_datetime(G.zaman, errors="coerce"); G = G.dropna(subset=["zaman"])
    try:
        G["zaman"] = G.zaman.dt.tz_localize(None)
    except Exception:
        pass
    G["zaman"] = G.zaman.astype("datetime64[ns]"); G["tarih"] = G.zaman.dt.normalize(); G["saat_var"] = (G.zaman != G.tarih)
    G["kurum_n"] = G.kurum.map(cy_v13_kurum); G["eylem"] = G.eylem.astype(str).str.lower(); G["hedef_eylem"] = G.hedef_eylem.astype(str)
    for c in ("hedef", "eski_hedef"):
        G[c] = pd.to_numeric(G[c], errors="coerce").replace(0, np.nan)
    yeni_u = G.yeni.astype(str).str.upper().str.strip()
    G["olumlu"] = (G.eylem == "up") | (G.hedef_eylem == "Raises") | ((G.eylem == "init") & yeni_u.isin(K["alim"]))
    G["olumsuz"] = (G.eylem == "down") | (G.hedef_eylem == "Lowers")
    G["hedef_degisim"] = np.where(G.eski_hedef > 0, G.hedef / G.eski_hedef - 1, np.nan)
    G = G.sort_values(["sembol", "tarih"]).drop_duplicates(["sembol", "kurum_n", "tarih"], keep="last").reset_index(drop=True)
    return G


def cy_v13_kapsam(G: pd.DataFrame, EVT: pd.DataFrame, P: pd.DataFrame) -> pd.DataFrame:
    """K51_ANALIST_VERI_KAPSAMI: alan / kaynak grubu / yıl bazında kapsama, eksik ve zaman damgası güvenilirliği."""
    rows = []; var = set(G.sembol) if len(G) else set()
    for ky, g in EVT.groupby("kaynak"):
        rows.append({"boyut": "kaynak", "deger": ky, "hisse": len(g), "analist_kaydi_olan_hisse": int(g.sembol.isin(var).sum()), "kapsama_oran": float(g.sembol.isin(var).mean()),
                     "kayit": int(G.sembol.isin(g.sembol).sum()) if len(G) else 0})
    if len(G):
        for y, g in G.groupby(G.tarih.dt.year):
            rows.append({"boyut": "yil", "deger": int(y), "hisse": int(g.sembol.nunique()), "kayit": len(g), "saat_var_oran": float(g.saat_var.mean()),
                         "hedef_var_oran": float(g.hedef.notna().mean()), "eski_hedef_var_oran": float(g.eski_hedef.notna().mean()),
                         "eski_tavsiye_var_oran": float(G.loc[g.index, "eski"].astype(str).str.strip().ne("").mean()), "olumlu_oran": float(g.olumlu.mean()), "olumsuz_oran": float(g.olumsuz.mean())})
        for alan, ad in (("zaman", "yayım tarih-saati"), ("kurum", "kurum kimliği"), ("eski", "önceki tavsiye"), ("yeni", "yeni tavsiye"), ("eski_hedef", "önceki hedef fiyat"),
                         ("hedef", "yeni hedef fiyat"), ("hedef_degisim", "hedef fiyat revizyon yüzdesi")):
            v = G[alan]; eksik = float(v.isna().mean()) if alan != "eski" else float(v.astype(str).str.strip().eq("").mean())
            rows.append({"boyut": "alan", "deger": ad, "kaynak": "Yahoo not günlüğü", "kayit": int(len(G)), "eksik_oran": eksik, "baslangic": str(G.tarih.min().date()), "bitis": str(G.tarih.max().date())})
        for ad in ("EPS / kâr tahmini revizyonu", "rapor gerekçesi ve riskler", "analist kişi kimliği", "rapor kimliği / tarihsel sürüm"):
            rows.append({"boyut": "alan", "deger": ad, "kaynak": "YOK (Yahoo günlüğünde bulunmuyor)", "eksik_oran": 1.0})
        sa = G.zaman.dt.hour
        rows.append({"boyut": "zaman", "deger": "saat dağılımı (UTC varsayımı): 00:00 payı / 10-16 payı / medyan saat", "kayit": int(len(G)),
                     "eksik_oran": float((G.zaman == G.tarih).mean()), "kapsama_oran": float(sa.between(10, 16).mean()), "hisse": int(sa.median()),
                     "saat_var_oran": float(G.saat_var.mean()), "olumlu_oran": float(G.tarih.dt.dayofweek.ge(5).mean())})
        pz = P[P.P1 | P.P2]
        rows.append({"boyut": "olay", "deger": "P1 / P2 olaylarında sembolün d'den önce kaydı olan pay", "kapsama_oran": float(pz.sembol.isin(var).mean()), "hisse": int(pz.sembol.nunique())})
    return pd.DataFrame(rows)


def cy_v13_ozellik(E: pd.DataFrame, G: pd.DataFrame, H: Dict[str, Dict[str, Any]], K: Dict[str, Any] = CY_V13) -> pd.DataFrame:
    """Olay (sembol, tarih, i) başına pencere özellikleri (ön kayıt 2): yalnız tarih <= d-1 kayıtları. Kurum doğruluğu: kurumun d - 90 günden
    önceki 'up' kayıtlarının isabeti (sonucu d'den önce bilinen). H4 zamanlaması: olumlu revizyon pencere dibinden >= %10 yükseliş SONRASI mı."""
    W = K["pencere"]; out = []; Gs = {s: g.sort_values("tarih") for s, g in G.groupby("sembol")} if len(G) else {}
    # kurum doğruluğu: her 'up' kaydını (sembol, ilk işlem günü >= tarih) etiketiyle eşle
    dog = {}
    if len(G):
        up = G[G.eylem == "up"][["sembol", "tarih", "kurum_n"]].copy(); yy = []
        for r in up.itertuples():
            h = H.get(r.sembol)
            if h is None:
                yy.append(np.nan); continue
            j = int(np.searchsorted(h["ptarih"], np.datetime64(r.tarih)))        # kaydı izleyen ilk likit panel günü (<= 7 takvim günü)
            yy.append(float(h["py"][j]) if (j < len(h["py"]) and h["ptarih"][j] - np.datetime64(r.tarih) <= np.timedelta64(7, "D")) else np.nan)
        up["y"] = yy; up = up.dropna(subset=["y"]).sort_values("tarih")
        for k_, g in up.groupby("kurum_n"):
            dog[k_] = (g.tarih.to_numpy(), np.cumsum(g.y.to_numpy()), np.arange(1, len(g) + 1))
    for r in E.itertuples():
        h = H[r.sembol]; d = np.datetime64(r.tarih); i = int(r.i); bas = h["tarih"][max(0, i - W)]; dmin1 = h["tarih"][i - 1] if i >= 1 else bas
        g = Gs.get(r.sembol); kayit_var = bool(g is not None and (g.tarih.to_numpy() <= dmin1).any())
        w = g[(g.tarih.to_numpy() >= bas) & (g.tarih.to_numpy() <= dmin1)] if g is not None else None
        f = {"sembol": r.sembol, "tarih": r.tarih, "i": i, "kayit_var": kayit_var, "n_kayit": 0, "n_yukari": 0, "n_asagi": 0, "n_baslangic_al": 0, "n_hedef_yukari": 0, "n_hedef_asagi": 0,
             "hedef_degisim_ort": np.nan, "olumlu": 0, "olumsuz": 0, "kurum_olumlu": 0, "kurum_toplam": 0, "genislik_oran": np.nan, "tazelik_gun": np.nan,
             "kurum_dogruluk": np.nan, "kapsama_365": 0, "olumlu_sonra_pay": np.nan, "teyit": False, "ters_teyit": False, "teyit_turu": "yok"}
        if g is not None:
            f["kapsama_365"] = int(((g.tarih.to_numpy() <= dmin1) & (g.tarih.to_numpy() > dmin1 - np.timedelta64(K["kapsama_gun"], "D"))).sum())
        if w is not None and len(w):
            f.update({"n_kayit": int(len(w)), "n_yukari": int((w.eylem == "up").sum()), "n_asagi": int((w.eylem == "down").sum()),
                      "n_baslangic_al": int(((w.eylem == "init") & w.olumlu).sum()), "n_hedef_yukari": int((w.hedef_eylem == "Raises").sum()),
                      "n_hedef_asagi": int((w.hedef_eylem == "Lowers").sum()), "hedef_degisim_ort": float(w.hedef_degisim.mean()) if w.hedef_degisim.notna().any() else np.nan,
                      "olumlu": int(w.olumlu.sum()), "olumsuz": int(w.olumsuz.sum()), "kurum_olumlu": int(w[w.olumlu].kurum_n.nunique()), "kurum_toplam": int(w.kurum_n.nunique())})
            f["genislik_oran"] = f["kurum_olumlu"] / f["kurum_toplam"] if f["kurum_toplam"] else np.nan
            wo = w[w.olumlu]
            if len(wo):
                son = wo.tarih.max(); f["tazelik_gun"] = int(np.searchsorted(h["tarih"], d) - np.searchsorted(h["tarih"], np.datetime64(son)))
                # H4: pencere dibinden >= %10 yükseliş sonrası gelen olumlu revizyon payı
                c = h["kapanis"][max(0, i - W):i]; t_ = h["tarih"][max(0, i - W):i]; sonra = []
                for tt in wo.tarih.to_numpy():
                    k_ = int(np.searchsorted(t_, np.datetime64(tt), side="right")) - 1
                    if k_ >= 1:
                        sonra.append(float(c[k_] >= np.nanmin(c[:k_ + 1]) * (1 + K["h4_yukselis"])))
                f["olumlu_sonra_pay"] = float(np.mean(sonra)) if sonra else np.nan
                acc = []
                for k_ in wo.kurum_n.unique():
                    if k_ in dog:
                        t2, cs, cn = dog[k_]; j = int(np.searchsorted(t2, d - np.timedelta64(K["dogruluk_gecikme_gun"], "D")))
                        if j >= K["dogruluk_min"]:
                            acc.append(cs[j - 1] / cn[j - 1])
                f["kurum_dogruluk"] = float(np.mean(acc)) if acc else np.nan
            f["teyit"] = bool(f["olumlu"] >= 1 and f["olumlu"] > f["olumsuz"]); f["ters_teyit"] = bool(f["olumsuz"] >= 1 and f["olumsuz"] > f["olumlu"])
            if f["teyit"]:
                f["teyit_turu"] = "yalniz_tavsiye" if (f["n_yukari"] + f["n_baslangic_al"] > 0 and f["n_hedef_yukari"] == 0) else ("yalniz_hedef" if (f["n_yukari"] + f["n_baslangic_al"] == 0) else "ikisi")
        out.append(f)
    return pd.DataFrame(out)


def cy_v13_fark(A_: pd.DataFrame, B_: pd.DataFrame, K: Dict[str, Any], rng: np.random.Generator) -> Dict[str, Any]:
    """Taban-ayarlı isabet farkı Δ = ort(y - e_y | A) - ort(y - e_y | B); ay kümeli aralık ve p; hisse x çeyrek aralığı (iki grubun ayrı kümeli
    varyanslarının toplamı); net fark; ham isabetler."""
    if not len(A_) or not len(B_):
        return {"n_a": int(len(A_)), "n_b": int(len(B_))}
    A2 = A_.assign(_f=A_.y - A_.e_y, _fn=A_.net - A_.e_net); B2 = B_.assign(_f=B_.y - B_.e_y, _fn=B_.net - B_.e_net); B = K["boot"]
    f, a, b = cy_boot_iki(A2, B2, "_f", B, rng); fn, an, bn = cy_boot_iki(A2, B2, "_fn", B, rng)
    ka = cy_boot_kume(A2, "_f", 1000, rng); kb = cy_boot_kume(B2, "_f", 1000, rng)
    if all(np.isfinite(v) for v in ka + kb):
        sa = (ka[1] - ka[0]) / 3.92; sb = (kb[1] - kb[0]) / 3.92; s = float(np.sqrt(sa ** 2 + sb ** 2)); hq = (f - 1.96 * s, f + 1.96 * s)
    else:
        hq = (np.nan, np.nan)
    # tek yönlü p: ay kümeli bootstrap farkının <= 0 payı
    ay = lambda D: (D.tarih.dt.year * 12 + D.tarih.dt.month).to_numpy()
    aa, ba = ay(A2), ay(B2); ua = np.unique(np.r_[aa, ba]); wa = A2["agirlik"].to_numpy(float) if "agirlik" in A2 else np.ones(len(A2)); wb = B2["agirlik"].to_numpy(float) if "agirlik" in B2 else np.ones(len(B2))
    sA = pd.DataFrame({"ay": aa, "s": A2._f.to_numpy() * wa, "c": wa}).groupby("ay").sum().reindex(ua, fill_value=0); sB = pd.DataFrame({"ay": ba, "s": B2._f.to_numpy() * wb, "c": wb}).groupby("ay").sum().reindex(ua, fill_value=0)
    ix = rng.integers(0, len(ua), (B, len(ua))); bs = sA.s.to_numpy()[ix].sum(1) / np.maximum(sA.c.to_numpy()[ix].sum(1), 1e-9) - sB.s.to_numpy()[ix].sum(1) / np.maximum(sB.c.to_numpy()[ix].sum(1), 1e-9)
    return {"n_a": int(len(A_)), "n_b": int(len(B_)), "hisse_a": int(A_.sembol.nunique()), "hisse_b": int(B_.sembol.nunique()), "isabet_a": float(np.average(A_.y, weights=wa)),
            "isabet_b": float(np.average(B_.y, weights=wb)), "taban_a": float(np.average(A_.e_y, weights=wa)), "taban_b": float(np.average(B_.e_y, weights=wb)),
            "delta": f, "delta_alt": a, "delta_ust": b, "delta_alt_hisse_ceyrek": hq[0], "delta_ust_hisse_ceyrek": hq[1], "ham_fark": float(np.average(A_.y, weights=wa) - np.average(B_.y, weights=wb)),
            "net_a": float(np.average(A_.net, weights=wa)), "net_b": float(np.average(B_.net, weights=wb)), "net_fark": fn, "net_fark_alt": an, "net_fark_ust": bn,
            "p": float((np.sum(bs <= 0) + 1) / (B + 1))}


def cy_v13_karar(h: Dict[str, Any], K: Dict[str, Any]) -> str:
    if min(h.get("n_a", 0), h.get("n_b", 0)) < K["n_min"]:
        return "YETERSİZ ÖRNEKLEM"
    if h["delta"] >= K["fark_esik"] and h["delta_alt"] > 0 and h["net_fark"] > 0:
        return "TUTAR"
    if h["delta"] <= -K["fark_esik"] and h["delta_ust"] < 0:
        return "TERS YÖN"
    return "TUTMAZ"


def cy_v13_panel(A: CYAyar, K: Dict[str, Any]) -> Dict[str, Any]:
    """v1.2 paneli (ABD): likit hisse-gün satırları (y, net, özellikler, P1 / P2 / ÇEK / HT), ağırlık, kaynak, sektör, vd / lt, K51 tabanı e_y / e_net,
    rejim; Hs = tam seri + likit panel etiketi. K['_endeks'] doldurulur. v1.3 ve v1.4 ortak."""
    cy_veri_hazirla(A); Vs, EV = cy_veri_yukle(A, K); cy_v12_tekil(EV); K["_endeks"] = cy_endeks(A, K)
    V = Vs["ABD"]; le = cy_likit_esik(V, "ABD", K); evp = EV[EV.pazar == "ABD"].set_index("sembol")
    args = [("ABD", s_, d, evp.loc[s_].to_dict(), le, K, None, None) for s_, d in V.items() if s_ in evp.index]
    import multiprocessing as mp
    with mp.get_context("fork").Pool(max(1, A.is_parcacigi)) as hv:
        son = [x for x in hv.imap_unordered(cy_v12_hisse, args, chunksize=8) if x is not None]
    P = pd.concat([r["panel"].assign(sembol=r["sembol"]) for r in son if len(r["panel"])], ignore_index=True)
    P = P.sort_values(["sembol", "tarih"], kind="stable").reset_index(drop=True)      # işçi sırası rastgele; örneklemler tekrar üretilebilsin
    P["tarih"] = pd.to_datetime(P.tarih).astype("datetime64[ns]"); P["agirlik"] = P.sembol.map(evp.agirlik).fillna(1.0).astype(np.float32); P["kaynak"] = P.sembol.map(evp.kaynak)
    sek = cy_sektor(A, EV); P["sektor"] = P.sembol.map(sek).fillna("bilinmiyor")
    P["vd"] = np.minimum((P.groupby("tarih").vol60.rank(pct=True) * 10).fillna(5).astype(int), 9).astype(np.int8)
    P["lt"] = np.minimum((P.groupby("tarih").log_dv20.rank(pct=True) * 3).fillna(1).astype(int), 2).astype(np.int8)
    ww = P.agirlik.where(P.y.notna()); grp = [P.tarih, P.vd]
    P["e_y"] = ((P.y * ww).groupby(grp).transform("sum") / ww.groupby(grp).transform("sum")).astype(np.float32)
    P["e_net"] = ((P.net * ww).groupby(grp).transform("sum") / ww.groupby(grp).transform("sum")).astype(np.float32)
    En = K.get("_endeks", pd.DataFrame())
    if isinstance(En, pd.DataFrame) and "SPY" in En:
        sp = En["SPY"].dropna(); boga = (sp > sp.rolling(200).mean()).reindex(P.tarih.values, method="ffill").to_numpy(); P["rejim"] = np.where(boga, "BOĞA", "AYI")
    else:
        P["rejim"] = "bilinmiyor"
    Hs = {}
    for r in son:                                                            # tam seri (tarih, kapanis) + likit panel etiketi (ptarih, py)
        d = V[r["sembol"]]; pn = r["panel"]
        Hs[r["sembol"]] = {"tarih": d.index.to_numpy().astype("datetime64[ns]"), "kapanis": d.Close.to_numpy(float),
                           "ptarih": pd.to_datetime(pn.tarih).to_numpy().astype("datetime64[ns]"), "py": pn.y.to_numpy(float)}
    return {"P": P, "V": V, "EV": EV, "evp": evp, "Hs": Hs, "sektor": sek}


def cy_v13_calistir(A: Optional[CYAyar] = None, K: Dict[str, Any] = CY, gunluk_yol: Optional[str] = None) -> Dict[str, Any]:
    """K52 sürücü: v1.2 paneli (P1 / P2 / ÇEK, y, e_y) + Yahoo not günlüğü -> kapsama, revizyon özellikleri, dört grup, H0-H6, çıktılar."""
    import hashlib, subprocess
    A = A or CYAyar(); os.makedirs(A.cikti, exist_ok=True); K = {**K, "_v12": CY_V12, "_v13": CY_V13}; V13 = CY_V13; t0 = time.time()
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    rng = np.random.default_rng(V13["tohum"]); PN = cy_v13_panel(A, K); P, V, EV, evp, Hs = PN["P"], PN["V"], PN["EV"], PN["evp"], PN["Hs"]
    cylog.info("v1.3 panel %d satır, %d hisse (%ds)", len(P), P.sembol.nunique(), time.time() - t0)
    # günlük
    gy = gunluk_yol or os.path.join(A.veri, "analist", "yahoo_grades.pkl")
    if not os.path.exists(gy):
        raise FileNotFoundError(f"analist günlüğü yok: {gy}")
    G = cy_v13_gunluk_yukle(gy, V13); EVT = pd.read_csv(os.path.join(A.cikti, "K51_EVREN_PIT.csv")) if os.path.exists(os.path.join(A.cikti, "K51_EVREN_PIT.csv")) else EV[EV.pazar == "ABD"].rename(columns={"kaynak": "kaynak"})
    KAP = cy_v13_kapsam(G, EVT, P); KAP.to_csv(os.path.join(A.cikti, "K51_ANALIST_VERI_KAPSAMI.csv"), index=False)
    cylog.info("v1.3 günlük %d kayıt, %d hisse", len(G), G.sembol.nunique() if len(G) else 0)
    # olay özellikleri: P1, P2 ve genel (ÇEK dışı) örneklem (G3 / G4 için her 5. likit gün)
    rng_g = np.random.default_rng(V13["tohum"]); genel = P[~P.cek_ham & ~P.P1 & ~P.P2]; genel = genel[rng_g.random(len(genel)) < min(1.0, 60000 / max(len(genel), 1))]
    olaylar = pd.concat([P[P.P1].assign(iz="P1"), P[P.P2].assign(iz="P2"), genel.assign(iz="YOK")], ignore_index=True)
    F = cy_v13_ozellik(olaylar[["sembol", "tarih", "i"]], G, Hs, V13); X = pd.concat([olaylar.reset_index(drop=True), F.drop(columns=["sembol", "tarih", "i"])], axis=1)
    X["grup"] = np.where(X.iz != "YOK", np.where(X.teyit, "G1", np.where(X.kayit_var, "G2a", "G2b")), np.where(X.teyit, "G3", np.where(X.kayit_var, "G4a", "G4b")))
    X["donem"] = ""
    for dn, a, b in V13["donem"]:
        X.loc[(X.tarih >= a) & (X.tarih <= b), "donem"] = dn
    X = X[X.donem != ""].reset_index(drop=True)                               # dönem dışı (fon krizi kesiti sonrası) olaylar girmez
    kol = ["iz", "grup", "sembol", "tarih", "i", "donem", "rejim", "kaynak", "sektor", "vd", "lt", "dd250", "r60", "log_dv20", "y", "net", "e_y", "e_net", "agirlik", "kayit_var",
           "n_kayit", "n_yukari", "n_asagi", "n_baslangic_al", "n_hedef_yukari", "n_hedef_asagi", "hedef_degisim_ort", "olumlu", "olumsuz", "kurum_olumlu", "kurum_toplam",
           "genislik_oran", "tazelik_gun", "kurum_dogruluk", "kapsama_365", "olumlu_sonra_pay", "teyit", "ters_teyit", "teyit_turu"]
    X[X.iz != "YOK"][kol].to_csv(os.path.join(A.cikti, "K51_ANALIST_REVIZYONLARI.csv.gz"), index=False)
    # dört grup tablosu
    G4 = []
    for (iz, grup, dn), g in X.groupby(["iz", "grup", "donem"]):
        w = g.agirlik.to_numpy(float)
        G4.append({"iz": iz, "grup": grup, "donem": dn, "n": len(g), "hisse": g.sembol.nunique(), "isabet": float(np.average(g.y, weights=w)), "taban_e_y": float(np.average(g.e_y, weights=w)),
                   "taban_ayarli": float(np.average(g.y - g.e_y, weights=w)), "net": float(np.average(g.net, weights=w)), "net_taban": float(np.average(g.e_net, weights=w)),
                   "kapsama_365_ort": float(g.kapsama_365.mean()), "log_dv20_ort": float(g.log_dv20.mean()), "dd250_ort": float(g.dd250.mean()), "r60_ort": float(g.r60.mean()),
                   "boga_pay": float((g.rejim == "BOĞA").mean()), "V_ABD_pay": float((g.kaynak == "V_ABD").mean()), "en_buyuk_sektor_pay": float(g.sektor.value_counts(normalize=True).iloc[0]) if len(g) else np.nan})
    G4 = pd.DataFrame(G4); G4.to_csv(os.path.join(A.cikti, "K51_GRAFIK_ANALIST_4GRUP.csv"), index=False)
    # hipotez testleri
    T = []; p23 = {}
    def test(kod, ad, Aset, Bset, hucre="tum"):
        kar = []
        for dn, a, b in V13["donem"]:
            h = cy_v13_fark(Aset[(Aset.tarih >= a) & (Aset.tarih <= b)], Bset[(Bset.tarih >= a) & (Bset.tarih <= b)], V13, rng); kr = cy_v13_karar(h, V13) if "delta" in h else "YETERSİZ ÖRNEKLEM"
            T.append({"kod": kod, "hipotez": ad, "hucre": hucre, "donem": dn, **h, "karar_hucre": kr}); kar.append(kr)
        h23 = cy_v13_fark(Aset[Aset.tarih >= "2023-01-01"], Bset[Bset.tarih >= "2023-01-01"], V13, rng); p23[(kod, hucre)] = h23.get("p", np.nan)
        T.append({"kod": kod, "hipotez": ad, "hucre": hucre, "donem": "2023-26 (Holm için)", **h23, "karar_hucre": cy_v13_karar(h23, V13) if "delta" in h23 else "YETERSİZ ÖRNEKLEM"})
        son_k = "YETERSİZ ÖRNEKLEM" if "YETERSİZ ÖRNEKLEM" in kar else ("DESTEKLENİYOR (KEŞİFSEL; 2023-26 bağımsız değil)" if all(k_ == "TUTAR" for k_ in kar) else ("DESTEKLENMİYOR (TERS YÖN)" if "TERS YÖN" in kar else "DESTEKLENMİYOR"))
        T.append({"kod": kod, "hipotez": ad, "hucre": hucre, "donem": "KARAR", "karar_hucre": son_k, "donem_kararlari": " | ".join(f"{d_[0]}: {k_}" for d_, k_ in zip(V13["donem"], kar))})
        return son_k
    for iz in ("P1", "P2"):
        Xi = X[X.iz == iz]; G1 = Xi[Xi.grup == "G1"]; G2a = Xi[Xi.grup == "G2a"]
        h0 = test(f"H0-{iz}", f"{iz}: yeni olumlu revizyon (G1) vs analist verisi var, teyit yok (G2a)", G1, G2a)
        test(f"H0b-{iz}", f"{iz}: G1 vs G2b (veri yok; bilgi, karışık nedensellik)", G1, Xi[Xi.grup == "G2b"])
        test(f"H2-{iz}", f"{iz}: yalnız tavsiye teyidi vs yalnız hedef fiyat teyidi", G1[G1.teyit_turu == "yalniz_tavsiye"], G1[G1.teyit_turu == "yalniz_hedef"])
        test(f"H3-{iz}", f"{iz}: >= 2 farklı kurumdan teyit vs tek kurum", G1[G1.kurum_olumlu >= 2], G1[G1.kurum_olumlu == 1])
        test(f"H4-{iz}", f"{iz}: olumlu revizyon fiyat hareketinden ÖNCE (sonra payı 0) vs SONRA (sonra payı 1)", G1[G1.olumlu_sonra_pay == 0], G1[G1.olumlu_sonra_pay == 1])
        for rj in ("AYI", "BOĞA"):
            test(f"H6-{iz}", f"{iz}: G1 vs G2a, rejim {rj}", G1[G1.rejim == rj], G2a[G2a.rejim == rj], hucre=rj)
        test(f"TERS-{iz}", f"{iz}: olumsuz teyit (bilgi) vs G2a", Xi[Xi.ters_teyit & Xi.kayit_var], G2a)
        dm = G1.kurum_dogruluk.median()
        test(f"DOG-{iz}", f"{iz}: kurum geçmiş doğruluğu üst yarı vs alt yarı (bilgi)", G1[G1.kurum_dogruluk > dm], G1[G1.kurum_dogruluk <= dm])
        # H5: eşleşmiş G2a (v1.2 eşleştirme + kapsama üçte biri)
        G1m = G1.copy(); G2m = G2a.copy(); kt = pd.qcut(Xi.kapsama_365.rank(method="first"), 3, labels=False)
        G1m["imza_h"] = kt.loc[G1m.index].astype(int); G2m["imza_h"] = kt.loc[G2m.index].astype(int); G1m["trend"] = Xi.loc[G1m.index, "trend"]; G2m["trend"] = Xi.loc[G2m.index, "trend"]
        G1m["ar20"] = Xi.loc[G1m.index, "ar20"]; G2m["ar20"] = Xi.loc[G2m.index, "ar20"]; G1m["vol60"] = Xi.loc[G1m.index, "vol60"]; G2m["vol60"] = Xi.loc[G2m.index, "vol60"]
        M5 = cy_v12_eslestir(P, G1m, G2m, K, V13["k_es"], V13["gun_tol"], rng, es_imza=True); G1e = pd.concat([G1m, M5], axis=1); G1e = G1e[G1e.kontrol_n > 0]
        kar5 = []
        for dn, a, b in V13["donem"]:
            D = G1e[(G1e.tarih >= a) & (G1e.tarih <= b)]
            if len(D) < V13["n_min"]:
                T.append({"kod": f"H5-{iz}", "hipotez": f"{iz}: G1 - eşleşmiş G2a (kapsama, sektör, oynaklık, likidite, düşüş, trend)", "hucre": "tum", "donem": dn, "n_a": len(D), "karar_hucre": "YETERSİZ ÖRNEKLEM"}); kar5.append("YETERSİZ ÖRNEKLEM"); continue
            h = cy_v12_hucre(D, K, rng); kr = cy_v12_karar(h, K)
            T.append({"kod": f"H5-{iz}", "hipotez": f"{iz}: G1 - eşleşmiş G2a (kapsama, sektör, oynaklık, likidite, düşüş, trend)", "hucre": "tum", "donem": dn, "n_a": h["n"], "delta": h["fark"], "delta_alt": h["fark_alt"], "delta_ust": h["fark_ust"],
                      "net_fark": h["net_fark"], "p": h["p"], "karar_hucre": kr, "eslesen_pay": float(len(G1e) / max(len(G1m), 1))}); kar5.append(kr)
        h5 = cy_v12_hucre(G1e[G1e.tarih >= "2023-01-01"], K, rng); p23[(f"H5-{iz}", "tum")] = h5.get("p", np.nan)
        T.append({"kod": f"H5-{iz}", "hipotez": f"{iz}: G1 - eşleşmiş G2a", "hucre": "tum", "donem": "KARAR", "karar_hucre": ("H5 DESTEKLENİYOR (katkı eşleşince kayboluyor)" if (h0.startswith("DESTEKLENİYOR") and not all(k_ == "TUTAR" for k_ in kar5)) else ("H5 DESTEKLENMİYOR (eşleşince de tutuyor)" if all(k_ == "TUTAR" for k_ in kar5) else "UYGULANAMAZ (H0 desteklenmiyor)")),
                  "donem_kararlari": " | ".join(f"{d_[0]}: {k_}" for d_, k_ in zip(V13["donem"], kar5))})
        # H4 zamanlama payı
        g1 = G1[G1.olumlu_sonra_pay.notna()]
        T.append({"kod": f"H4-{iz}", "hipotez": f"{iz}: W'deki olumlu revizyonların pencere dibinden >= %10 yükseliş SONRASI gelen payı", "hucre": "zamanlama", "donem": "hepsi", "n_a": len(g1),
                  "delta": float(g1.olumlu_sonra_pay.mean()) if len(g1) else np.nan, "karar_hucre": ("H4 DESTEKLENİYOR (çoğu sonra, H0 desteklenmiyor)" if (len(g1) and g1.olumlu_sonra_pay.mean() >= 0.5 and not h0.startswith("DESTEKLENİYOR")) else "H4 DESTEKLENMİYOR")})
    Td = pd.DataFrame(T)
    # Holm: aile = ölçülebilen hipotez hücreleri (H0, H2, H3, H4, H5, H6), P1 ve P2 ayrı aile
    for iz in ("P1", "P2"):
        pl = {k_: (v if np.isfinite(v) else 1.0) for k_, v in p23.items() if k_[0].endswith(iz) and k_[0].split("-")[0] in ("H0", "H2", "H3", "H4", "H5", "H6")}
        sr = sorted(pl.items(), key=lambda x: x[1]); m = len(sr); cum = 0.0
        for r_, (k_, p) in enumerate(sr):
            cum = max(cum, (m - r_) * p); Td.loc[(Td.kod == k_[0]) & (Td.hucre == k_[1]), "holm_p_2023_26"] = min(1.0, cum)
    Td["holm_gecer"] = Td.holm_p_2023_26 < 0.05
    Td.to_csv(os.path.join(A.cikti, "K51_ANALIST_EK_KATKI_TESTI.csv"), index=False)
    # kırılganlık: en iyi 20 hisse çıkarma (H0-P1), yıl, kaynak
    KR = []
    for iz in ("P1", "P2"):
        Xi = X[X.iz == iz]; G1 = Xi[Xi.grup == "G1"]; G2a = Xi[Xi.grup == "G2a"]
        if len(G1) >= 30:
            kat = (G1.y - G1.e_y).groupby(G1.sembol).sum().sort_values(ascending=False); top = set(kat.head(20).index)
            for dn, a, b in V13["donem"]:
                h = cy_v13_fark(G1[~G1.sembol.isin(top) & (G1.tarih >= a) & (G1.tarih <= b)], G2a[(G2a.tarih >= a) & (G2a.tarih <= b)], V13, rng)
                KR.append({"iz": iz, "kirilim": "en_iyi_20_cikarildi", "deger": dn, **{k_: h.get(k_) for k_ in ("n_a", "n_b", "delta", "delta_alt", "delta_ust", "net_fark")}})
        for yl, a, b in V13["yillar"]:
            h = cy_v13_fark(G1[(G1.tarih >= a) & (G1.tarih <= b)], G2a[(G2a.tarih >= a) & (G2a.tarih <= b)], V13, rng)
            KR.append({"iz": iz, "kirilim": "yil", "deger": f"{yl}{' (kısmi)' if yl == 2026 else ''}", **{k_: h.get(k_) for k_ in ("n_a", "n_b", "delta", "delta_alt", "delta_ust", "net_fark")}})
        for ky in ("V_ABD", "K34_yahoo", "K34_tiingo"):
            h = cy_v13_fark(G1[G1.kaynak == ky], G2a[G2a.kaynak == ky], V13, rng)
            KR.append({"iz": iz, "kirilim": "kaynak", "deger": ky, **{k_: h.get(k_) for k_ in ("n_a", "n_b", "delta", "delta_alt", "delta_ust", "net_fark")}})
    KRd = pd.DataFrame(KR)
    R = {"G": G, "KAP": KAP, "X": X, "G4": G4, "T": Td, "KR": KRd, "sure_dk": round((time.time() - t0) / 60, 1), "panel_n": int(len(P)), "hisse": int(P.sembol.nunique())}
    cy_v13_yaz(R, A, K); return R


def cy_v13_yaz(R: Dict[str, Any], A: CYAyar, K: Dict[str, Any]) -> None:
    """K51_ANALIST_TARIHSEL_VERI_DENETIMI.md ve K51_GRAFIK_ANALIST_ARASTIRMA.md."""
    import hashlib, subprocess
    TAM = {"n", "n_a", "n_b", "hisse", "hisse_a", "hisse_b", "analist_kaydi_olan_hisse", "kayit", "deger"}
    def f(x, p=3, tam=False):
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            return ""
        if isinstance(x, (float, np.floating)):
            return str(int(round(x))) if tam else f"{x:+.{p}f}"
        return str(x)
    def tablo(D: pd.DataFrame, kol: List[str]) -> List[str]:
        kol = [c for c in kol if c in D.columns]; L = ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
        for r in D[kol].itertuples(index=False):
            L.append("| " + " | ".join(f(v, tam=(c in TAM)) for c, v in zip(kol, r)) + " |")
        return L
    G, KAP, X, G4, T, KR = R["G"], R["KAP"], R["X"], R["G4"], R["T"], R["KR"]; V13 = K["_v13"]
    L = ["# K52 — ANALİST VERİSİ TARİHSEL DENETİMİ (v1.3, ön kayıt c33a10e)", "", "Kaynak: Yahoo Finance analist not günlüğü (yfinance `upgrades_downgrades`), çekim 29 Ekim 2026. Ücretsiz; EPS revizyonu, gerekçe, analist kişi kimliği, rapor kimliği YOK.", "",
         "## Kapsama (kaynak grubuna göre)", ""] + tablo(KAP[KAP.boyut == "kaynak"], ["deger", "hisse", "analist_kaydi_olan_hisse", "kapsama_oran", "kayit"])
    L += ["", "## Yıl yıl kayıt, zaman damgası ve alan doluluğu", ""] + tablo(KAP[KAP.boyut == "yil"], ["deger", "hisse", "kayit", "saat_var_oran", "hedef_var_oran", "eski_hedef_var_oran", "eski_tavsiye_var_oran", "olumlu_oran", "olumsuz_oran"])
    L += ["", "## Alanlar", ""] + tablo(KAP[KAP.boyut == "alan"], ["deger", "kaynak", "kayit", "eksik_oran", "baslangic", "bitis"])
    ol = KAP[KAP.boyut == "olay"]
    L += ["", "## Zaman sızıntısı ve güvenilirlik", "",
          "- Kural: olay günü d için yalnız tarih <= d-1 kayıtları (saat dilimi belgelenmediğinden aynı gün kayıtları kullanılmadı). Giriş d+1 açılışı. Hedef fiyatlar kayıt anındaki değer; sonraki güncelleme kullanılmadı. Aynı kurum aynı tarih tek kayıt.",
          "- Zaman damgası: kayıtların saat bilgisi olan payı yıl tablosundadır; saat 00:00 olan kayıtların gün içi sırası bilinmez. Saat dağılımı 10-16 UTC'de yoğundur (ABD piyasa öncesi notları), bu yüzden damga UTC kabul edildi; aynı gün kayıtları zaten dışarıda.",
          "- Tarihsel sürüm: Yahoo günlüğü olay kaydıdır; geriye dönük yeniden yazılıp yazılmadığı doğrulanamaz. Bu yüzden sonuçlar 'sağlayıcı günlüğü doğru kabul edilerek' okunmalıdır.",
          f"- Hayatta kalma / seçilim: P1 ve P2 olaylarında sembolün d'den önce kaydı olan pay {f(float(ol.kapsama_oran.iloc[0])) if len(ol) else ''}; kaydı olmayanlar G2b / G4b alt grubudur, olumsuz görüşle karıştırılmadı. Borsadan çıkmış şirketlerde veri çoğunlukla yoktur (yukarıdaki kaynak tablosu).",
          "- Ölçülemeyen hipotez: H1 (EPS revizyonu) — alan yok; karar verilmedi.", ""]
    open(os.path.join(A.cikti, "K51_ANALIST_TARIHSEL_VERI_DENETIMI.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    kok = os.path.dirname(os.path.abspath(globals().get("__file__", "COL_YOLU_ABD.py"))) or "."
    try:
        commit = subprocess.run(["git", "-C", kok, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "?"
    L = ["# K52 — GRAFİK İZİ + ANALİST REVİZYONLARI ARAŞTIRMASI (v1.3, ön kayıt c33a10e)", "",
         "K51 kararı (İZ DEĞİL) ve grafik kuralları değişmedi. 2023-26 bağımsız test değildir; üç dönemde tutma şartı sağlamlık kontrolüdür. AL sinyali yok.", "",
         f"- Veri: Yahoo not günlüğü {len(G)} kayıt, {G.sembol.nunique() if len(G) else 0} hisse; panel {R['panel_n']} likit hisse-gün, {R['hisse']} hisse; süre {R['sure_dk']} dk; kod {CY_SURUM}, commit {commit}.",
         "- Teyit = olay öncesi 20 işlem günü (tarih <= d-1) içinde olumlu revizyon (tavsiye yükseltme, hedef fiyat yükseltme ya da alım notuyla başlangıç) sayısı >= 1 ve olumsuzdan çok.",
         "- Birincil ölçüt Δ = ortalama(y - e_y | G1) - ortalama(y - e_y | G2a); y = +%20 / -%10 / 60 gün üst bariyer önce; e_y = K51 tabanı (aynı gün aynı oynaklık ondalığı). Koşullar: n >= 30, Δ >= +5 puan, ay kümeli alt uç > 0, net fark > 0, her dönemde.", "",
         "## Dört grup", "", "G1 = iz + teyit; G2a = iz + analist verisi var, teyit yok; G2b = iz + veri yok; G3 / G4a / G4b = iz yok (ÇEK dışı likit günlerden rastgele örnek). 'isabet' ağırlıklı; 'taban_ayarli' = isabet - K51 tabanı.", ""]
    L += tablo(G4, ["iz", "grup", "donem", "n", "hisse", "isabet", "taban_e_y", "taban_ayarli", "net", "kapsama_365_ort", "log_dv20_ort", "dd250_ort", "r60_ort", "boga_pay", "V_ABD_pay"])
    L += ["", "## Hipotez kararları", "", "| Kod | Hipotez | Hücre | Karar | Dönem kararları |", "|---|---|---|---|---|"]
    for r in T[T.donem.isin(("KARAR", "hepsi"))].itertuples():
        dk = getattr(r, "donem_kararlari", ""); dk = dk if isinstance(dk, str) else ""
        ek = f"sonra gelen pay {r.delta:+.3f}, n {int(r.n_a)}" if r.hucre == "zamanlama" else dk
        L.append(f"| {r.kod} | {r.hipotez} | {r.hucre} | **{r.karar_hucre}** | {ek} |")
    L += ["", "H1 (EPS revizyonu): ÖLÇÜLEMEZ, karar yok. H4'ün zamanlama satırı ('zamanlama' hücresi) olumlu revizyonların pencere dibinden >= %10 yükseliş SONRASI gelen payıdır.", "", "## Hücreler (Δ, aralıklar, net, p, Holm)", ""]
    L += tablo(T[T.donem != "KARAR"], ["kod", "hucre", "donem", "n_a", "n_b", "isabet_a", "isabet_b", "delta", "delta_alt", "delta_ust", "delta_alt_hisse_ceyrek", "delta_ust_hisse_ceyrek", "ham_fark", "net_fark", "net_fark_alt", "p", "holm_p_2023_26", "karar_hucre", "eslesen_pay"])
    L += ["", "## Kırılganlık (G1 - G2a)", ""] + tablo(KR, ["iz", "kirilim", "deger", "n_a", "n_b", "delta", "delta_alt", "delta_ust", "net_fark"])
    L += ["", "## Olumsuz bulgular ve sınırlar", "", "- Yalnız bugün Yahoo'da bulunan hisselerde veri var; G2b / G4b büyük ölçüde borsadan çıkmış ya da takip edilmeyen hisselerdir. G1 - G2b farkı (H0b) veri yokluğunun kendisiyle (hayatta kalma, küçüklük, takipsizlik) karışıktır; nedensel okunmaz.",
          "- Dengesizlik: G1'in r60 (son 60 gün getirisi) ve kapsama ortalaması G2a'dan yüksektir (dört grup tablosu); teyit alan izler daha önce yükselmeye başlamış ve daha çok takip edilen hisselerdir. K51 tabanı bunu ayarlamaz; H5 eşleştirmesi bunun için konmuştu ama eş bulunan olay sayısı 30'un altında kaldı (aynı gün ±10, aynı oynaklık ondalığı, likidite üçte biri, sektör, trend, |dd250| <= 0,10 ve kapsama üçte biri şartı G2a havuzunda çok az aday bırakıyor). Bu yüzden H5 KARARSIZ kaldı; ham Δ zaten eşik altında olduğu için karar değişmez.",
          "- Saat dilimi belirsiz; aynı gün kayıtları atıldığı için 'teyit' bazı gerçek teyitleri kaçırır (muhafazakâr).", "- Hedef fiyat yükseltmeleri çoğunlukla fiyat hareketini izler (H4 payı tabloda).",
          "- Kurum doğruluğu yalnız 'up' kayıtlarının geçmiş isabetiyle ölçüldü; kişi kimliği yok.", "", "## Yeniden üretim", "",
          f"- `R = cy_v13_calistir(gunluk_yol='.../yahoo_grades.pkl')`; günlük çekimi `yfinance.Ticker(s).upgrades_downgrades` ile (29 Ekim 2026). Tohum {V13['tohum']}, bootstrap {V13['boot']}. Çıktılar: K51_ANALIST_VERI_KAPSAMI.csv, K51_ANALIST_REVIZYONLARI.csv.gz, K51_GRAFIK_ANALIST_4GRUP.csv, K51_ANALIST_EK_KATKI_TESTI.csv, bu belge ve K51_ANALIST_TARIHSEL_VERI_DENETIMI.md."]
    open(os.path.join(A.cikti, "K51_GRAFIK_ANALIST_ARASTIRMA.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


# ---------------------------------------------------------------- v1.4 K53 BİLGİ DİRENCİ (BDS), ANALİST DAĞINIKLIĞI (ADE), KARAR GECİKMESİ (KGS)
# Ön kayıt: arastirma_cikti/col_yolu_abd/K53_onkayit.md (commit 488a407). K51 kuralları ve kararı değişmez; keşif deneyi, AL sinyali yok.
CY_V14: Dict[str, Any] = {
    "tohum": 514, "pencere": 5, "kume_gun": 20, "sb_gun": 10, "atr_gun": 20, "kgs_esik": 0.05, "kgs_azami": 20, "ade_gun": 90, "ade_min_kurum": 3,
    "h4_yukselis": 0.10, "genel_n": 60000, "olay_gecikme_gun": 4, "n_min": 30, "fark_esik": 0.05, "boot": 2000,
    "donem": (("2016-22", "2016-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-06-05")),
    "yillar": ((2023, "2023-01-01", "2023-12-31"), (2024, "2024-01-01", "2024-12-31"), (2025, "2025-01-01", "2025-12-31"), (2026, "2026-01-01", "2026-06-05")),
}


def cy_v14_sekil(C: np.ndarray, H: np.ndarray, L: np.ndarray, Vv: np.ndarray, R: np.ndarray, rs: np.ndarray, rk: np.ndarray, i: int,
                 K: Dict[str, Any] = CY_V14) -> Dict[str, Any]:
    """Karar günü i (pencere [i-4, i] = [d0, d0+4]) için ön kayıt 2 ölçüleri: tepki (r5, SPY / sektör göreli, hacim, aşağı gün, ATR değişimi),
    satış baskısı A10 = [i-9, i] vs B10 = [i-19, i-10] (negatif oran, negatif büyüklük, aşağı hacim payı, CLV) ve BDS (0-3). Yalnız i'ye kadar veri.
    Eksik SPY / OHLC / hacim ya da ATR20 = 0 sıfır sayılmaz: {'gecerli': False, 'neden': ...} döner (ön kayıt EK 1)."""
    W = K["pencere"]; a0 = i - W + 1; n20 = K["atr_gun"]; n10 = K["sb_gun"]; lo = a0 - max(n20, 2 * n10) - 1
    if lo < 0 or i >= len(C):
        return {"gecerli": False, "neden": "geçmiş kısa"}
    c0 = C[a0 - 1]
    if not (np.isfinite(c0) and c0 > 0):
        return {"gecerli": False, "neden": "kapanış eksik"}
    if not (np.all(np.isfinite(C[lo:i + 1])) and np.all(np.isfinite(H[lo:i + 1])) and np.all(np.isfinite(L[lo:i + 1]))):
        return {"gecerli": False, "neden": "OHLC eksik"}
    if not np.all(np.isfinite(rs[a0:i + 1])):
        return {"gecerli": False, "neden": "SPY eksik"}
    if not (np.all(np.isfinite(Vv[lo:i + 1])) and np.sum(Vv[a0 - n20:a0]) > 0 and np.sum(Vv[i - 2 * n10 + 1:i + 1]) > 0):
        return {"gecerli": False, "neden": "hacim eksik"}
    r5 = C[i] / c0 - 1; spy5 = float(np.prod(1 + rs[a0:i + 1]) - 1); rel_spy = r5 - spy5
    sek5 = float(np.prod(1 + rk[a0:i + 1]) - 1) if np.all(np.isfinite(rk[a0:i + 1])) else np.nan; rel_sek = r5 - sek5 if np.isfinite(sek5) else np.nan
    vB = Vv[a0 - n20:a0]; hacim_deg = float(np.mean(Vv[a0:i + 1]) / np.mean(vB) - 1) if np.mean(vB) > 0 else np.nan
    asagi_gun = int(np.sum(R[a0:i + 1] < 0))
    Cp = np.r_[np.nan, C[:-1]]; TR = np.nanmax(np.c_[H - L, np.abs(H - Cp), np.abs(L - Cp)], axis=1)
    atr5 = float(np.nanmean(TR[a0:i + 1])); atr20 = float(np.nanmean(TR[a0 - n20:a0]))
    if not (np.isfinite(atr20) and atr20 > 0 and np.isfinite(atr5)):
        return {"gecerli": False, "neden": "ATR sıfır / eksik"}
    atr_deg = atr5 / atr20 - 1
    def sb(lo, hi):
        r = R[lo:hi + 1]; v = Vv[lo:hi + 1]; neg = r < 0; rng_ = H[lo:hi + 1] - L[lo:hi + 1]; ok = rng_ > 0
        clv = float(np.mean(((C[lo:hi + 1] - L[lo:hi + 1])[ok]) / rng_[ok])) if ok.any() else np.nan
        return (float(neg.mean()), float((-r[neg]).mean()) if neg.any() else 0.0, float(v[neg].sum() / v.sum()) if v.sum() > 0 else np.nan, clv)
    A_ = sb(i - n10 + 1, i); B_ = sb(i - 2 * n10 + 1, i - n10)
    iyi = int(A_[0] < B_[0]) + int(A_[1] < B_[1]) + int(np.isfinite(A_[2]) and np.isfinite(B_[2]) and A_[2] < B_[2]) + int(np.isfinite(A_[3]) and np.isfinite(B_[3]) and A_[3] > B_[3])
    fiyat_zayif = bool(rel_spy <= 0); satis_azaliyor = bool(iyi >= 3); oyn_dusuyor = bool(np.isfinite(atr_deg) and atr_deg < 0)
    return {"gecerli": True, "neden": "", "r5": float(r5), "rel_spy5": float(rel_spy), "rel_sek5": rel_sek, "hacim_deg": hacim_deg, "asagi_gun": asagi_gun, "atr_deg": atr_deg,
            "neg_oran_A": A_[0], "neg_buyukluk_A": A_[1], "asagi_hacim_payi_A": A_[2], "clv_A": A_[3], "neg_oran_B": B_[0], "neg_buyukluk_B": B_[1],
            "asagi_hacim_payi_B": B_[2], "clv_B": B_[3], "iyilesme": iyi, "fiyat_zayif": fiyat_zayif, "satis_azaliyor": satis_azaliyor,
            "oyn_dusuyor": oyn_dusuyor, "bds": int(fiyat_zayif) + int(satis_azaliyor) + int(oyn_dusuyor)}


def cy_v14_kgs(C: np.ndarray, S: np.ndarray, d0: int, K: Dict[str, Any] = CY_V14, baslangic: str = "once") -> int:
    """Karar gecikmesi: başlangıç kapanışından itibaren SPY göreli birikimli getirinin ilk kez >= kgs_esik olduğu gün k (1..kgs_azami); yoksa kgs_azami + 1.
    baslangic 'once' = d0-1 kapanışı (KGS-önce, karar ölçüsü); 'sonra' = d0 kapanışı (KGS-sonra, ön kayıt EK 3, yalnız bilgi)."""
    b = d0 - 1 if baslangic == "once" else d0; c0 = C[b]; s0 = S[b]; M = K["kgs_azami"]
    if not (np.isfinite(c0) and c0 > 0):
        return M + 1
    for k in range(1, M + 1):
        j = b + k
        if j >= len(C):
            return M + 1
        if np.isfinite(C[j]) and np.isfinite(S[j]) and s0 > 0 and (C[j] / c0 - 1) - (S[j] / s0 - 1) >= K["kgs_esik"]:
            return k
    return M + 1


def cy_v14_olay_gunleri(idx: np.ndarray, tarihler: np.ndarray, K: Dict[str, Any] = CY_V14) -> Tuple[np.ndarray, np.ndarray]:
    """Olumlu kayıt tarihleri -> işlem günü indeksleri (kayıt tarihine eşit ya da sonraki ilk gün, en çok olay_gecikme_gun takvim günü).
    Dönüş: (tüm olumlu kayıtların d0 dizisi, kümeleme sonrası 'ilk' olaylar: önceki kume_gun işlem gününde başka olumlu kayıt yok)."""
    t = np.sort(np.unique(tarihler.astype("datetime64[ns]"))); j = np.searchsorted(idx, t); ok = j < len(idx)
    j = j[ok]; t = t[ok]; ok2 = (idx[j] - t) <= np.timedelta64(K["olay_gecikme_gun"], "D"); hepsi = np.unique(j[ok2])
    ilk = [d for d in hepsi if not np.any((hepsi >= d - K["kume_gun"]) & (hepsi < d))]
    return hepsi, np.array(ilk, dtype=int)


def cy_v14_ade(g: pd.DataFrame, gun: np.datetime64, K: Dict[str, Any] = CY_V14) -> Tuple[float, int]:
    """Analist dağınıklığı: [gun - ade_gun, gun] kayıtlarından kurum başına en son hedef fiyat; >= ade_min_kurum kurum varsa std / ortalama."""
    w = g[(g.tarih.to_numpy() <= gun) & (g.tarih.to_numpy() > gun - np.timedelta64(K["ade_gun"], "D")) & g.hedef.notna() & (g.hedef > 0)]
    if not len(w):
        return np.nan, 0
    son = w.sort_values("tarih").groupby("kurum_n").hedef.last(); n = int(len(son))
    return (float(son.std(ddof=0) / son.mean()) if n >= K["ade_min_kurum"] and son.mean() > 0 else np.nan), n


def cy_v14_calistir(A: Optional[CYAyar] = None, K: Dict[str, Any] = CY, gunluk_yol: Optional[str] = None) -> Dict[str, Any]:
    """K53 sürücü: panel + Yahoo günlüğü -> olaylar (ilk olumlu revizyon), BDS / ADE / KGS, G1-G5, T1-T8, Holm, kırılganlık, çıktılar."""
    A = A or CYAyar(); os.makedirs(A.cikti, exist_ok=True); K = {**K, "_v12": CY_V12, "_v13": CY_V13, "_v14": CY_V14}; V14 = CY_V14; t0 = time.time()
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    rng = np.random.default_rng(V14["tohum"]); PN = cy_v13_panel(A, K); P, V, EV, evp = PN["P"], PN["V"], PN["EV"], PN["evp"]; sek = PN["sektor"]
    cylog.info("v1.4 panel %d satır, %d hisse (%ds)", len(P), P.sembol.nunique(), time.time() - t0)
    gy = gunluk_yol or os.path.join(A.veri, "analist", "yahoo_grades.pkl")
    if not os.path.exists(gy):
        raise FileNotFoundError(f"analist günlüğü yok: {gy}")
    G = cy_v13_gunluk_yukle(gy, CY_V13); Gs = {s_: g for s_, g in G.groupby("sembol")} if len(G) else {}
    # endeks ve sektör günlük getirileri
    En = K.get("_endeks", pd.DataFrame()); spy = En["SPY"].dropna() if isinstance(En, pd.DataFrame) and "SPY" in En else pd.Series(dtype=float)
    if not len(spy):
        raise RuntimeError("SPY serisi yok (endeks.pkl)")
    spy.index = pd.DatetimeIndex(spy.index).tz_localize(None) if getattr(spy.index, "tz", None) is not None else pd.DatetimeIndex(spy.index)
    getiri = pd.DataFrame({s_: d.Close.pct_change() for s_, d in V.items()}); sek_map = pd.Series({s_: sek.get(s_, "bilinmiyor") for s_ in getiri.columns})
    sek_get = {}
    for sk, kol in sek_map.groupby(sek_map).groups.items():
        if sk != "bilinmiyor":
            sek_get[sk] = getiri[list(kol)].mean(axis=1, skipna=True)
    del getiri
    # panel satır arama: sembol -> (başlangıç, bitiş) ve i dizisi
    Pi = P.i.to_numpy(); sem_arr = P.sembol.to_numpy(); sinir = {}
    bas = 0
    for k_ in range(1, len(P) + 1):
        if k_ == len(P) or sem_arr[k_] != sem_arr[bas]:
            sinir[sem_arr[bas]] = (bas, k_); bas = k_
    def panel_satir(s_, i):
        if s_ not in sinir:
            return -1
        a, b = sinir[s_]; j = a + int(np.searchsorted(Pi[a:b], i))
        return j if (j < b and Pi[j] == i) else -1
    Py = P.y.to_numpy(float); Pn = P.net.to_numpy(float); Pey = P.e_y.to_numpy(float); Pen = P.e_net.to_numpy(float); Ptar = P.tarih.to_numpy()
    PP1 = P.P1.to_numpy(); PCEK = P.cek_ham.to_numpy() | P.CEK.to_numpy()
    # olaylar
    olaylar = []; sayac = {"kayit_olumlu": 0, "d0_eslesmeyen": 0, "ilk_olay": 0, "seri_sonu": 0, "panel_yok": 0, "sekil_yok": 0, "olcen": 0}; neden_say = {}; olumlu_d0 = {}
    Pvd = P.vd.to_numpy(); Plt = P["lt"].to_numpy(); Pdd = P.dd250.to_numpy(float); Pvol = P.vol60.to_numpy(float); Pldv = P.log_dv20.to_numpy(float)
    Pr60 = P.r60.to_numpy(float); Par20 = P.ar20.to_numpy(float); Ptr = P.trend.to_numpy(); Prej = P.rejim.to_numpy()
    def panel_oz(j):
        return {"vd": int(Pvd[j]), "lt": int(Plt[j]), "dd250": Pdd[j], "vol60": Pvol[j], "log_dv20": Pldv[j], "r60": Pr60[j], "ar20": Par20[j], "trend": int(Ptr[j]), "rejim": Prej[j]}
    def kapsama(g, gun):
        if g is None:
            return 0
        t = g.tarih.to_numpy(); gun = np.datetime64(gun); return int(((t <= gun) & (t > gun - np.timedelta64(365, "D"))).sum())
    for s_, d in V.items():
        g = Gs.get(s_)
        if g is None or s_ not in evp.index:
            continue
        go = g[g.olumlu]
        if not len(go):
            continue
        idx = d.index.to_numpy().astype("datetime64[ns]"); C = d.Close.to_numpy(float); H = d.High.to_numpy(float); L = d.Low.to_numpy(float); Vv = d.Volume.to_numpy(float)
        R = np.r_[np.nan, C[1:] / C[:-1] - 1]; S = spy.reindex(d.index, method="ffill").to_numpy(float); rs = np.r_[np.nan, S[1:] / S[:-1] - 1]
        sk = sek.get(s_, "bilinmiyor"); rk = sek_get[sk].reindex(d.index).to_numpy(float) if sk in sek_get else np.full(len(C), np.nan)
        hepsi, ilk = cy_v14_olay_gunleri(idx, go.tarih.to_numpy(), V14); olumlu_d0[s_] = hepsi; sayac["kayit_olumlu"] += len(go); sayac["d0_eslesmeyen"] += int(len(np.unique(go.tarih)) - len(hepsi))
        W = V14["pencere"]
        for d0 in ilk:
            sayac["ilk_olay"] += 1; i = int(d0 + W - 1)
            if i >= len(C):
                sayac["seri_sonu"] += 1; continue
            j = panel_satir(s_, i)
            if j < 0:
                sayac["panel_yok"] += 1; continue
            f = cy_v14_sekil(C, H, L, Vv, R, rs, rk, i, V14)
            if not f["gecerli"]:
                sayac["sekil_yok"] += 1; neden_say[f["neden"]] = neden_say.get(f["neden"], 0) + 1; continue
            kgs = cy_v14_kgs(C, S, int(d0), V14); ik = int(d0 + min(kgs, V14["kgs_azami"])); jk = panel_satir(s_, ik)
            kgs2 = cy_v14_kgs(C, S, int(d0), V14, "sonra"); ik2 = int(d0 + min(kgs2, V14["kgs_azami"])); jk2 = panel_satir(s_, ik2)
            ade, ade_n = cy_v14_ade(g, idx[d0], V14)
            c20 = C[max(0, d0 - 20):d0]; sonra_yukselis = bool(len(c20) and C[d0 - 1] >= np.nanmin(c20) * (1 + V14["h4_yukselis"]))
            olaylar.append({"sembol": s_, "d0_tarih": idx[d0], "tarih": Ptar[j], "i": i, "y": Py[j], "net": Pn[j], "e_y": Pey[j], "e_net": Pen[j], "P1": bool(PP1[j]), "CEK": bool(PCEK[j]),
                            "kgs": kgs, "kgs_kova": "hızlı" if kgs <= 5 else ("geç" if kgs <= V14["kgs_azami"] else "yok"), "kgs_tarih": Ptar[jk] if jk >= 0 else pd.NaT,
                            "y_kgs": Py[jk] if jk >= 0 else np.nan, "net_kgs": Pn[jk] if jk >= 0 else np.nan, "e_y_kgs": Pey[jk] if jk >= 0 else np.nan, "e_net_kgs": Pen[jk] if jk >= 0 else np.nan,
                            "kgs_sonra": kgs2, "kgs_sonra_kova": "hızlı" if kgs2 <= 5 else ("geç" if kgs2 <= V14["kgs_azami"] else "ulaşmadı"), "kgs_sonra_tarih": Ptar[jk2] if jk2 >= 0 else pd.NaT,
                            "y_kgs_sonra": Py[jk2] if jk2 >= 0 else np.nan, "net_kgs_sonra": Pn[jk2] if jk2 >= 0 else np.nan, "e_y_kgs_sonra": Pey[jk2] if jk2 >= 0 else np.nan, "e_net_kgs_sonra": Pen[jk2] if jk2 >= 0 else np.nan,
                            "ade": ade, "ade_kurum": ade_n, "sonra_yukselis": sonra_yukselis, "kapsama_365": kapsama(g, idx[d0]),
                            "n_kurum_d0": int((go.tarih.to_numpy() <= idx[d0]).sum() - (go.tarih.to_numpy() < idx[d0] - np.timedelta64(4, "D")).sum()), **panel_oz(j), **f})
            sayac["olcen"] += 1
    X = pd.DataFrame(olaylar)
    if not len(X):
        raise RuntimeError("K53: olay yok")
    X["tarih"] = pd.to_datetime(X.tarih).astype("datetime64[ns]"); X["kgs_tarih"] = pd.to_datetime(X.kgs_tarih); X["agirlik"] = X.sembol.map(evp.agirlik).fillna(1.0).astype(float)
    X["kaynak"] = X.sembol.map(evp.kaynak); X["sektor"] = X.sembol.map(sek).fillna("bilinmiyor"); X["grup"] = np.where(X.bds == 3, "G1", "G2")
    sayac["olculemeyen_neden"] = neden_say; cylog.info("v1.4 olay: %s (%ds)", sayac, time.time() - t0)
    # kontroller: G3 (P1 ∪ ÇEK, olumlu yok), G4 (rastgele, olumlu yok), G5 (G4 ∧ BDS 3). Olumlu yok = [i-24, i] aralığında olumlu d0 yok.
    rng_g = np.random.default_rng(V14["tohum"]); genel_m = ~PCEK & ~PP1; genel_ix = np.flatnonzero(genel_m); genel_ix = genel_ix[rng_g.random(len(genel_ix)) < min(1.0, V14["genel_n"] / max(len(genel_ix), 1))]
    g3_ix = np.flatnonzero(PP1 | PCEK); kont = []; cache = {}; kont_say = {"G3_aday": int(len(g3_ix)), "G4_aday": int(len(genel_ix)), "olumlu_var": 0, "olculemeyen": 0}
    def seri(s_):
        if s_ not in cache:
            d = V[s_]; C = d.Close.to_numpy(float); S = spy.reindex(d.index, method="ffill").to_numpy(float); sk = sek.get(s_, "bilinmiyor")
            cache[s_] = (C, d.High.to_numpy(float), d.Low.to_numpy(float), d.Volume.to_numpy(float), np.r_[np.nan, C[1:] / C[:-1] - 1], np.r_[np.nan, S[1:] / S[:-1] - 1],
                         sek_get[sk].reindex(d.index).to_numpy(float) if sk in sek_get else np.full(len(C), np.nan))
        return cache[s_]
    for ad, ixs in (("G3", g3_ix), ("G4", genel_ix)):
        for j in ixs:
            s_ = sem_arr[j]; i = int(Pi[j]); od = olumlu_d0.get(s_)
            if od is not None and np.any((od >= i - V14["kume_gun"] - V14["pencere"] + 1) & (od <= i)):
                kont_say["olumlu_var"] += 1; continue
            if len(cache) > 400:
                cache.clear()
            C, H, L, Vv, R, rs, rk = seri(s_); f = cy_v14_sekil(C, H, L, Vv, R, rs, rk, i, V14)
            if not f["gecerli"]:
                kont_say["olculemeyen"] += 1; continue
            kont.append({"sembol": s_, "tarih": Ptar[j], "i": i, "y": Py[j], "net": Pn[j], "e_y": Pey[j], "e_net": Pen[j], "P1": bool(PP1[j]), "CEK": bool(PCEK[j]), "grup": ad,
                         "kapsama_365": kapsama(Gs.get(s_), Ptar[j]), **panel_oz(j), **f})
    del cache
    Xk = pd.DataFrame(kont); Xk["tarih"] = pd.to_datetime(Xk.tarih).astype("datetime64[ns]"); Xk["agirlik"] = Xk.sembol.map(evp.agirlik).fillna(1.0).astype(float)
    Xk["kaynak"] = Xk.sembol.map(evp.kaynak); Xk["sektor"] = Xk.sembol.map(sek).fillna("bilinmiyor"); Xk.loc[(Xk.grup == "G4") & (Xk.bds == 3), "grup"] = "G5"
    XX = pd.concat([X, Xk], ignore_index=True); XX["donem"] = ""
    for dn, a, b in V14["donem"]:
        XX.loc[(XX.tarih >= a) & (XX.tarih <= b), "donem"] = dn
    XX = XX[XX.donem != ""].reset_index(drop=True); XX = XX[XX.y.notna() & XX.e_y.notna()].reset_index(drop=True)
    sayac["kontrol"] = kont_say; cylog.info("v1.4 kontrol %d satır; toplam %d (%ds)", len(Xk), len(XX), time.time() - t0)
    kol = ["grup", "sembol", "d0_tarih", "tarih", "i", "donem", "kaynak", "sektor", "y", "net", "e_y", "e_net", "agirlik", "P1", "CEK", "bds", "fiyat_zayif", "satis_azaliyor", "oyn_dusuyor",
           "r5", "rel_spy5", "rel_sek5", "hacim_deg", "asagi_gun", "atr_deg", "neg_oran_A", "neg_buyukluk_A", "asagi_hacim_payi_A", "clv_A", "neg_oran_B", "neg_buyukluk_B",
           "asagi_hacim_payi_B", "clv_B", "iyilesme", "kgs", "kgs_kova", "kgs_tarih", "y_kgs", "net_kgs", "e_y_kgs", "e_net_kgs", "kgs_sonra", "kgs_sonra_kova", "kgs_sonra_tarih",
           "y_kgs_sonra", "net_kgs_sonra", "e_y_kgs_sonra", "e_net_kgs_sonra", "ade", "ade_kurum", "sonra_yukselis", "kapsama_365", "n_kurum_d0", "vd", "lt", "vol60", "log_dv20", "dd250", "r60", "ar20", "trend", "rejim"]
    XX[XX.grup.isin(["G1", "G2"])][[c for c in kol if c in XX.columns]].to_csv(os.path.join(A.cikti, "K53_OLAYLAR.csv.gz"), index=False)   # kontrol satırları (190 bin) repoya girmez; kod yeniden üretir
    # grup tablosu
    GR = []
    for (gr, dn), g in XX.groupby(["grup", "donem"]):
        w = g.agirlik.to_numpy(float)
        GR.append({"grup": gr, "donem": dn, "n": len(g), "hisse": g.sembol.nunique(), "isabet": float(np.average(g.y, weights=w)), "taban_e_y": float(np.average(g.e_y, weights=w)),
                   "taban_ayarli": float(np.average(g.y - g.e_y, weights=w)), "net": float(np.average(g.net, weights=w)), "bds_ort": float(g.bds.mean()), "rel_spy5_ort": float(g.rel_spy5.mean()),
                   "atr_deg_ort": float(np.nanmean(g.atr_deg)), "iyilesme_ort": float(g.iyilesme.mean()), "P1_pay": float(g.P1.mean()), "V_ABD_pay": float((g.kaynak == "V_ABD").mean())})
    for (kv, dn), g in X[X.tarih.notna()].assign(donem=lambda t: pd.cut(t.tarih, bins=[pd.Timestamp("2016-01-01"), pd.Timestamp("2023-01-01"), pd.Timestamp("2024-01-01"), pd.Timestamp("2026-06-06")], right=False, labels=[d_[0] for d_ in V14["donem"]])).groupby(["kgs_kova", "donem"], observed=True):
        GR.append({"grup": f"KGS {kv}", "donem": str(dn), "n": len(g), "hisse": g.sembol.nunique(), "isabet": float(np.nanmean(g.y_kgs)) if g.y_kgs.notna().any() else np.nan,
                   "taban_e_y": float(np.nanmean(g.e_y_kgs)) if g.e_y_kgs.notna().any() else np.nan, "bds_ort": float(g.bds.mean())})
    GR = pd.DataFrame(GR); GR.to_csv(os.path.join(A.cikti, "K53_GRUPLAR.csv"), index=False)
    # testler
    T = []; p23 = {}; Kf = {"boot": V14["boot"], "n_min": V14["n_min"], "fark_esik": V14["fark_esik"]}
    def test(kod, ad, Aset, Bset, aile=True):
        kar = []
        for dn, a, b in V14["donem"]:
            h = cy_v13_fark(Aset[(Aset.tarih >= a) & (Aset.tarih <= b)], Bset[(Bset.tarih >= a) & (Bset.tarih <= b)], Kf, rng); kr = cy_v13_karar(h, Kf) if "delta" in h else "YETERSİZ ÖRNEKLEM"
            T.append({"kod": kod, "test": ad, "donem": dn, **h, "karar_hucre": kr}); kar.append(kr)
        h23 = cy_v13_fark(Aset[Aset.tarih >= "2023-01-01"], Bset[Bset.tarih >= "2023-01-01"], Kf, rng)
        if aile:
            p23[kod] = h23.get("p", np.nan)
        T.append({"kod": kod, "test": ad, "donem": "2023-26 (Holm için)", **h23, "karar_hucre": cy_v13_karar(h23, Kf) if "delta" in h23 else "YETERSİZ ÖRNEKLEM"})
        son_k = "YETERSİZ ÖRNEKLEM" if "YETERSİZ ÖRNEKLEM" in kar else ("DESTEKLENİYOR (KEŞİFSEL; 2023-26 bağımsız değil)" if all(k_ == "TUTAR" for k_ in kar) else ("DESTEKLENMİYOR (TERS YÖN)" if "TERS YÖN" in kar else "DESTEKLENMİYOR"))
        T.append({"kod": kod, "test": ad, "donem": "KARAR", "karar_hucre": son_k, "donem_kararlari": " | ".join(f"{d_[0]}: {k_}" for d_, k_ in zip(V14["donem"], kar))}); return son_k
    E = XX[XX.grup.isin(["G1", "G2"])]; G1 = E[E.grup == "G1"]; G2 = E[E.grup == "G2"]
    k1 = test("T1", "G1 (BDS 3) − G2 (BDS < 3)", G1, G2)
    test("T1b", "BDS 3 − BDS 0 (doz-yanıt)", G1, E[E.bds == 0])
    test("T1c", "BDS 2 − BDS 0 (doz-yanıt)", E[E.bds == 2], E[E.bds == 0], aile=False)
    test("T2", "G1 − G3 (grafik var, revizyon yok)", G1, XX[XX.grup == "G3"])
    test("T3", "G1 − G4 (hiçbiri)", G1, XX[XX.grup == "G4"])
    k4 = test("T4", "G1 − G5 (aynı şekil BDS 3, bilgi yok) [çürütme A]", G1, XX[XX.grup == "G5"])
    test("T4b", "G5 (şekil, bilgi yok) − G4 (hiçbiri) [desenin kendi etkisi]", XX[XX.grup == "G5"], XX[XX.grup == "G4"], aile=False)
    # KGS: karar anı tepki günü; etiket y_kgs
    XK = X[X.y_kgs.notna() & X.e_y_kgs.notna()].copy(); XK["tarih"] = pd.to_datetime(XK.kgs_tarih).astype("datetime64[ns]")
    XK = XK.rename(columns={"y": "y_d4", "net": "net_d4", "e_y": "e_y_d4", "e_net": "e_net_d4"}).rename(columns={"y_kgs": "y", "net_kgs": "net", "e_y_kgs": "e_y", "e_net_kgs": "e_net"})
    k5 = test("T5", "KGS geç (6-20) − hızlı (1-5), karar anı tepki günü", XK[XK.kgs_kova == "geç"], XK[XK.kgs_kova == "hızlı"])
    test("T5b", "KGS geç − yok (20 günde tepki yok; karar d0+20)", XK[XK.kgs_kova == "geç"], XK[XK.kgs_kova == "yok"], aile=False)
    test("T5c", "KGS hızlı − yok", XK[XK.kgs_kova == "hızlı"], XK[XK.kgs_kova == "yok"], aile=False)
    XA = X[X.ade.notna()].copy()
    if len(XA) >= 90:
        q = XA.ade.quantile([1 / 3, 2 / 3]).to_numpy(); k6 = test("T6", f"ADE üst üçte bir (> {q[1]:.3f}) − alt üçte bir (<= {q[0]:.3f})", XA[XA.ade > q[1]], XA[XA.ade <= q[0]])
    else:
        k6 = "YETERSİZ ÖRNEKLEM"; T.append({"kod": "T6", "test": "ADE", "donem": "KARAR", "karar_hucre": k6, "n_a": len(XA)})
    T.append({"kod": "T6", "test": "ADE ölçülebilen olay payı (>= 3 kurum hedefi)", "donem": "hepsi", "n_a": len(XA), "n_b": len(X), "delta": float(len(XA) / len(X)), "karar_hucre": "bilgi"})
    # T7 çapraz: BDS 3 olaylarda KGS kova payları
    for b_ in (3, 0):
        g = X[X.bds == b_]; pay = g.kgs_kova.value_counts(normalize=True)
        T.append({"kod": "T7", "test": f"BDS {b_} olaylarda KGS kova payı: hızlı / geç / yok", "donem": "hepsi", "n_a": len(g), "delta": float(pay.get("hızlı", 0)), "delta_alt": float(pay.get("geç", 0)), "delta_ust": float(pay.get("yok", 0)), "karar_hucre": "bilgi"})
    test("T7b", "geç tepki ∧ BDS 3 − geri kalan olaylar (karar anı tepki günü)", XK[(XK.kgs_kova == "geç") & (XK.bds == 3)], XK[~((XK.kgs_kova == "geç") & (XK.bds == 3))], aile=False)
    sy = G1.sonra_yukselis.fillna(False).astype(bool)                       # concat sonrası nesne türü olabilir
    test("T8", "G1 içinde revizyon yükselişten SONRA − ÖNCE gelen [çürütme B]", G1[sy], G1[~sy], aile=False)
    for bil in ("fiyat_zayif", "satis_azaliyor", "oyn_dusuyor"):
        b_ = E[bil].fillna(False).astype(bool)
        test(f"BIL-{bil}", f"olaylarda {bil} = 1 − 0 (bileşen tek başına)", E[b_], E[~b_], aile=False)
    # EK 3: KGS-sonra (bilgi; karar yalnız KGS-önce T5)
    XS = X[X.y_kgs_sonra.notna() & X.e_y_kgs_sonra.notna()].copy(); XS["tarih"] = pd.to_datetime(XS.kgs_sonra_tarih).astype("datetime64[ns]")
    XS = XS.drop(columns=["y", "net", "e_y", "e_net"]).rename(columns={"y_kgs_sonra": "y", "net_kgs_sonra": "net", "e_y_kgs_sonra": "e_y", "e_net_kgs_sonra": "e_net"})
    test("EK-KGS-sonra", "KGS-sonra geç (6-20) − hızlı (1-5), başlangıç d0 kapanışı [bilgi, EK 3]", XS[XS.kgs_sonra_kova == "geç"], XS[XS.kgs_sonra_kova == "hızlı"], aile=False)
    test("EK-KGS-sonra-b", "KGS-sonra geç − ulaşmadı [bilgi, EK 3]", XS[XS.kgs_sonra_kova == "geç"], XS[XS.kgs_sonra_kova == "ulaşmadı"], aile=False)
    for kv, g in X.groupby("kgs_sonra_kova"):
        T.append({"kod": "EK-KGS-sonra", "test": f"KGS-sonra kova payı: {kv}", "donem": "hepsi", "n_a": len(g), "delta": float(len(g) / len(X)), "karar_hucre": "bilgi"})
    # EK 2: G1 − eşleşmiş G5 (negatif kontrol; nedensel kanıt değil); yöntem v1.2 eşleştirme, sabit
    G5 = XX[XX.grup == "G5"]; M15 = cy_v12_eslestir(XX, G1, G5, K, 3, 10, rng, es_imza=False); G1e = pd.concat([G1, M15], axis=1); es_pay = float((G1e.kontrol_n > 0).mean()) if len(G1e) else np.nan
    G1e = G1e[G1e.kontrol_n > 0]
    for dn, a, b in V14["donem"]:
        D = G1e[(G1e.tarih >= a) & (G1e.tarih <= b)]
        if len(D) < V14["n_min"]:
            T.append({"kod": "EK-G1-G5-eslesik", "test": "G1 − eşleşmiş G5 (aynı gün ±10, oynaklık ondalığı, likidite üçte biri, trend, dd250, sektör; negatif kontrol)", "donem": dn, "n_a": len(D), "karar_hucre": "YETERSİZ ÖRNEKLEM", "eslesen_pay": es_pay}); continue
        h = cy_v12_hucre(D, K, rng)
        T.append({"kod": "EK-G1-G5-eslesik", "test": "G1 − eşleşmiş G5 (aynı gün ±10, oynaklık ondalığı, likidite üçte biri, trend, dd250, sektör; negatif kontrol)", "donem": dn, "n_a": h["n"], "hisse_a": h["hisse_n"],
                  "isabet_a": h["isabet"], "isabet_b": h["kontrol"], "delta": h["fark"], "delta_alt": h["fark_alt"], "delta_ust": h["fark_ust"], "delta_alt_hisse_ceyrek": h["fark_alt_hisse_ceyrek"],
                  "delta_ust_hisse_ceyrek": h["fark_ust_hisse_ceyrek"], "net_fark": h["net_fark"], "p": h["p"], "karar_hucre": cy_v12_karar(h, K) + " (bilgi)", "eslesen_pay": es_pay})
    # EK 2 / 5: denge tablosu (grup × dönem) ve G1'e göre standartlaştırılmış ortalama farkları
    DN = []; dk = ["dd250", "vol60", "log_dv20", "r60", "kapsama_365"]
    for (gr, dn), g in XX.groupby(["grup", "donem"]):
        DN.append({"grup": gr, "donem": dn, "n": len(g), "yil_ort": float(g.tarih.dt.year.mean()), "en_buyuk_sektor": str(g.sektor.value_counts().index[0]) if len(g) else "", "en_buyuk_sektor_pay": float(g.sektor.value_counts(normalize=True).iloc[0]) if len(g) else np.nan,
                   "sektor_bilinmiyor_pay": float((g.sektor == "bilinmiyor").mean()), "lt_ort": float(g["lt"].mean()), "vd_ort": float(g.vd.mean()), "dd250_ort": float(g.dd250.mean()), "vol60_ort": float(g.vol60.mean()),
                   "log_dv20_ort": float(g.log_dv20.mean()), "r60_ort": float(g.r60.mean()), "kapsama_365_ort": float(g.kapsama_365.mean()), "boga_pay": float((g.rejim == "BOĞA").mean()), "V_ABD_pay": float((g.kaynak == "V_ABD").mean())})
    g1 = XX[XX.grup == "G1"]
    for gr in ("G2", "G3", "G4", "G5"):
        g = XX[XX.grup == gr]; row = {"grup": f"SMD G1 vs {gr}", "donem": "hepsi", "n": len(g)}
        for c in dk:
            sd = np.sqrt((g1[c].var() + g[c].var()) / 2); row[c + "_smd"] = float((g1[c].mean() - g[c].mean()) / sd) if np.isfinite(sd) and sd > 0 else np.nan
        row["boga_pay_fark"] = float((g1.rejim == "BOĞA").mean() - (g.rejim == "BOĞA").mean()); row["lt_ort_fark"] = float(g1["lt"].mean() - g["lt"].mean()); row["vd_ort_fark"] = float(g1.vd.mean() - g.vd.mean()); DN.append(row)
    if len(G1e):
        row = {"grup": "SMD G1 (eşleşen) vs eşleşmiş G5", "donem": "hepsi", "n": len(G1e)}
        kim = G1e.kontrol_kimlik.str.split(";").explode(); kim = kim[kim.str.len() > 0]; ix5 = kim.str.split("@").str[1].astype(int)
        g5e = G5.loc[G5.index.intersection(ix5.to_numpy())]
        for c in dk:
            sd = np.sqrt((G1e[c].var() + g5e[c].var()) / 2); row[c + "_smd"] = float((G1e[c].mean() - g5e[c].mean()) / sd) if np.isfinite(sd) and sd > 0 else np.nan
        row["boga_pay_fark"] = float((G1e.rejim == "BOĞA").mean() - (g5e.rejim == "BOĞA").mean()); row["lt_ort_fark"] = float(G1e["lt"].mean() - g5e["lt"].mean()); row["vd_ort_fark"] = float(G1e.vd.mean() - g5e.vd.mean()); DN.append(row)
    DNd = pd.DataFrame(DN); DNd.to_csv(os.path.join(A.cikti, "K53_DENGE.csv"), index=False)
    Td = pd.DataFrame(T)
    sr = sorted([(k_, (v if np.isfinite(v) else 1.0)) for k_, v in p23.items()], key=lambda x: x[1]); m = len(sr); cum = 0.0
    for r_, (k_, p) in enumerate(sr):
        cum = max(cum, (m - r_) * p); Td.loc[Td.kod == k_, "holm_p_2023_26"] = min(1.0, cum)
    Td["holm_gecer"] = Td.holm_p_2023_26 < 0.05
    # kırılganlık (T1)
    KR = []
    if len(G1) >= 30:
        kat = (G1.y - G1.e_y).groupby(G1.sembol).sum().sort_values(ascending=False); top = set(kat.head(20).index)
        for dn, a, b in V14["donem"]:
            h = cy_v13_fark(G1[~G1.sembol.isin(top) & (G1.tarih >= a) & (G1.tarih <= b)], G2[(G2.tarih >= a) & (G2.tarih <= b)], Kf, rng)
            KR.append({"kirilim": "en_iyi_20_cikarildi", "deger": dn, **{k_: h.get(k_) for k_ in ("n_a", "n_b", "delta", "delta_alt", "delta_ust", "net_fark")}})
    for yl, a, b in V14["yillar"]:
        h = cy_v13_fark(G1[(G1.tarih >= a) & (G1.tarih <= b)], G2[(G2.tarih >= a) & (G2.tarih <= b)], Kf, rng)
        KR.append({"kirilim": "yil", "deger": f"{yl}{' (kısmi)' if yl == 2026 else ''}", **{k_: h.get(k_) for k_ in ("n_a", "n_b", "delta", "delta_alt", "delta_ust", "net_fark")}})
    for ky in ("V_ABD", "K34_yahoo", "K34_tiingo"):
        h = cy_v13_fark(G1[G1.kaynak == ky], G2[G2.kaynak == ky], Kf, rng)
        KR.append({"kirilim": "kaynak", "deger": ky, **{k_: h.get(k_) for k_ in ("n_a", "n_b", "delta", "delta_alt", "delta_ust", "net_fark")}})
    KRd = pd.DataFrame(KR); Td = pd.concat([Td, KRd.assign(kod="KIRILGANLIK-T1", test=KRd.kirilim + " " + KRd.deger.astype(str), donem="hepsi")], ignore_index=True)
    Td.to_csv(os.path.join(A.cikti, "K53_HIPOTEZ_TESTI.csv"), index=False)
    kapanis = not any(k_.startswith("DESTEKLENİYOR") for k_ in (k1, k5, k6))
    karar = ("K53 KAPANDI: T1, T5, T6 hiçbiri desteklenmiyor" if kapanis else ("DESEN ETKİSİ, BİLGİ ETKİSİ DEĞİL (T1 destekleniyor ama T4 < +5); K53 kapandı" if (k1.startswith("DESTEKLENİYOR") and not k4.startswith("DESTEKLENİYOR")) else "KEŞİFSEL DESTEK; bağımsız doğrulama gerekir (İZ denmez)"))
    # EK 4: günlük veri denetimi
    import pickle as _pk
    ham = _pk.load(open(gy, "rb")); ham_n = int(sum(len(u) for u in ham.values() if isinstance(u, pd.DataFrame))); ham_sem = int(sum(1 for u in ham.values() if isinstance(u, pd.DataFrame) and len(u)))
    kn = G.groupby("kurum_n").kurum.nunique(); VD = {"ham_kayit": ham_n, "ham_hisse": ham_sem, "kayit_sonra_kopya_ayiklama": int(len(G)), "yinelenen_atilan": ham_n - int(len(G)),
          "ham_kurum_adi": int(G.kurum.nunique()), "normalize_kurum": int(G.kurum_n.nunique()), "birlesen_ad_sayisi": int((kn > 1).sum()), "en_cok_birlesen": "; ".join(f"{k}: {v}" for k, v in kn.sort_values(ascending=False).head(8).items()),
          "hedef_eksik_pay": float(G.hedef.isna().mean()), "olumlu_pay": float(G.olumlu.mean()), "olumlu_up_pay": float((G.eylem == "up").mean()), "olumlu_raises_pay": float((G.hedef_eylem == "Raises").mean()),
          "olumlu_init_pay": float(((G.eylem == "init") & G.olumlu).mean()), "hafta_sonu_pay": float(G.tarih.dt.dayofweek.ge(5).mean()), "saat_0000_pay": float((G.zaman == G.tarih).mean()),
          "yil_dagilim": {int(k_): int(v) for k_, v in G.tarih.dt.year.value_counts().sort_index().items()}, "spy_bas": str(spy.index.min().date()), "spy_son": str(spy.index.max().date()),
          "sektor_bilinmiyor_hisse_pay": float((pd.Series({s_: sek.get(s_, "bilinmiyor") for s_ in V}) == "bilinmiyor").mean())}
    R = {"X": X, "XX": XX, "GR": GR, "T": Td, "DN": DNd, "VD": VD, "sayac": sayac, "karar": karar, "sure_dk": round((time.time() - t0) / 60, 1), "panel_n": int(len(P)), "hisse": int(P.sembol.nunique()), "kararlar": {"T1": k1, "T4": k4, "T5": k5, "T6": k6}}
    cy_v14_yaz(R, A, K); return R


def cy_v14_yaz(R: Dict[str, Any], A: CYAyar, K: Dict[str, Any]) -> None:
    """K53_RAPOR.md."""
    import subprocess
    TAM = {"n", "n_a", "n_b", "hisse", "hisse_a", "hisse_b", "kgs"}
    def f(x, p=3, tam=False):
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            return ""
        if isinstance(x, (float, np.floating)):
            return str(int(round(x))) if tam else f"{x:+.{p}f}"
        return str(x)
    def tablo(D, kol):
        kol = [c for c in kol if c in D.columns]; L = ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
        for r in D[kol].itertuples(index=False):
            L.append("| " + " | ".join(f(v, tam=(c in TAM)) for c, v in zip(kol, r)) + " |")
        return L
    X, XX, GR, T, V14 = R["X"], R["XX"], R["GR"], R["T"], K["_v14"]; sy = R["sayac"]
    kok = os.path.dirname(os.path.abspath(globals().get("__file__", "COL_YOLU_ABD.py"))) or "."
    try:
        commit = subprocess.run(["git", "-C", kok, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "?"
    L = ["# K53 — BİLGİ DİRENCİ (BDS), ANALİST DAĞINIKLIĞI (ADE), KARAR GECİKMESİ (KGS) (v1.4, ön kayıt 488a407)", "",
         f"**KARAR: {R['karar']}.** K51 kararı (İZ DEĞİL) ve kuralları değişmedi; hiçbir eşik sonuca göre oynatılmadı. T1 {R['kararlar']['T1']}; T4 {R['kararlar']['T4']}; T5 {R['kararlar']['T5']}; T6 {R['kararlar']['T6']}.", "",
         f"- Olay: ilk olumlu analist revizyonu (önceki 20 işlem günü temiz). Sayaç: olumlu kayıt {sy['kayit_olumlu']}, işlem gününe eşlenmeyen tarih {sy['d0_eslesmeyen']}, ilk olay {sy['ilk_olay']}, karar günü panelde likit değil {sy['panel_yok']}, ölçü hesaplanamayan {sy['sekil_yok']}, ölçülen {sy['olcen']}; dönem içi ve etiketli olay {int((XX.grup.isin(['G1', 'G2'])).sum())}.",
         f"- Panel {R['panel_n']} likit hisse-gün, {R['hisse']} hisse; süre {R['sure_dk']} dk; kod {CY_SURUM}, commit {commit}; tohum {V14['tohum']}, bootstrap {V14['boot']}.",
         "- Karar anı d0+4 kapanışı, giriş d0+5 açılışı; KGS testinde karar anı tepki günü (yok kovasında d0+20). Δ = ortalama(y − e_y | A) − ortalama(y − e_y | B); koşullar n ≥ 30, Δ ≥ +5 puan, ay kümeli alt uç > 0, net fark > 0, üç dönem.", ""]
    L += ["## Gruplar", "", "G1 = olay ∧ BDS 3; G2 = olay ∧ BDS < 3; G3 = P1 ∪ ÇEK günü, olumlu revizyon yok; G4 = rastgele likit gün, olumlu yok; G5 = G4 ∧ BDS 3 (aynı şekil, bilgi yok). KGS satırları: olayların kova dağılımı (etiket tepki gününde).", ""]
    L += tablo(GR, ["grup", "donem", "n", "hisse", "isabet", "taban_e_y", "taban_ayarli", "net", "bds_ort", "rel_spy5_ort", "atr_deg_ort", "iyilesme_ort", "P1_pay", "V_ABD_pay"])
    L += ["", "## BDS dağılımı (olaylar)", ""]
    dag = X.bds.value_counts().sort_index(); L += [f"- BDS {int(k)}: {int(v)} olay ({v / len(X):.1%})" for k, v in dag.items()]
    L += [f"- Bileşen payları: fiyat zayıf {X.fiyat_zayif.mean():.1%}, satış azalıyor {X.satis_azaliyor.mean():.1%}, oynaklık düşüyor {X.oyn_dusuyor.mean():.1%}; KGS kova: " + ", ".join(f"{k} {v:.1%}" for k, v in X.kgs_kova.value_counts(normalize=True).items()) + f"; ADE ölçülebilen {X.ade.notna().mean():.1%}.", ""]
    L += ["## Test kararları", "", "| Kod | Test | Karar | Dönem kararları |", "|---|---|---|---|"]
    for r in T[T.donem == "KARAR"].itertuples():
        L.append(f"| {r.kod} | {r.test} | **{r.karar_hucre}** | {getattr(r, 'donem_kararlari', '') if isinstance(getattr(r, 'donem_kararlari', ''), str) else ''} |")
    L += ["", "## Hücreler", ""] + tablo(T[~T.donem.isin(["KARAR"]) & ~T.kod.str.startswith("KIRILGANLIK")], ["kod", "donem", "n_a", "n_b", "isabet_a", "isabet_b", "delta", "delta_alt", "delta_ust", "delta_alt_hisse_ceyrek", "delta_ust_hisse_ceyrek", "net_fark", "p", "holm_p_2023_26", "karar_hucre"])
    L += ["", "T7 satırlarında delta / delta_alt / delta_ust = hızlı / geç / yok kova payları; T6 'hepsi' satırında delta = ADE ölçülebilen olay payı.", "", "## Kırılganlık (T1: G1 − G2)", ""]
    L += tablo(T[T.kod == "KIRILGANLIK-T1"], ["test", "n_a", "n_b", "delta", "delta_alt", "delta_ust", "net_fark"])
    L += ["", "## EK denetim (ön kayıt EK 1-6; karar değişmez)", "", "- Eşleşmiş G1 − G5 (negatif kontrol, nedensel kanıt değil), KGS-sonra (bilgi) ve bileşen testleri yukarıdaki hücre tablosunda ('EK-' kodları). Denge ve örneklem kaybı K53_VERI_DENETIMI.md ve K53_DENGE.csv'de.",
          f"- Bu denetim listesi ilk koşu sonuçları görüldükten sonra geldi; T1 / T5 / T6 kuralı ve karar değişmedi. Ölçülemeyen olay nedenleri: {R['sayac'].get('olculemeyen_neden', {})}.",
          "", "## Sınırlar", "", "- Analist günlüğü yalnız bugün Yahoo'da olan hisselerde var (hayatta kalma); EPS ve gerekçe yok; saat UTC, kayıt tarihi ≤ d0.",
          "- ADE ve KGS tanımları Claude'un sabitlediği tanımlardır (Cemal'in mesajı kesik geldi); sonuca göre değiştirilmedi.",
          "- G5 'aynı şekil, bilgi yok' kontrolü olumlu revizyon dışındaki haberleri (bilanço, içeriden alım) dışlamaz.", "", "## Yeniden üretim", "",
          "- `R = cy_v14_calistir(gunluk_yol='.../yahoo_grades.pkl')`. Çıktılar: K53_OLAYLAR.csv.gz, K53_GRUPLAR.csv, K53_HIPOTEZ_TESTI.csv, bu belge."]
    open(os.path.join(A.cikti, "K53_RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    # K53_VERI_DENETIMI.md (EK 4-5)
    VD = R.get("VD", {}); DN = R.get("DN", pd.DataFrame()); ks = sy.get("kontrol", {})
    M = ["# K53 — VERİ DENETİMİ, ÖRNEKLEM KAYBI VE DENGE (v1.4, ön kayıt EK)", "", "Bu belge karar üretmez; K53 kararı K53_RAPOR.md'dedir ve bu denetimle değişmemiştir.", "",
         "## Analist günlüğü (Yahoo, yfinance upgrades_downgrades)", "",
         f"- Ham kayıt {VD.get('ham_kayit')} ({VD.get('ham_hisse')} hisse); zaman damgası geçersiz ya da aynı kurum aynı tarih kopyası atılan {VD.get('yinelenen_atilan')}; kalan {VD.get('kayit_sonra_kopya_ayiklama')}.",
         f"- Kurum adı normalizasyonu: {VD.get('ham_kurum_adi')} ham ad → {VD.get('normalize_kurum')} normalize ad; birden çok ham adı birleştiren {VD.get('birlesen_ad_sayisi')} normalize ad. En çok birleşenler: {VD.get('en_cok_birlesen')}.",
         f"- Hedef fiyatı eksik kayıt payı {VD.get('hedef_eksik_pay', float('nan')):.3f}; olumlu kayıt payı {VD.get('olumlu_pay', float('nan')):.3f} (up {VD.get('olumlu_up_pay', float('nan')):.3f}, Raises {VD.get('olumlu_raises_pay', float('nan')):.3f}, alım notuyla başlangıç {VD.get('olumlu_init_pay', float('nan')):.3f}). Hedef fiyatı olmayan kurum olumlu / olumsuz görüş sayılmadı; ADE yalnız hedef fiyatı olan kurumlardan (≥ 3) hesaplandı, ortalama ≤ 0 ise ölçülemez.",
         f"- Kayıt tarihi: hafta sonu payı {VD.get('hafta_sonu_pay', float('nan')):.4f}; saat 00:00 payı {VD.get('saat_0000_pay', float('nan')):.4f} (damga UTC kabul). Yıl dağılımı: {VD.get('yil_dagilim')}.",
         "- Geçmiş tarihli verinin sonradan güncellenmiş olma riski: Yahoo günlüğü olay kaydıdır, sürüm bilgisi yoktur; geriye dönük düzeltme doğrulanamaz. Sonuçlar 'sağlayıcı günlüğü doğru' varsayımıyla okunur.",
         f"- SPY serisi {VD.get('spy_bas')} – {VD.get('spy_son')}; sektörü bilinmeyen hisse payı {VD.get('sektor_bilinmiyor_hisse_pay', float('nan')):.3f} (sektör göreli getiri boş kalır; BDS'de kullanılmaz).", "",
         "## Olay seçilimi ve örneklem kaybı", "",
         f"- Olumlu kayıt {sy['kayit_olumlu']} → işlem gününe eşlenmeyen tarih {sy['d0_eslesmeyen']} (seri başından önce / sonundan sonra / 4 günden uzun boşluk) → ilk olay (önceki 20 gün temiz) {sy['ilk_olay']} → seri sonu (d0+4 yok) {sy['seri_sonu']} → d0+4 panel dışı (likit değil ya da etiket yok; delist K51 kuralı) {sy['panel_yok']} → ölçülemeyen {sy['sekil_yok']} {sy.get('olculemeyen_neden', {})} → ölçülen {sy['olcen']}.",
         f"- Kontroller: G3 aday {ks.get('G3_aday')}, G4 aday {ks.get('G4_aday')}; [i-24, i] aralığında olumlu kayıt olduğu için atılan {ks.get('olumlu_var')}; ölçülemeyen {ks.get('olculemeyen')}.", "",
         "## Denge (grup × dönem) ve G1'e göre standartlaştırılmış ortalama farkları (SMD)", ""]
    if len(DN):
        M += tablo(DN[~DN.grup.str.startswith("SMD")], ["grup", "donem", "n", "yil_ort", "en_buyuk_sektor", "en_buyuk_sektor_pay", "sektor_bilinmiyor_pay", "lt_ort", "vd_ort", "dd250_ort", "vol60_ort", "log_dv20_ort", "r60_ort", "kapsama_365_ort", "boga_pay", "V_ABD_pay"])
        M += [""] + tablo(DN[DN.grup.str.startswith("SMD")], ["grup", "n", "dd250_smd", "vol60_smd", "log_dv20_smd", "r60_smd", "kapsama_365_smd", "boga_pay_fark", "lt_ort_fark", "vd_ort_fark"])
    ek = T[T.kod == "EK-G1-G5-eslesik"]
    M += ["", "## G1 − eşleşmiş G5 (negatif kontrol; nedensel kanıt değil)", ""] + tablo(ek, ["donem", "n_a", "isabet_a", "isabet_b", "delta", "delta_alt", "delta_ust", "net_fark", "p", "karar_hucre", "eslesen_pay"])
    M += ["", "Eşleşme: aynı gün ±10 işlem günü, aynı oynaklık ondalığı ve likidite üçte biri, aynı trend işareti, |dd250 farkı| ≤ 0,10, sektör biliniyorsa aynı, en yakın 3 (standartlaştırılmış uzaklık). 'eslesen_pay' = eş bulunan G1 olayı payı.", "",
          "## KGS-önce ve KGS-sonra", "", "- KGS-önce (karar ölçüsü, T5): başlangıç d0−1 kapanışı. KGS-sonra (bilgi, EK 3): başlangıç d0 kapanışı; sonuçlar hücre tablosunda 'EK-KGS-sonra'. Kova ve eşik aynı; karar yalnız KGS-önce ile."]
    open(os.path.join(A.cikti, "K53_VERI_DENETIMI.md"), "w", encoding="utf-8").write("\n".join(M) + "\n")


# ---------------------------------------------------------------- v1.5 K54 TARİHSEL HİSSE EVRENİ SAĞLAMLIK DENETİMİ
# Ön kayıt: arastirma_cikti/col_yolu_abd/K54_onkayit.md (commit d4dcdfb + açıklama). K51 / K52 / K53 kararları değişmez; eski dosyalar
# üzerine yazılmaz. Kaynaklar: Tiingo desteklenen sembol listesi (bitiş tarihi), SEC başvuru geçmişi özeti (8-K maddeleri, formlar, güncel
# semboller), company_tickers.json. Ham SEC verisi repoya girmez.
CY_V15: Dict[str, Any] = {
    "tohum": 515, "boot": 2000, "n_min": 30, "fark_esik": 0.05, "saglam_puan": 0.02, "gecersiz_pay": 0.30, "kes_gun": 120, "alive_sinir": "2026-08-01",
    "b103_gun": 365, "b201_gun": 120, "birlesme_gun": (400, 60), "devam_gun": 180,
    "donem": (("2016-22", "2016-01-01", "2022-12-31"), ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-06-05")),
    "ml_yillar": (2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026), "ml_oz": ("vol60", "log_dv20", "dd250", "r60", "ar20", "imza", "hacim_ok", "trend", "boga"),
    "embargo_gun": 10, "birlesme_form": ("DEFM14A", "SC TO-T", "SC 14D9", "S-4", "425"), "nse": ("25-NSE",), "kayit_dis": ("15-12G", "15-12B", "15-15D"),
    "sinif_ad": {1: "halen işlem gören", 2: "iflas / tasfiye", 3: "birleşme / satın alma", 4: "sembol değiştiren / başka şirkete dönüşen", 5: "veri sağlayıcısında kaybolan, belirsiz", 6: "işlem geçmişi doğrulanamayan"},
}


def _cy_v15_tarihler(sec: Dict[str, Any], kosul) -> np.ndarray:
    """SEC özetinden koşulu sağlayan başvuruların tarihleri (datetime64[D], sıralı)."""
    t = [d for f, d, it in zip(sec["form"], sec["date"], sec.get("items") or [""] * len(sec["form"])) if kosul(str(f), str(it or ""))]
    return np.sort(np.array(t, dtype="datetime64[D]")) if t else np.array([], dtype="datetime64[D]")


def _cy_v15_arada(t: np.ndarray, T: np.datetime64, once: int, sonra: int) -> Optional[np.datetime64]:
    m = t[(t >= T - np.timedelta64(once, "D")) & (t <= T + np.timedelta64(sonra, "D"))]
    return m[0] if len(m) else None


def cy_v15_sinifla(sembol: str, T: Any, cik: Optional[int], sec: Optional[Dict[str, Any]], tiingo: Optional[Dict[str, Any]], bugun_cik: Optional[int],
                   K: Dict[str, Any] = CY_V15) -> Dict[str, Any]:
    """Ön kayıt 2 sıralı kuralları. T = fiyat serisinin son günü. Dönüş: sinif (1-6), kural, kanıt tarihleri, kesim tarihi (4b), ek çıkış işlemi."""
    T = np.datetime64(pd.Timestamp(T).date()); sinir = np.datetime64(K["alive_sinir"]); erken = bool(T < sinir)
    tb = np.datetime64(tiingo["endDate"]) if tiingo and isinstance(tiingo.get("endDate"), str) else None
    sec_sem = [str(x).upper() for x in (sec.get("tickers") or [])] if sec else []
    out = {"sembol": sembol, "cik": cik, "son_islem": str(T), "erken_bitti": erken, "tiingo_bitis": str(tb) if tb is not None else "", "tiingo_borsa": (tiingo or {}).get("exchange", ""),
           "sec_semboller": ";".join(sec_sem), "sec_ad": (sec or {}).get("name", ""), "eski_adlar": ";".join(str(x.get("name")) for x in ((sec or {}).get("formerNames") or [])[:5]),
           "bugun_cik": bugun_cik, "nse25_tarih": "", "son_10k_10q": "", "b103_tarih": "", "b201_tarih": "", "birlesme_belge_tarih": "", "kayit_dis_tarih": "", "kesim_tarihi": "",
           "sinif": 5, "alt": "", "kural": "", "cikis_islemi": "y"}
    if sec:
        kq = _cy_v15_tarihler(sec, lambda f, it: f in ("10-K", "10-Q", "10-K/A", "10-Q/A", "20-F", "40-F")); b103 = _cy_v15_tarihler(sec, lambda f, it: f.startswith("8-K") and "1.03" in it)
        b201 = _cy_v15_tarihler(sec, lambda f, it: f.startswith("8-K") and "2.01" in it); nse = _cy_v15_tarihler(sec, lambda f, it: f in K["nse"])
        bir = _cy_v15_tarihler(sec, lambda f, it: f in K["birlesme_form"]); kd = _cy_v15_tarihler(sec, lambda f, it: f in K["kayit_dis"])
        out["son_10k_10q"] = str(kq[-1]) if len(kq) else ""; out["nse25_tarih"] = str(_cy_v15_arada(nse, T, 400, 400) or ""); out["kayit_dis_tarih"] = str(_cy_v15_arada(kd, T, 400, 400) or "")
    if not erken:
        if (tb is not None and tb >= sinir) or (sembol.upper() in sec_sem):
            out.update({"sinif": 1, "kural": "1: seri sürüyor; Tiingo bitiş >= sınır ya da SEC güncel sembol"}); return out
        out.update({"sinif": 6, "kural": "6: seri sürüyor ama Tiingo listesinde ve SEC güncel sembollerinde yok"}); return out
    if cik is None or not sec:
        out.update({"sinif": 6, "kural": "6: CIK yok ya da SEC başvuru geçmişi yok"}); return out
    a103 = _cy_v15_arada(b103, T, K["b103_gun"], K["b103_gun"])
    if a103 is not None:
        out.update({"sinif": 2, "kural": f"2: 8-K madde 1.03 {a103}", "b103_tarih": str(a103), "cikis_islemi": "y_d100"}); return out
    a201 = _cy_v15_arada(b201, T, K["b201_gun"], K["b201_gun"]); anse = _cy_v15_arada(nse, T, K["b201_gun"], K["b201_gun"]); abir = _cy_v15_arada(bir, T, K["birlesme_gun"][0], K["birlesme_gun"][1])
    out["b201_tarih"] = str(a201 or ""); out["birlesme_belge_tarih"] = str(abir or "")
    if (a201 is not None or anse is not None) and abir is not None:
        out.update({"sinif": 3, "kural": f"3: 8-K 2.01 / 25-NSE {a201 or anse} + birleşme belgesi {abir}", "cikis_islemi": "y_d0"}); return out
    son_kq = kq[-1] if len(kq) else None
    if son_kq is not None and son_kq >= T + np.timedelta64(K["devam_gun"], "D"):
        out.update({"sinif": 4, "alt": "4a sembol değişimi", "kural": f"4a: şirket T'den sonra 10-K / 10-Q veriyor (son {son_kq})", "cikis_islemi": "y_d0"}); return out
    if bugun_cik is not None and cik is not None and int(bugun_cik) != int(cik):
        kes = (son_kq + np.timedelta64(K["kes_gun"], "D")) if son_kq is not None else None
        out.update({"sinif": 4, "alt": "4b kod yeniden kullanımı", "kural": f"4b: bugünkü sembol başka CIK'e ({bugun_cik}) bağlı", "kesim_tarihi": str(kes or ""), "cikis_islemi": "y_kes" if (kes is not None and kes < T) else "y"}); return out
    out.update({"sinif": 5, "kural": "5: erken bitti; 1.03 / 2.01+belge / devam / kod kullanımı yok" + (" (kayıt dışı " + out["kayit_dis_tarih"] + ")" if out["kayit_dis_tarih"] else "")}); return out


def cy_v15_hucre(D: pd.DataFrame, ycol: str, ecol: str, ncol: str, encol: str, K: Dict[str, Any], rng: np.random.Generator) -> Dict[str, Any]:
    """Olay kümesi: n, +%20 / −%10 / zaman aşımı oranı, net, taban-ayarlı isabet (y − e_y) ay kümeli aralık, net fark, karar."""
    D = D[D[ycol].notna() & D[ecol].notna()]
    if not len(D):
        return {"n": 0}
    w = D.agirlik.to_numpy(float) if "agirlik" in D else np.ones(len(D)); X = D.assign(_f=D[ycol] - D[ecol], _fn=D[ncol] - D[encol])
    f, a, b = cy_boot_fark(X, "_f", K["boot"], rng); fn, an, bn = cy_boot_fark(X, "_fn", K["boot"], rng)
    brut = D["brut_k"] if "brut_k" in D else D.brut
    h = {"n": int(len(D)), "hisse": int(D.sembol.nunique()), "ust_oran": float(np.average(D[ycol] == 1, weights=w)), "alt_oran": float(np.average((D[ycol] == 0) & (brut <= -0.10), weights=w)),
         "zaman_asimi_oran": float(np.average((D[ycol] == 0) & (brut > -0.10), weights=w)), "isabet": float(np.average(D[ycol], weights=w)), "taban": float(np.average(D[ecol], weights=w)),
         "net": float(np.average(D[ncol], weights=w)), "fark": f, "fark_alt": a, "fark_ust": b, "net_fark": fn, "net_fark_alt": an, "net_fark_ust": bn}
    h["karar"] = "YETERSİZ ÖRNEKLEM" if h["n"] < K["n_min"] else ("TUTAR" if (f >= K["fark_esik"] and a > 0 and fn > 0) else ("TERS YÖN" if (f <= -K["fark_esik"] and b < 0) else "TUTMAZ"))
    return h


def cy_v15_degerlendir(eski: Dict[str, Any], yeni: Dict[str, Any], gecersiz_pay: float, K: Dict[str, Any]) -> str:
    """Ön kayıt 5: SAĞLAM / ETKİLENMİŞ / GEÇERSİZ (tek hücre)."""
    if gecersiz_pay > K["gecersiz_pay"]:
        return "GEÇERSİZ (belirsiz + doğrulanamayan çıkış payı > %30)"
    if eski.get("n", 0) == 0 or yeni.get("n", 0) == 0:
        return "GEÇERSİZ (hücre boş)"
    fark = abs(yeni["fark"] - eski["fark"]) if np.isfinite(yeni.get("fark", np.nan)) and np.isfinite(eski.get("fark", np.nan)) else np.inf
    ar = [eski.get("fark_alt", np.nan), eski.get("fark_ust", np.nan), yeni.get("fark_alt", np.nan), yeni.get("fark_ust", np.nan)]
    if all(isinstance(x, (int, float, np.floating)) and np.isfinite(x) for x in ar):
        ortusur = not (ar[2] > ar[1] or ar[0] > ar[3]); isaret = (np.sign(ar[0]) == np.sign(ar[2])) and (np.sign(ar[1]) == np.sign(ar[3]))
    else:
        ortusur = True; isaret = True                                        # aralık yoksa (ML satırı) yalnız etki ve karar ölçütü
    return "SAĞLAM" if (fark <= K["saglam_puan"] and eski.get("karar") == yeni.get("karar") and ortusur and isaret) else "ETKİLENMİŞ"


def cy_v15_calistir(A: Optional[CYAyar] = None, K: Dict[str, Any] = CY, k54_yol: Optional[str] = None) -> Dict[str, Any]:
    """K54 sürücü: sınıflandırma -> düzeltilmiş panel -> eski / yeni test hücreleri -> K52 / K53 denetimi -> çıktılar."""
    import json
    A = A or CYAyar(); os.makedirs(A.cikti, exist_ok=True); K = {**K, "_v12": CY_V12, "_v13": CY_V13, "_v15": CY_V15}; V15 = CY_V15; t0 = time.time()
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    rng = np.random.default_rng(V15["tohum"]); k54 = k54_yol or os.path.join(A.veri, "k54")
    cy_veri_hazirla(A); Vs, EV = cy_veri_yukle(A, K); cy_v12_tekil(EV); K["_endeks"] = cy_endeks(A, K); V = Vs["ABD"]; evp = EV[EV.pazar == "ABD"].set_index("sembol")
    # ---------- kaynaklar
    sec = json.load(open(os.path.join(k54, "sec_ozet.json"))); scik = json.load(open(os.path.join(k54, "sembol_cik.json")))
    ct = json.load(open(os.path.join(k54, "company_tickers.json"))); bugun = {str(v["ticker"]).upper(): int(v["cik_str"]) for v in ct.values()}
    tt = pd.read_csv(os.path.join(k54, "supported_tickers.csv")); tt = tt[tt.assetType == "Stock"].copy(); tt["ticker"] = tt.ticker.astype(str).str.upper()
    tt = tt.sort_values("endDate").drop_duplicates("ticker", keep="last").set_index("ticker")
    gy = os.path.join(A.veri, "analist", "yahoo_grades.pkl"); analist_var = set()
    if os.path.exists(gy):
        import pickle
        ham = pickle.load(open(gy, "rb")); analist_var = {s_ for s_, u in ham.items() if isinstance(u, pd.DataFrame) and len(u)}
    # ---------- sınıflandırma
    SD = []
    for s_, d in V.items():
        if s_ not in evp.index:
            continue
        cik = scik.get(s_); sc = sec.get(str(cik)) if cik is not None else None; tr = tt.loc[s_.upper()].to_dict() if s_.upper() in tt.index else None
        r = cy_v15_sinifla(s_, d.index[-1], int(cik) if cik is not None else None, sc, tr, bugun.get(s_.upper()), V15)
        r.update({"kaynak": evp.loc[s_, "kaynak"], "analist_kaydi": bool(s_ in analist_var), "n_gun": int(len(d)), "son_kapanis": float(d.Close.iloc[-1]), "agirlik": float(evp.loc[s_, "agirlik"])}); SD.append(r)
    SD = pd.DataFrame(SD); SD["sinif_ad"] = SD.sinif.map(V15["sinif_ad"]); sinif = SD.set_index("sembol").sinif.to_dict(); islem = SD.set_index("sembol").cikis_islemi.to_dict()
    kes_map = {r.sembol: pd.Timestamp(r.kesim_tarihi) for r in SD.itertuples() if r.cikis_islemi == "y_kes" and r.kesim_tarihi}
    cylog.info("v1.5 sınıflar: %s (%ds)", SD.sinif.value_counts().sort_index().to_dict(), time.time() - t0)
    SD[["sembol", "kaynak", "cik", "sec_ad", "sec_semboller", "eski_adlar", "bugun_cik", "tiingo_borsa", "tiingo_bitis", "son_islem", "n_gun", "analist_kaydi", "agirlik"]].to_csv(os.path.join(A.cikti, "K54_EVREN_ESLESTIRME.csv"), index=False)
    SD[["sembol", "kaynak", "cik", "sinif", "sinif_ad", "alt", "kural", "cikis_islemi", "son_islem", "erken_bitti", "tiingo_bitis", "nse25_tarih", "son_10k_10q", "b103_tarih", "b201_tarih", "birlesme_belge_tarih", "kayit_dis_tarih", "kesim_tarihi", "son_kapanis", "analist_kaydi"]].to_csv(os.path.join(A.cikti, "K54_SIRKET_DURUMU.csv"), index=False)
    # ---------- panel (v1.2 işçisi; 4b kesimi)
    le = cy_likit_esik(V, "ABD", K)
    args = [("ABD", s_, d, evp.loc[s_].to_dict(), le, K, None, kes_map.get(s_)) for s_, d in V.items() if s_ in evp.index]
    import multiprocessing as mp
    with mp.get_context("fork").Pool(max(1, A.is_parcacigi)) as hv:
        son = [x for x in hv.imap_unordered(cy_v12_hisse, args, chunksize=8) if x is not None]
    P = pd.concat([r["panel"].assign(sembol=r["sembol"]) for r in son if len(r["panel"])], ignore_index=True).sort_values(["sembol", "tarih"], kind="stable").reset_index(drop=True)
    P["tarih"] = pd.to_datetime(P.tarih).astype("datetime64[ns]"); P["agirlik"] = P.sembol.map(evp.agirlik).fillna(1.0).astype(np.float32); P["kaynak"] = P.sembol.map(evp.kaynak)
    sek = cy_sektor(A, EV); P["sektor"] = P.sembol.map(sek).fillna("bilinmiyor"); P["sinif"] = P.sembol.map(sinif).fillna(6).astype(int); P["islem"] = P.sembol.map(islem).fillna("y")
    P["imza_h"] = (P.imza - P.hacim_ok).astype(np.int8)
    En = K.get("_endeks", pd.DataFrame())
    if isinstance(En, pd.DataFrame) and "SPY" in En:
        sp = En["SPY"].dropna(); boga = (sp > sp.rolling(200).mean()).reindex(P.tarih.values, method="ffill").to_numpy(); P["rejim"] = np.where(boga, "BOĞA", "AYI")
    else:
        P["rejim"] = "bilinmiyor"
    P["boga"] = (P.rejim == "BOĞA").astype(np.int8)
    Hs = {r["sembol"]: V[r["sembol"]].index.to_numpy().astype("datetime64[ns]") for r in son}
    P["cikis_tarih"] = [Hs[s_][int(c)] if (0 <= int(c) < len(Hs[s_])) else np.datetime64("NaT") for s_, c in zip(P.sembol.to_numpy(), P.cikis.to_numpy())]
    # eski evren: K51 etiketi (y, net), K51 tabanı
    def taban(Q, yc, nc, maske):
        ww = Q.agirlik.where(Q[yc].notna() & maske); grp = [Q.tarih, Q.vd]
        ey = (Q[yc] * ww).groupby(grp).transform("sum") / ww.groupby(grp).transform("sum"); en = (Q[nc] * ww).groupby(grp).transform("sum") / ww.groupby(grp).transform("sum")
        return ey.astype(np.float32), en.astype(np.float32)
    P["vd"] = np.minimum((P.groupby("tarih").vol60.rank(pct=True) * 10).fillna(5).astype(int), 9).astype(np.int8)
    P["lt"] = np.minimum((P.groupby("tarih").log_dv20.rank(pct=True) * 3).fillna(1).astype(int), 2).astype(np.int8)
    P["e_y"], P["e_net"] = taban(P, "y", "net", pd.Series(True, index=P.index))
    # düzeltilmiş evren: sınıfa göre etiket; 6 çıkar; 4b kesim sonrası çıkar
    yk = {"y": ("y", "net"), "y_d100": ("y_d100", "net_d100"), "y_d0": ("y_d0", "net_d0"), "y_kes": ("y_kes", "net_kes")}
    P["y_yeni"] = np.nan; P["net_yeni"] = np.nan
    for isl, (yc, nc) in yk.items():
        m = P.islem == isl; P.loc[m, "y_yeni"] = P.loc[m, yc].to_numpy(); P.loc[m, "net_yeni"] = P.loc[m, nc].to_numpy()
    P["gecerli_yeni"] = (P.sinif != 6) & P.y_yeni.notna() & ((P.islem != "y_kes") | P.kes_gecerli.astype(bool))
    Q = P[P.gecerli_yeni].copy(); Q["vd"] = np.minimum((Q.groupby("tarih").vol60.rank(pct=True) * 10).fillna(5).astype(int), 9).astype(np.int8)
    Q["e_y_yeni"], Q["e_net_yeni"] = taban(Q, "y_yeni", "net_yeni", pd.Series(True, index=Q.index))
    P["e_y_yeni"] = np.nan; P["e_net_yeni"] = np.nan; P.loc[Q.index, "e_y_yeni"] = Q.e_y_yeni; P.loc[Q.index, "e_net_yeni"] = Q.e_net_yeni
    # brut karşılığı (−%10 oranı için) düzeltilmiş: y_yeni == 0 ve seri sonu kaybı; brut sütunu K51 etiketi; düzeltilmişte net_yeni + mal
    P["brut_k"] = P.brut; P["brut_yeni"] = P.net_yeni + P.mal
    cylog.info("v1.5 panel %d satır; düzeltilmiş %d; (%ds)", len(P), int(P.gecerli_yeni.sum()), time.time() - t0)
    # ---------- 1) K51 temel hücreleri + 2) delist duyarlılığı
    KR = []; DL = []
    def cift(ad, kume, maske_e, maske_y, ek=None):
        for dn, a, b in V15["donem"]:
            De = P[maske_e & (P.tarih >= a) & (P.tarih <= b)]; Dy = P[maske_y & P.gecerli_yeni & (P.tarih >= a) & (P.tarih <= b)].assign(brut_k=lambda t: t.brut_yeni)
            he = cy_v15_hucre(De, "y", "e_y", "net", "e_net", V15, rng); hy = cy_v15_hucre(Dy, "y_yeni", "e_y_yeni", "net_yeni", "e_net_yeni", V15, rng)
            cik_ = De[De.sinif.isin([5, 6])]; gp = float(len(cik_) / max(len(De), 1)) if len(De) else 0.0
            # yalnız seri erken biten (çıkış) olaylarının payı değil, tüm olaylar içinde 5 + 6 payı; ayrıca erken bitenler içinde 5 + 6 payı
            erk = De[De.sembol.map(SD.set_index("sembol").erken_bitti)]; gp2 = float(erk.sinif.isin([5, 6]).mean()) if len(erk) else 0.0
            row = {"test": ad, "kume": kume, "donem": dn, **{f"eski_{k_}": v for k_, v in he.items()}, **{f"yeni_{k_}": v for k_, v in hy.items()},
                   "fark_n": hy.get("n", 0) - he.get("n", 0), "fark_fark": (hy.get("fark", np.nan) - he.get("fark", np.nan)), "fark_ust_oran": hy.get("ust_oran", np.nan) - he.get("ust_oran", np.nan),
                   "fark_alt_oran": hy.get("alt_oran", np.nan) - he.get("alt_oran", np.nan), "fark_net": hy.get("net", np.nan) - he.get("net", np.nan),
                   "sinif56_pay_olay": gp, "sinif56_pay_erken_biten_olay": gp2, "degerlendirme": cy_v15_degerlendir(he, hy, gp, V15)}
            if ek:
                row.update(ek)
            KR.append(row)
            if he.get("n", 0) >= 30 and dn != "":
                kat = (De.y - De.e_y).groupby(De.sembol).sum().sort_values(ascending=False); top = set(kat.head(20).index)
                he2 = cy_v15_hucre(De[~De.sembol.isin(top)], "y", "e_y", "net", "e_net", V15, rng); hy2 = cy_v15_hucre(Dy[~Dy.sembol.isin(top)], "y_yeni", "e_y_yeni", "net_yeni", "e_net_yeni", V15, rng)
                KR.append({"test": ad, "kume": kume + " (en iyi 20 çıkarıldı)", "donem": dn, **{f"eski_{k_}": v for k_, v in he2.items()}, **{f"yeni_{k_}": v for k_, v in hy2.items()},
                           "fark_n": hy2.get("n", 0) - he2.get("n", 0), "fark_fark": hy2.get("fark", np.nan) - he2.get("fark", np.nan), "degerlendirme": cy_v15_degerlendir(he2, hy2, gp, V15)})
    for ad, kol in (("K51 P1", "P1"), ("K51 P2", "P2"), ("K51 ES", "ES"), ("K51 HT", "HT"), ("K51 ÇEK", "CEK")):
        cift("1 K51 temel", ad, P[kol].astype(bool), P[kol].astype(bool))
    # delist duyarlılığı: sınıf başına sayılar ve P1 / P2 hücrelerinin −%0 / −%30 / −%100 bandı (yalnız seri erken bitenler değişir)
    for sn_, g in SD.groupby("sinif"):
        DL.append({"kume": "sınıf", "sinif": int(sn_), "sinif_ad": V15["sinif_ad"][int(sn_)], "hisse": int(len(g)), "V_ABD": int((g.kaynak == "V_ABD").sum()), "K34_yahoo": int((g.kaynak == "K34_yahoo").sum()),
                   "K34_tiingo": int((g.kaynak == "K34_tiingo").sum()), "analist_kaydi_pay": float(g.analist_kaydi.mean()), "panel_satir": int((P.sinif == sn_).sum()),
                   "P1_olay": int((P.P1 & (P.sinif == sn_)).sum()), "P2_olay": int((P.P2 & (P.sinif == sn_)).sum()), "son_kapanis_medyan": float(g.son_kapanis.median())})
    for kol in ("P1", "P2"):
        for dn, a, b in V15["donem"]:
            D = P[P[kol].astype(bool) & (P.tarih >= a) & (P.tarih <= b)]
            row = {"kume": f"{kol} bandı", "donem": dn, "n": int(len(D)), "erken_biten_olay": int(D.sembol.map(SD.set_index('sembol').erken_bitti).sum())}
            for sc_, yc in (("d0", "y_d0"), ("d30", "y"), ("d100", "y_d100"), ("yeni", "y_yeni")):
                ww = D.agirlik.to_numpy(float); v = D[yc].to_numpy(float); ok = np.isfinite(v)
                row[f"isabet_{sc_}"] = float(np.average(v[ok], weights=ww[ok])) if ok.any() else np.nan
            row["bant_genislik_puan"] = (row["isabet_d0"] - row["isabet_d100"]) * 100; DL.append(row)
    DLd = pd.DataFrame(DL); DLd.to_csv(os.path.join(A.cikti, "K54_DELIST_DUYARLILIK.csv"), index=False)
    # ---------- 3) H-B / H-C / H-D (v1.2 tanımları; eşleştirme havuzu eski ve düzeltilmiş evren)
    V12 = CY_V12
    def esl(ad, O, havuz, k, gt, es_imza):
        for ev, yc, nc, maske in (("eski", "y", "net", pd.Series(True, index=P.index)), ("yeni", "y_yeni", "net_yeni", P.gecerli_yeni)):
            Oo = O[maske.loc[O.index]].assign(y=lambda t: t[yc], net=lambda t: t[nc]); Hv = havuz[maske.loc[havuz.index]].assign(y=lambda t: t[yc], net=lambda t: t[nc])
            M_ = cy_v12_eslestir(P, Oo, Hv, K, k, gt, rng, es_imza=es_imza); X = pd.concat([Oo, M_], axis=1)
            for dn, a, b in V15["donem"]:
                D = X[(X.tarih >= a) & (X.tarih <= b) & (X.kontrol_n > 0)]
                h = cy_v12_hucre(D, K, rng) if len(D) else {"n": 0}; kr = cy_v12_karar(h, K) if h.get("n", 0) else "YETERSİZ ÖRNEKLEM"
                KR.append({"test": "3 küçük mum / hacim / taban (v1.2 eşleşmiş)", "kume": ad, "donem": dn, "evren": ev, "n": h.get("n", 0), "fark": h.get("fark"), "fark_alt": h.get("fark_alt"), "fark_ust": h.get("fark_ust"),
                           "net_fark": h.get("net_fark"), "karar": kr, "eslesmeyen_pay": float((X.kontrol_n == 0).mean()) if len(X) else np.nan})
    genel = P[~P.cek_ham]; esl("H-B P1 vs ES (küçük mum)", P[P.P1], P[P.ES], V12["k_es"], V12["gun_tol"], False)
    esl("H-C ÇEK + hacim kuruması vs ÇEK hacimsiz", P[P.CEK & (P.hacim_ok == 1)], P[P.CEK & (P.hacim_ok == 0)], V12["k_es"], V12["gun_tol"], True)
    esl("H-D hacimli taban (HT) vs genel", P[P.HT], genel, V12["k"], 0, False)
    KR.append({"test": "3 BB sıkışması / EMA (K48, FON_IZI)", "kume": "K48 / K49 / K50 deneyleri", "donem": "hepsi", "degerlendirme": "GEÇERSİZ (evren yeniden kurulamıyor: yalnız bugün işlem gören V_ABD evreninde koştu; kod K34 evrenini almıyor)"})
    # ---------- 4) sessiz ML (LightGBM meta, P1 olayları, yıl yıl ileri)
    try:
        import lightgbm as lgb
        from sklearn.metrics import roc_auc_score
        for ev, yc, ec, maske in (("eski", "y", "e_y", pd.Series(True, index=P.index)), ("yeni", "y_yeni", "e_y_yeni", P.gecerli_yeni)):
            E = P[P.P1.astype(bool) & maske & P[yc].notna() & P.cikis_tarih.notna()].copy(); oz = list(V15["ml_oz"]); E["meta_p"] = np.nan; sat = []
            for Y in V15["ml_yillar"]:
                sinir = pd.Timestamp(f"{Y}-01-01") - pd.Timedelta(days=V15["embargo_gun"]); tr = E[E.cikis_tarih < sinir]; te = E[E.tarih.dt.year == Y]
                if len(tr) < 100 or tr[yc].nunique() < 2 or len(te) < 30:
                    sat.append({"yil": Y, "egitim_n": len(tr), "test_n": len(te), "auc": np.nan}); continue
                m = lgb.LGBMClassifier(**K["meta"]["lgbm"], random_state=V15["tohum"]); m.fit(tr[oz], tr[yc].astype(int)); pr = m.predict_proba(te[oz])[:, 1]
                E.loc[te.index, "meta_p"] = pr; q = np.quantile(pr, [1 / 3, 2 / 3]); ust = te[pr >= q[1]]; alt = te[pr <= q[0]]
                sat.append({"yil": Y, "egitim_n": len(tr), "test_n": len(te), "auc": float(roc_auc_score(te[yc].astype(int), pr)) if te[yc].nunique() > 1 else np.nan,
                            "ust_ucte_bir_fark": float((ust[yc] - ust[ec]).mean() - (alt[yc] - alt[ec]).mean())})
            S_ = pd.DataFrame(sat); Et = E[E.meta_p.notna()]
            genel_auc = float(roc_auc_score(Et[yc].astype(int), Et.meta_p)) if len(Et) and Et[yc].nunique() > 1 else np.nan
            q = Et.meta_p.quantile([1 / 3, 2 / 3]).to_numpy() if len(Et) else [np.nan, np.nan]
            ust = Et[Et.meta_p >= q[1]]; alt = Et[Et.meta_p <= q[0]]
            hu = cy_v15_hucre(ust, yc, ec, "net" if ev == "eski" else "net_yeni", "e_net" if ev == "eski" else "e_net_yeni", V15, rng)
            ha = cy_v15_hucre(alt, yc, ec, "net" if ev == "eski" else "net_yeni", "e_net" if ev == "eski" else "e_net_yeni", V15, rng)
            KR.append({"test": "4 sessiz ML (LightGBM meta, P1, yıl yıl ileri 2019-26)", "kume": "model üst üçte biri vs alt üçte biri", "donem": "2019-26 test yılları", "evren": ev, "n": int(len(Et)),
                       "auc": genel_auc, "fark": (hu.get("fark", np.nan) - ha.get("fark", np.nan)), "ust_fark": hu.get("fark"), "ust_fark_alt": hu.get("fark_alt"), "ust_fark_ust": hu.get("fark_ust"),
                       "alt_fark": ha.get("fark"), "yillik_auc": "; ".join(f"{int(r.yil)}: {r.auc:.3f}" for r in S_.itertuples() if np.isfinite(r.auc)),
                       "karar": "TUTAR" if (hu.get("n", 0) >= 30 and (hu.get("fark", 0) - ha.get("fark", 0)) >= V15["fark_esik"] and hu.get("fark_alt", 0) > 0) else "TUTMAZ"})
    except Exception as ex:
        KR.append({"test": "4 sessiz ML", "kume": "hata", "donem": "", "degerlendirme": f"koşulamadı: {ex}"})
    # ---------- 5) K52 / K53 kayıtlı olay dosyalarıyla düzeltilmiş etiket
    sinir = {}
    bas = 0; sem_arr = P.sembol.to_numpy(); Pi = P.i.to_numpy()
    for k_ in range(1, len(P) + 1):
        if k_ == len(P) or sem_arr[k_] != sem_arr[bas]:
            sinir[sem_arr[bas]] = (bas, k_); bas = k_
    def satir(s_, i):
        if s_ not in sinir:
            return -1
        a, b = sinir[s_]; j = a + int(np.searchsorted(Pi[a:b], i)); return j if (j < b and Pi[j] == i) else -1
    def yeni_etiket(X, icol="i"):
        js = np.array([satir(s_, int(i)) for s_, i in zip(X.sembol.to_numpy(), X[icol].to_numpy())])
        ok = js >= 0; out = X.copy(); out["_j"] = js; jj = np.where(ok, js, 0)
        def al(col, bos):
            v = P[col].to_numpy()[jj].copy(); v = np.where(ok, v, bos); return v
        out["y_yeni"] = al("y_yeni", np.nan).astype(float); out["net_yeni"] = al("net_yeni", np.nan).astype(float); out["e_y_yeni"] = al("e_y_yeni", np.nan).astype(float)
        out["e_net_yeni"] = al("e_net_yeni", np.nan).astype(float); out["gecerli_yeni"] = al("gecerli_yeni", False).astype(bool); out["sinif"] = al("sinif", 0).astype(int)
        out.loc[~ok, "sinif"] = 6                                              # panelde bulunamayan olay: doğrulanamayan sayılır
        return out
    Kf = {"boot": V15["boot"], "n_min": V15["n_min"], "fark_esik": V15["fark_esik"]}
    def cift_fark(ad, kume, Aold, Bold):
        An = yeni_etiket(Aold); Bn = yeni_etiket(Bold)
        An = An[An.gecerli_yeni].assign(y=lambda t: t.y_yeni, net=lambda t: t.net_yeni, e_y=lambda t: t.e_y_yeni, e_net=lambda t: t.e_net_yeni)
        Bn = Bn[Bn.gecerli_yeni].assign(y=lambda t: t.y_yeni, net=lambda t: t.net_yeni, e_y=lambda t: t.e_y_yeni, e_net=lambda t: t.e_net_yeni)
        for dn, a, b in V15["donem"]:
            he = cy_v13_fark(Aold[(Aold.tarih >= a) & (Aold.tarih <= b)], Bold[(Bold.tarih >= a) & (Bold.tarih <= b)], Kf, rng); hy = cy_v13_fark(An[(An.tarih >= a) & (An.tarih <= b)], Bn[(Bn.tarih >= a) & (Bn.tarih <= b)], Kf, rng)
            ke = cy_v13_karar(he, Kf) if "delta" in he else "YETERSİZ ÖRNEKLEM"; ky = cy_v13_karar(hy, Kf) if "delta" in hy else "YETERSİZ ÖRNEKLEM"
            e_ = {"n": he.get("n_a", 0), "fark": he.get("delta", np.nan), "fark_alt": he.get("delta_alt", np.nan), "fark_ust": he.get("delta_ust", np.nan), "karar": ke}
            y_ = {"n": hy.get("n_a", 0), "fark": hy.get("delta", np.nan), "fark_alt": hy.get("delta_alt", np.nan), "fark_ust": hy.get("delta_ust", np.nan), "karar": ky}
            Ad = Aold[(Aold.tarih >= a) & (Aold.tarih <= b)]; gp = float(yeni_etiket(Ad).sinif.isin([5, 6]).mean()) if len(Ad) else 0.0
            KR.append({"test": ad, "kume": kume, "donem": dn, "eski_n": e_["n"], "eski_n_b": he.get("n_b", 0), "eski_fark": e_["fark"], "eski_fark_alt": e_["fark_alt"], "eski_fark_ust": e_["fark_ust"], "eski_net_fark": he.get("net_fark"), "eski_karar": ke,
                       "yeni_n": y_["n"], "yeni_n_b": hy.get("n_b", 0), "yeni_fark": y_["fark"], "yeni_fark_alt": y_["fark_alt"], "yeni_fark_ust": y_["fark_ust"], "yeni_net_fark": hy.get("net_fark"), "yeni_karar": ky,
                       "fark_fark": y_["fark"] - e_["fark"] if np.isfinite(y_["fark"]) and np.isfinite(e_["fark"]) else np.nan, "sinif56_pay_olay": gp, "degerlendirme": cy_v15_degerlendir(e_, y_, gp, V15)})
    kap = {}
    f52 = os.path.join(A.cikti, "K51_ANALIST_REVIZYONLARI.csv.gz")
    if os.path.exists(f52):
        R52 = pd.read_csv(f52); R52["tarih"] = pd.to_datetime(R52.tarih)
        for iz in ("P1", "P2"):
            Xi = R52[R52.iz == iz]; cift_fark("5 K52 H0 (G1 − G2a)", f"K52 {iz}", Xi[Xi.grup == "G1"], Xi[Xi.grup == "G2a"])
        k52 = yeni_etiket(R52); kap["K52 olaylarında sınıf dağılımı"] = k52.sinif.value_counts(dropna=False).to_dict()
        kap["K52 olaylarında analist kaydı olan pay (sınıf 2-6 içinde)"] = float(k52[k52.sinif.isin([2, 3, 4, 5, 6])].kayit_var.mean()) if "kayit_var" in k52 and k52.sinif.isin([2, 3, 4, 5, 6]).any() else np.nan
    f53 = os.path.join(A.cikti, "K53_OLAYLAR.csv.gz")
    if os.path.exists(f53):
        R53 = pd.read_csv(f53); R53["tarih"] = pd.to_datetime(R53.tarih)
        cift_fark("5 K53 T1 (BDS 3 − BDS < 3)", "K53 T1", R53[R53.grup == "G1"], R53[R53.grup == "G2"])
        XK = R53[R53.y_kgs.notna()].copy(); XK["i_kgs"] = (XK.i - 4 + np.minimum(XK.kgs, 20)).astype(int); XK["tarih"] = pd.to_datetime(XK.kgs_tarih)
        XKo = XK.assign(y=XK.y_kgs, net=XK.net_kgs, e_y=XK.e_y_kgs, e_net=XK.e_net_kgs, i=XK.i_kgs)
        cift_fark("5 K53 T5 (KGS geç − hızlı)", "K53 T5", XKo[XKo.kgs_kova == "geç"], XKo[XKo.kgs_kova == "hızlı"])
        XA = R53[R53.ade.notna()]
        if len(XA) >= 90:
            q = XA.ade.quantile([1 / 3, 2 / 3]).to_numpy(); cift_fark("5 K53 T6 (ADE üst − alt üçte bir)", "K53 T6", XA[XA.ade > q[1]], XA[XA.ade <= q[0]])
        k53 = yeni_etiket(R53); kap["K53 olaylarında sınıf dağılımı"] = k53.sinif.value_counts(dropna=False).to_dict()
    # analist kapsaması sınıf başına
    for sn_, g in SD.groupby("sinif"):
        kap[f"sınıf {sn_} ({V15['sinif_ad'][int(sn_)]}) analist kaydı olan pay"] = float(g.analist_kaydi.mean())
    # 3 ve 4 numaralı testlerde eski / yeni satır çiftlerinden değerlendirme
    KRd = pd.DataFrame(KR)
    for t_, anahtar in (("3 ", ["kume", "donem"]), ("4 ", ["kume", "donem"])):
        m = KRd.test.str.startswith(t_) & KRd.evren.notna() if "evren" in KRd else pd.Series(False, index=KRd.index)
        for key, g in KRd[m].groupby(anahtar):
            e_ = g[g.evren == "eski"]; y_ = g[g.evren == "yeni"]
            if len(e_) and len(y_):
                e1 = e_.iloc[0].to_dict(); y1 = y_.iloc[0].to_dict(); dg = cy_v15_degerlendir(e1, y1, 0.0, V15)
                KRd.loc[y_.index, "degerlendirme"] = dg; KRd.loc[y_.index, "fark_fark"] = (y1.get("fark", np.nan) - e1.get("fark", np.nan))
    KRd.to_csv(os.path.join(A.cikti, "K54_ESKI_YENI_TEST_KARSILASTIRMA.csv"), index=False)
    R = {"SD": SD, "KR": KRd, "DL": DLd, "kap": kap, "sure_dk": round((time.time() - t0) / 60, 1), "panel_n": int(len(P)), "gecerli_n": int(P.gecerli_yeni.sum()), "hisse": int(P.sembol.nunique())}
    cy_v15_yaz(R, A, K); return R


def cy_v15_yaz(R: Dict[str, Any], A: CYAyar, K: Dict[str, Any]) -> None:
    """K54_RAPOR.md."""
    import subprocess
    V15 = K["_v15"]; SD, KR, DL, kap = R["SD"], R["KR"], R["DL"], R["kap"]
    TAM = {"n", "eski_n", "yeni_n", "eski_n_b", "yeni_n_b", "fark_n", "hisse", "eski_hisse", "yeni_hisse", "V_ABD", "K34_yahoo", "K34_tiingo", "panel_satir", "P1_olay", "P2_olay", "erken_biten_olay", "sinif"}
    def f(x, p=3, tam=False):
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            return ""
        if isinstance(x, (float, np.floating)):
            return str(int(round(x))) if tam else f"{x:+.{p}f}"
        return str(x)
    def tablo(D, kol):
        kol = [c for c in kol if c in D.columns]; L = ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
        for r in D[kol].itertuples(index=False):
            L.append("| " + " | ".join(f(v, tam=(c in TAM)) for c, v in zip(kol, r)) + " |")
        return L
    kok = os.path.dirname(os.path.abspath(globals().get("__file__", "COL_YOLU_ABD.py"))) or "."
    try:
        commit = subprocess.run(["git", "-C", kok, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "?"
    sd = SD.sinif.value_counts().sort_index(); erken = SD[SD.erken_bitti]
    L = ["# K54 — TARİHSEL HİSSE EVRENİ SAĞLAMLIK DENETİMİ (v1.5, ön kayıt d4dcdfb)", "",
         "K54 yeni iz araştırması değildir. K51 / K52 / K53 ön kayıtları ve kararları değişmedi (K51 İZ DEĞİL). Eski dosyalar üzerine yazılmadı; eski ve düzeltilmiş evren değerleri yan yana.", "",
         f"- Evren {len(SD)} sembol; panel {R['panel_n']} likit hisse-gün, düzeltilmiş evren {R['gecerli_n']} satır ({R['hisse']} hisse); süre {R['sure_dk']} dk; kod {CY_SURUM}, commit {commit}.",
         "- Kaynaklar: Tiingo desteklenen sembol listesi (bitiş tarihi, fiyat değil), SEC başvuru geçmişi (8-K madde 1.03 / 2.01, 25-NSE, 15-12G, birleşme belgeleri, 10-K / 10-Q devamı, güncel semboller, eski adlar), company_tickers.json. Tiingo fiyatı analist kaydının yerine kullanılmadı.", "",
         "## 1. Şirket durumu sınıfları", "", "| sınıf | ad | hisse | V_ABD | K34 Yahoo | K34 Tiingo | erken biten | analist kaydı payı |", "|---|---|---|---|---|---|---|---|"]
    for sn_, g in SD.groupby("sinif"):
        L.append(f"| {int(sn_)} | {V15['sinif_ad'][int(sn_)]} | {len(g)} | {(g.kaynak == 'V_ABD').sum()} | {(g.kaynak == 'K34_yahoo').sum()} | {(g.kaynak == 'K34_tiingo').sum()} | {g.erken_bitti.sum()} | {g.analist_kaydi.mean():+.3f} |")
    L += ["", f"- Seri erken biten (T < {V15['alive_sinir']}) {len(erken)} sembol: " + ", ".join(f"sınıf {int(k_)}: {int(v)}" for k_, v in erken.sinif.value_counts().sort_index().items()) + ".",
          "- K51'in eski tahmini (K51_EVREN_PIT 'cikis_turu_tahmin') ile karşılaştırma K54_SIRKET_DURUMU.csv'de (sembol başına kural ve kanıt tarihleri).", "",
          "## 2. Delist duyarlılığı (sınıf başına sayılar; P1 / P2 hücrelerinin −%0 / −%30 / −%100 bandı ve düzeltilmiş etiket)", ""]
    L += tablo(DL[DL.kume == "sınıf"], ["sinif", "sinif_ad", "hisse", "V_ABD", "K34_yahoo", "K34_tiingo", "analist_kaydi_pay", "panel_satir", "P1_olay", "P2_olay", "son_kapanis_medyan"])
    L += [""] + tablo(DL[DL.kume != "sınıf"], ["kume", "donem", "n", "erken_biten_olay", "isabet_d0", "isabet_d30", "isabet_d100", "isabet_yeni", "bant_genislik_puan"])
    L += ["", "## 3. Eski evren / düzeltilmiş evren / fark (aynı tanım ve eşikler)", "", "Taban-ayarlı isabet = y − e_y (K51 tabanı aynı gün aynı oynaklık ondalığı); 'fark_fark' = düzeltilmiş − eski (puan, ×100 değil). Değerlendirme: SAĞLAM (≤ 2 puan, karar ve aralık aynı), ETKİLENMİŞ, GEÇERSİZ (sınıf 5 + 6 payı > %30 ya da evren kurulamıyor).", ""]
    t1 = KR[KR.test.str.startswith("1 ")]
    L += ["### 3.1 K51 temel hücreleri", ""] + tablo(t1, ["kume", "donem", "eski_n", "yeni_n", "eski_ust_oran", "yeni_ust_oran", "eski_alt_oran", "yeni_alt_oran", "eski_net", "yeni_net", "eski_fark", "eski_fark_alt", "eski_fark_ust", "yeni_fark", "yeni_fark_alt", "yeni_fark_ust", "fark_fark", "eski_karar", "yeni_karar", "sinif56_pay_olay", "degerlendirme"])
    t3 = KR[KR.test.str.startswith("3 ")]
    L += ["", "### 3.2 Küçük mum / hacim kuruması / hacimli taban (v1.2 eşleşmiş kontrol; eşleştirme havuzu her evrende ayrı)", ""] + tablo(t3, ["kume", "donem", "evren", "n", "fark", "fark_alt", "fark_ust", "net_fark", "karar", "eslesmeyen_pay", "degerlendirme"])
    t4 = KR[KR.test.str.startswith("4 ")]
    L += ["", "### 3.3 Sessiz ML (LightGBM meta-etiketleme, P1, yıl yıl ileri)", ""] + tablo(t4, ["kume", "donem", "evren", "n", "auc", "fark", "ust_fark", "ust_fark_alt", "ust_fark_ust", "alt_fark", "karar", "yillik_auc", "degerlendirme"])
    t5 = KR[KR.test.str.startswith("5 ")]
    L += ["", "### 3.4 K52 / K53 (kayıtlı olay dosyaları, düzeltilmiş etiket; sınıf 6 çıkarıldı)", ""] + tablo(t5, ["test", "kume", "donem", "eski_n", "eski_n_b", "yeni_n", "yeni_n_b", "eski_fark", "eski_fark_alt", "eski_fark_ust", "yeni_fark", "yeni_fark_alt", "yeni_fark_ust", "fark_fark", "eski_karar", "yeni_karar", "sinif56_pay_olay", "degerlendirme"])
    L += ["", "## 4. K52 / K53 özel denetimi", ""] + [f"- {k_}: {v}" for k_, v in kap.items()]
    L += ["- Analist geçmişi olmayan şirketlere sıfır revizyon atanmadı; K52 / K53'te bunlar 'veri yok' (G2b / G4b) alt grubundaydı. Yahoo günlüğü yalnız bugün Yahoo'da bulunan sembolleri kapsadığından K52 / K53 sonuçları **yalnız Yahoo kapsamındaki (çoğu halen işlem gören) şirketler için geçerlidir**; batan / birleşen şirketlerin analist geçmişi yoktur ve Tiingo fiyatı bunun yerine kullanılmamıştır.", "",
          "## 5. Değerlendirme özeti", ""]
    oz = KR[KR.degerlendirme.notna()].groupby("test").degerlendirme.apply(lambda v: ", ".join(f"{k_}: {n}" for k_, n in v.value_counts().items()))
    L += [f"- {t}: {v}" for t, v in oz.items()]
    L += ["", "Sınıf 6 (doğrulanamayan) ve sınıf 5 (belirsiz) hiçbir hücrede iflas ya da aktif sayılmadı; 6 düzeltilmiş evrenden çıktı, 5 K51 kuralıyla kaldı ve bandı yazıldı.", "",
          "## Yeniden üretim", "", "- `R = cy_v15_calistir(k54_yol='.../k54')` (k54: sec_ozet.json, sembol_cik.json, company_tickers.json, supported_tickers.csv; SEC indirmesi e-posta User-Agent ile, kodda yok). Çıktılar: K54_EVREN_ESLESTIRME.csv, K54_SIRKET_DURUMU.csv, K54_ESKI_YENI_TEST_KARSILASTIRMA.csv, K54_DELIST_DUYARLILIK.csv, bu belge."]
    open(os.path.join(A.cikti, "K54_RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


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
