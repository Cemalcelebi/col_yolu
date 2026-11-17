"""GOZ_ETIKET — kodun bulduğu S6 bölgelerini Cemal'in gözüyle (kör) etiketleme hazırlığı: AŞAMA A (17 Kasım 2026 akşam;
iş tanımı arastirma_cikti/goz_etiket/GOZ_ETIKET_IS_TANIMI.md §3).

Cemal (17 Kas akşam): 'Benim nasıl karar aldığımı biliyorsun: mum dizilimi, taban oluşumu, taban savunması, mumların küçüklüğü, alt fitil kısa,
açılış ile dip neredeyse yakın. Kodun bulduğu bütün bölgeleri olur / olmaz + neden diye etiketle, koda aktar, eğit, metrik çıkar.'
Bu modül AŞAMA A'dır: ÖRNEKLEM (300 olay), KÖR GÖRSEL (PNG; t'den sonrası YOK), SAYISAL ÖZELLİK (F1-F18; bütün 26.663 Y1 olayı, yalnız t'ye
kadar) ve ÖN KAYIT (ON_KAYIT.md; §5 ölçüm planı aynen). Hiçbir sonuç / getiri / hedef sütunu OKUNMAZ (GE_KIMLIK_KOL + GE_SINYAL_KOL dışı yasak).

TANIM (ayrıntı GE_ESIK; sinyal günü t = S6 'al' günü, Y1 olayı; i = t'nin geçerli bar sırası):
  Veri: ORTAK_CETVEL.oc_veri(pazar) -> YAPI_HEDEF._yh_hazir (SY.sy_veri_hazirla: geçerli bar H>L, V>0, O/H/L/C>0; kriz kesiği 31.08.2026).
  S6: S6_TABAN.s6_taban (prm varsayılan v1.1); hat / tavan / BÖLGE YAPI_HEDEF Y1 / Y6 ile AYNI:
      hat = kutu_alt(t) (durum AL) ya da DİP(t-1) (AL_BOLGESIZ); tavan = TAVAN(t-1);
      BÖLGE = [kutu_sol_i(t), t-1] (AL) ya da [bas_i(t-1), t-1] (AL_BOLGESIZ); t bölgeye girmez.
  ÖRNEKLEM: olay_Y1.csv.gz yalnız kimlik sütunlarıyla (deneme, pazar, sembol, tarih, giris, donem); uygun = dönem 2023 / 2024-26 VE giriş
      <= kriz - 30 gün (15 barlık ölçü penceresi kriz kesiğini aşmasın; yalnız tarih kuralı); pazar x dönem katmanı (ABD 60 / 80, AVR 40 / 60,
      BIST 20 / 40 = 300); tohum 11; katman sırasıyla rastgele permütasyon, aynı (pazar, sembol) en çok 2; sonra 300 olay karıştırılıp No 1..300.
  GÖRSEL: veri t'de KESİLİR (dk = d[:t]), S6 kesik veride yeniden hesaplanır (hat / tavan olay dosyasıyla aynı olmalı, yoksa DURUR), son 120 bar
      mum + hacim, S6 bölgesi (mavi alan), tavan ve hat çizgisi; x ekseni bar sırası (-119..0; tarih yok), y ekseni gerçek fiyat; başlık yalnız
      'No k'. Dosya adı No_k.png (PNG metin parçası yok). Anahtar (no -> sembol, pazar, tarih) anahtar.json (GİZLİ; etiketleyen açmaz).
  ÖZELLİKLER F1-F18 (GE_ESIK['ozellik']; hepsi yalnız [.., t] verisiyle; prefix değişmezliği koşuda ve testte denetlenir).
Komut:  python GOZ_ETIKET.py orneklem                 olay_Y1 kimlik sütunları -> anahtar.json (300 olay)
        python GOZ_ETIKET.py gorsel [--png KLASOR]     anahtar.json + veri -> No_k.png (300)
        python GOZ_ETIKET.py ozellik [--islem 4]       bütün Y1 olayları -> ozellik_Y1.csv.gz (+ prefix denetimi, hat / tavan eşitliği)
        python GOZ_ETIKET.py onkayit                   ON_KAYIT.md (sha'lar, örneklem dağılımı, özellik tanımı, §5 aynen, kontrol tablosu + kapı)
Colab:  exec(open('GOZ_ETIKET.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_BIST.pkl, V_ABD.pkl, V_AVR.pkl (OC_VERI; git worktree add /tmp/iv origin/islenmis-veri; python FON_IZI.py vpac /tmp/iv/veri /tmp/veri).
Evren bugün işlem gören hisseler (hayatta kalma yanlılığı; AŞAMA C raporunda yazılır).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_GE = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_GE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_GE not in sys.path:
    sys.path.insert(0, KOK_GE)

import ORTAK_CETVEL as OC  # noqa: E402
import S6_TABAN as S6  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

gelog = logging.getLogger("col.goz_etiket")
if not gelog.handlers:
    _ge_h = logging.StreamHandler(sys.stderr)
    _ge_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s goz_etiket: %(message)s", "%H:%M:%S"))
    gelog.addHandler(_ge_h)
    gelog.setLevel(logging.INFO)
    gelog.propagate = False

GE_SURUM = "GOZ_ETIKET v1.0 (2026-11-17): AŞAMA A örneklem (300, tohum 11) + kör PNG (t sonrası yok) + F1-F18 özellik + ön kayıt"
_GE_SCRATCH = "/tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/goz_etiket/png"
GE_YOL = {"cikti": os.path.join(KOK_GE, "arastirma_cikti", "goz_etiket"),
          "olay": os.path.join(KOK_GE, "arastirma_cikti", "yapi_hedef", "olay_Y1.csv.gz"),
          "png": os.environ.get("GE_PNG", _GE_SCRATCH),
          "veri": os.environ.get("OC_VERI", "/tmp/veri"),
          "kod": os.path.join(KOK_GE, "GOZ_ETIKET.py"), "yh_kod": os.path.join(KOK_GE, "YAPI_HEDEF.py"),
          "s6_kod": os.path.join(KOK_GE, "S6_TABAN.py"), "oc_kod": os.path.join(KOK_GE, "ORTAK_CETVEL.py"),
          "is_tanimi": os.path.join(KOK_GE, "arastirma_cikti", "goz_etiket", "GOZ_ETIKET_IS_TANIMI.md")}
GE_DOSYA = {"anahtar": "anahtar.json", "ozellik": "ozellik_Y1.csv.gz", "onkayit": "ON_KAYIT.md", "ozellik_denetim": "ozellik_denetim.json"}

# ---- sütun izinleri: örneklem yalnız KİMLİK; görsel / özellik ayrıca t'de bilinen SİNYAL sütunları (hat / tavan doğrulaması). Gerisi YASAK.
GE_KIMLIK_KOL = ["deneme", "pazar", "sembol", "tarih", "giris", "donem"]
GE_SINYAL_KOL = ["hat", "tavan", "n", "ek"]
GE_SONUC_KOL_ORNEK = ["h5", "h10", "st5", "h5H", "h10H", "k5", "kst", "es_h5", "es_h10", "es_st5", "n_es", "tb_h5", "pl_h5", "getiri",
                      "cikis_bar", "cikis_tur", "olc", "E0", "dd", "stop0", "d", "j", "hucre", "hafiza"]   # bilgi (yasak sütun örnekleri)

# ================================================================ EŞİKLER (ön kayıtta mühürlü; sonuç görüldükten sonra DEĞİŞMEZ)
GE_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "kriz": "2026-08-31",
    "orneklem": {
        "tohum": 11, "deneme": "Y1",
        "katman": [["ABD", "2023", 60], ["ABD", "2024-26", 80], ["AVR", "2023", 40], ["AVR", "2024-26", 60], ["BIST", "2023", 20],
                   ["BIST", "2024-26", 40]],
        "sembol_azami": 2, "giris_kriz_pay_gun": 30,
        "tanim": "olay_Y1.csv.gz yalnız kimlik sütunları (deneme, pazar, sembol, tarih, giris, donem) okunur. Uygun = deneme Y1, dönem 2023 / "
                 "2024-26, giriş <= kriz - 30 gün (2026-08-01; 15 geçerli barlık ölçü penceresi en çok 30 takvim günü, kriz kesiğini aşmasın; "
                 "yalnız tarih kuralı). Uygunlar (pazar, sembol, tarih) sırasına dizilir; rng = numpy default_rng(11); katmanlar yukarıdaki sırayla "
                 "gezilir, her katmanda rng.permutation sırasıyla olay alınır, aynı (pazar, sembol) bütün örneklemde en çok 2 (aşan atlanır), "
                 "kota dolunca durulur (kota dolmazsa DURUR). Sonra 300 olay rng.permutation ile karıştırılır ve No 1..300 verilir (numara pazar / "
                 "dönem / tarih sırası taşımaz)."},
    "gorsel": {"bar": 120, "piksel": [1200, 800], "dpi": 100,
               "tanim": "hissenin geçerli bar verisi t'de KESİLİR (t dahil; t'den sonrası fonksiyona hiç girmez); S6 kesik veride yeniden hesaplanır "
                        "ve hat / tavan olay dosyasındakiyle (göreli 1e-5; csv 6 anlamlı basamak) aynı olmalı; son 120 bar: mum (yeşil C >= O, kırmızı C < O; fitil dahil), "
                        "alt panelde hacim; S6 bölgesi = mavi yarı saydam dikdörtgen [bölge solu, t-1] x [hat, bölge üstü] (AL: kutu_ust(t), "
                        "AL_BOLGESIZ: TAVAN(t-1)); tavan çizgisi (turuncu kesik) ve hat çizgisi (mavi) bölge solundan t'ye; x ekseni bar sırası "
                        "(-119..0, tarih yok); y ekseni gerçek fiyat; başlık yalnız 'No k'; PNG metin parçası yok; dosya adı No_k.png"},
    "ozellik": {
        "hat_bant": 0.015, "atr_gun": 250, "atr_min": 120, "konum_gun": 120, "buyuk_gun": 250, "buyuk_parca": 25, "kir_gun": 250,
        "dusus_gun": 60,
        "bolge": "BÖLGE = [kutu_sol_i(t), t-1] (durum AL) ya da [bas_i(t-1), t-1] (AL_BOLGESIZ); hat = kutu_alt(t) / DİP(t-1); tavan = TAVAN(t-1) "
                 "(YAPI_HEDEF Y1 / Y6 ile aynı). Bütün ölçüler yalnız [.., t] geçerli barlarıyla.",
        "F": {
            "F1": "hat dokunuş sayısı: bölgede Low <= hat x 1,015 olan bar sayısı",
            "F2": "hat eğimi: son dokunuşun Low'u / ilk dokunuşun Low'u - 1 (dokunuş yoksa NaN)",
            "F3": "bölge mum boyu medyanı / ATR250: medyan((H - L) / C, bölge) / ort(TR / C_önceki, bölgeden ÖNCEKİ min(250, sol - 1) bar); "
                  "120 bardan azsa NaN (YAPI_HEDEF Y7 ATR birimi)",
            "F4": "alt fitil payı medyanı: medyan((min(O, C) - L) / (H - L), bölge)",
            "F5": "açılış-dip yakınlığı: medyan((O - L) / (H - L), bölge)",
            "F6": "üst fitil payı medyanı: medyan((H - max(O, C)) / (H - L), bölge)",
            "F7": "yeşil mum payı: pay(C > O, bölge)",
            "F8": "bölge boyu n: bölgedeki geçerli bar sayısı (t - sol)",
            "F9": "bant: tavan / hat - 1",
            "F10": "net: C(t-1) / C(sol) - 1 (bölgenin son / ilk kapanışı)",
            "F11": "kırılım mumu payı: C_t / tavan - 1",
            "F12": "kırılım mumu gövdesi / bölge medyan mumu: |C_t - O_t| / medyan(H - L, bölge)",
            "F13": "kırılım günü hacmi / bölge medyan hacmi: V_t / medyan(V, bölge)",
            "F14": "büyük desen eğimi: [t-250, t-1] 10 parça x 25 bar dip noktalarına doğru, uyum(9) / uyum(0) - 1 (YAPI_HEDEF.yh_buyuk_egim); "
                   "250 bar yoksa ya da uyum(0) <= 0 ise NaN",
            "F15": "120 gün konumu: (C_t - min C) / (max C - min C), t dahil son 120 geçerli kapanış (aralık 0 ise NaN)",
            "F16": "son 250 barda KIRILDI bölge sayısı: [t-250, t-1] içinde S6 durumu 'KIRILDI' olan bar sayısı (bölge KIRILDI ile biter; "
                   "YAPI_HEDEF Y8 kir250 ile aynı)",
            "F17": "bölge öncesi 60 gün düşüş: C(sol) / max(C, [sol-60, sol-1]) - 1 (60 geçerli bar yoksa NaN)",
            "F18": "stop uzaklığı: C_t / hat - 1",
        },
    },
    "denetim": {"prefix_n": 10, "prefix_tohum": 615, "hat_tol": 1e-5,
                "tanim": "ozellik koşusunda her pazardan rastgele 10 olay: veri t'de kesilir, S6 ve F1-F18 yeniden hesaplanır, tam seriyle aynı olmalı "
                         "(NaN = NaN, göreli 1e-9); her olayda hat / tavan olay dosyasıyla aynı olmalı (göreli 1e-5: olay_Y1.csv.gz 6 anlamlı basamak); tutmazsa koşu DURUR"},
}

GE_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "AŞAMA A ölçüm yapmaz (etiket / özellik / görsel); kontrol grubu AŞAMA C'de: §5 eşli KAT5 = Σ h5 / Σ es_h5 (olay_Y1 eş "
                         "sütunları: aynı giriş günü, aynı OC kovası, aynı d ve kural) ve göz skoru üst / alt beşte bir aynı eşli cetvelle"),
    "K2": ("EVET", "örneklem yalnız kimlik sütunlarını okur (ge_olay_oku izin listesi; test: sonuç sütunları silinince / karıştırılınca örneklem "
                   "aynı); görsel veri t'de kesilerek çizilir (test: t sonrası barlar değişince PNG baytları aynı, son bar = t); F1-F18 yalnız [.., t] "
                   "(test + koşuda 10 olay / pazar prefix denetimi, tutmazsa DURUR); hat / tavan kesik veriden yeniden üretilir ve olay dosyasıyla aynı"),
    "K3": ("EVET", "veri YAPI_HEDEF._yh_hazir (SY.sy_veri_hazirla: H>L, V>0, O/H/L/C>0) ile; S6 ve bütün özellikler geçerli bar dizisinde; olay "
                   "günleri Y1 (geçerli bar)"),
    "K4": ("EVET", "olaylar olay_Y1 (OC.oc_olay_hazirla: aynı hissede 60 gün tekil); örneklemde aynı (pazar, sembol) en çok 2; (pazar, sembol, "
                   "tarih) tekil denetlenir"),
    "K5": ("UYGULANMAZ", "giriş fiyatı / getiri bu aşamada hesaplanmaz; AŞAMA C olay_Y1 sonuçlarını (giriş t+1 açılış) kullanır"),
    "K6": ("EVET", "tek kip V_*.pkl (düzeltilmiş fiyat; YAPI_HEDEF ile aynı veri, hat / tavan eşitliği denetimi); özellikler oran / pay (birimden "
                   "bağımsız); görselde y ekseni yerel para gerçek fiyat"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (V_ABD 1.411, k34 yok); örneklem ve özellikler aynı evrenden; AŞAMA C raporuna hayatta kalma "
                   "notu (hedef payı yukarı yanlı) yazılır"),
    "K8": ("EVET", "300 etiket küçük örneklem: §5 OLUR n < 30 ÖLÇÜLEMEDİ; pazar birleşik karar, pazar bazlı bilgi; göz skoru karar hücreleri n >= "
                   "1.000 güç kuralı; ölçü 2 BH q 0,10; katmanlar iki dönem x üç pazar"),
    "K9": ("EVET", "ON_KAYIT.md: GE_ESIK sha + GOZ_ETIKET / YAPI_HEDEF / S6_TABAN / ORTAK_CETVEL kod sha + olay_Y1 / anahtar / özellik dosyası sha "
                   "+ iş tanımı git kaydı; §5 ölçüm planı ve eşikleri iş tanımından aynen; etiketlemeden ve ölçümden ÖNCE ayrı commit; eşik "
                   "sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve olay_Y1 kimlik sütunları"),
    "K11": ("EVET", "anahtar.json + ozellik_Y1.csv.gz satır dosyaları; tohum 11 ile örneklem ve özellikler aynı komutla yeniden üretilir (test: "
                    "aynı tohum aynı örneklem); AŞAMA C en az iki hücreyi satır dosyasından yeniden üretir"),
    "K12": ("EVET", "AŞAMA A hiçbir sonuç / iz / emare sözü yazmaz; etiket = Cemal'in gözünün VEKİLİ (dil modeli), Cemal'in kendi etiketi değil "
                    "(§5 sınırlar); karar dili yalnız §5 kuralıyla"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_ge (test); yasak defter dosyalarına dokunulmadı (git diff); e-posta / anahtar taraması yazım "
                    "öncesi (_ge_sizinti); PNG'ler repoya girmez (scratchpad); push yok; kod değişirse 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; etiket ve ölçüm hazırlığı"),
}


class GEHata(RuntimeError):
    """Durdurucu hata: yasak sütun istendi, örneklem kotası dolmadı, hat / tavan tutmadı, prefix denetimi tutmadı, veri yok, girdi bozuk."""


# ================================================================ 0) ORTAK
_GE_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_GE_ANAHTAR = re.compile(r"(?i)(api[_-]?key|token|secret|password|şifre)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}")


def _ge_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _ge_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def ge_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    s = json.dumps(GE_ESIK if E is None else E, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _ge_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or GE_YOL["cikti"], GE_DOSYA.get(ad, ad))


def _ge_sizinti(metin: str, ad: str) -> None:
    if _GE_EPOSTA.search(metin) or _GE_ANAHTAR.search(metin):
        raise GEHata(f"{ad}: e-posta / anahtar benzeri metin var; yazılmadı")


def _ge_yaz(yol: str, metin: str, ad: str) -> None:
    _ge_sizinti(metin, ad)
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)


def ge_olay_oku(kolonlar: List[str], yol: Optional[str] = None) -> pd.DataFrame:
    """olay_Y1.csv.gz'den YALNIZ izinli sütunlar (GE_KIMLIK_KOL + GE_SINYAL_KOL). Sonuç sütunu istenirse DURUR; dosya usecols ile okunur
    (sonuç sütunları belleğe hiç girmez)."""
    izin = set(GE_KIMLIK_KOL) | set(GE_SINYAL_KOL)
    yasak = [k for k in kolonlar if k not in izin]
    if yasak:
        raise GEHata(f"yasak sütun istendi (AŞAMA A sonuç sütunu okumaz): {yasak}")
    yol = yol or GE_YOL["olay"]
    if not os.path.exists(yol):
        raise GEHata(f"olay dosyası yok: {yol}")
    try:
        X = pd.read_csv(yol, usecols=list(kolonlar), dtype={"sembol": str, "pazar": str, "donem": str, "deneme": str})
    except ValueError as ex:
        raise GEHata(f"olay dosyası sütunu eksik: {ex}")
    for k in ("tarih", "giris"):
        if k in X:
            X[k] = pd.to_datetime(X[k])
    return X


# ================================================================ 1) ÖRNEKLEM (yalnız kimlik sütunları)
def ge_orneklem(yol: Optional[str] = None, E: Dict[str, Any] = GE_ESIK) -> pd.DataFrame:
    """Katmanlı örneklem -> DataFrame[no, pazar, donem, sembol, tarih, giris] (no 1..N, karıştırılmış)."""
    O = E["orneklem"]
    X = ge_olay_oku(GE_KIMLIK_KOL, yol)
    if X.duplicated(["pazar", "sembol", "tarih"]).any():
        raise GEHata("olay dosyasında (pazar, sembol, tarih) tekil değil")
    sinir = pd.Timestamp(E["kriz"]) - pd.Timedelta(days=int(O["giris_kriz_pay_gun"]))
    donemler = sorted({k[1] for k in O["katman"]})
    U = X[(X.deneme == O["deneme"]) & X.donem.isin(donemler) & (X.giris <= sinir)]
    U = U.sort_values(["pazar", "sembol", "tarih"], kind="mergesort").reset_index(drop=True)
    rng = np.random.default_rng(int(O["tohum"]))
    say: Dict[Tuple[str, str], int] = {}
    sec: List[pd.DataFrame] = []
    for pazar, donem, kota in O["katman"]:
        K = U[(U.pazar == pazar) & (U.donem == donem)].reset_index(drop=True)
        al: List[int] = []
        for r in rng.permutation(len(K)):
            if len(al) >= int(kota):
                break
            a = (pazar, str(K.sembol.iat[r]))
            if say.get(a, 0) >= int(O["sembol_azami"]):
                continue
            say[a] = say.get(a, 0) + 1; al.append(int(r))
        if len(al) < int(kota):
            raise GEHata(f"katman {pazar} {donem}: kota {kota} dolmadı ({len(al)}; uygun {len(K)})")
        sec.append(K.iloc[al])
    S = pd.concat(sec, ignore_index=True)
    S = S.iloc[rng.permutation(len(S))].reset_index(drop=True)
    S.insert(0, "no", np.arange(1, len(S) + 1))
    return S[["no", "pazar", "donem", "sembol", "tarih", "giris"]]


def ge_anahtar_yaz(S: pd.DataFrame, cikti: Optional[str] = None, E: Dict[str, Any] = GE_ESIK) -> str:
    yol = _ge_yol("anahtar", cikti)
    J = {"uyari": "GİZLİ ANAHTAR: etiketleyen (AŞAMA B) bu dosyayı AÇMAZ. no -> sembol, pazar, tarih (sinyal günü t), giris, donem.",
         "surum": GE_SURUM, "esik_sha": ge_esik_sha(E), "olay_sha": _ge_sha_dosya(GE_YOL["olay"]) if os.path.exists(GE_YOL["olay"]) else None,
         "n": int(len(S)),
         "olay": {str(int(r.no)): {"sembol": r.sembol, "pazar": r.pazar, "tarih": str(pd.Timestamp(r.tarih).date()),
                                   "giris": str(pd.Timestamp(r.giris).date()), "donem": r.donem} for r in S.itertuples()}}
    _ge_yaz(yol, json.dumps(J, ensure_ascii=False, indent=1), "anahtar")
    gelog.info("anahtar: %s (%d olay)", yol, len(S))
    return yol


def ge_anahtar_oku(cikti: Optional[str] = None) -> pd.DataFrame:
    yol = _ge_yol("anahtar", cikti)
    if not os.path.exists(yol):
        raise GEHata(f"anahtar yok: {yol} (önce `python GOZ_ETIKET.py orneklem`)")
    J = json.load(open(yol, encoding="utf-8"))
    S = pd.DataFrame([{"no": int(k), **v} for k, v in J["olay"].items()]).sort_values("no").reset_index(drop=True)
    S["tarih"] = pd.to_datetime(S["tarih"]); S["giris"] = pd.to_datetime(S["giris"])
    return S


# ================================================================ 2) BÖLGE ve ÖZELLİKLER (yalnız t ve öncesi)
def ge_hazir(df: pd.DataFrame) -> pd.DataFrame:
    """YAPI_HEDEF ile aynı hazırlık (geçerli bar, kriz kesiği)."""
    return YH._yh_hazir(df)


def ge_s6(d: pd.DataFrame) -> Dict[str, np.ndarray]:
    """S6 durum dizileri (kesik ya da tam veride; S6 nedensel)."""
    T = S6.s6_taban(d, None)
    return {"durum": T["durum"].to_numpy(object), "kutu_sol_i": T["kutu_sol_i"].to_numpy(float), "kutu_alt": T["kutu_alt"].to_numpy(float),
            "kutu_ust": T["kutu_ust"].to_numpy(float), "bas_i": T["bas_i"].to_numpy(float), "dip": T["dip"].to_numpy(float),
            "tavan": T["tavan"].to_numpy(float), "al": T["al"].to_numpy(bool)}


def ge_bolge(T: Dict[str, np.ndarray], i: int) -> Dict[str, Any]:
    """t = i için Y1 hat / tavan ve BÖLGE [sol, i-1] (YAPI_HEDEF yh_s6_hisse + yh_y6_bayrak ile aynı). al değilse GEHata."""
    if i < 1 or not bool(T["al"][i]):
        raise GEHata(f"bar {i} S6 'al' günü değil")
    dur = str(T["durum"][i])
    if dur == "AL":
        hat = float(T["kutu_alt"][i]); sol = T["kutu_sol_i"][i]; ust = float(T["kutu_ust"][i])
    else:
        hat = float(T["dip"][i - 1]); sol = T["bas_i"][i - 1]; ust = float(T["tavan"][i - 1])
    tav = float(T["tavan"][i - 1])
    if not (np.isfinite(sol) and 0 <= int(sol) < i and np.isfinite(hat) and hat > 0):
        raise GEHata(f"bar {i}: bölge / hat tanımsız ({dur}, sol {sol}, hat {hat})")
    return {"durum": dur, "hat": hat, "tavan": tav, "ust": ust, "sol": int(sol)}


def _ge_trp(H: np.ndarray, L: np.ndarray, C: np.ndarray) -> np.ndarray:
    return YH._yh_trp(H, L, C)


def ge_ozellik_bar(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, V: np.ndarray, T: Dict[str, np.ndarray], i: int,
                   E: Dict[str, Any] = GE_ESIK) -> Dict[str, float]:
    """F1-F18 (t = i); yalnız [0..i] kullanılır (dizilerin i'den sonrası okunmaz: her dilim i + 1 ile sınırlı)."""
    P = E["ozellik"]; B = ge_bolge(T, i)
    O, H, L, C, V = O[:i + 1], H[:i + 1], L[:i + 1], C[:i + 1], V[:i + 1]
    hat, tav, sol = B["hat"], B["tavan"], B["sol"]
    z = slice(sol, i)                                     # bölge [sol, i-1]
    Oz, Hz, Lz, Cz, Vz = O[z], H[z], L[z], C[z], V[z]
    rz = Hz - Lz
    F: Dict[str, float] = {}
    dok = np.flatnonzero(Lz <= hat * (1 + P["hat_bant"]))
    F["F1"] = float(len(dok))
    F["F2"] = float(Lz[dok[-1]] / Lz[dok[0]] - 1) if len(dok) else np.nan
    trp = _ge_trp(H, L, C)
    cnt = min(int(P["atr_gun"]), sol - 1)
    atr = float(np.mean(trp[sol - cnt:sol])) if cnt >= int(P["atr_min"]) else np.nan
    m = float(np.median(rz / Cz))
    F["F3"] = m / atr if np.isfinite(atr) and atr > 0 else np.nan
    F["F4"] = float(np.median((np.minimum(Oz, Cz) - Lz) / rz))
    F["F5"] = float(np.median((Oz - Lz) / rz))
    F["F6"] = float(np.median((Hz - np.maximum(Oz, Cz)) / rz))
    F["F7"] = float(np.mean(Cz > Oz))
    F["F8"] = float(i - sol)
    F["F9"] = float(tav / hat - 1) if np.isfinite(tav) else np.nan
    F["F10"] = float(C[i - 1] / C[sol] - 1)
    F["F11"] = float(C[i] / tav - 1) if np.isfinite(tav) and tav > 0 else np.nan
    mr = float(np.median(rz))
    F["F12"] = float(abs(C[i] - O[i]) / mr) if mr > 0 else np.nan
    mv = float(np.median(Vz))
    F["F13"] = float(V[i] / mv) if mv > 0 else np.nan
    G = int(P["buyuk_gun"])
    if i >= G:
        e = YH.yh_buyuk_egim(L[i - G:i], int(P["buyuk_parca"]))
        F["F14"] = float(e) if np.isfinite(e) else np.nan
    else:
        F["F14"] = np.nan
    k = int(P["konum_gun"]); c120 = C[max(0, i - k + 1):i + 1]
    lo, hi = float(c120.min()), float(c120.max())
    F["F15"] = float((C[i] - lo) / (hi - lo)) if len(c120) == k and hi > lo else np.nan
    g = int(P["kir_gun"]); dur = T["durum"][:i + 1]
    F["F16"] = float(np.sum(dur[max(0, i - g):i] == "KIRILDI"))
    q = int(P["dusus_gun"])
    F["F17"] = float(C[sol] / np.max(C[sol - q:sol]) - 1) if sol >= q else np.nan
    F["F18"] = float(C[i] / hat - 1)
    return F


def ge_ozellik_hisse(df: pd.DataFrame, tarihler: List[pd.Timestamp], hazir: bool = False, E: Dict[str, Any] = GE_ESIK
                     ) -> Tuple[List[Dict[str, float]], List[Dict[str, Any]]]:
    """Bir hissenin olay günleri için F1-F18 ve bölge bilgisi (hat / tavan doğrulaması için)."""
    d = df if hazir else ge_hazir(df)
    T = ge_s6(d)
    O, H, L, C, V = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    pos = d.index.get_indexer(pd.DatetimeIndex(tarihler))
    if (pos < 0).any():
        raise GEHata(f"olay günü veride yok: {[str(t) for t, p in zip(tarihler, pos) if p < 0][:3]}")
    Fs, Bs = [], []
    for i in pos:
        Bs.append(ge_bolge(T, int(i))); Fs.append(ge_ozellik_bar(O, H, L, C, V, T, int(i), E))
    return Fs, Bs


_GE_IS_V: Dict[str, pd.DataFrame] = {}


def _ge_ozellik_isci(is_: List[Tuple[str, List[pd.Timestamp], List[float], List[float]]]) -> List[Dict[str, Any]]:
    out = []
    for s, tl, hl, tvl in is_:
        try:
            Fs, Bs = ge_ozellik_hisse(_GE_IS_V[s], tl)
            for t, f, b, h0, tv0 in zip(tl, Fs, Bs, hl, tvl):
                ok = bool(abs(b["hat"] / h0 - 1) <= GE_ESIK["denetim"]["hat_tol"]
                          and (abs(b["tavan"] / tv0 - 1) <= GE_ESIK["denetim"]["hat_tol"]))
                out.append({"sembol": s, "tarih": t, **f, "_hat_ok": ok, "_hata": ""})
        except Exception as ex:  # tek hisse bozuksa öteki hisseler sürer; sayımda ve sonda DURUR
            gelog.warning("özellik %s atlandı: %s", s, ex)
            for t in tl:
                out.append({"sembol": s, "tarih": t, "_hat_ok": False, "_hata": str(ex)[:200]})
    return out


def ge_prefix_denetimi(Vd: Dict[str, Any], X: pd.DataFrame, n: int, tohum: int, E: Dict[str, Any] = GE_ESIK) -> int:
    """Rastgele n olay: veri t'de kesilir, F1-F18 yeniden; tam seri sonucuyla aynı olmalı (NaN = NaN). Tutmazsa GEHata."""
    if not len(X):
        return 0
    rng = np.random.default_rng(tohum)
    sec = rng.choice(len(X), size=min(n, len(X)), replace=False)
    Fk = [f"F{k}" for k in range(1, 19)]
    for q in sec:
        r = X.iloc[int(q)]
        d = ge_hazir(Vd["V"][r.sembol]); t = pd.Timestamp(r.tarih)
        dk = d[d.index <= t]
        Fk_, _ = ge_ozellik_hisse(dk, [t], hazir=True, E=E)
        a = np.array([Fk_[0][k] for k in Fk], float); b = r[Fk].to_numpy(float)
        if not np.allclose(a, b, rtol=1e-9, atol=1e-12, equal_nan=True):
            raise GEHata(f"prefix denetimi tutmadı: {r.sembol} {t.date()} ({dict(zip(Fk, zip(a, b)))})")
    return int(len(sec))


def ge_ozellik(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, olay: Optional[str] = None,
               E: Dict[str, Any] = GE_ESIK) -> str:
    """Bütün Y1 olayları -> ozellik_Y1.csv.gz (pazar, sembol, tarih, durum, F1..F18); hat / tavan eşitliği + prefix denetimi."""
    global _GE_IS_V
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    X = ge_olay_oku(["deneme", "pazar", "sembol", "tarih", "hat", "tavan", "ek"], olay)
    X = X[X.deneme == "Y1"].reset_index(drop=True)
    Fk = [f"F{k}" for k in range(1, 19)]
    parcalar: List[pd.DataFrame] = []; denetim: Dict[str, Any] = {"zaman_utc": _ge_simdi(), "pazar": {}}
    for pno, p in enumerate(OC.OC_ESIK["pazar"]):
        Xp = X[X.pazar == p]
        if not len(Xp):
            continue
        Vd = OC.oc_veri(p, klasor=veri or GE_YOL["veri"])
        eksik = sorted(set(Xp.sembol) - set(Vd["V"]))
        if eksik:
            raise GEHata(f"{p}: olay sembolü veride yok: {eksik[:5]}")
        G = Xp.groupby("sembol", sort=True)
        isler = [(s, list(g.tarih), list(g.hat.astype(float)), list(g.tavan.astype(float))) for s, g in G]
        k = max(1, islem * 4); dilim = [isler[j::k] for j in range(k)]
        _GE_IS_V = Vd["V"]
        try:
            if islem > 1:
                import multiprocessing as mp
                with mp.get_context("fork").Pool(islem) as havuz:
                    R = havuz.map(_ge_ozellik_isci, [x for x in dilim if x])
            else:
                R = [_ge_ozellik_isci(x) for x in dilim if x]
        finally:
            _GE_IS_V = {}
        Z = pd.DataFrame([y for r in R for y in r])
        Z.insert(0, "pazar", p)
        hata = Z[Z["_hata"].astype(str) != ""]
        if len(hata):
            raise GEHata(f"{p}: {len(hata)} olayda özellik hesaplanamadı (ör. {hata.sembol.iat[0]}: {hata['_hata'].iat[0]})")
        if not Z["_hat_ok"].all():
            b = Z[~Z["_hat_ok"]]
            raise GEHata(f"{p}: {len(b)} olayda hat / tavan olay dosyasıyla tutmadı (ör. {b.sembol.iat[0]} {b.tarih.iat[0]})")
        Z = Z.merge(Xp[["sembol", "tarih", "ek"]], on=["sembol", "tarih"], how="left", validate="one_to_one")
        Z["durum"] = Z["ek"].astype(str).str.split(";").str[0]
        npre = ge_prefix_denetimi(Vd, Z, int(E["denetim"]["prefix_n"]), int(E["denetim"]["prefix_tohum"]) + pno, E)
        denetim["pazar"][p] = {"olay": int(len(Z)), "hat_tavan_esit": int(Z["_hat_ok"].sum()), "prefix_denetimi": npre,
                               "nan": {f: int(Z[f].isna().sum()) for f in Fk}}
        parcalar.append(Z[["pazar", "sembol", "tarih", "durum"] + Fk])
        gelog.info("özellik %s: %d olay, prefix %d tuttu (%.0f sn)", p, len(Z), npre, time.time() - t0)
        del Vd
    Ft = pd.concat(parcalar, ignore_index=True)
    sira = X[["pazar", "sembol", "tarih"]].reset_index().rename(columns={"index": "_sira"})
    Ft = Ft.merge(sira, on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one").sort_values("_sira").drop(columns="_sira")
    if len(Ft) != len(X):
        raise GEHata(f"özellik satırı {len(Ft)} != olay {len(X)}")
    Ft["tarih"] = pd.to_datetime(Ft["tarih"]).dt.strftime("%Y-%m-%d")
    yol = _ge_yol("ozellik", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True)
    Ft.to_csv(yol, index=False, float_format="%.6g", compression={"method": "gzip", "mtime": 0})
    denetim["sure_sn"] = round(time.time() - t0, 1); denetim["satir"] = int(len(Ft)); denetim["sha"] = _ge_sha_dosya(yol)
    _ge_yaz(_ge_yol("ozellik_denetim", cikti), json.dumps(denetim, ensure_ascii=False, indent=1), "özellik denetimi")
    gelog.info("özellik dosyası: %s (%d satır, %.0f sn)", yol, len(Ft), time.time() - t0)
    return yol


# ================================================================ 3) KÖR GÖRSEL (t'den sonrası YOK)
def ge_gorsel_veri(df: pd.DataFrame, t: pd.Timestamp, hazir: bool = False, E: Dict[str, Any] = GE_ESIK) -> Dict[str, Any]:
    """Veriyi t'de KESER, S6'yı kesik veride hesaplar; son 120 bar + bölge geometrisi. t sonrası bar dönüş değerine giremez."""
    d = df if hazir else ge_hazir(df)
    t = pd.Timestamp(t)
    dk = d[d.index <= t]
    if not len(dk) or dk.index[-1] != t:
        raise GEHata(f"sinyal günü {t.date()} geçerli bar değil")
    i = len(dk) - 1
    T = ge_s6(dk); B = ge_bolge(T, i)
    nb = int(E["gorsel"]["bar"]); a = max(0, i - nb + 1)
    W = dk.iloc[a:i + 1]
    return {"W": W, "hat": B["hat"], "tavan": B["tavan"], "ust": B["ust"], "sol": B["sol"] - a, "son": i - a, "durum": B["durum"]}


def ge_ciz(G: Dict[str, Any], no: int, yol: str, E: Dict[str, Any] = GE_ESIK) -> str:
    """Kör PNG: başlık yalnız 'No k'; x ekseni bar sırası; metin parçası yok."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    W = G["W"]; n = len(W); x = np.arange(n) - (n - 1)
    O, H, L, C, V = (W[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    px, py = E["gorsel"]["piksel"]; dpi = int(E["gorsel"]["dpi"])
    fig = plt.figure(figsize=(px / dpi, py / dpi), dpi=dpi)
    try:
        gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1], hspace=0.05)
        ax = fig.add_subplot(gs[0]); av = fig.add_subplot(gs[1], sharex=ax)
        yes = C >= O; renk = np.where(yes, "#1a9850", "#d73027")
        ax.vlines(x, L, H, colors=renk, linewidth=0.9, zorder=3)
        govde = np.maximum(np.abs(C - O), (H - L) * 0.01)
        ax.bar(x, govde, bottom=np.minimum(O, C), width=0.7, color=renk, edgecolor=renk, linewidth=0.5, zorder=4)
        sol = max(0, int(G["sol"])); son = int(G["son"])
        x0 = x[sol] - 0.5; x1 = x[son - 1] + 0.5
        ust = G["ust"] if np.isfinite(G["ust"]) else G["tavan"]
        ax.add_patch(Rectangle((x0, G["hat"]), x1 - x0, max(ust - G["hat"], 0.0), facecolor="#4575b4", alpha=0.15, edgecolor="#4575b4",
                               linewidth=0.8, zorder=1, label="S6 bölgesi"))
        ax.hlines(G["tavan"], x0, x[son] + 0.5, colors="#f46d43", linestyles="--", linewidth=1.2, zorder=5, label="tavan")
        ax.hlines(G["hat"], x0, x[son] + 0.5, colors="#313695", linestyles="-", linewidth=1.2, zorder=5, label="hat")
        ax.set_title(f"No {int(no)}", fontsize=14)
        ax.legend(loc="upper left", fontsize=9, frameon=False)
        ax.grid(alpha=0.25, zorder=0)
        ax.set_ylabel("fiyat")
        plt.setp(ax.get_xticklabels(), visible=False)
        av.bar(x, V, width=0.7, color=renk, alpha=0.7)
        av.set_ylabel("hacim"); av.set_xlabel("bar (0 = sinyal günü t)")
        av.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        av.grid(alpha=0.25)
        ax.set_xlim(x[0] - 1, x[-1] + 3)
        os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
        fig.savefig(yol, dpi=dpi, metadata={"Software": None})
    finally:
        plt.close(fig)
    return yol


def ge_gorsel(cikti: Optional[str] = None, png: Optional[str] = None, veri: Optional[str] = None, E: Dict[str, Any] = GE_ESIK) -> Dict[str, Any]:
    """anahtar.json -> No_k.png; hat / tavan kesik veriden yeniden üretilir ve olay dosyasıyla aynı olmalı."""
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    S = ge_anahtar_oku(cikti); png = png or GE_YOL["png"]
    if os.path.abspath(png).startswith(os.path.abspath(KOK_GE) + os.sep):
        raise GEHata(f"PNG klasörü repo içinde olamaz: {png}")
    X = ge_olay_oku(["pazar", "sembol", "tarih", "hat", "tavan"]).set_index(["pazar", "sembol", "tarih"])
    say = {"png": 0, "klasor": png}
    for p in OC.OC_ESIK["pazar"]:
        Sp = S[S.pazar == p]
        if not len(Sp):
            continue
        Vd = OC.oc_veri(p, klasor=veri or GE_YOL["veri"])
        for r in Sp.itertuples():
            if r.sembol not in Vd["V"]:
                raise GEHata(f"No {r.no}: sembol veride yok")
            G = ge_gorsel_veri(Vd["V"][r.sembol], r.tarih, E=E)
            h0, tv0 = (float(v) for v in X.loc[(p, r.sembol, r.tarih), ["hat", "tavan"]])
            tol = E["denetim"]["hat_tol"]
            if abs(G["hat"] / h0 - 1) > tol or abs(G["tavan"] / tv0 - 1) > tol:
                raise GEHata(f"No {r.no}: kesik veride hat / tavan olay dosyasıyla tutmadı")
            if G["W"].index[-1] != pd.Timestamp(r.tarih):
                raise GEHata(f"No {r.no}: görselin son barı t değil")
            ge_ciz(G, int(r.no), os.path.join(png, f"No_{int(r.no)}.png"), E)
            say["png"] += 1
        gelog.info("görsel %s: %d (%.0f sn)", p, len(Sp), time.time() - t0)
        del Vd
    say["sure_sn"] = round(time.time() - t0, 1)
    return say


# ================================================================ 4) ÖN KAYIT
def ge_kontrol_tablosu(tablo: Optional[Dict[str, Tuple[str, str]]] = None) -> str:
    import IZ_KARNE as IK
    tablo = GE_KONTROL if tablo is None else tablo
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = tablo.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def ge_is_tanimi_bolum(no: str, yol: Optional[str] = None) -> str:
    """İş tanımından '## <no>.' bölümünü AYNEN döndürür (bir sonraki '## ' başlığına kadar)."""
    yol = yol or GE_YOL["is_tanimi"]
    metin = open(yol, encoding="utf-8").read()
    m = re.search(rf"^## {re.escape(no)}\..*?(?=^## |\Z)", metin, flags=re.M | re.S)
    if not m:
        raise GEHata(f"iş tanımında §{no} yok")
    return m.group(0).rstrip()


def _ge_git(yol: str) -> Dict[str, str]:
    try:
        return OC._oc_git_islenmis(yol)
    except OC.OCHata as ex:
        raise GEHata(str(ex))


def ge_onkayit_metni(cikti: Optional[str] = None, png: Optional[str] = None, git: bool = True) -> str:
    cikti = cikti or GE_YOL["cikti"]; png = png or GE_YOL["png"]
    S = ge_anahtar_oku(cikti)
    oz = _ge_yol("ozellik", cikti)
    if not os.path.exists(oz):
        raise GEHata("ozellik_Y1.csv.gz yok (önce `python GOZ_ETIKET.py ozellik`)")
    den = json.load(open(_ge_yol("ozellik_denetim", cikti), encoding="utf-8"))
    pngler = sorted(f for f in os.listdir(png) if re.fullmatch(r"No_\d+\.png", f)) if os.path.isdir(png) else []
    if len(pngler) != len(S):
        raise GEHata(f"PNG sayısı {len(pngler)} != örneklem {len(S)} ({png})")
    git_bilgi = {}
    if git:
        for ad, y in (("kod", GE_YOL["kod"]), ("anahtar", _ge_yol("anahtar", cikti)), ("ozellik", oz), ("is_tanimi", GE_YOL["is_tanimi"])):
            git_bilgi[ad] = _ge_git(y)
    dag = S.groupby(["pazar", "donem"]).size()
    sym = S.groupby(["pazar", "sembol"]).size()
    Ft = pd.read_csv(oz)
    Fk = [f"F{k}" for k in range(1, 19)]
    sat = ["# GOZ_ETIKET — ÖN KAYIT (AŞAMA A; etiketlemeden ve ölçümden ÖNCE)", "", GE_SURUM, "",
           f"- GE_ESIK_SHA: `{ge_esik_sha()}`",
           f"- GE_KOD_SHA: `{_ge_sha_dosya(GE_YOL['kod'])}` (GOZ_ETIKET.py)",
           f"- YH_KOD_SHA: `{_ge_sha_dosya(GE_YOL['yh_kod'])}` (YAPI_HEDEF.py)",
           f"- S6_KOD_SHA: `{_ge_sha_dosya(GE_YOL['s6_kod'])}` (S6_TABAN.py)",
           f"- OC_KOD_SHA: `{_ge_sha_dosya(GE_YOL['oc_kod'])}` (ORTAK_CETVEL.py)",
           f"- OLAY_Y1_SHA: `{_ge_sha_dosya(GE_YOL['olay'])}` (arastirma_cikti/yapi_hedef/olay_Y1.csv.gz)",
           f"- ANAHTAR_SHA: `{_ge_sha_dosya(_ge_yol('anahtar', cikti))}` (anahtar.json; GİZLİ, etiketleyen açmaz)",
           f"- OZELLIK_SHA: `{_ge_sha_dosya(oz)}` (ozellik_Y1.csv.gz)",
           f"- IS_TANIMI_SHA: `{_ge_sha_dosya(GE_YOL['is_tanimi'])}` (GOZ_ETIKET_IS_TANIMI.md)"]
    for ad, g in git_bilgi.items():
        sat.append(f"- GIT_{ad.upper()}: {g['commit'][:10]}, {g['commit_zamani']}")
    sat += [f"- ZAMAN (UTC): `{_ge_simdi()}`", "",
            "Bu dosya AŞAMA B (etiketleme) ve AŞAMA C (ölçüm / eğitim) başlamadan ÖNCE yazıldı. AŞAMA A hiçbir sonuç sütununu (h5, h10, st5, eş, "
            "plasebo, getiri, olc ...) okumadı: olay_Y1.csv.gz yalnız kimlik (deneme, pazar, sembol, tarih, giris, donem) ve t'de bilinen sinyal "
            "(hat, tavan, ek) sütunlarıyla, usecols ile okundu (GOZ_ETIKET.ge_olay_oku izin listesi; test_goz_etiket). Eşikler sonuç görüldükten "
            "sonra değişmez; zorunlu sapma SAPMA-n diye bu dosyaya, ölçümden önce yazılır.", "",
            "## 1. Örneklem (tohum 11; yalnız kimlik sütunları)", "", GE_ESIK["orneklem"]["tanim"], "",
            "| Pazar | Dönem | Kota | Seçilen |", "|---|---|---|---|"]
    for pz, dn, kota in GE_ESIK["orneklem"]["katman"]:
        sat.append(f"| {pz} | {dn} | {kota} | {int(dag.get((pz, dn), 0))} |")
    sat += [f"| Toplam | | {sum(k[2] for k in GE_ESIK['orneklem']['katman'])} | {len(S)} |", "",
            f"- Ayrı hisse: {len(sym)}; aynı hisseden 2 olay: {int((sym == 2).sum())}; en çok {int(sym.max())} (sınır 2).",
            "- Numara sırası karıştırılmış (pazar / dönem / tarih bilgisi taşımaz). Sembol ve tarihler yalnız anahtar.json'da.", "",
            "## 2. Kör görsel", "", GE_ESIK["gorsel"]["tanim"], "",
            f"- PNG sayısı: {len(pngler)} (repo DIŞI klasör: {png}). Her PNG'de hat / tavan kesik veriden yeniden üretildi ve olay dosyasıyla aynı.",
            "", "## 3. Sayısal özellikler F1-F18 (bütün Y1 olayları; yalnız t'ye kadar)", "", GE_ESIK["ozellik"]["bolge"], ""]
    for k, v in GE_ESIK["ozellik"]["F"].items():
        sat.append(f"- {k}: {v}")
    sat += ["", f"- Dosya: ozellik_Y1.csv.gz, {len(Ft)} satır x (pazar, sembol, tarih, durum, F1-F18).",
            "- Denetim: " + "; ".join(f"{p}: olay {v['olay']}, hat / tavan eşit {v['hat_tavan_esit']}, prefix denetimi {v['prefix_denetimi']} olay tuttu"
                                      for p, v in den["pazar"].items()) + ".",
            "- NaN sayısı (F3 ATR geçmişi < 120 bar, F14 250 bar yok, F17 60 bar yok): "
            + ", ".join(f"{f} {int(Ft[f].isna().sum())}" for f in Fk if Ft[f].isna().sum()) + ".", "",
            "## 4. AŞAMA B kuralları (etiketleyen; iş tanımı §4)", "",
            "- Etiketleyen yalnız PNG klasörünü ve iş tanımı §4'ü okur; anahtar.json, olay_Y1.csv.gz, ozellik_Y1.csv.gz, YAPI_HEDEF çıktıları AÇILMAZ.",
            "- Çıktı arastirma_cikti/goz_etiket/etiket.json; 300 PNG'nin hepsi; 'sonrası' tahmini yazılmaz.", "",
            "## 5. ÖLÇÜM PLANI ve EŞİKLER (iş tanımı §5, AYNEN)", "", ge_is_tanimi_bolum("5"), "",
            "## 6. Yorumlar (iş tanımında açık bırakılan noktalar; ölçümden önce sabit)", "",
            "- Örneklem uygunluğu: giriş <= kriz - 30 gün (2026-08-01) yalnız tarih kuralıdır; olay_Y1 'olc' (ölçülebilir) sütunu OKUNMADI. "
            "Örneklemde ölçülemeyen (olc = False) olay kalırsa AŞAMA C onu ölçüden çıkarır ve sayısını yazar (etiket yine kalır).",
            "- AŞAMA C KAT5 için 'h5' ve 'es_h5' olay_Y1 sütunlarıdır (kapanışla +%5 stop'tan önce, 15 bar; eş = aynı gün aynı OC kovası, aynı d); "
            "P(stop önce) = 'st5' / 'es_st5'; 'getiri' = takip stoplu getiri (bilgi).",
            "- Göz skoru eğitimi: BELİRSİZ dışarı; F1-F18 NaN değerleri eğitim örnekleminin medyanıyla doldurulur ve standartlaştırılır (yalnız "
            "eğitim verisinden; dış örnekleme aynı dönüşüm); beşte bir sınırları skorun bütün 26.663 olaydaki dağılımından; eğitimde kullanılan "
            "300 olay dış örneklem satırında ayrıca çıkarılarak raporlanır.", "",
            ge_kontrol_tablosu(), ""]
    return "\n".join(sat)


def ge_onkayit_yaz(cikti: Optional[str] = None, png: Optional[str] = None, git: bool = True, uzerine: bool = False) -> str:
    cikti = cikti or GE_YOL["cikti"]; yol = _ge_yol("onkayit", cikti)
    if os.path.exists(yol) and not uzerine:
        raise GEHata(f"ön kayıt var ({yol}); git'e işlenmemişse --uzerine-yaz")
    if os.path.exists(os.path.join(cikti, "etiket.json")):
        raise GEHata("etiket.json var: ön kayıt etiketlemeden sonra yazılamaz")
    metin = ge_onkayit_metni(cikti, png, git)
    _ge_yaz(yol, metin, "ön kayıt")
    import IZ_KARNE as IK
    k = IK.ik_kontrol_kapisi(yol)
    gelog.info("ön kayıt: %s (kontrol kapısı %s, %d madde)", yol, "GEÇTİ" if k["gecti"] else "KAPALI", k["n"])
    return yol


def ge_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    """AŞAMA B / C başında: ön kayıt git'e işlenmiş, kontrol kapısı açık, mühürler (eşik, kod, anahtar, özellik) tutuyor."""
    cikti = cikti or GE_YOL["cikti"]; yol = _ge_yol("onkayit", cikti)
    g = _ge_git(yol)
    import IZ_KARNE as IK
    IK.ik_kontrol_kapisi(yol)
    metin = open(yol, encoding="utf-8").read()
    bek = {"GE_ESIK_SHA": ge_esik_sha(), "GE_KOD_SHA": _ge_sha_dosya(GE_YOL["kod"]), "ANAHTAR_SHA": _ge_sha_dosya(_ge_yol("anahtar", cikti)),
           "OZELLIK_SHA": _ge_sha_dosya(_ge_yol("ozellik", cikti)), "OLAY_Y1_SHA": _ge_sha_dosya(GE_YOL["olay"])}
    for ad, v in bek.items():
        m = re.search(rf"{ad}:\s*`([0-9a-f]{{64}})`", metin)
        if not m or m.group(1) != v:
            raise GEHata(f"kapı: {ad} tutmuyor (ön kayıttan sonra değişmiş)")
    return {"onkayit": g, "gecti": True}


# ================================================================ 5) AŞAMA C — ÖLÇÜM, EĞİTİM, HAKEM (iş tanımı §5 + SAPMA-1)
# GE_ESIK (AŞAMA A mührü) DEĞİŞMEZ; AŞAMA C sabitleri ayrı sözlük GE_C_ESIK'tedir (sha'sı ON_KAYIT.md SAPMA-1'de, ölçümden önce).
GE_C_DOSYA = {"etiket": "etiket.json", "satir": "etiket_olcu.csv.gz", "skor": "goz_skor_Y1.csv.gz", "sonuc": "sonuc_C.json", "rapor": "RAPOR.md",
              "hakem_pdf": "GOZ_HAKEM_SET.pdf", "hakem_anahtar": "hakem_anahtar.json", "hakem_sablon": "hakem_cevap_sablon.csv",
              "hakem_sonuc": "HAKEM_SONUC.md", "guc": os.path.join(KOK_GE, "arastirma_cikti", "yapi_hedef", "guc_tablosu.json")}
GE_KARARLAR = ("OLUR", "BELİRSİZ", "OLMAZ")
GE_F = [f"F{k}" for k in range(1, 19)]
GE_C_ESIK: Dict[str, Any] = {
    "surum": "C1.0",
    "olcu1": {"n_esik": 30, "fisher_p": 0.05, "fisher": "iki yönlü (scipy fisher_exact), yön ayrıca şart",
              "tanim": "OLUR vs OLMAZ: +%5 payı (h5) Fisher; KAT5 = Σ h5 / Σ es_h5 (ay kümeli bootstrap %95, YAPI_HEDEF.yh_kat = OC.oc_kat); "
                       "P(stop önce) st5 / es_st5. TUTAR = OLUR KAT5 alt uç > 1 VE OLUR h5 payı > OLMAZ h5 payı (Fisher p < 0,05) VE OLUR st5 "
                       "< OLUR es_st5. n OLUR < 30 -> ÖLÇÜLEMEDİ"},
    "olcu1b": {"n_esik": 30, "fisher_p": 0.05,
               "tanim": "SAPMA-1: OLMAZ-DEĞİL (OLUR + BELİRSİZ) vs OLMAZ: aynı ölçüler; TUTAR = OLMAZ-DEĞİL KAT5 alt uç > 1 VE OLMAZ-DEĞİL h5 "
                        "payı > OLMAZ h5 payı (Fisher iki yönlü p < 0,05) VE OLMAZ-DEĞİL st5 < OLMAZ-DEĞİL es_st5; OLMAZ-DEĞİL n < 30 -> ÖLÇÜLEMEDİ"},
    "olcu_satir": "ölçüye giren olay = h5 ve es_h5 sonlu (olay_Y1 'olc'); dışarıda kalan sayısı yazılır, etiketi kalır",
    "neden": {"bh_q": 0.10, "tanim": "her neden kodu (C1..C13, + / - ayrı) için var / yok: h5 payı, Fisher iki yönlü p, KAT5 (var grubu, ay kümeli %95); "
                                    "BH q 0,10 Fisher p'leri üzerinde (bilgi; karar değil); var n < 30 olan kod 'n az' notu"},
    "egitim": {"C": 1.0, "ceza": "l2", "kat": 5, "tohum": 13, "max_iter": 5000, "perm": 200, "perm_tohum": 1301,
               "tanim": "SAPMA-1 hedefi: OLMAZ-DEĞİL (1) vs OLMAZ (0), 300 etiket; F1-F18; boru hattı = medyan doldurma + standartlaştırma + "
                        "lojistik (L2, C = 1); bütün dönüşümler YALNIZ eğitim katından öğrenilir (CV sızıntısı yok); StratifiedKFold(5, karıştır, "
                        "tohum 13): kat AUC ortalaması ve kat dışı (OOF) havuz AUC; etiket permütasyonu 200 (tohum 1301) ile OOF AUC p (bilgi). "
                        "Son model 300 olayın tamamıyla kurulur; katsayılar standart birimde. Bilgi: §5 asıl hedef OLUR (1) / OLMAZ (0) "
                        "(BELİRSİZ dışarı) aynı boru hattıyla CV AUC (OLUR n 6 -> ÖLÇÜLEMEDİ)"},
    "skor": {"besli": 5, "tanim": "GÖZ SKORU = son modelin olasılığı, 26.663 Y1 olayının hepsine; beşte bir sınırları skorun 26.663 olaydaki "
                                  "dağılımından (np.quantile 0,2/0,4/0,6/0,8); B5 = üst, B1 = alt",
             "hucre": "karar hücreleri ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26 (bilgi BIST, 2016-22): B5 olayları YAPI_HEDEF.yh_hucre + "
                      "yh_durum (güç tablosu yapi_hedef/guc_tablosu.json, yön +) + yh_etiket; B1 aynı (bilgi); B5 vs B1 h5 Fisher (bilgi). "
                      "Ana satır = bütün olaylar (ön kayıt §6); 'dış' satır = 300 etiketli olay çıkarılmış; ikisinin etiketi farklıysa "
                      "muhafazakâr olan (İZ > EMARE > DESTEKLENMEDİ / ÖLÇÜLEMEDİ sırasında düşük olan) yazılır"},
    "hakem": {"tohum": 13, "yari": {"OLUR": 3, "BELİRSİZ": 7, "OLMAZ": 10}, "sayfa": 40,
              "tanim": "tohum 13: her karar grubu no sırasıyla dizilir, rng.permutation; OLUR 6'sının ilk 3'ü kör, son 3'ü açık; BELİRSİZ ilk 7 kör, "
                       "sonraki 7 açık; OLMAZ ilk 10 kör, sonraki 10 açık; her yarı ayrı rng.permutation ile sıralanır. Sayfa 1-20 KÖR (yalnız "
                       "grafik + 'Cemal: OLUR / OLMAZ / BELİRSİZ + neden'), 21-40 AÇIK (grafik + aşama B kararı + neden kodlarının açılımı + not + "
                       "'Cemal: DOĞRU / YANLIŞ + neden'). Grafik = AŞAMA A kör PNG (t sonrası yok, hisse adı yok)"},
    "dev_fitil": {"oran": 1.5, "tanim": "bilgi: geçerli barda High / max(O, C) > 1,5 ya da min(O, C) / Low > 1,5 = şüpheli dev fitil (veri hatası adayı)"},
}

GE_NEDEN_ACILIM: Dict[str, str] = {
    "C1": "taban net (hat >= 3 dokunuş, aynı seviye, eğim aşağı değil)",
    "C2": "dip savunulmuş (dipler kırılmamış, alçalan dip yok)",
    "C3": "mumlar küçük (fitiller dahil, öncesine göre)",
    "C4": "mum şekli (alt fitil kısa, açılış dibe yakın)",
    "C5": "kırılım mumu belirgin (kapanış tavanı net aşmış, gövdeli)",
    "C6": "büyük desen (120-250 bar yükselen / yatay; alçalan kanal değil)",
    "C7": "yapı boyu (düşüşe göre yeterli)",
    "C8": "kağıt hafızası (önceki benzer yapılar)",
    "C9": "kubbe / çanak (sağ kenar dönmüş)",
    "C10": "yol almış (fiyat tabandan çoktan uzaklaşmış)",
    "C11": "stop uzaklığı (kapanış hattan %10 içinde)",
    "C12": "çekiştirme / oluşum yok (yapı yok)",
    "C13": "dev mum / şüphe (geçmişte dev tek mum)",
}


def ge_neden_acilim(kod: str) -> str:
    """'C5-' -> 'C5- kırılım mumu belirgin ...: UYMUYOR'. + = kural lehte / uyuyor, - = kural aleyhte / uymuyor."""
    m = re.fullmatch(r"(C\d+)([+-])", str(kod).strip())
    if not m or m.group(1) not in GE_NEDEN_ACILIM:
        return str(kod)
    return f"{kod} {GE_NEDEN_ACILIM[m.group(1)]}: {'UYUYOR (lehte)' if m.group(2) == '+' else 'UYMUYOR (aleyhte)'}"


def ge_c_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    s = json.dumps(GE_C_ESIK if E is None else E, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def ge_etiket_oku(cikti: Optional[str] = None) -> pd.DataFrame:
    """etiket.json -> DataFrame[no, karar, nedenler, guven, not]. Okur, DEĞİŞTİRMEZ."""
    yol = os.path.join(cikti or GE_YOL["cikti"], GE_C_DOSYA["etiket"])
    if not os.path.exists(yol):
        raise GEHata(f"etiket yok: {yol}")
    J = json.load(open(yol, encoding="utf-8"))
    E = J.get("etiket", J)
    sat = []
    for k, v in E.items():
        if v.get("karar") not in GE_KARARLAR:
            raise GEHata(f"etiket No {k}: karar geçersiz ({v.get('karar')})")
        ned = [str(x).strip() for x in v.get("nedenler", [])]
        bad = [x for x in ned if not re.fullmatch(r"C(1[0-3]|[1-9])[+-]", x)]
        if bad:
            raise GEHata(f"etiket No {k}: neden kodu geçersiz {bad}")
        sat.append({"no": int(k), "karar": v["karar"], "nedenler": ned, "guven": v.get("guven"), "not": v.get("not", "")})
    T = pd.DataFrame(sat).sort_values("no").reset_index(drop=True)
    if T.no.duplicated().any():
        raise GEHata("etiket: no tekil değil")
    return T


def ge_birlestir(S: pd.DataFrame, T: pd.DataFrame, X: pd.DataFrame, F: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """anahtar (S: no, pazar, sembol, tarih) x etiket (T: no, karar, nedenler) x olay sonucu (X: olay_Y1 tüm sütunlar) [x özellik F].
    Bire bir eşleşme zorunlu: eksik / fazla / çift satır DURUR."""
    if set(S.no) != set(T.no):
        raise GEHata(f"anahtar / etiket numaraları farklı (anahtar {len(S)}, etiket {len(T)})")
    K = ["pazar", "sembol", "tarih"]
    S = S.copy(); X = X.copy()
    for D in (S, X):
        D["tarih"] = pd.to_datetime(D["tarih"]); D["sembol"] = D["sembol"].astype(str)
    if X.duplicated(K).any():
        raise GEHata("olay dosyasında (pazar, sembol, tarih) tekil değil")
    M = S.drop(columns=[c for c in ("giris", "donem") if c in S]).merge(T, on="no", how="inner", validate="1:1")
    M = M.merge(X, on=K, how="left", validate="1:1", indicator=True)
    if (M["_merge"] != "both").any():
        raise GEHata(f"{int((M['_merge'] != 'both').sum())} etiketli olay olay dosyasında yok")
    M = M.drop(columns="_merge")
    if F is not None:
        F = F.copy(); F["tarih"] = pd.to_datetime(F["tarih"]); F["sembol"] = F["sembol"].astype(str)
        M = M.merge(F[K + GE_F], on=K, how="left", validate="1:1", indicator=True)
        if (M["_merge"] != "both").any():
            raise GEHata("etiketli olayın özellik satırı yok")
        M = M.drop(columns="_merge")
    if len(M) != len(T):
        raise GEHata(f"birleştirme satır sayısı {len(M)} != {len(T)}")
    return M.sort_values("no").reset_index(drop=True)


def _ge_ay(X: pd.DataFrame) -> np.ndarray:
    return pd.to_datetime(X.giris).dt.to_period("M").astype(str).to_numpy() if len(X) else np.array([], dtype=object)


def ge_olculur(X: pd.DataFrame) -> pd.DataFrame:
    return X[np.isfinite(X.h5.astype(float)) & np.isfinite(X.es_h5.astype(float))]


def ge_grup(X: pd.DataFrame) -> Dict[str, Any]:
    """Bir grubun ölçüsü: n, h5 / es_h5 payı, KAT5 (ay kümeli %95; YH.yh_kat), h10 / KAT10, st5 / es_st5, getiri (bilgi)."""
    g = ge_olculur(X).sort_values("giris"); ay = _ge_ay(g)
    out: Dict[str, Any] = {"n": int(len(g)), "n_ham": int(len(X)), "ay": int(len(np.unique(ay)))}
    for k in ("h5", "h10", "st5"):
        r = YH.yh_kat(g[k].to_numpy(float), g["es_" + k].to_numpy(float), ay)
        out.update({f"{k}_{a}": v for a, v in r.items() if a != "n"})
    gt = g.getiri.to_numpy(float); gt = gt[np.isfinite(gt)]
    out["getiri_ort"] = float(gt.mean()) if len(gt) else np.nan
    out["getiri_med"] = float(np.median(gt)) if len(gt) else np.nan
    return out


def ge_fisher(a: pd.DataFrame, b: pd.DataFrame, k: str = "h5") -> float:
    from scipy.stats import fisher_exact
    a = ge_olculur(a); b = ge_olculur(b)
    if not len(a) or not len(b):
        return np.nan
    ah, bh = int(a[k].sum()), int(b[k].sum())
    return float(fisher_exact([[ah, len(a) - ah], [bh, len(b) - bh]], alternative="two-sided")[1])


def ge_iki_grup(A: pd.DataFrame, B: pd.DataFrame, ad_a: str, ad_b: str, kural: Dict[str, Any]) -> Dict[str, Any]:
    """Ölçü 1 / 1b: A (aday) vs B (OLMAZ). TUTAR kuralı GE_C_ESIK'teki gibi; n A < n_esik -> ÖLÇÜLEMEDİ."""
    ga, gb = ge_grup(A), ge_grup(B); p = ge_fisher(A, B)
    s_kat = bool(np.isfinite(ga.get("h5_alt", np.nan)) and ga["h5_alt"] > 1)
    s_pay = bool(np.isfinite(p) and p < kural["fisher_p"] and ga["h5_p_olay"] > gb["h5_p_olay"])
    s_stop = bool(np.isfinite(ga.get("st5_p_olay", np.nan)) and ga["st5_p_olay"] < ga["st5_p_ref"])
    if ga["n"] < kural["n_esik"]:
        durum = "ÖLÇÜLEMEDİ"
    else:
        durum = "TUTAR" if (s_kat and s_pay and s_stop) else "TUTMADI"
    return {"a": ad_a, "b": ad_b, ad_a: ga, ad_b: gb, "fisher_p": p, "s_kat": s_kat, "s_pay": s_pay, "s_stop": s_stop, "durum": durum}


def _ge_bh(p: List[float], q: float) -> List[bool]:
    return YH._yh_bh(p, q)


def ge_neden_olcu(M: pd.DataFrame, E: Dict[str, Any] = GE_C_ESIK) -> List[Dict[str, Any]]:
    """Ölçü 2: her neden kodu var / yok (bilgi; BH q 0,10)."""
    kodlar = sorted({k for ned in M.nedenler for k in ned}, key=lambda s: (int(re.sub(r"\D", "", s)), s[-1]))
    R = []
    for k in kodlar:
        var = M.nedenler.apply(lambda n, k=k: k in n)
        gv, gy = ge_grup(M[var]), ge_grup(M[~var])
        R.append({"kod": k, "acilim": ge_neden_acilim(k), "n_var": gv["n"], "n_yok": gy["n"], "h5_var": gv.get("h5_p_olay"),
                  "h5_yok": gy.get("h5_p_olay"), "es_h5_var": gv.get("h5_p_ref"), "kat5_var": gv.get("h5_kat"), "kat5_alt": gv.get("h5_alt"),
                  "kat5_ust": gv.get("h5_ust"), "st5_var": gv.get("st5_p_olay"), "st5_yok": gy.get("st5_p_olay"),
                  "p": ge_fisher(M[var], M[~var]), "n_az": bool(gv["n"] < 30)})
    bh = _ge_bh([r["p"] for r in R], E["neden"]["bh_q"])
    for r, b in zip(R, bh):
        r["bh"] = bool(b)
    return R


def ge_boru(E: Dict[str, Any] = GE_C_ESIK):
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    G = E["egitim"]
    return Pipeline([("doldur", SimpleImputer(strategy="median")), ("olcek", StandardScaler()),
                     ("lr", LogisticRegression(C=float(G["C"]), max_iter=int(G["max_iter"]), solver="lbfgs"))])   # varsayılan ceza L2 (GE_C_ESIK "ceza")


def _ge_Fmat(D: pd.DataFrame) -> np.ndarray:
    A = np.array(D[GE_F].to_numpy(float), dtype=float, copy=True)
    A[~np.isfinite(A)] = np.nan
    return A


def ge_cv(A: np.ndarray, y: np.ndarray, E: Dict[str, Any] = GE_C_ESIK, perm: bool = True) -> Dict[str, Any]:
    """5 katlı tabakalı CV; her katta boru hattı (doldurma + ölçek + lojistik) YALNIZ eğitim katından öğrenilir. OOF olasılıklar döner."""
    from sklearn.base import clone
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedKFold
    G = E["egitim"]; y = np.asarray(y, int)
    if y.sum() < G["kat"] or (len(y) - y.sum()) < G["kat"]:
        return {"auc_oof": np.nan, "auc_kat": [], "n1": int(y.sum()), "n0": int(len(y) - y.sum()), "not": "sınıf < kat sayısı"}
    skf = StratifiedKFold(n_splits=int(G["kat"]), shuffle=True, random_state=int(G["tohum"]))
    oof = np.full(len(y), np.nan); aucs = []; katlar = []
    for tr, te in skf.split(A, y):
        m = clone(ge_boru(E)).fit(A[tr], y[tr])
        oof[te] = m.predict_proba(A[te])[:, 1]
        aucs.append(float(roc_auc_score(y[te], oof[te])) if 0 < y[te].sum() < len(te) else np.nan)
        katlar.append({"tr": tr, "te": te, "doldur": m.named_steps["doldur"].statistics_.copy(), "ort": m.named_steps["olcek"].mean_.copy()})
    out = {"auc_oof": float(roc_auc_score(y, oof)), "auc_kat": aucs, "auc_kat_ort": float(np.nanmean(aucs)),
           "auc_kat_sd": float(np.nanstd(aucs)), "n1": int(y.sum()), "n0": int(len(y) - y.sum()), "oof": oof, "katlar": katlar}
    if perm:
        rng = np.random.default_rng(int(G["perm_tohum"])); v = []
        for _ in range(int(G["perm"])):
            yp = rng.permutation(y); oo = np.full(len(y), np.nan)
            for tr, te in skf.split(A, yp):
                oo[te] = clone(ge_boru(E)).fit(A[tr], yp[tr]).predict_proba(A[te])[:, 1]
            v.append(roc_auc_score(yp, oo))
        v = np.array(v); out["perm_p"] = float((1 + (v >= out["auc_oof"]).sum()) / (1 + len(v))); out["perm_ort"] = float(v.mean())
        out["perm_95"] = float(np.quantile(v, 0.95))
    return out


def ge_egitim(M: pd.DataFrame, E: Dict[str, Any] = GE_C_ESIK) -> Dict[str, Any]:
    """SAPMA-1 hedefi (OLMAZ-DEĞİL 1 / OLMAZ 0) CV + son model; bilgi: asıl hedef OLUR / OLMAZ CV; tek özellik AUC (bilgi)."""
    from sklearn.metrics import roc_auc_score
    A = _ge_Fmat(M); y = (M.karar != "OLMAZ").to_numpy(int)
    cv = ge_cv(A, y, E)
    son = ge_boru(E).fit(A, y)
    kat = son.named_steps["lr"].coef_[0]
    katsayi = sorted([{"F": f, "tanim": GE_ESIK["ozellik"]["F"][f].split(":")[0], "kat": float(c)} for f, c in zip(GE_F, kat)],
                     key=lambda r: -abs(r["kat"]))
    tek = []
    for j, f in enumerate(GE_F):
        a = A[:, j]; g = np.isfinite(a)
        tek.append({"F": f, "auc": float(roc_auc_score(y[g], a[g])) if 0 < y[g].sum() < g.sum() else np.nan, "nan": int((~g).sum())})
    ma = M.karar.isin(["OLUR", "OLMAZ"]).to_numpy()
    cv0 = ge_cv(A[ma], (M.karar[ma] == "OLUR").to_numpy(int), E, perm=False)
    return {"cv": {k: v for k, v in cv.items() if k not in ("oof", "katlar")}, "oof": cv["oof"], "model": son, "katsayi": katsayi,
            "sabit": float(son.named_steps["lr"].intercept_[0]), "tek": tek,
            "asil": {k: v for k, v in cv0.items() if k not in ("oof", "katlar")}}


def ge_skor(model, F: pd.DataFrame) -> np.ndarray:
    return model.predict_proba(_ge_Fmat(F))[:, 1]


def ge_besli(skor: np.ndarray, E: Dict[str, Any] = GE_C_ESIK) -> Tuple[np.ndarray, np.ndarray]:
    k = int(E["skor"]["besli"]); sin = np.quantile(skor, np.arange(1, k) / k)
    return np.searchsorted(sin, skor, side="right") + 1, sin


_GE_SIRA = {"İZ": 4, "İZ + BIST": 4, "EMARE": 3, "DESTEKLENMEDİ": 1, "ÖLÇÜLEMEDİ": 1}


def ge_skor_hucre(O: pd.DataFrame, guc: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """O: olay_Y1 + besli. Her (pazar, dönem): B5 -> YH.yh_hucre + yh_durum; B1 bilgi; B5 vs B1 h5 Fisher. Etiket YH.yh_etiket."""
    H_, dur = [], {}
    for p in OC.OC_ESIK["pazar"]:
        for q, _a, _b in OC.OC_ESIK["donem"]:
            x = O[(O.pazar == p) & (O.donem == q)]
            ust, alt = x[x.besli == 5], x[x.besli == 1]
            h = YH.yh_hucre(ust); ha = YH.yh_hucre(alt)
            durum, g = YH.yh_durum(h, 1, guc)
            dur[(p, q)] = durum
            H_.append({"pazar": p, "donem": q, "karar_hucre": [p, q] in YH.YH_ESIK["karar"]["hucre_karar"], "n_hucre": int(len(x)),
                       "ust": {k: v for k, v in h.items() if k != "cikis_tur"}, "alt": {k: v for k, v in ha.items() if k != "cikis_tur"},
                       "fisher_ust_alt": ge_fisher(ust, alt), "guc": g, "durum": durum})
    return {"hucre": H_, "etiket": YH.yh_etiket(dur)}


def ge_olasilik(O: pd.DataFrame, maske: np.ndarray) -> List[Dict[str, Any]]:
    """Beşli başına (B1..B5) olasılık tablosu: +%5 / +%10 / stop payı, eş payı, KAT (ay kümeli %95), getiri (bilgi)."""
    R = []
    for b in range(1, 6):
        g = ge_grup(O[maske & (O.besli == b).to_numpy()])
        R.append({"besli": b, **g})
    return R


def ge_dev_fitil(S: pd.DataFrame, T: pd.DataFrame, veri: Optional[str] = None, E: Dict[str, Any] = GE_C_ESIK) -> Dict[str, Any]:
    """Bilgi (veri denetimi): 300 kör görselin 120 bar penceresinde (t dahil, t sonrası yok) şüpheli dev fitil; C13- ile kesişim."""
    r_ = float(E["dev_fitil"]["oran"]); sat = []
    for p in OC.OC_ESIK["pazar"]:
        Sp = S[S.pazar == p]
        if not len(Sp):
            continue
        Vd = OC.oc_veri(p, klasor=veri or GE_YOL["veri"])
        for r in Sp.itertuples():
            d = ge_hazir(Vd["V"][r.sembol]); dk = d[d.index <= pd.Timestamp(r.tarih)].iloc[-int(GE_ESIK["gorsel"]["bar"]):]
            up = dk.High / np.maximum(dk.Open, dk.Close); dn = np.minimum(dk.Open, dk.Close) / dk.Low
            m = (up > r_) | (dn > r_)
            sat.append({"no": int(r.no), "pazar": p, "dev": bool(m.any()), "en_buyuk": float(max(up.max(), dn.max())),
                        "bar": int(np.flatnonzero(m.to_numpy())[0] - (len(dk) - 1)) if m.any() else None})
        del Vd
    D = pd.DataFrame(sat).merge(T[["no", "nedenler", "karar"]], on="no")
    D["c13"] = D.nedenler.apply(lambda n: "C13-" in n)
    return {"n_dev": int(D.dev.sum()), "dev_no": D[D.dev].sort_values("no")[["no", "pazar", "en_buyuk", "bar", "karar"]].to_dict("records"),
            "dev_ve_c13": int((D.dev & D.c13).sum()), "c13": int(D.c13.sum()), "c13_dev_yok": int((D.c13 & ~D.dev).sum())}


def ge_no274(veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    """No 274 dev fitil ham veri denetimi (yalnız t'ye kadar)."""
    S = ge_anahtar_oku(cikti); r = S[S.no == 274].iloc[0]
    Vd = OC.oc_veri(r.pazar, klasor=veri or GE_YOL["veri"]); d = ge_hazir(Vd["V"][r.sembol])
    dk = d[d.index <= r.tarih].iloc[-int(GE_ESIK["gorsel"]["bar"]):]
    boy = (dk.High - dk.Low) / dk.Close; j = int(np.argmax(boy.to_numpy())); b = dk.iloc[j]
    kom = dk.iloc[max(0, j - 2): j + 3]
    return {"pazar": r.pazar, "bar": j - (len(dk) - 1), "O": float(b.Open), "H": float(b.High), "L": float(b.Low), "C": float(b.Close),
            "boy_C": float(boy.iloc[j]), "boy_medyan": float(boy.median()), "H_komsu_max": float(kom.drop(kom.index[min(2, j)]).High.max())}


def ge_olc(cikti: Optional[str] = None, veri: Optional[str] = None, dev: bool = True) -> Dict[str, Any]:
    """AŞAMA C ölçüm: kapı -> birleştir -> ölçü 1 / 1b / 2 -> eğitim -> göz skoru -> hücreler -> olasılık -> satır dosyaları + sonuc_C.json."""
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or GE_YOL["cikti"]
    kapi = ge_kapi_c(cikti)
    S = ge_anahtar_oku(cikti); T = ge_etiket_oku(cikti)
    X = pd.read_csv(GE_YOL["olay"], dtype={"sembol": str, "pazar": str, "donem": str}); X["giris"] = pd.to_datetime(X["giris"])
    F = pd.read_csv(_ge_yol("ozellik", cikti), dtype={"sembol": str, "pazar": str})
    X["tarih"] = pd.to_datetime(X["tarih"]); F["tarih"] = pd.to_datetime(F["tarih"])
    if len(X) != len(F) or not ((X.sembol.to_numpy() == F.sembol.to_numpy()).all() and (X.tarih.to_numpy() == F.tarih.to_numpy()).all()):
        raise GEHata("olay_Y1 ve ozellik_Y1 sıraları aynı değil")
    M = ge_birlestir(S, T, X, F)
    E = GE_C_ESIK
    J: Dict[str, Any] = {"surum": GE_SURUM, "c_esik_sha": ge_c_esik_sha(), "zaman_utc": _ge_simdi(), "kapi": kapi,
                         "dagilim": M.karar.value_counts().to_dict(), "olcu_disi": int(len(M) - len(ge_olculur(M))),
                         "olcu_disi_no": ge_olculur(M).pipe(lambda g: sorted(set(M.no) - set(g.no)))}
    J["neden_sikligi"] = pd.Series([k for n in M.nedenler for k in n]).value_counts().to_dict()
    J["olcu1"] = ge_iki_grup(M[M.karar == "OLUR"], M[M.karar == "OLMAZ"], "OLUR", "OLMAZ", E["olcu1"])
    J["olcu1"]["olur_olaylar"] = [{"no": int(r.no), "pazar": r.pazar, "donem": r.donem, "h5": r.h5, "es_h5": r.es_h5, "st5": r.st5,
                                   "getiri": r.getiri} for r in M[M.karar == "OLUR"].itertuples()]
    J["olcu1b"] = ge_iki_grup(M[M.karar != "OLMAZ"], M[M.karar == "OLMAZ"], "OLMAZ-DEĞİL", "OLMAZ", E["olcu1b"])
    J["olcu1b"]["pazar"] = {p: {"OLMAZ-DEĞİL": ge_grup(M[(M.pazar == p) & (M.karar != "OLMAZ")]), "OLMAZ": ge_grup(M[(M.pazar == p) & (M.karar == "OLMAZ")])}
                            for p in OC.OC_ESIK["pazar"]}
    J["olcu1b"]["donem"] = {q: {"OLMAZ-DEĞİL": ge_grup(M[(M.donem == q) & (M.karar != "OLMAZ")]), "OLMAZ": ge_grup(M[(M.donem == q) & (M.karar == "OLMAZ")])}
                            for q in ("2023", "2024-26")}
    J["grup"] = {k: ge_grup(M[M.karar == k]) for k in GE_KARARLAR}
    J["neden"] = ge_neden_olcu(M, E)
    Eg = ge_egitim(M, E)
    J["egitim"] = {k: v for k, v in Eg.items() if k not in ("model", "oof")}
    M["oof"] = Eg["oof"]
    O = X.copy(); O["skor"] = ge_skor(Eg["model"], F)
    O["besli"], sin = ge_besli(O.skor.to_numpy(), E)
    J["besli_sinir"] = [float(v) for v in sin]
    etiketli = set(zip(M.pazar, M.sembol, M.tarih))
    O["etiketli"] = [k in etiketli for k in zip(O.pazar, O.sembol, O.tarih)]
    if int(O.etiketli.sum()) != len(M):
        raise GEHata("etiketli olay sayısı skor tablosunda tutmadı")
    guc = json.load(open(GE_C_DOSYA["guc"], encoding="utf-8")) if os.path.exists(GE_C_DOSYA["guc"]) else None
    J["guc_tablosu"] = bool(guc)
    J["skor_tum"] = ge_skor_hucre(O, guc)
    J["skor_dis"] = ge_skor_hucre(O[~O.etiketli], guc)
    e1, e2 = J["skor_tum"]["etiket"], J["skor_dis"]["etiket"]
    J["skor_etiket"] = e1 if _GE_SIRA.get(e1.split(" (")[0], 1) <= _GE_SIRA.get(e2.split(" (")[0], 1) else e2
    kp = (O.pazar.isin(["ABD", "AVR"]) & O.donem.isin(["2023", "2024-26"])).to_numpy()
    J["olasilik_karar"] = ge_olasilik(O, kp)
    J["olasilik_tum"] = ge_olasilik(O, np.ones(len(O), bool))
    J["olasilik_dis_karar"] = ge_olasilik(O, kp & ~O.etiketli.to_numpy())
    J["etiketli_besli"] = M.assign(b=O.set_index(["pazar", "sembol", "tarih"]).loc[list(zip(M.pazar, M.sembol, M.tarih)), "besli"].to_numpy()) \
        .groupby(["karar", "b"]).size().unstack(fill_value=0).to_dict("index")
    if dev:
        J["dev_fitil"] = ge_dev_fitil(S, T, veri); J["no274"] = ge_no274(veri, cikti)
    # satır dosyaları (yeniden üretim)
    Ms = M[["no", "pazar", "donem", "sembol", "tarih", "giris", "karar", "guven"] + ["h5", "h10", "st5", "es_h5", "es_h10", "es_st5", "getiri", "oof"]].copy()
    Ms["nedenler"] = M.nedenler.apply(lambda n: ";".join(n))
    Ms.to_csv(os.path.join(cikti, GE_C_DOSYA["satir"]), index=False)
    O[["pazar", "sembol", "tarih", "donem", "skor", "besli", "etiketli"]].to_csv(os.path.join(cikti, GE_C_DOSYA["skor"]), index=False,
                                                                                    float_format="%.6g")
    J["sure_sn"] = round(time.time() - t0, 1)
    _ge_yaz(os.path.join(cikti, GE_C_DOSYA["sonuc"]), json.dumps(_ge_json(J), ensure_ascii=False, indent=1), "sonuç C")
    gelog.info("AŞAMA C ölçüm bitti (%.0f sn)", J["sure_sn"])
    return J


def _ge_json(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _ge_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_ge_json(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return _ge_json(o.tolist())
    if isinstance(o, pd.Timestamp):
        return str(o.date())
    return o


# ---- AŞAMA C kapısı (AŞAMA A ge_kapi kod sha'sı aşama C kodu eklenince değişir; AŞAMA C kod sha'sı SAPMA-1'de mühürlü)
def ge_kapi_c(cikti: Optional[str] = None) -> Dict[str, Any]:
    """AŞAMA C başında: ON_KAYIT.md git'te ve SAPMA-1 bölümü var; GE_ESIK (A), GE_C_ESIK, aşama C kodu, etiket, anahtar, özellik, olay sha'ları
    ön kayıttakiyle aynı; kontrol kapısı açık."""
    cikti = cikti or GE_YOL["cikti"]; yol = _ge_yol("onkayit", cikti)
    g = _ge_git(yol)
    import IZ_KARNE as IK
    IK.ik_kontrol_kapisi(yol)
    metin = open(yol, encoding="utf-8").read()
    if "## SAPMA-1" not in metin:
        raise GEHata("kapı C: ON_KAYIT.md'de SAPMA-1 bölümü yok")
    bek = {"GE_ESIK_SHA": ge_esik_sha(), "GE_C_ESIK_SHA": ge_c_esik_sha(), "GE_KOD_SHA_C": _ge_sha_dosya(GE_YOL["kod"]),
           "ETIKET_SHA": _ge_sha_dosya(os.path.join(cikti, GE_C_DOSYA["etiket"])), "ANAHTAR_SHA": _ge_sha_dosya(_ge_yol("anahtar", cikti)),
           "OZELLIK_SHA": _ge_sha_dosya(_ge_yol("ozellik", cikti)), "OLAY_Y1_SHA": _ge_sha_dosya(GE_YOL["olay"])}
    for ad, v in bek.items():
        m = re.search(rf"{ad}:\s*`([0-9a-f]{{64}})`", metin)
        if not m or m.group(1) != v:
            raise GEHata(f"kapı C: {ad} tutmuyor (ön kayıttan sonra değişmiş ya da yok)")
    try:
        import subprocess
        st = subprocess.run(["git", "status", "--porcelain", "--", yol], cwd=KOK_GE, capture_output=True, text=True, timeout=30).stdout
        if st.strip():
            raise GEHata("kapı C: ON_KAYIT.md'de commit edilmemiş değişiklik var (SAPMA-1 ölçümden önce commit edilmeli)")
    except (OSError, subprocess.SubprocessError):
        gelog.warning("kapı C: git durumu okunamadı")
    return {"onkayit": g, "gecti": True}


# ---- RAPOR
def _p(x: Any, n: int = 1) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    return ("-" if float(x) < 0 else "") + f"%{abs(100 * float(x)):.{n}f}".replace(".", ",")


def _s(x: Any, n: int = 2) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{float(x):.{n}f}".replace(".", ",")


def _pv(x: Any) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else (f"{float(x):.3f}".replace(".", ",") if x >= 0.001 else "< 0,001")


def _ge_grup_satir(ad: str, g: Dict[str, Any]) -> str:
    return (f"| {ad} | {g['n']} | {_p(g.get('h5_p_olay'))} | {_p(g.get('h5_p_ref'))} | {_s(g.get('h5_kat'))} [{_s(g.get('h5_alt'))}; {_s(g.get('h5_ust'))}] | "
            f"{_p(g.get('h10_p_olay'))} | {_p(g.get('st5_p_olay'))} / {_p(g.get('st5_p_ref'))} | {_p(g.get('getiri_med'), 2)} |")


_GE_GH = "| Grup | n | +%5 payı | eş +%5 | KAT5 [%95] | +%10 payı | stop önce olay / eş | getiri medyan (takip stoplu, bilgi) |\n|---|---|---|---|---|---|---|---|"


def ge_c_rapor(J: Dict[str, Any], cikti: Optional[str] = None) -> str:
    """RAPOR.md (§5 içeriği + SAPMA-1 + sınırlar). Sayılar yalnız sonuc_C.json'dan."""
    cikti = cikti or GE_YOL["cikti"]
    o1, o1b, eg = J["olcu1"], J["olcu1b"], J["egitim"]
    d = J["dagilim"]
    s = ["# GOZ_ETIKET — AŞAMA C RAPORU (ölçüm, eğitim, göz skoru, hakem seti)", "",
         f"{J['surum']} · GE_C_ESIK sha `{J['c_esik_sha'][:16]}…` · {J['zaman_utc']}", "",
         "Etiketleyen bir DİL MODELİDİR (Cemal'in gözünün vekili); Cemal'in kendi etiketi değildir. Aşağıdaki her sonuç bu vekilin sonucudur.", "",
         "## 1. ÖZET", "",
         f"- Etiket dağılımı (300): OLUR {d.get('OLUR', 0)} · BELİRSİZ {d.get('BELİRSİZ', 0)} · OLMAZ {d.get('OLMAZ', 0)}. Ölçü dışı (h5 / eş ölçülemedi): {J['olcu_disi']}.",
         f"- ÖLÇÜ 1 (OLUR vs OLMAZ, ön kayıt): **{o1['durum']}** (OLUR n {o1['OLUR']['n']} < 30).",
         f"- ÖLÇÜ 1b (SAPMA-1, OLMAZ-DEĞİL vs OLMAZ): **{o1b['durum']}** (KAT5 alt uç > 1: {'evet' if o1b['s_kat'] else 'hayır'}; "
         f"+%5 payı farkı Fisher p < 0,05 ve yön: {'evet' if o1b['s_pay'] else 'hayır'}; stop payı < eş: {'evet' if o1b['s_stop'] else 'hayır'}).",
         f"- EĞİTİM (OLMAZ-DEĞİL / OLMAZ, F1-F18 lojistik): 5 kat CV AUC (kat dışı havuz) {_s(eg['cv']['auc_oof'], 3)}; kat ortalaması "
         f"{_s(eg['cv']['auc_kat_ort'], 3)} ± {_s(eg['cv']['auc_kat_sd'], 3)}; etiket permütasyonu p {_pv(eg['cv'].get('perm_p'))} "
         f"(permütasyon %95 {_s(eg['cv'].get('perm_95'), 3)}).",
         f"- GÖZ SKORU (üst beşte bir, YAPI_HEDEF karar kuralı): ETİKET **{J['skor_etiket']}** (bütün olaylar: {J['skor_tum']['etiket']}; "
         f"dış örneklem: {J['skor_dis']['etiket']}).", "",
         "## 2. SAPMA-1 (ölçümden önce yazıldı ve commit edildi; ON_KAYIT.md)", "",
         "OLUR n = 6 < 30 olduğundan ölçü 1 kuralla ÖLÇÜLEMEDİ. Eklenen ölçü 1b: OLMAZ-DEĞİL (OLUR + BELİRSİZ) vs OLMAZ; eğitim hedefi OLMAZ-DEĞİL (1) / "
         "OLMAZ (0). Ayrıntı ve eşikler ON_KAYIT.md SAPMA-1 bölümünde.", "",
         "## 3. ETİKET DAĞILIMI ve NEDEN KODU SIKLIĞI", "",
         "| Karar | n |", "|---|---|"] + [f"| {k} | {d.get(k, 0)} |" for k in GE_KARARLAR] + ["",
         "| Kod | n | açılım |", "|---|---|---|"] + [f"| {k} | {v} | {ge_neden_acilim(k)} |" for k, v in
                                                     sorted(J["neden_sikligi"].items(), key=lambda kv: (int(re.sub(r'\D', '', kv[0])), kv[0][-1]))]
    s += ["", "## 4. ÖLÇÜ 1 (ön kayıt) — OLUR vs OLMAZ", "", _GE_GH, _ge_grup_satir("OLUR", o1["OLUR"]), _ge_grup_satir("OLMAZ", o1["OLMAZ"]), "",
          f"Fisher (+%5 payı, iki yönlü) p = {_pv(o1['fisher_p'])}. KARAR: **{o1['durum']}** (OLUR n {o1['OLUR']['n']} < 30; olaylar tek tek aşağıda, bulgu değildir).", "",
          "| No | pazar | dönem | +%5 | eş +%5 | stop önce | getiri |", "|---|---|---|---|---|---|---|"]
    s += [f"| {r['no']} | {r['pazar']} | {r['donem']} | {_s(r['h5'], 0)} | {_p(r['es_h5'])} | {_s(r['st5'], 0)} | {_p(r['getiri'], 1)} |" for r in o1["olur_olaylar"]]
    s += ["", "## 5. ÖLÇÜ 1b (SAPMA-1) — OLMAZ-DEĞİL vs OLMAZ", "", _GE_GH, _ge_grup_satir("OLMAZ-DEĞİL", o1b["OLMAZ-DEĞİL"]),
          _ge_grup_satir("OLMAZ", o1b["OLMAZ"]), "",
          f"Fisher (+%5 payı, iki yönlü) p = {_pv(o1b['fisher_p'])}. Şartlar: KAT5 alt uç > 1 {'EVET' if o1b['s_kat'] else 'HAYIR'}; pay farkı (p < 0,05 ve "
          f"yön) {'EVET' if o1b['s_pay'] else 'HAYIR'}; stop önce < eş {'EVET' if o1b['s_stop'] else 'HAYIR'}. KARAR: **{o1b['durum']}**.", "",
          "Pazar / dönem kırılımı (bilgi; hücreler küçük):", "", _GE_GH]
    for k, v in list(o1b["pazar"].items()) + list(o1b["donem"].items()):
        s += [_ge_grup_satir(f"{k} OLMAZ-DEĞİL", v["OLMAZ-DEĞİL"]), _ge_grup_satir(f"{k} OLMAZ", v["OLMAZ"])]
    s += ["", "Karar grubu başına (bilgi):", "", _GE_GH] + [_ge_grup_satir(k, J["grup"][k]) for k in GE_KARARLAR]
    s += ["", "## 6. ÖLÇÜ 2 — NEDEN KODLARI (bilgi; BH q 0,10, Fisher iki yönlü)", "",
          "| Kod | açılım | n var / yok | +%5 var / yok | KAT5 var [%95] | stop önce var / yok | p | BH |", "|---|---|---|---|---|---|---|---|"]
    for r in J["neden"]:
        s.append(f"| {r['kod']} | {GE_NEDEN_ACILIM.get(r['kod'][:-1], '')} | {r['n_var']} / {r['n_yok']}{' (n az)' if r['n_az'] else ''} | "
                 f"{_p(r['h5_var'])} / {_p(r['h5_yok'])} | {_s(r['kat5_var'])} [{_s(r['kat5_alt'])}; {_s(r['kat5_ust'])}] | "
                 f"{_p(r['st5_var'])} / {_p(r['st5_yok'])} | {_pv(r['p'])} | {'geçer' if r['bh'] else '-'} |")
    s += [f"", f"BH q 0,10 ile geçen kod sayısı: {sum(r['bh'] for r in J['neden'])} / {len(J['neden'])}.", "",
          "## 7. EĞİTİM — göz sayısal özelliklerden ne kadar öğrenilebiliyor", "",
          f"- Hedef OLMAZ-DEĞİL (1, n {eg['cv']['n1']}) / OLMAZ (0, n {eg['cv']['n0']}); F1-F18; medyan doldurma + standartlaştırma + L2 lojistik (C = 1); "
          "her kat dönüşümleri yalnız eğitim katından (sızıntı yok; test_goz_etiket).",
          f"- 5 kat CV AUC: kat dışı havuz {_s(eg['cv']['auc_oof'], 3)}; katlar {', '.join(_s(a, 3) for a in eg['cv']['auc_kat'])}; "
          f"etiket permütasyonu (200) ortalaması {_s(eg['cv'].get('perm_ort'), 3)}, %95'i {_s(eg['cv'].get('perm_95'), 3)}, p {_pv(eg['cv'].get('perm_p'))}.",
          f"- Bilgi, §5 asıl hedef OLUR (n {eg['asil']['n1']}) / OLMAZ (n {eg['asil']['n0']}): CV AUC {_s(eg['asil'].get('auc_oof'), 3)} — OLUR n 6: ÖLÇÜLEMEDİ.",
          "", "Katsayılar (standart birim; + = OLMAZ-DEĞİL yönü; |katsayı| sırasıyla) ve tek özellik AUC (bilgi):", "",
          "| F | tanım | katsayı | tek başına AUC |", "|---|---|---|---|"]
    tek = {r["F"]: r for r in eg["tek"]}
    s += [f"| {r['F']} | {r['tanim']} | {_s(r['kat'], 3)} | {_s(tek[r['F']]['auc'], 3)} |" for r in eg["katsayi"]]
    s += ["", "## 8. GÖZ SKORU — hücre tablosu (B5 = üst beşte bir; YAPI_HEDEF karar kuralı: n >= 30, KAT5 eş alt uç > 1, stop önce < eş, "
          "plasebo KAT5 alt uç > 1; tutmazsa n >= 1.000 ya da güç >= %80 -> DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ)", "",
          f"Beşte bir sınırları (26.663 olay): {', '.join(_s(v, 3) for v in J['besli_sinir'])}.", ""]
    for ad, K in (("BÜTÜN OLAYLAR", J["skor_tum"]), ("DIŞ ÖRNEKLEM (300 etiketli olay çıkarılmış)", J["skor_dis"])):
        s += [f"### {ad} — etiket: {K['etiket']}", "",
              "| Hücre | B5 n | B5 +%5 / eş | KAT5 eş [%95] | plasebo KAT5 alt | stop önce B5 / eş | B1 n | B1 +%5 / eş | B1 KAT5 | B5 vs B1 Fisher p | güç | DURUM |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for h in K["hucre"]:
            u, a = h["ust"], h["alt"]
            s.append(f"| {h['pazar']} {h['donem']}{' (karar)' if h['karar_hucre'] else ''} | {u.get('n', 0)} | {_p(u.get('h5_p_olay'))} / {_p(u.get('h5_p_ref'))} | "
                     f"{_s(u.get('h5_kat'))} [{_s(u.get('h5_alt'))}; {_s(u.get('h5_ust'))}] | {_s(u.get('pl_h5_alt'))} | {_p(u.get('st5_p_olay'))} / {_p(u.get('st5_p_ref'))} | "
                     f"{a.get('n', 0)} | {_p(a.get('h5_p_olay'))} / {_p(a.get('h5_p_ref'))} | {_s(a.get('h5_kat'))} | {_pv(h['fisher_ust_alt'])} | {_p(h['guc'], 0)} | {h['durum']} |")
        s.append("")
    s += [f"ETİKET (muhafazakâr olan): **{J['skor_etiket']}**.", "",
          "## 9. OLASILIK TABLOSU (göz skoru beşte birleri; 15 bar, giriş t+1 açılış, stop hat x 0,98; eş = aynı gün aynı kova)", "",
          "### Karar pazarları (ABD + AVR, 2023 + 2024-26)", "", _GE_GH.replace("| Grup |", "| Beşli |")]
    s += [_ge_grup_satir(f"B{r['besli']}", r) for r in J["olasilik_karar"]]
    s += ["", "### Aynı, 300 etiketli olay çıkarılmış (dış örneklem)", "", _GE_GH.replace("| Grup |", "| Beşli |")]
    s += [_ge_grup_satir(f"B{r['besli']}", r) for r in J["olasilik_dis_karar"]]
    s += ["", "### Bütün olaylar (üç pazar, 2016-26; bilgi)", "", _GE_GH.replace("| Grup |", "| Beşli |")]
    s += [_ge_grup_satir(f"B{r['besli']}", r) for r in J["olasilik_tum"]]
    s += ["", "KAT5 = olayın +%5 payı / aynı gün aynı kovadaki eşlerin +%5 payı (1 = eşle aynı). Olasılık tablosu 15 bar standardıdır (12 ay +%100 "
          "bu ölçüde yoktur).", "", "Etiketli olayların skor beşlisi (eğitim içi; bilgi):", "", "| Karar | B1 | B2 | B3 | B4 | B5 |", "|---|---|---|---|---|---|"]
    s += [f"| {k} | " + " | ".join(str(J["etiketli_besli"].get(k, {}).get(str(b), J["etiketli_besli"].get(k, {}).get(b, 0))) for b in range(1, 6)) + " |"
          for k in GE_KARARLAR]
    if "dev_fitil" in J:
        df_, n2 = J["dev_fitil"], J["no274"]
        s += ["", "## 10. VERİ DENETİMİ — dev fitil (No 274 ve 300 görsel)", "",
              f"- No 274: sinyalden {n2['bar']} bar önce O {_s(n2['O'])} H {_s(n2['H'])} L {_s(n2['L'])} C {_s(n2['C'])}; mum boyu / kapanış {_p(n2['boy_C'])} "
              f"(pencere medyanı {_p(n2['boy_medyan'])}); komşu barların en yüksek High'ı {_s(n2['H_komsu_max'])}; High / max(O, C) = "
              f"{_s(n2['H'] / max(n2['O'], n2['C']))}. Açılış, kapanış ve dip komşularla uyumlu, yalnız High sapık: tek alanlık VERİ HATASI (gerçek işlem değil).",
              f"- 300 görselin {df_['n_dev']}'inde 120 bar penceresinde şüpheli dev fitil (High / max(O, C) ya da min(O, C) / Low > 1,5) var; "
              f"bunların {df_['dev_ve_c13']}'ünde etiketleyen C13- (dev mum / şüphe) yazmış. C13- toplam {df_['c13']} (fitil > 1,5 olmayan {df_['c13_dev_yok']}; "
              "C13 eşiği göz kararıdır, 1,5 kat yalnız veri hatası adayı içindir).",
              "| No | pazar | en büyük oran | bar | karar |", "|---|---|---|---|---|"]
        s += [f"| {r['no']} | {r['pazar']} | {_s(r['en_buyuk'])} | {r['bar']} | {r['karar']} |" for r in df_["dev_no"]]
    s += ["", "## 11. SIZINTI DENETİMİ", "",
          "- Etiketler sonuç görmeden: AŞAMA B kendi raporunda anahtar / olay dosyasını açmadığını yazdı; etiket.json AŞAMA C'de değiştirilmedi (ETIKET_SHA SAPMA-1'de "
          "mühürlü, kapı C denetler).",
          "- Özellikler t'ye kadar: AŞAMA A prefix testi (koşuda pazar başına 10 olay + test_goz_etiket).",
          "- Göz skoru 300 etiketli olay dışında ayrı raporlandı (§8 ve §9 'dış örneklem').",
          "- CV: doldurma ve ölçek her katta yalnız eğitim katından (test_goz_etiket 'CV sızıntısı yok').", "",
          "## 12. HAKEM SETİ", "",
          "arastirma_cikti/goz_etiket/GOZ_HAKEM_SET.pdf (40 sayfa; 1-20 KÖR, 21-40 AÇIK; t sonrası yok, hisse adı yok); hakem_anahtar.json GİZLİ (sayfa -> "
          "örneklem no, aşama B kararı). Yanıt: hakem_cevap_sablon.csv doldurulur (sayfa, cevap, neden) ve `python GOZ_ETIKET.py hakem --cevap-dosya DOSYA` "
          "ile iki yarı ayrı raporlanır (kör: Cohen kappa + çapraz tablo; açık: doğru / yanlış, kural başına yanlış sayımı).", "",
          "## 13. SINIRLAR", "",
          "- 300 etiket; OLUR yalnız 6: asıl ölçü (OLUR) ve asıl eğitim hedefi ÖLÇÜLEMEDİ. Ölçü 1b ve eğitim SAPMA-1'dir (önceden yazılı ama ön kayıttan sonra).",
          "- Etiketleyen bir dil modeli: Cemal'in gözünün vekilidir, Cemal'in kendi kararı değildir. Hakem seti bu vekilin Cemal'le ne kadar uyuştuğunu ölçmek içindir.",
          "- Evren bugün işlem gören hisseler (hayatta kalma yanlılığı): hedef payları yukarı yanlı okunmalı; eşler aynı evrenden olduğu için KAT daha az etkilenir.",
          "- Veri: tek alanlık dev fitil hataları var (§10); F-özellikleri oran / medyan olduğundan tek bar etkisi sınırlı, ama C13 etiketlerini etkileyebilir.",
          "- Takip stoplu getiri bilgi satırıdır, karar ölçüsü değildir.", ""]
    metin = "\n".join(s)
    _ge_yaz(os.path.join(cikti, GE_C_DOSYA["rapor"]), metin, "rapor C")
    return os.path.join(cikti, GE_C_DOSYA["rapor"])


# ---- HAKEM SETİ
def ge_hakem_sec(T: pd.DataFrame, E: Dict[str, Any] = GE_C_ESIK) -> pd.DataFrame:
    """Tohum 13: OLUR 3+3, BELİRSİZ 7+7, OLMAZ 10+10 -> sayfa 1-20 kör, 21-40 açık. DataFrame[sayfa, yari, no, karar]."""
    H = E["hakem"]; rng = np.random.default_rng(int(H["tohum"])); kor, acik = [], []
    for k in GE_KARARLAR:
        nos = np.array(sorted(T[T.karar == k].no.astype(int)))
        m = int(H["yari"][k])
        if len(nos) < 2 * m and k != "OLUR":
            raise GEHata(f"hakem: {k} sayısı {len(nos)} < {2 * m}")
        p = nos[rng.permutation(len(nos))]
        kor += [(int(x), k) for x in p[:m]]; acik += [(int(x), k) for x in p[m:2 * m]]
    kor = [kor[i] for i in rng.permutation(len(kor))]; acik = [acik[i] for i in rng.permutation(len(acik))]
    R = [{"sayfa": i + 1, "yari": "KÖR", "no": n, "karar": k} for i, (n, k) in enumerate(kor)]
    R += [{"sayfa": len(kor) + i + 1, "yari": "AÇIK", "no": n, "karar": k} for i, (n, k) in enumerate(acik)]
    D = pd.DataFrame(R)
    if len(D) != int(H["sayfa"]) or D.no.duplicated().any():
        raise GEHata(f"hakem seçimi {len(D)} sayfa / çift no")
    return D


def ge_hakem_pdf(cikti: Optional[str] = None, png: Optional[str] = None) -> Dict[str, Any]:
    """GOZ_HAKEM_SET.pdf + hakem_anahtar.json (gizli) + hakem_cevap_sablon.csv."""
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import simpleSplit
    cikti = cikti or GE_YOL["cikti"]; png = png or GE_YOL["png"]
    T = ge_etiket_oku(cikti); D = ge_hakem_sec(T); Tn = T.set_index("no")
    font = None
    for y in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              os.path.join(os.path.dirname(__import__("matplotlib").__file__), "mpl-data", "fonts", "ttf", "DejaVuSans.ttf")):
        if os.path.exists(y):
            font = y; break
    if not font:
        raise GEHata("Türkçe yazı tipi (DejaVuSans) bulunamadı")
    pdfmetrics.registerFont(TTFont("DV", font))
    yol = os.path.join(cikti, GE_C_DOSYA["hakem_pdf"])
    W, Hh = landscape(A4); c = canvas.Canvas(yol, pagesize=(W, Hh), invariant=1)
    c.setTitle("GOZ HAKEM SETI"); c.setAuthor(""); c.setCreator(""); c.setProducer("")
    for r in D.itertuples():
        p = os.path.join(png, f"No_{int(r.no)}.png")
        if not os.path.exists(p):
            raise GEHata(f"PNG yok: {p}")
        c.setFont("DV", 11)
        c.drawString(30, Hh - 28, f"GÖZ HAKEM SETİ — Sayfa {r.sayfa} / {len(D)} — {'KÖR (yalnız grafik)' if r.yari == 'KÖR' else 'AÇIK (aşama B kararıyla)'}")
        c.setFont("DV", 8)
        c.drawString(30, Hh - 40, "Grafik: sinyal günü t (bar 0) dahil son 120 bar; t sonrası YOK; hisse adı / tarih yok. Mavi alan S6 bölgesi, turuncu kesik tavan, mavi çizgi hat.")
        iw = 600 if r.yari == "AÇIK" else 690; ih = iw * 800 / 1200
        c.drawImage(p, 30, Hh - 48 - ih, width=iw, height=ih)
        if r.yari == "KÖR":
            c.setFont("DV", 12)
            c.drawString(30, 52, "Cemal: OLUR / OLMAZ / BELİRSİZ  (birini işaretle)")
            c.drawString(30, 30, "neden: ______________________________________________________________________________")
        else:
            e = Tn.loc[int(r.no)]; x0 = 30 + iw + 12; yy = Hh - 60; gen = W - x0 - 20
            c.setFont("DV", 11); c.drawString(x0, yy, f"Aşama B kararı: {e['karar']}"); yy -= 14
            c.drawString(x0, yy, f"güven: {e['guven']} / 5"); yy -= 18
            c.setFont("DV", 9); c.drawString(x0, yy, "Neden kodları:"); yy -= 12
            for k in e["nedenler"]:
                for ln in simpleSplit(ge_neden_acilim(k), "DV", 8, gen):
                    c.setFont("DV", 8); c.drawString(x0, yy, ln); yy -= 10
                yy -= 2
            yy -= 6; c.setFont("DV", 9); c.drawString(x0, yy, "Not:"); yy -= 12
            for ln in simpleSplit(str(e["not"]), "DV", 8, gen):
                c.setFont("DV", 8); c.drawString(x0, yy, ln); yy -= 10
            c.setFont("DV", 12)
            c.drawString(30, 52, "Cemal: DOĞRU / YANLIŞ  (aşama B kararı için)")
            c.drawString(30, 30, "neden (yanlışsa hangi kural, C1..C13): ______________________________________________")
        c.showPage()
    c.save()
    A = {"uyari": "GİZLİ HAKEM ANAHTARI: Cemal yanıtlamadan önce açılmaz. sayfa -> örneklem no, aşama B kararı.",
         "tohum": GE_C_ESIK["hakem"]["tohum"], "etiket_sha": _ge_sha_dosya(os.path.join(cikti, GE_C_DOSYA["etiket"])),
         "sayfa": {str(int(r.sayfa)): {"yari": r.yari, "no": int(r.no), "karar": r.karar, "nedenler": Tn.loc[int(r.no), "nedenler"]} for r in D.itertuples()}}
    _ge_yaz(os.path.join(cikti, GE_C_DOSYA["hakem_anahtar"]), json.dumps(A, ensure_ascii=False, indent=1), "hakem anahtarı")
    sab = "sayfa,yari,cevap,neden\n" + "".join(f"{int(r.sayfa)},{r.yari},,\n" for r in D.itertuples())
    _ge_yaz(os.path.join(cikti, GE_C_DOSYA["hakem_sablon"]), sab, "hakem şablonu")
    return {"pdf": yol, "boyut_mb": round(os.path.getsize(yol) / 2 ** 20, 2), "sayfa": len(D),
            "kor": D[D.yari == "KÖR"].karar.value_counts().to_dict(), "acik": D[D.yari == "AÇIK"].karar.value_counts().to_dict()}


_GE_TR = str.maketrans({"İ": "I", "ı": "I", "Ş": "S", "ş": "S", "Ğ": "G", "ğ": "G", "Ü": "U", "ü": "U", "Ö": "O", "ö": "O", "Ç": "C", "ç": "C"})
_GE_CEVAP = {"OLUR": "OLUR", "OLMAZ": "OLMAZ", "BELIRSIZ": "BELİRSİZ", "DOGRU": "DOĞRU", "YANLIS": "YANLIŞ"}


def ge_cevap_norm(x: Any) -> Optional[str]:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return None
    k = str(x).strip().translate(_GE_TR).upper()
    return _GE_CEVAP.get(k)


def ge_kappa(a: List[str], b: List[str]) -> float:
    """Cohen kappa (iki etiketçi, aynı öğeler)."""
    a = list(a); b = list(b)
    if not a or len(a) != len(b):
        return np.nan
    kat = sorted(set(a) | set(b)); n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(k) / n) * (b.count(k) / n) for k in kat)
    return float((po - pe) / (1 - pe)) if pe < 1 else np.nan


def ge_hakem_degerlendir(cevap_yol: str, cikti: Optional[str] = None) -> Dict[str, Any]:
    """Cemal'in yanıtı (CSV: sayfa, cevap, neden; ya da JSON {sayfa: {cevap, neden}}) -> iki yarı ayrı: kör kappa + çapraz tablo;
    açık doğru / yanlış + kural başına yanlış sayımı. HAKEM_SONUC.md yazar."""
    cikti = cikti or GE_YOL["cikti"]
    A = json.load(open(os.path.join(cikti, GE_C_DOSYA["hakem_anahtar"]), encoding="utf-8"))["sayfa"]
    if cevap_yol.endswith(".json"):
        Jc = json.load(open(cevap_yol, encoding="utf-8"))
        C = pd.DataFrame([{"sayfa": int(k), "cevap": v.get("cevap"), "neden": v.get("neden", "")} for k, v in Jc.items()])
    else:
        C = pd.read_csv(cevap_yol, dtype=str, keep_default_na=False)
        if "sayfa" not in C or "cevap" not in C:
            raise GEHata("cevap dosyası: 'sayfa' ve 'cevap' sütunları zorunlu")
        C["sayfa"] = C.sayfa.astype(int)
        if "neden" not in C:
            C["neden"] = ""
    C["cevap_n"] = C.cevap.apply(ge_cevap_norm)
    kor, acik, gecersiz = [], [], []
    for r in C.itertuples():
        a = A.get(str(int(r.sayfa)))
        if a is None:
            raise GEHata(f"cevap: sayfa {r.sayfa} anahtarda yok")
        if r.cevap_n is None:
            gecersiz.append(int(r.sayfa)); continue
        if a["yari"] == "KÖR":
            if r.cevap_n not in GE_KARARLAR:
                gecersiz.append(int(r.sayfa)); continue
            kor.append({"sayfa": int(r.sayfa), "B": a["karar"], "Cemal": r.cevap_n, "neden": r.neden})
        else:
            if r.cevap_n not in ("DOĞRU", "YANLIŞ"):
                gecersiz.append(int(r.sayfa)); continue
            acik.append({"sayfa": int(r.sayfa), "B": a["karar"], "nedenler": a["nedenler"], "Cemal": r.cevap_n, "neden": r.neden,
                         "andigi": sorted(set(re.findall(r"C(?:1[0-3]|[1-9])", str(r.neden).upper())))})
    K = pd.DataFrame(kor); out: Dict[str, Any] = {"kor_n": len(K), "acik_n": len(acik), "gecersiz": gecersiz}
    if len(K):
        out["kappa"] = ge_kappa(K.Cemal.tolist(), K.B.tolist())
        out["uyum"] = float((K.Cemal == K.B).mean())
        out["capraz"] = pd.crosstab(K.B, K.Cemal).reindex(index=list(GE_KARARLAR), columns=list(GE_KARARLAR), fill_value=0).to_dict("index")
        K2 = K.assign(B2=np.where(K.B == "OLMAZ", "OLMAZ", "OLMAZ-DEĞİL"), C2=np.where(K.Cemal == "OLMAZ", "OLMAZ", "OLMAZ-DEĞİL"))
        out["kappa_iki"] = ge_kappa(K2.C2.tolist(), K2.B2.tolist())
    if acik:
        Ac = pd.DataFrame(acik)
        out["dogru"] = int((Ac.Cemal == "DOĞRU").sum()); out["yanlis"] = int((Ac.Cemal == "YANLIŞ").sum())
        out["yanlis_karar"] = Ac[Ac.Cemal == "YANLIŞ"].B.value_counts().to_dict()
        y = Ac[Ac.Cemal == "YANLIŞ"]
        out["kural_andigi"] = pd.Series([k for l in y.andigi for k in l]).value_counts().to_dict() if len(y) else {}
        out["kural_B_yanlis"] = pd.Series([k[:-1] for l in y.nedenler for k in l]).value_counts().to_dict() if len(y) else {}
        out["kural_B_tum"] = pd.Series([k[:-1] for l in Ac.nedenler for k in l]).value_counts().to_dict()
    s = ["# GOZ_ETIKET — HAKEM SONUCU (Cemal vs aşama B vekili)", "", f"Cevap dosyası: {os.path.basename(cevap_yol)} · {_ge_simdi()}", "",
         "## KÖR YARI (sayfa 1-20)", "", f"- Yanıtlanan: {out['kor_n']}; uyum {_p(out.get('uyum'))}; Cohen kappa (3 sınıf) {_s(out.get('kappa'), 3)}; "
         f"kappa (OLMAZ / OLMAZ-DEĞİL) {_s(out.get('kappa_iki'), 3)}.", "", "| aşama B \\ Cemal | OLUR | BELİRSİZ | OLMAZ |", "|---|---|---|---|"]
    for k in GE_KARARLAR:
        r = out.get("capraz", {}).get(k, {})
        s.append(f"| {k} | " + " | ".join(str(r.get(c, 0)) for c in GE_KARARLAR) + " |")
    s += ["", "## AÇIK YARI (sayfa 21-40)", "", f"- Yanıtlanan: {out['acik_n']}; DOĞRU {out.get('dogru', 0)}, YANLIŞ {out.get('yanlis', 0)}; "
          f"yanlış bulunan kararlar: {out.get('yanlis_karar', {})}.", "", "| Kural | Cemal'in yanlış dediği sayfalarda andığı | yanlış sayfalarda aşama B'nin kullandığı | açık yarıda toplam kullanım |",
          "|---|---|---|---|"]
    for k in sorted(set(out.get("kural_andigi", {})) | set(out.get("kural_B_yanlis", {})) | set(out.get("kural_B_tum", {})), key=lambda x: int(x[1:])):
        s.append(f"| {k} {GE_NEDEN_ACILIM.get(k, '')} | {out.get('kural_andigi', {}).get(k, 0)} | {out.get('kural_B_yanlis', {}).get(k, 0)} | {out.get('kural_B_tum', {}).get(k, 0)} |")
    s += ["", f"Geçersiz / boş yanıt sayfaları: {gecersiz or 'yok'}.", ""]
    _ge_yaz(os.path.join(cikti, GE_C_DOSYA["hakem_sonuc"]), "\n".join(s), "hakem sonucu")
    out["rapor"] = os.path.join(cikti, GE_C_DOSYA["hakem_sonuc"])
    return out


# ================================================================ ÇAKIŞMA KAPISI ve KOMUT
def _cakisma_kontrol_ge(_once=_CK_ONCE_GE, _dosya="GOZ_ETIKET.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_GE", "_CK_KAYIT", "_cakisma_kontrol_ge", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "warnings", "_dt", "annotations",
           "Any", "Dict", "List", "Optional", "Tuple", "OC", "S6", "YH")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ge()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=GE_SURUM)
    ap.add_argument("komut", choices=["orneklem", "gorsel", "ozellik", "onkayit", "kapi", "sha", "kapi_c", "olc", "rapor", "hakem", "no274"])
    ap.add_argument("--cevap-dosya", default=None)
    ap.add_argument("--islem", type=int, default=1)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--png", default=None)
    ap.add_argument("--gitsiz", action="store_true")
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "orneklem":
            S_ = ge_orneklem()
            ge_anahtar_yaz(S_, a.cikti)
            print(S_.groupby(["pazar", "donem"]).size().to_string())
        elif a.komut == "gorsel":
            print(json.dumps(ge_gorsel(a.cikti, a.png, a.veri), ensure_ascii=False))
        elif a.komut == "ozellik":
            print(ge_ozellik(a.cikti, a.veri, a.islem))
        elif a.komut == "onkayit":
            print(ge_onkayit_yaz(a.cikti, a.png, git=not a.gitsiz, uzerine=a.uzerine_yaz))
        elif a.komut == "kapi":
            print(json.dumps(ge_kapi(a.cikti), ensure_ascii=False))
        elif a.komut == "kapi_c":
            print(json.dumps(ge_kapi_c(a.cikti), ensure_ascii=False))
        elif a.komut == "olc":
            J_ = ge_olc(a.cikti, a.veri)
            print(ge_c_rapor(_ge_json(J_), a.cikti))
        elif a.komut == "rapor":
            print(ge_c_rapor(json.load(open(os.path.join(a.cikti or GE_YOL["cikti"], GE_C_DOSYA["sonuc"]), encoding="utf-8")), a.cikti))
        elif a.komut == "hakem":
            if a.cevap_dosya:
                print(json.dumps(_ge_json(ge_hakem_degerlendir(a.cevap_dosya, a.cikti)), ensure_ascii=False, indent=1))
            else:
                print(json.dumps(ge_hakem_pdf(a.cikti, a.png), ensure_ascii=False))
        elif a.komut == "no274":
            print(json.dumps(ge_no274(a.veri, a.cikti), ensure_ascii=False))
        else:
            print(json.dumps({"esik": ge_esik_sha(), "c_esik": ge_c_esik_sha(), "kod": _ge_sha_dosya(GE_YOL["kod"])}, indent=1))
    except GEHata as ex:
        gelog.error("%s", ex); sys.exit(1)
