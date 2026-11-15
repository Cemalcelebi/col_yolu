"""K24_YENIDEN — K24 iki evre çöl kuralının (FON_IZI fi_k24_tara, Ç96) ORTAK CETVEL ile yeniden ölçümü, tek dosya
(14 Kasım 2026; dört aşamalı yeniden ölçümün AŞAMA 2'si).

Cemal (14 Kas 2026): "temel çöl yapısının tespit başarısını ölç"; "her aşamada aynı ölçüm kriterleri; sonucu beğenmediğimiz için eşikle oynanmaz".

SİNYAL (DEĞİŞMEZ): FON_IZI.fi_k24_tara(d, FI_K24) satırlarından kural == True olanlar (FON_IZI içe alınır, kod KOPYALANMAZ). Tanım
(FON_IZI 'K24 iki evre kuralı' açıklaması): t günü SMA20 üstündeki kapanış serisi tam 5'e ulaşır; serinin öncesindeki 10 barın >= %80'i
SMA20 altında kapanmış (1. evre); serideki 5 mumun en fazla 2'sinin dibi SMA20'yi deler; BB genişliği (4σ / SMA20) son 15 barın en
yükseğinin <= %70'i; son 15 barın dibi önceki 120 bar tepesinin <= -%30 altında; aynı hissede 60 barda tek. FI_K24 sözlüğünün ve
fi_k24_tara kaynak kodunun sha'sı ön kayıtta; biri değişirse koşu durur.
ÖLÇÜ: ORTAK_CETVEL (OC.oc_olc / OC.oc_rapor); kendi ölçü / eşik yok. Olay = (sembol, sinyal günü t, pazar); giriş t'den sonraki ilk açılış (OC).
SAPMA (sonuç görülmeden, ön kayıtta): (1) fi_k24_tara 'n < 200 ise boş' şartı serinin TOPLAM uzunluğuna bakar (geleceğe bakma: hisse
sonradan 200 bara ulaşmasa sinyal hiç olmazdı) -> yalnız t gününe kadar >= 200 barı olan sinyaller alınır (t'de kesilen seriyle birebir aynı
tespit; kos'ta gerçek veride örneklemle denetlenir). (2) Tarama OC temiz verisinde (H>L, V>0 olmayan bar atılmış; OC K3) yapılır; FON_IZI
eskiden ham fi_k1_veri'de tarardı. Ham / temiz sinyal sayısı ön kayıtta.
EK BİLGİ (karar dışı, cetvel içi): 1. evre süresi (çöl uzunluğu) tercilleri ve sert düşüş derinliği kovaları; her alt küme OC.oc_olc ile.

Komut:  python K24_YENIDEN.py onkayit   veri + tarama + olay sayımı (getiri YOK) -> arastirma_cikti/k24_yeniden/K24_YENIDEN_ON_KAYIT.md
        python K24_YENIDEN.py kos       OC.oc_kapi + K24 sha / kod / git kapısı + olay sha eşitliği + geleceğe bakma denetimi -> ölçüm -> rapor
        python K24_YENIDEN.py rapor     kos çıktısından (k24_yeniden_sonuc.json + satır verisi) raporu yeniden yazar
Colab:  exec(open('K24_YENIDEN.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   OC.oc_veri (V_BIST / V_ABD (+k34_yahoo) / V_AVR). Satır verisi /tmp/k24_yeniden/ (repoya girmez). Tiingo YOK, ücretli veri YOK.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_KY = {k: id(v) for k, v in globals().items()}

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

KOK_KY = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_KY not in sys.path:
    sys.path.insert(0, KOK_KY)

kylog = logging.getLogger("col.k24_yeniden")
if not kylog.handlers:
    _ky_h = logging.StreamHandler(sys.stderr)
    _ky_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k24_yeniden: %(message)s", "%H:%M:%S"))
    kylog.addHandler(_ky_h)
    kylog.setLevel(logging.INFO)
    kylog.propagate = False

KY_SURUM = "K24_YENIDEN v1.0 (2026-11-14)"
KY_YOL = {"cikti": os.path.join(KOK_KY, "arastirma_cikti", "k24_yeniden"), "satir": os.environ.get("KY_SATIR", "/tmp/k24_yeniden"),
          "kod": os.path.join(KOK_KY, "K24_YENIDEN.py")}
KY_DOSYA = {"onkayit": "K24_YENIDEN_ON_KAYIT.md", "rapor": "K24_YENIDEN_RAPOR.md", "json": "k24_yeniden_sonuc.json",
            "olay": "k24_olay.csv.gz", "sinyal": "k24_sinyal.csv.gz"}

# ================================================================ MÜHÜRLÜ AYAR (yalnız bu aşamanın gösterim / alt küme tanımı; ölçü OC'de)
KY_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "sinyal": "FON_IZI.fi_k24_tara(d, FON_IZI.FI_K24) satırlarından kural == True; tarih = sinyal günü t (t kapanışına kadar bilgi)",
    "pazar": ["ABD", "AVR", "BIST"],
    "veri": "OC.oc_veri(pazar)['V'] (OC temiz veri: geçersiz bar atılmış; ABD + k34_yahoo; fonlar çıkar)",
    "gecmis_bar_asgari": 200,
    "sapma": [
        "SAPMA-1 (geleceğe bakma): fi_k24_tara 'n < 200 -> boş' şartı serinin toplam uzunluğuna bakar; yalnız t gününde hissenin kendi "
        "takviminde >= 200 barı (t dahil) olan sinyaller alınır. Böylece tespit, seri t'de kesildiğinde yapılan tespitle birebir aynıdır.",
        "SAPMA-2 (veri): tarama OC temiz verisinde (OC K3: H>L, V>0, fiyat > 0 olmayan bar atılır); FON_IZI K24 eskiden ham fi_k1_veri'de "
        "tarardı. FI_K24 parametreleri ve fi_k24_tara kodu DEĞİŞMEZ."],
    "evre1": {"kesen_seri": 3,
              "tanim": "1. evre süresi L1 = serinin ilk barı a = t-4'ten geriye, SMA20 üstünde >= 3 ardışık kapanışlık son dizinin bittiği "
                       "bar j'den a-1'e kadar bar sayısı (a-1-j); böyle dizi yoksa SMA20'nin ilk geçerli barından (19) a-1'e kadar. "
                       "(fi_k24_tara'nın kendi 'seri' sayacı: c > SMA20 ardışık kapanış sayısı; yalnız t ve öncesi.)"},
    "tercil": {"kaynak_pazar": "ABD", "kaynak_donem": "2016-22", "donem_tarih": "sinyal günü t",
               "tanim": "kesikler L1'in ABD 2016-22 (keşif) sinyallerindeki 1/3 ve 2/3 yüzdeliği (np.quantile, linear); ön kayıtta "
                        "sayı olarak yazılır, bütün pazar / dönemlere aynı kesik uygulanır: kısa <= q1 < orta <= q2 < uzun"},
    "derinlik": {"kova": [["-%30..-%50", -0.50, -0.30], ["-%50..-%70", -0.70, -0.50], ["<-%70", -10.0, -0.70]],
                 "tanim": "fi_k24_tara 'dusus' (son 15 barın dibi / önceki 120 bar tepesi - 1); kova (alt, üst]: alt < dusus <= üst"},
    "gelecek_denetim": {"ornek": 60, "tohum": 24,
                        "tanim": "kos: her pazardan rastgele 60 sinyal; seri t'de kesilip fi_k24_tara yeniden koşulur; t'de kural satırı, "
                                 "aynı dusus / L1 yoksa koşu DURUR"},
    "karar": "OC_ESIK 'etiket' (oc_etiket); tek hipotez (bir sinyal) -> çoklu karşılaştırma düzeltmesi yok; alt küme tabloları BİLGİ "
             "(karar dışı, iddia üretmez)",
    "eski_kayit": ["Ç96", "Ç113", "Ç118", "Ç122", "Ç175"],
}

KY_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = OC (aynı giriş günü, aynı pazar, aynı 60 gün momentum beşliği x 20 gün likidite üçlüsü; plasebo 200 portföy). "
                   "Mekanik üstünlük: K24 sinyali 'SMA20 üstünde 5 kapanış' ister (kısa vadeli yükseliş) ve '-%30 düşüş' ister; eşler 60 gün "
                   "momentumla eşlenir, 5 gün getirisiyle eşlenmez -> kısa vadeli dönüş / devam etkisi sinyale karışabilir (raporda sınır)"),
    "K2": ("EVET", "fi_k24_tara yalnız geriye bakan pencereler (SMA20, std20, 120 bar tepe, 10 bar 1. evre); 'n < 200' toplam uzunluk şartı "
                   "SAPMA-1 ile t'ye kadar 200 bara indirildi; test_k24_yeniden 'gelecek' + kos'ta gerçek veride 60 sinyal/pazar kesme denetimi; "
                   "tercil kesikleri yalnız ABD 2016-22 (keşif) sinyallerinden, ön kayıtta sabit"),
    "K3": ("EVET", "tarama OC temiz verisinde (OC oc_veri_hazirla: H>L, V>0, fiyat>0 olmayan bar atılır; SAPMA-2); OC sinyal barı geçersizse olay düşer"),
    "K4": ("EVET", "fi_k24_tara 'tekrar' 60 bar (kural günleri arası) + OC 60 birleşik takvim günü tekilleştirme; n bağımsız olay; hücrede medyan"),
    "K5": ("EVET", "giriş = OC: t'den sonraki ilk geçerli bar açılışı (sinyal t kapanışında oluşur)"),
    "K6": ("EVET", "tek kip: V_*.pkl düzeltilmiş fiyat; OC bölünme şüphesi geçmiş penceresi; AVR likidite EUR (OC); getiri oranı birimden bağımsız"),
    "K7": ("EVET", "evren bugün işlem görenler + ABD k34 nakdi biten (yine bugün işlem gören); batanlar YOK -> getiriler yukarı, -%50 "
                   "olasılığı aşağı yanlı; raporda yazılır"),
    "K8": ("EVET", "3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; OC iki yarı aynı yön şartı; İZ DEĞİL yalnız güç yeterliyken (n >= 1.000 ya da "
                   "güç %80); tek hipotez -> BH gerekmez; alt kümeler bilgi"),
    "K9": ("EVET", "KY_ESIK sha + FI_K24 sha + fi_k24_tara kaynak sha + K24_YENIDEN.py sha + OC üç satırı + olay sha ön kayıtta; ön kayıt ve "
                   "modül commit + push SONRA kos; kos git kapısı + sha eşitliği; eşik yok, sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "metin / haber / KAP ayrıştırma yok; yalnız OHLCV; ham veriden 3 olay elle doğrulanır (denetim, raporda)"),
    "K11": ("EVET", "satır verisi /tmp/k24_yeniden/k24_olay.csv.gz; >= 2 hücre bağımsız kodla yeniden üretilir; 3 olay ham veriden elle"),
    "K12": ("EVET", "etiketler yalnız OC kuralıyla; fiyat değişimi (komisyon yok) yazılır; alt küme tabloları 'bilgi', iddia değil"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_ky; yasak dosyalara dokunulmaz (git diff --stat); e-posta / anahtar taraması testte; ücretli veri yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm"),
}


class KYHata(RuntimeError):
    """Durdurucu hata: ön kayıt yok / sha tutmuyor / git'e işlenmemiş / olay kümesi ön kayıttan farklı / geleceğe bakma denetimi tutmadı."""


