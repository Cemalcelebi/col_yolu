"""K55 evren (ONKAYIT_K55 bölüm 1; v1.3 düzeltmeleri, Cemal 30 Ekim): fonsuz ABD evreni + K54 şirket sınıfları + seri sonu işlemi + 4b kesimi +
çift yönlü V / EV denetimi + ayrı dışlama kategorileri + güçlü evren sürümü + garantili benzersiz deneme örneklemi + ağ kapalı kapısı.

Yapı: evren_kur (I/O: yükleyici, K54 dosyaları) -> evren_insa (SAF: yüklenmiş veriden evren; sentetik testlerle sınanır).
K51 yükleyicisi (COL_YOLU_ABD.cy_veri_yukle) değiştirilmez; eşiği (>= 320 gün) programatik olarak doğrulanır.

Evren doğruluğu hızdan ve örneklem büyüklüğünden önce gelir: bir şirketin yanlışlıkla dışarıda kalması ya da başka şirketin fiyatlarının ona
bağlanması sonraki 100 hücreyi bozar. Bu yüzden belirsiz / tutarsız kayıt sessizce "y" sayılmaz, raporlanır ve evren dışı kalır.
"""
from __future__ import annotations

import contextlib
import inspect
import json
import os
import socket
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
import pandas as pd

from .ortak import ALIVE_SINIR, K55Ayar, KOK, MIN_GUN, cy, log, sha256_dosya, sha256_metin

YUKLEYICI_MIN_GUN = 320        # K51 yükleyicisi (cy_veri_yukle) seri uzunluğu eşiği: MIN_GUN (260, özellik) + 60 günlük bir sonuç penceresi
# Sınıf -> izinli K54 çıkış işlemleri -> K55 seri sonu işlemi (ONKAYIT 1 / v1.2 madde 3). Başka her şey BELİRSİZ (evren dışı, raporlanır).
SINIF_ISLEM: Dict[int, Dict[str, str]] = {
    1: {"y": "k51"},                         # halen işlem gören (seri erken bitmişse K51 kuralı)
    2: {"y_d100": "d100"},                   # iflas / tasfiye: seri sonunda −%100
    3: {"y_d0": "d0"},                       # birleşme / satın alma: son kapanış = bedel
    4: {"y_kes": "kes", "y": "k51", "bagla": "k51"},   # 4b kesim; 4b seri erken bitmiş; 4a halef DOĞRULANMAMIŞ -> bağlanmaz, K51 kuralı
    5: {"y": "k51"},                         # belirsiz: K51 kuralı
    6: {},                                   # doğrulanamayan: evren dışı
}
KATEGORI = ("fon_evren_disi", "kisa_seri_yukleyici", "veri_saglayici_eksik", "sinif6", "k54_yok", "k54_tutarsiz", "cikis_belirsiz", "eslesme_yok_cik", "kesim_bos", "v_fazla")
DOGRU = {"true", "1", "yes", "evet", "t", "y"}; YANLIS = {"false", "0", "no", "hayir", "hayır", "f", "n", ""}


# ---------------------------------------------------------------- yardımcılar (saf)
def sembol_normalize(s: Any) -> str:
    """Boşluk kırp, büyük harf. Nokta / tire gösterimleri BİRLEŞTİRİLMEZ (BRK.B ≠ BRK-B; CIK ile eşleşme olmadan aynı şirket sayılmaz)."""
    return str(s).strip().upper()


def bool_cevir(x: Any) -> Optional[bool]:
    """Kontrollü boolean: True / False, 'True' / 'False', 1 / 0; başka her şey None (belirsiz). astype(bool) kullanılmaz ('False' metni True olurdu)."""
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    t = str(x).strip().lower()
    if t in DOGRU:
        return True
    if t in YANLIS:
        return False
    return None


def yukleyici_esigi_dogrula() -> int:
    """K51 yükleyicisinin gerçek seri eşiğini kaynak koddan doğrular (>= 320); farklıysa hata (evren tanımı sessizce kaymasın)."""
    src = inspect.getsource(cy().cy_veri_yukle)
    if f">= {YUKLEYICI_MIN_GUN}" not in src:
        raise RuntimeError(f"K51 yükleyici eşiği {YUKLEYICI_MIN_GUN} değil; K55 YUKLEYICI_MIN_GUN güncellenmeli")
    return YUKLEYICI_MIN_GUN


