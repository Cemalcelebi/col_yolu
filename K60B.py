"""K60-B — PİYANGO HAVUZU İÇİNDE KOŞULLU AYRIM, tek dosya (11 Kasım 2026; ana oturum iş tanımı; ön kayıt K60B_ON_KAYIT.md).

Soru: K60'ta oynak hisselerde ikiye katlanma olasılığı 2-2,7 kat, yarıya inme 2,8-3,8 kat, medyan eksi çıktı. HAVUZUN İÇİNDE (her ay uygun
evrenin 60 günlük oynaklığı en yüksek %20'si) hangi ölçülebilir özellik kazananı kaybedenden ayırıyor?
  Sınananlar  K60 kütüphanesindeki 77 sinyal + 12 bileşik; havuz içi ÜST / ALT %20 (bayrakta bayraklı grup). Sıralar HAVUZ içinde.
  Ölçü        12 ay: P(+%100), P(-%50), ortalama, medyan (uç ve havuz); kat_p100, kat_m50, ASIM = kat_p100 / kat_m50; K60 §5 bootstrap'ı.
  Akış        KEŞİF (mekanik seçim: plasebo en-büyük / en-küçük eşiği) -> DOĞRULAMA -> KASA; etiketler 'bilgi' düzeyinde, İZ değil.
K60 fonksiyonları (veri demeti, panel, sinyaller, ileri getiri, çekiliş dizini) MODÜL olarak içe alınır; K60.py DEĞİŞMEZ. Ağ kullanılmaz.

Komut:  python -I K60B.py kos      ön kayıt sha256 + git + K60 mührü + veri sha256 doğrulanır; üç dönem tek koşuda ölçülür; rapor yazılır
        python K60B.py rapor      K60B_RAPOR.md'yi çıktılardan yeniden yazar
Colab:  exec(open('K60B.py').read()); k60b_kos()
Çıktı:  arastirma_cikti/k60_kutuphane/ k60b_tablo.csv, k60b_aylik.csv, k60b_portfoy_aylik.csv, k60b_plasebo.csv, k60b_meta.json, K60B_RAPOR.md.
        Kişisel e-posta / anahtar yok.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K60B = {k: id(v) for k, v in globals().items()}

import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K60B = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K60B not in sys.path:
    sys.path.insert(0, KOK_K60B)

import K60  # noqa: E402

K58, K59 = K60.K58, K60.K59

k60blog = logging.getLogger("col.k60b")
if not k60blog.handlers:
    _k60b_h = logging.StreamHandler(sys.stderr)
    _k60b_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k60b: %(message)s", "%H:%M:%S"))
    k60blog.addHandler(_k60b_h)
    k60blog.setLevel(logging.INFO)
    k60blog.propagate = False

K60B_SURUM = "K60-B v1.0 (2026-11-11): piyango havuzu (oynaklığı en yüksek %20) içinde koşullu ayrım; K60 kütüphanesi, havuz içi ÜST / ALT %20, kat ve ASIM"
K60B_ONKAYIT_SHA = "b74f3e2d26568b816d3e7094d0c5b906e9035c533c0947ae1f2debe22dec57bb"      # K60B_ON_KAYIT.md (git 5aac5de); değişirse koşu durur
K60B_YOL = {"cikti": K60.K60_YOL["cikti"], "onkayit": os.path.join(K60.K60_YOL["cikti"], "K60B_ON_KAYIT.md")}
K60B_DOSYA = {"tablo": "k60b_tablo.csv", "aylik": "k60b_aylik.csv", "portfoy": "k60b_portfoy_aylik.csv", "plasebo": "k60b_plasebo.csv", "meta": "k60b_meta.json",
              "rapor": "K60B_RAPOR.md"}

# Ön kayıttaki sabitler (K60B_ON_KAYIT.md); buraya yeni eşik EKLENMEZ. 'asim_min_cekilis' K60-EK'teki kuraldır (BOŞLUK 3).
K60B_ESIK: Dict[str, Any] = {
    "havuz": {"sinyal": "VOL_60D", "pay": 0.20, "min_hisse": 150},
    "uc": {"pay": 0.20, "min_sinyal": 100, "min_bayrak": 10},
    "olcu": {"ana_ufuk": 12, "bilgi_ufuk": [6], "p100": 1.0, "m50": -0.5, "min_ay": 12, "min_hisse_ay": 200, "guven": [2.5, 97.5], "asim_min_cekilis": 400},
    "portfoy": {"maliyet": 0.001, "nw_lag": 6, "min_ay": 12},
    "plasebo": {"n": 200, "tohum": 60200, "maks_tekrar": 2000, "maks_tohum": 60203, "maks_yuzde": 95.0, "donem_yuzde": 95.0, "yp_esik": 0.05},
    "secim": {"kat_p100_min": 0.90, "bh_q": 0.10},
    "ek_satir": {"REV_YOY": {"yon": "+", "tur": "surekli", "aile": "EK"}},
    "baslik": [["DOSYA_Y", "UST"], ["COMP4", "UST"], ["SP", "UST"], ["NEF", "UST"], ["SALES_ACCEL", "UST"], ["REV_YOY", "UST"], ["EAR_ANN", "UST"], ["RUNWAY", "UST"], ["RUNWAY", "ALT"],
               ["NSI_1Y", "UST"], ["NSI_1Y", "ALT"], ["E_S3", "ALT"], ["E_424B5", "ALT"], ["E_RSPLIT", "ALT"], ["HIGH52", "UST"], ["HIGH52", "ALT"], ["MOM_12_1", "UST"],
               ["MOM_12_1", "ALT"], ["SIZE_ME", "UST"], ["SIZE_ME", "ALT"], ["PRICE_LVL", "UST"], ["PRICE_LVL", "ALT"], ["ROA_Q", "UST"], ["ROA_Q", "ALT"], ["BM", "UST"]],
    "etiket": {"firsat": "K60B-KOŞULLU FIRSAT", "koruma": "K60B-KOŞULLU KORUMA", "yakin": "YAKIN"},
}


class K60BHata(RuntimeError):
    """K60-B'ye özgü durdurucu hata (ön kayıt değişmiş / git'e işlenmemiş, veri K60 ön kaydındakinden farklı, çıktı yok)."""


def _k60b_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K60B_YOL["cikti"], K60B_DOSYA.get(ad, ad))


# ---------------------------------------------------------------- 0) ÖN KAYIT DOĞRULAMASI
def k60b_onkayit_dogrula(yol: Optional[str] = None, beklenen: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    """K60B_ON_KAYIT.md: dosya sha256'sı koda yazılı değerle aynı (içerik değişmemiş) ve (git=True) git'e işlenmiş, sonradan değişmemiş olmalı."""
    yol = yol or K60B_YOL["onkayit"]; beklenen = beklenen or K60B_ONKAYIT_SHA
    if not os.path.exists(yol):
        raise K60BHata(f"ön kayıt yok: {yol}")
    sha = K60._k60_sha(yol)
    if sha != beklenen:
        raise K60BHata(f"ön kayıt dosyası değişmiş (sha256 {sha[:12]} != {beklenen[:12]}): koşu durdu")
    out: Dict[str, Any] = {"yol": yol, "dosya_sha256": sha}
    if git:
        try:
            out["git"] = K60._k60_git_islenmis(yol, "K60-B ön kaydı")
        except K60.K60Hata as ex:
            raise K60BHata(str(ex))
    return out


# ---------------------------------------------------------------- 1) HAVUZ VE HAVUZ İÇİ SİNYALLER (yalnız t ve öncesi bilgi)
def k60b_havuz(P: Dict[str, Any], vol: np.ndarray, bag: np.ndarray, B: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Havuz (ay x hisse, bool): her ay sonu, uygun ve 60 günlük oynaklığı olan hisselerin oynaklığı en yüksek %pay'ı (sayı = max(1,
    yuvarla(pay x oynaklığı olan uygun hisse)); eşitlik K60 sabit tohumlu sırayla). Havuzu min_hisse'den küçük ay atlanır (bütünü False)."""
    Hv = (B or K60B_ESIK)["havuz"]; U = P["U"]
    key = K60.k60_sira(vol, U, bag); H = K58.k58_ust_dilim(key, np.isfinite(key), Hv["pay"])
    H[H.sum(axis=1) < Hv["min_hisse"]] = False
    return H


