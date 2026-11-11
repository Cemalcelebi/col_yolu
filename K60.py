"""K60 — SİNYAL KÜTÜPHANESİ x İKİ CETVEL (portföy cetveli v2 + OLASILIK TABLOSU), üç dönem, çoklu deneme muhasebesi; tek dosya
(11 Kasım 2026; ana oturum iş tanımı, yol haritası bölüm 5, CLAUDE.md 'Sonuç dili').

Soru: ölçülebilir hangi özellik (a) bir hissenin 12 ayda +%100 / +%50 yapma ve -%50 düşme OLASILIĞINI taban orana göre kaç kat değiştiriyor,
(b) aylık üst %10 portföyünde maliyetten sonra evrene göre fazla getiri bırakıyor? Veri: Yahoo günlük fiyat 2010 - Ağu 2026 (K60_veri
önbelleği), SEC XBRL frames 2009Q1 - 2026Q2 + EDGAR başvuru dizini (gerçek başvuru günleri). Evren: bugün yaşayan geniş ABD evreni.
  Kütüphane  SINYAL_ENVANTERI'nin eldeki veriyle hesaplanabilen bütün satırları (K60_ESIK['kutuphane']); başka indirme isteyenler DALGA 2 (K61).
  Dönemler   KEŞİF 2012-01..2021-12 (seçim burada), DOĞRULAMA 2022-01..2023-12 (yalnız keşifte seçilenler + aile bileşikleri),
             KASA 2024-01.. (tek açılış, yalnız doğrulamadan geçenler). Dönem = OLUŞUM ayı.
  Cetveller  R1 = K59 portföy cetveli v2 (K59 / K58 fonksiyonları MODÜL olarak çağrılır; kopya yok). R2 = olasılık tablosu (üst ve alt uç;
             12 ay ileri getiri; lift = P(uç) / P(evren); ay kümeli blok bootstrap).
  Çoklu deneme  Benjamini-Hochberg %10 (R1, R2 '+%100', R2 '-%50' ayrı aileler) + 200 rastgele sinyal plasebosu + |t| > 3.
SEC'e ya da başka bir yere İSTEK ATILMAZ (yalnız önbellek okunur; önbellek eksikse koşu durur).

Komut:  python -I K60.py kapsam                  yalnız SAYIM (hisse / ay / sinyal başına kaç hisse); getiri ve olasılık HESAPLANMAZ
        python K60.py onkayit                    ön kaydı yazar (ölçümden ÖNCE; mühür + veri sha256 + kapsam; varsa üzerine yazmaz)
        python -I K60.py kos --donem kesif       mühür + veri sha256 + ön kayıt git'e işlenmiş ve değişmemiş -> KEŞİF ölçümü + secili.json
        python -I K60.py kos --donem dogrulama   yalnız kesif çıktıları varsa ve secili.json git'e işlenmişse
        python -I K60.py kos --donem kasa        yalnız dogrulama çıktıları varsa, dogrulama_gecen.json git'e işlenmişse ve YALNIZ BİR KEZ
        python K60.py rapor                      K60_RAPOR.md ve olasilik_tablosu.md'yi çıktılardan yeniden yazar
Colab:  exec(open('K60.py').read()); k60_kos('kesif')
Veri:   /tmp/k60_fiyat, /tmp/k60_secframes (K60_veri), /tmp/secframes (K59 girdisi; yalnız okunur), /tmp/secfs/company_tickers.json,
        /tmp/k60_french (French günlük 3 faktör), /tmp/k58_french (aylık 5 faktör + momentum), islenmis-veri dalı k35/k35_sic.csv.
        Kişisel e-posta / anahtar yok. Çıktılar arastirma_cikti/k60_kutuphane/. Ara önbellek /tmp/k60_panel (K60_PANEL ile değişir).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K60 = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import zipfile  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K60 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K60 not in sys.path:
    sys.path.insert(0, KOK_K60)

import K59  # noqa: E402
import K60_veri as KV  # noqa: E402

K57, K58 = K59.K57, K59.K58

k60log = logging.getLogger("col.k60")
if not k60log.handlers:
    _k60_h = logging.StreamHandler(sys.stderr)
    _k60_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k60: %(message)s", "%H:%M:%S"))
    k60log.addHandler(_k60_h)
    k60log.setLevel(logging.INFO)
    k60log.propagate = False

K60_SURUM = ("K60 v1.0 (2026-11-11): sinyal kütüphanesi x iki cetvel (R1 portföy cetveli v2, R2 olasılık tablosu), KEŞİF / DOĞRULAMA / KASA, "
             "Benjamini-Hochberg + plasebo; geniş ABD evreni (yalnız yaşayanlar)")
K60_YOL = {"cikti": os.path.join(KOK_K60, "arastirma_cikti", "k60_kutuphane"),
           "panel": os.environ.get("K60_PANEL", "/tmp/k60_panel"),
           "french_gunluk": os.environ.get("K60_FRENCH", "/tmp/k60_french"),
           "tickers": os.path.join(K57.K57_YOL["secfs"], "company_tickers.json")}
K60_DOSYA = {"onkayit": "K60_ON_KAYIT.md", "kapsam": "kapsam.csv", "kapsam_ozet": "kapsam_ozet.json", "secili": "secili.json",
             "gecen": "dogrulama_gecen.json", "kasa_isaret": "kasa_acildi.json", "plasebo": "placebo.csv", "model": "model_kalibrasyon.csv",
             "tablo": "olasilik_tablosu.md", "rapor": "K60_RAPOR.md"}
K60_DONEM = ("kesif", "dogrulama", "kasa")
K60_DONEM_AD = {"kesif": "KEŞİF", "dogrulama": "DOĞRULAMA", "kasa": "KASA"}
_K60_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")

# ---------------------------------------------------------------- KÜTÜPHANE (ön kayıtlı; mühre girer)
# (kod, aile, yön, tür, tanım, kaynak). yön: '+' ölçü yüksekse beklenen getiri yüksek, '-' düşük, '?' iki yönlü. tür: 'surekli' (onluk)
# ya da 'bayrak' (0 / 1; onluk yerine bayraklı grup). t = oluşum ayının son işlem günü; m = o ayın sırası; A = temettü + bölünme düzeltmeli
# kapanış, C = bölünme düzeltmeli kapanış; ç0 = bilgi tarihi < t olan en son çeyrek; y0 = bilgi tarihi < t olan en son mali yıl; PD = piyasa değeri.
_K60_KUTUPHANE: List[Tuple[str, str, str, str, str, str]] = [
    ("MOM_12_1", "MOM", "+", "surekli", "A(m-1) / A(m-12) - 1", "Jegadeesh-Titman 1993"),
    ("MOM_6_1", "MOM", "+", "surekli", "A(m-1) / A(m-6) - 1", "Jegadeesh-Titman 1993"),
    ("MOM_INT_12_7", "MOM", "+", "surekli", "A(m-6) / A(m-12) - 1 (t-12 .. t-7 ayları)", "Novy-Marx 2012"),
    ("MOM_RES_12_1", "MOM", "+", "surekli", "36 aylık (m-35 .. m, hepsi dolu) aylık fazla getirinin French MKT-RF, SMB, HML üzerine sabitli EKK artıkları; "
     "m-11 .. m-1 artıklarının toplamı / aynı 11 artığın std'si (ddof 1)", "Blitz-Huij-Martens 2011"),
    ("HIGH52", "MOM", "+", "surekli", "C(t) / son 252 işlem gününün en yüksek gün içi fiyatı (en az 200 gözlem)", "George-Hwang 2004"),
    ("STREV_1M", "MOM", "-", "surekli", "A(m) / A(m-1) - 1 (geçen ayın getirisi)", "Jegadeesh 1990"),
    ("LTREV_60_13", "MOM", "-", "surekli", "A(m-12) / A(m-60) - 1", "De Bondt-Thaler 1985"),
    ("MOM_FIP", "MOM", "+", "surekli", "ay içi yüzdelik sıra ortalaması: MOM_12_1 ve süreklilik = işaret(MOM_12_1) x (artı gün payı - eksi gün payı), "
     "günler (m-12 ay sonu, m-1 ay sonu], en az 200 gün; ikisi de olmalı", "Da-Gurun-Warachka 2014"),
    ("TREND_MA", "MOM", "+", "surekli", "x_L = L günlük ortalama C / C(t), L = 3, 5, 10, 20, 50, 100, 200; her ay k: getiri(k) ~ x_L(k-1) kesit EKK'si "
     "(k-1'de uygun hisseler); sinyal(m) = Σ_L [son 12 ayın (m-11 .. m) katsayı ortalaması] x x_L(m)", "Han-Zhou-Zhu 2016"),
    ("BM", "VAL", "+", "surekli", "StockholdersEquity(ç0) / PD; özkaynak > 0", "Fama-French 1992"),
    ("EP", "VAL", "+", "surekli", "NetIncomeLoss son 4 çeyrek toplamı / PD", "Basu 1977"),
    ("SP", "VAL", "+", "surekli", "gelir son 4 çeyrek toplamı / PD", "Barbee-Mukherji-Raines 1996"),
    ("AM", "VAL", "+", "surekli", "toplam varlık(ç0) / PD", "Fama-French 1992"),
    ("LEV_MKT", "VAL", "+", "surekli", "toplam yükümlülük(ç0) / PD", "Bhandari 1988"),
    ("CFP", "VAL", "+", "surekli", "faaliyet nakit akışı (y0, yıllık) / PD", "Desai-Rajgopal-Venkatachalam 2004"),
    ("EV_EBITDA", "VAL", "-", "surekli", "(PD + uzun vadeli borç(ç0; yoksa 0) - nakit(ç0; yoksa 0)) / (OperatingIncomeLoss son 4 çeyrek + "
     "amortisman (y0, yıllık)); payda > 0 şart", "Loughran-Wellman 2011"),
    ("NET_PAYOUT_YLD", "VAL", "+", "surekli", "(temettü + geri alım - hisse ihracı geliri) (y0, yıllık; olmayan kalem 0; y0'da faaliyet nakit akışı olmalı) / PD",
     "Boudoukh et al. 2007"),
    ("ROE_TTM", "PRF", "+", "surekli", "NetIncomeLoss son 4 çeyrek / StockholdersEquity(ç0); özkaynak > 0", "Haugen-Baker 1996"),
    ("ROA_Q", "PRF", "+", "surekli", "NetIncomeLoss(ç0) / toplam varlık(ç0-1)", "Balakrishnan-Bartov-Faurel 2010"),
    ("D_ASSET_TURN", "PRF", "+", "surekli", "gelir 4ç(ç0) / varlık(ç0) - gelir 4ç(ç0-4) / varlık(ç0-4)", "Soliman 2008"),
    ("SALES_ACCEL", "PRF", "+", "surekli", "gelir(ç0) / [gelir(ç0-1) + gelir(ç0-2)] / 2; payda > 0 (K59 S7)", "proje ölçüsü (şüpheli: yayımlanmış kanıt yok)"),
    ("ACCRUALS", "PRF", "-", "surekli", "(net kâr(y0) - faaliyet nakit akışı(y0)) / [varlık(y0 sonu) + varlık(y0-1 sonu)] / 2", "Sloan 1996"),
    ("GP_A", "PRF", "+", "surekli", "brüt kâr son 4 çeyrek / varlık(ç0); brüt kâr = GrossProfit, yoksa gelir - satışların maliyeti", "Novy-Marx 2013"),
    ("OP_BE", "PRF", "+", "surekli", "OperatingIncomeLoss son 4 çeyrek / StockholdersEquity(ç0); özkaynak > 0", "Fama-French 2006"),
    ("CBOP_A", "PRF", "+", "surekli", "faaliyet nakit akışı(y0) / varlık(y0 sonu) (yaklaşık sürüm)", "Ball et al. 2016"),
    ("F_SCORE", "PRF", "+", "surekli", "Piotroski 9 ikili ölçü, yıllık (y0, y0-1): ROA > 0; OCF > 0; ΔROA > 0; OCF > net kâr; Δ(uzun vadeli borç / varlık) < 0; "
     "Δ(dönen varlık / kısa vadeli yükümlülük) > 0; hisse ihracı geliri <= 0 ya da yok; Δ brüt marj > 0; Δ(gelir / varlık) > 0. "
     "En az 7 ölçü hesaplanabilmeli; puan = toplam x 9 / hesaplanan sayı; eşitlik ROA ile bozulur (+0,001 x kırpılmış ROA)", "Piotroski 2000"),
    ("NOA", "PRF", "-", "surekli", "(uzun vadeli borç(ç0; yoksa 0) + özkaynak(ç0) - nakit(ç0)) / varlık(ç0-4) (yaklaşık)", "Hirshleifer et al. 2004"),
    ("OPLEV", "PRF", "+", "surekli", "(gelir 4ç - OperatingIncomeLoss 4ç) / varlık(ç0) (toplam faaliyet gideri / varlık)", "Novy-Marx 2011"),
    ("RD_ME", "PRF", "+", "surekli", "ResearchAndDevelopmentExpense son 4 çeyrek / PD; yalnız Ar-Ge bildirenler", "Chan-Lakonishok-Sougiannis 2001"),
    ("TAX_CHG", "PRF", "+", "surekli", "(IncomeTaxExpenseBenefit(ç0) - (ç0-4)) / varlık(ç0-4)", "Thomas-Zhang 2011"),
    ("ASSET_G", "INV", "-", "surekli", "varlık(ç0) / varlık(ç0-4) - 1", "Cooper-Gulen-Schill 2008"),
    ("NSI_1Y", "INV", "-", "surekli", "ln(pay(t) / pay(t - 12 ay)); pay bölünme düzeltmeli, iki uç aynı kaynaktan; oran > 5 ya da < 1/5 ise veri yok", "Pontiff-Woodgate 2008"),
    ("BE_G", "INV", "-", "surekli", "özkaynak(ç0) / özkaynak(ç0-4) - 1; ikisi de > 0", "Lockwood-Prombutr 2010"),
    ("NSI_5Y", "INV", "-", "surekli", "ln(pay(t) / pay(t - 60 ay)); oran > 20 ya da < 1/20 ise veri yok", "Daniel-Titman 2006"),
    ("NEF", "INV", "-", "surekli", "(hisse ihracı geliri - geri alım - temettü) (y0; olmayan kalem 0) / [varlık(y0 sonu) + varlık(y0-1 sonu)] / 2", "Bradshaw-Richardson-Sloan 2006"),
    ("NDF_BS", "INV", "-", "surekli", "(uzun vadeli borç(ç0) - (ç0-4)) / [varlık(ç0) + varlık(ç0-4)] / 2 (bilanço yaklaşımı)", "Bradshaw-Richardson-Sloan 2006"),
    ("BUYBACK_YLD", "INV", "+", "surekli", "geri alım ödemesi (y0; yoksa 0, y0'da faaliyet nakit akışı olmalı) / PD", "Ikenberry-Lakonishok-Vermaelen 1995"),
    ("CAPEX_G", "INV", "-", "surekli", "yatırım harcaması(y0) / [(y0-1) + (y0-2)] / 2 - 1; payda > 0", "Anderson-Garcia-Feijoo 2006"),
    ("EAR_ANN", "EAR", "+", "surekli", "açıklama günü VEKİLİ d* = 10-Q / 10-K başvuru gününe kadarki 30 takvim günü içindeki (başvuru günü dahil) EN SON 8-K günü, yoksa "
     "başvuru günü. Tepki = d*'den önceki, d* ve sonraki işlem günlerinin bileşik getirisi - aynı günlerde French piyasa getirisi. "
     "Penceresi t'ye kadar bitmiş ve son 63 işlem günü içindeki EN SON olayın tepkisi", "Chan-Jegadeesh-Lakonishok 1996"),
    ("EAR_FILE", "EAR", "+", "surekli", "EAR_ANN ile aynı, olay günü 10-Q / 10-K başvuru gününün kendisi (K59 S4'ün 2021-22 tanımı)", "Chan-Jegadeesh-Lakonishok 1996"),
    ("SUE_SRW", "EAR", "+", "surekli", "(net kâr(ç0) - net kâr(ç0-4)) / son 8 yıllık farkın (ç0 .. ç0-7) std'si (ddof 1)", "Foster-Olsen-Shevlin 1984"),
    ("REV_SURP", "EAR", "+", "surekli", "SUE_SRW'nin gelirle hesaplanmışı", "Jegadeesh-Livnat 2006"),
    ("EARN_STREAK", "EAR", "+", "surekli", "art arda aynı işaretli yıllık net kâr farkı sayısı (ç0'dan geriye, en çok 8), işaretli", "Loh-Warachka 2012"),
    ("EAR_VOL", "EAR", "+", "surekli", "d* günündeki hacim / önceki 50 işlem gününün ortalama hacmi (en az 30); son 63 işlem günü içindeki en son olay", "Garfinkel-Sokobin 2006"),
    ("VOL_60D", "RSK", "-", "surekli", "son 60 işlem gününün günlük getiri std'si (en az 40)", "Ang-Hodrick-Xing-Zhang 2006"),
    ("IVOL_FF3", "RSK", "-", "surekli", "t'nin takvim ayındaki günlük fazla getirinin French günlük MKT-RF, SMB, HML üzerine EKK artıklarının std'si (en az 15 gün)", "Ang-Hodrick-Xing-Zhang 2006"),
    ("BETA_BAB", "RSK", "-", "surekli", "korelasyon(hisse, piyasa; son 1260 gün, en az 504) x σ_hisse / σ_piyasa (son 252 gün, en az 120); günlük basit getiri, piyasa = French MKT", "Frazzini-Pedersen 2014"),
    ("MAX5", "RSK", "-", "surekli", "t'nin takvim ayındaki en yüksek 5 günlük getirinin ortalaması (en az 15 gün)", "Bali-Cakici-Whitelaw 2011"),
    ("SKEW_TOT", "RSK", "-", "surekli", "t'nin takvim ayındaki günlük getirilerin çarpıklığı (en az 15 gün)", "Bali-Engle-Murray 2015"),
    ("ISKEW", "RSK", "-", "surekli", "IVOL_FF3 artıklarının çarpıklığı", "Boyer-Mitton-Vorkink 2010"),
    ("PRICE_LVL", "RSK", "-", "surekli", "ln(o günkü fiyat) (ölçü yüksek = pahalı; beklenen yön düşük fiyat lehine)", "Blume-Husic 1973"),
    ("SIZE_ME", "LIQ", "-", "surekli", "ln(PD)", "Banz 1981"),
    ("AMIHUD", "LIQ", "+", "surekli", "son 252 işlem gününde (en az 150) ortalama |günlük getiri| / (C x hacim); işlem değeri 0 olan gün dışarıda", "Amihud 2002"),
    ("TURN_12M", "LIQ", "-", "surekli", "son 252 işlem gününün (en az 150) ortalama hacmi / pay sayısı (ikisi de bugünkü pay biriminde)", "Datar-Naik-Radcliffe 1998"),
    ("DOLVOL", "LIQ", "-", "surekli", "ln(m-1 ayının ortalama günlük işlem değeri)", "Brennan-Chordia-Subrahmanyam 1998"),
    ("VOL_SHOCK", "LIQ", "+", "surekli", "son 5 işlem gününün ortalama hacmi / ondan önceki 50 günün ortalama hacmi (en az 3 ve 30 gözlem)", "Gervais-Kaniel-Mingelgrin 2001"),
    ("SPREAD_CS", "LIQ", "+", "surekli", "Corwin-Schultz alış-satış farkı tahmini, t'nin takvim ayındaki günlük çiftlerin ortalaması (eksi tahmin 0; en az 12 çift)", "Corwin-Schultz 2012"),
    ("GAP_OVN", "LIQ", "?", "surekli", "t'nin takvim ayındaki gece getirilerinin toplamı Σ ln(açılış(g) / C(g-1)) (en az 15 gün)", "Lou-Polk-Skouras 2019"),
    ("SEAS_1", "SEA", "+", "surekli", "m-11 ayının getirisi (gelecek ayla aynı takvim ayı, bir yıl önce)", "Heston-Sadka 2008"),
    ("SEAS_2_5", "SEA", "+", "surekli", "m-23, m-35, m-47, m-59 aylarının getiri ortalaması (dördü de olmalı)", "Heston-Sadka 2008"),
    ("EA_MONTH", "SEA", "+", "bayrak", "gelecek ayla aynı takvim ayında bir yıl önce açıklama günü vekili d* var (o aya kadar en az bir 10-Q / 10-K başvurusu olmalı)", "Frazzini-Lamont 2007"),
    ("DIV_MONTH", "SEA", "+", "bayrak", "gelecek aydan 3, 6 ya da 12 ay önceki takvim ayında temettü hak düşüm günü var", "Hartzmark-Solomon 2013"),
    ("RUNWAY", "DIS", "-", "surekli", "nakit tüketim hızı = -faaliyet nakit akışı(y0) / nakit(ç0); nakit > 0 (yüksek = hızlı tüketim; yıllık sürüm)", "proje ölçüsü (K31 M3)"),
    ("NT_LATE", "DIS", "-", "bayrak", "son 60 takvim gününde (t hariç) NT 10-K / NT 10-Q başvurusu", "Bartov-Konchitchki 2017"),
    ("CHS_FAIL", "DIS", "-", "surekli", "Campbell-Hilscher-Szilagyi 12 ay ufuklu batma logiti (katsayılar makaleden sabit; girdiler ay içinde %5 / %95'te kırpılır)", "Campbell-Hilscher-Szilagyi 2008"),
    ("O_SCORE", "DIS", "-", "surekli", "Ohlson (1980) batma puanı, yıllık (y0, y0-1); FFO yerine faaliyet nakit akışı", "Dichev 1998"),
    ("IND_MOM_6", "SEC", "+", "surekli", "aynı SIC 2 hane sektöründeki uygun hisselerin (en az 5) A(m) / A(m-6) - 1 eşit ağırlıklı ortalaması", "Moskowitz-Grinblatt 1999"),
    ("IND_LEAD_BIG", "SEC", "+", "surekli", "aynı SIC 2 hane sektöründe (PD'si olan en az 10 uygun hisse) m-1 ay sonu PD'sine göre en büyük %30'un m ayı getirisi ortalaması; "
     "yalnız kalan %70'e atanır", "Hou 2007"),
    ("ACT_13D", "OWN", "+", "bayrak", "son 60 takvim gününde SC 13D / SCHEDULE 13D (değişiklik hariç) başvurusu", "Brav et al. 2008"),
    ("E_S3", "EVT", "-", "bayrak", "son 90 takvim gününde S-3 / S-3ASR", "Loughran-Ritter 1995"),
    ("E_424B5", "EVT", "-", "bayrak", "son 60 takvim gününde 424B5", "Loughran-Ritter 1995; Billett et al. 2019"),
    ("E_TENDER_SELF", "EVT", "+", "bayrak", "son 90 takvim gününde SC TO-I", "Peyer-Vermaelen 2009"),
    ("E_IPO_3Y", "EVT", "-", "bayrak", "ilk işlem günü (Yahoo) t'den en çok 1095 gün önce", "Ritter 1991"),
    ("E_SPLIT", "EVT", "+", "bayrak", "son 365 günde oranı >= 2 olan ileri bölünme", "Ikenberry-Rankine-Stice 1996"),
    ("E_RSPLIT", "EVT", "-", "bayrak", "son 365 günde ters bölünme (oran < 1)", "Kim-Klein-Rosenfeld 2008"),
    ("E_DIV_INIT", "EVT", "+", "bayrak", "son 365 günde temettü var, ondan önceki 730 günde yok (fiyat geçmişi en az 1095 gün)", "Michaely-Thaler-Womack 1995"),
    ("E_DIV_OMIT", "EVT", "-", "bayrak", "(t-730, t-365] aralığında en az 2 temettü var, son 365 günde yok", "Michaely-Thaler-Womack 1995"),
]
# (kod, aile, neden): bu turda ÖLÇÜLMEYEN envanter satırları
_K60_DALGA2: List[Tuple[str, str, str]] = [
    ("INV_A", "INV", "DALGA 2: PropertyPlantAndEquipmentNet, InventoryNet etiketleri inmedi"), ("INVTRY_G", "INV", "DALGA 2: InventoryNet inmedi"),
    ("HIRE_G", "INV", "YOK: XBRL'de düzenli etiket yok"),
    ("SUE_ANALYST", "EAR", "DALGA 2: Nasdaq takvimi 2022-12+; KEŞİF'te yok"), ("REC_UP", "EAR", "DALGA 2: Yahoo analist günlüğü"),
    ("REC_DOWN", "EAR", "DALGA 2: Yahoo analist günlüğü"), ("PT_REV", "EAR", "DALGA 2: Yahoo analist günlüğü"),
    ("N_ANALYST_CHG", "EAR", "DALGA 2: Yahoo analist günlüğü"), ("EPS_REV", "EAR", "YOK: IBES ücretli"), ("GUIDANCE_UP", "EAR", "YOK: metin"),
    ("INS_BUY_90", "OWN", "DALGA 2: Form 4 (2012-2020 inmedi)"), ("INS_CLUSTER", "OWN", "DALGA 2: Form 4"), ("INS_OPP_BUY", "OWN", "DALGA 2: Form 4"),
    ("INS_SELL_90", "OWN", "DALGA 2: Form 4"), ("INS_OPP_SELL", "OWN", "DALGA 2: Form 4"), ("IO_BREADTH_CHG", "OWN", "DALGA 2: 13F + CUSIP"),
    ("IO_CHG", "OWN", "DALGA 2: 13F + CUSIP"), ("SI_RATIO", "OWN", "DALGA 2: FINRA açığa satış"), ("DTC", "OWN", "DALGA 2: FINRA açığa satış"),
    ("SI_LOW", "OWN", "DALGA 2: FINRA açığa satış"), ("SHORT_VOL", "OWN", "DALGA 2: FINRA Reg SHO"),
    ("TAXLOSS_JAN", "SEA", "BU CETVELLE ÖLÇÜLEMEZ: yılda tek oluşum ayı (KEŞİF'te 10 gözlem < 36)"),
    ("Z_SCORE", "DIS", "DALGA 2: RetainedEarningsAccumulatedDeficit inmedi"), ("GC_FLAG", "DIS", "DALGA 2: EDGAR tam metin arama"),
    ("E_101", "EVT", "DALGA 2: 8-K madde kodu"), ("E_201", "EVT", "DALGA 2: 8-K madde kodu"), ("E_205_206", "EVT", "DALGA 2: 8-K madde kodu"),
    ("E_301", "EVT", "DALGA 2: 8-K madde kodu"), ("E_302", "EVT", "DALGA 2: 8-K madde kodu"), ("E_401", "EVT", "DALGA 2: 8-K madde kodu"),
    ("E_402", "EVT", "DALGA 2: 8-K madde kodu"), ("E_502", "EVT", "DALGA 2: 8-K madde kodu"),
    ("E_LOCKUP", "EVT", "BU EVRENDE ÖLÇÜLEMEZ: 252 gün geçmiş şartı halka arz + 180 gün penceresini dışarıda bırakır"),
    ("E_MA_TARGET", "EVT", "BU EVRENDE ÖLÇÜLEMEZ: devralınan şirket bugün yaşamıyor (yalnız yaşayanlar)"),
    ("E_IDX_ADD", "EVT", "DALGA 2: S&P 500 değişiklik tablosu"), ("E_SPINOFF", "EVT", "DALGA 2: 10-12B + evren dışı CIK eşlemesi"),
    ("COMM_LINK", "SEC", "DALGA 2: tanım belirsiz ('şüpheli'), k36 serilerinin bilgi tarihi denetlenmedi"),
    ("IO_MOM_CUST", "SEC", "DALGA 2: BEA girdi-çıktı tabloları"), ("IO_MOM_SUPP", "SEC", "DALGA 2: BEA girdi-çıktı tabloları"),
    ("GEO_MOM", "SEC", "DALGA 2: SEC adres alanı"), ("CUST_MOM", "SEC", "YOK: müşteri eşlemesi ücretli"),
    ("LAZY_SIM", "TXT", "DALGA 2: 10-K tam metinleri"), ("TONE_NEG", "TXT", "DALGA 2: Loughran-McDonald özetleri"), ("TONE_CHG", "TXT", "DALGA 2: Loughran-McDonald özetleri"),
]
_K60_AILE_SIRA = ["MOM", "VAL", "PRF", "INV", "EAR", "RSK", "LIQ", "SEA", "DIS", "SEC"]


def _k60_aile_bilesikleri() -> Dict[str, Dict[str, Any]]:
    """Aile bileşikleri: ailenin SÜREKLİ ve yönü belli ('+' / '-') üyelerinin yüzdelik sıra ortalaması (beklenen yön uygulanmış)."""
    out: Dict[str, Dict[str, Any]] = {}
    for a in _K60_AILE_SIRA:
        uye = [k for k, al, yon, tur, _t, _k in _K60_KUTUPHANE if al == a and tur == "surekli" and yon in "+-"]
        out["AILE_" + a] = {"ad": f"{a} ailesi bileşiği", "uye": uye, "min": int(math.ceil(len(uye) / 2)), "rol": "AİLE"}
    return out


# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256'sı K60_ON_KAYIT.md'de; sonradan değişmez)
K60_ESIK: Dict[str, Any] = {
    "veri": {"kes": "2026-08-31", "tur": ["EQUITY"], "kirpik_haric": True, "takvim_pay": 0.20, "ceyrek_bas": "2009Q1", "ceyrek_son": "2026Q2",
             "yil_bas": 2009, "yil_son": 2025, "french_gunluk": "F-F_Research_Data_Factors_daily_CSV.zip", "sic": "origin/islenmis-veri:k35/k35_sic.csv",
             "min_hisse": 3000},
    "uygunluk": {"fiyat_min": 2.0, "likit_min": 1.0e6, "likit_gun": 20, "likit_min_gun": 15, "gecmis_gun": 252, "ileri_tasima": 5, "min_evren": 100},
    "donem": {"kesif": ["2012-01", "2021-12"], "dogrulama": ["2022-01", "2023-12"], "kasa": ["2024-01", "2026-08"]},
    "bilgi": {"form_yil": ["10-K", "10-KT", "10-K405", "10-KSB", "20-F", "40-F"], "form_ceyrek": ["10-Q", "10-QT", "10-QSB"], "form_8k": ["8-K"],
              "form_nt": ["NT 10-K", "NT 10-Q", "NTN 10K", "NTN 10Q"], "form_s3": ["S-3", "S-3ASR"], "form_424b5": ["424B5"],
              "form_13d": ["SC 13D", "SCHEDULE 13D"], "form_toi": ["SC TO-I"],
              "yedek_ceyrek_gun": 90, "yedek_yil_gun": 120, "mali_yil_tol_gun": 10, "pay_yedek_gun": 60, "en_az_gun": 15,
              "ceyrek_max_gun": 200, "yil_max_gun": 550, "pay_max_gun": 400, "yil_sure": [350, 380]},
    "param": {"vol_gun": 60, "vol_min": 40, "yil_gun": 252, "yil_min": 150, "zirve_min": 200, "ay_min_gun": 15, "beta_kor_gun": 1260, "beta_kor_min": 504,
              "beta_vol_min": 120, "fip_min_gun": 200, "trend_gun": [3, 5, 10, 20, 50, 100, 200], "trend_ay": 12, "res_ay": 36, "res_son": 11,
              "ear_pencere": 63, "ear_8k_gun": 30, "evol_gun": 50, "evol_min": 30, "sue_n": 8, "streak_max": 8, "shock_kisa": 5, "shock_uzun": 50,
              "shock_min": [3, 30], "cs_min": 12, "nsi1_aykiri": 5.0, "nsi5_aykiri": 20.0, "sektor_min": 5, "lead_min": 10, "lead_pay": 0.30,
              "bayrak_gun": {"NT_LATE": 60, "ACT_13D": 60, "E_S3": 90, "E_424B5": 60, "E_TENDER_SELF": 90}, "ipo_gun": 1095, "olay_gun": 365,
              "sigma_gun": 63, "fscore_min": 7,
              "chs": {"sabit": -9.16, "NIMTAAVG": -20.26, "TLMTA": 1.42, "EXRETAVG": -7.13, "SIGMA": 1.41, "RSIZE": -0.045, "CASHMTA": -2.13, "MB": 0.075,
                      "PRICE": -0.058, "kirp": [5.0, 95.0], "fiyat_tavan": 15.0},
              "ohlson": {"sabit": -1.32, "lnTA": -0.407, "TLTA": 6.03, "WCTA": -1.43, "CLCA": 0.076, "OENEG": -1.72, "NITA": -2.37, "FUTL": -1.83,
                         "INTWO": 0.285, "CHIN": -0.521}},
    "kutuphane": [{"kod": k, "aile": a, "yon": y, "tur": t, "tanim": tn, "kaynak": ky} for k, a, y, t, tn, ky in _K60_KUTUPHANE],
    "dalga2": [{"kod": k, "aile": a, "neden": n} for k, a, n in _K60_DALGA2],
    "ek_bilesen": {"REV_YOY": "gelir(ç0) / gelir(ç0-4) - 1; ikisi de > 0 (K59 X1). Yalnız DOSYA_Y üyesidir; tek başına ÖLÇÜLMEZ"},
    "bilesik": {**_k60_aile_bilesikleri(),
                "COMP4": {"ad": "K59 COMP4: momentum + bilanço tepkisi + kârlılık + düşük ihraç", "uye": ["MOM_12_1", "EAR_ANN", "ROE_TTM", "NSI_1Y"], "min": 3,
                          "rol": "K59"},
                "DOSYA_Y": {"ad": "K59 DOSYA_Y (YEOTK tipi): ivmelenen, kârlı, seyrelmesiz büyüme",
                            "uye": ["SALES_ACCEL", "REV_YOY", "ROE_TTM", "NSI_1Y", "EAR_ANN"], "min": 4, "rol": "K59"}},
    "portfoy": {"dilim": 0.10, "min_sinyal": 100, "min_bayrak": 10, "bag_tohum": 60001},
    "r1": {"maliyet": 0.001, "cetvel": {"nw_lag": 6, "t_esik": 2.0, "alt_donem_n": 3, "alt_donem_min": 2, "son_pay": 0.30},
           "min_ay": {"kesif": 36, "dogrulama": 18, "kasa": 18}},
    "r2": {"ufuk": [12, 6, 3], "ana_ufuk": 12, "olay": {"p100": 1.0, "p50": 0.5, "m50": -0.5}, "blok": 12, "cekilis": 500, "tohum": 60002,
           "guven": [2.5, 97.5], "min_ay": 12, "min_hisse_ay": 200},
    "coklu": {"bh_q": 0.10, "t_dogrudan": 3.0, "plasebo_n": 200, "plasebo_tohum": 60100, "maks_tekrar": 2000, "maks_tohum": 60003, "maks_yuzde": 95.0,
              "yp_esik": 0.05},
    "dogrulama": {"t_tek_yon": 1.65, "plasebo_yuzde": 95.0},
    "model": {"girdi": ["AILE_" + a for a in _K60_AILE_SIRA], "hedef": "p100", "ufuk": 12, "eksik": 0.5, "ridge": 1.0e-6, "tur": 50, "dilim": 10},
    "etiket": {"iz": "K60-İZ ADAYI", "olasilik": "K60-OLASILIK İZİ", "kacinma": "K60-KAÇINMA İZİ", "ters": "K60-R1 TERS (bilgi)"},
    # K58 / K59 / K59-B'de (başka evren ve dönemlerde, yalnız R1 ile) sonucu görülmüş satırlar: K60'ta R1 için tam kör sayılmaz (raporda yazılır)
    "kor_degil": ["MOM_12_1", "ROE_TTM", "NSI_1Y", "SALES_ACCEL", "VOL_60D", "HIGH52", "STREV_1M", "SIZE_ME", "COMP4", "DOSYA_Y"],
}


class K60Hata(RuntimeError):
    """K60'a özgü durdurucu hata (ön kayıt yok / değişmiş / git'e işlenmemiş, veri eksik ya da farklı, dönem sırası bozuk, kasa ikinci kez)."""


def k60_tanim(E: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
    return {r["kod"]: r for r in (E or K60_ESIK)["kutuphane"]}


def _k60_bagimli() -> Dict[str, Any]:
    """Mühre giren dış tanımlar: K59 cetvel v2 ve French kuralları, K58 portföy cetveli, K60_veri uygunluk / kesik."""
    return {"K59_cetvel": K59.K59_ESIK["cetvel"], "K59_french": K59.K59_ESIK["french"], "K58_B_zip": K58.K58_ESIK["B"]["zip"],
            "K57_ABD_GELIR": list(K57.K57_ABD_GELIR), "K60V_uygunluk": KV.K60V_ESIK["uygunluk"], "K60V_kes": KV.K60V_ESIK["yahoo"]["kes"],
            "K60V_kirpik_gun": KV.K60V_ESIK["yahoo"]["kirpik_gun"]}


def k60_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: K60_ESIK (kütüphane tanımları dahil) + dış tanımlar; biri değişirse koşu durur."""
    s = json.dumps({"K60_ESIK": E or K60_ESIK, "bagimli": _k60_bagimli()}, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _k60_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K60_YOL["cikti"], K60_DOSYA.get(ad, ad))


