"""D9_AVR — Ç181c devamı: D9b sektör rüzgârının AVRUPA'da ölçümü (Avrupa sektör listesi sektor_AVR.csv ile; 15 Kasım 2026).

Cemal (15 Kas 2026): "sektör derle". Dayanak Ç181c (D9_YENIDEN satır c): yalnız sektör rüzgârı ABD 2024-26'da dört şartın üçünü tuttu,
ABD 2023 alt uç -0,3; AVR 'sektör listesi yok'. Bu dosya AYNI sinyali, AYNI cetvelle (ORTAK_CETVEL v1.0), AYNI eşiklerle yalnız AVR'de koşar.

YAPI (D9_YENIDEN KODU DEĞİŞTİRİLMEZ; kütüphane olarak içe alınır):
  - Sektör kaynağı: D9_YENIDEN.D9_ESIK'in DERİN KOPYASINDA E['sektor']['AVR'] = ['sektor_AVR.csv', 'ust'] (D9_YENIDEN'in global sözlüğü
    değişmez; d9_durum / d9_sektor E parametresiyle çağrılır).
  - Sinyal: D9_YENIDEN.d9_uzun_seri / d9_ruzgar_panel / d9_sektor üzerinden d9a_durum (D9_YENIDEN.d9_durum'un birebir kopyası; tek fark
    250 bardan kısa hissede eksik bant sütunu NaN: D9_YENIDEN.d9_durum o hissede rüzgâr varsa düşer), d9_satir (a / b / c), d9_sayim,
    d9_tercil_sinir, d9_olc_satir (OC.oc_olc).
  - Geleceğe bakma denetimi: D9_YENIDEN.d9_gelecek_denetimi AVR sektörünü göremediği (global E) için burada aynı mantık
    (d9_uzun_ref + d9_ruzgar_ref, seri t'de kesilir) AVR sektör sözlüğüyle koşar.
  - sektor_AVR.csv: islenmis-veri dalı avr/evren_avr_ham.csv (Wikipedia STOXX Europe 600 + FTSE 250 bileşen listeleri) -> V_AVR.pkl'deki
    581 sembol; 'ust' = ICB süpersektör (tek adlandırma, D9A_ESLESME); 3 boş sektör Wikipedia STOXX Europe 600 sayfasından (D9A_WIKI).

Komut:  python D9_AVR.py sektor    sektor_AVR.csv + sektor_AVR_eslesme.md (ham csv + V_AVR anahtarlarından; yeniden üretilebilir)
        python D9_AVR.py onkayit   ön kayıt (tanım, sha'lar, eşleme, KONTROL LİSTESİ, karar kuralı, OLAY SAYIMI; getiri hesaplanmaz)
        python D9_AVR.py kos       ölçüm (IZ_KARNE.ik_kontrol_kapisi + OC.oc_kapi + kendi sha / git kapısı geçmezse durur)
        python D9_AVR.py rapor     sonuç json'undan rapor
        seçenek: --veri <V_AVR.pkl klasörü> (varsayılan OC_VERI ya da /tmp/veri)
Colab:  exec(open('D9_AVR.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   V_AVR.pkl (islenmis-veri dalı; k34 / veri2 AVR'de kullanılmaz); satır verisi /tmp/d9_avr (repoya girmez).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_D9A = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_D9A = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_D9A not in sys.path:
    sys.path.insert(0, KOK_D9A)

import ORTAK_CETVEL as OC  # noqa: E402
import D9_YENIDEN as D9  # noqa: E402

d9alog = logging.getLogger("col.d9_avr")
if not d9alog.handlers:
    _d9a_h = logging.StreamHandler(sys.stderr)
    _d9a_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s d9_avr: %(message)s", "%H:%M:%S"))
    d9alog.addHandler(_d9a_h)
    d9alog.setLevel(logging.INFO)
    d9alog.propagate = False

D9A_SURUM = "D9_AVR v1.0 (2026-11-15): D9b sektör rüzgârı AVRUPA'da (sektor_AVR.csv 'ust'), D9_YENIDEN v1.0 + ORTAK CETVEL v1.0"
D9A_PAZAR = "AVR"
D9A_YOL = {"cikti": os.path.join(KOK_D9A, "arastirma_cikti", "d9_avr"), "satir": os.environ.get("D9A_SATIR", "/tmp/d9_avr"),
           "kod": os.path.join(KOK_D9A, "D9_AVR.py"), "d9_kod": os.path.join(KOK_D9A, "D9_YENIDEN.py"),
           "col_v1": os.path.join(KOK_D9A, "COL_v1.py"), "sektor": os.path.join(KOK_D9A, "sektor_AVR.csv"),
           "eslesme": os.path.join(KOK_D9A, "sektor_AVR_eslesme.md"),
           "d9_onkayit": os.path.join(KOK_D9A, "arastirma_cikti", "d9_yeniden", "D9_YENIDEN_ON_KAYIT.md"),
           "d9_sonuc": os.path.join(KOK_D9A, "arastirma_cikti", "d9_yeniden", "d9_yeniden_sonuc.json"),
           "veri": os.environ.get("OC_VERI", "/tmp/veri"), "ham_ref": "origin/islenmis-veri:avr/evren_avr_ham.csv"}
D9A_DOSYA = {"onkayit": "D9_AVR_ON_KAYIT.md", "sonuc": "d9_avr_sonuc.json", "rapor": "D9_AVR_RAPOR.md", "tercil": "d9_avr_tercil.json",
             "hucre_csv": "d9_avr_hucre.csv"}
D9A_DONEM = ("2016-22", "2023", "2024-26")
D9A_KARAR_DONEM = ("2023", "2024-26")

# ================================================================ SEKTÖR NORMALİZASYONU (ham Wikipedia adı -> ICB süpersektör; tek adlandırma)
D9A_FON = "Investment Trusts"      # işletme değil fon: ayrı sınıf (rüzgâr hesabına kendi sınıfı olarak girer; (c) için 'hariç' bilgi sayımı)
D9A_ICB = ("Automobiles and Parts", "Banks", "Basic Resources", "Chemicals", "Construction and Materials", "Consumer Products and Services",
           "Energy", "Financial Services", "Food, Beverage and Tobacco", "Health Care", "Industrial Goods and Services", "Insurance", "Media",
           "Personal Care, Drug and Grocery Stores", "Real Estate", "Retail", "Technology", "Telecommunications", "Travel and Leisure",
           "Utilities")
D9A_ESLESME: Dict[str, str] = {
    # STOXX Europe 600: zaten ICB süpersektör adları (20)
    **{a: a for a in D9A_ICB},
    # FTSE 250 (Wikipedia; eski ICB / FTSE alt sektör adları ve yazım farkları) -> ICB 2019 süpersektörü
    "Construction & Materials": "Construction and Materials", "Construction": "Construction and Materials",
    "Engineering and Construction": "Construction and Materials",
    "Travel & Leisure": "Travel and Leisure", "Travel and leisure": "Travel and Leisure",
    "Retailers": "Retail",
    "Food & Drug Retailers": "Personal Care, Drug and Grocery Stores", "Personal Products": "Personal Care, Drug and Grocery Stores",
    "Food Producers": "Food, Beverage and Tobacco", "Food and drink": "Food, Beverage and Tobacco", "Beverages": "Food, Beverage and Tobacco",
    "Aerospace & Defence": "Industrial Goods and Services", "Support Services": "Industrial Goods and Services",
    "Industrial Support Services": "Industrial Goods and Services", "Industrial Engineering": "Industrial Goods and Services",
    "Industrial Transportation": "Industrial Goods and Services", "Electronic & Electrical Equipment": "Industrial Goods and Services",
    "General Industrials": "Industrial Goods and Services", "Industrials": "Industrial Goods and Services",
    "Software and Computer Services": "Technology", "Software & Computer Services": "Technology", "Consumer Digital Services": "Technology",
    "Real Estate Investment Trusts": "Real Estate", "Real Estate Investment & Services": "Real Estate",
    "General Financial": "Financial Services", "Investment Banking and Brokerage Services": "Financial Services",
    "Banking": "Banks",
    "Oil & Gas Producers": "Energy", "Oil, Gas and Coal": "Energy", "Alternative Energy": "Energy",
    "Industrial Metals and Mining": "Basic Resources", "Precious Metals and Mining": "Basic Resources",
    "Pharmaceuticals & Biotechnology": "Health Care", "Pharmaceuticals and Biotechnology": "Health Care",
    "Health Care Equipment & Services": "Health Care",
    "Telecomms": "Telecommunications",
    "Gas, Water & Multiutilities": "Utilities", "Electricity": "Utilities",
    "Nonlife Insurance": "Insurance", "Life Insurance": "Insurance",
    "Home Construction": "Consumer Products and Services", "Household goods & home construction": "Consumer Products and Services",
    "Leisure Goods": "Consumer Products and Services", "Personal Goods": "Consumer Products and Services",
    "Consumer Staples": "Consumer Products and Services",   # tek üye Coats Group (iplik / tekstil; ICB Personal Goods karşılığı)
    # fon etiketleri (FTSE 250): işletme değil fon -> fon sınıfı
    "Investment Trusts": D9A_FON, "Equity Investments": D9A_FON, "Collective Investments": D9A_FON, "Hedge Funds": D9A_FON,
}
# ham csv'de sektörü boş 3 satır: Wikipedia 'STOXX Europe 600' bileşen tablosundaki satır (15 Kas 2026, action=raw)
D9A_WIKI: Dict[str, Tuple[str, str]] = {
    "ATCO-A.ST": ("Industrial Goods and Services", "en.wikipedia.org/wiki/STOXX_Europe_600 satırı: Atlas Copco | ATCO A | SE0017486889 | Industrial Goods and Services"),
    "ERIC-B.ST": ("Telecommunications", "en.wikipedia.org/wiki/STOXX_Europe_600 satırı: Ericsson | ERIC B | SE0000108656 | Telecommunications"),
    "BT.A.L": ("Telecommunications", "en.wikipedia.org/wiki/STOXX_Europe_600 satırı: BT Group | BT.A | GB0030913577 | Telecommunications"),
}

D9A_KARAR = {
    "satir": "c",
    "hucre_tutar": "hücre durumu ORTAK_CETVEL oc_hucre_durum == 'TUTAR' (FI dört şart: n >= 30, ort eşli fark > 0 ve ay kümeli %95 alt uç > 0, "
                   "sıra > 0,50, portföy > plasebo p90; + cetvelin iki alt yarı şartı) — Ç181a/b/c ile aynı cetvel kuralı; 'tutar4' bilgi olarak yazılır",
    "iki": "AVR 2023 ve AVR 2024-26 ikisi de TUTAR -> 'Ç181c EMARE GÜÇLENDİ (4 karar hücresinin 3'ü; ABD 2023 alt uç -0,3 olduğu için İZ DEĞİL, bilinen etki)'",
    "bir": "biri TUTAR -> 'EMARE (değişmedi), tek pazar tek dönem'",
    "hic": "hiçbiri TUTAR değil ve ikisi de TUTMADI (güç yeterli) -> 'EMARE ZAYIFLADI: rüzgâr Avrupa'da görünmüyor'",
    "olculemedi": "hiçbiri TUTAR değil ve en az biri ÖLÇÜLEMEDİ (n < 30 ya da güç yetersiz) -> 'EMARE (değişmedi); AVR ÖLÇÜLEMEDİ' "
                  "(İZ DEĞİL / zayıfladı sözü güç yetersizken kullanılmaz; CLAUDE.md emin olma yolu)",
    "a": "satır (a) D9 AVR Ç181a'da ölçüldü (İZ DEĞİL): yalnız tutarlılık — olay sayımı D9_YENIDEN ön kaydındaki AVR (a) satırıyla AYNI "
         "beklenir; koşuda AVR 2023 / 2024-26 n D9_YENIDEN sonucuyla aynı beklenir; farklıysa HATA",
    "b": "satır (b) D9 VE RÜZGÂR AVR: BİLGİ; hücre n < 1.000 ise ÖLÇÜLEMEDİ yazılır (karar değil)",
    "bilgi": "(c) 'Investment Trusts hariç' alt sayım ve ölçüm yalnız bilgi (karar hücresi değişmez); süre / tercil alt grupları bilgi",
    "sabit": "eşik, sektör sütunu ('ust') ve satır tanımları sonuca göre oynanmaz; ikinci sütunla (ham 'sektor') ikinci koşu YOK; sapma olursa SAPMA",
}

D9A_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc (D9_YENIDEN.d9_olc_satir): aynı giriş günü, aynı pazar (AVR), 60 gün momentum "
                   "beşliği x 20 gün likidite (EUR, Kur sütunu) üçlüsü, aynı açılış girişi / 60. gün çıkışı; 200 plasebo portföy. Mekanik üstünlük: "
                   "(c) rüzgâr SEKTÖR momentumudur; hisse momentumu eşlenir, sektör momentumu eşlenmez -> sonuç 'bilinen etki' (Moskowitz-Grinblatt "
                   "1999) okunur, yeni iz sayılmaz"),
    "K2": ("EVET", "D9 t'ye kadar barlarla (rolling, geriye), rüzgâr t'ye kadar kapanışlarla; kos d9a_gelecek_denetimi 30 rastgele olayda seriyi "
                   "t'de keser, COL_v1 kopyası (d9_uzun_ref / d9_ruzgar_ref) AVR sektör sözlüğüyle aynı D9 / ruz değerini mekanik denetler; "
                   "test_d9_avr 'geleceğe bakma'. SINIR: sektor_AVR.csv BUGÜNÜN listesi (Wikipedia 2026 bileşenleri ve bugünkü ICB sınıfı), "
                   "karar günündeki sektör değil; sınıf değişimi nadir ama etiket sabit varsayılır (K7 ile birlikte yazılır)"),
    "K3": ("EVET", "OC.oc_veri temiz bar (H>L, V>0, O/H/L/C > 0, 31.08.2026 kesik) üzerinden sinyal ve rüzgâr paneli; geçersiz bar olay "
                   "günü olamaz (cetvel 'sinyal barı geçersiz' sayımı)"),
    "K4": ("EVET", "durum günleri cetvele verilir; OC.oc_olay_hazirla aynı hissede 60 gün tekilleştirir; n bağımsız olay; hücre tablosunda medyan"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla); sinyal t kapanışında"),
    "K6": ("EVET", "tek kip V_AVR.pkl (fi_k1_veri düzeltilmiş, yerel para; .L peni); rüzgâr ve D9 oranlardan (birimden bağımsız); likidite EUR "
                   "(Kur). Ön kayıtta günlük >= 1,8x sıçrama listesi (temiz barlarda 18 gün, 100x birim kayması YOK; bölünme / şirket ayrılması "
                   "örn. VIV.PA 09.12.2024, HOLN.SW 16.06.2025) yazılı; düzeltilmez (sinyal tanımı değişmez; BIST / ABD ile aynı işlem), sepet "
                   "ortalamasını 60 gün etkileyebilir -> sınır olarak raporda"),
    "K7": ("EVET", "evren BUGÜN işlem gören STOXX 600 + FTSE 250 üyeleri (581 sembol); batan / endeksten çıkan YOK -> getiriler yukarı, -%50 "
                   "olasılığı aşağı yanlı okunur; sektör etiketi de bugünkü (K2 notu). Büyük hisselerde yanlılık küçük (CLAUDE.md)"),
    "K8": ("EVET", "AVR x 3 dönem (2016-22 keşif bilgi; 2023, 2024-26 karar); n < 30 ÖLÇÜLEMEDİ; İZ DEĞİL / zayıfladı yalnız güç yeterliyken; "
                   "3 satır, tek sektör sütunu (ikinci koşu yok); olay sayımı ön kayıtta getiri hesaplanmadan"),
    "K9": ("EVET", "D9A_ESIK (eşleme dahil) sha, D9_PARAM sha, D9_AVR.py / D9_YENIDEN.py sha (COL_v1.py sha bilgi), sektor_AVR.csv + eşleme md sha, "
                   "V_AVR.pkl sha, cetvel üç sha ön kayıtta; kos IZ_KARNE.ik_kontrol_kapisi + OC.oc_kapi + d9a_onkayit_dogrula (git "
                   "işlenmiş / değişmemiş; sha eşit) geçmezse durur; karar kuralı sonuçtan önce yazılı"),
    "K10": ("EVET", "ayrıştırma: Wikipedia bileşen listesi (islenmis-veri avr/evren_avr_ham.csv) -> sektör; 3 boş sektör Wikipedia STOXX Europe "
                    "600 satırından elle doğrulandı (D9A_WIKI); her ham ad tek ust'a (D9A_ESLESME; test); rastgele 3 satır elle denetlendi "
                    "(rapor); haber / kurum etiketi maddeleri uygulanmaz (metin yok). SINIR: FTSE 250 etiketleri isimden: bazı fonlar "
                    "'Financial Services' / 'Energy' etiketli (3IN, INPP, SEQI, SOI, PPET, GCP, VEIL, VOF, SEIT), Man Group 'Investment "
                    "Trusts' etiketli; etikete dokunulmadı (eşleme md)"),
    "K11": ("EVET", "satır verisi /tmp/d9_avr/olay_<satır>.csv.gz + durum.csv.gz; hücre özeti arastirma_cikti/d9_avr/d9_avr_hucre.csv; "
                    ">= 2 hücre bağımsız denetçi tarafından yeniden üretilir (ana model işi)"),
    "K12": ("EVET", "etiketler yalnız oc_hucre_durum / oc_etiket ve önceden yazılı karar kuralı; 'bilinen etki' etiketi; fiyat değişimi ile "
                    "işlem kârı ayrı (komisyon yok); sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_d9a; D9_YENIDEN / ORTAK_CETVEL / COL_v1 / IZ_KARNE / defterler yalnız okunur (git status "
                    "denetimi); D9_YENIDEN.D9_ESIK kalıcı değişmez (derin kopya; test); e-posta / anahtar taraması testte; ücretli veri yok "
                    "(Wikipedia + islenmis-veri)"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm (T8 üretim ekranı kararı Cemal'in)"),
}


class D9AHata(RuntimeError):
    """Durdurucu hata: sektör dosyası tutarsız / ön kayıt yok / sha tutmuyor / git'e işlenmemiş / geleceğe bakma denetimi tutmadı."""