def k60b_satirlar(E: Optional[Dict[str, Any]] = None, B: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Ölçülecek satırlar: K60 kütüphanesi + bileşikler ('aile' = True: hipotez ailesinde) + ön kayıtta adı geçen ek başlık satırı REV_YOY (aile dışı)."""
    out = [{**s, "hipotez": True} for s in K60.k60_satirlar(E)]
    for k, v in (B or K60B_ESIK)["ek_satir"].items():
        out.append({"kod": k, "yon": v["yon"], "yon_kayit": v["yon"], "tur": v["tur"], "aile": v["aile"], "r1_uc": [], "sinif": "ek", "hipotez": False})
    return out


def k60b_havuz_sinyalleri(Sd: Dict[str, np.ndarray], ek: Dict[str, Any], sureklilik: Optional[np.ndarray], H: np.ndarray,
                          E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """Havuz içi sinyaller (ay x hisse; havuz dışı NaN; HAM ölçü). Ham sinyaller K60'taki değerleriyle; sıra tabanlı olanlar HAVUZ içinde yeniden:
    MOM_FIP = havuz içi yüzdelik sıra ortalaması (MOM_12_1, süreklilik); bileşikler = üyelerin (beklenen yön uygulanmış) havuz içi yüzdelik
    sıra ortalaması (K59.k59_bilesik, evren yerine havuz). REV_YOY ek satır olarak eklenir."""
    E = E or K60.K60_ESIK; tn = K60.k60_tanim(E); maske = lambda X: np.where(H & np.isfinite(X), X, np.nan)  # noqa: E731
    Sh = {k: maske(Sd[k]) for k in tn}
    if sureklilik is not None:
        with np.errstate(invalid="ignore"):
            Sh["MOM_FIP"] = (K59.k59_yuzde_sira(Sd["MOM_12_1"], H) + K59.k59_yuzde_sira(sureklilik, H)) / 2.0
    else:
        Sh["MOM_FIP"] = np.full(H.shape, np.nan)
    yonlu = {k: (-1.0 if tn[k]["yon"] == "-" else 1.0) * Sh[k] for k in tn}
    for k in E["ek_bilesen"]:
        Sh[k] = maske(ek["bilesen"][k]) if k in ek.get("bilesen", {}) else np.full(H.shape, np.nan); yonlu[k] = Sh[k]
    for b, t in E["bilesik"].items():
        Sh[b] = K59.k59_bilesik(yonlu, H, [u for u in t["uye"] if u in yonlu], t["min"])
    return Sh


def k60b_uclar(S: np.ndarray, yon: str, tur: str, H: np.ndarray, bag: np.ndarray, B: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
    """Havuz içi uçlar. Sürekli: sinyali olan havuz hisselerinin beklenen yöne göre ÜST / ALT %pay'ı (sayı = max(1, yuvarla(pay x n))); bayrak:
    bayraklı havuz hisseleri ('+' ÜST, '-' ALT). 'say' = ay başına sinyali olan (bayrakta bayraklı) havuz hissesi; 'min' = o ayın ölçülme alt sınırı."""
    Uc = (B or K60B_ESIK)["uc"]
    if tur == "bayrak":
        with np.errstate(invalid="ignore"):
            b = H & np.isfinite(S) & (S > 0.5)
        return {("ALT" if yon == "-" else "UST"): {"sec": b, "say": b.sum(axis=1), "min": Uc["min_bayrak"]}}
    key = K60.k60_sira((-1.0 if yon == "-" else 1.0) * S, H, bag); Hs = np.isfinite(key); say = Hs.sum(axis=1)
    return {"UST": {"sec": K58.k58_ust_dilim(key, Hs, Uc["pay"]), "say": say, "min": Uc["min_sinyal"]},
            "ALT": {"sec": K58.k58_ust_dilim(-key, Hs, Uc["pay"]), "say": say, "min": Uc["min_sinyal"]}}


# ---------------------------------------------------------------- 2) ÖLÇÜ: KAT, ASIM, ARALIK
def k60b_kat(kd100: Any, nd: Any, kb100: Any, nb: Any, kdm: Any, kbm: Any, B: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    """Aylık sayımlardan (uçta +%100, uç hisse, havuzda +%100, havuz hisse, uçta -%50, havuzda -%50): havuz olasılıkları, kat_p100, kat_m50,
    ASIM ve %95 aralıkları (K60.k60_blok_dizini: blok 12 ay, 500 çekiliş, tohum 60002). kat aralığı K60.k60_lift kuralıyla (havuz oranı > 0
    olan çekilişler, en az yarısı); ASIM aralığı paydası sıfır olmayan çekilişlerle, geçerli çekiliş < asim_min_cekilis ise NaN. p değerleri
    z yaklaşımı: p_asim = P(ASIM <= 1), p_koruma = P(kat_m50 >= 1) (BH için; seçim şartı değil)."""
    O = (B or K60B_ESIK)["olcu"]; kd100, nd, kb100, nb, kdm, kbm = (np.asarray(x, float) for x in (kd100, nd, kb100, nb, kdm, kbm)); T = len(nd)
    out = {k: np.nan for k in ("P_p100", "havuz_p100", "kat_p100", "alt_p100", "ust_p100", "P_m50", "havuz_m50", "kat_m50", "alt_m50", "ust_m50", "asim", "asim_alt",
                               "asim_ust", "p_asim", "p_koruma")}
    out["asim_gecerli"] = 0
    if not T or nd.sum() <= 0 or nb.sum() <= 0:
        return out
    ix = K60.k60_blok_dizini(T); cek: Dict[str, np.ndarray] = {}
    with np.errstate(invalid="ignore", divide="ignore"):
        for ad, kd, kb in (("p100", kd100, kb100), ("m50", kdm, kbm)):
            Pd, Pb = kd.sum() / nd.sum(), kb.sum() / nb.sum(); out[f"P_{ad}"], out[f"havuz_{ad}"] = float(Pd), float(Pb)
            Ld = kd[ix].sum(axis=1) / nd[ix].sum(axis=1); Lb = kb[ix].sum(axis=1) / nb[ix].sum(axis=1)
            L = np.where(Lb > 0, Ld / np.where(Lb > 0, Lb, 1.0), np.nan); cek[ad] = L; s = L[np.isfinite(L)]
            if Pb > 0:
                out[f"kat_{ad}"] = float(Pd / Pb)
                if len(s) >= 0.5 * len(L):
                    out[f"alt_{ad}"], out[f"ust_{ad}"] = (float(x) for x in np.percentile(s, O["guven"]))
        if np.isfinite(out["kat_p100"]) and np.isfinite(out["kat_m50"]) and out["kat_m50"] > 0:
            out["asim"] = out["kat_p100"] / out["kat_m50"]
        A = np.where(np.isfinite(cek["p100"]) & np.isfinite(cek["m50"]) & (cek["m50"] > 0), cek["p100"] / np.where(cek["m50"] > 0, cek["m50"], 1.0), np.nan)
        s = A[np.isfinite(A)]; out["asim_gecerli"] = int(len(s))
        if len(s) >= O["asim_min_cekilis"]:
            out["asim_alt"], out["asim_ust"] = (float(x) for x in np.percentile(s, O["guven"]))
            poz = s[s > 0]; sd = float(np.log(poz).std(ddof=1)) if len(poz) > 1 else np.nan
            if np.isfinite(out["asim"]) and out["asim"] > 0 and sd > 0:
                out["p_asim"] = float(K60._k60_norm_p(math.log(out["asim"]) / sd))
        m = cek["m50"]; poz = m[np.isfinite(m) & (m > 0)]; sd = float(np.log(poz).std(ddof=1)) if len(poz) > 1 else np.nan
        if np.isfinite(out["kat_m50"]) and out["kat_m50"] > 0 and sd > 0:
            out["p_koruma"] = float(K60._k60_norm_p(-math.log(out["kat_m50"]) / sd))
    return out


def _k60b_taban(P: Dict[str, Any], H: np.ndarray, h: int, B: Dict[str, Any]) -> Dict[str, Any]:
    """Havuz tabanı (ufuk h): ileri getirisi olan havuz hisse-ayları ve olay maskeleri."""
    O = B["olcu"]; F = P["F"][h]; gec = H & np.isfinite(F)
    with np.errstate(invalid="ignore"):
        return {"gec": gec, "p100": gec & (F >= O["p100"]), "m50": gec & (F <= O["m50"]), "F": F}


def k60b_olc(P: Dict[str, Any], sec: np.ndarray, ol: np.ndarray, taban: Dict[int, Dict[str, Any]], B: Optional[Dict[str, Any]] = None) -> Tuple[List[Dict[str, Any]], pd.DataFrame]:
    """Bir ucun ölçüsü: her ufuk için bir satır (P, kat, ASIM, aralıklar, uç / havuz ortalama ve medyanı); ana ufkun aylık sayım tablosu.
    Aylar = ol içinde ileri penceresi veride biten aylar."""
    B = B or K60B_ESIK; O = B["olcu"]; me = P["ay_sonu"]; M = len(me); sat = []; A = pd.DataFrame()
    for h in [O["ana_ufuk"]] + list(O["bilgi_ufuk"]):
        tb = taban[h]; ay = np.flatnonzero(ol & (np.arange(M) + h <= M - 1)); row: Dict[str, Any] = {"ufuk": int(h), "ay": int(len(ay)), "olculdu": False}
        if len(ay):
            d = sec & tb["gec"]; nd = d.sum(axis=1)[ay]; nb = tb["gec"].sum(axis=1)[ay]
            kd100 = (d & tb["p100"]).sum(axis=1)[ay]; kb100 = tb["p100"].sum(axis=1)[ay]; kdm = (d & tb["m50"]).sum(axis=1)[ay]; kbm = tb["m50"].sum(axis=1)[ay]
            fd = tb["F"][ay][d[ay]]; fb = tb["F"][ay][tb["gec"][ay]]
            row.update({"n": int(nd.sum()), "n_havuz": int(nb.sum()), "ilk_ay": str(me[ay[0]].date()), "son_ay": str(me[ay[-1]].date()), **k60b_kat(kd100, nd, kb100, nb, kdm, kbm, B),
                        "ort": float(fd.mean()) if len(fd) else np.nan, "medyan": float(np.median(fd)) if len(fd) else np.nan,
                        "havuz_ort": float(fb.mean()) if len(fb) else np.nan, "havuz_medyan": float(np.median(fb)) if len(fb) else np.nan})
            row["olculdu"] = bool(len(ay) >= O["min_ay"] and nd.sum() >= O["min_hisse_ay"] and np.isfinite(row["kat_p100"]))
            if h == O["ana_ufuk"]:
                A = pd.DataFrame({"ay_sonu": [str(x.date()) for x in me[ay]], "n": nd, "n_havuz": nb, "k_p100": kd100, "k_havuz_p100": kb100, "k_m50": kdm, "k_havuz_m50": kbm})
        sat.append(row)
    return sat, A


def k60b_portfoy(P: Dict[str, Any], sec: np.ndarray, ol: np.ndarray, H: np.ndarray, B: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Aylık portföy (bilgi): uç eşit ağırlık, 1 ay tutma, maliyetli; kıyas = havuz eşit ağırlık (K58.k58_portfoy, evren yerine havuz). Net yıllık
    fazla ve beta düzeltmeli alfanın NW t'si (K59.k59_ols_nw)."""
    Pf = (B or K60B_ESIK)["portfoy"]; k = np.flatnonzero(ol); bos = {"pf_ay": int(len(k)), "pf_fazla": np.nan, "pf_alfa": np.nan, "pf_t_alfa": np.nan}
    if len(k) < Pf["min_ay"]:
        return bos, pd.DataFrame()
    X = K58.k58_portfoy(P["R"], sec, H, ol, Pf["maliyet"]); reg = K59.k59_ols_nw(X["net"], X["kiyas"], Pf["nw_lag"])
    A = pd.DataFrame({"ay_sonu": [str(x.date()) for x in P["ay_sonu"][k]], "net": X["net"], "brut": X["brut"], "kiyas": X["kiyas"], "devir": X["devir"]})
    return {"pf_ay": int(len(k)), "pf_fazla": float(12 * (X["net"] - X["kiyas"]).mean()), "pf_alfa": float(12 * reg["katsayi"][0]), "pf_t_alfa": float(reg["t"][0])}, A


def k60b_donem_olc(P: Dict[str, Any], Sh: Dict[str, np.ndarray], H: np.ndarray, donem: str, bag: np.ndarray, E: Optional[Dict[str, Any]] = None,
                   B: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Bir dönem: her (sinyal, uç) için ölçü + portföy; plasebolar; havuz ve evren taban oranları."""
    E = E or K60.K60_ESIK; B = B or K60B_ESIK; O = B["olcu"]; Pl = B["plasebo"]; U = P["U"]; me = P["ay_sonu"]; M = len(me)
    pm = K60.k60_donem_aylari(P, donem, 1, E) & H.any(axis=1); taban = {h: _k60b_taban(P, H, h, B) for h in [O["ana_ufuk"]] + list(O["bilgi_ufuk"])}
    sat, ayl, pfl = [], [], []
    for s in k60b_satirlar(E, B):
        if s["kod"] not in Sh:
            continue
        for taraf, u in k60b_uclar(Sh[s["kod"]], s["yon"], s["tur"], H, bag, B).items():
            ol = pm & (u["say"] >= u["min"]); rr, A = k60b_olc(P, u["sec"], ol, taban, B); pf, Ap = k60b_portfoy(P, u["sec"], ol, H, B)
            kim = {"sinyal": s["kod"], "taraf": taraf, "donem": donem, "aile": s["aile"], "yon": s["yon_kayit"], "tur": s["tur"], "hipotez": bool(s["hipotez"])}
            sat += [{**kim, **r, **(pf if r["ufuk"] == O["ana_ufuk"] else {}), "ort_n": float(u["say"][ol].mean()) if ol.any() else np.nan} for r in rr]
            if len(A):
                ayl.append(A.assign(sinyal=s["kod"], taraf=taraf, donem=donem))
            if len(Ap):
                pfl.append(Ap.assign(sinyal=s["kod"], taraf=taraf, donem=donem))
    pls = []
    for i in range(Pl["n"]):
        S = np.random.default_rng(Pl["tohum"] + i).random(U.shape); S[~H] = np.nan
        r = k60b_olc(P, K58.k58_ust_dilim(S, H, B["uc"]["pay"]), pm, taban, B)[0][0]
        pls.append({"plasebo": i, "donem": donem, **{k: r.get(k) for k in ("ay", "olculdu", "n", "kat_p100", "alt_p100", "ust_p100", "kat_m50", "alt_m50", "ust_m50", "asim", "asim_alt",
                                                                            "asim_ust", "ort", "medyan", "havuz_ort", "havuz_medyan")}})
    h = O["ana_ufuk"]; ay = np.flatnonzero(pm & (np.arange(M) + h <= M - 1)); tb = taban[h]; F = P["F"][h]; ge = U & np.isfinite(F)
    with np.errstate(invalid="ignore"):
        fh, fe = F[ay][tb["gec"][ay]], F[ay][ge[ay]]
        ozet = {"donem": donem, "ay_portfoy": int(pm.sum()), "ay_12": int(len(ay)), "havuz_ort_hisse": float(H[pm].sum(axis=1).mean()) if pm.any() else 0.0,
                "evren_ort_hisse": float(U[pm].sum(axis=1).mean()) if pm.any() else 0.0, "havuz_hisse_ay": int(len(fh)), "evren_hisse_ay": int(len(fe)),
                "havuz_p100": float((fh >= O["p100"]).mean()) if len(fh) else None, "havuz_m50": float((fh <= O["m50"]).mean()) if len(fh) else None,
                "havuz_ort": float(fh.mean()) if len(fh) else None, "havuz_medyan": float(np.median(fh)) if len(fh) else None,
                "evren_p100": float((fe >= O["p100"]).mean()) if len(fe) else None, "evren_m50": float((fe <= O["m50"]).mean()) if len(fe) else None,
                "evren_ort": float(fe.mean()) if len(fe) else None, "evren_medyan": float(np.median(fe)) if len(fe) else None}
    return {"tablo": pd.DataFrame(sat), "aylik": pd.concat(ayl, ignore_index=True) if ayl else pd.DataFrame(), "portfoy": pd.concat(pfl, ignore_index=True) if pfl else pd.DataFrame(),
            "plasebo": pd.DataFrame(pls), "ozet": ozet}


# ---------------------------------------------------------------- 3) SEÇİM, GEÇİŞ, ETİKET
def _k60b_f(r: Any, k: str) -> float:
    try:
        v = r[k] if isinstance(r, dict) else getattr(r, k)
        return float(v) if v is not None and pd.notna(v) else np.nan
    except (KeyError, AttributeError, TypeError, ValueError):
        return np.nan


def _k60b_evet(x: Any) -> bool:
    return str(x).strip().lower() in ("true", "1", "1.0")


def k60b_sartlar(r: Any, B: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
    """Bir satırın plasebo şartı DIŞINDAKİ şartları: 'firsat' (kat_p100 alt > 1, ASIM alt > 1, uç ort. > havuz ort.), 'koruma' (kat_m50 üst < 1,
    kat_p100 >= 0,90, uç medyanı > havuz medyanı) ve nokta karşılıkları ('_nokta': aralık yerine nokta değer). NaN ölçü şartı sağlamaz."""
    S = (B or K60B_ESIK)["secim"]; f = lambda k: _k60b_f(r, k)  # noqa: E731
    with np.errstate(invalid="ignore"):
        olc = _k60b_evet(r["olculdu"] if isinstance(r, dict) else getattr(r, "olculdu", False))
        ort = bool(f("ort") > f("havuz_ort")); med = bool(f("medyan") > f("havuz_medyan")); p90 = bool(f("kat_p100") >= S["kat_p100_min"])
        return {"firsat": bool(olc and f("alt_p100") > 1 and f("asim_alt") > 1 and ort), "koruma": bool(olc and f("ust_m50") < 1 and p90 and med),
                "firsat_nokta": bool(olc and f("kat_p100") > 1 and f("asim") > 1 and ort), "koruma_nokta": bool(olc and f("kat_m50") < 1 and p90 and med)}


def k60b_secim(T: pd.DataFrame, Pl: pd.DataFrame, B: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """KEŞİF seçimi (mekanik): hipotez ailesindeki ölçülmüş ana ufuk satırları; FIRSAT adayı = şartlar + ASIM > plasebo en-büyük eşiği; KORUMA
    adayı = şartlar + kat_m50 < plasebo en-küçük eşiği. BH %10 (p_asim, p_koruma) yalnız raporlanır. T'ye sütun ekler (yerinde)."""
    B = B or K60B_ESIK; Pp = B["plasebo"]; au = B["olcu"]["ana_ufuk"]
    f = ((T.donem == "kesif") & (T.ufuk == au) & T.hipotez.map(_k60b_evet) & T.olculdu.map(_k60b_evet)).to_numpy(); m = int(f.sum())
    Em = {"coklu": {"maks_tohum": Pp["maks_tohum"], "maks_tekrar": Pp["maks_tekrar"], "maks_yuzde": Pp["maks_yuzde"]}}
    esik = {"hipotez": m, "asim_maks": K60.k60_plasebo_maks(Pl.asim.astype(float), m, Em), "kat_m50_min": -K60.k60_plasebo_maks(-Pl.kat_m50.astype(float), m, Em),
            "plasebo_asim_maks": float(np.nanmax(Pl.asim.astype(float))), "plasebo_kat_m50_min": float(np.nanmin(Pl.kat_m50.astype(float)))}
    sr = [k60b_sartlar(r, B) for r in T.to_dict("records")]
    asim = T.asim.astype(float).to_numpy(); km = T.kat_m50.astype(float).to_numpy()
    with np.errstate(invalid="ignore"):
        T["aday_firsat"] = f & np.array([x["firsat"] for x in sr]) & (asim > esik["asim_maks"])
        T["aday_koruma"] = f & np.array([x["koruma"] for x in sr]) & (km < esik["kat_m50_min"])
    for ad, kol in (("bh_asim", "p_asim"), ("bh_koruma", "p_koruma")):
        T[ad] = False; T.loc[f, ad] = K60.k60_bh(T[kol].astype(float).to_numpy()[f], B["secim"]["bh_q"])
    aday = [{"sinyal": r.sinyal, "taraf": r.taraf, "yol": y} for y, kol in (("FIRSAT", "aday_firsat"), ("KORUMA", "aday_koruma")) for r in T[T[kol]].itertuples()]
    return {"esik": esik, "aday": aday}


def k60b_gecis(T: pd.DataFrame, Pl: pd.DataFrame, aday: List[Dict[str, Any]], donem: str, B: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """DOĞRULAMA / KASA: yalnız KEŞİF adayları, aynı uç ve yol. FIRSAT geçer = şartlar + ASIM > dönem plasebolarının %95 dilimi; KORUMA geçer =
    şartlar + kat_m50 < plasebo kat_m50'lerinin %5 dilimi. 'nokta' = aralık / plasebo dışındaki şartlar tam ve nokta değerler doğru yönde."""
    B = B or K60B_ESIK; y = B["plasebo"]["donem_yuzde"]; au = B["olcu"]["ana_ufuk"]
    a = Pl.asim.astype(float).to_numpy(); k = Pl.kat_m50.astype(float).to_numpy()
    pl = {"asim95": float(np.percentile(a[np.isfinite(a)], y)) if np.isfinite(a).any() else np.nan,
          "kat_m50_05": float(np.percentile(k[np.isfinite(k)], 100 - y)) if np.isfinite(k).any() else np.nan}
    ps = [k60b_sartlar({**r, "olculdu": r.get("olculdu", False)}, B) for r in Pl.to_dict("records")]
    pl["plasebo_firsat_oran"] = float(np.mean([x["firsat"] for x in ps])) if ps else np.nan; pl["plasebo_koruma_oran"] = float(np.mean([x["koruma"] for x in ps])) if ps else np.nan
    pl["aralik_dar"] = bool(max(pl["plasebo_firsat_oran"], pl["plasebo_koruma_oran"]) > B["plasebo"]["yp_esik"])
    ix = {(r["sinyal"], r["taraf"]): r for r in T[(T.donem == donem) & (T.ufuk == au)].to_dict("records")}; out = []
    for x in aday:
        r = ix.get((x["sinyal"], x["taraf"])); s = k60b_sartlar(r, B) if r is not None else {"firsat": False, "koruma": False, "firsat_nokta": False, "koruma_nokta": False}
        with np.errstate(invalid="ignore"):
            if x["yol"] == "FIRSAT":
                gecer = bool(s["firsat"] and _k60b_f(r, "asim") > pl["asim95"]); nokta = bool(s["firsat_nokta"])
            else:
                gecer = bool(s["koruma"] and _k60b_f(r, "kat_m50") < pl["kat_m50_05"]); nokta = bool(s["koruma_nokta"])
        out.append({**x, "donem": donem, "gecer": gecer, "nokta": nokta})
    return {"plasebo": pl, "sonuc": out}


def k60b_etiketler(aday: List[Dict[str, Any]], dog: List[Dict[str, Any]], kasa: List[Dict[str, Any]], B: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Etiket: KEŞİF adayı + DOĞRULAMA geçti + KASA geçti. YAKIN: ikisinden biri geçti, öteki yalnız aralık / plasebo şartını kaçırdı (nokta doğru yönde)."""
    Et = (B or K60B_ESIK)["etiket"]; d = {(x["sinyal"], x["taraf"], x["yol"]): x for x in dog}; k = {(x["sinyal"], x["taraf"], x["yol"]): x for x in kasa}; out = []
    for x in aday:
        a = (x["sinyal"], x["taraf"], x["yol"]); p, q = d.get(a), k.get(a); ad = Et["firsat"] if x["yol"] == "FIRSAT" else Et["koruma"]; et = ""
        if p and q:
            if p["gecer"] and q["gecer"]:
                et = ad
            elif (p["gecer"] and not q["gecer"] and q["nokta"]) or (q["gecer"] and not p["gecer"] and p["nokta"]):
                et = f"{Et['yakin']} ({ad}; {K60.K60_DONEM_AD['kasa' if p['gecer'] else 'dogrulama']}'da aralık / plasebo şartı kaçtı)"
        out.append({**x, "dogrulama": bool(p and p["gecer"]), "kasa": bool(q and q["gecer"]), "etiket": et})
    return out


# ---------------------------------------------------------------- 4) KOŞU
def k60b_hazirla(D: Dict[str, Any], E: Optional[Dict[str, Any]] = None, B: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Demetten panel, K60 sinyalleri, havuz ve havuz içi sinyaller (yalnız t ve öncesi bilgi)."""
    E = E or K60.K60_ESIK; B = B or K60B_ESIK
    P = K60.k60_panel(D, E, True); Sd, ek = K60.k60_sinyaller(D, P, E); bag = K60.k60_bag(P["U"].shape, E)
    try:
        sur = K60._k60_sinyal_fiyat(D, P, E)[1].get("sureklilik")
    except Exception as ex:       # süreklilik bileşeni üretilemezse MOM_FIP havuzda ölçülmez (öteki sinyaller sürer)
        k60blog.warning("süreklilik bileşeni üretilemedi (%s): MOM_FIP havuz içinde NaN", ex); sur = None
    H = k60b_havuz(P, Sd[B["havuz"]["sinyal"]], bag, B)
    return {"P": P, "Sd": Sd, "ek": ek, "bag": bag, "H": H, "Sh": k60b_havuz_sinyalleri(Sd, ek, sur, H, E)}


def k60b_kos(cikti: Optional[str] = None, demet: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None, B: Optional[Dict[str, Any]] = None,
             onkayit_yol: Optional[str] = None, git_sart: bool = True) -> Dict[str, Any]:
    """Tek koşu: ön kayıt (sha256 + git) -> [gerçek veride K60 mührü + veri sha256] -> KEŞİF -> mekanik seçim -> DOĞRULAMA -> KASA -> çıktılar + rapor.
    demet / E / B yalnız testler içindir (sentetik demet; veri sha256 doğrulaması atlanır, ön kayıt doğrulaması yine şarttır)."""
    Ek = E or K60.K60_ESIK; Bk = B or K60B_ESIK; sentetik = demet is not None; t0 = time.time()
    oc = k60b_onkayit_dogrula(onkayit_yol, None, git_sart)
    meta: Dict[str, Any] = {"surum": K60B_SURUM, "onkayit": oc, "sentetik": sentetik, "kos_baslangic": K60._k60_simdi(), "isolated": bool(sys.flags.isolated),
                            "k60_kod_sha256": K60._k60_sha(os.path.join(KOK_K60B, "K60.py")) if os.path.exists(os.path.join(KOK_K60B, "K60.py")) else None,
                            "k60b_kod_sha256": K60._k60_sha(os.path.join(KOK_K60B, "K60B.py")) if os.path.exists(os.path.join(KOK_K60B, "K60B.py")) else None,
                            "surumler": {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}, "not": []}
    if not sentetik:
        try:
            k60 = K60.k60_onkayit_dogrula(None, veri=True, git=False)      # K60 mührü + veri önbelleklerinin K60 ön kaydındaki sha256'ları
        except K60.K60Hata as ex:
            raise K60BHata(f"K60 ön kaydı / verisi doğrulanamadı: {ex}")
        meta["k60_muhur"] = k60["sha"]; meta["veri"] = k60["veri"]
        D = K60.k60_demet_yukle(k60["veri"])
    else:
        D = demet
    X = k60b_hazirla(D, Ek, Bk); P, H = X["P"], X["H"]
    meta["havuz_ay"] = int(H.any(axis=1).sum()); meta["hisse"] = len(P["sembol"])
    k60blog.info("hazır: %d hisse, havuzlu ay %d, havuz ort. %.0f hisse (%.0f sn)", meta["hisse"], meta["havuz_ay"], H[H.any(axis=1)].sum(axis=1).mean() if H.any() else 0, time.time() - t0)
    O = {d: k60b_donem_olc(P, X["Sh"], H, d, X["bag"], Ek, Bk) for d in K60.K60_DONEM}
    T = pd.concat([O[d]["tablo"] for d in K60.K60_DONEM], ignore_index=True); Pl = pd.concat([O[d]["plasebo"] for d in K60.K60_DONEM], ignore_index=True)
    for k in ("aday_firsat", "aday_koruma", "bh_asim", "bh_koruma"):
        T[k] = False
    Sc = k60b_secim(T, O["kesif"]["plasebo"], Bk)
    Gd = k60b_gecis(T, O["dogrulama"]["plasebo"], Sc["aday"], "dogrulama", Bk); Gk = k60b_gecis(T, O["kasa"]["plasebo"], Sc["aday"], "kasa", Bk)
    Gke = k60b_gecis(T, O["kesif"]["plasebo"], [], "kesif", Bk)
    meta.update({"esik": Sc["esik"], "aday": Sc["aday"], "plasebo_dilim": {"kesif": Gke["plasebo"], "dogrulama": Gd["plasebo"], "kasa": Gk["plasebo"]},
                 "gecis": {"dogrulama": Gd["sonuc"], "kasa": Gk["sonuc"]}, "etiket": k60b_etiketler(Sc["aday"], Gd["sonuc"], Gk["sonuc"], Bk),
                 "havuz": {d: O[d]["ozet"] for d in K60.K60_DONEM}})
    cik = cikti or K60B_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    T.to_csv(_k60b_yol("tablo", cikti), index=False); Pl.to_csv(_k60b_yol("plasebo", cikti), index=False)
    pd.concat([O[d]["aylik"] for d in K60.K60_DONEM], ignore_index=True).to_csv(_k60b_yol("aylik", cikti), index=False)
    pd.concat([O[d]["portfoy"] for d in K60.K60_DONEM], ignore_index=True).to_csv(_k60b_yol("portfoy", cikti), index=False)
    meta["kos_bitis"] = K60._k60_simdi(); meta["sure_sn"] = round(time.time() - t0)
    with open(_k60b_yol("meta", cikti), "w", encoding="utf-8") as f:
        json.dump(K60._k60_yuvarla(meta, 12), f, ensure_ascii=False, indent=1, default=str)
    return {"tablo": T, "plasebo": Pl, "meta": meta, "rapor": k60b_rapor(cikti, Bk)}


# ---------------------------------------------------------------- 5) RAPOR
def _yuz(x: Any, n: int = 1) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return ("%" + f"{100 * v:.{n}f}".replace(".", ",")) if np.isfinite(v) else "—"


def _say(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return f"{v:.{n}f}".replace(".", ",") if np.isfinite(v) else "—"


def _ara(r: Any, ad: str, alt: str, ust: str) -> str:
    return f"{_say(_k60b_f(r, ad))} [{_say(_k60b_f(r, alt))}; {_say(_k60b_f(r, ust))}]"


def k60b_rapor(cikti: Optional[str] = None, B: Optional[Dict[str, Any]] = None) -> str:
    """K60B_RAPOR.md'yi k60b_tablo.csv ve k60b_meta.json'dan yazar."""
    B = B or K60B_ESIK; yt, ym = _k60b_yol("tablo", cikti), _k60b_yol("meta", cikti)
    if not (os.path.exists(yt) and os.path.exists(ym)):
        raise K60BHata(f"K60-B çıktıları yok ({yt}): önce `python -I K60B.py kos`")
    T = pd.read_csv(yt); au = B["olcu"]["ana_ufuk"]; T = T[T.ufuk == au]
    with open(ym, encoding="utf-8") as f:
        m = json.load(f)
    Et = B["etiket"]; ix = {(r["sinyal"], r["taraf"], r["donem"]): r for r in T.to_dict("records")}
    bas = ("| çift | dönem | ay | hisse-ay | P(+%100) uç / havuz | kat [%95] | P(-%50) uç / havuz | kat [%95] | ASIM [%95] | ort. uç / havuz | medyan uç / havuz | portföy net fazla | t(alfa) |\n"
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")

    def blok(ciftler: List[Tuple[str, str]]) -> str:
        out = []
        for s, t in ciftler:
            for d in K60.K60_DONEM:
                r = ix.get((s, t, d))
                if r is None:
                    out.append(f"| {s} ({'ÜST' if t == 'UST' else 'ALT'}) | {K60.K60_DONEM_AD[d]} | — | — | — | — | — | — | — | — | — | — | — |"); continue
                out.append(f"| {s} ({'ÜST' if t == 'UST' else 'ALT'}) | {K60.K60_DONEM_AD[d]} | {int(r['ay'])} | {_say(_k60b_f(r, 'n'), 0)} | {_yuz(_k60b_f(r, 'P_p100'))} / {_yuz(_k60b_f(r, 'havuz_p100'))} | "
                           f"{_ara(r, 'kat_p100', 'alt_p100', 'ust_p100')} | {_yuz(_k60b_f(r, 'P_m50'))} / {_yuz(_k60b_f(r, 'havuz_m50'))} | {_ara(r, 'kat_m50', 'alt_m50', 'ust_m50')} | "
                           f"{_ara(r, 'asim', 'asim_alt', 'asim_ust')} | {_yuz(_k60b_f(r, 'ort'))} / {_yuz(_k60b_f(r, 'havuz_ort'))} | {_yuz(_k60b_f(r, 'medyan'))} / {_yuz(_k60b_f(r, 'havuz_medyan'))} | "
                           f"{_yuz(_k60b_f(r, 'pf_fazla'))} | {_say(_k60b_f(r, 'pf_t_alfa'))} |")
        return bas + ("\n".join(out) if out else "| (çift yok) |" + " |" * 12)
    es = m["esik"]; et = m["etiket"]; hv = m["havuz"]
    par = [f"# K60-B — piyango havuzu içinde koşullu ayrım: RAPOR\n\n{K60B_SURUM}. Ön kayıt K60B_ON_KAYIT.md (sha256 {m['onkayit']['dosya_sha256'][:12]}, git "
           f"{str(m['onkayit'].get('git', {}).get('commit', ''))[:7]}); koşu {m['kos_baslangic']} → {m['kos_bitis']} ({m.get('sure_sn')} sn).\n",
           "## Bulgular (düz dille)\n"
           f"- Etiket alan: {sum(1 for x in et if x['etiket'] in (Et['firsat'], Et['koruma']))} çift ('{Et['firsat']}' {sum(1 for x in et if x['etiket'] == Et['firsat'])}, "
           f"'{Et['koruma']}' {sum(1 for x in et if x['etiket'] == Et['koruma'])}); YAKIN {sum(1 for x in et if x['etiket'].startswith(Et['yakin']))}. KEŞİF adayı {len(m['aday'])} "
           f"(FIRSAT {sum(1 for x in m['aday'] if x['yol'] == 'FIRSAT')}, KORUMA {sum(1 for x in m['aday'] if x['yol'] == 'KORUMA')}); ölçülen hipotez {es['hipotez']}.\n"
           "- Etiketler 'bilgi' düzeyindedir, İZ değildir (yalnız ABD, yalnız yaşayanlar; KASA K60'ta bir kez açılmıştı).\n",
           "## Havuz ve taban oranlar (12 ay; aynı aylarda havuz / bütün uygun evren)\n| dönem | oluşum ayı | havuz ort. hisse | evren ort. hisse | P(+%100) | P(-%50) | ortalama | medyan |\n|---|---|---|---|---|---|---|---|\n"
           + "\n".join(f"| {K60.K60_DONEM_AD[d]} | {hv[d]['ay_12']} | {_say(hv[d]['havuz_ort_hisse'], 0)} | {_say(hv[d]['evren_ort_hisse'], 0)} | {_yuz(hv[d]['havuz_p100'])} / {_yuz(hv[d]['evren_p100'])} | "
                       f"{_yuz(hv[d]['havuz_m50'])} / {_yuz(hv[d]['evren_m50'])} | {_yuz(hv[d]['havuz_ort'])} / {_yuz(hv[d]['evren_ort'])} | {_yuz(hv[d]['havuz_medyan'])} / {_yuz(hv[d]['evren_medyan'])} |"
                       for d in K60.K60_DONEM) + "\n",
           f"## KEŞİF seçimi\nPlasebo en-büyük ASIM eşiği {_say(es['asim_maks'], 3)} (200 plasebonun en büyüğü {_say(es['plasebo_asim_maks'], 3)}); plasebo en-küçük kat_m50 eşiği "
           f"{_say(es['kat_m50_min'], 3)} (en küçüğü {_say(es['plasebo_kat_m50_min'], 3)}). Adaylar ve sonraki dönemler:\n\n| aday | yol | DOĞRULAMA | KASA | etiket |\n|---|---|---|---|---|\n"
           + ("\n".join(f"| {x['sinyal']} ({'ÜST' if x['taraf'] == 'UST' else 'ALT'}) | {x['yol']} | {'geçti' if x['dogrulama'] else 'kaldı'} | {'geçti' if x['kasa'] else 'kaldı'} | {x['etiket'] or '—'} |"
                         for x in et) or "| (aday yok) | | | | |") + "\n",
           "### Adayların üç dönemi\n" + blok(list(dict.fromkeys((x["sinyal"], x["taraf"]) for x in m["aday"]))) + "\n",
           "## Plasebo: dönem dilimleri ve tek dönem şart sağlama oranı (plasebo dilim şartı hariç)\n| dönem | ASIM %95 | kat_m50 %5 | FIRSAT şartı | KORUMA şartı | not |\n|---|---|---|---|---|---|\n"
           + "\n".join(f"| {K60.K60_DONEM_AD[d]} | {_say(v['asim95'], 3)} | {_say(v['kat_m50_05'], 3)} | {_yuz(v['plasebo_firsat_oran'])} | {_yuz(v['plasebo_koruma_oran'])} | {'aralık dar' if v['aralik_dar'] else ''} |"
                       for d, v in m["plasebo_dilim"].items()) + "\n",
           "## Önceden adı konan başlık satırları (seçilsin seçilmesin)\n" + blok([(a, b) for a, b in B["baslik"]]) + "\n"]
    uc = [k for k in dict.fromkeys((r["sinyal"], r["taraf"]) for r in T.to_dict("records"))
          if all((k[0], k[1], d) in ix and _k60b_evet(ix[(k[0], k[1], d)]["olculdu"]) and _k60b_f(ix[(k[0], k[1], d)], "kat_m50") < 1 and _k60b_f(ix[(k[0], k[1], d)], "kat_p100") >= 1 for d in K60.K60_DONEM)]
    par.append(f"## Üç dönemde de kat_m50 < 1 ve kat_p100 >= 1 (nokta değer; bilgi, etiket değil): {len(uc)} çift\n" + blok(uc) + "\n")
    if m.get("not"):
        par.append("## Koşu notları\n" + "\n".join(f"- {x}" for x in m["not"]) + "\n")
    par.append("## BOŞLUK (ön kayıtta açık kalan yerler; en dar yorum)\n"
               "BOŞLUK 1. Havuz sayısı = max(1, yuvarla(0,20 x oynaklığı olan uygun hisse)); eşitlik K60'ın sabit tohumlu sırasıyla bozulur.\n"
               "BOŞLUK 2. Bir sinyalin ölçüm ayları = dönemin havuzlu ayları içinde sinyali olan havuz hissesi >= 100 (bayrakta bayraklı >= 10) olan aylar (ay ay atlanır).\n"
               "BOŞLUK 3. ASIM aralığı K60-EK kuralıyla: paydası sıfır olan çekiliş atlanır, geçerli çekiliş < 400 ise aralık yok ve şart SAĞLANMAZ; hesaplanamayan her ölçü şartı sağlamaz.\n"
               "BOŞLUK 4. REV_YOY kütüphanede ayrı sinyal değildir (K60'ta yalnız DOSYA_Y üyesi): başlık satırı olarak ölçüldü, hipotez ailesine ve seçime GİRMEZ.\n"
               "BOŞLUK 5. Bayrak başlık satırlarının ucu K60'taki gibidir (beklenen yön '-' olan E_S3, E_424B5, E_RSPLIT 'ALT' adıyla bayraklı gruptur).\n"
               "BOŞLUK 6. 'YAKIN': KEŞİF adayı, DOĞRULAMA ve KASA'dan biri tam geçti, ötekinde aralık / plasebo dışındaki şartlar tam ve nokta değerler doğru yönde.\n"
               "BOŞLUK 7. BH p değerleri: p_asim = 1 - Φ(ln ASIM / sd(ln ASIM çekilişleri)); p_koruma = 1 - Φ(-ln kat_m50 / sd(ln kat_m50 çekilişleri)); kat_m50 = 0 ise p yok.\n"
               "BOŞLUK 8. Aylık portföy kıyası havuzun eşit ağırlıklı getirisi; t(alfa) = portföy net getirisinin havuz getirisi üzerine sabitli EKK'sinde sabitin NW(6) t'si.\n"
               "BOŞLUK 9. Plasebo ölçüm ayları dönemin bütün havuzlu aylarıdır; plasebo ÜST %20 = max(1, yuvarla(0,20 x havuz hissesi)).\n"
               "BOŞLUK 10. 6 ay ufuk satırları k60b_tablo.csv'de (ufuk = 6) durur; raporda yalnız 12 ay.\n"
               "\n## Sınırlar\nKASA ikinci kez kullanıldı (K60'ta marjinal sonuçlar için açılmıştı). Yalnız yaşayanlar: havuz batanlara en açık yerdir; P(-%50) alt sınır, 'FIRSAT' yukarı yanlıdır.\n")
    metin = "\n".join(par); yol = _k60b_yol("rapor", cikti)
    if K60._K60_EPOSTA.search(metin):
        raise K60BHata("rapor metninde e-posta biçimli parça var; yazılmadı")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k60blog.info("rapor: %s", yol)
    return yol


def _cakisma_kontrol_k60b(_once=_CK_ONCE_K60B, _dosya="K60B.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K60B", "_CK_KAYIT", "_cakisma_kontrol_k60b", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "annotations", "Any", "Dict", "List", "Optional", "Tuple", "K60", "K58", "K59", "_yuz", "_say", "_ara")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k60b()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=K60B_SURUM)
    ap.add_argument("komut", choices=["kos", "rapor"])
    ap.add_argument("--cikti", default=None)
    a = ap.parse_args()
    try:
        if a.komut == "kos":
            R_ = k60b_kos(a.cikti)
            print("K60-B bitti:", json.dumps({"aday": R_["meta"]["aday"], "etiket": R_["meta"]["etiket"], "esik": R_["meta"]["esik"], "sure_sn": R_["meta"]["sure_sn"]}, ensure_ascii=False, default=str))
            print(R_["rapor"])
        else:
            print(k60b_rapor(a.cikti))
    except (K60BHata, K60.K60Hata, FileNotFoundError) as ex:
        k60blog.error("%s", ex); sys.exit(1)
