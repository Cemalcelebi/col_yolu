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
    ap.add_argument("komut", choices=["orneklem", "gorsel", "ozellik", "onkayit", "kapi", "sha"])
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
        else:
            print(json.dumps({"esik": ge_esik_sha(), "kod": _ge_sha_dosya(GE_YOL["kod"])}, indent=1))
    except GEHata as ex:
        gelog.error("%s", ex); sys.exit(1)