@contextlib.contextmanager
def ag_kapali():
    """Blok içinde her soket bağlantısı hata verir: evren kurulurken ağ erişimi OLMADIĞININ kanıtı (cy_tiingo_indir etkisizleştirmesi yetmez)."""
    eski = socket.socket.connect; eski_ca = socket.create_connection

    def _yasak(*a, **k):
        raise RuntimeError("K55 evren kurulurken ağ erişimi yasak (network=False)")
    socket.socket.connect = _yasak; socket.create_connection = _yasak
    try:
        yield
    finally:
        socket.socket.connect = eski; socket.create_connection = eski_ca


# ---------------------------------------------------------------- K54 tutarlılık (saf)
def k54_tutarlilik(SD: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """K54_SIRKET_DURUMU satırlarını denetler. Dönüş: temiz tablo (sembol, sinif, alt, cikis_islemi, kesim, erken_bitti, seri_sonu, tutarli, sorun)
    ve sorun listesi. Kurallar: sınıf 1-6 tam sayı; çıkış işlemi sınıfın izinli kümesinde (eksik -> BELİRSİZ, 'y' varsayılmaz); y_kes kesim tarihi
    ister (geçerli tarih); kesim tarihi varken işlem y_kes değilse tutarsız; erken_bitti kontrollü boolean; yinelenen sembol tutarsız."""
    S = SD.copy(); S["sembol"] = S.sembol.map(sembol_normalize); rows = []
    yin = S.sembol.duplicated(keep=False)
    for r in S.itertuples():
        sorun = []
        try:
            sn = int(r.sinif) if pd.notna(r.sinif) else None
        except Exception:
            sn = None
        if sn not in SINIF_ISLEM:
            sorun.append(f"sınıf geçersiz: {r.sinif}")
        isl = str(r.cikis_islemi).strip() if pd.notna(getattr(r, "cikis_islemi", np.nan)) and str(r.cikis_islemi).strip() else ""
        alt = str(getattr(r, "alt", "") or "") if pd.notna(getattr(r, "alt", np.nan)) else ""
        kes = pd.to_datetime(getattr(r, "kesim_tarihi", None), errors="coerce") if pd.notna(getattr(r, "kesim_tarihi", np.nan)) and str(getattr(r, "kesim_tarihi", "")).strip() else pd.NaT
        eb = bool_cevir(getattr(r, "erken_bitti", None))
        seri_sonu = None
        if sn in SINIF_ISLEM:
            if not isl:
                sorun.append("çıkış işlemi eksik (BELİRSİZ; 'y' varsayılmadı)")
            elif isl not in SINIF_ISLEM[sn]:
                sorun.append(f"çıkış işlemi sınıfla uyumsuz: sınıf {sn}, işlem {isl}")
            else:
                seri_sonu = SINIF_ISLEM[sn][isl]
            if sn == 4 and isl == "y_kes" and not alt.startswith("4b"):
                sorun.append("y_kes yalnız 4b'de olur")
            if sn == 4 and alt.startswith("4a") and isl == "bagla":
                sorun.append("4a halef bağlama K55'te doğrulanmış sayılmaz (K51 kuralı uygulanır)")
        if isl == "y_kes" and pd.isna(kes):
            sorun.append("y_kes var, kesim tarihi yok / geçersiz")
        if pd.notna(kes) and isl != "y_kes":
            sorun.append("kesim tarihi var ama işlem y_kes değil")
        if eb is None:
            sorun.append(f"erken_bitti geçersiz: {getattr(r, 'erken_bitti', None)!r}")
        if bool(yin.loc[r.Index]):
            sorun.append("yinelenen sembol")
        tut = not sorun and seri_sonu is not None
        rows.append({"sembol": r.sembol, "sinif": sn, "alt": alt, "cikis_islemi": isl or None, "kesim": kes, "erken_bitti": eb, "seri_sonu": seri_sonu if tut else None,
                     "tutarli": tut, "sorun": "; ".join(sorun)})
    T = pd.DataFrame(rows, columns=["sembol", "sinif", "alt", "cikis_islemi", "kesim", "erken_bitti", "seri_sonu", "tutarli", "sorun"])
    return T, T[~T.tutarli][["sembol", "sinif", "cikis_islemi", "sorun"]].reset_index(drop=True)


# ---------------------------------------------------------------- evren inşası (saf)
def kesim_uygula(d: pd.DataFrame, kes: pd.Timestamp) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """4b: kesim tarihinden sonraki günler (başka şirketin fiyatları) atılır. Kesim günü işlem günü değilse son <= kesim günü kullanılır (raporlanır)."""
    once = len(d); d2 = d[d.index <= kes]; islem_gunu = bool(kes in d.index)
    return d2, {"kesim": str(kes.date()), "kesim_islem_gunu": islem_gunu, "etkin_kesim": str(d2.index[-1].date()) if len(d2) else "", "once": once, "sonra": int(len(d2)), "atilan": once - int(len(d2))}


def evren_insa(V_ham: Dict[str, pd.DataFrame], EV_ham: pd.DataFrame, SD: pd.DataFrame, ES: pd.DataFrame, fon_disi: Set[str], ham_kisa: Optional[pd.DataFrame] = None,
               saglayici_eksik: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Saf evren inşası. V_ham: yükleyiciden gelen fiyat sözlüğü; EV_ham: yükleyici evren tablosu (pazar, sembol, kaynak, evren_bas, batan, agirlik);
    SD / ES: K54 tabloları; fon_disi: evren_disi_ABD.csv sembolleri (bilgi; yükleyici zaten çıkarmış olabilir).
    Dönüş: V, EV, kesim tablosu, dışlama tablosu (kategori ayrı), K54 sorunları, tutarlılık raporu."""
    T, sorunlar = k54_tutarlilik(SD); Tx = T.drop_duplicates("sembol", keep="first").set_index("sembol")
    ES = ES.copy(); ES["sembol"] = ES.sembol.map(sembol_normalize); es = ES.drop_duplicates("sembol").set_index("sembol")
    V: Dict[str, pd.DataFrame] = {sembol_normalize(s): d for s, d in V_ham.items()}
    if len(V) != len(V_ham):
        raise RuntimeError("fiyat sözlüğünde normalize edince çakışan semboller var (büyük / küçük harf ya da boşluk)")
    EV = EV_ham.copy(); EV["sembol"] = EV.sembol.map(sembol_normalize)
    if EV.sembol.duplicated().any():
        raise RuntimeError(f"evren tablosunda yinelenen sembol: {EV.sembol[EV.sembol.duplicated()].tolist()[:10]}")
    disi: List[Dict[str, Any]] = []
    for s in sorted(fon_disi):
        disi.append({"kategori": "fon_evren_disi", "sembol": s, "ayrinti": "evren_disi_ABD.csv (fon)"})
    if ham_kisa is not None and len(ham_kisa):
        disi += [{"kategori": "kisa_seri_yukleyici", "sembol": r.sembol, "ayrinti": f"{r.kaynak}: {r.n_gun} gün < {YUKLEYICI_MIN_GUN} (yükleyici eşiği)"} for r in ham_kisa.itertuples()]
    if saglayici_eksik is not None and len(saglayici_eksik):
        disi += [{"kategori": "veri_saglayici_eksik", "sembol": r.sembol, "ayrinti": r.ayrinti} for r in saglayici_eksik.itertuples()]
    # EV'de olup V'de olmayan: hata (yükleyici tutarsız); V'de olup EV'de olmayan: raporla ve V'den çıkar
    ev_yok = sorted(set(EV.sembol) - set(V))
    if ev_yok:
        raise RuntimeError(f"evren tablosundaki {len(ev_yok)} sembolün fiyat serisi yok: {ev_yok[:10]}")
    for s in sorted(set(V) - set(EV.sembol)):
        disi.append({"kategori": "v_fazla", "sembol": s, "ayrinti": "fiyat serisi var, evren tablosunda yok (çıkarıldı)"}); V.pop(s)
    # K54 bağlama
    EV["sinif"] = EV.sembol.map(Tx.sinif); EV["alt"] = EV.sembol.map(Tx.alt).fillna(""); EV["cikis_islemi"] = EV.sembol.map(Tx.cikis_islemi)
    EV["kesim"] = pd.to_datetime(EV.sembol.map(Tx.kesim), errors="coerce"); EV["erken_bitti_k54"] = EV.sembol.map(Tx.erken_bitti); EV["seri_sonu"] = EV.sembol.map(Tx.seri_sonu)
    EV["k54_tutarli"] = EV.sembol.map(Tx.tutarli); EV["k54_sorun"] = EV.sembol.map(Tx.sorun).fillna("")
    EV["cik"] = EV.sembol.map(es.cik) if "cik" in es else np.nan; EV["sec_ad"] = EV.sembol.map(es.sec_ad).fillna("") if "sec_ad" in es else ""
    tut = []
    for r in EV.itertuples():
        if r.sembol not in Tx.index:
            disi.append({"kategori": "k54_yok", "sembol": r.sembol, "ayrinti": "K54_SIRKET_DURUMU'nda yok (doğrulanamayan)"}); tut.append(False); continue
        if pd.notna(r.sinif) and int(r.sinif) == 6:
            disi.append({"kategori": "sinif6", "sembol": r.sembol, "ayrinti": "K54 sınıf 6 (işlem geçmişi doğrulanamayan)"}); tut.append(False); continue
        if not bool(r.k54_tutarli):
            kat = "cikis_belirsiz" if ("eksik" in r.k54_sorun or "uyumsuz" in r.k54_sorun) else "k54_tutarsiz"
            disi.append({"kategori": kat, "sembol": r.sembol, "ayrinti": r.k54_sorun}); tut.append(False); continue
        tut.append(True)
    EV = EV[np.array(tut, dtype=bool)].copy()
    for s in sorted(set(V) - set(EV.sembol)):                               # evren dışı bırakılan sembollerin serileri de çıkar (kategorileri yukarıda yazıldı)
        V.pop(s)
    EV["sinif"] = EV.sinif.astype(int)
    EV["eslesme_yok_cik"] = EV.cik.isna()
    for s in EV.sembol[EV.eslesme_yok_cik]:
        disi.append({"kategori": "eslesme_yok_cik", "sembol": s, "ayrinti": "CIK eşleşmesi yok (evrende kalır, K54 sınıfı var; bilgi)"})
    # 4b kesimi
    kesim_rows = []; bos = []
    for r in EV.itertuples():
        if r.seri_sonu == "kes":
            d2, bilgi = kesim_uygula(V[r.sembol], pd.Timestamp(r.kesim)); kesim_rows.append({"sembol": r.sembol, **bilgi})
            if len(d2) == 0:
                bos.append(r.sembol); disi.append({"kategori": "kesim_bos", "sembol": r.sembol, "ayrinti": f"kesim {bilgi['kesim']} seri başından önce; seri boş"}); V.pop(r.sembol)
            else:
                V[r.sembol] = d2
    EV = EV[~EV.sembol.isin(bos)].copy()
    EV["seri_sonu_getiri"] = EV.seri_sonu.replace({"kes": "k51"})       # kesim sonrası seri sonu getiri kuralı: K51 (başka şirket değil, veri kesintisi)
    EV["son_islem"] = EV.sembol.map(lambda s: V[s].index[-1]); EV["ilk_islem"] = EV.sembol.map(lambda s: V[s].index[0]); EV["n_gun"] = EV.sembol.map(lambda s: len(V[s]))
    EV["seri_erken"] = EV.son_islem < pd.Timestamp(ALIVE_SINIR)
    EV["likidite_medyan"] = EV.sembol.map(lambda s: float((V[s].Close * V[s].Volume).tail(250).median()))
    EV["lik_uclu"] = pd.qcut(EV.likidite_medyan.rank(method="first"), 3, labels=[0, 1, 2]).astype(int) if len(EV) >= 3 else 1
    EV["sembol_varyant"] = EV.sembol.str.contains(r"[.\-]", regex=True)
    rapor = tutarlilik_V_EV(V, EV)
    D = pd.DataFrame(disi, columns=["kategori", "sembol", "ayrinti"]); KS = pd.DataFrame(kesim_rows, columns=["sembol", "kesim", "kesim_islem_gunu", "etkin_kesim", "once", "sonra", "atilan"])
    EV = EV.sort_values("sembol").reset_index(drop=True)
    return {"V": V, "EV": EV, "kesim": KS, "disi": D, "k54_sorun": sorunlar, "tutarlilik": rapor, "k54_tablo": T}


def tutarlilik_V_EV(V: Dict[str, pd.DataFrame], EV: pd.DataFrame) -> Dict[str, Any]:
    """Çift yönlü: EV'deki her sembolün serisi var; V'de EV dışı sembol yok; kesilmiş serilerde kesim sonrası satır yok; seri boş değil."""
    ev_set = set(EV.sembol); v_set = set(V)
    ev_serisiz = sorted(ev_set - v_set); v_fazla = sorted(v_set - ev_set); bos = [s for s in ev_set & v_set if len(V[s]) == 0]
    kesim_hata = [r.sembol for r in EV.itertuples() if r.seri_sonu == "kes" and pd.notna(r.kesim) and (V[r.sembol].index > pd.Timestamp(r.kesim)).any()]
    out = {"ev_serisiz": ev_serisiz, "v_fazla": v_fazla, "bos_seri": bos, "kesim_sonrasi_satir": kesim_hata}
    out["gecti"] = not (ev_serisiz or v_fazla or bos or kesim_hata)
    if not out["gecti"]:
        raise RuntimeError(f"V / EV tutarsız: {out}")
    return out


# ---------------------------------------------------------------- evren sürümü (güçlü)
def evren_surum(EV: pd.DataFrame, dosya_sha: Dict[str, str], veri_sha: Dict[str, str]) -> str:
    """sha256: EV içeriği (sembol, kaynak, sınıf, çıkış işlemi, seri sonu, kesim, ilk / son gün, n) + K54 dosyaları + evren_disi + veri paketi
    sha'ları + sınıflandırma / kesim kuralları (SINIF_ISLEM, YUKLEYICI_MIN_GUN, MIN_GUN, ALIVE_SINIR). Aynı sürüm altında farklı fiyat ya da sınıf olamaz."""
    kol = ["sembol", "kaynak", "sinif", "cikis_islemi", "seri_sonu", "n_gun"]
    metin = EV[kol].astype(str).agg("|".join, axis=1).str.cat(sep="\n") + "\n" + EV.kesim.astype(str).str.cat(sep=",") + "\n" + EV.ilk_islem.astype(str).str.cat(sep=",") + "\n" + EV.son_islem.astype(str).str.cat(sep=",")
    kural = json.dumps({"SINIF_ISLEM": SINIF_ISLEM, "YUKLEYICI_MIN_GUN": YUKLEYICI_MIN_GUN, "MIN_GUN": MIN_GUN, "ALIVE_SINIR": ALIVE_SINIR}, sort_keys=True)
    return sha256_metin(metin + "\n" + json.dumps(dosya_sha, sort_keys=True) + "\n" + json.dumps(veri_sha, sort_keys=True) + "\n" + kural)


# ---------------------------------------------------------------- I/O: yükleme + inşa
def _k54_oku(A: K55Ayar) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, str]]:
    sd_yol = os.path.join(A.k54, "K54_SIRKET_DURUMU.csv"); es_yol = os.path.join(A.k54, "K54_EVREN_ESLESTIRME.csv"); ed = os.path.join(KOK, "evren_disi_ABD.csv")
    for y in (sd_yol, es_yol, ed):
        if not os.path.exists(y):
            raise FileNotFoundError(f"evren girdisi yok: {y} (K55 koşulmaz)")
    SD = pd.read_csv(sd_yol, dtype={"kesim_tarihi": str, "erken_bitti": str, "cikis_islemi": str, "alt": str}); ES = pd.read_csv(es_yol)
    return SD, ES, {"K54_SIRKET_DURUMU.csv": sha256_dosya(sd_yol), "K54_EVREN_ESLESTIRME.csv": sha256_dosya(es_yol), "evren_disi_ABD.csv": sha256_dosya(ed)}


