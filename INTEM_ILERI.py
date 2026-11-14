"""INTEM_ILERI — Ç124 (K45) INTEM tipi kısa ufuk kutu çıkışı kuralının GÖRÜLMEMİŞ VERİDE ileri testi, tek dosya
(14 Kasım 2026; dört aşamalı yeniden ölçümün AŞAMA 5'i).

Cemal (14 Kas 2026): "önceki aşamalardan çıkan kuralları DEĞİŞTİRMEDEN, görülmemiş veride dene"; "her aşamada aynı ölçüm kriterleri;
sonucu beğenmediğimiz için eşikle oynanmaz".

KURAL (DEĞİŞMEZ; FON_IZI içe alınır, kopyalanmaz): K44 INTEM parmak izi (fi_k23_parmak; 8 ölçü dusus, egim, mum, konum, rsi, bbw, hacim,
yesil; INTEM 2026-10-09 bitişli 20 ve 10 barlık pencere) ve K44 birebir eşleşme (sekiz ölçünün pazar havuzundaki yüzdeliği INTEM
yüzdeliğinin +-band içinde; ABD bandı Ç124'te 0,125). CETVEL (yüzdelik cetveli) Ç124'ün ABD havuzudur (V_ABD ham, bütün L barlık
pencereler); görülmemiş hisselerin pencereleri bu SABİT cetvele göre yüzdeliğe çevrilir (= ham ölçü aralıkları dondurulur). K45 kendi
ölçüsü (ilk +-%5 / 8 / 12 hangisi önce, 20 gün; kutu çıkışı; koşullu +%8; oynaklık eşli rastgele taban, 10 tohum) FON_IZI fi_k45_olc /
fi_k45_rastgele_oynak ile, fon_izi_k45 istatistiği birebir (sentetik eşitlik testi).
GÖRÜLMEMİŞ VERİ: Ç124 (28 Eki) evreni = V_ABD (1.411), V_AVR (581), V_BIST (581), 2015-06 .. 2026-10 (eşleşmeler 317 / 39 ABD birebir
yeniden üretilir; ön kayıtta). Görülmemiş tek küme: ABD k34_yahoo ekinin V_ABD'de OLMAYAN hisseleri (OC.oc_veri 'k34_yahoo' kaynağı),
evrene ilk_giris gününden (2021+) itibaren. Avrupa Ç124'te KULLANILDI (görülmemiş değil); kullanılmamış dönem yok.
ÖLÇÜ ve KARAR: ORTAK_CETVEL (OC.oc_olc / OC.oc_rapor) ana pencere L=20; L=10 bilgi. Ç124'ün kendi ölçüsü eski sonuçla kıyas (bilgi).

Komut:  python INTEM_ILERI.py onkayit   veri + cetvel yeniden üretimi + tarama + olay sayımı (getiri YOK) -> ON_KAYIT.md
        python INTEM_ILERI.py kos       OC.oc_kapi + aşama sha / git kapısı + olay sha + geleceğe bakma denetimi -> ölçüm -> rapor
        python INTEM_ILERI.py rapor     intem_ileri_sonuc.json'dan raporu yeniden yazar
Colab:  exec(open('INTEM_ILERI.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_ABD.pkl, V_BIST.pkl (ham; cetvel ve INTEM izi), OC.oc_veri('ABD') (temiz + k34). Satır verisi /tmp/intem_ileri/.
        Tiingo YOK, ücretli veri YOK.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_II = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import inspect  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_II = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_II not in sys.path:
    sys.path.insert(0, KOK_II)

iilog = logging.getLogger("col.intem_ileri")
if not iilog.handlers:
    _ii_h = logging.StreamHandler(sys.stderr)
    _ii_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s intem_ileri: %(message)s", "%H:%M:%S"))
    iilog.addHandler(_ii_h)
    iilog.setLevel(logging.INFO)
    iilog.propagate = False

II_SURUM = "INTEM_ILERI v1.0 (2026-11-14)"
II_YOL = {"cikti": os.path.join(KOK_II, "arastirma_cikti", "intem_ileri"), "satir": os.environ.get("II_SATIR", "/tmp/intem_ileri"),
          "kod": os.path.join(KOK_II, "INTEM_ILERI.py"),
          "k44_eslesme": os.path.join(KOK_II, "arastirma_cikti", "fon_izi", "k44_eslesme.csv"),
          "k44_parmak": os.path.join(KOK_II, "arastirma_cikti", "fon_izi", "k44_parmak.csv")}
II_DOSYA = {"onkayit": "INTEM_ILERI_ON_KAYIT.md", "rapor": "INTEM_ILERI_RAPOR.md", "json": "intem_ileri_sonuc.json",
            "olay": "intem_olay.csv.gz", "sinyal": "intem_sinyal.csv.gz", "k45": "intem_k45_olay.csv.gz"}

# ================================================================ MÜHÜRLÜ AYAR (yalnız bu aşamanın veri seçimi / gösterimi; ölçü OC ve FON_IZI'de)
II_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "kural": "FON_IZI FI_K44 (parmak izi + birebir eşleşme) + FI_K45 (kendi ölçüsü); ikisi de DEĞİŞMEZ (sha ön kayıtta)",
    "pencere_ana": 20, "pencere_bilgi": 10,
    "band": {"20": 0.125, "10": 0.125},
    "band_kaynak": "Ç124 ABD eşleşmelerinin bandı (k44_eslesme.csv, ABD L20 ve L10: 0,125); band_genis kuralı (eşleşme < 30 -> 0,20) "
                   "Ç124 havuzunda tetiklenmedi, ileri testte bant Ç124'teki değerinde DONDURULUR",
    "cetvel": "Ç124 ABD havuzu: FON_IZI.fi_k44_havuz(V_ABD ham, L) (bütün hisselerin bütün L barlık pencereleri, süzgeçsiz); INTEM hedefi "
              "fi_k23_parmak(V_BIST ham INTEM, L) 2026-10-09 satırı; hedef yüzdelik fi_k44_yuzdelik(cetvel, hedef); görülmemiş pencerelerin "
              "yüzdeliği fi_k44_yuzdelik(cetvel, pencereler)",
    "cetvel_dogrula": "onkayit ve kos: cetvel + Ç124 adımları (ertesi birleşik takvim günü giriş, fi_k27_tekil 60) V_ABD'de k44_eslesme.csv "
                      "ABD satırlarını (L20 317, L10 39) BİREBİR üretmeli; INTEM izi k44_parmak.csv ile aynı olmalı; değilse DURUR",
    "gorulmemis": {
        "a_avrupa": "YOK: Ç124 V_AVR'yi kullandı (k44_eslesme AVR 117 + 271 eşleşme, Ç124 notu 'AVR 2016-22 +15,0 (n 92)'); görülmüş veri",
        "b_abd": "OC.oc_veri('ABD') kaynağı 'k34_yahoo' olan hisseler (V_ABD'de olmayan k34 nakdi biten şirketler); Ç124 havuzunda ve "
                 "eşleşmelerinde yok (k44_eslesme ABD sembollerinden hiçbiri k34-yalnız değil); evrene k34_evren ilk_giris gününden "
                 "itibaren (OC 'evren_once' süzgeci), 2021-01 .. 2026-08-31",
        "c_donem": "YOK: Ç124 verisi 2015-06-01 .. 2026-10 (kriz sonrası dahil); kullanılmamış dönem yok",
        "ortusme": "V_ABD hisseleri (Ç124 evreni) ölçüme GİRMEZ; görülmemiş k34 hisseleri yalnız sinyal kaynağıdır; eş / plasebo havuzu OC'nin "
                   "bütün ABD havuzudur (V_ABD + k34; kontrol grubu, sinyal değil)"},
    "sapma": [
        "SAPMA-1 (geleceğe bakma): fi_k23_parmak 'n < L + 200 -> boş' şartı serinin TOPLAM uzunluğuna bakar; yalnız t gününde hissenin "
        "kendi takviminde >= L + 200 barı (t dahil; pencere indeksi i >= L + 199) olan pencereler alınır (t'de kesilen seriyle aynı tespit).",
        "SAPMA-2 (veri): görülmemiş hisseler OC temiz verisinde taranır (H>L, V>0, fiyat>0 olmayan bar atılmış; 31.08.2026 kesiği); Ç124 ham "
        "veride tarardı. Cetvel (Ç124 havuzu) Ç124 gibi HAM V_ABD'den kurulur (birebir yeniden üretim için).",
        "SAPMA-3 (olay ve tekilleştirme): olay = eşleşen pencerenin bitiş günü t; giriş ve tekilleştirme OC kuralıyla (t'den sonraki ilk geçerli "
        "bar açılışı; 60 birleşik takvim gününde tek). Ç124 fi_k27_tekil (hissenin 60 barı) kullanırdı. Kendi ölçüsü (K45) AYNI olay "
        "kümesinde (OC olay tablosu: sembol, giris) ölçülür.",
        "SAPMA-4 (kriz kesiği, kendi ölçü): fiyat 31.08.2026'da kesildiği için K45 ölçüsü yalnız giriş + 41 bar (20 gün hedef + 20 gün "
        "koşullu + 1) hissenin verisinde olan olaylarda; oynaklık eşli rastgele satırlara AYNI tam pencere süzgeci uygulanır (Ç124'te veri "
        "Eki 2026'ya uzandığından kesik etkisi yoktu). İstatistik (oranlar, fark, bootstrap tohum 45 / 46, 2000) fon_izi_k45 ile birebir."],
    "k45": {"veri": "OC.oc_veri('ABD')['V'] (temiz; V_ABD + k34 bütün seriler; rastgele havuz = bütün ABD, Ç124'te V_ABD'ydi)",
            "tam_pencere": 41, "donem": "OC dönemi (giriş günü): hepsi (2021-26) + 2016-22 / 2023 / 2024-26 ayrı",
            "kural_kiyas": "Ç124 kendi kuralı: n >= 30, fark8 >= +10 puan ve bootstrap alt uç > 0 (ABD + AVR birleşik idi; burada yalnız ABD, bilgi)"},
    "gelecek_denetim": {"ornek": 60, "tohum": 124,
                        "tanim": "kos: rastgele 60 sinyal; seri t'de kesilir, aynı tarama; t'de eşleşme ve aynı 8 ölçü yoksa koşu DURUR"},
    "karar": "OC_ESIK 'etiket' (oc_etiket) yalnız L=20 olaylarıyla (tek ana hipotez; çoklu karşılaştırma yok); AVR'de görülmemiş veri yok -> "
             "en iyi etiket 'EMARE (ABD-ADAY; AVR verisi yok)'. L=10, kendi ölçüsü ve dönem kırılımları BİLGİ (iddia üretmez). "
             "İleri test cümlesi: ABD 2023 ve 2024-26 karar hücrelerinin ikisi TUTAR -> 'tuttu (ABD-ADAY)'; bir hücre TUTAR -> 'kısmen (EMARE)'; "
             "TUTAR yok ve hücreler TUTMADI (güç yeterli) -> 'tutmadı (İZ DEĞİL)'; aksi 'ölçülemedi (ÖLÇÜLEMEDİ)'",
    "eski_kayit": ["Ç123", "Ç124", "Ç175"],
}

II_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "OC eşleri (aynı giriş günü, aynı pazar, 60 gün momentum beşliği x 20 gün likidite üçlüsü; 200 plasebo portföy); kendi "
                   "ölçüsünde OYNAKLIK EŞLİ rastgele taban (aynı yıl, aynı 20 gün oynaklık dilimi +-0,05; H065 dersi). Mekanik üstünlük: "
                   "eşleşen bölgeler oynak (Ç124: 20 günde +-%8'e ulaşan %98) -> ana karar OC 60 gün eşli farkla; kendi ölçü oynaklık eşli"),
    "K2": ("EVET", "fi_k23_parmak yalnız geriye bakan pencereler (rolling / ewm / shift); 'n < L+200' toplam uzunluk şartı SAPMA-1 ile t'ye "
                   "indirildi; cetvel Ç124'te dondurulmuş sabit (ham ölçü aralıkları), görülmemiş verinin sonucundan bağımsız; kos'ta 60 sinyal "
                   "seri t'de kesilerek yeniden taranır (test_intem_ileri 'gelecek' + gerçek veri denetimi); k34 evrene ilk_giris'ten (OC)"),
    "K3": ("EVET", "görülmemiş hisseler OC temiz verisinde taranır (H>L, V>0 olmayan bar atılmış; SAPMA-2); OC sinyal barı geçersizse olay düşer; "
                   "K45 High / Low yalnız geçerli barlarda"),
    "K4": ("EVET", "OC 60 birleşik takvim günü tekilleştirme (SAPMA-3); n bağımsız olay; hücrede medyan; K45 aynı olay kümesi"),
    "K5": ("EVET", "giriş = OC: t'den sonraki ilk geçerli bar AÇILIŞI (pencere t kapanışında biter); K45 de bu açılıştan"),
    "K6": ("EVET", "tek kip: V_ABD / k34_yahoo düzeltilmiş fiyat (OC); oranlar birimden bağımsız; OC geçmiş bölünme şüphesi süzgeci; ABD tek pazar (USD)"),
    "K7": ("EVET", "k34 nakdi biten şirketler BUGÜN işlem görenler (batanlar YOK, Tiingo YOK) -> getiriler yukarı, -%50 olasılığı aşağı yanlı; "
                   "raporda yazılır; görülmemiş evren nakit yakan küçük şirketler (Ç124 evreninden farklı nüfus) -> sınır"),
    "K8": ("EVET", "OC hücreleri (n < 30 ÖLÇÜLEMEDİ; iki yarı aynı yön; İZ DEĞİL yalnız n >= 1.000 ya da güç %80); tek ana hipotez (L20) -> "
                   "BH gerekmez; L10 / kendi ölçü / dönem bilgi; olay sayımı ön kayıtta getiri hesaplanmadan"),
    "K9": ("EVET", "II_ESIK sha + FI_K44 / FI_K45 sha + FON_IZI kural kodu sha + INTEM_ILERI.py sha + hedef / cetvel sha + olay sha + OC üç satırı "
                   "ön kayıtta; ön kayıt ve modül commit + push SONRA kos; kos git kapısı + sha eşitliği; eşik yok, sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "metin / haber / KAP ayrıştırma yok; yalnız OHLCV; Ç124 eşleşmeleri ham csv'den birebir yeniden üretilir; 3 olay ham veriden elle (rapor)"),
    "K11": ("EVET", "satır verisi /tmp/intem_ileri/intem_olay.csv.gz; >= 2 hücre bağımsız kodla yeniden üretilir; eski sayılar IZ_KARNE metninden alıntı (denetlenir)"),
    "K12": ("EVET", "etiketler yalnız OC kuralıyla; fiyat değişimi (komisyon yok); kendi ölçü ve L10 'bilgi', iddia değil; sayı ve yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_ii; yasak dosyalara dokunulmaz (git diff --stat); e-posta / anahtar taraması testte; ücretli veri yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ileri test ölçümü"),
}

II_ESKI_SATIR = [   # IZ_KARNE notlarından aynen alınan sayılar (ii_eski_dogrula her birinin metinde geçtiğini denetler)
    ("Ç124", "20 bar +%8 önce, ABD (oynaklık eşli rastgele)", "ABD %54,9 / %43,2 (rastgele %43,7 / %43,2; fark +11,2 puan, aralık +6 .. +17)"),
    ("Ç124", "20 bar +%8 önce, AVR", "AVR %50,4 / %41,9 (rastgele %35,5 / %35,9; +15,0, aralık +6 .. +24)"),
    ("Ç124", "dönem sınaması ABD / AVR", "fark ABD 2016-22 +12,7 (n 240), 2023 +3,1 (n 26), 2024-26 +6,3 (n 51); AVR 2016-22 +15,0 (n 92)"),
    ("Ç124", "kutu yukarı kırılımında al kuralı", "Kutu yukarı kırılımında al kuralı: ABD +10,9 (aralık 0'a değiyor), AVR +1,9 -> tutmadı"),
    ("Ç123", "K44 60 gün eşli fark ABD 20 bar (2016-22 / 2023 / 2024-26)", "ABD -%4 / -%9 / -%1"),
]


class IIHata(RuntimeError):
    """Durdurucu hata: ön kayıt yok / sha tutmuyor / git'e işlenmemiş / Ç124 yeniden üretilemedi / olay kümesi farklı / geleceğe bakma."""


