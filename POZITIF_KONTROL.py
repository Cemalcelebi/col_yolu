"""POZITIF_KONTROL — 15 bar cetveli bilinen bir izi görebiliyor mu? (20 Kasım 2026; iş tanımı
arastirma_cikti/pozitif_kontrol/POZITIF_KONTROL_IS_TANIMI.md). Bu modül cetveli SINAR, iz aramaz.

CETVEL SABİT: DUSUS_SONRASI (ds_hazirla, ds_olc, ds_es_topla, ds_hucre, ds_perm_p; DS_ESIK) ve YAPI_HEDEF 15 bar makinesi (yh_sim,
yh_getiri, yh_d1_hucre, yh_d3_boot_l3o, yh_d3_guc; YH_ESIK) ve ORTAK_CETVEL (oc_veri, oc_panel, oc_olay_hazirla, oc_esli) AYNEN içe alınır;
KOPYA ya da değişiklik YOK. Kod sha'ları DS_ON_KAYIT.md'deki ile eşit olmalı (kapı denetler).

A. YAPAY İZ: DS ANA olay kümesi (ds_esik.json ile ds_hazirla; DS koşusundaki küme) üzerinde rastgele 'tutan' alt küme seçilir; yalnız o
   olayların giriş barından itibaren 15 geçerli barının Close / High / Low'u çarpımsal sürüklenmeyle (k. geçerli bar x (1 + delta x (k+1)/15))
   değiştirilip yh_sim ile yeniden ölçülür; eşler (DS içi, F == 0) dokunulmaz. ds_hucre aynen: FARK, boot, güç, p. Yakalama = FARK > 0 VE
   boot %95 alt > 0 VE p (tek yönlü '+') < 0,05. delta = 0 plasebodur (yanlış pozitif payı).
B. BİLİNEN İZ: (B1) 12-1 momentum (ay sonu, üst / alt onda); (B2) bilanço sonrası sürüklenme (sec_ozet 8-K 2.02; 2 günlük artık tepki üst / alt
   onda, eşikler eğitimden). Aynı ds_olc / ds_hucre ile 15 bar h5 FARK; aynı olay + aynı eşlerde stop'suz 15 bar kapanış getirisi farkı;
   OC r60 eşli fark (oc_esli). Üç cetvel yan yana.
C. ÖRNEKLER: TEHOL / BINBN / KTLEV (BIST; S6 'al' ya da 120 gün üst sınır kırılımı) ve Ekim 2026 kazananları (ESLER_2026-10-22 giriş günü).

Komut:  python POZITIF_KONTROL.py onkayit            ön kayıt (PK_ESIK sha, kod sha, cetvel sha = DS ön kaydı, kontrol listesi)
        python POZITIF_KONTROL.py kos [--islem 4]    kapı -> A + B + C -> pozitif_kontrol.json, satır dosyaları, POZITIF_KONTROL_RAPOR.md
        python POZITIF_KONTROL.py rapor              pozitif_kontrol.json -> POZITIF_KONTROL_RAPOR.md
Colab:  exec(open('POZITIF_KONTROL.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_ABD.pkl, V_AVR.pkl, V_BIST.pkl (islenmis-veri); /tmp/k55/sec_ozet.json + sembol_cik.json (K55.veri_paket.ac);
        C Ekim kazananları /tmp/veri_canli/V_ABD.pkl (19 Kas 2026'ya kadar; kriz kesiği yalnız C bilgi satırında aşılır).
Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_PK = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_PK = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_PK not in sys.path:
    sys.path.insert(0, KOK_PK)

import DUSUS_SONRASI as DS  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

pklog = logging.getLogger("col.pozitif_kontrol")
if not pklog.handlers:
    _pk_h = logging.StreamHandler(sys.stderr)
    _pk_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s pozitif_kontrol: %(message)s", "%H:%M:%S"))
    pklog.addHandler(_pk_h)
    pklog.setLevel(logging.INFO)
    pklog.propagate = False

PK_SURUM = "POZITIF_KONTROL v1.0 (2026-11-20): 15 bar cetveli pozitif kontrol (yapay iz, momentum 12-1, bilanço sonrası sürüklenme, örnekler)"
PK_YOL = {"cikti": os.path.join(KOK_PK, "arastirma_cikti", "pozitif_kontrol"), "veri": os.environ.get("PK_VERI", "/tmp/veri"),
          "canli": os.environ.get("PK_CANLI", "/tmp/veri_canli"), "k55": os.environ.get("PK_K55", "/tmp/k55"),
          "kod": os.path.join(KOK_PK, "POZITIF_KONTROL.py"),
          "ds_cikti": os.path.join(KOK_PK, "arastirma_cikti", "dusus_sonrasi")}
PK_DOSYA = {"onkayit": "POZITIF_KONTROL_ON_KAYIT.md", "json": "pozitif_kontrol.json", "rapor": "POZITIF_KONTROL_RAPOR.md",
            "a_satir": "pk_a_hucre.csv.gz", "b_satir": "pk_b_olay.csv.gz", "c_satir": "pk_c_ornek.csv"}

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
PK_ESIK: Dict[str, Any] = {
    "surum": "PK1.0",
    "cetvel": "DUSUS_SONRASI ds_olc / ds_es_topla / ds_hucre / ds_perm_p (DS_ESIK: boot 2000 ay kümeli, güç delta 0,05 R 1000, perm 10000) + "
              "YAPI_HEDEF yh_sim / yh_getiri (YH_ESIK['olcu']: ufuk 15, hedef +%5 / +%10 kapanışla, stop0 = hat x 0,98, kilit / takip) AYNEN; "
              "hat = son 20 geçerli bar en düşük Low (t dahil); giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla); eş = aynı "
              "giriş günü, aynı kova (ATRP tercili x OC likidite üçlüsü), özelliği 0, 15 barı ölçülebilir, olayın stop uzaklığı d ile; en az 3",
    "alfa": 0.05,
    "donem": {"egitim": ["2016-01-01", "2022-12-31"], "sinama": ["2023-01-01", "2026-08-31"],
              "not": "A: DS dönemleri ve ambargosu AYNEN (ds_esik.json). B: ambargo yok (eşikler sonuç kullanmaz: momentum kesitsel sıra; PEAD "
                     "onda sınırları eğitim tepkilerinden, getirisiz)"},
    "A": {"pazar": ["ABD", "AVR"], "hucre": ["egitim", "sinama"], "n": [30, 100, 300, 1000, "yari"], "delta": [0.0, 0.01, 0.02, 0.03, 0.05],
          "tohum_sayi": 20, "tohum": 3101, "ufuk": 15, "n_azami_pay": 2 / 3,
          "olay": "DS ANA olayları (ds_hazirla(pazar, esik_json = ds_esik.json) + ds_olc; DS koşusundaki küme ve eşler), h5 ölçülebilir ve DS içi "
                  "eşi (>= 3) olan olaylar havuzu; her tohum x n x hücre: havuzdan yerine koymadan n 'tutan' (yari = havuzun yarısı); öteki "
                  "olaylar F = 0 (eş adayı)",
          "surukleme": "yalnız tutan olayların penceresi (birleşik takvim, giriş barı satır 0, 30 satır): k. geçerli bar (k = 0 giriş barı) "
                       "Close / High / Low x (1 + delta x min(k + 1, 15) / 15); açılış (giriş fiyatı) ve stop0 değişmez; yh_sim yeniden; "
                       "eşler, taban ve güç tabanı (es_h5_hepsi) DOKUNULMAZ",
          "yakala": "FARK > 0 VE boot %95 alt > 0 VE p (ds_perm_p, tek yönlü '+') < 0,05; bilgi: iki yönlü p ile aynı şart; dört hücre "
                    "(ABD + AVR x eğitim + sınama) birlikte yakalama (aynı tohum)",
          "plasebo": "delta = 0: yanlış pozitif payı (beklenen tek yönlü <= %5)"},
    "B": {"pazar": ["ABD"], "bilgi_pazar": ["AVR"], "onda": [0.10, 0.90],
          "B1": {"ad": "12-1 momentum", "olay": "ay sonu t = birleşik takvimde ayın son işlem günü; MOM_12_1 = C(t-21) / C(t-252) - 1 (hissenin "
                                               "kendi geçerli barları, t'de geçerli bar, >= 252 bar geçmiş); OC.oc_olay_hazirla (havuz, giriş "
                                               "t+1 açılış) sonrası aynı t'deki hisseler arasında sıra (rank first, pct): üst onda (> 0,90) U, "
                                               "alt onda (<= 0,10) A; ötekiler orta (eş adayı)",
                 "yon": {"U": "+", "A": "-", "UA": "+"}},
          "B2": {"ad": "bilanço sonrası sürüklenme (PEAD)", "kaynak": "sec_ozet 8-K madde 2.02 başvuru tarihleri (K55)",
                 "olay": "bilgi barı b0 = başvuru gününden SONRAKİ ilk geçerli bar (DS sınıf II ile aynı); t = b0; tepki = C(b0) / C(b0-2) - 1 - "
                         "(E(b0) / E(b0-2) - 1), E = evren eşit ağırlık endeksi (DS.ds_baglam); aynı (hisse, t) bir kez; onda sınırları "
                         "eğitim (giriş 2016-22) olaylarının tepkisinden (getirisiz) q10 / q90; U = tepki >= q90, A = tepki <= q10; ANA = "
                         "U ya da A, aynı hissede >= 15 birleşik takvim günü arayla ilk; eş adayı = aynı giriş günü havuzdaki öteki hisseler",
                 "yon": {"U": "+", "A": "-", "UA": "+"}},
          "kod": "F_<B>U: U = 1, A = NaN, öteki = 0 (eş = orta); F_<B>A: A = 1, U = NaN, öteki = 0; F_<B>UA: U = 1, A = 0, öteki NaN (doğrudan "
                 "üst - alt; eş = aynı gün aynı kova alt onda)",
          "kova": "ATRP tercili (ATR14 / C, t; tercil sınırları eğitim ANA olaylarından) x OC likidite üçlüsü (H[d] % 3) - DS ile aynı",
          "uc_cetvel": "(1) 15 bar h5 FARK (ds_hucre); (2) aynı olay ve AYNI eşlerde stop'suz 15 bar kapanış getirisi r15 = C(15. geçerli bar) "
                       "/ giriş açılışı - 1, fark = r15 - eş ort r15; (3) OC r60 eşli fark (oc_esli: aynı gün, aynı momentum beşliği x "
                       "likidite üçlüsü). Hepsi aynı istatistik: ay kümeli boot (yh_d3_boot_l3o) ve ay kümeli işaret permütasyonu (ds_perm_p) "
                       "önceden yazılı yönle; U - A yayılımı ay kümeli ortak bootstrap",
          "olcu_birim": "h5 FARK yüzde puan (+%5 stop'tan önce payı farkı); r15 ve r60 farkı getiri yüzdesi"},
    "C": {"bist": [["TEHOL-24", "TEHOL", "2024-12-12"], ["TEHOL-25", "TEHOL", "2025-05-28"], ["BINBN-24", "BINBN", "2025-01-21"],
                   ["KTLEV-24", "KTLEV", "2024-10-15"]],
          "bist_kural": "sinyal günü = kutu sonu (Cemal etiketi, FON_IZI FI_K18_VAKA / CEMAL_COL_KURALLARI) - 5 .. + 60 geçerli bar penceresinde "
                        "ilk S6 'al' günü (YH.yh_s6_hisse; hat = Y1 hattı: kutu_alt ya da DİP(t-1)); yoksa ilk C_t > max(H, t-120 .. t-1) "
                        "günü (hat = son 20 bar en düşük Low); ikisi de yoksa 'sinyal yok'. 'KETLV' veride KTLEV",
          "ekim": [["CAPR", "2026-10-22", "ALKT", 15.08, 13.28], ["ARRY", "2026-10-21", "RARE", 16.02, 13.80],
                   ["AXGN", "2026-10-22", "ALKT", 15.08, 13.28], ["TDOC", "2026-10-21", "RARE", 16.02, 13.80],
                   ["JBLU", "2026-10-23", "FNF", 41.24, 37.69], ["LQDA", "2026-10-23", "FNF", 41.24, 37.69]],
          "ekim_kural": "giriş = ESLER_2026-10-22 giriş günü açılışı; t = önceki geçerli bar; (a) kendi hattı: hat = son 20 bar en düşük Low "
                        "(t dahil), stop0 = hat x 0,98; (b) ESLER geometrisi: stop0 = giriş x (1 - adayın d), d = 1 - aday stop0 / aday giriş "
                        "(CANLI_SONUC); veri /tmp/veri_canli (kriz kesiği yalnız bu bilgi satırında aşılır)"},
    "yeniden_uretim": {"A": ["ABD", "sinama", 300, 0.03, 0], "B": ["B1U", "sinama"], "elle_n": 50, "elle_es_n": 5, "tohum": 3109},
}

PK_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = DS ile aynı: aynı giriş günü, aynı kova (ATRP tercili x OC likidite üçlüsü), F == 0, olayın d'si ile aynı 15 bar kuralı "
                   "(ds_olc / ds_es_topla, kopya yok); A'da sürüklenme yalnız tutan olayın kendi penceresine eklenir, eşler dokunulmaz; B'de U ve A "
                   "orta eşlere karşı ayrı + doğrudan U-A; mekanik üstünlük: sürüklenme dışında olay ile eş aynı süreçten (A plasebo delta 0)"),
    "K2": ("EVET", "MOM t'de bitmiş barlardan (t-21, t-252); PEAD tepkisi b0 kapanışına kadar, giriş b0+1 açılışı; PEAD onda sınırları eğitimden "
                   "(getirisiz) sabit; ATRP / hat t'de; test_pozitif_kontrol prefix: veri t'de kesilince MOM / tepki / ATRP / hat aynı"),
    "K3": ("EVET", "OC.oc_veri_hazirla (H > L, V > 0, O/H/L/C > 0) + DS açılış kırpması (ds_veri); 15 bar yalnız geçerli barlar (yh_sim); "
                   "sinyal günü geçerli bar (oc_olay_hazirla)"),
    "K4": ("EVET", "A: DS ANA olayları (15 gün tekil); B1 ay sonu (aynı hissede >= ~21 bar arayla); B2 ANA >= 15 bar arayla, aynı (hisse, t) bir "
                   "kez; n = ölçülen olay; boot / permütasyon birimi giriş ayı; medyan raporda (B)"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar açılışı (oc_olay_hazirla d; yh_sim satır 0); C Ekim: ESLER giriş günü açılışı"),
    "K6": ("EVET", "V_*.pkl tek kip (fi_k1_veri düzeltilmiş); oranlar birimsiz; AVR likidite x Kur; geçmiş bölünme şüphesi havuz dışı (OC); C Ekim "
                   "verisi /tmp/veri_canli aynı kip (CANLI_SONUC ile aynı kaynak)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (V_ABD 1.411, V_AVR 580); yanlılık hem olaya hem eşe; raporda yazılır; A'da sürüklenme "
                   "bilinen değer olduğu için yanlılıktan bağımsız"),
    "K8": ("EVET", "A: 20 tohum x 5 n x 5 delta x 2 pazar x 2 hücre, n 30..yarı; B: eğitim 2016-22 / sınama 2023-26 ayrı; n < 30 hücre "
                   "ÖLÇÜLEMEDİ yazılır; C n = 1 / örnek: bulgu denmez, tek tek okunur"),
    "K9": ("EVET", "POZITIF_KONTROL_ON_KAYIT.md: PK_ESIK sha, kod sha, cetvel sha'ları (DS_ON_KAYIT ile eşit), veri sha; pk_kapi ön kayıt git'te "
                   "işlenmiş ve değişmemiş + ik_kontrol_kapisi denetler; tasarım iş tanımından (commit 4505d5c) önce yazıldı, sonuç görülmeden"),
    "K10": ("EVET", "sec_ozet 8-K madde alanı virgülle ayrılır (DS._ds_sec_olay ile aynı ayrıştırma, kopya yok); bilgi barı başvuru günü sonrası "
                    "ilk geçerli bar; 3 ham satır ön kayıtta gösterilir"),
    "K11": ("EVET", "A bir hücre (ABD sınama n 300 delta +%3 tohum 0) ve B bir hücre (B1U sınama) satır dosyasından düz pandas ile; A'da 50 tutan "
                    "olayın sürüklenmiş h5'i, B'de 50 olayın h5 / r15'i ve 5 olayın eş h5'i yh_sim'den bağımsız düz döngüyle"),
    "K12": ("EVET", "bu iş cetvel sınaması; 'iz' iddiası yok; yakalama payı, FARK ve p ayrı; sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_pk; pk_ / PK_ önekleri dışında ezme DURUR; test); DS / YH / OC değişmedi (sha = DS ön "
                    "kaydı); defter dosyalarına dokunulmadı; e-posta / anahtar taraması (YH._yh_yaz); dış servis yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; cetvel sınaması"),
}


class PKHata(RuntimeError):
    """Durdurucu hata: veri yok, mühür / sha tutmuyor, cetvel değişmiş, yeniden üretim tutmadı."""


# ================================================================ 0) ORTAK
def _pk_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def pk_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return YH.yh_esik_sha(PK_ESIK if E is None else E)


def _pk_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or PK_YOL["cikti"], PK_DOSYA.get(ad, ad))


def _pk_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _pk_kay(x: np.ndarray, k: int) -> np.ndarray:
    return YH._yh_kaydir(np.asarray(x, float), k)


def pk_seri(df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """Hissenin (t) ATRP'si (DS ile aynı: ATR14 / C, TR önceki kapanışla) ve hattı (son 20 geçerli bar en düşük Low, t dahil)."""
    H, L, C = (df[k].to_numpy(float) for k in ("High", "Low", "Close"))
    pC = _pk_kay(C, 1)
    TR = np.where(np.isfinite(pC), np.maximum(H, pC) - np.minimum(L, pC), H - L)
    atrp = pd.Series(TR).rolling(14, min_periods=14).mean().to_numpy() / C
    hat = pd.Series(L).rolling(DS.DS_ESIK["olay"]["hat_gun"], min_periods=DS.DS_ESIK["olay"]["hat_gun"]).min().to_numpy()
    return pd.Series(atrp, index=df.index), pd.Series(hat, index=df.index)


