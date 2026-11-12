"""K62-B — BİLANÇO SÜRPRİZİ ÇÖL SİNYALİNE EK BİLGİ TAŞIYOR MU? Tek dosya (12 Kasım 2026; ana oturum iş tanımı; ön kayıt
arastirma_cikti/col_dis_bilgi/K62B_ON_KAYIT.md).

Tasarım K64 + K65 ile AYNIDIR (K64_K65_ON_KAYIT.md): olay (ANA K24, İKİNCİL D13), S1 (çöl olayları içinde değişkenin ÜST / ALT üçte biri; ÜST - ALT ay kümeli
bootstrap; 'ek katkı' kuralı), S2 (çöl dışı evren; bilgi), cetvel (FON_IZI FI_OLCUT aynen), piyasa koşulu, maliyet, dönemler, karar ve BH. K64.py, K62.py,
K60.py ve FON_IZI.py MODÜL olarak içe alınır ve DEĞİŞMEZ; yalnız değişkenler yenidir (K62'nin sürpriz tanımları, çöl sinyal günü t'de bilinen SON açıklamaya göre):
  SUETF_C  (E_q - E_{q-4}) / MV_q  (K62 SUETF). BIST: K62 verisi (KAP ilk Finansal Rapor + İş Yatırım); TMS 29 kirli çeyrekler YOK. ABD: SEC frames (K60 demeti),
           net kâr NetIncomeLoss çeyreklik, MV_q = çeyrek sonu fiyat x o gün bilinen pay (K60 kuralı).
  EAR_C    [ta-1, ta+1] al-tut getirisi - eşleşen 2x3 büyüklük-DD/PD portföyününki (K62 EAR; K62.k62_portfoy_ata / k62_hazirla / _k62_altut).
  Bilgi:   ÇÖL + SÜRPRİZ (son açıklamada SUETF ve EAR ikisi de üst üçte bir; K62 C kuralı: önceki çeyreğin karar gününde bilinen kesimleri) ve 'son 90 günde
           açıklama yok' sınıfları.
Kural: açıklama ta değeri t'de ancak karar günü (ta'nın işlem günü + 1) < t VE ta >= t - 90 takvim günü ise kullanılır; yoksa değer YOK ('son 90 günde açıklama yok').

Komut:  python -I K62B.py kapsam    yalnız SAYIM (olay, son açıklama kapsamı, değişken kapsamı, ÜST / ALT n'leri iki sıra türüyle); getiri HESAPLANMAZ
        python K62B.py onkayit      ön kaydı yazar (ölçümden ÖNCE; mühür + veri sha256 + kapsam; varsa üzerine yazmaz)
        python -I K62B.py kos       mühür + veri sha256 + ön kayıt git'e işlenmiş ve değişmemiş -> ölçüm + rapor
        python K62B.py rapor        K62B_RAPOR.md'yi çıktılardan yeniden yazar
Colab:  exec(open('K62B.py').read()); k62b_kos()
Veri:   /tmp/veri/V_BIST.pkl, V_ABD.pkl (islenmis-veri dalı), /tmp/k62_veri (K62 önbelleği), /tmp/k60_* (K60 önbellekleri). Ağ yok; SEC'e istek atılmaz;
        kişisel e-posta / anahtar yok. Çıktılar arastirma_cikti/col_dis_bilgi/ (k62b_*).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K62B = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K62B = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K62B not in sys.path:
    sys.path.insert(0, KOK_K62B)

import K62  # noqa: E402
import K64  # noqa: E402

FI, K60 = K64.FI, K64.K60

k62blog = logging.getLogger("col.k62b")
if not k62blog.handlers:
    _k62b_h = logging.StreamHandler(sys.stderr)
    _k62b_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k62b: %(message)s", "%H:%M:%S"))
    k62blog.addHandler(_k62b_h)
    k62blog.setLevel(logging.INFO)
    k62blog.propagate = False

K62B_SURUM = "K62-B v1.0 (2026-11-12): bilanço sürprizi (K62 SUETF / EAR, çöl günü bilinen son açıklama) çöl sinyaline ek bilgi; K64 tasarımı aynen, BIST + ABD"
K62B_YOL = {"cikti": os.path.join(KOK_K62B, "arastirma_cikti", "col_dis_bilgi"), "veri": os.environ.get("K62B_VERI", K64.K64_YOL["veri"])}
K62B_DOSYA = {"onkayit": "K62B_ON_KAYIT.md", "kapsam": "k62b_kapsam.csv", "kapsam_ozet": "k62b_kapsam_ozet.json", "olay": "k62b_olaylar.csv.gz", "s1": "k62b_s1.csv",
              "fark": "k62b_s1_fark.csv", "s2": "k62b_s2.csv", "karar": "k62b_karar.csv", "bilgi": "k62b_bilgi.csv", "meta": "k62b_meta.json", "rapor": "K62B_RAPOR.md"}
_K62B_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256'sı ön kayıtta; sonradan değişmez)
_K62B_DEGISKEN: List[Tuple[str, str, str, str]] = [
    ("SUETF_C", "SUETF_C", "t'de bilinen son açıklamanın SUETF'i = (E_q - E_{q-4}) / MV_q (K62 tanımı). E = çeyreklik net kâr (BIST: İş Yatırım ana ortaklık payı, birikimli "
     "farkı; ABD: SEC NetIncomeLoss çeyreklik), MV_q = çeyrek sonu piyasa değeri. BIST'te TMS 29 kirli çeyreğin (K62 B3) değeri YOK", "Ahlatcıoğlu & Okay 2021; K62 (BIST PEAD)"),
    ("EAR_C", "EAR_C", "t'de bilinen son açıklamanın EAR'ı = prod[ta-1, ta+1](1 + R_i) - prod(1 + R_p); p = 2x3 büyüklük-DD/PD portföyü (Haziran sonu; K62 kuralı); "
     "ta = açıklama gününe eşit ya da sonraki ilk işlem günü", "Ahlatcıoğlu & Okay 2021; K62 (BIST PEAD)"),
]

K62B_ESIK: Dict[str, Any] = {
    "kriz": K64.K64_ESIK["kriz"],
    "donem": copy.deepcopy(K64.K64_ESIK["donem"]),
    "bagimsiz": list(K64.K64_ESIK["bagimsiz"]),
    "pazar": ["BIST", "ABD"], "karar_pazari": "ABD",
    "olay": copy.deepcopy(K64.K64_ESIK["olay"]),
    # KARAR SIRASI: kapsam sayımı görülerek, getiri görülmeden, 'sira_secim' kuralıyla seçildi (12 Kasım 2026; EAR_C ABD 2022-2026 EVREN ÜST 592 / ALT 1218, oran
    # 0,49 < 0,5 -> İÇ; SUETF_C bütün hücrelerde oran >= 0,66 -> EVREN); onkayit kuralın sonucuyla aynı olmasını denetler.
    "sira": {"ust": 2.0 / 3.0, "alt": 1.0 / 3.0, "min_evren": 30, "ic_gun": 365, "ic_min": 30, "karar": {"SUETF_C": "EVREN", "EAR_C": "IC"}},
    "sira_secim": {"n_min": 30, "oran_min": 0.5, "hucre": "ANA tanım x iki pazar x iki bağımsız dönem, EVREN sırası; değişken başına"},
    "surpriz": {"pencere_gun": 90, "karar_gecikme_islem": 1, "abd_bilgi_kaynak": [1], "abd_mv_gun": 10, "ileri_tasima": 5, "takvim_tol_gun": 10},
    "s1": {"n_esik": 30, "bootstrap": 2000, "tohum": 62201, "guven": [2.5, 97.5], "gecerli_pay": 0.90},
    "s2": {"bootstrap": 2000, "tohum": 62202},
    "ek_ufuk": 20, "piyasa": {"sma": 200, "min_hisse": 30},
    "maliyet": dict(K64.K64_ESIK["maliyet"]),
    "coklu": {"bh_q": 0.10},
    "bilgi_grup": ["CS", "CS_DEGIL", "YOK90"],
    "degisken": [{"kod": k, "aile": a, "tanim": t, "kaynak": ky} for k, a, t, ky in _K62B_DEGISKEN],
}


class K62BHata(RuntimeError):
    """K62-B'ye özgü durdurucu hata (ön kayıt yok / değişmiş / git'e işlenmemiş, karar sırası seçilmemiş, veri eksik ya da farklı, çıktı yok)."""


def _k62b_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K62B_YOL["cikti"], K62B_DOSYA.get(ad, ad))


def _k62b_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def k62b_kodlar(E: Optional[Dict[str, Any]] = None) -> List[str]:
    return K64.k64_kodlar(E or K62B_ESIK)


def k62b_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: K62B_ESIK + dış tanımlar (K64 bağımlıları: FI_K24, FI_OLCUT, K60 bilgi kuralı + mührü, COL_v1 D13; K64 mührü; K62 mührü)."""
    s = json.dumps({"K62B_ESIK": E or K62B_ESIK, "bagimli": K64._k64_bagimli(), "K64_muhur": K64.k64_esik_sha(), "K62_muhur": K62.k62_esik_sha()},
                   sort_keys=True, default=str, ensure_ascii=False)
    return K62._k62_metin_sha(s)


def _k62b_ffill(X: np.ndarray, limit: int) -> np.ndarray:
    return pd.DataFrame(X).ffill(limit=limit).to_numpy(float)


_K62B_DUYURU_KOL = ["sembol", "yil", "ceyrek", "ann", "t_gun", "karar", "karar_i", "SUETF", "EAR", "kirli"]