def _ham_kisa_ve_eksik(A: K55Ayar, V: Dict[str, pd.DataFrame], fon_disi: Set[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Yükleyici dışı kalanlar: V_ABD.pkl'de kısa seri (< 320); K34 listesinde olup fiyat dosyası / serisi olmayan (veri sağlayıcı eksik ya da kısa)."""
    kisa = []; eksik = []
    try:
        import pickle
        with open(os.path.join(A.veri, "V_ABD.pkl"), "rb") as f:
            ham = pickle.load(f)
        ham = ham.get("veri", ham) if isinstance(ham, dict) and "veri" in ham else ham
        for s, d in ham.items():
            s = sembol_normalize(s)
            if s not in V and s not in fon_disi and hasattr(d, "__len__") and len(d) < YUKLEYICI_MIN_GUN:
                kisa.append({"sembol": s, "kaynak": "V_ABD", "n_gun": int(len(d))})
    except Exception as ex:
        log.warning("V_ABD kısa seri taraması yapılamadı: %s", ex)
    ky = os.path.join(A.veri, "k34_evren.csv")
    if os.path.exists(ky):
        E = pd.read_csv(ky); yy = os.path.join(A.veri, "k34_yahoo.pkl"); Y = pd.read_pickle(yy) if os.path.exists(yy) else {}; tk = A.k54 and os.path.join(A.veri, "tiingo")
        for r in E.itertuples():
            s = sembol_normalize(r.sembol)
            if s in V or s in fon_disi:
                continue
            if r.kaynak == "yahoo":
                d = Y.get(r.sembol) if isinstance(Y, dict) else None
                if d is None or not len(d):
                    eksik.append({"sembol": s, "ayrinti": "K34 Yahoo: fiyat serisi yok (sağlayıcı eksik)"})
                else:
                    kisa.append({"sembol": s, "kaynak": "K34_yahoo", "n_gun": int(len(d))})
            else:
                yol = os.path.join(tk, f"{r.sembol}.csv")
                if not os.path.exists(yol):
                    eksik.append({"sembol": s, "ayrinti": "K34 Tiingo: fiyat dosyası yok (indirilmedi / lisans; sağlayıcı eksik)"})
                else:
                    try:
                        n = max(0, sum(1 for _ in open(yol, encoding="utf-8")) - 1)
                    except Exception:
                        n = -1
                    kisa.append({"sembol": s, "kaynak": "K34_tiingo", "n_gun": n})
    return pd.DataFrame(kisa, columns=["sembol", "kaynak", "n_gun"]), pd.DataFrame(eksik, columns=["sembol", "ayrinti"])


def evren_kur(A: K55Ayar, veri_sha: Optional[Dict[str, str]] = None, network: bool = False) -> Dict[str, Any]:
    """Evreni kurar (I/O). network=False: bütün yükleme ag_kapali kapısı içinde (soket açılırsa durur) ve cy_tiingo_indir etkisiz.
    Dönüş: evren_insa sözlüğü + 'surum', 'dosya_sha'."""
    C = cy(); yukleyici_esigi_dogrula(); Ac = C.CYAyar(veri=A.veri, cikti=A.cikti, pazarlar=("ABD",), is_parcacigi=A.isci)
    if not os.path.exists(os.path.join(A.veri, "V_ABD.pkl")):
        raise FileNotFoundError(f"{A.veri}/V_ABD.pkl yok; K55 evren kurulurken veri paketi indirilmez (önce paketi aç)")
    SD, ES, dosya_sha = _k54_oku(A); fon_disi = set(pd.read_csv(os.path.join(KOK, "evren_disi_ABD.csv")).sembol.map(sembol_normalize))
    eski_indir = C.cy_tiingo_indir; kapi = ag_kapali() if not network else contextlib.nullcontext()
    try:
        C.cy_tiingo_indir = lambda *a, **k: 0
        with kapi:
            Vs, EV_ham = C.cy_veri_yukle(Ac, C.CY)
    finally:
        C.cy_tiingo_indir = eski_indir
    if "ABD" not in Vs:
        raise RuntimeError("ABD verisi yüklenemedi")
    V_ham = Vs["ABD"]; EV_ham = EV_ham[EV_ham.pazar == "ABD"].copy()
    kisa, eksik = _ham_kisa_ve_eksik(A, {sembol_normalize(s): 1 for s in V_ham}, fon_disi)
    R = evren_insa(V_ham, EV_ham, SD, ES, fon_disi, kisa, eksik)
    sek = C.cy_sektor(Ac, R["EV"]); R["EV"]["sektor"] = R["EV"].sembol.map(sek).fillna("bilinmiyor")
    if veri_sha is None:
        from .ortak import veri_sha as _vs
        veri_sha = _vs(A)
    R["surum"] = evren_surum(R["EV"], dosya_sha, veri_sha); R["dosya_sha"] = dosya_sha
    D = R["disi"]; log.info("evren: %d sembol (sınıf %s); dışlama kategorileri %s; 4b kesim %d; sürüm %s", len(R["EV"]), R["EV"].sinif.value_counts().sort_index().to_dict(),
                            D.kategori.value_counts().to_dict() if len(D) else {}, len(R["kesim"]), R["surum"][:12])
    return R


# ---------------------------------------------------------------- deneme örneklemi (saf; garantili benzersiz)
KOTA_50: Tuple[Tuple[str, int, Optional[int], int], ...] = (          # (kaynak, sınıf, likidite üçlüsü | None, kota)
    ("V_ABD", 1, 0, 10), ("V_ABD", 1, 1, 10), ("V_ABD", 1, 2, 10), ("K34_yahoo", 1, None, 8),
    ("K34_tiingo", 2, None, 4), ("K34_tiingo", 3, None, 4), ("K34_tiingo", 5, None, 2), ("K34_tiingo", 4, None, 2))


def ornek_sec(EV: pd.DataFrame, n: int, tohum: int, kota: Tuple[Tuple[str, int, Optional[int], int], ...] = KOTA_50) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Tabakalı, tohumlu, TEKRARSIZ örneklem. Her tabaka: kaynak × sınıf (× likidite üçlüsü); aday yoksa / azsa eksik raporlanır (gizlenmez), kalan
    kontenjan seçilmemiş sembollerden tamamlanır. Evren n'den küçükse hepsi alınır ve raporlanır. Dönüş: (seçilen EV satırları, dağılım tablosu)."""
    rng = np.random.default_rng(tohum); olcek = n / sum(k for *_, k in kota); secilen: List[str] = []; sec_set: Set[str] = set(); dag = []
    for kay, sn, lk, k in kota:
        hedef = max(1, int(round(k * olcek)))
        m = (EV.kaynak == kay) & (EV.sinif == sn)
        if lk is not None and "lik_uclu" in EV:
            m &= EV.lik_uclu == lk
        aday = np.sort(EV.sembol[m & ~EV.sembol.isin(sec_set)].to_numpy())
        al = list(rng.choice(aday, size=min(hedef, len(aday)), replace=False)) if len(aday) else []
        secilen += al; sec_set.update(al)
        dag.append({"tabaka": f"{kay} sınıf {sn}" + (f" lik {lk}" if lk is not None else ""), "kaynak": kay, "sinif": sn, "lik_uclu": lk, "kota": hedef, "aday": int(len(aday)), "secilen": len(al), "eksik": hedef - len(al)})
    kalan = n - len(secilen)
    if kalan > 0:
        havuz = np.sort(EV.sembol[~EV.sembol.isin(sec_set)].to_numpy()); al = list(rng.choice(havuz, size=min(kalan, len(havuz)), replace=False)) if len(havuz) else []
        secilen += al; sec_set.update(al)
        dag.append({"tabaka": "tamamlama (eksik tabakalar yerine, tekrarsız)", "kaynak": "", "sinif": -1, "lik_uclu": None, "kota": kalan, "aday": int(len(havuz)), "secilen": len(al), "eksik": kalan - len(al)})
    if len(secilen) != len(set(secilen)):
        raise RuntimeError("örneklemde yinelenen sembol (hata)")
    if len(secilen) < n and len(EV) >= n:
        raise RuntimeError(f"örneklem {len(secilen)} < {n} (evren {len(EV)})")
    D = pd.DataFrame(dag); D["toplam_secilen"] = len(secilen); D["istenen"] = n; D["evren"] = len(EV)
    return EV[EV.sembol.isin(sec_set)].reset_index(drop=True), D


def evren_daralt(V: Dict[str, pd.DataFrame], EV: pd.DataFrame, EVo: pd.DataFrame) -> Tuple[Dict[str, pd.DataFrame], pd.DataFrame]:
    s = set(EVo.sembol); return {k: v for k, v in V.items() if k in s}, EV[EV.sembol.isin(s)].reset_index(drop=True)
