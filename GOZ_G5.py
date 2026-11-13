"""GOZ_G5 — VDYT2 G5 "sessiz bölge" dedektörünü Cemal'in DAHA ÖNCE gözle işaretlediği çöl bölgelerine karşı sınama (13 Kasım 2026). Tek dosya.

Bağlam: kör testte (KOR_TEST v1.1) Cemal 40 grafiğe bakıp 'hiçbir belirti / özellik yok, rastgele seçilen bölge' dedi (Ç166, İŞARET YOK). Yeni işaret
istemeden dedektör, Cemal'in elle verdiği mevcut göz etiketlerine karşı sınanır:
  ANA SET  kalibre_etiketler.csv (sembol, bas, son, sinif: 30 COL + 8 OLUMSUZ; Cemal, 18 Eylül 2026, COL_OZET §7)
  C SETİ   goz_esle/etiket_2026-10-20.csv (21 kutu, Cemal 21 Eki: hepsi DEĞİL) + goz_esle/etiket_obek_ARZUM.csv (4 öbek: 3 OBEK, 1 DEĞİL; Cemal 21 Eki)
  DIŞARIDA COL_GOZ 746 / 150 kutu (arastirma_cikti/col_goz): 'benim' kararları Claude'un gözü; Cemal'in 22 Eki EVET / HAYIR dosyası
           (col_goz_cemal_2024_26.csv) repoda yok -> kullanılmaz.

TEST A  G5 göze uyuyor mu: bölge içi G5 gün oranı >= 0,50 = yakaladı (ana), >= 1 gün (bilgi); COL vs OLUMSUZ vs RASTGELE (her COL bölgesine aynı hisseden,
        aynı uzunlukta, hiçbir Cemal etiketiyle kesişmeyen 20 pencere, sabit tohum); hisse kümeli bootstrap %95.
TEST B  10 basit pencere ölçüsü: AUC (COL vs RASTGELE, COL vs OLUMSUZ), hisse dışarıda bırakmalı (LOSO) AUC; aday varsa en çok iki ölçülü eşik kuralı.
TEST C  B'nin adayı C setinde (aynı eşikler): DEĞİL'de yanlış alarm, OBEK'te yakalama (bilgi).
Eşikler GOZ_ESIK'te; sha256 mührü ön kayıtta (arastirma_cikti/goz_g5/GOZ_G5_ON_KAYIT.md). Ön kayıt git'e işlenmeden `kos` çalışmaz.

SINIR: VDYT2.py, VDYT.py, KOR_TEST.py, kalibre_etiketler.csv, goz_esle/ DEĞİŞMEZ (yalnız okunur / içe aktarılır). Ağ yok, Tiingo yok, e-posta / anahtar yok.
Veri: V_BIST.pkl (V2.v2_fiyat: test kesik 31.08.2026; C seti canlı seri, veri sonu). PNG / veri repoya girmez (grafikler /tmp/goz_g5/grafik).

Komut:  python GOZ_G5.py onkayit         ön kaydı yazar (eşik mührü, kod / VDYT2 / etiket / veri sha256, etiket sayımı; varsa üzerine yazmaz)
        python GOZ_G5.py kos [--sapma M]  ön kayıt git'te ve mühür tutuyorsa ölçüm -> goz_g5_sonuc.json + GOZ_G5_RAPOR.md (kod değiştiyse --sapma şart)
        python GOZ_G5.py grafik          6 PNG (3 COL + 3 RASTGELE; KOR_TEST v1.1 kor_ciz_fig11) -> /tmp/goz_g5/grafik
        python GOZ_G5.py rapor           raporu sonuç JSON'undan yeniden yazar
Colab:  exec(open('GOZ_G5.py').read())  (VDYT.py, VDYT2.py, VDYT2B.py, KOR_TEST.py aynı klasörde)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_GOZ = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_GOZ = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_GOZ not in sys.path:
    sys.path.insert(0, KOK_GOZ)
import VDYT as V1  # noqa: E402  (DEĞİŞTİRİLMEZ)
import VDYT2 as V2  # noqa: E402  (G5 dedektörü; DEĞİŞTİRİLMEZ)

gozlog = logging.getLogger("col.goz_g5")
if not gozlog.handlers:
    _goz_h = logging.StreamHandler(sys.stderr)
    _goz_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s goz_g5: %(message)s", "%H:%M:%S"))
    gozlog.addHandler(_goz_h)
    gozlog.setLevel(logging.INFO)
    gozlog.propagate = False

GOZ_ETIKET = "goz_g5_20261113"
GOZ_SURUM = "GOZ_G5 v1.0 (goz_g5_20261113): G5 x Cemal'in mevcut göz etiketleri (Test A / B / C; ön kayıtlı)"

GOZ_YOL: Dict[str, str] = {
    "cikti": os.environ.get("GOZ_CIKTI", os.path.join(KOK_GOZ, "arastirma_cikti", "goz_g5")),
    "grafik": os.environ.get("GOZ_GRAFIK", "/tmp/goz_g5/grafik"),
    "ana": os.path.join(KOK_GOZ, "kalibre_etiketler.csv"),
    "c_kutu": os.path.join(KOK_GOZ, "goz_esle", "etiket_2026-10-20.csv"),
    "c_obek": os.path.join(KOK_GOZ, "goz_esle", "etiket_obek_ARZUM.csv"),
}
GOZ_DOSYA: Dict[str, str] = {"onkayit": "GOZ_G5_ON_KAYIT.md", "sonuc": "goz_g5_sonuc.json", "rapor": "GOZ_G5_RAPOR.md"}
_GOZ_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256 mührü ön kayıtta; sonuç görüldükten sonra değişmez)
GOZ_ESIK: Dict[str, Any] = {
    "surum_etiket": GOZ_ETIKET,
    "vdyt2": {"kod_sha256": "e33b2fd1c611e32930e8e8af29b9a4a9e86607a1df303e0fae8d9e94d0a30741",      # VDYT2 ön kaydındaki KOD_SHA256 (dedektör aynen)
              "vdyt_kod_sha256": "10ead8062c2c8ec25984a23b68b299cec4d8a7cfd144ad22e542e867d40c932d",
              "durum": "G5", "tanim": "G1 küçük mum VE G2 dar bant VE (G3 tepe/dip eğimi YA DA G4 gövde savunma hattı); V2.v2_olculer, değiştirilmeden",
              "fiyat_ana": "V2.v2_fiyat('BIST') test serisi (kesik 2026-08-31)", "fiyat_c": "V2.v2_fiyat('BIST', canli=True) (veri sonu; C seti BİLGİ)",
              "tanimsiz": "G5'in geçmişi yetmeyen günleri (ATRref / bant referansı NaN) dedektörün kendi davranışıyla YANLIŞ sayılır (ANA); tanımlı gün "
                          "oranı >= 0,50 olan bölgelerle yeniden hesap BİLGİ"},
    "etiket": {
        "ana": {"dosya": "kalibre_etiketler.csv", "siniflar": {"COL": "COL", "OLUMSUZ": "OLUMSUZ"}, "kaynak": "Cemal gözle, 18 Eylül 2026 (COL_OZET §7)"},
        "c": {"dosyalar": ["goz_esle/etiket_2026-10-20.csv", "goz_esle/etiket_obek_ARZUM.csv"],
              "sinif": "etiket_2026-10-20 'cemal' sütunu 'DEGIL' ile başlıyorsa DEGIL; etiket_obek_ARZUM 'cemal' 'OBEK' ile başlıyorsa OBEK, 'DEGIL' ise DEGIL",
              "kaynak": "Cemal gözle, 21 Ekim 2026 (COL_OZET §9.8)", "ortusme": "kalibre setiyle aynı hisse ve kesişen tarihli kutu C'den çıkarılır"},
        "disarida": "COL_GOZ (arastirma_cikti/col_goz): 'benim' sınıfları Claude'un gözü; Cemal'in 150 kutuluk EVET / HAYIR dosyası repoda yok",
        "gun": "bölge = serinin [bas, son] (dahil) aralığındaki işlem günleri; hafta sonu tarihleri sorun değil; 0 gün = VERİ DIŞI (sayılır, dışarıda)",
    },
    "A": {
        "yakalama_pay": 0.50, "bilgi_en_az_gun": 1,
        "rastgele": {"n": 20, "tohum": 20261113, "bas_tarih": "2022-01-01", "ilk_bar": 260,
                     "kural": "her COL bölgesi için aynı hisseden, aynı işlem günü uzunluğunda, başı >= bas_tarih ve >= ilk_bar, sonu <= seri sonu (test kesiği), "
                              "tarih aralığı hiçbir Cemal etiketiyle (ana + C setleri, COL / OLUMSUZ / DEĞİL / OBEK) kesişmeyen pencereler; başlangıçlar "
                              "uygun başlangıçlardan tekrarsız düzgün çekilir (tohum = sha256(tohum|sembol|bas)); uygun < n ise hepsi alınır (sayılır)"},
        "karar": {"uyuyor": {"col_min": 0.70, "rastgele_kat": 2.0, "olumsuz_ustu": True},
                  "zayif": {"col_min": 0.50, "rastgele_kat": 1.5},
                  "metin": "G5 GÖZE UYUYOR <=> yak(COL) >= 0,70 VE yak(COL) >= 2 x yak(RASTGELE) VE yak(COL) > yak(OLUMSUZ); ZAYIF <=> yak(COL) >= 0,50 VE "
                           "yak(COL) > 1,5 x yak(RASTGELE); değilse UYMUYOR (nokta tahminleri)"},
        "bootstrap": {"B": 2000, "tohum": 20261114, "kume": "hisse (COL, OLUMSUZ ve RASTGELE satırları hisseleriyle birlikte çekilir)", "guven": [2.5, 97.5]},
    },
    "B": {
        "olculer": ["aralik_kapanis", "aralik_atr", "kapanis_bant", "govde_atr", "uzunluk", "dusus120", "hacim_oran", "sma50_egim", "dip_savunma", "konum250"],
        "tanim": {
            "aralik_kapanis": "bölge içi medyan (H-L)/Kapanış",
            "aralik_atr": "bölge içi medyan (H-L) / ATR250 (ATR250 = bölge başından ÖNCEKİ en çok 250 günün ortalama gerçek aralığı, en az 60 gün)",
            "kapanis_bant": "(bölge maks kapanış - min kapanış) / bölge medyan kapanış",
            "govde_atr": "bölge içi medyan |C-O| / ATR250",
            "uzunluk": "bölge işlem günü sayısı (RASTGELE aynı uzunlukta: COL vs RASTGELE AUC tanım gereği 0,50)",
            "dusus120": "bölge başından önceki gün kapanışı / önceki 120 günün en yüksek kapanışı - 1 (en az 60 gün)",
            "hacim_oran": "bölge medyan hacmi / bölgeden önceki 250 gün medyan hacmi (en az 60 gün, payda > 0)",
            "sma50_egim": "100 x ln(SMA50[son] / SMA50[bas]) / max(son-bas, 1) (bar başına %)",
            "dip_savunma": "bölge içi en düşük 3 dip (Low'lar küçükten büyüğe, seçilenlerden >= 5 bar uzak olan alınır) arasındaki uzaklık (maks-min) / ATR250; "
                           "3 dip bulunamazsa NaN",
            "konum250": "(bölge medyan kapanışı - 250 günlük min Low) / (250 günlük maks High - min Low); 250 gün bölge sonunda biter (en az 120 gün)",
        },
        "atr_n": 250, "atr_min": 60, "hacim_n": 250, "hacim_min": 60, "dusus_n": 120, "dusus_min": 60, "sma": 50, "konum_n": 250, "konum_min": 120,
        "dip": {"k": 3, "ayrim": 5},
        "auc": "P(COL > karşı) + 0,5 P(eşit) (Mann-Whitney); NaN satır o ölçüde dışarıda",
        "loso": "her COL hissesi sırayla dışarıda: yön (+1 büyük = çöl / -1) kalan hisselerin COL vs RASTGELE AUC'sinden (>= 0,5 -> +1); dışarıdaki hissenin "
                "COL ve RASTGELE satırları yön x değer ile puanlanır; bütün dışarıdaki puanlar havuzlanıp AUC",
        "olumsuz_auc": "COL vs OLUMSUZ AUC, yön tam örneklem COL vs RASTGELE yönüyle sabit (yönlü AUC)",
        "aday": {"loso_rastgele_min": 0.80, "olumsuz_min": 0.70, "metin": "GÖZ ÖLÇÜSÜ ADAYI <=> LOSO AUC(COL vs RASTGELE) >= 0,80 VE yönlü AUC(COL vs OLUMSUZ) >= 0,70"},
        "kural": {"sart": "yalnız en az bir tek ölçü aday çıkarsa", "yuzdelik": [20, 80], "en_fazla_olcu": 2,
                  "esik": "yön +1: değer >= COL'un %20 yüzdeliği; yön -1: değer <= COL'un %80 yüzdeliği (eğitim COL satırlarından)",
                  "adaylar": "her aday ölçü tek başına + her aday ölçü ile öteki 9 ölçüden biri (VE)",
                  "loso": "eşik ve yön dışarıdaki hisse hariç eğitimden; J = yakalama(COL) - geçme(RASTGELE), dışarıdaki hisselerde havuzlu",
                  "secim": "en yüksek J'li tek ölçü kuralı; iki ölçülü kural ancak J'si en iyi tek ölçününkini >= 0,05 geçerse seçilir (basit önce)"},
    },
    "C": {
        "sart": "Test B'de seçilen kural varsa; yoksa 'C YAPILMADI (B'de aday yok)'",
        "esik": "seçilen kuralın tam ana setten (bütün COL) eşik ve yönü, aynen",
        "karar": {"degil_max": 0.30, "fark_min": 0.30,
                  "metin": "C TUTTU <=> geçme(DEĞİL) <= 0,30 VE geçme(DEĞİL) <= LOSO yakalama(COL) - 0,30; değilse C TUTMADI; OBEK yakalaması BİLGİ (n küçük)"},
        "g5_bilgi": "G5 yakalaması (Test A tanımı) C setinde her durumda BİLGİ olarak yazılır",
        "kriz_notu": "C kutularının çoğu 31.08.2026 sonrası (fon krizi dönemi): yalnız şekil ölçülür, getiri yok; karar dışı sayılmaz ama raporda belirtilir",
    },
    "grafik": {"col": 3, "rastgele": 3, "tohum": 20261115, "bar": 250, "sag_ek": 20, "cizim": "KOR_TEST v1.1 kor_ciz_fig11 (ortak log ölçek)",
               "secim": "COL: COL bölgelerinden tohumlu sırayla ilk 3; RASTGELE: bütün rastgele pencerelerden tohumlu sırayla ilk 3 (önce farklı hisse); "
                         "kor_pencere11 penceresi (en az 120 kesintisiz bar) kurulamayan atlanır",
               "isaret": "bölge açık sarı gölge; G5 günleri fiyat panelinin altında siyah çizgi; hisse adı / tarih / başlık yok", "klasor": "/tmp/goz_g5/grafik"},
}


class GozHata(RuntimeError):
    """GOZ_G5'e özgü durdurucu hata (ön kayıt yok / değişmiş / git'e işlenmemiş, mühür / kod sha256 tutmuyor, veri / etiket eksik)."""


# ---------------------------------------------------------------- 0) YARDIMCILAR
def _goz_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _goz_yol(ad: str, kl: Optional[str] = None) -> str:
    return os.path.join(kl or GOZ_YOL["cikti"], GOZ_DOSYA.get(ad, ad))


def _goz_yaz(yol: str, metin: str) -> str:
    if _GOZ_EPOSTA.search(metin):
        raise GozHata(f"{os.path.basename(yol)}: metinde e-posta biçimli parça var; yazılmadı")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _goz_kayit(x: Any) -> Any:
    if isinstance(x, pd.DataFrame):
        return [_goz_kayit(r) for r in x.to_dict(orient="records")]
    if isinstance(x, dict):
        return {str(k): _goz_kayit(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_goz_kayit(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        x = x.item()
    if isinstance(x, float) and not np.isfinite(x):
        return None
    if isinstance(x, pd.Timestamp):
        return str(x.date())
    if isinstance(x, _dt.date):
        return str(x)
    return x


def _goz_json(yol: str, obj: Any) -> str:
    return _goz_yaz(yol, json.dumps(_goz_kayit(obj), ensure_ascii=False, indent=1, sort_keys=True, default=str))


def _goz_json_oku(yol: str) -> Any:
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as ex:
        raise GozHata(f"{yol} okunamadı ({type(ex).__name__}: {ex})") from ex


def goz_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for p in iter(lambda: f.read(1 << 20), b""):
            h.update(p)
    return h.hexdigest()


def goz_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: GOZ_ESIK (sıralı JSON) + VDYT2'nin G5'i belirleyen eşikleri (sessiz, atr_ref, savunma)."""
    s = json.dumps({"GOZ": E or GOZ_ESIK, "VDYT2": {k: V2.VDYT2_ESIK[k] for k in ("sessiz", "atr_ref", "savunma")}},
                   sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def goz_kod_sha(yol: Optional[str] = None) -> str:
    return goz_sha_dosya(yol or os.path.join(KOK_GOZ, "GOZ_G5.py"))


def goz_vdyt2_denetim(E: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """VDYT2.py / VDYT.py ön kayıttaki dedektörle aynı mı (değilse durur)."""
    E = E or GOZ_ESIK; a, b = V2.v2_kod_sha(), V2.v2_v1_kod_sha()
    if a != E["vdyt2"]["kod_sha256"] or b != E["vdyt2"]["vdyt_kod_sha256"]:
        raise GozHata(f"VDYT2.py / VDYT.py değişmiş (vdyt2 {a[:12]}, vdyt {b[:12]}); G5 dedektörü ön kayıttakiyle aynı değil")
    return {"vdyt2": a, "vdyt": b}


def goz_git_durum(yol: str) -> Dict[str, str]:
    """Dosya git'e işlenmiş ve çalışma kopyası HEAD ile aynı mı? Değilse GozHata. Döner son commit ve zamanı."""
    kl = os.path.dirname(os.path.abspath(yol)); ad = os.path.basename(yol)
    try:
        r = subprocess.run(["git", "-C", kl, "ls-files", "--error-unmatch", ad], capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            raise GozHata(f"{ad} git'e işlenmemiş (ön kayıt önce commit edilmeli)")
        r = subprocess.run(["git", "-C", kl, "diff", "--quiet", "HEAD", "--", ad], capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            raise GozHata(f"{ad} işlenmiş sürümden farklı (commit sonrası değişmiş)")
        r = subprocess.run(["git", "-C", kl, "log", "-1", "--format=%H|%cI", "--", ad], capture_output=True, text=True, timeout=30)
        h, z = (r.stdout.strip().split("|") + [""])[:2]
        if not h:
            raise GozHata(f"{ad}: git geçmişi yok")
        return {"commit": h, "commit_zamani": z}
    except (OSError, subprocess.SubprocessError) as ex:
        raise GozHata(f"git denetimi yapılamadı ({type(ex).__name__}: {ex})") from ex


# ---------------------------------------------------------------- 1) ETİKETLER (yalnız Cemal'in gözle verdikleri)
def goz_etiket_ana(yol: Optional[str] = None) -> pd.DataFrame:
    """kalibre_etiketler.csv -> (id, sembol, bas, son, sinif in {COL, OLUMSUZ}, kaynak). Bilinmeyen sınıf / ters tarih -> durur."""
    yol = yol or GOZ_YOL["ana"]
    try:
        K = pd.read_csv(yol)
    except (OSError, ValueError) as ex:
        raise GozHata(f"ana etiket okunamadı: {ex}") from ex
    if not {"sembol", "bas", "son", "sinif"} <= set(K.columns):
        raise GozHata(f"ana etiket sütunları eksik: {list(K.columns)}")
    K = K.copy(); K["bas"] = pd.to_datetime(K.bas); K["son"] = pd.to_datetime(K.son); K["sinif"] = K.sinif.astype(str).str.strip().str.upper()
    if not K.sinif.isin(["COL", "OLUMSUZ"]).all():
        raise GozHata(f"ana etikette bilinmeyen sınıf: {sorted(set(K.sinif) - {'COL', 'OLUMSUZ'})}")
    if (K.son < K.bas).any():
        raise GozHata("ana etikette son < bas")
    K["id"] = K.sembol + "_" + K.bas.dt.strftime("%Y%m%d"); K["kaynak"] = "kalibre_etiketler.csv"
    if K.id.duplicated().any():
        raise GozHata("ana etikette yinelenen (sembol, bas)")
    return K[["id", "sembol", "bas", "son", "sinif", "kaynak"]].reset_index(drop=True)


def goz_etiket_c(kutu: Optional[str] = None, obek: Optional[str] = None, ana: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, List[str]]:
    """C seti: etiket_2026-10-20 (DEGIL) + etiket_obek_ARZUM (OBEK / DEGIL); ana setle aynı hissede kesişen kutu çıkarılır. Döner (tablo, çıkarılan id'ler)."""
    kutu = kutu or GOZ_YOL["c_kutu"]; obek = obek or GOZ_YOL["c_obek"]; rows = []
    try:
        A = pd.read_csv(kutu); B = pd.read_csv(obek)
    except (OSError, ValueError) as ex:
        raise GozHata(f"C etiketi okunamadı: {ex}") from ex
    for _, r in A.iterrows():
        cm = str(r["cemal"]).strip().upper()
        if not cm.startswith("DEGIL"):
            raise GozHata(f"etiket_2026-10-20: beklenmeyen Cemal etiketi '{r['cemal']}' (no {r['no']})")
        rows.append({"id": f"C20_{int(r['no']):02d}_{r['sembol']}", "sembol": r["sembol"], "bas": pd.Timestamp(r["kutu_bas"]), "son": pd.Timestamp(r["kutu_son"]),
                     "sinif": "DEGIL", "kaynak": "goz_esle/etiket_2026-10-20.csv"})
    for i, r in B.iterrows():
        cm = str(r["cemal"]).strip().upper()
        s = "OBEK" if cm.startswith("OBEK") else ("DEGIL" if cm.startswith("DEGIL") else None)
        if s is None:
            raise GozHata(f"etiket_obek_ARZUM: beklenmeyen Cemal etiketi '{r['cemal']}'")
        rows.append({"id": f"COB_{i + 1}_{r['sembol']}", "sembol": r["sembol"], "bas": pd.Timestamp(r["obek_bas"]), "son": pd.Timestamp(r["obek_son"]),
                     "sinif": s, "kaynak": "goz_esle/etiket_obek_ARZUM.csv"})
    C = pd.DataFrame(rows)
    if (C.son < C.bas).any():
        raise GozHata("C etiketinde son < bas")
    ana = goz_etiket_ana() if ana is None else ana; cik = []
    for _, r in C.iterrows():
        a = ana[ana.sembol == r.sembol]
        if ((a.bas <= r.son) & (a.son >= r.bas)).any():
            cik.append(r.id)
    return C[~C.id.isin(cik)].reset_index(drop=True), cik


def goz_yasak(ana: pd.DataFrame, C: pd.DataFrame) -> Dict[str, List[Tuple[pd.Timestamp, pd.Timestamp]]]:
    """Rastgele pencerelerin kesişemeyeceği bütün Cemal etiket aralıkları (hisse -> [(bas, son)])."""
    Y: Dict[str, List[Tuple[pd.Timestamp, pd.Timestamp]]] = {}
    for T in (ana, C):
        for _, r in T.iterrows():
            Y.setdefault(r.sembol, []).append((pd.Timestamp(r.bas), pd.Timestamp(r.son)))
    return Y


# ---------------------------------------------------------------- 2) G5 VE PENCERE ÖLÇÜLERİ (yalnız geriye bakan değerler)
def goz_gunler(d: pd.DataFrame, bas: Any, son: Any) -> np.ndarray:
    """Serinin [bas, son] (dahil) aralığındaki işlem günü sıra numaraları."""
    ix = d.index
    return np.flatnonzero((ix >= pd.Timestamp(bas)) & (ix <= pd.Timestamp(son)))


def goz_g5(d: pd.DataFrame) -> Dict[str, np.ndarray]:
    """VDYT2 G5 günlük durumu (V2.v2_olculer, değiştirilmeden) + tanımlılık (ATRref ve iki bant referansı sonlu)."""
    Ol = V2.v2_olculer(d)
    g5 = np.asarray(Ol["durum"]["G5"], bool)
    tanimli = np.isfinite(Ol["atr_ref"]) & np.isfinite(Ol["b_kapanis_bant"]) & np.isfinite(Ol["b_govde_bant"])
    return {"g5": g5, "tanimli": np.asarray(tanimli, bool)}


def _goz_tr(d: pd.DataFrame) -> np.ndarray:
    h, l, c = (d[k].to_numpy(float) for k in ("h", "l", "c"))
    cp = np.r_[np.nan, c[:-1]]
    with np.errstate(invalid="ignore"):
        return np.nanmax(np.vstack([h - l, np.abs(h - cp), np.abs(l - cp)]), axis=0)


def goz_dip_savunma(low: np.ndarray, k: int = 3, ayrim: int = 5) -> Tuple[float, List[int]]:
    """En düşük k dip: Low'lar küçükten büyüğe taranır, seçilenlerin hepsinden >= ayrim bar uzak olan alınır. Döner (maks-min, seçilen sıralar)."""
    low = np.asarray(low, float); sec: List[int] = []
    for i in np.argsort(low, kind="stable"):
        if not np.isfinite(low[i]):
            continue
        if all(abs(int(i) - j) >= ayrim for j in sec):
            sec.append(int(i))
            if len(sec) == k:
                break
    if len(sec) < k:
        return float("nan"), sec
    v = low[sec]
    return float(v.max() - v.min()), sec


def goz_olculer(d: pd.DataFrame, b: int, e: int, E: Optional[Dict[str, Any]] = None, tr: Optional[np.ndarray] = None) -> Dict[str, float]:
    """Test B'nin 10 basit ölçüsü, pencere [b, e] (dahil). Her değer yalnız e ve öncesindeki barlardan; geçmiş yetmezse NaN."""
    E = E or GOZ_ESIK; B = E["B"]; nan = float("nan")
    if not (0 <= b <= e < len(d)):
        raise GozHata(f"pencere sınır dışı (b={b}, e={e}, n={len(d)})")
    o, h, l, c, v = (d[k].to_numpy(float) for k in ("o", "h", "l", "c", "v"))
    tr = _goz_tr(d) if tr is None else tr
    sl = slice(b, e + 1); rng = h[sl] - l[sl]
    a0 = max(0, b - int(B["atr_n"])); trw = tr[a0:b]; trw = trw[np.isfinite(trw)]
    atr = float(trw.mean()) if len(trw) >= int(B["atr_min"]) and trw.mean() > 0 else nan
    with np.errstate(invalid="ignore", divide="ignore"):
        out: Dict[str, float] = {}
        out["aralik_kapanis"] = float(np.nanmedian(rng / c[sl]))
        out["aralik_atr"] = float(np.nanmedian(rng) / atr) if np.isfinite(atr) else nan
        mc = float(np.nanmedian(c[sl]))
        out["kapanis_bant"] = float((np.nanmax(c[sl]) - np.nanmin(c[sl])) / mc) if mc > 0 else nan
        out["govde_atr"] = float(np.nanmedian(np.abs(c[sl] - o[sl])) / atr) if np.isfinite(atr) else nan
        out["uzunluk"] = float(e - b + 1)
        d0 = max(0, b - int(B["dusus_n"])); cw = c[d0:b]
        out["dusus120"] = float(c[b - 1] / np.nanmax(cw) - 1.0) if (b - d0) >= int(B["dusus_min"]) and np.nanmax(cw) > 0 else nan
        h0 = max(0, b - int(B["hacim_n"])); vw = v[h0:b]; vw = vw[np.isfinite(vw)]
        vm = float(np.median(vw)) if len(vw) >= int(B["hacim_min"]) else nan
        out["hacim_oran"] = float(np.nanmedian(v[sl]) / vm) if np.isfinite(vm) and vm > 0 else nan
        n_s = int(B["sma"])
        if b - n_s + 1 >= 0:
            s_b = float(np.mean(c[b - n_s + 1: b + 1])); s_e = float(np.mean(c[e - n_s + 1: e + 1]))
            out["sma50_egim"] = float(100.0 * np.log(s_e / s_b) / max(e - b, 1)) if s_b > 0 and s_e > 0 else nan
        else:
            out["sma50_egim"] = nan
        ds, _ = goz_dip_savunma(l[sl], int(B["dip"]["k"]), int(B["dip"]["ayrim"]))
        out["dip_savunma"] = float(ds / atr) if np.isfinite(ds) and np.isfinite(atr) else nan
        k0 = max(0, e - int(B["konum_n"]) + 1)
        if e - k0 + 1 >= int(B["konum_min"]):
            lo, hi = float(np.nanmin(l[k0: e + 1])), float(np.nanmax(h[k0: e + 1]))
            out["konum250"] = float((mc - lo) / (hi - lo)) if hi > lo else nan
        else:
            out["konum250"] = nan
    return {k: (v_ if np.isfinite(v_) else nan) for k, v_ in out.items()}


def goz_rastgele(d: pd.DataFrame, uzun: int, yasak: List[Tuple[pd.Timestamp, pd.Timestamp]], tohum: Any,
                 E: Optional[Dict[str, Any]] = None) -> Tuple[List[Tuple[int, int]], int]:
    """Aynı hisseden `uzun` işlem günlük, hiçbir yasak aralıkla kesişmeyen rastgele pencereler. Döner ([(b, e)], uygun başlangıç sayısı)."""
    E = E or GOZ_ESIK; R = E["A"]["rastgele"]; n = len(d); ix = d.index
    if uzun < 1 or n < uzun:
        return [], 0
    bas = np.arange(0, n - uzun + 1)
    ok = (bas >= int(R["ilk_bar"])) & (ix[bas] >= pd.Timestamp(R["bas_tarih"]))
    tb = ix[bas].to_numpy(); te = ix[bas + uzun - 1].to_numpy()
    for (yb, ye) in yasak:
        ok &= ~((tb <= np.datetime64(pd.Timestamp(ye))) & (te >= np.datetime64(pd.Timestamp(yb))))
    uy = bas[ok]
    if not len(uy):
        return [], 0
    rng = np.random.default_rng(int(hashlib.sha256(str(tohum).encode("utf-8")).hexdigest()[:8], 16))
    sec = np.sort(rng.choice(uy, size=min(int(R["n"]), len(uy)), replace=False))
    return [(int(s), int(s) + uzun - 1) for s in sec], int(len(uy))


# ---------------------------------------------------------------- 3) İSTATİSTİK
def goz_auc(pos: np.ndarray, neg: np.ndarray) -> float:
    """P(pos > neg) + 0,5 P(eşit) (Mann-Whitney, sıra ortalamasıyla); NaN dışarıda; boş -> NaN."""
    p = np.asarray(pos, float); q = np.asarray(neg, float); p = p[np.isfinite(p)]; q = q[np.isfinite(q)]
    if not len(p) or not len(q):
        return float("nan")
    r = pd.Series(np.r_[p, q]).rank(method="average").to_numpy()
    return float((r[: len(p)].sum() - len(p) * (len(p) + 1) / 2.0) / (len(p) * len(q)))


def goz_yon(auc: float) -> int:
    return 1 if (not np.isfinite(auc)) or auc >= 0.5 else -1


def goz_loso_auc(R: pd.DataFrame, olcu: str) -> Dict[str, Any]:
    """COL vs RASTGELE LOSO AUC: yön kalan hisselerden, dışarıdaki hissenin satırları yön x değer; havuzlu AUC."""
    X = R[R.grup.isin(["COL", "RASTGELE"]) & np.isfinite(R[olcu].astype(float))]
    puan_p: List[float] = []; puan_n: List[float] = []; yonler: Dict[str, int] = {}
    for s in sorted(X[X.grup == "COL"].sembol.unique()):
        tr_ = X[X.sembol != s]; te = X[X.sembol == s]
        y = goz_yon(goz_auc(tr_[tr_.grup == "COL"][olcu].to_numpy(float), tr_[tr_.grup == "RASTGELE"][olcu].to_numpy(float)))
        yonler[s] = y
        puan_p += list(y * te[te.grup == "COL"][olcu].to_numpy(float)); puan_n += list(y * te[te.grup == "RASTGELE"][olcu].to_numpy(float))
    return {"auc": goz_auc(np.array(puan_p), np.array(puan_n)), "n_col": len(puan_p), "n_rastgele": len(puan_n),
            "yon_degisti": int(len(set(yonler.values())) > 1)}


def goz_esik(x_col: np.ndarray, yon: int, E: Optional[Dict[str, Any]] = None) -> float:
    E = E or GOZ_ESIK; p20, p80 = E["B"]["kural"]["yuzdelik"]; x = np.asarray(x_col, float); x = x[np.isfinite(x)]
    if not len(x):
        return float("nan")
    return float(np.percentile(x, p20 if yon > 0 else p80))


def goz_gecer(x: np.ndarray, yon: int, esik: float) -> np.ndarray:
    x = np.asarray(x, float)
    with np.errstate(invalid="ignore"):
        return np.where(np.isfinite(x), (x >= esik) if yon > 0 else (x <= esik), False)


def goz_kural_uygula(T: pd.DataFrame, kural: List[Dict[str, Any]]) -> np.ndarray:
    ok = np.ones(len(T), bool)
    for k in kural:
        ok &= goz_gecer(T[k["olcu"]].to_numpy(float), int(k["yon"]), float(k["esik"]))
    return ok


def goz_kural_kur(R: pd.DataFrame, olculer: List[str], E: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Eğitim satırlarından (COL + RASTGELE) yön ve eşik: yön = COL vs RASTGELE AUC; eşik = COL %20 / %80 yüzdeliği."""
    out = []
    for m in olculer:
        col = R[R.grup == "COL"][m].to_numpy(float); ra = R[R.grup == "RASTGELE"][m].to_numpy(float)
        y = goz_yon(goz_auc(col, ra)); out.append({"olcu": m, "yon": y, "esik": goz_esik(col, y, E)})
    return out


def goz_kural_loso(R: pd.DataFrame, olculer: List[str], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """LOSO: her COL hissesi dışarıda; kural kalanlardan; dışarıdaki COL / RASTGELE geçme oranı havuzlu. J = yakalama - yanlış alarm."""
    X = R[R.grup.isin(["COL", "RASTGELE"])]; gp = gn = np_ = nn = 0
    for s in sorted(X[X.grup == "COL"].sembol.unique()):
        k = goz_kural_kur(X[X.sembol != s], olculer, E); te = X[X.sembol == s]
        g = goz_kural_uygula(te, k); isc = (te.grup == "COL").to_numpy()
        gp += int(g[isc].sum()); np_ += int(isc.sum()); gn += int(g[~isc].sum()); nn += int((~isc).sum())
    yak = gp / np_ if np_ else float("nan"); ya = gn / nn if nn else float("nan")
    return {"olculer": olculer, "yakalama_col": yak, "gecme_rastgele": ya, "J": yak - ya, "n_col": np_, "n_rastgele": nn}


def goz_bootstrap_A(R: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, List[float]]:
    """Hisse kümeli bootstrap: hisseler tekrarlı çekilir; her grup oranı çekilen hisselerin satırlarından. Döner %2,5 / %97,5 aralıkları."""
    E = E or GOZ_ESIK; Bs = E["A"]["bootstrap"]; X = R[R.grup.isin(["COL", "OLUMSUZ", "RASTGELE"])]
    hs = sorted(X.sembol.unique()); rng = np.random.default_rng(int(Bs["tohum"]))
    grp = {g: {s: X[(X.sembol == s) & (X.grup == g)].yakaladi.to_numpy(float) for s in hs} for g in ("COL", "OLUMSUZ", "RASTGELE")}
    S: Dict[str, List[float]] = {"COL": [], "OLUMSUZ": [], "RASTGELE": [], "fark_col_rastgele": [], "kat_col_rastgele": [], "fark_col_olumsuz": []}
    for _ in range(int(Bs["B"])):
        ck = rng.choice(len(hs), size=len(hs), replace=True); oran = {}
        for g in grp:
            v = np.concatenate([grp[g][hs[i]] for i in ck]) if len(ck) else np.array([])
            oran[g] = float(v.mean()) if len(v) else float("nan")
        for g in grp:
            S[g].append(oran[g])
        S["fark_col_rastgele"].append(oran["COL"] - oran["RASTGELE"])
        S["kat_col_rastgele"].append(oran["COL"] / oran["RASTGELE"] if oran["RASTGELE"] and np.isfinite(oran["RASTGELE"]) else float("nan"))
        S["fark_col_olumsuz"].append(oran["COL"] - oran["OLUMSUZ"])
    lo, hi = Bs["guven"]
    return {k: [float(np.nanpercentile(v, lo)), float(np.nanpercentile(v, hi))] if np.isfinite(v).any() else [None, None]
            for k, v in ((k, np.array(v, float)) for k, v in S.items())}


def goz_karar_A(yc: float, yr: float, yo: float, E: Optional[Dict[str, Any]] = None) -> str:
    E = E or GOZ_ESIK; K = E["A"]["karar"]
    if yc >= K["uyuyor"]["col_min"] and yc >= K["uyuyor"]["rastgele_kat"] * yr and yc > yo:
        return "G5 GÖZE UYUYOR"
    if yc >= K["zayif"]["col_min"] and yc > K["zayif"]["rastgele_kat"] * yr:
        return "ZAYIF"
    return "UYMUYOR"


# ---------------------------------------------------------------- 4) TABLO KURULUMU
def goz_satir(grup: str, rid: str, sembol: str, d: pd.DataFrame, b: int, e: int, G: Dict[str, np.ndarray], tr: np.ndarray, E: Dict[str, Any],
              ana_id: Optional[str] = None) -> Dict[str, Any]:
    g = G["g5"][b: e + 1]; t = G["tanimli"][b: e + 1]
    r = {"grup": grup, "id": rid, "ana_id": ana_id, "sembol": sembol, "bas_i": int(b), "son_i": int(e), "bas": str(d.index[b].date()),
         "son": str(d.index[e].date()), "n_gun": int(e - b + 1), "g5_gun": int(g.sum()), "g5_pay": float(g.mean()),
         "tanimli_pay": float(t.mean()), "yakaladi": int(g.mean() >= float(E["A"]["yakalama_pay"])), "bir_gun": int(g.sum() >= int(E["A"]["bilgi_en_az_gun"]))}
    r.update(goz_olculer(d, b, e, E, tr))
    return r


def goz_hazirla(S_test: Dict[str, pd.DataFrame], S_canli: Optional[Dict[str, pd.DataFrame]] = None, E: Optional[Dict[str, Any]] = None,
                ana: Optional[pd.DataFrame] = None, C: Optional[pd.DataFrame] = None, c_cik: Optional[List[str]] = None) -> Dict[str, Any]:
    """Bütün satırlar: COL / OLUMSUZ (test serisi), RASTGELE (her COL'a n), C_DEGIL / C_OBEK (canlı seri). Döner {'R': DataFrame, 'kapsam': {...}}."""
    E = E or GOZ_ESIK
    ana = goz_etiket_ana() if ana is None else ana
    if C is None:
        C, c_cik = goz_etiket_c(ana=ana)
    c_cik = c_cik or []
    yasak = goz_yasak(ana, C); rows: List[Dict[str, Any]] = []; kap: Dict[str, Any] = {"veri_disi": [], "kirpilan": [], "rastgele_eksik": [], "c_cikarilan": c_cik}
    cache: Dict[Tuple[str, str], Tuple[pd.DataFrame, Dict[str, np.ndarray], np.ndarray]] = {}

    def seri(s: str, tur: str) -> Optional[Tuple[pd.DataFrame, Dict[str, np.ndarray], np.ndarray]]:
        if (s, tur) not in cache:
            SS = S_test if tur == "test" else (S_canli if S_canli is not None else S_test)
            if s not in SS or not len(SS[s]):
                return None
            d = SS[s]; cache[(s, tur)] = (d, goz_g5(d), _goz_tr(d))
        return cache[(s, tur)]

    for _, r in ana.iterrows():
        x = seri(r.sembol, "test")
        if x is None:
            kap["veri_disi"].append({"id": r.id, "neden": "hisse veride yok"}); continue
        d, G, tr = x; gi = goz_gunler(d, r.bas, r.son)
        if not len(gi):
            kap["veri_disi"].append({"id": r.id, "neden": "aralıkta işlem günü yok (veri / kesik dışı)"}); continue
        if pd.Timestamp(r.son) > d.index[-1] or pd.Timestamp(r.bas) < d.index[0]:
            kap["kirpilan"].append({"id": r.id, "gun": int(len(gi)), "seri_son": str(d.index[-1].date())})
        b, e = int(gi[0]), int(gi[-1])
        rows.append(goz_satir(r.sinif, r.id, r.sembol, d, b, e, G, tr, E))
        if r.sinif == "COL":
            pen, uy = goz_rastgele(d, e - b + 1, yasak.get(r.sembol, []), f"{E['A']['rastgele']['tohum']}|{r.sembol}|{r.bas.date()}", E)
            if len(pen) < int(E["A"]["rastgele"]["n"]):
                kap["rastgele_eksik"].append({"id": r.id, "pencere": len(pen), "uygun": uy})
            for j, (pb, pe) in enumerate(pen):
                rows.append(goz_satir("RASTGELE", f"{r.id}_R{j + 1:02d}", r.sembol, d, pb, pe, G, tr, E, ana_id=r.id))
    for _, r in C.iterrows():
        x = seri(r.sembol, "canli")
        if x is None:
            kap["veri_disi"].append({"id": r.id, "neden": "hisse (canlı) veride yok"}); continue
        d, G, tr = x; gi = goz_gunler(d, r.bas, r.son)
        if not len(gi):
            kap["veri_disi"].append({"id": r.id, "neden": "aralıkta işlem günü yok"}); continue
        if pd.Timestamp(r.son) > d.index[-1]:
            kap["kirpilan"].append({"id": r.id, "gun": int(len(gi)), "seri_son": str(d.index[-1].date())})
        rows.append(goz_satir("C_" + r.sinif, r.id, r.sembol, d, int(gi[0]), int(gi[-1]), G, tr, E))
    R = pd.DataFrame(rows)
    kap["sayim"] = {g: int((R.grup == g).sum()) for g in ("COL", "OLUMSUZ", "RASTGELE", "C_DEGIL", "C_OBEK")} if len(R) else {}
    return {"R": R, "kapsam": kap}


# ---------------------------------------------------------------- 5) TESTLER
def goz_test_A(R: pd.DataFrame, E: Optional[Dict[str, Any]] = None, bootstrap: bool = True) -> Dict[str, Any]:
    E = E or GOZ_ESIK; out: Dict[str, Any] = {}
    for g in ("COL", "OLUMSUZ", "RASTGELE", "C_DEGIL", "C_OBEK"):
        X = R[R.grup == g]
        out[g] = {"n": int(len(X)), "hisse": int(X.sembol.nunique()), "yakalama": float(X.yakaladi.mean()) if len(X) else None,
                  "yakalayan": int(X.yakaladi.sum()), "en_az_bir_gun": float(X.bir_gun.mean()) if len(X) else None,
                  "g5_pay_ort": float(X.g5_pay.mean()) if len(X) else None, "g5_pay_medyan": float(X.g5_pay.median()) if len(X) else None,
                  "tanimsiz_bolge": int((X.tanimli_pay < 0.5).sum())}
        Xt = X[X.tanimli_pay >= 0.5]
        out[g]["tanimli_yakalama"] = float(Xt.yakaladi.mean()) if len(Xt) else None
        out[g]["tanimli_n"] = int(len(Xt))
    yc, yr, yo = (out[g]["yakalama"] for g in ("COL", "RASTGELE", "OLUMSUZ"))
    out["karar"] = goz_karar_A(yc, yr, yo if yo is not None else 0.0, E)
    out["kat_col_rastgele"] = (yc / yr) if yr else None
    bc, br, bo = (out[g]["en_az_bir_gun"] for g in ("COL", "RASTGELE", "OLUMSUZ"))
    out["bilgi_en_az_bir_gun_karar"] = goz_karar_A(bc, br, bo if bo is not None else 0.0, E)
    if bootstrap:
        out["bootstrap"] = goz_bootstrap_A(R, E)
    return out


def goz_test_B(R: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or GOZ_ESIK; B = E["B"]; tab = []
    for m in B["olculer"]:
        col = R[R.grup == "COL"][m].to_numpy(float); ra = R[R.grup == "RASTGELE"][m].to_numpy(float); ol = R[R.grup == "OLUMSUZ"][m].to_numpy(float)
        a_r = goz_auc(col, ra); y = goz_yon(a_r); a_o = goz_auc(y * col, y * ol); L = goz_loso_auc(R, m)
        tab.append({"olcu": m, "auc_col_rastgele_ham": a_r, "yon": y, "auc_col_rastgele_yonlu": goz_auc(y * col, y * ra), "loso_auc": L["auc"],
                    "loso_yon_degisti": L["yon_degisti"], "auc_col_olumsuz_yonlu": a_o,
                    "medyan_col": float(np.nanmedian(col)) if np.isfinite(col).any() else None,
                    "medyan_rastgele": float(np.nanmedian(ra)) if np.isfinite(ra).any() else None,
                    "medyan_olumsuz": float(np.nanmedian(ol)) if np.isfinite(ol).any() else None,
                    "n_col": int(np.isfinite(col).sum()), "n_rastgele": int(np.isfinite(ra).sum()), "n_olumsuz": int(np.isfinite(ol).sum()),
                    "aday": bool(np.isfinite(L["auc"]) and L["auc"] >= B["aday"]["loso_rastgele_min"] and np.isfinite(a_o) and a_o >= B["aday"]["olumsuz_min"])})
    aday = [t["olcu"] for t in tab if t["aday"]]; out: Dict[str, Any] = {"tablo": tab, "aday": aday, "kural": None, "kural_denenen": []}
    if aday:
        den = []
        for a in aday:
            den.append(goz_kural_loso(R, [a], E))
            for m in B["olculer"]:
                if m != a and not any(set(x["olculer"]) == {a, m} for x in den):
                    den.append(goz_kural_loso(R, [a, m], E))
        tek = max((x for x in den if len(x["olculer"]) == 1), key=lambda x: x["J"])
        cift = [x for x in den if len(x["olculer"]) == 2]
        en_cift = max(cift, key=lambda x: x["J"]) if cift else None
        sec = en_cift if (en_cift is not None and en_cift["J"] >= tek["J"] + 0.05) else tek
        tam = goz_kural_kur(R[R.grup.isin(["COL", "RASTGELE"])], sec["olculer"], E)
        ol = R[R.grup == "OLUMSUZ"]
        out.update({"kural_denenen": den, "kural": {"loso": sec, "tam_kural": tam,
                                                    "gecme_olumsuz": float(goz_kural_uygula(ol, tam).mean()) if len(ol) else None}})
    return out


def goz_test_C(R: pd.DataFrame, TB: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or GOZ_ESIK; Kc = E["C"]["karar"]; D = R[R.grup == "C_DEGIL"]; O = R[R.grup == "C_OBEK"]
    out: Dict[str, Any] = {"n_degil": int(len(D)), "n_obek": int(len(O))}
    if not TB.get("kural"):
        out["karar"] = "C YAPILMADI (B'de aday yok)"; return out
    k = TB["kural"]["tam_kural"]; gd = goz_kural_uygula(D, k); go = goz_kural_uygula(O, k)
    pd_ = float(gd.mean()) if len(D) else float("nan"); yak = float(TB["kural"]["loso"]["yakalama_col"])
    out.update({"gecme_degil": pd_, "gecme_obek": float(go.mean()) if len(O) else None, "loso_yakalama_col": yak,
                "karar": "C TUTTU" if (np.isfinite(pd_) and pd_ <= Kc["degil_max"] and pd_ <= yak - Kc["fark_min"]) else "C TUTMADI"})
    return out


# ---------------------------------------------------------------- 6) ÖN KAYIT VE KAPI
def goz_veri_sha() -> Dict[str, Any]:
    y = V1.VDYT_YOL["v_bist"]
    return {"v_bist": y, "sha256": goz_sha_dosya(y) if os.path.exists(y) else None}


def goz_etiket_sha() -> Dict[str, str]:
    return {os.path.relpath(GOZ_YOL[k], KOK_GOZ): goz_sha_dosya(GOZ_YOL[k]) for k in ("ana", "c_kutu", "c_obek")}


def goz_onkayit_metin(zaman: str, sayim: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or GOZ_ESIK; es = json.dumps(_goz_kayit(E), ensure_ascii=False, indent=1, sort_keys=True)
    et = "\n".join(f"- {k}: `{v}`" for k, v in goz_etiket_sha().items()); vs = goz_veri_sha()
    return f"""# GOZ_G5 ÖN KAYIT — G5 x Cemal'in mevcut göz etiketleri ({GOZ_ETIKET})

Yazıldı: {zaman}. Ölçümden ÖNCE yazıldı; G5 hiçbir etiket bölgesinde hesaplanmadı. Eşikler aşağıdaki sözlükte, sonuca göre değişmez.

ESIK_SHA256: {goz_esik_sha(E)}
KOD_SHA256: {goz_kod_sha()}
VDYT2_KOD_SHA256: {V2.v2_kod_sha()}
VDYT_KOD_SHA256: {V2.v2_v1_kod_sha()}
VERI: {vs['v_bist']} sha256 {vs['sha256']}

## Soru
Kör testte Cemal G5 grafiklerinde hiçbir belirti görmedi (Ç166). Burada yeni işaret istenmeden G5, Cemal'in daha önce elle verdiği çöl etiketlerine karşı
sınanır: (A) G5 Cemal'in çöllerinin içinde rastgele pencerelerden daha sık mı yanıyor; (B) gözün gördüğünü hangi basit ölçü yakalıyor; (C) bulunan ölçü
ikinci bir Cemal etiket setinde tutuyor mu.

## Etiketler (yalnız Cemal'in gözle verdikleri)
{et}

Sayım (etiket dosyaları ve veri kapsamı; G5 / ölçü yok): {json.dumps(_goz_kayit(sayim), ensure_ascii=False)}

- ANA: kalibre_etiketler.csv — Cemal 18 Eylül 2026 (COL_OZET §7 'Cemal'in gözle işaretlediği 29 çöl + 8 olumsuz'; dosyada PEKER ile 30 COL, PEKER veride yok).
- C: goz_esle/etiket_2026-10-20.csv (21 kutu, 'cemal' sütunu: hepsi DEĞİL; COL_OZET §9.8 '21 kutunun HİÇBİRİ çöl değil') ve
  goz_esle/etiket_obek_ARZUM.csv (Cemal'in ARZUM öbek etiketleri: 3 OBEK, 1 DEĞİL 'düşen bıçak'). Öbek küçük ölçekli desendir (çöl değil): OBEK yakalaması
  yalnız BİLGİ. C kutularının çoğu 31.08.2026 sonrası (fon krizi dönemi): yalnız şekil ölçülür, getiri ölçülmez.
- DIŞARIDA: COL_GOZ (arastirma_cikti/col_goz/, 746 kutu, 45 ÇÖL / 105 SINIR): bu sınıflar Claude'un gözüdür ('benim'). Cemal'in 22 Ekim EVET / HAYIR kararları
  (col_goz_cemal_2024_26.csv, 150 kutu) repoda yok; ayrıca o kararlar sinyal sonrası atılıma göre verilmişti (COL_OZET §9.8). Kullanılmaz.

## Test A — G5 göze uyuyor mu
Bölge = serinin [bas, son] işlem günleri (test serisi, kesik 31.08.2026; kesikten taşan bölge kırpılır ve sayılır). G5 = VDYT2.py'deki hali (V2.v2_olculer
'durum'['G5']), değiştirilmeden; her gün yalnız o gün ve öncesine bakar. Yakaladı = bölge içi G5 gün oranı >= 0,50 (ANA); en az 1 gün (BİLGİ).
Gruplar: COL, OLUMSUZ, RASTGELE (her COL bölgesine aynı hisseden aynı uzunlukta 20 pencere; 2022-01-01 sonrası, seri başından >= 260 bar, hiçbir Cemal
etiketiyle kesişmez; tohum 20261113). Karar (nokta tahmini): G5 GÖZE UYUYOR <=> yak(COL) >= 0,70 VE >= 2 x yak(RASTGELE) VE > yak(OLUMSUZ); ZAYIF <=>
yak(COL) >= 0,50 VE > 1,5 x yak(RASTGELE); değilse UYMUYOR. Hisse kümeli bootstrap (2000, tohum 20261114) %95 aralık. G5'in geçmişi yetmeyen günleri
dedektörün kendi davranışıyla YANLIŞ (ANA); tanımlı gün oranı >= 0,50 bölgelerle yeniden hesap BİLGİ.

## Test B — basit ölçüler
10 ölçü (tanımlar sözlükte): aralik_kapanis, aralik_atr, kapanis_bant, govde_atr, uzunluk (RASTGELE ile tanım gereği eşit), dusus120, hacim_oran,
sma50_egim, dip_savunma, konum250. AUC (COL vs RASTGELE; yön tam örneklemden), hisse dışarıda bırakmalı (LOSO) AUC (yön eğitimden), COL vs OLUMSUZ
yönlü AUC. GÖZ ÖLÇÜSÜ ADAYI <=> LOSO AUC >= 0,80 VE AUC(COL vs OLUMSUZ) >= 0,70. Kural (yalnız aday varsa): aday tek başına ve aday + öteki bir ölçü (VE);
eşik COL'un %20 / %80 yüzdeliği (yöne göre); LOSO J = yakalama - yanlış alarm; iki ölçülü kural ancak J'si tekini >= 0,05 geçerse. Karmaşık model yok.

## Test C — bağımsız sağlama
B'nin seçilen kuralı tam ana setten eşikle C setine aynen uygulanır (canlı seri). C TUTTU <=> geçme(DEĞİL) <= 0,30 VE <= LOSO yakalama(COL) - 0,30;
OBEK yakalaması BİLGİ. B'de aday yoksa 'C YAPILMADI (B'de aday yok)'; G5'in C setindeki yakalaması her durumda BİLGİ.

## Grafik (gösterim, karar dışı)
3 COL bölgesi + 3 RASTGELE pencere (tohum 20261115), bölge sonundan 20 bar sonrasına kadar 250 bar, KOR_TEST v1.1 kor_ciz_fig11 (ortak log ölçek), bölge
gölgeli, G5 günleri altta; hisse adı yok; /tmp/goz_g5/grafik (repoya girmez).

## Kapı
`python GOZ_G5.py kos` ancak bu dosya git'e işlenmiş ve değişmemişse, ESIK_SHA256 ve KOD_SHA256 tutuyorsa, VDYT2.py / VDYT.py sha256'ları yukarıdakiyle
aynıysa çalışır (kod değişirse yalnız `--sapma` gerekçesiyle; gerekçe sonuca yazılır).

## Eşik sözlüğü (GOZ_ESIK)
```json
{es}
```
"""


def goz_sayim(S_test: Dict[str, pd.DataFrame], S_canli: Optional[Dict[str, pd.DataFrame]] = None) -> Dict[str, Any]:
    """Ön kayıt için etiket sayımı ve veri kapsamı (G5 / ölçü hesaplanmaz)."""
    ana = goz_etiket_ana(); C, cik = goz_etiket_c(ana=ana); out: Dict[str, Any] = {"ana": ana.sinif.value_counts().to_dict(), "c": C.sinif.value_counts().to_dict(),
                                                                                    "c_cikarilan_ortusme": cik, "veri_disi": [], "kesikten_tasan": []}
    for _, r in ana.iterrows():
        d = S_test.get(r.sembol)
        if d is None or not len(goz_gunler(d, r.bas, r.son)):
            out["veri_disi"].append(r.id)
        elif r.son > d.index[-1]:
            out["kesikten_tasan"].append(r.id)
    Sc = S_canli if S_canli is not None else S_test
    out["c_veri_disi"] = [r.id for _, r in C.iterrows() if Sc.get(r.sembol) is None or not len(goz_gunler(Sc[r.sembol], r.bas, r.son))]
    out["ana_hisse"] = int(ana.sembol.nunique()); out["c_hisse"] = int(C.sembol.nunique())
    return out


def goz_onkayit(kl: Optional[str] = None, S_test: Optional[Dict[str, pd.DataFrame]] = None, S_canli: Optional[Dict[str, pd.DataFrame]] = None) -> str:
    y = _goz_yol("onkayit", kl)
    if os.path.exists(y):
        raise GozHata(f"ön kayıt zaten var, üzerine yazılmaz: {y}")
    goz_vdyt2_denetim()
    if S_test is None:
        S_test = V2.v2_fiyat("BIST")["S"]
    if S_canli is None:
        S_canli = V2.v2_fiyat("BIST", canli=True)["S"]
    return _goz_yaz(y, goz_onkayit_metin(_goz_simdi(), goz_sayim(S_test, S_canli)))


def goz_onkayit_oku(yol: str) -> Dict[str, str]:
    try:
        with open(yol, encoding="utf-8") as f:
            t = f.read()
    except OSError as ex:
        raise GozHata(f"ön kayıt okunamadı: {ex}") from ex
    out = {}
    for k in ("ESIK_SHA256", "KOD_SHA256", "VDYT2_KOD_SHA256", "VDYT_KOD_SHA256"):
        m = re.search(rf"^{k}: ([0-9a-f]{{64}})$", t, re.M)
        if not m:
            raise GozHata(f"ön kayıtta {k} yok")
        out[k] = m.group(1)
    return out


def goz_kapi(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ön kayıt mühür kapısı: ön kayıt var + git'e işlenmiş ve değişmemiş + ESIK sha tutar + VDYT2 / VDYT sha tutar + KOD sha tutar (ya da sapma gerekçesi)."""
    E = E or GOZ_ESIK; y = _goz_yol("onkayit", kl)
    if not os.path.exists(y):
        raise GozHata("ön kayıt yok: önce `python GOZ_G5.py onkayit` ve commit")
    O = goz_onkayit_oku(y); out: Dict[str, Any] = {"onkayit": y}
    if git:
        out["onkayit_git"] = goz_git_durum(y)
    if O["ESIK_SHA256"] != goz_esik_sha(E):
        raise GozHata("eşik mührü tutmuyor (GOZ_ESIK ön kayıttan sonra değişmiş)")
    v = goz_vdyt2_denetim(E)
    if O["VDYT2_KOD_SHA256"] != v["vdyt2"] or O["VDYT_KOD_SHA256"] != v["vdyt"]:
        raise GozHata("VDYT2 / VDYT kod sha256 ön kayıttakiyle aynı değil")
    ks = goz_kod_sha(); out["kod_sha256"] = ks; out["kod_ayni"] = ks == O["KOD_SHA256"]
    if not out["kod_ayni"]:
        if not sapma:
            raise GozHata("GOZ_G5.py ön kayıttan sonra değişmiş: yalnız `--sapma GEREKCE` ile koşar (gerekçe sonuca yazılır)")
        out["sapma"] = sapma
    out["esik_sha256"] = O["ESIK_SHA256"]
    return out


# ---------------------------------------------------------------- 7) KOŞU, RAPOR, GRAFİK
def goz_kos(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, S_test: Optional[Dict[str, pd.DataFrame]] = None,
            S_canli: Optional[Dict[str, pd.DataFrame]] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or GOZ_ESIK; K = goz_kapi(kl, git, sapma, E); t0 = _goz_simdi()
    gozlog.info("kapı geçti (mühür %s); fiyatlar yükleniyor (ağ yok)", K["esik_sha256"][:12])
    if S_test is None:
        S_test = V2.v2_fiyat("BIST")["S"]
    if S_canli is None:
        S_canli = V2.v2_fiyat("BIST", canli=True)["S"]
    H = goz_hazirla(S_test, S_canli, E); R = H["R"]
    if not len(R) or not (R.grup == "COL").any():
        raise GozHata("ölçülecek COL bölgesi yok")
    gozlog.info("satırlar: %s", H["kapsam"]["sayim"])
    A = goz_test_A(R, E); B = goz_test_B(R, E); Cc = goz_test_C(R, B, E)
    S = {"surum": GOZ_SURUM, "baslangic": t0, "bitis": _goz_simdi(), "kapi": K, "kapsam": H["kapsam"], "A": A, "B": B, "C": Cc,
         "satirlar": R.drop(columns=["bas_i", "son_i"]).to_dict(orient="records")}
    _goz_json(_goz_yol("sonuc", kl), S); _goz_yaz(_goz_yol("rapor", kl), goz_rapor_md(S, E))
    gozlog.info("A: %s | B aday: %s | C: %s", A["karar"], B["aday"] or "yok", Cc["karar"])
    return S


def _f(x: Any, n: int = 2) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:.{n}f}".replace(".", ",") if isinstance(x, (float, np.floating)) else str(x)


def _ar(a: Any) -> str:
    return f"[{_f(a[0])}; {_f(a[1])}]" if a and a[0] is not None else "—"


_GOZ_AD = {"aralik_kapanis": "mum boyu / fiyat (medyan H-L / C)", "aralik_atr": "mum boyu / önceki ATR250", "kapanis_bant": "kapanış bandı (maks-min)/medyan",
           "govde_atr": "gövde / önceki ATR250", "uzunluk": "bölge uzunluğu (gün)", "dusus120": "önceki 120 günde tepeden düşüş",
           "hacim_oran": "hacim / önceki 250 gün", "sma50_egim": "SMA50 eğimi (%/gün)", "dip_savunma": "3 dip yakınlığı / ATR250",
           "konum250": "250 günlük aralıkta konum"}


def goz_rapor_md(S: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or GOZ_ESIK; A = S["A"]; B = S["B"]; C = S["C"]; bs = A.get("bootstrap", {}); kp = S["kapsam"]
    L = [f"# GOZ_G5 — G5 dedektörü Cemal'in gözle işaretlediği çöllere uyuyor mu? ({GOZ_ETIKET})", "",
         f"Koşu {S['baslangic']} → {S['bitis']}; ön kayıt commit {S['kapi'].get('onkayit_git', {}).get('commit', '—')[:12]} "
         f"({S['kapi'].get('onkayit_git', {}).get('commit_zamani', '—')}), mühür {S['kapi']['esik_sha256'][:12]}"
         + (f"; SAPMA: {S['kapi']['sapma']}" if S["kapi"].get("sapma") else "") + ".", "",
         "## Sonuç", "",
         f"- **Test A: {A['karar']}.** G5, Cemal'in {A['COL']['n']} çöl bölgesinin {A['COL']['yakalayan']}'ini yakalıyor "
         f"(%{_f(100 * A['COL']['yakalama'], 0)}); aynı hisselerin rastgele pencerelerinde %{_f(100 * A['RASTGELE']['yakalama'], 0)}, "
         f"Cemal'in 'olumsuz' bölgelerinde %{_f(100 * A['OLUMSUZ']['yakalama'], 0)}.",
         f"- **Test B:** " + (f"göz ölçüsü adayı: {', '.join(B['aday'])}." if B["aday"] else "hiçbir basit ölçü aday eşiğini (LOSO AUC >= 0,80 ve olumsuza karşı >= 0,70) geçmedi."),
         f"- **Test C:** {C['karar']}.", "",
         "## Test A — G5 bölgenin en az yarısında yanıyor mu", "",
         "| grup | bölge | hisse | yakalama (>= %50 gün) | %95 aralık (hisse kümeli) | en az 1 gün | G5 gün payı ort. | tanımsız bölge |", "|---|---|---|---|---|---|---|---|"]
    for g, ad in (("COL", "Cemal ÇÖL"), ("OLUMSUZ", "Cemal OLUMSUZ"), ("RASTGELE", "RASTGELE (aynı hisse, aynı uzunluk)"),
                  ("C_DEGIL", "C seti DEĞİL (bilgi)"), ("C_OBEK", "C seti ÖBEK (bilgi)")):
        a = A[g]
        L.append(f"| {ad} | {a['n']} | {a['hisse']} | {_f(a['yakalama'])} | {_ar(bs.get(g)) if g in bs else '—'} | {_f(a['en_az_bir_gun'])} | "
                 f"{_f(a['g5_pay_ort'])} | {a['tanimsiz_bolge']} |")
    L += ["", f"COL − RASTGELE farkı aralığı {_ar(bs.get('fark_col_rastgele'))}; COL / RASTGELE katı {_f(A.get('kat_col_rastgele'))} "
          f"(aralık {_ar(bs.get('kat_col_rastgele'))}); COL − OLUMSUZ {_ar(bs.get('fark_col_olumsuz'))}.",
          f"Bilgi: 'en az 1 gün' tanımıyla karar {A['bilgi_en_az_bir_gun_karar']}; yalnız G5'i tanımlı bölgelerde yakalama COL "
          f"{_f(A['COL']['tanimli_yakalama'])} (n {A['COL']['tanimli_n']}), RASTGELE {_f(A['RASTGELE']['tanimli_yakalama'])} (n {A['RASTGELE']['tanimli_n']}).",
          f"Karar kuralı: {E['A']['karar']['metin']}.", "",
          "## Test B — gözün gördüğünü hangi basit ölçü ayırıyor", "",
          "AUC 0,50 = ayırmıyor, 1,00 = tam ayırıyor (yönlü). LOSO = her hisse sırayla dışarıda, yön kalanlardan.", "",
          "| ölçü | yön (çöl ...) | AUC çöl vs rastgele | LOSO AUC | AUC çöl vs olumsuz | medyan çöl / rastgele / olumsuz | aday |", "|---|---|---|---|---|---|---|"]
    for t in sorted(B["tablo"], key=lambda t: -(t["loso_auc"] if t["loso_auc"] is not None and np.isfinite(t["loso_auc"]) else 0)):
        L.append(f"| {_GOZ_AD.get(t['olcu'], t['olcu'])} | {'büyük' if t['yon'] > 0 else 'küçük'} | {_f(t['auc_col_rastgele_yonlu'])} | {_f(t['loso_auc'])} | "
                 f"{_f(t['auc_col_olumsuz_yonlu'])} | {_f(t['medyan_col'], 3)} / {_f(t['medyan_rastgele'], 3)} / {_f(t['medyan_olumsuz'], 3)} | "
                 f"{'EVET' if t['aday'] else 'hayır'} |")
    if B.get("kural"):
        k = B["kural"]; lo = k["loso"]
        L += ["", f"Seçilen kural: {' VE '.join(f'{_GOZ_AD.get(x['olcu'], x['olcu'])} {'>=' if x['yon'] > 0 else '<='} {_f(x['esik'], 3)}' for x in k['tam_kural'])}; "
              f"LOSO yakalama {_f(lo['yakalama_col'])}, rastgele geçme {_f(lo['gecme_rastgele'])}, J {_f(lo['J'])}; olumsuz geçme {_f(k['gecme_olumsuz'])}."]
    L += ["", "## Test C — ikinci Cemal etiket seti", ""]
    if C.get("gecme_degil") is not None:
        L.append(f"C seti: {C['n_degil']} DEĞİL kutu, {C['n_obek']} ÖBEK. Kural DEĞİL'lerin %{_f(100 * C['gecme_degil'], 0)}'ini geçiriyor, ÖBEK'lerin "
                 f"%{_f(100 * C['gecme_obek'], 0) if C.get('gecme_obek') is not None else '—'}'ini. Karar: {C['karar']}.")
    else:
        L.append(f"{C['karar']}. Bilgi: G5 C setindeki {C['n_degil']} DEĞİL kutunun %{_f(100 * (A['C_DEGIL']['yakalama'] or 0), 0)}'ini, "
                 f"{C['n_obek']} öbeğin %{_f(100 * (A['C_OBEK']['yakalama'] or 0), 0)}'ini yakalıyor.")
    L += ["C kutularının çoğu 31.08.2026 sonrası (fon krizi dönemi; yalnız şekil). COL_GOZ kutuları kullanılmadı: sınıflar Claude'un gözü, Cemal'in 22 Ekim "
          "EVET / HAYIR dosyası repoda yok.", "",
          "## Kapsam", "",
          f"Satırlar: {kp.get('sayim')}. Veri dışı: {', '.join(x['id'] + ' (' + x['neden'] + ')' for x in kp['veri_disi']) or 'yok'}. "
          f"Kırpılan: {', '.join(x['id'] + ' (' + str(x['gun']) + ' gün)' for x in kp['kirpilan']) or 'yok'}. "
          f"20'den az rastgele pencere: {', '.join(x['id'] + ' (' + str(x['pencere']) + ')' for x in kp['rastgele_eksik']) or 'yok'}. "
          f"C'den çıkarılan (ana setle kesişen): {', '.join(kp['c_cikarilan']) or 'yok'}.", ""]
    return "\n".join(L) + "\n"


def goz_rapor(kl: Optional[str] = None) -> str:
    S = _goz_json_oku(_goz_yol("sonuc", kl))
    return _goz_yaz(_goz_yol("rapor", kl), goz_rapor_md(S))


def goz_grafik_sec(S: Dict[str, Any], E: Optional[Dict[str, Any]] = None, uygun: Optional[Any] = None) -> List[Dict[str, Any]]:
    """Önceden yazılı seçim: COL satırlarından tohumlu 3, RASTGELE satırlarından tohumlu 3 (önce farklı hisse); uygun(satır) yanlışsa (pencere
    kurulamıyor) sıradaki alınır."""
    E = E or GOZ_ESIK; G = E["grafik"]; R = pd.DataFrame(S["satirlar"]); rng = np.random.default_rng(int(G["tohum"])); out = []
    for grup, n in (("COL", int(G["col"])), ("RASTGELE", int(G["rastgele"]))):
        X = R[R.grup == grup].sort_values("id").reset_index(drop=True); sira = rng.permutation(len(X)); sec: List[int] = []; hs: set = set()
        for gecis in (0, 1):
            for i in sira:
                if len(sec) >= n:
                    break
                if i in sec or (gecis == 0 and X.sembol[i] in hs):
                    continue
                if uygun is not None and not uygun(dict(X.iloc[i])):
                    continue
                sec.append(int(i)); hs.add(X.sembol[i])
        out += [dict(X.iloc[i]) for i in sec]
    return out


def goz_grafik(kl: Optional[str] = None, cikti: Optional[str] = None, S_test: Optional[Dict[str, pd.DataFrame]] = None,
               E: Optional[Dict[str, Any]] = None) -> List[str]:
    """6 PNG: KOR_TEST v1.1 kor_ciz_fig11 + bölge gölgesi + G5 günleri. Hisse adı / tarih / başlık yok. Repoya yazılmaz."""
    E = E or GOZ_ESIK; G = E["grafik"]; cikti = cikti or GOZ_YOL["grafik"]
    if os.path.abspath(cikti).startswith(os.path.abspath(KOK_GOZ) + os.sep):
        raise GozHata("grafikler repoya yazılmaz (klasör repo içinde)")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import KOR_TEST as KT  # noqa: N814  (yalnız çizim; DEĞİŞTİRİLMEZ)
    S = _goz_json_oku(_goz_yol("sonuc", kl))
    if S_test is None:
        S_test = V2.v2_fiyat("BIST")["S"]
    os.makedirs(cikti, exist_ok=True); yazilan = []
    E_k = copy.deepcopy(KT.KOR_ESIK); E_k["grafik"]["bar"] = int(G["bar"])
    def konum(r: Dict[str, Any]) -> Tuple[pd.DataFrame, int, int, int]:
        d = S_test[r["sembol"]]; gi = goz_gunler(d, r["bas"], r["son"]); b, e = int(gi[0]), int(gi[-1])
        return d, b, e, min(e + int(G["sag_ek"]), len(d) - 1)

    def uygun(r: Dict[str, Any]) -> bool:
        if r["sembol"] not in S_test:
            return False
        d, _b, _e, t = konum(r)
        try:
            KT.kor_pencere11(d, t, E_k)
            return True
        except KT.KorHata:
            return False
    for j, r in enumerate(goz_grafik_sec(S, E, uygun)):
        d, b, e, t = konum(r); W, _bilgi = KT.kor_pencere11(d, t, E_k); g5 = goz_g5(d)["g5"]
        fig = KT.kor_ciz_fig11(W, E_k); ax = fig.axes[0]; n = len(W); b0 = t - n + 1
        ax.axvspan(b - t - 0.5, e - t + 0.5, color="#fff2a8", alpha=0.6, zorder=0)
        xs = [i - t for i in range(b0, t + 1) if g5[i]]
        y0, y1 = ax.get_ylim(); ax.scatter(xs, [y0 + 0.015 * (y1 - y0)] * len(xs), marker="|", s=90, color="black", linewidths=1.6)
        y = os.path.join(cikti, f"goz_g5_{j + 1}_{'COL' if r['grup'] == 'COL' else 'RASTGELE'}.png")
        fig.savefig(y, dpi=fig.dpi)
        plt.close(fig)
        yazilan.append(y)
    gozlog.info("%d grafik: %s", len(yazilan), cikti)
    return yazilan


def _cakisma_kontrol_goz(_once=_CK_ONCE_GOZ, _dosya="GOZ_G5.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_GOZ", "_CK_KAYIT", "_cakisma_kontrol_goz", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "re", "hashlib", "copy", "subprocess", "_dt", "annotations",
           "Any", "Dict", "List", "Optional", "Tuple", "V1", "V2")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_goz()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=GOZ_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "grafik", "rapor"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--sapma", default=None, help="kos: ön kayıttan sonra kod değiştiyse gerekçe (sonuca yazılır)")
    a_ = ap.parse_args()
    try:
        if a_.komut == "onkayit":
            y_ = goz_onkayit(a_.cikti); print(y_, "mühür", goz_esik_sha(), "kod", goz_kod_sha(), "dosya", goz_sha_dosya(y_))
        elif a_.komut == "kos":
            s_ = goz_kos(a_.cikti, sapma=a_.sapma)
            print(json.dumps({"A": s_["A"]["karar"], "B_aday": s_["B"]["aday"], "C": s_["C"]["karar"]}, ensure_ascii=False)); print(_goz_yol("rapor", a_.cikti))
        elif a_.komut == "grafik":
            print("\n".join(goz_grafik(a_.cikti)))
        else:
            print(goz_rapor(a_.cikti))
    except (GozHata, V2.Vdyt2Hata, V1.VdytHata, FileNotFoundError) as ex:
        gozlog.error("%s", ex); sys.exit(1)