def _k60_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


_k60_sha = K58._k58_dosya_sha
_yz, _sy = K58._yz, K58._sy


def _k60_metin_sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _k60_json_yaz(yol: str, govde: Any) -> str:
    """Kararlı JSON (anahtar sıralı; aynı içerik -> aynı bayt). Döner: sha256."""
    metin = json.dumps(govde, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n"
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return _k60_metin_sha(metin)


def _k60_json_oku(yol: str) -> Any:
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- 0) VERİ SHA256
def _k60_git_blob(dal_yolu: str) -> Optional[bytes]:
    """Git'teki bir dosyanın içeriği (ör. origin/islenmis-veri:k35/k35_sic.csv); yoksa None. Ağ kullanılmaz."""
    try:
        r = subprocess.run(["git", "-C", KOK_K60, "show", dal_yolu], capture_output=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 and r.stdout else None


def k60_frame_yollari() -> Tuple[List[Dict[str, Any]], List[str]]:
    """K60'ın okuyacağı bütün SEC çerçeveleri: her satıra 'yol' eklenir (önce yeni önbellek, yoksa K59 girdisi olan eski önbellek).
    Döner: (satırlar, eksik çerçeve adları). Dizin dosyaları satırlara 'tur' = 'dizin' ile eklenir."""
    kl = KV.K60V_YOL["frames"]; sat = []; eksik = []
    for r in KV.k60v_sec_listesi(True) + KV.k60v_dizin_listesi():
        y = os.path.join(kl, r["dosya"])
        if os.path.exists(y) and os.path.getsize(y) >= 2:
            sat.append({**r, "yol": y, "kaynak": "k60"})
        elif r.get("mevcut"):
            sat.append({**r, "yol": r["mevcut"], "kaynak": "eski"})
        else:
            eksik.append(r["ad"])
    return sat, eksik


def k60_veri_sha(dogrula: bool = True) -> Dict[str, Tuple[str, int]]:
    """Koşunun okuyacağı bütün verinin sha256'sı: ad -> (sha256, dosya sayısı). SEC ya da fiyat önbelleği eksikse / manifestle aynı değilse durur
    (dogrula=True: manifestteki her dosyanın sha256'sı diskten yeniden hesaplanır)."""
    out: Dict[str, Tuple[str, int]] = {}
    for ad, kl in (("k60_fiyat", KV.K60V_YOL["fiyat"]), ("k60_secframes", KV.K60V_YOL["frames"])):
        if not os.path.exists(os.path.join(kl, KV.K60V_DOSYA["manifest"])):
            raise K60Hata(f"{ad}: manifest yok ({kl}); önce K60_veri indirmeleri (ana oturum) tamamlanmalı")
        if dogrula:
            m = KV.k60v_manifest_dogrula(kl)
            if not m["saglam"]:
                raise K60Hata(f"{ad}: önbellek manifestle aynı değil (farklı {len(m['farkli'])}, eksik {len(m['eksik'])}, fazla {len(m['fazla'])})")
            out[ad] = (m["klasor_ozet_sha256"], int(m["dosya"]))
        else:
            M = KV.K60VManifest(kl); out[ad] = (M.ozet_sha(), len(M.d))
        try:
            dr = _k60_json_oku(os.path.join(kl, KV.K60V_DOSYA["durum"])).get("durum")
        except (OSError, ValueError):
            dr = None
        if dr != "tamam":
            raise K60Hata(f"{ad}: indirme durumu 'tamam' değil ({dr}); K60 eksik önbellekle başlamaz")
    sat, eksik = k60_frame_yollari()
    if eksik:
        raise K60Hata(f"SEC önbelleği eksik: {len(eksik)} çerçeve / dizin dosyası yok (ör. {eksik[:3]}); K60 SEC'e istek atmaz")
    eski = sorted(r["yol"] for r in sat if r["kaynak"] == "eski")
    if eski:
        out["eski_secframes"] = (K59._k59_klasor_sha(eski), len(eski))
    if not os.path.exists(K60_YOL["tickers"]):
        raise K60Hata(f"CIK - borsa kodu eşlemesi yok: {K60_YOL['tickers']}")
    out["company_tickers.json"] = (_k60_sha(K60_YOL["tickers"]), 1)
    ham = _k60_git_blob(K60_ESIK["veri"]["sic"])
    if ham is None:
        raise K60Hata(f"SIC tablosu okunamadı ({K60_ESIK['veri']['sic']}); `git fetch origin islenmis-veri` gerekir")
    out["k35_sic.csv"] = (hashlib.sha256(ham).hexdigest(), 1)
    fg = os.path.join(K60_YOL["french_gunluk"], K60_ESIK["veri"]["french_gunluk"])
    if not os.path.exists(fg):
        raise K60Hata(f"French günlük faktör dosyası yok: {fg}")
    out[K60_ESIK["veri"]["french_gunluk"]] = (_k60_sha(fg), 1)
    for z in K58.K58_ESIK["B"]["zip"].values():
        y = os.path.join(K58.K58_YOL["french"], z)
        if not os.path.exists(y):
            raise K60Hata(f"French aylık faktör dosyası yok: {y}")
        out[z] = (_k60_sha(y), 1)
    return out


# ---------------------------------------------------------------- 1) ÖN KAYIT
def k60_kapsam_notu(cikti: Optional[str] = None) -> str:
    """Faz 1 kapsam sayımının (kapsam.csv + kapsam_ozet.json; yalnız SAYI) ön kayıt metnine giren özeti. Mühre girmez (eşik değil)."""
    yk, yo = _k60_yol("kapsam", cikti), _k60_yol("kapsam_ozet", cikti)
    if not (os.path.exists(yk) and os.path.exists(yo)):
        return "Kapsam sayımı henüz koşulmadı (`python -I K60.py kapsam`); `kos` başında veri sha256'ları doğrulanır, sayım koşu meta dosyasına yazılır."
    K = pd.read_csv(yk); O = _k60_json_oku(yo); sat = []
    ev = O.get("evren", {})

    def yz(anahtar: str) -> str:
        v = O.get(anahtar)
        return "?" if v is None else f"{float(v) * 100:.1f}"
    bas = (f"Faz 1 kapsam sayımı ({O.get('zaman', '?')}; `python -I K60.py kapsam`; yalnız hisse / ay SAYILARI: getiri, olasılık, t hesaplanmadı).\n"
           f"Yüklenen hisse {O.get('hisse', '?')} (dışarıda: kırpık {O.get('kirpik', '?')}, tür dışı {O.get('tur_disi', '?')}, fiyatı yok {O.get('fiyatsiz', '?')}); "
           f"CIK'i olan {O.get('cikli', '?')}, SIC'i olan {O.get('sicli', '?')}; işlem günü {O.get('gun', '?')} ({O.get('ilk_gun', '?')} .. {O.get('son_gun', '?')}), ay sonu {O.get('ay', '?')}.\n"
           f"Bilgi tarihi kaynağı: çeyrek kayıtlarının %{yz('bilgi_dizin_pay')}'i, yıllık kayıtların %{yz('ybilgi_dizin_pay')}'i EDGAR dizininden (gerçek başvuru günü), kalanı yedek "
           f"kuraldan; yıllıktan türetilen 4. çeyrek {O.get('turetilen_q4', '?')}. Pay sayısı kaynağı (uygun hisse-ay, KEŞİF): kapak (dei) %{yz('pay_dei')}, bilanço %{yz('pay_cso')}, "
           f"ağırlıklı ortalama %{yz('pay_wads')}, yok %{yz('pay_yok')}.\n")
    dn = "\n".join(f"- {K60_DONEM_AD[d]}: oluşum ayı R1 {v.get('ay_r1')} ({v.get('ilk')} .. {v.get('son_r1')}), R2 12 ay {v.get('ay_r2_12')} (son {v.get('son_r2_12')}), "
                   f"6 ay {v.get('ay_r2_6')}, 3 ay {v.get('ay_r2_3')}; uygun evren ortalama {v.get('ort_evren')} ({v.get('min_evren')} - {v.get('maks_evren')}); uygun hisse-aylarda "
                   f"bilinen çeyrek payı %{float(v.get('ceyrek_bilinen') or 0) * 100:.0f}, bilinen mali yıl payı %{float(v.get('yil_bilinen') or 0) * 100:.0f}"
                   for d in K60_DONEM for v in [ev.get(d)] if v)
    for kod, g in K.groupby("sinyal", sort=False):
        h = {r.donem: r for r in g.itertuples()}

        def hucre(d: str) -> str:
            r = h.get(d)
            return "—" if r is None or not r.olcum_ay else f"{int(r.olcum_ay)} / {int(round(r.ort_n))}"
        r0 = g.iloc[0]
        sat.append(f"| {kod} | {r0.aile} | {r0.tur} | {hucre('kesif')} | {hucre('dogrulama')} | {hucre('kasa')} | {h['kesif'].ilk_ay if 'kesif' in h and isinstance(h['kesif'].ilk_ay, str) else '—'} |")
    tablo = ("| sinyal | aile | tür | KEŞİF ay / ort. hisse | DOĞRULAMA | KASA | KEŞİF ilk ölçüm ayı |\n|---|---|---|---|---|---|---|\n" + "\n".join(sat))
    return (bas + dn + "\n\n'ay' = R1'de ölçülebilen oluşum ayı sayısı (sürekli sinyal: sinyali olan uygun hisse >= min_sinyal olan ilk aydan sona; bayrak: bayraklı "
            "hisse >= min_bayrak olan aylar); 'ort. hisse' = o aylarda sinyali olan (bayrakta: bayraklı) uygun hisse ortalaması.\n\n" + tablo)


def k60_onkayit_metin(zaman: str, veri_sha: Dict[str, Tuple[str, int]], kapsam: str) -> str:
    E = K60_ESIK; uy = E["uygunluk"]; Dn = E["donem"]; Bg = E["bilgi"]; Pf = E["portfoy"]; R1 = E["r1"]; R2 = E["r2"]; Ck = E["coklu"]; Dg = E["dogrulama"]
    Md = E["model"]; C = R1["cetvel"]; Et = E["etiket"]
    vs = "\n".join(f"- {k}: sha256 {v[0]} ({v[1]} dosya)" for k, v in veri_sha.items()) or "- (veri dosyası bulunamadı)"
    L = E["kutuphane"]
    kut = "\n".join(f"| {r['kod']} | {r['aile']} | {r['yon']} | {r['tur']} | {r['tanim']} | {r['kaynak']} |" for r in L)
    say = pd.Series([r["aile"] for r in L]).value_counts()
    say2 = pd.Series([r["aile"] for r in E["dalga2"]]).value_counts()
    aileler = list(dict.fromkeys([r["aile"] for r in L] + [r["aile"] for r in E["dalga2"]]))
    sayim = "\n".join(f"| {a} | {int(say.get(a, 0))} | {int(say2.get(a, 0))} |" for a in aileler)
    d2 = "\n".join(f"- {r['kod']} ({r['aile']}): {r['neden']}" for r in E["dalga2"])
    bil = "\n".join(f"- {k} ({v['rol']}): {', '.join(v['uye'])}; en az {v['min']} üye." for k, v in E["bilesik"].items())
    n_s = len(L); n_b = len(E["bilesik"]); n_bay = sum(r["tur"] == "bayrak" for r in L); n_q = sum(r["yon"] == "?" for r in L)
    m_r1 = (n_s - n_bay - n_q) + 2 * n_q + n_bay + n_b; m_r2 = 2 * (n_s - n_bay) + n_bay + 2 * n_b
    return f"""# K60 ÖN KAYIT — sinyal kütüphanesi, iki cetvel (portföy v2 + olasılık tablosu), üç dönem

Yazım zamanı: {zaman} (ölçümden ÖNCE; gerçek veride hiçbir sinyale bağlı getiri, olasılık ya da t hesaplanmadı, sonuç görülmedi). Sürüm: {K60_SURUM}
ESIK_SHA256: {k60_esik_sha()}
(K60_ESIK'in (kütüphane tanımları, dönemler, cetveller, çoklu deneme ve karar kuralları) + K59 cetvel v2 / French, K58 French dosya adları,
K57 gelir etiket sırası ve K60_veri uygunluk / kesik tanımlarının sha256'sı. `python -I K60.py kos --donem ...` bu mühürle, aşağıdaki veri
sha256'larıyla ve bu dosya git'e işlenmiş, sonradan değişmemişse başlar; biri tutmazsa koşu durur.)

## Veri (sha256; her koşunun başında yeniden hesaplanır)
{vs}
k60_fiyat ve k60_secframes = K60_veri manifestinin klasör özeti (ada göre sıralı 'dosya adı:sha256' satırlarının sha256'sı; her dosya diskten
yeniden özetlenir). eski_secframes = K59 girdisi olan /tmp/secframes'ten okunan çerçeveler (aynı kural). k35_sic.csv = git'teki dosyanın
özeti ({E['veri']['sic']}). SEC'e ve başka hiçbir yere istek atılmaz; önbellek eksikse ya da indirme durumu 'tamam' değilse koşu durur.

## 0. Soru, hedef çıktı, sınır
Soru: ölçülebilir hangi özellik büyük kazananların ve büyük kaybedenlerin OLASILIĞINI değiştiriyor, hangisi maliyetten sonra fazla getiri
bırakıyor? Hedef çıktı (CLAUDE.md 'Sonuç dili'): OLASILIK TABLOSU = her seçilmiş özellik için taban oran, P(12 ayda >= +%100), kaç kat (lift)
ve aralığı, aynısı -%50 için, dönem dönem. Ortalama getiri (R1) ikinci sırada raporlanır.
İZ ilan EDİLEMEZ: CLAUDE.md standardı (FI_OLCUT; ABD + Avrupa dört hücre) değişmedi; bu çalışma yalnız ABD, yalnız yaşayanlar. K60'ın
verebileceği en yüksek etiketler '{Et['iz']}', '{Et['olasilik']}', '{Et['kacinma']}' (§7); standart değişikliği Cemal'in kararıdır.
Bu ön kayıttan ÖNCE görülmüş ilgili sonuçlar (kör olmayan kısım): K58 / K59 / K59-B (momentum, kârlılık, COMP4, DOSYA_Y 2016-26 ve 2021-26
dönemlerinde, başka evrenlerde ve yalnız R1 ile ölçüldü; COMP4 PORTFÖY-ADAY çıkmadı). K60 evreni (2010'dan Yahoo, {E['veri']['min_hisse']}+ hisse), dönemleri
(KEŞİF 2012-2021) ve R2 cetveli yenidir; {', '.join(E['kor_degil'])} satırlarının
2016 / 2021 sonrası R1 davranışı kısmen bilinmektedir: bu {len(E['kor_degil'])} satır R1 için tam kör sayılmaz (raporda 'kör değil' diye yazılır). R2 hiçbir satırda görülmedi.
Faz 1'de gerçek veride yalnız `kapsam` koşuldu (hisse / ay / sinyal başına SAYI; §12).

## 1. Kütüphane ({n_s} sinyal ölçülür; {len(E['dalga2'])} envanter satırı bu turda ölçülmez)
Kaynak: arastirma_cikti/yol_haritasi/SINYAL_ENVANTERI.md. Listede olmayan sinyal sonradan EKLENMEZ (yol haritası §5 kural 1); eklenecekse yeni tur.
Simgeler: t = oluşum ayının son işlem günü, m = o ayın sırası; A = temettü + bölünme düzeltmeli kapanış (Yahoo adjclose), C = bölünme
düzeltmeli kapanış; ay sonu değerleri en çok {uy['ileri_tasima']} gün ileri taşınır. ç0 = bilgi tarihi < t olan en son çeyrek (çeyrek sonu t'den en çok
{Bg['ceyrek_max_gun']} gün önce); y0 = bilgi tarihi < t olan en son mali yıl (yıl sonu t'den en çok {Bg['yil_max_gun']} gün önce). 'son 4 çeyrek' = ç0 .. ç0-3 toplamı
(dördü de bilinmeli). Gelir = K57 etiket sırası ({', '.join(K57.K57_ABD_GELIR)}); bir formüldeki bütün çeyrekleri aynı etiketten olan ilk
etiket. Toplam varlık = Assets, yoksa LiabilitiesAndStockholdersEquity. Toplam yükümlülük = Liabilities, yoksa varlık - özkaynak. Uzun vadeli
borç = LongTermDebt, yoksa LongTermDebtNoncurrent. Satışların maliyeti = CostOfRevenue, yoksa CostOfGoodsAndServicesSold. Temettü =
PaymentsOfDividends, yoksa PaymentsOfDividendsCommonStock. PD (piyasa değeri) = C(t) x pay sayısı (bugünkü pay biriminde; §3).
yön: '+' = ölçü yüksekse beklenen getiri yüksek; '-' = düşük; '?' = iki yönlü. 'ÜST uç' = beklenen yöne göre en iyi %{Pf['dilim'] * 100:.0f}; 'ALT uç' = en kötü %{Pf['dilim'] * 100:.0f}.

| kod | aile | yön | tür | tanım (formül, pencere) | kaynak |
|---|---|---|---|---|---|
{kut}

Aile başına sayım:

| aile | ölçülen | bu turda ölçülmeyen |
|---|---|---|
{sayim}

Bu turda ÖLÇÜLMEYEN satırlar (DALGA 2 = K61, başka indirme ister; YOK = ücretsiz veri yok; ÖLÇÜLEMEZ = bu evren / cetvelle anlamsız):
{d2}

Bileşikler (ölçümden önce yazıldı; seçim yok). Yöntem K59 ile aynı: üyelerin ay içi yüzdelik sıralarının ((sıra - 0,5) / n; uygun ve o
üyesi olan hisseler arasında, beklenen yön uygulanmış, eşitlikte ortalama sıra) ortalaması; hissenin en az 'min' üyede değeri olmalı.
AİLE bileşiğine ailenin SÜREKLİ ve yönü belli üyeleri girer (bayrak ve '?' sinyaller girmez); OWN ve EVT aileleri yalnız bayraktan oluştuğu
için bileşikleri yoktur. Ek bileşen REV_YOY: {E['ek_bilesen']['REV_YOY']}.
{bil}

## 2. Dönemler (OLUŞUM ayına göre)
- KEŞİF {Dn['kesif'][0]} .. {Dn['kesif'][1]}; DOĞRULAMA {Dn['dogrulama'][0]} .. {Dn['dogrulama'][1]}; KASA {Dn['kasa'][0]} .. ileri penceresi {E['veri']['kes']}'e kadar biten son oluşum ayı
  (R1: 1 ay; R2: 12 / 6 / 3 ay; pencere sonu veri kesiğini aşan oluşum ayı ÖLÇÜLMEZ).
- Fon krizi kesiği: fiyatlar {E['veri']['kes']}'de kesilir (CLAUDE.md, 27 Ekim 2026).

## 3. Evren ve zaman kuralları
- Evren: K60_veri fiyat önbelleği (K57-B evren tablosu + V_ABD; yalnız BUGÜN borsa kodu olan şirketler). Yahoo düzeltilmiş kapanışı <= 0 olan
  günler yok sayılır. Tür {', '.join(E['veri']['tur'])}; Yahoo'nun geçmişini
  kırptığı hisseler ('kırpık': ilk verilen gün ilk işlem gününden {KV.K60V_ESIK['yahoo']['kirpik_gun']} günden fazla sonra) kural gereği DIŞARIDA. En az {E['veri']['min_hisse']} hisse
  yüklenemezse koşu durur. İşlem takvimi = hisselerin en az %{E['veri']['takvim_pay'] * 100:.0f} x medyan kadarının işlem gördüğü günler.
- UYGUNLUK (her ay sonu t, yalnız t ve öncesi bilgi; K59 U2 ile aynı eşikler): t'ye kadar en az {uy['gecmis_gun']} günlük kapanış; o günkü fiyat
  (C x t'den sonraki bölünmelerin çarpımı) >= {uy['fiyat_min']:g} $; son {uy['likit_gun']} işlem gününün (en az {uy['likit_min_gun']} gözlem) medyan işlem değeri (C x hacim) >= {uy['likit_min'] / 1e6:g} milyon $;
  ay sonu m ve m-1 kapanışı var. Uygun hisse < {uy['min_evren']} olan ay atlanır.
- BİLGİ TARİHİ (gerçek başvuru günü): EDGAR çeyreklik başvuru dizini (master.gz, 2009Q1-2026Q3) İNDİ ve kullanılır. Frames yanıtında
  başvuru günü ve dizinde dönem alanı olmadığı için eşleme kuralı: bir çeyreğin bilgi tarihi = şirketin, çeyrek sonundan en az {Bg['en_az_gun']} gün SONRA
  yaptığı ilk dönemsel başvurunun günü (ilk {Bg['en_az_gun']} gündeki başvuru geciken önceki dönemin başvurusu sayılır); çeyrek sonu şirketin bir mali yıl sonuna ±{Bg['mali_yil_tol_gun']} gün yakınsa form {', '.join(Bg['form_yil'])}, değilse {', '.join(Bg['form_ceyrek'])}
  (düzeltme başvuruları /A sayılmaz; şirketin hiç yıllık çerçevesi yoksa iki aileden ilk gelen). Eşleşen başvuru yoksa YEDEK: çeyrek sonu + {Bg['yedek_ceyrek_gun']} gün,
  mali yıl sonu + {Bg['yedek_yil_gun']} gün. Yıllık kalemler ve yıllıktan türetilen 4. çeyrek = o mali yılın 10-K gününde bilinir. Bir değer ancak
  bilgi tarihi < t ise (başvuru + 1 işlem günü kuralı) kullanılır.
- 4. çeyrek: çeyreklik çerçevede yoksa yıl - önceki üç çeyrek (yıllık süre {Bg['yil_sure'][0]}-{Bg['yil_sure'][1]} gün ve üç çeyrek de doluysa).
- PAY SAYISI: kapak sayfası sayısı (dei EntityCommonStockSharesOutstanding; tarihi kapak günü, bilgi tarihi = kapak gününden sonraki (dahil) ilk
  dönemsel başvuru, yoksa kapak günü + {Bg['pay_yedek_gun']} gün; kapak günü t'den en çok {Bg['pay_max_gun']} gün önce). Kapak sayısı x kapak gününden SONRAKİ bölünmelerin çarpımı
  = bugünkü pay birimi (Yahoo kapanışı ve hacmi de bu birimdedir). Kapak sayısı olmayan hisselerde yedek: bilanço pay sayısı
  (CommonStockSharesOutstanding, ç0), o da yoksa ağırlıklı ortalama seyreltilmiş pay (ç0); yedekler YALNIZ Yahoo'da hiç bölünme kaydı
  olmayan hisselerde kullanılır (frames eski dönem pay sayılarını bölünme sonrası yeniden bildirilmiş haliyle verebilir).
- İşlem zamanı: sinyal t kapanışında hesaplanır; R1 ay sonu kapanışından sonraki ay sonu kapanışına (K59 / K58 ile aynı), R2 ay sonu
  kapanışından h ay sonraki ay sonu kapanışına; getiri temettü dahil (A).

## 4. Cetvel R1 — portföy cetveli v2 (K59 ile aynı; K59.k59_cetvel_v2 ve K58.k58_portfoy çağrılır)
- Portföy: sinyali olan uygun hisselerin ÜST ucu (sayı = max(1, yuvarla({Pf['dilim']:g} x sinyali olan uygun hisse))), eşit ağırlık, aylık dengeleme, 1 ay
  tutma, maliyet tek yön {R1['maliyet'] * 1e4:.0f} bp x devir. Kıyas = BÜTÜN uygun evrenin eşit ağırlıklı getirisi. Aykırı getiri kırpması YOK.
- İstatistikler dönemin kendi ayları içinde: net fazla ortalaması ve NW t (gecikme {C['nw_lag']}); ardışık {C['alt_donem_n']} alt dönemin en az {C['alt_donem_min']}'sinde fazla > 0;
  son %{C['son_pay'] * 100:.0f} ayda fazla > 0; beta düzeltmeli alfa (portföy = alfa + beta x kıyas) ve NW t(alfa). 'cetvel v2 TUTAR' = K59'daki dört şart
  (t eşiği {C['t_esik']}); her dönemde ayrı sütun olarak raporlanır. En az ölçüm ayı: KEŞİF {R1['min_ay']['kesif']}, DOĞRULAMA {R1['min_ay']['dogrulama']}, KASA {R1['min_ay']['kasa']}.
- Ölçüm ayları: sürekli sinyalde dönemin içinde sinyali olan uygun hisse sayısının ilk kez >= {Pf['min_sinyal']} olduğu aydan dönem sonuna (K59 kuralı);
  bayrakta bayraklı uygun hisse >= {Pf['min_bayrak']} olan aylar.
- R1 istatistiği = t(alfa) (net). p değeri iki yönlü normal yaklaşımı. Bilgi sütunları: FF5 + UMD alfası, Sharpe, en büyük düşüş, devir,
  brüt (maliyetsiz) karşılıklar, en büyük üç katkı (hisse ve toplam getiri katkısındaki payı).

## 5. Cetvel R2 — OLASILIK TABLOSU
- Her sinyalin ÜST ve ALT ucu (bayrakta bayraklı grup) için, R1 ile aynı ölçüm aylarında (ileri penceresi veride biten aylar): h ay ileri
  toplam getiri F_h = A(m+h) / A(m) - 1 (m+h ay sonunda son {uy['ileri_tasima']} işlem gününde fiyatı olmayan hisse-ay dışarıda). ANA ufuk {R2['ana_ufuk']} ay; {', '.join(str(u) for u in R2['ufuk'] if u != R2['ana_ufuk'])} ay bilgi.
- P(F >= +%100), P(F >= +%50), P(F <= -%50), ortalama ve medyan F; aynıları BÜTÜN uygun evren için aynı aylarda (taban oran). Olasılık =
  hisse-ay havuzunda olay sayısı / hisse-ay sayısı (ay ağırlığı = o ayki hisse sayısı). LIFT = P(uç) / P(evren).
- Belirsizlik: ay kümeli DAİRESEL blok bootstrap; blok {R2['blok']} ay, {R2['cekilis']} çekiliş, tohum {R2['tohum']} (çekiliş dizini yalnız ay sayısına bağlı; bütün sinyaller
  ve plasebolar aynı çekilişleri kullanır); %95 aralık = lift çekilişlerinin %{R2['guven'][0]:g} ve %{R2['guven'][1]:g} dilimleri. Örtüşen {R2['ana_ufuk']} aylık pencereler
  KABUL EDİLİR: komşu ayların sonuçları bağımlıdır, blok boyu bu yüzden {R2['blok']} aydır; aralık yine de dar kalabilir (plasebo ile sınanır).
- p değeri (lift > 1): p_z = 1 - Φ(ln(lift) / sd(ln(lift çekilişleri))); ayrıca yüzdelik p = (1 + #(çekiliş lift <= 1)) / (çekiliş + 1) raporlanır.
- Ölçülebilirlik: en az {R2['min_ay']} oluşum ayı ve uçta en az {R2['min_hisse_ay']} hisse-ay.

## 6. KEŞİF: çoklu deneme muhasebesi ve seçim
- R1 ailesi (yaklaşık {m_r1} hipotez; ölçülemeyenler düşer): yönü belli sürekli sinyallerin ve bileşiklerin ÜST ucu, '?' sinyallerin iki ucu,
  bayrakların bayraklı grubu. p = iki yönlü p(t(alfa)). Benjamini-Hochberg, yanlış keşif oranı %{Ck['bh_q'] * 100:.0f}.
- R2 ailesi (yaklaşık {m_r2} hipotez): BÜTÜN sinyal ve bileşiklerin iki ucu (bayrakta bayraklı grup); çünkü beklenen yön ortalama getiri içindir,
  sağ kuyruk olasılığı için değil (piyango tipi hisselerde ikisi ters düşebilir). p = '+%100 lift > 1' p_z. BH %{Ck['bh_q'] * 100:.0f}.
- R2K ailesi (kaçınma; aynı satırlar): p = '-%50 lift > 1' p_z. BH %{Ck['bh_q'] * 100:.0f}.
- PLASEBO: {Ck['plasebo_n']} rastgele sinyal (her ay uygun hisselere rastgele sıra; numpy default_rng({Ck['plasebo_tohum']} + i)), ÜST uç, iki cetvelden de geçer.
  'Plasebo en büyüğü' = {Ck['plasebo_n']} plasebo istatistiğinden, ailenin hipotez sayısı kadar (yerine koyarak) çekilen kümenin en büyüğü; {Ck['maks_tekrar']} tekrar
  (tohum {Ck['maks_tohum']}); eşik = bu en büyüklerin %{Ck['maks_yuzde']:g}'lik dilimi. Plasebo istatistiği: R1'de BRÜT t(alfa) (artı yön için en büyüğü, eksi yön için
  -(brüt t)'nin en büyüğü), R2'de +%100 lift, R2K'de -%50 lift. Neden brüt: rastgele portföy her ay baştan kurulur (devir ~%180), net t'si
  maliyet yüzünden hep eksidir ve kıyas olmaz; 'bilgisiz ve maliyetsiz' portföyün t dağılımı (sıfır çevresinde) doğru kıyastır. Sinyalin
  kendisi artı yönde NET t(alfa)'sıyla bu eşiği aşmalıdır (daha sıkı); eksi yönde sinyalin BRÜT t'si kullanılır (tutulmayacak bir portföyün
  işlem maliyeti onun 'kötülüğü' sayılmaz).
  placebo.csv'de plasebo dağılımı ve eşikler yazılır. Cetvel sağlaması: plasebonun 'cetvel v2 TUTAR' oranı (net ya da brüt) > %{Ck['yp_esik'] * 100:.0f} ise
  R1 yolu KAPANIR (hüküm yok); plasebonun 'lift alt sınırı > 1' oranı > %{Ck['yp_esik'] * 100:.0f} ise raporda 'R2 aralığı dar' diye yazılır (seçim plasebo
  en büyüğü eşiğiyle zaten korunur).
- KEŞİF-SEÇİLİ ⇔ (R1 ARTI: BH'den geçer VE net t(alfa) > plasebo brüt t en büyüğü eşiği, YA DA net t(alfa) > {Ck['t_dogrudan']}) YA DA (R1 EKSİ: BH'den geçer VE
  -(brüt t(alfa)) > plasebo eşiği, YA DA brüt t(alfa) < -{Ck['t_dogrudan']}) YA DA (R2: BH'den geçer VE +%100 lift > plasebo eşiği) YA DA (R2K: BH'den geçer VE
  -%50 lift > plasebo eşiği). Seçim (sinyal, uç) çifti içindir; R1 yolunda yön (artı / eksi) secili.json'a yazılır.
- secili.json = seçilenler + eşikler + §8 model katsayıları; `dogrulama` ancak bu dosya git'e işlendikten sonra başlar.
- Nedeni yazılamayan sinyal (SALES_ACCEL, RUNWAY: proje ölçüsü; yayımlanmış kanıt yok) seçilse de 'şüpheli' işaretlenir (yol haritası §5 kural 6).

## 7. DOĞRULAMA, KASA ve etiketler
- DOĞRULAMA'ya girenler: KEŞİF-SEÇİLİ (sinyal, uç) çiftleri + BÜTÜN bileşiklerin iki ucu (seçilmemiş bileşik 'AİLE BİLGİSİ'dir, etiket alamaz).
- Geçme kuralları (dönemin kendi ayları; aynı uç = aynı yön):
  R1: net ortalama fazla > 0 VE alfa > 0 VE net t(alfa) > {Dg['t_tek_yon']} (24 ay kısa; önceden yazılı tek yönlü eşik) VE net t(alfa) > aynı dönemin {Ck['plasebo_n']}
      plasebosunun BRÜT t(alfa)'larının %{Dg['plasebo_yuzde']:g}'lik dilimi (kalibrasyon şartı: kısa dönemde NW t şişebilir). KEŞİF'te yönü EKSİ seçilen çiftte ayna kural BRÜT değerlerle: brüt fazla < 0
      VE brüt alfa < 0 VE brüt t(alfa) < -{Dg['t_tek_yon']} VE brüt t(alfa) < plasebo brüt t'lerinin %{100 - Dg['plasebo_yuzde']:g}'lik dilimi (bilgi).
  R2: +%100 lift %95 aralığının alt sınırı > 1 VE lift > aynı dönemin plasebo lift'lerinin %{Dg['plasebo_yuzde']:g}'lik dilimi.
  R2K: -%50 lift alt sınırı > 1 VE lift > plasebo -%50 lift'lerinin %{Dg['plasebo_yuzde']:g}'lik dilimi.
  DOĞRULAMA'dan GEÇER ⇔ R1 ya da R2 ya da R2K geçer. Geçenler dogrulama_gecen.json'a yazılır.
- KASA: yalnız DOĞRULAMA'dan geçenler; TEK AÇILIŞ (kasa_acildi.json işareti ölçümden önce yazılır; ikinci `kos --donem kasa` durur);
  geçme kuralları aynı. KASA ancak dogrulama_gecen.json git'e işlendikten sonra açılır.
- ETİKETLER (yalnız KEŞİF-SEÇİLİ çiftler):
  '{Et['iz']}' ⇔ KEŞİF'te R1 yolundan artı yönle seçildi VE DOĞRULAMA R1 geçti VE KASA R1 geçti.
  '{Et['olasilik']}' ⇔ KEŞİF'te R2 yolundan seçildi VE DOĞRULAMA R2 geçti VE KASA R2 geçti (+%100 olasılığını artırır).
  '{Et['kacinma']}' ⇔ üç döneme de girdi VE üçünde de -%50 lift alt sınırı > 1 (KEŞİF'te ayrıca R2K yolundan seçilmiş olmalı). Yalnız
      yaşayanlar evreninde batanlar yok: ölçülen -%50 olasılığı ve lift ALT SINIRDIR (gerçek kaçınma faydası daha büyük olabilir).
  '{Et['ters']}' ⇔ R1 yolundan eksi yönle seçildi ve iki dönemde de ayna kural tuttu (uç evrenin gerisinde kalıyor; kaçınma bilgisi).
  Hiçbiri İZ değildir (§0).

## 8. Birleşik olasılık modeli (BİLGİ; önceden yazıldı, ayar yok)
Lojistik regresyon, KEŞİF'te: hedef = F_{Md['ufuk']} >= +%100; girdiler = {len(Md['girdi'])} aile bileşiği ({', '.join(Md['girdi'])}; yüzdelik sıra ortalaması, eksik
değer {Md['eksik']:g}); gözlem = KEŞİF oluşum aylarındaki bütün uygun hisse-aylar. Kestirim: Newton (IRLS), en çok {Md['tur']} tur, sırt cezası {Md['ridge']:g}
(yalnız sayısal kararlılık). Katsayılar secili.json'da DONDURULUR; DOĞRULAMA ve KASA'da aynen uygulanır. Raporlanır: tahmin olasılığı
onluklarına göre kalibrasyon (tahmin ve gerçekleşen oran) ve aylık üst %{Pf['dilim'] * 100:.0f}'un +%100 lift'i (R2 ile aynı bootstrap). KEŞİF değerleri örneklem
içidir. Etiket ya da karar rolü yoktur.

## 9. Yanlılık beyanı
1. YALNIZ YAŞAYANLAR (EVREN_SECENEKLERI.md §4): batan / devralınan şirket yok. En çok etkilenenler: kaybeden olasılıkları (P(<= -%50) eksik
   ölçülür: gerçek -%100'ler yok), küçüklük, düşük fiyat, sıkıntı ve likidite aileleri (açıklık 'çok yüksek'); momentumun alım bacağı ve
   kârlılık / düşük ihraç 'düşük'. P(+%100) taban oranı yukarı yanlıdır (hayatta kalanlar). Geriye gidildikçe evren '16 yıl hayatta kalmış'
   şirketlere yaslanır (2012'de ~1.200, 2026'da ~2.700 uygun hisse).
2. Frames şirketin EN SON bildirdiği değeri verir (yeniden sunum sızıntısı); tarih gerçek ilk başvuru günüdür. Dizin eşlemesi dönem alanı
   olmadan yapılır (§3); geç başvuranlarda yedek kural geleceğe bakabilir (kapsam §12'de yedek payı yazılıdır).
3. XBRL kapsamı 2009-2011'de kademeli açılır (küçük şirketler 2011 ortasından sonra); temel sinyallerin KEŞİF'in ilk yıllarındaki kapsamı
   eksiktir (§12 'ilk ölçüm ayı').
4. Yahoo: kırpık geçmişli hisseler kural gereği dışarıda; düzeltme katsayıları indirme günündeki haliyledir; tekil hatalı gün temizliği yok.
5. AYKIRILAR TUTULUR (GME tipi): kırpma yok; seçilen her çift için en büyük üç katkı (R1: getiri katkısı; R2: +%100 olayı sayısı) yazılır.
6. CIK - borsa kodu eşlemesi ve SIC kodu bugünkü haliyledir.
7. Dönemler oluşum ayına göredir; KEŞİF'in son 11 oluşum ayının 12 aylık pencereleri 2022'ye, DOĞRULAMA'nınkiler 2024'e taşar: komşu
   dönemler tam bağımsız değildir.
8. Kalibre maliyet yalnız {R1['maliyet'] * 1e4:.0f} bp / yön; küçük hisselerde gerçek alış-satış farkı daha büyüktür (SPREAD_CS bilgi verir).

## 10. Çıktılar (arastirma_cikti/k60_kutuphane/)
kapsam.csv, kapsam_ozet.json; kesif_r1.csv, kesif_r2.csv, kesif_aylik.csv (R1 aylık getiriler), kesif_r2_aylik.csv (R2 aylık sayımlar: her
sayı buradan yeniden üretilebilir), placebo.csv, secili.json (git'e işlenir), kesif_meta.json; dogrulama_r1.csv, dogrulama_r2.csv,
dogrulama_aylik.csv, dogrulama_r2_aylik.csv, dogrulama_gecen.json (git'e işlenir), dogrulama_meta.json; kasa_r1.csv, kasa_r2.csv,
kasa_aylik.csv, kasa_r2_aylik.csv, kasa_acildi.json, kasa_meta.json; model_kalibrasyon.csv; olasilik_tablosu.md (ana, okunur sonuç: seçilmiş
her çift için dönem dönem taban oran, P(+%100), lift ve aralığı, aynısı -%50 için); K60_RAPOR.md.

## 11. BOŞLUK listesi (iş tanımında açık bırakılan ya da veriden ötürü doldurulan yerler; hepsi ölçümden önce yazıldı)
BOŞLUK 1. KEŞİF başlangıcı: yol haritası §5 '2016' diyordu; iş tanımı {Dn['kesif'][0]} (XBRL kapsamı 2011Q2'den tam; 120 ay). {Dn['kesif'][0]} uygulanır.
BOŞLUK 2. Bilgi tarihi eşlemesi (§3): dizinde dönem alanı yok; 'mali yıl sonu çeyreği -> 10-K ailesi, öteki -> 10-Q ailesi, çeyrek sonundan en az
  {Bg['en_az_gun']} gün sonraki ilk başvuru' kuralı. Hiç eşleşmeyenlerde iş tanımındaki yedek (+{Bg['yedek_ceyrek_gun']} / +{Bg['yedek_yil_gun']} gün). Eşleşen başvuru çok geç ise (halka arz öncesi
  dönemler, form türü farklı şirketler) bilgi tarihi geç kalır: tutucu yöndedir (veri bayatlar, geleceğe bakılmaz).
BOŞLUK 3. R1 'aynen K59': giriş ay sonu kapanışıdır (envanterdeki 'sonraki ayın ilk günü açılışı' kuralı yerine K59 cetveli); 1 ay getirisi
  K58 gibi sınırsız ileri taşımalı son fiyattan, R2 getirisi m+h ay sonunda taze fiyat şartıyla hesaplanır.
BOŞLUK 4. R1 istatistiği: iş tanımı KEŞİF'te 'alfa t', DOĞRULAMA'da 'fazla > 0, t > 1,65' diyor; ikisinde de t(alfa) kullanılır ve
  DOĞRULAMA / KASA'da ayrıca net fazla > 0 ve alfa > 0 istenir (daha sıkı okuma) + plasebo kalibrasyon şartı (§7; ek, sıkılaştırır).
BOŞLUK 5. R2 p değeri: {R2['cekilis']} çekilişte yüzdelik p en az 1/{R2['cekilis'] + 1}'dir; ~{m_r2} hipotezli BH'de birinci sıra eşiği bundan küçüktür. Bu yüzden BH'ye
  giren p, bootstrap standart hatasıyla normal yaklaşımdır (p_z); yüzdelik p ayrıca raporlanır.
BOŞLUK 6. R2 ailesinde iki uç birden test edilir (2 hipotez / sinyal); kaçınma için ayrı BH ailesi (R2K) ve ayrı plasebo eşiği vardır;
  yoksa yalnız kaybeden olasılığını artıran bir özellik DOĞRULAMA'ya giremezdi.
BOŞLUK 7. 'Plasebo en büyüğünün %95'i': {Ck['plasebo_n']} plasebodan hipotez sayısı kadar yerine koyarak çekilen kümelerin en büyüğünün dağılımı (§6). Pratikte
  eşik {Ck['plasebo_n']} plasebonun en büyüğüne yakındır.
BOŞLUK 8. '|t| > {Ck['t_dogrudan']}' yalnız R1 t(alfa) içindir (artı yönde net, eksi yönde brüt t); eksi yönle seçilen çift '{Et['ters']}' adayıdır,
  '{Et['iz']}' olamaz. BH'ye giren p her iki yön için de net t(alfa)'nın iki yönlü p'sidir.
BOŞLUK 9. Bayrak (0 / 1) sinyallerde onluk kurulamaz: portföy = bayraklı uygun hisselerin tamamı (ay başına en az {Pf['min_bayrak']}); beklenen yön '+' ise ÜST,
  '-' ise ALT uç sayılır; karşı uç kurulmaz. Ara verilen aylardan sonra devir, tutulan son ağırlıklara göre hesaplanır (maliyet hafif eksik).
BOŞLUK 10. Eşitlik bozma: aynı değerli hisseler arasında onluk sınırı sabit tohumlu rastgele sırayla bozulur (default_rng({Pf['bag_tohum']}); bütün sinyaller
  aynı sıra matrisini kullanır). Eşitliği olmayan sinyalde sonuç K59 (kod sırası) ile aynıdır.
BOŞLUK 11. Bileşik kuralları (§1): en az üye = ailenin sürekli üye sayısının yarısı (yukarı yuvarlanmış; iki üyeli ailede 1: bileşim zamanla değişebilir); COMP4 ve DOSYA_Y'de K59'daki S4 yerine EAR_ANN
  (K60'ta Nasdaq takvimi yok), S6 yerine NSI_1Y (K60 pay tanımı), X1 yerine REV_YOY.
BOŞLUK 12. Açıklama günü: 8-K madde kodu (2.02) inmedi; EAR_ANN, EAR_VOL, EA_MONTH için gün VEKİLİ kullanılır (§1 tanım); EAR_FILE aynı
  ölçünün başvuru günü sürümüdür. İkisi de EAR ailesinde ayrı hipotez sayılır.
BOŞLUK 13. Yaklaşık tanımlar (etiket eksikliği / yalnız yıllık nakit akışı yüzünden; §1'de yazılı): EV_EBITDA (kısa vadeli borç yok), NOA, OPLEV
  (SG&A yerine gelir - faaliyet kârı), NDF_BS (bilanço farkı), CBOP_A (OCF / varlık), RUNWAY (yıllık OCF; sürekli ölçü), ACCRUALS / CFP / NEF /
  BUYBACK_YLD / NET_PAYOUT_YLD / CAPEX_G / F_SCORE / O_SCORE yıllık, O_SCORE'da FFO yerine OCF ve fiyat düzeyi düzeltmesi yok (ay içi sıra
  değişmez), CHS_FAIL'de çeyrek kârları bugünkü (t) piyasa değerli toplam varlığa bölünür, RSIZE paydası uygun evrenin toplam PD'si, BETA_BAB
  günlük basit getiriyle ve 1'e büzme yapılmadan, TREND_MA 200 güne kadar gecikmelerle, MOM_FIP çift sıralama yerine sıra ortalaması,
  VOL_SHOCK ikili yerine sürekli oran, IVOL / ISKEW için French GÜNLÜK 3 faktör dosyası (11 Kasım'da indirildi; sha256 yukarıda).
BOŞLUK 14. Bu turda ölçülemeyen üç envanter satırı (TAXLOSS_JAN, E_LOCKUP, E_MA_TARGET) ve DALGA 2 listesi §1'de.
BOŞLUK 15. KASA'da 12 ay ufuklu R2 yalnız ~20 oluşum ayıdır; blok bootstrap dairesel olduğu için hesaplanır ama aralık güvenilirliği düşüktür
  (plasebo dilim şartı bunun için). Tek açılış işareti silinmez; çökme olursa yeniden açma kararı ana oturumundur ve raporda yazılır.
BOŞLUK 16. KASA'nın ön şartı olarak dogrulama_gecen.json'ın da git'e işlenmiş olması istenir (iş tanımında yalnız secili.json vardı; ek).
BOŞLUK 17. Kapalı konulara komşu sinyaller (EAR_VOL, VOL_SHOCK: 'hacim'; IND_MOM_6, IND_LEAD_BIG: 'sektör ısısı'; TREND_MA: 'şekil') çöl giriş
  zamanlaması değil, portföy düzeyi literatür faktörleri olarak kütüphanededir (iş tanımı: envanterin hesaplanabilen bütün satırları).
BOŞLUK 18. Lojistik modelde eksik bileşik {Md['eksik']:g} (nötr sıra) ile doldurulur; kalibrasyon onlukları dönem havuzunda eşit sayılıdır.
BOŞLUK 19. Ortalama ve medyan F, hisse-ay havuzundadır (ay ortalaması değil).
BOŞLUK 20. KEŞİF yeniden koşulursa secili.json bayt bayt aynı çıkmalıdır; değilse koşu durur ve dosyaya dokunulmaz.
BOŞLUK 21. Plasebo kıyas istatistiği R1'de BRÜT t(alfa)'dır (§6 gerekçe); sinyal artı yönde NET t'siyle sınanır. İş tanımındaki 'plasebo en büyük
  |t|'si iki yöne ayrıldı (artı: en büyük brüt t; eksi: en büyük -(brüt t)).
BOŞLUK 22. Bayrak alt sınırı (ay başına bayraklı hisse) kapsam sayımından SONRA, yalnız SAYILARA bakılarak {Pf['min_bayrak']} olarak sabitlendi (ilk taslakta 20 idi:
  NT_LATE, E_SPLIT, E_RSPLIT, E_DIV_INIT KEŞİF'te 36 aya ulaşamıyordu). Hiçbir getiri ya da olasılık görülmedi. E_TENDER_SELF yine de ölçülemez
  (ayda ~4 hisse): tabloda 'ölçülemedi' çıkar.
BOŞLUK 23. Veri temizliği yalnız şudur: Yahoo düzeltilmiş kapanışı <= 0 olan günler yok sayılır (sayımda görüldü: getiri tanımsız / sonsuz).
  Başka kırpma, uç değer atma ya da hatalı gün düzeltmesi YOK; uçlar raporda sayılır (ay getirisi > +%300, 12 ay getirisi > +%1000).
BOŞLUK 24. Her koşunun meta dosyasına K60.py'nin sha256'sı ve kütüphane sürümleri yazılır; KEŞİF'ten sonra kod değişirse DOĞRULAMA / KASA
  meta dosyasına ve rapora not düşer (koşu durmaz: hata düzeltmesi gerekebilir; değişikliği ana oturum denetler).
BOŞLUK 25. SIC kodu yalnız islenmis-veri k35 tablosundaki şirketlerde var (kapsam §12); SEC ailesi yalnız bu hisselerde ölçülür.

## 12. Kapsam (yalnız sayım; mühre girmez)
{kapsam}

## 13. Değişmezlik ve komut sırası
Yukarıdaki bütün eşikler, tanımlar, dönemler ve karar kuralları sabittir; sonuç görüldükten sonra değiştirilmez. Kod hatası düzeltmesi
gerekirse ön kayıt değişmez, düzeltme raporda ayrıca yazılır.
1. (ana oturum) bu dosyayı denetler ve git'e işler.
2. `cd /home/user/col_yolu && python -I K60.py kos --donem kesif`  -> kesif_*.csv, placebo.csv, secili.json
3. (ana oturum) secili.json'ı denetler ve git'e işler.
4. `python -I K60.py kos --donem dogrulama`  -> dogrulama_*.csv, dogrulama_gecen.json
5. (ana oturum) dogrulama_gecen.json'ı denetler ve git'e işler.
6. `python -I K60.py kos --donem kasa`  (TEK AÇILIŞ) -> kasa_*.csv
7. `python K60.py rapor`  -> olasilik_tablosu.md, K60_RAPOR.md
"""


def _k60_onkayit_oku(yol: str) -> Dict[str, Any]:
    with open(yol, encoding="utf-8") as f:
        metin = f.read()
    m = re.search(r"^ESIK_SHA256: ([0-9a-f]{64})$", metin, re.M)
    z = re.search(r"^Yazım zamanı: (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC", metin, re.M)
    veri = {a: (h, int(n)) for a, h, n in re.findall(r"^- ([\w.\-]+): sha256 ([0-9a-f]{64}) \((\d+) dosya\)$", metin, re.M)}
    return {"sha": m.group(1) if m else None, "zaman_utc": z.group(1) if z else "", "veri": veri}


def k60_onkayit(cikti: Optional[str] = None, veri_sha: Optional[Dict[str, Tuple[str, int]]] = None) -> str:
    """Ön kaydı yazar. Dosya varsa ÜZERİNE YAZMAZ: mühür aynıysa yolu döndürür, değilse durur. veri_sha None ise veri özetleri hesaplanır
    (önbellek eksikse durur)."""
    yol = _k60_yol("onkayit", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True)
    if os.path.exists(yol):
        mevcut = _k60_onkayit_oku(yol)["sha"]
        if mevcut != k60_esik_sha():
            raise K60Hata(f"ön kayıt zaten var ve mühür farklı ({mevcut} != {k60_esik_sha()}): eşikler ön kayıttan sonra değişmiş")
        k60log.info("ön kayıt zaten var (mühür aynı): %s", yol)
        return yol
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    metin = k60_onkayit_metin(zaman, k60_veri_sha() if veri_sha is None else veri_sha, k60_kapsam_notu(cikti))
    if _K60_EPOSTA.search(metin):
        raise K60Hata("ön kayıt metninde e-posta biçimli parça var; yazılmadı")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k60log.info("ön kayıt yazıldı: %s (mühür %s)", yol, k60_esik_sha()[:12])
    return yol


def _k60_git_islenmis(yol: str, ne: str) -> Dict[str, str]:
    """Dosya git'e işlenmiş ve işlendikten sonra değişmemiş olmalı (denetim sırası: git zamanı + içerik)."""
    kl, ad = os.path.dirname(os.path.abspath(yol)), os.path.basename(yol)
    try:
        r = subprocess.run(["git", "-C", kl, "log", "-1", "--format=%H %cI", "--", ad], capture_output=True, text=True, timeout=60)
        d = subprocess.run(["git", "-C", kl, "status", "--porcelain", "--", ad], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as ex:
        raise K60Hata(f"git çalıştırılamadı ({ex}): {ne} dosyasının işlendiği doğrulanamadı, koşu durdu")
    if r.returncode != 0 or not r.stdout.strip():
        raise K60Hata(f"{ne} git'e işlenmemiş ({yol}): önce ana oturum denetleyip commit eder")
    if d.returncode != 0 or d.stdout.strip():
        raise K60Hata(f"{ne} git'e işlendikten sonra değişmiş ({d.stdout.strip() or d.stderr.strip()}): koşu durdu")
    h, z = r.stdout.strip().split(" ", 1)
    return {"commit": h, "commit_zamani": z}


def k60_onkayit_dogrula(cikti: Optional[str] = None, veri: bool = False, git: bool = False) -> Dict[str, Any]:
    """Mühür (her zaman), veri sha256'ları (veri=True) ve git'e işlenmişlik (git=True) doğrulanır; biri tutmazsa K60Hata."""
    yol = _k60_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise K60Hata(f"ön kayıt yok ({yol}): önce `python K60.py onkayit`")
    oc = _k60_onkayit_oku(yol)
    if oc["sha"] != k60_esik_sha():
        raise K60Hata(f"ön kayıt mührü tutmuyor ({oc['sha']} != {k60_esik_sha()}): eşikler ön kayıttan sonra değişmiş, koşu durdu")
    out = {"yol": yol, "sha": oc["sha"], "zaman_utc": oc["zaman_utc"], "dosya_sha256": _k60_sha(yol), "veri": oc["veri"]}
    if veri:
        simdi = k60_veri_sha()
        fark = sorted(k for k in set(simdi) | set(oc["veri"]) if simdi.get(k) != oc["veri"].get(k))
        if fark:
            raise K60Hata(f"veri ön kayıttakiyle aynı değil (sha256 / dosya sayısı farklı ya da eksik): {fark}; koşu durdu")
    if git:
        out["git"] = _k60_git_islenmis(yol, "ön kayıt")
    return out


def _k60_meta_yol(donem: str, cikti: Optional[str]) -> str:
    return _k60_yol(f"{donem}_meta.json", cikti)


def _k60_meta_bitti(donem: str, cikti: Optional[str]) -> Optional[Dict[str, Any]]:
    y = _k60_meta_yol(donem, cikti)
    if not os.path.exists(y):
        return None
    try:
        m = _k60_json_oku(y)
    except (OSError, ValueError):
        return None
    return m if m.get("kos_bitis") else None


def k60_sira_denetle(donem: str, cikti: Optional[str] = None, git_sart: bool = True) -> Dict[str, Any]:
    """DÖNEM SIRASI: dogrulama yalnız kesif çıktıları varsa ve secili.json git'e işlenmişse; kasa yalnız dogrulama çıktıları varsa,
    dogrulama_gecen.json git'e işlenmişse ve daha önce AÇILMAMIŞSA. Döner: önceki dönemlerin meta bilgisi."""
    if donem not in K60_DONEM:
        raise K60Hata(f"bilinmeyen dönem: {donem} (kesif | dogrulama | kasa)")
    out: Dict[str, Any] = {}
    if donem == "kesif":
        if os.path.exists(_k60_yol("kasa_isaret", cikti)):
            raise K60Hata("KASA açılmış: KEŞİF yeniden koşulamaz (dönem sırası)")
        return out
    mk = _k60_meta_bitti("kesif", cikti); ys = _k60_yol("secili", cikti)
    eksik = [a for a in ("kesif_r1.csv", "kesif_r2.csv", K60_DOSYA["plasebo"], K60_DOSYA["secili"]) if not os.path.exists(_k60_yol(a, cikti))]
    if mk is None or eksik:
        raise K60Hata(f"{K60_DONEM_AD[donem]} başlamaz: KEŞİF çıktıları yok / koşu bitmemiş (eksik: {eksik or 'kesif_meta.json'})")
    if _k60_sha(ys) != mk.get("secili_sha256"):
        raise K60Hata("secili.json KEŞİF koşusunun yazdığıyla aynı değil (sha256 farklı): koşu durdu")
    if mk.get("onkayit", {}).get("sha") != k60_esik_sha():
        raise K60Hata("KEŞİF başka bir mühürle koşulmuş: koşu durdu")
    out["kesif"] = mk; out["secili"] = _k60_json_oku(ys)
    if git_sart:
        out["secili_git"] = _k60_git_islenmis(ys, "secili.json (KEŞİF-SEÇİLİ listesi)")
    if donem == "dogrulama":
        if os.path.exists(_k60_yol("kasa_isaret", cikti)):
            raise K60Hata("KASA açılmış: DOĞRULAMA yeniden koşulamaz (dönem sırası)")
        return out
    md = _k60_meta_bitti("dogrulama", cikti); yg = _k60_yol("gecen", cikti)
    eksik = [a for a in ("dogrulama_r1.csv", "dogrulama_r2.csv", K60_DOSYA["gecen"]) if not os.path.exists(_k60_yol(a, cikti))]
    if md is None or eksik:
        raise K60Hata(f"KASA açılmaz: DOĞRULAMA çıktıları yok / koşu bitmemiş (eksik: {eksik or 'dogrulama_meta.json'})")
    if _k60_sha(yg) != md.get("gecen_sha256") or md.get("secili_sha256") != mk.get("secili_sha256"):
        raise K60Hata("dogrulama_gecen.json DOĞRULAMA koşusunun yazdığıyla aynı değil / DOĞRULAMA başka secili.json ile koşulmuş: koşu durdu")
    if os.path.exists(_k60_yol("kasa_isaret", cikti)):
        raise K60Hata("KASA daha önce AÇILDI (kasa_acildi.json var): tek açılış kuralı, ikinci koşu yok")
    out["dogrulama"] = md; out["gecen"] = _k60_json_oku(yg)
    if git_sart:
        out["gecen_git"] = _k60_git_islenmis(yg, "dogrulama_gecen.json")
    return out


# ---------------------------------------------------------------- 2) VERİ DEMETİ (gerçek veri; yalnız önbellek okunur, ağ yok)
def k60_fiyat_oku(yol: str, kes: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], str]:
    """Yahoo önbellek JSON'u -> günlük dizi sözlüğü: gun (datetime64[D]), o, h, l, c (bölünme düzeltmeli), a (temettü de düzeltilmiş), v,
    bolunme ((tarih ns, oran) ya da None), temettu (hak düşüm günleri), tur, ilk_islem, kirpik. Temizlik ve 'kırpık' kuralı K60_veri
    k60v_yahoo_oku ile AYNI (OHLC dolu, High >= Low, Close > 0, kes sonrası atılır); döner (None, neden) da aynı."""
    try:
        with open(yol, encoding="utf-8") as f:
            J = json.load(f)
    except (OSError, ValueError) as ex:
        return None, f"okunamadı ({type(ex).__name__})"
    if not isinstance(J, dict):
        return None, "okunamadı (biçim)"
    if "yok" in J:
        return None, "yok"
    res = ((J.get("chart") or {}).get("result") or [None])[0]
    if not res or not res.get("timestamp"):
        return None, "veri yok"
    meta = res.get("meta") or {}; tz = meta.get("exchangeTimezoneName") or "America/New_York"; Y = KV.K60V_ESIK["yahoo"]

    def gun(ts: Any) -> pd.DatetimeIndex:
        return pd.to_datetime(ts, unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()
    ilk = meta.get("firstTradeDate"); ilk_islem = gun([int(ilk)])[0] if isinstance(ilk, (int, float)) else pd.NaT
    beklenen = max(ilk_islem, pd.Timestamp(Y["bas"])) if pd.notna(ilk_islem) else pd.Timestamp(Y["bas"])
    kirpik = bool((gun([res["timestamp"][0]])[0] - beklenen).days > int(Y["kirpik_gun"]))
    q = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    try:
        d = pd.DataFrame({"o": q.get("open"), "h": q.get("high"), "l": q.get("low"), "c": q.get("close"), "v": q.get("volume")},
                         index=gun(res["timestamp"]), dtype=float)
    except (ValueError, TypeError):
        return None, "okunamadı (seri boyu)"
    adj = (((res.get("indicators") or {}).get("adjclose") or [{}])[0] or {}).get("adjclose")
    d["a"] = np.asarray(pd.Series(adj, dtype=float), float) if adj is not None and len(adj) == len(d) else d.c.to_numpy(float)
    d = d[~d.index.duplicated(keep="last")].dropna(subset=["o", "h", "l", "c"]).sort_index()
    d = d[(d.h >= d.l) & (d.c > 0)]
    if kes is not None:
        d = d[d.index <= pd.Timestamp(kes)]
    if not len(d):
        return None, "veri yok (kırpık)" if kirpik else "veri yok"
    olay = res.get("events") or {}; bol = []; tem = []
    for v in (olay.get("splits") or {}).values():
        try:
            pay, payda, t = float(v["numerator"]), float(v["denominator"]), int(v["date"])
        except (KeyError, TypeError, ValueError):
            continue
        if pay > 0 and payda > 0 and pay != payda:
            bol.append((gun([t])[0].to_datetime64().astype("datetime64[ns]"), pay / payda))
    for v in (olay.get("dividends") or {}).values():
        try:
            if float(v.get("amount", 0.0)) > 0:
                tem.append(gun([int(v["date"])])[0].to_datetime64().astype("datetime64[D]"))
        except (KeyError, TypeError, ValueError, AttributeError):
            continue
    bol.sort(key=lambda x: x[0])
    return {"gun": d.index.to_numpy("datetime64[D]"), "o": d.o.to_numpy(float), "h": d.h.to_numpy(float), "l": d.l.to_numpy(float),
            "c": d.c.to_numpy(float), "a": d.a.to_numpy(float), "v": d.v.fillna(0.0).to_numpy(float),
            "bolunme": (np.array([x[0] for x in bol], "datetime64[ns]"), np.array([x[1] for x in bol], float)) if bol else None,
            "temettu": np.sort(np.array(tem, "datetime64[D]")), "tur": meta.get("instrumentType"),
            "ilk_islem": ilk_islem.to_datetime64().astype("datetime64[D]") if pd.notna(ilk_islem) else np.datetime64("NaT", "D"), "kirpik": kirpik}, "fiyat"


def k60_french_gunluk(yol: Optional[str] = None) -> pd.DataFrame:
    """French günlük 3 faktör dosyası -> DataFrame (gün; MKT_RF, SMB, HML, RF; ondalık). Dosya yoksa K60Hata (indirme yapılmaz)."""
    yol = yol or os.path.join(K60_YOL["french_gunluk"], K60_ESIK["veri"]["french_gunluk"])
    if not os.path.exists(yol) or not zipfile.is_zipfile(yol):
        raise K60Hata(f"French günlük faktör dosyası yok / zip değil: {yol}")
    with zipfile.ZipFile(yol) as z:
        metin = z.read(z.namelist()[0]).decode("latin-1")
    sat = []
    for s in metin.splitlines():
        p = [x.strip() for x in s.split(",")]
        if len(p) == 5 and re.fullmatch(r"\d{8}", p[0]):
            try:
                sat.append((p[0], float(p[1]), float(p[2]), float(p[3]), float(p[4])))
            except ValueError:
                continue
    if not sat:
        raise K60Hata(f"French günlük dosyasında veri satırı yok: {yol}")
    F = pd.DataFrame(sat, columns=["gun", "MKT_RF", "SMB", "HML", "RF"])
    F.index = pd.to_datetime(F.pop("gun"), format="%Y%m%d")
    F = F.where(F > -99.0) / 100.0
    return F[~F.index.duplicated(keep="last")].sort_index()


def k60_dizin_oku(ciks: set, E: Optional[Dict[str, Any]] = None, satirlar: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Dict[str, np.ndarray]]:
    """EDGAR master dizinleri -> {grup: {cik: sıralı başvuru günleri (datetime64[D])}}. Gruplar: K (yıllık), Q (çeyreklik), 8K, NT, S3, 424B5,
    13D, TOI. Yalnız verilen CIK'ler; düzeltme (/A) başvuruları form adı farklı olduğu için girmez."""
    import gzip
    import io
    Bg = (E or K60_ESIK)["bilgi"]
    grup = {"K": Bg["form_yil"], "Q": Bg["form_ceyrek"], "8K": Bg["form_8k"], "NT": Bg["form_nt"], "S3": Bg["form_s3"], "424B5": Bg["form_424b5"],
            "13D": Bg["form_13d"], "TOI": Bg["form_toi"]}
    f2g = {f: g for g, fl in grup.items() for f in fl}
    if satirlar is None:
        satirlar = [r for r in k60_frame_yollari()[0] if r["tur"] == "dizin"]
    par = []
    for r in satirlar:
        with open(r["yol"], "rb") as f:
            ham = f.read()
        if ham[:2] == b"\x1f\x8b":
            ham = gzip.decompress(ham)
        d = pd.read_csv(io.BytesIO(ham), sep="|", header=None, names=["cik", "ad", "form", "gun", "dosya"], usecols=["cik", "form", "gun"], dtype=str,
                        encoding="latin-1", quoting=3, on_bad_lines="skip", engine="c")
        d = d[d.form.isin(f2g) & d.cik.isin(ciks)]
        if len(d):
            par.append(d)
    out: Dict[str, Dict[str, np.ndarray]] = {g: {} for g in grup}
    if not par:
        return out
    T = pd.concat(par, ignore_index=True)
    T["g"] = T.form.map(f2g); T["t"] = pd.to_datetime(T.gun, errors="coerce")
    T = T.dropna(subset=["t"])
    for (g, c), x in T.groupby(["g", "cik"], sort=False):
        out[g][c] = np.unique(x.t.to_numpy("datetime64[D]"))
    return out


def _k60_ceyrek_sira(t: np.ndarray) -> np.ndarray:
    """Dönem sonu (datetime64[D]) -> takvim çeyreği sırası (yıl * 4 + çeyrek - 1); K57 _k57_ceyrek_sira kuralı (bitişten 45 gün önceki günün
    çeyreği). NaT -> -10**6."""
    t = np.asarray(t, "datetime64[D]"); ok = ~np.isnat(t)
    ay = (np.where(ok, t, np.datetime64("2000-01-01")) - np.timedelta64(45, "D")).astype("datetime64[M]").astype(np.int64)
    return np.where(ok, (1970 + ay // 12) * 4 + (ay % 12) // 3, -10 ** 6)


_K60_PAY_ETIKET = ("EntityCommonStockSharesOutstanding", "CommonStockSharesOutstanding", "WeightedAverageNumberOfDilutedSharesOutstanding")


def k60_temel_yukle(cik: List[Optional[str]], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """SEC frames önbelleği -> HAM temel tablo (hisse sütunlu diziler): Q (çeyreklik süreli), I (çeyrek sonu anlık), Y (yıllık), bit / Ybit / Ybas
    (dönem sonu / başı), pay_ham (kapak pay sayısı kayıtları). 4. çeyrek türetme ve bilgi tarihleri k60_temel_tamamla'da."""
    E = E or K60_ESIK; V = E["veri"]; N = len(cik)
    qb, qs = pd.Period(V["ceyrek_bas"], "Q"), pd.Period(V["ceyrek_son"], "Q")
    q_bas = qb.year * 4 + qb.quarter - 1; nq = (qs.year * 4 + qs.quarter - 1) - q_bas + 1; y_bas = int(V["yil_bas"]); ny = int(V["yil_son"]) - y_bas + 1
    kol: Dict[int, List[int]] = {}
    for j, c in enumerate(cik):
        if c is not None:
            kol.setdefault(int(c), []).append(j)
    nat = np.datetime64("NaT", "D")
    T: Dict[str, Any] = {"q_bas": q_bas, "y_bas": y_bas, "Q": {}, "I": {}, "Y": {}, "bit": np.full((nq, N), nat), "Ybit": np.full((ny, N), nat),
                         "Ybas": np.full((ny, N), nat), "pay_ham": [[] for _ in range(N)]}
    sat, eksik = k60_frame_yollari()
    if eksik:
        raise K60Hata(f"SEC önbelleği eksik: {len(eksik)} dosya (ör. {eksik[:3]})")
    for r in sat:
        if r["tur"] == "dizin":
            continue
        try:
            with open(r["yol"], encoding="utf-8") as f:
                veri = (json.load(f) or {}).get("data") or []
        except (OSError, ValueError) as ex:
            raise K60Hata(f"SEC çerçevesi okunamadı: {r['yol']} ({type(ex).__name__})")
        js: List[int] = []; vals: List[float] = []; son: List[str] = []; bas: List[str] = []
        for d in veri:
            c = kol.get(d.get("cik"))
            if c is None or d.get("val") is None or not d.get("end"):
                continue
            for j in c:
                js.append(j); vals.append(float(d["val"])); son.append(d["end"]); bas.append(d.get("start") or d["end"])
        if not js:
            continue
        ja = np.array(js); va = np.array(vals, float); sa = np.array(son, "datetime64[D]"); etiket, donem = r["etiket"], r["donem"]
        if etiket == _K60_PAY_ETIKET[0]:
            for j, t_, v_ in zip(js, sa, va):
                T["pay_ham"][j].append((t_, v_))
            continue
        dt = KV._k60v_donem_turu(donem)
        if dt == "yil":
            y = int(donem[2:6]) - y_bas
            if not 0 <= y < ny:
                continue
            T["Y"].setdefault(etiket, np.full((ny, N), np.nan))[y, ja] = va
            bos = np.isnat(T["Ybit"][y, ja])
            T["Ybit"][y, ja[bos]] = sa[bos]; T["Ybas"][y, ja[bos]] = np.array(bas, "datetime64[D]")[bos]
        else:
            q = K57._k57_etiket(donem) - q_bas
            if not 0 <= q < nq:
                continue
            T["I" if dt == "an" else "Q"].setdefault(etiket, np.full((nq, N), np.nan))[q, ja] = va
            if etiket not in _K60_PAY_ETIKET:
                bos = np.isnat(T["bit"][q, ja]); T["bit"][q, ja[bos]] = sa[bos]
    return T


def k60_temel_tamamla(T: Dict[str, Any], K_gun: List[Optional[np.ndarray]], Q_gun: List[Optional[np.ndarray]],
                      E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ham temel tabloyu tamamlar (yerinde): (1) yıllıktan 4. çeyrek türetme; (2) mali yıl sonu çeyreği bayrağı; (3) BİLGİ TARİHİ: çeyrek /
    mali yıl sonundan en az en_az_gun gün SONRAKİ ilk 10-K ailesi (mali yıl sonu) ya da 10-Q ailesi (öteki çeyrek) başvurusu, yoksa yedek kural; (4) kapak pay
    sayısı kayıtlarının bilgi tarihi. K_gun / Q_gun: hisse başına sıralı başvuru günleri (datetime64[D]) ya da None."""
    Bg = (E or K60_ESIK)["bilgi"]; bit, Ybit, Ybas = T["bit"], T["Ybit"], T["Ybas"]; nq, N = bit.shape; ny = Ybit.shape[0]; q_bas = T["q_bas"]
    gD = lambda n: np.timedelta64(int(n), "D")  # noqa: E731
    Yq = _k60_ceyrek_sira(Ybit) - q_bas
    Yq = np.where((Yq >= 0) & (Yq < nq), Yq, -1)
    with np.errstate(invalid="ignore"):
        sure = (Ybit - Ybas).astype("timedelta64[D]").astype(float) + 1
    sure_ok = (sure >= Bg["yil_sure"][0]) & (sure <= Bg["yil_sure"][1]) & ~np.isnat(Ybit) & ~np.isnat(Ybas)
    turetilen = 0; sutun = np.arange(N)
    for etiket, Ya in T["Y"].items():
        if etiket in _K60_PAY_ETIKET or etiket not in T["Q"]:
            continue
        Qa = T["Q"][etiket]
        for y in range(ny):
            m = (Yq[y] >= 3) & sure_ok[y] & np.isfinite(Ya[y])
            if not m.any():
                continue
            c = sutun[m]; qy = Yq[y, c]
            once = Qa[qy - 1, c] + Qa[qy - 2, c] + Qa[qy - 3, c]
            mm = np.isfinite(once) & ~np.isfinite(Qa[qy, c])
            if mm.any():
                Qa[qy[mm], c[mm]] = Ya[y, c[mm]] - once[mm]; turetilen += int(mm.sum())
                bos = np.isnat(bit[qy[mm], c[mm]]); bit[qy[mm][bos], c[mm][bos]] = Ybit[y, c[mm][bos]]
    tol = gD(Bg["mali_yil_tol_gun"]); mali = np.zeros((nq, N), bool)
    with np.errstate(invalid="ignore"):
        for y in range(ny):
            mali |= np.abs(bit - Ybit[y][None, :]) <= tol
    yillik_var = (~np.isnat(Ybit)).any(axis=0)
    nat = np.datetime64("NaT", "D")
    bilgi = np.full((nq, N), nat); Ybilgi = np.full((ny, N), nat); kay = np.zeros((nq, N), np.int8); ykay = np.zeros((ny, N), np.int8); pay: List[Any] = [None] * N
    bos_dizi = np.array([], "datetime64[D]")

    def ilk_sonra(lst: np.ndarray, b: np.ndarray, yedek: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Her b için lst'te b + en_az_gun ve sonrasındaki ilk gün; yoksa yedek. Döner (gün, kaynak 1 = dizin / 2 = yedek). En az gün şartı: dönem
        sonundan hemen sonra gelen başvuru, geciken ÖNCEKİ dönemin başvurusudur; yeni döneme yazılırsa geleceğe bakılmış olur."""
        i = np.searchsorted(lst, b + gD(Bg["en_az_gun"]), side="left"); var = i < len(lst)
        return np.where(var, lst[np.minimum(i, max(len(lst) - 1, 0))] if len(lst) else yedek, yedek), np.where(var, 1, 2).astype(np.int8)
    for j in range(N):
        Kd = K_gun[j] if K_gun[j] is not None else bos_dizi; Qd = Q_gun[j] if Q_gun[j] is not None else bos_dizi
        hepsi = np.union1d(Kd, Qd)
        b = bit[:, j]; var = ~np.isnat(b)
        if var.any():
            bb = b[var]; ml = mali[var, j]
            gk, kk = ilk_sonra(Kd if yillik_var[j] else hepsi, bb, bb + gD(Bg["yedek_yil_gun"]))
            gq, kq = ilk_sonra(Qd if yillik_var[j] else hepsi, bb, bb + gD(Bg["yedek_ceyrek_gun"]))
            bilgi[var, j] = np.where(ml, gk, gq); kay[var, j] = np.where(ml, kk, kq)
        yb = Ybit[:, j]; yv = ~np.isnat(yb)
        if yv.any():
            g_, k_ = ilk_sonra(Kd, yb[yv], yb[yv] + gD(Bg["yedek_yil_gun"])); Ybilgi[yv, j] = g_; ykay[yv, j] = k_
        ham = T.get("pay_ham", [[]] * N)[j] if T.get("pay_ham") is not None else []
        if ham:
            d = np.array([x[0] for x in ham], "datetime64[D]"); n_ = np.array([x[1] for x in ham], float)
            s = np.argsort(d, kind="stable"); d, n_ = d[s], n_[s]
            gec = n_ > 0; d, n_ = d[gec], n_[gec]
            if len(d):
                i = np.searchsorted(hepsi, d, side="left"); v2 = i < len(hepsi)
                aday = hepsi[np.minimum(i, max(len(hepsi) - 1, 0))] if len(hepsi) else d
                yakin = v2 & ((aday - d) <= gD(120))
                pay[j] = (d, n_, np.where(yakin, aday, d + gD(Bg["pay_yedek_gun"])))
    T.update({"bilgi": bilgi, "Ybilgi": Ybilgi, "Yq": Yq, "mali": mali, "bilgi_kaynak": kay, "ybilgi_kaynak": ykay, "pay": pay, "turetilen_q4": turetilen})
    T.pop("pay_ham", None)
    return T


def _k60_panel_anahtar(veri_sha: Dict[str, Tuple[str, int]]) -> str:
    kod = _k60_sha(os.path.join(KOK_K60, "K60.py")) if os.path.exists(os.path.join(KOK_K60, "K60.py")) else "exec"
    return _k60_metin_sha(json.dumps({"veri": veri_sha, "kod": kod, "muhur": k60_esik_sha()}, sort_keys=True, default=str))[:16]


def k60_demet_yukle(veri_sha: Optional[Dict[str, Tuple[str, int]]] = None, onbellek: bool = True) -> Dict[str, Any]:
    """GERÇEK veri demeti (yalnız önbellek okunur; ağ yok): günlük O / H / L / C / A / V matrisleri (işlem günü x hisse), bölünmeler, temettü
    günleri, ilk işlem günü, CIK, SIC, temel tablo (bilgi tarihleriyle), başvuru günleri, French günlük ve aylık faktörler. Aynı veri ve aynı
    kodla ikinci çağrı /tmp/k60_panel önbelleğinden okur."""
    E = K60_ESIK; V = E["veri"]; t0 = time.time()
    veri_sha = veri_sha if veri_sha is not None else k60_veri_sha()
    yol = os.path.join(K60_YOL["panel"], f"demet_{_k60_panel_anahtar(veri_sha)}.pkl")
    if onbellek and os.path.exists(yol):
        try:
            with open(yol, "rb") as f:
                D = pickle.load(f)
            k60log.info("demet önbellekten: %s (%d hisse, %d gün; %.0f sn)", yol, len(D["sembol"]), len(D["gun"]), time.time() - t0)
            return D
        except Exception as ex:   # bozuk ara önbellek: yeniden kurulur
            k60log.warning("demet önbelleği okunamadı (%s): yeniden kuruluyor", ex)
    kl = KV.K60V_YOL["fiyat"]; ev = pd.read_csv(os.path.join(kl, KV.K60V_DOSYA["evren"]), dtype=str)
    ham: Dict[str, Dict[str, Any]] = {}; say = {"kirpik": 0, "tur_disi": 0, "fiyatsiz": 0}
    for s in ev.sembol:
        y = os.path.join(kl, KV._k60v_fiyat_adi(s))
        o, dr = k60_fiyat_oku(y, V["kes"]) if os.path.exists(y) else (None, "inmedi")
        if o is None:
            say["kirpik" if "kırpık" in dr else "fiyatsiz"] += 1
        elif o["tur"] not in V["tur"]:
            say["tur_disi"] += 1
        elif V["kirpik_haric"] and o["kirpik"]:
            say["kirpik"] += 1
        else:
            ham[s] = o
    if len(ham) < V["min_hisse"]:
        raise K60Hata(f"fiyat önbelleğinden {len(ham)} hisse yüklendi (< {V['min_hisse']}): önbellek {kl} eksik")
    S = sorted(ham); N = len(S)
    gunler, adet = np.unique(np.concatenate([ham[s]["gun"] for s in S]), return_counts=True)
    tak = gunler[adet >= max(1.0, float(V["takvim_pay"]) * float(np.median(adet)))]; G = len(tak)
    M = {k: np.full((G, N), np.nan) for k in ("O", "H", "L", "C", "A", "V")}
    bol: Dict[str, Any] = {}; tem: Dict[str, np.ndarray] = {}; ilk = np.full(N, np.datetime64("NaT", "D"))
    for j, s in enumerate(S):
        o = ham[s]; p = np.searchsorted(tak, o["gun"]); ok = (p < G); ok[ok] &= tak[p[ok]] == o["gun"][ok]
        for k, a in (("O", "o"), ("H", "h"), ("L", "l"), ("C", "c"), ("A", "a"), ("V", "v")):
            M[k][p[ok], j] = o[a][ok]
        if o["bolunme"] is not None:
            bol[s] = o["bolunme"]
        if len(o["temettu"]):
            tem[s] = o["temettu"]
        ilk[j] = o["ilk_islem"]
    del ham
    k60log.info("fiyat: %d hisse x %d gün (%s .. %s); dışarıda %s (%.0f sn)", N, G, tak[0], tak[-1], say, time.time() - t0)
    tk = _k60_json_oku(K60_YOL["tickers"]); s2c: Dict[str, str] = {}
    for v in tk.values():
        s2c.setdefault(str(v["ticker"]).upper().replace(".", "-"), str(int(v["cik_str"])))
    cik = [s2c.get(s) for s in S]
    import io
    sicd = pd.read_csv(io.BytesIO(_k60_git_blob(V["sic"]) or b"cik,sic\n"), dtype=str)
    c2sic = {str(int(c)): int(x) for c, x in zip(sicd.cik, sicd.sic) if str(x).isdigit() and str(c).isdigit()}
    sic = np.array([c2sic.get(c, -1) if c is not None else -1 for c in cik], int)
    B = k60_dizin_oku({c for c in cik if c is not None}, E)
    basv = {g: [B[g].get(c) if c is not None else None for c in cik] for g in B}
    k60log.info("dizin: %s (%.0f sn)", {g: sum(x is not None for x in basv[g]) for g in basv}, time.time() - t0)
    T = k60_temel_tamamla(k60_temel_yukle(cik, E), basv["K"], basv["Q"], E)
    k60log.info("temel: %d çeyreklik, %d anlık, %d yıllık etiket; %d türetilmiş 4. çeyrek (%.0f sn)", len(T["Q"]), len(T["I"]), len(T["Y"]), T["turetilen_q4"],
                time.time() - t0)
    try:
        ffa = K59.k59_french({k: os.path.join(K58.K58_YOL["french"], z) for k, z in K58.K58_ESIK["B"]["zip"].items()})
    except (K59.K59Hata, K58.K58Hata, OSError, ValueError) as ex:
        raise K60Hata(f"French aylık faktörleri okunamadı: {ex}")
    D = {"gun": pd.DatetimeIndex(tak.astype("datetime64[ns]")), "sembol": S, **M, "bolunme": bol, "temettu": tem, "ilk_islem": ilk,
         "tur_ok": np.ones(N, bool), "cik": cik, "sic": sic, "temel": T, "basvuru": basv, "ff_gunluk": k60_french_gunluk(), "ff_aylik": ffa,
         "sayim": {**say, "hisse": N}}
    if onbellek:
        os.makedirs(K60_YOL["panel"], exist_ok=True)
        with open(yol + ".yarim", "wb") as f:
            pickle.dump(D, f, protocol=4)
        os.replace(yol + ".yarim", yol)
    k60log.info("demet hazır: %d hisse, %d gün (%.0f sn)", N, G, time.time() - t0)
    return D


# ---------------------------------------------------------------- 3) AYLIK PANEL + UYGUNLUK (yalnız t ve öncesi bilgi)
def _k60_ffill(X: np.ndarray, limit: Optional[int]) -> np.ndarray:
    return np.array(pd.DataFrame(X).ffill(limit=limit).to_numpy(float), copy=True)


def k60_panel(D: Dict[str, Any], E: Optional[Dict[str, Any]] = None, getiri: bool = True) -> Dict[str, Any]:
    """Ay sonları, uygun evren U (K59 U2 ile aynı kurallar), ay sonu fiyatları; getiri=True ise ayrıca R (1 ay; K58 k58_aylik kuralı) ve
    F[h] (h ay ileri toplam getiri). getiri=False (kapsam sayımı): hiçbir ileri getiri hesaplanmaz."""
    E = E or K60_ESIK; uy = E["uygunluk"]; gun = pd.DatetimeIndex(D["gun"]); S = list(D["sembol"]); N = len(S)
    ay = gun.to_period("M"); son = np.r_[np.asarray(ay[1:] != ay[:-1]), True]; mp = np.flatnonzero(son); me = gun[mp]; M = len(mp)
    C, V = D["C"], D["V"]
    with np.errstate(invalid="ignore"):
        A = np.where(D["A"] > 0, D["A"], np.nan)          # Yahoo düzeltilmiş kapanışı <= 0 olan günler yok sayılır (getiri tanımsız)
    C5 = _k60_ffill(C, uy["ileri_tasima"]); A5 = _k60_ffill(A, uy["ileri_tasima"])
    Cm = np.array(C5[mp], copy=True); Am = np.array(A5[mp], copy=True)
    with np.errstate(invalid="ignore"):
        gecmis = np.cumsum(np.isfinite(C) & (np.nan_to_num(C, nan=0.0) > 0), axis=0)[mp] >= uy["gecmis_gun"]
    tl = np.full((M, N), np.nan); lg = int(uy["likit_gun"])
    with np.errstate(invalid="ignore"):
        for i, p in enumerate(mp):
            blok = C[max(0, p - lg + 1):p + 1] * V[max(0, p - lg + 1):p + 1]
            n_ = np.isfinite(blok).sum(axis=0); yeter = n_ >= uy["likit_min_gun"]
            if yeter.any():
                tl[i, yeter] = np.nanmedian(blok[:, yeter], axis=0)
    carp = np.ones((M, N)); mt = me.to_numpy("datetime64[ns]"); bol = D.get("bolunme") or {}
    for j, s in enumerate(S):
        if s in bol:
            carp[:, j] = K59.k59_bolunme_carpan(bol[s], mt)
    fiyat_o = Cm * carp
    once = np.vstack([np.full((1, N), np.nan), Am[:-1]])
    with np.errstate(invalid="ignore"):
        U = (np.isfinite(Am) & np.isfinite(once) & gecmis & np.isfinite(fiyat_o) & (fiyat_o >= uy["fiyat_min"])
             & (np.nan_to_num(tl, nan=-1.0) >= uy["likit_min"]) & np.asarray(D.get("tur_ok", np.ones(N, bool)), bool)[None, :])
    olusum = (U.sum(axis=1) >= uy["min_evren"]); olusum[-1] = False
    U[~olusum] = False
    P: Dict[str, Any] = {"ay_sonu": me, "me_pos": mp, "sembol": S, "U": U, "olusum": olusum, "Cm": Cm, "Am": Am, "C5": C5, "A5": A5, "tl_me": tl,
                         "fiyat_o": fiyat_o, "mtD": me.to_numpy("datetime64[D]"), "gunD": gun.to_numpy("datetime64[D]"), "R": None, "F": {}}
    if getiri:
        Ax = _k60_ffill(A, None)[mp]
        with np.errstate(invalid="ignore", divide="ignore"):
            R = np.full((M, N), np.nan); R[:-1] = Ax[1:] / Am[:-1] - 1
            P["R"] = np.where(U, R, np.nan)
            for h in E["r2"]["ufuk"]:
                F = np.full((M, N), np.nan)
                if h < M:
                    F[:-h] = Am[h:] / Am[:-h] - 1
                P["F"][int(h)] = np.where(U, F, np.nan)
    return P


def k60_donem_aylari(P: Dict[str, Any], donem: str, ufuk: int, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Dönemin OLUŞUM ayları (bool, ay): takvim ayı dönem aralığında, evren yeterli ve ileri penceresi (ufuk ay) veride bitiyor."""
    E = E or K60_ESIK; a, b = E["donem"][donem]; ay = P["ay_sonu"].to_period("M"); M = len(ay)
    m = np.asarray((ay >= pd.Period(a, "M")) & (ay <= pd.Period(b, "M"))) & P["olusum"]
    return m & (np.arange(M) + int(ufuk) <= M - 1)


# ---------------------------------------------------------------- 4) SİNYALLER (ay x hisse; HAM ölçü; yalnız t ve öncesi bilgi)
def _k60_cs(X: np.ndarray) -> np.ndarray:
    """Sütun bazında birikimli toplam (NaN = 0), başında sıfır satırı: pencere toplamı iki satırın farkıdır."""
    out = np.zeros((X.shape[0] + 1, X.shape[1]))
    np.cumsum(np.nan_to_num(X.astype(float), nan=0.0), axis=0, out=out[1:])
    return out


def _k60_pt(cs: np.ndarray, pos: np.ndarray, W: int) -> np.ndarray:
    """pos satırında biten W satırlık pencerenin toplamı (pos dahil)."""
    return cs[pos + 1] - cs[np.maximum(pos + 1 - int(W), 0)]


def _k60_kay(X: np.ndarray, k: int) -> np.ndarray:
    """k ay ÖNCEKİ değer (satır kaydırma; ilk k satır NaN)."""
    out = np.full(X.shape, np.nan)
    if 0 < k < len(X):
        out[k:] = X[:-k]
    elif k == 0:
        out[:] = X
    return out


def _k60_bol(a: np.ndarray, b: np.ndarray, pozitif: bool = False) -> np.ndarray:
    """a / b; b sıfır / sonlu değil (pozitif=True ise b <= 0) -> NaN."""
    with np.errstate(invalid="ignore", divide="ignore"):
        ok = np.isfinite(a) & np.isfinite(b) & ((b > 0) if pozitif else (b != 0))
        return np.where(ok, a / np.where(ok, b, 1.0), np.nan)


def _k60_ilk(*a: np.ndarray) -> np.ndarray:
    """Sırayla ilk sonlu değer."""
    out = np.array(a[0], float, copy=True)
    for x in a[1:]:
        out = np.where(np.isfinite(out), out, x)
    return out


def _k60_artik(Y: np.ndarray, X: np.ndarray, min_n: int) -> Tuple[np.ndarray, np.ndarray]:
    """Sütun sütun sabitsiz EKK (X'e sabit sütunu çağıran koyar): her sütun kendi geçerli satırlarıyla. Döner (artıklar; geçersiz NaN, n)."""
    sat = np.isfinite(X).all(axis=1); ok = np.isfinite(Y) & sat[:, None]
    Y0 = np.where(ok, Y, 0.0); X0 = np.where(sat[:, None], X, 0.0); w = ok.astype(float)
    XtX = np.einsum("kn,ka,kb->nab", w, X0, X0); Xty = np.einsum("kn,ka->na", Y0, X0)
    b = np.einsum("nab,nb->na", np.linalg.pinv(XtX), Xty)
    n = ok.sum(axis=0)
    e = np.where(ok & (n >= min_n)[None, :], Y0 - X0 @ b.T, np.nan)
    return e, n


def k60_duyuru_gunu(donemsel: Optional[np.ndarray], sekizk: Optional[np.ndarray], gun: int) -> np.ndarray:
    """Açıklama günü VEKİLİ d*: her 10-Q / 10-K başvuru günü f için, [f - gun, f] aralığındaki EN SON 8-K günü; yoksa f. Çıktı f ile hizalıdır
    (aynı uzunluk, aynı sıra); d* <= f olduğu için f bilindiği gün d* de bilinir."""
    if donemsel is None or not len(donemsel):
        return np.array([], "datetime64[D]")
    f = np.asarray(donemsel, "datetime64[D]")
    if sekizk is None or not len(sekizk):
        return f.copy()
    k = np.asarray(sekizk, "datetime64[D]"); i = np.searchsorted(k, f, side="right") - 1; var = i >= 0
    aday = k[np.maximum(i, 0)]
    return np.where(var & (aday >= f - np.timedelta64(int(gun), "D")), aday, f)


class _K60Temel:
    """Temel tablonun ay sonu 'o gün bilinen' görünümü. ç0 = bilgi tarihi < t olan EN SON çeyrek (çeyrek sonu t'den en çok ceyrek_max_gun gün
    önce); y0 = bilgi tarihi < t olan en son mali yıl. q / i / y / ya: ç0 - gecikme (y0 - gecikme) değerleri; gecikmeli dönemin de bilgi tarihi < t olmalı."""

    def __init__(self, T: Optional[Dict[str, Any]], mtD: np.ndarray, N: int, Bg: Dict[str, Any]):
        self.T = T; self.M = len(mtD); self.N = N; self.mt = mtD[:, None]; self.sut = np.arange(N)[None, :]
        self.q0 = np.full((self.M, N), -1); self.y0 = np.full((self.M, N), -1)
        if T is None:
            return
        with np.errstate(invalid="ignore"):
            for q in range(T["bilgi"].shape[0]):
                self.q0[T["bilgi"][q][None, :] < self.mt] = q
            b = T["bit"][np.maximum(self.q0, 0), self.sut]
            self.q0[~((self.q0 >= 0) & ((self.mt - b) <= np.timedelta64(int(Bg["ceyrek_max_gun"]), "D")))] = -1
            for y in range(T["Ybilgi"].shape[0]):
                self.y0[T["Ybilgi"][y][None, :] < self.mt] = y
            b = T["Ybit"][np.maximum(self.y0, 0), self.sut]
            self.y0[~((self.y0 >= 0) & ((self.mt - b) <= np.timedelta64(int(Bg["yil_max_gun"]), "D")))] = -1

    def _al(self, tab: str, etiket: str, i0: np.ndarray, gec: int, bil: str) -> np.ndarray:
        bos = np.full((self.M, self.N), np.nan)
        if self.T is None or etiket not in self.T[tab]:
            return bos
        i = i0 - gec; ic = np.maximum(i, 0)
        with np.errstate(invalid="ignore"):
            ok = (i0 >= 0) & (i >= 0) & (self.T[bil][ic, self.sut] < self.mt)
        return np.where(ok, self.T[tab][etiket][ic, self.sut], np.nan)

    def q(self, etiket: str, gec: int = 0) -> np.ndarray:
        return self._al("Q", etiket, self.q0, gec, "bilgi")

    def i(self, etiket: str, gec: int = 0) -> np.ndarray:
        return self._al("I", etiket, self.q0, gec, "bilgi")

    def y(self, etiket: str, gec: int = 0) -> np.ndarray:
        return self._al("Y", etiket, self.y0, gec, "Ybilgi")

    def ya(self, etiket: str, gec: int = 0) -> np.ndarray:
        """Mali yıl sonundaki anlık değer (y0 - gecikme yılının sonu)."""
        bos = np.full((self.M, self.N), np.nan)
        if self.T is None or etiket not in self.T["I"]:
            return bos
        i = self.y0 - gec; ic = np.maximum(i, 0)
        with np.errstate(invalid="ignore"):
            ok = (self.y0 >= 0) & (i >= 0) & (self.T["Ybilgi"][ic, self.sut] < self.mt)
        qy = self.T["Yq"][ic, self.sut]
        return np.where(ok & (qy >= 0), self.T["I"][etiket][np.maximum(qy, 0), self.sut], np.nan)

    def ttm(self, etiket: str, gec: int = 0) -> np.ndarray:
        return self.q(etiket, gec) + self.q(etiket, gec + 1) + self.q(etiket, gec + 2) + self.q(etiket, gec + 3)


def k60_pay(D: Dict[str, Any], P: Dict[str, Any], AO: _K60Temel, E: Optional[Dict[str, Any]] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Ay sonu t'de bilinen pay sayısı, BUGÜNKÜ pay biriminde (kapak sayısı x kapak gününden sonraki bölünmeler). Döner (pay, kaynak): kaynak
    1 = kapak (dei), 2 = bilanço pay sayısı, 3 = ağırlıklı ortalama (2 ve 3 yalnız hiç bölünmesi olmayan hisselerde), 0 = yok."""
    Bg = (E or K60_ESIK)["bilgi"]; M, N = P["U"].shape; SH = np.full((M, N), np.nan); kay = np.zeros((M, N), np.int8)
    T = D.get("temel"); mt = P["mtD"]; bol = D.get("bolunme") or {}; S = P["sembol"]
    if T is None:
        return SH, kay
    maxg = np.timedelta64(int(Bg["pay_max_gun"]), "D")
    for j in range(N):
        rec = T["pay"][j] if T.get("pay") is not None else None
        if rec is None or not len(rec[0]):
            continue
        d, n_, b = rec; s = np.argsort(b, kind="stable"); d, n_, b = d[s], n_[s], b[s]
        k_ = np.zeros(len(d), int); eniyi = 0                 # bilgi tarihi sırasında, o ana kadarki EN GEÇ kapak gününün kaydı
        for i_ in range(len(d)):
            if d[i_] >= d[eniyi]:
                eniyi = i_
            k_[i_] = eniyi
        i = np.searchsorted(b, mt, side="left") - 1; ok = i >= 0; kk = k_[np.maximum(i, 0)]
        dd = d[kk]
        with np.errstate(invalid="ignore"):
            ok &= (mt - dd) <= maxg
        if ok.any():
            c = K59.k59_bolunme_carpan(bol.get(S[j]), dd.astype("datetime64[ns]"))
            SH[ok, j] = (n_[kk] * c)[ok]; kay[ok, j] = 1
    bolunmesiz = np.array([s not in bol for s in S], bool)[None, :]
    for kod, etiket, al in ((2, _K60_PAY_ETIKET[1], AO.i), (3, _K60_PAY_ETIKET[2], AO.q)):
        x = al(etiket, 0)
        with np.errstate(invalid="ignore"):
            m = ~np.isfinite(SH) & np.isfinite(x) & (x > 0) & bolunmesiz
        SH[m] = x[m]; kay[m] = kod
    return SH, kay


def _k60_sinyal_fiyat(D: Dict[str, Any], P: Dict[str, Any], E: Dict[str, Any]) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """Fiyat / hacim sinyalleri (MOM, RSK, LIQ, SEA'nın getiri bölümü). Döner (sinyaller, ara ölçüler: v252, sigma, rm, getiri6, mkt_ay)."""
    pr = E["param"]; mp = P["me_pos"]; M, N = P["U"].shape; Am, Cm = P["Am"], P["Cm"]; S: Dict[str, np.ndarray] = {}; ara: Dict[str, np.ndarray] = {}
    kay = _k60_kay; bos = lambda: np.full((M, N), np.nan)  # noqa: E731
    with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
        S["MOM_12_1"] = kay(Am, 1) / kay(Am, 12) - 1; S["MOM_6_1"] = kay(Am, 1) / kay(Am, 6) - 1; S["MOM_INT_12_7"] = kay(Am, 6) / kay(Am, 12) - 1
        rm = Am / kay(Am, 1) - 1; S["STREV_1M"] = rm.copy(); S["LTREV_60_13"] = kay(Am, 12) / kay(Am, 60) - 1
        S["SEAS_1"] = kay(rm, 11); S["SEAS_2_5"] = (kay(rm, 23) + kay(rm, 35) + kay(rm, 47) + kay(rm, 59)) / 4.0
        ara["rm"] = rm; ara["getiri6"] = Am / kay(Am, 6) - 1
        S["PRICE_LVL"] = np.where(P["fiyat_o"] > 0, np.log(np.where(P["fiyat_o"] > 0, P["fiyat_o"], 1.0)), np.nan)
        A5 = P["A5"]; r = np.full(A5.shape, np.nan); r[1:] = A5[1:] / A5[:-1] - 1; r[~np.isfinite(r)] = np.nan
        G = len(r); C, V, H, L, O = D["C"], D["V"], D["H"], D["L"], D["O"]
        gun = pd.DatetimeIndex(D["gun"]); ffg = D.get("ff_gunluk")
        if ffg is not None:
            fx = ffg.reindex(gun); mkt = (fx["MKT_RF"] + fx["RF"]).to_numpy(float); rf = fx["RF"].to_numpy(float)
            X3 = np.column_stack([np.ones(G), fx[["MKT_RF", "SMB", "HML"]].to_numpy(float)])
        else:
            mkt = rf = X3 = None
        ara["mkt_gun"] = mkt
        # 60 / 63 günlük oynaklık
        c1, c2, cn = _k60_cs(r), _k60_cs(r * r), _k60_cs(np.isfinite(r))
        n = _k60_pt(cn, mp, pr["vol_gun"]); s1 = _k60_pt(c1, mp, pr["vol_gun"]); s2 = _k60_pt(c2, mp, pr["vol_gun"])
        S["VOL_60D"] = np.where(n >= pr["vol_min"], np.sqrt(np.maximum((s2 - s1 * s1 / np.maximum(n, 1)) / np.maximum(n - 1, 1), 0.0)), np.nan)
        n = _k60_pt(cn, mp, pr["sigma_gun"]); s2 = _k60_pt(c2, mp, pr["sigma_gun"])
        ara["sigma"] = np.where(n >= pr["vol_min"], np.sqrt(252.0 * s2 / np.maximum(n, 1)), np.nan)
        # süreklilik (MOM_FIP bileşeni): günler (m-12 ay sonu, m-1 ay sonu]
        cp, cg = _k60_cs(r > 0), _k60_cs(r < 0); sur = bos()
        for m in range(12, M):
            a, b = mp[m - 12] + 1, mp[m - 1] + 1
            nn = cn[b] - cn[a]; fark = (cp[b] - cp[a]) - (cg[b] - cg[a])
            sur[m] = np.where(nn >= pr["fip_min_gun"], np.sign(S["MOM_12_1"][m]) * fark / np.maximum(nn, 1), np.nan)
        ara["sureklilik"] = sur; del cp, cg
        # beta: korelasyon (uzun pencere) x oynaklık oranı (bir yıl)
        if mkt is not None:
            ok = np.isfinite(r) & np.isfinite(mkt)[:, None]; rb = np.where(ok, r, np.nan); mb = np.where(ok, mkt[:, None], np.nan)
            cb = {k: _k60_cs(x) for k, x in (("n", ok), ("r", rb), ("m", mb), ("rr", rb * rb), ("mm", mb * mb), ("rm", rb * mb))}
            del rb, mb

            def an(W: int) -> Tuple[np.ndarray, ...]:
                t = {k: _k60_pt(x, mp, W) for k, x in cb.items()}; nn_ = np.maximum(t["n"], 1)
                return t["n"], t["rr"] - t["r"] ** 2 / nn_, t["mm"] - t["m"] ** 2 / nn_, t["rm"] - t["r"] * t["m"] / nn_
            nk, vr, vm, cv = an(pr["beta_kor_gun"]); nv, vr1, vm1, _c = an(pr["yil_gun"])
            kor = np.where((nk >= pr["beta_kor_min"]) & (vr > 0) & (vm > 0), cv / np.sqrt(np.where((vr > 0) & (vm > 0), vr * vm, 1.0)), np.nan)
            S["BETA_BAB"] = np.where((nv >= pr["beta_vol_min"]) & (vr1 > 0) & (vm1 > 0), kor * np.sqrt(np.where(vm1 > 0, vr1 / np.where(vm1 > 0, vm1, 1.0), np.nan)), np.nan)
            del cb
        else:
            S["BETA_BAB"] = bos()
        del c1, c2
        # likidite
        dv = C * V; x = np.where(dv > 0, np.abs(r) / np.where(dv > 0, dv, 1.0), np.nan)
        n = _k60_pt(_k60_cs(np.isfinite(x)), mp, pr["yil_gun"])
        S["AMIHUD"] = np.where(n >= pr["yil_min"], 1.0e6 * _k60_pt(_k60_cs(x), mp, pr["yil_gun"]) / np.maximum(n, 1), np.nan); del x
        cv_, cvn = _k60_cs(V), _k60_cs(np.isfinite(V))
        n = _k60_pt(cvn, mp, pr["yil_gun"]); ara["v252"] = np.where(n >= pr["yil_min"], _k60_pt(cv_, mp, pr["yil_gun"]) / np.maximum(n, 1), np.nan)
        k_, u_ = pr["shock_kisa"], pr["shock_kisa"] + pr["shock_uzun"]
        n5, n55 = _k60_pt(cvn, mp, k_), _k60_pt(cvn, mp, u_); t5, t55 = _k60_pt(cv_, mp, k_), _k60_pt(cv_, mp, u_)
        ok = (n5 >= pr["shock_min"][0]) & (n55 - n5 >= pr["shock_min"][1]) & (t55 - t5 > 0)
        S["VOL_SHOCK"] = np.where(ok, (t5 / np.maximum(n5, 1)) / np.where(ok, (t55 - t5) / np.maximum(n55 - n5, 1), 1.0), np.nan); del cv_, cvn
        # 52 hafta zirvesi
        z = bos()
        for m in range(M):
            p = mp[m]; blok = H[max(0, p - pr["yil_gun"] + 1):p + 1]
            z[m] = np.where(np.isfinite(blok).sum(axis=0) >= pr["zirve_min"], np.fmax.reduce(blok, axis=0), np.nan)
        S["HIGH52"] = np.where(z > 0, Cm / np.where(z > 0, z, 1.0), np.nan)
        # takvim ayı pencereli ölçüler
        for k in ("MAX5", "SKEW_TOT", "IVOL_FF3", "ISKEW", "SPREAD_CS", "GAP_OVN"):
            S[k] = bos()
        dvm = bos(); mg = pr["ay_min_gun"]; kcs = 3.0 - 2.0 * math.sqrt(2.0)
        for m in range(M):
            a, b = (mp[m - 1] + 1 if m else 0), mp[m] + 1; rr = r[a:b]; nn = np.isfinite(rr).sum(axis=0); yeter = nn >= mg
            if b - a >= 5:
                az = -np.sort(-rr, axis=0)[:5]
                S["MAX5"][m] = np.where(yeter, az.mean(axis=0), np.nan)
                mu = np.nansum(rr, axis=0) / np.maximum(nn, 1); dd = rr - mu
                m2 = np.nansum(dd ** 2, axis=0) / np.maximum(nn, 1); m3 = np.nansum(dd ** 3, axis=0) / np.maximum(nn, 1)
                S["SKEW_TOT"][m] = np.where(yeter & (m2 > 0), m3 / np.where(m2 > 0, m2, 1.0) ** 1.5, np.nan)
                if X3 is not None:
                    e, ne = _k60_artik(rr - rf[a:b, None], X3[a:b], mg)
                    e2 = np.nansum(e ** 2, axis=0) / np.maximum(ne, 1); e3 = np.nansum(e ** 3, axis=0) / np.maximum(ne, 1); ok = (ne >= mg) & (e2 > 0)
                    S["IVOL_FF3"][m] = np.where(ok, np.sqrt(e2), np.nan); S["ISKEW"][m] = np.where(ok, e3 / np.where(ok, e2, 1.0) ** 1.5, np.nan)
                h0, l0, h1, l1 = H[a:b - 1], L[a:b - 1], H[a + 1:b], L[a + 1:b]
                ok = np.isfinite(h0) & np.isfinite(l0) & np.isfinite(h1) & np.isfinite(l1) & (l0 > 0) & (l1 > 0) & (h0 > 0) & (h1 > 0)
                g1 = lambda x_: np.where(ok, x_, 1.0)  # noqa: E731
                beta = np.log(g1(h0) / g1(l0)) ** 2 + np.log(g1(h1) / g1(l1)) ** 2
                gam = np.log(np.maximum(g1(h0), g1(h1)) / np.minimum(g1(l0), g1(l1))) ** 2
                alfa = (math.sqrt(2.0) - 1.0) * np.sqrt(beta) / kcs - np.sqrt(gam / kcs)
                sp = np.where(ok, np.maximum(2.0 * (np.exp(alfa) - 1.0) / (1.0 + np.exp(alfa)), 0.0), np.nan); ns = ok.sum(axis=0)
                S["SPREAD_CS"][m] = np.where(ns >= pr["cs_min"], np.nansum(sp, axis=0) / np.maximum(ns, 1), np.nan)
                a1 = max(a, 1); o_, cp_ = O[a1:b], C[a1 - 1:b - 1]; ok = np.isfinite(o_) & np.isfinite(cp_) & (o_ > 0) & (cp_ > 0)
                gece = np.where(ok, np.log(np.where(ok, o_, 1.0) / np.where(ok, cp_, 1.0)), 0.0)
                S["GAP_OVN"][m] = np.where(ok.sum(axis=0) >= mg, gece.sum(axis=0), np.nan)
            dd_ = dv[a:b]; nd = np.isfinite(dd_).sum(axis=0)
            dvm[m] = np.where(nd >= mg, np.nansum(dd_, axis=0) / np.maximum(nd, 1), np.nan)
        dv1 = kay(dvm, 1); S["DOLVOL"] = np.where(dv1 > 0, np.log(np.where(dv1 > 0, dv1, 1.0)), np.nan)
        # TREND_MA
        C5 = P["C5"]; ccs, ccn = _k60_cs(C5), _k60_cs(np.isfinite(C5)); Lg = list(pr["trend_gun"])
        X = np.stack([np.where((_k60_pt(ccn, mp, L_) >= L_) & (Cm > 0), _k60_pt(ccs, mp, L_) / L_ / np.where(Cm > 0, Cm, 1.0), np.nan) for L_ in Lg], axis=2); del ccs, ccn
        kat = np.full((M, len(Lg) + 1), np.nan); U = P["U"]
        for k in range(1, M):
            ok = U[k - 1] & np.isfinite(X[k - 1]).all(axis=1) & np.isfinite(rm[k])
            if ok.sum() >= 50:
                kat[k] = np.linalg.lstsq(np.column_stack([np.ones(int(ok.sum())), X[k - 1, ok]]), rm[k, ok], rcond=None)[0]
        tr = bos(); ta = pr["trend_ay"]
        for m in range(ta, M):
            eb = kat[m - ta + 1:m + 1]
            if np.isfinite(eb).all():
                tr[m] = X[m] @ eb.mean(axis=0)[1:]
        S["TREND_MA"] = tr
        # MOM_RES_12_1
        res = bos(); ffa = D.get("ff_aylik"); ra, rs = pr["res_ay"], pr["res_son"]
        if ffa is not None:
            fa = ffa.reindex(P["ay_sonu"].to_period("M")); Fm = fa[["MKT_RF", "SMB", "HML"]].to_numpy(float); rfm = fa["RF"].to_numpy(float)
            ara["mkt_ay"] = Fm[:, 0] + rfm
            for m in range(ra - 1, M):
                Xw = np.column_stack([np.ones(ra), Fm[m - ra + 1:m + 1]])
                if not np.isfinite(Xw).all() or not np.isfinite(rfm[m - ra + 1:m + 1]).all():
                    continue
                Yw = rm[m - ra + 1:m + 1] - rfm[m - ra + 1:m + 1, None]; c = np.isfinite(Yw).all(axis=0)
                if not c.any():
                    continue
                e = Yw[:, c] - Xw @ np.linalg.lstsq(Xw, Yw[:, c], rcond=None)[0]; alt = e[ra - 1 - rs:ra - 1]; sd = alt.std(axis=0, ddof=1)
                res[m, c] = np.where(sd > 0, alt.sum(axis=0) / np.where(sd > 0, sd, 1.0), np.nan)
        S["MOM_RES_12_1"] = res
    return S, ara


def _k60_sinyal_temel(D: Dict[str, Any], P: Dict[str, Any], E: Dict[str, Any], ara: Dict[str, np.ndarray]) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
    """Temel veri sinyalleri (VAL, PRF, INV, EAR'ın temel bölümü, DIS, SIZE_ME, TURN_12M) ve REV_YOY bileşeni."""
    pr = E["param"]; M, N = P["U"].shape; U = P["U"]; AO = _K60Temel(D.get("temel"), P["mtD"], N, E["bilgi"]); S: Dict[str, np.ndarray] = {}
    bol, ilk, kay = _k60_bol, _k60_ilk, _k60_kay; GEL = list(K57.K57_ABD_GELIR)
    SH, pk = k60_pay(D, P, AO, E)
    with np.errstate(invalid="ignore", divide="ignore"):
        PD = np.where(np.isfinite(SH) & (SH > 0) & np.isfinite(P["Cm"]), P["Cm"] * SH, np.nan)
        ek = {"pay_kaynak": pk, "q0": AO.q0, "y0": AO.y0, "PD": PD}
        if D.get("temel") is None:
            return S, ek

        def gel(f: Callable[[str], np.ndarray]) -> np.ndarray:
            """Gelir formülü: bütün çeyrekleri aynı etiketten olan ilk etiketin sonucu."""
            return ilk(*[f(t) for t in GEL])
        AT = lambda g=0: ilk(AO.i("Assets", g), AO.i("LiabilitiesAndStockholdersEquity", g))  # noqa: E731
        EQ = lambda g=0: AO.i("StockholdersEquity", g)  # noqa: E731
        LT = lambda g=0: ilk(AO.i("Liabilities", g), AT(g) - EQ(g))  # noqa: E731
        LTD = lambda g=0: ilk(AO.i("LongTermDebt", g), AO.i("LongTermDebtNoncurrent", g))  # noqa: E731
        NAKIT = AO.i("CashAndCashEquivalentsAtCarryingValue", 0)
        NI = lambda g=0: AO.q("NetIncomeLoss", g)  # noqa: E731
        ni4 = AO.ttm("NetIncomeLoss"); oi4 = AO.ttm("OperatingIncomeLoss"); rev4 = gel(lambda t: AO.ttm(t))
        gp4 = ilk(AO.ttm("GrossProfit"), gel(lambda t: AO.ttm(t)) - ilk(AO.ttm("CostOfRevenue"), AO.ttm("CostOfGoodsAndServicesSold")))
        # yıllık
        ATy = lambda g=0: ilk(AO.ya("Assets", g), AO.ya("LiabilitiesAndStockholdersEquity", g))  # noqa: E731
        OCF = lambda g=0: AO.y("NetCashProvidedByUsedInOperatingActivities", g)  # noqa: E731
        NIy = lambda g=0: AO.y("NetIncomeLoss", g)  # noqa: E731
        REVy = lambda g=0: ilk(*[AO.y(t, g) for t in GEL])  # noqa: E731
        GPy = lambda g=0: ilk(AO.y("GrossProfit", g), REVy(g) - ilk(AO.y("CostOfRevenue", g), AO.y("CostOfGoodsAndServicesSold", g)))  # noqa: E731
        TEM = ilk(AO.y("PaymentsOfDividends"), AO.y("PaymentsOfDividendsCommonStock")); GERI = AO.y("PaymentsForRepurchaseOfCommonStock")
        IHR = AO.y("ProceedsFromIssuanceOfCommonStock"); CAPEX = lambda g=0: AO.y("PaymentsToAcquirePropertyPlantAndEquipment", g)  # noqa: E731
        ocf0 = OCF(0); nakit_tablo = np.isfinite(ocf0); s0 = lambda x: np.where(np.isfinite(x), x, 0.0)  # noqa: E731
        ort_at_y = (ATy(0) + ATy(1)) / 2.0
        # DEĞER
        S["BM"] = bol(np.where(EQ() > 0, EQ(), np.nan), PD, True); S["EP"] = bol(ni4, PD, True); S["SP"] = bol(np.where(rev4 > 0, rev4, np.nan), PD, True)
        S["AM"] = bol(AT(), PD, True); S["LEV_MKT"] = bol(LT(), PD, True); S["CFP"] = bol(ocf0, PD, True)
        ebitda = oi4 + AO.y("DepreciationDepletionAndAmortization")
        S["EV_EBITDA"] = bol(PD + s0(LTD()) - s0(NAKIT), np.where(ebitda > 0, ebitda, np.nan), True)
        S["NET_PAYOUT_YLD"] = bol(np.where(nakit_tablo, s0(TEM) + s0(GERI) - s0(IHR), np.nan), PD, True)
        S["BUYBACK_YLD"] = bol(np.where(nakit_tablo, s0(GERI), np.nan), PD, True)
        S["RD_ME"] = bol(AO.ttm("ResearchAndDevelopmentExpense"), PD, True)
        # KÂRLILIK
        S["ROE_TTM"] = bol(ni4, EQ(), True); S["ROA_Q"] = bol(NI(0), AT(1), True)
        S["D_ASSET_TURN"] = gel(lambda t: bol(AO.ttm(t), AT(0), True) - bol(AO.ttm(t, 4), AT(4), True))
        S["SALES_ACCEL"] = gel(lambda t: bol(AO.q(t, 0), (AO.q(t, 1) + AO.q(t, 2)) / 2.0, True))
        ek["REV_YOY"] = gel(lambda t: np.where(AO.q(t, 0) > 0, bol(AO.q(t, 0), AO.q(t, 4), True) - 1.0, np.nan))
        S["ACCRUALS"] = bol(NIy(0) - ocf0, ort_at_y, True); S["GP_A"] = bol(gp4, AT(), True); S["OP_BE"] = bol(oi4, EQ(), True)
        S["CBOP_A"] = bol(ocf0, ATy(0), True); S["OPLEV"] = bol(rev4 - oi4, AT(), True)
        S["NOA"] = bol(s0(LTD()) + EQ() - NAKIT, AT(4), True)
        S["TAX_CHG"] = bol(AO.q("IncomeTaxExpenseBenefit", 0) - AO.q("IncomeTaxExpenseBenefit", 4), AT(4), True)
        # F_SCORE (yıllık)
        roa0, roa1 = bol(NIy(0), ATy(0), True), bol(NIy(1), ATy(1), True)
        LTDy = lambda g: s0(ilk(AO.ya("LongTermDebt", g), AO.ya("LongTermDebtNoncurrent", g)))  # noqa: E731
        kal0, kal1 = bol(LTDy(0), ATy(0), True), bol(LTDy(1), ATy(1), True)
        cari0, cari1 = bol(AO.ya("AssetsCurrent", 0), AO.ya("LiabilitiesCurrent", 0), True), bol(AO.ya("AssetsCurrent", 1), AO.ya("LiabilitiesCurrent", 1), True)
        bm0, bm1 = bol(GPy(0), REVy(0), True), bol(GPy(1), REVy(1), True); dv0, dv1 = bol(REVy(0), ATy(0), True), bol(REVy(1), ATy(1), True)
        olcu = [(roa0 > 0, np.isfinite(roa0)), (ocf0 > 0, nakit_tablo), (roa0 > roa1, np.isfinite(roa0) & np.isfinite(roa1)),
                (ocf0 > NIy(0), nakit_tablo & np.isfinite(NIy(0))), (kal0 < kal1, np.isfinite(kal0) & np.isfinite(kal1)),
                (cari0 > cari1, np.isfinite(cari0) & np.isfinite(cari1)), (~(s0(IHR) > 0), nakit_tablo),
                (bm0 > bm1, np.isfinite(bm0) & np.isfinite(bm1)), (dv0 > dv1, np.isfinite(dv0) & np.isfinite(dv1))]
        top = sum((a & b).astype(float) for a, b in olcu); nh = sum(b.astype(float) for _a, b in olcu)
        S["F_SCORE"] = np.where((nh >= pr["fscore_min"]) & np.isfinite(roa0), top * 9.0 / np.maximum(nh, 1) + 0.001 * np.clip(np.nan_to_num(roa0), -1, 1), np.nan)
        # YATIRIM / İHRAÇ
        S["ASSET_G"] = bol(AT(0), AT(4), True) - 1.0
        S["BE_G"] = np.where(EQ(0) > 0, bol(EQ(0), EQ(4), True) - 1.0, np.nan)
        for kod, ay_, ayk in (("NSI_1Y", 12, pr["nsi1_aykiri"]), ("NSI_5Y", 60, pr["nsi5_aykiri"])):
            once = kay(SH, ay_); ko = np.vstack([np.zeros((min(ay_, M), N), np.int8), pk[:max(M - ay_, 0)]])
            o_ = bol(SH, once, True); ok = np.isfinite(o_) & (o_ > 0) & (o_ <= ayk) & (o_ >= 1.0 / ayk) & (pk == ko) & (pk > 0)
            S[kod] = np.where(ok, np.log(np.where(ok, o_, 1.0)), np.nan)
        S["NEF"] = bol(np.where(nakit_tablo, s0(IHR) - s0(GERI) - s0(TEM), np.nan), ort_at_y, True)
        S["NDF_BS"] = bol(LTD(0) - LTD(4), (AT(0) + AT(4)) / 2.0, True)
        S["CAPEX_G"] = bol(CAPEX(0), (CAPEX(1) + CAPEX(2)) / 2.0, True) - 1.0
        # SÜRPRİZ (temel)
        def sue(al: Callable[[int], np.ndarray]) -> np.ndarray:
            f_ = np.stack([al(k) - al(k + 4) for k in range(pr["sue_n"])]); sd = f_.std(axis=0, ddof=1)
            return np.where(np.isfinite(sd) & (sd > 0), f_[0] / np.where(sd > 0, sd, 1.0), np.nan)
        S["SUE_SRW"] = sue(NI); S["REV_SURP"] = gel(lambda t: sue(lambda g: AO.q(t, g)))
        d = [NI(k) - NI(k + 4) for k in range(pr["streak_max"])]; i0 = np.sign(d[0]); canli = np.isfinite(d[0]) & (i0 != 0); seri_ = canli.astype(float)
        for k in range(1, pr["streak_max"]):
            canli = canli & np.isfinite(d[k]) & (np.sign(d[k]) == i0); seri_ += canli
        S["EARN_STREAK"] = np.where(np.isfinite(d[0]), i0 * seri_, np.nan)
        # BOYUT / DEVİR
        S["SIZE_ME"] = np.where(PD > 0, np.log(np.where(PD > 0, PD, 1.0)), np.nan)
        S["TURN_12M"] = bol(ara["v252"], SH, True)
        # SIKINTI
        S["RUNWAY"] = bol(-ocf0, NAKIT, True)
        ch = pr["chs"]; MTA = PD + LT(); fi = 0.5

        def kirp(X: np.ndarray) -> np.ndarray:
            out = np.full(X.shape, np.nan)
            for m in range(M):
                v = X[m][U[m] & np.isfinite(X[m])]
                if len(v) >= 20:
                    a_, b_ = np.percentile(v, ch["kirp"]); out[m] = np.clip(X[m], a_, b_)
            return out
        nim = sum(fi ** k * bol(NI(k), MTA, True) for k in range(4)) / sum(fi ** k for k in range(4))
        mk = ara.get("mkt_ay"); rm = ara["rm"]
        lr = np.log1p(np.where(rm > -1, rm, np.nan)); lu = np.where(U, lr, np.nan)
        piy = np.log1p(mk)[:, None] if mk is not None else (np.nansum(lu, axis=1) / np.maximum(np.isfinite(lu).sum(axis=1), 1))[:, None]
        ex = lr - piy
        f1 = 2.0 ** (-1.0 / 3.0); exavg = sum(f1 ** k * kay(ex, k) for k in range(12)) * (1 - f1) / (1 - f1 ** 12)
        topPD = np.nansum(np.where(U, PD, np.nan), axis=1)[:, None]
        beadj = EQ() + 0.1 * (PD - EQ()); mb = np.where(np.isfinite(beadj), bol(PD, np.where(beadj > 0, beadj, 1.0), True), np.nan)
        fiyat = np.where(P["fiyat_o"] > 0, np.log(np.minimum(np.where(P["fiyat_o"] > 0, P["fiyat_o"], 1.0), ch["fiyat_tavan"])), np.nan)
        S["CHS_FAIL"] = (ch["sabit"] + ch["NIMTAAVG"] * kirp(nim) + ch["TLMTA"] * kirp(bol(LT(), MTA, True)) + ch["EXRETAVG"] * kirp(exavg)
                         + ch["SIGMA"] * kirp(ara["sigma"]) + ch["RSIZE"] * kirp(np.where((PD > 0) & (topPD > 0), np.log(np.where(PD > 0, PD, 1.0) / np.where(topPD > 0, topPD, 1.0)), np.nan))
                         + ch["CASHMTA"] * kirp(bol(NAKIT, MTA, True)) + ch["MB"] * kirp(mb) + ch["PRICE"] * fiyat)
        oh = pr["ohlson"]; TA = ATy(0); TL = ilk(AO.ya("Liabilities", 0), TA - AO.ya("StockholdersEquity", 0))
        CA, CL = AO.ya("AssetsCurrent", 0), AO.ya("LiabilitiesCurrent", 0); n0, n1 = NIy(0), NIy(1)
        S["O_SCORE"] = (oh["sabit"] + oh["lnTA"] * np.where(TA > 0, np.log(np.where(TA > 0, TA, 1.0)), np.nan) + oh["TLTA"] * bol(TL, TA, True)
                        + oh["WCTA"] * bol(CA - CL, TA, True) + oh["CLCA"] * bol(CL, CA, True) + oh["OENEG"] * np.where(np.isfinite(TL) & np.isfinite(TA), (TL > TA).astype(float), np.nan)
                        + oh["NITA"] * bol(n0, TA, True) + oh["FUTL"] * bol(ocf0, TL, True) + oh["INTWO"] * np.where(np.isfinite(n0) & np.isfinite(n1), ((n0 < 0) & (n1 < 0)).astype(float), np.nan)
                        + oh["CHIN"] * bol(n0 - n1, np.abs(n0) + np.abs(n1), True))
    return S, ek


def _k60_sinyal_olay(D: Dict[str, Any], P: Dict[str, Any], E: Dict[str, Any], ara: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """Başvuru, bölünme, temettü ve açıklama günü sinyalleri (EAR_ANN, EAR_FILE, EAR_VOL, EA_MONTH, DIV_MONTH, NT_LATE, ACT_13D, EVT ailesi)."""
    pr = E["param"]; M, N = P["U"].shape; mp = P["me_pos"]; mt = P["mtD"]; gD = P["gunD"]; G = len(gD); S: Dict[str, np.ndarray] = {}; Sm = P["sembol"]
    bos = lambda: np.full((M, N), np.nan)  # noqa: E731
    basv = D.get("basvuru") or {}; al = lambda g, j: (basv.get(g) or [None] * N)[j]  # noqa: E731
    for k in ("EAR_ANN", "EAR_FILE", "EAR_VOL", "EA_MONTH", "DIV_MONTH", "E_IPO_3Y", "E_SPLIT", "E_RSPLIT", "E_DIV_INIT", "E_DIV_OMIT"):
        S[k] = bos()
    for k in pr["bayrak_gun"]:
        S[k] = bos()
    A5 = P["A5"]; V = D["V"]; mkt = ara.get("mkt_gun"); cik = D.get("cik") or [None] * N
    ayD = lambda t: np.asarray(t, "datetime64[M]").astype(np.int64)  # noqa: E731  (ay sırası; 1970-01 = 0)
    ay_no = ayD(mt)
    gun_grubu = {"NT_LATE": "NT", "ACT_13D": "13D", "E_S3": "S3", "E_424B5": "424B5", "E_TENDER_SELF": "TOI"}
    bol = D.get("bolunme") or {}; tem = D.get("temettu") or {}; ilk_islem = np.asarray(D.get("ilk_islem", np.full(N, np.datetime64("NaT", "D"))), "datetime64[D]")
    ilk_fiyat = np.full(N, np.datetime64("NaT", "D")); var = np.isfinite(D["C"])
    for j in range(N):
        i = np.flatnonzero(var[:, j])
        if len(i):
            ilk_fiyat[j] = gD[i[0]]
    og = np.timedelta64(int(pr["olay_gun"]), "D")

    def say(t: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Sıralı t içinde (a, b] aralığındaki gün sayısı (a, b: ay başına)."""
        return np.searchsorted(t, b, side="right") - np.searchsorted(t, a, side="right")

    def tepki(olay: np.ndarray, j: int, hacim: bool) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Olay günleri (olayla hizalı çıktı) -> (pencere sonu sırası, tepki, hacim oranı). Pencere = olaydan önceki, olay ve sonraki işlem
        günü (olay işlem günü değilse sonraki ilk işlem günü); penceresi veriye sığmayan olayın değeri NaN."""
        p0 = np.searchsorted(gD, olay, side="left"); ok = (p0 >= 2) & (p0 + 1 <= G - 1); pc = np.clip(p0, 2, max(G - 2, 2))
        a = A5[:, j]; tp = np.full(len(p0), np.nan); ev = np.full(len(p0), np.nan)
        if not ok.any() or G < 4:
            return p0 + 1, tp, ev
        with np.errstate(invalid="ignore", divide="ignore"):
            hisse = a[pc + 1] / a[pc - 2] - 1
            piyasa = (1 + mkt[pc - 1]) * (1 + mkt[pc]) * (1 + mkt[pc + 1]) - 1 if mkt is not None else np.zeros(len(pc))
            tp = np.where(ok, hisse - piyasa, np.nan)
            if hacim:
                v = V[:, j]; ng = int(pr["evol_gun"])
                for k in np.flatnonzero(ok):
                    q_ = pc[k]; blok = v[max(0, q_ - ng):q_]; n_ = int(np.isfinite(blok).sum())
                    if n_ >= pr["evol_min"] and np.isfinite(v[q_]) and np.nansum(blok) > 0:
                        ev[k] = v[q_] / (np.nansum(blok) / n_)
        return p0 + 1, tp, ev

    def son_olay(bilinme: np.ndarray, son: np.ndarray, deger: np.ndarray) -> np.ndarray:
        """Bilinme günü (başvuru günü) < t olan, değeri olan EN SON olayın değeri; olayın tepki penceresi t'ye kadar bitmiş ve son
        ear_pencere işlem günü içinde olmalı (K59 k59_pead_sinyal kuralı + 'başvuru t'den önce' şartı). bilinme sıralı olmalı."""
        out = np.full(M, np.nan); g = np.isfinite(deger)
        if not g.any():
            return out
        f_, s, d = bilinme[g], son[g], deger[g]; i = np.searchsorted(f_, mt, side="left") - 1; ic = np.maximum(i, 0)
        ok = (i >= 0) & (s[ic] <= mp) & (s[ic] > mp - pr["ear_pencere"])
        out[ok] = d[ic][ok]
        return out
    for j in range(N):
        K_, Q_ = al("K", j), al("Q", j)
        don = None
        if K_ is not None or Q_ is not None:
            don = np.union1d(K_ if K_ is not None else np.array([], "datetime64[D]"), Q_ if Q_ is not None else np.array([], "datetime64[D]")).astype("datetime64[D]")
        if don is not None and len(don):
            dv = k60_duyuru_gunu(don, al("8K", j), pr["ear_8k_gun"])
            s1, e1, v1 = tepki(dv, j, True); S["EAR_ANN"][:, j] = son_olay(don, s1, e1); S["EAR_VOL"][:, j] = son_olay(don, s1, v1)
            s2, e2, _v = tepki(don, j, False); S["EAR_FILE"][:, j] = son_olay(don, s2, e2)
            # EA_MONTH: hedef ay = m - 11 (t'den önce bitmiş); o aydaki d*'ların başvurusu en geç 30 gün sonra, yine t'den önce
            hedef = ay_no + 1 - 12
            S["EA_MONTH"][:, j] = np.where(ayD(don[0]) <= hedef, np.isin(hedef, np.unique(ayD(dv))).astype(float), np.nan)
        if cik[j] is not None:
            for kod, g in gun_grubu.items():
                t = al(g, j); w = np.timedelta64(int(pr["bayrak_gun"][kod]), "D")
                S[kod][:, j] = 0.0 if t is None else (np.searchsorted(t, mt, side="left") - np.searchsorted(t, mt - w, side="left") > 0).astype(float)
        if not np.isnat(ilk_islem[j]):
            S["E_IPO_3Y"][:, j] = ((mt - ilk_islem[j]) <= np.timedelta64(int(pr["ipo_gun"]), "D")).astype(float)
        b = bol.get(Sm[j]); S["E_SPLIT"][:, j] = 0.0; S["E_RSPLIT"][:, j] = 0.0
        if b is not None:
            bt = b[0].astype("datetime64[D]")
            for kod, sec in (("E_SPLIT", b[1] >= 2.0), ("E_RSPLIT", b[1] < 1.0)):
                if sec.any():
                    S[kod][:, j] = (say(bt[sec], mt - og, mt) > 0).astype(float)
        t = tem.get(Sm[j]); t = t if t is not None else np.array([], "datetime64[D]")
        ta = np.unique(ayD(t)) if len(t) else np.array([], np.int64)
        S["DIV_MONTH"][:, j] = (np.isin(ay_no + 1 - 3, ta) | np.isin(ay_no + 1 - 6, ta) | np.isin(ay_no + 1 - 12, ta)).astype(float)
        if not np.isnat(ilk_fiyat[j]):
            n1 = say(t, mt - og, mt); n2 = say(t, mt - 3 * og, mt - og); n3 = say(t, mt - 2 * og, mt - og)
            with np.errstate(invalid="ignore"):
                S["E_DIV_INIT"][:, j] = np.where(ilk_fiyat[j] <= mt - 3 * og, ((n1 >= 1) & (n2 == 0)).astype(float), np.nan)
                S["E_DIV_OMIT"][:, j] = np.where(ilk_fiyat[j] <= mt - 2 * og, ((n3 >= 2) & (n1 == 0)).astype(float), np.nan)
    return S


def _k60_sinyal_sektor(D: Dict[str, Any], P: Dict[str, Any], E: Dict[str, Any], ara: Dict[str, np.ndarray], PD: np.ndarray) -> Dict[str, np.ndarray]:
    """IND_MOM_6 ve IND_LEAD_BIG (SIC 2 hane)."""
    pr = E["param"]; M, N = P["U"].shape; U = P["U"]; sic = np.asarray(D.get("sic", np.full(N, -1)), int); s2 = np.where(sic >= 0, sic // 100, -1)
    S = {"IND_MOM_6": np.full((M, N), np.nan), "IND_LEAD_BIG": np.full((M, N), np.nan)}; g6 = ara["getiri6"]; rm = ara["rm"]; PDo = _k60_kay(PD, 1)
    for m in range(M):
        ok = U[m] & (s2 >= 0) & np.isfinite(g6[m])
        if ok.any():
            n = np.bincount(s2[ok], minlength=100); t = np.bincount(s2[ok], weights=g6[m, ok], minlength=100)
            deger = np.where(n >= pr["sektor_min"], t / np.maximum(n, 1), np.nan)
            S["IND_MOM_6"][m] = np.where(U[m] & (s2 >= 0), deger[np.maximum(s2, 0)], np.nan)
        ok = U[m] & (s2 >= 0) & np.isfinite(PDo[m]) & np.isfinite(rm[m])
        for k in np.unique(s2[ok]):
            j = np.flatnonzero(ok & (s2 == k))
            if len(j) < pr["lead_min"]:
                continue
            nb = max(1, int(round(pr["lead_pay"] * len(j)))); sira = j[np.argsort(-PDo[m, j], kind="stable")]
            S["IND_LEAD_BIG"][m, sira[nb:]] = float(rm[m, sira[:nb]].mean())
    return S


def k60_yuzde_sira(X: np.ndarray, U: np.ndarray) -> np.ndarray:
    return K59.k59_yuzde_sira(X, U)


def k60_sinyaller(D: Dict[str, Any], P: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
    """Kütüphanedeki bütün sinyaller (ay x hisse; HAM ölçü, yön UYGULANMAMIŞ; uygun olmayan / verisi olmayan NaN) ve bileşikler
    ('yüksek = iyi' sıra ortalaması). Yalnız t ve öncesi bilgi. Döner (sinyaller + bileşikler, ek: pay kaynağı, ç0, y0, PD, REV_YOY)."""
    E = E or K60_ESIK; U = P["U"]; tn = k60_tanim(E)
    Sf, ara = _k60_sinyal_fiyat(D, P, E); St, ek = _k60_sinyal_temel(D, P, E, ara); So = _k60_sinyal_olay(D, P, E, ara)
    Ss = _k60_sinyal_sektor(D, P, E, ara, ek["PD"]); ham = {**Sf, **St, **So, **Ss}
    with np.errstate(invalid="ignore"):
        y1, y2 = k60_yuzde_sira(ham["MOM_12_1"], U), k60_yuzde_sira(ara["sureklilik"], U)
        ham["MOM_FIP"] = (y1 + y2) / 2.0
    maske = lambda X: np.where(U & np.isfinite(X), X, np.nan)  # noqa: E731
    Sd = {k: maske(ham[k]) if k in ham else np.full(U.shape, np.nan) for k in tn}
    yonlu = {k: (-1.0 if tn[k]["yon"] == "-" else 1.0) * Sd[k] for k in tn}
    for k, v in E["ek_bilesen"].items():
        yonlu[k] = maske(ek[k]) if k in ek else np.full(U.shape, np.nan)
    for b, t in E["bilesik"].items():
        Sd[b] = K59.k59_bilesik(yonlu, U, [u for u in t["uye"] if u in yonlu], t["min"])
    ek["bilesen"] = {k: yonlu[k] for k in E["ek_bilesen"]}
    return Sd, ek


# ---------------------------------------------------------------- 5) UÇLAR, R1, R2
def k60_bag(shape: Tuple[int, int], E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Eşitlik bozma matrisi (ay x hisse; sabit tohum): aynı değerli hisselerin sırası bununla belirlenir."""
    return np.random.default_rng((E or K60_ESIK)["portfoy"]["bag_tohum"]).random(shape)


def k60_sira(S: np.ndarray, U: np.ndarray, bag: np.ndarray) -> np.ndarray:
    """Ay içi sıra numarası (0 = en küçük): uygun ve değeri olan hisseler (değer, eşitlikte bag) anahtarıyla sıralanır; ötekiler NaN."""
    out = np.full(S.shape, np.nan)
    for m in range(len(S)):
        j = np.flatnonzero(U[m] & np.isfinite(S[m]))
        if len(j):
            out[m, j[np.lexsort((bag[m, j], S[m, j]))]] = np.arange(len(j), dtype=float)
    return out


def k60_uclar(S: np.ndarray, yon: str, tur: str, P: Dict[str, Any], bag: np.ndarray, E: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
    """Bir sinyalin uçları. Sürekli: ÜST = beklenen yöne göre en iyi %dilim, ALT = en kötü %dilim (sinyali olan uygun hisseler arasında;
    K58 k58_ust_dilim). Bayrak: bayraklı uygun hisselerin tamamı; yön '+' ise ÜST, '-' ise ALT. Döner {uç: {'sec', 'say', 'min', 'tur'}}."""
    pf = (E or K60_ESIK)["portfoy"]; U = P["U"]
    if tur == "bayrak":
        with np.errstate(invalid="ignore"):
            b = U & np.isfinite(S) & (S > 0.5)
        return {("ALT" if yon == "-" else "UST"): {"sec": b, "say": b.sum(axis=1), "min": pf["min_bayrak"], "tur": tur}}
    key = k60_sira((-1.0 if yon == "-" else 1.0) * S, U, bag); Us = np.isfinite(key); say = Us.sum(axis=1)
    return {"UST": {"sec": K58.k58_ust_dilim(key, Us, pf["dilim"]), "say": say, "min": pf["min_sinyal"], "tur": tur},
            "ALT": {"sec": K58.k58_ust_dilim(-key, Us, pf["dilim"]), "say": say, "min": pf["min_sinyal"], "tur": tur}}


def k60_olcum_aylari(pm: np.ndarray, say: np.ndarray, min_n: int, tur: str) -> np.ndarray:
    """Ölçüm ayları: sürekli sinyalde dönem içinde sayının ilk kez >= min_n olduğu aydan dönem sonuna (K59 kuralı); bayrakta sayı >= min_n olan aylar."""
    yeter = pm & (say >= min_n)
    if tur == "bayrak" or not yeter.any():
        return yeter
    ol = pm.copy(); ol[:np.flatnonzero(yeter)[0]] = False
    return ol


def _k60_norm_p(z: float) -> float:
    """1 - Φ(z)."""
    return 0.5 * math.erfc(z / math.sqrt(2.0)) if np.isfinite(z) else (1.0 if z == -np.inf else (0.0 if z == np.inf else np.nan))


def k60_r1(P: Dict[str, Any], sec: np.ndarray, ol: np.ndarray, donem: str, FF: Optional[pd.DataFrame] = None,
           E: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """R1 = K59 portföy cetveli v2 (K58 k58_portfoy + K59 k59_olc), dönemin ölçüm aylarında. Döner (satır, aylık getiri tablosu)."""
    E = E or K60_ESIK; R1 = E["r1"]; C = {**R1["cetvel"], "min_ay": R1["min_ay"][donem]}; U = P["U"]; me = P["ay_sonu"]; k = np.flatnonzero(ol)
    if not len(k):
        return {"ay": 0, "olculdu": False, "tutar_v2": False}, pd.DataFrame()
    Pf = K58.k58_portfoy(P["R"], sec, U, ol, R1["maliyet"]); ay = pd.PeriodIndex(me[k + 1], freq="M")
    row = K59.k59_olc(Pf, ay, FF, {"cetvel": C, "french": K59.K59_ESIK["french"]})
    nh = (sec & U)[k].sum(axis=1); t = float(row.get("t_alfa", np.nan)) if row.get("olculdu") else np.nan
    w = (sec & U)[k] / np.maximum(nh, 1)[:, None]; katki = (w * np.nan_to_num(P["R"][k])).sum(axis=0); top = float(katki.sum()); ilk3 = np.argsort(-katki)[:3]
    row.update({"ilk_ay": str(me[k[0]].date()), "son_ay": str(me[k[-1]].date()), "ort_hisse": float(nh.mean()), "bos_ay": int((nh == 0).sum()),
                "p_alfa": 2.0 * _k60_norm_p(abs(t)) if np.isfinite(t) else np.nan,
                "katki_ilk3": "; ".join(f"{P['sembol'][j]} {katki[j] / top:.0%}" for j in ilk3 if katki[j] > 0) if top > 0 else ""})
    A = pd.DataFrame({"ay_sonu": [str(x.date()) for x in me[k]], "getiri_ayi": ay.astype(str), "brut": Pf["brut"], "net": Pf["net"], "kiyas": Pf["kiyas"],
                      "devir": Pf["devir"], "n_hisse": nh, "n_evren": U[k].sum(axis=1)})
    return row, A


_K60_BOOT: Dict[Tuple[int, int, int, int], np.ndarray] = {}


def k60_blok_dizini(T: int, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Dairesel blok bootstrap ay dizini (çekiliş x T): her çekilişte ceil(T / blok) rastgele başlangıç, ardışık blok ay (T'de başa sarar),
    T aya kırpılır. Yalnız (T, blok, çekiliş, tohum)'a bağlıdır: bütün sinyaller aynı çekilişleri kullanır."""
    R2 = (E or K60_ESIK)["r2"]; anahtar = (int(T), int(R2["blok"]), int(R2["cekilis"]), int(R2["tohum"]))
    if anahtar not in _K60_BOOT:
        rng = np.random.default_rng([anahtar[3], anahtar[0]]); nb = int(math.ceil(T / anahtar[1]))
        bas = rng.integers(0, T, size=(anahtar[2], nb))
        _K60_BOOT[anahtar] = ((bas[:, :, None] + np.arange(anahtar[1])[None, None, :]) % T).reshape(anahtar[2], -1)[:, :T]
    return _K60_BOOT[anahtar]


def k60_lift(kd: np.ndarray, nd: np.ndarray, kb: np.ndarray, nb: np.ndarray, E: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    """Aylık sayımlardan (uçta olay / hisse, evrende olay / hisse) havuz olasılıkları, lift ve blok bootstrap aralığı + p değerleri."""
    R2 = (E or K60_ESIK)["r2"]; kd, nd, kb, nb = (np.asarray(x, float) for x in (kd, nd, kb, nb)); T = len(kd)
    out = {"P": np.nan, "taban": np.nan, "lift": np.nan, "alt": np.nan, "ust": np.nan, "z": np.nan, "pz": np.nan, "py": np.nan}
    if not T or nd.sum() <= 0 or nb.sum() <= 0:
        return out
    Pd, Pb = kd.sum() / nd.sum(), kb.sum() / nb.sum(); out.update({"P": float(Pd), "taban": float(Pb)})
    if Pb <= 0:
        return out
    lift = Pd / Pb; out["lift"] = float(lift); ix = k60_blok_dizini(T, E)
    with np.errstate(invalid="ignore", divide="ignore"):
        Ld = kd[ix].sum(axis=1) / nd[ix].sum(axis=1); Lb = kb[ix].sum(axis=1) / nb[ix].sum(axis=1)
        L = np.where(Lb > 0, Ld / np.where(Lb > 0, Lb, 1.0), np.nan)
    g = L[np.isfinite(L)]
    if len(g) < 0.5 * len(L):
        return out
    out["alt"], out["ust"] = (float(x) for x in np.percentile(g, R2["guven"]))
    out["py"] = float((1 + (g <= 1.0).sum()) / (len(g) + 1))
    poz = g[g > 0]; sd = float(np.log(poz).std(ddof=1)) if len(poz) > 1 else np.nan
    z = (math.log(lift) / sd) if (lift > 0 and sd and sd > 0) else (-np.inf if lift <= 0 else np.nan)
    out["z"] = float(z); out["pz"] = float(_k60_norm_p(z))
    return out


def _k60_taban(P: Dict[str, Any], h: int, E: Dict[str, Any]) -> Dict[str, Any]:
    """Evrenin (taban) aylık sayımları, ufuk h için (panelde saklanır)."""
    dep = P.setdefault("_taban", {})
    if h not in dep:
        F = P["F"][h]; gec = P["U"] & np.isfinite(F); ol = E["r2"]["olay"]
        with np.errstate(invalid="ignore"):
            olay = {k: gec & ((F >= v) if v > 0 else (F <= v)) for k, v in ol.items()}
        dep[h] = {"gec": gec, "olay": olay, "nb": gec.sum(axis=1), "kb": {k: v.sum(axis=1) for k, v in olay.items()}}
    return dep[h]


def k60_r2(P: Dict[str, Any], sec: np.ndarray, ol: np.ndarray, E: Optional[Dict[str, Any]] = None,
           ufuklar: Optional[List[int]] = None) -> Tuple[List[Dict[str, Any]], pd.DataFrame]:
    """R2 = OLASILIK TABLOSU: uç (sec) ve evren için P(F >= +%100), P(>= +%50), P(<= -%50), lift, blok bootstrap aralığı, ortalama ve medyan F;
    her ufuk için bir satır. Aylar = ol içinde ileri penceresi veride biten aylar. Döner (satırlar, ana ufkun aylık sayım tablosu)."""
    E = E or K60_ESIK; R2 = E["r2"]; me = P["ay_sonu"]; M = len(me); sat = []; A = pd.DataFrame()
    for h in (ufuklar or R2["ufuk"]):
        tb = _k60_taban(P, h, E); ay = np.flatnonzero(ol & (np.arange(M) + h <= M - 1)); F = P["F"][h]
        row: Dict[str, Any] = {"ufuk": int(h), "ay": int(len(ay)), "olculdu": False}
        if len(ay):
            d = sec & tb["gec"]; nd = d.sum(axis=1)[ay]; nb = tb["nb"][ay]
            row.update({"n": int(nd.sum()), "n_evren": int(nb.sum()), "ilk_ay": str(me[ay[0]].date()), "son_ay": str(me[ay[-1]].date())})
            say = {"ay_sonu": [str(x.date()) for x in me[ay]], "n": nd, "n_evren": nb}
            for k in R2["olay"]:
                kd = (d & tb["olay"][k]).sum(axis=1)[ay]; kb = tb["kb"][k][ay]; L = k60_lift(kd, nd, kb, nb, E)
                row.update({f"{a}_{k}": v for a, v in L.items()}); say[f"k_{k}"] = kd; say[f"k_evren_{k}"] = kb
            fd = F[ay][d[ay]]; fb = F[ay][tb["gec"][ay]]
            row.update({"ort": float(fd.mean()) if len(fd) else np.nan, "medyan": float(np.median(fd)) if len(fd) else np.nan,
                        "taban_ort": float(fb.mean()) if len(fb) else np.nan, "taban_medyan": float(np.median(fb)) if len(fb) else np.nan})
            row["olculdu"] = bool(len(ay) >= R2["min_ay"] and nd.sum() >= R2["min_hisse_ay"] and np.isfinite(row.get("lift_p100", np.nan)))
            if h == R2["ana_ufuk"]:
                A = pd.DataFrame(say)
                olay_say = (d[ay] & tb["olay"]["p100"][ay]).sum(axis=0); top = int(olay_say.sum()); ilk3 = np.argsort(-olay_say)[:3]
                row["olay_ilk3"] = "; ".join(f"{P['sembol'][j]} {int(olay_say[j])}/{top}" for j in ilk3 if olay_say[j] > 0)
        sat.append(row)
    return sat, A


def k60_bh(p: Any, q: float) -> np.ndarray:
    """Benjamini-Hochberg adım-yukarı: sonlu p'ler arasında p(k) <= k / m x q sağlayan en büyük k'ya kadar olanlar True. NaN p False ve m'ye girmez."""
    p = np.asarray(p, float); out = np.zeros(len(p), bool); g = np.flatnonzero(np.isfinite(p)); m = len(g)
    if not m:
        return out
    sira = g[np.argsort(p[g], kind="stable")]; gec = p[sira] <= (np.arange(1, m + 1) / m) * q
    if gec.any():
        out[sira[:np.flatnonzero(gec)[-1] + 1]] = True
    return out


def k60_plasebo_maks(x: Any, m: int, E: Optional[Dict[str, Any]] = None) -> float:
    """'Plasebo en büyüğü' eşiği: plasebo istatistiklerinden m'lik (yerine koyarak) kümelerin en büyüğünün dağılımının %maks_yuzde dilimi."""
    Ck = (E or K60_ESIK)["coklu"]; x = np.asarray(x, float); x = x[np.isfinite(x)]
    if not len(x) or m < 1:
        return np.nan
    rng = np.random.default_rng([Ck["maks_tohum"], int(m)])
    return float(np.percentile(x[rng.integers(0, len(x), size=(Ck["maks_tekrar"], int(m)))].max(axis=1), Ck["maks_yuzde"]))


def k60_plasebo(P: Dict[str, Any], donem: str, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Plasebo: n rastgele sinyal (default_rng(tohum + i); her ay uygun hisselere rastgele sıra), ÜST uç, iki cetvelden de (R2 ana ufuk)."""
    E = E or K60_ESIK; Ck = E["coklu"]; U = P["U"]; pm = k60_donem_aylari(P, donem, 1, E); Z = []; au = E["r2"]["ana_ufuk"]
    for i in range(Ck["plasebo_n"]):
        rng = np.random.default_rng(Ck["plasebo_tohum"] + i); S = rng.random(U.shape); S[~U] = np.nan
        sec = K58.k58_ust_dilim(S, U, E["portfoy"]["dilim"])
        r1, _a = k60_r1(P, sec, pm, donem, None, E); r2 = k60_r2(P, sec, pm, E, [au])[0][0]
        Z.append({"plasebo": i, **{k: r1.get(k) for k in ("ay", "olculdu", "yillik_fazla", "nw_t", "alfa_yillik", "t_alfa", "tutar_v2", "brut_t_alfa", "brut_tutar_v2")},
                  **{f"r2_{k}": r2.get(k) for k in ("ay", "olculdu", "lift_p100", "alt_p100", "z_p100", "lift_m50", "alt_m50", "z_m50", "lift_p50")}})
    return pd.DataFrame(Z)


# ---------------------------------------------------------------- 6) BİRLEŞİK OLASILIK MODELİ (bilgi)
def k60_lojistik(X: np.ndarray, y: np.ndarray, ridge: float, tur: int) -> np.ndarray:
    """Lojistik regresyon (Newton / IRLS; sabit + katsayılar; sırt cezası sabite uygulanmaz). Döner [sabit, b1, ...]."""
    A = np.column_stack([np.ones(len(X)), X]); w = np.zeros(A.shape[1]); ceza = np.r_[0.0, np.full(A.shape[1] - 1, float(ridge))]
    if len(y) and 0 < y.mean() < 1:
        w[0] = math.log(y.mean() / (1 - y.mean()))
    for _ in range(int(tur)):
        p = 1.0 / (1.0 + np.exp(-np.clip(A @ w, -30, 30))); g = A.T @ (y - p) - ceza * w
        H = A.T @ (A * (p * (1 - p))[:, None]) + np.diag(ceza)
        try:
            adim = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            adim = np.linalg.lstsq(H, g, rcond=None)[0]
        w = w + adim
        if np.abs(adim).max() < 1e-9:
            break
    return w


def k60_model_girdi(Sd: Dict[str, np.ndarray], E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Model girdileri (ay x hisse x girdi): aile bileşikleri; eksik değer 'eksik' (nötr sıra)."""
    Md = (E or K60_ESIK)["model"]
    return np.stack([np.where(np.isfinite(Sd[k]), Sd[k], Md["eksik"]) for k in Md["girdi"]], axis=2)


def k60_model_skor(Sd: Dict[str, np.ndarray], U: np.ndarray, kat: Any, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Dondurulmuş katsayılarla tahmin olasılığı (ay x hisse; uygun olmayan NaN)."""
    kat = np.asarray(kat, float); X = k60_model_girdi(Sd, E)
    return np.where(U, 1.0 / (1.0 + np.exp(-np.clip(kat[0] + X @ kat[1:], -30, 30))), np.nan)


def k60_kalibrasyon(p: np.ndarray, y: np.ndarray, dilim: int) -> pd.DataFrame:
    """Tahmin olasılığına göre eşit sayılı dilimler: ortalama tahmin, gerçekleşen oran, gözlem."""
    if not len(p):
        return pd.DataFrame(columns=["dilim", "n", "tahmin", "gerceklesen"])
    sira = np.argsort(p, kind="stable"); par = np.array_split(sira, int(dilim))
    return pd.DataFrame([{"dilim": i + 1, "n": len(ix), "tahmin": float(p[ix].mean()), "gerceklesen": float(y[ix].mean())} for i, ix in enumerate(par) if len(ix)])


def _k60_model_gozlem(P: Dict[str, Any], donem: str, E: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
    """Modelin gözlemleri: dönemin oluşum aylarındaki, ileri getirisi olan uygun hisse-aylar (maske) ve hedef (F >= eşik)."""
    Md = E["model"]; h = Md["ufuk"]; pm = k60_donem_aylari(P, donem, h, E); tb = _k60_taban(P, h, E)
    return tb["gec"] & pm[:, None], tb["olay"][Md["hedef"]]


# ---------------------------------------------------------------- 7) DÖNEM ÖLÇÜMÜ, SEÇİM, GEÇİŞ
def k60_satirlar(E: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Ölçülecek bütün (kod, yön, tür, aile, R1 ailesinde hangi uçlar) satırları: kütüphane + bileşikler."""
    E = E or K60_ESIK; out = []
    for r in E["kutuphane"]:
        r1 = ["UST", "ALT"] if r["yon"] == "?" else (["ALT" if r["yon"] == "-" else "UST"] if r["tur"] == "bayrak" else ["UST"])
        out.append({"kod": r["kod"], "yon": "+" if r["yon"] == "?" else r["yon"], "yon_kayit": r["yon"], "tur": r["tur"], "aile": r["aile"], "r1_uc": r1, "sinif": "sinyal"})
    for k, v in E["bilesik"].items():
        out.append({"kod": k, "yon": "+", "yon_kayit": "+", "tur": "surekli", "aile": v["rol"], "r1_uc": ["UST"], "sinif": "bilesik"})
    return out


def k60_donem_olc(P: Dict[str, Any], Sd: Dict[str, np.ndarray], donem: str, FF: Optional[pd.DataFrame] = None, E: Optional[Dict[str, Any]] = None,
                  girdiler: Optional[set] = None, ek_satir: Optional[List[Dict[str, Any]]] = None, plasebo: bool = True) -> Dict[str, Any]:
    """Bir dönemin ölçümü: her (sinyal, uç) için R1 ve R2 (üç ufuk) + plasebo. girdiler verilirse yalnız o (kod, uç) çiftleri."""
    E = E or K60_ESIK; U = P["U"]; bag = k60_bag(U.shape, E); pm = k60_donem_aylari(P, donem, 1, E); r1s, r2s, a1, a2 = [], [], [], []
    for s in k60_satirlar(E) + list(ek_satir or []):
        kod = s["kod"]
        if kod not in Sd or (girdiler is not None and not any((kod, t) in girdiler for t in ("UST", "ALT"))):
            continue
        for taraf, u in k60_uclar(Sd[kod], s["yon"], s["tur"], P, bag, E).items():
            if girdiler is not None and (kod, taraf) not in girdiler:
                continue
            ol = k60_olcum_aylari(pm, u["say"], u["min"], u["tur"]); kim = {"sinyal": kod, "taraf": taraf, "aile": s["aile"], "yon": s["yon_kayit"], "tur": s["tur"], "sinif": s["sinif"]}
            row, A = k60_r1(P, u["sec"], ol, donem, FF, E)
            r1s.append({**kim, "aile_r1": bool(taraf in s["r1_uc"] and s["sinif"] != "model"), "ort_sinyal_n": float(u["say"][ol].mean()) if ol.any() else np.nan, **row})
            if len(A):
                a1.append(A.assign(sinyal=kod, taraf=taraf))
            sat, A2 = k60_r2(P, u["sec"], ol, E)
            r2s += [{**kim, "aile_r2": bool(s["sinif"] != "model"), **x} for x in sat]
            if len(A2):
                a2.append(A2.assign(sinyal=kod, taraf=taraf))
    R1 = pd.DataFrame(r1s); R2 = pd.DataFrame(r2s)
    for X, kol in ((R1, ("olculdu", "tutar_v2", "t_alfa", "p_alfa", "yillik_fazla", "alfa_yillik", "nw_t", "brut_t_alfa", "brut_yillik_fazla", "brut_alfa_yillik")), (R2, ("olculdu", "lift_p100", "alt_p100", "pz_p100", "lift_m50", "alt_m50", "pz_m50"))):
        for k in kol:
            if k not in X:
                X[k] = np.nan if k != "olculdu" else False
    return {"r1": R1, "r2": R2, "aylik": pd.concat(a1, ignore_index=True) if a1 else pd.DataFrame(), "r2_aylik": pd.concat(a2, ignore_index=True) if a2 else pd.DataFrame(),
            "plasebo": k60_plasebo(P, donem, E) if plasebo else None}


def _k60_dogru(s: Any) -> pd.Series:
    return pd.Series(s).astype(str).str.strip().str.lower().isin(["true", "1", "1.0"])


def k60_secim(R1: pd.DataFrame, R2: pd.DataFrame, Pl: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """KEŞİF seçimi (ön kayıt §6): BH + plasebo en büyüğü eşiği (R1 artı yön: sinyalin NET t(alfa)'sı > plasebo BRÜT t en büyüğü; R1 eksi yön:
    sinyalin BRÜT t(alfa)'sı < -(plasebo -brüt t en büyüğü); R2; R2K) ya da
    t(alfa) > t_dogrudan (eksi yönde brüt t < -t_dogrudan). Döner: R1 / R2 tablolarına eklenen sütunlar (yerinde), eşikler ve KEŞİF-SEÇİLİ
    (sinyal, uç) listesi."""
    E = E or K60_ESIK; Ck = E["coklu"]; au = E["r2"]["ana_ufuk"]
    R1["olculdu"] = _k60_dogru(R1.olculdu).to_numpy(); R2["olculdu"] = _k60_dogru(R2.olculdu).to_numpy()
    f1 = (R1.aile_r1.astype(bool) & R1.olculdu & np.isfinite(R1.p_alfa.astype(float))).to_numpy(); m1 = int(f1.sum())
    R1["bh_r1"] = False; R1.loc[f1, "bh_r1"] = k60_bh(R1.p_alfa.astype(float).to_numpy()[f1], Ck["bh_q"])
    f2 = ((R2.ufuk == au) & R2.aile_r2.astype(bool) & R2.olculdu).to_numpy(); m2 = int(f2.sum())
    for ad, kol in (("bh_r2", "pz_p100"), ("bh_r2k", "pz_m50")):
        R2[ad] = False; R2.loc[f2, ad] = k60_bh(R2[kol].astype(float).to_numpy()[f2], Ck["bh_q"])
    yp_net = float(_k60_dogru(Pl.tutar_v2).mean()); yp_brut = float(_k60_dogru(Pl.brut_tutar_v2).mean())
    with np.errstate(invalid="ignore"):
        yp_r2 = float((Pl.r2_alt_p100.astype(float) > 1).mean()); yp_r2k = float((Pl.r2_alt_m50.astype(float) > 1).mean())
    esik = {"m_r1": m1, "m_r2": m2, "t_arti": k60_plasebo_maks(Pl.brut_t_alfa.astype(float), m1, E), "t_eksi_brut": k60_plasebo_maks(-Pl.brut_t_alfa.astype(float), m1, E),
            "lift_p100": k60_plasebo_maks(Pl.r2_lift_p100, m2, E),
            "lift_m50": k60_plasebo_maks(Pl.r2_lift_m50, m2, E), "yp_net": yp_net, "yp_brut": yp_brut, "yp_r2": yp_r2, "yp_r2k": yp_r2k,
            "r1_acik": bool(max(yp_net, yp_brut) <= Ck["yp_esik"]), "r2_aralik_dar": bool(yp_r2 > Ck["yp_esik"]), "r2k_aralik_dar": bool(yp_r2k > Ck["yp_esik"]),
            "plasebo_maks_brut_t": float(np.nanmax(Pl.brut_t_alfa.astype(float))), "plasebo_maks_net_t": float(np.nanmax(Pl.t_alfa.astype(float))), "plasebo_min_brut_t": float(np.nanmin(Pl.brut_t_alfa.astype(float))), "plasebo_maks_lift_p100": float(np.nanmax(Pl.r2_lift_p100.astype(float))),
            "plasebo_maks_lift_m50": float(np.nanmax(Pl.r2_lift_m50.astype(float)))}
    t = R1.t_alfa.astype(float).to_numpy(); tb = R1.brut_t_alfa.astype(float).to_numpy(); bh = R1.bh_r1.to_numpy()
    with np.errstate(invalid="ignore"):
        arti = f1 & esik["r1_acik"] & ((bh & (t > esik["t_arti"])) | (t > Ck["t_dogrudan"]))
        eksi = f1 & esik["r1_acik"] & ~arti & ((bh & (-tb > esik["t_eksi_brut"])) | (-tb > Ck["t_dogrudan"]))
        R1["secili_r1"] = arti | eksi; R1["yon_r1"] = np.where(arti, 1, np.where(eksi, -1, 0))
        R2["secili_r2"] = f2 & R2.bh_r2.to_numpy() & (R2.lift_p100.astype(float).to_numpy() > esik["lift_p100"])
        R2["secili_r2k"] = f2 & R2.bh_r2k.to_numpy() & (R2.lift_m50.astype(float).to_numpy() > esik["lift_m50"])
    yol: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for r in R1[R1.secili_r1].itertuples():
        yol.setdefault((r.sinyal, r.taraf), {"yol": []})["yol"].append("R1"); yol[(r.sinyal, r.taraf)]["yon_r1"] = int(r.yon_r1)
    for ad, kod in (("secili_r2", "R2"), ("secili_r2k", "R2K")):
        for r in R2[R2[ad]].itertuples():
            yol.setdefault((r.sinyal, r.taraf), {"yol": []})["yol"].append(kod)
    secili = [{"sinyal": k[0], "taraf": k[1], "yol": sorted(v["yol"]), "yon_r1": int(v.get("yon_r1", 0))} for k, v in sorted(yol.items())]
    return {"esik": esik, "secili": secili}


def k60_gecis(R1: pd.DataFrame, R2: pd.DataFrame, Pl: pd.DataFrame, girenler: List[Dict[str, Any]], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """DOĞRULAMA / KASA geçme kuralları (ön kayıt §7): R1 (net fazla > 0, alfa > 0, t(alfa) > 1,65 ve > plasebo %95'i; eksi yönlü çiftte BRÜT ayna),
    R2 (+%100 lift alt sınırı > 1 ve lift > plasebo %95'i), R2K (-%50 için aynısı). Döner: çift başına sonuç + plasebo dilimleri."""
    E = E or K60_ESIK; Dg = E["dogrulama"]; au = E["r2"]["ana_ufuk"]; y = Dg["plasebo_yuzde"]

    def dilim(s: Any, q: float) -> float:
        x = np.asarray(pd.Series(s).astype(float)); x = x[np.isfinite(x)]
        return float(np.percentile(x, q)) if len(x) else np.nan
    pl = {"t95": dilim(Pl.brut_t_alfa, y), "brut_t05": dilim(Pl.brut_t_alfa, 100 - y), "lift_p100": dilim(Pl.r2_lift_p100, y), "lift_m50": dilim(Pl.r2_lift_m50, y)}
    i1 = {(r.sinyal, r.taraf): r for r in R1.itertuples()}; i2 = {(r.sinyal, r.taraf): r for r in R2[R2.ufuk == au].itertuples()}; out = []
    sayi = lambda r, k: float(getattr(r, k, np.nan)) if r is not None and pd.notna(getattr(r, k, np.nan)) else np.nan  # noqa: E731
    evet = lambda r: r is not None and str(getattr(r, "olculdu", False)).strip().lower() in ("true", "1", "1.0")  # noqa: E731
    for g in girenler:
        k = (g["sinyal"], g["taraf"]); a, b = i1.get(k), i2.get(k); t, fz, al = sayi(a, "t_alfa"), sayi(a, "yillik_fazla"), sayi(a, "alfa_yillik")
        arti = bool(evet(a) and fz > 0 and al > 0 and t > Dg["t_tek_yon"] and t > pl["t95"])
        tb, fzb, alb = sayi(a, "brut_t_alfa"), sayi(a, "brut_yillik_fazla"), sayi(a, "brut_alfa_yillik")
        eksi = bool(evet(a) and fzb < 0 and alb < 0 and tb < -Dg["t_tek_yon"] and tb < pl["brut_t05"])
        yon = int(g.get("yon_r1", 0))
        r1 = arti and yon >= 0; ters = eksi and yon < 0
        r2 = bool(evet(b) and sayi(b, "alt_p100") > 1 and sayi(b, "lift_p100") > pl["lift_p100"])
        r2k = bool(evet(b) and sayi(b, "alt_m50") > 1 and sayi(b, "lift_m50") > pl["lift_m50"])
        out.append({"sinyal": k[0], "taraf": k[1], "yon_r1": yon, "kesif_yol": list(g.get("yol", [])), "kesif_secili": bool(g.get("kesif_secili", True)),
                    "r1": bool(r1), "r1_ters": bool(ters), "r2": r2, "r2k": r2k, "alt_m50_ustu_1": bool(evet(b) and sayi(b, "alt_m50") > 1),
                    "gecer": bool(r1 or ters or r2 or r2k)})
    return {"plasebo": pl, "sonuc": out}


def k60_etiketler(secili: List[Dict[str, Any]], dog: List[Dict[str, Any]], kasa: List[Dict[str, Any]], kesif_r2: Optional[pd.DataFrame] = None,
                  E: Optional[Dict[str, Any]] = None) -> Dict[Tuple[str, str], List[str]]:
    """Etiketler (ön kayıt §7): yalnız KEŞİF-SEÇİLİ çiftler; üç dönemin sonuçlarından. kesif_r2 verilirse KAÇINMA için KEŞİF'teki -%50 lift alt
    sınırının da > 1 olduğu denetlenir (üç dönemin üçünde)."""
    E = E or K60_ESIK; Et = E["etiket"]; d = {(x["sinyal"], x["taraf"]): x for x in dog}; k = {(x["sinyal"], x["taraf"]): x for x in kasa}; out = {}; kes_alt: Dict[Tuple[str, str], float] = {}
    if kesif_r2 is not None and len(kesif_r2):
        ana = kesif_r2[kesif_r2.ufuk == E["r2"]["ana_ufuk"]]
        kes_alt = {(r.sinyal, r.taraf): float(r.alt_m50) for r in ana.itertuples() if pd.notna(r.alt_m50)}
    for s in secili:
        a = (s["sinyal"], s["taraf"]); x, y = d.get(a), k.get(a); et = []
        if x and y:
            if "R1" in s["yol"] and s.get("yon_r1", 0) > 0 and x["r1"] and y["r1"]:
                et.append(Et["iz"])
            if "R2" in s["yol"] and x["r2"] and y["r2"]:
                et.append(Et["olasilik"])
            if "R2K" in s["yol"] and x["alt_m50_ustu_1"] and y["alt_m50_ustu_1"] and (kesif_r2 is None or kes_alt.get(a, 0.0) > 1):
                et.append(Et["kacinma"])
            if "R1" in s["yol"] and s.get("yon_r1", 0) < 0 and x["r1_ters"] and y["r1_ters"]:
                et.append(Et["ters"])
        out[a] = et
    return out


# ---------------------------------------------------------------- 8) KOŞU
_K60_MODEL_SATIR = {"kod": "ODDS_MODEL", "yon": "+", "yon_kayit": "+", "tur": "surekli", "aile": "MODEL", "r1_uc": [], "sinif": "model"}


def _k60_yuvarla(x: Any, n: int = 10) -> Any:
    """JSON'a girecek sayıları n anlamlı basamağa yuvarlar (aynı koşu -> aynı bayt); NaN / sonsuz -> None."""
    if isinstance(x, dict):
        return {k: _k60_yuvarla(v, n) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_k60_yuvarla(v, n) for v in x]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return float(f"{float(x):.{n}g}") if np.isfinite(x) else None
    return x


def _k60_meta_yaz(meta: Dict[str, Any], donem: str, cikti: Optional[str]) -> None:
    with open(_k60_meta_yol(donem, cikti), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1, default=str)


def _k60_veri_denetimi(P: Dict[str, Any], donem: str, E: Dict[str, Any]) -> Dict[str, Any]:
    """Aykırı değer denetimi (kırpma YOK; raporda görünsün): dönemin en büyük tek hisse aylık ve 12 aylık getirisi, uç sayıları."""
    U = P["U"]; k = k60_donem_aylari(P, donem, 1, E); au = E["r2"]["ana_ufuk"]; k2 = k60_donem_aylari(P, donem, au, E)
    Ru = P["R"][k][U[k]]; Ru = Ru[np.isfinite(Ru)]; Fu = P["F"][au][k2][U[k2]]; Fu = Fu[np.isfinite(Fu)]
    return {"olusum_ayi_r1": int(k.sum()), "olusum_ayi_r2": int(k2.sum()), "ort_evren": float(U[k].sum(axis=1).mean()) if k.any() else 0.0,
            "hisse_ay": int(Ru.size), "maks_aylik_getiri": float(Ru.max()) if Ru.size else None, "aylik_ust_300": int((Ru > 3.0).sum()),
            "hisse_ay_12": int(Fu.size), "maks_12ay_getiri": float(Fu.max()) if Fu.size else None, "getiri12_ust_1000": int((Fu > 10.0).sum())}


def k60_kos(donem: str, cikti: Optional[str] = None, git_sart: bool = True, demet: Optional[Dict[str, Any]] = None,
            E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Bir dönemin ölçümü. Önce: mühür + veri sha256 + ön kaydın git'e işlenmiş ve değişmemiş olması + DÖNEM SIRASI (dogrulama: kesif çıktıları
    ve git'e işlenmiş secili.json; kasa: dogrulama çıktıları, git'e işlenmiş dogrulama_gecen.json ve TEK AÇILIŞ). demet / E yalnız testler
    içindir (sentetik demet; veri sha256 doğrulaması atlanır, mühür ve sıra yine şarttır)."""
    sentetik = demet is not None; Ek = E or K60_ESIK
    if donem not in K60_DONEM:
        raise K60Hata(f"bilinmeyen dönem: {donem} (kesif | dogrulama | kasa)")
    oc = k60_onkayit_dogrula(cikti, veri=not sentetik, git=git_sart)
    once = k60_sira_denetle(donem, cikti, git_sart)
    cik = cikti or K60_YOL["cikti"]; os.makedirs(cik, exist_ok=True); t0 = time.time()
    kod_yol = os.path.join(KOK_K60, "K60.py")
    meta: Dict[str, Any] = {"surum": K60_SURUM, "donem": donem, "onkayit": oc, "isolated": bool(sys.flags.isolated), "sentetik": sentetik,
                            "kos_baslangic": _k60_simdi(), "not": [], "kod_sha256": _k60_sha(kod_yol) if os.path.exists(kod_yol) else None,
                            "surumler": {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}}
    if donem != "kesif" and once["kesif"].get("kod_sha256") != meta["kod_sha256"]:
        meta["not"].append("K60.py, KEŞİF koşusundan sonra değişmiş (kod sha256 farklı): değişiklik ana oturumca denetlenmeli ve raporda açıklanmalı")
        k60log.warning("%s", meta["not"][-1])
    if oc["zaman_utc"] and pd.Timestamp(oc["zaman_utc"]) > pd.Timestamp(meta["kos_baslangic"].replace(" UTC", "")):
        raise K60Hata("ön kayıt koşu başlangıcından sonra: sıra bozuk")
    if donem == "kasa":       # TEK AÇILIŞ: işaret, veri yüklenmeden ve hiçbir KASA sonucu hesaplanmadan ÖNCE yazılır
        _k60_json_yaz(_k60_yol("kasa_isaret", cikti), {"acilis_utc": meta["kos_baslangic"], "muhur": oc["sha"], "gecen_sha256": once["dogrulama"]["gecen_sha256"]})
    _k60_meta_yaz(meta, donem, cikti)
    D = demet if sentetik else k60_demet_yukle(oc["veri"])
    P = k60_panel(D, Ek, True); Sd, _ek = k60_sinyaller(D, P, Ek); FF = D.get("ff_aylik"); U = P["U"]
    meta["veri_denetimi"] = _k60_veri_denetimi(P, donem, Ek); meta["hisse"] = len(P["sembol"])
    k60log.info("%s: %d hisse, %d oluşum ayı (R1), uygun evren ort %.0f; sinyaller hazır (%.0f sn)", K60_DONEM_AD[donem], meta["hisse"],
                meta["veri_denetimi"]["olusum_ayi_r1"], meta["veri_denetimi"]["ort_evren"], time.time() - t0)
    Md = Ek["model"]; kal = None; yaz: Dict[str, pd.DataFrame] = {}
    if donem == "kesif":
        goz, hedef = _k60_model_gozlem(P, donem, Ek); y = hedef[goz].astype(float); kat = None
        if len(y) and 0 < y.mean() < 1:
            kat = k60_lojistik(k60_model_girdi(Sd, Ek)[goz], y, Md["ridge"], Md["tur"])
        else:
            meta["not"].append("birleşik olasılık modeli kurulamadı (KEŞİF'te hedef olayı yok ya da gözlem yok)")
    else:
        kat = once["secili"].get("model", {}).get("katsayi"); goz, hedef = _k60_model_gozlem(P, donem, Ek); y = hedef[goz].astype(float)
    ek_satir = []
    if kat is not None:
        Sd["ODDS_MODEL"] = k60_model_skor(Sd, U, kat, Ek); ek_satir = [_K60_MODEL_SATIR]
        kal = k60_kalibrasyon(Sd["ODDS_MODEL"][goz], y, Md["dilim"]).assign(donem=donem)
    if donem == "kesif":
        O = k60_donem_olc(P, Sd, donem, FF, Ek, None, ek_satir, True)
        Sc = k60_secim(O["r1"], O["r2"], O["plasebo"], Ek)
        govde = _k60_yuvarla({"muhur": oc["sha"], "esik": Sc["esik"], "secili": Sc["secili"], "bilesik": sorted(Ek["bilesik"]),
                              "model": {"girdi": list(Md["girdi"]), "katsayi": None if kat is None else [float(x) for x in kat]}})
        ys = _k60_yol("secili", cikti); yeni = json.dumps(govde, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n"
        if os.path.exists(ys):
            with open(ys, encoding="utf-8") as f:
                if f.read() != yeni:
                    raise K60Hata("secili.json zaten var ve bu koşunun sonucu onunla bayt bayt aynı değil: dosyaya dokunulmadı, koşu durdu (KEŞİF bir kez seçer)")
        meta["secili_sha256"] = _k60_json_yaz(ys, govde); meta["esik"] = Sc["esik"]; meta["secili_n"] = len(Sc["secili"])
        yaz = {"kesif_r1.csv": O["r1"], "kesif_r2.csv": O["r2"], "kesif_aylik.csv": O["aylik"], "kesif_r2_aylik.csv": O["r2_aylik"],
               K60_DOSYA["plasebo"]: O["plasebo"].assign(donem=donem)}
        sonuc: Dict[str, Any] = {"secim": Sc}
    else:
        sec = once["secili"]; meta["secili_sha256"] = once["kesif"]["secili_sha256"]
        if donem == "dogrulama":
            girenler = [{**s, "kesif_secili": True} for s in sec["secili"]]; var = {(g["sinyal"], g["taraf"]) for g in girenler}
            girenler += [{"sinyal": b, "taraf": t, "yol": [], "yon_r1": 0, "kesif_secili": False} for b in sec["bilesik"] for t in ("UST", "ALT") if (b, t) not in var]
        else:
            girenler = [{"sinyal": g["sinyal"], "taraf": g["taraf"], "yol": g.get("kesif_yol", []), "yon_r1": g.get("yon_r1", 0), "kesif_secili": g.get("kesif_secili", True)}
                        for g in once["gecen"]["gecen"]]
        girdiler = {(g["sinyal"], g["taraf"]) for g in girenler} | ({("ODDS_MODEL", "UST")} if kat is not None else set())
        O = k60_donem_olc(P, Sd, donem, FF, Ek, girdiler, ek_satir, True)
        Gc = k60_gecis(O["r1"], O["r2"], O["plasebo"], girenler, Ek); meta["plasebo_dilim"] = Gc["plasebo"]; meta["sonuc"] = Gc["sonuc"]
        meta["giren_n"] = len(girenler); meta["gecen_n"] = int(sum(x["gecer"] for x in Gc["sonuc"]))
        if donem == "dogrulama":
            meta["gecen_sha256"] = _k60_json_yaz(_k60_yol("gecen", cikti), _k60_yuvarla(
                {"muhur": oc["sha"], "secili_sha256": meta["secili_sha256"], "plasebo": Gc["plasebo"], "sonuc": Gc["sonuc"], "gecen": [x for x in Gc["sonuc"] if x["gecer"]]}))
        else:
            et = k60_etiketler(sec["secili"], once["dogrulama"].get("sonuc", []), Gc["sonuc"], _k60_oku("kesif_r2.csv", cikti), Ek)
            meta["etiket"] = [{"sinyal": a[0], "taraf": a[1], "etiket": e} for a, e in sorted(et.items())]
        yaz = {f"{donem}_r1.csv": O["r1"], f"{donem}_r2.csv": O["r2"], f"{donem}_aylik.csv": O["aylik"], f"{donem}_r2_aylik.csv": O["r2_aylik"],
               f"{donem}_plasebo.csv": O["plasebo"].assign(donem=donem)}
        sonuc = {"gecis": Gc}
    for ad, X in yaz.items():
        X.to_csv(_k60_yol(ad, cikti), index=False)
    if kal is not None:
        ym = _k60_yol("model", cikti)
        eski = pd.read_csv(ym) if os.path.exists(ym) else pd.DataFrame()
        pd.concat([eski[eski.donem != donem] if len(eski) else eski, kal], ignore_index=True).to_csv(ym, index=False)
    meta["kos_bitis"] = _k60_simdi(); meta["sure_sn"] = round(time.time() - t0); _k60_meta_yaz(meta, donem, cikti)
    return {"donem": donem, "r1": O["r1"], "r2": O["r2"], "plasebo": O["plasebo"], "meta": meta, **sonuc, "rapor": k60_rapor(cikti, Ek)}


def k60_kapsam_kos(cikti: Optional[str] = None, demet: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """YALNIZ KAPSAM SAYIMI: dönem x sinyal başına ölçülebilen oluşum ayı ve hisse sayıları, evren ve veri kaynağı payları. İleri getiri, portföy
    getirisi, olasılık ya da t HESAPLANMAZ (panel getiri=False); ön kayıt gerekmez. kapsam.csv + kapsam_ozet.json yazar."""
    Ek = E or K60_ESIK; D = demet if demet is not None else k60_demet_yukle()
    P = k60_panel(D, Ek, getiri=False); Sd, ek = k60_sinyaller(D, P, Ek); U = P["U"]; bag = k60_bag(U.shape, Ek); me = P["ay_sonu"]; sat = []
    ozet: Dict[str, Any] = {"zaman": _k60_simdi(), "hisse": len(P["sembol"]), **{k: v for k, v in (D.get("sayim") or {}).items() if k != "hisse"},
                            "cikli": int(sum(c is not None for c in (D.get("cik") or []))), "sicli": int((np.asarray(D.get("sic", []), int) >= 0).sum()),
                            "gun": int(len(D["gun"])), "ilk_gun": str(pd.Timestamp(D["gun"][0]).date()), "son_gun": str(pd.Timestamp(D["gun"][-1]).date()), "ay": int(len(me)), "evren": {}}
    T = D.get("temel")
    if T is not None:
        kq, ky = T.get("bilgi_kaynak"), T.get("ybilgi_kaynak")
        ozet["bilgi_dizin_pay"] = float((kq == 1).sum() / max((kq > 0).sum(), 1)) if kq is not None else float("nan")
        ozet["ybilgi_dizin_pay"] = float((ky == 1).sum() / max((ky > 0).sum(), 1)) if ky is not None else float("nan")
        ozet["turetilen_q4"] = int(T.get("turetilen_q4", 0))
    for donem in K60_DONEM:
        pm = k60_donem_aylari(P, donem, 1, Ek); k = np.flatnonzero(pm)
        v: Dict[str, Any] = {"ay_r1": int(pm.sum()), "ilk": str(me[k[0]].date()) if len(k) else "", "son_r1": str(me[k[-1]].date()) if len(k) else "",
                             "ort_evren": int(round(U[k].sum(axis=1).mean())) if len(k) else 0, "min_evren": int(U[k].sum(axis=1).min()) if len(k) else 0,
                             "maks_evren": int(U[k].sum(axis=1).max()) if len(k) else 0}
        for h in Ek["r2"]["ufuk"]:
            kh = np.flatnonzero(k60_donem_aylari(P, donem, h, Ek)); v[f"ay_r2_{h}"] = int(len(kh))
            if h == Ek["r2"]["ana_ufuk"]:
                v[f"son_r2_{h}"] = str(me[kh[-1]].date()) if len(kh) else ""
        if len(k):
            pk = ek["pay_kaynak"][k][U[k]]; n_ = max(len(pk), 1)
            v.update({"pay_dei": float((pk == 1).sum() / n_), "pay_cso": float((pk == 2).sum() / n_), "pay_wads": float((pk == 3).sum() / n_), "pay_yok": float((pk == 0).sum() / n_),
                      "ceyrek_bilinen": float((ek["q0"][k][U[k]] >= 0).mean()), "yil_bilinen": float((ek["y0"][k][U[k]] >= 0).mean())})
            if donem == "kesif":
                ozet.update({a: v[a] for a in ("pay_dei", "pay_cso", "pay_wads", "pay_yok")})
        ozet["evren"][donem] = v
        for s in k60_satirlar(Ek):
            uc = k60_uclar(Sd[s["kod"]], s["yon"], s["tur"], P, bag, Ek); u = uc.get("UST") or uc["ALT"]
            ol = k60_olcum_aylari(pm, u["say"], u["min"], u["tur"]); ko = np.flatnonzero(ol)
            sat.append({"sinyal": s["kod"], "aile": s["aile"], "tur": s["tur"], "yon": s["yon_kayit"], "donem": donem, "donem_ay": int(pm.sum()), "olcum_ay": int(ol.sum()),
                        "ort_n": float(u["say"][ol].mean()) if len(ko) else 0.0, "min_n": int(u["say"][ol].min()) if len(ko) else 0,
                        "ilk_ay": str(me[ko[0]].date()) if len(ko) else "", "son_ay": str(me[ko[-1]].date()) if len(ko) else ""})
    Z = pd.DataFrame(sat); cik = cikti or K60_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    Z.to_csv(_k60_yol("kapsam", cikti), index=False); _k60_json_yaz(_k60_yol("kapsam_ozet", cikti), _k60_yuvarla(ozet, 6))
    return Z


# ---------------------------------------------------------------- 9) RAPOR
def _k60_oku(ad: str, cikti: Optional[str]) -> Optional[pd.DataFrame]:
    y = _k60_yol(ad, cikti)
    try:
        return pd.read_csv(y) if os.path.exists(y) else None
    except pd.errors.EmptyDataError:
        return None


def _k60_g(r: Any, k: str) -> float:
    try:
        v = float(r[k]) if not hasattr(r, "_fields") else float(getattr(r, k))
        return v if np.isfinite(v) else np.nan
    except (KeyError, TypeError, ValueError, AttributeError):
        return np.nan


def _k60_yuzde(x: Any, n: int = 1) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return "%" + f"{v * 100:.{n}f}".replace(".", ",") if np.isfinite(v) else "—"


def _k60_lift_yaz(r: Any, olay: str) -> str:
    l, a, u = _k60_g(r, f"lift_{olay}"), _k60_g(r, f"alt_{olay}"), _k60_g(r, f"ust_{olay}")
    return "—" if not np.isfinite(l) else f"{_sy(l)} [{_sy(a)}; {_sy(u)}]"


def _k60_r2_satir(R2: Optional[pd.DataFrame], sinyal: str, taraf: str, ufuk: int) -> Optional[pd.Series]:
    if R2 is None or not len(R2):
        return None
    x = R2[(R2.sinyal == sinyal) & (R2.taraf == taraf) & (R2.ufuk == ufuk)]
    return x.iloc[0] if len(x) else None


def k60_olasilik_tablosu(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """ANA SONUÇ: seçilmiş her (sinyal, uç) için dönem dönem taban oran, P(+%100), lift ve aralığı, aynısı -%50 için (olasilik_tablosu.md)."""
    E = E or K60_ESIK; au = E["r2"]["ana_ufuk"]; ys = _k60_yol("secili", cikti)
    R2 = {d: _k60_oku(f"{d}_r2.csv", cikti) for d in K60_DONEM}
    if not os.path.exists(ys) or R2["kesif"] is None:
        metin = "# K60 olasılık tablosu\n\nKEŞİF henüz koşulmadı (`python -I K60.py kos --donem kesif`).\n"
    else:
        sec = _k60_json_oku(ys); md = _k60_meta_bitti("dogrulama", cikti) or {}; mk = _k60_meta_bitti("kasa", cikti) or {}
        et = {(x["sinyal"], x["taraf"]): x["etiket"] for x in mk.get("etiket", [])}; tn = k60_tanim(E)
        bas = ("| özellik (uç) | dönem | ay | taban P(+%100) | P(+%100) | kat (lift) [%95 aralık] | taban P(-%50) | P(-%50) | kat [%95 aralık] | ort. 12 ay | medyan | evren ort. | etiket |\n"
               "|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")

        def satirlar(ciftler: List[Tuple[str, str, str]]) -> str:
            out = []
            for s, t, not_ in ciftler:
                for d in K60_DONEM:
                    r = _k60_r2_satir(R2[d], s, t, au)
                    if r is None:
                        continue
                    ad = f"{s} ({'ÜST' if t == 'UST' else 'ALT'})" + (f" — {tn[s]['tanim'][:60]}" if s in tn and d == "kesif" else "")
                    out.append(f"| {ad} | {K60_DONEM_AD[d]} | {int(_k60_g(r, 'ay')) if np.isfinite(_k60_g(r, 'ay')) else '—'} | {_k60_yuzde(_k60_g(r, 'taban_p100'))} | {_k60_yuzde(_k60_g(r, 'P_p100'))} | "
                               f"{_k60_lift_yaz(r, 'p100')} | {_k60_yuzde(_k60_g(r, 'taban_m50'))} | {_k60_yuzde(_k60_g(r, 'P_m50'))} | {_k60_lift_yaz(r, 'm50')} | "
                               f"{_yz(_k60_g(r, 'ort'))} | {_yz(_k60_g(r, 'medyan'))} | {_yz(_k60_g(r, 'taban_ort'))} | {not_ if d == 'kesif' else ''} |")
            return "\n".join(out) or "| (satır yok) | | | | | | | | | | | | |"
        secili = [(x["sinyal"], x["taraf"], ("yol " + "+".join(x["yol"])) + ("; " + ", ".join(et[(x["sinyal"], x["taraf"])]) if et.get((x["sinyal"], x["taraf"])) else ""))
                  for x in sec["secili"]]
        var = {(a, b) for a, b, _c in secili}
        bil = [(b, t, "AİLE BİLGİSİ") for b in sec["bilesik"] for t in ("UST", "ALT") if (b, t) not in var]
        model = [("ODDS_MODEL", "UST", "birleşik model (bilgi; KEŞİF örneklem içi)")]
        durum = "KASA açıldı" if mk else ("DOĞRULAMA bitti, KASA kapalı" if md else "yalnız KEŞİF bitti")
        metin = (f"# K60 olasılık tablosu ({durum})\n\n"
                 f"Okuma: 'taban' = aynı aylarda BÜTÜN uygun evrende 12 ayda o olayın görülme oranı; 'kat' = uçtaki oran / taban oran; köşeli parantez = ay kümeli "
                 f"blok bootstrap %95 aralığı. ÜST = beklenen yöne göre en iyi %{E['portfoy']['dilim'] * 100:.0f} (bayrakta bayraklı grup), ALT = en kötü %{E['portfoy']['dilim'] * 100:.0f}. Evren yalnız BUGÜN yaşayan "
                 f"şirketlerdir: P(-%50) ve katı ALT SINIRDIR, P(+%100) tabanı yukarı yanlıdır. Hiçbir satır İZ değildir (CLAUDE.md standardı: ABD + Avrupa).\n\n"
                 f"## KEŞİF-SEÇİLİ özellikler ({len(secili)} çift)\n\n{bas}{satirlar(secili)}\n\n"
                 f"## Aile bileşikleri ve K59 bileşikleri (seçilmemiş olanlar; bilgi)\n\n{bas}{satirlar(bil)}\n\n"
                 f"## Birleşik olasılık modeli (üst %{E['portfoy']['dilim'] * 100:.0f}; bilgi)\n\n{bas}{satirlar(model)}\n")
    yol = _k60_yol("tablo", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def k60_rapor(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """K60_RAPOR.md ve olasilik_tablosu.md'yi eldeki çıktılardan yeniden yazar (hangi dönemler koşulduysa)."""
    E = E or K60_ESIK; au = E["r2"]["ana_ufuk"]; ty = k60_olasilik_tablosu(cikti, E)
    try:
        oc = k60_onkayit_dogrula(cikti); ok_satir = f"Ön kayıt: {oc['zaman_utc']} UTC (mühür {oc['sha'][:12]}, dosya sha256 {oc['dosya_sha256'][:12]})"
    except K60Hata as ex:
        ok_satir = f"Ön kayıt doğrulanamadı: {ex}"
    M = {d: _k60_meta_bitti(d, cikti) for d in K60_DONEM}; R1 = {d: _k60_oku(f"{d}_r1.csv", cikti) for d in K60_DONEM}; R2 = {d: _k60_oku(f"{d}_r2.csv", cikti) for d in K60_DONEM}
    Pl = _k60_oku(K60_DOSYA["plasebo"], cikti); ys = _k60_yol("secili", cikti); sec = _k60_json_oku(ys) if os.path.exists(ys) else None
    par = [f"# K60 — sinyal kütüphanesi, iki cetvel, üç dönem: RAPOR\n\n{ok_satir}. {K60_SURUM}\n"]
    for d in K60_DONEM:
        if M[d]:
            v = M[d].get("veri_denetimi", {})
            par.append(f"- {K60_DONEM_AD[d]}: koşu {M[d]['kos_baslangic']} → {M[d]['kos_bitis']} ({M[d].get('sure_sn', '?')} sn); {M[d].get('hisse', '?')} hisse, oluşum ayı R1 {v.get('olusum_ayi_r1')}, "
                       f"R2 {v.get('olusum_ayi_r2')}; uygun evren ort. {v.get('ort_evren', 0):.0f}. Veri denetimi (kırpma yok): en büyük tek hisse aylık getirisi "
                       f"{_yz(v.get('maks_aylik_getiri'), 0)}, +%300 üstü {v.get('aylik_ust_300')} / {v.get('hisse_ay')} hisse-ay; en büyük 12 aylık getiri {_yz(v.get('maks_12ay_getiri'), 0)}, "
                       f"+%1000 üstü {v.get('getiri12_ust_1000')} / {v.get('hisse_ay_12')}.")
    if sec is None or R1["kesif"] is None or R2["kesif"] is None:
        par.append("\nKEŞİF henüz koşulmadı; sonuç yok.\n")
    else:
        es = sec["esik"]; K1, K2 = R1["kesif"], R2["kesif"]; k2 = K2[K2.ufuk == au]; tb = k2[_k60_dogru(k2.olculdu).to_numpy()]
        t100 = float(tb.taban_p100.median()) if len(tb) else np.nan; t50 = float(tb.taban_m50.median()) if len(tb) else np.nan
        ny = {y: sum(y in x["yol"] for x in sec["secili"]) for y in ("R1", "R2", "R2K")}
        par.append(f"\n## Bulgular (düz dille)\n"
                   f"- KEŞİF ({E['donem']['kesif'][0]} .. {E['donem']['kesif'][1]}): bir hissenin 12 ayda en az +%100 yapma taban oranı {_k60_yuzde(t100)}, en az -%50 düşme taban oranı {_k60_yuzde(t50)} "
                   f"(yalnız yaşayanlar; ortanca ölçüm).\n"
                   f"- {int(_k60_dogru(K1.olculdu).sum())} (sinyal, uç) satırı R1'de, {len(tb)} satır R2'de ölçüldü. KEŞİF-SEÇİLİ {len(sec['secili'])} çift: R1 yolundan {ny['R1']}, "
                   f"+%100 olasılığı (R2) yolundan {ny['R2']}, -%50 olasılığı (R2K) yolundan {ny['R2K']}.\n"
                   f"- Plasebo (200 rastgele sinyal): cetvel v2 yanlış pozitif net {_k60_yuzde(es.get('yp_net'))}, brüt {_k60_yuzde(es.get('yp_brut'))} (eşik %{E['coklu']['yp_esik'] * 100:.0f}; R1 yolu "
                   f"{'AÇIK' if es.get('r1_acik') else 'KAPALI: hüküm yok'}); 'lift alt sınırı > 1' oranı +%100 için {_k60_yuzde(es.get('yp_r2'))}, -%50 için {_k60_yuzde(es.get('yp_r2k'))}"
                   f"{' (R2 aralığı DAR: plasebo eşiği belirleyici)' if es.get('r2_aralik_dar') or es.get('r2k_aralik_dar') else ''}. Eşikler: net t(alfa) > {_sy(es.get('t_arti'))} (eksi yön: brüt t < -{_sy(es.get('t_eksi_brut'))}), "
                   f"+%100 lift > {_sy(es.get('lift_p100'))}, -%50 lift > {_sy(es.get('lift_m50'))} ({es.get('m_r1')} ve {es.get('m_r2')} hipotez).")
        for d, ad in (("dogrulama", "DOĞRULAMA"), ("kasa", "KASA")):
            if M[d]:
                s = M[d].get("sonuc", [])
                par.append(f"- {ad}: giren {M[d].get('giren_n')} çift, geçen {M[d].get('gecen_n')} (R1 {sum(x['r1'] for x in s)}, R2 {sum(x['r2'] for x in s)}, R2K {sum(x['r2k'] for x in s)}, "
                           f"R1 ters {sum(x['r1_ters'] for x in s)}).")
        if M["kasa"]:
            et = [x for x in M["kasa"].get("etiket", []) if x["etiket"]]
            par.append("- ETİKETLER: " + ("; ".join(f"{x['sinyal']} ({x['taraf']}): {', '.join(x['etiket'])}" for x in et) if et else "hiçbir çift etiket alamadı (üç dönemin üçünden geçen yok)") + ".")
        else:
            par.append("- Etiket verilmedi: KASA açılmadı.")
        par.append("- İZ ilan edilemez: CLAUDE.md standardı (FI_OLCUT, ABD + Avrupa) değişmedi; bu ölçüm yalnız ABD ve yalnız yaşayanlar.\n")
        with open(ty, encoding="utf-8") as f:
            par.append("## Olasılık tablosu (ana sonuç)\n" + f.read().split("\n", 1)[1])
        # R1: seçilenler + bileşikler
        var = {(x["sinyal"], x["taraf"]) for x in sec["secili"]} | {(b, "UST") for b in sec["bilesik"]}
        bas = ("| özellik (uç) | dönem | ay | yıllık fazla (net) | NW t | alfa (yıllık) | t(alfa) | beta | alt 1/2/3 | son %30 | cetvel v2 | FF5+UMD alfa | t | devir | hisse | en büyük üç katkı |\n"
               "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        sat = []
        for s, t in sorted(var):
            for d in K60_DONEM:
                X = R1[d]
                if X is None or not len(X):
                    continue
                x = X[(X.sinyal == s) & (X.taraf == t)]
                if not len(x):
                    continue
                r = x.iloc[0]; g = lambda k: _k60_g(r, k)  # noqa: E731
                sat.append(f"| {s} ({'ÜST' if t == 'UST' else 'ALT'}) | {K60_DONEM_AD[d]} | {int(g('ay')) if np.isfinite(g('ay')) else 0} | {_yz(g('yillik_fazla'))} | {_sy(g('nw_t'))} | {_yz(g('alfa_yillik'))} | "
                           f"{_sy(g('t_alfa'))} | {_sy(g('beta'))} | {_yz(g('alt1'), 2)} / {_yz(g('alt2'), 2)} / {_yz(g('alt3'), 2)} | {_yz(g('son30'), 2)} | "
                           f"{'TUTAR' if str(r.get('tutar_v2')).lower() == 'true' else 'tutmaz'} | {_yz(g('ff_alfa_yillik'))} | {_sy(g('ff_t_alfa'))} | {_k60_yuzde(g('ort_devir'), 0)} | "
                           f"{_sy(g('ort_hisse'), 0)} | {r.get('katki_ilk3') if isinstance(r.get('katki_ilk3'), str) else '—'} |")
        par.append("\n## R1 — portföy cetveli v2 (seçilen çiftler ve bileşiklerin ÜST ucu)\n" + bas + ("\n".join(sat) or "| (satır yok) |" + " |" * 15))
        kt = []
        for x in sec["secili"]:
            a1 = K1[(K1.sinyal == x["sinyal"]) & (K1.taraf == x["taraf"])]; a2 = k2[(k2.sinyal == x["sinyal"]) & (k2.taraf == x["taraf"])]
            g1 = a1.iloc[0].get("katki_ilk3") if len(a1) else None; g2 = a2.iloc[0].get("olay_ilk3") if len(a2) else None
            kt.append(f"| {x['sinyal']} ({'ÜST' if x['taraf'] == 'UST' else 'ALT'}) | {g1 if isinstance(g1, str) else '—'} | {g2 if isinstance(g2, str) else '—'} |")
        par.append("\n## En büyük üç katkı (KEŞİF; aykırılar kırpılmadı)\n| özellik (uç) | R1: toplam getiri katkısındaki pay | R2: +%100 olayı sayısı / uçtaki toplam olay |\n|---|---|---|\n"
                   + ("\n".join(kt) or "| (seçili çift yok) | | |"))
        # kütüphanenin tamamı (KEŞİF)
        bas = ("| sinyal | aile | yön | R1 ÜST: yıllık fazla | t(alfa) | BH | +%100 kat ÜST | ALT | -%50 kat ÜST | ALT | seçili |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
        sat = []; i1 = {(r.sinyal, r.taraf): r for r in K1.itertuples()}; i2 = {(r.sinyal, r.taraf): r for r in k2.itertuples()}
        secs = {(x["sinyal"], x["taraf"]): "+".join(x["yol"]) for x in sec["secili"]}
        for s in k60_satirlar(E):
            a = i1.get((s["kod"], "UST")) or i1.get((s["kod"], "ALT")); u, l = i2.get((s["kod"], "UST")), i2.get((s["kod"], "ALT"))
            isaret = "; ".join(f"{t} {secs[(s['kod'], t)]}" for t in ("UST", "ALT") if (s["kod"], t) in secs)
            sat.append(f"| {s['kod']} | {s['aile']} | {s['yon_kayit']} | {_yz(_k60_g(a, 'yillik_fazla')) if a is not None else '—'} | {_sy(_k60_g(a, 't_alfa')) if a is not None else '—'} | "
                       f"{'evet' if a is not None and str(getattr(a, 'bh_r1', False)).lower() == 'true' else ''} | {_k60_lift_yaz(u, 'p100') if u is not None else '—'} | {_k60_lift_yaz(l, 'p100') if l is not None else '—'} | "
                       f"{_k60_lift_yaz(u, 'm50') if u is not None else '—'} | {_k60_lift_yaz(l, 'm50') if l is not None else '—'} | {isaret} |")
        par.append("\n## Kütüphanenin tamamı (KEŞİF; R1 sütunları bayrakta bayraklı grup içindir)\n" + bas + "\n".join(sat))
        if Pl is not None and len(Pl):
            ta = Pl.t_alfa.astype(float); tbr = -Pl.brut_t_alfa.astype(float); l1 = Pl.r2_lift_p100.astype(float); l2 = Pl.r2_lift_m50.astype(float)
            par.append(f"\n## Plasebo dağılımı (KEŞİF, {len(Pl)} rastgele sinyal)\n| istatistik | medyan | %95 | en büyük | seçim eşiği |\n|---|---|---|---|---|\n"
                       f"| net t(alfa) (bilgi) | {_sy(ta.median())} | {_sy(ta.quantile(0.95))} | {_sy(ta.max())} | — |\n"
                       f"| brüt t(alfa) | {_sy((-tbr).median())} | {_sy((-tbr).quantile(0.95))} | {_sy((-tbr).max())} | {_sy(es.get('t_arti'))} |\n"
                       f"| -brüt t(alfa) | {_sy(tbr.median())} | {_sy(tbr.quantile(0.95))} | {_sy(tbr.max())} | {_sy(es.get('t_eksi_brut'))} |\n"
                       f"| +%100 lift | {_sy(l1.median())} | {_sy(l1.quantile(0.95))} | {_sy(l1.max())} | {_sy(es.get('lift_p100'))} |\n"
                       f"| -%50 lift | {_sy(l2.median())} | {_sy(l2.quantile(0.95))} | {_sy(l2.max())} | {_sy(es.get('lift_m50'))} |")
        Km = _k60_oku("model", cikti)
        if Km is not None and len(Km):
            kat = sec.get("model", {}).get("katsayi")
            par.append("\n## Birleşik olasılık modeli (bilgi)\nKatsayılar (KEŞİF'te donduruldu): " + (", ".join(f"{a} {_sy(b)}" for a, b in zip(["sabit"] + list(sec["model"]["girdi"]), kat)) if kat else "kurulamadı")
                       + ".\n\n| dönem | dilim | gözlem | tahmin | gerçekleşen |\n|---|---|---|---|---|\n"
                       + "\n".join(f"| {K60_DONEM_AD.get(r.donem, r.donem)} | {int(r.dilim)} | {int(r.n)} | {_k60_yuzde(r.tahmin, 2)} | {_k60_yuzde(r.gerceklesen, 2)} |" for r in Km.itertuples()))
    notlar = [f"- {K60_DONEM_AD[d]}: {n}" for d in K60_DONEM if M[d] for n in M[d].get("not", [])]
    if notlar:
        par.append("\n## Koşu notları\n" + "\n".join(notlar))
    par.append("\n## Yanlılık ve sınırlar\nYalnız yaşayanlar (kaybeden olasılıkları ALT SINIR; küçüklük, düşük fiyat, sıkıntı ve likidite aileleri en açık); frames en son bildirilen değeri "
               "verir; XBRL kapsamı 2011'e kadar kademeli; Yahoo kırpık hisseler dışarıda; aykırı getiriler tutuldu; dönemler oluşum ayına göre (12 aylık pencereler komşu "
               f"döneme taşar). R1 için tam kör OLMAYAN satırlar (K58 / K59'da görüldü): {', '.join(E['kor_degil'])}. Ayrıntı: K60_ON_KAYIT.md §9 ve §11.\n")
    metin = "\n".join(par); yol = _k60_yol("rapor", cikti)
    if _K60_EPOSTA.search(metin):
        raise K60Hata("rapor metninde e-posta biçimli parça var; yazılmadı")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k60log.info("rapor: %s", yol)
    return yol


def _cakisma_kontrol_k60(_once=_CK_ONCE_K60, _dosya="K60.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K60", "_CK_KAYIT", "_cakisma_kontrol_k60", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "hashlib", "json", "logging", "math", "pickle", "re", "subprocess", "time", "zipfile", "annotations", "Any", "Callable",
           "Dict", "List", "Optional", "Tuple", "K59", "KV", "K57", "K58", "_dt", "_yz", "_sy")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k60()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=K60_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kapsam", "kos", "rapor"])
    ap.add_argument("--donem", choices=list(K60_DONEM), default=None, help="kos: kesif | dogrulama | kasa")
    ap.add_argument("--cikti", default=None)
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(k60_onkayit(a.cikti)); print("ESIK_SHA256:", k60_esik_sha())
        elif a.komut == "kapsam":
            Zk = k60_kapsam_kos(a.cikti)
            print(Zk[Zk.donem == "kesif"][["sinyal", "aile", "tur", "olcum_ay", "ort_n", "ilk_ay"]].to_string(index=False))
            print(json.dumps(_k60_json_oku(_k60_yol("kapsam_ozet", a.cikti)), ensure_ascii=False, indent=1))
        elif a.komut == "kos":
            if not a.donem:
                raise K60Hata("kos için --donem kesif | dogrulama | kasa gerekir")
            Rk = k60_kos(a.donem, a.cikti)
            print(f"K60 {K60_DONEM_AD[a.donem]} bitti:", json.dumps({k: v for k, v in Rk["meta"].items() if k in ("secili_n", "giren_n", "gecen_n", "esik", "etiket", "sure_sn")},
                                                                    ensure_ascii=False, default=str)); print(Rk["rapor"])
        else:
            print(k60_rapor(a.cikti))
    except (K60Hata, K59.K59Hata, K58.K58Hata, KV.K60VHata, FileNotFoundError) as ex:
        k60log.error("%s", ex); sys.exit(1)
