"""DIP_COL_AYRIM — AŞAMA 4: düzgün dip (gerçek dip) ile çöl formasyonu ayrılabiliyor mu? Tek dosya (14 Kasım 2026; ana oturum iş tanımı).

Cemal (14 Kas 2026): "Çöl formasyonuyla gerçek dip oluşumunu birbirinden ayırabiliyor muyuz, bunu denetle."

SİNYALLER (mevcut kod, DEĞİŞMEZ; FON_IZI'den içe alınır, parametre + kaynak sha ön kayıtta):
  dip16 = FON_IZI.fi_k13_tara(V, FI_K16_GEVSEK)   (Ç75: çöküş sonrası taban, şekil şartı gevşek, dip tabanı >= 0,20)
  dip17 = FON_IZI.fi_k17_tara(V, FI_K17_ESIK)     (Ç78: dipten sonra ∩ sonra ∪, K17 Y1)
  col   = FON_IZI.fi_k24_tara(d, FI_K24) 'kural' günleri (K24 iki evre çöl; yalnız AYRIM için)
  'Gerçek dip' = dip16 ya da dip17. Sinyal günü t = tarayıcının bilgi / tarih günü (yalnız t'ye kadar bilgi).
  Zorunlu düzeltme (sonuç görülmeden, ön kayıtta): FON_IZI tarayıcıları hisse geçmişi kısa ise (k13/k17 n < 400, k24 n < 200) TÜM seriyi
  atlar; bu şart serinin TOPLAM uzunluğuna (gelecek dahil) bakar. Burada sinyal ancak t günü itibarıyla hissenin geçmişi o uzunluğa
  ulaşmışsa (bar konumu i >= 399 / 199) tutulur: seri t'de kesilse de aynı sinyal çıkar (geleceğe bakma testi).

KÜMELER (gerçek zamanlı; t günü yalnız [t-60, t] bilgisiyle sınıflanır; 60 = hissenin kendi geçerli bar takvimi):
  A yalnız dip : dip sinyali t, [t-60, t] içinde çöl sinyali yok
  B yalnız çöl : çöl sinyali t, [t-60, t] içinde dip sinyali yok
  C ikisi      : t'de bir türün sinyali, [t-60, t] içinde öteki türün sinyali (birleşim günü = geç olan sinyal günü)
  D hiçbiri    : A ∪ B ∪ C ham sinyal günlerinin her biri için aynı gün, aynı pazar, o gün geçerli barı olan ve [t-60, t] içinde hiçbir
                 sinyali olmayan rastgele hisse (tohum 1414); yalnız rapor (eş taban zaten 'hiçbiri'ni temsil eder)
  Bir dip olayı t'de A olup sonradan (t+1..t+60) bir çöl gelirse o çöl günü C olur: ikisi de gerçek zamanlı doğrudur (sayım ayrı yazılır).
ÖLÇÜ: her küme ORTAK_CETVEL oc_olc ile (aynı cetvel). AYRIM: her karar hücresinde (ABD / AVR x 2023 / 2024-26) KAT_C − KAT_A ve
  KAT_C − KAT_B (250 gün +%100 ve -%50 eş katı; ay kümeli ortak bootstrap 2000, tohum 27, %95) ve eşli fark farkı (bilgi).
  'AYRIM VAR' (hücre): +%100 kat farkının alt ucu > 0 hem A'ya hem B'ye karşı VE -%50 kat farkının alt ucu > 0 DEĞİL (ikisine karşı).
  Genel: dört karar hücresi VAR -> AYRIM VAR; en az bir hücre VAR -> EMARE; hiçbiri VAR değil ve dört hücrede C n250 >= 1.000 (OC_ESIK
  etiket n_yeter) -> AYRIM YOK; aksi (C / A / B n250 < 30 ya da C n250 < 1.000) -> ÖLÇÜLEMEDİ.

Komut:  python DIP_COL_AYRIM.py onkayit   sinyalleri tarar (getiri yok), olay sayımını + mühürleri ön kayda yazar
        python DIP_COL_AYRIM.py kos       oc_kapi + mühür + git kapısı; dört küme + dip tümü ölçümü; satır verisi /tmp/dip_col_ayrim/; json + rapor
        python DIP_COL_AYRIM.py rapor     json + satır verisinden raporu yeniden yazar
Colab:  exec(open('DIP_COL_AYRIM.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   ORTAK_CETVEL.oc_veri (V_*.pkl + ABD k34_yahoo). Tiingo / ücretli veri YOK. Hayatta kalma yanlılığı: evren bugün işlem görenler.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_DCA = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import inspect  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_DCA = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_DCA not in sys.path:
    sys.path.insert(0, KOK_DCA)

import ORTAK_CETVEL as OC  # noqa: E402

dcalog = logging.getLogger("col.dip_col_ayrim")
if not dcalog.handlers:
    _dca_h = logging.StreamHandler(sys.stderr)
    _dca_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s dip_col_ayrim: %(message)s", "%H:%M:%S"))
    dcalog.addHandler(_dca_h)
    dcalog.setLevel(logging.INFO)
    dcalog.propagate = False

DCA_SURUM = "DIP_COL_AYRIM v1.0 (2026-11-14)"
DCA_YOL = {"cikti": os.path.join(KOK_DCA, "arastirma_cikti", "dip_col_ayrim"), "satir": "/tmp/dip_col_ayrim",
           "kod": os.path.join(KOK_DCA, "DIP_COL_AYRIM.py"),
           "karne_hucre": os.path.join(KOK_DCA, "arastirma_cikti", "iz_karne", "karne_hucre.csv")}
DCA_DOSYA = {"onkayit": "DIP_COL_AYRIM_ON_KAYIT.md", "rapor": "DIP_COL_AYRIM_RAPOR.md", "json": "dip_col_ayrim_sonuc.json",
             "sinyal": "sinyaller.csv.gz"}

# ================================================================ TASARIM (ön kayıtta sha ile mühürlü; sonuç görüldükten sonra DEĞİŞMEZ)
DCA_TASARIM: Dict[str, Any] = {
    "surum": "1.0",
    "sinyal": {"dip16": "FON_IZI.fi_k13_tara(V, FON_IZI.FI_K16_GEVSEK) bilgi günü (Ç75)",
               "dip17": "FON_IZI.fi_k17_tara(V, FON_IZI.FI_K17_ESIK) bilgi günü (Ç78, K17 Y1)",
               "col": "FON_IZI.fi_k24_tara(d, FON_IZI.FI_K24) kural == True tarih günü (K24 iki evre)",
               "dip": ["dip16", "dip17"], "veri": "ORTAK_CETVEL.oc_veri temiz seriler (geçerli bar süzgeci, kriz kesiği) üzerinde tarama"},
    "gecmis_asgari": {"dip16": 400, "dip17": 400, "col": 200,
                      "tanim": "FON_IZI tarayıcıları seri uzunluğu (gelecek dahil) < 400 / 200 ise hisseyi atlar; burada sinyal ancak bar konumu "
                               "i >= asgari-1 ise tutulur (t günü geçmişi yeterli): geleceğe bakma düzeltmesi, sonuç görülmeden"},
    "pencere": 60,
    "pencere_tanim": "hissenin kendi geçerli bar takviminde [i-60, i] (dahil): t günü i'de öteki türün sinyali bu aralıkta varsa C",
    "kume": {"A": "dip t, [t-60, t] çöl yok", "B": "çöl t, [t-60, t] dip yok", "C": "t'de bir tür, [t-60, t] öteki tür; aynı (sembol, gün) tek",
             "D": "A ∪ B ∪ C ham sinyal günü başına aynı gün aynı pazar rastgele hisse: o gün geçerli bar, [t-60, t] hiçbir sinyal yok, "
                  "evren_bas <= t; en çok 200 deneme; tohum 1414 + pazar sırası",
             "DIP_TUM": "bütün dip sinyalleri (A ∪ C'nin dip günleri); yalnız uzaklık kovası bilgisi"},
    "D_tohum": 1414, "D_deneme": 200,
    "ayrim": {"olcu": ["up100", "dn50"], "ref": ["A", "B"], "bootstrap": "OC_ESIK olcu bootstrap (2000), tohum 27, guven [0.025, 0.975]",
              "kume": "giriş ayı; C ve ref'in aylarının birleşimi yerine koyarak çekilir, iki kümenin seçilen aylardaki toplamlarıyla KAT_C - KAT_ref",
              "hucre_var": "up100 kat farkı alt95 > 0 (A'ya ve B'ye karşı) VE dn50 kat farkı alt95 > 0 değil (A'ya ve B'ye karşı)",
              "hucre_yok": "VAR değil VE C n250 >= OC_ESIK etiket n_yeter (1.000) VE A, B n250 >= 30",
              "olculemedi": "C, A ya da B n250 < 30; ya da VAR değil ve C n250 < 1.000",
              "genel": "4 karar hücresi VAR -> AYRIM VAR; >= 1 VAR -> EMARE (AYRIM; hücreler); 4 hücre YOK -> AYRIM YOK; aksi ÖLÇÜLEMEDİ",
              "coklu": "karar dört hücre x iki referansın KESİŞİMİ (hepsi tutmalı; intersection-union): BH gerekmez; EMARE yalnız bilgi",
              "fark_r60": "ortalama eşli fark farkı C - ref, aynı ay kümeli ortak bootstrap (bilgi)"},
    "uzaklik_kova": [[0, 10], [11, 30], [31, 60], [61, 120], [121, 250], [251, None]],
    "uzaklik_tanim": "dip sinyali i ile en yakın ÖNCEKİ (<= i) çöl sinyali arasındaki bar; hiç yoksa son kova; yalnız bilgi (ABD + AVR, 2023 + 2024-26 birlikte)",
    "pazar": ["ABD", "AVR", "BIST"],
}

DCA_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = ORTAK_CETVEL oc_olc (aynı giriş günü, aynı pazar, momentum beşlisi x likidite üçlüsü; 200 plasebo portföy); her küme "
                   "AYNI cetvelle; AYRIM kümeler arası kat farkıdır (C vs A, C vs B), ikisi de eşe göre kat; mekanik üstünlük: C tanımı (iki sinyal "
                   "60 günde) çöküş sonrası bağlamı seçer, A ve B de çöküş sonrası (dip16/dip17 >= %40 düşüş, K24 >= %30 düşüş): bağlam benzer; "
                   "D aynı gün rastgele hisse (bilgi)"),
    "K2": ("EVET", "tarayıcılar t'de yalnız <= t barlarını kullanır; seri uzunluğu şartı (FON_IZI n < 400 / 200) geleceğe bakıyordu -> bar konumu "
                   "i >= 399 / 199 süzgeci; küme sınıfı yalnız [t-60, t]; test_dip_col_ayrim 'kesme' testi (sentetik) + kos'ta gerçek ABD "
                   "örnekleminde seri t'de kesilince sinyal aynı (dca_gelecek_denetim)"),
    "K3": ("EVET", "tarama OC.oc_veri temiz seriler üzerinde (H>L, V>0, O/H/L/C>0); sinyal barı geçersizse oc_olay_hazirla düşürür"),
    "K4": ("EVET", "her küme oc_olc içinde hissede 60 işlem gününde tek olay; C içinde aynı (sembol, gün) tek; n = bağımsız olay; medyan raporda"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar açılışı (oc_olay_hazirla)"),
    "K6": ("EVET", "tek kip fi_k1_veri düzeltilmiş V_*.pkl (+k34_yahoo); getiri oranı; AVR likidite EUR; bölünme şüphesi OC geçmiş penceresi"),
    "K7": ("EVET", "evren bugün işlem görenler (+ ABD k34 nakdi biten, yine yaşayan); batanlar yok; raporda 'yukarı yanlı / -%50 aşağı yanlı'"),
    "K8": ("EVET", "3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; ayrım YOK yalnız C n250 >= 1.000; kesişim kuralı (BH gerekmez, ön kayıtta); "
                   "olay sayıları ön kayıtta getiri hesaplanmadan"),
    "K9": ("EVET", "ön kayıtta CETVEL / KOD / GÜÇ sha (oc_kapi_satirlari), DCA_PARAM_SHA (FI_K16_GEVSEK, FI_K17_ESIK, FI_K24 + tarayıcı kaynak "
                   "kodu), DCA_TASARIM_SHA, DCA_KOD_SHA, SINYAL_SHA; kos önce oc_kapi + dca_kapi (git işlenmiş, değişmemiş) çağırır"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV; 3 olay ham veriden elle denetimde yeniden hesaplanır"),
    "K11": ("EVET", "satır verisi /tmp/dip_col_ayrim/olay_<küme>.csv.gz; rapor sonrası >= 2 hücre (C ve A ABD 2024-26) bağımsız kodla "
                    "yeniden üretilir; ayrım bootstrap'ı satır verisinden"),
    "K12": ("EVET", "etiketler yalnız oc_etiket / oc_olasilik_etiket ve ön kayıtlı ayrım kuralıyla; fiyat değişimi, komisyon yok; sayı / yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_dca; yasak dosyalara dokunulmaz (git diff --stat); e-posta / anahtar taraması testte; "
                    "ücretli veri / Tiingo yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm"),
}


class DCAHata(RuntimeError):
    """Durdurucu hata: mühür / sha tutmuyor, ön kayıt işlenmemiş, veri yok."""


# ================================================================ 0) ORTAK
def _dca_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _dca_sha_metin(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _dca_F():
    import FON_IZI as F   # kütüphane olarak içe alınır; FON_IZI kendi çakışma kapısını taşır
    return F


DCA_FONKSIYON = ("fi_k13_tara", "fi_k13_olc", "fi_k17_tara", "fi_k17_olc", "_fi_k17_parabol", "fi_k24_tara", "_fi_k23_yon")


def dca_param() -> Dict[str, Any]:
    """Sinyal parametre sözlükleri + tarayıcı fonksiyonlarının kaynak kodu sha'sı (FON_IZI'den, değiştirilmeden)."""
    F = _dca_F()
    kaynak = {ad: _dca_sha_metin(inspect.getsource(getattr(F, ad))) for ad in DCA_FONKSIYON}
    return {"FI_K16_GEVSEK": F.FI_K16_GEVSEK, "FI_K17_ESIK": F.FI_K17_ESIK, "FI_K24": F.FI_K24, "kaynak_sha": kaynak}


def dca_param_sha() -> str:
    return _dca_sha_metin(json.dumps(dca_param(), sort_keys=True, default=str, ensure_ascii=False))


def dca_tasarim_sha() -> str:
    return _dca_sha_metin(json.dumps(DCA_TASARIM, sort_keys=True, default=str, ensure_ascii=False))


def dca_kod_sha(yol: Optional[str] = None) -> str:
    return OC._oc_sha_dosya(yol or DCA_YOL["kod"])


def dca_sinyal_sha(S: pd.DataFrame) -> str:
    x = S[["pazar", "sembol", "tarih", "tur", "i"]].copy()
    x["tarih"] = pd.to_datetime(x.tarih).dt.strftime("%Y-%m-%d")
    x = x.sort_values(["pazar", "sembol", "tarih", "tur"]).reset_index(drop=True)
    return _dca_sha_metin(x.to_csv(index=False))


# ================================================================ 1) SİNYAL TARAMA (yalnız t'ye kadar bilgi)
def dca_tara_hisse(s: str, d: pd.DataFrame) -> List[Tuple[str, pd.Timestamp, str, int]]:
    """Tek hisse: dip16 / dip17 / col sinyal günleri (sembol, tarih, tur, bar konumu i). Geçmiş asgari süzgeci uygulanır."""
    F = _dca_F(); G = DCA_TASARIM["gecmis_asgari"]; out = []
    konum = {t: i for i, t in enumerate(d.index)}
    for tur, fn in (("dip16", lambda: F.fi_k13_tara({s: d}, F.FI_K16_GEVSEK)), ("dip17", lambda: F.fi_k17_tara({s: d}, F.FI_K17_ESIK))):
        O = fn()
        if len(O):
            for b in pd.to_datetime(O.bilgi):
                i = konum[pd.Timestamp(b)]
                if i >= G[tur] - 1:
                    out.append((s, pd.Timestamp(b), tur, i))
    try:
        T = F.fi_k24_tara(d, F.FI_K24)
    except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer
        dcalog.warning("k24 %s atlandı: %s", s, ex); T = pd.DataFrame()
    if len(T) and "kural" in T:
        for b in pd.to_datetime(T[T.kural].tarih):
            i = konum[pd.Timestamp(b)]
            if i >= G["col"] - 1:
                out.append((s, pd.Timestamp(b), "col", i))
    return out


def dca_tara(Vd: Dict[str, Any]) -> pd.DataFrame:
    """Pazarın bütün hisseleri -> sinyal tablosu (pazar, sembol, tarih, tur, i)."""
    sat = []
    for s, d in Vd["V"].items():
        try:
            sat += dca_tara_hisse(s, d)
        except Exception as ex:
            dcalog.warning("%s %s atlandı: %s", Vd.get("pazar"), s, ex)
    S = pd.DataFrame(sat, columns=["sembol", "tarih", "tur", "i"])
    S.insert(0, "pazar", Vd.get("pazar", "?"))
    return S.sort_values(["sembol", "tarih", "tur"]).reset_index(drop=True)


# ================================================================ 2) KÜMELER
def dca_kume(S: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Sinyal tablosu (tek ya da çok pazar) -> A, B, C, DIP_TUM olay tabloları (sembol, tarih, pazar, + bilgi sütunları). Yalnız [i-60, i]."""
    w = DCA_TASARIM["pencere"]; A, B, C, DT = [], [], [], []
    for (pz, s), g in S.groupby(["pazar", "sembol"], sort=True):
        dip = g[g.tur.isin(DCA_TASARIM["sinyal"]["dip"])]; col = g[g.tur == "col"]
        ci = np.sort(col.i.to_numpy()); di = np.sort(dip.i.to_numpy())
        for r in dip.itertuples():
            once = ci[ci <= r.i]
            uz = int(r.i - once.max()) if len(once) else -1
            DT.append((s, r.tarih, pz, r.tur, uz))
            if len(once) and r.i - once.max() <= w:
                C.append((s, r.tarih, pz, "dip_gec", r.tur, uz))
            else:
                A.append((s, r.tarih, pz, r.tur, uz))
        for r in col.itertuples():
            once = di[di <= r.i]
            if len(once) and r.i - once.max() <= w:
                tr = ",".join(sorted(set(dip[(dip.i <= r.i) & (dip.i >= r.i - w)].tur)))
                C.append((s, r.tarih, pz, "col_gec", tr, int(r.i - once.max())))
            else:
                B.append((s, r.tarih, pz))
    Ad = pd.DataFrame(A, columns=["sembol", "tarih", "pazar", "dip_tur", "uzaklik"])
    Bd = pd.DataFrame(B, columns=["sembol", "tarih", "pazar"])
    Cd = pd.DataFrame(C, columns=["sembol", "tarih", "pazar", "gec", "dip_tur", "uzaklik"])
    if len(Cd):   # aynı (sembol, gün) tek: dip ve çöl aynı gün -> tek C
        Cd = Cd.sort_values(["pazar", "sembol", "tarih", "gec"]).drop_duplicates(["pazar", "sembol", "tarih"]).reset_index(drop=True)
    Dt = pd.DataFrame(DT, columns=["sembol", "tarih", "pazar", "dip_tur", "uzaklik"])
    if len(Dt):   # dip16 ve dip17 aynı gün -> tek satır
        Dt = Dt.drop_duplicates(["pazar", "sembol", "tarih"]).reset_index(drop=True)
    return {"A": Ad, "B": Bd, "C": Cd, "DIP_TUM": Dt}


