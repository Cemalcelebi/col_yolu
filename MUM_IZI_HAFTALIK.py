"""MUM_IZI_HAFTALIK — MUM_IZI EK 3: AYNI KALIP HAFTALIK MUMLARDA, EVRENLER AYRI, SONRASI 15 HAFTA; CEMAL GÖRECEK (25 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI3_IS_TANIMI.md (commit 0a32da1; ana model). Cemal (25 Kas): "İz değil dediğin parmak izi kalıbına
HAFTALIK mumlarda uyan bölgeleri çıkar; mümkünse ayrı evrende olsunlar; bu kalıba TAM uyan bölgelere sahip hisseler sonrasında ne yapmışlar,
bakayım göreyim."

Kalıp, ölçüler, benzerlik puanı S ve eşikler MUM_IZI'den AYNEN (mum_izi_sablon.json + mum_izi_sentetik.json; tam 0,59 / tepesiz 0,56); haftalık
için yeniden ayar YOK. TAM UYAN = S >= eşik + 0,10. Sonuç BİLGİ'dir (ikinci bakış; 'iz' sözü kullanılmaz); kasa açılmaz.
Veri: TEZGAH2 V_ABD2 / V_AVR2 (/root/.kasa/ham/veri3, YALNIZ OKUNUR) ve V_BIST (/tmp/veri) -> <= 2022-12-31 kesikli kopyalar (/tmp/mum_izi/haftalik);
haftalık bar günlük geçerli barlardan (MI.mi_veri = OS.os_veri / C2.c2_veri temizliği). Eş için CETVEL2 v2.2 panel kovası (C2.c2_panel22_al)
ve TEZGAH2 P2 (KART_TUR2) içe alınır; mevcut modüller DEĞİŞTİRİLMEZ.

Komut:  python MUM_IZI_HAFTALIK.py haftalik_hazirla    kesikli günlük kopyalar (tam 2000-2022, P1 2000-2016) -> mum_izi3_veri.json
        python MUM_IZI_HAFTALIK.py onkayit             MUM_IZI3_ON_KAYIT.md
        python MUM_IZI_HAFTALIK.py haftalik_kos        kapı -> haftalık tarama -> P2 -> sonrası + eş + plasebo -> mum_izi3_olay.csv.gz, mum_izi3_sonuc.json
        python MUM_IZI_HAFTALIK.py haftalik_pdf        MUM_IZI3_HAFTALIK.pdf (özet + şablon + 40 bölge)
        python MUM_IZI_HAFTALIK.py rapor               MUM_IZI3_RAPOR.md
Colab:  exec(open('MUM_IZI.py').read()); exec(open('MUM_IZI_HAFTALIK.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_MH = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_MH = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_MH not in sys.path:
    sys.path.insert(0, KOK_MH)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ; yalnız çağrılır)

mhlog = logging.getLogger("col.mum_izi_haftalik")
if not mhlog.handlers:
    _mh_h = logging.StreamHandler(sys.stderr)
    _mh_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_haftalik: %(message)s", "%H:%M:%S"))
    mhlog.addHandler(_mh_h)
    mhlog.setLevel(logging.INFO)
    mhlog.propagate = False


class MHHata(RuntimeError):
    """Durdurucu hata: veri / kesik / kapı / doğrulama."""


MH_SURUM = "MUM_IZI_HAFTALIK v1.0 (2026-11-25): MUM_IZI kalıbı haftalık mumda; evrenler ayrı (2001-15 / 2016-22); sonrası 15 hafta (bilgi)"
MH_YOL = {"cikti": MI.MI_YOL["cikti"], "kod": os.path.join(KOK_MH, "MUM_IZI_HAFTALIK.py"), "kod1": MI.MI_YOL["kod"],
          "veri3": MI.MI_YOL["veri3"], "veri": MI.MI_YOL["veri"], "tam": "/tmp/mum_izi/haftalik/tam", "p1": "/tmp/mum_izi/haftalik/p1",
          "p2": MI.MI_YOL["acik"], "gecici": "/tmp/mum_izi/haftalik"}
MH_DOSYA = {"onkayit": "MUM_IZI3_ON_KAYIT.md", "rapor": "MUM_IZI3_RAPOR.md", "sonuc": "mum_izi3_sonuc.json", "olay": "mum_izi3_olay.csv.gz",
            "pdf": "MUM_IZI3_HAFTALIK.pdf", "veri": "mum_izi3_veri.json"}
MH_KESIK = pd.Timestamp("2022-12-31")

MH_ESIK: Dict[str, Any] = {
    "surum": "MH-1.0",
    "hafta": {"tanim": "ISO takvim haftası; O = haftanın ilk geçerli gününün açılışı, H = en yüksek, L = en düşük, C = son geçerli günün kapanışı, "
                       "V = toplam; tarih = haftanın son geçerli günü. Geçerli günü olmayan hafta yok. Günlük girdi MI.mi_veri temiz barları "
                       "(H > L, V > 0) olduğu için haftalık H > L her zaman sağlanır (denetlenir).",
              "tamamlanmis": "haftanın cuması <= veri sonu (2022-12-30, cuma): kesikteki son hafta tam; yarım hafta (cuması veri sonundan sonra) atılır",
              "bant": "Bollinger (20, 2) ve SMA20 haftalık kapanışlardan, yalnız o haftaya kadar (MI.mi_bant)"},
    "sablon": "MUM_IZI tam (L 20; pencere 16-24 hafta) ve tepesiz (L 17; 14-20 hafta) şablonu + kalibrasyon (tau, sd) AYNEN; S = MI.mi_tara_seri",
    "esik": {"tam": 0.59, "tepesiz": 0.56}, "tam_uyan_ek": 0.10,
    "seviye": "ESIK: S >= eşik; TAM_UYAN: S >= eşik + 0,10. Her seviyede aynı hissede eşiği geçen hafta sonları 15 hafta tekil (ilk kalır) -> iki ayrı "
              "olay listesi",
    "veri": {"tam": ["2000-01-01", "2022-12-31"], "p1": ["2000-01-01", "2016-12-31"], "p2": "MUM_IZI açık kopya (2015-01-01..2022-12-30)",
             "bist": "V_BIST (2015-06..), yalnız p2"},
    "hucre": {"h0107": ["2001-01-01", "2007-12-31"], "h0815": ["2008-01-01", "2015-12-31"], "h1622": ["2016-01-01", "2022-12-31"],
              "tanim": "bölge sonu t (son haftanın son geçerli günü); h0107 + h0815 = AYRI EVREN (günlük taramada kullanılmadı), h1622 = KARŞILAŞTIRMA",
              "panel": "h0107 / h0815 olaylarının sonrası p1 panelinde (2000-2016), h1622 p2 panelinde (2015-2022)"},
    "evren": {"ABD": "TEZGAH2 P2 (KART_TUR2.k2_panel + k2_P + _k2_oc tekil 1; giriş günü d'de; d'nin bilgisi t'ye kadar)", "AVR": "aynı",
              "BIST": "V_BIST, P2 yok (bilgi)"},
    "sonrasi": {"giris": "bölgenin son haftasından sonraki ilk geçerli günün açılışı (E0)",
                "ufuk_hafta": 15, "bilgi_hafta": 30,
                "R15h": "hissenin bölgeden sonraki 15. haftalık barının kapanışı / E0 - 1 (son günü <= 2022-12-30 olmalı; değilse ölçülmez, sayısı yazılır)",
                "max_min": "E0 günü .. 15. haftanın son günü arasında günlük en yüksek High / E0 - 1 ve en düşük Low / E0 - 1",
                "dokunma": "hedef +%5 / +%10 / +%20: günlük sırayla High >= E0 (1 + x) olan ilk gün, stop gününden ÖNCE (aynı gün = stop önce); stop = "
                           "bölgenin en düşük Low'u x 0,98; E0 <= stop ise olay ölçülmez; stop payı = ufukta Low <= stop olan gün var",
                "hedef": [0.05, 0.10, 0.20], "stop_carpan": 0.98},
    "es": {"tanim": "aynı giriş günü d, aynı kova (CETVEL2 v2.2 panel KV: ATRP tercili x likidite üçlüsü x F15 çeyreği; KV >= 0 havuz), aynı şablon ve "
                    "seviyede o gün olayı olan hisseler dışı, d'de geçerli açılış; ölçüler AYNI takvim aralığında: R = olayın 15. hafta son günündeki "
                    "(ya da öncesindeki son geçerli) kapanış / d açılışı - 1; max / min aynı satırlar; dokunma: eşin stop'u = olayın bölge takvim "
                    "aralığında eşin en düşük Low'u x 0,98",
           "min": 5, "fark": "R15h - eş ortalaması", "sira": "(olaydan küçük eş + 0,5 eşit) / eş sayısı"},
    "hucre_ist": "C2.c2_hucre(R15h, eş ort, SIRA, giriş, '?', egri yok -> güç şartı yok, perm 10.000) : n, ort / medyan FARK, ay kümeli boot %95, "
                 "SIRA, L3O, p; ayrıca olay / eş ortalama ve medyan R15h, max, min, dokunma ve stop payları",
    "plasebo": {"tohum_sayi": 200, "kok": 2522,
                "tanim": "her ölçülen olayın yerine aynı gün aynı kovadan rastgele bir eş (dışlanmamış) -> onun R15h'si ve öteki eşlerin ortalaması -> "
                         "aynı c2_hucre (perm yok); 200 tohumda ort FARK dağılımı ve TUTAR (+ / -) payları = şans tabanı"},
    "etiket": "c2 hükmü (TUTAR + / TUTAR - / TUTMADI); n < 30 'örneklem yetersiz'; BH q 0,10 aile = (tam, tepesiz) x (ESIK, TAM_UYAN) x hücreler "
              "(pazar x dönem, n >= 30); 'iz' sözü yok (ikinci bakış, bilgi); K7 evren bugün yaşayanlar -> 2001-15 yukarı yanlı, olaya ve eşe aynı",
    "pdf": {"secim": "tam şablon, ESIK seviyesi, ABD / AVR'de P2'den geçen olaylar; S büyükten küçüğe; aynı hisse en çok bir kez (sayfa listesinde): "
                     "AYRI EVREN (h0107 + h0815) ABD 10 + AVR 6; h1622 ABD 6 + AVR 4 + BIST 6; sonra bütün eşleşmelerden (iki şablon, iki seviye, "
                     "bütün pazarlar; daha önce seçilen hisseler hariç) rastgele 8 (tohum 2523)",
            "sayfa": "sayfa başına tek haftalık mum grafiği (dikey A4): bölgeden önce 40 hafta, bölge kutulu, sonra 30 hafta (veri kesiği aşılmaz), "
                     "Bollinger 20 + SMA20; başlıkta hisse + tarih açık, S, R15h ve eş ortalaması, en yüksek / en derin",
            "tohum": 2523, "adet": {"ayri_ABD": 10, "ayri_AVR": 6, "h1622_ABD": 6, "h1622_AVR": 4, "h1622_BIST": 6, "rastgele": 8}, "once": 40, "sonra": 30},
    "bh_q": 0.10,
}

MH_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü, aynı CETVEL2 v2.2 kovası (>= 5), aynı gün kalıp olayı olan hisseler dışı, AYNI takvim aralığında aynı ölçüler "
                   "(R15h, max, min, dokunma; eşin stop'u kendi bölge-aralığı dibi x 0,98); plasebo şans tabanı 200 tohum SAYIYLA (aynı gün aynı kova "
                   "rastgele eş)"),
    "K2": ("EVET", "haftalık bar yalnız o haftaya kadarki günlerden; bant haftalık kapanışla t'ye kadar; yarım hafta atılır; mh_prefix: 30 olayda günlük "
                   "veri t'de kesilince S(t) aynı (assert); veri <= 2022-12-31 assert + KASA.kasa_kapisi; sonrası penceresi kesiği aşan olay ölçülmez"),
    "K3": ("EVET", "günlük girdi MI.mi_veri geçerli bar süzgeci (H > L, V > 0); haftalık H > L denetlenir; eş d'de geçerli açılış"),
    "K4": ("EVET", "aynı hissede 15 hafta tekil (ilk kalır), seviye başına ayrı liste; plasebo / eş günlük panelde"),
    "K5": ("EVET", "giriş = bölgenin son haftasından sonraki ilk geçerli günün AÇILIŞI; eşler aynı gün açılışı"),
    "K6": ("EVET", "TEZGAH2 bölünme düzeltmeli fiyat (yfinance auto_adjust); S ölçek bağımsız; AVR yerel para (oran ölçüleri); BIST bilgi"),
    "K7": ("EVET", "evren bugün işlem gören hisseler: 2001-15 AYRI EVREN'de hayatta kalma yanlılığı büyük (batanlar yok) -> sonrası yukarı yanlı; "
                   "olaya ve eşe aynı biner; raporda yazılı"),
    "K8": ("EVET", "hücreler pazar x dönem (h0107, h0815, h1622) x şablon x seviye; n < 30 'örneklem yetersiz'; BH q 0,10; iki seviye ve iki dönem "
                   "ayrı satır; ikinci bakış -> bilgi"),
    "K9": ("EVET", "MUM_IZI3_ON_KAYIT.md: KOD3_SHA, ESIK3_SHA, MI_KOD_SHA, şablon / sentetik sha, veri sha'ları, PDF seçim kuralı ve tohumlar; ön kayıt "
                   "commit'i taramadan önce; mh_kapi kontrol + sha + git"),
    "K10": ("EVET", "mh_elle: 3 rastgele olayın haftalık barı günlük veriden düz döngüyle yeniden kurulur (O / H / L / C / V birebir) ve raporda yazılır"),
    "K11": ("EVET", "mh_yeniden: 2 hücre olay satır dosyasından düz pandas (n, ort FARK, +%10 payı); 5 olayın R15h'si ve eş ortalaması ham günlük "
                    "veriden düz döngüyle"),
    "K12": ("EVET", "'iz' sözü kullanılmaz; sonuç bilgi; c2 hükmü ve BH yazılır; sayı ve yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_mh); MUM_IZI.py / defterler / UC_IZ2 dosyaları değişmez; yalnız kendi yolları git add"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; kalıbın haftalık mumda gösterimi"),
}


# ================================================================ 0) YARDIMCI
def _mh_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or MH_YOL["cikti"], MH_DOSYA[ad])


def mh_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or MH_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def mh_hucre(t: Any) -> np.ndarray:
    g = pd.to_datetime(pd.Series(t)).to_numpy(); out = np.full(len(g), "dis", dtype=object)
    for ad, v in MH_ESIK["hucre"].items():
        if ad.startswith("h"):
            m = (g >= np.datetime64(pd.Timestamp(v[0]))) & (g <= np.datetime64(pd.Timestamp(v[1])))
            out[m] = ad
    return out


# ================================================================ 1) HAFTALIK BAR
def mh_haftalik(d: pd.DataFrame, veri_sonu: Optional[pd.Timestamp] = None) -> pd.DataFrame:
    """Günlük geçerli barlar -> ISO hafta barları (index = haftanın son geçerli günü; 'bas' ilk gün). Yarım hafta (cuması veri_sonu'ndan sonra) atılır."""
    if not len(d):
        return pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume", "bas", "n_gun"])
    ix = pd.DatetimeIndex(d.index)
    iso = ix.isocalendar()
    key = iso.year.to_numpy(np.int64) * 100 + iso.week.to_numpy(np.int64)
    if (np.diff(key) < 0).any():
        raise MHHata("günlük veri sıralı değil")
    st = np.r_[0, np.flatnonzero(np.diff(key) != 0) + 1]; en = np.r_[st[1:] - 1, len(d) - 1]
    O, H, L, C, V = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    W = pd.DataFrame({"Open": O[st], "High": np.maximum.reduceat(H, st), "Low": np.minimum.reduceat(L, st), "Close": C[en],
                      "Volume": np.add.reduceat(V, st), "bas": ix[st], "n_gun": en - st + 1}, index=ix[en])
    if "Kur" in d.columns:
        W["Kur"] = d["Kur"].to_numpy(float)[en]
    vs = pd.Timestamp(veri_sonu) if veri_sonu is not None else ix.max()
    yil = iso.year.to_numpy(np.int64)[en]; hf = iso.week.to_numpy(np.int64)[en]
    cuma = pd.to_datetime([_dt.date.fromisocalendar(int(a), int(b), 5) for a, b in zip(yil, hf)])
    W = W[np.asarray(cuma <= vs)]
    if len(W) and not (W.High > W.Low).all():
        raise MHHata("haftalık H > L değil")
    return W


def mh_haftalik_pazar(V: Dict[str, pd.DataFrame], veri_sonu: pd.Timestamp) -> Dict[str, pd.DataFrame]:
    return {s: w for s, w in ((s, mh_haftalik(d, veri_sonu)) for s, d in V.items()) if len(w) >= 40}


# ================================================================ 2) VERİ HAZIRLIĞI (kesikli kopyalar)
def mh_hazirla(cikti: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    cikti = cikti or MH_YOL["cikti"]; J: Dict[str, Any] = {"zaman": MI._mi_simdi()}
    for kl in ("tam", "p1"):
        os.makedirs(MH_YOL[kl], exist_ok=True)
    for p, kay in (("ABD", os.path.join(MH_YOL["veri3"], "V_ABD2.pkl")), ("AVR", os.path.join(MH_YOL["veri3"], "V_AVR2.pkl")),
                   ("BIST", os.path.join(MH_YOL["veri"], "V_BIST.pkl"))):
        if not os.path.exists(kay):
            raise MHHata(f"veri yok: {kay}")
        V0 = pd.read_pickle(kay)
        if isinstance(V0, dict) and "veri" in V0 and isinstance(V0["veri"], dict):
            V0 = V0["veri"]
        J[p] = {"kaynak": kay, "kaynak_sha": MI._mi_sha(kay)}
        W, say = MI.mi_kes_fiyat(V0, MH_ESIK["veri"]["tam"][0])
        y = os.path.join(MH_YOL["tam"], f"V_{p}.pkl"); pd.to_pickle(W, y)
        J[p]["tam"] = {**say, "yazilan": len(W), "sha": MI._mi_sha(y), "ilk": str(min(x.index.min() for x in W.values()).date()),
                       "son": str(max(x.index.max() for x in W.values()).date())}
        if p != "BIST":
            W1, s1 = MI.mi_kes_fiyat(W, MH_ESIK["veri"]["p1"][0], pd.Timestamp(MH_ESIK["veri"]["p1"][1]))
            y1 = os.path.join(MH_YOL["p1"], f"V_{p}.pkl"); pd.to_pickle(W1, y1)
            J[p]["p1"] = {**s1, "yazilan": len(W1), "sha": MI._mi_sha(y1), "son": str(max(x.index.max() for x in W1.values()).date())}
            del W1
        del V0, W; gc.collect()
        mhlog.info("hazırlık %s: %s", p, J[p]["tam"])
    J["p2"] = {p: MI._mi_sha(os.path.join(MH_YOL["p2"], f"V_{p}.pkl")) for p in ("ABD", "AVR", "BIST")}
    J["kasa"] = KS.kasa_kapisi([os.path.join(MH_YOL["tam"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] +
                               [os.path.join(MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")], str(MH_KESIK.date()))
    MI._mi_jyaz(_mh_yol("veri", cikti), J, "veri 3")
    return J


# ================================================================ 3) TARAMA
def mh_tara_hisse(W: pd.DataFrame, sab: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    O, H, L, C = (W[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")); ix = W.index; bas = W.bas.to_numpy()
    ol = []
    for ad, s in sab.items():
        best, bm = MI.mi_tara_seri(O, H, L, C, s)
        for sev, th in (("ESIK", s["esik"]), ("TAM_UYAN", s["esik"] + MH_ESIK["tam_uyan_ek"])):
            e = np.flatnonzero(np.nan_to_num(best, nan=-1) >= th)
            if not len(e):
                continue
            for t in MI._mi_tekil(e, int(MI.MI_ESIK["gercek"]["tekil"])):
                m = int(bm[t]); a = t - m + 1
                ol.append({"sablon": ad, "seviye": sev, "tarih": ix[t], "hafta_no": int(t), "S": float(best[t]), "m": m, "bolge_bas": pd.Timestamp(bas[a]),
                           "bolge_min_low": float(L[a:t + 1].min()), "C_t": float(C[t])})
    return ol


_MH_ISCI: Dict[str, Any] = {}


def _mh_isci(s: str) -> Tuple[str, List[Dict[str, Any]], int]:
    W = _MH_ISCI["W"][s]
    return s, mh_tara_hisse(W, _MH_ISCI["sab"]), int(len(W))


def mh_tara_pazar(Wd: Dict[str, pd.DataFrame], sab: Dict[str, Dict[str, Any]], pazar: str, islem: int = 3) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    import multiprocessing as mp
    _MH_ISCI.clear(); _MH_ISCI.update({"W": Wd, "sab": sab}); semb = sorted(Wd); t0 = time.time()
    try:
        if islem > 1 and "fork" in mp.get_all_start_methods():
            with mp.get_context("fork").Pool(islem) as pool:
                R = list(pool.imap(_mh_isci, semb, chunksize=16))
        else:
            R = [_mh_isci(s) for s in semb]
    finally:
        _MH_ISCI.clear()
    ol = []
    for s, o, _ in R:
        for r in o:
            r["sembol"] = s
        ol.extend(o)
    X = pd.DataFrame(ol)
    if len(X):
        X["pazar"] = pazar; X["hucre"] = mh_hucre(X.tarih)
        X = X[X.hucre != "dis"].reset_index(drop=True)
    hb = {h: int(sum(((w.index >= pd.Timestamp(v[0])) & (w.index <= pd.Timestamp(v[1]))).sum() for w in Wd.values()))
          for h, v in MH_ESIK["hucre"].items() if h.startswith("h")}
    mhlog.info("%s haftalık tarama: %d hisse, olay %d (%.0f sn)", pazar, len(semb), len(X), time.time() - t0)
    return X, {"hisse": len(semb), "hafta": int(sum(n for _, _, n in R)), "hucre_hafta": hb}


def mh_prefix(V: Dict[str, pd.DataFrame], X: pd.DataFrame, sab: Dict[str, Dict[str, Any]], n: int = 30) -> Dict[str, Any]:
    """K2: günlük veri t'de kesilip haftalık yeniden kurulunca S(t) aynı."""
    if not len(X):
        return {"n": 0, "tuttu": True}
    rng = np.random.default_rng(2524); sec = X.iloc[rng.choice(len(X), size=min(n, len(X)), replace=False)]; mx = 0.0
    for r in sec.itertuples():
        d = V[r.sembol]; Wk = mh_haftalik(d[d.index <= r.tarih], pd.Timestamp(r.tarih) + pd.Timedelta(days=6))
        b, _ = MI.mi_tara_seri(*(Wk[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), sab[r.sablon])
        if Wk.index[-1] != r.tarih:
            raise MHHata(f"prefix: son hafta {Wk.index[-1].date()} != t {r.tarih.date()}")
        mx = max(mx, abs(float(b[-1]) - float(r.S)))
    if not mx < 1e-12:
        raise MHHata(f"PREFIX TUTMADI {mx}")
    return {"n": int(len(sec)), "en_buyuk_fark": mx, "tuttu": True}


# ================================================================ 4) SONRASI (olay + eş)
def mh_olay_olc(V: Dict[str, pd.DataFrame], Wd: Dict[str, pd.DataFrame], X: pd.DataFrame) -> pd.DataFrame:
    """Olayın kendi ölçüleri (günlük veriden): giriş, 15. / 30. hafta sonu, R15h, R30h, max, min, dokunma, stop."""
    S = MH_ESIK["sonrasi"]; U = int(S["ufuk_hafta"]); U2 = int(S["bilgi_hafta"]); hed = S["hedef"]; sc = float(S["stop_carpan"])
    out = []
    for r in X.itertuples():
        d = V[r.sembol]; W = Wd[r.sembol]; t = int(r.hafta_no)
        rec: Dict[str, Any] = {"giris": pd.NaT, "son15": pd.NaT, "olculdu": False, "neden": ""}
        if t + 1 >= len(W):
            rec["neden"] = "giris_yok"; out.append(rec); continue
        g = W.bas.iloc[t + 1]; rec["giris"] = g
        di = d.index.get_loc(g); E0 = float(d.Open.iloc[di]); stop = float(r.bolge_min_low) * sc
        rec["E0"] = E0; rec["stop"] = stop
        if t + U < len(W):
            e15 = W.index[t + U]; rec["son15"] = e15
        else:
            rec["neden"] = "ufuk_kesik"; out.append(rec); continue
        if E0 <= stop:
            rec["neden"] = "giris_stop_altinda"; out.append(rec); continue
        ei = d.index.get_loc(e15); Hs = d.High.to_numpy(float)[di:ei + 1]; Ls = d.Low.to_numpy(float)[di:ei + 1]
        rec["R15h"] = float(d.Close.iloc[ei]) / E0 - 1; rec["max15"] = float(Hs.max()) / E0 - 1; rec["min15"] = float(Ls.min()) / E0 - 1
        sk = np.flatnonzero(Ls <= stop); ks = int(sk[0]) if len(sk) else 10 ** 9
        rec["stop15"] = float(len(sk) > 0)
        for x in hed:
            hk = np.flatnonzero(Hs >= E0 * (1 + x)); rec[f"d{int(round(x * 100))}"] = float(len(hk) > 0 and int(hk[0]) < ks)
        if t + U2 < len(W):
            rec["R30h"] = float(d.Close.loc[W.index[t + U2]]) / E0 - 1
        rec["olculdu"] = True
        out.append(rec)
    Y = pd.DataFrame(out, index=X.index)
    return pd.concat([X, Y], axis=1)


def mh_es(Pn: Dict[str, Any], X: pd.DataFrame, olay_set: Dict[Tuple[Any, ...], set]) -> Tuple[pd.DataFrame, List[Optional[Dict[str, np.ndarray]]]]:
    """Eş ölçüleri (CETVEL2 v2.2 panel, aynı gün aynı kova, olay hisseleri dışı, aynı takvim aralığı). Döner: X + eş sütunları ve olay başına eş
    vektörleri (plasebo için)."""
    P = Pn["P"]; idx = P["tarih"]; kol = P["kol"]; KV = Pn["KV"]; Op, Hi, Lo, Cl = P["Op"], P["Hi"], P["Lo"], Pn["Cl"]
    S = MH_ESIK["sonrasi"]; hed = S["hedef"]; sc = float(S["stop_carpan"]); mn = int(MH_ESIK["es"]["min"])
    sut = {k: np.full(len(X), np.nan) for k in ["es_R15h", "es_med", "n_es", "sira", "fark", "es_max15", "es_min15", "es_stop15", "kova"] +
           [f"es_d{int(round(x * 100))}" for x in hed]}
    vek: List[Optional[Dict[str, np.ndarray]]] = [None] * len(X)
    for q, r in enumerate(X.itertuples()):
        if not r.olculdu:
            continue
        j = kol.get(r.sembol)
        try:
            d = idx.get_loc(pd.Timestamp(r.giris)); e = idx.get_loc(pd.Timestamp(r.son15))
            a = idx.get_loc(pd.Timestamp(r.bolge_bas)); tt = idx.get_loc(pd.Timestamp(r.tarih))
        except KeyError:
            continue
        if j is None or KV[d, j] < 0:
            continue
        kv = int(KV[d, j]); sut["kova"][q] = kv
        uye = np.flatnonzero((KV[d] == kv) & np.isfinite(Op[d]) & (Op[d] > 0))
        dis = olay_set.get((r.sablon, r.seviye, d), set())
        uye = np.array([u for u in uye if u != j and u not in dis], np.int64)
        if len(uye) < mn:
            continue
        E = Op[d, uye]
        c = Cl[d:e + 1, uye]; okc = np.isfinite(c)
        son = np.where(okc.any(0), c.shape[0] - 1 - np.argmax(okc[::-1], axis=0), -1)
        Rr = np.where(son >= 0, c[np.maximum(son, 0), np.arange(len(uye))] / E - 1, np.nan)
        h = Hi[d:e + 1, uye]; lo = Lo[d:e + 1, uye]
        with np.errstate(all="ignore"):
            mx = np.nanmax(h, axis=0) / E - 1; mi = np.nanmin(lo, axis=0) / E - 1
            st = np.nanmin(Lo[a:tt + 1, uye], axis=0) * sc
        ok = np.isfinite(Rr) & np.isfinite(st) & (E > st)
        if ok.sum() < mn:
            continue
        uye, E, Rr, mx, mi, st, h, lo = uye[ok], E[ok], Rr[ok], mx[ok], mi[ok], st[ok], h[:, ok], lo[:, ok]
        with np.errstate(invalid="ignore"):
            stopm = np.where(np.isnan(lo), False, lo <= st[None, :])
        ks = np.where(stopm.any(0), np.argmax(stopm, axis=0), 10 ** 9)
        sut["es_stop15"][q] = float(stopm.any(0).mean())
        dk = {}
        for x in hed:
            with np.errstate(invalid="ignore"):
                hm = np.where(np.isnan(h), False, h >= E[None, :] * (1 + x))
            kh = np.where(hm.any(0), np.argmax(hm, axis=0), 10 ** 9)
            dk[x] = (kh < ks) & (kh < 10 ** 9)
            sut[f"es_d{int(round(x * 100))}"][q] = float(dk[x].mean())
        R = float(r.R15h)
        sut["es_R15h"][q] = float(Rr.mean()); sut["es_med"][q] = float(np.median(Rr)); sut["n_es"][q] = len(Rr)
        sut["sira"][q] = float(((Rr < R).sum() + 0.5 * (Rr == R).sum()) / len(Rr)); sut["fark"][q] = R - float(Rr.mean())
        sut["es_max15"][q] = float(np.nanmean(mx)); sut["es_min15"][q] = float(np.nanmean(mi))
        vek[q] = {"R": Rr}
    Y = X.copy()
    for k, v in sut.items():
        Y[k] = v
    return Y, vek


def mh_p2(X: pd.DataFrame, pazar: str, klasor: str) -> np.ndarray:
    """ABD / AVR: giriş günü P2 üyeliği (KART_TUR2 / TEZGAH2), olay tarihi t ile."""
    if pazar not in ("ABD", "AVR") or not len(X):
        return np.ones(len(X), bool)
    import KART_TUR2 as KT2
    import OLCU_SINAMA as OS
    Vd = OS.os_veri(pazar, klasor); Pk, P2 = KT2.k2_panel(Vd, pazar); P = KT2.k2_P(Pk, Vd, P2)
    Z, _ = KT2._k2_oc(X[["sembol", "tarih"]].drop_duplicates(), P, 1)
    k = set(zip(Z.sembol, pd.to_datetime(Z.tarih)))
    out = np.array([(s, pd.Timestamp(t)) in k for s, t in zip(X.sembol, X.tarih)])
    del Vd, Pk, P2, P; gc.collect()
    return out


def mh_hucre_ist(x: pd.DataFrame, tohum_ek: int) -> Dict[str, Any]:
    import CETVEL2 as C2
    x = x[np.isfinite(x.fark.to_numpy(float))]; out: Dict[str, Any] = {"n": int(len(x))}
    if len(x) < 2:
        out["hukum"] = "örneklem yetersiz"; return out
    c = C2.c2_hucre(x.R15h.to_numpy(float), x.es_R15h.to_numpy(float), x.sira.to_numpy(float), pd.to_datetime(x.giris).to_numpy(), "?",
                    tohum_ek=tohum_ek, egri=None, perm=True)
    out.update({k: c.get(k) for k in ("fark", "med", "boot_alt", "boot_ust", "sira", "l3o", "l3o_neg", "p", "tutar_p", "tutar_n")})
    out.update({"R_ort": float(x.R15h.mean()), "R_med": float(x.R15h.median()), "es_ort": float(x.es_R15h.mean()), "es_med": float(x.es_med.median()),
                "max_ort": float(x.max15.mean()), "es_max_ort": float(x.es_max15.mean()), "min_ort": float(x.min15.mean()), "es_min_ort": float(x.es_min15.mean()),
                "stop": float(x.stop15.mean()), "es_stop": float(x.es_stop15.mean())})
    for h in MH_ESIK["sonrasi"]["hedef"]:
        k = f"d{int(round(h * 100))}"; out[k] = float(x[k].mean()); out[f"es_{k}"] = float(x[f"es_{k}"].mean())
    if "R30h" in x.columns:
        out["R30_ort"] = float(np.nanmean(x.R30h.to_numpy(float))) if np.isfinite(x.R30h.to_numpy(float)).any() else np.nan
    yon = "+" if c.get("tutar_p") else ("-" if c.get("tutar_n") else "")
    out["yon"] = yon
    out["hukum"] = "örneklem yetersiz" if out["n"] < 30 else (f"TUTAR ({yon})" if yon else "TUTMADI")
    return out


def mh_plasebo(x: pd.DataFrame, vek: List[Optional[Dict[str, np.ndarray]]], tohum_ek: int) -> Dict[str, Any]:
    """Her olayın yerine aynı gün aynı kovadan rastgele eş (vektörlü): onun R15h'si, öteki eşlerin ortalaması ve SIRA'sı -> C2.c2_hucre (perm yok)."""
    import CETVEL2 as C2
    Pl = MH_ESIK["plasebo"]; ii = [i for i in range(len(x)) if vek[i] is not None and np.isfinite(x.fark.iloc[i]) and len(vek[i]["R"]) >= 2]
    if len(ii) < 30:
        return {"n": len(ii), "not": "örneklem yetersiz"}
    lens = np.array([len(vek[i]["R"]) for i in ii], np.int64); off = np.r_[0, np.cumsum(lens)]
    allR = np.concatenate([vek[i]["R"] for i in ii]); less = np.empty(len(allR)); eq = np.empty(len(allR))
    for q in range(len(ii)):
        v = allR[off[q]:off[q + 1]]; srt = np.sort(v)
        less[off[q]:off[q + 1]] = np.searchsorted(srt, v, "left"); eq[off[q]:off[q + 1]] = np.searchsorted(srt, v, "right") - less[off[q]:off[q + 1]]
    sums = np.add.reduceat(allR, off[:-1]); g = pd.to_datetime(x.giris.iloc[ii]).to_numpy(); fs, tp, tn = [], 0, 0
    T = int(Pl["tohum_sayi"])
    for t in range(T):
        rng = np.random.default_rng([int(Pl["kok"]), int(tohum_ek), t])
        k = off[:-1] + np.minimum(np.floor(rng.random(len(ii)) * lens).astype(np.int64), lens - 1)
        R = allR[k]; E = (sums - R) / (lens - 1); Sr = (less[k] + 0.5 * (eq[k] - 1)) / (lens - 1)
        c = C2.c2_hucre(R, E, Sr, g, "?", tohum_ek=900000 + t, egri=None, perm=False, l3o_neg=True)
        fs.append(c["fark"]); tp += int(bool(c["tutar_p"])); tn += int(bool(c["tutar_n"]))
    return {"n": len(ii), "fark_ort": float(np.mean(fs)), "fark_sd": float(np.std(fs, ddof=1)), "fark_ust95": float(np.quantile(fs, 0.95)),
            "fark_alt05": float(np.quantile(fs, 0.05)), "tutar_pay_arti": tp / T, "tutar_pay_eksi": tn / T}


# ================================================================ 5) KAPI ve ÖN KAYIT
def mh_sha_simdi(cikti: Optional[str] = None) -> Dict[str, str]:
    return {"KOD3_SHA": MI._mi_sha(MH_YOL["kod"]), "ESIK3_SHA": mh_esik_sha(), "MI_KOD_SHA": MI._mi_sha(MH_YOL["kod1"]),
            "SABLON_SHA": MI._mi_sha(MI._mi_yol("sablon")), "SENTETIK_SHA": MI._mi_sha(MI._mi_yol("sentetik")),
            "VERI3_SHA": MI._mi_sha(_mh_yol("veri", cikti))}


def mh_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or MH_YOL["cikti"]; yol = _mh_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise MHHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = mh_sha_simdi(cikti)
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise MHHata(f"ön kayıt kapısı: {ad} farklı (şimdiki {v[:12]}) -> DURDU")
    rel = os.path.relpath(yol, KOK_MH)
    c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise MHHata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_HAFTALIK.py", "MUM_IZI.py"]):
        raise MHHata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def mh_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or MH_YOL["cikti"]; y = _mh_yol("onkayit", cikti)
    if os.path.exists(y):
        raise MHHata("ön kayıt zaten var")
    sh = mh_sha_simdi(cikti); VJ = json.load(open(_mh_yol("veri", cikti), encoding="utf-8"))
    sab = MI.mi_sablon_yukle()
    if abs(sab["tam"]["esik"] - MH_ESIK["esik"]["tam"]) > 1e-12 or abs(sab["tepesiz"]["esik"] - MH_ESIK["esik"]["tepesiz"]) > 1e-12:
        raise MHHata("eşikler MUM_IZI sentetik json'uyla aynı değil")
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"] +
                   [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in MH_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_HAFTALIK.py"])
    s = [f"# MUM_IZI3 ÖN KAYIT ({MI._mi_simdi()})", "",
         "Haftalık tarama ve sonrası bu dosya commit edildikten SONRA koşar (`mh_kapi`). Bu ana kadar haftalık barda hiçbir pencere puanlanmadı; yalnız "
         "kesikli günlük kopyalar hazırlandı (getirisiz).", "", "## Mühürler", "",
         *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_HAFTALIK.py commit'i: {kc or 'yok'}",
         f"- Veri: ABD tam {VJ['ABD']['tam']['yazilan']} hisse ({VJ['ABD']['tam']['ilk']}..{VJ['ABD']['tam']['son']}), P1 {VJ['ABD']['p1']['yazilan']}; "
         f"AVR tam {VJ['AVR']['tam']['yazilan']}, P1 {VJ['AVR']['p1']['yazilan']}; BIST {VJ['BIST']['tam']['yazilan']} ({VJ['BIST']['tam']['ilk']}..); "
         f"KASA kapısı kesik {VJ['kasa']['kesik']}", "",
         "## Tanımlar (MH_ESIK; sha yukarıda; sonuca göre DEĞİŞMEZ)", "", "```", json.dumps(MH_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 3")


# ================================================================ 6) KOŞU
def mh_kos(cikti: Optional[str] = None, kuru: bool = False, klasor: Optional[Dict[str, str]] = None, plasebo_tohum: Optional[int] = None,
           pazarlar: Optional[List[str]] = None) -> Dict[str, Any]:
    import CETVEL2 as C2
    t0 = time.time(); cikti = cikti or MH_YOL["cikti"]; kl = {"tam": MH_YOL["tam"], "p1": MH_YOL["p1"], "p2": MH_YOL["p2"], **(klasor or {})}
    if os.path.exists(_mh_yol("sonuc", cikti)) and not kuru:
        raise MHHata("sonuç zaten var (ikinci koşu DURUR)")
    G0 = {"kuru": True} if kuru else mh_kapi(cikti)
    if not kuru:
        import KASA as KS
        kasa = KS.kasa_kapisi([os.path.join(kl[k], f"V_{p}.pkl") for k, ps in (("tam", ("ABD", "AVR", "BIST")), ("p1", ("ABD", "AVR")),
                                                                                 ("p2", ("ABD", "AVR", "BIST"))) for p in ps], str(MH_KESIK.date()))
    else:
        kasa = {"kuru": True}
    sab = MI.mi_sablon_yukle()
    if plasebo_tohum:
        MH_ESIK["plasebo"]["tohum_sayi"] = int(plasebo_tohum)          # yalnız kuru koşu (esik sha kapıda kuru değilse değişmez)
    J: Dict[str, Any] = {"surum": MH_SURUM, "baslangic": MI._mi_simdi(), "kapi": G0, "kasa": kasa, "tarama": {}, "prefix": {}, "hucre": {},
                         "plasebo": {}, "sayim": {}}
    satir = []
    for p in (pazarlar or ["ABD", "AVR", "BIST"]):
        V = MI.mi_veri(p, kl["tam"])["V"]
        en_gec = max(d.index.max() for d in V.values())
        if en_gec > MH_KESIK:
            raise MHHata(f"{p}: KESİK AŞIMI {en_gec.date()}")
        Wd = mh_haftalik_pazar(V, pd.Timestamp(en_gec))
        X, ist = mh_tara_pazar(Wd, sab, p); J["tarama"][p] = ist
        if not len(X):
            continue
        J["prefix"][p] = mh_prefix(V, X, sab)
        X = mh_olay_olc(V, Wd, X)
        X["parca"] = np.where(X.hucre.isin(["h0107", "h0815"]), "p1", "p2")
        parca = []
        for pc in ("p1", "p2"):
            Y = X[X.parca == pc].copy()
            if not len(Y) or (p == "BIST" and pc == "p1"):
                if len(Y):
                    Y["p2"] = np.nan; parca.append((Y, [None] * len(Y)))
                continue
            Y["p2"] = mh_p2(Y, p, kl[pc])
            Pn = C2.c2_panel22_al(p, kl[pc], None, onbellek=False)
            gir = pd.to_datetime(Y.giris)
            dmap = {}
            for (ad, sev), g in Y[Y.olculdu & Y.giris.notna()].groupby(["sablon", "seviye"]):
                for s_, gg in zip(g.sembol, pd.to_datetime(g.giris)):
                    try:
                        dmap.setdefault((ad, sev, Pn["P"]["tarih"].get_loc(gg)), set()).add(Pn["P"]["kol"][s_])
                    except KeyError:
                        pass
            Ye, vek = mh_es(Pn, Y, dmap)
            del Pn, gir; C2._C2_PN22.clear(); gc.collect()
            parca.append((Ye, vek))
        Xa = pd.concat([a for a, _ in parca], ignore_index=True); vekt = [v for _, vv in parca for v in vv]
        Xa["evren_ici"] = Xa.p2.fillna(True).astype(bool) if p != "BIST" else True
        # hücreler: şablon x seviye x hücre (evren içi)
        for (ad, sev, hc), g in Xa[Xa.evren_ici].groupby(["sablon", "seviye", "hucre"]):
            k = f"{p}|{ad}|{sev}|{hc}"; tk = int(hashlib.md5(k.encode()).hexdigest()[:8], 16) % 100000     # sabit (süreçten bağımsız) tohum
            J["hucre"][k] = mh_hucre_ist(g, 610000 + tk)
            ii = g.index.to_numpy()
            J["plasebo"][k] = mh_plasebo(g.reset_index(drop=True), [vekt[i] for i in ii], 620000 + tk)
        J["sayim"][p] = {f"{ad}|{sev}|{hc}": {"bulunan": int(len(g)), "evren_ici": int(g.evren_ici.sum()), "olculdu": int((g.evren_ici & g.olculdu).sum()),
                                               "esli": int((g.evren_ici & np.isfinite(g.fark.to_numpy(float))).sum()),
                                               "ufuk_kesik": int((g.neden == "ufuk_kesik").sum())}
                         for (ad, sev, hc), g in Xa.groupby(["sablon", "seviye", "hucre"])}
        satir.append(Xa)
        del V, Wd, X, Xa, vekt; gc.collect()
        mhlog.info("%s bitti (%.0f sn)", p, time.time() - t0)
    O = pd.concat(satir, ignore_index=True) if satir else pd.DataFrame()
    # BH
    ks = [k for k, c in J["hucre"].items() if c.get("n", 0) >= 30 and c.get("p") is not None and np.isfinite(c.get("p", np.nan))]
    bh = C2.c2_bh([J["hucre"][k]["p"] for k in ks], MH_ESIK["bh_q"]) if ks else []
    J["bh"] = {k: bool(b) for k, b in zip(ks, bh)}
    for c_ in ("tarih", "bolge_bas", "giris", "son15"):
        if c_ in O.columns:
            O[c_] = pd.to_datetime(O[c_]).dt.strftime("%Y-%m-%d")
    if len(O):
        eg = max(pd.to_datetime(O.tarih).max(), pd.to_datetime(O.son15.dropna()).max() if O.son15.notna().any() else pd.Timestamp("1900-01-01"))
        if eg > MH_KESIK:
            raise MHHata(f"KESİK AŞIMI {eg}")
        J["en_gec"] = str(eg.date())
    kol = ["pazar", "sembol", "sablon", "seviye", "hucre", "bolge_bas", "tarih", "m", "S", "evren_ici", "p2", "olculdu", "neden", "giris", "son15", "E0",
           "stop", "R15h", "R30h", "max15", "min15", "d5", "d10", "d20", "stop15", "kova", "n_es", "es_R15h", "es_med", "sira", "fark", "es_max15",
           "es_min15", "es_d5", "es_d10", "es_d20", "es_stop15"]
    O = O[[c for c in kol if c in O.columns]]
    O["tam_uyan"] = O.S >= O.sablon.map({k: v + MH_ESIK["tam_uyan_ek"] for k, v in MH_ESIK["esik"].items()})
    O.to_csv(_mh_yol("olay", cikti), index=False, compression={"method": "gzip", "mtime": 0}, float_format="%.8g")
    J["satir_sha"] = MI._mi_sha(_mh_yol("olay", cikti)); J["olay_n"] = int(len(O))
    J["yeniden"] = mh_yeniden(O, J, kl)
    J["bitis"] = MI._mi_simdi(); J["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_mh_yol("sonuc", cikti), J, "sonuç 3")
    mhlog.info("haftalık kos bitti (%.0f sn)", time.time() - t0)
    return J


def mh_yeniden(O: pd.DataFrame, J: Dict[str, Any], kl: Dict[str, str]) -> Dict[str, Any]:
    """K11: 2 hücre düz pandas; 5 olayın R15h'si ham günlük veriden düz; K10: 3 olayın haftalık barı günlük veriden düz döngüyle."""
    out: Dict[str, Any] = {}
    ks = [k for k, c in J["hucre"].items() if c.get("n", 0) >= 30][:2]
    for k in ks:
        p, ad, sev, hc = k.split("|")
        g = O[(O.pazar == p) & (O.sablon == ad) & (O.seviye == sev) & (O.hucre == hc) & O.evren_ici.astype(bool)]
        g = g[np.isfinite(g.fark.to_numpy(float))]
        out[k] = {"duz": {"n": int(len(g)), "fark": float(g.fark.mean()), "d10": float(g.d10.mean())},
                  "json": {"n": J["hucre"][k]["n"], "fark": J["hucre"][k]["fark"], "d10": J["hucre"][k]["d10"]}}
        out[k]["tuttu"] = bool(out[k]["duz"]["n"] == out[k]["json"]["n"] and abs(out[k]["duz"]["fark"] - out[k]["json"]["fark"]) < 1e-9
                               and abs(out[k]["duz"]["d10"] - out[k]["json"]["d10"]) < 1e-12)
    x = O[O.olculdu.astype(bool)]
    if len(x):
        sec = x.sample(n=min(5, len(x)), random_state=2525); V = {}; mx = 0.0; hf = 0
        for r in sec.itertuples():
            if r.pazar not in V:
                V[r.pazar] = pd.read_pickle(os.path.join(kl["tam"], f"V_{r.pazar}.pkl"))
            d = V[r.pazar][r.sembol]; d = d[(d.High > d.Low) & (d.Volume > 0) & (d.Open > 0) & (d.Close > 0) & (d.Low > 0)]
            g = pd.Timestamp(r.giris); e = pd.Timestamp(r.son15)
            R = float(d.Close.loc[e]) / float(d.Open.loc[g]) - 1; mx = max(mx, abs(R - float(r.R15h)))
            # haftalık bar düz döngü: bölgenin son haftası
            t = pd.Timestamp(r.tarih); y, w, _ = t.isocalendar(); gun = [ix for ix in d.index if ix.isocalendar()[0] == y and ix.isocalendar()[1] == w]
            hf += int(gun[-1] != t)
        out["R15h_ham_en_buyuk_fark"] = mx; out["hafta_son_gun_hata"] = hf
    out["tuttu"] = all(v.get("tuttu", True) for v in out.values() if isinstance(v, dict)) and out.get("R15h_ham_en_buyuk_fark", 0) < 1e-6 and \
        out.get("hafta_son_gun_hata", 0) == 0
    return out


# ================================================================ 7) PDF ve RAPOR
def mh_pdf_secim(O: pd.DataFrame) -> pd.DataFrame:
    P = MH_ESIK["pdf"]; A = P["adet"]
    x = O[(O.sablon == "tam") & (O.seviye == "ESIK") & O.evren_ici.astype(bool)].sort_values("S", ascending=False)
    secilen, gorulen = [], set()
    for ad, pz, hc in (("ayri_ABD", "ABD", ("h0107", "h0815")), ("ayri_AVR", "AVR", ("h0107", "h0815")), ("h1622_ABD", "ABD", ("h1622",)),
                       ("h1622_AVR", "AVR", ("h1622",)), ("h1622_BIST", "BIST", ("h1622",))):
        k = 0
        for r in x[(x.pazar == pz) & x.hucre.isin(hc)].itertuples():
            if r.sembol in gorulen:
                continue
            secilen.append((ad, r.Index)); gorulen.add(r.sembol); k += 1
            if k >= A[ad]:
                break
    kalan = O[~O.sembol.isin(gorulen)].drop_duplicates("sembol")
    rs = kalan.sample(n=min(A["rastgele"], len(kalan)), random_state=P["tohum"]) if len(kalan) else kalan
    secilen += [("rastgele", i) for i in rs.index]
    S = O.loc[[i for _, i in secilen]].copy(); S["grup"] = [g for g, _ in secilen]
    return S


def mh_pdf(cikti: Optional[str] = None, klasor: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import Rectangle
    from PIL import Image
    cikti = cikti or MH_YOL["cikti"]; kl = klasor or MH_YOL["tam"]
    J = json.load(open(_mh_yol("sonuc", cikti), encoding="utf-8")); O = pd.read_csv(_mh_yol("olay", cikti))
    S = mh_pdf_secim(O); y = _mh_yol("pdf", cikti); Vc: Dict[str, Any] = {}
    with PdfPages(y, metadata={"Title": "MUM_IZI3 haftalık", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7))
        DN = {"h0107": "2001-07", "h0815": "2008-15", "h1622": "2016-22"}
        pc = lambda v, n=0: "-" if v is None or not np.isfinite(v) else f"{100 * v:+.{n}f}"  # noqa: E731
        pp = lambda v: "-" if v is None or not np.isfinite(v) else f"%{100 * v:.0f}"  # noqa: E731
        bas_ = ["pazar", "seviye", "dönem", "n", "15 hafta ort\nolay / eş", "medyan\nolay / eş", "+%10\nolay / eş", "+%20\nolay / eş",
                "stop\nolay / eş", "eşli fark\n(%95)", "hüküm"]
        for ti, (ad, y0_, h_, fs_) in enumerate((("tam", 0.42, 0.42, 7.0), ("tepesiz", 0.06, 0.3, 6.0))):
            ax = fig.add_axes([0.03, y0_, 0.94, h_]); ax.axis("off"); sat = []
            for k, c in J["hucre"].items():
                p_, a_, sev, hc = k.split("|")
                if a_ != ad or c.get("n", 0) < 1:
                    continue
                g = lambda kk: c.get(kk, np.nan)  # noqa: E731
                sat.append([p_, "TAM UYAN" if sev == "TAM_UYAN" else "eşik", DN[hc], str(c["n"]), f"{pc(g('R_ort'), 1)} / {pc(g('es_ort'), 1)}",
                            f"{pc(g('R_med'), 1)} / {pc(g('es_med'), 1)}", f"{pp(g('d10'))} / {pp(g('es_d10'))}", f"{pp(g('d20'))} / {pp(g('es_d20'))}",
                            f"{pp(g('stop'))} / {pp(g('es_stop'))}", f"{pc(g('fark'), 1)}\n({pc(g('boot_alt'), 1)}..{pc(g('boot_ust'), 1)})" if c.get("n", 0) >= 2 else "-",
                            c.get("hukum", "-") + (" (BH)" if J["bh"].get(k) else "")])
            if sat:
                tb = ax.table(cellText=sat, colLabels=bas_, loc="upper center", cellLoc="center", colWidths=[0.06, 0.08, 0.07, 0.05, 0.11, 0.11, 0.09, 0.09, 0.09, 0.12, 0.13])
                tb.auto_set_font_size(False); tb.set_fontsize(fs_)
                tb.scale(1, (2.0 if len(sat) <= 8 else 1.45) if ti == 0 else (1.7 if len(sat) <= 8 else 1.2))
            ax.set_title(f"{'TAM şablon (20 mum)' if ad == 'tam' else 'TEPESİZ şablon (17 mum)'}: sonraki 15 HAFTA, olay / eş (yüzde)", fontsize=8.5)
        bul = "; ".join(f"{p_}: " + ", ".join(f"{DN[hc]} {sum(v['evren_ici'] for kk, v in d_.items() if kk == 'tam|ESIK|' + hc)}"
                                              f" (TAM UYAN {sum(v['evren_ici'] for kk, v in d_.items() if kk == 'tam|TAM_UYAN|' + hc)})"
                                              for hc in ("h0107", "h0815", "h1622")) for p_, d_ in J["sayim"].items())
        ks = [k for k, c in J["hucre"].items() if c.get("n", 0) >= 30]
        ayr = [k for k in ks if str(J["hucre"][k].get("hukum", "")).startswith("TUTAR") and J["bh"].get(k)]
        fk = [J["hucre"][k]["fark"] for k in ks if J["hucre"][k].get("fark") is not None]
        cumle = (f"OKUMA: n >= 30 olan {len(ks)} hücrenin {len(ayr)}'inde olay eşinden ayrıştı (c2 TUTAR + BH); eşli fark {100 * min(fk):+.1f} .. "
                 f"{100 * max(fk):+.1f} puan." if fk else "OKUMA: n >= 30 hücre yok.")
        fig.text(0.04, 0.975, "HAFTALIK MUMDA AYNI KALIP: kaç bölge bulundu, sonra ne oldu?", fontsize=11, weight="bold", va="top")
        fig.text(0.04, 0.95, "Bulunan bölge (tam şablon, eşik; evren içi): " + bul, fontsize=7, va="top", wrap=True)
        fig.text(0.04, 0.905, "eş = aynı gün aynı kovadaki öteki hisseler; +%10 / +%20 = stop'tan önce dokunma; stop = bölge dibi x 0,98; ufuk 15 haftalık mum.\n"
                 + cumle, fontsize=7.5, va="top")
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=(8.3, 11.7))
        a1 = fig.add_axes([0.02, 0.35, 0.47, 0.6]); a1.imshow(Image.open(MI.MI_YOL["goruntu"])); a1.axis("off"); a1.set_title("Cemal'in grafiği (4 saatlik)", fontsize=8)
        a2 = fig.add_axes([0.51, 0.35, 0.47, 0.6]); a2.imshow(Image.open(MI._mi_yol("bindirme"))); a2.axis("off"); a2.set_title("kodun şablonu (20 mum; son 3 = tepe)", fontsize=8)
        fig.text(0.05, 0.3, "Kalıp: dipten sonra küçük mumlar, uzun üst fitil, yükselen dipler, alt banttan üst banda yürüyüş.\n"
                 "Aynı şablon ve aynı eşik HAFTALIK mumlara uygulandı (tam S >= 0,59; TAM UYAN S >= 0,69).", fontsize=8)
        pdf.savefig(fig); plt.close(fig)
        G = MH_ESIK["pdf"]
        for r in S.itertuples():
            if r.pazar not in Vc:
                Vc[r.pazar] = MI.mi_veri(r.pazar, kl)["V"]
            W = mh_haftalik(Vc[r.pazar][r.sembol], MH_KESIK)
            t = W.index.get_loc(pd.Timestamp(r.tarih)); a = t - int(r.m) + 1
            i0 = max(0, a - G["once"]); i1 = min(len(W), t + 1 + G["sonra"]); w = W.iloc[i0:i1]; C = W.Close.to_numpy(float)
            BU, BO, BA = MI.mi_bant(C)
            fig = plt.figure(figsize=(8.3, 11.7)); ax = fig.add_axes([0.08, 0.38, 0.88, 0.5])
            MI._mi_mum_ciz(ax, *(w[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")))
            xx = np.arange(i1 - i0)
            ax.plot(xx, BU[i0:i1], color="#9e8fd6"); ax.plot(xx, BA[i0:i1], color="#9e8fd6"); ax.plot(xx, BO[i0:i1], color="#7b3294", linestyle="--", linewidth=1)
            lo_, hi_ = float(w.Low.iloc[a - i0:t - i0 + 1].min()), float(w.High.iloc[a - i0:t - i0 + 1].max())
            ax.add_patch(Rectangle((a - i0 - 0.5, lo_), t - a + 1, hi_ - lo_, facecolor="#ffb347", alpha=0.25, edgecolor="#ff7f00"))
            if pd.notna(getattr(r, "E0", np.nan)):
                ax.axhline(float(r.E0) * 1.10, color="#1a9850", linestyle="--", linewidth=0.8); ax.axhline(float(r.E0) * 1.20, color="#1a9850", linestyle=":", linewidth=0.8)
                ax.axhline(float(r.stop), color="#d73027", linestyle="--", linewidth=0.8)
                ax.axvline(t - i0 + 15.5, color="#555555", linestyle=":", linewidth=0.8)
            ax.set_xticks(xx[::8]); ax.set_xticklabels([d_.strftime("%Y-%m") for d_ in w.index[::8]], fontsize=7, rotation=30); ax.tick_params(labelsize=7)
            fmt = lambda v: "-" if not (isinstance(v, (int, float)) and np.isfinite(v)) else f"{100 * v:+.1f}%"  # noqa: E731
            eksik = "" if i1 - (t + 1) >= G["sonra"] else f" (sonra yalnız {i1 - t - 1} hafta: veri kesiği)"
            ax.set_title(f"{r.pazar} {r.sembol} | bölge {r.bolge_bas} .. {r.tarih} ({int(r.m)} hafta) | {r.sablon}, S {r.S:.2f}"
                         f"{' TAM UYAN' if r.tam_uyan else ''}", fontsize=9)
            fig.text(0.08, 0.32, f"Seçim: {r.grup} (yalnız S'ye göre; ön kayıtlı)\n"
                     f"Sonraki 15 hafta: getiri {fmt(r.R15h)} | aynı gün aynı kovadaki eşlerin ortalaması {fmt(getattr(r, 'es_R15h', np.nan))}\n"
                     f"En yüksek {fmt(r.max15)}, en derin {fmt(r.min15)} | +%10 {('evet' if r.d10 == 1 else 'hayır') if pd.notna(r.d10) else '-'}, "
                     f"+%20 {('evet' if r.d20 == 1 else 'hayır') if pd.notna(r.d20) else '-'}, stop {('evet' if r.stop15 == 1 else 'hayır') if pd.notna(r.stop15) else '-'}\n"
                     f"30 hafta getiri {fmt(getattr(r, 'R30h', np.nan))}{eksik}\n"
                     "Turuncu kutu = bölge; mor = Bollinger 20 / SMA20 (haftalık); yeşil kesik = giriş +%10 / +%20; kırmızı = stop; dikey nokta = 15. hafta",
                     fontsize=8.5, va="top")
            pdf.savefig(fig); plt.close(fig)
    return y


def mh_rapor(cikti: Optional[str] = None) -> str:
    cikti = cikti or MH_YOL["cikti"]; J = json.load(open(_mh_yol("sonuc", cikti), encoding="utf-8"))
    L = [f"# MUM_IZI3 RAPOR ({MI._mi_simdi()})", "", f"Sürüm: {MH_SURUM}", "", "## EVREN x DÖNEM", "",
         "| pazar | şablon | seviye | dönem | n (eşli) | 15 hf ort olay / eş | medyan olay / eş | eşli fark (%95) | SIRA | +%10 olay / eş | +%20 olay / eş | stop olay / eş | plasebo fark ort (%5-%95) / TUTAR + / - | hüküm | BH |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, c in J["hucre"].items():
        p, ad, sev, hc = k.split("|"); pl = J["plasebo"].get(k, {})
        if c.get("n", 0) < 2:
            L.append(f"| {p} | {ad} | {sev} | {hc} | {c.get('n', 0)} | - | - | - | - | - | - | - | - | örneklem yetersiz | - |"); continue
        L.append(f"| {p} | {ad} | {sev} | {hc} | {c['n']} | {MI._p(c['R_ort'])} / {MI._p(c['es_ort'])} | {MI._p(c['R_med'])} / {MI._p(c['es_med'])} | "
                 f"{MI._p(c['fark'], 2)} ({MI._p(c['boot_alt'], 2)}..{MI._p(c['boot_ust'], 2)}) | {MI._s(c['sira'], 3)} | {MI._p(c['d10'], 0)} / {MI._p(c['es_d10'], 0)} | "
                 f"{MI._p(c['d20'], 0)} / {MI._p(c['es_d20'], 0)} | {MI._p(c['stop'], 0)} / {MI._p(c['es_stop'], 0)} | "
                 f"{MI._p(pl.get('fark_ort'), 2)} ({MI._p(pl.get('fark_alt05'), 2)}..{MI._p(pl.get('fark_ust95'), 2)}) / {MI._p(pl.get('tutar_pay_arti'), 0)} / {MI._p(pl.get('tutar_pay_eksi'), 0)} | "
                 f"{c['hukum']} | {'geçti' if J['bh'].get(k) else '-'} |")
    L += ["", "## SAYIM (bulunan / evren içi / ölçülen / eşli / ufuk kesik)", "", "```", json.dumps(J["sayim"], ensure_ascii=False, indent=0)[:6000], "```", "",
          f"Tarama: {J['tarama']}", f"Prefix (K2): {J['prefix']}", f"Yeniden üretim (K10 / K11): {J['yeniden']}", f"Kapı: {J['kapi']}", f"KASA: {J['kasa']}", ""]
    return MI._mi_yaz(_mh_yol("rapor", cikti), "\n".join(L), "rapor 3")


# ================================================================ 8) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_mh(_once=_CK_ONCE_MH, _dosya="MUM_IZI_HAFTALIK.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_MH",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_mh()


def _mh_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_HAFTALIK: kalıp haftalık mumda")
    ap.add_argument("komut", choices=["haftalik_hazirla", "onkayit", "haftalik_kos", "haftalik_pdf", "rapor", "sha"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "sha":
            print(json.dumps({"KOD3_SHA": MI._mi_sha(MH_YOL["kod"]), "ESIK3_SHA": mh_esik_sha()}, indent=1))
        elif a.komut == "haftalik_hazirla":
            J = mh_hazirla(); print(json.dumps(MI._mi_json({k: v for k, v in J.items() if k != "kasa"}), ensure_ascii=False)[:3000])
        elif a.komut == "onkayit":
            print(mh_onkayit_yaz())
        elif a.komut == "haftalik_kos":
            J = mh_kos(); print(json.dumps(MI._mi_json({k: J[k] for k in ("sayim", "bh", "yeniden")}), ensure_ascii=False)[:4000])
        elif a.komut == "haftalik_pdf":
            print(mh_pdf())
        elif a.komut == "rapor":
            print(mh_rapor())
    except MHHata as ex:
        mhlog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_mh_ana())
