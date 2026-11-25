"""UC_IZ — ÜÇ FİYAT DIŞI İZ AYNI DİP OLAYINDA, AYNI ANDA (25 Kasım 2026; iş tanımı: ana model mesajı).

Cemal (25 Kas 2026): "Şimdi iz olacak diğer hipotezleri dene, en iyi ilk üç tane." + KASA KURALI: "kasa en azından iki üç olayı aynı anda
ölçen olaylarla açılmalı". Bu iş bir KEŞİF ölçümüdür (açık veri, KASA kesik 2022-12-31); kasa AÇILMAZ.

SORU: dipteki bir ABD hissesinde (KART_TUR2 KT02 'dipte' olayı) üç izden kaçı birlikte var; hisse 15 mumda eşlerinden ne kadar ayrışıyor,
eşler içinde en çok zıplayanlar (üst %10) arasına ne sıklıkla giriyor?

İZLER (tanımlar mevcut modüllerden AYNEN; UC_ESIK; sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
  R  sektör rüzgârı = KART_TUR2 KT10: D9_YENIDEN durum tablosu (KART_TUR2.k2_d9_durum, olay_bas K2_ESIK['d9_olay_bas']) 'c' satırı
     (D9.d9_satir: RÜZGÂR ∧ ¬D9 ∧ sektör var) olay günü t'de. Bilgi: R_any = RÜZGÂR (D9 şartsız).
  B  bilanço (FON_IZI k28 'ust'): KURULAMADI -> YEDEK Y1. k28_X_abd / pead liste_abd 2022-12-01'de başlar (açık kesikten önce yalnız Aralık
     2022); karar hücreleri 2016-19 / 2020-22 kapsanmaz. B0 da kurulamaz (bilanço günü listesi yok).
  I  içeriden alım (FON_IZI k30 A1): KURULAMADI -> YEDEK Y2. k30_alim 2022-01-03'te başlar (2016-21 Form 4 setleri repoda yok; indirme yasak).
     Bilgi: I22 = son 30 takvim gününde (dosyalama günü D <= t) >= 1 A1 alımı, yalnız t >= 2022-02-02 (pencere tam kapsanır).
  Y1 (B yerine) Ç112 blok hacimli taban günü = FON_IZI.fi_k38_sinyaller 'S3_blok_taban_yukari' (hacim >= 20 x önceki 20 gün medyanı VE gün
     <= -%9,5) hissenin t'ye kadarki son 15 geçerli barında (t dahil).
  Y2 (I yerine) Ç223 T derin toplam uyumsuzluk = arastirma_cikti/macd_uyum/uyum_toplam.csv.gz ABD satırları, PFc <= -0,10 ∧ MRc >= 0,30
     (UYUM_T_ON_KAYIT), olay günü hissenin t'ye kadarki son 15 geçerli barında (t dahil).
  N = R + Y1 + Y2 (0..3).
DİP OLAYI: KART_TUR2 KT02 aynen (YH.yh_s6_hisse 'al' -> Y1 olayı OC.oc_olay_hazirla P2 havuzu, 60 gün tekil -> Ş1 (YH.yh_s9_sartlar 'S1')).
  Ölçüm CETVEL2 v2.2: C2.c2_olay (CETVEL2 havuzu, tekil 15 birleşik takvim satırı; giriş t+1 açılış) -> R15, konum eşi C2.c2_es (aynı giriş
  günü, aynı kova ATRP x likidite x F15, >= 5 eş; dışlanan = aynı gün bütün KT02 olay hisseleri (tekil 1 eşlemesi)).
ÖLÇÜLER: Ö1 FARK (C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum, plasebo hariç; TUTAR hücrede C2.c2_plasebo); Ö2 ÜST10 / ALT10 payı - taban
  (formül ve plasebo: aynı gün aynı kovadan rastgele üye, 200 tohum); Ö3 h5 / stop (C2.c2_bilgi; eş = plasebo tohum 0 üyesi), piyasa yönü.
Komut:  python UC_IZ.py hazirla     olaylar + bayraklar (getirisiz) + D1 / D2 / D3 -> /tmp/uc_iz/olay.pkl, uc_iz_hazirlik.json
        python UC_IZ.py kos         kapı (kontrol + ön kayıt sha + commit) -> ölçüm -> uc_iz_satir.csv.gz, uc_iz_sonuc.json
        python UC_IZ.py sha         kod / eşik sha
Colab:  exec(open('UC_IZ.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/kasa/acik (KASA açık, KASA.kasa_kapisi), /tmp/veri2 (FON_IZI vpac). Komisyon yok. Evren bugün işlem gören hisseler (K7: yukarı yanlı).
Mevcut modüller DEĞİŞTİRİLMEZ; içe alınır.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_UC = {k: id(v) for k, v in globals().items()}

import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import datetime as _dt  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_UC = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_UC not in sys.path:
    sys.path.insert(0, KOK_UC)

uclog = logging.getLogger("col.uc_iz")
if not uclog.handlers:
    _uc_h = logging.StreamHandler(sys.stderr)
    _uc_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s uc_iz: %(message)s", "%H:%M:%S"))
    uclog.addHandler(_uc_h)
    uclog.setLevel(logging.INFO)
    uclog.propagate = False


class UCHata(RuntimeError):
    """Durdurucu hata: kasa / kontrol / ön kayıt kapısı, veri yok, kesik aşımı, doğrulama tutmadı."""


UC_SURUM = "UC_IZ v1.0 (2026-11-25): R (KT10) + Y1 (Ç112, B yedeği) + Y2 (Ç223 T, I yedeği) KT02 dip olayında; CETVEL2 v2.2 R15; açık veri"
UC_YOL = {"cikti": os.path.join(KOK_UC, "arastirma_cikti", "uc_iz"), "kod": os.path.join(KOK_UC, "UC_IZ.py"),
          "veri": os.environ.get("UC_VERI", "/tmp/kasa/acik"), "veri2": os.environ.get("UC_VERI2", "/tmp/veri2"),
          "kasa": os.environ.get("KASA_DIZIN", "/tmp/kasa"), "gecici": os.environ.get("UC_GECICI", "/tmp/uc_iz"),
          "uyum_toplam": os.path.join(KOK_UC, "arastirma_cikti", "macd_uyum", "uyum_toplam.csv.gz"),
          "k2_satir": os.path.join(KOK_UC, "arastirma_cikti", "kart2", "acik", "k2_satir.csv.gz")}
UC_DOSYA = {"onkayit": "UC_IZ_ON_KAYIT.md", "rapor": "UC_IZ_RAPOR.md", "satir": "uc_iz_satir.csv.gz", "sonuc": "uc_iz_sonuc.json",
            "hazirlik": "uc_iz_hazirlik.json", "olay": "olay.pkl"}
UC_KESIK = pd.Timestamp("2022-12-31")

UC_ESIK: Dict[str, Any] = {
    "surum": "UC-1.0",
    "pazar": "ABD",
    "donem": {"d1619": ["2016-01-01", "2019-12-31"], "d2022": ["2020-01-01", "2022-12-31"]},
    "ufuk": 15, "tekil": 15, "es_min": 5,
    "pencere_bar": 15,                       # Y1 / Y2: t'ye kadarki son 15 geçerli bar (t dahil)
    "i22": {"gun": 30, "bas": "2022-02-02"},  # bilgi: k30 A1, son 30 takvim günü, pencere tam kapsanınca
    "y2": {"PFc_ust": -0.10, "MRc_alt": 0.30},
    "ust_pay": 0.90, "alt_pay": 0.10,
    "plasebo_tohum": 200, "plasebo_kok": 25112026,
    "n_min": 30, "guc_esik": 0.80, "bh_q": 0.10,
    "iz": ["R", "Y1", "Y2"],
    "karar_kurali": (
        "YÖN TUTARLI(iz) <=> iki karar hücresinin (ABD d1619, ABD d2022) ikisinde de FARK(iz var) > 0 VE FARK(var) - FARK(yok) > 0 VE "
        "(ÜST10 - taban_formül) > 0 VE (ÜST10 - taban_plasebo) > 0. TUTAR <=> ayrıca iki hücrede c2 hükmü (C2.c2_hucre + MU.mu_sira_boot + "
        "MU.mu_hukum, plasebo hariç) TUTAR. Aksi: iki hücrede de iz-var n >= 30 ve güç >= 0,80 ise TUTMADI, değilse ÖLÇÜLEMEDİ. "
        "BİRLİKTE ARTIYOR <=> iki hücrede FARK(N=0) < FARK(N=1) < FARK(N>=2) VE N>=2 FARK boot alt > 0 en az bir hücrede, ötekinde FARK > 0. "
        "KASA ADAYI <=> en az iki iz YÖN TUTARLI VE BİRLİKTE ARTIYOR (yalnız ÖNERİ; kasa açılmaz). BH q 0,10: aile = 3 tek iz + N>=2 "
        "(p = iki hücrenin en büyük permütasyon p'si)."),
}

UC_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = CETVEL2 v2.2 konum eşi (aynı giriş günü, aynı kova ATRP x likidite x F15, >= 5 eş; aynı gün KT02 dip olayları "
                   "dışlanır); iz var / yok ve N = 0 aynı dip olay kümesinden; taban formül + plasebo (aynı gün aynı kova rastgele üye, 200 tohum)"),
    "K2": ("EVET", "R: D9 durumu t'ye kadar fiyatla; Y1 / Y2: pencere [t-14 geçerli bar, t]; I22: D <= t; olay dosyaları <= 2022-12-31 KES + "
                   "assert (uc_kes); D2 prefix testi (2019-06-28 ve 2021-06-30 kesik) + 30 rastgele olayda hisse kesik denetimi"),
    "K3": ("EVET", "geçerli bar GE.ge_hazir (H > L, V > 0); KT02 YH S6 / GE özellikleri aynen; Y1 S3 'gecerli' şartı; R15 CETVEL2 panel"),
    "K4": ("EVET", "dip olayları aynı hissede >= 15 birleşik takvim satırı (C2.c2_olay tekil 15, ilk kalır); Y1 sinyali 60 gün tekil (KT02 aynen); medyan yazılır"),
    "K5": ("EVET", "giriş = t + 1 açılış (OC.oc_olay_hazirla); R15 = 15. geçerli bar kapanışı / giriş açılışı - 1"),
    "K6": ("EVET", "fiyat KASA açık V_ABD (fi_k1_veri bölünme düzeltmeli, tek kip); yeni pazar yok; Y1 hacim oranı birim bağımsız"),
    "K7": ("EVET", "evren bugün işlem gören 1.361 ABD hissesi; batanlar yok; dip olaylarında sonuç yukarı yanlı okunur (raporda)"),
    "K8": ("EVET", "n < 30 hücre ÖLÇÜLEMEDİ; iki dönem (2016-19 / 2020-22) aynı yön şartı; BH q 0,10 aile 4; küçük örneklemden bulgu denmez"),
    "K9": ("EVET", "tanım + eşik (UC_ESIK sha) + kod sha + D1-D3 ön kayıtta, ön kayıt commit'i koşudan önce; kapı uc_kapi bunu denetler"),
    "K10": ("EVET", "D3: 10 rastgele Y1 ve 10 rastgele Y2 (ve 10 I22) bayraklı olayda ham satır (S3 günü hacim / medyan / getiri; T satırı PFc / MRc; "
                    "Form 4 satırı) yazdırılıp elle okunur; haber / kurum etiketi maddeleri UYGULANMAZ (KAP haberi yok)"),
    "K11": ("EVET", "D4: en az 2 hücre uc_iz_satir.csv.gz'den bağımsız düz pandas ile yeniden üretilir (raporda)"),
    "K12": ("EVET", "fiyat değişimi (R15) ile kâr / zarar ayrı; 'iz' sözü yalnız karar kuralı geçerse; sayı ile yorum ayrı cümlede"),
    "K13": ("EVET", "çakışma kapısı var; mevcut modüller / defterler değişmez; push yok; yeni dal yok; e-posta / anahtar yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; alım-satım önerisi yok; keşif ölçümü"),
}


# ================================================================ 0) YARDIMCI
def _uc_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _uc_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def uc_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or UC_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _uc_json(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _uc_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_uc_json(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, np.datetime64)):
        return str(pd.Timestamp(o).date())
    return o


def _uc_jyaz(yol: str, J: Any) -> None:
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol + ".tmp", "w", encoding="utf-8") as f:
        json.dump(_uc_json(J), f, ensure_ascii=False, indent=1)
    os.replace(yol + ".tmp", yol)


def _uc_git(args: List[str]) -> str:
    try:
        return subprocess.run(["git"] + args, cwd=KOK_UC, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as ex:   # git yoksa kapı düşer (fail-closed çağıranda)
        uclog.warning("git çalışmadı: %s", ex)
        return ""


def uc_donem(g: Any) -> np.ndarray:
    import CETVEL2 as C2
    return C2._c2_donem22(g, UC_ESIK["donem"])


def uc_kes(X: pd.DataFrame, kol: str, ad: str, kesik: pd.Timestamp = UC_KESIK) -> pd.DataFrame:
    """Olay dosyası satırlarını tarih <= kesik olarak keser ve MEKANİK denetler (kesik sonrası satır kalırsa DURUR)."""
    t = pd.to_datetime(X[kol])
    Y = X[t <= kesik].copy()
    if len(Y) and pd.to_datetime(Y[kol]).max() > kesik:
        raise UCHata(f"{ad}: kesik sonrası satır kaldı -> DURDU")
    uclog.info("%s: %d satır, %d kesikten sonra atıldı", ad, len(Y), int(len(X) - len(Y)))
    return Y


def uc_pencere_bayrak(gecerli_idx: pd.DatetimeIndex, t: np.ndarray, olay_gunleri: np.ndarray, bar: int) -> Tuple[np.ndarray, np.ndarray]:
    """Bir hissede: her t için [t'ye kadarki son `bar` geçerli bar] içinde olay günü var mı (bool) ve en son olay günü (NaT).
    Yalnız <= t olan olay günleri sayılır (geleceğe bakma yok; pencere başı = t'den geriye bar-1 geçerli bar)."""
    gi = pd.DatetimeIndex(gecerli_idx).sort_values()
    ev = np.sort(pd.to_datetime(np.asarray(olay_gunleri)).values.astype("datetime64[ns]"))
    t = pd.to_datetime(np.asarray(t)).values.astype("datetime64[ns]")
    bay = np.zeros(len(t), bool); son = np.full(len(t), np.datetime64("NaT"), dtype="datetime64[ns]")
    if not len(ev) or not len(gi):
        return bay, son
    giv = gi.values.astype("datetime64[ns]")
    for k, tt in enumerate(t):
        p = int(np.searchsorted(giv, tt, side="right")) - 1       # t'ye kadarki son geçerli bar
        if p < 0:
            continue
        bas = giv[max(0, p - int(bar) + 1)]
        e = int(np.searchsorted(ev, tt, side="right")) - 1        # t'ye kadarki son olay günü
        if e >= 0 and ev[e] >= bas:
            if ev[e] > tt:
                raise UCHata("pencere bayrağı geleceği gördü")
            bay[k] = True; son[k] = ev[e]
    return bay, son


def uc_taban(n_es: np.ndarray, ust: float = 0.90, alt: float = 0.10) -> Tuple[np.ndarray, np.ndarray]:
    """Olay başına şans tabanı: olay N_es eşle birlikte rastgele sırada (k = olaydan küçük eş sayısı, 0..N_es eşit olasılık), SIRA = k / N_es.
    ÜST: SIRA >= ust <=> k >= tavan(ust N) -> (N - tavan(ust N) + 1) / (N + 1); ALT: SIRA <= alt <=> k <= taban(alt N) -> (taban(alt N) + 1) / (N + 1).
    Tam sayı aritmetiği (ust / alt onda bir katı)."""
    N = np.asarray(n_es, float); out_u = np.full(len(N), np.nan); out_a = np.full(len(N), np.nan)
    ok = np.isfinite(N) & (N >= 1)
    Ni = N[ok].astype(np.int64)
    qu = int(round(ust * 10)); qa = int(round(alt * 10))
    tav = -((-qu * Ni) // 10)                # tavan(qu N / 10)
    tab = (qa * Ni) // 10                    # taban(qa N / 10)
    out_u[ok] = (Ni - tav + 1) / (Ni + 1.0); out_a[ok] = (tab + 1) / (Ni + 1.0)
    return out_u, out_a


def uc_ust_alt(sira: np.ndarray, ust: float = 0.90, alt: float = 0.10) -> Tuple[np.ndarray, np.ndarray]:
    s = np.asarray(sira, float); ok = np.isfinite(s)
    u = np.where(ok, s >= ust - 1e-12, np.nan); a = np.where(ok, s <= alt + 1e-12, np.nan)
    return u.astype(float), a.astype(float)


def uc_n(R: np.ndarray, Y1: np.ndarray, Y2: np.ndarray) -> np.ndarray:
    return np.asarray(R, int) + np.asarray(Y1, int) + np.asarray(Y2, int)


# ================================================================ 1) KAPILAR
def uc_kasa(veri: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    v = veri or UC_YOL["veri"]
    try:
        D = KS._durum_oku(UC_YOL["kasa"])
    except Exception as ex:   # fail-closed
        raise UCHata(f"KASA durumu okunamadı: {type(ex).__name__}: {ex}") from ex
    if str(D.get("acik_kesik")) != "2022-12-31" or D.get("acilan"):
        raise UCHata(f"KASA açık kesik {D.get('acik_kesik')} / açılan {D.get('acilan')} -> DURDU")
    try:
        K = KS.kasa_kapisi([os.path.join(v, "V_ABD.pkl")], "2022-12-31")
    except KS.KasaHata as ex:
        raise UCHata(f"KASA kapısı KAPALI: {ex}") from ex
    return {"kesik": str(K["kesik"]), "muhur_id": D.get("muhur_id"), "dosya": K.get("dosya")}


def uc_kapi(onkayit: Optional[str] = None) -> Dict[str, Any]:
    """Ölçüm kapısı: IZ_KARNE kontrol kapısı + ön kayıttaki KOD_SHA / ESIK_SHA = şimdiki + ön kayıt commit'li ve çalışma ağacında değişmemiş."""
    import IZ_KARNE as IK
    yol = onkayit or os.path.join(UC_YOL["cikti"], UC_DOSYA["onkayit"])
    k = IK.ik_kontrol_kapisi(yol)
    metin = open(yol, encoding="utf-8").read()
    beklenen = {"KOD_SHA": _uc_sha(UC_YOL["kod"]), "ESIK_SHA": uc_esik_sha()}
    for ad, v in beklenen.items():
        if f"{ad}: {v}" not in metin:
            raise UCHata(f"ön kayıt kapısı: {ad} ön kayıtta yok ya da farklı (şimdiki {v[:12]}) -> DURDU")
    rel = os.path.relpath(yol, KOK_UC)
    c = _uc_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise UCHata("ön kayıt commit'li değil -> DURDU")
    if _uc_git(["status", "--porcelain", "--", rel]):
        raise UCHata("ön kayıt çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **beklenen}


# ================================================================ 2) OLAYLAR VE BAYRAKLAR (getirisiz)
def uc_dip_ham(Vd: Dict[str, Any], islem: int = 1) -> Dict[str, Any]:
    """KART_TUR2 fonksiyonlarıyla: Y1 sinyalleri -> P2 / 60 gün tekil Y1 olayı -> F_KT02 (dipte) ve D9 durum ('c' = KT10)."""
    import D9_YENIDEN as D9
    import KART_TUR2 as KT2
    import ORTAK_CETVEL as OC
    t0 = time.time()
    Y = KT2.k2_y1(Vd["V"], islem)["yeni"]
    Pk, P2 = KT2.k2_panel(Vd, UC_ESIK["pazar"])
    P = KT2.k2_P(Pk, Vd, P2)
    Z, say = KT2._k2_oc(Y, P, OC.OC_ESIK["olay"]["tekil_gun"])
    Z = Z.merge(Y[["sembol", "tarih", "F_KT02"]], on=["sembol", "tarih"], how="left", validate="one_to_one")
    K02 = Z[Z.F_KT02.to_numpy(float) == 1.0][["sembol", "tarih", "giris", "d", "j"]].reset_index(drop=True)
    Dd = KT2.k2_d9_durum(Vd, UC_ESIK["pazar"], KT2.K2_ESIK["d9_olay_bas"])
    Cc = D9.d9_satir(Dd, "c")
    Z10, s10 = KT2._k2_oc(Cc[["sembol", "tarih"]], P, 1)
    # KART_TUR2 ölçüm tekili (H = 15) -> D1 karşılaştırması için
    K02_t = K02[KT2.k2_tekil(K02, 15)].reset_index(drop=True)
    K10_t = Z10[KT2.k2_tekil(Z10, 15)].reset_index(drop=True)
    uclog.info("dip ham: Y1 %d sinyal, Y1 olayı %d, KT02 %d, KT10 'c' %d (%.0f sn)", len(Y), len(Z), len(K02), len(Cc), time.time() - t0)
    return {"Y1": Y, "K02": K02, "D9": Dd[["sembol", "tarih", "D9", "ruzgar", "sektor_var"]].copy(), "C": Cc[["sembol", "tarih"]].copy(),
            "K02_t15": K02_t[["sembol", "tarih", "giris"]], "K10_t15": K10_t[["sembol", "tarih", "giris"]], "say": {"y1": say, "kt10": s10}}


def uc_bayrak(K02: pd.DataFrame, H: Dict[str, Any], Vd: Dict[str, Any], veri2: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """KT02 olaylarına R, R_any, Y1, Y2, I22 bayrakları ve ham olay tarihleri. Yalnız t'ye kadar bilgi."""
    import FON_IZI as FI
    import GOZ_ETIKET as GE
    X = K02[["sembol", "tarih"]].copy(); X["tarih"] = pd.to_datetime(X.tarih)
    # R (KT10 'c') ve R_any
    C = H["C"].assign(tarih=lambda x: pd.to_datetime(x.tarih)); C["R"] = 1
    X = X.merge(C.drop_duplicates(["sembol", "tarih"]), on=["sembol", "tarih"], how="left")
    D = H["D9"].assign(tarih=lambda x: pd.to_datetime(x.tarih))
    D = D[D.ruzgar.astype(bool) & D.sektor_var.astype(bool)][["sembol", "tarih"]].drop_duplicates().assign(R_any=1)
    X = X.merge(D, on=["sembol", "tarih"], how="left")
    X["R"] = X.R.fillna(0).astype(int); X["R_any"] = X.R_any.fillna(0).astype(int)
    # Y1: Ç112 S3 blok taban
    S3 = FI.fi_k38_sinyaller(Vd["V"])["S3_blok_taban_yukari"]
    S3 = uc_kes(S3.rename(columns={"gun": "tarih"}), "tarih", "S3 blok taban")
    # Y2: Ç223 T
    U = pd.read_csv(UC_YOL["uyum_toplam"])
    U = U[(U.pazar == UC_ESIK["pazar"]) & (U.PFc <= UC_ESIK["y2"]["PFc_ust"]) & (U.MRc >= UC_ESIK["y2"]["MRc_alt"])]
    U = uc_kes(U, "tarih", "Ç223 T")
    # I22: k30 A1
    A = pd.read_pickle(os.path.join(veri2 or UC_YOL["veri2"], "k30_alim.pkl"))
    A = uc_kes(A, "D", "k30 alım")
    gS = {s: g.tarih.to_numpy() for s, g in S3.groupby("sembol")}
    gU = {s: pd.to_datetime(g.tarih).to_numpy() for s, g in U.groupby("sembol")}
    gA = {s: g.D.to_numpy() for s, g in A.groupby("sembol")}
    bar = int(UC_ESIK["pencere_bar"]); igun = int(UC_ESIK["i22"]["gun"]); ibas = pd.Timestamp(UC_ESIK["i22"]["bas"])
    X["Y1"] = 0; X["Y2"] = 0; X["I22"] = np.nan
    X["y1_gun"] = pd.NaT; X["y2_gun"] = pd.NaT; X["i22_gun"] = pd.NaT
    for s, g in X.groupby("sembol"):
        gi = GE.ge_hazir(Vd["V"][s]).index
        t = g.tarih.to_numpy()
        b1, s1 = uc_pencere_bayrak(gi, t, gS.get(s, np.array([], "datetime64[ns]")), bar)
        b2, s2 = uc_pencere_bayrak(gi, t, gU.get(s, np.array([], "datetime64[ns]")), bar)
        X.loc[g.index, "Y1"] = b1.astype(int); X.loc[g.index, "y1_gun"] = s1
        X.loc[g.index, "Y2"] = b2.astype(int); X.loc[g.index, "y2_gun"] = s2
        ev = np.sort(gA.get(s, np.array([], "datetime64[ns]")).astype("datetime64[ns]"))
        for ix, tt in zip(g.index, pd.to_datetime(t)):
            if tt < ibas:
                continue
            m = ev[(ev <= np.datetime64(tt)) & (ev > np.datetime64(tt - pd.Timedelta(days=igun)))]
            X.loc[ix, "I22"] = float(len(m) > 0)
            if len(m):
                X.loc[ix, "i22_gun"] = m.max()
    for c, k in (("y1_gun", "Y1"), ("y2_gun", "Y2"), ("i22_gun", "I22")):
        x = pd.to_datetime(X[c])
        if (x > X.tarih).any():
            raise UCHata(f"{k}: ham olay günü > t -> DURDU")
    X["N"] = uc_n(X.R, X.Y1, X.Y2)
    for c in ("B", "B0", "I"):
        X[c] = np.nan     # kurulamadı (veri açık dönemi kapsamıyor)
    info = {"S3_satir": int(len(S3)), "T_satir": int(len(U)), "k30_satir": int(len(A)),
            "k30_ilk": str(pd.to_datetime(A.D).min().date()) if len(A) else None}
    return X, info


def uc_olc_olay(X: pd.DataFrame, K02: pd.DataFrame, veri: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any], Dict[str, Any]]:
    """C2.c2_olay (tekil 15) + konum eşi (dışlama: aynı gün bütün KT02 olayları, tekil 1 eşlemesi). Getiri sütunları burada üretilir; hazırlıkta
    yalnız SAYILAR okunur."""
    import CETVEL2 as C2
    Pn = C2.c2_panel22_al(UC_ESIK["pazar"], veri or UC_YOL["veri"], int(UC_ESIK["ufuk"]))
    kol = ["sembol", "tarih", "R", "R_any", "Y1", "Y2", "I22", "N", "B", "B0", "I", "y1_gun", "y2_gun", "i22_gun"]
    S, say = C2.c2_olay(X[kol], Pn, int(UC_ESIK["tekil"]))
    E1, _ = C2.c2_olay(K02[["sembol", "tarih"]], Pn, 1)
    exd = E1.d.to_numpy(np.int64); exj = E1.j.to_numpy(np.int64)
    d = S.d.to_numpy(np.int64); j = S.j.to_numpy(np.int64)
    e = C2.c2_es(Pn, d, j, S.r15.to_numpy(float), exd, exj, es_min=int(UC_ESIK["es_min"]))
    S["es_r15"] = e["es_r15"]; S["n_es"] = e["n_es"]; S["sira"] = e["sira"]; S["fark"] = e["fark"]
    S["donem"] = uc_donem(S.giris)
    tu, ta = uc_taban(S.n_es.to_numpy(float), UC_ESIK["ust_pay"], UC_ESIK["alt_pay"])
    S["taban_ust10"] = np.where(np.isfinite(S.fark), tu, np.nan); S["taban_alt10"] = np.where(np.isfinite(S.fark), ta, np.nan)
    u, a = uc_ust_alt(S.sira.to_numpy(float), UC_ESIK["ust_pay"], UC_ESIK["alt_pay"])
    S["ust10"] = u; S["alt10"] = a
    return S, say, {"Pn": Pn, "exd": exd, "exj": exj}


# ================================================================ 3) PLASEBO (aynı gün, aynı kova, rastgele üye)
def uc_aday_listesi(Pn: Dict[str, Any], d: np.ndarray, j: np.ndarray, exd: np.ndarray, exj: np.ndarray) -> List[np.ndarray]:
    """Her olay için aynı (gün, kova) havuz konumları, KT02 dip olayları hariç."""
    import CETVEL2 as C2
    K = C2.C2_KOVA_SAYI; hk = Pn["h_key"]
    ex = np.zeros(len(hk), bool); pp = Pn["h_pix"][exd, exj]; ex[pp[pp >= 0]] = True
    kv = Pn["KV"][d, j].astype(np.int64); key = d * K + kv
    lo = np.searchsorted(hk, key, "left"); hi = np.searchsorted(hk, key, "right")
    out = []
    for a, b, k in zip(lo, hi, kv):
        if k < 0:
            out.append(np.zeros(0, np.int64)); continue
        r = np.arange(a, b, dtype=np.int64); out.append(r[~ex[r]])
    return out


def uc_plasebo(Pn: Dict[str, Any], S: pd.DataFrame, ctx: Dict[str, Any], tohum: Optional[int] = None) -> Dict[str, Any]:
    """200 tohum: her ölçülen olayın yerine aynı gün aynı kovadan rastgele üye (dip olayı olmayan); üyenin SIRA'sı c2_es ile (dışlanan = dip
    olayları ∪ o tohumun üyeleri). Döner: olay x tohum ÜST10 / ALT10 matrisleri (NaN = aday yok / eşsiz) ve tohum 0 üyeleri (Ö3 eşi)."""
    import CETVEL2 as C2
    T = int(tohum or UC_ESIK["plasebo_tohum"])
    ol = np.isfinite(S.fark.to_numpy(float)); ii = np.nonzero(ol)[0]
    d = S.d.to_numpy(np.int64)[ii]; j = S.j.to_numpy(np.int64)[ii]
    aday = uc_aday_listesi(Pn, d, j, ctx["exd"], ctx["exj"])
    na = np.array([len(a) for a in aday]); var = na > 0
    U = np.full((len(S), T), np.nan); A = np.full((len(S), T), np.nan); uye0 = None
    for t in range(T):
        rng = np.random.default_rng([int(UC_ESIK["plasebo_kok"]), t])
        sec = np.array([a[rng.integers(len(a))] if len(a) else -1 for a in aday], np.int64)
        m = sec >= 0
        rd = Pn["h_d"][sec[m]]; rj = Pn["h_j"][sec[m]]; x = Pn["h_r"][sec[m]]
        e = C2.c2_es(Pn, rd, rj, x, np.r_[ctx["exd"], rd], np.r_[ctx["exj"], rj], es_min=int(UC_ESIK["es_min"]))
        u, a_ = uc_ust_alt(e["sira"], UC_ESIK["ust_pay"], UC_ESIK["alt_pay"])
        U[ii[m], t] = u; A[ii[m], t] = a_
        if t == 0:
            uye0 = pd.DataFrame({"i": ii[m], "d": rd, "j": rj, "r15": x, "es_r15": e["es_r15"]})
    return {"U": U, "A": A, "aday_yok": int((~var).sum()), "uye0": uye0}


# ================================================================ 4) HÜCRE, GRUP, KARAR
def uc_grup_maske(S: pd.DataFrame) -> Dict[str, np.ndarray]:
    R, Y1, Y2, N = (S[c].to_numpy(int) for c in ("R", "Y1", "Y2", "N"))
    G = {"HEPSI": np.ones(len(S), bool)}
    for k, v in (("R", R), ("Y1", Y1), ("Y2", Y2)):
        G[f"{k}=1"] = v == 1; G[f"{k}=0"] = v == 0
    G["R_any=1"] = S.R_any.to_numpy(int) == 1
    i22 = S.I22.to_numpy(float)
    G["I22=1"] = i22 == 1; G["I22=0"] = i22 == 0
    for n in range(4):
        G[f"N={n}"] = N == n
    G["N>=2"] = N >= 2
    G["R∧Y1"] = (R == 1) & (Y1 == 1); G["R∧Y2"] = (R == 1) & (Y2 == 1); G["Y1∧Y2"] = (Y1 == 1) & (Y2 == 1)
    return G


def uc_hucre(S: pd.DataFrame, m: np.ndarray, hc: str, tohum_ek: int, PL: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    import CETVEL2 as C2
    import MACD_UYUM as MU
    mm = m & (S.donem.to_numpy() == hc) & np.isfinite(S.fark.to_numpy(float))
    x = S[mm]; out: Dict[str, Any] = {"n": int(mm.sum())}
    if len(x) < 2:
        out.update({"hukum": "ÖLÇÜLEMEDİ", "fark": float(x.fark.mean()) if len(x) else np.nan})
        return out
    ay = pd.to_datetime(x.giris).dt.strftime("%Y-%m").to_numpy()
    c = C2.c2_hucre(x.r15.to_numpy(float), x.es_r15.to_numpy(float), x.sira.to_numpy(float), x.giris.to_numpy(), "+",
                    tohum_ek=tohum_ek, egri=C2._c2_egri22_al(UC_ESIK["pazar"], hc, int(UC_ESIK["ufuk"]), None))
    c["sira_alt"], c["sira_ust"] = MU.mu_sira_boot(x.sira.to_numpy(float), ay, tohum_ek)
    c["plasebo_gecti"] = True       # plasebo HARİÇ hüküm (ön kayıt)
    hk, neden = MU.mu_hukum(c)
    du = x.ust10.to_numpy(float) - x.taban_ust10.to_numpy(float); da = x.alt10.to_numpy(float) - x.taban_alt10.to_numpy(float)
    ua, uu = MU.mu_sira_boot(du, ay, tohum_ek + 7); aa, au = MU.mu_sira_boot(da, ay, tohum_ek + 11)
    out.update({k: c.get(k) for k in ("fark", "med", "boot_alt", "boot_ust", "sira", "sira_alt", "l3o", "p", "guc", "r15_ort", "es_ort")})
    out.update({"hukum": hk, "neden": neden, "ust10": float(np.mean(x.ust10)), "alt10": float(np.mean(x.alt10)),
                "taban_ust_f": float(np.mean(x.taban_ust10)), "taban_alt_f": float(np.mean(x.taban_alt10)),
                "ust_eksi_taban": float(np.mean(du)), "ust_eksi_taban_alt": ua, "ust_eksi_taban_ust": uu,
                "alt_eksi_taban": float(np.mean(da)), "alt_eksi_taban_alt": aa, "alt_eksi_taban_ust": au,
                "n_es_med": float(np.median(x.n_es))})
    if PL is not None:
        U = PL["U"][mm]; A = PL["A"][mm]
        out["taban_ust_p"] = float(np.nanmean(np.nanmean(U, axis=0))); out["taban_alt_p"] = float(np.nanmean(np.nanmean(A, axis=0)))
        out["ust_eksi_taban_p"] = out["ust10"] - out["taban_ust_p"]; out["alt_eksi_taban_p"] = out["alt10"] - out["taban_alt_p"]
    # Ö3 bilgi
    for c_ in ("h5", "st5", "h5_es", "st5_es", "fark2"):
        if c_ in x.columns:
            out[c_] = float(np.nanmean(x[c_].to_numpy(float))) if np.isfinite(x[c_].to_numpy(float)).any() else np.nan
    yuk = x.es_r15.to_numpy(float) > 0
    out["fark_piy_yukari"] = float(np.mean(x.fark.to_numpy(float)[yuk])) if yuk.any() else np.nan
    out["fark_piy_asagi"] = float(np.mean(x.fark.to_numpy(float)[~yuk])) if (~yuk).any() else np.nan
    out["n_piy_yukari"] = int(yuk.sum())
    return out


def uc_iz_karar(H: Dict[str, Dict[str, Any]], iz: str) -> Dict[str, Any]:
    hucre = list(UC_ESIK["donem"]); kosul, guclu, tutar = {}, {}, {}
    for hc in hucre:
        v, y = H[f"{iz}=1|{hc}"], H[f"{iz}=0|{hc}"]
        f1, f0 = v.get("fark", np.nan), y.get("fark", np.nan)
        uf, up = v.get("ust_eksi_taban", np.nan), v.get("ust_eksi_taban_p", np.nan)
        ok = all(a is not None and np.isfinite(a) for a in (f1, f0, uf, up))
        kosul[hc] = bool(ok and f1 > 0 and f1 - f0 > 0 and uf > 0 and up > 0)
        g = v.get("guc", np.nan)
        guclu[hc] = bool(v.get("n", 0) >= UC_ESIK["n_min"] and g is not None and np.isfinite(g) and g >= UC_ESIK["guc_esik"])
        tutar[hc] = v.get("hukum") == "TUTAR"
    yt = all(kosul.values())
    if yt and all(tutar.values()):
        k = "TUTAR"
    elif yt:
        k = "YÖN TUTARLI"
    elif all(guclu.values()):
        k = "TUTMADI"
    else:
        k = "ÖLÇÜLEMEDİ"
    return {"karar": k, "yon_tutarli": yt, "kosul": kosul, "guclu": guclu, "c2_tutar": tutar}


def uc_birlikte(H: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    hucre = list(UC_ESIK["donem"]); sira, alt, nok = {}, {}, {}
    for hc in hucre:
        f = [H[f"{g}|{hc}"].get("fark", np.nan) for g in ("N=0", "N=1", "N>=2")]
        sira[hc] = bool(all(np.isfinite(f)) and f[0] < f[1] < f[2])
        ba = H[f"N>=2|{hc}"].get("boot_alt", np.nan)
        alt[hc] = bool(ba is not None and np.isfinite(ba) and ba > 0); nok[hc] = bool(np.isfinite(f[2]) and f[2] > 0)
    a, b = hucre
    art = all(sira.values()) and ((alt[a] and nok[b]) or (alt[b] and nok[a]))
    return {"birlikte_artiyor": bool(art), "sira": sira, "boot_alt_pozitif": alt, "nokta_pozitif": nok}


# ================================================================ 5) KOMUTLAR
def uc_hazirla(veri: Optional[str] = None, islem: int = 4, d2: bool = True) -> Dict[str, Any]:
    """Getirisiz: olaylar + bayraklar + sayımlar + D1 / D2 / D3 -> olay.pkl + uc_iz_hazirlik.json."""
    import OLCU_SINAMA as OS
    t0 = time.time(); veri = veri or UC_YOL["veri"]
    kapi = uc_kasa(veri)
    Vd = OS.os_veri(UC_ESIK["pazar"], veri)
    H = uc_dip_ham(Vd, islem)
    X, info = uc_bayrak(H["K02"], H, Vd)
    S, say, ctx = uc_olc_olay(X, H["K02"], veri)
    J: Dict[str, Any] = {"surum": UC_SURUM, "zaman": _uc_simdi(), "kasa": kapi, "kod_sha": _uc_sha(UC_YOL["kod"]), "esik_sha": uc_esik_sha(),
                         "veri_sha": {"V_ABD.pkl": _uc_sha(os.path.join(veri, "V_ABD.pkl")), "uyum_toplam": _uc_sha(UC_YOL["uyum_toplam"]),
                                      "k30_alim.pkl": _uc_sha(os.path.join(UC_YOL["veri2"], "k30_alim.pkl"))},
                         "olay_kaynak": info, "huni": {"y1": H["say"]["y1"], "kt10": H["say"]["kt10"], "c2_olay": say}}
    J["D1"] = uc_d1(H)
    J["sayim"] = uc_sayim(S)
    J["D3"] = uc_d3(X, Vd)
    if d2:
        J["D2"] = uc_d2(veri, X, islem)
    os.makedirs(UC_YOL["gecici"], exist_ok=True)
    pd.to_pickle({"X": X, "K02": H["K02"], "S_anahtar": S[["sembol", "tarih", "giris", "d", "j"]]}, os.path.join(UC_YOL["gecici"], UC_DOSYA["olay"]))
    J["olay_pkl_sha"] = _uc_sha(os.path.join(UC_YOL["gecici"], UC_DOSYA["olay"]))
    J["sure_sn"] = round(time.time() - t0)
    _uc_jyaz(os.path.join(UC_YOL["cikti"], UC_DOSYA["hazirlik"]), J)
    return J


def uc_sayim(S: pd.DataFrame) -> Dict[str, Any]:
    """Getirisiz sayımlar: ölçülebilir (eşli) olaylarda N dağılımı, iz sayıları, çift örtüşmeleri, hücre başına; beklenen güç (n -> güç eğrisi)."""
    import CETVEL2 as C2
    ol = np.isfinite(S.fark.to_numpy(float)); out: Dict[str, Any] = {"olay_c2": int(len(S)), "esli": int(ol.sum())}
    G = uc_grup_maske(S)
    for hc in UC_ESIK["donem"]:
        m = ol & (S.donem.to_numpy() == hc)
        eg = C2._c2_egri22_al(UC_ESIK["pazar"], hc, int(UC_ESIK["ufuk"]), None)
        out[hc] = {g: {"n": int((mk & m).sum()), "guc": C2.c2_guc(int((mk & m).sum()), eg) if (mk & m).sum() else 0.0} for g, mk in G.items()}
    out["dis"] = int((ol & (S.donem.to_numpy() == "dis")).sum())
    x = S[ol]
    out["ortusme"] = {"R_Y1_phi": float(np.corrcoef(x.R, x.Y1)[0, 1]) if x.R.std() and x.Y1.std() else None,
                      "R_Y2_phi": float(np.corrcoef(x.R, x.Y2)[0, 1]) if x.R.std() and x.Y2.std() else None,
                      "Y1_Y2_phi": float(np.corrcoef(x.Y1, x.Y2)[0, 1]) if x.Y1.std() and x.Y2.std() else None}
    return out


def uc_d1(H: Dict[str, Any]) -> Dict[str, Any]:
    """KART_TUR2 açık çıktısıyla (k2_satir, ABD, ufuk 15) KT02 / KT10 olay sayıları ve örtüşme, 2016-01-01 .. 2022-11-30 olay günleri."""
    S = pd.read_csv(UC_YOL["k2_satir"]); a, b = pd.Timestamp("2016-01-01"), pd.Timestamp("2022-11-30")
    out = {}
    for kod, Mine in (("KT02", H["K02_t15"]), ("KT10", H["K10_t15"])):
        T = S[(S.kod == kod) & (S.pazar == "ABD") & (S.ufuk == 15)].copy(); T["tarih"] = pd.to_datetime(T.tarih)
        T = T[(T.tarih >= a) & (T.tarih <= b)]; M = Mine.copy(); M["tarih"] = pd.to_datetime(M.tarih); M = M[(M.tarih >= a) & (M.tarih <= b)]
        ka = set(zip(T.sembol, T.tarih)); km = set(zip(M.sembol, M.tarih)); ortak_s = set(T.sembol) & set(M.sembol)
        Ts = {k for k in ka if k[0] in ortak_s}; Ms = {k for k in km if k[0] in ortak_s}
        yil = lambda Z: {str(y): int(n) for y, n in pd.Series([k[1].year for k in Z]).value_counts().sort_index().items()}  # noqa: E731
        out[kod] = {"k2_acik": len(ka), "uc_iz": len(km), "ortak": len(ka & km), "k2_sembol": int(T.sembol.nunique()),
                    "uc_sembol": int(M.sembol.nunique()), "ortak_sembol": len(ortak_s), "ortak_sembolde_k2": len(Ts), "ortak_sembolde_uc": len(Ms),
                    "ortak_sembolde_ortak": len(Ts & Ms), "yil_k2": yil(ka), "yil_uc": yil(km)}
    return out


def uc_d2(veri: str, X: pd.DataFrame, islem: int) -> Dict[str, Any]:
    """PREFIX: veri bellek içinde kesik tarihinde kesilir, olaylar ve bayraklar baştan hesaplanır; olay günü <= kesik - 30 gün (Y1 S3 / Ç223
    açık dosyası tam veriden) olan olaylar ve R / Y1 / Y2 / I22 aynı olmalı. Ayrıca 30 rastgele olayda Y2 / Y1 ham günü <= t assert."""
    import OLCU_SINAMA as OS
    out: Dict[str, Any] = {}
    for kes in ("2019-06-28", "2021-06-30"):
        k = pd.Timestamp(kes)
        Vk = OS.os_veri(UC_ESIK["pazar"], veri, kesik=k)
        Hk = uc_dip_ham(Vk, islem)
        Xk, _ = uc_bayrak(Hk["K02"], Hk, Vk)
        son = k - pd.Timedelta(days=30)
        A = X[X.tarih <= son][["sembol", "tarih", "R", "Y1", "Y2", "I22"]].reset_index(drop=True)
        B = Xk[Xk.tarih <= son][["sembol", "tarih", "R", "Y1", "Y2", "I22"]].reset_index(drop=True)
        M = A.merge(B, on=["sembol", "tarih"], how="outer", suffixes=("_tam", "_kes"), indicator=True)
        ayni = M[M._merge == "both"]
        fark_b = {c: int((ayni[f"{c}_tam"].fillna(-1) != ayni[f"{c}_kes"].fillna(-1)).sum()) for c in ("R", "Y1", "Y2", "I22")}
        out[kes] = {"tam": int(len(A)), "kesik": int(len(B)), "yalniz_tam": int((M._merge == "left_only").sum()),
                    "yalniz_kesik": int((M._merge == "right_only").sum()), "bayrak_fark": fark_b,
                    "tuttu": bool((M._merge == "both").all() and not any(fark_b.values()))}
        uclog.info("D2 prefix %s: %s", kes, out[kes])
    rng = np.random.default_rng(2511)
    sec = X.iloc[rng.choice(len(X), size=min(30, len(X)), replace=False)]
    ok = True
    for c in ("y1_gun", "y2_gun", "i22_gun"):
        x = pd.to_datetime(sec[c]); ok &= bool(((x <= sec.tarih) | x.isna()).all())
    out["rastgele30_ham_gun_le_t"] = ok
    out["tuttu"] = all(v["tuttu"] for k, v in out.items() if isinstance(v, dict)) and ok
    return out


def uc_d3(X: pd.DataFrame, Vd: Dict[str, Any]) -> Dict[str, Any]:
    """10 rastgele Y1, 10 rastgele Y2, 10 rastgele I22 bayraklı olayda ham satır (elle okunur)."""
    out: Dict[str, Any] = {}
    rng = np.random.default_rng(3311)
    U = pd.read_csv(UC_YOL["uyum_toplam"]); U["tarih"] = pd.to_datetime(U.tarih)
    A = pd.read_pickle(os.path.join(UC_YOL["veri2"], "k30_alim.pkl"))
    for k in ("Y1", "Y2", "I22"):
        Z = X[X[k] == 1]
        Z = Z.iloc[rng.choice(len(Z), size=min(10, len(Z)), replace=False)] if len(Z) else Z
        sat = []
        for r in Z.itertuples():
            v = {"sembol": r.sembol, "t": str(r.tarih.date())}
            if k == "Y1":
                d = Vd["V"][r.sembol]; g = pd.Timestamp(r.y1_gun); i = d.index.get_loc(g)
                med = float(d.Volume.iloc[max(0, i - 20):i].median()); rr = float(d.Close.iloc[i] / d.Close.iloc[i - 1] - 1)
                v.update({"s3_gun": str(g.date()), "hacim": float(d.Volume.iloc[i]), "med20": med, "kat": float(d.Volume.iloc[i] / med) if med else None,
                          "getiri": rr, "bar_farki": int(np.searchsorted(d.index, r.tarih) - i)})
            elif k == "Y2":
                u = U[(U.pazar == "ABD") & (U.sembol == r.sembol) & (U.tarih == pd.Timestamp(r.y2_gun))]
                v.update({"T_gun": str(pd.Timestamp(r.y2_gun).date()), "PFc": float(u.PFc.iloc[0]) if len(u) else None,
                          "MRc": float(u.MRc.iloc[0]) if len(u) else None})
            else:
                a = A[(A.sembol == r.sembol) & (A.D == pd.Timestamp(r.i22_gun))]
                v.update({"D": str(pd.Timestamp(r.i22_gun).date()), "deger": float(a.deger.iloc[0]) if len(a) else None,
                          "rol": str(a.rol.iloc[0]) if len(a) else None, "acc": str(a.ACCESSION_NUMBER.iloc[0]) if len(a) else None})
            sat.append(v)
        out[k] = sat
    return out


def uc_kos(veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    """Kapı -> olay.pkl (hazırlıktaki sha) -> ölçüm -> satır / sonuç dosyaları."""
    import CETVEL2 as C2
    t0 = time.time(); bas = _uc_simdi(); veri = veri or UC_YOL["veri"]; cikti = cikti or UC_YOL["cikti"]
    if os.path.exists(os.path.join(cikti, UC_DOSYA["sonuc"])):
        raise UCHata("sonuç zaten var (ikinci koşu DURUR)")
    G0 = uc_kapi(os.path.join(cikti, UC_DOSYA["onkayit"]))
    kapi = uc_kasa(veri)
    Hz = json.load(open(os.path.join(cikti, UC_DOSYA["hazirlik"]), encoding="utf-8"))
    yol = os.path.join(UC_YOL["gecici"], UC_DOSYA["olay"])
    if _uc_sha(yol) != Hz["olay_pkl_sha"]:
        raise UCHata("olay.pkl hazırlıktaki sha ile aynı değil -> DURDU")
    O = pd.read_pickle(yol)
    S, say, ctx = uc_olc_olay(O["X"], O["K02"], veri)
    if not S[["sembol", "tarih", "giris", "d", "j"]].reset_index(drop=True).equals(O["S_anahtar"].reset_index(drop=True)):
        raise UCHata("olay anahtarları hazırlıktakiyle aynı değil -> DURDU")
    Pn = ctx["Pn"]
    PL = uc_plasebo(Pn, S, ctx)
    # Ö3: h5 / stop (C2.c2_bilgi); eş = plasebo tohum 0 üyesi
    B = C2.c2_bilgi(Pn, S); S["h5"] = B.h5.to_numpy(float); S["st5"] = B.st5.to_numpy(float)
    u0 = PL["uye0"]
    if u0 is not None and len(u0):
        Xu = pd.DataFrame({"sembol": np.asarray(Pn["P"]["sembol"])[u0.j.to_numpy(int)], "tarih": Pn["P"]["tarih"][u0.d.to_numpy(int)],
                           "giris": Pn["P"]["tarih"][u0.d.to_numpy(int)], "d": u0.d.to_numpy(int), "j": u0.j.to_numpy(int),
                           "hat": Pn["HAT"][u0.d.to_numpy(int), u0.j.to_numpy(int)], "atr": Pn["ATR"][u0.d.to_numpy(int), u0.j.to_numpy(int)]})
        Bu = C2.c2_bilgi(Pn, Xu)
        S["h5_es"] = np.nan; S["st5_es"] = np.nan
        S.loc[S.index[u0.i.to_numpy(int)], "h5_es"] = Bu.h5.to_numpy(float); S.loc[S.index[u0.i.to_numpy(int)], "st5_es"] = Bu.st5.to_numpy(float)
    # ikinci eş (bilgi): aynı gün N = 0 dip olaylarının ortalaması (kendisi hariç)
    f = np.isfinite(S.r15.to_numpy(float)); z = f & (S.N.to_numpy(int) == 0)
    gs = pd.Series(np.where(z, S.r15, 0.0)).groupby(S.d.to_numpy()).transform("sum").to_numpy()
    gn = pd.Series(z.astype(float)).groupby(S.d.to_numpy()).transform("sum").to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        es2 = (gs - np.where(z, S.r15, 0.0)) / (gn - z.astype(float))
    S["es2_r15"] = np.where(f & np.isfinite(es2), es2, np.nan); S["fark2"] = S.r15 - S.es2_r15
    # hücreler
    Gm = uc_grup_maske(S); H: Dict[str, Dict[str, Any]] = {}
    for gi, (g, m) in enumerate(Gm.items()):
        for hi, hc in enumerate(list(UC_ESIK["donem"]) + ["dis"]):
            H[f"{g}|{hc}"] = uc_hucre(S, m, hc, 500000 + gi * 10 + hi, PL)
    # TUTAR hücrede c2_plasebo
    for k, c in H.items():
        if c.get("hukum") == "TUTAR":
            g, hc = k.split("|"); mm = Gm[g] & (S.donem.to_numpy() == hc) & np.isfinite(S.fark.to_numpy(float))
            pl = C2.c2_plasebo(Pn, S.d.to_numpy(np.int64)[mm], "+", C2._c2_egri22_al("ABD", hc, 15, None), tohum_ek=777, iki_yon_ayri=True)
            c["c2_plasebo"] = {"fark_ort": pl["fark_ort"], "tutar_pay_arti": pl["tutar_pay_arti"], "gecti_arti": pl["gecti_arti"]}
    K = {iz: uc_iz_karar(H, iz) for iz in UC_ESIK["iz"]}
    Bk = uc_birlikte(H)
    yt = [iz for iz in UC_ESIK["iz"] if K[iz]["yon_tutarli"]]
    aday = len(yt) >= 2 and Bk["birlikte_artiyor"]
    def _p(c: Dict[str, Any]) -> float:
        v = c.get("p", np.nan)
        return float(v) if (v is not None and np.isfinite(v) and c.get("n", 0) >= UC_ESIK["n_min"]) else 1.0
    ps = [max(_p(H[f"{iz}=1|{hc}"]) for hc in UC_ESIK["donem"]) for iz in UC_ESIK["iz"]]
    ps.append(max(_p(H[f"N>=2|{hc}"]) for hc in UC_ESIK["donem"]))
    bh = C2.c2_bh(ps, UC_ESIK["bh_q"])
    # satır dosyası
    kol = ["sembol", "tarih", "giris", "donem", "R", "R_any", "Y1", "Y2", "B", "B0", "I", "I22", "N", "r15", "es_r15", "n_es", "sira", "fark",
           "taban_ust10", "taban_alt10", "ust10", "alt10", "es2_r15", "fark2", "h5", "st5", "h5_es", "st5_es", "y1_gun", "y2_gun", "i22_gun"]
    Ss = S[[c for c in kol if c in S.columns]].copy()
    Ss["plasebo_ust10"] = np.nanmean(PL["U"], axis=1); Ss["plasebo_alt10"] = np.nanmean(PL["A"], axis=1)
    for c in ("tarih", "giris", "y1_gun", "y2_gun", "i22_gun"):
        Ss[c] = pd.to_datetime(Ss[c]).dt.strftime("%Y-%m-%d")
    en_gec = max(pd.to_datetime(Ss.giris).max(), pd.to_datetime(Ss.tarih).max())
    if en_gec > UC_KESIK:
        raise UCHata(f"KESİK AŞIMI: {en_gec}")
    ys = os.path.join(cikti, UC_DOSYA["satir"])
    Ss.to_csv(ys, index=False, compression={"method": "gzip", "mtime": 0}, float_format="%.10g")
    J = {"surum": UC_SURUM, "baslangic": bas, "bitis": _uc_simdi(), "sure_sn": round(time.time() - t0), "kapi": G0, "kasa": kapi,
         "huni": say, "plasebo_aday_yok": PL["aday_yok"], "hucre": H, "iz_karar": K, "birlikte": Bk, "yon_tutarli": yt, "kasa_adayi": bool(aday),
         "bh": {"aile": UC_ESIK["iz"] + ["N>=2"], "p": ps, "gecti": bh}, "satir_sha": _uc_sha(ys), "en_gec": str(en_gec.date())}
    _uc_jyaz(os.path.join(cikti, UC_DOSYA["sonuc"]), J)
    uclog.info("bitti: kasa adayı %s, yön tutarlı %s, birlikte %s (%.0f sn)", aday, yt, Bk["birlikte_artiyor"], time.time() - t0)
    return J


# ================================================================ 6) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_uc(_once=_CK_ONCE_UC, _dosya="UC_IZ.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_UC",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_uc()


def _uc_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="UC_IZ: üç iz aynı dip olayında")
    ap.add_argument("komut", choices=["hazirla", "kos", "sha"])
    ap.add_argument("--veri", default=None); ap.add_argument("--islem", type=int, default=4); ap.add_argument("--d2_yok", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.komut == "sha":
            print(json.dumps({"KOD_SHA": _uc_sha(UC_YOL["kod"]), "ESIK_SHA": uc_esik_sha()}, indent=1))
        elif a.komut == "hazirla":
            J = uc_hazirla(a.veri, a.islem, d2=not a.d2_yok)
            print(json.dumps(_uc_json({k: J[k] for k in ("D1", "sayim", "olay_kaynak") if k in J}), ensure_ascii=False)[:6000])
        else:
            J = uc_kos(a.veri)
            print(json.dumps(_uc_json({k: J[k] for k in ("iz_karar", "birlikte", "kasa_adayi", "bh")}), ensure_ascii=False)[:6000])
    except UCHata as ex:
        uclog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_uc_ana())
