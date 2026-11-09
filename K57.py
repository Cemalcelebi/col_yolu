"""K57 — YEOTK PROFİLİ ('SIKI DOSYA') ÖN KAYITLI GEÇMİŞ TESTİ, tek dosya (Cemal, 9 Kasım 2026, 'tek ve son talimat'; IZ_KARNE Ç148).

Soru: YEOTK'nın 5 Kasım 2026 bilançosundaki profil (satış büyümesi + çeyrek ivmesi + kârda sıçrama, sağlam bilanço, seyrelme yok,
fon lekesi yok, fiyat tepeden düşmüş, bilanço gününe güçlü tepki) geçmişte BIST'te ve ABD'de eşlerini sistematik olarak geçti mi?

Komut:  python K57.py onkayit   ön kaydı yazar (ölçümden ÖNCE; eşiklerin sha256'sı içinde; varsa üzerine yazmaz)
        python K57.py indir     SEC XBRL frames (ABD temel verisi) indirir; SEC reddederse durur ve söyler
        python K57.py kos       olaylar + süzgeçler + FI_OLCUT ölçümü + önceden yazılı 3 devam + rapor
        python K57.py rapor     K57_RAPOR.md'yi çıktılardan yeniden yazar
Colab:  exec(open('K57.py').read()); k57_kos()
Ölçüm kütüphanesi FON_IZI.py modül olarak içe alınır (fi_k28_olaylar, fi_olcut_panel / olay / hucre, _fi_olcut_karar_ortak,
fi_k31_finansal, fi_k25_pay_tablo); kopyalanmaz. Çıktılar arastirma_cikti/k57_yeotk_profili/.
Veri: /tmp/veri (islenmis-veri 'veri' paketi: V_BIST, V_ABD, G, oran, dol), /tmp/secfs (islenmis-veri secfs), islenmis-veri pead/
listeleri (git show ile açılır), SEC frames /tmp/secframes. Fiyat yeniden indirilmez. Kişisel e-posta koda / çıktıya yazılmaz.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K57 = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import ssl  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import urllib.error  # noqa: E402
import urllib.request  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K57 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K57 not in sys.path:
    sys.path.insert(0, KOK_K57)

import FON_IZI as FI  # noqa: E402

k57log = logging.getLogger("col.k57")
if not k57log.handlers:
    _k57_h = logging.StreamHandler(sys.stderr)
    _k57_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k57: %(message)s", "%H:%M:%S"))
    k57log.addHandler(_k57_h)
    k57log.setLevel(logging.INFO)
    k57log.propagate = False

K57_SURUM = "K57 v1.0 (2026-11-09): YEOTK profili ön kayıtlı geçmiş testi (BIST bilgi, ABD karar, Avrupa verisi yok)"
K57_SEC_UA = "col-yolu-arastirma/1.0 (+https://github.com/cemalcelebi/col_yolu)"
K57_DAL = "origin/islenmis-veri"
K57_YOL = {
    "cikti": os.path.join(KOK_K57, "arastirma_cikti", "k57_yeotk_profili"),
    "veri": os.environ.get("K57_VERI", "/tmp/veri"),
    "secfs": os.environ.get("K57_SECFS", "/tmp/secfs"),
    "frames": os.environ.get("K57_FRAMES", "/tmp/secframes"),
    "frames_ek": [p for p in os.environ.get("K57_FRAMES_EK", "").split(os.pathsep) if p],
    "onbellek": os.environ.get("K57_ONBELLEK", "/tmp/k57"),
    "fon_pay": os.environ.get("K57_FONPAY", ""),
    "ca": "/root/.ccr/ca-bundle.crt",
}

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256'sı K57_ON_KAYIT.md'de; sonradan değişmez)
K57_ESIK: Dict[str, Any] = {
    "F1_abd_yoy": 0.25,            # ABD: çeyrek satışı geçen yılın aynı çeyreğine göre >= +%25
    "F1_bist_dilim": 0.40,         # BIST: satış yıllık büyümesi, o ana kadar açıklayanların (son 92 gün) üst %40'ı (enflasyondan bağımsız)
    "F1_pencere_gun": 92, "F1_min_n": 30,
    "F2_kat": 1.4,                 # bu çeyrek satış >= 1,4 x önceki iki çeyreğin ortalaması VE net kâr > 0 VE > önceki çeyrek
    "F3_bist_borc_oz": 2.0,        # BIST: özkaynak > 0 ve net borç / özkaynak < 2
    "F3_abd_borc_kat": 3.0,        # ABD: özkaynak > 0 ve toplam yükümlülük <= 3 x özkaynak
    "F4_pay_yil": 0.10,            # ABD: pay sayısı 4 çeyrekte <= +%10 (bölünme oranı ±%3 tamsayıysa bölünme, seyrelme değil)
    "F4_bolunme_tol": 0.03,
    "F5_fon_pay": 0.02,            # BIST: K25 raporlu fon payı < %2 (yayın anı tepki gününden önce; rapor yoksa 0)
    "F6_dd_alt": -0.70, "F6_dd_ust": -0.30, "F6_tepe_gun": 250, "F6_tepe_min": 120, "F6_mom_gun": 60,
    "F7_dilim": 0.20, "F7_ham": 0.05, "F7_pencere_gun": 92, "F7_min_n": 30,
    "ceyrek_bilgi_max_gun": 120, "bilgi_yedek_gun": 90, "abd_temel_kapsam_min": 0.50,
    "abd_bas": "2021-01-01", "nasdaq_bas": "2022-12-01",
    "sec_ceyrek": ["2020Q1", "2026Q2"], "sec_yil": [2020, 2025],
    "varyant": {"V0": ["F7"], "V1": ["F7", "F1", "F2", "F3"], "V2": ["F7", "F1", "F2", "F3", "F6"],
                "V3": ["F7", "F1", "F2", "F3", "F6", "F4", "F5"], "V4": ["F1", "F2", "F3", "F6"]},
    "ana_varyant": "V3",
    "deney": {"D1": {"ad": "F2 1,2 kat", "F2_kat": 1.2, "varyant": ["V1", "V2", "V3", "V4"]},
              "D2": {"ad": "120 gün ufuk", "ufuk": 120, "varyant": ["V0", "V1", "V2", "V3", "V4"]},
              "D3": {"ad": "art arda iki ivmeli çeyrek", "varyant": ["V1", "V2", "V3", "V4"]}},
    "hucre": {"BIST": [["2022-23", "2022-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-12-31"]],
              "ABD": [["2021-22", "2021-01-01", "2022-12-31"], ["2023", "2023-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-12-31"]]},
    "karar_hucre": [["ABD", "2023"], ["ABD", "2024-26"]],
    "bist_karar_eslem": {"2022-23": "2023", "2024-26": "2024-26"},
}
K57_ATLA = {"BIST": ["F4"], "ABD": ["F5"]}
K57_TEMEL = ("F1", "F2", "F3")
K57_ABD_GELIR = ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet")
K57_ABD_ANLIK = ("StockholdersEquity", "Liabilities", "LiabilitiesAndStockholdersEquity")
K57_DOSYA = {"onkayit": "K57_ON_KAYIT.md", "bist": "olaylar_bist.csv", "abd": "olaylar_abd.csv", "hucre": "hucre.csv",
             "rapor": "K57_RAPOR.md", "meta": "k57_kos_meta.json"}
_K57_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


class K57Hata(RuntimeError):
    """K57'ye özgü durdurucu hata (ön kayıt yok / değişmiş, veri bozuk)."""


class K57SecRet(RuntimeError):
    """SEC isteği reddetti (403): indirme durur, ABD temel süzgeçleri 'ABD TEMEL VERİSİ YOK' olur."""


def _k57_olcut() -> Dict[str, Any]:
    return dict(FI.FI_OLCUT)


def k57_esik_sha() -> str:
    """Ön kayıt mührü: K57_ESIK + FI_OLCUT (ölçüt) birlikte; biri değişirse koşu durur."""
    s = json.dumps({"K57_ESIK": K57_ESIK, "FI_OLCUT": _k57_olcut(), "K57_ATLA": K57_ATLA}, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _k57_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K57_YOL["cikti"], K57_DOSYA[ad])


def _yz(x: Any, nokta: int = 1) -> str:
    """Türkçe yüzde: +%5,0."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    if not np.isfinite(v):
        return "—"
    return ("+" if v >= 0 else "-") + "%" + f"{abs(v) * 100:.{nokta}f}".replace(".", ",")


def _sy(x: Any, nokta: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return f"{v:.{nokta}f}".replace(".", ",") if np.isfinite(v) else "—"


# ---------------------------------------------------------------- 0) ÖN KAYIT
def k57_onkayit_metin(zaman: str) -> str:
    E = K57_ESIK; O = _k57_olcut()
    return f"""# K57 ÖN KAYIT — YEOTK profili ('sıkı dosya') geçmiş testi

