"""CANLI_TARAMA — haftalık ileri test taraması (20 Kasım 2026; iş tanımı arastirma_cikti/yapi_hedef/CANLI_TARAMA_IS_TANIMI.md).

DÜRÜSTLÜK: bu liste 'izleme / ileri test' listesidir, ÖNERİ DEĞİLDİR. CLAUDE.md öneri modülünün üç kapısından (tarama + dosya + risk) burada
yalnız tarama kapısı var ve seçici ÖLÇÜLEMEDİ düzeyindedir (dipte + gövdeli kırılım KATKI+ ama hücre başına +3..+9 puan).

AKIŞ (kurallar CT_ESIK'te; sha256 arastirma_cikti/canli/CANLI_ON_KAYIT.md'de; sonuca göre değişmez):
  1) VERİ   : evren = /tmp/veri V_*.pkl sembolleri (ABD, AVR, BIST). `--guncelle` ile yfinance (auto_adjust=True) son 400 takvim günü paket
              paket indirilir, eski seriyle birleştirilir (yeni bar eklenir; ortak günlerde fark > %1 uyarı, yeni veri esas; ayarlama oranı
              tek tip ise eski kısım yeni kipe ölçeklenir), /tmp/veri_canli/V_*.pkl yazılır (repoya GİRMEZ). Seans kapanmadan gelen bugünkü
              yarım bar atılır. Yeni barlarda |günlük getiri| > %40 -> 'şüpheli' (listeden dışlanır).
  2) SİNYAL : S6 AL (YAPI_HEDEF.yh_s6_hisse = Y1), havuz (OC kuralı t günündeki bilgiyle: geçerli bar, 60 gün momentum, likidite alt %20
              dışı, geçmiş 61 günde bölünme şüphesi yok), aynı hissede 60 birleşik takvim günü tekil; pazarın son 5 işlem günü içinde.
  3) ÖZELLİK: F1-F18 (GOZ_ETIKET.ge_ozellik_hisse), F19 parmak P1.1, F20-F23 (yh_s7_ozellik), F24-F29 (yh_s9_ozellik), F65-F68 / Ş10
              (yh_s10_ozellik), mahkeme (yh_mahkeme_hisse; 12 kural puanı), puan7 (7. tur M2 birleşik HistGradientBoosting; ayarlar YH_ESIK7;
              eğitim = olay_G6 ölçülen satırları, giriş <= 31.08.2026; model /tmp/veri_canli/puan7_model.pkl).
  4) HAVUZ  : Ş1 (F15 <= 0,25 VE F17 <= -0,20) VE Ş7 (F22 > 0, F22a < 0 yani O_t < F21, F23 >= 0,50). Boşsa (i) Ş1 VE F22 > 0, (ii) Ş1.
  5) SIRA   : puan7 azalan; eşitlikte Ş9 var önce, sonra F18 küçük. En iyi 10, pazar başına en çok 5.
  6) ÇIKTI  : arastirma_cikti/canli/CANLI_TARAMA_<etiket>.md / .json / .pdf (hisse adı ve tarih açık; 120 bar + S6 bölge + hat + F21 +
              Ş9 çanak + MACD(12, 26, 9) + hacim).
  7) İLERİ TEST: `olc --tarih <etiket>`: listedeki adaylar yeni veriyle YAPI_HEDEF cetveliyle (yh_olay_olc: giriş t+1 açılış, 15 geçerli bar,
              +%5 / +%10 stop'tan önce, takip stopu, eş = aynı gün aynı momentum x likidite kovası) ölçülür, CANLI_SONUC.md'ye EKLENİR (silinmez).

Komutlar:
    python CANLI_TARAMA.py onkayit                       CANLI_ON_KAYIT.md (CT_ESIK sha + kontrol listesi; varsa yazmaz)
    python CANLI_TARAMA.py guncelle                      yalnız veri güncellemesi (/tmp/veri_canli)
    python CANLI_TARAMA.py tara [--guncelle] [--etiket YYYY-MM-DD] [--veri KLASOR] [--islem 4]
    python CANLI_TARAMA.py olc --tarih YYYY-MM-DD [--veri KLASOR]      (ya da --vadesi: vadesi gelmiş, ölçülmemiş bütün listeler)
    python CANLI_TARAMA.py model                         puan7 modelini (yeniden) eğit
Colab:  exec(open('CANLI_TARAMA.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Komisyon / kayma YOK. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı). 31.08.2026 fon krizi kesiği YALNIZ bu canlı taramada (bellekte,
geçici) kaldırılır: canlı sinyal kriz sonrası veride aranır; model eğitimi kriz öncesi satırlarla sınırlıdır.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_CT = {k: id(v) for k, v in globals().items()}

import contextlib  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_CT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_CT not in sys.path:
    sys.path.insert(0, KOK_CT)

import ORTAK_CETVEL as OC  # noqa: E402
import SIKISMA_YENIDEN as SY  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402
import GOZ_ETIKET as GE  # noqa: E402

ctlog = logging.getLogger("col.canli_tarama")
if not ctlog.handlers:
    _ct_h = logging.StreamHandler(sys.stderr)
    _ct_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s canli_tarama: %(message)s", "%H:%M:%S"))
    ctlog.addHandler(_ct_h)
    ctlog.setLevel(logging.INFO)
    ctlog.propagate = False

CT_SURUM = "CANLI_TARAMA v1.0 (2026-11-20): S6 son 5 gün + havuz Ş1 VE Ş7 (kademeli) + puan7 sırası; ileri test olc (YAPI_HEDEF cetveli)"
CT_DURUSTLUK = ("DÜRÜSTLÜK: bu liste 'izleme / ileri test' listesidir, ÖNERİ DEĞİLDİR. CLAUDE.md öneri modülünün üç kapısından (tarama + "
                "dosya + risk) burada yalnız tarama kapısı var ve seçici ÖLÇÜLEMEDİ düzeyindedir (dipte + gövdeli kırılım KATKI+ ama hücre "
                "başına +3..+9 puan). Alım-satım kararı Cemal'indir; Claude yatırım danışmanı değildir.")
CT_YOL = {"veri": os.environ.get("OC_VERI", "/tmp/veri"), "canli": os.environ.get("CT_VERI_CANLI", "/tmp/veri_canli"),
          "cikti": os.path.join(KOK_CT, "arastirma_cikti", "canli"), "onkayit": os.path.join(KOK_CT, "arastirma_cikti", "canli", "CANLI_ON_KAYIT.md"),
          "sonuc": os.path.join(KOK_CT, "arastirma_cikti", "canli", "CANLI_SONUC.md")}
CT_DOSYA = {"md": "CANLI_TARAMA_{e}.md", "json": "CANLI_TARAMA_{e}.json", "pdf": "CANLI_TARAMA_{e}.pdf", "model": "puan7_model.pkl",
            "ozet": "guncelleme_ozet.json"}

# ================================================================ KURALLAR (ön kayıtta mühürlü; sonuç görüldükten sonra DEĞİŞMEZ)
CT_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "pazar": ["ABD", "AVR", "BIST"],
    "para": {"ABD": "USD", "AVR": "EUR", "BIST": "TL"},
    "veri": {"yahoo_ek": {"ABD": "", "AVR": "", "BIST": ".IS"}, "indir_gun": 400, "paket": 100, "fark_esik": 0.01, "supheli_getiri": 0.40,
             "olcek_azami": 0.40, "oran_yayilim_azami": 1.40, "kapanis_utc": {"BIST": "15:30", "AVR": "16:45", "ABD": "21:15"},
             "tanim": "yfinance auto_adjust=True, son 400 takvim günü, 100'lük paket, threads; başarısızlar ikinci turda 20'lik pakette bir kez "
                      "daha. Birleştirme: eski seri korunur, yeni barlar eklenir; ortak günlerde Close farkı > %1 olan gün sayısı uyarıdır ve ortak "
                      "günlerde yeni veri esastır; ortak günlerin medyan oranı (yeni / eski) 1'den > %1 farklıysa (temettü / ayarlama kipi) eski "
                      "kısmın O/H/L/C'si bu oranla ölçeklenir (tek fiyat kipi, K6); oran 1'den > %40 farklıysa (bölünme / birim: peni-sterlin) "
                      "sembol ŞÜPHELİ; ortak günlerin gün oranlarında en büyük / en küçük > 1,40 ise (ayarlama ya da birim ortak pencerenin bir kısmında farklı: BIST bedelsiz, Londra peni-sterlin) sembol ŞÜPHELİ (SAPMA 1, 20 Kas: ön kayıttan sonra, liste görülmeden eklendi). Yeni barlarda |günlük getiri| > %40 -> ŞÜPHELİ (listeden dışlanır). AVR yeni barlarda Kur = son bilinen "
                      "Kur (ileri taşınır; yalnız likidite ölçüsü). Seans kapanmadan (pazar kapanış UTC saati + pay) gelen bugünkü bar atılır."},
    "sinyal": {"son_bar": 5, "tekil_gun": 60, "likidite_gun": 20, "likidite_min": 10, "likidite_alt": 0.20, "mom_gun": 60, "bolunme_geri": 61,
               "tanim": "S6 AL (YAPI_HEDEF.yh_s6_hisse X1 = Y1) günü t; havuz t günündeki bilgiyle (OC 'gecmis' kipinin t+1 girişli hali): "
                        "t'de geçerli bar, momentum C(t)/C(t-60) sonlu (kapanış en çok 5 gün ileri taşınır), likidite = C*V*Kur'un t dahil "
                        "son 20 birleşik takvim günü medyanı (en az 10), aynı gün geçerli barı olan pazar hisseleri arasında alt %20 değil, "
                        "[t-60, t] içinde bölünme şüphesi (OC.oc_bolunme_supheli) yok; aynı hissede havuzdan geçen AL günleri birleşik "
                        "takvimde >= 60 gün arayla tekil (ilk tutulur). Liste: pazarın birleşik takviminin son 5 günündeki tekil AL günleri."},
    "havuz": {"kademe": ["S1_S7", "S1_F22", "S1"],
              "tanim": "Ş1 = F15 <= 0,25 VE F17 <= -0,20; Ş7 = F22 > 0 VE F22a < 0 (O_t < F21) VE F23 >= 0,50 (YAPI_HEDEF.yh_s7_sartlar, "
                       "YH_ESIK Y10 eşikleri). Kademe 0: Ş1 VE Ş7. Bütün pazarlarda havuz boşsa kademe (i): Ş1 VE F22 > 0; o da boşsa (ii): "
                       "Ş1. Kademe atlanmaz; raporda yazılır."},
    "sira": {"en_iyi": 10, "pazar_azami": 5,
             "tanim": "puan7 azalan; eşitlikte Ş9 (U dip) var önce; sonra F18 küçük (yol almamış). Pazar karışık, pazar başına en çok 5."},
    "olcu": {"hedef": [0.05, 0.10], "stop_carp": 0.98, "ufuk": 15,
             "tanim": "stop0 = hat x 0,98; hedef fiyatları kapanışa göre (giriş = sonraki açılış varsayımı; gerçek ölçüm giriş açılışıyla); "
                      "ileri test yh_olay_olc (YAPI_HEDEF 15 bar cetveli; eş aynı gün aynı OC kovası, en az 3); ölçüm tarihi = sinyal + 15 "
                      "işlem günü (giriş t+1, 15. geçerli bar t+15)"},
    "model": {"ad": "M2 birleşik (YH_ESIK7['M2'] ayarları aynen)", "egitim_sinir": "2026-08-31", "hedef": "h5",
              "tanim": "eğitim = YH.yh_veri7() satırlarından ölçülen (h5 ve es_h5 var) VE giriş <= 2026-08-31 olanlar; özellikler _YH_OZ7 "
                       "(F1-F29, F22a dahil) + NaN bayrakları (YH_ESIK7['nan_bayrak']); NaN -> eğitim medyanı; puan7 = P(h5 = 1)"},
    "kriz": "canlı taramada 31.08.2026 kesiği bellekte geçici olarak kaldırılır (SY_ESIK / OC_ESIK / YH_ESIK 'kriz' -> 2100-01-01); dosyalar "
            "değişmez; fonksiyon çıkışında eski değer geri yazılır",
}

CT_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "liste ölçüm değildir; ileri test (olc) eşi YAPI_HEDEF yh_olay_olc ile aynı giriş günü, aynı OC momentum x likidite kovası, "
                   "aynı d / hedef / takip / 15 bar; tek tek okunur, n < 30 iken 'örneklem yetersiz'"),
    "K2": ("EVET", "S6 nedensel (yh_s6_hisse); özellikler yalnız [.., t] (önceki turların prefix denetimleri: F1-F29, F65-F68, mahkeme prefix "
                   "kapısı); havuz t günündeki bilgiyle; model eğitimi giriş <= 31.08.2026 satırlarıyla, canlı sinyaller Ekim 2026 ve sonrası; "
                   "test_canli_tarama prefix testi"),
    "K3": ("EVET", "OC.oc_veri_hazirla / YH._yh_hazir geçerli bar (H > L, V > 0, O/H/L/C > 0); seans kapanmadan gelen bugünkü bar atılır"),
    "K4": ("EVET", "aynı hissede 60 birleşik takvim günü tekil (havuzdan geçen AL günleri); olc oc_olay_hazirla tekilleştirmesiyle"),
    "K5": ("EVET", "liste hedefleri kapanışa göre (bilgi); ileri test girişi t+1 AÇILIŞI (yh_olay_olc E0 = Op[d])"),
    "K6": ("EVET", "tek fiyat kipi: yfinance auto_adjust=True; ortak günlerde oran tek tipse eski kısım yeni kipe ölçeklenir; oran > %40 "
                   "(bölünme / peni-sterlin) ve yeni barda |getiri| > %40 ŞÜPHELİ, listeden dışlanır; AVR likidite EUR (Kur)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (V_*.pkl); batan yok; rapor ve ileri test sonucu yukarı yanlı okunur (her çıktıda yazılı)"),
    "K8": ("EVET", "liste 10 isim: bulgu değil; ileri test sonuçları birikimli, n < 30 'örneklem yetersiz', olaylar tek tek listelenir"),
    "K9": ("EVET", "kurallar iş tanımında (commit 39a8d2f) ve CT_ESIK sha256'sı bu ön kayıtta, ilk taramadan önce commit; tara komutu ESIK "
                   "sha'sını ve kontrol kapısını (IZ_KARNE.ik_kontrol_kapisi) denetler, tutmazsa DURUR"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV (yfinance) ve mühürlü özellik / olay dosyaları"),
    "K11": ("EVET", "json'da her adayın bütün sayıları; test_canli_tarama olc hesabını YAPI_HEDEF cetveliyle (yh_sim elle) yeniden üretir; "
                    "puan7 matrisi YH._yh_matris7 ile eşit"),
    "K12": ("EVET", "çıktıların başında dürüstlük cümlesi (izleme, öneri değil); 'iz / emare' sözü yok; sayı ve yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_ct; yasak defter dosyalarına, YAPI_HEDEF / GOZ_ETIKET / üretim zincirine dokunulmaz "
                    "(yalnız import); e-posta / anahtar taraması (_ct_yaz); veri repoya girmez; push yok; kod değişti -> Colab'da çalışma "
                    "zamanını yeniden başlat"),
    "K14": ("EVET", "öneri değil; boyut / giriş / çıkış kuralı yazılmaz; gerçek para kararı için öneri modülü üç kapısı (dosya + risk) "
                    "ayrıca gerekir; taban oran (3 yılda 10x ~%1) her çıktıda dürüstlük cümlesiyle"),
}


CT_SAPMA: List[str] = [
    "SAPMA 1 (20 Kas 2026, ilk ön kayıt 03b9658'den sonra; Ekim listesi bu kuraldan etkilenmez, güncellemesiz koştu): ilk yfinance güncellemesinin "
    "ÖZETİ (liste değil) görülünce veri denetimi eklendi: ortak günlerin gün oranlarında en büyük / en küçük > 1,40 -> ŞÜPHELİ. Neden: BIST 19, "
    "AVR 4 (Londra peni-sterlin), ABD 1 sembolde Yahoo'nun ayarlaması ortak pencerenin yalnız bir kısmında farklıydı; 'yeni veri esas' kuralı bu "
    "sembollerde seriye sahte sıçrama sokuyordu (K6). Seçim / sıralama / havuz kuralı değişmedi.",
]


class CTHata(RuntimeError):
    """Durdurucu hata: veri yok, ön kayıt / eşik sha'sı tutmuyor, model eğitilemedi, girdi bozuk."""