# ================================================================ 0) ORTAK
_D9A_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _d9a_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _d9a_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or D9A_YOL["cikti"], D9A_DOSYA.get(ad, ad))


def d9a_E(sektor_yol: str = "sektor_AVR.csv") -> Dict[str, Any]:
    """D9_YENIDEN.D9_ESIK'in DERİN KOPYASI; yalnız AVR sektör kaynağı ve AVR notu değişir (global sözlük değişmez)."""
    E = copy.deepcopy(D9.D9_ESIK)
    E["sektor"]["AVR"] = [sektor_yol, "ust"]
    E["avr"] = "AVR sektör listesi sektor_AVR.csv 'ust' (ICB süpersektör; D9_AVR); (a) / (b) / (c) AVR'de ölçülür"
    E["d9_avr"] = {"surum": D9A_SURUM, "eslesme": D9A_ESLESME, "wiki": {k: v[0] for k, v in D9A_WIKI.items()}, "fon": D9A_FON,
                   "karar": D9A_KARAR}
    return E


def d9a_esik_sha() -> str:
    return D9.d9_sha(d9a_E())


def d9a_ust(ham: Any) -> str:
    """ham Wikipedia sektör adı -> ust (bilinmeyen ad durur: sessiz sınıf yok)."""
    if ham is None or (isinstance(ham, float) and np.isnan(ham)) or str(ham).strip() == "":
        return ""
    h = str(ham).strip()
    if h not in D9A_ESLESME:
        raise D9AHata(f"eşleme tablosunda olmayan ham sektör adı: '{h}' (D9A_ESLESME'ye eklenmeli)")
    return D9A_ESLESME[h]