def dca_D(S: pd.DataFrame, Vd: Dict[str, Any], kumeler: Dict[str, pd.DataFrame], pazar_sira: int) -> pd.DataFrame:
    """D (hiçbiri): A ∪ B ∪ C ham sinyal günleri başına aynı gün aynı pazar rastgele hisse; o gün geçerli bar, [t-60, t] sinyal yok."""
    w = DCA_TASARIM["pencere"]; rng = np.random.default_rng(DCA_TASARIM["D_tohum"] + pazar_sira)
    pz = Vd["pazar"]; V = Vd["V"]; sem = sorted(V); evb = Vd.get("evren_bas", {})
    sig = {s: np.sort(g.i.to_numpy()) for s, g in S[S.pazar == pz].groupby("sembol")}
    gunler = pd.concat([kumeler[k][kumeler[k].pazar == pz][["tarih"]] for k in ("A", "B", "C")], ignore_index=True)
    sat = []
    for t in pd.to_datetime(gunler.tarih).sort_values():
        for _ in range(DCA_TASARIM["D_deneme"]):
            s = sem[int(rng.integers(len(sem)))]; ix = V[s].index
            k = ix.searchsorted(t)
            if k >= len(ix) or ix[k] != t or (s in evb and pd.Timestamp(evb[s]) > t):
                continue
            si = sig.get(s)
            if si is not None and ((si <= k) & (si >= k - w)).any():
                continue
            sat.append((s, t, pz)); break
    return pd.DataFrame(sat, columns=["sembol", "tarih", "pazar"])