# ================================================================ 0) ORTAK
_CT_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_CT_ANAHTAR = re.compile(r"(?i)(api[_-]?key|token|secret|password|şifre)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}")


def _ct_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ct_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(CT_ESIK if E is None else E, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _ct_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _ct_sizinti(metin: str, ad: str) -> None:
    if _CT_EPOSTA.search(metin) or _CT_ANAHTAR.search(metin):
        raise CTHata(f"{ad}: e-posta / anahtar benzeri metin var -> yazılmadı")


def _ct_yaz(yol: str, metin: str, ad: str) -> None:
    _ct_sizinti(metin, ad)
    os.makedirs(os.path.dirname(yol) or ".", exist_ok=True)
    tmp = yol + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(metin)
    os.replace(tmp, yol)


def _ct_json(o: Any) -> Any:
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(float(o)) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, _dt.date)):
        return str(pd.Timestamp(o).date())
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def _ct_temiz(x: Any) -> Any:
    """json için NaN -> None (iç içe)."""
    if isinstance(x, dict):
        return {k: _ct_temiz(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_ct_temiz(v) for v in x]
    if isinstance(x, (float, np.floating)):
        return None if not np.isfinite(float(x)) else float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, pd.Timestamp):
        return str(x.date())
    return x


def _f(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    return f"{v:,.{n}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def _y(x: Any, n: int = 1) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(v) else f"%{v * 100:+.{n}f}".replace(".", ",")


@contextlib.contextmanager
def ct_kriz_ac():
    """31.08.2026 fon krizi kesiğini YALNIZ canlı tarama süresince bellekte kaldırır (dosyalar değişmez); çıkışta eski değerler geri yazılır."""
    hedef = [(SY.SY_ESIK, "kriz"), (OC.OC_ESIK, "kriz"), (YH.YH_ESIK, "kriz")]
    eski = [(d, k, d.get(k)) for d, k in hedef]
    try:
        for d, k in hedef:
            d[k] = "2100-01-01"
        yield
    finally:
        for d, k, v in eski:
            d[k] = v


def _ct_pkl_oku(yol: str) -> Dict[str, pd.DataFrame]:
    if not os.path.exists(yol):
        raise CTHata(f"veri yok: {yol} (git worktree add /tmp/iv origin/islenmis-veri; python FON_IZI.py vpac /tmp/iv/veri /tmp/veri)")
    V = pd.read_pickle(yol)
    if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
        V = V["veri"]
    if not isinstance(V, dict):
        raise CTHata(f"{yol}: sözlük değil")
    return {str(k): v for k, v in V.items()}


def ct_kaynak(pazar: str, veri: Optional[str] = None) -> str:
    """Taramanın okuyacağı klasör: verilen > /tmp/veri_canli (varsa) > /tmp/veri."""
    if veri:
        return veri
    c = CT_YOL["canli"]
    return c if os.path.exists(os.path.join(c, f"V_{pazar}.pkl")) else CT_YOL["veri"]


# ================================================================ 1) VERİ GÜNCELLEME
def ct_yarim_bar_sinir(pazar: str, simdi: Optional[pd.Timestamp] = None, E: Dict[str, Any] = CT_ESIK) -> pd.Timestamp:
    """Kabul edilen en geç bar tarihi: pazar bugün kapandıysa bugün, değilse dün (UTC)."""
    simdi = pd.Timestamp(simdi) if simdi is not None else pd.Timestamp.now(tz="UTC").tz_localize(None)
    sa, dk = (int(x) for x in E["veri"]["kapanis_utc"][pazar].split(":"))
    bugun = simdi.normalize()
    kapandi = simdi >= bugun + pd.Timedelta(hours=sa, minutes=dk)
    return bugun if kapandi else bugun - pd.Timedelta(days=1)


def ct_indir(kodlar: List[str], bas: pd.Timestamp, paket: int = 100) -> Tuple[Dict[str, pd.DataFrame], List[str]]:
    """yfinance (auto_adjust=True) paket paket; başarısızlar 20'lik pakette bir kez daha. Döner ({kod: OHLCV}, başarısız kodlar)."""
    import yfinance as yf
    out: Dict[str, pd.DataFrame] = {}

    def tur(liste: List[str], boy: int) -> List[str]:
        kalan = []
        for i in range(0, len(liste), boy):
            pk = liste[i:i + boy]
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    D = yf.download(pk, start=str(bas.date()), auto_adjust=True, progress=False, group_by="ticker", threads=True)
            except Exception as ex:  # paket düşerse öteki paketler sürer; kodlar ikinci tura kalır
                ctlog.warning("yfinance paket %d düştü: %s", i, ex); kalan += pk; continue
            for k in pk:
                try:
                    d = D[k] if isinstance(D.columns, pd.MultiIndex) else D
                    d = d[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"]).astype(float)
                    ix = pd.DatetimeIndex(d.index)
                    d.index = (ix.tz_convert(None) if ix.tz is not None else ix).normalize()
                    d = d[~d.index.duplicated(keep="last")].sort_index()
                    if len(d):
                        out[k] = d
                    else:
                        kalan.append(k)
                except Exception:  # sembol pakette yok / boş
                    kalan.append(k)
            ctlog.info("yfinance %d/%d (başarılı %d)", min(i + boy, len(liste)), len(liste), len(out))
        return kalan
    k1 = tur(list(kodlar), paket)
    k2 = tur(k1, 20) if k1 else []
    return out, k2


def ct_birlestir(eski: pd.DataFrame, yeni: pd.DataFrame, sinir: pd.Timestamp, E: Dict[str, Any] = CT_ESIK) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Eski + yeni seri. Döner (birleşik, bilgi: yeni_bar, fark_gun, oran, olcek, supheli, neden)."""
    V = E["veri"]
    eski = eski.copy()
    ix = pd.DatetimeIndex(eski.index)
    eski.index = (ix.tz_convert(None) if ix.tz is not None else ix).normalize()
    eski = eski[~eski.index.duplicated(keep="last")].sort_index()
    yeni = yeni[yeni.index <= pd.Timestamp(sinir)].copy()
    kur_var = "Kur" in eski.columns
    bilgi: Dict[str, Any] = {"yeni_bar": 0, "fark_gun": 0, "oran": 1.0, "olcek": False, "supheli": False, "neden": ""}
    if not len(yeni):
        return eski, bilgi
    ortak = eski.index.intersection(yeni.index)
    if len(ortak):
        with np.errstate(all="ignore"):
            r = yeni.Close.reindex(ortak).to_numpy(float) / eski.Close.reindex(ortak).to_numpy(float)
        r = r[np.isfinite(r) & (r > 0)]
        if len(r):
            med = float(np.median(r)); bilgi["oran"] = med
            bilgi["fark_gun"] = int(np.sum(np.abs(r - 1) > V["fark_esik"]))
            if abs(med - 1) > V["olcek_azami"]:
                bilgi["supheli"] = True; bilgi["neden"] = f"ortak günlerde yeni/eski oranı {med:.3f} (bölünme / birim)"
            elif float(np.max(r)) / float(np.min(r)) > V["oran_yayilim_azami"]:
                bilgi["supheli"] = True
                bilgi["neden"] = f"ortak günlerde oran tek tip değil ({float(np.min(r)):.3f} .. {float(np.max(r)):.3f}; ayarlama / birim karışık)"
            elif abs(med - 1) > V["fark_esik"]:
                bilgi["olcek"] = True
                for c in ("Open", "High", "Low", "Close"):
                    eski[c] = eski[c].astype(float) * med
        bas = ortak.min()
    else:
        bas = eski.index.max() + pd.Timedelta(days=1)
    yeni_k = yeni[yeni.index >= bas][["Open", "High", "Low", "Close", "Volume"]].astype(float)
    if kur_var:
        yeni_k["Kur"] = eski["Kur"].reindex(yeni_k.index)
        yeni_k["Kur"] = yeni_k["Kur"].fillna(float(eski["Kur"].dropna().iloc[-1]) if eski["Kur"].notna().any() else 1.0)
    son_eski = eski.index.max()
    bilgi["yeni_bar"] = int((yeni_k.index > son_eski).sum())
    B = pd.concat([eski[eski.index < bas], yeni_k]).sort_index()
    B = B[~B.index.duplicated(keep="last")]
    # yeni barlarda |günlük getiri| > %40 (eski son kapanıştan itibaren)
    C = B.Close.to_numpy(float); ii = np.flatnonzero(B.index > son_eski)
    if len(ii):
        with np.errstate(all="ignore"):
            g = np.abs(C[ii] / C[ii - 1] - 1) if ii[0] >= 1 else np.abs(C[ii[1:]] / C[ii[1:] - 1] - 1)
        g = g[np.isfinite(g)]
        if len(g) and float(np.max(g)) > V["supheli_getiri"]:
            bilgi["supheli"] = True
            bilgi["neden"] = (bilgi["neden"] + "; " if bilgi["neden"] else "") + f"yeni barda günlük getiri %{float(np.max(g)) * 100:.0f}"
    return B, bilgi


def ct_guncelle(veri: Optional[str] = None, canli: Optional[str] = None, pazarlar: Optional[List[str]] = None,
                simdi: Optional[pd.Timestamp] = None, E: Dict[str, Any] = CT_ESIK) -> Dict[str, Any]:
    """V_*.pkl (taban: canlı klasörde varsa o, yoksa /tmp/veri) + yfinance -> canli/V_*.pkl. Özet döner ve canli/guncelleme_ozet.json yazılır."""
    canli = canli or CT_YOL["canli"]; os.makedirs(canli, exist_ok=True)
    ozet: Dict[str, Any] = {"zaman_utc": _ct_simdi(), "pazar": {}, "supheli": []}
    for p in pazarlar or E["pazar"]:
        taban = veri or (canli if os.path.exists(os.path.join(canli, f"V_{p}.pkl")) else CT_YOL["veri"])
        V = _ct_pkl_oku(os.path.join(taban, f"V_{p}.pkl"))
        ek = E["veri"]["yahoo_ek"][p]; sinir = ct_yarim_bar_sinir(p, simdi, E)
        bas = pd.Timestamp(simdi or pd.Timestamp.now()).normalize() - pd.Timedelta(days=int(E["veri"]["indir_gun"]))
        kod = {s + ek: s for s in V}
        t0 = time.time()
        Y, bas_siz = ct_indir(sorted(kod), bas, int(E["veri"]["paket"]))
        out: Dict[str, pd.DataFrame] = {}; ps = {"istenen": len(kod), "basarili": 0, "basarisiz": [], "yeni_bar": 0, "fark_sembol": 0,
                                                 "olcek_sembol": 0, "supheli": 0, "taban": taban, "yarim_bar_siniri": str(sinir.date())}
        for k, s in kod.items():
            if k not in Y:
                out[s] = V[s]; ps["basarisiz"].append(s); continue
            try:
                B, b = ct_birlestir(V[s], Y[k], sinir, E)
            except Exception as ex:  # tek sembol bozuksa eski seri kalır, başarısız sayılır
                ctlog.warning("%s %s birleştirilemedi: %s", p, s, ex); out[s] = V[s]; ps["basarisiz"].append(s); continue
            out[s] = B; ps["basarili"] += 1; ps["yeni_bar"] += b["yeni_bar"]
            ps["fark_sembol"] += int(b["fark_gun"] > 0); ps["olcek_sembol"] += int(b["olcek"])
            if b["supheli"]:
                ps["supheli"] += 1; ozet["supheli"].append({"pazar": p, "sembol": s, "neden": b["neden"]})
        son = pd.Series({s: d.index.max() for s, d in out.items() if len(d)})
        ps["son_tarih"] = str(son.max().date()) if len(son) else None
        ps["son_tarih_mod"] = str(son.mode().iloc[0].date()) if len(son) else None
        ps["sure_sn"] = round(time.time() - t0, 1)
        pd.to_pickle(out, os.path.join(canli, f"V_{p}.pkl"))
        ps["basarisiz_n"] = len(ps["basarisiz"]); ps["basarisiz"] = sorted(ps["basarisiz"])[:200]
        ozet["pazar"][p] = ps
        ctlog.info("%s: %d/%d başarılı, son tarih %s, şüpheli %d (%.0f sn)", p, ps["basarili"], ps["istenen"], ps["son_tarih"], ps["supheli"],
                   ps["sure_sn"])
    _ct_yaz(os.path.join(canli, CT_DOSYA["ozet"]), json.dumps(ozet, ensure_ascii=False, indent=1, default=_ct_json), "güncelleme özeti")
    return ozet


# ================================================================ 2) SİNYAL (S6 + havuz t bilgisiyle + tekil)
_CT_IS_V: Dict[str, pd.DataFrame] = {}


def _ct_s6_isci(semboller: List[str]) -> List[pd.DataFrame]:
    out = []
    with ct_kriz_ac():
        for s in semboller:
            try:
                X1, _ = YH.yh_s6_hisse(_CT_IS_V[s])
                if len(X1):
                    X1 = X1.copy(); X1.insert(0, "sembol", s); out.append(X1)
            except Exception as ex:  # tek hisse bozuksa öteki hisseler sürer
                ctlog.warning("S6 %s atlandı: %s", s, ex)
    return out


def ct_s6_hepsi(V: Dict[str, pd.DataFrame], islem: int = 1) -> pd.DataFrame:
    """Bütün hisselerde bütün S6 AL günleri (Y1; tekilleştirmesiz)."""
    global _CT_IS_V
    S = sorted(V); parca = [S[i::max(1, islem * 4)] for i in range(max(1, islem * 4))]
    _CT_IS_V = V
    try:
        if islem > 1:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(islem) as hv:
                R = hv.map(_ct_s6_isci, [p for p in parca if p])
        else:
            R = [_ct_s6_isci(p) for p in parca if p]
    finally:
        _CT_IS_V = {}
    L = [x for r in R for x in r]
    return pd.concat(L, ignore_index=True) if L else pd.DataFrame(columns=["sembol"] + YH._SIG_KOL)


def ct_havuz_tablo(V: Dict[str, pd.DataFrame], E: Dict[str, Any] = CT_ESIK) -> Dict[str, Any]:
    """Birleşik takvim x hisse: t günündeki havuz üyeliği (OC 'gecmis' kipinin t+1 girişli hali; yalnız t ve öncesi)."""
    Sg = E["sinyal"]; S = sorted(V)
    idx = pd.DatetimeIndex(sorted(set().union(*[V[s].index for s in S])))
    C = pd.DataFrame({s: V[s].Close for s in S}).reindex(idx)
    Tl = pd.DataFrame({s: V[s].Close * V[s].Volume * (V[s]["Kur"] if "Kur" in V[s] else 1.0) for s in S}).reindex(idx)
    gec = C.notna().to_numpy()
    Lq = Tl.rolling(int(Sg["likidite_gun"]), min_periods=int(Sg["likidite_min"])).median().to_numpy()
    Cf = C.ffill(limit=5)
    M = (Cf / Cf.shift(int(Sg["mom_gun"])) - 1).to_numpy()
    q = pd.DataFrame(np.where(gec & np.isfinite(Lq), Lq, np.nan)).quantile(float(Sg["likidite_alt"]), axis=1).to_numpy()
    with np.errstate(invalid="ignore"):
        lik_alt = Lq < q[:, None]
    sup = np.zeros(C.shape, bool)
    for j, s in enumerate(S):
        sj = OC.oc_bolunme_supheli(V[s].Close.to_numpy(float), OC.OC_ESIK)
        if sj.any():
            sup[idx.get_indexer(V[s].index[sj]), j] = True
    g = int(Sg["bolunme_geri"])
    sup_g = pd.DataFrame(sup.astype(int)).rolling(g, min_periods=1).max().to_numpy().astype(bool)   # [t-60, t]
    ok = gec & np.isfinite(M) & np.isfinite(Lq) & ~lik_alt & ~sup_g
    return {"tarih": idx, "sembol": S, "kol": {s: i for i, s in enumerate(S)}, "ok": ok, "lik_alt": lik_alt, "sup": sup_g, "Lq": Lq, "M": M,
            "gec": gec}


def ct_sinyal_sec(A: pd.DataFrame, H: Dict[str, Any], E: Dict[str, Any] = CT_ESIK) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Bütün AL günleri -> havuz (t) -> 60 gün tekil -> son 5 gün. Döner (sinyaller, sayım)."""
    Sg = E["sinyal"]; idx = H["tarih"]; n = int(Sg["son_bar"])
    son5 = idx[-n:] if len(idx) >= n else idx
    say = {"al_son5": 0, "havuz_disi": 0, "likidite_alt20": 0, "bolunme": 0, "tekil": 0, "sinyal": 0}
    if not len(A):
        return A.assign(d=[]), say
    A = A.copy(); A["tarih"] = pd.to_datetime(A.tarih)
    A["d"] = idx.get_indexer(A.tarih); A["j"] = A.sembol.map(H["kol"]).astype(int)
    if (A.d < 0).any():
        raise CTHata("S6 günü birleşik takvimde yok")
    say["al_son5"] = int(A.tarih.isin(son5).sum())
    okm = H["ok"][A.d.to_numpy(), A.j.to_numpy()]
    s5 = A.tarih.isin(son5).to_numpy()
    say["havuz_disi"] = int((s5 & ~okm).sum())
    say["likidite_alt20"] = int((s5 & H["lik_alt"][A.d.to_numpy(), A.j.to_numpy()]).sum())
    say["bolunme"] = int((s5 & H["sup"][A.d.to_numpy(), A.j.to_numpy()]).sum())
    A = A[okm].sort_values(["sembol", "d"], kind="mergesort").reset_index(drop=True)
    tut = np.zeros(len(A), bool); son: Dict[str, int] = {}
    for i, (s, d) in enumerate(zip(A.sembol.to_numpy(), A.d.to_numpy())):
        if s not in son or d - son[s] >= int(Sg["tekil_gun"]):
            tut[i] = True; son[s] = int(d)
    say["tekil"] = int((~tut & A.tarih.isin(son5).to_numpy()).sum())
    A = A[tut & A.tarih.isin(son5).to_numpy()].reset_index(drop=True)
    say["sinyal"] = int(len(A))
    return A, say


# ================================================================ 3) ÖZELLİK + MAHKEME
def ct_ozellik_hisse(df: pd.DataFrame, tarihler: List[pd.Timestamp]) -> pd.DataFrame:
    """Bir hissenin sinyal günleri için F1-F29 (+F22a), F65-F68 / S10, mahkeme (12 kural puanı, karar). Kriz kesiği açık ortamda çağrılır."""
    d = YH._yh_hazir(df)
    Fs, Bs = GE.ge_ozellik_hisse(d, tarihler, hazir=True)
    P11 = GE.ge_parmak_hisse(d, tarihler, hazir=True, E=GE.ge_parmak_surum("P1.1")["esik"])
    S7 = YH.yh_s7_ozellik(d, tarihler, hazir=True); S9 = YH.yh_s9_ozellik(d, tarihler, hazir=True)
    S10 = YH.yh_s10_ozellik(d, tarihler, hazir=True)
    sat = []
    for k, t in enumerate(tarihler):
        r = {"tarih": pd.Timestamp(t), **Fs[k], "F19": P11[k]["F19"], "hat": Bs[k]["hat"], "tavan_s6": Bs[k]["tavan"], "durum": Bs[k]["durum"],
             "sol": Bs[k]["sol"]}
        r.update(S7.iloc[k].to_dict()); r.update(S9.iloc[k].to_dict())
        r.update({c: S10.iloc[k][c] for c in ("F65", "F66", "F67", "F68", "S10")})
        try:
            M = YH.yh_mahkeme_hisse(d, pd.Timestamp(t))
            r.update({"kural12": int(M["secilen"]["puan"]), "mahkeme_onceki": bool(M["onceki_daha_uygun"]), "mahkeme": M["karar"],
                      "mahkeme_eksik": ",".join(M["eksik"])})
        except Exception as ex:  # mahkeme bilgi; düşerse aday kalır, neden yazılır
            r.update({"kural12": np.nan, "mahkeme_onceki": False, "mahkeme": f"mahkeme çalışmadı: {str(ex)[:120]}", "mahkeme_eksik": ""})
        i = int(d.index.get_loc(pd.Timestamp(t)))
        r["kapanis"] = float(d.Close.iloc[i]); r["acilis"] = float(d.Open.iloc[i])
        w = d.iloc[max(0, i - 19):i + 1]
        r["likidite20"] = float(np.mean(w.Close * w.Volume * (w["Kur"] if "Kur" in w else 1.0)))
        r["veri_son"] = d.index[-1]
        sat.append(r)
    return pd.DataFrame(sat)


def _ct_oz_isci(is_: List[Tuple[str, List[pd.Timestamp]]]) -> List[Dict[str, Any]]:
    out = []
    with ct_kriz_ac():
        for s, tl in is_:
            try:
                F = ct_ozellik_hisse(_CT_IS_V[s], tl); F.insert(0, "sembol", s)
                out += F.to_dict("records")
            except Exception as ex:  # tek hisse bozuksa öteki adaylar sürer; raporda listelenir
                ctlog.warning("özellik %s atlandı: %s", s, ex)
                out += [{"sembol": s, "tarih": t, "_hata": str(ex)[:200]} for t in tl]
    return out


def ct_ozellik(V: Dict[str, pd.DataFrame], sig: pd.DataFrame, islem: int = 1) -> pd.DataFrame:
    global _CT_IS_V
    if not len(sig):
        return pd.DataFrame()
    G = [(s, list(pd.to_datetime(g.tarih))) for s, g in sig.groupby("sembol")]
    _CT_IS_V = V
    try:
        if islem > 1 and len(G) > 8:
            import multiprocessing as mp
            parca = [G[i::islem * 2] for i in range(islem * 2)]
            with mp.get_context("fork").Pool(islem) as hv:
                R = hv.map(_ct_oz_isci, [p for p in parca if p])
        else:
            R = [_ct_oz_isci(G)]
    finally:
        _CT_IS_V = {}
    return pd.DataFrame([x for r in R for x in r])


# ================================================================ 4) PUAN7 MODELİ
def _ct_matris(D: pd.DataFrame, med: pd.Series, E7: Dict[str, Any] = YH.YH_ESIK7) -> np.ndarray:
    """YH._yh_matris7 ile aynı: özellikler (eğitim medyanıyla doldurulmuş) + NaN bayrakları."""
    oz = E7["ozellik"]
    X = D[oz].astype(float)
    B = np.column_stack([D[c].isna().to_numpy(float) for c in E7["nan_bayrak"]]) if E7["nan_bayrak"] else np.zeros((len(D), 0))
    return np.column_stack([X.fillna(med).to_numpy(float), B])


def ct_model(yol: Optional[str] = None, yeniden: bool = False, E: Dict[str, Any] = CT_ESIK) -> Dict[str, Any]:
    """puan7 modeli: yol varsa ve meta tutarsa yüklenir; yoksa YH_ESIK7 M2 ayarlarıyla bir kez eğitilir ve saklanır."""
    yol = yol or os.path.join(CT_YOL["canli"], CT_DOSYA["model"])
    E7 = YH.YH_ESIK7; esik7 = YH.yh_esik7_sha(); g6 = os.path.join(YH.YH_YOL["cikti"], YH.YH_DOSYA["olay_g6"])
    g6_sha = _ct_sha_dosya(g6) if os.path.exists(g6) else ""
    skl = YH._yh_sklearn_surum()
    if os.path.exists(yol) and not yeniden:
        try:
            with open(yol, "rb") as f:
                Mm = pickle.load(f)
            if Mm.get("esik7_sha") == esik7 and Mm.get("olay_g6_sha") == g6_sha and Mm.get("sklearn") == skl \
                    and Mm.get("egitim_sinir") == E["model"]["egitim_sinir"]:
                return Mm
            ctlog.info("puan7 modeli meta tutmadı (eşik / veri / sklearn); yeniden eğitiliyor")
        except Exception as ex:  # bozuk dosya: yeniden eğit
            ctlog.warning("puan7 modeli okunamadı (%s); yeniden eğitiliyor", ex)
    D = YH.yh_veri7()
    tr = D.olcu.to_numpy() & (D.giris <= pd.Timestamp(E["model"]["egitim_sinir"])).to_numpy()
    Dtr = D[tr]
    med = Dtr[E7["ozellik"]].median().fillna(0.0)
    X = _ct_matris(Dtr, med, E7); y = (Dtr.h5.to_numpy(float) > 0.5).astype(int)
    if len(np.unique(y)) < 2:
        raise CTHata("puan7: eğitim hedefinde tek sınıf -> DURDU")
    M = YH.yh_model7("M2", E7); M.fit(X, y)
    Mm = {"model": M, "med": med, "ad": list(E7["ozellik"]) + [f"nan_{c}" for c in E7["nan_bayrak"]], "n": int(len(Dtr)), "pozitif": float(y.mean()),
          "esik7_sha": esik7, "olay_g6_sha": g6_sha, "sklearn": skl, "egitim_sinir": E["model"]["egitim_sinir"], "giris_max": str(Dtr.giris.max().date()),
          "n_iter": int(M.n_iter_), "zaman_utc": _ct_simdi()}
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "wb") as f:
        pickle.dump(Mm, f)
    ctlog.info("puan7 modeli eğitildi: n %d, P(h5) %.3f, iter %d -> %s", Mm["n"], Mm["pozitif"], Mm["n_iter"], yol)
    return Mm


def ct_puan(F: pd.DataFrame, Mm: Dict[str, Any]) -> np.ndarray:
    if not len(F):
        return np.zeros(0)
    eksik = [c for c in YH.YH_ESIK7["ozellik"] if c not in F.columns]
    if eksik:
        raise CTHata(f"puan7: özellik eksik {eksik}")
    return Mm["model"].predict_proba(_ct_matris(F, Mm["med"]))[:, 1]


# ================================================================ 5) HAVUZ + SIRA
def ct_havuz_sec(F: pd.DataFrame, E: Dict[str, Any] = CT_ESIK) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Kademeli havuz (bütün pazarlar birlikte): Ş1 VE Ş7 -> boşsa Ş1 VE F22 > 0 -> boşsa Ş1. Döner (havuz, bilgi)."""
    if not len(F):
        return F, {"kademe": None, "sayi": {"S1_S7": 0, "S1_F22": 0, "S1": 0}}
    S = YH.yh_s7_sartlar(F)
    T = YH.YH_ESIK["denemeler"]["Y10"]["esik"]
    with np.errstate(invalid="ignore"):
        f22 = F["F22"].to_numpy(float) > float(T["F22_alt_acik"])
    m = {"S1_S7": S["S1"] & S["S7"], "S1_F22": S["S1"] & f22, "S1": S["S1"].copy()}
    say = {k: int(v.sum()) for k, v in m.items()}
    say_p = {k: {p: int((v & (F.pazar == p).to_numpy()).sum()) for p in E["pazar"]} for k, v in m.items()}
    for k in E["havuz"]["kademe"]:
        if m[k].any():
            H = F[m[k]].copy(); H["kademe"] = k
            return H.reset_index(drop=True), {"kademe": k, "sayi": say, "sayi_pazar": say_p}
    return F.iloc[0:0].assign(kademe=[]), {"kademe": None, "sayi": say, "sayi_pazar": say_p}


def ct_sirala(H: pd.DataFrame, E: Dict[str, Any] = CT_ESIK) -> pd.DataFrame:
    """puan7 azalan; eşitlikte Ş9 var önce; sonra F18 küçük. En iyi 10, pazar başına en çok 5."""
    if not len(H):
        return H
    H = H.copy(); H["_s9"] = -H["S9"].astype(float).fillna(0.0); H["_p"] = -H["puan7"].astype(float)
    H = H.sort_values(["_p", "_s9", "F18", "pazar", "sembol"], kind="mergesort").reset_index(drop=True)
    sec, sp = [], {}
    for i, r in H.iterrows():
        if sp.get(r.pazar, 0) >= int(E["sira"]["pazar_azami"]):
            continue
        sec.append(i); sp[r.pazar] = sp.get(r.pazar, 0) + 1
        if len(sec) >= int(E["sira"]["en_iyi"]):
            break
    L = H.loc[sec].drop(columns=["_s9", "_p"]).reset_index(drop=True)
    L.insert(0, "sira", np.arange(1, len(L) + 1))
    return L


def ct_aday_alanlari(L: pd.DataFrame, E: Dict[str, Any] = CT_ESIK) -> pd.DataFrame:
    """stop0, % uzaklık, hedef fiyatları, ölçüm tarihi."""
    if not len(L):
        return L
    L = L.copy(); O = E["olcu"]
    L["stop0"] = L.hat * float(O["stop_carp"])
    L["stop_uzak"] = L.stop0 / L.kapanis - 1
    L["hedef5"] = L.kapanis * (1 + O["hedef"][0]); L["hedef10"] = L.kapanis * (1 + O["hedef"][1])
    L["olcum_tarihi"] = [pd.Timestamp(t) + pd.offsets.BDay(int(O["ufuk"])) for t in L.tarih]
    L["para"] = L.pazar.map(E["para"])
    return L


# ================================================================ 6) TARAMA (sürücü)
def ct_onkayit_metni(E: Dict[str, Any] = CT_ESIK) -> str:
    s = ["# CANLI_TARAMA — ön kayıt (kurallar; sonuç görülmeden)", "", CT_DURUSTLUK, "",
         f"- Zaman (UTC): {_ct_simdi()}", f"- Sürüm: {CT_SURUM}", f"- CT_ESIK_SHA: `{ct_esik_sha(E)}`",
         f"- YH_ESIK7_SHA (puan7 ayarları): `{YH.yh_esik7_sha()}`",
         "- İş tanımı: arastirma_cikti/yapi_hedef/CANLI_TARAMA_IS_TANIMI.md (commit 39a8d2f)", "",
         "## Kurallar (CT_ESIK)", ""]
    for k in ("veri", "sinyal", "havuz", "sira", "olcu", "model"):
        s.append(f"- **{k}**: {E[k]['tanim']}")
    s += [f"- **kriz**: {E['kriz']}", "", "## SAPMA kaydı", ""] + [f"- {x}" for x in CT_SAPMA] + ["", "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL)", "",
          "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    ad = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
          "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
          "K13": "süreç", "K14": "boyut (gerçek para)"}
    for k, (y, kn) in CT_KONTROL.items():
        s.append(f"| {k} | {ad[k]} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(s) + "\n"


def ct_onkayit_yaz(uzerine: bool = False) -> str:
    yol = CT_YOL["onkayit"]
    if os.path.exists(yol) and not uzerine:
        raise CTHata(f"ön kayıt zaten var: {yol} (kurallar değişmez; yeni kural = yeni sürüm + yeni ön kayıt)")
    _ct_yaz(yol, ct_onkayit_metni(), "ön kayıt")
    return yol


def ct_kapi(onkayit: Optional[str] = None) -> Dict[str, Any]:
    """Ön kayıt var, CT_ESIK sha'sı tutuyor, kontrol listesi kapısı geçiyor; değilse DURUR."""
    yol = onkayit or CT_YOL["onkayit"]
    if not os.path.exists(yol):
        raise CTHata(f"ön kayıt yok: {yol} (python CANLI_TARAMA.py onkayit) -> DURDU")
    m = re.search(r"CT_ESIK_SHA:\s*`([0-9a-f]{64})`", open(yol, encoding="utf-8").read())
    if not m or m.group(1) != ct_esik_sha():
        raise CTHata("CT_ESIK sha'sı ön kayıtla tutmuyor (kural sonuçtan sonra değişmiş olabilir) -> DURDU")
    try:
        import IZ_KARNE as IK
        k = IK.ik_kontrol_kapisi(yol)
    except ImportError:
        raise CTHata("IZ_KARNE.py bulunamadı (kontrol kapısı) -> DURDU")
    return {"esik_sha": m.group(1), "kontrol": bool(k["gecti"])}


def ct_tara(veri: Optional[str] = None, etiket: Optional[str] = None, cikti: Optional[str] = None, islem: int = 1,
            guncelle: Optional[Dict[str, Any]] = None, model_yol: Optional[str] = None, pdf: bool = True, kapi: bool = True,
            E: Dict[str, Any] = CT_ESIK) -> Dict[str, Any]:
    """Tarama: veri -> S6 son 5 gün -> özellik + puan7 -> havuz (kademe) -> en iyi 10 -> md / json / pdf."""
    t0 = time.time(); cikti = cikti or CT_YOL["cikti"]
    K = ct_kapi() if kapi else {"esik_sha": ct_esik_sha(), "kontrol": None}
    Mm = ct_model(model_yol)
    tum, sayim, veri_bilgi, kaynak = [], {}, {}, {}
    supheli = list((guncelle or {}).get("supheli", []))
    sup_set = {(x["pazar"], x["sembol"]) for x in supheli}
    for p in E["pazar"]:
        kl = ct_kaynak(p, veri); kaynak[p] = kl
        with ct_kriz_ac():
            Vd = OC.oc_veri(p, klasor=kl)
        V = Vd["V"]
        if not guncelle:   # güncelleme yoksa şüpheli denetimi son 5 barda (bilgi; aynı eşik)
            for s, d in V.items():
                c = d.Close.to_numpy(float)[-6:]
                if len(c) >= 2 and np.nanmax(np.abs(c[1:] / c[:-1] - 1)) > E["veri"]["supheli_getiri"]:
                    supheli.append({"pazar": p, "sembol": s, "neden": "son 5 barda |günlük getiri| > %40"}); sup_set.add((p, s))
        H = ct_havuz_tablo(V, E)
        A = ct_s6_hepsi(V, islem)
        sig, say = ct_sinyal_sec(A, H, E)
        ds = sig[[(p, s) in sup_set for s in sig.sembol]] if len(sig) else sig
        say["supheli_dislanan"] = int(len(ds)); sig = sig[[(p, s) not in sup_set for s in sig.sembol]].reset_index(drop=True) if len(sig) else sig
        F = ct_ozellik(V, sig, islem)
        hatali = F[F["_hata"].notna()] if "_hata" in F.columns else F.iloc[0:0]
        if "_hata" in F.columns:
            F = F[F["_hata"].isna()].drop(columns="_hata")
        say["ozellik_hata"] = int(len(hatali))
        say["ozellik_hata_liste"] = [f"{r.sembol} {pd.Timestamp(r.tarih).date()}: {r._hata}" for r in hatali.itertuples()][:20]
        if len(F):
            F.insert(0, "pazar", p)
            F = F.merge(sig[["sembol", "tarih", "n", "ek"]], on=["sembol", "tarih"], how="left")
            tum.append(F)
        idx = H["tarih"]
        veri_bilgi[p] = {"son_tarih": str(idx[-1].date()), "son5": [str(x.date()) for x in idx[-int(E["sinyal"]["son_bar"]):]], "hisse": len(V),
                         "kaynak": kl, "not": Vd.get("not", [])}
        sayim[p] = say
        ctlog.info("%s: hisse %d, son5 AL %d, sinyal %d, özellik %d", p, len(V), say["al_son5"], say["sinyal"], len(F))
    Ft = pd.concat(tum, ignore_index=True) if tum else pd.DataFrame()
    if len(Ft):
        Ft["puan7"] = ct_puan(Ft, Mm)
        Sm = YH.yh_s7_sartlar(Ft); Ft["S1"] = Sm["S1"]; Ft["S7"] = Sm["S7"]
        Ft["S9"] = YH.yh_s9_sartlar(Ft)["S9"]
    Hv, hb = ct_havuz_sec(Ft, E)
    L = ct_aday_alanlari(ct_sirala(Hv, E), E)
    etiket = etiket or max(v["son_tarih"] for v in veri_bilgi.values())
    J = ct_json(etiket, L, Hv, Ft, hb, sayim, veri_bilgi, supheli, guncelle, Mm, K, E)
    J["sure_sn"] = round(time.time() - t0, 1)
    os.makedirs(cikti, exist_ok=True)
    yj = os.path.join(cikti, CT_DOSYA["json"].format(e=etiket)); ym = os.path.join(cikti, CT_DOSYA["md"].format(e=etiket))
    _ct_yaz(yj, json.dumps(_ct_temiz(J), ensure_ascii=False, indent=1, default=_ct_json), "tarama json")
    _ct_yaz(ym, ct_md(J), "tarama md")
    out = {"json": yj, "md": ym, "J": J, "L": L, "F": Ft}
    if pdf:
        yp = os.path.join(cikti, CT_DOSYA["pdf"].format(e=etiket))
        with ct_kriz_ac():
            ct_pdf(J, L, yp, veri)
        out["pdf"] = yp
    return out


_CT_ADAY_KOL = ["sira", "pazar", "sembol", "tarih", "durum", "kapanis", "acilis", "hat", "F21", "stop0", "stop_uzak", "hedef5", "hedef10", "puan7",
                "S9", "S10", "F19", "F15", "F17", "F18", "F22", "F23", "kural12", "mahkeme_onceki", "mahkeme", "mahkeme_eksik", "likidite20", "para",
                "kademe", "olcum_tarihi", "veri_son", "n", "ek"]


def ct_json(etiket: str, L: pd.DataFrame, Hv: pd.DataFrame, Ft: pd.DataFrame, hb: Dict[str, Any], sayim: Dict[str, Any], vb: Dict[str, Any],
            supheli: List[Dict[str, Any]], guncelle: Optional[Dict[str, Any]], Mm: Dict[str, Any], K: Dict[str, Any],
            E: Dict[str, Any] = CT_ESIK) -> Dict[str, Any]:
    ad = [{k: (r[k] if k in r else None) for k in _CT_ADAY_KOL} for r in L.to_dict("records")] if len(L) else []
    for a in ad:
        a["giris_varsayim"] = "sinyal gününden sonraki ilk işlem günü açılışı (t+1)"
        for k in ("tarih", "olcum_tarihi", "veri_son"):
            if a.get(k) is not None:
                a[k] = str(pd.Timestamp(a[k]).date())
    hav = [{k: r.get(k) for k in ("pazar", "sembol", "tarih", "puan7", "kademe", "hat", "kapanis", "F15", "F17", "F18", "S9")}
           for r in Hv.to_dict("records")] if len(Hv) else []
    for h in hav:
        h["stop0"] = float(h["hat"]) * float(E["olcu"]["stop_carp"]) if h.get("hat") is not None else None
    tum = [{k: r.get(k) for k in ("pazar", "sembol", "tarih", "puan7", "S1", "S7", "S9", "F15", "F17", "F22", "F23")}
           for r in Ft.to_dict("records")] if len(Ft) else []
    return {"durustluk": CT_DURUSTLUK, "surum": CT_SURUM, "etiket": etiket, "uretim_utc": _ct_simdi(), "esik_sha": ct_esik_sha(E), "kapi": K,
            "veri": vb, "guncelleme": guncelle, "sayim": sayim, "havuz": hb, "adaylar": ad, "havuz_tumu": hav, "sinyal_tumu": tum,
            "supheli": supheli,
            "model": {k: Mm[k] for k in ("n", "pozitif", "esik7_sha", "sklearn", "egitim_sinir", "giris_max", "n_iter", "zaman_utc")},
            "ileri_test": {"komut": f"python CANLI_TARAMA.py olc --tarih {etiket}",
                           "olcum_tarihi": {f"{a['pazar']}:{a['sembol']}": a["olcum_tarihi"] for a in ad},
                           "olcum_tarihi_en_gec": max((a["olcum_tarihi"] for a in ad), default=None),
                           "cetvel": "YAPI_HEDEF yh_olay_olc: giriş t+1 açılış, 15 geçerli bar, +%5 / +%10 kapanışla stop'tan önce (h5 / h10), "
                                     "stop önce (st5), takip stopu; eş = aynı giriş günü aynı OC momentum x likidite kovası (en az 3); "
                                     "liste (10) ve havuzun tamamı ölçülür; sonuç CANLI_SONUC.md'ye eklenir (satır silinmez)",
                           "kapsam": ["adaylar", "havuz_tumu"]}}


def ct_md(J: Dict[str, Any]) -> str:
    E = CT_ESIK; hb = J["havuz"]; s = [f"# CANLI TARAMA — {J['etiket']}", "", f"**{J['durustluk']}**", "",
                                        "Taban oran hatırlatması: 3 yılda 10x ABD mikro-cap ~%1, BIST USD ~%1,85. Evren bugün işlem gören hisseler "
                                        "(hayatta kalma yanlılığı: sonuçlar yukarı yanlı okunur).", "",
                                        f"- Üretim (UTC): {J['uretim_utc']} · {J['surum']}", f"- Kurallar CT_ESIK_SHA `{J['esik_sha'][:16]}…` "
                                        f"(ön kayıt arastirma_cikti/canli/CANLI_ON_KAYIT.md; kapı {'geçti' if J['kapi'].get('kontrol') else 'denetlenmedi'})", ""]
    s += ["## 1. Veri", "", "| Pazar | hisse | son tarih | son 5 işlem günü | kaynak |", "|---|---|---|---|---|"]
    for p, v in J["veri"].items():
        s.append(f"| {p} | {v['hisse']} | {v['son_tarih']} | {v['son5'][0]} .. {v['son5'][-1]} | {v['kaynak']} |")
    g = J.get("guncelleme")
    if g:
        s += ["", "İndirme özeti (yfinance, auto_adjust):", "", "| Pazar | istenen | başarılı | başarısız | yeni bar | ortak günde fark > %1 olan sembol | "
              "kipi ölçeklenen | şüpheli | son tarih (en çok / en sık) |", "|---|---|---|---|---|---|---|---|---|"]
        for p, v in g["pazar"].items():
            s.append(f"| {p} | {v['istenen']} | {v['basarili']} | {v['basarisiz_n']} | {v['yeni_bar']} | {v['fark_sembol']} | {v['olcek_sembol']} | "
                     f"{v['supheli']} | {v['son_tarih']} / {v['son_tarih_mod']} |")
        for p, v in g["pazar"].items():
            if v["basarisiz_n"]:
                s.append(f"- {p} başarısız ({v['basarisiz_n']}; eski seri kaldı, son 5 günde sinyal veremez): {', '.join(v['basarisiz'][:40])}"
                         + (" …" if v["basarisiz_n"] > 40 else ""))
    else:
        s += ["", "Veri güncellemesi YOK: mevcut V_*.pkl ile tarandı; 'son 5 işlem günü' her pazarın kendi son tarihinden geriye 5 bar."]
    s += ["", "## 2. Sinyal ve havuz", "", "| Pazar | son 5 günde S6 AL | havuz dışı (t) | likidite alt %20 | bölünme şüphesi | 60 gün tekil düşen | "
          "şüpheli dışlanan | sinyal | özellik hatası |", "|---|---|---|---|---|---|---|---|---|"]
    for p, v in J["sayim"].items():
        s.append(f"| {p} | {v['al_son5']} | {v['havuz_disi']} | {v['likidite_alt20']} | {v['bolunme']} | {v['tekil']} | {v['supheli_dislanan']} | "
                 f"{v['sinyal']} | {v['ozellik_hata']} |")
    sp = hb.get("sayi_pazar", {})
    s += ["", "| Havuz kademesi | toplam | " + " | ".join(E["pazar"]) + " |", "|---|---|" + "---|" * len(E["pazar"])]
    adk = {"S1_S7": "Ş1 VE Ş7 (asıl)", "S1_F22": "(i) Ş1 VE F22 > 0", "S1": "(ii) Ş1"}
    for k in E["havuz"]["kademe"]:
        s.append(f"| {adk[k]} | {hb['sayi'].get(k, 0)} | " + " | ".join(str(sp.get(k, {}).get(p, 0)) for p in E["pazar"]) + " |")
    s += ["", f"**Kullanılan kademe: {adk.get(hb.get('kademe'), 'YOK (havuz boş)')}**", ""]
    s += ["## 3. En iyi 10 (puan7 sırası; pazar başına en çok 5)", "",
          "| # | pazar | sembol | sinyal | kapanış | hat | F21 | stop0 (uzaklık) | +%5 / +%10 | puan7 | Ş9 | Ş10 | parmak | F15 | F17 | F18 | "
          "12 kural | mahkeme | likidite 20g |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in J["adaylar"]:
        mh = "ÖNCEKİ BÖLGE DAHA UYGUN" if a["mahkeme_onceki"] else ("tutarlı" if str(a["mahkeme"]).startswith("SEÇİM") else str(a["mahkeme"])[:30])
        s.append(f"| {a['sira']} | {a['pazar']} | {a['sembol']} | {pd.Timestamp(a['tarih']).date()} | {_f(a['kapanis'])} | {_f(a['hat'])} | "
                 f"{_f(a['F21'])} | {_f(a['stop0'])} ({_y(a['stop_uzak'])}) | {_f(a['hedef5'])} / {_f(a['hedef10'])} | {_f(a['puan7'], 3)} | "
                 f"{'✓' if a['S9'] else '-'} | {'✓' if a['S10'] == 1 else '-'} | {'✓' if a['F19'] == 1 else '-'} | {_f(a['F15'])} | {_y(a['F17'], 0)} | "
                 f"{_y(a['F18'])} | {'-' if a['kural12'] is None or not np.isfinite(float(a['kural12'])) else int(a['kural12'])}/12 | {mh} | "
                 f"{_f(float(a['likidite20']) / 1e6, 1)} M {a['para']} |")
    if not J["adaylar"]:
        s.append("| - | havuz boş | | | | | | | | | | | | | | | | | |")
    s += ["", "Okuma: stop0 = hat x 0,98; hedefler kapanışa göre (gerçek giriş ertesi açılış). puan7 = 7. tur M2 modelinin P(15 barda +%5 stop'tan "
          "önce) tahmini (eğitim 2016 - 31.08.2026 Y1 olayları; modelin taban P'si "
          f"{_f(J['model']['pozitif'], 3)}). Ş9 = U dip çanağı; Ş10 = MACD pozitif uyumsuzluk; parmak = F19 P1.1 (4 mum dip öbeği). Mahkeme bilgi "
          "satırıdır (eleme değil).", ""]
    s += ["## 4. Şüpheli veri (listeden dışlandı)", ""]
    if J["supheli"]:
        s += [f"- {x['pazar']} {x['sembol']}: {x['neden']}" for x in J["supheli"][:60]]
    else:
        s.append("- yok")
    s += ["", "## 5. İleri test", "", f"- Ölçüm komutu: `{J['ileri_test']['komut']}` (en geç ölçüm tarihi {J['ileri_test']['olcum_tarihi_en_gec']}).",
          f"- Cetvel: {J['ileri_test']['cetvel']}.", "- Sonuçlar arastirma_cikti/canli/CANLI_SONUC.md'ye eklenir.", ""]
    return "\n".join(s)


# ================================================================ 7) PDF
def ct_pdf(J: Dict[str, Any], L: pd.DataFrame, yol: str, veri: Optional[str] = None) -> str:
    """Kapak (dürüstlük + tablo) + aday başına bir sayfa: 120 bar + S6 bölge + hat + F21 + Ş9 çanak + stop0 / hedefler + MACD + hacim."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import Rectangle
    Vc: Dict[str, Dict[str, pd.DataFrame]] = {}
    with PdfPages(yol, metadata={"Title": f"CANLI TARAMA {J['etiket']}", "Creator": "CANLI_TARAMA", "Producer": None}) as pp:
        fig = plt.figure(figsize=(11.69, 8.27))
        try:
            fig.text(0.04, 0.95, f"CANLI TARAMA — {J['etiket']}  (izleme / ileri test listesi)", fontsize=15, weight="bold")
            import textwrap
            fig.text(0.04, 0.80, "\n".join(textwrap.wrap(J["durustluk"], 150)), fontsize=9, color="#a50026", va="bottom")
            sat = [f"Kademe: {J['havuz'].get('kademe')}   ·   veri son tarih: " + ", ".join(f"{p} {v['son_tarih']}" for p, v in J["veri"].items())]
            sat.append("")
            sat.append(f"{'#':>2} {'pazar':<5} {'sembol':<10} {'sinyal':<10} {'kapanış':>10} {'stop0':>10} {'puan7':>6}  Ş9 Ş10 parmak 12k  mahkeme")
            for a in J["adaylar"]:
                sat.append(f"{a['sira']:>2} {a['pazar']:<5} {a['sembol']:<10} {str(pd.Timestamp(a['tarih']).date()):<10} {_f(a['kapanis']):>10} "
                           f"{_f(a['stop0']):>10} {_f(a['puan7'], 3):>6}  {'✓ ' if a['S9'] else '- '} {'✓  ' if a['S10'] == 1 else '-  '} "
                           f"{'✓     ' if a['F19'] == 1 else '-     '} {'-' if a['kural12'] is None else int(a['kural12']):>2}  "
                           f"{'ÖNCEKİ BÖLGE DAHA UYGUN' if a['mahkeme_onceki'] else 'tutarlı'}")
            if not J["adaylar"]:
                sat.append("havuz boş: aday yok")
            fig.text(0.04, 0.76, "\n".join(sat), fontsize=8.5, family="DejaVu Sans Mono", va="top")
            fig.text(0.04, 0.04, "Sayfalar: 120 bar (son bar = verinin son günü), mavi kutu = S6 bölgesi, lacivert = hat, kırmızı kesik = F21 (15 bar tepe), "
                                 "mor kesik = Ş9 çanak (son 40 bar 2. derece uyum), kırmızı nokta-çizgi = stop0, yeşil = +%5 / +%10 (kapanışa göre), "
                                 "dikey = sinyal günü. Alt panel MACD (12, 26, 9) ve hacim.", fontsize=7.5, wrap=True)
            pp.savefig(fig)
        finally:
            plt.close(fig)
        for a in J["adaylar"]:
            p, s = a["pazar"], a["sembol"]
            if p not in Vc:
                Vc[p] = OC.oc_veri(p, klasor=J["veri"][p]["kaynak"])["V"]
            d = YH._yh_hazir(Vc[p][s]); t = pd.Timestamp(a["tarih"])
            i = int(d.index.get_loc(t)); N = len(d) - 1
            G = GE.ge_gorsel_veri(d, t, hazir=True)
            a0 = max(0, N - 119); W = d.iloc[a0:N + 1]
            x = np.arange(a0, N + 1) - i
            o, h, l, c, v = (W[k].to_numpy(float) for k in ("Open", "High", "Low", "Close", "Volume"))
            w0 = max(0, N - int(YH.YH_ESIK8["macd"]["pencere"]))
            m, sg, hs = YH.yh_macd(d.Close.to_numpy(float)[w0:N + 1])
            k0 = a0 - w0
            fig = plt.figure(figsize=(11.69, 8.27))
            try:
                gs = fig.add_gridspec(3, 1, height_ratios=[3.2, 1.0, 0.8], hspace=0.06)
                ax = fig.add_subplot(gs[0]); am = fig.add_subplot(gs[1], sharex=ax); av = fig.add_subplot(gs[2], sharex=ax)
                renk = np.where(c >= o, "#1a9850", "#d73027")
                ax.vlines(x, l, h, colors=renk, linewidth=0.8, zorder=3)
                ax.bar(x, np.maximum(np.abs(c - o), (h - l) * 0.01), bottom=np.minimum(o, c), width=0.7, color=renk, edgecolor=renk, linewidth=0.4, zorder=4)
                sol = int(G["sol"]) - int(G["son"])
                x0 = max(sol, x[0]) - 0.5
                ust = G["ust"] if np.isfinite(G["ust"]) else G["tavan"]
                ax.add_patch(Rectangle((x0, G["hat"]), -0.5 - x0, max(ust - G["hat"], 0.0), facecolor="#4575b4", alpha=0.10, edgecolor="#4575b4",
                                       linewidth=0.6, zorder=1, label="S6 bölgesi"))
                ax.hlines(a["hat"], x0, x[-1] + 0.5, colors="#313695", linewidth=1.3, zorder=5, label=f"S6 hat {_f(a['hat'])}")
                if a.get("F21") is not None and np.isfinite(float(a["F21"])):
                    ax.hlines(float(a["F21"]), -15.5, 0.5, colors="#d7191c", linestyles="--", linewidth=1.5, zorder=6, label=f"F21 yakın tavan {_f(a['F21'])}")
                n9 = int(YH.YH_ESIK["denemeler"]["Y11"]["s9_prm"]["pencere"])
                if i >= n9:
                    Lw = d.Low.to_numpy(float)[i - n9:i]; xx = np.arange(n9, dtype=float)
                    cf = np.polyfit(xx, Lw, 2)
                    ax.plot(xx - n9, np.polyval(cf, xx), color="#762a83", linewidth=2.0, linestyle="--", zorder=6,
                            label="Ş9 çanak (son 40 bar uyum)" + (" ✓" if a["S9"] else " (Ş9 tutmadı)"))
                ax.hlines(a["stop0"], 0.5, x[-1] + 3, colors="#a50026", linestyles="-.", linewidth=1.0, zorder=5, label=f"stop0 {_f(a['stop0'])}")
                ax.hlines(a["hedef5"], 0.5, x[-1] + 3, colors="#1a9850", linestyles="--", linewidth=1.0, zorder=5, label=f"+%5 {_f(a['hedef5'])}")
                ax.hlines(a["hedef10"], 0.5, x[-1] + 3, colors="#006837", linestyles=":", linewidth=1.3, zorder=5, label=f"+%10 {_f(a['hedef10'])}")
                for z in (ax, am, av):
                    z.axvline(0, color="#555555", linewidth=0.8, linestyle=":", zorder=2)
                ax.legend(loc="upper left", fontsize=7, ncol=2, frameon=False)
                ax.grid(alpha=0.25); ax.set_ylabel("fiyat")
                ylo = min(np.nanmin(l), a["stop0"]); yhi = max(np.nanmax(h), a["hedef10"])
                ax.set_ylim(ylo - (yhi - ylo) * 0.04, yhi + (yhi - ylo) * 0.06)
                mm, ss, hh = m[k0:], sg[k0:], hs[k0:]
                am.bar(x, hh, width=0.7, color=np.where(np.nan_to_num(hh) >= 0, "#91cf60", "#fc8d59"), zorder=2)
                am.plot(x, mm, color="#2166ac", linewidth=1.0, label="MACD"); am.plot(x, ss, color="#f46d43", linewidth=1.0, label="sinyal")
                am.axhline(0, color="#888888", linewidth=0.6); am.legend(loc="upper left", fontsize=7, frameon=False); am.grid(alpha=0.25)
                am.set_ylabel("MACD 12,26,9")
                av.bar(x, v, width=0.7, color=renk, alpha=0.7); av.set_ylabel("hacim"); av.grid(alpha=0.25)
                av.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
                av.set_xlabel(f"bar (0 = sinyal günü {t.date()}; son bar {d.index[-1].date()})")
                plt.setp(ax.get_xticklabels(), visible=False); plt.setp(am.get_xticklabels(), visible=False)
                ax.set_xlim(x[0] - 1, x[-1] + 4)
                mh = "ÖNCEKİ BÖLGE DAHA UYGUN" if a["mahkeme_onceki"] else "mahkeme: tutarlı"
                fig.suptitle(f"#{a['sira']}  {p} {s}  sinyal {t.date()}  ·  puan7 {_f(a['puan7'], 3)}  ·  Ş9 {'✓' if a['S9'] else '-'}  Ş10 "
                             f"{'✓' if a['S10'] == 1 else '-'}  parmak {'✓' if a['F19'] == 1 else '-'}  ·  12 kural "
                             f"{'-' if a['kural12'] is None else int(a['kural12'])}/12  ·  {mh}", fontsize=10.5, weight="bold", y=0.975)
                fig.text(0.5, 0.935, "İZLEME / İLERİ TEST — ÖNERİ DEĞİL. " + f"kapanış {_f(a['kapanis'])} · stop0 uzaklık {_y(a['stop_uzak'])} · F15 "
                         f"{_f(a['F15'])} · F17 {_y(a['F17'], 0)} · F18 {_y(a['F18'])} · likidite20 {_f(float(a['likidite20']) / 1e6, 1)} M {a['para']}",
                         ha="center", fontsize=8.5, color="#a50026")
                pp.savefig(fig)
            finally:
                plt.close(fig)
    return yol


# ================================================================ 8) İLERİ TEST ÖLÇÜMÜ
def ct_olc_olaylar(Ad: pd.DataFrame, veri: Optional[str] = None, E: Dict[str, Any] = CT_ESIK) -> pd.DataFrame:
    """Ad: [pazar, sembol, tarih, hat, (kapsam)] -> yh_olay_olc satırları (YAPI_HEDEF cetveli). Kriz kesiği bellekte açık."""
    out = []
    for p, g in Ad.groupby("pazar"):
        with ct_kriz_ac():
            Vd = OC.oc_veri(p, klasor=ct_kaynak(p, veri))
            bas = pd.to_datetime(g.tarih).min() - pd.Timedelta(days=200)
            Vd = {**Vd, "V": {s: d[d.index >= bas] for s, d in Vd["V"].items() if len(d[d.index >= bas]) >= 30}}
            P = OC.oc_panel(Vd); Cl = YH.yh_kapanis(P, Vd)
            sig = g.assign(tarih=pd.to_datetime(g.tarih), yon=1)
            sig["stop0"] = sig.hat.astype(float) * float(E["olcu"]["stop_carp"])
            X, say = OC.oc_olay_hazirla(sig[["sembol", "tarih", "pazar"]], P)
            if len(X):
                X = X.merge(sig[["sembol", "tarih", "stop0", "yon", "hat"] + [c for c in ("kapsam", "sira") if c in sig.columns]],
                            on=["sembol", "tarih"], how="left")
                Z = YH.yh_olay_olc(P, Cl, Vd, X, YH._yh_deneme_no("Y1"), OC.OC_ESIK["pazar"].index(p) + 1)
                Z.insert(0, "pazar", p); out.append(Z)
            dus = sig.merge(X[["sembol", "tarih"]], on=["sembol", "tarih"], how="left", indicator=True) if len(X) else sig.assign(_merge="left_only")
            dus = dus[dus._merge == "left_only"]
            if len(dus):
                neden = ", ".join(f"{k} {v}" for k, v in say.items() if v and k not in ("girdi",))
                out.append(dus.drop(columns="_merge").assign(olc=False, cikis_tur=f"olay_hazirla_dustu (OC süzgeci giriş günü: {neden})"))
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def ct_olc(etiket: str, veri: Optional[str] = None, cikti: Optional[str] = None, sonuc: Optional[str] = None) -> Dict[str, Any]:
    """Bir tarama listesinin ileri test ölçümü -> CANLI_SONUC.md'ye EKLER. Döner özet."""
    cikti = cikti or CT_YOL["cikti"]; sonuc = sonuc or CT_YOL["sonuc"]
    yj = os.path.join(cikti, CT_DOSYA["json"].format(e=etiket))
    if not os.path.exists(yj):
        raise CTHata(f"tarama json yok: {yj}")
    J = json.load(open(yj, encoding="utf-8"))
    A = pd.DataFrame(J["adaylar"]); Hv = pd.DataFrame(J["havuz_tumu"])
    if not len(A) and not len(Hv):
        raise CTHata(f"{etiket}: aday yok")
    A = A.assign(kapsam="liste") if len(A) else A
    if len(Hv):
        Hv = Hv.assign(kapsam="havuz")
        if len(A):
            Hv = Hv[~Hv.set_index(["pazar", "sembol", "tarih"]).index.isin(A.set_index(["pazar", "sembol", "tarih"]).index)]
    Ad = pd.concat([x[["pazar", "sembol", "tarih", "hat", "kapsam"] + (["sira"] if "sira" in x.columns else [])] for x in (A, Hv) if len(x)],
                   ignore_index=True)
    Z = ct_olc_olaylar(Ad, veri)
    vson = {}
    for p in sorted(Ad.pazar.unique()):
        try:
            vson[p] = str(max(d.index.max() for d in _ct_pkl_oku(os.path.join(ct_kaynak(p, veri), f"V_{p}.pkl")).values()).date())
        except Exception as ex:  # yalnız bilgi satırı
            vson[p] = f"? ({ex})"
    oz = ct_olc_ozet(Z)
    md = ct_olc_md(etiket, Z, oz, vson, J)
    kalici = Z.cikis_tur.astype(str).str.startswith("olay_hazirla_dustu") | (Z.cikis_tur.astype(str) == "giris_stop_otesi")
    tamam = bool(len(Z)) and bool((Z.olc.fillna(False).astype(bool) | kalici).all())     # ölçülemeyen yalnız kalıcı nedenle (süzgeç / stop ötesi)
    onceki = open(sonuc, encoding="utf-8").read() if os.path.exists(sonuc) else ("# CANLI TARAMA — İLERİ TEST SONUÇLARI (eklenir, silinmez)\n\n"
                                                                               f"**{CT_DURUSTLUK}**\n\n")
    isaret = f"<!-- OLCULDU {etiket} -->" if tamam else f"<!-- KISMI {etiket} {_ct_simdi()} -->"
    _ct_yaz(sonuc, onceki.rstrip("\n") + "\n\n" + md + "\n" + isaret + "\n", "ileri test sonucu")
    return {"etiket": etiket, "tamam": tamam, "ozet": oz, "satir": Z, "md": md}


def ct_olc_ozet(Z: pd.DataFrame) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if not len(Z):
        return out
    for k in ("liste", "havuz", "hepsi"):
        X = Z if k == "hepsi" else Z[Z.kapsam == k]
        X = X[X.olc.fillna(False).astype(bool)]
        Xe = X[X.es_h5.notna()] if "es_h5" in X else X.iloc[0:0]
        out[k] = {"n": int(len(X)), "h5": float(X.h5.mean()) if len(X) else np.nan, "h10": float(X.h10.mean()) if len(X) else np.nan,
                  "st5": float(X.st5.mean()) if len(X) else np.nan, "n_esli": int(len(Xe)),
                  "es_h5": float(Xe.es_h5.mean()) if len(Xe) else np.nan, "es_st5": float(Xe.es_st5.mean()) if len(Xe) else np.nan,
                  "h5_esli": float(Xe.h5.mean()) if len(Xe) else np.nan,
                  "getiri_ort": float(X.getiri.mean()) if len(X) else np.nan, "getiri_med": float(X.getiri.median()) if len(X) else np.nan}
    return out


def ct_olc_md(etiket: str, Z: pd.DataFrame, oz: Dict[str, Any], vson: Dict[str, str], J: Dict[str, Any]) -> str:
    s = [f"## Ölçüm: liste {etiket} (ölçüm zamanı {_ct_simdi()}; veri son tarihi " + ", ".join(f"{p} {v}" for p, v in vson.items()) + ")", "",
         f"Kademe: {J['havuz'].get('kademe')}. Cetvel: {J['ileri_test']['cetvel']}. İZLEME / İLERİ TEST — ÖNERİ DEĞİL.", "",
         "| kapsam | n ölçülen | +%5 payı (h5) | +%10 payı | stop önce (st5) | eşli n | olay h5 (eşli) | eş h5 | eş st5 | takip getirisi ort / medyan (bilgi) |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for k in ("liste", "havuz", "hepsi"):
        o = oz.get(k)
        if not o:
            continue
        s.append(f"| {k} | {o['n']} | {_y(o['h5'], 0)} | {_y(o['h10'], 0)} | {_y(o['st5'], 0)} | {o['n_esli']} | {_y(o['h5_esli'], 0)} | "
                 f"{_y(o['es_h5'], 0)} | {_y(o['es_st5'], 0)} | {_y(o['getiri_ort'])} / {_y(o['getiri_med'])} |")
    n = oz.get("hepsi", {}).get("n", 0)
    s += ["", f"Örneklem: n = {n}" + (" < 30: ÖRNEKLEM YETERSİZ; olaylar tek tek okunur, bulgu denmez." if n < 30 else "."),
          "Hayatta kalma: evren bugün işlem gören hisseler (yukarı yanlı).", "",
          "| kapsam | # | pazar | sembol | sinyal | giriş | giriş açılış | stop0 | h5 | h10 | st5 | +%5 günü | stop günü | eş h5 (n eş) | takip getirisi | çıkış |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    if len(Z):
        Z = Z.sort_values(["kapsam", "pazar", "sembol"], key=lambda c: c.map({"liste": 0, "havuz": 1}) if c.name == "kapsam" else c)
        for r in Z.to_dict("records"):
            ol = bool(r.get("olc")) if r.get("olc") is not None and r.get("olc") == r.get("olc") else False
            g = lambda k: r.get(k) if r.get(k) is not None else np.nan  # noqa: E731
            s.append(f"| {r.get('kapsam')} | {'' if g('sira') != g('sira') else int(g('sira'))} | {r['pazar']} | {r['sembol']} | "
                     f"{pd.Timestamp(r['tarih']).date()} | {pd.Timestamp(r['giris']).date() if isinstance(r.get('giris'), (pd.Timestamp, str)) else '-'} | "
                     f"{_f(g('E0'))} | {_f(g('stop0'))} | {_f(g('h5'), 0) if ol else 'ölçülemedi'} | {_f(g('h10'), 0) if ol else '-'} | "
                     f"{_f(g('st5'), 0) if ol else '-'} | {int(g('k5')) + 1 if ol and np.isfinite(g('k5')) and g('k5') >= 0 else '-'} | "
                     f"{int(g('kst')) + 1 if ol and np.isfinite(g('kst')) and g('kst') >= 0 else '-'} | {_f(g('es_h5'))} ({_f(g('n_es'), 0)}) | "
                     f"{_y(g('getiri'))} | {r.get('cikis_tur') or ''} |")
    return "\n".join(s)


def ct_olc_vadesi(veri: Optional[str] = None, cikti: Optional[str] = None, sonuc: Optional[str] = None) -> List[Dict[str, Any]]:
    """Vadesi gelmiş (en geç ölçüm tarihi <= verinin son tarihi) ve ölçülmemiş (OLCULDU işareti yok) bütün listeler."""
    cikti = cikti or CT_YOL["cikti"]; sonuc = sonuc or CT_YOL["sonuc"]
    metin = open(sonuc, encoding="utf-8").read() if os.path.exists(sonuc) else ""
    son = []
    for p in CT_ESIK["pazar"]:
        try:
            son.append(max(d.index.max() for d in _ct_pkl_oku(os.path.join(ct_kaynak(p, veri), f"V_{p}.pkl")).values()))
        except CTHata:
            pass
    if not son:
        raise CTHata("ölçüm için veri yok")
    vson = min(son); out = []
    for f in sorted(os.listdir(cikti)) if os.path.isdir(cikti) else []:
        m = re.fullmatch(r"CANLI_TARAMA_(\d{4}-\d{2}-\d{2})\.json", f)
        if not m or f"<!-- OLCULDU {m.group(1)} -->" in metin:
            continue
        J = json.load(open(os.path.join(cikti, f), encoding="utf-8"))
        eg = J.get("ileri_test", {}).get("olcum_tarihi_en_gec")
        if eg and pd.Timestamp(eg) <= vson:
            try:
                R = ct_olc(m.group(1), veri, cikti, sonuc); out.append({"etiket": m.group(1), "tamam": R["tamam"]})
                metin = open(sonuc, encoding="utf-8").read()
            except CTHata as ex:
                ctlog.warning("olc %s: %s", m.group(1), ex)
    return out


# ================================================================ ÇAKIŞMA KAPISI
def _cakisma_kontrol_ct(_once=_CK_ONCE_CT, _dosya="CANLI_TARAMA.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_CT", "_CK_KAYIT", "_cakisma_kontrol_ct", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "warnings", "_dt", "annotations", "contextlib", "pickle",
           "Any", "Dict", "List", "Optional", "Tuple", "OC", "SY", "YH", "GE", "_f", "_y")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ct()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=CT_SURUM)
    ap.add_argument("komut", choices=["onkayit", "guncelle", "tara", "olc", "model", "sha"])
    ap.add_argument("--veri", default=None, help="okunacak klasör (varsayılan: /tmp/veri_canli varsa o, yoksa /tmp/veri)")
    ap.add_argument("--etiket", default=None, help="çıktı adı tarihi (varsayılan: verinin en geç son tarihi)")
    ap.add_argument("--tarih", default=None, help="olc: ölçülecek listenin etiketi")
    ap.add_argument("--vadesi", action="store_true", help="olc: vadesi gelmiş ölçülmemiş bütün listeler")
    ap.add_argument("--guncelle", action="store_true", help="tara: önce yfinance güncellemesi")
    ap.add_argument("--islem", type=int, default=max(1, min(4, os.cpu_count() or 1)))
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--pdfsiz", action="store_true")
    ap.add_argument("--uzerine-yaz", dest="uzerine_yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(ct_onkayit_yaz(a.uzerine_yaz))
        elif a.komut == "guncelle":
            print(json.dumps(ct_guncelle(a.veri), ensure_ascii=False, indent=1, default=_ct_json)[:4000])
        elif a.komut == "tara":
            G_ = ct_guncelle(a.veri) if a.guncelle else None
            R_ = ct_tara(None if a.guncelle else a.veri, a.etiket, a.cikti, a.islem, G_, pdf=not a.pdfsiz)
            print(open(R_["md"], encoding="utf-8").read()[:6000])
        elif a.komut == "olc":
            if a.vadesi:
                print(json.dumps(ct_olc_vadesi(a.veri, a.cikti), ensure_ascii=False, indent=1))
            elif a.tarih:
                print(ct_olc(a.tarih, a.veri, a.cikti)["md"][:6000])
            else:
                raise CTHata("olc: --tarih YYYY-MM-DD ya da --vadesi gerekli")
        elif a.komut == "model":
            M_ = ct_model(yeniden=True); print(json.dumps({k: v for k, v in M_.items() if k not in ("model", "med")}, ensure_ascii=False, indent=1))
        else:
            print(json.dumps({"CT_ESIK_SHA": ct_esik_sha(), "YH_ESIK7_SHA": YH.yh_esik7_sha()}, indent=1))
    except CTHata as ex:
        ctlog.error("%s", ex); sys.exit(1)