# ================================================================ 0) ORTAK
_KY_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _ky_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ky_sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _ky_F():
    import FON_IZI as F   # kütüphane olarak; FON_IZI kendi çakışma kapısını taşır
    return F


def _ky_OC():
    import ORTAK_CETVEL as OC
    return OC


def ky_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return _ky_sha(json.dumps(E or KY_ESIK, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def ky_fi_k24_sha() -> str:
    """FI_K24 sözlüğünün sha'sı (kanonik JSON)."""
    return _ky_sha(json.dumps(_ky_F().FI_K24, sort_keys=True).encode("utf-8"))


def ky_fi_kod_sha() -> str:
    """fi_k24_tara + _fi_k23_yon kaynak kodu + FI_K23 (yon alanları) sha'sı: sinyal kodu değişirse koşu durur."""
    F = _ky_F()
    kaynak = inspect.getsource(F.fi_k24_tara) + inspect.getsource(F._fi_k23_yon) + json.dumps(F.FI_K23, sort_keys=True, default=str)
    return _ky_sha(kaynak.encode("utf-8"))


def ky_kod_sha(yol: Optional[str] = None) -> str:
    with open(yol or KY_YOL["kod"], "rb") as f:
        return _ky_sha(f.read())


def ky_olay_sha(S: pd.DataFrame) -> str:
    """Sinyal kümesinin sha'sı (pazar, sembol, tarih sıralı)."""
    if not len(S):
        return _ky_sha(b"")
    X = S[["pazar", "sembol", "tarih"]].copy(); X["tarih"] = pd.to_datetime(X.tarih).dt.strftime("%Y-%m-%d")
    X = X.sort_values(["pazar", "sembol", "tarih"]).reset_index(drop=True)
    return _ky_sha(X.to_csv(index=False).encode("utf-8"))


def _ky_donem_t(t: pd.Series, E_oc: Dict[str, Any]) -> np.ndarray:
    t = pd.to_datetime(t); out = np.full(len(t), "dışı", dtype=object)
    for ad, a, b in E_oc["donem"]:
        out[((t >= a) & (t <= b)).to_numpy()] = ad
    return out


# ================================================================ 1) TARAMA
def ky_evre1(c: np.ndarray, E: Dict[str, Any] = KY_ESIK) -> Tuple[np.ndarray, np.ndarray]:
    """fi_k24_tara ile aynı SMA20 ve 'seri' sayacı; her bar t için (seri[t], L1 tanımının kullanacağı 'son kesen dizi sonu' dizisi).
    Döner: seri, kes (kes[i] = i ve öncesinde seri >= kesen_seri olan son bar; yoksa -1). Yalnız geçmiş bilgi."""
    cs = pd.Series(c); sma = cs.rolling(20).mean().to_numpy(); n = len(c)
    seri = np.zeros(n, int)
    for t in range(1, n):
        seri[t] = seri[t - 1] + 1 if c[t] > sma[t] else 0
    k = E["evre1"]["kesen_seri"]
    isaret = np.where(seri >= k, np.arange(n), -1)
    kes = np.maximum.accumulate(isaret) if n else isaret
    return seri, kes


def ky_tara(d: pd.DataFrame, E: Dict[str, Any] = KY_ESIK) -> pd.DataFrame:
    """Bir hissede K24 kural sinyalleri (FON_IZI.fi_k24_tara, değişmeden) + SAPMA-1 (t'ye kadar >= 200 bar) + L1 (1. evre süresi).
    Döner: tarih, t_i, dusus, once_alt, delen, bbw, L1 (yalnız t ve öncesi bilgisi; fi_k24_tara'nın ileri alanları yon60 / yon20 / r120 ATILIR)."""
    F = _ky_F()
    X = F.fi_k24_tara(d, F.FI_K24)
    if not len(X) or "kural" not in X:
        return pd.DataFrame(columns=["tarih", "t_i", "dusus", "once_alt", "delen", "bbw", "L1"])
    X = X[X.kural.astype(bool)].copy()
    ti = d.index.get_indexer(pd.DatetimeIndex(X.tarih))
    if (ti < 0).any():
        raise KYHata("fi_k24_tara tarihleri seride yok (iç tutarsızlık)")
    X["t_i"] = ti
    X = X[X.t_i >= E["gecmis_bar_asgari"] - 1].copy()          # SAPMA-1: t dahil >= 200 bar
    if not len(X):
        return pd.DataFrame(columns=["tarih", "t_i", "dusus", "once_alt", "delen", "bbw", "L1"])
    seri, kes = ky_evre1(d.Close.to_numpy(float), E)
    t = X.t_i.to_numpy(int); a = t - (_ky_F().FI_K24["seri"] - 1)
    if not (seri[t] == _ky_F().FI_K24["seri"]).all():
        raise KYHata("seri sayacı fi_k24_tara ile tutmuyor (iç tutarsızlık)")
    j = kes[a - 1]
    X["L1"] = np.where(j >= 0, a - 1 - j, a - 1 - 19)
    return X[["tarih", "t_i", "dusus", "once_alt", "delen", "bbw", "L1"]].reset_index(drop=True)


def ky_sinyaller(V: Dict[str, Dict[str, Any]], E: Dict[str, Any] = KY_ESIK) -> Tuple[pd.DataFrame, Dict[str, Dict[str, int]]]:
    """V: pazar -> OC.oc_veri çıktısı. Döner: sinyal tablosu (pazar, sembol, tarih, t_i, dusus, L1, ...) ve sayım (SAPMA-1 düşen dahil)."""
    F = _ky_F(); parca: List[pd.DataFrame] = []; say: Dict[str, Dict[str, int]] = {}
    for pz in [p for p in E["pazar"] if p in V]:
        n_ham_kural = 0; n_s1 = 0; hata = 0
        for s, d in V[pz]["V"].items():
            try:
                X0 = F.fi_k24_tara(d, F.FI_K24)
                k0 = int(X0.kural.sum()) if len(X0) and "kural" in X0 else 0
                X = ky_tara(d, E)
            except KYHata:
                raise
            except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer (sayımda)
                hata += 1; kylog.warning("%s %s atlandı: %s", pz, s, ex); continue
            n_ham_kural += k0; n_s1 += k0 - len(X)
            if len(X):
                parca.append(X.assign(pazar=pz, sembol=s))
        say[pz] = {"hisse": len(V[pz]["V"]), "kural_tum": n_ham_kural, "sapma1_dusen": n_s1, "sinyal": n_ham_kural - n_s1, "hata": hata}
        kylog.info("%s: %d hisse, %d kural, SAPMA-1 düşen %d", pz, len(V[pz]["V"]), n_ham_kural, n_s1)
    S = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame(columns=["pazar", "sembol", "tarih", "t_i", "dusus", "L1"])
    S["tarih"] = pd.to_datetime(S.tarih)
    return S[["pazar", "sembol", "tarih", "t_i", "dusus", "once_alt", "delen", "bbw", "L1"]], say


def ky_ham_sayim(pazar: str, OC: Any = None) -> int:
    """SAPMA-2 bilgisi: ham V_<pazar>.pkl (temizlenmemiş, k34 yok) üzerinde aynı tarama + SAPMA-1 ile sinyal sayısı (getiri yok)."""
    OC = OC or _ky_OC()
    yol = os.path.join(OC.OC_YOL["veri"], f"V_{pazar}.pkl")
    ham = pd.read_pickle(yol)
    if isinstance(ham, dict) and "veri" in ham and isinstance(ham["veri"], dict):
        ham = ham["veri"]
    n = 0
    for s, d in ham.items():
        try:
            n += len(ky_tara(d))
        except Exception:   # noqa: BLE001 — ham veride bozuk hisse sayılmaz (yalnız bilgi sayımı)
            continue
    return n


def ky_tercil(S: pd.DataFrame, E: Dict[str, Any] = KY_ESIK) -> Tuple[float, float]:
    OC = _ky_OC(); T = E["tercil"]
    x = S[(S.pazar == T["kaynak_pazar"]) & (_ky_donem_t(S.tarih, OC.OC_ESIK) == T["kaynak_donem"])].L1.to_numpy(float)
    if len(x) < 30:
        raise KYHata(f"tercil kaynağı yetersiz (n {len(x)})")
    q1, q2 = np.quantile(x, [1 / 3, 2 / 3])
    return float(q1), float(q2)


def ky_kova_ekle(S: pd.DataFrame, q: Tuple[float, float], E: Dict[str, Any] = KY_ESIK) -> pd.DataFrame:
    S = S.copy(); q1, q2 = q
    S["L1_kova"] = np.where(S.L1 <= q1, "kısa", np.where(S.L1 <= q2, "orta", "uzun"))
    dk = np.full(len(S), "?", dtype=object)
    for ad, alt, ust in E["derinlik"]["kova"]:
        dk[((S.dusus > alt) & (S.dusus <= ust)).to_numpy()] = ad
    S["derinlik_kova"] = dk
    return S


def ky_gelecek_denetimi(V: Dict[str, Dict[str, Any]], S: pd.DataFrame, E: Dict[str, Any] = KY_ESIK) -> Dict[str, Any]:
    """Her pazardan rastgele örnek sinyal: seri t'de kesilir, ky_tara yeniden; t'de aynı satır (dusus, L1) yoksa KYHata."""
    G = E["gelecek_denetim"]; rng = np.random.default_rng(G["tohum"]); out = {}
    for pz in S.pazar.unique():
        X = S[S.pazar == pz]
        sec = X.iloc[rng.choice(len(X), min(G["ornek"], len(X)), replace=False)]
        bozuk = []
        for r in sec.itertuples():
            d = V[pz]["V"][r.sembol]; dk = d.loc[:r.tarih]
            Y = ky_tara(dk, E)
            Y = Y[Y.tarih == r.tarih]
            if len(Y) != 1 or not np.isclose(Y.dusus.iloc[0], r.dusus) or int(Y.L1.iloc[0]) != int(r.L1):
                bozuk.append(f"{r.sembol} {r.tarih.date()}")
        out[pz] = {"ornek": len(sec), "bozuk": bozuk}
        if bozuk:
            raise KYHata(f"geleceğe bakma denetimi TUTMADI ({pz}): {bozuk[:5]}")
    return out


# ================================================================ 2) ESKİ KAYITLAR (IZ_KARNE; yeniden ölçülmez)
def ky_eski_kayitlar(E: Dict[str, Any] = KY_ESIK) -> List[Dict[str, str]]:
    import IZ_KARNE as IK
    sat = []
    for k in IK.IK_KAYIT:
        if k["kod"] in E["eski_kayit"]:
            sat.append({"kod": k["kod"], "tarih": k["tarih"], "ad": k["ad"], "not": k.get("not", "")})
    return sat


KY_ESKI_SATIR = [   # IZ_KARNE notlarından aynen alınan sayılar (ky_eski_dogrula her birinin metinde geçtiğini denetler)
    ("Ç96", "K24 ilk ölçüm (eski tek cetvel: 60 gün önce +%15 oranı, kural / eşli kat)", "ABD 2023 0,92, ABD 2024-26 0,97"),
    ("Ç113", "FI_OLCUT eşli fark ABD 2023 / 2024-26, AVR 2023 / 2024-26, BIST 2023 / 2024-26",
     "çöl K24 +%3,1 (aralık artı) / -%0,5, +%0,4 / +%0,5, "),
    ("Ç118", "ABD çöl sinyali sayısı ve eşli fark", "6.912 çöl sinyali"),
    ("Ç122", "ham fark (eşit ağırlıklı piyasaya göre) ABD 2016-22 / 2023 / 2024-26", "çöl K24 -%0,8 / +%5,1 / +%1,0"),
]


def ky_eski_dogrula() -> List[Dict[str, Any]]:
    K = {k["kod"]: k["not"] for k in ky_eski_kayitlar()}
    out = []
    for kod, ne, alinti in KY_ESKI_SATIR:
        out.append({"kod": kod, "ne": ne, "alinti": alinti.strip().rstrip(","), "metinde": alinti in K.get(kod, "")})
    return out


# ================================================================ 3) ÖN KAYIT
def ky_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = KY_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def _ky_sayim_tablosu(S: pd.DataFrame) -> List[str]:
    OC = _ky_OC(); dn = _ky_donem_t(S.tarih, OC.OC_ESIK)
    don = [a for a, _b, _c in OC.OC_ESIK["donem"]] + ["dışı"]
    s = ["| Pazar | " + " | ".join(don) + " | toplam |", "|---|" + "---|" * (len(don) + 1)]
    for pz in KY_ESIK["pazar"]:
        m = (S.pazar == pz).to_numpy()
        s.append(f"| {pz} | " + " | ".join(str(int((m & (dn == d)).sum())) for d in don) + f" | {int(m.sum())} |")
    return s


def _ky_kova_sayim(S: pd.DataFrame, kol: str, sira: List[str]) -> List[str]:
    OC = _ky_OC(); dn = _ky_donem_t(S.tarih, OC.OC_ESIK)
    s = ["| Pazar | Dönem | " + " | ".join(sira) + " |", "|---|---|" + "---|" * len(sira)]
    for pz in KY_ESIK["pazar"]:
        for d, _a, _b in OC.OC_ESIK["donem"]:
            m = ((S.pazar == pz).to_numpy()) & (dn == d)
            s.append(f"| {pz} | {d} | " + " | ".join(str(int((m & (S[kol] == k).to_numpy()).sum())) for k in sira) + " |")
    return s


def ky_onkayit_metni(S: pd.DataFrame, say: Dict[str, Dict[str, int]], ham: Dict[str, int], q: Tuple[float, float], notlar: Dict[str, List[str]]) -> str:
    OC = _ky_OC(); F = _ky_F()
    Sk = ky_kova_ekle(S, q)
    dn = _ky_donem_t(S.tarih, OC.OC_ESIK)
    guc = []
    for pz in OC.OC_ESIK["karar_pazar"]:
        for d in OC.OC_ESIK["karar_donem"]:
            n = int(((S.pazar == pz).to_numpy() & (dn == d)).sum())
            guc.append(f"| {pz} | {d} | {n} | {OC.oc_guc_bak(n) * 100:.0f} |")
    eski = ky_eski_dogrula()
    s = [f"# K24 İKİ EVRE ÇÖL — YENİDEN ÖLÇÜM ÖN KAYDI ({KY_SURUM})", "",
         f"Yazım: {_ky_simdi()}. Bu dosya ölçümden ÖNCE yazıldı. Bu modülde hiçbir getiri / eşli fark / olasılık HESAPLANMADI; yalnız sinyal "
         "tarandı ve sayıldı. Ön kayıt + modül commit + push edilir, SONRA `python K24_YENIDEN.py kos`.", "",
         "Cemal (14 Kas 2026): \"temel çöl yapısının tespit başarısını ölç\"; \"her aşamada aynı ölçüm kriterleri; sonucu beğenmediğimiz için eşikle oynanmaz\".", "",
         "## 1. Sinyal tanımı (DEĞİŞMEZ; FON_IZI.fi_k24_tara içe alınır, kopyalanmaz)", "",
         "t günü SMA20 üstündeki kapanış serisi tam 5'e ulaşır (2. evre dizilme teyidi); serinin öncesindeki 10 barın >= %80'i SMA20 altında "
         "kapanmış (1. evre); serideki 5 mumun en fazla 2'sinin dibi SMA20'yi deler; BB genişliği (4σ / SMA20) son 15 barın en yükseğinin "
         "<= %70'i (sıkışma); son 15 barın dibi önceki 120 bar tepesinin <= -%30 altında (düşüş sonrası); aynı hissede 60 barda tek. "
         "(FON_IZI 'K24 iki evre kuralı' açıklaması, Ç96; eşikler MANAS'ın iki bölgesinden, 25 Eki.)", "",
         "```json", json.dumps(F.FI_K24, sort_keys=True), "```", "",
         "## 2. Mühür satırları", "",
         "### ORTAK CETVEL (aynen; OC.oc_kapi_satirlari())", "", OC.oc_kapi_satirlari(), "",
         "### Bu aşama", "",
         f"KY_ESIK_SHA: `{ky_esik_sha()}`", f"FI_K24_SHA: `{ky_fi_k24_sha()}`", f"FI_K24_KOD_SHA: `{ky_fi_kod_sha()}`",
         f"KY_KOD_SHA: `{ky_kod_sha()}`", f"OLAY_SHA: `{ky_olay_sha(S)}`", f"TERCIL: `{q[0]:.6f}` `{q[1]:.6f}`", "",
         "- FI_K24_SHA = sha256(FI_K24 kanonik JSON); FI_K24_KOD_SHA = sha256(inspect.getsource(fi_k24_tara) + getsource(_fi_k23_yon) + FI_K23); "
         "KY_KOD_SHA = sha256(K24_YENIDEN.py bayt); OLAY_SHA = sha256(pazar, sembol, sinyal tarihi sıralı csv). kos bunların hepsini yeniden "
         "hesaplar; biri farklıysa DURUR.", "",
         "## 3. Sapmalar (sonuç görülmeden)", ""] + [f"- {x}" for x in KY_ESIK["sapma"]] + [
         "", "Ham (temizlenmemiş V_*.pkl, k34 yok) / temiz (OC) sinyal sayısı (SAPMA-2 etkisi; getiri yok):", "",
         "| Pazar | ham V_*.pkl | OC temiz (ABD: + k34) |", "|---|---|---|"] + [
         f"| {pz} | {ham.get(pz, '-')} | {say.get(pz, {}).get('sinyal', '-')} |" for pz in KY_ESIK["pazar"]] + [
         "", "## 4. Ölçüm ve karar (ORTAK CETVEL; kendi ölçü / eşik yok)", "",
         "- Olay = (sembol, sinyal günü t, pazar) -> `OC.oc_olc(olaylar, V)`; rapor `OC.oc_rapor`. Pazarlar ABD (+k34), AVR, BIST; dönemler "
         "2016-22 keşif, 2023, 2024-26/08 (OC dönemi GİRİŞ gününe göre atar).",
         f"- Karar: {KY_ESIK['karar']}.",
         "- Eski sonuçlarla kıyas (bilgi; yeniden ölçülmez, IZ_KARNE kayıtlarından okunur):", ""] + [
         f"  - {e['kod']}: {e['ne']}: \"{e['alinti']}\" (IZ_KARNE metninde: {'EVET' if e['metinde'] else 'HAYIR'})" for e in eski] + [
         "", "## 5. Ek bilgi tabloları (karar dışı; her alt küme OC.oc_olc ile, cetvel içi)", "",
         f"- 1. evre süresi L1: {KY_ESIK['evre1']['tanim']}",
         f"- Tercil: {KY_ESIK['tercil']['tanim']}. Kesikler (ABD 2016-22 sinyallerinden): q1 = {q[0]:.2f} bar, q2 = {q[1]:.2f} bar.",
         f"- Derinlik: {KY_ESIK['derinlik']['tanim']}; kovalar " + ", ".join(k[0] for k in KY_ESIK["derinlik"]["kova"]) + ".", "",
         "## 6. OLAY SAYIMI (getiri hesaplanmadan; sinyal günü t'ye göre dönem; OC giriş gününe göre atar, sınırda birkaç olay kayabilir)", ""]
    s += _ky_sayim_tablosu(S)
    s += ["", "Tarama sayımı:", "", "| Pazar | hisse | kural (tüm) | SAPMA-1 düşen | sinyal | okunamayan hisse |", "|---|---|---|---|---|---|"]
    s += [f"| {pz} | {c['hisse']} | {c['kural_tum']} | {c['sapma1_dusen']} | {c['sinyal']} | {c['hata']} |" for pz, c in say.items()]
    s += ["", "L1 tercil sayımı:", ""] + _ky_kova_sayim(Sk, "L1_kova", ["kısa", "orta", "uzun"])
    s += ["", "Derinlik kova sayımı:", ""] + _ky_kova_sayim(Sk, "derinlik_kova", [k[0] for k in KY_ESIK["derinlik"]["kova"]])
    s += ["", "Beklenen güç (OC güç tablosu, δ +%5; sinyal sayısıyla; OC süzgeçleri n'i düşürür, gerçek güç raporda):", "",
          "| Pazar | Dönem | sinyal n | güç % |", "|---|---|---|---|"] + guc
    s += ["", "Ç175 tahmini ABD ~6.900 sinyal (eski Ç118: 6.912). Bu taramada ABD 2023 + 2024-26 (sinyal günü) = "
          f"{int(((S.pazar == 'ABD').to_numpy() & np.isin(dn, ['2023', '2024-26'])).sum())}; ABD tüm dönem {int((S.pazar == 'ABD').sum())} "
          "(k34 nakdi biten 1.472 hisse eklendi; 2016-22 dahil).", "",
          "Veri notları:", ""] + [f"- {pz}: {'; '.join(v)}" for pz, v in notlar.items()]
    s += ["", ky_kontrol_tablosu(), "",
          "## Test", "", "`python test_k24_yeniden.py` (sentetik: sinyal tespiti FON_IZI ile birebir; geleceğe bakma: seri t'de kesilince aynı tespit; "
          "SAPMA-1; L1 elle; kova; cetvel çağrısı; kapı; çakışma kapısı; e-posta / anahtar yok).", ""]
    return "\n".join(s)


def ky_veri(pazarlar: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
    OC = _ky_OC()
    return {pz: OC.oc_veri(pz) for pz in (pazarlar or KY_ESIK["pazar"])}


def ky_onkayit_yaz(cikti: Optional[str] = None, uzerine: bool = False) -> str:
    OC = _ky_OC(); cikti = cikti or KY_YOL["cikti"]; os.makedirs(cikti, exist_ok=True)
    yol = os.path.join(cikti, KY_DOSYA["onkayit"])
    if os.path.exists(yol):
        try:
            OC._oc_git_islenmis(yol); islenmis = True
        except OC.OCHata:
            islenmis = False
        if islenmis or not uzerine:
            raise KYHata(f"ön kayıt var ({yol}); git'e işlenmişse üzerine yazılmaz, işlenmemişse --uzerine-yaz")
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    V = ky_veri(); S, say = ky_sinyaller(V)
    ham = {pz: ky_ham_sayim(pz, OC) for pz in KY_ESIK["pazar"]}
    q = ky_tercil(S)
    metin = ky_onkayit_metni(S, say, ham, q, {pz: V[pz]["not"] for pz in V})
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _ky_oku_satir(metin: str, ad: str) -> str:
    m = re.search(rf"^{ad}:\s*`([0-9a-f]{{64}})`", metin, flags=re.M)
    if not m:
        raise KYHata(f"ön kayıtta {ad} satırı yok")
    return m.group(1)


def ky_kapi(onkayit_yolu: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    """Koşu kapısı: OC.oc_kapi (kontrol listesi + cetvel / kod / güç sha + git) + bu aşamanın sha'ları + modül git'te işlenmiş / değişmemiş."""
    OC = _ky_OC(); yol = onkayit_yolu or os.path.join(KY_YOL["cikti"], KY_DOSYA["onkayit"])
    try:
        out = OC.oc_kapi(yol, git=git)
    except OC.OCHata as ex:
        raise KYHata(f"OC kapısı kapalı: {ex}")
    metin = open(yol, encoding="utf-8").read()
    simdi = {"KY_ESIK_SHA": ky_esik_sha(), "FI_K24_SHA": ky_fi_k24_sha(), "FI_K24_KOD_SHA": ky_fi_kod_sha(), "KY_KOD_SHA": ky_kod_sha()}
    for ad, v in simdi.items():
        o = _ky_oku_satir(metin, ad)
        if o != v:
            raise KYHata(f"{ad} tutmuyor: ön kayıt {o[:12]}…, şimdi {v[:12]}… -> koşu DURDU")
    m = re.search(r"^TERCIL:\s*`([-0-9.]+)`\s*`([-0-9.]+)`", metin, flags=re.M)
    if not m:
        raise KYHata("ön kayıtta TERCIL satırı yok")
    out.update(simdi); out["OLAY_SHA"] = _ky_oku_satir(metin, "OLAY_SHA"); out["TERCIL"] = (float(m.group(1)), float(m.group(2)))
    if git:
        try:
            out["git_modul"] = OC._oc_git_islenmis(KY_YOL["kod"])
        except OC.OCHata as ex:
            raise KYHata(str(ex))
    kylog.info("ky_kapi AÇIK (%s)", yol)
    return out


# ================================================================ 4) KOŞU
def _ky_alt_ozet(S: Dict[str, Any], ad: str, kova: str) -> List[Dict[str, Any]]:
    T = S["hucre"]; Ob = S["olasilik"].set_index(["pazar", "donem"]) if len(S["olasilik"]) else None; out = []
    for r in T.to_dict("records"):
        o = Ob.loc[(r["pazar"], r["donem"])].to_dict() if Ob is not None and (r["pazar"], r["donem"]) in Ob.index else {}
        out.append({"tablo": ad, "kova": kova, "pazar": r["pazar"], "donem": r["donem"], "n": int(r.get("n") or 0),
                    "ort_fark": r.get("ort_fark"), "alt95": r.get("alt95"), "ust95": r.get("ust95"), "medyan_fark": r.get("medyan_fark"),
                    "sira": r.get("sira"), "portfoy": r.get("portfoy"), "plasebo_p90": r.get("portfoy_esli_p90"), "durum": r.get("durum"),
                    "n250": o.get("n250"), "up100_es_kat": o.get("up100_es_kat"), "dn50_es_kat": o.get("dn50_es_kat"), "olas": r.get("olas")})
    return out


def ky_kos(onkayit_yolu: Optional[str] = None, git: bool = True, cikti: Optional[str] = None) -> Dict[str, Any]:
    OC = _ky_OC(); t0 = time.time(); bas = _ky_simdi()
    K = ky_kapi(onkayit_yolu, git=git)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    V = ky_veri(); S, say = ky_sinyaller(V)
    if ky_olay_sha(S) != K["OLAY_SHA"]:
        raise KYHata("olay kümesi ön kayıttakinden farklı (OLAY_SHA) -> koşu DURDU")
    q = ky_tercil(S)
    if not np.allclose(q, K["TERCIL"], atol=1e-5):
        raise KYHata(f"tercil kesikleri ön kayıttan farklı: {q} vs {K['TERCIL']}")
    GD = ky_gelecek_denetimi(V, S)
    kylog.info("geleceğe bakma denetimi: %s", {k: v["ornek"] for k, v in GD.items()})
    S = ky_kova_ekle(S, q)
    # paneller bir kez kurulur (OC _oc_panel_al hazır paneli kabul eder); ham çerçeveler panelden sonra bırakılır
    P = {}
    for pz in list(V):
        P[pz] = OC.oc_panel(V[pz]); V[pz] = None
    ol = S[["sembol", "tarih", "pazar"]]
    R = OC.oc_olc(ol, P)
    alt: List[Dict[str, Any]] = []
    for kol, sira, ad in (("L1_kova", ["kısa", "orta", "uzun"], "L1 tercil"),
                          ("derinlik_kova", [k[0] for k in KY_ESIK["derinlik"]["kova"]], "derinlik")):
        for k in sira:
            Sx = S[S[kol] == k]
            if not len(Sx):
                continue
            alt += _ky_alt_ozet(OC.oc_olc(Sx[["sembol", "tarih", "pazar"]], P), ad, k)
    # satır verisi (repo dışı)
    os.makedirs(KY_YOL["satir"], exist_ok=True)
    X = R["olay"].merge(S.drop(columns=["t_i"]).rename(columns={"tarih": "tarih"}), on=["pazar", "sembol", "tarih"], how="left")
    X.to_csv(os.path.join(KY_YOL["satir"], KY_DOSYA["olay"]), index=False)
    S.to_csv(os.path.join(KY_YOL["satir"], KY_DOSYA["sinyal"]), index=False)
    J = {"surum": KY_SURUM, "kos_bas_utc": bas, "kos_son_utc": _ky_simdi(), "sure_sn": round(time.time() - t0),
         "kapi": {k: (v if not isinstance(v, tuple) else list(v)) for k, v in K.items() if k != "kontrol"},
         "sayim_tarama": say, "sayim_oc": R["sayim"], "etiket": R["etiket"], "cetvel_sha": R["cetvel_sha"], "kod_sha": R["kod_sha"],
         "hucre": json.loads(R["hucre"].to_json(orient="records", force_ascii=False)),
         "olasilik": json.loads(R["olasilik"].to_json(orient="records", force_ascii=False)),
         "alt": json.loads(pd.DataFrame(alt).to_json(orient="records", force_ascii=False)), "gelecek_denetim": GD,
         "tercil": list(q), "eski": ky_eski_dogrula(), "oc_rapor": OC.oc_rapor(R, "K24 iki evre çöl")}
    cikti = cikti or KY_YOL["cikti"]; os.makedirs(cikti, exist_ok=True)
    with open(os.path.join(cikti, KY_DOSYA["json"]), "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1, default=str)
    yol = ky_rapor_yaz(J, cikti)
    kylog.info("kos bitti: %s (%d sn)", yol, J["sure_sn"])
    return J


# ================================================================ 5) RAPOR
def _yz(x: Any, n: int = 1) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{x * 100:+.{n}f}".replace(".", ",")


def _kz(x: Any, n: int = 2) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


def ky_duz_ozet(J: Dict[str, Any]) -> List[str]:
    H = pd.DataFrame(J["hucre"]); O = pd.DataFrame(J["olasilik"]); et = J["etiket"]
    s = ["## DÜZ DİL ÖZET", ""]
    s.append(f"- Genel etiket: **{et['genel']}**; olasılık etiketi: **{et['olasilik']}** (ORTAK CETVEL kuralı).")
    for r in H[H.karar_hucre].to_dict("records"):
        o = O[(O.pazar == r["pazar"]) & (O.donem == r["donem"])]
        o = o.iloc[0].to_dict() if len(o) else {}
        s.append(f"- {r['pazar']} {r['donem']}: n {int(r['n'] or 0)}, 60 gün eşli fark {_yz(r.get('ort_fark'))} puan "
                 f"[%95 {_yz(r.get('alt95'))}, {_yz(r.get('ust95'))}], medyan {_yz(r.get('medyan_fark'))}, sıra {_kz(r.get('sira'))}; "
                 f"12 ayda +%100 eşlerin {_kz(o.get('up100_es_kat'))} katı, -%50 eşlerin {_kz(o.get('dn50_es_kat'))} katı -> {r['durum']}.")
    for r in H[(H.pazar == "BIST") & (H.donem != "2016-22")].to_dict("records"):
        s.append(f"- BIST {r['donem']} (bilgi): n {int(r['n'] or 0)}, eşli fark {_yz(r.get('ort_fark'))} [%95 {_yz(r.get('alt95'))}, "
                 f"{_yz(r.get('ust95'))}] -> {r['durum']}.")
    s.append("- Hayatta kalma: evren bugün işlem görenler (+ABD nakdi biten, yine yaşayan); batanlar yok: getiriler yukarı, -%50 olasılığı "
             "aşağı yanlı okunmalı. Komisyon yok.")
    return s


def ky_rapor_md(J: Dict[str, Any]) -> str:
    s = [f"# K24 İKİ EVRE ÇÖL — YENİDEN ÖLÇÜM RAPORU ({J['surum']})", "",
         f"Koşu: {J['kos_bas_utc']} -> {J['kos_son_utc']} ({J['sure_sn']} sn). Ön kayıt git: {J['kapi'].get('git', {})}; modül git: "
         f"{J['kapi'].get('git_modul', {})}.", ""]
    s += ky_duz_ozet(J) + ["", J["oc_rapor"], ""]
    s += ["## Eski sonuçlarla kıyas (bilgi; IZ_KARNE kayıtlarından okundu, yeniden ölçülmedi)", "",
          "| Kayıt | Ne | Eski sonuç (IZ_KARNE metninden) | metinde |", "|---|---|---|---|"]
    s += [f"| {e['kod']} | {e['ne']} | {e['alinti']} | {'EVET' if e['metinde'] else 'HAYIR'} |" for e in J["eski"]]
    H = pd.DataFrame(J["hucre"])
    yeni = "; ".join(f"{r['pazar']} {r['donem']} {_yz(r.get('ort_fark'))} (n {int(r['n'] or 0)})" for r in H.to_dict("records")
                     if r["donem"] != "2016-22")
    s += ["", f"Bu ölçüm (ORTAK CETVEL, giriş dönemi): {yeni}. Fark kaynakları: k34 nakdi biten ABD hisseleri eklendi; OC temiz veri; "
          "OC havuzu 'geçmiş' (likidite alt %20 ve geçmiş bölünme şüphesi dışarıda); SAPMA-1 (t'ye kadar 200 bar).", ""]
    A = pd.DataFrame(J["alt"])
    for ad in ("L1 tercil", "derinlik"):
        X = A[A.tablo == ad] if len(A) else A
        if not len(X):
            continue
        s += [f"## Ek bilgi tablosu: {ad} (karar dışı; her kova OC.oc_olc ile)", "",
              ("Tercil kesikleri (ABD 2016-22): q1 = " + _kz(J["tercil"][0]) + " bar, q2 = " + _kz(J["tercil"][1]) + " bar." if ad == "L1 tercil"
               else "Kova: son 15 barın dibi / önceki 120 bar tepesi - 1."), "",
              "| Kova | Pazar | Dönem | n | ort fark [%95] | medyan | sıra | portföy / p90 | durum | n250 | +%100 kat eş | -%50 kat eş | olasılık |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in X.to_dict("records"):
            s.append(f"| {r['kova']} | {r['pazar']} | {r['donem']} | {r['n']} | {_yz(r['ort_fark'])} [{_yz(r['alt95'])}, {_yz(r['ust95'])}] | "
                     f"{_yz(r['medyan_fark'])} | {_kz(r['sira'])} | {_yz(r['portfoy'], 0)} / {_yz(r['plasebo_p90'], 0)} | {r['durum']} | "
                     f"{r['n250'] if r['n250'] == r['n250'] and r['n250'] is not None else '-'} | {_kz(r['up100_es_kat'])} | {_kz(r['dn50_es_kat'])} | {r['olas']} |")
        s.append("")
    s += ["## Tarama sayımı", "", "| Pazar | hisse | kural (tüm) | SAPMA-1 düşen | sinyal |", "|---|---|---|---|---|"]
    s += [f"| {pz} | {c['hisse']} | {c['kural_tum']} | {c['sapma1_dusen']} | {c['sinyal']} |" for pz, c in J["sayim_tarama"].items()]
    s += ["", "Geleceğe bakma denetimi (gerçek veri, seri t'de kesildi): " +
          ", ".join(f"{pz} {v['ornek']} örnek, bozuk {len(v['bozuk'])}" for pz, v in J["gelecek_denetim"].items()), "",
          "## Sınırlar", "",
          "- Mekanik: sinyal 'SMA20 üstünde 5 kapanış' ve '-%30 düşüş' ister; eşler 60 gün momentum x likiditeyle eşlenir, son 5 gün getirisiyle "
          "eşlenmez (kısa vadeli dönüş / devam etkisi sinyale karışabilir).",
          "- Hayatta kalma: batanlar yok (Tiingo kullanılmadı); ABD k34 nakdi bitenler yine bugün işlem görenler.",
          "- Avrupa evreni 580 hisse (STOXX 600 + FTSE 250 bugünkü üyeler); BIST bilgi.",
          "- Alt küme tabloları karar dışıdır; çoklu karşılaştırma düzeltmesi yapılmadı, iddia üretmez.", ""]
    return "\n".join(s)


def ky_rapor_yaz(J: Optional[Dict[str, Any]] = None, cikti: Optional[str] = None) -> str:
    cikti = cikti or KY_YOL["cikti"]
    if J is None:
        J = json.load(open(os.path.join(cikti, KY_DOSYA["json"]), encoding="utf-8"))
    yol = os.path.join(cikti, KY_DOSYA["rapor"])
    metin = ky_rapor_md(J)
    if _KY_EPOSTA.search(metin):
        raise KYHata("raporda e-posta deseni var; yazılmadı")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


# ================================================================ ÇAKIŞMA KAPISI
def _cakisma_kontrol_ky(_once=_CK_ONCE_KY, _dosya="K24_YENIDEN.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_KY", "_CK_KAYIT", "_cakisma_kontrol_ky", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "inspect", "warnings", "_dt", "_yz", "_kz",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ky()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=KY_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "sha"])
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(ky_onkayit_yaz(uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            J_ = ky_kos()
            print(J_["etiket"])
        elif a.komut == "rapor":
            print(ky_rapor_yaz())
        else:
            print(json.dumps({"KY_ESIK_SHA": ky_esik_sha(), "FI_K24_SHA": ky_fi_k24_sha(), "FI_K24_KOD_SHA": ky_fi_kod_sha(),
                              "KY_KOD_SHA": ky_kod_sha()}, indent=1))
    except KYHata as ex:
        kylog.error("%s", ex); sys.exit(1)