# ================================================================ 0) ORTAK
_II_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _ii_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ii_sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _ii_F():
    import FON_IZI as F   # kütüphane olarak; FON_IZI kendi çakışma kapısını taşır
    return F


def _ii_OC():
    import ORTAK_CETVEL as OC
    return OC


def ii_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return _ii_sha(json.dumps(E or II_ESIK, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def ii_fi_param_sha() -> str:
    """FI_K44 + FI_K45 + FI_K23 parametre sözlüklerinin sha'sı (kural eşikleri)."""
    F = _ii_F()
    return _ii_sha(json.dumps({"FI_K44": F.FI_K44, "FI_K45": F.FI_K45, "FI_K23": F.FI_K23}, sort_keys=True, default=str).encode("utf-8"))


II_FI_FONK = ("fi_k23_parmak", "fi_k44_havuz", "fi_k44_yuzdelik", "fi_k44_eslesme", "fi_k27_tekil", "fi_k45_ilk_hedef",
              "fi_k45_kutu_cikis", "fi_k45_olc", "fi_k45_rastgele_oynak", "fon_izi_k45")


def ii_fi_kod_sha() -> str:
    """Kural kodu (FON_IZI'deki kullanılan fonksiyonların kaynağı) sha'sı: kod değişirse koşu durur."""
    F = _ii_F()
    return _ii_sha("".join(inspect.getsource(getattr(F, f)) for f in II_FI_FONK).encode("utf-8"))


def ii_kod_sha(yol: Optional[str] = None) -> str:
    with open(yol or II_YOL["kod"], "rb") as f:
        return _ii_sha(f.read())


def ii_olay_sha(S: pd.DataFrame) -> str:
    if not len(S):
        return _ii_sha(b"")
    X = S[["pencere", "sembol", "tarih"]].copy(); X["tarih"] = pd.to_datetime(X.tarih).dt.strftime("%Y-%m-%d")
    X = X.sort_values(["pencere", "sembol", "tarih"]).reset_index(drop=True)
    return _ii_sha(X.to_csv(index=False).encode("utf-8"))


def _ii_donem_t(t: Any, E_oc: Dict[str, Any]) -> np.ndarray:
    t = pd.to_datetime(pd.Series(t)).reset_index(drop=True); out = np.full(len(t), "dışı", dtype=object)
    for ad, a, b in E_oc["donem"]:
        out[((t >= a) & (t <= b)).to_numpy()] = ad
    return out


def _ii_ham(pazar: str) -> Dict[str, pd.DataFrame]:
    OC = _ii_OC(); yol = os.path.join(OC.OC_YOL["veri"], f"V_{pazar}.pkl")
    if not os.path.exists(yol):
        OC.oc_veri(pazar)   # yoksa islenmis-veri dalından açar
    ham = pd.read_pickle(yol)
    if isinstance(ham, dict) and "veri" in ham and isinstance(ham["veri"], dict):
        ham = ham["veri"]
    return ham


# ================================================================ 1) CETVEL (Ç124 havuzu) ve yeniden üretim
def ii_hedef(VB: Dict[str, pd.DataFrame], L: int) -> pd.Series:
    """INTEM parmak izi (8 ölçü) — K44 ile aynı çağrı."""
    F = _ii_F(); K = F.FI_K44
    return F.fi_k23_parmak(VB[K["sembol"]], L).loc[pd.Timestamp(K["bitis"]), list(K["olcu"])].astype(float)


def ii_cetvel(VA: Dict[str, pd.DataFrame], hedef: pd.Series, L: int) -> Dict[str, Any]:
    """Ç124 ABD havuzu (cetvel), hedef yüzdelik, ham ölçü aralıkları (bilgi) ve Ç124 eşleşmelerinin yeniden üretimi."""
    F = _ii_F(); K = F.FI_K44; band = II_ESIK["band"][str(L)]
    H = F.fi_k44_havuz(VA, L, K)
    hy = F.fi_k44_yuzdelik(H, hedef.to_frame().T, K).iloc[0]
    E = F.fi_k44_eslesme(H, hy, band, K)
    if len(E) < K["n_min"]:
        raise IIHata(f"Ç124 havuzunda L{L} eşleşme {len(E)} < {K['n_min']}: band_genis tetiklenirdi, Ç124 kaydıyla çelişir")
    aralik = {k: (float(E[k].min()), float(E[k].max())) for k in K["olcu"]}
    E = E.rename(columns={"tarih": "gun"})[["sembol", "gun"]]
    gun = pd.DatetimeIndex(sorted(set().union(*[d.index for d in VA.values()]))); j = gun.searchsorted(pd.DatetimeIndex(E.gun), side="right")
    ok = j < len(gun); E = E[ok].assign(giris=gun[j[ok]]); E = E[[g in VA[s].index for s, g in zip(E.sembol, E.giris)]]
    E = E.sort_values(["giris", "sembol"]).assign(_b=True).reset_index(drop=True); E = F.fi_k27_tekil(E, "_b", VA, K["ayri"])
    return {"H": H, "hy": hy, "aralik": aralik, "es_ham": E, "band": band}


def ii_cetvel_dogrula(C: Dict[int, Dict[str, Any]], hedefler: Dict[int, pd.Series]) -> Dict[str, Any]:
    """k44_parmak / k44_eslesme ile birebir eşitlik; tutmazsa IIHata."""
    F = _ii_F(); K = F.FI_K44
    PI = pd.read_csv(II_YOL["k44_parmak"]); E0 = pd.read_csv(II_YOL["k44_eslesme"], parse_dates=["gun", "giris"]); out = {}
    for L, c in C.items():
        p = PI[PI.pencere == L][list(K["olcu"])].to_numpy(float)[0]
        if not np.allclose(p, hedefler[L].to_numpy(float), rtol=1e-9, atol=1e-12):
            raise IIHata(f"INTEM izi L{L} k44_parmak.csv ile tutmuyor")
        o = E0[(E0.pazar == "ABD") & (E0.pencere == L)]
        if not np.allclose(o.band.unique(), [c["band"]]):
            raise IIHata(f"Ç124 ABD L{L} bandı {o.band.unique()} != {c['band']}")
        a = set(zip(c["es_ham"].sembol, pd.to_datetime(c["es_ham"].gun))); b = set(zip(o.sembol, o.gun))
        if a != b:
            raise IIHata(f"Ç124 ABD L{L} eşleşmeleri yeniden üretilemedi: yeni {len(a)}, Ç124 {len(b)}, ortak {len(a & b)}")
        out[str(L)] = {"c124_n": len(b), "yeniden": len(a), "ortak": len(a & b), "parmak_esit": True}
    return out


def ii_cetvel_sha(C: Dict[int, Dict[str, Any]], hedefler: Dict[int, pd.Series]) -> str:
    d = {str(L): {"hedef": [round(float(x), 12) for x in hedefler[L]], "hy": [round(float(x), 12) for x in c["hy"]], "band": c["band"],
                  "havuz_n": int(len(c["H"]))} for L, c in C.items()}
    return _ii_sha(json.dumps(d, sort_keys=True).encode("utf-8"))


# ================================================================ 2) GÖRÜLMEMİŞ VERİDE TARAMA
def ii_pencereler(d: pd.DataFrame, L: int) -> pd.DataFrame:
    """Bir hissenin L barlık pencere ölçüleri (fi_k23_parmak) + SAPMA-1 (i >= L + 199); NaN ölçülü pencere atılır."""
    F = _ii_F(); K = F.FI_K44
    P = F.fi_k23_parmak(d, L)
    if not len(P):
        return pd.DataFrame(columns=["tarih", "i"] + list(K["olcu"]))
    P = P[P["i"] >= L + 199]
    return P[["i"] + list(K["olcu"])].rename_axis("tarih").reset_index().dropna(subset=list(K["olcu"])).reset_index(drop=True)


def ii_esle(X: pd.DataFrame, c: Dict[str, Any]) -> np.ndarray:
    """X pencerelerinin sabit cetvele göre yüzdeliği; sekiz ölçü hedef +-band içinde mi."""
    F = _ii_F(); K = F.FI_K44
    if not len(X):
        return np.zeros(0, bool)
    Y = F.fi_k44_yuzdelik(c["H"], X, K); m = np.ones(len(X), bool)
    for k in K["olcu"]:
        y = Y[k].to_numpy(); m &= (y >= c["hy"][k] - c["band"]) & (y <= c["hy"][k] + c["band"])
    return m


def ii_gorulmemis(V_oc: Dict[str, Any], VA: Dict[str, pd.DataFrame]) -> List[str]:
    return sorted(s for s, k in V_oc["kaynak"].items() if k == "k34_yahoo" and s not in VA)


def ii_tara(V_oc: Dict[str, Any], semboller: List[str], C: Dict[int, Dict[str, Any]]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Görülmemiş hisselerde eşleşen pencere bitişleri. Döner: sinyal tablosu (pencere, sembol, tarih) ve sayım."""
    say: Dict[str, Any] = {"hisse": len(semboller), "hata": 0}; parca = []
    for L, c in C.items():
        W = []
        for s in semboller:
            try:
                X = ii_pencereler(V_oc["V"][s], L)
            except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer (sayımda)
                say["hata"] += 1; iilog.warning("L%d %s atlandı: %s", L, s, ex); continue
            if len(X):
                W.append(X.assign(sembol=s))
        W = pd.concat(W, ignore_index=True) if W else pd.DataFrame(columns=["tarih", "i", "sembol"])
        m = ii_esle(W, c)
        say[f"L{L}_pencere"] = int(len(W)); say[f"L{L}_eslesme"] = int(m.sum())
        parca.append(W[m][["sembol", "tarih"]].assign(pencere=L))
        iilog.info("L%d: %d pencere, %d eşleşme (görülmemiş %d hisse)", L, len(W), int(m.sum()), len(semboller))
    S = pd.concat(parca, ignore_index=True); S["tarih"] = pd.to_datetime(S.tarih); S["pazar"] = "ABD"
    return S[["pencere", "pazar", "sembol", "tarih"]].sort_values(["pencere", "sembol", "tarih"]).reset_index(drop=True), say


def ii_ham_sayim(semboller: List[str], C: Dict[int, Dict[str, Any]]) -> Dict[str, int]:
    """SAPMA-2 bilgisi: aynı hisselerin HAM k34_yahoo serisinde eşleşme sayısı (getiri yok)."""
    OC = _ii_OC(); Y = pd.read_pickle(os.path.join(OC.OC_YOL["veri2"], "k34_yahoo.pkl")); out = {}
    for L, c in C.items():
        W = []
        for s in semboller:
            try:
                d = Y[s].copy()
                if isinstance(d.columns, pd.MultiIndex):
                    d.columns = d.columns.get_level_values(0)
                X = ii_pencereler(d[["Open", "High", "Low", "Close", "Volume"]].astype(float), L)
            except Exception:   # noqa: BLE001 — bilgi sayımı
                continue
            if len(X):
                W.append(X)
        W = pd.concat(W, ignore_index=True) if W else pd.DataFrame()
        out[f"L{L}"] = int(ii_esle(W, c).sum()) if len(W) else 0
    return out


def ii_gelecek_denetimi(V_oc: Dict[str, Any], S: pd.DataFrame, C: Dict[int, Dict[str, Any]], E: Dict[str, Any] = II_ESIK) -> Dict[str, Any]:
    """Rastgele örnek sinyal: seri t'de kesilir, aynı tarama; t'de eşleşme yoksa IIHata."""
    G = E["gelecek_denetim"]; rng = np.random.default_rng(G["tohum"])
    sec = S.iloc[rng.choice(len(S), min(G["ornek"], len(S)), replace=False)] if len(S) else S; bozuk = []
    for r in sec.itertuples():
        X = ii_pencereler(V_oc["V"][r.sembol].loc[:r.tarih], int(r.pencere))
        X = X[X.tarih == r.tarih]
        if len(X) != 1 or not ii_esle(X, C[int(r.pencere)])[0]:
            bozuk.append(f"{r.sembol} {pd.Timestamp(r.tarih).date()} L{r.pencere}")
    if bozuk:
        raise IIHata(f"geleceğe bakma denetimi TUTMADI: {bozuk[:5]}")
    return {"ornek": int(len(sec)), "bozuk": bozuk}


# ================================================================ 3) KENDİ ÖLÇÜSÜ (K45; fon_izi_k45 istatistiği birebir + SAPMA-4)
def ii_tam(V: Dict[str, pd.DataFrame], X: pd.DataFrame, tam: int) -> pd.DataFrame:
    """Giriş + tam bar hissenin verisinde olan satırlar (SAPMA-4)."""
    if not len(X):
        return X
    k = [(s in V and g in V[s].index and int(V[s].index.get_loc(g)) + tam <= len(V[s])) for s, g in zip(X.sembol, X.giris)]
    return X[np.array(k, bool)].reset_index(drop=True)


def ii_k45(V: Dict[str, pd.DataFrame], E: pd.DataFrame, tam: Optional[int] = None, K: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """fon_izi_k45'in tek (pazar, pencere) satırı, aynı yapı taşları ve aynı istatistikle; tam verilirse olay ve rastgele satırlara
    tam pencere süzgeci (SAPMA-4). tam=None iken fon_izi_k45 ile birebir (test)."""
    F = _ii_F(); K = K or F.FI_K45
    def oran(X: pd.DataFrame, kol: str, kazanan: str, kaybeden: str) -> Tuple[float, float, int]:
        n = len(X); return (float((X[kol] == kazanan).mean()) if n else np.nan, float((X[kol] == kaybeden).mean()) if n else np.nan, n)
    E = E[["sembol", "giris"]].assign(giris=pd.to_datetime(E.giris))
    if tam is not None:
        E = ii_tam(V, E, tam)
    if not len(E):
        return {"n": 0}
    X = F.fi_k45_olc(V, E, K)
    R = []
    for t in range(K["tohum_n"]):
        Rr = F.fi_k45_rastgele_oynak(V, E, t)
        if tam is not None:
            Rr = ii_tam(V, Rr, tam)
        R.append(F.fi_k45_olc(V, Rr, K))
    row: Dict[str, Any] = {"n": len(X), "n_rast": int(np.mean([len(r_) for r_ in R]))}
    for e in K["esik"]:
        kol = f"ilk_{int(e*100)}"; a, b, _ = oran(X, kol, "arti", "eksi"); ra = np.mean([oran(r_, kol, "arti", "eksi")[0] for r_ in R]); rb = np.mean([oran(r_, kol, "arti", "eksi")[1] for r_ in R])
        row.update({f"arti{int(e*100)}": a, f"eksi{int(e*100)}": b, f"arti{int(e*100)}_rast": ra, f"eksi{int(e*100)}_rast": rb, f"fark{int(e*100)}": a - ra})
        if e == K["ana_esik"] and len(X) >= 10:
            rng = np.random.default_rng(45); v = (X[kol] == "arti").to_numpy(float)
            bs = [rng.choice(v, len(v)).mean() - ra for _ in range(2000)]; row["fark8_alt95"] = float(np.quantile(bs, 0.025)); row["fark8_ust95"] = float(np.quantile(bs, 0.975))
    row.update({"kutu_yukari": float((X.kutu == "yukari").mean()), "kutu_asagi": float((X.kutu == "asagi").mean()),
                "kutu_gun_ortanca": float(X.kutu_gun.median()), "kutu_yukari_rast": float(np.mean([(r_.kutu == "yukari").mean() for r_ in R]))})
    Xu = X[X.kutu == "yukari"]; Xd = X[X.kutu == "asagi"]; Ru = pd.concat([r_[r_.kutu == "yukari"] for r_ in R]); Rd = pd.concat([r_[r_.kutu == "asagi"] for r_ in R])
    row.update({"yukari_sonra_arti8": float((Xu.kosullu == "arti").mean()) if len(Xu) else np.nan, "yukari_sonra_eksi8": float((Xu.kosullu == "eksi").mean()) if len(Xu) else np.nan,
                "yukari_n": len(Xu), "yukari_sonra_arti8_rast": float((Ru.kosullu == "arti").mean()) if len(Ru) else np.nan,
                "asagi_sonra_eksi8": float((Xd.kosullu == "eksi").mean()) if len(Xd) else np.nan, "asagi_sonra_arti8": float((Xd.kosullu == "arti").mean()) if len(Xd) else np.nan,
                "asagi_n": len(Xd), "asagi_sonra_eksi8_rast": float((Rd.kosullu == "eksi").mean()) if len(Rd) else np.nan})
    if len(Xu) >= 10 and len(Ru):
        rng = np.random.default_rng(46); v = (Xu.kosullu == "arti").to_numpy(float); ra = float((Ru.kosullu == "arti").mean())
        bs = [rng.choice(v, len(v)).mean() - ra for _ in range(2000)]; row["kosullu_fark"] = float(v.mean() - ra); row["kosullu_alt95"] = float(np.quantile(bs, 0.025))
    row["_olay"] = X
    return row


def ii_k45_kural(r: Dict[str, Any]) -> str:
    """Ç124 kendi kuralı (ABD tek başına; bilgi): n >= 30, fark8 >= +10 puan, alt uç > 0."""
    F = _ii_F(); K = F.FI_K45
    if not r or r.get("n", 0) < K["n_min"]:
        return "n < 30"
    ok = r.get("fark8", np.nan) >= K["fark_esik"] and r.get("fark8_alt95", np.nan) > 0
    return "TUTAR" if ok else "TUTMAZ"


# ================================================================ 4) ESKİ KAYITLAR
def ii_eski_dogrula() -> List[Dict[str, Any]]:
    import IZ_KARNE as IK
    K = {k["kod"]: k.get("not", "") for k in IK.IK_KAYIT if k["kod"] in II_ESIK["eski_kayit"]}
    return [{"kod": kod, "ne": ne, "alinti": al, "metinde": al in K.get(kod, "")} for kod, ne, al in II_ESKI_SATIR]


# ================================================================ 5) ÖN KAYIT
def ii_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = II_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def ii_hazirla() -> Dict[str, Any]:
    """Ortak hazırlık (onkayit ve kos): ham veri, cetvel + doğrulama, OC veri, görülmemiş hisseler, tarama."""
    OC = _ii_OC(); warnings.filterwarnings("ignore", category=RuntimeWarning); warnings.filterwarnings("ignore", message="All-NaN")
    VB = _ii_ham("BIST"); VA = _ii_ham("ABD")
    pen = (II_ESIK["pencere_ana"], II_ESIK["pencere_bilgi"])
    hed = {L: ii_hedef(VB, L) for L in pen}; del VB
    C = {L: ii_cetvel(VA, hed[L], L) for L in pen}
    dog = ii_cetvel_dogrula(C, hed)
    Voc = OC.oc_veri("ABD")
    sem = ii_gorulmemis(Voc, VA)
    E0 = pd.read_csv(II_YOL["k44_eslesme"]); ort = sorted(set(E0[E0.pazar == "ABD"].sembol) & set(sem))
    if ort:
        raise IIHata(f"görülmemiş sanılan hisseler Ç124 eşleşmelerinde var: {ort[:5]}")
    n_va = len(VA); del VA
    S, say = ii_tara(Voc, sem, C)
    return {"hedef": hed, "C": C, "dogrula": dog, "V": Voc, "sem": sem, "S": S, "say": say, "n_va": n_va,
            "cetvel_sha": ii_cetvel_sha(C, hed)}


def ii_oc_sayim(Voc: Dict[str, Any], S: pd.DataFrame) -> Tuple[Dict[int, Dict[str, int]], Dict[int, Dict[str, int]], Dict[str, Any]]:
    """OC süzgeçlerinden sonra olay sayısı (getiri / eşli fark HESAPLANMAZ; yalnız oc_olay_hazirla) ve K45 tam pencere sayısı."""
    OC = _ii_OC(); P = OC.oc_panel(Voc); out, k45 = {}, {}
    for L in sorted(S.pencere.unique(), reverse=True):
        X, say = OC.oc_olay_hazirla(S[S.pencere == L][["sembol", "tarih", "pazar"]], P)
        c = {d: int((X.donem == d).sum()) for d, _a, _b in OC.OC_ESIK["donem"]}; c["toplam"] = int(len(X)); c["_say"] = say
        out[int(L)] = c
        Xt = ii_tam(Voc["V"], X.rename(columns={})[["sembol", "giris"]], II_ESIK["k45"]["tam_pencere"]) if len(X) else X
        dn = _ii_donem_t(Xt.giris, OC.OC_ESIK) if len(Xt) else np.array([])
        k45[int(L)] = {**{d: int((dn == d).sum()) for d, _a, _b in OC.OC_ESIK["donem"]}, "toplam": int(len(Xt))}
    return out, k45, P


def ii_onkayit_metni(H: Dict[str, Any], ocs: Dict[int, Dict[str, int]], k45s: Dict[int, Dict[str, int]], ham: Dict[str, int]) -> str:
    OC = _ii_OC(); F = _ii_F(); S = H["S"]; say = H["say"]
    dn = _ii_donem_t(S.tarih, OC.OC_ESIK); don = [a for a, _b, _c in OC.OC_ESIK["donem"]]
    eski = ii_eski_dogrula()
    s = [f"# INTEM İLERİ TEST — ÖN KAYIT ({II_SURUM})", "",
         f"Yazım: {_ii_simdi()}. Bu dosya ölçümden ÖNCE yazıldı. Bu modülde görülmemiş veride hiçbir getiri / eşli fark / olasılık / K45 "
         "hedef oranı HESAPLANMADI; yalnız Ç124 cetveli yeniden üretildi, görülmemiş hisseler tarandı ve olaylar sayıldı. Ön kayıt + modül "
         "commit + push edilir, SONRA `python INTEM_ILERI.py kos`.", "",
         "Cemal (14 Kas 2026): \"önceki aşamalardan çıkan kuralları DEĞİŞTİRMEDEN, görülmemiş veride dene\"; \"her aşamada aynı ölçüm "
         "kriterleri; sonucu beğenmediğimiz için eşikle oynanmaz\".", "",
         "İleri test edilecek başka kural yok: Aşama 2 (K24 iki evre çöl) ve Aşama 4 (düzgün dip vs çöl) ORTAK CETVEL ile ÖLÇÜLEMEDİ / "
         "TUTMADI çıktı, kural üretmedi; Aşama 3 (D9) sonucu gelirse ana model ayrı iş açar. Konu: sıkışma ailesindeki tek EMARE Ç124.", "",
         "## 1. Kural (DEĞİŞMEZ; FON_IZI içe alınır)", "",
         "- K44 INTEM parmak izi: `fi_k23_parmak(d, L)` sekiz ölçü (dusus, egim, mum, konum, rsi, bbw, hacim, yesil); INTEM 2026-10-09 bitişli "
         "L = 20 (ana) ve L = 10 (bilgi) barlık pencere.",
         "- K44 birebir eşleşme: sekiz ölçünün pazar havuzundaki yüzdeliği INTEM yüzdeliğinin +-band içinde (ABD Ç124: 0,125). Cetvel = Ç124 "
         "ABD havuzu (V_ABD ham, bütün L barlık pencereler); görülmemiş pencereler bu SABİT cetvele göre yüzdeliğe çevrilir.",
         "- K45 kendi ölçüsü: girişten (açılış) ilk +-%5 / 8 / 12 hangisi önce (20 gün, High / Low); kutu (son 10 bar) çıkışı; yukarı çıkışta "
         "+%8 / -%8 koşullu; oynaklık eşli rastgele taban (10 tohum).", "",
         "```json", json.dumps({"FI_K44": F.FI_K44, "FI_K45": F.FI_K45}, sort_keys=True), "```", "",
         "INTEM hedef ölçüleri ve Ç124 ABD cetvelindeki hedef yüzdelikleri:", "",
         "| L | " + " | ".join(F.FI_K44["olcu"]) + " |", "|---|" + "---|" * len(F.FI_K44["olcu"])]
    for L, c in H["C"].items():
        s.append(f"| {L} ölçü | " + " | ".join(f"{H['hedef'][L][k]:.4f}" for k in F.FI_K44["olcu"]) + " |")
        s.append(f"| {L} yüzdelik | " + " | ".join(f"{c['hy'][k]:.4f}" for k in F.FI_K44["olcu"]) + " |")
        s.append(f"| {L} ham aralık (Ç124 eşleşmelerinde min..maks, bilgi) | " + " | ".join(f"{a:.3g}..{b:.3g}" for a, b in c["aralik"].values()) + " |")
    s += ["", "## 2. Görülmemiş veri (tam liste)", ""]
    s += [f"- (a) Avrupa: {II_ESIK['gorulmemis']['a_avrupa']}.",
          f"- (b) ABD: {II_ESIK['gorulmemis']['b_abd']}. Sayı: {len(H['sem'])} hisse (Ç124 evreni V_ABD {H['n_va']} hisse; k44_eslesme ABD "
          "sembolleriyle kesişim 0, denetlendi).",
          f"- (c) Dönem: {II_ESIK['gorulmemis']['c_donem']}.",
          f"- Örtüşme: {II_ESIK['gorulmemis']['ortusme']}.", "",
          "**Görülmemiş veri yalnız (b): ABD k34 ekindeki nakit yakan, bugün işlem gören 2021+ şirketler. Avrupa görülmüş olduğu için AVR karar "
          "hücreleri bu ileri testte BOŞTUR; en iyi etiket 'EMARE (ABD-ADAY; AVR verisi yok)' olabilir.**", "",
          "Ç124 yeniden üretimi (cetvelin doğru kurulduğunun kanıtı):", "", "| L | Ç124 ABD eşleşme | yeniden üretilen | ortak | INTEM izi k44_parmak ile aynı |",
          "|---|---|---|---|---|"]
    s += [f"| {L} | {v['c124_n']} | {v['yeniden']} | {v['ortak']} | {'EVET' if v['parmak_esit'] else 'HAYIR'} |" for L, v in H["dogrula"].items()]
    s += ["", "## 3. Mühür satırları", "", "### ORTAK CETVEL (aynen; OC.oc_kapi_satirlari())", "", OC.oc_kapi_satirlari(), "", "### Bu aşama", "",
          f"II_ESIK_SHA: `{ii_esik_sha()}`", f"FI_PARAM_SHA: `{ii_fi_param_sha()}`", f"FI_KOD_SHA: `{ii_fi_kod_sha()}`",
          f"II_KOD_SHA: `{ii_kod_sha()}`", f"HEDEF_CETVEL_SHA: `{H['cetvel_sha']}`", f"OLAY_SHA: `{ii_olay_sha(S)}`", "",
          "- FI_PARAM_SHA = sha256(FI_K44 + FI_K45 + FI_K23 kanonik JSON); FI_KOD_SHA = sha256(" + ", ".join(II_FI_FONK) + " kaynak kodu); "
          "II_KOD_SHA = sha256(INTEM_ILERI.py bayt); HEDEF_CETVEL_SHA = sha256(INTEM ölçüleri, hedef yüzdelikleri, bant, havuz n); OLAY_SHA = "
          "sha256(pencere, sembol, sinyal tarihi sıralı csv). kos hepsini yeniden hesaplar; biri farklıysa DURUR.", "",
          "### II_ESIK (tam metin)", "", "```json", json.dumps(II_ESIK, ensure_ascii=False, indent=1, sort_keys=True), "```", "",
          "## 4. Sapmalar (sonuç görülmeden)", ""] + [f"- {x}" for x in II_ESIK["sapma"]]
    s += ["", "Ham (k34_yahoo temizlenmemiş) / temiz (OC) eşleşme sayısı (SAPMA-2 etkisi; getiri yok): " +
          "; ".join(f"{k} ham {v} / temiz {say.get(k + '_eslesme', '-')}" for k, v in ham.items()), "",
          "## 5. Ölçüm ve karar", "",
          "- Ana: L = 20 sinyalleri -> `OC.oc_olc(olaylar, {'ABD': panel})`; rapor `OC.oc_rapor`. Bilgi: L = 10 aynı yolla.",
          f"- Karar: {II_ESIK['karar']}.",
          f"- Kendi ölçüsü (bilgi): {II_ESIK['k45']['veri']}; {II_ESIK['k45']['donem']}; {II_ESIK['k45']['kural_kiyas']}.",
          "- Eski sonuçlar (yeniden ölçülmez; IZ_KARNE metninden alıntı):", ""]
    s += [f"  - {e['kod']}: {e['ne']}: \"{e['alinti']}\" (IZ_KARNE metninde: {'EVET' if e['metinde'] else 'HAYIR'})" for e in eski]
    s += ["", "## 6. OLAY SAYIMI (getiri hesaplanmadan)", "",
          f"Tarama: {say['hisse']} görülmemiş hisse, okunamayan {say['hata']}; " +
          "; ".join(f"L{L}: {say.get(f'L{L}_pencere')} pencere, {say.get(f'L{L}_eslesme')} eşleşen pencere" for L in H["C"]), "",
          "Eşleşen pencereler, sinyal günü t'ye göre dönem (tekilleştirme öncesi):", "",
          "| L | " + " | ".join(don + ["dışı"]) + " | toplam |", "|---|" + "---|" * (len(don) + 2)]
    for L in H["C"]:
        m = (S.pencere == L).to_numpy()
        s.append(f"| {L} | " + " | ".join(str(int((m & (dn == d)).sum())) for d in don + ["dışı"]) + f" | {int(m.sum())} |")
    s += ["", "OC süzgeçlerinden sonra bağımsız olay (giriş dönemi; ORTAK CETVEL oc_olay_hazirla; ölçüme girecek n; r60 ölçülemeyenler "
          "kos'ta ayrıca düşer):", "", "| L | " + " | ".join(don) + " | toplam | düşmeler |", "|---|" + "---|" * (len(don) + 2)]
    for L, c in ocs.items():
        dus = ", ".join(f"{k} {v}" for k, v in c["_say"].items() if v and k != "girdi")
        s.append(f"| {L} | " + " | ".join(str(c[d]) for d in don) + f" | {c['toplam']} | girdi {c['_say']['girdi']}; {dus} |")
    s += ["", "K45 kendi ölçüsüne girecek olay (SAPMA-4 tam pencere):", "", "| L | " + " | ".join(don) + " | toplam |", "|---|" + "---|" * (len(don) + 1)]
    s += [f"| {L} | " + " | ".join(str(c[d]) for d in don) + f" | {c['toplam']} |" for L, c in k45s.items()]
    s += ["", "Beklenen güç (OC güç tablosu, δ +%5, OC sonrası n; L = 20 karar hücreleri):", "", "| Hücre | n | güç % | n < 30 ise |", "|---|---|---|---|"]
    for d in OC.OC_ESIK["karar_donem"]:
        n = ocs.get(II_ESIK["pencere_ana"], {}).get(d, 0)
        s.append(f"| ABD {d} | {n} | {OC.oc_guc_bak(n) * 100:.0f} | {'ÖLÇÜLEMEDİ (önceden belli)' if n < 30 else '-'} |")
    s += ["| AVR 2023 / 2024-26 | 0 | 0 | görülmemiş veri yok |", "",
          "Not: güç tablosuna göre n < 1.000 iken 'TUTMADI' (İZ DEĞİL) yazılamaz; TUTAR olmayan hücre ÖLÇÜLEMEDİ olur.", "",
          "Veri notları: " + "; ".join(H["V"]["not"]), "", ii_kontrol_tablosu(), "",
          "## Test", "", "`python test_intem_ileri.py` (sentetik: eşleşme = FON_IZI fi_k44_eslesme; sabit cetvel; geleceğe bakma: seri t'de "
          "kesilince aynı tespit; SAPMA-1; ii_k45 = fon_izi_k45 birebir; tam pencere süzgeci; cetvel çağrısı OC.oc_olc; kapı; çakışma kapısı; "
          "e-posta / anahtar yok).", ""]
    return "\n".join(s)


def ii_onkayit_yaz(cikti: Optional[str] = None, uzerine: bool = False) -> str:
    OC = _ii_OC(); cikti = cikti or II_YOL["cikti"]; os.makedirs(cikti, exist_ok=True)
    yol = os.path.join(cikti, II_DOSYA["onkayit"])
    if os.path.exists(yol):
        try:
            OC._oc_git_islenmis(yol); islenmis = True
        except OC.OCHata:
            islenmis = False
        if islenmis or not uzerine:
            raise IIHata(f"ön kayıt var ({yol}); git'e işlenmişse üzerine yazılmaz, işlenmemişse --uzerine-yaz")
    H = ii_hazirla()
    ham = ii_ham_sayim(H["sem"], H["C"])
    ocs, k45s, _P = ii_oc_sayim(H["V"], H["S"])
    metin = ii_onkayit_metni(H, ocs, k45s, ham)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _ii_oku(metin: str, ad: str) -> str:
    m = re.search(rf"^{ad}:\s*`([0-9a-f]{{64}})`", metin, flags=re.M)
    if not m:
        raise IIHata(f"ön kayıtta {ad} satırı yok")
    return m.group(1)


def ii_kapi(onkayit_yolu: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    """Koşu kapısı: OC.oc_kapi (kontrol listesi + cetvel / kod / güç sha + git) + bu aşamanın sha'ları + modül git'te işlenmiş / değişmemiş."""
    OC = _ii_OC(); yol = onkayit_yolu or os.path.join(II_YOL["cikti"], II_DOSYA["onkayit"])
    try:
        out = OC.oc_kapi(yol, git=git)
    except OC.OCHata as ex:
        raise IIHata(f"OC kapısı kapalı: {ex}")
    metin = open(yol, encoding="utf-8").read()
    simdi = {"II_ESIK_SHA": ii_esik_sha(), "FI_PARAM_SHA": ii_fi_param_sha(), "FI_KOD_SHA": ii_fi_kod_sha(), "II_KOD_SHA": ii_kod_sha()}
    for ad, v in simdi.items():
        o = _ii_oku(metin, ad)
        if o != v:
            raise IIHata(f"{ad} tutmuyor: ön kayıt {o[:12]}…, şimdi {v[:12]}… -> koşu DURDU")
    out.update(simdi); out["OLAY_SHA"] = _ii_oku(metin, "OLAY_SHA"); out["HEDEF_CETVEL_SHA"] = _ii_oku(metin, "HEDEF_CETVEL_SHA")
    if git:
        try:
            out["git_modul"] = OC._oc_git_islenmis(II_YOL["kod"])
        except OC.OCHata as ex:
            raise IIHata(str(ex))
    iilog.info("ii_kapi AÇIK (%s)", yol)
    return out


# ================================================================ 6) KOŞU
def ii_ileri_cumle(et: Dict[str, Any]) -> str:
    k = et.get("karar_hucre", {}); a = [k.get(f"ABD {d}") for d in ("2023", "2024-26")]
    if all(x == "TUTAR" for x in a):
        return "Ç124 kuralı görülmemiş veride TUTTU (ABD-ADAY; AVR görülmemiş verisi yok)"
    if any(x == "TUTAR" for x in a):
        return "Ç124 kuralı görülmemiş veride KISMEN tuttu (EMARE: tek dönem)"
    if all(x == "TUTMADI" for x in a):
        return "Ç124 kuralı görülmemiş veride TUTMADI (İZ DEĞİL; güç yeterli)"
    return "Ç124 kuralı görülmemiş veride ÖLÇÜLEMEDİ (n ya da güç yetersiz; iddia kapanmaz)"


def ii_kos(onkayit_yolu: Optional[str] = None, git: bool = True, cikti: Optional[str] = None) -> Dict[str, Any]:
    OC = _ii_OC(); t0 = time.time(); bas = _ii_simdi()
    K = ii_kapi(onkayit_yolu, git=git)
    H = ii_hazirla(); S = H["S"]
    if ii_olay_sha(S) != K["OLAY_SHA"]:
        raise IIHata("olay kümesi ön kayıttakinden farklı (OLAY_SHA) -> koşu DURDU")
    if H["cetvel_sha"] != K["HEDEF_CETVEL_SHA"]:
        raise IIHata("hedef / cetvel ön kayıttakinden farklı (HEDEF_CETVEL_SHA) -> koşu DURDU")
    GD = ii_gelecek_denetimi(H["V"], S, H["C"])
    iilog.info("geleceğe bakma denetimi: %d örnek, bozuk 0", GD["ornek"])
    Vd = H["V"]["V"]; H["C"] = None
    P = {"ABD": OC.oc_panel(H["V"])}
    R = {}
    for L in (II_ESIK["pencere_ana"], II_ESIK["pencere_bilgi"]):
        R[L] = OC.oc_olc(S[S.pencere == L][["sembol", "tarih", "pazar"]], P)
    P = None
    tam = II_ESIK["k45"]["tam_pencere"]; K45: List[Dict[str, Any]] = []; K45_olay = []
    for L in (II_ESIK["pencere_ana"], II_ESIK["pencere_bilgi"]):
        X = R[L]["olay"][["sembol", "giris", "donem"]]
        gruplar = [("2016-26 (hepsi)", X)] + ([(d, X[X.donem == d]) for d, _a, _b in OC.OC_ESIK["donem"]] if L == II_ESIK["pencere_ana"] else [])
        for ad, Xg in gruplar:
            r = ii_k45(Vd, Xg, tam) if len(Xg) else {"n": 0}
            if "_olay" in r:
                K45_olay.append(r.pop("_olay").assign(pencere=L, grup=ad))
            K45.append({"pencere": L, "grup": ad, **r, "kural": ii_k45_kural(r)})
            iilog.info("K45 L%d %s: n %s", L, ad, r.get("n"))
    os.makedirs(II_YOL["satir"], exist_ok=True)
    pd.concat([R[L]["olay"].assign(pencere=L) for L in R], ignore_index=True).to_csv(os.path.join(II_YOL["satir"], II_DOSYA["olay"]), index=False)
    S.to_csv(os.path.join(II_YOL["satir"], II_DOSYA["sinyal"]), index=False)
    if K45_olay:
        pd.concat(K45_olay, ignore_index=True).to_csv(os.path.join(II_YOL["satir"], II_DOSYA["k45"]), index=False)
    ana = R[II_ESIK["pencere_ana"]]
    J = {"surum": II_SURUM, "kos_bas_utc": bas, "kos_son_utc": _ii_simdi(), "sure_sn": round(time.time() - t0),
         "kapi": {k: v for k, v in K.items() if k != "kontrol"}, "dogrula": H["dogrula"], "gorulmemis_hisse": len(H["sem"]),
         "sayim_tarama": H["say"], "gelecek_denetim": GD,
         "etiket": ana["etiket"], "ileri_cumle": ii_ileri_cumle(ana["etiket"]),
         "hucre": {str(L): json.loads(R[L]["hucre"].to_json(orient="records", force_ascii=False)) for L in R},
         "olasilik": {str(L): json.loads(R[L]["olasilik"].to_json(orient="records", force_ascii=False)) for L in R},
         "sayim_oc": {str(L): R[L]["sayim"] for L in R}, "etiket_L10": R[II_ESIK["pencere_bilgi"]]["etiket"],
         "k45": json.loads(pd.DataFrame(K45).to_json(orient="records", force_ascii=False)), "eski": ii_eski_dogrula(),
         "cetvel_sha": ana["cetvel_sha"], "kod_sha": ana["kod_sha"],
         "oc_rapor": OC.oc_rapor(ana, "Ç124 INTEM kuralı, görülmemiş ABD (L = 20, ana)"),
         "oc_rapor_L10": OC.oc_rapor(R[II_ESIK["pencere_bilgi"]], "Ç124 INTEM kuralı, görülmemiş ABD (L = 10, bilgi)")}
    cikti = cikti or II_YOL["cikti"]; os.makedirs(cikti, exist_ok=True)
    with open(os.path.join(cikti, II_DOSYA["json"]), "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1, default=str)
    yol = ii_rapor_yaz(J, cikti)
    iilog.info("kos bitti: %s (%d sn)", yol, J["sure_sn"])
    return J


# ================================================================ 7) RAPOR
def _yz(x: Any, n: int = 1) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{x * 100:+.{n}f}".replace(".", ",")


def _py(x: Any, n: int = 1) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"%{x * 100:.{n}f}".replace(".", ",")


def _kz(x: Any, n: int = 2) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


def ii_duz_ozet(J: Dict[str, Any]) -> List[str]:
    H = pd.DataFrame(J["hucre"]["20"]); O = pd.DataFrame(J["olasilik"]["20"]); et = J["etiket"]
    s = ["## DÜZ DİL ÖZET", "", f"**{J['ileri_cumle']}.**", "",
         f"- Görülmemiş veri: yalnız ABD k34 ekinin {J['gorulmemis_hisse']} hissesi (nakit yakan, bugün işlem gören, 2021+). Avrupa Ç124'te "
         "kullanıldığı için görülmemiş değil; AVR karar hücreleri boş.",
         f"- ORTAK CETVEL genel etiket (L = 20): **{et['genel']}**; olasılık etiketi **{et['olasilik']}**."]
    for r in H.to_dict("records"):
        if r["pazar"] != "ABD":
            continue
        o = O[(O.pazar == r["pazar"]) & (O.donem == r["donem"])]; o = o.iloc[0].to_dict() if len(o) else {}
        s.append(f"- ABD {r['donem']}{' (keşif, bilgi)' if r['donem'] == '2016-22' else ''}: n {int(r['n'] or 0)}, 60 gün eşli fark "
                 f"{_yz(r.get('ort_fark'))} puan [%95 {_yz(r.get('alt95'))}, {_yz(r.get('ust95'))}], medyan {_yz(r.get('medyan_fark'))}; "
                 f"12 ayda +%100 eşlerin {_kz(o.get('up100_es_kat'))} katı, -%50 eşlerin {_kz(o.get('dn50_es_kat'))} katı (n250 {o.get('n250', 0)}) "
                 f"-> {r['durum']}.")
    k = [x for x in J["k45"] if x["pencere"] == 20]
    for x in k:
        if x.get("n", 0):
            s.append(f"- Ç124'ün kendi ölçüsü, {x['grup']}: 20 günde önce +%8 {_py(x.get('arti8'))} (oynaklık eşli rastgele {_py(x.get('arti8_rast'))}; "
                     f"fark {_yz(x.get('fark8'))} puan, %95 [{_yz(x.get('fark8_alt95'))}, {_yz(x.get('fark8_ust95'))}]), önce -%8 {_py(x.get('eksi8'))} "
                     f"(rastgele {_py(x.get('eksi8_rast'))}); n {x['n']} -> Ç124 kuralıyla {x['kural']} (bilgi).")
    s.append("- Eski Ç124 (görülmüş veri): ABD fark +11,2 puan (2016-22 +12,7 n 240; 2023 +3,1 n 26; 2024-26 +6,3 n 51), AVR +15,0.")
    s.append("- Hayatta kalma: görülmemiş hisseler bugün işlem gören nakit yakan şirketler; batanlar yok -> getiriler yukarı, -%50 olasılığı "
             "aşağı yanlı. Komisyon yok.")
    return s


def ii_rapor_md(J: Dict[str, Any]) -> str:
    s = [f"# INTEM İLERİ TEST — RAPOR ({J['surum']})", "",
         f"Koşu: {J['kos_bas_utc']} -> {J['kos_son_utc']} ({J['sure_sn']} sn). Ön kayıt git: {J['kapi'].get('git', {})}; modül git: "
         f"{J['kapi'].get('git_modul', {})}.", ""]
    s += ii_duz_ozet(J) + ["", J["oc_rapor"], ""]
    s += ["## Ç124'ün kendi ölçüsü (K45; bilgi, karar dışı; SAPMA-4 tam pencere)", "",
          "| L | grup | n | +%8 önce olay / rastgele | fark [%95] | -%8 önce olay / rastgele | +%5 fark | +%12 fark | kutu yukarı olay / rast | "
          "yukarı çıkış sonra +%8 olay / rast (n) | koşullu fark [alt] | Ç124 kuralı |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in J["k45"]:
        if not x.get("n"):
            s.append(f"| {x['pencere']} | {x['grup']} | 0 | - | - | - | - | - | - | - | - | {x['kural']} |"); continue
        s.append(f"| {x['pencere']} | {x['grup']} | {x['n']} | {_py(x.get('arti8'))} / {_py(x.get('arti8_rast'))} | {_yz(x.get('fark8'))} "
                 f"[{_yz(x.get('fark8_alt95'))}, {_yz(x.get('fark8_ust95'))}] | {_py(x.get('eksi8'))} / {_py(x.get('eksi8_rast'))} | "
                 f"{_yz(x.get('fark5'))} | {_yz(x.get('fark12'))} | {_py(x.get('kutu_yukari'))} / {_py(x.get('kutu_yukari_rast'))} | "
                 f"{_py(x.get('yukari_sonra_arti8'))} / {_py(x.get('yukari_sonra_arti8_rast'))} ({x.get('yukari_n')}) | "
                 f"{_yz(x.get('kosullu_fark'))} [{_yz(x.get('kosullu_alt95'))}] | {x['kural']} |")
    s += ["", "## Eski sonuçlarla kıyas (IZ_KARNE metninden alıntı; yeniden ölçülmedi)", "", "| Kayıt | Ne | Eski sonuç | metinde |", "|---|---|---|---|"]
    s += [f"| {e['kod']} | {e['ne']} | {e['alinti']} | {'EVET' if e['metinde'] else 'HAYIR'} |" for e in J["eski"]]
    s += ["", J["oc_rapor_L10"], "",
          "## Cetvel ve tarama", "", "| L | Ç124 ABD eşleşme | yeniden üretilen | ortak |", "|---|---|---|---|"]
    s += [f"| {L} | {v['c124_n']} | {v['yeniden']} | {v['ortak']} |" for L, v in J["dogrula"].items()]
    st = J["sayim_tarama"]
    s += ["", f"Tarama: {st['hisse']} görülmemiş hisse; L20 {st.get('L20_pencere')} pencere / {st.get('L20_eslesme')} eşleşme; L10 "
          f"{st.get('L10_pencere')} / {st.get('L10_eslesme')}. Geleceğe bakma denetimi: {J['gelecek_denetim']['ornek']} örnek, bozuk "
          f"{len(J['gelecek_denetim']['bozuk'])}.", "",
          "## Sınırlar", "",
          "- Görülmemiş veri yalnız ABD k34 ekidir: nakit yakan küçük şirketler (Ç124'ün V_ABD evreninden farklı nüfus); Avrupa görülmüş "
          "olduğundan AVR karar hücreleri boş; kullanılmamış dönem yok. Gerçek ileri test (yeni zaman) Mart 2027+ verisi ister (IK_ILERI).",
          "- Hayatta kalma: batanlar yok (Tiingo kullanılmadı); k34 hisseleri bugün işlem görenler.",
          "- Mekanik: eşleşen bölgeler oynak (Ç124 dersi); OC eşleri 60 gün momentum x likiditeyle eşlenir, oynaklıkla eşlenmez; kendi ölçü "
          "oynaklık eşli tabanla.",
          "- K45 rastgele havuzu V_ABD + k34 (Ç124'te V_ABD); 31.08.2026 kesiği nedeniyle tam pencere süzgeci (SAPMA-4).",
          "- L = 10, dönem kırılımları ve kendi ölçü bilgi; çoklu karşılaştırma düzeltmesi yapılmadı, iddia üretmez.", ""]
    return "\n".join(s)


def ii_rapor_yaz(J: Optional[Dict[str, Any]] = None, cikti: Optional[str] = None) -> str:
    cikti = cikti or II_YOL["cikti"]
    if J is None:
        J = json.load(open(os.path.join(cikti, II_DOSYA["json"]), encoding="utf-8"))
    metin = ii_rapor_md(J)
    if _II_EPOSTA.search(metin):
        raise IIHata("raporda e-posta deseni var; yazılmadı")
    yol = os.path.join(cikti, II_DOSYA["rapor"])
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


# ================================================================ ÇAKIŞMA KAPISI
def _cakisma_kontrol_ii(_once=_CK_ONCE_II, _dosya="INTEM_ILERI.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_II", "_CK_KAYIT", "_cakisma_kontrol_ii", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "inspect", "warnings", "_dt", "_yz", "_kz", "_py",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ii()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=II_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "sha"])
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(ii_onkayit_yaz(uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            J_ = ii_kos()
            print(J_["ileri_cumle"]); print(J_["etiket"])
        elif a.komut == "rapor":
            print(ii_rapor_yaz())
        else:
            print(json.dumps({"II_ESIK_SHA": ii_esik_sha(), "FI_PARAM_SHA": ii_fi_param_sha(), "FI_KOD_SHA": ii_fi_kod_sha(),
                              "II_KOD_SHA": ii_kod_sha()}, indent=1))
    except IIHata as ex:
        iilog.error("%s", ex); sys.exit(1)