def pk_surukle(Cr: np.ndarray, Hr: np.ndarray, Lr: np.ndarray, delta: float, ufuk: int = 15) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Pencere (R, K), satır 0 = giriş günü; geçerli bar = Close sonlu. k. geçerli bar (k = 0 giriş barı) fiyatları x (1 + delta x min(k+1, ufuk) / ufuk)."""
    Cr = np.asarray(Cr, float); v = np.isfinite(Cr)
    k = np.cumsum(v, axis=0) - 1
    f = np.where(v, 1.0 + float(delta) * np.minimum(k + 1, ufuk) / float(ufuk), 1.0)
    return Cr * f, np.asarray(Hr, float) * f, np.asarray(Lr, float) * f


def _pk_pencere(A: np.ndarray, d: np.ndarray, j: np.ndarray, R: int) -> np.ndarray:
    """(R, K): A[d + r, j] (taşan satır NaN)."""
    n = A.shape[0]; r = d[None, :] + np.arange(R)[:, None]
    out = A[np.minimum(r, n - 1), j[None, :]].astype(float)
    out[r >= n] = np.nan
    return out


def pk_istat(val: np.ndarray, es: np.ndarray, giris: Any, yon: str, tohum_ek: int) -> Dict[str, Any]:
    """Olay değeri ile eş ortalaması farkı: n, ort, medyan fark, ay kümeli boot (yh_d3_boot_l3o), p (ds_perm_p) yönlü ve iki yönlü."""
    g = pd.DataFrame({"h5": np.asarray(val, float), "es_h5": np.asarray(es, float), "giris": pd.to_datetime(np.asarray(giris))})
    g = g[np.isfinite(g.h5) & np.isfinite(g.es_h5)]
    n = int(len(g))
    if n == 0:
        return {"n": 0, "olay": np.nan, "es": np.nan, "fark": np.nan, "med": np.nan, "boot_alt": np.nan, "boot_ust": np.nan,
                "p": np.nan, "p_iki": np.nan}
    b = YH.yh_d3_boot_l3o(g, g.assign(h5=g.es_h5), DS.DS_ESIK, tohum_ek=tohum_ek)
    R, t0 = int(DS.DS_ESIK["perm"]["R"]), int(DS.DS_ESIK["perm"]["tohum"]) + int(tohum_ek)
    return {"n": n, "olay": float(g.h5.mean()), "es": float(g.es_h5.mean()), "fark": float((g.h5 - g.es_h5).mean()),
            "med": float((g.h5 - g.es_h5).median()), "boot_alt": b["boot_alt"], "boot_ust": b["boot_ust"],
            "p": DS.ds_perm_p(g, yon, R, t0), "p_iki": DS.ds_perm_p(g, "?", R, t0)}


def pk_yayilim(gU: pd.DataFrame, gA: pd.DataFrame, tohum_ek: int) -> Dict[str, float]:
    """U - A yayılımı (her biri olay - eş ortalaması) için ay kümeli ortak bootstrap (aylar birlikte çekilir)."""
    def ay(g):
        g = g[np.isfinite(g.h5) & np.isfinite(g.es_h5)]
        return pd.DataFrame({"s": (g.h5 - g.es_h5).to_numpy(float), "n": 1.0,
                             "ay": pd.to_datetime(g.giris).dt.strftime("%Y-%m").to_numpy()}).groupby("ay")[["s", "n"]].sum()
    U, A = ay(gU), ay(gA)
    if not len(U) or not len(A):
        return {"yayilim": np.nan, "alt": np.nan, "ust": np.nan}
    ix = U.index.union(A.index); U = U.reindex(ix, fill_value=0.0); A = A.reindex(ix, fill_value=0.0)
    su, nu, sa, na = (x.to_numpy(float) for x in (U.s, U.n, A.s, A.n))
    B = int(DS.DS_ESIK["boot"]["B"]); rng = np.random.default_rng([int(DS.DS_ESIK["boot"]["tohum"]), 7000 + int(tohum_ek)])
    W = rng.multinomial(len(ix), np.full(len(ix), 1.0 / len(ix)), size=B).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        mb = (W @ su) / (W @ nu) - (W @ sa) / (W @ na)
    mb = mb[np.isfinite(mb)]
    return {"yayilim": float(su.sum() / nu.sum() - sa.sum() / na.sum()),
            "alt": float(np.quantile(mb, 0.025)) if len(mb) else np.nan, "ust": float(np.quantile(mb, 0.975)) if len(mb) else np.nan}


def _pk_yakala(c: Dict[str, Any], p: float) -> bool:
    a = float(PK_ESIK["alfa"])
    return bool(np.isfinite(c.get("fark", np.nan)) and c["fark"] > 0 and np.isfinite(c.get("boot_alt", np.nan)) and c["boot_alt"] > 0
                and np.isfinite(p) and p < a)


# ================================================================ 1) A: YAPAY İZ
_PK_A: Dict[str, Any] = {}


def pk_a_hazirla(pazar: str, islem: int = 1, veri: Optional[str] = None, esik_json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """DS ANA olay kümesi + eşler (ds_hazirla + ds_olc, DS koşusuyla aynı) ve her delta için tutan olay olsaydı sürüklenmiş h5 / st5 / h10."""
    t0 = time.time()
    if esik_json is None:
        yol = os.path.join(PK_YOL["ds_cikti"], DS.DS_DOSYA["esik"])
        if not os.path.exists(yol):
            raise PKHata(f"ds_esik.json yok: {yol}")
        esik_json = json.load(open(yol, encoding="utf-8"))
    H = DS.ds_hazirla(pazar, islem, esik_json, veri)
    A, Cd = DS.ds_olc(H["X"], H["P"], H["Vd"], H["Z"], islem)
    P = H["P"]; Cl = YH.yh_kapanis(P, H["Vd"]); R = int(YH.YH_ESIK["olcu"]["pencere_azami"])
    d = A.d.to_numpy(int); j = A.j.to_numpy(int)
    Cr, Hr, Lr = _pk_pencere(Cl, d, j, R), _pk_pencere(P["Hi"], d, j, R), _pk_pencere(P["Lo"], d, j, R)
    E0 = P["Op"][d, j]; st0 = A.hat.to_numpy(float) * float(YH.YH_ESIK["olcu"]["stop0"]["hat_carpan"])
    Hd: Dict[float, Dict[str, np.ndarray]] = {}
    for de in PK_ESIK["A"]["delta"]:
        c2, h2, l2 = pk_surukle(Cr, Hr, Lr, de, int(PK_ESIK["A"]["ufuk"]))
        S = YH.yh_sim(c2, h2, l2, E0, st0, 1)
        Hd[float(de)] = {"h5": S["h5"], "st5": S["st5"], "h10": S["h10"]}
    h0 = A.h5.to_numpy(float)
    if not np.array_equal(np.isfinite(h0), np.isfinite(Hd[0.0]["h5"])) or not np.allclose(h0[np.isfinite(h0)], Hd[0.0]["h5"][np.isfinite(h0)]):
        raise PKHata(f"{pazar}: delta 0 yeniden simülasyonu ds_olc h5'ine eşit değil")
    me = int(DS.DS_ESIK["olcu"]["es_min"])
    Al = A[["sembol", "pazar", "donem", "giris", "kova", "h5", "st5", "h10", "getiri", "d", "j", "hat"]].copy()
    esH = DS.ds_es_topla(Al, Cd, pd.DataFrame(index=range(len(H["X"]))), "_hepsi", me)
    say = {"ana_olculen": {h: int(((Al.donem == h) & np.isfinite(Al.h5)).sum()) for h in PK_ESIK["A"]["hucre"]},
           "havuz": {h: int(((Al.donem == h) & np.isfinite(Al.h5) & np.isfinite(esH["es_h5"])).sum()) for h in PK_ESIK["A"]["hucre"]},
           "h5_ort": {h: float(np.nanmean(Al.h5[Al.donem == h])) for h in PK_ESIK["A"]["hucre"]},
           "sure_sn": round(time.time() - t0, 1)}
    for de in PK_ESIK["A"]["delta"]:
        say[f"h5_ort_d{de}"] = {h: float(np.nanmean(Hd[float(de)]["h5"][(Al.donem == h).to_numpy()])) for h in PK_ESIK["A"]["hucre"]}
    pklog.info("A %s: ANA ölçülen %s, havuz %s (%.0f sn)", pazar, say["ana_olculen"], say["havuz"], time.time() - t0)
    return {"A": Al, "Cd": Cd, "nX": len(H["X"]), "H": Hd, "esH": esH, "say": say, "Vd": H["Vd"], "P": P}


def _pk_a_sec(G: Dict[str, Any], pazar: str, ti: int, nk: Any) -> Tuple[Dict[str, np.ndarray], np.ndarray]:
    Al, esH = G["A"], G["esH"]; Ea = PK_ESIK["A"]; pi = Ea["pazar"].index(pazar); ni = Ea["n"].index(nk)
    sec: Dict[str, np.ndarray] = {}
    for hi, h in enumerate(Ea["hucre"]):
        havuz = np.flatnonzero((Al.donem.to_numpy() == h) & np.isfinite(Al.h5.to_numpy(float)) & np.isfinite(esH["es_h5"]))
        n = len(havuz) // 2 if nk == "yari" else int(nk)
        if n < 1 or n > Ea["n_azami_pay"] * len(havuz):      # eş adayı kalmalı (önceden yazılı: tutan <= havuzun 2/3'ü)
            sec[h] = np.array([], int); continue
        rng = np.random.default_rng([int(Ea["tohum"]), int(ti), ni, pi, hi])
        sec[h] = np.sort(rng.choice(havuz, size=n, replace=False))
    F = np.zeros(G["nX"]); idx = Al.index.to_numpy()
    for h in sec:
        F[idx[sec[h]]] = 1.0
    return sec, F


def pk_a_hucre(G: Dict[str, Any], pazar: str, ti: int, nk: Any, satir: bool = False) -> List[Dict[str, Any]]:
    """Bir pazar x tohum x n: seçim, eş toplama (ds_es_topla), her delta x hücre için ds_hucre + tek yönlü p."""
    Al, Cd, esH = G["A"], G["Cd"], G["esH"]; Ea = PK_ESIK["A"]; me = int(DS.DS_ESIK["olcu"]["es_min"])
    sec, F = _pk_a_sec(G, pazar, ti, nk)
    Fall = pd.DataFrame({"F_PKS": F})
    es = DS.ds_es_topla(Al, Cd, Fall, "PKS", me)
    out = []
    for di, de in enumerate(Ea["delta"]):
        A2 = Al.copy(); A2["F_PKS"] = F[Al.index.to_numpy()]
        hd = G["H"][float(de)]; tum = np.concatenate([sec[h] for h in sec]) if sec else np.array([], int)
        for k in ("h5", "st5", "h10"):
            v = A2[k].to_numpy(float).copy(); v[tum] = hd[k][tum]; A2[k] = v
        for hi, h in enumerate(Ea["hucre"]):
            if not len(sec[h]):
                out.append({"pazar": pazar, "tohum": ti, "n_hedef": nk, "delta": de, "hucre": h, "n": 0}); continue
            tek = 100000 + ti * 100 + Ea["n"].index(nk) * 10 + hi * 2 + Ea["pazar"].index(pazar)
            c = DS.ds_hucre(A2, es, esH, "PKS", pazar, h, tek)
            m = ((A2.pazar == pazar) & (A2.donem == h) & (A2.F_PKS == 1)).to_numpy()
            g = pd.DataFrame({"h5": A2.h5.to_numpy(float), "es_h5": es["es_h5"], "giris": A2.giris.to_numpy()})[m]
            g = g[g.h5.notna() & g.es_h5.notna()]
            p1 = DS.ds_perm_p(g, "+", int(DS.DS_ESIK["perm"]["R"]), int(DS.DS_ESIK["perm"]["tohum"]) + tek) if len(g) else np.nan
            r = {"pazar": pazar, "tohum": ti, "n_hedef": nk, "delta": de, "hucre": h, "n": int(c["n"]), "fark": c["fark"],
                 "p_olay": c["p_olay"], "p_es": c["p_es"], "boot_alt": c["boot_alt"], "boot_ust": c["boot_ust"], "guc": c.get("guc", np.nan),
                 "p_tek": p1, "p_iki": c["p"], "st": c["st"], "es_st": c["es_st"]}
            r["yakala"] = _pk_yakala(c, p1); r["yakala_iki"] = _pk_yakala(c, c["p"])
            out.append(r)
            if satir:
                gg = pd.DataFrame({"satir": Al.index.to_numpy(), "sembol": Al.sembol.to_numpy(), "giris": Al.giris.to_numpy(),
                                   "h5": A2.h5.to_numpy(float), "es_h5": es["es_h5"], "n_es": es["n_es"]})[m]
                gg = gg[np.isfinite(gg.h5) & np.isfinite(gg.es_h5)].assign(delta=de, hucre=h)
                r["_satir"] = gg
    return out


def _pk_a_isci(is_: Tuple[str, int, Any]) -> List[Dict[str, Any]]:
    pazar, ti, nk = is_
    return pk_a_hucre(_PK_A[pazar], pazar, ti, nk)


def pk_a_kos(islem: int = 1, veri: Optional[str] = None, pazarlar: Optional[List[str]] = None, tohum_sayi: Optional[int] = None,
             esik_json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    global _PK_A
    Ea = PK_ESIK["A"]; pazarlar = pazarlar or Ea["pazar"]; T = int(tohum_sayi or Ea["tohum_sayi"])
    say = {}
    for p in pazarlar:
        _PK_A[p] = pk_a_hazirla(p, islem, veri, esik_json); say[p] = _PK_A[p]["say"]
    isler = [(p, ti, nk) for p in pazarlar for ti in range(T) for nk in Ea["n"]]
    t0 = time.time()
    if islem > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(islem) as hv:
            R = hv.map(_pk_a_isci, isler, chunksize=1)
    else:
        R = [_pk_a_isci(x) for x in isler]
    S = pd.DataFrame([r for x in R for r in x])
    pklog.info("A ızgara: %d satır (%.0f sn)", len(S), time.time() - t0)
    return {"satir": S, "say": say}


def pk_a_ozet(S: pd.DataFrame) -> Dict[str, Any]:
    """Yakalama payı tablosu (pazar x hücre x n x delta) ve dört hücre birlikte."""
    g = S[S.n > 0].copy()
    g["nk"] = g.n_hedef.astype(str)
    tab = g.groupby(["pazar", "hucre", "nk", "delta"]).agg(yakala=("yakala", "mean"), yakala_iki=("yakala_iki", "mean"), n=("n", "mean"),
                                                         fark=("fark", "mean"), guc=("guc", "mean"), tohum=("tohum", "count")).reset_index()
    dort = []
    for (nk, de), x in g.groupby(["nk", "delta"]):
        k = x.groupby("tohum").agg(hep=("yakala", "all"), say=("yakala", "size"))
        k = k[k.say == 4]
        dort.append({"nk": nk, "delta": de, "dort_hucre": float(k.hep.mean()) if len(k) else np.nan, "tohum": int(len(k))})
    return {"tablo": tab.to_dict("records"), "dort": dort}


# ================================================================ 2) B: BİLİNEN İZ (momentum, PEAD)
def pk_b_sinyal_mom(Vd: Dict[str, Any], P: Dict[str, Any]) -> pd.DataFrame:
    idx = P["tarih"]
    ays = pd.DatetimeIndex(pd.Series(idx, index=idx).groupby(idx.to_period("M")).max().to_numpy())
    sat = []
    for s, df in Vd["V"].items():
        ix = df.index; pos = ix.get_indexer(ays); pos = pos[pos >= 252]
        if not len(pos):
            continue
        C = df.Close.to_numpy(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            mom = C[pos - 21] / C[pos - 252] - 1
        sat.append(pd.DataFrame({"sembol": s, "tarih": ix[pos], "deger": mom}))
    X = pd.concat(sat, ignore_index=True)
    return X[np.isfinite(X.deger)].reset_index(drop=True)


def pk_b_sinyal_pead(Vd: Dict[str, Any], bag: Dict[str, Any], sec: Dict[str, Any]) -> pd.DataFrame:
    J, SC = sec["J"], sec["SC"]; E = bag["E"]; sat = []
    for s, df in Vd["V"].items():
        cik = SC.get(s)
        if cik is None or str(cik) not in J:
            continue
        ev = pd.DatetimeIndex(DS._ds_sec_olay(J[str(cik)])["2.02"])
        if not len(ev):
            continue
        ix = df.index; C = df.Close.to_numpy(float); Ee = E.reindex(ix).to_numpy(float)
        b0 = np.unique(np.searchsorted(ix, ev, side="right"))
        b0 = b0[(b0 >= 2) & (b0 < len(ix))]
        if not len(b0):
            continue
        with np.errstate(invalid="ignore", divide="ignore"):
            tep = (C[b0] / C[b0 - 2] - 1) - (Ee[b0] / Ee[b0 - 2] - 1)
        sat.append(pd.DataFrame({"sembol": s, "tarih": ix[b0], "deger": tep}))
    X = pd.concat(sat, ignore_index=True)
    return X[np.isfinite(X.deger)].reset_index(drop=True)


def _pk_donem(g: pd.Series) -> np.ndarray:
    g = pd.to_datetime(g); Dn = PK_ESIK["donem"]
    eg = (g >= Dn["egitim"][0]) & (g <= Dn["egitim"][1]); sn = (g >= Dn["sinama"][0]) & (g <= Dn["sinama"][1])
    return np.where(eg, "egitim", np.where(sn, "sinama", "dis"))


def pk_b_kur(ad: str, Vd: Dict[str, Any], P: Dict[str, Any], sinyal: pd.DataFrame, seri: Dict[str, Tuple[pd.Series, pd.Series]],
             esik_q: Optional[Tuple[float, float]] = None) -> Tuple[pd.DataFrame, Dict[str, Any], Dict[str, Any]]:
    """Sinyal (sembol, tarih, deger) -> X (olay + eş adayı satırları; d, j, kova, hat, ana, donem, F_<ad>U / A / UA) ve Z (ds_olc girdisi)."""
    E1 = json.loads(json.dumps(OC.OC_ESIK)); E1["olay"]["tekil_gun"] = 1
    ol = sinyal.assign(pazar=Vd["pazar"])[["sembol", "tarih", "pazar"]]
    Xe, say = OC.oc_olay_hazirla(ol, P, E1)
    Xe = Xe.merge(sinyal, on=["sembol", "tarih"], how="left", validate="one_to_one")
    Xe["donem"] = _pk_donem(Xe.giris)
    q = PK_ESIK["B"]["onda"]
    if esik_q is None:          # momentum: aynı t kesitinde sıra
        rk = Xe.groupby("tarih").deger.rank(method="first", pct=True).to_numpy()
        U = rk > q[1]; A_ = rk <= q[0]; sinir = {"tur": "kesit sırası", "q": q}
    else:                       # PEAD: eğitimden sabit sınırlar
        U = Xe.deger.to_numpy(float) >= esik_q[1]; A_ = Xe.deger.to_numpy(float) <= esik_q[0]; sinir = {"tur": "eğitim onda", "q10": esik_q[0], "q90": esik_q[1]}
    Xe["U"] = U; Xe["A"] = A_
    # ANA: U ya da A; aynı hissede >= 15 bar arayla ilk (DS tekil_bar)
    Xe = Xe.sort_values(["sembol", "d"], kind="mergesort").reset_index(drop=True)
    ana = np.zeros(len(Xe), bool); son: Dict[str, int] = {}
    for i, (s, d, u, a) in enumerate(zip(Xe.sembol.to_numpy(), Xe.d.to_numpy(int), Xe.U.to_numpy(bool), Xe.A.to_numpy(bool))):
        if (u or a) and (s not in son or d - son[s] >= DS.DS_ESIK["olay"]["tekil_bar"]):
            ana[i] = True; son[s] = d
    Xe["ana"] = ana & np.isin(Xe.donem.to_numpy(), ["egitim", "sinama"])
    S = P["sembol"]; idx = P["tarih"]
    hat = np.full(len(Xe), np.nan)
    for s, g in Xe.groupby("sembol"):
        hat[g.index.to_numpy()] = seri[s][1].reindex(pd.DatetimeIndex(g.tarih)).to_numpy(float)
    Xe["hat"] = hat
    AT = pd.DataFrame({s: seri[s][0].shift(1) for s in S}).reindex(idx).to_numpy(float)
    Xe["atrp_d"] = AT[Xe.d.to_numpy(int), Xe.j.to_numpy(int)]
    g = Xe[Xe.ana & (Xe.donem == "egitim")]
    e = {"ATRP_t1": DS._ds_q(g.atrp_d.to_numpy(float), 1 / 3), "ATRP_t2": DS._ds_q(g.atrp_d.to_numpy(float), 2 / 3)}
    # eş adayı satırları: ANA olayların giriş günlerinde havuzdaki öteki hisseler (momentum: yalnız sinyal kesiti; PEAD: bütün havuz)
    if esik_q is None:
        X = Xe.copy()
    else:
        gun = np.unique(Xe.d[Xe.ana].to_numpy(int)); var = set(zip(Xe.d.to_numpy(int), Xe.j.to_numpy(int))); ek = []
        for d in gun:
            js = np.flatnonzero(P["ok"][d] & (P["H"][d] >= 0))
            js = [j for j in js if (d, j) not in var]
            if js:
                ek.append(pd.DataFrame({"d": d, "j": js}))
        E_ = pd.concat(ek, ignore_index=True) if ek else pd.DataFrame(columns=["d", "j"])
        E_["sembol"] = [S[j] for j in E_.j.to_numpy(int)]; E_["tarih"] = pd.NaT; E_["giris"] = idx[E_.d.to_numpy(int)]
        E_["hucre"] = P["H"][E_.d.to_numpy(int), E_.j.to_numpy(int)]; E_["U"] = False; E_["A"] = False; E_["ana"] = False
        E_["hat"] = np.nan; E_["deger"] = np.nan; E_["donem"] = "aday"; E_["atrp_d"] = AT[E_.d.to_numpy(int), E_.j.to_numpy(int)]
        X = pd.concat([Xe, E_[[c for c in Xe.columns if c in E_.columns]]], ignore_index=True)
    X["pazar"] = Vd["pazar"]
    a = X.atrp_d.to_numpy(float)
    at = np.where(np.isfinite(a), np.where(a <= e["ATRP_t1"], 0, np.where(a <= e["ATRP_t2"], 1, 2)), -1)
    X["kova"] = np.where((at >= 0) & (X.hucre.to_numpy(int) >= 0), at * 3 + X.hucre.to_numpy(int) % 3, -1)
    U = X.U.to_numpy(bool); A_ = X.A.to_numpy(bool)
    X[f"F_{ad}U"] = np.where(U, 1.0, np.where(A_, np.nan, 0.0))
    X[f"F_{ad}A"] = np.where(A_, 1.0, np.where(U, np.nan, 0.0))
    X[f"F_{ad}UA"] = np.where(U, 1.0, np.where(A_, 0.0, np.nan))
    X = X.reset_index(drop=True)
    uye = {s: pd.Series(False, index=Vd["V"][s].index) for s in S}
    for s, g in Xe[Xe.U | Xe.A].groupby("sembol"):
        uye[s].loc[pd.DatetimeIndex(g.tarih)] = True
    Z = {"ds": uye, "atrp": {s: seri[s][0] for s in S}, "esik": e}
    say.update({"olay_havuz": int(len(Xe)), "U": int(Xe.U.sum()), "A": int(Xe.A.sum()), "ana": int(X.ana.sum()),
                "ana_donem": {k: int(v) for k, v in X[X.ana].donem.value_counts().items()}, "satir": int(len(X)), "atrp": e, "sinir": sinir})
    return X, Z, say


def pk_r15(P: Dict[str, Any], Cl: np.ndarray, d: np.ndarray, j: np.ndarray) -> np.ndarray:
    """Stop'suz 15 bar: 15. geçerli barın (giriş barı 1.) kapanışı / giriş açılışı - 1; yh_sim ölçülebilirlik kuralı (30 satırda >= 15 geçerli)."""
    R = int(YH.YH_ESIK["olcu"]["pencere_azami"]); u = int(YH.YH_ESIK["olcu"]["ufuk"])
    d = np.asarray(d, int); j = np.asarray(j, int); out = np.full(len(d), np.nan)
    for i0 in range(0, len(d), 200000):
        dd, jj = d[i0:i0 + 200000], j[i0:i0 + 200000]
        W = _pk_pencere(Cl, dd, jj, R); v = np.isfinite(W); cs = np.cumsum(v, axis=0)
        ok = v[0] & (cs[-1] >= u)
        row = np.argmax(cs >= u, axis=0)
        E0 = P["Op"][dd, jj]
        with np.errstate(invalid="ignore", divide="ignore"):
            r = W[row, np.arange(len(dd))] / E0 - 1
        out[i0:i0 + len(dd)] = np.where(ok & np.isfinite(E0) & (E0 > 0), r, np.nan)
    return out


