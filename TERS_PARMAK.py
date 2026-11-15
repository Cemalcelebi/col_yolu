"""TERS_PARMAK — büyük mumdan GERİYE bakarak bölge parmak izi (keşif) + ileriye doğru doğrulama (15 Kasım 2026).

Cemal (15 Kas 2026): "TERSTEN gidelim: her büyük mumdan ÖNCEKİ mumların dizilimi, boyu, fitili, eğimi ölçülsün; belki büyük muma has bir
bölge profili (parmak izi) bulunur; sonra o parmak izinden büyük mum gelme olasılığı ölçülsün."

İKİ ADIM (geriye bakma yanıltmasına karşı kesin ayrım; COL_OZET ders 5):
  ADIM A — KEŞİF (yalnız ABD 2016-22 ve AVR 2016-22; 2023+ sonuç sütunları panelde MASKELİ): büyük mum (mutlak: gün gerçek aralığı >= 3 x
           ATR250 VE |getiri| >= 2 x σ250) öncesi 5 / 10 / 20 / 40 barın 30 ölçüsü vs aynı pazar, aynı takvim ayı, aynı σ250 ondalığı x
           likidite üçlüsünden rastgele kontrol günleri (büyük mum başına 5). Tek ölçü d / AUC / BH, yön ayrımı, L1 lojistik (5 kat), derinlik
           3 ağaç; aday kurallar P1-P3 bu dosyada ÖNCEDEN yazılmış arama yordamıyla (tp_kural_ara) seçilir; keşifte duyarlılık / kesinlik.
  ADIM B — DOĞRULAMA (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26 karar; BIST bilgi): ön kayıt (TERS_ON_KAYIT_B.md, kurallar sha'sı)
           commit'li ve değişmemiş olmadan çalışmaz. Profil günü t (yalnız t'ye kadar bilgi; 20 günde bir) -> 20 gün içinde büyük mum
           olasılığı vs aynı gün / σ250 ondalığı / likidite üçlüsündeki profilsiz eşler = KAT (ay kümeli bootstrap, OC.oc_kat), ilk 5 gün,
           yön payı, ORTAK_CETVEL oc_olc 60 gün eşli + olasılık tablosu (bilgi). Kör grafik seti (20 P1 + 20 kontrol, KOR_TEST v1.1 çizimi).

Komut:  python TERS_PARMAK.py kesif      ADIM A (keşif raporu + ters_kurallar.json; 2023+ sonuçları görülmez)
        python TERS_PARMAK.py onkayitB   ADIM B ön kaydı (kurallar sha, cetvel satırları, KONTROL LİSTESİ, profil günü SAYIMI; sonuç hesaplanmaz)
        python TERS_PARMAK.py dogrula    ADIM B (OC.oc_kapi + kendi mühür / git kapısı geçmezse durur)
        python TERS_PARMAK.py rapor      sonuç json'undan TERS_RAPOR.md
Colab:  exec(open('TERS_PARMAK.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   ORTAK_CETVEL.oc_veri (/tmp/veri V_*.pkl + /tmp/veri2/k34_yahoo.pkl); satır verisi /tmp/ters_parmak (repoya girmez). Tiingo YOK.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_TP = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_TP = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_TP not in sys.path:
    sys.path.insert(0, KOK_TP)

import ORTAK_CETVEL as OC  # noqa: E402

tplog = logging.getLogger("col.ters_parmak")
if not tplog.handlers:
    _tp_h = logging.StreamHandler(sys.stderr)
    _tp_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s ters_parmak: %(message)s", "%H:%M:%S"))
    tplog.addHandler(_tp_h)
    tplog.setLevel(logging.INFO)
    tplog.propagate = False

TP_SURUM = "TERS_PARMAK v1.0 (2026-11-15): büyük mum öncesi bölge parmak izi — keşif (2016-22) / ön kayıt / ileriye doğru doğrulama"
TP_YOL = {"cikti": os.path.join(KOK_TP, "arastirma_cikti", "ters_parmak"), "satir": os.environ.get("TP_SATIR", "/tmp/ters_parmak"),
          "kod": os.path.join(KOK_TP, "TERS_PARMAK.py"), "veri": os.environ.get("OC_VERI", "/tmp/veri"),
          "veri2": os.environ.get("OC_VERI2", "/tmp/veri2")}
TP_DOSYA = {"kesif_rapor": "TERS_KESIF_RAPOR.md", "kesif_json": "ters_kesif.json", "kural": "ters_kurallar.json",
            "onkayit": "TERS_ON_KAYIT_B.md", "sonuc": "ters_sonuc.json", "rapor": "TERS_RAPOR.md",
            "pdf": "TERS_ORNEK_40.pdf", "anahtar": "TERS_ORNEK_40_anahtar.json"}

# ================================================================ MÜHÜRLÜ EŞİKLER (keşiften ÖNCE yazıldı; sonuç görülünce DEĞİŞMEZ)
TP_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "buyuk": {"n": 250, "tr_kat": 3.0, "sigma_kat": 2.0, "bosluk_takvim": 7, "tekil": 20,
              "tanim": "hissenin kendi geçerli barlarında gün t: gerçek aralık TR_t = max(H_t, C_t-1) - min(L_t, C_t-1) >= 3 x ATR250(t-1) VE "
                       "|C_t / C_t-1 - 1| >= 2 x σ250(t-1); ATR250(t-1) = t-250..t-1 TR ortalaması, σ250(t-1) = t-250..t-1 günlük ln getiri std "
                       "(ddof 1); t-1 ile t arası en çok 7 takvim günü (askı / boşluk sonrası sıçrama sayılmaz); yön = getiri işareti (yukarı / aşağı "
                       "ayrı etiket). Büyük mum günü HİÇBİR ölçüye girmez (önceki pencere t-1'de biter)."},
    "pencere": [5, 10, 20, 40],
    "ohlc": "açılış ya da kapanış H-L dışında olan barlarda (AVR ~%0,2-0,4, ABD / BIST ~0) H = max(H, O, C), L = min(L, O, C)",
    "olcu": {"kucuk": 0.5, "dar_bant": 2.0, "test_tol": 0.25, "sessiz": 0.25, "hacim": [10, 50], "konum": 250, "dusus": 120},
    "uygun": {"likit_gun": 20, "likit_min": 10, "alt_kesik": 0.20, "bolunme_geri": 60, "min_bar": 251,
              "tanim": "profil / pencere son günü s (büyük mum için s = t-1): ATR250 ve σ250 tanımlı (>= 251 bar); likidite = s'de biten 20 barın "
                       "C x V (x Kur, AVR EUR) medyanı, aynı pazar aynı gün kesitinin alt %20'si dışarı; bölünme şüphesi (OC.oc_bolunme_supheli) "
                       "[s-60, s] barlarında varsa dışarı (yalnız geçmiş pencere); ABD k34 hissesi evren_bas'tan önce dışarı."},
    "kontrol": {"kat": 5, "sig_kova": 10, "lik_kova": 3, "tohum": 1515,
                "tanim": "büyük mum satırı (s = t-1) başına 5 kontrol: aynı pazar, aynı takvim ayı (yıl-ay, s'nin), aynı σ250 ondalığı x likidite "
                         "üçlüsü (kovalar pazar-ay içi uygun satırlarda), uygun, ertesi gün (s+1) büyük mum OLMAYAN satırlardan yerine koymadan "
                         "rastgele (katmanda yetmezse katmandaki hepsi)."},
    "donem": {"kesif": ["2016-01-01", "2022-12-31"], "kes": "2023-01-01",
              "karar": [["2023", "2023-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-08-31"]],
              "tarih": "dönem = s (profil / pencere son günü) tarihi; KEŞİF ve ön kayıt sayımında 'kes' gününden itibaren büyük mum etiketi "
                       "bilinmez sayılır (sonuç penceresi 2023'e taşan keşif satırının sonucu NaN)"},
    "kesif_pazar": ["ABD", "AVR"], "karar_pazar": ["ABD", "AVR"], "bilgi_pazar": ["BIST"],
    "analiz": {"bh_q": 0.10, "cv_kat": 5, "cv_tohum": 7, "l1_C": 0.05, "agac_derinlik": 3, "agac_min_yaprak": 0.01, "kirpma": [0.01, 0.99],
               "karisik_tohum": 11,
               "tanim": "tek ölçü: Cohen d (büyük - kontrol, havuzlanmış std; değerler pazar örnekleminin %1-%99 yüzdeliğine kırpılarak), AUC (sıra; Mann-Whitney normal yaklaşımı p, iki yönlü), BH q 0,10 "
                        "(pazar başına 30 ölçü); yön: yukarı vs aşağı büyük mum öncesi d / AUC / q. Çok değişkenli: ölçüler pazar içi %1-%99 "
                        "kırpılıp standartlaştırılır; L1 lojistik (C 0,05, saga, dengeli ağırlık) 5 katlı CV AUC + etiket karıştırma kontrolü; "
                        "derinlik 3 ağaç (min yaprak %1, dengeli) yalnız okunabilirlik."},
    "kural": {"aday_olcu": 8, "yuzdelik_kucuk": [0.10, 0.20, 0.30], "yuzdelik_buyuk": [0.70, 0.80, 0.90], "en_cok_kosul": 3,
              "min_duyarlilik_cc": 0.10, "n_kural": 3, "en_cok_ortak": 1,
              "tanim": "ADAY ÖLÇÜ: ABD ve AVR keşfinde ikisinde de BH q < 0,10 ve d aynı işaretli ölçüler, min(|d_ABD|, |d_AVR|) sırasıyla ilk 8. "
                       "KOŞUL: d < 0 ise 'ölçü <= eşik' (eşik = keşif kontrol satırlarının (ABD+AVR) %10 / %20 / %30 yüzdeliği), d > 0 ise "
                       "'ölçü >= eşik' (%70 / %80 / %90). KURAL: 1-3 farklı ölçünün koşullarının VE'si (8 ölçüde 1.788 kural). Her pazarda "
                       "duyarlılık_cc = P(kural | büyük mum, s = t-1), yanlış = P(kural | kontrol), LR = duyarlılık_cc / yanlış. Şart: iki "
                       "pazarda duyarlılık_cc >= %10. SKOR = min(LR_ABD, LR_AVR). P1 = en yüksek skor; P2 = P1 ile en çok 1 ortak ölçülü en "
                       "yüksek; P3 = P1 ve P2 ile en çok 1'er ortak ölçülü en yüksek (eşitlikte az koşul, sonra ad sırası)."},
    "dogrulama": {"ufuk": 20, "ilk": 5, "tekil": 20, "min_es": 3, "n_esik": 30, "duyarlilik_esik": 0.05, "kat_alt_esik": 1.0, "bh_alfa": 0.05,
                  "guc_n": 1000,
                  "tanim": "profil günü s: kural s'de doğru VE uygun; aynı hissede 20 barda bir (ilk). OLAY = s+1..s+20 barında en az bir büyük mum "
                           "(yalnız fiyat tanımı; geçerli bar), ilk 5 = s+1..s+5. EŞ = aynı gün, aynı pazar, gün içi σ250 ondalığı x likidite "
                           "üçlüsü, uygun, profil DIŞI, sonucu ölçülebilir hisseler (en az 3); eş oranı = eşlerin olay oranı. KAT = Σ olay / Σ eş "
                           "oranı (OC.oc_kat: ay kümeli bootstrap 2000, tohum 27, %95). DUYARLILIK = hücrenin uygun, 20 günde bir tekilleştirilmiş "
                           "büyük mumlarından (s = t-1 uygun) önceki 20 barda (t-20..t-1) en az bir profil günü (tekilsiz) olanların payı. "
                           "Hücre GEÇER = n >= 30 VE KAT alt uç > 1 VE duyarlılık >= %5. p_hücre = bootstrap KAT <= 1 payı ((k+1)/(B+1)); "
                           "p_kural = dört karar hücresinin en büyüğü; 3 kural BH (alfa 0,05). ETİKET: dört karar hücresi GEÇER ve BH q <= 0,05 -> "
                           "PARMAK İZİ VAR; en az bir hücre GEÇER (dördü değil ya da BH tutmaz) -> EMARE; hiçbiri geçmez ve dört hücrede n >= 1.000 "
                           "-> İZ DEĞİL (parmak izi yok, güç yeterli); aksi -> ÖLÇÜLEMEDİ. BIST bilgi."},
    "gelecek_denetimi_n": 30, "tohum": 2027,
    "kor": {"n": 20, "once": 120, "sonra": 20, "tohum": 4040, "max_mb": 8.0,
            "tanim": "doğrulama setinden (s >= 2023-01-01; ABD + AVR) P1 profil günlerinden rastgele 20 + her birinin günü ve katmanından (σ250 "
                     "ondalığı x likidite üçlüsü) rastgele bir profilsiz uygun hisse (20 kontrol); 120 bar önce + s + 20 bar sonra; KOR_TEST v1.1 "
                     "çizimi (ortak log ölçek, %10 cetveli, hisse adı / tarih yok); s'nin sağına kesikli dikey çizgi; sıra karıştırılır; anahtar ayrı json."},
}

TP_OLCU_ACIKLAMA: Dict[str, str] = {
    **{f"mum_{w}": f"son {w} barın ortalama mum boyu (H-L) / ATR250" for w in (5, 10, 20, 40)},
    **{f"egim_{w}": f"son {w} kapanışın ln doğrusal eğimi (bar başına) / σ250" for w in (5, 10, 20, 40)},
    **{f"bant_{w}": f"son {w} kapanış bandı ln(max/min) / (σ250 x √{w})" for w in (5, 10, 20, 40)},
    "kucul_20": "20 barda son 5 / ilk 5 ortalama mum boyu (küçülme eğimi)", "kucul_10": "10 barda son 5 / ilk 5 ortalama mum boyu",
    "govde_20": "20 bar ortalama gövde / aralık", "ust_fitil_20": "20 bar ortalama üst fitil / aralık", "alt_fitil_20": "20 bar ortalama alt fitil / aralık",
    "kucuk_pay_20": "20 barda küçük mum (H-L < 0,5 x ATR250) payı", "kucuk_dizi_40": "40 barda en uzun küçük mum dizisi (bar)",
    "kucuk_son": "s'de biten ardışık küçük mum sayısı (en çok 40)", "hacim_10_50": "son 10 bar ortalama hacim / son 50 bar",
    "konum_250": "kapanışın 250 bar (Low min .. High max) aralığındaki konumu (0-1)", "dusus_120": "ln(C / 120 bar High max) / (σ250 x √120)",
    "dar_bant_gun": "s'den geriye kapanış bandı (max-min) <= 2 x ATR250 kalan gün sayısı (en çok 40)",
    "alt_test_20": "20 barda Low <= pencere dibi + 0,25 x ATR250 olan bar sayısı - 1 (alt bant test sayısı)",
    "sessiz_20": "20 barda |ln getiri| < 0,25 x σ250 gün payı", "oyn_oran_20": "20 bar ln getiri std / σ250",
    "son_mum": "s günü mum boyu / ATR250", "yesil_20": "20 barda C > O payı", "bosluk_20": "20 bar ortalama |O - önceki C| / ATR250",
}
TP_OLCULER: List[str] = list(TP_OLCU_ACIKLAMA)

TP_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "keşif kontrolü: aynı pazar, aynı takvim ayı, aynı σ250 ondalığı x likidite üçlüsü, uygun, ertesi gün büyük mum olmayan rastgele "
                   "satırlar (büyük mum başına 5; tp_kesif_orneklem); doğrulama eşi: aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü, "
                   "profilsiz (tp_kural_olc). Mekanik üstünlük: büyük mum hissenin kendi ATR250 / σ250'sine göre; σ250 eşlendiği için 'oynak hisse' "
                   "etkisi dışlanır, son 20 gün oynaklığı eşlenmez (ölçü olarak raporda: oynaklık kümelenmesi). 60 gün getirisi yalnız OC.oc_olc"),
    "K2": ("EVET", "ölçüler yalnız s'ye kadar barlarla (geriye pencere; büyük mum günü hariç); büyük mum etiketi ATR / σ'yı t-1'den alır; keşif ve "
                   "ön kayıtta 2023-01-01'den sonraki büyük mum etiketleri panelde NaN (tp_panel kes); dogrula 30 rastgele profil gününde seri "
                   "s'de kesilince ölçüler ve kural aynı (tp_gelecek_denetimi; test 'geleceğe bakma'). Sınır: bölünme şüphesi tespiti 10 bar "
                   "sonrasını kullanır (cetvel ile aynı veri temizliği)"),
    "K3": ("EVET", "OC.oc_veri temiz bar (H>L, V>0, fiyat > 0); geçersiz bar atılır, büyük mum ve ölçüler yalnız geçerli barlarla; t-1 / t arası > 7 "
                   "takvim günü ise büyük mum sayılmaz (askı sonrası sıçrama)"),
    "K4": ("EVET", "büyük mum aynı hissede 20 barda bir (ilk; uygunluk süzgecinden sonra); profil günü 20 barda bir; n = bağımsız gün; 60 gün ölçüsünde "
                   "OC.oc_olc kendi 60 gün tekilleştirmesi; KAT oran-oran (ortalama) + sayılar"),
    "K5": ("EVET", "KAT ölçüsü olay olasılığıdır (fiyat girişi yok); 60 gün eşli getiri OC.oc_olc: giriş = s'den sonraki ilk geçerli bar açılışı"),
    "K6": ("EVET", "tek kip fi_k1_veri düzeltilmiş fiyat (V_*.pkl); bütün ölçüler ATR250 / σ250 ile ölçeksiz; AVR likidite x Kur (EUR); bölünme "
                   "şüphesi geçmiş pencerede dışarı; büyük mum günündeki bölünme şüphesi sayısı keşif raporunda (dışlanmaz, iş tanımı)"),
    "K7": ("EVET", "evren bugün işlem görenler (+ ABD k34 nakdi biten, yine bugün işlem gören); batanlar yok; raporda 'hayatta kalma' notu: büyük "
                   "aşağı mumlar ve 60 gün getirisi yukarı yanlı okunmalı"),
    "K8": ("EVET", "keşif 2016-22 / doğrulama 2023 ve 2024-26 ayrı; n < 30 hücre ÖLÇÜLEMEDİ; tek ölçüde BH q 0,10, kurallarda BH (3 kural); İZ DEĞİL "
                   "yalnız dört hücrede n >= 1.000; profil günü sayımı ön kayıtta sonuç hesaplanmadan"),
    "K9": ("EVET", "arama yordamı ve bütün eşikler (TP_ESIK) keşiften önce commit'li kodda; kurallar ters_kurallar.json sha256 + TP_ESIK sha + kod sha "
                   "+ cetvel üç sha ön kayıt B'de; dogrula OC.oc_kapi + tp_onkayit_dogrula (git işlenmiş / değişmemiş) geçmezse durur; "
                   "eşik doğrulama sonucuna göre oynanmaz"),
    "K10": ("UYGULANMAZ", "metin / KAP ayrıştırma yok; yalnız OHLCV; 3 büyük mum ham veriden elle doğrulanır (rapor DENETİM)"),
    "K11": ("EVET", "satır verisi /tmp/ters_parmak (keşif örneklemi, profil günleri, olaylar); 3 ölçünün d / AUC'u ve 2 hücre KAT'ı bağımsız kodla "
                    "yeniden üretilir (rapor DENETİM)"),
    "K12": ("EVET", "'parmak izi var / emare / iz değil / ölçülemedi' yalnız ön kayıtlı kuralla; KAT olasılık oranıdır, kâr değil; yön bilinmediği için "
                    "60 gün getirisi yalnız bilgi; sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_tp; yasak dosyalar (IZ_KARNE, defterler, ORTAK_CETVEL, FON_IZI, COL_v1, takip, K58, VDYT*, "
                    "SIKISMA_YENIDEN, D9_YENIDEN, K24_YENIDEN, DIP_COL_AYRIM, INTEM_ILERI) yalnız okunur / içe alınır, git diff denetimi; "
                    "e-posta / anahtar taraması testte; ücretli veri yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; araştırma ölçümü"),
}


class TPHata(RuntimeError):
    """Durdurucu hata: ön kayıt yok / sha tutmuyor / git'e işlenmemiş / geleceğe bakma denetimi tutmadı / veri yok."""