# ---------------------------------------------------------------- 1) AÇIKLAMA TABLOLARI (her açıklama için SUETF ve EAR; yalnız açıklama ve öncesi bilgi)
def k62b_bist_duyuru(D: Dict[str, Any], E62: Optional[Dict[str, Any]] = None, H: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """BIST açıklamaları (K62 demeti: KAP ilk Finansal Rapor + İş Yatırım). SUETF ve EAR K62.k62_olay_tablosu ile BİREBİR aynı formülle (bayraklar K62'den, sayım
    modunda; CAR HESAPLANMAZ). ta = yayın gününe eşit ya da sonraki ilk işlem günü; karar = ta + 1 işlem günü. kirli = TMS 29 kirli çeyrek (K62 B3): SUETF YOK."""
    E62 = E62 or K62.K62_ESIK; H = H or K62.k62_hazirla(D, E62, True)
    Ev = K62.k62_olay_tablosu(D, E62, False, H); tak = D["takvim"]; T = len(tak); kol = {k: j for j, k in enumerate(D["kod"])}
    Q = K62.k62_ceyreklik(D["mali"]); PDf = _k62b_ffill(D["PD"], 5); R, Rp, A, Pid = H["R"], H["Rp"], H["A"], H["Pid"]
    e0, e1 = E62["olay"]["ear"]; kirli = {(int(a), int(b)) for a, b in E62["bolum_b"]["tms29_haric"]}; sat = []
    for r in Ev.itertuples():
        j = kol[r.kod]; t = int(r.t_i); y, c = int(r.yil), int(r.ceyrek)
        qs = pd.Timestamp(year=y, month=3 * c, day=1) + pd.offsets.MonthEnd(0); iq = K62._k62_son_gun(tak, qs)
        eq, e4 = Q.get((r.kod, y, c), (np.nan, np.nan))[0], Q.get((r.kod, y - 1, c), (np.nan, np.nan))[0]
        mv = PDf[iq, j] if iq >= 0 and tak[iq] > qs - pd.Timedelta(days=10) else np.nan
        su = float((eq - e4) / mv) if r.f_mali else np.nan
        ear = np.nan
        if r.f_ear:
            pid = int(Pid[t, j]); ear = K62._k62_altut(R[t + e0:t + e1 + 1, j], Rp[t + e0:t + e1 + 1, pid], A[t + e0:t + e1 + 1, j])[0]
        kr = (y, c) in kirli
        sat.append({"sembol": r.kod, "yil": y, "ceyrek": c, "ann": pd.Timestamp(r.yayin).normalize(), "t_gun": tak[t] if t < T else pd.NaT,
                    "karar": tak[t + 1] if t + 1 < T else pd.NaT, "karar_i": t + 1, "SUETF": np.nan if kr else su, "EAR": ear, "kirli": kr})
    return pd.DataFrame(sat, columns=_K62B_DUYURU_KOL)


def k62b_abd_demet(Va_sembol: List[str], D60: Dict[str, Any]) -> Dict[str, Any]:
    """ABD alt demeti (V_ABD sembolleri; K60 demetinden): gun, kod, C (bölünme düzeltmeli kapanış), A (düzeltilmiş kapanış), T (temel tablo; K64.k64_abd_temel),
    bolunme, var (K60 demetinde bulunan sembol). Demette olmayan sembol: NaN."""
    T, bol, var = K64.k64_abd_temel(Va_sembol, D60); ix = {s: j for j, s in enumerate(D60["sembol"])}; c = np.array([ix.get(s, 0) for s in Va_sembol], int)

    def al(X: np.ndarray) -> np.ndarray:
        Y = np.array(X[:, c], dtype=float, copy=True); Y[:, ~var] = np.nan
        return Y
    return {"gun": pd.DatetimeIndex(D60["gun"]), "kod": list(Va_sembol), "C": al(D60["C"]), "A": al(D60["A"]), "T": T, "bolunme": bol, "var": var}


def k62b_abd_duyuru(Dz: Dict[str, Any], E: Optional[Dict[str, Any]] = None, E62: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """ABD açıklamaları: her (hisse, çeyrek) için açıklama günü = K60 BİLGİ TARİHİ (çeyrek sonundan >= 15 gün sonraki ilk 10-Q / 10-K başvurusu); yalnız gerçek
    başvuru günü olanlar (bilgi_kaynak 1; yedek kural günü açıklama günü değildir). SUETF = (NI_q - NI_{q-4}) / MV_q; MV_q = çeyrek sonuna eşit ya da önceki son
    işlem günündeki (en çok abd_mv_gun gün geride) bölünme düzeltmeli kapanış x o gün bilinen pay (K60.k60_pay; bugünkü birim). EAR = K62 EAR: 2x3 portföy
    K62.k62_portfoy_ata ile (Haziran sonu PD = kapanış x pay; DD = takvim yılı Y-1'de biten mali yılın SEC özkaynağı, bilgi tarihi Haziran sonundan önce),
    günlük getiriler düzeltilmiş kapanıştan. Döner (tablo, özet)."""
    E = E or K62B_ESIK; E62 = E62 or K62.K62_ESIK; Sp = E["surpriz"]; gun = Dz["gun"]; gD = gun.to_numpy("datetime64[D]"); G = len(gD); S = list(Dz["kod"]); N = len(S)
    T = Dz["T"]; nq = T["bit"].shape[0]; I = k62b_abd_portfoy_girdi(Dz, E); ME, sat_ix, pb, pb_ok = I["ME"], I["sat_ix"], I["pb"], I["pb_ok"]
    H = K62.k62_hazirla(I["Dk"], E62, True); R, Rp, A, Pid, RpA = H["R"], H["Rp"], H["A"], H["Pid"], H["RpA"]
    e0, e1 = E62["olay"]["ear"]; pay = E62["olay"]["getiri_pay"]; NI = T["Q"].get("NetIncomeLoss"); kay = T.get("bilgi_kaynak"); bilgi = np.asarray(T["bilgi"], "datetime64[D]")
    bit = np.asarray(T["bit"], "datetime64[D]"); tol = np.timedelta64(int(Sp["takvim_tol_gun"]), "D")
    sat = []; say = {"ceyrek_hisse": int((~np.isnat(bit)).sum()), "gercek_gun": 0, "yedek_gun": 0, "takvim_disi": 0}
    for j in range(N):
        for q in range(nq):
            if np.isnat(bit[q, j]) or np.isnat(bilgi[q, j]):
                continue
            if kay is None or int(kay[q, j]) not in Sp["abd_bilgi_kaynak"]:
                say["yedek_gun"] += 1; continue
            say["gercek_gun"] += 1; ann = bilgi[q, j]; t = int(np.searchsorted(gD, ann, side="left"))
            takvimde = bool(t < G and gD[t] - ann <= tol)
            if not takvimde:
                say["takvim_disi"] += 1
            su = np.nan
            if NI is not None and q >= 4 and pb_ok[q, j]:
                eq, e4, mv = NI[q, j], NI[q - 4, j], ME[sat_ix[int(pb[q, j])], j]
                if np.isfinite(eq) and np.isfinite(e4) and np.isfinite(mv) and mv > 0:
                    su = float((eq - e4) / mv)
            ear = np.nan
            if takvimde and t + e0 >= 1 and t + e1 < G:
                pid = int(Pid[t, j])
                if pid >= 0 and A[t + e0:t + e1 + 1, j].sum() >= int(np.ceil(pay * (e1 - e0 + 1) - 1e-9)) and RpA[t + e0:t + e1 + 1, pid].all():
                    ear = K62._k62_altut(R[t + e0:t + e1 + 1, j], Rp[t + e0:t + e1 + 1, pid], A[t + e0:t + e1 + 1, j])[0]
            b_ = pd.Timestamp(bit[q, j])
            sat.append({"sembol": S[j], "yil": b_.year, "ceyrek": (b_.month - 1) // 3 + 1, "ann": pd.Timestamp(ann), "t_gun": gun[t] if takvimde else pd.NaT,
                        "karar": gun[t + 1] if (takvimde and t + 1 < G) else pd.NaT, "karar_i": t + 1, "SUETF": su, "EAR": ear, "kirli": False})
    say["portfoy_gun"] = int((Pid >= 0).any(axis=1).sum()); say["be_satir"] = int(len(I["Dk"]["mali"]))
    return pd.DataFrame(sat, columns=_K62B_DUYURU_KOL), say


def k62b_abd_portfoy_girdi(Dz: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """ABD 2x3 portföy girdisi ve çeyrek sonu piyasa değeri: ME (seçilmiş işlem günleri x hisse; kapanış x o gün bilinen pay), sat_ix (gün konumu -> ME satırı), pb /
    pb_ok (her çeyreğin MV günü konumu ve geçerliliği), Dk (K62.k62_hazirla / k62_portfoy_ata demeti: takvim, kod, C = düzeltilmiş kapanış, PD = yalnız Haziran ve
    Aralık son işlem günlerinde ME, mali = defter değeri satırları (yil = mali yıl sonunun takvim yılı, ceyrek 4; bilgi tarihi sonraki Haziran sonundan önce))."""
    E = E or K62B_ESIK; Sp = E["surpriz"]; gun = Dz["gun"]; gD = gun.to_numpy("datetime64[D]"); G = len(gD); S = list(Dz["kod"]); N = len(S)
    T = Dz["T"]; Bg = K60.K60_ESIK["bilgi"]; bit = np.asarray(T["bit"], "datetime64[D]")
    with np.errstate(invalid="ignore"):
        pb = np.searchsorted(gD, bit, side="right") - 1
        pb_ok = (~np.isnat(bit)) & (pb >= 0) & (gD[np.maximum(pb, 0)] > bit - np.timedelta64(int(Sp["abd_mv_gun"]), "D"))
    yillar = range(gun[0].year, gun[-1].year + 1)
    yp = {}
    for Y in yillar:
        for ad, gun_ in (("J", f"{Y}-06-30"), ("D", f"{Y}-12-31")):
            p = int(np.searchsorted(gD, np.datetime64(gun_, "D"), side="right")) - 1
            if p >= 0 and gun[p].year == Y:
                yp[(Y, ad)] = p
    uniq = np.unique(np.r_[pb[pb_ok], np.array(list(yp.values()), int)]).astype(int)
    mtD = gD[uniq]; sat_ix = {int(p): i for i, p in enumerate(uniq)}
    AO = K60._K60Temel(T, mtD, N, Bg)
    SH, _kay = K60.k60_pay({"temel": T, "bolunme": Dz.get("bolunme") or {}}, {"U": np.zeros((len(mtD), N), bool), "mtD": mtD, "sembol": S}, AO, K60.K60_ESIK)
    Cf = _k62b_ffill(Dz["C"], int(Sp["ileri_tasima"]))
    with np.errstate(invalid="ignore"):
        ME = np.where(np.isfinite(SH) & (SH > 0), Cf[uniq] * SH, np.nan)
    PDs = np.full((G, N), np.nan)
    for p in yp.values():
        PDs[p] = ME[sat_ix[p]]
    be = []
    Yq, Ybit, Ybilgi = T["Yq"], np.asarray(T["Ybit"], "datetime64[D]"), np.asarray(T["Ybilgi"], "datetime64[D]"); EQ = T["I"].get("StockholdersEquity")
    for y in range(Ybit.shape[0]):
        for j in range(N):
            if EQ is None or np.isnat(Ybit[y, j]) or Yq[y, j] < 0:
                continue
            Yc = int(str(Ybit[y, j])[:4]); haz = np.datetime64(f"{Yc + 1}-06-30", "D")
            v = EQ[int(Yq[y, j]), j]
            if np.isfinite(v) and not np.isnat(Ybilgi[y, j]) and Ybilgi[y, j] < haz:
                be.append({"kod": S[j], "yil": Yc, "ceyrek": 4, "kar_bir": np.nan, "ozkaynak": float(v), "grup": "SEC", "_s": str(Ybit[y, j])})
    M = pd.DataFrame(be, columns=["kod", "yil", "ceyrek", "kar_bir", "ozkaynak", "grup", "_s"])
    M = M.sort_values("_s").drop_duplicates(["kod", "yil"], keep="last").drop(columns="_s").reset_index(drop=True)
    Dk = {"takvim": gun, "kod": S, "C": Dz["A"], "PD": PDs, "mali": M, "X": np.ones(G)}
    return {"Dk": Dk, "ME": ME, "sat_ix": sat_ix, "pb": pb, "pb_ok": pb_ok, "SH": SH, "uniq": uniq}


def k62b_surpriz_sinif(U: pd.DataFrame, pazar: str, E62: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Her açıklamanın SUETF ve EAR sınıfı K62 C kuralıyla (K62.k62_tertil_onsel: önceki çeyreğin karar günü bilinen 1/3 - 2/3 kesimleri; geleceğe bakmaz;
    BIST SUETF'te TMS 29 kirli çeyrekler havuz olamaz). CS = ikisi de üst üçte bir (2). Karar günü olmayan açıklama sınıfsız (-1)."""
    E62 = E62 or K62.K62_ESIK; U = U.copy(); U["s_SUETF"] = -1; U["s_EAR"] = -1
    m = U.karar.notna().to_numpy()
    if m.any():
        X = U[m].reset_index(drop=True)
        haric = E62["bolum_b"]["tms29_haric"] if pazar == "BIST" else None
        U.loc[m, "s_SUETF"] = K62.k62_tertil_onsel(X, "SUETF", E62, haric); U.loc[m, "s_EAR"] = K62.k62_tertil_onsel(X, "EAR", E62, None)
    U["cs"] = (U.s_SUETF == 2) & (U.s_EAR == 2); U["cs_var"] = (U.s_SUETF >= 0) & (U.s_EAR >= 0)
    return U


# ---------------------------------------------------------------- 2) ÇÖL GÜNÜ BİLİNEN SON AÇIKLAMA (gün x hisse; yalnız t'den önce karar günü)
def k62b_son_indeks(U: pd.DataFrame, takvim: pd.DatetimeIndex, semboller: List[str]) -> np.ndarray:
    """L[g, j] = hisse j için karar günü < takvim[g] olan EN SON açıklamanın U'daki satır numarası (yoksa -1). Aynı karar gününde birden çok açıklama varsa
    dönemi en geç olan. Açıklama günü (ann) ya da değer gelecekte bozulsa L değişmez: yalnız karar < t olan satırlar okunur."""
    G, N = len(takvim), len(semboller); L = np.full((G, N), -1, np.int64); tv = takvim.to_numpy("datetime64[ns]"); kol = {s: j for j, s in enumerate(semboller)}
    if not len(U):
        return L
    X = U[U.karar.notna()].assign(_r=lambda d: d.index.to_numpy()).sort_values(["sembol", "karar", "yil", "ceyrek"], kind="stable")
    for s, g in X.groupby("sembol", sort=False):
        j = kol.get(s)
        if j is None:
            continue
        kd = pd.DatetimeIndex(g.karar).to_numpy("datetime64[ns]"); i = np.searchsorted(kd, tv, side="left") - 1
        L[:, j] = np.where(i >= 0, g._r.to_numpy()[np.maximum(i, 0)], -1)
    return L


def k62b_degiskenler(U: pd.DataFrame, L: np.ndarray, takvim: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """Gün x hisse: SUETF_C, EAR_C (son açıklama 90 gün içinde ise değeri; değilse NaN), YAS (son açıklamadan bu yana takvim günü; açıklama yoksa NaN), CS / CS_VAR
    (son açıklama 90 gün içinde ve sınıfı), KIRLI (son açıklama 90 gün içinde ve TMS 29 kirli çeyrek)."""
    E = E or K62B_ESIK; P = int(E["surpriz"]["pencere_gun"]); G, N = L.shape; ok = L >= 0; li = np.maximum(L, 0)
    yas = np.full((G, N), np.nan); out: Dict[str, np.ndarray] = {}
    if len(U):
        ann = pd.DatetimeIndex(U.ann).to_numpy("datetime64[D]"); tD = takvim.to_numpy("datetime64[D]")[:, None]
        fark = (tD - ann[li]).astype("timedelta64[D]").astype(float); yas[ok] = fark[ok]
    taze = ok & np.isfinite(yas) & (yas >= 0) & (yas <= P)
    out["YAS"] = yas; out["TAZE"] = taze
    for k, kol in (("SUETF_C", "SUETF"), ("EAR_C", "EAR")):
        v = U[kol].to_numpy(float) if len(U) else None
        out[k] = (np.where(taze, v[li], np.nan) if v is not None else np.full((G, N), np.nan)).astype(np.float32)
    for k, kol in (("CS", "cs"), ("CS_VAR", "cs_var"), ("KIRLI", "kirli")):
        v = U[kol].to_numpy(bool) if (len(U) and kol in U) else None
        out[k] = taze & v[li] if v is not None else np.zeros((G, N), bool)
    return out


def k62b_pazar_hazirla(g: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """K64.k64_olay_degerleri / k64_s1 / k64_s2'nin beklediği H demeti (takvim, sembol, kol, X, sira, var, rejim) + bilgi matrisleri. Getiri HESAPLANMAZ."""
    E = E or K62B_ESIK; V = g["V"]; M = K64.k64_fiyat_matrisleri(V, K64.K64_ESIK); tak = M["takvim"]; S = M["sembol"]
    U = g["duyuru"].reset_index(drop=True); L = k62b_son_indeks(U, tak, S); Z = k62b_degiskenler(U, L, tak, E)
    X = {k: Z[k] for k in k62b_kodlar(E)}
    sira = {k: K64.k64_sira(v, M["var"], E["sira"]["min_evren"]) for k, v in X.items()}
    return {"takvim": tak, "sembol": S, "kol": {s: j for j, s in enumerate(S)}, "X": X, "sira": sira, "var": M["var"], "rejim": K64.k64_rejim(M["C"], E),
            "L": L, "Z": Z, "duyuru": U}


def k62b_olay_bilgi(X: pd.DataFrame, H: Dict[str, Any]) -> pd.DataFrame:
    """Olay tablosuna (sinyal günü t) son açıklama bilgileri: son_ann, son_donem, yas, yok90 (karar < t olan açıklama yok ya da > 90 gün önce), hic (hiç yok),
    kirli, cs, cs_var. Yalnız t'deki matrislerden okunur."""
    X = X.copy(); n = len(X)
    it = H["takvim"].get_indexer(pd.DatetimeIndex(X.sinyal)) if n else np.array([], int); jj = np.array([H["kol"].get(s, -1) for s in X.sembol], int) if n else np.array([], int)
    ok = (it >= 0) & (jj >= 0); a, b = np.maximum(it, 0), np.maximum(jj, 0); L = H["L"]; U = H["duyuru"]; Z = H["Z"]
    l = np.where(ok, L[a, b], -1) if n else np.array([], int); li = np.maximum(l, 0)
    X["son_ann"] = pd.DatetimeIndex(U.ann.to_numpy()[li]).where(l >= 0) if n and len(U) else pd.NaT
    X["son_donem"] = [f"{int(U.yil.iat[i])}Q{int(U.ceyrek.iat[i])}" if i >= 0 else "" for i in l] if n and len(U) else ""
    X["yas"] = np.where(ok, Z["YAS"][a, b], np.nan) if n else []
    X["hic"] = (l < 0) if n else []
    X["yok90"] = ~(np.where(ok, Z["TAZE"][a, b], False)) if n else []
    for k, z in (("kirli", "KIRLI"), ("cs", "CS"), ("cs_var", "CS_VAR")):
        X[k] = np.where(ok, Z[z][a, b], False) if n else []
    return X


# ---------------------------------------------------------------- 3) GİRDİ, OLAYLAR, KAPSAM
def k62b_girdi(E: Optional[Dict[str, Any]] = None, k60_veri: Optional[Dict[str, Tuple[str, int]]] = None, k62_veri: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """GERÇEK girdi (yalnız önbellek; ağ yok): pazar -> {V, duyuru, ozet}."""
    E = E or K62B_ESIK; out: Dict[str, Dict[str, Any]] = {}; t0 = time.time()
    Vb = K64.k64_fiyat_yukle("BIST", K62B_YOL["veri"], K64.K64_ESIK); D62 = K62.k62_demet_kur(k62_veri); Ub = k62b_surpriz_sinif(k62b_bist_duyuru(D62), "BIST")
    out["BIST"] = {"V": Vb, "duyuru": Ub, "ozet": {"hisse": len(Vb), "k62_hisse": len(D62["kod"]), "v_k62_ortak": len(set(Vb) & set(D62["kod"])), "aciklama": int(len(Ub))}}
    k62blog.info("BIST açıklama tablosu: %d (%.0f sn)", len(Ub), time.time() - t0); del D62
    Va = K64.k64_fiyat_yukle("ABD", K62B_YOL["veri"], K64.K64_ESIK); D60 = K60.k60_demet_yukle(k60_veri); Dz = k62b_abd_demet(sorted(Va), D60); del D60
    Ua, oz = k62b_abd_duyuru(Dz, E); Ua = k62b_surpriz_sinif(Ua, "ABD")
    out["ABD"] = {"V": Va, "duyuru": Ua, "ozet": {"hisse": len(Va), "demette": int(Dz["var"].sum()), "aciklama": int(len(Ua)), **oz}}
    k62blog.info("ABD açıklama tablosu: %d (%.0f sn)", len(Ua), time.time() - t0)
    return out


def _k62b_olaylar(pazar: str, V: Dict[str, pd.DataFrame], E: Dict[str, Any], sentetik: bool) -> Dict[str, pd.DataFrame]:
    """ANA (K24) ve İKİNCİL (D13) olaylar K64 fonksiyonlarıyla (tanımlar aynen). Gerçek veride D13 olay ayarları K64 ile aynıysa K64'ün ara önbelleği okunur."""
    out = {"K24": K64.k64_olay_k24(V, E)}
    if E["olay"]["d13"]["etkin"]:
        ara = None
        if not sentetik and E["olay"] == K64.K64_ESIK["olay"] and E["kriz"] == K64.K64_ESIK["kriz"] and K62B_YOL["veri"] == K64.K64_YOL["veri"]:
            ara = K64._k64_d13_ara(pazar)
        out["D13"] = K64.k64_olay_d13(V, E, None, ara)
    return out


def _k62b_olay_tablosu(X0: pd.DataFrame, H: Dict[str, Any], tanim: str, E: Dict[str, Any]) -> pd.DataFrame:
    X = K64.k64_olay_degerleri(X0, H, tanim, E)
    return k62b_olay_bilgi(X, H)


def k62b_sira_sec(K: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, str], List[Dict[str, Any]]]:
    """KARAR SIRASI SEÇİM KURALI (ölçümden önce, yalnız kapsam sayısıyla; eşikler kapsam koşulmadan yazıldı). Değişken başına: ANA tanım, iki pazar, iki bağımsız
    dönem; EVREN sırasıyla ÜST ve ALT pencereli olay sayıları. Bir hücrede küçük grup < n_min YA DA küçük / büyük < oran_min ise çöl olayları evren sırasında bir
    uçta TOPLANIYOR sayılır; değişkenin herhangi bir hücresinde toplanma varsa karar sırası 'IC' (çöl içi), yoksa 'EVREN'. Döner ({değişken: seçim}, hücreler)."""
    E = E or K62B_ESIK; R = E["sira_secim"]; sat = []; sec: Dict[str, str] = {}
    A = K[(K.tanim == E["olay"]["ana"]) & (K.degisken.isin(k62b_kodlar(E))) & K.donem.isin(E["bagimsiz"])]
    for r in A.itertuples():
        u, a = int(r.n_ust), int(r.n_alt); kucuk, buyuk = min(u, a), max(u, a)
        top = bool(buyuk == 0 or kucuk < R["n_min"] or kucuk / buyuk < R["oran_min"])
        sat.append({"degisken": r.degisken, "pazar": r.pazar, "donem": r.donem, "n_ust": u, "n_alt": a, "oran": (kucuk / buyuk) if buyuk else float("nan"), "toplanma": top})
    for k in k62b_kodlar(E):
        h = [s for s in sat if s["degisken"] == k]
        if not h:
            raise K62BHata(f"karar sırası seçimi için {k} kapsam satırı yok")
        sec[k] = "IC" if any(s["toplanma"] for s in h) else "EVREN"
    return sec, sat


def k62b_kapsam(cikti: Optional[str] = None, girdi: Optional[Dict[str, Dict[str, Any]]] = None, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """KAPSAM: yalnız SAYIM. Pazar x tanım x dönem: olay sayısı (ham / tekil / pencereli), son 90 günde açıklaması olan / olmayan / hiç olmayan, TMS 29 kirli,
    ÇÖL + SÜRPRİZ, değişken kapsamı ve ÜST / ORTA / ALT sayıları (evren içi ve çöl içi sıra). Getiri, eşli fark, CAR, FI_OLCUT paneli HESAPLANMAZ."""
    E = E or K62B_ESIK; sentetik = girdi is not None; t0 = time.time()
    girdi = girdi if sentetik else k62b_girdi(E, K60.k60_veri_sha(dogrula=False))
    sat = []; ozet: Dict[str, Any] = {"zaman": _k62b_simdi(), "surum": K62B_SURUM, "muhur": k62b_esik_sha(E), "pazar": {}}
    for pazar in E["pazar"]:
        if pazar not in girdi:
            continue
        g = girdi[pazar]; V = g["V"]; H = k62b_pazar_hazirla(g, E); tak = H["takvim"]; son = len(tak) - 1; O = _k62b_olaylar(pazar, V, E, sentetik); U = H["duyuru"]
        ozet["pazar"][pazar] = {**g.get("ozet", {}), "takvim_gun": len(tak), "ilk_gun": str(tak[0].date()), "son_gun": str(tak[-1].date()), "k24_sapma": int(O["K24"].attrs.get("sapma", 0)),
                                "aciklama_SUETF": int(U.SUETF.notna().sum()), "aciklama_EAR": int(U.EAR.notna().sum()), "aciklama_kirli": int(U.kirli.sum()),
                                "aciklama_ilk": str(pd.DatetimeIndex(U.ann).min().date()) if len(U) else None, "aciklama_son": str(pd.DatetimeIndex(U.ann).max().date()) if len(U) else None,
                                "evren_kapsam": {k: float(np.isfinite(np.where(H["var"], H["X"][k], np.nan)).sum() / max(int(H["var"].sum()), 1)) for k in k62b_kodlar(E)}}
        for tanim, X0 in O.items():
            X = _k62b_olay_tablosu(X0, H, tanim, E); gi = tak.get_indexer(pd.DatetimeIndex(X.giris)) if len(X) else np.array([], int)
            X["pencere"] = (gi >= 0) & (gi + FI.FI_OLCUT["ufuk"] - 1 <= son) if len(X) else []
            if tanim == "D13" and E["olay"]["d13"]["gecer"] and len(X):
                X = X[X.gecer].reset_index(drop=True)
            for dn, a, b in E["donem"]:
                md = ((X.giris >= a) & (X.giris <= b)).to_numpy() if len(X) else np.zeros(0, bool); tk = md & X.tekil.to_numpy(bool) if len(X) else md
                pn = tk & X.pencere.to_numpy(bool) if len(X) else md
                f = (lambda k: int((pn & X[k].to_numpy(bool)).sum()) if len(X) else 0)  # noqa: E731
                kim = {"tanim": tanim, "pazar": pazar, "donem": dn, "n_ham": int(md.sum()), "n_tekil": int(tk.sum()), "n_pencere": int(pn.sum())}
                sat.append({**kim, "degisken": "(olay)", "n_son90": int(pn.sum()) - f("yok90"), "n_yok90": f("yok90"), "n_hic": f("hic"), "n_kirli": f("kirli"),
                            "n_cs": f("cs"), "n_cs_var": f("cs_var")})
                for k in k62b_kodlar(E):
                    ge = K64.k64_grup(X[k + "_sira"].to_numpy(float), E) if len(X) else np.array([], str); gc = K64.k64_grup(X[k + "_ic"].to_numpy(float), E) if len(X) else ge
                    sat.append({**kim, "degisken": k, "n_deger": int((pn & np.isfinite(X[k].to_numpy(float))).sum()) if len(X) else 0,
                                "n_ust": int((pn & (ge == "UST")).sum()), "n_orta": int((pn & (ge == "ORTA")).sum()), "n_alt": int((pn & (ge == "ALT")).sum()),
                                "n_ust_ic": int((pn & (gc == "UST")).sum()), "n_orta_ic": int((pn & (gc == "ORTA")).sum()), "n_alt_ic": int((pn & (gc == "ALT")).sum())})
        k62blog.info("kapsam %s: %d hisse, %d gün, %d açıklama (%.0f sn)", pazar, len(H["sembol"]), len(tak), len(U), time.time() - t0)
    K = pd.DataFrame(sat); cik = cikti or K62B_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    try:
        sec, hucre = k62b_sira_sec(K, E); ozet["sira_secim"] = {"secim": sec, "hucre": hucre, "kural": E["sira_secim"]}
    except K62BHata as ex:
        ozet["sira_secim"] = {"secim": None, "neden": str(ex)}
    K.to_csv(_k62b_yol("kapsam", cikti), index=False); K60._k60_json_yaz(_k62b_yol("kapsam_ozet", cikti), K60._k60_yuvarla(ozet, 10))
    return K


def k62b_kapsam_notu(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """Kapsam sayımının ön kayıt metnine giren özeti (yalnız SAYI). Mühre girmez."""
    E = E or K62B_ESIK; yk, yo = _k62b_yol("kapsam", cikti), _k62b_yol("kapsam_ozet", cikti)
    if not (os.path.exists(yk) and os.path.exists(yo)):
        return "Kapsam sayımı henüz koşulmadı (`python -I K62B.py kapsam`)."
    K = pd.read_csv(yk); O = K60._k60_json_oku(yo)
    par = [f"Kapsam sayımı ({O.get('zaman', '?')}; `python -I K62B.py kapsam`; yalnız SAYI: getiri, eşli fark, CAR, FI_OLCUT paneli hesaplanmadı).\n"]
    for p, v in O.get("pazar", {}).items():
        ek = ", ".join(f"{k} %{100 * float(x):.0f}" for k, x in (v.get("evren_kapsam") or {}).items())
        par.append(f"- {p}: {v.get('hisse')} hisse, takvim {v.get('takvim_gun')} gün ({v.get('ilk_gun')} .. {v.get('son_gun')}); açıklama tablosu {v.get('aciklama')} "
                   f"({v.get('aciklama_ilk')} .. {v.get('aciklama_son')}); SUETF'i olan {v.get('aciklama_SUETF')}, EAR'ı olan {v.get('aciklama_EAR')}, TMS 29 kirli {v.get('aciklama_kirli')}"
                   + (f"; K62 verisinde de olan hisse {v.get('v_k62_ortak')}" if v.get("v_k62_ortak") is not None else "")
                   + (f"; K60 demetinde {v.get('demette')}; gerçek başvuru günlü çeyrek {v.get('gercek_gun')}, yedek kural günlü (açıklama sayılmayan) {v.get('yedek_gun')}; 2x3 portföylü "
                      f"gün {v.get('portfoy_gun')}" if v.get("demette") is not None else "")
                   + f". Evren hisse-günlerinde değişken doluluk: {ek}.")
    for tanim in K.tanim.unique():
        par.append(f"\n**{tanim} olayları** (ham / tekil / pencere = 60 günlük penceresi 31.08.2026'dan önce biten tekil olay; son 90 gün = pencereli olaylardan karar günü t'den önce, "
                   "açıklaması t'den en çok 90 gün önce olan; hiç = t'den önce hiç açıklaması olmayan"
                   + ("; D13'te yalnız GECER" if tanim == "D13" else "") + ")\n\n| pazar | dönem | ham | tekil | pencere | son 90 gün | yok (90 gün) | hiç | TMS 29 kirli | ÇÖL+SÜRPRİZ / sınıflı |\n"
                   "|---|---|---|---|---|---|---|---|---|---|")
        for r in K[(K.tanim == tanim) & (K.degisken == "(olay)")].itertuples():
            pay = 100 * r.n_son90 / r.n_pencere if r.n_pencere else float("nan")
            par.append(f"| {r.pazar} | {r.donem} | {int(r.n_ham)} | {int(r.n_tekil)} | {int(r.n_pencere)} | {int(r.n_son90)} (%{pay:.0f}) | {int(r.n_yok90)} | {int(r.n_hic)} | "
                       f"{int(r.n_kirli)} | {int(r.n_cs)} / {int(r.n_cs_var)} |")
        par.append(f"\n**{tanim}: değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; EVREN = aynı gün evren içi sıra, İÇ = çöl içi sıra; hücre = değer / ÜST / ALT)\n\n"
                   "| değişken | sıra | " + " | ".join(f"{p} {d[0]}" for p in E["pazar"] for d in E["donem"]) + " |\n|---|---|" + "---|" * (len(E["pazar"]) * len(E["donem"])))
        for k in k62b_kodlar(E):
            for st, u, al in (("EVREN", "n_ust", "n_alt"), ("İÇ", "n_ust_ic", "n_alt_ic")):
                h = []
                for p in E["pazar"]:
                    for d in E["donem"]:
                        x = K[(K.tanim == tanim) & (K.pazar == p) & (K.donem == d[0]) & (K.degisken == k)]
                        h.append("—" if not len(x) else f"{int(x.n_deger.iloc[0])} / {int(x[u].iloc[0])} / {int(x[al].iloc[0])}")
                par.append(f"| {k} | {st} | " + " | ".join(h) + " |")
    sec = (O.get("sira_secim") or {})
    if sec.get("hucre"):
        par.append("\n**Karar sırası seçim kuralı uygulaması** (ANA tanım, iki pazar, bağımsız dönemler, EVREN sırası; toplanma = küçük grup < "
                   f"{E['sira_secim']['n_min']} ya da küçük / büyük < {E['sira_secim']['oran_min']}): "
                   + "; ".join(f"{h['degisken']} {h['pazar']} {h['donem']} ÜST {h['n_ust']} / ALT {h['n_alt']} (oran {float(h['oran']):.2f}{', TOPLANMA' if h['toplanma'] else ''})"
                               for h in sec["hucre"])
                   + ". Kuralın sonucu: " + ", ".join(f"**{k}: {'İÇ' if v == 'IC' else 'EVREN'}**" for k, v in (sec.get("secim") or {}).items()) + ".")
    kr = E["sira"]["karar"]
    if all(v in ("IC", "EVREN") for v in kr.values()):
        A = K[(K.tanim == E["olay"]["ana"]) & (K.degisken.isin(k62b_kodlar(E))) & K.donem.isin(E["bagimsiz"])]
        az = []
        for r in A.itertuples():
            ic = kr[r.degisken] == "IC"; u, a = int(r.n_ust_ic if ic else r.n_ust), int(r.n_alt_ic if ic else r.n_alt)
            if min(u, a) < E["s1"]["n_esik"]:
                az.append(f"{r.degisken} {r.pazar} {r.donem} ({'İÇ' if ic else 'EVREN'}: ÜST {u}, ALT {a})")
        par.append(f"\nANA tanım, KARAR sırası, bağımsız dönemlerde grubu n < {E['s1']['n_esik']} olan (karar kuralında 'ÖLÇÜLEMEZ' kalacak) hücreler (pencereli olay sayısıyla; "
                   "ölçülebilen olay daha az olabilir): " + ("; ".join(az) if az else "yok") + ".")
    return "\n".join(par)


# ---------------------------------------------------------------- 4) ÖN KAYIT
def k62b_veri_sha(k62_veri: Optional[str] = None) -> Dict[str, Tuple[str, int]]:
    """Koşunun okuyacağı verinin ve içe alınan kodun / tasarımın sha256'ları: ad -> (sha256, dosya sayısı). Eksik dosyada durur. K60 önbellekleri K60 ön kaydıyla
    doğrulanır (`kos` başında K60.k60_onkayit_dogrula veri=True)."""
    sha = K60._k60_sha; out: Dict[str, Tuple[str, int]] = {}
    for p in ("BIST", "ABD"):
        y = os.path.join(K62B_YOL["veri"], f"V_{p}.pkl")
        if not os.path.exists(y):
            raise K62BHata(f"fiyat verisi yok: {y}")
        out[f"V_{p}.pkl"] = (sha(y), 1)
    v = K62.k62_veri_sha(k62_veri)
    if not v.get("fiyat_dosya") or not v.get("kap_dosya") or not v.get("mali_dosya"):
        raise K62BHata(f"K62 veri önbelleği eksik: {v}")
    out["k62_veri"] = (v["sha256"], int(v["kap_dosya"] + v["fiyat_dosya"] + v["mali_dosya"]))
    for ad, yol in (("K60_ON_KAYIT.md", K60._k60_yol("onkayit")), ("K64_K65_ON_KAYIT.md", K64._k64_yol("onkayit")), ("K62_ON_KAYIT.md", K62._k62_yol("onkayit"))):
        if not os.path.exists(yol):
            raise K62BHata(f"içe alınan ön kayıt yok: {yol}")
        out[ad] = (sha(yol), 1)
    for a in ("FON_IZI.py", "K60.py", "K59.py", "COL_v1.py", "K64.py", "K62.py"):
        y = os.path.join(KOK_K62B, a)
        if not os.path.exists(y):
            raise K62BHata(f"içe alınan kod dosyası yok: {y}")
        out[a] = (sha(y), 1)
    return out


def k62b_onkayit_metin(zaman: str, veri_sha: Dict[str, Tuple[str, int]], kapsam: str, E: Optional[Dict[str, Any]] = None) -> str:
    E = E or K62B_ESIK; O = E["olay"]; S = E["sira"]; S1 = E["s1"]; Sp = E["surpriz"]; FO = FI.FI_OLCUT; K24 = FI.FI_K24; RS = E["sira_secim"]; E62 = K62.K62_ESIK
    kr = S["karar"]; ad = {"IC": "İÇ (çöl içi sıra)", "EVREN": "EVREN (aynı gün evren içi sıra)"}
    vs = "\n".join(f"- {k}: sha256 {v[0]} ({v[1]} dosya)" for k, v in veri_sha.items()) or "- (veri dosyası bulunamadı)"
    dg = "\n".join(f"| {d['kod']} | {d['tanim']} | {d['kaynak']} |" for d in E["degisken"])
    dn = ", ".join(f"{a} ({b} .. {c})" for a, b, c in E["donem"]); m = len(E["degisken"]) * 2 * len(E["pazar"]) * len(E["bagimsiz"])
    kirli = ", ".join(f"{a}Ç{b}" for a, b in E62["bolum_b"]["tms29_haric"])
    return f"""# K62-B — BİLANÇO SÜRPRİZİ ÇÖL SİNYALİNE EK BİLGİ TAŞIYOR MU: ÖN KAYIT (ölçümden ÖNCE)

{K62B_SURUM}
Yazım zamanı: {zaman}
ESIK_SHA256: {k62b_esik_sha(E)}

Bu dosya gerçek veride değişkene bağlı HİÇBİR getiri / eşli fark / CAR hesaplanmadan yazıldı (yalnız `kapsam` sayımı koşuldu: §12). `python -I K62B.py kos`
bu dosya git'e işlenmeden, mühür ya da veri sha256'ları tutmadan çalışmaz. Sonuç görüldükten sonra yeni kural eklenmez. Tasarım K64_K65_ON_KAYIT.md ile aynıdır
(K64.py fonksiyonları içe alınır, kopyalanmaz; K64.py değişmez); değişken tanımları K62'den (K62_ON_KAYIT.md; K62.py fonksiyonları içe alınır, K62.py değişmez).
K64 SONUÇ dosyaları (K64_K65_RAPOR.md, k64_s1*.csv, k64_karar.csv) bu iş tasarlanırken OKUNMADI.

## Veri (sha256; `kos` başında yeniden hesaplanır, farklıysa koşu durur)
{vs}
K60 önbellekleri (/tmp/k60_fiyat, /tmp/k60_secframes ...; ABD temel tablosu, pay, bölünme) K60 ön kaydındaki sha256'larla doğrulanır (K60.k60_onkayit_dogrula, veri = True).
K64, K62 ve K60 mühürleri bu işin mührüne girer.

## 0. Soru (Cemal'in ana sorusu)
Bilanço sürprizi ÇÖL sinyaline ek bilgi taşıyor mu? Çöl tanımı ve cetvel DEĞİŞMEZ. Değişkenler K62'nin (Ahlatcıoğlu & Okay 2021 birebir tekrarı) iki sürpriz ölçüsüdür,
çöl sinyal günü t'de BİLİNEN son açıklamaya göre. Her değişken İKİ YÖNDE sınanır; katkı değişkensiz temel modele (yalnız çöl) karşı ölçülür. Üretim koduna ekleme yapılmaz.

## 1. Olay (K64_K65_ON_KAYIT.md §1 AYNEN; K64.k64_olay_k24 / k64_olay_d13 çağrılır)
- ANA: K24 'iki evre' çöl sinyali — FON_IZI.fi_k24_tara, FI_K24 = {json.dumps(K24, ensure_ascii=False)}. Sinyal günü t; giriş = hissenin t'den sonraki ilk işlem
  günü açılışı. TEKİLLEŞTİRME: son TUTULAN sinyalden en az {O['tekil_gun']} işlem günü sonra gelen ilk sinyal (FI_K24 'tekrar' = 60 ile birebir).
- İKİNCİL (sağlamlık; BH ailesine ve karara GİRMEZ): üretim D13 + AL kırılımı (K64 §1 (ii) aynen; gerçek veride K64'ün ara önbelleği).
- Evren: V_BIST.pkl (581) ve V_ABD.pkl (1.411) (islenmis-veri dalı; K24 cetvelinin evrenleri). Fon krizi: {E['kriz']} sonrası barlar atılır; penceresi aşan olay ölçülmez.

## 2. Açıklama, değer ve BİLGİ TARİHİ
- BIST açıklamaları: K62 verisi (KAP 'Finansal Rapor' bildirim sınıfı FR, 2009-06 -> 2026-08; her hisse-mali yıl-çeyreğin İLK yayını; İş Yatırım fiyat / piyasa
  değeri / mali tablo, kotasyondan çıkanlar dahil). SUETF ve EAR K62.k62_olay_tablosu ile BİREBİR aynı formülle (testte denetlenir). TMS 29 KİRLİ çeyrekler
  ({kirli}; K62 SAPMA 9 / B3): o açıklamanın SUETF'i YOK (EAR'ı var).
- ABD açıklamaları: K60 demeti (SEC XBRL frames + EDGAR başvuru dizini), V_ABD sembolleri. Açıklama günü = K60 BİLGİ TARİHİ: çeyrek sonundan en az 15 gün sonraki
  ilk 10-Q / 10-K başvurusunun günü; yalnız GERÇEK başvuru günü olan çeyrekler (bilgi_kaynak {Sp['abd_bilgi_kaynak']}); yedek kural günü (çeyrek sonu + 90 / 120)
  açıklama günü değildir, o çeyrek açıklama sayılmaz. **SAPMA**: şirketlerin çoğu bilançoyu basın bülteniyle (8-K) 10-Q / 10-K'dan GÜNLER önce açıklar; burada
  açıklama günü başvuru günüdür (EAR penceresi asıl tepkiyi kaçırabilir; SUETF'in bilinme günü tutucudur).
- ta = açıklama gününe eşit ya da sonraki ilk işlem günü (açıklama saati kullanılmaz); KARAR GÜNÜ = ta + {Sp['karar_gecikme_islem']} işlem günü (EAR o günün kapanışında bilinir).
- **KURAL**: t günü bir hissenin değeri, karar günü < t olan EN SON açıklamanın değeridir; ancak o açıklamanın günü t'den en çok {Sp['pencere_gun']} takvim günü önceyse.
  Değilse (ya da hiç açıklama yoksa) değer YOK ve olay 'son 90 günde açıklama yok' sınıfındadır (bilgi). Son açıklamanın değeri yoksa (veri eksik / TMS 29 kirli)
  daha eskiye GİDİLMEZ: değer YOK. Aynı karar gününde birden çok açıklama varsa dönemi en geç olan.

## 3. Değişkenler
| kod | tanım | kaynak |
|---|---|---|
{dg}

- SUETF ayrıntısı: BIST E = İş Yatırım net dönem kârı ana ortaklık payı (birikimli farkı), MV_q = çeyrek son işlem günü PD (İş Yatırım); ABD E = SEC NetIncomeLoss
  çeyreklik (K60 temel tablosu; türetilmiş 4. çeyrek dahil), E_(q-4) aynı tablonun dört çeyrek önceki değeri, MV_q = çeyrek sonuna eşit ya da önceki son işlem günü
  (en çok {Sp['abd_mv_gun']} gün geride) bölünme düzeltmeli kapanış (5 güne kadar ileri taşıma) x o gün bilinen pay (K60.k60_pay; bugünkü birim).
- EAR ayrıntısı: BIST K62 aynen (2x3 portföy: Haziran sonu PD 2 kova x önceki yıl sonu özkaynak / Aralık PD 3 kova; günlük eşit ağırlık; portföyde günlük getirisi
  olan en az 5 hisse; [ta-1, ta+1] getirilerinin en az 2/3'ü). ABD: aynı K62.k62_portfoy_ata / k62_hazirla kuralı; PD = kapanış x pay (Haziran ve Aralık son işlem
  günü); defter değeri = takvim yılı Y-1'de biten mali yılın SEC özkaynağı, BİLGİ TARİHİ Y Haziran sonundan önce (aksi portföy dışı); evren = V_ABD sembolleri
  (K60 demetindeki fiyatla); günlük getiri = düzeltilmiş kapanış (temettü dahil). Bu yüzden ABD'de 'eşit ağırlıklı evren' yedeğine gerek kalmadı.
- ÇÖL + SÜRPRİZ (bilgi; karara girmez): son açıklamanın SUETF ve EAR sınıfı K62 C kuralıyla (K62.k62_tertil_onsel; önceki çeyreğin karar günü bilinen
  1/3 - 2/3 kesimleri, pazarın bütün açıklamaları; BIST SUETF'te kirli çeyrek havuz olamaz); ikisi de üst üçte bir = CS. Bilgi grupları: CS, CS_DEGIL (ikisi de
  sınıflı ama CS değil), YOK90 (son 90 günde açıklama yok). Her biri FI_OLCUT ölçüleriyle raporlanır.

## 4. S1 — 'ek katkı' (K64 §4 aynen; K64.k64_s1)
- Örneklem: yalnız ÇÖL OLAYLARI (tekil; FI_OLCUT ile ölçülebilen). Değeri olmayan olay ÜST / ALT gruplarına girmez (TEMEL'de kalır).
- EVREN sırası: aynı gün o pazarda işlem gören ve değeri olan hisseler içinde (küçük + 0,5 x eşit) / n (n >= {S['min_evren']}); İÇ sırası: [t - {S['ic_gun']} gün, t] aralığındaki
  aynı pazar ve tanımın tekil çöl olayları içinde (n >= {S['ic_min']}). ÜST >= 2/3, ALT <= 1/3.
- **KARAR SIRASI** (değişken başına; mekanik kural, eşikleri kapsam koşulmadan yazıldı: ANA tanım, iki pazar, iki bağımsız dönem, EVREN sırasıyla ÜST ve ALT pencereli
  olay sayısı; bir hücrede küçük grup < {RS['n_min']} ya da küçük / büyük < {RS['oran_min']} ise 'toplanma'; herhangi bir hücrede toplanma -> İÇ, yoksa EVREN):
  SUETF_C = **{ad.get(kr['SUETF_C'], kr['SUETF_C'])}**, EAR_C = **{ad.get(kr['EAR_C'], kr['EAR_C'])}**. Öteki sıra 'sağlamlık, karar dışı'.
  **Kapsam sayımı görüldü, getiri görülmedi** (hiçbir getiri / eşli fark hesaplanmadı; §12'deki sayılar).
- Temel model = hücredeki BÜTÜN çöl olayları. ÜST - ALT: ay kümeli bootstrap ({S1['bootstrap']} çekiliş, tohum {S1['tohum']}; geçerli çekiliş payı < %{100 * S1['gecerli_pay']:.0f} ise aralık yok).
- 'EK KATKI VAR (yön ÜST)' <=> n_ÜST >= {S1['n_esik']} ve n_ALT >= {S1['n_esik']} VE ÜST ortalama eşli farkı > temel VE (ÜST - ALT) %95 alt sınırı > 0; ALT ayna.

## 5. S2 — 'tek başına' (bilgi; K64 §5 aynen, K64.k64_s2; tohum {E['s2']['tohum']})

## 6. Cetvel (FON_IZI FI_OLCUT aynen; K64.k64_olc / k64_hucre)
FI_OLCUT = {json.dumps({k: FO[k] for k in ("ufuk", "mom", "likit", "mom_kova", "likit_kova", "kriz", "bootstrap", "tohum", "slot", "n_esik", "port_n", "port_yuzde")}, ensure_ascii=False)}.
Eşli fark (60 gün), ay kümeli %95, hücre içi sıra, slot portföyü; HÜCRE TUTAR <=> n >= 30, alt uç > 0, sıra > 0,50, portföy > rastgele %90. Piyasa koşulu katmanı (eşit
ağırlıklı evren endeksi 200 gün ortalamasının üstü / altı; bilgi), 20 günlük ek ufuk (bilgi). MALİYET gidiş-dönüş BIST %{100 * E['maliyet']['BIST']:.1f}, ABD %{100 * E['maliyet']['ABD']:.1f}
(her olaydan düşülür; rastgele eşler maliyetsiz: tutucu).

## 7. Hücreler ve KARAR (K64 §7 aynen; K64.k64_karar)
- Hücre = pazar (BIST, ABD) x dönem (GİRİŞ gününe göre): {dn}. Bağımsız: {', '.join(E['bagimsiz'])}; 2023-2026 tutarlılık (BH ailesine girmez).
- Pazar kararı 'ADAY' <=> iki bağımsız dönemde aynı yönde 'EK KATKI VAR' ve BH'den geçiyor; bir bağımsız dönemde n_ÜST ya da n_ALT < 30 -> 'ÖLÇÜLEMEZ'; aksi 'İZ DEĞİL'.
- İŞARET: ölçülebilen bütün hücrelerde (iki pazar x üç dönem) ÜST - ALT nokta farkının işareti yönle aynı olmalı.
- Genel karar: karar pazarı {E['karar_pazari']}; ABD 'ADAY' ve işaret tutarlı -> **'ABD-ADAY'** (en fazla; İZ için Avrupa olay verisi yok); yalnız BIST 'ADAY' -> 'BIST-ADAY (bilgi)'.

## 8. Çoklu test
Aile = ANA tanım, değişkenin KARAR sırası, ölçülebilen bütün (değişken x yön x pazar x bağımsız dönem) hipotezleri (en çok {m}). p = 1 - Φ(±(ÜST - ALT) / bootstrap sd)
(tek yönlü). Benjamini-Hochberg q = %{100 * E['coklu']['bh_q']:.0f} (K60.k60_bh); Bonferroni bilgi.

## 9. GÜÇ BEYANI
K58: FI_OLCUT 60 günde +%2'lik gerçek etkiyi n = 300 olayda %11, +%4'ü %45 olasılıkla yakalar. Üçte bir grupları daha küçüktür ve değişkenin değeri yalnız son 90 günde
açıklaması olan olaylarda vardır (§12). 'Ek katkı yok' = bu veriyle gösterilemedi; 'ÖLÇÜLEMEZ' = n < 30.

## 10. Yanlılık beyanı
- YAŞAYAN YANLILIĞI: çöl evrenleri (V_BIST, V_ABD) yalnız bugün işlem görenlerdir. BIST açıklama ve EAR portföyü verisi (K62) kotasyondan çıkanları da içerir; ABD
  EAR portföyü yalnız V_ABD sembolleridir (yaşayanlar).
- YENİDEN SUNUM: İş Yatırım yıllık değerleri sonradan düzeltilmiş (K62 SAPMA 9; kanıtlı); SEC frames değerleri de düzeltilmiş olabilir (tarih doğru, değer değil).
- ABD açıklama günü 10-Q / 10-K başvuru günüdür (basın bülteni değil; §2).
- BIST açıklaması akşam yayımlanır (çoğu 18:00 sonrası); ta = yayın günü (işlem günüyse) olduğundan EAR penceresi ertesi günü kapsar; karar günü ta + 1 kapanışıdır,
  yani bilgi akşam yayınında bile çöl gününden önce piyasada.

## 11. SAPMA / BOŞLUK listesi (en dar yorum)
SAPMA 1. ABD açıklama günü = 10-Q / 10-K başvuru günü (iş tanımındaki gibi; basın bülteni çoğu zaman daha erken).
SAPMA 2. BIST SUETF'te TMS 29 kirli çeyrekler YOK; son açıklama kirliyse değer yok (daha eskiye gidilmez).
SAPMA 3. ABD 2x3 portföy kurulabildi (SEC özkaynağı + K60 pay); eşit ağırlıklı evren yedeği kullanılmadı. Portföy evreni V_ABD (1.411), K62 BIST'te bütün KAP / İş Yatırım evreni.
SAPMA 4. BIST'te çöl fiyatları V_BIST (fi_duzelt; bölünme / bedelsiz düzeltmeli, temettüsüz), açıklama değerleri İş Yatırım (temettü düzeltmeli) fiyatından: iki kaynak.
BOŞLUK 1. '90 takvim günü' açıklama günü (ann) ile t arasındadır; karar günü < t ayrıca şarttır.
BOŞLUK 2. ABD çeyrek etiketi (çeyrek içi tertil grubu) = dönem sonu tarihinin takvim çeyreği; mali çeyrek değil.
BOŞLUK 3. ABD MV_q: çeyrek sonu günü bilinen pay bir önceki başvurunun kapak sayısıdır (K60 kuralı; pay o çeyreğin raporunda değil).
BOŞLUK 4. ABD defter değeri için birden çok mali yıl aynı takvim yılında biterse sonuncusu.
BOŞLUK 5. Bilgi grupları (CS, CS_DEGIL, YOK90) yalnız ANA tanım ve HEPSİ rejiminde; BH ailesine ve karara girmez.
BOŞLUK 6. Bir olayın son açıklaması 90 günden eskiyse ya da değeri yoksa o değişken için grupsuzdur; TEMEL model her zaman bütün çöl olaylarıdır (K64 kuralı).
BOŞLUK 7. ABD açıklama günü fiyat takviminin dışındaysa (ilk günden önce ya da sonraki ilk işlem günü {Sp['takvim_tol_gun']} günden uzak) karar günü ve EAR yok (açıklama kullanılmaz).
BOŞLUK 8. ABD açıklama tablosunda 2009-2010 başvuruları da vardır (K60 demeti 2010-01-04'ten); çöl olayları 2015-06'dan başladığı için 90 gün kuralıyla kullanılmazlar.

## 12. Kapsam (yalnız SAYI; mühre girmez)
{kapsam}

## 13. Çıktılar ve komutlar
Çıktılar arastirma_cikti/col_dis_bilgi/: k62b_olaylar.csv.gz, k62b_s1.csv, k62b_s1_fark.csv, k62b_s2.csv, k62b_karar.csv, k62b_bilgi.csv, k62b_meta.json, K62B_RAPOR.md.
1. (ana oturum) bu dosyayı denetler ve git'e işler.
2. `python -I K62B.py kos`  -> ölçüm + rapor (mühür, veri sha256, git doğrulanır)
3. `python K62B.py rapor`   -> raporu çıktılardan yeniden yazar

## 14. Değişmezlik
K62B_ESIK ya da içe alınan tanımlar (FI_K24, FI_OLCUT, K60 bilgi kuralı ve mührü, COL_v1 D13, K64 mührü, K62 mührü) değişirse ESIK_SHA256 değişir ve koşu durur. Veri ya da
içe alınan kod / ön kayıt dosyaları değişirse sha256 tutmaz ve koşu durur.
"""


def k62b_onkayit(cikti: Optional[str] = None, veri_sha: Optional[Dict[str, Tuple[str, int]]] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kaydı yazar. Dosya varsa ÜZERİNE YAZMAZ: mühür aynıysa yolu döndürür, değilse durur. Karar sırası seçilmemişse (None) durur; kapsam dosyası varsa seçim
    kuralının sonucu mühürdeki karar sırasıyla aynı olmalı."""
    E = E or K62B_ESIK; yol = _k62b_yol("onkayit", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True)
    if any(v not in ("IC", "EVREN") for v in E["sira"]["karar"].values()):
        raise K62BHata(f"karar sırası seçilmemiş ({E['sira']['karar']}): önce `kapsam`, kuralın sonucu K62B_ESIK['sira']['karar']'a yazılır")
    if os.path.exists(yol):
        mevcut = K64._k64_onkayit_oku(yol)["sha"]
        if mevcut != k62b_esik_sha(E):
            raise K62BHata(f"ön kayıt zaten var ve mühür farklı ({mevcut} != {k62b_esik_sha(E)}): eşikler ön kayıttan sonra değişmiş")
        k62blog.info("ön kayıt zaten var (mühür aynı): %s", yol)
        return yol
    yk = _k62b_yol("kapsam", cikti)
    if os.path.exists(yk):
        sec, _h = k62b_sira_sec(pd.read_csv(yk), E)
        if sec != E["sira"]["karar"]:
            raise K62BHata(f"karar sırası seçim kuralı kapsam sayımında {sec} veriyor, mühürdeki {E['sira']['karar']}: ön kayıt yazılmadı")
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    metin = k62b_onkayit_metin(zaman, k62b_veri_sha() if veri_sha is None else veri_sha, k62b_kapsam_notu(cikti, E), E)
    if _K62B_EPOSTA.search(metin):
        raise K62BHata("ön kayıt metninde e-posta biçimli parça var; yazılmadı")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k62blog.info("ön kayıt yazıldı: %s (mühür %s)", yol, k62b_esik_sha(E)[:12])
    return yol


def k62b_onkayit_dogrula(cikti: Optional[str] = None, veri: bool = False, git: bool = False, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Mühür (her zaman), veri sha256'ları (veri=True) ve git'e işlenmişlik (git=True) doğrulanır; biri tutmazsa K62BHata."""
    E = E or K62B_ESIK; yol = _k62b_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise K62BHata(f"ön kayıt yok ({yol}): önce `python K62B.py onkayit`")
    oc = K64._k64_onkayit_oku(yol)
    if oc["sha"] != k62b_esik_sha(E):
        raise K62BHata(f"ön kayıt mührü tutmuyor ({oc['sha']} != {k62b_esik_sha(E)}): eşikler ön kayıttan sonra değişmiş, koşu durdu")
    out = {"yol": yol, "sha": oc["sha"], "zaman_utc": oc["zaman_utc"], "dosya_sha256": K60._k60_sha(yol), "veri": oc["veri"]}
    if veri:
        simdi = k62b_veri_sha()
        fark = sorted(k for k in set(simdi) | set(oc["veri"]) if simdi.get(k) != oc["veri"].get(k))
        if fark:
            raise K62BHata(f"veri / içe alınan kod ön kayıttakiyle aynı değil (sha256 ya da dosya sayısı farklı): {fark}; koşu durdu")
    if git:
        try:
            out["git"] = K60._k60_git_islenmis(yol, "K62-B ön kaydı")
        except K60.K60Hata as ex:
            raise K62BHata(str(ex))
    return out


# ---------------------------------------------------------------- 5) KOŞU (K64 cetvel / S1 / S2 / karar fonksiyonları aynen)
def k62b_bilgi_gruplari(X: pd.DataFrame, pazar: str, tanim: str, E: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Bilgi grupları (karar dışı): CS (son açıklamada SUETF ve EAR üst üçte bir), CS_DEGIL (ikisi de sınıflı, CS değil), YOK90; dönem başına FI_OLCUT ölçüleri."""
    c = float(E["maliyet"][pazar]); out = []
    for dn, a, b in E["donem"]:
        md = ((X.giris >= a) & (X.giris <= b) & X.fark.notna()).to_numpy() if len(X) else np.zeros(0, bool)
        for g, m in (("CS", md & X.cs.to_numpy(bool)), ("CS_DEGIL", md & X.cs_var.to_numpy(bool) & ~X.cs.to_numpy(bool)), ("YOK90", md & X.yok90.to_numpy(bool))):
            out.append({"tanim": tanim, "pazar": pazar, "donem": dn, "grup": g, **(K64.k64_hucre(X[m], c) if m.any() else {"n": 0})})
    return out


def k62b_kos(cikti: Optional[str] = None, git_sart: bool = True, girdi: Optional[Dict[str, Dict[str, Any]]] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Tek koşu: ön kayıt (mühür + git) -> [gerçek veride veri sha256 + K60 ön kaydı / verisi] -> olaylar -> değişkenler -> FI_OLCUT -> S1, S2, bilgi grupları ->
    karar -> çıktılar + rapor. girdi / E yalnız testler içindir (sentetik girdi: veri sha256 doğrulaması atlanır; ön kayıt doğrulaması yine şarttır)."""
    Ek = E or K62B_ESIK; sentetik = girdi is not None; t0 = time.time()
    oc = k62b_onkayit_dogrula(cikti, veri=not sentetik, git=git_sart, E=Ek)
    meta: Dict[str, Any] = {"surum": K62B_SURUM, "onkayit": oc, "sentetik": sentetik, "kos_baslangic": _k62b_simdi(), "isolated": bool(sys.flags.isolated),
                            "k62b_kod_sha256": K60._k60_sha(os.path.join(KOK_K62B, "K62B.py")) if os.path.exists(os.path.join(KOK_K62B, "K62B.py")) else None,
                            "surumler": {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}, "pazar": {}}
    if not sentetik:
        try:
            k60 = K60.k60_onkayit_dogrula(None, veri=True, git=False)
        except K60.K60Hata as ex:
            raise K62BHata(f"K60 ön kaydı / verisi doğrulanamadı: {ex}")
        meta["k60_muhur"] = k60["sha"]; girdi = k62b_girdi(Ek, k60["veri"])
    olaylar, s1, frk, s2, bil = [], [], [], [], []
    for pazar in Ek["pazar"]:
        if pazar not in girdi:
            continue
        g = girdi[pazar]; V = g["V"]; H = k62b_pazar_hazirla(g, Ek)
        P = FI.fi_olcut_panel(V); P20 = FI.fi_olcut_panel(V, {**FI.FI_OLCUT, "ufuk": int(Ek["ek_ufuk"])}); F = K64.k64_fark_matris(P)
        if list(P["sembol"]) != list(H["sembol"]) or not P["tarih"].equals(H["takvim"]):
            raise K62BHata(f"{pazar}: FI_OLCUT paneli ile değişken matrisleri aynı takvim / sembol sırasında değil")
        O = _k62b_olaylar(pazar, V, Ek, sentetik); meta["pazar"][pazar] = {**g.get("ozet", {}), "hisse": len(V), "gun": len(H["takvim"])}
        for tanim, X0 in O.items():
            X = _k62b_olay_tablosu(X0, H, tanim, Ek); n_ham = len(X); X = X[X.tekil & X.giris.notna()].reset_index(drop=True)
            if tanim == "D13" and Ek["olay"]["d13"]["gecer"] and len(X):
                X = X[X.gecer].reset_index(drop=True)
            X = K64.k64_olc(P, P20, X) if len(X) else X.assign(r60=np.nan, esli_r60=np.nan, sira=np.nan, fark=np.nan, r20=np.nan, fark20=np.nan)
            X["pazar"] = pazar; X["tanim"] = tanim
            meta["pazar"][pazar][tanim] = {"ham": int(n_ham), "tekil": int(len(X)), "olculen": int(X.fark.notna().sum()) if len(X) else 0}
            a, b = K64.k64_s1(X, pazar, tanim, Ek); s1.append(a); frk.append(b); olaylar.append(X.drop(columns=[c for c in ("_esler",) if c in X]))
            if tanim == Ek["olay"]["ana"]:
                s2.append(K64.k64_s2(P, F, H, X0, pazar, Ek)); bil += k62b_bilgi_gruplari(X, pazar, tanim, Ek)
        k62blog.info("%s ölçüldü (%.0f sn)", pazar, time.time() - t0)
    if not s1:
        raise K62BHata("ölçülecek pazar yok")
    S1 = pd.concat(s1, ignore_index=True); Fk = pd.concat(frk, ignore_index=True); S2 = pd.concat(s2, ignore_index=True) if s2 else pd.DataFrame(); Kr = K64.k64_karar(Fk, Ek)
    Bi = pd.DataFrame(bil); cik = cikti or K62B_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    pd.concat(olaylar, ignore_index=True).to_csv(_k62b_yol("olay", cikti), index=False); S1.to_csv(_k62b_yol("s1", cikti), index=False)
    Fk.to_csv(_k62b_yol("fark", cikti), index=False); S2.to_csv(_k62b_yol("s2", cikti), index=False); Kr.to_csv(_k62b_yol("karar", cikti), index=False)
    Bi.to_csv(_k62b_yol("bilgi", cikti), index=False)
    meta["kos_bitis"] = _k62b_simdi(); meta["sure_sn"] = round(time.time() - t0)
    with open(_k62b_yol("meta", cikti), "w", encoding="utf-8") as f:
        json.dump(K60._k60_yuvarla(meta, 12), f, ensure_ascii=False, indent=1, default=str)
    return {"s1": S1, "fark": Fk, "s2": S2, "karar": Kr, "bilgi": Bi, "meta": meta, "rapor": k62b_rapor(cikti, Ek)}


# ---------------------------------------------------------------- 6) RAPOR
def _k62b_oku(yol: str) -> pd.DataFrame:
    try:
        return pd.read_csv(yol) if os.path.getsize(yol) > 2 else pd.DataFrame()
    except (OSError, pd.errors.EmptyDataError):
        return pd.DataFrame()


def k62b_rapor(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """K62B_RAPOR.md'yi çıktı dosyalarından yazar."""
    E = E or K62B_ESIK; yol = {k: _k62b_yol(k, cikti) for k in ("s1", "fark", "s2", "karar", "bilgi", "meta")}
    if not all(os.path.exists(y) for y in yol.values()):
        raise K62BHata(f"K62-B çıktıları yok ({yol['s1']}): önce `python -I K62B.py kos`")
    S1 = _k62b_oku(yol["s1"]); Fk = _k62b_oku(yol["fark"]); S2 = _k62b_oku(yol["s2"]); Kr = _k62b_oku(yol["karar"]); Bi = _k62b_oku(yol["bilgi"])
    if len(S1):
        S1[["degisken", "sira_turu"]] = S1[["degisken", "sira_turu"]].fillna("")
    with open(yol["meta"], encoding="utf-8") as f:
        m = json.load(f)
    f_, y_, t_ = K64._k64_f, K64._k64_yuz, K64._k64_tam; ana = E["olay"]["ana"]; tn = {d["kod"]: d for d in E["degisken"]}
    par = [f"# K62-B — bilanço sürprizi çöl sinyaline ek bilgi: RAPOR\n\n{K62B_SURUM}. Ön kayıt K62B_ON_KAYIT.md (mühür {str(m['onkayit']['sha'])[:12]}, dosya sha256 "
           f"{str(m['onkayit']['dosya_sha256'])[:12]}, git {str(m['onkayit'].get('git', {}).get('commit', ''))[:7]}); koşu {m['kos_baslangic']} -> {m['kos_bitis']} ({m.get('sure_sn')} sn).\n"]
    if len(Kr):
        par.append("## Karar tablosu (ANA tanım K24; değişkenin karar sırasıyla)\n| değişken | yön | karar | ABD | BIST | ABD ek katkı (3 dönem) | BIST ek katkı | ABD BH | işaret tutarlı | "
                   "ABD grubu dört şart (brüt / net) |\n|---|---|---|---|---|---|---|---|---|---|")
        for r in Kr.to_dict("records"):
            par.append(f"| {r['degisken']} | {'ÜST' if r['yon'] == 'UST' else 'ALT'} | {r['karar']} | {r.get('ABD_karar', '—')} | {r.get('BIST_karar', '—')} | {r.get('ABD_ek', '—')} | "
                       f"{r.get('BIST_ek', '—')} | {r.get('ABD_bh', '—')} | {'evet' if K64._k64_evet(r['isaret_tutarli']) else 'hayır'} | "
                       f"{'evet' if K64._k64_evet(r.get('ABD_dort_sart')) else 'hayır'} / {'evet' if K64._k64_evet(r.get('ABD_dort_sart_net')) else 'hayır'} |")
        par.append(f"\nBH ailesi m = {int(Kr.aile_m.iloc[0])}; q = %{100 * E['coklu']['bh_q']:.0f}. 'İZ' bu işte verilemez (Avrupa olay verisi yok).\n")
    T = S1[(S1.tanim == ana) & (S1.grup == "TEMEL") & (S1.rejim == "HEPSI")] if len(S1) else S1
    par.append("## Temel model (yalnız çöl)\n| pazar | dönem | n | ort. r60 | medyan r60 | ort. eşli fark [%95] | medyan eşli fark | sıra | dört şart |\n|---|---|---|---|---|---|---|---|---|")
    for r in T.to_dict("records"):
        par.append(f"| {r['pazar']} | {r['donem']} | {t_(f_(r, 'n'))} | {y_(f_(r, 'ort_r60'))} | {y_(f_(r, 'medyan_r60'))} | {y_(f_(r, 'ort_fark'))} [{y_(f_(r, 'alt95'))}; {y_(f_(r, 'ust95'))}] | "
                   f"{y_(f_(r, 'medyan_fark'))} | {f_(r, 'sira'):.2f} | {'tutar' if K64._k64_evet(r.get('tutar')) else 'tutmaz'} |")
    for k in k62b_kodlar(E):
        d = tn[k]; st = K64.k64_karar_sirasi(k, E)
        par.append(f"\n## {k}\nTanım: {d['tanim']}. Karar sırası: {'çöl içi (İÇ)' if st == 'IC' else 'evren içi (EVREN)'}; öteki sıra sağlamlık.\n")
        par.append("| pazar | dönem | grup | n | ort. r60 | medyan r60 | ort. eşli fark [%95] | medyan eşli fark | net eşli fark | dört şart (brüt / net) |\n|---|---|---|---|---|---|---|---|---|---|")
        for r in (S1[(S1.tanim == ana) & (S1.degisken == k) & (S1.sira_turu == st) & (S1.rejim == "HEPSI") & S1.grup.isin(["UST", "ALT"])].to_dict("records") if len(S1) else []):
            par.append(f"| {r['pazar']} | {r['donem']} | {'ÜST' if r['grup'] == 'UST' else 'ALT'} | {t_(f_(r, 'n'))} | {y_(f_(r, 'ort_r60'))} | {y_(f_(r, 'medyan_r60'))} | "
                       f"{y_(f_(r, 'ort_fark'))} [{y_(f_(r, 'alt95'))}; {y_(f_(r, 'ust95'))}] | {y_(f_(r, 'medyan_fark'))} | {y_(f_(r, 'ort_fark_net'))} | "
                       f"{'tutar' if K64._k64_evet(r.get('tutar')) else 'tutmaz'} / {'tutar' if K64._k64_evet(r.get('tutar_net')) else 'tutmaz'} |")
        par.append("\n| tanım | sıra | pazar | dönem | n ÜST / ALT | ÜST - ALT [%95] | temel eşli fark | ek katkı | 20 gün ÜST - ALT |\n|---|---|---|---|---|---|---|---|---|")
        for r in (Fk[Fk.degisken == k].to_dict("records") if len(Fk) else []):
            ek = "ÖLÇÜLEMEZ" if not K64._k64_evet(r["olculebilir"]) else ("VAR (ÜST)" if K64._k64_evet(r["ek_UST"]) else ("VAR (ALT)" if K64._k64_evet(r["ek_ALT"]) else "yok"))
            par.append(f"| {r['tanim']} | {r['sira_turu']} | {r['pazar']} | {r['donem']} | {int(r['n_ust'])} / {int(r['n_alt'])} | {y_(f_(r, 'nokta'))} [{y_(f_(r, 'alt'))}; {y_(f_(r, 'ust'))}] | "
                       f"{y_(f_(r, 'ort_temel'))} | {ek} | {y_(f_(r, 'nokta20'))} |")
        if len(S2):
            par.append("\nS2 (çöl dışı evren; bilgi): " + "; ".join(f"{r['pazar']} {r['donem']} ÜST - ALT {y_(f_(r, 'nokta'))} [{y_(f_(r, 'alt'))}; {y_(f_(r, 'ust'))}] "
                                                                     f"(n {t_(f_(r, 'n_ust'))} / {t_(f_(r, 'n_alt'))})" for r in S2[S2.degisken == k].to_dict("records")))
    if len(Bi):
        par.append("\n## Bilgi grupları (karar dışı): ÇÖL + SÜRPRİZ, sınıflı ama CS değil, son 90 günde açıklama yok\n| pazar | dönem | grup | n | ort. eşli fark [%95] | medyan eşli fark | "
                   "sıra | dört şart |\n|---|---|---|---|---|---|---|---|")
        for r in Bi.to_dict("records"):
            par.append(f"| {r['pazar']} | {r['donem']} | {r['grup']} | {t_(f_(r, 'n'))} | {y_(f_(r, 'ort_fark'))} [{y_(f_(r, 'alt95'))}; {y_(f_(r, 'ust95'))}] | {y_(f_(r, 'medyan_fark'))} | "
                       f"{f_(r, 'sira'):.2f} | {'tutar' if K64._k64_evet(r.get('tutar')) else 'tutmaz'} |")
    par.append("\n## Sınırlar\nABD açıklama günü 10-Q / 10-K başvuru günüdür (basın bülteni değil). BIST SUETF'te TMS 29 kirli çeyrekler yok. Çöl evrenleri yalnız yaşayanlar. "
               "'ÖLÇÜLEMEZ' = n < 30, 'İZ DEĞİL' değildir. Ayrıntı: K62B_ON_KAYIT.md §9-§11.\n")
    metin = "\n".join(par); y = _k62b_yol("rapor", cikti)
    if _K62B_EPOSTA.search(metin):
        raise K62BHata("rapor metninde e-posta biçimli parça var; yazılmadı")
    with open(y, "w", encoding="utf-8") as f:
        f.write(metin)
    k62blog.info("rapor: %s", y)
    return y


def _cakisma_kontrol_k62b(_once=_CK_ONCE_K62B, _dosya="K62B.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K62B", "_CK_KAYIT", "_cakisma_kontrol_k62b", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "copy", "_dt", "annotations", "Any", "Dict", "List", "Optional", "Tuple", "FI", "K60", "K62", "K64")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k62b()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=K62B_SURUM)
    ap.add_argument("komut", choices=["kapsam", "onkayit", "kos", "rapor"])
    ap.add_argument("--cikti", default=None)
    a_ = ap.parse_args()
    try:
        if a_.komut == "kapsam":
            K_ = k62b_kapsam(a_.cikti); print(k62b_kapsam_notu(a_.cikti))
        elif a_.komut == "onkayit":
            print(k62b_onkayit(a_.cikti))
        elif a_.komut == "kos":
            R_ = k62b_kos(a_.cikti)
            print("K62-B bitti:", R_["karar"][["degisken", "yon", "karar"]].to_string(index=False) if len(R_["karar"]) else "(karar yok)"); print(R_["rapor"])
        else:
            print(k62b_rapor(a_.cikti))
    except (K62BHata, K64.K64Hata, K62.K62Hata, K60.K60Hata, FileNotFoundError) as ex:
        k62blog.error("%s", ex); sys.exit(1)