def pk_es_deger(A: pd.DataFrame, Cd: Dict[str, np.ndarray], Fall: pd.DataFrame, kod: str, deger_aday: np.ndarray, me: int) -> np.ndarray:
    """ds_es_topla ile AYNI eş kümesi (F == 0, h5 ölçülebilir, >= me eş) üzerinde başka bir değerin (r15) ortalaması."""
    pos = pd.Index(A.index).get_indexer(Cd["ce"])
    Fc = Fall[f"F_{kod}"].to_numpy(float)[Cd["cr"]]
    m = (Fc == 0) & np.isfinite(Cd["c5"]) & (pos >= 0)
    nA = len(A); cnt = np.bincount(pos[m], minlength=nA).astype(float)
    mv = m & np.isfinite(deger_aday)
    cv = np.bincount(pos[mv], minlength=nA).astype(float); sm = np.bincount(pos[mv], weights=deger_aday[mv], minlength=nA)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where((cnt >= me) & (cv == cnt), sm / np.where(cv > 0, cv, 1), np.nan)


def pk_b_olc(ad: str, Vd: Dict[str, Any], P: Dict[str, Any], X: pd.DataFrame, Z: Dict[str, Any], islem: int, bilgi: bool = False) -> Dict[str, Any]:
    """ds_olc + üç cetvel. Döner: hücre sonuçları ve olay satırları."""
    t0 = time.time()
    A, Cd = DS.ds_olc(X, P, Vd, Z, islem)
    me = int(DS.DS_ESIK["olcu"]["es_min"]); Cl = YH.yh_kapanis(P, Vd)
    A["r15"] = pk_r15(P, Cl, A.d.to_numpy(int), A.j.to_numpy(int))
    r15c = pk_r15(P, Cl, X.d.to_numpy(int)[Cd["cr"]], X.j.to_numpy(int)[Cd["cr"]])
    Xo = OC.oc_esli(P, A[["sembol", "tarih", "giris", "d", "j"]].reset_index(drop=True))
    A["r60"] = Xo.r60.to_numpy(float); A["esli_r60"] = Xo.esli_r60.to_numpy(float)
    esH = DS.ds_es_topla(A, Cd, X, "_hepsi", me)
    yonler = PK_ESIK["B"][ad]["yon"]; sonuc = []; kols = {}
    for ki, k in enumerate(("U", "A", "UA")):
        kod = f"{ad}{k}"; es = DS.ds_es_topla(A, Cd, X, kod, me)
        A[f"es_h5_{k}"] = es["es_h5"]; A[f"es_r15_{k}"] = pk_es_deger(A, Cd, X, kod, r15c, me); A[f"F_{kod}"] = X.loc[A.index, f"F_{kod}"].to_numpy(float)
        for hi, h in enumerate(("egitim", "sinama")):
            tek = 200000 + ki * 10 + hi + (500 if bilgi else 0)
            c = DS.ds_hucre(A, es, esH, kod, Vd["pazar"], h, tek)
            m = ((A.donem == h) & (A[f"F_{kod}"] == 1)).to_numpy()
            s15 = pk_istat(A.h5.to_numpy(float)[m], es["es_h5"][m], A.giris.to_numpy()[m], yonler[k], tek)
            r15 = pk_istat(A.r15.to_numpy(float)[m], A[f"es_r15_{k}"].to_numpy(float)[m], A.giris.to_numpy()[m], yonler[k], tek)
            if k == "UA":
                r60 = {"n": 0}
            else:
                r60 = pk_istat(A.r60.to_numpy(float)[m], A.esli_r60.to_numpy(float)[m], A.giris.to_numpy()[m], yonler[k], tek)
            sonuc.append({"kod": kod, "hucre": h, "pazar": Vd["pazar"], "h5": {**{x: c.get(x) for x in ("n", "p_olay", "p_es", "fark", "boot_alt",
                                                                                                       "boot_ust", "guc", "st", "es_st",
                                                                                                       "h5_med", "getiri_ort", "getiri_med",
                                                                                                       "h10", "es_h10")},
                                                                              "p": s15["p"], "p_iki": s15["p_iki"]},
                          "r15": r15, "r60": r60})
            kols[(k, h)] = m
    yay = []
    for hi, h in enumerate(("egitim", "sinama")):
        mU, mA = kols[("U", h)], kols[("A", h)]
        r = {"hucre": h}
        for cet, (v, eU, eA) in {"h5": ("h5", "es_h5_U", "es_h5_A"), "r15": ("r15", "es_r15_U", "es_r15_A"), "r60": ("r60", "esli_r60", "esli_r60")}.items():
            gU = pd.DataFrame({"h5": A[v].to_numpy(float)[mU], "es_h5": A[eU].to_numpy(float)[mU], "giris": A.giris.to_numpy()[mU]})
            gA = pd.DataFrame({"h5": A[v].to_numpy(float)[mA], "es_h5": A[eA].to_numpy(float)[mA], "giris": A.giris.to_numpy()[mA]})
            r[cet] = pk_yayilim(gU, gA, hi * 10 + len(yay))
        yay.append(r)
    pklog.info("B %s %s: %d ANA olay ölçüldü (%.0f sn)", ad, Vd["pazar"], int(np.isfinite(A.h5).sum()), time.time() - t0)
    return {"sonuc": sonuc, "yayilim": yay, "A": A, "Cd": Cd, "r15c": r15c}