Yazım zamanı: {zaman} (ölçümden ÖNCE; sonuç görülmedi). Sürüm: {K57_SURUM}
ESIK_SHA256: {k57_esik_sha()}
(K57_ESIK + FI_OLCUT + pazar atlamalarının sha256'sı. `python K57.py kos` bu mühürle başlar; eşik değişirse koşu durur.)

## 1. Soru ve kaynak
Cemal (9 Kas 2026, tek ve son talimat): YEOTK gibi 'sıkı dosya' hisseleri BIST'te ve özellikle ABD'de eşlerini geçiyor mu?
YEOTK 9A26 (5 Kas 2026): satış +%31, FAVÖK +%103, 3Ç satışı ≈ 9,2 milyar TL (ilk yarı toplamından fazla), 3Ç net kâr ≈ 864 milyon TL
(ilk yarı 670 milyon), 24 ayda nakit seyrelme yok, raporlu fon payı %0,4, fiyat Mayıs 2026 tepesinin %54 altında, 90 günde -%38;
ertesi gün tavan açılış. Bu olay örneklemde değildir (fiyat 31.08.2026'da kesik, temel_duz 2026/6'ya kadar).

## 2. Olay, giriş, getiri (K28 ile aynı kurgu; FON_IZI fi_k28_olaylar modül olarak çağrılır)
- Açıklama günü D. BIST: KAP 'Finansal Rapor' listesi (islenmis-veri pead/liste_bist), hisse-yıl-dönemin ilk raporu, 18:00 sonrası
  yayın ertesi gün (K28). temel_duz 'aciklama' sütunu gerçek gün değil, yasal süre vekili (çeyrek sonu + 50 / 70 gün; temel.py) olduğu
  için olay günü olarak kullanılmaz; KAP kaydı olmayan dönemde yalnız bilgi tarihi yedeği olur.
  ABD: 2022-12-01'den itibaren Nasdaq bilanço takvimi (K28 listesi); 2021-01-01 .. 2022-11-30 arası SEC finansal tablo özütlerindeki
  10-Q / 10-K başvuru günü (filed; Nasdaq listesi o dönemi kapsamıyor).
- TEPKİ (K28): D'den önceki son işlem günü kapanışından D'den sonraki ilk işlem günü kapanışına getiri ('ham') ve aynı pencerede
  piyasa medyanı düşülmüş tepki ('ear'). BIST akşam, ABD açılış öncesi / kapanış sonrası açıklamalarını kapsar (YEOTK: 5 Kas akşam,
  6 Kas tavan). Tepki günü = bu pencerenin son günü.
- GİRİŞ = tepki gününden sonraki ilk işlem günü AÇILIŞI. r60 = 60. gün kapanışı / giriş - 1 (FI_OLCUT, fiyatlar {O['kriz']}'de kesik).
- Ölçüt FI_OLCUT (değiştirilmeden): eşli fark = r60 - aynı gün aynı 60 gün momentum beşliği x 20 gün likidite üçlüsündeki öteki
  hisselerin ortalama r60'ı; ay kümeli bootstrap ({O['bootstrap']}) %95 aralık; hücre içi sıra; 10 yuvalı slot portföyü vs 200 eşli
  rastgele portföy. HÜCRE TUTAR: n >= {O['n_esik']}, ortalama eşli fark > 0 ve aralık alt ucu > 0, sıra > 0,50, portföy > rastgele %90.

## 3. Süzgeçler (yalnız tepki gününde bilinen bilgi; her temel değerin bilgi tarihi <= D)
- F1 büyüme: ABD çeyrek satışı yıllık >= +%{E['F1_abd_yoy'] * 100:.0f}. BIST: satış yıllık büyümesi, D'ye kadar son {E['F1_pencere_gun']} günde
  açıklayanların üst %{E['F1_bist_dilim'] * 100:.0f}'ı (eşik o ana kadar bilinenlerden; en az {E['F1_min_n']} değer; enflasyondan bağımsız).
- F2 ivme: bu çeyrek satış >= {E['F2_kat']} x önceki iki çeyrek ortalaması VE bu çeyrek net kâr > 0 VE > önceki çeyrek net kâr.
- F3 bilanço: özkaynak > 0 ve BIST net borç / özkaynak < {E['F3_bist_borc_oz']}; ABD yükümlülük <= {E['F3_abd_borc_kat']} x özkaynak
  (Liabilities yoksa LiabilitiesAndStockholdersEquity - StockholdersEquity).
- F4 seyrelme yok (ABD): pay sayısı 4 çeyrekte <= +%{E['F4_pay_yil'] * 100:.0f} (FON_IZI fi_k31_finansal, SEC özütleri: bilanço pay sayısı,
  yoksa ağırlıklı ortalama; başvuru günü <= D olan en son bildirim). Oran bir tamsayıya ±%{E['F4_bolunme_tol'] * 100:.0f} yakınsa bölünme
  sayılır (geçer). Veri yoksa geçmez. BIST'te ATLANIR (bedelsiz sermaye artırımları seyrelme değil; ayrım verisi yok).
- F5 temiz sahiplik (BIST): K25 raporlu fon payı < %{E['F5_fon_pay'] * 100:.0f} (fi_k25_pay_tablo; yayın anı D'den önce olan en son ay; rapor
  yoksa pay 0 = alt sınır). ABD'de ATLANIR.
- F6 sevilmeyen fiyat: D öncesi son kapanış {E['F6_tepe_gun']} günlük en yüksekten %{-E['F6_dd_ust'] * 100:.0f}-%{-E['F6_dd_alt'] * 100:.0f} aşağıda
  VE {E['F6_mom_gun']} günlük getirisi o gün pazarın medyanının altında.
- F7 güçlü tepki: 'ear' D'ye kadar son {E['F7_pencere_gun']} günde tepki günü biten olayların üst %{E['F7_dilim'] * 100:.0f}'ında (yalnız o ana
  kadar bilinenler; K28'in çeyrek içi diliminde görülen etiket sızıntısı böyle önlenir) VE ham tepki >= +%{E['F7_ham'] * 100:.0f}.
  K28'in çeyrek içi 'ust' etiketi olaylar dosyasında bilgi olarak kalır.

## 4. Varyantlar ve hücreler
- V0 = F7 (K28 tabanı); V1 = F7+F1+F2+F3; V2 = V1+F6; V3 = V2+F4+F5 (TAM YEOTK PROFİLİ, ana sonuç); V4 = F1+F2+F3+F6 (tepkisiz).
- Hücreler (giriş gününe göre): BIST 2022-23 ve BIST 2024-26 = BİLGİ; ABD 2021-22 = BİLGİ; ABD 2023 ve ABD 2024-26 = KARAR.
- Karar (FON_IZI _fi_olcut_karar_ortak, karar pazarları ABD + AVR): iki ABD karar hücresi tutarsa en fazla 'ABD-ADAY (AVRUPA VERİSİ YOK)'
  (Avrupa'da bilanço olay verisi bedava yok); BIST de tutuyorsa '+ BIST' bilgisi. Aksi 'İZ DEĞİL'.

## 5. Veri durumu ve önceden yazılı yedek kural
- ABD temel verisi (F1-F3) SEC XBRL frames API'sinden gelir (Revenues > RevenueFromContractWithCustomerExcludingAssessedTax >
  SalesRevenueNet: gereken çeyreklerin hepsini taşıyan ilk etiket, etiket karıştırılmaz; NetIncomeLoss; StockholdersEquity,
  Liabilities anlık; 4. çeyrek = yıllık - üç çeyrek, dönemler hizalıysa). Frames kayıtlarında 'filed' yok; bilgi tarihi = çeyrek sonundan
  sonraki ilk Nasdaq açıklama günü ya da SEC özütlerindeki ilk 10-Q / 10-K başvuru günü (hangisi önce), ikisi de yoksa çeyrek sonu
  + {E['bilgi_yedek_gun']} gün. Frames değerleri son başvurudaki (gerekirse düzeltilmiş) değerdir: küçük bir geriye dönük düzeltme etkisi.
- Ön kayıt anında durum: SEC, istenen kimlik satırıyla (User-Agent '{K57_SEC_UA}', e-posta yok)
  9 Kas 2026'da 403 ('Undeclared Automated Tool') döndürdü. Başka kimlikle deneme yapılmaz.
- YEDEK KURAL: ABD karar hücrelerindeki olayların en az %{E['abd_temel_kapsam_min'] * 100:.0f}'ında F1-F3 hesaplanamıyorsa ABD'de F1-F3 ATLANIR ve
  o satırlar 'ABD TEMEL VERİSİ YOK' diye işaretlenir; F1-F3 içeren varyantların (V1-V4, D1, D3) kararı 'ÖLÇÜLEMEDİ (ABD TEMEL VERİSİ YOK)'
  olur, İZ / ABD-ADAY denemez. Fiyat + pay kısmı (F7, F6, F4) yine ölçülür ve 'kısmi karar' bilgi olarak yazılır. BIST tam profille ölçülür.

## 6. Beklenti (önceden)
K28: iyi bilanço tepkisi BIST'te artı, ABD 2023'te artı, ABD 2024-26'da eksi (-%1,4) çıkmıştı; çöl + güçlü tepki örneklem dışında
tersine dönmüştü. Beklenti: V0 tutmaz; temel süzgeçler n'yi çok küçültür (BIST V3 hücre başına muhtemelen < 30); profilin iki ABD
hücresinde birden tutma olasılığı düşük. Sonuç ne olursa olsun eşik değişmez.

## 7. İz çıkmazsa sıradaki 3 deneme (önceden yazıldı; sonuç görülmeden; HEPSİ KOŞULUR, ayrı etiketle)
- D1 'F2 1,2 kat': F2'de 1,4 yerine 1,2 (V1-V4).
- D2 '120 gün ufuk': aynı varyantlar (V0-V4), FI_OLCUT ufku 120 gün (portföy tutma da 120 gün; kriz kesiği aynı).
- D3 'art arda iki ivmeli çeyrek': F2 hem bu çeyrekte hem bir önceki çeyrekte (önceki çeyrek satışı >= 1,4 x ondan önceki iki çeyrek,
  önceki çeyrek kârı > 0 ve kendinden önceki çeyrekten büyük) (V1-V4).
Devamlar aynı karar kuralıyla okunur; çoklu deneme nedeniyle yalnız ana varyantın (V3) iki ABD karar hücresi kanıt sayılır, devamlar aday üretir.
"""


def k57_onkayit(cikti: Optional[str] = None) -> str:
    """Ön kaydı yazar. Dosya varsa ÜZERİNE YAZMAZ (eşikler sonradan değişmesin): mühür aynıysa yolu döndürür, değilse durur."""
    yol = _k57_yol("onkayit", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True)
    if os.path.exists(yol):
        mevcut = _k57_onkayit_sha(yol)
        if mevcut != k57_esik_sha():
            raise K57Hata(f"ön kayıt zaten var ve mühür farklı ({mevcut} != {k57_esik_sha()}): eşikler ön kayıttan sonra değişmiş")
        k57log.info("ön kayıt zaten var (mühür aynı): %s", yol)
        return yol
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    with open(yol, "w", encoding="utf-8") as f:
        f.write(k57_onkayit_metin(zaman))
    k57log.info("ön kayıt yazıldı: %s (mühür %s)", yol, k57_esik_sha()[:12])
    return yol


def _k57_onkayit_sha(yol: str) -> Optional[str]:
    with open(yol, encoding="utf-8") as f:
        m = re.search(r"^ESIK_SHA256: ([0-9a-f]{64})$", f.read(), re.M)
    return m.group(1) if m else None


def k57_onkayit_dogrula(cikti: Optional[str] = None) -> Dict[str, str]:
    yol = _k57_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise K57Hata(f"ön kayıt yok ({yol}): önce `python K57.py onkayit`")
    sha = _k57_onkayit_sha(yol)
    if sha != k57_esik_sha():
        raise K57Hata(f"ön kayıt mührü tutmuyor ({sha} != {k57_esik_sha()}): eşikler ön kayıttan sonra değişmiş, koşu durdu")
    with open(yol, encoding="utf-8") as f:
        m = re.search(r"^Yazım zamanı: (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC", f.read(), re.M)
    return {"yol": yol, "sha": sha, "zaman_utc": m.group(1) if m else ""}


# ---------------------------------------------------------------- 1) VERİ
def _k57_git_cikar(dal_yolu: str, hedef: str) -> str:
    """islenmis-veri dalındaki bir dosyayı (git show) hedefe yazar; varsa dokunmaz."""
    if os.path.exists(hedef) and os.path.getsize(hedef) > 0:
        return hedef
    os.makedirs(os.path.dirname(hedef), exist_ok=True)
    for deneme in range(2):
        r = subprocess.run(["git", "-C", KOK_K57, "show", f"{K57_DAL}:{dal_yolu}"], capture_output=True)
        if r.returncode == 0 and r.stdout:
            gecici = hedef + ".yarim"
            with open(gecici, "wb") as f:
                f.write(r.stdout)
            os.replace(gecici, hedef)
            return hedef
        if deneme == 0:
            k57log.warning("%s dalda bulunamadı, dal getiriliyor", dal_yolu)
            subprocess.run(["git", "-C", KOK_K57, "fetch", "origin", "islenmis-veri"], capture_output=True)
    raise FileNotFoundError(f"{K57_DAL}:{dal_yolu} açılamadı: {r.stderr.decode(errors='ignore')[:200]}")


def k57_fiyat(pazar: str) -> Dict[str, pd.DataFrame]:
    """İşlenmiş fiyat sözlüğü (fi_k1_veri çıktısı, islenmis-veri veri/ paketi). Yeniden indirme yok."""
    yol = os.path.join(K57_YOL["veri"], f"V_{pazar}.pkl")
    if not os.path.exists(yol):
        raise FileNotFoundError(f"{yol} yok: `git worktree add /tmp/iv origin/islenmis-veri` + `python FON_IZI.py vpac /tmp/iv/veri /tmp/veri`")
    with open(yol, "rb") as f:
        V = pickle.load(f)
    if not isinstance(V, dict) or not V:
        raise K57Hata(f"{yol}: sözlük değil / boş")
    gerek = {"Open", "High", "Low", "Close", "Volume"}
    bozuk = [s for s, d in V.items() if not isinstance(d, pd.DataFrame) or not gerek <= set(d.columns)]
    if bozuk:
        raise K57Hata(f"{yol}: OHLCV eksik hisse {len(bozuk)} (ör. {bozuk[:3]})")
    k57log.info("%s fiyat: %d hisse", pazar, len(V))
    return V


def k57_kap_liste() -> pd.DataFrame:
    """BIST açıklama günleri: KAP 'Finansal Rapor' listesi (K28), fon_izi_k28 ile aynı ön işlem (ilk rapor, 18:00 sonrası ertesi gün)."""
    yol = _k57_git_cikar("pead/liste_bist.csv.gz", os.path.join(K57_YOL["onbellek"], "pead", "liste_bist.csv.gz"))
    L = pd.read_csv(yol)
    L["t"] = pd.to_datetime(L.yayin, format="%d.%m.%Y %H:%M:%S", errors="coerce")
    L = L.dropna(subset=["t", "yil", "donem"])
    L["yil"] = L.yil.astype(int); L["donem"] = L.donem.astype(int)
    return L


def k57_nasdaq_liste() -> pd.DataFrame:
    yol = _k57_git_cikar("pead/liste_abd.csv.gz", os.path.join(K57_YOL["onbellek"], "pead", "liste_abd.csv.gz"))
    L = pd.read_csv(yol).dropna(subset=["sembol"])
    L["D"] = pd.to_datetime(L.tarih, errors="coerce")
    return L.dropna(subset=["D"])


def _k57_secfs_klasor() -> str:
    k = K57_YOL["secfs"]
    if os.path.isdir(k) and any(f.startswith("fs_") for f in os.listdir(k)):
        return k
    k = os.path.join(K57_YOL["onbellek"], "secfs")
    r = subprocess.run(["git", "-C", KOK_K57, "ls-tree", "--name-only", K57_DAL, "secfs/"], capture_output=True, text=True)
    adlar = [x.split("/", 1)[1] for x in r.stdout.split() if x.startswith("secfs/")]
    if not adlar:
        raise FileNotFoundError("SEC özütleri yok (/tmp/secfs ve islenmis-veri secfs/)")
    for a in adlar:
        _k57_git_cikar("secfs/" + a, os.path.join(k, a))
    return k


def k57_cik_sembol(klasor: str) -> Dict[str, str]:
    """company_tickers.json -> cik (str, sıfırsız) -> borsa kodu (K31 ile aynı eşleme: ilk kayıt)."""
    tk = json.load(open(os.path.join(klasor, "company_tickers.json")))
    out: Dict[str, str] = {}
    for v in tk.values():
        out.setdefault(str(int(v["cik_str"])), str(v["ticker"]).upper().replace(".", "-"))
    return out


def k57_secfs_basvuru(klasor: str) -> pd.DataFrame:
    """SEC özütlerinden başvuru listesi: cik, adsh, form, period (dönem sonu), filed (ilk başvuru günü)."""
    import glob
    parca = []
    for f in sorted(glob.glob(os.path.join(klasor, "fs_*.csv.gz"))):
        try:
            parca.append(pd.read_csv(f, usecols=["adsh", "cik", "form", "period", "filed"], dtype=str).drop_duplicates("adsh"))
        except Exception as ex:   # tek çeyrek bozuksa ötekiler sürer
            k57log.warning("SEC özütü %s okunamadı: %s", f, ex)
    if not parca:
        raise K57Hata(f"{klasor}: fs_*.csv.gz yok")
    B = pd.concat(parca, ignore_index=True).drop_duplicates("adsh")
    B["cik"] = B.cik.astype(str).str.lstrip("0")
    B["filed"] = pd.to_datetime(B.filed, format="%Y%m%d", errors="coerce")
    B["period"] = pd.to_datetime(B.period, format="%Y%m%d", errors="coerce")
    return B.dropna(subset=["filed"])


def k57_fon_pay() -> pd.DataFrame:
    """K25 raporlu fon payı (hisse x ay; bil = yayın anı). FON_IZI fi_k25_pay_tablo(G, oran, dol); K57_FONPAY verilirse o CSV."""
    if K57_YOL["fon_pay"]:
        M = pd.read_csv(K57_YOL["fon_pay"])
    else:
        oku = lambda a: pickle.load(open(os.path.join(K57_YOL["veri"], a), "rb"))  # noqa: E731
        M = FI.fi_k25_pay_tablo(oku("G.pkl"), oku("oran.pkl"), oku("dol.pkl"))
    M = M.assign(bil=pd.to_datetime(M.bil, errors="coerce")).dropna(subset=["bil", "pay"])
    k57log.info("K25 fon payı: %d hisse-ay, %d hisse, %s .. %s", len(M), M.kod.nunique(), M.bil.min().date(), M.bil.max().date())
    return M[["kod", "ay", "pay", "bil"]].sort_values(["kod", "bil"]).reset_index(drop=True)


# ---------------------------------------------------------------- 2) SEC XBRL FRAMES (ABD temel)
def _k57_sec_url(etiket: str, donem: str, birim: str = "USD", tax: str = "us-gaap") -> str:
    return f"https://data.sec.gov/api/xbrl/frames/{tax}/{etiket}/{birim}/{donem}.json"


def k57_sec_listesi() -> List[Tuple[str, str]]:
    """İndirilecek (etiket, dönem) çiftleri: süreli etiketler çeyreklik + yıllık, anlık etiketler çeyrek sonu."""
    a, b = K57_ESIK["sec_ceyrek"]; y0, y1 = K57_ESIK["sec_yil"]
    ceyrek = [f"CY{p.year}Q{p.quarter}" for p in pd.period_range(a, b, freq="Q")]
    out = [(t, c) for t in K57_ABD_GELIR + ("NetIncomeLoss",) for c in ceyrek]
    out += [(t, f"CY{y}") for t in K57_ABD_GELIR + ("NetIncomeLoss",) for y in range(y0, y1 + 1)]
    out += [(t, c + "I") for t in K57_ABD_ANLIK for c in ceyrek]
    return out


def _k57_frame_yol(etiket: str, donem: str) -> Optional[str]:
    """Önbellekte dosya: /tmp/secframes/us-gaap_<etiket>_<dönem>.json ya da ek klasörlerde frame_<etiket>_<dönem>.json."""
    adlar = (f"us-gaap_{etiket}_{donem}.json", f"frame_{etiket}_{donem}.json")
    for k in [K57_YOL["frames"]] + K57_YOL["frames_ek"]:
        for a in adlar:
            y = os.path.join(k, a)
            if os.path.exists(y) and os.path.getsize(y) >= 2:
                return y
    return None


def k57_sec_indir(hiz: float = 8.0) -> Dict[str, Any]:
    """SEC frames indirme: saniyede en çok `hiz` istek, gzip, 3 deneme; 404 = o dönem / etiket yok ('{}' işareti); 403 = SEC reddi, durur.
    Kimlik satırı K57_SEC_UA (e-posta yok); K57_SEC_UA ortam değişkeniyle değiştirilebilir (Cemal'in kararı), günlüğe e-posta yazılmaz."""
    ua = os.environ.get("K57_SEC_UA", K57_SEC_UA)
    os.makedirs(K57_YOL["frames"], exist_ok=True)
    ctx = ssl.create_default_context(cafile=K57_YOL["ca"]) if os.path.exists(K57_YOL["ca"]) else ssl.create_default_context()
    durum = {"indirilen": 0, "onbellek": 0, "yok_404": 0, "hata": [], "durum": "tamam", "ua": _K57_EPOSTA.sub("<e-posta>", ua)}
    son = 0.0
    for etiket, donem in k57_sec_listesi():
        if _k57_frame_yol(etiket, donem):
            durum["onbellek"] += 1; continue
        url = _k57_sec_url(etiket, donem); hedef = os.path.join(K57_YOL["frames"], f"us-gaap_{etiket}_{donem}.json")
        for deneme in range(3):
            bekle = 1.0 / hiz - (time.time() - son)
            if bekle > 0:
                time.sleep(bekle)
            son = time.time()
            try:
                req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "gzip, deflate"})
                with urllib.request.urlopen(req, context=ctx, timeout=90) as r:
                    ham = r.read()
                    if r.headers.get("Content-Encoding") == "gzip":
                        ham = gzip.decompress(ham)
                json.loads(ham)
                with open(hedef + ".yarim", "wb") as f:
                    f.write(ham)
                os.replace(hedef + ".yarim", hedef); durum["indirilen"] += 1
                break
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    with open(hedef, "w") as f:
                        f.write("{}")
                    durum["yok_404"] += 1; break
                if e.code == 403:
                    durum["durum"] = "reddedildi (403)"
                    k57log.error("SEC isteği reddetti (403, %s): indirme durdu; ABD F1-F3 'ABD TEMEL VERİSİ YOK' olacak", url)
                    raise K57SecRet(json.dumps(durum, ensure_ascii=False))
                k57log.warning("SEC %s: HTTP %s (deneme %d)", url, e.code, deneme + 1); time.sleep(2 * (deneme + 1))
            except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
                k57log.warning("SEC %s: %s (deneme %d)", url, str(e)[:120], deneme + 1); time.sleep(2 * (deneme + 1))
        else:
            durum["hata"].append(f"{etiket}/{donem}")
    if durum["hata"]:
        durum["durum"] = "eksik"
    k57log.info("SEC frames: %s", {k: v for k, v in durum.items() if k != "hata"})
    return durum


def _k57_etiket(c: str) -> int:
    """'CY2023Q2' -> çeyrek sırası (yıl * 4 + çeyrek - 1)."""
    m = re.match(r"CY(\d{4})Q(\d)", c)
    return int(m.group(1)) * 4 + int(m.group(2)) - 1


def _k57_ceyrek_sira(t: pd.Timestamp) -> int:
    """Bir dönem sonunu takvim çeyreğine bağlar (frames 'en yakın takvim dönemi' mantığı: bitişten 45 gün önceki günün çeyreği)."""
    g = pd.Timestamp(t) - pd.Timedelta(days=45)
    return g.year * 4 + (g.month - 1) // 3


def k57_abd_temel_tablo(listele: bool = False) -> Tuple[Optional[Dict[str, Any]], str]:
    """Frames -> {'Q': {(cik, etiket): {sıra: (bitiş, değer)}}, 'I': {...}}. Gereken çeyreklik dosyalardan biri yoksa (None, neden)."""
    gerekli = [(t, d) for t, d in k57_sec_listesi() if not re.fullmatch(r"CY\d{4}", d)]
    eksik = [f"{t}/{d}" for t, d in gerekli if _k57_frame_yol(t, d) is None]
    if eksik:
        return None, f"ABD TEMEL VERİSİ YOK: {len(eksik)} / {len(gerekli)} frames dosyası yok (ör. {eksik[:2]})"
    Q: Dict[Tuple[str, str], Dict[int, Tuple[pd.Timestamp, float]]] = {}
    I: Dict[Tuple[str, str], Dict[int, Tuple[pd.Timestamp, float]]] = {}
    Y: Dict[Tuple[str, str], List[Tuple[pd.Timestamp, pd.Timestamp, float]]] = {}
    Qs: Dict[Tuple[str, str], Dict[int, pd.Timestamp]] = {}
    for etiket, donem in k57_sec_listesi():
        y = _k57_frame_yol(etiket, donem)
        if y is None:
            continue
        try:
            J = json.load(open(y))
        except (OSError, ValueError) as ex:
            return None, f"ABD TEMEL VERİSİ YOK: {y} okunamadı ({ex})"
        for d in J.get("data", []) or []:
            try:
                cik = str(int(d["cik"])); bit = pd.Timestamp(d["end"]); val = float(d["val"])
            except (KeyError, TypeError, ValueError):
                continue
            if donem.endswith("I"):
                I.setdefault((cik, etiket), {})[_k57_etiket(donem)] = (bit, val)
            elif re.fullmatch(r"CY\d{4}", donem):
                if "start" in d:
                    Y.setdefault((cik, etiket), []).append((pd.Timestamp(d["start"]), bit, val))
            else:
                s = _k57_etiket(donem); Q.setdefault((cik, etiket), {})[s] = (bit, val)
                if "start" in d:
                    Qs.setdefault((cik, etiket), {})[s] = pd.Timestamp(d["start"])
    tureyen = 0
    for anahtar, yillar in Y.items():
        q = Q.setdefault(anahtar, {}); bas = Qs.get(anahtar, {})
        for a0, a1, av in yillar:
            ic = [s for s, (b, _) in q.items() if s in bas and bas[s] >= a0 - pd.Timedelta(days=15) and b <= a1 - pd.Timedelta(days=60)]
            if len(ic) != 3:
                continue
            gun = sum((q[s][0] - bas[s]).days + 1 for s in ic)
            if abs((a1 - a0).days + 1 - gun - 91) > 20:
                continue
            s4 = _k57_ceyrek_sira(a1)
            if s4 not in q and s4 not in ic:
                q[s4] = (a1, av - sum(q[s][1] for s in ic)); tureyen += 1
    k57log.info("ABD temel: %d şirket-etiket çeyreklik, %d anlık, %d türetilmiş 4. çeyrek", len(Q), len(I), tureyen)
    return {"Q": Q, "I": I}, "ABD TEMEL VERİSİ VAR"


def _k57_abd_bilgi_tarihleri(T: Dict[str, Any], N: pd.DataFrame, B: pd.DataFrame, cik2s: Dict[str, str]) -> Dict[Tuple[str, int], pd.Timestamp]:
    """(cik, çeyrek sırası) -> bilgi tarihi: çeyrek sonundan sonraki 120 gün içindeki ilk Nasdaq açıklaması ya da ilk 10-Q / 10-K
    başvurusu (dönem sonu ±10 gün); ikisi de yoksa çeyrek sonu + bilgi_yedek_gun."""
    E = K57_ESIK; s2c = {v: k for k, v in cik2s.items()}
    nas: Dict[str, np.ndarray] = {s2c[s]: np.sort(g.D.to_numpy("datetime64[ns]")) for s, g in N.groupby("sembol") if s in s2c}
    Bq = B[B.form.isin(["10-Q", "10-K", "10-KT"])].dropna(subset=["period"])
    bas: Dict[str, Tuple[np.ndarray, np.ndarray]] = {c: (g.period.to_numpy("datetime64[ns]"), g.filed.to_numpy("datetime64[ns]"))
                                                     for c, g in Bq.groupby("cik")}
    out: Dict[Tuple[str, int], pd.Timestamp] = {}
    uc = np.timedelta64(E["ceyrek_bilgi_max_gun"], "D"); on = np.timedelta64(10, "D")
    for (cik, _e), q in T["Q"].items():
        for s, (bit, _v) in q.items():
            if (cik, s) in out:
                continue
            b = np.datetime64(bit); aday = []
            if cik in nas:
                x = nas[cik]; x = x[(x > b) & (x <= b + uc)]
                if len(x):
                    aday.append(x[0])
            if cik in bas:
                p, f = bas[cik]; m = (np.abs(p - b) <= on) & (f > b)
                if m.any():
                    aday.append(f[m].min())
            out[(cik, s)] = pd.Timestamp(min(aday)) if aday else bit + pd.Timedelta(days=E["bilgi_yedek_gun"])
    return out


def k57_abd_temel_ekle(X: pd.DataFrame, T: Dict[str, Any], bilgi: Dict[Tuple[str, int], pd.Timestamp], cik2s: Dict[str, str],
                       kat_listesi: Tuple[float, ...] = (1.4, 1.2)) -> pd.DataFrame:
    """ABD olaylarına F1-F3 girdileri: o gün bilinen en son çeyrek (bilgi <= D, D - çeyrek sonu <= 120 gün) ve öncekiler."""
    E = K57_ESIK; s2c = {v: k for k, v in cik2s.items()}; sat = []
    uc = pd.Timedelta(days=E["ceyrek_bilgi_max_gun"])
    cq: Dict[str, Dict[int, pd.Timestamp]] = {}
    for (c, e), q in T["Q"].items():
        if e in K57_ABD_GELIR + ("NetIncomeLoss",):
            for s, (b, _) in q.items():
                cq.setdefault(c, {})[s] = b
    for r in X.itertuples():
        cik = s2c.get(r.sembol); D = pd.Timestamp(r.D); z: Dict[str, Any] = {}
        if cik is not None:
            adaylar = [s for s, b in cq.get(cik, {}).items() if bilgi.get((cik, s), D + pd.Timedelta(days=1)) <= D and D - b <= uc]
            if adaylar:
                s0 = max(adaylar); kul = set()

                def deger(etiketler: Tuple[str, ...], sira: List[int], tablo: str = "Q") -> Tuple[Optional[str], List[float]]:
                    for e in etiketler:
                        q = T[tablo].get((cik, e), {})
                        if all(s in q and bilgi.get((cik, s), D + pd.Timedelta(days=1)) <= D for s in sira):
                            kul.update(sira); return e, [q[s][1] for s in sira]
                    return None, [np.nan] * len(sira)
                _, (g0, g4) = deger(K57_ABD_GELIR, [s0, s0 - 4])
                _, (h0, h1, h2) = deger(K57_ABD_GELIR, [s0, s0 - 1, s0 - 2])
                _, (k1, k2, k3) = deger(K57_ABD_GELIR, [s0 - 1, s0 - 2, s0 - 3])
                _, (n0, n1, n2) = deger(("NetIncomeLoss",), [s0, s0 - 1, s0 - 2])
                _, (oz,) = deger(("StockholdersEquity",), [s0], "I")
                _, (yk,) = deger(("Liabilities",), [s0], "I")
                if not np.isfinite(yk):
                    _, (lse,) = deger(("LiabilitiesAndStockholdersEquity",), [s0], "I")
                    yk = lse - oz if np.isfinite(lse) and np.isfinite(oz) else np.nan
                z = {"cik": cik, "ceyrek_sira": s0, "satis0": h0 if np.isfinite(h0) else g0, "satis_yoy": g0 / g4 - 1 if g0 > 0 and g4 > 0 else np.nan,
                     "_s": (h0, h1, h2), "_k": (k1, k2, k3), "_n": (n0, n1, n2), "ozkaynak": oz, "yukumluluk": yk,
                     "bilgi_son": max(bilgi[(cik, s)] for s in kul) if kul else pd.NaT}
        sat.append(z)
    Z = pd.DataFrame(sat, index=X.index)
    for c in ("satis0", "satis_yoy", "ozkaynak", "yukumluluk", "bilgi_son", "cik", "ceyrek_sira"):
        X[c] = Z[c] if c in Z else np.nan
    bos = (np.nan, np.nan, np.nan)
    s = [v if isinstance(v, tuple) else bos for v in (Z["_s"] if "_s" in Z else [bos] * len(X))]
    k = [v if isinstance(v, tuple) else bos for v in (Z["_k"] if "_k" in Z else [bos] * len(X))]
    n = [v if isinstance(v, tuple) else bos for v in (Z["_n"] if "_n" in Z else [bos] * len(X))]
    X["F1"] = _k57_bool(X.satis_yoy >= E["F1_abd_yoy"], X.satis_yoy)
    for kat in kat_listesi:
        X[_k57_f2_ad(kat)] = _k57_f2(np.array([a[0] for a in s]), np.array([a[1] for a in s]), np.array([a[2] for a in s]),
                                     np.array([a[0] for a in n]), np.array([a[1] for a in n]), kat)
    X["F2_once"] = _k57_f2(np.array([a[0] for a in k]), np.array([a[1] for a in k]), np.array([a[2] for a in k]),
                           np.array([a[1] for a in n]), np.array([a[2] for a in n]), E["F2_kat"])
    oz, yk = X.ozkaynak.astype(float), X.yukumluluk.astype(float)
    X["F3"] = _k57_bool((oz > 0) & (yk <= E["F3_abd_borc_kat"] * oz), oz + yk)
    return X


# ---------------------------------------------------------------- 3) ORTAK ÖLÇÜLER
def _k57_bool(kosul: pd.Series, girdi: pd.Series) -> pd.Series:
    """Girdi NaN ise süzgeç hesaplanamadı -> False (olay o varyanta girmez)."""
    return (pd.Series(kosul, index=girdi.index).fillna(False).astype(bool) & pd.Series(girdi, index=girdi.index).notna())


def _k57_f2_ad(kat: float) -> str:
    return "F2" if abs(kat - K57_ESIK["F2_kat"]) < 1e-12 else "F2_" + str(kat).replace(".", "")


def _k57_f2(s0, s1, s2, n0, n1, kat: float) -> np.ndarray:
    """F2: s0 >= kat x ortalama(s1, s2) (ortalama > 0) VE n0 > 0 VE n0 > n1; eksik veri -> False."""
    s0, s1, s2, n0, n1 = (np.asarray(v, float) for v in (s0, s1, s2, n0, n1))
    with np.errstate(invalid="ignore"):
        ort = (s1 + s2) / 2
        ok = np.isfinite(s0) & np.isfinite(ort) & (ort > 0) & np.isfinite(n0) & np.isfinite(n1)
        return ok & (s0 >= kat * ort) & (n0 > 0) & (n0 > n1)


def k57_kayan_esik(t: pd.Series, x: pd.Series, q: float, gun: int, min_n: int) -> np.ndarray:
    """Her olay için eşik = (t - gun, t] penceresinde (yalnız o ana kadar bilinen olaylar, kendisi dahil) x'in q yüzdeliği; az veri -> NaN."""
    tt = pd.to_datetime(pd.Series(t)).to_numpy("datetime64[ns]"); xv = pd.Series(x).to_numpy(float)
    o = np.argsort(tt, kind="mergesort"); ts = tt[o]; xs = xv[o]; gec = np.isfinite(xs)
    out = np.full(len(xv), np.nan); g = np.timedelta64(int(gun), "D")
    for k in range(len(ts)):
        a = np.searchsorted(ts, ts[k] - g, side="right"); b = np.searchsorted(ts, ts[k], side="right")
        w = xs[a:b][gec[a:b]]
        if len(w) >= min_n:
            out[o[k]] = np.quantile(w, q)
    return out


def k57_fiyat_olcu(V: Dict[str, pd.DataFrame], X: pd.DataFrame) -> pd.DataFrame:
    """Ham tepki, 250 gün tepeden uzaklık, 60 gün getiri ve o gün pazar medyanı; F6 ve F7 (kayan, geleceğe bakmayan eşik)."""
    E = K57_ESIK; S = sorted(V); idx = pd.DatetimeIndex(sorted(set().union(*[V[s].index for s in S])))
    C = pd.DataFrame({s: V[s].Close for s in S}).reindex(idx)
    Cf = C.ffill(limit=5)
    Hm = pd.DataFrame({s: V[s].High for s in S}).reindex(idx).rolling(E["F6_tepe_gun"], min_periods=E["F6_tepe_min"]).max()
    M = Cf / Cf.shift(E["F6_mom_gun"]) - 1
    med = M.median(axis=1, skipna=True).to_numpy()
    Ca, Cfa, Ha, Ma = C.to_numpy(float), Cf.to_numpy(float), Hm.to_numpy(float), M.to_numpy(float)
    ti = {t: i for i, t in enumerate(idx)}; kol = {s: j for j, s in enumerate(S)}
    ham, dd, mom, mmed = [], [], [], []
    for r in X.itertuples():
        i, b, j = ti.get(pd.Timestamp(r.d0)), ti.get(pd.Timestamp(r.tepki_son)), kol.get(r.sembol)
        if i is None or b is None or j is None:
            ham.append(np.nan); dd.append(np.nan); mom.append(np.nan); mmed.append(np.nan); continue
        c0 = Ca[i, j]
        ham.append(Ca[b, j] / c0 - 1 if np.isfinite(c0) and c0 > 0 else np.nan)
        dd.append(Cfa[i, j] / Ha[i, j] - 1 if np.isfinite(Ha[i, j]) and Ha[i, j] > 0 else np.nan)
        mom.append(Ma[i, j]); mmed.append(med[i])
    X = X.copy()
    X["ham"], X["dd250"], X["mom60"], X["mom60_med"] = ham, dd, mom, mmed
    X["F6"] = _k57_bool((X.dd250 >= E["F6_dd_alt"]) & (X.dd250 <= E["F6_dd_ust"]) & (X.mom60 < X.mom60_med), X.dd250 + X.mom60 + X.mom60_med)
    X["f7_esik"] = k57_kayan_esik(X.tepki_son, X.ear, 1 - E["F7_dilim"], E["F7_pencere_gun"], E["F7_min_n"])
    X["F7"] = _k57_bool((X.ear >= X.f7_esik) & (X.ham >= E["F7_ham"]), X.ear + X.f7_esik + X.ham)
    return X


# ---------------------------------------------------------------- 4) OLAYLAR
def k57_olay_bist(Vb: Dict[str, pd.DataFrame], L: pd.DataFrame, T: pd.DataFrame, M: pd.DataFrame) -> pd.DataFrame:
    """BIST olayları: KAP açıklama günü -> K28 tepki / giriş (fi_k28_olaylar) + temel_duz (bilgi tarihi KAP yayını) + K25 fon payı."""
    E = K57_ESIK
    L = L.assign(sembol=[next((x.strip() for x in str(k).split(",") if x.strip() in Vb), None) for k in L.kod]).dropna(subset=["sembol"])
    L = L.sort_values("t").drop_duplicates(["sembol", "yil", "donem"])
    L = L.assign(D=L.t.dt.normalize() + pd.to_timedelta((L.t.dt.hour >= 18).astype(int), unit="D"))
    A_ = L.sort_values(["D", "yil", "donem"]).drop_duplicates(["sembol", "D"], keep="last")
    X = FI.fi_k28_olaylar(A_[["sembol", "D"]], Vb, "BIST", FI.FI_K28)
    X = X.rename(columns={"ust": "K28_ust"}).merge(A_[["sembol", "D", "yil", "donem", "t"]], on=["sembol", "D"], how="left")
    k57log.info("BIST: %d KAP raporu -> %d olay (tepki ölçülebilen)", len(A_), len(X))
    # temel: bilgi tarihi = o dönemin KAP günü (D kuralı), KAP yoksa temel_duz 'aciklama' (yasal süre vekili)
    T = T.copy(); T["aciklama"] = pd.to_datetime(T.aciklama)
    kap = L.set_index(["sembol", "yil", "donem"]).D
    T["bilgi"] = [kap.get((s, y, q), a) for s, y, q, a in zip(T.sembol, T.yil, T.q, T.aciklama)]
    tt = {(s, y * 4 + q - 1): r for s, y, q, r in zip(T.sembol, T.yil, T.q, T.to_dict("records"))}
    sat = []
    for r in X.itertuples():
        D = pd.Timestamp(r.D); s0 = int(r.yil) * 4 + int(r.donem) - 1; kul = []

        def al(k: int, c: str) -> float:
            z = tt.get((r.sembol, s0 - k))
            if z is None or not pd.notna(z.get(c)) or pd.Timestamp(z["bilgi"]) > D:
                return np.nan
            kul.append(pd.Timestamp(z["bilgi"])); return float(z[c])
        v = {f"s{k}": al(k, "satis_q") for k in (0, 1, 2, 3, 4)}
        v.update({f"n{k}": al(k, "net_kar_q") for k in (0, 1, 2)})
        v["ozkaynak"] = al(0, "ozkaynak"); v["borc_oz"] = al(0, "borc_oz")
        v["bilgi_son"] = max(kul) if kul else pd.NaT
        sat.append(v)
    Z = pd.DataFrame(sat, index=X.index); X = pd.concat([X, Z], axis=1)
    X["satis0"] = X.s0
    X["satis_yoy"] = np.where((X.s0 > 0) & (X.s4 > 0), X.s0 / X.s4 - 1, np.nan)
    X["f1_esik"] = k57_kayan_esik(X.D, X.satis_yoy, 1 - E["F1_bist_dilim"], E["F1_pencere_gun"], E["F1_min_n"])
    X["F1"] = _k57_bool(X.satis_yoy >= X.f1_esik, X.satis_yoy + X.f1_esik)
    for kat in (E["F2_kat"], E["deney"]["D1"]["F2_kat"]):
        X[_k57_f2_ad(kat)] = _k57_f2(X.s0, X.s1, X.s2, X.n0, X.n1, kat)
    X["F2_once"] = _k57_f2(X.s1, X.s2, X.s3, X.n1, X.n2, E["F2_kat"])
    X["F3"] = _k57_bool((X.ozkaynak > 0) & (X.borc_oz < E["F3_bist_borc_oz"]), X.ozkaynak + X.borc_oz)
    # F5: yayın anı D'den önce olan en son ay
    pay, bil = [], []
    Mg = {k: (g.bil.to_numpy("datetime64[ns]"), g.pay.to_numpy(float)) for k, g in M.groupby("kod")}
    for r in X.itertuples():
        b = Mg.get(r.sembol)
        if b is None:
            pay.append(0.0); bil.append(pd.NaT); continue
        i = np.searchsorted(b[0], np.datetime64(pd.Timestamp(r.D)), side="left") - 1
        pay.append(float(b[1][i]) if i >= 0 else 0.0); bil.append(pd.Timestamp(b[0][i]) if i >= 0 else pd.NaT)
    X["fon_pay"], X["fon_bil"] = pay, bil
    X["F5"] = X.fon_pay < E["F5_fon_pay"]
    X["F4"] = pd.NA
    X = k57_fiyat_olcu(Vb, X)
    X["pazar"] = "BIST"
    return X


def k57_olay_abd(Va: Dict[str, pd.DataFrame], N: pd.DataFrame, B: pd.DataFrame, cik2s: Dict[str, str], secfs: str) -> pd.DataFrame:
    """ABD olayları: Nasdaq takvimi (2022-12 sonrası, K28) + SEC 10-Q / 10-K başvuru günü (2021-01 .. 2022-11) -> fi_k28_olaylar; F4 SEC."""
    E = K57_ESIK
    Nn = N[(N.D >= E["nasdaq_bas"]) & N.sembol.isin(Va)].drop_duplicates(["sembol", "D"])[["sembol", "D", "surpriz", "ceyrek"]]
    Bs = B[B.form.isin(["10-Q", "10-K", "10-KT"]) & (B.filed >= E["abd_bas"]) & (B.filed < E["nasdaq_bas"])].copy()
    Bs["sembol"] = Bs.cik.map(cik2s); Bs = Bs[Bs.sembol.isin(Va)]
    Bs = Bs.sort_values("filed").drop_duplicates(["sembol", "filed"]).rename(columns={"filed": "D"})
    A_ = pd.concat([Nn.assign(kaynak="nasdaq"), Bs[["sembol", "D"]].assign(surpriz=np.nan, ceyrek=None, kaynak="sec_basvuru")], ignore_index=True)
    A_ = A_.drop_duplicates(["sembol", "D"]).reset_index(drop=True)
    X = FI.fi_k28_olaylar(A_[["sembol", "D", "surpriz"]], Va, "ABD", FI.FI_K28)
    X = X.rename(columns={"ust": "K28_ust"}).merge(A_[["sembol", "D", "kaynak", "ceyrek"]], on=["sembol", "D"], how="left")
    k57log.info("ABD: %d takvim / başvuru günü -> %d olay (nasdaq %d, sec %d)", len(A_), len(X), (X.kaynak == "nasdaq").sum(),
                (X.kaynak == "sec_basvuru").sum())
    # F4: o güne kadar başvurusu yapılmış en son bildirimin yıllık pay değişimi (FON_IZI K31)
    F = FI.fi_k31_finansal(dict(FI.FI_K31, klasor=secfs))
    Fg = {s: (g.filed.to_numpy("datetime64[ns]"), g.pay_yil.to_numpy(float)) for s, g in F.sort_values("filed").groupby("sembol")}
    py, pf = [], []
    for r in X.itertuples():
        g = Fg.get(r.sembol)
        i = np.searchsorted(g[0], np.datetime64(pd.Timestamp(r.D)), side="right") - 1 if g is not None else -1
        py.append(float(g[1][i]) if i >= 0 else np.nan); pf.append(pd.Timestamp(g[0][i]) if i >= 0 else pd.NaT)
    X["pay_yil"], X["pay_filed"] = py, pf
    X["F4"] = k57_f4(X.pay_yil)
    X["F5"] = pd.NA
    X = k57_fiyat_olcu(Va, X)
    X["pazar"] = "ABD"
    return X


def k57_f4(pay_yil: pd.Series) -> pd.Series:
    """F4: yıllık pay değişimi <= +%10; oran (1 + değişim) bir tamsayıya (>= 2) ±%3 yakınsa bölünme (geçer); veri yok -> False."""
    E = K57_ESIK; r = 1 + pd.Series(pay_yil, dtype=float); k = r.round()
    bolunme = (k >= 2) & ((r / k - 1).abs() <= E["F4_bolunme_tol"])
    return _k57_bool((pay_yil <= E["F4_pay_yil"]) | bolunme, pd.Series(pay_yil, dtype=float))


# ---------------------------------------------------------------- 5) VARYANT + ÖLÇÜM
def k57_maske(X: pd.DataFrame, suzgec: List[str], atla: List[str], f2: str = "F2") -> pd.Series:
    m = pd.Series(True, index=X.index)
    for f in suzgec:
        if f in atla:
            continue
        kol = f2 if f == "F2" else f
        if kol == "F2_ivme2":
            m &= X["F2"].fillna(False).astype(bool) & X["F2_once"].fillna(False).astype(bool)
        else:
            m &= X[kol].fillna(False).astype(bool)
    return m


def k57_portfoy_yuzdelik(X: pd.DataFrame, O: Dict[str, Any]) -> float:
    """BİLGİ: gerçek slot portföyünün 200 eşli rastgele portföy içindeki yüzdeliği (FI_OLCUT slot kuralı; ayrı tohum). Karar
    fi_olcut_hucre'nin p90 kıyasıyla verilir; bu sayı yalnız tabloya yazılır."""
    X = X.dropna(subset=["fark"]).sort_values("giris")
    if not len(X):
        return np.nan
    gun = pd.to_datetime(X.giris).to_numpy().astype("datetime64[D]").astype(np.int64); rng = np.random.default_rng(O["tohum"] + 57)

    def slot(getiri: np.ndarray) -> float:
        bos = np.zeros(O["slot"]); deger = np.ones(O["slot"]) / O["slot"]
        for gi, ri in zip(gun, getiri):
            k = int(np.argmin(bos))
            if bos[k] <= gi:
                deger[k] *= 1 + ri; bos[k] = gi + int(O["ufuk"] * 1.45)
        return float(deger.sum() - 1)
    gercek = slot(X.r60.to_numpy(float))
    rast = np.array([slot(np.array([rng.choice(e) if e is not None and len(e) else x for e, x in zip(X["_esler"], X.r60.to_numpy(float))]))
                     for _ in range(O["port_n"])])
    return float((rast < gercek).mean())


def k57_tutar(z: Dict[str, Any], O: Dict[str, Any]) -> bool:
    """FI_OLCUT dört şartı (fi_olcut_karar'daki ile aynı)."""
    try:
        return bool(z["n"] >= O["n_esik"] and z["alt95"] > 0 and z["sira"] > 0.5 and z["portfoy"] > z["portfoy_esli_p90"])
    except (KeyError, TypeError):
        return False


def k57_hucreler(X: pd.DataFrame, pazar: str, deney: str, varyantlar: List[str], atla: List[str], O: Dict[str, Any],
                 f2: str = "F2") -> List[Dict[str, Any]]:
    E = K57_ESIK; out = []
    for v in varyantlar:
        suz = E["varyant"][v]; m = k57_maske(X, suz, atla, f2)
        for ad, a, b in E["hucre"][pazar]:
            g = pd.to_datetime(X.giris); S = X[m & (g >= a) & (g <= b)]
            z = FI.fi_olcut_hucre(S, O) if len(S) else {"n": 0}
            rol = "KARAR" if [pazar, ad] in E["karar_hucre"] else "BİLGİ"
            out.append({"deney": deney, "varyant": v, "suzgec": "+".join(f for f in suz if f not in atla),
                        "eksik": "+".join(f for f in suz if f in atla), "f2": f2, "ufuk": O["ufuk"], "pazar": pazar, "donem": ad, "rol": rol,
                        "olay_n": int(len(S)), **z, "portfoy_yuzdelik": k57_portfoy_yuzdelik(S, O) if z.get("n", 0) else np.nan,
                        "tutar": k57_tutar(z, O)})
    return out


def k57_karar(Z: pd.DataFrame, abd_temel: bool) -> Dict[Tuple[str, str], Dict[str, str]]:
    """Her (deney, varyant) için karar: FON_IZI _fi_olcut_karar_ortak (karar pazarları ABD + AVR; BIST bilgi)."""
    E = K57_ESIK; O = _k57_olcut(); out = {}
    for (d, v), g in Z.groupby(["deney", "varyant"], sort=False):
        t = {}
        for r in g.itertuples():
            if r.pazar == "ABD" and r.donem in ("2023", "2024-26"):
                t[("ABD", r.donem)] = bool(r.tutar)
            elif r.pazar == "BIST":
                t[("BIST", E["bist_karar_eslem"][r.donem])] = bool(r.tutar)
        k = FI._fi_olcut_karar_ortak(t, O).replace("(AVR verisi yok)", "(AVRUPA VERİSİ YOK)") if any(p == "ABD" for p, _ in t) else "İZ DEĞİL (ABD ölçülmedi)"
        temel_gerek = any(f in E["varyant"][v] for f in K57_TEMEL) or d in ("D1", "D3")
        ana = k if (abd_temel or not temel_gerek) else "ÖLÇÜLEMEDİ (ABD TEMEL VERİSİ YOK)"
        bist = all(t.get(("BIST", x), False) for x in ("2023", "2024-26"))
        out[(d, v)] = {"karar": ana, "kismi": k, "bist_iki_hucre": "TUTAR" if bist else "tutmaz"}
    return out


# ---------------------------------------------------------------- 6) SÜRÜCÜ
def k57_kos(cikti: Optional[str] = None, indir: bool = True) -> Dict[str, Any]:
    """Ön kayıt mührü doğrulanır -> veri -> olaylar -> süzgeçler -> FI_OLCUT -> 3 devam -> çıktılar + rapor."""
    cikti = cikti or K57_YOL["cikti"]; os.makedirs(cikti, exist_ok=True)
    ok = k57_onkayit_dogrula(cikti)
    bas = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    k57log.info("%s | ön kayıt %s (%s)", K57_SURUM, ok["zaman_utc"], ok["sha"][:12])
    E = K57_ESIK; O60 = _k57_olcut(); O120 = dict(O60, ufuk=E["deney"]["D2"]["ufuk"])
    meta: Dict[str, Any] = {"surum": K57_SURUM, "onkayit": ok, "kos_baslangic": bas, "sec": {}, "veri": {}}
    # ABD temel (SEC frames)
    if indir:
        try:
            meta["sec"] = k57_sec_indir()
        except K57SecRet as ex:
            meta["sec"] = json.loads(str(ex))
    T_abd, neden = k57_abd_temel_tablo()
    meta["abd_temel_kaynak"] = neden; k57log.info("%s", neden)
    # veri
    Vb, Va = k57_fiyat("BIST"), k57_fiyat("ABD")
    secfs = _k57_secfs_klasor(); cik2s = k57_cik_sembol(secfs); B = k57_secfs_basvuru(secfs)
    Lk, N = k57_kap_liste(), k57_nasdaq_liste()
    Tb = pd.read_csv(os.path.join(KOK_K57, "temel_duz.csv")); M = k57_fon_pay()
    meta["veri"] = {"V_BIST": len(Vb), "V_ABD": len(Va), "kap_rapor": len(Lk), "nasdaq_satir": len(N), "secfs_basvuru": len(B),
                    "temel_duz": len(Tb), "fon_pay_ay": len(M)}
    # olaylar
    Xb = k57_olay_bist(Vb, Lk, Tb, M)
    Xa = k57_olay_abd(Va, N, B, cik2s, secfs)
    abd_temel = False
    if T_abd is not None:
        bilgi = _k57_abd_bilgi_tarihleri(T_abd, N, B, cik2s)
        Xa = k57_abd_temel_ekle(Xa, T_abd, bilgi, cik2s, (E["F2_kat"], E["deney"]["D1"]["F2_kat"]))
        g = pd.to_datetime(Xa.giris); kh = (g >= "2023-01-01") & (g <= "2026-12-31")
        kapsam = float((Xa.loc[kh, "satis_yoy"].notna() & Xa.loc[kh, "ozkaynak"].notna()).mean()) if kh.any() else 0.0
        abd_temel = kapsam >= E["abd_temel_kapsam_min"]
        meta["abd_temel_kapsam"] = kapsam
        if not abd_temel:
            meta["abd_temel_kaynak"] = f"ABD TEMEL VERİSİ YOK: karar hücrelerinde kapsam %{kapsam * 100:.0f} < %{E['abd_temel_kapsam_min'] * 100:.0f}"
    if not abd_temel:
        for c in ("F1", "F2", _k57_f2_ad(E["deney"]["D1"]["F2_kat"]), "F2_once"):
            Xa[c] = pd.NA
    atla = {"BIST": list(K57_ATLA["BIST"]), "ABD": list(K57_ATLA["ABD"]) + ([] if abd_temel else list(K57_TEMEL))}
    meta["atla"] = atla; meta["abd_temel"] = abd_temel
    # ölçüm: bütün olaylar bir kez (60 ve 120 gün), hücreler maskeyle
    Z: List[Dict[str, Any]] = []; olay_kayit = {}
    for pazar, X, V in (("BIST", Xb, Vb), ("ABD", Xa, Va)):
        P60 = FI.fi_olcut_panel(V, O60)
        X60 = FI.fi_olcut_olay(P60, X[["sembol", "giris"]])
        X = X.assign(r60=X60.r60.to_numpy(), esli_r60=X60.esli_r60.to_numpy(), sira=X60.sira.to_numpy(), fark=X60.fark.to_numpy(),
                     _esler=list(X60["_esler"]))
        del P60
        for v in E["varyant"]:
            X[v] = k57_maske(X, E["varyant"][v], atla[pazar])
        Z += k57_hucreler(X, pazar, "ANA", list(E["varyant"]), atla[pazar], O60)
        temel_var = pazar == "BIST" or abd_temel
        if temel_var:
            Z += k57_hucreler(X, pazar, "D1", E["deney"]["D1"]["varyant"], atla[pazar], O60, _k57_f2_ad(E["deney"]["D1"]["F2_kat"]))
            Z += k57_hucreler(X, pazar, "D3", E["deney"]["D3"]["varyant"], atla[pazar], O60, "F2_ivme2")
        P120 = FI.fi_olcut_panel(V, O120)
        X120 = FI.fi_olcut_olay(P120, X[["sembol", "giris"]]); del P120
        X2 = X.assign(r60=X120.r60.to_numpy(), esli_r60=X120.esli_r60.to_numpy(), sira=X120.sira.to_numpy(), fark=X120.fark.to_numpy(),
                      _esler=list(X120["_esler"]))
        Z += k57_hucreler(X2, pazar, "D2", E["deney"]["D2"]["varyant"], atla[pazar], O120)
        X["r120"], X["fark120"] = X120.r60.to_numpy(), X120.fark.to_numpy()
        olay_kayit[pazar] = X
        k57log.info("%s ölçüldü: %d olay, V0 %d, V3 %d", pazar, len(X), int(X.V0.sum()), int(X.V3.sum()))
    Zt = pd.DataFrame(Z)
    kr = k57_karar(Zt, abd_temel)
    Zt["karar"] = [kr[(d, v)]["karar"] for d, v in zip(Zt.deney, Zt.varyant)]
    Zt["kismi_karar"] = [kr[(d, v)]["kismi"] for d, v in zip(Zt.deney, Zt.varyant)]
    Zt["bist_iki_hucre"] = [kr[(d, v)]["bist_iki_hucre"] for d, v in zip(Zt.deney, Zt.varyant)]
    # çıktılar
    Zt.to_csv(_k57_yol("hucre", cikti), index=False)
    for pazar, ad in (("BIST", "bist"), ("ABD", "abd")):
        olay_kayit[pazar].drop(columns=["_esler"]).sort_values("D").to_csv(_k57_yol(ad, cikti), index=False)
    meta["kos_bitis"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    meta["karar"] = {f"{d} {v}": k for (d, v), k in kr.items()}
    meta["sayilar"] = {p: {"olay": int(len(X)), **{v: int(X[v].sum()) for v in E["varyant"]},
                           "olculen": int(X.fark.notna().sum())} for p, X in olay_kayit.items()}
    with open(_k57_yol("meta", cikti), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1, default=str)
    rap = k57_rapor(cikti)
    return {"hucre": Zt, "olay": olay_kayit, "karar": kr, "meta": meta, "rapor": rap}


# ---------------------------------------------------------------- 7) RAPOR
def _k57_tablo(Z: pd.DataFrame, deney: str) -> str:
    g = Z[Z.deney == deney]
    if not len(g):
        return "_(bu deney koşulmadı)_\n"
    sat = ["| Varyant | Hücre | Rol | n | Eşli fark | %95 aralık | Sıra | Portföy yüzdeliği | Tutar |", "|---|---|---|---|---|---|---|---|---|"]
    for r in g.itertuples():
        ek = f" (yok: {r.eksik})" if isinstance(r.eksik, str) and r.eksik else ""
        sat.append(f"| {r.varyant}{ek} | {r.pazar} {r.donem} | {r.rol} | {int(r.n) if pd.notna(r.n) else 0} | {_yz(getattr(r, 'ort_fark', np.nan))} | "
                   f"{_yz(getattr(r, 'alt95', np.nan))} .. {_yz(getattr(r, 'ust95', np.nan))} | {_sy(getattr(r, 'sira', np.nan))} | "
                   f"{_sy(r.portfoy_yuzdelik)} | {'**TUTAR**' if r.tutar else 'tutmaz'} |")
    return "\n".join(sat) + "\n"


def _k57_son_olaylar(X: pd.DataFrame, pazar: str, n: int = 10) -> str:
    g = X[X.V3.astype(bool)].sort_values("D").tail(n)
    if not len(g):
        return f"_{pazar}: V3 olayı yok_\n"
    kol = ["| Hisse | Açıklama | Tepki (ham) | Satış yıllık | Tepeden | 60g / pazar medyanı | Fon payı / pay değişimi | r60 | Eşli fark |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in g.itertuples():
        pay = _yz(r.fon_pay) if pazar == "BIST" else _yz(getattr(r, "pay_yil", np.nan))
        kol.append(f"| {r.sembol} | {pd.Timestamp(r.D).date()} | {_yz(r.ham)} | {_yz(getattr(r, 'satis_yoy', np.nan), 0)} | {_yz(r.dd250, 0)} | "
                   f"{_yz(r.mom60, 0)} / {_yz(r.mom60_med, 0)} | {pay} | {_yz(r.r60)} | {_yz(r.fark)} |")
    return "\n".join(kol) + "\n"


def k57_rapor(cikti: Optional[str] = None) -> str:
    """K57_RAPOR.md: karar, ana tablo, 3 devam, eşiğe en yakınlar, son 10 V3 olayı / pazar, YEOTK geçmişi, Ç148 önerisi."""
    cikti = cikti or K57_YOL["cikti"]
    for a in ("hucre", "bist", "abd", "meta"):
        if not os.path.exists(_k57_yol(a, cikti)):
            raise K57Hata(f"rapor için {K57_DOSYA[a]} yok: önce `python K57.py kos`")
    Z = pd.read_csv(_k57_yol("hucre", cikti))
    Xb = pd.read_csv(_k57_yol("bist", cikti), parse_dates=["D"]); Xa = pd.read_csv(_k57_yol("abd", cikti), parse_dates=["D"])
    meta = json.load(open(_k57_yol("meta", cikti), encoding="utf-8")); E = K57_ESIK
    kar = Z.drop_duplicates(["deney", "varyant"]).set_index(["deney", "varyant"])
    ana = kar.loc[("ANA", E["ana_varyant"])]
    abd_temel = bool(meta.get("abd_temel"))
    yakin = Z[(Z.n >= 30)].drop_duplicates(["pazar", "donem", "ufuk", "n", "ort_fark"]).sort_values("alt95", ascending=False).head(5)
    bolunme_n = int((Xa.V3.astype(bool) & (Xa.pay_yil > E["F4_pay_yil"])).sum()) if "pay_yil" in Xa else 0

    def duz(pazar: str, donem: str, d: str = "ANA", v: str = "V3") -> str:
        g = Z[(Z.deney == d) & (Z.varyant == v) & (Z.pazar == pazar) & (Z.donem == donem)]
        if not len(g) or not g.n.iloc[0] or pd.isna(g.n.iloc[0]):
            return f"{pazar} {donem}: olay yok"
        r = g.iloc[0]; yon = "eşlerini GEÇTİ (dört şart tuttu)" if r.tutar else ("ortalamada eşlerinin üstünde ama şartlar tutmadı" if r.ort_fark > 0
                                                                                   else "eşlerinin altında kaldı")
        return f"{pazar} {donem}: {int(r.n)} olay, 60 günde eşlerine göre {_yz(r.ort_fark)} → {yon}"
    tut = Z[Z.tutar.astype(bool)]
    sec = meta.get("sec", {})
    # V3 ABD karar hücreleri (kısmi) kısa özet
    def hucre_ozet(d: str, v: str) -> str:
        g = Z[(Z.deney == d) & (Z.varyant == v)]
        return "; ".join(f"{r.pazar} {r.donem} {_yz(r.ort_fark)} (n {int(r.n) if pd.notna(r.n) else 0}{', TUTAR' if r.tutar else ''})" for r in g.itertuples())
    satir_ozet = "\n".join(f"| {d} | {v} | {kar.loc[(d, v), 'karar']} | {kar.loc[(d, v), 'kismi_karar']} | {hucre_ozet(d, v)} |"
                           for d, v in kar.index)
    yeotk = Xb[Xb.sembol == "YEOTK"].sort_values("D")
    yeotk_t = "\n".join(f"| {pd.Timestamp(r.D).date()} | {int(r.yil)}/{int(r.donem)} | {_yz(r.ham)} | {_yz(r.satis_yoy, 0)} | "
                        f"{'evet' if r.F1 else 'hayır'} / {'evet' if r.F2 else 'hayır'} / {'evet' if r.F3 else 'hayır'} / "
                        f"{'evet' if r.F5 else 'hayır'} / {'evet' if r.F6 else 'hayır'} / {'evet' if r.F7 else 'hayır'} | "
                        f"{'V3' if r.V3 else ('V2' if r.V2 else ('V1' if r.V1 else '—'))} | {_yz(r.fark)} |" for r in yeotk.itertuples())
    ana_karar = ana["karar"]
    ozet_kisa = (f"ABD tam profil ölçülemedi (SEC temel verisi indirilemedi); ABD fiyat + pay kısmı (F7 + F6 + F4): {ana['kismi_karar']}. "
                 if not abd_temel else "") + f"BIST tam profil (bilgi): iki hücrede {ana.get('bist_iki_hucre', '—')}."
    bist_v3 = Z[(Z.deney == "ANA") & (Z.varyant == "V3") & (Z.pazar == "BIST")]
    bist_v3_s = "; ".join(f"{r.donem}: n {int(r.n) if pd.notna(r.n) else 0}, {_yz(r.ort_fark)} ({_yz(r.alt95)} .. {_yz(r.ust95)}), sıra {_sy(r.sira)}, "
                          f"{'TUTAR' if r.tutar else 'tutmaz'}" for r in bist_v3.itertuples())
    abd_v3 = Z[(Z.deney == "ANA") & (Z.varyant == "V3") & (Z.pazar == "ABD")]
    abd_v3_s = "; ".join(f"{r.donem}: n {int(r.n) if pd.notna(r.n) else 0}, {_yz(r.ort_fark)} ({_yz(r.alt95)} .. {_yz(r.ust95)}), sıra {_sy(r.sira)}, "
                         f"{'TUTAR' if r.tutar else 'tutmaz'}" for r in abd_v3.itertuples())
    tutan_s = "; ".join(f"{r.deney} {r.varyant} {r.pazar} {r.donem} {_yz(r.ort_fark)}" for r in tut.itertuples()) or "yok"
    c148 = (f'_ik_k("Ç148", "2026-11-09", "YEOTK PROFİLİ (\'SIKI DOSYA\') ÖN KAYITLI GEÇMİŞ TESTİ: bilanço günü güçlü tepki (F7, kayan üst %20 + ham >= +%5) + satış '
            f'büyümesi (F1) + çeyrek ivmesi ve kâr sıçraması (F2) + sağlam bilanço (F3) + seyrelme yok (F4, ABD) + fon payı < %2 (F5, BIST) + tepeden %30-70 '
            f'aşağıda ve 60 gün pazarın altında (F6); V0-V4, önceden yazılı 3 devam (F2 1,2 kat, 120 gün, iki ivmeli çeyrek)", "K57.py, test_k57.py", '
            f'"Cemal (9 Kas 2026, tek ve son talimat): YEOTK gibi sıkı dosyalar BIST\'te ve ABD\'de eşlerini geçiyor mu?", '
            f'"Yeni deneme (ön kayıt K57_ON_KAYIT.md, sha {meta["onkayit"]["sha"][:12]}; ölçüt FI_OLCUT; karar ABD 2023 + 2024-26, Avrupa verisi yok)", "", 3, '
            f'cikti="arastirma_cikti/k57_yeotk_profili/ (K57_ON_KAYIT.md, K57_RAPOR.md, hucre.csv, olaylar_bist.csv, olaylar_abd.csv)", '
            f'notu="{ana_karar}. Olay: BIST {meta["sayilar"]["BIST"]["olay"]} (V3 {meta["sayilar"]["BIST"]["V3"]}), ABD {meta["sayilar"]["ABD"]["olay"]} '
            f'(V3 kısmi {meta["sayilar"]["ABD"]["V3"]}). BIST V3 (bilgi) {bist_v3_s}. ABD V3 {"" if abd_temel else "(F1-F3 yok, fiyat + pay kısmı) "}{abd_v3_s}. '
            f'Tutan hücreler: {tutan_s}. {meta.get("abd_temel_kaynak", "")}; SEC durumu: {sec.get("durum", "—")}."),')
    metin = f"""# K57 — YEOTK profili ('sıkı dosya') geçmiş testi: RAPOR

Ön kayıt: {meta['onkayit']['zaman_utc']} UTC (sha {meta['onkayit']['sha'][:12]}); koşu {meta['kos_baslangic']} → {meta.get('kos_bitis', '')}. {K57_SURUM}

## KARAR: {ana_karar}

Düz dille:
- {duz('BIST', '2024-26')} (BIST bilgi; 2022-23'te yıllık büyüme için 2022 tabanı gerektiğinden olay çok az: {duz('BIST', '2022-23')}).
- {duz('ABD', '2023')}; {duz('ABD', '2024-26')}{'' if abd_temel else ' (ABD satış / kâr / bilanço süzgeçleri YOK: yalnız güçlü tepki + tepeden düşmüş fiyat + seyrelme yok)'}.
- Bilanço gününe güçlü tepki tek başına (V0, K28 tabanı): {duz('ABD', '2023', 'ANA', 'V0')}; {duz('ABD', '2024-26', 'ANA', 'V0')}.
- Ana sonuç = V3 (tam YEOTK profili), iki ABD karar hücresi (2023, 2024-26). Avrupa'da bilanço olay verisi yok → en fazla ABD-ADAY.
- {ozet_kisa}
- ABD temel verisi: {meta.get('abd_temel_kaynak', '—')} (SEC frames indirme durumu: {sec.get('durum', 'denenmedi')}).
- Olaylar: BIST {meta['sayilar']['BIST']['olay']} (ölçülen {meta['sayilar']['BIST']['olculen']}), ABD {meta['sayilar']['ABD']['olay']} (ölçülen {meta['sayilar']['ABD']['olculen']}).
  Varyant olay sayıları BIST {', '.join(f"{v} {meta['sayilar']['BIST'][v]}" for v in E['varyant'])}; ABD {', '.join(f"{v} {meta['sayilar']['ABD'][v]}" for v in E['varyant'])}.

## Karar tablosu (deney × varyant)
| Deney | Varyant | Karar | Kısmi karar (yalnız ölçülebilen süzgeçlerle) | Hücreler (eşli fark, n) |
|---|---|---|---|---|
{satir_ozet}

## Ana ölçüm (60 gün, FI_OLCUT)
{_k57_tablo(Z, 'ANA')}
## Önceden yazılı 3 devam
D1 — F2 1,2 kat:
{_k57_tablo(Z, 'D1')}
D2 — 120 gün ufuk:
{_k57_tablo(Z, 'D2')}
D3 — art arda iki ivmeli çeyrek:
{_k57_tablo(Z, 'D3')}
## Eşiğe en yakın hücreler (n >= 30, aralık alt ucuna göre)
""" + "\n".join(f"- {r.deney} {r.varyant} {r.pazar} {r.donem}: n {int(r.n)}, eşli fark {_yz(r.ort_fark)}, aralık {_yz(r.alt95)} .. {_yz(r.ust95)}, "
                f"sıra {_sy(r.sira)}, portföy yüzdeliği {_sy(r.portfoy_yuzdelik)}{' — TUTAR' if r.tutar else ''}" for r in yakin.itertuples()) + f"""

## Akıl sağlığı: en son 10 V3 olayı
BIST (tam profil):
{_k57_son_olaylar(Xb, 'BIST')}
ABD ({'tam profil' if abd_temel else 'F1-F3 yok: F7 + F6 + F4'}):
{_k57_son_olaylar(Xa, 'ABD')}
## YEOTK'nın kendi geçmiş olayları (BIST)
| Açıklama | Dönem | Tepki | Satış yıllık | F1 / F2 / F3 / F5 / F6 / F7 | Varyant | Eşli fark |
|---|---|---|---|---|---|---|
{yeotk_t}

5 Kasım 2026 (9A26) olayı örneklemde değil: temel_duz 2026/6'da, fiyatlar 22.10.2026'da bitiyor, ölçüm 31.08.2026'da kesik.

## Notlar ve sınırlar
- Olay kurgusu K28 (fi_k28_olaylar): tepki = açıklama öncesi son kapanış → açıklamadan sonraki ilk kapanış; giriş ertesi açılış.
- F7 ve BIST F1 eşikleri yalnız o güne kadar bilinen olaylardan (son 92 gün) hesaplandı; K28'in çeyrek içi 'ust' etiketi olaylar dosyasında 'K28_ust'.
- F4 bölünme kuralı (önceden yazılı): pay oranı bir tamsayıya ±%3 yakınsa bölünme sayıldı; ABD V3 olaylarından {bolunme_n} tanesi pay artışı > %10 olduğu hâlde bu kuralla geçti (bir kısmı bölünme değil, payı ikiye katlayan ihraç olabilir: kural gevşek tarafta).
- BIST'te F4 (seyrelme) ölçülmedi (bedelsiz / bedelli ayrımı yok); ABD'de F5 yok (fon krizi BIST'e özgü).
- BIST temel verisi temel_duz.csv (İş Yatırım); bilgi tarihi o dönemin KAP yayını (yoksa yasal süre vekili). ABD F4 SEC özütleri (K31).
- ABD evreni V_ABD (1.411 hisse, bugün işlem görenler: hayatta kalma yanlılığı); BIST evreni V_BIST.
- Kişisel e-posta kullanılmadı; SEC istenen kimlik satırını reddetti. ABD tam profil için Cemal'in kararı gerekir (SEC kuralı iletişim bilgisi ister).

## IZ_KARNE önerisi (Ç148; IZ_KARNE.py'ye ana oturum işler)
```
{c148}
```
"""
    yol = _k57_yol("rapor", cikti)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k57log.info("rapor: %s | KARAR: %s", yol, ana_karar)
    return yol


def _cakisma_kontrol_k57(_once=_CK_ONCE_K57, _dosya="K57.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K57", "_CK_KAYIT", "_cakisma_kontrol_k57", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "gzip", "hashlib", "io", "json", "logging", "pickle", "re", "ssl", "subprocess", "time", "urllib",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple", "FI", "_dt")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k57()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    ap = argparse.ArgumentParser(description=K57_SURUM)
    ap.add_argument("komut", choices=["onkayit", "indir", "kos", "rapor"])
    ap.add_argument("--cikti", default=None); ap.add_argument("--indirme", choices=["evet", "hayir"], default="evet")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(k57_onkayit(a.cikti))
        elif a.komut == "indir":
            try:
                print(k57_sec_indir())
            except K57SecRet as ex:
                print("SEC REDDETTİ:", ex); sys.exit(2)
        elif a.komut == "kos":
            R = k57_kos(a.cikti, indir=a.indirme == "evet")
            print("KARAR (V3):", R["karar"][("ANA", K57_ESIK["ana_varyant"])]["karar"]); print(R["rapor"])
        else:
            print(k57_rapor(a.cikti))
    except K57Hata as ex:
        k57log.error("%s", ex); sys.exit(1)