def dca_sayim(S: pd.DataFrame, K: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Olay sayımı (getiri yok): pazar x dönem (sinyal günü) x {ham sinyal türleri, A, B, C, DIP_TUM}."""
    E = OC.OC_ESIK; sat = []
    for pz in DCA_TASARIM["pazar"]:
        for ad, a, b in E["donem"] + [["tümü", "1900-01-01", "2100-01-01"]]:
            def say(x):
                x = x[x.pazar == pz]; t = pd.to_datetime(x.tarih)
                return int(((t >= a) & (t <= b)).sum())
            r = {"pazar": pz, "donem": ad}
            for tur in ("dip16", "dip17", "col"):
                r[tur] = say(S[S.tur == tur])
            for k in ("A", "B", "C", "DIP_TUM"):
                r[k] = say(K[k])
            Cx = K["C"][K["C"].pazar == pz]; t = pd.to_datetime(Cx.tarih)
            r["C_col_gec"] = int(((t >= a) & (t <= b) & (Cx.gec == "col_gec")).sum())
            sat.append(r)
    return pd.DataFrame(sat)


# ================================================================ 3) AYRIM (C vs ref, satır verisinden)
def dca_kat_fark(Cx: pd.DataFrame, Rx: pd.DataFrame, olcu: str, E: Dict[str, Any] = OC.OC_ESIK) -> Dict[str, float]:
    """KAT_C - KAT_ref (eş katı: Σ olay / Σ eş oranı; oc_kat ile aynı geçerli satırlar) ve ay kümeli ortak bootstrap %95."""
    O = E["olcu"]

    def hazir(X):
        if not len(X):
            return np.array([]), np.array([]), np.array([], dtype=object)
        a = X[olcu].to_numpy(float); b = X[f"es_{olcu}"].to_numpy(float); g = np.isfinite(a) & np.isfinite(b)
        m = pd.to_datetime(X.giris).dt.to_period("M").astype(str).to_numpy()
        return a[g], b[g], m[g]
    ac, bc, mc = hazir(Cx); ar, br, mr = hazir(Rx)
    out = {"n_C": int(len(ac)), "n_ref": int(len(ar)), "kat_C": np.nan, "kat_ref": np.nan, "fark": np.nan, "alt": np.nan, "ust": np.nan}
    if not len(ac) or not len(ar) or bc.sum() <= 0 or br.sum() <= 0:
        return out
    out["kat_C"] = float(ac.sum() / bc.sum()); out["kat_ref"] = float(ar.sum() / br.sum()); out["fark"] = out["kat_C"] - out["kat_ref"]
    aylar = np.unique(np.r_[mc, mr])
    gac = {x: ac[mc == x].sum() for x in aylar}; gbc = {x: bc[mc == x].sum() for x in aylar}
    gar = {x: ar[mr == x].sum() for x in aylar}; gbr = {x: br[mr == x].sum() for x in aylar}
    rng = np.random.default_rng(O["tohum"]); v = []
    for _ in range(O["bootstrap"]):
        sec = rng.choice(aylar, len(aylar), replace=True)
        pc = sum(gbc[x] for x in sec); pr = sum(gbr[x] for x in sec)
        if pc <= 0 or pr <= 0:
            continue
        v.append(sum(gac[x] for x in sec) / pc - sum(gar[x] for x in sec) / pr)
    if v:
        out["alt"] = float(np.quantile(v, O["guven"][0])); out["ust"] = float(np.quantile(v, O["guven"][1]))
    return out


def dca_fark_fark(Cx: pd.DataFrame, Rx: pd.DataFrame, E: Dict[str, Any] = OC.OC_ESIK) -> Dict[str, float]:
    """Ortalama eşli fark (r60) farkı C - ref; ay kümeli ortak bootstrap %95 (bilgi)."""
    O = E["olcu"]
    c = Cx.dropna(subset=["fark"]) if len(Cx) else Cx; r = Rx.dropna(subset=["fark"]) if len(Rx) else Rx
    out = {"n_C": int(len(c)), "n_ref": int(len(r)), "fark": np.nan, "alt": np.nan, "ust": np.nan}
    if not len(c) or not len(r):
        return out
    fc, fr = c.fark.to_numpy(float), r.fark.to_numpy(float)
    mc = pd.to_datetime(c.giris).dt.to_period("M").astype(str).to_numpy(); mr = pd.to_datetime(r.giris).dt.to_period("M").astype(str).to_numpy()
    out["fark"] = float(fc.mean() - fr.mean())
    aylar = np.unique(np.r_[mc, mr]); gc = {x: fc[mc == x] for x in aylar}; gr = {x: fr[mr == x] for x in aylar}
    rng = np.random.default_rng(O["tohum"]); v = []
    for _ in range(O["bootstrap"]):
        sec = rng.choice(aylar, len(aylar), replace=True)
        a = np.concatenate([gc[x] for x in sec]); b = np.concatenate([gr[x] for x in sec])
        if len(a) and len(b):
            v.append(a.mean() - b.mean())
    if v:
        out["alt"] = float(np.quantile(v, O["guven"][0])); out["ust"] = float(np.quantile(v, O["guven"][1]))
    return out


def dca_ayrim(Ol: Dict[str, pd.DataFrame], E: Dict[str, Any] = OC.OC_ESIK) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Ol: küme -> oc_olc olay satırları (pazar, donem, giris, fark, up100, es_up100, dn50, es_dn50). Hücre tablosu + genel ayrım etiketi."""
    n_esik = E["hucre_karar"]["n_esik"]; n_yeter = E["etiket"]["n_yeter"]; sat = []
    for pz in DCA_TASARIM["pazar"]:
        for ad, _a, _b in E["donem"]:
            def x(k):
                X = Ol.get(k, pd.DataFrame())
                return X[(X.pazar == pz) & (X.donem == ad)] if len(X) else X
            Cx = x("C"); r = {"pazar": pz, "donem": ad, "karar": pz in E["karar_pazar"] and ad in E["karar_donem"]}
            var_hepsi = True; olculemedi = False
            for ref in DCA_TASARIM["ayrim"]["ref"]:
                Rx = x(ref)
                u = dca_kat_fark(Cx, Rx, "up100", E); dn = dca_kat_fark(Cx, Rx, "dn50", E); ff = dca_fark_fark(Cx, Rx, E)
                for k, v in u.items():
                    r[f"up_{ref}_{k}"] = v
                for k, v in dn.items():
                    r[f"dn_{ref}_{k}"] = v
                for k in ("fark", "alt", "ust", "n_C", "n_ref"):
                    r[f"r60_{ref}_{k}"] = ff[k]
                if u["n_C"] < n_esik or u["n_ref"] < n_esik:
                    olculemedi = True
                v_ = bool(np.isfinite(u["alt"]) and u["alt"] > 0 and not (np.isfinite(dn["alt"]) and dn["alt"] > 0))
                r[f"var_{ref}"] = v_
                var_hepsi &= v_
            nC = int(r.get("up_A_n_C", 0))
            if olculemedi:
                durum = "ÖLÇÜLEMEDİ"
            elif var_hepsi:
                durum = "VAR"
            elif nC >= n_yeter:
                durum = "YOK"
            else:
                durum = "ÖLÇÜLEMEDİ"
            r["durum"] = durum
            sat.append(r)
    T = pd.DataFrame(sat)
    K = T[T.karar]
    dur = list(K.durum)
    if dur and all(d == "VAR" for d in dur):
        genel = "AYRIM VAR"
    elif any(d == "VAR" for d in dur):
        genel = "EMARE (AYRIM; " + ", ".join(f"{a} {b}" for a, b, d in zip(K.pazar, K.donem, dur) if d == "VAR") + ")"
    elif dur and all(d == "YOK" for d in dur):
        genel = "AYRIM YOK"
    else:
        genel = "ÖLÇÜLEMEDİ"
    return T, {"genel": genel, "karar_hucre": {f"{a} {b}": d for a, b, d in zip(K.pazar, K.donem, dur)}}


def dca_uzaklik(X: pd.DataFrame, E: Dict[str, Any] = OC.OC_ESIK) -> pd.DataFrame:
    """DIP_TUM satırları (uzaklik sütunlu) -> kova başına n, ortalama eşli fark, +%100 / -%50 eş katı (oc_kat). ABD + AVR, 2023 + 2024-26."""
    X = X[X.pazar.isin(E["karar_pazar"]) & X.donem.isin(E["karar_donem"])] if len(X) else X
    sat = []
    for a, b in DCA_TASARIM["uzaklik_kova"]:
        if b is None:
            m = (X.uzaklik >= a) | (X.uzaklik < 0)
            ad = f">= {a} ya da çöl yok"
        else:
            m = (X.uzaklik >= a) & (X.uzaklik <= b)
            ad = f"{a}-{b}"
        x = X[m]; ay = pd.to_datetime(x.giris).dt.to_period("M").astype(str).to_numpy() if len(x) else np.array([], dtype=object)
        u = OC.oc_kat(x.up100.to_numpy(float), x.es_up100.to_numpy(float), ay, E) if len(x) else {"n": 0}
        d = OC.oc_kat(x.dn50.to_numpy(float), x.es_dn50.to_numpy(float), ay, E) if len(x) else {"n": 0}
        f = x.fark.dropna() if len(x) else pd.Series(dtype=float)
        sat.append({"kova": ad, "n": int(len(x)), "n_fark": int(len(f)), "ort_fark": float(f.mean()) if len(f) else np.nan,
                    "n250": u.get("n", 0), "up_kat": u.get("kat"), "up_alt": u.get("alt"), "up_ust": u.get("ust"),
                    "dn_kat": d.get("kat"), "dn_alt": d.get("alt"), "dn_ust": d.get("ust")})
    return pd.DataFrame(sat)


def dca_eski_kiyas() -> pd.DataFrame:
    """Eski Ç75 / Ç78 sonuçları (IZ_KARNE karne_hucre.csv; yeniden ÖLÇÜLMEZ): n, önce +%20 oranı, eşli taban, kat."""
    yol = DCA_YOL["karne_hucre"]
    if not os.path.exists(yol):
        return pd.DataFrame()
    K = pd.read_csv(yol)
    K = K[K.kod.isin(["Ç75", "Ç78"])][["kod", "pazar", "donem", "n", "ana", "ana_esli", "ana_kat", "ters_kat"]]
    return K.reset_index(drop=True)


# ================================================================ 4) GELECEĞE BAKMA DENETİMİ (gerçek veri örneklemi)
def dca_gelecek_denetim(S: pd.DataFrame, Vd: Dict[str, Any], n_ornek: int = 25, tohum: int = 7) -> Dict[str, Any]:
    """Her türden n_ornek sinyal: seri t'de kesilince aynı tür sinyal t'de yine çıkıyor mu (yalnız t'ye kadar bilgi)."""
    rng = np.random.default_rng(tohum); out = {}
    for tur in ("dip16", "dip17", "col"):
        x = S[(S.tur == tur) & (S.pazar == Vd["pazar"])]
        if not len(x):
            out[tur] = {"n": 0, "ayni": 0}; continue
        sec = x.iloc[rng.choice(len(x), min(n_ornek, len(x)), replace=False)]
        ayni = 0; fark = []
        for r in sec.itertuples():
            d = Vd["V"][r.sembol]; d = d[d.index <= pd.Timestamp(r.tarih)]
            y = dca_tara_hisse(r.sembol, d)
            if any(t == pd.Timestamp(r.tarih) and tt == tur for _s, t, tt, _i in y):
                ayni += 1
            else:
                fark.append(f"{r.sembol} {pd.Timestamp(r.tarih).date()}")
        out[tur] = {"n": int(len(sec)), "ayni": int(ayni), "fark": fark[:10]}
    return out


# ================================================================ 5) ÖN KAYIT
def _dca_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = DCA_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def _md_tablo(T: pd.DataFrame) -> str:
    if not len(T):
        return "(boş)"
    s = ["| " + " | ".join(map(str, T.columns)) + " |", "|" + "---|" * len(T.columns)]
    for r in T.itertuples(index=False):
        s.append("| " + " | ".join("-" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.3f}" if isinstance(v, float) else str(v)) for v in r) + " |")
    return "\n".join(s)


def dca_veri_tara(pazarlar: Optional[List[str]] = None) -> pd.DataFrame:
    """Bütün pazarlarda sinyal tarama; sinyal tablosu /tmp/dip_col_ayrim/sinyaller.csv.gz."""
    os.makedirs(DCA_YOL["satir"], exist_ok=True); L = []
    for pz in pazarlar or DCA_TASARIM["pazar"]:
        t0 = time.time(); Vd = OC.oc_veri(pz); S = dca_tara(Vd); L.append(S)
        dcalog.info("%s: %d hisse, %d sinyal (%.0f s)", pz, len(Vd["V"]), len(S), time.time() - t0)
        del Vd
    S = pd.concat(L, ignore_index=True)
    S.to_csv(os.path.join(DCA_YOL["satir"], DCA_DOSYA["sinyal"]), index=False)
    return S


def dca_sinyal_oku() -> pd.DataFrame:
    S = pd.read_csv(os.path.join(DCA_YOL["satir"], DCA_DOSYA["sinyal"]), parse_dates=["tarih"])
    return S


def dca_onkayit_yaz(uzerine: bool = False) -> str:
    os.makedirs(DCA_YOL["cikti"], exist_ok=True)
    yol = os.path.join(DCA_YOL["cikti"], DCA_DOSYA["onkayit"])
    if os.path.exists(yol) and not uzerine:
        raise DCAHata(f"ön kayıt var: {yol} (git'e işlenmişse üzerine yazılmaz)")
    S = dca_veri_tara(); K = dca_kume(S); Z = dca_sayim(S, K)
    P = dca_param()
    s = [f"# DIP_COL_AYRIM — ÖN KAYIT ({DCA_SURUM})", "",
         f"Yazım: {_dca_simdi()}. Bu dosya ölçümden ÖNCE yazıldı: yalnız sinyaller tarandı ve sayıldı; hiçbir getiri / olasılık hesaplanmadı.", "",
         "Soru (Cemal, 14 Kas 2026): çöl formasyonuyla gerçek dip oluşumunu birbirinden ayırabiliyor muyuz?", "",
         "## Tanım", "",
         "- dip16 = `FON_IZI.fi_k13_tara(V, FI_K16_GEVSEK)` (Ç75 düzgün dip gevşek), dip17 = `FON_IZI.fi_k17_tara(V, FI_K17_ESIK)` (Ç78 iki yuvarlama Y1), "
         "col = `FON_IZI.fi_k24_tara(d, FI_K24)` kural günleri (K24 iki evre). Kod DEĞİŞTİRİLMEDİ; FON_IZI içe alınır.",
         "- 'Gerçek dip' = dip16 ya da dip17; 'çöl' = col. Sinyal günü t; giriş t'den sonraki ilk geçerli bar açılışı (ORTAK_CETVEL).",
         "- Kümeler (gerçek zamanlı, yalnız [t-60, t]): A yalnız dip, B yalnız çöl, C ikisi (geç olan sinyal günü), D aynı gün rastgele 'hiçbiri' (bilgi).",
         "- AYRIM kuralı: DCA_TASARIM 'ayrim' (aşağıda tam metin). Karar hücreleri ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26; BIST bilgi; 2016-22 keşif.",
         "- Zorunlu düzeltme (sonuç görülmeden): FON_IZI tarayıcıları seri TOPLAM uzunluğu < 400 / 200 ise hisseyi atlar (geleceğe bakma); "
         "burada sinyal ancak bar konumu i >= 399 (dip) / 199 (çöl) ise tutulur.", "",
         "## Mühür satırları", "", OC.oc_kapi_satirlari(),
         f"DCA_PARAM_SHA: `{dca_param_sha()}`", f"DCA_TASARIM_SHA: `{dca_tasarim_sha()}`", f"DCA_KOD_SHA: `{dca_kod_sha()}`",
         f"SINYAL_SHA: `{dca_sinyal_sha(S)}`", "",
         "- DCA_PARAM_SHA = sha256(FI_K16_GEVSEK, FI_K17_ESIK, FI_K24 + tarayıcı fonksiyonlarının kaynak sha'sı; JSON sort_keys). "
         "DCA_KOD_SHA = sha256(DIP_COL_AYRIM.py). SINYAL_SHA = sha256(sıralı sinyal tablosu CSV; pazar, sembol, tarih, tur, i).", "",
         "## Parametre sözlüğü (FON_IZI'den)", "", "```json", json.dumps(P, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
         "## Tasarım (DCA_TASARIM; mühürlü)", "", "```json", json.dumps(DCA_TASARIM, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
         "## OLAY SAYIMI (getiri hesaplanmadan; ham sinyal günü dönemine göre; oc_olc tekilleştirmesinden ÖNCE)", "", _md_tablo(Z), "",
         "- C_col_gec: C olaylarından çöl sinyalinin geç geldiği (dip önce, çöl sonra) olanlar; kalanı dip geç.",
         "- Not: bir dip olayı A sayılıp 60 gün içinde gelen çölle C de olabilir (gerçek zamanlı sınıf).", "",
         _dca_kontrol_tablosu(), "",
         "## Test", "", "`python test_dip_col_ayrim.py` (sentetik: sinyal tespiti, kümeleme, geleceğe bakma kesme testi, cetvel çağrısı, ayrım "
         "kuralı, kapı, çakışma kapısı, e-posta / anahtar taraması).", ""]
    with open(yol, "w", encoding="utf-8") as f:
        f.write("\n".join(s))
    return yol


# ================================================================ 6) KAPI ve KOŞU
_DCA_DESEN = {"param": r"DCA_PARAM_SHA:\s*`?([0-9a-f]{64})`?", "tasarim": r"DCA_TASARIM_SHA:\s*`?([0-9a-f]{64})`?",
              "kod": r"DCA_KOD_SHA:\s*`?([0-9a-f]{64})`?", "sinyal": r"SINYAL_SHA:\s*`?([0-9a-f]{64})`?"}


def dca_kapi(onkayit_yolu: Optional[str] = None, git: bool = True, S: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """oc_kapi (kontrol listesi + cetvel sha + git) + DCA mühürleri (param / tasarım / kod / sinyal sha) + modül git işlenmiş ve değişmemiş."""
    yol = onkayit_yolu or os.path.join(DCA_YOL["cikti"], DCA_DOSYA["onkayit"])
    try:
        out = {"oc": OC.oc_kapi(yol, git=git)}
    except OC.OCHata as ex:
        raise DCAHata(f"oc_kapi KAPALI: {ex}")
    metin = open(yol, encoding="utf-8").read(); bul = {}
    for ad, d in _DCA_DESEN.items():
        m = re.search(d, metin)
        if not m:
            raise DCAHata(f"ön kayıtta {ad} sha satırı yok")
        bul[ad] = m.group(1)
    simdi = {"param": dca_param_sha(), "tasarim": dca_tasarim_sha(), "kod": dca_kod_sha()}
    if S is not None:
        simdi["sinyal"] = dca_sinyal_sha(S)
    for ad, v in simdi.items():
        if bul[ad] != v:
            raise DCAHata(f"{ad} sha tutmuyor: ön kayıt {bul[ad][:12]}…, şimdi {v[:12]}…; koşu DURDU")
    if git:
        out["git_kod"] = OC._oc_git_islenmis(DCA_YOL["kod"])
    out.update(bul)
    dcalog.info("dca_kapi AÇIK")
    return out


def _dca_birlestir(parca: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Pazar başına oc_olc çıktılarını tek S'ye birleştirir; etiket OC.oc_etiket ile yeniden (bütün pazarlar)."""
    T = pd.concat([p["hucre"] for p in parca if len(p["hucre"])], ignore_index=True) if parca else pd.DataFrame()
    Ol = pd.concat([p["olay"] for p in parca if len(p["olay"])], ignore_index=True) if parca else pd.DataFrame()
    Ob = pd.concat([p["olasilik"] for p in parca if len(p["olasilik"])], ignore_index=True) if parca else pd.DataFrame()
    say = {}
    for p in parca:
        say.update(p["sayim"])
    et = OC.oc_etiket(T) if len(T) else {"genel": "VERİ YOK", "olasilik": "ÖLÇÜLEMEDİ", "karar_hucre": {}}
    return {"hucre": T, "olay": Ol, "olasilik": Ob, "sayim": say, "etiket": et, "cetvel_sha": OC.oc_esik_sha(),
            "kod_sha": OC.oc_kod_sha(), "surum": OC.OC_SURUM}


def dca_kos() -> Dict[str, Any]:
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    yol_s = os.path.join(DCA_YOL["satir"], DCA_DOSYA["sinyal"])
    S = dca_sinyal_oku() if os.path.exists(yol_s) else dca_veri_tara()
    kapi = dca_kapi(S=S)
    bas = _dca_simdi(); K = dca_kume(S)
    kumeler = ("A", "B", "C", "D", "DIP_TUM")
    parca: Dict[str, List[Dict[str, Any]]] = {k: [] for k in kumeler}; gelecek = {}; Dset = []
    for si, pz in enumerate(DCA_TASARIM["pazar"]):
        t0 = time.time(); Vd = OC.oc_veri(pz)
        if pz == "ABD":
            gelecek[pz] = dca_gelecek_denetim(S, Vd)
        D = dca_D(S, Vd, K, si); Dset.append(D)
        P = OC.oc_panel(Vd)
        for k in kumeler:
            X = D if k == "D" else K[k][K[k].pazar == pz]
            r = OC.oc_olc(X[["sembol", "tarih", "pazar"]], {pz: P})
            Ol = r["olay"]
            if k in ("C", "A", "DIP_TUM") and len(Ol):
                ek = K[k][K[k].pazar == pz].drop(columns=["pazar"]).drop_duplicates(["sembol", "tarih"])
                Ol = Ol.merge(ek, on=["sembol", "tarih"], how="left")
            r["olay"] = Ol
            parca[k].append(r)
            dcalog.info("%s %s: girdi %d, ölçülen %d", pz, k, len(X), len(Ol))
        del P, Vd
        dcalog.info("%s bitti (%.0f s)", pz, time.time() - t0)
    os.makedirs(DCA_YOL["satir"], exist_ok=True)
    SS = {k: _dca_birlestir(parca[k]) for k in kumeler}
    for k in kumeler:
        SS[k]["olay"].to_csv(os.path.join(DCA_YOL["satir"], f"olay_{k}.csv.gz"), index=False)
    Ol = {k: SS[k]["olay"] for k in kumeler}
    AT, AE = dca_ayrim(Ol)
    UZ = dca_uzaklik(SS["DIP_TUM"]["olay"]) if len(SS["DIP_TUM"]["olay"]) else pd.DataFrame()
    J = {"surum": DCA_SURUM, "baslangic_utc": bas, "bitis_utc": _dca_simdi(), "kapi": {k: v for k, v in kapi.items() if k != "oc"},
         "onkayit_git": kapi["oc"].get("git"), "cetvel_sha": OC.oc_esik_sha(), "param_sha": dca_param_sha(), "tasarim_sha": dca_tasarim_sha(),
         "kod_sha": dca_kod_sha(), "sinyal_sha": dca_sinyal_sha(S), "gelecek_denetim": gelecek,
         "sayim_onkayit": dca_sayim(S, K).to_dict("records"), "D_n": int(sum(len(x) for x in Dset)),
         "kume": {k: {"hucre": SS[k]["hucre"].to_dict("records"), "olasilik": SS[k]["olasilik"].to_dict("records"), "sayim": SS[k]["sayim"],
                      "etiket": SS[k]["etiket"]} for k in kumeler},
         "ayrim": AT.to_dict("records"), "ayrim_etiket": AE, "uzaklik": UZ.to_dict("records"),
         "eski": dca_eski_kiyas().to_dict("records")}
    with open(os.path.join(DCA_YOL["cikti"], DCA_DOSYA["json"]), "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1, default=lambda o: None if (isinstance(o, float) and not np.isfinite(o)) else str(o))
    dca_rapor(J)
    return J


# ================================================================ 7) RAPOR
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


def _S_json(Jk: Dict[str, Any]) -> Dict[str, Any]:
    return {"hucre": pd.DataFrame(Jk["hucre"]), "olasilik": pd.DataFrame(Jk["olasilik"]), "sayim": Jk["sayim"], "etiket": Jk["etiket"],
            "surum": OC.OC_SURUM, "cetvel_sha": OC.oc_esik_sha(), "kod_sha": OC.oc_kod_sha()}


def _ol(Jk: Dict[str, Any], pz: str, dn: str) -> Dict[str, Any]:
    for r in Jk["olasilik"]:
        if r["pazar"] == pz and r["donem"] == dn:
            return r
    return {}


def _hc(Jk: Dict[str, Any], pz: str, dn: str) -> Dict[str, Any]:
    for r in Jk["hucre"]:
        if r["pazar"] == pz and r["donem"] == dn:
            return r
    return {}


def dca_rapor(J: Optional[Dict[str, Any]] = None) -> str:
    if J is None:
        J = json.load(open(os.path.join(DCA_YOL["cikti"], DCA_DOSYA["json"]), encoding="utf-8"))
    E = OC.OC_ESIK; KU = J["kume"]; AE = J["ayrim_etiket"]
    ad = {"A": "A yalnız dip", "B": "B yalnız çöl", "C": "C dip + çöl (60 gün)", "D": "D hiçbiri (aynı gün rastgele)", "DIP_TUM": "Bütün dip sinyalleri"}
    s = [f"# DIP_COL_AYRIM — RAPOR ({DCA_SURUM})", "",
         f"Koşu {J['baslangic_utc']} – {J['bitis_utc']}; ön kayıt commit {(J.get('onkayit_git') or {}).get('commit', '-')} "
         f"({(J.get('onkayit_git') or {}).get('commit_zamani', '-')}). Cetvel {OC.OC_SURUM}.", "",
         "## DÜZ DİL ÖZET", ""]
    # özet satırları (sayılar json'dan)
    oz = [f"- **AYRIM: {AE['genel']}** (karar hücreleri: " + ", ".join(f"{k} {v}" for k, v in AE["karar_hucre"].items()) + ")."]
    for k in ("A", "B", "C", "D"):
        et = KU[k]["etiket"]
        nn = ", ".join(f"{pz} {dn} n {int(_hc(KU[k], pz, dn).get('n', 0) or 0)} / n250 {int(_ol(KU[k], pz, dn).get('n250', 0) or 0)}"
                       for pz in E["karar_pazar"] for dn in E["karar_donem"])
        oz.append(f"- {ad[k]}: genel {et['genel']}, olasılık {et['olasilik']} ({nn}).")
    for pz in E["karar_pazar"]:
        for dn in E["karar_donem"]:
            p = [f"{k} {_sy(_ol(KU[k], pz, dn).get('up100_es_kat'))}" for k in ("A", "B", "C", "D")]
            q = [f"{k} {_sy(_ol(KU[k], pz, dn).get('dn50_es_kat'))}" for k in ("A", "B", "C", "D")]
            oz.append(f"- {pz} {dn}: +%100 eş katı " + ", ".join(p) + "; -%50 eş katı " + ", ".join(q) + ".")
    oz.append("- Hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı. Komisyon yok.")
    s += oz + ["", "## AYRIM TABLOSU (C vs A, C vs B; 250 gün eş katı farkı, ay kümeli ortak bootstrap %95; r60 eşli fark farkı bilgi)", "",
               "| Pazar | Dönem | K | n250 C / A / B | +%100 kat C | kat A | C−A [%95] | kat B | C−B [%95] | -%50 kat C | C−A [%95] | C−B [%95] | "
               "r60 fark C−A [%95] | C−B [%95] | durum |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in J["ayrim"]:
        def g(k):
            return r.get(k)
        s.append(f"| {r['pazar']} | {r['donem']} | {'K' if r['karar'] else 'b'} | {g('up_A_n_C')} / {g('up_A_n_ref')} / {g('up_B_n_ref')} | "
                 f"{_sy(g('up_A_kat_C'))} | {_sy(g('up_A_kat_ref'))} | {_sy(g('up_A_fark'))} [{_sy(g('up_A_alt'))}, {_sy(g('up_A_ust'))}] | "
                 f"{_sy(g('up_B_kat_ref'))} | {_sy(g('up_B_fark'))} [{_sy(g('up_B_alt'))}, {_sy(g('up_B_ust'))}] | {_sy(g('dn_A_kat_C'))} | "
                 f"{_sy(g('dn_A_fark'))} [{_sy(g('dn_A_alt'))}, {_sy(g('dn_A_ust'))}] | {_sy(g('dn_B_fark'))} [{_sy(g('dn_B_alt'))}, {_sy(g('dn_B_ust'))}] | "
                 f"{_yz(g('r60_A_fark'))} [{_yz(g('r60_A_alt'))}, {_yz(g('r60_A_ust'))}] | {_yz(g('r60_B_fark'))} [{_yz(g('r60_B_alt'))}, {_yz(g('r60_B_ust'))}] | "
                 f"{r['durum']} |")
    s += ["", f"Kural (ön kayıt): {DCA_TASARIM['ayrim']['hucre_var']}; YOK: {DCA_TASARIM['ayrim']['hucre_yok']}; ÖLÇÜLEMEDİ: "
          f"{DCA_TASARIM['ayrim']['olculemedi']}. Genel: {DCA_TASARIM['ayrim']['genel']}.", ""]
    s += ["## Dipten çöle uzaklık (bilgi; ABD + AVR, 2023 + 2024-26; dip günü ile en yakın önceki çöl arası bar)", "",
          "| Kova (bar) | n | ort eşli fark (n) | n250 | +%100 eş katı [%95] | -%50 eş katı [%95] |", "|---|---|---|---|---|---|"]
    for r in J["uzaklik"]:
        s.append(f"| {r['kova']} | {r['n']} | {_yz(r['ort_fark'])} ({r['n_fark']}) | {r['n250']} | {_sy(r['up_kat'])} [{_sy(r['up_alt'])}, {_sy(r['up_ust'])}] | "
                 f"{_sy(r['dn_kat'])} [{_sy(r['dn_alt'])}, {_sy(r['dn_ust'])}] |")
    s += ["", "## Eski Ç75 / Ç78 kıyası (IZ_KARNE karne_hucre.csv; eski tek cetvel 'önce +%20 / eşli taban', yeniden ölçülmedi) ve bu koşu "
          "(60 gün önce +%20 eş katı, ORTAK CETVEL)", "", "| Kayıt | Pazar | Dönem | eski n | eski kat | yeni A n / kat | yeni C n / kat |", "|---|---|---|---|---|---|---|"]
    for r in J["eski"]:
        a = _ol(KU["A"], r["pazar"], r["donem"]); c = _ol(KU["C"], r["pazar"], r["donem"])
        s.append(f"| {r['kod']} | {r['pazar']} | {r['donem']} | {r['n']} | {_sy(r['ana_kat'])} | {a.get('once20_es_n', '-')} / {_sy(a.get('once20_es_kat'))} | "
                 f"{c.get('once20_es_n', '-')} / {_sy(c.get('once20_es_kat'))} |")
    s += ["", "- Eski Ç75 = bütün dip16, Ç78 = bütün dip17 olayları (eski veri ve eşli taban); yeni A / C ikisinin birleşimini çöl yakınlığına göre böler: "
          "satırlar birebir aynı evren değildir, yön kıyası içindir.", ""]
    g = J.get("gelecek_denetim", {})
    s += ["## Geleceğe bakma denetimi (gerçek ABD örneklemi; seri t'de kesilince aynı sinyal)", ""]
    for pz, d in g.items():
        s.append(f"- {pz}: " + "; ".join(f"{t} {v['ayni']}/{v['n']}" + (f" (farklı: {v['fark']})" if v.get('fark') else "") for t, v in d.items()))
    s += ["", "## Ön kayıt olay sayımı (yeniden)", "", _md_tablo(pd.DataFrame(J["sayim_onkayit"])), "", f"D örneklemi: {J['D_n']} olay.", ""]
    for k in ("C", "A", "B", "D"):
        s += [OC.oc_rapor(_S_json(KU[k]), baslik=f"Küme {ad[k]}"), ""]
    s += ["## Sınırlar", "",
          "- C kümesi iki sinyalin 60 gün içinde çakışmasıdır; küçük n'de hücreler ÖLÇÜLEMEDİ kalır (ayrım için C n250 >= 1.000 ister).",
          "- dip16 / dip17 / col tarayıcıları FON_IZI'deki haliyle (eşikler TEHOL / MANAS örneklerinden); burada değiştirilmedi.",
          "- Avrupa ve ABD fiyat-hacim; ABD evreni V_ABD + k34_yahoo (nakdi biten, yaşayan); batanlar yok.",
          "- 250 gün dokunma ölçüsü en geç ~Ağustos 2025 girişlerini kapsar (31.08.2026 kriz kesiği).", ""]
    metin = "\n".join(s)
    with open(os.path.join(DCA_YOL["cikti"], DCA_DOSYA["rapor"]), "w", encoding="utf-8") as f:
        f.write(metin)
    return metin


def _cakisma_kontrol_dca(_once=_CK_ONCE_DCA, _dosya="DIP_COL_AYRIM.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_DCA", "_CK_KAYIT", "_cakisma_kontrol_dca", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "subprocess", "warnings", "copy", "_dt", "io", "inspect",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple", "OC", "_yz", "_sy", "_md_tablo")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_dca()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=DCA_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "sha"])
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(dca_onkayit_yaz(uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            J_ = dca_kos(); print(json.dumps({"ayrim": J_["ayrim_etiket"], **{k: v["etiket"] for k, v in J_["kume"].items()}}, ensure_ascii=False, indent=1))
        elif a.komut == "rapor":
            print(dca_rapor()[:3000])
        else:
            print(json.dumps({"param": dca_param_sha(), "tasarim": dca_tasarim_sha(), "kod": dca_kod_sha()}, indent=1))
    except (DCAHata, OC.OCHata) as ex:
        dcalog.error("%s", ex); sys.exit(1)