# ================================================================ 1) SEKTÖR LİSTESİ
def d9a_ham_oku(ham_yol: Optional[str] = None) -> pd.DataFrame:
    """islenmis-veri dalındaki avr/evren_avr_ham.csv (ya da verilen yol)."""
    if ham_yol:
        return pd.read_csv(ham_yol, keep_default_na=False, na_values=[""])
    try:
        r = subprocess.run(["git", "-C", KOK_D9A, "show", D9A_YOL["ham_ref"]], capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as ex:
        raise D9AHata(f"ham evren okunamadı ({ex}); --ham <yol> ver")
    if r.returncode != 0:
        raise D9AHata(f"ham evren okunamadı: {r.stderr.strip()} (git fetch origin islenmis-veri ya da --ham <yol>)")
    return pd.read_csv(io.StringIO(r.stdout), keep_default_na=False, na_values=[""])


def d9a_v_semboller(veri: Optional[str] = None) -> List[str]:
    yol = os.path.join(veri or D9A_YOL["veri"], f"V_{D9A_PAZAR}.pkl")
    if not os.path.exists(yol):
        raise D9AHata(f"veri yok: {yol} (--veri <klasör> ya da islenmis-veri vpac)")
    V = pd.read_pickle(yol)
    if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
        V = V["veri"]
    return sorted(str(s) for s in V)


def d9a_sektor_tablosu(ham: pd.DataFrame, semboller: List[str]) -> pd.DataFrame:
    """ham evren + V_AVR sembolleri -> sektor_AVR tablosu (sembol, sektor, ust, ulke, kaynak). Boş ham sektör D9A_WIKI'den."""
    h = ham.copy()
    h["kod"] = h["kod"].astype(str).str.strip()
    if h.kod.duplicated().any():
        raise D9AHata(f"ham evrende tekrar eden kod: {sorted(h.kod[h.kod.duplicated()])[:10]}")
    eksik = sorted(set(semboller) - set(h.kod))
    if eksik:
        raise D9AHata(f"V_AVR sembolü ham evrende yok: {eksik[:10]} ({len(eksik)})")
    h = h[h.kod.isin(semboller)].copy()
    bos = h.sektor.isna() | (h.sektor.astype(str).str.strip() == "")
    for i in h.index[bos]:
        k = h.at[i, "kod"]
        if k in D9A_WIKI:
            h.at[i, "sektor"] = D9A_WIKI[k][0]
    h["ust"] = [d9a_ust(x) for x in h.sektor]
    out = h.rename(columns={"kod": "sembol"})[["sembol", "sektor", "ust", "ulke", "kaynak"]].sort_values("sembol").reset_index(drop=True)
    return out


def d9a_eslesme_md(T: pd.DataFrame, ham: pd.DataFrame) -> str:
    """Eşleme tablosu (ham ad -> ust, V_AVR'deki hisse sayısı, ham 692'deki sayı), ust sınıf tablosu, Wikipedia tamamlamaları, notlar."""
    hamsay = ham.sektor.fillna("(boş)").astype(str).value_counts()
    s = ["# sektor_AVR.csv — eşleme tablosu (ham Wikipedia sektör adı -> ust = ICB süpersektör)", "",
         f"{D9A_SURUM}. Üretim: `python D9_AVR.py sektor` (islenmis-veri dalı avr/evren_avr_ham.csv + V_AVR.pkl anahtarları). "
         f"Evren: V_AVR.pkl {len(T)} sembol (ham 692 satırın V_AVR'de olanları: STOXX600 {int((T.kaynak == 'STOXX600').sum())}, "
         f"FTSE250 {int((T.kaynak == 'FTSE250').sum())}).", "",
         "Rüzgâr sınıfı sütunu: **ust** (ön kayıtta sabit; ikinci sütunla ikinci koşu yok). BIST 'alt_bist' (~30 sınıf) kabalığına yakın "
         f"({T.ust.replace('', np.nan).nunique()} sınıf); ABD 'endustri' daha incedir — fark ön kayıtta yazılır.", "",
         "## Eşleme (ham ad -> ust)", "", "| ham sektör adı | ust | hisse (V_AVR) | hisse (ham 692) |", "|---|---|---|---|"]
    vs = T.sektor.astype(str).value_counts()
    for h in sorted(D9A_ESLESME, key=lambda a: (D9A_ESLESME[a], a)):
        s.append(f"| {h} | {D9A_ESLESME[h]} | {int(vs.get(h, 0))} | {int(hamsay.get(h, 0))} |")
    s += ["", "## ust sınıfları (V_AVR evreni)", "", "| ust | üye | not |", "|---|---|---|"]
    m = D9.D9_PARAM["RUZ_MIN_UYE"]
    for u, n in T.ust.replace("", "(boş)").value_counts().sort_index().items():
        nt = []
        if n - 1 < m:
            nt.append(f"RUZ_MIN_UYE {m} altı (öteki üye {n - 1}): rüzgâr hiç alamaz")
        if u == D9A_FON:
            nt.append("işletme değil FON sınıfı; (c) için 'hariç' bilgi sayımı")
        s.append(f"| {u} | {n} | {'; '.join(nt)} |")
    s += ["", f"- Sektörü boş sembol: {int((T.ust == '').sum())}.",
          f"- Not: RUZ_MIN_UYE = {m} 'öteki üye' sayısıdır; bir sınıf en az {m + 1} üyeyle rüzgâr üretir. Günlük taze üye sayısı (veri başlangıcı, "
          "geçersiz bar) bu sayıdan az olabilir; panel her gün yeniden sayar.", "",
          "## Wikipedia tamamlamaları (ham csv'de sektör boş)", ""]
    for k, (u, kay) in D9A_WIKI.items():
        s.append(f"- {k}: {u} — {kay}" + ("" if k in set(T.sembol) else " (V_AVR'de yok; tabloya girmez)"))
    s += ["", "## Notlar", "",
          f"- '{D9A_FON}': FTSE 250 'Investment Trusts' (70) + fon etiketli 'Equity Investments' (3), 'Collective Investments' (3), "
          "'Hedge Funds' (1) -> tek fon sınıfı (işletme değil fon). ICB'de bunlar Financial Services / Closed End Investments altındadır; "
          "iş tanımı gereği ayrı sınıf.",
          "- Etiket isimden: FTSE 250 listesinde bazı fonlar 'Financial Services' (3IN, INPP, SEQI, SOI, PPET), 'General Financial' (GCP, VEIL, VOF) "
          "ya da 'Energy' (SEIT) etiketlidir; Man Group (işletme) 'Investment Trusts' etiketlidir. Etikete dokunulmadı (ham ad -> ust tek kural).",
          "- 'Consumer Staples' (tek üye Coats Group, iplik / tekstil) -> Consumer Products and Services (ICB Personal Goods karşılığı).",
          "- 'Home Construction', 'Household goods & home construction', 'Leisure Goods', 'Personal Goods' -> Consumer Products and Services; "
          "'Food & Drug Retailers', 'Personal Products' -> Personal Care, Drug and Grocery Stores; 'Consumer Digital Services' -> Technology; "
          "'Alternative Energy' -> Energy (ICB 2019 yapısı).",
          "- Sektör etiketi BUGÜNKÜ listedir (K2 / K7 sınırı)."]
    return "\n".join(s) + "\n"


def d9a_sektor_yaz(ham_yol: Optional[str] = None, veri: Optional[str] = None) -> Dict[str, Any]:
    ham = d9a_ham_oku(ham_yol)
    T = d9a_sektor_tablosu(ham, d9a_v_semboller(veri))
    T.to_csv(D9A_YOL["sektor"], index=False, lineterminator="\n")
    md = d9a_eslesme_md(T, ham)
    with open(D9A_YOL["eslesme"], "w", encoding="utf-8") as f:
        f.write(md)
    d9alog.info("sektor_AVR.csv yazıldı: %d sembol, %d ust sınıfı, boş %d", len(T), T.ust.replace("", np.nan).nunique(), int((T.ust == "").sum()))
    return {"n": len(T), "ust": T.ust.value_counts().to_dict(), "bos": int((T.ust == "").sum())}


def d9a_sektor_denetle(veri: Optional[str] = None, semboller: Optional[List[str]] = None) -> pd.DataFrame:
    """sektor_AVR.csv: V_AVR sembolleriyle birebir, her satır sektor -> ust eşlemesine uygun, ust boş değilse bilinen sınıf."""
    yol = D9A_YOL["sektor"]
    if not os.path.exists(yol):
        raise D9AHata(f"sektör dosyası yok: {yol} (önce `python D9_AVR.py sektor`)")
    T = pd.read_csv(yol)     # D9_YENIDEN.d9_sektor ile AYNI okuma (varsayılan NA kuralları)
    if list(T.columns) != ["sembol", "sektor", "ust", "ulke", "kaynak"]:
        raise D9AHata(f"sektor_AVR.csv sütunları beklenmiyor: {list(T.columns)}")
    S = semboller if semboller is not None else d9a_v_semboller(veri)
    if sorted(T.sembol.astype(str)) != sorted(S):
        raise D9AHata(f"sektor_AVR.csv sembolleri V_AVR ile birebir değil (csv {len(T)}, V {len(S)})")
    for r in T.itertuples():
        if isinstance(r.sektor, str) and d9a_ust(r.sektor) != (r.ust if isinstance(r.ust, str) else ""):
            raise D9AHata(f"{r.sembol}: sektor '{r.sektor}' -> ust '{r.ust}' eşleme tablosuyla tutmuyor")
    gecerli = set(D9A_ESLESME.values())
    bilinmez = sorted(set(T.ust.dropna()) - gecerli)
    if bilinmez:
        raise D9AHata(f"bilinmeyen ust sınıfı: {bilinmez}")
    return T


# ================================================================ 2) ÖLÇÜM YARDIMCILARI
def d9a_sicrama(Vd: Dict[str, Any], esik: float = 1.8) -> List[Tuple[str, str, float]]:
    """K6 veri denetimi (getiri ölçüsü değil): temiz barlarda günlük kapanış oranı >= esik ya da <= 1/esik olan günler."""
    out = []
    for s, x in sorted(Vd["V"].items()):
        c = x.Close.to_numpy(float)
        if len(c) < 2:
            continue
        r = c[1:] / c[:-1]
        for i in np.where((r >= esik) | (r <= 1 / esik))[0]:
            out.append((s, str(x.index[i + 1].date()), round(float(r[i]), 3)))
    return out


def d9a_fon_semboller(T: Optional[pd.DataFrame] = None) -> set:
    T = T if T is not None else pd.read_csv(D9A_YOL["sektor"])
    return set(T.sembol[T.ust == D9A_FON].astype(str))


def d9a_sayim_fon_haric(D: pd.DataFrame, PN: Dict[str, Any], fon: set) -> Dict[str, Any]:
    """(b) / (c) satırları için 'Investment Trusts hariç' olay sayımı (getiri yok): tekil olaylar ana satırdan, sonra fon sembolleri çıkar."""
    out = {}
    for sat in ("b", "c"):
        x = D9.d9_satir(D, sat)
        x = x[x.pazar == D9A_PAZAR]
        Y, _say = OC.oc_olay_hazirla(x[["sembol", "tarih", "pazar"]], PN, OC.OC_ESIK)
        if not len(Y):
            out[sat] = {d: 0 for d in D9A_DONEM}; continue
        Yh = Y[~Y.sembol.astype(str).isin(fon)]
        out[sat] = {d: int((Yh.donem == d).sum()) for d in D9A_DONEM}
        out[sat]["fon_olay"] = {d: int(((Y.donem == d) & Y.sembol.astype(str).isin(fon)).sum()) for d in D9A_DONEM}
    return out


def d9a_d9_yeniden_a_sayim(yol: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """D9_YENIDEN ön kaydındaki '| a | AVR | ...' satırı (yalnız olay sayımı; getiri yok)."""
    yol = yol or D9A_YOL["d9_onkayit"]
    if not os.path.exists(yol):
        return None
    m = re.search(r"^\|\s*a\s*\|\s*AVR\s*\|\s*(\d+) / (\d+) / (\d+)\s*\|\s*(\d+) / (\d+) / (\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
                  open(yol, encoding="utf-8").read(), flags=re.M)
    if not m:
        return None
    v = [int(x) for x in m.groups()]
    return {"durum_gunu": dict(zip(D9A_DONEM, v[0:3])), "olay": dict(zip(D9A_DONEM, v[3:6])), "tekil": v[6], "havuz_disi": v[7]}


def d9a_a_tutarlilik(say: Dict[str, Any], ref: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if ref is None:
        return {"durum": "REFERANS YOK", "not": "D9_YENIDEN ön kaydında AVR (a) satırı okunamadı"}
    c = say["a"][D9A_PAZAR]
    simdi = {"durum_gunu": c["durum_gunu"], "olay": c.get("olay", {}), "tekil": c["dusme"].get("tekil", 0),
             "havuz_disi": c["dusme"].get("havuz_disi", 0)}
    esit = all(simdi[k] == ref[k] for k in ref)
    return {"durum": "AYNI" if esit else "FARKLI (HATA)", "d9_yeniden": ref, "d9_avr": simdi}


def d9a_gelecek_denetimi(Vd: Dict[str, Any], X: pd.DataFrame, sek: Dict[str, str], n: int, tohum: int) -> int:
    """D9_YENIDEN.d9_gelecek_denetimi ile aynı mantık, AVR sektör sözlüğüyle: rastgele n olayda seri t'de kesilir; COL_v1 kopyası
    (d9_uzun_ref / d9_ruzgar_ref) aynı D9 / ruz değerini vermeli. Tutmazsa D9AHata."""
    if not len(X):
        return 0
    rng = np.random.default_rng(tohum); sec = X.iloc[rng.choice(len(X), min(n, len(X)), replace=False)]
    V = Vd["V"]; evb = Vd.get("evren_bas", {})
    for r in sec.itertuples():
        t = pd.Timestamp(r.tarih)
        u = D9.d9_uzun_ref(V[r.sembol], t)
        d9 = bool(u and u["uzun"])
        if d9 != bool(r.D9) or (d9 and u["uzun"] != r.uzun):
            raise D9AHata(f"geleceğe bakma / kopya denetimi D9 tutmadı: {r.sembol} {t.date()} ({u} vs {r.D9} {r.uzun})")
        kes = {s: x[x.index <= t] for s, x in V.items() if not (s in evb and t < pd.Timestamp(evb[s]))}
        R = D9.d9_ruzgar_ref(kes, sek, t)
        rz = float(R.ruz.get(r.sembol, np.nan)) if r.sembol in R.index else np.nan
        if not ((np.isnan(rz) and np.isnan(r.ruz)) or (np.isfinite(rz) and np.isfinite(r.ruz) and abs(rz - r.ruz) < 1e-9)):
            raise D9AHata(f"geleceğe bakma / kopya denetimi rüzgâr tutmadı: {r.sembol} {t.date()} ({rz} vs {r.ruz})")
    return len(sec)


def d9a_durum(Vd: Dict[str, Any], pazar: str, E: Dict[str, Any]) -> pd.DataFrame:
    """D9_YENIDEN.d9_durum'un BİREBİR kopyası; TEK fark: 250 bardan kısa hissede d9_uzun_seri 'bant250' (ve 125'ten kısada 'bant125')
    sütunu üretmez; D9_YENIDEN.d9_durum o hissede rüzgâr günü varsa AttributeError ile düşer (AVR'de SHAW.L, 210 temiz bar; Ç181'de AVR
    rüzgârı olmadığı için ortaya çıkmadı). Eksik bant sütunu NaN yazılır; sinyal (D9, rüzgâr) değişmez. test_d9_avr: uzun hisselerde
    D9_YENIDEN.d9_durum ile birebir aynı tablo."""
    P = E["param"]; V = Vd["V"]; sek = D9.d9_sektor(pazar, E)
    RP = D9.d9_ruzgar_panel(Vd, sek, P) if sek else None
    a, b = pd.Timestamp(E["olay_bas"]), pd.Timestamp(E["olay_son"])
    parca = []
    for s in sorted(V):
        x = V[s]
        U = D9.d9_uzun_seri(x, P, tuple(E["bilgi"]["sure_W"])[::-1])
        tar = x.index
        if RP is not None:
            r = RP["tarih"].get_indexer(tar); j = RP["kol"][s]
            ruz = RP["ruz"][r, j]; sep = RP["sepet"][r, j]; rz = RP["ruzgar"][r, j]
        else:
            ruz = np.full(len(tar), np.nan); sep = ruz.copy(); rz = np.zeros(len(tar), bool)
        evb = Vd.get("evren_bas", {}).get(s)
        m = (U.D9.to_numpy() | rz) & (tar >= a) & (tar <= b)
        if evb is not None:
            m &= tar >= pd.Timestamp(evb)
        if not m.any():
            continue
        bos = np.full(len(tar), np.nan)
        b250 = U["bant250"].to_numpy() if "bant250" in U else bos
        b125 = U["bant125"].to_numpy() if "bant125" in U else bos
        parca.append(pd.DataFrame({"sembol": s, "tarih": tar[m], "pazar": pazar, "D9": U.D9.to_numpy()[m], "uzun": U.uzun.to_numpy()[m],
                                   "sure": U.sure.to_numpy()[m], "ruz": ruz[m], "sepet": sep[m], "ruzgar": rz[m],
                                   "bant250": b250[m], "bant125": b125[m]}))
    D = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame(columns=["sembol", "tarih", "pazar", "D9", "uzun", "sure", "ruz",
                                                                                "sepet", "ruzgar", "bant250", "bant125"])
    D["sektor_var"] = bool(sek)
    return D


def d9a_hazirla(veri: Optional[str] = None) -> Tuple[Dict[str, Any], pd.DataFrame, Dict[str, Any], Dict[str, Any], Dict[str, str]]:
    """Veri + sektör denetimi + durum tablosu + panel. Döner (Vd, D, PN, E, sek)."""
    E = d9a_E()
    Vd = OC.oc_veri(D9A_PAZAR, klasor=veri or D9A_YOL["veri"])
    d9a_sektor_denetle(veri)
    sek = D9.d9_sektor(D9A_PAZAR, E)
    if not sek:
        raise D9AHata("AVR sektör sözlüğü boş")
    D = d9a_durum(Vd, D9A_PAZAR, E)
    PN = OC.oc_panel(Vd)
    return Vd, D, PN, E, sek


# ================================================================ 3) ÖN KAYIT
_D9A_DESEN = {"esik": r"D9A_ESIK_SHA:\s*`([0-9a-f]{64})`", "param": r"D9_PARAM_SHA:\s*`([0-9a-f]{64})`",
              "kod": r"D9A_KOD_SHA:\s*`([0-9a-f]{64})`", "d9_kod": r"D9_YENIDEN_SHA:\s*`([0-9a-f]{64})`",
              "sektor": r"SEKTOR_AVR_SHA:\s*`([0-9a-f]{64})`",
              "eslesme": r"ESLESME_SHA:\s*`([0-9a-f]{64})`", "veri": r"V_AVR_SHA:\s*`([0-9a-f]{64})`"}


def d9a_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = D9A_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def _d9a_shalar(veri: Optional[str] = None) -> Dict[str, str]:
    return {"esik": d9a_esik_sha(), "param": D9.d9_sha(D9.D9_PARAM), "kod": D9._d9_sha_dosya(D9A_YOL["kod"]),
            "d9_kod": D9._d9_sha_dosya(D9A_YOL["d9_kod"]), "col_v1": D9._d9_sha_dosya(D9A_YOL["col_v1"]),
            "sektor": D9._d9_sha_dosya(D9A_YOL["sektor"]), "eslesme": D9._d9_sha_dosya(D9A_YOL["eslesme"]),
            "veri": D9._d9_sha_dosya(os.path.join(veri or D9A_YOL["veri"], f"V_{D9A_PAZAR}.pkl"))}


def _d9a_ust_tablo(T: pd.DataFrame) -> List[str]:
    m = D9.D9_PARAM["RUZ_MIN_UYE"]
    s = ["| ust | üye | rüzgâr alabilir mi (öteki üye >= 4) |", "|---|---|---|"]
    for u, n in T.ust.fillna("(boş)").value_counts().sort_index().items():
        s.append(f"| {u} | {n} | {'EVET' if n - 1 >= m else 'HAYIR (sınıf küçük)'} |")
    return s


def d9a_onkayit_metni(say: Dict[str, Any], tercil: Dict[str, List[float]], sha: Dict[str, str], T: pd.DataFrame, fonh: Dict[str, Any],
                      a_tut: Dict[str, Any], sicrama: List[Tuple[str, str, float]], Vd_n: int) -> str:
    K = D9A_KARAR
    s = ["# D9_AVR — ÖN KAYIT (Ç181c devamı: sektör rüzgârı Avrupa'da)", "", D9A_SURUM, "",
         f"- D9A_ESIK_SHA: `{sha['esik']}`", f"- D9_PARAM_SHA: `{sha['param']}`", f"- D9A_KOD_SHA: `{sha['kod']}`",
         f"- D9_YENIDEN_SHA: `{sha['d9_kod']}`", f"- COL_V1_SHA (bilgi; kapı değil): `{sha['col_v1']}`", f"- SEKTOR_AVR_SHA: `{sha['sektor']}`",
         f"- ESLESME_SHA: `{sha['eslesme']}`", f"- V_AVR_SHA: `{sha['veri']}`", f"- ZAMAN (UTC): `{_d9a_simdi()}`", "",
         "Bu dosya ölçümden ÖNCE yazıldı; hiçbir getiri / eş farkı / olasılık hesaplanmadı (yalnız olay sayımı). `kos` bu dosya, D9_AVR.py, "
         "sektor_AVR.csv, eşleme md, tercil json ve D9_YENIDEN.py git'e işlenmiş ve değişmemiş değilse, sha'lardan biri tutmazsa ya da KONTROL LİSTESİ "
         "eksikse durur. COL_v1.py sha'sı yalnız bilgidir (T8 üretim ekranı işi COL_v1'i ayrıca değiştirebilir); D9 / rüzgâr D9_YENIDEN'deki birebir "
         "kopyalarla hesaplanır ve kapı D9_PARAM == COL_v1 sabitlerini (d9_param_denetle) ayrıca denetler.", "",
         "## Cetvel mühür satırları (ORTAK_CETVEL; aynen)", "", OC.oc_kapi_satirlari(), "",
         "## Soru", "", "Ç181c: 'yalnız sektör rüzgârı' (RÜZGÂR VE D9 DEĞİL) ABD 2024-26'da dört şartın üçünü tuttu, ABD 2023 alt uç -0,3; AVR'de "
         "sektör listesi yoktu. Aynı sinyal, aynı cetvel, aynı eşiklerle AVR 2023 ve AVR 2024-26'da tutuyor mu? Literatür: sektör momentumu "
         "bilinen etkidir (Moskowitz-Grinblatt 1999); sonuç yeni iz sayılmaz, 'bilinen etki' etiketi taşır.", "",
         "## Tanım (D9_YENIDEN v1.0'dan birebir; yalnız AVR sektör kaynağı eklendi)", "", "```json",
         json.dumps(D9.D9_PARAM, ensure_ascii=False, indent=1, sort_keys=True), "```", "",
         "- D9 = COL_v1 uzun_col_olc (W 250 / 125; bant <= 1,50; mum <= 0,04; konum <= 0,50). RÜZGÂR = COL_v1 sektor_ruzgar: ruz = sepet (aynı "
         "sınıfın öteki üyeleri, en az 4, eşit ağırlık, 60 bar getirisi) - piyasa (AVR taze hisselerinin 60 bar getiri MEDYANI) >= 0,10 VE sepet > 0.",
         f"- Satırlar: {json.dumps(D9.D9_ESIK['satirlar'], ensure_ascii=False)}", f"- Olay: {D9.D9_ESIK['olay']}", f"- Veri: {D9.D9_ESIK['veri']}",
         "- SEKTÖR SÜTUNU (sabit): sektor_AVR.csv **'ust'** = ICB süpersektör (21 sınıf: 20 ICB + 'Investment Trusts' fon sınıfı). BIST 'alt_bist' "
         "(~30 sınıf) kabalığına yakın; ABD 'endustri' daha incedir (sınıf başına daha az, daha benzer hisse). Bu fark sonuç okunurken yazılır. "
         "İkinci sütunla (ham 'sektor') ikinci koşu YOK.",
         "- Piyasa: AVR evreninin tamamı (fonlar dahil) taze hisselerinin medyanı (COL_v1 tanımı). Fon sınıfı rüzgâr hesabına kendi sınıfı olarak girer.",
         f"- Dönemler (cetvel): {json.dumps(OC.OC_ESIK['donem'], ensure_ascii=False)}; kriz kesiği {OC.OC_ESIK['kriz']} (fiyat kesik; 60 gün "
         "penceresi aşan olay ölçülmez). Karar hücreleri: AVR 2023, AVR 2024-26; 2016-22 keşif / bilgi.",
         f"- Evren: V_AVR.pkl {len(T)} sembol (oc_veri sonrası {Vd_n}); hayatta kalma: bugün işlem görenler.", "",
         "## ÖNCEDEN YAZILI KARAR (sonuç görülmeden)", "",
         f"- Karar satırı: ({K['satir']}) RÜZGÂR VE D9 DEĞİL.", f"- Hücre: {K['hucre_tutar']}.", f"- {K['iki']}.", f"- {K['bir']}.",
         f"- {K['hic']}.", f"- {K['olculemedi']}.", f"- (a): {K['a']}.", f"- (b): {K['b']}.", f"- Bilgi: {K['bilgi']}.", f"- {K['sabit']}.", "",
         "## SAPMA / AÇIKLAMA (sonuç görülmeden yazıldı)", "",
         "- İş tanımı 'OC dört şartı' diyor; cetvelin hücre durumu 'TUTAR' dört şarta ek iki alt yarı şartını da ister (oc_hucre 'tutar'). "
         "Ç181a/b/c ile aynı cetvel kuralı kullanıldı; 'tutar4' (yalnız dört şart) raporda bilgi olarak yazılır. Karar 'TUTAR'a göredir.",
         "- İş tanımındaki üç sonuç dalına dördüncü dal eklendi: hiçbir hücre TUTAR değil ve biri ÖLÇÜLEMEDİ ise 'EMARE (değişmedi); AVR "
         "ÖLÇÜLEMEDİ' (güç yetersizken 'zayıfladı' denmez; CLAUDE.md emin olma yolu).",
         "- D9_YENIDEN.d9_gelecek_denetimi AVR sektörünü global sözlükten okuduğu için AVR'de rüzgârı denetleyemez; aynı mantık d9a_gelecek_denetimi "
         "olarak AVR sözlüğüyle koşar (D9_YENIDEN değişmez).",
         "- d9_tercil.json'da AVR satırı yok (Ç181'de AVR rüzgârı yoktu): AVR tercil sınırları bu ön kayıtta, AVR RÜZGÂR durum günlerinin ruz "
         "değerlerinden (getiri yok) aynı kuralla hesaplandı ve d9_avr_tercil.json'a yazıldı.", "",
         "## Sektör listesi (sektor_AVR.csv 'ust'; eşleme: sektor_AVR_eslesme.md, sha yukarıda)", ""] + _d9a_ust_tablo(T) + [
         "", f"- Sektörü boş sembol: {int(T.ust.isna().sum())}. Fon sınıfı '{D9A_FON}': {int((T.ust == D9A_FON).sum())} sembol (işletme değil fon).",
         "", "### Eşleme tablosu (ham ad -> ust)", "", "| ham | ust | hisse (V_AVR) |", "|---|---|---|"]
    vs = T.sektor.astype(str).value_counts()
    for h in sorted(D9A_ESLESME, key=lambda a: (D9A_ESLESME[a], a)):
        if int(vs.get(h, 0)):
            s.append(f"| {h} | {D9A_ESLESME[h]} | {int(vs.get(h, 0))} |")
    s += ["", "Wikipedia tamamlamaları: " + "; ".join(f"{k} -> {v[0]}" for k, v in D9A_WIKI.items()), "",
          "## Bilgi (karar dışı) alt gruplar", "", f"- Çöl süresi: {D9.D9_ESIK['bilgi']['sure']}", f"- Rüzgâr şiddeti: {D9.D9_ESIK['bilgi']['tercil']}",
          "- AVR tercil sınırları (ruz, sonuç görülmeden): " + "; ".join(f"{p}: {q[0]:.4f} / {q[1]:.4f}" for p, q in tercil.items()),
          f"- (c) '{D9A_FON} hariç': (c) tekil olaylarından fon sembolleri çıkarılarak (bilgi).", "",
          "## K6 veri denetimi: günlük kapanış oranı >= 1,8 ya da <= 1/1,8 (temiz barlar; getiri ölçüsü değil)", "",
          f"{len(sicrama)} gün: " + ", ".join(f"{a} {b} x{c}" for a, b, c in sicrama) + ". 100x birim kayması yok; bölünme / şirket ayrılması / "
          "sermaye artırımı sıçramaları düzeltilmedi (sinyal tanımı değişmez; BIST / ABD ile aynı işlem).", "",
          "## OLAY SAYIMI (getiri hesaplanmadan)", ""] + D9._d9_say_tablo(say) + ["",
          f"(b) / (c) '{D9A_FON} hariç' olay sayımı (girişe göre dönem 2016-22 / 2023 / 2024-26; bilgi):", ""]
    for sat in ("b", "c"):
        f = fonh.get(sat, {})
        s.append(f"- ({sat}) hariç: {f.get('2016-22', 0)} / {f.get('2023', 0)} / {f.get('2024-26', 0)}; fon olayı: "
                 f"{f.get('fon_olay', {}).get('2016-22', 0)} / {f.get('fon_olay', {}).get('2023', 0)} / {f.get('fon_olay', {}).get('2024-26', 0)}")
    s += ["", "Süre sınıfları ve tercil sayıları (olay, girişe göre dönem):", "", "```json",
          json.dumps({k: {p: {a: b for a, b in c.items() if a in ("sure", "tercil")} for p, c in v.items() if "not" not in c} for k, v in say.items()},
                     ensure_ascii=False, indent=1), "```", "",
          "## GÜÇ ÖN BİLGİSİ (getiri yok; cetvel güç tablosu guc_tablosu.json, δ = +%5, OC.oc_guc_bak; hücre n'i r60 / eş düşmesiyle "
          "olay sayısından biraz küçük olabilir)", "",
          "| Satır | Hücre | olay | güç (δ +%5) | 'TUTMADI' yazılabilir mi (n >= 1.000 ya da güç >= %80) |", "|---|---|---|---|---|"]
    for sat in ("b", "c"):
        for d in D9A_KARAR_DONEM:
            n = int(say[sat][D9A_PAZAR].get("olay", {}).get(d, 0))
            g = OC.oc_guc_bak(n)
            yeter = n >= OC.OC_ESIK["etiket"]["n_yeter"] or g >= OC.OC_ESIK["etiket"]["guc_esik"]
            s.append(f"| {sat} | AVR {d} | {n} | {100 * g:.1f}% | {'EVET' if yeter else 'HAYIR: TUTAR değilse ÖLÇÜLEMEDİ'} |")
    s += ["", "Sonuç görülmeden not: (c) iki karar hücresinde de güç yetersizse karar kuralının 'EMARE ZAYIFLADI' dalına ulaşılamaz; olası "
          "sonuçlar GÜÇLENDİ / değişmedi (tek hücre TUTAR) / 'EMARE (değişmedi); AVR ÖLÇÜLEMEDİ'. Eşik ve kural bu yüzden değiştirilmez.", "",
          f"(a) tutarlılık (D9_YENIDEN ön kaydı AVR (a) satırı ile): **{a_tut['durum']}**"
          + (f" — D9_YENIDEN {a_tut.get('d9_yeniden')}, D9_AVR {a_tut.get('d9_avr')}" if a_tut.get("d9_yeniden") else ""), "",
          "Kural: bir hücrede n < 30 ise ÖLÇÜLEMEDİ yazılır, 'iz değil' denmez (cetvel oc_hucre_durum).", "",
          d9a_kontrol_tablosu(), "",
          "## Test", "", "`python test_d9_avr.py` (sektor_AVR.csv V_AVR ile birebir ve eşleme tutarlı; sentetik AVR akışı b / c boş değil; "
          "D9_YENIDEN BIST / ABD / AVR davranışı değişmedi; kontrol kapısı eksik satırda durur; e-posta / anahtar taraması) ve "
          "`python test_d9_yeniden.py` (değişmeden geçer).", ""]
    return "\n".join(s)


def d9a_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False) -> str:
    yol = _d9a_yol("onkayit", cikti)
    if os.path.exists(yol):
        try:
            OC._oc_git_islenmis(yol)
            raise D9AHata(f"ön kayıt git'e işlenmiş ({yol}); üzerine yazılmaz")
        except OC.OCHata:
            if not uzerine:
                raise D9AHata(f"ön kayıt var ({yol}); git'e işlenmemişse --uzerine-yaz")
    D9.d9_param_denetle()
    if D9.D9_ESIK["sektor"].get("AVR") is not None:
        raise D9AHata("D9_YENIDEN.D9_ESIK['sektor']['AVR'] None değil: D9_YENIDEN değişmiş ya da bellekte ezilmiş")
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    Vd, D, PN, E, sek = d9a_hazirla(veri)
    d9alog.info("AVR durum günleri: %d (rüzgâr %d, D9 %d)", len(D), int(D.ruzgar.astype(bool).sum()), int(D.D9.astype(bool).sum()))
    tercil = D9.d9_tercil_sinir(D)
    say = D9.d9_sayim(D, {D9A_PAZAR: PN}, tercil)
    T = d9a_sektor_denetle(veri)
    fonh = d9a_sayim_fon_haric(D, PN, d9a_fon_semboller(T))
    a_tut = d9a_a_tutarlilik(say, d9a_d9_yeniden_a_sayim())
    if a_tut["durum"] != "AYNI":
        d9alog.warning("(a) tutarlılık: %s", a_tut)
    metin = d9a_onkayit_metni(say, tercil, _d9a_shalar(veri), T, fonh, a_tut, d9a_sicrama(Vd), len(Vd["V"]))
    if _D9A_EPOSTA.search(metin):
        raise D9AHata("ön kayıtta e-posta biçimli parça var")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    with open(_d9a_yol("tercil", cikti), "w", encoding="utf-8") as f:
        json.dump(tercil, f, indent=1)
    d9alog.info("ön kayıt yazıldı: %s", yol)
    return yol


def d9a_onkayit_dogrula(yol: Optional[str] = None, git: bool = True, veri: Optional[str] = None) -> Dict[str, Any]:
    yol = yol or _d9a_yol("onkayit")
    if not os.path.exists(yol):
        raise D9AHata(f"ön kayıt yok ({yol}): önce `python D9_AVR.py onkayit`")
    metin = open(yol, encoding="utf-8").read(); b = {}
    for ad, desen in _D9A_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise D9AHata(f"ön kayıt bozuk: '{ad}' satırı yok")
        b[ad] = m.group(1)
    simdi = _d9a_shalar(veri)
    for ad in _D9A_DESEN:
        if b[ad] != simdi[ad]:
            raise D9AHata(f"{ad} sha tutmuyor (ön kayıt {b[ad][:12]}…, şimdi {simdi[ad][:12]}…): koşu DURDU (SAPMA)")
    D9.d9_param_denetle()
    if D9.D9_ESIK["sektor"].get("AVR") is not None:
        raise D9AHata("D9_YENIDEN.D9_ESIK['sektor']['AVR'] None değil: koşu DURDU")
    out = {"yol": yol, **b}
    if git:
        try:
            out["git"] = OC._oc_git_islenmis(yol)
            for ad, p in (("git_kod", D9A_YOL["kod"]), ("git_sektor", D9A_YOL["sektor"]), ("git_eslesme", D9A_YOL["eslesme"]),
                          ("git_tercil", os.path.join(os.path.dirname(yol), D9A_DOSYA["tercil"])), ("git_d9", D9A_YOL["d9_kod"])):
                out[ad] = OC._oc_git_islenmis(p)
        except OC.OCHata as ex:
            raise D9AHata(str(ex))
    return out


# ================================================================ 4) KOŞU
def d9a_karar(J_c: Dict[str, Any]) -> Dict[str, Any]:
    """Önceden yazılı karar kuralı (D9A_KARAR) satır (c) AVR karar hücrelerine uygulanır."""
    H = {(h["pazar"], h["donem"]): h for h in J_c["hucre"]}
    dur = {d: (H.get((D9A_PAZAR, d)) or {}).get("durum", "ÖLÇÜLEMEDİ") for d in D9A_KARAR_DONEM}
    tut = [d for d, v in dur.items() if v == "TUTAR"]
    if len(tut) == 2:
        k = "Ç181c EMARE GÜÇLENDİ (4 karar hücresinin 3'ü; ABD 2023 alt uç -0,3 olduğu için İZ DEĞİL, bilinen etki)"
    elif len(tut) == 1:
        k = f"EMARE (değişmedi), tek pazar tek dönem (AVR {tut[0]} TUTAR)"
    elif all(v == "TUTMADI" for v in dur.values()):
        k = "EMARE ZAYIFLADI: rüzgâr Avrupa'da görünmüyor"
    else:
        k = "EMARE (değişmedi); AVR ÖLÇÜLEMEDİ"
    return {"karar": k, "hucre": dur, "tutar4": {d: bool((H.get((D9A_PAZAR, d)) or {}).get("tutar4", False)) for d in D9A_KARAR_DONEM}}


def d9a_b_bilgi(J_b: Dict[str, Any]) -> Dict[str, str]:
    H = {(h["pazar"], h["donem"]): h for h in J_b["hucre"]}
    out = {}
    for d in D9A_KARAR_DONEM:
        h = H.get((D9A_PAZAR, d)) or {}
        n = int(h.get("n", 0) or 0)
        out[d] = "ÖLÇÜLEMEDİ (n < 1.000)" if n < 1000 else f"BİLGİ: {h.get('durum')}"
    return out


def d9a_a_kos_tutarlilik(J_a: Dict[str, Any], yol: Optional[str] = None) -> Dict[str, Any]:
    yol = yol or D9A_YOL["d9_sonuc"]
    if not os.path.exists(yol):
        return {"durum": "REFERANS YOK"}
    R = json.load(open(yol, encoding="utf-8"))
    ref = {h["donem"]: int(h.get("n", 0) or 0) for h in R["ana"]["a"]["hucre"] if h["pazar"] == D9A_PAZAR}
    simdi = {h["donem"]: int(h.get("n", 0) or 0) for h in J_a["hucre"] if h["pazar"] == D9A_PAZAR}
    return {"durum": "AYNI" if ref == simdi else "FARKLI (HATA)", "d9_yeniden_n": ref, "d9_avr_n": simdi}


def d9a_kos(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    t_bas = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    yol = _d9a_yol("onkayit", cikti)
    if kontrol:
        import IZ_KARNE as IK
        try:
            IK.ik_kontrol_kapisi(yol)
        except RuntimeError as ex:
            raise D9AHata(str(ex))
    kapi = OC.oc_kapi(yol, git=git, kontrol=False)
    oc = d9a_onkayit_dogrula(yol, git=git, veri=veri)
    kos_zaman = _d9a_simdi()
    tercil = json.load(open(_d9a_yol("tercil", cikti), encoding="utf-8"))
    satir_kl = D9A_YOL["satir"]; os.makedirs(satir_kl, exist_ok=True)
    Vd, D, PN, E, sek = d9a_hazirla(veri)
    X = D[D.D9.astype(bool) | D.ruzgar.astype(bool)]
    den = d9a_gelecek_denetimi(Vd, X, sek, E["gelecek_denetimi_n"], E["tohum"])
    d9alog.info("AVR: durum %d, geleceğe bakma denetimi %d olay TUTTU", len(D), den)
    D.to_csv(os.path.join(satir_kl, "durum.csv.gz"), index=False)
    PNd = {D9A_PAZAR: PN}; fon = d9a_fon_semboller()
    sonuc: Dict[str, Any] = {"surum": D9A_SURUM, "onkayit": oc, "oc_kapi": {k: v for k, v in kapi.items() if k != "kontrol"},
                             "kos_zaman_utc": kos_zaman, "tercil": tercil, "gelecek_denetimi": {D9A_PAZAR: den}, "ana": {}, "bilgi": {}}
    hucre_csv = []
    for sat in ("a", "b", "c"):
        Xs = D9.d9_satir(D, sat)
        S = D9.d9_olc_satir(Xs, PNd)
        Ol = S["olay"].merge(Xs[["sembol", "tarih", "pazar", "uzun", "sure", "ruz", "sepet"]], on=["sembol", "tarih", "pazar"], how="left")
        Ol["fon"] = Ol.sembol.astype(str).isin(fon)
        Ol.to_csv(os.path.join(satir_kl, f"olay_{sat}.csv.gz"), index=False)
        sonuc["ana"][sat] = D9._d9_json_S(S); sonuc["ana"][sat]["rapor"] = OC.oc_rapor(S, f"({sat}) {D9.D9_ESIK['satirlar'][sat]} — AVR")
        if len(S["hucre"]):
            hucre_csv.append(S["hucre"].assign(satir=sat, grup="ana"))
        d9alog.info("satır %s: %s / %s (%.0f sn)", sat, S["etiket"]["genel"], S["etiket"]["olasilik"], time.time() - t_bas)
        if sat == "a":
            grup = {k: Ol[Ol.sure == k] for k in ("6-9", "9-12", ">=12")}
        else:
            tt = D9.d9_tercil(Ol, tercil); grup = {k: Ol[tt == k] for k in ("T1 zayıf", "T2 orta", "T3 güçlü")}
        if sat == "c":
            grup[f"{D9A_FON} hariç"] = Ol[~Ol.fon]
        sonuc["bilgi"][sat] = {}
        for k, g in grup.items():
            Sg = D9.d9_olc_satir(g[["sembol", "tarih", "pazar"]], PNd)
            sonuc["bilgi"][sat][k] = D9._d9_json_S(Sg)
            if len(Sg["hucre"]):
                hucre_csv.append(Sg["hucre"].assign(satir=sat, grup=k))
    sonuc["karar"] = d9a_karar(sonuc["ana"]["c"])
    sonuc["b_bilgi"] = d9a_b_bilgi(sonuc["ana"]["b"])
    sonuc["a_tutarlilik"] = d9a_a_kos_tutarlilik(sonuc["ana"]["a"])
    sonuc["sure_sn"] = round(time.time() - t_bas, 1)
    os.makedirs(cikti or D9A_YOL["cikti"], exist_ok=True)
    if hucre_csv:
        pd.concat(hucre_csv, ignore_index=True).to_csv(_d9a_yol("hucre_csv", cikti), index=False)
    with open(_d9a_yol("sonuc", cikti), "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1, default=str)
    return {"sonuc": sonuc, "rapor": d9a_rapor(cikti)}


# ================================================================ 5) RAPOR
_D9A_KORU = ("## TEST", "## HATA", "## SAPMA", "## DENETİM", "## ÖNERİLEN DEFTER METNİ")


def _d9a_bolum_al(metin: str, baslik: str) -> Optional[str]:
    m = re.search(rf"^{re.escape(baslik)}\b.*?(?=^## |\Z)", metin, flags=re.M | re.S)
    return m.group(0).rstrip() if m else None


def d9a_sektor_bolumu() -> List[str]:
    T = pd.read_csv(D9A_YOL["sektor"])
    return ["## SEKTÖR LİSTESİ (sektor_AVR.csv 'ust'; ayrıntı sektor_AVR_eslesme.md)", ""] + _d9a_ust_tablo(T) + [
        "", f"- Sembol {len(T)}; sektörü boş {int(T.ust.isna().sum())}; fon sınıfı '{D9A_FON}' {int((T.ust == D9A_FON).sum())} (işletme değil fon).", ""]


def d9a_rapor(cikti: Optional[str] = None) -> str:
    J = json.load(open(_d9a_yol("sonuc", cikti), encoding="utf-8"))
    eski = open(_d9a_yol("rapor", cikti), encoding="utf-8").read() if os.path.exists(_d9a_yol("rapor", cikti)) else ""
    ad = D9.D9_ESIK["satirlar"]; _yz, _sy = D9._yz, D9._sy
    s = ["# D9_AVR — RAPOR (Ç181c devamı: sektör rüzgârı Avrupa'da; ORTAK CETVEL v1.0)", "",
         f"Ön kayıt commit {J['onkayit'].get('git', {}).get('commit', '-')[:10]} ({J['onkayit'].get('git', {}).get('commit_zamani', '-')}); "
         f"koşu {J['kos_zaman_utc']}; süre {J.get('sure_sn')} sn. Geleceğe bakma / kopya denetimi: "
         + ", ".join(f"{p} {n} olay TUTTU" for p, n in J["gelecek_denetimi"].items()) + ".", "",
         "## ÖZET", "", f"- KARAR (önceden yazılı kural, satır c): **{J['karar']['karar']}**.",
         "  - hücreler: " + "; ".join(f"AVR {d}: {v} (dört şart {'tuttu' if J['karar']['tutar4'][d] else 'tutmadı'})"
                                      for d, v in J["karar"]["hucre"].items()),
         f"- (a) tutarlılık (D9_YENIDEN AVR n ile): {J['a_tutarlilik']['durum']} {J['a_tutarlilik'].get('d9_avr_n', '')}",
         "- (b) bilgi: " + "; ".join(f"AVR {d}: {v}" for d, v in J["b_bilgi"].items())]
    for sat in ("a", "b", "c"):
        e = J["ana"][sat]["etiket"]
        oz = D9.d9_ozet_satir(J["ana"][sat])
        par = [f"{k}: n {v['n']}, eş farkı {_yz(v['fark'])} [alt {_yz(v['alt'])}] ({v['durum']}), +%100 katı {_sy(v['up'])}, -%50 katı {_sy(v['dn'])}"
               for k, v in oz.items()]
        s.append(f"- ({sat}) {ad[sat]}: cetvel etiketi {e['genel']} / {e['olasilik']}. " + "; ".join(par))
    s += ["", "- Okuma: 'eş farkı' = olay hissesinin 60 günlük getirisi eksi aynı gün, aynı momentum ve likidite kovasındaki öteki hisselerin "
          "ortalaması; '+%100 katı' = 250 günde +%100'e dokunma olasılığının eşlerinkine oranı. Rüzgâr sektör momentumudur (bilinen etki); "
          "hisse momentumu eşlenir, sektör momentumu eşlenmez. Hayatta kalma: evren bugün işlem gören hisseler. Komisyon yok.", ""]
    s += ["## Bilgi alt grupları (karar dışı): süre (a), rüzgâr tercilleri (b, c), (c) fon hariç", "",
          "| Satır | Grup | Hücre | n | eş farkı [%95 alt] | durum | +%100 kat eş [%95] | -%50 kat eş [%95] |", "|---|---|---|---|---|---|---|---|"]
    for sat, G in J["bilgi"].items():
        for k, Jg in G.items():
            for h, v in D9.d9_ozet_satir(Jg).items():
                s.append(f"| {sat} | {k} | {h} | {v['n']} | {_yz(v['fark'])} [{_yz(v['alt'])}] | {v['durum']} | {_sy(v['up'])} [{_sy(v['up_alt'])}, "
                         f"{_sy(v['up_ust'])}] | {_sy(v['dn'])} [{_sy(v['dn_alt'])}, {_sy(v['dn_ust'])}] |")
    s.append("")
    for sat in ("a", "b", "c"):
        s += [J["ana"][sat]["rapor"], ""]
    s += ["## Tercil sınırları (ön kayıttan)", "", "; ".join(f"{p}: {q[0]:.4f} / {q[1]:.4f}" for p, q in J["tercil"].items()), ""]
    s += d9a_sektor_bolumu()
    for b in _D9A_KORU:
        blok = _d9a_bolum_al(eski, b)
        if blok:
            s += [blok, ""]
    s += [d9a_kontrol_tablosu(), ""]
    metin = "\n".join(s)
    if _D9A_EPOSTA.search(metin):
        raise D9AHata("raporda e-posta biçimli parça var")
    with open(_d9a_yol("rapor", cikti), "w", encoding="utf-8") as f:
        f.write(metin)
    return metin


# ================================================================ 6) ÇAKIŞMA KAPISI
def _cakisma_kontrol_d9a(_once=_CK_ONCE_D9A, _dosya="D9_AVR.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_D9A", "_CK_KAYIT", "_cakisma_kontrol_d9a", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "warnings", "copy", "io", "subprocess", "_dt", "OC", "D9",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_d9a()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=D9A_SURUM)
    ap.add_argument("komut", choices=["sektor", "onkayit", "kos", "rapor"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--ham", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "sektor":
            print(json.dumps(d9a_sektor_yaz(a.ham, a.veri), ensure_ascii=False, indent=1))
        elif a.komut == "onkayit":
            print(d9a_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            R_ = d9a_kos(a.cikti, a.veri)
            print(R_["rapor"].split("## Bilgi")[0])
        else:
            print(d9a_rapor(a.cikti))
    except (D9AHata, D9.D9Hata, OC.OCHata) as ex:
        d9alog.error("%s", ex); sys.exit(1)