def pk_b_kos(islem: int = 1, veri: Optional[str] = None, k55: Optional[str] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {"sonuc": [], "yayilim": [], "say": {}, "satir": []}
    k55 = k55 or PK_YOL["k55"]
    sec = DS.ds_sec_yukle(k55)
    for pazar in PK_ESIK["B"]["pazar"] + PK_ESIK["B"]["bilgi_pazar"]:
        bilgi = pazar in PK_ESIK["B"]["bilgi_pazar"]
        Vd = DS.ds_veri(pazar, veri or PK_YOL["veri"]); P = OC.oc_panel(Vd)
        seri = {s: pk_seri(Vd["V"][s]) for s in P["sembol"]}
        isler = [("B1", pk_b_sinyal_mom(Vd, P), None)]
        if not bilgi:
            if sec is None:
                raise PKHata(f"sec_ozet yok ({k55}): B2 PEAD ölçülemez (K55.veri_paket.ac('/tmp/iv/k55', '{k55}'))")
            bag = DS.ds_baglam(Vd); sp = pk_b_sinyal_pead(Vd, bag, sec)
            Xt, _ = OC.oc_olay_hazirla(sp.assign(pazar=pazar)[["sembol", "tarih", "pazar"]], P,
                                       {**json.loads(json.dumps(OC.OC_ESIK)), "olay": {**OC.OC_ESIK["olay"], "tekil_gun": 1}})
            Xt = Xt.merge(sp, on=["sembol", "tarih"], how="left")
            eg = Xt.deger[_pk_donem(Xt.giris) == "egitim"].to_numpy(float)
            q = (float(np.quantile(eg, PK_ESIK["B"]["onda"][0])), float(np.quantile(eg, PK_ESIK["B"]["onda"][1])))
            out["say"]["B2_esik"] = {"q10": q[0], "q90": q[1], "n_egitim": int(len(eg)), "ornek": DS._ds_sec_ornek(sec)}
            isler.append(("B2", sp, q))
        for ad, sg, q in isler:
            X, Z, say = pk_b_kur(ad, Vd, P, sg, seri, q)
            R = pk_b_olc(ad, Vd, P, X, Z, islem, bilgi)
            for r in R["sonuc"]:
                r["bilgi"] = bilgi
            out["sonuc"] += R["sonuc"]; out["yayilim"] += [{**y, "kod": ad, "pazar": pazar, "bilgi": bilgi} for y in R["yayilim"]]
            out["say"][f"{ad}_{pazar}"] = say
            kol = ["sembol", "tarih", "giris", "d", "j", "donem", "kova", "hat", "deger", "U", "A", "h5", "h10", "st5", "getiri", "cikis_bar",
                   "r15", "r60", "esli_r60", "es_h5_U", "es_h5_A", "es_h5_UA", "es_r15_U", "es_r15_A", "es_r15_UA", "n_aday"]
            S_ = R["A"][[c for c in kol if c in R["A"].columns]].copy(); S_.insert(0, "kod", ad); S_.insert(1, "pazar", pazar)
            S_["satir"] = R["A"].index.to_numpy()
            out["satir"].append(S_)
            if ad == "B1" and pazar == "ABD":
                out["_yu"] = {"X": X, "Vd": Vd, "P": P, "A": R["A"]}
    return out


# ================================================================ 3) C: ÖRNEKLER
def _pk_temiz_v(yol: str, semboller: List[str], kriz: Optional[str]) -> Tuple[Dict[str, pd.DataFrame], pd.DatetimeIndex]:
    ham = pd.read_pickle(yol)
    if isinstance(ham, dict) and "veri" in ham and isinstance(ham["veri"], dict):
        ham = ham["veri"]
    E = json.loads(json.dumps(OC.OC_ESIK))
    if kriz:
        E["kriz"] = kriz
    V, ix = {}, set()
    for s, d in ham.items():
        try:
            x, _ = OC.oc_veri_hazirla(d, E)
        except Exception:   # tek hisse bozuksa takvim yine kurulur
            continue
        ix |= set(x.index)
        if s in semboller:
            V[s] = x
    return V, pd.DatetimeIndex(sorted(ix))


def pk_c_olc(df: pd.DataFrame, takvim: pd.DatetimeIndex, t: pd.Timestamp, stop0: Optional[float], d_es: Optional[float] = None) -> Dict[str, Any]:
    """Tek hisse, sinyal t: giriş = t'den sonraki ilk geçerli bar açılışı; yh_sim (takvim penceresi 30) + yh_getiri + stop'suz r15 + en yüksek kapanış."""
    ix = df.index; gi = int(ix.searchsorted(t, side="right"))
    if gi >= len(ix):
        return {"durum": "giriş yok"}
    O, H, L, C = (df[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    E0 = float(O[gi]); st0 = float(stop0) if d_es is None else E0 * (1 - float(d_es))
    R = int(YH.YH_ESIK["olcu"]["pencere_azami"]); dp = int(takvim.get_loc(ix[gi])); cal = takvim[dp:dp + R]
    w = df.reindex(cal)
    Cr, Hr, Lr = (np.r_[w[k].to_numpy(float), np.full(R - len(cal), np.nan)][:, None] for k in ("Close", "High", "Low"))
    S = YH.yh_sim(Cr, Hr, Lr, np.array([E0]), np.array([st0]), 1)
    g_, b_, t_ = YH.yh_getiri(O, H, L, C, gi, E0, st0, 1)
    v = np.isfinite(Cr[:, 0]); cs = np.cumsum(v)
    r15 = float(Cr[np.argmax(cs >= 15), 0] / E0 - 1) if cs[-1] >= 15 else np.nan
    ilk = Cr[:, 0][v][:15]
    return {"durum": "ölçüldü" if bool(S["olc"][0]) else "15 bar ölçülemez", "giris": str(ix[gi].date()), "E0": E0, "stop0": st0,
            "d": 1 - st0 / E0, "h5": float(S["h5"][0]), "h10": float(S["h10"][0]), "st5": float(S["st5"][0]), "h5H": float(S["h5H"][0]),
            "k5": int(S["k5"][0]), "kst": int(S["kst"][0]), "getiri": g_, "cikis_bar": int(b_), "cikis_tur": t_, "r15": r15,
            "maks15": float(np.nanmax(ilk) / E0 - 1) if len(ilk) else np.nan, "min15": float(np.nanmin(ilk) / E0 - 1) if len(ilk) else np.nan}


def _pk_neden(r: Dict[str, Any]) -> str:
    if r.get("durum") != "ölçüldü":
        return r.get("durum", "-")
    if r["h5"] == 1:
        return f"HEDEFE ULAŞTI: +%5 kapanış bar {r['k5']}" + (" (+%10 da)" if r["h10"] == 1 else "")
    if r["st5"] == 1:
        return (f"stop önce: bar {r['kst']} kapanışı stop altında (stop uzaklığı %{100 * r['d']:.1f}; 15 barda en düşük kapanış "
                f"%{100 * r['min15']:+.1f}, en yüksek %{100 * r['maks15']:+.1f})")
    return f"15 barda +%5 kapanış yok, stop da yok (en yüksek kapanış %{100 * r['maks15']:+.1f})"


def pk_c_kos(veri: Optional[str] = None, canli: Optional[str] = None) -> List[Dict[str, Any]]:
    Ec = PK_ESIK["C"]; out = []
    Vb, tb = _pk_temiz_v(os.path.join(veri or PK_YOL["veri"], "V_BIST.pkl"), sorted({x[1] for x in Ec["bist"]}), None)
    for ad, s, son in Ec["bist"]:
        r: Dict[str, Any] = {"ornek": ad, "sembol": s, "pazar": "BIST", "kutu_sonu": son}
        if s not in Vb:
            r.update({"durum": "veride yok", "neden": "veride yok"}); out.append(r); continue
        df = Vb[s]; ix = df.index; i0 = int(ix.searchsorted(pd.Timestamp(son))); a, b = max(0, i0 - 5), min(len(ix) - 1, i0 + 60)
        X6, _ = YH.yh_s6_hisse(df)
        X6 = X6[(X6.tarih >= ix[a]) & (X6.tarih <= ix[b])] if len(X6) else X6
        if len(X6):
            t = pd.Timestamp(X6.tarih.iloc[0]); hat = float(X6.hat.iloc[0]); kay = f"S6 al ({str(X6.ek.iloc[0]).split(';')[0]})"
        else:
            H = df.High.to_numpy(float); C = df.Close.to_numpy(float); t = None
            for i in range(max(a, 120), b + 1):
                if C[i] > np.max(H[i - 120:i]):
                    t = ix[i]; break
            if t is None:
                r.update({"durum": "sinyal yok", "neden": "pencerede S6 al ve 120 gün üst sınır kırılımı yok"}); out.append(r); continue
            hat = float(pk_seri(df)[1].loc[t]); kay = "120 gün üst sınır kırılımı (hat 20 bar dip)"
        r.update({"sinyal": str(t.date()), "kaynak": kay, "sinyal_bar_kutu_sonundan": int(ix.get_loc(t) - i0), "hat": hat})
        m = pk_c_olc(df, tb, t, hat * float(YH.YH_ESIK["olcu"]["stop0"]["hat_carpan"]))
        r.update(m); r["neden"] = _pk_neden(m)
        h20 = float(pk_seri(df)[1].loc[t])
        if kay.startswith("S6"):
            m2 = pk_c_olc(df, tb, t, h20 * float(YH.YH_ESIK["olcu"]["stop0"]["hat_carpan"]))
            r["hat20"] = {k: m2.get(k) for k in ("h5", "h10", "st5", "getiri", "cikis_bar", "d")}
        out.append(r)
    yc = os.path.join(canli or PK_YOL["canli"], "V_ABD.pkl")
    if not os.path.exists(yc):
        for s, g, ad_, *_ in Ec["ekim"]:
            out.append({"ornek": f"{s} (eş / {ad_})", "sembol": s, "pazar": "ABD", "durum": "veri yok", "neden": f"{yc} yok"})
        return out
    Va, ta = _pk_temiz_v(yc, sorted({x[0] for x in Ec["ekim"]}), "2099-12-31")
    for s, g, aday, ag, ast in Ec["ekim"]:
        r = {"ornek": f"{s} (eş / {aday})", "sembol": s, "pazar": "ABD", "giris_hedef": g}
        if s not in Va:
            r.update({"durum": "veride yok", "neden": "veride yok"}); out.append(r); continue
        df = Va[s]; ix = df.index; gi = int(ix.searchsorted(pd.Timestamp(g)))
        if gi >= len(ix) or ix[gi] != pd.Timestamp(g) or gi < 20:
            r.update({"durum": "giriş günü veride yok", "neden": "giriş günü veride yok"}); out.append(r); continue
        t = ix[gi - 1]; hat = float(pk_seri(df)[1].loc[t])
        m = pk_c_olc(df, ta, t, hat * float(YH.YH_ESIK["olcu"]["stop0"]["hat_carpan"]))
        r.update({"sinyal": str(t.date()), "kaynak": "kendi hattı (20 bar dip)", "hat": hat}); r.update(m); r["neden"] = _pk_neden(m)
        m2 = pk_c_olc(df, ta, t, None, d_es=1 - ast / ag)
        r["esler_geo"] = {k: m2.get(k) for k in ("h5", "h10", "st5", "getiri", "cikis_bar", "d", "maks15", "k5", "kst")}
        r["esler_geo"]["neden"] = _pk_neden(m2)
        out.append(r)
    return out


# ================================================================ 4) YENİDEN ÜRETİM (bağımsız düz döngü)
def pk_elle_h5(C: np.ndarray, takvim_pos: np.ndarray, gi: int, E0: float, st0: float, delta: float = 0.0) -> Tuple[float, float, float]:
    """yh_sim'den BAĞIMSIZ düz döngü (YH_ESIK['olcu'] metni): hissenin barları gi'den; 15 bar giriş gününden 30 takvim satırı içinde değilse
    ölçülmez; k. bar kapanışı x (1 + delta (k+1)/15); stop kapanışla (bar k-1 sonu stop'u), sonra +%5 / +%10, sonra stop güncellemesi."""
    if gi + 15 > len(C) or takvim_pos[gi + 14] - takvim_pos[gi] > 29 or not (E0 > st0):
        return np.nan, np.nan, np.nan
    stop = st0; g5 = g10 = False; ext = -np.inf
    for k in range(15):
        c = C[gi + k] * (1 + delta * (k + 1) / 15.0)
        if c < stop:
            return float(g5), float(g10), float(not g5)
        if not g5 and c >= E0 * (1 + 0.05):
            g5 = True
        if not g10 and c >= E0 * (1 + 0.10):
            g10 = True
        if g5:
            stop = max(stop, E0 * (1 + 0.02))
        if g10:
            stop = max(stop, E0 * (1 + 0.07))
        ext = max(ext, c); stop = max(stop, ext * (1 - 0.07))
    return float(g5), float(g10), 0.0


def pk_yeniden_a(G: Dict[str, Any], cikti: str) -> Dict[str, Any]:
    pazar, h, nk, de, ti = PK_ESIK["yeniden_uretim"]["A"]
    R = pk_a_hucre(G, pazar, ti, nk, satir=True)
    r = [x for x in R if x["hucre"] == h and float(x["delta"]) == float(de)][0]
    g = r.pop("_satir"); yol = os.path.join(cikti, PK_DOSYA["a_satir"]); g.to_csv(yol, index=False, compression="gzip")
    Y = pd.read_csv(yol)                     # düz pandas: dosyadan
    fark = float(Y.h5.mean() - Y.es_h5.mean())
    # 50 tutan olayın sürüklenmiş h5'i düz döngüyle (hissenin kendi verisi)
    rng = np.random.default_rng(int(PK_ESIK["yeniden_uretim"]["tohum"])); sec = rng.choice(len(Y), size=min(int(PK_ESIK["yeniden_uretim"]["elle_n"]), len(Y)), replace=False)
    Al = G["A"]; Vd = G["Vd"]; P = G["P"]; idx = P["tarih"]; bozuk = []
    for i in sec:
        row = Al.loc[int(Y.satir.iloc[i])]; df = Vd["V"][row.sembol]; ix = df.index
        gi = int(ix.get_loc(pd.Timestamp(row.giris))); pos = idx.get_indexer(ix)
        E0 = float(df.Open.iloc[gi]); st0 = float(row.hat) * 0.98
        h5, _, _ = pk_elle_h5(df.Close.to_numpy(float), pos, gi, E0, st0, float(de))
        if not (h5 == float(Y.h5.iloc[i])):
            bozuk.append({"sembol": row.sembol, "giris": str(row.giris), "elle": h5, "kod": float(Y.h5.iloc[i])})
    return {"hucre": [pazar, h, nk, de, ti], "kod_fark": r["fark"], "dosya_fark": fark, "n_kod": r["n"], "n_dosya": int(len(Y)),
            "fark_esit": bool(abs(fark - r["fark"]) < 1e-12 and len(Y) == r["n"]), "elle_n": int(len(sec)), "elle_bozuk": bozuk}


def pk_yeniden_b(Y: Dict[str, Any], satir: pd.DataFrame, json_sonuc: List[Dict[str, Any]]) -> Dict[str, Any]:
    kod, h = PK_ESIK["yeniden_uretim"]["B"]
    S = satir[(satir.kod == kod[:2]) & (satir.pazar == "ABD") & (satir.donem == h) & (satir.U == True)]  # noqa: E712
    S = S[np.isfinite(S.h5) & np.isfinite(S.es_h5_U)]
    fark = float(S.h5.mean() - S.es_h5_U.mean()); S15 = S[np.isfinite(S.r15) & np.isfinite(S.es_r15_U)]
    f15 = float((S15.r15 - S15.es_r15_U).mean())
    j = [x for x in json_sonuc if x["kod"] == kod and x["hucre"] == h and x["pazar"] == "ABD"][0]
    X, Vd, P, A = Y["X"], Y["Vd"], Y["P"], Y["A"]; idx = P["tarih"]
    rng = np.random.default_rng(int(PK_ESIK["yeniden_uretim"]["tohum"]) + 1)
    sec = rng.choice(len(S), size=min(int(PK_ESIK["yeniden_uretim"]["elle_n"]), len(S)), replace=False)
    bozuk = []

    def elle(s: str, giris: pd.Timestamp, st0: Optional[float], dd: Optional[float]) -> Tuple[float, float]:
        df = Vd["V"][s]; ix = df.index; gi = int(ix.get_loc(pd.Timestamp(giris))); pos = idx.get_indexer(ix)
        E0 = float(df.Open.iloc[gi]); st = st0 if dd is None else E0 * (1 - dd)
        h5, _, _ = pk_elle_h5(df.Close.to_numpy(float), pos, gi, E0, st)
        ok = gi + 15 <= len(ix) and pos[gi + 14] - pos[gi] <= 29
        r15 = float(df.Close.iloc[gi + 14] / E0 - 1) if ok else np.nan
        return h5, r15
    for i in sec:
        r = S.iloc[i]; h5, r15 = elle(r.sembol, r.giris, float(r.hat) * 0.98, None)
        if not (h5 == float(r.h5) and abs(r15 - float(r.r15)) < 1e-9):
            bozuk.append({"sembol": r.sembol, "giris": str(r.giris), "elle": [h5, r15], "kod": [float(r.h5), float(r.r15)]})
    es_boz = []
    for i in sec[:int(PK_ESIK["yeniden_uretim"]["elle_es_n"])]:
        r = S.iloc[i]; a = A.loc[int(r.satir)]; d_ = int(a.d); E0 = float(P["Op"][d_, int(a.j)]); dd = 1 - float(a.hat) * 0.98 / E0
        c = X[(X.d.to_numpy(int) == d_) & (X.kova.to_numpy(int) == int(a.kova)) & (X.sembol != a.sembol) & (X[f"F_{kod}"] == 0)]
        v = []
        for e in c.itertuples():
            if not P["ok"][d_, int(e.j)]:
                continue
            h5e, _ = elle(e.sembol, idx[d_], None, dd)
            if np.isfinite(h5e):
                v.append(h5e)
        es = float(np.mean(v)) if len(v) >= 3 else np.nan
        if not (np.isfinite(es) and abs(es - float(r.es_h5_U)) < 1e-12):
            es_boz.append({"sembol": r.sembol, "giris": str(r.giris), "elle": es, "kod": float(r.es_h5_U), "n_elle": len(v)})
    return {"hucre": [kod, h], "kod_fark": j["h5"]["fark"], "dosya_fark": fark, "kod_r15": j["r15"]["fark"], "dosya_r15": f15,
            "esit": bool(abs(fark - j["h5"]["fark"]) < 1e-12 and abs(f15 - j["r15"]["fark"]) < 1e-12 and len(S) == j["h5"]["n"]),
            "elle_n": int(len(sec)), "elle_bozuk": bozuk, "elle_es_n": int(min(len(sec), int(PK_ESIK["yeniden_uretim"]["elle_es_n"]))),
            "elle_es_bozuk": es_boz}


# ================================================================ 5) ÖN KAYIT, KAPI
def pk_sha_simdi(veri: Optional[str] = None) -> Dict[str, str]:
    v = veri or PK_YOL["veri"]
    out = {"PK_ESIK_SHA": pk_esik_sha(), "PK_KOD_SHA": _pk_sha(PK_YOL["kod"])}
    ds = DS.ds_sha_simdi(veri=v)
    for k in ("DS_KOD_SHA", "YH_KOD_SHA", "OC_KOD_SHA", "S6_KOD_SHA", "DS_ESIK_SHA", "YH_ESIK_SHA", "OC_ESIK_SHA", "DS_ESIK_JSON_SHA",
              "V_ABD_SHA", "V_AVR_SHA", "V_BIST_SHA"):
        out[k] = ds[k]
    return out


def pk_cetvel_ayni() -> Dict[str, Any]:
    """DS / YH / OC / S6 kod ve eşik sha'ları DS_ON_KAYIT.md'deki ile eşit mi (cetvel değişmedi kanıtı)."""
    yol = os.path.join(PK_YOL["ds_cikti"], DS.DS_DOSYA["onkayit"]); metin = open(yol, encoding="utf-8").read()
    simdi = DS.ds_sha_simdi(); out = {}
    for k in ("DS_KOD_SHA", "YH_KOD_SHA", "OC_KOD_SHA", "S6_KOD_SHA", "DS_ESIK_SHA", "YH_ESIK_SHA", "OC_ESIK_SHA", "DS_ESIK_JSON_SHA"):
        m = re.search(DS._DS_DESEN[k], metin)
        out[k] = bool(m and m.group(1) == simdi[k])
    if not all(out.values()):
        raise PKHata(f"cetvel DS ön kaydından farklı: {[k for k, v in out.items() if not v]}")
    return out


def pk_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False) -> str:
    c = cikti or PK_YOL["cikti"]; yol = _pk_yol("onkayit", c)
    if os.path.exists(yol) and not uzerine:
        raise PKHata(f"ön kayıt zaten var: {yol}")
    sha = pk_sha_simdi(veri); ayni = pk_cetvel_ayni()
    s = [f"# POZİTİF KONTROL — ÖN KAYIT ({_pk_simdi()})", "", PK_SURUM + ". Bu dosya ölçümden ÖNCE yazıldı ve git'e işlendi; pk_kapi PK_ESIK ve kod "
         "sha'larını, cetvel sha'larının DS_ON_KAYIT.md ile eşitliğini, git kaydını ve IZ_KARNE.ik_kontrol_kapisi'ni denetler; biri tutmazsa koşu "
         "DURUR. Sonuç (h5 / getiri) bu dosya yazılırken hesaplanmadı.", ""]
    s += [f"- {k}: `{v}`" for k, v in sha.items()]
    s += [f"- CETVEL = DS ön kaydı: {', '.join(k for k, v in ayni.items() if v)}", ""]
    s += ["## 1. TASARIM (PK_ESIK; iş tanımı commit 4505d5c)", ""]

    def dz(d, on=""):
        for k, v in d.items():
            if isinstance(v, dict):
                s.append(f"- {on}{k}:"); dz(v, on + "  ")
            else:
                s.append(f"- {on}{k}: {v}")
    dz(PK_ESIK)
    s += ["", "## 2. ÖNCEDEN YAZILI OKUMA KURALI", "",
          "- A: cetvel bir (n, delta) noktasında 'görür' = o pazar x hücrede 20 tohumun >= %80'inde yakalama. Plasebo (delta 0) yanlış pozitif payı "
          "> %10 ise cetvel 'gevşek' yazılır.",
          "- B: bilinen etki 'görünür' = bir cetvelde eğitim VE sınama hücrelerinde fark beklenen yönde ve p < 0,05 (U: +, A: -, UA: +). Cetvel "
          "duyarlılığı: aynı olaylarda h5 FARK z (fark / boot yarı genişliği) ile r15 ve r60 z'si yan yana.",
          "- SONUÇ: HAYIR = A'da gerçek boyutta (yari) delta +%5 bile dört hücrede >= %80 yakalanmıyor; EVET = A'da bir delta'da yakalanıyor VE B'de "
          "en az bir bilinen etki (kod) h5 cetvelinde görünür; KISMEN = A'da yakalanıyor ama hiçbir bilinen etki h5'te görünmüyor (r15 / r60'ta "
          "görünüp görünmediği ayrıca yazılır). 'Daha duyarlı cetvel' = aynı olaylarda |fark| / boot yarı genişliği büyük olan.",
          "", "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "",
          "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    try:
        import IZ_KARNE as IK
        ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    except Exception:   # IZ_KARNE yoksa madde adı yazılmaz; kapı yine kodları okur
        ad = {}
    for k, (y, kn) in PK_KONTROL.items():
        s.append(f"| {k} | {ad.get(k, k)} | {y} | {kn} |")
    metin = "\n".join(s) + "\n"
    YH._yh_yaz(yol, metin, "PK ön kayıt")
    return yol


def pk_kapi(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    yol = _pk_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise PKHata(f"ön kayıt yok: {yol} (python POZITIF_KONTROL.py onkayit)")
    metin = open(yol, encoding="utf-8").read(); simdi = pk_sha_simdi(veri)
    for k, v in simdi.items():
        m = re.search(rf"(?<![A-Z0-9_]){k}:\s*`([0-9a-f]{{64}})`", metin)
        if not m or m.group(1) != v:
            raise PKHata(f"{k} ön kayıttakiyle aynı değil -> koşu DURDU")
    out = {"sha": simdi, "cetvel": pk_cetvel_ayni()}
    if git:
        try:
            st = subprocess.run(["git", "status", "--porcelain", yol], cwd=KOK_PK, capture_output=True, text=True, check=True).stdout.strip()
            lg = subprocess.run(["git", "log", "-1", "--format=%H %cI", "--", yol], cwd=KOK_PK, capture_output=True, text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as ex:
            raise PKHata(f"git denetimi yapılamadı: {ex}") from ex
        if st or not lg:
            raise PKHata(f"ön kayıt git'e işlenmemiş ya da değişmiş ({st or 'kayıt yok'}) -> koşu DURDU")
        out["git_onkayit"] = lg
    if kontrol:
        import IZ_KARNE as IK
        out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
    pklog.info("pk_kapi AÇIK (%s)", yol)
    return out


# ================================================================ 6) KOŞU ve RAPOR
def _pk_jsonla(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _pk_jsonla(v) for k, v in o.items() if not str(k).startswith("_")}
    if isinstance(o, (list, tuple)):
        return [_pk_jsonla(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, _dt.datetime, _dt.date)):
        return str(o)
    return o


def pk_kos(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, git: bool = True, kontrol: bool = True,
           tohum_sayi: Optional[int] = None) -> Dict[str, Any]:
    c = cikti or PK_YOL["cikti"]; t0 = time.time()
    if os.path.exists(_pk_yol("json", c)):
        raise PKHata(f"sonuç zaten var: {_pk_yol('json', c)} (ikinci koşu DURUR)")
    kapi = pk_kapi(c, veri, git, kontrol); bas = _pk_simdi()
    J: Dict[str, Any] = {"surum": PK_SURUM, "kapi": kapi, "baslangic": bas}
    Ra = pk_a_kos(islem, veri, tohum_sayi=tohum_sayi)
    J["A"] = {"say": Ra["say"], "ozet": pk_a_ozet(Ra["satir"]), "satir": Ra["satir"].to_dict("records")}
    J["yeniden_A"] = pk_yeniden_a(_PK_A["ABD"], c)
    _PK_A.clear()
    Rb = pk_b_kos(islem, veri)
    S = pd.concat(Rb["satir"], ignore_index=True); S.to_csv(_pk_yol("b_satir", c), index=False, compression="gzip")
    J["B"] = {"sonuc": Rb["sonuc"], "yayilim": Rb["yayilim"], "say": Rb["say"]}
    J["yeniden_B"] = pk_yeniden_b(Rb["_yu"], pd.read_csv(_pk_yol("b_satir", c), parse_dates=["giris", "tarih"]), Rb["sonuc"])
    J["C"] = pk_c_kos(veri)
    pd.DataFrame([{k: v for k, v in r.items() if not isinstance(v, dict)} for r in J["C"]]).to_csv(_pk_yol("c_satir", c), index=False)
    J["bitis"] = _pk_simdi(); J["sure_sn"] = round(time.time() - t0, 1)
    ya, yb = J["yeniden_A"], J["yeniden_B"]
    if not (ya["fark_esit"] and not ya["elle_bozuk"] and yb["esit"] and not yb["elle_bozuk"] and not yb["elle_es_bozuk"]):
        J["yeniden_uretim_durum"] = "TUTMADI"
    else:
        J["yeniden_uretim_durum"] = "TUTTU"
    YH._yh_yaz(_pk_yol("json", c), json.dumps(_pk_jsonla(J), ensure_ascii=False, indent=1, default=YH._yh_json), "PK json")
    J["rapor"] = pk_rapor(c)
    if J["yeniden_uretim_durum"] != "TUTTU":
        raise PKHata(f"yeniden üretim TUTMADI: A {ya['fark_esit']} / {ya['elle_bozuk'][:3]}; B {yb['esit']} / {yb['elle_bozuk'][:3]} / {yb['elle_es_bozuk'][:3]}")
    return J


def _pk_z(x: Dict[str, Any]) -> float:
    """Gösterim: FARK / (boot %95 yarı genişliği / 1,96)."""
    try:
        f, a, u = float(x.get("fark")), float(x.get("boot_alt")), float(x.get("boot_ust"))
    except (TypeError, ValueError):
        return float("nan")
    return f / ((u - a) / 2 / 1.959963984540054) if np.isfinite(f) and u > a else float("nan")


def _pk_y(x: Any, n: int = 1, isaret: bool = True) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    return (f"{100 * v:+.{n}f}" if isaret else f"{100 * v:.{n}f}").replace(".", ",")


def _pk_s(x: Any, n: int = 3) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(v) else f"{v:.{n}f}".replace(".", ",")


def pk_rapor(cikti: Optional[str] = None) -> str:
    c = cikti or PK_YOL["cikti"]; J = json.load(open(_pk_yol("json", c), encoding="utf-8"))
    Ea = PK_ESIK["A"]; s: List[str] = []
    s += [f"# POZİTİF KONTROL — RAPOR ({J['bitis']})", "",
          f"{PK_SURUM}. Ön kayıt POZITIF_KONTROL_ON_KAYIT.md (git {J['kapi'].get('git_onkayit', '-')}); koşu {J['baslangic']} .. {J['bitis']} "
          f"({J['sure_sn']} sn). Cetvel DS ile bayt bayt aynı (kod / eşik sha = DS_ON_KAYIT). h5 = 15 geçerli barda kapanışla +%5, stop'tan önce; "
          "FARK = olay h5 payı - eş h5 payı (yüzde puan). Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma).", ""]
    # A
    tab = pd.DataFrame(J["A"]["ozet"]["tablo"]); tab["nk"] = tab.nk.astype(str)
    s += ["## 1. A — YAPAY İZ: yakalama payı (20 tohum; yakalama = FARK > 0 VE boot %95 alt > 0 VE tek yönlü p < 0,05)", "",
          "Sürüklenme delta: tutan olayın 15 barına doğrusal yayılmış fiyat artışı (15. barda +delta). Hücre başına: yakalama payı (iki yönlü p ile) / "
          "ortalama ölçülen n / ortalama FARK (puan).", ""]
    nks = [str(x) for x in Ea["n"]]; des = Ea["delta"]
    for p in Ea["pazar"]:
        for h in Ea["hucre"]:
            s += [f"**{p} {h}** (DS havuzu {J['A']['say'][p]['havuz'][h]} olay; DS h5 ortalaması %{100 * J['A']['say'][p]['h5_ort'][h]:.1f})", "",
                  "| n | " + " | ".join(f"delta {('+%' + str(int(round(100 * d)))) if d else '0 (plasebo)'}" for d in des) + " |",
                  "|---|" + "---|" * len(des)]
            for nk in nks:
                row = []
                for de in des:
                    x = tab[(tab.pazar == p) & (tab.hucre == h) & (tab.nk == nk) & (np.isclose(tab.delta, de))]
                    if not len(x):
                        row.append("-"); continue
                    x = x.iloc[0]
                    row.append(f"**%{100 * x.yakala:.0f}** (%{100 * x.yakala_iki:.0f}) / {x.n:.0f} / {_pk_y(x.fark)}")
                s.append(f"| {nk} | " + " | ".join(row) + " |")
            s.append("")
    dort = pd.DataFrame(J["A"]["ozet"]["dort"]); dort["nk"] = dort.nk.astype(str)
    s += ["Dört karar hücresi (ABD + AVR x eğitim + sınama) AYNI tohumda birlikte yakalama payı (DS karne v3'ün 'her hücrede' şartının çekirdeği):", "",
          "| n | " + " | ".join(f"delta {d:+.0%}".replace("+0%", "0") for d in des) + " |", "|---|" + "---|" * len(des)]
    for nk in nks:
        row = []
        for de in des:
            x = dort[(dort.nk == nk) & np.isclose(dort.delta, de)]
            row.append(f"%{100 * x.dort_hucre.iloc[0]:.0f}" if len(x) and np.isfinite(x.dort_hucre.iloc[0]) else "-")
        s.append(f"| {nk} | " + " | ".join(row) + " |")
    s.append("")
    # düz dil A
    gor = []
    for p in Ea["pazar"]:
        for h in Ea["hucre"]:
            for de in des[1:]:
                x = tab[(tab.pazar == p) & (tab.hucre == h) & np.isclose(tab.delta, de) & (tab.yakala >= 0.8)]
                if len(x):
                    nmin = min(x.nk, key=lambda z: 10 ** 9 if z == "yari" else int(z))
                    gor.append(f"{p} {h}: delta {de:+.0%} için n >= {nmin}".replace("+", "+"))
                    break
    fp = tab[np.isclose(tab.delta, 0.0)]
    s += ["Düz dil: cetvelin bir hücrede >= %80 yakaladığı en küçük delta ve o delta'da en küçük n: " + ("; ".join(gor) if gor else "hiçbiri") + ".",
          f"Plasebo (delta 0) yanlış pozitif payı: ortalama %{100 * fp.yakala.mean():.1f} (en yüksek hücre %{100 * fp.yakala.max():.0f}); iki yönlü "
          f"p ile %{100 * fp.yakala_iki.mean():.1f}.", ""]
    S0 = pd.DataFrame(J["A"]["satir"]); S0 = S0[(S0.n > 0) & np.isclose(S0.delta.astype(float), 0.0)]
    s.append("Plasebo (delta 0) hücre başına ortalama FARK (bütün n ve tohumlar; beklenen 0) / yakalama: " + "; ".join(
        f"{p} {h} {_pk_y(g.fark.mean(), 2)} puan / %{100 * g.yakala.mean():.0f}" for (p, h), g in S0.groupby(["pazar", "hucre"])) + ".")
    s.append("")
    for p in Ea["pazar"]:
        sy = J["A"]["say"][p]
        s.append(f"- {p} sürüklenmenin ham h5'e etkisi (bütün ANA olaylar tutan olsaydı; eğitim / sınama): " + "; ".join(
            f"delta {d:+.0%}: %{100 * sy[f'h5_ort_d{d}']['egitim']:.1f} / %{100 * sy[f'h5_ort_d{d}']['sinama']:.1f}" for d in des))
    s.append("")
    # B
    s += ["## 2. B — BİLİNEN GERÇEK İZ: üç cetvel yan yana (ABD karar; AVR momentum BİLGİ)", "",
          "Kod: U = üst onda vs orta eşler; A = alt onda vs orta eşler; UA = üst onda vs aynı gün aynı kova alt onda (doğrudan). p = ay kümeli "
          "işaret permütasyonu, önceden yazılı yön (U +, A -, UA +). h5 FARK puan; r15 = stop'suz 15 bar kapanış getirisi farkı (aynı eşler); r60 = OC "
          "eşli fark (momentum x likidite eşleri). [alt, üst] = ay kümeli boot %95.", "",
          "| B | pazar | kod | hücre | n | h5 olay / eş | h5 FARK [alt, üst] | p (h5) | güç | r15 FARK [alt, üst] | p (r15) | r60 FARK [alt, üst] | p (r60) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in J["B"]["sonuc"]:
        h5, r15, r60 = r["h5"], r["r15"], r["r60"]
        s.append(f"| {r['kod'][:2]} | {r['pazar']}{' (bilgi)' if r.get('bilgi') else ''} | {r['kod'][2:]} | {r['hucre']} | {h5.get('n', 0)} | "
                 f"{_pk_y(h5.get('p_olay'), 1, False)} / {_pk_y(h5.get('p_es'), 1, False)} | {_pk_y(h5.get('fark'))} [{_pk_y(h5.get('boot_alt'))}, {_pk_y(h5.get('boot_ust'))}] | "
                 f"{_pk_s(h5.get('p'), 4)} | {_pk_s(h5.get('guc'), 2)} | {_pk_y(r15.get('fark'), 2)} [{_pk_y(r15.get('boot_alt'), 2)}, {_pk_y(r15.get('boot_ust'), 2)}] | "
                 f"{_pk_s(r15.get('p'), 4)} | {_pk_y(r60.get('fark'), 2) if r60.get('n') else '-'} "
                 f"[{_pk_y(r60.get('boot_alt'), 2) if r60.get('n') else '-'}, {_pk_y(r60.get('boot_ust'), 2) if r60.get('n') else '-'}] | "
                 f"{_pk_s(r60.get('p'), 4) if r60.get('n') else '-'} |")
    s += ["", "U - A yayılımı (her biri orta eşlere göre; ay kümeli ortak boot %95):", "",
          "| B | pazar | hücre | h5 yayılım [alt, üst] | r15 yayılım [alt, üst] | r60 yayılım [alt, üst] |", "|---|---|---|---|---|---|"]
    for y in J["B"]["yayilim"]:
        s.append(f"| {y['kod']} | {y['pazar']} | {y['hucre']} | {_pk_y(y['h5']['yayilim'])} [{_pk_y(y['h5']['alt'])}, {_pk_y(y['h5']['ust'])}] | "
                 f"{_pk_y(y['r15']['yayilim'], 2)} [{_pk_y(y['r15']['alt'], 2)}, {_pk_y(y['r15']['ust'], 2)}] | "
                 f"{_pk_y(y['r60']['yayilim'], 2)} [{_pk_y(y['r60']['alt'], 2)}, {_pk_y(y['r60']['ust'], 2)}] |")
    s += ["", "Duyarlılık (aynı olaylar; z = FARK / (boot %95 yarı genişliği / 1,96); işaret beklenen yönle karşılaştırılır):", "",
          "| B | pazar | kod | hücre | beklenen | z h5 | z r15 | z r60 |", "|---|---|---|---|---|---|---|---|"]
    for r in J["B"]["sonuc"]:
        yon = PK_ESIK["B"][r["kod"][:2]]["yon"][r["kod"][2:]]
        s.append(f"| {r['kod'][:2]} | {r['pazar']} | {r['kod'][2:]} | {r['hucre']} | {yon} | " + " | ".join(_pk_s(_pk_z(r[c]), 2) for c in ("h5", "r15", "r60")) + " |")
    sb = J["B"]["say"]
    s += ["", "Huni: " + "; ".join(f"{k}: sinyal {v.get('girdi')}, havuz olay {v.get('olay_havuz')}, U {v.get('U')}, A {v.get('A')}, ANA {v.get('ana_donem')}"
                                 for k, v in sb.items() if isinstance(v, dict) and "girdi" in v)]
    if "B2_esik" in sb:
        e = sb["B2_esik"]
        s.append(f"PEAD onda sınırları (eğitim {e['n_egitim']} tepki): q10 {_pk_y(e['q10'], 2)}, q90 {_pk_y(e['q90'], 2)}. sec_ozet ham satır örnekleri: "
                 + " | ".join(e.get("ornek", [])))
    s.append("")
    # C
    s += ["## 3. C — ÖRNEKLER (her biri n = 1; bulgu denmez, tek tek okunur)", "",
          "| örnek | sinyal (kaynak) | giriş | stop uzaklığı | h5 | h10 | st5 | takip getirisi | çıkış barı (tür) | r15 | neden |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in J["C"]:
        if r.get("durum") != "ölçüldü":
            s.append(f"| {r['ornek']} | {r.get('sinyal', '-')} ({r.get('kaynak', '-')}) | - | - | - | - | - | - | - | - | {r.get('neden', '-')} |"); continue
        s.append(f"| {r['ornek']} | {r['sinyal']} ({r['kaynak']}) | {r['giris']} | %{100 * r['d']:.1f} | {int(r['h5'])} | {int(r['h10'])} | {int(r['st5'])} | "
                 f"{_pk_y(r['getiri'])} | {r['cikis_bar']} ({r['cikis_tur']}) | {_pk_y(r['r15'])} | {r['neden']} |")
    s += ["", "Ek satırlar: S6 sinyalinde hat = 20 bar dip ile; Ekim kazananlarında ESLER geometrisi (adayın stop uzaklığı):", ""]
    for r in J["C"]:
        for k, ad in (("hat20", "20 bar dip hattı"), ("esler_geo", "ESLER geometrisi")):
            if isinstance(r.get(k), dict):
                x = r[k]
                s.append(f"- {r['ornek']} ({ad}): d %{100 * (x.get('d') or 0):.1f}, h5 {x.get('h5')}, h10 {x.get('h10')}, st5 {x.get('st5')}, "
                         f"getiri {_pk_y(x.get('getiri'))}, çıkış barı {x.get('cikis_bar')}" + (f"; {x['neden']}" if x.get("neden") else ""))
    s.append("")
    # SONUÇ
    s += ["## 4. SONUÇ", "", pk_sonuc_metni(J), ""]
    # YENİDEN ÜRETİM
    ya, yb = J["yeniden_A"], J["yeniden_B"]
    s += ["## 5. YENİDEN ÜRETİM", "",
          f"- A hücresi {ya['hucre']} (pazar, hücre, n, delta, tohum): kod FARK {_pk_y(ya['kod_fark'], 3)} puan, satır dosyasından düz pandas "
          f"{_pk_y(ya['dosya_fark'], 3)} (n {ya['n_kod']} / {ya['n_dosya']}) -> {'EŞİT' if ya['fark_esit'] else 'FARKLI'}; {ya['elle_n']} tutan olayın "
          f"sürüklenmiş h5'i yh_sim'den bağımsız düz döngüyle: bozuk {len(ya['elle_bozuk'])}.",
          f"- B hücresi {yb['hucre']}: kod h5 FARK {_pk_y(yb['kod_fark'], 3)} / dosya {_pk_y(yb['dosya_fark'], 3)}; r15 FARK kod {_pk_y(yb['kod_r15'], 3)} / "
          f"dosya {_pk_y(yb['dosya_r15'], 3)} -> {'EŞİT' if yb['esit'] else 'FARKLI'}; {yb['elle_n']} olayın h5 ve r15'i düz döngüyle: bozuk "
          f"{len(yb['elle_bozuk'])}; {yb['elle_es_n']} olayın eş h5'i (eş kümesi elle: aynı gün, aynı kova, orta, havuzda, adayın d'si) bozuk "
          f"{len(yb['elle_es_bozuk'])}.", f"- Durum: **{J['yeniden_uretim_durum']}**.", ""]
    s += ["## 6. HATA", "", "Koşu sırasında bulunan hatalar ve sınırlar (ayrıntı alt ajan raporunda):", ""] + [f"- {x}" for x in PK_HATA_NOT] + [""]
    s += ["## 7. KONTROL LİSTESİ (K1-K14)", "", "| Kod | Yanıt | Kanıt |", "|---|---|---|"] + [f"| {k} | {y} | {kn} |" for k, (y, kn) in PK_KONTROL.items()]
    metin = "\n".join(s) + "\n"
    YH._yh_yaz(_pk_yol("rapor", c), metin, "PK rapor")
    return metin


PK_HATA_NOT: List[str] = [
    "Ekim 2026 kazananları (C) /tmp/veri'de yok (V_ABD 22 Eki'de biter, kriz kesiği 31.08.2026); CANLI_SONUC ile aynı kaynak /tmp/veri_canli "
    "kullanıldı ve kriz kesiği YALNIZ bu bilgi satırında aşıldı (iş tanımı 'yalnız /tmp/veri' dedi: SAPMA, bilgi satırı).",
    "B1 eğitim hücresi V_ABD 2015-06 başlangıcı yüzünden 252 bar geçmiş ancak 2016 ortasından itibaren var (eğitim ilk ayları eksik).",
    "B2 PEAD tepki vekili 2 günlük artık getiri (analist sürprizi değil); 8-K 2.02 bilanço dışı (ara duyuru) başvuruları da içerir.",
    "B'de ambargo yok (önceden yazılı gerekçe: eşikler sonuç kullanmaz); A DS ambargosunu aynen taşır.",
    "A plasebosunda AVR sınama hücresi sıfır değil: rastgele 'tutan' kümesi DS içi eşlere göre ortalama +2,2 puan FARK veriyor (n 100'de "
    "yanlış pozitif %20, yarıda %15). Rastgele etiket altında bu fark DS içi eş geometrisinden (eşler olayın stop uzaklığıyla ölçülür) ve "
    "küçük hücreden geliyor; DS raporundaki AVR sınama FARK'larının çoğunun pozitif olması bununla okunmalı (cetvel bulgusu).",
    "A'da AVR sınama n = 1000 ölçülmedi: havuz 1.206 olay, önceden yazılı tavan (tutan <= havuzun 2/3'ü = 804).",
    "C: BINBN-24 ve KTLEV-24 için kutu sonu penceresinde S6 'al' yok; 120 gün kuralı veri kısa olduğu için (BINBN 2024-10, KTLEV 2024-03 "
    "başlıyor) ancak 2025-04-03 / 2024-12-12'de sinyal verdi: Cemal'in kırılım günü değil, bu iki satır onun örneğinin sınaması sayılmaz.",
    "Ön kayıttan önce gerçek veride yalnız getirisiz duman denemesi yapıldı (B sinyal / huni sayıları, C sinyal günleri; h5 / getiri "
    "hesaplanmadı).",
    "Rapor gösterimi koşudan SONRA genişletildi (plasebo hücre satırı, z duyarlılık tablosu, ters yön satırı, bu HATA maddeleri); hesap kodu ve "
    "pozitif_kontrol.json değişmedi (gösterim; ön kayıttaki PK_KOD_SHA koşu anındaki koddur).",
]


def pk_sonuc_metni(J: Dict[str, Any]) -> str:
    """Önceden yazılı okuma kuralıyla (ön kayıt bölüm 2) SONUÇ satırları."""
    tab = pd.DataFrame(J["A"]["ozet"]["tablo"]); tab["nk"] = tab.nk.astype(str)
    yari = tab[tab.nk == "yari"]
    kucuk_d = []
    for de in PK_ESIK["A"]["delta"][1:]:
        x = yari[np.isclose(yari.delta, de)]
        if len(x) and (x.yakala >= 0.8).all():
            kucuk_d.append(de)
    a_d = min(kucuk_d) if kucuk_d else None
    fp = float(tab[np.isclose(tab.delta, 0.0)].yakala.mean())
    gorunur = {}
    for r in J["B"]["sonuc"]:
        if r.get("bilgi"):
            continue
        for cet in ("h5", "r15", "r60"):
            x = r[cet]
            if not x.get("n"):
                continue
            yon = PK_ESIK["B"][r["kod"][:2]]["yon"][r["kod"][2:]]
            ok = x.get("fark") is not None and x.get("p") is not None and ((x["fark"] > 0) if yon == "+" else (x["fark"] < 0)) and x["p"] < 0.05
            gorunur.setdefault((r["kod"], cet), []).append(bool(ok))
    gor = {k: all(v) and len(v) == 2 for k, v in gorunur.items()}
    b_h5 = [k[0] for k, v in gor.items() if v and k[1] == "h5"]; b_dz = [k for k, v in gor.items() if v and k[1] != "h5"]
    if a_d is None:
        karar = "HAYIR"
    elif b_h5:
        karar = "EVET"
    else:
        karar = "KISMEN"
    ters = []
    for r in J["B"]["sonuc"]:
        if r.get("bilgi"):
            continue
        yon = PK_ESIK["B"][r["kod"][:2]]["yon"][r["kod"][2:]]
        for cet in ("h5", "r15", "r60"):
            x = r[cet]
            if not x.get("n") or x.get("boot_alt") is None or x.get("boot_ust") is None:
                continue
            if (yon == "+" and x["boot_ust"] < 0) or (yon == "-" and x["boot_alt"] > 0):
                ters.append(f"{r['kod']}/{cet} {r['hucre']} ({_pk_y(x['fark'], 2)}, boot [{_pk_y(x['boot_alt'], 2)}, {_pk_y(x['boot_ust'], 2)}])")
    satir = [f"**Cetvel bilinen izi görüyor mu: {karar}** (ön kayıt bölüm 2 kuralı).",
             f"- A: gerçek DS boyutunda (yari) dört hücrede de >= %80 yakalanan en küçük sürüklenme: {('+%' + str(round(100 * a_d))) if a_d else 'yok (delta +%5 bile)'}; "
             f"plasebo yanlış pozitif ortalama %{100 * fp:.1f}.",
             f"- B: iki dönemde de beklenen yönde ve p < 0,05 olan (kod, cetvel): " + (", ".join(f"{k}/{c}" for (k, c), v in gor.items() if v) or "yok") + ".",
             "- Beklenen yönün TERSİNE boot aralığı sıfırı dışlayan (kod, cetvel, hücre): " + ("; ".join(ters) or "yok") + ".",
             "- Hangi cetvel daha duyarlı: duyarlılık tablosu (z) aynı olaylarda h5 / r15 / r60'ı yan yana koyar; A'da delta'nın h5'e "
             "dönüşümü (sürüklenme satırları) h5'in fiyat sürüklenmesini ne kadar seyrelttiğini gösterir."]
    return "\n".join(satir)


# ================================================================ ÇAKIŞMA KAPISI
def _cakisma_kontrol_pk(_once=_CK_ONCE_PK, _dosya="POZITIF_KONTROL.py"):
    """Çakışma kapısı: bu dosya bellekteki pk_ / PK_ / _pk öneki DIŞINDAKİ mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_PK", "_CK_KAYIT", "_cakisma_kontrol_pk", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "subprocess", "_dt", "annotations",
           "Any", "Dict", "List", "Optional", "Tuple", "OC", "YH", "DS")
    onek = ("pk_", "PK_", "_pk", "PKHata", "pklog", "_PK", "KOK_PK")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std and not k.startswith(onek))
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_pk()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=PK_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "sha"])
    ap.add_argument("--islem", type=int, default=1)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--gitsiz", action="store_true")
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(pk_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            R_ = pk_kos(a.cikti, a.veri, a.islem, git=not a.gitsiz)
            print(R_["rapor"][:6000])
        elif a.komut == "rapor":
            print(pk_rapor(a.cikti))
        else:
            print(json.dumps(pk_sha_simdi(a.veri), indent=1))
    except (PKHata, DS.DSHata, OC.OCHata) as ex:
        pklog.error("%s", ex); sys.exit(1)