# ================================================================ 0) ORTAK
_TP_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _tp_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _tp_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for p in iter(lambda: f.read(1 << 20), b""):
            h.update(p)
    return h.hexdigest()


def tp_sha(x: Any) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")).hexdigest()


def _tp_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or TP_YOL["cikti"], TP_DOSYA[ad])


def _tp_yaz(yol: str, metin: str) -> str:
    if _TP_EPOSTA.search(metin):
        raise TPHata(f"{os.path.basename(yol)}: e-posta biçimli parça var; yazılmadı")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _tp_json(yol: str, obj: Any) -> str:
    return _tp_yaz(yol, json.dumps(obj, ensure_ascii=False, indent=1, default=_tp_kayit))


def _tp_kayit(x: Any) -> Any:
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return None if not np.isfinite(x) else float(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (pd.Timestamp, _dt.date)):
        return str(x)[:10]
    if isinstance(x, np.ndarray):
        return x.tolist()
    return str(x)


def _tp_temiz(o: Any) -> Any:
    """json için NaN / inf -> None (iç içe)."""
    if isinstance(o, dict):
        return {str(k): _tp_temiz(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_tp_temiz(v) for v in o]
    if isinstance(o, (float, np.floating)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


# ================================================================ 1) HİSSE: büyük mum + önceki pencere ölçüleri (yalnız geçmiş)
def _gecik(a: np.ndarray, k: int) -> np.ndarray:
    """Geriye gecikmeli matris: sütun j = a[i-j] (j = 0..k-1); geçersiz NaN."""
    n = len(a); M = np.full((n, k), np.nan)
    for j in range(k):
        M[j:, j] = a[:n - j] if j else a
    return M


def _ileri(a: np.ndarray, k: int) -> np.ndarray:
    """İleri matris: sütun j = a[i+1+j] (j = 0..k-1); yoksa NaN."""
    n = len(a); M = np.full((n, k), np.nan)
    for j in range(k):
        m = j + 1
        if m < n:
            M[:n - m, j] = a[m:]
    return M


def _tp_ohlc(d: pd.DataFrame) -> Tuple[np.ndarray, ...]:
    """O, H, L, C, V; açılış / kapanış H-L dışındaysa (AVR barlarının ~%0,2-0,4'ü) H = max(H, O, C), L = min(L, O, C) (aralık genişletilir)."""
    O, H, L, C, V = (d[k].to_numpy(float) for k in ("Open", "High", "Low", "Close", "Volume"))
    return O, np.fmax(H, np.fmax(O, C)), np.fmin(L, np.fmin(O, C)), C, V


def tp_buyuk(d: pd.DataFrame, E: Dict[str, Any] = TP_ESIK) -> pd.DataFrame:
    """Hisse temiz OHLCV -> her bar için ATR250, σ250 (bar dahil), TR, büyük mum (+1 / -1 / 0; ATR / σ önceki bardan; tanımsızsa NaN)."""
    B = E["buyuk"]; N = int(B["n"])
    O, H, L, C, _V = _tp_ohlc(d)
    n = len(C); Cp = np.r_[np.nan, C[:-1]]
    TR = np.fmax(H, Cp) - np.fmin(L, Cp); TR[0] = H[0] - L[0]
    with np.errstate(all="ignore"):
        lr = np.log(C / Cp)
        ret = C / Cp - 1
    A = pd.Series(TR).rolling(N, min_periods=N).mean().to_numpy()
    S = pd.Series(lr).rolling(N, min_periods=N).std(ddof=1).to_numpy()
    Ap, Sp = np.r_[np.nan, A[:-1]], np.r_[np.nan, S[:-1]]
    gun = np.r_[np.nan, np.diff(d.index.values).astype("timedelta64[D]").astype(float)] if n else np.array([])
    tanim = np.isfinite(Ap) & np.isfinite(Sp) & (Sp > 0) & (Ap > 0)
    with np.errstate(all="ignore"):
        kos = (TR >= B["tr_kat"] * Ap) & (np.abs(ret) >= B["sigma_kat"] * Sp) & (gun <= B["bosluk_takvim"])
    big = np.where(tanim, np.where(kos, np.sign(ret), 0.0), np.nan)
    return pd.DataFrame({"TR": TR, "A": A, "S": S, "big": big, "lr": lr}, index=d.index)


def tp_olculer(d: pd.DataFrame, E: Dict[str, Any] = TP_ESIK, BB: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Her bar s için 30 ölçü (yalnız s ve önceki barlar; normalleştirici ATR250(s), σ250(s))."""
    Oe = E["olcu"]
    BB = tp_buyuk(d, E) if BB is None else BB
    O, H, L, C, V = _tp_ohlc(d)
    A, S, lr = BB.A.to_numpy(), BB.S.to_numpy(), BB.lr.to_numpy()
    n = len(C); rng = H - L; Cp = np.r_[np.nan, C[:-1]]
    with np.errstate(all="ignore"):
        lnC = np.log(C)
        RG, LL, CC, LN, LR = _gecik(rng, 40), _gecik(L, 40), _gecik(C, 40), _gecik(lnC, 40), _gecik(lr, 20)
        Ac, Sc = A[:, None], S[:, None]
        F: Dict[str, np.ndarray] = {}
        for w in E["pencere"]:
            F[f"mum_{w}"] = np.mean(RG[:, :w], axis=1) / A
        for w in E["pencere"]:
            x = (w - 1 - np.arange(w)).astype(float); xc = x - x.mean(); wt = xc / np.sum(xc ** 2)
            F[f"egim_{w}"] = (LN[:, :w] @ wt) / S
        for w in E["pencere"]:
            F[f"bant_{w}"] = (np.max(LN[:, :w], axis=1) - np.min(LN[:, :w], axis=1)) / (S * math.sqrt(w))
        F["kucul_20"] = np.mean(RG[:, :5], axis=1) / np.mean(RG[:, 15:20], axis=1)
        F["kucul_10"] = np.mean(RG[:, :5], axis=1) / np.mean(RG[:, 5:10], axis=1)
        gv = np.abs(C - O) / rng; ust = (H - np.maximum(O, C)) / rng; alt = (np.minimum(O, C) - L) / rng
        F["govde_20"] = pd.Series(gv).rolling(20, min_periods=20).mean().to_numpy()
        F["ust_fitil_20"] = pd.Series(ust).rolling(20, min_periods=20).mean().to_numpy()
        F["alt_fitil_20"] = pd.Series(alt).rolling(20, min_periods=20).mean().to_numpy()
        kc = (RG < Oe["kucuk"] * Ac)
        gecerli40 = np.isfinite(RG).all(axis=1) & np.isfinite(A)
        F["kucuk_pay_20"] = np.mean(kc[:, :20], axis=1)
        run = np.zeros(n); mx = np.zeros(n)
        for j in range(40):
            run = (run + 1) * kc[:, j]; mx = np.maximum(mx, run)
        F["kucuk_dizi_40"] = mx
        F["kucuk_son"] = np.cumprod(kc, axis=1).sum(axis=1).astype(float)
        hk, hu = Oe["hacim"]
        F["hacim_10_50"] = (pd.Series(V).rolling(hk, min_periods=hk).mean() / pd.Series(V).rolling(hu, min_periods=hu).mean()).to_numpy()
        Kn = int(Oe["konum"])
        lo = pd.Series(L).rolling(Kn, min_periods=Kn).min().to_numpy(); hi = pd.Series(H).rolling(Kn, min_periods=Kn).max().to_numpy()
        F["konum_250"] = (C - lo) / (hi - lo)
        Dn = int(Oe["dusus"])
        F["dusus_120"] = (lnC - np.log(pd.Series(H).rolling(Dn, min_periods=Dn).max().to_numpy())) / (S * math.sqrt(Dn))
        cmx = np.fmax.accumulate(CC, axis=1); cmn = np.fmin.accumulate(CC, axis=1)
        F["dar_bant_gun"] = np.cumprod((cmx - cmn) <= Oe["dar_bant"] * Ac, axis=1).sum(axis=1).astype(float)
        L20 = LL[:, :20]
        F["alt_test_20"] = (np.sum(L20 <= np.min(L20, axis=1)[:, None] + Oe["test_tol"] * Ac, axis=1) - 1).astype(float)
        F["sessiz_20"] = np.mean(np.abs(LR) < Oe["sessiz"] * Sc, axis=1)
        F["oyn_oran_20"] = np.std(LR, axis=1, ddof=1) / S
        F["son_mum"] = rng / A
        F["yesil_20"] = pd.Series((C > O).astype(float)).rolling(20, min_periods=20).mean().to_numpy()
        F["bosluk_20"] = pd.Series(np.abs(O - Cp)).rolling(20, min_periods=20).mean().to_numpy() / A
    X = pd.DataFrame({k: F[k] for k in TP_OLCULER}, index=d.index)
    X[~(gecerli40 & np.isfinite(S) & (S > 0) & (A > 0))] = np.nan
    return X


def tp_hisse(d: pd.DataFrame, E: Dict[str, Any] = TP_ESIK, kes: Optional[str] = None) -> pd.DataFrame:
    """Hisse satırları s: ölçüler (geçmiş), A, S, likidite, geçmiş bölünme şüphesi, SONUÇ sütunları (ileri; kes'ten itibaren büyük mum bilinmez):
    nb1 (s+1 büyük mum yönü), f20 / f5 (s+1..s+20 / s+5 içinde büyük mum), y20 (ilk büyük mumun yönü; yoksa 0)."""
    BB = tp_buyuk(d, E); X = tp_olculer(d, E, BB); U = E["uygun"]; Dg = E["dogrulama"]
    C, V, K = d.Close.to_numpy(float), d.Volume.to_numpy(float), (d["Kur"].to_numpy(float) if "Kur" in d else np.ones(len(d)))
    X["A"] = BB.A.to_numpy(); X["S"] = BB.S.to_numpy()
    X["Lq"] = pd.Series(C * V * K).rolling(U["likit_gun"], min_periods=U["likit_min"]).median().to_numpy()
    sup = OC.oc_bolunme_supheli(C).astype(float)
    X["sup60"] = pd.Series(sup).rolling(U["bolunme_geri"] + 1, min_periods=1).max().to_numpy() > 0
    big = BB.big.to_numpy().copy()
    if kes is not None:
        big[d.index >= pd.Timestamp(kes)] = np.nan
    X["big0"] = big   # s gününün kendisi büyük mum mu (yalnız bilgi / tekilleştirme; ölçülere girmez)
    X["nb1"] = np.r_[big[1:], np.nan]
    Fw = _ileri(big, int(Dg["ufuk"]))
    ab = np.abs(Fw); bil = np.isfinite(ab).all(axis=1)
    X["f20"] = np.where(bil, (ab == 1).any(axis=1).astype(float), np.nan)
    X["f5"] = np.where(np.isfinite(ab[:, :Dg["ilk"]]).all(axis=1), (ab[:, :Dg["ilk"]] == 1).any(axis=1).astype(float), np.nan)
    ilk = np.argmax(ab == 1, axis=1); var = (ab == 1).any(axis=1)
    X["y20"] = np.where(bil, np.where(var, Fw[np.arange(len(big)), ilk], 0.0), np.nan)
    X["i"] = np.arange(len(d))
    return X


# ================================================================ 2) PANEL (pazar; uzun biçim)
def tp_panel(Vd: Dict[str, Any], E: Dict[str, Any] = TP_ESIK, kes: Optional[str] = None, bas: str = "2015-01-01") -> pd.DataFrame:
    """Pazarın bütün hisse satırları (s >= bas ve >= 251 bar): ölçüler (float32), sonuçlar, uygunluk, kovalar (ay içi ve gün içi)."""
    V = Vd["V"]; evb = Vd.get("evren_bas", {}); U = E["uygun"]; Kt = E["kontrol"]
    parca, semboller = [], sorted(V)
    for sid, s in enumerate(semboller):
        d = V[s]
        if len(d) < U["min_bar"]:
            continue
        try:
            X = tp_hisse(d, E, kes)
        except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer
            tplog.warning("%s %s atlandı: %s", Vd.get("pazar"), s, ex); continue
        X = X[(X.index >= pd.Timestamp(bas)) & np.isfinite(X.A.to_numpy()) & np.isfinite(X.S.to_numpy())]
        if s in evb:
            X = X[X.index >= pd.Timestamp(evb[s])]
        if not len(X):
            continue
        X = X.reset_index().rename(columns={X.index.name or "index": "tarih"})
        X.insert(0, "sid", sid)
        parca.append(X)
    if not parca:
        raise TPHata(f"{Vd.get('pazar')}: panel boş")
    T = pd.concat(parca, ignore_index=True)
    T["tarih"] = pd.to_datetime(T["tarih"])
    for k in TP_OLCULER:
        T[k] = T[k].astype(np.float32)
    T["sid"] = T.sid.astype(np.int32); T["i"] = T.i.astype(np.int32)
    T.attrs["sembol"] = semboller; T.attrs["pazar"] = Vd.get("pazar", "?")
    # likidite alt %20 (gün kesiti; ATR / σ tanımlı ve likiditesi sonlu satırlar)
    lq_ok = np.isfinite(T.Lq.to_numpy())
    q = T[lq_ok].groupby("tarih").Lq.quantile(U["alt_kesik"])
    T["lik_alt"] = ~lq_ok | (T.Lq.to_numpy() < T.tarih.map(q).to_numpy())
    oz = np.isfinite(T[TP_OLCULER].to_numpy(np.float32)).all(axis=1)
    T["uygun"] = ~T.lik_alt.to_numpy() & ~T.sup60.to_numpy() & oz
    T["ay"] = T.tarih.dt.to_period("M").astype(str)
    # kovalar: yalnız uygun satırlarda; ay içi (keşif kontrolü) ve gün içi (doğrulama eşi)
    T["sig_ay"] = -1; T["lik_ay"] = -1; T["sig_gun"] = -1; T["lik_gun"] = -1
    u = T.uygun.to_numpy()
    Tu = T.loc[u, ["ay", "tarih", "S", "Lq"]]
    for grp, ks, kl in (("ay", "sig_ay", "lik_ay"), ("tarih", "sig_gun", "lik_gun")):
        g = Tu.groupby(grp)
        rs = g.S.rank(method="first", pct=True).to_numpy(); rl = g.Lq.rank(method="first", pct=True).to_numpy()
        T.loc[u, ks] = np.minimum((rs * Kt["sig_kova"]).astype(int), Kt["sig_kova"] - 1)
        T.loc[u, kl] = np.minimum((rl * Kt["lik_kova"]).astype(int), Kt["lik_kova"] - 1)
    T["kat_ay"] = np.where(u, T.sig_ay * Kt["lik_kova"] + T.lik_ay, -1)
    T["kat_gun"] = np.where(u, T.sig_gun * Kt["lik_kova"] + T.lik_gun, -1)
    return T


def tp_tekil(sid: np.ndarray, i: np.ndarray, aralik: int) -> np.ndarray:
    """Aynı hissede (sid) bar sırası i ile ilk satır tutulur; sonraki en az `aralik` bar sonra. Girdi sid, i sırasında olmalı."""
    tut = np.zeros(len(sid), bool); son_s, son_i = -1, -10 ** 9
    for k in range(len(sid)):
        if sid[k] != son_s or i[k] - son_i >= aralik:
            tut[k] = True; son_s, son_i = sid[k], i[k]
    return tut


def tp_buyuk_satir(T: pd.DataFrame, E: Dict[str, Any] = TP_ESIK) -> np.ndarray:
    """Uygun ve s+1'de büyük mum olan satırlar, aynı hissede 20 barda bir (s = t-1 sırası). Döner bool maske."""
    m = T.uygun.to_numpy() & np.isfinite(T.nb1.to_numpy()) & (np.abs(T.nb1.to_numpy()) == 1)
    out = np.zeros(len(T), bool); ix = np.flatnonzero(m)
    if len(ix):
        out[ix[tp_tekil(T.sid.to_numpy()[ix], T.i.to_numpy()[ix], E["buyuk"]["tekil"])]] = True
    return out


# ================================================================ 3) KEŞİF ÖRNEKLEMİ
def tp_kesif_orneklem(T: pd.DataFrame, E: Dict[str, Any] = TP_ESIK, bas: Optional[str] = None, son: Optional[str] = None) -> pd.DataFrame:
    """Büyük mum satırları (s = t-1; tekil) + aynı pazar / ay / σ250 ondalığı x likidite üçlüsünden 5 kontrol (ertesi gün büyük mum yok)."""
    bas = bas or E["donem"]["kesif"][0]; son = son or E["donem"]["kesif"][1]
    dm = (T.tarih >= pd.Timestamp(bas)) & (T.tarih <= pd.Timestamp(son))
    bm = tp_buyuk_satir(T, E) & dm.to_numpy()
    km = T.uygun.to_numpy() & dm.to_numpy() & (T.nb1.to_numpy() == 0)
    rng = np.random.default_rng(E["kontrol"]["tohum"])
    B = T.loc[bm, ["ay", "kat_ay"]]; Kd = T.loc[km, ["ay", "kat_ay"]]
    ihtiyac = B.groupby(["ay", "kat_ay"]).size() * E["kontrol"]["kat"]
    havuz = Kd.groupby(["ay", "kat_ay"]).indices
    sec = []
    for key, k in ihtiyac.sort_index().items():
        h = havuz.get(key)
        if h is None:
            continue
        ix = Kd.index.to_numpy()[h]
        sec.append(ix if len(ix) <= k else rng.choice(ix, int(k), replace=False))
    kix = np.sort(np.concatenate(sec)) if sec else np.array([], int)
    X = pd.concat([T.loc[bm].assign(grup="BUYUK"), T.loc[kix].assign(grup="KONTROL")], ignore_index=True)
    X["yon"] = np.where(X.grup == "BUYUK", np.where(X.nb1 > 0, "YUKARI", "ASAGI"), "")
    X["pazar"] = T.attrs.get("pazar", "?")
    X["sembol"] = [T.attrs["sembol"][s] for s in X.sid.to_numpy()]
    return X


# ================================================================ 4) TEK ÖLÇÜ ANALİZİ
def tp_auc(a: np.ndarray, b: np.ndarray) -> Tuple[float, float]:
    """AUC = P(a > b) + 0,5 P(eşit) (sıra), iki yönlü Mann-Whitney normal yaklaşımı p (bağ düzeltmesi)."""
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]; n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return np.nan, np.nan
    r = pd.Series(np.r_[a, b]).rank(method="average").to_numpy()
    U = r[:n1].sum() - n1 * (n1 + 1) / 2; auc = U / (n1 * n2)
    _, c = np.unique(np.r_[a, b], return_counts=True); N = n1 + n2
    sd = math.sqrt(n1 * n2 / 12.0 * ((N + 1) - np.sum(c ** 3 - c) / (N * (N - 1))))
    if sd <= 0:
        return auc, np.nan
    z = (U - n1 * n2 / 2) / sd
    return float(auc), float(math.erfc(abs(z) / math.sqrt(2)))


def tp_cohen_d(a: np.ndarray, b: np.ndarray) -> float:
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    sp = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return float((a.mean() - b.mean()) / sp) if sp > 0 else np.nan


def tp_bh(p: np.ndarray) -> np.ndarray:
    """Benjamini-Hochberg q değerleri (NaN korunur)."""
    p = np.asarray(p, float); q = np.full(len(p), np.nan); ok = np.isfinite(p); m = int(ok.sum())
    if not m:
        return q
    pv = p[ok]; o = np.argsort(pv); r = pv[o] * m / np.arange(1, m + 1)
    r = np.minimum.accumulate(r[::-1])[::-1]; qq = np.empty(m); qq[o] = np.minimum(r, 1.0)
    q[ok] = qq
    return q


def tp_tek_olcu(X: pd.DataFrame, E: Dict[str, Any] = TP_ESIK) -> pd.DataFrame:
    """Pazar başına (ve ABD+AVR havuzu) her ölçü: büyük vs kontrol, yukarı vs kontrol, aşağı vs kontrol, yukarı vs aşağı: d, AUC, p, BH q."""
    sat = []
    for pz in sorted(set(X.pazar)) + (["HAVUZ"] if X.pazar.nunique() > 1 else []):
        x = X if pz == "HAVUZ" else X[X.pazar == pz]
        b, k = x[x.grup == "BUYUK"], x[x.grup == "KONTROL"]; yu, ya = b[b.yon == "YUKARI"], b[b.yon == "ASAGI"]
        for o in TP_OLCULER:
            r = {"pazar": pz, "olcu": o, "n_buyuk": len(b), "n_kontrol": len(k), "n_yukari": len(yu), "n_asagi": len(ya),
                 "ort_buyuk": float(np.nanmean(b[o])), "ort_kontrol": float(np.nanmean(k[o])),
                 "med_buyuk": float(np.nanmedian(b[o])), "med_kontrol": float(np.nanmedian(k[o]))}
            lo, hi = np.nanquantile(x[o].to_numpy(float), E["analiz"]["kirpma"])
            for ad, a1, a2 in (("", b, k), ("yu_", yu, k), ("ya_", ya, k), ("yy_", yu, ya)):
                v1, v2 = a1[o].to_numpy(float), a2[o].to_numpy(float)
                r[f"{ad}d"] = tp_cohen_d(np.clip(v1, lo, hi), np.clip(v2, lo, hi)); r[f"{ad}auc"], r[f"{ad}p"] = tp_auc(v1, v2)
            sat.append(r)
    R = pd.DataFrame(sat)
    for ad in ("", "yu_", "ya_", "yy_"):
        R[f"{ad}q"] = np.nan
        for pz in R.pazar.unique():
            m = R.pazar == pz
            R.loc[m, f"{ad}q"] = tp_bh(R.loc[m, f"{ad}p"].to_numpy())
    return R


# ================================================================ 5) ÇOK DEĞİŞKENLİ (L1 lojistik, ağaç)
def _tp_matris(x: pd.DataFrame, E: Dict[str, Any]) -> np.ndarray:
    Z = x[TP_OLCULER].to_numpy(float).copy(); lo, hi = E["analiz"]["kirpma"]
    for j in range(Z.shape[1]):
        a, b = np.nanquantile(Z[:, j], [lo, hi]); Z[:, j] = np.clip(Z[:, j], a, b)
        sd = np.nanstd(Z[:, j]); Z[:, j] = (Z[:, j] - np.nanmean(Z[:, j])) / (sd if sd > 0 else 1.0)
    return np.nan_to_num(Z)


def tp_cok_degiskenli(X: pd.DataFrame, E: Dict[str, Any] = TP_ESIK) -> Dict[str, Any]:
    """L1 lojistik 5 katlı CV AUC (+ etiket karıştırma), sıfır olmayan katsayılar; derinlik 3 ağaç metni. sklearn yoksa 'atlandı'."""
    warnings.filterwarnings("ignore")
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import roc_auc_score
        from sklearn.model_selection import StratifiedKFold
        from sklearn.tree import DecisionTreeClassifier, export_text
    except ImportError:
        tplog.warning("sklearn yok: çok değişkenli analiz atlandı")
        return {"atlandi": "sklearn yok"}
    Aa = E["analiz"]; out: Dict[str, Any] = {}
    for pz in sorted(set(X.pazar)) + (["HAVUZ"] if X.pazar.nunique() > 1 else []):
        x = X if pz == "HAVUZ" else X[X.pazar == pz]
        Z = _tp_matris(x, E); y = (x.grup == "BUYUK").to_numpy(int)
        kf = StratifiedKFold(Aa["cv_kat"], shuffle=True, random_state=Aa["cv_tohum"])
        auc, auc_k = [], []; rng = np.random.default_rng(Aa["karisik_tohum"]); yk = rng.permutation(y)
        for tr, te in kf.split(Z, y):
            m = LogisticRegression(penalty="l1", C=Aa["l1_C"], solver="saga", class_weight="balanced", max_iter=300, tol=1e-3)
            m.fit(Z[tr], y[tr]); auc.append(roc_auc_score(y[te], m.decision_function(Z[te])))
            mk = LogisticRegression(penalty="l1", C=Aa["l1_C"], solver="saga", class_weight="balanced", max_iter=300, tol=1e-3)
            mk.fit(Z[tr], yk[tr]); auc_k.append(roc_auc_score(yk[te], mk.decision_function(Z[te])))
        m = LogisticRegression(penalty="l1", C=Aa["l1_C"], solver="saga", class_weight="balanced", max_iter=300, tol=1e-3).fit(Z, y)
        kat = {o: float(c) for o, c in zip(TP_OLCULER, m.coef_[0]) if abs(c) > 1e-6}
        agac = DecisionTreeClassifier(max_depth=Aa["agac_derinlik"], min_samples_leaf=Aa["agac_min_yaprak"], class_weight="balanced",
                                      random_state=Aa["cv_tohum"]).fit(x[TP_OLCULER].to_numpy(float), y)
        out[pz] = {"n": int(len(y)), "n_buyuk": int(y.sum()), "cv_auc": float(np.mean(auc)), "cv_auc_kat": [float(a) for a in auc],
                   "karisik_auc": float(np.mean(auc_k)),
                   "katsayi": dict(sorted(kat.items(), key=lambda kv: -abs(kv[1]))),
                   "agac": export_text(agac, feature_names=TP_OLCULER, decimals=3),
                   "agac_auc_icerde": float(roc_auc_score(y, agac.predict_proba(x[TP_OLCULER].to_numpy(float))[:, 1]))}
        tplog.info("çok değişkenli %s: CV AUC %.3f (karışık %.3f)", pz, out[pz]["cv_auc"], out[pz]["karisik_auc"])
    return out


# ================================================================ 6) KURAL ARAMA (önceden yazılı yordam; yalnız keşif örneklemi)
def tp_kural_uygula(T: pd.DataFrame, kural: Dict[str, Any]) -> np.ndarray:
    """Kural koşullarının VE'si (ölçü NaN ise yanlış)."""
    m = np.ones(len(T), bool)
    for k in kural["kosul"]:
        v = T[k["olcu"]].to_numpy(float)
        with np.errstate(invalid="ignore"):
            m &= (v <= k["esik"]) if k["yon"] == "<=" else (v >= k["esik"])
    return m


def tp_kural_metin(kural: Dict[str, Any]) -> str:
    return " VE ".join(f"{k['olcu']} {k['yon']} {k['esik']:.4g} (kontrol %{int(round(100 * k['yuzdelik']))})" for k in kural["kosul"])


def tp_kural_ara(X: pd.DataFrame, tek: pd.DataFrame, E: Dict[str, Any] = TP_ESIK) -> Dict[str, Any]:
    """TP_ESIK['kural'] yordamı: aday ölçüler -> 1-3 koşullu kurallar -> iki pazarda duyarlılık_cc >= %10 -> skor min LR -> P1, P2, P3."""
    Kr = E["kural"]; Pz = E["kesif_pazar"]
    t = tek[tek.pazar.isin(Pz)].pivot(index="olcu", columns="pazar")
    aday = []
    for o in TP_OLCULER:
        d = [t.loc[o, ("d", p)] for p in Pz]; q = [t.loc[o, ("q", p)] for p in Pz]
        if all(np.isfinite(d)) and all(qq < E["analiz"]["bh_q"] for qq in q) and len({np.sign(v) for v in d}) == 1:
            aday.append((o, float(min(abs(v) for v in d)), float(np.sign(d[0]))))
    aday = sorted(aday, key=lambda r: (-r[1], r[0]))[:Kr["aday_olcu"]]
    kx = X[X.grup == "KONTROL"]; kosullar = []
    for o, _, sg in aday:
        yz = Kr["yuzdelik_kucuk"] if sg < 0 else Kr["yuzdelik_buyuk"]
        for y in yz:
            kosullar.append({"olcu": o, "yon": "<=" if sg < 0 else ">=", "yuzdelik": float(y), "esik": float(np.nanquantile(kx[o].to_numpy(float), y))})
    Mb = {k["olcu"] + k["yon"] + str(k["yuzdelik"]): tp_kural_uygula(X, {"kosul": [k]}) for k in kosullar}
    pzr = X.pazar.to_numpy(); buy = (X.grup == "BUYUK").to_numpy()
    maske = {p: (pzr == p) for p in Pz}
    adaylar = []
    olcu_ad = [a[0] for a in aday]
    for r in range(1, Kr["en_cok_kosul"] + 1):
        for oset in itertools.combinations(olcu_ad, r):
            secenek = [[k for k in kosullar if k["olcu"] == o] for o in oset]
            for kk in itertools.product(*secenek):
                m = np.ones(len(X), bool)
                for k in kk:
                    m &= Mb[k["olcu"] + k["yon"] + str(k["yuzdelik"])]
                cc = {}
                for p in Pz:
                    b = maske[p] & buy; c = maske[p] & ~buy
                    sens = float(m[b].mean()) if b.any() else np.nan; fpr = float(m[c].mean()) if c.any() else np.nan
                    cc[p] = {"duyarlilik_cc": sens, "yanlis_cc": fpr, "LR": sens / fpr if fpr and fpr > 0 else np.nan}
                if not all(np.isfinite(cc[p]["LR"]) and cc[p]["duyarlilik_cc"] >= Kr["min_duyarlilik_cc"] for p in Pz):
                    continue
                ad = " & ".join(f"{k['olcu']}{k['yon']}q{int(round(100 * k['yuzdelik']))}" for k in kk)
                adaylar.append({"ad": ad, "kosul": [dict(k) for k in kk], "olcu_set": list(oset), "cc": cc,
                                "skor": float(min(cc[p]["LR"] for p in Pz))})
    adaylar.sort(key=lambda a: (-a["skor"], len(a["kosul"]), a["ad"]))
    secilen: List[Dict[str, Any]] = []
    for a in adaylar:
        if len(secilen) >= Kr["n_kural"]:
            break
        if all(len(set(a["olcu_set"]) & set(s["olcu_set"])) <= Kr["en_cok_ortak"] for s in secilen):
            secilen.append(a)
    for i, s in enumerate(secilen, 1):
        s["kod"] = f"P{i}"
    return {"aday_olcu": [{"olcu": o, "min_abs_d": m, "isaret": sg} for o, m, sg in aday], "n_aday_kural": len(adaylar),
            "kurallar": secilen, "ilk20": [{k: a[k] for k in ("ad", "skor", "cc")} for a in adaylar[:20]]}


# ================================================================ 7) KURAL ÖLÇÜMÜ (keşifte ve doğrulamada AYNI fonksiyon)
def _tp_kapsar(T: pd.DataFrame, flag: np.ndarray, gun: int) -> np.ndarray:
    """Satır s için [s-gun+1, s] (aynı hisse) içinde flag var mı. T sid, i sırasında."""
    P = np.r_[0, np.cumsum(flag.astype(np.int64))]; r = np.arange(len(T))
    bas = np.r_[0, np.flatnonzero(np.diff(T.sid.to_numpy())) + 1]
    ilk = np.repeat(bas, np.diff(np.r_[bas, len(T)]))   # hissenin ilk satırı (satırlar hisse içinde ardışık barlar)
    lo = np.maximum(r - gun + 1, ilk)
    return (P[r + 1] - P[lo]) > 0


def tp_kat_p(olay: np.ndarray, oran: np.ndarray, ay: np.ndarray, E: Dict[str, Any] = OC.OC_ESIK) -> Dict[str, float]:
    """OC.oc_kat ile AYNI yeniden örnekleme (ay kümeli, 2000, tohum 27): KAT, %95 ve tek yönlü p = (#boot KAT <= 1 + 1) / (B + 1)."""
    r = OC.oc_kat(olay, oran, ay, E)
    O = E["olcu"]; g = np.isfinite(olay) & np.isfinite(oran)
    a, b, m = olay[g].astype(float), oran[g].astype(float), ay[g]
    if not len(a) or b.sum() <= 0:
        r["p"] = np.nan; return r
    aylar = np.unique(m); ga = np.array([a[m == x].sum() for x in aylar]); gb = np.array([b[m == x].sum() for x in aylar])
    rng = np.random.default_rng(O["tohum"]); v = np.empty(O["bootstrap"])
    for k in range(O["bootstrap"]):
        sec = rng.choice(len(aylar), len(aylar), replace=True)
        pb = gb[sec].sum(); v[k] = ga[sec].sum() / pb if pb > 0 else np.nan
    v = v[np.isfinite(v)]
    r["p"] = float((np.sum(v <= 1.0) + 1) / (len(v) + 1)) if len(v) else np.nan
    r["alt_kontrol"] = float(np.quantile(v, O["guven"][0])) if len(v) else np.nan
    return r


def tp_kural_olc(T: pd.DataFrame, kural: Dict[str, Any], donemler: List[List[str]], E: Dict[str, Any] = TP_ESIK,
                 satir_don: bool = False) -> Dict[str, Any]:
    """Bir kuralın pazar panelinde dönem dönem ölçümü: profil günü (tekil 20), KAT (20 gün / ilk 5), eş oranı, duyarlılık, taban, yön."""
    Dg = E["dogrulama"]
    kur = tp_kural_uygula(T, kural)
    pf = kur & T.uygun.to_numpy()
    tek = np.zeros(len(T), bool); ix = np.flatnonzero(pf)
    if len(ix):
        tek[ix[tp_tekil(T.sid.to_numpy()[ix], T.i.to_numpy()[ix], Dg["tekil"])]] = True
    # eşler: aynı gün, aynı kat_gun, uygun, profil dışı, sonucu ölçülebilir
    es_m = T.uygun.to_numpy() & ~kur
    out: Dict[str, Any] = {}; sat_l = []
    kapsar = _tp_kapsar(T, pf, Dg["ufuk"])
    bmask = tp_buyuk_satir(T, E)
    for ad, bas, son in donemler:
        dm = ((T.tarih >= pd.Timestamp(bas)) & (T.tarih <= pd.Timestamp(son))).to_numpy()
        r: Dict[str, Any] = {"donem": ad, "profil_gunu_tekilsiz": int((pf & dm).sum()), "profil_gunu": int((tek & dm).sum()),
                             "uygun_satir": int((T.uygun.to_numpy() & dm).sum())}
        r["profil_pay"] = r["profil_gunu_tekilsiz"] / r["uygun_satir"] if r["uygun_satir"] else np.nan
        bb = bmask & dm
        r["buyuk_mum"] = int(bb.sum()); r["duyarlilik"] = float(kapsar[bb].mean()) if bb.any() else np.nan
        r["duyarlilik_t1"] = float(pf[bb].mean()) if bb.any() else np.nan
        for kol, ek in (("f20", ""), ("f5", "_5")):
            v = T[kol].to_numpy()
            tb = T.uygun.to_numpy() & dm & np.isfinite(v)
            r[f"taban{ek}"] = float(v[tb].mean()) if tb.any() else np.nan
            em = es_m & dm & np.isfinite(v)
            Es = pd.DataFrame({"tarih": T.tarih.to_numpy()[em], "kat": T.kat_gun.to_numpy()[em], "v": v[em]}).groupby(["tarih", "kat"]).v.agg(["sum", "count"])
            P_ = pd.DataFrame({"tarih": T.tarih.to_numpy()[tek & dm], "kat": T.kat_gun.to_numpy()[tek & dm], "v": v[tek & dm],
                               "sid": T.sid.to_numpy()[tek & dm], "ay": T.ay.to_numpy()[tek & dm]})
            P_ = P_.join(Es, on=["tarih", "kat"])
            P_["es"] = np.where(P_["count"] >= Dg["min_es"], P_["sum"] / P_["count"], np.nan)
            g = np.isfinite(P_.v.to_numpy()) & np.isfinite(P_.es.to_numpy())
            r[f"n{ek}"] = int(g.sum())
            k = tp_kat_p(P_.v.to_numpy(float), P_.es.to_numpy(float), P_.ay.to_numpy())
            r[f"p_olay{ek}"] = k.get("p_olay"); r[f"p_es{ek}"] = k.get("p_ref"); r[f"kat{ek}"] = k.get("kat")
            r[f"alt{ek}"] = k.get("alt"); r[f"ust{ek}"] = k.get("ust"); r[f"p{ek}"] = k.get("p")
            if kol == "f20":
                r["olcum_disi"] = int((~g).sum())
                if satir_don:
                    P_["pazar"] = T.attrs.get("pazar", "?"); P_["donem"] = ad
                    P_["sembol"] = [T.attrs["sembol"][s] for s in P_.sid.to_numpy()]
                    sat_l.append(P_)
        # yön: büyük mumla biten profil günlerinde ilk büyük mumun yukarı payı vs eş (aynı günler, profilsiz uygun, büyük mumla biten)
        y = T.y20.to_numpy(); f = T.f20.to_numpy()
        py = tek & dm & (f == 1); ey = es_m & dm & (f == 1)
        gunler = np.unique(T.tarih.to_numpy()[py])
        ey &= np.isin(T.tarih.to_numpy(), gunler)
        r["yukari_pay"] = float((y[py] > 0).mean()) if py.any() else np.nan
        r["yukari_pay_es"] = float((y[ey] > 0).mean()) if ey.any() else np.nan
        r["n_yon"] = int(py.sum())
        alt_ = r["alt"]; du_ = r["duyarlilik"]
        r["gecer"] = bool(r["n"] >= Dg["n_esik"] and alt_ is not None and np.isfinite(alt_) and alt_ > Dg["kat_alt_esik"]
                          and du_ is not None and np.isfinite(du_) and du_ >= Dg["duyarlilik_esik"])
        out[ad] = _tp_temiz(r)
    res = {"hucre": out, "profil_tekil_maske": tek if satir_don else None}
    if satir_don:
        res["satir"] = pd.concat(sat_l, ignore_index=True) if sat_l else pd.DataFrame()
    return res


def tp_kural_etiket(H: Dict[str, Dict[str, Any]], q: float, E: Dict[str, Any] = TP_ESIK) -> str:
    """H: 'ABD 2023' ... -> hücre ölçümü; q: kuralın BH q'su."""
    Dg = E["dogrulama"]; kh = [f"{p} {d[0]}" for p in E["karar_pazar"] for d in E["donem"]["karar"]]
    gec = [bool(H.get(k, {}).get("gecer")) for k in kh]
    if all(gec) and np.isfinite(q) and q <= Dg["bh_alfa"]:
        return "PARMAK İZİ VAR"
    if any(gec):
        return "EMARE"
    if all((H.get(k, {}).get("n") or 0) >= Dg["guc_n"] for k in kh):
        return "İZ DEĞİL"
    return "ÖLÇÜLEMEDİ"


# ================================================================ 8) VERİ
def tp_veri(pazar: str, veri: Optional[str] = None, veri2: Optional[str] = None) -> Dict[str, Any]:
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    return OC.oc_veri(pazar, klasor=veri or TP_YOL["veri"], veri2=veri2 or TP_YOL["veri2"])


# ================================================================ 9) ADIM A — KEŞİF
def tp_kesif(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    """Keşif: yalnız 2016-22 satırları; panel 2023-01-01 'kes' ile kurulur (2023+ büyük mum etiketleri NaN). Kod git'e işlenmiş olmalı."""
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    kz = _tp_simdi(); kod_git = OC._oc_git_islenmis(TP_YOL["kod"]) if git else {}
    satir = TP_YOL["satir"]; os.makedirs(satir, exist_ok=True)
    kes = TP_ESIK["donem"]["kes"]; Xs, bilgi, TT = [], {}, {}
    for p in TP_ESIK["kesif_pazar"]:
        Vd = tp_veri(p, veri)
        T = tp_panel(Vd, kes=kes); del Vd; TT[p] = T
        X = tp_kesif_orneklem(T)
        bm = X.grup == "BUYUK"
        bilgi[p] = {"satir": int(len(T)), "uygun_kesif": int((T.uygun & (T.tarih <= TP_ESIK["donem"]["kesif"][1]) & (T.tarih >= TP_ESIK["donem"]["kesif"][0])).sum()),
                    "buyuk": int(bm.sum()), "yukari": int((X.yon == "YUKARI").sum()), "asagi": int((X.yon == "ASAGI").sum()),
                    "kontrol": int((~bm).sum()), "buyuk_ham_kesif": int(((np.abs(T.nb1) == 1) & (T.tarih <= TP_ESIK["donem"]["kesif"][1])
                                                                         & (T.tarih >= TP_ESIK["donem"]["kesif"][0])).sum()),
                    "hisse": int(T.sid.nunique())}
        Xs.append(X); tplog.info("keşif %s: %s (%.0f sn)", p, bilgi[p], time.time() - t0)
    X = pd.concat(Xs, ignore_index=True)
    X.to_csv(os.path.join(satir, "kesif_orneklem.csv.gz"), index=False)
    tek = tp_tek_olcu(X); tek.to_csv(os.path.join(satir, "kesif_tek_olcu.csv"), index=False)
    cok = tp_cok_degiskenli(X)
    ara = tp_kural_ara(X, tek)
    if not ara["kurallar"]:
        tplog.warning("keşif: şartı geçen aday kural yok")
    # keşifte tam ölçüm: duyarlılık / kesinlik (2016-22; aynı tp_kural_olc)
    kesif_olc: Dict[str, Any] = {}
    for p in TP_ESIK["kesif_pazar"]:
        T = TT.pop(p)
        for kr in ara["kurallar"]:
            kesif_olc.setdefault(kr["kod"], {})[p] = tp_kural_olc(T, kr, [["2016-22"] + TP_ESIK["donem"]["kesif"]])["hucre"]["2016-22"]
        del T
    kur_json = {"surum": TP_SURUM, "esik_sha": tp_sha(TP_ESIK), "kod_sha": _tp_sha_dosya(TP_YOL["kod"]), "kesif_zaman_utc": kz,
                "kod_git": kod_git, "kurallar": [{k: v for k, v in kr.items() if k in ("kod", "ad", "kosul", "olcu_set", "cc", "skor")}
                                                for kr in ara["kurallar"]]}
    _tp_json(_tp_yol("kural", cikti), _tp_temiz(kur_json))
    J = {"surum": TP_SURUM, "zaman_utc": kz, "kod_git": kod_git, "bilgi": bilgi, "tek": json.loads(tek.to_json(orient="records")),
         "cok": cok, "arama": _tp_temiz({k: v for k, v in ara.items() if k != "kurallar"}), "kurallar": _tp_temiz(kur_json["kurallar"]),
         "kesif_olc": kesif_olc, "sure_sn": round(time.time() - t0, 1)}
    _tp_json(_tp_yol("kesif_json", cikti), _tp_temiz(J))
    md = tp_kesif_rapor(J)
    _tp_yaz(_tp_yol("kesif_rapor", cikti), md)
    return J


def _yz(x: Any, n: int = 1) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"%{100 * x:.{n}f}".replace(".", ",")


def _sy(x: Any, n: int = 2) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


def _tp_q(x: Any) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else ("<0,001" if x < 0.001 else f"{x:.3f}".replace(".", ","))


def tp_kesif_rapor(J: Dict[str, Any]) -> str:
    tek = pd.DataFrame(J["tek"])
    s = ["# TERS PARMAK İZİ — ADIM A KEŞİF RAPORU (ABD ve AVR 2016-22)", "",
         f"{TP_SURUM}. Keşif koşusu {J['zaman_utc']} (kod commit {str(J.get('kod_git', {}).get('commit', '-'))[:10]}). "
         "Panel 2023-01-01 'kes' ile kuruldu: 2023 ve sonrasının büyük mum etiketleri bu adımda görülmedi.", "",
         "## Örneklem", "", "| Pazar | hisse | uygun satır 2016-22 | büyük mum (ham, s+1) | büyük mum (uygun, 20 günde bir) | yukarı / aşağı | kontrol |",
         "|---|---|---|---|---|---|---|"]
    for p, b in J["bilgi"].items():
        s.append(f"| {p} | {b['hisse']} | {b['uygun_kesif']} | {b['buyuk_ham_kesif']} | {b['buyuk']} | {b['yukari']} / {b['asagi']} | {b['kontrol']} |")
    s += ["", "Büyük mum: gün gerçek aralığı >= 3 x ATR250 VE |getiri| >= 2 x σ250 (ATR / σ önceki 250 bardan). Önceki pencere büyük mum gününü "
          "içermez (s = t-1'de biter). Kontrol: aynı pazar / takvim ayı / σ250 ondalığı x likidite üçlüsü, ertesi gün büyük mum olmayan günler (5 kat).", ""]
    for pz in ["HAVUZ"] + list(J["bilgi"]):
        x = tek[tek.pazar == pz].copy()
        if not len(x):
            continue
        x["abs_d"] = x.d.abs(); x = x.sort_values("abs_d", ascending=False)
        s += [f"## Tek ölçü: büyük mum öncesi vs kontrol — {pz} (|d| sırasıyla)", "",
              "| # | ölçü | ort büyük / kontrol | d | AUC | q | yukarı d | aşağı d | yukarı vs aşağı d (AUC, q) |", "|---|---|---|---|---|---|---|---|---|"]
        for k, r in enumerate(x.itertuples(), 1):
            s.append(f"| {k} | {r.olcu} | {_sy(r.ort_buyuk, 3)} / {_sy(r.ort_kontrol, 3)} | {_sy(r.d, 3)} | {_sy(r.auc, 3)} | {_tp_q(r.q)} | "
                     f"{_sy(r.yu_d, 3)} | {_sy(r.ya_d, 3)} | {_sy(r.yy_d, 3)} ({_sy(r.yy_auc, 3)}, {_tp_q(r.yy_q)}) |")
        s.append("")
    s += ["## Çok değişkenli (L1 lojistik 5 katlı CV; derinlik 3 ağaç yalnız okunabilirlik)", ""]
    for pz, c in J["cok"].items():
        if not isinstance(c, dict):
            continue
        s += [f"### {pz}", "", f"n {c['n']} (büyük {c['n_buyuk']}); CV AUC **{_sy(c['cv_auc'], 3)}** (katlar {', '.join(_sy(a, 3) for a in c['cv_auc_kat'])}); "
              f"etiket karıştırılınca {_sy(c['karisik_auc'], 3)}; ağaç (içeride) AUC {_sy(c['agac_auc_icerde'], 3)}.", "",
              "Sıfır olmayan katsayılar (standart ölçek): " + ", ".join(f"{k} {_sy(v, 3)}" for k, v in list(c["katsayi"].items())[:15]), "",
              "```", c["agac"].rstrip(), "```", ""]
    a = J["arama"]
    s += ["## Aday kural arama (önceden yazılı yordam, TP_ESIK 'kural')", "",
          "Aday ölçüler (iki pazarda q < 0,10, aynı yön; min |d|): " + ", ".join(f"{r['olcu']} ({_sy(r['min_abs_d'], 3)}, {'+' if r['isaret'] > 0 else '-'})"
                                                                            for r in a["aday_olcu"]),
          f"; şartı geçen kural sayısı {a['n_aday_kural']}.", "",
          "| Kod | kural | ABD duyarlılık_cc / yanlış / LR | AVR duyarlılık_cc / yanlış / LR | skor |", "|---|---|---|---|---|"]
    for kr in J["kurallar"]:
        cc = kr["cc"]
        s.append(f"| {kr['kod']} | {tp_kural_metin(kr)} | " + " | ".join(
            f"{_yz(cc[p]['duyarlilik_cc'])} / {_yz(cc[p]['yanlis_cc'])} / {_sy(cc[p]['LR'])}" for p in TP_ESIK["kesif_pazar"]) + f" | {_sy(kr['skor'])} |")
    s += ["", "## Aday kuralların keşifte tam ölçümü (2016-22; her uygun gün; DOĞRULAMA ile aynı fonksiyon)", "",
          "| Kod | Pazar | profil günü (tekil) | profil payı | DUYARLILIK (büyük mumların önceki 20 günde profil görme payı) | KESİNLİK P(20 günde büyük mum) | "
          "eş | taban | KAT [%95] | ilk 5 gün KAT | yukarı payı (eş) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for kod, d in J["kesif_olc"].items():
        for p, r in d.items():
            s.append(f"| {kod} | {p} | {r['profil_gunu']} | {_yz(r['profil_pay'])} | {_yz(r['duyarlilik'])} | {_yz(r['p_olay'])} | {_yz(r['p_es'])} | "
                     f"{_yz(r['taban'])} | {_sy(r['kat'])} [{_sy(r['alt'])}, {_sy(r['ust'])}] | {_sy(r['kat_5'])} | {_yz(r['yukari_pay'])} ({_yz(r['yukari_pay_es'])}) |")
    s += ["", "Okuma: DUYARLILIK = büyük mumların yüzde kaçında önceki 20 günde bu profil görüldü; KESİNLİK = profil günlerinin yüzde kaçı 20 gün içinde büyük "
          "mumla bitti; KAT = kesinlik / aynı gün, aynı oynaklık ve likidite kovasındaki profilsiz hisselerin oranı. Bu sayılar keşif verisinde (geriye bakarak "
          "seçilmiş kurallar); karar ADIM B'de görülmemiş 2023 ve 2024-26 verisinde.", "",
          "Hayatta kalma: evren bugün işlem gören hisseler (ABD + k34 nakdi biten); batanlar yok.", ""]
    return "\n".join(s)


# ================================================================ 10) ADIM B — ÖN KAYIT
_TP_DESEN = {"esik": r"TP_ESIK_SHA:\s*`([0-9a-f]{64})`", "kod": r"TP_KOD_SHA:\s*`([0-9a-f]{64})`",
             "kural": r"TP_KURAL_SHA:\s*`([0-9a-f]{64})`"}


def tp_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = TP_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def tp_onkayit_metni(K: Dict[str, Any], say: Dict[str, Any], vsha: Dict[str, str], kgit: Dict[str, str]) -> str:
    E = TP_ESIK; Dg = E["dogrulama"]
    s = ["# TERS PARMAK İZİ — ADIM B ÖN KAYDI (doğrulama; ileriye doğru)", "", TP_SURUM, "",
         f"- TP_ESIK_SHA: `{tp_sha(E)}`", f"- TP_KOD_SHA: `{_tp_sha_dosya(TP_YOL['kod'])}`", f"- TP_KURAL_SHA: `{_tp_sha_dosya(_tp_yol('kural'))}`",
         f"- ZAMAN (UTC): `{_tp_simdi()}`", f"- Keşif koşusu: {K.get('kesif_zaman_utc')}; kurallar dosyası commit {str(kgit.get('commit', '-'))[:10]} "
                                               f"({kgit.get('commit_zamani', '-')})", "",
         "Bu dosya doğrulamadan ÖNCE yazıldı. Panel 2023-01-01 'kes' ile kuruldu: 2023 ve sonrası büyük mum etiketleri / sonuçları HESAPLANMADI "
         "(yalnız profil günü sayımı). `dogrula` bu dosya git'e işlenmiş ve değişmemiş değilse ya da sha'lardan biri tutmazsa durur.", "",
         "## Cetvel mühür satırları (ORTAK_CETVEL; aynen)", "", OC.oc_kapi_satirlari(), "",
         "## Önceki işlerden farkı", "",
         "K23 (Ç95, bölge parmak izi) ve K44 (Ç123, INTEM parmak izi) TEK bir bölgenin (Cemal'in işaretlediği MANAS / BINBN / INTEM) ölçülerine en "
         "yakın bölgeleri arayıp sonraki getiriyi ölçtü: çıkış noktası seçilmiş bir örnekti. K46 / K48 (Ç125, Ç128) makineye '20 günde +%8 önce' "
         "dönüş etiketini öğretti: çıkış noktası GETİRİ etiketiydi, bölge değil. Ç58 SESSIZ_ML alış / satış sinyali öğretti. VDYT / VDYT2 (Ç162-Ç163) "
         "önce sıkışma bölgesini tanımlayıp sonra genişlemeyi ölçtü ve VDYT2-B (Ç164) büyük mumun bölgenin KENDİ küçük mumlarına göre tanımlanmasının "
         "üstünlüğü tanımsal yaptığını gösterdi. Bu iş TERSİNDEN başlar: çıkış noktası sinyal ya da bölge değil, MUTLAK ölçekli BÜYÜK MUMDUR (hissenin "
         "250 günlük ATR / σ'sına göre; bölgeden bağımsız); profil büyük mumdan geriye bakarak keşif verisinde (2016-22) çıkarılır, burada dondurulur ve "
         "yalnız görülmemiş 2023 / 2024-26 verisinde ileriye doğru ölçülür (keşif / doğrulama kesin ayrı).", "",
         "## Dondurulan aday kurallar (ters_kurallar.json; keşif kontrol yüzdeliklerinden eşikler)", "",
         "| Kod | kural | keşif ABD LR (duyarlılık_cc) | keşif AVR LR (duyarlılık_cc) |", "|---|---|---|---|"]
    for kr in K["kurallar"]:
        s.append(f"| {kr['kod']} | {tp_kural_metin(kr)} | {_sy(kr['cc']['ABD']['LR'])} ({_yz(kr['cc']['ABD']['duyarlilik_cc'])}) | "
                 f"{_sy(kr['cc']['AVR']['LR'])} ({_yz(kr['cc']['AVR']['duyarlilik_cc'])}) |")
    s += ["", "```json", json.dumps(K["kurallar"], ensure_ascii=False, indent=1, default=_tp_kayit), "```", "",
          "## Ölçüm ve karar (önceden yazılı; eşik sonuca göre oynanmaz)", "",
          f"- Büyük mum: {E['buyuk']['tanim']}", f"- Uygunluk: {E['uygun']['tanim']}", f"- Doğrulama: {Dg['tanim']}",
          "- Karar hücreleri: ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26 (dönem = profil günü s tarihi; 2024-26 = 2024-01-01 .. 2026-08-31, sonuç "
          "penceresi 31.08.2026'yı aşan gün ölçülmez). BIST 2023 / 2024-26 bilgi (V_BIST 2023-06'dan; 250 bar şartıyla ilk uygun gün ~2024-06).",
          "- İkinci ölçü: ilk 5 gün KAT (bilgi). Üçüncü: yön (büyük mumla biten profil günlerinde ilk büyük mumun yukarı payı vs aynı günlerin profilsiz "
          "büyük mumlu eşleri; bilgi). Dördüncü: ORTAK_CETVEL oc_olc ile profil günlerinin (cetvelin 60 gün tekilleştirmesiyle) 60 gün eşli getirisi + "
          "olasılık tablosu (giriş = s sonrası ilk açılış; yön bilinmediği için yalnız bilgi; cetvel etiketleri yazılır, karar değil).",
          f"- Kör grafik seti: {E['kor']['tanim']} Amaç: Cemal 'bunlar gerçek sıkışma mı' diye kendi gözüyle yargılar; ölçüm değil.",
          "- Hayatta kalma: evren bugün işlem gören hisseler (ABD + k34 nakdi biten); batanlar yok: büyük aşağı mum olasılığı aşağı yanlı olabilir.",
          "- İleri test (IK_ILERI önerisi): aynı komut, aynı kurallar (bu sha), aynı eşikle Eylül 2026 - Şubat 2027 verisi geldiğinde (kriz sonrası "
          "dönem ayrı hücre; en erken Mart 2027) yeniden ölçülür.", "",
          "## Veri sha256", ""] + [f"- V_{p}.pkl: `{v}`" for p, v in vsha.items()] + ["",
          "## PROFİL GÜNÜ SAYIMI (sonuç hesaplanmadan; uygun, 20 günde bir tekil / tekilsiz)", "",
          "| Kural | Pazar | Dönem | profil günü (tekil) | profil günü (tekilsiz) | uygun satır |", "|---|---|---|---|---|---|"]
    for kod, d in say.items():
        for p, dd in d.items():
            for dn, c in dd.items():
                s.append(f"| {kod} | {p} | {dn} | {c['tekil']} | {c['tekilsiz']} | {c['uygun']} |")
    s += ["", "Kural: hücrede n < 30 ise ÖLÇÜLEMEDİ; İZ DEĞİL yalnız dört karar hücresinde n >= 1.000 iken.", "", tp_kontrol_tablosu(), "",
          "## Test", "", "`python test_ters_parmak.py` (sentetik: büyük mum tanımı, önceki pencere ölçüleri yalnız s öncesi, geleceğe bakma kesme testi, "
          "kontrol eşleme, kural uygulaması, KAT bootstrap = OC.oc_kat, kapı, e-posta / anahtar taraması).", ""]
    return "\n".join(s)


def tp_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False, git: bool = True) -> str:
    yol = _tp_yol("onkayit", cikti)
    if os.path.exists(yol):
        try:
            OC._oc_git_islenmis(yol)
            raise TPHata(f"ön kayıt git'e işlenmiş ({yol}); üzerine yazılmaz")
        except OC.OCHata:
            if not uzerine:
                raise TPHata(f"ön kayıt var ({yol}); git'e işlenmemişse --uzerine-yaz")
    ky = _tp_yol("kural", cikti)
    if not os.path.exists(ky):
        raise TPHata("ters_kurallar.json yok: önce `python TERS_PARMAK.py kesif`")
    try:
        kgit = OC._oc_git_islenmis(ky) if git else {}
    except OC.OCHata as ex:
        raise TPHata(f"keşif kuralları git'e işlenmemiş: {ex}")
    K = json.load(open(ky, encoding="utf-8"))
    if K.get("esik_sha") != tp_sha(TP_ESIK):
        raise TPHata("keşif kuralları bu TP_ESIK ile üretilmemiş")
    say: Dict[str, Any] = {}; vsha = {}
    donem = [d for d in TP_ESIK["donem"]["karar"]]
    for p in TP_ESIK["karar_pazar"] + TP_ESIK["bilgi_pazar"]:
        vsha[p] = _tp_sha_dosya(os.path.join(veri or TP_YOL["veri"], f"V_{p}.pkl"))
        Vd = tp_veri(p, veri); T = tp_panel(Vd, kes=TP_ESIK["donem"]["kes"]); del Vd
        for kr in K["kurallar"]:
            pf = tp_kural_uygula(T, kr) & T.uygun.to_numpy()
            ix = np.flatnonzero(pf); tek = np.zeros(len(T), bool)
            if len(ix):
                tek[ix[tp_tekil(T.sid.to_numpy()[ix], T.i.to_numpy()[ix], TP_ESIK["dogrulama"]["tekil"])]] = True
            for ad, bas, son in donem:
                dm = ((T.tarih >= pd.Timestamp(bas)) & (T.tarih <= pd.Timestamp(son))).to_numpy()
                say.setdefault(kr["kod"], {}).setdefault(p, {})[ad] = {"tekil": int((tek & dm).sum()), "tekilsiz": int((pf & dm).sum()),
                                                                     "uygun": int((T.uygun.to_numpy() & dm).sum())}
        del T
        tplog.info("ön kayıt sayımı %s tamam", p)
    return _tp_yaz(yol, tp_onkayit_metni(K, say, vsha, kgit))


def tp_onkayit_dogrula(yol: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    yol = yol or _tp_yol("onkayit")
    if not os.path.exists(yol):
        raise TPHata(f"ön kayıt yok ({yol}): önce `python TERS_PARMAK.py onkayitB`")
    metin = open(yol, encoding="utf-8").read(); b = {}
    for ad, desen in _TP_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise TPHata(f"ön kayıt bozuk: '{ad}' satırı yok")
        b[ad] = m.group(1)
    ky = os.path.join(os.path.dirname(yol), TP_DOSYA["kural"])
    simdi = {"esik": tp_sha(TP_ESIK), "kod": _tp_sha_dosya(TP_YOL["kod"]), "kural": _tp_sha_dosya(ky) if os.path.exists(ky) else ""}
    for ad in simdi:
        if b[ad] != simdi[ad]:
            raise TPHata(f"{ad} sha tutmuyor (ön kayıt {b[ad][:12]}…, şimdi {simdi[ad][:12]}…): doğrulama DURDU (SAPMA)")
    out = {"yol": yol, **b}
    if git:
        try:
            out["git"] = OC._oc_git_islenmis(yol); out["git_kod"] = OC._oc_git_islenmis(TP_YOL["kod"]); out["git_kural"] = OC._oc_git_islenmis(ky)
        except OC.OCHata as ex:
            raise TPHata(str(ex))
    return out


# ================================================================ 11) GELECEĞE BAKMA DENETİMİ (koşu içinde)
def tp_gelecek_denetimi(Vd: Dict[str, Any], T: pd.DataFrame, kurallar: List[Dict[str, Any]], n: int, tohum: int) -> int:
    """Rastgele n profil gününde hissenin serisi s'de kesilir: 30 ölçü, ATR / σ ve kural sonuçları aynı olmalı."""
    m = np.zeros(len(T), bool)
    for kr in kurallar:
        m |= tp_kural_uygula(T, kr) & T.uygun.to_numpy()
    ix = np.flatnonzero(m)
    if not len(ix):
        return 0
    rng = np.random.default_rng(tohum); sec = rng.choice(ix, min(n, len(ix)), replace=False)
    for r in sec:
        s = T.attrs["sembol"][int(T.sid.iat[r])]; t = T.tarih.iat[r]
        d = Vd["V"][s]; dk = d[d.index <= t]
        Xk = tp_olculer(dk).iloc[-1]; Bk = tp_buyuk(dk).iloc[-1]
        a = T.loc[r, TP_OLCULER].to_numpy(float); b = Xk[TP_OLCULER].to_numpy(np.float32).astype(float)
        if not (np.allclose(a, b, rtol=1e-5, atol=1e-6, equal_nan=True) and abs(Bk.A - T.A.iat[r]) < 1e-9 * max(1, abs(Bk.A))
                and abs(Bk.S - T.S.iat[r]) < 1e-12 + 1e-9 * abs(Bk.S)):
            raise TPHata(f"geleceğe bakma denetimi TUTMADI: {s} {t.date()}")
        Tk = pd.DataFrame([Xk[TP_OLCULER].astype(np.float32)])
        for kr in kurallar:
            if bool(tp_kural_uygula(Tk, kr)[0]) != bool(tp_kural_uygula(T.loc[[r]], kr)[0]):
                raise TPHata(f"geleceğe bakma denetimi kural {kr['kod']} TUTMADI: {s} {t.date()}")
    return len(sec)


# ================================================================ 12) KÖR GRAFİK SETİ
def tp_kor_aday(T: pd.DataFrame, kural: Dict[str, Any], tek: np.ndarray, E: Dict[str, Any] = TP_ESIK) -> pd.DataFrame:
    """Doğrulama P1 profil günleri (tekil; s >= kes; sonucu ölçülebilir; önce >= 120 bar) + her biri için aynı gün / katmandan rastgele profilsiz kontrol."""
    Kr = E["kor"]; kur = tp_kural_uygula(T, kural)
    m = tek & (T.tarih >= pd.Timestamp(E["donem"]["kes"])).to_numpy() & np.isfinite(T.f20.to_numpy()) & (T.i.to_numpy() >= Kr["once"])
    km = T.uygun.to_numpy() & ~kur & np.isfinite(T.f20.to_numpy()) & (T.i.to_numpy() >= Kr["once"]) & \
        (T.tarih >= pd.Timestamp(E["donem"]["kes"])).to_numpy()
    K_ = T.loc[km, ["tarih", "kat_gun"]]; hv = K_.groupby(["tarih", "kat_gun"]).indices; kidx = K_.index.to_numpy()
    rng = np.random.default_rng(Kr["tohum"]); sat = []
    for r in np.flatnonzero(m):
        h = hv.get((T.tarih.iat[r], int(T.kat_gun.iat[r])))
        if h is None or not len(h):
            continue
        c = int(kidx[h[rng.integers(len(h))]])
        sat.append({"pazar": T.attrs["pazar"], "p_sembol": T.attrs["sembol"][int(T.sid.iat[r])], "tarih": T.tarih.iat[r],
                    "p_f20": float(T.f20.iat[r]), "k_sembol": T.attrs["sembol"][int(T.sid.iat[c])], "k_f20": float(T.f20.iat[c])})
    return pd.DataFrame(sat)


def tp_kor_pencere(d: pd.DataFrame, t: pd.Timestamp, E: Dict[str, Any] = TP_ESIK) -> pd.DataFrame:
    Kr = E["kor"]; k = d.index.get_loc(t)
    W = d.iloc[k - Kr["once"]: k + Kr["sonra"] + 1][["Open", "High", "Low", "Close", "Volume"]].astype(float).copy()
    W.columns = ["o", "h", "l", "c", "v"]
    if len(W) != Kr["once"] + Kr["sonra"] + 1:
        raise TPHata(f"kör pencere eksik ({len(W)} bar)")
    kk = float(d.Close.iat[k]); W[["o", "h", "l", "c"]] = W[["o", "h", "l", "c"]] / kk * 100.0
    return W


def tp_kor_ciz(W: pd.DataFrame, yol: str, E: Dict[str, Any] = TP_ESIK) -> Dict[str, Any]:
    """KOR_TEST v1.1 çizimi (kor_ciz_fig11) + x ekseni s'ye göre (−120 .. 0 .. 20) + s'nin sağına kesikli dikey çizgi; metin denetimi KOR_TEST ile."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import KOR_TEST as KT
    Kr = E["kor"]; fig = KT.kor_ciz_fig11(W, KT.KOR_ESIK)
    try:
        ax, axv = fig.axes[0], fig.axes[1]
        n = len(W); s_x = -(n - 1) + Kr["once"]
        xt = list(range(-Kr["once"], Kr["sonra"] + 1, 20))
        axv.set_xticks([s_x + v for v in xt], labels=[str(v) for v in xt])
        for a in (ax, axv):
            a.axvline(s_x + 0.5, color="#555555", linestyle="--", linewidth=1.0)
        yab = KT.kor_metin_yabanci(KT.kor_metinler(fig))
        if yab:
            raise TPHata(f"grafikte sayı dışı metin: {yab[:5]}")
        fig.savefig(yol, dpi=fig.dpi, metadata={"Software": None})
    finally:
        plt.close(fig)
    return {"dosya": os.path.basename(yol), "sha256": _tp_sha_dosya(yol)}


def tp_kor_set(aday: pd.DataFrame, veri: Optional[str] = None, cikti: Optional[str] = None, E: Dict[str, Any] = TP_ESIK) -> Dict[str, Any]:
    Kr = E["kor"]
    if len(aday) < Kr["n"]:
        return {"atlandi": f"aday {len(aday)} < {Kr['n']}"}
    rng = np.random.default_rng(Kr["tohum"])
    sec = aday.iloc[np.sort(rng.choice(len(aday), Kr["n"], replace=False))].reset_index(drop=True)
    ogeler = [{"grup": "P1", "pazar": r.pazar, "sembol": r.p_sembol, "tarih": str(r.tarih)[:10], "f20": r.p_f20} for r in sec.itertuples()] + \
             [{"grup": "KONTROL", "pazar": r.pazar, "sembol": r.k_sembol, "tarih": str(r.tarih)[:10], "f20": r.k_f20} for r in sec.itertuples()]
    sira = rng.permutation(len(ogeler)); ogeler = [ogeler[k] for k in sira]
    png = os.path.join(TP_YOL["satir"], "kor_png"); os.makedirs(png, exist_ok=True)
    VV: Dict[str, Any] = {}
    for p in sorted({o["pazar"] for o in ogeler}):
        VV[p] = tp_veri(p, veri)["V"]
    from PIL import Image
    imgs = []
    for k, o in enumerate(ogeler, 1):
        W = tp_kor_pencere(VV[o["pazar"]][o["sembol"]], pd.Timestamp(o["tarih"]))
        yol = os.path.join(png, f"{k:02d}.png"); o.update({"no": k, **tp_kor_ciz(W, yol)})
        im = Image.open(yol).convert("RGB"); imgs.append(im)
    pdf = _tp_yol("pdf", cikti)
    os.makedirs(os.path.dirname(pdf), exist_ok=True)
    imgs[0].save(pdf, save_all=True, append_images=imgs[1:], resolution=100.0, quality=85)
    mb = os.path.getsize(pdf) / 1e6
    if mb > Kr["max_mb"]:
        raise TPHata(f"PDF {mb:.1f} MB > {Kr['max_mb']} MB")
    anahtar = {"surum": TP_SURUM, "tanim": Kr["tanim"], "pdf_sha256": _tp_sha_dosya(pdf), "pdf_mb": round(mb, 2),
               "not": "f20 = profil gününden sonraki 20 barda büyük mum oldu mu (1/0); Cemal işaretlemeden önce açılmaz",
               "ogeler": [{k: o[k] for k in ("no", "grup", "pazar", "sembol", "tarih", "f20", "sha256")} for o in ogeler]}
    _tp_json(_tp_yol("anahtar", cikti), _tp_temiz(anahtar))
    return {"pdf": os.path.basename(pdf), "mb": round(mb, 2), "n": len(ogeler), "p1_f20": float(np.mean([o["f20"] for o in ogeler if o["grup"] == "P1"])),
            "kontrol_f20": float(np.mean([o["f20"] for o in ogeler if o["grup"] == "KONTROL"]))}


# ================================================================ 13) ADIM B — DOĞRULAMA
def _tp_birlestir(parca: List[Dict[str, Any]]) -> Dict[str, Any]:
    T = pd.concat([p["hucre"] for p in parca if len(p["hucre"])], ignore_index=True) if parca else pd.DataFrame()
    return {"hucre": T, "olay": pd.concat([p["olay"] for p in parca], ignore_index=True) if parca else pd.DataFrame(),
            "olasilik": pd.concat([p["olasilik"] for p in parca], ignore_index=True) if parca else pd.DataFrame(),
            "sayim": {k: v for p in parca for k, v in p["sayim"].items()},
            "etiket": OC.oc_etiket(T) if len(T) else {"genel": "VERİ YOK", "olasilik": "ÖLÇÜLEMEDİ", "karar_hucre": {}},
            "cetvel_sha": parca[0]["cetvel_sha"] if parca else OC.oc_esik_sha(), "kod_sha": parca[0]["kod_sha"] if parca else "", "surum": OC.OC_SURUM}


def tp_dogrula(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    yol = _tp_yol("onkayit", cikti)
    kapi = OC.oc_kapi(yol, git=git, kontrol=kontrol)
    ok = tp_onkayit_dogrula(yol, git=git)
    kz = _tp_simdi()
    K = json.load(open(_tp_yol("kural", cikti), encoding="utf-8")); kur = K["kurallar"]
    satir = TP_YOL["satir"]; os.makedirs(satir, exist_ok=True)
    donem = [["2016-22"] + TP_ESIK["donem"]["kesif"]] + TP_ESIK["donem"]["karar"]
    H: Dict[str, Dict[str, Any]] = {kr["kod"]: {} for kr in kur}; oc_parca: Dict[str, List[Dict[str, Any]]] = {kr["kod"]: [] for kr in kur}
    den, kor_aday, sat_l = {}, [], []
    for p in TP_ESIK["karar_pazar"] + TP_ESIK["bilgi_pazar"]:
        Vd = tp_veri(p, veri); T = tp_panel(Vd, kes=None)
        den[p] = tp_gelecek_denetimi(Vd, T, kur, TP_ESIK["gelecek_denetimi_n"], TP_ESIK["tohum"])
        tplog.info("%s: panel %d satır; geleceğe bakma denetimi %d gün TUTTU", p, len(T), den[p])
        bmask = tp_buyuk_satir(T)
        B_ = T.loc[bmask, ["sid", "tarih", "nb1"]].copy(); B_["sembol"] = [T.attrs["sembol"][s] for s in B_.sid]; B_["pazar"] = p
        B_.to_csv(os.path.join(satir, f"buyuk_{p}.csv.gz"), index=False)
        for kr in kur:
            R = tp_kural_olc(T, kr, donem, satir_don=True)
            for dn, r in R["hucre"].items():
                H[kr["kod"]][f"{p} {dn}"] = r
            S_ = R["satir"]; S_["kural"] = kr["kod"]; sat_l.append(S_)
            olay = S_[["sembol", "tarih"]].copy(); olay["pazar"] = p
            oc_parca[kr["kod"]].append(OC.oc_olc(olay.reset_index(drop=True), {p: Vd}))
            if kr["kod"] == "P1" and p in TP_ESIK["karar_pazar"]:
                kor_aday.append(tp_kor_aday(T, kr, R["profil_tekil_maske"]))
            tplog.info("%s %s: %s (%.0f sn)", p, kr["kod"], {k: (v.get("n"), v.get("kat")) for k, v in R["hucre"].items()}, time.time() - t0)
        del T, Vd
        OC._OC_PANEL_ONBELLEK.clear()
    Sat = pd.concat(sat_l, ignore_index=True); Sat.to_csv(os.path.join(satir, "profil_gunleri.csv.gz"), index=False)
    # karar: p_kural = dört karar hücresinin en büyük p'si; 3 kural BH
    kh = [f"{p} {d[0]}" for p in TP_ESIK["karar_pazar"] for d in TP_ESIK["donem"]["karar"]]
    pk = np.array([max([(H[kr["kod"]].get(k, {}).get("p") if H[kr["kod"]].get(k, {}).get("p") is not None else 1.0) for k in kh]) for kr in kur])
    qk = tp_bh(pk)
    karar, oc_s = {}, {}
    for kr, p_, q_ in zip(kur, pk, qk):
        karar[kr["kod"]] = {"p_kural": float(p_), "q_bh": float(q_), "etiket": tp_kural_etiket(H[kr["kod"]], q_)}
        S = _tp_birlestir(oc_parca[kr["kod"]])
        S["olay"].to_csv(os.path.join(satir, f"oc_olay_{kr['kod']}.csv.gz"), index=False)
        oc_s[kr["kod"]] = {"hucre": json.loads(S["hucre"].to_json(orient="records", force_ascii=False)) if len(S["hucre"]) else [],
                           "olasilik": json.loads(S["olasilik"].to_json(orient="records", force_ascii=False)) if len(S["olasilik"]) else [],
                           "etiket": S["etiket"], "rapor": OC.oc_rapor(S, f"{kr['kod']} profil günleri (60 gün eşli; BİLGİ)")}
    KA = pd.concat(kor_aday, ignore_index=True) if kor_aday else pd.DataFrame()
    try:
        kor = tp_kor_set(KA, veri, cikti)
    except Exception as ex:   # kör set ölçüm değildir; hatası sonucu durdurmaz, raporda yazılır
        tplog.error("kör set üretilemedi: %s", ex); kor = {"hata": str(ex)}
    J = {"surum": TP_SURUM, "onkayit": ok, "oc_kapi": {k: v for k, v in kapi.items() if k != "kontrol"}, "dogrula_zaman_utc": kz,
         "gelecek_denetimi": den, "kurallar": kur, "hucre": H, "karar": karar, "oc": oc_s, "kor": kor, "sure_sn": round(time.time() - t0, 1)}
    _tp_json(_tp_yol("sonuc", cikti), _tp_temiz(J))
    return {"sonuc": J, "rapor": tp_rapor(cikti)}


# ================================================================ 14) RAPOR
def tp_rapor(cikti: Optional[str] = None) -> str:
    J = json.load(open(_tp_yol("sonuc", cikti), encoding="utf-8"))
    kh = [f"{p} {d[0]}" for p in TP_ESIK["karar_pazar"] for d in TP_ESIK["donem"]["karar"]]
    bil = [f"{p} {d[0]}" for p in TP_ESIK["bilgi_pazar"] for d in TP_ESIK["donem"]["karar"]] + [f"{p} 2016-22" for p in TP_ESIK["karar_pazar"]]
    g = J["onkayit"].get("git", {})
    s = ["# TERS PARMAK İZİ — ADIM B DOĞRULAMA RAPORU", "",
         f"{TP_SURUM}. Ön kayıt B commit {str(g.get('commit', '-'))[:10]} ({g.get('commit_zamani', '-')}); doğrulama koşusu {J['dogrula_zaman_utc']}; "
         f"süre {J.get('sure_sn')} sn. Geleceğe bakma denetimi: " + ", ".join(f"{p} {n} gün TUTTU" for p, n in J["gelecek_denetimi"].items()) + ".", "",
         "## DÜZ DİL ÖZET", ""]
    for kr in J["kurallar"]:
        k = J["karar"][kr["kod"]]; H = J["hucre"][kr["kod"]]
        par = []
        for c in kh:
            r = H.get(c, {})
            par.append(f"{c}: KAT {_sy(r.get('kat'))} [{_sy(r.get('alt'))}, {_sy(r.get('ust'))}], duyarlılık {_yz(r.get('duyarlilik'))}, n {r.get('n')}"
                       f"{' GEÇER' if r.get('gecer') else ''}")
        s.append(f"- **{kr['kod']}** ({tp_kural_metin(kr)}): **{k['etiket']}** (p_kural {_tp_q(k['p_kural'])}, BH q {_tp_q(k['q_bh'])}). " + "; ".join(par) + ".")
    s += ["", "Okuma: KAT = profil günlerinde 20 gün içinde büyük mum olasılığı / aynı gün, aynı σ250 ondalığı ve likidite üçlüsündeki profilsiz hisselerin "
          "olasılığı (1 = fark yok). Duyarlılık = o dönemdeki büyük mumların yüzde kaçının önceki 20 gününde bu profil vardı. Hayatta kalma: evren bugün "
          "işlem gören hisseler; batanlar yok.", "",
          "## Doğrulama KAT tablosu (karar hücreleri + bilgi)", "",
          "| Kural | Hücre | karar | profil günü n | P(20 gün büyük mum) profil / eş / taban | KAT [%95] | p | ilk 5 gün KAT [%95] | duyarlılık (s=t-1) | "
          "yukarı payı profil / eş | GEÇER |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for kr in J["kurallar"]:
        H = J["hucre"][kr["kod"]]
        for c in kh + bil:
            r = H.get(c)
            if r is None:
                continue
            s.append(f"| {kr['kod']} | {c} | {'K' if c in kh else 'b'} | {r.get('n')} | {_yz(r.get('p_olay'))} / {_yz(r.get('p_es'))} / {_yz(r.get('taban'))} | "
                     f"{_sy(r.get('kat'))} [{_sy(r.get('alt'))}, {_sy(r.get('ust'))}] | {_tp_q(r.get('p'))} | {_sy(r.get('kat_5'))} [{_sy(r.get('alt_5'))}, "
                     f"{_sy(r.get('ust_5'))}] | {_yz(r.get('duyarlilik'))} ({_yz(r.get('duyarlilik_t1'))}) | {_yz(r.get('yukari_pay'))} / "
                     f"{_yz(r.get('yukari_pay_es'))} | {'EVET' if r.get('gecer') else 'hayır'} |")
    s += ["", "## Kör grafik seti (Cemal'in gözü için)", ""]
    kor = J.get("kor", {})
    if "pdf" in kor:
        s.append(f"{kor['pdf']} ({kor['mb']} MB, {kor['n']} grafik: 20 P1 + 20 aynı gün / katman kontrolü, karışık sıra; anahtar "
                 f"{TP_DOSYA['anahtar']}, işaretlemeden önce açılmaz). Grafik: 120 bar önce + profil günü + 20 bar sonra, kesikli çizgi profil gününün sağı.")
    else:
        s.append(f"Üretilemedi: {kor}")
    s += ["", "## 60 gün eşli getiri ve olasılık tablosu (ORTAK CETVEL; yön bilinmediği için BİLGİ)", ""]
    for kr in J["kurallar"]:
        s += [J["oc"][kr["kod"]]["rapor"], ""]
    metin = "\n".join(s)
    _tp_yaz(_tp_yol("rapor", cikti), metin)
    return metin


# ================================================================ 15) ÇAKIŞMA KAPISI
def _cakisma_kontrol_tp(_once=_CK_ONCE_TP, _dosya="TERS_PARMAK.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_TP", "_CK_KAYIT", "_cakisma_kontrol_tp", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "warnings", "itertools", "_dt", "OC",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple", "_yz", "_sy")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_tp()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=TP_SURUM)
    ap.add_argument("komut", choices=["kesif", "onkayitB", "dogrula", "rapor"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "kesif":
            J_ = tp_kesif(a.cikti, a.veri)
            print(open(_tp_yol("kesif_rapor", a.cikti), encoding="utf-8").read()[:6000])
        elif a.komut == "onkayitB":
            print(tp_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "dogrula":
            R_ = tp_dogrula(a.cikti, a.veri)
            print(R_["rapor"].split("## 60 gün")[0])
        else:
            print(tp_rapor(a.cikti))
    except (TPHata, OC.OCHata) as ex:
        tplog.error("%s", ex); sys.exit(1)
